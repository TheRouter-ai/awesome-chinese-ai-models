#!/usr/bin/env python3
"""Broadcast high-signal Chinese AI model updates to a Telegram channel.

Reads data/news.yaml, picks the highest-signal events for a date range, and
posts a compact message to the channel via the Telegram Bot API.

Standard library only. Credentials come from environment variables:

    ACAM_TELEGRAM_BOT_TOKEN   bot token from @BotFather
    ACAM_TELEGRAM_CHANNEL     channel id, e.g. @ChineseAIModels

Usage:
    python3 scripts/broadcast_telegram.py --date 2026-05-22
    python3 scripts/broadcast_telegram.py --date 2026-05-22 --dry-run
    python3 scripts/broadcast_telegram.py --since 2026-05-16 --weekly
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
NEWS = ROOT / "data" / "news.yaml"
REPO_URL = "https://github.com/TheRouter-ai/awesome-chinese-ai-models"

# Categories that are worth broadcasting, highest priority first.
PRIORITY = {"pricing": 5, "model_update": 4, "open_source": 3, "benchmark": 3, "api_update": 2}
MAX_ITEMS = 8


def load_news() -> list[dict]:
    with NEWS.open("r", encoding="utf-8") as f:
        return (yaml.safe_load(f) or {}).get("news", [])


def parse_date(value: str | None) -> date | None:
    try:
        return date.fromisoformat(str(value or "")[:10])
    except ValueError:
        return None


def select_items(news: list[dict], start: date, end: date) -> list[dict]:
    picked = []
    for item in news:
        item_date = parse_date(item.get("date"))
        if item_date is None or not (start <= item_date <= end):
            continue
        picked.append(item)

    def rank(item: dict) -> tuple[int, int]:
        return (PRIORITY.get(item.get("category", ""), 0), int(item.get("score", 0)))

    picked.sort(key=rank, reverse=True)
    return picked[:MAX_ITEMS]


def escape_md(text: str) -> str:
    for ch in ("_", "*", "[", "]", "`"):
        text = text.replace(ch, "\\" + ch)
    return text


def render_message(items: list[dict], start: date, end: date, weekly: bool) -> str:
    if weekly:
        header = f"📅 *This Week in China AI Models* ({start.isoformat()} → {end.isoformat()})"
    else:
        header = f"🤖 *Chinese AI Models — {end.isoformat()}*"
    lines = [header, ""]
    if not items:
        lines.append("No high-signal updates in this window.")
    for item in items:
        title = escape_md(item.get("title", "Untitled"))
        url = (item.get("source") or {}).get("url", "")
        category = item.get("category", "update")
        entry = f"• `{category}` [{title}]({url})" if url else f"• `{category}` {title}"
        lines.append(entry)
    lines.append("")
    lines.append(f"Full index → {REPO_URL}")
    return "\n".join(lines)


def send(token: str, channel: str, text: str) -> dict:
    payload = urlencode(
        {
            "chat_id": channel,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")
    request = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--since", default=None, help="start date (inclusive); defaults to --date")
    parser.add_argument("--weekly", action="store_true", help="format as a weekly digest")
    parser.add_argument("--dry-run", action="store_true", help="print the message, do not send")
    args = parser.parse_args()

    end = date.fromisoformat(args.date)
    start = date.fromisoformat(args.since) if args.since else end

    items = select_items(load_news(), start, end)
    message = render_message(items, start, end, args.weekly)

    if args.dry_run:
        print("--- DRY RUN: message that would be sent ---")
        print(message)
        print(f"--- {len(items)} item(s) selected ---")
        return 0

    token = os.environ.get("ACAM_TELEGRAM_BOT_TOKEN")
    channel = os.environ.get("ACAM_TELEGRAM_CHANNEL")
    if not token or not channel:
        print("ACAM_TELEGRAM_BOT_TOKEN and ACAM_TELEGRAM_CHANNEL must be set.", file=sys.stderr)
        return 2

    result = send(token, channel, message)
    if not result.get("ok"):
        print(f"Telegram API error: {result}", file=sys.stderr)
        return 1
    print(f"Sent broadcast with {len(items)} item(s) to {channel}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
