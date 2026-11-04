# cascade 축 ③ 판독기 + 세 축 합치기 변이 검사 (2026-11-04)

- 대상: tools/cascade/analyze_cathode_reactivity.py 의 `--axis_li` (li_product_class · li_gates · li_readout · li_full_reduction) 와
  `ax_combine(ncm, hyd, li)` 의 축 ③ 부분 (위험 표시 F1_Li · F2_Li · 모름 · G4 · G7 · 막는 게이트).
- `li_mutate.py` 24 개 · `li_mutate.log` — 첫 판 23/24 (L22 = R5 짝의 등급 비교 끔 — Sn 짝의 δ 차가 25 로 커서 등급을 안 봐도 '다름' 이었다)
  → Sn 짝을 δ 차 5 · 등급 다름으로 바꾼 뒤 **24 / 24 빨강**.
- 회수 전 커밋 (카드 §8 ②) · 결과 0 건.
- 축 ① · ② 판독 재현: 고친 판독기로 `cascade_axis_ncm_v2_2026_11_04` · `cascade_axis_hyd_2026_11_04` 를 다시 읽어 봉인된 판독
  (`cascade_axis_ncm_readout_2026_11_04.json` · `cascade_axis_hyd_readout_2026_11_04.json`) 과 **같음** (run_dir · G5 카드 sha 제외).
- 축 ② 하네스 (`../cascade_axis_hyd_reader_mutation_2026_11_04/hy_mutate.py`) 의 H18 (도구 sha 검사 끔) 은 축 ③ 이 같은 줄을 더해 자리가 둘이 됐다 —
  그 하네스는 축 ② 판 파일 (d22bb622) 에서만 다시 돈다 (축 ① 하네스가 축 ② 뒤 그랬던 것과 같다).
