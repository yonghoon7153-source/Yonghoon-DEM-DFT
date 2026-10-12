# DEM 지배방정식 배경 보고서 (2026-10-11) — 자료 폴더

- 보고서 정본: `docs/dem_governing_equations_background_20261011.md` (1저자 10-11 요청 — *"지배방정식 관련해서 논문, 코드 백그라운드로 report 대학원생이 서치한 느낌으로 정갈하게"*).
  PDF (18 쪽) · DOCX (Word 수식 · 맑은 고딕) 는 `build.sh` 로 다시 만든다 — 1저자에게 전달 · 리포에는 넣지 않는다.
- 짝 문서: `docs/dem_governing_equations_report_20261009.md` (10-09 · 식 ↔ 소스 줄 압축판 · 발표 슬라이드 기본형의 근거).

| 파일 | 내용 |
|---|---|
| `make_figs.py` | 그림 1 (접촉 기하 모식도) · 그림 2 (`normal_model_hooke_hysteresis.h` 156–195 행을 옮긴 함수로 그린 이력 법선력) — `python3 make_figs.py --selftest` (식 검사 5 개) · `python3 make_figs.py .` |
| `fig1_contact_geometry.{png,svg}` · `fig2_hysteresis_cycle.{png,svg}` | 위 스크립트 출력 (Matplotlib · DejaVu Sans) |
| `deck_numbers.py` | 3.3 절 (Rayleigh 비율) · 5.4 절 (상 쌍별 $k_1$ · $\gamma_n$ · $\delta_{\lim}$ · $\delta_0$ · $\delta_a$) 산술 — 덱 값 × 소스 식 |
| `build.sh` · `build_html.mjs` · `docx_tables.py` | md → PDF (KaTeX 서버 렌더 + Chromium) · DOCX (pandoc + 표 가로줄 후처리) |

## 근거

- 코드 · 설명서: LIGGGHTS-PUBLIC 3.8.0, 커밋 3d5c00f20519e6bb6eb6756f51f1ad36564e649d — 이 보고서가 인용한 사본은 `docs/data/liggghts_3d5c00f_dem_eq_source_20261009/` (10-11 확장 · SHA256SUMS).
- 덱: `docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts` (sha256 앞 16 자리 69f4359c0f436ebe).
- 문헌: litdb 정본 카드 (정본 브랜치 커밋 0a098664e 시점 385 장) — 보조 에이전트 두 개가 이론 · 방법 카드 15 장 (+ 추가 8) 과 배터리 전극 DEM 카드 27 장 (+ 추가 12) 에서 카드 줄 번호와 함께 뽑은 사실만 썼다. 서지는 카드에 적힌 대로 (영문 제목은 카드에 있을 때만) · 정본 카드가 없는 원전은 [재인용].
- 같은 $\delta_{\lim}$ 산술이 `docs/reviews/codex_review_dem_unloading_prereg_20261011.md` Q6(a) 표에 있고 값이 같다.

## 한정

- 이 보고서는 **식 · 문헌 근거 자료**다. 덱 값이 실제 런과 같은지 (실행 재현), SE 유효 영률 1.35 GPa 보정이 타당한지는 검증하지 않는다 (원장 `MV-01`–`09` · `DEMP-01`).
- 문헌 집계 (10.3 절 · 22 장 기준) 는 이 보고서의 분류다 — 카드가 법칙을 적지 않은 연구는 "미명시" 로 셌다.
