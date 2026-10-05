# REIL 부속 C 기존 판정 — 독립 교차검토 전달 묶음

2026-10-05. 원 입력 `REIL_V2_ANNEX_C_REVIEW_20261005.zip`의 기존 판정을 재검토했다. 원 판정문을 수정하거나 그대로 새 검토로 제시한 것이 아니다.

- `REIL_V2_ANNEX_C_CROSSREVIEW_20261005.md`: 독립 판정, 수치 반례, Q1–Q5, 수정 문구.
- `REPLY_KO.md`: 전달용 짧은 회신.
- `DECISION.json`: 기존 finding 타당성, 수정 상태, 실행 권한을 분리한 기록.
- `independent_document_checks.py`: 연구 코드를 실행하지 않는 문서·합성 산술 검사.
- `evidence/intake.json`: 원 ZIP·8개 문서·PDF의 식별 및 읽기 범위.
- `evidence/remote_identity.json`: 고정 커밋 GitHub 조회로 확인한 문서 식별값.
- `evidence/independent_checks.json`: 이번 63개 독립 검사 결과. REIL 기능/실측 데이터 검사가 아니다.
- `input_bundle/`: 원 ZIP의 8개 파일을 그대로 보존. 그 안의 판정은 입력 증거다.
- `PACKAGE_MANIFEST.json`: 이 전달 묶음의 파일별 SHA-256.

재현은 Python 표준 라이브러리만 필요하다. 묶음 루트에서:

```bash
python independent_document_checks.py --out evidence/reproduced_checks.json
```

기본 60개 검사. 직전 부속 B 검토의 `RECEIVED_SNAPSHOT.json`을 `--prior-snapshot <경로>`로 주면 바이트 비교 3개가 추가된다. 그 입력은 이 묶음에 포함하지 않았다. 이번 결과에는 해당 별도 입력으로 실행한 63개가 기록돼 있다. 출력 JSON은 지정 경로에 새로 쓰므로 기존 증거와 다른 이름을 사용하는 것을 권한다.

논문 본문·보충의 해시 및 쪽수는 검토서에 있다. PDF 원문, 전체 텍스트 추출물, 렌더, 연구 데이터/코드, 노트북은 배포하지 않는다. 문헌 판단은 자동 검사의 PASS로 대체하지 않는다.

최종 상태: 기존 P2 세 건 타당, 새 P1 미발견, 세 수정 미확인, 실행 승인 없음. 원문 수정·원격 쓰기·외부 발송 없음.
