# Raw sources

| File | Source | License / note |
|------|--------|----------------|
| `japan.topojson` | [dataofjapan/land](https://github.com/dataofjapan/land) — converted from 地球地図日本 (国土地理院, GSI) | Non-commercial use requires attribution: 「出典: 地球地図日本（国土地理院）」. Attribution is shown in the app footer. |
| `prefecturalCapital.csv` | [dataofjapan/land](https://github.com/dataofjapan/land) | Prefectural office coordinates (2014). |
| `tokyo23.geojson` | [dataofjapan/land](https://github.com/dataofjapan/land) `tokyo.geojson` — 地球地図日本 (国土地理院, GSI) | Only the 23 wards (都区部), property `ja` = ward name, coordinates rounded to 1e-5°. Same terms as `japan.topojson` (attribution). `nihon geo` turns it into `public/geo/tokyo23.topo.json` for the 23区 popup. |
| `lakes.geojson` | [Natural Earth](https://www.naturalearthdata.com/) 10m lakes (`ne_10m_lakes`), Biwa only | Public domain. Coordinates rounded to 1e-4°. `nihon geo` adds it to `public/geo/japan.topo.json` as `objects.lakes`. |
| `city-areas.geojson` | [smartnews-smri/japan-topography](https://github.com/smartnews-smri/japan-topography) `N03-21_210101` municipalities + `_designated_city` (1% simplified) — 国土交通省 国土数値情報（行政区域） | 「国土数値情報（行政区域データ）（国土交通省）を加工して作成」 credit required (shown in the app footer). Every city with a dot in `places.json` (68: `kind` = `designated` 20 with wards merged, `city` 48; 江の島 is not a municipality; 津軽市 = つがる市), `code` = JIS code, coordinates rounded to 1e-4°. `nihon geo` → `objects.cities` of `japan.topo.json`, 那覇市 shifted into the Okinawa inset there. |
| `canva-text.json` | my Canva mind-map PDF (1 page, 1440×810 pt) | Every line of text with its position, size and colour — the input of `nihon audit`. |
| `canva-audit.json` | — | PDF lines that are knowingly not in the data, each with a reason (`fixed` = fixed with my OK, `pending` = waiting for my answer). |

`npm run geo:build` turns `japan.topojson` into the simplified `public/geo/japan.topo.json`
used by the site and `src/generated/prefecture-geo.json` (label anchors / bboxes).

`nihon audit` (also part of `nihon check`) proves that every line of `canva-text.json` is somewhere in `data/`:
names may repeat freely, but note text is used up — if the PDF says 「高い」 four times, the data needs four.
