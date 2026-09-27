# Raw sources

| File | Source | License / note |
|------|--------|----------------|
| `japan.topojson` | [dataofjapan/land](https://github.com/dataofjapan/land) — converted from 地球地図日本 (国土地理院, GSI) | Non-commercial use requires attribution: 「出典: 地球地図日本（国土地理院）」. Attribution is shown in the app footer. |
| `prefecturalCapital.csv` | [dataofjapan/land](https://github.com/dataofjapan/land) | Prefectural office coordinates (2014). |
| `canva-text.json` | my Canva mind-map PDF (1 page, 1440×810 pt) | Every line of text with its position, size and colour — the input of `nihon audit`. |
| `canva-audit.json` | — | PDF lines that are knowingly not in the data, each with a reason (`fixed` = fixed with my OK, `pending` = waiting for my answer). |

`npm run geo:build` turns `japan.topojson` into the simplified `public/geo/japan.topo.json`
used by the site and `src/generated/prefecture-geo.json` (label anchors / bboxes).

`nihon audit` (also part of `nihon check`) proves that every line of `canva-text.json` is somewhere in `data/`:
names may repeat freely, but note text is used up — if the PDF says 「高い」 four times, the data needs four.
