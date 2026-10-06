# ps45 (r4.5 세대) 다섯 조성 — 활물질 배위수 (AM–SE CN) · PC · SC 따로 (10-07)

- 1저자 WSL 실행 (10-07 새벽) — 웹앱 케이스 다섯 (`docs/data/ps45_r45_network_webapp_20261005/network_5comp.tsv` 의 webapp_case_id) 의 `atoms.csv` · `contacts.csv` 에서 셈.
  규칙 = 웹앱 보고값과 같음 (`scripts/viewer3d_data.py` `CN_CONTACT_RULE` — contacts.csv 행 하나 = 접촉 하나 · δ · 면적으로 거르지 않음 · 접촉 0 입자도 평균에 넣음 · 상 = 케이스 `network_provenance.json` 의 type_map).
- **검산**: SE 배위수 열 = 기존 표 `SE_SE_CN` 4.41 · 4.80 · 5.06 · 5.38 · 5.57 과 같다.
- 결과 (`ps45_AM_coordination.csv` — 1 행 이름 · 2 행 단위): PC (AM_P) 211.80 · 220.31 · 227.39 · 228.95 (3:7 → 10:0) · SC (AM_S) 42.41 · 45.46 · 47.74 · 50.64 (0:10 → 7:3).
  "AM 전체" 열 = 입자 개수 가중 평균 (PC · SC 입자 수 비가 조성마다 달라 그 비율 효과가 섞인다 — 그래프는 PC · SC 따로 권고).
