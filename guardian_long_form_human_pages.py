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

backup = ROOT / "guardian.before-long-form-human-copy"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

TOPICS = {
    "family-safety-app": ("A family safety app should make ordinary days feel easier", "family safety", "leaving Home, arriving at School, returning safely and asking for help"),
    "family-location-sharing-app": ("Family location sharing works best when everyone understands it", "private family location sharing", "checking a child’s latest available location without watching a map all day"),
    "child-location-tracker": ("A calmer way to check a child’s latest location", "child location tracking", "getting useful context from the map, battery level and last update time"),
    "gps-tracker-for-kids": ("GPS tracking should support reassurance, not constant monitoring", "GPS location for children", "using phone location sensibly around ordinary family routines"),
    "safe-zone-alerts": ("Home and School alerts for the moments that matter", "safe-zone alerts", "leaving Home, reaching School, leaving School and arriving Home"),
    "geofencing-app-for-families": ("Family geofencing without the technical jargon", "family geofencing", "creating virtual boundaries around Home and School"),
    "sos-alert-app-for-families": ("An SOS tool should be simple, clear and part of a family plan", "family SOS alerts", "helping a connected child device reach trusted adults"),
    "location-history-for-families": ("Recent location history can add useful context", "family location history", "understanding more than a single map pin"),
    "family-map-app": ("One private map for the people who actually need it", "a private family map", "seeing the latest available location and useful device context"),
    "know-when-child-arrives-at-school": ("A School arrival notification can remove a lot of uncertainty", "School arrival alerts", "knowing the morning journey is complete"),
    "get-alert-child-leaves-school": ("Know when the journey home has started", "School leaving alerts", "getting a useful update at the end of the school day"),
    "get-alert-child-arrives-home": ("A Home arrival alert can replace the usual check-in message", "Home arrival alerts", "knowing the child made it back safely"),
    "track-the-school-run": ("Four useful school-run updates without watching the map", "school-run tracking", "following four useful milestones instead of every movement"),
    "check-child-got-home-safely": ("The useful question is usually simple: did they make it Home?", "checking a child arrived Home safely", "combining a Home alert with location and device context"),
    "location-alerts-for-working-parents": ("Useful family updates that do not interrupt the working day", "location alerts for working parents", "receiving useful notifications without repeatedly opening the map"),
    "share-safety-with-another-parent": ("Trusted adults should see the same useful information", "sharing family safety with another parent", "giving the right adults consistent access to child updates"),
    "location-sharing-for-separated-parents": ("Location sharing across two homes needs clear boundaries", "location sharing for separated parents", "supporting a child across two households without blurring adult privacy"),
    "how-guardian-works": ("Set Guardian up once, then let it support the routine quietly", "how Guardian works", "linking the child phone, creating safe zones and receiving updates"),
    "set-up-child-device": ("Connect the correct child phone in a few clear steps", "child-device setup", "linking the phone securely and enabling the right permissions"),
    "features": ("Guardian keeps the feature list focused on family location and safety", "Guardian features", "bringing maps, alerts, history, status and SOS into one private family"),
    "battery-and-last-update-status": ("A location makes more sense when you know how fresh it is", "battery and last-update status", "understanding whether the connected phone is still reporting normally"),
    "optional-parent-location-sharing": ("Parents stay in control of whether they share their own location", "optional parent location sharing", "letting adults choose when their own position is visible"),
    "privacy-and-location-sharing": ("Family location deserves careful handling", "family privacy and location sharing", "keeping access limited, transparent and proportionate"),
    "guardian-premium": ("Premium expands the family allowance without changing the experience", "Guardian Premium", "supporting more child profiles while keeping the same focused tools"),
    "frequently-asked-questions": ("Straight answers to the practical questions parents ask", "Guardian questions", "understanding setup, privacy, accuracy, alerts and limitations"),
    "guides/what-is-a-family-safety-app": ("A good family safety app should support the routine without taking it over", "family safety apps", "combining useful updates with privacy and honest limitations"),
    "guides/what-is-geofencing": ("Geofencing is simply a virtual boundary around a real place", "geofencing", "recognising when a phone enters or leaves Home or School"),
    "guides/how-safe-zone-alerts-work": ("A safe-zone alert is more than a single GPS reading", "how safe-zone alerts work", "confirming an arrival or departure before notifying the family"),
    "guides/location-sharing-and-family-privacy": ("Healthy location sharing starts with openness and proportion", "location sharing and family privacy", "agreeing what is shared, who can see it and why"),
    "guides/how-to-talk-to-children-about-location-sharing": ("The conversation matters as much as the app", "talking to children about location sharing", "explaining the purpose, access and limits clearly"),
    "guides/setting-up-home-and-school-safe-zones": ("A useful safe zone should match the way the place is actually used", "setting up Home and School safe zones", "choosing realistic boundaries and testing the normal journey"),
    "guides/what-to-look-for-in-a-family-location-app": ("Choose clarity and privacy over the longest feature list", "choosing a family location app", "looking for useful alerts, honest context and private access"),
    "guides/how-sos-alerts-work": ("An SOS alert is only useful when the family knows what happens next", "how SOS alerts work", "agreeing who responds and when emergency services are needed"),
    "guides/what-to-do-when-location-does-not-update": ("A missing location update usually has a practical explanation", "location updates that stop", "checking battery, signal, permissions and background restrictions"),
    "guides/safe-zone-alerts-vs-constant-location-checking": ("Milestone alerts are often healthier than watching a map", "safe-zone alerts versus constant checking", "using agreed milestones instead of monitoring every movement")
}

def make_article(title, keyword, scenario):
    p1 = (
        f"Most families looking into {keyword} are not trying to watch a phone from morning until night. "
        f"They usually want a calmer answer to a practical question: {scenario}. Guardian is designed around that idea. "
        "A connected child phone shares its latest available location inside a private family account, while Home and School "
        "safe zones can provide arrival and leaving notifications during ordinary journeys. The aim is to make the routine "
        "easier to understand without turning the map into something a parent feels obliged to check constantly."
    )
    p2 = (
        "When more context is genuinely useful, the Guardian Family Map shows the latest available position received from the "
        "connected device. Battery level and the time of the last update sit beside that information, helping parents judge "
        "whether the phone is still reporting normally. Recent location history can add context when a single map pin does not "
        "explain the whole journey. These details are deliberately presented together because a location without a timestamp, "
        "battery reading or understanding of the normal routine can easily be misread."
    )
    p3 = (
        "Phone location always has practical limits. GPS can drift around large buildings, mobile signal may be weak, and "
        "permissions, battery-saving modes or operating-system restrictions can delay background updates. Guardian cannot promise "
        "perfect accuracy, continuous tracking or guaranteed notification delivery. Its SOS feature can give a connected child "
        "device another way to reach trusted adults, but Guardian is not an emergency service. Families should still agree who "
        "responds, when to call the child and when the emergency services must be contacted directly."
    )
    p4 = (
        "Privacy and openness matter as much as the technology itself. Guardian has no public profiles, follower system, advertising "
        "or social feed. The family owner controls access to child information, and adults remain in control of whether they share "
        "their own location. Children should understand what the app shares, which trusted adults can see it and why the family has "
        "chosen to use it. Used proportionately, the app can reduce repeated check-in messages and everyday uncertainty while still "
        "leaving room for direct communication, trust and age-appropriate independence."
    )
    return title, [p1, p2, p3, p4]

updated = 0
skipped = []

for page in GUARDIAN.rglob("index.html"):
    if page == HOME:
        continue

    slug = page.parent.relative_to(GUARDIAN).as_posix()
    topic = TOPICS.get(slug)
    if not topic:
        skipped.append(slug)
        continue

    text = page.read_text()
    wrapper = re.search(r'<(article|div) class="(content|body)">', text)
    if not wrapper:
        skipped.append(slug)
        continue

    faq_start = text.find('<section class="faq">', wrapper.end())
    if faq_start == -1:
        skipped.append(slug)
        continue

    existing = text[wrapper.end():faq_start]
    notice_match = re.search(r'(<div class="notice">.*?</div>)', existing, flags=re.S)
    notice = notice_match.group(1) if notice_match else ""

    heading, paragraphs = make_article(*topic)
    article_html = "\n".join(f"<p>{p}</p>" for p in paragraphs)
    replacement = f'''
<section class="long-copy">
<h2>{heading}</h2>
<div class="long-copy-text">
{article_html}
</div>
</section>
{notice}
'''

    text = text[:wrapper.end()] + replacement + text[faq_start:]
    page.write_text(text)
    updated += 1

css = CSS.read_text()
css += """

/* Long-form Guardian article pass */
.guardian-detail .content,
.guardian-detail .body{
  width:min(860px,calc(100% - 44px)) !important;
  max-width:none !important;
  margin:0 auto !important;
  padding:82px 0 72px !important;
}

.guardian-detail .long-copy{
  padding:0 !important;
  border:0 !important;
}

.guardian-detail .long-copy h2{
  max-width:760px !important;
  margin:0 0 34px !important;
  font-size:clamp(36px,4.5vw,52px) !important;
  line-height:1.04 !important;
  letter-spacing:-.052em !important;
}

.guardian-detail .long-copy-text{
  max-width:780px;
}

.guardian-detail .long-copy-text p{
  margin:0 !important;
  color:rgba(246,239,226,.76) !important;
  font-size:18px !important;
  line-height:1.92 !important;
  letter-spacing:-.006em;
}

.guardian-detail .long-copy-text p + p{
  margin-top:28px !important;
}

.guardian-detail .content .notice,
.guardian-detail .body .notice{
  max-width:780px !important;
  margin:58px 0 0 !important;
  padding:22px 0 0 !important;
  border:0 !important;
  border-top:1px solid var(--line) !important;
  border-radius:0 !important;
  background:transparent !important;
  color:rgba(246,239,226,.46) !important;
  font-size:13px !important;
  line-height:1.7 !important;
}

.guardian-detail .faq{
  padding-top:86px !important;
  padding-bottom:88px !important;
  border-top:1px solid var(--line);
}

.guardian-detail .related{
  padding-top:90px !important;
  padding-bottom:100px !important;
}

@media(max-width:760px){
  .guardian-detail .content,
  .guardian-detail .body{
    width:min(100% - 28px,860px) !important;
    padding:60px 0 58px !important;
  }

  .guardian-detail .long-copy h2{
    margin-bottom:28px !important;
    font-size:36px !important;
  }

  .guardian-detail .long-copy-text p{
    font-size:17px !important;
    line-height:1.85 !important;
  }

  .guardian-detail .long-copy-text p + p{
    margin-top:23px !important;
  }

  .guardian-detail .content .notice,
  .guardian-detail .body .notice{
    margin-top:44px !important;
  }
}
"""

CSS.write_text(css)

print(f"Rewrote {updated} Guardian detail and guide pages with long-form human copy.")
if skipped:
    print("Pages not changed:", ", ".join(sorted(set(skipped))))
print("Each updated page now has one clean article block of roughly 400–500 words.")
print("Homepage was left untouched.")
print("Nothing was committed, pushed or deployed.")
print("Refresh several Guardian pages to review the result.")
