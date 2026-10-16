# LHS214 재검증 반례 수정 (L214R-01–11 · WEB-09) — 증거 (2026-10-16 · 결과 0 건 · 새 214 실행 없음)

> 근거 = Codex 재검증 판정문 `docs/reviews/codex_review_lhs214_fix_reverify_20261015.md` (검토 핀 `9e3ef54ca`) · 수정 계획 `docs/reviews/lhs214r_fix_plan_20261016.md` (§2 Q1–Q5 · §4 · §4-2 · §4-3 = 1저자 10-16 비준) ·
> 요청서 `docs/reviews/codex_lhs214r_fix_recheck_request_20261016.md`.
> **기준** = 본 가지 `6cb256956` (수정 직전 — 검토 핀 `9e3ef54ca` 와 바뀐 코드 = `scripts/check_doc_refs.py` 하나 · 봉인 32 · 인계 도구 바이트 같음).
> **최종 코드** = 본 가지 `60ba39e22` (L214R-09–11 수정 · 이 폴더를 담은 커밋은 문서 · 증거만 더한다).  모든 실행 = 컨테이너 Linux · Python 3.11 · `OMP_NUM_THREADS=1`.

## 1. 무엇이 어디에

| 파일 · 폴더 | 내용 |
|---|---|
| `before/` | 시험 먼저 — 각 시험 먼저 커밋 (고치기 전 코드 + 새 시험) 을 깨끗한 작업 폴더 (`git worktree` · detached) 에 체크아웃해 돌린 로그 여덟 (종료코드 = `rc.tsv`) |
| `final/` | 최종 코드 `60ba39e22` (깨끗한 작업 폴더) 에서 같은 시험 + `webapp/test_pipeline_provenance.py` + 봉인 지문 보고 (`code_fp_report.log`) (종료코드 = `rc.tsv`) |
| `a4_l214r_no_impact.py` · `.log` · `.json` | 무영향 대조 (기준 `6cb256956` ↔ 최종 코드 · 읽기 전용 · L214 증거의 `a4_no_impact.py` 도우미 · 침대 · 웹앱 탐침을 그대로 가져다 쓴다) |
| `probe_rerun/` | Codex 탐침 다섯 무변경 재실행 — 드라이버 `drive_l214r_probe.py` · 파생 `receipt_identity_noassert.py` · 고치기 전 `pre_6cb256956/` · 최종 `final_60ba39e22/` (출력 JSON · 드라이버 로그 · `driver_summary.json`) · 대조 `cmp_pre_vs_final.json` · 화면 행 대조 `display_rowdiff_pre_vs_final.txt` (도구 `display_rowdiff.py`) |
| `rc.tsv` | 단계 · 원장 · 커밋 · 명령 · 종료코드 · 결과 · 로그 (시험 · 무영향 대조 · 탐침 전부) |
| `SHA256SUMS` | 이 폴더 파일의 sha256 (자기 자신 제외) |

## 2. 결과

### 2-1. 시험 먼저 → 고친 뒤

| 원장 | 시험 | 시험 먼저 커밋 · 고치기 전 (`before/`) | 수정 커밋 · 최종 (`final/`) |
|---|---|---|---|
| `L214R-01` | `scripts/test_l214r01_certificate.py` | `a955050df` · 48/112 | `3676a33eb` · 112/112 |
| `L214R-02` | `scripts/test_l214r02_model_limit_flag.py` | `1cd47e940` · 17/47 | `2450cb858` · 47/47 |
| `L214R-03` | `webapp/test_l214r03_display.py` | `f28636a54` · 5/14 | `2fc138274` · 14/14 |
| `L214R-04` | `scripts/supp20_input_receipt.py --selftest` | `3b739519c` · 100/111 | `e6f7895d0` · 111/111 |
| `L214R-05` | `scripts/test_l214r05_published_certificate.py` | `755b71feb` · 109/184 | `530ddb355` · 184/184 |
| `WEB-09` | `webapp/test_web09_accepted_refresh.py` | `7a54d0199` · 7/16 | `dcd06869d` · 16/16 |
| `L214R-06`–`08` | `scripts/test_l214r06_same_class.py` | `40a08afb5` · 118/306 | `2e85d08eb` · 306/306 |
| `L214R-09`–`11` | `scripts/test_l214r09_same_class.py` | `a5cab63c7` · 43/96 | `60ba39e22` · 96/96 |

- 고치기 전 실패 = 등록한 반례 묶음 (대조군은 고치기 전에도 통과) · 시험 먼저 실행은 전부 종료코드 1 · 최종은 전부 0 (`rc.tsv`) · `L214R-06`–`11` 은 통합 때도 메인 세션이 본 가지 체크아웃에서 돌려 에이전트 수와 같음을 확인했다.
- `final/test_pipeline_provenance.log` 284/284 — L214R-06 뒤 첫 게이트가 267/284 로 잡은 가짜 증서 (시도 목록 없음) 를 fixture-drift 규약대로 고친 뒤 (push 전 · 요청서 §2).

### 2-2. Codex 탐침 무변경 재실행 (`probe_rerun/`)

- 탐침 다섯 = Codex 묶음 바이트 그대로 (sha256 = 묶음 `package_manifest.json` · `driver_summary.json` 의 `probes.*.same` = true) · source = 그 rev 의 Codex manifest 경로 ∪ `scripts/*.py` · `webapp/**` · 기준 트리 `0c557e72a` · `python3 -E -X utf8 -B`.
- 종료코드 — 고치기 전: 아홉 실행 전부 0 · 최종: 전부 0 · 단 `receipt_identity` 1 (그 탐침은 결함의 존재를 assert 로 적어 두었다 — `minimal_activate_section3` 실패 칸 == ['R0','D1'] · 최종 트리의 실패 칸 = [] 라 그 줄에서 멈춘다 = 고침 표지) · assert 일곱 줄만 뺀 파생 `receipt_identity_noassert` 0.
- 고치기 전 ↔ 최종 바뀐 판정값 (`cmp_pre_vs_final.json` · 환경 = run id · 시각 · 경로 · 파일 해시 · MemAvailable · 비교기의 NaN ≠ NaN 제외):

| 출력 | 바뀐 것 |
|---|---|
| `numeric_probes.json` | 증서 변이 7 = None → 거부 사유 · 레코드 넷 (overflow_q_reconstruction_currents · contradictory_attempt × 3) = 공용 판정 · 0b · 채널 판정 · 모드 파일 내용 판정 · Physics τ 에서 거부 · `scale = 1e200` = OverflowError → `not_computed` · `invalid_geometry` · τ 표지 두 칸 더함 · 증서 결합 [] · 세대 g2 그대로 (요청서 §5-3) |
| `consumers_*.json` | 띠 폴백 (L1 · L2) + H0 모형 한계 두 고정 사례 = 배포 HOLD (`build_v13` ReleaseError) · 인계 행 primary_hold · 인계표 표지 두 칸 · 음성 경로 74 칸 같음 |
| `display_source.json` | 68 케이스 중 55 바뀜 — 받아들이지 않은 모드 칸 `—` · 받아들인 모드 칸 = 지금 값 · valid_zero `—` · Δ = 두 칸 모두 숫자일 때만 (`display_rowdiff_pre_vs_final.txt`) · 13 케이스 그대로 |
| `display_base.json` | 같음 (기준 트리) |
| `receipt_identity/*` | 비준 전환 변이 rc 1 → 0 · 다른 변이 여섯 그대로 · 대기 지문 값 · 지연 import 수 91 → 92 (L214R-11 의 `_stop_num` 이 `tau_flux` 를 부름) |

- `L214R-06`–`11` 수정 전 · 후 (`dcd06869d` ↔ `60ba39e22`) 사이에 Codex 탐침 판정값은 바뀌지 않았다 (새 수정이 겨눈 입력은 Codex 탐침 밖 — 새 시험 둘이 본다).

### 2-3. 무영향 대조 (`a4_l214r_no_impact.log`) — PASS 36/36 (197.7 s)

- N 생산자 16 = 결과 JSON 전체 비트 같음 (합성 넷 · real_14 · case15 · 격자 둘 × 두 모드 · real_14 run_decomposition).
- T τ 소비자 6 = v1.2 τ 원천 194 케이스 옛 50 칸 비트 같음 + 표지 두 칸 194 건 전부 False · 새 생산자 레코드 넷 · lhsx_054 진단 레코드 = 옛 칸 · 세대 계약 · 0b · 증서 결합 같음.
- R 배포 빌더 6 = v1.2 인계표 (130 · 64) 빈칸 뜻 · 관통 분류 · 상태 집계 같음 · **의도 변경 2** = 주 타깃 관문이 v1.2 표 (표지 칸 없음) 에 문제 하나 (fail-closed · L214R-02) · 같은 표에 상태에서 유도한 표지를 붙인 사본 = 문제 없음.
- W 웹앱 transform 8 = 네 꼴 × 두 표 같음.

### 2-4. 봉인 지문 (`final/code_fp_report.log` · 재봉인 아님)

- 봉인 CODE_FILES 32 · 기준 `0c557e72a` = `e8b2496b…` (등록 §3 그대로) → 최종 = `e76dbe0897c4a0f5e2a359f07e7197400d49be3d257a8676c0bf8a1cd052a07e` = 두 등록 초안의 대기 선언 (`code_fp_pending`).
- 바뀐 봉인 파일 4 = `scripts/network_conductivity.py` · `scripts/tau_flux.py` · `webapp/app.py` · `webapp/pipeline_service.py`.

## 3. 다시 돌리기

```bash
# 시험 먼저 수: §2-1 표의 시험 먼저 커밋을 체크아웃해 그 시험 (예: git checkout a5cab63c7 && python3 scripts/test_l214r09_same_class.py → 43/96)
# 최종: 리뷰 핀 체크아웃에서
OMP_NUM_THREADS=1 python3 scripts/test_l214r06_same_class.py      # 306/306
OMP_NUM_THREADS=1 python3 scripts/test_l214r09_same_class.py      # 96/96
OMP_NUM_THREADS=1 python3 -B docs/reviews/lhs214r_fix_evidence_20261016/a4_l214r_no_impact.py --base 6cb256956 --json /tmp/a4.json   # PASS 36/36
python3 docs/reviews/lhs214_fix_evidence_20261015/code_fp_report.py --base 0c557e72a                                                # e76dbe08…
# 탐침 재실행 (리포 밖 새 폴더 · Codex 탐침 무변경): REV = 6cb256956 (고치기 전) · 리뷰 핀 (최종)
L214R_REPO=$PWD python3 -I docs/reviews/lhs214r_fix_evidence_20261016/probe_rerun/drive_l214r_probe.py /tmp/l214r_probe_REV REV
python3 -I docs/reviews/codex_supp20_support_review_evidence_20261012/_repro_ours_20261012/compare_probe_outputs.py <pre>/evidence <final>/evidence out.json numeric_probes.json …
```

- 드라이버는 리포 경로를 환경변수 `L214R_REPO` (기본 = 이 세션의 리포 경로) 로 받는다 — 다른 기계에서는 그 값을 준다 (위 명령처럼 리포 루트에서 `$PWD`) · OUT 은 리포 밖 새 폴더만 받는다.
