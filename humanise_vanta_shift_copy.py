from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "vanta-shift"

PLAN = json.loads(
    (ROOT / "vanta_shift_page_plan.json").read_text(
        encoding="utf-8"
    )
)

PAGES = PLAN["pages"]

CLUSTER_LABELS = {
    "shift-calendar": "Shift calendar",
    "rota-viewing": "Your rota",
    "notifications": "Shift reminders",
    "hours": "Scheduled hours",
    "earnings": "Estimated pay",
    "shift-patterns": "Shift patterns",
    "common-patterns": "Common rotas",
    "night-shifts": "Night shifts",
    "workers": "For shift workers",
    "guides": "Shift-work guide",
}

LEADS = {
    "shift-calendar": (
        "See your assigned shifts in one clear calendar, so it is easier "
        "to check when you are working and what comes next."
    ),
    "rota-viewing": (
        "Keep your personal rota close at hand instead of relying on "
        "screenshots, paper copies or old messages."
    ),
    "notifications": (
        "Use upcoming-shift reminders to reduce the chance of losing "
        "track of an early start, late finish or changed working day."
    ),
    "hours": (
        "Review the hours currently scheduled in your rota and get a "
        "clearer view of how the week or month is adding up."
    ),
    "earnings": (
        "Estimate what your scheduled shifts may pay, using the rate and "
        "shift information entered in the app."
    ),
    "shift-patterns": (
        "Lay out a repeating shift pattern in a calendar that is easier "
        "to understand than counting days forward by hand."
    ),
    "common-patterns": (
        "Set out a familiar rotating rota and see how working days and "
        "rest days fall across the weeks ahead."
    ),
    "night-shifts": (
        "Keep night work visible in your personal calendar, including "
        "shifts that cross midnight or run into the following day."
    ),
    "workers": (
        "Give shift workers a clearer personal view of upcoming work, "
        "scheduled hours and estimated earnings."
    ),
    "guides": (
        "Practical guidance for understanding rotas, repeating patterns, "
        "scheduled hours and estimated pay."
    ),
}

DESCRIPTIONS = {
    "shift-calendar": (
        "View assigned shifts in a clear personal calendar with Vanta Shift."
    ),
    "rota-viewing": (
        "Keep your personal work rota available in one clear mobile view."
    ),
    "notifications": (
        "Receive reminders about relevant upcoming assigned shifts."
    ),
    "hours": (
        "Review scheduled weekly and monthly hours from your personal rota."
    ),
    "earnings": (
        "Estimate pay from scheduled shifts and the rate information entered."
    ),
    "shift-patterns": (
        "View repeating shift patterns in a clear personal calendar."
    ),
    "common-patterns": (
        "Lay out common rotating rotas and see upcoming work and rest days."
    ),
    "night-shifts": (
        "Keep overnight and night shifts clear in your personal work calendar."
    ),
    "workers": (
        "View personal shifts, reminders, scheduled hours and estimated pay."
    ),
    "guides": (
        "Practical guidance for rotas, shift patterns, hours and estimated pay."
    ),
}

HEADINGS = {
    "shift-calendar": [
        "See the working month without hunting for the rota",
        "A clearer view of when you are actually working",
        "Keep the next shift easy to find",
        "Put your assigned shifts into one useful calendar",
        "See working days and rest days at a glance",
        "Make the rota easier to check on a busy week",
        "Keep your personal schedule somewhere dependable",
        "A shift calendar built around your own working time",
        "Stop piecing the month together from old messages",
        "Know what is coming before the working week begins",
    ],
    "rota-viewing": [
        "Keep your rota close without carrying the paper copy",
        "A personal rota that is easier to check",
        "See your own shifts without the surrounding clutter",
        "Keep the latest schedule in one clear view",
        "Make the work rota easier to live with",
        "Check the week without scrolling through old chats",
        "Your own rota, laid out properly",
        "A simpler way to look ahead at work",
        "Keep working days and times easy to find",
        "Give your personal schedule a permanent home",
    ],
    "notifications": [
        "Get a reminder before the shift starts",
        "Keep early starts from sneaking up on you",
        "A useful nudge when the next shift is getting close",
        "Use reminders without filling the phone with noise",
        "Keep upcoming work in mind",
        "Make shift alerts work around the rota",
        "A small reminder can prevent a big scramble",
        "Know when the next working day is approaching",
        "Keep unusual starts and finishes easier to remember",
        "Let the calendar do some of the remembering",
    ],
    "hours": [
        "See how the scheduled hours are adding up",
        "Keep a clearer eye on the working week",
        "Understand the hours currently sitting in your rota",
        "Review weekly and monthly totals without counting by hand",
        "Turn a busy rota into a useful hours total",
        "See the shape of the month before it is over",
        "Keep scheduled time easier to understand",
        "Check whether the rota looks lighter or heavier than usual",
        "A clearer total for the hours you are due to work",
        "Know what the current schedule adds up to",
    ],
    "earnings": [
        "Get a sensible estimate from the shifts in your calendar",
        "See what the scheduled month may be worth",
        "Turn planned hours into a useful pay estimate",
        "Keep expected earnings easier to understand",
        "Estimate pay without pretending it is payroll",
        "See how different shifts affect the month",
        "Use the rota to plan ahead financially",
        "A practical estimate for the work currently scheduled",
        "Understand the link between shifts, hours and pay",
        "Keep estimated earnings alongside the rota",
    ],
    "shift-patterns": [
        "Make a repeating rota easier to understand",
        "See where the pattern leads over the weeks ahead",
        "Stop counting working days forward by hand",
        "Put the rotation into a calendar you can actually read",
        "See how the pattern falls across the month",
        "Keep repeating shifts clear beyond the current week",
        "Turn the rota cycle into visible working days",
        "Understand the rhythm of the shift pattern",
        "Look further ahead without rebuilding the rota each time",
        "Make rotating work feel less unpredictable",
    ],
    "common-patterns": [
        "Lay out a familiar rota without doing the date maths",
        "See the full cycle of work days and rest days",
        "Make a common shift pattern useful on your own calendar",
        "Look ahead through the next rotation",
        "Keep the working cycle easy to recognise",
        "Put a standard rota into a personal view",
        "See how the cycle crosses weeks and months",
        "Understand where you are in the rotation",
        "Keep the pattern clear when the dates change",
        "A more useful view of a repeating rota",
    ],
    "night-shifts": [
        "Keep overnight work clear in the calendar",
        "See where the night shift begins and ends",
        "Make shifts across midnight easier to follow",
        "Keep nights and recovery days visible",
        "Understand how overnight work shapes the week",
        "Put late starts and next-day finishes in context",
        "A clearer calendar for working through the night",
        "See night work without squeezing it into one date",
        "Keep the overnight rota easier to plan around",
        "Know how night shifts fall across the month",
    ],
    "workers": [
        "A personal rota view for people who work shifts",
        "Keep work, hours and estimated pay together",
        "Make an irregular schedule easier to live around",
        "A clearer personal calendar for shift work",
        "See the job from your own side of the rota",
        "Keep upcoming work easy to check",
        "Plan around shifts without managing the whole workplace",
        "A simple view of the work assigned to you",
        "Keep personal working time organised",
        "Understand the month from an employee’s point of view",
    ],
    "guides": [
        "Start with the rota you actually work",
        "Make the schedule easier to understand before adding detail",
        "Check the pattern, then look further ahead",
        "Use hours and pay estimates as planning tools",
        "Keep the calendar accurate enough to be useful",
        "Review unusual shifts before relying on the totals",
        "Treat reminders as support, not the official rota",
        "Make overnight work clear across both dates",
        "Keep rates and shift times up to date",
        "Use the app to understand the schedule, not prove attendance",
    ],
}

OPENERS = [
    (
        "Shift work becomes harder to plan around when the rota is spread "
        "across screenshots, paper copies and old messages."
    ),
    (
        "A working rota may make sense at a glance in the workplace, but "
        "it is not always convenient when you are trying to plan your own time."
    ),
    (
        "The useful question is usually simple: when am I working next, "
        "and what does the rest of the week look like?"
    ),
    (
        "Rotating work can make ordinary plans surprisingly difficult when "
        "the next few weeks are not laid out clearly."
    ),
    (
        "A personal shift calendar should remove uncertainty rather than "
        "add another complicated system."
    ),
    (
        "Most employees do not need a management dashboard. They need a "
        "dependable view of the shifts assigned to them."
    ),
    (
        "The schedule is easier to live with when working days, rest days "
        "and unusual start times are visible together."
    ),
    (
        "Checking the rota should take a few seconds, not a search through "
        "several conversations and attachments."
    ),
    (
        "A clear calendar can make it easier to plan family time, travel, "
        "sleep and the rest of life around work."
    ),
    (
        "The app is most useful when it stays focused on the employee’s own "
        "schedule instead of trying to run the workplace."
    ),
]

CLUSTER_PARAGRAPHS = {
    "shift-calendar": [
        "Vanta Shift puts assigned work into a personal calendar, making the next shift and the wider month easier to see.",
        "Working days appear together in one view so you can check the schedule without reconstructing it from separate notes.",
        "The calendar keeps attention on the shifts assigned to you rather than the schedules of the wider team.",
        "You can look ahead through the month and see where work sits alongside rest days and personal plans.",
        "A personal calendar is especially useful when start times or working days change from week to week.",
        "The app gives each assigned shift a clear place instead of leaving the rota as a block of text or a photo.",
        "It becomes easier to answer ordinary questions such as whether you are working next weekend or finishing late.",
        "The view is designed for quick checks as well as planning further ahead.",
        "Scheduled shifts stay connected to hours, reminders and estimated pay elsewhere in the app.",
        "The calendar remains a planning view based on the information entered or assigned to it.",
    ],
    "rota-viewing": [
        "Vanta Shift keeps your personal rota available on the phone so it is easier to check away from work.",
        "The app strips the schedule back to the shifts that matter to you.",
        "A clear rota view can be easier to read than a large workplace spreadsheet containing every employee.",
        "You can check dates, times and upcoming working days without zooming into a screenshot.",
        "The rota remains centred on personal planning rather than workplace control.",
        "Keeping the schedule in one place can reduce confusion when several versions have been shared.",
        "The app helps turn an awkward rota format into a calendar that works better on a mobile screen.",
        "It is useful for looking ahead before making appointments or family plans.",
        "The personal view does not change the employer’s official rota or create attendance records.",
        "Vanta Shift is there to help the employee understand the schedule they have been given.",
    ],
    "notifications": [
        "Vanta Shift can remind you about relevant upcoming shifts using the schedule held in the app.",
        "A notification is particularly useful when a start time is unusual or the rota changes frequently.",
        "Reminders can reduce the need to keep reopening the calendar just to check tomorrow’s shift.",
        "The feature is intended to provide a timely nudge rather than constant alerts.",
        "Whether an alert appears also depends on the notification settings and behaviour of the device.",
        "Shift reminders work best when the rota in the app is accurate and up to date.",
        "An alert can help with early starts, night work and patterns where working days move each week.",
        "The notification supports the schedule but does not replace checking the official rota.",
        "Employees can use reminders as one more layer of planning around assigned work.",
        "The goal is simple: make the next shift a little harder to forget.",
    ],
    "hours": [
        "Vanta Shift totals the hours currently scheduled in the personal rota.",
        "Weekly and monthly totals can make a busy pattern easier to understand.",
        "The hours view saves repeatedly adding shift lengths by hand.",
        "Scheduled totals can help when comparing one week or month with another.",
        "The figure reflects planned work rather than proof of time actually completed.",
        "Breaks, overtime rules and payroll treatment may affect the hours recognised elsewhere.",
        "A visible total can make it easier to spot when a shift is missing or entered incorrectly.",
        "Employees can use the figure for personal planning before receiving an official timesheet or payslip.",
        "The value is strongest when shift times and durations are kept accurate.",
        "Hours sit alongside the calendar so the schedule and its total can be understood together.",
    ],
    "earnings": [
        "Vanta Shift uses the shifts and rate information available in the app to produce an estimated figure.",
        "The estimate can help you understand how a heavier or lighter rota may affect the month.",
        "It is a planning tool rather than a payroll calculation.",
        "Actual pay may differ because of deductions, overtime rules, premiums, unpaid breaks or employer policies.",
        "Keeping rate information current makes the estimate more useful.",
        "The feature can show how scheduled hours translate into a rough gross-pay expectation.",
        "Employees can compare upcoming periods without waiting until the payslip arrives.",
        "Different shift lengths or rates can make the estimate change across the month.",
        "The figure should be treated as guidance, especially where pay arrangements are complicated.",
        "Estimated earnings remain connected to the personal rota rather than workplace payroll records.",
    ],
    "shift-patterns": [
        "Vanta Shift can lay a repeating work cycle across future dates in a personal calendar.",
        "The pattern makes it easier to see which part of the rotation falls on a particular week.",
        "A visible cycle can remove the need to count work days and rest days forward manually.",
        "The schedule becomes more useful when the correct starting point and pattern are entered.",
        "Rotating work often crosses calendar months, so seeing the cycle beyond the current page matters.",
        "The app can help with planning appointments, family events and time away from work.",
        "Patterns are personal planning tools and should still be checked against the employer’s official rota.",
        "A repeating cycle can be adjusted when the real schedule changes.",
        "The calendar helps turn an abstract pattern into actual dates.",
        "The result is a clearer sense of where work and rest days land over time.",
    ],
    "common-patterns": [
        "Many workplaces use familiar repeating cycles, but employees still need to see how the pattern lands on real dates.",
        "Vanta Shift places the cycle into a personal calendar rather than leaving it as a pattern name.",
        "The correct start date is important because the same rotation can produce a very different calendar when offset.",
        "Seeing the whole cycle can make rest days and weekends easier to plan around.",
        "Patterns may continue across month boundaries without restarting on the first day of the month.",
        "The app helps the employee understand the dates created by the chosen rotation.",
        "Real workplace changes should always be reflected in the personal schedule.",
        "The pattern does not override a rota issued by an employer.",
        "A familiar cycle becomes more useful once it is shown alongside hours and estimated pay.",
        "The aim is to make repeating work predictable enough for personal planning.",
    ],
    "night-shifts": [
        "Night work often starts on one date and finishes on the next, which can make simple calendars misleading.",
        "Vanta Shift keeps the start and finish of an overnight shift in the wider context of the schedule.",
        "Seeing nights clearly can help when planning sleep, travel and recovery time.",
        "The calendar can show how several consecutive nights affect the rest of the week.",
        "Hours and estimated pay remain based on the shift information entered into the app.",
        "Overnight work should be checked carefully where breaks or premium rates apply.",
        "A clear date view can reduce confusion about whether a shift belongs to the evening it starts or the morning it ends.",
        "Night patterns may also affect which days appear as working or resting days.",
        "The app is intended to make those patterns easier for the employee to understand.",
        "It does not create attendance evidence or confirm that an overnight shift was completed.",
    ],
    "workers": [
        "Vanta Shift is built around the employee’s own assigned work.",
        "It combines a personal calendar with reminders, scheduled hours and estimated earnings.",
        "The app does not provide manager dashboards or workplace attendance control.",
        "That narrower focus keeps the experience relevant to somebody checking their own rota.",
        "Employees can use it to look ahead before arranging family time, appointments or travel.",
        "The schedule is useful across jobs where working days and hours vary.",
        "A clear personal view can reduce the friction caused by large or awkward rota formats.",
        "The app supports planning but does not replace official workplace information.",
        "Scheduled hours and pay estimates remain guidance based on the data available.",
        "Everything stays centred on understanding personal working time.",
    ],
    "guides": [
        "Start by making sure the shifts in the app match the rota you have actually been given.",
        "A simple accurate calendar is more useful than a detailed one built from outdated information.",
        "Check the starting point carefully before extending a repeating pattern into future weeks.",
        "Treat scheduled-hour totals as planned time rather than proof of time worked.",
        "Estimated pay is most useful when rates and shift lengths are kept current.",
        "Review overnight shifts carefully so the start and finish dates make sense.",
        "Device notification settings can affect whether upcoming-shift reminders appear.",
        "Use the official rota as the final source when workplace information conflicts.",
        "Update unusual changes rather than assuming the repeating pattern will always continue unchanged.",
        "The purpose of Vanta Shift is to make your personal schedule easier to understand and plan around.",
    ],
}

NOTICES = {
    "shift-calendar": (
        "The calendar is a personal planning view and should still be checked "
        "against the official rota supplied by the employer."
    ),
    "rota-viewing": (
        "Vanta Shift does not change the official workplace rota or prove "
        "that a scheduled shift was completed."
    ),
    "notifications": (
        "Shift reminders depend on the schedule in the app and the notification "
        "settings on the device."
    ),
    "hours": (
        "Scheduled hours are planning figures and may differ from paid hours "
        "or an employer’s official timesheet."
    ),
    "earnings": (
        "Estimated pay may differ from actual pay because of deductions, "
        "breaks, overtime, premiums and payroll rules."
    ),
    "shift-patterns": (
        "Repeating patterns should be checked against real rota changes issued "
        "by the employer."
    ),
    "common-patterns": (
        "A named shift pattern does not guarantee that every workplace uses "
        "the same times or rules."
    ),
    "night-shifts": (
        "Overnight shifts may be treated differently by payroll, overtime or "
        "premium-rate rules."
    ),
    "workers": (
        "Vanta Shift is employee-facing and does not provide attendance "
        "tracking, clocking-in or manager oversight."
    ),
    "guides": (
        "Use employer-issued rota, payroll and workplace information as the "
        "final source where it differs from the app."
    ),
}

FAQS = {
    "shift-calendar": [
        (
            "What appears in the shift calendar?",
            "The calendar shows the assigned shifts and working dates held in Vanta Shift.",
        ),
        (
            "Does the calendar prove that a shift was worked?",
            "No. It represents scheduled work and is not an attendance record.",
        ),
        (
            "Should I still check the official rota?",
            "Yes. Employer-issued rota information should remain the final source.",
        ),
    ],
    "rota-viewing": [
        (
            "Is Vanta Shift a manager rota system?",
            "No. It is focused on the employee viewing their own assigned shifts.",
        ),
        (
            "Can I use it away from work?",
            "Yes. The personal rota is designed to be convenient to check on a phone.",
        ),
        (
            "Does it replace the official workplace rota?",
            "No. It supports personal planning but does not replace employer-issued information.",
        ),
    ],
    "notifications": [
        (
            "Can Vanta Shift remind me about an upcoming shift?",
            "Yes. It can provide reminders about relevant upcoming assigned shifts.",
        ),
        (
            "Why might a reminder not appear?",
            "The rota data and the device’s notification permissions and settings can affect alerts.",
        ),
        (
            "Should I rely only on a notification?",
            "No. Employees should still check their personal calendar and official rota.",
        ),
    ],
    "hours": [
        (
            "What do scheduled hours represent?",
            "They total the working time currently planned in the personal rota.",
        ),
        (
            "Are scheduled hours the same as paid hours?",
            "Not always. Breaks, overtime and employer rules may affect the official figure.",
        ),
        (
            "Can I review both weekly and monthly totals?",
            "Yes. Vanta Shift can present scheduled-hour totals across relevant periods.",
        ),
    ],
    "earnings": [
        (
            "Is estimated pay the same as my payslip?",
            "No. It is a personal planning estimate based on the information available in the app.",
        ),
        (
            "Why could actual pay be different?",
            "Deductions, breaks, overtime, premiums and payroll rules may change the final amount.",
        ),
        (
            "What makes the estimate more useful?",
            "Accurate shift times and up-to-date rate information improve the estimate.",
        ),
    ],
    "shift-patterns": [
        (
            "Can Vanta Shift show a repeating rota?",
            "Yes. A repeating pattern can be laid across future dates in the personal calendar.",
        ),
        (
            "Why does the pattern need a correct starting point?",
            "The starting point determines where working and rest days land on actual dates.",
        ),
        (
            "Should pattern dates be checked against work?",
            "Yes. Real rota changes issued by the employer should always take priority.",
        ),
    ],
    "common-patterns": [
        (
            "Do all workplaces use named patterns in the same way?",
            "No. Shift times, start points and local rules can vary between employers.",
        ),
        (
            "Can I see future dates in the rotation?",
            "Yes. The pattern can be shown across future weeks and months.",
        ),
        (
            "Does the pattern override a changed rota?",
            "No. Employer-issued changes should be reflected in the personal calendar.",
        ),
    ],
    "night-shifts": [
        (
            "Can Vanta Shift show a shift that crosses midnight?",
            "Yes. Overnight work can be represented across its start and finish dates.",
        ),
        (
            "Are night premiums included automatically?",
            "Only where the relevant rate information has been entered and the estimate supports it.",
        ),
        (
            "Does the calendar prove the night shift was completed?",
            "No. It remains a scheduled personal planning view.",
        ),
    ],
    "workers": [
        (
            "Who is Vanta Shift designed for?",
            "It is designed for employees viewing their own assigned shifts, reminders, hours and estimated pay.",
        ),
        (
            "Does it include workplace attendance tracking?",
            "No. Vanta Shift does not provide clocking-in, booking-on or manager attendance oversight.",
        ),
        (
            "Can it help with personal planning?",
            "Yes. The calendar can make it easier to plan life around upcoming shifts.",
        ),
    ],
    "guides": [
        (
            "What information should I check first?",
            "Start with the official rota, correct shift times and the right point in any repeating pattern.",
        ),
        (
            "Are hours and earnings official records?",
            "No. They are personal planning figures based on the information available in the app.",
        ),
        (
            "What happens when the workplace rota changes?",
            "The personal calendar should be updated so it continues to reflect the real schedule.",
        ),
    ],
}


def page_file(page: dict) -> Path:
    if page["path"] == "/vanta-shift/":
        return SITE / "index.html"

    slug = page["path"].removeprefix("/vanta-shift/").strip("/")
    return SITE / slug / "index.html"


def replace_once(
    text: str,
    pattern: str,
    replacement: str,
    label: str,
) -> str:
    updated, count = re.subn(
        pattern,
        replacement,
        text,
        count=1,
        flags=re.I | re.S,
    )

    if count != 1:
        raise RuntimeError(
            f"{label}: expected one match, found {count}"
        )

    return updated


def update_schema(
    text: str,
    page: dict,
    description: str,
    faqs: list[tuple[str, str]],
) -> str:
    pattern = re.compile(
        r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)',
        re.I | re.S,
    )

    def replacement(match: re.Match[str]) -> str:
        data = json.loads(match.group(2))

        def visit(value: object) -> None:
            if isinstance(value, list):
                for item in value:
                    visit(item)
                return

            if not isinstance(value, dict):
                return

            schema_type = value.get("@type")

            if schema_type in {
                "SoftwareApplication",
                "Article",
            }:
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
                    for question, answer in faqs
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


def human_copy(page: dict) -> dict:
    cluster = page["cluster"]
    position = int(page.get("position", 1))
    index = (position - 1) % 10

    heading = HEADINGS[cluster][index]
    first = f"{OPENERS[index]} {CLUSTER_PARAGRAPHS[cluster][index]}"

    second_by_cluster = {
        "shift-calendar": (
            "The calendar remains centred on your own assigned work, making "
            "it useful for personal planning without becoming a workplace "
            "management tool."
        ),
        "rota-viewing": (
            "It gives the employee a cleaner way to understand the rota they "
            "have been given while leaving workplace control with the employer."
        ),
        "notifications": (
            "Used alongside the calendar and official rota, the reminder can "
            "make unusual or changing shift times easier to keep in mind."
        ),
        "hours": (
            "The total is there to help with personal planning and should not "
            "be treated as an official timesheet or payroll record."
        ),
        "earnings": (
            "It can be useful for planning ahead, but the final payslip may "
            "differ for several legitimate payroll reasons."
        ),
        "shift-patterns": (
            "Once the cycle is visible on real dates, it becomes much easier "
            "to plan the rest of life around working and rest days."
        ),
        "common-patterns": (
            "The chosen pattern should match the employee’s real arrangement "
            "and be updated whenever the workplace rota changes."
        ),
        "night-shifts": (
            "The clearer date view can help the employee understand where "
            "overnight work sits in the week without treating it as attendance proof."
        ),
        "workers": (
            "That employee-only focus is what separates Vanta Shift from "
            "workforce attendance or management software."
        ),
        "guides": (
            "Vanta Shift can make the information easier to understand, but "
            "official rota and payroll records should remain the final source."
        ),
    }

    return {
        "heading": heading,
        "paragraph_one": first,
        "paragraph_two": second_by_cluster[cluster],
        "notice": NOTICES[cluster],
        "lead": LEADS[cluster],
        "description": DESCRIPTIONS[cluster],
        "faqs": FAQS[cluster],
    }


changed = 0

for page in PAGES:
    file = page_file(page)

    if not file.is_file():
        raise FileNotFoundError(file)

    text = file.read_text(encoding="utf-8")

    if page["path"] == "/vanta-shift/":
        text = replace_once(
            text,
            r'<p class="lead">.*?</p>',
            '''<p class="lead">
Keep your assigned shifts, upcoming reminders, scheduled hours and
estimated pay together in one clear personal view.
</p>''',
            f"{file}: home lead",
        )

        text = replace_once(
            text,
            r'<section class="long-copy">.*?</section>',
            '''<section class="long-copy">
<h2>Your own work schedule, made easier to live around</h2>

<div class="long-copy-text">
<p>
Vanta Shift is for employees who want a clearer view of their own rota.
Assigned shifts sit in a personal calendar, making it easier to check
the next working day, look ahead through the month and plan the rest of
life around work.
</p>

<p>
The same schedule can be used for upcoming-shift reminders, scheduled
hour totals and estimated earnings. These are personal planning tools,
not attendance records, manager controls or official payroll figures.
</p>
</div>
</section>''',
            f"{file}: home article",
        )

        file.write_text(text, encoding="utf-8")
        changed += 1
        continue

    copy = human_copy(page)

    text = replace_once(
        text,
        r'<p class="lead">.*?</p>',
        f'<p class="lead">\n{html.escape(copy["lead"])}\n</p>',
        f"{file}: lead",
    )

    description = html.escape(
        copy["description"],
        quote=True,
    )

    text = replace_once(
        text,
        r'(<meta\s+name="description"\s+content=")[^"]*("\s*/>)',
        rf'\g<1>{description}\g<2>',
        f"{file}: description",
    )

    text = replace_once(
        text,
        r'(<meta\s+property="og:description"\s+content=")[^"]*("\s*/>)',
        rf'\g<1>{description}\g<2>',
        f"{file}: og description",
    )

    article = f'''<section class="long-copy">
<h2>{html.escape(copy["heading"])}</h2>

<div class="long-copy-text">
<p>{html.escape(copy["paragraph_one"])}</p>
<p>{html.escape(copy["paragraph_two"])}</p>
</div>
</section>'''

    text = replace_once(
        text,
        r'<section class="long-copy">.*?</section>',
        article,
        f"{file}: article",
    )

    notice = f'''<div class="notice">
<strong>Keep the official rota as the final source.</strong>
{html.escape(copy["notice"])}
</div>'''

    text = replace_once(
        text,
        r'<div class="notice">.*?</div>',
        notice,
        f"{file}: notice",
    )

    faq_html = "\n".join(
        f'''<details>
<summary>{html.escape(question)}</summary>
<p>{html.escape(answer)}</p>
</details>'''
        for question, answer in copy["faqs"]
    )

    text = replace_once(
        text,
        r'(<section class="faq">\s*<h2>Quick questions</h2>).*?(</section>)',
        rf'\1\n{faq_html}\n\2',
        f"{file}: FAQ",
    )

    text = update_schema(
        text,
        page,
        copy["description"],
        copy["faqs"],
    )

    file.write_text(text, encoding="utf-8")
    changed += 1

print(f"Humanised Vanta Shift pages: {changed}")
