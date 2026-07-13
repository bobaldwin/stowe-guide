# Guide template — how this site is built

`index.html` (the deployed site) is generated from these sources:

- `mobile_a.html` — design tokens/CSS (light + dark), masthead, sticky nav, Welcome, Cycling
- `mobile_b.html` — Hiking, Pickleball & Fitness, Adventures
- `mobile_c.html` — Beer, Restaurants, Hidden Gems & Quick Reference, colophon
- `build_mobile.py` — assembler: substitutes `{{IMG:name}}` (photos → base64 data URIs),
  `{{QR:name}}` (QR codes as inline SVG), `{{AM:key}}` (Apple Maps URLs), `{{PIN}}` (map-pin icon)

## Rebuild

```
python3 -m venv venv && ./venv/bin/pip install qrcode pillow
# put source photos in img/*.jpg (1600px wide is plenty; they get downscaled to 880px)
./venv/bin/python build_mobile.py
```

Outputs a self-contained `index.html` (~1.7 MB) — commit and push to update the live site.

## Conventions for future guides

- Every named place gets a `⌖ Map` pill AND place-QR pointing to `https://maps.apple.com/?q=<place, town, state>` — location beats website.
- Website QRs only for live information (forecast, trail conditions).
- Photos: Wikimedia Commons, correct season, CC-licensed, credited in captions + colophon.
- Single column, ~40rem measure, Charter body + system sans display, one green accent,
  dark mode via CSS custom properties.
