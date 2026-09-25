# 73차 게이트 리뷰 요청 — 72차 잔여 하나(E3-R 원장 `evidence.out` 결속)에 대한 답 · **한정 실행 GO 재요청**

> **상태: 확정 (2026-09-25).** 72차 회신(한정 GO 보류 — 잔여 **E3-R 원장 실행 자리 결속 [P1] 1건**, E9-R·D7~D9·E6 수용)의 §4.5 유한 종결 조건 ①②③ 에 답한다.
> 범위는 리뷰어가 정한 대로 **"E3-R 원장 실행 자리 필수화/멱등 순서 수정만"** 이다. E9 를 다시 열지 않았고, E1/E2/E4·서명·새 principal·과거 class 이관은 요구되지 않았고 하지 않았다.
> 계획 항목(prospective)은 아직 쓰지 않았다 — 리뷰어: "GO 가 아직 없으므로 prospective 를 쓰거나 본 실행을 시작하지 않는다."

## 판정 대상 (이 블록이 정본이다)

| 항목 | 값 |
|---|---|
| 요청문 커밋 | `(이 파일을 담은 커밋 — 발송문에 실측해 적는다)` (브랜치 head SHA 와 함께, 커밋 뒤 실측) |
| **판정 대상 코드** | **`7a7945564e6a94803b4d3bc72e8202534189ccdb`** — RUN_SCOPE 마지막 변경 커밋 (72차 E3-R 잔여, `tools/preserve.py`) · `source_digest` **`c2ef1a811e70bb4c`** (72차 대상 `82854571` · `518d4f63076b77e3` → `7a794556` · `c2ef1a811e70bb4c`). 그 뒤 커밋은 영수증·원장·시험(구조 회귀의 패키지 제외)·문서뿐 (RUN_SCOPE diff 0) |
| 리뷰 원자료 | 72차 패키지 `docs/22p_gap/gate72_review/` (zip `9ae5356c…`, MANIFEST 48/48) — `-text !eol` 규칙 먼저 커밋 |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §96(접수) · §97(대응) · 작업 상태 `docs/GATE70_WORKING_STATE.md` |
| 새 시험 | `tests/test_gate72_defensive.py` 10 node (RED 5 → GREEN 10) · 변이 1 신규 + 1 재조준 (`mutation_replay.py -k g72`, `-k attach-binds`) |

## §0 72차 잔여에 대한 답 (§4.5 ①②③)

| 조건 | 이번 상태 | 근거 |
|---|---|---|
| ① 신규 pending→full_bundle: `evidence.out` **필수** 비어 있지 않은 문자열 · 결속 자리와 일치 · 부재 skip 금지 | **닫음** — `_assert_ledger_run_bound()`: out 이 비어 있지 않은 str 이 아니면 **미결속** 거부, 있으면 posix 정규화 뒤 영수증·묶음이 결속한 복원 자리와 일치해야 진행. 71차의 `if "out" in ev:` 선택적 분기 삭제 | A02 `test_g72_a02` · A02b(빈/공백/int/list) · A01 `test_g71_e3r_07b` · 변이 `ledger-run-location-is-mandatory-g72` |
| ② 멱등 성공 이전에도 결속 확인 · 역사적 out 부재는 소급·재작성 없이 미결속/거부 | **닫음** — 원장 lock 안에서 실행 기록을 읽자마자, **full_bundle 멱등 분기보다 먼저** 결속을 확인한다. 실물 `paired_fixed5_v4`(소급 다리, out 없음)는 원장 **사본** 위에서 attach → 미결속 거부, 운영 원장 바이트 불변 — 소급해서 채우지 않았다 | A04 `test_g72_a04` · A05 `test_g72_a05` · A06 (다른 영수증 + out 누락 — 결속 검사가 identity 비교보다 먼저) · A07 실물 · 변이 `attach-binds-the-ledger-run-location-g71` (재조준: 07b + A04) |
| ③ 정상 + pending 누락/불일치 + full_bundle 누락/불일치 회귀 · 거부 시 원장 불변 | **닫음** — 리뷰어 표 6경우: A00(`e3r_00`) · A01(`e3r_07b`) · A02 · A03(`test_g72_a03` 멱등 양성, 바이트 불변) · A04 · A05. 모든 부정 시험이 원장 바이트를 전후 대조 | `tests/test_gate72_defensive.py` |
| E9-R · D7~D9 · E6 · E1/E2/E4 · E5 · E7 · E8 · E10 | 72차 수용 — 변경 없음 | — |

## §1 결과 라벨 — 72차 §1 그대로, attach 문장만 갱신

> **archive / 복원 / retention:** archive_results.sh + make_receipt(empty-root 복원·재채점) 수행, `attach_bundle_evidence`(짝·일치·source fits·복원 자리·봉인 summary·**원장 실행 자리 필수** 결속) 수행; retention/object-lock/power-loss 는 미수행·보증 안 함.
> (나머지 문장 — 실행 허용 범위 · 코드/입력/실행 식별 · 현지 검증 · E1/E2/E4/E6 한계 · 실패 처리 — 는 72차 §1 과 같다. 현지 검증 수치는 §4.)

## §2 실행 명세 — 72차 §2 (= 71차 §2 + D6~D9) 그대로. 바뀐 것 없음

E9-3 4단계의 `attach_bundle_evidence('grid_fit_v5', …)` 는 이제 원장의 `evidence.out`(run.sh `leg_finalize` 가 적는 `--out` 값 = `results/grid_fit_v5`) 이 묶음 `restore_map.run_dir` · 영수증 `restore.run_dir_relative` 와 같아야만 올린다.

## §3 리뷰어에게 묻는 것

1. **E3-R 종결 수용** — §4.5 ①②③ 이 닫혔는가 (예/아니오, 아니오면 남은 조건 한 줄).
2. **한정 실행 GO** — 예이면 `7a7945564e6a94803b4d3bc72e8202534189ccdb` + (GO 뒤) 사람이 커밋한 계획 항목에 한정 실행 GO 인가 (예/아니오/조건부).

## §4 실행 출력 (커밋 뒤 실측)

```
판정 대상 코드                                7a7945564e6a94803b4d3bc72e8202534189ccdb
source_digest                                 c2ef1a811e70bb4c
전체 pytest (tests/)                          0 failed · 1879 passed · 2 xfailed (35:26)   (시작 HEAD = 끝 HEAD = cfacfe6b44a27ee34af536cc84f29806d916f392 · 미추적 0)
strict smoke (scripts/smoke_e2e.sh)           EXIT 0
pytest gate63~72 묶음                          162 passed · 1 xfailed (gate63~68 + gate70~72, 21.2 s)
mutation_replay --check-preimages · -k premise · -k g70 · -k g71 · -k g72   전 지점 1회 · 4/4 · 4/4 · 3/3 · 1/1
등록부                                        tracked 367 · 디스크 367 · 미추적 0
```

## §5 우리가 스스로 신고하는 것

- 역사적 `paired_fixed5_v4` 원장 기록에는 `out` 이 없고 **그대로 둔다** — attach 는 그것을 미결속으로 거부한다 (A07). 그 다리의 `full_bundle` 상태 자체는 24~27차에 사람이 검증·기록한 것이고 이번 소비자가 만든 것이 아니다.
- 72차 §5 그대로: 영수증 서명 없음 · restore_map 은 묶음 구성원(payload index 안)이지 독립 attestation 이 아님 · 실물 양성 대조군은 RUN_SCOPE 가 바뀔 때마다 영수증 재생성 (`54d50763`).
- 첫 전체 회귀(`54d50763`)는 **1 failed** 였다 — 구조 회귀 `test_every_callsite_of_the_raw_sink_is_inside_the_publisher` 가 72차 패키지의 `reference/tools/preserve.py` 사본을 코드로 셌다. 패키지는 고치지 않고 시험이 리뷰 패키지 디렉터리를 건너뛰게 했다 (`cfacfe6b`, 시험만 · RUN_SCOPE diff 0). §4 는 그 뒤 재실행 수치다. 처음 실패를 숨기지 않는다.
- 수치는 송신 실행 증거다.

## §6 예산과 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **한정 실행 GO 를 재요청한다.**
