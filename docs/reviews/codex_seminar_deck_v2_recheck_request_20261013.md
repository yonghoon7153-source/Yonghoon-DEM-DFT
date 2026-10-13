# Codex 요청 — [연구세미나 덱] v2 재확인 (NO-GO → P0/P1 편집 반영 · 2026-10-13 · 발송 = 1저자)

> **한 줄**: v3 묶음 통합 판정 (NO-GO) 의 P0 · P1 을 생성기로 반영한 **수정 PPT + 그 파일에서 내보낸 PDF** 를 보낸다.  확인할 것 = SEM-01~06 이 본문 · 그림 · notes · 요약에서 **동시에** 고쳐졌는가 · 7 / 9 / 12 / 15 장의 해석 조건 · 12 장 다섯 라벨 · 글 밀도 · 투영 가독성.  새 시뮬레이션 · 재계산 없음 (값 불변).  검토 핀 = 이 요청서가 든 커밋.

## 0. 무엇이 바뀌었나 (v1 = v2 = v3 ZIP 의 PPT 와 다른 첫 파일)

| 항목 | v2 |
|---|---|
| 생성기 | `docs/seminar_20261013/build_seminar.py` v2 — Codex §9 좌표 · pt · 문구 · 1저자 Q1–Q6 결정.  selftest 추가 = Codex 지적 문구 16 개 본문 금지 · F4 라벨 5 · 장당 단어 ≤ 100 (두 칸 · 점선 장 ≤ 120 · 자리 표시 제외) · bullet ≥ 15 pt · 캡션 ≥ 12 pt · 금지값 42 · 내부 용어 (코드명 · 원장 ID · 기계명 · `uma` · `WSL`) 0.  **고치기 전 덱에서 실패 확인** (내부 용어 `WSL` · `uma` 자리 표시 · F4 라벨 2/5) 뒤 고쳤다 |
| 글자 | 절 표지 24 · ■ 제목 18 (상속 유지) · 본문 **15 pt** (줄 간격 125 % · 문단 뒤 5 pt · 두 칸 112 % · 앞 4 pt) · 캡션 **12 pt** (해석 조건 포함 · 두 줄) · 자리 표시 라벨 12 · 참고문헌 12 |
| 새 그림 | F1–F4 다시 그림 (값 불변): F2–F4 글씨 = 최종 배치 (4.35 × 3.0 in) 기준 ≈ 12 pt · **F4 조성 라벨 5/5** (locator 순서 결함 수정 · SEM-09) · F1 상자 문구 축약 + 아래 띠 = `calibration target` · `comparison target` (완료 표지 삭제 · SEM-01) |
| 자리 표시 6 | 한 줄 라벨 `Figure pending: …` (12 pt) · 제작 명령 · 파일 · 기계명 = notes (6 장 CLI 정정 `--se … --scaffold … --y 0.5`) — 1저자 Q3 (가) |
| 1저자 결정 | Q1 7 장 E ≈ **22 GPa** (우리 DFT E_VRH · DEM 문헌 입력 22.1 GPa [8]) — Sakuda 24 GPa 유리값은 notes · Q2 8 장 **30.7 비교 삭제** (상태표로 대체 · 새 숫자 없음) · Q4 14 장 Codex 다섯 행 상태표 + 빨간 hold 줄 삭제 · Q5 `transport tortuosity` (10-05 규약) + 정의식 `T = φ_SE σ₀ / σ_eff` 화면 · Q6 = 이 재확인 |
| 참고문헌 | 14 → **16**: [15] Sakuda 2013 (Sci. Rep. 3, 2261) · [16] Wang 2018 (J. Power Sources 393, 75–82) — 둘 다 litdb 정본 카드 · [n] 을 4 · 5 · 7 · 12 · 14 장 본문 · 캡션에 연결 · Holm · MLS-MPM = 카드 없음 → 서지 없이 "사용 모델" 로 (notes) |
| 단어 수 (장 위 · 자리 표시 제외) | p02 40 · p03 86 · p04 89 · p05 97 · p06 77 · p07 120 · p08 83 · p09 70 · p10 84 · p11 55 · p12 72 · p13 71 · p14 94 · p15 75 · p16 75 · p17 44 (v1: 46 · 71 · 118 · 99 · 120 · 151 · 104 · 133 · 63 · 94 · 64 · 61 · 113 · 62 · 109 · 70) |

## 1. SEM-01~14 ↔ v2 대응

| ID | v2 에서 한 것 | 장 |
|---|---|---|
| SEM-01 | `A coupled DEM–MPM–transport workflow` / `Each stage has specific calibration targets and unresolved validation tasks.` / `Agreement between models sharing inputs is a consistency check, not independent validation.` · F1 띠 = 보정 표적 · 17 장 네 줄 교체 | 2 · 17 |
| SEM-02 | `Compaction agreement depends on initialization and loading protocol` + 상태표 (옛 cell-filled servo = 역사 · 현재 등록 f = 0 완료 · f(a) 실행 실패 · 가설 판정 미완) · 30.7 비교 · 자리 표시 삭제 · 16 장 `nothing below has a result` 삭제 · 17 장 두께 검증 문장 삭제 | 8 · 16 · 17 |
| SEM-03 | `The electronic ratio decreases across the three tested voxel spacings; the ionic ratio crosses 1.` / `Grid convergence has not been established.` · 우측 `No converged conductivity ratio is reported.` · `What survives` 3 항 · 옛 원고 회고 → notes · 멱법칙 문장 삭제 | 11 |
| SEM-04 | `NCM–NCM contacts contribute 48–60 % of vertical stress after relaxation at fixed platen position; 7:3 is the minimum.` · 캡션 `21 planes, load-weighted; relaxed at fixed platen` · `wall SE excluded` | 13 |
| SEM-05 | 상태표 1 행 `Historical eight-origin study — Conductivity estimates and inference remain on hold` · h1 추론 문장 삭제 | 14 |
| SEM-06 | 상태표 4 · 5 행 분리 (`194-bed dataset v1.2 — Released for conditional use as model descriptors` / `Updated transport software — Seven reviews completed; production remains pending`) · 16 장 `Pending: separate launch approvals for the updated 194-bed run and the 20-bed extension.` · 17 장 전칭 보증 삭제 | 14 · 16 · 17 |
| SEM-07 | 22 GPa (DFT · [8]) · σy = 보정 스윕 · `Tested alternatives (volumetric cap, real E) did not remove the need for effective parameters.` · `the earlier attribution was withdrawn` · 두 칸 제목 (5.05, 2.20, 4.40, 0.36) | 7 |
| SEM-08 | `ideal-interface voxel model — an upper bound only within the same geometry, properties and boundaries` · 전기 (σ, φ) · 열 (κ, T) 구분 · 17 장 `ideal-interface calculations` | 9 · 17 |
| SEM-09 | F4 라벨 5/5 · 캡션에 조건 (`Hertz H0 contacts` · `common NCM reference 4.1 mS cm⁻¹ [16]; empirical size factor off; one bed per composition` · `conditions not yet matched`) · 본문 범위 숫자 삭제 (이중 반올림 해소) | 12 |
| SEM-10 | loading 삭제 · 협력자 R² 비교 삭제 (notes 에도 승패 없음) · `released as v1.2 (conditional use as model descriptors)` · G5b → notes · G5a · G3 확대 | 15 |
| SEM-11 | `Holm/Maxwell constriction using Hertz contact radii` · `T = φ_SE σ₀ / σ_eff` · `Contact constriction accounts for 73–75 % of Joule dissipation in this network model.` · 캡션 `truncated y-axis — compare values` · 시드 산포 · 길이 효과 문장 삭제 | 4 |
| SEM-12 | 자리 표시 = 라벨 한 줄 · 6 장 CLI 정정 (notes) · 8 장 비교 지시 삭제 · 10 장 `Additive seeding illustration` · `Synthetic morphology example` · `not a production stamp` | 4 · 6 · 8 · 9 · 10 |
| SEM-13 | [15] · [16] 추가 · [n] 연결 · 정본 카드 없는 원전은 notes 에 "사용 모델" | 7 · 12 · 18 |
| SEM-14 | 표지 저자 블록 (0.68, 2.98, 8.40, 0.75) 16/14/14 pt (그림 상단 3.84 위) · F1 축약 · 7 장 소제목 15 pt 한 줄 · 17 장 상자 (0.61, 1.08, 8.84, 3.75) | 1 · 2 · 7 · 17 |

## 2. 확인 요청

- **Q-V2-1** SEM-01~06 이 본문 · 그림 · notes · 요약에서 동시에 닫혔는가 — 남은 곳이 있으면 장 · 문장 · 고칠 영어 문구.
- **Q-V2-2** 7 / 9 / 12 / 15 장 해석 조건이 화면 (캡션 12 pt) 에 충분한가 · 12 장 다섯 라벨 · 22 GPa 표기 (DFT E_VRH + [8]) 가 적절한가.
- **Q-V2-3** 글 밀도 — p07 120 · p05 97 · p14 94 가 아직 많은가 (지울 문장 · notes 로 넘길 문장 콕 집어서).
- **Q-V2-4** 투영 가독성 — 새 그림 글씨 (≈ 12 pt) · 캡션 12 · 재사용 그림 (p03 3D 라벨 · p13 열지도) 에서 뺄 것.
- **Q-V2-5** 판정 — **GO / 조건부 GO / NO-GO** · 남은 P0/P1/P2 를 장 · 요소 · 구체 수정으로 · 끝에 장별 표 `장 | 그대로 / 손질 / 다시 | 걸리는 것 | 고칠 것`.

고정 조건 · 이미 아는 것 = 앞 요청서 §3 그대로 (19 장 · 순서 · 템플릿 · 표지 공란 · 자리 표시 6 = 그림은 1저자가 채움 · 값 · 재사용 그림 불변 · hold 값 없음).  회신은 한국어 · 장 위 문구만 영어 · 리포 수정 없이 판정문 하나 (우리가 반입).

## 3. 동봉 (ZIP)

- `seminar_20261013_v2.pptx` + 그 파일에서 내보낸 `seminar_20261013_v2.pdf` · `render/p-01…19.png` (1280 × 960) + `contact_sheet.jpg` · 리포 `docs/seminar_20261013/` (생성기 v2 · `figs/` 새 그림 4 + svg · csv · `slide_text_v2.md` · README · `slide_sources.json`) · 이 요청서 · 앞 판정 둘의 리포 사본 경로 = `docs/reviews/codex_review_seminar_deck_20261013.md` · `…_v3_20261013.md`.
- 10-13 템플릿 덱 = 미동봉 (생성기 템플릿 · 사용자 덱 규약).
