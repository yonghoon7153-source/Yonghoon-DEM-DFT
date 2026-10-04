# LHS 감사 묶음 ④ — real_14 실측 (10-04 · J20-s)

`real14_audit.json` = `scripts/lhs_stress_constriction_audit.py` 의 출력 (리포만으로 재현 — 입력은 `docs/data/real14_reference_20260928/` 의 덤프).

```
python3 scripts/lhs_stress_constriction_audit.py --selftest                      # 9/9
python3 scripts/lhs_stress_constriction_audit.py --prepare-network OUT           # atoms.csv · contacts.csv · mesh_info.json
python3 scripts/network_conductivity.py OUT/atoms.csv OUT/contacts.csv -o OUT -t 1:AM_P,2:AM_S,3:SE -s 1000 --contact-mode both --dump-raw-dir OUT/raw
python3 scripts/lhs_stress_constriction_audit.py --network-dir OUT --json OUT/audit.json   # = real14_audit.json (10-04 대조: 같음)
```

- `stress` — 웹앱 정의 (대각 성분 VM · 상 평균 / 전체 평균 · CV) 를 두 규약으로: `webapp_50_50` (= LIGGGHTS `stress/atom` ÷ 부피 · 접촉 virial 50/50 분할 —
  재현 중앙 비 1.000000) · `love_weber_branch` (입자 중심 → 접촉점).  벽 · 판 접촉은 둘 다 없다 (`fix wall/gran` virial 없음 · 접촉 덤프에도 없음).
- `constriction` — `bulk_resistance_fraction` (접촉별 R_bulk/R_total 비가중 평균 · 원장 `L2-08`) ↔ 같은 망 해의 I²R 가중 협착 몫 (관통 간선).
- 판정 · 권고는 `docs/reviews/lhs_handover_judgments_20260924.md` J20-s.
- ④b 생산 (10-04 · 비준 뒤): `dem_analysis_core.calc_love_weber_stress` — 같은 덤프로 `scripts/test_love_weber_stress.py` L12 가 매번 다시 잰다
  (대각 σ_LW = 이 감사기 `per_particle_virials` 와 입자마다 상대 차 < 1e-9 · 전체 텐서 값 · 벽 제외 · 벽 비율 표 = J20-s ④b 구현 절).
