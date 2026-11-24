<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-11-23 신규 (대피 세션 · git 미사용 — 커밋은 메인 세션).
     ① 리뷰다 — 자체 계산 0 · 자체 실험 0 → 이 digest 의 수치는 **전부 2 차 소환값**이다. 원 논문은 [ref 번호] 로 같이 적었다.
     ② 크롭 18장 (그림 15 + 표 3) 중 **그림 11장 실독** + 확대 재렌더 4곳 (Fig. 4d · 7b/7c · 9a,b · 9k,l — 스크래치에만, figures 폴더 안 건드림).
        안 본 그림: Fig. 2 · 5 · 13 · 14. 표 1–3 은 PDF 텍스트로 전사 (이미지로 안 봄).
     ③ 원 digest 가 litdb 에 있는 인용 12편과 리뷰 서술을 대조했다 (§9).
     ④ 우리 값은 our_dft_baseline.md · canonical_registry.json 에서만. 우리 수송값 (σ·D·Ea) 은 싣지 않는다 (계 간 순위 인용이 원장에서 막혀 있다).
        점착 W (W_ad) 는 우리 값도 문헌 값도 숫자로 싣지 않는다 (이번 세션 규칙 · 위치만). -->

# Integration of experimental insights and computational modeling for all-solid-state batteries — Kansara, Trivedi, Lee et al. (*J. Mater. Chem. A* **2026**, 14, 29613–29654)

> slug `kansara2026_experiment_computation_integration_assb_review` · DOI `10.1039/d6ta02406h` · type `review (자체 계산 0 · 자체 실험 0 — 수치 전부 2차 소환)` · PDF `litdb/inbox/204ad35b-2._Integration_of_experimental_insights_and_computational_modeling_for_all-solid-state_batteries.pdf` (본문 42 pp · 논문은 "SI available" 이라 적지만 **우리 inbox 에 SI 없음**) · digested `2026-11-23` · status ✅ · 태그 **[외부 · 리뷰]**

> elements: Li, P, S, Cl, Br, In, Y, O, La, Zr, Ta, Al, Nb, Ti, Co, Ni, Mn, Ge, Na, Se, F
> methods: DFT, AIMD, MD, MLIP, NEB, DOS, PDOS, elastic, ESW

> **저자**: **Shivam Kansara**†ᵃ · **Om Trivedi**†ᵇ · **Seungwon Lee**†ᵃ · Rutva Maheta ᵇ · Hyeona Park ᵃ · Shizhao Xiong ᶜ · Dominic Bresser ᵈᵉ · **Dan Zhou\***ᶠ · **Sanjeev K. Gupta\***ᵇ · **P. N. Gajjar\***ᵍ · **Jang-Yeon Hwang\***ᵃʰ († 공동 1저자)
> ᵃ 한양대 에너지공학과 · ᵇ St. Xavier's College (Ahmedabad) 물리·전자 · ᶜ Kunming Univ. of Sci. & Tech. · ᵈ HIU Ulm · ᵉ KIT · ᶠ USTB (北京) 재료유전체 · ᵍ Gujarat Univ. 물리 · ʰ 한양대 배터리공학과
> 접수 **2026-03-20** · 수락 **06-11** · 게재 **06-17** · 참고문헌 **199** (185 = 192 **중복**) · 그림 15 · 표 3 · 데이터 = "교신저자에게 요청" · 지원: NRF RS-2024-00408156 · NST GTL24011-000 · 국가슈퍼컴센터 KSC-2025-CRE-0230 · 인도 ANRF CRG/2022/007329 · CRG/2023/006920
> **자기 인용**: ref 155 (Jeong 2024 *Energy Storage Mater.* — Kansara · Lee · Hwang 공저) 를 §3.4 의 대표 '통합 사례' 로 쓴다 (`Fig. 11`) · ref 14 (Shaikh … Gupta · Gajjar 2024).
>
> 🎤 **관련 발표: 해당 없음** — `litdb/talks/*.md` 의 '논문 에이전트 인입 대기열' (현재 `lee2026_skku_mlip_materials_design.md` §99-10 하나) 에 이 논문 없음 (grep 실측 0건). 참고: 그 대기열 #4 가 이 리뷰의 ref 87 (GNoME, Merchant 2023) 이고 PDF 가 아직 inbox 에 없다 → 이 리뷰의 GNoME 수치는 대조 못 했다 (§10-B).
>
> **본 digest 에서 실제로 본 그림 (2026-11-23)**: `Fig. 1` `Fig. 3` `Fig. 4` (+4d 확대) `Fig. 6` `Fig. 7` (+7b·7c 확대) `Fig. 8` `Fig. 9` (+9a,b · 9k,l 확대) `Fig. 10` `Fig. 11` `Fig. 12` `Fig. 15` — **11장**.
> 안 본 것: `Fig. 2` (NCM811/LGPS 다중척도 개념도) · `Fig. 5` (NASICON 스크리닝 · BLIGE Na⁺ 분포) · `Fig. 13` (열변형 · 이방 굴곡도) · `Fig. 14` (재가압 EIS · NCM111 O 공공 · 단일입자 모델). `Table 1`–`Table 3` 은 PDF 텍스트로 전사.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 우리가 계산한 값은 **`우리 산수`** 로 표시했다.

---

## 0. 이 digest 를 읽는 법

이 편은 **물성 논문이 아니라 "계산을 실험에 어떻게 이어 붙이나" 의 지도**다. 저자들 스스로 *"기존 리뷰는 계산 기법을 목록으로 늘어놓는데, 우리는 계산 예측이 **어디서 왜 성공하고 실패하는지**, 불확실성이 척도를 건너며 어떻게 전파되는지를 본다"* (p. 29615) 고 차별점을 건다. 그래서 읽는 축은 셋이다:

1. **방법 지도로서** — DFT/AIMD → ML → 다중척도 (kMC · 위상장) → 연속체 (COMSOL · P2D) → 실험의 '닫힌 고리' (`Fig. 1` · `Fig. 3` · `Fig. 15`). 우리 방법 정본 (`kb/methodology/computational_methods_canonical.md`) 과 **15 축으로 맞대 본다** (§4c).
2. **우리 축에 걸리는 2차 수치** — 우리 계 (Li₆PS₅Cl) 가 이름으로 나오는 곳이 넷이다: ① `Fig. 4b,d` LPSCl grand-potential 창 (Wang 2025 재수록) · ② `Fig. 9g–l` Li|LPSCl(_Se/_F/_O) 계면 HAML (Lai 2025 재수록 — 우리 O 도핑 계와 가까운 이름) · ③ `Fig. 10` 중간층 × LPSC 반응 에너지 지도 · ④ `Fig. 11` NCM712|LPSCl|탄소|바인더 DFT 모형. 그 밖에 탄성 (`Table 3`, Deng 2016 인용) · ML 탄성 오차 (`Fig. 12e–h`) · MLIP 벤치마크 (본문만).
3. **인용 위생 감사** — 이 리뷰는 인용 번호 · 저자 이름 · 그림 짝이 여러 곳에서 어긋난다 (§10-B ⑤–⑧ · 30건 안팎 — 한 사건이 두 항목에 걸친 것이 있어 정확한 수는 세지 않았다). **리뷰에서 숫자를 가져올 때는 반드시 §9 대조표 · 원 논문으로 거슬러 간다.**

> ⛔ **이 digest 의 모든 수치는 2차 소환값이다.** 원 논문 digest 가 litdb 에 있으면 그쪽이 정본이고 (§9), 없으면 "원전 미확보" 로 적었다. 우리 db 값과 같은 표 · 같은 줄에 놓지 않았다 — §7 은 리뷰 값과 우리 값을 **줄을 갈라** 적는다.

---

## 1. 한 줄 요약

DFT·AIMD·ML·kMC·위상장·COMSOL/P2D 를 "**원자 서술자 → 유효 매개변수 → 셀 거동 → 실험 되먹임**" 의 닫힌 고리로 묶자는 서사 리뷰다. 다섯 물성 축 (열역학·전기화학 안정성 / 이온전도·결함 / 계면 반응·SCL / 기계 / 열화) 마다 '사례 연구' 를 2–6개씩 모으고 한계 (failure modes) 를 짚은 뒤, 0–2년 · 3–5년 · 5년 로드맵 (`Fig. 15`) 으로 끝낸다.
⚠ 그러나 '실제로 구현된 공동설계 파이프라인' 이라는 주장 (p. 29620) 의 근거는 **노드 하나씩만 덮는 서로 다른 계의 사례 4편**이고, '정량 열화 캐스케이드' (§3.5.2 · §3.6) 는 **다른 계의 숫자를 이어 붙인 서사**다. 'uncertainty' 를 26번 말하지만 리뷰가 보여 주는 오차막대는 재수록 캡션의 ±0.06 eV 하나다. 그리고 *"LPSCl 이 산화되면 Li₂S 와 LiₓP 가 생긴다"* 는 화학 오류가 세 번 나온다 (§10-A).

---

## 2. 메타 / 구조

| 절 | 쪽 | 내용 | 그림·표 |
|---|---|---|---|
| §1 서론 | 29613–15 | LIB 한계 → ASSB · SE 4계열 (고분자·산화물·황화물·할라이드) · 양극 4계열 · 음극 · "계산은 설명 동반자가 아니라 설계 도구" | `Fig. 1` |
| §2.1 ab initio | 29615–16 | NEB·AIMD·MLMD·kMC 의 한계 · 결함 형성에너지 · 응집에너지 식 · Gibbs · Nernst · 계면 코팅 · ESW 3법 (HOMO–LUMO / 화학량론 / 상안정) | — |
| §2.1.2 한계 | 29616 | DFT 값은 "고유 서술자 또는 상한" 으로 읽어라 | — |
| §2.2 다중척도 | 29616–18 | pymatgen hull · AIMD NVT · FEA · Hooke · cideMOD · Hwang NCM811/LGPS · MatterGen · 계층/동시 결합 | `Fig. 2` (미독) |
| §2.3 COMSOL | 29619–20 | 보존법칙 · 5단계 워크플로 · **best practice 5개** · §2.3.2 통합 논리 (사례 4편) | `Fig. 3` · `Table 1` |
| §3.1 안정성 | 29621–26 | 실험 진단법 · 사례 1–4 (LGPS/LIPON/LLZO 창 · **LIC/LPSC hull·ESW** · E_hull 스크리닝 · COMSOL Na⁺ 분포) · "어느 ESW 법도 보편적이지 않다" | `Fig. 4` · `Fig. 5` (미독) |
| §3.2 이온전도·결함 | 29626–31 | 사례 1–6 (Beutl 교차 실험 · LYC 적층결함 · Li₇TaO₆ · Li₂S ReaxFF · Na₃OBr DeePMD · LiPON NequIP · uMLIP 벤치마크 · 비정질 옥시할라이드 · CSE 플럭스) | `Fig. 6` · `Fig. 7` |
| §3.3 계면·SCL | 29631–37 | SCL 형성 · 코팅 · 사례 1–5 (ΔE_chem 식 · Haruyama LNO · Zhu16 · Sharafi · HAML · Nolan · Wang Li\|LPSC · reactive MLIP · COMSOL) · 운동학적 안정화 | `Fig. 8` · `Fig. 9` · `Fig. 10` · `Table 2` |
| §3.4 기계 | 29638–42 | K·G · 적층압 · 사례 1–5 (PVDF-CTFE 바인더 · LLZO 탄성 · Deng · Mücke · ML 포텐셜 · CGCNN · Abaqus · 열변형 · 굴곡도) | `Fig. 11` · `Fig. 12` · `Table 3` · `Fig. 13` (미독) |
| §3.5 열화 | 29642–48 | 사례 1–5 (재가압 · NMC532/LPSCl · in situ TEM · PBE0 EC · NCM111 불순물 · P2D/FE²/ROM · **'정량 캐스케이드'** · SPM · PINN) | `Fig. 14` (미독) |
| §3.6 통합 워크플로 | 29648 | ML 의 네 역할 · 캐스케이드 재서술 | — |
| §4 미래 방향 | 29648–50 | 시장 수치 · 상용화 장벽 · 제조성 반영 스크리닝 · 디지털 트윈 · 단계별 로드맵 | `Fig. 15` |

---

## 3. 핵심 수치 총정리 ★ (전부 2차 소환 · [ref] = 리뷰 참고문헌 번호)

> 표기: **본문** = 리뷰 본문에 숫자로 적힘 · **figure-read** = 그림에서 우리가 읽음 · **우리 산수** = 우리가 계산 · 원 digest 가 litdb 에 있으면 slug 를 단다.

### 3a. 이온전도 · 결함 (축 A)

| 물성 | 값 | 계 · 조건 | 출처 |
|---|---|---|---|
| σ (교차 실험 4기관) | **0.3–0.4 mS cm⁻¹** → 360 MPa 로 Al/C 전극을 누르면 **1.8 mS cm⁻¹** | LPSCl (Beutl 교차 실험, NMC90505 셀) | 본문 [43 Beutl 2024] — 원전 미확보 |
| 초기 용량 | **114–146 mA h g⁻¹** @ C/20 | 같은 4기관 셀 | 본문 [43] |
| σ_RT (적층결함) | **0.49** (볼밀) vs **0.067 mS cm⁻¹** (고상) | Li₃YCl₆ | 본문 · `Fig. 6b` figure-read ≈ 0.48 / 0.068 mS cm⁻¹ [94 Sebti] |
| 겉보기 Ea (EIS) | figure-read ≈ **0.41 eV** (볼밀 그대로) · ≈0.40 (333 K 처리) · ≈0.42 (353 K) · ≈0.43 (423 K) · ≈**0.47 eV** (고상) | Li₃YCl₆ | `Fig. 6b` [94] |
| NEB 장벽 (meV, ±60) | 벌크 M1–M2 면내 **358** / 면외 **117** · 벌크 M1–M3 **255** / **294** · 적층결함 **132** / **121** · 비화학량론 적층결함 **549** / **62** | Li₃YCl₆ | `Fig. 6d` figure-read (막대 위 숫자 인쇄) [94] |
| Ea · σ_RT | **0.29 eV** · **5.7×10⁻⁴ S cm⁻¹** ("예측보다 약간 낮다") | Li₇TaO₆ (계산+실험) | 본문 [31] |
| σ_max (25 °C) | **6.61×10⁻⁴ S cm⁻¹** | Li₆.₈₋ᵧGe₀.₀₅La₃Zr₂₋ᵧTaᵧO₁₂ | 본문 [32] |
| σ (900 °C) | **0.047 S cm⁻¹** @ Gd₂O₃ 10–12 mol% | ZrO₂–Gd₂O₃ | 본문 [93] |
| σ · 창 | **1.35 mS cm⁻¹** ("ultrahigh temperatures" — 온도 미기재) · **4.95 V** | SiO₂ 나노구 / PVDF-HFP CSE | 본문 [92] |
| σ_RT | **10⁻³ S cm⁻¹ 급** | NASICON | 본문 [95] |
| σ(700 K) (장 구동 ReaxFF MD) | 공공 0.3 % **5.614×10⁻⁸** · 2 % **3.008×10⁻⁶** · 3 % **2.814×10⁻⁴** · 격자간 1 % / Frenkel 2 % **2.651×10⁻⁹ S cm⁻¹** | Li₂S (Li 음극 코팅) · 인가장 0.03 / 0.01 / 0.0005 / 0.01 V Å⁻¹ | 본문 [97 D'Amore 2023] · ⚠ `Fig. 7b`·`7c` 는 패널이 뒤바뀌어 붙었다 (§5.6) |
| Ea · σ_RT (외삽) | **0.42–0.43 eV** · **1–2×10⁻⁴ mS cm⁻¹** (= 1–2×10⁻⁷ S cm⁻¹) | Na₃OBr (DeePMD) | 본문 [41] |
| MLIP 정확도 | 학습 **13,454** DFT 구조 · 에너지 MAE **5.5 meV/atom** · 힘 MAE **13.6 meV Å⁻¹** | 비정질 LiPON (NequIP) · Li\|LiPON 계면 ns MD | 본문 [99] |
| MLIP 비용 | DFT 대비 **10³–10⁴ 배** 저렴 · 미세조정 **~500–2000** 구조 | 일반 | 본문 [101] |
| 무질서 효과 | S/Cl 음이온 무질서 **40–50 %** 에서 Li⁺ 이동 연결성 ↑ (MatterSim) | Li₆PS₅Cl | 본문 [100] — ⚠ 저자명 오기 (§10-B) · 원전 미확보 |
| 격자상수 | 중성자 회절 대비 **2 % 이내** · Br 치환 σ 경향 재현 | Li₃YCl₆₋ₓBrₓ (미세조정 CHGNet) | 본문 [101] |
| CSE 플럭스 | 세라믹 ≈ 3,200 / 3,050 / 2,750 · 고분자 ≈ 280 / 800 / 1,250 · 평균 ≈ 1,330 / 1,800 / 1,930 mmol m⁻² s⁻¹ (LLZTO 섬유 10 µm / 1 µm / 100 nm) | LLZTO/PVDF-HFP COMSOL | `Fig. 12a–c` figure-read [106] — ⚠ 단위 그대로면 전류밀도 ≈ 12–31 A cm⁻² 상당 (§10-C) |

**홉 수 검산** (규율 `D-2026-09-27-barrier-hop-count` · Γ = ν₀·exp(−Ea/kT) · **ν₀ 10¹³ s⁻¹ 가정**):
- Li₇TaO₆ 0.29 eV · 300 K → Γ ≈ 1.3×10⁸ s⁻¹ · 평균 대기 ≈ 7 ns (리뷰의 '빠르다' 와 차수 모순 없음)
- Na₃OBr 0.42–0.43 eV · 300 K → Γ ≈ 0.6–0.9×10⁶ s⁻¹ · 대기 ≈ 1.1–1.7 µs (σ_RT ~10⁻⁷ S cm⁻¹ 과 같은 방향)
- LYC 겉보기 Ea ≈ 0.41 / 0.47 eV (figure-read · 298 K) → Γ ≈ 1.2×10⁶ / 1.1×10⁵ s⁻¹ · 대기 ≈ 0.9 / 9 µs — ⚠ EIS 거시 Ea 라 단일 홉이 아니다 (차수 검산만)
- LYC NEB 62 → 549 meV · 300 K → 대기 ≈ 1 ps → 0.17 ms (**8 자릿수**) · 117/121/132 meV ≈ 9–17 ps · 358 meV ≈ 0.1 µs

### 3b. 안정성 · ESW · 계면 반응 (축 B)

| 물성 | 값 | 계 · 조건 | 출처 |
|---|---|---|---|
| E_hull (hull 아래) | **−28 meV/atom** (Li₃InCl₆ → InCl₃ + 3 LiCl 대비 안정) | Li₃InCl₆ (LIC) | 본문 [81 C.-M. Wang 2025 *J. Power Sources* 640, 236719] — litdb 미보유 |
| **E_hull** | **+19 meV/atom** (vs Li₃PS₄ + Li₂S + LiCl) — "준안정" | **Li₆PS₅Cl** (LPSC) | 본문 [81] · `Fig. 4b` (LPSC 점이 Li₃PS₄–Li₂S–LiCl 단체 안에 있다) |
| ab initio ESW | LIC **2.5–4.3 V** · LPSC **1.8–2.0 V** | grand-potential (MP 자료) | 본문 [81] · `Fig. 4c,d` |
| ┗ LPSC 경계 (figure-read) | 환원 **≈1.79 V** · 산화 **≈1.99 V** · 2단 **≈2.38 V** · 3단 **≈3.26 → 3.35 V** · 환원 2단 ≈1.28 / 1.18 V → ≈0.95 / 0.88 V | 확대 렌더 (≈230 px/V · 판독 ±0.02 V) | `Fig. 4d` |
| ┗ LPSC 평형 상 (figure-read) | 2.0–2.38 V: **LiCl + LiS₄ + Li₃PS₄** · 2.38–≈3.3 V: LiCl + LiS₄ + P₂S₇ · ≈3.3 V↑: SCl + S + P₂S₇ / 1.79 V↓: LiCl + Li₂S + P → LiP₇ · Li₃P₇ · LiP · Li₃P | **LiS₄ 포함 상 집합** | `Fig. 4d` 오른쪽 칸 |
| LIC 경계 (figure-read) | 환원 ≈2.45 · 산화 ≈4.33 V | | `Fig. 4c` |
| ESW (DFT) | Na₃PS₄ **1.55–2.25 V** · Na₃PSe₄ **1.80–2.15 V** ("실험과 일치") | vs Na | 본문 [45 Tian 2017] |
| ESW (DFT, 대상 불명확) | 환원 **1.5–1.7 V** 까지 · 산화 **4.5–5.3 V** 까지 | 문장 주어가 "LGPS, LIPON, LLZO, LLTO … the material" — 어느 물질인지 불명 | 본문 [79 Benabed 2021 *Front. Energy Res.* 9, 682008] — 원전 미확보 |
| 분해 온도 (DFT) | **1819 K** | Ta-LLZO (Li₆.₆La₃Zr₁.₆Ta₀.₄O₁₂) | 본문 [80] vs 실험 1000 °C / 1250 °C 분해 (La₂O₃ + La₂Zr₂O₇) [33] |
| 산화 개시 (실험, 출처 번호 없음) | "**2.5–3.0 V vs Li/Li⁺ 위에서 산화**" + "절연성 Li₂S 와 P 함유 부산물" | LPSCl | 본문 p. 29621 — ⚠ 겉보기 개시 · Li₂S 는 산화 산물이 아니다 (§10-A) |
| E_hull 스크리닝 문턱 | **≤ 0.050 eV/atom** (입방 LLZO 가 MP 에서 정방정보다 높아서) · **> 0.040 eV/atom 제외** + 띠틈 **< 1 eV 제외** | 6,744 이중도핑 조성 · 4,348 CDHE 가넷 | 본문 [85 Jeong 2024] · [86 J.-H. Kim 2025] |
| M3GNet 구조 수 시험 | 25 vs 100 구조 최저에너지 MAE **0.00339 eV/atom** | NASICON 양극 3,126 → 50 후보 | 본문 · `Fig. 5a,b` (미독) [85] |
| 상호 반응 에너지 (전위 아래 · mutual) | **[−737, −594] meV/atom** (리뷰 표기) | Li₃PS₄ (LPS) \| LiCoO₂ · 2–5 V | 본문 [15 Zhu 2016] — ⚠ 원 digest 단위는 **meV per non-Li atom** · 리뷰는 '(Fig. 9a)' 라 적지만 실제는 `Fig. 9b` |
| 총 분해 에너지 (total) | **−1.27 eV/atom @ 5 V** | LGPS · Li₃PS₄ \| LCO | 본문 [15] · `Fig. 9b` 점선 figure-read ≈ −1270 |
| 화학 반응 에너지 ΔE_chem | LPSC\|Al₂O₃ figure-read **≈ −19 ~ −21 meV/atom** (x = 0 에서도 ≈ −19) · LIC\|Al₂O₃ ≈ 0 · Li\|Al₂O₃ 최소 figure-read **≈ −230 meV/atom** (x ≈ 0.33) | 닫힌계 pseudo-binary | `Fig. 9a` [81] (캡션: LIC·LPSC 쪽 "0 또는 거의 0") |
| 중간층 지도 (figure-read, 색) | LPSC 기준 **진한 빨강 (< −100 meV/atom)**: Co₃O₄ · ZnO · Ga₂O₃ · In₂O₃ · SnO₂ · **La₂O₃** · PbO · Li₅AlO₄ · **LiNbO₃** · Li₃N · SbCl₃ · 거의 모든 Li 합금 / **흰색 (≈0)**: SiO₂ · LiAl₅O₈ · BN · Si₃N₄ · Li₂S · MoS₂ · LiF · LiCl · LiBr · **LiI** · C · **Li₃PO₄** · Li₂PNO₂ · Ag · Au · Cu · Hg / 옅은 색: Al₂O₃ · LiAlO₂ · SnS₂ · LiH₂PO₄ · BiBr₃ (중간) · Ge · Sn · Bi · CuSn | 닫힌계 ΔE_chem (MP) | `Fig. 10` [81] |
| HAML 유사도 (280 ps 구조 기준, figure-read) | before relax / 0 ps: Li\|LPSC **0.933 / 0.967** · _Se 0.845 / 0.920 · _F 0.861 / 0.912 · _O **0.887 / 0.936** | SOAP 코사인 · 300 K (원 digest) | `Fig. 9k` [124 Lai 2025] — 원 digest 값과 일치 |
| HAML 결합 수 (0 ps → 280 ps, figure-read ±3) | Li\|LPSC: P–S 8 → **0** · Li–P 8 → 33 · Li–S 58 → **58** · Li–Cl 11 → 21 / _Se: P–S 10 → 0 · Li–P 0 → 37 · Li–S 45 → 141 · Li–Cl 0 → 28 · Li–Se 6 → 6 / _F: P–S 10 → 0 · Li–P → 34 · Li–S 50 → 143 · Li–Cl → 13 · Li–F → 5 / _O: P–S 10 → 0 · Li–P → 34 · Li–S 45 → 129 · Li–Cl → 19 · Li–O 5 → 5 | | `Fig. 9l` [124] — ⚠ 무도핑 280 ps Li–S 막대 의심 (원 digest · §10-D) |
| 코팅 후보 (HT 열역학) | **Li₂ZrO₃ · Li₃TaO₄ · LiAlO₂** | NCM \| LLZO 계면 | 본문 [128 Nolan 2021] — 원 digest 와 일치 |
| SCL 두께 | "**수 µm 까지**" | 일반 | 본문 [57] — ⚠ ref 57 = de Klerk 2018 (β-Li₃PS₄ MD 확산 논문 · SCL 내용 0) (§10-D) |

**관측창** (규율 `D-2026-10-05-md-observation-window` · 개정 1) — Lai 2025 의 *"무도핑 LPSC 는 280 ps 뒤에도 대체로 온전"* 에 붙인다:
관측창 (300 K · 280 ps · n = 1 · ν₀ 10¹³ s⁻¹ 가정 · 정상성 가정): **기대 사건 1 ≈ 0.21 eV (검출 63 %) · 95 % 검출 ≈ 0.18 eV**. (반응 기회 n = 10 / 100 이면 Ea₁ ≈ 0.27 / 0.32 eV.)

### 3c. 기계 (축 C)

| 물성 | 값 | 계 · 방법 | 출처 |
|---|---|---|---|
| E_VRH / G_VRH | **154.5 / 61.4 GPa** (Al-LLZO) · **147.2 / 59.4 GPa** (Ta-LLZO) | DFT | 본문 [157 Yu 2016] |
| K / G / E / ν | **95 / 57.6 / 143.7 GPa / 0.25** | "NASICON LiTi₂(PO₄)₃ (LATP)" — ⚠ 조성은 LTP | 본문 [159 Deng 2016] — 원 digest: **PBEsol** 값 · 일치 |
| K / G / E / ν | **23.3 / 11.4 / 29.5 GPa / 0.29** | β-Li₃PS₄ | 본문 [159] — 원 digest 와 일치 (PBEsol) |
| E_VRH / ν / K_VRH | Li₀.₅NCM271 **221 / 0.26 / 155** · Li₀.₅NCM361 **221 / 0.26 / 155** (⚠ 두 행 동일) · Li₀.₅NCM955 **195 / 0.29 / 153** · Li₀.₁NCM955 **188 / 0.29 / 145** · Li₀.₅CoO₂ **212 / 0.25 / 141 GPa** | DFT (충방전 중 이방 강성) | 본문 [160 Mücke 2023] |
| 비교 | PEO **0.1 GPa / 0.4 / 0.167 GPa** · LLZO **146 GPa / 0.26 / 101 GPa** | | 본문 [160] |
| `Table 3` 입방 LLZO | ML 포텐셜 vs DFT: C₁₁ 200.3 / 188.7 · C₁₂ 84.6 / 77.7 · "C₁₄" 70.4 / 72.7 (⚠ 입방정이라 **C₄₄** 여야 함) · B 123.1 / 114.7 · G 65.0 / 65.2 · E 165.9 / 164.5 GPa · 오차 6.1 / 8.9 / 3.2 / 7.3 / 0.3 / 0.9 % | ML 포텐셜 (SLAD · NN) | `Table 3` [170, 171] — 우리 산수: B = (C₁₁+2C₁₂)/3 = 114.7 ✓ · G_VRH(C₄₄=72.7) = 65.2 ✓ |
| `Table 3` "수치 모델링" 행 | Al-LLZO **E 8.83** · NMC622 **E 7.21** ("units: GPa") | Abaqus 모형 입력 | `Table 3` [174 Adjah 2024] — ⚠ DFT E 의 1/18 · 설명 없음 (§10-C) |
| 경험 포텐셜 오차 | DFT 대비 탄성상수 **18–60 %** 어긋남 (Morse/Buckingham + Coulomb) | LLZO | 본문 [168–170] |
| 비정질 LLZO ML | 격자상수 · 부피탄성률 오차 **< 2 %** | | 본문 [172, 173] |
| CGCNN 탄성 예측 | G_VRH R² **0.822** · MAE **9.7 GPa** (일반 층화) / K_VRH (> 450 GPa 층) R² **0.892** · MAE **14.0 GPa** · 최적 모형: G R² **0.852** · MAE **9.3** / K R² **0.906** · MAE **13.6 GPa** | Materials Project 탄성 자료 | 본문 · `Fig. 12e–h` figure-read (막대 숫자 인쇄) [130 Choi 2021] |
| 바인더 결합에너지 | BR **0.249 eV** vs PVdF-CTFE **9.016 eV** ("36 배" — 우리 산수 36.2) | NCM712 \| LPSCl \| Super C \| 바인더 적층 DFT | `Fig. 11c` [155 Jeong 2024 · 자기 인용] — ⚠ 흡착 ≳ 2 eV 규율 (§10-F) |
| '복합양극' 모듈러스 | BR: E **21.75** · K figure-read ≈ 11.2 · G ≈ 7.9 GPa / PVdF-CTFE: E **25.09** · K ≈ 14.9 · G ≈ 8.5 GPa | 같은 적층 모형 · VRH | `Fig. 11d` [155] — ⛔ 우리 E_VRH 옆에 놓지 않는다 (§7d) |
| SAICAS 박리 하중 | figure-read 평균 BR ≈ 0.35 / 0.68 / 0.78 N vs PVdF-CTFE ≈ 0.75 / 1.2 / 1.35 N (깊이 25 / 50 / 75 %) → 비 ≈ 2.1 / 1.8 / 1.7 | 실험 | `Fig. 11g` · 본문 "**1.8 배**" [155] |
| 미세균열 개시 | 전류밀도 **> 0.8 mA cm⁻²** (응력집중 + Li 침투) | Abaqus 비결합 열–전기–기계 | 본문 [174] |
| 열변형 | 부피 열팽창률 최대 **0.0327 %** (탭–본체 접합부) · 본체 중심 **0.0198 %** · 탭 **0.0047 %** @ 1C | 셀 | 본문 · `Fig. 13a` (미독) [107] |
| 굴곡도 | 이방 굴곡도 흑연 음극이 0 V 도달까지 **364 vs 306 s** (4C · 3 mA h cm⁻² · HOLE) | | 본문 · `Fig. 13b` (미독) [173] |
| '캐스케이드' 숫자 | 분해에너지 **≈ −0.5 eV/atom** (LGPS · 양극 계면) → 인장응력 **> 1–2 GPa** → 파괴 '인성' **20–30 J m⁻²** (단위는 파괴에너지) → 접촉면적 **최대 −40 %** → 출력밀도 **−11 %** · 용량 **−15–20 %** | 서로 다른 계를 이은 서사 | 본문 §3.5.2 · §3.6 [15] + [166 Taghikhani 2025] (§10-E) |

### 3d. 전자구조 (축 D)

| 물성 | 값 | 비고 | 출처 |
|---|---|---|---|
| 띠틈 (DFT+U) | **3.82 eV**, "직접 띠틈" — 실험 **2.68–4 eV** 와 "일치" | LiFePO₄ | 본문 [31] — ⚠ [31] 은 Li₇TaO₆ 논문 (오귀속 · §10-B) · 실험 범위 폭 1.3 eV 를 '일치' 판정에 썼다 |
| 띠 가장자리 (figure-read) | Li₃SbS₄ CBM ≈ 3.3 eV · **Li₃PS₄ CBM ≈ 3.95 eV** · Li₄SnS₄ ≈ 3.5 eV (VBM = 0) · E_f,eq ≈ 2.1 / 1.83 / 1.4 eV | 범함수 리뷰에 미기재 | `Fig. 6g–i` [35 Helm 2024] |
| 스크리닝 문턱 | 띠틈 **< 1 eV** → 전자전도체로 제외 | ML 대리모형 | 본문 [86] |
| HOMO–LUMO 창 | "ESW 의 상한" · 고분자 전해질 산화 안정성 스크리닝에 여전히 유용 | | 본문 [23 · 66] |

### 3e. ML · 스크리닝 · 생성

| 항목 | 값 | 출처 |
|---|---|---|
| 고분자 전해질 용매 HT | **~10,000** 후보 · HOMO/LUMO 로 ESW > 4 V 문턱 → 최상위: σ **5.5×10⁻⁴ S cm⁻¹ @ 30 °C** · ESW **4.5 V** · **500 사이클 86.7 %** · EIS 를 학습셋으로 되먹임 (XGBoost · SISSO · CGCNN) | 본문 [74 Shen 2025] |
| 할라이드 다목표 | CatBoost · LightGBM · NN 으로 σ · K_VRH · G_VRH · ESW 동시 예측 → **Rb₂LiBiCl₆ · Rb₂LiAlF₆** 가 다섯 문턱 동시 통과 · AIMD MSD 로 확인 | 본문 [75 Choong 2026] (p. 29620 에선 "Ha et al." — 오기) |
| GNoME | "**3,200만** 후보 → **381,000** 신규 안정 → **736** 독립 합성" | 본문 [87] — ⚠ 원전 미확보 · 대조 못 함 |
| GNN 발견 | "**18** 신규 SE 조성 전부 합성·특성화" | 본문 [88] (본문 "Zheng et al." ↔ 목록 1저자 C. Chen) |
| 표면 보호층 HT | MP **15,000** 후보 → Li₉S₃N · LiAlB₂O₅ · LiYO₂ · LiSbF₄ · Sr₄Li(BN₂)₃ | 본문 [98 Honrao 2021] |
| 경로 ML | K₀.₉₇Fe₀.₉₇Ti₀.₀₃O₂ **128** 경로 · 특성 20개의 비동치 집합 **89** · **~70 %** 구별 가능 · `Fig. 6f` R² 0.783 (ridge, MAE 0.028) / 0.899 (RF, 0.019) / **0.935** (GB, MAE 0.012 · RMSE 0.020 eV/ion) | 본문 · `Fig. 6e,f` figure-read [36 Eremin 2019] |
| uMLIP 벤치마크 | "**12** 종" (이름은 7개: GRACE · MACE · MatterSim · DPA · SevenNet · CHGNet · M3GNet) × 에너지 · 힘 · 포논 · ESW · 탄성 · Li⁺ 확산 · Li₃YCl₆ · Li₆PS₅Cl | 본문 [100] — **UMA 언급 0** |
| 베이즈 하이브리드 PINN | FEM 대비 **47×** 빠름 · SOH 정확도 **≥ 60.61 %** 향상 | 본문 [193] |
| reactive MLIP | **ns · ~10⁵ 원자** · 자기제한 SEI 성장 | 본문 [102 Ding 2025] |
| MLIP 규모 (§3.6) | **ns–µs · 10⁴–10⁶ 원자** | 본문 |

### 3f. 연속체 · 소자 · 시장

| 항목 | 값 | 출처 |
|---|---|---|
| 재가압 | 50 사이클 뒤 **300 MPa** 재가압 → 방전용량 **80 mA h g⁻¹** 까지 회복 · EIS 1/20/50/51 사이클 | 본문 · `Fig. 14a–d` 캡션 (미독) [52 Shi 2020] (본문은 "Shi et al.53") |
| 단일입자 모델 | 입자 반경 10 µm (추출 텍스트 'mm') · SE σ 1 mS cm⁻¹ · 0.2C (34 mA g⁻¹) / 1C (170) / 5C (850) · 피복률 10–30 % 에서 ≥ 1C 기울기 | `Fig. 14g–j` 캡션 (미독) [182 Lee 2024] |
| Li–CO₂ 셀 | DFT + AIMD + MD + FEA 로 1 mA cm⁻² 전압–용량을 **경험적 맞춤 없이** 재현 · 전류밀도에 지수적으로 용량 감소 (기공 막힘) | 본문 [77 Lemaalem 2025] |
| 시장 | 2018 **~330 GWh** → 2030 **~2.6 TWh** (CAGR ~26 %) · 2021 **~400 GWh** · Fraunhofer ISI 연 30–40 % · ASSB 2035 **5–120 GWh** · BNEF 미·유럽만 **> 300 GWh** | 본문 [196–198] |

---

## 4. DFT/계산 방법 ★

### 4a. 자체 계산

**없다.** code · functional · pseudo · k점 · ecut · supercell · DFT+U · AIMD 조건 · MLIP · 무질서 처리 — 리뷰 자신의 값은 전부 **n/a**. `Table 1` 이 도구 23종 (VASP 1996 · QE 2001 · ABINIT · WIEN2K · CP2K · LAMMPS · GROMACS · DeePMD-kit · n2p2 · MLIP/MTP · QUIP/GAP · SchNetPack/TorchMD/PiNN · ASE · pymatgen · Matminer · AiiDA · PyBaMM · COMSOL · Abaqus/ANSYS · FEniCS · 위상장 · kMC · VESTA/OVITO · MP/OQMD/AFLOW · Git/Zenodo) 을 척도·용도·라이선스·연도로 나열할 뿐이다.
- `Table 1` 에 **없는** 우리 도구: LOBSTER (COHP) · Bader · phonopy · fairchem (UMA) · MACE (본문엔 있음).
- ⚠ `Table 1` 은 VESTA 를 "open source" 로 분류한다 — VESTA 는 무료 배포 (freeware) 이지 소스 공개가 아니다 (사소).

### 4b. 리뷰가 적은 방법 서술 — 전부

| 방법 | 리뷰 문장 (요지) | 쪽 |
|---|---|---|
| NEB | 확산 경로·장벽을 효율적으로 비교하지만 **정적 격자 · 단일 기전** 가정 → 온도·격자 동역학·결함 상호작용·운반자 농도 효과를 못 본다 | 29615 |
| AIMD | 열활성 이온 운동·동적 무질서를 직접 · 그러나 **짧은 시간·작은 계** → 실험 시간척도 외삽 불확실 · NVT · **Nosé–Hoover** · VASP/QE · **300–1000 K** 평형 뒤 **"수십 ps"** 궤적 → D → **Nernst–Einstein** 으로 σ | 29615–17 |
| MLMD | 큰 계·긴 시간 · 신뢰도는 학습 자료의 질·전이성에 달림 | 29615 |
| kMC | 시간척도 다리 · **미리 정한 홉 망**에 의존 → 새 경로를 놓칠 수 있다 | 29615 |
| 결함 형성에너지 | 인쇄식 *E_form = (E_layer − Σ Nᵢμᵢ) / Σ Nᵢ* — ⚠ 이건 층 (layer) 의 원자당 형성에너지 꼴이지 결함 형성에너지 식이 아니다 · **화학퍼텐셜 가정에 민감 · 결함–결함 상호작용·뭉침·비평형 무시** | 29615 |
| 전자구조 | 띠 구조·DOS 는 **범함수 선택에 민감** · 국소 상태·폴라론 놓침 | 29615 |
| 응집에너지 | *E_CO = [m E(A) + n E(B) − E(AₘBₙ)] / (m + n)* — 계면 안정성 판단에 널리 쓰임 | 29615 |
| Gibbs · Nernst | G = H − TS · 인쇄식 "**H = P + EV**" (⚠ E + PV 의 오식) · ΔᵣG = −nFE | 29616 |
| ESW 3법 | ① **HOMO–LUMO** (ΔE_HL 은 ESW 의 상한 · 전자 이동만 보고 화학반응 무시) ② **화학량론 안정법** (원자 하나씩 넣고 빼기 · ①과 ③의 다리) ③ **상안정법** (grand-canonical 상도 · 임계 화학퍼텐셜) | 29616 |
| DFT 한계 (§2.1.2) | 범함수 · 초셀 크기 · **기준 상태**에 민감 · σ · 계면 안정성 · ESW 를 **"자주 과대평가"** → "고유 서술자 또는 상한" 으로 읽어라 | 29616 |
| hull | pymatgen hull 은 평형 한정 · DFT 형성에너지 정확도에 의존 → hull 위 물질도 실작동에선 분해 가능 | 29616 |
| 탄성 | 작은 변형 εⱼ → 응력 σᵢ = Σⱼ Cᵢⱼ εⱼ (Hooke) · VRH 평균 | 29617 · 29639 |
| 계면 반응 | **ΔE_chem = E{c_eq[(1 − x)c_A + x c_B]} − (1 − x)E(c_A) − xE(c_B)** (식 1 · Richards/Ceder) · 최소값을 계면 화학 반응 에너지로 | 29632 |
| 구속 | K_crit = 섭동 반응을 열역학적으로 불리하게 만드는 데 필요한 유효 강성 K_eff | 29622 |
| 연속체 best practice | ① 척도를 건널 때 **단위·열역학 기준 상태** 일관 ② **메시·시간 간격 수렴** 시험 ③ 실험 제약 없는 **과매개변수화** 경계 ④ 계면·미세구조 **불균질** 포함 ⑤ 결합 강도에 맞는 **풀이기 결합** (약하면 분리, 강하면 완전 결합) | 29619–20 |
| ESW 해석 계층 (§3.1 끝) | 산화물 = 상안정법이 장기 열화와 상관 · **황화물 = 예측 불안정 vs 실작동 괴리 큼 (준안정·이온전도성 계면상) → 화학량론 안정 + 반응경로가 HOMO–LUMO 보다 현실적** · 할라이드 = 띠 가장자리로 환원 내성 + 상안정으로 음이온 교환 · 고분자 = HOMO–LUMO 산화 스크리닝 유효 · **"서술자가 다르면 ESW 는 서로 바꿔 쓸 수 없다 — 비교용 지표로"** | 29625–26 |
| MLIP 워크플로 | 범용 MLIP (MP 수백만 구조 사전학습) → **~500–2000** 계 특화 DFT 구조로 미세조정 → operando 회절·NMR 로 검증 → 대규모 예측 · 결함 뭉침·입계·비평형에서 발산 → **능동학습** 필수 | 29629 |

### 4c. ★ 리뷰의 'best practice' ↔ 우리 방법 정본 (`kb/methodology/computational_methods_canonical.md`)

> 값이 아니라 **방법** 대조다 (숫자는 프로토콜 매개변수만). 전문 검색 실측: 리뷰 본문에 **k점 · 컷오프 · 의사퍼텐셜/PAW · vdW/D3 · PBEsol · SQS · 시드 · Haven · MSD 적합 창 · vc-relax/고정셀 · relaxed/clamped-ion · BVSE · Bader/COHP/ELF = 0 회**, "uncertainty" = **26 회**.

| # | 축 | 리뷰 | 우리 정본 | 판정 |
|---|---|---|---|---|
| 1 | 셀 이완 | 언급 없음 ("초셀 크기에 민감" 만) | argyrodite 는 **고정셀 + 등방 E(V) BM3 → V₀ 에서 이온만 relax** · vc-relax 안 씀 (정적 스냅숏 셀은 cubic 이 아니라 뒤틀림은 배치 인공물 · Pulay) · 잔류 편차응력 별도 보고 · 예외는 사용자 허락 | 리뷰에 없는 축 — **우리가 더 엄격** |
| 2 | 탄성 | 작은 변형 + Hooke + VRH · relaxed/clamped 구분 **0 회** · Deng 값 인용 때 범함수 미기재 | **relaxed-ion** stress–strain (12 SCF) 만 인용 — clamped 는 argyrodite 에서 **~2.3× 과대** · 조성 간 비교는 셀·k·ecut 통일 (`HZ-elastic-cross-composition`) | 리뷰 처방만 따르면 clamped 를 받아들일 수 있다 |
| 3 | MD 수송 | NVT Nosé–Hoover · 300–1000 K · "수십 ps" · MSD → D → Nernst–Einstein | UMA-s-1p1 (omat) · Langevin NVT · dt 2 fs · friction 0.02 · 5 + 200 ps · **MSD 창 2–50 ps 고정** · 600/800/1000 K · **멀티시드** · Haven = 1 · 절대 σ 비인용 · **상자 크기 축** (같은 계에서 D 1.65×) · **골격 MSD 게이트** | 리뷰는 창 · 시드 · Haven · 상자 · 골격 점검 **0 회** |
| 4 | MLIP | 범용 → 500–2000 구조 미세조정 → 검증 → 배포 · 능동학습 | UMA **미세조정 없이** · 외부 앵커 (Li₃PS₄ 힘 MAE 30.0 meV/Å) · **Li₃N 에는 UMA 금지** · MLIP 장벽 절대값 금지 | 방향은 겹침 · 리뷰는 UMA 를 모른다 (언급 0) |
| 5 | NEB | 정적 격자 · 단일 기전 한계 | **셀 수직폭** (1 → 2×2×2 에서 장벽 1.3–3.3배 ↓) · **전하 규약** · no-CI 먼저 → CI · 끝점 심화 이완 · elementary 여부 · 장벽 인용 땐 **홉 수 검산** | 리뷰는 셀 크기 · 전하 · CI 순서 0 회 |
| 6 | ESW | 3법 · "서로 바꿔 쓸 수 없다 · 비교 지표로" | grand-potential **층① (분해 개시)** · 상 집합 명시 (LiS₄ · SCl₃ · Li₅PS₄Cl₂ 제외 = GG set) · 구속 축 B② 따로 · HOMO–LUMO 안 씀 · **띠틈 ≠ ESW** · 축 이름 없이 'Cl-rich 산화 안정' 금지 | **방향 일치** — 그러나 리뷰 자신이 LPSC 창을 상 집합 · hull 규약 없이 '1.8–2.0 V' 로 인용 (§7a) |
| 7 | E_hull 스크리닝 | 40 · 50 meV/atom 문턱 · 판본 언급 없음 | 우리 도구도 `e_above_hull` 을 정렬 키로 쓴 이력 (CLAUDE.md '조용히 틀린 경로') | **같은 LPSCl 이 19 vs 83 meV/atom** (§7b) — 문턱 판정이 DB 판본에 묶인다 |
| 8 | 띠틈 | "범함수 민감 · 폴라론 놓침" · LFP 3.82 eV ↔ 실험 2.68–4 eV '일치' | **fixed-occupation nscf 고유값만** (DOS 문턱 판독 ~0.3 eV 과소 금지) · PBE 과소 · 무질서 민감 → **'넓은 띠틈' 수준으로만 비교** | 리뷰의 '일치' 기준 (1.3 eV 폭) 은 우리 기준으로 판정이 아니다 |
| 9 | 계면 반응 에너지 | 닫힌계 ΔE_chem (`Fig. 9a`·`Fig. 10`) 와 Li 열린계 mutual/total (`Fig. 9b`) 을 같은 '반응 에너지' 로 나란히 · 정규화 미기재 | `interface_reactivity` (pymatgen `InterfacialReactivity` · use_hull_energy · 닫힌계 · per atom) · **열린/닫힌 · per atom / per non-Li atom 구분** · 양극 쪽은 **작동창 2.5–4.25 V** 에서 판단 | 리뷰는 정규화 · 계 개방 여부를 안 적는다 |
| 10 | 짧은 MD '무반응' | "280 ps 동안 무도핑 LPSC 대체로 온전" | **관측창 한 줄 필수** | 300 K · 280 ps · n = 1 → Ea₁ ≈ 0.21 eV (63 %) · Ea₉₅ ≈ 0.18 eV (§3b) |
| 11 | 흡착·결합 ≳ 2 eV | 바인더 9.016 vs 0.249 eV "36 배" | **결합 자리 배위수부터** · 구조 없으면 '배위 미확인' · 정규화 | 배위 미확인 · 비정규화 총에너지 · 두 모형의 접촉 기하 다름 (§10-F) |
| 12 | SCL | "수 µm 까지" (ref 57) | SCL 두께 · 전위 · Debye 길이 **원전에도 0** (Haruyama 2014 · Chen 2024 전문 실독) · **"SCL 을 계산했다" 금지** | 리뷰 문장은 근거 없음 (§10-D) |
| 13 | 기계 설계 · 파괴 | 고탄성률 → 덴드라이트 저항 (Monroe–Newman 류) · "파괴인성 20–30 J m⁻²" · DFT 가 파괴 저항을 정량 | **Monroe–Newman 을 무기 SE 설계원칙으로 안 씀** ([Famprikis19]) · **K_IC 는 원자 스케일 산출물 아님** (DEM/CZM 매개변수) · J m⁻² 는 파괴에너지 G_c | 우리 경계가 더 엄격 |
| 14 | 무질서 | "무질서 초셀의 대규모 MLIP-MD" 언급만 · SQS 0 | DFT 는 단일 배열 (띠틈 ±0.2–0.3 eV 흔들림 명시) · MLIP-MD 는 멀티시드 · comp2 디스오더 앙상블 | 리뷰에 처방 없음 |
| 15 | UQ · 재현 | 'uncertainty' 26 회 · 실제 오차막대 0 · 로드맵 0–2년 = "기준 불확실성 경계 · 일관 상태의 기준 워크플로 · 표준 보고" | 보고량 카드 (결과 전 게이트) · 멀티시드/IQR · `canonical_registry` + `citation_hazards` · 재개 규칙 · 마감 파일 | 리뷰 로드맵의 1단계 항목이 우리 원장 규율과 겹친다 (§11-③) |
| (참고) | BVSE | 0 회 | b = 0.37 Brown 형식 BV 합 · **softBV 아님** | 해당 없음 — 이 리뷰를 BVSE 근거로 쓰지 않는다 |

---

## 5. 절별 상세 (그림 실독 포함)

### 5.1 §1 서론 + `Fig. 1`
LIB 의 안전·에너지밀도 한계 → ASSB. SE 계열 장단점: 고분자 (유연·가공 쉬움 / 저 σ_RT · 좁은 창 · 열안정 한계) · 황화물 (σ · 계면 젖음 우수) · 산화물 (열·전기화학 견고 / 취성·가공 어려움) · 할라이드 (고전압 양극 양립) · 복합 (장점 결합 시도, 상충 미해소). 양극: 고-Ni 층상 · Li-rich Mn (> 300 mA h g⁻¹ · > 4.5 V · 전압 감쇠) · 고전압 스피넬 (4.7 V · 140 mA h g⁻¹ · Mn 용출) · 폴리음이온. Li 금속 3860 mA h g⁻¹ · −3.04 V vs SHE.
핵심 문장: *"중심 과제는 더 이상 계산 도구의 가용성이 아니라 원자 예측을 소자 수준 결과로 옮기지 못하는 것"* — 리뷰의 존재 이유.
`Fig. 1` 실독: 원형 도식. 네 사분면 (Atomic Level Modeling · Data-Driven Approach · High-Throughput Screening · Multiphysics Simulation), 고리 문자열 AIMD · NEB · DFT · ESW · ML · Aflow · MP · Workflow DFT · FEA · **D2D** · Phase Field · PyBaMM · COMSOL, 가운데 "Experimental Validation" 셀 그림. 정량 내용 없음. ⚠ "D2D" 는 본문 어디에도 정의가 없다.

### 5.2 §2.1 ab initio · §2.1.2 한계
- NEB → AIMD → MLMD → kMC 를 각자의 한계가 다음 방법을 부르는 사슬로 소개한다 (정적 격자 → 짧은 시간 → 학습 자료 → 홉 망).
- 결함 형성에너지는 운반자 농도와 지배 운반자를 정하는 데 쓰이지만 **"낮은 형성에너지만으로 높은 σ 가 보장되지 않는다 — 농도와 이동도의 결합"**. 맞는 말이고 우리 결함 축에도 그대로 적용된다.
- 계면: 높은 계면저항 = 접촉 불량 · 계면 화학반응 · 기계 불일치. 대책 = 코팅 · 완충층 · 표면 개질. LGPS + Li → Li₂S · Li₃P · Li–Ge 합금 → Li₃PO₄ · Li₂CO₃ · Li₄Ti₅O₁₂ 코팅으로 회피. "LGPS 나 Li₆PS₅X (본문 오식 'Li₆S₅') 완충층이 원치 않는 반응을 줄인다" [20]. LLZO 도핑 → 전자전도도 ↓ · 화학 안정성 ↑ [21]. 계면 전자 상태가 Li⁺ 장벽이 될 수 있다 [22].
- ESW 3법 (§4b). 
- **§2.1.2 의 결론 문장**: DFT 는 이상화·준평형 · σ · 계면 안정성 · ESW 를 "자주 과대평가" → **"고유 서술자 또는 상한"**. 그리고 E_ads · Ea · ESW · σ · K · G 가 `Fig. 3` 의 '재료 서술자' 로 흘러간다고 정의한다.
  ⚠ 이 문장은 §3.3 의 *"static DFT calculations tend to **overestimate interfacial reactivity**"* (p. 29634 · 29636) 와 **정면으로 반대**다 (§10-E).

### 5.3 §2.2 다중척도 · §2.2.1 한계 (`Fig. 2` 미독)
- "다중척도는 방법의 합이 아니라 단일 척도 예측 한계를 넘는 전략" · 원자 계산은 수송을 과대평가 · 메조/연속체는 측정 어려운 입력에 의존.
- AIMD/LAMMPS NVT Nosé–Hoover · VASP/QE · 300–1000 K · 수십 ps → D → Nernst–Einstein [26, 67].
- FEA: 입력 (탄성 · 계면 강도 · 확산 유도 변형) 에 매우 민감. FEniCS 기반 cideMOD (리튬화 팽창을 부피 변형 원천으로) [27].
- Hwang (T. Hwang · K. Cho) 의 NCM811/LGPS 전기–화학–기계 다중척도 [68] (`Fig. 2`): 제일원리로 E_eq · 구조 · 영률 · 파괴에너지 G_c → Butler–Volmer · Nernst–Planck · Fick + 확산 유도 응력 · 균열 진전 결합 모형 → FEM 으로 접촉 손실 기전. 응집대 모형 (CZM) 으로 활물질–SE 박리 [69]. (교신저자 J.-Y. Hwang 과 다른 사람이다.)
- ML 증강 DFT (KRR · GPR · GNN 으로 에너지·힘·안정성 회귀) · **MatterGen** [71]: 원자종 · 좌표 · 격자 결합 확산 → 조성 · 대칭 · 자성 · 띠틈 · 부피탄성률 조건부 생성 · 위상장으로 다중척도 · 합성 1건 검증.
- §2.2.1: 원자 오차가 메조·연속체에서 증폭 · 이상 구조·평형 가정 → "결정론적 예측 도구가 아니라 반복·검증 틀".

### 5.4 §2.3 COMSOL 연속체 · §2.3.2 통합 논리 · `Fig. 3` · `Table 1`
- 보존법칙 (질량 · 전하 · 에너지): Nernst–Planck · Poisson · Ohm · Fick · Butler–Volmer/Marcus · 열 방정식. 워크플로 5단계: 기하 → 영역·유효물성 → 경계조건 (전류/전위 · 열 · 적층압/접촉) → 계면·경계층 메시 세분 → 풀이기 (강결합 = 완전 결합 · 강성 높으면 분리/반복). 산출: 과전위·전류밀도 지도 · 농도 구배 · 덴드라이트 취약 영역 · 줄열 열점 · 응력·변형장 (박리·균열 핵생성) · 사용자 정의 반응항으로 SEI 성장·용량 감퇴.
- **"연속체는 완전 예측형 디지털 트윈이 아니라 일관성 점검·시나리오 탐색 도구"** · 검증은 대개 **단일 작동조건 곡선 맞춤** · 원자 → 소자 오차 전파는 "거의 미탐색". 검증 수단: EIS · GITT · operando 열/응력 · X선 단층촬영 · FIB-SEM. best practice 5개는 §4b.
- **§2.3.2 '통합 논리'**: DFT 만으로는 집단 수송·미세구조 진화·장기 열화를 못 본다 → 사례 4편을 노드마다 하나씩 든다:
  ① DFT/AIMD 노드 — Shen [74]: 용매 ~10,000 HOMO/LUMO → ESW > 4 V → 최상위 σ 5.5×10⁻⁴ S cm⁻¹ @ 30 °C · 500 사이클 86.7 % ("DFT 서술자의 예측 가치 확인").
  ② ML 노드 — "Ha et al." [75 = Choong 2026]: 할라이드 σ · K · G · ESW 동시 예측 → Rb₂LiBiCl₆.
  ③ 다중척도 노드 — "Dong et al." [76 = Y.-C. Yang 2025 arXiv]: Na 양극 MLIP 로 온도별 D · 계면에너지 · 자유에너지 지형 → 의사 2D 위상장.
  ④ 연속체 노드 — Ngo [77 = Lemaalem 2025]: Li–CO₂ 셀 1 mA cm⁻² 전압–용량을 맞춤 없이 재현.
  결론 문장: *"`Fig. 3` 은 개념적 위계가 아니라 **실제로 구현된 공동설계 파이프라인**"*. ⚠ 넷은 **서로 다른 계** (고분자 용매 · 할라이드 SE · Na 양극 · Li–CO₂) 이고 **어느 하나도 고리를 끝까지 돌지 않는다** (§10-E).
- `Fig. 3` 실독: 다섯 상자 → 화살표 → 아래 되먹임. **DFT/AIMD** (ESW limits · Diffusion barriers · Reaction energies · Interfacial stability) → "Materials descriptors" → **Machine Learning** (HT screening · Property prediction · Uncertainty-aware models · Generative design) → "Effective parameters" → **Multiscale** (Phase-field microstructure · Defect–transport coupling · Interfacial evolution · Stress accumulation) → "Cell-scale behavior" → **Continuum** (FEM/COMSOL · Electro-chemo-mechanical coupling · Contact loss · Performance degradation) → **Integration** 상자. 아래 "Experimental validation & feedback" (EIS/Operando XRD · Stack & pouch cells · Pressure-dependent tests · Failure-mode identification · 양극복합체/SE/Li 음극 셀 그림) 에서 "Parameter feedback" (→ DFT) · "Model validation & refinement" (→ 통합) 두 화살표.
  ⚠ **그림 ↔ 본문 불일치**: 본문 (§2.1.2 · p. 29621) 은 DFT 노드가 **E_ads 와 탄성상수 (→ K, G)** 를 공급한다고 하는데, 그림의 DFT/AIMD 상자에는 **둘 다 없다**.

### 5.5 §3.1 열역학·전기화학 안정성 — `Fig. 4` (`Fig. 5` 미독)
- 실험 진단: LSV · CV (산화·환원 분해 전위) · 사이클 후 XPS · ToF-SIMS · in situ XRD.
- **문제의 문장** (p. 29621, 출처 번호 없음): *"Li₆PS₅Cl 은 2.5–3.0 V vs Li/Li⁺ 위에서 산화되어 **절연성 Li₂S** 와 P 함유 부산물을 만든다"* — ⚠ §10-A.
- 산화물 양극 × 황화물 SE 의 화학 비양립 → 저항성 계면상 → LiNbO₃ · Al₂O₃ 코팅.
- **3.1.1**: NMC811 위 얇은 TiO₂ 코팅 [69] · TPP 완충층 (가넷) [78].
- **3.1.2 사례 1**: "그 물질은 환원 1.5–1.7 V 까지 · 산화 4.5–5.3 V 까지 안정" [79] — 문장 주어가 LGPS · LIPON · LLZO · LLTO 를 나열한 뒤 "the material" 이라 **어느 물질의 창인지 알 수 없다**. Ta-LLZO DFT 분해온도 1819 K [80] vs 실험 LLZO 1000 / 1250 °C 분해 (La₂O₃ + La₂Zr₂O₇) [33] — 저자들은 "계산이 영향 인자를 단순화" + "계산 쪽은 Ta 도핑" 두 가지로 설명. LLTO 는 혼합 이온–전자 전도상 때문에 DFT 창과 다르게 거동 [80].
- **3.1.3 사례 2 (우리 계)** — `Fig. 4` 실독:
  - `Fig. 4a`: Li–In–Cl 삼각도. Li₃InCl₆ 은 InCl₃–LiCl 선 위 · 탈리튬 (빨강) 은 Cl–InCl₃ 쪽 좁은 영역 · 리튬화 (파랑) 는 넓다 · Li₃InCl₆–Li '의사 이성분' 선.
  - `Fig. 4b`: Li–P–S–Cl 사면체. 표시된 상: SCl₄ · PCl₅ · PCl₃ · SCl · LiCl · Li · Li₂S · Li₃P · LiP · Li₃P₇ · LiP₇ · P · P₄S₃ · P₄S₇ · P₄S₉ · P₂S₅ · P₂S₇ · **LiS₄** · Li₃PS₄ · S · Cl. **Li₆PS₅Cl 회색 점이 Li₃PS₄–Li₂S–LiCl 보라 단체 안**에 있다 = 본문 E_hull +19 meV/atom. (우리 GG set 이 빼는 LiS₄ 가 들어 있고 SCl₃ · Li₅PS₄Cl₂ 는 보이지 않는다.)
  - `Fig. 4c`: LIC 전압 프로파일 — 산화 ≈4.33 V (Cl₂ + InCl₃) · 회색 안정 띠 ≈2.45–4.33 V · 환원 계단 → 0.1 V (In · Li–In 합금 계열).
  - **`Fig. 4d` (확대 렌더 · ≈230 px/V)**: y 0–4 V vs Li/Li⁺, x = LPSC 당 리튬화 −6 → 8. 회색 띠 **≈1.82–2.0 V** 에 "Li₆PS₅Cl". 산화 (빨강): x 0 → −1.8 에서 **≈1.99 V** · −1.8 → −5 에서 **≈2.38 V** · −5 → −5.4 에서 ≈3.26 V · −5.4 → −6 에서 ≈3.35 V. 환원 (파랑): x 0 → ≈5 에서 **≈1.79 V** · 이어서 ≈1.28 · ≈1.18 · ≈0.95 · ≈0.88 V. 평형 상 칸은 §3b 표.
  - 본문: "LIC 2.5–4.3 V · LPSC 1.8–2.0 V · 둘 다 환원 전위 ≈2 V 라 Li 음극에 열역학적으로 불안정" [81].
  - `Fig. 4e–g` (Fitzhugh 2021 [82] 재수록): (e) 유사상 (pseudo-phase) hull — 노란 별 = 계면상 조성·에너지 · 초록 = 반응상 · 진파랑 = hull 을 이루는 안정상 · 지렛대 규칙 D₁, D₂, d₁, d₂ · G_hull = 분해에너지. (f) **K_crit > K_eff (약한 구속)**: 분해상 에너지가 Gᵢ → Gᵢ + p(D)Vᵢ 로 조금 올라가도 순서 불변. (g) **K_crit < K_eff (강한 구속)**: 계면상이 분해 산물보다 안정해진다. 그림 속 라벨 (K_crit > K_eff / K_crit < K_eff) 과 캡션 (K_eff < K_crit / K_eff > K_crit) 은 같은 말 — 일치.
  - Benabed [83]: 도핑 LLZO 문헌 창 모음 — DFT · CSE · CV 외 전기화학법이 더 낮은 산화 전위를 준다. Na₃PS₄ 1.55–2.25 V · Na₃PSe₄ 1.80–2.15 V 가 실험과 일치 [45] ("DFT ESW 신뢰성").
  - 메조: Liu [84] 전기–열 모형 — 전류 수축·불균일 이온 흐름 → 국소 열점 · PLL 복합·상용 SE 셀 최고온도는 열폭주 문턱 아래 ("부반응을 빼면").
- **3.1.4 사례 3**: E_hull 로 이중도핑 6,744 조성 걸러냄 · 입방 LLZO 가 MP 에서 정방정보다 높아 **≤ 0.050 eV/atom** 문턱 [85] · Kim/Sun [86] CDHE 가넷 4,348 → ML 대리모형으로 띠틈 < 1 eV · E_hull > 0.040 eV/atom 제외 → CHGNet 로 최안정 배열 → DFT 이완 → CHGNet 미세조정. `Fig. 5a,b` (미독): NASICON 양극 3,126 → 50 · M3GNet 무작위 치환 25 vs 100 구조 MAE 0.00339 eV/atom. (⚠ 문단이 가넷 [86] 설명 도중 NASICON [85] 그림으로 넘어가 읽기 어렵다.) "ML 은 DFT 자료·평형 가정을 물려받는다 → 운동학적으로 안정화된 준안정 계면상을 놓칠 수 있다 · 불확실성 인식 예측 + operando 검증 필요". Choong [75]: Rb₂LiBiCl₆ · Rb₂LiAlF₆ 다섯 문턱 동시. GNoME [87] · [88] (§3e).
- **3.1.5 사례 4**: COMSOL 3D 전기–온도 결합 (온도 변화 · 덴드라이트) [89] · Li [90] BLIGE · PTEN · PHEN · 역 BLIGE 의 Na⁺ 과도 농도 (`Fig. 5c` 미독) — 낮은 σ 나 낮은 운반률이 분극을 키워 국소 고갈/축적 → 국소 전위 이동 → 불안정. 열폭주 ODE [91]. *"ESW 는 원자·데이터 모형에서 받아야 한다 — 형성에너지·띠 위치는 COMSOL 능력 밖"*.
- 종합 문장: DFT → AIMD/NEB → ML → 위상장/kMC → COMSOL → 실험이 "코팅 · 도펀트 · 적층압 · 작동창" 을 처방 · **DFT ESW 의 불확실성 (범함수 · 기준 상태 · 운동학 무시) 이 계면 수명 예측으로 그대로 전파**.

### 5.6 §3.2 이온전도·결함 — `Fig. 6` · `Fig. 7`
- 진단: 온도별 EIS · 고체 NMR · X선/중성자 회절 Rietveld · QENS. 황화물은 약한 Li–S 결합·큰 S²⁻ → 넓은 통로 · 산화물은 단단한 골격이라 구조 도핑 필요 · 이가 도핑은 공공·음이온 무질서로 σ↑ (과하면 상 불안정) · 복합양극에서 분산 불량 = 이온 병목 · 도전재 과다 = 기생 산화환원 촉진.
- **3.2.1 사례 1**: Beutl [43] 4기관 교차 실험 (§3a) · SiO₂/PVDF-HFP CSE [92] · Ge/Ta-LLZO [32] · ZrO₂–Gd₂O₃ [93] · **Sebti [94] LYC 적층결함**.
  `Fig. 6` 실독:
  - (a) ln(σT) [mS cm⁻¹ K] vs 1000/T (3.0–3.8, ≈263–323 K): 볼밀 그대로 (파랑 □) 가 위 (6.3 → 2.9) · 333/353 K 처리와 고상은 ≈4.5 → 0.5–1.2 로 겹침 · 423 K 처리 (▼) 가 맨 아래 (2.2 → −0.8).
  - (b) 흰 막대 = σ_RT (위 축 로그 10⁻⁶–10⁻³ S cm⁻¹) · 빨간 막대 = Ea (아래 축 0.3–0.55 eV): figure-read §3a.
  - (c) PFG-NMR ln D [m² s⁻¹] (−26 → −29.7) vs 1000/T (2.8–3.3). ⚠ 캡션은 "Ionic conductivity measured … using PFG-NMR" 인데 **세로축은 확산계수**다. 그리고 **고온 끝 (≈357 K) 에서는 고상 시료 성분 2 (ln D ≈ −26.0) 가 볼밀 성분 2 (≈ −26.6) 보다 높다** — "결함 많은 쪽이 자기확산이 더 크다" 는 본문 문장은 저온 쪽에서만 성립한다.
  - (d) NEB 장벽 (§3a): 적층결함이 면내 장벽을 358/255 → 132 meV 로 낮추는 것은 맞지만, **벌크 M1–M2 면외 117 meV 가 이미 적층결함 값 (121–132) 과 ±60 meV 안에서 같고**, 비화학량론 적층결함 면내 549 meV 는 **전체 최고**다. "결함 → 빠른 통로" 는 면내 홉이 율속일 때의 이야기다.
  - (e,f) Eremin [36] K-Fe-Ti-O 경로 최대에너지의 ML 회귀 (§3e). ⚠ 본문 p. 29629 는 이걸 "**Fig. 7a**" 라 부르고 p. 29627 은 출처를 [33] 으로 단다 — 둘 다 틀렸다 (캡션 = [36]).
  - (g–i) Helm [35] Li₃SbS₄ · Li₃PS₄ · Li₄SnS₄ 결함 형성에너지 vs 페르미 준위 (각각 Li₂S–X–S 영역): E_f,eq ≈ 2.1 / 1.83 / 1.4 eV 에서 Li 격자간–Li 공공 교차가 지배 · 교차 높이 figure-read ≈0.85 / ≈0.7 / ≈0.3 eV. ⚠ 본문 p. 29628 은 이 패널을 "**β-Li₃PS₄ 의 AIMD · Br 도핑이 σ 를 크게 올린다 (Fig. 6g–i)**" 의 근거로 쓴다 — 그림에는 Br 도 AIMD 도 없다. 그 내용은 우리 litdb 의 **de Klerk 2018** (리뷰 ref 57) 이다 (§9).
- **3.2.2 사례 2**: Li₇TaO₆ 0.29 eV · 5.7×10⁻⁴ S cm⁻¹ [31] · LiFePO₄ DFT+U 3.82 eV [31 — 오귀속] · K₁₋ₓFe₁₋ₓTiₓO₂ [33 → 실제 36] · 격자 뒤틀림 ↔ 장벽 [37 Kim & Siegel 2019] · Sn⁴⁺ · P⁵⁺ 치환 Li₃SbS₄ [35] · NASICON 10⁻³ S cm⁻¹ [95] · 비정질 "LiPO₃ (lithium **phosphite**)" 압축 → 장벽 ↓ [38] (⚠ LiPO₃ 는 메타인산리튬) · SEI 성분 Li₂CO₃ · Li₂O · LiF 의 공공·입계 [39] · c-LLZO Ga/Fe 도핑 → Li 화학퍼텐셜 **+0.05–0.08 eV** (σ↑) · Al 도핑 **−0.08 eV** (σ↓) [40].
- **3.2.3 사례 3**: Fan [42] 비치밀 SE 의 σ 를 FEM 으로 (상대밀도 일반 수치법). D'Amore [97] Li 음극 위 Li₂S 코팅의 ReaxFF (LAMMPS) — 700 K 값 §3a · "짧은 AIMD 와 실험이 맞았다" (수치 없음).
  `Fig. 7a–d` 실독 (확대 렌더 포함): 각 패널 = log σT (왼축, 파란 점 + 빨간 직선) vs 1/T (아래 축) 와 σT (오른축, 빨간 ◆) vs T (위 축) 를 **한 판에 겹친 이중 축**. 파란 점은 **3–4 개**, 직선 적합이 점을 잘 안 지난다 — (d) 는 1/T 1.43 · 1.67×10⁻³ 두 점이 **같은 높이** (log σT ≈ −13.2) 라 기울기가 사실상 고온 한 점으로 정해진다.
  🔴 **패널 (b) 와 (c) 가 뒤바뀌어 붙었다**: (b) 자리 그림 아래 원판 소문자 라벨이 **"c"**, (c) 자리 그림에는 **"b"** 가 찍혀 있다. 700 K 판독: (b) 자리 σT ≈ 0.197 S K cm⁻¹ → σ ≈ **2.8×10⁻⁴** S cm⁻¹ (= 본문의 '3 %' 값) · (c) 자리 σT ≈ 0.0021 → **3.0×10⁻⁶** (= 본문 '2 %' 값) · (a) σT ≈ 3.9×10⁻⁵ → 5.6×10⁻⁸ (✓) · (d) ≈1.9×10⁻⁶ → 2.7×10⁻⁹ (✓). ⇒ **본문 수치는 원판 라벨과 맞고, 리뷰의 캡션 (b = 2 %, c = 3 %) 은 그림 배치와 어긋난다.** 또 본문은 4번째를 "1 % 공공" 이라 하지만 캡션은 "1 % 격자간 Li⁺ 또는 2 % Frenkel 쌍" 이다.
  ⚠ 인가장이 모형마다 **0.03 → 0.0005 V Å⁻¹ (60 배)** 다르다 — 선형 응답 확인 없이 모형 간 σ 를 나란히 놓았다.
- **3.2.4 사례 4**: Na₃OBr DeePMD + DFT [41] (§3a — "DFT calculations produced the Na⁺ diffusion coefficient at different temperatures" 는 MD 의 일이다). Honrao [98] 표면보호 HT 15,000 · K-Fe-Ti-O 경로 ML [36] (§3e). "결정 벌크로 학습한 ML 은 결함·입계·비정질로 전이가 제한적 · UQ·물리 제약 없으면 **자료 편향을 강화**".
- **3.2.5 사례 5**: "실제 σ 는 ns · 수백–수천 원자 필요 — AIMD 밖" → MLIP. LiPON NequIP [99] (§3a). **"Kulichenko et al. [100]"** uMLIP 12종 벤치마크 (Li₃YCl₆ · Li₆PS₅Cl) · **MatterSim 으로 S/Cl 무질서 40–50 % 가 LPSCl Li⁺ 연결성을 높인다** — "정적 DFT 로는 안 보이는 특징 · 합성법에 따른 실험 σ 산포를 설명". 미세조정 CHGNet Li₃YCl₆₋ₓBrₓ [101] → 워크플로 (§4b). MLIP 은 결함 뭉침·입계·비평형에서 발산 → 능동학습 [102]. 비정질 옥시할라이드: 용융–급랭 AIMD → O 가 음이온 장거리 질서를 깨고 Li–음이온 배위를 약화 → 퍼콜레이션 확산망 (⚠ 이 문장 한가운데 "phase-stability calculations to capture anion-exchange" 가 다른 절에서 끼어든 **텍스트 오염**이 있다) [103, 104] · 낮은 탄성률·점탄성 → 저압 사이클 [105].
- **3.2.6 사례 6**: `Fig. 7e–g` (실독) — LLZTO 섬유 (10 µm · 1 µm · 100 nm) CSE 의 Li⁺ 플럭스 (색: 0–10 mol m⁻² s⁻¹), t_d = 1 / 20 / 50 s. LLZTO 영역 (노랑 ≈6 → 초록 ≈4.5 → 청록 ≈3.5) ≫ 고분자 (짙은 파랑 ≈0). 섬유가 가늘수록 고르게. Li [106 재사용] CMP/VAMMT 겔 고분자 — 수직 정렬 몬모릴로나이트 = 저굴곡 '고속도로'.
- 종합: "같은 DFT 저장벽도 결함 뭉침·입계 편석이 운반자를 묶으면 높은 σ 로 이어지지 않는다" · 황화물 = 무른 음이온 골격 + 약한 Li–S → 무질서에 관대 (적층결함·부분 비정질이 오히려 σ↑) · 산화물 = 단단한 골격이라 무질서가 장벽·입계저항 ↑ · 할라이드 = 중간 (적층결함이 통로를 연다 → 이상 벌크 모형은 σ 를 **과소**평가).
  ⚠ *"많은 계산이 10⁻³–10⁻² S cm⁻¹ 를 보고하지만 실험 **계면저항**은 한두 자릿수 더 높다"* (p. 29630) — 전도도와 저항을 같은 자릿수 잣대로 비교한 문장이다 (차원이 다르다).

### 5.7 §3.3 계면 반응·SCL — `Fig. 8` · `Fig. 9` · `Fig. 10` · `Table 2`
- 서두: 묻힌 계면 · nm · sub-s → **"계산이 주된 기전 정보원"**. SCL 형성: 화학퍼텐셜 차 → 황화물 SE 의 Li⁺ 가 산화물 양극으로 → SE 쪽 Li⁺ 고갈층 → 국소 σ ↓ · 계면저항 ↑. μ_Li = μ̃_Li⁺ + μ̃_e⁻. 코팅이 구배를 완화해 SCL 억제.
  `Fig. 8` 실독: (a) 충전 전압–시간 개념도 · (b–d) CA|SE 의 μ_Li · μ̃_Li⁺ · μ̃_e⁻ · c_Li⁺ 곡선 — **거리축·눈금·단위 없음** (개념도) · (e) 코팅층 · (f) 내장 전기장 결합 전략 · (g) 전위 사다리 개념도 (음극–계면상–SE (환원·산화 한계)–계면상–양극 · 세로 0–5 V · 숫자 없음) · (h) Li 금속 \| SE 계면 3유형 (안정 · 이온전도·전자절연 계면상 · 혼합전도 불안정 계면상) · 오른쪽 큰 패널 = LiCoO₂ \| Li₂S–P₂S₅ STEM + EDS 선 분석 (50 nm 눈금 · 0–100 nm).
  - 길이 눈금이 있는 **유일한** 패널 (Sakuda 2010 [112]): 점선으로 표시한 계면층 폭 figure-read **≈ 9–10 nm** · Co 는 ≈35 → 55 nm 에서 97 → 25 at% 로 떨어지고 SE 쪽으로 **≈20–40 nm 꼬리** (10–20 at%) · S 는 37 → 52 nm 에서 3 → 60 at% · P 는 서서히 40 at% 까지. — **리뷰 본문의 'SCL 수 µm' 를 받치는 정량 그림은 없다.** (이건 SCL 이 아니라 상호확산층이다.)
  - 🔴 **라벨 불일치**: 그림 속 **(h) = Li\|SE 계면 3유형**인데 캡션은 그것을 **(i)** 로 부르고, 라벨 없는 STEM–EDS 패널을 **(h)** 로 부른다. 본문은 "세 유형 (Fig. 8h)" · "원소 확산 (Fig. 8i)" 라 적어 **그림 라벨**을 따랐다. 또 `Fig. 8g` 캡션 "ref. 68 · Copyright 2015 ACS" 는 ref 68 (Hwang 2023 *JMCA* · RSC) 과 맞지 않는다 · `Fig. 8f` 캡션 "ref. 111 · Copyright 2020 Springer Nature" 도 ref 111 (*Batteries* 2023) 과 맞지 않는다.
- 요인: 전기화학퍼텐셜 불일치 (고전압 산화물 양극이 SE 표면 Li⁺ 를 뽑아 고갈층 + "**Li₂S 나 원소 S 같은 저항성 부산물**") · Li 금속 \| 불안정 SE 의 지속 환원 · 좁은 ESW · 분극 큰 음이온 · 탄성률/열팽창 불일치 → 공극·입계 파괴. 코팅 LiNbO₃ · "LiBO₃" · ZrO₂ · Al₂O₃ · 적층압 최적화.
- *"SCL 은 **수 µm** 두께에 이를 수 있고, 그 크기는 유전율 · 이온 농도 · 접촉 물질의 전위차로 정해지며, 이로운지 해로운지는 SE 의 확산 특성에 달렸다 [57]"* — ⚠ §10-D.
- Cheng [114]: LiCoO₂ 위 **0.06 wt%** Li₂SiOₓ 코팅 → 계면저항 ↓ · 방전용량 ↑ · STEM 으로 더 얇고 깨끗한 계면. 산화물/산화물 · 고분자/산화물 계면의 SCL 은 상대적으로 미탐색. 혼합전도체 [117].
- **3.3.1 사례 1**: Ceder 방법 (식 1 · 닫힌계 · 계면층 운동학 무시) [5]. "Al₂O₃ 는 Li · LPSC · LIC 와 덜 음의 반응에너지" [81]. Haruyama [118] DFT+U: LiCoO₂ \| β-Li₃PS₄ 사이 LiNbO₃ → 매끈한 정합 · Li 흡착 자리 없음 → SCL 억제. Gao [119] LiNbO₃ 가 Li⁺ 전기화학퍼텐셜 장벽 ↓. Richards [5]: PS₄ 기 SE 는 고전압 산화물에 산화 → PO₄ 기 + 전이금속 황화물. "Haruyama [118]: **Co↔P 교환이 유리** → SCL 성장 촉진" (⚠ 이 내용은 Haruyama **2017** · §9). Zhu [66] "LUMO–HOMO 차로도 창을 추정할 수 있다" (⚠ §9). LCO–Li₃PS₄ 계면은 2–5 V 전 구간 불안정 · mutual [−737, −594] "meV per atom" (Fig. 9a 라 적음) · total −1.27 eV/atom @ 5 V (Fig. 9b) [15].
  `Fig. 9` 실독 (확대 포함):
  - (a) 반응 에너지 (meV/atom, 0 → −400) vs A\|Al₂O₃ 혼합의 Al₂O₃ 몰분율: LIC\|Al₂O₃ (파랑) ≈ 0 · **LPSC\|Al₂O₃ (빨강) ≈ −19 ~ −21 으로 평평** (★ x ≈ 0.8) · Li\|Al₂O₃ (검정) 최소 ≈ −230 (★ x ≈ 0.33). 🔑 **빨간 선은 x = 0 (순수 LPSC) 에서 이미 ≈ −19 meV/atom** 이다 — 본문이 준 LPSC E_hull +19 meV/atom 과 같은 크기다. 즉 그 '반응 에너지' 의 상당 부분은 Al₂O₃ 와의 반응이 아니라 **LPSC 자신의 준안정성**일 수 있다 (원 논문 미확보 · 해석 보류).
  - (b) Zhu 2016 [15] 재수록: 위 축 μ_Li (−2 → −5 eV) · 아래 축 φ (2 → 5 V vs Li/Li⁺) · LGPS (빨강) · LPS (보라) · LiPON₀.₁₄ · LLZO · LLTO · LATP · 실선 = mutual · 점선 = total. 보라 실선 ≈ −600 → −740 · 빨강·보라 점선이 5 V 에서 ≈ −1270 으로 모인다 — 본문 수치와 그림이 맞는다 (패널 이름만 틀림).
  - (c–f) Haruyama 2014 [118]: LCO(110)\|LNO(1̄10) · LCO(110)\|LNO(110) · LCO(110)\|LPS(010) · LNO(1̄10)\|LPS(010) 최적 구조 (CoO₆ · NbO₆ 팔면체 · CoO₄S 오면체 삽도). 본문은 버퍼를 "**LiNbO₂** transition layer" 라 적는다 (LiNbO₃ 오식).
  - (g–j) Lai 2025 [124] HAML 280 ps 뒤 Li\|LPSC · _Se · _F · _O 구조 (원자 그림 · 정량 없음).
  - (k) **유사도** — 세로축 라벨 "Similarity (%)" 인데 눈금은 **0.80–1.00 분수**. 값 §3b. 🔑 **0 ps 기준으로 보면 _O (0.936) 도 '93 % 이상'** 이다 — 리뷰의 *"무도핑만 > 93 % 를 유지하고 도핑 계면은 뚜렷이 진화"* 는 'before relax' 기준에서만 성립하고, 0 ps 기준 차이는 0.967 vs 0.936 (3 %p) 이다.
  - (l) **결합 수** — 값 §3b. 🔑 **무도핑도 P–S 가 8 → 0 으로 전부 끊기고 Li–P 가 8 → 33 으로 4배** — "대체로 온전" 과 어긋난다 (리뷰도 "P–S 결합은 모든 계면에서 사라진다" 고 인정은 한다). 그리고 리뷰의 *"도핑 계는 Li–S · **Li–P · Li–Cl** 결합을 훨씬 더 많이 만든다"* 는 **Li–S 에서만** 성립한다 — 280 ps Li–P 는 33 vs 34–37 (같은 수준) · Li–Cl 은 21 vs 28 / **13 / 19** (F · O 는 무도핑보다 **적다**). 또 **0 ps 출발 구조가 다르다** (무도핑만 Li–P 8 · Li–Cl 11 로 출발 · 도핑 계는 0) — 비교가 출발 기하와 교락돼 있다. 마지막으로 무도핑 280 ps Li–S 막대 (58) 는 0 ps 막대와 같은 높이인데, 원 논문 자신의 다른 그림은 무도핑도 ~20 ps 안에 Li–S ~150 으로 반응한다고 보인다 (원 digest `lai2025_…` §4 — §10-D).
- **3.3.2 사례 2**: Sharafi [120] — Young–Dupré + DFT: 세척한 LLZO 위 Li 의 W_ad 가 Li\|Li₂CO₃ 의 **"거의 7배"** (절대값 두 개는 리뷰 p. 29634 — 이번 세션 규칙상 W_ad 숫자는 싣지 않는다) → 계면저항 ↓. Iwasaki [121]: Li\|LLZO 계면에서 Li 격자간 결함 형성에너지 **음수** → 계면 근처 자발 Li 삽입 (Li₇₊ₓLa₃Zr₂O₁₂). Jand [122] LCO\|LLZO (001) 격자 불일치 무질서 · Zhang [123] NCM\|LLZO Ni–La · Ni–Li 교환. `Fig. 9c–f` 서술: LCO–LPS Li 화학퍼텐셜 차 → LPS 의 Li 가 CoO₆·Li 층 위로 흡착 → LPS 질서 소실 + SCL · LNO 를 넣으면 LCO\|LNO (비슷한 구조 → 높은 접착) + LNO\|LPS (LNO 최외곽 O 가 Li⁺ 를 덜 끌어 Li⁺ 가 오히려 LPS 쪽으로) → SCL 억제 · 코팅이 표면 불안정 O 를 가둬 O 방출 억제.
  - **운동학적 안정화 단락** (p. 29634): operando 분광·현미경이 정적 DFT 상도로는 불안정한데도 **지속되는 얇은 복합 계면상** (이온전도·전자절연 → 부동태) 을 본다 → *"정적 DFT 는 운동학을 빼면 계면 반응성을 **과대평가**한다"* · 코팅은 구동력을 없애는 게 아니라 경로를 바꾸고 상호확산을 막아 준안정 부동태 계면상을 만든다. **역학적 변형의 부호·크기에 따라 SCL 을 키우거나 줄인다**.
- **3.3.3 사례 3**: Lai [124] HAML (위). Yang [126] LiPON · LLZO · Li₃PS₄ 의 (010) · (001) · (010) 면 \| SiCO 음극 HT 워크플로. Gao [127] 저에너지 LLZO (100) · (110) 종단은 Li 접촉 시 환원되기 쉬움 (저배위 Zr). Nolan [128] NCM\|LLZO 코팅 후보 Li₂ZrO₃ · Li₃TaO₄ · LiAlO₂.
- **3.3.4 사례 4**: 반응 단계 MD (초기–전이 상태 차로 확률) vs 하이브리드 MD/MC (초기–최종 상태 차) [107, 129, 130]. Wang [81]: Li\|Li₆PS₅Cl · Li\|Li₃InCl₆ 둘 다 불안정 · LPSC/Li = **절연성 SEI** · LIC/Li = **전도성 SEI** · "LIC 반응에너지가 커서 불안정, LPSC 는 작아서 더 안정" · 완충재로 **LiI** (반응 적고 Li 와 정합).
  `Fig. 10` 실독 (색 지도 · 0 → < −100 meV/atom): §3b 표. 🔑 **LiI** 행은 Li · LPSC 둘 다 흰색 (본문과 일치 · LIC 칸은 빨강 ≈ −90) · 🔑 **LiNbO₃ \| LPSC = 진한 빨강 (< −100)** — 리뷰가 §3.1 · §3.3 에서 효과적 코팅으로 소개하는 바로 그 물질이 자기 그림에서 LPSC 와 강하게 반응한다. 앞의 '운동학적 안정화' 단락이 그 설명인데 **리뷰는 둘을 연결하지 않는다**. 🔑 **La₂O₃ \| LPSC 도 진한 빨강** · **Li₃PO₄ · SiO₂ \| LPSC 는 흰색** · 순금속 Ag · Au · Cu · Hg 는 LPSC 와 흰색인데 그 **Li 합금 (LiAg₃ · LiAu₃ … )** 은 진한 빨강 — 중간층이 리튬화되는 순간 반응성이 생긴다.
  - reactive MLIP (등변 NN + 능동학습) → ns · ~10⁵ 원자 → 자기제한 SEI 성장 [102] · 그 수송값으로 COMSOL 이 Li⁺ 플럭스·계면저항 분포를 예측 [106 — 인용 의심].
- **3.3.5 사례 5**: Lee [106] LLZTO/PVDF-HFP CSE 2D COMSOL (정전기 · 희석종 수송 · Nernst–Planck · CSE 내 반응 없음 · 낮은 Li⁺ 농도 · 전하 중성).
  `Fig. 12a–d` 실독: (a) 세라믹 · (b) 고분자 · (c) 평균 플럭스 vs 방전시간 (0–18,000 s) — §3a 표. 고분자 플럭스는 섬유가 가늘수록 커지고 (280 → 1250) 세라믹은 조금 작아진다 (3200 → 2750) → 불균일 비 ≈ 11.4 → 3.8 → 2.2 (우리 산수). (d1–d3) t_d = 1 s 궤적 — 고분자 쪽 유선이 계면을 따라 휘어 오른다 (100 nm 에서 가장 촘촘). 범례가 "10 µm · 1 µm · 100 nm" 라 본문 추출의 "10 mm" 는 µ 글리프 소실이다.
  ⚠ **단위 검산 (우리 산수)**: 평탄부 ≈ 1.3–3.2 mol m⁻² s⁻¹ × F = **12–31 A cm⁻²** 상당 — 5 h (18,000 s) 방전이면 면적 용량 ≈ 90 A h cm⁻² 가 된다. 실제 셀 (mA cm⁻² · mA h cm⁻²) 과 4 자릿수 이상 어긋난다 → 플럭스 정의 (순 플럭스 vs 성분 플럭스) · 단위를 원 논문에서 확인하기 전 **정량 인용 금지**.
- 종합: DFT (반응 경로 · 분해 산물 · 띠 정렬) → AIMD/하이브리드 (속도) → ML (스크리닝 · 포텐셜) → 위상장/kMC (SCL · 조성 구배) → COMSOL (전위 · 농도 · 전류 열점) — "벌크는 좋아 보이는데 계면이 왜 실패하나 · 어디에 개입하나 · 무엇을 바꾸나 (초박 코팅 · 도펀트 · 경사 계면 · 적층압·온도창)". **"작은 원자 계면에너지 불확실성이 연속체 계면저항·전류분포 예측의 큰 오차로"**.
- `Table 2` (PDF 텍스트 전사 · 23행): 황화물-LPSCl 8행 — LiNbO₃–Li₃BO₃ 코팅 (1.50 mA cm⁻² · 100 cyc · 88.4 % · 실험 [131]) · Li₂S–LiI 희생제 (0.64 mA · 200 · 98 % · 실험 [132]) · Nb₂O₅ + 붕산 코팅·도핑 (90 mA g⁻¹ · 100 · > 86 % · 실험 [133]) · Ti₃(PO₄)₄ (0.057 mA cm⁻² · 100 · 95.2 % · 실험 [134]) · **LiPO₂F₂ (0.2C · 200 · 81.4 % · 통합 [135 Qian 2025])** · EMG 바인더 (0.2C · 300 · 85.1 % · 통합 [136]) · Li₂B₄O₇ 도핑 + 3D 망 (1C · 2000 · 80.4 % · 통합 [138]) / 황화물-LPS 음극 Li–Ga 합금/LiCl (0.1C · 100 · 84.7 % · 통합 [137]) / 산화물 LLZTO · LLZTTNO · LLZHTNO 8행 (KF 중간층 380 mA g⁻¹ · **3500 cyc · 99.99 %** 등) / 할라이드 LAOC · LYCB · LYC · LIC · LZC · LIZCO · LIHfC 7행. ⚠ '셀 성능' 열의 단위가 mA cm⁻² · **mA (면적 없음)** · mA g⁻¹ · C-rate 로 섞여 있어 **행끼리 순위를 매길 수 없다**. '통합' 판정의 기준도 적혀 있지 않다.

### 5.8 §3.4 기계·구조 — `Fig. 11` · `Fig. 12e–h` · `Table 3` (`Fig. 13` 미독)
- 서두: 기계 무결성 = K · G + 파괴인성 · 계면 접착에너지 · 크리프 저항. DFT 탄성 → 연속체 응력 · 검증 = 나노압입 · SAICAS · operando TEM. 할라이드 (Li₃InBr₆ · Li₃YCl₆) 는 작동 조건 근처 상전이 위험. **"높은 탄성률은 덴드라이트 저항을 높이지만 취성을 키운다"** (⚠ §4c #13). 적층압 "수십 MPa" 가 접촉 유지 · 공극 최소화 · Li 크리프 촉진 / 부족하면 공극 성장 · 과하면 세라믹 파괴. 복합양극: 액체가 없어 변형 완화가 안 되고 불균일 리튬화 → 박리 · 입자 이탈 · 미세균열.
- **3.4.1 사례 1**: Jeong [155 · 자기 인용] PVDF-CTFE 극성 바인더 (부타디엔 고무 BR 대체).
  `Fig. 11` 실독:
  - (a) BR / Super C / **LPSCl** / **NCM712** 적층 · (b) "PVdF-CTFE & Super C" / LPSCl / NCM712 적층. ⚠ (b) 의 고분자 쪽은 **여러 조각**으로 보이고 Cl 원자 하나가 사슬에서 떨어져 보인다 (figure-read · 해상도 한계로 확정 못 함). 그리고 (a) 는 BR 이 탄소 층 **위**에 · (b) 는 바인더와 탄소가 섞여 **LPSCl 에 직접** 닿는다 — **두 모형의 접촉 기하가 다르다**.
  - (c) 결합에너지 (eV, 축 0 → 8.0 끊김 → 9.5): BR **0.249** · PVdF-CTFE **9.016** · "36 times". 단위는 eV (면적·단량체 정규화 없음).
  - (d) '복합양극' E · K_VRH · G_VRH (§3c). 
  - (e) SAICAS 개념도 (깊이 25 / 50 / 75 %) · (f) 25 % 깊이 긁힘 사진 — BR 은 매끈 · PVdF-CTFE 는 부분 파괴 · (g) 수평 하중 vs 시간 (0–200 s) — §3c 판독 · 본문 "접착 강도 1.8 배 · 건조 중 바인더 이동 감소".
- 적층압 창: "접촉 유지에 충분하되 잔류 기공으로 Li 가 기어들지 않을 만큼" · Porz [156] 무기 SE 4종 — 기존 결함 안의 Li 도금이 균열 끝 응력 → 균열 진전 · 응력 보조 Li 침투가 고전 덴드라이트보다 입계·결함을 따라 [157–159].
- **3.4.2 사례 2**: Al/Ta-LLZO 탄성 [157] · Tian [158] LLZO 표면 균열·입계 조대 기공이 잉여 전자를 가둬 Li 핵생성 · "PVDF–CTFE 높은 결합에너지 → 견고한 복합구조 (**Fig. 12e–h**)" (⚠ 실제 `Fig. 11`) · Deng [159] LTP · β-Li₃PS₄ (§3c) · Mücke [160] NCM · LCO 이방 강성 (§3c).
- **3.4.3 사례 3**: 전기–화학–기계 결합을 명시해야 접촉 손실·계면 손상·필라멘트를 잡는다 [161–164] · 결합을 빼면 성능 지표를 크게 잘못 예측 [164] · Taghikhani [166] 위상장 + FEM 복합양극 열화 · **DEM** 이 제조·사이클 중 활물질·전해질·바인더 입자 상호작용 (접촉역학 · 입자 변형 · 응력) 을 실시간으로 — 초기 압축과 부피 팽창의 영향 예측 [167].
- **3.4.4 사례 4**: LLZO 경험 포텐셜 (Morse + Coulomb 반발 · Buckingham + Coulomb) [168, 169] 의 탄성상수가 DFT 와 **18–60 %** 어긋남 [170] → SLAD · NN ML 포텐셜 [170, 171] → `Table 3` (0 K 분자정역학 · VRH) 오차 9 % 이내 · 비정질 LLZO < 2 % [172, 173]. 층화 표집 CGCNN [130] (§3c).
  `Fig. 12e–h` 실독: (e) G_VRH R² 막대 Normal 0.822 · > 320 GPa 0.803 · > 360 0.804 · > 400 0.810 · > 480 0.812 / MAE 9.7 · 9.6 · 9.6 · 9.7 · 9.7 GPa. (f) K_VRH Normal 0.867 · > 400 0.890 · > 450 **0.892** · > 500 0.886 · > 550 0.881 / MAE 14.2 · 13.9 · 14.0 · 14.0 · 14.1. (g) 예측 vs 계산 G_VRH (−50 → 500 GPa) R² 0.852 · MAE 9.3 · (h) K_VRH R² 0.906 · MAE 13.6. 점들은 대부분 **0–150 GPa 에 몰려 있고** 400 GPa 근처 소수 점이 범위를 늘린다.
  Adjah [174] Abaqus 비결합 열–전기–기계: **> 0.8 mA cm⁻²** 에서 미세균열 개시. Barai [175] 다중척도 · 위상장 HT + 압축센싱 ML 로 덴드라이트 길이·면적비 해석식 [176] · Mücke [177] 소결 LLZO/LCO 재구성 미세구조 + 격자 기반 역학 풀이기 · Taghavian [178] 베이즈 최적화로 위상장 전착 모형의 계면 이동도 임계값 (덴드라이트 억제 + 급속충전).
- **3.4.5 사례 5**: 결합 다중물리 모형 (구조 이방 · 입간 파괴 · 리튬화 취화 · 입내 분리) · 열변형 [107] · 이방 굴곡도 흑연 [173] (§3c) · Taghikhani [179] NMC811 + **LPSC** — 작은 단결정 + 높은 적층압이 유리 · **첫 사이클에 열화 최대**. 
- 종합: DFT (탄성 · 표면에너지 · 벽개면 · 결함) → AIMD/MLIP (균열 핵생성 · Li 침투 · 국소 소성) → 위상장 · DEM · kMC (미세구조 · 입계 미끄럼 · 입자 재배열) → COMSOL · Abaqus (응력장 · 접촉 손실) — "기술적이 아니라 처방적". **MD = 국소 응력이완·결함·접착 / DEM = 입자 접촉·압력 분포 / 위상장 = 메조 균열·화학–기계 / FEM = 전 셀** 의 분업.

### 5.9 §3.5 열화 · 장기 사이클 (`Fig. 14` 미독)
- 서두: §3.1–3.4 의 고장 모드 (ESW 위반 · Ea 증가 · SCL 확장 · 모듈러스 저하) 를 통합. *"이 리뷰에서 다중척도 틀의 **가장 강력한 시연**은 아래 **정량 열화 캐스케이드**다"*.
- 진단: EIS · SEM/TEM/FIB 단면 · 방사광 XRD · 중성자 · ToF-SIMS. **"양극 쪽에서 황화물은 고전압 산화 분해로 Li₂S 와 LiₓP 같은 저항성 산물을 만든다"** (⚠ §10-A) · Li 음극 쪽 환원 분해 · 코팅 불완전 피복 · 도전재 통한 전자 누설 · 국소 열점. 무음극 계의 Li 고갈·공극 · 섬유형/저표면적 탄소.
- **3.5.1 사례 1**: Shi [52] FIB-SEM — 사이클 후 양극 입자 근처 공극·균열 → 재가압으로 80 mA h g⁻¹ 회복 · EIS 계면저항 감소 (`Fig. 14a–d` 캡션: 50 사이클 뒤 300 MPa). NMC532/Li₆PS₅Cl 계면 — **SE 의 산화환원 구동 구조 붕괴가 주 열화** [53]. LAGP / LFP / LVP FIB 박편 미세전지 in situ TEM — 입계 파괴 · 비정질화 [54]. 부족한 적층압·과다 활물질 → 결함 축적 [180]. PBE0 하이브리드로 LiₓMn₂O₄ (001) 위 EC 산화 — 저전압에서 흡착 조각 · 고전압 (LNMO · 저 Li) 에서 CO₂ — CEI 형성 후 재산화의 2단계 ("Leung et al. [183]" — 목록 183 은 Sun & Bo). Schwietert [184] "고유 창" (⚠ §9). NCM111 의 Na⁺ · Mg²⁺ · Al³⁺ 불순물 — 상 안정 · 구조 변화 · O 공공 형성 → Na⁺ 부적합 · Mg²⁺ · Al³⁺ 사이클 안정 ↑ ("**Fig. 15e and f**" — 실제 `Fig. 14e,f` · 출처 [182] → 캡션은 [181]) — 그리고 "**이 SE 들은** 고용체로 충방전" (NCM111 은 양극이다). P2-Naₓ[Ni₁/₃Mn₂/₃]O₂ DOS — Mn 이 +4 유지 → Jahn–Teller 억제 [111 · 187 혼선].
- **3.5.2 사례 2**: P2D (다공 전극 + 농축 용액 이론) 를 SEI · Li 도금 · 활물질 손실로 확장 [108] · Ali [129] 흑연 Li 도금·균열·SEI 상호의존 · "Mo et al. [28]" FE² 동시 다중척도 (⚠ ref 28 = Mo, Ong, Ceder 2012 LGPS 논문) · Barai [188] 축소차수모형 (ROM) 음극 미세균열.
  **'정량 캐스케이드'** (p. 29647 · 반복 p. 29648): ① DFT — LGPS 등 황화물은 양극 계면에서 분해에너지 **≈ −0.5 eV/atom** [15] → Li₂S 같은 저항성 계면상 → ② 위상장 — 활물질 팽창이 **> 1–2 GPa** 인장응력 → ③ 파괴인성 **20–30 J m⁻²** 인 물질에서 계면 박리 → 활성 접촉면적 **최대 −40 %** → ④ 연속체 — 계면저항 급증 → 출력밀도 **−11 %** · 용량 **−15–20 %** [166]. "분자 결합 절단이 수명을 정한다". ⚠ §10-E.
- **3.5.3 사례 3**: Klinsmann [109] 위상장 파괴 · Xu [110] 유한변형 위상장 파괴 (상분리 + 반응) · Golmon [189] 균질화 셀 응력 · Kumbhar [180] 메조–연속체 반동시 · Fathiannasab [187] 단층촬영 재구성 전극 정전류 방전 · Wegener [190] 1차 입자 방향을 넣은 3D 단일입자 · Sun [183] 위상장 리뷰 · DEM 으로 활물질/도전재 크기비 제어 → 고로딩 [191].
- **3.5.4 사례 4**: Lee [182] 2D 단일입자 모형 (피복률 · 공극 = 절연 영역) — 0.2–0.5C 는 낮은 피복률에서도 고른 리튬화 · ≥ 1C · 피복 10–30 % 에서 기울기 · 2–5C 에서 고체 확산 제한이 심각 · 높은 피복률이 균일. Fofana [192 = 185 중복] 3YSZ 섬광소결 COMSOL (아크–시료 거리).
- **3.5.5 사례 5**: Shen [74] EIS 를 ML 학습셋으로 되먹임 ("가속 도구 → 공동설계 동반자") · 베이즈 하이브리드 PINN [193] (§3e) · "ML 수명 모형은 장기 자료 부족·프로토콜 일반화 한계 → 물리 정보 + UQ (가우스 과정 신뢰구간 · 앙상블 불일치) 를 **모든** ML 열화 예측에 붙여라".

### 5.10 §3.6 통합 워크플로 · §4 미래 방향 · `Fig. 15`
- §3.6: ML 의 네 역할 — ① 물성 대리모형 (GNN · CatBoost · "M3GNet") ② MLIP (NequIP · CHGNet · MACE · MTP · DeePMD · ns–µs · 10⁴–10⁶ 원자) ③ 베이즈 최적화 · 닫힌 고리 설계 행위자 ④ PINN · 베이즈 하이브리드 NN 으로 UQ 전파. 캐스케이드 재서술. 능동학습이 매개변수 빈칸에 DFT·실험을 요청.
- §4: 시장 수치 (§3f) · 상용화 장벽 (가압·고온 셀 vs 저압·불균일 파우치 · 제조비 · 장기 검증 부족 · 생산기술 미성숙) · **"계산 워크플로가 제조 현실과 단절"** → 스크리닝 목적함수에 가공성 · 두께 허용 · 기계 순응 · 원료 가용성 · 연속체는 적층압·치밀화·코팅 균일도 관리에 · **"가장 성숙한 연결 = 원자 계산 → 재료 스크리닝 / 가장 약한 고리 = 메조 열화 → 소자 예측"** (p. 29649 — ⚠ §3.5 에서 '가장 강력한 시연' 이라 한 것과 같은 고리다).
  디지털 트윈 · 표준 입출력 · 공동체 벤치마크. 로드맵 (1) 고품질 자료·벤치마크 (2) UQ 모듈 파이프라인 (3) 제조성·안전 지표 (4) 디지털 트윈 + 자율 실험.
  `Fig. 15` 실독: "5-year roadmap for computational–experimental integration in ASSBs · Benchmarked validation → uncertainty-aware multiscale prediction → scale-relevant design rules (by Year 5)". 세 열 × VALIDATE / MODELS / DATA 세 행.
  - **Near-term (Years 0–2)**: operando 앵커 (EIS/XRD/분광) · 압력 의존 접촉 진단 · 지표에 맞춘 고장 분류 / **기준 불확실성 경계 (ESW / 수송 / 계면)** · **일관된 상태의 기준 워크플로** · 통제 실험 대비 점검 / **보고 표준화 (압력 · 온도 · 셀 형식)** · DFT ↔ operando 벤치마크 · 교차 실험실 재현 기준.
  - **Mid-term (Years 3–5)**: 임피던스 성장 영역의 검증된 예측 · 정량 신뢰도의 설계 규칙 · 파우치 조건 (RT · 저압) / UQ ML (신뢰 · 전이 · 편향) · 원자 → 소자 오차 전파 · 고장 정보 다중척도 결합 (위상장/FEM) / 산화물·황화물·할라이드 벤치마크 확장 · 실조건 계면 자료 · FAIR + provenance.
  - **By Year 5**: 제조 가능 셀 예측 지침 · 압력/접촉 설계 지도 · 빠른 고리 / 전파된 오차막대의 일상 UQ · DFT → 메조 → 소자 교정 · 디지털 트윈 시제품 / 벤치마크 모음 + 검증 점수표 · 자료와 연결된 계면 전략표 · 표준 보고 양식.
  ⚠ 본문은 "근기 1–2년 · 중기 **3–4년** · 장기 5년까지" 라 적고 그림은 "**0–2 · 3–5** · By Year 5" 다.

---

## 6. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 원형 개념도 — 원자 모델링 · 데이터 구동 · HT 스크리닝 · 다중물리 네 사분면 + 고리 문자열 (AIMD · NEB · DFT · ESW · ML · Aflow · MP · Workflow DFT · FEA · D2D · Phase Field · PyBaMM · COMSOL) + 가운데 실험 검증. 정량 0 · 'D2D' 정의 없음 | 서론용 개념 그림 참고만 |
| 2 | (미독) NCM811/LGPS 전기–화학–기계 다중척도 (미시 · 메조 · 거시) [68 Hwang 2023] | — |
| 3 | 공동설계 흐름도 — DFT/AIMD → ML → Multiscale → Continuum → Integration + 실험 되먹임 두 화살표 ('Parameter feedback' · 'Model validation & refinement'). ⚠ 본문이 말하는 E_ads · 탄성상수가 DFT 상자에 없다 | 우리 원장 흐름 (카드 → 계산 → 레지스트리 → 위험원장) 을 설명할 때 대조 그림 · '실제 구현' 근거는 아니다 (§10-E) |
| 4a,b | Li–In–Cl 삼각도 · Li–P–S–Cl 사면체 (리튬화 파랑 · 탈리튬 빨강) · LPSC 점이 Li₃PS₄–Li₂S–LiCl 단체 안 (E_hull +19 meV/atom) · **LiS₄ 포함 · SCl₃ · Li₅PS₄Cl₂ 안 보임** | 우리 GG set (LiS₄ · SCl₃ · Li₅PS₄Cl₂ 제외) 과 상 집합이 다르다는 시각 증거 |
| 4c,d | LIC · LPSC 전압 프로파일 + 평형 상 칸. LPSC figure-read 환원 ≈1.79 · 산화 ≈1.99 · 2단 ≈2.38 · 3단 ≈3.26–3.35 V · 첫 산화 산물 LiCl + LiS₄ + Li₃PS₄ | **LPSCl 창 세 번째 문헌 점** — 우리 1.717 / 2.14 (LiS₄ 포함) / 2.256 (GG) 와 규약 대조 · E_hull 미반영 가설 (§7a) |
| 4e–g | 유사상 hull · 구속 유사상 (K_crit > / < K_eff) [82 Fitzhugh 2021] | 우리 B② 구속 ESW 의 개념 원전 (`fitzhugh2021_…` · §J-71) — ⛔ argyrodite 값으로 옮기지 않는다 |
| 5a,b | (미독) NASICON 양극 3,126 → 50 스크리닝 · M3GNet 25 vs 100 구조 [85] | — |
| 5c | (미독) BLIGE · PTEN · PHEN · 역 BLIGE Na⁺ 분포 [90] | — |
| 6a–c | Li₃YCl₆ 볼밀 vs 고상: ln(σT) 아레니우스 · σ_RT/Ea 막대 (≈0.48 vs 0.068 mS cm⁻¹ · ≈0.41 vs 0.47 eV) · PFG-NMR ln D (⚠ 캡션은 '전도도') [94] | 적층결함 = 할라이드의 빠른 통로 사례 · 고온 끝에서는 고상이 더 빠르다는 그림 사실을 같이 적을 것 |
| 6d | Li₃YCl₆ NEB 장벽 막대 (358/117 · 255/294 · 132/121 · 549/62 meV · ±60) | 홉 수 검산 예시 (1 ps → 0.17 ms) · '결함 = 낮은 장벽' 이 방향마다 다르다는 반례 |
| 6e,f | K-Fe-Ti-O 경로 최대에너지 ML (ridge · RF · GB · R² 0.783/0.899/0.935) [36] (본문은 'Fig. 7a' · [33] 으로 오기) | ML 장벽 회귀의 오차 스케일 (MAE 0.012–0.028 eV/ion) 참고 |
| 6g–i | Li₃SbS₄ · Li₃PS₄ · Li₄SnS₄ 결함 형성에너지 vs E_F (E_f,eq ≈ 2.1 / 1.83 / 1.4 eV) [35] (본문은 Br 도핑 AIMD 근거로 오용) | 결함 화학 도식 참고 · Br 도핑 β-Li₃PS₄ 는 `deklerk2018_…` 로 |
| 7a–d | Li₂S ReaxFF 장 구동 MD 의 log σT 이중축 아레니우스 (3–4 점) · 공공 0.3 / 2 / 3 % · 격자간 1 % [97]. 🔴 **(b) · (c) 패널 뒤바뀜** (원판 라벨 'c' · 'b') | ⛔ li2s 트랙은 닫혔다 — 새 일 제안 없음 · SEI 트랙 Li₂S NEB 와 같은 양 아님 (장 구동 σ vs 정적 장벽) |
| 7e–g | LLZTO 섬유 (10 µm · 1 µm · 100 nm) CSE Li⁺ 플럭스 색지도 · 1/20/50 s [106] | — (고분자 복합 · 우리 축 밖) |
| 8a–f | SCL 개념도 — μ_Li · μ̃ · c_Li⁺ 곡선 (**거리축 없음**) · 코팅 · 내장장 [111] | 'SCL 정량 0' 의 또 하나의 예 (정본 §2 말미와 같은 결론) |
| 8g | 전위 사다리 (음극–계면상–SE 창–계면상–양극) 개념도 (캡션 출처 ref 68 · 2015 ACS 불일치) | 층① 창 설명용 개념 그림 |
| 8h | Li\|SE 계면 3유형 (안정 · 이온전도/전자절연 · 혼합전도) [113 Banerjee 2020] (캡션은 '(i)') | `banerjee2020_…` 정본 쪽에서 인용 |
| 8 (STEM) | LiCoO₂\|Li₂S–P₂S₅ STEM-EDS 선분석 — 계면층 figure-read ≈ 9–10 nm · Co 꼬리 ≈20–40 nm (라벨 없음 · 캡션은 '(h)') [112 Sakuda 2010] | 상호확산 규모 (nm) 참고 — SCL 두께 근거로 쓰지 않는다 |
| 9a | LIC · LPSC · Li \| Al₂O₃ 닫힌계 반응 에너지 — LPSC 곡선이 x = 0 에서 이미 ≈ −19 meV/atom (= LPSC E_hull) [81] | 준안정 SE 의 '반응 에너지' 에 자기 분해가 섞이는 함정 — 우리 interface_reactivity 를 읽을 때 같은 질문 |
| 9b | SE–LCO mutual (실선) · total (점선) vs φ 2–5 V [15 Zhu 2016] — 보라 실선 ≈ −600 → −740 · 점선 5 V ≈ −1270 (단위: 원 digest 기준 per non-Li atom) | 작동창 2.5–4.25 V 로 다시 읽기 (§7c · §J-74) |
| 9c–f | LCO/LNO/LPS 계면 최적 구조 [118 Haruyama 2014] | `haruyama2014_…` · §J-34 정본 쪽에서 |
| 9g–j | Li\|LPSC · _Se · _F · _O HAML 280 ps 구조 [124] | 원자 그림만 — 정량은 (k)(l) |
| 9k | SOAP 유사도 (before relax / 0 ps) — 0.933/0.967 · 0.845/0.920 · 0.861/0.912 · 0.887/0.936 · 축 라벨 '%' 인데 분수 | 0 ps 기준이면 _O 도 > 93 % — 리뷰 문장 반례 |
| 9l | 결합 수 0 → 280 ps — 무도핑도 P–S 8 → 0 · Li–P 8 → 33 · 도핑 계 Li–S ≈3배 · Li–Cl (F · O) 는 무도핑보다 적다 · 출발 구조 다름 | ⛔ "O 도핑이 Li 계면을 더 반응성으로 만든다" 를 이 그림으로 쓰지 않는다 (§10-D) — 우리 LPSOCl(+O) 서사에 이식 금지 |
| 10 | 세라믹 · 합금 중간층 × Li · LIC · LPSC 의 ΔE_chem 색지도 [81] — **LiNbO₃ \| LPSC 진한 빨강** · La₂O₃ 진한 빨강 · Li₃PO₄ · SiO₂ · LiI 흰색 · 순금속 흰색 → Li 합금 빨강 | 코팅·중간층 후보의 닫힌계 1차 체 (방향만) · LiNbO₃ 역설 = '열역학 반응성 ≠ 실패' 의 문헌 예 |
| 11a–c | NCM712 \| LPSCl \| Super C \| 바인더 DFT 적층 · 결합에너지 BR 0.249 vs PVdF-CTFE 9.016 eV [155 · 자기 인용] | ⚠ 흡착 ≳ 2 eV 규율 사례 — 배위 미확인 · 비정규화 · 기하 다름 (§10-F) |
| 11d | '복합양극' E 21.75 / 25.09 · K ≈ 11.2 / 14.9 · G ≈ 7.9 / 8.5 GPa | ⛔ 우리 E_VRH (comp1 22.06) 옆에 놓지 않는다 — 숫자 우연 근접 · 정의 불명 |
| 11e–g | SAICAS 개념도 · 긁힘 사진 · 수평 하중 (≈1.7–2.1× · 본문 1.8×) | 바인더 접착의 실험 지표 참고 |
| 12a–d | CSE COMSOL 플럭스 vs 시간 (세라믹 · 고분자 · 평균) + 궤적 [106] | ⚠ 단위 그대로면 12–31 A cm⁻² 상당 — 정량 인용 금지 |
| 12e–h | CGCNN G_VRH · K_VRH 예측 정확도 vs 학습셋 층화 · parity (G MAE 9.3 · K MAE 13.6 GPa) [130] | **ML 탄성 오차 ≈ 황화물 탄성값 자릿수** — §J-23 결론의 두 번째 문헌 점 (§7d) |
| 13a | (미독) 셀 열변형 개념도 [107] | — |
| 13b–e | (미독) 등방 vs 이방 굴곡도 흑연 음극 전압 · 반응 전류 분포 [173] | — |
| 14a–d | (미독) 재가압 전후 방전용량 · EIS [52] | — |
| 14e,f | (미독) NCM111 계 O 공공 형성에너지 (Li 100 % · 66.7 %) [181] | — |
| 14g–j | (미독) 단일 NMC 입자 피복률 × C-rate 리튬화 · 전압 [182] | — |
| 15 | 5년 로드맵 (0–2 · 3–5 · 5년 × VALIDATE · MODELS · DATA) — 본문 (1–2 · 3–4) 과 기간 표기 불일치 | 1단계 항목 (기준 UQ 경계 · 일관 상태 워크플로 · 보고 표준) 이 우리 원장 규율과 겹친다 — 서론/전망 문장 참고 |
| Table 1 | 계산 코드·도구 23종 (척도 · 용도 · 라이선스 · 연도) | 방법 절 도구 소개 참고 · LOBSTER · Bader · UMA 없음 · VESTA 'open source' 오분류 |
| Table 2 | 계면 공학 전략 23행 (SE 계열 × 계면 × 전략 × 재료 × 셀 성능 × 근거 유형) — LPSCl LiPO₂F₂ 행 = `qian2025_…` 와 일치 | 단위 혼재 (mA cm⁻² · mA · mA g⁻¹ · C) — 행 간 순위 금지 |
| Table 3 | 입방 LLZO 탄성 ML vs DFT (오차 0.3–8.9 %) + Abaqus 입력 Al-LLZO · NMC622 E (8.83 · 7.21 'GPa') | MLIP 탄성 검증 형식 참고 · "C₁₄" 는 C₄₄ 오식 · 수치 모델링 행 단위 의심 |

---

## 7. 우리 DFT 대비 ★★ (`../our_dft_baseline.md` · `db/properties/canonical_registry.json`)

> 규율: 리뷰 값 (2차) 과 우리 값을 **줄을 갈라** 적는다 — 같은 표 · 같은 줄에 섞지 않는다. 우리 이온 수송값 (σ · D · Ea) 은 싣지 않는다 (계 간 순위 인용이 원장에서 막혀 있다 — `cross_composition_ranking` 금지 · `HZ-cross-system-Ea` BLOCKED).

### 7a. LPSCl grand-potential 창 (축 B① · 층①)
- **리뷰 (2차 · Wang 2025 [81] · litdb 미보유)**: 본문 "LPSC 1.8–2.0 V" · `Fig. 4d` figure-read 환원 ≈1.79 / 산화 ≈1.99 V · 2단 ≈2.38 · 3단 ≈3.26–3.35 V · 첫 산화 산물 **LiCl + LiS₄ + Li₃PS₄** (LiS₄ 포함 상 집합) · 같은 편이 LPSC E_hull **+19 meV/atom** 을 보고.
- **우리 (baseline · grand-potential · `esw_lis4excluded.json`)**: 환원 한계 **1.717 V** (Li 교환 0 경계) · 산화 개시 **2.256 V** (GG set = LiS₄ · SCl₃ · Li₅PS₄Cl₂ 제외 · `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻`) · LiS₄ 포함 시 **2.14 V** · 이후 2.385 V (P₂S₇ + S) · 3.326 V (SCl). ⚠ `HZ-esw-reduction-limit-label` · `HZ-esw-reduction-limit-facet-convention` (둘 다 **CONDITIONAL**) — 창 폭 1.014 V 금지 (0.539 V) · 규약 (Li-rich facet) 을 같이 적고 다음 breakpoint 를 병기.
- **판정**:
  - 2단 (2.38 ↔ 2.385) · 3단 (≈3.3 ↔ 3.326) 은 **같은 자리**다 → 상위 계단은 판본 차에 둔감.
  - 첫 두 끝은 다르다: 환원 ≈1.79 vs 1.717 (+0.07) · 산화 ≈1.99 vs 2.14 (LiS₄ 포함, −0.15). **방향이 반대** (리뷰 쪽 창이 위에서 눌리고 아래에서 올라간다 = 좁다).
  - 🔑 *우리 산수 (가설)*: LPSC 의 준안정 에너지 **0.019 eV/atom × 13 원자 = 0.247 eV/f.u.** 를 hull 로 내리지 않고 LPSC 자신의 에너지로 반응을 세우면 — 환원 (+5 e⁻) **1.717 + 0.247/5 = 1.77 V** · 산화 (LiS₄ 경로 1.75 e⁻) **2.14 − 0.247/1.75 = 2.00 V** — **figure-read 두 끝 (1.79 · 1.99) 과 한 매개변수로 함께 맞는다.** 즉 Wang 의 '창' 은 우리 (그리고 [Zhu15]) 처럼 SE 를 hull 로 내린 규약이 아니라 **준안정 LPSC 의 에너지를 그대로 쓴 규약**일 수 있다. ⚠ 원 논문 미확보라 **검증 안 됨** · `[Wang26IF]` (litdb `wang2026_interface_stability_kinetics_sulfide_assb`) 의 1.78–2.30 V 에서 환원 끝 1.78 은 같은 꼴 (E_hull ≈ 24 meV/atom 상당) 이지만 **산화 끝 2.30 은 이 가설로 설명 안 된다** → 가설로만 둔다.
  - 개념상 짚을 것: E_hull > 0 인 상은 **모든 μ_Li 에서 중성 분해 (Li₃PS₄ + Li₂S + LiCl) 가 유리**하므로 엄밀한 '안정창' 이 없다. 리뷰는 "준안정 (+19 meV/atom)" 과 "창 1.8–2.0 V" 를 나란히 쓰면서 **어떤 규약의 창인지 적지 않는다** — 우리 'ESW 는 축을 밝힌다' 규율로는 인용 불가 형태다.
  - ⛔ "문헌 창 1.8–2.0 V 가 우리 창과 맞다/틀리다" 식 문장은 쓰지 않는다 — 규약이 확인될 때까지 **'세 번째 문헌 점 · 규약 미상'** 으로만.

### 7b. E_hull — 같은 LPSCl 의 판본 의존 (축 B · 스크리닝)
- **리뷰 (2차)**: LPSC E_hull **+19 meV/atom** [81] · 스크리닝 문턱 **≤ 50** [85] · **> 40 meV/atom 제외** [86] — 판본·보정 언급 없음.
- **litdb 원 digest**: `[Zhu15]` Table S1 — LPSCl 조성 평형 Li₃PS₄ + Li₂S + LiCl 의 E_hull **83 meV/atom** (MP-2015 · `zhu2015_…` §판정 ③).
- **우리**: E_above_hull 축은 원장에 없다 (조성 간 준안정성 = 우리 공백 · `zuo2022_…` §7b-E 와 같은 결론).
- **판정**: 🔑 **같은 Li₆PS₅Cl 이 19 vs 83 meV/atom 으로 40–50 meV/atom 문턱의 양쪽에 걸린다.** → E_hull 문턱 판정은 **DB 판본 (+ MP2020 음이온 보정 등) 에 묶인다**. 리뷰는 E_hull 을 '널리 쓰이는 스크리닝 기준' 으로 권하면서 이 의존을 말하지 않는다. 우리 도구도 `e_above_hull` 을 정렬 키로 쓴 이력이 있으니 (CLAUDE.md '조용히 틀린 경로' — `or 9e9` 사고), **문턱을 쓸 땐 판본을 행마다 남기고 같은 판본 안 상대 순위로만** 쓰는 게 맞다 (점검 제안 · 이번 세션에서 우리 cascade 의 판본 기록 여부는 확인 안 함).

### 7c. 계면 반응 에너지 · 작동창 (축 B③)
- **리뷰 (2차 · [15] Zhu 2016)**: Li₃PS₄–LCO mutual **[−737, −594]** (리뷰 "meV per atom") · total **−1.27 eV/atom @ 5 V**. 리뷰 '캐스케이드' 의 "≈ −0.5 eV/atom (LGPS)" 도 같은 원전.
- **litdb 원 digest (`zhu2016_…`)**: 단위는 **meV per non-Li atom** (Table 5 · S3) · LGPS–LCO mutual **[−696, −519]** per non-Li atom · Li₃PS₄–LCO mutual 2.5 V ≈ −627 → ≈3.0 V −594 (최소 크기) → 4.18 V 부터 평탄 ≈ −735 · total @ 5 V −1273.
- **우리 (`db/properties/oxidation_stability.json` · interface_reactivity)**: **닫힌계** (use_hull_energy) · per atom · vs LiCoO₂ 산물 Co₉S₈ + Li₃PO₄ + Li₂S + LiCl + Li₂SO₄ (값은 그 원장에서만).
- **판정**:
  - 리뷰는 **열린계 (전위 아래) per non-Li atom** 값을 "per atom" 으로 옮겼다 → 우리 닫힌계 per atom 값과 **같은 이름 다른 양**. 나란히 놓지 않는다.
  - **우리 작동창 2.5–4.25 V** 로 다시 읽으면 (원 digest 판독): Li₃PS₄–LCO mutual ≈ −594 ~ −735 meV per non-Li atom — **창 전체가 반응 구간**이다. 리뷰의 헤드라인 "−1.27 eV/atom" 은 **5 V (창 밖)** 값이다 (§J-74 의 독법과 같음).
  - "≈ −0.5 eV/atom" 은 LGPS–LCO mutual 범위의 **작은 쪽 끝**을 대표값처럼 쓴 것 + 정규화 단서 소실.
  - `Fig. 9a` 의 LPSC\|Al₂O₃ ≈ −19 meV/atom 이 x = 0 에서 이미 같은 값 → **준안정 SE 의 '혼합 반응 에너지' 에는 SE 자기 분해가 섞인다**. 우리 interface_reactivity (use_hull_energy) 를 쓸 때도 "그 최소값 중 얼마가 SE 자기 분해인가" 를 같이 적을 가치가 있다 (제안).

### 7d. 기계 (축 C)
- **리뷰 (2차 · [159] Deng 2016 · PBEsol · 원 digest 일치)**: β-Li₃PS₄ K / G / E / ν = 23.3 / 11.4 / 29.5 GPa / 0.29 · LiTi₂(PO₄)₃ 95 / 57.6 / 143.7 / 0.25. **리뷰는 범함수를 안 적는다.**
- **litdb 원 digest (`deng2016_…`)**: 같은 Table III 의 **Li₆PS₅Cl PBEsol E 22.1 / G 8.1 GPa** — 리뷰는 LPSCl 을 길게 다루면서 **이 값은 안 가져왔다**.
- **우리 (레지스트리 canonical)**: comp1 relaxed-ion **E_VRH 22.06 GPa** · EOS **B₀ 26.23 GPa** (PBE 계열 USPP · 52/520 · k444 · cubic-52). G_VRH 8.13 GPa 는 `db/properties/elastic.json` 값 (레지스트리 미등록). ⚠ 조성 간 비교는 `HZ-elastic-cross-composition` (CONDITIONAL).
- **판정**:
  - 리뷰가 인용한 β-Li₃PS₄ 는 다른 물질 — 우리 comp1 과 **같은 자릿수 (수십 GPa)** 라는 것까지만.
  - 🔑 **ML 탄성 오차 스케일**: 리뷰가 옮긴 CGCNN [130] 의 G_VRH MAE **9.3–9.7 GPa** · K_VRH MAE **13.6–14.2 GPa** 는 우리 comp1 의 G (8.13) 보다 **크고**, B₀ (26.23) 의 **52–54 %** (우리 산수) 다 → **이 계 (무른 황화물) 에서 ML 탄성 대리모형은 DFT 를 대체 못 한다.** `[WangZeierYou25]` (§J-23: LGBM K MAE 21.58 · G 16.05 GPa) 와 같은 결론의 두 번째 문헌 점. (값 비교가 아니라 오차 스케일 대 물성 스케일 판정.)
  - ⛔ `Fig. 11d` '복합양극 E 21.75 / 25.09 GPa' 는 **우리 E_VRH 22.06 옆에 놓지 않는다** — 숫자가 우연히 가깝지만 NCM712 · LPSCl · 탄소 · 바인더 적층 슬랩의 VRH 는 균질 결정 가정 밖이고 (진공 포함 여부도 미기재), NCM (같은 리뷰가 인용한 Mücke DFT E ≈ 188–221 GPa) 을 품은 복합체가 LPSCl 단독만큼 무르다는 것은 **무엇을 잰 값인지 정의가 없다**는 뜻이다.
  - 리뷰의 "relaxed/clamped 구분 0 회" 는 우리에게 실질 위험이다 — argyrodite 에서 clamped 는 ~2.3× 과대 (정본 §2).

### 7e. 전자구조 (축 D)
- **리뷰 (2차)**: LFP DFT+U 3.82 eV '실험 2.68–4 eV 와 일치' · Helm [35] Li₃PS₄ CBM figure-read ≈ 3.95 eV (범함수 미기재) · 스크리닝 '띠틈 < 1 eV = 전자전도체'.
- **우리**: comp1 **2.066** · modelc **2.099 eV** (PBE · fixed-occupation nscf 고유값 · 레지스트리 canonical · 방법일치 해소됨).
- **판정**: 다른 물질 · 다른 (또는 미상) 범함수 → **'넓은 띠틈 절연체' 수준만** 같다. Li₃PS₄ ≈ 3.95 eV 는 PBE 로 보기 어려운 크기라 (범함수 미상) 우리 2.07 과 **절대 비교 금지**. 리뷰의 *"띠틈 < 1 eV 면 전자전도체"* 문턱은 우리 계와 무관 (우리 두 값 모두 그 위). 그리고 ⛔ **띠틈을 ESW 로 읽지 않는다** — 리뷰 §2.1 의 HOMO–LUMO '상한' 은 우리 층① 창 (0.539 V) 보다 몇 배 넓은 다른 양이다.

### 7f. 수송 · MLIP (축 A · §J)
- **리뷰 (2차)**: uMLIP 12종 (UMA 없음) · MatterSim 으로 **S/Cl 무질서 40–50 % 가 LPSCl 연결성↑** · MLIP 10³–10⁴ 배 저렴 · 미세조정 500–2000 구조.
- **litdb**: `deklerk2016_…` (AIMD · 2016) 이 '할로겐 자리 무질서 → inter-cage 활성화 → σ' 서사의 원전이고 "**무질서 75 % 에서 σ 최고**" 를 보고 (원 digest). `[Agarwal26AD]` 가 UMA-s-1p1 (omat) 을 포함한 uMLIP 계면 벤치마크 (우리 쪽 외부 앵커).
- **우리**: UMA-s-1p1 (omat · 미세조정 없음) · 외부 앵커 Li₃PS₄ 힘 MAE 30.0 meV/Å. 수송값은 싣지 않는다.
- **판정**: 리뷰는 무질서 효과를 *"정적 DFT 로는 안 보이는, MLIP 대규모 MD 로 발견된 특징"* 으로 소개하지만, 같은 방향은 **2016 AIMD 원전**에 이미 있다. 그리고 '40–50 %' (리뷰 2차) 와 '75 % 최고' (de Klerk) 는 무질서 정의·조성·지표가 같은지 원전 대조 전에는 **비교 불가**. 우리 MD 축은 계 간 순위 인용이 막혀 있으므로 이 리뷰의 무질서 명제를 우리 comp1 ↔ modelc 차이에 대지 않는다.

### 7g. 진짜 차이 vs 방법 인공물 — 분류

| 항목 | 분류 | 근거 |
|---|---|---|
| LPSCl 창 첫 끝 (≈1.79 / 1.99 vs 우리 1.717 / 2.14) | **방법 (규약) 인공물 가설** | E_hull 미반영 한 매개변수로 두 끝이 같이 맞는다 (우리 산수) · 원전 미확보 |
| LPSCl 창 상위 계단 (2.38 · ≈3.3) | **일치** | 우리 2.385 · 3.326 과 같은 자리 |
| E_hull 19 vs 83 meV/atom | **방법 (DB 판본) 인공물** | 같은 조성 · 다른 MP 판본 |
| 계면 mutual 'per atom' | **표기 인공물 (정규화 소실)** | 원 digest 는 per non-Li atom |
| β-Li₃PS₄ · LTP 탄성 | **물질 차이 (비교 대상 아님)** | 다른 화합물 · PBEsol |
| ML 탄성 MAE ≈ 황화물 모듈러스 | **실질 (방법 한계)** | 오차 스케일 대 물성 스케일 |
| '복합양극 E ≈ 22 GPa' | **정의 불명 — 비교 금지** | 적층 슬랩 VRH |
| LFP · Li₃PS₄ 띠틈 | **물질·범함수 차이** | 넓은 띠틈 수준만 |
| HAML '무도핑 온전 · 도핑 반응' | **판정 보류 (자료 결함 의심)** | 원 digest: 무도핑 280 ps 막대 의심 · 출발 구조 다름 |

---

## 8. Post-processing ★ (리뷰가 거론한 분석·도구)

- **무엇**: NEB 장벽 · MSD → D → Nernst–Einstein σ · 아레니우스 · 결함 형성에너지 vs E_F (E_f,eq) · convex hull / E_hull · grand-canonical 상도 (임계 μ_Li) · 닫힌계 pseudo-binary ΔE_chem (식 1) · 열린계 mutual/total 반응 에너지 · 구속 유사상 (K_crit) · 응집에너지 · Cᵢⱼ → VRH (K · G · E · ν) · SOAP 코사인 유사도 · 결합 수 계수 (HAML) · DOS/PDOS (결정장 분리 · 결합 혼성) · ML 회귀 (ridge · RF · GB · CatBoost · LightGBM · CGCNN · XGBoost · SISSO) + R² · MAE · RMSE · 층화 표집 · 베이즈 최적화 · PINN · 연속체 (Butler–Volmer · Nernst–Planck · Fick · 열 · 응력/변형 · CZM · 위상장 파괴 · FE² · ROM · SPM · P2D) · DEM.
- **도구** (`Table 1` + 본문): VASP · QE · ABINIT · WIEN2K · CP2K · LAMMPS (ReaxFF) · GROMACS · DeePMD-kit · n2p2 · MTP · GAP · NequIP · CHGNet · M3GNet · MACE · MatterSim · SevenNet · GRACE · DPA · ASE · **pymatgen** · Matminer · AiiDA · PyBaMM · COMSOL · Abaqus/ANSYS · FEniCS (cideMOD) · VESTA/OVITO · MP/OQMD/AFLOW.
- **수치화·기록 방식**: 리뷰 자신은 **수치를 새로 만들지 않는다** — 재수록 그림의 값을 문장으로 옮긴다. 오차막대 · 시드 수 · 수렴 시험 · 입력 파일 · 데이터 공개 경로를 **한 번도 요구하거나 보고하지 않는다** (로드맵 `Fig. 15` 에서 '앞으로 할 일' 로만 등장).

---

## 9. 원 digest 대조 — 리뷰 [ref] ↔ 우리 litdb ★

| 리뷰 ref | 원 논문 | litdb slug | 리뷰 서술 | 원 digest 와 | 판정 |
|---|---|---|---|---|---|
| 5 | Richards 2016 *Chem. Mater.* 28, 266 | `richards2016_interface_stability_pseudobinary` | ΔE_chem 식 (1) · PS₄ → PO₄ + 전이금속 황화물 | pseudo-binary 닫힌 식 2 / Li 열린 식 4 · Li₆PS₅Cl 포함 | ✅ 방향 일치 (세부 수치 미대조) |
| 15 | Zhu, He, Mo 2016 *JMCA* 4, 3253 | `zhu2016_first_principles_interface_stability_assb` | mutual [−737, −594] "meV per atom" (Fig. 9a) · total −1.27 eV/atom @ 5 V · LGPS ≈ −0.5 | Table 5 · S3: **per non-Li atom** · LGPS mutual [−696, −519] · total −1273 | ⚠ 값 ✓ · **단위 축 소실** · 패널 오기 (9a → 9b) |
| 57 | de Klerk, van der Maas, Wagemaker 2018 *ACS AEM* 1, 3230 | `deklerk2018_diffusion_analysis_md_beta_li3ps4` | "**SCL 은 수 µm**" 의 근거 | **β-Li₃PS₄ MD 확산 분석 · Br · O 도핑** — SCL 내용 0 | 🔴 **오인용**. 그리고 리뷰가 [35] 에 단 'Br 도핑 β-Li₃PS₄ AIMD' 는 **이 논문 내용**이다 (번호 뒤바뀜) |
| 66 | Zhu, He, Mo 2015 *ACS AMI* 7, 23685 | `zhu2015_esw_grand_potential_origin` | "LUMO–HOMO 차로도 창을 추정할 수 있다" 고 제안 | 본론은 **중성 Li 평형 (grand potential)** 창 · LPSCl **1.71–2.01 V** · HOMO–LUMO 는 '다른 추정법' 으로 언급만 · E_hull 83 meV/atom | ⚠ **원전의 기여를 뒤집어 소개** |
| 82 | Fitzhugh … Li 2021 *EES* 14, 4574 | `fitzhugh2021_sei_design_constrained_ensemble` | `Fig. 4e–g` K_crit | K_crit = −ΔG⁰/(ε_RXN V⁰) · **argyrodite 0** | ✅ 개념 일치 · ⛔ LPSC 패널 옆 배치가 적용 가능성을 암시 — 아지로다이트 값으로 옮기지 않는다 |
| 113 | Banerjee … Meng 2020 *Chem. Rev.* 120, 6878 | `banerjee2020_interfaces_interphases_assb_review` | `Fig. 8h` 계면 3유형 | (재수록 그림) | ✅ |
| 118 | Haruyama … Tateyama 2014 *Chem. Mater.* 26, 4248 | `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` | LNO 버퍼가 **SCL 성장 억제** · **Co↔P 교환 유리** | 버퍼 = Li 흡착 자리 제거 ✓ · **SCL 은 한 번도 정량 안 됨** (원 digest · 정본 §2) · Co↔P 교환은 **이 논문에 없다** | ⚠ Co↔P 는 **Haruyama 2017** (`haruyama2017_cation_mixing_co_diffusion_lco_lps` — 리뷰 미인용) |
| 124 | Lai … Zheng 2025 *npj Comput. Mater.* 11, 245 | `lai2025_haml_li_metal_lpscl_interface_doping_seFO` | 무도핑 "대체로 온전 · > 93 %" · 도핑 "Li–S · Li–P · Li–Cl 훨씬 많이" | 유사도 · 결합 수 **figure-read 일치 (±3)** · 300 K · Γ-only · **무도핑 280 ps Li–S 막대가 0 ps 와 픽셀 단위로 같음 · 원 논문 Fig. 4e (528 ps 144) · S14c (20 ps 만에 ~150)** · 반응은 ~20 ps 안에 끝남 | 🔴 리뷰가 **의심 막대를 그대로 옮겨 결론을 세웠다** · Li–P · Li–Cl 서술은 그림과 어긋남 |
| 128 | Nolan, Wachsman, Mo 2021 *ESM* 41, 571 | `nolan2021_garnet_cathode_coating` | Li₂ZrO₃ · Li₃TaO₄ · LiAlO₂ | 같은 후보 (원 digest §Table 2) | ✅ |
| 135 | Qian … Nazar 2025 *ACIE* 64, e202413591 | `qian2025_lipo2f2_coating_stable_cei` | `Table 2` 0.2C · 200 cyc · 81.4 % · 통합 | 200 cyc @ 0.2 C · 81.4 % (147 mA h g⁻¹) · DFT hull 예측 + 실험 | ✅ 일치 |
| 159 | Deng … Ong 2016 *JES* 163, A67 | `deng2016_elastic_superionic_electrolytes_dft` | β-Li₃PS₄ 23.3/11.4/29.5/0.29 · "LATP" 95/57.6/143.7/0.25 | **PBEsol** 값 일치 · 조성은 **LiTi₂(PO₄)₃** · 같은 표에 Li₆PS₅Cl E 22.1 / G 8.1 | ⚠ 값 ✓ · 범함수 미기재 · LTP→'LATP' 오기 |
| 184 | Schwietert, Vasileiadis, Wagemaker 2021 *JACS Au* 1, 1488 | `schwietert2021_intrinsic_vs_decomposition_window_sse` | "**양극**은 더 작은 고유 창 안에서 전기화학적으로 불안정" | 대상은 **SE** · decomposition 창 (층①) vs intrinsic 창 (층②) · **황화물 4종은 intrinsic 이 훨씬 넓다** (좁아지는 건 LLTO · LATP) | 🔴 **대상과 방향 둘 다 어긋남** |
| 81 · 87 · 88 · 100 · 155 · 166 | Wang 2025 · GNoME · Chen 2024 · Du 2025 · Jeong 2024 · Taghikhani 2025 | litdb **없음** | — | — | 원전 미확보 — 2차값 그대로 · 확인 전 인용 금지 (GNoME = 대기열 #4) |

---

## 10. 비판 ★ — 이 리뷰의 약한 곳

### A. 사실·화학 오류
① **"LPSCl 산화 → Li₂S"** (p. 29621 · 출처 번호 없음) · **"양극 쪽 고전압 산화 분해 → Li₂S 와 LiₓP"** (p. 29644) · **"양극 계면 분해 → Li₂S 같은 저항성 계면상"** (p. 29647). Li₂S · LiₓP 는 **환원 (Li 흡수) 산물**이다. 전기화학 산화 (탈리튬) 경로는 Li₃PS₄ + LiCl + S (우리 grand-potential 개시 반응 · [Zhu15] 같은 반응) → P₂S₇/P₂S₅ … 로 간다. (예외 하나: 산화물 양극과의 **닫힌계 화학 반응**에선 Li₂S 가 산물에 낄 수 있다 — 우리 interface_reactivity vs LiCoO₂ 산물에도 있다. 리뷰 p. 29632 의 "SE 표면 Li⁺ 추출 + Li₂S 나 S" 는 그 의미로 변호될 수 있지만, 리뷰는 **두 기전을 구분하지 않는다**.)
② **§2.1.2 ↔ §3.3 정면 모순**: §2.1.2 *"DFT 는 σ · **계면 안정성** · ESW 를 자주 과대평가"* vs §3.3 *"정적 DFT 는 **계면 반응성**을 과대평가 (= 안정성 과소평가)"*. 방향은 **방법마다** 다르다 — HOMO–LUMO 창은 과대, grand-potential 창 (층①) 은 실용 창보다 좁다 (과소). 리뷰 자신의 §3.1 "황화물은 예측 불안정 vs 실작동 괴리" 도 후자 방향이다.
③ "H = P + EV" (→ E + PV) · "Li₆S₅ (X = Cl, Br, I)" (→ Li₆PS₅X) · "LiNbO₂ transition layer" (→ LiNbO₃) · "LiPO₃ (lithium phosphite)" (→ 메타인산염) · "LiTi₂(PO₄)₃ (LATP)" (→ LTP) · "NMC90505 = LiNi₀.₉₅Co₀.₀₅O₂" (이름과 조성 불일치) · "these SEs were charged and discharged" (NCM111 은 양극) · "DFT calculations produced the Na⁺ diffusion coefficient at different temperatures" (MD 의 일) · `Table 3` "C₁₄" (입방정 → C₄₄) · 결함 형성에너지로 제시한 식이 실은 층의 원자당 형성에너지 꼴.
④ "PS₄²⁻ breakdown" (→ PS₄³⁻) · "phase-stability calculations to capture anion-exchange" 구절이 §3.2.5 문장 한가운데 끼어든 **텍스트 오염** · "12 universal MLIPs" 인데 7개만 나열.

### B. 인용 위생 — 번호 · 이름 · 그림 짝 (리뷰에서 숫자를 가져오면 안 되는 이유)
⑤ **저자명 ↔ 참고문헌 목록 불일치**: "Ha et al. [75]" (목록 = Choong) · "Dong et al. [76]" (= Y.-C. Yang) · "Zheng et al. [88]" (= C. Chen) · "**Kulichenko et al. [100]**" (= H. Du · uMLIP 벤치마크의 저자명이 다르다) · "Shi et al. [53]" (그림 캡션 = [52] Shi · [53] = Hu) · "Leung et al. [183]" (= Sun & Bo 리뷰) · "Lee et al. [187]" (= Fathiannasab) · "Mo et al. [28]" FE² (= Mo, Ong, Ceder 2012 LGPS 논문) · "Sun and coworkers [86]" (1저자 J.-H. Kim).
⑥ **같은 번호의 다른 내용**: [31] Li₇TaO₆ 논문이 LiFePO₄ 띠틈에도 · [33] 이 LLZO 분해온도와 K-Fe-Ti-O 에 · [68] (Hwang 2023 RSC) 이 `Fig. 8g` "2015 ACS" 에도 · [106] 이 LLZTO COMSOL 과 CMP/VAMMT 겔에 · [107] (열변형 *Energies* 2025) 이 SCL 코팅·반응 단계 MD 에 · [109, 110] (위상장 파괴) 이 SCL 코팅에 · [111] (*Batteries* 2023) 이 `Fig. 8f` "2020 Springer Nature" 와 P2-Na 에 · [173] (굴곡도 MethodsX) 이 비정질 LLZO ML 에 · [177] 이 `Fig. 13c–e` 에 · [182] 가 NCM111 불순물 (캡션 = [181]) 에 · [185] (섬광소결) 이 Jahn–Teller 에 · **[185] = [192] 중복 항목** · [57] · [35] · [118] · [184] (§9).
⑦ **그림 짝 어긋남**: "Fig. 7a" (→ `Fig. 6e,f`) · "Fig. 6g–i" 를 Br 도핑 AIMD 로 (그림은 결함 형성에너지) · "Fig. 9a" (→ `Fig. 9b`) · "Fig. 12e–h" 를 바인더로 (→ `Fig. 11`) · "Fig. 15e,f" (→ `Fig. 14e,f`) · `Fig. 6` 캡션 "Copyright 2022" vs 목록 [94] *JACS* 2025.
⑧ **그림 안에서만 보이는 조립 오류** (실독으로만 잡힘): `Fig. 7b` · `7c` **패널 뒤바뀜** (원판 소문자 라벨 'c' · 'b') · `Fig. 8` 그림 라벨 (h) = 계면 3유형인데 캡션은 (i) · STEM 패널 무라벨 · `Fig. 3` DFT 상자에 본문이 말하는 탄성상수·E_ads 없음 · `Fig. 15` 기간 (0–2 · 3–5) ↔ 본문 (1–2 · 3–4) · `Fig. 9k` 축 '%' ↔ 분수 눈금 · `Fig. 6c` 캡션 '전도도' ↔ 축 '확산계수'.
⑨ **원전 미확인 수치**: GNoME "3,200만 → 381,000 → 736" [87] (원전 미확보 · 대기열 #4) · "18 신규 SE 전부 합성" [88].

### C. 단위 · 정의
⑩ Zhu16 mutual 을 "meV per atom" 으로 (원전 per non-Li atom) · `Table 3` '수치 모델링' 행 Al-LLZO E **8.83** · NMC622 **7.21** "GPa" — 같은 표 DFT E (164.5) 의 1/18 · 설명 없음 · "**파괴인성 20–30 J m⁻²**" — J m⁻² 는 파괴에너지 (G_c) 단위 (인성 K_IC 는 MPa·m^½) · `Fig. 11c` 결합에너지가 **총량 (eV)** — 면적·단량체 정규화 없음 · `Fig. 12a–c` 플럭스가 단위 그대로면 **12–31 A cm⁻²** 상당 (우리 산수) · *"계산 σ 10⁻³–10⁻² S cm⁻¹ vs 실험 계면저항 한두 자릿수 더 높다"* (전도도 vs 저항 — 차원 다름) · `Table 2` 성능 열 단위 혼재 (mA cm⁻² · mA · mA g⁻¹ · C).

### D. 근거가 없거나 원전과 다른 주장
⑪ **"SCL 은 수 µm 까지"** — 인용한 [57] 은 β-Li₃PS₄ MD 확산 논문이다 (원 digest). 황화물 SE\|산화물 양극 SCL 의 원전 Haruyama 2014 · 그 아지로다이트판 Chen 2024 둘 다 **SCL 두께 · 전위 · Debye 길이를 한 번도 정량하지 않았다** (정본 §2 말미 · `chen2024_space_charge_layer_ncm_linbo3_lpscl` · §J-77). 리뷰의 `Fig. 8b–f` 도 거리축 없는 개념도이고, 눈금이 있는 유일한 패널 (Sakuda STEM-EDS) 은 **≈10 nm 급 상호확산**이다.
⑫ **HAML '무도핑 온전 · 도핑 반응'** (`Fig. 9g–l`) — ⓐ 무도핑도 P–S 8 → 0 · Li–P 8 → 33 ⓑ 0 ps 기준 유사도는 _O 0.936 도 > 93 % ⓒ Li–P · Li–Cl '훨씬 많이' 는 그림과 어긋남 (F · O 의 Li–Cl 은 무도핑보다 적다) ⓓ 출발 구조가 계마다 다름 ⓔ 원 digest: 무도핑 280 ps Li–S 막대가 0 ps 막대 복사로 의심되고 원 논문 자신의 다른 그림은 무도핑도 ~20 ps 안에 Li–S ~150 으로 반응. ⓕ 관측창: 300 K · 280 ps · n = 1 → **기대 사건 1 ≈ 0.21 eV (검출 63 %) · 95 % 검출 ≈ 0.18 eV** — '온전' 서술이 말할 수 있는 범위가 이만큼이다.
⑬ **Schwietert 2021 [184]** 을 "양극은 더 작은 고유 창 안에서 불안정" 으로 소개 — 원전은 SE 이고 황화물은 intrinsic 창이 **더 넓다**. **Zhu 2015 [66]** 을 'LUMO–HOMO 창 제안' 으로 소개 — 원전의 기여는 grand-potential 창이다. **Haruyama 2014 [118]** 에 Co↔P 교환을 붙였다 (2017 논문 내용).
⑭ MatterSim 의 무질서 효과를 *"정적 DFT 로는 안 보이던"* 새 발견처럼 — 같은 방향은 de Klerk 2016 AIMD 원전에 있다 (litdb).

### E. 과대 주장 · 서사가 증거를 앞선다
⑮ *"`Fig. 3` 은 개념적 위계가 아니라 **실제로 구현된 공동설계 파이프라인**"* — 근거 4편이 **각자 다른 계 · 노드 하나씩** (고분자 용매 · 할라이드 SE · Na 양극 · Li–CO₂). ASSB 에서 고리를 끝까지 돈 사례는 0.
⑯ **'정량 열화 캐스케이드'** — ≈ −0.5 eV/atom (LGPS · 원전 Zhu16 · per non-Li atom) → 1–2 GPa (위상장 · 계 미상) → 20–30 J m⁻² (단위 오기) → 접촉 −40 % → −11 % · −15–20 % (Taghikhani 2025). 숫자들이 **서로 다른 계·논문**에서 왔고 인과 사슬을 한 연구가 보인 적이 없다. 그런데 §3.5 는 이걸 *"이 리뷰에서 다중척도 틀의 가장 강력한 시연"* 이라 부르고, §4 는 *"가장 약한 고리는 메조 열화 → 소자 예측"* 이라 한다 — **같은 고리**다. 게다가 1–2 GPa 인장응력은 E ≈ 20–30 GPa 급 황화물이라면 ≈3–10 % 탄성 변형에 해당한다 (우리 산수 · 계를 밝히지 않아 판정 불가).
⑰ 'uncertainty' **26 회** — 리뷰가 보여 주는 오차막대는 `Fig. 6d` 캡션의 ±0.06 eV (재수록) 하나 · UQ 를 전파한 사례 0 · 로드맵은 그걸 1–5년 뒤 과제로 둔다. **핵심 권고가 리뷰 안에서 한 번도 시연되지 않는다.**
⑱ LiNbO₃ 역설을 놓쳤다 — 자기 `Fig. 10` 에서 LiNbO₃ \| LPSC 가 진한 빨강 (< −100 meV/atom) 인데 LiNbO₃ 를 효과적 코팅으로 소개하고, 둘을 잇는 '운동학적 안정화' 단락은 따로 있다.
⑲ LFP 띠틈 3.82 eV 를 실험 '2.68–4 eV' 와 '일치' 로 — 1.3 eV 폭 범위 안에 있는 것은 판정이 아니다.

### F. 우리 규율로 다시 읽은 것
⑳ **흡착 ≳ 2 eV**: `Fig. 11c` PVdF-CTFE **9.016 eV** 는 화학결합 규모 — 결합 자리 배위수가 리뷰에 없다 (**배위 미확인** · 구조 파일 미공개) · (b) 의 고분자 쪽이 여러 조각이고 Cl 이 떨어져 보인다 (figure-read) → 결합 절단·Li–Cl/Li–F 형성 에너지가 섞였을 가능성 · 비정규화 총에너지 · 두 모형의 접촉 기하가 다르다 (BR 은 탄소 위 · PVdF-CTFE 는 LPSCl 에 직접) → *"36배 높은 결합에너지"* 는 **같은 양의 비**가 아니다. 그 자리의 결합 포화 에너지로만 읽고 일반 접착 세기·기전 근거로 쓰지 않는다. 이것이 리뷰의 **자기 인용** 대표 사례라는 점도 적어 둔다.
㉑ **Monroe–Newman 류 서술** ("높은 탄성률 → 덴드라이트 저항" · "고분자 전해질은 높은 기계 모듈러스가 필요") — 우리 정본은 무기 SE 에 이 기준을 설계원칙으로 쓰지 않는다 ([Famprikis19] · E ≈ 20–150 GPa 전 구간에서 Li 침투 실측). 리뷰 자신이 Porz [156] 를 인용해 "고전 덴드라이트가 아니라 균열을 따른 침투" 라 쓰면서 앞 문장을 유지한다.
㉒ **E_hull 판본 의존** (§7b) — 같은 LPSCl 19 vs 83 meV/atom · 리뷰는 문턱만 권한다.
㉓ **작동창** — 리뷰의 계면 반응 헤드라인 (−1.27 eV/atom) 은 5 V (우리 창 2.5–4.25 V 밖). 창 안 값은 원 digest 로 다시 읽어야 한다 (§7c).
㉔ **홉 수** — 리뷰가 옮긴 장벽들은 차수 검산과 모순되지 않는다 (§3a) — 이 리뷰는 장벽 쪽 과장은 없다.
㉕ **방법 공백** — 'best practice' 를 표방하면서 k점 · 컷오프 · 의사퍼텐셜 · vdW · SQS · 시드 · Haven · MSD 창 · 셀 이완 정책 · relaxed/clamped-ion 이 **0 회**. 연속체 best practice 5개는 구체적인데 원자 쪽은 없다.

---

## 11. 적용 인사이트 ★ (가장 날카로운 것부터)

① **LPSCl 창의 '첫 끝' 은 규약 문제일 수 있다 — 상위 계단은 이미 맞는다.** 이 리뷰가 옮긴 Wang 2025 의 2·3단 (2.38 · ≈3.3 V) 은 우리 2.385 · 3.326 V 와 같은 자리이고, 어긋나는 첫 두 끝 (1.79 · 1.99) 은 **LPSC 준안정 에너지 0.247 eV/f.u. 를 hull 로 내리지 않았다** 는 한 가설로 함께 맞는다 (1.77 · 2.00 · 우리 산수). baseline 이 열어 둔 "산화 쪽 문헌 격차" 가운데 **Wang 2025 점에 대해서는 검증 가능한 후보 설명 하나**가 생긴 셈이다 — Wang 원문 (*J. Power Sources* 640, 236719) 을 inbox 에 넣으면 규약 문장 하나로 판정된다. ⚠ 범위를 좁게: `[Zhu15]` 2.01 V 는 SE 를 hull 로 내린 규약이라 **이 가설로 설명되지 않는다** (거긴 여전히 판본·상 배제 문제) · `[Wang26IF]` 의 산화 끝 2.30 도 설명 안 된다.
② **E_hull 문턱은 판본에 묶인다 — 같은 LPSCl 이 19 vs 83 meV/atom.** 40–50 meV/atom 문턱의 양쪽이다. 우리 도구가 `e_above_hull` 을 정렬·필터에 쓰는 곳에서는 **판본 · 보정 체계를 행마다 남기고 같은 판본 안 상대 순위로만** 쓰는 게 안전하다. 그리고 준안정 SE 의 '혼합 반응 에너지' 에는 **SE 자기 분해 (E_hull 만큼) 가 섞인다** (`Fig. 9a` 의 x = 0 값) — 우리 interface_reactivity 최소값을 인용할 때 "그중 자기 분해 몫" 을 같이 적을 가치가 있다.
③ **이 리뷰의 로드맵 1단계는 우리가 이미 하는 일이다** — "기준 불확실성 경계 (ESW/수송/계면) · 일관된 상태의 기준 워크플로 · 보고 표준 (압력 · 온도 · 셀 형식) · 교차 실험실 재현" (`Fig. 15` Near-term) ↔ 우리 보고량 카드 (결과 전 게이트 · 상태 선택 정책) · 멀티시드/IQR · 레지스트리 + 위험원장 · 고정셀 + EOS · MSD 창 고정. 서론·전망 문장에서 *"필드 로드맵이 1–2년 과제로 꼽는 것을 우리는 원장 규율로 운영한다"* 는 방향은 쓸 수 있다 (자화자찬 금지 — 무엇을 하는지만).
④ **ML 탄성 대리모형은 이 계에서 못 쓴다** — G MAE 9.3–9.7 GPa > 우리 comp1 G, K MAE ≈ 우리 B₀ 의 절반. §J-23 결론의 두 번째 문헌 점 (`Fig. 12e–h`). 우리 relaxed-ion DFT 탄성의 존재 이유를 설명하는 문장 근거.
⑤ **SCL 은 여전히 정량 원전이 없다** — 리뷰가 '수 µm' 라 쓴 근거가 엉뚱한 논문이다. 우리 정본의 *"SCL 을 계산했다고 쓰지 않는다 · 'SCL 두께가 ~nm/µm 로 알려져 있다' 류는 원전에 근거가 없다"* 가 한 번 더 확인됐다.
⑥ **LiNbO₃ 역설은 '열역학 반응성 ≠ 실패' 의 문헌 예**다 (`Fig. 10`). [혁주] LZO 코팅 트랙처럼 코팅 화학을 볼 때, 닫힌계 ΔE_chem 이 음수라는 것만으로 후보를 버리지 않는다는 근거로 쓸 수 있다 — 단 Li₂ZrO₃ 는 `Fig. 10` 에 없고 (Nolan 2021 의 NCM\|LLZO 코팅 후보로만 등장), 그 트랙 문서가 그은 선 (속도 · 보호 효과는 실험과 함께) 을 넘지 않는다.
⑦ **리뷰에서 숫자를 가져오지 말 것** — 인용 번호·이름·그림 짝 오류가 30건 안팎이다 (§10-B ⑤–⑧). 이 리뷰의 쓰임은 **방법 지도 · 용어 · 로드맵** 이고, 수치는 §9 의 원 digest 나 원 논문에서만.

---

## 12. 인용 가능 문장 (영문 초안)

- "Recent reviews frame computational design of all-solid-state batteries as a closed loop in which atomistic descriptors (stability windows, migration barriers, reaction energies, elastic constants) parameterize machine-learning surrogates, mesoscale and continuum models, with experimental feedback refining each stage [Kansara26Rev]." — ⚠ 방향 문장만 · '구현됐다' 고 쓰지 않는다.
- "Electrochemical stability windows derived from different descriptors (HOMO–LUMO gaps, stoichiometric stability, or grand-potential phase equilibria) are not interchangeable and should be treated as comparative screening metrics rather than operational limits [Kansara26Rev]; we therefore report the decomposition onset of the grand-potential construction and state the phase set explicitly."
- "Energy-above-hull screening thresholds of 40–50 meV atom⁻¹ are database-dependent: the same Li₆PS₅Cl has been reported 19 meV atom⁻¹ [Wang 2025, via Kansara26Rev] and 83 meV atom⁻¹ [Zhu15] above the hull." — ⚠ 2차 소환 둘을 나란히 쓰는 문장 · Wang 원전 확인 후 각주 정정.
- "Machine-learned elastic surrogates trained on database moduli carry mean absolute errors of ~9–14 GPa [Choi 2021, reviewed in Kansara26Rev], comparable to the moduli of soft sulfide electrolytes themselves, which motivates explicit first-principles (relaxed-ion) elastic constants for argyrodites." — ⚠ 우리 값을 같은 문장에 넣을 땐 레지스트리 값 · 방법 명시.

## 13. 주의 / 한계 (인용 규율)

- ⛔ **이 리뷰의 수치를 '원전 값' 처럼 인용하지 않는다** — 전부 2차 · 인용 위생 불량 (§10-B). 쓸 땐 §9 의 원 digest 또는 원 논문에서.
- ⛔ **LPSC 창 1.8–2.0 V 를 우리 1.717–2.256 V 와 '일치/불일치' 로 쓰지 않는다** — 규약 미상 (§7a). 우리 값을 쓸 땐 `HZ-esw-reduction-limit-label` · `…-facet-convention` 규약 문장을 같이.
- ⛔ **Zhu16 mutual 값을 'per atom' 으로 옮기지 않는다** — per non-Li atom (원 digest). 우리 닫힌계 per atom interface_reactivity 와 나란히 놓지 않는다.
- ⛔ **"SCL 은 수 µm"** · **"LPSCl 산화 → Li₂S"** · **"무도핑 LPSC 는 280 ps 동안 온전 / O·F·Se 도핑은 Li 계면을 더 반응성으로"** — 인용 금지 (§10-A · D).
- ⛔ `Fig. 11d` 복합양극 E 를 우리 E_VRH 옆에 · `Fig. 11c` 9.016 eV 를 '접착 세기' 로 · `Fig. 12a–c` 플럭스 절대값을 · `Table 3` 수치 모델링 행을 인용하지 않는다.
- ⛔ `Fig. 4e–g` (Fitzhugh) 의 K_crit 를 아지로다이트 값으로 옮기지 않는다 (`fitzhugh2021_…` 금지 문장 그대로).
- ⛔ `Fig. 7a–d` (Li₂S ReaxFF) 로 li2s 쪽 일을 제안하지 않는다 — li2s 계열은 닫혔다. SEI 트랙 Li₂S NEB 와도 다른 양이다.
- ⚠ GNoME 세 수치 · '18 신규 SE' 는 원전 확인 전 인용 금지.
- ⚠ 우리 이온 수송값 (σ · D · Ea) 은 이 리뷰의 무질서·MLIP 명제 옆에 놓지 않는다 (계 간 순위 인용 금지 원장).
- ⚠ W_ad (Sharafi · Haruyama 류) 는 이 digest 에 숫자로 싣지 않았다 — 필요하면 리뷰 p. 29634 · 원 digest 에서.

---

## 14. 기법 용어 미니사전 (한 단계씩)

- **DFT (밀도범함수이론)**: 전자 수천 개의 파동함수 대신 **전자밀도 하나**로 바닥상태 에너지를 푼다. 근사는 '교환–상관 범함수' 에 몰려 있다 (PBE · PBEsol · SCAN · HSE · PBE0). 출력 = 0 K 에너지 · 힘 · 응력 · 띠 구조. 그래서 **온도·시간이 없다** — 이 리뷰의 거의 모든 '한계' 문장이 여기서 나온다. 띠틈은 PBE 가 체계적으로 작게 준다 (우리 규율: 고유값만 · '넓은 띠틈' 수준 비교).
- **AIMD (제일원리 분자동역학)**: 매 시간 간격마다 DFT 로 힘을 구해 원자를 움직인다. 정확하지만 비싸서 **수십–수백 ps · 수백 원자**가 한계. 확산은 MSD 기울기 → D → (Nernst–Einstein) σ. 짧은 궤적에서 '아무 일도 없었다' 는 **그 시간 안에 일어날 만큼 낮은 장벽이 없었다**는 뜻일 뿐이다 (관측창).
- **고전 MD · ReaxFF**: 힘을 미리 정한 식 (포텐셜) 으로 계산해 ns–µs · 수백만 원자까지. ReaxFF 는 결합이 끊기고 생기는 것을 '결합 차수' 로 흉내 내는 반응성 포텐셜이다. 정확도는 매개변수화에 달렸다 (LLZO 탄성 18–60 % 어긋남 예).
- **장 구동 MD (NEMD)**: 전기장을 걸어 이온 흐름을 직접 재는 법 (`Fig. 7a–d`). 장이 너무 크면 선형 응답 (σ = J/E) 이 깨진다 — 장 세기를 바꿔 같은 σ 가 나오는지 확인해야 한다.
- **MLIP (기계학습 원자간 포텐셜)**: DFT 에너지·힘을 학습한 신경망 (NequIP · MACE · CHGNet · UMA …) 으로 DFT 급 정확도를 10³–10⁴ 배 싸게. **범용 (universal)** 은 Materials Project 같은 거대 자료로 미리 학습한 것, **미세조정**은 그걸 우리 계 DFT 수백–수천 구조로 다시 맞춘 것, **능동학습**은 모형이 자신 없는 배치를 골라 DFT 를 더 돌리는 고리. 학습 분포 밖 (결함 뭉침 · 계면 · 고온 용융) 에서 조용히 틀릴 수 있다.
- **HAML (Lai 2025)**: AIMD ↔ MLIP-MD 를 오가며, MLIP 가 외삽 등급 (γ) 이 높은 배치를 만나면 AIMD 로 돌아가 학습을 보충하는 하이브리드.
- **NEB (nudged elastic band)**: 처음·끝 상태 사이에 '이미지' 들을 스프링으로 잇고 에너지 골짜기를 따라 늘어뜨려 **최소 에너지 경로와 장벽**을 찾는다. CI (climbing image) 는 가장 높은 이미지를 안장점으로 밀어 올린다. 정적 (0 K) 이고 경로를 미리 정해 줘야 한다. 장벽 → 홉 속도는 Γ = ν₀ exp(−Ea/kT) (ν₀ ~10¹³ s⁻¹ 가정).
- **kMC (운동학적 몬테카를로)**: 미리 아는 사건 목록 (홉 · 반응) 과 그 속도로 '다음에 무슨 일이 얼마 뒤 일어나나' 를 확률적으로 뽑아 긴 시간을 건너뛴다. 목록에 없는 사건은 영원히 안 일어난다 (리뷰: "미리 정한 홉 망").
- **위상장 (phase-field)**: 상 경계·균열을 날카로운 선 대신 **매끄러운 질서변수 장**으로 표현해 미세구조 진화 (상분리 · 덴드라이트 · 균열 진전) 를 연속 방정식으로 푼다. 입력은 계면에너지 · 이동도 · 확산계수 등 — 원자 계산에서 받는 '유효 매개변수'.
- **FEM / COMSOL / Abaqus**: 실제 기하를 작은 요소로 쪼개 편미분방정식 (전하·물질·열 보존 · 응력 평형) 을 수치로 푼다. COMSOL 은 여러 물리를 결합하는 상용 플랫폼. 리뷰의 best practice 5개 (단위·기준 상태 · 메시/시간 수렴 · 과매개변수화 · 불균질 · 풀이기 결합) 가 여기에 걸린다.
- **P2D (의사 2차원) · PyBaMM**: Newman 모형 — 전극 두께 방향 1D × 입자 반경 방향 1D 를 겹쳐 다공 전극 전체를 푼다. 셀 전압·용량을 빠르게 내지만 입자 사이 불균질은 평균으로 지운다. PyBaMM 은 그 오픈소스 구현. SPM (단일입자 모형) 은 더 단순화한 것.
- **FE² · ROM**: FE² = 거시 FEM 의 각 적분점마다 미시 FEM 을 붙이는 동시 다중척도 · ROM (축소차수모형) = 비싼 모형을 몇 개 모드로 줄인 근사.
- **DEM (이산요소법)**: 입자 하나하나를 강체/변형체로 두고 접촉력으로 움직인다 — 압축 · 혼합 · 접촉망 · 균열 (µm 입자 역학). 우리 정본 경계: **µm 급 입자 역학은 DEM/연속체 몫**, 우리는 재료 상수 (E · G · B · γ · ΔV) 를 댄다.
- **ML 스크리닝 대리모형**: 이미 계산된 자료 (MP 등) 로 물성을 회귀하는 빠른 모형 — CGCNN · M3GNet · CHGNet (그래프 신경망) · CatBoost/LightGBM/XGBoost (부스팅 트리) · SISSO (기호 회귀). 성능은 R² · MAE 로 말하지만, **MAE 가 대상 물성 크기와 같은 자릿수면 그 계에선 쓸모가 없다** (ML 탄성 예).
- **생성 모형 (MatterGen)**: 확산 모형으로 원자종·좌표·격자를 함께 만들어 내되 조성·대칭·물성 조건을 걸 수 있다 — '후보를 고르는' 대신 '후보를 만드는' 역설계.
- **베이즈 최적화 · PINN**: 베이즈 최적화 = 다음에 어디를 계산/실험할지 불확실성까지 따져 고르는 법. PINN = 학습 손실에 물리 방정식 (Butler–Volmer · Nernst–Planck) 잔차를 넣어 물리를 어기지 않게 한 신경망.
- **Convex hull · E_hull**: 조성 공간에서 가장 안정한 상들을 잇는 아래 껍질. E_hull = 그 껍질 위로 몇 meV/atom 떠 있나 (0 = 안정 · > 0 = 준안정). **DB 판본·보정에 따라 바뀐다** (LPSCl 19 vs 83 meV/atom).
- **ESW 3법**: ① HOMO–LUMO (분자/띠 가장자리 — 전자만 보고 화학반응 무시 → 창 과대) ② 화학량론 안정 (Li 하나씩 넣고 빼며 골격 유지 여부) ③ 상안정 = **grand-potential** (Li 에 열린 상도에서 SE 가 분해되기 시작하는 μ_Li → 전압. 실용 창보다 좁게 나온다 = 우리 '층①'). 같은 이름 'ESW' 지만 **세 양은 서로 다르다**.
- **mutual / total 반응 에너지 (Zhu 2016)**: 계면 두 물질을 섞었을 때 (mutual) vs 섞은 것 + 전위 아래 Li 교환까지 (total) 의 최대 구동력. 닫힌계 (Li 교환 없음 · Richards 식 1) 와 열린계 (전위 고정) 를 구분하고 **정규화 (per atom vs per non-Li atom)** 를 같이 적어야 같은 양이 된다.
- **구속 앙상블 · K_crit (Fitzhugh 2021)**: 분해 산물이 원래보다 부피가 크면 주변이 되눌러 분해가 손해가 된다. 그 되누름의 유효 강성 K_eff 가 임계값 K_crit 보다 크면 계면 반응이 멈춘다. 우리 B② (구속 ESW) 의 개념 원전.
- **SCL (공간전하층)**: 두 고체의 Li 화학퍼텐셜 차 때문에 계면 근처에 Li⁺ 가 몰리거나 빠진 대전층. 개념은 오래됐지만 **두께·전위 프로파일을 정량한 원전은 아직 없다** (우리 정본 판정).
- **VRH 평균**: 단결정 Cᵢⱼ (방향별 강성) 를 다결정 등방 값 (K · G → E · ν) 으로 바꾸는 법 — Voigt (균일 변형 · 상한) 와 Reuss (균일 응력 · 하한) 의 평균. **균질한 결정** 을 전제한다.
- **relaxed-ion vs clamped-ion 탄성**: 변형을 줄 때 원자가 셀 안에서 다시 자리를 잡게 하느냐 (relaxed) 그대로 두느냐 (clamped). argyrodite 처럼 무른 골격은 clamped 가 ~2.3배 과대 — 우리는 relaxed 만 인용.
- **SOAP 유사도**: 각 원자 주변 환경을 벡터로 인코딩해 두 구조의 코사인 유사도 (0–1) 를 낸다. 전체 평균이라 **얇은 계면층의 화학 변화에 둔할 수 있다** (HAML 의 '> 93 %' 와 'P–S 전부 끊김' 이 함께 성립하는 이유).
- **SAICAS**: 다이아몬드 날로 정해진 깊이를 수평으로 긁으며 박리 하중을 재는 접착 시험.
- **Nernst–Einstein · Haven 비**: σ = n q² D / (kT) — 추적자 D 로 σ 를 내는 식. 이온들이 함께 움직이면 (상관) 보정이 필요한데 그 비가 Haven 비 H_R. 우리는 H_R = 1 로 두고 절대 σ 를 인용하지 않는다.
- **응집에너지**: 고립 원자들이 결합해 화합물이 될 때 내놓는 원자당 에너지 — 결합 세기의 대략적 지표. 계면 '안정성' 을 이것만으로 말하면 반응 경로·준안정상이 빠진다 (리뷰 자신도 인정).
- **디지털 트윈**: 특정 셀 하나를 따라가는 물리 기반 모형이 제조·작동 센서 자료를 받아 계속 갱신되며 열점·고장 전조·공정 조정을 예측하는 것. 리뷰 로드맵의 5년 목표.
