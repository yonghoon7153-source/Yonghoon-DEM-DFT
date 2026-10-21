# Codex Rint ② 설계 리뷰 (10-21) — 우리 트리 재현 (10-21 KST 아침 = 10-20 22:50–23:24 UTC · 읽기 전용)

판정문 `codex_review_rint2_carbon_additive_design_20261021.md` · 리뷰 핀 `5dc6f7f0b91fd9db39ab595f6b8c79a8f0d2f3b5`.
리포 작업 트리 · 다른 작업 트리 안 씀 · fetch / push 안 함 · 원 미니 묶음 (`import_rint2rev/x/`) 무변경.

## 0. 한 줄

판정문 · 브리프에 쓰인 숫자 **165 항목 (추가 대조 3 포함) 중 153 같음 · 12 다름**.
다른 12 = **RCA-07 CG 반올림 11** (그중 **판정값 뒤집힘 1 건** — 주 반례의 판 균형 ⓑ 가 우리 환경에서 실패 → `certify ok=False`) + **RINT2-B-01 1** (Windows 전용 CRCRLF — Linux 재현 안 됨, 예상대로).
Part B 시험 · 탐침 · 독립 입력 · 실덤프 수는 **전부 같음** (324 · 138 · 179/324 · 144 · 113 · 62 · 457/660 · 104/119 · `delta_bound_um`).
RCA-07 의 결론 자체 (A/B/C 통과 ≠ 1e-4 인증) 는 우리 환경에서도 선다 — 연결 보조 사례 (−0.9037 %) · 23 반복 사례 (+5.56e-4) 가 A/B/C 통과.

## 1. 환경

| | 우리 | Codex |
|---|---|---|
| OS | Linux 6.18.44 x86_64 · glibc 2.39 · 4 코어 (다른 에이전트 동시 · 부하 2–5) | Windows |
| Python | 3.11.15 | 3.12.14 |
| NumPy | **2.4.6** | **2.5.3** |
| SciPy | **1.17.1** | **1.16.3** |
| BLAS | scipy-openblas 0.3.31 | 기록 없음 |
| zlib | 1.3 (gzip OS 바이트 3 = Unix) | 기록 없음 |
| 스레드 | OPENBLAS · OMP · MKL · NUMEXPR = 1 | 1 |
| 실행 | `nice -n 19 python3 -I -X utf8 -B` | `python -X utf8 -B` |

## 2. 입력 재구성 (git 객체 · 읽기 전용)

| 대상 | 방법 | 결과 |
|---|---|---|
| 핀 소스 `source/` | manifest 경로마다 `git show 5dc6f7f0b:<경로>` | **1,161 / 1,161** SHA256 · git blob · 바이트 같음 · 65,504,947 B (판정문 §1-1 과 같음) |
| `part_b/baseline/early/source/scripts/rint_iface_join.py` | `git show dcb97f1ed:scripts/rint_iface_join.py` | MANIFEST SHA `ee72b0d1…` 같음 (미니 묶음에서 빠져 있었음) |
| `baseline/early/tmp/join_independent/*` 30 | 핀의 `docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015/evidence/join_fixtures/` | **30 / 30** MANIFEST SHA 같음 |
| `baseline/old_join` (2b9efa253) · probes 4 | 묶음 그대로 + `git show 2b9efa253:` 대조 | 같음 → baseline MANIFEST **36 / 36** |
| 2b9efa253 모듈 트리 (179/324 용) | Codex `.imports.json` 의 8 모듈 + 시험 자료 7 을 `git show 2b9efa253:` | 모듈 **8 / 8** = Codex 기록 SHA · 자료 7 = 핀과 같은 바이트 |
| 2b9efa253 시험 (138 용) | `git show 2b9efa253:scripts/test_rint_g2_join.py` | sha256 `8db7f5a9ec5d967b…` (Codex 기록 없음 · 단언 줄 139/139 같음으로 갈음) |
| Codex `fullpin_overlay_match.json` 21 | 우리 소스와 SHA 대조 | **21 / 21** |

⚠ **Codex 묶음 결함 (기록)**: `REPRODUCTION_part_b.md` 는 *"보존 합성 입력 30개 … `part_b/baseline/` 에 정확 바이트로 동봉"* 이라 쓰지만 **Codex 전체 ZIP 의 `delivery_manifest.json` 에 그 30 파일이 없다** (baseline 항목 7 개뿐). ZIP 만 받은 쪽은 `structure_probe` · `structure_minimal_replay` 를 그대로 돌릴 수 없다. 우리는 핀 안 같은 바이트 사본으로 복원했다.

## 3. 탐침별 실행 결과

| 탐침 | rc | 시간 | 우리 결과 | Codex JSON 키 대조 |
|---|---|---|---|---|
| `geometry/geometry_probes.py` | 0 | 0.1 s | — | 144 값: 정확 142 · ≤1e-12 2 · 다름 0 |
| `registration/probe_registration.py` | 0 | 0.1 s | 실제 핀 스칼라 블록 exec 포함 | 133: 정확 131 · ≤1e-12 2 (1 ULP) · 다름 0 |
| `geometry/convergence_probes.py` | 0 | 0.8 s | 5 사례 · 두 번 · 4 스레드 실행도 바이트 같음 | 218: 정확 178 · ≤1e-12 3 · **다름 37 (CG 반올림)** · 판정 뒤집힘 1 |
| `geometry/search_cg_counterexample.py` (seed 611 · 80 s 예산 · 한 번) | 0 | 80 s | 143,478 표본 (Codex 200,000 / 33.8 s) · **찾은 표본 57,686 같음** · certify ok | 81: 정확 54 · ≤1e-12 7 · 다름 20 (표본 수 · 시간 · 같은 표본의 끝자리) |
| `part_b/independent_join_checks.py` | 0 | 32 s | **62: PASS 32 / REJECT 30 · 기대 밖 0** · F1 잔여 8 · real14 · case15 구/신 배열 전부 같음 | 1,258: 정확 1,251 · 경로 1 · 다름 6 (gzip 입력 SHA 만) |
| `part_b/known_limit_and_mutant.py` | 0 | 0.8 s | wd-only REJECT `derived_nonfinite` (n=1) · 변이 PASS · 5e-324 PASS r=0 · area=0 | 34: 정확 29 · 경로 1 · 다름 4 (개행 픽스처 = Linux) |
| `run_review test test_rint_g2_join.py` (원문) | 0 | 197 s | **324 / 324** | Codex Windows 320/324 · 단언 줄 대조 = **CR/CRLF 4 단언만 다름** |
| 같은 시험 `--lf-test-writer` | 0 | 195 s | 324 / 324 (Linux 에서는 no-op) | 단언 줄 325/325 · 로그 전체 0 줄 차 |
| 이전 138 시험 → 현행 모듈 | 0 | 186 s | **138 / 138** | 로그 전체 0 줄 차 |
| 현행 324 시험 → 2b9efa253 모듈 (`--lf-test-writer --loose-fixture`) | 1 | 188 s | **179 / 324** | 로그 전체 554 줄 0 차 (같은 145 실패) |
| `run_review probe structure_probe.py` | 0 | 17 s | **144 · 기대 밖 0** · real14 457/457/457 · 660 · case15 104/104/104 · 119 | 12,899: 정확 12,465 · 경로 434 · 다름 0 |
| `run_review probe numeric_review.py` | 0 | 17 s | **113: PASS 8 / REJECT 105 / 예외 0** | 9,091: 정확 9,090 · 경로 1 · 다름 0 |
| `run_review probe numeric_overflow_replay.py` | 0 | 0.8 s | 정상 PASS · 1e160 `derived_nonfinite` · 1e150 `delta_pos_mismatch` | 49: 정확 48 · 경로 1 · 다름 0 |
| `run_review probe structure_minimal_replay.py` | **1** | 0.8 s | `join_gate_failed(T4-2 n=1)` (예상 = 고친 관문 발화) | 같은 rc · 같은 오류 · traceback 줄번호 3 개만 +2 (§5 ⑧) |
| `step3_sigma --selftest` · `--selftest-rint` · `rint_t41_census --selftest` | 0 · 0 · 0 | ~1 s | PASS × 3 | 로그 0 줄 차 × 3 |
| am_iface · rrm · t4 · t43 · t2 (전체 핀) | 0 × 5 | 9 · 5 · 1 · 1 · 1 s | **136 · 55 · 8 · 6 · 23** 전부 통과 | 로그 줄 차 0 · 1 (rrm 기록 줄 끝자리 ~1e-15) · 0 · 0 · 0 |

## 4. 판정 숫자 대조 (브리프 목록 · 전체 165 항목 = `verdict_numbers_table.md`)

판정 = 판정문이 찍은 자릿수에서 우리 값이 같은가 (반 단위 안).  Codex JSON 값도 같은 기준.

| 판정문 자리 | 판정문 값 | 우리 값 | 같음? |
|---|---|---|---|
| RCA-01 마지막 이웃 | 31,622.7766 / 100,000 Ω | 31,622.776601683792 / 100,000.0 | 같음 |
| RCA-01 e · e_min | 0.01885983293 · 0.01737177928 | 0.018859832928079 · 0.017371779276130 | 같음 |
| RCA-01 W | 0.419353749 → 0.467828346 (PASS_INFORMATIVE → CONSISTENT_WEAK) | 0.41935374899 → 0.46782834646 · 같은 등급 | 같음 |
| RCA-01 R_hi/R_lo · 64,000 Ω 확인 | 199.9542703 · S 1.6263191459 (−0.2258193 %) | 199.95427034 · 1.6263191459 (−0.2258193 %) | 같음 |
| RCA-02 W | 0.293 → 0.836 | 0.2930476574 → 0.8362390828 · 같은 등급 | 같음 |
| RCA-03 R | 5 → 2 Ω · G 2.5 배 · 가닥 거리 0.1838477631 µm | **우리 직렬 망 독립 계산** 5 → 2 · 2.5 · 0.18384776311 · `segment_cells` 가 (0,0,0) 을 선분 0 · 4 에서 지남 | 같음 ⚠ 탐침 JSON 의 5/2/2.5 는 계산이 아니라 상수 |
| RCA-04 G | 1 / 0.5 S | 1.0 / 0.5 | 같음 |
| RCA-05 G | 1.366013071895 / 5 / 0.238095238095 | 1.3660130718954 / 5.0 / 0.2380952380952 | 같음 |
| RCA-06 | 90.49773756 % · P_SV 4.5351473923e-5 < P_VV 1e-4 · 가드 false | 90.497737557 % · 4.535147392e-5 < 1.0e-4 · false | 같음 |
| **RCA-07 상대 오차** | **−1.88593002409e-4** | **−1.88989686465e-4** | **다름** (상대 0.21 %) |
| RCA-07 info · 첫 CG 반복 · 이어 풀기 반복 · ΔG/G | 0 · 10 · 0 · 0 | 0 · 10 · 0 · 0 | 같음 |
| **RCA-07 판 불균형 · A/B/C** | **9.14779553358e-5 (< 1e-4) · A/B/C pass · ok** | **1.47199e-4 (> 1e-4) · A ✓ B ✗ C ✓ · ok = False** | **다름 (판정값 뒤집힘)** |
| RCA-07 보조 (연결 · 자유도 7) | −0.9037086166 % · A/B/C pass | −0.9037086507 % · A/B/C pass | 판정 같음 · 8 째 자리 다름 |
| RCA-12 | 1.1709917265 / 0.4932649517 · 문턱 3.9967891509 | 1.1709917265 / 0.4932649517 · 3.9967891509 | 같음 |
| RCA-13 | τ_mono 단위 의존 (산술) | 탐침 없음 · 산술 확인 (0.5 > 1e-3 · 0.0005 < 1e-3) | 같음 |
| §4-1 α · K4/K8 · K16 · K32 | 0.0134549613712 · 0 · .015625 · .01171875 | 0.013454961371219 · 0 · 0.015625 · 0.01171875 | 같음 |
| §5-2 dt · 속도 비 | 1.3108617603e-4 · 1.5257138934 | 1.31086176026e-4 (실제 핀 스칼라 블록 exec) · 1.52571389343 | 같음 |
| Part B 시험 | 324 · 138 · 179/324 | 324/324 (Linux 원문) · 138/138 · 179/324 | 같음 |
| Part B 탐침 | 144 · 113 (PASS 8 / REJECT 105) | 144 (기대 밖 0) · 113 (8 / 105 / 예외 0) | 같음 |
| Part B 독립 입력 | 62 (PASS 32 / REJECT 30) | 62 (32 / 30 · 기대 밖 0 · F1 잔여 8) | 같음 |
| Part B 실덤프 | real14 457 / 660 · case15 104 / 119 · `delta_bound_um` 0.002915255888325765 | 같음 (두 덤프 모두 0.002915255888325765) | 같음 |
| RINT2-B-01 | Windows CRCRLF 2 개 | Linux 0 (`410a420a` → `410d0a420d0a`) | 다름 = 예상 (Windows 전용) |

## 5. 차이 전부 (원인 · 판정 영향)

| # | 차이 | 크기 | 원인 (추정 표지) | 판정 영향 |
|---|---|---|---|---|
| ① | RCA-07 주 반례 (`small=True`, 대비 6.59e11) 첫 CG 판 전류 | G 상대 4.0e-7 · 오차 −1.88593e-4 → −1.88990e-4 · 불균형 9.15e-5 → **1.47e-4** | 같은 10 반복 · 같은 행렬 · SciPy cg / NumPy 반올림 차 (SciPy 1.17.1 ↔ 1.16.3 · NumPy 2.4.6 ↔ 2.5.3 — 어느 쪽인지 미분리 · 추정) | **ⓑ 판 균형 실패 → ok False** (Codex 는 ε_I 의 91 % 자리 · 칼날 위). 이 사례만으로는 우리 환경에서 "A/B/C 통과 반례" 가 아니다 |
| ② | RCA-07 연결 보조 · 23 반복 사례 | 상대 3.8e-8 · 4.4e-5 (G) | 같은 원인 | 없음 — 둘 다 우리도 A/B/C 통과 · 오차 −0.9037 % · +5.558e-4 → RCA-07 결론 유지 |
| ③ | search seed 611 | 143,478 / 200,000 표본 (80 s 예산 · nice · 동시 부하) | 벽시계 예산 | 없음 — 최대 오차 표본 57,686 이 예산 안 · 같은 표본 |
| ④ | RINT2-B-01 | 원문 시험 4 단언 (J12P CRLF ×2 · J15P CR · J15P 섞임) | Windows text 쓰기 LF→CRLF 뒤 재치환 | Linux 324/324 = 저자 Linux 주장과 같음 · Windows 전용 확인 |
| ⑤ | gzip 픽스처 SHA (독립 6 · 픽스처 manifest 3) | 컨테이너 바이트 | gzip 헤더 OS 바이트 (우리 3) · zlib | 없음 — 풀면 LF 픽스처와 같은 바이트 (그 SHA 는 Codex 와 같음) |
| ⑥ | 경로 문자열 (`\` ↔ `/` · 절대 경로) | 434 + 396 + … | 환경 | 없음 |
| ⑦ | geometry 2 · registration 2 · rrm 기록 1 줄 | 상대 ≤ 6e-16 · ~1e-15 | LAPACK · libm 끝자리 | 없음 |
| ⑧ | `structure_minimal_replay` traceback 줄번호 | 118/87/72 → 120/89/74 | **Codex 가 최종 탐침을 돌린 `run_review.py` 가 동봉본보다 2 줄 짧다** (초기 overlay 는 93/76/65) | 결과 같음 · 동봉 harness ≠ 실행 harness 바이트 (기록) |
| ⑨ | 봉인 표 (§6) ε_I 구간 | Codex [5.685e-5, 1.342e-4) · 우리 [5.762e-5, 1.239e-4) · 제출 [4.89e-5, 1.146e-4) | 접합 꼴 CG 궤적 환경 의존 | 선택값 같음 (rtol 1e-12 · ε_I 1e-4) · 24 행 증서 깃발 전부 같음 |

판정값 (PASS/REJECT · 등급 · 증서 ok · 시험 통과 수) 차이 = **①의 1 건** (+ ④ 는 예상된 Windows 전용).

## 6. 추가 대조 (브리프 밖 · 가벼움 · 판정문 서술 확인용)

| 대조 | 결과 |
|---|---|
| Codex 구조 탐침을 **2b9efa253 모듈**로 (격리 harness 사본 `part_b_old2b9/`) | 144 중 기대 밖 PASS **10 = 헤더 공격 10 건 전부** (`*_rows_no_boundary` · `*_box_no_boundary` · `*_rows_repeated_marker` · `*_box_repeated_marker` · `*_rows_marker_at_end` × atom/contact) → 판정문 *"이전 header 거짓 통과 10개 모두 거부"* 확인 |
| Codex 수치 탐침을 2b9efa253 모듈로 | **PASS 15 / REJECT 98** → 핀 8/105 · 전환 7 = **unicode 1 + overflow 6** (`derived_nonfinite`) → 판정문 *"이전15/98에서 unicode1+overflow6 수정"* 확인 |
| 핀 `step3_conv_cert.py --table` (24 행 봉인 표 · 1 m 55 s) | rtol_stop 1e-12 · ε_I 1e-4 · good 20 / bad 4 = Codex 와 같음 · 행별 cert/A/B/C/prod_ok/info **24/24 같음** · 반복 수 다른 행 11 · 구간 [5.7619e-5, 1.2388e-4) (§5 ⑨) |
| 탐침 JSON `warm_candidate` (설명용 25 %) · `valid_zero` | 정확히 같음 (영값 = A ✓ B ✗ C ✗) |

## 7. 실행 못 한 것 · 안 한 것

| 대상 | 이유 · 대신 한 것 |
|---|---|
| `part_b/verify_fullpin.py` | Codex 의 `staged_source` overlay 가 묶음에 없음 → 그 결과 JSON 의 21 파일 SHA 를 우리 소스와 직접 대조 (21/21) |
| `part_b/package_baseline.py` | Codex 작업공간 폴더에서 복사하는 포장 도구 → git 재구성 + MANIFEST 36/36 대조로 갈음 |
| `geometry/search_cg_results.json` (eps 없는 100,000 표본 검색) | 만든 스크립트가 묶음에 없음 → 재실행 불가 · 그 표본 76,368 은 `convergence_probes` 의 `small=True` (/16384 축척) 로 재실행됨 |
| `test_step3_conv_cert.py` K1–K9 전체 (판정문 25/25) | 브리프 목록 밖 · 무거움 (10-20 기록 2,305 s) → 봉인 표 (`--table`) 만 돌림 (§6) |
| `numeric_review.py --baseline` (dcb97f1ed 모듈) | 판정문이 쓰지 않음 · 대신 2b9efa253 모듈로 현행 모드 (§6) |
| `part_b/preliminary_overlay_evidence/` 재실행 | Codex 스스로 "최종 실행과 합산하지 않음" |
| Windows `resource` shim · `--lf-test-writer` | Linux 에서 비활성 (`resource` 있음) · LF 어댑터는 no-op 로 실행만 (324/324) |
| 무거운 실침대 · GPU | 판정문도 안 함 |

## 8. 바꾼 것

- **경로 상수만** (`path_constant_changes.diff` · 사본 `probe_copies_with_path_changes/`): 결과 JSON 4 개 출력 경로 → 이 폴더 · Codex 작업공간 `deps` 경로 3 곳 → 존재하지 않는 `rint2rev_repro/_absent_deps/…` (원래도 우리 쪽에 없음 · 섀도잉 방지). 계산 · assertion 줄 무변경.
- `run_review.py` 의 탐침 경로 치환 (`part_b_adapted/`) 은 Codex harness 자신의 것 그대로.
- `-I` 는 스크립트 폴더를 `sys.path` 에서 뺀다 → `from run_review import …` 를 쓰는 두 스크립트는 `tools/run_with_dir.py` (그 폴더만 `sys.path[0]` 에 넣고 `__main__` 으로 실행) 로 돌림.
- `run_review.py` 가 띄우는 자식 프로세스는 원 코드대로 `-I` 없음 → 환경 `PYTHONNOUSERSITE=1` · `PYTHONPATH` 없음으로 대신 격리 (자식 `sys.path[0]` = `part_b/` = 읽은 파일만).
- 작업 사본의 `part_b/evidence` (Codex 사본) → `part_b/evidence_codex_copy` 로 옮기고 우리 실행은 빈 `evidence/` 에 (대조는 늘 원본 `x/`).

## 9. 이 폴더

| 파일 · 폴더 | 내용 |
|---|---|
| `README.md` | 이 문서 |
| `verdict_numbers_table.md` · `verdict_numbers.json` | 판정 숫자 165 항목 전부 (우리 · Codex JSON · 판정문) |
| `*_results.json` (4) · `*.log` · `run_review_*.stdout` | Part A 탐침 우리 출력 · 화면 로그 · Part B harness 출력 |
| `part_b_evidence/` | Part B 우리 출력 전부 (로그 · harness 행 · `.imports.json` · 탐침 JSON) |
| `part_b_adapted/` · `part_b_old2b9_*` | harness 경로 치환본 · 2b9efa253 추가 대조 |
| `compare/` | 키별 대조 (`*.cmp.json/txt`) · 로그 대조 (`log_*.json` · `full_log_and_imports.json`) · 봉인 표 대조 · overlay 21 |
| `source_rebuild_report.json` · `partb_setup_report.json` | 입력 재구성 영수증 (1,161 · 36 · 15) |
| `extra_step3_conv_cert_table.log` | 봉인 표 화면 |
| `tools/` | 재구성 · 대조 · 실행 도구 (우리 작성) |

2 MB 넘는 파일 없음 · 탐침이 만든 합성 픽스처 (`part_b/tmp` 3.8 MB · 결정적 재생성) 는 넣지 않음 — SHA 는 `part_b_evidence/structure_fixture_manifest.json` · `independent_join_checks.json`.
`source/` 사본 (65 MB) · 2b9efa253 트리 · 작업 사본은 끝나고 지움 — 다시 만들려면 `tools/rebuild_source.py` · `tools/setup_partb.py`.
