# 세미나 방향 전환 브리프 (2026-08-11 밤) — Codex 재구성용 재료 목록

사용자 판정 5건 (전부 수용):
1. **SDCP 아웃** — cascade 세미나에 바인더 흡착 서사가 낄 이유 없음. 철회 원장에 딸려
   들어간 것. 필요하면 백업 1장.
2. **self-audit 는 척추가 아니다** — repo 규율로는 맞지만 연단에서 "우리가 철회한 것들"을
   4장씩 말하는 발표는 어색함. **과학(cascade 방법·결과·지식기반)이 척추**, 정직성 장치는
   부록 1~2장으로 축소.
3. **cascade·webapp 내용 증량** — 47종 스크리닝의 실제 내용(축·게이트·테마·개별 도펀트
   프로필)과 webapp 지식기반이 본문의 살이 돼야 함.
4. **형식은 Codex revised 판 느낌** — AI 티(과잉 정돈·슬로건·em-dash) 제거.
5. **레이더(육각형/팔각형) 그림** — 항목별 랭킹이 뻗어 있는 도펀트 프로필.

## 준비된 재료 (전부 repo 등재)

### 신규 (오늘 제작)
- `docs/figures/cascade/cascade_radar_6panel.png` — 8축 팔각형 6종
  (WO₃·CaO·LiF = G4 생존 대표 / B₂O₃ = 축충돌 / Cr₂O₃·HfO₂ = 조합 반쪽).
  축: Oxidation·ESW window·Li pathway·Low blocking·Disorder·Lightweight·Low cost·Soft
  — 전부 47종 내 favorable percentile. **air 축은 의도적으로 제외**(provisional 편향).
- `docs/figures/cascade/cascade_radar_pair_CrHf.png` — Cr₂O₃ vs HfO₂ 겹침
  = 상보성을 그림 한 장으로. 단서 내장("end-member only, pair uncomputed").
- `db/properties/cascade_radar_axes_origin.csv` — 47종 전체 8축 percentile (Origin-ready).
- 생성기: `tools/figures/fig_cascade_radar.py` (도펀트 추가·축 변경 쉬움).
- 문헌 선례: `litdb/figures/duquesnoy2023_.../fig_6.png` — radar 로 다목적 비교 (형식 인용 가능).

### 기존 (검산 완료, 바로 쓸 수 있음)
- 그림: scorecard 47종 히트맵 · oxidation-transport 트레이드오프(6/6) · attrition · pareto
  (`docs/figures/cascade/cascade_seminar_*.png`) + BV percolation path(정본) + ELF 쌍 + Zhu 크롭.
- 수치 골격: 91×3=273 슬롯 → 141행(47×3) 스냅샷 · 게이트 5단 실제 임계
  (0 / 0.05 V / 2.14 V=host / norm 0.3+blocking 0.6 / 로스터 중앙값) · 워터폴 47→43→25→11 ·
  120 순열 불변 · unique-kill 0 · 트레이드오프 6/6 · 시너지 상위 4쌍(+0.36 V, proxy) ·
  ML 0.9998 vs 0.089 (LODO 음수) · 로스터 5족 분류.
- webapp 매핑(스크린샷 후보): `/cascade` 테마 그리드 · `/compare` · `/` coverage matrix ·
  `/elements` 주기율표 · 개별 조성 페이지. **webapp 자체가 "지식이 화면과 동기화된다"는
  본문 소재** — 발표에서 라이브 데모 1분도 가능.
- 대본: 한국어 노트 내장 (final.pptx) + Codex 대본 파일(`codex_closed_2026_08_11/`).

## 남는 논지 (축소판)
"승자 선언이 아니라 **방어 가능한 후보 목록과 그 근거**" — 이 한 줄이면 self-audit 의
값어치가 과학 서사 안에 자연스럽게 들어감. 철회 원장·provenance 는 부록.

## Codex 재구성 시 유의
- SDCP 흔적 제거 대상: 철회 원장 6·7·8행, "철회의 철회" 장, MLIP 한계 ①의 "SDCP" 언급.
- Li_24g 주장은 heuristic 등급 + Hf 양쪽성(P_4b or Li_24g) — 단정 금지 (원천:
  `kb/methodology/dopant_site_preference_literature.md:43,71`).
- x002/x005/x010 = campaign label (concentration=0.25 충돌) 유지.
- 숫자는 위 "검산 완료" 목록만. 새 숫자 도입 시 원자료 경로 필수.
