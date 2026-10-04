# 89차 제출자 증거 — 원문 로그 (G88-N1 한정 보완)

스크래치패드 원문을 **바이트 그대로** 옮겼다. `.gitattributes` 의 `docs/22p_gap/gate89_evidence/** -text !eol` 규칙은 증거 로그를 넣기
**전에** 더했다 (`b1b44cf0f`). `.gitignore` 의 `*.log` 때문에 로그는 `git add -f` 로 넣었다. 셸 래퍼 안의 절대 경로는 제출자 세션의
스크래치패드다. 편집한 파일은 이 README 하나다. 줄머리 집계는 고정 (`^물었다` · `^★ 안 물었다` · `^★ 실행오류`).

| 파일 | 무엇 | 실행 상태 |
|---|---|---|
| `00_red_first_run_header_label_wrong.log` | RED 첫 회 — **4 failed / 2 passed** · 머리 둘째 줄을 `source_digest e462a3d19` 로 잘못 적었다 (RUN_SCOPE 를 마지막으로 바꾼 커밋 · 요청문 §6-a) | HEAD `b1b44cf0f` + 작업 트리 (시험 파일 · conftest 등록) |
| `01_red_test_gate89.log` | RED `pytest tests/test_gate89_finalize_input_binding.py -rA` — **4 failed / 2 passed** · 실패 4 = d02 넷 `Failed: DID NOT RAISE PreserveError` (G88-N1 실행 재현) · 머리 `source_digest 7dd546baaee9e823` | 같은 작업 트리 → `76a5da16e` |
| `01b_kexpr_overlap_registry395_new_nodes0.txt` | 등록부 `-k` 395 를 pytest `KeywordMatcher` 로 새 node 6 에 대 본 출력 — 겹침 **0**. 끝 줄 라벨의 "non-g88" 은 88차 플러그인을 옮기며 남은 문구다 — 세는 조건은 이름이 `-g89` 로 끝나지 않는 등록 (그때 395 전부) | RED 와 같은 작업 트리 |
| `02_green_gate89_6passed_gate88_24passed.log` | GREEN — test_gate89 **6 passed** · test_gate88 **24 passed** (88차 이유 불변) · 머리 `source_digest 803e2b7781cbc9cd` | `76a5da16e` + GREEN 작업 트리 → `26c11d6fc` |
| `03_related_finalize_modules_7failed_stale_receipt_identity.log` | `finalize_leg` 를 쓰는 관련 8 모듈 — **485 passed / 7 failed** · 7 = `test_gate74_defensive` 의 영수증 validator identity 낡음 (예상) | 같은 작업 트리 (영수증 재생성 전) |
| `04_replay_g89_emit_expect_2killed.log` | `-k g89 --emit-expect` — 2/2 기대 node 빨강 · EXPECT 미선언이라 줄머리는 `★ 안 물었다` · rc 1 | `14978adb0` + 등록 2 |
| `05_replay_g88_finalize_binds_emit_expect_witness_changed.log` | `-k finalize-binds-the-receipt-package-to-the-consumer-g88 --emit-expect` — fail node 그대로 · **증인 바뀜** (`DID NOT RAISE` → 이유 대조 실패) · rc 1 | 같은 작업 트리 |
| `06_replay_g89_verify_rc0.log` | `-k g89` (EXPECT 2) — **2/2 물었다 · rc 0** | 작업 트리 → `134f26f48` |
| `07_replay_g88_verify_21_rc0.log` | `-k g88` (EXPECT 21 · 한 항목 증인 갱신) — **21/21 물었다 · rc 0** | 작업 트리 → `134f26f48` |
| `08_make_receipt_134f26f48_rc0.log` | `make_receipt.py paired_fixed5_v4 grid_fit_v5` — rc 0 · 35 · 34 · core `20645070…` · `e5563807…` | clean `134f26f48` → `66129fc6a` |
| `09_gate74_defensive_after_receipts_41passed.log` | 재생성 뒤 `test_gate74_defensive` — **41 passed** (03 의 7 이 닫힘) | `134f26f48` + 재생성 작업 트리 → `66129fc6a` |
| `10_full_pytest_66129fc6a_2139passed.log` | 전체 `pytest tests/ -q -rfEx` — **2139 passed / 1 xfailed / rc 0** · 2026-10-04T07:08:17Z → 2026-10-04T08:00:50Z (0:52:30) · 시작 HEAD = 끝 HEAD · dirty 0 | clean `66129fc6a` |
| `11_smoke_66129fc6a_rc0.log` | `./scripts/smoke_e2e.sh` — **rc 0** · 2026-10-04T08:00:50Z → 2026-10-04T08:03:15Z · 시작 HEAD = 끝 HEAD · dirty 0 | clean `66129fc6a` |
| `12_full_replay_66129fc6a_397_of_397_rc0.log` | 등록부 전체 재생 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) — **scenario 408 (executable 397 · declared 11) · site 446 · ran 397 · 397/397 call 단계에서 선언한 이유로 물었다 · 안 물었다 0 · rc 0** · 2026-10-04T08:03:15Z → 2026-10-04T10:29:58Z · 시작 HEAD = 끝 HEAD · dirty 0 | clean `66129fc6a` |
| `13_docs_lint_gate88_send_d6056415b_358passed.log` | **보충** — 88차 발송 HEAD 의 `pytest tests/test_docs_lint.py` 원문 · 358 passed · rc 0 · 2026-10-03T14:15:28Z → 14:40:56Z · 시작 HEAD = 끝 HEAD · dirty 0 (88차 16 원문 밖이었다 — 88차 리뷰어 지적) | clean `d6056415b` |

## 전체 sha256 · 크기 (바이트)

```
1775b7433a47d04ce9dab636d83dbffe0c983b3efd2c74cc0d7b512396c5f640  7930  00_red_first_run_header_label_wrong.log
6f7ac67fd848dfbed63d3c32fde35012703135376de4c26d91a08f4263a5d370  7937  01_red_test_gate89.log
55120c28c22d1b7359796785865d6801db6a517558ec725f3c8019936cacdd25  1507  01b_kexpr_overlap_registry395_new_nodes0.txt
fc82cd55c7110c006aaf2d3d81e07a96d28e96f8bcea294b7fadef828316110d  2985  02_green_gate89_6passed_gate88_24passed.log
e808420b2e2f7b79746978818ecd0c31fc38e7ef94eb6134e5121182836cc3b0  11049  03_related_finalize_modules_7failed_stale_receipt_identity.log
d9d7a5ee0550991e05a2558f5d6563622208c86f66751911e6180403bdb00458  3036  04_replay_g89_emit_expect_2killed.log
04262f6b27b1e794261988d181ec8cf54d33f942728b8b370279152a3d37d913  1541  05_replay_g88_finalize_binds_emit_expect_witness_changed.log
3fb046d06ddca13d898cc3e819baf4c7ee54a26d4bbbcd35a0359271d439bcad  717  06_replay_g89_verify_rc0.log
41805343aa90c0df26f02e907a41c2b18d2008ccd884dcc6133645dc5f70e962  2473  07_replay_g88_verify_21_rc0.log
baf8567c42e146e69db12f28795f87a562b76a35f182ed0ac72a93714dfd8d80  469  08_make_receipt_134f26f48_rc0.log
f2448e8041c5627ce3bb988e8e930e55374123440b910f5ca10afca0c8b4d9a4  909  09_gate74_defensive_after_receipts_41passed.log
e5f8cdf2ef20271d4aff2ec3c3a44318107578ffe733d613c917b92c04b32aa1  3504  10_full_pytest_66129fc6a_2139passed.log
effbed4a26edf6a940e175511a03c0385c1278530a9f4e7d8fc4a48671013774  5762  11_smoke_66129fc6a_rc0.log
1c6d2caa7a1161bb36bc39aeeab01f4e53ed8ffae50555e0c3362766ae5fb9a8  52232  12_full_replay_66129fc6a_397_of_397_rc0.log
f5445e0d768c75a6d268173750e5eda5d5acd0c5cc5fcdbd397a9651c1a30cec  1163  13_docs_lint_gate88_send_d6056415b_358passed.log
```

## 없는 것 (그대로 적는다)

- 이 라운드 사이의 게이트 차수 밖 docs-lint 두 회 (`c14775710` · `234ee23a7` · 둘 다 358 passed) 의 원문은 싣지 않았다 — 88차 회신 접수와
  REIL 기록의 점검이지 이 게이트의 판정 근거가 아니다 (요청문 §6-h).
- 발송 HEAD 의 docs-lint 는 발송문에 적는다 (이 README 가 든 커밋보다 뒤라서).
