# B_A8R1 오프라인 배치 전달

**D01–D16 / 하위57개 첫1회 PASS, B/COMSOL 미승인.** 기존389 suite/F 재실행 없음. 실제 B 실행본은 독립 검토와 사용자 별도 승인을 기다린다.

읽을 순서: IMPLEMENTATION_REPORT_KO.md → SOURCE_DIFF.patch / STATIC_REPORT.json → deployment_01.json·completion·external 및 deployment_evidence/HOST_SUITE_RUN01.json → CODE_MANIFEST.json / PRE_TEST_SEAL_run01.json → B_APPROVAL_REQUEST_DRAFT.md.

새 Java SHA `5a9da0f9da79a6d5f848af5ee3ea9792b06918110a8fae8a54b5a4fc05db6c39`, CODE_MANIFEST `fa5592734f4d082bfc7bcb7ceaf70ec1407cd35342dadee100bf939f8297329b`. raw 계약의 준비 플래그 true는 시험 전부터 봉인됐으며 이후 바꾸지 않았다. A7/A8 원본과 선택224개 파일 전후 식별 동일. 실제 runtime/approvals/token 폴더 없음. sf/의 승인·프로세스/시간 자료는 명시적인 합성 fixture다.

경로 준비는 B 실행 승인이 아니다. contract.approved=false/usable=false를 독립 실행차단 기능으로 주장하지 않는다. 실제 승인 검증 함수 경계는 D11에서 inert로만 확인했다. 특히 TTY 사전 확인은 여전히 미완이다. 현 launcher의 TTY 검사는 apply Desktop 뒤에 있다.

주 ZIP 내부 상태는 AWAITING_EXTERNAL_FINALIZATION이다. COMSOL63_B_A8R1_EXTERNAL_FINALIZATION_20260924.zip과 그 뒤 마지막 실제 도구 rc/시간 반환을 함께 받아야 최종 전달 경계를 판단할 수 있다. 원시 도구 객체가 별도 보충되면 후속 직렬화 출처를 유지한다. 입력 MPH/원본 baseline/전체 prefs/전체 역사 ZIP은 이 묶음에 포함하지 않는다.
