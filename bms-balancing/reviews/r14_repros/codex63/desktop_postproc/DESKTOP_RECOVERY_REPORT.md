# Desktop 저장 해 후처리 복구 — 부분 회수 및 종료 기록

2026-09-15. 이번 결과는 **필수 수치 부분 회수 / 정상 전체 gate 미완**이다.
새 solve·API/batch 제출·실행용 Java 생성·의도적 보안 설정 변경은 수행하지 않았다.
Desktop 조작은 사용자가 수행했고, 현지 Codex는 화면·사용자 보고·생성 CSV·OS 파일을 확인했다.

## 회수 결과

- 전해질 자동/명시 단위 CSV: 각각 실제 987개 시각, 0–5초. 두 시간 열 및 모든 숫자가 Decimal 비교에서 동일하다.
- 정의한 coupling 평가점의 전체 최소는 **1194.4372136345671 mol/m³**, 5초, domain 1. 전체 최소와 세 domain 최소의 최솟값이 모든 행에서 일치한다.
- 임계값=0, 전해질 중단 논리값=0. OCP·고체 표면 두 보호식도 987개 저장 시각에서 모두 0이다. CSV 헤더의 식을 원래 식과 직접 대조했다.
- 경계 1/4 CSV는 각각 987행이며 13개 식·단위 및 Point: 1/4 식별이 원본과 맞는다. Eeq 직접 구성식 및 전압 성분 항등식의 기존 허용차를 충족한다.
- **전압 부분**의 요청187/정확 공통987 × 네 창, 총 8개 비교가 1mV 기준 이내다. 시간 보간·최근접 대체를 하지 않았다.
- 241좌표 pointwise 표면 조성 비교와 Li 수지/나머지 필수 출력 회수는 미완이다. 경계 표면 값으로 공간 전체 비교를 대신하지 않았다.

| 시각 집합 | 창(s) | 실제 개수 | 최대 전압 차(mV) | 최대 시각(s) |
|---|---:|---:|---:|---:|
| requested187 | 0.1–1 | 91 | 3.7000E-12 | 0.14 |
| requested187 | 1–5 | 81 | 3.6000E-12 | 3.9 |
| requested187 | 0–1 | 107 | 3.7000E-12 | 0.14 |
| requested187 | 0–5 | 187 | 3.7000E-12 | 0.14 |
| exact_common_stored | 0.1–1 | 99 | 3.7000E-12 | 0.14 |
| exact_common_stored | 1–5 | 82 | 3.6000E-12 | 3.9 |
| exact_common_stored | 0–1 | 906 | 4.8000E-12 | 0.052750000000000005 |
| exact_common_stored | 0–5 | 987 | 4.8000E-12 | 0.052750000000000005 |

동일 시각의 signed Eeq·etaMid·phil 차이 및 성분 합산 잔차는 `analysis/boundary_voltage_comparison.json`에 있다.
여기서 비교값은 소수 CSV의 재계산 결과이며 내부 double 비트 동일성·물성 정확도·참값 오차를 뜻하지 않는다.
0.1–1초와 1–5초의 양 끝은 포함한다. 서로 다른 창의 개수에 공유 경계가 포함되므로 단순 합하지 않는다.

## 공간 평가를 멈춘 이유

`GUI_N_sol1`의 domain 1 선택과 propagation off, Cut Point의 Snapping=None, All 저장 시각, 8개 식/단위,
Summation/Normalization/Transformation=None까지 화면으로 확인했다. 기준 axes_generated.java의 SHA를 이전 manifest와 대조한 후
N/P 각각 241개 **원래 좌표 리터럴**을 재생성 없이 텍스트로 추출했다. 이 파일의 GUI 소비는 아직 검증되지 않았다.

그러나 원본 API Interp의 ext=0·recover=off·coorderr=on과 현재 Cut Point + EvalPoint의 동등한 동작을 확인하지 못했다.
공식 Interp 문서는 Cut Point/EvalPoint에서 제공되지 않는 추가 고급 속성이 있음을 명시한다.
이것은 **동등성 증거 부족**이며, 실제 공간 수치 오류나 COMSOL 6.3에서 공간 평가가 불가능하다는 증거가 아니다.
ext는 메시 밖 평가 거리이며 OCP 함수 외삽 설정과 구분한다.
사용자 승인문의 '표준 UI에서 동등한 설정을 확인할 수 없다면 그 지점에서 미완으로 중지'에 따라
profile Evaluate/Export는 각각 0회, 뒤의 Li 회수도 시작하지 않았다. 이 확인을 UI 준비 전에 마치지 못해 불필요한 준비 조작이 발생했다.

공식 근거:
- https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_results.52.075.html
- https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_results.52.039.html
- https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_results.52.052.html
- https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_results.37.082.html

## 종료·보존과 증거 범위

사용자가 모델을 닫았다고 보고했다. 종료 후 comsol/comsolbatch/comsolmethodexec 이름의 프로세스 조회 결과는 비어 있었다.
입력 복사본 **1,266,539,803 bytes**, SHA-256 **7fefc0cfdf6910d40f2fec8021d6efbc72250c4e8ff79ba4a9442233bc581658**은 전후 동일하고 mtime도 동일하다.
기존 기록15개와 기준 CSV14개의 현재 바이트를 사전 식별과 대조해 모두 동일함을 현지에서 확인했다. job 디렉터리 목록도 전후 같다.
원래 NEXT_RUN_PLAN은 수정하지 않았다. 이번 다음 계획은 이 폴더의 별도 문서다.

Preferences 파일은 22,252 bytes로 크기는 같지만 SHA가 바뀌었다. 보안 관련16개 key/value는 모두 동일하다.
전후 전체 preferences 원문을 보관하지 않았으므로 다른 키의 구체적 변화 원인은 확정하지 않는다. 임의 복원하지 않았다.
외부 해시 일치는 입력 파일 보존이며 전체 메모리 해 불변을 증명하지 않는다. OS 스냅샷은 전체 과정의 실행 부재를 독립 증명하지 않는다.

관측된 새 평가5건/CSV 내보내기5건: 자동 단위, 명시 단위, 두 기존 guard, 경계1, 경계4.
이는 사용자 보고·다섯 표 CSV·일부 설정 스크린샷의 연결로 집계했으며 연속 UI 감사는 아니다.
자동 단위/명시 단위 export의 Full 설정은 직접 화면 확인했다. guard/경계 export는 Full 지시와 사용자 완료 보고가 있으며
동일 항목의 export 설정 화면은 별도로 회수하지 않았다. 실제 CSV의 자릿수와 헤더는 원본 그대로 보존했다.
이번에 추가한 Results 설정은 MPH에 저장하지 않아 재개방 시 남지 않으며, 스크린샷·계약·입력좌표·CSV가 설정/결과 기록이다.

기존 failed job 56ef13bee5a448c5a029b02656ebf6bb와 API 복구 failed 28f40815e3a3410aab411ec93cd36fe1의 상태는 바꾸지 않았다.
loadCopy는 여전히 미시험이다. 원래 API 분석기의 completed marker·1,143개 속성·Java 전후검사·argmin 근거를 GUI 결과로 대체하지 않았다.
정상 guard 전체 PASS·발동1198 성공·연속 시공간 양수성은 판정하지 않는다.

## 제공 자료

| 새 원시 CSV | bytes | SHA-256 |
|---|---:|---|
| boundary1.csv | 231624 | `c3d1e0c8c7dd92e5920659fb9cd6832dcb409e49e88c9b341b1c81ce46a52e8a` |
| boundary4.csv | 244362 | `3893644b7776065bdc496452ea52429b8de4af1d46d31e02f2ce61c9f091dda7` |
| electrolyte_auto_units.csv | 106333 | `8288a94a77278cd8150343280407611c9cd6a2273d97993fd2b75c9e72b95114` |
| electrolyte_explicit_units.csv | 106333 | `0da3fb0b28a6683e5c57a085613bc98a5df9f1ceea36d351f94708653430e0e2` |
| ocp_surface_guards.csv | 32596 | `d65693f21385eb63090352f46fbc87785cf76d833a776363d22e473fefea0e82` |

이번 ZIP에는 새 자료와 명시적으로 복사한 기존 소스/경계CSV/일부 실패 기록만 들어 있다. 원본/복사본 MPH, 전체 역사333,
현지 전체 파일 또는 기준 profile CSV14개 전체를 포함하지 않는다. `REUSED_EVIDENCE_INDEX.json`과 manifest가 실제 범위를 정한다.
기존 파일 전후 보존 중 ZIP에 없는 바이트에 대한 판단은 현지 기록이며 수신 측의 직접 재검증 가능 범위와 구분한다.
분석 스크립트는 작성 당시 현지 BASELINE_CONTRACT의 절대 경로를 사용한다. 다른 PC에서 원형 그대로 실행 가능한 묶음으로 주장하지 않는다.
수신자는 포함된 원시 CSV와 `reused_evidence`의 기준 경계 CSV/소스로 독립 재계산할 수 있다.
Python __pycache__와 전달 ZIP/영수증 자체는 payload manifest에서 제외한다.

**전체 수렴 미완·장시간 운전 보류, OCP 외삽 금지, 기존 failed/INCOMPLETE_RANGE_STOP 보존,
TIME_CAPS raw ZIP 차이 원인 미확인을 유지한다. 이번 후처리 작업은 여기서 종료한다.**
