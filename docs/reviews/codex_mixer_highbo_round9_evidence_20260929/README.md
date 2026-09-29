# 믹서 고-Bo LH — 9차 문서 리뷰 증거

판정문은 `review.md`다. 범위는 v2.3 문서 해제와 DEV-ONLY 7런의 착수 조건이다. 실행 승인이나 새 생산 코드 감사가 아니다.

핵심:
- 새 P1 없음.
- HBR8-01의 핵심 전이 충돌 해소. §0 옛 효과 설명 등 잔여 문구는 부분.
- HBR8-02의 v2.3 정의, HBR8-03의 현재 별도 fresh 계획, HBR8-04의 비용 범위 고지는 문서상 닫힘.
- DEV7에는 soft가 없으므로 soft 범위 미정이 직접 차단 사유는 아님. 실제 개발 경로 기술 증거는 여전히 필요.
- 확인 soft 시작 전 범위·처리 규약을 봉인. M 비열람만으로 QC를 본 후 문턱 선택이 허용되지는 않음.
- 실제 확인 18런의 HOLD를 해제하지 않음.

## 핀

- 첨부: 104,185 bytes, SHA256 9b1e142cfcc67b54f43ba0586b7b5835f1dd87f65000486637814334be43f2c6
- 요청서: 60행, SHA256 504c97f5bc5c6e6c64e0fd1e2fe2f1edc0477e4de94705920af49caf504573b8
- v2.3: 294행, SHA256 e7311197509268b9302708847ac00d19daa68fa4fb09232e74908524cada080c
- 앞서 대화의 291행판이 아닌 위 첨부판을 심사했다.
- P:행 = prereg_v23_extracted.md, B:행 = bundle_lf.md. B=P+67.

## 재현

표준 Python만 필요하다.

```bash
python3 audit_round9.py
```

문서 추출물, submitted_v22_to_v23.diff, audit_results.json을 이 폴더에서 재생성한다. 20개 assertion은 문서 핀·diff 적용·명시된 기준 모델과 합성 반례를 검사한다. **제출된 생산 코드의 20개 테스트가 아니다.**

동봉 diff를 별도로 보존한 v2.2에 직접 적용해 v2.3와 바이트 단위로 같은지 확인한다. 새 원격 커밋 동일성이나 생성기/런처 실행 성공을 인증하지 않는다.

```bash
python3 package_evidence.py
```

상위 폴더의 codex_mixer_highbo_round9_prereg_20260929.zip을 덮어쓰고, 파일별 SHA256·CRC·구성원을 검증한다.

## 구성과 제한

- baseline/: 지난 8차의 문서·판정·감사 수치 보존본. 새 코드가 아님.
- review_status.json: 문서/실행 상태를 분리한 **권고**. 실제 findings.json을 변경하지 않음.
- SOURCES.md: 출처와 증거의 범위.
- MANIFEST.json: 동봉 파일 해시. 자기 자신은 제외.

판정문의 로컬 절대 링크는 작성 환경용이다. 다른 환경에서 ZIP을 읽으면 같은 이름의 동봉 파일과 P/B 행 번호를 참조하면 된다.

DEM·무입자 DEM·MPI·ibb·스케줄러·생산 코드·Git 변경 명령 실행 없음. 추가한 것은 검토 문서와 감사 증거뿐이다.

