# 주장 대조표 — `codex_rint2_codepkg_review_request_20261113.md` (Codex 봉인 전 묶음 1/2 · 2026-11-13 초안)

> 요청서의 숫자 · 전칭 ("N/N" · "같음" · "전부" · "닫힘" · "없음") 을 하나씩 근거와 맞춘 표 (CLAUDE.md "Codex 요청 전 사전 공격 리뷰" ①).
> 근거 표기: `경로:행` = 코드 핀 `56f4cfbb1` 의 리포 파일 (리포 뿌리 기준) · `$ 명령 → 출력` = 리포 뿌리에서 읽기 명령 · `<기록>/…` = 기록 묶음
> `docs/reviews/rint2_codepkg_20261113/rint2_codepkg_records_20261113.tgz` 안 경로 · `extra/…` = ZIP 의 extra (우리 다시 돌림 · 블록).
> 판정: ✓ = 근거와 같음 · **고침** = 초안에서 틀려 고쳤다 (무엇을) · [미확인] = 근거 없음 → 요청서에 표지 · [추정] = 추론 (요청서에 표지).

## 0. 요약

| 항목 | 수 |
|---|---|
| 대조한 주장 (아래 행) | 147 |
| 초안에서 고친 것 (**고침** 행) | 21 |
| 요청서의 [미확인] 표지 (§9 의 메타 언급 뺌) | 13 |
| 요청서의 [추정] 표지 | 3 |

## 1. 머리 (1–5 줄)

| 주장 | 근거 | 판정 |
|---|---|---|
| 1저자 11-12 결정 = Q2 + Q11 한 코드 묶음 | `docs/reviews/rint2_time_reestimate_20261111/README.md:428` 절 · 436 (Q2) · 445 (Q11 "한 묶음") | ✓ (절 이름 · 행 넣음 = **고침**) |
| 코드 · 시험 16 커밋 | `$ git rev-list --count a0455e90b..8ace86a82` → `16` | ✓ |
| 비교 기준 `a0455e90b` 의 `step3_sigma.py` = `11a794674` 와 sha256 `8d428ff5…` 같음 | `$ git show <c>:scripts/step3_sigma.py \| sha256sum` → a0455e90b · 11a794674 둘 다 `8d428ff5c6c214ea…` | ✓ |
| 내부 반박 리뷰 세 회 + 마지막 좁은 고침 · Codex 아님 | 커밋 제목 (`88ece7636` · `27ef82d24` · `8ace86a82` "마지막 좁은 고침 3 회차 (내부 반박 리뷰 재확인 2 · Codex 아님)") · `docs/reviews/rint2_codepkg_20261113/README.md:8` | ✓ |
| 1저자 11-10 운영 결정 (반박 리뷰 = 내부) | CLAUDE.md 11-10 줄 "★ 1저자 11-10 운영 결정 = Codex 토큰 소진 → … 내부 반박 리뷰" | ✓ |
| 회차 ⑥ 검토 핀 `aec8ca2f6` · "전체 HOLD" 그대로 | `docs/reviews/codex_review_rint2_rr_round6_20261110.md:3` (검토 핀) · 5 ("전체 HOLD 유지") · 169 | ✓ |

## 2. §0 닫는 것 / 닫지 않는 것

| 주장 | 근거 | 판정 |
|---|---|---|
| S0 다시 = kgy · 11-13 01:47:26 UTC 시작 · 결과 미열람 | 리포 · 기록에 없음 (본 세션 전달) | [미확인] 표지 |
| 봉인 숫자 maxiter ≥ 3,000,000 · 시간 상한 · 최대 시도 수 = 1저자 11-12 Q3 · Q4 | `rint2_time_reestimate_20261111/README.md:437–438` | ✓ |
| `run_probe6.sh` 가 시도 1 · 2 짝만 안다 (236–251) | `docs/reviews/rint2_probe6_prep_20261110/tools/run_probe6.sh:236` (`p6log_a1_*`) · 251 ("registered pair 1 -> 30000, 2 -> 1500000") | ✓ |
| 러너 env 의 `CJUNC*` 를 지운다 (430–438) | 같은 파일 430 (머리 주석) · 434 (`…\|CJUNC*\|…`) · 438 (`done`) | ✓ |
| 회차 ⑥ 남은 조건 = 현장 자격 부분 · Q5 순서 보완 | 판정문 5 줄 ("현장 자격 §7④ … 부분 수용" · "Q5 순서 요약은 보완 필요") · 28–29 | ✓ |
| `RR6-01` · `02` = 남은 조건 | `docs/reviews/findings.json` → RR6-01 · RR6-02 status `claimed_fixed` | **고침** — 초안은 "남은 조건" 에 넣었다 → "claimed_fixed · Codex 확인 전" 으로 |
| 열린 원장 `P6R3-01` · `02` · `03` · `05` · `RIMPR-04` · `RCA-11` | findings.json → 여섯 다 `open` (P6R3-04 = claimed_fixed · 그래서 뺐다) | ✓ |
| 게이트 배선 = `check_all.sh` 새 단계 넷 + 머리 한 줄 | `$ git diff a0455e90b 56f4cfbb1 -- scripts/check_all.sh \| grep '^+\s*run '` → 4 줄 · `check_all.sh:19` (GIT_DROP_SH) | ✓ |
| `check_kgy_py38.sh` 17 묶음 | `grep -cE '^\s*run ' scripts/check_kgy_py38.sh` → 17 · 72 줄 "17 묶음 통과" | ✓ |
| 두 기계 조립 = 1저자 11-12 Q10 | `rint2_time_reestimate_20261111/README.md:444` | ✓ |

## 3. §1 보내는 것

| 주장 | 근거 | 판정 |
|---|---|---|
| 시험 ZIP = 파일 64 (repo/ 51 · extra/ 11 · PIN.txt · ZIP_MANIFEST.tsv) · 3,356,303 B · 두 번 바이트 같음 | `make_zip.sh 56f4cfbb1 …TEST_b.zip` 출력 "[zip] 파일 64 (repo/ 51 · extra/ 11 …) · repo/ blob 대조 51/51 같음" · "3356303 B · sha256 f4712f78…" · 두 번째 빌드 `cmp` → 같음 · `zipfile.testzip()` → None | ✓ (초안 63 · 3,352,242 B = ⑥ 시도 2 README 를 더하기 전 → **고침**) |
| 바뀐 25 파일 = 표의 목록 | `$ git diff --name-only a0455e90b 8ace86a82` → 25 줄 (표의 12 + 시험 11 + S0 등록 2 와 같음) | ✓ |
| 새 파일 넷 (시험) + `cjunc_store.py` (새) | `$ git diff --name-only --diff-filter=A a0455e90b 8ace86a82` → 7 = cjunc_store · 시험 넷 · S0 등록 둘 | ✓ |
| 기록 tgz 888,018 B · sha256 `887566e8…` | `stat -c %s` → 888018 · `sha256sum` → `887566e8eb7a…` = `SHA256SUMS` | ✓ |
| MANIFEST 233 + 자신 = 234 파일 | tgz 멤버 234 (전부 파일) · MANIFEST.tsv 234 줄 = 머리 1 + 233 · MANIFEST 자신은 목록에 없음 · 기록 README "파일 233" = 목록 수 | ✓ |
| ZIP 밖 근거 E2 = `…/s0_stage1_kit_SBE_vgcf100.json:397` `n_instances` 117583 · 6,286,674 B | 그 행 `"n_instances": 117583,` · `find -printf %s` → 6286674 | ✓ |
| 게이트 서술 = 인계 문서 11 줄 | `docs/handoff_return_to_stoic_knuth_20261113.md:11` "(게이트 = 대피 세션이 인계 커밋에서 두 조각 통과 …)" | ✓ (서술만 · 출력 원본 없음) |

## 4. §2 무엇이 바뀌었나

| 주장 | 근거 | 판정 |
|---|---|---|
| 16 커밋 · 25 파일 · +5,727 / −60 | `$ git diff --shortstat a0455e90b 8ace86a82` → "25 files changed, 5727 insertions(+), 60 deletions(-)" | ✓ |
| `30a9e937c` 기록 · `56f4cfbb1` 인계 = 코드 무변경 | `$ git diff --stat 8ace86a82 56f4cfbb1 -- scripts webapp docs/reviews/rint2_probe6_prep_20261110 docs/reviews/rint2_s0_store_probe_20261112` → 빈 출력 | ✓ |
| 커밋마다 끝 줄 `cherry picked from` | 16 커밋 본문 `grep -o 'cherry picked from commit …'` → 16 / 16 (ebb0e9f80 … 8b59b9618) | ✓ |
| 회차별 커밋 · 내용 (표 일곱 줄) | 커밋 제목 · 본문 (`650ecaae5` G1–G7 · T0–T11 · P · R · C · Z0–Z6 · `95cf418ee` 결함 둘 · `e32ac7f8e` 제목 · `853672840` 제목 RCP 목록 · `e4c51669f` RCP-02 · `882f03a8d` 186 → 187 · `ab33150e2` G6 넷 → 일곱 · `27ef82d24` RCP3) | ✓ (RCP3 요약에 01 = S0 시험 고정물 git 빠짐 → **고침**) |
| `cjunc_store.py` 889 줄 · 행 범위 15 개 | `wc -l` → 889 · 각 행 `sed -n` 확인 (85 `CODE_MODULES` · 391 `def machine_fp` · 412 `def code_file` · 427 `def env_paths_fp` · 470 `def _start_record` · 484 `_START =` · 487 `def code_drift` · 142 `class _Walk` · 242 `def _no_overlap` · 548 `def __init__` · 580 `def key_parts` · 600 `def _read` · 615 `def _content` · 651 `def _publish` · 734 `def get_or_build` · 804 `def _read_members`) | ✓ |
| `ca_ext_cjunc.py` 35–36 (cjunc_store 먼저) · `payload_prepare` 219–270 | 35 `import cjunc_store as CJS` · 36 `import carbon_junction as CJ` · 219 `def payload_prepare` · 242 `store.get_or_build` · 269 `out['store'] = _st` · 270 `return out` | ✓ |
| payload `--step3-cjunc-store` 1621 · `_cjunc_entry_contract` 912–1023 (세 사유) · 본 길 2491–2509 | 1621 `ap.add_argument('--step3-cjunc-store'` · 912 `def _cjunc_entry_contract` · 938 · 942 · 949 (`STORE_GRAPH_ONLY` · `STORE_RASTERIZE_ONLY` · `STORE_PATH`) · 2506 `S2_CJUNC_STORE\|INCONSISTENT\|` · 2509 `outcome_line` | ✓ |
| 러너 `CJUNC_STORE` 583–621 | `sdcp_gain_vox015_8arm.sh:583` (주석) · 588 `CJS_FLAG=""` · 620 · 621 `fi` | ✓ |
| 사슬 `cjunc_store_dir_problem` 5614–5637 · `env_delta` 5658–5662 · 5852 · 6597 · 6801 · 8629–8639 | 각 행 확인 (5852 `d.pop('CJUNC_STORE', None)` · 8629 `--cjunc-store` · 8639 `ap.error`) | ✓ |
| CLI 회계 `run_contract.py:142` (mode) · 규율 검사기 `check_method_discipline.py:937` | 142 `'--step3-cjunc-store': ('mode', None)` · 937 `'CJUNC_STORE')` | ✓ |
| 사슬 `CODE_FILES` 19 → 20 | AST: a0455e90b `CODE_FILES` 19 (335–339) · 56f4cfbb1 20 (335–340 · 340 = `'cjunc_store.py'`) | ✓ (초안 "336–341" → **고침**) |
| `_solve_cg` 535–629 · `LinearOperator` import 574–578 · 586–587 · 600–608 | 535 `def _solve_cg` · 574 `try:` · 575 import · 577 `'no_linop'` · 578 `raise` · 586 `_dinv` · 587 `Mg = _LinOp(…)` · 600 `if REQUIRE_GPU and _gpu_why == 'no_linop'` · 608 글 끝 · 629 `return _r` | ✓ (초안 "573–578" → **고침**) |
| 기록 `precond` 'jacobi' 그대로 · 새 기록 키 없음 · CPU 길 그대로 | `$ git diff a0455e90b 56f4cfbb1 -- scripts/step3_sigma.py` → 더한 것 = 지역 변수 `_gpu_why` · import try · `_dinv` · `Mg` · REQUIRE_GPU 글 (GPU 가지 안) · 기록 키 줄 없음 · G3 "LAST_BACKEND … 글자 그대로 · 새 키 없음" PASS | ✓ |
| git 환경 행 범위 (run_contract 1464–1534 · payload 607–743 · 사슬 948–3088 · census 901–905 · findings 744–750) | 각 행 `sed -n` 확인 (1464 `GIT_DROP_NAMES` · 1469 `GIT_DROP_SH` · 1477 `def git_env` · 1484 `def drop_git_env` · 1498 `def git_fixture_env` · 1519 `def normal_path_problem` · 607 `def _exec_env` · 678 `def _code_sha` · 948 `def git_identity` · 1767 `def plan_commit_problem` · 3069 `def ledger_git` · 3082 `def _git_top` · 901 `def _git` · 744 `def _git_env_clean`) | ✓ |
| selftest RCPT-sha 임시 저장소 (꼭대기 확인 뒤만 쓰기) | `run_contract.py:2435` (절 머리) · 2464 ("RCPT-sha-tmp 임시 저장소 꼭대기 = 임시 폴더 (쓰기 전 확인 …)") · 2471 | ✓ (행 넣음) |
| 셸 꼴 `check_all.sh:19` · `check_kgy_py38.sh:12` · 러너 1082 | 세 행 = `for _gv in $(compgen -e); do case "$_gv" in (GIT_DIR\|…` | ✓ |
| 시험 모듈 = 불러올 때 지움 | `grep -n "drop_git_env()"` → scripts 시험 여덟 (모듈 머리) + `test_probe6_read.py:91` · `test_git_env_isolation.py:431` `G6_MODULES` = 여덟 (probe6 포함 · gpu_precond 없음) · `test_step3_gpu_precond.py:45` 은 G4 가 봄 | **고침** — 초안 "여덟" → "아홉 (G6 여덟 + gpu_precond = G4)" |
| 게이트 단계 333 · 334 · 336 · 341 | 네 행 = `run 'step3_gpu_precond …'` · `'cjunc_store …'` · `'cjunc_store_e2e …'` · `'git_env_isolation …'` | ✓ |

## 5. §3 보장 B1–B12

| 주장 | 근거 | 판정 |
|---|---|---|
| B1 열쇠 칸 (format · model · schema · code · env · machine · sid · lo · vox · inputs · thresholds) | `cjunc_store.py:584–587` | ✓ ("모델 판" 더함 = **고침**) |
| B1 문턱 열 칸 (s_min 포함) | `ca_ext_cjunc.py:48–49` `REGISTRY_THRESHOLD_KEYS` → 10 (`s_min_um` 포함) · 237 `_rthr` | ✓ |
| B1 T4 넷 · 27 갈래 · T5h · T8 · T14 · T14a–d | `extra/runs_56f4cfbb1/test_cjunc_store.log` (T4 네 줄 · "열쇠 결속 27 갈래" · T5h · T8 · T14 · T14a–d 줄) | ✓ |
| B1 고치기 전 → 뒤 | `853672840` 본문 3 줄 "store 40 PASS · 14 FAIL → 54/54" · `0f2ecaa05` 5 줄 "(고치기 전 판 = 40 PASS · 14 FAIL · 실패 = 새 검사뿐)" | **고침** — 초안 "T14: 40 · 14 → 54/54" (T14 하나의 수처럼 적음) → "저장본 시험 40 PASS · 14 FAIL (실패 = 새 검사뿐) → 54/54" |
| B1 한정 = BLAS · SIMD 실행 env 는 열쇠 밖 | `cjunc_store.py:576` env = `env_unit_now()` + `env_paths_fp()` (판 글자 + 설치 자리 지문) · `env_paths_fp` 머리 428–430 | ✓ |
| B2 T6 7 갈래 · T6b · P3 | 시험 로그 T6 ("못 읽음 7 갈래") · T6b · P3 | ✓ |
| B2 0/21 → 46/46 · 넘겨받은 판 33 · 8 | `650ecaae5` 7 줄 "고치기 전 판 0/21" · `95cf418ee` 24 줄 "0/21 → 46/46" · 16 줄 "33 PASS · 8 FAIL" | ✓ |
| B2 한정 = 덮어쓰지 않음 → 그 열쇠 팔마다 다시 짓기 | `cjunc_store.py:774` `'unreadable_rebuilt'` "파일 그대로 · 덮어쓰지 않음 · 운영자 확인" · 발행 = `os.link` (덮어쓰기 없음) | ✓ (초안 "다시 짓는 동안 남는다" → 뜻 분명히 = **고침**) |
| B3 T7 17 갈래 · T7b · T7c · T11 8 갈래 · T12 · P4 · P1 일곱 · P1b · R1 열셋 · C1 열넷 | 시험 로그 각 줄 ("어긋남 17 갈래" · "T11 8 갈래" · "입구 거부 일곱" · "ABORT 열셋" · "거부 열넷") | ✓ |
| B3 2 회차 51 · 11 → 62/62 | `410920bcb` 14 줄 "test_cjunc_store 51 PASS · 11 FAIL" · `5eba3628e` 17 줄 "51 → 62/62" | ✓ |
| B3 한정 = 경로 기준 · 마지막 성분 | `cjunc_store.py:55–56` | ✓ |
| B4 단일 작성자 꼴 | `cjunc_store.py:673` (O_EXCL 0600) · 713–717 (폴더 fsync) · `_publish` 651–732 · T9a–c · T10a–b 로그 줄 | ✓ |
| B4 한정 = 링크 수 안 봄 · 임시 파일 남음 · 공유 파일계 미검토 | `cjunc_store.py:819` ("링크 수는 보지 않는다") · T10a 로그 "남은 것 = 임시 파일뿐" · `<기록>/review/review_codepkg.md` RCP-07 · 공유 파일계 = 우리 서술 (코드 · 시험에 NFS 꼴 없음 · `grep -n NFS scripts/cjunc_store.py` → 0) | ✓ (임시 파일 줄 더함 = **고침**) |
| B5 켬 ↔ 끔 바이트 같음 (P2 · P5 · R2 · T5c · T5d · Z1–Z6) | 시험 로그 P2 ("팔 JSON 바이트 같음 셋") · R2 ("팔 이름 · 팔 JSON 바이트 · 영수증 바이트 · OUTDIR") · `scripts/test_cjunc_store_e2e.py:10–18` (Z1–Z6 정의) | ✓ (Z 목록 풀이 다듬음) |
| B5 e2e Z0 실패 → 6/6 · 511.4 s · 412.4 s | `650ecaae5` 9 줄 "고치기 전 판 = Z0 실패" · `<기록>/logs_r5/py311/_summary.txt` "6 PASS · 0 FAIL (511.4 s)" · `<기록>/logs_r5/kgy/cjunc_store_e2e.log` 끝 "(412.4 s)" | ✓ |
| B5 한정 = 합치기 시험 없음 | `scripts/test_cjunc_store_e2e.py:20–21` | ✓ |
| B6 봉인 원천은 저장본을 읽지 않는다 | `rint_r_chain.py:5852` · 시험 C3 · Z4 (`test_cjunc_store_e2e.py:13` · 252) · payload 938 · R1 ("조립만") | ✓ |
| B6 한정 = 1저자 Q-A "한정 유지" | `<기록>/amend_drafts.md:30` "⬜ 1저자 질문 Q-A" · `<기록>/notes.md:169` "한정 = 03 (+ 1저자 Q-A)" · `cjunc_store.py:37` "대조 길 = 1저자 결정 · … (한정 그대로)" — 답 기록 없음 | **고침** — 초안 "1저자 11-12 Q-A = 한정 유지" (근거 없음) → "Q-A 열림 · 지금 한정 그대로" |
| B7 stat 신원 [dev · ino · size · mtime_ns · ctime_ns] · 두 자리 다시 셈 | `cjunc_store.py:449` · 753 (시작) · 691 (발행 직전) · `self.code != _sc` 754–756 | ✓ |
| B7 T15a–m (13) · P6 · P6b | 시험 로그 T15a … T15m = 13 줄 · P6 · P6b | ✓ |
| B7 13 · 6 → 19/19 · 지금 70/70 | `88ece7636` 23 줄 · `27ef82d24` 22 줄 · `extra/runs_56f4cfbb1/test_cjunc_store.log` "70 PASS · 0 FAIL (93.2 s)" | ✓ |
| B8 가짜 = cupy 12.3.0 `cg` · `_make_system` | `scripts/test_step3_gpu_precond.py:21` | ✓ |
| B8 G1 · G1r · G2 · G3 24 짝 · G4a–c · G7 | `extra/runs_56f4cfbb1/test_step3_gpu_precond.log` (G3 줄 "… · 24 짝") | ✓ |
| B8 10/13 → 15/15 · 18/19 → 19/19 | `650ecaae5` 5 줄 · `95cf418ee` 5 줄 · `0f2ecaa05` 15 줄 · `853672840` 3 줄 | ✓ |
| B9 G5 · G6 · G6b | 같은 로그 | ✓ |
| B10 적대 꼴 넷 · G1–G8c | `scripts/test_git_env_isolation.py:9–10` · 로그 19 줄 (G2 적대 "GIT_DIR · +WORK_TREE+INDEX_FILE · OBJECT_DIRECTORY+COMMON_DIR · 훅 꼴") | ✓ |
| B10 4 · 6 → 10/10 · 9 · 1 → 10/10 · 9 · 8 → 17/17 → 19/19 | `410920bcb` 14–15 · `5eba3628e` 17 · `ab33150e2` 11 · `2bae2d936` 11 · `88ece7636` 20 · `27ef82d24` 22 · `8ace86a82` 18–19 | ✓ |
| B10 격리 변수 셋은 산다 | `run_contract.py:1464–1466` 지우는 목록에 CEILING · NOSYSTEM · GLOBAL 없음 · G7a · G7b PASS | ✓ |
| B11 바탕 `af3cce37b` ↔ `a0455e90b` scripts 차이 = 믹서 둘 | `$ git diff --name-only af3cce37b a0455e90b -- scripts webapp` → `mixer_precal_observe.py` · `test_mixer_precal_observe.py` | ✓ |
| B11 끝 8b59b9618 (작업 트리 커밋 · 원격에 없음) = 반입 `8ace86a82` | `8ace86a82` 본문 끝 "cherry picked from commit 8b59b9618…" | ✓ |
| B11 payload 넷 + 러너 · rc 0 · σ_e 같음 · 다른 잎 = 코드 신원뿐 | `<기록>/logs_r5/off_vs_base_py311.log` 1–32 줄 (요약 `{"payload/b6/cj": [0, 0, 3], … "runner": [0, 0, 6]}` · 다른 잎 = code_sha · loaded_project_modules (8 ↔ 9 · 10 ↔ 11) · project_module_digest · receipt code_sha · receipt_digest) · `_py38.log` 같은 요약 줄 | ✓ |
| B11 "접합 켬 +1 = cjunc_store" | `ca_ext_cjunc.py:35` 가 cjunc_store 를 부른다 — 로그는 수만 보인다 (모듈 이름은 안 찍음) | [추정 · 코드로 본 것] — 요청서 글 그대로 둠 (낮은 위험) |
| B12 run 줄 187 · 183 → 186 → 187 | `grep -cE '^\s*run '` → a0455e90b 183 · e4c51669f 186 · 882f03a8d 187 · 56f4cfbb1 187 · `e4c51669f` 본문 6 줄 "183 → 186" · `882f03a8d` 3 줄 "186 → 187" · `<기록>/logs_r5/check_all_split.log:1` "원문 run 187" | ✓ |
| B12 `56f4cfbb1` 게이트 두 조각 fail 0 | 인계 문서 11 줄 서술뿐 · 출력 원본 리포 · 기록 밖 | ✓ 리뷰 핀 커밋에서 진행 기록 `docs/session_20260923_progress.md` 11-13 [Rint ②] 줄로 (두 조각 fail 0 · 출력 원본은 리포 밖) |
| B12 kgy 판 13 → 16 → 17 | `git show <c>:scripts/check_kgy_py38.sh \| grep -cE '^\s*run '` → 13 · 16 · 17 | ✓ |

### 변이 문단

| 주장 | 근거 | 판정 |
|---|---|---|
| 구현 판 89 전부 · 겹 방어 3 (W6b · P5 · N3c) | `<기록>/notes.md:77–79` · 103–104 | ✓ |
| 1 회차 뒤 리뷰어 31 → 30 + MS7 · 구현 107 → 104 + 3 · F1–F18 18/18 · Z 3/3 | `<기록>/notes.md:145–146` · 150–151 · 157 · 171 | ✓ |
| 2 회차 뒤 N 21/21 · H 32 → 29 + 3 · W14 → `7173083c4` 뒤 잡힘 | `<기록>/notes.md:206–213` (W14 → 609d78ca4 = `7173083c4` 의 원 sha) · 237 | ✓ |
| 3 회차 J1–J32 → 31 · J22 겹 방어 · 3.11 · 3.8 같음 | `<기록>/notes.md:289–291` · `docs/reviews/rint2_codepkg_20261113/README.md:10` | ✓ |
| J21 이 T15i 에서도 잡힘 (inode 번호 재사용) · 결정적 판 T15l | `<기록>/notes.md:291` | ✓ (다른 파일계 = [추정] 표지) |

## 6. §4 내부 반박 리뷰

| 주장 | 근거 | 판정 |
|---|---|---|
| 1 회차 대상 `af3cce37b..2f97617ef` · P1 1 · P2 3 · P3 7 (RCP-01–11) | `<기록>/review/review_codepkg.md:1` · 9 ("## 1. 지적 (P1 1 · P2 3 · P3 7)") · 13–23 (RCP-01 … 11) | ✓ |
| 1 회차 처분 (고침 01 · 02 · 05 · 06 · 08 · 09 · 10 · 11 / 한정 03 · 07 / 단계 04) | `<기록>/notes.md:169` (글자 그대로) · RCP-09 = 시험만 (`0f2ecaa05` 18 줄 G4) | ✓ (09 = 시험만 표지 더함) |
| 2 회차 대상 · 닫힘 7 · 일부 3 · 안 닫힘 1 · 새 P1 0 · P2 2 · P3 4 | `<기록>/review/rereview_codepkg.md:1` · 20 · 24–34 · 36 | ✓ |
| 2 회차 리뷰어 변이 21 (20 잡힘) · GIT_DIR 샘 | 같은 파일 47 줄 · 7–12 줄 (사고) | ✓ |
| 고친 쪽 N 21/21 (깨끗한 환경) | `<기록>/notes.md:206–207` ("GIT_DIR 없음" · "X1–X21 (= N1–N21) 21/21") | ✓ |
| 3 회차 대상 · 닫힘 6 · 부분 3 · 안 됨 0 · 새 P1 0 · P2 1 · P3 4 | `<기록>/review/recheck2_codepkg.md:1` · 11 · 25 | ✓ |
| 기록 README "RCP-01–08" ↔ 원문 01–11 | `docs/reviews/rint2_codepkg_20261113/README.md:8` ↔ review 13–23 | ✓ (불일치 그대로 적음) |
| RCP · RCP2 · RCP3 원장 줄 없음 | findings.json `id` 접두 'RCP' → 0 · SELF-169 = claimed_fixed | ✓ |

## 7. §5 측정 블록

| 주장 | 근거 | 판정 |
|---|---|---|
| 등록 블록 275 줄 · md5 `39c4b975…` | `wc -l` → 275 · `md5sum` → `39c4b975ebd32ff3…` | ✓ |
| 1저자 11-12 밤 Q-B (가) · T1–T3 채택 | `docs/reviews/rint2_s0_store_probe_20261112/README.md:9` | ✓ |
| S0 일곱 가운데 셋 바뀜 · 원장 코드 둘은 `f47bde0f6` 뒤 그대로 | AST `S0_SAME_FILES` 7 (`rint_r_chain.py:345–346`) · `$ git diff --name-only f47bde0f6 56f4cfbb1 -- <일곱>` → ca_s0_census · mpm_webapp_payload · step3_sigma · `f47bde0f6..a0455e90b` → 빈 출력 | ✓ |
| ca_s0_census 변경 = `_git` git 환경만 | `$ git diff a0455e90b 8ace86a82 -- scripts/ca_s0_census.py` → `_git` 에 `env=_RC.git_env()` + 주석 | ✓ |
| 사본 = 두 줄 (30 · 34) | `diff <등록> extra/kgy_1_s0_rerun_block.txt` → `30c30` PIN · `34c34` BR | ✓ |
| 등록 블록 BR = stoic · 원격 추적 ref `af3cce37b` · 관문 56 줄 | 등록 블록 34 `BR=claude/stoic-knuth-NObVQ` · 56 "PIN is not the tip of $BR after the fetch" · `$ git rev-parse --short=9 origin/claude/stoic-knuth-NObVQ` → `af3cce37b` (로컬 원격 추적 ref · fetch 안 함) | ✓ (그 뒤 본 세션 앞당김 = [미확인] 표지) |
| 안쪽 md5 둘 그대로 | 등록 README 11–12 줄 (`86e9bf4b…` · `ff385531…`) · 사본 ↔ 등록 차이 = 두 줄뿐 → heredoc 바이트 같음 | ✓ |
| 사본 ASCII · 탭 · CR · 느낌표 0 · `bash -n` | `grep -c` → 탭 0 · CR 0 · `!` 0 · 비 ASCII 0 · `bash -n` rc 0 | ✓ |
| 감싸개 ①–⑤ · 같은 원장 객체 돌려줌 | 등록 블록 75–80 줄 | ✓ |
| E1–E4 · instance 117,583 | 등록 README 21–22 줄 · JSON 397 줄 | ✓ |
| T1–T3 문턱 값 | 등록 README 30–32 줄 | ✓ |
| E3 어긋남 처분 | 등록 README 34–35 줄 | ✓ |
| 멈춤 목록 · 감시 셸 30 s | 등록 README 48–50 줄 · 블록 270 줄 | ✓ |
| 약 1.5 h | 등록 README 21 줄 (11-08 실측 5,383 s) · 블록 273 줄 "about 1.5 h" | ✓ |
| GPU: 옛 `8d428ff5…` · 새 `859310da…` | 위 sha256 명령 · 블록 `--old-sha 8d428ff5…` · `make_zip.sh` 관문 (새 sha = 핀의 파일) 통과 | ✓ |
| 298³ = 26,463,592 | 산술 298 × 298 × 298 = 26,463,592 · 벤치 README 16 줄 "n 26,463,592" | ✓ |
| 전도도 10^−1..10^1 · 시드 20261112 · maxiter 60,000 · 상한 5,400 s · rtol 1e-12 · 1e-14 · 200 반복 · 1e-300 | GPU 블록 하네스 156–162 줄 (`--logc 1.0` · `--seed 20261112` · `--rtol` · `--rtol-resolve` · `--maxiter 60000` · `--short-iters 200`) · 58–66 줄 (log-uniform 10^−logc..10^logc) · 194 줄 (`tiny = 1e-300`) · 7 · 243 줄 (`timeout 5400`) | ✓ |
| 하네스 md5 `acfeb4b4…` | `make_zip.sh` 관문 (heredoc md5) 통과 · 블록 243 줄 | ✓ |
| 두 모듈 sha256 관문 = 하네스 175–176 | 블록 175–176 줄 | ✓ |
| 블록은 fetch 하지 않는다 | 블록 6 줄 (머리 주석) · 실행 줄에 `fetch` 없음 | ✓ |
| A / C = 3.40 gabia · 3.79 kgy | `bench/results_20261112/README.md:12–14` (3.397 · 3.795 · 3.794) | ✓ |
| 11-12 kgy GPU 다른 부하 (util 83–93 %) | 같은 README 13–14 줄 | ✓ (초안 "지금 부하" [세션 메모] → **고침**: 11-12 값은 근거 · 지금 = [미확인]) |
| ⑥ 시도 3 · 4 = (나) 결정 | `<기록>/amend_drafts.md:202` "⬜ 1저자 결정 (가) · (나) · 권고 (나)" — 고른 기록 없음 | [미확인] 표지 (초안 "1저자 = (나) 권고대로" → **고침**) |
| 한도 권고 1,500,000 | `<기록>/amend_drafts.md:189` "권고 1500000 = 시도 2 와 같은 값" | ✓ |

## 8. §6 질문 속 숫자 · 사실

| 주장 | 근거 | 판정 |
|---|---|---|
| Q2 사슬 `env_record` = BLAS · OPENBLAS_CORETYPE · CPU 모델 · numpy SIMD 기록만 | `rint_r_chain.py:1072–1096` | ✓ (초안 "스레드 수 · 1078–1095" → **고침**) |
| Q2 `np.einsum` 247 · `norm(axis=1)` 276 · 331 · 384 · 1100 · 1130 · 1179 · cKDTree 1003–1004 · 1129–1135 · 1178–1195 | `grep -n` (carbon_junction.py) | ✓ (초안 cKDTree "1003 · 1129 · 1178" = import 줄만 → 범위로 **고침**) |
| Q2 1 차원 `np.linalg.norm` = BLAS dot | `fibre_segment_raster.py:76` · 173 (`np.linalg.norm(d)` · 1 차원) · `cjunc_store.py:428–430` 머리 글 | ✓ (BLAS dot 인지 = numpy 구현 · 머리 글 서술 그대로) |
| Q2 machine-id 못 읽음 = 꺼짐 | `cjunc_store.py:76` (두 경로) · 391–401 · 747–749 | ✓ |
| Q3 처분 목록 (`disabled` · `key_unavailable` 포함) | `cjunc_store.py:747–766` · 774 · 784–801 | ✓ (`disabled` · `key_unavailable` 더함 = **고침**) |
| Q7 `ResumeRunner` 5750–5787 · 남은 payload 바이트 대조 | 5750 `class ResumeRunner` · 5786 `RESUME_MISMATCH … 남은 payload` · 5787 `return arms_` | ✓ |
| Q8 A 꼴 = 적용마다 `tocsc().tocsr()` | `step3_sigma.py` C 꼴 주석 (diff 의 "cupyx cg 의 `_make_system` 이 MatrixLinearOperator 로 감싸 적용할 때마다 `tocsc().tocsr()`") | ✓ (주석 서술 · cupy 소스 대조 안 함) |
| Q8 (b) 가짜 LinearOperator 머리 글 | `test_step3_gpu_precond.py:89–91` | ✓ ([추정] 표지 · 실제 cupy 미대조) |
| Q10 (a) elapsed_s · rss.log 섞임 | 등록 README 55–56 줄 | ✓ |
| Q11 시도 2 = 26,529,223 · 277,885 · 84,485 · 1.0519e-12 · 9.63612e-07 | `docs/data/rint2_probe6_a2_20261111/README.md:26–29` | ✓ |
| Q11 대비 · 행 길이 | 잰 적 없음 | [추정] 표지 (초안 "대비 약 10⁵–10⁶" 숫자 → **고침**: 숫자 지움) |
| Q11 두 핀 사이 풀이 경로 코드 차이 = 이 묶음 + 믹서 둘 | `$ git diff --name-only 5bca50c88 56f4cfbb1 -- scripts webapp docs/reviews/rint2_probe6_prep_20261110/tools` → 25 = 이 묶음의 그 경로 23 + `mixer_precal_observe.py` · `test_mixer_precal_observe.py` | ✓ |
| Q12 '원장 밖 킷 풀이 금지' = 원장 · Q9 §3-5 | `docs/reviews/rint2_dev_probe_ledger_20261026.md:5` · `q9_predict_units_design.md:11` | ✓ |
| Q12 `cjunc_graph_only_record` | `mpm_webapp_payload.py:1043` · `run_contract` 의 같은 이름 | ✓ |
| Q13 이 컨테이너 env git 설정 셋 · 키 이름 | `$ env \| grep -c '^GIT_CONFIG_KEY_'` → 3 · 키 = `credential.interactive` · `url.<…>.insteadOf` 둘 (값은 적지 않음) | ✓ (초안 "값 = 네트워크 쪽" → 키 이름으로 **고침**) |

## 9. §7 · §8

| 주장 | 근거 | 판정 |
|---|---|---|
| 판 Python 3.11.18 · numpy 2.4.6 · scipy 1.17.1 · git 2.43.0 | `$ python3 -I -c "…"` → `3.11.18 2.4.6 1.17.1` · `$ git --version` → 2.43.0 | ✓ |
| 우리 다시 돌림 19/19 (2 s) · 19 · 0 (19 s) · 70 · 0 (94 s) · 전 · 뒤 깨끗 | extra/runs_56f4cfbb1/_summary.txt (HEAD `56f4cfbb1d26…` · porcelain_before 0 · 세 줄 rc 0 · porcelain_after 0) | ✓ |
| e2e 기록 412 s (kgy 판) · 511 s (3.11) | §5 B5 행 | ✓ (초안 "7–11 분" = 근거 없는 범위 → **고침** · `check_all.sh:336` 이름표는 "7–10 분") |
| 기록 HEAD 0db6dee6d (작업 트리 커밋 · 원격에 없음) = `27ef82d24` 의 작업 트리 · 뒤 = 시험 두 파일만 | `<기록>/logs_r5/py311/_summary.txt` 2 줄 · `27ef82d24` 끝 줄 cherry-pick 0db6dee6d (작업 트리 커밋 · 원격에 없음) · `$ git diff --stat 27ef82d24 8ace86a82` → `test_cjunc_store.py` · `test_git_env_isolation.py` 둘 | ✓ |
| 기록 수 (사슬 506 · e2e 51 · e2e12 33 · conv_cert 30 · 저장본 e2e 6 · probe6 330 · b6 502 · 러너 151 · 계약 125 · 규율 128 · repo 0 오류 17 경고 · undef 2) | `<기록>/logs_r5/py311/_summary.txt` 각 줄 | ✓ |
| undef 2 = `generate_comparison_plots.py` 6905 · 6906 · 묶음 밖 · `a0455e90b` 에도 | `<기록>/logs_r5/py311/undef.log` · 25 바뀐 파일에 없음 · `$ git show a0455e90b:scripts/generate_comparison_plots.py \| sed -n 6905,6906p` → `log_vuln` · `log_phi_logcn` 같은 줄 | ✓ |
| 저장본 67 · 1 (T8) → 8b59b9618 (작업 트리 커밋 · 원격에 없음) 70/70 | `<기록>/logs_r5/py311/_summary.txt` (cjunc_store rc 1 · PASS 67 · FAIL 1 · T8) · `<기록>/logs_r5/mutfix/store_py311.log` · `store_py38.log` "70 PASS · 0 FAIL" · `<기록>/notes.md:280–281` (mutfix = 8b59b9618) | ✓ |
| 관찰: `load_base` 임시 폴더 안 지움 · 약 0.8 MB | `test_step3_gpu_precond.py:70–75` (`tempfile.mkdtemp` · 지우는 줄 없음 · `grep rmtree\|atexit` → 0) · 우리 다시 돌림 뒤 남은 폴더 `du -b` → 816,568 B (사본 374,803 B + .pyc) | ✓ (그 폴더는 우리 scratch 에서 지움) |
| 관찰: `scripts/__pycache__` 생김 · 무시 파일 | `git check-ignore -v` → `.gitignore:2:__pycache__/` · porcelain 0 | ✓ |
| §8 (가)–(마) · (바)–(파) | `<기록>/amend_drafts.md:101–112` (글 줄여 옮김) | ✓ |
| (카) G6 여덟에 gpu_precond 없음 | `test_git_env_isolation.py:431` | ✓ (더함) |
| (타) `GIT_CONFIG_GLOBAL` = git ≥ 2.32 | `<기록>/amend_drafts.md:111` (git 릴리스 노트는 대조 안 함) | ✓ (출처 = 기록) |
| 감싸개 픽스처 = cjunc_store `e175d475…` (2 회차) · 3.11.18 · 3.8.20 · 출력 같음 | `extra/wrapper_fixture_round2_code/try_probe_v2_py311.log:18` · 25 (`e175d475…`) · 12 (`"python": "3.11.18"`) · 5–8 (바이트 · 배열 같음 True) · py38 판 12 줄 3.8.20 · `$ git show 5eba3628e:scripts/cjunc_store.py \| sha256sum` → `e175d475…` (= 882f03a8d) | ✓ |
| 끝 핀 cjunc_store `5468e68d…` | `$ git show 56f4cfbb1:scripts/cjunc_store.py \| sha256sum` → `5468e68d1e7a…` (= 27ef82d24) | ✓ |
| VmHWM 머리 글 ② 앞 ↔ 코드 ① 앞 | 등록 블록 79 줄 (글) · 165 (`_reset_hwm`) · 168 (`encode_strict`) | ✓ |
| 등록 README E2 근거 "둘" · "PIN 한 줄만" | 등록 README 22 줄 · 10–11 줄 | ✓ (불일치 그대로 적음) |
| kgy 판 16 ✓ + cjunc_store ✗ | `<기록>/logs_r5/kgy.out` (16 ✓ · `cjunc_store` ✗ · rc 1) | ✓ |
| GPU 블록 7 판 4-f (셸 모의 rc 1 · CPU 흐름 5 판 · 267 · 37) | `<기록>/amend_drafts.md:303–312` · 270–271 · 291 · `<기록>/logs_r5/gpu_block_v7_shell_mock_result.json` (`"error": "ModuleNotFoundError: No module named 'cupy'"` · 두 sha256 = 블록 값) | ✓ |
| S0 재기 = 보수 어림 | 등록 README 54 줄 | ✓ |

## 10. 요청서의 [미확인] 표지 13 (§9 메타 뺌)

1. S0 다시 시작 시각 · 미열람 (§0) — 본 세션 전달 · 리포 기록 없음
2. 실기계 GPU 비트 같음 (B8 한정)
3. `56f4cfbb1` 게이트 두 조각 출력 (B12)
4. 본 세션의 stoic 앞당김 여부 (§5-1)
5. 지금 kgy GPU 부하 (§5-2)
6. gabia 판 GPU 블록 (§5-2)
7. 1저자가 ⑥ 시도 3 · 4 를 (나) 로 골랐는지 (§5-3)
8. kgy · gabia machine-id 유무 (Q2 c)
9. 같은 기계 실침대 결정성 (Q11 b)
10. kgy git 판 (§8 (타))
11. 감싸개 픽스처를 끝 핀에서 다시 (§8)
12. GPU 블록 GPU 길 (§8)
13. 실기계 묶음 (저장 꼴 · 시간 · 메모리 · machine-id · kgy 총 메모리 · 기계 사이 지문 · gabia Q11REPO) (§8)

## 11. 대조하다 본 것 (요청서 밖 · 본 세션 참고)

- ZIP repo/ blob 가운데 리포 원래 글에 집 폴더 경로 · 시험용 주소 글자가 있다 — `docs/reviews/findings.json` 7 곳 · 기록 tgz 안 24 파일 46 곳 · `scripts/test_rint_r_chain.py` 2 곳 (사설 주소 꼴 글자 = 기계 이름표 거부 시험 입력 · 4616 · 6345).  우리가 쓴 글 (요청서 · extra/ · make_zip.sh) 에는 0 곳.
- 기록 묶음 `logs_r5/mutfix/crf_selftest_py311.log` = `check_review_findings selftest: 22/24 PASS` (실패 16 "등록부가 비어 있지 않다" · 21 "리포 전체가 지금 깨끗하다") — 변이 사본 (리포 일부) 환경에서 돈 것으로 보인다 [추정] · 이번에 다시 돌리지 않았다 (허용 시험 밖).  요청서는 이 수를 인용하지 않는다.
- `<기록>/amend_drafts.md:189` 시도 3 원장 줄 초안의 "핀 = … stoic 끝" — 지금 Rint 가지는 `claude/sdcp-dem-manuscript-si-pqwtv8` (대피 세션) 이라 원장 줄을 쓸 때 가지 이름을 다시 본다.

- (11-13 · 본 세션) 리뷰 핀 커밋에서: 세션 메모 표지 → 진행 기록 `docs/session_20260923_progress.md` 11-13 [Rint ②] 줄 · 등록 README 정정 표지 둘 · §9 를 '채운 것' 으로.
