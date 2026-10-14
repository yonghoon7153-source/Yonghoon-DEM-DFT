# REIL C4E v2 검토 회신 전달문

고정 HEAD `dc6e5b7e043ff11b73095ddb9d60db7837e665c7`의 v2를 검토했습니다. 첨부 요청문 35,172 B / SHA-256 `a4fb202549e6f785080c0e0feab09f930a2f0afd288cb3a3e5005096dd6d8e28`은 커밋 바이트와 같습니다.

판정은 `REQUEST_REVISION_BEFORE_E0_APPROVAL`입니다. 지역 오류와 E3a 성공의 구분, 66 returned 조건, NE/reference 둘과 실제 소비 입력 결속, M1 정정은 문서상 수용합니다. 다음 세 항목만 승인문·발송문·예정 대조에 반영해 주세요.

1. §6-2 실제 fork는 기존10+새5=15입니다(상한17 유지). n3_a/n3_b는 모사 Process이고 c_8은 두 파입니다. COBYQA는 내부≤50과 독립 재평가≤1을 분리하고, util의 “몇 회”는 함수별 유한 상한으로 바꿔 주세요.
2. `final_record → 끝 sha → 판정 → 끝 기록`에서 마지막 기록 뒤의 시간·크기가 빠집니다. 끝 재해시와 마지막 쓰기·재읽기를 포함한 뒤 같은 출력 루트 크기와 최종 snapshot으로 E3a 수용을 확정하고, 9,900/10,800초의 적용 경계를 적어 주세요. 마지막 기록으로 초과하는 대조도 필요합니다.
3. active 초과 즉시 STARTED_INTERRUPTED로 확정하지 마세요. 마지막 drain에서 done을 받으면 원래 COMPLETED와 termination을 보존하고, active 초과/global_stop은 유지합니다. 마지막 drain의 늦은 완료 목록도 채우고 해당 경합 대조를 명시해 주세요.

구체 좌표와 대체 문장은 REVIEW_KO.md와 REQUEST_CORRECTIONS_KO.md에 있습니다. 이번 회신은 문서 정정 요구이며 구현·재시험·자료 반입·계산 승인이 아닙니다. 기존 시험을 다시 돌리거나 과거 관측을 보충할 필요는 없습니다. 정정 수용 뒤 사용자 E0 승인, E0 결과 검토 뒤 사용자 E1 별도 GO 순서를 유지합니다.
