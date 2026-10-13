# 연구세미나 덱 — Codex 10-13 NO-GO 반영 수정 계획 (1저자 비준 대기)

> ✅ **비준 · 적용 10-13** — 1저자: Q1 = 22 GPa (논문 reference 있음 · DFT E_VRH + DEM 문헌 입력 22.1 [8]) · Q2 권고 (가) · Q3–Q6 권고대로.  구현 = 생성기 v2 (`docs/seminar_20261013/build_seminar.py` · 시험 먼저) · 재확인 요청서 `docs/reviews/codex_seminar_deck_v2_recheck_request_20261013.md`.  아래 본문은 비준 전 계획 원문.  → Codex 재확인 10-13 = **조건부 GO** (`codex_review_seminar_deck_v2_recheck_20261013.md`) → v2.1 (P0 p8 servo · p15 캡션 · P1 다섯) → 종결 확인 요청서 `codex_seminar_deck_v2_1_closure_request_20261013.md`.

> 대상 = 초안 4 (19 장 · `docs/seminar_20261013/build_seminar.py` 생성).  판정 = `docs/reviews/codex_review_seminar_deck_20261013.md` (첫 판 과학 리뷰 · SEM-01~14) + `codex_review_seminar_deck_v3_20261013.md` (v3 묶음 통합 판정 · 장별 교체문 · 좌표 · pt).  **NO-GO = 현재 파일 그대로의 발표판 확정 불가.  새 시뮬레이션 · 재계산 요구 없음 — 문장 · 출처 · 표시 편집.**  재확인 = **수정된 PPT + 그 파일에서 내보낸 PDF**.

## 0. 판정 요약

| 항목 | Codex |
|---|---|
| 판정 | NO-GO (발표판 확정) · P0 편집 뒤 수정 PPT/PDF 재확인 · 조건부 GO 선지급 없음 |
| 열린 결함 | P1 = SEM-01~06 (발표의 과학적 결론 · 증거 지위를 바꾸는 오류 — 이번 편집 우선순위 P0) · P2 = SEM-07~13 · P3 = SEM-14 (원장 `SEM-01`~`14` open) |
| v3 ZIP | PPT · PDF 세 판 바이트 동일 (v1 = v2 = v3) — 바뀐 것은 `outline_v1.md` 한 줄뿐 → 기존 지적 전부 미해결 |
| 금지값 | 42 패턴 0 (본문 · notes · csv · svg) · hold **수치** 없음 — 그러나 hold **추론** 재사용 둘 (11 장 멱법칙 · 14 장 h1) |
| 템플릿 | 10-13 원본 미동봉 → 완전 일치 판정 불가 · 실제 XML = ■ 제목 **18 pt 상속** (요청서의 15 는 오기 `SELF-110`) · 출처 줄 미구현 (생성기가 `TextBox 69` 삭제 · `tag()` 미호출) |

## 1. 우리 트리 재현 (판정값 차이 0)

| 항목 | Codex | 우리 트리 |
|---|---|---|
| 13 장 AM–AM 21 단면 하중 가중 몫 (0:10 → 10:0) | 59.562243 · 54.634924 · 52.371659 · 48.463893 · 56.914398 % | 같음 (`docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json` · `contribution_sigma_zz_pct` = 하중 가중 평균과 같음) |
| 단면 평균 축응력 | 158.25 · 159.93 · 164.44 · 167.14 · 175.48 MPa | 같음 — 고정판 이완 상태 (300 MPa 가압 최고점 아님) |
| 11 장 공개 3 점 (vox 0.4 · 0.3 · 0.25) | Δ비 3.360103627 · R = A + C·h^p 의 p 3.131238 | Δ비 3.360104 · p 3.131238 — "멱법칙 불성립" 은 CL-41 (vox ≤ 0.15 · hold) 계열의 추론이고 공개 3 점에는 성립 안 함 |
| 14 장 h1 추론 | 원장 hold | CL-33 · CL-34 = `hold` |
| 12 장 F4 라벨 | 5 중 2 만 표시 | `make_seminar_figs.py`: `set_xticklabels` 뒤 `_fmt` 의 `MaxNLocator` 가 덮음 — 값 불변 · 라벨 복구 |
| 참고문헌 | Sakuda 2013 · Wang 2018 연결 요구 | 정본 카드 **있음** (`sakuda2013_sulfide_mechanical_property` = 75Li₂S·25P₂S₅ 유리 18–25 GPa · `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` = NMC811 4.1 × 10⁻³ S/cm) → 추가 가능 · Holm · MPM 수치법 = 카드 없음 → 서지 안 채움 |

## 2. 수정 원칙

- 생성기 (`build_seminar.py`) 로만 고친다 — 좌표 (in) · pt · 문구 = Codex 통합 판정 §9 그대로 (상충 시 통합 판정 > `notes/visual_*`).  값 · 재사용 그림 · 19 장 · 순서 · 템플릿 · 표지 날짜 공란 = 불변.
- **시험 먼저**: 생성기 selftest 에 ① 제거 문구 금지 목록 (`Large–large` · `follow no power law` · `changes sign` · `never to one another` · `cross-validation` · `retracted` · `Every production number` · `nothing below has a result` · `30.7`) ② F4 라벨 5 개 (svg 텍스트) ③ 단어 수 상한 (장당 본문 ≤ 90 · 자리 표시 글 제외) ④ bullet 15 pt · 캡션 ≥ 12 pt 를 넣고, 고치기 전 덱에서 **실패**를 확인한 뒤 고친다.
- 글자: 절 표지 24 · ■ 제목 18 (상속 유지) · 본문 **15** (줄 간격 120–130 % · 문단 뒤 4–6 pt · 두 칸 110–115 %) · 해석용 캡션 · 범례 **12** · 일반 출처 10–11 · 참고문헌 12.  글을 먼저 줄이고 (장당 50–80 단어 · 제작 지시 제외) 그림을 위로 올려 키운다.
- 새 그림 (F1–F4): 최종 배치 크기 기준 축 · 눈금 · 범례 12 pt (지금 7.3 / 6.4 pt 로 축소됨) — 값 불변.  재사용 그림 11 은 다시 그리지 않음 (여백 자르기 · 캡션만).
- 자리 표시 6: 발표판 = 한 줄 라벨 (`Figure pending: …`) + 제작 명령은 notes (6 장 명령 정정 = `--se … --scaffold … --y 0.5`).  장 합치기 없음.
- 출처: 작은 출처 상자 복원 대신 캡션 · 문장에 검증된 `[n]` · 긴 경로는 notes.  요청서 정오표 = 머리 표지.

## 3. P0 — 장별 교체 (Codex 통합 판정 §1 · §9 · 영어 = 화면 문구)

| 장 | 요소 | 교체 |
|---|---|---|
| 2 | 제목 · bullet · F1 | `A coupled DEM–MPM–transport workflow` / `Each stage has specific calibration targets and unresolved validation tasks.` / `Agreement between models sharing inputs is a consistency check, not independent validation.` · F1 상자 = `DEM packing / Plastic compaction / Voxel transport / Electrode response` · 아래 띠 = 보정 **표적** 표현 (`anchored to … measurements` 삭제) · 본문 (0.61, 1.08, 8.84, 1.65) · F1 (0.77, 3.00, 8.46, 3.15) · 캡션 (1.00, 6.28, 8.00, 0.36) 12 pt |
| 3 | 제목 | `Composition-dependent porosity in five simulated beds` · "7:3 = 이 다섯 침대 중 최소" 유지 · 조성당 침대 1 · 시드 없음 · 이완 상태 한정 |
| 4 | bullet · 캡션 | `Holm/Maxwell constriction using Hertz contact radii` · 화면에 `T = φ_SE σ₀ / σ_eff` · `Contact constriction accounts for 73–75 % of Joule dissipation in this network model.` · 캡션 `Truncated y-axes; compare numerical values` · 시드 산포 문구 · 길이 효과 이분법 삭제 · 제작 지시 notes |
| 7 | 두 칸 | 왼쪽 `Effective material inputs` · 오른쪽 `Calibration target and limits` (5.05, 2.20, 4.40, 0.36) 15 pt · 본문 (0.55/5.05, 2.66, 4.25/4.40, 2.75) 15 pt · E ≈ 24 GPa 재료 라벨 (Q1) · σy 0.30 = 보정 스윕 선택값 · `The tested alternatives did not remove the need for effective parameters.` · `Our earlier attribution to the literature was withdrawn.` · 70–90 단어 |
| 8 | 전부 | `Compaction agreement depends on initialization and loading protocol` / `Historical and current scaffold calculations use different electrolyte initialization and loading protocols.` / `AM load sharing remains a candidate explanation for over-compaction; the final hypothesis verdict is pending.` · 30.7 (Q2) · 자리 표시 → 상태표 (역사 cell-filled servo · 현재 등록 f=0 25.842 µm · f(a) 실행 실패 · 판정 미완료) · `Pressed honestly` 삭제 |
| 9 · 17 | 정의 | `ideal-interface voxel model` (같은 기하 · 물성 · 경계의 모형 내 상한) · `Finite-volume conservation on the phase grid gives electrical and thermal transport.` · 전기 (σ, φ) · 열 (κ, T) 구분 · `contact-free branch` 등가 주장 삭제 |
| 10 | 라벨 · 제목 | `Additive geometry used in transport rasterization` · 왼쪽 `additive seeding illustration` · 가운데 `synthetic morphology example` (12 pt) · G6 상대 확대 · 72/72 = 시험 범위 |
| 11 | 전부 | `Problem 1: Grid dependence` / `The electronic ratio decreases across the three tested voxel spacings. The ionic ratio crosses 1.` / `Grid convergence has not been established.` · 우측 `No converged conductivity ratio is reported.` 하나 · F2 (0.65, 2.85, 5.20, 3.15) · 우측 (6.05, 3.05, 3.30, 1.40) 15 pt · 캡션 (0.65, 6.10, 5.20, 0.45) 12 pt · `What survives` 3 항 · 옛 원고 회고 · GPU 메모리 → notes |
| 12 | 전부 | `Problem 2: Absolute electronic conductivity` / `Voxel predictions exceed the available DC-polarization estimates; measurement conditions remain unverified.` / `The NCM–SE comparison uses a common reference conductivity and a specified contact model.` · 왼쪽 캡션 `Model and DC-polarization estimates — log scale; conditions not yet matched` · 오른쪽 `Carbon- and binder-free NCM–SE beds; Hertz H0 contacts` + `Common NCM reference: 4.1 mS cm⁻¹; empirical size factor off; one bed per composition` · F3 (0.60, 2.95, 4.35, 3.00) · F4 (5.10, 2.95, 4.35, 3.00) · 캡션 y 6.10 h 0.50–0.65 12 pt · F4 라벨 5 복구 · 범위 `0.375–0.467 mS cm⁻¹` 또는 삭제 |
| 13 | 전부 | `Problem 3: Load sharing during compaction` / `NCM–NCM contacts contribute 48–60 % of vertical stress after relaxation at fixed platen position.` / `The porosity ranking agrees for the selected five compositions (exploratory comparison).` · 왼쪽 (0.50, 2.95, 4.25, 3.00) · 오른쪽 (4.95, 3.10, 4.65, 2.80) · 우측 캡션 (4.95, 6.03, 4.65, 0.58) 12 pt `SE von Mises stress, 0–150 MPa; wall SE excluded` |
| 14 | 점선 상자 | 제목 `Registered studies and current status` · 탭 `Study status` 15 pt · 틀 (0.55, 2.40, 8.90, 3.25) · 왼쪽 x 0.80 w 3.75 · 오른쪽 x 4.75 w 4.55 · 행 y 2.72/3.26/3.80/4.34/4.88 h 0.48 14–15 pt · 다섯 행 = `Historical eight-origin study | Conductivity estimates and inference remain on hold` · `VGCF ordering study | Ordering holds across tested grids and offsets (72/72)` · `Absolute-conductivity comparison | R = 2.07 (Tier 1); Q = 0.84` · `194-bed dataset v1.2 | Released for conditional use as model descriptors` · `Updated transport software | Seven reviews completed; production remains pending` · 정의 (0.80, 5.85, 8.60, 0.58) 12 pt `R: model / literature conductivity. Q: conductivity retained after PTFE treatment.` · 빨간 hold 줄 삭제 (남기면 (0.55, 6.40, 8.90, 0.35) 14 pt `The historical eight-origin result remains on hold.`) · `only the procedure and the verdict are reported` 삭제 |
| 15 | bullet | loading 삭제 · 협력자 R² 비교 삭제 (notes 에도 승패 없음) · 130 + 64 코호트 · 조건부 모델 디스크립터 · G5b → notes · G5a (0.55, 2.95, 4.30, 3.00) · G3 (5.05, 2.95, 4.30, 3.00) · 캡션 12 pt (geometric · 범위 = 130 집합 유한값) |
| 16 | 전부 | 제목 `Tests for unresolved model limits` · 위 `Grid sensitivity remains unresolved. Diagnostic results exist, while final hypothesis verdicts remain pending.` · 두 칸 15 pt 세 항목씩 (Electronic transport: `Interface resistance: film model implemented, production on hold` · `Carbon conductivity: comparison with DC polarization` · `NCM conductivity: literature-based input review` / Compaction and mixing: `AM load sharing: final hypothesis verdict pending` · `Unloading: springback and measured thickness` · `Mixing: an adhesion parameter for SE–SE contacts`) · 하단 (0.55, 5.75, 8.90, 0.65) 14 pt `Pending: separate launch approvals for the updated 194-bed run and the 20-bed extension.` |
| 17 | 전부 | 제목 `Current findings and limitations` · 상자 (0.61, 1.08, 8.84, 3.75) 15 pt · 네 줄 = `DEM and contact networks: composition trends from one bed per composition` · `MPM: plastic deformation, with compaction agreement dependent on initialization and loading protocol` · `Voxel transport: ideal-interface calculations with grid dependence and unresolved absolute conductivity` · `Final model-validation verdicts remain pending` · `Every production number …` 삭제 |

## 4. P1

| 장 | 조치 |
|---|---|
| 1 | 저자 블록 (0.68, 2.98, 8.40, 0.75) 이름 16 · 소속 · 이메일 14 · 세 줄 · 그림 상단 y 3.84 위 · 날짜 공란 유지 |
| 2 | F1 상자 제목 · 설명 축약 (긴 보정 문장 제거) |
| 4 · 6 · 9 | 제작 지시 → notes · 자리 표시 = 한 줄 라벨 (Q3) · 6 장 명령 정정 |
| 5 | `Selected literature survey (22 studies; author classification)` · `Contact-law illustration from the implementation` · fixed-shape soft-sphere 로 한정 · 65–80 단어 |
| 10 | 바깥 12 pt 캡션으로 모식 / 합성 / 실제 수치 구분 |
| 15 | G5b notes · G5a · G3 확대 · G5a 빨간 × = 관통 경로 부재 표지 |
| 18 | 두 열 (0.50/5.05, 1.00, 4.45, 5.85) 12 pt · [n] 연결 · Sakuda 2013 · Wang 2018 추가 (정본 카드) → 16 편 · Holm · MPM 수치법 = 카드 없음 → `[n]` 없이 사용 모델 지위만 |

## 5. P2 (이번 확정 조건 아님)

- 자리 표시 그림 확보 뒤 6 · 9 장 보강 · 필요 시 합치기 (지금은 19 장 유지).
- 4 장 재사용 막대 다음 판 (0 시작 또는 점 도표).  ML 검증 규약 맞춘 뒤 성능 그림.

## 6. 사용자가 정할 것

`[세미나]`
- **Q1** 7 장 E ≈ 24 GPa 의 라벨 — (가) 24 GPa 유지 + `sulfide glass (75Li₂S·25P₂S₅) literature value [n]` (Sakuda 2013 카드) / (나) 우리 DFT E_VRH 22 GPa 를 `bulk LPSCl (our DFT)` 로 · 24 는 notes.  **권고 (가)** — CLAUDE.md 3 층 (real bulk 24) 과 같고 카드가 있다.
- **Q2** 8 장 30.7 vs 30.28 µm — (가) 비교 삭제 (Codex 최소안) / (나) `Earlier cell-filled SE calculation with bidirectional servo` 한정어로 유지.  **권고 (가)** — 현재 DEM-seeded 결과의 검증값이 아니고 29.95 와도 다른 정의.
- **Q3** 자리 표시 6 의 발표판 처리 — (가) 한 줄 라벨 `Figure pending: …` + 명령 notes / (나) 지금처럼 제작 지시 전문 유지 (검토판).  **권고 (가)** — 청중용 화면에 명령이 보일 이유 없음 · 그림은 1저자 캡처로 채움.
- **Q4** 14 장 — Codex 다섯 행 상태표 그대로 + 빨간 hold 줄 삭제.  **권고 그대로**.
- **Q5** 용어 — Codex `transport tortuosity factor, T = …` ↔ 1저자 10-05 규약 `수송 tortuosity (transport tortuosity)`.  **권고 = 규약 유지 (`transport tortuosity`) + 정의식 `T = φ_SE σ₀ / σ_eff` 를 화면에** (규약이 요구하는 정의 한 줄 · "factor" 는 τ² 에만 허용되는 말이라 어느 쪽도 규약 위반 아님).
- **Q6** v2 를 만든 뒤 Codex 재확인 (수정 PPT + 그 PDF) 을 발표 전에 받을지.  **권고 예** — NO-GO 해제 조건이다.

비준 뒤 = 시험 먼저 → 생성기 수정 → 렌더 19 장 → 단어 수 · 금지 문구 · 라벨 selftest → ZIP v4 (수정 PPT · PDF · 렌더 · 생성기) → 1저자 발송.
