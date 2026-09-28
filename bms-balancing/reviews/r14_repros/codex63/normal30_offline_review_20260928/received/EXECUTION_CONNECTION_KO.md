# 실행 연결 후보와 승인 대응

현재는 비활성이다. 정확한 전체 argv 배열은 `COMMAND_MAP.json`, 실제 native compile/batch 배열은 `CONTRACT.json`에 있다. 두 파일은 같은 source/run을 가리킨다.

| 대상 | 고정값/연결 |
|---|---|
| source root |현재 workspace의 outputs/normal30_offline_preparation_20260928 |
| run_id |normal30_candidate_001 |
| manifest |28dd6da5cc76885263c17b2671548a00692064807e02e77ceb6f3edbdd946fa5 |
| Java |src/Normal30Candidate.java; staged class도같은이름 |
| 실행/분석 Python |C:/Users/BML/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe; -I -S -B -X utf8 |
| execute/analyze cwd |C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/b020_profile_unit_stages_20260927/src |
| native cwd |새root/future_run_001 |
| native 출력 |batch.log,batch_console.log,result_Model.mph,axes_generated.java,분리된prefs/config/data,추출tables/ |
| 분석 결과 |future_run_001/DIAGNOSTIC_RESULT.json |
| 부모 기록 |새root/future_parent_001 |
| 실제 승인 예정 경로 |새root/future_authorizations/normal30_001.json |
| 별도 검증 release 예정 경로 |새root/future_authorizations/VALIDATION_RELEASE.json |
| 사용자 결정 예정 경로 |새root/future_authorizations/USER_DECISION.json |

위 future_* 디렉터리/파일은 이번 작업에서 생성하지 않았다. 전달 ZIP의 candidate 사본을 실행 경로로 대체하지 않는다. cwd는 기존 C2 환경 계약 때문에 원래 경로를 유지하며 새 source가 그 위치에 섞이는 것은 아니다. COMSOL은 새run에서만 실행하는 후보 배열이다.

## 향후 사용자 승인과 release의 결속

1. 변경부 검증에 사용된 **최종 manifest 바이트와 동일한 후보**를 고정한다. 검증 결과 파일과 필요한 현 정책 경로 확인의 식별을 보존한다.
2. 실제 native 승인 전에는 source/contract의 approved=false/usable=false를 수정하지 않는다. 실행 때 별도 manifest-bound 승인·release를 소비하는 기존 방식을 유지한다.
3. 별도 승인 파일은 run_id/manifest, approved=true, native30_one_shot=true, allow_policy_changes=false, effective_policy_unverified_accepted=true, 계약과 정확히 같은 commands/budgets, USER_DECISION 식별, VALIDATION_RELEASE 식별, 정확 default_prefs_identity를 필요로 한다. **현재 이 값들을 활성 파일로 작성하지 않았다.**
4. release는 changed_branch_validation=PASS, native_permission_route_reviewed=true, manifest_bytes_unchanged_since_validation=true와 빈 배열이 아닌 실제 검증증거 식별을 필요로 한다. 기존1198 시험/승인으로 새 변경부를 PASS라고 채우지 않는다.
5. 고정 사용자 PowerShell5.1 NoProfile 전경 경로와 같은 Python 프로세스의 fresh 두 입력을 유지한다. AI 입력/붙여넣기 자동화/별도 check-only 반복/정책 우회는 없다.

## 정책

1198에서 통과한 policy-unchanged fresh 생성 경로를 재사용한다. 실행 시 승인된 정확 default prefs 바이트를 읽고 전용 폴더에 복사하며 보안값 변경0·기본파일 불변을 확인한다. Java stdout과 `m.save("axes_generated.java","java")`의 쓰기는 이전에 실제 사용된 각각의 경로다. 현재후보의 native 성공/실효정책을 미리 확인했다고 쓰지 않는다.

현재 파일 값이 이전 근거와 달라지면 실행 전에 멈춰 보고한다. All files 전환이나 관리자로 변경하거나 ACL/registry/설치INI를 고치는 fallback은 없다. 기존 일반 정책 진단이나 입력 진단을 새 필수 시험으로 반복하지 않는다.

## 최종 수용

부모 `-NoExit`는 그대로다. 수용 경계는 local decision + final boundary + 실제 반환문 + 사용자의 프롬프트 복귀 관측이다. native/analysis의 실제 자식 rc를 확인하되 바깥 PowerShell OSrc를0으로 채우지 않는다. 최종경계/해시/오류/시간이 누락되면 전체 수용은 미완이다. 다음30초 승인 초안에 이 차이를 명시했다.
