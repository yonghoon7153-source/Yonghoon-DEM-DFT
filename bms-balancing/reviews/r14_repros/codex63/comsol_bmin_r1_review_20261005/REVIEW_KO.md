# COMSOL B-min R1 준비 재검토

2026-10-05 · 정적 검토만 · 게이트 차수 밖

판정: **LOCAL_CORRECTION_REQUIRED — P2 잔여 1건.** BMIN-N1의 종료 축 분리는 이 준비 검토 범위에서 수용한다. BMIN-N2는 원래의 누락/구간 밖 문제를 막았지만, 한 줄 안의 중복·잔여 문자열을 허용하는 경계가 남는다. C1의 범위 축소는 수용한다. 기능 검증 PASS나 native 실행 승인이 아니다.

## 고정 대상과 확인 범위

- 커밋: `741dde19b5d07be1872e8bdcedaa90611cbf5b71`.
- 요청문 blob: `f5fa9e2e1d8bbe3d8bd2eb146903c4ab2669b5fb`.
- CODE_MANIFEST: 1,050 bytes / SHA-256 `9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb`.
- manifest의 생산 파일 5개 크기/SHA를 독립 대조했다. Java·entry는 v1과 바이트 동일하다. 부모·consumer의 선언 변경을 검토자 자체 텍스트 처리로 역치환하면 v1 전체 바이트와 같다. CONTRACT의 차이는 DOF 상태 문구 하나, COMMAND_MAP·승인 필드 명세의 차이는 manifest SHA뿐이다.
- 이전 리뷰에서 확보한 v1 파일 28개의 Git blob이 현 고정 커밋에서도 같다. 제출자의 “29개 전체”와 이 28개 표본을 혼동하지 않는다. 이전 리뷰의 NORMAL480→v1 검토를 이번에 전부 재실행했다고 주장하지 않는다.
- 후보 및 제출자의 build/audit 프로그램은 import·구문 해석·컴파일·실행하지 않았다. COMSOL/JVM/native/기능 시험 0회. 검토자 자체 JSON·해시·문자열·ZIP 로그 읽기만 수행했다. 제출자의 42/42는 제출자 정적 검사 기록이며 기능 사례 수가 아니다.

## Q1 — BMIN-N1: 준비 수준 수용

`GNativeAxis`는 native child 반환의 타입/rc/오류, 결과 run/manifest, 구조화된 종료 근거와 consumer 라벨의 일치를 확인한다. `GFields`는 비교·구성·분석·전달 판정이 미완이어도 이 종료 축을 보존하고 다른 두 축은 INVALID/INCONCLUSIVE로 둔다. 정상 종료+구성 실패, 분석/전달 예산 초과, 보호 중단의 분리 방향이 이전 지적을 해결한다. [부모 135–186행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/741dde19b5d07be1872e8bdcedaa90611cbf5b71/bms-balancing/comsol_candidates/bmin_particle640_r1_20261005/candidate/PARENT_COMMAND.ps1#L135)

여기서 “독립”은 **같은 consumer의 구조화된 종료 증거를 부모가 별도 조건으로 소비한다**는 뜻이다. 원시 native 로그를 다른 관측자로 독립 측정했다는 뜻은 아니다. 원시 로그·저장 시각의 상세 대조는 기존 `native_stop`이 담당한다.

entry가 사후 보존/정책/정리 실패에도 rc1을 반환하여 부모가 NOT_ESTABLISHED/NATIVE_CHILD_RC로 남기는 한계는 보수적 미확정으로 수용한다. 이 준비 건에서 entry 제어를 다시 열 필요는 없다. 이를 “solver 실패가 확인됨”으로 표현하거나 원래 오류를 지우면 안 된다. [entry 126–145행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/741dde19b5d07be1872e8bdcedaa90611cbf5b71/bms-balancing/comsol_candidates/bmin_particle640_r1_20261005/candidate/src/candidate_entry.py#L126)

이는 정적 수용이며 실제 PowerShell 검증은 아직 별도 단계다. 구조화된 종료 근거 자체가 없거나 읽히지 않는 경우까지 정상 종료를 보존하라고 요구하지 않는다.

## Q2 — BMIN-N2: 원래 결함 개선 확인, P2 잔여

### BMIN-R1-N1 / P2 — 한 줄 안의 중복 DOF도 명확한 단일 관측으로 읽는다

대상: `candidate/src/diagnostic_consumer.py:322–325`.

`mentions`는 문구를 포함한 **줄** 수만 센다. 다음 `re.search`는 그 줄 중 일부분만 맞으면 첫 관측을 반환한다. 따라서 아래 한 줄은 두 서로 다른 DOF를 갖는데도 `len(mentions)==1`이고 첫 값 79485를 채택한다.

```text
Number of degrees of freedom solved for: 79485 (plus 12 internal DOFs). Number of degrees of freedom solved for: 156925 (plus 12 internal DOFs).
```

정상 문구 뒤에 `Number of degrees of freedom solved for: ???`가 붙은 한 줄도 첫 정상 조각만 읽는다. 이것은 “정확히 하나·형식 일치·모호하면 I-3 미완”이라는 이번 보완 계약과 맞지 않는다. [consumer 320–325행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/741dde19b5d07be1872e8bdcedaa90611cbf5b71/bms-balancing/comsol_candidates/bmin_particle640_r1_20261005/candidate/src/diagnostic_consumer.py#L320)

검토자는 후보 함수를 실행하지 않았다. 위 결론은 소스의 분기 추적과 검토자 소유의 작은 문자열 모형 대조다(`INDEPENDENT_STATIC_AUDIT.json/static_string_cases`). 실제 COMSOL이 이런 로그를 생성했다고 주장하지 않는다. 로그 손상/모호 입력의 수용 경계에 대한 지적이다.

최소 보완: 단일 후보 줄의 앞뒤 공백을 허용하되 **전체 줄**을 정해진 DOF 형식과 대조하거나 동등하게 모든 잔여 내용을 거부한다. 첫 부분 문자열만 선택하지 않는다. 같은 줄의 정상 두 문구, 정상+불완전 문구를 이유를 고정한 음성 사례로 추가한다. 예상 156925+12와 다르다는 이유로 거부하는 변경은 금지한다.

### NORMAL480 실제 원 로그 대조

기존 ZIP을 다시 읽어 SHA `e991ab4c918f6576b18d6225a86ed41759ab6ee726dd6543b9a9158e581cbc30`, 크기 420,748,594 bytes를 확인했다. `run/batch.log`는 886,975 bytes / SHA `805e649493f6d793e0b780a3899c40132d2e15011742de047fecae16711fcfa8`.

| 위치 | 원문 관측 | 해석 |
|---|---|---|
| 86행 | solved 1202 / internal 12 | Stationary 초기화, transient 근거로 사용 불가 |
| 131행 | solved 79485 / internal 12 | 단일 Time-Dependent Solver 구간 안의 유일한 DOF 줄 |

해당 시간 의존 구간에 다른 `Number of degrees of freedom` 줄은 없다. 따라서 원 NORMAL480 로그는 새 “단일 transient 관측” 규칙의 양성 자료로 사용할 수 있다. 단, 이것은 particle320 기준 로그이지 새 particle640의 실측 DOF가 아니다. 현재 R1은 구간 내 관측 없음·초기화 줄만 남음·서로 다른 두 줄·solved=0을 정적으로 거부하는 구조다.

## Q3 — C1 수용, 비차단 문구 정정

PS01-03/04를 한도 부근/라벨 일치 검사로 좁힌 것은 적절하다. PS01-16의 목적을 “긴 소수의 부모/consumer 불일치는 INCOMPLETE로 닫는다”로 둔 것도 적절하며 실제 목표 엔진에서 확인해야 한다. 임의 정밀도의 십진 비교를 보증하는 시험으로 표현하지 않는다.

문자열 `0.001000000000000000000000000001`은 **소수점 아래 30자리, 유효숫자 28자리**다. 검증안과 변경 경계 문서의 “31 significant digits”는 정정한다. PS01-16은 정확한 등호 사례가 아니므로 `v2_section_8_required_items/value exactly equal to a limit` 목록에서도 빼고 정밀도 불일치 항목으로 분류한다. 정확 등호 대조는 기존 PY01-02/PS01-04가 담당한다. 새 생산 코드 변경 사유는 아니다.

## Q4 — 한정 검증안의 수용 조건

9군·54개 고유 case ID의 합은 **Python 35 + Java helper 2 + PowerShell 17 = 54**다. 예산 합도 **1530초**다. 일부 ID는 복수 입력을 포함하므로 “54 ID”와 엔진 호출/하위 입력 수를 혼동하지 않는다. 현재 세션·횟수·예산은 제안이지 승인 또는 충분성 실측이 아니다.

핵심 양성/음성 경로는 마련돼 있다. 다만 시작 전 다음을 한정 검증안에 명시한다.

1. 위 동일 행 DOF 중복/정상+불완전 꼬리 거부를 추가하고, 정상 단일 행·다른 유효값 수용은 유지한다.
2. consumer의 `TRANSIENT_DOF_READBACK_VALUE`도 직접 도달하도록 solved=0을 넣는다. PS01-17의 부모 측 0 거부는 consumer 경로의 대체가 아니다.
3. 새 GNativeAxis의 native 반환 누락/오류, 다른 run 또는 manifest, 모양은 있지만 모순된 종료 근거를 이유별로 확인하도록 기존 음성 사례를 보강한다. 현재 PS01-12~15만으로 여섯 실패 원인이 모두 시험됐다고 부르지 않는다. 이는 검증 커버리지 보강이며 새로운 생산 제어기 요구가 아니다.
4. 실제 봉인된 함수·harness·엔진·각 입력/기대 이유·최종 고유 ID/하위 사례 수를 실행 전에 고정한다. 추가 사례가 생기면 총수와 예산안을 갱신하고 사용자에게 제시한다. 별도 승인 없이 횟수나 예산을 늘리지 않는다.

이 검토는 제한 suite를 실행하지 않았고 합격을 예견하지 않는다. 기존 전체 시험·NORMAL480·rtol30을 다시 열지 않는다.

## 다음 제출물과 중지선

국소 수정 대상은 DOF 한 줄 파싱, 해당 검증안, C1 문구/분류, 변경표·manifest·참조 결속뿐이다. Java·entry·물리·수치 허용치·시간/좌표·기준 파일은 유지한다. 새 source seal과 v1/R1 대비 최소 diff를 제출한 뒤 멈춘다.

그 후 변경부 검증은 사용자 별도 승인, 검증 수용 뒤 native150초 최대1회는 다시 별도 승인이다. 이번 회신은 구현·시험·native 권한을 새로 부여하지 않는다. approved=false / usable=false, 전체·정상 gate INCOMPLETE, 내부 실효 정책 UNVERIFIED, 960초·유한 sigma·다른 공간 축 미승인을 유지한다.

회신은 문서 작성 기준에 따라 제출자 보고, 검토자 데이터 관측, 정적 추론, 미실행 기능 검증을 분리했다. 원본 후보·기록·설정은 변경하지 않았다.
