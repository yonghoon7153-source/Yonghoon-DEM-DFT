# LHS 피복률 재검증 5 판정

## 0. 결론

**GO — 이번 재검증의 HOLD를 해제한다. LHSC-03-R5(P2)와 LHSC-04-R5-PIN-TYPE(P3)는 닫힘. 새 P1·P2 없음. LHSC-04-R5-DOMAIN(P3)은 비차단으로 열어 둔다.**

이 GO는 **제출 패치 0018·0019의 수정 수용 및 통합 게이트 진행**에 대한 판정이다. 실제 병합·대상 환경의 전체 게이트·트리 해시 봉인·새 디렉터리 재수확을 이미 완료했거나, 실 데이터와 설치 엔진까지 인증했다는 뜻은 아니다. 이번 검토에서도 생산 코드·Git ref·findings 원장은 수정하지 않았고 DEM·실 재수확·원격 캠페인은 실행하지 않았다.

| 질문 / 항목 | 판정 | 독립 증거 |
|---|---|---|
| Q1 / LHSC-03-R5 | **닫힘** | 상별 평균 0%·std 40%p 변이 모두 False / 필수 단계 failed. 99.999%·std 0.001%p도 거부 |
| Q2 / LHSC-04-R5-PIN-TYPE | **닫힘** | 잘못된 hosts 10종이 예외 없이 claim=True·로컬 대조 None·설치 인증 False·사유 반환 |
| Q3 / LHSC-04-R5-DOMAIN | **열림, 비차단 유지** | 1e160 sim에서 기존 OverflowError 재현. 이번 병합 전에 지원영역 마스크를 새로 요구하지 않음 |
| Q4 / 병합 순서 | **동의** | 0001→…→0019→대상 환경 게이트→트리 해시→새 출력 디렉터리. 실제 실행은 별도 절차 |

### 실물 핀

- 입력 ZIP: `codex_lhs_coverage_reverify5_20260930.zip`, **57,408 bytes**, SHA256 `41cc620d72334dc253c8da1df724c0bf0bca46405cfd724fb1bcd7847de5cc73`.
- 선언 base `9ab4bc3203e64930f860ec805ae9fb09fdb898f5`, tip `6e4ef69256a075c5cf5cee337bf30a465cf125d4`.
- 이전 후보의 대상 파일 해시를 확인한 뒤 별도 비 Git 사본에 **0018 → 0019**를 적용했다. 제출 SHA256SUMS **11건** 일치. 변경 3파일은 LF 정규화 후 크기·SHA256·Git blob 모두 제출 manifest와 일치했다.
- 원격에 없는 커밋의 실재를 별도 인증한 것이 아니라 **제출 패치 바이트와 적용 후 소스**를 검증했다. 시험 후에도 검토 대상 소스와 이전 후보의 대상 파일이 그대로인지 해시로 확인했다.

[독립 소스 원장](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/source_manifest.json) · [이전 판정](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/docs/reviews/codex_lhs_coverage_reverify4_verdict_20260930.md).

## 1. Q1 — 전체 클립 끝점의 최소 해제를 충족한다

위치: [전체 클립 분기:3313](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/candidate/webapp/app.py:3313).

`n_am > 0` 내부에서 `n_clip == n_am`일 때만 존재하는 평균·std 키를 검사한다. 앞선 유한성·범위 검사가 유지돼 음수 std나 NaN을 새 분기로 우회할 수도 없다. 전체 클립이면 모든 저장 입자 값이 정확히 100이라는 생산 규약에 맞는다. 이번 수정은 피복 물성식·입자별 계산값을 바꾸지 않는다.

### 기존 반례를 같은 시험 코드로 재실행

이전 독립 `audit_r5.py`를 후보 사본에 **무변경** 실행했다. 저자의 재현 JSON을 답의 근거로 대신 읽은 것이 아니다.

| 기록 | 검증기 / 필수 단계 |
|---|---|
| 전체 클립인데 AM_P 평균 0% | **False / failed** |
| 전체 클립인데 AM_S std 40%p | **False / failed** |
| 부분 클립의 전체 평균을 75%→1%로 내림 | False / failed — 이전 하한 보존 |
| 실제 생산자의 0접촉 / 부분 / 전체 클립 | **3/3 허용**, 평균 0% / 75% / 100% |

추가 `audit_r6.py`에서 전체 클립 레코드의 AM_S 평균 **0·99·99.999%**와 std **0.001·40%p**를 각각 넣었다. **다섯 변이 모두 False / failed**였다. 평균 100%와 std 0%p의 원값은 True / done이다. 따라서 최소 요구뿐 아니라 생산 반올림 한 눈금(0.001%p) 밖의 이탈도 막는다. 합성 입력의 임의 소수 자릿수를 전부 생산 격자에 맞추는 별도 포맷 검사까지 요구하지는 않는다.

### 과잉차단 대조 — 없는 상·부분 클립·가중 평균

제출 selftest의 수동 레코드 변형만 믿지 않고, 새로운 합성 atoms/contacts에서 실제 `compute_case`를 다시 호출했다. 각 AM 반경 0.001 sim, AM 중심 간격 0.01 sim, 각 SE의 반경 0.001 sim, 해당 AM과의 중심거리 0.001 sim, scale=1000이다. 이는 CPU 판독기 시험 자료이며 DEM 평형 침대를 주장하지 않는다.

| 실제 생산자 대조 | n_AM / n_clip | AM_P 평균 | AM_S 평균·std | 전체 평균 | 필수 단계 |
|---|---:|---:|---:|---:|---|
| AM_P만, 전체 클립 | 1 / 1 | 100% | **키 없음** | 100% | done |
| AM_S만, 전체 클립 | 1 / 1 | **키 없음** | 100% · 0%p | 100% | done |
| P 1개·S 2개, 부분 클립 | 3 / 1 | 100% | 25% · **25%p** | **50%** | done |
| P 2개·S 1개, 전체 클립 | 3 / 3 | 100% | 100% · 0%p | 100% | done |
| AM_S만, 접촉 0 | 1 / 0 | **키 없음** | 0% · 0%p | 0% | done |

부분 클립 대조의 저장 입자 값은 P=[100], S=[50,0]이다. 따라서 전체 평균은 **50%**이며 두 상 평균의 단순 평균 **62.5%**와 다르다. 통과 결과는 “상별 단순 평균을 강제하지 않는다”와 “부분 클립에 새 std=0 조건을 걸지 않는다”를 동시에 보여 준다. 기존 공통 population std≤50%p 검사는 그대로이며 이를 없앴다는 뜻은 아니다. AM 0개의 SE-only 정상 대조도 옛 스키마 시험에서 통과했다.

### 새 상주 회귀가 실제로 수정 부위를 검사하는가

현재 selftest는 **216/216**, rc=0이다. 추가로 소스 파일은 그대로 두고 메모리에서 `_v2_ok_record` 하나만 이전 후보의 실제 함수로 교체한 뒤 **현재** `test_pipeline_provenance.main()`을 실행했다.

~~~text
수정된 검사기: 216/216 PASS
옛 검사기로 메모리 롤백: 214/216, rc=1
실패: T11s · T11t만
T11t의 옛 동작: 두 변이 모두 (True, 'done')
~~~

따라서 [T11s:929](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/candidate/webapp/test_pipeline_provenance.py:929)·[T11t:949](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/candidate/webapp/test_pipeline_provenance.py:949)는 이번 결함을 되돌리면 실제로 실패한다. 통과 숫자나 주석만 보고 닫은 것이 아니다.

재현: `python lhs_coverage_reverify5_20260930/evidence/audit_r5.py` 및 `python lhs_coverage_reverify5_20260930/evidence/audit_r6.py`.

[기존 반례 재실행](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/r5_results.json) · [추가 정상 대조·변이·롤백 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/r6_results.json) · [상주 회귀 롤백 전체 로그](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/resident_rollback.log).

한정: 변이 시험에서 계산 subprocess만 레코드 전달기로 대체했다. 필수 단계·검증기·summarize는 실제 함수다. 웹앱 HTTP 전체 경로나 실 재수확을 실행했다는 뜻은 아니다.

## 2. Q2 — PIN-TYPE은 사유 있는 미검증 반환으로 충분하다

위치: [hosts 스키마 검사:608](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/candidate/scripts/lhs_descriptor_harvest.py:608).

기존 `hosts:1`의 TypeError는 없어졌다. 추가 독립 시험에서는 다음 **10종**을 실제 `producer_pin()`과 `contact_area_check.producer_model` 양쪽에 넣었다.

~~~text
1 · "x" · false · {} · [1]
path 없는 원소 · 숫자 path · 숫자 sha · "zz" sha · 정상 원소+잘못된 원소 혼합
~~~

전부 **예외 없음 / claim=True / source_hash_verified_locally=None / installed_build_pinned=False / hosts 오류 사유 있음**이었다. 상위 claim의 필수 필드가 유효한 상태에서 선택적 로컬 대조 자료만 잘못된 것이므로 자기 신고를 보존하는 처리는 정합적이다. claim=True가 사실 인증이라는 뜻은 아니다.

정상·음성 대조도 유지된다.

| hosts 상태 | 로컬 SHA 대조 | 설치 인증 |
|---|---|---|
| None / 빈 목록, 유효한 절대 source_file | True | False |
| 유효 path + 상위 SHA 사용 / 원소별 SHA 사용 | True | False |
| 존재하는 파일의 SHA 불일치 | False | False |
| 잘못된 원소가 하나라도 있음 | **None + 사유** | False |

잘못된 hosts가 있으면 정상 절대 source_file이 함께 있어도 로컬 대조 전체를 None으로 돌린다. 이는 검증 범위를 보수적으로 낮추는 처리이며, 검증 성공으로 승격하는 처리가 아니다. 그 경우까지 부분 검증을 제공해야 이번 P3가 닫히는 것은 아니다.

날짜는 여전히 형식 검사뿐이다. `2026-99-99`가 claim=True인 사실은 유지됐으며 달력 유효성·실제 작성일 인증으로 표현하지 않는다. 설치 인증은 여전히 False이고 공개 식 가정하의 진단이라는 한정을 유지한다.

증거는 §1의 `r5_results.json` 및 `r6_results.json`의 pin 항목이다. 새 P1/P2 없음.

## 3. Q3 — DOMAIN은 비차단으로 남기는 데 동의한다

**이번 병합 전에 기하 계산 전 마스크를 요구하지 않는다.** 이전 판정의 경계를 유지한다.

~~~text
r1 = r2 = 1e160 sim, delta = 1e159 sim
_producer_error_bound → E=∞, uncertified=True
contact_area_check   → OverflowError: (34, 'Result too large')
~~~

[현재 호출 순서:643](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/candidate/scripts/lhs_descriptor_harvest.py:643)는 여전히 점 기하·enclosure를 먼저 계산한 뒤 E를 계산한다. 따라서 **모든 유한 입력이 예외 없이 미인증 기록으로 반환된다는 전역 주장은 금지**한다. 1e160 sim의 극단 입력이 실제 LHS 생산값이라는 증거는 없으며, 이것을 이번에 갑자기 P2나 새 HOLD로 올리지 않는다.

기존 1e-100 sim 언더플로 반례는 E=∞·미인증 1·시험 0이다. 수치 경로를 이번 패치가 바꾸지는 않았지만 이전 독립 시험도 다시 실행했다.

| 수치 회귀 | 이번 결과 |
|---|---:|
| 3D 좌표 산술 17,926점 / Decimal 90자리 | 오차>E 0, 최대 오차/E 0.21310838611670851 |
| 인증·비음수 토큰 8,170행 | 거짓 초과 0 |
| ±1% 보증 5,928행 | 양방향 누락 0, 분류 변화 0 |
| 기하 288,000점 | Decimal 80자리 / 실제 로컬 함수 이탈 0 / 0 |
| 출력 경계 1,980,567 치환값 | 누락 0 |

이는 **유한 합성 표본·공개 식의 산술 검산**이다. 설치 엔진 실행이나 모든 double에 대한 정형 증명이 아니다. [3D 검산](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/error_3d_results.json) · [기하 검산](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/geometry_results.json) · [출력 경계 검산](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/power_boundary_results.json).

## 4. 게이트 실행 결과 · 과장하지 않을 것

| 항목 | 독립 실행 결과 |
|---|---|
| 이전 R4 장부 변이 4개 | 4/4 거부·필수 단계 failed |
| 이전 스키마 정상 8종 / 변이 20종 | 8/8 허용 / 20/20 거부 |
| 정당한 blank의 rule=None·h_film 부재 | 허용 유지 |
| lens / plastic / coverage selftest | rc=0 / 0 / 0 |
| pipeline provenance | **216/216, rc=0** |
| harvest 원본 selftest | rc=1: 이전과 같은 CRLF fixture hash·τ median 1 ULP 두 실패 |
| harvest LF fixture 대조 | CRLF 실패 해소, τ 1 ULP만 남음 |
| batch 원본 selftest | Windows symlink WinError 1314 뒤 IndexError, rc=1 |
| batch byte-copy 보조 대조 | rc=0, 실제 배포 symlink 인증은 아님 |
| 옛 수확 값 36키×16호출 | 불일치 0 |

τ median은 baseline과 후보가 모두 **2.080532952769607**, selftest 기대값은 **2.0805329527696066**이다. 이를 이번 패치 회귀라고 하지 않는다. 반대로 제출 Linux 로그의 전수 녹색을 이 Windows에서 독립 재현했다고 쓰지도 않는다. **전체 check_all.sh는 이번에 독립 실행하지 않았다.**

[selftest 로그 요약](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/selftests.json) · [환경 대조·옛 키 비교](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/regression_results.json) · [옛 장부 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/r4_results.json) · [스키마 회귀](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify5_20260930/evidence/schema_results.json).

## 5. Q4 — 병합과 다음 수확

제안한 **0001→…→0019→게이트→트리 해시 고정→새 디렉터리 재수확** 순서에 동의한다. 운영 단계에서는 다음 경계를 유지한다.

1. 이번에 검증한 base+패치 결과와 실제 통합 결과의 소스 세대를 대조한다. 충돌 해결·추가 편집이 생기면 그 차이는 이번 검증 바이트에 포함되지 않는다.
2. 대상 실행 환경에서 전체 게이트를 실행하고 실제 종료 상태·로그를 남긴다. 이번 합성 Windows 검증을 운영 환경의 전체 게이트 대신 쓰지 않는다.
3. 트리/입력/실행 규약을 봉인하고 새 출력 디렉터리를 사용한다. 기존 결과를 덮어쓰거나 다른 세대와 혼합하지 않는다.
4. installed_build_pinned=False와 DOMAIN의 지원 범위 한정을 보존한다. 진단의 비교 가능 행 수를 설치 빌드 인증이나 실 데이터의 전역 정확성으로 승격하지 않는다.

앞 라운드에서 닫힌 항목을 다시 열지 않는다. 현재 남은 DOMAIN P3를 이유로 새로운 DEM이나 지원영역 확대를 이번 해제 조건에 추가하지 않는다. **이번 수정 범위에서 추가 차단 결함을 찾지 못했다.**

**GO**
