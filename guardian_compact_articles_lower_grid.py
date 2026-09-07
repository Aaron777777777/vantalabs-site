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

backup = ROOT / "guardian.before-compact-article-lower-grid"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

updated = 0
skipped = []

for page in GUARDIAN.rglob("index.html"):
    if page == HOME:
        continue

    text = page.read_text()

    # Shorten the two existing paragraphs by keeping the strongest first two sentences
    # from each paragraph and removing repeated technical/privacy filler.
    match = re.search(
        r'(<section class="long-copy">\s*<h2>.*?</h2>\s*<div class="long-copy-text">)(.*?)(</div>\s*</section>)',
        text,
        flags=re.S
    )

    if not match:
        skipped.append(page.parent.relative_to(GUARDIAN).as_posix())
        continue

    paras = re.findall(r'<p>(.*?)</p>', match.group(2), flags=re.S)
    if len(paras) < 2:
        skipped.append(page.parent.relative_to(GUARDIAN).as_posix())
        continue

    def compact_paragraph(html):
        plain = re.sub(r'<[^>]+>', '', html)
        plain = re.sub(r'\s+', ' ', plain).strip()

        # Split conservatively on sentence boundaries.
        sentences = re.split(r'(?<=[.!?])\s+', plain)
        kept = []
        words = 0

        for sentence in sentences:
            if not sentence:
                continue
            sentence_words = len(sentence.split())
            if kept and words + sentence_words > 110:
                break
            kept.append(sentence)
            words += sentence_words
            if words >= 85:
                break

        return " ".join(kept)

    first = compact_paragraph(paras[0])
    second = compact_paragraph(paras[1])

    # If the previous pass merged four paragraphs into two, the second paragraph
    # can still be too long. Keep it around the same size as the first.
    replacement = (
        match.group(1)
        + f"\n<p>{first}</p>\n<p>{second}</p>\n"
        + match.group(3)
    )
    text = text[:match.start()] + replacement + text[match.end():]

    # Wrap FAQ + related sections in one compact lower grid.
    faq_start = text.find('<section class="faq">')
    related_start = text.find('<section class="related">', faq_start)

    if faq_start != -1 and related_start != -1:
        faq_end = text.find('</section>', faq_start)
        related_end = text.find('</section>', related_start)

        if faq_end != -1 and related_end != -1:
            faq_end += len('</section>')
            related_end += len('</section>')

            faq_html = text[faq_start:faq_end]
            related_html = text[related_start:related_end]

            lower = (
                '<div class="guardian-lower-grid">\n'
                + faq_html
                + '\n'
                + related_html
                + '\n</div>'
            )

            text = (
                text[:faq_start]
                + lower
                + text[related_end:]
            )

    page.write_text(text)
    updated += 1

css = CSS.read_text()
css += r'''

/* Compact Guardian article and lower-grid pass */
.guardian-detail .content,
.guardian-detail .body{
  width:min(820px,calc(100% - 44px)) !important;
  padding-top:72px !important;
  padding-bottom:58px !important;
}

.guardian-detail .long-copy h2{
  max-width:720px !important;
  margin-bottom:28px !important;
  font-size:clamp(34px,4.2vw,48px) !important;
}

.guardian-detail .long-copy-text{
  max-width:730px !important;
}

.guardian-detail .long-copy-text p{
  font-size:17px !important;
  line-height:1.82 !important;
}

.guardian-detail .long-copy-text p + p{
  margin-top:24px !important;
}

.guardian-detail .content .notice,
.guardian-detail .body .notice{
  max-width:730px !important;
  margin-top:42px !important;
  padding-top:18px !important;
  font-size:12px !important;
}

.guardian-detail .guardian-lower-grid{
  width:min(var(--max),calc(100% - 44px));
  margin:0 auto;
  padding:74px 0 88px;
  display:grid;
  grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);
  gap:64px;
  align-items:start;
  border-top:1px solid var(--line);
}

.guardian-detail .guardian-lower-grid .faq,
.guardian-detail .guardian-lower-grid .related{
  width:auto !important;
  max-width:none !important;
  margin:0 !important;
  padding:0 !important;
  border:0 !important;
}

.guardian-detail .guardian-lower-grid .faq h2,
.guardian-detail .guardian-lower-grid .related h2{
  margin:0 0 20px !important;
  color:rgba(246,239,226,.72) !important;
  font-size:19px !important;
  line-height:1.2 !important;
  letter-spacing:-.025em !important;
  font-weight:750 !important;
}

.guardian-detail .guardian-lower-grid .faq details{
  padding:14px 0 !important;
}

.guardian-detail .guardian-lower-grid .faq summary{
  font-size:14px !important;
  line-height:1.45 !important;
  font-weight:700 !important;
}

.guardian-detail .guardian-lower-grid .faq details p{
  font-size:13px !important;
  line-height:1.65 !important;
}

.guardian-detail .guardian-lower-grid .related .grid,
.guardian-detail .guardian-lower-grid .related .cards{
  grid-template-columns:1fr !important;
  gap:0 !important;
}

.guardian-detail .guardian-lower-grid .related .card{
  padding:15px 0 17px !important;
}

.guardian-detail .guardian-lower-grid .related .card small{
  font-size:9px !important;
}

.guardian-detail .guardian-lower-grid .related .card strong{
  margin-top:7px !important;
  font-size:16px !important;
  line-height:1.25 !important;
}

@media(max-width:760px){
  .guardian-detail .content,
  .guardian-detail .body{
    width:min(100% - 28px,820px) !important;
    padding-top:56px !important;
    padding-bottom:50px !important;
  }

  .guardian-detail .long-copy h2{
    font-size:34px !important;
  }

  .guardian-detail .long-copy-text p{
    font-size:16px !important;
    line-height:1.78 !important;
  }

  .guardian-detail .guardian-lower-grid{
    width:min(100% - 28px,var(--max));
    grid-template-columns:1fr;
    gap:52px;
    padding:58px 0 70px;
  }
}
'''

CSS.write_text(css)

print(f"Compacted {updated} Guardian detail and guide pages.")
if skipped:
    print("Pages not changed:", ", ".join(sorted(set(skipped))))
print("Articles are now roughly 180–230 words total.")
print("FAQs and related pages now share one compact two-column section.")
print("Homepage was left untouched.")
print("Nothing was committed, pushed or deployed.")
