# Codex 짧은 재확인 요청 — 연구세미나 덱 v3.2 (2026-10-14 · 회신 10-15 까지 · 세미나 10-16)

대상 = Codex 가 **GO** 로 닫은 v3.1 (`docs/reviews/codex_review_seminar_deck_v3_1_closure_20261013.md`) 에 1저자 10-14 결정 1–9 를 넣은 판이다.
**바뀐 장만** 봐 주십시오 — 손대지 않은 6 장은 v3.1 과 내용 대조로 같음을 보였다 (§1 · 종결 판정 §6 승계 조건 1–4).
새 시뮬레이션 · 새 계산값은 없다.  새 숫자는 전부 리포에 이미 기록된 값이다 (장마다 출처 · §2).

## 0. 파일 고정

| 파일 | SHA-256 |
|---|---|
| v3.2 PPTX (18 장 · 리포 밖) | `1b6988f3e55dc6bcf7e81d0ba4ec35b11ed2a0790a1357ba6e6185d22b08f28d` |
| v3.2 PDF (LibreOffice + Carlito · 18 쪽 · 리포 밖) | `0e8f9a74cbb8ee004af293c4dbec2795f92efd4f540a8135de178ecf833a769e` |
| 비교 기준 = Codex 종결 v3.1 PPTX | `73fa2dc3b5629eabb9ec744b47495512db477dd962753a003820ad02b525401b` |
| 지배방정식 원 슬라이드 (1저자 10-09 `DEM_Equations_final_20261009_2.pptx` · 리포 밖 · 3 장의 식 · 그림 출처) | `8e76819a9f89516d75c7bd40c529cd65ce055e31a2c8b777d1b8e8edfc669223` |
| 양식 = 1저자 10-13 덱 (리포 밖 · 이 파일로 v3.1 을 다시 만들어 종결본과 내용이 같음을 확인 · §1) | `7746e163ddb399a62c40b1de85e71b0cd8df1aa87917b3621b3c015704387be7` |

- 생성기 · 그림 · 글 전문 = 이 요청서와 같은 커밋의 `docs/seminar_20261013/build_seminar_v32.py` (v3.1 생성기 `build_seminar_v3.py` 를 그대로 불러 v3.1 을 만든 뒤 차분만 적용) · `docs/seminar_20261013/figs_v3/make_seminar_figs_v32.py` (F_p4) · `docs/seminar_20261013/slide_text_v32.md` (18 장 글 · 표 · 출처 줄 · 다리 줄 · notes 전문) · `docs/seminar_20261013/slide_sources_v32.json` · README v3.2 절.
- PowerPoint 앱 렌더는 우리도 하지 않았다.  ⚠ 3 장의 식은 OMML 이다 — LibreOffice PDF 에는 **대체 그림**이 그려지고 PowerPoint 는 OMML 을 그린다 (§3).
- PPTX 는 python-pptx 저장이라 빌드마다 해시가 바뀐다.  동일성은 해시가 아니라 내용 대조로 말한다 (§1).

## 1. 장 대응 · 승계 조건 (종결 판정 §6)

| v3.2 | v3.1 | 바뀜 | 이번 확인 |
|---:|---:|---|---|
| 1 · 2 | p01 · p02 | 없음 (2 장 다리 줄만) | 불필요 |
| **3** | — | **새 장** — DEM 지배방정식 (1저자 10-09 슬라이드의 식 · 그림 복사) | **예** |
| 4 | p05 | 인용 번호만 (본문 `[1, 7]` → `[1, 2]` · notes `[15]` → `[3]`) · 다리 줄 | 번호만 |
| **5** | p06 | 표 마지막 행 · notes 덧붙임 | **예** |
| 6 | p07 | 없음 (다리 줄만) | 불필요 |
| **7** | p03 | 문헌 꼬리표 · notes 덧붙임 | **예** |
| 8 | p04 | 없음 (다리 줄만) | 불필요 |
| **9** | p08 | 본문 2 · 새 표 두 줄 · 해석 줄 자리 · notes | **예** |
| **10** | p09 | notes 덧붙임 (문헌) | **예** (notes) |
| **11** | — | **새 장** — Problem 4 (그림 F_p4 · 표) | **예** |
| **12 · 13** | p11 · p12 | notes 덧붙임 (문헌) | **예** (notes) |
| **14** | p13 | 문헌 꼬리표 · notes 덧붙임 | **예** |
| **15** | p14 | 결론 줄 삭제 · 언로딩 항목 · 세대 2 계획 띠 · notes 교체 | **예** |
| **16** | p15 | "DEM loading" 한 줄 (지시 목록 밖 · 일관성) · notes 덧붙임 | **예** |
| **17** | p16 | 인용된 것만 13 · 번호 다시 · 새 문헌 6 | **예** |
| 18 | p17 | 없음 | 불필요 |
| — | p10 | **삭제** (194-bed / 데이터셋 진행 장) — R / Q 는 9 장 표로 · 8 원점 연구 "보류" 는 9 장 notes 로 | 옮긴 문장 = 9 장 |

승계 조건 (판정 §6) 에 대한 기록:

1. **손대지 않은 장 = v3.1 과 같음** — `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_2_fix/cmp_codex_v31.py` 가 Codex 증거 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_1_closure/evidence/pptx.json` (장별 글 run · notes · 그림 sha256) 과 대조: ① 다시 만든 v3.1 덱 = 종결 v3.1 PPTX 와 17 / 17 장 같음 ② v3.2 의 1 · 2 · 4 · 6 · 8 · 18 장 = v3.1 p01 · p02 · p05 · p07 · p04 · p17 과 같음 (인용 번호 바꿈 적용 · 다리 줄 제외) — 기록 `cmp_codex_v31.json`.  생성기 검사 A5 도 같은 결과 (표 · 무리 안 글 · 그림 바이트 · notes).
2. **해시 · 대응표** = §0 · 위 표.
3. **줄바꿈 · 잘림 · 장 간 참조 · 인용 번호** — 렌더 18 쪽 육안 확인 · 장 간 참조 다섯 (3 장 → "Problem 4" · 4 장 notes "next slide" → 5 장 · 8 장 notes → Transport 장 (6) · 11 장 notes → porosity · load-sharing 장 · 16 장 notes → Problem 4) 모두 실재 · 참고문헌 13 = 전부 인용됨 · 인용 번호 전부 참고문헌 있음 (검사 A6).
4. **한정어 유지** — 6 장 (이상적 계면 · 상한 한정) · 15 장 (격자 민감도 미해결 · 최종 판정 미정 · Rint 생산 보류) · 16 장 (이상적 계면 · 격자 의존 · 절대값 미해결 · 최종 판정 미정) 그대로.  15 장에서 지운 것 = 194-bed / 20-bed 발사 승인 줄 하나 (1저자 결정 2).

## 2. 바뀐 장 — 화면 글 old → new · 출처

| 장 | v3.1 (old) | v3.2 (new) | 출처 |
|---|---|---|---|
| 5 표 | `Validation` · `against independent experiments: pending` | `Lab anchor (planned)` · `EIS + DC polarization, no results yet: NCM pellets 0.1 / 0.2 / 0.3 g, polycrystalline and single-crystal; LPSCl pellets, small and large particles` | `docs/session_20260923_progress.md` 10-14 오후 3 ④ (LPSCl 0.1 g · NCM PC · SC × 0.1 / 0.2 / 0.3 g = 6 펠릿 · EIS + DC) · 10-14 저녁 ③ (소립 SE 펠릿 = 기하 공극률 · 진밀도 미확인) · 큰 입자 펠릿 = 1저자 10-14 결정 5 (진행 기록에는 아직 "답 대기") |
| 7 꼬리표 | — | `Literature: pure LPSCl in the die at 0.3 GPa, porosity ≈ 13 % (D50 40 µm) to ≈ 26 % (4 µm) [13] — not composite beds` | 정본 카드 `faka2026_particle_size_consolidation_strain_lpscl` (Fig. S2 판독 12.9 · 16.0 · 22.5 · 26.3 % · in-die · 순응도 보정 서술 없음) · notes = 같은 카드 + `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` (CT 1.277 µm · 479 MPa 입계 공극 대부분 닫힘 · 1155 MPa 공극 안 보임) |
| 9 본문 2 | `… measurement conditions remain unverified. The NCM–SE comparison uses a common reference conductivity and a specified contact model.` | `… measurement conditions remain unverified. A registered re-run calibrates carbon on SBE alone (σ_VGCF* = 3.41 S cm⁻¹, an effective value); the DBE prediction (order only) is pending.` — 옛 마지막 문장은 notes 로 (같은 뜻이 (c) 해석 줄에 남음) | σ* = 진행 기록 10-14 오후 2 ③ (S2 · 2.618–3.927 보간 · 국소 기울기 0.545) · 한정어 = `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md` §4 (vox 0.15 유효값 · 섬유 물성 아님 · SBE 한 점 보정 · DBE = 대소만 · 실험 조건 미확인) · S3 (8 원점 × 두 침대) = 진행 중 · J1 · J2 판정 전 |
| 9 새 표 | (v3.1 p10 상태표 행 `R = 2.07 (order-of-magnitude agreement); Q = 0.84` + 해석 줄) | `Lee 2025 [10]` · `R = 2.07, model / literature: order-of-magnitude agreement, not within the registered band` / `PTFE 1 vs 0.5 wt%` · `Q = 0.84, retained after PTFE: registered model-sensitivity prediction met, not an experimental hit` | `docs/reviews/lee_abs_sigma_e_prereg_20260923.md` §5 (R 2.074 ± 0.004 · Tier 1 · Q 0.840) |
| 9 해석 줄 | (c) `… [16] …` | (c) `… [11] …` (번호만) · 자리 = 그림 바로 아래 · 줄 간격 1.0 | — |
| 9 notes | 8 원점 연구 = v3.1 p10 상태표 행 | `Historical eight-origin study … on hold in the claims ledger (CL-33/34/41), so no result is reported` | `docs/reviews/sdcp_gain_prereg_v2_20260816.md` · `docs/reviews/claims.json` |
| 10 notes | — | Thompson 2026 [12] 감압 (격자 이동 가역 · 선폭 · σ 증가 남음 · ≈1.1–1.8 GPa 까지만 · σ 는 다른 셀) · Faka 2026 [13] in-die ↔ out-of-die Heckel 구분 (그 논문은 in-die 만) | 두 정본 카드 (§0 표 · 한정어 절) |
| **11 (새)** | — | 제목 `Problem 4: what the 300 MPa plate reaction contains` · 본문 1 `The 300 MPa stop criterion reads the plate reaction during compression, which includes global viscous damping: in one 7:3 bed the drag is 57.9 % of the target force (750 N, deck units).` · 본문 2 `At fixed platen the same bed relaxes to 165 MPa; a servo branch holding the target force (damping 1e-5) instead compacts it further (111.05 → 105.84 µm) — model-internal until the open checks pass.` · 표 (열린 검사 셋 = MV-01 · MV-02 · MV-08) · 그림 F_p4 (a) 판 압력 300.9 / 165.3 / 299.3 MPa (b) ε_sphere 14.95 / 10.77 % · 등록 띠 8.3–11.7 % | `docs/reviews/findings.json` DEMP-01 (434.3 N = 750 N 의 57.9 % · 750 N = 0.30 덱 MPa × 판 면적 0.0025 (덱 단위 · `docs/dem_governing_equations_background_20261011.md` §9) · 165 MPa) · MV-01 · MV-02 · MV-08 (open) · `docs/data/ps73_damping_branch_20261007/README.md` §1 (165.34) · §4 (B1 · B2 결과 전 등록) · §12-4 (300.906 · 111.052 µm · ε 14.953 % · 434.18 N = 57.89 % / 299.274 · 105.842 µm · ε 10.769 % · 13 SE 소실) · notes 의 결론 문장 = `docs/reviews/codex_review_model_validation_20261008.md` Q11 문안 ("static 300 MPa" 는 그 조건문 안에만) |
| 12–14 notes | — | Hersey 1975 [4] (무작위 기준 균질 지표는 정렬 혼합물에 만족스럽지 않다 · 정렬 혼합) · Egermann & Orr 1983 [5] (상호작용 혼합 · 'ordered' = σ < σ_R) · Kissel 2026 [6] (고강도 믹서 거친 입자 DEM · 한 입자종 · 점착 없음 · 비동력은 고속에서만 맞음 · 피복 = 응력 강도) · Kim 2012 [7] (LiNiO₂ · LiCoO₂ 청정 슬랩 DFT · 계산한 모든 면에서 LNO 낮음 · 결합 절단 에너지 ≠ 입자 접촉 점착 W) | 네 정본 카드 · 용어 = `docs/hetero_thesis.md` §2-5 (1저자 10-14 비준 문안) · §2-8 |
| 14 꼬리표 | — | `Literature: fines adhering to carriers — ordered mixing [4], interactive mixture [5]; clean-slab DFT γ: LiNiO₂ < LiCoO₂ [7]` | 같은 카드 |
| 15 오른쪽 항목 | `Unloading: springback and measured thickness` | `Unloading (springback vs. measured thickness): history test passed; kit re-review HOLD, fixes ratified` | `docs/reviews/dem_unloading_history_test_20261014/README.md` (H0–H5 PASS) · `docs/reviews/codex_review_dem_unloading_kit_20261014.md` (HOLD · ULKR-01–12) · 진행 기록 10-14 오후 2 ② (수정 계획 Q1–Q9 비준) |
| 15 결론 줄 | `Pending: separate launch approvals for the updated 194-bed run and the 20-bed extension.` | 삭제 (1저자 결정 2) | — |
| 15 새 띠 | — | `DEM protocol generation 2 — plan, no runs yet` · insertion → stabilization → compression → servo → relaxation → platen removal → unloading · `SE true density 1.64 g cm⁻³ (lab standard, unverified) · E_SE set so that pure-SE beds reach ε_union = 10–13 % after 300 MPa and relaxation (ε_sphere kept internally) · Heckel analysis redone` | 진행 기록 10-14 저녁 2 · 저녁 3 (단계 · 1.64 · 10–13 % union) · MV-03 (union 만으로는 질량 공극률 불일치를 못 푼다 = notes) · "ε_sphere kept internally" · "Heckel analysis redone" = 1저자 10-14 결정 6 문구 (진행 기록에 아직 없음) |
| 16 새 줄 | — | `DEM loading: the nominal 300 MPa plate reaction includes damping; a revised protocol is planned` | 11 장 · 15 장 요약 (새 숫자 없음) |
| 17 | 16 항목 | 13 항목 (인용된 것만) · 머리 셋 · 번호 v3.1 → v3.2: [7]→[2] · [15]→[3] · [12]→[10] · [16]→[11] · [1] · [8] · [9] 그대로 | 서지 = 정본 카드 (검사 A6 = 카드 실재 + 서지 낱말 대조) · [2] = `docs/data/liggghts_add_pair_pin.json` (커밋 3d5c00f · 날짜 = `docs/data/liggghts_3d5c00f_dem_eq_source_20261009/README.md`) |
| 다리 줄 15 | — | 내용 장 2–16 · 바닥글 띠 같은 자리 · 12 pt 기울임 · 숫자 없음 (목록 = `BRIDGES`) | 장 제목 · 본문에서만 |

## 3. 새 3 장 (DEM 지배방정식) — 복사 방법

- 원 슬라이드의 식 여덟 (`mc:AlternateContent` · Choice `Requires="a14"` 안 `a14:m` → `m:oMathPara` · Fallback = 대체 그림) · 힘 그림 무리 · 판 틀 그림 · 계산 순서 띠를 **관계 (`r:embed` → 새 image part) 와 함께 복사**했다.  식을 다시 타이핑하지 않았다.
- 검사 A8 = 식 XML (C14N) 바이트 같음 8 / 8 · 대체 그림 바이트 같음 8 / 8 · 그림 둘 바이트 같음 · Choice 의 `a14` 이름공간 유지.
- 바꾼 것 = 한글 라벨 → 영어 (`TRANS` 표 — ① Translation · ② Rotation · ③ Normal contact force · ④ Tangential friction · rolling resistance · ⑤ Contact stiffness · Load · 판 제목 · 탭) · 프로젝트 머리 (한글) 삭제 · 배치 (`xfrm`) · 대체 그림의 `fillRect` (원 슬라이드는 식 무리를 가로 0.717 배로 눌러 넣었고 대체 그림도 그 크기에서 그려졌다 → 식 상자 폭 = 원래 3.461 in 그대로 · 높이만 필요한 만큼 · `fillRect` 다시 계산 · 전부 ≤ 0).
- 한글 본문 한 줄 (판 안) → 영어 두 상자 (왼쪽 열 · 힘 그림 아래): `Per particle: translational and rotational equations of motion; per contact pair: contact force and rolling-resistance torque.` · `Global damping −γv_i in ①: γ = 0.5 during stabilization and compression, 1e-5 during settling and relaxation (input-deck units) — see Problem 4.` (`docs/dem_governing_equations_background_20261011.md` §8.2).
- 한정어 (notes) = LIGGGHTS-PUBLIC 3.8.0 hooke/hysteresis 의 **구현식** (소스에서 읽음 · 런으로 다시 유도하지 않음) [2] · 선형 이력 법칙 = Luding 2008 [1] · ③ = 비포화 가지만 · ④ = 스프링 부분 (비미끄럼 단계 접선 감쇠 생략) · k_t = k_n · 구름 토크 = k_n δ · k1 ∝ m*^(1/5) V^(2/5) (V = 강성 입력) · E_SE 1.35 GPa = 보정 입력 · 전역 감쇠 = DEMP-01 open.
- ⚠ **PowerPoint 표시 미확인** — LibreOffice 는 OMML 을 그리지 않고 대체 그림을 그린다.  우리 PDF · PNG 의 식은 대체 그림이다.  PowerPoint 렌더가 가능하면 3 장의 식 줄바꿈 · 잘림을 봐 주십시오.

## 4. 검사 기록 (시험 먼저)

| 대상 | 검사 수 | 실패 |
|---|---:|---:|
| v3.1 덱 — 구현 **전** 에 쓴 v3.2 검사 | 202 | 125 |
| v3.1 덱 — 최종 검사기 | 204 | 124 |
| **v3.2 덱 — 최종 검사기** | **245** | **0** |

- 기록 = `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_2_fix/` (`testfirst_v32.json` · `finalchecks_on_v31.json` · `checks_v32.json` · `cmp_codex_v31.py` · `cmp_codex_v31.json`).
- 항목 (A1–A12) = 장 수 18 · 절 / 제목 · 194 / LHS / ML / 데이터셋 / Latin 없음 (14 장 notes 의 v3.1 문장 "about 194×" (접착 산술) 하나만 예외) · 다리 줄 (문구 · 12 pt 기울임 · 한 줄 · 숫자 없음 · 같은 자리) · 손대지 않은 장 동일 · 참고문헌 ↔ 정본 카드 · 필수 / 금지 문구 (v3.1 목록 + 새 장) · 식 복사 (A8) · F_p4 값 = README 기록 문자열 · 철회값 0 · 내부 식별자 0 · 단어 ≤ 100 / 120 · 본문 ≥ 15 pt · 해석 줄 ≥ 12 pt · 겹침 · 바닥 · 도형 id 유일 · notes 의 리포 경로 실재.
- 제작자 검사는 판정 근거가 아니다 (v3.1 판정 §2 와 같다).  위 기록은 "검사가 옛 판에서 실패하고 새 판에서 통과한다" 는 것만 보인다.

## 5. 확인 질문 (바뀐 장만)

| Q | 질문 |
|---|---|
| Q1 | **11 장 (Problem 4)** — 본문 2 의 "a servo branch holding the target force (damping 1e-5) instead compacts it further … model-internal until the open checks pass" 가 Q11 문안 · MV-01 / 02 / 08 한정 안에 있는가.  가지 B 는 결합 프로토콜 (판 재생성 = 이력 초기화 + 감쇠 낮춤 + 힘 유지) 이다 — 화면은 표 2 행과 해석 줄, notes (ii) 로 그 한정을 단다.  화면 본문에 결합 프로토콜을 직접 써야 하는가. |
| Q2 | **11 장 그림 F_p4** — 값이 README §12-4 · DEMP-01 기록과 같고 (b) 의 등록 띠 (8.3–11.7 %) · 빗금 (= 검사 미완) 표시가 결과를 과장하지 않는가. |
| Q3 | **3 장** — 식 · 그림 = 원 슬라이드 그대로 (A8) 이고 notes 한정어가 충분한가.  왼쪽 열의 감쇠 문장 (γ 0.5 / 1e-5 · 덱 단위) 이 §8.2 와 맞는가.  가능하면 PowerPoint 표시 확인. |
| Q4 | **9 장** — σ_VGCF* 3.41 S cm⁻¹ 문장 ("effective value" · "order only" · "pending") 과 R / Q 표 두 줄 ("not within the registered band" · "not an experimental hit") 이 등록 §4 · Lee 등록 §5 범위 안인가.  옛 본문 마지막 문장을 notes 로 옮긴 것 (같은 뜻이 (c) 해석 줄에 남음) 이 괜찮은가. |
| Q5 | **5 장 표** — `Lab anchor (planned)` 행이 결과 없는 계획으로만 읽히는가.  큰 입자 LPSCl 펠릿은 1저자 10-14 결정이다 (진행 기록에는 아직 권고 · "답 대기"). |
| Q6 | **문헌 (7 · 10 · 12–14 장)** — 꼬리표 · notes 가 카드 범위 안이고 모델 검증으로 읽히지 않는가.  특히 7 장 꼬리표 (순수 SE · in-die · "not composite beds") 와 14 장 꼬리표 (Kim 2012 = LiNiO₂ · LiCoO₂ 끝 조성 · 청정 슬랩). |
| Q7 | **15 · 16 장** — 언로딩 상태 문구 (이력 시험 PASS · 키트 재검토 HOLD · 수정 비준) 와 세대 2 띠 ("plan, no runs yet") 가 과장 없는가.  16 장 "DEM loading" 줄은 지시 목록 밖에서 넣었다 — 빼는 것이 나은가. |
| Q8 | **17 장 · 다리 줄** — 참고문헌 13 · 번호 바꿈 · 미인용 0 · 잘못된 인용 0 이 맞는가.  다리 줄 15 개 중 장 밖 주장으로 읽히는 것이 있는가 (예: 6 장 "Model chain set — next: results from the simulated beds"). |

장 순서에서 생기는 논리 문제 (순서는 1저자 결정대로 두었다 · 의견만 주십시오):
① 6 장 발표자 그림 (i) = 7:3 침대의 접촉망 전류 경로인데 접촉망 (8 장) · 7:3 침대 (7 장) 는 뒤에 나온다.
② 4 장 Luding 크롭 (이력 법칙) 이 3 장 식 ③ 과 겹치고, 4 장 notes 의 "감쇠 58 %" 가 11 장과 겹친다 (손대지 않은 장).
③ 7 장 porosity · 10 장 하중 분담이 쓰는 "300 MPa" 의 속은 11 장에서 나온다 (11 장 notes = "세대 1" 표지).
④ 5 장 보정 표적 "10 % at 300 MPa" (CL-94 · 우리 보정 표적) 와 15 장 세대 2 의 "ε_union 10–13 %" 는 다른 목표다.

## 6. 묶음 (ZIP v8 · 발송 = 1저자)

- v3.2 PPTX + PDF + 렌더 PNG 18 장 + `MANIFEST` (해시 · 장 대응).
- `docs/seminar_20261013/` (생성기 v3.2 · v3.1 생성기 · `figs_v3/` (F_p4 png / svg / csv 포함) · `slide_text_v32.md` · `slide_sources_v32.json` · README).
- 이 요청서 + `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_2_fix/` + `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_1_closure/evidence/pptx.json` (동일성 대조의 기준).
- 1저자 10-09 지배방정식 슬라이드 (3 장 식 · 그림의 원본 · §0 해시).
- 이 판정은 시뮬레이션 발사 · 194 / 보충 20 / v1.3 배포 · 모델 검증 승인과 무관하다 (발표물 한정).
