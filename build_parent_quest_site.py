from __future__ import annotations

# PARENT_QUEST_LEGACY_WRITE_GUARD
import os as _parent_quest_guard_os

if (
    _parent_quest_guard_os.environ.get(
        "PARENT_QUEST_ALLOW_LEGACY_REBUILD"
    )
    != "I_UNDERSTAND_THIS_CAN_OVERWRITE_FINISHED_COPY"
):
    raise SystemExit(
        "Legacy Parent Quest writer locked. "
        "Use build_parent_quest_from_canonical.py for safe rebuilds."
    )


import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "parent-quest"
PLAN_PATH = ROOT / "parent_quest_page_plan.json"
BASE_URL = "https://vantalabs.co.uk"

ANDROID_URL = (
    "https://play.google.com/store/apps/details"
    "?id=com.vantalabs.parentquest"
)
IOS_URL = (
    "https://apps.apple.com/us/app/parent-quest/"
    "id6782297539"
)

plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
pages = plan["pages"]

page_by_path = {page["path"]: page for page in pages}

if len(pages) < 2:
    raise SystemExit("Expected Parent Quest pages")

if len(page_by_path) != len(pages):
    raise SystemExit("Duplicate Parent Quest paths")

approved_home = SITE / "index.html"
approved_detail = SITE / "chore-chart-app/index.html"
approved_css = SITE / "assets/parent-quest.css"

for required in (approved_home, approved_detail, approved_css):
    if not required.is_file():
        raise SystemExit(f"Missing approved prototype file: {required}")


CLUSTER_LABELS = {
    "chore-charts": "Chore charts",
    "daily-chores": "Daily chores",
    "kids-tasks": "Kids tasks",
    "family-routines": "Family routines",
    "rewards": "Family rewards",
    "coins": "Reward coins",
    "parent-approval": "Parent approval",
    "child-profiles": "Child profiles",
    "parent-device": "Parent device",
    "guides": "Parent guide",
}


CLUSTER_OPENINGS = {
    "chore-charts": (
        "A chore chart gives everyday household tasks a visible place in "
        "the family routine."
    ),
    "daily-chores": (
        "Daily chores are easier to follow when the parent can keep them "
        "together in one straightforward list."
    ),
    "kids-tasks": (
        "Clear task lists help children understand what has been chosen "
        "for them without turning the routine into a complicated system."
    ),
    "family-routines": (
        "Family routines become easier to repeat when regular tasks, "
        "progress and rewards are organised in the same place."
    ),
    "rewards": (
        "A family reward works best when the parent chooses what is "
        "appropriate and connects it to progress they have reviewed."
    ),
    "coins": (
        "Reward coins provide a simple in-app way to represent progress "
        "towards rewards created by the parent."
    ),
    "parent-approval": (
        "Parent approval keeps completed chores under adult control before "
        "progress or rewards are confirmed."
    ),
    "child-profiles": (
        "Separate child profiles help a parent keep chores, progress and "
        "rewards organised for each child."
    ),
    "parent-device": (
        "Parent Quest is intended to be managed on a parent-owned device, "
        "keeping setup and approval with the adult."
    ),
    "guides": (
        "A useful family chore system does not need to be complicated; it "
        "needs to be clear, manageable and suitable for the household."
    ),
}


CLUSTER_SECOND_PARAGRAPHS = {
    "chore-charts": (
        "Parent Quest lets the parent decide which chores appear, which "
        "child profile they belong to and how completed progress should be "
        "reviewed."
    ),
    "daily-chores": (
        "The app can bring repeated daily tasks alongside other chores so "
        "the parent can shape a routine that reflects their own home."
    ),
    "kids-tasks": (
        "Tasks remain parent created and parent managed. The app does not "
        "replace the adult’s judgement about what is suitable or complete."
    ),
    "family-routines": (
        "Each household can choose its own balance of tasks, reward coins "
        "and custom rewards without relying on a fixed reward catalogue."
    ),
    "rewards": (
        "Rewards shown in Parent Quest are created and managed by the "
        "parent. They are not issued, funded or guaranteed by Vanta Labs."
    ),
    "coins": (
        "Coins in Parent Quest have no monetary value inside the app and "
        "remain part of the family’s own parent-managed reward system."
    ),
    "parent-approval": (
        "The Parent PIN approval flow helps separate a child marking a task "
        "from the parent deciding whether that progress should be accepted."
    ),
    "child-profiles": (
        "Profiles can keep each child’s own tasks and progress distinct "
        "while the parent continues to manage the overall family system."
    ),
    "parent-device": (
        "Using one parent-owned device keeps the parent in control of task "
        "creation, approval, reward coins and custom rewards."
    ),
    "guides": (
        "Parent Quest can support that routine by keeping child profiles, "
        "chores, approval and rewards together on a parent-owned device."
    ),
}


CLUSTER_NOTICES = {
    "chore-charts": (
        "Chores should remain suitable for the child’s age, abilities and "
        "the parent’s own household expectations."
    ),
    "daily-chores": (
        "Daily task lists should stay realistic. A shorter routine that is "
        "used consistently is often clearer than an overloaded checklist."
    ),
    "kids-tasks": (
        "The parent remains responsible for choosing, explaining and "
        "supervising every task."
    ),
    "family-routines": (
        "Parent Quest supports organisation but does not replace parental "
        "supervision or safeguarding."
    ),
    "rewards": (
        "Custom rewards are promises managed by the parent or guardian, not "
        "rewards supplied by Vanta Labs."
    ),
    "coins": (
        "Reward coins are an in-app family progress measure and are not "
        "cash, stored value or a financial product."
    ),
    "parent-approval": (
        "Keep the Parent PIN private so approval remains under the parent "
        "or guardian’s control."
    ),
    "child-profiles": (
        "Use names or nicknames that are appropriate for your family and "
        "avoid entering unnecessary personal information."
    ),
    "parent-device": (
        "Parent Quest is designed for parent-controlled use on a device "
        "owned or managed by the parent or guardian."
    ),
    "guides": (
        "Every family is different. Choose chores and rewards that fit the "
        "child, household and parent’s own judgement."
    ),
}


def sentence_title(title: str) -> str:
    if not title:
        return title
    return title[0].lower() + title[1:]


def schema_json(data: object) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":"),
    )


def absolute_url(path: str) -> str:
    return f"{BASE_URL}{path}"


def related_pages(page: dict) -> list[dict]:
    cluster_pages = [
        candidate
        for candidate in pages
        if (
            candidate["cluster"] == page["cluster"]
            and candidate["path"] != page["path"]
        )
    ]

    leader_path = page["cluster_leader"]
    leader = page_by_path.get(leader_path)

    chosen: list[dict] = []

    if leader and leader["path"] != page["path"]:
        chosen.append(leader)

    for candidate in cluster_pages:
        if candidate not in chosen:
            chosen.append(candidate)
        if len(chosen) == 4:
            break

    if len(chosen) < 4:
        for candidate in pages[1:]:
            if (
                candidate["path"] != page["path"]
                and candidate not in chosen
            ):
                chosen.append(candidate)
            if len(chosen) == 4:
                break

    return chosen[:4]


def faq_items(page: dict) -> list[tuple[str, str]]:
    title = page["title"]
    cluster = page["cluster"]

    if cluster == "guides":
        return [
            (
                f"What should parents consider when using this {title.lower()} guide?",
                (
                    "Parents should choose chores, expectations and rewards "
                    "that fit their own child, household and family routine."
                ),
            ),
            (
                "How can Parent Quest support the routine?",
                (
                    "Parent Quest can organise child profiles, chores, "
                    "parent-approved progress, reward coins and custom rewards."
                ),
            ),
            (
                "Does Parent Quest replace parental supervision?",
                (
                    "No. Parent Quest is an organisation tool and is not a "
                    "replacement for parental supervision or safeguarding."
                ),
            ),
        ]

    return [
        (
            f"What does {sentence_title(title)} help organise?",
            (
                f"It focuses on {page['intent']} within a parent-managed "
                "system of child profiles, chores, progress and rewards."
            ),
        ),
        (
            "Who controls tasks and approval in Parent Quest?",
            (
                "The parent or guardian creates the family system and "
                "reviews completed progress through the parent-controlled "
                "approval flow."
            ),
        ),
        (
            "Are Parent Quest rewards supplied by Vanta Labs?",
            (
                "No. Reward coins and custom rewards are created and "
                "managed by the parent and are not funded or guaranteed by "
                "Vanta Labs."
            ),
        ),
    ]


def guide_intro(page: dict) -> str:
    title = page["title"]

    options = [
        (
            f"{title} starts with deciding what the family actually needs "
            "from the routine. Keep the first version small enough to "
            "explain clearly and use consistently."
        ),
        (
            f"When thinking about {sentence_title(title)}, begin with the "
            "child’s age, the household’s normal routine and what the "
            "parent can realistically review."
        ),
        (
            f"A practical approach to {sentence_title(title)} is to choose "
            "a few clear expectations, explain them and adjust the system "
            "after seeing how it works at home."
        ),
    ]

    position = int(page.get("position", 1))
    return options[(position - 1) % len(options)]


def page_copy(page: dict) -> tuple[str, str, str, str]:
    cluster = page["cluster"]
    title = page["title"]
    position = int(page.get("position", 1))

    if cluster == "guides":
        heading_options = [
            "Keep the family system clear and manageable",
            "Build a routine that works in your own home",
            "Start simply, then adjust the routine",
            "Use chores and rewards with a clear purpose",
        ]

        heading = heading_options[(position - 1) % len(heading_options)]
        paragraph_one = guide_intro(page)
        paragraph_two = CLUSTER_SECOND_PARAGRAPHS[cluster]
        notice = CLUSTER_NOTICES[cluster]
        return heading, paragraph_one, paragraph_two, notice

    heading_options = [
        f"A clearer way to use {sentence_title(title)}",
        f"Keep {sentence_title(title)} simple and parent managed",
        f"Bring {sentence_title(title)} into the family routine",
        f"Organise {sentence_title(title)} without unnecessary clutter",
        f"Make {sentence_title(title)} easier to review",
    ]

    heading = heading_options[(position - 1) % len(heading_options)]

    opening = CLUSTER_OPENINGS[cluster]
    paragraph_one = (
        f"{title} focuses on {page['intent']} in Parent Quest. "
        f"{opening}"
    )

    paragraph_two = CLUSTER_SECOND_PARAGRAPHS[cluster]
    notice = CLUSTER_NOTICES[cluster]

    return heading, paragraph_one, paragraph_two, notice


def detail_schema(page: dict) -> list[dict]:
    faqs = faq_items(page)

    schemas: list[dict] = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Parent Quest",
            "applicationCategory": "LifestyleApplication",
            "operatingSystem": "Android, iOS",
            "description": page["description"],
            "url": absolute_url(page["path"]),
            "downloadUrl": [ANDROID_URL, IOS_URL],
            "image": f"{BASE_URL}/parentquest.png",
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
                    "name": "Parent Quest",
                    "item": f"{BASE_URL}/parent-quest/",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page["title"],
                    "item": absolute_url(page["path"]),
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
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": page["title"],
                "description": page["description"],
                "mainEntityOfPage": absolute_url(page["path"]),
                "author": {
                    "@type": "Organization",
                    "name": "Vanta Labs",
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Vanta Labs",
                    "url": f"{BASE_URL}/",
                },
            }
        )

    return schemas


def render_detail(page: dict) -> str:
    heading, paragraph_one, paragraph_two, notice = page_copy(page)
    related = related_pages(page)
    faqs = faq_items(page)
    label = CLUSTER_LABELS[page["cluster"]]

    related_html = "\n".join(
        f'''<a class="card" href="{item["path"]}">
<small>{html.escape(CLUSTER_LABELS.get(item["cluster"], "Parent Quest"))}</small>
<strong>{html.escape(item["title"])}</strong>
</a>'''
        for item in related
    )

    faq_html = "\n".join(
        f'''<details>
<summary>{html.escape(question)}</summary>
<p>{html.escape(answer)}</p>
</details>'''
        for question, answer in faqs
    )

    page_title = f'{page["title"]} | Parent Quest'
    canonical = absolute_url(page["path"])

    return f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>

<title>{html.escape(page_title)}</title>

<meta
  name="description"
  content="{html.escape(page["description"], quote=True)}"
/>

<link rel="canonical" href="{canonical}"/>
<meta content="index,follow,max-image-preview:large" name="robots"/>

<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Vanta Labs"/>
<meta property="og:title" content="{html.escape(page["title"], quote=True)}"/>
<meta
  property="og:description"
  content="{html.escape(page["description"], quote=True)}"
/>
<meta property="og:url" content="{canonical}"/>
<meta
  property="og:image"
  content="https://vantalabs.co.uk/parentquest.png"
/>

<meta name="twitter:card" content="summary_large_image"/>

<link href="/parent-quest/assets/parent-quest-icon.png" rel="icon"/>
<link href="/parent-quest/assets/parent-quest.css" rel="stylesheet"/>
<script defer src="/parent-quest/assets/app-links.js"></script>

<script type="application/ld+json">
{schema_json(detail_schema(page))}
</script>
</head>

<body class="parent-quest-detail">
<header class="head">
<nav>
<a class="brand" href="/">Vanta Labs</a>

<div class="links">
<a href="/parent-quest/">Parent Quest</a>
<a href="/parent-quest/chore-chart-app/">Chore charts</a>
<a href="/parent-quest/parent-pin-approval/">Parent approval</a>
<a href="/parent-quest/custom-rewards-for-kids/">Rewards</a>
</div>
</nav>
</header>

<main>
<div class="hero">
<div>
<span class="eyebrow">{html.escape(label)}</span>

<h1>{html.escape(page["h1"])}</h1>

<p class="lead">
{html.escape(page["description"])}
</p>

<div class="ctas">
<a class="btn" data-store="android">Google Play</a>
<a class="btn" data-store="ios">App Store</a>
</div>
</div>

<div class="iconbox">
<img
  alt="Parent Quest app icon"
  height="512"
  src="/parent-quest/assets/parent-quest-icon.png"
  width="512"
/>
</div>
</div>

<article class="body">
<section class="long-copy">
<h2>{html.escape(heading)}</h2>

<div class="long-copy-text">
<p>{html.escape(paragraph_one)}</p>
<p>{html.escape(paragraph_two)}</p>
</div>
</section>

<div class="notice">
<strong>Parent controlled by design.</strong>
{html.escape(notice)}
</div>

<div class="parent-quest-lower-grid">
<section class="related">
<h2>Keep exploring Parent Quest</h2>

<div class="grid">
{related_html}
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
'''


generated = 0
preserved = {
    "/parent-quest/",
    "/parent-quest/chore-chart-app/",
}

for page in pages:
    if page["path"] in preserved:
        continue

    relative = page["path"].removeprefix("/parent-quest/").strip("/")
    destination = SITE / relative / "index.html"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        render_detail(page),
        encoding="utf-8",
    )
    generated += 1


sitemap_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]

for page in pages:
    sitemap_lines.extend([
        "  <url>",
        f"    <loc>{absolute_url(page['path'])}</loc>",
        "  </url>",
    ])

sitemap_lines.append("</urlset>")

(SITE / "sitemap.xml").write_text(
    "\n".join(sitemap_lines) + "\n",
    encoding="utf-8",
)

print(f"Generated detail pages: {generated}")
print(f"Total planned pages: {len(pages)}")
print("Created separate sitemap: parent-quest/sitemap.xml")
