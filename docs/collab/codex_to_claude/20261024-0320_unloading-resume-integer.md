# [DEM 제하] 재개 식별자 정수 파싱 보완 — 2026-10-24 03:20 KST

1저자 “계속 진행”·“다 비준이야” 이후 기존 ULPR의 fractional RESUME k 잔여 문제를 기존 등록의 정수 경계 요구 안에서 수정했다. 진행 지시는 새 과학값·물리 실행·외부 GO를 채운 기록이 아니다.

작업 가지는 `codex/unloading-ulpr`, 기준 pin은 `8347d32ea678c0174bd77d4c79cfbd7b0591e4a3`이다. 최종 반입 커밋과 외부 PIN.txt는 root가 고정한다. Claude 가지와 공유 기록·원장은 직접 수정하지 않는다. reader와 봉인·설명 6파일의 실제 변경·SHA는 [검토 요청서](../../reviews/codex_dem_unloading_resume_integer_request_20261024.md)와 [증거 README](../../reviews/ulpr_resume_integer_evidence_20261024/README.md)를 따른다.

RESUME k/step·상태 ul_k/ul_rstep의 원문 정수값을 대조해 소수 반올림 승인을 막았다. 중복/모호 표지와 사건 CSV 구조 결손은 재개 승인 근거에서 조용히 빼지 않는다. 정상 ASCII 정수 표기·CRLF/CR과 기존 경계 의미는 유지한다. 공용 숫자/CSV 파서, 생산 덱·history·params·물리 기준은 그대로다.

공유 진행 기록에 넣을 제안:

> [DEM 제하 / 10-24 KST] 1저자 비준 후 기존 fractional RESUME k 파싱 오류를 좁게 보완. 최종 kit 13개 명령 모두 rc 0, reader 304/304(기존 214 + 신규 90), 작성자 변이 11개 관련 단언 검출. 내부 독립 공격 150/150와 reader 304/304 및 별도 독립 변이 2개 검출. 봉인 76파일·활성 24규칙. 실물 실행·설치 바이너리·외부 GO와 일반 숫자 필드 전체 강화는 범위 밖. 전체 저장소 gate는 실제 receipt 상태를 따름.

독립 발견 세 우회(비ASCII manifest 앞 공백, 상태/manifest Unicode 줄구분, 사건 CSV 구조 결손)는 실패 원자료와 수정 후 결과를 모두 보존했다. 작성자 11변이와 독립 2변이는 같은 총수로 합치지 않는다. 실제 arm CLI는 정상 2개 OK·잘못된 표지 8개 미식별/null이며 입력 CSV는 무변경이다. 덱 모의 재개 k=0/1은 행 전체 동등성을 주장하지 않고 최종 상태/수치의 보존만 기록했다.

현재 [전체 gate receipt](../../reviews/ulpr_resume_integer_evidence_20261024/full_gate_receipt.json)는 PENDING이며 root의 실제 반입·preflight·후보 commit·전체 gate 뒤 갱신한다. 원문 보고서는 archive와 provenance로 보존했고 live NOTE의 링크만 저장소 상대경로로 정규화했다. 원장 verified 변경이나 외부 실행 GO 제안은 없다. 최종 발송과 공유 문서 반영은 기존 인계 역할에 맡긴다.
