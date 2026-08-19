#!/usr/bin/env python3

import json
from collections import Counter
from pathlib import Path

OUTPUT = Path("workforce_page_plan.json")

clusters = [
    {
        "id": "attendance",
        "name": "Staff attendance",
        "leader": "staff-attendance-app",
        "pages": [
            ("staff-attendance-app", "Vanta Workforce | Staff Attendance App", "staff attendance software"),
            ("employee-attendance-app", "Vanta Workforce | Employee Attendance App", "employee attendance app"),
            ("workforce-attendance-system", "Vanta Workforce | Workforce Attendance System", "workforce attendance system"),
            ("mobile-staff-attendance-app", "Vanta Workforce | Mobile Staff Attendance App", "mobile staff attendance"),
            ("digital-attendance-register", "Vanta Workforce | Digital Attendance Register", "digital attendance register"),
            ("attendance-management-app", "Vanta Workforce | Attendance Management App", "attendance management"),
            ("staff-attendance-tracker", "Vanta Workforce | Staff Attendance Tracker", "staff attendance tracking"),
            ("employee-attendance-records", "Vanta Workforce | Employee Attendance Records", "employee attendance records"),
        ],
    },
    {
        "id": "clocking",
        "name": "Clocking in and out",
        "leader": "employee-clock-in-app",
        "pages": [
            ("employee-clock-in-app", "Vanta Workforce | Employee Clock-In App", "employee clock-in app"),
            ("staff-clock-in-app", "Vanta Workforce | Staff Clock-In App", "staff clock-in app"),
            ("clock-in-clock-out-app", "Vanta Workforce | Clock-In Clock-Out App", "clock in and out"),
            ("mobile-time-clock-app", "Vanta Workforce | Mobile Time Clock App", "mobile time clock"),
            ("digital-clock-in-system", "Vanta Workforce | Digital Clock-In System", "digital clock-in"),
            ("workplace-clock-in-app", "Vanta Workforce | Workplace Clock-In App", "workplace clock-in"),
            ("worker-booking-on-app", "Vanta Workforce | Worker Booking-On App", "worker booking on"),
            ("worker-booking-off-app", "Vanta Workforce | Worker Booking-Off App", "worker booking off"),
        ],
    },
    {
        "id": "gps-attendance",
        "name": "GPS and location-aware attendance",
        "leader": "gps-clock-in-app",
        "pages": [
            ("gps-clock-in-app", "Vanta Workforce | GPS Clock-In App", "GPS clock-in app"),
            ("location-based-clock-in", "Vanta Workforce | Location-Based Clock-In", "location-based clock-in"),
            ("geofenced-time-clock", "Vanta Workforce | Geofenced Time Clock", "geofenced time clock"),
            ("worksite-clock-in-app", "Vanta Workforce | Worksite Clock-In App", "worksite clock-in"),
            ("location-aware-attendance-app", "Vanta Workforce | Location-Aware Attendance App", "location-aware attendance"),
            ("gps-attendance-system", "Vanta Workforce | GPS Attendance System", "GPS attendance system"),
            ("employee-location-clock-in", "Vanta Workforce | Employee Location Clock-In", "employee location clock-in"),
            ("site-based-clock-in-system", "Vanta Workforce | Site-Based Clock-In System", "site-based clock-in"),
        ],
    },
    {
        "id": "timesheets",
        "name": "Timesheets and working hours",
        "leader": "employee-timesheet-app",
        "pages": [
            ("employee-timesheet-app", "Vanta Workforce | Employee Timesheet App", "employee timesheet app"),
            ("staff-timesheet-app", "Vanta Workforce | Staff Timesheet App", "staff timesheet app"),
            ("mobile-timesheet-app", "Vanta Workforce | Mobile Timesheet App", "mobile timesheets"),
            ("digital-timesheet-system", "Vanta Workforce | Digital Timesheet System", "digital timesheet system"),
            ("working-hours-tracker", "Vanta Workforce | Working Hours Tracker", "working hours tracking"),
            ("employee-hours-tracking", "Vanta Workforce | Employee Hours Tracking", "employee hours tracking"),
            ("monthly-timesheet-app", "Vanta Workforce | Monthly Timesheet App", "monthly timesheets"),
            ("overnight-shift-timesheets", "Vanta Workforce | Overnight Shift Timesheets", "overnight shift timesheets"),
        ],
    },
    {
        "id": "workplace-presence",
        "name": "Workplace and site presence",
        "leader": "workplace-presence-app",
        "pages": [
            ("workplace-presence-app", "Vanta Workforce | Workplace Presence App", "workplace presence"),
            ("employee-presence-tracking", "Vanta Workforce | Employee Presence Tracking", "employee presence"),
            ("site-attendance-app", "Vanta Workforce | Site Attendance App", "site attendance"),
            ("multi-site-attendance-system", "Vanta Workforce | Multi-Site Attendance System", "multi-site attendance"),
            ("construction-site-attendance-app", "Vanta Workforce | Construction Site Attendance App", "construction attendance"),
            ("workplace-attendance-register", "Vanta Workforce | Workplace Attendance Register", "workplace attendance register"),
            ("staff-on-site-tracker", "Vanta Workforce | Staff On-Site Tracker", "staff on-site status"),
            ("who-is-working-app", "Vanta Workforce | Who Is Working App", "who is working"),
        ],
    },
    {
        "id": "mobile-workforces",
        "name": "Mobile and field workforces",
        "leader": "field-worker-attendance-app",
        "pages": [
            ("field-worker-attendance-app", "Vanta Workforce | Field Worker Attendance App", "field worker attendance"),
            ("mobile-workforce-management-app", "Vanta Workforce | Mobile Workforce Management App", "mobile workforce management"),
            ("remote-worker-check-in-app", "Vanta Workforce | Remote Worker Check-In App", "remote worker check-in"),
            ("mobile-worker-clock-in-app", "Vanta Workforce | Mobile Worker Clock-In App", "mobile worker clock-in"),
            ("field-team-timesheet-app", "Vanta Workforce | Field Team Timesheet App", "field team timesheets"),
            ("distributed-workforce-attendance", "Vanta Workforce | Distributed Workforce Attendance", "distributed workforce attendance"),
            ("off-site-worker-attendance", "Vanta Workforce | Off-Site Worker Attendance", "off-site worker attendance"),
            ("field-staff-hours-tracker", "Vanta Workforce | Field Staff Hours Tracker", "field staff hours"),
        ],
    },
    {
        "id": "worker-safety",
        "name": "Worker safety and scheduled checks",
        "leader": "worker-safety-check-app",
        "pages": [
            ("worker-safety-check-app", "Vanta Workforce | Worker Safety Check App", "worker safety checks"),
            ("lone-worker-check-in-app", "Vanta Workforce | Lone Worker Check-In App", "lone worker check-in"),
            ("scheduled-worker-checks", "Vanta Workforce | Scheduled Worker Checks", "scheduled worker checks"),
            ("staff-welfare-check-app", "Vanta Workforce | Staff Welfare Check App", "staff welfare checks"),
            ("workplace-incident-reporting-app", "Vanta Workforce | Workplace Incident Reporting App", "workplace incident reporting"),
            ("employee-incident-reporting", "Vanta Workforce | Employee Incident Reporting", "employee incident reporting"),
            ("worker-phone-checks", "Vanta Workforce | Worker Phone Checks", "worker phone checks"),
            ("scheduled-safety-prompts", "Vanta Workforce | Scheduled Safety Prompts", "scheduled safety prompts"),
        ],
    },
    {
        "id": "control-centre",
        "name": "Manager and Control Centre oversight",
        "leader": "control-centre-workforce-app",
        "pages": [
            ("control-centre-workforce-app", "Vanta Workforce | Control Centre Workforce App", "workforce control centre"),
            ("live-workforce-status", "Vanta Workforce | Live Workforce Status", "live workforce status"),
            ("manager-attendance-dashboard", "Vanta Workforce | Manager Attendance Dashboard", "manager attendance dashboard"),
            ("workforce-oversight-app", "Vanta Workforce | Workforce Oversight App", "workforce oversight"),
            ("manager-worker-status-app", "Vanta Workforce | Manager Worker Status App", "manager worker status"),
            ("staff-status-dashboard", "Vanta Workforce | Staff Status Dashboard", "staff status dashboard"),
            ("workplace-control-centre", "Vanta Workforce | Workplace Control Centre", "workplace control centre"),
            ("multi-site-workforce-dashboard", "Vanta Workforce | Multi-Site Workforce Dashboard", "multi-site workforce dashboard"),
        ],
    },
    {
        "id": "reporting",
        "name": "Attendance reporting and exports",
        "leader": "attendance-reporting-app",
        "pages": [
            ("attendance-reporting-app", "Vanta Workforce | Attendance Reporting App", "attendance reporting"),
            ("timesheet-export-app", "Vanta Workforce | Timesheet Export App", "timesheet export"),
            ("staff-hours-reporting", "Vanta Workforce | Staff Hours Reporting", "staff hours reporting"),
            ("employee-attendance-reports", "Vanta Workforce | Employee Attendance Reports", "employee attendance reports"),
            ("monthly-attendance-reports", "Vanta Workforce | Monthly Attendance Reports", "monthly attendance reports"),
            ("workforce-hours-export", "Vanta Workforce | Workforce Hours Export", "workforce hours export"),
            ("cross-month-timesheet-records", "Vanta Workforce | Cross-Month Timesheet Records", "cross-month timesheets"),
            ("attendance-history-app", "Vanta Workforce | Attendance History App", "attendance history"),
        ],
    },
    {
        "id": "operations",
        "name": "Workplace operations",
        "leader": "workforce-management-app",
        "pages": [
            ("workforce-management-app", "Vanta Workforce | Workforce Management App", "workforce management"),
            ("site-management-app", "Vanta Workforce | Site Management App", "site management"),
            ("workplace-management-app", "Vanta Workforce | Workplace Management App", "workplace management"),
            ("manager-and-worker-app", "Vanta Workforce | Manager and Worker App", "manager and worker roles"),
            ("business-attendance-app", "Vanta Workforce | Business Attendance App", "business attendance"),
            ("staff-operations-app", "Vanta Workforce | Staff Operations App", "staff operations"),
            ("workforce-records-app", "Vanta Workforce | Workforce Records App", "workforce records"),
            ("android-ios-workforce-app", "Vanta Workforce | Android and iOS Workforce App", "Android and iOS workforce app"),
        ],
    },
    {
        "id": "scheduling",
        "name": "Staff scheduling and rotas",
        "leader": "staff-scheduling-app",
        "pages": [
            ("staff-scheduling-app", "Vanta Workforce | Staff Scheduling App", "staff scheduling app"),
            ("employee-scheduling-app", "Vanta Workforce | Employee Scheduling App", "employee scheduling app"),
            ("shift-scheduling-app", "Vanta Workforce | Shift Scheduling App", "shift scheduling app"),
            ("staff-rota-app", "Vanta Workforce | Staff Rota App", "staff rota app"),
            ("employee-rota-app", "Vanta Workforce | Employee Rota App", "employee rota app"),
            ("rota-management-app", "Vanta Workforce | Rota Management App", "rota management app"),
            ("employee-work-schedule-app", "Vanta Workforce | Employee Work Schedule App", "employee work schedule app"),
            ("staff-shift-planner", "Vanta Workforce | Staff Shift Planner", "staff shift planner"),
            ("multi-site-staff-scheduling", "Vanta Workforce | Multi-Site Staff Scheduling", "multi-site staff scheduling"),
            ("workplace-shift-scheduling", "Vanta Workforce | Workplace Shift Scheduling", "workplace shift scheduling"),
        ],
    },
]

guides = [
    ("how-staff-attendance-apps-work", "How Staff Attendance Apps Work", "attendance"),
    ("choosing-a-staff-attendance-system", "Choosing a Staff Attendance System", "attendance"),
    ("attendance-app-vs-paper-register", "Attendance App vs Paper Register", "attendance"),
    ("how-to-introduce-digital-attendance", "How to Introduce Digital Attendance", "attendance"),
    ("how-mobile-clock-in-works", "How Mobile Clock-In Works", "clocking"),
    ("how-to-improve-clock-in-accuracy", "How to Improve Clock-In Accuracy", "clocking"),
    ("how-gps-clock-in-works", "How GPS Clock-In Works", "gps-attendance"),
    ("employee-location-privacy", "Employee Location Privacy", "gps-attendance"),
    ("what-to-do-when-clock-in-location-fails", "What to Do When Clock-In Location Fails", "gps-attendance"),
    ("how-to-improve-timesheet-accuracy", "How to Improve Timesheet Accuracy", "timesheets"),
    ("how-to-track-working-hours", "How to Track Working Hours", "timesheets"),
    ("how-overnight-shifts-affect-timesheets", "How Overnight Shifts Affect Timesheets", "timesheets"),
    ("how-monthly-attendance-periods-work", "How Monthly Attendance Periods Work", "timesheets"),
    ("how-to-manage-mobile-workers", "How to Manage Mobile Workers", "mobile-workforces"),
    ("how-worker-safety-checks-work", "How Worker Safety Checks Work", "worker-safety"),
    ("how-scheduled-worker-prompts-work", "How Scheduled Worker Prompts Work", "worker-safety"),
    ("how-to-report-a-workplace-incident", "How to Report a Workplace Incident", "worker-safety"),
    ("how-managers-monitor-workforce-status", "How Managers Monitor Workforce Status", "control-centre"),
    ("how-to-export-timesheet-records", "How to Export Timesheet Records", "reporting"),
    ("troubleshooting-mobile-attendance", "Troubleshooting Mobile Attendance", "operations"),
    ("how-to-create-a-staff-rota", "How to Create a Staff Rota", "scheduling"),
    ("how-employee-shift-scheduling-works", "How Employee Shift Scheduling Works", "scheduling"),
    ("staff-scheduling-vs-spreadsheets", "Staff Scheduling vs Spreadsheets", "scheduling"),
    ("how-to-schedule-staff-across-multiple-workplaces", "How to Schedule Staff Across Multiple Workplaces", "scheduling"),
]

pages = [
    {
        "path": "/workforce/",
        "slug": "",
        "title": "Vanta Workforce | Staff Scheduling, Attendance & Timesheets",
        "type": "homepage",
        "cluster": "homepage",
        "cluster_name": "Vanta Workforce",
        "cluster_leader": "/workforce/",
        "intent": "staff scheduling, rotas, attendance, timesheets and workforce management",
    }
]

for cluster in clusters:
    leader_path = f"/workforce/{cluster['leader']}/"
    for slug, title, intent in cluster["pages"]:
        pages.append(
            {
                "path": f"/workforce/{slug}/",
                "slug": slug,
                "title": title,
                "type": "cluster_leader" if slug == cluster["leader"] else "commercial",
                "cluster": cluster["id"],
                "cluster_name": cluster["name"],
                "cluster_leader": leader_path,
                "intent": intent,
            }
        )

for slug, heading, cluster_id in guides:
    cluster = next(item for item in clusters if item["id"] == cluster_id)
    pages.append(
        {
            "path": f"/workforce/guides/{slug}/",
            "slug": f"guides/{slug}",
            "title": f"Vanta Workforce Guide | {heading}",
            "type": "guide",
            "cluster": cluster_id,
            "cluster_name": cluster["name"],
            "cluster_leader": f"/workforce/{cluster['leader']}/",
            "intent": heading.lower(),
        }
    )

paths = [page["path"] for page in pages]
titles = [page["title"] for page in pages]

duplicate_paths = sorted(path for path, count in Counter(paths).items() if count > 1)
duplicate_titles = sorted(title for title, count in Counter(titles).items() if count > 1)

if len(pages) < 2:
    raise SystemExit(f"Expected a homepage plus supporting pages, found {len(pages)}")

if duplicate_paths:
    raise SystemExit(f"Duplicate paths: {duplicate_paths}")

if duplicate_titles:
    raise SystemExit(f"Duplicate titles: {duplicate_titles}")

payload = {
    "product": "Vanta Workforce",
    "base_path": "/workforce/",
    "locale": "en-GB",
    "status": "local-planning-only",
    "store_links": {
        "android": None,
        "ios": None,
        "note": "No confirmed Vanta Workforce store URLs found during repository inspection.",
    },
    "page_count": len(pages),
    "clusters": [
        {
            "id": cluster["id"],
            "name": cluster["name"],
            "leader": f"/workforce/{cluster['leader']}/",
            "page_count": len(cluster["pages"])
            + sum(1 for _, _, cluster_id in guides if cluster_id == cluster["id"]),
        }
        for cluster in clusters
    ],
    "pages": pages,
}

OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print(f"Created: {OUTPUT}")
print(f"Total planned HTML pages: {len(pages)}")
print(f"Homepage pages: {sum(page['type'] == 'homepage' for page in pages)}")
print(f"Cluster leaders: {sum(page['type'] == 'cluster_leader' for page in pages)}")
print(f"Commercial/supporting pages: {sum(page['type'] == 'commercial' for page in pages)}")
print(f"Guide pages: {sum(page['type'] == 'guide' for page in pages)}")
print(f"Duplicate paths: {len(duplicate_paths)}")
print(f"Duplicate titles: {len(duplicate_titles)}")

print("\nCluster totals:")
for cluster in payload["clusters"]:
    print(f"- {cluster['name']}: {cluster['page_count']}")
