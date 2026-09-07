#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import json
import re
import shutil

from bs4 import BeautifulSoup


ROOT = Path.home() / "Projects" / "vantalabs-site"
GUARDIAN = ROOT / "guardian"
PLAY_URL = "https://play.google.com/store/apps/details?id=com.vantalabs.guardian&pcampaignid=web_share"

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup = ROOT / f"guardian.before-final-seo-play-cleanup-{timestamp}"

if not GUARDIAN.is_dir():
    raise SystemExit(f"Guardian folder not found: {GUARDIAN}")

if backup.exists():
    raise SystemExit(f"Backup already exists: {backup}")

print(f"Creating backup:\n  {backup}")
shutil.copytree(GUARDIAN, backup)


H1_REPLACEMENTS = {
    "/guardian/see-my-childs-location-app/":
        "Check a child phone’s latest shared location at a glance",

    "/guardian/home-and-school-alerts-app/":
        "One place for Home and School arrival alerts",

    "/guardian/school-run-safety-app/":
        "School-run alerts for the moments that matter",
}


ARTICLE_REWRITES = {
    "/guardian/child-location-app/": (
        "Location sharing for quick reassurance, not constant watching",
        (
            "Guardian gives trusted adults a clear view of a connected child "
            "phone’s latest available location, battery level and last update "
            "time. It is designed for quick checks during everyday routines, "
            "rather than leaving the Family Map open throughout the day."
        ),
        (
            "Home and School alerts can provide useful updates without repeated "
            "messages, while recent location context helps explain the journey "
            "when a closer look is needed. Location still depends on the phone’s "
            "signal, permissions and battery settings."
        ),
    ),

    "/guardian/child-locator-app/": (
        "What a private child locator should show",
        (
            "A useful child locator should provide more than a pin on a map. "
            "Guardian pairs the connected phone’s latest available position "
            "with battery status and the time of its last update, so parents "
            "can understand how current the information is."
        ),
        (
            "Access stays inside the parent-managed Guardian family. There are "
            "no public profiles or social discovery features, and adult location "
            "sharing remains optional."
        ),
    ),

    "/guardian/child-tracker-app/": (
        "A child tracker built around ordinary routines",
        (
            "Guardian focuses on the moments families commonly need help with: "
            "leaving Home, reaching School, leaving School and returning Home. "
            "Safe-zone notifications can provide those updates without requiring "
            "constant map checks."
        ),
        (
            "When a parent needs more context, the Family Map shows the latest "
            "available child-device location alongside battery and update status. "
            "The aim is practical reassurance while preserving sensible family "
            "boundaries."
        ),
    ),

    "/guardian/kids-gps-tracker-app/": (
        "Understanding GPS tracking on a child’s phone",
        (
            "A phone-based GPS tracker relies on the connected device’s location "
            "services, permissions, connectivity and background settings. Guardian "
            "shows the latest information the child phone has successfully shared, "
            "rather than pretending every map position is perfectly live."
        ),
        (
            "Battery level and last-update time provide important context when a "
            "position appears old. Buildings, weak signal and battery optimisation "
            "can all affect accuracy or delay an update."
        ),
    ),

    "/guardian/gps-tracker-for-children/": (
        "Set realistic expectations for phone GPS",
        (
            "Guardian can help a family check a connected child phone’s latest "
            "available location and receive useful Home and School updates. It "
            "cannot turn a phone into a flawless, continuously reporting tracker."
        ),
        (
            "Parents should test permissions and battery settings on the child "
            "device, explain how location sharing will be used, and keep direct "
            "communication as part of the normal family routine."
        ),
    ),

    "/guardian/phone-tracker-for-kids/": (
        "Device context matters as much as the map",
        (
            "Guardian connects a child’s phone to a private, parent-managed family. "
            "Alongside the latest available map position, parents can see battery "
            "status and when the device last reported."
        ),
        (
            "That context can help distinguish a genuine journey update from a "
            "phone that has poor signal, restrictive background settings or a low "
            "battery. Guardian is intended to support communication, not replace it."
        ),
    ),

    "/guardian/parent-child-location-app/": (
        "Parent-managed access with clear family boundaries",
        (
            "Guardian places family access under trusted adult control. A connected "
            "child device shares information only inside its Guardian family, and "
            "parents decide which trusted adults can access that family."
        ),
        (
            "The app combines map context, Home and School alerts, device status "
            "and SOS tools without public profiles or a social feed. Adult location "
            "sharing is optional rather than a requirement."
        ),
    ),

    "/guardian/family-location-map-app/": (
        "A private family map with useful context",
        (
            "Guardian’s Family Map brings connected family devices into one private "
            "view. It shows the latest available shared location together with "
            "battery level and update time, so the map is easier to interpret."
        ),
        (
            "The map is there when extra context is genuinely useful. Home and "
            "School alerts are intended to reduce the need to keep reopening it "
            "during familiar daily journeys."
        ),
    ),

    "/guardian/family-tracker-app/": (
        "Keep trusted adults informed without a public network",
        (
            "Guardian helps trusted adults stay aligned around connected child "
            "devices, safe-zone updates and recent location context. Everything "
            "stays inside the private family rather than appearing on public "
            "profiles or a social map."
        ),
        (
            "Different adults can use the same family information to coordinate "
            "school runs and ordinary journeys. Parent location sharing remains "
            "optional, so adults are not forced to share their own position."
        ),
    ),

    "/guardian/family-map-app/": (
        "Use the map when an alert needs more context",
        (
            "A family map is most useful when it answers a specific question. "
            "Guardian lets trusted adults check the latest available shared "
            "location after an unexpected delay, an alert or a change in plans."
        ),
        (
            "Battery and last-update details help parents judge how current the "
            "map information is. The map complements Home and School notifications "
            "rather than demanding constant attention."
        ),
    ),

    "/guardian/location-sharing-app-for-parents/": (
        "Location sharing that remains optional for adults",
        (
            "Guardian allows trusted adults to take part in a private family without "
            "forcing them to continuously share their own location. Adult location "
            "sharing can be used when it suits the family and left off when it does not."
        ),
        (
            "Connected child-device information remains available to authorised "
            "family adults according to the app’s access controls. This keeps the "
            "focus on practical coordination rather than compulsory adult tracking."
        ),
    ),

    "/guardian/optional-parent-location-sharing/": (
        "Parents choose whether to share their own location",
        (
            "A parent can use Guardian’s family safety tools without being required "
            "to broadcast their own position. Adult location sharing is an optional "
            "family choice, not a condition of viewing an authorised child device."
        ),
        (
            "Families can agree when adult sharing is useful—for example during a "
            "pickup or shared journey—and leave it disabled during the rest of the day."
        ),
    ),

    "/guardian/talk-to-children-about-location-sharing/": (
        "Make location sharing a family conversation",
        (
            "Before connecting a child phone, explain what Guardian will share, who "
            "can see it and when parents expect to check it. Clear boundaries help "
            "location tools feel predictable rather than secretive."
        ),
        (
            "The conversation should also cover Home and School alerts, SOS use, "
            "phone permissions and the fact that GPS can sometimes be delayed or "
            "inaccurate. Review the agreement as the child becomes more independent."
        ),
    ),

    "/guardian/what-to-look-for-in-family-location-app/": (
        "Choose a family location app by behaviour, not hype",
        (
            "Look for clear access controls, understandable privacy choices, useful "
            "device context and honest explanations of GPS limitations. A long list "
            "of features matters less if families cannot tell who sees their data."
        ),
        (
            "It is also worth checking whether alerts reduce unnecessary map watching, "
            "whether adult sharing is optional and whether the service avoids public "
            "profiles or unrelated social features."
        ),
    ),

    "/guardian/what-to-do-when-location-does-not-update/": (
        "Check the phone before assuming the journey stopped",
        (
            "An old location can mean the connected phone has weak signal, disabled "
            "permissions, battery optimisation, restricted background activity or a "
            "low battery. Start by checking Guardian’s battery and last-update details."
        ),
        (
            "Then confirm mobile data, precise location permission and background "
            "access on the child device. Restarting the app or phone can help, but "
            "directly contacting the family member remains the safest next step when "
            "the information is important."
        ),
    ),

    "/guardian/family-location-data-privacy/": (
        "Family location data deserves careful handling",
        (
            "Location information can reveal routines, schools and frequently visited "
            "places. Guardian keeps family information inside a private, parent-managed "
            "account rather than using public profiles or a social discovery feed."
        ),
        (
            "Families should still limit access to trusted adults, protect their "
            "accounts and discuss how location information will be used. Privacy is "
            "both a product design choice and an everyday family responsibility."
        ),
    ),

    "/guardian/private-child-location-tracking-app/": (
        "Private access for trusted family adults",
        (
            "Guardian is designed so a connected child phone shares information "
            "inside its authorised family. It is not a public tracker and does not "
            "place child profiles into a searchable social network."
        ),
        (
            "Trusted adults can use map context, safe-zone alerts and device status "
            "for ordinary family routines. Access should be reviewed whenever family "
            "circumstances or trusted caregivers change."
        ),
    ),

    "/guardian/safe-zone-alerts-vs-constant-location-checking/": (
        "Alerts can replace many unnecessary map checks",
        (
            "Constantly refreshing a family map can create more anxiety than useful "
            "information. Home and School safe-zone alerts focus attention on the "
            "arrival and leaving moments families normally care about."
        ),
        (
            "The Family Map remains available when an alert is late or extra context "
            "is needed. This alert-first approach can support reassurance without "
            "turning location sharing into continuous observation."
        ),
    ),

    "/guardian/family-safety-app-for-school-runs/": (
        "Support the whole school journey",
        (
            "A school run includes more than arriving at the school gate. Guardian "
            "can provide updates when the connected child phone leaves Home, reaches "
            "School, leaves School and returns Home."
        ),
        (
            "Parents can use those milestones alongside the latest available map "
            "position, battery level and update time when plans change. The result "
            "is broader journey context rather than a single arrival notification."
        ),
    ),

    "/guardian/get-notified-when-child-leaves-school/": (
        "A departure alert for the journey after School",
        (
            "A School departure notification can help parents know that the next "
            "part of the day has begun—whether that means walking Home, meeting a "
            "pickup or travelling to an after-school activity."
        ),
        (
            "Leaving a safe zone does not mean the child has reached the next "
            "destination. Guardian keeps the latest available map position, battery "
            "status and update time available when parents need additional context."
        ),
    ),

    "/guardian/school-safe-zone-alerts/": (
        "How a School safe zone supports routine alerts",
        (
            "A School safe zone creates a practical boundary around the place rather "
            "than relying on one exact GPS point. Guardian can use that boundary to "
            "support arrival and leaving notifications during the normal school day."
        ),
        (
            "The boundary should allow for entrances, playgrounds and ordinary GPS "
            "drift around large buildings. Families should test it during the real "
            "journey and adjust expectations when signal or phone settings interfere."
        ),
    ),
}


PLATFORM_REPLACEMENTS = {
    "Guardian is being prepared for both platforms. Store buttons activate when official links are added.":
        "Guardian is available on Android through Google Play. The iPhone version is awaiting App Store approval.",

    "Guardian is being prepared for both platforms. The buttons will activate when the official store links are added.":
        "Guardian is available on Android through Google Play. The iPhone version is awaiting App Store approval.",

    "Guardian is being prepared for families using iPhone, Android or a mixture of both.":
        "Guardian is available on Android through Google Play, while the iPhone version is awaiting App Store approval.",

    "Final availability and store information will be shown on the official App Store and Google Play pages once the release is approved.":
        "Guardian is now available on Google Play. Final iPhone availability will be shown when the App Store release is approved.",
}


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT)

    if rel.name == "index.html":
        parent = rel.parent.as_posix()
        return "/" if parent == "." else f"/{parent}/"

    return f"/{rel.as_posix()}"


def replace_article(soup: BeautifulSoup, heading: str, paragraph_1: str, paragraph_2: str) -> bool:
    main = soup.find("main") or soup.body or soup
    h2 = main.find("h2")

    if not h2:
        return False

    h2.string = heading

    paragraphs = []
    node = h2

    while node and len(paragraphs) < 2:
        node = node.find_next()

        if not node:
            break

        if node.name == "h2":
            break

        if node.name == "p":
            paragraphs.append(node)

    if len(paragraphs) < 2:
        return False

    paragraphs[0].string = paragraph_1
    paragraphs[1].string = paragraph_2
    return True


changed_files = []
play_links_updated = 0
rewritten_pages = []
h1_pages = []
article_failures = []

html_files = sorted(GUARDIAN.rglob("*.html"))

for path in html_files:
    raw = path.read_text(encoding="utf-8", errors="replace")
    original = raw

    for old, new in PLATFORM_REPLACEMENTS.items():
        raw = raw.replace(old, new)

    soup = BeautifulSoup(raw, "html.parser")
    current_url = url_for(path)

    for anchor in soup.find_all("a"):
        label = " ".join(anchor.get_text(" ", strip=True).split())

        if re.search(r"\bGoogle\s*Play\b", label, re.I):
            anchor["href"] = PLAY_URL
            anchor["target"] = "_blank"
            anchor["rel"] = ["noopener"]
            anchor.string = "Google Play"
            play_links_updated += 1

    if current_url in H1_REPLACEMENTS:
        h1 = soup.find("h1")

        if h1:
            h1.string = H1_REPLACEMENTS[current_url]
            h1_pages.append(current_url)

    if current_url in ARTICLE_REWRITES:
        heading, p1, p2 = ARTICLE_REWRITES[current_url]

        if replace_article(soup, heading, p1, p2):
            rewritten_pages.append(current_url)
        else:
            article_failures.append(current_url)

    if current_url == "/guardian/":
        has_software_schema = False

        for script in soup.find_all(
            "script",
            attrs={"type": re.compile(r"application/ld\+json", re.I)},
        ):
            try:
                data = json.loads(script.string or script.get_text())
                text = json.dumps(data)

                if "SoftwareApplication" in text:
                    has_software_schema = True
                    break
            except Exception:
                pass

        if not has_software_schema:
            schema = {
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                "name": "Guardian",
                "applicationCategory": "LifestyleApplication",
                "operatingSystem": "Android",
                "description": (
                    "Guardian is a private family safety app with a Family Map, "
                    "Home and School alerts, recent location context, device status "
                    "and SOS tools."
                ),
                "url": "https://www.vantalabs.co.uk/guardian/",
                "downloadUrl": PLAY_URL,
                "installUrl": PLAY_URL,
                "publisher": {
                    "@type": "Organization",
                    "name": "Vanta Labs",
                    "url": "https://www.vantalabs.co.uk/",
                },
            }

            tag = soup.new_tag("script")
            tag["type"] = "application/ld+json"
            tag.string = json.dumps(schema, indent=2)

            if soup.head:
                soup.head.append(tag)
            else:
                soup.insert(0, tag)

    updated = str(soup)

    if updated != original:
        path.write_text(updated, encoding="utf-8")
        changed_files.append(str(path.relative_to(ROOT)))


if article_failures:
    print()
    print("ARTICLE UPDATE FAILURES:")
    for item in article_failures:
        print(f"  {item}")
    raise SystemExit(
        "Stopped because one or more article structures were not recognised. "
        f"Restore from: {backup}"
    )


# Validate every Guardian HTML page contains a real Google Play URL.
missing_play = []

for path in html_files:
    soup = BeautifulSoup(
        path.read_text(encoding="utf-8", errors="replace"),
        "html.parser",
    )

    matching = [
        a for a in soup.find_all("a", href=True)
        if re.search(r"\bGoogle\s*Play\b", a.get_text(" ", strip=True), re.I)
    ]

    if not matching or any(a.get("href") != PLAY_URL for a in matching):
        missing_play.append(url_for(path))


if missing_play:
    print()
    print("PAGES WITHOUT THE APPROVED PLAY LINK:")
    for item in missing_play:
        print(f"  {item}")
    raise SystemExit(
        "Play-link validation failed. "
        f"Restore from: {backup}"
    )


print()
print("Guardian local cleanup complete.")
print(f"Backup: {backup}")
print(f"HTML files changed: {len(changed_files)}")
print(f"Google Play buttons updated: {play_links_updated}")
print(f"Article pages rewritten: {len(set(rewritten_pages))}")
print(f"Duplicate H1 pages corrected: {len(set(h1_pages))}")
print("iOS remains coming soon.")
print("No commit, push or deployment was performed.")
print()
