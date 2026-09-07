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
PLAN_PATH = ROOT / "parent_quest_page_plan.json"

plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
pages = plan["pages"]

page_by_path = {page["path"]: page for page in pages}

CLUSTER_LABELS = {
    "chore-charts": "Chore charts",
    "daily-chores": "Daily chores",
    "kids-tasks": "Kids tasks",
    "family-routines": "Family routines",
    "rewards": "Rewards",
    "coins": "Reward coins",
    "parent-approval": "Parent approval",
    "child-profiles": "Child profiles",
    "parent-device": "Parent device",
    "guides": "Parent guide",
}

HEADINGS = {
    "chore-charts": [
        "A chore chart the family can actually use",
        "Keep everyday jobs clear without overcomplicating them",
        "Put the week’s chores somewhere everyone can see",
        "A simpler way to keep household jobs organised",
        "Make the chore list easier to follow",
        "Turn scattered jobs into one clear routine",
        "Give each child a clear view of what needs doing",
        "Keep chores visible, simple and manageable",
        "A practical chore chart for ordinary family life",
        "Less nagging, more clarity around daily jobs",
    ],
    "daily-chores": [
        "Make daily jobs easier to remember",
        "Keep the everyday routine from becoming a scramble",
        "Put regular chores in one dependable place",
        "A clearer rhythm for the jobs that happen every day",
        "Help children see what needs doing today",
        "Keep repeated tasks simple and visible",
        "Build a daily routine the family can stick to",
        "Organise everyday chores without filling the fridge with notes",
        "Give regular household jobs a proper place",
        "A calmer way to handle the daily checklist",
    ],
    "kids-tasks": [
        "Give children a task list they can understand",
        "Keep children’s jobs clear and age appropriate",
        "Make the next task easy to see",
        "Turn vague reminders into clear, manageable jobs",
        "Keep personal task lists simple",
        "Help each child know what belongs to them",
        "A straightforward way to organise children’s tasks",
        "Put household expectations into plain language",
        "Make family jobs easier to explain and follow",
        "Keep tasks clear without turning home into a workplace",
    ],
    "family-routines": [
        "Build a routine that fits real family life",
        "Make repeated jobs feel less chaotic",
        "Give the household a rhythm everyone recognises",
        "Keep family routines clear without making them rigid",
        "Bring chores and rewards into one familiar routine",
        "A practical way to organise the week",
        "Help everyday routines become easier to repeat",
        "Create structure without making home feel overmanaged",
        "Keep the family routine moving",
        "A simple system for the jobs that keep coming back",
    ],
    "rewards": [
        "Choose rewards that mean something to your family",
        "Keep rewards personal, simple and parent controlled",
        "Connect completed jobs with something worth working towards",
        "Make family rewards feel fair and achievable",
        "Create rewards that suit your own household",
        "Let progress lead to rewards chosen by you",
        "A clearer way to manage chores and rewards together",
        "Keep the reward system flexible",
        "Use rewards without turning every job into a transaction",
        "Build a reward list your children actually care about",
    ],
    "coins": [
        "Use reward coins without pretending they are real money",
        "Give children a simple way to see their progress",
        "Turn completed jobs into visible progress",
        "Keep reward coins clear and parent managed",
        "Help children understand what they are working towards",
        "A simple progress system for family rewards",
        "Use coins as a marker of effort, not cash",
        "Make progress easier to see",
        "Keep the family reward system easy to understand",
        "Let completed chores add up to something meaningful",
    ],
    "parent-approval": [
        "Keep the final say with the parent",
        "Review completed chores before rewards are added",
        "Separate ‘marked done’ from ‘actually checked’",
        "Make approval part of the family routine",
        "Keep progress fair with a quick parent check",
        "Give completed jobs a proper review step",
        "Use the Parent PIN to keep approval adult controlled",
        "Make sure progress is confirmed, not assumed",
        "Keep rewards tied to chores you have actually reviewed",
        "A simple approval step that keeps parents in control",
    ],
    "child-profiles": [
        "Keep each child’s chores separate and easy to follow",
        "Give every child their own clear view",
        "Organise tasks without mixing everyone together",
        "Keep progress personal to each child",
        "Make sibling routines easier to manage",
        "Put each child’s jobs and rewards in the right place",
        "A clearer setup for families with more than one child",
        "Keep chores organised child by child",
        "Make individual progress easier to see",
        "Give each child a routine that belongs to them",
    ],
    "parent-device": [
        "Keep the whole system on the parent’s device",
        "Manage chores and rewards without creating child accounts",
        "A family chore app that stays under parent control",
        "Use one device without handing over the settings",
        "Keep setup, approval and rewards with the adult",
        "A simpler option for families using one shared screen",
        "Manage the routine from the phone you already use",
        "Keep children out of the account settings",
        "Run the family system from a parent-owned device",
        "One place for the parent to manage the whole routine",
    ],
    "guides": [
        "Start small and build a routine that lasts",
        "Keep the first version simple",
        "Choose chores the family can realistically manage",
        "Make the routine clear before making it bigger",
        "Build consistency before adding more rewards",
        "Use a system that suits your own household",
        "Keep expectations realistic and easy to explain",
        "Create a routine children can understand",
        "Review what works and change what does not",
        "Aim for useful, not perfect",
    ],
}

OPENERS = [
    "Family routines rarely fail because parents do not care. They usually fall apart because the system is awkward to keep up with.",
    "A good family routine should make life easier, not create another job for the parent.",
    "Most homes do not need a complicated productivity system. They need a clear answer to who is doing what and when.",
    "Children are more likely to follow a routine when the next job is easy to understand.",
    "The useful part of a chore system is not the chart itself. It is the clarity it gives the family.",
    "Some days run smoothly. Other days need a bit more structure. A clear task list helps on both.",
    "A family routine works best when it is simple enough to use even on busy days.",
    "Parents should not need a spreadsheet to keep track of a few household jobs.",
    "The goal is not to make home feel like work. It is to remove some of the repeated confusion.",
    "A clear routine can cut down on the constant back-and-forth about what still needs doing.",
]

CLUSTER_PARAGRAPHS = {
    "chore-charts": [
        "Parent Quest gives you one place to create chores, assign them to the right child and see what has been marked complete.",
        "You decide which jobs belong on the chart, how often they appear and which child is responsible for them.",
        "The chart stays focused on the jobs your family actually uses rather than forcing you into a fixed template.",
        "Each chore can sit inside a child’s own profile, making it easier to see what belongs to whom.",
        "Instead of relying on paper lists or repeated reminders, the current jobs remain together in one clear view.",
        "You can keep the list short for younger children or build a fuller routine when the family needs it.",
        "The parent stays in control of the setup while children get a much clearer picture of what is expected.",
        "The result is a chore chart that can change with the household rather than becoming another abandoned system.",
        "It is designed for ordinary home routines: bedrooms, dishes, school bags, pet jobs and the other things families choose.",
        "The app keeps the chart practical, visible and tied to the child profiles you create.",
    ],
    "daily-chores": [
        "Use Parent Quest to collect the small, repeated jobs that are otherwise easy to forget or argue about.",
        "Daily chores can be added to the child’s routine so the same expectations do not need to be explained from scratch each day.",
        "The parent chooses what counts as a daily job and can keep the list realistic for the child.",
        "Regular tasks sit alongside the rest of the child’s chores instead of being scattered across notes and messages.",
        "A clear daily list can help mornings, after-school time and evenings feel more predictable.",
        "The app is flexible enough for a handful of essentials rather than an overwhelming list of everything that could be done.",
        "Parents can use the routine as a prompt, while still deciding when a job needs changing, skipping or explaining.",
        "The aim is a dependable rhythm, not perfection every single day.",
        "Children can see the jobs that form part of today’s routine, while the parent keeps control of approval.",
        "When life changes, the list can change with it instead of locking the family into one pattern.",
    ],
    "kids-tasks": [
        "Parent Quest turns broad instructions into individual tasks that are easier for children to understand.",
        "Each child can have a personal list rather than trying to work out which jobs apply to everyone.",
        "The parent writes the task, decides who it belongs to and keeps responsibility for explaining it properly.",
        "Clear task names can reduce the vague reminders that often lead to frustration on both sides.",
        "The app works best with jobs that are specific, realistic and suitable for the child.",
        "Tasks can cover everyday household responsibilities without pretending that every part of family life needs tracking.",
        "Children get a clear next step, while parents keep the wider context and final judgement.",
        "A personal list can be especially useful when siblings have different ages, routines or responsibilities.",
        "The system gives structure without replacing conversation, help or supervision.",
        "Parents can keep the task list focused on what genuinely matters that day or week.",
    ],
    "family-routines": [
        "Parent Quest brings chores, progress and rewards together so the family is not using a different system for each part.",
        "Regular tasks can become familiar parts of the day instead of last-minute instructions.",
        "The parent shapes the routine around the household rather than fitting the family into somebody else’s template.",
        "A repeatable structure can make mornings, after-school time and evenings easier to navigate.",
        "The app gives the routine a home, but the parent still decides when flexibility matters more than the checklist.",
        "Children can learn what normally happens next without the system becoming overly strict.",
        "Rewards can sit alongside the routine when they are useful, rather than becoming compulsory for every job.",
        "A good routine leaves room for busy days, tired children and normal family life.",
        "The goal is to create something recognisable enough to follow and flexible enough to keep using.",
        "Parents can adjust the setup as children grow or the household’s needs change.",
    ],
    "rewards": [
        "Parent Quest lets you create rewards that fit your own children rather than choosing from a generic catalogue.",
        "A reward might be extra screen time, choosing a film, a small treat or anything else the parent considers appropriate.",
        "You decide what rewards are available and how they connect to the progress you have reviewed.",
        "Because every family values different things, the reward list remains fully parent created.",
        "Rewards can recognise effort without turning every ordinary responsibility into a negotiation.",
        "The system works best when expectations are clear and rewards remain achievable.",
        "Parents can change the reward list as children’s interests and family circumstances change.",
        "Nothing is purchased or supplied by Vanta Labs; the reward stays between the parent and child.",
        "Reward coins provide a simple bridge between completed tasks and the rewards the parent has chosen.",
        "The parent keeps the final say over whether progress is approved and whether a reward is suitable.",
    ],
    "coins": [
        "Parent Quest uses reward coins as a simple way to show progress towards family-created rewards.",
        "Coins are added within the parent-managed routine and are not money, credit or anything that can be withdrawn.",
        "The balance helps children see that completed tasks are adding up to a goal chosen by the family.",
        "Parents decide how coins fit into the routine and what the available rewards require.",
        "Because the coins stay inside Parent Quest, they remain part of the household’s own reward system.",
        "The aim is to make progress visible without pretending the app is a bank or payment service.",
        "Parents can keep the values simple so children understand what each completed task contributes.",
        "Reward coins can help with longer-term goals where one completed chore would not normally earn a full reward.",
        "The system remains flexible: families can use coins heavily, lightly or only for selected tasks.",
        "Approval remains important because the parent decides when completed work should count towards the balance.",
    ],
    "parent-approval": [
        "When a child marks something complete, the parent can review it before progress is confirmed.",
        "The Parent PIN helps keep approval away from the child-facing part of the routine.",
        "This gives parents a chance to check the job, talk about it and decide whether it should count.",
        "Approval prevents the app from treating every tap on ‘done’ as the final word.",
        "The step is intentionally simple: the parent reviews the progress and keeps control of the outcome.",
        "Families can use the check as a quick confirmation rather than turning every chore into an inspection.",
        "The Parent PIN should stay private so children cannot approve their own progress.",
        "Approval keeps reward coins connected to work the parent has actually accepted.",
        "It also gives parents room to recognise effort when a task was attempted but needs discussion.",
        "The feature supports the parent’s judgement instead of trying to replace it with automatic rules.",
    ],
    "child-profiles": [
        "Each child can have a separate profile for their own chores, progress and rewards.",
        "Profiles stop sibling tasks from becoming one mixed list that nobody fully understands.",
        "The parent can set different expectations for different ages and routines.",
        "One child may have a short daily checklist while another has a broader weekly set of jobs.",
        "Keeping progress separate makes it easier to review what each child has actually done.",
        "The profiles remain inside the parent-managed family setup rather than becoming independent child accounts.",
        "Names or nicknames can be used so the household recognises each profile quickly.",
        "Parents can organise the routine without entering unnecessary personal information.",
        "Separate profiles can also make rewards feel fairer because progress is not mixed between siblings.",
        "The parent still sees and controls the overall system from the same device.",
    ],
    "parent-device": [
        "Parent Quest is designed to run as a parent-managed family system on a parent-owned device.",
        "Children do not need separate accounts just to see chores or take part in the routine.",
        "The parent keeps control of setup, approval, reward coins and custom rewards.",
        "This can suit families that do not want every child to need their own phone, email address or login.",
        "A shared screen can be used for the child-facing parts while protected actions stay behind the Parent PIN.",
        "The app keeps the important settings with the adult who is responsible for the routine.",
        "Using one device can make the system easier to introduce to younger children.",
        "It also avoids turning a simple chore chart into another collection of family accounts and passwords.",
        "The parent can manage several child profiles from the same place.",
        "The setup remains deliberately straightforward: one family system, controlled by the parent.",
    ],
    "guides": [
        "Begin with a small number of jobs that are easy to explain and realistic to complete.",
        "Choose chores that suit the child’s age, abilities and normal place in the household.",
        "Explain the routine before expecting the app itself to do the teaching.",
        "Keep the first reward list short so children understand what they are working towards.",
        "Review the routine after a week or two and remove anything that is creating more friction than value.",
        "Use clear task names instead of broad instructions such as ‘be good’ or ‘help more’.",
        "Try to keep expectations consistent while leaving room for illness, busy days and normal family changes.",
        "Make approval quick and fair so the check does not become another argument.",
        "Avoid adding so many jobs that the most important ones disappear inside the list.",
        "The best routine is usually the one the family can keep using without constant rebuilding.",
    ],
}

NOTICES = {
    "chore-charts": "The parent chooses the chores and remains responsible for making sure they are suitable for the child.",
    "daily-chores": "A daily list should help the routine, not overwhelm it. Keep the number of jobs realistic.",
    "kids-tasks": "Tasks should be explained and supervised by the parent or guardian where needed.",
    "family-routines": "Parent Quest can support organisation, but it does not replace parental supervision or judgement.",
    "rewards": "Rewards are created and provided by the parent. Vanta Labs does not supply or guarantee them.",
    "coins": "Reward coins have no cash value and cannot be exchanged with Vanta Labs.",
    "parent-approval": "Keep the Parent PIN private so approval remains under adult control.",
    "child-profiles": "Use only the information the family needs. A nickname is often enough for a child profile.",
    "parent-device": "Protected settings and approvals should remain under the parent or guardian’s control.",
    "guides": "Every household is different. Use the ideas that fit your family and ignore the ones that do not.",
}

FAQ_SECOND = {
    "chore-charts": (
        "Can the parent choose the chores?",
        "Yes. The parent decides which chores appear, which child they belong to and when they should be used.",
    ),
    "daily-chores": (
        "Do all chores have to happen every day?",
        "No. The parent chooses which jobs belong in the daily routine and can keep other tasks separate.",
    ),
    "kids-tasks": (
        "Can different children have different tasks?",
        "Yes. Child profiles allow the parent to create separate task lists for different children.",
    ),
    "family-routines": (
        "Does the routine have to stay the same?",
        "No. Parents can adjust the setup as the family’s schedule, children and priorities change.",
    ),
    "rewards": (
        "Who provides the rewards?",
        "The parent or guardian creates and provides the rewards. They are not supplied by Vanta Labs.",
    ),
    "coins": (
        "Are reward coins real money?",
        "No. They are an in-app progress measure used only inside the family’s own reward system.",
    ),
    "parent-approval": (
        "Why is there a Parent PIN?",
        "The PIN helps keep approval and protected parent actions under adult control.",
    ),
    "child-profiles": (
        "Do children need separate accounts?",
        "No. Child profiles are part of the parent-managed family setup and are not separate child accounts.",
    ),
    "parent-device": (
        "Does every child need their own device?",
        "No. Parent Quest is designed to be managed from a parent-owned device.",
    ),
    "guides": (
        "Should every family use the same routine?",
        "No. Chores, expectations and rewards should be chosen for the individual child and household.",
    ),
}

DESCRIPTIONS = {
    "chore-charts": "Create a clear family chore chart with child profiles, parent approval and rewards chosen by you.",
    "daily-chores": "Organise everyday chores for children in a simple routine managed and approved by the parent.",
    "kids-tasks": "Give each child a clear personal task list while keeping setup and approval under parent control.",
    "family-routines": "Bring chores, repeated tasks and family rewards into one flexible routine that is easy to follow.",
    "rewards": "Create custom family rewards and connect them to progress reviewed by the parent.",
    "coins": "Use parent-managed reward coins to show children their progress towards family-created rewards.",
    "parent-approval": "Review completed chores through the Parent PIN flow before progress and rewards are confirmed.",
    "child-profiles": "Keep each child’s chores, progress and rewards organised in a separate parent-managed profile.",
    "parent-device": "Manage child profiles, chores, approvals and rewards from one parent-owned device.",
    "guides": "Practical guidance for building clear family chore routines, task lists and parent-managed rewards.",
}


def file_for_page(page: dict) -> Path:
    if page["path"] == "/parent-quest/":
        return SITE / "index.html"

    relative = page["path"].removeprefix("/parent-quest/").strip("/")
    return SITE / relative / "index.html"


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
        raise RuntimeError(f"{label}: expected one replacement, found {count}")

    return updated


def clean_title_for_sentence(title: str) -> str:
    return title[0].lower() + title[1:] if title else title


def human_copy(page: dict) -> dict:
    cluster = page["cluster"]
    position = int(page.get("position", 1))
    index = (position - 1) % 10
    title = page["title"]

    opener = OPENERS[index]
    cluster_paragraph = CLUSTER_PARAGRAPHS[cluster][index]

    if cluster == "guides":
        first = cluster_paragraph
        second = (
            f"Parent Quest can support this by keeping child profiles, "
            f"chores, approval and rewards together, but the parent still "
            f"decides what works at home."
        )
    else:
        first = f"{opener} {cluster_paragraph}"
        second = (
            f"With {title}, the parent keeps control of the setup and the "
            f"final approval, while the child gets a clearer view of what "
            f"they are working on."
        )

    faq_one_q = f"What is {clean_title_for_sentence(title)} useful for?"
    faq_one_a = (
        f"It helps the family organise {page['intent']} inside Parent Quest "
        f"without taking control away from the parent or guardian."
    )

    faq_two_q, faq_two_a = FAQ_SECOND[cluster]

    faq_three_q = "Does Parent Quest replace parental supervision?"
    faq_three_a = (
        "No. Parent Quest is an organisation tool. The parent or guardian "
        "remains responsible for the child, the tasks and the rewards."
    )

    description = f"{title}: {DESCRIPTIONS[cluster]}"

    if len(description) > 158:
        description = DESCRIPTIONS[cluster]

    return {
        "heading": HEADINGS[cluster][index],
        "paragraph_one": first,
        "paragraph_two": second,
        "notice": NOTICES[cluster],
        "description": description,
        "faq": [
            (faq_one_q, faq_one_a),
            (faq_two_q, faq_two_a),
            (faq_three_q, faq_three_a),
        ],
    }


updated_pages = 0

for page in pages:
    file = file_for_page(page)

    if not file.is_file():
        raise FileNotFoundError(file)

    text = file.read_text(encoding="utf-8")

    if page["path"] == "/parent-quest/":
        text = replace_once(
            text,
            r'<p class="lead">.*?</p>',
            '''<p class="lead">
Create chores that make sense for your family, let children see what
needs doing and review their progress before rewards are added.
</p>''',
            str(file),
        )

        text = replace_once(
            text,
            r'<section class="long-copy">.*?</section>',
            '''<section class="long-copy">
<h2>A family routine that does not become another job</h2>
<div class="long-copy-text">
<p>
Parent Quest gives parents one clear place to organise child profiles,
everyday chores and the rewards their family has chosen. Children can
see what they are working on without getting access to the protected
parent settings.
</p>
<p>
When a task is marked complete, the parent can review it through the
Parent PIN flow. Reward coins and custom rewards remain part of your
own family routine—they are not money and they are not supplied by
Vanta Labs.
</p>
</div>
</section>''',
            str(file),
        )

        file.write_text(text, encoding="utf-8")
        updated_pages += 1
        continue

    copy = human_copy(page)

    escaped_description = html.escape(
        copy["description"],
        quote=True,
    )

    text = replace_once(
        text,
        r'(<meta\s+name="description"\s+content=")[^"]*("\s*/>)',
        rf'\g<1>{escaped_description}\g<2>',
        f"{file}: meta description",
    )

    text = replace_once(
        text,
        r'(<meta\s+property="og:description"\s+content=")[^"]*("\s*/>)',
        rf'\g<1>{escaped_description}\g<2>',
        f"{file}: og description",
    )

    lead = (
        f"{page['title']} helps parents organise "
        f"{page['intent']} in a clear family routine, with the final "
        f"setup and approval kept under adult control."
    )

    text = replace_once(
        text,
        r'<p class="lead">.*?</p>',
        f'<p class="lead">\n{html.escape(lead)}\n</p>',
        f"{file}: lead",
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
<strong>Parent controlled by design.</strong>
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
        for question, answer in copy["faq"]
    )

    text = replace_once(
        text,
        r'(<section class="faq">\s*<h2>Quick questions</h2>).*?(</section>)',
        rf'\1\n{faq_html}\n\2',
        f"{file}: FAQ",
    )

    file.write_text(text, encoding="utf-8")
    updated_pages += 1

print(f"Humanised Parent Quest pages: {updated_pages}")
