#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import shutil
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


ROOT = Path.home() / "Projects" / "vantalabs-site"
GUARDIAN = ROOT / "guardian"
SITEMAP = ROOT / "sitemap.xml"

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = ROOT / f"sitemap.before-guardian-repair-{timestamp}.xml"

if not SITEMAP.is_file():
    raise SystemExit(f"Sitemap not found: {SITEMAP}")

if not GUARDIAN.is_dir():
    raise SystemExit(f"Guardian folder not found: {GUARDIAN}")

shutil.copy2(SITEMAP, backup)

existing_entries = []
seen_urls = set()

try:
    old_root = ET.parse(SITEMAP).getroot()

    for url_node in old_root.findall(f"{{{NS}}}url"):
        loc_node = url_node.find(f"{{{NS}}}loc")

        if loc_node is None or not loc_node.text:
            continue

        loc = loc_node.text.strip()

        if not loc or loc in seen_urls:
            continue

        # Guardian entries will be rebuilt from the actual local pages.
        if "/guardian" in loc:
            continue

        seen_urls.add(loc)

        entry = {"loc": loc}

        for tag in ("lastmod", "changefreq", "priority"):
            node = url_node.find(f"{{{NS}}}{tag}")

            if node is not None and node.text:
                entry[tag] = node.text.strip()

        existing_entries.append(entry)

except ET.ParseError as error:
    raise SystemExit(f"Current sitemap is not valid XML: {error}")


guardian_entries = []

for html_file in sorted(GUARDIAN.rglob("*.html")):
    raw = html_file.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")

    canonical = soup.find(
        "link",
        attrs={"rel": lambda value: value and "canonical" in value},
    )

    if not canonical:
        print(f"Skipping page without canonical: {html_file}")
        continue

    loc = canonical.get("href", "").strip()

    if not loc or loc in seen_urls:
        continue

    seen_urls.add(loc)

    guardian_entries.append({
        "loc": loc,
        "lastmod": datetime.fromtimestamp(
            html_file.stat().st_mtime
        ).strftime("%Y-%m-%d"),
    })


new_root = ET.Element(f"{{{NS}}}urlset")

for entry in existing_entries + guardian_entries:
    url_node = ET.SubElement(new_root, f"{{{NS}}}url")

    loc_node = ET.SubElement(url_node, f"{{{NS}}}loc")
    loc_node.text = entry["loc"]

    if entry.get("lastmod"):
        lastmod_node = ET.SubElement(url_node, f"{{{NS}}}lastmod")
        lastmod_node.text = entry["lastmod"]

    if entry.get("changefreq"):
        changefreq_node = ET.SubElement(
            url_node,
            f"{{{NS}}}changefreq",
        )
        changefreq_node.text = entry["changefreq"]

    if entry.get("priority"):
        priority_node = ET.SubElement(
            url_node,
            f"{{{NS}}}priority",
        )
        priority_node.text = entry["priority"]


tree = ET.ElementTree(new_root)
ET.indent(tree, space="  ")

tree.write(
    SITEMAP,
    encoding="utf-8",
    xml_declaration=True,
)

print()
print("Sitemap repair complete.")
print(f"Backup: {backup}")
print(f"Existing non-Guardian URLs retained: {len(existing_entries)}")
print(f"Guardian URLs added: {len(guardian_entries)}")
print(f"Total sitemap URLs: {len(existing_entries) + len(guardian_entries)}")
print("No commit, push or deployment was performed.")
print()
