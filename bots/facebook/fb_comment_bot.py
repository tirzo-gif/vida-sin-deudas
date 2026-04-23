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
