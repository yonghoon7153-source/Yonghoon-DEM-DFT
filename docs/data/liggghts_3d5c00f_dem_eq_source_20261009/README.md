# LIGGGHTS-PUBLIC 3.8.0 (git 3d5c00f) — DEM 지배방정식 근거 소스 사본 (2026-10-09)

- 출처: 공개 저장소 github.com/CFDEMproject/LIGGGHTS-PUBLIC 의 커밋 3d5c00f (2024-06-07, "Remove logos") 의 `src/` 파일 그대로 (GPL-2.0 — 저장소의 라이선스 그대로 따른다).
- 쓰임: `docs/dem_governing_equations_report_20261009.md` 의 줄 번호 근거.  normal_model_hooke_hysteresis.h 는 리포의 기존 사본
  (`docs/reviews/codex_ps45_porosity_evidence_20261001/reference/normal_model_hooke_hysteresis.h`) 과 바이트가 같다.
- 무결성: SHA256SUMS (이 폴더).

## 10-11 추가 (DEM 지배방정식 배경 보고서 `docs/dem_governing_equations_background_20261011.md`)

- 소스 일곱: `contact_models.h` (모델 사슬 순서 228–237) · `surface_model_default.h` (접촉 기하 146–203) · `pair_gran_base.h` (겹침 · 환산 질량 311–394) ·
  `fix_nve.cpp` (적분 간격 85–86) · `fix_viscous.cpp` (전역 감쇠 140–157) · `fix_wall_gran_base.h` (벽 접촉 178–195) · `fix_check_timestep_gran.cpp` (Rayleigh · Hertz 시간 261–262 · 348).
- 설명서 열둘 (`doc/*.txt`) · 식 그림 셋 (`doc/Eqs/`) · 저장소 README (`README_LIGGGHTS.md`) · `LICENSE` (GPL-2.0) — 같은 커밋 3d5c00f20519e6bb6eb6756f51f1ad36564e649d 에서 그대로 복사.
- 무결성: SHA256SUMS 에 경로째 더했다 (10-09 다섯 줄은 그대로).
