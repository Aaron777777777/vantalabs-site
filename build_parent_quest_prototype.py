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
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = ROOT / "parent-quest"
ASSETS = SITE / "assets"

ANDROID_URL = "https://play.google.com/store/apps/details?id=com.vantalabs.parentquest"
IOS_URL = "https://apps.apple.com/us/app/parent-quest/id6782297539"

clusters = {
    "chore-charts": [
        ("chore-chart-app", "Chore Chart App"),
        ("kids-chore-chart", "Kids Chore Chart"),
        ("digital-chore-chart", "Digital Chore Chart"),
        ("family-chore-chart", "Family Chore Chart"),
        ("daily-chore-chart", "Daily Chore Chart"),
        ("simple-chore-chart", "Simple Chore Chart"),
        ("home-chore-chart", "Home Chore Chart"),
        ("child-chore-chart", "Child Chore Chart"),
        ("parent-managed-chore-chart", "Parent-Managed Chore Chart"),
        ("chore-checklist-app", "Chore Checklist App"),
    ],
    "daily-chores": [
        ("daily-chores-app", "Daily Chores App"),
        ("daily-chores-for-kids", "Daily Chores for Kids"),
        ("child-daily-task-list", "Child Daily Task List"),
        ("home-chores-for-kids", "Home Chores for Kids"),
        ("simple-daily-chores", "Simple Daily Chores"),
        ("daily-household-tasks", "Daily Household Tasks"),
        ("daily-chore-checklist", "Daily Chore Checklist"),
        ("daily-family-tasks", "Daily Family Tasks"),
        ("organise-daily-chores", "Organise Daily Chores"),
        ("parent-managed-daily-chores", "Parent-Managed Daily Chores"),
    ],
    "kids-tasks": [
        ("kids-task-app", "Kids Task App"),
        ("task-list-for-kids", "Task List for Kids"),
        ("child-task-checklist", "Child Task Checklist"),
        ("family-task-app", "Family Task App"),
        ("home-tasks-for-children", "Home Tasks for Children"),
        ("simple-kids-task-list", "Simple Kids Task List"),
        ("parent-approved-tasks", "Parent-Approved Tasks"),
        ("tasks-and-rewards-for-kids", "Tasks and Rewards for Kids"),
        ("organise-child-tasks", "Organise Child Tasks"),
        ("personal-task-lists-for-children", "Personal Task Lists for Children"),
        ("homework-checklist-for-kids", "Homework Checklist for Kids"),
        ("homework-task-app-for-kids", "Homework Task App for Kids"),
        ("reading-goals-for-kids", "Reading Goals for Kids"),
        ("reading-checklist-for-kids", "Reading Checklist for Kids"),
    ],
    "family-routines": [
        ("family-routine-app", "Family Routine App"),
        ("kids-routine-app", "Kids Routine App"),
        ("daily-family-routine", "Daily Family Routine"),
        ("home-routine-checklist", "Home Routine Checklist"),
        ("child-routine-chart", "Child Routine Chart"),
        ("simple-family-routines", "Simple Family Routines"),
        ("chores-and-routines-app", "Chores and Routines App"),
        ("build-daily-routines-for-kids", "Build Daily Routines for Kids"),
        ("family-organisation-routine", "Family Organisation Routine"),
        ("parent-managed-routines", "Parent-Managed Routines"),
        ("morning-routine-app-for-kids", "Morning Routine App for Kids"),
        ("kids-morning-checklist", "Kids Morning Checklist"),
        ("bedtime-routine-app-for-kids", "Bedtime Routine App for Kids"),
        ("kids-bedtime-checklist", "Kids Bedtime Checklist"),
        ("after-school-routine-app", "After School Routine App"),
        ("school-morning-routine", "School Morning Routine"),
    ],
    "rewards": [
        ("kids-reward-app", "Kids Reward App"),
        ("chore-reward-app", "Chore Reward App"),
        ("custom-rewards-for-kids", "Custom Rewards for Kids"),
        ("family-reward-chart", "Family Reward Chart"),
        ("task-and-reward-app", "Task and Reward App"),
        ("child-reward-list", "Child Reward List"),
        ("parent-created-rewards", "Parent-Created Rewards"),
        ("rewards-for-completed-chores", "Rewards for Completed Chores"),
        ("simple-kids-rewards", "Simple Kids Rewards"),
        ("home-reward-system-for-kids", "Home Reward System for Kids"),
        ("homework-reward-chart", "Homework Reward Chart"),
        ("reading-reward-chart", "Reading Reward Chart"),
    ],
    "coins": [
        ("kids-coins-app", "Kids Coins App"),
        ("chore-coins-app", "Chore Coins App"),
        ("reward-coins-for-kids", "Reward Coins for Kids"),
        ("coins-for-completed-tasks", "Coins for Completed Tasks"),
        ("family-coin-reward-system", "Family Coin Reward System"),
        ("child-coins-tracker", "Child Coins Tracker"),
        ("parent-managed-reward-coins", "Parent-Managed Reward Coins"),
        ("earn-coins-for-chores", "Earn Coins for Chores"),
        ("simple-chore-coins", "Simple Chore Coins"),
        ("coins-and-custom-rewards", "Coins and Custom Rewards"),
    ],
    "parent-approval": [
        ("parent-approval-chore-app", "Parent Approval Chore App"),
        ("parent-pin-approval", "Parent PIN Approval"),
        ("approve-completed-chores", "Approve Completed Chores"),
        ("parent-approved-rewards", "Parent-Approved Rewards"),
        ("parent-controlled-chore-app", "Parent-Controlled Chore App"),
        ("pin-protected-parent-controls", "PIN-Protected Parent Controls"),
        ("review-child-tasks", "Review Child Tasks"),
        ("confirm-completed-tasks", "Confirm Completed Tasks"),
        ("parent-checks-for-chores", "Parent Checks for Chores"),
        ("parent-managed-task-approval", "Parent-Managed Task Approval"),
    ],
    "child-profiles": [
        ("child-profiles-chore-app", "Child Profiles Chore App"),
        ("kids-chore-profiles", "Kids Chore Profiles"),
        ("separate-task-lists-for-children", "Separate Task Lists for Children"),
        ("family-child-profiles", "Family Child Profiles"),
        ("personal-chore-lists-for-kids", "Personal Chore Lists for Kids"),
        ("manage-multiple-child-profiles", "Manage Multiple Child Profiles"),
        ("child-rewards-profile", "Child Rewards Profile"),
        ("child-task-progress", "Child Task Progress"),
        ("organise-chores-by-child", "Organise Chores by Child"),
        ("parent-managed-child-profiles", "Parent-Managed Child Profiles"),
    ],
    "parent-device": [
        ("chore-app-on-parent-phone", "Chore App on a Parent Phone"),
        ("parent-device-chore-app", "Parent Device Chore App"),
        ("family-chore-app-one-device", "Family Chore App on One Device"),
        ("parent-owned-device-chore-app", "Parent-Owned Device Chore App"),
        ("shared-family-task-screen", "Shared Family Task Screen"),
        ("manage-kids-chores-on-your-phone", "Manage Kids Chores on Your Phone"),
        ("simple-parent-phone-chore-chart", "Simple Parent Phone Chore Chart"),
        ("family-rewards-on-one-device", "Family Rewards on One Device"),
        ("parent-controlled-family-task-app", "Parent-Controlled Family Task App"),
        ("chores-without-child-accounts", "Chores Without Child Accounts"),
    ],
    "guides": [
        ("how-to-create-a-chore-chart", "How to Create a Chore Chart"),
        ("how-to-set-daily-chores-for-kids", "How to Set Daily Chores for Kids"),
        ("how-to-use-rewards-for-chores", "How to Use Rewards for Chores"),
        ("how-to-organise-family-tasks", "How to Organise Family Tasks"),
        ("how-to-build-a-family-routine", "How to Build a Family Routine"),
        ("how-to-choose-kids-rewards", "How to Choose Kids Rewards"),
        ("how-to-review-completed-chores", "How to Review Completed Chores"),
        ("how-to-manage-chores-for-siblings", "How to Manage Chores for Siblings"),
        ("how-to-use-coins-for-family-rewards", "How to Use Coins for Family Rewards"),
        ("how-to-keep-a-chore-chart-simple", "How to Keep a Chore Chart Simple"),
        ("how-to-build-a-morning-routine-for-kids", "How to Build a Morning Routine for Kids"),
        ("how-to-build-a-bedtime-routine-for-kids", "How to Build a Bedtime Routine for Kids"),
    ],
}

cluster_copy = {
    "chore-charts": "organising chores and checklists in a clear parent-managed view",
    "daily-chores": "setting out everyday chores and tasks for children",
    "kids-tasks": "creating clear personal task lists for children",
    "family-routines": "turning repeated household tasks into simpler family routines",
    "rewards": "connecting completed tasks with rewards chosen by the parent",
    "coins": "using in-app reward coins managed by the parent",
    "parent-approval": "reviewing task completion through parent-controlled approval",
    "child-profiles": "keeping each child’s chores, rewards and progress organised",
    "parent-device": "managing family chores and rewards on a parent-owned device",
    "guides": "practical ideas for chores, tasks, routines and parent-managed rewards",
}

pages = [{
    "path": "/parent-quest/",
    "type": "home",
    "cluster": "home",
    "title": "Parent Quest",
    "h1": "Chores, routines and rewards for family life",
    "intent": "Parent Quest app",
    "cluster_leader": "/parent-quest/",
    "description": (
        "Parent Quest helps parents organise child profiles, daily chores, "
        "parent-approved progress, reward coins and custom family rewards."
    ),
}]

for cluster, entries in clusters.items():
    leader = f"/parent-quest/{entries[0][0]}/"
    for position, (slug, title) in enumerate(entries, start=1):
        page_type = "guide" if cluster == "guides" else "feature"
        pages.append({
            "path": f"/parent-quest/{slug}/",
            "type": page_type,
            "cluster": cluster,
            "title": title,
            "h1": title,
            "intent": title.lower(),
            "description": (
                f"Explore {title.lower()} with Parent Quest, focused on "
                f"{cluster_copy[cluster]}."
            ),
            "cluster_leader": leader,
            "position": position,
        })

plan = {
    "product": "Parent Quest",
    "base_path": "/parent-quest/",
    "product_scope": (
        "Parent-managed child profiles, daily chores and tasks, Parent PIN "
        "approval, reward coins and custom rewards on a parent-owned device"
    ),
    "release_boundaries": [
        "Do not describe Parent Quest as Guardian or as a location or safety app.",
        "Do not claim child accounts, messaging, location tracking, banking or cash rewards.",
        "Do not edit the root homepage or root sitemap during prototype work.",
        "Do not edit, stage or release Vanta Workforce.",
        "Do not touch Guardian.",
    ],
    "android_url": ANDROID_URL,
    "ios_url": IOS_URL,
    "page_count": len(pages),
    "clusters": list(clusters),
    "pages": pages,
}

assert len(pages) >= 101
assert len({p["path"] for p in pages}) == len(pages)
assert len({p["title"] for p in pages}) == len(pages)
assert len({p["h1"] for p in pages}) == len(pages)

(ROOT / "parent_quest_page_plan.json").write_text(
    json.dumps(plan, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

ASSETS.mkdir(parents=True, exist_ok=True)

shutil.copy2(ROOT / "parentquest.png", ASSETS / "parent-quest-icon.png")

# Approved Parent Quest prototype CSS, frozen after visual approval.
css = ':root {\n  --bg: #030303;\n  --text: #f6efe2;\n  --muted: rgba(246, 239, 226, 0.68);\n  --soft: rgba(246, 239, 226, 0.38);\n  --line: rgba(246, 239, 226, 0.10);\n  --gold: #c9a646;\n  --parent-quest: #a79ad8;\n  --max: 1120px;\n}\n\n* {\n  box-sizing: border-box;\n  margin: 0;\n  padding: 0;\n}\n\nhtml {\n  scroll-behavior: smooth;\n}\n\nbody {\n  min-height: 100vh;\n  color: var(--text);\n  background:\n    radial-gradient(circle at 24% 0%, rgba(201, 166, 70, 0.08), transparent 28%),\n    linear-gradient(180deg, #080806 0%, #020202 45%, #000 100%);\n  font-family:\n    -apple-system,\n    BlinkMacSystemFont,\n    "SF Pro Display",\n    "Segoe UI",\n    Roboto,\n    Helvetica,\n    Arial,\n    sans-serif;\n  line-height: 1.65;\n}\n\nbody::before {\n  content: "";\n  position: fixed;\n  inset: 0;\n  pointer-events: none;\n  background-image:\n    linear-gradient(rgba(255, 255, 255, 0.012) 1px, transparent 1px),\n    linear-gradient(90deg, rgba(255, 255, 255, 0.012) 1px, transparent 1px);\n  background-size: 92px 92px;\n  opacity: 0.42;\n  mask-image:\n    linear-gradient(to bottom, black 0%, rgba(0, 0, 0, 0.6) 40%, transparent 70%);\n}\n\na {\n  color: inherit;\n  text-decoration: none;\n}\n\nimg {\n  max-width: 100%;\n  height: auto;\n}\n\n.head {\n  position: relative;\n  z-index: 2;\n  border-bottom: 1px solid var(--line);\n}\n\nnav {\n  width: min(var(--max), calc(100% - 44px));\n  height: 86px;\n  margin: 0 auto;\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n}\n\n.brand {\n  color: var(--gold);\n  font-size: 13px;\n  font-weight: 900;\n  letter-spacing: 0.24em;\n  text-transform: uppercase;\n}\n\n.links {\n  display: flex;\n  gap: 26px;\n}\n\n.links a {\n  color: var(--muted);\n  font-size: 14px;\n  font-weight: 650;\n}\n\n.links a:hover {\n  color: var(--text);\n}\n\n.hero {\n  position: relative;\n  z-index: 1;\n  width: min(var(--max), calc(100% - 44px));\n  margin: 0 auto;\n  padding: 76px 0 84px;\n  border-bottom: 1px solid var(--line);\n  display: grid;\n  grid-template-columns: 190px minmax(0, 1fr);\n  gap: 52px;\n  align-items: center;\n}\n\n.hero-visual {\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n\n.hero-icon {\n  width: 138px;\n  height: 138px;\n  object-fit: cover;\n  border-radius: 28px;\n  box-shadow: 0 22px 48px rgba(0, 0, 0, 0.48);\n}\n\n.hero-content {\n  max-width: 760px;\n}\n\n.eyebrow,\n.kicker,\n.label {\n  display: block;\n  color: var(--gold);\n  font-size: 11px;\n  font-weight: 900;\n  letter-spacing: 0.24em;\n  text-transform: uppercase;\n}\n\n.eyebrow {\n  margin-bottom: 16px;\n}\n\nh1 {\n  max-width: 700px;\n  font-size: clamp(46px, 5.3vw, 68px);\n  line-height: 1.01;\n  letter-spacing: -0.058em;\n  font-weight: 800;\n}\n\n.lead {\n  max-width: 660px;\n  margin-top: 24px;\n  color: var(--muted);\n  font-size: 18px;\n  line-height: 1.75;\n}\n\n.ctas {\n  display: flex;\n  flex-wrap: wrap;\n  gap: 10px;\n  margin-top: 24px;\n}\n\n.btn {\n  display: inline-flex;\n  align-items: center;\n  justify-content: center;\n  width: fit-content;\n  padding: 11px 15px;\n  border: 1px solid rgba(201, 166, 70, 0.28);\n  border-radius: 999px;\n  color: var(--gold);\n  background: rgba(201, 166, 70, 0.045);\n  font-size: 13px;\n  font-weight: 850;\n}\n\n.btn:hover {\n  border-color: rgba(201, 166, 70, 0.52);\n  background: rgba(201, 166, 70, 0.085);\n}\n\n.btn.disabled {\n  opacity: 0.62;\n  cursor: not-allowed;\n}\n\n.hero-note {\n  margin-top: 13px;\n  color: var(--soft);\n  font-size: 13px;\n}\n\n.hero-note a {\n  color: var(--gold);\n}\n\n.section {\n  position: relative;\n  z-index: 1;\n  width: min(var(--max), calc(100% - 44px));\n  margin: 0 auto;\n  padding: 92px 0;\n  border-bottom: 1px solid var(--line);\n}\n\n.section-head {\n  max-width: 720px;\n  margin-bottom: 42px;\n}\n\n.section h2 {\n  margin-top: 12px;\n  font-size: clamp(38px, 5vw, 58px);\n  line-height: 1;\n  letter-spacing: -0.06em;\n  font-weight: 850;\n}\n\n.section-head p {\n  margin-top: 22px;\n  color: var(--muted);\n  font-size: 18px;\n  line-height: 1.8;\n}\n\n.timeline {\n  position: relative;\n  display: grid;\n  grid-template-columns: repeat(4, 1fr);\n  gap: 28px;\n  padding-top: 28px;\n}\n\n.timeline::before {\n  content: "";\n  position: absolute;\n  top: 8px;\n  left: 0;\n  right: 0;\n  height: 1px;\n  background: var(--line);\n}\n\n.moment {\n  position: relative;\n  padding-right: 18px;\n}\n\n.moment::before {\n  content: "";\n  position: absolute;\n  top: -24px;\n  left: 0;\n  width: 9px;\n  height: 9px;\n  border-radius: 50%;\n  background: var(--parent-quest);\n  box-shadow: 0 0 0 5px rgba(167, 154, 216, 0.08);\n}\n\n.moment-num {\n  color: var(--gold);\n  font-size: 11px;\n  font-weight: 900;\n  letter-spacing: 0.18em;\n}\n\n.moment h3 {\n  margin-top: 12px;\n  font-size: 24px;\n  line-height: 1.05;\n  letter-spacing: -0.045em;\n}\n\n.moment p {\n  margin-top: 10px;\n  color: rgba(246, 239, 226, 0.74);\n  font-size: 14px;\n  line-height: 1.7;\n}\n\n.feature-list {\n  display: grid;\n  grid-template-columns: repeat(3, 1fr);\n  border-top: 1px solid var(--line);\n}\n\n.feature {\n  padding: 34px 34px 0 0;\n}\n\n.feature + .feature {\n  padding-left: 34px;\n  border-left: 1px solid var(--line);\n}\n\n.feature h3 {\n  margin-top: 18px;\n  font-size: 25px;\n  line-height: 1.06;\n  letter-spacing: -0.045em;\n}\n\n.feature p {\n  margin-top: 13px;\n  color: var(--muted);\n  font-size: 15px;\n  line-height: 1.75;\n}\n\n.parent-quest-focus {\n  margin-top: 58px;\n  padding: 40px;\n  border: 1px solid rgba(255, 255, 255, 0.11);\n  border-radius: 24px;\n  background: rgba(255, 255, 255, 0.018);\n  display: grid;\n  grid-template-columns: 0.95fr 1.05fr;\n  gap: 72px;\n}\n\n.parent-quest-focus h2 {\n  max-width: 500px;\n  font-size: clamp(32px, 4vw, 48px);\n}\n\n.parent-quest-focus p {\n  margin-top: 20px;\n  color: var(--muted);\n  font-size: 17px;\n  line-height: 1.8;\n}\n\n.checks {\n  padding-top: 4px;\n  display: grid;\n  gap: 16px;\n}\n\n.check {\n  display: flex;\n  gap: 10px;\n  color: var(--muted);\n  font-size: 16px;\n}\n\n.check b {\n  color: var(--parent-quest);\n}\n\n.faq-mini {\n  width: min(var(--max), calc(100% - 44px));\n  margin: 0 auto;\n  padding: 74px 0 80px;\n  border-bottom: 1px solid var(--line);\n}\n\n.faq-mini-head {\n  max-width: 680px;\n  margin-bottom: 30px;\n}\n\n.faq-mini h2 {\n  font-size: clamp(36px, 4.5vw, 54px);\n  line-height: 1;\n  letter-spacing: -0.055em;\n}\n\n.faq-mini-head p {\n  margin-top: 18px;\n  color: var(--muted);\n  font-size: 17px;\n  line-height: 1.75;\n}\n\n.faq-mini details {\n  padding: 22px 0;\n  border-top: 1px solid var(--line);\n}\n\n.faq-mini summary {\n  cursor: pointer;\n  font-size: 18px;\n  font-weight: 800;\n  letter-spacing: -0.02em;\n}\n\n.faq-mini details p {\n  max-width: 760px;\n  margin-top: 12px;\n  color: var(--muted);\n  font-size: 15px;\n  line-height: 1.75;\n}\n\n.related {\n  width: min(var(--max), calc(100% - 44px));\n  margin: 0 auto;\n  padding: 68px 0 86px;\n}\n\n.related-head {\n  display: grid;\n  grid-template-columns: 0.9fr 1.1fr;\n  gap: 54px;\n  align-items: end;\n  margin-bottom: 34px;\n}\n\n.related h2 {\n  font-size: clamp(34px, 4vw, 46px);\n  line-height: 1;\n  letter-spacing: -0.05em;\n}\n\n.related-intro {\n  color: var(--muted);\n  font-size: 17px;\n  line-height: 1.75;\n}\n\n.explore-grid {\n  display: grid;\n  grid-template-columns: repeat(2, 1fr);\n  gap: 0 44px;\n  border-top: 1px solid var(--line);\n}\n\n.explore-link {\n  display: block;\n  padding: 26px 0 28px;\n  border-bottom: 1px solid var(--line);\n}\n\n.explore-link:hover {\n  opacity: 0.76;\n}\n\n.explore-top {\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  gap: 18px;\n}\n\n.explore-link small {\n  color: var(--gold);\n  font-size: 10px;\n  font-weight: 900;\n  letter-spacing: 0.17em;\n  text-transform: uppercase;\n}\n\n.explore-arrow {\n  color: var(--soft);\n  font-size: 19px;\n}\n\n.explore-link strong {\n  display: block;\n  margin-top: 10px;\n  font-size: 25px;\n  line-height: 1.08;\n  letter-spacing: -0.04em;\n}\n\n.explore-link p {\n  max-width: 460px;\n  margin-top: 10px;\n  color: var(--muted);\n  font-size: 14px;\n  line-height: 1.7;\n}\n\n.all-guides {\n  display: inline-flex;\n  gap: 8px;\n  margin-top: 26px;\n  color: var(--gold);\n  font-size: 13px;\n  font-weight: 850;\n}\n\n.parent-quest-detail .hero {\n  grid-template-columns: minmax(0, 1fr) 180px;\n  padding: 86px 0;\n}\n\n.parent-quest-detail .hero > div:first-child {\n  max-width: 780px;\n}\n\n.parent-quest-detail .hero h1 {\n  max-width: 760px;\n  margin-top: 12px;\n  font-size: clamp(42px, 5.2vw, 66px);\n}\n\n.iconbox {\n  width: 180px;\n  height: 180px;\n  padding: 24px;\n  border: 1px solid var(--line);\n  border-radius: 28px;\n  background:\n    linear-gradient(\n      180deg,\n      rgba(255, 255, 255, 0.045),\n      rgba(255, 255, 255, 0.014)\n    );\n  display: flex;\n  align-items: center;\n  justify-content: center;\n}\n\n.iconbox img {\n  width: 112px;\n  height: 112px;\n  object-fit: cover;\n  border-radius: 23px;\n}\n\n.body {\n  width: min(860px, calc(100% - 44px));\n  margin: 0 auto;\n  padding: 78px 0 58px;\n}\n\n.long-copy {\n  padding: 0 0 46px;\n}\n\n.long-copy h2 {\n  max-width: 680px;\n  font-size: clamp(32px, 4vw, 46px);\n  line-height: 1.06;\n  letter-spacing: -0.05em;\n}\n\n.long-copy-text {\n  margin-top: 24px;\n}\n\n.long-copy p {\n  color: var(--muted);\n  font-size: 17px;\n  line-height: 1.9;\n}\n\n.long-copy p + p {\n  margin-top: 22px;\n}\n\n.notice {\n  padding: 17px 19px;\n  border: 1px solid rgba(201, 166, 70, 0.22);\n  border-radius: 16px;\n  background: rgba(201, 166, 70, 0.04);\n  color: var(--muted);\n  font-size: 14px;\n  line-height: 1.7;\n}\n\n.parent-quest-lower-grid {\n  display: grid;\n  grid-template-columns: 1.08fr 0.92fr;\n  gap: 58px;\n  margin-top: 68px;\n  padding-top: 10px;\n}\n\n.parent-quest-detail .related,\n.parent-quest-detail .faq {\n  width: auto;\n  margin: 0;\n  padding: 0;\n}\n\n.parent-quest-detail .related h2,\n.parent-quest-detail .faq h2 {\n  margin-bottom: 28px;\n  font-size: clamp(30px, 3.5vw, 42px);\n}\n\n.parent-quest-detail .related .grid {\n  display: grid;\n}\n\n.parent-quest-detail .related .card {\n  padding: 23px 0;\n  border-top: 1px solid var(--line);\n}\n\n.parent-quest-detail .related .card small {\n  color: var(--gold);\n  font-size: 10px;\n  font-weight: 900;\n  letter-spacing: 0.15em;\n  text-transform: uppercase;\n}\n\n.parent-quest-detail .related .card strong {\n  display: block;\n  margin-top: 8px;\n  font-size: 21px;\n  line-height: 1.12;\n  letter-spacing: -0.035em;\n}\n\n.parent-quest-detail .faq details {\n  padding: 22px 0;\n  border-top: 1px solid var(--line);\n}\n\n.parent-quest-detail .faq summary {\n  cursor: pointer;\n  font-size: 17px;\n  font-weight: 800;\n}\n\n.parent-quest-detail .faq p {\n  margin-top: 11px;\n  color: var(--muted);\n  font-size: 15px;\n  line-height: 1.75;\n}\n\nfooter {\n  width: min(var(--max), calc(100% - 44px));\n  margin: 0 auto;\n  display: flex;\n  justify-content: space-between;\n  gap: 20px;\n  padding: 30px 0 34px;\n  color: var(--soft);\n  font-size: 13px;\n}\n\n@media (max-width: 900px) {\n  .timeline {\n    grid-template-columns: repeat(2, 1fr);\n    gap: 42px 28px;\n  }\n\n  .timeline::before {\n    display: none;\n  }\n\n  .moment {\n    padding-top: 18px;\n    border-top: 1px solid var(--line);\n  }\n\n  .moment::before {\n    top: -5px;\n  }\n\n  .feature-list,\n  .parent-quest-focus,\n  .parent-quest-lower-grid {\n    grid-template-columns: 1fr;\n  }\n\n  .feature {\n    padding: 28px 0;\n    border-bottom: 1px solid var(--line);\n  }\n\n  .feature + .feature {\n    padding-left: 0;\n    border-left: 0;\n  }\n}\n\n@media (max-width: 760px) {\n  .hero,\n  .parent-quest-detail .hero {\n    grid-template-columns: 1fr;\n    gap: 28px;\n    padding: 58px 0 64px;\n  }\n\n  .hero-visual {\n    justify-content: center;\n  }\n\n  .hero-icon {\n    width: 104px;\n    height: 104px;\n    border-radius: 22px;\n  }\n\n  .hero-content {\n    text-align: center;\n  }\n\n  .hero h1,\n  .hero .lead {\n    margin-left: auto;\n    margin-right: auto;\n  }\n\n  .ctas {\n    justify-content: center;\n  }\n\n  .hero-note {\n    text-align: center;\n  }\n\n  .parent-quest-detail .iconbox {\n    order: -1;\n    width: 112px;\n    height: 112px;\n    padding: 14px;\n    border-radius: 23px;\n  }\n\n  .parent-quest-detail .iconbox img {\n    width: 80px;\n    height: 80px;\n    border-radius: 18px;\n  }\n\n  .related-head,\n  .explore-grid {\n    grid-template-columns: 1fr;\n  }\n}\n\n@media (max-width: 560px) {\n  nav,\n  .hero,\n  .section,\n  .faq-mini,\n  .related,\n  .body,\n  footer {\n    width: min(100% - 28px, var(--max));\n  }\n\n  nav {\n    height: auto;\n    padding: 22px 0 18px;\n  }\n\n  .brand {\n    font-size: 11px;\n  }\n\n  .links {\n    display: none;\n  }\n\n  h1 {\n    font-size: 46px;\n  }\n\n  .ctas .btn {\n    width: 100%;\n  }\n\n  .section {\n    padding: 64px 0;\n  }\n\n  .timeline {\n    grid-template-columns: 1fr;\n  }\n\n  .parent-quest-focus {\n    padding: 28px 22px;\n    border-radius: 18px;\n    gap: 34px;\n  }\n\n  footer {\n    flex-direction: column;\n  }\n}\n\n/* Vanta Shift hero refinements */\n.parent-quest-home .hero,\nbody:not(.parent-quest-detail) .hero {\n  grid-template-columns: minmax(0, 1.3fr) minmax(280px, 0.7fr);\n  align-items: center;\n  gap: clamp(48px, 7vw, 110px);\n}\n\n.parent-quest-home .hero > div:first-child,\nbody:not(.parent-quest-detail) .hero > div:first-child {\n  min-width: 0;\n  max-width: 780px;\n}\n\n.parent-quest-home .hero h1,\nbody:not(.parent-quest-detail) .hero h1 {\n  max-width: 760px;\n  font-size: clamp(4rem, 7vw, 7rem);\n  line-height: 0.94;\n  letter-spacing: -0.055em;\n}\n\n.parent-quest-home .hero .lead,\nbody:not(.parent-quest-detail) .hero .lead {\n  max-width: 640px;\n}\n\n.parent-quest-home .iconbox,\nbody:not(.parent-quest-detail) .iconbox {\n  position: static;\n  justify-self: end;\n  align-self: center;\n  width: min(100%, 390px);\n  min-height: 390px;\n  display: grid;\n  place-items: center;\n}\n\n.parent-quest-home .iconbox img,\nbody:not(.parent-quest-detail) .iconbox img {\n  width: min(72%, 260px);\n  height: auto;\n}\n\n@media (max-width: 900px) {\n  .parent-quest-home .hero,\n  body:not(.parent-quest-detail) .hero {\n    grid-template-columns: 1fr;\n    gap: 42px;\n  }\n\n  .parent-quest-home .hero h1,\n  body:not(.parent-quest-detail) .hero h1 {\n    max-width: 680px;\n    font-size: clamp(3.5rem, 13vw, 6rem);\n  }\n\n  .parent-quest-home .iconbox,\n  body:not(.parent-quest-detail) .iconbox {\n    justify-self: start;\n    width: min(100%, 320px);\n    min-height: 300px;\n  }\n}\n/* Parent Quest Guardian-style finished detail rhythm */\n.parent-quest-detail .body {\n  width: min(var(--max), calc(100% - 44px)) !important;\n  margin: 0 auto !important;\n  padding: 82px 0 0 !important;\n  text-align: left !important;\n}\n\n.parent-quest-detail .long-copy {\n  max-width: 760px !important;\n  margin: 0 !important;\n  padding: 0 !important;\n  text-align: left !important;\n}\n\n.parent-quest-detail .long-copy h2 {\n  max-width: 650px !important;\n  margin: 0 0 28px !important;\n  font-size: clamp(30px, 3.6vw, 42px) !important;\n  line-height: 1.12 !important;\n  letter-spacing: -0.045em !important;\n}\n\n.parent-quest-detail .long-copy-text {\n  max-width: 710px !important;\n  margin: 0 !important;\n}\n\n.parent-quest-detail .long-copy-text p {\n  color: var(--muted) !important;\n  font-size: 17px !important;\n  line-height: 1.82 !important;\n}\n\n.parent-quest-detail .long-copy-text p + p {\n  margin-top: 22px !important;\n}\n\n.parent-quest-detail .body .notice {\n  max-width: 710px !important;\n  margin: 42px 0 0 !important;\n  padding: 20px 0 0 !important;\n  border: 0 !important;\n  border-top: 1px solid rgba(201, 166, 70, 0.22) !important;\n  border-radius: 0 !important;\n  background: transparent !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid {\n  width: min(var(--max), calc(100% - 44px)) !important;\n  margin: 78px auto 0 !important;\n  padding: 76px 0 78px !important;\n  border-top: 1px solid var(--line) !important;\n  grid-template-columns: minmax(0, 1.2fr) minmax(300px, 0.8fr) !important;\n  gap: 72px !important;\n  text-align: left !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .related,\n.parent-quest-detail .parent-quest-lower-grid .faq {\n  width: auto !important;\n  margin: 0 !important;\n  padding: 0 !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .related h2,\n.parent-quest-detail .parent-quest-lower-grid .faq h2 {\n  margin: 0 0 22px !important;\n  color: var(--text) !important;\n  font-size: 22px !important;\n  font-weight: 800 !important;\n  line-height: 1.16 !important;\n  letter-spacing: -0.035em !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .related .grid {\n  display: grid !important;\n  grid-template-columns: 1fr !important;\n  gap: 0 !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .related .card {\n  position: relative;\n  padding: 19px 34px 21px 0 !important;\n  border-top: 1px solid var(--line) !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .related .card::after {\n  content: "→";\n  position: absolute;\n  right: 2px;\n  top: 22px;\n  color: rgba(246, 239, 226, 0.42);\n  transition: color 0.18s ease, transform 0.18s ease;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .related .card:hover::after {\n  color: var(--gold);\n  transform: translateX(3px);\n}\n\n.parent-quest-detail .parent-quest-lower-grid .related .card small {\n  display: none !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .related .card strong {\n  max-width: 520px;\n  margin: 0 !important;\n  font-size: 17px !important;\n  line-height: 1.3 !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .faq {\n  padding: 24px !important;\n  border: 1px solid var(--line) !important;\n  border-radius: 20px !important;\n  background: rgba(255, 255, 255, 0.018) !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .faq h2 {\n  margin-bottom: 10px !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .faq details {\n  padding: 15px 0 !important;\n}\n\n.parent-quest-detail .parent-quest-lower-grid .faq summary {\n  font-size: 14px !important;\n  line-height: 1.45 !important;\n}\n\n@media (max-width: 760px) {\n  .parent-quest-detail .body {\n    padding: 60px 0 0 !important;\n  }\n\n  .parent-quest-detail .long-copy h2 {\n    margin-bottom: 23px !important;\n    font-size: clamp(29px, 9vw, 38px) !important;\n    line-height: 1.13 !important;\n  }\n\n  .parent-quest-detail .body .notice {\n    margin-top: 38px !important;\n  }\n\n  .parent-quest-detail .parent-quest-lower-grid {\n    margin-top: 60px !important;\n    padding: 58px 0 70px !important;\n    grid-template-columns: 1fr !important;\n    gap: 46px !important;\n  }\n}\n/* Parent Quest full-first-screen detail hero */\n.parent-quest-detail .hero {\n  min-height: calc(100vh - 86px) !important;\n  align-items: center !important;\n  padding: 96px 0 96px !important;\n}\n\n.parent-quest-detail .hero > div:first-child {\n  align-self: center !important;\n}\n\n.parent-quest-detail .iconbox {\n  align-self: center !important;\n}\n\n@media (max-width: 900px) {\n  .parent-quest-detail .hero {\n    min-height: auto !important;\n    padding: 72px 0 74px !important;\n  }\n}\n'
(ASSETS / "parent-quest.css").write_text(
    css,
    encoding="utf-8",
)

(ASSETS / "app-links.js").write_text(
    f'''(() => {{
  const links = {{
    android: "{ANDROID_URL}",
    ios: "{IOS_URL}",
  }};

  document.querySelectorAll("[data-store]").forEach((element) => {{
    const url = links[element.dataset.store];
    if (!url) return;
    element.href = url;
    element.target = "_blank";
    element.rel = "noopener noreferrer";
  }});
}})();
''',
    encoding="utf-8",
)

def schema_json(items: list[dict]) -> str:
    return json.dumps(items, ensure_ascii=False, separators=(",", ":"))

home_schema = [{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Parent Quest",
    "applicationCategory": "LifestyleApplication",
    "operatingSystem": "Android, iOS",
    "description": pages[0]["description"],
    "url": "https://www.vantalabs.co.uk/parent-quest/",
    "downloadUrl": [ANDROID_URL, IOS_URL],
    "publisher": {
        "@type": "Organization",
        "name": "Vanta Labs",
        "url": "https://www.vantalabs.co.uk/",
    },
}]

home = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Parent Quest</title>
<meta name="description" content="{html.escape(pages[0]["description"], quote=True)}"/>
<link rel="canonical" href="https://www.vantalabs.co.uk/parent-quest/"/>
<meta content="index,follow,max-image-preview:large" name="robots"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Vanta Labs"/>
<meta property="og:title" content="Parent Quest"/>
<meta property="og:description" content="Chores, parent-approved progress, reward coins and custom family rewards in one clear app."/>
<meta property="og:url" content="https://www.vantalabs.co.uk/parent-quest/"/>
<meta property="og:image" content="https://www.vantalabs.co.uk/parentquest.png"/>
<link href="/parent-quest/assets/parent-quest-icon.png" rel="icon"/>
<link href="/parent-quest/assets/parent-quest.css" rel="stylesheet"/>
<script defer src="/parent-quest/assets/app-links.js"></script>
<script type="application/ld+json">{schema_json(home_schema)}</script>
</head>

<body class="parent-quest-home">
<header class="head">
<nav>
<a class="brand" href="/">Vanta Labs</a>
<div class="links">
<a href="/parent-quest/">Parent Quest</a>
<a href="/parent-quest/chore-chart-app/">Chore charts</a>
<a href="#rewards">Rewards</a>
<a href="#questions">Questions</a>
</div>
</nav>
</header>

<main>
<div class="hero">
<div>
<span class="eyebrow">Parent Quest</span>
<h1>Chores, routines and rewards for family life</h1>
<p class="lead">
Create child profiles, organise daily chores and tasks, approve completed
progress with the parent PIN and let children work towards reward coins
and custom rewards chosen by you.
</p>
<div class="ctas">
<a class="btn" data-store="android">Google Play</a>
<a class="btn" data-store="ios">App Store</a>
</div>
</div>

<div class="iconbox">
<img alt="Parent Quest app icon" height="512"
src="/parent-quest/assets/parent-quest-icon.png" width="512"/>
</div>
</div>

<article class="body">
<section class="long-copy">
<h2>A simple family system that stays parent controlled</h2>
<div class="long-copy-text">
<p>
Parent Quest brings chores, task lists, child profiles and family rewards
into one clear place. Parents decide what needs doing, which child it belongs
to and what rewards are available.
</p>
<p>
Completed tasks can be reviewed through the parent-controlled approval flow.
Reward coins and custom rewards remain part of the family’s own routine rather
than money issued or guaranteed by Vanta Labs.
</p>
</div>
</section>

<div class="notice">
<strong>Designed for a parent-owned device.</strong>
Parent Quest is managed by the parent or guardian and is not a replacement
for parental supervision.
</div>

<div class="parent-quest-lower-grid">
<section class="related" id="rewards">
<h2>The useful parts, together</h2>
<div class="grid">
<a class="card" href="/parent-quest/chore-chart-app/">
<small>Chores</small><strong>Set out clear daily tasks</strong>
</a>
<a class="card" href="/parent-quest/child-profiles-chore-app/">
<small>Child profiles</small><strong>Keep each child organised</strong>
</a>
<a class="card" href="/parent-quest/parent-pin-approval/">
<small>Parent approval</small><strong>Review completed progress</strong>
</a>
<a class="card" href="/parent-quest/custom-rewards-for-kids/">
<small>Rewards</small><strong>Create rewards for your family</strong>
</a>
</div>
</section>

<section class="faq" id="questions">
<h2>Quick questions</h2>
<details>
<summary>What is Parent Quest designed for?</summary>
<p>Parent Quest helps parents manage child profiles, chores, tasks, reward coins and custom rewards.</p>
</details>
<details>
<summary>Who approves completed chores?</summary>
<p>The parent or guardian reviews progress through the parent-controlled approval flow.</p>
</details>
<details>
<summary>Are reward coins real money?</summary>
<p>No. They are parent-managed reward currency inside the family’s own chore and reward system.</p>
</details>
</section>
</div>
</article>
</main>

<footer>
<span>© 2026 Vanta Labs NW LTD · Manchester, UK</span>
<span><a href="/privacy.html">Privacy</a> ·
<a href="/terms.html">Terms</a> ·
<a href="/">All Vanta Labs apps</a></span>
</footer>
</body>
</html>
'''

SITE.mkdir(exist_ok=True)
(SITE / "index.html").write_text(home, encoding="utf-8")

detail_page = next(p for p in pages if p["path"] == "/parent-quest/chore-chart-app/")
detail_dir = SITE / "chore-chart-app"
detail_dir.mkdir(exist_ok=True)

detail_schema = [
    {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Parent Quest",
        "applicationCategory": "LifestyleApplication",
        "operatingSystem": "Android, iOS",
        "description": detail_page["description"],
        "url": "https://www.vantalabs.co.uk/parent-quest/chore-chart-app/",
        "downloadUrl": [ANDROID_URL, IOS_URL],
        "image": "https://www.vantalabs.co.uk/parentquest.png",
        "publisher": {
            "@type": "Organization",
            "name": "Vanta Labs",
            "url": "https://www.vantalabs.co.uk/",
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
                "item": "https://www.vantalabs.co.uk/",
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Parent Quest",
                "item": "https://www.vantalabs.co.uk/parent-quest/",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": "Chore Chart App",
                "item": "https://www.vantalabs.co.uk/parent-quest/chore-chart-app/",
            },
        ],
    },
    {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What does the chore chart organise?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "It organises parent-created chores and tasks for child profiles in Parent Quest.",
                },
            },
            {
                "@type": "Question",
                "name": "Can parents review completed chores?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes. Completed progress can be reviewed through the parent-controlled approval flow.",
                },
            },
            {
                "@type": "Question",
                "name": "Can chores connect to family rewards?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Parents can use reward coins and custom rewards as part of their own family routine.",
                },
            },
        ],
    },
]

detail = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>Chore Chart App | Parent Quest</title>
<meta name="description" content="{html.escape(detail_page["description"], quote=True)}"/>
<link rel="canonical" href="https://www.vantalabs.co.uk/parent-quest/chore-chart-app/"/>
<meta content="index,follow,max-image-preview:large" name="robots"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Vanta Labs"/>
<meta property="og:title" content="Chore Chart App"/>
<meta property="og:description" content="{html.escape(detail_page["description"], quote=True)}"/>
<meta property="og:url" content="https://www.vantalabs.co.uk/parent-quest/chore-chart-app/"/>
<meta property="og:image" content="https://www.vantalabs.co.uk/parentquest.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<link href="/parent-quest/assets/parent-quest-icon.png" rel="icon"/>
<link href="/parent-quest/assets/parent-quest.css" rel="stylesheet"/>
<script defer src="/parent-quest/assets/app-links.js"></script>
<script type="application/ld+json">{schema_json(detail_schema)}</script>
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
<span class="eyebrow">Chore charts</span>
<h1>Chore Chart App</h1>
<p class="lead">
Organise child profiles, daily chores and clear task lists in a simple
parent-managed view.
</p>
<div class="ctas">
<a class="btn" data-store="android">Google Play</a>
<a class="btn" data-store="ios">App Store</a>
</div>
</div>

<div class="iconbox">
<img alt="Parent Quest app icon" height="512"
src="/parent-quest/assets/parent-quest-icon.png" width="512"/>
</div>
</div>

<article class="body">
<section class="long-copy">
<h2>A clearer way to organise everyday chores</h2>
<div class="long-copy-text">
<p>
Chore Chart App brings the tasks chosen by the parent into a clear list
for each child profile. Daily chores can sit alongside other household
tasks so everyone can see what belongs in the routine.
</p>
<p>
Parent Quest keeps control with the parent or guardian. Progress can be
reviewed through the parent approval flow before reward coins or custom
family rewards become part of the child’s progress.
</p>
</div>
</section>

<div class="notice">
<strong>Rewards remain parent managed.</strong>
Coins and rewards shown in Parent Quest have no monetary value within
the app and are not issued or funded by Vanta Labs.
</div>

<div class="parent-quest-lower-grid">
<section class="related">
<h2>Keep exploring Parent Quest</h2>
<div class="grid">
<a class="card" href="/parent-quest/kids-chore-chart/">
<small>Chore charts</small><strong>Kids Chore Chart</strong>
</a>
<a class="card" href="/parent-quest/daily-chore-chart/">
<small>Chore charts</small><strong>Daily Chore Chart</strong>
</a>
<a class="card" href="/parent-quest/child-profiles-chore-app/">
<small>Child profiles</small><strong>Child Profiles Chore App</strong>
</a>
<a class="card" href="/parent-quest/custom-rewards-for-kids/">
<small>Rewards</small><strong>Custom Rewards for Kids</strong>
</a>
</div>
</section>

<section class="faq">
<h2>Quick questions</h2>
<details>
<summary>What does the chore chart organise?</summary>
<p>It organises parent-created chores and tasks for child profiles in Parent Quest.</p>
</details>
<details>
<summary>Can parents review completed chores?</summary>
<p>Yes. Completed progress can be reviewed through the parent-controlled approval flow.</p>
</details>
<details>
<summary>Can chores connect to family rewards?</summary>
<p>Parents can use reward coins and custom rewards as part of their own family routine.</p>
</details>
</section>
</div>
</article>
</main>

<footer>
<span>© 2026 Vanta Labs NW LTD · Manchester, UK</span>
<span><a href="/privacy.html">Privacy</a> ·
<a href="/terms.html">Terms</a> ·
<a href="/">All Vanta Labs apps</a></span>
</footer>
</body>
</html>
'''

(detail_dir / "index.html").write_text(detail, encoding="utf-8")

print("Created Parent Quest page plan:", len(pages), "pages")
print("Created prototype:", SITE / "index.html")
print("Created detail prototype:", detail_dir / "index.html")
