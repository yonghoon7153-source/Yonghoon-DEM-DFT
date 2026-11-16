> # 🔎 6 월 덱 두 판의 지금 유효성 (배너 2026-11-16)
>
> 이 문서로 만든 덱이 두 판 있다 — **06-22 pptx (27 장 · 우리 판)** 과 **06-23 PDF (24 쪽 · 사수 수정판)**.
> 아래 판정은 11-16 원장 · litdb 기준이고 **PDF 쪽 번호**로 적는다 (괄호 = pptx 장).
> ✅ 그대로 유효 · ⚠ 조건부 (표현 · 단서를 고쳐야 함) · ⛔ 지금은 못 씀. 금지 값은 여기 다시 적지 않는다 (위치만).
>
> **사수 판에서 바뀐 것 (pptx → PDF)**
> - 빠진 장 — s8 PMF F* · s23 자리별 PDOS (free S²⁻ 가 가장 얕다) · s24 CDD · s25 UPS 대 DFT · s26 ESW 개념도
> - 빠진 문장 — s5 '1.41 × 3.2 ≈ 4' · s6 단서 ('새 채널은 BVS 가 큰 덜 유리한 자리 · 정적 채널만으론 σ↑ 를 설명 못 함') 와 8.75 → 7.4 % ·
>   s10 '조성이 아니라 disorder 가 결정' · s12 'Li 공공 → Coulomb 응집 약화 → bulk 연화' · s21 N(EF) 행 ·
>   s27 '산화 onset = S²⁻ → S₂²⁻ · free S 가 먼저' 와 '> 3.3 V PCl₅ 단계' · s2 문헌 DFT 기계값 (→ '--')
> - 새로 들어온 것 — p3 계산 descriptor 개요 · p6 MSD 단독 장 · p13–14 VRH 식 · p16 |ICOHP| 막대그림 · p18–19 '다른 원소 치환 때 활용' 주석 ·
>   p21 '절대값 사용 불가 · 진공 도입 확인 예정' · **p22 'LPSC1.6 산화 안정성 저하 = S VBM 상대 이동'** · p24 Liu 2023 Angew · p2 BML 실험 Ea (LPSCl)
> - 고친 라벨 — p7 'Accessible sites' → 'Li 개수' (✅ 사수 쪽이 맞다 — 5×5×5 셀의 Li 원자 수 3000 / 2700)
>
> | PDF 쪽 (pptx) | 내용 | 판정 | 이유 |
> |---|---|---|---|
> | p2 (s2) | 문헌 · BML 요약표 | ⛔ / ⚠ | DFT σ 열은 MLIP-MD 상온 외삽 절대값 (인용 금지) · DFT Ea 열은 단일 시드 계간 대조 (`HZ-cross-system-Ea` BLOCKED · LPSCl 값 HOLD) · 'DFT' 가 아니라 MLIP-MD · E 는 설정이 달라 각주 비교만 (`HZ-elastic-cross-composition`) · 띠틈 ✅ · 문헌 값은 방법 표시 없이 우리 값과 한 줄에 두지 않는다 |
> | p3 (새) | 계산 descriptor 개요 | ✅ (⚠ 1) | ELF · Bader 는 p18–19 스스로 '결합 특성 불변' 이라 '(원인)' 보다 '(대조)' |
> | p5 (s4–5) | Arrhenius · D 표 · σ(300 K) | ⛔ | 'AIMD' → MLIP-MD (UMA · 07-27 정정) · 단일 시드 계간 Ea · D 대조 BLOCKED · σ 절대값 금지 (Nernst–Einstein · Haven 1 = 상한) · ×4 분해 줄이 빠진 건 ✅ |
> | p6 (s4) | MSD | ⚠ / ⛔ | 식 ✅ · 'LPSCl1.6 MSD 증가' 는 같은 단일 시드 계간 대조 (비율은 멀티시드 판정만) · 기울기 창을 적는다 (규약 2–50 ps) |
> | p7 (s6) | Li 자리 BVS 분포 | ✅ 표 · ⚠ 해석 | 표는 Li 자리 BVS 분포라 '채널' 이 아니다 · 상대 비교만 (S · Cl R0 출처 미기록 → Li BVS ≈ 1.7) · pptx 단서를 빼고 'percolated network → 이동 용이' 로 세졌는데 이 표는 연결성을 재지 않는다 · '부피 15 % 감소' 는 옛 정의 (저-BVSE ≤ 0.30 채널) 라 원장 정의 (원래 주기셀 · above-min iso) 와 같이 쓰지 않는다 |
> | p8 (s7) | Li 밀도 · 케이지 연결 | ⚠ | 'AIMD' → MLIP-MD · 'LPSCl 케이지 고립' 은 완전 정렬 comp1 모델의 성질 (실제 Li₆PS₅Cl 의 S/Cl 무질서는 측정법에 따라 5–62 % · litdb `feng2020` · `kraft2017`) → '정렬 대 무질서 모델' 대조로 |
> | p9 (s9) | Voronoi std | ✅ 관찰 · ⚠ 주석 | comp1 은 정렬 모델이라 std 0.00 은 구성상 당연 → 'F-43m 등가 자리의 직접 증거' 는 순환 |
> | p10 (s10) | 무질서 맞춘 Ea | ⚠ (⛔ 1 행) | '기존' 행은 p5 와 같은 BLOCKED 값 · 조절 값은 원장 미등록 (06-09 앙상블 · d 0.5 · n 3 · β 게이트 평가 안 됨) · '비슷한 Ea' 까지 — '결정학적 disorder 정도에 따라 Ea 차이 유도' 는 아직 인과 주장 |
> | p12 (s12) | EOS · B₀ | ✅ | canonical (`b0-dft-bm3-v1` · 같은 비교군) · 기전 문장이 빠진 건 ✅ (Li 배치만 바꿔도 B −33 % · litdb `pustorino2025`) |
> | p13 (s13) | E · B · G VRH · ν · Zener A | ⚠ / ⛔ | E · G 는 각주 비교만 · **Zener A 증가 ⛔** — 세 쌍 값 (comp1 1.14 / 0.75 / 0.92 · modelc 1.44 / 2.25 / 0.50) 의 산포가 차이보다 크다 (elastic.json) |
> | p14 (s14) | Cij · C44 +72 % | ⚠ | modelc C44 13.7 은 세 값 17.8 / 18.4 / 4.85 의 평균 · 2× 셀 검사 회색 (11-03 마감) → 전단 증가 미확인 |
> | p15–16 (s15–16) | ICOHP | ✅ 평균 · ⛔ 자리 분할 | 평균 \|ICOHP\| 막대 (`b2o3_icohp.json` 의 modelc 값과 일치) 는 유효 · 4a Cl 90 % / 4d Cl 10 % 와 자리별 값은 10-14 에 정정된 Li 배위 분류기 산물 — P 배위로 세면 4d Cl 3/8 → 다시 가른 뒤에 |
> | p17 (s17) | 결합 길이 | ✅ 평균 · ⛔ 자리별 | 4a / 4d 길이 · Cl Voronoi 는 같은 분류기 문제 |
> | p18–19 (s19 · s18) | ELF · Bader | ✅ | 'ICOHP · 길이 변화는 순수 geometry 때문' 은 맞는 방향의 추론까지 |
> | p21 (s21) | DOS · 띠틈 | ✅ (문구 ⚠) | 띠틈 canonical (fixed-occ nscf) · 결론 맞음 · 문구 두 곳: 주기 bulk DFT 는 진공 준위가 없고 기준이 셀 평균 전위라 셀끼리 절대값이 안 맞는다 ('Evacuum 임의 설정' 이 아님) · 절연체 EF 는 smearing 점유가 갭 안에 놓는 값 ('DOS edge 에서 도출' 이 아님) |
> | **p22 (s22)** | PDOS 표 + **새 문장** | 표 ✅ · **문장 ⛔** | 'LPSC1.6 산화 안정성 저하 = S VBM 상대 이동' 은 ① p21 이 못 쓴다고 한 절대 VBM 을 쓰고 ② p23 · 우리 ESW (두 조성 산화 onset 같음) 와 어긋나고 ③ 덱 p2 에도 실험 저하 근거가 약하다 (BML LPSCl 칸 비어 있음 · 문헌 1.95 대 1.9 V) |
> | p23 (s27) | grand-potential ESW | ⛔ / ⚠ | **'환원 한계 1.24 V' ⛔** (`HZ-esw-reduction-limit-label` · off-by-one) — 1.24 V 는 아직 Li 를 흡수하는 첫 환원 평탄이고 아래 가장자리는 1.717 V (= 표의 'OCV 자가분해') · 산화 2.14 V ⚠ — LiS₄ 가 든 상집합 값 (LiS₄ · SCl₃ · Li₅PS₄Cl₂ 를 뺀 지금 상집합은 2.256 V · 문헌 2.01 V 와의 차는 미해결) → 판을 적는다 · '두 조성 차이 없음' ✅ · 열 이름 comp1 / modelC → 조성 이름 |
> | p24 (새) | Liu 2023 Angew (MgF₂ 공도핑) | ✅ | litdb `liu2023_electron_redistribution_redox_resistible_mgf2` (DOI 10.1002/anie.202302655) · Li 금속 쪽 (환원) 이야기 · 그 논문 PDOS 'gap' 은 smearing 0.2 eV PDOS 추정치 (digest) |
>
> p1 · p4 · p11 · p20 은 표지 · 장 표지다. ⛔ 아래 09-09 배너와 본문은 지우지 않는다 (kb/SCHEMA.md Update Policy).

> # ⛔ σ "4배" · 절대 σ · 조성 간 Ea 대조는 **인용 금지** (배너 2026-09-09)
>
> 이 카드는 comp1↔modelc 의 **σ 비(~4×)와 절대 σ(3.35 → 13.96 mS/cm)** 를 헤드라인으로 쓴다.
> 값은 **이력으로 보존**하되, 지금은 아래가 이긴다:
> - **σ 절대값 인용 금지** (CLAUDE.md 데이터 규율 — Nernst–Einstein Haven=1 은 **상한**이다).
>   정본 `db/properties/li_transport.json` 스스로 같은 ~14 를 *"실험보다 3–5배 높다"* 고 적는다.
>   ⇒ *"실험 x=0.6 = 11.34 mS/cm 와 일치"* 류의 문장은 **다른 조성의 실험값을 골라 맞춘 것**이라 쓰지 않는다.
> - **조성 간 순위·비 금지** — `canonical_registry.json` 의 `MD_Ea_eV_singleseed@comp1`(0.2532)은
>   **단일시드 · `provisional`** 이고 `prohibitions` 에 `absolute_sigma` · `cross_composition_ranking` ·
>   `cite_until_beta_gate_passes` 가 걸려 있다. 계간 Ea 직접 비교는 `HZ-cross-system-Ea` = **BLOCKED**.
>   (`md_axis_status_2026_09_07.md` §0: *"지금 이 축에서 원고에 넣을 수 있는 활성화에너지는 0개"*.)
> - **방법 라벨**: 여기서 "AIMD" 라고 쓴 것은 실제로 **MLIP-MD (UMA-s-1p1, task=omat)** 다.
>   ab initio MD 논문과 나란히 놓으면 방법 오기가 된다 (2026-07-27 정정).
> - ✅ **살아 있는 것**: 구조 관측(anti-site Cl · Li 공공 · Voronoi/BVSE 기하)과 **계 내부** 서술.
>   ⚠ "장벽↓ + 캐리어↑" 기전은 두 조성의 Ea·D₀ 대조 위에 서 있으므로, **조성 간 정량 대조로는
>   쓰지 않는다** — 기전을 말하려면 축이 먼저 열려야 한다.
>
> ⛔ 아래 본문은 지우지 않는다 (kb/SCHEMA.md Update Policy).

# Structure–Property Relationship of Argyrodite SEs — 통합 논리 (MASTER)
LPSCl (Li₆PS₅Cl) vs LPSCl₁.₆ (Li₅.₄PS₄.₄Cl₁.₆) · 2026-06-21
모든 수치는 우리 DFT/MLIP db. 흩어진 per-axis 리포트를 하나의 인과 사슬로 통합.

---

## 0. 중심 명제 (one sentence)
> **할로겐 enrichment(Cl↑)는 "구조 레버"다: 결합 화학은 그대로 둔 채 Li 공공 + anti-site Cl/S 무질서만 주입한다. 이 구조 변화가 이온전도도(×4)와 강성(+25%)을 동시에 올리면서, 내재 산화창은 그대로(S²⁻-limited)이고 양극 열역학 반응성은 오히려 낮춘다. Cl-rich의 알려진 실험적 단점은 열역학이 아니라 kinetic/interfacial이다 (전자전도도 두 조성이 같아서 원인 아님 — 후보: 이온전도 ×4·CEI passivation, 세부는 본 계산으로 미규명).**

---

## 1. 인과 사슬 (structure → property)

### [A] 조성 변화 = 두 가지 구조 효과
**Aliovalent 치환** 2Cl⁻ → S²⁻ + V_Li (Kröger–Vink: Cl•_S + V′_Li). 결과:
- **(i) Li 공공** (5 f.u.당 Li 27 vs 30 → 3 vacancy)
- **(ii) anti-site Cl/S 무질서** (free-anion 4a/4d 자리 SOF 분산)
→ 이 둘이 모든 물성 변화의 *뿌리*. (≠ "mixed", ≠ 공유성 변화)

### [B] 이온전도도 ×4 — 이중 메커니즘
| 인자 | 값 | 출처(증거) |
|---|---|---|
| Ea 인자 exp(ΔEa/kT)@300K | **×3.2** | AIMD Ea 0.253→0.224; anti-site가 inter-cage landscape 평탄화 |
| carrier/D₀ 인자 | **×1.41** | D₀ 4.11e-4→5.8e-4; Li vacancy가 운반자↑ |
| **곱** | **×4.5 (≈실측 14/3.4=×4.1)** | 잔차 거의 0 |

**다중 독립 증거 (같은 결론):**
- **AIMD-MLIP**: Ea 0.253→0.224, σ 3.4→14 mS/cm, D600 3.09e-6→7.90e-6.
- **BVSE**: comp1 단일 채널(BVS 1.60–1.64) → modelc bimodal(60.2%가 1.83–1.89, anti-site Cl 인접). 정적 채널은 −15%인데 σ는 ×4 (역설) → vacancy가 BVSE 못 보는 곳에서 작동.
- **Voronoi 무질서 std**: P 0→0.37, Cl 0→0.74, Li 0.21→1.15 (무질서↑ 정량).
> ⚠ **2026-08-05 단서 (open_items #9)**: 아래 F* 는 **600 K MLIP-MD** 궤적 산출이고,
> comp1 의 그 궤적(deck)은 β 게이트 **미검사**이며 형제 시드는 **6/6 케이지**다.
> F* 는 연결 경로의 **가장 덜 방문된 voxel** 이 정하므로 표집 부족 시 **상한(과대)** 이고,
> 더 갇힌 comp1 이 더 부풀려져 **−15% 감소폭이 과장됐을 수 있다**. 1600 ps 연장이 판별.
> 또한 BVSE 와는 독립이지만 **MD 와는 같은 궤적**이라 상호검증으로 쓰면 순환논증이다.
- **Percolation (Li-density PMF, F=−kT·lnρ, exact cube)**: 침투 *전이*(largest-cluster steepest-rise) comp1 **0.20** → modelc **0.17 eV** (~15%↓, **AIMD Ea 0.253→0.224와 정합**, ratio 0.85≈0.89). ⚠️ 첫-관통(first-spanning) 정의는 0.20/0.08이나 modelc의 0.08은 largest-cluster **1.4% 가는 실가닥(유한크기 우연 연결)**이라 대표 장벽 아님 → **전이값(0.20/0.17) 사용**(2.5×가 아니라 ~15%↓). inter-cage 경로 평탄 = Ea↓를 BVSE와 독립 재확인; cluster-count/부피 역설 해소.

### [C] 결합 화학은 불변 (= 대조군, σ↑가 구조 탓임을 증명)
- **ELF**: Li–Cl·Li–S 이온결합 + P–S 공유결합, **조성 무관 유지** (bond-min ELF 동일).
- **Bader**: Li +0.88, Cl −0.91, P +4.7, S −1.8; **PS₄ 전하 불변**. (|Cl|>|Br| = Cl이 더 이온성)
- **CDD**: 재배치 ~5.8e(comp1)/6.84e(modelc), 둘 다 노랑(P–S 축적)/파랑(Li 결핍) **같은 패턴**.
→ **σ 변화는 공유성/전하 변화가 아니라 순수 구조(공공+무질서)** — 3개 독립 방법이 같은 대조 결론.

### [D] 기계: B0↓(vacancy) vs E_VRH↑(disorder) — 두 모듈러스가 반대로 (paradox 해결)
- **B0 (bulk, EOS)**: comp1 **26.2** → modelc **21.7 GPa (−17%)** ← **vacancy**: Li⁺ 빠지면 Coulomb 응집↓ → 부피압축이 쉬워짐(**bulk 연화**).
- **E_VRH (Young, relaxed-ion)**: comp1 **22.1** → modelc **27.7 GPa (+25%)** ← **anti-site disorder**: C44(전단) 8.0→**13.7** + Zener A 1.14→**1.44** → G(전단)↑. E는 전단 지배라 **E↑**.
- **★ divergence**: E = 9KG/(3K+G)에서 vacancy의 **K↓**를 disorder의 **G↑**가 이겨 net **E↑**. 즉 **vacancy = bulk 연화 / disorder = shear 강화**, 서로 반대 방향. (vacancy 단독은 오히려 E를 내리는 쪽.)
- clamped-ion은 둘 다 52.3로 동일(2.3× 과대 = paradox 인공물) → **relaxed-ion이라야 이 divergence가 드러남**. EOS B0(26.2) ≈ relaxed B_VRH(25.5) 교차검증.
- (정량 분리: ordered-vacancy vs disordered modelc의 C_ij 비교 = Ea 슬라이드7 disorder-control의 기계 버전.)
- clamped-ion은 52.3으로 둘 다 동일(2.3× 과대) = **paradox 인공물**. 이온 이완(Born screening) 허용해야 실험(~23)·문헌 DFT(SQS 22.1, ensm 27.8–29.9)와 일치.
- EOS B0(26.2) ≈ relaxed B_VRH(25.5) → 교차검증 통과.
→ Cl-rich가 **더 단단함** (문헌 Kim 초음파는 두 조성 비슷하나, 단결정 DFT는 강화 예측).

### [E] 전자구조는 조성 무관 (gap·VBM)
- **gap (eigenvalue)**: comp1 **2.066** ≈ modelc **2.099 eV** (PBE; 실제 mBJ 3.11/HSE 3.30). 갭은 disorder 무관.
- **VBM = S 3p** (둘 다). **PDOS**: free S²⁻ 3p가 가장 얕음(mean −0.88/−0.90 eV), PS₄-S 깊음(−2.14/−2.25, P–S 공유결합 안정화), Cl 더 깊음(−2.83).
→ **free S²⁻ = 산화-prone 자리**, 조성 무관. Cl-rich는 free S²⁻를 4→2로 줄임.

### [F] 산화/전기화학 안정성
- **내재 ESW (grand-potential)**: 둘 다 환원 1.24 / OCV 1.72 / **산화 onset 2.14 V (S²⁻→폴리설파이드)**. **동일** — Cl⁻는 3.3 V까지 불활성이라 onset 안 바꿈 (S²⁻-limited). VBM 0.32 eV 차이에도 onset 동일 = 산화는 밴드엣지 아니라 분해화학.
- **계면 반응성 (전압분해, v2)**: LPSCl이 모든 양극·전압에서 **더 반응성**, 격차 +0.04(2.5V)→+0.20(4.3V). Cl이 반응성 S/Li를 희석 → **Cl-rich가 열역학적으로 덜 반응**.
→ 문헌 "Cl-rich 양극서 더 나쁨(분해전류↑)"은 **열역학 아님 → kinetic/interfacial**. ⚠️ **전자전도도 아님** (LPSCl≈LPSCl1.6 갭 2.066≈2.099 → σ_e 동일). 후보: 이온전도 ×4가 분해 kinetics 가속 / CEI passivation 품질 (세부 미규명). 우리 계산이 *열역학·전자구조* 둘 다 배제.

---

## 2. 마스터 비교표
| 물성 | LPSCl (comp1) | LPSCl₁.₆ (modelc) | 변화 | 근거 |
|---|---|---|---|---|
| 구조 | 입방, 공공 0 | 능면체, 공공 3/5fu + anti-site | 무질서↑ | XRD/구조 |
| Ea (eV) | 0.253 | 0.224 | ↓ | AIMD |
| σ₃₀₀ (mS/cm) | ~3.4 | ~14 | **×4** | AIMD+NE |
| 침투 전이 F* (eV) | 0.20 | 0.17 | ↓ (~15%, Ea와 정합) | Li-density PMF |
| 결합(ELF/Bader/CDD) | 이온 Li/공유 PS₄ | **동일** | — | 대조군 |
| **B0 bulk (GPa)** | 26.2 | 21.7 | **−17%** | EOS (vacancy 연화) |
| C44 shear (GPa) | 8.0 | 13.7 | +71% | disorder |
| E_VRH relaxed (GPa) | 22.1 | 27.7 | **+25%** | 탄성 (disorder) |
| 밴드갭 (eV) | 2.066 | 2.099 | ~동일 | eigenvalue |
| VBM | S 3p | S 3p | 동일 | PDOS |
| 산화 onset (V) | 2.14 | 2.14 | **동일** | grand-potential |
| 양극 반응성 @4.3V | −1.54 | −1.35 | Cl-rich↓ | interface v2 |

---

## 3. 증명됨 vs 대기
**증명됨 (다중 독립 증거):**
- σ↑ 이중 메커니즘 (AIMD×BVSE×Voronoi×percolation, 정량 닫힘).
- 결합 불변 (ELF×Bader×CDD).
- 강성↑ + vacancy paradox 해결 (relaxed vs clamped, EOS 교차검증).
- 산화 onset 동일 + S²⁻-limited (grand-potential + PDOS).
- 양극 반응성 Cl-rich 우위 (interface v2, 전압분해).

**대기 (HPC):**
- **ε∞ (격자 분극률, Kraft 메커니즘)** — epsilon.x 입력 준비됨. "분극률↑→연한 격자→Ea↓"를 우리 DFT로 직접 연결 → [B]를 보강할 마지막 축.
- modelc MP-호환 DFT 에너지 (interface reactivity 정밀화).

---

## 4. 슬라이드 매핑
- S1–2: 동기·문헌표 / S3: 시스템 설계 / **S4–7: 이온전도도([B][C] + percolation·이중메커니즘 슬라이드)**
- S10: 기계([D]) / S15–16: ELF·Bader([C]) / S18: 전자구조([E])
- 산화 섹션: ESW staircase + interface v2([F]) / PDOS(free S²⁻)
- 신규(우리 기여): percolation, 이중메커니즘 분해, CDD 비교, PDOS site, interface v2, ε∞(대기)

## 5. 한 줄 결론 (발표 마무리)
> "Cl enrichment는 결합을 바꾸지 않고 **공공+무질서**만으로 σ(×4)·강성(+25%)을 올리며, 내재 산화창(S²⁻-limited, 2.14 V)은 보존하고 양극 열역학 반응성은 낮춘다. 남는 단점은 kinetic/interfacial(전자전도 아님 — 갭 동일; 이온전도·CEI 후보)이라 코팅/계면설계로 다룰 영역이다."
