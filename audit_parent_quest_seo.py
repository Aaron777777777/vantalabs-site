from __future__ import annotations

import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "parent-quest"
PLAN_PATH = ROOT / "parent_quest_page_plan.json"
SITEMAP_PATH = SITE / "sitemap.xml"

BASE_URL = "https://vantalabs.co.uk"
ANDROID_URL = (
    "https://play.google.com/store/apps/details"
    "?id=com.vantalabs.parentquest"
)
IOS_URL = (
    "https://apps.apple.com/us/app/parent-quest/"
    "id6782297539"
)

SIMILARITY_THRESHOLD = 0.88

FORBIDDEN_PHRASES = (
    "location tracking",
    "location sharing",
    "safe zone",
    "safe zones",
    "geofence",
    "gps tracker",
    "child tracker",
    "family locator",
    "live location",
    "sos alert",
    "emergency alert",
    "child login",
    "child account",
    "child messaging",
    "family messaging",
    "bank account",
    "banking",
    "cash reward",
    "real money reward",
    "workforce",
    "clocking in",
    "clocking out",
    "booking on",
    "booking off",
    "attendance tracking",
)

IGNORED_LINK_PREFIXES = (
    "mailto:",
    "tel:",
    "javascript:",
    "#",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()

        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.meta_description: str | None = None
        self.canonical: str | None = None
        self.links: list[str] = []
        self.schemas: list[object] = []

        self._in_title = False
        self._in_h1 = False
        self._in_script = False
        self._schema_parts: list[str] = []

        self.visible_parts: list[str] = []
        self._hidden_depth = 0

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        data = dict(attrs)

        if tag == "title":
            self._in_title = True

        if tag == "h1":
            self._in_h1 = True

        if tag in {"script", "style", "noscript", "svg"}:
            self._hidden_depth += 1

        if (
            tag == "meta"
            and data.get("name", "").lower() == "description"
        ):
            self.meta_description = data.get("content")

        if tag == "link":
            rel = (data.get("rel") or "").lower()
            if "canonical" in rel:
                self.canonical = data.get("href")

        if tag == "a" and data.get("href"):
            self.links.append(data["href"] or "")

        if (
            tag == "script"
            and data.get("type") == "application/ld+json"
        ):
            self._in_script = True
            self._schema_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

        if tag == "h1":
            self._in_h1 = False

        if tag == "script" and self._in_script:
            raw = "".join(self._schema_parts).strip()

            if raw:
                try:
                    self.schemas.append(json.loads(raw))
                except json.JSONDecodeError as error:
                    self.schemas.append({
                        "__invalid_json_ld__": str(error),
                    })

            self._in_script = False
            self._schema_parts = []

        if tag in {"script", "style", "noscript", "svg"}:
            self._hidden_depth = max(0, self._hidden_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)

        if self._in_h1:
            self.h1_parts.append(data)

        if self._in_script:
            self._schema_parts.append(data)

        if self._hidden_depth == 0:
            clean = " ".join(data.split())
            if clean:
                self.visible_parts.append(clean)


def clean_text(value: str | None) -> str:
    if not value:
        return ""

    return " ".join(html.unescape(value).split())


def normalize_body(value: str) -> str:
    value = html.unescape(value).lower()
    value = re.sub(r"©\s*2026.*", " ", value)
    value = re.sub(r"\bparent quest\b", " ", value)
    value = re.sub(r"\bvanta labs(?: nw ltd)?\b", " ", value)
    value = re.sub(r"\bgoogle play\b|\bapp store\b", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def local_file_for_path(path: str) -> Path:
    parsed = urlparse(path)
    clean_path = parsed.path

    if clean_path == "/parent-quest/":
        return SITE / "index.html"

    if clean_path.startswith("/parent-quest/"):
        relative = clean_path.removeprefix("/parent-quest/").strip("/")
        return SITE / relative / "index.html"

    if clean_path == "/":
        return ROOT / "index.html"

    relative = clean_path.lstrip("/")

    if not relative:
        return ROOT / "index.html"

    target = ROOT / relative

    if target.is_dir():
        return target / "index.html"

    return target


def flatten_schema_types(value: object) -> list[str]:
    types: list[str] = []

    if isinstance(value, dict):
        schema_type = value.get("@type")

        if isinstance(schema_type, str):
            types.append(schema_type)
        elif isinstance(schema_type, list):
            types.extend(
                item for item in schema_type if isinstance(item, str)
            )

        for child in value.values():
            types.extend(flatten_schema_types(child))

    elif isinstance(value, list):
        for child in value:
            types.extend(flatten_schema_types(child))

    return types


def duplicates(values: dict[str, str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)

    for file, value in values.items():
        grouped[value].append(file)

    return {
        value: files
        for value, files in grouped.items()
        if value and len(files) > 1
    }


def print_groups(
    label: str,
    groups: dict[str, list[str]],
    limit: int = 10,
) -> None:
    print(f"{label}: {len(groups)}")

    for value, files in list(groups.items())[:limit]:
        print(f"  {value!r}")
        for file in files:
            print(f"    - {file}")


if not SITE.is_dir():
    raise SystemExit("Missing parent-quest directory")

if not PLAN_PATH.is_file():
    raise SystemExit("Missing parent_quest_page_plan.json")

if not SITEMAP_PATH.is_file():
    raise SystemExit("Missing parent-quest/sitemap.xml")


plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
planned_pages = plan["pages"]
planned_paths = {page["path"] for page in planned_pages}
page_by_path = {page["path"]: page for page in planned_pages}

html_files = sorted(SITE.rglob("index.html"))

records: dict[str, dict] = {}

issues: list[str] = []
broken_links: list[tuple[str, str, str]] = []
forbidden_hits: list[tuple[str, str]] = []
invalid_json_ld: list[tuple[str, str]] = []
missing_schema: list[tuple[str, str]] = []
missing_home_links: list[str] = []
missing_cluster_links: list[tuple[str, str]] = []
wrong_store_links: list[str] = []
wrong_branding: list[str] = []

for file in html_files:
    relative_file = str(file.relative_to(ROOT))
    text = file.read_text(encoding="utf-8")

    parser = PageParser()
    parser.feed(text)

    title = clean_text("".join(parser.title_parts))
    h1 = clean_text("".join(parser.h1_parts))
    description = clean_text(parser.meta_description)
    canonical = clean_text(parser.canonical)
    visible = clean_text(" ".join(parser.visible_parts))
    normalized = normalize_body(visible)

    records[relative_file] = {
        "file": file,
        "text": text,
        "title": title,
        "h1": h1,
        "description": description,
        "canonical": canonical,
        "visible": visible,
        "normalized": normalized,
        "links": parser.links,
        "schemas": parser.schemas,
    }

    if not title:
        issues.append(f"Missing title: {relative_file}")

    if not h1:
        issues.append(f"Missing H1: {relative_file}")

    if not description:
        issues.append(f"Missing meta description: {relative_file}")

    if not canonical:
        issues.append(f"Missing canonical: {relative_file}")

    if canonical and not canonical.startswith(
        f"{BASE_URL}/parent-quest/"
    ):
        issues.append(
            f"Unexpected canonical: {relative_file}: {canonical}"
        )

    schema_types: list[str] = []

    for schema in parser.schemas:
        if (
            isinstance(schema, dict)
            and "__invalid_json_ld__" in schema
        ):
            invalid_json_ld.append(
                (
                    relative_file,
                    str(schema["__invalid_json_ld__"]),
                )
            )
            continue

        schema_types.extend(flatten_schema_types(schema))

    required_types = {
        "SoftwareApplication",
    }

    is_home = file == SITE / "index.html"

    if not is_home:
        required_types.update({
            "BreadcrumbList",
            "FAQPage",
        })

    canonical_path = urlparse(canonical).path if canonical else ""
    planned_page = page_by_path.get(canonical_path)

    if planned_page and planned_page["type"] == "guide":
        required_types.add("Article")

    for required_type in sorted(required_types):
        if required_type not in schema_types:
            missing_schema.append(
                (relative_file, required_type)
            )

    if '"name":"Vanta Labs"' not in text and (
        '"name": "Vanta Labs"' not in text
    ):
        wrong_branding.append(relative_file)

    if "/parent-quest/assets/app-links.js" not in text:
        wrong_store_links.append(relative_file)

    lower_text = visible.lower()

    for phrase in FORBIDDEN_PHRASES:
        if phrase in lower_text:
            forbidden_hits.append((relative_file, phrase))

    if not is_home:
        if "/parent-quest/" not in parser.links:
            missing_home_links.append(relative_file)

        if planned_page:
            leader = planned_page["cluster_leader"]

            if (
                leader != planned_page["path"]
                and leader not in parser.links
            ):
                missing_cluster_links.append(
                    (relative_file, leader)
                )

    for href in parser.links:
        href = href.strip()

        if not href:
            continue

        if href.startswith(IGNORED_LINK_PREFIXES):
            continue

        parsed = urlparse(href)

        if parsed.scheme in {"http", "https"}:
            if parsed.netloc not in {
                "www.vantalabs.co.uk",
                "vantalabs.co.uk",
                "play.google.com",
                "apps.apple.com",
            }:
                continue

            if parsed.netloc in {
                "play.google.com",
                "apps.apple.com",
            }:
                continue

        target = local_file_for_path(href)

        if not target.exists():
            broken_links.append(
                (
                    relative_file,
                    href,
                    str(target.relative_to(ROOT)),
                )
            )


titles = {
    file: record["title"]
    for file, record in records.items()
}

descriptions = {
    file: record["description"]
    for file, record in records.items()
}

h1s = {
    file: record["h1"]
    for file, record in records.items()
}

canonicals = {
    file: record["canonical"]
    for file, record in records.items()
}

bodies = {
    file: record["normalized"]
    for file, record in records.items()
}

duplicate_titles = duplicates(titles)
duplicate_descriptions = duplicates(descriptions)
duplicate_h1s = duplicates(h1s)
duplicate_canonicals = duplicates(canonicals)
exact_duplicate_bodies = duplicates(bodies)


similarity_pairs: list[tuple[float, str, str]] = []

record_items = list(records.items())

for left_index, (left_file, left_record) in enumerate(record_items):
    left_body = left_record["normalized"]

    if len(left_body) < 120:
        continue

    for right_file, right_record in record_items[left_index + 1:]:
        right_body = right_record["normalized"]

        if len(right_body) < 120:
            continue

        length_ratio = min(
            len(left_body),
            len(right_body),
        ) / max(
            len(left_body),
            len(right_body),
        )

        if length_ratio < 0.68:
            continue

        matcher = SequenceMatcher(
            None,
            left_body,
            right_body,
            autojunk=True,
        )
        if matcher.quick_ratio() < SIMILARITY_THRESHOLD:
            continue
        score = matcher.ratio()

        if score >= SIMILARITY_THRESHOLD:
            similarity_pairs.append(
                (score, left_file, right_file)
            )

similarity_pairs.sort(reverse=True)


namespace = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
}

tree = ET.parse(SITEMAP_PATH)
root = tree.getroot()

sitemap_urls = [
    clean_text(element.text)
    for element in root.findall("sm:url/sm:loc", namespace)
]

sitemap_paths = {
    urlparse(url).path
    for url in sitemap_urls
}

duplicate_sitemap_urls = [
    url
    for url, count in Counter(sitemap_urls).items()
    if count > 1
]

missing_sitemap_entries = sorted(
    planned_paths - sitemap_paths
)

sitemap_urls_without_pages = sorted(
    sitemap_paths - planned_paths
)


script = (
    SITE / "assets/app-links.js"
).read_text(encoding="utf-8")

if ANDROID_URL not in script:
    issues.append("Android store URL missing from app-links.js")

if IOS_URL not in script:
    issues.append("iOS store URL missing from app-links.js")


print()
print("===== PARENT QUEST SEO AUDIT =====")
print(f"HTML pages: {len(html_files)}")
print(f"Planned pages: {len(planned_pages)}")
print(f"Sitemap URLs: {len(sitemap_urls)}")
print()

print_groups("Duplicate title groups", duplicate_titles)
print_groups(
    "Duplicate meta-description groups",
    duplicate_descriptions,
)
print_groups("Duplicate H1 groups", duplicate_h1s)
print_groups(
    "Duplicate canonical groups",
    duplicate_canonicals,
)
print_groups(
    "Exact duplicate body groups",
    exact_duplicate_bodies,
)

print(f"High-similarity pairs: {len(similarity_pairs)}")

for score, left, right in similarity_pairs[:20]:
    print(f"  {score:.3%}: {left} ↔ {right}")

print(f"Broken internal links: {len(broken_links)}")

for source, href, target in broken_links[:30]:
    print(f"  {source}: {href} -> {target}")

print(f"Missing sitemap entries: {len(missing_sitemap_entries)}")

for item in missing_sitemap_entries[:30]:
    print(f"  {item}")

print(
    "Sitemap URLs without planned pages: "
    f"{len(sitemap_urls_without_pages)}"
)

for item in sitemap_urls_without_pages[:30]:
    print(f"  {item}")

print(
    "Duplicate sitemap URLs: "
    f"{len(duplicate_sitemap_urls)}"
)

for item in duplicate_sitemap_urls[:30]:
    print(f"  {item}")

print(f"Invalid JSON-LD pages: {len(invalid_json_ld)}")

for file, error in invalid_json_ld[:30]:
    print(f"  {file}: {error}")

print(f"Missing required schema: {len(missing_schema)}")

for file, schema_type in missing_schema[:30]:
    print(f"  {file}: {schema_type}")

print(
    "Pages missing Parent Quest home links: "
    f"{len(missing_home_links)}"
)

for item in missing_home_links[:30]:
    print(f"  {item}")

print(
    "Pages missing cluster-leader links: "
    f"{len(missing_cluster_links)}"
)

for file, leader in missing_cluster_links[:30]:
    print(f"  {file}: {leader}")

print(f"Forbidden wording hits: {len(forbidden_hits)}")

for file, phrase in forbidden_hits[:30]:
    print(f"  {file}: {phrase!r}")

print(
    "Pages missing store-link script: "
    f"{len(wrong_store_links)}"
)

for item in wrong_store_links[:30]:
    print(f"  {item}")

print(
    "Pages missing Vanta Labs schema branding: "
    f"{len(wrong_branding)}"
)

for item in wrong_branding[:30]:
    print(f"  {item}")

print(f"Other structural issues: {len(issues)}")

for item in issues[:50]:
    print(f"  {item}")


failure_count = sum([
    len(duplicate_titles),
    len(duplicate_descriptions),
    len(duplicate_h1s),
    len(duplicate_canonicals),
    len(exact_duplicate_bodies),
    len(similarity_pairs),
    len(broken_links),
    len(missing_sitemap_entries),
    len(sitemap_urls_without_pages),
    len(duplicate_sitemap_urls),
    len(invalid_json_ld),
    len(missing_schema),
    len(missing_home_links),
    len(missing_cluster_links),
    len(forbidden_hits),
    len(wrong_store_links),
    len(wrong_branding),
    len(issues),
])

if len(html_files) != len(planned_pages):
    print(
        f"FAIL: expected HTML count to match plan, "
        f"found {len(html_files)}"
    )
    failure_count += 1

if len(planned_paths) != len(planned_pages):
    print(
        f"FAIL: expected unique planned paths, "
        f"found {len(planned_pages)}"
    )
    failure_count += 1

if len(sitemap_urls) != len(planned_pages):
    print(
        f"FAIL: expected sitemap count to match plan, "
        f"found {len(sitemap_urls)}"
    )
    failure_count += 1

report = {
    "html_page_count": len(html_files),
    "planned_page_count": len(planned_pages),
    "sitemap_url_count": len(sitemap_urls),
    "duplicate_title_groups": len(duplicate_titles),
    "duplicate_meta_description_groups": len(
        duplicate_descriptions
    ),
    "duplicate_h1_groups": len(duplicate_h1s),
    "duplicate_canonical_groups": len(
        duplicate_canonicals
    ),
    "exact_duplicate_body_groups": len(
        exact_duplicate_bodies
    ),
    "high_similarity_pairs": len(similarity_pairs),
    "broken_internal_links": len(broken_links),
    "missing_sitemap_entries": len(
        missing_sitemap_entries
    ),
    "sitemap_urls_without_pages": len(
        sitemap_urls_without_pages
    ),
    "duplicate_sitemap_urls": len(
        duplicate_sitemap_urls
    ),
    "invalid_json_ld_pages": len(invalid_json_ld),
    "missing_required_schema": len(missing_schema),
    "missing_parent_quest_home_links": len(
        missing_home_links
    ),
    "missing_cluster_leader_links": len(
        missing_cluster_links
    ),
    "forbidden_wording_hits": len(forbidden_hits),
    "missing_store_link_scripts": len(
        wrong_store_links
    ),
    "missing_vanta_labs_schema_branding": len(
        wrong_branding
    ),
    "other_structural_issues": len(issues),
    "highest_similarity_pairs": [
        {
            "score": round(score, 6),
            "left": left,
            "right": right,
        }
        for score, left, right in similarity_pairs[:30]
    ],
}

(ROOT / "parent-quest-seo-audit.json").write_text(
    json.dumps(report, indent=2) + "\n",
    encoding="utf-8",
)

print()
print("Audit report: parent-quest-seo-audit.json")

if failure_count:
    print(f"PARENT QUEST AUDIT FAILED: {failure_count} issue groups")
    sys.exit(1)

print("PARENT QUEST AUDIT PASSED")
