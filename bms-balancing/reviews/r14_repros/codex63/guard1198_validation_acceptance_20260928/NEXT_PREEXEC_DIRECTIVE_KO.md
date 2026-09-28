# 다음 작업 — 정책·실행 경로 읽기 전용 확인과1198 승인문 확정

2026-09-28. **사용자가 채택해 현지 Codex에 전달할 작업지시 초안. 이 문서 자체는 실제1198 실행 승인이 아니다.**

> G1198-N1/N2와26논리군·78하위사례 한정 검증은 수용된 범위로 유지하세요. 다음은 고정 R1 실행본의 현재 정책·경로를 읽기 전용으로 확인하고, 최종1198 단발 시험 승인문을 채워 제출하는 한 건입니다. 새 코드/재봉인/suite/입력 진단/COMSOL 호출은 하지 마세요. 동일 개괄 계획을 반복하지 말고 아래 미확정값과 근거를 구체적으로 채우세요.

## 1. 고정 대상

- 검증 ZIP SHA `6af5463ed0d395353de1a9935088c1d6f9503e476d0b5bc1fc9fb65ab80903d1`.
- 실행 후보 manifest SHA `0c14c4f886d53398fc4869db117577066b821837cd3593a6727e2ac4d0a63c45`.
- Java SHA `a742a3f6a19cc21c4c6b3be7ca9cf69eb35c68a70c52b38166971774c0ce1e95`.
- run_id `guard1198_candidate_001`.
- 원 실행 source 위치는 현지 workspace의 `outputs/guard1198_limited_validation_R1_20260928/`다. 전달 ZIP의 candidate/ 사본 위치에서 실행하거나 임의로 옮겨 ROOT를 바꾸지 않는다. COMMAND_MAP/CONTRACT의 정확 argv/cwd를 사용한다.
- 기존 코드·manifest·계약·NATIVE_APPROVAL_DRAFT의 과거 상태는 수정하지 않는다. 새 현재 상태 부속서에 검증 수용과 남은 조건을 연결한다.

## 2. 확인할 최소 항목

### A. 현재 식별과 경로

현재 원 source/contract/parent 및 외부 의존 식별이 봉인값과 같은지 읽기 전용으로 대조한다. compile/batch 실행파일 식별도 읽기만 한다. 모듈 import, 버전 명령을 위한 프로세스 기동, COMSOL probe는 하지 않는다.

future_run_001·future_parent_001·실제 승인/release/token 경로가 아직 생성되지 않았는지 확인한다. 있으면 삭제/재사용/다른 이름 fallback하지 말고 보고한다. 기본 prefs는 CONTRACT가 가리키는 정확 파일의 크기/SHA·security 키/값만 읽고 중복/Enforce 및 관측 시각을 남긴다. 라이선스/로그인/전체 prefs 원문은 전달하지 않는다. 이 단계에서는 전용 prefs 사본도 생성하지 않는다.

### B. 읽기/쓰기 주체와 정책 범위

다음 대응표를 작성한다: 주체 / 고정 경로 또는 출력 / 근거 / 현재 알려진 제한 / native에서 아직 미관측인 부분.

- 외부 Python의 source·baseline·prefs 읽기, 승인받을 전용 복사본/기록/추출 CSV 쓰기.
- compile의 staged Java 읽기 및 class 출력.
- batch의 class·prefs/configuration/data 읽기/쓰기와 native log·MPH 출력.
- 후보 Java의 stdout BASE64 표 출력 및 `m.save("axes_generated.java","java")`의 상대 경로 쓰기. stdout과 COMSOL 파일 쓰기를 같은 권한이라고 묶지 않는다.
- 부모 PowerShell의 transcript·즉시 반환 rc·시간·후처리 결과 소비와 최종 경계 기록.

기존 로그/정확한 설정/필요한 설치 문서 또는 공식 문서로 설명하되, 과거 B020의 loadCopy·Files.newInputStream 실패를 새 fresh 모델 경로와 혼동하지 않는다. OS 접근 가능·prefs 파일 값·COMSOL 내부 실효 정책·실제 호출 성공은 서로 다른 증거다.

정책 무변경을 기본으로 한다. All files 전환·레지스트리/ACL/기본prefs 편집·관리자/다른 셸·우회는 허용하지 않는다. 현재 근거상 필요한 호출이 차단된다면 “확인 완료”로 채우지 말고 해당 호출과 필요한 최소 별도 결정만 제시한다. 반대로 실제 native 성공은 아직 없다는 이유만으로 반복 probe를 새 필수 단계로 만들지 않는다. 남은 런타임 불확실성은 별도 단발 시험 승인문에 명시한다.

### C. 실행 승인에 넣을 대응

현재 CMD/PowerShell/exec 경로를 섞지 않고, 기존 사용자 소유 일반 NoProfile PowerShell5.1·고정 Python·동일 프로세스의 새 두 challenge를 유지한다. 이 작업에서 입력 시험은 하지 않는다. AI 대리 입력도 없다.

사용자 결정→RUN 밖 승인파일→별도 검증 release→고정 manifest/검증 자료/정책 경로 보고서의 식별 대응을 표로 제시한다. 실제 승인·사용 가능한 release·runtime/token은 아직 만들지 않는다. approved=false/usable=false인 봉인본 자체를 true로 바꾸지 않는다.

## 3. 확정할1198 단발 사양 — 이번에는 실행 금지

- fresh t=0, threshold1198, 최대5초. 저장 MPH 이어달리기 아님. compile≤1/batch≤1/solve≤1, 자동retry0, 정상control 추가solve0.
- physical300/particle320·320/0.1C/sigma1e−20/기존 초기화·물성/OCP·Time·두 guard 및 stepbefore_stepafter 유지. 수치/단위/좌표/허용치 변경0.
- 요청16코어와 실제 코어 UNVERIFIED를 구분. 원 후보의 시작 RAM/디스크 관측·디스크10GiB 조건·소유 Job 정리만 사용한다. 미구현8GiB 상한/새 메모리 감시를 구현됐다고 쓰지 않는다.
- 원 계약 예산 그대로: 사전/새입력180초, compile+batch1800초, cleanup 합계120초, 분석600초, 전달300초, 전체3000초. 새 시행 원점·부모 rc·최종 경계를 명시한다. 미사용분 전용·과거 예산 재사용 금지.
- 정상 이전 ce_min>1198 / 다음≤1198, 같은 operator·guard·native 중단사유·이후 적분 없음과 필수 출력/단위/strict prefix/241좌표/Li·전압·표면 비교를 요구한다. 고정987시각을 조기 종료에 강제하지 않는다.
- trigger/sample/preservation/process_cleanup/policy_preservation을 따로 판정한다. rc0·ZIP 완성·trigger 하나만으로 전체 PASS하지 않는다. 원래 전체/정상 gate INCOMPLETE 유지.
- 첫 오류/시간·식별·경로·정책·소유 귀속 불명확이면 다음 native 단계로 넘어가지 않는다. 기존 실패/pending/state/영수증을 고쳐 재호출하지 않는다. 추가 정책 적용/원복 세션은 포함하지 않는다.

## 4. 문서 보충 및 제출

새 읽기 전용 관측·승인문 부속 기록은 기존 폴더와 분리한다. 이번 문서 작업 예산은 별도 제안 **총900초**: 식별/정책·경로확인600초, 보고/승인문240초, 보존·미완기록60초. 실제 시험/프로세스 예산으로 전용하지 않는다. 이 초안을 사용자가 채택해야 유효하다.

제출물은 현재 source/prefs 식별, 위 읽기/쓰기 대응표, 정확한 부모/execute/analyze/native argv·cwd 연결, 승인 필드 대응, 사용자가 바로 판단할 비활성1198 승인문이다. 시험을 다시 만드는 문서를 요구하지 않는다.

비차단 V-O1은 별도 기록에서 harness raw SHA `5cbe34b28b53a6034b5cf8e8d819aae21c1813fc4f1a53bd6bd83bd8f04d95b4`와 LF 정규화 SHA `352ed9d4183b4d5629d3b74fa33c74f9788e62c5025d060b735f71231b911e35`의 대상을 구분한다. 기존 CORRECTION/ZIP을 수정하지 않는다. V-O2는 이미 존재하는 DELIVERY_RECEIPT/마지막 포장 반환이 있으면 원문만 보충하고, 없으면 미확인 유지한다. 이를 만들려고 과거 시험/포장을 재실행하지 않는다.

결과를 제시하고 멈춘다. 현 정책·경로가 검토되고 사용자가 위험·횟수·자원 범위를 명시 승인하면 **그때1198 최대5초1회**로 넘어간다. 그 결과를 수용한 뒤에만 fresh0→30초 진단을 별도 승인한다. 1198을 생산 임계값으로 옮기거나30초/장시간/12시간/1198 외 시험을 이번 승인에 묶지 않는다.
