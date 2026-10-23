# DEM 세대 2 비준 개정 근거 (2026-10-24)

> 현재 canonical 전체 gate: **PASS, 155/0, rc 0**. [완료 기록](completion.md)을 따른다. 아래 작성자/초기 반입 시점의 예정·대기 문구는 원 스냅샷의 범위이며 현재 상태를 대신하지 않는다.


현재 문서는 `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md`의 **§12**와 `docs/reviews/codex_dem_protocol_gen2_ratified_update_20261024.md`다. 이 폴더의 과거 사본은 현재 지시가 아니다.

- `source-provenance.json`: 지정 기준 `962caea2d1857b0e34fe724e38815661936b7183`에서 원계획·당시 요청서·기존 산술 JSON·검산 도구를 가져온 경로와 SHA256. 사본 4개는 원 blob과 바이트 동일하다.
- `plan-before-20261024.md`·`request-before-20261024.md`: 개정 전 문서 원문. 잘못된 수치와 당시 승인 대기 상태도 역사 보존 목적상 그대로다.
- `reviewed-draft-v1/`: 첫 검토 초안 원문. 이 초안의 신규 §11 번호는 원래 문헌 §11과 겹쳤다. 현재판은 신규 개정만 §12로 고쳤고, 과거 ‘비준 뒤/기존 문서 무변경’을 당시 상태로 명시했다. 기존에 커밋된 협업 쪽지를 바꾼 것이 아니다.
- `applied-replacements.json`·`plan-before-to-ratified.diff`: 본문의 날짜 표시 정정과 개정 전후 전체 차이. 머리 현재 우선 규칙과 신규 §12는 diff에 포함된다.
- `prior-arithmetic-results.json`·`prior-probe_design_arithmetic.py`·`arithmetic-replay.json`·`arithmetic-replay-receipt.json`: 기존 작은 산술/이산 제어 반례와 같은 도구의 재실행. 표준 라이브러리 도구를 이 폴더에서 `python3 -I -B prior-probe_design_arithmetic.py`로 실행하면 JSON을 stdout에 쓴다. 새 물리시험이나 실제 측정이 아니다.
- `t12-preserved-files.json`: 앞선 T12 계약·빈 사실 양식·문서 감사 8파일을 바이트 그대로 반입한 목록. T12 기능 또는 물리 준비 완료 증거가 아니다.
- `verification.json`: 원문/복사·역사 행·새 절·정정·참조·금지값 집중 검사의 범위와 결과, 별도 독립 문서 검토 상태. 문서 SHA 도달성은 root가 지정한 기준판에서 이어지는 해당 트랙을 대상으로 한다. 다른 트랙인 공유 체크아웃 HEAD에서의 차이도 기록한다.
- `independent/`: 별도 검토자의 보고서·25항 결과·검사 도구를 원바이트 보존했다. 이 PASS는 문서/기존 산술 원자료 대조에 한정하며 새 MC·물리시험·전체 게이트가 아니다. 도구의 절대 실행 경로는 당시 scratch 문맥이다.
- `full_gate_receipt.json`: 조정 작업자가 실제 통합판에서 수행한 전체 검사만 기록한다. PENDING은 미완료이며, 과거판의 PASS로 채우지 않는다.
- `MANIFEST.sha256`: 이 증거 폴더의 파일별 해시(자기 파일 제외). 최종 receipt 추가/갱신 시 조정 작업자가 새 문맥과 함께 갱신한다.

사용자 비준은 계획 정정과 제시한 검증 요구에 적용됐다. 빈 사실 양식의 실제값, Q7–Q9 실측, 새 등록, P2 생산기, 실제 서보/R-a/S0, 외부 판정, T5/T11/T12 통과를 만들어 내지 않았다.
