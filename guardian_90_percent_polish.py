#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path.cwd()
GUARDIAN = ROOT / "guardian"
CSS = GUARDIAN / "assets" / "guardian.css"
HOME = GUARDIAN / "index.html"

if not (ROOT / "index.html").exists():
    raise SystemExit("Run this from ~/Projects/vantalabs-site")
if not GUARDIAN.exists():
    raise SystemExit("Guardian folder is missing.")

backup = ROOT / "guardian.before-90-percent-polish"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

css = CSS.read_text()
css += r'''

/* 90% polish pass */
.hero{
  padding:76px 0 84px !important;
}
.hero-visual{
  align-self:center !important;
}
.hero h1{
  max-width:670px !important;
}
.hero .lead{
  max-width:660px !important;
  font-size:18px !important;
}
.hero .ctas{
  margin-top:24px !important;
}
.hero .btn.disabled{
  opacity:.68 !important;
}
.hero-note{
  margin-top:13px !important;
}
.hero-note a{
  color:var(--gold);
}

.timeline{
  margin-top:6px;
}
.moment-num{
  color:var(--gold) !important;
}
.moment h3{
  margin-top:12px !important;
}
.moment p{
  color:rgba(246,239,226,.74) !important;
}

#features .section-head{
  margin-bottom:34px !important;
}
#features .section-head h2{
  font-size:clamp(36px,4.4vw,54px) !important;
}
.feature h3{
  font-size:25px !important;
}

.privacy-copy-left p{
  max-width:520px;
}
.privacy-points .btn{
  padding:9px 13px !important;
  font-size:12px !important;
}

.faq-mini{
  width:min(var(--max),calc(100% - 44px));
  margin:0 auto;
  padding:78px 0 82px;
  border-bottom:1px solid var(--line);
}
.faq-mini-head{
  max-width:680px;
  margin-bottom:28px;
}
.faq-mini h2{
  margin-top:12px;
  font-size:clamp(36px,4.5vw,54px);
  line-height:1;
  letter-spacing:-.055em;
}
.faq-mini p{
  margin-top:18px;
  color:var(--muted);
  font-size:17px;
  line-height:1.75;
}
.faq-mini details{
  padding:20px 0;
  border-top:1px solid var(--line);
}
.faq-mini summary{
  cursor:pointer;
  font-weight:800;
  font-size:18px;
  letter-spacing:-.02em;
}
.faq-mini details p{
  max-width:760px;
  margin-top:12px;
  font-size:15px;
}

.related{
  padding-top:68px !important;
}
.explore-link strong{
  color:var(--text) !important;
}
.explore-link p{
  color:rgba(246,239,226,.68) !important;
}
.explore-link:hover .explore-arrow{
  color:var(--gold);
}
.all-guides{
  display:inline-flex;
  align-items:center;
  gap:8px;
  margin-top:26px;
  color:var(--gold);
  font-size:13px;
  font-weight:850;
}
.all-guides:hover{
  opacity:.78;
}

@media(max-width:560px){
  .hero{
    padding:58px 0 64px !important;
  }
  .faq-mini{
    width:min(100% - 28px,var(--max));
    padding:60px 0 64px;
  }
}
'''

home = HOME.read_text()

home = home.replace(
    'Home and School alerts, a private family map, location history, battery status and SOS tools—kept simple.',
    'Get an alert when they leave Home, arrive at School or make it back safely — with private location sharing and SOS when it matters.'
)

home = home.replace(
    '<p class="hero-note">Built by Vanta Labs.</p>',
    '<p class="hero-note">Built by <a href="/">Vanta Labs</a>.</p>'
)

home = home.replace(
    '<p>The reassuring arrival notification.</p>',
    '<p>Know the school journey is complete.</p>'
)

home = home.replace(
    '<h3>History, battery and updates</h3>',
    '<h3>Location history and device status</h3>'
)

home = home.replace(
    'Guardian uses a private, parent-managed family account. There are no public profiles, adverts or social feeds.',
    'Guardian keeps location sharing inside a private, parent-managed family. There are no public profiles, adverts or social feeds.'
)

faq_block = '''<section class="faq-mini">
<div class="faq-mini-head">
<span class="kicker">Common questions</span>
<h2>What parents usually want to know.</h2>
<p>Clear answers about location sharing, School alerts and family privacy.</p>
</div>

<details>
<summary>How does Guardian track a child’s location?</summary>
<p>A parent creates the child profile and links the child’s phone to the private family. Guardian then shows the latest available location provided by that connected device, subject to location permissions, signal, battery settings and operating-system restrictions.</p>
</details>

<details>
<summary>Can Guardian alert me when my child arrives at School?</summary>
<p>Yes. A parent can create a School safe zone and receive an arrival notification when Guardian confirms that the connected child device has entered the area.</p>
</details>

<details>
<summary>Does Guardian share family location publicly?</summary>
<p>No. Guardian does not use public profiles, follower systems or public location sharing. Family information stays inside the connected, parent-managed family account.</p>
</details>
</section>

'''

insert_point = home.find('<section class="related">')
if insert_point == -1:
    raise SystemExit("Could not find Explore Guardian section.")
home = home[:insert_point] + faq_block + home[insert_point:]

needle = '''</div>
</section>
</main>'''
replacement = '''</div>
<a class="all-guides" href="/guardian/guides/what-is-a-family-safety-app/">View all Guardian guides <span>→</span></a>
</section>
</main>'''
if needle not in home:
    raise SystemExit("Could not find Explore Guardian closing block.")
home = home.replace(needle, replacement, 1)

CSS.write_text(css)
HOME.write_text(home)

print("Guardian 90% polish applied.")
print("Hero, timeline, features, privacy, FAQ and Explore Guardian refined.")
print("No screenshots added.")
print("Nothing was committed, pushed or deployed.")
print("Refresh http://localhost:8000/guardian/")
