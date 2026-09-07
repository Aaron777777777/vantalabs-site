#!/usr/bin/env python3
from pathlib import Path
import shutil
import re
import html
import json

ROOT = Path.cwd()
GUARDIAN = ROOT / "guardian"
BACKUP = ROOT / "guardian.before-90-page-seo-system"
CSS = GUARDIAN / "assets" / "guardian.css"

if not (ROOT / "index.html").exists():
    raise SystemExit("Run this from ~/Projects/vantalabs-site")

if not GUARDIAN.exists():
    raise SystemExit("guardian/ was not found.")

if not BACKUP.exists():
    raise SystemExit(
        "guardian.before-90-page-seo-system was not found. "
        "That backup is needed to restore the polished Guardian design."
    )

# Back up the current generated state before replacing it.
safety = ROOT / "guardian.before-polished-94-page-rebuild"
if safety.exists():
    shutil.rmtree(safety)
shutil.copytree(GUARDIAN, safety)

# Restore the exact CSS from the approved pre-expansion design.
backup_css = BACKUP / "assets" / "guardian.css"
if not backup_css.exists():
    raise SystemExit("The polished backup CSS was not found.")
shutil.copy2(backup_css, CSS)

# Pick the polished school-run page as the visual master.
master_candidates = [
    BACKUP / "track-the-school-run" / "index.html",
    BACKUP / "school-run-safety-app" / "index.html",
    BACKUP / "set-up-child-device" / "index.html",
]

master_path = next((p for p in master_candidates if p.exists()), None)
if master_path is None:
    raise SystemExit("Could not find a polished Guardian detail page in the backup.")

master = master_path.read_text()

def esc(value):
    return html.escape(value, quote=True)

def text_between(pattern, source, default=""):
    match = re.search(pattern, source, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", "", match.group(1)).strip() if match else default

def attr(pattern, source, default=""):
    match = re.search(pattern, source, flags=re.S | re.I)
    return html.unescape(match.group(1)).strip() if match else default

def clean_title(value):
    return value.split("|")[0].strip()

def editorial_heading(keyword):
    k = keyword.lower()

    if "school" in k:
        return "Useful school-run updates, without watching the map"
    if "home" in k:
        return "Clear Home updates when a journey begins or ends"
    if "safe zone" in k or "geofence" in k or "place alert" in k:
        return "Place alerts for the moments that matter"
    if "sos" in k or "emergency" in k:
        return "An extra way to reach trusted adults"
    if "privacy" in k or "private" in k:
        return "Family location sharing with clearer boundaries"
    if "map" in k or "real-time" in k or "location" in k:
        return "Useful location context when you genuinely need it"
    if "life360" in k or "alternative" in k or "best" in k:
        return "A simpler way to compare family location tools"
    if "free" in k or "premium" in k:
        return "Guardian plans for different family needs"
    if "iphone" in k or "android" in k:
        return "Guardian across the phones your family uses"
    if "set up" in k or "how" in k or "what is" in k:
        return "A practical Guardian guide for parents"

    return "A calmer way to stay informed"

def human_copy(keyword, title):
    k = keyword.lower()

    if "school" in k:
        return (
            "Guardian focuses on the four school-run moments parents usually care about most: "
            "leaving Home, arriving at School, leaving School and returning Home. Safe-zone alerts "
            "can provide those updates without turning the Family Map into something that needs to "
            "be watched throughout the journey.",
            "When more context is useful, Guardian shows the connected phone’s latest available "
            "location, battery level and last update time. GPS, signal and phone settings can affect "
            "reporting, so Guardian is designed to support ordinary family communication rather than replace it."
        )

    if "home" in k:
        return (
            "Home alerts help parents understand when an everyday journey has started or finished. "
            "A connected child phone can trigger a leaving or arrival notification around the family’s "
            "Home safe zone, reducing the need for repeated messages during familiar routines.",
            "The Family Map remains available when extra context is genuinely needed, alongside battery "
            "level and last update time. Location can still be affected by GPS, signal, permissions and "
            "battery settings, so direct family communication always remains important."
        )

    if "safe zone" in k or "geofence" in k or "place alert" in k:
        return (
            "Guardian safe zones create simple virtual boundaries around familiar places such as Home "
            "and School. Parents can receive useful arrival and leaving alerts without following every "
            "movement on a map, making the feature better suited to ordinary routines.",
            "Safe-zone timing depends on the connected phone’s available location readings and can be "
            "affected by buildings, weak signal, permissions or battery restrictions. The alerts provide "
            "helpful context, but they should not be treated as perfectly immediate or guaranteed."
        )

    if "sos" in k or "emergency" in k:
        return (
            "Guardian gives a connected child device an SOS option for reaching trusted adults. "
            "The resulting family alert can include the latest available location and device context, "
            "helping parents decide how to respond and who should make contact.",
            "Guardian is not an emergency service and an SOS notification cannot guarantee delivery. "
            "Families should agree in advance who responds, when to call the child and when emergency "
            "services must be contacted directly."
        )

    if "privacy" in k or "private" in k or "controlled" in k:
        return (
            "Guardian keeps family location information inside a private, parent-managed account. "
            "There are no public profiles, followers, advertising feeds or social features, and adult "
            "location sharing remains optional.",
            "Children should understand what is shared, which trusted adults can see it and why the family "
            "has chosen to use the app. Clear conversations and reviewed access are just as important as "
            "the technology itself."
        )

    if "life360" in k or "alternative" in k or "best" in k:
        return (
            "Families comparing location apps usually need more than a long feature list. Privacy, clear "
            "access controls, useful place alerts, device context and honest accuracy limits all matter "
            "when deciding which service fits everyday family life.",
            "Guardian is designed for families who want a private Family Map, Home and School alerts, "
            "recent location context and SOS tools without public profiles or a social feed. The right "
            "choice depends on the routines and boundaries each family is comfortable with."
        )

    if "free" in k or "premium" in k:
        return (
            "Guardian’s core experience is designed to make family location tools straightforward. "
            "Parents can connect a child profile, use private location features and receive useful "
            "place-based updates without filling the app with unrelated social features.",
            "Guardian Premium is intended for families who need support for additional child profiles. "
            "Final availability and store information will be shown on the official App Store and Google "
            "Play pages once the release is approved."
        )

    if "iphone" in k or "android" in k:
        return (
            "Guardian is being prepared for families using iPhone, Android or a mixture of both. "
            "Connected devices share the latest available information inside the same private family, "
            "with Home and School alerts, map context and device status.",
            "Background location behaviour differs between phones and operating systems. Permissions, "
            "battery optimisation and connectivity can all affect updates, so each connected device needs "
            "to be configured correctly."
        )

    if "how" in k or "what is" in k or "set up" in k:
        return (
            f"{title} should be straightforward rather than technical. Guardian brings the relevant setup, "
            "location context and family controls together so parents can understand what the connected "
            "phone is sharing and how everyday alerts are produced.",
            "Phone location always has practical limits. GPS, signal, permissions, battery settings and "
            "operating-system restrictions can affect updates, so Guardian should be used openly and "
            "alongside direct family communication."
        )

    return (
        f"Guardian approaches {keyword} as a practical family tool rather than something parents need to "
        "watch all day. It combines Home and School alerts, a private Family Map, recent location history, "
        "battery status and SOS tools inside one parent-managed family.",
        "The latest available location is shown with useful context, but no phone app can promise perfect "
        "accuracy or guaranteed notification delivery. Used openly and proportionately, Guardian can reduce "
        "repeated check-in messages while leaving room for trust and independence."
    )

def replace_once(source, pattern, replacement, label):
    updated, count = re.subn(pattern, replacement, source, count=1, flags=re.S | re.I)
    if count != 1:
        raise RuntimeError(f"Could not replace {label}")
    return updated

# Find all generated SEO pages from the failed expansion.
generated = []
for page in GUARDIAN.glob("*/index.html"):
    source = page.read_text()
    if "guardian-seo-page" not in source:
        continue

    slug = page.parent.name
    title_tag = attr(r"<title>(.*?)</title>", source, slug.replace("-", " ").title())
    name = clean_title(title_tag)
    h1 = text_between(r"<h1>(.*?)</h1>", source, name)
    keyword = text_between(r'<div class="eyebrow">(.*?)</div>', source, name)
    description = attr(
        r'<meta\s+name="description"\s+content="(.*?)"',
        source,
        f"Explore {name.lower()} with Guardian."
    )
    canonical = attr(
        r'<link\s+rel="canonical"\s+href="(.*?)"',
        source,
        f"https://www.vantalabs.co.uk/guardian/{slug}/"
    )

    related_section = re.search(
        r'<section class="related">.*?</section>',
        source,
        flags=re.S | re.I
    )
    faq_section = re.search(
        r'<section class="faq">.*?</section>',
        source,
        flags=re.S | re.I
    )

    generated.append({
        "page": page,
        "slug": slug,
        "name": name,
        "h1": h1,
        "keyword": keyword,
        "description": description,
        "canonical": canonical,
        "related": related_section.group(0) if related_section else "",
        "faq": faq_section.group(0) if faq_section else "",
    })

if not generated:
    raise SystemExit("No generated Guardian SEO pages were found to rebuild.")

for item in generated:
    page = master

    # Metadata.
    page = replace_once(page, r"<title>.*?</title>",
                        f"<title>{esc(item['name'])} | Guardian by Vanta Labs</title>",
                        "title")
    page = replace_once(page,
                        r'<meta\s+name="description"\s+content=".*?">',
                        f'<meta name="description" content="{esc(item["description"])}">',
                        "description")
    page = replace_once(page,
                        r'<link\s+rel="canonical"\s+href=".*?">',
                        f'<link rel="canonical" href="{esc(item["canonical"])}">',
                        "canonical")

    # Open Graph metadata when present.
    page = re.sub(r'<meta\s+property="og:title"\s+content=".*?">',
                  f'<meta property="og:title" content="{esc(item["name"])} | Guardian by Vanta Labs">',
                  page, count=1, flags=re.S | re.I)
    page = re.sub(r'<meta\s+property="og:description"\s+content=".*?">',
                  f'<meta property="og:description" content="{esc(item["description"])}">',
                  page, count=1, flags=re.S | re.I)
    page = re.sub(r'<meta\s+property="og:url"\s+content=".*?">',
                  f'<meta property="og:url" content="{esc(item["canonical"])}">',
                  page, count=1, flags=re.S | re.I)

    # Hero.
    page = replace_once(page,
                        r'(<div class="eyebrow">).*?(</div>)',
                        rf'\1{esc(item["keyword"])}\2',
                        "eyebrow")
    page = replace_once(page, r"<h1>.*?</h1>",
                        f"<h1>{esc(item['h1'])}</h1>",
                        "H1")
    page = replace_once(page,
                        r'(<p class="lead">).*?(</p>)',
                        rf'\1{esc(item["description"])}\2',
                        "hero description")

    # Article.
    article_h2 = editorial_heading(item["keyword"])
    p1, p2 = human_copy(item["keyword"], item["name"])

    page = replace_once(page,
                        r'(<section class="long-copy">\s*<h2>).*?(</h2>)',
                        rf'\1{esc(article_h2)}\2',
                        "article heading")
    page = replace_once(
        page,
        r'(<div class="long-copy-text">).*?(</div>\s*</section>)',
        rf'\1<p>{esc(p1)}</p><p>{esc(p2)}</p>\2',
        "article paragraphs"
    )

    # Preserve the generated page-specific related links and FAQ.
    if item["related"]:
        page = replace_once(page,
                            r'<section class="related">.*?</section>',
                            item["related"],
                            "related section")
    if item["faq"]:
        page = replace_once(page,
                            r'<section class="faq">.*?</section>',
                            item["faq"],
                            "FAQ section")

    # Ensure old generator class is removed so only the polished CSS applies.
    page = page.replace(" guardian-seo-page", "")

    item["page"].write_text(page)

# Remove the failed expansion CSS block if it somehow remained.
css = CSS.read_text()
marker = "/* Guardian 90-page SEO system */"
if marker in css:
    css = css[:css.index(marker)].rstrip() + "\n"
CSS.write_text(css)

report = {
    "rebuilt_pages": len(generated),
    "master_template": str(master_path.relative_to(ROOT)),
    "css_restored_from": str(backup_css.relative_to(ROOT)),
    "committed": False,
    "pushed": False,
    "deployed": False,
}
(ROOT / "guardian-polished-rebuild-report.json").write_text(
    json.dumps(report, indent=2)
)

print(f"Rebuilt {len(generated)} Guardian SEO pages from the approved polished template.")
print(f"Restored Guardian CSS from {backup_css.relative_to(ROOT)}.")
print("Replaced oversized generic headings and shortened the copy.")
print("Preserved page metadata, FAQs, related links and sitemap URLs.")
print("Nothing was committed, pushed or deployed.")
