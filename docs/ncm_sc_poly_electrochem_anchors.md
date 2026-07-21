# NMC811 소립 단결정(SC) vs 대립 다결정(PC) 전기화학 앵커 — D_s · i0

2026-07-21, 4-에이전트 리서치(wf_d6b11be7: 로컬 litdb/PDF + 웹) + 적대 검증(32/41 판정
완료 — CONFIRMED/PLAUSIBLE만 수록, 출처불명 1건 제외).  STEP4 per-particle 분리
(`step4_dyn --d-s-poly/--d-s-sc/--i0-poly/--i0-sc`, 킷 `--step4-ds-*`)의 값 공급원.
§F1: 출판값만, 단위 원문 그대로 병기, confidence 라벨.

## 0. 스케일 규약 (필수 — 리뷰 #0 MAJOR)
STEP4의 D_s는 **입자-반경(r_um) 스케일의 effective D** (구형확산 τ=R²/D).  따라서:
- **poly(대립 ~6µm 반경)**: 2차입자-반경 규약의 DFN-fit/GITT effective D 사용
  (Chen2020이 정확히 이 규약 — r=5.22µm 대표입자로 D를 피팅).
- **SC(소립 ~2µm 반경)**: 단결정 입자 GITT/모델 D 사용.
- 1차결정(grain/µSR) D를 2차입자 반경과 조합하면 **스케일 불일치 = 금지.**

## 1. ★ 핵심 발견 — 액체-셀 SC/PC 순서는 ASSB에서 뒤집힌다
액체 셀 GITT: **PC가 SC보다 ~1오더 빠름** (PC 1e-10–1e-9 vs SC 1e-11–1e-10 cm²/s,
Trevisanello 2021) — 이유는 첫 충전 입계균열에 **전해액이 침투**해 유효 확산길이가
1차결정(sub-µm)로 줄기 때문.  **ASSB에선 SE가 균열에 침투 불가** (Ruess 2020: 고체
셀은 균열 무관 = monolithic 거동; Jung 2023 랩 실측: GITT 분극 ASSB에선 SC<PC로
역전, 5C retention SC 74.0% vs PC 41.6%).
⇒ **액체-셀 PC-빠름 GITT 값(1e-14–1e-13 m²/s)을 우리 ASSB 모델의 poly에 이식 금지.**
poly-in-ASSB는 2차입자-반경 monolithic effective D (DFN-fit 계열)가 정직한 선택.

## 2. D_s 앵커
| 값 (원문 단위) | m²/s 환산 | 대상/조건 | 출처 | 신뢰 |
|---|---|---|---|---|
| SC 1e-11–1e-10 cm²/s | **1e-15–1e-14** | GITT, 액체 반쪽셀 (SC는 균열무관→ASSB 이식 가능) | Trevisanello 2021 AEM 2003400 | web_abstract |
| PC 1e-10–1e-9 cm²/s | 1e-14–1e-13 | GITT, 액체 — ★균열-침투 부스트, **ASSB 이식 금지(§1)** | Trevisanello 2021 | web_abstract |
| SC ~1e-9→1e-12 cm²/s (SOC 강의존) | 1e-13→1e-16 | in-situ EIS+GITT, 방전말 급락 | Ge 2021 Angew 60:17350 | web_abstract |
| **poly 4e-15 m²/s (상수)** | 4e-15 | **DFN-fit, r=5.22µm 규약** = 우리 스케일 정합; LG M50 NMC811 | **Chen 2020 JES 167:080534** (OCP 앵커와 동일 계보) | web_fulltext |
| poly D(sto) 3-Gaussian 식 ×2.7 | ~1e-15–1e-14 | 동일 셀 SOC-의존 개선판 (파라미터 전문 확보) | O'Regan 2022 EA 425:140700 | web_fulltext |
| poly 3e-14 m²/s | 3e-14 | FEM 입력 (측정 아님), NCA/LPSCl r=5µm — **현행 STEP4 기본값의 출처** | Kang&Shin 2025 SI T.S4 | pdf_local |
| 격자(1차결정) ~3.4e-11 cm²/s | 3.4e-15 | operando µSR (입계 무관 Å-스케일) — poly 하한 sanity | McClelland 2023 Chem.Mater. | PLAUSIBLE |
| SC-NCA 모델 1.5e-15 m²/s | 1.5e-15 | 디지털트윈 모델 입력 (SC 5µm) | Koo 2025 (litdb) | secondary |
| NCA GITT 스프레드 1e-15–1e-14 | — | A8 프리셋 조사 재인용 | docs/nca_material_preset.md | secondary |
| 사이클 열화: PTFE ~1e-10 유지 vs NBR →1e-12 cm²/s @50cyc | 1e-14→1e-16 | 사이클-GITT (바인더 의존) — A10 연결점 | Hong 2026 (litdb) | secondary |

## 3. i0 / R_ct 앵커
| 값 | 대상/조건 | 출처 | 신뢰 |
|---|---|---|---|
| Chen2020 m_ref=3.42e-6 (A/m²)(m³/mol)^1.5 (→ j0 ~0.6–0.9 A/m² @중간 SOC, 액체 c_e 1M) | poly, 액체 BV | Chen 2020 (PyBaMM 소스 검증) | web_fulltext |
| O'Regan i_ref=5.028 A/m², α=0.43 | poly, 액체 | O'Regan 2022 | web_fulltext |
| FEM 입력 i0=10 A/m² | poly NCA/LPSCl (측정 아님) | Kang&Shin 2025 | pdf_local |
| R_ct uncoated 453/290/382 → LNO-coated 22.4/18.2/17.2 Ω·cm² (62/72/82wt%) | NCM811/LPSCl 3전극, 30°C — 코팅이 ~20× 지배 | Kim 2025 EA 147413 | pdf_local |
| facet (201) 1.50 vs (003) ~0.06 mA/cm² (25×) | SC facet-분해 — SC i0의 표면-의존 근거 | Nat.Comm. facet 연구 | web_abstract |
| ASSB SC vs PC R_ct: **정성만** (액체 R_ct PC<SC; ASSB 역전 주장, 수치 無) | Jung 2023 (랩) Fig S7/6d | pdf_local |

**⚠ i0의 SC/PC 분리 정량값은 ASSB 문헌에 부재** (facet/정성뿐) — §F1에 따라 **i0 분리
값은 미지정** (메커니즘만 배선).  R_ct 앵커에서 유효-i0 역산은 가능하나 코팅(LNO)
지배가 결정계(SC/PC)보다 커서 분리 근거로 부적합.

## 4. 추천 (STEP4 bimodal 12:4µm-직경 = 반경 6:2 베드)
- **공유 기본 유지**: `--d-s 3e-14`, `--i0 2.0` (프로덕션 연속성 — 회귀 0).
- **분리 시작점 (스윕 권장, 단정 금지)**:
  - `--d-s-sc`: **1.5e-15–1e-14** 밴드 (Trevisanello SC + Koo; 중앙 ~3e-15)
  - `--d-s-poly`: **4e-15**(Chen2020, 스케일-규약 정합 최우선) … 3e-14(Kang&Shin FEM) 밴드
  - 주의: 이 밴드에서 SC/poly의 **D 자체는 비슷한 오더** — 실제 응답차는 τ=R²/D의
    **R² (9×)** 가 지배 (poly 6µm: τ~9000s vs SC 2µm @3e-15: τ~1300s).  Jung 5C
    SC 74/PC 42% 방향과 일치 — 검증점.
  - `--i0-poly/-sc`: **값 미지정** (§3) — 민감도 스윕 전용.
- 사이클 열화 궤적(D_s(N), Hong 2026)은 A10 트랙에서 연결.

## 5. 미결
1. ASSB에서 SC/PC D_s 직접 비교 정량 (Jung은 정성 ΔV만) — 랩 GITT 디지타이즈 후보.
2. i0 SC/PC 분리 정량 (부재 확인됨).
3. 검증 마지막 청크(익명 9/41) 판정 도착 시 본 문서 갱신.
