import os
import sys
import importlib.util

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
