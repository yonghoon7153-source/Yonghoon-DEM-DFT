# 반입에서 뺀 것 (Codex v3.1 종결 묶음 · 2026-10-13)

받은 묶음 = `codex_seminar_v31_closure_review_20261013.zip` (sha256 `265b0cb2f351d4e079fffe79723e2fdf27145f693f60349dd2b6bd889b30236b` · 135 항목 · 30.3 MB).  판정문 · 검사 스크립트 · 증거 JSON 14 파일만 넣었다.  스크립트는 반입만 했고 돌리지 않았다.

- `input/` — 우리가 보낸 ZIP v7 사본 (덱 PPTX sha256 `73fa2dc3…` · PDF `5335e3fe…` · 렌더 17 장 · `MANIFEST.md` · 리포 파일 · 문헌 크롭 3).  사용자 덱은 리포에 넣지 않는다 · 나머지는 리포 원본 (`docs/seminar_20261013/` · `docs/reviews/codex_seminar_deck_v3_1_closure_request_20261013.md`) 과 같은 파일.
- `renders/` — 위 PDF 의 독립 렌더 17 장 (덱에서 나온 그림이라 같은 이유로 제외).
- `evidence/so_v3_crop.png` — v3 판 So 2021 Fig. 4a 크롭 (1045 × 1005 px · sha256 접두 `2f7d556bb0a59662`).  새 크롭 (1133 × 1005 px · `dac42775fe263fc8`) 과 함께 문헌 그림 크롭이라 리포에 넣지 않는다 — 정본 = litdb 정본 브랜치 `so2021_dem_fabrication_degradation_ductile_particles` 그림.
- `evidence/numeric_inputs/` (19 파일) — 검산에 쓴 이전 입력 사본.  리포에 같은 내용이 있다:
  - `sources_mixing/docs/data/mixer_highbo_devbo_prelim_20261003/devbo_c{8x2,12x3,16x4}.json` · `…/mixer_highbo_devu_prelim_20261006/devu_c{8x2,12x3,16x4}.json` · `devu_contact.json` (7) = 리포의 같은 경로.  JSON 내용이 같고 Codex 사본이 끝에 줄바꿈 한 바이트를 더 가졌다 (`json.loads` 같음 · 끝 줄바꿈을 빼면 바이트 같음).
  - `input/repo/docs/seminar_20261013/figs_v3/F_{dataset,limits,load,poro,trans,vgcf}.csv` (6) = 리포 HEAD 의 같은 경로와 바이트 같음.
  - `input/repo/docs/seminar_20261013/figs_v3/F_mix{1,2,3}.csv` (3) = **v3 판** (리포 커밋 `0c6f5c84e` 의 같은 경로 · git blob `178d11f6` · `37ef1f13` · `db59cf31`).  v3.1 판 (리포 HEAD) 은 머리 · 소수 자릿수가 다르다 (판정문 §4 가 설명하는 변화).
  - 묶음 안 `evidence/numeric_inputs/` 아래 두 사본 (2) = 리포 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_recheck/evidence/so_figures_source.json` · `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_recheck/notes/sources/phase_a_original_primary96.json` 와 바이트 같음 (묶음 안 경로 = 같은 꼬리).
  - `input/lit/so2021_fig4a_crop.png` (1) = 위 v3 크롭과 같은 파일.
- `notes/__pycache__/` (`.pyc` 2) — 실행 부산물.
- 판정문 안의 이 폴더들을 가리키는 상대 경로는 Codex 묶음 기준이다.
