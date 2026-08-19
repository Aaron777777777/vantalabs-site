#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path.cwd()
SITE = ROOT / "vanta-shift"
PLAN = json.loads(
    Path("vanta_shift_page_plan.json").read_text(encoding="utf-8")
)

pages = sorted(
    path for path in SITE.rglob("index.html")
    if path != SITE / "rota-app-for-shift-workers" / "index.html"
)
planned_paths = {
    page["path"]
    for page in PLAN["pages"]
}

FORBIDDEN = [
    "book on",
    "book off",
    "booking on",
    "booking off",
    "clock in",
    "clock-in",
    "attendance tracker",
    "attendance management",
    "manager dashboard",
    "workforce oversight",
]

def extract(pattern: str, source: str) -> str:
    match = re.search(pattern, source, re.I | re.S)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def page_path(path: Path) -> str:
    relative = path.parent.relative_to(SITE)

    if str(relative) == ".":
        return "/vanta-shift/"

    return f"/vanta-shift/{relative.as_posix()}/"


records = []
issues = []
links = {}

for path in pages:
    source = path.read_text(encoding="utf-8")
    visible = re.sub(
        r"<script\b.*?</script>|<style\b.*?</style>",
        " ",
        source,
        flags=re.I | re.S,
    )
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", visible).strip()

    title = extract(r"<title>(.*?)</title>", source)
    meta = extract(
        r'<meta\s+name="description"\s+content="(.*?)"\s*/?>',
        source,
    )
    h1 = extract(r"<h1[^>]*>(.*?)</h1>", source)
    canonical = extract(
        r'<link\s+rel="canonical"\s+href="(.*?)"\s*/?>',
        source,
    )

    path_value = page_path(path)

    records.append(
        {
            "path": path_value,
            "title": title,
            "meta": meta,
            "h1": h1,
            "canonical": canonical,
            "body": visible.casefold(),
        }
    )

    for field, value in [
        ("title", title),
        ("meta", meta),
        ("h1", h1),
        ("canonical", canonical),
    ]:
        if not value:
            issues.append(f"{path_value}: missing {field}")

    for required in [
        'property="og:title"',
        'property="og:description"',
        'property="og:url"',
        'property="og:site_name"',
    ]:
        if required not in source:
            issues.append(f"{path_value}: missing {required}")

    blocks = re.findall(
        r'<script\b[^>]*type="application/ld\+json"[^>]*>'
        r'(.*?)</script>',
        source,
        re.I | re.S,
    )

    if not blocks:
        issues.append(f"{path_value}: missing JSON-LD")

    for block in blocks:
        try:
            json.loads(block.strip())
        except Exception as exc:
            issues.append(
                f"{path_value}: invalid JSON-LD: {exc}"
            )

    if 'href="/vanta-shift/"' not in source:
        issues.append(
            f"{path_value}: missing Vanta Shift home link"
        )

    if "data-store=\"android\"" not in source:
        issues.append(
            f"{path_value}: missing Android store button"
        )

    if "data-store=\"ios\"" not in source:
        issues.append(
            f"{path_value}: missing iOS store button"
        )

    lower = visible.casefold()

    for forbidden in FORBIDDEN:
        if forbidden in lower:
            issues.append(
                f"{path_value}: forbidden Workforce wording: {forbidden}"
            )

    page_links = re.findall(
        r'href="(/vanta-shift/[^"#?]*)"',
        source,
        re.I,
    )

    links[path_value] = {
        link
        for link in page_links
        if not link.startswith("/vanta-shift/assets/")
        and not re.search(
            r"\.(?:css|js|png|jpg|jpeg|webp|svg|ico)$",
            link,
            re.I,
        )
    }


def duplicate_groups(field: str) -> list[list[str]]:
    grouped = {}

    for record in records:
        grouped.setdefault(record[field], []).append(record["path"])

    return [
        paths
        for value, paths in grouped.items()
        if value and len(paths) > 1
    ]


existing_paths = {
    record["path"]
    for record in records
}

broken = []

for source_path, targets in links.items():
    for target in targets:
        normalised = target if target.endswith("/") else target + "/"

        if normalised not in existing_paths:
            broken.append((source_path, target))


similarities = []

for index, left in enumerate(records):
    for right in records[index + 1:]:
        ratio = SequenceMatcher(
            None,
            left["body"],
            right["body"],
        ).ratio()

        if ratio >= 0.82:
            similarities.append(
                {
                    "page_a": left["path"],
                    "page_b": right["path"],
                    "similarity": ratio,
                }
            )

sitemap_source = (SITE / "sitemap.xml").read_text(encoding="utf-8")
sitemap_urls = re.findall(r"<loc>(.*?)</loc>", sitemap_source)

sitemap_paths = {
    urlparse(url).path
    for url in sitemap_urls
}

summary = {
    "html_page_count": len(records),
    "planned_page_count": len(planned_paths),
    "duplicate_title_groups": len(duplicate_groups("title")),
    "duplicate_meta_description_groups": len(duplicate_groups("meta")),
    "duplicate_h1_groups": len(duplicate_groups("h1")),
    "duplicate_canonical_groups": len(duplicate_groups("canonical")),
    "exact_duplicate_body_groups": len(duplicate_groups("body")),
    "high_similarity_pairs": len(similarities),
    "broken_internal_links": len(broken),
    "missing_site_sitemap_entries": len(
        existing_paths - sitemap_paths
    ),
    "sitemap_urls_without_pages": len(
        sitemap_paths - existing_paths
    ),
    "duplicate_sitemap_urls": sum(
        count - 1
        for count in Counter(sitemap_urls).values()
        if count > 1
    ),
    "forbidden_or_structural_issues": len(issues),
}

report = {
    "summary": summary,
    "issues": issues,
    "broken_internal_links": broken,
    "high_similarity_pairs": sorted(
        similarities,
        key=lambda item: item["similarity"],
        reverse=True,
    ),
}

output = (
    Path.home()
    / "Desktop"
    / "vanta-shift-seo-audit-report"
)

output.mkdir(parents=True, exist_ok=True)

(output / "vanta-shift-seo-audit.json").write_text(
    json.dumps(
        report,
        indent=2,
        ensure_ascii=False,
    ) + "\n",
    encoding="utf-8",
)

print("Audit complete.")
print("Reports:", output)
print()

for key, value in summary.items():
    print(f"{key}: {value}")

print("\nIssues:")

if issues:
    for issue in issues[:30]:
        print("-", issue)
else:
    print("- none")

print("\nHighest similarity pairs:")

if similarities:
    for pair in report["high_similarity_pairs"][:15]:
        print(
            f"- {pair['similarity']:.1%}: "
            f"{pair['page_a']} <-> {pair['page_b']}"
        )
else:
    print("- none")
