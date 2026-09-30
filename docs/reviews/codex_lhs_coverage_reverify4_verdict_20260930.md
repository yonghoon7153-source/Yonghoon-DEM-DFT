# LHS 피복률 재검증 4 판정

## 0. 결론 · 검토 범위

**HOLD. 새 P1 없음. 이전 최소 해제 목록의 두 P2는 닫혔다. 이번 Q3에 해당하는 잔여 P2 한 계열을 새로 발견했다: 전체 AM이 100%로 클립된 기록에서 상별 평균 0% 또는 상별 표준편차 40%p를 받아들이는 완료 검사기다.**

이전 네 불변식을 구현하지 않았다는 판정이 아니다. 네 가지 모두 구현됐고 옛 반례도 거부한다. 따라서 **LHSC-03-R4와 LHSC-04-R4-PIN은 닫고**, 새 반례는 **LHSC-03-R5**로 분리한다. 생산자가 실제로 틀린 피복률을 냈다는 증거, 실 130/64 데이터 오염의 증거, 닫힌 LHSC-01·02 P1의 재개방은 아니다.

| 요청 / 기존 항목 | 판정 | 근거와 한정 |
|---|---|---|
| Q1 / LHSC-04-R4-PIN | **닫힘** | 자기 신고·로컬 해시 대조·설치 인증 분리. 해시가 맞아도 설치 인증은 False |
| Q2 / LHSC-04-R4-DOMAIN | **기존 반례와 문구 요구는 닫힘** | 1e-100 sim 반례는 E=∞, 미인증. 모든 유한 입력의 안전 처리는 아님; §3의 비차단 P3 |
| Q3 / LHSC-03-R4 | **기존 네 항목 닫힘** | 네 변이 모두 False / 필수 단계 failed. 정상 생산자 출력도 허용 |
| Q3 / 새 LHSC-03-R5 | **열림, P2** | 전체 클립의 상별 통계 모순 2종이 True / 필수 단계 done |
| Q4 / 병합·재수확 순서 | **순서에 동의, 이번 착수 승인은 아님** | 새 P2를 닫은 세대를 게이트·트리 해시로 봉인한 뒤 새 출력 디렉터리 사용 |

### 실물 핀

- 입력 ZIP: `codex_lhs_coverage_reverify4_20260930.zip`, **51,865 bytes**, SHA256 `9d35be5dd6f8fb90adf010d0c4521f9968b12fe2d44db6a0d0f213c560a139ae`.
- 선언 base `220b1426ea39eae13f077e9f0585388f3eb61d08`, tip `9ab4bc3203e64930f860ec805ae9fb09fdb898f5`. 로컬 검토 브랜치 커밋의 원격 실재를 인증한 것이 아니라 **패치 바이트와 적용 후 소스**를 인증했다.
- 이전 후보의 변경 대상 3파일 해시 확인 → 별도 비 Git 사본 → **0016 → 0017** 순서로 적용. 제출 SHA256SUMS **8건** 일치. 적용 후 변경 3파일의 LF 크기·SHA256·Git blob이 제출 manifest와 일치.
- 생산 코드·Git ref·findings 원장은 수정하지 않았다. DEM·설치 엔진·원격 캠페인·실 재수확·실 coverage 배치는 실행하지 않았다. 아래 시험은 격리 소스 사본의 합성 CPU 호출이다.

[독립 소스 원장](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/source_manifest.json) · [이전 판정](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/docs/reviews/codex_lhs_coverage_reverify3_verdict_20260930.md).

## 1. Q3 우선 — LHSC-03-R5: 전체 클립인데 상별 통계는 다른 값

**P2 / REFUTED. 무너지는 결론: “필수 coverage 단계의 done은 기록된 피복률 통계와 클립 장부의 공존을 보증한다.”** 물성식의 정당성이나 정상 생산자의 수치 정확성에 대한 반례가 아니다.

위치: [검증기 전체 평균 하한:3308](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/webapp/app.py:3308), [상별 std는 50%p 상한만 검사:3300](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/webapp/app.py:3300).

### 독립 양성 대조 — 이번에는 클립 기록도 생산자가 직접 생성

`coverage_physics_vs_hertzian.compute_case`를 실제 호출했다. AM_P·AM_S 각각 한 입자, 반경 **0.001 sim (=1 µm, scale=1000)**, AM 중심 간격 0.01 sim이다. 각 AM 주변에 같은 반경의 SE를 중심거리 0.001 sim로 배치하고 AM–SE 접촉을 공급했다. AM–AM 접촉은 없어서 분모는 양수다. 이것은 판독기 시험용 접촉 자료이며 DEM 평형 침대를 주장하지 않는다.

| 입력 AM–SE 접촉 수 (P / S) | n_AM / n_clip | AM_P 평균 | AM_S 평균 | 전체 평균 | 검증기 |
|---|---:|---:|---:|---:|---|
| 0 / 0 | 2 / 0 | 0% | 0% | 0% | True |
| 4 / 1 | 2 / 1 | 100% | 50% | 75% | True |
| 4 / 4 | 2 / 2 | 100% | 100% | 100% | True |

세 기록의 상별 population std는 모두 **0%p**다. 전체 클립 산출물은 AM–SE 접촉 8, geom 결속 8, n_cap=8, AM–SE 총면적 **50.27 µm²**다. 정상 출력은 새 불변식에 막히지 않는다.

### 반례 — 위 전체 클립 출력에서 한 필드씩만 변경

| 변이 | 유지한 장부 | 실제 검사 / 필수 단계 |
|---|---|---|
| `coverage_AM_P_mean_physics_v2: 100.0 → 0.0` | n_AM=2, n_clip=2, 전체 평균=100%, 나머지 정상 출력 그대로 | **True / done** |
| `coverage_AM_S_std_physics_v2: 0.0 → 40.0` | n_AM=2, n_clip=2, 상별·전체 평균=100%, 나머지 그대로 | **True / done** |

생산자는 [raw>100을 세고 min(raw,100)을 저장:327](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:327), [상별 mean·population std를 계산:344](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:344)한다. 따라서 `n_clip == n_AM > 0`이면 저장된 모든 AM 값이 정확히 100이다. **어떤 비어 있지 않은 AM 부분집합도 평균 100%, 표준편차 0%p**여야 한다. 이 명제에는 상별 입자 수·상별 가중·원자료 재계산이 필요 없다.

대조로 부분 클립 정상 기록의 전체 평균을 75%→1%로 내리면 **False / failed**다. 즉 이번 패치의 전체 평균 하한은 실제로 작동하고, 빠진 것은 그 하한이 강제하는 **전체 클립 상태의 상별 귀결**이다.

재현:

~~~text
python lhs_coverage_reverify4_20260930/evidence/audit_r5.py
~~~

[시험 코드](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/audit_r5.py) · [생산자 원출력·변이·실제 필수 단계 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/r5_results.json).

하위 프로세스 실행만 변조 레코드를 기록하는 전달기로 대체했다. `_coverage_stage`, `_coverage_v2_written`, `pipeline_service.summarize`는 실제 함수이며 `required=True`, `verify_failed=False`, `pipeline_status='done'`까지 확인했다. 전체 웹앱 HTTP 흐름이나 실제 재수확을 실행했다는 뜻은 아니다.

### 최소 해제

1. `n_clip == n_AM > 0`일 때 **존재하는 AM 상별/전체 평균은 100%, 존재하는 상별 std는 0%p**를 요구한다. 생산자의 소수 셋째 자리 반올림 계약 안에서 검사하면 된다.
2. 위 두 변이가 helper False뿐 아니라 필수 단계 failed가 됨을 남긴다. 실제 생산자가 만든 0접촉·부분 클립·전체 클립 정상 대조를 유지한다.

없는 상의 키를 새로 요구하거나, 두 상 평균의 단순 평균을 전체 평균에 맞추거나, 일반 부분 클립까지 std=0으로 제한하면 안 된다. 평균을 쓴 일반 분산 상한을 전부 구현하라는 요구도 아니다. 이번 해제는 **전체 클립 끝점의 두 반례**에 한정한다.

## 2. Q1 — 없는 설치 인증을 True라고 부르는 문제는 닫힘

**세 층 분리에 동의한다. 날짜·host·build 필수화는 자기 신고의 완전성 검사이지 사실성 검증이 아니다.** 이 구분을 현재 이름과 출력이 보존한다.

위치: [producer_pin:566](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/scripts/lhs_descriptor_harvest.py:566), [초깃값 False:583](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/scripts/lhs_descriptor_harvest.py:583), [contact_area_check 출력도 False:671](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/scripts/lhs_descriptor_harvest.py:671).

기존 가짜 pin 둘은 claim=False·installed=False로 바뀐다. 추가로 **엔진 소스가 아닌 시험 텍스트**의 실제 바이트를 해시해 다음을 시험했다.

| 입력 | claim_present | source_hash_verified_locally | installed_build_pinned |
|---|---|---|---|
| 로컬 파일·정확한 SHA | True | True | **False** |
| 같은 파일·틀린 SHA | True | False | **False** |
| 이 기계에 없는 source 경로 | True | None | **False** |
| 상대 source_file + 유효 hosts[].path | True | True | **False** |
| 여러 로컬 항목 중 하나 불일치 | True | False | **False** |
| build 누락 | False | None | **False** |

이 표에서 엔진이 아닌 파일도 로컬 해시 True인 것은 결함이 아니다. 지금 표지가 보증하는 것은 **그 파일의 바이트 대조**이며 add_pair의 의미·실행파일·과거 dump와의 연결은 보증하지 않는다. 실제 `contact_area_check.producer_model` 출력도 별도로 대조했다. 제출자가 언급한 실제 원격 source/설치 빌드는 검증하지 않았다.

날짜 `2026-99-99`도 claim=True다. 구현은 YYYY-MM-DD **형식**만 검사하므로 달력상 날짜 유효성이나 실제 작성일을 인증했다고 쓰면 안 된다. 현재 claim이라는 명칭에는 이 한정이 맞으며, 이것 때문에 설치 인증 결함을 재개방하지 않는다.

### LHSC-04-R5-PIN-TYPE — P3, 비차단 강건성

정상 claim에 `"hosts": 1`을 넣으면 [608행](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/scripts/lhs_descriptor_harvest.py:608)에서 `TypeError: 'int' object is not iterable`로 `contact_area_check`까지 중단된다. **False 인증이 True가 되는 결함은 아니다.** 선택 진단의 잘못된 메타데이터가 예외 대신 사유를 가진 미검증 상태로 반환되게 하려면 hosts의 목록 타입과 원소 스키마를 검사하면 된다. 이번 P2 해제 필수 목록에 추가하지 않는다.

## 3. Q2 — 정의역 가드는 개선됐지만 전체 진입점의 예외 차단은 아님

기존 수치 반례는 닫혔다. `r1=r2=1e-100 sim`, 중심거리 `1.9e-100 sim`에서 생산 식 면적이 0으로 언더플로해도 이제 **E=∞**다. 전체 진단도 미인증 1·시험 0·초과 0을 낸다. 이것은 정상으로 인증한 것이 아니라 비교 대상에서 분리한 결과다.

위치: [곱·d_min 가드:527](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/scripts/lhs_descriptor_harvest.py:527). “정상 중간 산술·공개 구형 식·등록 출력 형식 가정하의 진단”이라는 한정은 적절하다. `n_tested`를 설치 인증이나 정밀 비교 통과와 같게 부르지 않는 문구도 반영됐다.

### LHSC-04-R5-DOMAIN — P3, 비차단: 가드 이전 기하 연산의 overflow

아래 실제 함수 호출은 서로 다른 결과다.

~~~text
r1 = r2 = 1e160 sim, delta = 1e159 sim, A_dump = 0 sim²
_producer_error_bound(...) → E=inf, uncertified=True
contact_area_check(...)    → OverflowError: (34, 'Result too large')
~~~

[634–637행 호출 순서](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/candidate/scripts/lhs_descriptor_harvest.py:634)는 점 기하·enclosure를 먼저 계산한 뒤 E 가드를 부른다. 그러므로 **“지원 영역 밖 모든 입력은 예외 없이 미인증으로 기록된다”는 전역 주장은 틀리다.** 영역 밖 입력을 정상 반환하려면 기하 계산 전 마스크가 필요하다. 단, 1e160 sim은 실 LHS와 무관한 극단 입력이다. 실 생산의 P1/P2로 올리지 않으며 이번 병합을 이것만으로 막지 않는다.

곱의 최댓값과 d_min 두 검사는 모든 중간 연산의 정상성에 대한 완전한 증명도 아니다. 다음은 이번 소스에서 **재실행한 유한 표본 증거**다.

| 독립 검산 | 결과 |
|---|---:|
| 세 좌표 성분·좌표 뺄셈 포함 17,926점, Decimal 90자리 대비 | 오차>E **0**, 최대 오차/E **0.21310838611670851** |
| 인증·비음수 6자리 토큰 8,170행 | 거짓 초과 **0** |
| ±1% 보증이 켜진 5,928행 | 양방향 누락 **0**, 분류 변화 **0** |
| 기하 12,000상자×24점=288,000점 | Decimal 80자리 / 실제 로컬 함수 이탈 **0 / 0** |
| 출력 자릿수 경계 500,000 합성 구간 | 보증 263,988구간, 1,980,567 치환값, 누락 **0** |

동심 토큰의 미인증 분리·완전 포함/비접촉 음수 면적 분리도 유지됐다. 이 결과를 설치 C++ 엔진 실행이나 모든 double 입력에 대한 정형 증명으로 인용해서는 안 된다.

[수치 영역 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/numeric_domain_results.json) · [새 극단 입력과 정상 대조](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/r5_results.json) · [3D E 검산](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/error_3d_results.json) · [기하 검산](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/geometry_results.json) · [출력 경계 검산](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/power_boundary_results.json).

## 4. 기존 수정의 회귀와 실행 한정

| 시험 | 이번 독립 실행 |
|---|---|
| 이전 R4 장부 반례 4개 | **4/4 거부**, 필수 단계 failed |
| 이전 스키마 정상 8종 / 옛 변이 20종 | **8/8 허용 / 20/20 거부** |
| 정당한 blank의 rule=None / h_film 부재 | 허용 유지 |
| 실제 생산 함수의 새 클립 대조 | 0접촉·부분·전체 **3/3 허용** |
| lens / plastic / coverage selftest | rc=0 / 0 / 0 |
| pipeline provenance | **214/214**, rc=0 |
| harvest 원본 selftest | rc=1, 이전과 같은 CRLF fixture hash·τ median 1 ULP 두 실패 |
| harvest LF fixture 대조 | CRLF 실패 해소, τ 1 ULP만 남음 |
| batch 원본 selftest | Windows symlink WinError 1314 뒤 calls[0] IndexError, rc=1 |
| batch byte-copy 대조 | symlink_to만 파일 복사로 대체하면 rc=0; 배포 symlink 인증 아님 |
| 옛 수확 값 | baseline 36키×16호출 불일치 **0** |

τ median은 baseline과 후보가 모두 **2.080532952769607**, selftest 기대값은 **2.0805329527696066**이다. 이 차이를 이번 패치 회귀라 부르지 않는다. 제출자의 Linux 녹색 로그와 이 Windows의 독립 실행은 구분한다. **전체 check_all.sh는 이번에 독립 실행하지 않았다.**

[옛 반례 재실행](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/r4_results.json) · [스키마 회귀](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/schema_results.json) · [selftest 로그 요약](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/selftests.json) · [환경 대조·옛 키 비교](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify4_20260930/evidence/regression_results.json).

## 5. Q4 — 다음 순서와 정확한 해제 경계

`0001 → … → 0017 → 이번 잔여 P2 수정 → 게이트 → 트리 해시 고정 → 새 디렉터리 재수확`이라는 **세대 보존 순서에는 동의한다.** 다만 지금은 Q3 반례 때문에 GO가 아니다. 새 디렉터리는 옛 결과 보존·세대 혼합 방지이고 설치 빌드 인증을 대신하지 않는다.

이번 차단 항목은 **§1의 LHSC-03-R5 한 계열**이다. 실제 producer 양성 대조를 유지하며 두 변이를 필수 단계에서 거부하면 된다. 설치 빌드 영수증 전체를 새로 모으거나, 피복 물성식을 바꾸거나, 새 DEM을 돌려야 이번 P2가 닫히는 것은 아니다. P3 둘은 비차단으로 남기되 전역 지원/안전 반환을 과장하지 않는다.

**HOLD**
