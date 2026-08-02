#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import ssl
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen


ORCID_API = "https://pub.orcid.org/v3.0/{orcid}/record"


@dataclass(frozen=True)
class WorkEntry:
    year: str
    title: str
    venue: str
    doi: str


def _related_links_for_title(title: str) -> list[str]:
    title_lower = title.lower()
    links: list[str] = []

    if "gravitational wave" in title_lower:
        links.append("project: [Research Projects](/pages/research/projects/)")
        links.append("seminar: [Undergraduate Seminar](/pages/seminar/)")
    if "ai generated text" in title_lower or "llm" in title_lower:
        links.append("project: [Research Projects](/pages/research/projects/)")
        links.append("outreach: [Topology and AI article](/pages/social/topology-ai/)")
    if "segmentation" in title_lower or "mutual information" in title_lower:
        links.append("seminar session: [Undergraduate Seminar](/pages/seminar/)")
        links.append("project: [Research Projects](/pages/research/projects/)")

    deduped: list[str] = []
    seen: set[str] = set()
    for item in links:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _fetch_orcid_record(orcid_id: str) -> dict[str, Any]:
    request = Request(
        ORCID_API.format(orcid=orcid_id),
        headers={"Accept": "application/vnd.orcid+json"},
    )

    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except URLError:
        context = ssl._create_unverified_context()
        with urlopen(request, context=context, timeout=30) as response:
            return json.load(response)


def _text_value(node: Any, *path: str) -> str:
    current = node
    for key in path:
        if not isinstance(current, dict):
            return ""
        current = current.get(key)
    return current if isinstance(current, str) else ""


def _collect_work_entries(record: dict[str, Any]) -> list[WorkEntry]:
    groups = record.get("activities-summary", {}).get("works", {}).get("group", [])
    entries: list[WorkEntry] = []
    seen_keys: set[str] = set()

    for group in groups:
        summaries = group.get("work-summary", []) or []
        if not summaries:
            continue

        summary = max(
            summaries,
            key=lambda item: (
                len(_text_value(item, "title", "title", "value")),
                1 if _text_value(item, "journal-title", "value") else 0,
                1 if any(
                    external_id.get("external-id-type") == "doi"
                    for external_id in item.get("external-ids", {}).get("external-id", []) or []
                ) else 0,
            ),
        )
        title = _text_value(summary, "title", "title", "value")
        year = _text_value(summary, "publication-date", "year", "value")
        venue = _text_value(summary, "journal-title", "value")

        doi = ""
        for external_id in summary.get("external-ids", {}).get("external-id", []) or []:
            if external_id.get("external-id-type") == "doi":
                doi = external_id.get("external-id-value", "")
                break

        if title:
            dedupe_key = doi.lower() if doi else f"{year}|{title.lower()}|{venue.lower()}"
            if dedupe_key in seen_keys:
                continue
            seen_keys.add(dedupe_key)
            entries.append(WorkEntry(year=year, title=title, venue=venue, doi=doi))

    entries.sort(key=lambda entry: (entry.year or "0000", entry.title), reverse=True)
    return entries


def _format_publications_page(orcid_id: str, entries: list[WorkEntry]) -> str:
    lines = [
        "Title: Publications",
        "Date: 2026-07-09",
        "URL: pages/research/publications/",
        "Save_as: pages/research/publications/index.html",
        "",
        f"This page is generated automatically from the public ORCID record for [{orcid_id}](https://orcid.org/{orcid_id}).",
        "",
        "## Selected publications",
        "",
    ]

    for entry in entries:
        venue_text = f" {entry.venue}" if entry.venue else ""
        doi_text = f" DOI: [{entry.doi}](https://doi.org/{entry.doi})" if entry.doi else ""
        related_links = _related_links_for_title(entry.title)
        related_text = f" Related: {'; '.join(related_links)}" if related_links else ""
        lines.append(f"* **{entry.year or 'n.d.'}**. {entry.title}.{venue_text}{doi_text}{related_text}")

    lines.extend([
        "",
        "## Full record",
        "",
        "The full and most up-to-date publication list should remain on ORCID. This page is regenerated from the public record during the build.",
        "",
        "## Related content",
        "",
        "<div class=\"ds-related-module\">",
        "<p>Continue through project pages, teaching materials, and seminar sessions connected to these publications:</p>",
        "<ul class=\"ds-reference-list\">",
        "<li>[Research Projects](/pages/research/projects/)</li>",
        "<li>[Undergraduate Seminar](/pages/seminar/)</li>",
        "<li>[Courses and teaching materials](/pages/courses/)</li>",
        "<li>[Repositories and learning notes](/pages/repositories/)</li>",
        "</ul>",
        "</div>",
    ])
    return "\n".join(lines) + "\n"


def _format_research_page(orcid_id: str, entries: list[WorkEntry]) -> str:
    featured = entries[:3]
    lines = [
        "Title: Research",
        "Date: 2026-07-09",
        "URL: pages/research/",
        "Save_as: pages/research/index.html",
        "",
        "This is the research hub for current projects, publications, and ORCID-linked output.",
        "",
        f"My public record is connected to ORCID iD [{orcid_id}](https://orcid.org/{orcid_id}).",
        "",
        "## Research tree",
        "",
        "* [Projects](projects/): active collaborations, grants, and work in progress.",
        "* [Publications](publications/): selected papers and ORCID-linked records.",
        "",
        "## At a glance",
        "",
        "* Current position: Professor, Instituto Tecnológico y de Estudios Superiores de Monterrey, Monterrey, Nuevo Leon, MX",
        "* Office: A7-222, Campus Monterrey",
        "* Teaching areas: topological data science, mathematics, and modeling",
        "* Previous position: Postdoc, Institut de mathématiques de Jussieu Paris Rive Gauche, Paris, Île-de-France, FR",
        "* Education: Ph.D., Universidad Nacional Autónoma de México, Instituto de Matemáticas Unidad Cuernavaca",
        "* Doctoral advisor: Dr. Jose Seade",
        "* Postdoctoral mentor: Dr. Elisha Falbel",
        "* Service: reviewer for Mathematical Reviews; member of Sociedad Matemática Mexicana; former SNI candidate",
        "",
        "## Short summary",
        "",
        "My research profile spans geometry, complex analysis, Kleinian groups, and related geometric-analytic topics, with recent work in topological data analysis, neural-network methods, and detection of LLM-generated text.",
        "",
        "## Related IDs",
        "",
        "* Scopus Author ID: 57193900366",
        "* ResearcherID: OTI-7073-2025",
        "",
        "## Featured publications",
        "",
    ]

    if featured:
        for entry in featured:
            venue_text = f" {entry.venue}" if entry.venue else ""
            doi_text = f" DOI: [{entry.doi}](https://doi.org/{entry.doi})" if entry.doi else ""
            related_links = _related_links_for_title(entry.title)
            related_text = f" Related: {'; '.join(related_links)}" if related_links else ""
            lines.append(f"* **{entry.year or 'n.d.'}**. {entry.title}.{venue_text}{doi_text}{related_text}")
    else:
        lines.append("* No works were found in the public ORCID record.")

    lines.extend([
        "",
        "## Related content",
        "",
        "<div class=\"ds-related-module\">",
        "<p>Move across the research narrative:</p>",
        "<ul class=\"ds-reference-list\">",
        "<li>[Research Projects](projects/)</li>",
        "<li>[Publications](publications/)</li>",
        "<li>[Undergraduate Seminar](/pages/seminar/)</li>",
        "<li>[Repositories and learning notes](/pages/repositories/)</li>",
        "</ul>",
        "</div>",
    ])

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync Pelican content from a public ORCID record")
    parser.add_argument("--orcid", default=os.environ.get("ORCID_ID", "0000-0002-0037-9394"))
    parser.add_argument(
        "--content-dir",
        default="content/pages/research",
        help="Path to the research content directory that should be rewritten",
    )
    args = parser.parse_args()

    content_dir = Path(args.content_dir)
    research_path = content_dir / "index.md"
    publications_path = content_dir / "publications.md"

    try:
        record = _fetch_orcid_record(args.orcid)
    except Exception as error:  # pragma: no cover - defensive fallback path
        if research_path.exists() and publications_path.exists():
            print(
                "Warning: ORCID sync failed; keeping existing research pages at "
                f"{content_dir}. Reason: {error}"
            )
            return 0
        raise RuntimeError(
            "ORCID sync failed and no existing research pages are available for fallback"
        ) from error

    entries = _collect_work_entries(record)
    content_dir.mkdir(parents=True, exist_ok=True)

    (content_dir / "index.md").write_text(_format_research_page(args.orcid, entries), encoding="utf-8")
    (content_dir / "publications.md").write_text(_format_publications_page(args.orcid, entries), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())