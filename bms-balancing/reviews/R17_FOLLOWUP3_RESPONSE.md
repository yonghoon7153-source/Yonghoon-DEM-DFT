# R17 후속 **3차** NO-GO 대응 — 삭제의 근거 · 정상 비교의 표현 가능성 · 오류 판정의 경계

대상 리뷰: `reviews/r17_followup3/codex/R17_FOLLOWUP3_REVIEW.md` (NO-GO · P1 1 · P2 2).
리뷰어가 고정한 HEAD `e834b01e4066c5e78c06b6ed1f77878e5a27a481`, BMS 수정 커밋
`7f09804fdc6be2892746dece201b98da48aac6cd`.

**우리도 실측으로 확인했다**: `git diff 7f09804f..e834b01e -- bms-balancing` 은
`docs/ASSB_TRANSFER_NOTE.md` 한 문서뿐이고 Python/shell 차이는 없다 ·
`git diff e834b01e..HEAD -- bms-balancing` 은 이번 대응 **직전에 비어 있었다**.
리뷰어가 짚은 대로 직전 회신의 `a4c311ef` 는 **그 라운드의 검토 대상**이지 이번 수정 대상이
아니다 — 회신 문서에서 그 둘을 구분해 쓴다.

리뷰 패키지 원본은 `reviews/r17_followup3/` (zip 바이트 그대로 + `codex/` 풀어 둔 것, zip
sha256 `01f829e9e9f56204cee447c1b2bd2a2735c067768ca6736171230c4c0dce31bd`).

## 0. 한 줄

**경로를 아는 것과 그 바이트·존재를 아는 것은 다르다** (F3-01) · **한 의미를 두 이름으로 세면
정상 변경이 표현 불가능해진다** (F3-02) · **검사한 것과 소비하는 것이 또 갈라졌다** (F3-03).

앞 라운드의 한 줄("검사한 것과 사용한 것이 다르다")이 **같은 모양으로 한 번 더** 나왔다는
사실을 그대로 적는다 — F3-03 은 F2-06 을 고치면서 *찾기*는 넣고 *소비 경계*는 안 넣은 것이다.

## 1. 먼저 재현했다 (수정 전, 리뷰어 스크립트를 고치지 않고)

```
repro_followup3.py --part fast
  gc_valid_control        0    gc_changed_bytes        0  ← F3-01 ① (rc 2 여야 한다)
  gc_unindexed_control    2    gc_missing_retained     0  ← F3-01 ② (rc 2 여야 한다)
  receipt_valid_control   0    receipt_code_null       1  ← F3-03 (rc 3 여야 한다)
                               receipt_instrument_list 1  ← F3-03
  common_cycle_control 0 · common_cycle_999 0 · receipt_tree_instead_of_blob 0 (§5 관측)

repro_followup3.py --part producer
  starts1_single 0 · starts2_single 0
  starts_axis_compare 2 · n_multistart_axis_compare 2      ← F3-02 (rc 0 이어야 한다)
```

## 2. 발견별 대응

### F3-01 (P1) — 대조가 **단방향**이었다

`scripts/gc_partial.py`.

전 판은 `on_disk - known`(모르는 디렉터리)과 미등록 파일만 봤다 — 전부 *"디스크에 있는데
index 가 모르는 것"* 쪽이다. **반대 방향**은 아무도 안 봤다:

- **등록된 파일이 실제로 있는가**
- **그 경로의 바이트가 index 가 지목한 바이트인가**

그래서 둘이 뚫렸다 (리뷰어, **동시성 가정 없이 정적 상태로** 재현):

| 반례 | 전 판 | 지금 |
|---|---|---|
| 버릴 항목의 경로에 **다른 바이트** (index SHA 는 원래 것) | rc 0 · 다른 바이트 삭제, 로그엔 **원래 SHA** 인쇄 | **rc 2 · 삭제 0 · index 쓰기 0** |
| **최신 보존 파일 B 가 없음** (index·디렉터리는 그대로) | rc 0 · **유일하게 남은 A 삭제**, payload 0개 | **rc 2 · 삭제 0 · index 쓰기 0** |

**고침**: 삭제·보존을 가르기 **전에**, `index["attempts"]` **전체**에 대해 ① 기록 digest 가
64자리 hex 인가 ② 그 경로가 실재하는 **일반 파일**인가 ③ 그 바이트의 sha256 이 기록과 같은가
를 본다. 하나라도 어긋나면 **삭제 0 · index 쓰기 0 · rc 2**.

리뷰어 지적을 그대로 받는다 — *"`rmtree` 제거는 옳았지만, 삭제 단위를 파일로 줄이는 것과 그
파일의 동일성을 검증하는 것은 다르다."* **경로 집합은 파일 동일성이 아니다.**

우리가 더한 것 둘 (리뷰어가 따로 내지 않았지만 같은 계약의 반대편):

- **보존 쪽** 바이트가 바뀐 경우도 거부 (`test_fu3_03`) — 계약이 "삭제·보존 **전체** 항목" 이다.
- **dry-run 도 거부** (`test_fu3_07`). dry-run 의 출력은 *무엇을 지울지*의 예고이고, 예고가
  틀린 바이트를 가리키면 사람이 그것을 믿는다.

보존한 것: 정상 GC rc 0 · 서로 다른 artifact 보존(A/100·A/200·B/100) · 미등록 파일 rc 2 ·
path↔tuple alias rc 2 · escape·중복 rc 2.

**동시 게시는 이번 범위가 아니다.** 리뷰어가 *"이번 두 반례를 동시성 문제로 돌리지 말 것"*
이라고 했고 그러지 않았다 — 위 둘은 전부 **GC 시작 전의 정적 상태**다. crash/동시 GC 의 완전한
안전성은 이 라운드가 검증하지 않았고, 그렇다고 적는다.

### F3-02 (P2) — 한 의미를 두 이름으로 세지 않는다

`scripts/width_report.py`.

`fit_cycles.py` 는 `--starts` **하나**를 받아 sidecar 에 `starts` 와 `n_multistart` 로 **두 번**
적는다. 단일 파일 안에서 둘의 일치를 요구한 것(F2-02)은 옳지만, 비교에서 **독립 축 둘로 세면**
정상 변경이 어느 이름으로도 표현되지 않는다 — `--axis starts` 면 `n_multistart` 가,
`--axis n_multistart` 면 `starts` 가 남아 **둘 다 rc 2** 였다.

**고침**: `SETTING_ALIASES = (("starts", "n_multistart"),)` 와 `alias_group()` 을 두고,
`guard_same_except` 가 고른 축의 **무리 전체**를 뺀다. "축이 안 움직였다" 판정도 무리 단위로
본다. 무리 안의 일치는 파일마다 `_typed_meta_problems` 가 이미 요구하므로, 무리를 통째로 빼도
"축 하나만 다르다" 는 약해지지 않는다 — 무리 **밖** 설정은 전부 그대로 본다.

리뷰어의 금지 조건(*"목록에서 아무 검사나 빼서 양성만 열지 말 것"*)을 음성 대조군 넷으로 고정했다:

| 시험 | 입력 | 기대 |
|---|---|---|
| `test_fu3_10` | 단일 파일 안 `starts != n_multistart` | rc 2 |
| `test_fu3_11` | 행의 `n_starts` 가 sidecar 와 불일치 | rc 2 |
| `test_fu3_12` | starts 말고 **seed 까지** 바뀜 | rc 2 |
| `test_fu3_13` | 고른 축이 **안 움직임** (같은 파일 두 벌) | rc 2 |

### F3-03 (P2) — 찾아 놓고 그 객체를 계속 썼다

`scripts/verify_run_receipt.py`.

`_typed_problems` 는 `code=null`·`instrument=["not-a-map"]` 을 **찾는다**. 그런데 바로 아래가
같은 객체에 `r["code"].get(...)` · `instrument.items()` 를 불렀다 → `AttributeError` · **rc 1** ·
`RUN_RECEIPT_VERIFY` 출력 없음. 리뷰어가 분명히 한정한 대로 **verified=true 로 수용한 반례가
아니라** 구조화 실패 경로의 문제다.

**고침 둘**:

1. **구조가 틀린 필드에 기대는 검사는 수행하지 않는다.** `code` 가 객체가 아니면 ancestry·tree 를
   돌리지 않고, `code`/`instrument` 중 하나라도 객체가 아니면 instrument 대조를 돌리지 않는다.
2. **수행하지 못한 검사를 성공으로 채우지 않는다.** 그 자리는 `None`(안 함)이고, 판정 객체에
   `unperformed: {검사: 사유}` 를 새로 실어 **왜** 못 했는지 드러낸다. `code_reference_verified`
   는 `is True` 로만 센다 — `None` 은 확인이 아니다. `--skip-instrument` 의 `None`(합법적으로
   뺀 것)과 구조가 틀려 못 한 `None` 을 `unperformed` 가 가른다.

리뷰어의 금지 조건(*"rc 1 을 단순히 3 으로 바꾸고 판정 객체를 잃은 채 두는 수정은 불충분"*)을
`test_fu3_14`/`test_fu3_15` 가 고정한다 — traceback 없음 · rc 3 · `RUN_RECEIPT_VERIFY` 존재 ·
`verified=false` · `checks.complete=false` · `checks.ancestry`/`tree` 가 **`None`**.

## 3. §5 의 별도 권고 셋 — 결정하고 닫았다

리뷰어가 **독립 결함으로 세지 않은** 것들이다. 그대로 두지 않고 결정했다.

| # | 리뷰어가 요구한 결정 | 우리 결정 | 회귀 |
|---|---|---|---|
| §5-1 | 공통 receipt 의 `cycle` 키를 **금지할지 무시 가능으로 명시할지** | **금지**. 공통은 정의상 cycle 을 말하지 않는다 — 거기 적혀 있으면 생산자·sidecar 중 하나가 틀린 것이고, 전 판은 그것을 행의 cycle 로 **조용히 덮어썼다**. 조용한 정정은 틀린 선언을 지운다 | `test_fu3_19` · 양성 `test_fu3_20` |
| §5-2 | instrument 가 **파일 전용인지 tree 도 허용인지** | **파일 blob 전용**. `rev-parse <commit>:./<rel>` 은 디렉터리면 tree OID 를 주고 전 판은 그것도 `ok` 였다. 무결성 우회는 아니지만 **문서가 blob 이라고 적고 있었다** — 도구는 파일이므로 계약을 문서 쪽에 맞췄다 (`cat-file -t` 가 `blob` 일 때만 ok) | `test_fu3_21` |
| §5-3 | 비정상 solver 반환까지 방어하는 계약을 유지할지 | **유지한다**. 최종 SLSQP `r.x` 에도 `_in_box` 를 건다 — "모든 후보에 같은 술어" 는 solver 가 돌려준 점도 후보라는 뜻이다 | `test_fu3_22` |

§5-3 의 범위를 리뷰어가 한정한 그대로 유지한다: **실제 SciPy 가 그 반환값을 만들었다는 native
반례가 아니다.** 우리 회귀도 `unittest.mock` 으로 SLSQP 반환을 **명시적으로 주입**해서 그
술어가 걸리는지만 본다 — 과학 결과 오류로 세지 않는다.

## 4. 수정이 그 축을 무는지 — 변이로 확인

새 회귀가 **자기 축이 아닌 이유로** 초록일 수 있으므로(앞 라운드에서 실제로 그랬다) 각 수정을
되돌려 봤다:

| 변이 | 빨개진 시험 | 확인한 것 |
|---|---|---|
| F3-01 의 존재·digest 대조 건너뜀 | `fu3_01` · `02` · `03` · `04` · `07` (양성 `05`·`06` 은 초록 유지) | 다섯이 전부 새 검사에 걸린 것이다 |
| `alias_group(axis)` → `(axis,)` | `fu3_08` ×2 (`09`·`12`·`13` 초록 유지) | 별칭 정규화가 실제로 여는 것이다 |
| `code_shaped`/`inst_shaped` → `True` | `fu3_14` ×3 · `fu3_15` (`16`·`18` 초록 유지) | 구조 경계가 실제로 막는 것이다 |

## 5. 깨진 fixture

| fixture / 문서 계약 | 무엇이 틀렸나 | 고침 |
|---|---|---|
| `tests/test_r17_followup3.py::starts_pair` (내가 쓴 것) | tag 마다 `_synth_root` 를 **따로** 만들어 `consumed_inputs` 의 **경로**가 달라졌다 → `guard_same_identity` 가 먼저 막았다. **fixture 가 축을 하나 더 흔들고 있었다** (리뷰어는 같은 workbook 으로 두 번 돌렸다) | 합성 원자료·workbook 을 **한 번** 만들어 두 실행이 공유 |
| `WORKING_STATE.md` 의 "N passed 기대" | 493 (R6 내부 DF-04 의 문서 계약) | **519** (새 회귀 26건) |

기존 fixture 는 이번엔 하나도 깨지지 않았다 — 앞 라운드에서 이미 실제 producer 계약으로
맞췄기 때문이다 (F2-04 의 `per_cycle_receipt` 공유, `dataset_manifest` 발행자 모양,
행의 `n_starts`·`scale_seed` 실제 값, receipt 의 `{python, platform}`).

## 6. 실행 결과 (이 회신 직전, 실측)

```
python3 -m pytest tests/test_r17_followup3.py -q    26 passed        (53.68s)   EXIT=0
  첫 실행(수정 전) 11 failed · 11 passed — 그중 둘은 내 fixture 문제였고 §5 에 적었다

python3 -m pytest tests/ -q                        519 passed      (688.71s)  EXIT=0
  수집 개수 519 = WORKING_STATE.md 의 "N passed 기대" (R6 내부 DF-04 의 문서 계약)
  도중 한 번은 1 failed · 518 passed 였고 그 1 은 **문서 계약 그 자체**였다 (493 → 519)

리뷰어 재현기 — 우리가 한 줄도 고치지 않고 다시 돌렸다 (스크래치패드 사본):

repro_followup3.py --part fast                     수정 전 → 지금
  gc_changed_bytes                                     0 → 2      ← F3-01 ①
  gc_missing_retained                                  0 → 2      ← F3-01 ②
  receipt_code_null                                    1 → 3      ← F3-03
  receipt_instrument_list                              1 → 3      ← F3-03
  common_cycle_999                                     0 → 2      ← §5-1 (금지 결정)
  receipt_tree_instead_of_blob                         0 → 3      ← §5-2 (blob 전용 결정)
  optimizer_out_of_box_fault  LAM_PE.min  −733.3333 → −16.0       ← §5-3 (참 상자 ±16.6667 안)
  대조군 유지: gc_valid_control 0 · gc_unindexed_control 2 ·
              common_cycle_control 0 · receipt_valid_control 0

repro_followup3.py --part producer
  starts1_single 0 · starts2_single 0                    (유지)
  starts_axis_compare                                  2 → 0      ← F3-02
  n_multistart_axis_compare                            2 → 0      ← F3-02

repro_followup2.py (47 case)   **리뷰어 관측과 한 칸도 다르지 않다** (회귀 없음)
repro_producer_reader.py       rc 0 · 축 분리 대조군 rc 2 · check_rows [] (F2-04 유지)
```

## 7. 이 라운드가 하지 않은 것

- **실데이터 재적합·A/B 재실행·과학 결과 갱신** — 이번 검토가 승인하지 않았고 하지 않았다.
- **동시 게시/crash 중 GC 의 안전성** — F3-01 의 두 반례는 정적 상태이고, 동시성은 별도 계약이다.
  리뷰어도 *"본 리뷰는 crash/동시 GC 의 완전한 안전성까지 검증하지 않았다"* 고 적었다.
- **Windows 집계의 대체** — 리뷰어의 **357 passed · 110 failed · 26 errors**(493 수집)를 우리
  Linux 숫자로 바꾸지 않는다. 리뷰어 분류(기존 실패 108 유지 · 새 비통과 28 은 전부 `fcntl`
  부재 · 새 회귀 파일의 나머지 13 통과)를 그대로 인용한다.
- **package 독립 실행 증명** — 미착수. `check_u14 --new out --schema-only` 의 rc 0 은
  `promotion_eligible=true` 가 아니고, legacy 는 rc 2 · 52/25/10/1 인 것도 그대로다.
- **모든 가능한 metadata schema 완전성의 증명** — F2-03 에서 리뷰어가 한정한 그대로, 요구한
  축만 닫혔다고 적는다.
