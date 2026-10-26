# [DEM 제하] 재개 식별자 정수 파싱 보완 검토 요청 — 2026-10-24 KST

> 현재 canonical 전체 gate: **PASS, 155/0, rc 0**. [완료 기록](ulpr_resume_integer_evidence_20261024/completion.md)을 따른다. 아래 작성자/초기 반입 시점의 예정·대기 문구는 원 스냅샷의 범위이며 현재 상태를 대신하지 않는다.


사용자 “계속 진행”·“다 비준이야” 이후 기존 ULPR의 fractional RESUME k 잔여 문제를 수정했다. 이 지시는 좁은 코드 오류 수정과 검토 진행 권한이며 새 물리값·실물 결과·외부 GO를 공급한 것으로 해석하지 않았다. 기존 등록 §14-11①/§14-12의 같은 정수 경계를 확인하기 전에 반올림하던 파서 경로가 대상이다.

| 항목 | 범위 |
| --- | --- |
| 가지 | `claude/sdcp-dem-manuscript-si-pqwtv8` 기반 `codex/unloading-ulpr`; Claude 가지 commit/push 금지 |
| 기준 pin | `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3` |
| 변경 | reader·seal source·active rules·SHA256SUMS·kit README·사전등록 설명 6파일 |
| 증거 | [README](ulpr_resume_integer_evidence_20261024/README.md), [NOTE](ulpr_resume_integer_evidence_20261024/NOTE.md), [6파일 diff](ulpr_resume_integer_evidence_20261024/source/candidate.diff) |
| 파일 신원 | [source_manifest.json](ulpr_resume_integer_evidence_20261024/source_manifest.json), [package_manifest.json](ulpr_resume_integer_evidence_20261024/package_manifest.json) |
| 최종 리뷰 pin | root가 고정한 실제 커밋/외부 PIN.txt를 따른다. 본문에 자기 SHA를 예측해 쓰지 않음 |
| 전체 저장소 gate | [receipt](ulpr_resume_integer_evidence_20261024/full_gate_receipt.json)의 실제 상태 확인. 현재 전체 gate PASS (완료 기록 참조) |

다음을 반박해 달라.

1. RESUME k/step과 상태 ul_k/ul_rstep이 float 반올림 전에 원문의 정확한 비음수 정수값으로 대조되는가? 실제 소수·정밀도 손실·비유한·큰 지수·과도한 길이·Unicode 숫자/공백이 승인되지 않으며 ASCII 정수 decimal/scientific 표기는 유지되는가?
2. 같은 상태 식별자의 중복 정의나 정상 사건과 모호한 RESUME가 공존할 때 한쪽을 버려 승인하지 않는가? manifest의 잘못된 `resume_from=` 표지, Unicode 줄구분, 사건 CSV 구조 오류가 승인 증거에서 사라지는 경로가 남았는가?
3. 실제 `arm` 진입점이 잘못된 경계에서 승인 없음·미식별·null을 유지하고 입력 CSV를 바꾸지 않는가? 정상 생산 덱 모의 재개 k=0/1/2/3의 기존 상태·수치는 유지되는가?
4. 공용 `_i`/`_csv`, 생산 덱 64개, history 16개, params, 물리 기준이 바뀌지 않았으며 봉인 76파일·활성 24규칙과 R39 증인이 정합하는가?
5. 실제 원자료의 수치와 README/NOTE의 한정이 일치하고, 내부 검토·합성 fixture·모의 덱 실행·실제 CLI·전체 gate·실물 실행을 혼동하는 문구가 없는가?

최종 작성자 검증은 13개 kit 명령 모두 rc 0·0 FAIL, reader 304(기존 214 + 신규 90), 관련 R39 단언으로 검출한 변이 11개다. 별도의 독립 공격은 150/150, 독립 reader 자체시험은 304/304이며 독립 변이 2개도 각각 22개/3개 관련 단언 실패와 예외 0을 확인했다. 이 수를 합산하지 않는다.

독립 검토 중 발견된 manifest 앞 비ASCII 공백, 상태/manifest Unicode 줄구분, 사건 CSV 구조 결손의 세 우회는 먼저 실패를 기록한 뒤 수정했다. 원래 실패·당시 판·최종 재확인을 함께 보존했다. 최종 reader SHA-256 `7a395a549e8ad3eae820a9e575f094219ca7d47a4b9a07c5bc27623d7018af4b`와 diff SHA-256 `ccd610c9e7c9b3d1443edba03324a8c0fdf0bed0330f908ca7844586b293efd0`에 한정한 내부 코드 PASS다.

최종 발송·원장·공유 진행 기록 반영은 기존 인계 역할을 따른다. 이번 문서가 외부 Codex 세션 판정이나 실행 GO를 생성하지 않는다. 일반 숫자 필드 전체의 강화·모든 악성 파일 문법·실물 재개·설치 바이너리 검증은 별도 범위다.
