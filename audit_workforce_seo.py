#!/usr/bin/env python3

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

ROOT = Path.cwd()
WORKFORCE = ROOT / "workforce"
PLAN_FILE = ROOT / "workforce_page_plan.json"
ROOT_SITEMAP = ROOT / "sitemap.xml"
OUTPUT = Path.home() / "Desktop" / "workforce-seo-audit-report"

BASE_URL = "https://vantalabs.co.uk"
HIGH_SIMILARITY_THRESHOLD = 0.82

if not WORKFORCE.is_dir():
    raise SystemExit("Missing workforce directory")

if not PLAN_FILE.is_file():
    raise SystemExit("Missing workforce_page_plan.json")

OUTPUT.mkdir(parents=True, exist_ok=True)

plan = json.loads(PLAN_FILE.read_text(encoding="utf-8"))
planned_pages = {page["path"]: page for page in plan["pages"]}

TAG_RE = re.compile(r"<[^>]+>", re.S)
SCRIPT_STYLE_RE = re.compile(
    r"<(?:script|style)\b[^>]*>.*?</(?:script|style)>",
    re.I | re.S,
)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def first_match(pattern: str, source: str, flags: int = re.I | re.S) -> str:
    match = re.search(pattern, source, flags)
    return html.unescape(match.group(1).strip()) if match else ""


def all_matches(pattern: str, source: str, flags: int = re.I | re.S) -> list[str]:
    return [html.unescape(value.strip()) for value in re.findall(pattern, source, flags)]


def normalise_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def strip_html(source: str) -> str:
    source = COMMENT_RE.sub(" ", source)
    source = SCRIPT_STYLE_RE.sub(" ", source)
    source = TAG_RE.sub(" ", source)
    return normalise_space(html.unescape(source))


def main_body_text(source: str) -> str:
    main = first_match(r"<main\b[^>]*>(.*?)</main>", source)
    return strip_html(main or source)


def canonical_path(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path or "/"
    if not path.endswith("/"):
        path += "/"
    return path


def local_href_to_file(href: str) -> Path | None:
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None

    parsed = urlparse(href)

    if parsed.scheme in {"http", "https"}:
        if parsed.netloc not in {"www.vantalabs.co.uk", "vantalabs.co.uk"}:
            return None
        path = parsed.path
    elif parsed.scheme:
        return None
    else:
        path = parsed.path

    if not path:
        return None

    if path.endswith("/"):
        return ROOT / path.lstrip("/") / "index.html"

    candidate = ROOT / path.lstrip("/")
    if candidate.suffix:
        return candidate

    return candidate / "index.html"


def page_web_path(file_path: Path) -> str:
    relative = file_path.relative_to(WORKFORCE)
    if relative == Path("index.html"):
        return "/workforce/"
    return "/workforce/" + str(relative.parent).replace("\\", "/").strip("/") + "/"


def extract_json_ld(source: str) -> list[dict]:
    blocks = re.findall(
        r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        source,
        re.I | re.S,
    )

    parsed_blocks = []
    for raw in blocks:
        try:
            parsed_blocks.append(
                {
                    "valid": True,
                    "data": json.loads(raw.strip()),
                    "error": "",
                    "raw_prefix": raw.strip()[:120],
                }
            )
        except Exception as exc:
            parsed_blocks.append(
                {
                    "valid": False,
                    "data": None,
                    "error": str(exc),
                    "raw_prefix": raw.strip()[:120],
                }
            )

    return parsed_blocks


def schema_types(value) -> set[str]:
    found = set()

    if isinstance(value, dict):
        schema_type = value.get("@type")
        if isinstance(schema_type, str):
            found.add(schema_type)
        elif isinstance(schema_type, list):
            found.update(item for item in schema_type if isinstance(item, str))

        for child in value.values():
            found.update(schema_types(child))

    elif isinstance(value, list):
        for child in value:
            found.update(schema_types(child))

    return found


html_files = sorted(WORKFORCE.rglob("index.html"))

records = []
all_internal_links = []
body_texts = {}
body_hashes = defaultdict(list)
titles = defaultdict(list)
descriptions = defaultdict(list)
h1s = defaultdict(list)
canonicals = defaultdict(list)

for file_path in html_files:
    source = file_path.read_text(encoding="utf-8")
    path = page_web_path(file_path)
    planned = planned_pages.get(path, {})

    title = first_match(r"<title\b[^>]*>(.*?)</title>", source)
    description = first_match(
        r'<meta\b[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\'][^>]*>',
        source,
    )

    if not description:
        description = first_match(
            r'<meta\b[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\'][^>]*>',
            source,
        )

    canonical = first_match(
        r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\'][^>]*>',
        source,
    )

    if not canonical:
        canonical = first_match(
            r'<link\b[^>]*href=["\'](.*?)["\'][^>]*rel=["\']canonical["\'][^>]*>',
            source,
        )

    h1_values = all_matches(r"<h1\b[^>]*>(.*?)</h1>", source)
    h1_values = [strip_html(value) for value in h1_values]

    og_title = first_match(
        r'<meta\b[^>]*property=["\']og:title["\'][^>]*content=["\'](.*?)["\'][^>]*>',
        source,
    )
    og_description = first_match(
        r'<meta\b[^>]*property=["\']og:description["\'][^>]*content=["\'](.*?)["\'][^>]*>',
        source,
    )
    og_url = first_match(
        r'<meta\b[^>]*property=["\']og:url["\'][^>]*content=["\'](.*?)["\'][^>]*>',
        source,
    )

    json_ld = extract_json_ld(source)
    valid_json_ld = [block for block in json_ld if block["valid"]]
    invalid_json_ld = [block for block in json_ld if not block["valid"]]

    types = set()
    for block in valid_json_ld:
        types.update(schema_types(block["data"]))

    visible_faq = bool(re.search(r"<details\b", source, re.I))
    body = main_body_text(source)
    normalised_body = body.lower()

    body_texts[path] = normalised_body
    body_hashes[hashlib.sha256(normalised_body.encode("utf-8")).hexdigest()].append(path)

    if title:
        titles[title].append(path)
    if description:
        descriptions[description].append(path)
    for h1 in h1_values:
        h1s[h1].append(path)
    if canonical:
        canonicals[canonical].append(path)

    hrefs = all_matches(r'<a\b[^>]*href=["\'](.*?)["\']', source)

    broken_links = []
    internal_link_paths = []

    for href in hrefs:
        local_file = local_href_to_file(href)
        if local_file is None:
            continue

        parsed = urlparse(href)
        local_path = parsed.path

        if local_path.startswith("/workforce/"):
            internal_link_paths.append(local_path)

        all_internal_links.append((path, href, local_file))

        if not local_file.exists():
            broken_links.append(href)

    android_buttons = len(re.findall(r'data-store=["\']android["\']', source, re.I))
    ios_buttons = len(re.findall(r'data-store=["\']ios["\']', source, re.I))
    android_before_ios = True

    android_position = source.find('data-store="android"')
    ios_position = source.find('data-store="ios"')

    if android_position >= 0 and ios_position >= 0:
        android_before_ios = android_position < ios_position

    links_home = any(
        urlparse(href).path.rstrip("/") == "/workforce"
        for href in hrefs
    )

    leader = planned.get("cluster_leader", "")
    links_cluster_leader = (
        path == leader
        or any(urlparse(href).path.rstrip("/") == leader.rstrip("/") for href in hrefs)
    )

    guardian_terms = sorted(
        set(
            re.findall(
                r"\b(?:Guardian|child|children|parent|parents|school|family locator|safe zone)\b",
                strip_html(source),
                re.I,
            )
        )
    )

    issues = []

    if not title:
        issues.append("missing_title")
    if not description:
        issues.append("missing_meta_description")
    if not canonical:
        issues.append("missing_canonical")
    if len(h1_values) != 1:
        issues.append(f"h1_count_{len(h1_values)}")
    if not og_title:
        issues.append("missing_og_title")
    if not og_description:
        issues.append("missing_og_description")
    if not og_url:
        issues.append("missing_og_url")
    if not json_ld:
        issues.append("missing_json_ld")
    if invalid_json_ld:
        issues.append("invalid_json_ld")
    if "SoftwareApplication" not in types:
        issues.append("missing_software_application_schema")
    if visible_faq and "FAQPage" not in types:
        issues.append("visible_faq_without_faq_schema")
    if path != "/workforce/" and "BreadcrumbList" not in types:
        issues.append("missing_breadcrumb_schema")
    if broken_links:
        issues.append("broken_internal_links")
    if not links_home:
        issues.append("missing_workforce_home_link")
    if path != "/workforce/" and not links_cluster_leader:
        issues.append("missing_cluster_leader_link")
    if android_buttons == 0:
        issues.append("missing_google_play_button")
    if ios_buttons == 0:
        issues.append("missing_app_store_button")
    if android_buttons != ios_buttons:
        issues.append("store_button_count_mismatch")
    if not android_before_ios:
        issues.append("google_play_not_first")
    if guardian_terms:
        issues.append("guardian_wording_found")

    records.append(
        {
            "path": path,
            "file": str(file_path.relative_to(ROOT)),
            "type": planned.get("type", ""),
            "cluster": planned.get("cluster", ""),
            "cluster_leader": leader,
            "title": title,
            "meta_description": description,
            "canonical": canonical,
            "h1": " | ".join(h1_values),
            "h1_count": len(h1_values),
            "og_title": og_title,
            "og_description": og_description,
            "og_url": og_url,
            "json_ld_blocks": len(json_ld),
            "invalid_json_ld_blocks": len(invalid_json_ld),
            "schema_types": " | ".join(sorted(types)),
            "visible_faq": visible_faq,
            "broken_internal_links": " | ".join(sorted(set(broken_links))),
            "links_workforce_home": links_home,
            "links_cluster_leader": links_cluster_leader,
            "google_play_buttons": android_buttons,
            "app_store_buttons": ios_buttons,
            "google_play_first": android_before_ios,
            "guardian_terms": " | ".join(guardian_terms),
            "body_word_count": len(normalised_body.split()),
            "issues": " | ".join(issues),
        }
    )


duplicate_title_groups = {
    key: paths for key, paths in titles.items() if len(paths) > 1
}
duplicate_description_groups = {
    key: paths for key, paths in descriptions.items() if len(paths) > 1
}
duplicate_h1_groups = {
    key: paths for key, paths in h1s.items() if len(paths) > 1
}
duplicate_canonical_groups = {
    key: paths for key, paths in canonicals.items() if len(paths) > 1
}
exact_duplicate_body_groups = {
    key: paths for key, paths in body_hashes.items() if len(paths) > 1
}

similarity_rows = []

paths = sorted(body_texts)
for index, left_path in enumerate(paths):
    for right_path in paths[index + 1:]:
        left = body_texts[left_path]
        right = body_texts[right_path]
        score = SequenceMatcher(None, left, right).ratio()

        if score >= HIGH_SIMILARITY_THRESHOLD:
            similarity_rows.append(
                {
                    "page_a": left_path,
                    "page_b": right_path,
                    "similarity": round(score, 4),
                    "same_cluster": (
                        planned_pages.get(left_path, {}).get("cluster")
                        == planned_pages.get(right_path, {}).get("cluster")
                    ),
                }
            )

similarity_rows.sort(key=lambda row: row["similarity"], reverse=True)

workforce_sitemap_urls = []
workforce_sitemap_error = ""

try:
    tree = ET.parse(WORKFORCE / "sitemap.xml")
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    workforce_sitemap_urls = [
        node.text.strip()
        for node in tree.findall(".//sm:loc", namespace)
        if node.text
    ]
except Exception as exc:
    workforce_sitemap_error = str(exc)

root_sitemap_urls = []

try:
    tree = ET.parse(ROOT_SITEMAP)
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root_sitemap_urls = [
        node.text.strip()
        for node in tree.findall(".//sm:loc", namespace)
        if node.text
    ]
except Exception:
    pass

generated_urls = {
    BASE_URL + record["path"]
    for record in records
}

workforce_sitemap_set = set(workforce_sitemap_urls)
root_sitemap_set = set(root_sitemap_urls)

missing_workforce_sitemap_entries = sorted(generated_urls - workforce_sitemap_set)
workforce_sitemap_without_pages = sorted(workforce_sitemap_set - generated_urls)
missing_root_sitemap_entries = sorted(generated_urls - root_sitemap_set)

duplicate_workforce_sitemap_urls = sorted(
    url for url, count in Counter(workforce_sitemap_urls).items() if count > 1
)

broken_link_rows = [
    {
        "source": source,
        "href": href,
        "expected_file": str(expected.relative_to(ROOT))
        if expected.is_relative_to(ROOT)
        else str(expected),
    }
    for source, href, expected in all_internal_links
    if not expected.exists()
]

issue_counter = Counter()

for record in records:
    for issue in filter(None, record["issues"].split(" | ")):
        issue_counter[issue] += 1

summary = {
    "html_page_count": len(records),
    "planned_page_count": len(planned_pages),
    "duplicate_title_groups": len(duplicate_title_groups),
    "duplicate_meta_description_groups": len(duplicate_description_groups),
    "duplicate_h1_groups": len(duplicate_h1_groups),
    "duplicate_canonical_groups": len(duplicate_canonical_groups),
    "exact_duplicate_body_groups": len(exact_duplicate_body_groups),
    "high_similarity_pairs": len(similarity_rows),
    "high_similarity_threshold": HIGH_SIMILARITY_THRESHOLD,
    "broken_internal_links": len(broken_link_rows),
    "missing_workforce_sitemap_entries": len(missing_workforce_sitemap_entries),
    "workforce_sitemap_urls_without_pages": len(workforce_sitemap_without_pages),
    "duplicate_workforce_sitemap_urls": len(duplicate_workforce_sitemap_urls),
    "missing_root_sitemap_entries": len(missing_root_sitemap_entries),
    "invalid_json_ld_pages": sum(
        record["invalid_json_ld_blocks"] > 0 for record in records
    ),
    "pages_missing_workforce_home_link": sum(
        not record["links_workforce_home"] for record in records
    ),
    "pages_missing_cluster_leader_link": sum(
        record["path"] != "/workforce/" and not record["links_cluster_leader"]
        for record in records
    ),
    "pages_with_guardian_wording": sum(
        bool(record["guardian_terms"]) for record in records
    ),
    "issue_counts": dict(sorted(issue_counter.items())),
}

audit_json = {
    "summary": summary,
    "duplicate_titles": duplicate_title_groups,
    "duplicate_meta_descriptions": duplicate_description_groups,
    "duplicate_h1s": duplicate_h1_groups,
    "duplicate_canonicals": duplicate_canonical_groups,
    "exact_duplicate_bodies": exact_duplicate_body_groups,
    "high_similarity_pairs": similarity_rows,
    "broken_internal_links": broken_link_rows,
    "missing_workforce_sitemap_entries": missing_workforce_sitemap_entries,
    "workforce_sitemap_urls_without_pages": workforce_sitemap_without_pages,
    "duplicate_workforce_sitemap_urls": duplicate_workforce_sitemap_urls,
    "missing_root_sitemap_entries": missing_root_sitemap_entries,
    "workforce_sitemap_error": workforce_sitemap_error,
    "pages": records,
}

(OUTPUT / "workforce-seo-audit.json").write_text(
    json.dumps(audit_json, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

with (OUTPUT / "workforce-page-audit.csv").open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(handle, fieldnames=list(records[0].keys()))
    writer.writeheader()
    writer.writerows(records)

with (OUTPUT / "workforce-copy-similarity.csv").open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    fieldnames = ["page_a", "page_b", "similarity", "same_cluster"]
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(similarity_rows)

summary_lines = [
    "# Vanta Workforce SEO Audit",
    "",
    "Local, read-only audit of `/workforce/`.",
    "",
    "## Headline results",
    "",
    f"- HTML pages: {summary['html_page_count']}",
    f"- Planned pages: {summary['planned_page_count']}",
    f"- Duplicate title groups: {summary['duplicate_title_groups']}",
    f"- Duplicate meta-description groups: {summary['duplicate_meta_description_groups']}",
    f"- Duplicate H1 groups: {summary['duplicate_h1_groups']}",
    f"- Exact duplicate body groups: {summary['exact_duplicate_body_groups']}",
    f"- High-similarity pairs at or above {HIGH_SIMILARITY_THRESHOLD:.0%}: {summary['high_similarity_pairs']}",
    f"- Broken internal links: {summary['broken_internal_links']}",
    f"- Invalid JSON-LD pages: {summary['invalid_json_ld_pages']}",
    f"- Missing Workforce sitemap entries: {summary['missing_workforce_sitemap_entries']}",
    f"- Workforce sitemap URLs without pages: {summary['workforce_sitemap_urls_without_pages']}",
    f"- Duplicate Workforce sitemap URLs: {summary['duplicate_workforce_sitemap_urls']}",
    f"- Workforce URLs missing from root sitemap: {summary['missing_root_sitemap_entries']}",
    f"- Pages missing `/workforce/` link: {summary['pages_missing_workforce_home_link']}",
    f"- Pages missing cluster-leader link: {summary['pages_missing_cluster_leader_link']}",
    f"- Pages containing Guardian/child/family wording: {summary['pages_with_guardian_wording']}",
    "",
    "## Issue counts",
    "",
]

if issue_counter:
    summary_lines.extend(
        f"- `{issue}`: {count}"
        for issue, count in sorted(issue_counter.items())
    )
else:
    summary_lines.append("- No page-level issues found.")

summary_lines.extend(
    [
        "",
        "## Root sitemap status",
        "",
        (
            f"The root sitemap currently lacks {len(missing_root_sitemap_entries)} "
            "Workforce URLs. This is expected while the microsite remains local-only."
        ),
        "",
        "## Highest-similarity pairs",
        "",
    ]
)

if similarity_rows:
    for row in similarity_rows[:20]:
        summary_lines.append(
            f"- {row['similarity']:.1%}: `{row['page_a']}` ↔ `{row['page_b']}`"
        )
else:
    summary_lines.append("- None at the configured threshold.")

summary_lines.extend(
    [
        "",
        "## Important structured-data finding",
        "",
        (
            "JSON-LD must contain literal JSON. HTML entities such as `&quot;` "
            "inside an `application/ld+json` script block are invalid."
        ),
        "",
    ]
)

(OUTPUT / "workforce-seo-audit-summary.md").write_text(
    "\n".join(summary_lines),
    encoding="utf-8",
)

print("Audit complete.")
print(f"Reports: {OUTPUT}")
print()
for key, value in summary.items():
    if key != "issue_counts":
        print(f"{key}: {value}")

print("\nIssue counts:")
if issue_counter:
    for issue, count in sorted(issue_counter.items()):
        print(f"- {issue}: {count}")
else:
    print("- none")

print("\nHighest similarity pairs:")
if similarity_rows:
    for row in similarity_rows[:10]:
        print(
            f"- {row['similarity']:.1%}: "
            f"{row['page_a']} <-> {row['page_b']}"
        )
else:
    print("- none")
