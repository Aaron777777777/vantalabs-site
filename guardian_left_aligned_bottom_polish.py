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

backup = ROOT / "guardian.before-left-aligned-bottom-polish"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

updated = 0
skipped = []

for page in GUARDIAN.rglob("index.html"):
    if page == HOME:
        continue

    text = page.read_text()

    # Shorten article copy again: retain the strongest opening sentences
    # from each of the current two paragraphs.
    match = re.search(
        r'(<section class="long-copy">\s*<h2>.*?</h2>\s*<div class="long-copy-text">)(.*?)(</div>\s*</section>)',
        text,
        flags=re.S,
    )

    if not match:
        skipped.append(page.parent.relative_to(GUARDIAN).as_posix())
        continue

    paragraphs = re.findall(r'<p>(.*?)</p>', match.group(2), flags=re.S)

    if len(paragraphs) >= 2:
        def trim_to_sentences(html, maximum_words=72):
            plain = re.sub(r'<[^>]+>', '', html)
            plain = re.sub(r'\s+', ' ', plain).strip()
            sentences = re.split(r'(?<=[.!?])\s+', plain)

            kept = []
            words = 0
            for sentence in sentences:
                count = len(sentence.split())
                if kept and words + count > maximum_words:
                    break
                kept.append(sentence)
                words += count
                if words >= 55:
                    break

            return " ".join(kept)

        first = trim_to_sentences(paragraphs[0])
        second = trim_to_sentences(paragraphs[1])

        replacement = (
            match.group(1)
            + f"\n<p>{first}</p>\n<p>{second}</p>\n"
            + match.group(3)
        )
        text = text[:match.start()] + replacement + text[match.end():]

    # Rename the lower headings.
    text = text.replace(
        '<section class="faq"><h2>Questions parents ask</h2>',
        '<section class="faq"><h2>Quick questions</h2>',
        1,
    )
    text = text.replace(
        '<section class="related"><h2>Related Guardian pages</h2>',
        '<section class="related"><h2>Keep exploring Guardian</h2>',
        1,
    )

    # Rebuild the lower grid with related links first and FAQ second.
    grid_match = re.search(
        r'<div class="guardian-lower-grid">\s*(<section class="faq">.*?</section>)\s*(<section class="related">.*?</section>)\s*</div>',
        text,
        flags=re.S,
    )

    if grid_match:
        faq_html = grid_match.group(1)
        related_html = grid_match.group(2)

        rebuilt = (
            '<div class="guardian-lower-grid">\n'
            + related_html
            + '\n'
            + faq_html
            + '\n</div>'
        )

        text = text[:grid_match.start()] + rebuilt + text[grid_match.end():]

    # Add the final store strip once.
    if 'class="detail-store-strip"' not in text:
        lower_end = text.find('</div>', text.find('<div class="guardian-lower-grid">'))
        if lower_end != -1:
            # Find the actual closing div for guardian-lower-grid using a simple
            # forward search to the following </main>, then insert after the last
            # </div> before </main>.
            main_end = text.find('</main>')
            insert_at = text.rfind('</div>', 0, main_end)

            if insert_at != -1:
                insert_at += len('</div>')
                strip = '''
<section class="detail-store-strip">
<div>
<span class="eyebrow">Guardian is nearly ready</span>
<h2>Coming soon to iPhone and Android.</h2>
<p>The download buttons will activate as soon as the official store links are added.</p>
<div class="ctas">
<a class="btn disabled" data-store="ios" aria-disabled="true">App Store — coming soon</a>
<a class="btn alt disabled" data-store="android" aria-disabled="true">Google Play — coming soon</a>
</div>
</div>
</section>
'''
                text = text[:insert_at] + strip + text[insert_at:]

    # Simplify and repair the footer wording.
    text = re.sub(
        r'<span>© 2026 Vanta Labs NW LTD · Manchester, UK</span>',
        '<span>© 2026 Vanta Labs NW LTD</span>',
        text,
    )
    text = re.sub(
        r'<a href="/">Vanta Labs</a>',
        '<a href="/">All Vanta Labs apps</a>',
        text,
    )

    page.write_text(text)
    updated += 1

css = CSS.read_text()
css += r'''

/* Left-aligned article and finished lower-page layout */
.guardian-detail .content,
.guardian-detail .body{
  width:min(var(--max),calc(100% - 44px)) !important;
  margin:0 auto !important;
  padding:72px 0 58px !important;
  text-align:left !important;
}

.guardian-detail .long-copy{
  max-width:760px !important;
  margin:0 !important;
  text-align:left !important;
}

.guardian-detail .long-copy h2{
  max-width:650px !important;
  margin:0 0 25px !important;
  font-size:clamp(30px,3.6vw,42px) !important;
  line-height:1.08 !important;
  letter-spacing:-.045em !important;
}

.guardian-detail .long-copy-text{
  max-width:710px !important;
  margin:0 !important;
}

.guardian-detail .long-copy-text p{
  font-size:17px !important;
  line-height:1.82 !important;
}

.guardian-detail .long-copy-text p + p{
  margin-top:22px !important;
}

.guardian-detail .content .notice,
.guardian-detail .body .notice{
  max-width:710px !important;
  margin:38px 0 0 !important;
  padding:17px 0 0 !important;
}

.guardian-detail .guardian-lower-grid{
  width:min(var(--max),calc(100% - 44px)) !important;
  margin:0 auto !important;
  padding:76px 0 78px !important;
  grid-template-columns:minmax(0,1.2fr) minmax(300px,.8fr) !important;
  gap:72px !important;
  text-align:left !important;
}

.guardian-detail .guardian-lower-grid .related h2,
.guardian-detail .guardian-lower-grid .faq h2{
  margin:0 0 22px !important;
  color:var(--text) !important;
  font-size:22px !important;
  font-weight:800 !important;
  letter-spacing:-.035em !important;
}

.guardian-detail .guardian-lower-grid .related .grid,
.guardian-detail .guardian-lower-grid .related .cards{
  display:grid !important;
  grid-template-columns:1fr !important;
  gap:0 !important;
}

.guardian-detail .guardian-lower-grid .related .card{
  position:relative;
  padding:19px 34px 21px 0 !important;
  border-top:1px solid var(--line) !important;
}

.guardian-detail .guardian-lower-grid .related .card::after{
  content:"→";
  position:absolute;
  right:2px;
  top:22px;
  color:rgba(246,239,226,.42);
  transition:color .18s ease, transform .18s ease;
}

.guardian-detail .guardian-lower-grid .related .card:hover::after{
  color:var(--gold);
  transform:translateX(3px);
}

.guardian-detail .guardian-lower-grid .related .card small{
  display:none !important;
}

.guardian-detail .guardian-lower-grid .related .card strong{
  max-width:520px;
  margin:0 !important;
  font-size:17px !important;
  line-height:1.3 !important;
}

.guardian-detail .guardian-lower-grid .faq{
  padding:24px !important;
  border:1px solid var(--line) !important;
  border-radius:20px !important;
  background:rgba(255,255,255,.018) !important;
}

.guardian-detail .guardian-lower-grid .faq h2{
  margin-bottom:10px !important;
}

.guardian-detail .guardian-lower-grid .faq details{
  padding:15px 0 !important;
}

.guardian-detail .guardian-lower-grid .faq summary{
  font-size:14px !important;
  line-height:1.45 !important;
}

.guardian-detail .detail-store-strip{
  width:min(var(--max),calc(100% - 44px));
  margin:0 auto 84px;
  padding:46px 52px;
  border:1px solid var(--line);
  border-radius:24px;
  background:linear-gradient(180deg,rgba(255,255,255,.025),rgba(255,255,255,.012));
  text-align:left;
}

.guardian-detail .detail-store-strip > div{
  max-width:780px;
}

.guardian-detail .detail-store-strip h2{
  margin:10px 0 0;
  font-size:clamp(30px,3.6vw,42px);
  line-height:1.06;
  letter-spacing:-.045em;
}

.guardian-detail .detail-store-strip p{
  max-width:620px;
  margin:16px 0 0;
  color:var(--muted);
  font-size:16px;
  line-height:1.7;
}

.guardian-detail .detail-store-strip .ctas{
  justify-content:flex-start !important;
  margin-top:24px;
}

.guardian-detail footer{
  padding-top:24px !important;
}

.guardian-detail footer > div{
  display:flex !important;
  justify-content:space-between !important;
  gap:28px !important;
  align-items:center !important;
}

@media(max-width:760px){
  .guardian-detail .content,
  .guardian-detail .body{
    width:min(100% - 28px,var(--max)) !important;
    padding:56px 0 48px !important;
  }

  .guardian-detail .long-copy h2{
    font-size:32px !important;
  }

  .guardian-detail .guardian-lower-grid{
    width:min(100% - 28px,var(--max)) !important;
    grid-template-columns:1fr !important;
    gap:46px !important;
    padding:58px 0 62px !important;
  }

  .guardian-detail .detail-store-strip{
    width:min(100% - 28px,var(--max));
    margin-bottom:62px;
    padding:34px 24px;
  }

  .guardian-detail footer > div{
    align-items:flex-start !important;
    flex-direction:column !important;
    gap:12px !important;
  }
}
'''

CSS.write_text(css)

print(f"Polished {updated} Guardian detail and guide pages.")
if skipped:
    print("Pages not changed:", ", ".join(sorted(set(skipped))))
print("Article content is shorter and fully left-aligned.")
print("Related links now lead the lower section, with FAQ in a quiet side panel.")
print("Added a final coming-soon store strip and cleaned the footer.")
print("Homepage was left untouched.")
print("Nothing was committed, pushed or deployed.")
