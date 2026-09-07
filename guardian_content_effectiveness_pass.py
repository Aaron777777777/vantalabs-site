#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import hashlib
import re
import shutil

from bs4 import BeautifulSoup


ROOT = Path.home() / "Projects" / "vantalabs-site"
GUARDIAN = ROOT / "guardian"

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
BACKUP = ROOT / f"guardian.before-content-effectiveness-pass-{timestamp}"


ARTICLE_REWRITES = {
    "/guardian/family-locator-app/": (
        "One private view for connected family devices",
        (
            "Guardian’s Family Map brings authorised family devices into one "
            "parent-managed view. Trusted adults can check each connected phone’s "
            "latest available location, battery level and last update time without "
            "placing family information on a public social map."
        ),
        (
            "Home and School alerts help reduce routine map checking, while optional "
            "adult location sharing lets parents decide whether their own position "
            "should appear. The focus is coordination between trusted family adults."
        ),
    ),

    "/guardian/real-time-child-location-app/": (
        "What real-time phone location can realistically mean",
        (
            "Guardian displays the latest location successfully shared by the "
            "connected child phone. Updates can be frequent when signal, permissions "
            "and background activity are working normally, but no phone app can "
            "promise a perfectly continuous live position."
        ),
        (
            "Battery level and last-update time help parents judge how current the "
            "map information is. Buildings, weak mobile coverage and operating-system "
            "restrictions can all delay an otherwise normal update."
        ),
    ),

    "/guardian/see-my-childs-location-app/": (
        "A quick location check when plans change",
        (
            "When a pickup is late or a familiar journey changes, Guardian lets a "
            "trusted adult check the connected child phone’s latest available "
            "location. The map also shows battery status and when the phone last "
            "reported."
        ),
        (
            "This page is about the direct task of checking the map, rather than "
            "watching a journey continuously. Home and School alerts can handle many "
            "routine updates without repeated manual checks."
        ),
    ),

    "/guardian/share-child-location-with-another-parent/": (
        "Give another trusted parent access to the same family",
        (
            "Guardian allows authorised adults to use the same private family account "
            "when responsibility is shared between parents or caregivers. This avoids "
            "sending screenshots or repeatedly forwarding location updates."
        ),
        (
            "Access should only be given to people the family trusts and reviewed when "
            "circumstances change. Adult location sharing remains optional, even when "
            "an adult can view an authorised child device."
        ),
    ),

    "/guardian/app-that-tells-me-when-my-child-gets-to-school/": (
        "A simple answer to one school-run question",
        (
            "Guardian can notify trusted adults when a connected child phone reaches "
            "the family’s School safe zone. That provides a clear arrival update "
            "without requiring the parent to keep refreshing the Family Map."
        ),
        (
            "The notification reflects the phone crossing the configured boundary, "
            "not a guarantee that the child has entered a particular classroom. GPS, "
            "signal and background phone settings can affect timing."
        ),
    ),

    "/guardian/notify-me-when-my-child-gets-to-school/": (
        "Use a School arrival alert instead of repeated messages",
        (
            "A Guardian School arrival notification can replace the familiar stream "
            "of ‘Are you there yet?’ messages during an ordinary school run. Trusted "
            "adults receive an update when the connected phone reaches the safe zone."
        ),
        (
            "Families should test the School boundary around the real entrances and "
            "grounds. Large buildings and GPS drift may mean the most useful boundary "
            "is wider than one exact point on the map."
        ),
    ),

    "/guardian/get-notified-when-child-arrives-at-school/": (
        "How Guardian detects arrival at School",
        (
            "Guardian compares the child phone’s reported location with the family’s "
            "configured School safe zone. Once the arrival is confirmed, trusted "
            "adults can receive a notification that the phone has reached the area."
        ),
        (
            "Permissions, connectivity and battery optimisation influence how quickly "
            "the phone reports. The latest map position, battery level and update time "
            "remain available when more context is needed."
        ),
    ),

    "/guardian/child-location-alerts-for-school/": (
        "Arrival and departure alerts across the school day",
        (
            "Guardian’s School alerts cover both sides of the routine: reaching School "
            "and leaving it later. This broader view is useful for families who want "
            "the main journey milestones rather than one arrival notification."
        ),
        (
            "Leaving School only means the connected phone has moved outside the safe "
            "zone. It does not mean the child has reached Home, a pickup point or an "
            "after-school activity."
        ),
    ),

    "/guardian/school-arrival-notification-app/": (
        "School arrival notifications built around a safe zone",
        (
            "Guardian uses a family-defined School safe zone to support arrival "
            "notifications. A practical boundary can account for entrances, grounds "
            "and ordinary GPS movement around a large school building."
        ),
        (
            "Parents can combine that alert with the latest available Family Map "
            "position and device status when necessary. Guardian is designed to "
            "provide useful routine context rather than guaranteed attendance records."
        ),
    ),

    "/guardian/school-run-safety-app/": (
        "Follow the four useful moments in the school run",
        (
            "Guardian can support the full routine: leaving Home, arriving at School, "
            "leaving School and returning Home. These milestones give parents a calmer "
            "overview of the journey without requiring continuous map watching."
        ),
        (
            "The app also provides recent location context, battery status and last "
            "update time when a journey differs from the normal pattern. Direct family "
            "communication remains important whenever plans change."
        ),
    ),

    "/guardian/app-that-tells-me-when-my-child-leaves-home/": (
        "Know when the journey away from Home begins",
        (
            "Guardian can notify trusted adults when the connected child phone leaves "
            "the family’s Home safe zone. This can confirm that a school journey, walk "
            "or pickup routine has started."
        ),
        (
            "A leaving alert does not describe the child’s final destination. Parents "
            "can use later School or Home alerts—and the Family Map when necessary—to "
            "understand the rest of the journey."
        ),
    ),

    "/guardian/get-notified-when-child-gets-home/": (
        "A Home arrival update at the end of the journey",
        (
            "Guardian can send a notification when the connected child phone returns "
            "to the Home safe zone. This gives families a useful end-of-journey update "
            "without relying on another message or call."
        ),
        (
            "Arrival timing can be influenced by GPS accuracy, signal and background "
            "phone settings. The device’s battery level and last update time provide "
            "additional context if the alert appears delayed."
        ),
    ),

    "/guardian/family-place-alerts-app/": (
        "Useful alerts for the places a family chooses",
        (
            "Place alerts are most helpful when they represent meaningful family "
            "routines. Guardian centres on Home and School, giving trusted adults "
            "updates around the locations they are most likely to care about daily."
        ),
        (
            "The goal is not to create a notification for every movement. Carefully "
            "chosen boundaries can provide reassurance while keeping alerts relevant "
            "and manageable."
        ),
    ),

    "/guardian/geofence-alerts-app-for-parents/": (
        "What parents receive when a safe-zone event occurs",
        (
            "Guardian turns confirmed safe-zone arrivals and departures into clear "
            "parent-facing notifications. The alert identifies the connected child "
            "phone and whether it entered or left the relevant place."
        ),
        (
            "Parents can then decide whether the alert is enough or whether they need "
            "to open the Family Map. This notification-first workflow reduces the need "
            "to repeatedly check the map during familiar routines."
        ),
    ),

    "/guardian/gps-geofence-app-for-kids/": (
        "How the child phone supports geofence alerts",
        (
            "The connected child phone supplies the location reports Guardian uses to "
            "evaluate Home and School boundaries. Location permission, background "
            "access, battery optimisation and connectivity all affect that process."
        ),
        (
            "A geofence is an area rather than a single perfect GPS coordinate. The "
            "boundary should allow for normal signal variation, especially around "
            "large buildings and busy school grounds."
        ),
    ),

    "/guardian/child-safety-app-with-sos/": (
        "Everyday family safety tools with an SOS option",
        (
            "Guardian combines routine tools such as Home and School alerts, a private "
            "Family Map and device status with an SOS option on the connected child "
            "device. SOS is one part of the wider family-safety experience."
        ),
        (
            "Families should agree when the child should use SOS, which trusted adult "
            "will respond and when emergency services must be contacted directly. "
            "Guardian itself is not an emergency service."
        ),
    ),

    "/guardian/child-sos-alert-app/": (
        "What happens after a child presses SOS",
        (
            "When SOS is activated on a connected child device, Guardian can alert "
            "trusted family adults and include the latest available location and "
            "device context. That information can help the family decide who should "
            "call, travel or seek further assistance."
        ),
        (
            "Notification delivery and location accuracy cannot be guaranteed. In an "
            "immediate emergency, the child or responding adult should contact the "
            "emergency services directly."
        ),
    ),
}


META_OVERRIDES = {
    "/guardian/family-locator-app/":
        "View connected family devices on Guardian’s private map, with latest location, battery status, safe-zone alerts and optional adult sharing.",

    "/guardian/real-time-child-location-app/":
        "Understand how Guardian shows a child phone’s latest reported location, including battery status, update time and the limits of live GPS.",

    "/guardian/see-my-childs-location-app/":
        "Check a connected child phone’s latest available location, battery level and update time inside Guardian’s private Family Map.",

    "/guardian/share-child-location-with-another-parent/":
        "Give another trusted parent access to an authorised child device inside the same private, parent-managed Guardian family.",

    "/guardian/app-that-tells-me-when-my-child-gets-to-school/":
        "Receive a Guardian alert when a connected child phone reaches the family’s School safe zone, without continuously watching the map.",

    "/guardian/notify-me-when-my-child-gets-to-school/":
        "Replace repeated school-run check-ins with a Guardian notification when the connected child phone reaches the School safe zone.",

    "/guardian/get-notified-when-child-arrives-at-school/":
        "Learn how Guardian confirms that a connected child phone has reached the family’s configured School safe zone.",

    "/guardian/child-location-alerts-for-school/":
        "Use Guardian arrival and departure alerts to follow the main School milestones without checking the Family Map all day.",

    "/guardian/school-arrival-notification-app/":
        "Create a practical School safe zone and receive Guardian arrival notifications with location, battery and last-update context.",

    "/guardian/school-run-safety-app/":
        "Follow leaving Home, arriving at School, leaving School and returning Home with Guardian’s private family alerts and map context.",

    "/guardian/app-that-tells-me-when-my-child-leaves-home/":
        "Receive a Guardian alert when the connected child phone leaves the Home safe zone and begins its next journey.",

    "/guardian/get-notified-when-child-gets-home/":
        "Get a Guardian notification when the connected child phone returns to the family’s Home safe zone.",

    "/guardian/family-place-alerts-app/":
        "Use Guardian place alerts for meaningful family routines, centred on Home, School and the journeys between them.",

    "/guardian/geofence-alerts-app-for-parents/":
        "Receive clear parent-facing Guardian notifications when a connected child phone enters or leaves a configured safe zone.",

    "/guardian/gps-geofence-app-for-kids/":
        "Learn how a connected child phone’s GPS, permissions and background settings support Guardian safe-zone alerts.",

    "/guardian/child-safety-app-with-sos/":
        "Combine Guardian’s private Family Map, Home and School alerts, device status and child-device SOS option in one family safety app.",

    "/guardian/child-sos-alert-app/":
        "See what Guardian sends to trusted family adults after SOS is activated on a connected child device.",
}


def page_url(path: Path) -> str:
    relative = path.relative_to(ROOT)

    if relative.name == "index.html":
        parent = relative.parent.as_posix()
        return "/" if parent == "." else f"/{parent}/"

    return f"/{relative.as_posix()}"


def tidy(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def shorten(text: str, limit: int = 158) -> str:
    text = tidy(text)

    if len(text) <= limit:
        return text

    trimmed = text[:limit + 1].rsplit(" ", 1)[0]
    return trimmed.rstrip(" ,;:-") + "."


def natural_topic(path: Path) -> str:
    slug = path.parent.name.replace("-", " ")
    return slug


def generated_description(path: Path, soup: BeautifulSoup) -> str:
    topic = natural_topic(path)
    h1 = soup.find("h1")
    heading = tidy(h1.get_text(" ", strip=True) if h1 else topic)

    templates = []

    if any(word in topic for word in ("school", "school run")):
        templates = [
            f"Learn how Guardian supports {topic} with School safe-zone alerts, private map context, battery status and honest GPS limitations.",
            f"Use Guardian for {topic}, with useful arrival or departure alerts and the connected phone’s latest available device context.",
            f"Explore {topic} through Guardian’s private family alerts, School safe zones and latest reported location information.",
        ]

    elif any(word in topic for word in ("home", "gets home", "leaves home")):
        templates = [
            f"Use Guardian for {topic}, with Home safe-zone notifications, private map context and the child phone’s latest update status.",
            f"Learn how Guardian supports {topic} through Home arrival or departure alerts and useful device information.",
            f"Get clearer context around {topic} with Guardian’s private Home alerts, Family Map and battery status.",
        ]

    elif any(word in topic for word in ("sos", "emergency")):
        templates = [
            f"Learn how Guardian supports {topic}, including trusted-adult alerts, latest location context and clear emergency limitations.",
            f"Explore Guardian’s approach to {topic}, with child-device alerts, family context and guidance on when to contact emergency services.",
            f"Understand {topic} in Guardian, including what trusted adults receive and why SOS delivery cannot be guaranteed.",
        ]

    elif any(word in topic for word in ("privacy", "private", "data")):
        templates = [
            f"Understand Guardian’s approach to {topic}, with parent-managed access, no public profiles and optional adult location sharing.",
            f"Learn how Guardian handles {topic} inside a private family account controlled by trusted adults.",
            f"Explore {topic} with Guardian’s private family access, clear sharing controls and no public social map.",
        ]

    elif any(word in topic for word in ("geofence", "safe zone", "place alert")):
        templates = [
            f"Learn how Guardian uses {topic} for meaningful Home and School arrival or departure notifications.",
            f"Explore {topic} with Guardian, including practical boundaries, GPS limitations and parent-facing alerts.",
            f"Use Guardian {topic} to reduce repeated map checks during familiar Home and School routines.",
        ]

    elif any(word in topic for word in ("android", "iphone", "ios")):
        templates = [
            f"Learn how Guardian supports {topic}, including location permissions, background settings and cross-platform family access.",
            f"Explore Guardian for {topic}, with private family sharing, safe-zone alerts and device configuration guidance.",
            f"Understand how {topic} works with Guardian’s Family Map, alerts and background location requirements.",
        ]

    elif any(word in topic for word in (
        "setup", "set up", "not update", "battery", "permissions",
        "troubleshooting", "location history"
    )):
        templates = [
            f"Get practical guidance for {topic} in Guardian, including permissions, battery settings and latest-update context.",
            f"Learn how to manage {topic} in Guardian and check the phone settings that affect background location reporting.",
            f"Use this Guardian guide to understand {topic}, device status and common causes of delayed location updates.",
        ]

    elif any(word in topic for word in ("best", "alternative", "compare", "vs ")):
        templates = [
            f"Compare {topic} by privacy, useful alerts, device context and realistic location expectations with Guardian.",
            f"See what families should consider when researching {topic}, from access controls to safe-zone alerts and GPS limitations.",
            f"Evaluate {topic} using Guardian’s private Family Map, Home and School alerts and parent-managed access as practical examples.",
        ]

    elif any(word in topic for word in ("location", "tracker", "locator", "map", "gps")):
        templates = [
            f"Explore {topic} with Guardian’s private Family Map, latest location, battery status and Home and School alerts.",
            f"Learn how Guardian supports {topic} with parent-managed access, useful device context and honest GPS limitations.",
            f"Use Guardian for {topic}, with the connected phone’s latest available position, battery level and update time.",
        ]

    else:
        templates = [
            f"Learn how {heading.lower()} works in Guardian’s private, parent-managed family with useful alerts and device context.",
            f"Explore {topic} with Guardian’s private family access, practical notifications and honest location limitations.",
            f"Understand {topic} through Guardian’s Family Map, device status and parent-controlled sharing.",
        ]

    digest = hashlib.sha256(page_url(path).encode()).hexdigest()
    index = int(digest[:2], 16) % len(templates)

    return shorten(templates[index])


def replace_article(
    soup: BeautifulSoup,
    heading: str,
    paragraph_one: str,
    paragraph_two: str,
) -> bool:
    main = soup.find("main") or soup.body or soup

    long_copy = main.find(
        "section",
        class_=lambda classes:
            classes and "long-copy" in classes
            if isinstance(classes, list)
            else classes == "long-copy",
    )

    section = long_copy or main
    h2 = section.find("h2")

    if not h2:
        return False

    paragraphs = section.find_all("p", limit=2)

    if len(paragraphs) < 2:
        return False

    h2.string = heading
    paragraphs[0].string = paragraph_one
    paragraphs[1].string = paragraph_two

    return True


if not GUARDIAN.is_dir():
    raise SystemExit(f"Guardian directory not found: {GUARDIAN}")

if BACKUP.exists():
    raise SystemExit(f"Backup already exists: {BACKUP}")

print(f"Creating backup:\n  {BACKUP}")
shutil.copytree(GUARDIAN, BACKUP)

changed_files = []
metadata_changed = 0
articles_changed = 0
article_failures = []

for path in sorted(GUARDIAN.rglob("*.html")):
    raw = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(raw, "html.parser")
    url = page_url(path)
    touched = False

    description_tag = soup.find(
        "meta",
        attrs={"name": re.compile(r"^description$", re.I)},
    )

    if description_tag:
        old_description = tidy(description_tag.get("content", ""))

        if old_description.lower().startswith("explore "):
            new_description = META_OVERRIDES.get(
                url,
                generated_description(path, soup),
            )

            if new_description != old_description:
                description_tag["content"] = new_description
                metadata_changed += 1
                touched = True

        og_description = soup.find(
            "meta",
            attrs={"property": re.compile(r"^og:description$", re.I)},
        )

        if og_description:
            current_meta = description_tag.get("content", "")

            if og_description.get("content", "") != current_meta:
                og_description["content"] = current_meta
                touched = True

    if url in ARTICLE_REWRITES:
        heading, paragraph_one, paragraph_two = ARTICLE_REWRITES[url]

        if replace_article(
            soup,
            heading,
            paragraph_one,
            paragraph_two,
        ):
            articles_changed += 1
            touched = True
        else:
            article_failures.append(url)

    if touched:
        path.write_text(str(soup), encoding="utf-8")
        changed_files.append(str(path.relative_to(ROOT)))


if article_failures:
    print()
    print("Could not recognise the article structure on:")
    for url in article_failures:
        print(f"  {url}")

    raise SystemExit(
        f"Stopped. Restore Guardian from backup if required:\n{BACKUP}"
    )


print()
print("Guardian content-effectiveness pass complete.")
print(f"Backup: {BACKUP}")
print(f"HTML files changed: {len(changed_files)}")
print(f"Meta descriptions rewritten: {metadata_changed}")
print(f"Overlapping article pages rewritten: {articles_changed}")
print("URLs, canonicals, sitemap and page layout were preserved.")
print("No commit, push or deployment was performed.")
print()
