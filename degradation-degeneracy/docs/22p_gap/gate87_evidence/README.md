# 87차 제출자 증거 — 원문 로그 (라운드 2b 제한 구현)

스크래치패드 원문을 **바이트 그대로** 옮겼다. `.gitattributes` 의 `gate87_evidence/** -text !eol` 규칙은 `d82e840d` 에서
더했다 — 그 전에 커밋된 01–05 는 원본과 sha256 동일 · CR 0 을 확인했다 (11 smoke 로그에는 CR 이 1 개 있다 — 규칙 뒤에
들어갔다). `.gitignore` 의 `*.log` 때문에 전부 `git add -f` 로 넣었다. 셸 래퍼 안의 절대 경로는 제출자 세션의
스크래치패드다. 편집한 파일은 이 README 하나다.

| 파일 | 무엇 | 실행 상태 |
|---|---|---|
| `01_red_test_gate87_round2b.log` | RED `pytest tests/test_gate87_round2b.py -rfE` — **52 failed / 11 passed** | 작업 트리 (시험 파일 · conftest 등록만 추가 · RUN_SCOPE = `0b21490d` = `632e4b0a` 코드) |
| `02_green_attempt1_6failed.log` | GREEN 1 회차 — 6 failed (시험 쪽: 계획 이름 · design `arms` dict) | 작업 트리 (생산 diff 적용 · 커밋 전) |
| `03_green_attempt2_1failed.log` | GREEN 2 회차 — 1 failed (arm registry 에 걸린 설계 변경) | 작업 트리 |
| `04_green_63passed.log` | GREEN — 63 passed | 작업 트리 → 이 상태로 `b8d4b693` 커밋 |
| `05_related_modules_before_receipts.log` | 관련 11 모듈 — **986 passed / 15 failed** (14 = 영수증 identity 낡음 · 1 = 계약 인용 좌표) · 29:56 | `b8d4b693` (영수증 재생성 전 · 예상된 실패) |
| `06_green_after_witness_fix_63passed.log` | 증인 고정 · s03_04 자기일관 위조 · s02_05 추가 뒤 63 passed (+ 이 셸이 붙인 `module rc=0`) | 작업 트리 → `929b7cee` |
| `07_replay_g87_round1_emit_expect_3survived.log` | `mutation_replay.py -k g87 --emit-expect` — 22 중 **3 안 물었다** (envelope 결속 3 · 시험 결함 · 요청문 §6-a) · EXPECT 미선언 표시 · rc 1 | 작업 트리 (변이 등록 · 시험 `b8d4b693`) |
| `08_replay_g87_round2_emit_expect_22killed.log` | 같은 명령 — **22/22 기대 node 빨강** · EXPECT 미선언 표시 · rc 1 | 작업 트리 (시험 `929b7cee` 와 같은 내용) |
| `09_replay_g87_verify_expect_rc0.log` | `-k g87` — **22/22 물었다 · rc 0** (EXPECT 대조) | 작업 트리 (EXPECT 추가 · `ba0f48b1` 커밋 내용) |
| `10_full_pytest_7fbaa45b_2109passed.log` | 전체 `pytest tests/ -q -rfEx` — **2109 passed / 1 xfailed / rc 0** · 03:25:14Z → 04:26:48Z | clean `7fbaa45b` (첫 줄 `dirty=0`) |
| `11_smoke_7fbaa45b_rc0.log` | `./scripts/smoke_e2e.sh` — **rc 0** · 04:26:48Z → 04:29:49Z | clean `7fbaa45b` (`dirty=0`) |
| `12_full_replay_…_attempt1_cut_at_2h_254_of_374.log` | 등록부 전체 재생 1 회차 — `timeout 7000` (하네스 시간 상한) 으로 **rc 124 · 중단** · 254 물었다 · 안 물었다 0 · **판정 근거 아님** | clean `7fbaa45b` |
| `13_full_replay_7fbaa45b_run2_374_of_374_rc0.log` | 등록부 전체 재생 2 회차 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) — **scenario 385 · executable 374 · declared 11 · site 423 · ran 374 · 374 물었다 · rc 0** · 06:27:50Z → 09:14:23Z | clean `7fbaa45b` (`dirty=0`) |

행 집계는 줄머리 고정 (`^물었다` · `^★ 안 물었다` · `^★ 실행오류`). 13 의 `^물었다` 374 · `^★` 0.

## 전체 sha256 · 크기 (바이트)

```
7a90f485217d9ec0687fcc9b87b83c9c22daa555c0e9e0821d60927bc39ebc91  84151  01_red_test_gate87_round2b.log
9f89cb7a918f641936da3d90e069fd7ffdc52ec1790d9e289d444b609a5f50ce  17838  02_green_attempt1_6failed.log
069d9978281172afb53641e3703476aa047e5862ec705f5e18da146f09c02d09  2591  03_green_attempt2_1failed.log
1fda62669c3dfccfddcd3a1a37cdc6be7ca444b285fb9546f5bd60a4315ee2b4  665  04_green_63passed.log
d3dcc64294e34859237695545a03535fb762630066a0bfcebe792b6a8d9a8df3  42821  05_related_modules_before_receipts.log
f9d119a1603329ce9fda426f299f9ad17ded47470cad5d7bf6b441143a1f6938  677  06_green_after_witness_fix_63passed.log
2cd7af55555f622166674d02b0205982c18dd68a8e8e44e390a247c66ffa5295  19875  07_replay_g87_round1_emit_expect_3survived.log
c698d1bf531f48e529bb6f876e9f8840efeab61e732aec1431d017f455564ef1  19505  08_replay_g87_round2_emit_expect_22killed.log
8852a18d067ba931f0762ffdedb0143a947f6ee11d1f65594b0d21041e94c1a0  2038  09_replay_g87_verify_expect_rc0.log
3bf49fc9f5066b94f74ce911910713e7ef3a40321cc4ed0aedb91225b68fbfb2  3449  10_full_pytest_7fbaa45b_2109passed.log
ff0ec69e51c63b9cd81848e2319e42337d357eea4cc8a4b2d5f1fed3dd503d94  5707  11_smoke_7fbaa45b_rc0.log
100600f035bc73d19920bc80120665be0d31d3f0f0d55ca7cc6861dfb481e1be  31415  12_full_replay_7fbaa45b_attempt1_cut_at_2h_254_of_374.log
2b8056e0d3224653ace11442281df2576e95c6247922056ba0725bdc5e2aa1c4  50010  13_full_replay_7fbaa45b_run2_374_of_374_rc0.log
```

## 없는 것 (그대로 적는다)

- 영수증 재생성 출력은 따로 `tee` 하지 않았다 — 원문은 커밋 `7fbaa45b` 메시지와 영수증 파일 자체 (rc 0 · 35 · 34 검사).
- 05 이후 관련 모듈만 다시 돌린 로그는 없다 — 10 (전체) 이 그것을 덮는다.
