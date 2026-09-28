# 사용자 결정·승인·검증 release 대응 — 비활성 명세

이 표는 원 candidate_entry.permission이 읽는 필드와 출처다. **실제 승인/release/USER_DECISION/token 파일은 만들지 않았다.** 아래 true/PASS 값은 별도 사용자 승인 뒤에만 작성할 예정 값이며 현 manifest/contract는 false 그대로다. 추가 보안 권한을 플랫폼이 허가했다고 표현하지 않는다.

| 대상 필드 | 승인 후 예정 값 | 근거/한계 |
|---|---|---|
| approval.code_manifest_sha256, release.code_manifest_sha256 | 0c14c4f886d53398fc4869db117577066b821837cd3593a6727e2ac4d0a63c45 | 원 R1 manifest와 현재 대조 |
| 두 파일의 run_id | guard1198_candidate_001 | CONTRACT와 일치 |
| approval.approved / native1198_one_shot | true / true | 향후 사용자의 이번 단발 명시 승인 원문만 근거. 현재 미작성 |
| approval.allow_policy_changes | false | 기본/전용 security 정책 변경 없음 |
| approval.effective_policy_unverified_accepted | true | 사용자가 승인문에 명시된 미확인 위험을 수용한 뒤에만 |
| approval.commands | CONTRACT.commands와 정확한 객체 동일 | compile/batch argv만; 부모/분석은 별도 COMMAND_MAP 고정 |
| approval.budgets_seconds | CONTRACT.budgets_seconds와 정확한 객체 동일 | preflight180, compile_batch1800, cleanup120, analysis600, delivery300, overall3000 |
| approval.default_prefs_identity | 아래 현재 관측 객체 | 실행 시 재해시 불일치면 중지 |
| approval.user_decision | 미래 사용자 결정 원문 path/bytes/SHA | 승인 경로의 부모 future_authorizations 아래 새 파일. 아직 없는 바이트/hash를 만들지 않음 |
| approval.validation_release | 미래 release 파일 path/bytes/SHA | 승인 후 release 생성→그 실제 바이트 식별→approval 연결 순서 |
| release.changed_branch_validation | PASS | 수용된 26군·78사례, 시험 재실행 없음 |
| release.manifest_bytes_unchanged_since_validation | true | 현재 봉인 일치 및 승인 후 준비 시 재확인 |
| release.native_permission_route_reviewed | true | 현 정책·주체별 경로·미관측 경계를 검토했다는 뜻. native 허가/성공 실측이 아님 |
| release.validation_evidence | PROPOSED_EVIDENCE_REFERENCES.json의 개별 ref 목록 | 원 검증 ZIP/결과/봉인/수신 수용/현재 관측/경로/승인문에 결속. 작성 직전 해시 재확인 |

기본 prefs 예정 identity:
```json
{
  "path": "C:/Users/BML/.comsol/v63/comsol.prefs",
  "bytes": 22252,
  "sha256": "064d190077d7533f9fff22b61460d377cb53fb314e5c0f32a0bd02e3fa28b651"
}
```

정확 승인 경로: `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/guard1198_limited_validation_R1_20260928/future_authorizations/guard1198_001.json`.

정확 release 경로: `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/guard1198_limited_validation_R1_20260928/future_authorizations/VALIDATION_RELEASE.json`.

사용자 결정→원문 파일 식별→현재 증거 목록과 검증 release→release 바이트 식별을 승인파일에 연결→부모/entry의 기존 검사 순서로 진행한다. 새 정책 보고서 식별은 release.validation_evidence에 들어가므로 별도 소비되지 않는 임의 승인 필드로 대체하지 않는다. 원 소스/계약을 재봉인하지 않으며, release true는 문서검토 완료를 런타임 실효정책 PASS로 승격하지 않는다.

문서 스냅샷 이후 source/정책/증거 식별이 달라지거나 예약 경로가 생기면 이 표를 임의 갱신해서 실행하지 않는다. 해당 차이를 보고한다. 승인 파일을 미리 만들어 기존 실행 실패를 지우거나 테스트 fixture 승인을 재사용하지 않는다.
