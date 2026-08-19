#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path.cwd()
SITE = ROOT / "vanta-shift"
PLAN_PATH = ROOT / "vanta_shift_page_plan.json"

BASE_URL = "https://vantalabs.co.uk"
ANDROID_URL = (
    "https://play.google.com/store/apps/details"
    "?id=com.vantashift.app"
)
IOS_URL = (
    "https://apps.apple.com/us/app/"
    "shift-planner-rota-hours/id6771880899"
)

plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
planned_pages = plan["pages"]

if len(planned_pages) < 2:
    raise SystemExit("Expected homepage plus supporting pages")

supporting_pages = [
    page
    for page in planned_pages
    if page["path"] != "/vanta-shift/"
]

if len(supporting_pages) != len(planned_pages) - 1:
    raise SystemExit(
        f"Expected {len(planned_pages)-1} supporting pages, found {len(supporting_pages)}"
    )

if not (SITE / "index.html").is_file():
    raise SystemExit("Approved Vanta Shift homepage is missing")

if not (SITE / "assets" / "vanta-shift.css").is_file():
    raise SystemExit("Approved Vanta Shift stylesheet is missing")


CLUSTERS = {
    "shift-calendar": {
        "label": "Shift calendar",
        "focus": (
            "assigned work shifts, upcoming working days and the employee’s "
            "personal schedule"
        ),
        "benefit": (
            "see what shift comes next without relying on screenshots, "
            "messages or a paper rota"
        ),
        "limit": (
            "The calendar represents scheduled work and does not prove that "
            "a shift was completed."
        ),
    },
    "rota-viewing": {
        "label": "Your rota",
        "focus": (
            "the employee’s own rota, working days and upcoming scheduled "
            "shifts"
        ),
        "benefit": (
            "keep a personal view of assigned shifts available on a mobile "
            "device"
        ),
        "limit": (
            "The employer remains the source of the official rota and any "
            "subsequent changes."
        ),
    },
    "notifications": {
        "label": "Shift notifications",
        "focus": (
            "reminders connected to upcoming or changed assigned shifts"
        ),
        "benefit": (
            "reduce the chance of overlooking the next working time or shift "
            "change"
        ),
        "limit": (
            "Notification delivery can be affected by device permissions, "
            "battery settings and operating-system behaviour."
        ),
    },
    "hours": {
        "label": "Scheduled hours",
        "focus": (
            "shift durations and weekly or monthly scheduled-hour totals"
        ),
        "benefit": (
            "understand how assigned shifts contribute to the week or month"
        ),
        "limit": (
            "Scheduled-hour totals are personal planning information rather "
            "than an official attendance or payroll record."
        ),
    },
    "earnings": {
        "label": "Estimated pay",
        "focus": (
            "estimated earnings calculated from available shift and hourly "
            "rate information"
        ),
        "benefit": (
            "form a clearer personal estimate of what scheduled shifts may "
            "earn"
        ),
        "limit": (
            "Actual pay can differ because of payroll rules, deductions, "
            "premiums, overtime and employer-held information."
        ),
    },
    "shift-patterns": {
        "label": "Shift patterns",
        "focus": (
            "repeating and rotating working patterns shown in a personal "
            "calendar"
        ),
        "benefit": (
            "understand how days, nights and rest days repeat across future "
            "weeks"
        ),
        "limit": (
            "A displayed pattern should still be checked against the latest "
            "official rota."
        ),
    },
    "common-patterns": {
        "label": "Common rota patterns",
        "focus": (
            "patterns such as 4 on 4 off, Panama, continental and alternating "
            "shifts"
        ),
        "benefit": (
            "visualise a repeating rotation without manually calculating "
            "every future working day"
        ),
        "limit": (
            "Employers can use local variations, so the configured pattern "
            "must match the employee’s real rota."
        ),
    },
    "night-shifts": {
        "label": "Night shifts",
        "focus": (
            "overnight work, changing sleep periods and upcoming night duties"
        ),
        "benefit": (
            "see night work alongside rest days and other assigned shifts"
        ),
        "limit": (
            "The app supports personal planning but does not provide medical "
            "or fatigue-management advice."
        ),
    },
    "workers": {
        "label": "Shift-based work",
        "focus": (
            "personal schedules for employees working changing days, nights "
            "and weekends"
        ),
        "benefit": (
            "keep a clear mobile view of assigned work across a changing rota"
        ),
        "limit": (
            "Workplace arrangements differ, and the employer’s official "
            "schedule always takes priority."
        ),
    },
    "guides": {
        "label": "Vanta Shift guide",
        "focus": (
            "practical ways to understand assigned shifts, notifications, "
            "hours and estimated pay"
        ),
        "benefit": (
            "make a changing work schedule easier to understand and plan "
            "around"
        ),
        "limit": (
            "The guidance is general and does not replace an employer’s rota, "
            "payroll information or workplace policy."
        ),
    },
}


OPENINGS = [
    (
        "{title} is useful when an employee wants a clearer personal view of "
        "{focus}."
    ),
    (
        "The practical purpose of {title_lower} is to make {focus} easier to "
        "understand during an ordinary working week."
    ),
    (
        "Employees usually look for {title_lower} when a changing rota is "
        "becoming difficult to follow through messages, screenshots or paper."
    ),
    (
        "{title} brings {focus} into one place so the next working day is "
        "easier to see."
    ),
    (
        "A good {title_lower} should answer the employee’s immediate question "
        "without adding another complicated workplace system."
    ),
    (
        "{title} is centred entirely on the employee’s own assigned schedule, "
        "reminders, hours and estimated earnings."
    ),
    (
        "The value of {title_lower} comes from turning {focus} into a clearer "
        "personal calendar."
    ),
    (
        "For employees working changing patterns, {title_lower} can make the "
        "week ahead much easier to read."
    ),
]

SECOND_PARAGRAPHS = [
    (
        "Vanta Shift helps the employee {benefit}. The app remains focused on "
        "assigned shifts, reminders, scheduled hours and estimated earnings."
    ),
    (
        "The employee can use Vanta Shift to {benefit}. Its purpose stays "
        "limited to the employee’s own assigned schedule and personal totals."
    ),
    (
        "The main benefit is being able to {benefit}. That personal view can "
        "support planning around work, rest days and other commitments."
    ),
    (
        "Vanta Shift is designed to {benefit}. The information stays centred "
        "on the employee’s own work schedule."
    ),
    (
        "A clear mobile calendar can help the employee {benefit}, especially "
        "when shifts repeat or change across the month."
    ),
    (
        "The app provides a simpler way to {benefit}, while keeping official "
        "rota and payroll responsibilities with the employer."
    ),
]

THIRD_PARAGRAPHS = [
    (
        "The employee should still check unusual changes or missing "
        "information against the latest employer-issued rota."
    ),
    (
        "Clear notifications and accurate shift details depend on the latest "
        "information being available in the app."
    ),
    (
        "The app is most useful when the displayed pattern, assigned shifts "
        "and pay settings reflect the employee’s real arrangements."
    ),
    (
        "It supports personal planning rather than replacing formal employer "
        "records."
    ),
    (
        "Any difference between the app and an official schedule should be "
        "checked before relying on the displayed shift."
    ),
    (
        "Employees should treat the app as a personal view of the information "
        "available rather than the source of workplace policy."
    ),
]

HEADINGS = [
    "A clearer view of the working week",
    "Keep the next shift easy to find",
    "Your own schedule in one place",
    "A practical view of changing shifts",
    "Make the rota easier to understand",
    "See how the month is taking shape",
    "From assigned shift to personal plan",
    "Designed around the employee’s week",
]

GUIDE_HEADINGS = [
    "The practical idea behind this guide",
    "What employees should understand first",
    "A clearer approach to changing shifts",
    "Where the official rota still matters",
    "How to use the information sensibly",
    "Planning around a changing schedule",
]


PAGE_NOTES = {
    "/vanta-shift/personal-shift-calendar/": (
        "A personal shift calendar is intended to sit alongside the rest of "
        "the employee’s life. It helps show working days, rest days and "
        "changing duties in a format that is quick to check privately."
    ),
    "/vanta-shift/work-schedule-calendar/": (
        "A work schedule calendar concentrates on the structure of upcoming "
        "employment: dates, shift types and the sequence of scheduled work "
        "across the week or month."
    ),
    "/vanta-shift/hourly-pay-shift-tracker/": (
        "An hourly-pay view starts with the employee’s configured hourly "
        "rate and applies it to scheduled shift durations to form a personal "
        "estimate before official payroll adjustments."
    ),
    "/vanta-shift/weekly-earnings-tracker/": (
        "A weekly earnings view groups estimated shift value inside one "
        "seven-day period, helping the employee compare one working week "
        "with another."
    ),
    "/vanta-shift/night-shift-calendar/": (
        "A night-shift calendar makes evening start times and next-morning "
        "finish times easier to distinguish from ordinary daytime duties."
    ),
    "/vanta-shift/overnight-shift-calendar/": (
        "An overnight calendar is especially useful when one scheduled shift "
        "crosses midnight and therefore occupies parts of two calendar dates."
    ),
    "/vanta-shift/monthly-work-rota/": (
        "A monthly rota gives a broader view of work, rest days and repeating "
        "patterns across the complete calendar month."
    ),
    "/vanta-shift/weekly-work-rota/": (
        "A weekly rota keeps attention on the immediate seven-day schedule, "
        "making the next few assigned shifts quicker to review."
    ),
    "/vanta-shift/estimated-wages-calculator/": (
        "An estimated-wages calculation brings together scheduled duration "
        "and the available pay rate to provide a forward-looking personal "
        "figure."
    ),
    "/vanta-shift/work-pay-calculator/": (
        "A work-pay calculation helps the employee explore how different "
        "scheduled hours may affect the approximate value of a working period."
    ),
    "/vanta-shift/employee-shift-calendar/": (
        "An employee shift calendar is centred on one person’s assigned work "
        "rather than the schedules of a wider team."
    ),
    "/vanta-shift/weekly-shift-calendar/": (
        "A weekly shift calendar narrows the view to the current or upcoming "
        "week so near-term working days remain easy to scan."
    ),
}


def stable_index(path: str, salt: str, length: int) -> int:
    digest = hashlib.sha256(
        f"{salt}:{path}".encode("utf-8")
    ).hexdigest()
    return int(digest[:8], 16) % length


def choose(items, path: str, salt: str):
    return items[stable_index(path, salt, len(items))]


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def canonical(path: str) -> str:
    return f"{BASE_URL}{path}"


def target_file(path: str) -> Path:
    relative = path.removeprefix("/vanta-shift/").strip("/")
    return SITE / relative / "index.html"


def context_for(page: dict) -> dict:
    cluster = page.get("cluster", "shift-calendar")
    return CLUSTERS.get(cluster, CLUSTERS["shift-calendar"])


def related_pages(page: dict) -> list[dict]:
    selected = []
    leader_path = page.get("cluster_leader")

    if leader_path and leader_path != page["path"]:
        leader = next(
            (
                other
                for other in supporting_pages
                if other["path"] == leader_path
            ),
            None,
        )

        if leader is not None:
            selected.append(leader)

    same_cluster = [
        other
        for other in supporting_pages
        if other["path"] != page["path"]
        and other.get("cluster") == page.get("cluster")
        and other not in selected
    ]

    same_cluster.sort(key=lambda item: item["path"])

    if same_cluster:
        start = stable_index(
            page["path"],
            "related",
            len(same_cluster),
        )
        same_cluster = same_cluster[start:] + same_cluster[:start]

    for other in same_cluster:
        if len(selected) == 4:
            break
        selected.append(other)

    if len(selected) < 4:
        for other in supporting_pages:
            if (
                other["path"] != page["path"]
                and other not in selected
            ):
                selected.append(other)

            if len(selected) == 4:
                break

    return selected[:4]


def faqs_for(page: dict, context: dict) -> list[tuple[str, str]]:
    title = page["title"]

    return [
        (
            f"What does {title.lower()} show?",
            (
                f"It focuses on {context['focus']}, using the shift "
                "information available in Vanta Shift."
            ),
        ),
        (
            "What is Vanta Shift intended to help with?",
            (
                "Vanta Shift helps employees view assigned shifts, receive "
                "notifications and review scheduled hours and estimated pay."
            ),
        ),
        (
            "Should I still check the official rota?",
            context["limit"],
        ),
    ]


def schema_for(
    page: dict,
    description: str,
    faqs: list[tuple[str, str]],
) -> str:
    items = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Vanta Shift",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Android, iOS",
            "description": description,
            "url": canonical(page["path"]),
            "downloadUrl": [ANDROID_URL, IOS_URL],
            "image": f"{BASE_URL}/vanta-shift.png",
            "publisher": {
                "@type": "Organization",
                "name": "Vanta Labs",
                "url": f"{BASE_URL}/",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Vanta Labs",
                    "item": f"{BASE_URL}/",
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "Vanta Shift",
                    "item": f"{BASE_URL}/vanta-shift/",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page["title"],
                    "item": canonical(page["path"]),
                },
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": answer,
                    },
                }
                for question, answer in faqs
            ],
        },
    ]

    if page["type"] == "guide":
        items.append(
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": page["title"],
                "description": description,
                "datePublished": "2026-07-31",
                "dateModified": "2026-07-31",
                "author": {
                    "@type": "Organization",
                    "name": "Vanta Labs",
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Vanta Labs",
                },
            }
        )

    return json.dumps(
        items,
        ensure_ascii=False,
        separators=(",", ":"),
    ).replace("</", "<\\/")


def render_related(page: dict) -> str:
    cards = []

    for related in related_pages(page):
        related_context = context_for(related)

        cards.append(
            f"""
<a class="card" href="{esc(related['path'])}">
<small>{esc(related_context['label'])}</small>
<strong>{esc(related['title'])}</strong>
</a>""".strip()
        )

    return "\n".join(cards)


def render_page(page: dict) -> str:
    context = context_for(page)
    description = page["description"]
    faqs = faqs_for(page, context)

    values = {
        **context,
        "title": page["title"],
        "title_lower": page["title"].lower(),
    }

    opening = choose(
        OPENINGS,
        page["path"],
        "opening",
    ).format(**values)

    second = choose(
        SECOND_PARAGRAPHS,
        page["path"],
        "second",
    ).format(**values)

    third = choose(
        THIRD_PARAGRAPHS,
        page["path"],
        "third",
    )

    page_note = PAGE_NOTES.get(page["path"], "")

    if page["type"] == "guide":
        heading = choose(
            GUIDE_HEADINGS,
            page["path"],
            "heading",
        )
    else:
        heading = choose(
            HEADINGS,
            page["path"],
            "heading",
        )

    faq_html = "\n".join(
        f"""<details>
<summary>{esc(question)}</summary>
<p>{esc(answer)}</p>
</details>"""
        for question, answer in faqs
    )

    body_class = (
        "workforce-detail vanta-shift-guide"
        if page["type"] == "guide"
        else "workforce-detail"
    )

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>

<title>{esc(page['title'])} | Vanta Shift</title>

<meta
  name="description"
  content="{esc(description)}"
/>

<link
  rel="canonical"
  href="{esc(canonical(page['path']))}"
/>

<meta content="index,follow,max-image-preview:large" name="robots"/>

<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Vanta Labs"/>
<meta property="og:title" content="{esc(page['title'])}"/>
<meta property="og:description" content="{esc(description)}"/>
<meta property="og:url" content="{esc(canonical(page['path']))}"/>
<meta
  property="og:image"
  content="{BASE_URL}/vanta-shift.png"
/>

<meta name="twitter:card" content="summary_large_image"/>

<link href="/vanta-shift/assets/vanta-shift-icon.png" rel="icon"/>
<link href="/vanta-shift/assets/vanta-shift.css" rel="stylesheet"/>
<script defer src="/vanta-shift/assets/app-links.js"></script>

<script type="application/ld+json">
{schema_for(page, description, faqs)}
</script>
</head>

<body class="{body_class}">
<header class="head">
<nav>
<a class="brand" href="/">Vanta Labs</a>

<div class="links">
<a href="/vanta-shift/">Vanta Shift</a>
<a href="/vanta-shift/shift-calendar-app/">Shift calendar</a>
<a href="/vanta-shift/shift-notification-app/">Notifications</a>
<a href="/vanta-shift/shift-earnings-tracker/">Estimated pay</a>
</div>
</nav>
</header>

<main>
<div class="hero">
<div>
<span class="eyebrow">{esc(context['label'])}</span>

<h1>{esc(page['title'])}</h1>

<p class="lead">
{esc(description)}
</p>

<div class="ctas">
<a class="btn" data-store="android">Google Play</a>
<a class="btn" data-store="ios">App Store</a>
</div>
</div>

<div class="iconbox">
<img
  alt="Vanta Shift app icon"
  height="512"
  src="/vanta-shift/assets/vanta-shift-icon.png"
  width="512"
/>
</div>
</div>

<article class="body">
<section class="long-copy">
<h2>{esc(heading)}</h2>

<div class="long-copy-text">
<p>{esc(opening)} {esc(second)}</p>
<p>{esc(page_note + " " if page_note else "")}{esc(third)}</p>
</div>
</section>

<div class="notice">
<strong>{esc(context['label'])} remains a personal planning view.</strong>
{esc(context['limit'])}
</div>

<div class="workforce-lower-grid">
<section class="related">
<h2>Keep exploring Vanta Shift</h2>

<div class="grid">
{render_related(page)}
</div>
</section>

<section class="faq">
<h2>Quick questions</h2>
{faq_html}
</section>
</div>
</article>
</main>

<footer>
<span>© 2026 Vanta Labs NW LTD · Manchester, UK</span>
<span>
<a href="/privacy.html">Privacy</a> ·
<a href="/terms.html">Terms</a> ·
<a href="/">All Vanta Labs apps</a>
</span>
</footer>
</body>
</html>
"""


generated = 0

for page in supporting_pages:
    target = target_file(page["path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        render_page(page),
        encoding="utf-8",
    )
    generated += 1


urls = [
    f"{BASE_URL}/vanta-shift/",
    *[
        canonical(page["path"])
        for page in sorted(
            supporting_pages,
            key=lambda item: item["path"],
        )
    ],
]

sitemap = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]

for url in urls:
    sitemap.extend(
        [
            "  <url>",
            f"    <loc>{html.escape(url)}</loc>",
            "  </url>",
        ]
    )

sitemap.append("</urlset>")

(SITE / "sitemap.xml").write_text(
    "\n".join(sitemap) + "\n",
    encoding="utf-8",
)

manifest = {
    "product": "Vanta Shift",
    "scope": (
        "Employee shift viewing, notifications, scheduled hours and "
        "estimated pay"
    ),
    "generated_supporting_pages": generated,
    "total_html_pages": len(list(SITE.rglob("index.html"))),
    "sitemap_urls": len(urls),
    "android_url": ANDROID_URL,
    "ios_url": IOS_URL,
    "root_homepage_modified": False,
    "root_sitemap_modified": False,
    "workforce_modified": False,
    "guardian_modified": False,
}

(SITE / "build-manifest.json").write_text(
    json.dumps(
        manifest,
        indent=2,
        ensure_ascii=False,
    ) + "\n",
    encoding="utf-8",
)

print("Generated supporting pages:", generated)
print("Total HTML pages:", manifest["total_html_pages"])
print("Sitemap URLs:", manifest["sitemap_urls"])
print("Root homepage modified: no")
print("Root sitemap modified: no")
print("Vanta Workforce modified: no")
print("Guardian modified: no")

# PAGE-SPECIFIC SEO DIFFERENTIATION
def _differentiate_shift_page(slug, description, heading, p1, p2):
    path = SITE / slug / "index.html"
    source = path.read_text(encoding="utf-8")

    source = re.sub(
        r'<meta content="[^"]*" name="description"/>',
        f'<meta content="{html.escape(description, quote=True)}" name="description"/>',
        source,
        count=1,
    )
    source = re.sub(
        r'<meta property="og:description" content="[^"]*"/>',
        f'<meta property="og:description" content="{html.escape(description, quote=True)}"/>',
        source,
        count=1,
    )
    source = re.sub(
        r'<p class="lead">.*?</p>',
        f'<p class="lead">{html.escape(description)}</p>',
        source,
        count=1,
        flags=re.S,
    )
    source = re.sub(
        r'<section class="long-copy">\s*<h2>.*?</h2>\s*<div class="long-copy-text">\s*<p>.*?</p>\s*<p>.*?</p>',
        (
            f'<section class="long-copy">\n'
            f'<h2>{html.escape(heading)}</h2>\n'
            f'<div class="long-copy-text">\n'
            f'<p>{html.escape(p1)}</p>\n'
            f'<p>{html.escape(p2)}</p>'
        ),
        source,
        count=1,
        flags=re.S,
    )

    path.write_text(source, encoding="utf-8")


_differentiate_shift_page(
    "police-shift-calendar",
    "Plan personal police shift patterns, rest days and changing day or night duties with Vanta Shift.",
    "Keep changing police shifts clear in one personal calendar",
    "Police rotas can move between early, late, night and rest periods. A personal shift calendar helps keep those changing duties visible without turning Vanta Shift into an employer scheduling or workforce system.",
    "Workers can enter their own known shifts, review upcoming working days and see how repeating patterns affect their time. The employer remains the source of the official rota and any later changes."
)

_differentiate_shift_page(
    "paramedic-shift-calendar",
    "Plan personal paramedic shifts, long duties, nights and rest days with a clear Vanta Shift calendar.",
    "Plan paramedic duties around long and irregular shifts",
    "Paramedic schedules can include long duties, overnight work, changing start times and recovery days. Keeping those shifts in a personal calendar makes it easier to see the working pattern alongside upcoming time off.",
    "Vanta Shift can help an individual organise their own known rota, scheduled hours and estimated earnings. It does not manage ambulance staff, allocate crews or replace an employer-issued rota."
)
