# R1 소비자 정정 기록 — S1O-N1 / N2

정정 대상은 새 R1 폴더의 `candidate/consumer.py.inactive.txt`와 `contracts/CHARGE_BALANCE.json` 두 파일뿐이다. 원본은 수정하지 않았다. 후보 import·함수 호출·기능 시험·COMSOL/JVM·컴파일은 수행하지 않았다. 아래 평가는 소스 작성과 정적 텍스트 확인 범위이며 기능 PASS가 아니다.

## N1: 전체 저장 격자와 Li 출처 결속

`charge_balance`(218행 시작)는 charge의 전체 시각 배열, global의 순서 있는 키, 별도로 제공되는 native 실제 저장 시각 배열을 Decimal 값으로 정확히 대조한다. global 각 행의 time_s도 키와 같아야 한다. 정상 종료는 configured=actual=safe end이고 보호 종료는 safe=t_minus=마지막 직전 저장 시각 < actual=t_plus=마지막 저장 시각 < configured이다. 보호 중단 뒤 상태를 전하 적분에서 버리거나 수치 비교 prefix로 전하 적분 구간을 잘라서는 통과하지 않는다.

같은 시각의 LiN/P/E는 global Li 세 항과 정확히 같아야 한다. `analyze`(355행 시작)는 charge/global/raw-native-grid의 path·bytes·SHA가 각각 별도 입력 식별 및 source_evidence에 결속되는지와 run/manifest를 확인한다. 단위는 고정 8개 필드 매핑 및 mol/m^2이다. quadrature bound의 grid SHA도 같은 raw-native-grid 식별에 결속한다.

이 작업은 raw/native 어댑터를 구현하지 않았다. 기존처럼 원시 바이트·단위의 실제 판독 및 정규화 연결은 OPEN이며 새 필수 식별/격자가 없으면 실패한다. 어댑터가 없는 지금, 메타데이터를 채웠다는 사실만으로 실제 native 출처나 동작을 입증했다고 하지 않는다.

반환 charge_budget은 S1O_CHARGE_BUDGET_R1이다. grid_binding에 전체 times_s, count, 시작/실제/설정/safe 종료, native_reason, 세 원본 식별, 단위·Li 정확 일치 상태가 있다. 부모가 자신의 검증된 native 축과 비교하도록 전달했다.

## N2: 인접 구간 방향과 첫 위반 보존

누적 qN/qP 판정은 유지한다. 여기에 모든 인접 실제 저장 시각에서 dqN=F*(LiN_prev-LiN_now), dqP=F*(LiP_now-LiP_prev)를 검사한다. 기존 2e-4 C/m²보다 엄격히 작은 음의 증분만 역행이다. 정확한 ±2e-4 및 그 안의 변화는 RESOLUTION_LIMITED이며, 새로운 변화율 한도나 시간 간격으로 나눈 문턱은 추가하지 않았다.

누적량이 양수인데 구간만 역행하면 REVERSE_LI_INCREMENT이다. 누적량도 기존 기준을 위반하면 기존 REVERSE_LI_TRANSFER 이유를 우선 보존한다. 양쪽 모두 실제 최초 역행 구간이 있으면 errors.details와 부분 charge_budget에 t_minus/t_plus, dqN/dqP, deadband, 위반 전극 목록을 남긴다. 후보는 그 지점에서 정지하며 뒤 행을 검사했다고 하지 않는다. 누적 기준 위반이지만 모든 인접 증분이 deadband 안인 경우에는 존재하지 않는 구간 역행을 만들어 기록하지 않는다.

정상 기록에는 각 행의 interval_start_s/dqN/dqP/interval_sign 및 전체 checked_intervals=count-1, first_violation=null을 남긴다. 미세한 개별 구간의 부호 미해결은 기존 최종 누적 부호/전하 보존/적분 불확실성 판정과 구분한다.

## 후속 검증안에 필요한 조건

- 기존 CHARGE01–12는 새 필수 문맥을 가진 동일 양성 fixture에서 시작한다. N1 반례가 아닌 수치 반례는 charge와 global Li를 함께 일관되게 바꾸어 의도하지 않은 앞단 거부를 PASS로 세지 않는다.
- native/charge/global 전체 격자 양성, 끝/중간 누락, 같은 길이 시각 변이, global Li/시각/출처/단위 불일치, 보호 종료의 전체 charge와 safe 비교 prefix 구분을 포함한다.
- 양의 누적 q에서 인접 역행, 정확 음·양 deadband 경계, deadband 안 변화, N 또는 P만 역행, 첫 위반 이후 자료를 처리하지 않는지와 오류 구조 보존을 확인한다.
- 실제 analyze 결과 JSON을 부모가 직접 소비한다. 함수 모사로 대체하지 않는다. 원래 98개 ID의 표기와 새 사례 수는 검증안 담당자가 별도로 기록한다.

## 정적 도구 기록

수신 코드 대신 PowerShell 텍스트 읽기/Get-FileHash와 apply_patch만 사용했다. 후보를 읽어 함수 실행한 것은 없다. 읽기 명령 b83eb1은 control 원문 읽기 뒤 새 폴더 `notes` 목록 확인에서 경로 부재 오류를 내 rc1, wall 6.8695128초였다. 원문: `Cannot find path 'C:\Users\BML\Documents\Codex\2026-09-13\files-mentioned-by-the-user-comsol63\outputs\microshort_s1o_r1_20261008\notes' because it does not exist.` 이는 준비 관측 도구 오류이며 후보 시험 실패가 아니다. 이후 부모가 notes 폴더를 만들었다. 오류를 기능 실행으로 바꾸거나 숨기지 않는다.

파일 위치와 SHA는 이후 전체 정적 확인·봉인 때 다시 산출해야 한다. 최종 정정 consumer SHA는 `0cb1aa3cc4593dcb041115baf208c4dd09186fcc75055ddcde53c68086cc6b79`, 계약 SHA는 `6ce428333b98bc219e99d8fd4de173d28680489d0e86ec630213cc2a709fe66c`다.

부모의 `S1ChargeFields`·`S1NativeAxis`·`S1Coverage`를 텍스트로 교차 확인했다. 소비자와 부모의 전체 charge 격자·필드명·방향/deadband 분류 및 safe-prefix 구분이 정적으로 대응한다. 보호중단 t_minus를 양쪽 모두 마지막 직전 실제 저장 시각으로 맞췄다. 실제 Python JSON→PS 호출은 아직 하지 않았다.
