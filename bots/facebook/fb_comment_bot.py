"""
FB Comment Bot — Libertad Financiera Ya
Polls every 5 minutes, auto-replies as El Profe.
Run: python fb_comment_bot.py
"""

import json
import os
import re
import logging
from pathlib import Path

import anthropic
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

FB_PAGE_ACCESS_TOKEN = os.environ["FB_PAGE_ACCESS_TOKEN"]
FB_PAGE_ID = os.environ["FB_PAGE_ID"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
GRAPH_BASE = "https://graph.facebook.com/v21.0"
REPLIED_IDS_PATH = Path(__file__).parent / "replied_ids.json"

_EMOJI_RE = re.compile(
    "[\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "]+",
    flags=re.UNICODE,
)


def is_emoji_only(text: str) -> bool:
    """Return True if text contains no real word/character content."""
    stripped = _EMOJI_RE.sub("", text).strip()
    return stripped == ""


def load_replied_ids() -> set:
    """Load the set of already-replied comment IDs from disk."""
    if not REPLIED_IDS_PATH.exists():
        return set()
    return set(json.loads(REPLIED_IDS_PATH.read_text()))


def save_replied_ids(ids: set) -> None:
    """Save the set of replied comment IDs to disk as JSON."""
    REPLIED_IDS_PATH.write_text(json.dumps(list(ids)))


def parse_claude_response(raw: str) -> tuple[str, str]:
    """Parse Claude's JSON response. Returns (action, content) tuple.
    action is 'reply' or 'skip'. On parse failure returns ('skip', reason).
    """
    try:
        data = json.loads(raw)
        action = data.get("action")
        if action == "reply":
            return "reply", data.get("reply", "")
        if action == "skip":
            return "skip", data.get("reason", "")
        return "skip", f"unknown action: {action}"
    except (json.JSONDecodeError, AttributeError) as exc:
        return "skip", f"parse error: {exc}"


def fetch_comments() -> list[dict]:
    """Return list of {comment_id, comment_text, post_text} for recent comments."""
    posts_url = f"{GRAPH_BASE}/{FB_PAGE_ID}/posts"
    posts_resp = requests.get(
        posts_url,
        params={"fields": "id,message", "limit": 10, "access_token": FB_PAGE_ACCESS_TOKEN},
        timeout=15,
    )
    posts_resp.raise_for_status()
    posts = posts_resp.json().get("data", [])

    results = []
    for post in posts:
        post_id = post.get("id")
        post_text = post.get("message", "")
        comments_url = f"{GRAPH_BASE}/{post_id}/comments"
        comments_resp = requests.get(
            comments_url,
            params={"fields": "id,message,from", "limit": 100, "access_token": FB_PAGE_ACCESS_TOKEN},
            timeout=15,
        )
        comments_resp.raise_for_status()
        for comment in comments_resp.json().get("data", []):
            results.append({
                "comment_id": comment["id"],
                "comment_text": comment.get("message", ""),
                "post_text": post_text,
            })
    return results


def post_reply(comment_id: str, reply_text: str) -> None:
    """Post a reply to a Facebook comment."""
    url = f"{GRAPH_BASE}/{comment_id}/replies"
    resp = requests.post(
        url,
        params={"access_token": FB_PAGE_ACCESS_TOKEN},
        data={"message": reply_text},
        timeout=15,
    )
    resp.raise_for_status()
    logger.info("Replied to comment %s", comment_id)
