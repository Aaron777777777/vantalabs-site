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

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "parent-quest"
PLAN = json.loads(
    (ROOT / "parent_quest_page_plan.json").read_text(encoding="utf-8")
)

pages = PLAN["pages"]

LEADS = {
    "chore-charts":
        "Create a clear chore chart for your family, assign jobs to the right child and review what has been completed.",
    "daily-chores":
        "Keep everyday chores in one simple list so children can see what needs doing and parents can review the result.",
    "kids-tasks":
        "Give each child a clear task list while keeping setup, changes and approval with the parent.",
    "family-routines":
        "Bring repeated chores, family routines and rewards together without turning home life into a complicated system.",
    "rewards":
        "Create rewards that suit your own family and connect them to progress you have actually reviewed.",
    "coins":
        "Use simple reward coins to show progress towards family-created rewards without treating them like real money.",
    "parent-approval":
        "Review completed chores through the Parent PIN before progress and reward coins are confirmed.",
    "child-profiles":
        "Keep each child’s chores, progress and rewards separate in a profile managed by the parent.",
    "parent-device":
        "Run the family chore and reward system from one parent-owned device without creating separate child accounts.",
    "guides":
        "Practical ideas for building a family chore routine that is clear, realistic and easy to keep using.",
}

DESCRIPTIONS = {
    "chore-charts":
        "Create family chore charts with child profiles, parent approval and rewards chosen by you.",
    "daily-chores":
        "Organise children’s everyday chores in a clear routine managed and approved by the parent.",
    "kids-tasks":
        "Give each child a personal task list while keeping the family setup under parent control.",
    "family-routines":
        "Bring chores, repeated tasks and family rewards into one flexible routine.",
    "rewards":
        "Create custom family rewards linked to progress reviewed by the parent.",
    "coins":
        "Use parent-managed reward coins to show progress towards family-created rewards.",
    "parent-approval":
        "Review completed chores with the Parent PIN before progress and rewards are confirmed.",
    "child-profiles":
        "Keep each child’s chores, progress and rewards in a separate parent-managed profile.",
    "parent-device":
        "Manage chores, child profiles, approval and rewards from one parent-owned device.",
    "guides":
        "Practical guidance for building clear family chores, routines and parent-managed rewards.",
}

FAQS = {
    "chore-charts": [
        (
            "Can parents choose which chores appear?",
            "Yes. The parent decides which chores are used, which child they belong to and when they should be completed.",
        ),
        (
            "Can completed chores be checked?",
            "Yes. The parent can review completed progress before rewards or reward coins are confirmed.",
        ),
        (
            "Does Parent Quest replace parental supervision?",
            "No. The parent or guardian remains responsible for the child, the chores and the rewards.",
        ),
    ],
    "daily-chores": [
        (
            "Do all chores have to happen every day?",
            "No. Parents choose which jobs belong in the daily routine and which should stay occasional.",
        ),
        (
            "Can different children have different routines?",
            "Yes. Each child profile can have its own chores and expectations.",
        ),
        (
            "Who decides whether a chore is complete?",
            "The parent or guardian reviews the child’s progress through the approval flow.",
        ),
    ],
    "kids-tasks": [
        (
            "Can each child have a different task list?",
            "Yes. Parents can organise separate tasks for different child profiles.",
        ),
        (
            "Who creates the tasks?",
            "The parent or guardian creates and manages the tasks.",
        ),
        (
            "Does the app decide whether a task is suitable?",
            "No. The parent remains responsible for choosing age-appropriate tasks.",
        ),
    ],
    "family-routines": [
        (
            "Can the family routine be changed later?",
            "Yes. Parents can adjust chores, rewards and expectations whenever family life changes.",
        ),
        (
            "Do rewards have to be used for every chore?",
            "No. Parents decide when rewards are useful and when chores are simply part of family life.",
        ),
        (
            "Does Parent Quest replace parental supervision?",
            "No. It helps organise the routine but does not replace parental judgement or supervision.",
        ),
    ],
    "rewards": [
        (
            "Who creates the rewards?",
            "The parent or guardian creates and provides every reward.",
        ),
        (
            "Are rewards supplied by Vanta Labs?",
            "No. Vanta Labs does not fund, supply or guarantee family rewards.",
        ),
        (
            "Can rewards be changed?",
            "Yes. Parents can change the reward list as the family’s interests and circumstances change.",
        ),
    ],
    "coins": [
        (
            "Are reward coins real money?",
            "No. They are an in-app way to show progress and have no cash value.",
        ),
        (
            "Who decides how many coins a task is worth?",
            "The parent controls how reward coins are used inside the family routine.",
        ),
        (
            "Can coins be exchanged with Vanta Labs?",
            "No. Reward coins cannot be withdrawn, purchased from or exchanged with Vanta Labs.",
        ),
    ],
    "parent-approval": [
        (
            "Why does Parent Quest use a Parent PIN?",
            "The PIN helps keep approval and protected parent actions under adult control.",
        ),
        (
            "Can children approve their own chores?",
            "No. Approval is intended to remain with the parent or guardian.",
        ),
        (
            "Does approval have to be complicated?",
            "No. It is designed as a quick parent check before progress is confirmed.",
        ),
    ],
    "child-profiles": [
        (
            "Can each child have their own profile?",
            "Yes. Each child can have separate chores, progress and rewards.",
        ),
        (
            "Do child profiles need separate accounts?",
            "No. They remain part of the parent-managed family setup.",
        ),
        (
            "How much personal information is needed?",
            "Parents should only enter what the family needs. A first name or nickname is often enough.",
        ),
    ],
    "parent-device": [
        (
            "Does every child need their own phone?",
            "No. Parent Quest is designed to be managed from a parent-owned device.",
        ),
        (
            "Do children need email accounts?",
            "No. Child profiles are not separate email-based accounts.",
        ),
        (
            "Who controls settings and approval?",
            "The parent or guardian controls protected settings, approval and rewards.",
        ),
    ],
    "guides": [
        (
            "Should every family use the same chore routine?",
            "No. Chores and rewards should suit the individual child and household.",
        ),
        (
            "How many chores should parents start with?",
            "A small, realistic list is usually easier to explain and maintain.",
        ),
        (
            "Can the routine be changed later?",
            "Yes. Parents should review what works and adjust anything that creates unnecessary friction.",
        ),
    ],
}


def page_file(page: dict) -> Path:
    if page["path"] == "/parent-quest/":
        return SITE / "index.html"

    slug = page["path"].removeprefix("/parent-quest/").strip("/")
    return SITE / slug / "index.html"


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    updated, count = re.subn(
        pattern,
        replacement,
        text,
        count=1,
        flags=re.I | re.S,
    )
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return updated


def update_schema(text: str, page: dict, description: str) -> str:
    pattern = re.compile(
        r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',
        re.I | re.S,
    )

    def replacement(match: re.Match[str]) -> str:
        data = json.loads(match.group(2))

        def visit(value):
            if isinstance(value, list):
                for item in value:
                    visit(item)
                return

            if not isinstance(value, dict):
                return

            schema_type = value.get("@type")

            if schema_type == "SoftwareApplication":
                value["description"] = description

            if schema_type == "Article":
                value["description"] = description

            if schema_type == "FAQPage":
                value["mainEntity"] = [
                    {
                        "@type": "Question",
                        "name": question,
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": answer,
                        },
                    }
                    for question, answer in FAQS[page["cluster"]]
                ]

            for child in value.values():
                visit(child)

        visit(data)

        encoded = json.dumps(
            data,
            ensure_ascii=False,
            separators=(",", ":"),
        )

        return match.group(1) + encoded + match.group(3)

    updated, count = pattern.subn(replacement, text)

    if count != 1:
        raise RuntimeError(
            f"{page['path']}: expected one JSON-LD block, found {count}"
        )

    return updated


changed = 0

for page in pages:
    file = page_file(page)
    text = file.read_text(encoding="utf-8")

    if page["path"] == "/parent-quest/":
        continue

    cluster = page["cluster"]
    lead = LEADS[cluster]
    description = DESCRIPTIONS[cluster]

    text = replace_once(
        text,
        r'<p class="lead">.*?</p>',
        f'<p class="lead">\n{html.escape(lead)}\n</p>',
        f"{file}: lead",
    )

    text = replace_once(
        text,
        r'(<meta\s+name="description"\s+content=")[^"]*("\s*/>)',
        rf'\g<1>{html.escape(description, quote=True)}\g<2>',
        f"{file}: description",
    )

    text = replace_once(
        text,
        r'(<meta\s+property="og:description"\s+content=")[^"]*("\s*/>)',
        rf'\g<1>{html.escape(description, quote=True)}\g<2>',
        f"{file}: og description",
    )

    faq_html = "\n".join(
        f"""<details>
<summary>{html.escape(question)}</summary>
<p>{html.escape(answer)}</p>
</details>"""
        for question, answer in FAQS[cluster]
    )

    text = replace_once(
        text,
        r'(<section class="faq">\s*<h2>Quick questions</h2>).*?(</section>)',
        rf'\1\n{faq_html}\n\2',
        f"{file}: FAQ",
    )

    text = update_schema(text, page, description)

    file.write_text(text, encoding="utf-8")
    changed += 1

print(f"Cleaned Parent Quest pages: {changed}")
