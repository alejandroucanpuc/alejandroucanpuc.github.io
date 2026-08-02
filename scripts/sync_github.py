#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import ssl
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GITHUB_REPOS_API = "https://api.github.com/users/{username}/repos"
DEFAULT_OVERRIDES = "content/extra/github_repositories_overrides.json"
DEFAULT_OUTPUT = "content/pages/repositories/index.md"


@dataclass(frozen=True)
class Repository:
    name: str
    html_url: str
    description: str
    language: str
    is_fork: bool
    stargazers_count: int
    archived: bool
    pushed_at: str


@dataclass(frozen=True)
class CuratedItem:
    name: str
    note: str


def _read_json_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data if isinstance(data, dict) else {}


def _github_headers(token: str | None) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "alejandroucanpuc-site-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _fetch_json(request: Request) -> Any:
    try:
        with urlopen(request, timeout=30) as response:
            return json.load(response)
    except URLError:
        context = ssl._create_unverified_context()
        with urlopen(request, context=context, timeout=30) as response:
            return json.load(response)


def _fetch_all_repositories(username: str, token: str | None) -> list[Repository]:
    page = 1
    repos: list[Repository] = []

    while True:
        query = urlencode({"type": "owner", "per_page": 100, "page": page, "sort": "pushed"})
        url = f"{GITHUB_REPOS_API.format(username=username)}?{query}"
        request = Request(url, headers=_github_headers(token))

        try:
            payload = _fetch_json(request)
        except HTTPError as error:
            if error.code == 404:
                raise RuntimeError(f"GitHub user '{username}' was not found") from error
            raise RuntimeError(f"GitHub API request failed with status {error.code}") from error

        if not isinstance(payload, list):
            raise RuntimeError("Unexpected payload from GitHub API")

        if not payload:
            break

        for repo in payload:
            if not isinstance(repo, dict):
                continue
            repos.append(
                Repository(
                    name=str(repo.get("name", "")),
                    html_url=str(repo.get("html_url", "")),
                    description=str(repo.get("description") or "").strip(),
                    language=str(repo.get("language") or ""),
                    is_fork=bool(repo.get("fork", False)),
                    stargazers_count=int(repo.get("stargazers_count", 0) or 0),
                    archived=bool(repo.get("archived", False)),
                    pushed_at=str(repo.get("pushed_at") or ""),
                )
            )

        if len(payload) < 100:
            break
        page += 1

    repos.sort(key=lambda repo: (repo.pushed_at, repo.stargazers_count, repo.name.lower()), reverse=True)
    return repos


def _parse_curated_items(raw_items: Any) -> list[CuratedItem]:
    curated: list[CuratedItem] = []
    if not isinstance(raw_items, list):
        return curated

    for raw in raw_items:
        if isinstance(raw, str):
            name = raw.strip()
            if name:
                curated.append(CuratedItem(name=name, note=""))
            continue

        if not isinstance(raw, dict):
            continue

        name = str(raw.get("name", "")).strip()
        note = str(raw.get("note", "")).strip()
        if name:
            curated.append(CuratedItem(name=name, note=note))

    return curated


def _repo_lookup(repositories: list[Repository]) -> dict[str, Repository]:
    lookup: dict[str, Repository] = {}
    for repo in repositories:
        lookup[repo.name.lower()] = repo
    return lookup


def _format_repository_item(repo: Repository, manual_note: str = "") -> str:
    language_text = f" ({repo.language})" if repo.language else ""
    description = manual_note or repo.description or "No description provided yet."
    if repo.archived:
        description = f"{description} [archived]"
    return f"* **[{repo.name}]({repo.html_url})**{language_text}: {description}"


def _build_curated_section(
    curated: list[CuratedItem],
    repo_by_name: dict[str, Repository],
    expected_fork_state: bool,
) -> tuple[list[str], list[str]]:
    lines: list[str] = []
    missing: list[str] = []

    for item in curated:
        repo = repo_by_name.get(item.name.lower())
        if repo is None:
            missing.append(item.name)
            continue
        if repo.is_fork != expected_fork_state:
            continue
        lines.append(_format_repository_item(repo, item.note))

    return lines, missing


def _build_recent_section(
    repositories: list[Repository],
    curated_names: set[str],
    excluded_names: set[str],
    max_items: int,
    include_forks: bool,
) -> list[str]:
    if max_items <= 0:
        return []

    lines: list[str] = []
    for repo in repositories:
        repo_key = repo.name.lower()
        if repo_key in curated_names:
            continue
        if repo_key in excluded_names:
            continue
        if repo.is_fork and not include_forks:
            continue
        lines.append(_format_repository_item(repo))
        if len(lines) >= max_items:
            break

    return lines


def _format_page(
    username: str,
    date_value: str,
    description_text: str,
    featured_lines: list[str],
    fork_lines: list[str],
    recent_lines: list[str],
    learning_log: list[str],
    missing_names: list[str],
) -> str:
    lines = [
        "Title: Repositories and Learning Notes",
        f"Date: {date_value}",
        f"Description: {description_text}",
        "URL: pages/repositories/",
        "Save_as: pages/repositories/index.html",
        "",
        "This page is generated automatically from the public GitHub API and manual curation overrides.",
        "",
        f"GitHub profile: [github.com/{username}](https://github.com/{username}?tab=repositories)",
        "",
        "## Featured public repositories",
        "",
    ]

    if featured_lines:
        lines.extend(featured_lines)
    else:
        lines.append("* No curated repositories were resolved from the current public profile.")

    lines.extend(["", "## Public forks used for exploration", ""])

    if fork_lines:
        lines.extend(fork_lines)
    else:
        lines.append("* No curated forks were resolved from the current public profile.")

    if recent_lines:
        lines.extend(["", "## Recently updated repositories", ""])
        lines.extend(recent_lines)

    lines.extend(["", "## Learning log", ""])

    if learning_log:
        for entry in learning_log:
            lines.append(f"* {entry}")
    else:
        lines.append("* Add learning notes in content/extra/github_repositories_overrides.json")

    lines.extend(["", "## Maintenance notes", ""])
    lines.append("* This page includes only public repositories from the current GitHub profile.")
    lines.append("* Repository metadata (language, description, archive status) is synced from the public GitHub API.")
    lines.append("* Curation and ordering are controlled in content/extra/github_repositories_overrides.json.")

    lines.extend([
        "",
        "## Related content",
        "",
        "<div class=\"ds-related-module\">",
        "<p>Follow related paths from repositories into research and events:</p>",
        "<ul class=\"ds-reference-list\">",
        "<li>[Research Projects](/pages/research/projects/)</li>",
        "<li>[Publications and talks](/pages/research/publications/)</li>",
        "<li>[Courses and teaching materials](/pages/courses/)</li>",
        "<li>[Undergraduate Seminar sessions](/pages/seminar/)</li>",
        "</ul>",
        "</div>",
    ])

    if missing_names:
        lines.extend(["", "### Curation warnings", ""])
        lines.append(
            "* The following curated repositories were not found in the public profile and were omitted: "
            + ", ".join(sorted(set(missing_names), key=str.lower))
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync repositories page from public GitHub API")
    parser.add_argument("--username", default=os.environ.get("GITHUB_USERNAME", "alxcn"))
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--overrides", default=DEFAULT_OVERRIDES)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    overrides_path = Path(args.overrides)
    if not overrides_path.exists():
        raise RuntimeError(f"Overrides file not found: {overrides_path}")

    overrides = _read_json_file(overrides_path)
    username = str(overrides.get("github_username") or args.username)
    date_value = str(overrides.get("date") or "2026-07-15")
    description_text = str(
        overrides.get("description")
        or "Curated public GitHub repositories, exploratory forks, and practical learning notes from ongoing technical work."
    )

    output_path = Path(args.output)

    try:
        repositories = _fetch_all_repositories(username=username, token=args.token)
    except Exception as error:  # pragma: no cover - defensive fallback path
        if output_path.exists():
            print(
                "Warning: GitHub sync failed; keeping existing repositories page "
                f"at {output_path}. Reason: {error}"
            )
            return 0
        raise RuntimeError(
            "GitHub sync failed and no existing repositories page is available for fallback"
        ) from error

    repo_by_name = _repo_lookup(repositories)

    curated_featured = _parse_curated_items(overrides.get("featured_repositories"))
    curated_forks = _parse_curated_items(overrides.get("featured_forks"))

    featured_lines, missing_featured = _build_curated_section(
        curated=curated_featured,
        repo_by_name=repo_by_name,
        expected_fork_state=False,
    )
    fork_lines, missing_forks = _build_curated_section(
        curated=curated_forks,
        repo_by_name=repo_by_name,
        expected_fork_state=True,
    )

    curated_names = {item.name.lower() for item in curated_featured + curated_forks}
    excluded_names = {
        str(name).strip().lower()
        for name in overrides.get("exclude_repositories", [])
        if isinstance(name, str) and str(name).strip()
    }
    recent_limit = int(overrides.get("recent_repositories_limit", 5) or 0)
    include_forks_in_recent = bool(overrides.get("recent_repositories_include_forks", False))

    recent_lines = _build_recent_section(
        repositories=repositories,
        curated_names=curated_names,
        excluded_names=excluded_names,
        max_items=recent_limit,
        include_forks=include_forks_in_recent,
    )

    learning_log = [
        str(entry).strip()
        for entry in overrides.get("learning_log", [])
        if isinstance(entry, str) and str(entry).strip()
    ]

    page_text = _format_page(
        username=username,
        date_value=date_value,
        description_text=description_text,
        featured_lines=featured_lines,
        fork_lines=fork_lines,
        recent_lines=recent_lines,
        learning_log=learning_log,
        missing_names=missing_featured + missing_forks,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(page_text, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
