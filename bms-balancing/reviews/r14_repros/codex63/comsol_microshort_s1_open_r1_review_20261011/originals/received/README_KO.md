# OPEN-R1 전달 묶음

N1–N3 오프라인 정정·정적 재봉인 결과다. 먼저 REPORT_KO.md, DECISION.json, CODE_MANIFEST.json, LIMITED_VALIDATION_PLAN.json을 읽는다. 기능 검증과 native 실행은 미수행·미승인이다.

새 비활성 파일은 candidate에 있고, 바뀌지 않은 전체 원준비본과 R1 의존부는 basis/prior_preparation에 원바이트로 보존했다. 원본 문서의 상대 evidence/reference 경로는 그 원준비본 폴더를 기준으로 읽는다. 이번 경로 대응은 REVISION_BINDING.json과 FUNCTION_SPANS.json을 따른다. 과거 문서의 수용/시각/개수는 과거 범위이며 이번 결과로 소급 변경하지 않는다.

ZIP 밖 DELIVERY_RECEIPT.json, FINAL_PACKAGE_TOOL_RETURN.json, FINAL_SUBMISSION_CHECK.json, FINAL_CHECK_TOOL_RETURN.json은 포장 뒤에 생긴 별도 기록이다. 검토 시 함께 전달한다. 실제 마지막 반환은 해당 도구 호출의 시점과 전사 시점을 구분한다.
