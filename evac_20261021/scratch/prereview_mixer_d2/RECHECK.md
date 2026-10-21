# 재확인 — 믹서 D2 수정 (MXD2-01–06) · 수정 diff `055ddd04e..9412f384a`

**결론 (한 줄): ⏳**

---

## 0. 범위 · 입력 · 방법

| 항목 | 내용 |
|---|---|
| 작업 트리 | `git reset --hard 9412f384a` (fetch 없음) · 끝까지 `git status` 깨끗 (리포에 쓴 것 없음 · pycache 없음) |
| 기반 | `055ddd04e` = 내 리뷰 판 `a76f59d0d` + **9 커밋** (지시문의 "원장 커밋 둘" 보다 많다) — 그러나 `scripts/` · `dem_scripts/` 차이는 `check_all.sh` 한 줄뿐 = 믹서 코드는 리뷰 판과 같다 |
| 수정 | `fd76cc11c` (시험 먼저) · `b6cdfc7e4` (생성기 + devlog v1.6) · `9412f384a` (되읽기 · 덱 비교 · 스모크 · 접촉 판독기 · 런처) — 9 파일 +1657 / −135 |
| 범위 밖 | MXD2-07 (D3 문서 숫자 · D3 설계 v2 몫) |
| 방법 | 첫 리뷰 탐침을 고친 코드에 다시 (고친 생성기 사본 `gen/mmd_FIX.py` md5 `d4a3d074…` · 옛 판 `gen/mmd_HEAD.py` = `a76f59d0d` md5 `829a1a15…` · 시험 먼저 판 = `git archive fd76cc11c` 스냅숏) · 변이 (생성기 50 · 도구 42 · 런처 4) · 같은 부류 탐침 · 정상 덱 거짓 거부 그물 · 고친 사람 증거 (`mxd2fix/`) 는 참고만 |
| 규칙 | 60 s 넘는 실행 = `heavy.sh` · python `-I -B` · `PYTHONDONTWRITEBYTECODE=1` · push · fetch · check_all 안 함 |

## 1. 항목별 판정

| ID | 원 반례 (첫 리뷰) | 지금 (9412f384a) | 판정 |
|---|---|---|---|
| MXD2-01 (P2) | (a) lab D2 · LC lab 표 E 되읽기 rc 1 (gen1 밀도만) · (b) 같은 ρ 세계 비코팅 ↔ 코팅 짝을 인증할 표 · 허용목록 없음 (A · B · U · E · EB 전부 rc 1) · (c) 스모크 계획 수 gen1 · 셀 이름 문법 없음 | (a) 표 E LC lab · GMuu lab soft → ×20 **PASS** (gen1 도 PASS) · (b) 되읽기 표 GM · `--allow GM` 둘 다 uu→cc · uu→cu · uu→uc · cu→cc · cc→uu · gen1 uu→cc **PASS** · CGF 100 · 200 · 123.456 PASS · 같은 짝에 A · B · U · E · EB 는 **FAIL (옳은 사유)** · 다른 ρ 세계 · 다른 Bo · 다른 세대 · 같은 표면 · 다른 강성 · 명시 벽 ↔ NCM 벽 · 옛 팔 → **FAIL (사유 맞음)** · `--expect-deck` 틀린 목표 FAIL · (c) 스모크 계획 수 = 셀 세대 (⑨c · lab 143/699/99,158) · 셀 이름 → `d2_cli_args` → 생성기 → 셀 계약 문제 0 · `--runs --allow GM` 1/1 PASS · 메타 없는 D2 셀 거부 | **닫힘** (원 반례) — 같은 부류 잔여 = PRE-MIXD2R-01 · 05 |
| MXD2-02 (P2) | M04 (F₀_SS 에 gen1 ρ_SE) · M05 (덱 경로 밀도 안 넘김) · M16 (meta bo_se 상수) 가 생성기 시험 143/143 통과 · 그 덱이 diff `--allow E` 1/1 PASS | 생성기 시험: ⏳ · 하류: M04 · M05 변이 생성기 덱 → 되읽기 표 E **FAIL** ("절대 수준 Bo_SE … ≠ 머리 선언") · diff `--allow E` **FAIL** (d2_rule Bo) · 표 GM · `--allow GM` 도 FAIL · M16 덱 → 되읽기 FAIL (메타 결합) · `--runs` 셀 계약 FAIL · ⚠ 두 덱 모드 diff 는 메타를 안 읽어 M16 덱 PASS (설계상 "덱만" — 한정어) | **닫힘** (원 반례) — 같은 부류 잔여 = PRE-MIXD2R-02 |
| MXD2-03 (P3) | M06 (혼합쌍 천장 건너뜀) 생존 · γ_AM 10 · Bo 800 에서 AM_P–SE 1.418 % 덱을 씀 | 생성기 시험: ⏳ (MX③ 이 겨냥) · 하류: M06 변이 덱 → 되읽기 표 E **FAIL** ("AM_P–SE 겹침 δ0/min r 1.4176 % > 천장 1 %") · diff `--allow E` FAIL · 고친 생성기는 그 입력을 거부 · Bo 300 은 수용 (δ0 ≤ 0.74 %) | **닫힘** |
| MXD2-04 (P3) | γ 1e-200 · Bo 1e-310 수용 · `AM_P=0_3` → 3.0 · `register_arm('GM\n')` 통과 | 범위 밖 거부 (γ · ρ · γ_W [1e-6, 1e6] · Bo [1e-6, 1e4] · 사유 낱말) · 사후 단언 (CED 정규 양수) · 이름 fullmatch (줄바꿈 · CR · 탭 · NUL · 끝 공백 거부) · 설명 제어 문자 거부 · `--gm-*` 값 `0_3` · `０.３` · `nan` · `+0.3` 거부 (rc 2) · 경계 수용 (ρ 1e6 + Bo 1e-6 · ρ 4e-5 · Bo `.5` `5.` `3E-1`) | **닫힘** (리뷰가 요구한 `--gm-*` 범위) — 커밋 주장 문장은 더 넓다 = PRE-MIXD2R-03 |
| MXD2-05 (P3) | Q2 (벽 = 비코팅 NCM) 미강제 · ρ ↔ γ 어긋남 수용 · 도움말 · 주석이 열린 질문 | 라이브러리 강제: `--gm-wall-ncm ρ` 면 γ_W = 0.0256·ρ 정확 · NCM γ ∈ {1, ρ} · 명시 벽은 NCM γ 전부 1 · 리뷰 F4 셋 + 리뷰 덱 둘 거부 (사유 "Q2") · 도움말 · 주석 정정 (도움말에 "0.0256·ρ 여부" 없음) | **닫힘** |
| MXD2-06 (P3) | D2 덱의 옛 벽 주석 (÷ 1.842) · registered / schema 옛 값 · devlog `--dens-gen` 누락 · M13 · M15 · M18 생존 | D2 덱 옛 벽 주석 0 (옛 팔 LC 는 그대로 1) · registered = "D2 … 결과 전 등록 없음" (+ 강성 경로 문구) · schema /2 · 머리 벽 줄 · 표면 · 삽입 줄 · devlog v1.6 정정 줄 · 변이: ⏳ | ⏳ |

## 2. 고친 사람 주장 대조 (커밋 메시지 · devlog)

| 주장 | 내 재현 | 판정 |
|---|---|---|
| 기본 경로 바이트 같음 — 라이브러리 342/342 (21 양쪽 거부) · CLI 14/14 (70 파일) · 옛 HEAD · D2 전 판 둘 다 | `probe_byteident_fix.py`: preD2 ↔ FIX **342/342 · 거부 21 · CLI 14/14 · 70 파일** · HEAD(a76f59d0d) ↔ FIX 같은 수 | 맞음 |
| 리뷰의 D2 덱 9 = 주석 · deck_meta (adhesion_rule · registered · schema) 만 바뀜 · 주석 밖 명령 토큰 · pairs 표 같음 · 둘은 Q2 거부 | `probe_regen9.py`: 7 덱 주석 밖 토큰 같음 · pairs 같음 · 메타 차이 = adhesion_rule.{layered, surface} (+ 명시 벽 덱 rho_world · wall_rule) · registered · schema · 2 덱 rc 1 (사유 Q2: "명시 벽은 NCM γ 전부 1 인 팔만" · "ρ 0.3 세계 NCM γ 는 1 또는 ρ 만 {AM_S 0.5}") | 맞음 |
| 생성기 시험 147/154 → 154/154 | 뒤 **154/154** (내 실행) · 앞 (fd76cc11c) ⏳ | ⏳ |
| 변이 32/32 죽음 (리뷰 24 + 새 가드 8) | ⏳ (내 판 = 리뷰 24 + 새 가드 26) | ⏳ |
| 되읽기 24/31 → 31/31 · diff 55/61 → 61/61 · 스모크 30/31 → 31/31 · 접촉 판독기 30/31 → 31/31 · test_launcher 136/138 → 138/138 | 뒤: **31/31 · 61/61 · 31/31 · 31/31 · 138/0** (내 실행) · 앞 ⏳ | ⏳ |
| 되읽기 480 D2 덱 거짓 문제 0 · 법칙 / Bo / 머리 편차 = 한계의 61 / 58 / 50 % | ⏳ (`probe_falsereject.py`) | ⏳ |
| "deck_meta.json next to the deck is bound" | in.mixer 옆 메타만 — 이름 다른 덱 · deck_file 다른 메타 · 메타 없음 = 결합 없이 PASS | **부분** → PRE-MIXD2R-02 |
| "CLI numeric tokens ASCII decimal only ('0_3', full-width digits, nan, inf refused)" (b6cdfc7e4) · devlog "수 토큰 = ASCII 십진수만" | `--gm-*` 넷만 참 — `--stiffen-se 2_0` → 20 · `--stiffen-se ２０` → 20 · `--dt-factor ０.５` → 0.5 (D2 덱 씀) · `--cgf 15_1.4` → 151.4 수용 | **넓음** → PRE-MIXD2R-03 |
| D2 셀은 run_all.sh · resume_all.sh 가 띄우지 · 잇지 않는다 (이름 또는 D2 머리) | 이름 가드 = test_launcher D2① · 머리 가드 = 내 탐침 (진짜 D2 덱을 `X_s32452843` 아래 → 두 런처 다 건너뜀 · 옛 팔 덱 대조군은 뜸) · launch_highbo.sh = 등록 코호트만 (D2 없음) | 맞음 — 머리 가드는 시험 밖 = PRE-MIXD2R-04 |
| 가져다 쓰는 도구 무변경 · 통과 (check_contact_validity 89/89 · measure_mixing_index 40/40 · mixer_exact_frames 31/31 · mixer_restart_phase_test 35/35 · mixer_stage_gate 14/14 · make_mixer_resume · mixer_gate_reader_diff) | ⏳ | ⏳ |

## 3. 새 결함 (PRE-MIXD2R-NN)

| ID | 등급 | 자리 | 반례 입력 → 기대 → 실제 | 최소 해결 |
|---|---|---|---|---|
| **PRE-MIXD2R-01** | P3 (등록 전 필수) | `scripts/mixer_smoke_blind.py:70` `REG r_container=0.013138` → `run_contract_cert:317` · `run_blind:154` `mi.analyse(…, reg['r_container'], …)` · `scripts/mixer_stage_gate.py:80-81` `REG_R_CONTAINER` · `READER_REG` · `_e0_of:530` (E0 이름에 세대 없음) | lab 계획 드럼 R = **0.0125832** m (gen1 0.0131377 · **−4.2 %**) · 수정은 스모크의 **상별 수만** 셀 세대로 바꿨다 (⑨c) — `--contract <GMuu_rho0p3_bo0p5_lab20261014_ref_r2_s…> --ref … --cert …` 는 D2 이름을 받고 (parse_cell) 상별 수는 lab 143 · 699 · 99,158 로 맞추면서 판독 칸은 **gen1 R** 로 짠다 (`measure_mixing_index.cell_stats:131-133` 의 (a+R)/(2R)·16 → 단면 칸 정사각이 드럼보다 4.4 % 넓다) → 기대 = 셀 세대의 R (또는 거부) · 실제 = gen1 격자의 판독이 봉인 · 기술 판정에 남는다 · 지금은 D2 · lab 셀을 띄우는 런처가 없어 (런처 가드 · 코호트 없음) 손 CLI 로만 도달 · 실데이터 없음 · devlog 10-21 "스모크가 lab 세대 … 다시 검산" 은 이 범위보다 넓다 | 셀 세대의 계획 R (`_gen.plan(…, dens_gen=…)['R']`) 을 판독 · 관문 r_container 로 쓰고 증서에 기록 — 또는 등록 (정책 v5) 전까지 non-gen1 셀을 판독 경로에서 거부 (fail-closed) · devlog 문장을 "계획 상별 수 · 기대 덱" 으로 |
| **PRE-MIXD2R-02** | P3 | `scripts/mixer_deck_readback.py:929-941` `_load_meta` (메타의 `deck_file` ≠ 덱 파일 이름 → None) · `:445-447` `_meta_problems` (`m is None → []`) | ① GMcc 셀 deck_meta.json 에 `adhesion_rule.bo_se 0.21244` (M16 꼴 · 덱 머리 0.5) + `deck_file "other.mixer"` → `--table GM uu cc` **rc 0 PASS** (deck_file 그대로면 rc 1 "adhesion_rule.bo_se 0.21244 ≠ 덱 머리 … 0.5") · ② 같은 변조 메타 · 메타는 그대로 두고 **덱만 같은 폴더에 `cc.mixer` 로 복사**해 비교 → **rc 0 PASS** (화면엔 결합 여부가 없고 JSON `meta_bound: false` 만) · ③ D2 in.mixer 옆 메타를 지우면 PASS → 기대: D2 덱의 결합 누락은 검사 행 (FAIL 또는 명시 경고) · 실제: 조용히 생략 · 영향 한정: 생성기는 늘 deck_file `in.mixer` 를 쓰므로 생성기 결함 (M16) 은 in.mixer 에서 잡히고 (MX⑥) `--runs` 셀 계약은 따로 결합한다 (① 도 거부) — 덱을 다른 이름으로 모아 비교하는 흔한 사용 (요청서 묶음 등) 에서 결합이 빠진다 · 9412f384a 메시지 "deck_meta.json next to the deck is bound" 보다 좁다 | D2 덱이면 "메타 결합" 을 표의 검사 행으로 (같은 폴더에 메타가 있는데 이름이 안 맞음 = FAIL · in.mixer D2 + 메타 없음 = FAIL 또는 경고 행) · 문장을 "in.mixer (또는 meta.deck_file 이 가리키는 이름)" 으로 |
| **PRE-MIXD2R-03** | P3 (주장 범위 · 같은 부류) | `scripts/make_mixer_deck.py:3227` `--stiffen-se type=float` · `:3234` `--dt-factor type=float` · `:3193` `--cgf type=float` (그 밖 `--fr` · `--rpm` · `--settle-s` · `--baffle-h`) · 커밋 `b6cdfc7e4` 메시지 "CLI numeric tokens ASCII decimal only ('0_3', full-width digits, nan, inf refused)" · devlog v1.6 10-21 "수 토큰 = ASCII 십진수만" | D2 덱: `--gm-gamma AM_P=0.3,AM_S=0.3 --gm-wall-ncm 0.3 --gm-bo-se 0.5 --dens-gen lab20261014 --stiffen-se 2_0 --hold-bo-pairwise` → rc 0 · ×**20** 덱 (meta stiffen_se 20.0 · argv `2_0`) — `2.0` 을 뜻한 오타면 10 배 · `--stiffen-se ２０` → 20 · `--dt-factor ０.５` → 0.5 (D2 덱 씀) · `--cgf 15_1.4` → 151.4 (nan · inf 는 값 검사로 거부) → 원 리뷰 최소 해결 (`--gm-*` 값) 은 채웠다 — 문장이 넓고, D2 덱에 들어가는 강성 · dt · CGF 값이 같은 부류로 남았다 | 문장을 "`--gm-*` 값" 으로 좁히거나 D2 덱에 들어가는 float 옵션에도 `_ascii_float_arg` (ASCII 토큰은 값이 같아 기본 경로 바이트 무영향 · 이상한 토큰만 거부) |
| **PRE-MIXD2R-04** | P3 (시험 공백) | `dem_scripts/mixer_20260921/test_launcher.sh` D2① · D2② | D2① 은 **가짜 proto 덱**을 GM 이름 아래 둔다 → 이름 가드만 시험 · 머리 grep 가지 (`grep -qF '★ D2 결합 규칙 (기하평균'` — 중립 이름 아래 진짜 D2 덱) 는 시험 밖 · 내 탐침: 진짜 생성기 D2 덱을 `X_s32452843` 아래 → run_all.sh "D2 결합 규칙 셀 건너뜀" · resume_all.sh "재개 없음 … 건너뜀" (가드 자체는 동작 · 옛 팔 덱 대조군 `Y_s32452843` 은 뜸) · 변이 ⏳ (L1 · L3 = grep 가지 삭제) | D2③: 진짜 D2 덱 (생성기 CLI) 을 중립 이름 아래 두고 두 런처가 건너뛰는지 · 옛 팔 덱은 뜨는지 |
| **PRE-MIXD2R-05** | P3 (낮음) | `scripts/mixer_deck_diff.py:312-331` `_diff_decks_GM` (`changed` = 인쇄 값 REL_TOL 1e-6 · `expected` = e≠1 · `missing = expected − changed`) · `:742-764` 셀 문법 | ① ρ **1.00001** 세계 (Q2 안 · 생성기 수용) uu → cc: 되읽기 표 GM **PASS** · diff `--allow GM` **FAIL** "개입 누락 AM_P–SE · AM_S–SE" (배수 ρ^(−1/6) = 1 − 1.7e-6 가 6 자리 인쇄 · REL_TOL 아래) — 같은 정상 짝에 두 도구가 다른 판정 (ρ 1.0001 은 둘 다 PASS) · 셀 문법은 `rho1p00001` 을 받는다 · ② 문법은 생성기가 거부하는 이름도 받는다 — `GMuu_rho0p00001_…` (γ_W 2.56e-7 < 1e-6) · `…_bo10000_…` (천장) → `cell_expected_deck` · `cell_deck_problems` 가 **SystemExit** (ValueError 아님 · `--runs` 는 rc 1 로 끝남 = fail-closed) | diff GM: \|e−1\| 이 인쇄 분해능 (≈1e-5) 아래인 원소는 "바뀜 · 안 바뀜" 둘 다 허용하고 배수 허용폭으로만 (되읽기와 같은 규칙) — 또는 문법에서 \|ρ−1\| < 1e-4 거부 · 문법 범위에 γ_W = 0.0256ρ · 천장 사전 확인 |

## 4. 변이 시험

⏳

## 5. 확인했지만 결함 아님

- **⑥ 리뷰 덱 둘의 Q2 거부 = 설계와 맞다.**  1저자 10-14 Q2 (`docs/mixer_d2_wall_gamma_derivation_20261014.md` §5 ✅ 줄): *"벽 = 비코팅 NCM 에 묶는다 — γ_W/γ_SE = 0.0256 × ρ_비코팅 · 같은 ρ 세계의 코팅 · 비코팅 팔은 같은 벽"* · 파이프라인 D2 (가) (`docs/mixer_paper_pipeline_draft_20261013.md` D2 행): *"비코팅 = γ_A/γ_S 한 노브 · 코팅 = 비 1"*.  `mixed_03_05_w0256_lab_ref20` (AM 0.3/0.5 + 명시 벽 0.0256) = 비코팅 NCM 이 있는데 벽이 그 ρ 에 안 묶임 · `mixed_ref20_dthalf_fullprec` (ρ 0.3 세계에 AM_S 0.5) = 비코팅 값이 둘 (노브 하나 위반).  Q2 안 대체 덱 (uu · cu · uc · cc · 명시 벽 cc) 은 전부 생성 · 되읽기 PASS.  ⚠ 단 poly · 단결정 NCM 의 비코팅 γ 를 따로 두는 설계가 필요해지면 새 결정이 든다 (지금은 사유를 내고 거부 — 조용히 막지 않는다).
- **옛 판 (a76f59d0d) 이 만든 D2 덱은 새 되읽기에서 거부** ("NCM 표면 · 삽입 줄 0 개" · schema /1) = fail-closed · D2 런은 띄운 적이 없어 영향 없음.
- **명시 벽 cc (γ_W 0.00768) ↔ NCM 벽 uu (ρ 0.3) 짝은 표 GM · `--allow GM` 둘 다 거부** (벽 규칙 다름) — 수치가 같아도 규칙 표지가 다르면 비교 안 함 = 보수적 · `d2_cli_args` 는 늘 `--gm-wall-ncm` 이라 등록 셀 짝은 걸리지 않는다.
- ρ 1e-6 · 3e-5 거부의 사유 = 파생 γ_W (0.0256ρ) 범위 (메시지가 γ_W 를 짚는다) — 실효 ρ 하한 = 1e-6/0.0256 ≈ 3.9e-5 (문서 범위 [1e-6, 1e6] 는 ρ 단독) · 물리 범위 (γ 비 O(10⁻²–10²)) 밖이라 영향 없음.
- `--gm-*` 값 앞뒤 유니코드 공백 (NBSP · EM SPACE) 은 `str.strip` 으로 수용 — 값 같음 (무해 · 밑줄 · 전각 · 부호는 거부).
- `--allow U` / 표 U 로 같은 D2 팔의 Bo 만 다른 짝 (0.5 → 5) PASS — 균일 F₀ 배율 = Bo 배율이라 뜻이 맞다.
- 커밋된 DEV 덱 (`docs/data/mixer_highbo_dev_decks_20260930_v26` · `_20261005_u`) 에 고친 되읽기 6 표 (U ×3 · B · E0 · DT) · diff B · U · `--cohort dev-rot` PASS (dev-e0 는 NP 프로브 폴더가 커밋에 없어 FAIL — 고친 것과 무관) = 기본 경로 소비자 거짓 거부 없음.
- 런처 머리 grep 문자열 (`★ D2 결합 규칙 (기하평균`) 은 커밋된 어떤 in.mixer 에도 없다 (`docs/data` 0 · `dem_scripts` 는 런처 둘뿐) → 옛 덱을 막지 않는다.
- 독립 되읽기 (내 파서 · 리포 도구 없이 · 정확 SJKR 당김힘): 고친 생성기 D2 덱 14 (리뷰 7 + Q2 안 새 7 — cu · uc · gen1 ×40 dt/2 · 명시 벽 cc · ρ 10 Bo 300 · ρ 1e6 Bo 1e-6 · Bo 1010) 법칙 편차 ≤ **2.5e-5** · Bo ≤ **1.3e-5** · 머리 표 ≤ **2.4e-5** · δ0 ≤ **0.9964 %** · 당김힘 비 ≤ 3.3e-3 (δ0 ~1 % 의 유한 겹침 2 차 항 · 첫 리뷰와 같은 크기).
- 다른 CGF (100 · 200 · 123.456) 의 lab D2 uu → cc: 되읽기 GM · diff GM PASS.
- 범위 밖 (기존 · D2 무관): 덱 명령의 수 토큰은 두 도구 모두 `float()` 로 읽어 `1_0` 같은 토큰을 받는다 — 생성기는 그런 토큰을 쓰지 않는다 (손으로 고친 덱만).

## 6. 못 본 것 · 이유

- LIGGGHTS 실행 (금지) — D2 덱의 실제 동역학 · 메시 area_ratio.
- `webapp/test_mixer_devlog_page.py` — 봉인 `webapp/app.py` 를 import 해 폴더를 만들 수 있어 안 돌림 (메인 게이트 몫) · devlog 문구는 읽기로만 확인.
- `launch_highbo.sh` 의 SLURM 경로는 정적 읽기만 — 새 단계는 등록 코호트 (`--cohort`) 관문을 거치고 D2 셀은 코호트에 없다는 데까지.
- 원장: MXD2-01–06 은 아직 `open` · `claimed_fixed_sha` 없음 · `evidence_tests` 는 생성기 셀프테스트만 (되읽기 · 덱 비교 · 스모크 · 접촉 판독기 · 런처 시험은 아직 안 적힘) — 반입 · 원장 갱신은 수정자 몫이라 확인만.
- MXD2-07 (D3 문서) — 범위 밖.

## 7. 산출 · 재실행 (모두 이 폴더 · 리포에 쓰지 않음)

| 탐침 | 내용 | 결과 |
|---|---|---|
| `probe_byteident_fix.py` (`run_byteident_fix.sh`) | 기본 경로 바이트 — preD2 ↔ FIX · HEAD ↔ FIX | `probe_byteident_fix_preD2.json` · `probe_byteident_fix_HEAD.json` |
| `probe_regen9.py` | 리뷰 D2 덱 9 재생성 (옛 ↔ 고친 생성기) + Q2 안 새 덱 9 · 독립 되읽기 | `probe_regen9.json` · `.log` |
| `probe_recheck_tools.py` `<W> decks · rb · df · mut · runs · edge` | 고친 되읽기 · 덱 비교 (두 덱 · `--runs` · 셀 이름) · 변이 생성기 덱의 하류 · CLI 수 토큰 · 문법 | `probe_recheck_tools.json` · `decks/recheck/` |
| `probe_launcher_grep.sh` · `probe_launcher_grep2.sh` | 진짜 D2 덱을 중립 이름 아래 — run_all.sh · resume_all.sh | `launcher_probe*/` |
| `probe_meta_rename.sh` · `probe_grammar_runs.sh` · `probe_cgf.sh` · `probe_committed_decks.sh` | 메타 결합 (이름 바꾼 덱) · 문법 밖 이름 `--runs` · 다른 CGF · 커밋된 DEV 덱 | `meta_rename/` · `grammar_runs/` · `decks/cgf/` · `committed_*.out` |
| `run_selftests_fix.sh` · `run_selftests_root.sh <snap_fd76>` | 셀프테스트 뒤 (9412f384a) · 앞 (fd76cc11c 스냅숏) | `selftests_fix/` · `selftests_fd76/` |
| `probe_mutations_fix.py` | 생성기 변이 50 (리뷰 24 + 새 가드 26) | `probe_mutations_fix.json` |
| `probe_tool_mutations.py <W> rb df cr sm` | 되읽기 25 · 덱 비교 14 · 접촉 판독기 2 · 스모크 1 | `probe_tool_mutations_rb_df_cr_sm.json` |
| `probe_launcher_mutations.py` | 런처 가드 4 (이름 · 머리 grep × run_all · resume_all) | `probe_launcher_mutations.json` |
| `probe_falsereject.py` | 정상 D2 덱 그물 (세대 2 × 강성 3 × ρ 13 × Bo 13 × 표면 5) 거짓 거부 · 허용폭 사용률 | `probe_falsereject.json` |
| `run_importers.sh` | 가져다 쓰는 도구 셀프테스트 7 | `selftests_importers/` |

```
P=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519      # 9412f384a
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/heavy.sh
bash $H bash $P/run_byteident_fix.sh
bash $H bash $P/run_py.sh probe_regen9.py
for s in decks rb df mut runs edge; do bash $P/run_py.sh probe_recheck_tools.py $W $s; done
bash $H bash $P/run_selftests_fix.sh ; bash $H bash $P/run_selftests_root.sh $P/snap_fd76 $P/selftests_fd76
bash $H bash $P/run_py.sh probe_mutations_fix.py $W ; bash $H bash $P/run_py.sh probe_tool_mutations.py $W rb df cr sm
bash $H bash $P/run_py.sh probe_launcher_mutations.py $W ; bash $H bash $P/run_py.sh probe_falsereject.py $W ; bash $H bash $P/run_importers.sh
```
