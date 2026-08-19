#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import urlparse
from collections import Counter, defaultdict
from difflib import SequenceMatcher
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


SITE_ROOT = Path.home() / "Projects" / "vantalabs-site"
GUARDIAN_ROOT = SITE_ROOT / "guardian"
SITEMAP = SITE_ROOT / "sitemap.xml"
REPORT_DIR = Path.home() / "Desktop" / "guardian-seo-audit-report"

SIMILARITY_THRESHOLD = 0.82


def clean(value):
    return re.sub(r"\s+", " ", value or "").strip()


def page_url(path):
    relative = path.relative_to(SITE_ROOT)

    if relative.name == "index.html":
        parent = relative.parent.as_posix()
        return "/" if parent == "." else f"/{parent}/"

    return f"/{relative.as_posix()}"


def canonical_path(value):
    if not value:
        return ""

    return urlparse(value).path or "/"


def resolve_internal_link(source_file, href):
    href = href.strip()

    if not href:
        return None

    if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None

    parsed = urlparse(href)

    if parsed.scheme in ("http", "https"):
        if not parsed.path.startswith("/guardian"):
            return None
        link_path = parsed.path
    else:
        link_path = parsed.path

    if not link_path:
        return None

    if link_path.startswith("/"):
        target = SITE_ROOT / link_path.lstrip("/")
    else:
        target = source_file.parent / link_path

    target = target.resolve()

    candidates = [target]

    if target.suffix == "":
        candidates.extend([
            target / "index.html",
            target.with_suffix(".html"),
        ])

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return target


def collect_schema_types(value, output):
    if isinstance(value, dict):
        schema_type = value.get("@type")

        if isinstance(schema_type, str):
            output.add(schema_type)
        elif isinstance(schema_type, list):
            output.update(str(item) for item in schema_type)

        for child in value.values():
            collect_schema_types(child, output)

    elif isinstance(value, list):
        for child in value:
            collect_schema_types(child, output)


def similarity_text(text):
    stopwords = {
        "the", "and", "for", "that", "with", "this", "from", "your",
        "you", "are", "can", "guardian", "app", "family", "child",
        "children", "their", "when", "into", "about", "have", "has",
        "our", "not", "but", "its", "they", "them", "who", "what",
    }

    words = re.findall(r"[a-z0-9]+", text.lower())

    return " ".join(
        word for word in words
        if len(word) > 2 and word not in stopwords
    )


if not GUARDIAN_ROOT.is_dir():
    raise SystemExit(f"Guardian folder not found: {GUARDIAN_ROOT}")

if not SITEMAP.is_file():
    raise SystemExit(f"Sitemap not found: {SITEMAP}")

html_files = sorted(
    path for path in GUARDIAN_ROOT.rglob("*.html")
    if ".git" not in path.parts
    and "node_modules" not in path.parts
    and not any(part.startswith("guardian.before-") for part in path.parts)
)

pages = []

for path in html_files:
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")

    title = clean(soup.title.get_text(" ", strip=True) if soup.title else "")

    description_tag = soup.find(
        "meta",
        attrs={"name": re.compile(r"^description$", re.I)},
    )
    description = clean(
        description_tag.get("content", "") if description_tag else ""
    )

    canonical_tag = soup.find(
        "link",
        attrs={
            "rel": lambda value: value and "canonical" in value
        },
    )
    canonical = clean(
        canonical_tag.get("href", "") if canonical_tag else ""
    )

    h1_values = [
        clean(tag.get_text(" ", strip=True))
        for tag in soup.find_all("h1")
    ]

    h2_values = [
        clean(tag.get_text(" ", strip=True))
        for tag in soup.find_all("h2")
    ]

    schema_types = set()
    jsonld_count = 0
    jsonld_valid = True

    for script in soup.find_all(
        "script",
        attrs={"type": re.compile(r"application/ld\+json", re.I)},
    ):
        jsonld_count += 1

        try:
            parsed = json.loads(script.string or script.get_text())
            collect_schema_types(parsed, schema_types)
        except Exception:
            jsonld_valid = False

    broken_links = []

    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        target = resolve_internal_link(path, href)

        if target is not None and not target.exists():
            broken_links.append(href)

    body_soup = BeautifulSoup(raw, "html.parser")

    for tag in body_soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    body_text = clean(
        (body_soup.find("main") or body_soup.body or body_soup)
        .get_text(" ", strip=True)
    )

    visible_text = clean(body_soup.get_text(" ", strip=True))
    word_count = len(re.findall(r"\b[\w'-]+\b", body_text))

    image_sources = [
        image.get("src", "")
        for image in body_soup.find_all("img")
    ]

    has_guardian_image = any(
        "guardian" in source.lower()
        for source in image_sources
    )

    issues = []

    if not title:
        issues.append("Missing title")

    if not description:
        issues.append("Missing meta description")

    if not canonical:
        issues.append("Missing canonical")

    if len(h1_values) != 1:
        issues.append(f"H1 count is {len(h1_values)}")

    if jsonld_count == 0:
        issues.append("Missing JSON-LD")
    elif not jsonld_valid:
        issues.append("Invalid JSON-LD")

    if "SoftwareApplication" not in schema_types:
        issues.append("Missing SoftwareApplication schema")

    if "FAQPage" not in schema_types:
        issues.append("Missing FAQPage schema")

    if not has_guardian_image:
        issues.append("Guardian image not detected")

    if not re.search(r"\bApp\s*Store\b", visible_text, re.I):
        issues.append("App Store placeholder missing")

    if not re.search(r"\bGoogle\s*Play\b", visible_text, re.I):
        issues.append("Google Play placeholder missing")

    if not re.search(r"coming\s+soon", visible_text, re.I):
        pass  # Guardian store links are live

    if "guardian-seo-page" in raw:
        issues.append("Failed-generator class still present")

    if broken_links:
        issues.append(f"{len(set(broken_links))} broken internal links")

    if word_count < 80:
        issues.append("Very low visible word count")

    if word_count > 700:
        issues.append("Unexpectedly high visible word count")

    current_url = page_url(path)

    if canonical:
        if canonical_path(canonical).rstrip("/") != current_url.rstrip("/"):
            issues.append("Canonical does not match page path")

    pages.append({
        "file": str(path),
        "url": current_url,
        "title": title,
        "description": description,
        "canonical": canonical,
        "h1_count": len(h1_values),
        "h1": h1_values[0] if h1_values else "",
        "h2_count": len(h2_values),
        "word_count": word_count,
        "schema_types": sorted(schema_types),
        "jsonld_count": jsonld_count,
        "jsonld_valid": jsonld_valid,
        "broken_links": sorted(set(broken_links)),
        "body_text": body_text,
        "body_hash": hashlib.sha256(
            body_text.lower().encode("utf-8")
        ).hexdigest(),
        "issues": issues,
    })

title_groups = defaultdict(list)
description_groups = defaultdict(list)
h1_groups = defaultdict(list)
body_groups = defaultdict(list)

for page in pages:
    if page["title"]:
        title_groups[page["title"].lower()].append(page["url"])

    if page["description"]:
        description_groups[page["description"].lower()].append(page["url"])

    if page["h1"]:
        h1_groups[page["h1"].lower()].append(page["url"])

    body_groups[page["body_hash"]].append(page["url"])

duplicate_titles = {
    key: urls
    for key, urls in title_groups.items()
    if len(urls) > 1
}

duplicate_descriptions = {
    key: urls
    for key, urls in description_groups.items()
    if len(urls) > 1
}

duplicate_h1s = {
    key: urls
    for key, urls in h1_groups.items()
    if len(urls) > 1
}

duplicate_bodies = {
    key: urls
    for key, urls in body_groups.items()
    if len(urls) > 1
}

similarity_pairs = []

for index, first in enumerate(pages):
    first_text = similarity_text(first["body_text"])

    if len(first_text) < 100:
        continue

    for second in pages[index + 1:]:
        second_text = similarity_text(second["body_text"])

        if len(second_text) < 100:
            continue

        score = SequenceMatcher(
            None,
            first_text,
            second_text,
        ).ratio()

        if score >= SIMILARITY_THRESHOLD:
            similarity_pairs.append({
                "page_a": first["url"],
                "page_b": second["url"],
                "score": round(score, 4),
            })

similarity_pairs.sort(
    key=lambda item: item["score"],
    reverse=True,
)

sitemap_urls = []
sitemap_error = ""

try:
    sitemap_root = ET.parse(SITEMAP).getroot()

    for element in sitemap_root.iter():
        if element.tag.endswith("loc") and element.text:
            sitemap_urls.append(clean(element.text))
except Exception as error:
    sitemap_error = str(error)

guardian_sitemap_paths = [
    canonical_path(url)
    for url in sitemap_urls
    if canonical_path(url).startswith("/guardian")
]

sitemap_counts = Counter(guardian_sitemap_paths)

duplicate_sitemap_paths = {
    path: count
    for path, count in sitemap_counts.items()
    if count > 1
}

page_paths = {page["url"] for page in pages}
sitemap_paths = set(guardian_sitemap_paths)

pages_missing_from_sitemap = sorted(
    page_paths - sitemap_paths
)

sitemap_urls_without_pages = sorted(
    path for path in sitemap_paths - page_paths
    if path.rstrip("/") != "/guardian"
)

REPORT_DIR.mkdir(parents=True, exist_ok=True)

issue_counts = Counter(
    issue
    for page in pages
    for issue in page["issues"]
)

report = {
    "page_count": len(pages),
    "pages_with_issues": sum(
        bool(page["issues"]) for page in pages
    ),
    "duplicate_title_groups": duplicate_titles,
    "duplicate_description_groups": duplicate_descriptions,
    "duplicate_h1_groups": duplicate_h1s,
    "exact_duplicate_body_groups": duplicate_bodies,
    "similarity_pairs": similarity_pairs,
    "duplicate_sitemap_paths": duplicate_sitemap_paths,
    "pages_missing_from_sitemap": pages_missing_from_sitemap,
    "sitemap_urls_without_pages": sitemap_urls_without_pages,
    "sitemap_error": sitemap_error,
    "issue_counts": dict(issue_counts),
    "pages": pages,
}

(REPORT_DIR / "guardian-seo-audit.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8",
)

with (REPORT_DIR / "guardian-page-audit.csv").open(
    "w",
    newline="",
    encoding="utf-8",
) as file:
    writer = csv.writer(file)

    writer.writerow([
        "url",
        "file",
        "title",
        "description",
        "canonical",
        "h1_count",
        "h1",
        "h2_count",
        "word_count",
        "schema_types",
        "broken_links",
        "issues",
    ])

    for page in pages:
        writer.writerow([
            page["url"],
            page["file"],
            page["title"],
            page["description"],
            page["canonical"],
            page["h1_count"],
            page["h1"],
            page["h2_count"],
            page["word_count"],
            " | ".join(page["schema_types"]),
            " | ".join(page["broken_links"]),
            " | ".join(page["issues"]),
        ])

with (REPORT_DIR / "guardian-copy-similarity.csv").open(
    "w",
    newline="",
    encoding="utf-8",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["page_a", "page_b", "score"],
    )
    writer.writeheader()
    writer.writerows(similarity_pairs)

summary_lines = [
    "# Guardian SEO Audit",
    "",
    "Read-only audit. No website files were modified.",
    "",
    "## Results",
    "",
    f"- Guardian HTML pages scanned: **{len(pages)}**",
    f"- Pages with issues: **{sum(bool(page['issues']) for page in pages)}**",
    f"- Duplicate title groups: **{len(duplicate_titles)}**",
    f"- Duplicate description groups: **{len(duplicate_descriptions)}**",
    f"- Duplicate H1 groups: **{len(duplicate_h1s)}**",
    f"- Exact duplicate body groups: **{len(duplicate_bodies)}**",
    f"- High-similarity page pairs: **{len(similarity_pairs)}**",
    f"- Broken internal-link occurrences: **{sum(len(page['broken_links']) for page in pages)}**",
    f"- Pages missing from sitemap: **{len(pages_missing_from_sitemap)}**",
    f"- Sitemap URLs without matching pages: **{len(sitemap_urls_without_pages)}**",
    f"- Duplicate Guardian sitemap paths: **{len(duplicate_sitemap_paths)}**",
    "",
    "## Issue totals",
    "",
]

if issue_counts:
    for issue, count in issue_counts.most_common():
        summary_lines.append(f"- {issue}: **{count}**")
else:
    summary_lines.append("- No page-level issues found.")

summary_lines.extend([
    "",
    "## Highest copy-similarity pairs",
    "",
])

if similarity_pairs:
    for pair in similarity_pairs[:40]:
        summary_lines.append(
            f"- `{pair['page_a']}` ↔ `{pair['page_b']}` — "
            f"**{pair['score']:.1%}**"
        )
else:
    summary_lines.append("- No pairs exceeded the threshold.")

summary_lines.extend([
    "",
    "## Pages with issues",
    "",
])

problem_pages = [
    page for page in pages
    if page["issues"]
]

if problem_pages:
    for page in problem_pages:
        summary_lines.append(f"### `{page['url']}`")

        for issue in page["issues"]:
            summary_lines.append(f"- {issue}")

        summary_lines.append("")
else:
    summary_lines.append("- None.")

if sitemap_error:
    summary_lines.extend([
        "",
        "## Sitemap parsing error",
        "",
        f"`{sitemap_error}`",
    ])

(REPORT_DIR / "guardian-seo-audit-summary.md").write_text(
    "\n".join(summary_lines) + "\n",
    encoding="utf-8",
)

print()
print("Guardian SEO audit complete.")
print(f"Pages scanned: {len(pages)}")
print(f"Pages with issues: {sum(bool(page['issues']) for page in pages)}")
print(f"High-similarity pairs: {len(similarity_pairs)}")
print(f"Reports: {REPORT_DIR}")
print()
