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
if not (ROOT / "guardian.png").exists():
    raise SystemExit("guardian.png is missing.")

backup = ROOT / "guardian.before-refined-layout"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

css = CSS.read_text()

css += r'''

/* Refined Guardian layout: split hero + stronger editorial links */
.hero{
  width:min(var(--max),calc(100% - 44px)) !important;
  display:grid !important;
  grid-template-columns:230px 1fr !important;
  gap:64px !important;
  align-items:center !important;
  text-align:left !important;
  padding:96px 0 104px !important;
}
.hero-visual{
  display:flex;
  align-items:center;
  justify-content:flex-start;
}
.hero-icon{
  width:154px !important;
  height:154px !important;
  border-radius:30px !important;
  margin:0 !important;
}
.hero-content{
  max-width:760px;
}
.hero .eyebrow{
  margin-bottom:16px !important;
}
.hero h1{
  max-width:760px !important;
  margin:0 !important;
  font-size:clamp(48px,5.6vw,72px) !important;
}
.hero .lead{
  max-width:700px !important;
  margin:26px 0 0 !important;
}
.hero .ctas{
  justify-content:flex-start !important;
}
.hero-note{
  text-align:left;
}

.related{
  padding:82px 0 90px !important;
}
.related-head{
  display:grid;
  grid-template-columns:.9fr 1.1fr;
  gap:54px;
  align-items:end;
  margin-bottom:36px;
}
.related h2{
  margin:0 !important;
  font-size:46px !important;
}
.related-intro{
  color:var(--muted);
  font-size:17px;
  line-height:1.75;
  max-width:580px;
}
.explore-grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:0 44px;
  border-top:1px solid var(--line);
}
.explore-link{
  display:block;
  padding:26px 0 28px;
  border-bottom:1px solid var(--line);
  transition:opacity .18s ease;
}
.explore-link:hover{opacity:.76}
.explore-top{
  display:flex;
  justify-content:space-between;
  align-items:center;
  gap:18px;
}
.explore-link small{
  color:var(--gold);
  font-size:10px;
  font-weight:900;
  letter-spacing:.17em;
  text-transform:uppercase;
}
.explore-arrow{
  color:var(--soft);
  font-size:19px;
}
.explore-link strong{
  display:block;
  margin-top:10px;
  font-size:25px;
  line-height:1.08;
  letter-spacing:-.04em;
}
.explore-link p{
  margin-top:10px;
  color:var(--muted);
  font-size:14px;
  line-height:1.7;
  max-width:460px;
}

@media(max-width:760px){
  .hero{
    grid-template-columns:1fr !important;
    gap:32px !important;
    text-align:center !important;
  }
  .hero-visual{
    justify-content:center;
  }
  .hero-icon{
    width:108px !important;
    height:108px !important;
    border-radius:22px !important;
  }
  .hero-content{
    max-width:none;
  }
  .hero h1,
  .hero .lead{
    margin-left:auto !important;
    margin-right:auto !important;
  }
  .hero .ctas{
    justify-content:center !important;
  }
  .hero-note{
    text-align:center;
  }
  .related-head{
    grid-template-columns:1fr;
    gap:18px;
  }
  .explore-grid{
    grid-template-columns:1fr;
  }
}
'''

home = HOME.read_text()

old_hero = '''<section class="hero">
<img class="hero-icon" src="/guardian.png" alt="Guardian family tracker app icon">
<span class="eyebrow">Guardian · Family Tracker</span>
<h1>Know they got there.<br>Without checking every five minutes.</h1>
<p class="lead">Home and School alerts, a private family map, location history, battery status and SOS tools—kept simple.</p>
<div class="ctas">
<a class="btn disabled" data-store="ios" aria-disabled="true">App Store — coming soon</a>
<a class="btn disabled" data-store="android" aria-disabled="true">Google Play — coming soon</a>
</div>
<p class="hero-note">Built by Vanta Labs in Manchester, UK.</p>
</section>'''

new_hero = '''<section class="hero">
<div class="hero-visual">
<img class="hero-icon" src="/guardian.png" alt="Guardian family tracker app icon">
</div>
<div class="hero-content">
<span class="eyebrow">Guardian · Family Tracker</span>
<h1>Know they got there.<br>Without checking every five minutes.</h1>
<p class="lead">Home and School alerts, a private family map, location history, battery status and SOS tools—kept simple.</p>
<div class="ctas">
<a class="btn disabled" data-store="ios" aria-disabled="true">App Store — coming soon</a>
<a class="btn disabled" data-store="android" aria-disabled="true">Google Play — coming soon</a>
</div>
<p class="hero-note">Built by Vanta Labs in Manchester, UK.</p>
</div>
</section>'''

if old_hero not in home:
    raise SystemExit("Could not find current hero block.")
home = home.replace(old_hero, new_hero, 1)

start = home.find('<section class="related">')
end = home.find('</section>', start)
if start == -1 or end == -1:
    raise SystemExit("Could not find Explore Guardian section.")
end += len('</section>')

new_related = '''<section class="related">
<div class="related-head">
<h2>Explore Guardian</h2>
<p class="related-intro">Useful guides and feature pages for parents who want to understand how Guardian works before downloading it.</p>
</div>

<div class="explore-grid">
<a class="explore-link" href="/guardian/safe-zone-alerts/">
<div class="explore-top"><small>Safe zones</small><span class="explore-arrow">→</span></div>
<strong>Home and School alerts</strong>
<p>See how Guardian recognises useful arrivals and departures around everyday family routines.</p>
</a>

<a class="explore-link" href="/guardian/child-location-tracker/">
<div class="explore-top"><small>Location</small><span class="explore-arrow">→</span></div>
<strong>Child location sharing</strong>
<p>Understand how connected child devices share their latest available location with the private family.</p>
</a>

<a class="explore-link" href="/guardian/sos-alert-app-for-families/">
<div class="explore-top"><small>Urgent alerts</small><span class="explore-arrow">→</span></div>
<strong>Family SOS tools</strong>
<p>Learn what happens when a connected child device sends an urgent alert to trusted adults.</p>
</a>

<a class="explore-link" href="/guardian/guides/location-sharing-and-family-privacy/">
<div class="explore-top"><small>Parent guide</small><span class="explore-arrow">→</span></div>
<strong>Location sharing and privacy</strong>
<p>A practical guide to transparent, proportionate family location sharing and trusted access.</p>
</a>
</div>
</section>'''

home = home[:start] + new_related + home[end:]

CSS.write_text(css)
HOME.write_text(home)

print("Refined Guardian layout applied.")
print("Hero now uses split icon-and-copy layout.")
print("Explore Guardian rebuilt as a stronger editorial section.")
print("Nothing was committed, pushed or deployed.")
print("Refresh http://localhost:8000/guardian/")
