# R17 후속 3차 수신 검토 — e834b01e

## 판정

**NO-GO — P1 1건 · P2 2건.** 기존 F2-01~06의 구체적 반례는 수정 효과를 확인했다. 특히 정상 producer의 cycle별 receipt를 reader가 거부하던 F2-04는 실제 합성 계산으로 닫힘을 확인했다. 이번 NO-GO의 핵심은 **GC가 경로만 알려져 있으면 파일 내용과 보존 대상의 실재 여부를 확인하지 않고 삭제한다**는 새 반례다. 정상 starts 비교의 불가능성, receipt 오류 처리의 계약 이탈도 별도 재현했다.

검토 대상은 `e834b01e4066c5e78c06b6ed1f77878e5a27a481`, 실제 BMS 수정은 `7f09804fdc6be2892746dece201b98da48aac6cd`다. fix→HEAD의 BMS 차이는 `docs/ASSB_TRANSFER_NOTE.md` 한 문서이며 Python/shell 차이는 없다. 회신의 `a4c311ef`는 **직전 리뷰 대상**이지 이번 수정 대상이 아니다. 원문은 `reviews/R17_FOLLOWUP2_RESPONSE.md`다.

이 판정은 BMS 하네스 코드 재검토다. Gate67·COMSOL·실데이터 적합/과학 결과 갱신과 분리한다. 제품 코드는 수정하지 않았다. 합성 계산과 임시 파일 삭제 시험만 실행했다. Linux 전체 게시 CLI 성공이나 새 과학 결과를 주장하지 않는다.

## 1. F3-01 — P1: index↔디스크 대조가 단방향이라 잘못된 바이트 또는 유일하게 남은 결과를 삭제한다

무효화되는 것: 보존, GC의 “모르면 안 지운다 / index와 디스크가 어긋나면 rc 2” 계약.

자리: `scripts/gc_partial.py:68`의 sha256 문자열 검사, `:98`의 디렉터리 집합 차, `:111`의 경로 집합, `:134`의 보관 선정, `:188`의 unlink 및 `:197`의 index 교체. `sha256`은 출력에는 쓰지만 실제 파일 내용과 대조하지 않는다. 존재 검사는 `if f.is_file(): unlink()`일 뿐이며 보존 파일의 존재는 요구하지 않는다.

### 만드는 상태와 실제 결과

두 정상 항목을 만든다. 모두 `kind=matrix`, `artifact=matrix_100.csv`, 기록 순서는 A→B다. 파일과 index의 path/tuple, 원래 digest는 모두 맞춘다. `--keep 1`이면 A를 버리고 B를 남긴다.

| case | 검사 전에 만든 상태 | 기대 | 실제 |
|---|---|---|---|
| `gc_valid_control` | 둘 다 원래 바이트로 존재 | rc 0, A 삭제·B 보존 | 일치 |
| `gc_changed_bytes` | A 경로만 다른 바이트로 덮음. index SHA는 원래 A의 것 | rc 2, 삭제 0 | **rc 0, 다른 바이트 삭제**. 로그에는 원래 SHA `21c514850291…`를 인쇄 |
| `gc_missing_retained` | 최신 B 파일만 없음. B의 index/디렉터리는 그대로 | rc 2, 유일하게 남은 A 보존 | **rc 0, A 삭제**. 남은 index는 없는 B를 가리킴. 결과 payload 0개 |
| `gc_unindexed_control` | A 안에 다른 이름의 미등록 파일 하나 | rc 2, 전체 보존 | 일치 |

동시 교체를 가정한 추정이 아니다. **GC를 시작하기 전에 이미 만들어진 정적 불일치**로 재현했다. 사용자의 원자료가 아니라 재현기가 새로 만든 하위 폴더에서만 삭제했다. 전후 경로별 해시는 `NEW_FAST_RESULTS.json`에 있다.

```text
python repro_followup3.py --target <bms-balancing> --part fast
# 그 안에서 실제 호출:
python <bms-balancing>/scripts/gc_partial.py --root <fresh-fixture>/gc_changed_bytes --keep 1 --apply
python <bms-balancing>/scripts/gc_partial.py --root <fresh-fixture>/gc_missing_retained --keep 1 --apply
```

현재 코드는 `on_disk - known`과 미등록 경로만 검사한다. 반대 방향의 “등록된 파일이 실제로 있는가”, “그 경로의 바이트가 index가 지목한 바이트인가”는 검사하지 않는다. `rmtree` 제거는 옳았지만, **삭제 단위를 파일로 줄이는 것과 그 파일의 동일성을 검증하는 것은 다르다.**

최소 종결 조건: 첫 삭제 전에 삭제·보존 항목 전체에 대해 실제 일반 파일 존재와 digest 일치를 확인하고, 하나라도 불일치하면 index 포함 쓰기/삭제 0으로 rc 2. 정상 GC, 서로 다른 artifact 보존, 미등록 파일 거부는 유지한다. 별도의 동시 게시 지원 여부도 명시해야 하지만 이번 두 반례를 동시성 문제로 돌리지 말 것. 본 리뷰는 crash/동시 GC의 완전한 안전성까지 검증하지 않았다.

## 2. F3-02 — P2: 같은 실행 축을 두 키로 비교해서 정상 starts A/B가 표현 불가능하다

무효화되는 것: 정상 비교 경로, 단일 실행 조건 변경의 표현 가능성.

자리: `scripts/width_report.py:49`의 `COMPARED_SETTINGS`, `:197`의 starts==n_multistart, `:350`의 `guard_same_except`.

실제 `cycles.fit_cycles` API로 같은 합성 workbook의 2사이클을 두 번 계산했다. `n_starts=1`과 `2`만 바꾸었다. 각 결과는 실제 `sidecar_dict`로 직렬화했다. 두 파일 각각 `width_report` **rc 0**이다. 하지만:

```text
python scripts/width_report.py n1/cycles_syn_Li.csv n2/cycles_syn_Li.csv --axis starts
→ rc 2: n_multistart: 1 ↔ 2

python scripts/width_report.py n1/cycles_syn_Li.csv n2/cycles_syn_Li.csv --axis n_multistart
→ rc 2: starts: 1 ↔ 2
```

정상 파일은 새 검사 때문에 항상 `starts == n_multistart`여야 한다. 그런데 비교 함수는 선택한 문자열 키 **하나만** 제외한다. 따라서 어느 별칭을 선택해도 다른 별칭이 남아 정상 변경을 거부한다. 양쪽 데이터셋에 의도하지 않은 다른 설정이 섞였기 때문이 아니다. 실제 출력의 거부 목록도 이 별칭 한 개뿐이다.

재현: `python repro_followup3.py --target <bms-balancing> --part producer`. `NEW_PRODUCER_RESULTS.json`과 네 로그에 단일 파일 양성·두 축 이름의 음성이 있다. Windows `fcntl` 부재 때문에 게시 CLI 전체를 성공시켰다고 주장하지 않는다. **계산은 실제 API, CSV/sidecar 쓰기는 리뷰어 소유 직렬화, reader는 실제 CLI**다.

최소 종결 조건: 단일 파일 안에서는 별칭의 일치를 계속 요구하고, 두 파일 비교에서는 이를 하나의 의미 축으로 정규화한다. 실제 producer starts 1/2가 rc 0으로 비교되고, `starts!=n_multistart`·row `n_starts` 불일치·다른 seed까지 바뀐 경우는 각각 rc 2여야 한다. 목록에서 아무 검사나 빼서 양성만 열지 말 것.

## 3. F3-03 — P2: typed 오류를 발견한 뒤 잘못된 객체를 계속 사용해 구조화 판정 없이 죽는다

무효화되는 것: receipt 검증 실패의 출력/종료 계약. **잘못된 receipt를 verified=true로 수용하는 반례는 아니다.**

자리: `scripts/verify_run_receipt.py:46`의 `_typed_problems`, `:144`의 결과 수집, `:160`의 `r['code'].get`, `:181`의 instrument `.items()`.

실제 producer가 만든 유효 receipt를 양성 대조군으로 사용했다(rc 0). 서명 checksum은 변경한 내용을 정확히 덮도록 다시 계산한다. 공개 checksum 재계산이며 비밀키 위조가 아니다.

| 입력 | 기대 | 실제 |
|---|---|---|
| `code=null` | 구조화 `verified=false`, 검증 실패 rc 3 | **AttributeError, rc 1**, `RUN_RECEIPT_VERIFY` 없음 |
| `instrument=["not-a-map"]` | 구조화 `verified=false`, 검증 실패 rc 3 | **AttributeError, rc 1**, `RUN_RECEIPT_VERIFY` 없음 |

`_typed_problems`는 두 입력을 발견한다. 그러나 타입 오류가 후속 실행의 경계를 만들지 않아 다시 `.get`/`.items`를 호출한다. 따라서 오류 누락보다 **검사와 소비의 배선** 문제다. 재현 명령은 `--part fast`; 각각의 receipt JSON과 CLI stdout/stderr를 보존했다.

최소 종결 조건: 구조가 잘못된 필드에 의존하는 후속 검사를 실행하지 않되, 확인하지 못한 검사를 성공으로 채우지 않는다. 두 case가 traceback 없이 구조화 실패를 내고 유효 receipt·합법 `materialized=None`은 계속 rc 0이어야 한다. rc를 2로 분류하려면 계약과 회귀에 그 분류를 명시할 것. rc 1을 단순히 3으로 바꾸고 판정 객체를 잃은 채 두는 수정은 불충분하다.

## 4. 기존 여섯 조건의 수용 범위

| 이전 ID | 이번 독립 결과 | 판정 |
|---|---|---|
| F2-01 | path/tuple alias·unknown file rc 2. 정상 GC/cross-artifact rc 0, escape/duplicate 거부 유지 | **원 반례 닫힘**. 더 넓은 보존 계약은 F3-01 때문에 미완 |
| F2-02 | row scale_seed/n_starts 및 혼합값 거부 | **원 반례 닫힘**. 새 별칭 일치와 비교 함수의 합성은 F3-02 |
| F2-03 | env 내부 null/공백/누락, 잘못된 manifest/box/width_starts 거부 | **요구한 축 닫힘**. 모든 가능한 메타데이터 schema 완전성의 증명은 아님 |
| F2-04 | 실제 합성 producer→reader rc 0; row cycle 제거 대조군 rc 2 | **API+직렬화+reader 범위 닫힘**. Linux 게시 CLI 전체는 현지 미검증 |
| F2-05 | best NaN ValueError, 기존 부적합 best 거부 및 양성 유지 | **요구한 NaN 축 닫힘**. 아래 solver 반환 주입과 구분 |
| F2-06 | nested runtime/materialized 잘못된 값 rc 3, 유효 receipt rc 0 | **요구한 nested 축 닫힘**. code/instrument 실패 경로는 F3-03 |

원래 `repro_followup2.py`와 `repro_producer_reader.py`는 바이트 그대로 재실행했다. 47 case 실행을 확인했다. 다만 옛 재현기는 현재 저장소의 fixture를 import하므로 “재현기 바이트 불변”과 “fixture도 불변”은 다르다. 실제 producer 경로를 별도로 실행해 그 한계를 보완했다.

발신 측 493 passed는 발신 측 Linux 결과다. 이번 Windows 전수 결과·trace 분류·직전 실패 집합과의 차이는 `TEST_STATUS.md`/`TEST_RESULTS.json`에 별도로 기록한다. full 실행은 독립 재현과 함께 실행됐으므로 수치 성능 benchmark로 사용하지 않는다.

## 5. 추가 관측 — 위 세 결함과 합산하지 않음

1. `schema.per_cycle_receipt`는 공통 full_cell에 이미 있는 `cycle=999`를 row cycle로 덮어쓴다. 그 공통 sidecar를 가진 synthetic CSV도 rc 0이었다. 입력 파일 digest와 실제 row cycle이 바뀐 반례는 아니므로 **입력 교체 우회로 세지 않는다**. 공통 receipt의 cycle 키를 금지할지, 파생 과정에서 무시 가능한 필드로 명시할지 결정하라.
2. instrument에 파일 blob 대신 `bms_balancing` 디렉터리의 git tree OID를 넣어도 rc 0이었다. 문서는 blob이라고 하나 구현은 `rev-parse`의 OID 일치만 본다. tree도 내용을 주소화하므로 **무결성 우회라고 확대하지 않는다**. 파일 전용인지 tree도 허용하는지 계약을 맞출 것.
3. 명시적인 solver 반환 fault injection에서는 `_in_box`가 최종 SLSQP `r.x`에 적용되지 않는다(`verify.py:538`). `[25,0,3,0,.1]`을 주입하자 참 상자 PE 범위 ±16.6667%p 대신 최소 −733.3333%p를 반환했다. **실제 SciPy가 그 반환값을 만들었다는 native 반례가 아니다.** 의존 solver의 비정상 반환까지 방어한다는 계약을 유지할 경우 같은 witness 술어를 적용할 보강 항목이다. 이 주입 결과를 실제 과학 결과 오류나 추가 P1로 합산하지 않는다.
4. 실데이터 A/B 재실행, 제품 과학 결과 갱신, package 독립 실행 증명은 이번에도 하지 않았다. 기존 과학 문장의 좁힌 범위를 그대로 유지한다. schema-only rc 0은 `promotion_eligible=true`가 아니다.

## 6. 다음 회신에 필요한 것

- F3-01: mismatch와 missing-retained 두 정적 상태에서 첫 삭제/쓰기 전 거부. 정상 보관 동작 유지.
- F3-02: 실제 starts 1/2 양성 비교와 별칭/row 불일치 음성의 동시 통과.
- F3-03: typed-invalid 입력의 구조화 실패, 유효 receipt 정상 통과.
- 새 full SHA, 수정한 코드/회귀, 실제 stdout/rc 및 환경 차이. 이번 Windows 환경 실패 수를 새 제품 결함 수로 옮기지 말 것.

**최종 NO-GO. 기존 여섯 반례가 그대로 남았기 때문이 아니라, 삭제의 근거와 정상 비교/오류 판정 경계에서 새 세 조건이 남았기 때문이다.** 실데이터 적합이나 본 실행 승인은 별도다.
