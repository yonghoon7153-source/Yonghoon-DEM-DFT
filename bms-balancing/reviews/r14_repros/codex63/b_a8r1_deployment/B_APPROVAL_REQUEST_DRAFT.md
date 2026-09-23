# B_A8R1 고정 후보 — 실제 B 별도 승인용 비활성 초안

2026-09-24. **B 미승인 / usable=false. 이 문서는 실제 승인 파일이 아니다.** 오프라인 배치의 독립 수용과 아래 TTY 조건 확인 전 실제 B를 시작하지 않는다.

## 고정 후보

- source: `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/api_recovery_B_A8R1`
- run: `saved_solution_A8R1_b006`
- RUN/OUT: `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/api_recovery_B_A8R1/runtime/b006` / `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/api_recovery_B_A8R1/runtime/b006/output` — 아직 생성하지 않음
- Java SHA: `5a9da0f9da79a6d5f848af5ee3ea9792b06918110a8fae8a54b5a4fc05db6c39`
- raw contract SHA: `45a63bf1a33039c6556f024e26592d01e4ec4db1594dd7ef28713354cdc49043`
- CODE_MANIFEST SHA: `fa5592734f4d082bfc7bcb7ceaf70ec1407cd35342dadee100bf939f8297329b`
- 사용자 실제 승인 예정 위치: `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/api_recovery_B_A8R1/approvals/saved_solution_A8R1_b006.json` — RUN 밖, 아직 없음
- 내부 batch_authorized.json 및 permission_token.txt는 승인된 launcher가 B 실행 안에서만 생성한다. 현재 없음.
- 네 executable/argv/cwd: `PLANNED_COMMANDS.json` 및 봉인 contract/binding. arbitrary 경로 fallback 없음.

## 아직 충족하지 않은 TTY 조건

현 launcher는 **Desktop apply가 끝난 뒤** timed_attest에서 isatty를 검사한다. Desktop 전의 코드 gate가 아니다. 같은 실제 호출 경로에서 현지 사용자가 ALL_FILES/RESTORED를 입력할 TTY의 사전 확인·확인 주체·증거가 아직 없다. 이번 오프라인 작업에서는 실제 TTY/native 시험이나 launcher/transport 변경을 하지 않았다. 이를 해결하지 않은 채 B 실행을 승인·시작하지 않는다. 코드 선행 gate가 필요하면 그 최소 변경을 별도로 승인받는다.

## 향후 B 사용자 승인에 포함할 범위

1. 입력 `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/comsol63/electrolyte_recovery/inputs/failed_normal_copy.mph`, 1,266,539,803 bytes / SHA `7fefc0cfdf6910d40f2fec8021d6efbc72250c4e8ff79ba4a9442233bc581658`의 저장 해만 사용한다. 기준 job5d1a87652ed54e6a945d4f2af4aeda70의 봉인14 CSV·좌표를 재사용하고 기준해 추가 로드/solve는0회다.
2. 새 source/runtime·코드·실행파일·입력/보호/기준 파일 식별, 현재 작업·자원·일반 사용자 권한을 확인한다. RUN이 이미 있거나 값이 다르면 중지하고 삭제·재사용·재시도하지 않는다. 과거 A7/A8/b003 승인/횟수를 쓰지 않는다.
3. 현재 기본 prefs 22,252 bytes / SHA `064d190077d7533f9fff22b61460d377cb53fb314e5c0f32a0bd02e3fa28b651`, security16개 동일을 시작 기준으로 한다. B에서만 새 전용 prefs로 복사한다. 기본 prefs/설치INI/registry/ACL은 변경하거나 과거 바이트로 복원하지 않는다.
4. 적용 Desktop1회 + 원복 Desktop1회, 각각 모델로드0. 현지 사용자가 전용 All files를 적용하고 원래 limited로 원복한다. All files는 일반 사용자에게 허용된 파일 전반에 대한 Java 접근 확대이므로 그 범위를 별도로 수용해야 한다. 특정 MPH 하나의 권한이나 OS sandbox가 아니다. Enforce 및 다른 보안값 유지. 정책잠금/추가완화/기존작업 충돌이면 중지한다.
5. compile≤1, batch≤1, loadCopy≤1, solve/초기화/메시 재생성/MPH 저장0. Java RUN/OUT 외 수치·API 본문은 A8과 동일하다. daudit/sol1/mesh1, 전체987 저장시각,9개 허용 numerical tag·14열 global·boundary1/4·pce6표·전극당241좌표 및 단위/형상/domain/유한값을 원래 계약으로 검사한다. 해시/argmin 제외·기존 미완을 숨기지 않는다.
6. 요청187 및 정확 공통×4창, ΔV≤1mV, pointwise Δx≤1e-4, Li 총상대변화≤1e-6/초기각항차≤1e-9mol/m², 최소 일치≤1e-9mol/m³·threshold0·세 guard0 유지. 시간/공간/단위 대체·근처값·평균값 보정 없음.
7. 명시 launcher와 네 자식 argv/cwd 전체를 앱의 정식 명령 심사에 제시한다. 사용자 승인과 도구 허용은 별개다. 추가 elevation/관리자 실행·sandbox 우회·다른 loader/transport는 허용하지 않는다.
8. timeout/오류 때 소유 root PID+생성시각/Job membership·assignment/resume·terminal에 근거한 소유 Job만 정리한다. 배정 전 suspended root는 보유 handle의 그 root만 대상으로 한다. 이름 일괄 종료 금지. 불명 귀속/helper 잔류/종료 미확정이면 후속 native 단계와 추가 UI를 시작하지 않는다.
9. first error·raw console/batch.log·부분 출력·정리/보존/원복 오류를 함께 보존한다. 정상 finally와 외부 정리를 구분한다. 강제 종료 후 after-U 부재는 미완이며 자동 원복 보장은 없다. 원복 소진/실패 뒤 state를 고쳐 재호출하지 않는다. 기존 b003 pending 및 별도 원복 기록은 수정하지 않는다.

## 새 B 예산 제안 — 아직 승인 아님

| 단계 | 제안 |
|---|---:|
| 시작 확인 | 300초 |
| 적용 UI | 900초,1세션 |
| compile+batch | 합계1800초,각1회,16코어 |
| 소유 정리 | phase당120초,최대4phase |
| 원복 UI | 900초,1세션 |
| 오프라인 분석 | 600초,1회 |
| 보존 | 180초 |
| 전달·최종 관측 | 600초 |
| 전체 | 새 착수 anchor부터7200초 |

시작 가용 RAM8GiB/디스크5GiB 이상. 충분함/최대 메모리 보장은 아니다. native helper/자원/응답 불명은 재시도 사유가 아니라 중단 사유다. launcher가 집행하는 다섯 예산 필드는 `{"apply": 900, "compile_batch": 1800, "process_cleanup": 120, "restore": 900, "offline_analysis": 600}`이며 전체/시작/보존/전달 관리 한도를 이미 모두 강제하는 코드로 표현하지 않는다. 단계 미사용분을 시험·계산 연장으로 전용하지 않는다.

별도 실제 승인 파일은 사용자 B 승인 후에만 만들고 run/최종 manifest SHA/위 다섯 예산 필드 및 All files·두 UI·무상승·solve0·정식 도구 심사·자식 범위·기존 pending 보존·현재 prefs 시작값·소유 정리 수용을 명시해야 한다. `contract.approved=false`/문서 usable=false 자체가 별도 실행 차단장치라는 주장은 하지 않는다. 실제 승인 파일·검증 경로가 실행권을 결속한다.

## 최종 판정 및 유지

numeric_recovery/sampled_comparison/preservation/process_cleanup/policy_restore와 전달 완료를 나눈다. 완료 소비·원시 rc·마지막 누적시간/코드/파일 식별이 함께 맞아야 해당 범위 완료다. 숫자 또는 파일 PASS만으로 전체 완료를 만들지 않는다. 오류 자료 포장은 진단용으로 구분한다.

정상 전체 gate/API 복구/전체 수렴·장시간 보류, OCP 외삽 금지, TIME_CAPS raw ZIP 차이 원인 미확인, 원래 failed·MPH·ZIP·recipient=null을 유지한다.1198/후보C/추가 모델 시험/전체프로토콜/12시간휴지/유한sigma/sweep은 미승인이다. 결과 전달 후 정지한다.
