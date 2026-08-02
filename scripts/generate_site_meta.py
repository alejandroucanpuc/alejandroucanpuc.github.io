#!/usr/bin/env python3
"""Generate operational metadata files for the built static site.

Creates:
- sitemap.xml
- robots.txt
- optional feeds/updates.xml from changelog entries
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import pathlib
import re
import xml.etree.ElementTree as ET


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate sitemap/robots/updates feed")
    parser.add_argument("--output-dir", default="output", help="Built site output directory")
    parser.add_argument(
        "--site-url",
        default="https://alejandroucanpuc.github.io",
        help="Canonical site URL (e.g. https://example.com)",
    )
    parser.add_argument(
        "--changelog-file",
        default="content/pages/changelog/index.md",
        help="Markdown changelog source file",
    )
    parser.add_argument(
        "--enable-updates-rss",
        action="store_true",
        help="Generate feeds/updates.xml from changelog entries",
    )
    return parser.parse_args()


def canonical_site_url(url: str) -> str:
    return url.rstrip("/")


def to_public_path(output_dir: pathlib.Path, html_file: pathlib.Path) -> str:
    rel = html_file.relative_to(output_dir).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    if rel.endswith(".html"):
        return "/" + rel
    return "/" + rel


def iter_sitemap_urls(output_dir: pathlib.Path, site_url: str) -> list[tuple[str, str]]:
    urls: list[tuple[str, str]] = []

    for html_file in sorted(output_dir.rglob("*.html")):
        rel = html_file.relative_to(output_dir).as_posix()

        if rel == "404.html":
            continue
        if rel.startswith("feeds/"):
            continue

        loc = site_url + to_public_path(output_dir, html_file)
        lastmod = dt.datetime.fromtimestamp(html_file.stat().st_mtime, tz=dt.timezone.utc)
        urls.append((loc, lastmod.date().isoformat()))

    return urls


def write_sitemap(output_dir: pathlib.Path, site_url: str) -> None:
    urlset = ET.Element("urlset", {"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})

    for loc, lastmod in iter_sitemap_urls(output_dir, site_url):
        url_node = ET.SubElement(urlset, "url")
        ET.SubElement(url_node, "loc").text = loc
        ET.SubElement(url_node, "lastmod").text = lastmod

    tree = ET.ElementTree(urlset)
    sitemap_path = output_dir / "sitemap.xml"
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)


def write_robots(output_dir: pathlib.Path, site_url: str) -> None:
    robots_content = "\n".join(
        [
            "User-agent: *",
            "Allow: /",
            "",
            f"Sitemap: {site_url}/sitemap.xml",
            "",
        ]
    )
    (output_dir / "robots.txt").write_text(robots_content, encoding="utf-8")


def parse_changelog_entries(changelog_file: pathlib.Path) -> list[dict[str, str | list[str]]]:
    if not changelog_file.exists():
        return []

    lines = changelog_file.read_text(encoding="utf-8").splitlines()
    entries: list[dict[str, str | list[str]]] = []
    in_body = False
    current: dict[str, str | list[str]] | None = None

    heading_re = re.compile(r"^##\s+v(?P<version>[0-9]+\.[0-9]+\.[0-9]+)\s+-\s+(?P<date>\d{4}-\d{2}-\d{2})\s*$")
    bullet_re = re.compile(r"^\s*[-*]\s+(?P<text>.+?)\s*$")

    for line in lines:
        stripped = line.strip()

        if not in_body:
            if stripped == "":
                continue
            if stripped.startswith("---") or ":" in stripped:
                continue
            in_body = True

        match = heading_re.match(stripped)
        if match:
            if current:
                entries.append(current)
            current = {
                "version": match.group("version"),
                "date": match.group("date"),
                "items": [],
            }
            continue

        if current:
            bullet_match = bullet_re.match(line)
            if bullet_match:
                items = current["items"]
                assert isinstance(items, list)
                items.append(bullet_match.group("text"))

    if current:
        entries.append(current)

    return entries


def build_rss_item_description(items: list[str]) -> str:
    if not items:
        return ""
    parts = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f"<ul>{parts}</ul>"


def write_updates_rss(output_dir: pathlib.Path, site_url: str, changelog_file: pathlib.Path) -> None:
    entries = parse_changelog_entries(changelog_file)
    if not entries:
        return

    feed_dir = output_dir / "feeds"
    feed_dir.mkdir(parents=True, exist_ok=True)
    feed_path = feed_dir / "updates.xml"

    now = dt.datetime.now(dt.timezone.utc)
    pub_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Alejandro Ucan-Puc - Site Updates"
    ET.SubElement(channel, "link").text = f"{site_url}/pages/changelog/"
    ET.SubElement(channel, "description").text = "Versioned changelog and operational updates."
    ET.SubElement(channel, "language").text = "en"
    ET.SubElement(channel, "lastBuildDate").text = pub_date

    for entry in entries:
        version = str(entry["version"])
        date_str = str(entry["date"])
        items = entry["items"]
        assert isinstance(items, list)

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = f"v{version}"
        ET.SubElement(item, "link").text = f"{site_url}/pages/changelog/#v{version.replace('.', '')}"
        ET.SubElement(item, "guid").text = f"{site_url}/pages/changelog/#v{version.replace('.', '')}"

        parsed_date = dt.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
        ET.SubElement(item, "pubDate").text = parsed_date.strftime("%a, %d %b %Y 00:00:00 +0000")

        description = ET.SubElement(item, "description")
        description.text = build_rss_item_description(items)

    ET.ElementTree(rss).write(feed_path, encoding="utf-8", xml_declaration=True)


def main() -> None:
    args = parse_args()

    output_dir = pathlib.Path(args.output_dir)
    site_url = canonical_site_url(args.site_url)
    changelog_file = pathlib.Path(args.changelog_file)

    output_dir.mkdir(parents=True, exist_ok=True)

    write_sitemap(output_dir, site_url)
    write_robots(output_dir, site_url)

    if args.enable_updates_rss:
        write_updates_rss(output_dir, site_url, changelog_file)


if __name__ == "__main__":
    main()
