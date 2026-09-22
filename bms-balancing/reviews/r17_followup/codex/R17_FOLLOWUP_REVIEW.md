# R17 후속 재검토 — 7c8f61f9

판정: **NO-GO**. 기존 반례 여러 개와 chain-rule의 수학적 수정은 확인했다. 그러나 **파일 경계·비교 조건의 결속·영수증 완전성**을 종결했다고 받을 수 없다. 이번 판정은 BMS 하네스의 수정 수용 여부이며, COMSOL 또는 degradation-degeneracy 게이트 판정이 아니다.

대상은 `7c8f61f943199c3782bf3c3d81f6b573aa0a1b79`. 사용자 회신 상단의 갱신을 정본으로 해석했다. 따라서 보존된 본문의 “chain rule 미구현” 문장은 새 결함으로 세지 않았다. 이전 대상 `dfc1fc78b3396c95709650860f1502c0e83ead40`과 대조했다.

## 1. 범위와 증거

- 새 분리 checkout의 코드·회귀·수식·과학 문장 검토. production 코드는 수정하지 않았다.
- 실데이터 A/B 적합, 기존 실험 산출 재생성, COMSOL, push는 하지 않았다. 시험이 만드는 합성 적합과 합성 파일은 별개다.
- `repro_followup.py`는 원본을 변경하지 않고 리뷰 폴더에 매번 새로운 합성 fixture를 만든다. GC 반례의 삭제 대상도 그 안에 만든 파일/폴더만이다. 사용자 자료를 삭제한 시험이 아니다.
- `REPRO_RESULTS.json`의 각 case와 같은 이름의 `.log`가 실제 출력이다. 재현 스크립트 rc 0은 **잘못된 동작을 예상대로 관측했다**는 뜻이지 제품 PASS가 아니다.
- 전체 시험은 **318 passed · 108 failed · 952.84초**였다. 실패 99건에는 fcntl/Bash/링크 권한/Windows 경로 차이의 흔적이 있고, **9건은 원인 미확정**이다. 이를 전부 환경 문제로 확정하지 않는다. 정확한 분류는 `TEST_STATUS.md`를 보라. Linux의 `426 passed`를 이 기계에서 재인증했다고 쓰지 않는다.

재현 명령(저장소 밖의 이 리뷰 폴더에서):

```powershell
python repro_followup.py --target <7c8f61f9-checkout>/bms-balancing
```

Python에 대상 tests의 numpy/scipy/pandas/openpyxl/pytest 의존성이 필요하다. 스크립트는 등록된 회귀의 완전한 CSV fixture를 재사용하고, 코드 식별과 manifest는 현재 고정 checkout의 실제 값으로 채운다. 각 우회는 정상 대조군과 해당 음성 대조군이 성립하는 상태에서 시험했다.

## 2. P1 조건

### P1-01 — GC의 파일 검사와 디렉터리 삭제가 다른 경로를 사용한다

위치: `scripts/gc_partial.py:91–98`, `:111–119`; retained 경로 보호는 `:82–84`.

**반례 A (`gc_cleanup_escape`)**:

1. 합성 `out/partial/matrix/A/matrix_100.csv`, `B/matrix_100.csv`와 `out/victim/sentinel.txt`를 만든다.
2. 오래된 index 항목의 `path`는 유효한 `matrix/A/matrix_100.csv`로 둔다. 반면 `kind='..'`, `attempt='victim'`으로 둔다. 같은 그룹의 새 항목과 실제 A/B 디렉터리를 인식시키는 보존 항목도 있다.
3. `python scripts/gc_partial.py --root <fixture>/out --keep 1 --apply`.
4. **실제 rc 0, partial 밖 `out/victim/sentinel.txt` 소실.** 기대는 삭제 전 rc 2와 전체 바이트 보존이다.

`path`만 resolve/containment 검사를 거친다. 그 뒤 `att = root / e['kind'] / e['attempt']`를 새로 만들고 검증 없이 `rmtree(att)`한다. **검사한 삭제 대상이 실제 삭제 대상 전체를 덮지 않는다.** 이 반례는 malformed index를 전제로 한다. 정상 producer가 이 index를 자동 생성했다거나 실제 canonical이 지워졌다는 주장은 아니다. 하지만 “모르면 안 지우고 partial 밖은 절대 안 건드린다”는 GC 계약은 깨진다.

**반례 B (`gc_duplicate`)**: 같은 payload를 가리키는 동일 index 항목 두 개에서 `--keep 1 --apply`하면 한 항목은 보존되는데 그 파일은 삭제된다(rc 0). `retained_attempts`는 디렉터리 제거만 막고 앞선 `f.unlink()`는 막지 않는다. 중복/alias가 있으면 거부하거나 보존 참조 파일을 삭제 집합에서 제외해야 한다.

**최소 종결 조건**: 모든 index 항목을 먼저 typed 파싱하고 `(kind,attempt,artifact)`와 실제 경로를 결속한다. 파일·sidecar·디렉터리를 포함한 **전체 변경 대상**의 정규 경로가 partial 안인지 첫 삭제 전에 확인한다. 보존/삭제 경로가 겹치면 거부하거나 보존을 우선한다. A/B 각각에서 바이트 불변 음성 시험과 정상 GC 양성 시험을 갖춘다. 원장에 없는 파일을 디렉터리째 지우는 정책도 명시적으로 정해야 한다.

이전 A/100·A/200·B/100 반례 자체는 독립 합성 index로 다시 실행해 A/200이 남는 것을 확인했다(`gc_old_cross_artifact`). 그 수정의 효과는 인정한다.

### P1-02 — 행의 실행 조건과 sidecar 선언이 결속되지 않는다

위치: `scripts/width_report.py:96–117`, `:148–177`; `bms_balancing/schema.py:600–602`, `:742–746`.

정상 두 파일은 `w_dqdv`만 0→1이고 rc 0이다. sidecar의 seed 또는 objective_version도 바꾸면 rc 2이다. 이 대조군을 유지한 채 **B의 행만** 아래처럼 바꾸고 CSV SHA를 sidecar에 정확하게 갱신한다.

| case | 만드는 상태 | 실제 |
|---|---|---|
| `width_body_version` | B 행 모두 v2, B meta는 legacy | rc 0, 한 축 비교 허용 |
| `width_body_mixed_version` | B 내부의 한 행만 v2 | rc 0 |
| `width_body_tol` | B 행 width_tol=.90, meta는 .01 | rc 0 |
| `width_body_cell` | B 행 cell=DIFFERENT_CELL, meta는 syn | rc 0 |
| `width_body_run` | B 행 run_id=unrelated-run | rc 0 |
| `width_fractional_cycles` | B cycle 0.9/1.9, meta [0,1] | rc 0, 두 cycle 동일 취급 |

본문 hash와 입력 receipt는 모두 정확하다. 무결성 hash를 거짓으로 만든 반례가 아니라 **서로 모순되는 내용 자체를 검증하지 않는 반례**다. 행 enum 검사는 각각 유효한 값인지만 확인한다. reader는 입력 receipt만 meta와 대조하고, 실제 비교 조건은 meta에서만 읽는다. cycle은 `int(float(...))`로 정수가 아닌 값까지 접는다.

**최소 종결 조건**: 한 파일 안의 objective_version/cell/run_id/width_tol/scale_seed 등 공통 필드를 단일 선언에 결속하고, 두 실행 비교는 그렇게 검증한 선언만 소비한다. 정수 cycle을 절단 변환하지 말고 값의 정수성을 먼저 검사한다. 위 각 축이 다른 guard에 가려지지 않게 단독 음성 시험을 둔다. v2 대 v2 정상 비교와 명시 `--axis objective_version` A/B는 살아 있어야 한다.

따라서 **1/a 수정은 수용하지만 “행·sidecar·비교기에서 두 버전이 섞이지 않는다”는 종결은 불가**다. 현재 실데이터에 혼합 행이 존재한다는 주장은 아니다.

### P1-03 — 필수 key를 넣고 null로 채우면 동일성 검사가 다시 열린다

위치: `scripts/width_report.py:85–88`, `:148–170`.

- `width_null_identity`: 양쪽 `git_commit=null`, `env=null`, `dataset_manifest=null` → **rc 0**, “코드·환경·입력·모집단 동일 확인”.
- `width_null_settings`: 양쪽 `seed/lb/ub/initial/objective_version=null` → **rc 0**.
- CSV 행과 consumed_inputs는 유효하게 유지한다. 정상 비교 rc 0, 실제 seed 불일치 rc 2 대조군도 통과했다.

“키가 있나”만 추가했고 값의 타입·필수성은 닫지 않았다. 그래서 기존 absent==absent 문제를 null==null 형태로 옮겼다. `gamma_lb=None`처럼 합법적으로 nullable한 항목과 필수 identity/setting을 구분해야 한다.

**최소 종결 조건**: 공유 schema에서 meta의 필수 타입·enum·형식·환경 축을 검증하고 그 결과만 비교한다. nonnullable 필드별 null/공백/잘못된 타입 음성을 두되 합법적 nullable 값은 양성으로 남긴다. null identity에서 “동일 확인”을 출력하면 안 된다.

## 3. P2 조건

### P2-01 — “하한 폭”에 실제 허용집합 밖의 점이 포함된다

위치: `bms_balancing/verify.py:451`, `:468–481`, `:491`; `bms_balancing/cycles.py:88–115`.

**A (`width_out_of_box_seed`)**: 기본 상자 a_PE∈[1,1.4], ref a_PE=1.2, 용량비1, J(p)=1, tol=.01. seed만 a_PE=10으로 준다. 상자 내 진짜 LAM_PE 범위는 [-16.6667,+16.6667]%p인데 **반환 min=-733.3333%p**, `is_lower_bound=true`다. seed는 목적값이 충분히 작다는 이유로 bounds 검사 없이 feasible에 들어간다.

**B (`width_infeasible_best`)**: J(p)=1+(a_PE−1)², best.a_PE=1.4, 전달 best_val=1, tol=.01. 실제 J(best)=1.16으로 한계1.01 밖이다. 유효한 다른 점이 있어 공집합 검사는 통과한다. 그 후 `vals=[mode_of(best), ...]`가 그 밖의 best를 다시 넣는다. 허용집합의 참 LAM_PE 범위는 [8.3333,16.6667]%p인데 **반환 min=-16.6667%p**. 실제 `_width_fields()`도 `measured`로 직렬화했다.

이 둘은 잘못된 seed/stale best_val을 전달한 API 계약 반례다. 정상 multistart가 실데이터에서 그렇게 반환했다는 증거는 아니다. 기존 음수 tol 반례와 같은 producer 방어 범주의 P2로 분류한다.

**최소 종결 조건**: best·seed·solver 결과를 같은 finite/shape/bounds/objective-feasibility 술어로 확인한다. obj(best)와 best_val의 관계를 검증하고 실패면 `failed`, 아니면 검증된 witness만 extrema에 넣는다. 임의 best를 “점추정을 구간 안에 넣기 위해” 삽입하면 하한 보증이 무너진다.

시험 감사: `test_r17_11`은 tol=-.5라 objective 호출 **0회**에 ValueError로 끝났다(`empty_set_test_axis`). 이름과 달리 empty feasible 분기를 직접 시험하지 않는다. 별도 정상 tol=0, J≡2, best_val=1의 진짜 공집합은 RuntimeError가 나오는 것을 확인했다(`true_empty_set_control`). 후자의 방어 자체가 없다는 지적은 아니다.

### P2-02 — run receipt의 “typed 완전성”은 여전히 필드 존재 검사다

위치: `scripts/verify_run_receipt.py:83–96`; 실제 producer `reviews/r11_repros/replay_codex_r11.py:335–351`, `reviews/evidence_gate.py:55–65`.

실제 대상의 commit/tree/instrument blob을 쓴 양성 영수증에서 각각 하나만 바꾸고 공개 receipt hash를 다시 계산한다:

- runtime=null / runtime="not-a-runtime-object"
- materialized=17
- produced_utc="not-a-date"
- package.digest="not-a-digest"

**모두 rc 0, checks.complete=true, verified=true.** runtime 키를 아예 빼면 rc 3이다. 즉 누락만 닫고 잘못된 타입/내용은 받는다. 서명키를 깬 공격이 아니다. 공개 checksum·ancestry 통과가 typed 완전성을 증명하지 않는다는 기존 축의 잔여다.

더구나 실제 r11 writer에서 `package_digest()`의 두 번째 반환값은 SHA가 아니라 `{파일명: 'ok'|'mismatch'|'missing'}`이다. 이를 `str(digest)`로 `package.digest`에 넣는다. 합성 패키지 A/B의 one.txt bytes와 각각의 올바른 SHA256SUMS가 서로 달라도 패키지 필드가 모두 `{'one.txt': 'ok'}`가 됐고, 두 receipt는 검증 rc 0이었다(`receipt_package_status_collision`). 코드 commit이 패키지 파일까지 간접적으로 지목할 수 있다는 것과 이 필드 자체가 실제 검사한 payload의 digest라는 것은 다르다. 이 반례만으로 전체 replay gate를 우회했다고 주장하지 않는다.

**최소 종결 조건**: producer/consumer가 공유하는 receipt schema로 nested type·nullable/tagged 상태·timestamp·실제 digest 형식을 정의한다. 패키지 검사 상태와 내용 주소를 별도 필드로 분리하고, payload/hash manifest의 정규 내용 digest를 발행·검증한다. `materialized=None`처럼 현재 producer가 허용하는 상태를 무조건 금지하라는 뜻은 아니다. 그 의미와 완전/부분 판정이 명시돼야 한다.

## 4. 직전 항목별 판정

| R17 항목 | 이번 판정 | 근거 |
|---|---|---|
| P1-01 A/100·A/200 GC | 원 반례 닫힘 / GC 전체는 부분 | A/200 보존 실측. 새 P1-01의 별도 경로·중복 참조 잔여 |
| P1-02 absolute run_id | 닫힘(시험한 범위) | 절대·상위·구분자·빈 값 등 거부 회귀 통과. 동시 예약/OS principal까지 증명한 것은 아님 |
| P1-03 legacy wildcard | 닫힘 | None/다른 rev 거부, exact old rev만 rc4+legacy 승인. promotion은 false |
| P1-04 width 비교 | 부분 | 기존 다섯 반례 rc2. 본문↔meta·null 값·fractional cycle 잔여 |
| P1-05 과학 과잉 추론 | 정정 취지 수용 / 문서 정합성 잔여 | §12-6·14-1·14-3·15-6 철회는 맞음. 아래 주의 참조 |
| P2-01 width union/공집합 | 원 반례 닫힘 / producer 보증 부분 | 음수·NaN·역전 구간 거부. 새 P2-01은 유효 witness만 쓰는 보증의 잔여 |
| P2-02 불완전 receipt | 원 누락 반례 닫힘 / typed 결속 부분 | 키 삭제 rc3, wrong-type/placeholders rc0 |
| chain-rule | 수학·명시 인자 수용 / 산출물 전달 부분 | 9회귀 통과, 1/a 경로 확인. 비교기 혼합 허용은 P1-02 |
| 실데이터 A/B·UNKNOWN_BLOCKERS 정본화 | 미실행/미착수 유지 | 새 발견으로 다시 세지 않음 |

과학 문장 정정은 실제로 전보다 좁아졌다. 다만 `BML_R1_RESPONSE.md:707–714`의 “말할 수 있다” 요약은 여전히 **부호 식별을 잃는다**, §15-6에서 원인을 닫았다고 쓴다. `:500–501`도 앞 정정 바로 뒤에서 옛 실험이 결론을 강화한다고 말한다. 보존 목적의 원문 삭제는 필요 없지만, 현재 유효 결론 블록/요약에도 철회 우선순위를 표시해야 한다. 이를 독립된 새 P1로 중복 집계하지 않았다.

추가 회귀 한계: chain-rule `cr_04`의 잡음 경우는 하나의 RNG를 버전 루프 안에서 연속 소비하므로 legacy와 v2가 **서로 다른 잡음 실현**을 적합한다(`tests/test_chain_rule_contract.py:160–181`). v2의 절대 허용 시험 자체를 무효화하지는 않지만, 두 오차의 차이를 단일 인자 효과로 인용할 수 없다. 같은 cap/vol 배열을 먼저 고정해 두 버전에 공유해야 한다. 현재 시험은 두 truth와 잡음 한 조건이며 평활/bound를 바꾼 전수 강건성 시험은 아니다.

## 5. 재수용을 위한 최소 조건

1. GC의 모든 변경 대상과 보존 참조를 단일 검증 경로에 묶고 P1-01 두 fixture에서 첫 삭제 전 거부/보존을 확인.
2. width reader의 본문↔meta 결속과 cycle 정수성(P1-02), 필수 값의 typed 검증(P1-03)을 각각 독립 회귀로 닫기.
3. 근최적 폭에는 실제 허용집합의 witness만 포함하고 stale best_val/상자 밖 seed가 `measured`가 되지 않게 하기.
4. receipt의 실제 nested schema와 package 내용 digest를 생산·소비 양쪽에서 연결하기.
5. 현재 과학 요약의 철회 우선순위를 정리하고, 지원 Linux 환경 전수 로그를 별도 제공하기. 이 환경의 실패 중 특히 원인 미확정 9건을 항목별로 설명/재현하기. Windows에서 관측한 실패를 모두 환경 문제 또는 새 수치 반례로 단정하거나 Linux PASS로 대체하지 않기.

그 뒤 코드 수용을 다시 판정한다. **실데이터 재적합은 이 회신으로 승인하지 않는다.** A/B 목적·축·입력·version·자원·종료 조건을 고정한 별도 승인안이 필요하다. 한 항의 미분 수정이 기존 실데이터의 LAM 부호·참 폭·물리 정답까지 자동 인증하지 않는다.
