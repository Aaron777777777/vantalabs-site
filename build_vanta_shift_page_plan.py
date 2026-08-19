#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from pathlib import Path

OUTPUT = Path("vanta_shift_page_plan.json")

clusters = {
    "shift-calendar": [
        ("shift-calendar-app", "Shift Calendar App"),
        ("work-shift-calendar", "Work Shift Calendar"),
        ("employee-shift-calendar", "Employee Shift Calendar"),
        ("personal-shift-calendar", "Personal Shift Calendar"),
        ("mobile-shift-calendar", "Mobile Shift Calendar"),
        ("weekly-shift-calendar", "Weekly Shift Calendar"),
        ("monthly-shift-calendar", "Monthly Shift Calendar"),
        ("upcoming-shifts-app", "Upcoming Shifts App"),
        ("view-my-work-shifts", "View My Work Shifts"),
        ("work-schedule-calendar", "Work Schedule Calendar"),
        ("shift-planner-app", "Shift Planner App"),
        ("personal-shift-planner-app", "Personal Shift Planner App"),
    ],
    "rota-viewing": [
        ("rota-app-for-employees", "Rota App for Employees"),
        ("employee-rota-app", "Employee Rota App"),
        ("view-my-rota", "View My Rota"),
        ("work-rota-app", "Work Rota App"),
        ("mobile-rota-viewer", "Mobile Rota Viewer"),
        ("weekly-work-rota", "Weekly Work Rota"),
        ("monthly-work-rota", "Monthly Work Rota"),
        ("staff-rota-viewer", "Staff Rota Viewer"),
        ("digital-work-rota", "Digital Work Rota"),
        ("personal-rota-calendar", "Personal Rota Calendar"),
        ("rota-planner-app", "Rota Planner App"),
        ("personal-rota-planner", "Personal Rota Planner"),
    ],
    "notifications": [
        ("shift-notification-app", "Shift Notification App"),
        ("work-shift-reminders", "Work Shift Reminders"),
        ("upcoming-shift-alerts", "Upcoming Shift Alerts"),
        ("rota-notification-app", "Rota Notification App"),
        ("employee-shift-alerts", "Employee Shift Alerts"),
        ("work-schedule-reminders", "Work Schedule Reminders"),
        ("next-shift-reminder", "Next Shift Reminder"),
        ("shift-change-notifications", "Shift Change Notifications"),
        ("mobile-shift-alerts", "Mobile Shift Alerts"),
        ("never-miss-a-work-shift", "Never Miss a Work Shift"),
    ],
    "hours": [
        ("work-hours-tracker", "Work Hours Tracker"),
        ("shift-hours-tracker", "Shift Hours Tracker"),
        ("weekly-hours-tracker", "Weekly Hours Tracker"),
        ("monthly-hours-tracker", "Monthly Hours Tracker"),
        ("scheduled-hours-tracker", "Scheduled Hours Tracker"),
        ("shift-duration-calculator", "Shift Duration Calculator"),
        ("weekly-work-hours", "Weekly Work Hours"),
        ("monthly-work-hours", "Monthly Work Hours"),
        ("hours-from-work-rota", "Hours From a Work Rota"),
        ("work-time-summary", "Work Time Summary"),
    ],
    "earnings": [
        ("shift-earnings-tracker", "Shift Earnings Tracker"),
        ("estimated-pay-app", "Estimated Pay App"),
        ("work-pay-calculator", "Work Pay Calculator"),
        ("shift-pay-calculator", "Shift Pay Calculator"),
        ("weekly-earnings-tracker", "Weekly Earnings Tracker"),
        ("monthly-earnings-tracker", "Monthly Earnings Tracker"),
        ("estimated-wages-calculator", "Estimated Wages Calculator"),
        ("hourly-pay-shift-tracker", "Hourly Pay Shift Tracker"),
        ("work-hours-and-pay-app", "Work Hours and Pay App"),
        ("rota-earnings-calculator", "Rota Earnings Calculator"),
    ],
    "shift-patterns": [
        ("shift-pattern-calendar", "Shift Pattern Calendar"),
        ("rotating-shift-calendar", "Rotating Shift Calendar"),
        ("repeating-shift-calendar", "Repeating Shift Calendar"),
        ("day-and-night-shifts", "Day and Night Shifts"),
        ("alternating-shift-calendar", "Alternating Shift Calendar"),
        ("work-rotation-calendar", "Work Rotation Calendar"),
        ("shift-cycle-calendar", "Shift Cycle Calendar"),
        ("repeating-rota-calendar", "Repeating Rota Calendar"),
        ("rotating-work-schedule", "Rotating Work Schedule"),
        ("personal-shift-pattern", "Personal Shift Pattern"),
        ("custom-shift-calendar", "Custom Shift Calendar"),
        ("custom-shift-pattern-app", "Custom Shift Pattern App"),
        ("days-off-calendar", "Days Off Calendar"),
    ],
    "common-patterns": [
        ("4-on-4-off-calendar", "4 On 4 Off Calendar"),
        ("4-on-4-off-shift-app", "4 On 4 Off Shift App"),
        ("2-on-2-off-calendar", "2 On 2 Off Calendar"),
        ("panama-shift-calendar", "Panama Shift Calendar"),
        ("continental-shift-calendar", "Continental Shift Calendar"),
        ("dupont-shift-calendar", "DuPont Shift Calendar"),
        ("12-hour-shift-calendar", "12-Hour Shift Calendar"),
        ("8-hour-shift-calendar", "8-Hour Shift Calendar"),
        ("alternating-week-shifts", "Alternating Week Shifts"),
        ("rotating-day-night-calendar", "Rotating Day and Night Calendar"),
    ],
    "night-shifts": [
        ("night-shift-calendar", "Night Shift Calendar"),
        ("night-worker-rota-app", "Night Worker Rota App"),
        ("overnight-shift-calendar", "Overnight Shift Calendar"),
        ("rotating-night-shifts", "Rotating Night Shifts"),
        ("night-shift-hours-tracker", "Night Shift Hours Tracker"),
        ("night-shift-earnings-tracker", "Night Shift Earnings Tracker"),
        ("night-shift-reminders", "Night Shift Reminders"),
        ("upcoming-night-shifts", "Upcoming Night Shifts"),
        ("day-night-rota-calendar", "Day and Night Rota Calendar"),
        ("plan-life-around-night-shifts", "Plan Life Around Night Shifts"),
    ],
    "workers": [
        ("nurse-shift-calendar", "Nurse Shift Calendar"),
        ("healthcare-worker-rota", "Healthcare Worker Rota"),
        ("security-guard-shift-app", "Security Guard Shift App"),
        ("factory-worker-shift-calendar", "Factory Worker Shift Calendar"),
        ("warehouse-worker-rota", "Warehouse Worker Rota"),
        ("hospitality-worker-shifts", "Hospitality Worker Shifts"),
        ("transport-worker-shift-calendar", "Transport Worker Shift Calendar"),
        ("emergency-services-rota", "Emergency Services Rota"),
        ("offshore-worker-shift-calendar", "Offshore Worker Shift Calendar"),
        ("care-worker-rota-app", "Care Worker Rota App"),
        ("firefighter-shift-calendar", "Firefighter Shift Calendar"),
        ("police-shift-calendar", "Police Shift Calendar"),
        ("paramedic-shift-calendar", "Paramedic Shift Calendar"),
    ],
    "guides": [
        ("guides/how-shift-calendar-apps-work", "How Shift Calendar Apps Work"),
        ("guides/how-to-view-your-work-rota", "How to View Your Work Rota"),
        ("guides/how-shift-notifications-work", "How Shift Notifications Work"),
        ("guides/how-to-track-scheduled-hours", "How to Track Scheduled Hours"),
        ("guides/how-to-estimate-shift-pay", "How to Estimate Shift Pay"),
        ("guides/how-4-on-4-off-shifts-work", "How 4 On 4 Off Shifts Work"),
        ("guides/how-panama-shifts-work", "How Panama Shifts Work"),
        ("guides/how-to-manage-rotating-shifts", "How to Manage Rotating Shifts"),
        ("guides/how-to-plan-around-night-shifts", "How to Plan Around Night Shifts"),
        ("guides/shift-calendar-vs-paper-rota", "Shift Calendar vs Paper Rota"),
        ("guides/how-to-create-a-custom-shift-pattern", "How to Create a Custom Shift Pattern"),
        ("guides/how-to-plan-your-work-rota", "How to Plan Your Work Rota"),
        ("guides/how-to-calculate-hours-from-your-rota", "How to Calculate Hours From Your Rota"),
        ("guides/how-to-estimate-pay-from-your-rota", "How to Estimate Pay From Your Rota"),
    ],
}

cluster_descriptions = {
    "shift-calendar": "assigned shifts and upcoming work in a clear personal calendar",
    "rota-viewing": "an employee’s own rota and scheduled working days",
    "notifications": "reminders and alerts for upcoming or changed shifts",
    "hours": "scheduled shift durations and weekly or monthly hour totals",
    "earnings": "estimated pay based on scheduled hours and hourly rates",
    "shift-patterns": "repeating work patterns shown in a personal calendar",
    "common-patterns": "common rotating schedules such as 4 on 4 off and Panama shifts",
    "night-shifts": "overnight work, changing schedules and upcoming night shifts",
    "workers": "personal shift visibility across common shift-based occupations",
    "guides": "practical explanations for employees who work changing shifts",
}

pages = [
    {
        "path": "/vanta-shift/",
        "type": "home",
        "cluster": "home",
        "title": "Vanta Shift",
        "h1": "Your shifts, hours and estimated pay",
        "intent": "Vanta Shift app",
        "cluster_leader": "/vanta-shift/",
        "description": (
            "Vanta Shift helps employees view assigned shifts, receive shift "
            "notifications, review scheduled hours and estimate their pay."
        ),
    }
]

for cluster, entries in clusters.items():
    leader_path = f"/vanta-shift/{entries[0][0]}/"

    for index, (slug, title) in enumerate(entries):
        path = f"/vanta-shift/{slug}/"
        page_type = "guide" if cluster == "guides" else "feature"

        description = (
            f"Explore {title.lower()} with Vanta Shift, including "
            f"{cluster_descriptions[cluster]}."
        )

        pages.append(
            {
                "path": path,
                "type": page_type,
                "cluster": cluster,
                "title": title,
                "h1": title,
                "intent": title.lower(),
                "description": description,
                "cluster_leader": leader_path,
                "position": index + 1,
            }
        )

paths = [page["path"] for page in pages]
titles = [page["title"].casefold() for page in pages]
h1s = [page["h1"].casefold() for page in pages]

checks = {
    "page_count": len(pages),
    "unique_paths": len(set(paths)),
    "unique_titles": len(set(titles)),
    "unique_h1s": len(set(h1s)),
    "cluster_count": len(clusters),
}

if checks["unique_paths"] != checks["page_count"]:
    raise SystemExit(f"Duplicate paths in plan: {checks}")

if checks["unique_titles"] != checks["page_count"]:
    raise SystemExit(f"Duplicate titles in plan: {checks}")

if checks["unique_h1s"] != checks["page_count"]:
    raise SystemExit(f"Duplicate H1s in plan: {checks}")


for page in pages:
    if page["path"] == "/vanta-shift/":
        continue

    if not re.fullmatch(
        r"/vanta-shift/(?:guides/)?[a-z0-9-]+/",
        page["path"],
    ):
        raise SystemExit(f"Invalid path: {page['path']}")

for forbidden in [
    "booking on",
    "booking off",
    "attendance",
    "manager dashboard",
    "workforce oversight",
    "clock in",
    "clock-in",
]:
    for page in pages:
        combined = " ".join(
            str(page.get(key, ""))
            for key in ["title", "h1", "intent", "description"]
        ).casefold()

        if forbidden in combined:
            raise SystemExit(
                f"Forbidden Workforce wording found in {page['path']}: "
                f"{forbidden}"
            )

OUTPUT.write_text(
    json.dumps(
        {
            "product": "Vanta Shift",
            "base_path": "/vanta-shift/",
            "product_scope": (
                "Employee-facing shift viewing, notifications, scheduled "
                "hours and estimated pay"
            ),
            "android_url": (
                "https://play.google.com/store/apps/details"
                "?id=com.vantashift.app"
            ),
            "ios_url": (
                "https://apps.apple.com/us/app/"
                "shift-planner-rota-hours/id6771880899"
            ),
            "page_count": len(pages),
            "clusters": list(clusters),
            "pages": pages,
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n",
    encoding="utf-8",
)

print("Plan written:", OUTPUT)
print("Scope: employee shift viewing, notifications, hours and estimated pay")
print("Pages:", checks["page_count"])
print("Clusters:", checks["cluster_count"])
print("Unique paths:", checks["unique_paths"])
print("Unique titles:", checks["unique_titles"])
print("Unique H1s:", checks["unique_h1s"])
print("Forbidden Workforce wording: 0")
