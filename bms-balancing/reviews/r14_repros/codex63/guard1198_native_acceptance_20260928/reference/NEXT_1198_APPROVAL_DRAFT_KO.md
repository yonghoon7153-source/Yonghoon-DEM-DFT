# 1198 최대5초 단발 시험 — 비활성 사용자 승인문

**현재 approved=false / usable=false. 이 문서는 실행 승인·승인파일·검증 release가 아니다. 이번 사용자 “ㄱ ㄱ”는 정책·경로의 읽기 전용 확인과 이 문서 작성 범위로 기록했다.**

검토 완료된 범위: G1198-N1/N2 및 26개 논리군·78개 하위 사례. 재시험 없이 사용한다. 고정 R1 CODE_MANIFEST SHA `0c14c4f886d53398fc4869db117577066b821837cd3593a6727e2ac4d0a63c45`, 검증 ZIP SHA `6af5463ed0d395353de1a9935088c1d6f9503e476d0b5bc1fc9fb65ab80903d1`. 원 source 위치와 정확 부모/execute/analyze/compile/batch 명령은 EXACT_COMMANDS_KO.md에 고정했다.

## 사용자가 승인할 한 건

> 위 고정 R1과 현재 정책·경로 부속서에 결속한 **1198 발동 시험 최대5초·1회**를 승인합니다. 일반 사용자 Windows PowerShell5.1 NoProfile에서 같은 Python 프로세스의 새 두 challenge를 직접 입력합니다. 현 prefs `security.external.enable=on / filepermission=limited`를 변경하지 않으며, COMSOL 내부 실효 정책과 특히 Java 상대 경로 저장·batch 출력의 성공은 아직 미확인임을 수용합니다. 거부 시 중지하고 정책 완화·우회·자동 재시도하지 않습니다. 아래 준비·실행·보존 범위만 승인합니다.

## 고정 입력과 승인 후 준비

- run_id `guard1198_candidate_001`. 실행본은 `outputs/guard1198_limited_validation_R1_20260928/` 원본을 사용한다. 전달 ZIP의 candidate 사본에서 실행하지 않는다.
- Java 73,405 bytes / SHA `a742a3f6a19cc21c4c6b3be7ca9cf69eb35c68a70c52b38166971774c0ce1e95`.
- Python 107,312 bytes / SHA `b7a12c3af0b4db44191eec14ea095eba731b7328917f570806183093d19ddca2`, 옵션 `-I -S -B -X utf8`.
- 기본 prefs 22,252 bytes / SHA `064d190077d7533f9fff22b61460d377cb53fb314e5c0f32a0bd02e3fa28b651`. 승인 후 시작 때 같은 식별이어야 하며 달라지면 중지한다. 기본 파일 편집 없이 원 코드의 전용 byte copy만 허용한다. 전체 prefs 원문을 외부로 전달하지 않는다.
- 승인 뒤에만 RUN 밖 future_authorizations에 사용자 결정 원문, 코드가 요구하는 승인파일, 별도 검증 release를 새로 만든다. 승인 필드와 증거 식별 대응은 APPROVAL_FIELD_MAPPING_KO.md에 따른다. 기존 manifest/contract의 false를 true로 고치지 않는다.
- future_run_001·future_parent_001·승인/release 경로는 지금 부재이나 시작 직전 다시 확인한다. 이미 있으면 삭제·재사용·다른 이름으로 회피하지 않는다. 과거 실패·승인·영수증은 보존한다.

## 실행과 자원

- fresh t=0, 시험 threshold1198 mol/m³, 물리시간 최대5초. compile≤1 / batch≤1 / solve≤1. 저장 MPH 이어달리기·새 정상 control·추가 solve 없음.
- physical300 / particle320·320 / 0.1C / sigma1e−20 / 기존 초기화·물성·OCP·Time·두 guard / stepbefore_stepafter를 유지한다. 수치 허용치·좌표·단위 변경 없음.
- 요청16코어와 실제 코어 UNVERIFIED를 구분한다. 원 코드의 시작 RAM/디스크 관측과 디스크10GiB 조건을 사용한다. RAM8GiB 시작 문턱·8GiB working-set 상한·1GiB/10초 메모리 감시는 구현되어 있지 않고 추가하지 않는다. 메모리 부족 등 실패 가능성이 남는다.
- 원 소유 Job 제어만 사용한다. 불명 PID·다른 사용자의 COMSOL을 종료하지 않는다. 전체 시스템이 정리됐다는 범위로 확대하지 않는다.
- 사전/새 입력180초(두 응답 각 최대60초), compile+batch 합계1800초, cleanup 합계120초, 분석600초, 전달300초, 전체3000초. 새 부모 Stopwatch 및 자식 ENTRY_START를 각각 기록한다. 원점이 다르며 과거 예산을 이어 쓰거나 단계 잔여를 재시도에 전용하지 않는다. 전체 상한은 각 단계 한도와 함께 적용한다.
- 부모는 호출 직후 `$?`와 `$global:LASTEXITCODE`를 보존하고 외부 기록·분석 결과·최종 경계를 소비한다. 자체 실행 중 아직 모르는 최종 host rc를 미리 성공으로 기록하지 않는다. native 실패 자료의 분석은 state가 있을 때 원 부모가 최대1회 수행하며 추가 native 시도는 아니다.

## 판정과 중지

초기 guard=false, `t_minus<t_plus<=5`, 직전 동일 Minimum>1198 / 다음≤1198, 전해질 guard0→1, 동일 operator/selection/단위, native 중단사유 일치 및 이후 추가 적분 없음이 필요하다. StopCondition의 step 후 평가와 정지 전후 저장은 모든 내부 반복/연속 시공간 양수성 보장이 아니다.

실제 저장 시각의 strict 요청 prefix·정확 공통 비교를 사용한다. 빈집합·t=0만의 비교·누락/중복·보간/최근접 대체는 PASS로 인정하지 않는다. N/P 각241좌표·domain/유한값/단위, Li·전압분해·표면 비교를 유지한다. 비교 허용치는 전압1mV, 표면x1e−4, 상대Li1e−6, 전압항등식1e−8V 등 원 계약 값이며 절대 운전 한계가 아니다.

trigger / sampled_comparison / preservation / process_cleanup / policy_preservation을 각각 판정한다. 수용 대기라도 overall/normal gate는 INCOMPLETE, effective policy/실제 코어는 UNVERIFIED다. rc0·trigger 하나·ZIP 생성만으로 전체 PASS하지 않는다.

첫 오류·정책 거부·시간/식별/경로 위반·소유 불명확이면 다음 native 단계로 넘어가지 않는다. 원 코드가 허용하는 소유 정리/실패 보존/분석 외 수동 재실행·추가 설정 적용/원복 세션은 없다. 실패를 고쳐 덮어쓰지 않는다.

출력은 원본 로그·GATE·예약·즉시rc·state·MPH 식별·BASE64 추출CSV·단위/guard/solver 증거·비교/정리/정책보존·부모 최종 경계다. 실효 정책 확인을 꾸며 넣거나 외부 지원에 자동 전송하지 않는다. 결과 제출 후 중지한다. 1198 결과 수용 후 fresh0→30초 진단은 별도 승인이다. 장시간/12시간/후보C/CDC/휴지/1198의 생산 임계값 전환은 포함하지 않는다.
