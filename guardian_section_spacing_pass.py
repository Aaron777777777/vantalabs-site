#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path.cwd()
GUARDIAN = ROOT / "guardian"
CSS = GUARDIAN / "assets" / "guardian.css"

if not (ROOT / "index.html").exists():
    raise SystemExit("Run this from ~/Projects/vantalabs-site")
if not GUARDIAN.exists() or not CSS.exists():
    raise SystemExit("Guardian files were not found.")

backup = ROOT / "guardian.before-section-spacing-pass"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

css = CSS.read_text()

marker = "/* Guardian section-spacing pass */"
if marker in css:
    css = css[:css.index(marker)].rstrip() + "\n"

css += r'''

/* Guardian section-spacing pass */
.guardian-detail .hero{
  min-height:calc(100vh - 92px) !important;
  box-sizing:border-box !important;
  display:grid !important;
  align-items:center !important;
  padding-top:72px !important;
  padding-bottom:96px !important;
}

.guardian-detail .body,
.guardian-detail .content{
  padding-top:110px !important;
  padding-bottom:104px !important;
}

.guardian-detail .guardian-lower-grid{
  margin-top:34px !important;
  padding-top:92px !important;
  padding-bottom:96px !important;
}

.guardian-detail footer{
  margin-top:18px !important;
}

@media(max-width:760px){
  .guardian-detail .hero{
    min-height:auto !important;
    padding-top:54px !important;
    padding-bottom:72px !important;
  }

  .guardian-detail .body,
  .guardian-detail .content{
    padding-top:76px !important;
    padding-bottom:74px !important;
  }

  .guardian-detail .guardian-lower-grid{
    margin-top:22px !important;
    padding-top:70px !important;
    padding-bottom:76px !important;
  }
}
'''

CSS.write_text(css)

print("Added full first-screen hero spacing to Guardian detail pages.")
print("Added more separation between the article and lower support section.")
print("Homepage content was not changed.")
print("Nothing was committed, pushed or deployed.")
