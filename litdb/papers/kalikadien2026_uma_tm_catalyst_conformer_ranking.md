<!-- digest: litdb-curator, 2026-08-25. papers/_TEMPLATE.md 확장판 (depth ref = zuo2022 / petmad2026) -->
# Performance of Meta's Universal Model for Atoms across the Conformational and Configurational Space of Diverse Transition-Metal Catalysts — Kalikadien & Pidko (J. Phys. Chem. A 2026)

> slug `kalikadien2026_uma_tm_catalyst_conformer_ranking` · DOI `10.1021/acs.jpca.5c07061` · type `MLIP 벤치마크 (UMA single-point) + 참조 DFT` · PDF `a8e0b114-65._Perforalysts.pdf` · digested `2026-08-25` · status ✅ · 태그 **[외부·methods·UMA 감사]**
> elements: Ni, Ir, Ru, Mn, P, Cl, C, H, N, O
> methods: DFT, MLIP

> **저자**: Adarsh V. Kalikadien¹, **Evgeny A. Pidko**¹\* (¹ Inorganic Systems Engineering, Dept. of Chemical Engineering, **TU Delft**) · *J. Phys. Chem. A* **130**, 1897–1904 (2026) · Open Access CC-BY 4.0 · Received 2025-10-14 / Revised 2026-01-06 / Accepted 2026-01-07 / Published 2026-02-18
> **자금**: Janssen Pharmaceutica NV (J&J) · NWO Snellius 국가슈퍼컴퓨터
> **데이터 공개**: 4TU.ResearchData `10.4121/6b178daf-e1c0-4c99-840f-06d382f37945` (데이터셋 + 리간드 목록 + 재현 코드 + readme)

> ⚠ **파일명 주의**: 업로드 PDF 이름 `65._Perforalysts.pdf` 는 `Perfor(mance) … (Cat)alysts` 가 잘린 것이다. "Perforalysts" 라는 논문·용어는 존재하지 않는다.

---

## 0. 이 digest 를 읽는 법 (먼저)

이건 **재료 논문이 아니라 우리 계산기(UMA)를 남이 감사한 논문**이다. 그래서:

1. **여기서 물성값을 가져올 것은 하나도 없다.** 조성이 Ni/Ir/Ru/Mn 유기금속 착물이고, 우리 계(황화물 SE, LPSCl)와 **화학적 겹침이 0** 이다. §12 에 "겹침 없음"을 명시했다.
2. **가져올 것은 딱 하나 — "UMA 는 어디서 무너지나"의 외부 정량 표본**이다. 그리고 그 표본이 **우리가 쓰는 것과 같은 체크포인트 세대**(`uma-s-1.1` = 우리 `uma-s-1p1`)를 쓴다. 단 **task 가 다르다**(그들 `omol`, 우리 `omat`).
3. 이 논문의 결론 문장("실패는 near-degenerate 영역에만 몰린다")은 **안심시키는 문장이지만, 우리가 실제로 겪은 UMA 실패 2건을 설명하지 못한다.** §12-② 가 그 얘기다. 그 절을 안 읽으면 이 digest 를 잘못 쓰게 된다.
4. `figure-read ≈` 표시는 **내가 크로핑 이미지를 눈으로 읽은 값**이다. 본문 명시값과 구분해서 썼다.
5. §14 에 **내가 직접 검산해서 논문 서술과 어긋나는 것을 찾은 기록**이 있다 — 특히 §14-A(Data set 2 의 "신뢰율"이 사실은 무슨 뜻인지)는 이 논문을 인용할 때 반드시 같이 읽어야 한다.

> 🔗 **짝 문헌**: `papers/uma2026_family_of_universal_models_for_atoms.md` (Wood et al., FAIR at Meta, arXiv 2506.23971v2)
> = **UMA 자체의 1차 사양서**. 저쪽이 *"모델이 무엇인가"*, 이쪽이 *"제3자가 그 모델을 써 보니 어땠나"* 다.
> 두 digest 는 **같이 읽어야 뜻이 산다** — 특히 이 논문의 `omol` task 정의·OMol25 학습분포는 저쪽에 있다.

---

## 1. 한 줄 요약

**UMA-s-1.1(OMol25 task) 을 전이금속 촉매 착물의 conformer/configuration 상대에너지 랭킹에 시험했더니, 집계지표(R² 0.96–0.97, RMSE 2.4–4.9 kJ/mol)는 훌륭한데 리간드별 랭킹 신뢰율은 84 %(강직) → 53 %(유연) / 61 %(Ru) → 44 %(Mn) 로 무너진다.** 저자 결론: 실패는 **상대에너지 차가 2–5 kJ/mol(21–52 meV) 이하인 near-degenerate 영역**에 몰려 있고, 그 영역은 DFT 자신도 유일한 정답을 못 주는 곳이므로 "치명적이지 않다" — 다만 **집계지표만 보고 MLIP 을 믿으면 안 된다.**

## 2. 메타 / 동기

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| A. V. Kalikadien, E. A. Pidko (TU Delft) | J. Phys. Chem. A 2026, 130, 1897–1904 | 10.1021/acs.jpca.5c07061 | [L]Ni(II)Cl₂ · [L]Ni(II)(CH₃CN)(*p*-OMe-C₆H₄)⁺ · [L]IrH₃(CH₃CN) · [L]RuH₂(CO)(CH₃CN) · [L]MnH(CO)₂(CH₃CN) (L = bisphosphine) | **MLIP 벤치마크** (UMA single-point vs 자체 참조 DFT). 실험 0, MD 0, NEB 0 |

**동기 (§1 의 비용 사고실험, 인용 가능)**
- 전형적 TM 착물 1개: **32 CPU core × 4 h** (hybrid DFT + double-ζ 로 구조최적화 + 진동수 해석) = **128 SBU**
- 네덜란드 SBU 단가 **€0.01** (저자 표현: "optimistic")
- ⇒ **1만 개 착물 최적화 ≈ €12,800.** 고속 스크리닝에선 이 규모가 흔하다 → "chemical accuracy 를 지키면서 비용을 줄이는 reductionist 접근이 필요하다"
- 대비: UMA single-point 는 **소비자용 GPU(RTX 3050 노트북)에서 구조당 수 초**

**연구 질문 (저자 표현 그대로)**: *"UMA 가 예측하는 서로 다른 배열의 상대 안정성이 실용적으로 쓸 만큼 정확한가?"* — 즉 **에너지 오차가 아니라 랭킹(순위) 이 보존되는가**.

**이 논문의 자기 제한 (중요)**: 저자들은 **UMA 로 기하최적화를 하지 않았다.** 본문 §1 마지막:
> *"An ideal long-term goal would be to employ MLIPs directly in geometry optimization... however, the methodology is not yet stable enough for routine application to complex systems (refs 20,21). In the present work, therefore, our focus is restricted to assessing how well UMA can reproduce DFT-calculated energies **on DFT-optimized geometries**."*

⇒ **이 벤치는 UMA 의 single-point 에너지만 잰다. 힘·이완·MD·장벽은 하나도 안 잰다.** (§12-① 에서 이게 우리에게 왜 결정적인지 다룬다.)

## 3. 핵심 수치 총정리

### 3.1 집계 지표 (Pearson R² · RMSE)

| 데이터셋 | 계 | 구조 수 | R² | RMSE (kJ/mol) | RMSE (meV) | 그림 |
|---|---|---|---|---|---|---|
| **1-rigid** | [L]Ni(II)Cl₂ conformers | 746 (19 리간드) | **0.96** | **2.39** (본문 반올림 2.4) | ≈ 24.8 | `Fig. 2`a |
| **1-flexible** | [L]Ni(II)(CH₃CN)(*p*-OMeC₆H₄)⁺ conformers | 1260 (19 리간드) | **0.68** | **9.07** (본문 9.1) | ≈ 94.0 | `Fig. 2`b |
| **2** | Ir/Ru/Mn octahedral configurations | 909 geometries (88 리간드 × 3 금속) | **0.97** | **4.92** (본문 4.9) | ≈ 51.0 | `Fig. 4` |

> 단위 변환: 1 kJ/mol = **10.364 meV**. ⚠ 이 RMSE 는 **구조당(착물 1개당)** 값이지 **원자당**이 아니다. 착물이 대략 50–120 원자이므로 원자당으로는 **0.2–1 meV/atom** 수준 — 우리 Li₃PS₄ 벤치의 13.5 meV/atom(총에너지·원소참조 보정 후)과 **같은 축이 아니다.** 섞어서 "UMA 가 분자에서 더 정확하다" 같은 말을 하면 안 된다.

### 3.2 랭킹 신뢰율 (per-ligand Spearman ρ, 기준 ρ > 0.6 **AND** p < 0.05)

| 계 | 신뢰 비율 | 리간드당 표본 n | 그림 |
|---|---|---|---|
| Data set 1 — **rigid** [L]NiCl₂ | **84 %** (19 중 16) | ≈ 39 conformers 평균 (746/19), 최소 4 | `Fig. 3`a |
| Data set 1 — **flexible** [L]Ni(CH₃CN)(Ar)⁺ | **53 %** (19 중 10) | ≈ 66 평균 (1260/19), **L2 는 8 · L12 는 6** | `Fig. 3`b |
| Data set 2 — **Ru(II)** | **61 %** | **4** (H–H / C–N / C–H / H–N axial) | `Fig. 5` |
| Data set 2 — **Mn(I)** | **44 %** | **4** (C–C / C–N / C–H / H–N axial) | `Fig. 5` |
| Data set 2 — 두 금속 합 | **53 %** | | `Fig. 5` |
| Data set 2 — **Ir(III)** | **평가 불가 → 제외** | **2** (H–H / H–N axial) — 랭킹 상관을 못 냄 | — |

> ⚠⚠ **두 개의 "53 %" 를 혼동하지 말 것.** 하나는 *Data set 1 flexible 의 리간드 53 %*, 다른 하나는 *Data set 2 의 리간드–금속 조합 53 %* 다. 서로 다른 수이고 서로 다른 표본크기에서 나왔다(§14-A).

### 3.3 실패가 몰리는 에너지 스케일

| 관측 | 값 | 출처 |
|---|---|---|
| Data set 1 랭킹 실패 임계 | conformer 간 ΔE_DFT **< 2 kJ/mol** (≈ 21 meV) | 초록 + §3 (L2·L12 사례) |
| Data set 2 랭킹 실패 임계 | configuration 간 ΔE **< 5 kJ/mol** (≈ 52 meV) | 초록 |
| 성공 사례의 에너지 간격 | L17: 최소 **6 kJ/mol** (Ru H–H 는 **43**, C–N 은 **34**) · L51: 최소 **4 kJ/mol**, 보통 **> 15** | §3 |
| 실패 사례의 에너지 간격 | L133 Mn(C–C·C–H): 기준 대비 **< 2 kJ/mol** · L149 Mn(C–C): **0.2 kJ/mol**, 나머지 Mn 배열 **5 kJ/mol 이내** | §3 |
| 경계 성공 | L149 **Ru** C–N 은 기준에서 **2.3 kJ/mol** 인데도 순위를 맞췄다 | §3 |
| 이전 연구(ref 22) 관측 | Mn 착물은 **10 kJ/mol 안에 여러 배열**이 몰려 있다 | §3 |

### 3.4 계산 비용

| | DFT | UMA |
|---|---|---|
| 하드웨어 | HPC (32 CPU core) | **Dell XPS 15 9520 노트북** — Intel Core i5 12세대 / RAM 32 GB / **NVIDIA RTX 3050** |
| 착물 1개 | ~4 h (최적화 + 진동수) | **수 초** (single-point) |
| 1만 개 | ≈ €12,800 | (본문 미제시 — "seconds per structure" 만) |

> 😅 **PDF 텍스트 함정**: 본문에 *"a Dell **X-ray photoelectron spectroscopy (XPS)** 15 9520 laptop"* 이라고 인쇄돼 있다. 저널 교정이 노트북 모델명 **XPS** 를 XPS 분광법으로 자동 확장한 오식이다. **이 논문은 XPS 측정을 하지 않았다.** 키워드 스크래퍼가 이 논문을 XPS 논문으로 태깅하면 그게 원인이다 — 그래서 위 `methods:` 태그에 XPS 를 **넣지 않았다.**

## 4. 어떤 MLIP 을 어떻게 썼나 ★★ (우리 관심 1번)

| 항목 | 논문 값 | 우리(참고) |
|---|---|---|
| 모델 | **UMA (Universal Model for Atoms), Meta FAIR** | 같음 |
| 변종 | **UMA-**`s`**(small)** — 본문 *"the latest version of the small UMA model"* | **UMA-s** 같음 |
| 버전 | **UMA-s-1.1** | **`uma-s-1p1`** — fairchem 체크포인트 문자열로 **같은 세대** |
| **task** | **OMol25** (분자 task = `omol`). 본문: *"pretrained on the OMol25 data set"* | ⚠ **`omat`** (Open Materials 2024, 주기계) — **다르다** |
| 파라미터 | **150 M total** (본문 명시) | 같은 체크포인트 |
| 왜 small 을 골랐나 | *"we were mainly interested in a single-point energy calculation of structures with less than 1k atoms"* | — |
| 인터페이스 | **ASE (Python)** | 같음 (`FAIRChemCalculator`) |
| 무엇을 계산했나 | **single-point 에너지 only** | 우리는 **이완(cascade) + Langevin NVT MD + 탄성 + NEB** |
| 힘 평가 | ❌ 없음 | 우리 핵심 |
| MD | ❌ 없음 | 우리 핵심 (dt 2 fs, MSD 창 2–50 ps) |
| NEB / 장벽 | ❌ 없음 | 우리 핵심 (NEB 0.528 eV) |
| 파인튜닝 | ❌ 없음 (사전학습 그대로) | 우리도 없음 |
| 스핀·전하 지정 | 본문 미기재 (⚠ OMol25 task 는 charge/spin 을 입력으로 받는다 — 양이온성 flexible 모델에서 이 설정이 결과를 좌우할 수 있는데 **논문에 없다**) | n/a |
| 불확실도(UQ) | ❌ 없음 (UMA 단일모델) | 우리도 없음 — 이게 우리 committee 논의의 배경 |

**⇒ 요약**: *같은 체크포인트 세대, 다른 task head, 다른 화학, single-point 만.*

## 5. 참조 DFT (이 논문이 "정답"으로 삼은 것) ★

| 항목 | 값 |
|---|---|
| **범함수** | **PBE0** (hybrid, 25 % HF exchange) + **D3(BJ)** 분산보정 |
| **기저** | **def2-SVP** (double-ζ + polarization) |
| **코드** | **Gaussian 16 Rev. C.01** (ref 29) |
| **환경** | **기체상(gas phase)** — 용매 모형 없음 |
| **작업** | 전 구조 **완전 기하최적화** + **normal-mode 해석**(국소최소 확인) |
| 허수진동수 처리 | **PyQRC** 로 제거 후 재최적화 (refs 33,34) |
| pseudo / k-points / ecut | **n/a** (전자 all-electron 분자 계산, 주기계 아님) |
| DFT+U | **n/a** |
| AIMD | **없음** |
| **무질서 처리** | **n/a — 주기계 무질서 개념이 없다.** 대신 **입체이성질체 전수 열거 + conformer 탐색** 이 그 자리를 차지한다 (§5.1) |

### 5.1 구조 생성 파이프라인 (우리 "무질서 처리" 칸에 대응하는 것)

1. **MACE Python package** (ref 24) — ⚠⚠ **이건 MACE MLIP 이 아니다.** Chernyshov & Pidko, *JCTC* **2024**, *20*, 2313 의 **"Metal Complex Automated Configuration Enumeration"** 도구로, 전이금속 착물의 **입체화학(가능한 모든 stereoisomer)을 자동 열거**한다. 우리 repo 의 `zhang2026_…mace_finetune…` digest 의 MACE(MLIP)와 **이름만 같은 완전히 다른 물건**이다. 인용할 때 반드시 구분.
2. **Data set 1**: 위 구조들에 **CREST @ GFN2-xTB** 로 exhaustive conformer search (refs 25–27) → 전부 DFT 최적화.
3. **Data set 2**: **RDKit** 로 conformer 생성 → **리간드당 최저에너지 conformer 1개만** 선택 → DFT 최적화.
4. 상대에너지 정의: **ΔE = E_i − E_ref** (같은 리간드 안에서, 기준구조 대비). **UMA 와 DFT 가 완전히 같은 기하(=DFT 최적화 구조)를 쓴다.**

> 🔑 **우리 식으로 옮기면**: 이들의 "conformer 랭킹" = 우리의 **"같은 조성 안 S/Cl 무질서 배열 랭킹"**과 구조적으로 같은 문제다(같은 화학식, 여러 국소최소, 그중 순위). 방법 대응: 그들 MACE+CREST 열거 ↔ 우리 `enumerate → lowest-Ewald` / SQS.

## 6. 평가 지표의 정의와 그 함정 ★★

이 논문의 방법론적 알맹이는 여기다.

**(1) 왜 R²·RMSE 로 부족한가** — 저자 논지: R²는 선형성·정규분포를 가정하는 **Pearson** 계열이고 RMSE 는 평균 편차다. 둘 다 **"같은 리간드 안에서 conformer 순위가 보존됐는가"** 를 직접 재지 않는다. 순위는 conformer 분석의 필수 조건인데 집계지표는 그걸 못 본다.

**(2) 그래서 Spearman ρ** — 값이 아니라 **순위**에만 작용하는 비모수 단조성 지표. 분포 모양과 무관.

**(3) "trusted" 판정 2조건** (둘 다 만족해야 함):
- **ρ > 0.6** ("moderate-to-strong monotonic agreement")
- **p < 0.05** (통계적 유의)
- 추가 필터: **리간드당 conformer ≥ 4개**

**(4) ⚠⚠ 여기가 함정이다 — 같은 문턱이 n 에 따라 전혀 다른 뜻이 된다.**

내가 직접 계산한 표 (scipy `spearmanr` 기본 = t-근사 양측; 정확 permutation 도 병기):

| n (표본 conformer/configuration 수) | p < 0.05 를 통과하려면 필요한 ρ | 비고 |
|---|---|---|
| **4** | **ρ = 1.0 만** (ρ=0.8 → p = 0.20) | **Data set 2 (Ru·Mn)** |
| 5 | ρ ≥ 0.9 (p = 0.037) | |
| 6 | ρ ≥ 0.81 | **L12 flexible (n=6)** |
| 8 | ρ ≥ 0.71 | **L2 flexible (n=8)** |
| 10 | ρ ≥ 0.63 | ← 여기서부터 ρ>0.6 이 실효 문턱이 됨 |
| 20 | ρ ≥ 0.44 | |
| 39 (rigid 평균) | ρ ≥ 0.32 | **Data set 1 rigid** |
| 66 (flexible 평균) | ρ ≥ 0.24 | **Data set 1 flexible** |

> 정확 permutation 으로는 n=4 일 때 ρ=1.0 조차 단측 p=0.0417(겨우 통과)·**양측 p=0.083(불통과)** 이다. 논문이 44 %/61 % 라는 0 이 아닌 값을 보고했으므로 **scipy 기본 t-근사(ρ=1 → p→0)를 썼다고 보는 게 유일하게 일관된 해석**이다.

**⇒ 결론 (§14-A 에서 그림으로 확인):**
- **Data net 1** (n ≈ 39–66): 구속조건은 **ρ > 0.6**. → "84 %/53 %" 는 *"순위가 대체로 맞는가"* 를 잰다.
- **Data set 2** (n = 4): 구속조건은 **p < 0.05**, 그리고 그건 **ρ = 1.0** 을 뜻한다. → "61 %/44 %" 는 *"4개 배열 순위를 **완벽하게** 맞췄는가"* 를 잰다.
- **두 수는 같은 척도가 아니다.** 논문은 *"A similar pattern is observed in Data set 2"* 라며 나란히 놓는다 — **그 병치는 방어되지 않는다.**

## 7. 결과 — 절별 상세 ★

### 7.1 Data set 1 정의

| | rigid | flexible |
|---|---|---|
| 구조 | **[L]Ni(II)Cl₂** (중성, square-planar, Cl₂ 가 **대칭** 배위환경) | **[L]Ni(II)(CH₃CN)(−*p*-OMe(C₆H₄))⁺** (양이온, **비대칭** 배위 → 형태자유도 증가) |
| 화학적 의미 | 전구촉매 모델 | **Ni 촉매 nitrile arylation** 의 중간체 모델 |
| 원래 규모 | 23 리간드 / **2100** conformers | 21 리간드 / **3505** conformers |
| 비교용 필터 후 | **19 리간드 / 746 conformers** | **19 리간드 / 1260 conformers** |

필터 규칙: **rigid·flexible 양쪽 모두 conformer 기하가 완전 수렴한 리간드만** 남김.

### 7.2 Data set 1 — 상관 (`Fig. 2`)

- **(a) rigid**: R² 0.96, RMSE 2.39 kJ/mol. 축 ΔE_UMA **−30 … +50**, ΔE_DFT **−25 … +55** kJ/mol. 점들이 회귀선에 바짝 붙는다. **figure-read ≈ 기울기 1.04** (x=−30 → y≈−29, x=+50 → y≈+54) — UMA 가 DFT 대비 에너지 폭을 **아주 살짝 압축**한다. 절편도 **figure-read ≈ +2 kJ/mol** 로 0 이 아니다(논문 미언급).
- **(b) flexible**: R² 0.68, RMSE 9.07. 축 ΔE_UMA **−60 … +40**, ΔE_DFT **−70 … +60**.
  - **figure-read**: |ΔE| < 25 kJ/mol 의 중앙 덩어리는 **거의 구조가 없는 뭉치**다. 회귀선을 떠받치는 건 왼쪽 아래의 **점 10여 개**(ΔE_UMA −60…−30, ΔE_DFT −70…−55). ⇒ **R² 0.68 은 leverage 점 소수가 만든 값**이고, 정작 랭킹 판정이 일어나는 near-degenerate 구간에는 상관 정보가 거의 없다. 논문의 논지("집계지표가 랭킹을 못 본다")를 그림이 오히려 더 강하게 지지한다.
  - 그 왼쪽 아래 무리는 회귀선보다 **아래**에 있다(선 −53 vs 실제 −65…−68) — 큰 안정화 배열에서 **UMA 가 안정화를 과소평가**하는 계통 경향으로 보인다. **figure-read, 논문 미언급.**

### 7.3 Data set 1 — 랭킹 (`Fig. 3`)

19개 리간드 각각에 대해 Spearman ρ 를 막대로. 파랑 = reliable(ρ>0.6 **그리고** p<0.05), 회색 = not reliable, 빨강 파선 = ρ = 0.6.

**(a) rigid — 16/19 = 84 % 파랑.** 회색 3개: **L6 · L25 · L27**.
**figure-read ≈ 막대 높이 (±0.03)**: L2 0.88 · L4 0.82 · L5 0.82 · **L6 0.26(회색)** · L7 0.68 · L8 0.62 · L11 0.82 · L12 0.91 · **L25 0.64(회색)** · **L27 0.32(회색)** · L28 0.92 · L29 0.62 · L30 0.99 · L31 0.94 · L32 0.68 · L34 0.83 · L35 0.72 · L36 0.96 · L39 0.64.

> ⭐ **그림에서만 나오는 결정적 사실**: **L25 의 회색 막대는 빨간 0.6 점선보다 위에 있다.** ρ 문턱을 넘었는데 회색이라는 건 **p ≥ 0.05 로 떨어졌다**는 뜻 — 즉 그 리간드는 conformer 수가 적다. **⇒ 빨간 점선은 판정선이 아니다.** 그림만 보면 "0.6 위 = 파랑"으로 읽히는데 실제 규칙은 다르다. 논문 본문은 이 불일치를 설명하지 않는다.

**(b) flexible — 10/19 = 53 % 파랑.** 파랑: L7 · L8 · L11 · L25 · L28 · L29 · L31 · L34 · L35 · L39. 회색 9개: L2 · L4 · L5 · L6 · L12 · L27 · L30 · L32 · L36.
**figure-read ≈**: **L2 −0.37** · L4 0.21 · L5 0.50 · L6 0.48 · L7 0.87 · L8 0.93 · L11 0.90 · **L12 −0.81** · L25 0.86 · L27 0.06 · L28 0.88 · L29 0.86 · L30 0.41 · L31 0.73 · L32 0.49 · L34 0.97 · L35 0.88 · L36 0.42 · L39 0.84.

- **음수 ρ 2건 = L2, L12** — 본문의 *"in two cases, a negative Spearman ρ was observed, indicating that UMA predicts the reverse energy ranking"* 와 그림이 정확히 일치. ✅
- **L25 는 rigid 에서 회색(0.64), flexible 에서 파랑(0.86)** 으로 뒤집힌다 — 신뢰성이 유연성에 단조롭지 않다. **figure-read, 논문 미언급.**

**오른쪽 패널의 대표 리간드 5종** (구조식으로 확인):

| 리간드 | 이름 | 구조 (그림에서 확인) | rigid ρ | flexible ρ | 논문 해석 |
|---|---|---|---|---|---|
| **L2** | dCyhpp | P(Cy)₂–(CH₂)₃–P(Cy)₂ (사이클로헥실 ×4, 3탄소 링커) | ≈0.88 ✅ | **≈−0.37** ❌ | flexible 에서 conformer **8개뿐**, ΔE_DFT 전부 **< 2 kJ/mol** |
| **L4** | Dcyppp | P(Cp)₂–(CH₂)₃–P(Cp)₂ (사이클로펜틸 ×4) | ≈0.82 ✅ | ≈0.21 ❌ | 같은 이유(본문은 L2 만 상술) |
| **L7** | dppm | Ph₂P–**CH₂**–PPh₂ (**1탄소** 링커) | ≈0.68 ✅ | ≈0.87 ✅ | 짧은 링커 → 형태공간 제한 → 양쪽 다 좋음 |
| **L8** | dppe | Ph₂P–(CH₂)₂–PPh₂ (**2탄소**) | ≈0.62 ✅ | ≈0.93 ✅ | 동상 |
| **L12** | dppb | Ph₂P–(CH₂)₄–PPh₂ (**4탄소**) | ≈0.91 ✅ | **≈−0.81** ❌ | conformer **6개뿐**, ΔE_DFT **< 2 kJ/mol** |

> 🔑 **읽어낼 물리**: *링커가 길고 치환기가 알킬(sp³)일수록 → 형태공간이 넓고 conformer 들이 에너지적으로 붙는다 → 랭킹이 무너진다.* 반대로 **짧은 링커(dppm/dppe)** 는 형태공간 자체가 좁아 안전하다.

### 7.4 Data set 2 정의

- **88개 chiral bisphosphine 리간드** × 3 금속 → 입체이성질체 샘플링 후 **909 geometries**.
- 3 계열: **[L]IrH₃(CH₃CN)** · **[L]RuH₂(CO)(CH₃CN)** · **[L]MnH(CO)₂(CH₃CN)** — 균일계 **수소화(hydrogenation)** 촉매.
- 배열 명명 = **축방향(axial) 자리의 주개원자 쌍**. `Fig. 1` 에서 직접 확인:
  - **Ir(III)**: H–H axial, H–N axial → **2개**
  - **Ru(II)**: H–H, C–N, C–H, H–N axial → **4개**
  - **Mn(I)**: C–C, C–N, C–H, H–N axial → **4개**
- 88 × (2+4+4) = 880 ≈ 909 (나머지 29 는 추가 입체이성질체).

### 7.5 Data set 2 — 상관 (`Fig. 4`)

- R² **0.97**, RMSE **4.92 kJ/mol**. 축 −200 … +200 kJ/mol(최대점 ≈ +230/+207). 색: **Ru 빨강 · Mn 파랑 · Ir 초록**.
- **figure-read 비판**: R² 0.97 은 **±200 kJ/mol 이라는 넓은 동적범위** 덕이다. 실제 랭킹이 결정되는 |ΔE| < 50 kJ/mol 의 조밀한 코어에서는 선 주위 산포가 RMSE(≈5 kJ/mol)와 같은 크기다. **동적범위를 넓히면 R² 는 언제나 올라간다** — 이건 모델이 좋아진 게 아니다.
- **figure-read (약한 관측, 논문 미언급)**: 초록(**Ir**) 점들이 0 … +50 kJ/mol 구간에서 회귀선보다 **살짝 위**에 몰려 있다 → 금속별 계통 오프셋 가능성. 눈대중이고 Ir 은 랭킹 분석에서 제외됐으므로 **강하게 주장하지 않는다.**

### 7.6 Data set 2 — 랭킹 (`Fig. 5`)

Mn·Ru 2열 × 리간드 행 히트맵. 셀 색 = ρ (빨강 0 → 초록 1.0), 흰 셀 = 해당 금속에서 배열 수 부족(≥4 필터 탈락)으로 평가 제외. **Ir 은 열 자체가 없다**(배열 2개).

- 본문 수치: **Ru 61 % · Mn 44 % · 합 53 %** reliable.
- **⚠ 그림과 본문이 겉보기에 충돌한다**: 히트맵은 **양쪽 열 모두 압도적으로 초록**이다. Mn 열의 명백한 실패는 **빨강 3줄(ρ≈0.2: L70·L133·L147 근방)** + **노랑 5–6줄(ρ≈0.4: L53·L59·L94·L143·L183 근방)** 뿐이고, Ru 열은 **노랑 1줄(L47 근방, ρ≈0.4)** 이 전부다. 그림만 보면 신뢰율이 90 % 는 돼 보인다.
- **해소**: §6-(4) 의 산술. n=4 라서 **ρ=0.8 셀은 p=0.20 으로 전부 탈락**한다. 내 픽셀 계수(§14-A): Mn 열 **ρ=0.8 셀이 채점대상의 38.8 %**, Ru 열 **25.0 %**. 이걸 빼면 본문 수치와 맞아떨어진다.
- **⇒ Data set 2 의 "신뢰율"은 사실상 "UMA 가 4개 배열 순위를 100 % 맞춘 리간드의 비율"이다.**

**금속 간 차이에 대한 저자 설명** (기전 주장, 계산 근거는 없음):
> Mn(I) 착물은 **더 fluxional** 하다 → PES 가 복잡하고 얕다 → 범용 MLIP 이 배우기 어렵다. 반면 Ru(II) 는 같은 리간드장에서 **더 강직하고 구조가 잘 정의된다**.

### 7.7 대표 리간드 4종 (`Fig. 5` 오른쪽)

| 리간드 | 이름 | Mn | Ru | 에너지 간격 |
|---|---|---|---|---|
| **L17** | (R)-BINAM-P | **ρ = 1.0** ✅ | **ρ = 1.0** ✅ | 최소 **6 kJ/mol**, Ru H–H **43**, C–N **34** |
| **L51** | (S)-iPr-BIPHEP | **ρ = 1.0** ✅ | **ρ = 1.0** ✅ | 최소 **4 kJ/mol**(Mn C–N), 보통 **> 15** |
| **L133** | (R)-An-PhanePhos | ❌ (그림 **ρ ≈ 0.2**, 빨강) | ✅ | Ru 최소 6 kJ/mol vs **Mn C–C·C–H 는 기준 대비 < 2 kJ/mol** |
| **L149** | (R)-Tol-GarPhos | ❌ | ✅ | Ru C–N **2.3 kJ/mol 인데도 맞춤** · **Mn C–C 0.2 kJ/mol**, 나머지 5 kJ/mol 이내 → 틀림 |

> 표기 오류: `Fig. 5` 오른쪽 라벨이 **"149"** 로 인쇄돼 있다(다른 셋은 L17·L51·L133). 본문은 L149.

## 8. 저자가 밝힌 한계 ★ (우리 관심 4번)

논문이 **자기 입으로** 적은 것 (§4 Conclusions):

1. **전자구조 정보가 없다** — *"they do not yet provide access to electronic structure information such as the electron density, which remains essential for understanding charge distribution, reactivity, and spectroscopic properties."*
   ⇒ **밴드갭·DOS·COHP·Bader·ELF 는 MLIP 으로 대체 불가.** 우리 전자구조 축이 DFT 를 못 버리는 이유의 외부 문장.
2. **기체상 전용 · 용매 없음** — *"UMA is trained exclusively on gas-phase data and does not currently incorporate solvation effects."* 용매가 형태 에너지론을 크게 바꾸므로 implicit/data-driven 용매 확장이 필요하다.
3. **기하최적화에 못 쓴다(현 시점)** — §1, refs 20,21 인용: *"the methodology is not yet stable enough for routine application to complex systems."* ⇒ 그래서 이 논문은 **DFT 최적화 기하 위 single-point** 로 한정했다.
4. **블랙박스 · 해석 불가** — *"general-purpose ML models such as UMA are trained as black boxes on vast data sets, and their performance is not easily interpretable. This abstraction risks concealing underlying failures if used uncritically."*
5. **near-degenerate 면책** — *"the instances where UMA fails to reproduce DFT rankings occur predominantly in near-degenerate energy regimes, where DFT itself cannot provide a uniquely reliable ranking."* 그리고 그 정도 차이는 *"could appear from any DFT methodology by changing basis sets or functionals within the same rung on Jacob's ladder."*

**저자가 밝히지 **않은** 한계** (내 판단, §10):
- **분포 밖 외삽(OOD)** 에 대한 언급이 **한 줄도 없다.** 이들 화학(bisphosphine TM 착물)은 OMol25 학습분포 **안쪽**이다(본문 §1 이 *"OMOL25 데이터셋이 대단히 많은 TM 착물을 포함한다"* 고 스스로 밝힌다). ⇒ **이 논문은 in-distribution 성능만 잰 것**이고, 그 사실을 결론에서 조건으로 달지 않았다. ⚠ **우리에게는 이게 가장 중요한 공백이다**(§12-②).
- **특정 화학계 경고 없음** — "Mn 이 fluxional 하다" 는 금속별 관찰뿐, "이 원소/결합류에서는 쓰지 마라" 식 경고는 없다.

## 9. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| **1** | 두 데이터셋 정의 도해. 위 = Data set 1 (Ni: rigid [L]NiCl₂ / flexible [L]Ni(CH₃CN)(Ar)⁺, 주황 물결 = 형태자유도). 아래 = Data set 2 (Ir 2배열 · Ru 4배열 · Mn 4배열 axial 표기, Ir/Ru/Mn 골격 구조식) | **표본크기 n 의 출처.** Ir=2 · Ru=4 · Mn=4 를 여기서 세어야 §6-(4) 의 "n=4 → ρ=1.0 만 통과" 논증이 성립한다. 캡션에 n 은 안 적혀 있다 |
| **2a,b** | Data set 1 ΔE_UMA vs ΔE_DFT 산점도. (a) rigid R²=0.96/RMSE=2.39, (b) flexible R²=0.68/RMSE=9.07. 축 kJ/mol | ⭐ **"집계지표는 랭킹을 못 본다"의 원본.** (b) 의 R²=0.68 은 좌하단 leverage 점 10여 개가 만든 값이고 중앙 뭉치엔 상관 정보가 없다(figure-read) — 우리 parity plot 을 쓸 때 같은 함정 |
| **3a,b** | 리간드 19종 per-ligand Spearman ρ 막대. 파랑=reliable, 회색=not, 빨간 파선 ρ=0.6. (a) rigid 84 %, (b) flexible 53 %, 음수 2건(L2·L12). 오른쪽 = L2·L4·L7·L8·L12 구조식 | ⭐⭐ **이 논문의 핵심 그림.** + **L25 가 0.6 위인데 회색** = 빨간 점선이 판정선이 아니라는 증거(p 필터). 우리가 "문턱선"을 그림에 그릴 때의 교훈 |
| **4** | Data set 2 전체 ΔE 산점도, R²=0.97/RMSE=4.92, 금속별 색(Ru 빨강·Mn 파랑·Ir 초록), 축 ±200 kJ/mol | **동적범위가 넓으면 R² 는 자동으로 올라간다**는 사례. 우리 cascade predictor R² 보고할 때 같은 비판을 미리 받아야 함 |
| **5** | Data set 2 per-ligand ρ 히트맵 (Mn·Ru 2열 × 리간드 행, 빨강→초록, 흰 셀=배열 부족). 오른쪽 = L17·L51(초록, 양쪽 성공) / L133·"149"(주황, Ru만 성공) | ⭐ **그림과 본문 수치가 겉보기 충돌** — 히트맵은 거의 다 초록인데 신뢰율은 44/61 %. 해소는 n=4 산술(§14-A). "히트맵이 초록이면 좋다"는 직관을 못 믿게 만드는 좋은 표본 |

**내가 실제로 이미지로 본 그림 (5장 = 전부)**: `Fig. 1`, `Fig. 2`, `Fig. 3`, `Fig. 4`, `Fig. 5`.
**안 본 그림**: 없음 (본문 그림이 5장뿐이고 SI 없음). `Fig. 5` 는 저해상 판독이 애매해 상단(L17 근방)을 **2배 확대해 재판독**했다 — §14-B.

## 10. Post-processing ★

우리 관례의 "post-processing"(NEB/Bader/COHP/DOS/ESW…)에 해당하는 것은 **하나도 없다.** 이 논문의 post-processing 은 **전부 통계**다.

| 무엇 | 도구 | 수치화·플롯·기록 방식 |
|---|---|---|
| 상대에너지 ΔE = E_i − E_ref | Python | 같은 리간드 안에서 기준구조 대비. **UMA·DFT 가 동일 기하** |
| **Pearson R²** | (명시 안 됐으나 numpy/scipy) | `Fig. 2`·`Fig. 4` 좌상단 주석 |
| **RMSE** (kJ/mol) | 동상 | 동상 |
| **Spearman ρ + p-value** | scipy 계열로 추정 (명시 없음) | `Fig. 3` 막대 / `Fig. 5` 히트맵 |
| 신뢰 판정 | ρ>0.6 AND p<0.05 AND n≥4 | 색으로만 기록 (수치표 없음) |
| 구조 생성 | **MACE**(입체이성질체 열거, ref 24) · **CREST/GFN2-xTB**(Data set 1) · **RDKit**(Data set 2) | — |
| 진동수 정리 | **PyQRC** | 허수진동수 제거 후 재최적화 |
| 추론 | **ASE** + UMA-s-1.1 | RTX 3050 노트북 |
| 공개 | **4TU.ResearchData** 10.4121/6b178daf-… | 데이터셋 + 리간드 목록 + 재현 코드 + readme |

- ❌ **없는 것**: NEB, Bader, COHP/ICOHP, DOS/PDOS, ELF, BVSE, grand-potential ESW, 탄성, 포논 분산, MD/MSD, 전하해석. (분자 normal-mode 해석은 있으나 **DFT 쪽 구조검증용**이지 UMA 평가 대상이 아니다 → `methods:` 태그에 `phonon` 을 넣지 않았다.)

## 11. 우리 계(황화물 SE / LPSCl)와의 겹침 — **결론: 화학적 겹침 없음** ★ (우리 관심 5번)

정직하게 적는다:

| 축 | 이 논문 | 우리 | 겹침? |
|---|---|---|---|
| 조성 | Ni·Ir·Ru·Mn 유기금속 착물 (bisphosphine, CO, CH₃CN, H⁻) | Li₆PS₅Cl / Li₅.₄PS₄.₄Cl₁.₆ / +B₂O₃ / LPSOCl | ❌ **없음** |
| Li | **원자 1개도 없다** | 주역 | ❌ |
| S | **없다** (P 는 있으나 포스핀 P(III), 우리는 PS₄³⁻ 의 P(V)) | 주역 | ❌ |
| Cl | **있다** — 단 [L]Ni**Cl₂** 의 **분자 말단 리간드 Cl** | 골격 음이온 자리의 **Cl⁻**, S/Cl 무질서 | ❌ 이름만 같음 |
| 주기계 / 격자 | ❌ 전부 기체상 분자 | ✅ 주기 결정 | ❌ |
| 이온전도·MD·확산 | ❌ 없음 | 핵심 | ❌ |
| 산화 안정성 / ESW | ❌ 없음 | 핵심 (축 ①–④) | ❌ |
| 기계적 물성 | ❌ 없음 | 핵심 | ❌ |
| 전자구조 | ❌ 없음 (오히려 "MLIP 은 못 한다"고 명시) | 핵심 | ❌ |

**겹치는 것은 딱 하나: 계산기(UMA-s-1.1)와 그 실패 양상.** 그 외에 **이 논문에서 우리 물성표로 옮길 숫자는 0 개**다. 억지로 연결하지 않는다.

## 12. ⭐⭐ 우리 시야 — 판정 (§7 "우리 DFT 대비" 확장)

### ① 이 벤치가 우리 사용법을 **보증하지 않는다** — 커버리지 표

| 우리가 UMA 로 하는 일 | 이 논문이 시험했나 |
|---|---|
| **Langevin NVT MD** (dt 2 fs, 200 ps, 600/800/1000 K) → D, Ea | ❌ MD 0 |
| **힘 정확도** | ❌ 힘 0 (single-point 에너지만) |
| **구조 이완 / cascade** (fmax 0.05) | ❌ 명시적으로 **회피** ("아직 안정적이지 않다") |
| **NEB 장벽** | ❌ 0 |
| **응력 / 탄성** | ❌ 0 |
| **주기계·격자** | ❌ 0 |
| **`omat` task** | ❌ 그들은 `omol` |
| 같은 조성 내 **배열(무질서) 상대에너지 랭킹** | ⭕ **이것만 시험했다** |

⇒ **이 논문에서 우리 MD/이완/장벽에 대한 면죄부를 받아올 수 없다.** 유일하게 이전 가능한 것은 마지막 줄, **"UMA 로 같은 조성의 여러 배열 순위를 매기는 작업"** 에 대한 경고다.

### ② ⚠⚠ **이 논문의 안심 문장이 우리 실패 2건을 설명하지 못한다** (가장 중요)

논문 결론: *"UMA 의 랭킹 실패는 압도적으로 near-degenerate 영역(ΔE < 2–5 kJ/mol = 21–52 meV)에서 일어난다."*

우리 실측 2건을 그 척도에 얹으면:

| 우리 사건 | 에너지 규모 | 이 논문 프레임에 들어가나 |
|---|---|---|
| **b2o3 O-자리**: DFT 가 UMA 선호를 **−6.63 eV** 로 뒤집음 (kb/methodology/b2o3_doping_chemistry.md) | **≈ 640 kJ/mol** = 그들 실패 임계의 **약 130–320배** | ❌ **전혀.** near-degenerate 이 아니라 **완전히 다른 답**이다 |
| **UMA Li₃N 결정론적 편향** (2026-06 사용금지 판정) | 계통 편향 (랜덤 순위잡음 아님) | ❌ **전혀** |

⇒ **판정**: 이 논문의 실패 모형은 **"통계적 순위잡음(in-distribution)"** 이고, 우리 실패 모형은 **"분포 밖 외삽에서의 계통 오답(OOD)"** 이다. **다른 병이다.**
- 그래서 이 논문을 *"UMA 는 near-degenerate 에서만 틀린다"* 는 방어논거로 우리 원고에 쓰면 **틀린 인용**이 된다.
- 반대로 **쓸 수 있는 방식**은 이것이다: *"in-distribution 조건(OMol25 안쪽 화학)에서조차 랭킹 신뢰율이 44–84 % 로 흔들린다. 하물며 분포 밖에서는 —"* 라는 **하한선 논거**.

### ③ ⭕ 우리 규율과 **정합**하는 것 (외부 지지)

1. **"평균이 좋아도 목표량은 틀린다"** — R² 0.96–0.97 / RMSE 2.4–4.9 kJ/mol 인데 랭킹은 44–84 %.
   → 우리 축 J-1 의 *"최악 힘 = 평균의 16배"*, J-4 의 *"평균 RMSE 가 낮아도 목표 물성이 틀릴 수 있다"* 와 **같은 얘기의 다른 화학계 표본**이다. **[Zhang npj]** 의 *"힘 0.16 eV/Å 인데 NEB 상대에너지 RRMSE 22.8 %"* 와 나란히 놓을 수 있다.
2. **"MLIP 은 전자구조를 못 준다"** — 저자가 명시. 우리가 밴드갭·VBM/CBM·ICOHP 를 **DFT fixed-occ nscf 로만** 내는 규율의 외부 문장.
3. **"블랙박스 실패 은폐 위험 → 도메인 검증 필수"** — 우리의 "문헌 수치는 소환값" · "방법 명시 없이 이식 금지" 규율과 같은 정신.
4. **입체이성질체·conformer 전수 열거 후 랭킹** — 우리 `enumerate → lowest-Ewald` / SQS 와 같은 구조의 문제. 그들 결론(*짧은 링커 = 좁은 형태공간 = 안전*)을 우리 말로 옮기면: **배열 사이 에너지 간격이 클수록 MLIP 랭킹이 안전하다.**

### ④ 🔎 우리가 당장 할 수 있는 값싼 점검 (이 논문에서 파생)

**우리 S/Cl 무질서 배열 랭킹에 같은 시험을 그대로 돌릴 수 있다.**
- 재료: modelc(Li₅.₄PS₄.₄Cl₁.₆)의 무질서 배열 앙상블 (이미 `tools/modelc_v3/disorder_ensemble_diffusion.py` 가 배열을 만든다).
- 방법: 같은 DFT 최적화 기하 위에서 **UMA(omat) single-point vs QE 총에너지** → **Spearman ρ + 배열 간 ΔE 분포**.
- 판정 기준을 이 논문에서 빌린다: **배열 간 ΔE 가 몇 meV 아래로 붙으면 UMA 랭킹을 믿지 않는다**.
- ⚠ 단, 문턱값 21–52 meV 는 **분자·구조당** 값이므로 그대로 쓰면 안 된다. 우리 52원자 셀의 **셀당 ΔE** 로 다시 재야 한다(§14-C).
- 비용: 새 DFT 없이 기존 배열 계산이 있으면 거의 0. **미착수.**

### ⑤ ⛔ 이 논문에서 **하면 안 되는 것**

- ❌ RMSE 2.39 kJ/mol(24.8 meV)를 우리 **13.5 meV/atom** 옆에 놓기 — **구조당 vs 원자당**이고, **omol vs omat**이고, **PBE0-D3/def2-SVP vs PBEsol/PBE** 다. 세 겹으로 다르다.
- ❌ "84 %" 를 우리 무질서 랭킹에 그대로 기대하기 — 화학·task·표본크기가 전부 다르다.
- ❌ "UMA 는 near-degenerate 에서만 틀린다"를 **일반 명제로** 인용 (§12-②).
- ❌ 44 %/61 % 를 84 %/53 % 와 **같은 척도로** 비교 (§6-(4), §14-A).

## 13. 우리 DFT/MLIP 기준 대비 (comp1 / modelc) → `../our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| MLIP 체크포인트 | **UMA-s-1.1** | **uma-s-1p1** | ⭕ **같은 세대** — 우리가 쓰는 것을 남이 감사한 첫 논문 |
| task | **omol** (OMol25, 분자) | **omat** (OMat24, 주기계) | ❌ **다른 head.** 오차 수치 이전 불가 |
| 참조 DFT | **PBE0-D3(BJ)/def2-SVP**, Gaussian16, 기체상 | **PBE**, QE, 주기계 | ❌ 범함수 계열이 다르다(hybrid vs GGA) |
| 무엇을 평가 | single-point ΔE 랭킹 | D·Ea(MD) · gap(nscf) · C_ij · onset | ❌ 축이 안 겹침 |
| 밴드갭 | **n/a** (MLIP 이 못 한다고 명시) | 2.066 / 2.099 / 1.9671 / 2.2309 eV | 비교 대상 없음 |
| Ea · D | **n/a** | 0.253/0.224 eV · 3.09/7.90×10⁻⁶ cm²/s | 비교 대상 없음 |
| ESW onset | **n/a** | 2.256 V (S²⁻-limited) | 비교 대상 없음 |
| 탄성 | **n/a** | E_VRH 22.06/27.66 GPa | 비교 대상 없음 |
| **가져올 것** | **"집계지표 우수 ↔ 랭킹 44–84 %" 라는 괴리 자체** | 축 J (MLIP 방법론) | ⭕ **유일한 이전 항목** |

> 🔗 UMA 모델 자체의 사양(아키텍처·task head·OMol25/OMat24 학습분포·공표 오차)은
> `papers/uma2026_family_of_universal_models_for_atoms.md` 에 있다. **이 digest 는 그 사양서의 외부 검증편**이다.

## 14. ⭐ 검산 기록 — 내가 실제로 확인한 것 / 어긋난 것

### A. **Data set 2 의 "신뢰율"이 실제로 무엇을 세는가** (그림 ↔ 본문 긴장 해소)

1. `Fig. 1` 에서 배열 수를 직접 셌다: **Ir 2 · Ru 4 · Mn 4.** (본문은 Ir=2 만 명시)
2. n=4 에서 Spearman 유의성을 직접 계산했다 (scipy `spearmanr`, 24개 순열 전수):
   - ρ=1.0 → t-근사 양측 p = **0.0000** (통과) / 정확 permutation 단측 **0.0417**, 양측 **0.083**
   - ρ=0.8 → p = **0.20** (탈락)
   - ρ=0.6 → p = **0.40** (탈락)
   ⇒ **n=4 에서 p<0.05 를 통과할 수 있는 ρ 는 1.0 뿐이다. 논문이 내건 ρ>0.6 문턱은 Data set 2 에서 작동하지 않는다.**
3. `Fig. 5` 히트맵의 셀 색을 **픽셀로 분류**해 열별 비율을 냈다 (채점대상 = 흰 셀 제외):

| 열 | ρ≈1.0 (진초록) | ρ≈0.8 (중초록) | ρ≤0.6 (노랑) | ρ≈0.2 (빨강) | 흰(제외) |
|---|---|---|---|---|---|
| **Mn** | **48.0 %** | 38.8 % | 7.9 % | 3.9 % | 13.5 % |
| **Ru** | **72.1 %** | 25.0 % | 1.6 % | — | 19.5 % |

   - **Mn: 픽셀 48.0 % vs 논문 44 %** — 잘 맞는다.
   - **Ru: 픽셀 72.1 % vs 논문 61 %** — **11 %p 어긋난다.** 원인 후보: (i) 배열 5개인 리간드가 섞여 있어 ρ=0.9/0.96 셀도 진초록으로 분류됨(그림에 0.96·0.89 주석이 실제로 있다), (ii) 행 높이가 균일하지 않음. ⇒ **이 픽셀 값은 논지의 방향을 확인하는 용도이지 정확한 재현이 아니다.**
   - **⇒ 판정**: "Ru 61 % / Mn 44 %" ≈ **"UMA 가 4개 배열 순위를 완벽히 맞춘 리간드의 비율"**. **Data set 1 의 84 %/53 %(n≈39–66, 실효문턱 ρ>0.6)와 같은 척도가 아니다.** 논문은 두 수를 *"A similar pattern"* 으로 병치한다 — 방어되지 않는다.

### B. `Fig. 5` 상단 재판독 (내 초판 판독을 스스로 뒤집음)

- 처음 저해상으로 볼 때 **L17 의 Ru 셀이 0.8** 로 보였다 → 본문의 *"L17 은 양쪽 금속 모두 ρ = 1.0"* 과 충돌하는 줄 알았다.
- 해당 영역을 **2배 확대해 재판독**하니 **최상단 행이 Mn=1 · Ru=1** 로 정확히 일치했다. 히트맵의 y축 눈금 라벨이 **한 행 걸러 하나씩만** 붙어 있어 행-라벨 대응이 헷갈렸던 것. **본문과 그림은 일치한다. 내 초판 판독이 틀렸다.**
- 교훈(우리 관례): 히트맵에서 라벨이 격행이면 확대 없이 행을 세지 말 것.

### C. 단위 검산

- 1 kJ/mol = 10.364 meV ⇒ 2 kJ/mol = **20.7 meV**, 5 kJ/mol = **51.8 meV**.
- RMSE 2.39 / 9.07 / 4.92 kJ/mol = **24.8 / 94.0 / 51.0 meV** — **구조당**.
- 착물 원자수 대략 50–120 ⇒ **원자당 0.2–1 meV/atom**. ⚠ 우리 13.5 meV/atom 과 **직접 비교 금지**.
- 비용 사고실험 재계산: 4 h × 32 core = 128 SBU × €0.01 = €1.28/착물 × 10,000 = **€12,800** ✅ 본문과 일치.
- 84 % = 16/19 ✅ · 53 % = 10/19 ✅ (`Fig. 3` 막대 색을 세어 확인).

### D. 텍스트 오식 2건

1. **"Dell X-ray photoelectron spectroscopy (XPS) 15 9520 laptop"** — 저널 약어 자동확장 오식. 이 논문에 XPS 측정은 없다.
2. `Fig. 5` 오른쪽 리간드 라벨 **"149"** (다른 셋은 L17·L51·L133) — L149 의 L 누락.

### E. 확인 못 한 것 (정직 목록)

- Spearman p 를 **어느 구현·단측/양측**으로 계산했는지 논문에 없다 → 나는 scipy 기본(t-근사)으로 추정했다. 4TU 공개 코드를 열면 확정 가능(미착수).
- OMol25 task 의 **전하·스핀 입력**을 어떻게 줬는지 없다. flexible 모델이 **양이온**이라 이 설정이 결과에 직접 영향을 준다.
- 착물별 정확한 원자수 미기재 → 원자당 환산은 내 추정(50–120).
- `Fig. 3` 막대 높이는 **눈대중 figure-read(±0.03)** 다. 픽셀 적합은 시도했으나 막대 색 마스크가 깔끔히 안 잡혀 포기했다.

## 15. 인용 가능 문장 (deck / 원고용)

- "A third-party audit of the same UMA-s-1.1 checkpoint reported excellent aggregate agreement with hybrid DFT (R² = 0.96–0.97, RMSE = 2.4–4.9 kJ/mol) while per-ligand rank correlations remained reliable for only 44–84 % of cases — aggregate error metrics do not certify that the ordering of nearly-degenerate configurations is preserved." (Kalikadien & Pidko, *J. Phys. Chem. A* **2026**, *130*, 1897)
- "Kalikadien and Pidko explicitly note that current MLIPs, including UMA, 'do not yet provide access to electronic structure information such as the electron density' — motivating our use of DFT, not MLIP, for all band-structure and bonding analyses."
- "Ranking failures were concentrated where DFT-level energy differences fall below ~2–5 kJ/mol (21–52 meV), a regime in which the authors argue DFT itself cannot supply a unique ordering." ⚠ **인용 시 반드시 "in-distribution, single-point, molecular" 조건을 함께 적을 것** (§12-②).
- (비용) "A representative transition-metal complex requires ≈ 4 h on 32 CPU cores for hybrid-DFT optimization plus frequency analysis; screening 10,000 such complexes costs on the order of €12,800, whereas UMA single-point evaluations run in seconds on a consumer laptop GPU."

## 16. 주의 / 한계 (비판) ★

**우리 관점의 비판 — 논문 방법이 약하거나 주장이 방법 의존인 지점.**

1. **⚠⚠ 두 데이터셋의 "신뢰율"이 같은 척도가 아니다** (§6-(4), §14-A). Data set 2 의 n=4 에서는 **ρ>0.6 문턱이 작동하지 않고 사실상 "완벽한 순위"만 통과**한다. 그런데 논문은 84/53 %(n≈39–66)와 61/44 %(n=4)를 *"A similar pattern"* 으로 나란히 놓는다. **가장 큰 방법론적 결함.**
2. **⚠ 핵심 안심 주장("실패는 ΔE < 2–5 kJ/mol 에만")의 근거가 일화 4건뿐이다.** Data set 1 flexible 에서 실패한 리간드는 **9개**인데 본문이 에너지 간격으로 설명한 건 **L2·L12 둘뿐**이다(L4·L5·L6·L27·L30·L32·L36 은 설명 없음). rigid 실패 3건(L6·L25·L27)은 **한 줄도 설명이 없다**. Data set 2 도 L133·L149 두 사례뿐. **"ρ vs 에너지 스프레드" 산점도 하나만 그렸으면 정량 주장이 됐을 텐데 그게 없다.** 현재 상태에선 **가설이지 결과가 아니다.**
3. **⚠ 초록·결론이 본문 결과보다 낙관적이다.** 초록·결론 모두 *"promise of MLIPs for both rigid, well-defined systems **and** highly flexible or fluxional catalysts"* 라고 쓴다. 그런데 본문 수치는 유연계 **53 %**, fluxional Mn **44 %** 다. 랭킹 신뢰율 44 % 를 "promise" 로 요약하는 건 과다주장이다.
4. **⚠ 집계지표를 자기가 비판해 놓고 자기도 "excellent agreement" 로 쓴다.** `Fig. 2`b(R²=0.68)의 상관은 좌하단 leverage 점 10여 개가 만든 것이고(figure-read), `Fig. 4`(R²=0.97)는 ±200 kJ/mol 동적범위 덕이다. 두 R² 모두 "모델이 좋다"의 증거로 쓰기 약하다.
5. **⚠ 분포 밖 외삽(OOD) 논의가 통째로 없다.** 이 화학은 OMol25 **학습분포 안쪽**이다(저자 스스로 §1 에서 OMol25 가 TM 착물을 대량 포함한다고 밝힌다). 즉 **이 논문은 in-distribution 상한을 잰 것**인데, 결론은 그 조건 없이 일반 명제처럼 읽힌다. **우리 b2o3(−6.63 eV)·Li₃N 사례가 정확히 그 공백에 있다** (§12-②).
6. **⚠ single-point 만 잰다.** 힘·이완·MD·장벽이 전부 없다. 그런데 초록/결론은 *"high-throughput screening and early stage catalyst design workflows"* 에 쓸 수 있다고 말한다 — 스크리닝에는 **기하최적화가 필수**인데 그 능력은 이 논문이 **의도적으로 시험하지 않았다.** 저자가 §1 에서 그 한계를 명시한 건 정직하지만, 결론이 그 조건을 다시 달지 않는다.
7. **⚠ 방법 세부 누락**: Spearman p 의 구현/단측여부, OMol25 의 전하·스핀 입력, 착물 원자수, UMA 추론 시간의 실측값. 특히 **전하·스핀은 flexible 모델이 양이온이라 결정적**이다.
8. **⚠ 참조 DFT 가 하나뿐이다.** PBE0-D3(BJ)/def2-SVP 단일 수준. 저자 스스로 *"similar differences in ranking could appear from any DFT methodology by changing basis sets or functionals"* 라고 쓰면서 **정작 def2-TZVP 재계산 같은 대조군을 두지 않았다.** ⇒ **"UMA 의 랭킹 오차가 DFT 자체의 랭킹 불확실성과 같은 크기"** 라는 핵심 면책이 **측정된 게 아니라 주장된 것**이다. 대조군 하나면 논문의 무게가 완전히 달라졌을 것이다.
9. **네이밍 충돌**: 구조생성 도구 **MACE**(ref 24, Pidko 그룹의 입체화학 열거기)는 **MACE MLIP 과 무관**하다. 우리 repo 에 MACE(MLIP) digest 가 이미 있으므로 인용 시 반드시 구분.
10. **범위**: 실험 0, 재료 0, 주기계 0. **우리 물성 축(A–I)에 넣을 것이 하나도 없다** — 축 **J(MLIP 방법론)** 전용.

## 17. 기법 용어 미니사전

| 용어 | 뜻 (이 논문 맥락) |
|---|---|
| **UMA** | Universal Model for Atoms. Meta FAIR 의 범용 MLIP 계열. 하나의 backbone 에 **task head 여러 개**(omat=재료 / omol=분자 / oc20=촉매표면 / odac=DAC / omc=분자결정). 같은 체크포인트라도 **task 를 바꾸면 다른 참조 DFT 를 흉내낸다** |
| **OMol25** | Open Molecules 2025. UMA 의 분자 task 학습 데이터셋. TM 착물을 대량 포함. **전하·스핀을 입력으로 받는다** |
| **conformer** | 결합을 끊지 않고 **회전만**으로 오가는 이성질체 (형태이성질체) |
| **configuration** (이 논문) | 착물에서 **어느 주개원자가 축(axial) 자리에 오는가** — 배위 배열. H–H / C–N / C–H / C–C axial 등 |
| **fluxional** | 분자 내 리간드가 실온에서 자리를 바꿔 다니는 성질. PES 가 얕고 국소최소가 촘촘 → 랭킹이 어려움. 이 논문에선 **Mn(I)** 이 대표 |
| **bisphosphine** | P 주개 2개가 탄소 링커로 이어진 이자리(bidentate) 리간드. dppm(1탄소)·dppe(2)·dppb(4) 등. 링커 길이 = 형태자유도 |
| **Spearman ρ** | 값이 아니라 **순위**의 단조 상관. 비모수. −1(완전 역순) … +1(완전 일치) |
| **p-value** (여기) | 그 ρ 가 우연으로 나올 확률. **표본 n 이 작으면 아무리 ρ 가 커도 p 가 안 내려간다** ⇒ §6-(4) |
| **R² (Pearson)** | 선형상관의 제곱. **동적범위가 넓으면 자동으로 커진다** |
| **RMSE** | 평균 편차. 여기선 **구조당 kJ/mol** (원자당 아님) |
| **CREST / GFN2-xTB** | 반경험적 tight-binding(xTB) 기반 conformer 전수탐색 도구 |
| **MACE (ref 24)** | ⚠ **MLIP 아님.** Pidko 그룹의 TM 착물 **입체화학 자동열거** Python 패키지 (JCTC 2024) |
| **PyQRC** | 허수진동수를 가진 구조를 정상모드 방향으로 밀어 국소최소로 재수렴시키는 도구 |
| **PBE0-D3(BJ)** | PBE0 = 25 % HF 교환 혼성 범함수. D3(BJ) = Grimme 분산보정(Becke–Johnson 감쇠) |
| **def2-SVP** | Ahlrichs split-valence + polarization **이중-ζ** 기저. 빠르지만 작은 기저 |
| **SBU** | Standard Billing Unit = CPU 코어 수 × 벽시계 시간. HPC 과금 단위 |

## 18. INDEX / comparison 에 넣을 항목 (⚠ **파일 충돌 회피 — 여기에만 적어 둔다**)

> 2026-08-25 현재 다른 논문 에이전트가 `INDEX.md` · `comparison_vs_ours.md` 를 동시에 만지고 있어
> **이 digest 는 그 두 파일을 건드리지 않았다.** 아래를 그대로 옮겨 붙이면 된다.

### 18.1 `INDEX.md` — "✅ Digest 완료" 표에 추가할 행

```
| `papers/kalikadien2026_uma_tm_catalyst_conformer_ranking.md` | **[외부·methods·UMA 감사]** Kalikadien & **Pidko** (TU Delft), "**Performance of Meta's Universal Model for Atoms across the Conformational and Configurational Space of Diverse Transition-Metal Catalysts**" (**J. Phys. Chem. A 2026, 130, 1897–1904**, DOI 10.1021/acs.jpca.5c07061; 본문 8 pp·Fig 5·SI 없음·CC-BY) — **우리와 같은 체크포인트 세대(UMA-s-1.1 = `uma-s-1p1`, 150 M param)를 남이 감사한 첫 논문.** ⚠ 단 **task 가 `omol`(OMol25)** 이고 우리는 `omat` · **single-point 에너지만**(힘·이완·MD·NEB 전부 없음, 저자가 *"기하최적화는 아직 안정적이지 않다"* 며 회피) · 참조 DFT **PBE0-D3(BJ)/def2-SVP, Gaussian16, 기체상**. 계: **[L]NiCl₂ / [L]Ni(CH₃CN)(Ar)⁺** conformer(746·1260) + **[L]IrH₃/RuH₂(CO)/MnH(CO)₂(CH₃CN)** 배열(909 geom, 88 chiral bisphosphine). ★ **집계지표 ↔ 랭킹 괴리**: R² **0.96/0.68/0.97** · RMSE **2.39/9.07/4.92 kJ/mol** 인데 per-ligand Spearman 신뢰율(ρ>0.6 **AND** p<0.05)은 **rigid 84 % → flexible 53 %**, **Ru 61 % → Mn 44 %**, **역순위(ρ<0) 2건(L2 −0.37·L12 −0.81, figure-read)**. 저자 면책 = *"실패는 ΔE < 2–5 kJ/mol(21–52 meV) near-degenerate 영역에만"*. 명시 한계 = **전자구조 접근 불가·기체상 전용(용매 없음)·블랙박스**. 🔑 **우리 검산 2건**: ① **Data set 2 는 배열이 리간드당 4개뿐**(`Fig. 1` 실측: Ir 2·Ru 4·Mn 4)이라 **n=4 에서 p<0.05 를 통과하는 ρ 는 1.0 뿐**(ρ=0.8 → p=0.20) ⇒ **"61 %/44 %" 는 사실상 "완벽 순위 비율"이고 84 %/53 %(n≈39–66)와 같은 척도가 아니다** — 논문의 *"A similar pattern"* 병치는 방어 안 됨(`Fig. 5` 픽셀 계수: Mn ρ=1.0 셀 48.0 % vs 논문 44 %, Ru 72.1 % vs 61 %) ② `Fig. 3`a 의 **L25 는 ρ≈0.64 로 빨간 0.6 점선 위인데 회색(not reliable)** = 판정선이 점선이 아니라 p 필터임을 그림이 자백. ⚠ **핵심 안심주장의 근거가 일화 4건**(실패 리간드 9+ 중 L2·L12·L133·L149 만 설명, "ρ vs 에너지간격" 그림 없음) · **초록/결론이 본문보다 낙관**(44 % 를 "promise" 로) · **참조 DFT 대조군 없음**(단일 PBE0/def2-SVP 라 "UMA 오차 ≈ DFT 자체 불확실성" 면책이 측정 아닌 주장) · **OOD 논의 0**(이 화학은 OMol25 분포 안쪽) · 오식 2건("Dell **X-ray photoelectron spectroscopy (XPS)** 15 9520 laptop" = 노트북 모델명 자동확장, XPS 측정 아님 / `Fig. 5` 라벨 "149"). ⛔ **우리 계와 화학적 겹침 0** (Li·S·주기계 전무, Cl 은 NiCl₂ 말단 리간드) — **물성값 이전 0** | **축 J(MLIP 방법론) 전용 — UMA in-distribution 랭킹 신뢰도의 외부 상한.** ⛔ 물성 A–I 축 해당 없음 |
```

### 18.2 `comparison_vs_ours.md` — 축 **J** 에 추가

**J-0 출처표에 한 줄 추가:**

```
| **[Kalikadien JPCA]** | `kalikadien2026_uma_tm_catalyst_conformer_ranking` |
```

**J-7 을 신설 (J-6 뒤, `---` 앞):**

```markdown
### J-7. ★★ [Kalikadien JPCA] — 우리와 **같은 체크포인트**를 남이 감사했다 (2026-08-25 추가)

> **우리 계와 화학적 겹침은 0 이다** (Li·S·주기계 전무, Cl 은 NiCl₂ 말단 리간드).
> 그런데도 이 축에 들어오는 이유는 단 하나 — **UMA-s-1.1 = 우리 `uma-s-1p1` 과 같은 세대**를
> 제3자가 정량 감사한 **첫 외부 논문**이기 때문이다. **물성값은 하나도 가져오지 않는다.**

| 항목 | [Kalikadien JPCA] | 우리 |
|---|---|---|
| 체크포인트 | **UMA-s-1.1** (150 M param) | **uma-s-1p1** — ⭕ 같은 세대 |
| **task** | **`omol`** (OMol25, 분자·전하/스핀 입력) | **`omat`** — ❌ **다른 head, 오차 이전 불가** |
| 평가 대상 | **single-point ΔE 랭킹만** | 이완(cascade)·**Langevin NVT MD**·탄성·NEB |
| 힘 / MD / 장벽 / 응력 | ❌ 전부 없음 (저자가 이완을 *"아직 안정적이지 않다"* 며 회피) | 전부 우리 핵심 |
| 참조 DFT | PBE0-D3(BJ)/def2-SVP, Gaussian16, 기체상 | PBE, QE, 주기계 |

**⇒ 커버리지 판정: 이 논문은 우리 MD·이완·장벽에 대한 면죄부를 주지 않는다.**
유일하게 이전 가능한 것은 **"같은 조성의 여러 배열 순위를 UMA 로 매기는 작업"** 에 대한 경고다.

**① 이전 가능한 것 — "집계지표 우수 ↔ 랭킹 실패"의 다른 화학계 표본**
- R² **0.96 / 0.68 / 0.97**, RMSE **2.39 / 9.07 / 4.92 kJ/mol** (= 24.8 / 94.0 / 51.0 meV, **구조당**)
  인데 per-ligand Spearman 신뢰율은 **rigid 84 % → flexible 53 %**, **Ru 61 % → Mn 44 %**,
  **역순위(ρ<0) 2건**.
- ⇒ **J-1 의 "최악 힘 = 평균의 16배"**, **J-4 의 "평균 RMSE 가 낮아도 목표 물성이 틀린다"**,
  **[Zhang npj] 의 "힘 0.16 eV/Å 인데 NEB RRMSE 22.8 %"** 와 **같은 얘기의 세 번째 표본**.
  이제 이 명제는 **분자(omol)·주기계(omat)·SE(MACE-MP-0)** 세 축에서 각각 근거가 있다.
- ⭕ **"MLIP 은 전자구조를 못 준다"** 를 저자가 명시 — 우리가 gap·VBM/CBM·ICOHP 를
  **DFT fixed-occ nscf 로만** 내는 규율의 외부 문장 (인용 가능).

**② ⚠⚠ 이 논문의 안심 문장을 우리 실패 2건에 쓰면 안 된다**
저자 결론은 *"UMA 랭킹 실패는 ΔE < 2–5 kJ/mol(**21–52 meV**) near-degenerate 영역에 몰린다"* 인데,

| 우리 사건 | 규모 | 이 프레임에 들어가나 |
|---|---|---|
| **b2o3 O-자리 DFT 역전 −6.63 eV** | **≈ 640 kJ/mol** = 그들 임계의 **130–320배** | ❌ 전혀 |
| **UMA Li₃N 결정론적 편향** (2026-06 사용금지) | 계통 편향 (순위잡음 아님) | ❌ 전혀 |

**다른 병이다.** 저쪽은 **in-distribution 순위잡음**, 우리 쪽은 **분포 밖 계통 오답(OOD)**.
이 논문에는 **OOD 논의가 한 줄도 없다** — 이 화학은 OMol25 학습분포 안쪽이다(저자 §1 자인).
⇒ 쓸 수 있는 인용은 **하한선 논거뿐**: *"in-distribution 에서조차 랭킹 신뢰율이 44–84 % 다."*

**③ ⭐ 우리가 그대로 복제할 수 있는 시험 (미착수, 새 DFT ≈ 0)**
우리 **S/Cl 무질서 배열 랭킹**에 같은 프로토콜을 돌린다:
같은 DFT 최적화 기하 위 **UMA(omat) single-point vs QE 총에너지 → Spearman ρ + ΔE 분포**.
(배열 생성은 `tools/modelc_v3/disorder_ensemble_diffusion.py` 에 이미 있다.)
판정 문장: **"배열 간 ΔE 가 X meV 아래로 붙으면 UMA 랭킹을 믿지 않는다."**
⚠ 문턱 21–52 meV 는 **분자·구조당** 값이라 그대로 못 쓴다 — **우리 52원자 셀당** 으로 재정의할 것.

**④ ⛔ 이 논문에서 인용하면 안 되는 것**
- ❌ RMSE 2.39 kJ/mol(24.8 meV)을 우리 **13.5 meV/atom** 옆에 놓기 —
  **구조당 vs 원자당 · omol vs omat · PBE0-D3/def2-SVP vs PBEsol/PBE**, 세 겹으로 다르다.
- ❌ **"61 %/44 %" 를 "84 %/53 %" 와 같은 척도로 비교** — Data set 2 는 리간드당 배열이 **4개뿐**이라
  **n=4 에서 p<0.05 를 통과하는 ρ 는 1.0 뿐**이다(ρ=0.8 → p=0.20; 내가 순열 전수로 확인).
  즉 **61 %/44 % = "완벽 순위 비율"**, 84 %/53 % = "대체로 맞는 비율". **논문 자신이 이 둘을 병치하는데 그게 오류다.**
- ❌ "UMA 는 near-degenerate 에서만 틀린다"를 **일반 명제로** 인용 (②).
- ❌ "84 %" 를 우리 무질서 랭킹의 기대치로 쓰기 — 화학·task·표본크기가 전부 다르다.
```
