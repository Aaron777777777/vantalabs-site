#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path.cwd()
WORKFORCE = ROOT / "workforce"
PLAN = json.loads(
    (ROOT / "workforce_page_plan.json").read_text(encoding="utf-8")
)

pages = {
    page["path"]: page
    for page in PLAN["pages"]
    if page["path"] != "/workforce/"
}

cluster_context = {
    "attendance": {
        "setting": "organisations replacing paper registers or inconsistent attendance messages",
        "manager_focus": "whether the attendance record is complete enough to review",
        "worker_focus": "a quick and understandable way to record the start and end of attendance",
        "record": "booking activity, attendance history and recorded hours",
        "risk": "late, forgotten or incomplete booking actions",
        "process": "agree when workers should book on, explain how exceptions are handled and review incomplete records promptly",
    },
    "clocking": {
        "setting": "teams that need a repeatable booking-on and booking-off routine",
        "manager_focus": "when an attendance period began, when it ended and whether anything needs correcting",
        "worker_focus": "a clear action at the beginning and end of the working period",
        "record": "the opening and closing points used to calculate attendance",
        "risk": "missing book-off actions or records created at the wrong time",
        "process": "define the expected clock-in moment, make the booking-off step equally clear and review exceptions before they become old",
    },
    "gps-attendance": {
        "setting": "businesses operating from defined workplaces, customer locations or changing sites",
        "manager_focus": "whether available location context supports the recorded workplace activity",
        "worker_focus": "understanding when location is requested and what happens when it is unavailable",
        "record": "attendance information combined with available device-location context",
        "risk": "assuming that a phone location is always exact or immediately available",
        "process": "explain location use, check permissions during setup and provide a fair exception process for signal or device problems",
    },
    "timesheets": {
        "setting": "organisations turning daily attendance activity into monthly working-hour records",
        "manager_focus": "whether recorded periods accurately describe the hours being reviewed",
        "worker_focus": "being able to see their own hours and identify missing attendance",
        "record": "My Hours, monthly attendance periods and exportable timesheet information",
        "risk": "treating incomplete attendance as a final payroll-ready total",
        "process": "review incomplete entries, check unusual durations and verify records before further payroll or accounting use",
    },
    "workplace-presence": {
        "setting": "managers who need to understand who is currently recorded as working at a site",
        "manager_focus": "current booking status across the relevant workplace or workplaces",
        "worker_focus": "knowing that their booking action has been recorded correctly",
        "record": "current presence status connected to historic attendance",
        "risk": "confusing delayed device data with a definite absence",
        "process": "use current status as an operational view, check delayed records sensibly and retain a clear escalation route",
    },
    "mobile-workforces": {
        "setting": "field teams, travelling staff and workers who do not begin every shift at one fixed office",
        "manager_focus": "how attendance and hours are recorded across changing locations",
        "worker_focus": "a consistent process that works from a supported mobile device",
        "record": "off-site bookings, field attendance and working-hour history",
        "risk": "poor connectivity or unclear expectations producing inconsistent records",
        "process": "define suitable work locations, explain offline or signal problems and keep the same attendance expectations across teams",
    },
    "worker-safety": {
        "setting": "organisations using scheduled contact points, welfare prompts or incident-reporting procedures",
        "manager_focus": "which checks are due, completed or need a human response",
        "worker_focus": "knowing what action is expected and who responds when help is needed",
        "record": "scheduled prompts, phone checks and relevant incident information",
        "risk": "mistaking an app notification for a complete safety system",
        "process": "assign responsibility for missed checks, keep emergency routes separate and train workers on the organisation’s actual procedure",
    },
    "control-centre": {
        "setting": "authorised managers overseeing worker status, checks and attendance activity",
        "manager_focus": "which workers are active, which records need attention and what follow-up is appropriate",
        "worker_focus": "having their relevant attendance and check actions reflected accurately",
        "record": "Control Centre status, attendance information and manager checks",
        "risk": "making decisions from stale or incomplete device data",
        "process": "review timestamps, distinguish routine exceptions from genuine concerns and record appropriate follow-up",
    },
    "reporting": {
        "setting": "businesses reviewing attendance history or moving authorised records into another business process",
        "manager_focus": "whether the selected workers, dates and attendance periods are correct",
        "worker_focus": "having recorded hours represented clearly and consistently",
        "record": "attendance reports, monthly history and timesheet exports",
        "risk": "using an unchecked export as a final payroll, legal or accounting conclusion",
        "process": "select the correct period, inspect unusual records and verify the export before relying on it elsewhere",
    },
    "operations": {
        "setting": "businesses bringing workplaces, workers, roles and attendance activity into one operational system",
        "manager_focus": "whether access, sites and worker records reflect the real organisation",
        "worker_focus": "seeing only the actions and information relevant to their role",
        "record": "workplace configuration, role-based activity and workforce records",
        "risk": "unclear ownership of setup, corrections or ongoing administration",
        "process": "assign responsible managers, keep workplace details current and review user access when roles change",
    },
}

heading_sets = [
    (
        "Where this fits in a working day",
        "What the manager actually needs to see",
        "A sensible operating process",
        "What the record can and cannot prove",
    ),
    (
        "The business problem behind the search",
        "What workers experience",
        "How to introduce it without confusion",
        "Where human review still matters",
    ),
    (
        "A practical use case",
        "The information created",
        "Questions to settle before rollout",
        "Important limits to keep visible",
    ),
    (
        "Why organisations look for this",
        "How the workflow develops",
        "What makes the record useful",
        "What technology does not remove",
    ),
    (
        "From day-to-day action to usable record",
        "The worker side of the process",
        "The manager side of the process",
        "Handling exceptions fairly",
    ),
    (
        "The operational situation",
        "What a good result looks like",
        "Setting expectations with the team",
        "Reviewing unusual records",
    ),
    (
        "When this approach is most useful",
        "What happens inside Vanta Workforce",
        "How the organisation should support it",
        "What to check before relying on the result",
    ),
    (
        "The question this page answers",
        "How the record becomes useful",
        "A clearer rollout method",
        "Honest limitations",
    ),
]

scenario_templates = [
    (
        "The search for {intent} usually begins when {setting}. "
        "The immediate aim is not simply to replace one form with another. "
        "It is to create a repeatable action that produces information people can understand later."
    ),
    (
        "Businesses considering {intent} are often trying to solve a visibility problem. "
        "In practice, {setting}. Vanta Workforce gives that activity a defined place instead of leaving it across paper, messages and memory."
    ),
    (
        "{intent_title} matters most when the working environment is not naturally producing one reliable record. "
        "That is common for {setting}. The value comes from connecting the worker action with the later management review."
    ),
    (
        "A useful {intent} process starts with the real workplace rather than the software screen. "
        "For {setting}, the organisation first needs to decide what should be recorded, when it should happen and who handles exceptions."
    ),
    (
        "The business case for {intent} is strongest when {setting}. "
        "A structured mobile record can reduce uncertainty, but only when the process around it is explained and followed consistently."
    ),
    (
        "{intent_title} is not a separate administrative exercise. "
        "For {setting}, it becomes part of the normal working routine and later supports attendance, presence or hour review."
    ),
    (
        "Organisations normally investigate {intent} after discovering that their current evidence is fragmented. "
        "This is especially noticeable for {setting}, where small gaps quickly become difficult to reconstruct."
    ),
    (
        "The practical question behind {intent} is straightforward: how can {setting} produce a clearer record without creating unnecessary work for staff?"
    ),
]

worker_templates = [
    (
        "For the worker, the important part is {worker_focus}. "
        "The screen should support the agreed process rather than make the worker interpret company policy. "
        "Clear onboarding is especially important when permissions, location or scheduled prompts are involved."
    ),
    (
        "Workers mainly need {worker_focus}. "
        "They should also know what to do when the expected action cannot be completed, because device, signal and account problems can happen during a real shift."
    ),
    (
        "The worker-facing experience centres on {worker_focus}. "
        "A business should explain why the information is needed, who can see it and how genuine mistakes will be corrected."
    ),
    (
        "From a worker’s perspective, success means {worker_focus}. "
        "The process should remain understandable during a busy arrival, departure, site move or scheduled check."
    ),
    (
        "The relevant worker action needs to be brief, but its meaning must be clear: {worker_focus}. "
        "Without that shared understanding, even technically valid records can be misleading."
    ),
    (
        "Workers are more likely to use the system consistently when they understand the purpose. "
        "Here that means {worker_focus}, together with a known route for reporting a missing or incorrect record."
    ),
    (
        "The app supplies the mobile action; the organisation supplies the expectation. "
        "For this use case, workers need {worker_focus} and a fair response when normal device conditions interfere."
    ),
    (
        "A worker should not have to guess what counts as completion. "
        "The central expectation is {worker_focus}, supported by simple guidance for unusual situations."
    ),
]

manager_templates = [
    (
        "The manager is trying to understand {manager_focus}. "
        "Vanta Workforce keeps the relevant {record} together, making review more structured than collecting separate updates."
    ),
    (
        "For an authorised manager, the useful question is {manager_focus}. "
        "The resulting view brings together {record}, but it still needs interpretation when a record is late, incomplete or unusual."
    ),
    (
        "Management value comes from being able to review {manager_focus}. "
        "The app organises {record}; the manager remains responsible for deciding whether follow-up or correction is needed."
    ),
    (
        "The dashboard or record should help answer {manager_focus}. "
        "It does this through {record}, not through unsupported assumptions about what happened beyond the information received."
    ),
    (
        "A manager needs more than a list of taps. "
        "They need to understand {manager_focus}, using {record} and the surrounding workplace context."
    ),
    (
        "The relevant management view focuses on {manager_focus}. "
        "Because {record} can be affected by human and device conditions, exceptions should be reviewed rather than automatically judged."
    ),
    (
        "The purpose of the manager view is to make {manager_focus} easier to assess. "
        "Vanta Workforce supplies {record}, while the organisation retains responsibility for the final operational decision."
    ),
    (
        "Authorised managers can use the system to examine {manager_focus}. "
        "That evidence includes {record} and should be read with its timestamp and workplace circumstances."
    ),
]

process_templates = [
    (
        "A sensible rollout is to {process}. "
        "That creates a shared standard before the first unusual record appears. "
        "The known risk is {risk}, so the correction and escalation route should be agreed in advance."
    ),
    (
        "Before launch, the business should {process}. "
        "This matters because {risk}. A clear exception process protects both record quality and worker confidence."
    ),
    (
        "The most reliable approach is to {process}. "
        "Managers should avoid treating {risk} as automatic misconduct without checking the surrounding facts."
    ),
    (
        "Implementation should begin with one documented routine: {process}. "
        "The organisation can then review how often {risk} occurs and improve guidance where needed."
    ),
    (
        "The app works best inside an explicit process. "
        "The business should {process}, while recognising that {risk} may still require manual review."
    ),
    (
        "Good records begin before anyone opens the app. "
        "The organisation should {process}. This reduces the chance that {risk} becomes a recurring source of disagreement."
    ),
    (
        "Rollout should include a short explanation, a test action and a known support route. "
        "In practical terms, that means the organisation must {process}, particularly because of {risk}."
    ),
    (
        "A fair operating method is to {process}. "
        "That allows managers to distinguish a genuine attendance or safety concern from {risk}."
    ),
]

limit_templates = [
    (
        "Vanta Workforce records information received through the service; it does not make every record conclusive. "
        "Connectivity, permissions, battery restrictions, device behaviour and human error can all affect what appears."
    ),
    (
        "The system improves organisation, not certainty. "
        "A timestamp, status or location value should be reviewed as part of the wider workplace record rather than treated as infallible proof."
    ),
    (
        "Technology cannot remove the need for proportionate management judgement. "
        "Unusual records should be checked against the worker’s explanation, device conditions and the organisation’s procedure."
    ),
    (
        "No mobile attendance or safety app can promise perfect availability. "
        "The organisation still needs fallback arrangements for poor signal, device failure, emergencies and genuine user mistakes."
    ),
    (
        "The information is operational evidence, not an automatic legal, payroll or disciplinary conclusion. "
        "Records and exports should be checked before they are used for decisions outside the app."
    ),
    (
        "Current status can be delayed, and location can be imprecise. "
        "Managers should check timing and context before deciding that a worker failed to follow the expected process."
    ),
    (
        "The app supports the organisation’s process but does not replace it. "
        "Emergency response, employment decisions, payroll review and legal obligations remain with the appropriate people."
    ),
    (
        "A useful digital record can still be incomplete. "
        "The safest approach is to preserve an audit trail, review exceptions consistently and avoid promises the device cannot support."
    ),
]


def deterministic_index(path: str, count: int, salt: str) -> int:
    digest = hashlib.sha256(f"{salt}:{path}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % count


def select(items: list | tuple, path: str, salt: str):
    return items[deterministic_index(path, len(items), salt)]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def page_file(web_path: str) -> Path:
    relative = web_path.removeprefix("/workforce/").strip("/")
    return WORKFORCE / relative / "index.html"


def render_page_content(page: dict) -> str:
    path = page["path"]
    context = cluster_context[page["cluster"]]
    headings = select(heading_sets, path, "headings")

    values = {
        **context,
        "intent": page["intent"],
        "intent_title": page["intent"].title(),
    }

    paragraphs = [
        select(scenario_templates, path, "scenario").format(**values),
        select(worker_templates, path, "worker").format(**values),
        select(manager_templates, path, "manager").format(**values),
        select(process_templates, path, "process").format(**values),
        select(limit_templates, path, "limits").format(**values),
    ]

    workflow_steps = [
        f"Define what counts as a valid {page['intent']} action for this organisation.",
        f"Explain the worker-facing process and how {context['risk']} will be handled.",
        f"Review {context['record']} using the relevant worker, workplace and date.",
        "Correct genuine errors through the authorised management process.",
    ]

    use_case_heading = (
        f"Using {page['intent']} in practice"
        if page["type"] != "guide"
        else f"Putting this guidance into practice"
    )

    return f"""<article class="content-shell">
    <section class="content-section page-specific">
      <p class="section-label">{esc(page['cluster_name'])}</p>
      <h2>{esc(headings[0])}</h2>
      <p>{esc(paragraphs[0])}</p>
      <p>{esc(paragraphs[1])}</p>
    </section>

    <section class="feature-panel page-specific">
      <div>
        <p class="section-label">{esc(use_case_heading)}</p>
        <h2>{esc(headings[1])}</h2>
        <p>{esc(paragraphs[2])}</p>
        <ul>
          <li>{esc(workflow_steps[0])}</li>
          <li>{esc(workflow_steps[1])}</li>
          <li>{esc(workflow_steps[2])}</li>
        </ul>
      </div>
      <aside>
        <strong>{esc(headings[3])}</strong>
        <p>{esc(paragraphs[4])}</p>
      </aside>
    </section>

    <section class="content-section page-specific">
      <p class="section-label">Implementation</p>
      <h2>{esc(headings[2])}</h2>
      <p>{esc(paragraphs[3])}</p>
      <p>
        The final step is to {esc(workflow_steps[3].lower())}
        That keeps the record useful without pretending that every device event
        explains the complete working situation.
      </p>
    </section>

    <section class="cluster-callout">
      <div>
        <p class="section-label">Related topic</p>
        <h2>{esc(page['cluster_name'])}</h2>
        <p>
          This page forms part of the Vanta Workforce
          {esc(page['cluster_name'].lower())} cluster, where related attendance,
          workplace and management questions are covered in more detail.
        </p>
      </div>
      <a class="store-button secondary" href="{esc(page['cluster_leader'])}">
        Explore the cluster
      </a>
    </section>

    <section class="faq-section">"""


pattern = re.compile(
    r'<article class="content-shell">.*?<section class="faq-section">',
    re.S,
)

changed = 0

for path, page in sorted(pages.items()):
    target = page_file(path)

    if not target.is_file():
        raise SystemExit(f"Missing page: {target}")

    source = target.read_text(encoding="utf-8")

    replacement = render_page_content(page)

    updated, count = pattern.subn(replacement, source, count=1)

    if count != 1:
        raise SystemExit(f"Could not replace content structure in {target}")

    target.write_text(updated, encoding="utf-8")
    changed += 1

print(f"Diversified supporting pages: {changed}")
print("Homepage changed: no")
print("URLs changed: no")
print("Titles changed: no")
print("Metadata changed: no")
print("Schema changed: no")
print("Store links changed: no")
