# cascade 축 ② 판독기 + 합치는 규칙 변이 검사 (2026-11-04)

- 대상: tools/cascade/analyze_cathode_reactivity.py 의 `--axis_hyd` (hy_gates · hy_h2s_share · hy_readout) 와 `ax_combine` (합치는 규칙 R1 · R3 · R4)
- `hy_mutate.py` 18 개 · `hy_mutate.log` — 첫 판 17/18 (H19 = 호스트 행 검사 끔 — 시험에 '호스트 행 없음' 경우가 없었다 · G1b 가 대신 막고 있었다)
  → 경우를 보탠 뒤 **18 / 18 빨강**.
- 축 ① 판독기 하네스 (`../cascade_axis_ncm_reader_mutation_2026_11_04/ax_mutate.py`) 는 d6cda752 판 파일에 맞춰져 있다 — 축 ② 코드가 비슷한 줄을 더해
  자리가 둘이 된 5 개 (A13 · A14 · A15 · A21 · A28) 는 그 판에서만 다시 돈다. 대신 새 파일로 축 ① 판독을 다시 내 **결과가 같음** 을 확인했다
  (다른 곳은 G5 의 카드 sha 하나 — 판독 뒤 카드에 판독 절을 더했기 때문).
