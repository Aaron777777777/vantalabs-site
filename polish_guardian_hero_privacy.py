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

backup = ROOT / "guardian.before-hero-privacy-polish"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

css = CSS.read_text()
css += r'''

/* Final polish: tighter hero, distinct privacy section */
.hero{
  grid-template-columns:190px 1fr !important;
  gap:52px !important;
  align-items:center !important;
  padding:88px 0 96px !important;
}
.hero-visual{
  justify-content:center !important;
}
.hero-icon{
  width:138px !important;
  height:138px !important;
  border-radius:28px !important;
}
.hero h1{
  max-width:700px !important;
  font-size:clamp(46px,5.3vw,68px) !important;
  line-height:1.01 !important;
}
.hero .lead{
  max-width:650px !important;
  margin-top:24px !important;
}
.hero .ctas{
  margin-top:26px !important;
}
.hero-note{
  margin-top:15px !important;
  color:var(--soft) !important;
}

.privacy{
  grid-template-columns:.95fr 1.05fr !important;
  gap:72px !important;
  align-items:start !important;
}
.privacy > div:first-child{
  display:block !important;
}
.privacy > div:first-child img{
  display:none !important;
}
.privacy-copy-left{
  max-width:500px;
}
.privacy-copy-left h2{
  margin-top:12px;
}
.privacy-copy-left p{
  margin-top:22px;
  color:var(--muted);
  font-size:18px;
  line-height:1.8;
}
.privacy-points{
  padding-top:30px;
  border-top:1px solid var(--line);
}
.privacy-points .checks{
  grid-template-columns:1fr !important;
  gap:16px !important;
  margin-top:0 !important;
}
.privacy-points .check{
  font-size:16px !important;
}
.privacy-points .ctas{
  justify-content:flex-start !important;
  margin-top:28px !important;
}

@media(max-width:760px){
  .hero{
    grid-template-columns:1fr !important;
    gap:28px !important;
    padding:64px 0 72px !important;
  }
  .hero-icon{
    width:104px !important;
    height:104px !important;
    border-radius:22px !important;
  }
  .privacy{
    grid-template-columns:1fr !important;
    gap:34px !important;
  }
}
'''

home = HOME.read_text()

home = home.replace(
    '<p class="hero-note">Built by Vanta Labs in Manchester, UK.</p>',
    '<p class="hero-note">Built by Vanta Labs.</p>'
)

old_privacy = '''<section class="section" id="privacy">
<div class="privacy">
<div><img src="/guardian.png" alt="Guardian app icon"></div>
<div>
<span class="kicker">Private by design</span>
<h2>Family location should stay in the family.</h2>
<p>Guardian uses a private, parent-managed family account. There are no public profiles, adverts or social feeds.</p>
<div class="checks">
<div class="check"><b>✓</b><span>No public profiles or follower system</span></div>
<div class="check"><b>✓</b><span>No advertising or third-party ad tracking</span></div>
<div class="check"><b>✓</b><span>Owner controls for family management</span></div>
<div class="check"><b>✓</b><span>Optional parent location sharing</span></div>
</div>
<div class="ctas" style="justify-content:flex-start">
<a class="btn" href="/guardian/privacy-and-location-sharing/">Read about privacy</a>
<a class="btn" href="/privacy.html">Vanta Labs Privacy Policy</a>
</div>
</div>
</div>
</section>'''

new_privacy = '''<section class="section" id="privacy">
<div class="privacy">
<div class="privacy-copy-left">
<span class="kicker">Private by design</span>
<h2>Family location should stay in the family.</h2>
<p>Guardian uses a private, parent-managed family account. There are no public profiles, adverts or social feeds.</p>
</div>

<div class="privacy-points">
<div class="checks">
<div class="check"><b>✓</b><span>No public profiles or follower system</span></div>
<div class="check"><b>✓</b><span>No advertising or third-party ad tracking</span></div>
<div class="check"><b>✓</b><span>Owner controls for family management</span></div>
<div class="check"><b>✓</b><span>Optional parent location sharing</span></div>
</div>
<div class="ctas">
<a class="btn" href="/guardian/privacy-and-location-sharing/">Read about privacy</a>
<a class="btn" href="/privacy.html">Vanta Labs Privacy Policy</a>
</div>
</div>
</div>
</section>'''

if old_privacy not in home:
    raise SystemExit("Could not find current privacy section.")
home = home.replace(old_privacy, new_privacy, 1)

CSS.write_text(css)
HOME.write_text(home)

print("Guardian hero and privacy polish applied.")
print("Hero tightened and simplified.")
print("Privacy section rebuilt to avoid repeating the hero layout.")
print("Built by line changed to 'Built by Vanta Labs.'")
print("Nothing was committed, pushed or deployed.")
print("Refresh http://localhost:8000/guardian/")
