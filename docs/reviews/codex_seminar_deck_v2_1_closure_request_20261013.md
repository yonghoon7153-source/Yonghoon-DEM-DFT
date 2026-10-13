# Codex 요청 — [연구세미나 덱] v2.1 종결 확인 (조건부 GO → P0 둘 · P1 다섯 반영 · 2026-10-13 · 발송 = 1저자)

> **한 줄**: v2 재확인 (조건부 GO · `codex_review_seminar_deck_v2_recheck_20261013.md`) 의 P0 두 건 (SEMV2-01 · 02) 과 P1 다섯 (03~07) 을 반영한 **v2.1 PPT + 그 PDF**.  종결 기준 = Codex §5 그대로 — 바뀐 문장 · 그림의 PPT/notes/PDF 일치 · 기존 수치 불변 · 새 겹침 없음.  닫힌 다섯 항목 재심 · 새 계산 없음.  검토 핀 = 이 요청서가 든 커밋.

## 1. 반영표

| ID | 장 | v2.1 |
|---|---|---|
| SEMV2-01 (P0) | 8 | 상태표 2 행 `Current registered runs: DEM-seeded SE, stress-controlled servo — f = 0 completed; f(a) execution failed` · 첫 bullet `… use different electrolyte initializations and run configurations; they are not one validation series.` · notes `The current statuses refer to the registered servo runs (--protocol servo; primary endpoint = final thickness after servo convergence).` |
| SEMV2-02 (P0) | 15 | 왼쪽 캡션 `Geometric tortuosity vs SE fraction — 130 + 64 beds` / `×: 24 non-percolating beds in the 130-bed set` · 오른쪽 `Porosity vs SE fraction — 130-bed set` · 본문 `In the 130-bed set: SE percolation 106/130; …` · 그림 두 장 바이트 불변 |
| SEMV2-03 | 12 | F3 · F4 세로축 제목 두 줄 (`Electronic conductivity` / `(mS cm⁻¹)` · 값 · 축 범위 · 글씨 불변) · 오른쪽 캡션 3 줄 `NCM–SE beds, no carbon/binder; Hertz H0` / `common NCM reference 4.1 mS cm⁻¹ [16]; size factor off` / `one bed per composition` |
| SEMV2-04 | 2 | F1 제목 두 줄 (`DEM / packing` · `Plastic / compaction` · `Voxel / transport` · `Electrode / response`) · 부연 축약 (`MPM: J2 plasticity / DEM scaffold` · `finite-volume solver / ionic · electronic · thermal`) · 띠 `compaction data` · `pure-SE compaction` · `conductivity data` |
| SEMV2-05 | 5 notes | `Young's modulus reference: our DFT E_VRH = 22.06 GPa (…); the bulk modulus K / B0 = 26.23 GPa is a separate quantity` |
| SEMV2-06 | 7 | 첫 행 `LPSCl reference: E ≈ 22 GPa (our DFT E_VRH; literature DEM input 22.1 GPa [8])` (σy 범위 삭제) · 오른쪽 = 보정 표적 + `Validation against independent experiments: pending` · 철회 이력 · ν = 0.49 / K 문장 → notes (`keeps K = 25.5 GPa close to the DFT reference B0 = 26.23 GPa`) · 단어 120 → 106 |
| SEMV2-07 | 4 | `Contact-network approach [8]: bulk resistance + Holm/Maxwell constriction using Hertz contact radii; chosen σ₀ = 1.5 mS cm⁻¹ (pellet-literature range).` |
| 선택 | 14 · 10 | 14 장 소개 `The table summarizes the current status of each registered study.` · 10 장 오른쪽 캡션 축약 |

- 생성기 selftest 추가 (v2 덱에서 **실패** 확인 뒤 고침): 금지 문구 `fixed-platen hold` · `σy 0.05–0.30` · 옛 15 장 캡션 · p15 캡션 ↔ 집단 검사 (왼쪽 `130 + 64` + tortuosity · 오른쪽 `130-bed set` + Porosity).
- 단어 수 (장 위 · 자리 표시 제외): p02 40 · p03 86 · p04 88 · p05 97 · p06 77 · **p07 106** · p08 83 · p09 70 · p10 82 · p11 55 · p12 71 · p13 71 · p14 90 · p15 76 · p16 75 · p17 44.
- 자리 표시 5 (p4 · p6 ×2 · p9 ×2) = 1저자가 채움 (합의 범위) · 표지 날짜 공란 유지.

## 2. 확인 요청

- **Q-C-1** SEMV2-01 · 02 가 PPT · notes · PDF 에서 일치하는가 (p8 servo · p15 집단).
- **Q-C-2** SEMV2-03~07 손질이 새 겹침 · 잘림 없이 들어갔는가 (p2 F1 · p12 축 제목 · 캡션 3 줄 · p7 두 칸).
- **Q-C-3** 기존 수치 · 재사용 그림 불변 (F2–F4 csv 바이트 동일 · G3 · G5a sha 동일).
- **Q-C-4** 판정 — **GO / 조건부 GO / NO-GO**.

고정 조건 = 앞 요청서들 §3 그대로.  회신 = 한국어 · 장 위 문구만 영어 · 리포 수정 없이 판정문 하나 (우리가 반입).

## 3. 동봉 (ZIP v5)

`seminar_20261013_v2_1.pptx` + 그 파일에서 내보낸 `seminar_20261013_v2_1.pdf` · `render/p-01…19.png` + `contact_sheet.jpg` · 리포 `docs/seminar_20261013/` (생성기 v2.1 · `figs/` · `slide_text_v2.md` (v2.1) · README) · 이 요청서.
