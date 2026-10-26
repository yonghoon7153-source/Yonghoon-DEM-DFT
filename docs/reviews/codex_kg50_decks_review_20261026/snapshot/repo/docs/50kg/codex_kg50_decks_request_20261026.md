# Codex 짧은 검토 요청 — 50kg 4차년도 SE 입도 비교 DEM 덱 (10-26)

- 리뷰 핀 = 이 문서를 넣은 커밋 (`claude/sdcp-dem-manuscript-si-pqwtv8`).  발송 = 1저자.
- 계기: 1저자 10-26 — DEM 세션이 토큰 부족으로 검토 못 함 → *"너가 확실하게 해야돼"* · *"아님 codex 리뷰 받아도 되고"* → Q6 *"권고대로"* = Codex 짧은 검토 + 그동안 싼 런 (D3 칸 비교 · 속도 시험) 먼저.
- 런이 길다 (D0.7-40 추정 1.5–3 일 이상) → 며칠짜리 런을 버리게 만들 결함을 런 전에 찾는 것이 목적.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (보아 달라) | 닫지 않는 것 |
|---|---|
| 덱 생성기 `scripts/make_se_size_decks.py` 와 생성 덱 `docs/data/kg50_decks_20261026/` 가 기준 덱 (`docs/data/phase_a_6mah/in.real_4.liggghts`) 에서 정해진 자리만 바꾸는가 (①–⑮) · 그 자리들이 옳은가 | 기준 덱의 물리 (재료 연화 E_SE 1.35 GPa · hooke/hysteresis · gen-1 프로토콜) 자체의 타당성 |
| 며칠짜리 런을 망칠 운영 결함 (삽입 실패 · 상별 수 · 체크포인트 · 재개 · 디스크 · 정수 넘침 · 시드) | 결과 해석 · 7 쪽 그림 (런 뒤) |
| 칸 비교 (40 ↔ 50) 설계 · 판정 기준 (README §5) | 언로딩 (이번 범위 밖 · 1저자) |

## 1. 바꾼 자리 (덱 머리에 같은 목록)

① 조성 단일 활물질 (AM_P 자리 · pts2 정의만) 85 : 15 wt% · ② r_AM 3 µm · r_SE 0.35 / 0.5 / 1.0 / 1.5 µm · ③ 진밀도 `lab20261014` (4.85 / 1.64) · ④ 영역 40 · 50 µm (reg_box · reg_mix · 판 꼭짓점 · 압력 면적 두 곳) · ⑤ 삽입 위끝 = 고체 두께 101.98 µm / volumefraction 0.321 · ⑥ 시드 다섯 (8 자리 소수 · 슬롯별 독립 · ps45 대역 밖) · ⑦ 태그 · ⑧ maxattempt 3,000 (int32: 예상 수 × 3,000 × 1.3 < 2³¹ · 원장 PS-01) · ⑨ `processors * * 1` · ⑩ 삽입 수 99 % 검사 · ⑪ 압축 체크포인트 200,000 · ⑫ atom 덤프 50,000 · ⑬ step 1 체크포인트 + 삽입 전용 덱 (본 덱의 그 줄까지 바이트 그대로 + `run 2000`) · ⑭ 활물질 수 검사 ±0.5 % · ⑮ (속도 시험 덱만) skin.

## 2. Claude 자체 검토 (10-26 · D0.7-40 덱 줄 대조)

문제 없음으로 본 것: 단위 ×1000 · 압력 면적 0.0016 두 자리 · target 0.30 (300 MPa) · 판 속도 0.01 · 밀도 · E (AM 140 · SE 유효 1.35 GPa) · ν · dt 1e-6 (D0.7 SE Rayleigh 시간 ≈ 6.7e-5 s 의 1.5 %) · `shell mkdir` (post · restart) · 판 위치 = 정착 뒤 z_max + r_AM + margin (삽입 높이와 무관) · 시드 소수 · hooke k ∝ R → 같은 압력에서 δ/R 크기 무관.

고친 것 · 정한 것 (1저자 Q1–Q6 · `docs/50kg/dem_plan_20261026.md` §4-2): 삽입 NP 1 + 활물질 수 검사 (SELF-70) · 덤프 · 체크포인트 간격 (디스크) · skin 속도 시험 · D3 칸 비교 시드 3 · D0.7-50 철회 · 시간 추정 3–5 배 정정.

⬜ 독립 에이전트 사전 공격 리뷰 (CLAUDE.md 규칙 ③) = Rint 묶음 B 에이전트가 끝난 뒤 (에이전트 하나씩) — 그 전에 이 요청을 보내면 그 사실을 한정으로 둔다.

## 3. 질문

1. **삽입 · 상별 수 (SELF-70).**  `fix insert/pack` (volumefraction_region · 분포 두 템플릿) 의 랭크별 절삭이 소수 상 (활물질 · 수 0.3 %) 을 체계적으로 부족하게 만든다는 우리 읽기가 맞는가.  NP 1 삽입 → step 1 restart → 다른 NP 로 `read_restart` 하는 길에 부작용이 있는가 (restart 이 정착 전 · 접촉 0 · 메시 없음).
2. **재개 도구.**  `scripts/resume_ckpt.sh` settling 모드가 step 1 restart + 삽입 전용 런 로그 (thermo 1000 · step 1 · 1000 · 2000 · 2001) 로 G1–G3 를 판정할 수 있는가 (G2 = settling 은 G1 KE 로 대신).  ibb `dem_restart.py` 는 리포에 없다.
3. **skin.**  `neigh_modify delay 0 check yes` 에서 skin 2 → 0.5 µm 가 물리 같음 (궤적만 다름) 이라는 판단에 LIGGGHTS 쪽 함정 (mesh 벽 이웃 · 접촉 이력 · 고스트 반경) 이 있는가.
4. **`quit 1` (if 안).**  LIGGGHTS-PUBLIC 3.8 의 `quit` 이 인자를 받는가 — 안 받아도 오류로 멈추면 검사 목적은 같다고 보는데 맞는가.
5. **삽입 성공.**  volumefraction 0.321 · 크기비 8.6 : 1 (AM 3 µm · SE 0.35 µm) · maxattempt 3,000 (템플릿 15,000 에서 낮춤 · int32) 으로 전부 들어가는가 — 99 % 검사가 실패를 잡지만 며칠 전에 알고 싶다.
6. **시간 · 병렬.**  step 수 5–7 M (판 이동 ≈ 50–60 µm ÷ 0.01 mm/s) · 입자당 비용 (skin 이웃 수) · 40×40 을 56 코어로 나눴을 때 칸 5.7×5 µm < 고스트 반경 8 µm 의 효율 판단이 맞는가.
7. **칸 비교 설계.**  D3 40 · 50 각 시드 3 · 네 지표 문턱 (porosity 0.5 %p · coverage 1 %p · tortuosity 5 % · σ_ion 5 %) 으로 D0.7 · D1 · D2 의 영역을 정하는 것이 타당한가 (가장 큰 입자는 활물질로 같다).
8. 그 밖에 며칠짜리 런을 버리게 만들 것.

## 4. 파일

- `scripts/make_se_size_decks.py` (selftest 81/81 · `python3 scripts/make_se_size_decks.py --selftest`)
- `docs/data/kg50_decks_20261026/` (README · manifest.json · 덱 · 러너)
- `docs/50kg/dem_plan_20261026.md` (§4-1 · §4-2 결정)
- 기준 덱 `docs/data/phase_a_6mah/in.real_4.liggghts` · 러너 원형 `docs/data/pure_se_r075_20260927/run_pse_r075_a_r30.sh` · 재개 도구 `scripts/resume_ckpt.sh` · 원장 SELF-70 (`docs/reviews/findings.json`)
