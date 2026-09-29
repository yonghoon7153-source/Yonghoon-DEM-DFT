# 믹서 고-Bo LH — 8차 사전등록 리뷰 증거

- 판정: 현재 발사 **HOLD**. 확인 18런 선행·선택적 감도 6런 후행이라는 순서 자체는, 두 고정 유한 수치 수준의 결과만 주장한다는 조건 아래 수용 가능.
- 본문: `review.md`. Q1~Q7, HBR7-01~06 상태, 신규 HBR8-01~04, 최소 교체 문안과 해제 목록을 포함한다.
- 결과 데이터가 아닌 사전등록 구조 검토다. 실제 DEM·MPI·스케줄러·원격 서버·실제 캠페인 수치에 접근하지 않았다.
- 생성기는 기존 고정 소스의 산술 함수를 호출했고 덱 문자열은 메모리에서만 계산했다. 실행용 덱을 만들거나 제출하지 않았다.

## 자료 구분

| 파일 | 의미 |
|---|---|
| bundle_original.md | 사용자 첨부 원문 바이트 그대로 |
| bundle_lf.md | 행 번호 대조본. 이번 입력은 이미 LF라 원문과 해시 동일 |
| prereg_v22_extracted.md | PART 2 v2.2만 원문에서 추출. 245행, 묶음 69행부터 |
| baseline/ | 이전 7차 증거의 고정 소스·판정문. 이번 미제출 구현을 대신하지 않음 |
| audit_round8.py | 표준 Python만 쓰는 감사 재현 |
| audit_results.json | 15개 assertion 및 원문 핀·CED·관측 시계·합성 반례·비용 산술 |
| MANIFEST.json | 동봉 파일별 SHA256·길이 |
| package_evidence.py | 고정 허용목록으로 패키지 생성·CRC 및 파일 해시 검증 |
| SOURCES.md | 원문·고정 소스·외부 1차 자료와 검증 한계 |

판정문의 B:행은 bundle_lf.md, P:행은 prereg_v22_extracted.md다. P:1=B:69. 판정문의 로컬 절대 링크는 작성 환경용이며 ZIP 수신자는 동일한 이름의 동봉 파일을 참조하면 된다.

## 재현

증거 폴더 안에서:

```bash
python3 audit_round8.py
```

필요 라이브러리는 표준 라이브러리뿐이다. 감사 프로그램은 정규화 원문·추출 문서·audit_results.json만 이 폴더 안에서 재생성한다. 성공 시 assertion 15 PASS/0 FAIL이며, 이는 **초안 승인 15건**이라는 뜻이 아니다.

독립 확인 후 패키지를 재작성하려면:

```bash
python3 package_evidence.py
```

상위 폴더의 `codex_mixer_highbo_round8_prereg_20260929.zip`을 덮어쓴다. 실제 제출물이나 실행 상태는 건드리지 않는다.

## 주요 핀

- 첨부 SHA256: b7caae05802ac9a93c13fed4c83b303eece0a224f432b273d10a5ca1ae57c231
- 추출 v2.2 SHA256: ab20ef775f3e6bdb660f82f36a15b18a3c7cb0d0f85a6881d840b1b2171dff44
- 기준 생성기 commit: 18787ab98a13361c37b2343bd07ae276142d0953
- 기준 생성기 Git blob: 033fac54d73566ac1dad54f24cc28b9d0510ccbc

신규 구현·실측 성능·실제 궤적·최신 원격 HEAD의 인증은 포함하지 않는다. 합성 반례의 d/r/t는 실제 관측이 아니고, 비용의 런 시간은 저자 제시 가정이다.

