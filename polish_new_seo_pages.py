from pathlib import Path
from bs4 import BeautifulSoup
from copy import deepcopy
import json

R=Path("/Users/aaron/Projects/vantalabs-site")

GUARDIAN={
"school-departure-notification-app":("Know when the journey home has started","Get a useful School departure update when the connected child phone leaves its familiar School safe zone.","How does Guardian help with School departure alerts?"),
"child-home-arrival-alert-app":("A simple update when they get home","Receive a Home arrival update when the connected child phone reaches its configured Home safe zone.","How can Guardian tell me when my child gets home?"),
"after-school-location-app":("Useful context for the journey after School","Use School departure and Home arrival alerts for the parts of the after-school journey families usually care about most.","How can Guardian help with the journey after School?"),
"walking-to-school-safety-app":("Support independence without watching every step","Use Home and School alerts to support independent school journeys without keeping the Family Map open all morning.","Can Guardian help when my child walks to School?"),
"child-journey-alerts-app":("Focus on the moments that actually matter","Use familiar-place alerts for the beginning and end of everyday journeys instead of watching every movement.","What kinds of child journey alerts can Guardian provide?"),
"child-device-battery-status-app":("Battery level helps explain what the phone is reporting","See battery level and last-update time alongside the connected child phone's latest available location.","Why is child-device battery status useful in Guardian?"),
"child-phone-last-location-app":("See the latest available update — and how recent it is","Check the latest location successfully shared by the connected child phone together with its last-update time.","What does Guardian mean by the latest available location?"),
"child-location-not-updating-app":("When a location stops updating, check the phone first","Check battery, signal, permissions and background settings when a connected child phone stops reporting location.","What should I check when my child's location stops updating?"),
"family-location-app-with-safe-zones":("Use familiar places instead of watching the map all day","Combine a private Family Map with Home, School and other familiar-place alerts.","How do safe zones make family location sharing more useful?"),
"family-location-app-with-sos":("Everyday location tools, plus a way to ask for help","Combine private family location, safe-zone alerts and an SOS option on the connected child device.","How does SOS fit alongside Guardian's location features?"),
"parent-location-sharing-app":("Parents choose whether to share their own location","Adult location sharing stays optional, so parents decide when sharing their own position is useful.","Do parents have to share their own location in Guardian?"),
"co-parent-location-sharing-app":("Keep trusted parents looking at the same family picture","Give another trusted parent access to useful child-location and safe-zone updates inside the private Guardian family.","Can two trusted parents use the same Guardian family?"),
"family-location-app-without-social-feed":("Family location without feeds, followers or public profiles","Keep family location, safe-zone alerts and device information private without adding social-network features.","Does Guardian have a public feed or social profiles?"),
"private-family-location-app-iphone-android":("One private family view across iPhone and Android","Use Guardian across supported iPhone and Android devices while keeping family location information inside the private family.","Can Guardian work across iPhone and Android devices?")
}

WORKFORCE={
"staff-scheduling-app":("Build the rota, assign the work and keep changes clear","Plan staff shifts, assign workers to workplaces and keep the rota clear when the week changes."),
"employee-scheduling-app":("A clearer view of who is working when","Give managers one place to plan employee shifts, review cover and keep scheduled work organised."),
"shift-scheduling-app":("Turn planned shifts into a rota people can actually use","Build workplace shift schedules, assign staff and keep planned work easy to review before the day starts."),
"staff-rota-app":("Keep the working week visible without another spreadsheet","Create a staff rota showing who is working, when they are due in and which workplace they are covering."),
"employee-rota-app":("Make each employee's planned shifts easier to review","Keep employee shifts visible in a rota managers can update when staffing needs change."),
"rota-management-app":("Keep the rota organised when plans change","Manage workplace rotas without losing track of assignments, changes or the people affected."),
"employee-work-schedule-app":("Put scheduled work in one clear place","Give employees and managers a clearer view of planned working times and workplace assignments."),
"staff-shift-planner":("Plan staff shifts around the cover you actually need","Plan shifts around the people and workplaces that need covering, then review the schedule before publishing."),
"multi-site-staff-scheduling":("Schedule people across more than one workplace","Coordinate staff schedules across multiple workplaces while keeping each site's planned cover clear."),
"workplace-shift-scheduling":("Build shifts around the workplace that needs covering","Create a clear shift schedule for each workplace and keep staff assignments tied to the right site."),
"guides/how-to-create-a-staff-rota":("Start with the cover you need, then build the rota","A practical way to create a staff rota: define required cover, add available workers and check the gaps before publishing."),
"guides/how-employee-shift-scheduling-works":("From required cover to a rota people can review","See how employee shift scheduling moves from planned cover to assigned workers and a published rota."),
"guides/staff-scheduling-vs-spreadsheets":("When a spreadsheet starts making the rota harder","Compare dedicated staff scheduling with spreadsheets as changes, rotas and multi-site cover become harder to manage."),
"guides/how-to-schedule-staff-across-multiple-workplaces":("Keep each workplace clear before assigning people","Plan multi-site staffing by separating required cover, worker availability and each workplace's schedule before assigning shifts.")
}

SHIFT={
"shift-planner-app":("Keep your shifts clear without turning it into a work system","Plan your own shifts in a clear calendar, including repeating patterns, notes, working hours and estimated pay."),
"personal-shift-planner-app":("Your own rota, hours and pay in one place","Keep your personal rota, upcoming shifts, working hours and estimated earnings together without workplace admin."),
"rota-planner-app":("Build a rota that makes sense at a glance","Build and view your own rota in a simple calendar designed for repeating shift patterns."),
"personal-rota-planner":("Plan the pattern you actually work","Plan your own rota, adjust individual shifts and see what is coming next."),
"custom-shift-calendar":("Shape the calendar around your own pattern","Create a shift calendar around your own day, night and off pattern instead of forcing it into a fixed template."),
"custom-shift-pattern-app":("Build the day, night and off pattern you need","Create the repeating shift sequence that matches the rota you actually work."),
"days-off-calendar":("See working days and days off without counting ahead","View working days and days off together so you can plan ahead without manually counting through the rota."),
"firefighter-shift-calendar":("Make long rotations easier to see","Lay out long duties, nights and rest days in a personal calendar that makes repeating firefighter patterns easier to follow."),
"police-shift-calendar":("Keep early, late, night and rest days clear","Put your own police shift pattern into a personal calendar without turning it into a workforce scheduling tool."),
"paramedic-shift-calendar":("Plan long duties, nights and recovery days","Keep long duties, overnight shifts and recovery days clear in a personal calendar built around your own rota."),
"guides/how-to-create-a-custom-shift-pattern":("Start with the sequence you actually work","Build a custom shift pattern by laying out the real order of day shifts, nights and days off before repeating it."),
"guides/how-to-plan-your-work-rota":("Turn your real rota into something easier to follow","Plan your work rota around the shifts you actually work, then adjust individual days when the pattern changes."),
"guides/how-to-calculate-hours-from-your-rota":("Use the shifts on your rota to understand your hours","Work from the start and finish times on your rota to keep a clearer running view of scheduled hours."),
"guides/how-to-estimate-pay-from-your-rota":("Turn scheduled hours into a useful pay estimate","Use your rota and hourly rate to estimate earnings while keeping the result clearly separate from payroll.")
}

def text(node):
    return node.get_text(" ",strip=True) if node else ""

def update_schema(soup, description):
    for script in soup.find_all("script",attrs={"type":"application/ld+json"}):
        try:
            data=json.loads(script.string or script.get_text())
        except Exception:
            continue
        def walk(x):
            if isinstance(x,dict):
                if x.get("@type")=="SoftwareApplication":
                    x["description"]=description
                for v in x.values(): walk(v)
            elif isinstance(x,list):
                for v in x: walk(v)
        walk(data)
        script.string=json.dumps(data,ensure_ascii=False,separators=(",",":"))

def rebuild(path, template, lower_class, heading, description, faq_question=None):
    current=BeautifulSoup(path.read_text(),"html.parser")
    base=BeautifulSoup(template.read_text(),"html.parser")

    # Keep target SEO metadata while using the exact approved visual shell.
    if current.title and base.title:
        base.title.string=text(current.title)

    cm=current.find("meta",attrs={"name":"description"})
    bm=base.find("meta",attrs={"name":"description"})
    if bm: bm["content"]=description

    cc=current.find("link",rel="canonical")
    bc=base.find("link",rel="canonical")
    if cc and bc: bc["href"]=cc.get("href","")

    for prop in ("og:title","og:url"):
        c=current.find("meta",attrs={"property":prop})
        b=base.find("meta",attrs={"property":prop})
        if c and b: b["content"]=c.get("content","")

    b=base.find("meta",attrs={"property":"og:description"})
    if b: b["content"]=description

    # Target schema replaces template schema.
    for s in base.find_all("script",attrs={"type":"application/ld+json"}):
        s.decompose()
    for s in current.find_all("script",attrs={"type":"application/ld+json"}):
        base.head.append(deepcopy(s))

    # Keep target keyword/H1 but put it inside the known-good shell.
    for selector in (".hero .eyebrow",".hero h1"):
        c=current.select_one(selector)
        b=base.select_one(selector)
        if c and b: b.string=text(c)

    lead=base.select_one(".hero .lead")
    if lead: lead.string=description

    c_long=current.select_one(".long-copy")
    b_long=base.select_one(".long-copy")
    if c_long and b_long:
        b_long.replace_with(deepcopy(c_long))

    c_notice=current.select_one(".notice")
    b_notice=base.select_one(".notice")
    if c_notice and b_notice:
        b_notice.replace_with(deepcopy(c_notice))

    lower=base.select_one("."+lower_class)
    if not lower:
        raise SystemExit(f"Missing approved lower shell: {template}")

    for cls in ("related","faq"):
        c=current.select_one("."+cls)
        b=lower.select_one("."+cls)
        if c and b:
            b.replace_with(deepcopy(c))

    h2=base.select_one(".long-copy h2")
    if h2: h2.string=heading

    if faq_question:
        q=base.select_one(".faq details summary")
        if q: q.string=faq_question

    update_schema(base,description)
    path.write_text(str(base),encoding="utf-8")

# Guardian: exact shell from an existing polished Guardian page.
g_template=R/"guardian/child-location-app/index.html"
for slug,(h2,desc,q) in GUARDIAN.items():
    rebuild(R/f"guardian/{slug}/index.html",g_template,"parent-quest-lower-grid",h2,desc,q)

# Workforce: exact shell from an established page; guides use an established guide shell.
w_template=R/"workforce/staff-attendance-app/index.html"
w_guide=next(p for p in (R/"workforce/guides").glob("*/index.html") if "how-to-create-a-staff-rota" not in str(p))
for slug,(h2,desc) in WORKFORCE.items():
    template=w_guide if slug.startswith("guides/") else w_template
    rebuild(R/f"workforce/{slug}/index.html",template,"workforce-lower-grid",h2,desc)

# Vanta Shift: same treatment, using genuine existing Vanta Shift shells.
s_template=R/"vanta-shift/shift-calendar-app/index.html"
s_guide=next(p for p in (R/"vanta-shift/guides").glob("*/index.html") if p.relative_to(R/"vanta-shift").as_posix() not in {x+"/index.html" for x in SHIFT})
for slug,(h2,desc) in SHIFT.items():
    template=s_guide if slug.startswith("guides/") else s_template
    rebuild(R/f"vanta-shift/{slug}/index.html",template,"workforce-lower-grid",h2,desc)

print("Polished:",len(GUARDIAN),"Guardian,",len(WORKFORCE),"Workforce,",len(SHIFT),"Vanta Shift pages")


# Metadata safety pass
def ensure_page_metadata(path, base_url):
    import html as _html, re as _re
    from bs4 import BeautifulSoup as _BS
    t=path.read_text()
    s=_BS(t,"html.parser")
    title=s.title.get_text(" ",strip=True) if s.title else ""
    lead=s.select_one(".hero .lead")
    desc=lead.get_text(" ",strip=True) if lead else ""
    canonical=base_url

    t=_re.sub(r'<meta[^>]*name=["\']description["\'][^>]*>',"",t,flags=_re.I|_re.S)
    t=_re.sub(r'<link[^>]*rel=["\']canonical["\'][^>]*>',"",t,flags=_re.I|_re.S)
    for prop in ("og:title","og:description","og:url"):
        t=_re.sub(
            rf'<meta[^>]*property=["\']{_re.escape(prop)}["\'][^>]*>',
            "",t,flags=_re.I|_re.S
        )

    tags=(
        '\n<meta name="description" content="'+_html.escape(desc,quote=True)+'">'
        '\n<link rel="canonical" href="'+canonical+'">'
        '\n<meta property="og:title" content="'+_html.escape(title,quote=True)+'">'
        '\n<meta property="og:description" content="'+_html.escape(desc,quote=True)+'">'
        '\n<meta property="og:url" content="'+canonical+'">\n'
    )
    t=t.replace("</title>","</title>"+tags,1)
    path.write_text(t)

for _slug in WORKFORCE:
    ensure_page_metadata(
        R/"workforce"/_slug/"index.html",
        "https://vantalabs.co.uk/workforce/"+_slug+"/"
    )

for _slug in SHIFT:
    ensure_page_metadata(
        R/"vanta-shift"/_slug/"index.html",
        "https://vantalabs.co.uk/vanta-shift/"+_slug+"/"
    )
