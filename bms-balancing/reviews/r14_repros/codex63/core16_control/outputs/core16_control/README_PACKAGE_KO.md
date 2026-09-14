# COMSOL 6.3 — 원래 H0125 16코어 통제 계산 1회

새 Caps300R320H0125C16 / job 5d1a87652ed54e6a945d4f2af4aeda70 한 건만 실행했다. 원래 cap `if(t<0.1[s],0.000125[s],0.1[s])`, 물리 300(120/60/120)·입자 320/320, t=0 초기화와 물리시간 5초를 유지했다. 실제 16코어·벽시계 대기한도 1800초다. 기존 H0125 2코어와 A 16코어는 재실행하지 않았다.

- [결과 보고서](CONTROL16_RESULTS_KO.md), [16개 비교창 분석](results/analysis.json), [독립 원시 재검산](results/independent_review.md)
- [실제 step/설정](native_steps_summary.json), [구간별 분포 비교](accepted_interval_comparison.json), [최종 검사](final_checks.json)
- [소스 감사](INDEPENDENT_SOURCE_REVIEW.md), [native 감사](INDEPENDENT_NATIVE_AUDIT.md), [보존 범위](PROVENANCE_LEVELS.json)
- [수신 확인과 기존 A 판정 정정](RECEIPT_AND_CORRECTION_KO.md), [수정 계획](../NEXT_RUN_PLAN.md), [변경 전 계획](NEXT_RUN_PLAN_before_core16_control.md)
- [비교 그림 PNG](figures/core16_control_comparison.png), [PDF](figures/core16_control_comparison.pdf)

## 두 비교의 수용 범위

1. 기존 H0125 2코어 → 새 H0125 16코어: 원래 시간조건에서 두 코어 설정을 사용한 실행의 표본 차이.
2. 새 H0125 16코어 → 기존 A 16코어: 동일 코어 설정에서 후기 시간상한 변경의 표본 차이.

각 쌍은 지정 187시각·전극별 241좌표와 정확 공통 저장 시각을 별도로 비교했다. 네 창 [.1,1], [1,5], [0,1], [0,5]초의 총 16개 판정은 1mV·표면 x 1e-4 기준 이내다. 공통 저장 시각 수는 첫 쌍 987, 둘째 쌍 986이다. 시간 보간·근접 시각 대체를 하지 않았다.

첫 쌍의 최대 차이는 내보낸 수치의 극소 차이이며 물리 측정 정밀도나 참값 오차를 뜻하지 않는다. 세 해 공통 986시각에서 같은 시각·위치의 signed 항등식은 산술 일관성 검사다. 서로 다른 시각의 최대값을 더하거나 상쇄가 없다고 가정하지 않았다. 초기의 작은 차이로 후기 코어 영향을 0으로 처리하지 않았으며 일반적인 core×cap 상호작용 부재를 입증하지 않는다. 1–5초 차이에는 앞 구간의 상태 차이가 이어진다.

기존 A16 대 H0125 2코어의 정확한 수용 문구는 **“후기 시간상한·코어 수 변경을 포함한 두 실행의 지정 표본 차이가 기준 이내”**다. 기존 원시 결과·ZIP·생성 영수증은 보존하고 별도 정정 기록을 추가했다.

## 자료와 재현

세 해의 원시 CSV·정본/staged Java·request/status·전체 로그·실제 설정/step과 새 통제 MPH를 포함한다. 기존 두 MPH와 이전 A 원본 ZIP은 이미 전달된 자료여서 이 포장에 중복 포함하지 않았다. 기존 MPH의 현지 해시 확인과 이 ZIP에서 새로 재해시 가능한 파일을 구분한다.

별도 작업 사본에서 다음 검사는 Python 표준 라이브러리로 수행할 수 있으며 COMSOL을 호출하지 않는다. 산출물을 쓰므로 수신 보존 원본을 작업 폴더로 직접 사용하지 않는다.

```text
python work/core16_control/analyze_results.py
python work/core16_control/raw_recheck.py
python work/core16_control/extract_steps.py
python work/core16_control/independent_native_review.py
python work/time_caps/zip_identity_verify.py --root .
```

extract_steps는 동봉되지 않은 기존 MPH에 대해 audit_files.json의 기존 해시를 사용하고 재검증 아님을 명시한다. source preparation·전체 보존·final_checks·final provenance는 현지 전체 목록을 필요로 하며 이 부분 포장만으로 전체 현지 파일을 재검증할 수 없다. 그림 재생성에는 Matplotlib/NumPy가 필요하다. 설치 캐시와 임시 fixture는 포함하지 않는다.

## 보존 수준과 종료

새 계산 전 현지 명부 1,247개 중 1,246개 불변과 계획서 1개의 변경 전 사본을 현지에서 확인했다. 이 명부 전체가 외부 검증됐다는 뜻은 아니다. 직접 포함된 명부 파일 수와 불변/계획서 사본 수는 PROVENANCE_LEVELS.json 및 최종 영수증에 따로 적는다.

이전 A 수신 확인은 780,744,308bytes·SHA 63bdb39c2956e1865441e26ffff344017b6c884519a7e94cf7c8acbf717e60b7, 201payload+manifest/CRC/history333이다. 이는 사용자가 보고한 수신 측 확인이며 현지 생성 영수증과 구분한다. 당시 현지 1,099개 중 직접 57개(56개 불변+계획서 변경 전 사본 1개) 범위이고 다른 1,042개 현재 바이트의 외부 검증이 아니다. 승인·중복 부재·20코어 요청 거부의 현지 기록과 수신 측 직접 관측도 구분한다. 이전 TIME_CAPS 두 raw ZIP 차이 원인은 미확인이다.

역사적 333개 보관 바이트는 PREFLIGHT ZIP·manifest·SHA 영수증·333 명부·검증 코드를 포함하여 최종 ZIP에서 재구성하고 검증한다. 현재 현지 파일 검증 수에 합산하지 않는다. package_manifest.json은 자기 자신을 제외한 payload의 크기·SHA를 적으며 과거 manifest는 당시 기록이다. 전체 새 ZIP의 크기·SHA·CRC와 역사 333개 검사 후 외부 영수증에 현지 생성본 raw 식별을 기록한다. 새 수신본의 확인은 아직 별도다.

**전체 수렴 미완·장시간 운전 보류.** OCP 외삽 none과 OCP입력/고체표면 StopCondition, 기존 failed/INCOMPLETE_RANGE_STOP을 보존한다. 전해질 양수는 **후처리 검사**다. OCP·초기 조성·Li 재고 보정은 없다. B·추가 메시/시간 계산·재시도·전체 프로토콜·12시간 휴지·유한 sigma·sweep은 별도 승인이다. 이번 한 건과 자료 검증을 마치고 정지한다.
