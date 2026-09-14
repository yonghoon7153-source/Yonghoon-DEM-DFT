# 5초 메시 축 분리 시험 독립 감사

2026-09-13 KST. 기존 소스, 제출 사본, COMSOL 네이티브 로그, 모델 메타데이터, 디코딩 CSV 및 보존 manifest를 읽어 검증했다. 이 감사에서 COMSOL 실행·재제출, 모델·설정 변경은 하지 않았다.

**세 작업 모두 실제 5초 해석과 14개 CSV 출력을 완료했다.** 세 작업에서 사전 지정 공통 저장 시각 187개가 각각 유일하게 존재한다. 소스 차이는 승인된 메시 축, 동일한 조밀 시간 목록 및 증거 출력에 한정된다. 입자 방사형 메시 세분화 비교는 전압 차이 한도를 초과하므로 이번 결과를 전체 수렴 완료로 판정할 수 없다.

## 실제 실행과 메시

| 모델 / 작업 ID | 물리 메시 API: 요소 / 정점 | 영역 1 / 2 / 3 요소 | native batch의 세 메시 요소 수 | 과도 해석 DOF | 전체 저장 시각 |
|---|---:|---:|---|---:|---:|
| Axes300R40 / `f211901885774793ab39e89ebee0144f` | 300 / 301 | 120 / 60 / 120 | 300 / 40 / 40 | 11,725 | 215 |
| Axes300R80 / `a4d58eb7f97c48cc9109657d4a8f0ba3` | 300 / 301 | 120 / 60 / 120 | 300 / 80 / 80 | 21,405 | 235 |
| Axes600R40 / `7e78bebd745e437da5bb8fe77a01ef84` | 600 / 601 | 240 / 120 / 240 | 600 / 40 / 40 | 23,365 | 215 |

모두 worker `completed`, compile exit 0, batch exit 0, `EXPORT_OK`이며 마지막 저장 시각은 5 s이다. 각 DOF 로그에는 별도 내부 DOF 12개도 표시된다. 물리 메시 수는 `mesh1.getNumElem("edg")`, `getNumVertex()` 및 요소별 영역 readback의 직접 증거이다. 방사형 메시 수는 두 Particle Intercalation의 `Nel` 설정, native batch의 추가 메시 수 및 저장 모델 XML의 두 `BUILT` 방사형 메시 좌표 수(각각 41 / 81 / 41개)가 일치한다. 방사형 수를 `mesh1`의 직접 API 반환값으로 주장하지 않는다. XML의 explicit 좌표 모드에서 비활성 기본값 `numelem=10`은 실제 요소 수가 아니다.

## 소스와 물리 입력 보존

`work/mesh_axes/independent_source_review.py`의 역변환 비교에서 각 새 소스의 명시된 이름·메시·187점 tlist·증거 출력 helper만 제거하면 이전 `PreflightMeshFine5s.java` 본문 전체와 일치한다. 이전 소스 SHA-256은 `dbcb95c47abad474485fcc281fe71f30c5a2e48204c2c65614d780c203724adf`이다.

- 세 새 소스는 메시와 식별 이름을 정규화하면 동일하다. 50개 물리 파라미터, 초기 재고, 입자 반경, OCP/entropy 표 값과 함수, 표면 범위 guard, 솔버 설정은 동일하다.
- 전류는 기존 0.1C, separator 전도도는 `1e-20 S/m`, 시간 구간은 0–5 s이다. 각 소스의 solver 실행은 한 번이며 장시간 해석·전도도 sweep이 추가되지 않았다.
- OCP/entropy 네 함수의 `extrap=none`이 유지된다. 새 코드는 런타임 설정·공간 profile 출력 및 생성 Java 저장을 추가한다. 명시적인 외부 입력 읽기, 네트워크, 외부 프로그램 실행 또는 관리자 동작은 없다.
- 현재 Java, 실제 작업 폴더에 제출된 Java 사본 및 `source_configs.json`의 SHA-256이 세 작업 모두 일치한다.

| 모델 | 소스 SHA-256 | 실제 저장 MPH SHA-256 |
|---|---|---|
| Axes300R40 | `b4298feb95a6dd2306967fad44c55ab668450633c0a0ec7760681c3b76047e44` | `8be66085dc14475d768e203e459b7286e974b29b99431db2c1663f92580abe69` |
| Axes300R80 | `f2745f4a157ab5102ff69a980da177060d2323722ab0f79079e3c531212dd2f2` | `6f9c498f952832d2921c8427230c3dfe8c2201f6659bbb152fc05abf8daa65de` |
| Axes600R40 | `8ad0b8b31f47896bc8dbc46e80cc61373278edd8efd8ee21c8ed56312a5d1448` | `e3e87359e14cc278076ed503925ad97d6cc4107a21aae5aa295f9cec0dc50a9e` |

## 실제 시간 설정과 스케일

세 모델의 핵심 Time 설정 및 과도 해석 필드 스케일 readback은 동일하다. Time/Variables와 그 하위 노드를 합해 모델당 1,143개 속성이 로그에 기록되었고 읽기 오류는 0개이다. 1,143개 전체를 Time 최상위 노드만의 속성 수로 해석하면 안 된다.

| 항목 | 공통 readback |
|---|---|
| 상대 허용오차 | `rtol=1e-6` |
| BDF 초기 step | 활성화, `1e-5 s` |
| BDF 최대 step 설정 | `const`, `0.1 s` |
| 요청 시각 처리 | `tstepsbdf=strict`, `tout=tsteps`, `tstepsstore=1` |
| 일관 초기화 | `consistent=bweuler` |
| 절대 허용오차 방식 | `atolglobalmethod=scaled`, `atolglobalvaluemethod=factor`, factor `0.1`; 각 필드 global/factor |
| 과도 필드 수동 스케일 | electrolyte concentration `1000`, 양 전극 solid concentration `10000`, 두 전위 `1` |

`atolglobal=0.001`과 각 필드 `atol=0.001`도 저장되어 있으나 현재 선택은 factor 방식이다. 이를 모든 물리량에 실제 적용된 단일 절대 허용오차 `0.001`로 기술하지 않는다. native batch의 `Scales for dependent variables`가 위 필드 스케일을 별도로 확인한다.

**공통 설정은 동일한 내부 시간 이력을 뜻하지 않는다.** native accepted-step 로그에서 관측한 최대 step은 모두 `0.05 s`이며, 전압 차이가 최대인 `t=0.04 s`의 실제 step은 300/40에서 `0.005 s`, 300/80에서 `0.002 s`, 600/40에서 `0.005 s`이다. 따라서 방사형 메시 민감도에는 동일한 제어 하에서 달라진 적응형 내부 시간 이력의 영향도 포함될 수 있다. 이번 시험은 시간 간격 수렴 시험이 아니다.

## 저장 시각과 전극별 profile

분석은 **사전 지정 공통 저장 시각 187개**만 정확히 선택한다(0–1 s에는 107개). CSV 시간 문자열을 Decimal로 읽어 존재·유일성을 검증했다. 실제 저장 시각 전체의 교집합은 방사형 비교 200개, 물리 메시 비교 215개이므로 “전체 공통 시각은 187개”라는 표현은 부정확하다. 세 새 모델의 scalar CSV는 0–5 s 범위에서 엄격히 증가하고 유한하다.

`axes_profile_N.csv`, `axes_profile_P.csv`는 `time_s, coordinate_m, x_surface, x_particle_average, Eeq_V, etaMid_V, phil_V, domain_id`의 8열이다. 매 저장 시각에 전극마다 241개 좌표가 있다. 음극은 domain 1, 양극은 domain 3으로 분리되며 두 전극을 가로질러 보간하지 않는다. 전체 profile 행 수는 전극별 51,815 / 56,635 / 51,815개이다. 모든 값이 유한하고 각 profile 시각은 scalar 저장 시각과 정확히 일치한다. 좌표의 계약 값 대비 최대 오차는 `3e-20 m` 이하이다(독립 float 격자 검산은 `1.36e-20 m` 이하, 분석 JSON의 Decimal 검산은 `3e-20 m` 이하).

공간 값은 COMSOL `Interp`가 각 전극의 고정 공통 물리 좌표에서 계산한 **유한요소 공간 보간 값**이다. `timeinterp=off`, `ext=0`, `recover=off`, geometry unit `m`, 1D 및 domain 선택을 확인했다. 결과 비교에는 외부 공간 보간이나 시간 보간, 가장 가까운 시각 선택을 사용하지 않았다. 전역·집전체 native 수치와 이 공간 profile의 성격을 구분해야 한다.

## 보호 조건과 완료 판정의 범위

현재 런타임 StopCondition은 전극 표면 DOC의 표 범위 및 물리적 0–1 범위를 감시한다. OCP/entropy 공통 허용 범위는 음극 `[0, 0.98]`, 양극 `[0.2228930343076256, 0.983245033354389]`이며 Min/Max Lagrange 5 샘플링을 사용한다. 모든 저장 시각의 표면 guard는 0이다. 이 증거는 연속 공간 전체의 극값 증명이나 Newton trial 단계의 범위 이탈 사전 차단을 뜻하지 않는다. StopCondition은 내부 step 이후 평가되며, 외삽 금지 정책은 별도 보호다.

**전해질 농도 양수 확인은 POSTPROCESSING_ONLY이다.** 이를 실시간 electrolyte StopCondition으로 주장하지 않는다. 저장 시각에서 측정한 최소 전해질 농도는 각각 `1194.4372376491106`, `1194.4372193572083`, `1194.4372374390439 mol/m³`로 양수이다. 유한 출력 확인 역시 solve 후 검사다.

## 두 축 비교의 제한된 결론

독립적으로 원시 저장 시각, 분석 코드의 정확 시각 선택, 결과 JSON/CSV를 대조했다. 차이의 부호는 세분화 모델 − 300/40이다. 한도는 전압 `1 mV`, pointwise 표면 조성 `1e-4`이다.

| 비교 | 구간 | 최대 절대 전압 차이 | 최대 pointwise 표면 조성 차이 | 제한된 판정 |
|---|---|---|---|---|
| 300/40 → 300/80 | 0–1 s, 0–5 s | `2.505310864 mV`, 0.04 s | `4.182398438e-5`, 음극 52 µm, 0.04 s | 전압 한도 초과 |
| 300/40 → 600/40 | 0–1 s | `1.08668e-11 V`, 0.001 s | `2.2088256e-9`, 양극 121 µm, 1 s | 지정 샘플에서 두 한도 충족 |
| 300/40 → 600/40 | 0–5 s | `1.08668e-11 V`, 0.001 s | `5.2286938e-9`, 양극 121 µm, 5 s | 지정 샘플에서 두 한도 충족 |

방사형 비교의 전압 최대 시각 0.04 s에서 동시 분해는 ΔEeq `+2.550630094 mV`, Δη `−0.04577689555 mV`, ΔφL `+0.0004576654234 mV`이다. 모든 비교 행의 분해 잔차 절댓값은 `7.35e-16 V` 이하이다. 내부 JSON의 `particle_radius`는 물리적 입자 반경 변경이 아니라 **입자 방사형 메시 세분화**로 읽어야 한다.

이 결과는 지정 시각과 전극별 241좌표에서의 민감도 결과다. 연속 시공간 수렴, `1e-11 V` 절대 정확도, 전체 12시간 프로토콜 또는 전도도 sweep의 검증·승인을 뜻하지 않는다.

## 기존 증거 보존

`preserved_before.json`의 기존 파일 **333개, 191,105,291 bytes**를 SHA-256과 크기로 다시 검사하여 모두 일치했다. 보존 manifest 자체 SHA-256도 `2326bcbae80657bfb6dccce56f1272366af8fe8f9bbbc71dd57daa4c905748bb`로 동일하다. 독립 최종 검사 시각은 2026-09-13 21:51:40–21:51:42 KST이다. 명시적으로 갱신하도록 허용된 NEXT_RUN_PLAN의 이전 사본은 별도 snapshot으로 보존되어 있다.

기존 범위 경계 fixture 작업 `08e0fc5d41e147678f3940e98100ec12`는 여전히 native `failed`, `INCOMPLETE_RANGE_STOP`, `physical_checks_pass=false`이다. 마지막 부분 시각 약 `0.00986002 s`, 부분 MPH·CSV·로그 등 관련 manifest 파일 13개(6,779,328 bytes)도 그대로다. 그 작업의 native fatal banner/비유한 출력과 이번 세 완료 작업을 혼합하거나 기존 실패를 성공으로 바꾸지 않았다.

## 재현 근거

- `work/mesh_axes/independent_source_review.py`: 이전 소스와 새 소스의 전체 비교.
- `work/mesh_axes/independent_native_audit.py`, `independent_native_snapshot.json`: 세 작업의 입력/MPH 해시, 상태·로그·설정·187개 시각·profile 행 및 유한성 독립 검사.
- `outputs/mesh_axes/native_evidence.json`, 각 `*_native_steps.csv`, `preservation_verified.json`: root가 별도 수집한 증거와 대조 완료.
- `outputs/mesh_axes/results/analysis.json` 및 비교 CSV: 지정 시각의 전압 분해와 전극별 pointwise 비교.
- 감사 당시 `source_configs.json` SHA-256: `f90eea31380c6a65ed6c8a0e72c7d4f59997f811aa3ad423abdb7d53a37ea5e5`; `jobs.json`: `6dc668034feea90f4dbd4c95c3a7cda14ead30edf54c1d5c5b7b9ee0c35de760`; `comparison_contract.json`: `4e57a8be54a263aa7ed915ae5de061e937e066267bedd8c4445045190655f85d`.
