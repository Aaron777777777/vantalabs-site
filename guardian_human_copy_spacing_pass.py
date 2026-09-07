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

backup = ROOT / "guardian.before-human-copy-spacing-pass"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

human_intros = {
    "family-safety-app": "Most parents are not looking to watch a map all day. They just want a clear update when a normal journey starts, finishes, or needs attention.",
    "family-location-sharing-app": "Family location sharing works best when everyone understands why it is being used. Guardian keeps the experience private, simple and centred on everyday family routines.",
    "child-location-tracker": "Sometimes a quick check is useful. Guardian shows the latest available location from a connected child device without turning the whole day into constant monitoring.",
    "gps-tracker-for-kids": "A child location app should help with reassurance, not create another source of anxiety. Guardian focuses on useful updates, familiar places and clear device status.",
    "safe-zone-alerts": "The school run is where place alerts make the most sense. Guardian can tell you when the connected child device leaves Home, reaches School, leaves School and gets back Home.",
    "geofencing-app-for-families": "Geofencing sounds technical, but the idea is simple: draw a virtual boundary around a real place and receive an update when a connected device enters or leaves it.",
    "sos-alert-app-for-families": "An SOS tool matters most when it is easy to find and easy to understand. Guardian lets a connected child device send an urgent alert to trusted family members.",
    "location-history-for-families": "A single map pin does not always tell the whole story. Recent location records can add useful context when a parent needs to understand what happened earlier.",
    "family-map-app": "The Family Map is there when you need it, not something you have to stare at. It shows the latest available location and useful device information in one private family space.",
    "know-when-child-arrives-at-school": "For many parents, the most useful notification of the day is simply knowing the school journey is complete.",
    "get-alert-child-leaves-school": "Knowing when School finishes can make the journey home feel much less uncertain, especially when a parent is working or travelling.",
    "get-alert-child-arrives-home": "A Home arrival alert can remove the need for another message asking whether they made it back safely.",
    "track-the-school-run": "Guardian follows the school run through four useful moments rather than encouraging constant location checking.",
    "check-child-got-home-safely": "The useful question is usually not where they are every second. It is simply whether they made it home.",
    "location-alerts-for-working-parents": "When you are working, you may not be able to keep opening a map. Place alerts can provide the useful update without breaking your concentration.",
    "share-safety-with-another-parent": "Family safety information is often more useful when the right adults can see the same updates and respond consistently.",
    "location-sharing-for-separated-parents": "Location sharing across two homes needs clear boundaries, trusted access and respect for existing family arrangements.",
    "how-guardian-works": "Guardian is designed to be set up once, then quietly support the family routine in the background.",
    "set-up-child-device": "Connecting the correct child phone is the most important part of setup. Guardian uses a secure code so the device is linked to the right child profile.",
    "features": "Guardian does not try to become a full parental-control suite. It stays focused on location, familiar places, device status and urgent family alerts.",
    "battery-and-last-update-status": "A location is more useful when you can see when it was last updated and whether the phone still has enough battery to keep reporting.",
    "optional-parent-location-sharing": "Adults should remain in control of whether they share their own location. Guardian keeps parent location sharing optional.",
    "privacy-and-location-sharing": "Location sharing can be genuinely helpful, but it deserves clear rules, trusted access and honest conversations inside the family.",
    "guardian-premium": "Some families need more than one child profile. Guardian Premium expands the family allowance while keeping the same simple experience.",
    "frequently-asked-questions": "These are the practical questions parents usually ask before deciding whether Guardian fits their family.",
    "guides/what-is-a-family-safety-app": "A good family safety app should make ordinary routines calmer. It should provide useful context without turning family life into constant surveillance.",
    "guides/what-is-geofencing": "Geofencing is simply a way for a phone to recognise that it has entered or left a familiar place such as Home or School.",
    "guides/how-safe-zone-alerts-work": "Safe-zone alerts combine phone location, a virtual boundary and a confirmation step before a notification is sent.",
    "guides/location-sharing-and-family-privacy": "The healthiest location-sharing arrangements are open, proportionate and understood by everyone involved.",
    "guides/how-to-talk-to-children-about-location-sharing": "The conversation matters as much as the technology. Children should know what is shared, who can see it and why the family is using it.",
    "guides/setting-up-home-and-school-safe-zones": "A safe zone should match the real place closely enough to be useful, while allowing for normal GPS variation around buildings and roads.",
    "guides/what-to-look-for-in-a-family-location-app": "The best choice is not always the app with the longest feature list. Privacy, clarity and honest limitations matter more.",
    "guides/how-sos-alerts-work": "An SOS alert should be easy to send, clear to receive and supported by an agreed family response plan.",
    "guides/what-to-do-when-location-does-not-update": "A missing update usually has a practical cause such as battery, signal, permissions or background restrictions.",
    "guides/safe-zone-alerts-vs-constant-location-checking": "For everyday routines, a useful place alert is often healthier than repeatedly opening a live map."
}

def slug_for(path: Path) -> str:
    return path.parent.relative_to(GUARDIAN).as_posix()

detail_count = 0
intro_count = 0

for page in GUARDIAN.rglob("index.html"):
    if page == HOME:
        continue

    text = page.read_text()
    text = re.sub(
        r'<a[^>]*href="/"[^>]*>\s*(?:Made by Vanta Labs|Built by Vanta Labs)\s*</a>',
        '',
        text,
        flags=re.I
    )

    slug = slug_for(page)
    intro = human_intros.get(slug)

    if intro and 'class="human-intro"' not in text:
        notice_pos = text.find('class="notice"')
        notice_end = text.find('</div>', notice_pos) if notice_pos != -1 else -1
        if notice_end != -1:
            notice_end += len('</div>')
            text = text[:notice_end] + f'\n<p class="human-intro">{intro}</p>\n' + text[notice_end:]
            intro_count += 1

    page.write_text(text)
    detail_count += 1

home = HOME.read_text()
home = home.replace(
    "Get an alert when they leave Home, arrive at School or make it back safely — with private location sharing and SOS when it matters.",
    "Get a useful update when they leave Home, arrive at School or make it back safely. Guardian keeps private location sharing, device status and SOS close when the family needs them."
)
home = home.replace(
    "Guardian is built around ordinary family journeys—not constant map checking.",
    "Most parents do not want to watch a map all day. Guardian focuses on the four everyday updates that usually matter most."
)
home = home.replace(
    "See the latest available location of connected family devices when you need context.",
    "Open the private Family Map when you need more context, and see the latest available location shared by connected family devices."
)
home = home.replace(
    "Receive Home and School alerts, and urgent SOS notifications from a connected child device.",
    "Receive Home and School alerts during ordinary journeys, with an SOS option available on the connected child device when something is wrong."
)
home = home.replace(
    "Review recent location records, battery level and the time of the latest device update.",
    "Check recent location records, the child phone's battery level and when Guardian last received an update from the device."
)
HOME.write_text(home)

css = CSS.read_text()
css += r'''

/* Human copy and breathing-room pass */
.guardian-detail .hero{
  padding-top:86px !important;
  padding-bottom:86px !important;
}

.guardian-detail .hero .ctas{
  gap:10px !important;
}

.guardian-detail .content{
  padding-top:78px !important;
  padding-bottom:58px !important;
}

.guardian-detail .human-intro{
  max-width:760px;
  margin:0 0 68px !important;
  padding:0 0 40px;
  border-bottom:1px solid var(--line);
  color:rgba(246,239,226,.84) !important;
  font-size:21px !important;
  line-height:1.75 !important;
  letter-spacing:-.015em;
}

.guardian-detail .content .notice{
  margin-bottom:44px !important;
  color:rgba(246,239,226,.62) !important;
  font-size:14px !important;
  line-height:1.7 !important;
}

.guardian-detail .content section{
  padding:52px 0 56px !important;
}

.guardian-detail .content section + section{
  margin-top:12px;
}

.guardian-detail .content h2{
  max-width:680px !important;
  margin-bottom:22px !important;
}

.guardian-detail .content p{
  max-width:720px !important;
  margin-top:0 !important;
  font-size:17px !important;
  line-height:1.9 !important;
}

.guardian-detail .content p + p{
  margin-top:22px !important;
}

.guardian-detail .faq{
  padding-top:54px !important;
  padding-bottom:80px !important;
}

.guardian-detail .faq h2{
  margin-bottom:32px !important;
}

.guardian-detail .faq details{
  padding:24px 0 !important;
}

.guardian-detail .related{
  padding-top:82px !important;
  padding-bottom:94px !important;
}

.guardian-detail .related h2{
  margin-bottom:38px !important;
}

.guardian-detail .related .card{
  padding-top:26px !important;
  padding-bottom:28px !important;
}

#routine.section,
#features.section,
#privacy.section{
  padding-top:104px !important;
  padding-bottom:104px !important;
}

#routine .section-head,
#features .section-head{
  margin-bottom:54px !important;
}

#routine .section-head p,
#features .section-head p{
  max-width:680px;
}

#features .feature-list{
  padding-top:8px;
}

#features .feature{
  padding-top:40px !important;
  padding-bottom:22px !important;
}

#features .feature p{
  max-width:330px;
  line-height:1.82 !important;
}

#privacy .privacy{
  padding-top:14px;
  padding-bottom:14px;
}

#privacy .privacy-copy-left p{
  line-height:1.85 !important;
}

.faq-mini{
  padding-top:96px !important;
  padding-bottom:98px !important;
}

.faq-mini-head{
  margin-bottom:38px !important;
}

.faq-mini details{
  padding-top:25px !important;
  padding-bottom:25px !important;
}

.related{
  padding-top:90px !important;
  padding-bottom:100px !important;
}

.related-head{
  margin-bottom:48px !important;
}

.explore-link{
  padding-top:30px !important;
  padding-bottom:34px !important;
}

@media(max-width:760px){
  .guardian-detail .human-intro{
    margin-bottom:46px !important;
    padding-bottom:30px;
    font-size:19px !important;
  }

  .guardian-detail .content section{
    padding:40px 0 44px !important;
  }

  #routine.section,
  #features.section,
  #privacy.section{
    padding-top:72px !important;
    padding-bottom:72px !important;
  }
}
'''

CSS.write_text(css)

print(f"Updated {detail_count} Guardian detail and guide pages.")
print(f"Added tailored human introductions to {intro_count} pages.")
print("Removed the redundant Made/Built by Vanta Labs CTA from all detail pages.")
print("Improved homepage copy and spacing.")
print("Nothing was committed, pushed or deployed.")
print("Refresh the Guardian homepage and several subpages.")
