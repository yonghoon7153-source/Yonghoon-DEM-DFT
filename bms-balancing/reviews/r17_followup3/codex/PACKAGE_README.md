# R17 후속 3차 리뷰 전달본

- `R17_FOLLOWUP3_REVIEW.md`: 판정·새 반례 세 건·이전 여섯 조건의 수용 범위.
- `CLAUDE_REPLY.md`: 그대로 전달할 회신.
- `TEST_STATUS.md`, `TEST_RESULTS.json`, `full.xml`, `full.stdout.bin`, `full.stderr.bin`, `full.json`: Windows 전수 실측과 trace 분류.
- `REPRO_RESULTS.json`: 원래 47 case 재실행. `PRODUCER_READER_RESULTS.json`: 실제 합성 producer/reader와 cycle 제거 대조군.
- `NEW_FAST_RESULTS.json`: 새 정적 GC·receipt 반례 및 별도 추가 관측. `NEW_PRODUCER_RESULTS.json`: 실제 starts 1/2 합성 계산·reader 비교.
- `OBSERVATION_CHECK.json`: 저장된 관측의 일치 검사. 제품 전체 GO 또는 독립 replay 인증이 아니다.
- `IDENTITY.json`/`FINAL_IDENTITY.json`: 대상 full SHA·소스 식별·전후 보존·clean status. `reviewed_source/`는 읽은 소스의 사본이며 설치용 프로젝트가 아니다.
- `EXECUTION_NOTES.md`: 리뷰어 wrapper 인코딩 오류, 잘못 작성한 최초 probe 호출, 환경 제약을 별도 기록.
- `repro_followup2.py`, `repro_producer_reader.py`, `repro_followup3.py`: 아래 명령으로 별도 checkout에서 재현한다. old 두 스크립트는 이전 리뷰와 바이트가 같다. 테스트/패키지 의존성이 설치된 Python 필요.

```text
python repro_followup2.py --target <checkout>/bms-balancing
python repro_producer_reader.py --target <checkout>/bms-balancing
python repro_followup3.py --target <checkout>/bms-balancing --part fast
python repro_followup3.py --target <checkout>/bms-balancing --part producer
```

스크립트는 자신의 디렉터리 아래 새 합성 fixture를 만든다. GC는 그 새 fixture의 파일만 삭제한다. 제품 checkout 수정, 실제 원자료 적합, commit/push는 하지 않는다. 스크립트 rc 0은 진단 완료이지 제품 승인 값이 아니다.

`run_review.py`/`summarize_checks.py`/`build_package.py`는 이번 PC의 작업 디렉터리 배치를 사용하는 기록/포장 도구다. 다른 PC에서는 재현기 네 명령을 우선 사용한다. Windows 전수 실패 수를 Linux 결과로 바꾸거나 모두 신규 코드 결함으로 세지 않는다. 합성 producer 직렬화를 Linux 잠금/게시 CLI 검증으로 확대하지 않는다.

manifest는 모든 payload 이름·크기·SHA를 다루며, 외부 영수증은 ZIP 바이트 식별을 담는다. 해시 검사는 전달 무결성 검증이지 해당 코드의 정확성 또는 실행 자체를 암호학적으로 인증하는 장치가 아니다.
