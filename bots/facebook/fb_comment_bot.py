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
