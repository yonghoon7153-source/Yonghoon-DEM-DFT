# 프로젝트 규약 (이 브랜치 — 건식 후막 bimodal 전고체 복합양극 실험 파트)

## 정체성 / 연계
- 이 브랜치 = **실험 + 2차년도 설계** 파트 (`claude/solid-state-cathode-improvement-hevry0`).
- DEM/MPM 시뮬레이션 = **`claude/stoic-knuth-NObVQ`** 브랜치. **연계하되 독립**.
- 두 모델은 cross-fit 금지 — 각자 ground truth(실험/시뮬)에 보정, 비교는 cross-validation.

## 소재 명명 (★ 항상 이 매핑 사용)
- **No.1 = NCM_2** (단결정, 매끈, Ni 82.5%, 205.9 mAh/g)
- **No.2 = NCM_3** (단결정, satellite 잔류물, Ni 86.9%, 213 mAh/g)
- **Poly = 대립** (다결정 NCM811, ~10 µm)
- NCM_1 (자체구입 5µm 응집) = **미사용**. 보고서 NCM_1/2/3 ↔ 실험 No.1/No.2/Poly 혼동 주의.
- P = Poly(대립), S = Single(소립). P:S 비율 = 대립:소립.

## 단위 규약
- 전도도 σ = **mS/cm**. (킥오프 "mS cm⁻²"는 오타 — `docs/project/05_ISSUES_AND_FIXES.md`)
- 비용량 mAh/g · 면용량 mAh/cm² · 로딩 mg/cm² · 압력 MPa · 저항 Ω(·cm²).

## 데이터 다룰 때
- 원본 PDF/docx = `docs/project/sources/` (무수정 보존). 추출 텍스트/수정값은 DB에.
- 수치는 `db/*.csv`, 서술은 `docs/project/*.md`, 문헌은 `litdb/`.
- 수치 출처(stated vs digitized-from-figure)와 측정조건(온도·압력·셀) 항상 기록.
- 모델값 vs 실측값 불일치는 발명하지 말고 `05_ISSUES_AND_FIXES.md`에 기록.

## 논문 에이전트
- PDF 업로드 후 **"논문 에이전트 실행해줘"** → `.claude/agents/litdb-curator.md` 동작.
- PDF 렌더가 안 되면 PyMuPDF로 텍스트 추출 (`pip install pymupdf`).
- digest는 `litdb/papers/<slug>.md`, 비교는 `our_experiment_baseline.md` + `our_dem_baseline.md`.

## Git
- 작업 브랜치: `claude/solid-state-cathode-improvement-hevry0`. 요청 없이 PR 생성 금지.
- 커밋/푸시는 사용자 요청 시. 모델 식별자/시크릿을 커밋에 남기지 않음.
