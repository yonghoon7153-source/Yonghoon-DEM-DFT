# wrdkit

WonATech / Zive `.wrd` 배터리 사이클러 파일을 읽고 분석하는 순수 파이썬 패키지.
numpy 외 의존성이 없고, 웹/DB 계층을 전혀 모른다.

```python
from wrdkit import read_wrd, summarize_cycles, CellSpec, Basis, normalize_capacity

wrd = read_wrd("cell.wrd")
cell = CellSpec(total_mass_mg=31.6, active_wt_percent=80, diameter_mm=13).resolve()

for cycle in summarize_cycles(wrd):
    if not cycle.complete:
        continue
    print(cycle.cycle_number,
          normalize_capacity(cycle.discharge_capacity_mah, cell, Basis.SPECIFIC),
          cycle.coulombic_efficiency)
```

CLI:

```bash
wrdkit info cell.wrd
wrdkit convert cell.wrd --out-dir csv --basis mAh/g --mass 31.6 --wt 80 --diameter 13
```

포맷 스펙은 `docs/raw/specs/wrd-binary-format.md`.
