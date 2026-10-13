# 연구세미나 v3.1 종결 검토 묶음

최종 판정문: `codex_review_seminar_v31_closure_20261013.md`

**GO.** 현재 제출된 17장 v3.1 발표물의 SEMV3-01–10을 닫는다. 연구 모델의 검증 완료나 시뮬레이션·생산·배포 승인이 아니다. 원본 PPTX/PDF는 변경하지 않았다.

## 파일

- `input/`: 제출 ZIP의 원본 추출 사본. PPTX/PDF·그림·요청서 포함.
- `renders/`: 제출 PDF의 독립 렌더 17쪽.
- `evidence/`: 실제 내용 추출, v3 대비, 직접 계산한 동일성·수치 검사 기록.
- `evidence/numeric_inputs/`: 이전 검토에서 보존한 원 판독 자료 등 필요한 입력 19개. 재시뮬레이션 결과가 아님.
- `notes/audit_numbers.py`, `audit_closure.py`: 독립 재현기.
- `package_manifest.json`: 파일별 SHA-256. 자기 자신은 제외.

중간 담당자 메모는 전달 ZIP에서 제외했다. 입력 ZIP에 원래 동봉된 Python 캐시는 원본 사본의 완전성을 위해 보존했지만 실행하지 않았다. 최종 판정문과 재현 증거를 읽으면 된다.

## 재현

압축을 푼 검토 폴더에서 Python으로:

```bash
python audit_closure.py
python notes/audit_numbers.py
```

필요 라이브러리: Pillow, pdfplumber. 제작자 코드·selftest·시뮬레이션은 실행하지 않는다. 최초 추출 기록인 `inspect_closure.py`는 당시의 외부 ZIP·이전 검토 폴더를 참조하며 위 두 재현기의 필수 의존성이 아니다.

이전 수치 원자료 조회 핀: `a0439bdf8156236f454bd3f8b5bf4d044e127039`.
문헌 메타데이터 조회 핀: `6e568c4f0bb7df299959fd0e77e349838ad8ac98`.
이번 제출 파일의 정체성은 최종 판정문의 SHA-256으로 고정한다.
