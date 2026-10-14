# element_effects demo (2026-10-14)

DEMO on Stage-1 labels (2026-10-14): the labels are flawed (configuration noise, composition-referenced energy, one dopant level, n = 91) — this tests the code, not the chemistry. Not citable.

Made by `tools/cascade/element_effects.py --demo --seed 20261014 --n_boot 200 --n_perm 199`. One JSON + two CSVs per label; `anion_effects_demo.png` = anion effects with 5–95 % bands (configuration bootstrap; interface labels have one value per precursor, so no band).

Inputs (sha256):

- `db/properties/cascade_all_302_2026_08_25.csv` 0d9a839e2dc208d8b020ab73087f068bf91a4c1d6fefa81090b762667f265c30
- `db/properties/cascade_interface_90.jsonl` 4a8476a65268b93dfb640ca1395993c8531c1822aa7c6453cd7674f3f92f11f0
- `db/properties/cascade_interface_li.jsonl` cd1d3bb3809bd88964c192c780f1e92df9c843d032ba9a45e4ab8366e5543a23
- `db/properties/cascade_interface_baseline.jsonl` 47aa81ff74b4ed77a3cb7ea8d73c3e842ae5f1eb0ba8b0a69dfa31dafc41c4a9
- `db/properties/cascade_interface_baseline_closed.jsonl` 7139f3fe284d89495f9ef78d57dce95598ab62bde14ef710821ec258eb04fa42
