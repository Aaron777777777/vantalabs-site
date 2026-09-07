#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path.cwd()
GUARDIAN = ROOT / "guardian"
CSS = GUARDIAN / "assets" / "guardian.css"

if not (ROOT / "index.html").exists():
    raise SystemExit("Run this from ~/Projects/vantalabs-site")
if not GUARDIAN.exists():
    raise SystemExit("Guardian folder is missing.")
if not CSS.exists():
    raise SystemExit("guardian/assets/guardian.css is missing.")

backup = ROOT / "guardian.before-detail-page-fix"
if backup.exists():
    shutil.rmtree(backup)
shutil.copytree(GUARDIAN, backup)

detail_pages = []
for page in GUARDIAN.rglob("index.html"):
    if page == GUARDIAN / "index.html":
        continue
    text = page.read_text()
    if '<body class="guardian-detail">' not in text:
        text = text.replace("<body>", '<body class="guardian-detail">', 1)
    page.write_text(text)
    detail_pages.append(page)

css = CSS.read_text()
css += r'''

/* Guardian detail and guide pages */
.guardian-detail .head{
  position:relative;
}

.guardian-detail .hero{
  width:min(var(--max),calc(100% - 44px)) !important;
  margin:0 auto !important;
  padding:78px 0 76px !important;
  display:grid !important;
  grid-template-columns:minmax(0,1fr) 180px !important;
  gap:58px !important;
  align-items:center !important;
  text-align:left !important;
  border-bottom:1px solid var(--line) !important;
}

.guardian-detail .hero > div:first-child{
  min-width:0;
  max-width:780px;
}

.guardian-detail .hero h1{
  max-width:760px !important;
  margin:12px 0 0 !important;
  font-size:clamp(42px,5.2vw,66px) !important;
  line-height:1.01 !important;
  letter-spacing:-.058em !important;
  overflow-wrap:normal !important;
  word-break:normal !important;
}

.guardian-detail .hero .lead{
  max-width:700px !important;
  margin:24px 0 0 !important;
  color:var(--muted) !important;
  font-size:18px !important;
  line-height:1.75 !important;
}

.guardian-detail .hero .ctas{
  justify-content:flex-start !important;
  margin-top:26px !important;
}

.guardian-detail .hero .text-btn{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width:fit-content;
  padding:11px 15px;
  border:1px solid rgba(201,166,70,.28);
  border-radius:999px;
  color:var(--gold);
  background:rgba(201,166,70,.045);
  font-size:13px;
  font-weight:850;
  text-decoration:none;
}

.guardian-detail .hero .store-btn{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width:fit-content;
  min-height:auto !important;
  padding:11px 15px !important;
  border:1px solid rgba(201,166,70,.28) !important;
  border-radius:999px !important;
  color:var(--gold) !important;
  background:rgba(201,166,70,.045) !important;
  font-size:13px !important;
  font-weight:850 !important;
  text-decoration:none !important;
}

.guardian-detail .hero .store-btn.secondary{
  color:var(--gold) !important;
  background:rgba(201,166,70,.045) !important;
}

.guardian-detail .hero .store-btn.disabled{
  opacity:.62 !important;
}

.guardian-detail .icon-wrap{
  width:180px !important;
  height:180px !important;
  padding:24px !important;
  border:1px solid var(--line) !important;
  border-radius:28px !important;
  background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.014)) !important;
  display:flex !important;
  align-items:center !important;
  justify-content:center !important;
  box-shadow:none !important;
}

.guardian-detail .icon-wrap img{
  display:block !important;
  width:112px !important;
  max-width:112px !important;
  height:112px !important;
  object-fit:cover !important;
  border-radius:23px !important;
  margin:0 !important;
}

.guardian-detail .content{
  width:min(820px,calc(100% - 44px)) !important;
  max-width:none !important;
  margin:0 auto !important;
  padding:64px 0 48px !important;
}

.guardian-detail .content .notice{
  margin:0 0 34px !important;
  padding:17px 19px !important;
  border:1px solid rgba(201,166,70,.22) !important;
  border-radius:16px !important;
  background:rgba(201,166,70,.04) !important;
  color:var(--muted) !important;
}

.guardian-detail .content section{
  padding:30px 0 !important;
  border-top:1px solid var(--line) !important;
}

.guardian-detail .content h2{
  margin:0 !important;
  max-width:720px;
  font-size:clamp(30px,4vw,44px) !important;
  line-height:1.06 !important;
  letter-spacing:-.05em !important;
}

.guardian-detail .content p{
  margin:15px 0 0 !important;
  color:var(--muted) !important;
  font-size:17px !important;
  line-height:1.82 !important;
}

.guardian-detail .faq{
  width:min(820px,calc(100% - 44px)) !important;
  max-width:none !important;
  margin:0 auto !important;
  padding:24px 0 62px !important;
}

.guardian-detail .faq h2{
  margin-bottom:22px !important;
  font-size:clamp(32px,4vw,46px) !important;
}

.guardian-detail .faq details{
  margin:0 !important;
  padding:19px 0 !important;
  border:0 !important;
  border-top:1px solid var(--line) !important;
  border-radius:0 !important;
  background:transparent !important;
}

.guardian-detail .faq summary{
  color:var(--text) !important;
  font-size:17px !important;
  font-weight:800 !important;
}

.guardian-detail .faq details p{
  margin-top:11px !important;
  color:var(--muted) !important;
  font-size:15px !important;
  line-height:1.75 !important;
}

.guardian-detail .related{
  width:min(var(--max),calc(100% - 44px)) !important;
  max-width:none !important;
  margin:0 auto !important;
  padding:68px 0 82px !important;
  border-top:1px solid var(--line);
}

.guardian-detail .related h2{
  margin:0 0 28px !important;
  font-size:clamp(32px,4vw,46px) !important;
}

.guardian-detail .related .cards,
.guardian-detail .related .grid{
  display:grid !important;
  grid-template-columns:repeat(2,minmax(0,1fr)) !important;
  gap:0 42px !important;
}

.guardian-detail .related .card{
  min-height:auto !important;
  padding:21px 0 !important;
  border:0 !important;
  border-top:1px solid var(--line) !important;
  border-radius:0 !important;
  background:transparent !important;
  box-shadow:none !important;
}

.guardian-detail .related .card:hover{
  transform:none !important;
  border-color:var(--line) !important;
  opacity:.76;
}

.guardian-detail .related .card small{
  color:var(--gold) !important;
  font-size:10px !important;
  letter-spacing:.15em !important;
  text-transform:uppercase !important;
}

.guardian-detail .related .card strong{
  display:block !important;
  margin-top:9px !important;
  color:var(--text) !important;
  font-size:21px !important;
  line-height:1.1 !important;
  letter-spacing:-.035em !important;
}

.guardian-detail footer{
  width:min(var(--max),calc(100% - 44px)) !important;
  margin:0 auto !important;
}

@media(max-width:760px){
  .guardian-detail .hero{
    grid-template-columns:1fr !important;
    gap:28px !important;
    padding:58px 0 62px !important;
  }

  .guardian-detail .icon-wrap{
    order:-1;
    width:112px !important;
    height:112px !important;
    padding:14px !important;
    border-radius:23px !important;
  }

  .guardian-detail .icon-wrap img{
    width:80px !important;
    max-width:80px !important;
    height:80px !important;
    border-radius:18px !important;
  }

  .guardian-detail .hero h1{
    font-size:44px !important;
  }

  .guardian-detail .hero .ctas{
    flex-direction:column !important;
    align-items:stretch !important;
  }

  .guardian-detail .hero .store-btn,
  .guardian-detail .hero .text-btn{
    width:100% !important;
  }

  .guardian-detail .related .cards,
  .guardian-detail .related .grid{
    grid-template-columns:1fr !important;
  }
}
'''

CSS.write_text(css)

print(f"Fixed {len(detail_pages)} Guardian detail and guide pages.")
print("Homepage was left untouched.")
print("Backup created at guardian.before-detail-page-fix/")
print("Nothing was committed, pushed or deployed.")
print("Refresh any Guardian subpage in your browser.")
