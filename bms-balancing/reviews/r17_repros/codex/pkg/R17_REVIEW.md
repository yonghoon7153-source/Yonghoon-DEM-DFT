# R17 적대적 검토 — NO-GO
2026-09-22. 사용자 승인 범위: R17 요청문을 기준으로 코드·회귀·독립 반례·과학적 추론을 검토. production 수정·push·실데이터 본 계산·COMSOL 작업은 하지 않았다.

## 1. 판정과 대상
**R17의 “A·B 종결 및 C 결론 수용”은 NO-GO.** P1 5개 항목과 P2 2개 항목을 아래에 둔다. 각 항목의 변형 입력은 독립 재현 스크립트에 있으며, 문서 주장에 대한 합성 반례는 실데이터 재현과 분리했다. 이 판정은 degradation-degeneracy 게이트나 COMSOL 승인으로 옮길 수 없다.

- 브랜치: claude/14-gate-code-review-9qkx05.
- 고정 대상: **dfc1fc78b3396c95709650860f1502c0e83ead40**. 이동하는 “head” 대신 최초 취득한 커밋을 끝까지 고정했다.
- [저장소 R17 요청문](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/reviews/R17_REQUEST.md)과 [BML 응답 원장](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/reviews/BML_R1_RESPONSE.md)을 확인했다.
- 첨부 R17_REQUEST의 전수 결과는 대기 문구였고, 위 커밋의 요청문에는 작성자 실측 **390 passed / 678.01s**가 있다. 아래 리뷰어 결과와 구분한다.
- out 트리 객체: 1da2e9f5600dc5f91dd0a989188ef7b0ecb19437. production 작업트리는 검토 전·중간 확인에서 clean.
- 요청문의 “R14 GO 대상 1bb45b3”는 정정 필요. 1bb45b3 검토는 NO-GO였고, 후속 098728c 코드가 포함된 **3aca0906dcf0e8690ab534f0bef3abf6a02cdb9a**에서 잔여를 종결했다. 옛 실패 시점을 GO 기준으로 소급하지 말 것.

### 검증 범위
Windows 11, Python 3.12.14, numpy 2.5.3, scipy 1.18.1, pandas 3.0.6, openpyxl 3.1.5의 격리 환경. Bash 미가용, fcntl 미가용, WSL 조회는 접근 거부였다. 제한을 바꾸지 않았다.

| 실행 | 리뷰어 관측 |
|---|---|
| R15/R16 관련 6개 시험 파일, 작업 폴더 전용 basetemp | **61 passed, 3 failed / 37.10s**. 실패는 Bash 없음 1개·fcntl 없음 2개 |
| 폭 계약 관련 선택 회귀 | **9 passed, 14 deselected / 3.88s** |
| check_u14 --new out --schema-only | rc 0, promotion_eligible=false, env_contract_legacy=13 |
| check_u14 --new out --old-rev 42314198e0beee59834d394cdba2757183503b59 | rc 4, legacy 승인 true, promotion false. 정상 대조군 |
| check_u14 --new out/archive/legacy_r6_u14 --schema-only | rc 2; schema 52 / provenance_cols 25 / content 10 / provenance 1. 예전 40·25·6·1과 다름; openpyxl 계약 추가가 반영된 출력 |
| 독립 코드 반례 | [REPRO_RESULTS.json](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/REPRO_RESULTS.json), 실제 CLI/함수 호출 |
| 과학적 추론 대조군 | [SCIENCE_REPRO_RESULTS.json](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/SCIENCE_REPRO_RESULTS.json), 해석 가능한 합성 함수 사용 |
| 전체 pytest | 최종 집계는 별도 TEST_STATUS.md 참조. 작성자 390 passed를 이 기계에서 재현했다고 주장하지 않음 |

첫 표적 실행은 공용 임시 폴더의 pytest-current 접근 거부로 종료 정리도 실패했다. 전용 basetemp 재실행 결과를 위 표에 사용했다. 이 환경 오류는 아래 결함의 근거가 아니다. Linux용 파일 잠금을 가짜로 대체해 통과시키지도 않았다.

## 2. 코드 반례

### P1-01 — GC의 보관 단위와 삭제 단위가 달라, 다른 산출의 최신 부분 결과를 삭제한다
위치: [gc_partial.py:74](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/scripts/gc_partial.py:74), [삭제 루프:90](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/scripts/gc_partial.py:90).
무효화되는 주장: 조건 8 축 ④의 산출별 최근 N개 보존.

만드는 상태:
- matrix/A/matrix_100.csv = 100의 구 시도
- matrix/A/matrix_200.csv = 200의 **유일한 최신 시도**
- matrix/B/matrix_100.csv = 100의 새 시도

index에는 이 순서로 세 항목을 기록한다. 실제 publish_target으로 디렉터리를 만들고, POSIX 기록 잠금이 없는 Windows에서는 문서화된 index 모양을 fixture에 직접 작성했다. GC 코드는 수정하지 않았다.

호출: python scripts/gc_partial.py --root <fixture> --keep 1 --apply

기대: 100의 A만 제거하고 200의 A는 파일과 index에 남는다.
실제: **rc 0**, matrix/A 전체를 지워 200의 유일한 결과까지 사라지고 index에서도 제거된다. REPRO_RESULTS의 gc_shared_attempt.victim_survives=false.

원인: keep/doomed는 (kind, artifact)로 계산하지만 rmtree와 index 제거는 (kind, attempt)로 계산한다.
최소 종결 조건: 삭제 후보 파일/단위와 retained 집합을 한 모델로 결정한다. 어떤 retained artifact가 참조하는 attempt 디렉터리도 통째로 삭제하지 않는다. 이 세 항목 교차 fixture가 회귀로 남아야 한다. index와 디스크 갱신 중단/동시성은 별도의 추가 검토 대상이며 이번에 재현했다고 세지 않았다.

### P1-02 — absolute attempt-id 하나로 partial 목적지가 canonical이 된다
위치: [verify.py:1283](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/bms_balancing/verify.py:1283), [실제 matrix 게시 경로:1808](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/bms_balancing/verify.py:1808).

독립 호출:
    canonical = fixture / "canonical-fixture/matrix_100.csv"
    dest = publish_target(canonical, "partial", run_id=str(canonical.parent.resolve()))

기대: 잘못된 attempt-id를 첫 디렉터리 생성 전에 거부한다.
실제: **dest.resolve() == canonical.resolve()**. REPRO_RESULTS.partial_canonical_target.is_canonical=true.
이 반례에서는 반환 경로를 확인했으며 canonical payload를 쓰거나 사용자 산출을 덮지 않았다.

원인: Path 결합의 절대경로 성분은 앞의 partial/kind를 버린다. run-id는 CLI/환경에서 받을 수 있는데 단일 식별자 검사가 없다. production은 이 반환 경로에 atomic_write_csv를 한 뒤 record_partial을 호출하므로 뒤의 relative_to 오류를 예방 장치로 간주할 수 없다.
최소 종결 조건: attempt-id를 제한된 단일 성분으로 검증하고 절대경로·부모 이동·구분자·alias를 거부한다. 해석된 목적지가 고정 partial root 아래임을 쓰기 전에 확인한다. 단순 “partial이라는 문자열 포함” 검사는 불충분하다. 이 검토는 실제 canonical 전체 게시 성공까지 재현한 것은 아니며 **게시 목적지 불변식 자체의 반례**다.

### P1-03 — --old 디렉터리에는 과거 revision 결속 없이 일회성 승인이 붙는다
위치: [check_u14.py:458](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/scripts/check_u14.py:458), 특히 481행의 조건부 old_rev_full 비교.

fixture: 현행 out를 복사하고 sidecar와 본문 run_id만 제거한다. 수치·입력 영수증은 현행 그대로다. 이것은 기록된 옛 revision에서 추출한 산출이 아니다.
호출:
    python scripts/check_u14.py --new out --old <current-as-old>

실제: **rc 4, legacy_transition_approved=true, legacy_transition=U18B-R16-2026-09-16**.
정상 대조군 --old-rev 42314198…도 rc 4와 같은 승인을 준다. 함수에 다른 full revision을 주면 거부하지만 --old에서는 revision이 None여서 비교 자체가 생략된다.

영향을 과장하지 않는다: **promotion_eligible=false는 유지된다. 일반 승격 우회가 아니라 특정 과거 상태에 대한 사용자 승인 범위가 넓어진 결함**이다.
최소 종결 조건: 기록된 revision을 직접 추출하거나 그 revision의 exact artifact manifest와 디렉터리 바이트를 대조해야만 legacy 승인 가능. None은 미검증이지 wildcard가 아니다. 임의 디렉터리 비교 자체는 허용하되 승인 false를 유지할 수 있다.

### P1-04 — width_report rc 0은 “한 축만 달랐다” 또는 “전수 cycle” 증거가 아니다
위치: [width_report.py:36](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/scripts/width_report.py:36), [guard:83](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/scripts/width_report.py:83), [compare:99](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/scripts/width_report.py:99).
무효화되는 주장: BML §14-1의 rc 0 자체가 조건 동일성 증거라는 문장.

실제 CLI 반례는 REPRO_RESULTS의 다음 키와 재현 fixture에 있다.

| 입력 | 기대 | 실제 |
|---|---|---|
| 알려진 모든 COMPARED_SETTINGS를 채우고 w_dqdv만 변경 | 허용 | rc 0 — 양성 대조군 |
| w_dqdv와 seed 동시 변경 | 거부 | rc 2 — 방어 대조군 |
| w_dqdv + full_cell SHA 변경; 행/sidecar receipt도 그 입력으로 일치시킴 | 거부 | **rc 0** |
| sidecar cycles=[0,1] 유지, B에서 cycle 1 삭제 | 거부 또는 명시적 부분 비교 | **rc 0**, 교집합 1개로 비교 |
| B에 cycle 0 중복, 마지막 행의 폭만 변경 | 거부 | **rc 0**, dict가 마지막 행을 선택 |
| B의 첫 cycle LAM_NE_hi=nan | 거부 | **rc 0**, nan을 포함한 표/판정 출력 |

원인: 일반 provenance/row validator를 사용하지 않는다. 열거한 설정만 비교하고 입력·코드·환경 결속을 확인하지 않는다. 키 부재 양쪽은 None==None으로 통과한다. CSV의 SHA/sidecar 결속 검사도 없고 cycle은 교집합/dict 축약이다.

최소 종결 조건:
1. 완전한 typed 산출을 기존 검증 경로로 읽고 CSV↔sidecar↔입력 역할/SHA를 대조.
2. 코드/목적함수 버전·환경·대조할 설정의 required key 집합을 명시. 지정한 변경 축 이외의 차이 거부.
3. (cell, cycle) 유일성, 본문과 sidecar의 exact roster, 두 파일의 동일 모집단을 강제. 부분 비교가 필요하면 별도 이름/상태로 보고.
4. NaN/무한값/뒤집힌 구간/잘못된 lower-bound 태그를 소비 전 거부.
이 반례가 작성자 실데이터 두 파일이 실제로 다르다는 증거는 아니다. **현재 비교기가 동일성을 증명한다는 주장을 무효화**한다.

### P2-01 — 폭 tagged union이 의미를 닫지 못하고, 빈 허용집합을 measured 0으로 낸다
위치: [schema.py:290](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/bms_balancing/schema.py:290), [check_rows:665](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/bms_balancing/schema.py:665), [verify.py:433](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/bms_balancing/verify.py:433), [fallback:470](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/bms_balancing/verify.py:470), [cycles.py:78](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/bms_balancing/cycles.py:78).

완전한 CYCLES_ROW와 유효한 입력 영수증을 만든 후 한 축씩 변경:
- width_is_lower_bound="False" 또는 "banana"
- width_tol=-0.5
- LAM_NE_lo=0.2, LAM_NE_hi=-0.2

**check_width_union뿐 아니라 전체 check_rows도 모두 []**. 정상 대조군도 [].

별도 실제 producer 함수 반례:
    _width_fields(True, J=lambda p:1, ..., best_val=1, tol=-0.5, starts=0, ...)
허용집합은 J<=0.5여서 공집합인데 실제 반환은 **width_status=measured, 세 mode의 lo=hi=0**.
여기서는 단순 예외 주입 없이 실제 optimizer/폭 함수를 호출했다.

최소 종결 조건: CLI와 core 모두 유한한 비음수 tol 및 유효한 계산 기준값을 검사. best와 모든 witness의 상자·목적값 적합성을 먼저 확인. 유효 witness가 없으면 failed/거부이고 best를 무조건 복구값으로 넣지 말 것. CSV에서는 True의 정해진 직렬화, lo<=hi, 유한값, 필요 시 점추정 포함을 검사. **measured인 참 0은 허용하되, 안 잼/실패/빈 집합을 0으로 바꾸지 않는다.**

### P2-02 — run receipt 필수 결속을 제거한 객체도 verified=true
위치: [verify_run_receipt.py:62](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/scripts/verify_run_receipt.py:62), [evidence_gate.py:275](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/reviews/evidence_gate.py:275).

입력: 실제 HEAD/tree와 실제 evidence_gate.py blob을 넣고 code/instrument/signature만 둔다. receipt_version, package, materialized, runtime, produced_utc는 없다. 공개 receipt_signature로 이 객체의 digest를 계산한다.
호출: python scripts/verify_run_receipt.py --receipt <incomplete-receipt.json> --target <bms-balancing>
실제: **rc 0, verified=true, receipt_version=null**, skip-instrument를 사용하지 않았다.

이것은 암호학적 서명 위조나 실행 증명 우회라고 부르지 않는다. 현재 signature는 키 없는 무결성 digest다. ancestry/tree/instrument의 대조 자체는 작동한다. 문제는 그 부분 대조를 **불완전한 run receipt 전체 검증**으로 출력한다는 것이다.
최소 종결 조건: supported receipt version과 closed/typed required 구조를 먼저 확인하고 package 결속을 필수화. 실행 여부는 이 객체만으로 증명되지 않는다고 유지. 부분 검증을 지원하려면 code_reference_verified 등 다른 상태로 분리하고 verified 전체 성공을 주지 않는다.

## 3. P1-05 — 관측이 지지하는 것보다 강한 과학 결론
위치: [BML §12-6:473](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/reviews/BML_R1_RESPONSE.md:473), [§14-1:592](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/reviews/BML_R1_RESPONSE.md:592), [§14-3:611](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/reviews/BML_R1_RESPONSE.md:611), [§15-6:839](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/r17-head/bms-balancing/reviews/BML_R1_RESPONSE.md:839).
독립 실행: science_repro.py. 아래는 논리적 반례이지 보유하지 않은 실제 셀 데이터의 재적합이 아니다.

### 3.1 초기값에 둔감한 것은 비식별성의 증명이 아니다
J_A(p)=||p-a||², J_B(p)=||p-b||²를 사용했다. 두 함수의 Hessian은 2I이고 전역 최소가 각각 유일하다.
- 각 모델에서 gamma 초기 0.25/하한 0과 초기 0.02/하한 0.02는 같은 최적점에 도달.
- A의 최적 gamma=0.2407, B=0.2240.
- NE를 나타내는 단순 signed proxy는 A=-0.02, B=+0.02.
즉 요청문과 같은 “시작/하한 변경으로 안 움직이고 모델 간 부호가 다름”이 **양쪽 모두 식별 가능한 모델**에서도 일어난다.

수용 가능한 문장: “시험한 두 gamma 시작/하한 변경은 그 차이를 설명하지 못했다.”
수용 불가: “따라서 다른 설정은 원인이 아니고 비식별성이다”, “multistart가 같으므로 진짜 전역 최소다.”
같은 목적함수·입력·전처리·정규화·가중·bound에서 서로 다른 mode를 내는 근최적 witness를 검증해야 한다. 다른 모델/목적함수 간 차이는 model discrepancy일 수도 있다.

### 3.2 하한의 크기 순서는 참 폭의 순서가 아니다
관측 하한 A=2.439, B=7.099는 참 폭 A=20, B=8과 동시에 모순 없이 성립한다. 관측비 2.91인데 참 비는 0.4일 수 있다.
따라서 “찾은 하한이 2.91배”는 가능하지만 **참 폭이 넓어졌다/LLI가 참으로 가장 좁다**는 증명은 아니다.

같은 이유로 A의 발견 구간이 양수뿐이었다고 부호 식별이 성립하지 않는다. B에서 유효한 양·음 witness를 실제로 찾았다면 B의 부호 모호성은 입증할 수 있지만 “A에서 있던 부호 식별을 B가 잃게 했다”는 더 강한 문장은 아직 미입증이다. signed witness 파라미터와 J값을 함께 저장해 재평가할 수 있게 할 것을 권한다.

또한 현재 기준은 J<=1.01 J_min이다. 합성 예:
- J_A=1+x²: 폭 0.2, 곡률 2.
- J_B=J_A+100+(x-0.1)²: 폭 1.421302…, 곡률 4.
항을 추가해 곡률이 커져도 최소값에 비례하는 허용 폭이 커져 수용구간이 넓어진다. 이 규칙을 유지할 수는 있지만 이를 통계적 신뢰구간이나 정보량 감소와 동일시하면 안 된다. fixed absolute excess, 잔차/잡음 기준, 동일 witness의 목적함수별 수용 여부 등으로 원인을 나눠 보아야 한다.

### 3.3 큰 RMSE는 원인을 확정하지 않는다
합성 뒤집기에서 5.04가 나왔고 실데이터가 0.47이라는 이유로 실데이터 방향 규약을 배제할 수 없다. 곡선 크기·평활·정규화가 다른 집합의 RMSE 수치는 식별 가능한 원인 서명이 아니다. 합성 측정 범위를 바꿔 gamma가 그대로인 것은 그 합성 함수의 대조군이지 실제 곡선 구간 영향의 부재 증명이 아니다.

수용: “검토한 전처리/목적함수에서 실데이터 맞춤이 좋지 않다”; “항상 bound에 붙는 구현은 아니다.”
미수용: “optimizer·방향·범위는 배제됐고 포팅 버그가 아니다.” 실데이터의 통제된 방향/범위 변형과 native 구현의 같은 입력 중간배열 대조 없이는 열린 원인으로 남겨야 한다.

### 3.4 외부 구현과 ground truth를 구분할 것
pyDMA 결과표와의 일치는 구현 간 일치이지, 독립적으로 알려진 물리적 LAM/LLI 참값을 의미하지 않는다. [PyDMA 공식 저장소](https://github.com/tum-ees/PyDMA)는 반쪽전지 전위로 pseudo-OCV를 재구축하고 목적함수 가중을 선택하는 모델 기반 도구로 설명한다. 이 일반 설명은 이번에 사용한 과거 pyDMA 버전이나 규진팀 표의 provenance를 검증한 것이 아니다.
“정답 있는 데이터”는 합성 주입 truth/독립 측정 truth가 있는지 구별하고, 없으면 “외부 도구 참조값이 있는 자료”로 수정한다.

최소 종결 조건: 위 강한 단정을 좁히고 근거·witness·조건부 범위를 문서와 출력에 함께 고정한다. §12-8이 실데이터 CSV/sidecar 부재를 정직하게 신고한 점은 인정한다. 이 검토는 그 숫자의 실제 재현이나 반증을 주장하지 않는다.

## 4. 요청문 §5 네 질문에 대한 답
1. **chain rule은 고쳐야 한다. 충실 포팅은 별도 legacy objective로 보존한다.** 조용한 기본값 교체도, 새 과학 실행에 알려진 잘못된 미분을 조용히 계속 적용하는 것도 피한다. objective_version=legacy_matlab / chain_rule_v2 같은 명시 선택을 영수증·행·sidecar·비교기에 전달하고 서로 섞지 않는다. 기존 재현 작업의 A 유지와 신규 과학 추정에서 A를 권장하는 것은 다르다. B가 검증되기 전에는 신규 실행에 명시 선택을 요구하는 것이 낫다.
2. **“200배”를 계약 회귀로 못 박지 말 것.** 독립 analytic E_PE=3+x², E_NE=0.2+0.3x²의 target E_cell 수치미분에서 기존 최대 오차 0.370833…가 1/a 적용 후 4.027e-10로 줄었다. 이는 수학적 불일치의 독립 확인이며 작성자의 200배 fitting 실험 재현은 아니다. 필요한 회귀는 a≠1의 chain-rule 항등식, a=1 대조군, 복수 truth/bound/잡음/평활 사례와 예산별 fit 정확도다. 특정 optimizer의 오차비는 환경 의존적이며 보조 관측으로 둔다.
3. **편향과 폭은 다르다는 구분은 맞다.** B의 폭이 줄어들지는 미지수다. 수정한 목적함수로 baseline/target/scales/near-optimal witness를 모두 새로 계산해야 한다. 현행 폭은 pristine ref_p를 고정한 조건부 폭이므로 기준 상태 불확실성 전체까지 덮는다고 쓰지 말 것.
4. **w_dvdq=1의 잘못된 미분은 신규 추정의 안전한 기본값이 아니다.** legacy 재현은 A와 가중을 명시 보존. 신규 진단은 pOCV-only와 corrected derivative를 나란히 비교하고, 검증 후 기본을 정한다. dV/dQ는 같은 전압 데이터에서 나온 변환이므로 0으로 하면 “독립 정보가 그만큼 사라진다”는 단순 해석도 피한다. w_dqdv는 별개 항이며 바꾸어 문제를 고친 것으로 기록하지 않는다.
B의 실제 LAM 개선·실험 정량 대응은 실데이터 A/B 및 원자료 검토 전에는 미입증이다.

## 5. 조건별 판정
| 조건 | 판정 | 근거와 한계 |
|---|---|---|
| bundle commit 집합 + 기록된 예외 | 검토 범위 수용 | 표적 회귀 통과. out 기준 예외 소비 재현 |
| legacy_transition 별도 승인 | **미종결** | P1-03. promotion false와 rc 4 보존은 인정 |
| 기록용 CLI root 필수 | 검토 범위 수용 | 누락/빈 root 관련 회귀 통과 |
| preserve_handoff 공유 manifest 판별 | 구현 확인·실전 shell 미완 | 목록 키 관련 회귀 통과; Bash 실행 한 건 환경 실패. 호출 문자열 개수는 모든 소비 경로의 의미적 증명이 아님 |
| R16 조건 6 동적 shadow 대조군 | 검토 범위 수용 | 4 runner 각각 무장 시 marker 발생, 방어 시 marker 없음 + argparse 도달 회귀 통과. AST만의 대조가 아님 |
| shared snapshot | 검토 범위 수용 | 실제 워크북 재-export 양성 대조와 공통 snapshot 재사용 회귀 통과. command 배선 회귀 일부는 여전히 source-count 검사 |
| dataset manifest/env openpyxl | 부분 | 관련 검사 대부분 통과, 변경 입력 게시 두 시험은 fcntl 부재로 미완 |
| run receipt | **부분** | code ancestry/tree/instrument 대조 수용, P2-02 required package/version 경계 미종결 |
| partial 수명/GC | **미종결** | P1-01, P1-02 |
| receipt_paths 소비자/대체 증거 이름 | 구현 확인 | 기존 검사 범위 수용; 원격 독립 replay 전수 수행한 것으로 확대하지 않음 |
| unknown 사유 셋의 문서 표류 | 여전히 개선 필요 | UNKNOWN_BLOCKERS를 기계 정본으로 결정 기록 스키마와 보고 템플릿을 생성/대조. 옛 승인문을 새 의미로 덮어쓰지 않음 |
| width tagged union/비교 | **미종결** | P1-04, P2-01 |
| C의 비식별성·폭·gamma 원인 결론 | **재작성 필요** | P1-05 |
| chain rule | 알려진 미구현 | 새 발견으로 중복 계산하지 않음. 위 §4에 수정/버전 전략 답변 |

## 6. 다음 회신의 최소 닫힘 조건
- GC의 교차 artifact 보존, partial 목적지의 사전 경계 검증.
- legacy old identity가 빠진 비교에 승인 부착 금지.
- width 소비자의 입력/환경/코드/본문/sidecar/roster/유한값 결속.
- 음수 tol·빈 feasible set·거짓 lower-bound·뒤집힌 구간을 거부하는 producer/consumer 회귀.
- incomplete run receipt를 전체 verified로 출력하지 않기.
- 과학 결론을 실제 근거에 맞게 좁히고 A/B objective 버전을 명시하는 계획 제시. 미승인 실데이터 재계산을 임의로 시작하지 말 것.
- Linux 지원 환경의 회귀 출력과 이번 반례가 **의도한 이유로** 거부되는 출력 제출.

## 7. 재현 자료
- [코드 반례 생성/호출](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/repro_r17.py), [실제 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/REPRO_RESULTS.json).
- [과학 논리 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/science_repro.py), [실제 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/SCIENCE_REPRO_RESULTS.json).
- [실행 방법·범위](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/REPRO_README.md), [시험 상태](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/TEST_STATUS.md).
- [Claude 전달용 회신](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r17_review_20260922/CLAUDE_REPLY.md).

원본 CSV·모델은 변경하지 않았다. GC 시험에서 삭제된 것은 새로 만든 fixture의 A 디렉터리(파일 두 개)뿐이며 스크립트로 재생성할 수 있다. 원시 CSV/합성 fixture 검토는 스프레드시트 읽기 전용 검토 지침에 따라 원자료·파생 수치·조건부 해석을 분리했다. **R17 NO-GO, 다른 트랙 판정은 변경 없음.**
