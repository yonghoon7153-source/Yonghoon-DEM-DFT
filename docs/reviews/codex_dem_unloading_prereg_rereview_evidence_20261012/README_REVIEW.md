# DEM 언로딩 개정 1 재검토 묶음 (2026-10-12)

판정 정본: `codex_review_dem_unloading_prereg_rereview_20261012.md`.

결론: 문서 부분 수용 · 키트 개발 가능 · 본 R/10:0 이완 연장/개발·생산 U HOLD.
새 지적: ULR1-01·02 P1, ULR1-03·04·05 P2. 기존 UL-01–10의 문서 닫힘과 실행 검증을 구분했다.

## 핀

- 프로젝트: `3409814a3b6e024d6b5c7d2918aa29494b642ae1`
- LIGGGHTS: `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`
- 첨부 두 파일은 해당 프로젝트 핀과 바이트 단위로 같다 (`evidence/pin_receipt.json`).

## 구성

- `submitted/`: 사용자가 제출한 두 문서의 그대로인 사본.
- `source/`: 핀의 프로젝트 파일 97개. SHA256 및 Git blob SHA를 검증했다.
- `upstream/`: 고정 LIGGGHTS 소스 37개. SHA256 목록 포함.
- `probes/ulr_state.py`: 문서의 선택·상태·TIMEOUT·괄호 반례, 유한 합성 산술.
- `probes/ulr_observers.py`: 관측 함수·단위·창·샘플·표면 규약의 합성 산술.
- `probes/reproduce.py`: 위 두 출력과 보존 JSON 재대조, 모든 소스 SHA 및 일정 검사.
- `evidence/`: JSON 증거와 실행 영수증.
- `notes/`: 독립 검토 보조 노트. 통합 판정·심각도·ID는 최종 보고서가 우선한다.
- `prepare_sources.py`, `tree.json`: 자료 확보 경로·핀 목록. 오프라인 재검산에는 불필요.
- `CONTENTS_SHA256.json`: 아래 생성된 묶음 파일 목록. 이 목록 자체는 해시 대상에서 제외.

## 오프라인 재현

Python 3.12, 표준 라이브러리만 사용. 압축을 푼 묶음 루트에서:

```text
python -X utf8 -B probes/ulr_state.py
python -X utf8 -B probes/ulr_observers.py
python -X utf8 -B probes/reproduce.py
```

`reproduce.py`는 `evidence/reproduction.json`을 현재 환경 정보로 다시 쓴다. 다른 파일은 수정하지 않는다.
환경이 다르면 해당 영수증의 바이트 해시만 달라질 수 있다. 두 반례 출력 및 소스 해시 대조는 그대로 수행한다.

DEM/MPM, ibb/WSL, 실제 언로딩 키트는 실행하지 않았다. 생산 소스·원장·사전등록·Git 상태도 변경하지 않았다.
합성 반례 PASS와 소스 무결성 PASS는 생산 GO나 실제 회복 측정 결과가 아니다.
보고서의 LIGGGHTS 덤프 명령은 고정 소스로 검토한 **키트 시험 후보**이지 실행 검증한 제출 덱이 아니다.
