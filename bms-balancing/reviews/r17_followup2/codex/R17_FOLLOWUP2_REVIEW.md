# R17 후속 2차 재검토 — NO-GO

대상: `a4c311eff898615932ae6f333bbb26b605abf762`.
검토 문서: `bms-balancing/reviews/R17_FOLLOWUP_RESPONSE.md`.
BMS 수정 커밋: `8733453351b5570c0dc0b0182ae7c490f900b380`.
`8733453..a4c311ef`의 `bms-balancing/` diff는 비어 있다.
날짜: 2026-09-22. 승인 범위: Astra XHigh, 읽기/합성 재현/검토 산출물 작성.
Gate66·COMSOL과 독립된 BMS 하네스 검토다. 제품 코드 수정·실데이터 재적합·과학 결과 갱신·push는 하지 않았다.

## 1. 판정

**NO-GO. P1 4건·P2 2건.** 예전 반례의 구체적인 입력은 막혔지만, 그 입력을 막는 검사가 전체 계약을 닫지는 않았다.

특히 `width_report`는 **정상 생산자가 만드는 cycle별 영수증을 거부하면서**, 합성 fixture처럼 모든 행의 영수증을 공통 영수증과 같게 만들면 통과한다. 실패 입력만 막는 회귀뿐 아니라 실제 producer → consumer 양성 경로가 필요하다.

| ID | 심각도 | 실행으로 확인한 반례 | 무효화되는 주장 |
|---|---|---|---|
| F2-01 | P1 | GC의 `rmtree`가 보존 index가 가리키는 다른 파일·미등록 파일까지 삭제 | 보존 우선·모르면 거부 |
| F2-02 | P1 | 행의 `scale_seed=99`, `n_starts=999`인데 sidecar는 0/4여도 rc 0 | 한 축만 다른 비교 |
| F2-03 | P1 | 필수 환경 내부가 전부 null/공백, 잘못된 bounds여도 rc 0 | 동일 환경·유효 조건 확인 |
| F2-04 | P1 | 실제 `fit_cycles` API 산출의 cycle별 receipt를 정상 reader가 rc 2로 거부 | 생산자·소비자 계약의 연결 |
| F2-05 | P2 | `best[0]=NaN`으로 `measured`, NaN 구간, `is_lower_bound=true` 반환 | 유효 witness만으로 폭을 발행 |
| F2-06 | P2 | `runtime={"python":null,"platform":null}`도 complete/verified=true | typed 실행 영수증의 완전성 |

F2-01의 두 사례는 같은 재귀 삭제 범위 문제로 한 건이다. F2-03의 여러 잘못된 값도 미완인 sidecar schema의 사례로 묶었다. F2-04는 이번 독립 재검토에서 추가로 발견한 정상 경로 결함이다. 남아 있다고 신고한 실데이터 검증·UNKNOWN_BLOCKERS·Windows 미분류 실패를 새 반례로 중복 집계하지 않는다.

## 2. 재현 방법과 증거의 의미

Python에 대상의 테스트 의존성을 설치하고, 이 보고서와 함께 전달한 두 스크립트를 실행한다. `--target`은 고정 커밋의 `bms-balancing` 절대경로다.

```text
python repro_followup2.py --target <BMS_DIR>
python repro_producer_reader.py --target <BMS_DIR>
python verify_observations.py
```

- 첫 스크립트: 이전 반례·대조군·인접 입력 **47 case**. 각 CLI의 명령/rc/stdout/stderr를 `REPRO_RESULTS.json`에 남긴다. 첫 실패 assertion에서 다음 case가 생략되지 않는다.
- 두 번째: 저장소 테스트가 사용하는 합성 workbook으로 **실제 `cycles.fit_cycles` API**를 호출한다. 생산 결과와 실제 `sidecar_dict`로 CSV/sidecar를 직렬화한 뒤 실제 reader를 호출한다.
- 세 번째: **63개 관측 조건**을 검사한다. `all_observations_match=true`는 보고한 성공/거부/결함이 재현됐다는 뜻이며 제품 PASS가 아니다.
- GC는 스크립트 옆 고유 `synthetic-*` 아래 새로 만든 파일만 지운다. 실제 사용자 산출물은 대상으로 삼지 않는다. 삭제 전 실경로가 해당 임시 트리 안인지 검사한다.
- `PRODUCER_READER_RESULTS.json`의 실제 생산자 시험은 Windows의 `fcntl` 부재 때문에 게시 CLI 전체를 통과했다고 주장하지 않는다. 계산 API·sidecar builder·reader는 실제 코드이고, **디스크 직렬화만 검토용 코드**다. 잠금 구현을 가짜로 바꾸지 않았다.
- `REPRO_RESULTS.json`의 NaN은 의도적으로 재현한 Python 비유한 수 관측이다. 이를 정상 과학 데이터/표준 JSON 결과로 취급하지 않는다.

아래 줄 번호는 모두 이 HEAD의 `bms-balancing/` 상대경로다.

## 3. P1 반례와 최소 종결 조건

### F2-01 — 개별 파일 충돌 검사는 재귀 삭제의 전체 범위를 보호하지 않는다

위치: `scripts/gc_partial.py:80`, `:131`, `:139`, `:153`–`:157`.

재현 case: `gc_retained_path_alias`, `gc_unknown_file`. 명령은 각 fixture에 대해 다음과 같다.

```text
python scripts/gc_partial.py --root <synthetic fixture> --keep 1 --apply
```

첫 상태:

```text
partial/matrix/A/matrix_100.csv  ← 오래된 100, 삭제 예정
partial/matrix/A/matrix_200.csv  ← 유일한 200, 보존 index의 path
partial/matrix/B/matrix_100.csv  ← 최신 100
partial/matrix/C/               ← index의 200 항목은 attempt=C라고 선언
```

세 번째 항목의 `path`는 `matrix/A/matrix_200.csv`이지만 `kind/attempt`는 `matrix/C`다. 모든 경로는 partial 안이며 각 component는 평범한 문자열이다. SHA도 실제 payload와 맞는다.

**실제:** rc 0. 보존 index에는 `matrix/A/matrix_200.csv`가 남았지만 그 파일은 삭제됐다. `REPRO_RESULTS.json`의 `watched_exists=false`와 전후 파일 목록으로 확인했다.

이유: `retained_files`는 `A/100`과 `A/200`이 같지 않으니 통과한다. `retained_dirs`는 payload의 실제 조상이 아니라 선언된 `C`에서 만든다. 이어서 `rmtree(A)`가 `A/200`까지 제거한다. 손상된 index를 받아들여도 된다는 뜻이 아니다. **모순된 index면 첫 삭제 전에 거부해야 한다.**

두 번째 상태는 index가 정상인 A/100·B/100에 `A/unindexed.txt`만 추가한다. **rc 0으로 이 미등록 파일도 삭제됐다.** `unknown`은 두 단계의 시도 디렉터리만 열거하므로 그 안의 파일을 보지 않는다. 회신 §5의 “원장에 없는 파일도 unknown 검출에서 rc 2”는 현재 코드와 다르다.

대조군: 예전 `kind='..'`는 rc 2·sentinel 보존, 같은 payload 중복 참조는 rc 2·보존, 정상 A/100+A/200+B/100은 rc 0·A/200 보존, 별도 미등록 시도 디렉터리는 rc 2다. 단순 경로 이탈 검사가 실패해서 생긴 반례가 아니다.

최소 종결 조건:

1. 항목의 `(kind, attempt, artifact)`와 실제 payload 경로의 관계를 **전체 index에 대해** 먼저 검증한다. 불일치는 삭제 0건·rc 2.
2. 모든 삭제 방식의 실제 범위가 보존 payload/미등록 파일을 침범하지 않음을 보장한다. 가장 작은 구현은 검증된 개별 파일만 지운 뒤 빈 디렉터리만 `rmdir`하는 방식이다. `rmtree`를 유지한다면 전체 하위 파일의 정책을 검사해야 한다.
3. 위 두 반례가 첫 삭제 전에 거부되거나 해당 파일을 보존하고, 기존 대조군이 계속 통과해야 한다. 중복 참조 rc 2 정책 자체는 수용한다.

### F2-02 — 행에 남은 실행 조건 두 개가 sidecar 비교를 우회한다

위치: `scripts/width_report.py:59`, `:164`; 생산 위치 `bms_balancing/cycles.py:216`, `:218`.

재현: `width_row_scale_seed`, `width_row_n_starts`, `width_row_scale_mixed`.
두 파일의 sidecar는 `w_dqdv`만 0→1로 다르다. 한쪽 **행만** `scale_seed=99` 또는 `n_starts=999`로 바꾸고 본문 SHA를 정확히 갱신한다. 원래 sidecar의 scale_seed는 0, starts/n_multistart는 4다.

**실제:** 세 case 모두 rc 0, `코드·환경·입력·모집단 동일 확인`과 폭 비교를 출력했다. 한 파일 안에서 일부 행의 scale_seed만 바꿔도 통과했다. 반면 sidecar 자체의 scale_seed나 starts를 바꾸는 대조군은 rc 2다.

이유: `BODY_META_BOUND`의 네 쌍에 `scale_seed`, `n_starts`가 없다. `schema.check_rows`는 숫자의 모양을 보지만 sidecar와의 의미상 동등성을 대신하지 않는다. `scale_seed`는 목적함수 scale 샘플, `n_starts`는 실제 multistart 수를 바꾸는 생산자 기록이다.

최소 종결 조건: 행과 sidecar가 공동 선언하는 축을 실제 producer에서 도출해 결속한다. 최소한 `scale_seed↔scale_seed`, `n_starts↔starts/n_multistart` 및 sidecar의 두 starts 선언 사이 관계가 필요하다. 파일 내 혼합도 거부해야 한다. 회신 질문의 `si_source`는 **현재 `CYCLES_ROW`에 없으므로** 무작정 행 결속 목록에 추가할 대상은 아니다. 실제 존재하는 두 열부터 닫아야 한다.

### F2-03 — null을 객체 안으로 한 단계 옮기면 다시 “동일 확인”이다

위치: `scripts/width_report.py:71`–`:100`, 특히 `:82`·`:83`·`:90`.

재현과 실제 결과:

| case | 양쪽 sidecar에 준 값 | 실제 |
|---|---|---|
| `width_env_python_only` | env에 python만 | rc 0 |
| `width_env_null_values` | env 여섯 축 값 모두 null | rc 0 |
| `width_env_whitespace` | env 여섯 축 값 모두 공백/탭/NBSP | rc 0 |
| `width_manifest_whitespace` | dataset_manifest = 공백 문자열 | rc 0 |
| `width_bounds_singleton` | lb=ub=initial=[0] | rc 0 |
| `width_bounds_nan` | lb=[NaN,NaN,NaN,NaN,NaN] | rc 0 |
| `width_untyped_width_starts` | width_starts=null | rc 0 |

각 CSV의 값·입력 receipt·본문 SHA는 해당 case의 축 외에는 정상 대조군과 같다. 이미 고친 최상위 `env=null`/`lb=null`은 rc 2다.

이유: “비어 있지 않은 dict”는 환경 여섯 축이 존재하고 값이 있다는 계약이 아니다. 숫자 목록도 길이·유한성·상자 순서까지 검사하지 않는다. width_starts 등은 비교에는 들어가지만 typed 검사에서는 빠져 있다. 두 잘못된 값이 같다는 사실이 유효성을 대신한다.

최소 종결 조건:

- env는 기존 `schema.env_axes_missing()`의 실제 필수 축 규칙을 사용한다. unknown/legacy를 허용해야 한다면 “환경 동일 확인”과 별도 상태로 출력한다.
- dataset identity는 실제 `half_cell_manifest_identity()`가 발행하는 version/dataset_id/sha256 계약을 검증한다. 아무 비공백 dict로 대체하지 않는다.
- bounds는 공통 `resolve_box`의 5차원·유한·순서 규칙, initial은 그에 맞는 유효 벡터, 그 밖의 필수 설정은 명시 schema로 검사한다. 합법 nullable인 gamma_lb 등과 미기록을 구분한다.
- 양쪽 값이 같은 경우에도 각 파일의 유효성을 먼저 검사한다. 위 case와 정상 nullable 대조군을 각각 회귀로 둔다.

### F2-04 — 실제 producer의 cycle별 receipt와 reader의 공통 receipt 요구가 충돌한다

위치: `bms_balancing/cycles.py:159`, `:206`; `scripts/fit_cycles.py:116`; `scripts/width_report.py:151`–`:160`.

재현: `repro_producer_reader.py`.

1. 저장소의 `_synth_root`와 `_cycle_workbook`으로 합성 2사이클 입력을 만든다.
2. 실제 `C.fit_cycles(..., widths=True, n_starts=1, width_starts=0)`을 호출한다. **두 행 모두 measured**, 실제 `schema.check_rows`의 문제 목록은 `[]`다.
3. `scripts/fit_cycles.py`처럼 `res['consumed']`를 sidecar에 넣고 실제 `sidecar_dict`를 사용한다. 행에는 producer가 이미 붙인 `full_cell.cycle=0/1`이 있다.
4. `width_report.py <cycles_syn_Li.csv>` 호출.

**실제:** rc 2, `행 0 의 receipt 가 sidecar 의 입력과 다르다`.

원본 입력 파일 path/SHA는 같다. 차이는 행의 `cycle` 추가다. reader는 두 JSON과 aggregate digest가 통째로 같아야 한다고 요구한다. 여러 행에 각각 다른 cycle을 기록한 정상 producer가 이 조건을 만족할 수 없다.

축 분리 대조군: 계산 값은 그대로 두고 행 receipt의 `cycle`만 제거한 뒤 행 inputs_sha/본문 SHA를 재계산하면 **rc 0**이다. 이것은 **수정 제안이 아니라**, 현재 검사가 의미 있는 식별을 더 적은 정상 산출을 거부한다는 확인이다.

기존 `_fake_widths_csv`는 모든 행과 sidecar에 동일 `_FAKE_CONSUMED`를 넣어 이 충돌을 가렸다. 실제 생산자로 확인하지 않은 정상 fixture가 계약을 대신한 사례다.

최소 종결 조건: common receipt와 per-cycle receipt를 명시적으로 구분하고, 해당 행의 cycle로 기대 receipt를 구성해 정확 대조한다. 행 cycle/receipt cycle 불일치, 다른 workbook SHA, 누락·중복 cycle은 계속 거부한다. 실제 생산자 → sidecar → reader 정상 경로를 합성 E2E로 추가해야 한다. Windows publisher 잠금 성공을 이 API 재현으로 주장하지 않는다.

## 4. P2 반례와 최소 종결 조건

### F2-05 — best만 유한성 검사에서 빠져 measured NaN을 만든다

위치: `bms_balancing/verify.py:443`, `:463`, `:515`; `bms_balancing/cycles.py:106`.

재현 case: `width_nan_best`.

```python
bp = (model.LB5 + model.UB5) / 2
best = bp.copy(); best[0] = float('nan')
obj = lambda p: 1.0
near_optimal_extrema(obj, bp, 1., 1., best, 1.,
    tol=.01, seeds=[], n_starts=0, seed=0, lb=model.LB5, ub=model.UB5)
```

**실제:** 예외 없이 LAM_PE/LLI min·max·span=NaN, `is_lower_bound=true`. 실제 `_width_fields` 호출도 `width_status='measured'`와 NaN 끝점을 돌려준다.

이유: `_b`의 선행 비교는 NaN에 대해 두 부등식이 모두 false가 되므로 거부하지 않는다. `_in_box`는 유한성을 검사하지만 best를 `vals`에 직접 다시 넣는 줄이 그것을 통과하지 않는다. “모든 후보에 같은 술어”가 여전히 아니다.

최소 종결 조건: best/ref 및 mode에 필요한 입력의 유한성을 먼저 검사하고, 최종 witness/끝점도 같은 검증 경로에 묶는다. 실패 시 `_width_fields='failed'`여야 한다. 기존 상자 밖 seed 거부와 정상 계산을 보존한다.

범위 한정: 이 재현은 공개 수치 함수와 실제 행 필드 helper의 잘못된 상태를 입증한다. 실제 셀 적합이 이 NaN best를 생산했다거나, 후속 schema gate까지 NaN이 통과했다고 주장하지 않는다. schema reader의 유한성 방어는 별도다.

추가 관측(독립 건수에 넣지 않음): `obj=1+(p[0]-1)^2`, best[0]=1인데 best_val=100을 주면 검사에 걸리지 않고 LAM_PE min=-16.6667%p를 낸다. best_val=1 대조군은 +8.3333%p다. current predicate는 **best가 전달된 limit 안인가**만 보며 `obj(best)==best_val`을 보증하지 않는다. 외부 기준 목적값을 허용하는 API라면 그렇게 명명/문서화하고, “전달 best_val은 이 best의 실제 값”이라는 주장은 좁혀야 한다. 수치 부등식 자체의 버그로 중복 집계하지 않는다.

### F2-06 — receipt의 nested schema가 내부 필드가 아니라 바깥 컨테이너에서 멈춘다

위치: `scripts/verify_run_receipt.py:46`, `:74`–`:78`; 실제 발행 예 `reviews/r11_repros/replay_codex_r11.py:355` 부근.

재현 case:

```text
receipt_runtime_python_null        runtime={"python":null,"platform":null}
receipt_runtime_wrong_keys         runtime={"irrelevant":true}
receipt_materialized_wrong_fields  materialized={"mode":17}
```

각 receipt는 실제 고정 HEAD/tree/instrument git blob을 사용하고 공개 `receipt_signature`로 checksum을 재계산한다. **암호학적 위조나 실행 사실 증명 공격이 아니라 입력 schema 검사**다.

**실제:** 세 경우 모두 rc 0, `checks.complete=true`, `verified=true`.

이유: runtime은 bool(dict)만, materialized는 isinstance(dict)만 본다. 발행자가 실제로 쓰는 python/platform 문자열과 materialized mode의 의미를 확인하지 않는다. 최상위 null/문자열/runtime, materialized=17 대조군은 모두 rc 3으로 고쳐졌다.

최소 종결 조건: 공유 producer/consumer schema에서 버전별 runtime의 필수 필드/타입/비공백과 materialized의 허용 tagged 형태를 정의한다. `materialized=None`이 합법인 상태는 유지한다. 부분·unknown 기록을 허용한다면 complete/verified와 구분한다. public checksum을 비밀 서명으로 바꾸라는 요구가 아니다.

package digest 부분은 종결을 인정한다: 정상 SHA 목록을 가진 content-A/content-B 두 묶음의 상태 dict는 같지만 새 `package_content_digest`는 달랐다. 다만 이것은 **목록이 가리키는 파일 내용 주소**다. 실제 실행·독립 replay·디렉터리의 모든 파일·manifest 원문까지 인증한다는 주장은 하지 않아야 한다. consumer가 package bytes를 재검증한다고도 표현하면 안 된다.

## 5. 이전 다섯 조건 판정표

| 이전 ID | 원래 반례의 재실행 | 이번 종결 판단 |
|---|---|---|
| P1-01 GC | escape/duplicate 모두 rc 2·보존. 기존 정상 cross-artifact 보존 | **부분** — F2-01 재귀 삭제 범위 잔여 |
| P1-02 row binding | version/mixed version/tol/cell/run_id/fractional cycle 모두 rc 2 | **부분** — F2-02 누락 열, F2-04 정상 producer 불일치 |
| P1-03 null identity/settings | 최상위 null 두 묶음 모두 rc 2 | **부분** — F2-03 내부 결측·불법 설정 수용 |
| P2-01 witnesses | out-of-box seed min=-16.6666667%p로 참 상자 안, infeasible best는 RuntimeError 및 failed | **부분** — F2-05 best NaN 경로 |
| P2-02 receipt | 종전 잘못된 최상위 타입 다섯 개 모두 rc 3, 내용 digest 분리 확인 | **부분** — F2-06 내부 타입. **내용 digest 수정 자체는 닫힘** |

“원래 입력이 막힌 것”은 인정하지만 “동일 불변식이 구조적으로 닫힌 것”으로 확대하지 않는다.

## 6. 회귀와 과학 문장 감사

- `test_fu_11`은 상자 밖 seed, `test_fu_12/14`는 stale best를 실제로 건드린다. 그 축의 수정 효과는 독립 수치 호출에서도 확인했다.
- `test_fu_12`는 `obj(best)>limit`에서 멈춘다. 일반적인 **허용집합 공집합 판정 알고리즘을 실행했다는 증거는 아니다**. 이번 독립 tol=0·상수 J=2 시험도 선행 best 검사에서 거부된다. 거부 결과와 도달한 분기를 구분해야 한다.
- `_fake_widths_csv`의 common receipt fixture는 F2-04의 실제 producer 계약과 다르다. reader 양성 회귀를 이 fixture만으로 대신하면 안 된다.
- 잡음 공유 수정 후 `test_chain_rule_contract.py` 9건은 집중 시험에서 통과했다. 동일 입력으로 두 objective version을 비교하도록 고친 방향은 수용한다. 여기서 실데이터 LAM 부호·참 폭·물리적 정답·전체 강건성으로 확대하지 않는다.
- 현재 `check_u14 --new out --schema-only`: **rc 0**, 그러나 `promotion_eligible=false`, `env_contract_legacy=13`, baseline_absent=1이다. schema-only rc 0을 승격 GO로 읽지 않는다.
- legacy schema-only는 **rc 2**, schema/provenance_cols/content/provenance = **52/25/10/1**로 관측됐다.
- 독립 시험 집계와 환경 차이는 `TEST_STATUS.md`, 원시 JUnit/log/command JSON에 분리한다. 발신 측 451 passed+1 failed 뒤 52개 재시험을 임의로 “독립 전수 452 passed”로 바꾸지 않는다.

## 7. 회신의 네 질문에 대한 답

1. 중복 payload 참조를 rc 2로 거부하는 정책은 적절하다. 이번 요구는 보존 우선으로 정책을 바꾸라는 것이 아니라 디렉터리 삭제의 실제 범위까지 같은 정책을 적용하라는 것이다.
2. 행/sidecar 결속 네 축은 부족하다. 실제 두 곳에 있는 scale_seed·starts부터 결속하라. 현재 cycles 행에 없는 si_source를 있다고 가정하지 않는다.
3. runtime 빈 객체를 complete로 허용할 이유는 확인하지 못했다. 더 중요한 문제는 비어 있지 않아도 내용이 전부 null 또는 전혀 다른 키일 수 있다는 점이다. unknown이면 부분 상태다.
4. 새 digest는 기존 상태 문자열 충돌을 고쳤다. 다만 문서의 “이름으로 정렬”과 달리 구현은 `hash + 이름` 전체 줄을 정렬한다. 내용 주소로서 결정성은 있으므로 이것만 새 버그로 세지 않는다. 알고리즘 정의를 맞추고, 누락/중복 이름/범위 밖 이름/manifest 원문 포함 여부의 계약은 별도로 명확히 하라. `<missing>`이 들어간 내용 주소가 만들어졌다는 것 자체는 완전한 패키지의 증명이 아니다.

## 8. 재검토를 위한 종결 조건

F2-01~06 각각의 기대 결과를 독립 회귀로 고정하고, 기존 양성/음성 대조군을 함께 통과시킬 것. 특히 F2-04 정상 생산자 연결을 먼저 확보해야 “더 강한 검사”가 올바른 산출까지 막지 않는지 판단할 수 있다.

수정 뒤 새 HEAD/full SHA, 바뀐 코드/시험, 실제 실행 로그, 환경별 실패 분류를 보내면 된다. 이 검토는 코드 변경이나 실데이터 A/B 재실행을 승인하지 않는다. 원자료 재적합은 목적·축·입력·version·예산·종료 조건을 별도로 정해야 한다.

**최종 판정: NO-GO.**
