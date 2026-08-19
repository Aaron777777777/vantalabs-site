from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CANONICAL = ROOT / "parent-quest-canonical-source"
LIVE_SITE = ROOT / "parent-quest"


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def relative_file_hashes(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): file_hash(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def clean(value: str) -> str:
    return " ".join(html.unescape(value).split())


def extract_meta(
    source: str,
    key_type: str,
    key_name: str,
) -> str:
    patterns = [
        re.compile(
            rf'<meta\b[^>]*{key_type}=["\']{re.escape(key_name)}["\']'
            rf'[^>]*content=["\'](.*?)["\']',
            re.I | re.S,
        ),
        re.compile(
            rf'<meta\b[^>]*content=["\'](.*?)["\'][^>]*'
            rf'{key_type}=["\']{re.escape(key_name)}["\']',
            re.I | re.S,
        ),
    ]

    for pattern in patterns:
        match = pattern.search(source)

        if match:
            return clean(match.group(1))

    return ""


def validate(site: Path) -> None:
    pages = sorted(site.rglob("index.html"))

    if len(pages) < 101:
        raise SystemExit(
            f"{site}: expected at least 101 HTML pages, found {len(pages)}"
        )

    sitemap = site / "sitemap.xml"

    if not sitemap.is_file():
        raise SystemExit(f"{site}: missing sitemap.xml")

    sitemap_source = sitemap.read_text(encoding="utf-8")
    sitemap_urls = re.findall(
        r"<loc>\s*(.*?)\s*</loc>",
        sitemap_source,
        flags=re.I | re.S,
    )

    if len(sitemap_urls) != len(pages):
        raise SystemExit(
            f"{site}: expected sitemap URL count to match HTML pages, found "
            f"{len(sitemap_urls)}"
        )

    css = site / "assets" / "parent-quest.css"

    if not css.is_file():
        raise SystemExit(f"{site}: missing Parent Quest CSS")

    css_source = css.read_text(encoding="utf-8")

    marker = "/* Shared Vanta app hero standard */"

    if css_source.count(marker) != 1:
        raise SystemExit(
            f"{site}: expected exactly one shared hero marker"
        )

    homepage = site / "index.html"
    homepage_source = homepage.read_text(encoding="utf-8")

    body_match = re.search(
        r'<body\b[^>]*class=["\']([^"\']*)["\']',
        homepage_source,
        flags=re.I,
    )

    homepage_classes = (
        set(body_match.group(1).split())
        if body_match
        else set()
    )

    required_home_classes = {
        "parent-quest-home",
        "parent-quest-detail",
    }

    if not required_home_classes.issubset(homepage_classes):
        raise SystemExit(
            f"{site}: homepage must keep classes "
            f"{sorted(required_home_classes)}"
        )

    titles = []
    descriptions = []
    failures = []

    for path in pages:
        source = path.read_text(encoding="utf-8")

        title_match = re.search(
            r"<title\b[^>]*>(.*?)</title>",
            source,
            flags=re.I | re.S,
        )

        title = clean(title_match.group(1)) if title_match else ""
        description = extract_meta(
            source,
            "name",
            "description",
        )
        og_description = extract_meta(
            source,
            "property",
            "og:description",
        )
        twitter_description = extract_meta(
            source,
            "name",
            "twitter:description",
        )

        page_failures = []

        if not 25 <= len(title) <= 65:
            page_failures.append(
                f"title length {len(title)}"
            )

        if not 100 <= len(description) <= 155:
            page_failures.append(
                f"description length {len(description)}"
            )

        if description != og_description:
            page_failures.append(
                "og:description differs"
            )

        if description != twitter_description:
            page_failures.append(
                "twitter:description differs"
            )

        if len(re.findall(r"<h1\b", source, flags=re.I)) != 1:
            page_failures.append("invalid H1 count")

        if page_failures:
            failures.append(
                f"{path}: {', '.join(page_failures)}"
            )

        titles.append(title)
        descriptions.append(description)

    duplicate_titles = {
        value: count
        for value, count in Counter(titles).items()
        if value and count > 1
    }

    duplicate_descriptions = {
        value: count
        for value, count in Counter(descriptions).items()
        if value and count > 1
    }

    if duplicate_titles:
        failures.append(
            f"duplicate titles: {len(duplicate_titles)}"
        )

    if duplicate_descriptions:
        failures.append(
            f"duplicate descriptions: "
            f"{len(duplicate_descriptions)}"
        )

    if failures:
        raise SystemExit(
            "Parent Quest validation failed:\n"
            + "\n".join(failures)
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild Parent Quest from the approved canonical source."
        )
    )

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Destination directory for the rebuilt microsite.",
    )

    parser.add_argument(
        "--allow-live",
        action="store_true",
        help=(
            "Allow writing directly to the live parent-quest directory. "
            "Use only after explicit approval."
        ),
    )

    args = parser.parse_args()

    if not CANONICAL.is_dir():
        raise SystemExit(
            f"Missing canonical source: {CANONICAL}"
        )

    output = args.output.expanduser().resolve()
    live = LIVE_SITE.resolve()
    canonical = CANONICAL.resolve()

    if output == canonical:
        raise SystemExit(
            "Refusing to overwrite the canonical source."
        )

    if output == live and not args.allow_live:
        raise SystemExit(
            "Refusing to overwrite the live Parent Quest site. "
            "Use --allow-live only after explicit approval."
        )

    validate(CANONICAL)

    if output.exists():
        shutil.rmtree(output)

    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(CANONICAL, output)

    validate(output)

    canonical_hashes = relative_file_hashes(CANONICAL)
    output_hashes = relative_file_hashes(output)

    if canonical_hashes != output_hashes:
        raise SystemExit(
            "Rebuilt output differs from the canonical source."
        )

    manifest = {
        "source": str(CANONICAL),
        "output": str(output),
        "html_pages": len(list(output.rglob("index.html"))),
        "sitemap_urls": 101,
        "files_verified": len(output_hashes),
        "byte_identical": True,
    }

    manifest_path = output / "canonical-build-manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    print("Parent Quest canonical build passed.")
    print(f"Output: {output}")
    print(f"HTML pages: {manifest['html_pages']}")
    print(f"Verified files: {manifest['files_verified']}")
    print("Canonical files byte-identical: yes")


if __name__ == "__main__":
    main()
