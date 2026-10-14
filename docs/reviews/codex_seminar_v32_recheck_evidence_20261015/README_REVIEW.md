# 세미나 v3.2 재확인 증거 묶음

최종 판정: `codex_review_seminar_v32_recheck_20261015.md`.

2026-10-15의 읽기 전용 검토. 제출 덱·소스는 수정하지 않았다. 18장 실제 PPTX와 PDF, 핀 자료, 원로그, 독립 검산, PDF 렌더를 포함한다. 최종 판정문이 분담 노트보다 우선한다.

## 재현

Python 3, lxml, pypdf가 필요하다. 작업 폴더는 이 파일이 있는 폴더다.

```text
python inspect_deck.py
python agents/equations_probe.py
python agents/physics_probe.py --out agents/physics_probe_results.json
python final_checks.py
```

앞의 세 명령은 로컬 파일만 읽는다. 생성기·솔버·시뮬레이션을 실행하지 않는다. `final_checks.py`에는 고정 문헌 커밋 메타데이터 조회가 포함된다. 이번 판정의 문헌 핀은 `ebfed0ff5cb3ef81d386ca0575037469a824e3e5`이고, 당시 원문 사본·해시가 `external_fetched/`, `evidence/external_sources.json`에 보존돼 있다. 새 HEAD로 이번 판정을 소급 변경하지 않는다.

`prepare_sources.py`와 `verify_external_sources.py`는 별도 자료 확보 경로다. 이번에 확보한 source 사본으로 검토를 재현할 수 있으므로 필수 재실행 명령은 아니다. 리포 소스 핀은 `90ca2c8cd6766c5e5df173533a78893cec04f6c3`, LIGGGHTS 핀은 `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`다.

## 파일 구분

- `input/`: 제출 ZIP을 안전하게 펼친 사본. 제작자 검사 기록도 이 안에 있으며 독립 검증 결과로 취급하지 않는다.
- `source/`: 고정 커밋에서 Git blob을 대조한 자료. `evidence/source_manifest.json` 및 `final_checks.json`의 추가 자료 항목 참조.
- `source_upstream/`, `external_fetched/`: 고정 LIGGGHTS와 문헌 카드의 원문 사본.
- `baseline/`: 이전 종결 PPTX 및 원 고정판 이완 로그. 각각 해시로 식별한다.
- `evidence/`: 실제 제출 파일의 XML·본문·notes·차이·매니페스트·독립 산술.
- `renders/`: 제출 PDF의 독립 렌더. PowerPoint 앱 네이티브 렌더가 아니다.
- `agents/`: 분담 검토, 세부 탐침, 문헌 원문 크롭. 최종 판정에서 철회한 의심은 finding이 아니다.

입력 수식 원본 SHA `8e76819a…` 파일은 제출 ZIP에 없었으므로 포함하지 못했다. PDF의 수식은 fallback 표시이며, 실제 PowerPoint OMML 표시 점검은 발표 컴퓨터에서 남아 있다.

`REVIEW_MANIFEST.sha256`은 최종 증거 묶음의 파일별 해시다. 원 제출 파일의 매니페스트와 구별한다. ZIP의 무결성 검사와 논문·모델의 과학적 타당성은 다른 검사다.
