# 88차 제출자 증거 — 원문 로그 (G87-N1 한정 보완)

스크래치패드 원문을 **바이트 그대로** 옮겼다. `.gitattributes` 의 `docs/22p_gap/gate88_evidence/** -text !eol` 규칙은 증거 로그를 넣기
**전에** 더했다 (`6594cb1dd`). `.gitignore` 의 `*.log` 때문에 전부 `git add -f` 로 넣었다. 셸 래퍼 안의 절대 경로는 제출자 세션의
스크래치패드다. 편집한 파일은 이 README 하나다. 줄머리 집계는 고정 (`^물었다` · `^★ 안 물었다` · `^★ 실행오류`).

| 파일 | 무엇 | 실행 상태 |
|---|---|---|
| `01_red_test_gate88.log` | RED `pytest tests/test_gate88_fit_only_lifecycle.py -rA` — **9 failed / 7 passed** · f01_01 의 traceback 이 G87-N1 실행 재현 (`_record_phase(claim, "fit")` 이 commit 뒤 거부) | HEAD `9b539ce8b` + 작업 트리 (고정 표 §14 · 원장 §129 · 시험 파일 — 셋 다 커밋 전 · 09:17:02Z 실행 · 09:21 에 `00ed85b44` → `6594cb1dd` → `9e53a7edb` 로 커밋) · RUN_SCOPE = 87차 판정 대상 그대로 |
| `02_red_after_witness_stabilization.log` | 증인 고정 뒤 RED 재확인 — **9 failed / 7 passed** (같은 node) | `9e53a7edb` + 작업 트리 → `5cdf22bea` |
| `03_green_37passed.log` | GREEN — test_gate88 16 + spy 정정한 61 · 62 모듈 **37 passed** | `5cdf22bea` + GREEN 작업 트리 → `e462a3d19` |
| `04_related_modules_run1_aborted_probe_contamination.log` | 관련 21 모듈 1 회차 — **중단 (rc 143)** · 탐침 오염 (요청문 §6-e) · 판정 근거 아님 | scratch worktree (`9e53a7edb` + GREEN) |
| `04b_probe_stray_exec_class_records_worktree_only.txt` | 그 탐침이 scratch worktree 의 `_exec_class/` 에 남긴 기록 2 개의 원문 (지우기 전 보존) | 본 checkout 아님 |
| `05_related_modules_run2_9failed_before_receipts.log` | 관련 21 모듈 2 회차 — **820 passed / 9 failed** (7 = 영수증 identity 낡음 · 2 = spy 서명 → 정정 · 03 에 포함) | scratch worktree (영수증 재생성 전 · 예상된 실패) |
| `06_replay_g88_emit_expect_16killed.log` | `-k g88 --emit-expect` (16) — 16/16 기대 node 빨강 · EXPECT 미선언이라 줄머리는 `★ 안 물었다` · rc 1 | `e462a3d19` + 등록 16 |
| `07_replay_g88_verify_expect_rc0.log` | `-k g88` (EXPECT 16) — **16/16 물었다 · rc 0** | 작업 트리 → `12a2c27be` |
| `08_full_pytest_38522285f_aborted_at_27pct_for_pins.log` | 전체 pytest 1 회차 — **27 % (실패 0) 에서 내가 멈췄다** (자체 점검 고정을 먼저 넣으려고 · 요청문 §6-b) · 판정 근거 아님 | clean `38522285f` |
| `09_replay_g88_pins_emit_expect_20_baseline_collision.log` | `-k g88 --emit-expect` (20 — 고정 4 추가) — 새 4 관측 · 기존 15 선언 일치 · **f03_01 baseline 빨강** (같은 시각 손 실행과 고정 scratch 경로 충돌 · 요청문 §6-f) · rc 1 | 작업 트리 (고정 시험 일부 + 등록 20) |
| `10_replay_g88_pin5_emit_expect.log` | `-k only-for-fit-only --emit-expect` — 다섯째 1/1 관측 · rc 1 (미선언) | 작업 트리 (등록 21) |
| `11_replay_g88_verify_21_rc0.log` | `-k g88` (EXPECT 21 · **단독 실행**) — **21/21 물었다 · rc 0** | 작업 트리 → `07aefea11` |
| `12_registry_modules_before_pin_commit_aborted.log` | 등록부를 읽는 시험 모듈 11 (사전 점검) — **12 분에 3 node 에서 멈췄다 (rc 143)** · 판정 근거 아님 (같은 모듈은 13 이 덮는다) | 작업 트리 → `07aefea11` |
| `13_full_pytest_07aefea11_2133passed.log` | 전체 `pytest tests/ -q -rfEx` — **2133 passed / 1 xfailed / rc 0** · 2026-10-03T10:45:57Z → 2026-10-03T11:40:14Z (0:54:14) · 시작 HEAD = 끝 HEAD · dirty 0 | clean `07aefea11` |
| `14_smoke_07aefea11_rc0.log` | `./scripts/smoke_e2e.sh` — **rc 0** · 2026-10-03T11:40:14Z → 2026-10-03T11:42:44Z · 시작 HEAD = 끝 HEAD · dirty 0 | clean `07aefea11` |
| `15_full_replay_07aefea11_395_of_395_rc0.log` | 등록부 전체 재생 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) — **scenario 406 (executable 395 · declared 11) · site 444 · ran 395 · 395/395 call 단계에서 선언한 이유로 물었다 · 안 물었다 0 · rc 0** · 2026-10-03T11:42:44Z → 2026-10-03T14:13:33Z · 시작 HEAD = 끝 HEAD · dirty 0 | clean `07aefea11` |

## 전체 sha256 · 크기 (바이트)

```
79a2694e4f643c4dea781942e81a7fe1940540c80ba604d0ba8b0f070dbbb153  53471  01_red_test_gate88.log
25b8acd3b4e788a31228f1d9d5ccf909be3d37955bafd447cd21fa0bf96a748b  53999  02_red_after_witness_stabilization.log
dca5d54ff9a759ae6f94e47505a25b2ac493fc5dc741d6269d4584b26c375e1b  5471  03_green_37passed.log
ede5509a0fccefe62167b5522bef11370a0a4e445d24b2e6eda4b293dc76dcb4  1847  04_related_modules_run1_aborted_probe_contamination.log
7d44210776d83763459e7fd0768524551cd463692145c751b0d2e45ef87b1284  628  04b_probe_stray_exec_class_records_worktree_only.txt
04a66b6fbc25ef542a9a4c0a7cdbb8e3fcaf0934156d77b96b61707a75751258  31778  05_related_modules_run2_9failed_before_receipts.log
ffd9724259c743be928e0286172782c677384ba345a063e295ec764e0dffe1af  21330  06_replay_g88_emit_expect_16killed.log
0305f41728f86a0635bf6221c463a21c96db7d46466f6085c606d1f8e7fa085e  2033  07_replay_g88_verify_expect_rc0.log
35368587cc6d6e47b5f34b470e72c9dac7efe186bd0d7878d623e68cdf1c74ea  1293  08_full_pytest_38522285f_aborted_at_27pct_for_pins.log
20d03db9d7b06e1525cf8412f56dd9980e40272482c4c3560d95b8b48d51f865  22579  09_replay_g88_pins_emit_expect_20_baseline_collision.log
21905e590deb5308082270315aa16388966c8d7bf735d64e3cc3a56dca95ba60  1333  10_replay_g88_pin5_emit_expect.log
7d46f78b22d926eabeaf1f3ec64437fc8533159c79eb8cb0fe80dd194e33761d  2554  11_replay_g88_verify_21_rc0.log
c31dface11aec43c90d124b863313583b5f2c73582a1a1bdf65de8e68044e0fa  924  12_registry_modules_before_pin_commit_aborted.log
bfb3ccbfc01dace46d75936dd62d3505c28dad56167723d990fe8baf0ac65ff5  3504  13_full_pytest_07aefea11_2133passed.log
36d2a750932fdcc5ca4c15ae4ceee87473721deeabc674660f702ab56fd4f0de  5762  14_smoke_07aefea11_rc0.log
df507237097e20b0c6b2591ef55201ee9033c726519ae422815a8ada91f56711  52023  15_full_replay_07aefea11_395_of_395_rc0.log
```

## 없는 것 (그대로 적는다)

- 영수증 재생성 출력은 따로 커밋하지 않았다 — 원문은 커밋 `38522285f` 메시지와 영수증 파일 자체 (rc 0 · 35 · 34 검사). 스크래치패드의
  `08_make_receipt.log` 는 두 줄 요약뿐이라 넣지 않았다.
- docs-lint 를 `timeout 900` 으로 잘랐던 회차와 상한 없이 다시 돌린 회차 (358 passed · 23:41) 의 원문은 보존하지 않았다 (요청문 §6-k) —
  13 (전체) 이 docs-lint 를 포함한다.
