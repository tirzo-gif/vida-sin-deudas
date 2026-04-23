import os
import sys
import importlib.util
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

# Set environment variables BEFORE importing the module
os.environ.setdefault("FB_PAGE_ACCESS_TOKEN", "x")
os.environ.setdefault("FB_PAGE_ID", "x")
os.environ.setdefault("ANTHROPIC_API_KEY", "x")

# Import the module directly from file path
spec = importlib.util.spec_from_file_location(
    "fb_comment_bot",
    "/Users/tirzoquintero/Desktop/Claude/Vida sin Deudas/.worktrees/fb-comment-bot/bots/facebook/fb_comment_bot.py"
)
fb_comment_bot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb_comment_bot)

is_emoji_only = fb_comment_bot.is_emoji_only
load_replied_ids = fb_comment_bot.load_replied_ids
save_replied_ids = fb_comment_bot.save_replied_ids


def test_emoji_only_single():
    assert is_emoji_only("👍") is True


def test_emoji_only_multiple():
    assert is_emoji_only("😍🔥💯") is True


def test_emoji_only_with_text():
    assert is_emoji_only("buen video 👍") is False


def test_emoji_only_plain_text():
    assert is_emoji_only("Excelente consejo") is False


def test_emoji_only_empty():
    assert is_emoji_only("") is True


def test_emoji_only_whitespace_and_emoji():
    assert is_emoji_only("  🎉  ") is True


def test_emoji_only_punctuation_with_emoji():
    assert is_emoji_only("👍!") is False


def test_load_replied_ids_missing_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "replied_ids.json"
        with patch.object(fb_comment_bot, "REPLIED_IDS_PATH", path):
            result = load_replied_ids()
    assert result == set()


def test_save_and_load_replied_ids_roundtrip():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "replied_ids.json"
        ids = {"123", "456", "789"}
        with patch.object(fb_comment_bot, "REPLIED_IDS_PATH", path):
            save_replied_ids(ids)
            result = load_replied_ids()
    assert result == ids


def test_save_replied_ids_writes_json_array():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "replied_ids.json"
        with patch.object(fb_comment_bot, "REPLIED_IDS_PATH", path):
            save_replied_ids({"abc"})
        content = json.loads(path.read_text())
    assert isinstance(content, list)
    assert "abc" in content
