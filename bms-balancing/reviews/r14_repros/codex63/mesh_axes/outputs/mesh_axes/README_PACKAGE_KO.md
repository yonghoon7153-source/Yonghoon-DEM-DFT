# COMSOL 6.3 — 5초 메시 축별 추가 진단 전달본

이번 범위는 0.1C·sigma=1e-20 S/m에서 300/40, 300/80, 600/40의 **새 5초 계산 세 번**이다. 세 조건 모두 새 187개 시간표를 사용했다. 첫 1초에는 107개 공통 시각이 있다.

반경 축의 최대 전압 차는 0.04초에서 2.505310864 mV로 기준 1 mV를 넘었다. 최대 표면 x 차는 4.182398438e-5로 기준 안이다. 물리 축 비교는 지정 표본의 두 기준을 충족했다. 전체 메시 수렴은 미완이다.

추가 600/80·시간간격 반감 시험은 제안만 했으며 실행하지 않았다. 전체 프로토콜·12시간 휴지·기준값 외 sigma·sweep도 실행하지 않았다.

## 먼저 읽을 자료

- [결과 보고서](MESH_AXES_RESULTS_KO.md), [수정한 NEXT_RUN_PLAN](../NEXT_RUN_PLAN.md)
- [독립 소스·native·보존 감사](INDEPENDENT_AUDIT.md), [독립 수치 검토](results/independent_review.md)
- [비교 그림 PNG](figures/axis_comparison.png), [PDF](figures/axis_comparison.pdf)
- [소스 SHA](source_configs.json), [실제 메시·solver 요약](native_evidence.json), [전달 전 검사](delivery_checks.json)

표면 값은 공통 저장 시각에서 241개 좌표/전극의 FE 공간 보간으로 평가했다. 시간 보간은 없으며 최대값은 지정 시간·공간 표본에 한정된다. 전압 분해와 최대 시각/좌표는 results/ CSV와 JSON에 있다.

현재 StopCondition은 OCP 입력과 고체 표면 조성을 감시한다. **전해질 양수는 후처리 검사이며 전해질 음수의 실시간 중단은 구현되지 않았다.** OCP 외삽 금지·초기 조성·Li 재고를 유지했다. 기존 범위 시험의 failed 및 INCOMPLETE_RANGE_STOP은 그대로이며 다른 실패에 이를 자동 부여하지 않는다.

## 묶음 구성

ZIP 경로는 작업 폴더 기준 상대경로를 유지한다.

- outputs/mesh_axes/: 새 결과·설정·비교 CSV·그림·독립 검토·이전 파일 보존 ledger·이전 계획 사본
- outputs/model_audit/<새 job>/: 원시 CSV 14개/job, MPH에서 추출한 dmodel.xml, audit_files.json
- outputs/comsol63/.comsol-jobs/<새 job>/: request/status, staged Java, compile/batch/console/worker 로그, generated Java, 저장 MPH
- outputs/comsol63/mesh_axes/: 실제 제출 Java 세 개
- work/mesh_axes/: 준비·분석·검증·그림·보고서·묶음 스크립트와 테스트. 이 스크립트들은 COMSOL을 자동 제출하지 않는다.
- work/decode_comsol_audit.py, work/dense_surface_profile_api.md, 원래 PreflightMeshFine5s.java: 추출·재현의 근거
- outputs/preflight/results/analysis.json 및 기존 range job의 request/status/log: **과거 실패 분류를 확인하는 참조 증거**다. 새 메시 비교 입력이 아니다.

새 모델 세 개는 수동으로 검토할 수 있게 포함했다. COMSOL 6.3 및 해당 라이선스가 필요한 재실행은 이번 인계에서 승인되지 않았다. 분석은 Python 표준 라이브러리, 그림은 Matplotlib/NumPy를 사용한다. 로컬 Python·COMSOL 설치와 캐시는 포함하지 않았다. 일부 준비/검증 스크립트는 기존 작업 폴더의 baseline 증거를 필요로 하므로 새 ZIP만으로 333개 과거 파일의 검증을 모두 다시 수행할 수 있는 것은 아니다.

이전 ZIP은 원본 그대로 별도로 유지했다. COMSOL63_VALIDATED_SHORT_HANDOFF.zip SHA-256: fe52f0d72ae3bb122cdd5135dbb6322e1f2531e6d6b9e1a767e23cde19c0c9c2. COMSOL63_PREFLIGHT_HANDOFF.zip SHA-256: 3bc4e4e4d14ff815a710998ac3e538712343933cef6d460eb5845f21e7235018.

## 무결성

package_manifest.json은 자기 자신을 제외한 모든 ZIP 항목의 경로·크기·SHA-256을 기록한다. 패키저는 ZIP의 전체 CRC와 각 항목의 SHA·크기를 확인한 뒤 ZIP 옆에 SHA-256 파일과 검증 영수증을 만든다. ZIP 자신의 SHA와 검증 영수증은 자기 참조를 피하기 위해 ZIP 밖에 둔다. 파일 무결성은 독립 COMSOL 재실행이나 물성 정확도 검증과 다르다.
