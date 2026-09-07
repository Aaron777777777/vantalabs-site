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

backup = ROOT / "guardian.before-muted-lower-section"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

updated = 0

for page in GUARDIAN.rglob("index.html"):
    if page == HOME:
        continue

    text = page.read_text()

    # Remove the lower coming-soon strip, including all inner markup.
    text, removed = re.subn(
        r'\s*<section class="detail-store-strip">.*?</section>\s*',
        '\n',
        text,
        flags=re.S,
    )

    page.write_text(text)
    updated += 1

css = CSS.read_text()
css += r'''

/* Muted supporting-content pass */
.guardian-detail .guardian-lower-grid{
  padding-top:66px !important;
  padding-bottom:74px !important;
  border-top-color:rgba(246,239,226,.075) !important;
}

.guardian-detail .guardian-lower-grid .related h2,
.guardian-detail .guardian-lower-grid .faq h2{
  color:rgba(246,239,226,.58) !important;
  font-size:18px !important;
  font-weight:720 !important;
  letter-spacing:-.02em !important;
}

.guardian-detail .guardian-lower-grid .related .card{
  border-top-color:rgba(246,239,226,.07) !important;
}

.guardian-detail .guardian-lower-grid .related .card strong{
  color:rgba(246,239,226,.66) !important;
  font-size:15px !important;
  font-weight:680 !important;
}

.guardian-detail .guardian-lower-grid .related .card::after{
  color:rgba(246,239,226,.24) !important;
}

.guardian-detail .guardian-lower-grid .related .card:hover strong{
  color:rgba(246,239,226,.9) !important;
}

.guardian-detail .guardian-lower-grid .faq{
  padding:18px 20px !important;
  border-color:rgba(246,239,226,.075) !important;
  border-radius:16px !important;
  background:rgba(255,255,255,.008) !important;
}

.guardian-detail .guardian-lower-grid .faq details{
  border-top-color:rgba(246,239,226,.065) !important;
}

.guardian-detail .guardian-lower-grid .faq summary{
  color:rgba(246,239,226,.62) !important;
  font-size:13px !important;
  font-weight:650 !important;
}

.guardian-detail .guardian-lower-grid .faq details p{
  color:rgba(246,239,226,.46) !important;
}

.guardian-detail footer{
  margin-top:10px !important;
}

@media(max-width:760px){
  .guardian-detail .guardian-lower-grid{
    padding-top:54px !important;
    padding-bottom:62px !important;
  }

  .guardian-detail .guardian-lower-grid .faq{
    padding:16px 18px !important;
  }
}
'''

CSS.write_text(css)

print(f"Updated {updated} Guardian detail and guide pages.")
print("Removed the lower coming-soon section from every subpage.")
print("Dimmed Keep exploring Guardian and Quick questions.")
print("Homepage was left untouched.")
print("Nothing was committed, pushed or deployed.")
