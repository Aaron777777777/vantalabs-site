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

backup = ROOT / "guardian.before-two-paragraph-pass"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

updated = 0
skipped = []

for page in GUARDIAN.rglob("index.html"):
    if page == HOME:
        continue

    text = page.read_text()

    match = re.search(
        r'(<section class="long-copy">\s*<h2>.*?</h2>\s*<div class="long-copy-text">)(.*?)(</div>\s*</section>)',
        text,
        flags=re.S
    )
    if not match:
        skipped.append(page.parent.relative_to(GUARDIAN).as_posix())
        continue

    paragraphs = re.findall(r'<p>(.*?)</p>', match.group(2), flags=re.S)
    if len(paragraphs) < 2:
        skipped.append(page.parent.relative_to(GUARDIAN).as_posix())
        continue

    clean = [re.sub(r'\s+', ' ', p).strip() for p in paragraphs]

    if len(clean) >= 4:
        first = clean[0] + " " + clean[1]
        second = clean[2] + " " + clean[3]
    else:
        split = (len(clean) + 1) // 2
        first = " ".join(clean[:split])
        second = " ".join(clean[split:])

    replacement = (
        match.group(1)
        + f"\n<p>{first}</p>\n<p>{second}</p>\n"
        + match.group(3)
    )

    text = text[:match.start()] + replacement + text[match.end():]
    page.write_text(text)
    updated += 1

css = CSS.read_text()
css += r'''

/* Two-paragraph article and quieter FAQ pass */
.guardian-detail .long-copy-text{
  max-width:760px !important;
}

.guardian-detail .long-copy-text p{
  font-size:18px !important;
  line-height:1.88 !important;
}

.guardian-detail .long-copy-text p + p{
  margin-top:30px !important;
}

.guardian-detail .faq{
  padding-top:64px !important;
  padding-bottom:72px !important;
}

.guardian-detail .faq h2{
  margin:0 0 18px !important;
  color:rgba(246,239,226,.72) !important;
  font-size:20px !important;
  line-height:1.2 !important;
  letter-spacing:-.02em !important;
  font-weight:750 !important;
}

.guardian-detail .faq details{
  padding:17px 0 !important;
}

.guardian-detail .faq summary{
  color:rgba(246,239,226,.78) !important;
  font-size:15px !important;
  font-weight:700 !important;
}

.guardian-detail .faq details p{
  color:rgba(246,239,226,.58) !important;
  font-size:14px !important;
  line-height:1.7 !important;
}

@media(max-width:760px){
  .guardian-detail .long-copy-text p{
    font-size:17px !important;
    line-height:1.82 !important;
  }

  .guardian-detail .long-copy-text p + p{
    margin-top:24px !important;
  }

  .guardian-detail .faq{
    padding-top:52px !important;
    padding-bottom:60px !important;
  }
}
'''

CSS.write_text(css)

print(f"Reduced {updated} Guardian pages to two long-form paragraphs.")
if skipped:
    print("Pages not changed:", ", ".join(sorted(set(skipped))))
print("FAQ headings and questions are now smaller and quieter.")
print("Homepage was left untouched.")
print("Nothing was committed, pushed or deployed.")
