# 세미나 v3 재검토 전달 묶음

2026-10-13. 최종 판정은 `codex_review_seminar_v3_recheck_20261013.md`이다.

**조건부 GO — 원본 무수정 승인이 아니다.** 발표 전 출처와 해석을 고칠 항목, 영어 교체 문구, 수치 검산을 판정문에 구분했다. 원본 PPTX/PDF와 리포 코드·시뮬레이션은 수정하지 않았다.

## 구성

- `input/`: 사용자가 보낸 ZIP의 추출 사본. PPTX/PDF는 변경하지 않음.
- `renders/`: 제출 PDF를 독립 렌더한 17쪽. PowerPoint 앱 자체 렌더는 아님.
- `evidence/`: 본문·발표 노트 추출, 저장 수치 재계산, 원자료 식별 기록.
- `sources_code/`, `sources_mixing/`, `notes/sources/`: 검산에 사용한 저장 코드·판독 자료 사본. 새 실험 결과가 아님.
- `notes/audit_root.py`, `audit_charts.py`, `audit_mixing.py`: 아래 세 재현기. 표준 Python만 사용하며 시뮬레이션과 그림 생성기를 호출하지 않음.
- `inspect_delivery.py`: 최초 추출·이전 판 대조의 환경별 기록. 외부 입력 경로가 있으므로 아래 재현에는 불필요.
- `package_manifest.json`: 묶음 내 파일별 SHA-256. 매니페스트 자기 자신은 제외.

중간 분야별 검토 메모는 전달 묶음에서 제외했다. 최종 판정문을 읽으면 된다.

## 재현

압축을 푼 `seminar_recheck_v3_20261013` 폴더에서:

```bash
python notes/audit_root.py
python notes/audit_charts.py --save
python notes/audit_mixing.py --save
```

첫 재현기는 현재 덱에 지적한 표현이 존재하는지도 검사하므로, 전부 true라는 출력은 덱의 무결점 승인이 아니다. 숫자 재현은 저장 판독 자료의 산술 검증이며 원 입자 덤프의 재판독·솔버 재실행이 아니다.

원 제출 ZIP의 SHA-256:
`ad85809cee600a8ed7300ceee04797ff1bf23f37fbd7d45e12d294093423c72d`

자료 조회 핀: `a0439bdf8156236f454bd3f8b5bf4d044e127039`.
문헌 자산 조회 핀: `6e568c4f0bb7df299959fd0e77e349838ad8ac98`.
제출물 자체의 정체성은 판정문에 기록한 PPTX/PDF 파일 해시로 고정한다.
