#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path.cwd()
WORKFORCE = ROOT / "workforce"
PLAN_PATH = ROOT / "workforce_page_plan.json"
BASE_URL = "https://vantalabs.co.uk"

if not WORKFORCE.is_dir():
    raise SystemExit("Missing approved workforce prototype directory.")

if not (WORKFORCE / "index.html").is_file():
    raise SystemExit("Missing approved Workforce homepage.")

if not (WORKFORCE / "assets" / "workforce.css").is_file():
    raise SystemExit("Missing approved Workforce CSS.")

plan_data = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
planned_pages = plan_data["pages"]

pages = [
    page for page in planned_pages
    if page["path"] != "/workforce/"
]

if len(planned_pages) < 2:
    raise SystemExit(
        f"Expected a homepage plus supporting pages, found {len(planned_pages)}."
    )

if len(pages) != len(planned_pages) - 1:
    raise SystemExit(
        f"Expected {len(planned_pages) - 1} supporting pages, found {len(pages)}."
    )


CLUSTERS = {
    "attendance": {
        "label": "Staff attendance",
        "focus": "booking activity, attendance history and recorded working periods",
        "worker": "a clear booking action at the beginning and end of attendance",
        "manager": "whether the attendance record is complete and needs correction",
        "risk": "forgotten bookings, delayed records or unusual attendance durations",
        "limit": "Attendance records should be reviewed before payroll, accounting or employment decisions.",
    },
    "clocking": {
        "label": "Clocking in and out",
        "focus": "the start and end points of each recorded attendance period",
        "worker": "a repeatable booking-on and booking-off routine",
        "manager": "when attendance began, when it ended and whether anything is missing",
        "risk": "missed book-off actions, late entries or incorrect booking times",
        "limit": "A booking record supports review but does not automatically explain every workplace circumstance.",
    },
    "gps-attendance": {
        "label": "GPS and location-aware attendance",
        "focus": "attendance information supported by the latest available device-location context",
        "worker": "knowing when location is requested and what happens when it is unavailable",
        "manager": "whether the location context supports the recorded workplace activity",
        "risk": "poor signal, restricted permissions, GPS drift or delayed location updates",
        "limit": "Location can be delayed or inaccurate and should never be treated as infallible proof.",
    },
    "timesheets": {
        "label": "Timesheets and working hours",
        "focus": "My Hours, monthly attendance periods and timesheet records",
        "worker": "being able to review available hours and identify missing attendance",
        "manager": "whether the recorded periods accurately describe the hours under review",
        "risk": "incomplete attendance being mistaken for a final payroll-ready total",
        "limit": "Timesheets and exports must be checked before they are used outside Vanta Workforce.",
    },
    "workplace-presence": {
        "label": "Workplace presence",
        "focus": "the latest available worker status connected to attendance history",
        "worker": "knowing that the expected booking action has been received",
        "manager": "who is currently recorded as working at the relevant workplace",
        "risk": "confusing delayed device information with a definite absence",
        "limit": "Current status is an operational view and may be affected by delayed or incomplete data.",
    },
    "mobile-workforces": {
        "label": "Mobile and field workforces",
        "focus": "off-site bookings, field attendance and working-hour history",
        "worker": "a consistent attendance process from a supported mobile device",
        "manager": "how attendance is recorded across changing sites and field locations",
        "risk": "weak connectivity or unclear expectations producing inconsistent records",
        "limit": "Mobile attendance still needs a documented fallback for signal, device and account problems.",
    },
    "worker-safety": {
        "label": "Worker safety and scheduled checks",
        "focus": "scheduled prompts, worker phone checks and relevant incident information",
        "worker": "knowing what response is expected and who follows up when something is wrong",
        "manager": "which checks are due, complete or require a human response",
        "risk": "treating an app notification as a complete workplace-safety system",
        "limit": "Vanta Workforce supports workplace procedures but is not an emergency service.",
    },
    "control-centre": {
        "label": "Control Centre",
        "focus": "worker status, workplace activity and authorised management checks",
        "worker": "having relevant attendance and check actions reflected accurately",
        "manager": "which workers are active and which records require attention",
        "risk": "making decisions from stale, incomplete or misunderstood device data",
        "limit": "Managers remain responsible for reviewing timestamps, context and appropriate follow-up.",
    },
    "reporting": {
        "label": "Attendance reporting and exports",
        "focus": "attendance history, monthly reports and authorised timesheet exports",
        "worker": "having recorded hours represented clearly and consistently",
        "manager": "whether the selected workers, dates and periods are correct",
        "risk": "using an unchecked export as a final payroll or accounting conclusion",
        "limit": "Reports and exports are operational records and require verification before further use.",
    },
    "operations": {
        "label": "Workforce operations",
        "focus": "workplaces, workers, roles and attendance activity in one operational system",
        "worker": "seeing only the actions and information relevant to their role",
        "manager": "whether sites, access and worker records match the real organisation",
        "risk": "unclear ownership of setup, corrections or ongoing administration",
        "limit": "The organisation remains responsible for user access, workplace configuration and policy.",
    },
    "scheduling": {
        "label": "Staff scheduling and rotas",
        "focus": "planned shifts, staff assignments, workplace schedules and the connection between scheduled work and attendance",
        "worker": "seeing assigned shifts clearly enough to know when and where work is expected",
        "manager": "whether the right workers are assigned to the right shifts and workplaces",
        "risk": "last-minute changes, outdated rotas or unclear assignments creating confusion",
        "limit": "Published schedules still need human review when staffing needs, availability or workplace circumstances change.",
    },
}


OPENINGS = [
    (
        "{intent_title} is most useful when a business wants to replace "
        "scattered messages, paper records or end-of-month guesswork with "
        "one repeatable process."
    ),
    (
        "Businesses normally look for {intent} when the working day is "
        "creating information in too many separate places."
    ),
    (
        "The practical purpose of {intent} is not simply to digitise a form. "
        "It is to produce a clearer record that remains useful after the "
        "working day has finished."
    ),
    (
        "{intent_title} becomes valuable when workers and managers need the "
        "same understanding of what was recorded, when it happened and what "
        "still needs checking."
    ),
    (
        "A useful {intent} process begins with the real workplace routine, "
        "not with the software screen."
    ),
    (
        "Organisations considering {intent} are usually trying to make a "
        "daily worker action easier to review later."
    ),
    (
        "The question behind {intent} is straightforward: how can the "
        "business create a clearer record without adding unnecessary work?"
    ),
    (
        "{intent_title} can bring structure to a process that otherwise "
        "depends heavily on memory, messages or manual reconciliation."
    ),
]

WORKER_PARAGRAPHS = [
    (
        "For the worker, the important part is {worker}. The organisation "
        "should explain what counts as completion and what to do when a "
        "device, account or connection problem prevents the normal action."
    ),
    (
        "Workers mainly need {worker}. Clear onboarding matters because even "
        "a technically valid record can be misunderstood when the expected "
        "workplace process has not been explained."
    ),
    (
        "From the worker’s perspective, success means {worker}. A fair "
        "exception route should also exist for genuine mistakes and device "
        "problems."
    ),
    (
        "The worker-facing process centres on {worker}. It should remain "
        "understandable during busy arrivals, departures, site moves and "
        "scheduled checks."
    ),
    (
        "The app supplies the mobile action; the business supplies the "
        "expectation. Here that means {worker}, together with a known support "
        "route."
    ),
    (
        "Workers are more likely to use the process consistently when they "
        "understand its purpose. In this case, that purpose is {worker}."
    ),
]

MANAGER_PARAGRAPHS = [
    (
        "For an authorised manager, the useful question is {manager}. "
        "Vanta Workforce keeps {focus} together so the review does not depend "
        "on collecting separate updates."
    ),
    (
        "Management value comes from being able to understand {manager}. "
        "The system organises {focus}; the manager still decides whether "
        "follow-up or correction is appropriate."
    ),
    (
        "The relevant management view focuses on {manager}. It uses {focus}, "
        "while preserving the need to check unusual or incomplete records."
    ),
    (
        "A manager needs more than a list of taps. They need to assess "
        "{manager}, using {focus} and the surrounding workplace context."
    ),
    (
        "The manager view is intended to make {manager} easier to review. "
        "It presents {focus} without pretending that every device event tells "
        "the complete story."
    ),
    (
        "Authorised managers can use the available record to examine "
        "{manager}. That evidence includes {focus} and should be read with "
        "its timing and workplace circumstances."
    ),
]

PROCESS_PARAGRAPHS = [
    (
        "A sensible rollout is to define the expected action, show workers "
        "how it works and agree who reviews exceptions. This matters because "
        "{risk} can still occur during normal use."
    ),
    (
        "Before launch, the business should document the routine and the "
        "correction process. That prevents {risk} from becoming an automatic "
        "assumption about the worker."
    ),
    (
        "The most reliable approach is to test the process with the team, "
        "explain the available records and review {risk} proportionately."
    ),
    (
        "Good records begin before anyone opens the app. The organisation "
        "should set clear expectations and establish how {risk} will be "
        "handled."
    ),
    (
        "The app works best inside an explicit operating process. Managers "
        "should know how to distinguish a genuine concern from {risk}."
    ),
    (
        "Rollout should include a short explanation, a test action and a "
        "known support route, particularly because of {risk}."
    ),
]

HEADINGS = [
    "A clearer record for the real working day",
    "From worker action to useful review",
    "A practical process for everyday operations",
    "Where this fits inside Vanta Workforce",
    "Turning daily activity into a usable record",
    "A simpler way to review the working day",
    "What the organisation actually needs to see",
    "Making the workplace process easier to follow",
]

GUIDE_HEADINGS = [
    "The practical idea behind this guide",
    "What businesses should decide first",
    "How to introduce the process clearly",
    "Where human review still matters",
    "A sensible approach for real workplaces",
    "What the technology can and cannot do",
]


PAGE_OVERRIDES = {
    "/workforce/attendance-history-app/": {
        "description": (
            "Review past attendance records in Vanta Workforce, including recorded "
            "working periods, dates and worker activity that managers can revisit later."
        ),
        "heading": "Look back at recorded attendance clearly",
        "opening": (
            "Attendance history is about reviewing what was recorded previously rather "
            "than only looking at who is working right now. A useful history gives the "
            "business a chronological place to revisit earlier attendance periods."
        ),
        "worker": (
            "For workers, that historical view can make it easier to identify a missing, "
            "unexpected or incomplete attendance period and raise it through the "
            "organisation's normal correction process."
        ),
        "manager": (
            "For managers, the value is being able to look back across previous dates "
            "and recorded working periods when checking what happened. Historical "
            "records are more useful when the original attendance information remains "
            "clear rather than being reconstructed later from messages or memory."
        ),
        "process": (
            "Older records should still be reviewed in context. A past booking time or "
            "duration can show what reached the system, but unusual entries may still "
            "need an explanation before any correction or employment decision is made."
        ),
        "notice": (
            "Historical attendance is an operational record and should be reviewed in "
            "context before it is relied upon for payroll, accounting or employment decisions."
        ),
        "faqs": [
            (
                "What is attendance history used for?",
                "It gives authorised users a way to look back at previously recorded "
                "attendance periods and review earlier worker activity."
            ),
            (
                "What if an older attendance record looks wrong?",
                "It should be reviewed using the organisation's normal correction "
                "process rather than treated as automatically accurate."
            ),
            (
                "Is attendance history the same as a final payroll record?",
                "No. Historical attendance can support later review, but the relevant "
                "records still need checking before payroll or accounting use."
            ),
        ],
    },

    "/workforce/monthly-attendance-reports/": {
        "description": (
            "Review monthly attendance reports in Vanta Workforce, bringing recorded "
            "attendance for a selected monthly period into a clearer management view."
        ),
        "heading": "Review attendance one monthly period at a time",
        "opening": (
            "Monthly attendance reporting turns day-to-day attendance activity into a "
            "period that is easier to review as a whole. Instead of checking isolated "
            "bookings one by one, managers can approach the month's available records "
            "as one reporting period."
        ),
        "worker": (
            "Workers benefit when the underlying attendance is kept complete throughout "
            "the month, because missing or incorrect bookings can otherwise carry into "
            "the later report."
        ),
        "manager": (
            "For managers, the practical job is to check that the selected month, workers "
            "and recorded periods match what is actually being reviewed. The monthly view "
            "helps organise that information without turning an unchecked total into a "
            "final conclusion."
        ),
        "process": (
            "A sensible month-end process is to review exceptions and incomplete "
            "attendance before relying on the report elsewhere. Corrections should be "
            "made through the agreed business process so the resulting period reflects "
            "the best available record."
        ),
        "notice": (
            "Monthly reports summarise available attendance information; they still need "
            "verification before payroll, accounting or other external use."
        ),
        "faqs": [
            (
                "What does a monthly attendance report help managers review?",
                "It brings the available attendance information for a selected monthly "
                "period into one clearer review process."
            ),
            (
                "What happens if attendance is missing during the month?",
                "The underlying record may be incomplete, so the business should review "
                "and correct genuine exceptions before relying on the monthly report."
            ),
            (
                "Does a monthly attendance report replace payroll?",
                "No. It is an operational attendance record and should be verified before "
                "being used for payroll or accounting."
            ),
        ],
    },

    "/workforce/distributed-workforce-attendance/": {
        "description": (
            "Use one attendance process for a distributed workforce working across "
            "multiple sites, field locations and changing workplaces."
        ),
        "heading": "One attendance process across a distributed team",
        "opening": (
            "Distributed workforce attendance becomes important when the team is not "
            "working from one fixed workplace. Staff may be spread across sites, field "
            "locations or changing jobs while the business still needs a consistent "
            "attendance process."
        ),
        "worker": (
            "For workers, consistency matters more than where the day's job happens. "
            "The expected booking routine should remain understandable when moving "
            "between workplaces, while genuine connectivity or device problems need a "
            "known fallback."
        ),
        "manager": (
            "Managers need to review activity across the workforce without assuming "
            "every person is operating under identical site conditions. Bringing "
            "off-site bookings, field attendance and working-hour history together can "
            "make differences between locations easier to investigate."
        ),
        "process": (
            "The organisation should define the attendance process across all relevant "
            "workplaces, including who reviews exceptions when workers move between "
            "sites or cannot complete the normal mobile action."
        ),
        "notice": (
            "A distributed attendance process still needs clear site expectations and a "
            "fallback for connectivity, device or account problems."
        ),
        "faqs": [
            (
                "What does distributed workforce attendance mean?",
                "It describes an attendance process used by workers spread across "
                "multiple sites, field locations or changing workplaces."
            ),
            (
                "Can different sites create different attendance conditions?",
                "Yes. Connectivity, workplace layout and device conditions can vary, so "
                "managers should review unusual records with the relevant site context."
            ),
            (
                "Should distributed teams use a fallback attendance process?",
                "Yes. The organisation should define what workers do when connectivity, "
                "device or account problems prevent the normal action."
            ),
        ],
    },

    "/workforce/off-site-worker-attendance/": {
        "description": (
            "Record and review attendance for workers carrying out authorised work away "
            "from the normal workplace, with mobile bookings and working-hour context."
        ),
        "heading": "Attendance when work happens away from the usual workplace",
        "opening": (
            "Off-site worker attendance is specifically about work performed away from "
            "the organisation's normal workplace. The challenge is giving that worker a "
            "clear attendance routine without requiring a fixed desk, terminal or office."
        ),
        "worker": (
            "The worker needs to understand when the off-site attendance action is "
            "expected and what to do if the mobile device cannot complete it. The "
            "process should remain simple enough to use while travelling between jobs "
            "or working at an authorised external location."
        ),
        "manager": (
            "For the manager, an off-site record provides context for attendance that "
            "cannot be checked against a conventional fixed workplace routine. Available "
            "booking information and working-hour history can support review when the "
            "worker's job legitimately takes place elsewhere."
        ),
        "process": (
            "The business should define what counts as authorised off-site work and how "
            "exceptions are handled. That prevents an unusual mobile record from being "
            "treated as evidence of a problem without first checking the circumstances."
        ),
        "notice": (
            "An off-site attendance record reflects the available booking and device "
            "context; it does not explain every moment or circumstance of a working day."
        ),
        "faqs": [
            (
                "What is off-site worker attendance?",
                "It is attendance recorded for authorised work carried out away from the "
                "organisation's normal or fixed workplace."
            ),
            (
                "Can mobile conditions affect an off-site attendance record?",
                "Yes. Connectivity, permissions, device settings and other conditions can "
                "affect what reaches the service."
            ),
            (
                "Does an off-site attendance record explain the whole working day?",
                "No. It provides available attendance context, but unusual records still "
                "need human review and the surrounding workplace circumstances."
            ),
        ],
    },
}


def stable_index(path: str, salt: str, count: int) -> int:
    digest = hashlib.sha256(
        f"{salt}:{path}".encode("utf-8")
    ).hexdigest()
    return int(digest[:8], 16) % count


def choose(items, path: str, salt: str):
    return items[stable_index(path, salt, len(items))]


def esc(value: str) -> str:
    return html.escape(str(value), quote=True)


def clean_title(value: str) -> str:
    value = value.strip()
    value = re.sub(
        r"^(?:Vanta Workforce Guide|Vanta Workforce)\s*\|\s*",
        "",
        value,
        flags=re.I,
    )
    value = re.sub(
        r"\s*\|\s*Vanta Workforce\s*$",
        "",
        value,
        flags=re.I,
    )
    value = re.sub(
        r"\s*\|\s*Vanta Labs\s*$",
        "",
        value,
        flags=re.I,
    )
    return value.strip()


def sentence_case(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    return value[0].upper() + value[1:]


def web_path_to_file(path: str) -> Path:
    relative = path.removeprefix("/workforce/").strip("/")
    return WORKFORCE / relative / "index.html"


def canonical(path: str) -> str:
    return f"{BASE_URL}{path}"


def title_for(page: dict) -> str:
    raw = (
        page.get("title")
        or page.get("seo_title")
        or page.get("h1")
        or page.get("name")
        or page.get("intent")
        or page["path"].strip("/").split("/")[-1].replace("-", " ").title()
    )
    raw = clean_title(raw)

    if page.get("type") == "guide":
        return f"{raw} | Vanta Workforce"

    return f"{raw} | Vanta Workforce"


def h1_for(page: dict) -> str:
    raw = (
        page.get("h1")
        or page.get("headline")
        or page.get("title")
        or page.get("intent")
        or page["path"].strip("/").split("/")[-1].replace("-", " ")
    )
    return clean_title(sentence_case(raw))


def intent_for(page: dict) -> str:
    return (
        page.get("intent")
        or clean_title(page.get("title", ""))
        or page["path"].strip("/").split("/")[-1].replace("-", " ")
    ).strip()


def meta_for(page: dict) -> str:
    override = PAGE_OVERRIDES.get(page["path"], {})

    supplied = (
        override.get("description")
        or page.get("meta_description")
        or page.get("description")
        or page.get("meta")
    )

    if supplied:
        return supplied

    intent = intent_for(page)

    if page.get("type") == "guide":
        return (
            f"Learn how {intent} works, what businesses should decide before "
            f"rollout and which records still need human review."
        )

    return (
        f"Explore {intent} with Vanta Workforce, including worker actions, "
        f"manager review, attendance records and practical limitations."
    )


def context_for(page: dict) -> dict:
    cluster = page.get("cluster", "operations")

    if cluster not in CLUSTERS:
        cluster = "operations"

    return CLUSTERS[cluster]


def related_pages(page: dict) -> list[dict]:
    selected = []

    leader_path = page.get("cluster_leader")

    if leader_path and leader_path != page["path"]:
        leader = next(
            (
                other
                for other in pages
                if other["path"] == leader_path
            ),
            None,
        )

        if leader is not None:
            selected.append(leader)

    same_cluster = [
        other
        for other in pages
        if other["path"] != page["path"]
        and other.get("cluster") == page.get("cluster")
        and other not in selected
    ]

    same_cluster.sort(key=lambda item: item["path"])

    if same_cluster:
        related_start = stable_index(
            page["path"],
            "related",
            len(same_cluster),
        )
        same_cluster = (
            same_cluster[related_start:]
            + same_cluster[:related_start]
        )

    for other in same_cluster:
        if len(selected) == 4:
            break
        selected.append(other)

    if len(selected) < 4:
        for other in pages:
            if (
                other["path"] != page["path"]
                and other not in selected
            ):
                selected.append(other)

            if len(selected) == 4:
                break

    return selected[:4]


def faqs_for(page: dict, context: dict) -> list[tuple[str, str]]:
    intent = intent_for(page)
    override = PAGE_OVERRIDES.get(page["path"], {})

    if override.get("faqs"):
        return override["faqs"]

    if page.get("type") == "guide":
        return [
            (
                f"Does this guide guarantee that {intent} will always work?",
                (
                    "No. Device conditions, connectivity, permissions and "
                    "human error can affect the available record."
                ),
            ),
            (
                "Should workers be told how the process works?",
                (
                    "Yes. Businesses should explain what is recorded, why it "
                    "is needed and how genuine exceptions are handled."
                ),
            ),
            (
                "Can the resulting record be used without review?",
                context["limit"],
            ),
        ]

    return [
        (
            f"What does Vanta Workforce record for {intent}?",
            (
                f"The relevant view can include {context['focus']}, depending "
                "on the worker action, device conditions and organisation setup."
            ),
        ),
        (
            "Can workers and managers review the same information?",
            (
                "Access depends on the user’s authorised role. Workers and "
                "managers may see different views of the relevant records."
            ),
        ),
        (
            "Does the record still need checking?",
            context["limit"],
        ),
    ]


def schema_for(
    page: dict,
    page_title: str,
    description: str,
    faqs: list[tuple[str, str]],
) -> str:
    items = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": "Vanta Workforce",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Android, iOS",
            "description": description,
            "url": canonical(page["path"]),
            "image": f"{BASE_URL}/vanta-workforce.png",
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
                    "name": "Vanta Workforce",
                    "item": f"{BASE_URL}/workforce/",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page_title,
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

    if page.get("type") == "guide":
        items.append(
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": page_title,
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
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{BASE_URL}/vanta-workforce.png",
                    },
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
        related_title = h1_for(related)
        related_context = context_for(related)

        cards.append(
            f"""
<a class="card" href="{esc(related['path'])}">
<small>{esc(related_context['label'])}</small>
<strong>{esc(related_title)}</strong>
</a>""".strip()
        )

    return "\n".join(cards)


def render_page(page: dict) -> str:
    context = context_for(page)
    intent = intent_for(page)
    page_title = title_for(page)
    display_title = h1_for(page)
    description = meta_for(page)
    faqs = faqs_for(page, context)
    guide = page.get("type") == "guide"

    values = {
        **context,
        "intent": intent,
        "intent_title": sentence_case(intent),
    }

    opening = choose(
        OPENINGS,
        page["path"],
        "opening",
    ).format(**values)

    worker_copy = choose(
        WORKER_PARAGRAPHS,
        page["path"],
        "worker",
    ).format(**values)

    manager_copy = choose(
        MANAGER_PARAGRAPHS,
        page["path"],
        "manager",
    ).format(**values)

    process_copy = choose(
        PROCESS_PARAGRAPHS,
        page["path"],
        "process",
    ).format(**values)

    if guide:
        section_heading = choose(
            GUIDE_HEADINGS,
            page["path"],
            "guide-heading",
        )
        eyebrow = "Workforce guide"
    else:
        section_heading = choose(
            HEADINGS,
            page["path"],
            "heading",
        )
        eyebrow = context["label"]

    override = PAGE_OVERRIDES.get(page["path"], {})

    if override:
        opening = override.get("opening", opening)
        worker_copy = override.get("worker", worker_copy)
        manager_copy = override.get("manager", manager_copy)
        process_copy = override.get("process", process_copy)
        section_heading = override.get("heading", section_heading)

    notice_copy = override.get("notice", context["limit"])

    faq_html = "\n".join(
        f"""<details>
<summary>{esc(question)}</summary>
<p>{esc(answer)}</p>
</details>"""
        for question, answer in faqs
    )

    body_class = "workforce-detail workforce-guide" if guide else "workforce-detail"

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<link href="/assets/favicon/favicon.ico" rel="icon" sizes="any"/>
<link href="/assets/favicon/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/assets/favicon/favicon-16x16.png" rel="icon" sizes="16x16" type="image/png"/>
<link href="/assets/favicon/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/assets/favicon/site.webmanifest" rel="manifest"/>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{esc(page_title)}</title>
<meta content="{esc(description)}" name="description"/>
<link href="{esc(canonical(page['path']))}" rel="canonical"/>
<meta content="index,follow,max-image-preview:large" name="robots"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Vanta Labs"/>
<meta property="og:title" content="{esc(display_title)}"/>
<meta property="og:description" content="{esc(description)}"/>
<meta property="og:url" content="{esc(canonical(page['path']))}"/>
<meta property="og:image" content="{BASE_URL}/vanta-workforce.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<link href="/workforce/assets/workforce-icon.png" rel="icon"/>
<link href="/workforce/assets/workforce.css" rel="stylesheet"/>
<script defer src="/workforce/assets/app-links.js"></script>
<script type="application/ld+json">{schema_for(page, display_title, description, faqs)}</script>
</head>

<body class="{body_class}">
<header class="head">
<nav>
<a class="brand" href="/">Vanta Labs</a>
<div class="links">
<a href="/workforce/">Vanta Workforce</a>
<a href="/workforce/staff-attendance-app/">Attendance</a>
<a href="/workforce/employee-timesheet-app/">Timesheets</a>
<a href="/workforce/guides/how-staff-attendance-apps-work/">Guides</a>
</div>
</nav>
</header>

<main>
<div class="hero">
<div>
<span class="eyebrow">{esc(eyebrow)}</span>
<h1>{esc(display_title)}</h1>
<p class="lead">{esc(description)}</p>
<div class="ctas">
<a class="btn" data-store="android">Google Play — coming soon</a>
<a class="btn" data-store="ios">App Store — coming soon</a>
</div>
</div>

<div class="iconbox">
<img
  alt="Vanta Workforce app icon"
  height="512"
  src="/workforce/assets/workforce-icon.png"
  width="512"
/>
</div>
</div>

<article class="body">
<section class="long-copy">
<h2>{esc(section_heading)}</h2>
<div class="long-copy-text">
<p>{esc(opening)} {esc(worker_copy)}</p>
<p>{esc(manager_copy)} {esc(process_copy)}</p>
</div>
</section>

<div class="notice">
<strong>What to keep in mind</strong>
{esc(notice_copy)}
</div>

<div class="workforce-lower-grid">
<section class="related">
<h2>Keep exploring Vanta Workforce</h2>
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

for page in pages:
    target = web_path_to_file(page["path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        render_page(page),
        encoding="utf-8",
    )
    generated += 1


sitemap_urls = [
    f"{BASE_URL}/workforce/",
    *[
        canonical(page["path"])
        for page in sorted(
            pages,
            key=lambda item: item["path"],
        )
    ],
]

sitemap = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
]

for url in sitemap_urls:
    sitemap.extend(
        [
            "  <url>",
            f"    <loc>{html.escape(url)}</loc>",
            "  </url>",
        ]
    )

sitemap.append("</urlset>")

(WORKFORCE / "sitemap.xml").write_text(
    "\n".join(sitemap) + "\n",
    encoding="utf-8",
)

# Keep the main Vanta Labs sitemap in sync with the Workforce plan.
root_sitemap = ROOT / "sitemap.xml"
root_sitemap_added = 0

if root_sitemap.is_file():
    root_text = root_sitemap.read_text(encoding="utf-8")

    missing_urls = [
        url for url in sitemap_urls
        if f"<loc>{url}</loc>" not in root_text
    ]

    if missing_urls:
        if "</urlset>" not in root_text:
            raise SystemExit("Root sitemap is missing </urlset>.")

        blocks = []
        for url in missing_urls:
            blocks.extend([
                "  <url>",
                f"    <loc>{html.escape(url)}</loc>",
                "  </url>",
            ])

        root_text = root_text.replace(
            "</urlset>",
            "\n".join(blocks) + "\n</urlset>",
            1,
        )

        root_sitemap.write_text(root_text, encoding="utf-8")
        root_sitemap_added = len(missing_urls)

manifest = {
    "generated_pages": generated,
    "total_html_pages": len(list(WORKFORCE.rglob("index.html"))),
    "sitemap_urls": len(sitemap_urls),
    "design_system": "Vanta Labs / Guardian editorial",
    "store_links_enabled": False,
    "root_homepage_modified": False,
    "root_sitemap_modified": bool(root_sitemap_added),
    "root_sitemap_urls_added": root_sitemap_added,
    "guardian_modified": False,
}

(WORKFORCE / "build-manifest.json").write_text(
    json.dumps(
        manifest,
        indent=2,
        ensure_ascii=False,
    ) + "\n",
    encoding="utf-8",
)

print(f"Generated supporting pages: {generated}")
print(f"Total HTML pages: {manifest['total_html_pages']}")
print(f"Workforce sitemap URLs: {manifest['sitemap_urls']}")
print("Design: Vanta Labs / Guardian editorial")
print("Store links enabled: no")
print("Root homepage modified: no")
print("Root sitemap modified: no")
print("Guardian modified: no")
