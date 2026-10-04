# 90차 제출자 증거 — 원문 로그 (PyBaMM 환경 고정 라운드 — C lock 기록 대조 + B 역사 기록)

스크래치패드 원문을 **바이트 그대로** 옮겼다. `.gitattributes` 의 `docs/22p_gap/gate90_evidence/** -text !eol` 규칙은 증거 로그를 넣기
**전에** 더했다 (`fb29e63f0`). `.gitignore` 의 `*.log` 때문에 로그는 `git add -f` 로 넣었다. 셸 래퍼 안의 절대 경로는 제출자 세션의
스크래치패드다. 편집한 파일은 이 README 하나다. 줄머리 집계는 고정 (`^물었다` · `^★ 안 물었다` · `^★ 실행오류`).

| 파일 | 무엇 | 실행 상태 |
|---|---|---|
| `00_red_test_gate90_38failed.log` | RED `pytest tests/test_gate90_env_profile.py -rA` — **38 failed** (33 `ModuleNotFoundError: tools.env_profile` · e01 lock 없음 · e11 B 없음 · e09 smoke 호출 0 · e10 `_stamp` 없음 · e12 정정 전) · 머리 `source_digest 803e2b7781cbc9cd` | `1f3829b9a` + 새 시험 파일 (= `cff5e409b`) |
| `00b_kexpr_overlap_registry397_new_nodes38_overlap0.txt` | 등록부 `-k` 397 (k 없는 선언 11 제외) 을 pytest `KeywordMatcher` 로 새 node 38 에 대 본 출력 — 겹침 **0** · collect rc 0 | 같은 작업 트리 |
| `01_green_test_gate90_38passed.log` | GREEN — **38 passed** · 머리 `source_digest 3f84c0db52d2b9ac` | `2165a9183` + GREEN 작업 트리 (= `e2160c2ef`) |
| `02_related_modules_10failed_stale_receipt_identity.log` | 관련 10 모듈 — **577 passed / 10 failed** · 10 = "영수증이 낡았다 — validator `803e2b7781cbc9cd` ≠ 현행 `3f84c0db52d2b9ac`" (예상) · 끝 HEAD 같음 · dirty 0 | clean `e2160c2ef` |
| `03a_replay_g90_emit_expect_first_witness_nondeterministic.log` | 첫 `-k g90 --emit-expect` — 13 변이 모두 기대 node 사망 · 그러나 증인에 tmp 경로 (`pytest-NNNN`) 가 섞여 **쓰지 않았다** (요청문 §6-b) | `c547c2458` + 등록 13 |
| `03_replay_g90_emit_expect_13killed.log` | 시험 assert 메시지 결정화 뒤 `-k g90 --emit-expect` — 13 변이 · 21 node 사망 · 결정적 증인 · EXPECT 미선언이라 줄머리는 `★ 안 물었다` · rc 1 | 같은 + 메시지 결정화 (→ `2586138c3`) |
| `04_replay_g90_verify_13_rc0.log` | `-k g90` (EXPECT 13) — **13/13 물었다 · rc 0** · scenario 13 · site 13 | 작업 트리 → `2586138c3` |
| `05_green_after_message_fix_38passed.log` | 메시지 결정화 뒤 GREEN 재실행 — **38 passed** (판정 · node 이름 불변) | 작업 트리 → `2586138c3` |
| `06_make_receipt_2586138c3_rc0.log` | `make_receipt.py paired_fixed5_v4 grid_fit_v5` — rc 0 · 35 · 34 · core `8408f8c2…` · `7f0f40f0…` | clean `2586138c3` → `1296af1f5` |
| `06b_make_receipt_check_core_identical_rc0.log` | `make_receipt.py … --check` — 두 leg core 재생성 **바이트 동일** · rc 0 | `2586138c3` + 재생성 작업 트리 → `1296af1f5` |
| `07_receipt_modules_after_regeneration_113passed.log` | 재생성 뒤 `test_gate70/71/72/74_defensive` — **113 passed** (02 의 10 건이 닫힘) | 같은 작업 트리 → `1296af1f5` |
| `08_env_profile_json_257d4cc1c_match.log` | `python -m tools.env_profile --json` — **MATCH** · rc 0 · 시작 HEAD = 끝 HEAD · dirty 0 | clean `257d4cc1c` |
| `10_full_pytest_257d4cc1c_2177passed.log` | 전체 `pytest tests/ -q -rfEx -p no:cacheprovider` — **2177 passed / 1 xfailed / rc 0** · 18:04:55Z → 19:05:45Z (1:00:47) · 시작 HEAD = 끝 HEAD · dirty 0 | clean `257d4cc1c` |
| `11_smoke_257d4cc1c_rc0.log` | `./scripts/smoke_e2e.sh` — **rc 0** · 기록 단계 줄 MATCH · 19:05:45Z → 19:08:32Z · 시작 HEAD = 끝 HEAD · dirty 0 | clean `257d4cc1c` |
| `12_full_replay_257d4cc1c_410_of_410_rc0.log` | 등록부 전체 재생 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) — **scenario 421 (executable 410 · declared 11) · site 459 · ran 410 · 410/410 call 단계에서 선언한 이유로 물었다 · rc 0** · 19:08:32Z → 21:53:04Z (2:44:32) · 시작 HEAD = 끝 HEAD · dirty 0 | clean `257d4cc1c` |
| `13_docs_lint_fixed_table_1f3829b9a_358passed.log` | **보충** — 고정 표 커밋의 `pytest tests/test_docs_lint.py` 원문 · **358 passed · rc 0** (25:40) · 끝 HEAD `cff5e409b` (그 사이 차이는 docs-lint 가 읽지 않는 `tests/` 시험 파일 하나) · dirty 0 | `1f3829b9a` |
| `14_docs_lint_send_24f499ba6_358passed.log` | **발송 뒤 덧붙임** — 발송 HEAD 의 `pytest tests/test_docs_lint.py` 원문 · **358 passed · rc 0** · 21:55:08Z → 22:23:10Z (27:59) · 시작 HEAD = 끝 HEAD · dirty 0 | `24f499ba6` (발송 SHA) |

## 전체 sha256 · 크기 (바이트)

```
5c087216ee0c428893c3502aa1cc3c9352937684b03e884e68a859dfdc7bb996  57819  00_red_test_gate90_38failed.log
1d29c3c9288f7edf824755bfbef3f58b62cc12133a66b7475640f13777c41db5  3860  00b_kexpr_overlap_registry397_new_nodes38_overlap0.txt
cb47100b67b2cb30c3379cd72817efa4635952302362b4f73f1a369837d24987  4788  01_green_test_gate90_38passed.log
299c443e9b9cf83d50181e6f27d502fb5e919d835afcb6419dee15f31a88f95e  30665  02_related_modules_10failed_stale_receipt_identity.log
c14c00d17c6e5dd2ede4eaf7cbaf27b1bd88190ae228a5abd684a523bef3858d  10031  03_replay_g90_emit_expect_13killed.log
b0ca43bd69c66ad8009bb54cbd359af31a03c5716b0776cc348ce93cd0f846b0  13016  03a_replay_g90_emit_expect_first_witness_nondeterministic.log
e2640d134bd1f357c4c9ea3677a01faf6f633e477be3507737696231463f2ff9  1849  04_replay_g90_verify_13_rc0.log
497d26c08a98079d0b546928ffd31a2fd63988d902c3a7cc6618e6921c3c4483  4813  05_green_after_message_fix_38passed.log
0e825109e79ebc5c1cb32bbc1775805dc66f128bd23dbaf2dd790c7505f9578d  431  06_make_receipt_2586138c3_rc0.log
67baa7c034eb91d3af464d4a183cfaca4f8375df6b67b1f13760110d2366fe16  300  06b_make_receipt_check_core_identical_rc0.log
63b178dcbac3f0f26cba9f4ea6f2d31d6ee33a0dc998b517d5b5b724db839184  1080  07_receipt_modules_after_regeneration_113passed.log
6507957816822bde3ab26b9d319a3402506fad8483234d4c8a781c11ef778758  883  08_env_profile_json_257d4cc1c_match.log
616020f20656ac8341c86848bc42f52d8547fc1efdc0035225c8c6c29039eb41  3584  10_full_pytest_257d4cc1c_2177passed.log
dc9328a124c91dadd1c4c8f48892ba4d72f73bcf22f0015f66828f3936c7e521  6462  11_smoke_257d4cc1c_rc0.log
45b2bfee822b1de0702a39d8ccec3f3a6ac9b6ba2ba4f3e320a99a1bf75cf59c  53612  12_full_replay_257d4cc1c_410_of_410_rc0.log
52db2ebd8f5003cf7289eb0f36b66c93f0e6a7e6043fdfb9ebdcff7d2eeb0de2  1147  13_docs_lint_fixed_table_1f3829b9a_358passed.log
105c18cb2d455a6cbe305563fbac01c1678826aca5fb3fc975726ac9021943e8  1219  14_docs_lint_send_24f499ba6_358passed.log
```

## 없는 것 (그대로 적는다)

- 번호 09 는 비워 두었다 (89차 증거의 09 자리 — 재생성 뒤 영수증 모듈 — 는 이번에 07 로 앞당겼다).
- 이 라운드 사이의 게이트 차수 밖 docs-lint (`1fb9a24ed` · 358 passed) 원문은 싣지 않았다 — REIL 문서의 점검이지 이 게이트의 판정 근거가 아니다.
- 발송 HEAD 의 docs-lint 는 발송문에 적는다 (이 README 가 든 커밋보다 뒤라서). — 발송 뒤 덧붙임: 그 원문이 14 번이다 (README 표 · sha256 에 한 줄씩 더했다).
