# T12 준비 증거 — 고정 P1 소비자 (2026-10-24)

상위 문서: `docs/reviews/dem_gen2_t12_consumer_contract_20261024.md`.

- `source-manifest.json`: ULPR 고정 핀과 실행에 필요한 5개 모듈·params의 실제 Git blob SHA256. 소스 신원 증거다.
- `p1-consumer-contract.json`: 그 params에서 재발췌한 기존 P1 계약과 현재 RESUME 승인 의미. P2 등록이 아니다.
- `factual-input-form.blank.json`: 기준 핀을 갱신한 빈 사실 수집 양식. 실제 입력·판정·등록은 null이다.
- `fixture-results.json`: `python3 -I scripts/test_dem_gen2_t12_consumer_contract.py`의 직접 실행 JSON. 소스 hash 확인 후 실제 소비 함수 52개 사례의 기대·관측 결과를 담는다.

합성 관측 범위의 PASS와 실제 연구 자격을 분리한다. `physical_ready=false`, P2 T12는 `NOT_RUN`, 물리 실행 0건이다. 이 검사는 공용 155개 검사나 CI에 자동 등록하지 않았다. 별도 독립 리뷰·전체 게이트 결과는 이 직접 검사 영수증으로 대신하지 않는다.

- `external-review-provenance.json`: old01c1 외부 정수 교정 수용·무결성 HOLD의 원본/저장본 hash. 수정판의 외부 재확인이나 GO가 아니다.

- `historical/`: 기존 41개 PASS와 old01c1의 44/52 tests-first 실패·재현 ZIP·검증 영수증을 원 bytes로 보존. 현재 직접 실행 결과는 52/52 PASS이며 수정판 외부 재확인은 대기 중이다.
- `consumer-publication-proof.json`: ULPRI 최종 전체 pin의 실제 원격 조회·push 성공 영수증. T12 가지 게시나 T12 전체 게이트 영수증이 아니다.
