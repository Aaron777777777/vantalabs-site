#!/usr/bin/env python3
from pathlib import Path
import shutil,re,json,html,difflib
ROOT=Path.cwd(); G=ROOT/"guardian"; CSS=G/"assets"/"guardian.css"; SM=ROOT/"sitemap.xml"; SITE="https://www.vantalabs.co.uk"
if not (ROOT/"index.html").exists(): raise SystemExit("Run from ~/Projects/vantalabs-site")
if not G.exists() or not CSS.exists() or not SM.exists(): raise SystemExit("Guardian files or sitemap.xml not found.")
B=ROOT/"guardian.before-90-page-seo-system"
if B.exists(): shutil.rmtree(B)
shutil.copytree(G,B); shutil.copy2(SM,ROOT/"sitemap.before-90-page-seo-system.xml")
RAW=r"""child-tracker-app|Child Tracker App|A calmer child tracker app for everyday family routines|child tracking
child-locator-app|Child Locator App|A private child locator app for the moments that matter|child location
kids-safety-app|Kids Safety App|A kids safety app built around real journeys|kids safety
family-locator-app|Family Locator App|A private family locator app without the social noise|family location
family-tracker-app|Family Tracker App|A family tracker app that stays focused|family tracking
child-gps-tracker-app|Child GPS Tracker App|A child GPS tracker app with useful context|child GPS tracking
kids-gps-tracker-app|Kids GPS Tracker App|A kids GPS tracker app for ordinary family life|kids GPS tracking
child-location-app|Child Location App|A child location app for quick reassurance|child location sharing
family-location-sharing-app|Family Location Sharing App|Private family location sharing, kept simple|family location sharing
location-sharing-app-for-parents|Location Sharing App for Parents|Location sharing for parents who want useful updates|parent location sharing
parent-child-location-app|Parent and Child Location App|A parent and child location app with clear boundaries|parent child location
gps-tracker-for-kids|GPS Tracker for Kids|GPS tracking for kids without constant map watching|GPS tracker for kids
gps-tracker-for-children|GPS Tracker for Children|A GPS tracker for children that respects family privacy|GPS tracker for children
phone-tracker-for-kids|Phone Tracker for Kids|Use the child phone for useful family location updates|phone tracker for kids
find-my-child-app|Find My Child App|A find my child app for agreed family routines|find my child app
family-safety-app|Family Safety App|Family safety without turning life into surveillance|family safety app
private-family-locator-app|Private Family Locator App|A private family locator app with no public profiles|private family locator
private-child-location-tracking-app|Private Child Location Tracking App|Private child location tracking with sensible limits|private child tracking
parent-controlled-family-locator-app|Parent-Controlled Family Locator App|A parent-controlled family locator for trusted adults|parent controlled family locator
family-location-sharing-without-social-features|Family Location Sharing Without Social Features|Family location sharing without followers, feeds or adverts|private family sharing
location-sharing-for-separated-parents|Location Sharing for Separated Parents|Clearer child location updates across two homes|separated parents location sharing
share-child-location-with-another-parent|Share Child Location With Another Parent|Share useful child safety updates with another trusted parent|shared parenting location
optional-parent-location-sharing|Optional Parent Location Sharing|Parents stay in control of whether they share their own location|optional parent sharing
family-location-data-privacy|Family Location Data Privacy|Family location data should stay carefully controlled|family location privacy
responsible-child-location-tracking|Responsible Child Location Tracking|Use child location tracking openly and proportionately|responsible child tracking
location-tracking-and-child-independence|Location Tracking and Child Independence|Location sharing that leaves room for growing independence|child independence and tracking
safe-zone-alerts-app|Safe Zone Alerts App|Safe-zone alerts for Home, School and familiar places|safe zone alerts
geofence-alerts-app-for-parents|Geofence Alerts App for Parents|Geofence alerts that fit real family routines|geofence alerts for parents
child-geofencing-app|Child Geofencing App|Child geofencing for useful arrival and leaving alerts|child geofencing
family-geofencing-app|Family Geofencing App|Family geofencing without the technical clutter|family geofencing
gps-geofence-app-for-kids|GPS Geofence App for Kids|GPS geofences for the places children visit every day|GPS geofence for kids
location-alerts-for-kids|Location Alerts for Kids|Location alerts for the moments families actually care about|location alerts for kids
place-alerts-app-for-families|Place Alerts App for Families|Place alerts for ordinary family journeys|family place alerts
family-place-alerts-app|Family Place Alerts App|Simple place alerts inside one private family|family place alerts app
safe-places-app-for-kids|Safe Places App for Kids|Create familiar places and receive useful family alerts|safe places for kids
home-and-school-alerts-app|Home and School Alerts App|Home and School alerts without checking the map all day|home and school alerts
school-safe-zone-alerts|School Safe Zone Alerts|School safe-zone alerts for calmer mornings and afternoons|school safe zone alerts
school-arrival-notification-app|School Arrival Notification App|Know when the school journey is complete|school arrival notification
child-arrived-at-school-app|Child Arrived at School App|A simple alert when the child phone reaches School|child arrived at school
notify-me-when-my-child-gets-to-school|Notify Me When My Child Gets to School|Get a useful notification when your child gets to School|notify child gets to school
get-notified-when-child-arrives-at-school|Get Notified When a Child Arrives at School|School arrival alerts for everyday family routines|get notified child arrives school
get-notified-when-child-leaves-school|Get Notified When a Child Leaves School|Know when the journey home begins|get notified child leaves school
app-to-know-when-child-leaves-school|App to Know When a Child Leaves School|A clear update when the child phone leaves School|app child leaves school
app-that-tells-me-when-my-child-gets-to-school|App That Tells Me When My Child Gets to School|One calm notification when School is reached|app tells child gets to school
family-safety-app-for-school-runs|Family Safety App for School Runs|A family safety app built around the school run|family safety school run
school-run-safety-app|School Run Safety App|A calmer way to follow the school run|school run safety app
child-location-alerts-for-school|Child Location Alerts for School|Child location alerts around the School routine|child school location alerts
app-to-know-when-child-gets-home|App to Know When a Child Gets Home|Know when the connected child phone gets Home|app child gets home
get-notified-when-child-gets-home|Get Notified When a Child Gets Home|A Home arrival alert without another check-in message|get notified child gets home
home-arrival-notification-app-for-kids|Home Arrival Notification App for Kids|Home arrival notifications for ordinary family routines|home arrival app kids
child-left-home-notification-app|Child Left Home Notification App|Know when the morning journey has started|child left home notification
app-that-tells-me-when-my-child-leaves-home|App That Tells Me When My Child Leaves Home|A useful alert when the child phone leaves Home|app tells child leaves home
child-location-alerts-for-home|Child Location Alerts for Home|Home location alerts for departures and arrivals|child home location alerts
check-child-got-home-safely|Check a Child Got Home Safely|A calmer way to check that they made it Home|check child home safely
family-map-app|Family Map App|One private family map for the people who matter|family map app
family-location-map-app|Family Location Map App|A family location map with useful device context|family location map
real-time-family-location-app|Real-Time Family Location App|Understand what real-time family location actually means|real time family location
real-time-child-location-app|Real-Time Child Location App|A child location app with clear update context|real time child location
private-family-map-app|Private Family Map App|A private family map with controlled access|private family map
track-child-location-from-parent-phone|Track Child Location From a Parent Phone|Check a connected child phone from the parent device|track child from parent phone
see-my-childs-location-app|See My Child’s Location App|See a child’s latest shared location when it matters|see my child's location
app-to-see-where-my-child-is|App to See Where My Child Is|A private app for checking a child phone’s latest location|app see where child is
emergency-sos-app-for-children|Emergency SOS App for Children|An SOS tool for reaching trusted adults|emergency SOS children
child-sos-alert-app|Child SOS Alert App|A child SOS alert app with clear family context|child SOS alert
family-emergency-alert-app|Family Emergency Alert App|A family alert tool for urgent situations|family emergency alert
sos-button-app-for-kids|SOS Button App for Kids|A simple SOS button for a connected child device|SOS button kids
child-safety-app-with-sos|Child Safety App With SOS|Child safety tools with an SOS option|child safety SOS
life360-alternative|Life360 Alternative|A focused Life360 alternative for families who want less noise|Life360 alternative
life360-alternative-for-families|Life360 Alternative for Families|A family-focused Life360 alternative without social features|Life360 alternative families
find-my-kids-app-alternative|Find My Kids App Alternative|A Find My Kids alternative focused on useful family updates|Find My Kids alternative
best-child-tracker-app|Best Child Tracker App|What to look for in the best child tracker app|best child tracker app
best-family-locator-app|Best Family Locator App|What makes a family locator app genuinely useful|best family locator app
best-gps-tracker-app-for-kids|Best GPS Tracker App for Kids|How to choose a GPS tracker app for kids|best GPS app kids
best-location-sharing-app-for-families|Best Location Sharing App for Families|How to choose a family location sharing app|best family location sharing
free-child-tracker-app|Free Child Tracker App|A free child tracker app for one child profile|free child tracker app
free-family-locator-app|Free Family Locator App|A free family locator app with focused safety tools|free family locator app
guardian-premium|Guardian Premium|Guardian Premium for larger families|Guardian Premium
guardian-for-iphone|Guardian for iPhone|Guardian family location and safety tools on iPhone|Guardian iPhone
guardian-for-android|Guardian for Android|Guardian family location and safety tools on Android|Guardian Android
child-location-sharing-android-iphone|Child Location Sharing on Android and iPhone|Child location sharing across Android and iPhone|Android iPhone child sharing
how-guardian-works|How Guardian Works|Set Guardian up once, then let it support the routine|how Guardian works
set-up-child-device|Set Up a Child Device|Connect the correct child phone in a few clear steps|set up child device
battery-and-last-update-status|Battery and Last Update Status|Understand what the connected phone is reporting|battery last update
location-history-for-families|Location History for Families|Recent location history that adds useful context|family location history
what-is-a-family-safety-app|What Is a Family Safety App?|A practical guide to family safety apps|what is family safety app
what-is-geofencing|What Is Geofencing?|Geofencing explained without the jargon|what is geofencing
how-safe-zone-alerts-work|How Safe Zone Alerts Work|How Guardian confirms safe-zone arrivals and departures|how safe zone alerts work
location-sharing-and-family-privacy|Location Sharing and Family Privacy|How to use family location sharing responsibly|location sharing privacy
talk-to-children-about-location-sharing|Talk to Children About Location Sharing|How to discuss location sharing with children|talk children location sharing
setting-up-home-and-school-safe-zones|Set Up Home and School Safe Zones|Create useful safe zones around familiar places|set up home school zones
what-to-look-for-in-family-location-app|What to Look for in a Family Location App|Choose clarity and privacy over feature overload|choose family location app
how-sos-alerts-work|How SOS Alerts Work|How family SOS alerts should fit into a response plan|how SOS alerts work
what-to-do-when-location-does-not-update|What to Do When Location Does Not Update|Practical checks when a child phone stops updating|location not updating
safe-zone-alerts-vs-constant-location-checking|Safe Zone Alerts vs Constant Location Checking|Why milestone alerts can be healthier than watching a map|alerts vs constant checking"""
rows=[tuple(x.split("|",3)) for x in RAW.splitlines() if x.strip()]
if len(rows) != 94: raise SystemExit(f"Expected 94 pages, found {len(rows)}")
def e(s): return html.escape(s,quote=True)
def copy_for(i,k):
 o=[f"Most families searching for {k} are not trying to watch a phone all day.",f"The useful question behind {k} is usually simpler than constant tracking.",f"Parents considering {k} often want reassurance around ordinary journeys, not another dashboard.",f"Good {k} should answer a real family question without taking over the routine."]
 c=["Guardian combines Home and School alerts, a private Family Map, recent location history, battery status and SOS tools inside one parent-managed family.","Guardian keeps the latest available location, safe-zone alerts, device status and trusted-family access together without public profiles or a social feed.","Guardian focuses on familiar places and useful updates, with optional adult location sharing and clear access controls.","Guardian supports agreed family routines with place alerts, map context, recent updates and an SOS option on the connected child device."]
 x=["The aim is quick reassurance rather than minute-by-minute monitoring.","Parents can open the map only when extra context is genuinely useful.","Battery level and last-update time help explain what the phone is reporting.","Home and School zones provide useful milestones during ordinary journeys."]
 p1=o[i%4]+" "+c[i%4]+" "+x[i%4]
 y=[f"For families comparing {k}, privacy and sensible boundaries matter as much as features.",f"Guardian approaches {k} as a practical family tool rather than hidden surveillance.",f"With {k}, the healthiest setup is one the family has discussed and agreed.",f"The best use of {k} is clear, limited and honest about the technology."]
 z=["Phone location can still be affected by GPS, signal, permissions, battery settings and operating-system restrictions.","The map shows the latest available information, but no app can promise perfect accuracy or guaranteed delivery.","Children should understand what is shared, who can see it and why the family uses the app.","Used openly and proportionately, Guardian can reduce repeated check-in messages while leaving room for trust and independence."]
 return p1,y[i%4]+" "+z[(i+1)%4]+" Guardian is not an emergency service; in immediate danger, contact the emergency services directly."
def faqs(i,k):
 sets=[[
 ("Is Guardian available on iPhone and Android?","Guardian is being prepared for both platforms. Store buttons activate when official links are added."),
 (f"Can {k} ever be inaccurate?","Yes. GPS, signal, buildings, permissions and battery settings can affect location and timing."),
 ("Is Guardian an emergency service?","No. In immediate danger, contact the emergency services directly.")],[
 (f"Who can see information used for {k}?","Only trusted adults with access to the private Guardian family."),
 ("Does Guardian show battery and last-update time?","Yes. Those details help explain whether the child phone is reporting normally."),
 ("Is parent location sharing required?","No. Adult location sharing is optional.")],[
 (f"Does {k} mean watching the map all day?","No. Guardian focuses on useful alerts and quick checks when context is needed."),
 ("Can phone settings delay updates?","Yes. Battery optimisation, permissions and background restrictions can affect reporting."),
 ("Does Guardian have public profiles?","No. Family information stays inside a private, parent-managed account.")]]
 return sets[i%3]
S=[]
for i,(slug,name,h1,k) in enumerate(rows):
 p1,p2=copy_for(i,k); d=f"Explore {name.lower()} with Guardian: private family access, useful alerts, device context and honest location limits."
 S.append(dict(slug=slug,name=name,h1=h1,k=k,p1=p1,p2=p2,d=d,faq=faqs(i,k),cluster=i//10))
for i,s in enumerate(S):
 pool=[x for x in S if x["cluster"]==s["cluster"] and x["slug"]!=s["slug"]]
 if len(pool)<3: pool=[x for x in S if x["slug"]!=s["slug"]]
 s["rel"]=[pool[(i+j)%len(pool)] for j in range(3)]
def page(s):
 url=f'{SITE}/guardian/{s["slug"]}/'; title=f'{s["name"]} | Guardian by Vanta Labs'
 fq="".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in s["faq"])
 rl="".join(f'<a class="card" href="/guardian/{r["slug"]}/"><strong>{e(r["name"])}</strong></a>' for r in s["rel"])
 sc=json.dumps([{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Guardian: Family Tracker","applicationCategory":"LifestyleApplication","operatingSystem":"Android, iOS","description":s["d"],"url":url,"image":SITE+"/guardian.png","author":{"@type":"Organization","name":"Vanta Labs","url":SITE}},{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in s["faq"]]}],ensure_ascii=False)
 return f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(s["d"])}"><link rel="canonical" href="{e(url)}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="website"><meta property="og:site_name" content="Vanta Labs"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(s["d"])}"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{SITE}/guardian.png"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="/guardian.png"><link rel="stylesheet" href="/guardian/assets/guardian.css"><script defer src="/guardian/assets/app-links.js"></script><script type="application/ld+json">{sc}</script></head><body class="guardian-detail guardian-seo-page"><header class="head"><nav><a class="brand" href="/">Vanta Labs</a><div class="links"><a href="/guardian/">Guardian</a><a href="/guardian/features/">Features</a><a href="/guardian/guides/what-is-a-family-safety-app/">Guides</a><a href="/">All apps</a></div></nav></header><main><section class="hero"><div><div class="eyebrow">{e(s["k"])}</div><h1>{e(s["h1"])}</h1><p class="lead">{e(s["d"])}</p><div class="ctas"><a class="btn disabled" data-store="ios" aria-disabled="true">App Store — coming soon</a><a class="btn alt disabled" data-store="android" aria-disabled="true">Google Play — coming soon</a></div></div><div class="iconbox"><img src="/guardian.png" alt="Guardian family tracker app icon" width="512" height="512"></div></section><article class="body"><section class="long-copy"><h2>{e(s["name"])}, without the unnecessary noise</h2><div class="long-copy-text"><p>{e(s["p1"])}</p><p>{e(s["p2"])}</p></div></section><div class="notice"><strong>Guardian is not an emergency service.</strong> Location and notifications can be affected by GPS, connectivity, permissions, battery settings and operating-system restrictions.</div></article><div class="guardian-lower-grid"><section class="related"><h2>Keep exploring Guardian</h2><div class="grid">{rl}</div></section><section class="faq"><h2>Quick questions</h2>{fq}</section></div></main><footer><div><span>© 2026 Vanta Labs NW LTD</span><span><a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a> · <a href="/">All Vanta Labs apps</a></span></div></footer></body></html>"""
for s in S:
 d=G/s["slug"]; d.mkdir(parents=True,exist_ok=True); (d/"index.html").write_text(page(s))
css=CSS.read_text(); mark="/* Guardian 90-page SEO system */"
if mark in css: css=css[:css.index(mark)]
css+=r"""
/* Guardian 90-page SEO system */
.guardian-seo-page .hero,.guardian-seo-page .body,.guardian-seo-page .guardian-lower-grid,.guardian-seo-page footer>div{width:min(var(--max),calc(100% - 44px));margin-left:auto;margin-right:auto}
.guardian-seo-page .hero{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:72px;align-items:center;padding:88px 0;text-align:left}.guardian-seo-page .hero>div:first-child{max-width:820px}.guardian-seo-page .hero h1{max-width:800px}.guardian-seo-page .hero .lead{max-width:760px}
.guardian-seo-page .iconbox{width:176px;height:176px;padding:24px;border:1px solid rgba(246,239,226,.10);border-radius:28px;background:rgba(255,255,255,.012);display:flex;align-items:center;justify-content:center}.guardian-seo-page .iconbox img{width:112px;height:112px;border-radius:23px;display:block}
.guardian-seo-page .body{padding:70px 0 56px;text-align:left}.guardian-seo-page .long-copy{max-width:760px}.guardian-seo-page .long-copy h2{margin:0 0 24px;max-width:680px;font-size:clamp(30px,3.6vw,42px);line-height:1.08;letter-spacing:-.045em}.guardian-seo-page .long-copy-text{max-width:710px}.guardian-seo-page .long-copy-text p{margin:0;color:rgba(246,239,226,.74);font-size:17px;line-height:1.82}.guardian-seo-page .long-copy-text p+p{margin-top:22px}
.guardian-seo-page .notice{max-width:710px;margin-top:38px;padding-top:17px;border-top:1px solid rgba(246,239,226,.075);color:rgba(246,239,226,.43);font-size:12px;line-height:1.7}
.guardian-seo-page .guardian-lower-grid{padding:66px 0 74px;display:grid;grid-template-columns:minmax(0,1.2fr) minmax(300px,.8fr);gap:72px;align-items:start;border-top:1px solid rgba(246,239,226,.075);text-align:left}.guardian-seo-page .guardian-lower-grid .related,.guardian-seo-page .guardian-lower-grid .faq{width:auto;margin:0;padding:0}.guardian-seo-page .guardian-lower-grid h2{margin:0 0 18px;color:rgba(246,239,226,.56);font-size:18px;line-height:1.2;letter-spacing:-.02em}
.guardian-seo-page .related .grid{display:grid;grid-template-columns:1fr}.guardian-seo-page .related .card{position:relative;padding:18px 34px 20px 0;border-top:1px solid rgba(246,239,226,.07)}.guardian-seo-page .related .card:after{content:"→";position:absolute;right:2px;top:20px;color:rgba(246,239,226,.24)}.guardian-seo-page .related .card strong{color:rgba(246,239,226,.66);font-size:15px;line-height:1.3}
.guardian-seo-page .faq{padding:18px 20px!important;border:1px solid rgba(246,239,226,.075)!important;border-radius:16px;background:rgba(255,255,255,.008)}.guardian-seo-page .faq details{padding:14px 0;border-top:1px solid rgba(246,239,226,.065)}.guardian-seo-page .faq summary{color:rgba(246,239,226,.62);font-size:13px;line-height:1.45;font-weight:650}.guardian-seo-page .faq details p{color:rgba(246,239,226,.46);font-size:13px;line-height:1.65}
@media(max-width:760px){.guardian-seo-page .hero,.guardian-seo-page .body,.guardian-seo-page .guardian-lower-grid,.guardian-seo-page footer>div,.guardian-seo-page .head nav{width:min(100% - 28px,var(--max))}.guardian-seo-page .head .links{gap:16px;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}.guardian-seo-page .hero{grid-template-columns:1fr;gap:32px;padding:58px 0 60px}.guardian-seo-page .iconbox{order:-1;width:108px;height:108px;padding:14px;border-radius:22px}.guardian-seo-page .iconbox img{width:78px;height:78px;border-radius:17px}.guardian-seo-page .hero h1{font-size:clamp(44px,14vw,66px)}.guardian-seo-page .ctas{display:flex;flex-direction:column;align-items:stretch}.guardian-seo-page .ctas .btn{width:100%;text-align:center}.guardian-seo-page .body{padding:54px 0 48px}.guardian-seo-page .long-copy h2{font-size:32px}.guardian-seo-page .long-copy-text p{font-size:16px;line-height:1.78}.guardian-seo-page .guardian-lower-grid{grid-template-columns:1fr;gap:46px;padding:54px 0 62px}.guardian-seo-page footer>div{display:flex;flex-direction:column;align-items:flex-start;gap:12px}}
"""
CSS.write_text(css)
sm=SM.read_text()
for s in S:
 url=f'{SITE}/guardian/{s["slug"]}/'; sm=re.sub(r'\s*<url>\s*<loc>'+re.escape(url)+r'</loc>.*?</url>','',sm,flags=re.S)
entries="\n".join(f'  <url><loc>{SITE}/guardian/{s["slug"]}/</loc><changefreq>monthly</changefreq><priority>0.75</priority></url>' for s in S)
SM.write_text(sm.replace("</urlset>",entries+"\n</urlset>"))
issues=[]; titles={}; descs={}; bodies=[]
for s in S:
 t=(G/s["slug"]/"index.html").read_text(); ti=re.search(r"<title>(.*?)</title>",t,re.S); de=re.search(r'<meta name="description" content="(.*?)">',t,re.S)
 if not ti or not de or len(re.findall(r"<h1>.*?</h1>",t,re.S))!=1: issues.append("Structure: "+s["slug"])
 if ti: titles.setdefault(ti.group(1),[]).append(s["slug"])
 if de: descs.setdefault(de.group(1),[]).append(s["slug"])
 bodies.append((s["slug"],s["p1"]+" "+s["p2"]))
for d in (titles,descs):
 for _,sl in d.items():
  if len(sl)>1: issues.append("Duplicate metadata: "+", ".join(sl))
for i in range(len(bodies)):
 for j in range(i+1,len(bodies)):
  r=difflib.SequenceMatcher(None,bodies[i][1],bodies[j][1]).ratio()
  if r>.92: issues.append(f"Similar copy: {bodies[i][0]} / {bodies[j][0]} ({r:.2f})")
(ROOT/"guardian-seo-audit.json").write_text(json.dumps({"pages":len(S),"issues":issues,"store_links":"placeholders","committed":False,"pushed":False,"deployed":False},indent=2))
print(f"Generated/refreshed {len(S)} Guardian SEO pages.")
print(f"Added {len(S)} Guardian URLs to sitemap.xml.")
print("Applied compact Vanta-style responsive behaviour.")
print("Audit:","PASS" if not issues else f"{len(issues)} issue(s) — see guardian-seo-audit.json")
print("Nothing was committed, pushed or deployed.")
