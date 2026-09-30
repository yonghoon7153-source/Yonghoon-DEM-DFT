# Codex 재판정 — LHS 피복률 두 묶음 재검증 (HOLD 수정 0008–0011) · 2026-09-30

> **반입 기록 (claude · 09-30 밤)**: 1저자가 전달한 Codex 재판정문 **원문 그대로** (아래 가로줄 밑).  전달 메시지: *"재검증 완료. 기존 P1 두 건은
> 닫혔고 새 P1은 발견하지 않았습니다. 다만 P2 두 건이 남아 전체 HOLD입니다 … 패치별로 0008·0011 GO / 0009·0010 HOLD입니다. 생산 코드는 수정하지
> 않았습니다."*  증거 ZIP `codex_lhs_coverage_reverify_20260930.zip` (sha256 `b9f815a5b5444d16…` · 1,397,978 B) → 스크립트 · 결과 · 로그 · 매니페스트는
> `docs/reviews/codex_lhs_coverage_reverify_evidence_20260930/` (합성 fixture 폴더 · 우리 소스 사본은 반입하지 않음).  본문의 `C:/Users/Administrator/…`
> 링크는 Codex 작업 공간의 절대 경로다 — 이 리포에서는 같은 상대 파일 · 줄 번호 (검토 트리 = `review-coverage-20260930` 의 `002cc2881`) 로 읽는다.
> 우리 재현 (같은 스크립트 `audit_delta.py` 를 검토 worktree 에 실행): 스키마 변이 10/10 accepted (필수 단계 done 2/2) · 지원 범위 안 반올림 반례 diff/B
> **1.3323976750260462** (동일) · 비단조 예 동일 · 깨끗한 import False · 생산자 대조 8/8 동일 = **전부 일치**
> (`_reproduction_delta_results_wtcov_002cc2881.json`).  Codex 후보 9 파일 ↔ 우리 검토 트리 = CRLF 를 빼면 동일.  원장 `LHSC-01`~`06` · 새 항목은
> `findings.json` · 판정 반영은 진행 문서 · 체크리스트 4c.

---

# LHS 피복률 두 묶음 재검증 — HOLD 수정 0008–0011 (2026-09-30)

## 0. 결론과 범위

**묶음 HOLD. 기존 P1 두 건은 닫힘. 이번 범위에서 새 P1은 발견하지 않았지만, LHSC-03·04의 P2 반례가 남는다.**

닫힌 수정까지 되돌릴 이유는 없다. 남은 것은 (1) 산출물 스키마의 결손·모순 통과, (2) 새 지원 범위 안의 반올림 오탐이다. 전자는 현재 정상 생산자가 그 결함 파일을 만든다는 주장이 아니며, 후자는 피복률 수치를 바꾸는 결함이 아니다.

- 요청서/패치 고정 핀: **ac484ba5cda082caffe2c3c408de86cbd760befc**. 첨부에는 "§4 해시"라고 했지만 실제 해시가 없었다. 요청서 경로의 파일 이력에서 그 요청서를 담은 커밋을 읽기 전용으로 찾아 고정했다.
- 검토 트리: **da4670594 + 제출 패치 0001–0011**. 이전 검토 핀은 2e57dff90e7eebead7a446478f97e2c414176c28. 이후 브랜치 끝은 사용하지 않았다.
- 0001·0002·0004·0005의 기존 GO는 재심하지 않았다. 이 글의 GO는 해당 수정의 소프트웨어 계약에 대한 것이며 v2 물리 모델의 검증·코퍼스 적격성 승인이 아니다.
- 생산 코드·원장·물성·판정 문턱·Git ref는 변경하지 않았다. 별도 소스 사본에서 CPU 합성 검사만 실행했다. DEM 시뮬레이션·원격 캠페인·실 130/64 재수확은 하지 않았다.
- 이하 줄 번호는 패치 11개를 적용한 후보 트리 기준이다. [소스·패치 해시 원장](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/source_manifest.json), [독립 실행 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_evidence_20260930/delta_results.json).

### 이전 항목별 판정

| 항목 | 심각도 | 재판정 | 근거 |
|---|---|---|---|
| LHSC-01 | P1 | **닫힘** | 옛 무효 분모·고립 NaN 반례가 blank+사유로 바뀜. 정상 접촉 0은 ok·0.0 유지 |
| LHSC-02 | P1 | **닫힘** | 명시적 stop_after의 atoms-only가 failed. raw/CSV 두 경로의 음성 대조 및 기본 viewer 양성 대조 통과 |
| LHSC-03 | P2 | **부분** | 빈/임의 status·필수 키 전체 부재는 거부. 그러나 AM 개수 누락·NaN 면적 등이 필수 단계 done으로 통과 |
| LHSC-04 | P2 | **부분** | 옛 경계 반례는 따로 제외됨. 새 지원 범위 안에서도 정상 반올림을 초과로 셈 |
| LHSC-05 | P2 | **닫힘** | 순수 기하 분리. 깨끗한 프로세스에서 수확기 import 후 plastic_coverage 미적재. 기존 import 우회 두 개 검출 |
| LHSC-06 | P3 | **닫힘** | 분모 보정 proxy·분자 미절단·제외 편향 방향 미정·계산 상태와 물리 적격성 구별을 명시 |

### 신규 패치별 판정

| 패치 | 판정 | 이유 |
|---|---|---|
| 0008 / aba311054 | **GO** | LHSC-01의 선택된 침대 전체 빈칸 계약을 만족 |
| 0009 / 471ad778b | **HOLD** | LHSC-02는 닫혔으나 같은 패치의 LHSC-03은 미완료 |
| 0010 / c125254a9 | **HOLD** | LHSC-05는 닫혔으나 같은 패치의 LHSC-04는 미완료 |
| 0011 / 002cc2881 | **GO** | 숫자 변경 없이 해석 범위를 바로잡음 |

## 1. LHSC-03-R2 — AM 개수 누락을 "AM 없음"으로 읽는 스키마 우회

**P2 · 기존 LHSC-03 잔여.** 무너지는 결론은 "coverage 필수 단계의 done이 유효한 v2 값 또는 온전한 blank 판정을 보증한다"이다.

위치: [app.py:3214](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/webapp/app.py:3214), [app.py:3220](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/webapp/app.py:3220), [필수 단계 연결:3236](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/webapp/app.py:3236).

현재 검사는 필수 키에 None이 아닌 값이 있는지를 먼저 보고, 다음 분기로 간다.

~~~python
if (diag.get('n_am') or 0) > 0:
    # coverage_AM_mean_physics_v2가 유한 실수인가
    ...
return True
~~~

이는 **실제 0개 / 키 누락 / 음수 / NaN**을 구별하지 못한다. 면적 키는 None 여부만 검사하므로 문자열·NaN·음수도 남는다.

### 실제 생산자 출력에서 출발한 변이

먼저 compute_case로 정상 합성 침대의 full_metrics.json을 만들었다. 그 결과를 복사한 뒤 아래 필드만 변이했다. 테스트용 필수 키 목록으로 가짜 정상 파일을 먼저 만든 것이 아니다.

| 변이 | _coverage_v2_written | 실제 _coverage_stage / summarize |
|---|---:|---|
| diag.n_am과 AM 피복률 키들을 삭제 | True | required stage ok=True, **done** |
| area_AM전체_SE_total_physics_v2=NaN | True | required stage ok=True, **done** |
| n_am=-1 또는 NaN, 피복률 키 없음 | 모두 True | 직접 스키마 호출 |
| 면적="broken" 또는 -1 | 모두 True | 직접 스키마 호출 |
| coverage_AM_mean_physics_v2=-1 | True | 직접 스키마 호출 |
| status=ok인데 무효 분모 수=1 또는 contact failures=1 | 모두 True | 직접 스키마 호출 |
| status만 blank: 사유로 바꾸고 양수 면적·피복률을 남김 | True | 직접 스키마 호출 |

필수 단계 재현에서 **계산 subprocess만 변이 파일을 쓰는 대역**으로 교체했고, _coverage_stage·검증기·summarize는 실제 함수다. "현 생산자가 이런 파일을 정상적으로 생성한다"거나 "실 130건이 이미 오염됐다"는 주장은 하지 않는다. 그러나 검사기가 막기로 한 불완전 산출물에 대한 false-green은 재현된다. 문자열·음수 변이도 통과하므로 비표준 JSON NaN 하나에 의존하는 반례도 아니다.

재현: §5의 환경 설정 후 아래 명령. 결과 JSON의 schema_mutations를 본다.

~~~bash
python3 lhs_coverage_reverify_evidence_20260930/audit_delta.py
~~~

### 최소 해제 증거

- n_am을 **명시적 비음수 정수(bool 제외)**로 요구한다. 누락을 0으로 보충하지 않는다.
- ok에서는 면적의 유한·비음수, 피복률의 유한·[0,100], 관련 개수의 정수·범위를 검사한다. 반경/분모 실패·접촉 계산 실패와 ok가 공존하지 못하게 한다.
- blank에서는 비지 않은 사유와 진단을 받되, 물리 값의 양수 잔재를 받아들이지 않는다. 내부 집계 오류에서 진단 일부가 None일 수 있다는 기존 의도는 보존한다.
- 위 음성 대조와 함께 **실제 생산자의 정상 침대·고립 AM·SE-only·무효 분모·NaN 반경·scale 불일치·접촉 열 부재**를 양성 대조로 둔다. 계산을 검증기에 복제할 필요는 없다.

## 2. LHSC-04-R2 — 새 지원 범위 안에서도 반올림 오탐

**P2 · 기존 LHSC-04 잔여.** 무너지는 결론은 "등록 지원 범위 안에서 축별 탐침의 합 B가 정상 6자리 반올림을 덮는다"이다.

위치: [지원 범위:366](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_descriptor_harvest.py:366), [축별 합:393](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_descriptor_harvest.py:393), [생산 진단의 범위 적용:430](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_descriptor_harvest.py:430).

### 반례 — 실제 geometry 함수와 contact_area_check 호출

원 입력 길이는 sim 단위, 면적은 sim²이다.

~~~text
r1    = 0.0012345649
r2    = 0.0012345551
delta = 0.00246909
A_true (실제 함수) = 4.277265491991140e-6
~~~

독립 60자리 십진 계산은 A_true=4.2772654919826414…e-6. 어느 계산이든 6 유효숫자 토큰은 **4.27727e-6**이다. 네 값을 정상 %.6g로 기록하면:

~~~text
r1_token = r2_token = 0.00123456
delta_token = 0.00246909
area_token  = 4.27727e-6

gap    = 2.999999999982184e-8
margin = 2.500000000000000e-8
_in_domain_rows = True

A_calc = 4.788221979681050e-6
diff   = 5.109519796810495e-7
B      = 3.834830916160681e-7
diff/B = 1.332397675026046
~~~

실제 contact_area_check 결과:

~~~text
n_values_beyond_6sig = {area: 0, delta: 0, radius: 0}
n_boundary_excluded = 0
n_beyond_tol        = 1
~~~

**면적을 변조하지 않고 정상 반올림만 했는데 불일치 1건이 된다.** 옛 행 수준 함수만 다시 돌린 결과가 아니라 새 범위 분류가 포함된 생산 진단 진입점의 결과다.

한정: 두 구의 중심이 매우 가까운 깊은 겹침 합성 경계 시험이다. 실 130/64에서의 발생률을 주장하지 않는다. 이 진단은 기록 전용이므로 이번 반례가 피복률 값이나 수확 거부를 직접 바꾸지는 않는다.

### 왜 범위 분리만으로 해결되지 않았는가

반올림 전에는 다른 두 반지름이 같은 토큰으로 합쳐진다. 면적의 (r1²−r2²)²/d² 항 때문에 동시 오차가 축별 한 번씩의 탐침으로 덮이지 않는다. 포함 경계를 넘지 않는다는 보장은 **공동 오차의 상한**과 다르다.

"각 입력에 단조"라는 설명도 지원 범위 전체에서 성립하지 않는다. 실제 함수에 r1=.002, r2=.001을 넣으면:

~~~text
delta=.00160 → A=2.708181095665975e-6 sim²
delta=.00161 → A=2.678016109139022e-6 sim²
~~~

두 행은 지원 범위 안인데 delta 증가에 면적이 감소한다. 부분 교차 구간의 식

~~~text
A(d) = π/4 · [2(r1²+r2²) − d² − (r1²−r2²)²/d²]
~~~

에서도 d²=|r1²−r2²|에 극값이 있다. [lens_geometry.py:25](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lens_geometry.py:25)의 "불연속" 설명은 일반 포함 경계와 동일 반경·d=0 퇴화를 구별해야 한다. 서로 다른 고정 반지름에서 일반 포함 경계로 접근하면 면적은 0으로 연속이다. "구간 상한 자체가 서지 않는다"는 요청서의 주장도 철회해야 한다. 기하학적으로 0≤A≤π·min(r1,r2)²라는 유한 상한부터 존재한다.

### 기존 수정이 해결한 부분과 해제안

- 옛 반올림 반례·깊은 겹침 치환 반례는 실제 contact_area_check에서 **boundary 1 / 초과 0**으로 바뀌었다. 그 분류 수정 자체는 유효하다.
- delta=0·음수와 A=0은 초과 0, delta=0인데 A=1e-6은 초과 1이었다. 이번 검사에서는 이 비접촉 대조들이 깨지지 않았다.
- 지원 범위 계약을 택하는 것 자체에는 반대하지 않는다. **현재 범위는 부족하다.** 공동 반올림 구간을 안전하게 감싸는 계산(수치 오차 포함), 또는 상한을 보증할 수 있는 더 제한된 범위/불확정 분류가 필요하다. 이 반례에 맞춰 1.001을 임의 증대하는 것은 해제가 아니다.
- "불연속·단조" 설명과 그 이름을 가진 시험을 바로잡는다. 경계 제외 수 외에 실제 시험된 행 수를 명시하면 n_compared를 유효 판정 수로 오독하는 것을 줄일 수 있다.

재현은 같은 audit_delta.py. 결과의 in_domain_rounding_false_alarm 및 interior_geometry_nonmonotonic를 본다.

## 3. 닫힌 수정의 독립 재현

### LHSC-01 / Q1: 침대 전체 빈칸과 진단 개수

[coverage:310](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:310), [blank 변환:365](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:365).

옛 감사 스크립트를 그대로 후보 트리에 실행했다.

- AM 4개 무효 분모: n_am=4, n_free_surface_nonpositive=4, blank 사유 있음. 면적 null, 유효 피복률 없음.
- 고립 NaN 반경: n_am=1, n_radius_invalid=1, blank 사유 있음.
- 정상 고립 AM: status=ok, coverage_AM_mean_physics_v2=**0.0 %**.
- legacy 6변형의 full_metrics(legacy)·per-AM CSV·반환값 해시가 각각 일치했다.

**Q1: 동의.** 정수 진단 개수는 유효 부분집합의 면적·피복률 추정량이 아니다. 전침대 무효와 그 이유를 남기는 계약에 맞는다. 단 "모든 값 키가 언제나 명시적 null"은 엄밀하지 않다. 집계할 AM이 없으면 일부 피복률 키가 생성되지 않는다. 이번 경로에서는 누락/None 모두 값 없음이며, 이를 0으로 채우면 안 된다.

### LHSC-02 / Q2: failed가 맞다

[atoms-only 거부:3167](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/webapp/app.py:3167), [배치 재개 상태:73](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_webapp_batch.py:73), [재개 skip:258](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_webapp_batch.py:258).

옛 CSV-only 반례는 success=False, status=failed, metrics 파일 미작성으로 바뀌었다. 제출 테스트의 raw/CSV × contact/coverage 네 거부와 기본 viewer 두 허용도 통과했다.

**Q2: failed에 동의.** 배치는 done·partial을 건너뛴다. 필수 접촉이 없는 것을 partial로 바꾸면 다음 재개에도 필수 계산을 하지 않는다. stopped_after는 요청한 중단 지점이지 그 지점까지 성공했다는 증서가 아니다. 접촉 파일이 계속 없으면 재시도도 계속 실패해야 한다. 별도 입력 결손 사유를 기록하는 것은 좋지만 성공/부분 성공으로 분류할 이유는 없다. LHS 배치 자체의 입력 사전검사는 별개이며, 모든 누락 케이스가 실제로 이 경로까지 도달한다고 주장하지 않는다.

### LHSC-05 / Q5: 순수 기하 분리에 동의

[수확기 import:140](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_descriptor_harvest.py:140), [legacy 별칭:963](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/plastic_coverage.py:963), [AST lint:464](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_descriptor_harvest.py:464).

깨끗한 Python 프로세스에서 수확기만 import한 뒤 plastic_coverage가 sys.modules에 없었다. 옛 패키지 import·importlib 별칭 우회는 실제 함수를 호출할 수 있는 문장이지만, 새 가드는 두 개 모두 위반으로 검출한다. geometry 별칭 동일성·legacy 수치 대조도 통과했다.

**Q5: 현재 의존 경로의 분리 및 기존 두 우회 해제에 충분하다.** lint를 임의 Python의 완전한 금지 증명으로 부르지 않는 한 getattr·exec·문자열 합성까지 쫓는 작업을 이번 병합 조건으로 추가하지 않는다. 정상 import 경로의 회귀 검사는 유지한다.

### LHSC-06: proxy 라벨 정정

[WALLEXCL_FORMULA:782](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_descriptor_harvest.py:782), [coverage_wall:875](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/candidate/scripts/lhs_descriptor_harvest.py:875).

벽 밖 원판을 포함하는 옛 입력의 결과는 **31.626275510204017 %**로 그대로다. 새 문구는 이것을 ROI 면적의 실제 절단 결과라고 부르지 않는다. 두 벽을 모두 뺀 동일 입자값을 벽 접촉군별로 평균한다는 점도 분명해졌다. 계산값은 그대로지만 formula라는 문자열 메타데이터는 바뀌므로 "파일 바이트까지 무변경"이라는 뜻은 아니다.

## 4. 나머지 질문과 반입 기록

**Q3 — 조건부 동의, 현 스키마는 미완료.** 실제 생산자로 SE만 2개·접촉 0 침대를 만들면 n_am=0, status=ok, AM 피복률 키 없음, 면적 0으로 나온다. "연산 완료, AM 피복률 적용 대상 없음"은 정당하다. 이는 AM 피복률 0도, LHS AM 코퍼스 적격 판정도 아니다. 분모 0인 cap-conflict 분율의 None 역시 정당하다. 다만 개수·분모를 명시적으로 검증한 뒤에만 이 예외를 허용해야 한다. 누락/NaN/음수까지 허용한 §1은 별개다.

**Q4 — 범위 계약이라는 선택에는 동의, 현재 식에는 반대.** §2의 범위 안 오탐이 반례다. 일반 포함 경계·동심 퇴화·비접촉을 구분하고, 범위 안의 상한 보증과 밖의 미판정 표지를 분리해야 한다. 합성 무작위 3000/15000건의 성적은 해당 표본 성적이지 전역 상한 증명이 아니다.

**Q6 — 순서는 가능하지만 지금 전부 claimed_fixed로 바꾸는 것에는 반대.** 남은 LHSC-03·04를 고친 뒤 의존 순서대로 병합·게이트를 실행하는 계획에는 이의 없다. 01·02·05·06은 이번 증거로 닫힘 근거가 생겼지만 03·04는 부분이다. 중간 0006/0007 상태로 배치를 돌리지 말고 최종 트리 해시를 고정한다. 새 디렉터리 재수확, 후보 연산자 라벨, 실제 무효 분모율·경계 제외율·cap 충돌률 보고는 유지한다. 이 리뷰는 원장 수정·병합·배치 실행을 수행하지 않았다.

**반입 정정(P3, 계산 HOLD와 별개):** 제출본 0001–0007은 이전본과 **바이트 동일하지 않다. SHA도 7개 모두 다르다.** 메일 패치 번호 [PATCH n/7]→[PATCH nn/11] 및 제목 인코딩/줄 접기 등이 바뀌었다. 반면 각 파일의 diff --git 이후 본문은 **7/7 동일**하다. 따라서 이전 GO를 재심할 코드 변경은 없지만, "sha 7/7 같다·Codex가 바이트 동일 확인"이라는 문구는 "diff 본문 동일"로 고쳐야 한다. [개별 대조](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_20260930/source_manifest.json)에 양쪽 SHA를 남겼다.

요청서 §4의 명령도 실행 checkout을 요청서 커밋으로 잡으면서 패치 기반은 da4670594라고 쓰고 있다. 해제 증거에는 "요청서/패치 반입 핀"과 "패치 적용 기준"을 분리해 적는 것이 안전하다. 이번에는 기존 검토 후보의 대상 해시 및 옛 7개 diff 동일성을 확인한 뒤 별도 사본에 0008–0011을 적용했다.

## 5. 재현·회귀·한계

[증거 README](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify_evidence_20260930/README.md)에 전체 실행법과 플랫폼 통제를 적었다. ZIP의 소스는 대상 파일만 포함하며 완전한 실행 저장소가 아니다. 전체 후보 소스 사본과 Python 의존성을 준비한 뒤:

~~~bash
export LHS_REVIEW_REPO=/absolute/path/to/full/candidate
export LHS_REVIEW_BASELINE=/absolute/path/to/unpacked/lhs_coverage_review_20260930/baseline
export PYTHONUTF8=1
export PYTHONDONTWRITEBYTECODE=1
python3 lhs_coverage_reverify_evidence_20260930/audit.py
python3 lhs_coverage_reverify_evidence_20260930/audit_pipeline.py
python3 lhs_coverage_reverify_evidence_20260930/audit_harvest.py
python3 lhs_coverage_reverify_evidence_20260930/audit_cli.py
python3 lhs_coverage_reverify_evidence_20260930/audit_delta.py
~~~

audit_pipeline.py는 거부 후 파일이 없는 것이 정상이므로 이전 스크립트의 read_text 한 곳만 존재 여부 guard를 넣었다. 나머지 기존 감사 로직은 유지했다. audit_delta.py가 이번 추가 반례다.

| 독립 실행 | 결과·한정 |
|---|---|
| lens_geometry | 5/5 |
| plastic_coverage | 28/28 |
| coverage_physics_vs_hertzian | 16개 check 통과, rc=0 (번호 ①b 포함) |
| test_pipeline_provenance | 206/206 |
| lhs_design_dataset | 113/113 |
| lhs_descriptor_harvest | Windows 원형 142/144 → fixture LF 통제 143/144 |
| 남은 수확기 1건 | τ median=2.080532952769607, 핀=2.0805329527696066. baseline/candidate 결과 동일; 이번 패치 수치 회귀로 세지 않음 |
| lhs_webapp_batch | 원형은 Windows symlink 권한 오류 뒤 실패. symlink만 byte copy로 치환한 통제 29/29; 배포 환경 symlink 인증 아님 |
| baseline↔후보 legacy 수확기 | 16호출 × 36키, 불일치 0 |
| 전체 check_all | **독립 재실행 안 함**. 제출자의 169/170 및 litdb 단독 통과 로그는 제출 증거로만 보관 |

원형 실패를 지우거나 "전수 초록"으로 요약하지 않았다. 실 침대 발생률·후보 v2의 물리 타당성·병합 후 운영 게이트는 이 합성 재검증이 보증하지 않는다.

## 6. 남은 최소 해제 목록

1. **0009 / LHSC-03:** 누락 n_am의 0 승격 및 무효 값·상태 모순 통과를 막고, 실제 생산자 양성 대조를 보존한다.
2. **0010 / LHSC-04:** 이번 지원 범위 안 반올림 반례를 정상/불확정으로 올바르게 처리한다. 같은 범위 안의 진짜 면적 치환 검출도 함께 보존하고, 상한·단조·불연속 설명을 정정한다.
3. 재판정 근거의 패치 바이트 동일 주장을 diff 동일로 고친다. 01–06 일괄 종결은 하지 않는다.

**HOLD**
