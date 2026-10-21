# Rint ② 2 일 차 Z1 — 러너 · 판정기 굳히기 (시험 먼저 · 작업 트리 · push 안 함)

## 기반
- 너의 작업 트리에서 `git reset --hard d9404ccb2` (메인 끝 = X (S0 · 지문) + Y/Y2 (B6 payload · 러너 · 판정기 · 웹앱 표지) 합친 판) → `git log --oneline -3`.  `git fetch` 하지 않는다.
- 정본: 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §1-2 #1 · #2 (VGCF σ = 두 전극 같은 값 · 직경 보존 · Endo 단섬유 1 × 10⁴ S/cm → vox 0.15 에서 7,853.98 S/cm) · §6 (수렴) · §7 (세대 · 영수증 · 네 방어) · 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §3-5 · §10 (멈춤 목록) · 지금 코드 = `scripts/sdcp_gain_vox015_8arm.sh` · `scripts/run_contract.py` (`RUNNER_CA_EXT_ENV` · `runner_ca_ext` · `runner_ca_ext_view`) · `scripts/sdcp_gain_verdict.py` · `scripts/sdcp_anchor_v2_chain.py`.
- 직전 에이전트 (Y2) 보고의 "남은 것" 이 이번 일이다 (아래 1–5).

## 할 일 (묶음마다 시험 먼저 → 구현 · 기본 끔 = 옛 동작 바이트 같음)
1. **`SIGMA_FIBRE_BULK`** — 러너가 σ_bulk [S/cm] 를 받아 직경 보존 복셀 σ_VGCF = σ_bulk · (π d_f²/4) / vox² (d_f = 섬유 지름 · 지금 코드가 bulk 100 고정으로 쓰는 같은 식 · 그 자리를 찾아 같은 함수로) 로 payload 에 넘긴다.  `SIGMA_VGCF_OVERRIDE` 와 같이 있으면 거부 (구조화 사유) · 매니페스트에 쓰인 σ_VGCF 값 + bulk 값 + 식 이름 기록 · 선언 축 · 팔 태그 (옛 팔과 이름 충돌 없게).  손계산 시험: vox 0.15 · 1e4 → 7,853.98 · vox 0.4 · 100 → 11.0447 (옛 값 재현).
2. **다음 세대 노브에 `STEP3_RTOL` 필수** — `CJUNC=1` · `PTFE_STAMP=face_alpha` · `SDCP_MOD_C` 중 하나라도 켜면 `STEP3_RTOL` 이 없을 때 **팔 시작 전** 거부 (지금은 계산 뒤 봉인에서 HOLD — GPU 시간 낭비) · 개발 런은 값을 명시해 넘긴다 (기본값 없음 원칙).  옛 세대 (노브 끔) 는 그대로.
3. **`sdcp_anchor_v2_chain.py`** — 부모 셸의 `CJUNC*` · `SDCP_MOD_C` · `STEP3_RTOL` · `SIGMA_FIBRE_BULK` 가 env 에 있으면 거부 (현 세대 사슬이 다음 세대 노브에 오염되지 않게 · 지우기보다 거부 = 사람이 안다).
4. **compare_dirs** (두 런 디렉터리 대조 · `--compare-dir --expect-differ` 계약 — 위치는 코드에서 찾는다) 가 `ca_ext` 키를 분류하지 않아 다음 세대 두 디렉터리 대조가 HOLD 된다 → `ca_ext` 하위 블록 (`ptfe_face` · `cjunc` · `sdcp_mod`) 을 등록 축으로 분류 (`run_contract.CA_EXT_SUBBLOCKS` 와 같은 원천) · 등록 밖 차이는 여전히 HOLD.
5. **판정기 `--expect-generation`** (설계 §7 의 네 번째 방어) — 코호트 전체 세대 (`physics_protocol_id` 접두 · `p2-` / `p3ca-`) 를 선언하고 다르면 거부.
- 러너 시험 (`scripts/test_ca_ext_runner.py` · 92–106 s) 은 게이트에 그대로 둔다 (메인 결정) — 새 시험은 가능하면 60 s 안.

## 회귀 (끝에 한 번 · 수 그대로 보고)
- `scripts/test_ca_ext_runner.py` · `scripts/test_ca_ext_verdict.py` · `scripts/test_ca_ext_b6.py` · `webapp/test_ca_ext_labels.py` · `python3 scripts/run_contract.py --selftest` · `python3 scripts/sdcp_gain_verdict.py` 의 selftest · `python3 scripts/check_method_discipline.py --selftest` + 인자 없이 (오류 0 · 규칙 M) · `scripts/sdcp_anchor_v2_chain.py` 시험이 있으면 그것 · 끈 경로 비트 대조 (노브 다 끄면 러너 영수증 · OUTDIR · 팔 이름 · payload argv · 매니페스트 = d9404ccb2 와 같음 · Y2 의 NB 꼴).
- ⚠ **메인 게이트가 ≈ 20:15 UTC 까지 돈다 — 그 전엔 무거운 시험 (60 s 넘는 것) 을 돌리지 않는다** (코드 · 시험 작성 · 작은 확인만).  `scripts/test_step3_conv_cert.py` 는 돌리지 않는다.

## 규칙
- push · `scripts/check_all.sh` · `git fetch` 안 함 · 디스크 적게.
- 다른 에이전트 Z2 가 같이 돈다 (새 파일 `scripts/rint_r_chain.py` · `scripts/test_rint_r_chain.py` 만 만든다) — 그 파일은 건드리지 않는다.  Z2 가 쓰는 러너 env 이름 (`CJUNC=1` · `CJUNC_RJ` · `CJUNC_LEN_LAW` · `CJUNC_UNREG_LAW` · `CJUNC_S_MIN_UM` · `CJUNC_TOL_FF_UM` · `CJUNC_PTFE_JLAW` · `SDCP_MOD_C` · `STEP3_RTOL` · `PTFE_STAMP`) 은 바꾸지 않는다 (새 이름 보탬만).
- ⛔ 봉인 32 파일 (`scripts/run_network_194_parallel.py` 의 `CODE_FILES`) · 문서 · 원장 · CLAUDE.md · 진행 기록 금지.
- 커밋 메시지 영어 · 모델 이름 없음 · "pre-fix N/M (fails = K checks from J counterexamples)" 꼴 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 커밋 SHA · 고치기 전 → 뒤 · 새 env · 거부 사유 이름 · 손계산 대조 값 · 끈 경로 비트 대조 · 시험 실행 시간 · 설계와 다르게 한 곳 · 남은 것.
