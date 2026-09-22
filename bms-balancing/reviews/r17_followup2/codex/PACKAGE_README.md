# R17 후속 2차 검토 전달본

판정은 R17_FOLLOWUP2_REVIEW.md, 전달용 회신은 CLAUDE_REPLY.md를 먼저 읽는다.
TEST_STATUS.md는 독립 실측과 Windows 환경 차이, EXECUTION_NOTES.md는 중간 실패·재실행 범위다.

재현 대상 full SHA: `a4c311eff898615932ae6f333bbb26b605abf762`.

```text
python repro_followup2.py --target <고정 HEAD의 bms-balancing 경로>
python repro_producer_reader.py --target <같은 경로>
python verify_observations.py
```

대상의 Python 테스트 의존성이 필요하다. REVIEW_IDENTITY.json에 이번 실제 버전이 있다.
verify_observations의 성공은 **결함을 포함한 관측의 일치**이며 소프트웨어 승인 신호가 아니다.
대상 checkout의 파일은 수정하지 않는다. GC가 삭제하는 파일은 새 synthetic fixture 안의 파일뿐이다.

원시 자료:

- REPRO_RESULTS.json 및 case별 log: 47 case의 명령·반환값·관측.
- PRODUCER_READER_RESULTS.json / producer_reader.log: 실제 합성 producer API와 reader 불일치.
- OBSERVATION_CHECK.json: 63개 관측 조건.
- focused_scoped/full_scoped log·xml·json: 독립 pytest 결과. *_failures.json은 XML에서 도출한 분류 자료.
- FULL_TEST_DELTA.json: 이전 Windows 실패 집합과 비교. 이전 raw 자료 전체를 다시 포함한 묶음은 아니다.
- source_snapshot/: REVIEW_IDENTITY에 명시한 검토 파일의 실제 checkout 바이트. blob 및 줄바꿈 구분은 identity 참조.
- producer_fixture/: 마지막 합성 API 재현 입력·CSV·sidecar. 실험 셀 원자료가 아니다. 절대경로가 들어 있는 meta는 당시 관측이며 재현할 때 새로 발행한다.

PACKAGE_MANIFEST.json은 자신을 제외한 정확 payload 집합·크기·SHA256이다.
ZIP 전체 식별 영수증은 ZIP 밖 PACKAGE_RECEIPT.json이다. 수신 검증을 대신하지 않는다.
본 묶음은 COMSOL/Gate 실행 승인이나 실데이터 재적합 승인 문서가 아니다.
