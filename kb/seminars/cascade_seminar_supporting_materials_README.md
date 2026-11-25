# Cascade seminar supporting materials

- 작성 기준: 2026-08-11
- 범위: 수정 PPTX를 제외한 세미나 대본·가이드·감사 문서·그림·Origin-ready CSV·그림 재생성 코드

## 먼저 읽을 파일

1. `kb/seminars/cascade_seminar_2026_08_spec.md` — 24장 슬라이드 대본, Defense Q&A, 근거 파일
2. `docs/reviews/cascade_db_ml_readiness_audit_2026_08_10.md` — 273→47 계보와 co-doping ML 준비도 감사
3. `docs/reviews/cascade_ai_screening_literature_comparison_2026_08_10.md` — litdb figure까지 확인한 AI screening 문헌 비교
4. `docs/cascade_ml_integration_guide.md` — 실제 pair label과 active-learning loop로 확장하는 방법
5. `docs/cascade_pipeline_guide.md` — 현행 cascade의 계산·판정·검증 경계

## 핵심 해석 규칙

- `273`은 273종 물질이 아니라 `91 species × 3 campaign labels`의 run slot 수다.
- 현재 47종은 2026-06-25에 versioning된 O/F snapshot이며, 273개 실행의 물리적 생존 집합이 아니다.
- G1–G5는 versioned 47종에 적용한 post-hoc audit view다.
- UMA·BVSE·DFT·문헌·실험값은 protocol과 fidelity를 구분해서 사용한다.
- 현재 1,081개 co-doping pair는 실제 공동치환 label이 없는 H0 가설 목록이다.

## 데이터와 그림

- `db/properties/cascade_seminar_*.csv` — Origin-ready source data
- `docs/figures/cascade/cascade_seminar_*.png` — 발표용 300 dpi PNG
- `docs/figures/cascade/cascade_seminar_*.pdf` — 벡터 PDF
- `tools/figures/plot_cascade_seminar_47.py` — 네 그림의 재생성 코드

PPTX는 사용자가 별도로 받은 파일이므로 이 ZIP에는 포함하지 않았다.
