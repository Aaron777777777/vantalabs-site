#!/usr/bin/env python3
from pathlib import Path
import sys
if len(sys.argv) != 3:
    raise SystemExit('Usage: python3 guardian/set-store-links.py APP_STORE_URL GOOGLE_PLAY_URL')
p=Path('guardian/assets/app-links.js')
s=p.read_text().replace('__GUARDIAN_IOS_URL__',sys.argv[1]).replace('__GUARDIAN_ANDROID_URL__',sys.argv[2])
p.write_text(s)
print('Guardian App Store and Google Play links are now active on every page.')
