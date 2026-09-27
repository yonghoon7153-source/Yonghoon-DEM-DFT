# Raw sources

| File | Source | License / note |
|------|--------|----------------|
| `japan.topojson` | [dataofjapan/land](https://github.com/dataofjapan/land) — converted from 地球地図日本 (国土地理院, GSI) | Non-commercial use requires attribution: 「出典: 地球地図日本（国土地理院）」. Attribution is shown in the app footer. |
| `prefecturalCapital.csv` | [dataofjapan/land](https://github.com/dataofjapan/land) | Prefectural office coordinates (2014). |

`npm run geo:build` turns `japan.topojson` into the simplified `public/geo/japan.topo.json`
used by the site and `src/generated/prefecture-geo.json` (label anchors / bboxes).
