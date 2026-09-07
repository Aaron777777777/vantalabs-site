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

backup = ROOT / "guardian.before-simplified-vanta"
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
.head{position:relative;z-index:2;border-bottom:1px solid var(--line)}
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
  width:min(860px,calc(100% - 44px));
  margin:0 auto;
  padding:90px 0 100px;
  text-align:center;
  border-bottom:1px solid var(--line);
}
.hero-icon{
  display:block;
  width:116px;
  height:116px;
  object-fit:cover;
  border-radius:24px;
  margin:0 auto 28px;
  box-shadow:0 20px 42px rgba(0,0,0,.45);
}
.eyebrow,.kicker,.label{
  display:block;
  color:var(--gold);
  font-size:11px;
  font-weight:900;
  letter-spacing:.24em;
  text-transform:uppercase;
}
.eyebrow{margin-bottom:18px}
h1{
  font-size:clamp(46px,6vw,72px);
  line-height:1;
  letter-spacing:-.058em;
  font-weight:800;
}
.lead{
  max-width:680px;
  margin:28px auto 0;
  color:var(--muted);
  font-size:20px;
  line-height:1.72;
}
.ctas{
  display:flex;
  justify-content:center;
  flex-wrap:wrap;
  gap:10px;
  margin-top:30px;
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
.btn.disabled{opacity:.52;cursor:not-allowed}
.hero-note{
  margin-top:18px;
  color:var(--soft);
  font-size:13px;
}
.section{
  position:relative;
  z-index:1;
  width:min(var(--max),calc(100% - 44px));
  margin:0 auto;
  padding:88px 0;
  border-bottom:1px solid var(--line);
}
.section-head{
  max-width:720px;
  margin-bottom:44px;
}
.section h2{
  margin-top:12px;
  font-size:clamp(38px,5vw,62px);
  line-height:1;
  letter-spacing:-.06em;
  font-weight:850;
}
.section-head p{
  margin-top:22px;
  color:var(--muted);
  font-size:18px;
  line-height:1.8;
}
.journey{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:20px;
}
.step{
  padding:24px;
  border:1px solid var(--line);
  border-radius:22px;
  background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.012));
}
.step-num{
  color:var(--gold);
  font-size:12px;
  font-weight:900;
  letter-spacing:.18em;
}
.step h3{
  margin-top:26px;
  font-size:24px;
  line-height:1.05;
  letter-spacing:-.045em;
}
.step p{
  margin-top:12px;
  color:var(--muted);
  font-size:14px;
}
.feature-row{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:20px;
}
.feature{
  padding:26px;
  border-top:1px solid var(--line);
}
.feature h3{
  margin-top:18px;
  font-size:26px;
  line-height:1.05;
  letter-spacing:-.045em;
}
.feature p{
  margin-top:12px;
  color:var(--muted);
  font-size:15px;
}
.privacy{
  display:grid;
  grid-template-columns:.8fr 1.2fr;
  gap:56px;
  align-items:center;
}
.privacy img{
  width:132px;
  height:132px;
  object-fit:cover;
  border-radius:26px;
  box-shadow:0 20px 42px rgba(0,0,0,.45);
}
.privacy h2{margin-top:12px}
.privacy p{
  margin-top:22px;
  color:var(--muted);
  font-size:18px;
  line-height:1.8;
}
.checks{display:grid;gap:12px;margin-top:24px}
.check{display:flex;gap:10px;color:var(--muted)}
.check b{color:var(--gold)}
.related{
  width:min(var(--max),calc(100% - 44px));
  margin:0 auto;
  padding:72px 0 84px;
}
.related h2{
  font-size:42px;
  line-height:1;
  letter-spacing:-.055em;
  margin-bottom:28px;
}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:18px}
.card{
  padding:22px;
  border:1px solid var(--line);
  border-radius:20px;
  background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.012));
}
.card small{
  color:var(--gold);
  font-size:11px;
  font-weight:900;
  letter-spacing:.15em;
  text-transform:uppercase;
}
.card strong{
  display:block;
  margin-top:10px;
  font-size:23px;
  line-height:1.1;
  letter-spacing:-.04em;
}
.body,.faq{
  width:min(860px,calc(100% - 44px));
  margin:0 auto;
  padding:72px 0;
}
.notice{
  padding:18px 20px;
  border:1px solid rgba(201,166,70,.24);
  border-radius:18px;
  background:rgba(201,166,70,.045);
  color:var(--muted);
  margin-bottom:36px;
}
.body section{padding:30px 0;border-top:1px solid var(--line)}
.body h2,.faq h2{
  font-size:38px;
  line-height:1.06;
  letter-spacing:-.05em;
}
.body p,.faq p{
  margin-top:14px;
  color:var(--muted);
  font-size:17px;
  line-height:1.8;
}
.faq details{padding:20px 0;border-top:1px solid var(--line)}
.faq summary{cursor:pointer;font-weight:800}
footer{
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
  .journey{grid-template-columns:repeat(2,1fr)}
  .feature-row{grid-template-columns:1fr}
  .privacy{grid-template-columns:1fr}
}
@media(max-width:560px){
  nav,.hero,.section,.related,footer{width:min(100% - 28px,var(--max))}
  nav{height:auto;padding:22px 0 18px}
  .brand{font-size:11px}
  .links{display:none}
  .hero{padding:64px 0 72px}
  .hero-icon{width:92px;height:92px;border-radius:20px}
  h1{font-size:46px}
  .lead{font-size:18px}
  .ctas .btn{width:100%;justify-content:center}
  .section{padding:64px 0}
  .journey,.grid{grid-template-columns:1fr}
  .privacy{gap:30px}
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
<img class="hero-icon" src="/guardian.png" alt="Guardian family tracker app icon">
<span class="eyebrow">Guardian · Family Tracker</span>
<h1>Know they got there.<br>Without checking every five minutes.</h1>
<p class="lead">Home and School alerts, a private family map, location history, battery status and SOS tools—kept simple.</p>
<div class="ctas">
<a class="btn disabled" data-store="ios" aria-disabled="true">App Store — coming soon</a>
<a class="btn disabled" data-store="android" aria-disabled="true">Google Play — coming soon</a>
</div>
<p class="hero-note">Built by Vanta Labs in Manchester, UK.</p>
</section>

<section class="section" id="routine">
<div class="section-head">
<span class="kicker">The everyday routine</span>
<h2>Four updates that matter.</h2>
<p>Guardian is built around ordinary family journeys—not constant map checking.</p>
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
<span class="kicker">Guardian features</span>
<h2>The useful bits, all in one place.</h2>
</div>
<div class="feature-row">
<article class="feature"><span class="label">Location</span><h3>Private Family Map</h3><p>See the latest available location of connected family devices when you need context.</p></article>
<article class="feature"><span class="label">Safety</span><h3>Safe zones and SOS</h3><p>Receive Home and School alerts, and urgent SOS notifications from a connected child device.</p></article>
<article class="feature"><span class="label">Status</span><h3>History, battery and updates</h3><p>Review recent location records, battery level and the time of the latest device update.</p></article>
</div>
</section>

<section class="section" id="privacy">
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

print("Simplified Guardian page applied.")
print("Backup created at guardian.before-simplified-vanta/")
print("Nothing was committed, pushed or deployed.")
print("Refresh http://localhost:8000/guardian/")
