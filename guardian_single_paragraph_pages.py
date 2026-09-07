#!/usr/bin/env python3
from pathlib import Path
import shutil
import re

ROOT = Path.cwd()
GUARDIAN = ROOT / "guardian"
CSS = GUARDIAN / "assets" / "guardian.css"
HOME = GUARDIAN / "index.html"

if not (ROOT / "index.html").exists():
    raise SystemExit("Run this from ~/Projects/vantalabs-site")
if not GUARDIAN.exists() or not CSS.exists():
    raise SystemExit("Guardian pages were not found.")

backup = ROOT / "guardian.before-single-paragraph-pass"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

summaries = {
    "family-safety-app": ("How Guardian helps", "Guardian gives parents the useful parts of a family safety app without turning everyday life into constant monitoring. A connected child phone can share its latest available location, trigger Home and School arrival or leaving alerts, show recent location history and device status, and send an SOS alert to trusted adults when something is wrong."),
    "family-location-sharing-app": ("Private family location sharing", "Guardian keeps location sharing inside a private, parent-managed family. Parents can check the latest available location from connected devices, see battery and last-update information, and use place alerts around Home or School, while adults remain in control of whether they share their own location."),
    "child-location-tracker": ("A calmer way to check location", "Guardian lets parents see the latest available location shared by a connected child phone, together with the battery level and the time of the last update. It is designed for quick reassurance and useful context rather than watching a moving map throughout the day."),
    "gps-tracker-for-kids": ("Location sharing with sensible boundaries", "Guardian turns a child phone into a private family location device with Home and School safe zones, arrival and leaving alerts, recent location history and SOS tools. It supports family awareness, but it does not promise perfect GPS accuracy or replace direct communication."),
    "safe-zone-alerts": ("Home and School alerts", "Guardian can notify trusted parents when a connected child device leaves Home, arrives at School, leaves School or returns Home. These safe-zone alerts are designed to cover the moments families usually care about without requiring anyone to keep checking the map."),
    "geofencing-app-for-families": ("Family geofencing in plain English", "Guardian uses virtual boundaries around real places such as Home and School. When a connected child device enters or leaves one of those areas, Guardian can confirm the change and send a useful arrival or departure notification to the family."),
    "sos-alert-app-for-families": ("An urgent family alert", "A connected child device can use Guardian to send an SOS alert to trusted family members, together with available location and device information. It is a family notification tool rather than an emergency service, so immediate danger should always be handled through the emergency services."),
    "location-history-for-families": ("Useful recent context", "Guardian records meaningful recent location updates from a connected child device so parents can understand more than a single map pin. Location history is most useful when it is read alongside the time of the latest update, battery status and the normal family routine."),
    "family-map-app": ("One private family map", "The Guardian Family Map shows the latest available location of connected family devices in one private place. Parents can also see useful context such as battery level and last-update time, while adult location sharing remains optional."),
    "know-when-child-arrives-at-school": ("A simple School arrival update", "Create a School safe zone in Guardian and receive a notification when the connected child phone reaches the area. It gives parents the useful reassurance that the school journey is complete without another message or repeated map checks."),
    "get-alert-child-leaves-school": ("Know when the journey home starts", "Guardian can send a leaving alert when the connected child device moves outside the School safe zone. That gives working parents and other trusted adults a clear update that the journey home has begun."),
    "get-alert-child-arrives-home": ("Know they made it back", "A Home safe-zone alert can tell the family when the connected child phone has returned to the Home area. It is a simple way to reduce the usual follow-up message asking whether they arrived safely."),
    "track-the-school-run": ("Four useful school-run updates", "Guardian follows the school run through the moments that usually matter most: leaving Home, arriving at School, leaving School and returning Home. The aim is simple reassurance through place alerts rather than constant location checking."),
    "check-child-got-home-safely": ("Reassurance at the end of the journey", "Guardian can combine a Home arrival alert with the private Family Map, recent location history and last-update information. Together, those details help a parent understand whether the connected child phone made it home without turning the whole journey into live surveillance."),
    "location-alerts-for-working-parents": ("Useful updates during the working day", "Home and School notifications can keep a working parent informed without repeatedly opening the Family Map. Guardian focuses on the routine moments that matter, while keeping location sharing private and controlled by the family."),
    "share-safety-with-another-parent": ("Keep trusted adults informed", "Guardian allows the family owner to invite another trusted parent or guardian into the private family. The right adults can then see relevant child location, place alerts, device status and SOS information without using public profiles or a social feed."),
    "location-sharing-for-separated-parents": ("Clearer information across two homes", "Guardian can help trusted co-parents share relevant child location and safety updates across separate households. The arrangement should always respect consent, legal agreements and clear boundaries around which adults can access family information."),
    "how-guardian-works": ("Simple setup, useful updates", "A parent creates the private family, adds a child profile, links the child phone with a secure setup code and enables the required permissions. Home and School safe zones can then provide arrival or leaving alerts, while the Family Map, location history, device status and SOS tools remain available when needed."),
    "set-up-child-device": ("Connect the correct child phone", "Guardian links a child device to the right family profile using a secure setup code. Once location and notification permissions are enabled, the device can share its latest available location, trigger safe-zone alerts and send SOS notifications to trusted adults."),
    "features": ("Guardian features at a glance", "Guardian brings together a private Family Map, child-device setup, Home and School safe zones, arrival and leaving alerts, recent location history, battery and last-update status, SOS notifications and trusted-adult controls. It stays focused on family location and safety rather than messages, website blocking or screen-time management."),
    "battery-and-last-update-status": ("Understand what the phone is reporting", "Guardian shows the child phone's battery level and the time of the latest location update beside the map information. That context helps parents judge whether a position is recent and whether the device is still likely to keep reporting normally."),
    "optional-parent-location-sharing": ("Adult location sharing stays optional", "Parents and guardians can choose whether to share their own location inside the connected Guardian family. Adult sharing is optional, while the family owner continues to manage access to child profiles and safety information."),
    "privacy-and-location-sharing": ("Private by design", "Guardian keeps family location sharing inside a private, parent-managed account with no public profiles, social feed, advertising or third-party ad tracking. Families should still use location sharing openly, proportionately and only with trusted adults who genuinely need access."),
    "guardian-premium": ("Premium for larger families", "Guardian's free plan supports one child profile, while Guardian Premium increases the family allowance to up to five child profiles. Billing is managed through the relevant Apple or Google app-store account."),
    "frequently-asked-questions": ("Straight answers for parents", "Guardian is a private family location and safety app for connected child devices, Home and School safe zones, arrival and leaving alerts, recent location history, device status and SOS notifications. It is not a hidden surveillance tool or an emergency service, and its accuracy can be affected by GPS, signal, permissions, battery settings and operating-system restrictions."),
    "guides/what-is-a-family-safety-app": ("A practical definition", "A family safety app should help trusted adults understand useful moments such as a child leaving Home, arriving at School or asking for help. The best tools combine private location sharing, place alerts, device status and SOS features with clear limits, honest privacy choices and a backup plan when the phone is unavailable."),
    "guides/what-is-geofencing": ("Geofencing without the jargon", "Geofencing creates a virtual boundary around a real place such as Home or School. When a connected phone enters or leaves the area, the app can recognise the change and send an arrival or leaving alert, although GPS accuracy and notification timing can still vary."),
    "guides/how-safe-zone-alerts-work": ("How the alert is created", "A safe-zone alert starts with the phone's location, a virtual boundary around a familiar place and a confirmation that the device has genuinely entered or left the area. Guardian then sends the relevant Home or School notification, subject to signal, permissions, battery settings and operating-system restrictions."),
    "guides/location-sharing-and-family-privacy": ("Use location sharing openly", "Family location sharing works best when everyone understands what is shared, who can see it and why the family uses it. Keep access limited to trusted adults, use alerts for agreed routines rather than constant checking, and review the arrangement as children grow more independent."),
    "guides/how-to-talk-to-children-about-location-sharing": ("Start with a clear conversation", "Explain what Guardian shares, which adults can see the information and why the family wants to use Home, School or SOS features. Children should understand that the app supports agreed safety routines rather than replacing trust, communication or age-appropriate independence."),
    "guides/setting-up-home-and-school-safe-zones": ("Create useful boundaries", "Place Home and School safe zones around the real arrival area, allow for ordinary GPS variation and avoid boundaries that overlap or sit too tightly against the building. Test the normal journey and adjust the zone only when there is clear evidence that it needs changing."),
    "guides/what-to-look-for-in-a-family-location-app": ("Choose clarity over feature overload", "Look for private family access, useful place alerts, clear device status, honest wording around SOS and transparent limits on GPS accuracy. A family location app should support the routine without public profiles, confusing controls or pressure to monitor every movement."),
    "guides/how-sos-alerts-work": ("Agree what happens after an SOS", "An SOS alert should reach trusted family members with clear information about the connected device and its available location. Families should agree who responds, who calls the child and when emergency services should be contacted, because no app can guarantee delivery or replace an emergency response."),
    "guides/what-to-do-when-location-does-not-update": ("Check the practical causes first", "Look at the last-update time, battery level, internet connection, location permission and background settings before assuming something is wrong. Buildings, weak signal, battery-saving modes and operating-system restrictions can all delay a location update."),
    "guides/safe-zone-alerts-vs-constant-location-checking": ("Use milestones instead of watching the map", "Home and School alerts can provide routine reassurance at agreed moments without encouraging parents to check a live location throughout the day. Open the Family Map when extra context is genuinely useful, then return to direct communication when the situation needs it.")
}

def slug_for(path: Path) -> str:
    return path.parent.relative_to(GUARDIAN).as_posix()

updated = 0

for page in GUARDIAN.rglob("index.html"):
    if page == HOME:
        continue

    slug = slug_for(page)
    if slug not in summaries:
        continue

    heading, paragraph = summaries[slug]
    text = page.read_text()

    content_start = text.find('<article class="content">')
    if content_start == -1:
        content_start = text.find('<div class="content">')
    if content_start == -1:
        raise SystemExit(f"Could not find content block in {page}")

    open_end = text.find('>', content_start) + 1
    faq_start = text.find('<section class="faq">', open_end)
    if faq_start == -1:
        raise SystemExit(f"Could not find FAQ block in {page}")

    current_content = text[open_end:faq_start]
    notice_match = re.search(r'(<div class="notice">.*?</div>)', current_content, flags=re.S)
    notice = notice_match.group(1) if notice_match else ""

    new_content = f'''
{notice}
<section class="single-copy">
<h2>{heading}</h2>
<p>{paragraph}</p>
</section>
'''

    text = text[:open_end] + new_content + text[faq_start:]
    page.write_text(text)
    updated += 1

css = CSS.read_text()
css += r'''

/* Single-paragraph detail-page layout */
.guardian-detail .content{
  padding-top:76px !important;
  padding-bottom:66px !important;
}

.guardian-detail .content .notice{
  max-width:820px;
  margin-bottom:58px !important;
}

.guardian-detail .single-copy{
  max-width:780px;
  padding:0 !important;
  border:0 !important;
}

.guardian-detail .single-copy h2{
  max-width:680px !important;
  margin:0 0 24px !important;
  font-size:clamp(34px,4.3vw,48px) !important;
  line-height:1.04 !important;
  letter-spacing:-.052em !important;
}

.guardian-detail .single-copy p{
  max-width:760px !important;
  margin:0 !important;
  color:rgba(246,239,226,.76) !important;
  font-size:19px !important;
  line-height:1.88 !important;
  letter-spacing:-.01em;
}

.guardian-detail .faq{
  padding-top:76px !important;
  border-top:1px solid var(--line);
}

.guardian-detail .related{
  margin-top:0 !important;
}

@media(max-width:760px){
  .guardian-detail .content{
    padding-top:58px !important;
    padding-bottom:54px !important;
  }

  .guardian-detail .content .notice{
    margin-bottom:42px !important;
  }

  .guardian-detail .single-copy p{
    font-size:17px !important;
    line-height:1.82 !important;
  }

  .guardian-detail .faq{
    padding-top:58px !important;
  }
}
'''

CSS.write_text(css)

print(f"Collapsed {updated} Guardian detail and guide pages into one concise paragraph.")
print("Homepage was left untouched.")
print("FAQ and related Guardian links remain in place.")
print("Nothing was committed, pushed or deployed.")
print("Refresh several Guardian subpages to review the cleaner layout.")
