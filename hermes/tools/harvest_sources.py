#!/usr/bin/env python3
"""
Fetch allowlisted vendor RSS feeds and write a dated markdown corpus.

Stdlib only — safe to run on the VPS without uv.

Usage:
  python3 hermes/tools/harvest_sources.py
  python3 hermes/tools/harvest_sources.py --days 30 --out content/source-corpus/2026-10-30.md
  python3 hermes/tools/harvest_sources.py --keywords "agent,bedrock,rag"
"""

from __future__ import annotations

import argparse
import email.utils
import json
import re
import sys
import textwrap
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = REPO_ROOT / "hermes" / "sources" / "verified-sources.json"
DEFAULT_OUT_DIR = REPO_ROOT / "content" / "source-corpus"

USER_AGENT = "AgenticArchitecture-SourceHarvester/1.0 (+learning-in-public; RSS only)"


@dataclass
class FeedItem:
    feed_id: str
    publisher: str
    title: str
    link: str
    published: datetime | None
    summary: str


def load_config(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def host_allowed(link: str, allowed_hosts: Iterable[str]) -> bool:
    host = (urlparse(link).hostname or "").lower()
    if not host:
        return False
    for suffix in allowed_hosts:
        suffix = suffix.lower()
        if host == suffix or host.endswith("." + suffix):
            return True
    return False


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_rss(xml_bytes: bytes, feed_id: str, publisher: str) -> list[FeedItem]:
    root = ET.fromstring(xml_bytes)
    items: list[FeedItem] = []

    # RSS 2.0
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_raw = item.findtext("pubDate") or item.findtext("{http://purl.org/dc/elements/1.1/}date")
        published = None
        if pub_raw:
            try:
                published = email.utils.parsedate_to_datetime(pub_raw)
                if published.tzinfo is None:
                    published = published.replace(tzinfo=timezone.utc)
            except (TypeError, ValueError):
                published = None
        desc = item.findtext("description") or ""
        enc = item.findtext("{http://purl.org/rss/1/modules/content/}encoded") or ""
        summary = strip_html(enc or desc)
        if title and link:
            items.append(
                FeedItem(feed_id, publisher, title, link, published, summary[:4000])
            )

    # Atom
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//atom:entry", ns):
        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
        link_el = entry.find("atom:link[@rel='alternate']", ns) or entry.find("atom:link", ns)
        link = (link_el.get("href") if link_el is not None else "") or ""
        updated = entry.findtext("atom:updated", default="", namespaces=ns) or entry.findtext(
            "atom:published", default="", namespaces=ns
        )
        published = None
        if updated:
            try:
                published = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            except ValueError:
                published = None
        summary = strip_html(
            entry.findtext("atom:summary", default="", namespaces=ns)
            or entry.findtext("atom:content", default="", namespaces=ns)
        )
        if title and link:
            items.append(
                FeedItem(feed_id, publisher, title, link, published, summary[:4000])
            )

    return items


def parse_html_list_page(
    html: str,
    page_id: str,
    publisher: str,
    page_url: str,
    link_path_prefix: str,
    allowed_hosts: Iterable[str],
) -> list[FeedItem]:
    """Extract recent news links from a static index page (no RSS)."""
    items: list[FeedItem] = []
    seen: set[str] = set()
    for match in re.finditer(r'href="(/[^"#?]+)"', html):
        path = match.group(1)
        if not path.startswith(link_path_prefix) or path.rstrip("/") == link_path_prefix.rstrip("/"):
            continue
        link = urljoin(page_url, path)
        if link in seen:
            continue
        if not host_allowed(link, allowed_hosts):
            continue
        seen.add(link)
        slug = path.strip("/").split("/")[-1].replace("-", " ").title()
        items.append(
            FeedItem(
                feed_id=page_id,
                publisher=publisher,
                title=slug,
                link=link,
                published=None,
                summary="(HTML index entry — open URL for full text; do not invent body content.)",
            )
        )
    return items[:40]


def fetch_feed(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def keyword_match(item: FeedItem, keywords: list[str]) -> bool:
    if not keywords:
        return True
    blob = f"{item.title} {item.summary} {item.link}".lower()
    return any(k.lower() in blob for k in keywords)


def write_corpus(
    path: Path,
    items: list[FeedItem],
    config: dict,
    days: int,
    keywords: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    lines = [
        "# Vendor source corpus",
        "",
        f"**Generated (UTC):** {now.strftime('%Y-%m-%d %H:%M')}",
        f"**Window:** last {days} days",
        f"**Keyword filter:** {', '.join(keywords) if keywords else '(none — all items in window)'}",
        "",
        "Use this file for grounding. Do not cite vendor claims that are not supported here or in official doc roots.",
        "",
        f"Config: `hermes/sources/verified-sources.json` (version {config.get('version')})",
        "",
        "## Entries",
        "",
    ]
    for i, item in enumerate(sorted(items, key=lambda x: x.published or datetime.min.replace(tzinfo=timezone.utc), reverse=True), start=1):
        pub = item.published.strftime("%Y-%m-%d") if item.published else "unknown-date"
        lines.extend(
            [
                f"### {i}. {item.title}",
                "",
                f"- **Publisher:** {item.publisher} (`{item.feed_id}`)",
                f"- **URL:** {item.link}",
                f"- **Published:** {pub}",
                "",
                textwrap.fill(item.summary or "(no summary in feed)", width=88),
                "",
            ]
        )
    lines.append(f"_Total entries: {len(items)}_")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Harvest allowlisted vendor RSS into markdown corpus")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--days", type=int, default=14, help="Include items published within this many days")
    parser.add_argument("--keywords", type=str, default="", help="Comma-separated optional filter")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output markdown path (default: content/source-corpus/YYYY-MM-DD.md)",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    allowed_hosts = config.get("allowed_link_hosts", [])
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)

    out_path = args.out or (DEFAULT_OUT_DIR / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.md")

    collected: list[FeedItem] = []
    errors: list[str] = []

    for feed in config.get("feeds", []):
        feed_id = feed.get("id", "unknown")
        publisher = feed.get("publisher", "Unknown")
        url = feed.get("url")
        if not url:
            continue
        try:
            xml_bytes = fetch_feed(url)
            for item in parse_rss(xml_bytes, feed_id, publisher):
                if not host_allowed(item.link, allowed_hosts):
                    continue
                if item.published and item.published < cutoff:
                    continue
                if keyword_match(item, keywords):
                    collected.append(item)
        except (urllib.error.URLError, ET.ParseError, TimeoutError) as exc:
            errors.append(f"{feed_id}: {exc}")

    for page in config.get("html_list_pages", []):
        page_id = page.get("id", "html-index")
        publisher = page.get("publisher", "Unknown")
        url = page.get("url")
        prefix = page.get("link_path_prefix", "/")
        if not url:
            continue
        try:
            html = fetch_feed(url).decode("utf-8", errors="replace")
            for item in parse_html_list_page(html, page_id, publisher, url, prefix, allowed_hosts):
                if keyword_match(item, keywords):
                    collected.append(item)
        except (urllib.error.URLError, TimeoutError) as exc:
            errors.append(f"{page_id}: {exc}")

    write_corpus(out_path, collected, config, args.days, keywords)

    latest = DEFAULT_OUT_DIR / "latest.md"
    latest.write_text(out_path.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"Wrote {len(collected)} entries to {out_path}")
    print(f"Updated {latest}")
    if errors:
        print("Feed errors (check URLs in verified-sources.json):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
    if not collected:
        return 1
    return 0 if not errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
