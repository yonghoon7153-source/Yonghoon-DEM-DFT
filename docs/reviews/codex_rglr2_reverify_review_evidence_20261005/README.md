# 재검증 전달 묶음

판정은 `codex_review_rglr2_reverify_20261005.md`, 새 발견은 `findings_review.json`에 있다.
대상은 `11fcf91e8a1f4837b83892b7e4a81125eaeee4e5`의 검증된 부분 스냅샷이다.
생산 저장소·원장·실행 중인 배치는 변경하지 않았다.

- `source/`: 고정 핀의 456개 파일. 전체 리포나 설치 환경이 아니다.
- `probes/`: 독립 반례·경계 시험과 과거 비교용 함수.
- `evidence/`: 실제 시험 결과·로그·현재 결과가 참조한 합성 fixture.
- `inputs/postpin_wsl.md`: 핀 이후 제출자의 WSL 요약. 독립 실행 증거와 구별한다.
- `source_manifest.json`: 원 Git blob 해시 및 SHA-256.
- `package_manifest.json`: 전달 파일의 길이·SHA-256. 자체 파일은 목록에서 제외한다.

외부 Python 라이브러리는 포함하지 않았다. 의존 버전은 `environment.json`을 참조한다.
시험 실행 명령과 대역 사용 범위는 판정문 §2·§9에 있다.
기존 로그의 절대 경로는 당시 실행 위치이며, 새 시험은 현재 묶음 위치에서 fixture를 만든다.
`verify_delivery.py`는 전달 파일을 읽기만 하여 해시를 검산한다.
이 묶음의 무결성은 실제 194 생산 결과의 봉인·성공을 보증하지 않는다.
