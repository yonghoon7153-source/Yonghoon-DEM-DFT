# Rint ② 구현 A · B · C 합치기 (작업 트리 · push 안 함 · 10-20)

## 기반
- 너의 작업 트리에서 `git reset --hard 952ad1a25` (본 가지 로컬 끝 · 게이트 통과 뒤 push 될 커밋 · `git log -1` 로 확인).  `git fetch` 하지 않는다.
- 옮길 커밋 (모두 기반 `d1768cf0c` 위 · 순서대로 `git cherry-pick`):
  1. C (S0 원장 · 새 파일만): `42537ea18` → `18c4f70c8` → `9a76f8152` (가지 `worktree-agent-a4d60a4fd46988f2c`)
  2. B (S2 탄소 접합 · S3 SDCP · 수렴 증서): `160edb0be` → `28e7bc689` → `61b6a9ec5` (가지 `worktree-agent-a3a891444f3a490d1`)
  3. A (S1 PTFE face_alpha · `ca_ext` 블록): `733fe0ad2` → `8138bb3d0` → `7b4cf89bd` (가지 `worktree-agent-a8962a22f0993f713`)
- 각 커밋 메시지는 그대로 (cherry-pick 기본) · 충돌 푼 커밋은 메시지 끝에 `(integrated: <무엇을 어떻게 합쳤나 한 줄>)` 한 줄 덧붙임 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft` 유지.

## 충돌 · 합칠 때 지킬 것 (두 에이전트 보고)
- `scripts/step3_sigma.py` `couple()` — A 의 α 블록 (행렬 조립 직전 g 에 α 곱 · α = 0 면 제거 · `_keep`) 이 **먼저**, B 의 cjunc 훅이 **그 바로 뒤**.  cjunc 가 면별 배열 (sid · pid) 을 압축하면 같은 `_keep` 을 적용.  face_alpha 와 cjunc 를 같이 켰을 때의 정책 (`require_plan` 이 cjunc 를 거부하지 않음) 은 **지금은 둘을 같이 켜면 거부** (설계가 조합을 아직 정의하지 않음 — 거부 시험 하나 먼저 · 고치기 전 실패 확인) — 이후 1저자 · Codex 결정.
- `scripts/run_contract.py` — A 의 `CA_EXT_SUBBLOCKS` 등록부 + B 의 회계 한 줄 둘 다 · B 의 cjunc · sdcp_mod 를 A 등록부 꼴로 올리는 것은 **이번에 하지 않는다** (B 보고 "남은 것" B1) — 등록부에 B 블록이 없다는 사실을 보고에 적는다.
- `scripts/mpm_webapp_payload.py` — A 의 face_alpha 배선 · `ca_ext` + B 의 `--step3-rtol` 둘 다.
- `scripts/check_all.sh` 등록 줄 (A 가 시험 둘 등록) · `docs/reviews/selftest_inventory.tsv` 가 있으면 B · C 시험도 같은 꼴로 등록되어 있는지 확인 (없으면 등록 · 기존 꼴 그대로).
- 같은 규칙 사본 둘 (B `carbon_junction` 의 끊기 규칙 · C `ca_s0_census` 의 조각 규칙 = `_fibre_segment_ijk` 사본) — 이번에 하나로 합치지 않는다 · 셋 (생산 · B · C) 이 셀 단위로 같은지 대조하는 시험이 이미 각자 있는지 확인하고 보고.

## 시험 (⚠ 본 트리 게이트가 끝나기 전 (≈ 14:30 UTC) 에는 무거운 시험 금지 — 체리픽 · 충돌 해결 · 작은 확인만 · 그 뒤 전부)
- 새 시험: `scripts/test_ptfe_face_alpha.py` (A 238) · `webapp/test_ca_ext_labels.py` (9) · `scripts/test_carbon_junction.py` (B 92) · `scripts/test_step3_conv_cert.py` (27) · `scripts/test_ca_s0_census.py` (C 108) — 합친 뒤 수가 바뀌면 이유.
- 회귀: `python3 scripts/step3_sigma.py --selftest` · `--selftest-rint` · `scripts/test_rint_g2_am_iface.py` 136 · `scripts/test_rint_g2_rrm.py` 55 · `scripts/test_rint_g2_join.py` 309 · `scripts/test_rint_receipts.py` · `python3 scripts/run_contract.py --selftest` · `python3 scripts/check_method_discipline.py --selftest` + 인자 없이 (오류 0) · 철회값 스윕은 게이트가 한다.
- **끈 경로 비트 대조**: A 의 B1 · B2 (`--old-scripts /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/s1/old/scripts`) · B 의 C0 (기반 `d1768cf0c`) 를 **합친 트리에서** 다시 — 셋 다 같음이어야.
- 봉인 32 교집합: `git diff --name-only 952ad1a25 HEAD` ∩ `scripts/run_network_194_parallel.py` 의 `CODE_FILES` = 빈칸이어야 (아니면 멈추고 보고).

## 규칙
- push · `scripts/check_all.sh` · `git fetch` 안 함 · 디스크 적게 (큰 사본 금지 · 임시 = 스크래치 · 쓰고 지움).
- 문서 (설계 · 등록 · 요청서 · 원장 · CLAUDE.md · 진행 기록) 는 고치지 않는다 (메인이 한다).  원격에 없는 커밋 번호를 문서에 쓰지 않는다.
- 보고 (한국어 · 표 · 짧게): 합친 커밋 SHA 9 개 (순서) · 충돌 자리와 푼 방법 · 새 거부 시험 (face_alpha + cjunc 동시) 고치기 전 → 뒤 · 새 시험 · 회귀 수 · 비트 대조 셋 · 봉인 교집합 · 남은 것.
