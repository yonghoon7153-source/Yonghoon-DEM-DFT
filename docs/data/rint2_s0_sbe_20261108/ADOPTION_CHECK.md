# kgy S0 단계 1 (SBE) — 채택 조건 하나씩 대조 (11-09 · 메인 세션)

- 기준 = 수정 계획 `docs/reviews/rint2_rr3_fix_plan_20261108.md` §5 조건 1–5 (판정문 §6 · SELF-155 닫는 확인) · `docs/reviews/rint2_s0_mem_fix_20261106/REPORT.md` §12.
- 입력 = 1저자가 kgy 에서 묶은 `s0fix_1106_done.tgz` (24,284,950 B · sha256 `d48f55c1b6884a75f011e9517d3f592c25aecf8a73d7a02ebbbee86eaede0a13` · kgy 화면의 sha256 과 같음) · 실행 = 11-08 (kgy · 1저자 · 기록 폴더 · 출력 폴더 날짜 11-08).
- 대조 = 빈 임시 폴더에 풀어 읽기만 (python -I · 아무것도 실행 안 함) · σ 값 열지 않음 (단계 1 = 접합 census · 계획).
- 판정 = **채택** (조건 1–4 충족 · 조건 5 = 문구 · 순서 그대로).

| 조건 | 대조 | 결과 |
|---|---|---|
| 1. rc = S0 Python 자식 rc | 기록 폴더 `rss.log` 끝 줄 `rc=0` = 감시 셸 `run2.sh` 15 줄 `wait $PID; echo "rc=$?" >> rss.log` (그 셸 = 핀 `f47bde0f6` 의 `docs/reviews/rint2_s0_mem_fix_20261106/tools/run2.sh` 와 같은 글) · `rc=` 줄 1 개 · `CAP_TERM` 줄 0 (메모리 상한 중단 없음) · dumps.txt 89 줄 = USR1 스택 기록 요청 (probe2.py · stacks.txt · 끝맺음 신호 아님) | rc 0 ✓ |
| 2. 여섯 출력을 실제로 읽음 · 같은 실행에 결속 | 여섯 다 있음 · 실행 끝에 pack.sh 가 적은 `out_sha256.txt` = 실제 sha256 **6/6 같음** · kit JSON: schema `ca-s0-census-v4` · stage 1 · kit `kit_SBE_vgcf100` (run_complete_marker True) · tool `s0-b3-registry-v1` · elapsed_s 5382.8 · 계획 sha256 `4da98863…0197bd` = `cjunc_plan.sha256` 선언 = 계획 파일 실제 sha256 = kit JSON plan.sha256 = run.log 끝 줄 (네 곳 같음) · NPZ 둘 = `allow_pickle=False` 로 열림 (접합 117,583 행 · 접촉 117,070 행 · 배열 이름 · 꼴만 봄) · payload 로그 = 같은 킷의 STEP3 payload 기록 | ✓ |
| 3. 새 빈 폴더 · SBE 한 침대 · stage 1 · σ 비열람 · 실패 보존 | 출력 폴더 = 새 이름 (`ca1_s0_sbe_20261106_memfix`) · stage 1 · 킷 하나 · σ 값 칸 없음 (census · 계획만) · 실패 없음 | ✓ (원 입력 무쓰기 = 도구 계약 · 묶음으로는 직접 대조 못 함 — 한정) |
| 4. 고정 환경 · 코드 지문 · 핀 · 종료 · 시간 · RSS | kit JSON code: git_head `f47bde0f631f94340f745e5ae5fa20f902c58333` · git_dirty False · Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · 코드 지문 7 (`S0_SAME_FILES` = ca_s0_census · step3_sigma · mpm_webapp_payload · fibre_segment_raster · sr01_stamp_compare · carbon_junction · ptfe_face_alpha) = 리포 `f47bde0f6` blob sha256 **7/7 같음** · 기록 폴더 pin.txt = 같은 핀 · 시간 5,384 s (rss.log 마지막 표본) · **표본 최대 RSS 5,694,360 kB (≈ 5.43 GiB · t = 5,379 s · 5 초 간격 표본 — 실제 peak 아님)** · 상한 41 GB | ✓ |
| 5. 한정 · 순서 | 두 예외의 실침대 영향 = 미확인 문구 그대로 · 다음 = s_min → ⑥ → 기하 · 반복 수 → 숫자 · 실행 정책 → 새 계획 / 핀 봉인 → 단계 2 → 등록 R 진입 판단 (순서 그대로) · 이 채택 = 단계 1 개발 자료의 실측 성공 기록 (등록 R 결과 아님 · 실행 승인 아님) | 문구 ✓ |

- 비교 (SELF-155): 11-04 첫 시도 = 52.1 GB 에서 신호 kill (출력 없음) → 11-06 고침 (`f47bde0f6` · 합성 후보 17,701,828 → 61,131) → 이번 실침대 표본 최대 ≈ 5.43 GiB · rc 0.
- 반입 도구 = 이 폴더 `tools/import_s0_tgz.py` (11-09 고침판 · rc 근거를 rss.log `rc=` 줄 하나로 · `CAP_TERM` = 채택 안 함) · 처음 판 (11-08 준비판) 은 이 tgz 에 FAILED_PRESERVED (rc 미확인) 를 냈다 — 합성 고정물이 rc 를 run2.log · payload 로그에 적어 실제 run2.sh 꼴 (rss.log) 을 따르지 않았고, 같은 원인으로 rc 1 · CAP_TERM · rc 줄 둘 꼴도 "채택" 으로 냈다 (`tools/selftest.log` = 옛 판 5/5 채택 · 고친 판 = 정상 1 채택 · 나머지 4 거부).  자기 결함 = 원장 SELF 항목.
