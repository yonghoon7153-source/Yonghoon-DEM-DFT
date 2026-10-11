# DEM 언로딩 등록 검토 — 전달 묶음

읽을 순서:

1. `codex_review_dem_unloading_prereg_20261011.md` — 최종 판정, Q1–Q6 답, 최소 수정 문안.
2. `evidence/` — 실제 함수 반례, 기존 로그 재계산, 소스식 산술, 핀·재현 영수증.
3. `notes/` — 이력 / 물리 / 설계별 상세 교차검토. 최종 등급·ID는 최종 판정문이 정본.
4. `source/` 및 `upstream/` — 핀된 원문 사본. `source_manifest.json`은 Git blob 및 SHA-256, `upstream_manifest.json`은 고정 버전 소스 SHA-256을 기록.

판정: 현재 등록안의 본 U는 **HOLD**. 새 DEM/MPM 런, ibb 실행, 원 코드 수정, Git 상태 변경 없음. 기존 기록의 후처리와 합성 산술만 실행함.

## 로컬 재현

Python 3.12.14 / NumPy 2.3.5, PowerShell 및 tar를 사용했다. 내려받기·시뮬레이터·별도 컴파일 불필요. 묶음을 푼 뒤 루트에서:

```powershell
python -X utf8 -B probes/review_counterexamples.py
python -X utf8 -B probes/recheck_original_log.py
python -X utf8 -B probes/physics_arithmetic.py --output evidence/physics_arithmetic.json
powershell -NoProfile -ExecutionPolicy Bypass -File probes/design_arithmetic.ps1
```

`python`이 WindowsApps alias이면 설치된 Python 실행 파일의 절대 경로를 사용한다. 원 실행 환경의 경로는 재현 영수증에 있다. 스크립트는 source를 수정하지 않고 evidence JSON만 재생성한다. 중력 사슬·힘 상쇄·교차 괄호·중력 팔·판 일의 수치는 합성 반례/명목 계산이며 실측 언로딩 결과가 아니다.

`prepare_sources.py`와 `probes/source_receipt.py`는 최초 확보용이며 재현에 필요 없다. `upstream_manifest.json`의 일부 404는 사용하지 않는 파일 이름 조회 기록이다. 실제 인용 파일은 모두 동봉했다. 추가 원 소스는 `notes/source_extra/`에 있으며 전체 묶음 해시 목록에 포함된다.

`review_bundle_manifest.json`은 자신을 제외한 파일의 SHA-256을 담는다. 이는 포장 무결성 증거이며 검토 내용의 과학적 타당성을 자동 보증하지 않는다. ZIP 외부의 `.receipt.json`에는 ZIP 해시와 압축 해제 검증 결과가 기록된다.
