# 1198 현재 정책·실행 경로 부속서

2026-09-28. 고정 R1 후보의 읽기 전용 확인과 실행 전 승인문 작성 결과다. **오프라인 검증 수용을 재사용하며, 정책 무변경 단발 시험을 별도 사용자 결정에 올릴 수 있다. 실제 호출 성공·내부 실효 정책 확인 또는 실행 승인은 아니다.**

## 현재 확인

- 검증 ZIP SHA `6af5463ed0d395353de1a9935088c1d6f9503e476d0b5bc1fc9fb65ab80903d1`와 현지 파일이 일치한다. 수신 검토 ZIP은 자체 manifest/집합/크기/SHA/CRC/경로를 확인했다. 수신자 보고 26군·78사례 수용을 별도 기록으로 접수하며 시험은 반복하지 않았다.
- 원 R1 manifest SHA `0c14c4f886d53398fc4869db117577066b821837cd3593a6727e2ac4d0a63c45`, Java SHA `a742a3f6a19cc21c4c6b3be7ca9cf69eb35c68a70c52b38166971774c0ce1e95` 일치. 소스·계약·부모·외부 의존·기준 CSV·Python/PowerShell/compile/batch 실행파일을 68항목(중복 참조 포함) 대조했다. CSV는 해시만 읽었으며 수치 재분석하지 않았다.
- 기본 prefs: `C:/Users/BML/.comsol/v63/comsol.prefs`, **22,252 bytes / SHA `064d190077d7533f9fff22b61460d377cb53fb314e5c0f32a0bd02e3fa28b651`**. security 16키 중복 없음, `security.external.enable=on`, `security.external.filepermission=limited`. 전체 prefs/로그인/라이선스 내용 및 전용 복사본은 보관·생성하지 않았다. 시각/전체 security 값은 POLICY_OBSERVATION.json에 있다.
- future_run_001, future_parent_001, future_authorizations 디렉터리 및 승인/release 경로는 관측 시 부재다. 부모/자식 cwd는 존재한다. 생략된 다른 위치의 token 부재까지 주장하지 않는다.
- 46개 선택 파일의 전후 식별을 보존한다. 라이브 프로세스·사용자 SID/elevation/콘솔·ACL 쓰기 권한·실효 정책은 이번에 조회/시험하지 않았다. 실제 실행 직전에 고정 코드가 확인할 대상이다.

## 주체별 읽기·쓰기와 증거 경계

경로의 `ROOT`, `RUN`, `PARENT`는 각각 원 R1 폴더, 그 아래 future_run_001, future_parent_001이다. 절대 경로와 인자 전체는 EXACT_COMMANDS_KO.md 및 EXACT_COMMAND_MAP_REFERENCE.json에 있다.

| 주체 | 고정 입력/출력 | 소스 근거 | 현재 제한 및 아직 미관측인 부분 |
|---|---|---|---|
| 외부 Python | ROOT 소스/계약, baseline_files, 기본 prefs 읽기; RUN의 staged Java·전용 prefs·START/GATE/예약/event/반환/state·tables/CSV·TRIGGER_RESULT 쓰기 | candidate_entry.py:47–59, 96–177, 184–212 | 입력 바이트 읽기는 이번에 확인. RUN 쓰기는 미시도. COMSOL methods의 파일 정책과 외부 Python의 OS 권한은 별개. prefs 사본은 승인 뒤 byte copy만 허용하며 기본 파일을 바꾸지 않음 |
| COMSOL compile 실행파일 | RUN/Guard1198Candidate.java 읽기, 같은 RUN의 class 출력; 전용 prefs/config_compile/data_compile 사용 | CONTRACT.commands.compile; candidate_entry.py의 compile 예약/transport 호출 | 실행파일 바이트 일치. native 컴파일/API 호환성·OS 쓰기·설치 보안 정책의 실제 적용 미관측 |
| COMSOL batch 실행파일 | RUN/Guard1198Candidate.class, prefs/config_batch/data_batch; batch.log·콘솔·MPH 출력 | CONTRACT.commands.batch, expected_mph_name; candidate_entry.py의 process_ok 및 MPH 집합 검사 | -np16은 요청이다. 출력 result.mph 인자와 기대 실제 result_Model.mph를 구분. class 실행/기본 기능의 파일 저장 성공 미관측 |
| 후보 Java 표 출력 | `System.out.println(AUDIT_TABLE_BASE64=...)`; 외부 Python이 콘솔 로그에서 추출 CSV 생성 | Guard1198Candidate.java:61; candidate_entry.analyze | Java stdout 쓰기와 디스크 CSV 쓰기는 다른 주체. 표가 출력되어도 후속 저장·전체 완료 성공을 뜻하지 않음 |
| 후보 Java 파일 저장 | `m.save("axes_generated.java","java")`; 의도 경로 RUN/axes_generated.java | Guard1198Candidate.java:468; batch cwd=RUN | 상대 경로 COMSOL API 저장. 현 limited 정책에서 허용되는지 **미확인**. stdout 성공으로 이 권한을 추론하지 않음. 저장 실패는 오류 보존·후속 성공표시 차단 대상 |
| 부모 PowerShell5.1 | PARENT transcript/시작/즉시 native·analysis rc/분석 소비/최종 경계 | PARENT_COMMAND.ps1 BInvoke/GDecision/try/finally | 일반 사용자 NoProfile 전경 호출. 부모 파일 쓰기·native workflow 전체는 미실행. 기록 문자열/rc0만으로 전체 PASS하지 않음 |

고정 후보는 fresh ModelUtil.create로 모델을 만들고 embedded 재료/OCP 표를 사용한다. 코드의 LIBRARY_SHA 출력은 원 재료 출처 표식이지 이번에 라이브러리 MPH를 읽었다는 영수증이 아니다. 새 후보에 loadCopy/Files.newInputStream/getPreference를 호출하는 경로는 없다. 과거 B020의 저장 해 로드·원시 파일 읽기 실패를 이번 fresh 모델 경로의 확정 실패로 옮기지 않는다.

## 공식 근거와 판정

COMSOL 문서는 methods/Java libraries의 파일 접근을 제한하는 설정과 외부 프로세스 설정의 범위를 설명한다. `allowexternalprocess=off`를 외부 Python에서 COMSOL 실행파일을 시작할 수 없다는 뜻으로 해석하지 않는다. 다만 저장된 설정은 실제 프로세스의 내부 정책을 증명하지 않는다. [Security Settings](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_running.38.10.html)

Windows CLI 문서는 -prefsdir/-configuration/-data와 -np의 목적을 설명한다. 이번 명령은 고정 전용 경로를 사용한다. -tmpdir는 고정 argv에 없으므로 COMSOL의 모든 임시 파일이 RUN 아래만 생성된다고 주장하지 않는다. 새 옵션을 넣거나 다른 경로로 우회하지 않는다. [Windows Commands](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_ref_running.38.31.html)

model.save의 Java 저장과 상대 경로 규칙은 공식 API에 있다. 이 후보에는 modelPath/user.dir 재설정이 없어 RUN 하위 파일이 의도한 대상이다. 그러나 이 설명은 limited 정책에서 그 API 호출이 허용된다는 확인이 아니다. [model API](https://doc.comsol.com/6.3/doc/com.comsol.help.comsol/comsol_api_general.47.16.html)

**읽기 전용 근거로 확정한 native 차단은 없으며, 모든 native 파일 작업이 허용된다고 확정할 근거도 없다.** 가장 구체적인 잔여는 Java의 상대 경로 저장, batch 출력 및 전용 prefs/config/data 사용이다. 별도 probe를 요구하지 않고, 이러한 실패 가능성을 수용한 정책 무변경 1198 단발 시험으로 한정한다. 차단되면 원문을 남기고 중지한다. All files·Enforce 해제·기본 prefs/registry/ACL 편집·관리자/다른 셸/fallback은 포함하지 않는다.

## 상태와 보충

N1/N2 및 26군·78사례는 수용 완료다. 승인과 검증 release는 아직 없다. 원 manifest/계약의 approved=false/usable=false와 과거 '검증 미실행' 문구를 수정하지 않고 이 부속서가 현재 검증 수용을 연결한다. 원 EXECUTION_CONNECTION_KO.md는 R1에 없었으므로 이번 실제 소스/COMMAND_MAP 근거의 연결표로 문서 참조를 보충했다. 실행 파일 누락은 아니다.

V-O1: harness raw SHA와 LF 정규화 SHA는 별개다. REVIEW_NOTES_SUPPLEMENT.json에 각각 기록했다. V-O2: 기존 DELIVERY_RECEIPT.json 원문을 VALIDATION_DELIVERY_RECEIPT_ORIGINAL.json으로 추가했다. 마지막 포장 도구 반환의 원시 파일은 찾지 못해 미확인으로 남기며 가짜 반환/OS 감사를 만들지 않는다.

과거 전체/정상 gate INCOMPLETE, 실제 코어/내부 정책 UNVERIFIED, failed/pending/원복·recipient=null, OCP 외삽 금지 및 TIME_CAPS 원인 미확인을 유지한다. 이번에는 문서용 데이터 검사만 실행했고 후보 import/시험/COMSOL/JVM/입력/정책 변경은 0회다.
