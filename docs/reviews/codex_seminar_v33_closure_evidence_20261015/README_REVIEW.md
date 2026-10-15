# v3.3 종결 확인 자료

먼저 `codex_review_seminar_v33_closure_20261015.md`를 읽는다.

판정: 내용 종결 GO. SEMV32-01–04·SELF-117 닫힘, 새 P1/P2 없음. 실제 발표 PC의 PowerPoint에서 3장 네이티브 수식 8개 및 두 줄 출처의 아래첨자 표시 확인은 별도 조건으로 남는다. 이 판정은 계산·발사·배포 승인이나 모델의 실험 검증이 아니다.

## 구성

- `input/`: 제출 ZIP에서 추출한 43개 파일. PPTX·PDF·원 수식 덱 및 제작자 기록. 내용 수정 없음. 이 안의 생성기·검사기는 이번 리뷰에서 실행하지 않았다.
- `baseline/`: 이전 v3.2 검토의 그림·판정문·PDF·18 PNG, 이전 검토가 보존한 LIGGGHTS 핀 `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`의 세 헤더. 복사 바이트 그대로.
- `agents/`: 독립 수식·의미·시각 검토 스크립트, 결과 JSON, 상세 메모. 증거 파일의 절대 경로는 검토 당시 환경 기록이다.
- `renders/`: 제출 PDF와 이전 PDF를 각각 Poppler 144 dpi로 렌더한 화면. PowerPoint 네이티브 표시를 대신하지 않는다.
- `evidence/`: 최초 반입 확인, 그림/패키지 독립 검사, 의미 검사 출력, 입력 보존 확인.
- `REVIEW_MANIFEST.json`: 이 전달 묶음의 파일별 SHA256. 자기 자신만 해시 목록에서 제외한다.

## 독립 재현

이 폴더를 기준으로 실행한다. Python 3에 lxml·Pillow·pdfplumber, PowerShell 7(`pwsh`), Poppler가 필요하다. 수식·의미·그림 대조는 동봉 파일만 읽는다. PDF 렌더러 경로는 `agents/visual_render.py`의 `POPPLER`를 설치 위치에 맞춘다. 실행 정책을 바꾸지 않고 허용된 런타임을 사용한다.

```powershell
python agents/equations_probe.py
./agents/semantics_probe.ps1 -Check
./agents/semantics_probe.ps1 -Compare
python figure_package_probe.py
python agents/visual_render.py
python agents/visual_metrics.py
```

기대 결과는 수식 C14N 8/8·대체 그림 8/8·일반 그림 2/2, 의미 검사 21/21, 수치/띠/빗금 유지, 이전 PDF와 14/18쪽 픽셀 동일이다. 3·7·11·15장은 의도된 수정이다. 전체 PPTX 파일이나 원 수식 XML의 직렬화 문자열까지 같다는 뜻은 아니다.

`prepare_inputs.py`는 최초 Downloads ZIP을 읽는 반입 스크립트이므로 압축 해제된 전달물의 재검증에 다시 실행할 필요가 없다. 파일별 고정값은 `evidence/intake.json` 및 본문 §2에 있다. 제작자의 `input/repo/` 검사 결과를 독립 검사 결과로 세지 않는다.

## 핀의 경계

최종 본 가지 커밋 SHA는 제출 `PIN.txt`에 숫자로 기입되어 있지 않다. 따라서 제출 PPTX·PDF·ZIP의 전체 SHA256으로 판정 대상을 고정했다. `db04a2a7a`는 제작 base이지 최종 리뷰 핀으로 인증한 값이 아니다. 반입 시 실제 커밋을 연결하되 파일이 바뀌었다면 이번 동일성 판정을 그대로 옮기지 않는다.

## 전달 검사

`package_review.py`는 제출 파일 43개의 보존 여부와 별도 첨부 PPTX·PDF·ZIP을 다시 대조하고 독립 의미 검사를 저장한다. 그 뒤 파일 목록·해시를 만들어 ZIP에 담고, ZIP CRC·멤버 집합·전체 파일 해시를 다시 검사한다. 재실행은 리뷰 증거와 ZIP만 재생성하며 제출 파일이나 리포 코드를 바꾸지 않는다.
