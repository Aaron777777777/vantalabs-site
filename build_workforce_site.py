#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path.cwd()
PLAN_FILE = ROOT / "workforce_page_plan.json"
OUTPUT = ROOT / "workforce"
ASSETS = OUTPUT / "assets"
BASE_URL = "https://vantalabs.co.uk"
PRODUCT = "Vanta Workforce"
ICON_SOURCE = ROOT / "vanta-workforce.png"

if not PLAN_FILE.exists():
    raise SystemExit("Missing workforce_page_plan.json")

if not ICON_SOURCE.exists():
    raise SystemExit("Missing vanta-workforce.png")

if OUTPUT.exists():
    raise SystemExit(
        "Refusing to overwrite existing workforce directory. "
        "Inspect or remove it manually first."
    )

plan = json.loads(PLAN_FILE.read_text(encoding="utf-8"))
pages = plan["pages"]
page_by_path = {page["path"]: page for page in pages}

cluster_descriptions = {
    "attendance": {
        "eyebrow": "Staff attendance",
        "summary": (
            "Keep a clear record of who has booked on, who has booked off and "
            "how attendance develops across the working month."
        ),
        "benefits": [
            "Give workers a straightforward mobile attendance flow.",
            "Keep attendance records available to the appropriate manager.",
            "Review individual hours without relying on paper registers.",
        ],
        "limitations": (
            "Attendance records still depend on workers using the app correctly, "
            "having a working device and following the organisation’s process."
        ),
    },
    "clocking": {
        "eyebrow": "Clocking in and out",
        "summary": (
            "Replace handwritten clock sheets with a mobile booking-on and "
            "booking-off process designed around real workplace routines."
        ),
        "benefits": [
            "Record the beginning and end of a worker’s attendance.",
            "Reduce the need to reconstruct hours from messages or memory.",
            "Give managers a clearer view of current worker status.",
        ],
        "limitations": (
            "A mobile clock-in record is evidence within an attendance process, "
            "not an automatic guarantee that every working circumstance has been captured."
        ),
    },
    "gps-attendance": {
        "eyebrow": "Location-aware attendance",
        "summary": (
            "Use device location as useful context when workers book on or off "
            "at a workplace or managed site."
        ),
        "benefits": [
            "Add workplace context to mobile attendance records.",
            "Support teams that operate across more than one location.",
            "Help managers investigate attendance records that need clarification.",
        ],
        "limitations": (
            "GPS and mobile location can be affected by buildings, signal, device "
            "settings, permissions, battery restrictions and operating-system behaviour."
        ),
    },
    "timesheets": {
        "eyebrow": "Timesheets and hours",
        "summary": (
            "Turn attendance activity into readable working-hour records, monthly "
            "periods and exportable timesheet information."
        ),
        "benefits": [
            "Let workers review their own recorded hours.",
            "Keep attendance organised into monthly periods.",
            "Split overnight records correctly when they cross a monthly midnight boundary.",
        ],
        "limitations": (
            "Vanta Workforce provides attendance and timesheet records; it does not "
            "promise automatic payroll processing or replace professional payroll review."
        ),
    },
    "workplace-presence": {
        "eyebrow": "Workplace presence",
        "summary": (
            "See which workers are currently recorded as present and review site "
            "attendance without chasing multiple separate updates."
        ),
        "benefits": [
            "Review current booking status across a workplace.",
            "Support attendance oversight across managed sites.",
            "Keep historic presence information connected to worker records.",
        ],
        "limitations": (
            "Live status reflects the information received by the service and may be "
            "delayed by connectivity, permissions or a worker’s device state."
        ),
    },
    "mobile-workforces": {
        "eyebrow": "Mobile workforces",
        "summary": (
            "Support teams whose working day happens across sites, customer locations "
            "or changing field environments rather than one fixed desk."
        ),
        "benefits": [
            "Give field workers a consistent mobile attendance process.",
            "Keep distributed attendance records in one system.",
            "Help managers understand which workers are active away from the main office.",
        ],
        "limitations": (
            "Remote and field attendance still requires suitable connectivity, device "
            "permissions and a clear organisational booking process."
        ),
    },
    "worker-safety": {
        "eyebrow": "Worker safety checks",
        "summary": (
            "Combine scheduled prompts, phone checks and incident reporting with the "
            "same system used for attendance and workplace presence."
        ),
        "benefits": [
            "Schedule checks and prompts for relevant workers.",
            "Support manager follow-up when a check needs attention.",
            "Provide an in-app route for workplace incident reporting.",
        ],
        "limitations": (
            "Vanta Workforce is not an emergency service and cannot guarantee worker "
            "safety. Immediate danger should always be handled through the appropriate "
            "emergency and workplace procedures."
        ),
    },
    "control-centre": {
        "eyebrow": "Control Centre oversight",
        "summary": (
            "Give authorised managers a clearer operational view of worker status, "
            "scheduled checks and attendance activity."
        ),
        "benefits": [
            "Review live worker status from the Control Centre.",
            "Carry out relevant worker phone and safety checks.",
            "Keep operational oversight connected to attendance records.",
        ],
        "limitations": (
            "Control Centre information depends on data reaching the service and should "
            "be interpreted alongside the organisation’s own management procedures."
        ),
    },
    "reporting": {
        "eyebrow": "Reports and exports",
        "summary": (
            "Review attendance history, monthly records and timesheet exports without "
            "rebuilding staff hours from scattered notes."
        ),
        "benefits": [
            "Review attendance records by worker and period.",
            "Export timesheet information for further business use.",
            "Keep cross-month and overnight attendance correctly allocated.",
        ],
        "limitations": (
            "Exports should be checked before being used for payroll, accounting, legal "
            "or employment decisions."
        ),
    },
    "operations": {
        "eyebrow": "Workplace operations",
        "summary": (
            "Bring manager and worker roles, workplace records, attendance and safety "
            "flows together in one mobile workforce platform."
        ),
        "benefits": [
            "Manage workplaces and relevant worker access.",
            "Use separate manager and worker experiences.",
            "Access Vanta Workforce on supported Android and iOS devices.",
        ],
        "limitations": (
            "Availability and behaviour can vary by device, operating system, permissions, "
            "connectivity and subscription status."
        ),
    },
}

intent_openers = {
    "staff attendance software": "A practical staff attendance system should make the everyday record clearer, not add another layer of admin.",
    "employee attendance app": "Employee attendance is easiest to review when each worker follows the same clear booking process.",
    "workforce attendance system": "A workforce attendance system gives managers one consistent place to review working activity.",
    "mobile staff attendance": "Mobile attendance is useful when staff do not begin every shift beside a shared clocking terminal.",
    "digital attendance register": "A digital attendance register replaces loose sheets with structured worker records.",
    "attendance management": "Attendance management works best when current status and historic hours are connected.",
    "staff attendance tracking": "Staff attendance tracking should show useful records without pretending that technology removes the need for management.",
    "employee attendance records": "Employee attendance records provide a clearer history of when workers booked on and off.",
    "employee clock-in app": "An employee clock-in app gives workers a direct way to record the beginning of attendance.",
    "staff clock-in app": "A staff clock-in app can simplify the first and last action of a working period.",
    "clock in and out": "Clocking in and out creates the basic record from which working hours can be reviewed.",
    "mobile time clock": "A mobile time clock moves attendance recording onto the worker’s supported phone.",
    "digital clock-in": "Digital clock-in records are easier to organise than handwritten entries spread across multiple sites.",
    "workplace clock-in": "Workplace clock-in connects a worker’s booking action with the site where work is taking place.",
    "worker booking on": "Booking on records that a worker has begun the relevant attendance period.",
    "worker booking off": "Booking off closes the attendance period so that hours can be calculated and reviewed.",
    "GPS clock-in app": "GPS-assisted clock-in can add location context to a worker’s booking action.",
    "location-based clock-in": "Location-based clock-in helps show whether a booking action occurred near the expected workplace.",
    "geofenced time clock": "A geofenced time-clock approach uses a defined workplace area as attendance context.",
    "worksite clock-in": "Worksite clock-in is designed for staff who report to a managed location rather than a central office.",
    "location-aware attendance": "Location-aware attendance combines a booking action with available device-location context.",
    "GPS attendance system": "A GPS attendance system can help managers review where a mobile booking action was recorded.",
    "employee location clock-in": "Employee location clock-in uses the worker’s device to provide useful workplace context.",
    "site-based clock-in": "Site-based clock-in supports organisations that need attendance records connected to specific workplaces.",
    "employee timesheet app": "An employee timesheet app turns booking activity into hours a worker and manager can review.",
    "staff timesheet app": "A staff timesheet app keeps working-hour records close to the attendance process that created them.",
    "mobile timesheets": "Mobile timesheets let workers review their recorded hours without waiting for a paper summary.",
    "digital timesheet system": "A digital timesheet system organises working records into consistent periods.",
    "working hours tracking": "Working-hours tracking begins with reliable booking-on and booking-off records.",
    "employee hours tracking": "Employee-hours tracking helps managers and workers see how recorded attendance becomes time worked.",
    "monthly timesheets": "Monthly timesheets keep records aligned to a defined attendance period.",
    "overnight shift timesheets": "Overnight shifts need careful handling when one attendance record runs across midnight.",
    "workplace presence": "Workplace presence is easier to understand when current bookings and historic attendance use the same records.",
    "employee presence": "Employee presence tracking gives authorised managers a current operational view.",
    "site attendance": "Site attendance connects worker records to the workplace where activity is expected.",
    "multi-site attendance": "Multi-site attendance needs a consistent process across different managed locations.",
    "construction attendance": "Construction-site attendance often involves mobile workers, changing teams and site-based records.",
    "workplace attendance register": "A workplace attendance register provides a structured view of who has attended and when.",
    "staff on-site status": "Staff on-site status helps answer the immediate question of who is currently booked on.",
    "who is working": "Knowing who is working should not require checking multiple messages, sheets or group chats.",
    "field worker attendance": "Field-worker attendance needs to work away from a shared office terminal.",
    "mobile workforce management": "Mobile workforce management brings attendance, presence and relevant safety activity into one app.",
    "remote worker check-in": "Remote worker check-in gives distributed staff a consistent attendance action.",
    "mobile worker clock-in": "Mobile workers can record attendance from supported devices while working across locations.",
    "field team timesheets": "Field-team timesheets should reflect the attendance activity recorded throughout the month.",
    "distributed workforce attendance": "Distributed workforce attendance needs a process that works across different sites and teams.",
    "off-site worker attendance": "Off-site attendance records help managers review workers operating away from the main workplace.",
    "field staff hours": "Field-staff hours become easier to review when attendance records are captured consistently.",
    "worker safety checks": "Worker safety checks are most useful when prompts, status and follow-up are visible to authorised managers.",
    "lone worker check-in": "A lone-worker check-in provides a scheduled point of contact but is not a guarantee of safety.",
    "scheduled worker checks": "Scheduled worker checks help organisations create a repeatable welfare process.",
    "staff welfare checks": "Staff welfare checks provide managers with a structured prompt and response flow.",
    "workplace incident reporting": "Workplace incident reporting gives workers and managers a consistent route for recording relevant events.",
    "employee incident reporting": "Employee incident reports are more useful when they remain connected to the workplace system.",
    "worker phone checks": "Worker phone checks support manager follow-up when contact or status needs to be confirmed.",
    "scheduled safety prompts": "Scheduled safety prompts remind workers to complete relevant checks at expected times.",
    "workforce control centre": "A workforce Control Centre brings current status and management checks into one operational view.",
    "live workforce status": "Live workforce status helps managers see which workers are currently recorded as active.",
    "manager attendance dashboard": "A manager attendance dashboard turns individual booking records into an overview.",
    "workforce oversight": "Workforce oversight is clearer when attendance, sites and safety checks are not split between systems.",
    "manager worker status": "Manager worker-status tools help authorised users review current operational activity.",
    "staff status dashboard": "A staff-status dashboard provides a quick view of workers who are booked on or need attention.",
    "workplace control centre": "A workplace Control Centre supports day-to-day operational monitoring.",
    "multi-site workforce dashboard": "A multi-site dashboard helps managers review activity across more than one workplace.",
    "attendance reporting": "Attendance reporting turns booking records into information that can be checked and exported.",
    "timesheet export": "Timesheet export makes recorded hours available for further authorised business use.",
    "staff hours reporting": "Staff-hours reporting helps businesses review recorded time by worker and period.",
    "employee attendance reports": "Employee attendance reports provide a structured history rather than a collection of informal updates.",
    "monthly attendance reports": "Monthly attendance reports organise worker records into a consistent reporting period.",
    "workforce hours export": "A workforce-hours export provides a portable record for further review.",
    "cross-month timesheets": "Cross-month timesheets require records to be allocated correctly when midnight begins a new month.",
    "attendance history": "Attendance history helps managers and workers review earlier booking activity.",
    "workforce management": "Workforce management becomes simpler when attendance, presence, hours and safety share one system.",
    "site management": "Site management connects workplaces with the workers and attendance activity associated with them.",
    "workplace management": "Workplace management requires a clear view of sites, roles and current worker activity.",
    "manager and worker roles": "Separate manager and worker roles help keep operational actions appropriate to each user.",
    "business attendance": "A business attendance app should support real staff processes rather than behave like a personal stopwatch.",
    "staff operations": "Staff operations benefit from one clear view of attendance, presence and relevant checks.",
    "workforce records": "Workforce records are easier to review when attendance and timesheets follow the same structure.",
    "Android and iOS workforce app": "Vanta Workforce is designed for supported Android and iOS devices used by managers and workers.",
}

guide_content = {
    "how-staff-attendance-apps-work": (
        "Staff attendance apps replace or support manual registers by recording when a worker books on and off. "
        "The resulting entries can then be reviewed as attendance history and working hours."
    ),
    "choosing-a-staff-attendance-system": (
        "Choosing an attendance system starts with the working environment: fixed site, multiple workplaces, field teams or a mixture. "
        "Businesses should also consider worker usability, manager oversight, location privacy and reporting needs."
    ),
    "attendance-app-vs-paper-register": (
        "Paper registers are familiar, but they can be difficult to read, search and consolidate. "
        "A mobile attendance app provides structured records while still requiring a sensible internal process."
    ),
    "how-to-introduce-digital-attendance": (
        "A digital-attendance rollout should explain why the process is changing, what workers must do, how location is used and who can review the records."
    ),
    "how-mobile-clock-in-works": (
        "Mobile clock-in allows a worker to record attendance using a supported phone. "
        "The app creates a booking record that can later contribute to hours and timesheets."
    ),
    "how-to-improve-clock-in-accuracy": (
        "Clear workplace instructions, correct device time, reliable permissions and prompt booking actions all help improve attendance-record quality."
    ),
    "how-gps-clock-in-works": (
        "GPS clock-in uses available device location as context around a booking action. "
        "It should be treated as useful supporting information rather than infallible proof."
    ),
    "employee-location-privacy": (
        "Location-aware attendance should be explained openly to workers, limited to legitimate business use and reviewed alongside applicable privacy obligations."
    ),
    "what-to-do-when-clock-in-location-fails": (
        "When location is unavailable, check permissions, signal, device settings and battery restrictions before assuming the worker is at fault."
    ),
    "how-to-improve-timesheet-accuracy": (
        "Timesheet accuracy improves when workers book on and off promptly, managers review exceptions and overnight records are handled consistently."
    ),
    "how-to-track-working-hours": (
        "Working hours are calculated from the attendance periods recorded for each worker. "
        "Managers should still review unusual or incomplete entries."
    ),
    "how-overnight-shifts-affect-timesheets": (
        "An overnight attendance period can span two calendar dates and, at month end, two monthly reporting periods."
    ),
    "how-monthly-attendance-periods-work": (
        "Monthly attendance periods group worker records by calendar month so that current and previous hours remain easier to review."
    ),
    "how-to-manage-mobile-workers": (
        "Mobile workers need clear booking expectations, suitable devices, defined workplaces and a practical process for handling poor connectivity."
    ),
    "how-worker-safety-checks-work": (
        "Worker safety checks use scheduled prompts or manager actions to create a repeatable welfare process. "
        "They do not replace emergency procedures."
    ),
    "how-scheduled-worker-prompts-work": (
        "Scheduled prompts create expected check points during a working period. "
        "Organisations should decide who responds when a check is missed."
    ),
    "how-to-report-a-workplace-incident": (
        "A useful incident report records what happened, when it happened and any relevant supporting information, including photos where appropriate."
    ),
    "how-managers-monitor-workforce-status": (
        "Managers can use current booking status, attendance records and scheduled checks to build an operational picture of the workforce."
    ),
    "how-to-export-timesheet-records": (
        "Timesheet exports provide attendance information outside the app for authorised review. "
        "Exported records should be checked before further business use."
    ),
    "troubleshooting-mobile-attendance": (
        "Mobile attendance issues commonly involve connectivity, permissions, account access, device settings or incomplete booking actions."
    ),
}

def esc(value: str) -> str:
    return html.escape(value, quote=True)

def absolute(path: str) -> str:
    return urljoin(BASE_URL, path)

def slug_label(page: dict) -> str:
    return page["intent"].replace("-", " ").strip().title()

def related_pages(page: dict, limit: int = 3) -> list[dict]:
    same_cluster = [
        candidate
        for candidate in pages
        if candidate["cluster"] == page["cluster"]
        and candidate["path"] != page["path"]
        and candidate["type"] != "homepage"
    ]
    leaders_first = sorted(
        same_cluster,
        key=lambda item: (
            item["type"] != "cluster_leader",
            item["type"] == "guide",
            item["path"],
        ),
    )
    return leaders_first[:limit]

def visible_title(page: dict) -> str:
    if page["type"] == "guide":
        return page["title"].replace("Vanta Workforce Guide | ", "")
    return page["title"].replace("Vanta Workforce | ", "")

def meta_description(page: dict) -> str:
    if page["type"] == "homepage":
        return (
            "Vanta Workforce combines staff scheduling, rotas, attendance, timesheets, "
            "workplace visibility and worker safety in one workforce management app."
        )

    cluster = cluster_descriptions[page["cluster"]]
    if page["type"] == "guide":
        return (
            f"Learn {page['intent']} with practical guidance from Vanta Workforce, "
            f"including honest limitations and links to relevant {cluster['eyebrow'].lower()} tools."
        )

    return (
        f"Use Vanta Workforce for {page['intent']}, with mobile attendance records, "
        f"manager oversight and clear {cluster['eyebrow'].lower()} information for businesses."
    )

def faq_items(page: dict) -> list[tuple[str, str]]:
    cluster = page["cluster"]

    common = [
        (
            f"Is Vanta Workforce suitable for {page['intent']}?",
            (
                f"Vanta Workforce includes tools relevant to {page['intent']}, including "
                "worker booking activity, attendance records and authorised manager oversight. "
                "Suitability depends on the organisation’s exact process and device requirements."
            ),
        ),
        (
            "Does Vanta Workforce guarantee GPS or live-status accuracy?",
            (
                "No. Location and status can be affected by connectivity, buildings, permissions, "
                "battery settings, device behaviour and delayed data."
            ),
        ),
    ]

    third = {
        "attendance": (
            "Can workers review their own recorded hours?",
            "Yes. The My Hours area is designed to let workers review their recorded attendance and hours.",
        ),
        "clocking": (
            "What happens if someone forgets to book off?",
            "The resulting attendance record may need manager review or correction under the organisation’s process.",
        ),
        "gps-attendance": (
            "Is location used as perfect proof of attendance?",
            "No. Location is supporting context and should be reviewed alongside the booking record and workplace circumstances.",
        ),
        "timesheets": (
            "How are overnight records handled at month end?",
            "Attendance that crosses the monthly midnight boundary is split so the relevant time is allocated to each month.",
        ),
        "workplace-presence": (
            "Does current status always update instantly?",
            "Not necessarily. Connectivity and device conditions can delay the information received by the service.",
        ),
        "mobile-workforces": (
            "Can workers use the app across different sites?",
            "The product includes workplace and site-management functionality intended to support mobile and multi-site teams.",
        ),
        "worker-safety": (
            "Is Vanta Workforce an emergency service?",
            "No. It supports workplace checks and reporting but does not replace emergency services or established safety procedures.",
        ),
        "control-centre": (
            "Who should use the Control Centre?",
            "The Control Centre is intended for authorised managers responsible for relevant workforce oversight and checks.",
        ),
        "reporting": (
            "Can exported records be sent directly to payroll?",
            "Exports can support further business review, but Vanta Workforce does not promise automatic payroll processing or payroll integration.",
        ),
        "operations": (
            "Is Vanta Workforce available for Android and iOS?",
            "The product has Android and iOS apps, although availability can depend on the current store release and supported device.",
        ),
    }[cluster]

    return common + [third]

def schema_json(page: dict, faqs: list[tuple[str, str]]) -> str:
    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": PRODUCT,
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Android, iOS",
            "description": meta_description(page),
            "url": absolute(page["path"]),
            "image": absolute("/vanta-workforce.png"),
            "author": {
                "@type": "Organization",
                "name": "Vanta Labs",
                "url": BASE_URL,
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
                    "item": absolute("/"),
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": PRODUCT,
                    "item": absolute("/workforce/"),
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": visible_title(page),
                    "item": absolute(page["path"]),
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
    return json.dumps(schemas, ensure_ascii=False)

def head(page: dict) -> str:
    description = meta_description(page)
    return f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(page['title'])}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(absolute(page['path']))}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Vanta Labs">
  <meta property="og:title" content="{esc(page['title'])}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(absolute(page['path']))}">
  <meta property="og:image" content="{esc(absolute('/vanta-workforce.png'))}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/workforce/assets/workforce-icon.png">
  <link rel="stylesheet" href="/workforce/assets/workforce.css">
  <script defer src="/workforce/assets/app-links.js"></script>
"""

def nav() -> str:
    return """<header class="site-header">
  <nav class="nav-shell" aria-label="Primary navigation">
    <a class="brand" href="/">Vanta Labs</a>
    <div class="nav-links">
      <a href="/workforce/">Vanta Workforce</a>
      <a href="/workforce/staff-attendance-app/">Attendance</a>
      <a href="/workforce/employee-timesheet-app/">Timesheets</a>
      <a href="/workforce/worker-safety-check-app/">Worker safety</a>
      <a href="/">All apps</a>
    </div>
  </nav>
</header>
"""

def store_buttons() -> str:
    return """<div class="store-actions" aria-label="App store links">
  <a class="store-button disabled" data-store="android" aria-disabled="true">Google Play — coming soon</a>
  <a class="store-button secondary disabled" data-store="ios" aria-disabled="true">App Store — coming soon</a>
</div>"""

def footer() -> str:
    return """<footer class="site-footer">
  <div>
    <strong>Vanta Workforce</strong>
    <p>Staff scheduling, rotas, attendance, timesheets and worker safety in one workforce management app.</p>
  </div>
  <div class="footer-links">
    <a href="/workforce/">Workforce home</a>
    <a href="/privacy.html">Privacy</a>
    <a href="/terms.html">Terms</a>
    <a href="/">Vanta Labs</a>
  </div>
</footer>
"""

def homepage_html(page: dict) -> str:
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": PRODUCT,
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Android, iOS",
            "description": meta_description(page),
            "url": absolute("/workforce/"),
            "image": absolute("/vanta-workforce.png"),
            "author": {
                "@type": "Organization",
                "name": "Vanta Labs",
                "url": BASE_URL,
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Vanta Labs",
            "url": BASE_URL,
        },
    ]

    cluster_cards = []
    for cluster in plan["clusters"]:
        leader = page_by_path[cluster["leader"]]
        cluster_cards.append(
            f"""<a class="topic-card" href="{esc(cluster['leader'])}">
  <span>{esc(cluster_descriptions[leader['cluster']]['eyebrow'])}</span>
  <h2>{esc(cluster['name'])}</h2>
  <p>{esc(cluster_descriptions[leader['cluster']]['summary'])}</p>
</a>"""
        )

    return (
        head(page)
        + f"""  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace("</", "<\\/")}</script>
</head>
<body>
{nav()}
<main>
  <section class="hero home-hero">
    <div class="hero-copy">
      <p class="eyebrow">Workforce management for teams</p>
      <h1>Plan shifts.<br>Know who is working.</h1>
      <p class="lead">
        Vanta Workforce brings staff scheduling, rotas, attendance, workplace presence,
         timesheets, scheduled checks and manager oversight into one workforce management platform.
      </p>
      {store_buttons()}
      <p class="store-note">Store links are held centrally and will remain disabled until confirmed.</p>
    </div>
    <div class="hero-visual">
      <img src="/workforce/assets/workforce-icon.png"
           alt="Vanta Workforce app icon"
           width="1254"
           height="1254">
      <div class="status-panel">
        <span class="status-dot"></span>
        <div>
          <strong>Workforce visibility</strong>
          <small>Shifts, attendance, hours, sites and checks</small>
        </div>
      </div>
    </div>
  </section>

  <section class="intro-grid">
    <article>
      <p class="section-label">One connected system</p>
      <h2>Plan shifts, then keep attendance connected</h2>
      <p>
        Managers can schedule shifts and assign staff, while workers can see their assigned work
         and use the same app for attendance. Booking records then feed My Hours,
         monthly attendance periods and timesheet information that managers can review.
      </p>
    </article>
    <article>
      <p class="section-label">Built for operations</p>
      <h2>Current worker status without chasing updates</h2>
      <p>
        Authorised managers can use Control Centre oversight, workplace records,
        worker phone checks and scheduled prompts to understand current activity.
      </p>
    </article>
    <article>
      <p class="section-label">Honest location context</p>
      <h2>Useful GPS information, without impossible promises</h2>
      <p>
        Device location can support workplace attendance, but signal, buildings,
        permissions and battery settings can affect what is available.
      </p>
    </article>
  </section>

  <section class="topic-section">
    <div class="section-heading">
      <p class="section-label">Explore Vanta Workforce</p>
      <h2>Tools for day-to-day workforce management</h2>
      <p>Choose the area that best matches how your organisation works.</p>
    </div>
    <div class="topic-grid">
      {''.join(cluster_cards)}
    </div>
  </section>

  <section class="split-panel">
    <div>
      <p class="section-label">Working-hour detail</p>
      <h2>Monthly periods and overnight shifts handled carefully</h2>
      <p>
        Attendance records that cross midnight at the end of a month are split
        correctly so that each part is allocated to the relevant monthly period.
      </p>
      <a class="text-link" href="/workforce/overnight-shift-timesheets/">Explore overnight timesheets</a>
    </div>
    <div>
      <p class="section-label">Worker safety</p>
      <h2>Scheduled checks beside attendance and presence</h2>
      <p>
        Worker checks, prompts and incident-reporting flows sit within the same
        operational environment used by managers and workers.
      </p>
      <a class="text-link" href="/workforce/worker-safety-check-app/">Explore worker safety checks</a>
    </div>
  </section>

  <section class="final-cta">
    <img src="/workforce/assets/workforce-icon.png" alt="" width="96" height="96">
    <div>
      <p class="section-label">Vanta Workforce</p>
      <h2>Staff scheduling, attendance, timesheets and worker safety in one app.</h2>
      {store_buttons()}
    </div>
  </section>
</main>
{footer()}
</body>
</html>
"""
    )

def detail_html(page: dict) -> str:
    cluster = cluster_descriptions[page["cluster"]]
    faqs = faq_items(page)
    title = visible_title(page)
    leader = page_by_path[page["cluster_leader"]]
    related = related_pages(page)

    if page["type"] == "guide":
        body_intro = guide_content[page["slug"].split("/", 1)[1]]
        purpose_heading = f"What to understand about {page['intent']}"
        purpose_text = (
            f"{body_intro} Vanta Workforce supports this process through its "
            f"{cluster['eyebrow'].lower()} functionality, while leaving policy and "
            "management decisions with the organisation."
        )
    else:
        opener = intent_openers.get(
            page["intent"],
            f"{title} is designed around a clear and practical workforce process.",
        )
        body_intro = (
            f"{opener} Vanta Workforce connects this area with attendance records, "
            "working hours and authorised manager oversight."
        )
        purpose_heading = f"A clearer approach to {page['intent']}"
        purpose_text = (
            f"For businesses using {page['intent']}, the useful outcome is not simply "
            "another digital button. It is a consistent record that can be reviewed "
            "alongside worker status, hours and the relevant workplace."
        )

    benefits = "".join(f"<li>{esc(item)}</li>" for item in cluster["benefits"])
    faq_html = "".join(
        f"""<details>
  <summary>{esc(question)}</summary>
  <p>{esc(answer)}</p>
</details>"""
        for question, answer in faqs
    )
    related_html = "".join(
        f"""<a class="related-card" href="{esc(item['path'])}">
  <span>{esc(item['cluster_name'])}</span>
  <strong>{esc(visible_title(item))}</strong>
  <p>{esc(meta_description(item))}</p>
</a>"""
        for item in related
    )

    breadcrumb_middle = ""
    if page["type"] == "guide":
        breadcrumb_middle = '<span aria-hidden="true">/</span><span>Guides</span>'

    cluster_link_text = (
        f"Explore the {leader['cluster_name'].lower()} cluster"
        if page["path"] != page["cluster_leader"]
        else "This is the main cluster page"
    )

    return (
        head(page)
        + f"""  <script type="application/ld+json">{schema_json(page, faqs).replace("</", "<\\/")}</script>
</head>
<body>
{nav()}
<main>
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <a href="/">Vanta Labs</a>
    <span aria-hidden="true">/</span>
    <a href="/workforce/">Vanta Workforce</a>
    {breadcrumb_middle}
    <span aria-hidden="true">/</span>
    <span>{esc(title)}</span>
  </nav>

  <section class="hero detail-hero">
    <div class="hero-copy">
      <p class="eyebrow">{esc(cluster['eyebrow'])}</p>
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(meta_description(page))}</p>
      {store_buttons()}
    </div>
    <div class="hero-visual compact">
      <img src="/workforce/assets/workforce-icon.png"
           alt="Vanta Workforce app icon"
           width="1254"
           height="1254">
    </div>
  </section>

  <article class="content-shell">
    <section class="content-section">
      <p class="section-label">{esc(page['cluster_name'])}</p>
      <h2>{esc(purpose_heading)}</h2>
      <p>{esc(body_intro)}</p>
      <p>{esc(purpose_text)}</p>
    </section>

    <section class="feature-panel">
      <div>
        <p class="section-label">What Vanta Workforce supports</p>
        <h2>Connected records rather than isolated entries</h2>
        <ul>{benefits}</ul>
      </div>
      <aside>
        <strong>Important limitation</strong>
        <p>{esc(cluster['limitations'])}</p>
      </aside>
    </section>

    <section class="content-section">
      <p class="section-label">How it fits together</p>
      <h2>From worker action to manager review</h2>
      <p>
        Workers use the supported mobile app for relevant booking, attendance,
        safety or reporting actions. Information is stored through the
        Firebase-backed service and presented to the appropriate worker or manager role.
      </p>
      <p>
        The exact record available depends on the action completed, device conditions,
        permissions, connectivity and the organisation’s own configuration.
      </p>
    </section>

    <section class="cluster-callout">
      <div>
        <p class="section-label">Topic cluster</p>
        <h2>{esc(page['cluster_name'])}</h2>
        <p>{esc(cluster['summary'])}</p>
      </div>
      <a class="store-button secondary"
         href="{esc(page['cluster_leader'])}">
        {esc(cluster_link_text)}
      </a>
    </section>

    <section class="faq-section">
      <div class="section-heading">
        <p class="section-label">Frequently asked questions</p>
        <h2>Questions about {esc(page['intent'])}</h2>
      </div>
      <div class="faq-list">{faq_html}</div>
    </section>

    <section class="related-section">
      <div class="section-heading">
        <p class="section-label">Related Vanta Workforce pages</p>
        <h2>Continue exploring this topic</h2>
      </div>
      <div class="related-grid">{related_html}</div>
    </section>

    <section class="final-cta">
      <img src="/workforce/assets/workforce-icon.png" alt="" width="96" height="96">
      <div>
        <p class="section-label">Vanta Workforce</p>
        <h2>Know who is working. Keep every hour accounted for.</h2>
        <a class="text-link" href="/workforce/">Return to the Vanta Workforce homepage</a>
      </div>
    </section>
  </article>
</main>
{footer()}
</body>
</html>
"""
    )

CSS = r"""
:root {
  --bg: #071014;
  --bg-soft: #0b171c;
  --panel: #102127;
  --panel-2: #142b32;
  --line: rgba(178, 232, 222, 0.16);
  --text: #f2f7f6;
  --muted: #a9bab8;
  --accent: #66e0c2;
  --accent-soft: rgba(102, 224, 194, 0.12);
  --gold: #d6b56f;
  --max: 1180px;
  --radius: 24px;
}

* {
  box-sizing: border-box;
}

html {
  background: var(--bg);
  color-scheme: dark;
  scroll-behavior: smooth;
}

body {
  margin: 0;
  background:
    radial-gradient(circle at 80% 8%, rgba(50, 148, 132, 0.14), transparent 28rem),
    linear-gradient(180deg, #071014 0%, #081318 45%, #071014 100%);
  color: var(--text);
  font-family:
    Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  line-height: 1.65;
}

a {
  color: inherit;
}

img {
  display: block;
  max-width: 100%;
}

.site-header {
  border-bottom: 1px solid var(--line);
  background: rgba(7, 16, 20, 0.86);
  backdrop-filter: blur(18px);
  position: sticky;
  top: 0;
  z-index: 20;
}

.nav-shell {
  width: min(calc(100% - 40px), var(--max));
  min-height: 72px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}

.brand {
  font-weight: 800;
  letter-spacing: -0.03em;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
  font-size: 0.93rem;
}

.nav-links a,
.footer-links a {
  color: var(--muted);
  text-decoration: none;
}

.nav-links a:hover,
.footer-links a:hover,
.text-link:hover {
  color: var(--accent);
}

main {
  width: min(calc(100% - 40px), var(--max));
  margin: 0 auto;
}

.hero {
  min-height: 620px;
  padding: 90px 0 70px;
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
  align-items: center;
  gap: 70px;
}

.detail-hero {
  min-height: 500px;
  padding-top: 68px;
}

.eyebrow,
.section-label {
  margin: 0 0 14px;
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.13em;
  text-transform: uppercase;
}

h1,
h2,
h3,
p {
  margin-top: 0;
}

h1 {
  margin-bottom: 24px;
  font-size: clamp(3rem, 6vw, 5.8rem);
  line-height: 0.98;
  letter-spacing: -0.065em;
}

.detail-hero h1 {
  font-size: clamp(2.8rem, 5vw, 5rem);
}

h2 {
  font-size: clamp(1.8rem, 3.5vw, 3.15rem);
  line-height: 1.08;
  letter-spacing: -0.045em;
}

.lead {
  max-width: 760px;
  margin-bottom: 30px;
  color: #c6d4d2;
  font-size: clamp(1.08rem, 2vw, 1.35rem);
}

.store-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.store-button {
  min-height: 50px;
  padding: 13px 21px;
  border: 1px solid var(--accent);
  border-radius: 999px;
  background: var(--accent);
  color: #06231c;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  text-decoration: none;
}

.store-button.secondary {
  background: transparent;
  color: var(--accent);
}

.store-button.disabled {
  cursor: default;
  opacity: 0.62;
}

.store-note {
  margin-top: 14px;
  color: var(--muted);
  font-size: 0.84rem;
}

.hero-visual {
  position: relative;
  padding: 42px;
  border: 1px solid var(--line);
  border-radius: 40px;
  background:
    linear-gradient(145deg, rgba(102, 224, 194, 0.12), transparent 45%),
    var(--panel);
  box-shadow: 0 38px 90px rgba(0, 0, 0, 0.38);
}

.hero-visual.compact {
  max-width: 440px;
  justify-self: end;
}

.hero-visual img {
  width: 100%;
  border-radius: 25%;
}

.status-panel {
  position: absolute;
  right: -24px;
  bottom: 34px;
  min-width: 250px;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(7, 16, 20, 0.94);
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 20px 48px rgba(0, 0, 0, 0.35);
}

.status-panel small {
  display: block;
  color: var(--muted);
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 7px var(--accent-soft);
}

.intro-grid,
.topic-grid,
.related-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.intro-grid {
  padding: 0 0 100px;
}

.intro-grid article,
.topic-card,
.related-card {
  padding: 28px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(16, 33, 39, 0.76);
}

.intro-grid p,
.topic-card p,
.related-card p,
.content-section p,
.split-panel p,
.feature-panel p,
.cluster-callout p,
.site-footer p {
  color: var(--muted);
}

.topic-section,
.related-section,
.faq-section {
  padding: 90px 0;
  border-top: 1px solid var(--line);
}

.section-heading {
  max-width: 720px;
  margin-bottom: 38px;
}

.topic-card,
.related-card {
  text-decoration: none;
  transition: transform 160ms ease, border-color 160ms ease;
}

.topic-card:hover,
.related-card:hover {
  transform: translateY(-3px);
  border-color: rgba(102, 224, 194, 0.48);
}

.topic-card span,
.related-card span {
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.topic-card h2 {
  margin: 12px 0;
  font-size: 1.45rem;
}

.related-card strong {
  display: block;
  margin: 10px 0;
  font-size: 1.15rem;
}

.split-panel,
.feature-panel,
.cluster-callout {
  margin: 100px 0;
  padding: 34px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background:
    linear-gradient(145deg, rgba(102, 224, 194, 0.07), transparent 48%),
    var(--panel);
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 46px;
}

.text-link {
  color: var(--accent);
  font-weight: 800;
  text-decoration: none;
}

.final-cta {
  margin: 100px 0;
  padding: 34px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel-2);
  display: flex;
  align-items: center;
  gap: 28px;
}

.final-cta img {
  width: 96px;
  border-radius: 24px;
}

.final-cta h2 {
  margin-bottom: 20px;
  font-size: clamp(1.6rem, 3vw, 2.6rem);
}

.breadcrumbs {
  padding-top: 28px;
  display: flex;
  flex-wrap: wrap;
  gap: 9px;
  color: var(--muted);
  font-size: 0.86rem;
}

.breadcrumbs a {
  color: var(--muted);
  text-decoration: none;
}

.content-shell {
  max-width: 1040px;
  margin: 0 auto;
}

.content-section {
  max-width: 780px;
  padding: 70px 0;
}

.content-section p {
  font-size: 1.08rem;
}

.feature-panel ul {
  margin: 24px 0 0;
  padding-left: 20px;
}

.feature-panel li + li {
  margin-top: 12px;
}

.feature-panel aside {
  padding: 26px;
  border: 1px solid rgba(214, 181, 111, 0.24);
  border-radius: 18px;
  background: rgba(214, 181, 111, 0.07);
}

.feature-panel aside strong {
  color: var(--gold);
}

.cluster-callout {
  align-items: center;
}

.faq-list {
  display: grid;
  gap: 12px;
}

details {
  padding: 20px 22px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(16, 33, 39, 0.72);
}

summary {
  cursor: pointer;
  font-weight: 800;
}

details p {
  margin: 14px 0 0;
  color: var(--muted);
}

.site-footer {
  width: min(calc(100% - 40px), var(--max));
  margin: 0 auto;
  padding: 42px 0 60px;
  border-top: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  gap: 30px;
}

.site-footer p {
  max-width: 520px;
  margin: 8px 0 0;
}

.footer-links {
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
  justify-content: flex-end;
  gap: 18px;
}

@media (max-width: 900px) {
  .nav-shell {
    align-items: flex-start;
    padding: 18px 0;
  }

  .nav-links {
    max-width: 520px;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 10px 18px;
  }

  .hero {
    min-height: auto;
    padding: 64px 0;
    grid-template-columns: 1fr;
  }

  .hero-visual,
  .hero-visual.compact {
    width: min(100%, 520px);
    justify-self: start;
  }

  .status-panel {
    right: 18px;
  }

  .intro-grid,
  .topic-grid,
  .related-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .split-panel,
  .feature-panel,
  .cluster-callout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 620px) {
  main,
  .nav-shell,
  .site-footer {
    width: min(calc(100% - 28px), var(--max));
  }

  .site-header {
    position: static;
  }

  .nav-shell {
    display: block;
  }

  .nav-links {
    margin-top: 12px;
    justify-content: flex-start;
    font-size: 0.82rem;
  }

  h1 {
    font-size: clamp(2.65rem, 15vw, 4.4rem);
  }

  .intro-grid,
  .topic-grid,
  .related-grid {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    padding: 26px;
    border-radius: 28px;
  }

  .status-panel {
    position: static;
    min-width: 0;
    margin-top: 18px;
  }

  .store-actions {
    display: grid;
  }

  .store-button {
    width: 100%;
  }

  .split-panel,
  .feature-panel,
  .cluster-callout,
  .final-cta {
    margin: 70px 0;
    padding: 24px;
  }

  .final-cta {
    align-items: flex-start;
  }

  .site-footer {
    display: block;
  }

  .footer-links {
    margin-top: 24px;
    justify-content: flex-start;
  }
}
"""

APP_LINKS = r"""
(() => {
  const stores = {
    android: null,
    ios: null
  };

  document.querySelectorAll("[data-store]").forEach((element) => {
    const store = element.dataset.store;
    const url = stores[store];

    if (!url) {
      element.removeAttribute("href");
      element.setAttribute("aria-disabled", "true");
      element.classList.add("disabled");
      return;
    }

    element.href = url;
    element.target = "_blank";
    element.rel = "noopener";
    element.removeAttribute("aria-disabled");
    element.classList.remove("disabled");
  });
})();
"""

OUTPUT.mkdir()
ASSETS.mkdir()

shutil.copy2(ICON_SOURCE, ASSETS / "workforce-icon.png")
(ASSETS / "workforce.css").write_text(CSS.strip() + "\n", encoding="utf-8")
(ASSETS / "app-links.js").write_text(APP_LINKS.strip() + "\n", encoding="utf-8")

for page in pages:
    relative = page["path"].removeprefix("/workforce/").strip("/")
    directory = OUTPUT if not relative else OUTPUT / relative
    directory.mkdir(parents=True, exist_ok=True)

    page_html = homepage_html(page) if page["type"] == "homepage" else detail_html(page)
    (directory / "index.html").write_text(page_html, encoding="utf-8")

sitemap_urls = [absolute(page["path"]) for page in pages]
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
(OUTPUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

manifest = {
    "status": "local-only",
    "generated_pages": len(pages),
    "root_homepage_modified": False,
    "root_sitemap_modified": False,
    "guardian_modified": False,
    "store_links_confirmed": False,
    "files": sorted(
        str(path.relative_to(ROOT))
        for path in OUTPUT.rglob("*")
        if path.is_file()
    ),
}
(OUTPUT / "build-manifest.json").write_text(
    json.dumps(manifest, indent=2) + "\n",
    encoding="utf-8",
)

print(f"Created {OUTPUT}")
print(f"Generated HTML pages: {len(list(OUTPUT.rglob('index.html')))}")
print(f"Generated sitemap URLs: {len(sitemap_urls)}")
print(f"Generated files: {len(manifest['files']) + 1}")
print("Root homepage modified: no")
print("Root sitemap modified: no")
print("Guardian modified: no")
print("Store links enabled: no")
