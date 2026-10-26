# T12 외부 검토 반환 묶음 (2026-10-26)

먼저 `codex_review_dem_gen2_t12_consumer_20261026.md`를 읽는다.

- 입력 핀: bffc42cab29da37b45f8a713e30e8572b91e7da3.
- 소비자 핀: 4c29705fa1c4ba94737a858b206fa4f4c5bb2bde.
- 판정: 설계/관측 해석 범위 한정 수용. 자동 fetch 방지 계약 T12R-01(P2) 수정 필요. 실제 P2 T12 NOT_RUN / 물리 GO 없음.
- `snapshot/`: 제출 194항목 원문(수정 없음). 그 저장소 파일 190개는 원격 핀 blob과 대조.
- `consumer/`: 실제 검증한 고정 소비자 여섯 파일. SHA256/원래 Git 객체 ID로 확인.
- `evidence/`: 원격 대조, 실제 재현, 반례 trace. 과거 155는 제출 로그 감사이며 새 실행 아님.
- `review_scope.json`: 범위별 판정; 물리 실행 영수증으로 전용하지 않음.
- `MANIFEST.sha256`: 이 반환 ZIP의 파일 내용 봉인.

새 디렉터리에 펼친 뒤 Python 3 + Git으로 재현:

```bash
python3 -I -X utf8 -B reproduce_review.py --output ./fresh_review_replay
```

Git source objects는 원본 객체 metadata와 consumer blobs로 새 검토 폴더 안에 재구성한다. 기존 리포의 브랜치/인덱스를 바꾸지 않는다. promisor 반례의 Git remote는 file 프로토콜의 로컬 빈 bare 저장소뿐이다. 네트워크 요청이나 시뮬레이션을 요구하지 않는다. Windows 자식 Python은 UTF-8 옵션만 보정한다.

실행 뒤 같은 출력 폴더를 재사용하지 않는다. 기존 증거를 덮어쓰지 않도록 새 이름을 준다. `intake.py`는 원래 Downloads 첨부를 사용한 최초 반입 감사 스크립트여서 전체 재현의 필수 단계가 아니다. 공유 Git objects에 대한 과거 탐색이 아니라 반환 폴더의 offline objects를 사용한다.
