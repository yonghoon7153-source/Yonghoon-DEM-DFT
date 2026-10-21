# Rint ② Z3 — 사슬이 실제 런을 돌 수 있게: face_alpha + 접합 조합 · 극한 런 · 팔 고르기 · 기록 칸 (시험 먼저 · 작업 트리 · push 안 함)

## 기반
- 너의 작업 트리에서 `git reset --hard c7bbd8474` (= Z1 러너 · 판정기 굳히기 + Z2 R 런 사슬 `scripts/rint_r_chain.py` 를 합친 메인 · 아직 push 전 · 같은 저장소라 객체가 있다) → `git log --oneline -5`.  `git fetch` 하지 않는다.
- 정본: 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §3 (S1 face_alpha) · §4 (S2 탄소 접합 · P0/P1 = PTFE–접합 끝 법칙 · 길이 법칙 v0 · 극한 · 단락 J11) · §5 (S3) · §6 (수렴 증서) · §7 (세대 · 영수증) · 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3-1 (바닥 R_j → ∞ · 천장 R_j → 0 = 정확한 축약) · §3-3 · §4-2 (origin arm 1 · 2) · §10 (명령 꼴 · 멈춤).
- 사슬 `scripts/rint_r_chain.py` 의 머리 · 시험 `scripts/test_rint_r_chain.py` 의 가짜 계약 자리 (X03) 를 먼저 읽는다 — 이번 일 = 그 사슬 보고의 "필요한 API" 일곱 중 ②–⑦ (① `SIGMA_FIBRE_BULK` 은 Z1 이 했다 · 확인만).

- Z1 이 바꾼 것 (알고 시작): 다음 세대 노브 (`CJUNC` · `PTFE_STAMP=face_alpha` · `SDCP_MOD_C`) 를 켜면 `STEP3_RTOL` 필수 (없으면 러너 rc 2 · 팔 시작 전) · `SIGMA_FIBRE_BULK` (직경 보존 · 팔 태그 `_fb<값>` · `SIGMA_VGCF_OVERRIDE` 와 동시 = 거부) · 손잡이 표 10 칸 · compare_dirs 의 `ca_ext` 축 · 판정기 `--expect-generation`.
- ⚠ **메인 게이트가 ≈ 21:25 – 22:15 UTC 에 돈다 — 그 사이 무거운 시험 (60 s 넘는 것 · 여러 프로세스) 금지** (코드 · 시험 작성 · 작은 확인만).

## 할 일 (묶음마다 시험 먼저 → 구현 · 기본 끔 = 옛 동작 바이트 같음 · 각 묶음 고치기 전 실패 확인)
1. **face_alpha + 탄소 접합 한 런 (+ P1)** — 지금 `runner_ca_ext` · `cjunc_protocol_record` · `cjunc_block_problem` (· payload 입구 · `step3_sigma.solve_sigma_z` 입구) 이 둘을 같이 켜면 거부한다 = 통합 때 넣은 **임시** 거부 (설계 §3 · §4 의 동시 거부 목록에는 없다 · 등록 R §10 꼴 = `PTFE_STAMP=face_alpha` + 접합 + P0/P1).  조합 규칙 = 설계 그대로: α (면 개구율) 는 `couple()` 에서 **먼저** 융합 면에 곱하고 (α = 0 면 = 제거 · `_keep`) · 그 다음 접합 훅이 발자국 면을 끊고 접합 간선을 넣는다 (면별 배열 압축은 같은 `_keep`) · PTFE 가 접합 끝을 덮을 때는 P0/P1 법칙만 (α 를 접합 간선에 곱하지 않는다 — 이중 계상 금지).  시험 먼저: (i) PTFE 0 → 조합 = 접합만 과 비트 같음 (ii) 접합 끔 → face_alpha 만 과 비트 같음 (iii) 접합이 끊은 면에 α 가 남지 않음 · α 배열 · sid · pid 압축 일관 (iv) PTFE 캡슐이 접합 끝을 덮는 픽스처: P0 = 접합 간선 그대로 · P1 = 설계의 P1 동작 · α 는 접합 간선에 안 걸림 (v) Rayleigh 단조: PTFE 늘리면 σ 증가 없음 · σ(P1) ≤ σ(P0) (vi) 순열 · 원점 이동 불변 (vii) 원장 · 소산 항등식 · `ca_ext` 에 두 하위 블록 다 · 세대 `p3ca-` · `ca_ext_record_ok`.  `centerline + P1` 거부는 그대로 (설계 목록).
2. **극한 런** — `CJUNC_RJ=inf` (바닥 = 접합 간선 없음 · 발자국 면은 끊긴 채) · `CJUNC_RJ=0` (천장 = 접합 양 끝 정확한 축약 · 설계 §4 의 단락 J11 처리 · `carbon_junction.cjunc_plan(allow_rj_limits=True)` 기구가 있다) → 러너 · payload · `ca_ext_cjunc` · `run_contract` 배선 · 매니페스트 표지 `rj_limit` (`inf` / `zero`) · `allow_rj_limits` · `quantitative=False` (판정 값이 아니라 사다리 진단) · `cjunc_block_problem` 이 바닥의 `n_none_inf` · 천장 축약 (S3 없이) 을 받는다 · 영수증 · JSON 에 R_j = ∞ 를 쓰는 꼴 (`receipt_match` 대조 · JSON 은 inf 를 못 쓴다 → 문자열 표지 + 숫자 칸 null 등 · 한 꼴로) · 손계산 시험 (두 섬유 + 접합 하나: 바닥 = 접합 없는 회로 · 천장 = 접합 양 끝을 한 노드로 묶은 회로).
3. **러너 `ARM_LIST`** (예 `1,2`) — origin 검사에서 a0 를 다시 돌지 않게 · 기본 끔 = 지금 `ARMS` 그대로 · OUTDIR · 팔 이름 · 영수증 · 봉인 동작 일관 · 중복 · 범위 밖 = 거부.
4. **off 격자 sid 지문** — `ca_ext.ptfe_face.evidence.fp.sid_off` (face_alpha 런이 쓰는 off 격자의 sid 지문) · 사슬이 같은 킷 런끼리 · S0 와 대조할 수 있게.
5. **CG 반복 수 기록** — 수렴했을 때도 STEP3 기록에 반복 수 (주 솔브 · 보조 솔브 · ⓒ 이어 풀기) 를 남긴다 (등록 R §11 예외 = 숫자 탐침이 보는 칸 · σ 아님).
6. 사슬 쪽 맞춤 — 위 API 가 들어오면 `scripts/rint_r_chain.py` 의 가짜 계약 자리 (시험 X03) 를 실제 `ca_ext_record_ok` · `check_arm` 으로 · origin = `ARM_LIST=1,2` (ARMS=3 우회 삭제) · 극한 런 env 꼴 · `sid_off` 대조 · 시험 갱신 (고치기 전 실패 확인).
- 끝으로 사슬 끝-끝 시험 하나: 가짜 runner 가 아니라 **실제 러너를 아주 작은 픽스처 킷**으로 (GPU 없이 payload 가 도는 크기 · 기존 b6 · 러너 시험 픽스처 꼴) 바닥 → 천장 → 사다리 점 하나까지 (시간 되면) — 안 되면 무엇이 막는지 보고.

## 회귀 (끝에 한 번 · 수 그대로)
- `scripts/test_rint_r_chain.py` · `scripts/test_ca_ext_b6.py` · `scripts/test_ca_ext_runner.py` · `scripts/test_ca_ext_verdict.py` · `webapp/test_ca_ext_labels.py` · `scripts/test_carbon_junction.py` · `scripts/test_ptfe_face_alpha.py --old-scripts /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/s1/old/scripts` · `python3 scripts/step3_sigma.py --selftest` · `--selftest-rint` · `python3 scripts/run_contract.py --selftest` · `python3 scripts/check_method_discipline.py --selftest` + 인자 없이 (오류 0 · 규칙 M) · 끈 경로 비트 대조 (새 노브 다 끄면 매니페스트 · 러너 영수증 · 팔 이름 = 기반 sha 와 같음).  `scripts/test_step3_conv_cert.py` 는 돌리지 않는다 (2,000 초대) — 수렴 코드를 바꾸면 그 사실을 보고.
- 무거운 시험은 하나씩 (`nice -n 19`).

## 규칙
- push · `scripts/check_all.sh` · `git fetch` 안 함 · 실제 GPU 런 · kgy 접속 없음 · 디스크 적게.
- ⛔ 봉인 32 파일 (`scripts/run_network_194_parallel.py` 의 `CODE_FILES`) · 문서 · 원장 · CLAUDE.md · 진행 기록 금지.
- 커밋 메시지 영어 · 모델 이름 없음 · "pre-fix N/M (fails = K checks from J counterexamples)" 꼴 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 커밋 SHA · 고치기 전 → 뒤 · 조합 규칙을 코드에서 어떻게 했나 (설계와 다르면 이유) · 극한 런 꼴 (env · 표지 · JSON) · 손계산 대조 · 끈 경로 비트 대조 · 실제 러너 끝-끝 결과 · 시험 실행 시간 · 남은 것.
