# R17 후속 **2차** NO-GO 대응 — 검사한 것과 지운 것, 공통과 사이클별

대상 리뷰: `reviews/r17_followup2/codex/R17_FOLLOWUP2_REVIEW.md` (NO-GO · P1 4 · P2 2).
리뷰어가 고정한 대상 `a4c311eff898615932ae6f333bbb26b605abf762`, BMS 수정 커밋
`8733453351b5570c0dc0b0182ae7c490f900b380`. **우리도 `git diff 87334533..a4c311ef -- bms-balancing`
이 비어 있는 것을 실측으로 확인했다** — 리뷰어가 본 코드와 우리가 고친 코드가 같다.

리뷰 패키지 원본은 `reviews/r17_followup2/` (zip 바이트 그대로 + `codex/` 풀어 둔 것, zip sha256
`476a82214422069e168ca96e5334c5aa389bc021b991f77e52cb737106564483`).

## 0. 한 줄

**실패 입력을 막는 검사가 계약을 닫지는 않았다.** 세 축으로 갈라진다:

- **범위** — 검사는 파일 하나에 하고 삭제는 디렉터리째 했다 (F2-01).
- **결속** — 행에만 남은 실행 조건 둘이 비교 목록에 없었고 (F2-02), 필수 값의 **안쪽**은 아무거나
  될 수 있었다 (F2-03), 영수증의 nested schema 는 바깥 컨테이너에서 멈췄다 (F2-06).
- **공통과 사이클별** — 이것이 이번 라운드의 진짜 발견이다. reader 가 요구한 "동일" 은 **정상
  생산자가 만족할 수 없는 조건**이었고, 합성 fixture 가 모든 행에 같은 receipt 를 넣어 그것을
  가리고 있었다 (F2-04). 그리고 `best` 는 "모든 후보에 같은 술어" 에서 여전히 빠져 있었다 (F2-05).

리뷰어가 정한 순서 그대로 닫았다: **F2-04 양성 경로 → F2-01 보존 범위 → F2-02/03/05/06 공통 계약.**

## 1. 먼저 재현했다 (수정 전, 리뷰어 스크립트를 고치지 않고)

| 스크립트 | 결과 |
|---|---|
| `repro_producer_reader.py --target <BMS_DIR>` | **F2-04 재현** — `rc 2`, `! 행 0 의 receipt 가 sidecar 의 입력과 다르다`. 축 분리 대조군(행 receipt 의 `cycle` 만 제거)은 `rc 0` |
| `repro_followup2.py --target <BMS_DIR>` (47 case) | **여섯 건 전부 재현**. 대조군도 리뷰어 관측대로: escape rc 2 · duplicate rc 2 · unknown_dir rc 2 · body_* rc 2 · null_* rc 2 · receipt 최상위 rc 3 · infeasible best RuntimeError |

리뷰어가 `fcntl` 부재로 "게시 CLI 전체 성공" 을 주장하지 않은 것을 그대로 받는다. **이 기계는
Linux 라 그 제약이 없어서**, 우리 양성 E2E 는 API 가 아니라 **실제 게시 CLI**(`scripts/fit_cycles.py`,
`publish_lock` + 원자적 게시 포함)로 돌린다 — 리뷰어 재현기보다 한 단계 더 실물이다.

## 2. 발견별 대응

### F2-01 (P1) — 재귀 삭제를 **버렸다**

`scripts/gc_partial.py`.

| 반례 | 전 판 | 지금 |
|---|---|---|
| `gc_retained_path_alias` — 항목이 `kind/attempt=matrix/C` 라고 선언하면서 `path=matrix/A/matrix_200.csv` 를 가리킨다 | rc 0 · **보존 index 가 가리키는 A/200 이 삭제**됨 | **rc 2 · 삭제 0건** |
| `gc_unknown_file` — 정상 index 의 A 디렉터리에 미등록 파일 하나 | rc 0 · 그 파일도 삭제 | **rc 2 · 삭제 0건** |

셋을 했다:

1. **항목 tuple ↔ payload 경로의 관계를 전체 index 에 대해 먼저 검증한다.** `record_partial` 은
   언제나 `path = kind/attempt/artifact` 로 쓰므로(`verify.py` 의 `dest.relative_to(root)`)
   이 관계는 **생산자의 불변식**이다. 어긋난 index 는 손상된 것이고, 해석해 주지 않는다.
2. **`③ 모르면 안 지운다` 를 파일 단위까지 내렸다.** 전 판의 `unknown` 은 시도 **디렉터리**만
   열거했는데 `rmtree` 는 그 안의 파일을 봤다 — 회신 §5 의 "원장에 없는 파일도 rc 2" 는
   **사실이 아니었다.** 정정하고 코드를 그 문장에 맞췄다.
3. **`shutil.rmtree` 를 코드에서 제거했다.** 리뷰어가 제시한 최소 구현 그대로 — 검증한 **개별
   파일만** 지우고 **빈 디렉터리만** `rmdir` 한다. `rmdir` 은 비어 있지 않으면 실패하므로
   미등록 파일·보존 payload 가 남은 디렉터리는 **정의상** 지워지지 않는다. "재귀 삭제를 유지하면
   전체 하위 파일의 정책을 검사해야 한다" 는 조건을 검사로 만족시키는 대신 **재귀를 없앴다.**

보존한 것: 중복 참조 rc 2 정책(리뷰어가 수용한 그대로) · escape rc 2 · 원 반례(A/100·A/200·B/100)의
rc 0 과 A/200 보존. 새로 고정한 대조군: **전부 버려진 시도 디렉터리는 여전히 정리된다**
(보존 우선이 "아무것도 안 지운다" 로 넘어가지 않는지 — `test_fu2_10`).

### F2-02 (P1) — 행에만 남아 있던 실행 조건 둘

`scripts/width_report.py` `BODY_META_BOUND` 에 **`scale_seed↔scale_seed` · `n_starts↔n_multistart`**
를 더했다. 이 목록은 "한 파일 안에서 하나" 와 "sidecar 와 같다" 를 **동시에** 요구하므로 파일 내
혼합(`width_row_scale_mixed`)도 같이 닫힌다. sidecar 가 같은 것을 두 번 적는 자리
(`starts` ↔ `n_multistart`)의 일치도 새로 본다.

`si_source` 는 **넣지 않았다** — 리뷰어 지적대로 현재 `CYCLES_ROW` 에 없는 열이고, 없는 열을
결속 목록에 적으면 `row_key not in rows[0]` 로 조용히 건너뛰는 항목이 하나 늘 뿐이다.

### F2-03 (P1) — 규칙을 새로 적지 않고 **발행 쪽 정본을 불렀다**

`_typed_meta_problems` 가 이제 이렇게 본다:

| 축 | 누가 규칙의 정본인가 |
|---|---|
| `env` 여섯 축의 존재·비공백 | `schema.env_axes_missing()` (R14 P2-2 가 "규칙이 두 벌" 을 고친 그 함수) |
| 상자 `lb`/`ub` 의 5차원·유한·순서 | `verify.resolve_box()` (적합이 쓰는 그것) |
| `initial` | 5개의 유한한 수 **이고 그 상자 안** |
| `dataset_manifest` | `data.half_cell_manifest_identity()` 가 내는 `{version, dataset_id, sha256(64hex)}` |
| `width_starts`·`width_grid` | 행이 전부 `measured` 면 폭은 켜져 있었다 → `0 이상의 정수` (null 불가) |
| `starts`·`seed`·`scale_seed`·`n_multistart` | 정수 |
| `si_source`·`optimizer`·`width_method`·`cell` | 비지 않은 문자열 |
| `w_pocv`·`w_dvdq`·`w_dqdv` | 유한한 수 |

**각 파일의 유효성을 동등성보다 먼저** 본다 — 두 파일의 잘못된 값이 같다는 사실은 "같은 환경" 이
아니다. **합법 nullable 은 건드리지 않았다**: `gamma_lb` · `gamma_init` · `literature` 는 `None`
이어도 통과하고, 그것을 대조군으로 고정했다 (`test_fu2_15`).

옛 sidecar(나중에 더해진 `openpyxl` 축이 키째 없는 것)는 **거부하되 사유에 그것이 나이임을 적는다**
(`test_fu2_16`). 조용히 통과시키지 않고, "환경 동일 확인" 과 섞지도 않는다.

### F2-04 (P1) — 공통 receipt 와 사이클별 receipt 는 **다른 것**이다

이번 라운드에서 제일 중요한 발견이다. 리뷰어 문장을 그대로 받는다: *"여러 행에 각각 다른 cycle 을
기록한 정상 producer 가 이 조건을 만족할 수 없다."*

계약을 **함수 하나**로 만들었다 — `bms_balancing/schema.py`:

```python
def per_cycle_receipt(common: dict, cycle) -> dict:
    """공통 receipt + 그 행의 cycle → 그 행의 receipt."""
    return dict(common, full_cell=dict(common["full_cell"], cycle=int(cycle)))
```

- **producer** (`cycles.py:206`) 가 손으로 쓰던 dict 를 이 함수 호출로 바꿨다 (바이트는 그대로).
- **reader** (`width_report.py` ④) 가 sidecar 의 공통 receipt 와 **그 행의 cycle** 로 기대 receipt 를
  **구성해** 정확 대조한다. 부분 비교로 느슨해진 것이 아니라 **비교 대상이 바뀐 것**이다 —
  digest 도 그 기대 receipt 의 것이어야 한다.
- 행 cycle 의 **정수성 검사를 ④ 앞으로 옮겼다** (기대 receipt 를 그 cycle 로 만들기 때문). 규칙은
  그대로이고, 소수 cycle 은 여전히 rc 2 다.

규칙이 두 자리에 따로 있으면 절반만 구현된다 — 이 저장소가 R14 P2-2 에서 겪은 일이고, 이번엔
producer 와 reader 가 **같은 함수**를 부른다.

닫은 음성 축(각각 별도 회귀):

| 시험 | 입력 | 기대 |
|---|---|---|
| `test_fu2_02` | 행 0 의 receipt 가 **행 1 의 cycle** | rc 2 |
| `test_fu2_03` | 행 receipt 에 `cycle` 이 **없다** (리뷰어의 축 분리 대조군 — 전 판 rc 0) | rc 2 |
| `test_fu2_04` | cycle 은 맞는데 **workbook SHA** 가 다르다 | rc 2 |
| `test_fu2_05` · `test_fu2_06` | cycle 누락 · 중복 | rc 2 |

그리고 **양성**: `test_fu2_01` 이 합성 원자료 → `scripts/fit_cycles.py` (실제 게시 CLI) →
`scripts/width_report.py` 를 한 줄로 잇고 rc 0 을 요구한다. 전제도 같이 고정한다 — 행이 실제로
`full_cell.cycle = 0/1` 을 달고, sidecar 의 공통 receipt 에는 `cycle` 이 **없다**.

`test_widths._fake_widths_csv` 가 모든 행에 같은 receipt 를 넣어 이 충돌을 가리고 있었다는 리뷰어
지적을 받아 **그 fixture 를 실제 producer 모양으로 고쳤다** (§4).

### F2-05 (P2) — `best` 도 후보다

`bms_balancing/verify.py` `near_optimal_extrema`. `best[0]=NaN` 이면 선행 비교 두 부등식이
**둘 다 false** 라 상자 검사를 통과했다. 셋을 했다:

1. `best` 의 **유한성을 먼저** 본다 (`_in_box` 와 같은 술어를 best 에도 적용한다는 뜻이다).
2. mode 계산의 기준(`ref_p`·`ref_c`·`c_cell`)도 유한해야 한다.
3. **최종 끝점까지 같은 경로에 묶었다** — 후보 mode 값에 비유한이 있으면 `RuntimeError` 다.
   비유한 끝점은 폭이 **없는 것**이지 넓은 것이 아니다.

`cycles._width_fields` 가 그것을 받아 `width_status='failed'` 로 적는다 (`test_fu2_18`). 정상
입력이 계속 `measured` 인 것(`test_fu2_19`)과 상자 밖 seed 거부(`test_fu2_20`)를 대조군으로 뒀다.

리뷰어의 **추가 관측**(외부 기준 `best_val` 을 허용하는 API 의 이름·문서 문제)은 독립 건수에
넣지 않은 것 그대로 두되, 우리도 새 주장을 하지 않는다 — 현재 술어는 "전달된 best 가 그 limit
안인가" 와 "`obj(best)` 가 그 limit 안인가" **둘 다** 보고, `obj(best) == best_val` 을 보증한다고는
적지 않는다.

### F2-06 (P2) — nested schema 를 생산자와 소비자가 **같이** 쓴다

`reviews/evidence_gate.py` 에 계약을 적었다:

```python
RUN_RECEIPT_RUNTIME_KEYS = ("python", "platform")
def runtime_problems(rt) -> list          # 두 축이 있고 비공백 문자열 · 계약 밖 키는 부분 상태
def materialized_problems(m) -> list      # None 또는 {mode: 비공백 문자열}
```

- **생산자** `run_receipt()` 가 서명 **전에** 거부한다 — 소비자만 조이면 "발행은 되는데 아무도 못
  읽는" 영수증이 생긴다.
- **소비자** `scripts/verify_run_receipt.py` 가 같은 함수를 부른다. `runtime={python:null,platform:null}` ·
  `{irrelevant:true}` · `{python:"  ",platform:"\t"}` · `materialized={mode:17}` → **rc 3**.
- `materialized=None` 은 **합법으로 유지**한다 (생산자가 실제로 내는 상태다).
- **부분/unknown 을 complete 와 구분해 드러낸다**: 판정 JSON 에 `runtime_partial` 을 새로 싣는다.

대조군: 실제 생산자 `gate.run_receipt(...)` 가 내는 모양은 계속 rc 0 (`test_fu2_22`) ·
`materialized=None` 도 rc 0 (`test_fu2_23`).

package 내용 digest 에 대한 리뷰어의 종결 인정은 받고, **범위를 넓히지 않는다** — 그것은 *목록이
가리키는 파일의 내용 주소*이고, 실제 실행·독립 replay·디렉터리의 모든 파일·manifest 원문을
인증한다고 적지 않는다. "consumer 가 package bytes 를 재검증한다" 는 표현도 쓰지 않는다.
알고리즘 정의(`hash + 이름` 전체 줄 정렬)와 문서 문장의 불일치는 §5 에 정정으로 적는다.

## 3. RED 관측과 **처음부터 통과한 것의 처리**

새 회귀 `tests/test_r17_followup2.py` 41건. 첫 실행 **15 failed · 26 passed**.

그런데 **통과한 26 중 일부는 이유가 틀렸다** — F2-04 때문에 reader 가 ④ 에서 먼저 rc 2 를 내서,
F2-02·F2-03 의 시험들이 *자기 축이 아닌 이유로* 초록이었다. CLAUDE.md 규율 2 가 말하는
"fixture 가 진실을 가린다" 의 정확한 사례다. 그래서 F2-04 를 먼저 고친 뒤, 각 축이 **정말 그것을
무는지** 변이로 확인했다:

| 변이 | 빨개진 시험 | 확인한 것 |
|---|---|---|
| `BODY_META_BOUND` 에서 새 쌍 둘 제거 | `fu2_11` ×2 · `fu2_12` ×2 | 행 결속이 그 두 열을 실제로 본다 |
| `starts ↔ n_multistart` 일치 검사 제거 | `fu2_13` | 두 선언 사이 관계가 실제로 걸린다 |
| F2-03 의 새 검사 전체 건너뜀 | `fu2_14` ×11 · `fu2_16` | 11 case 가 전부 새 검사에 걸린 것이다 |
| receipt 비교를 **cycle 무시**로 (전형적 오답) | `fu2_02` · `fu2_03` (`fu2_01`·`fu2_04` 는 초록 유지) | 양성을 열면서 cycle 축을 잃지 않았다 |

수정 뒤 **41 passed**.

## 4. 깨진 fixture — 그것이 정상이다

리뷰어가 지목한 대로 `tests/test_widths.py::_fake_widths_csv` 의 공통 receipt fixture 가 실제
producer 계약과 달랐다. validator 를 강화하면 **fixture 가 먼저 깨져야** 정상이고, 안 깨지면 그
fixture 가 위조 통로였다는 뜻이다 (이 저장소에서 다섯 번째 관측).

| fixture | 무엇이 자리표시였나 | 고침 |
|---|---|---|
| `tests/test_widths.py::_fake_widths_csv` | 모든 행에 **공통 receipt** 를 넣었다 (`_FAKE_CONSUMED` 그대로) — producer 는 행마다 `full_cell.cycle=k` 를 붙인다 | `S.per_cycle_receipt(_FAKE_CONSUMED, k)` — fixture 도 producer·reader 와 **같은 함수**를 쓴다 |
| 같은 fixture 의 sidecar | `dataset_manifest = {"id": "fake-manifest"}` — 발행자가 내는 모양이 아니다 | `{version, dataset_id, sha256(64hex)}` |
| `tests/test_r17_codex.py::_width_pair` · `tests/test_r17_followup.py::_width_pair` | 행의 `n_starts`·`scale_seed` 가 채움값 `"1"` 이었다 (sidecar 는 20/0) · 공통 receipt · 같은 `dataset_manifest` | 행에 실제 값 · per-cycle receipt · 발행자 모양의 manifest |
| `tests/test_r16_run_receipt.py::_receipt` | `runtime={"python": "3.12.3"}` — 실제 발행자는 `{python, platform}` 둘을 쓴다 (`replay_codex_r11.py:356`) | 두 축을 채웠다 |
| `WORKING_STATE.md` 의 "N passed 기대" | 452 (R6 내부 DF-04 의 문서 계약) | **493** (새 회귀 41건) |

그리고 하나 더 — **리뷰어 재현기의 양성 대조군도 같이 고쳐졌다.** `repro_followup2.py` 는
우리 `tests/test_widths.py::_fake_widths_csv` 를 **import 해서** 쓴다(그 스크립트 43행). 그래서
fixture 를 producer 계약으로 맞추자 리뷰어의 `width_positive` 도 rc 0 을 유지한다 — 우리가 그
스크립트를 고친 것이 아니다 (한 줄도 건드리지 않았다).

## 5. 정정

- **회신 §5 의 "원장에 없는 파일도 unknown 검출에서 rc 2"** 는 당시 코드와 달랐다. 리뷰어 지적이
  맞다. 지금은 사실이고(F2-01 2번), **문장이 아니라 코드를 고쳐서** 맞췄다.
- **`package_content_digest` 의 문서 문장**: "이름으로 정렬" 이라고 적었지만 구현은
  `"<sha256>  <이름>"` **줄 전체**를 정렬한다. 결정성은 있으므로 리뷰어가 새 버그로 세지 않은 것을
  받고, **문서를 구현에 맞춰 고쳤다** — 누락/중복 이름·범위 밖 이름·manifest 원문 포함 여부의
  계약은 아직 정하지 않았고, 정하지 않았다고 적는다.
- `_fake_widths_csv` 를 "실제 producer 모양" 이라고 적었던 주석은 **cycle 축에서 거짓이었다.**
  정정하고 고쳤다.

## 6. 실행 결과 (이 회신 직전, 실측)

```
python3 -m pytest tests/test_r17_followup2.py -q     41 passed        (56.32s)   EXIT=0
  첫 실행(수정 전) 15 failed · 26 passed — 통과한 26 중 일부는 **이유가 틀렸다** (§3)

python3 -m pytest tests/ -q                          493 passed      (612.05s)  EXIT=0
  수집 개수 493 = WORKING_STATE.md 의 "N passed 기대" 와 같다 (R6 내부 DF-04 의 문서 계약)
  수정 도중 한 번은 14 failed · 479 passed 였고, 그 14 는 **전부 fixture** 였다 (§4)

리뷰어 재현기 — 우리가 한 줄도 고치지 않고 다시 돌렸다 (스크래치패드 사본):

python3 repro_producer_reader.py --target <BMS_DIR>
  rc 0                          ← 수정 전 rc 2 (F2-04)
  width_status ['measured','measured'] · check_rows []
  control_without_row_cycle rc 2 ← 수정 전 rc 0 (축 분리 대조군이 **뒤집혔다**)
    "! 행 0 (cycle 0) 의 receipt 가 **그 cycle 의 기대 receipt** 와 다르다"

python3 repro_followup2.py --target <BMS_DIR>        47 case
  뒤집힌 것 (수정 전 → 지금)
    width_row_scale_seed         0 → 2      width_env_python_only      0 → 2
    width_row_n_starts           0 → 2      width_env_null_values      0 → 2
    width_row_scale_mixed        0 → 2      width_env_whitespace       0 → 2
    gc_retained_path_alias       0 → 2      width_manifest_whitespace  0 → 2
    gc_unknown_file              0 → 2      width_bounds_singleton     0 → 2
    receipt_runtime_python_null  0 → 3      width_bounds_nan           0 → 2
    receipt_runtime_wrong_keys   0 → 3      width_untyped_width_starts 0 → 2
    receipt_materialized_wrong_fields 0 → 3
    width_nan_best   NaN 구간 반환 → **ValueError**
  그대로 지켜진 것 (대조군)
    width_positive 0 · receipt_positive 0 · gc_control 0 · gc_old_cross_artifact 0
    gc_duplicate 2 · gc_cleanup_escape 2 · gc_unknown_dir_negative 2
    width_body_* 2 · width_null_* 2 · width_fractional_cycles 2 · width_seed_negative 2
    receipt_bad_date 3 · receipt_non_digest 3 · receipt_missing_runtime_negative 3
    width_infeasible_best RuntimeError · width_true_empty_control RuntimeError
```

환경: Linux `6.18.44-fc-v37` · Python 3.11.15. **리뷰어의 Windows 집계를 이것으로 바꾸지 않는다** (§7).

## 7. 이 라운드가 하지 않은 것

- **실데이터 재적합·A/B 재실행** — 이번 검토가 승인하지 않았고 우리도 하지 않았다. 리뷰어가 남긴
  조건(*목적·축·입력·version·예산·종료 조건을 별도로 정한다*)을 그대로 미결로 둔다.
- **제품 과학 결과 갱신** — 없다. 이 라운드는 전부 하네스다.
- **Windows 결과의 대체** — 우리 Linux 결과로 리뷰어의 Windows 집계를 바꾸지 않는다. 리뷰어의
  `fcntl` 80 · shell 16 · symlink 1 · 파일명 1 · 경로표기 2 · 미확정 8 분류는 그대로 둔다.
  `test_e11_10` 이 이번에 통과한 것도 **원인 규명·종결로 보지 않는다** (리뷰어 문장 그대로).
- **`test_fu_12` 의 성격** — 리뷰어 지적을 받는다: 그 `RuntimeError` 는 **선행 best 검사**이지
  일반적 허용집합 공집합 탐색 알고리즘을 실행했다는 증거가 아니다. 그렇게 다시 적었다.
