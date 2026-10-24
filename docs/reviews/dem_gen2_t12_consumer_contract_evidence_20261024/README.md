# T12 준비 증거 — 고정 P1 소비자 (2026-10-24)

상위 문서: `docs/reviews/dem_gen2_t12_consumer_contract_20261024.md`.

- `source-manifest.json`: ULPR 고정 핀과 실행에 필요한 5개 모듈·params의 실제 Git blob SHA256. 소스 신원 증거다.
- `p1-consumer-contract.json`: 그 params에서 재발췌한 기존 P1 계약과 현재 RESUME 승인 의미. P2 등록이 아니다.
- `factual-input-form.blank.json`: 기준 핀을 갱신한 빈 사실 수집 양식. 실제 입력·판정·등록은 null이다.
- `fixture-results.json`: `python3 -I scripts/test_dem_gen2_t12_consumer_contract.py`의 직접 실행 JSON. 소스 hash 확인 후 실제 소비 함수 41개 사례의 기대·관측 결과를 담는다.

합성 관측 범위의 PASS와 실제 연구 자격을 분리한다. `physical_ready=false`, P2 T12는 `NOT_RUN`, 물리 실행 0건이다. 이 검사는 공용 155개 검사나 CI에 자동 등록하지 않았다. 별도 독립 리뷰·전체 게이트 결과는 이 직접 검사 영수증으로 대신하지 않는다.
