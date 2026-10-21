# Rint ② 2 일 차 Z2 — R 런 사슬 (보정 사다리 · holdout 예측 · 판정) · 시험 먼저 · 작업 트리 · push 안 함

## 기반
- 너의 작업 트리에서 `git reset --hard d9404ccb2` (메인 끝 = S0 · 지문 + B6 payload · 러너 · 판정기 · 웹앱 표지) → `git log --oneline -3`.  `git fetch` 하지 않는다.
- **정본 (먼저 다 읽는다)**: 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3 (보정 절차 3-1 – 3-5) · §4 (holdout 4-1 · 4-2) · §5 (예측 구간 · 정보량 · 판정) · §6 (측정 꼴) · §10 (명령 꼴 (3)–(5) · **멈춤 목록** · 런 수) · §11 (선행 관문) · 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §6 (수렴 증서 ⓐ ⓑ ⓒ) · §7 (세대 `p3ca-` · 영수증 · LEAN 표) · 같은 부류의 앞선 사슬 `scripts/sdcp_anchor_v2_chain.py` (값 봉인 · 멈춤 · 사슬이 점을 고르는 꼴 — 그 꼴을 따른다) · 러너 `scripts/sdcp_gain_vox015_8arm.sh` (env: `CJUNC=1` · `CJUNC_RJ` · `CJUNC_LEN_LAW` · `CJUNC_UNREG_LAW` · `CJUNC_S_MIN_UM` · `CJUNC_TOL_FF_UM` · `CJUNC_PTFE_JLAW` (P0/P1) · `SDCP_MOD_C` (0/1) · `STEP3_RTOL` · `PTFE_STAMP=face_alpha` · 팔 이름 `p2_<침대>[_sph][_fa][_cj<R_j>_<해시8>][_c<0|1>][_rt<rtol>]_a<i>`) · 판정기 `scripts/sdcp_gain_verdict.py` (팔마다 `run_contract.ca_ext_record_ok` · 세대 섞임 거부 · 증서 없음 = 미게시) · `scripts/run_contract.py`.

## 만들 것 — 새 파일 둘만
- `scripts/rint_r_chain.py` — 단계 `ladder` (법칙 끝 P0 · P1 마다) · `predict` · `verdict` (등록 R §10 (3)–(5) 의 꼴 · 인자 이름은 그 꼴을 따르되 필요하면 보탬).
  - **ladder** = 등록 R §3 그대로 기계적으로: 바닥 (R_j → ∞ = 접합 간선 없음) · 천장 (R_j → 0) → `CALIB_IMPOSSIBLE` · `CALIB_EDGE` (2 %) → 점 {1e4, 1e6, 1e8} Ω → 끼지 않으면 같은 쪽 ×100 → 끼면 로그 중점 반씩 (이웃 비 ≤ 10^0.5) → ln σ ↔ ln R_j 직선 보간 · 유효숫자 3 자리 = R_j,0 → 식별성 e ≥ e_min (0.02 / ln √10) → 확인 런 |σ/1.63 − 1| ≤ 2 % (넘으면 그 점 넣고 다시 · 최대 두 번 → `CALIB_UNCONFIRMED`) → 비단조 τ_mono 1e-3 → 점 수 상한 12 → R_j,lo · R_j,hi (±2 %) → origin 확인 §3-3 (arm 1 · 2 · ln(max/min) ≤ 0.02 아니면 표지).  어떤 바닥 · 천장 극한을 러너 env 로 어떻게 부를지 (R_j 아주 큼 / 접합 끔 / 정확 축약) 는 지금 코드에서 가능한 것을 확인해 정하고 보고 (없으면 "미구현 · 필요한 API" 로).
  - **predict** = §4-1 네 모서리 (c ∈ {0, 1} × P ∈ {P0, P1}) × {R_j,lo · R_j,0 · R_j,hi} · DBE arm 0 · 같은 P 일관 검사 (c1 ≥ c0 − τ_mono · SBE 에서 c 는 no-op 비트 같음) · §4-2 origin 규칙 (네 모서리 모두 arm 1 · 2 · 0.1 W).  R_j 는 사다리 요약에서 사슬이 읽는다 (사람이 옮겨 적지 않는다).
  - **verdict** = §5 그대로 · 원 팔 JSON 전부에서 다시 계산 (같은 답인지 = 다시 판정 도구) · 판정 이름 · 표지 (§5-6) · §7-1 문장 조건.
  - **값 봉인**: 사슬은 σ 를 읽어 점을 고르지만 화면 · 로그에는 σ 값을 찍지 않는다 (반복 수 · 잔차 · 판 전류 불균형 · 시간 · 상태만) · `--show-results` 는 판정에 쓰는 런이 다 끝난 뒤 한 번 (등록 R §4-1).
  - **멈춤** = 등록 R §10 끝 목록 전부 (출력 폴더 비어 있지 않음 · 러너 rc ≠ 0 · `.rejected_*` · 매니페스트 ≠ 요청 · `physics_protocol_id` 가 `p3ca-` 아님 · `ca_ext_record_ok` 실패 · 영수증 ≠ LEAN 표 · 수렴 증서 실패 (= 그 점 `NOT_COMPUTED` · 사다리 멈춤) · 계획 해시 ≠ §2-1 개정값 · env 에 `SIGMA_VGCF_OVERRIDE` · face_alpha 런의 `ptfe_cells_observed` > 0 · sid 격자 ≠ off 격자 · 같은 P 일관 위반 · 비단조 · 식별성 · 점 수 상한 · 시간 상한 · 같은 킷 · 같은 계획 두 번 · 판정 입력 sha256 ≠ 런 산출).  각 멈춤 = 구조화 사유 + 원인 칸.
  - 숫자 문턱 (2 % · 0.02 · e_min · τ_mono · 10^0.5 · 12 · 0.1 W) = 등록 R 의 값을 상수로 · 한 곳에 · 이름 붙여.
- `scripts/test_rint_r_chain.py` — **가짜 러너** (작은 파이썬 · 정해 둔 σ(R_j) 함수와 진짜 꼴의 팔 JSON · 매니페스트 · `ca_ext` · 증서를 쓴다 · GPU 없음) 로: 끼기 · ×100 확장 · 반씩 좁히기 · 보간값 손계산 대조 · 식별성 실패 · IMPOSSIBLE · EDGE · 확인 실패 두 번 → UNCONFIRMED · 비단조 · 12 넘음 · 증서 실패 → NOT_COMPUTED · lo/hi 손계산 · origin 두 규칙 · 같은 P 일관 위반 · 멈춤 목록 하나씩 (변조 팔 · 섞인 세대 · env 오염 · 출력 폴더 있음 · 계획 해시 다름 …) · 값 봉인 (화면 · 로그에 σ 숫자 없음) · 다시 판정 = 같은 답 · 정상 사슬 끝-끝 (양성).  변이 몇 개 (보간을 선형 R_j 로 · 2 % → 3 % · origin 규칙 끔) 가 시험을 떨어뜨려야.

## 순서 · 규칙
- 커밋 1 = 시험 먼저 (모듈 없음 → 전부 실패 · "pre-fix 0/N (module absent)") · 커밋 2 = 구현 · 필요하면 3 = 다듬기.  각 커밋 메시지에 고치기 전 → 뒤.
- **다른 파일은 건드리지 않는다** — 러너 · 판정기 · run_contract · sdcp_anchor_v2_chain · compare 는 다른 에이전트 Z1 이 같이 고친다.  필요한 API 가 없으면 사슬 안에서 지금 있는 함수만 쓰고, 모자란 것을 보고의 "필요한 API" 에 적는다.
- ⚠ **메인 게이트가 ≈ 20:15 UTC 까지 돈다 — 그 전엔 무거운 시험 금지** (가짜 러너 시험은 가볍게 설계 — 전체 60 s 안 목표).
- push · `scripts/check_all.sh` · `git fetch` 안 함 · 실제 GPU 런 · kgy 접속 없음 · 디스크 적게.
- ⛔ 봉인 32 파일 · 문서 · 원장 · CLAUDE.md · 진행 기록 금지.
- 커밋 메시지 영어 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 커밋 SHA · 시험 수 · 단계별 CLI · 멈춤 사유 이름 목록 · 바닥 · 천장을 어떻게 불렀나 · 손계산 대조 · 변이 표 · 실행 시간 · 등록 R 과 다르게 한 곳 (있으면 이유) · 필요한 API · kgy 에서 쓸 명령 꼴 (§10 (3)–(5) 를 실제 이름으로).
