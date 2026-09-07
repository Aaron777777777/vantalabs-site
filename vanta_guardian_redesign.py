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
    raise SystemExit("Guardian folder is missing. Run: python3 build_guardian_seo.py")
if not (ROOT / "guardian.png").exists():
    raise SystemExit("guardian.png is missing.")

backup = ROOT / "guardian.before-vanta-redesign"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

css = r'''
:root{
  --bg:#030303;
  --text:#f6efe2;
  --muted:rgba(246,239,226,.68);
  --soft:rgba(246,239,226,.38);
  --line:rgba(246,239,226,.10);
  --gold:#c9a646;
  --max:1120px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  min-height:100vh;
  font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color:var(--text);
  background:
    radial-gradient(circle at 24% 0%,rgba(201,166,70,.08),transparent 28%),
    linear-gradient(180deg,#080806 0%,#020202 45%,#000 100%);
  line-height:1.65;
}
body::before{
  content:"";
  position:fixed;
  inset:0;
  pointer-events:none;
  background-image:
    linear-gradient(rgba(255,255,255,.012) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.012) 1px,transparent 1px);
  background-size:92px 92px;
  opacity:.42;
  mask-image:linear-gradient(to bottom,black 0%,rgba(0,0,0,.6) 40%,transparent 70%);
}
a{color:inherit;text-decoration:none}
img{max-width:100%;height:auto}
.head{
  position:relative;
  z-index:2;
  background:transparent;
  border-bottom:1px solid var(--line);
}
nav{
  width:min(var(--max),calc(100% - 44px));
  height:86px;
  margin:0 auto;
  display:flex;
  justify-content:space-between;
  align-items:center;
}
.brand{
  color:var(--gold);
  font-size:13px;
  font-weight:900;
  letter-spacing:.24em;
  text-transform:uppercase;
}
.links{display:flex;gap:26px}
.links a{color:var(--muted);font-size:14px;font-weight:650}
.links a:hover{color:var(--text)}
.hero{
  position:relative;
  z-index:1;
  width:min(var(--max),calc(100% - 44px));
  margin:0 auto;
  padding:96px 0 112px;
  display:grid;
  grid-template-columns:1.15fr .85fr;
  gap:72px;
  align-items:start;
  border-bottom:1px solid var(--line);
}
.hero-copy{max-width:720px}
.eyebrow,.kicker,.label{
  display:block;
  color:var(--gold);
  font-size:11px;
  font-weight:900;
  letter-spacing:.24em;
  text-transform:uppercase;
}
.eyebrow{margin-bottom:22px}
h1{
  max-width:820px;
  font-size:clamp(46px,6vw,76px);
  line-height:1.01;
  letter-spacing:-.057em;
  font-weight:800;
}
.lead{
  max-width:650px;
  margin-top:34px;
  color:var(--muted);
  font-size:20px;
  line-height:1.72;
}
.ctas{
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  margin-top:32px;
}
.btn{
  display:inline-flex;
  align-items:center;
  width:fit-content;
  padding:11px 15px;
  border:1px solid rgba(201,166,70,.28);
  border-radius:999px;
  color:var(--gold);
  background:rgba(201,166,70,.045);
  font-size:13px;
  font-weight:850;
}
.btn:hover{
  border-color:rgba(201,166,70,.52);
  background:rgba(201,166,70,.085);
}
.btn.primary,.btn.secondary,.btn.ghost{color:var(--gold);background:rgba(201,166,70,.045)}
.btn.disabled{opacity:.52;cursor:not-allowed}
.product-panel{
  min-height:420px;
  padding:34px;
  border:1px solid var(--line);
  border-radius:28px;
  background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.014));
  display:flex;
  flex-direction:column;
  justify-content:space-between;
}
.product-panel img{
  width:104px;
  height:104px;
  object-fit:cover;
  border-radius:20px;
  box-shadow:0 20px 42px rgba(0,0,0,.45);
}
.product-panel h2{
  margin-top:28px;
  font-size:38px;
  line-height:1;
  letter-spacing:-.055em;
}
.product-panel p{
  margin-top:18px;
  color:var(--muted);
  font-size:17px;
  line-height:1.65;
}
.panel-list{
  display:grid;
  gap:14px;
  margin-top:28px;
  padding-top:22px;
  border-top:1px solid var(--line);
}
.panel-item{
  display:grid;
  grid-template-columns:32px 1fr;
  gap:12px;
  align-items:start;
}
.panel-num{
  color:var(--gold);
  font-size:12px;
  font-weight:900;
  letter-spacing:.12em;
}
.panel-item strong{display:block;font-size:15px}
.panel-item span{display:block;color:var(--soft);font-size:13px;margin-top:2px}
.section{
  position:relative;
  z-index:1;
  width:min(var(--max),calc(100% - 44px));
  margin:0 auto;
  padding:110px 0;
  border-bottom:1px solid var(--line);
}
.section-head{max-width:760px;margin-bottom:62px}
.section h2,.body h2,.faq h2,.related h2{
  font-size:clamp(38px,5.5vw,68px);
  line-height:.98;
  letter-spacing:-.062em;
  font-weight:850;
}
.section-head p,.section-intro{
  margin-top:26px;
  color:var(--muted);
  font-size:18px;
  line-height:1.8;
}
.journey,.features{
  display:grid;
  gap:28px;
}
.journey{grid-template-columns:repeat(4,1fr)}
.features{grid-template-columns:repeat(3,1fr)}
.step,.feature,.card{
  min-height:220px;
  padding:28px;
  border:1px solid var(--line);
  border-radius:24px;
  background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.014));
}
.step-num{
  color:var(--gold);
  font-size:12px;
  font-weight:900;
  letter-spacing:.18em;
}
.step h3,.feature h3{
  margin-top:38px;
  font-size:28px;
  line-height:1.05;
  letter-spacing:-.045em;
}
.step p,.feature p{
  margin-top:14px;
  color:var(--muted);
  font-size:15px;
  line-height:1.7;
}
.feature .label{margin-bottom:46px}
.privacy{
  display:grid;
  grid-template-columns:.7fr 1.3fr;
  gap:70px;
  align-items:center;
}
.privacy-visual{
  padding:32px;
  border:1px solid var(--line);
  border-radius:28px;
  background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.014));
}
.privacy-visual img{
  display:block;
  width:150px;
  height:150px;
  object-fit:cover;
  border-radius:28px;
}
.privacy-copy h2{margin-top:16px}
.checks{display:grid;gap:14px;margin-top:28px}
.check{
  display:flex;
  gap:12px;
  color:var(--muted);
  font-size:16px;
}
.check b{color:var(--gold)}
.download{
  text-align:left;
  display:grid;
  grid-template-columns:110px 1fr;
  gap:34px;
  align-items:center;
  padding:38px;
  border:1px solid var(--line);
  border-radius:28px;
  background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.014));
}
.download img{
  width:104px;
  height:104px;
  object-fit:cover;
  border-radius:20px;
}
.download h2{
  font-size:42px;
  line-height:1;
  letter-spacing:-.055em;
}
.download p{margin-top:14px;color:var(--muted);font-size:17px}
.body,.faq,.related{
  position:relative;
  z-index:1;
  width:min(860px,calc(100% - 44px));
  margin:0 auto;
  padding:84px 0;
}
.notice{
  padding:18px 20px;
  border:1px solid rgba(201,166,70,.24);
  border-radius:18px;
  background:rgba(201,166,70,.045);
  color:var(--muted);
  margin-bottom:38px;
}
.body section{
  padding:34px 0;
  border-top:1px solid var(--line);
}
.body h2{font-size:38px;line-height:1.06}
.body p{margin-top:14px;color:var(--muted);font-size:17px;line-height:1.8}
.faq h2,.related h2{font-size:44px;margin-bottom:26px}
.faq details{
  padding:20px 0;
  border-top:1px solid var(--line);
}
.faq summary{cursor:pointer;font-weight:800}
.faq p{margin-top:12px;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.card{min-height:auto;text-decoration:none}
.card small{color:var(--gold);font-size:11px;font-weight:900;letter-spacing:.15em;text-transform:uppercase}
.card strong{display:block;margin-top:12px;font-size:24px;line-height:1.1;letter-spacing:-.04em}
footer{
  position:relative;
  z-index:1;
  width:min(var(--max),calc(100% - 44px));
  margin:0 auto;
  display:flex;
  justify-content:space-between;
  gap:20px;
  padding:30px 0 34px;
  color:var(--soft);
  font-size:13px;
}
@media(max-width:900px){
  .hero,.privacy{grid-template-columns:1fr}
  .journey{grid-template-columns:repeat(2,1fr)}
  .features{grid-template-columns:repeat(2,1fr)}
  .product-panel{min-height:auto}
}
@media(max-width:560px){
  nav,.hero,.section,footer{width:min(100% - 28px,var(--max))}
  nav{height:auto;padding:22px 0 18px}
  .brand{font-size:11px}
  .links{display:none}
  .hero{padding:58px 0 68px;gap:38px}
  h1{font-size:48px;line-height:.98}
  .lead{font-size:18px;margin-top:26px}
  .product-panel{padding:24px;border-radius:24px}
  .product-panel img{width:72px;height:72px;border-radius:18px}
  .product-panel h2{font-size:30px}
  .section{padding:64px 0}
  .section-head{margin-bottom:34px}
  .section h2{font-size:36px}
  .journey,.features,.grid{grid-template-columns:1fr}
  .step,.feature{min-height:auto;padding:24px}
  .privacy{gap:32px}
  .privacy-visual img{width:110px;height:110px}
  .download{grid-template-columns:1fr;padding:28px}
  .download h2{font-size:34px}
  .body,.faq,.related{width:min(100% - 28px,860px);padding:62px 0}
  footer{flex-direction:column}
}
'''

home = r'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Guardian Family Tracker App | Home, School and SOS Alerts</title>
<meta name="description" content="Guardian helps parents stay connected with private child location sharing, Home and School alerts, location history, battery status and SOS tools.">
<link rel="canonical" href="https://www.vantalabs.co.uk/guardian/">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Vanta Labs">
<meta property="og:title" content="Guardian Family Tracker App">
<meta property="og:description" content="Private family location sharing, Home and School alerts, SOS and useful device status.">
<meta property="og:url" content="https://www.vantalabs.co.uk/guardian/">
<meta property="og:image" content="https://www.vantalabs.co.uk/guardian.png">
<link rel="icon" href="/guardian.png">
<link rel="stylesheet" href="/guardian/assets/guardian.css">
<script defer src="/guardian/assets/app-links.js"></script>
</head>
<body>
<header class="head">
<nav>
<a class="brand" href="/">Vanta Labs</a>
<div class="links">
<a href="#routine">Routine</a>
<a href="#features">Features</a>
<a href="#privacy">Privacy</a>
<a href="/guardian/guides/what-is-a-family-safety-app/">Guides</a>
</div>
</nav>
</header>

<main>
<section class="hero">
<div class="hero-copy">
<span class="eyebrow">Guardian · Family Tracker</span>
<h1>Know they got there. Without checking every five minutes.</h1>
<p class="lead">Guardian helps parents follow the moments that matter: leaving Home, arriving at School, getting back safely, or asking for help.</p>
<div class="ctas">
<a class="btn primary disabled" data-store="ios" aria-disabled="true">App Store — coming soon</a>
<a class="btn secondary disabled" data-store="android" aria-disabled="true">Google Play — coming soon</a>
<a class="btn ghost" href="#routine">How Guardian fits into the day</a>
</div>
</div>

<aside class="product-panel">
<div>
<img src="/guardian.png" alt="Guardian family tracker app icon">
<h2>Family safety, kept simple.</h2>
<p>No public profiles. No adverts. No social feed. Just useful family updates and clear tools when you need them.</p>
</div>
<div class="panel-list">
<div class="panel-item"><span class="panel-num">01</span><div><strong>Home and School alerts</strong><span>Know when everyday journeys begin and end.</span></div></div>
<div class="panel-item"><span class="panel-num">02</span><div><strong>Private Family Map</strong><span>Check the latest available location when context matters.</span></div></div>
<div class="panel-item"><span class="panel-num">03</span><div><strong>SOS and device status</strong><span>See urgent alerts, battery level and last update time.</span></div></div>
</div>
</aside>
</section>

<section class="section" id="routine">
<div class="section-head">
<span class="kicker">The everyday routine</span>
<h2>Four updates. One less thing to worry about.</h2>
<p>Guardian is built around the simple moments parents actually care about—not watching a moving dot all day.</p>
</div>
<div class="journey">
<article class="step"><span class="step-num">01</span><h3>Leaves Home</h3><p>The morning journey has started.</p></article>
<article class="step"><span class="step-num">02</span><h3>Arrives at School</h3><p>The reassuring arrival notification.</p></article>
<article class="step"><span class="step-num">03</span><h3>Leaves School</h3><p>The journey home has begun.</p></article>
<article class="step"><span class="step-num">04</span><h3>Arrives Home</h3><p>They made it back safely.</p></article>
</div>
</section>

<section class="section" id="features">
<div class="section-head">
<span class="kicker">Focused family safety</span>
<h2>Everything useful. Nothing invasive.</h2>
<p>Guardian stays focused on location, familiar places and urgent family alerts. It does not read messages, block apps or turn family life into a social network.</p>
</div>
<div class="features">
<article class="feature"><span class="label">Location</span><h3>Private Family Map</h3><p>See the latest available location of connected family devices in one place.</p></article>
<article class="feature"><span class="label">Places</span><h3>Home and School zones</h3><p>Receive meaningful arrival and leaving alerts around everyday routines.</p></article>
<article class="feature"><span class="label">Urgent</span><h3>SOS alerts</h3><p>A connected child device can send an urgent alert to trusted family members.</p></article>
<article class="feature"><span class="label">History</span><h3>Recent location records</h3><p>Review useful recent updates when the latest location needs more context.</p></article>
<article class="feature"><span class="label">Status</span><h3>Battery and last update</h3><p>Understand whether a device is reporting normally and whether its location is recent.</p></article>
<article class="feature"><span class="label">Family</span><h3>Trusted adults</h3><p>Invite another parent or guardian into the private family when needed.</p></article>
</div>
</section>

<section class="section" id="privacy">
<div class="privacy">
<div class="privacy-visual"><img src="/guardian.png" alt="Guardian app icon"></div>
<div class="privacy-copy">
<span class="kicker">Private by design</span>
<h2>Family location should stay in the family.</h2>
<p class="section-intro">Guardian is built around a private, parent-managed family account—not a public network.</p>
<div class="checks">
<div class="check"><b>✓</b><span>No public profiles or follower system</span></div>
<div class="check"><b>✓</b><span>No advertising or third-party ad tracking</span></div>
<div class="check"><b>✓</b><span>Owner controls for family management</span></div>
<div class="check"><b>✓</b><span>Optional parent location sharing</span></div>
</div>
<div class="ctas">
<a class="btn ghost" href="/guardian/privacy-and-location-sharing/">Read about privacy</a>
<a class="btn ghost" href="/privacy.html">Vanta Labs Privacy Policy</a>
</div>
</div>
</div>
</section>

<section class="section">
<div class="download">
<img src="/guardian.png" alt="Guardian app icon">
<div>
<h2>Guardian is nearly ready.</h2>
<p>As soon as the official Apple and Google links are available, both download buttons will activate across the entire Guardian website.</p>
<div class="ctas">
<a class="btn primary disabled" data-store="ios" aria-disabled="true">App Store — coming soon</a>
<a class="btn secondary disabled" data-store="android" aria-disabled="true">Google Play — coming soon</a>
</div>
</div>
</div>
</section>

<section class="related">
<h2>Explore Guardian</h2>
<div class="grid">
<a class="card" href="/guardian/safe-zone-alerts/"><small>Safe zones</small><strong>Home and School alerts</strong></a>
<a class="card" href="/guardian/child-location-tracker/"><small>Location</small><strong>Child location sharing</strong></a>
<a class="card" href="/guardian/sos-alert-app-for-families/"><small>Urgent alerts</small><strong>Family SOS tools</strong></a>
<a class="card" href="/guardian/guides/location-sharing-and-family-privacy/"><small>Parent guide</small><strong>Location sharing and privacy</strong></a>
</div>
</section>
</main>

<footer>
<span>© 2026 Vanta Labs NW LTD · Manchester, UK</span>
<span><a href="/privacy.html">Privacy</a> · <a href="/terms.html">Terms</a> · <a href="/">All Vanta Labs apps</a></span>
</footer>
</body>
</html>
'''

CSS.write_text(css.strip() + "\n")
HOME.write_text(home)

print("Vanta-style Guardian redesign applied.")
print("Backup created at guardian.before-vanta-redesign/")
print("Nothing was committed, pushed or deployed.")
print("Refresh http://localhost:8000/guardian/")
