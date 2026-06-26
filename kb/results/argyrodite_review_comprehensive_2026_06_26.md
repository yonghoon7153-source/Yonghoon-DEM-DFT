# Lithium Argyrodite 황화물 고체전해질: 구조–수송–안정성–계면–기계의 통합 리뷰
### 그리고 우리 first-principles/MLIP 프로그램의 위치와 적용 (2026-06-26)

> **범위.** 본 리뷰는 2026-06 세션에 litdb로 정밀 정리한 28편(실험·이론·방법론, `litdb/papers/`)을 **6개 과학 축**으로 종합하고, 우리 그룹(한양대 argyrodite DFT)의 grand-potential ESW·BVSE·탄성·interface_reactivity·47-도펀트 UMA cascade 결과가 각 축에서 어디에 서는지, 무엇이 외부에서 검증되고 무엇이 우리 고유 기여인지를 *정직하게* 평가한다. 인용은 `[저자연도]`, DOI는 §12. 모재 약칭: **comp1 = Li₆PS₅Cl**, **modelc = Li₅.₄PS₄.₄Cl₁.₆**(Cl-rich).

> **핵심 한 문장.** *황(S²⁻)이 argyrodite의 산화 한계·이온 수송 병목·전단 취성을 동시에 지배한다. 황 backbone 자체는 치환으로 못 바꾸며, 실효 레버는 (i) 음이온 무질서/운반자(→σ), (ii) 계면 passivation 산물의 전자절연성(→안정), (iii) 격자 이완(→기계)이다.* 이 명제는 본 리뷰 전반에서 외부 문헌과 우리 계산이 *수렴*한다.

---

## 1. 서론 — 왜 argyrodite, 왜 지금
Li₆PS₅X(X=Cl,Br,I) argyrodite는 실온 이온전도도 10⁻³ S/cm급(액체 전해질 LiPF₆ 수준)과 냉간가압 성형성으로 황화물 ASSB의 주력 전해질이 되었다[Rao11, Bai20]. 그러나 (1) 좁은 본질 산화창(S²⁻ 한계), (2) Li 금속·고전압 양극과의 계면 분해, (3) 전단 취성이 상용화를 가로막는다. 지난 15년의 연구는 이 셋을 **무질서·도핑·코팅·물질군 교체**로 공략해 왔고, 동시에 first-principles(grand-potential ESW, NEB/AIMD, 탄성 텐서, 계면 반응)와 MLIP가 *왜* 그러한지를 분자 수준에서 밝혀왔다. 본 리뷰는 그 두 흐름을 한 틀로 묶는다.

Bai 등[Bai20]의 argyrodite 전용 리뷰가 구조·튜닝·합성·계면·대기안정·셀의 6토픽 field-map을 제시했고, Rupp 그룹[Kim21]은 oxide–sulfide 계면의 광역 비교를 주었다. 두 리뷰 이후 5년간 (i) 다중치환(Cu/Sn/Sb+anion), (ii) S-pin 산화 명제의 정량화[Banik22], (iii) percolation 수송 이론[Ishikawa25], (iv) operando 밴드구조[Hikima22], (v) vacancy-paradox 기계 판정[Torii25], (vi) 5V급 물질군 교체[Son25]가 더해졌다. 본 리뷰는 이 신규 결과들을 우리 계산과 정렬한다.

---

## 2. 결정구조와 Li⁺ 수송 메커니즘

### 2.1 골격과 음이온 무질서
입방 F-43m argyrodite는 PS₄³⁻ 사면체가 만드는 골격에 X⁻(4a, 팔면체)와 free S²⁻(4d)가 배치되고 Li⁺가 24g/48h cage 자리를 점유한다. 핵심 디스크립터는 **4a/4d 음이온 자리 무질서(S²⁻↔X⁻ site-mixing)**다. Bai[Bai20]와 Rao[Rao11]가 정리하듯, X=Cl/Br에서는 이온반경이 S²⁻에 가까워 무질서가 활성화되어 inter-cage 장벽을 낮추고 superionic σ를 낳지만, X=I는 반경이 과대(≈2.20 Å)해 무질서가 소멸하고 σ가 3–4 자릿수 급락한다(Cl 1.9 ≈ Br 6.8 ≫ I 4.6×10⁻⁴ mS/cm)[Rao11].

### 2.2 세 가지 점프와 inter-cage 율속
Li⁺ 수송은 위계적 세 점프로 분해된다[Rao11, Bai20, Liang25]: **doublet(48h–48h 국소)**, **intra-cage(한 cage 내 hexagon, Ea 0.15–0.18 eV, 빠름·non-limiting)**, **inter-cage(cage 사이 interstitial 통과, Ea 0.27–0.35 eV)**. 거시(dc) 전도도를 율속하는 것은 **inter-cage 점프**이며, 이는 본 리뷰가 다루는 세 독립 계열의 결론이 일치하는 지점이다(§2.3). Rao의 bond-valence(BVSE) energy landscape[Rao11]가 이 위계를 처음 정량화했고, 이는 우리 cascade의 `migration_volume_fraction`(BVSE 병목 부피) 디스크립터의 직접적 방법론 출처다.

### 2.3 거시 σ의 percolation·hopping 이론
무질서 고체에서 *왜* inter-cage 연결성이 σ를 지배하는가에 대한 이론적 토대가 두 편으로 확립된다.
- **Site percolation [Ishikawa25].** 무작위 치환 결정의 운반이온 농도가 FCC 부격자 site-percolation 임계 **pc≈0.2**를 넘는 순간 σ가 *문턱형*으로 급등한다. 전도는 단일이온 hop이 아니라 침투 클러스터 위의 **cooperative knock-on(연쇄 밀어내기)**이며, 증거로 σ가 Nernst–Einstein σ_NE를 ~2 자릿수 상회한다. 침투 클러스터에 속한 이온만 mobile하다.
- **Hopping(random-barrier) [Dyre04].** dc 활성화에너지는 *침투 클러스터 위에서 반드시 넘어야 하는 최대 병목 장벽*과 같다. 역설적으로 **장벽 분포가 *넓을* 때만** percolation이 단일 병목을 골라 Arrhenius dc가 성립한다.

두 이론의 공통 함의: **dopant가 σ를 떨구는 모드는 (i) 병목 *장벽 높이*↑(Ea-blocking)와 (ii) percolation *경로/창* 제거(connectivity-blocking)로 구분된다.** 이는 우리 cascade 해석에 결정적이다(§3.4, §10).

### 2.4 준층상 변이형 [Liang25]
Liang 등은 입방 argyrodite의 4a/4c 자리에 50% 무질서를 강제하면 공간군이 내려가 **S층–halide-cage–halide층–S-cage가 번갈아 쌓인 준층상(P2mm) 음이온 골격**이 됨을 보였다. 4c-halide의 약결합(특히 Cl: Mayer 결합차수 ≤0.5×S)과 4a-S의 고활성이 **비등방 inter-LAYER 전도**(σ_up/σ_down 최대 2.07)를 낳고, NEB(0.12 eV)와 AIMD-Arrhenius(0.088 eV)가 일치한다. 이는 anion-site 메커니즘을 **Mayer 결합차수로 정량**한 평행본으로, inter-cage 율속의 *네 번째 독립 근거*(AIMD 궤적+NEB)다. **주의: 준층상(4a/4c)은 우리 입방(4a/4d)과 *구조 분지가 다르다* — "inter-layer"를 우리 "inter-cage"와 등치하면 안 된다.**

### 2.5 우리 위치(§2)
우리 AIMD(comp1 Ea 0.253, modelc 0.224 eV; σ_NE ~3.35 mS/cm)와 BVSE 디스크립터는 위 inter-cage·무질서·percolation 서사의 *계산적 구현*이다. Rao의 실측 σ(comp1) **1.9 mS/cm**는 우리 AIMD의 외부 실측 anchor이며, 우리가 같은 10⁻³ 차수임을 확인하되 UMA-MLIP가 3–5× 과대(D* overshoot)임을 정량한다. **수치 직접 등치 금지** — σ 절대값은 방법(UMA/AIMD/BVSE)·외삽 온도마다 갈린다.

---

## 3. 조성 튜닝과 도핑

### 3.1 Cl-rich(할라이드 증량)
Cl/S 비를 올린 modelc(Li₅.₄PS₄.₄Cl₁.₆)는 Li 공공+무질서로 σ를 올린다(Bai 정리: Cl1.5 ~10 mS/cm[Bai20]). Gil-González[GG22]는 Cl-rich가 기계 구속하 산화창을 넓힘을, Zuo[Zuo22]는 양극 계면 거동 개선을 보였다(§4, §5). 우리는 comp1→modelc를 grand-potential·탄성·AIMD 4축에서 비교하는 baseline으로 삼는다.

### 3.2 Aliovalent 양이온 치환
Si/Ge(→P 자리)·Al/Y/Ca/RE(→Li 자리)는 lattice·무질서·운반자를 바꿔 σ를 조절한다[Bai20]. 우리 47-도펀트 cascade는 이 자리 선호(고가전자→P_4b, 3가/2가→Li-site, Hf/Zr amphoteric)를 문헌과 일치하게 재현하며, *동시에* 산화창·Li이동도·탄성을 스크린한다.

### 3.3 다중/공도핑 (양이온+음이온)
세 편이 같은 전략을 보인다: **Li 2025 CuBr₂(Cu²⁺+Br⁻)**[Li25], **Ma 2024 Sn⁴⁺/Sb⁵⁺/I⁻**[Ma24], **Taklu 2021 CuCl**[Taklu21]. 공통 결과는 σ·Li호환·대기안정의 *동시* 개선이다. 대표 수치(Li25): σ 3.4→5.2 mS/cm, Ea 0.295→0.239, σ_e 1.02×10⁻⁸→3.35×10⁻⁹ S/cm, gap 1.82→2.41 eV, CCD 0.6→1.9 mA/cm². 대기안정 기전은 **HSAB**(soft-acid Cu/Sn/Sb가 soft-base S²⁻와 강결합 → PS₄ 가수분해 저항). 이는 우리 **O-도핑의 P–O bonding-lock**(ICOHP −8.43, +41% vs P–S)과 *같은 원리*(강한 음이온-host 결합 → 분해 저항)이되 *다른 화학*이다.

### 3.4 전도도 레버의 본질: 무질서·운반자, *할라이드 종류가 아니다*
Rao[Rao25]는 동일 X/Cl 비에서 Cl/Br/I의 σ가 거의 같음을 보이고, Liang[Liang25]은 σ↔Mayer-균일성 상관을 보인다. 즉 σ를 올리는 것은 *어느 할라이드냐*가 아니라 *총량·비율·무질서·채널 부피*다 — 이는 우리 comp1→modelc(Cl 함량 축)와 위 다중치환(다른 도펀트 축)이 **같은 물리**임을 뜻한다. **percolation 언어로**: 도핑은 운반망의 site 농도/병목 창을 바꿔 σ를 *문턱형*으로 움직인다(§2.3).

---

## 4. 산화 및 전기화학 안정성 (★ 우리 핵심축)

### 4.1 황-고정(S-pin) 산화 한계 [Banik22] — 외부 정답지
Banik·**Yifei Mo**·**Wolfgang Zeier**는 "치환이 argyrodite 산화 안정성을 바꾸는가?"에 **"거의 못 바꾼다"**로 답한다. 가전자대 끝(VBM)이 **free S²⁻ + PS₄³⁻의 비결합(non-bonding) S 3p**로 구성되므로, S가 조성에 있는 한 **S²⁻→폴리설파이드/S 산화가 onset을 고정(pin)**하고, 양이온/음이온 치환은 gap(전도대 위치)만 바꿀 뿐 VBM=onset은 못 옮긴다(*"Sulfur is the Achilles' heel"*). 결론: 단순 치환으론 고전압 못 가며 **코팅 또는 타 물질군이 필요**하다. **이 논문의 결정적 의의**: 교신 Mo가 *우리 grand-potential 방법(Mo–Ong–Ceder 2012)의 원저자*이므로, 우리 결론(comp1=modelc onset 동일, cascade 47개 대부분 S²⁻-pin)을 **방법의 본가가 독립 발표**한 셈이다. Banik의 COHP(VBM=비결합 S 3p, P–S 결합은 훨씬 깊음)는 우리 ICOHP/ELF 해석을 외부 확증한다.

### 4.2 Grand-potential vs 밴드엣지 — 두 종류의 "창"
산화창에는 두 정의가 있다: **밴드엣지 창**(VBM/CBM, UPS/HAXPES 관측량)과 **분해창**(grand-potential phase-stability, Mo/Ong/Ceder). 밴드엣지 창은 분해창을 **2–3× 과대**평가한다(상한). 우리 `oxidation_stability_VBM_vs_grandpotential_report`가 이를 분리했고, Banik이 같은 분리를 명시한다(Fig 1b). 우리 자체 증거: comp1/modelc는 **VBM이 달라도 onset이 동일(2.14 V, S²⁻-limited)** → UPS-VBM 단독을 "산화창"으로 읽으면 틀린다. (방법론 계보: §8 참조.)

### 4.3 Cl-rich 산화의 4축 — 반드시 명명
"Cl-rich가 산화에 좋은가/나쁜가"는 *축을 명명하지 않으면 모순*이다. 네 축으로 정리된다:
| 축 | 결론 | 근거 |
|---|---|---|
| ① intrinsic onset (0 GPa) | **무승부** (둘 다 ~2.14–2.26 V, S²⁻-limited) | 우리 grand-potential · [Banik22] |
| ② 기계 구속 창 (K_eff 10–20 GPa) | **Cl-rich 승** (Cl-product 고몰부피 strain이 창 확장; LPSCl1.5 0.80–4.30 V) | [GG22] |
| ③ 양극 cycling 계면 | **Cl-rich 승** (gas diversion: 고체 sulfate↓·기체 SO₂↑ → 얇은 CEI, R_cat 13.2→8.9) | [Zuo22] |
| ④ calendar/대기 | Cl-rich 다소 불리 (가수분해; 우리 0K hull 밖) | [Bai20] |
이 4축은 우리 Paper#1 "전도도 vs 안정성" 서사의 골격이다. 분해 stoichiometry는 우리 grand-potential(comp1: Li₆PS₅Cl→Li₃PS₄+LiCl+S+2Li)이 [Zuo22] Eq1·[Banik22]와 정확히 일치한다.

### 4.4 5-볼트급: 물질군 천장 [Son25] — 외부 캡스톤
Son 등(Nat. Energy 2025)은 5V급 양극(LNMO 4.7V·LCMO 5.3V)을 ASSB에서 쓰려면 양극에 닿는 물질이 고전압 산화안정해야 하나 기존 후보가 모두 부족함을 *수치로* 명시한다: **황화물 LPSCl <2.5 V**, 할라이드 Li₃YCl₆ 3.7V·Zr-oxychloride ~4.1V(~4.3V 분해), 산화물코팅 LiNbO₃ 3.86V(그 위 O방출→절연 Mn₃O₄). 해법은 코팅·조성튜닝이 아니라 **물질군 교체** — 불소계 SE **LiCl–4Li₂TiF₆**(σ 1.7×10⁻⁵ S/cm, 산화안정 >6.7 V)로 LNMO 표면 차폐(130 mAh/g, 2C 500cyc 75.2%, 35.3 mAh/cm² 후막). **우리와의 정량 일치(★)**: 본문 "LPSCl <2.5 V" = 우리 grand-potential **2.256 V(S²⁻-limited)**. Banik의 *진단*("왜 못 가나")과 Son의 *처방*("그래서 무엇이 필요한가")이 우리 onset을 사이에 두고 한 쌍을 이룬다.

### 4.5 우리 cascade의 예외와 backbone
우리 47-도펀트 ESW는 19개가 정확히 S-limit 2.14 V에 고정(Banik 성립)되고, **6개가 onset을 올린다 — 전부 trivalent(M³⁺) 산화물**: Sc₂O₃·Cr₂O₃·In₂O₃·Ga₂O₃ **2.356 V**, B₂O₃ **2.317**, Y₂O₃ **2.282**(+0.14–0.22 V). 이들은 헤테로밸런트 산화물이 *새 산화-한정 반응*을 도입한 결과로, Banik의 iso-structural 교환(P→Si/Ge, Cl→I)이 접근 못 하는 경로다. **단 S-backbone 산화는 어느 경우도 못 늦춘다** → Banik의 S-pin은 backbone 수준에서 robust. (figure: `cascade_oxidation_vs_banik.png`.) Nd₂O₃ 도핑은 onset을 1.92 V로 *내리지만*(trace Nd–S 산화) bulk 폴리설파이드는 2.30 V이므로 충돌이 아니며, Nd의 실효 이점은 onset이 아니라 **wide-gap passivation 산물**(NdPO₄/Li₃PO₄/Li₂O)이다(§5).

---

## 5. 양극 계면 공학

### 5.1 분해 화학과 산물
고전압에서 황화물 SE는 양극과 반응해 **Co₉S₈ + Li₃PO₄ + Li₂S + LiCl + Li₂SO₄**(우리 interface_reactivity, vs LiCoO₂; O는 cathode서 옴)를 만들고, 이는 [Zuo22]의 ToF-SIMS 분해종(phosphate·sulfate·폴리설파이드·LiCl)과 1:1 대응한다. 산물 XPS는 우리 `xps_reference_sei.csv` anchor(Li₃PO₄ P 2p 133.3·Li₂SO₄ S 2p 168.0·LiCl Cl 2p 198.6·Li₂S 160.2 eV)가 BE 수준에서 커버한다. *세 도구(grand-potential 분해식 + interface_reactivity 산물 + XPS BE)가 같은 계면 화학을 지목* = 독립 교차검증.

### 5.2 세 가지 레버 (우리 그룹 3부작 + cascade)
양극 계면을 관리하는 레버가 셋으로 정리된다:
- **[Cha24] 할라이드 코팅(차단).** NCM에 Li₂ZrCl₆ 등 할라이드 SE를 8–10 nm 코팅. "**dual compatibility**": 코팅이 NCM(산화물)·LPSCl(황화물) *양쪽*과 부반응을 안 해야 하며, LIC(In)/LYC(Y)/LZC(Zr) 중 **Zr⁴⁺만** 만족(계면저항 74.4→20.1 Ω·cm², 100cyc 91.2%).
- **[Kang25] SE 코팅(기생반응 균일화).** LPSCl 자체 코팅으로 기생반응을 *균일화*해 보호.
- **우리 cascade SE 도핑(절연 CEI).** 도핑 산물의 wide-gap 절연성으로 전자누설 차단.
지붕은 [Kang26] electrochemo-mechanical 통합 리뷰. **★ 전압대 절제(Son25 반영)**: 우리 코팅 3부작은 **4V급 계면관리**로 위치시켜야 한다 — 할라이드조차 ~4V에서 분해하므로 **5V급(LNMO)은 물질군 교체(불소계) 영역**이다. 우리 코팅 결론을 5V로 과확장하면 오류다.

### 5.3 "레버 = interphase/형상, bulk σ가 아니다"
[Cha24]에서 σ가 가장 높은 LIC가 수명 꼴찌(σ 1.12 mS/cm, 100cyc 80.8% < bare 83.1%)다. 이 σ-역상관은 [KimICCF](공동충전 σ)·[KimCA](도전재 형상→σ_e)·[Li25](σ_e 실측)와 합쳐 **"수명 레버 = 계면/형상, bulk σ 무관"의 4중 증거**를 이룬다.

### 5.4 계산 계면 스크리닝 [Sundar25]
Sundar(Argonne)는 LPSCl에 바이너리 산화물 ALD 코팅 후보를 DFT 2단계로 스크린해 **분해산물의 σ_ion/σ_e가 코팅 자체 안정성보다 예측력 있는 지표**임을 보였다(MgO champion). 이들의 pymatgen **InterfaceReactions**는 우리 `interface_reactivity`/`GrandPotentialInterfacialReactivity`와 *동일 알고리즘*(분야 표준이라는 외부 확증; 우리는 전압분해까지 확장 = 우위). 분해산물 gap 순서(Li₂S < LiCl)가 우리 `sei_products.json`(LiCl 6.65 ≫ Li₂S 3.90)을 재확인.

---

## 6. 음극 계면과 Li 금속
황화물 SE는 ~1.7 V(vs Li)에서 환원 분해하며, 전자전도 σ_e가 dendrite를 좌우한다(σ_e↓→CCD↑; [Li25] Fig 3b 직접 그래프). Cl-rich는 음극서 **LiCl passivation**을 형성하고([Lu25]), [Liu22]는 Cl 결정화/계면 거동을 추적한다. 우리 Nd cascade의 **wide-gap 전자절연 passivation**(NdPO₄ 5.55·Li₃PO₄ 5.73·Li₂O 5.24 eV; vs 도전성 Li₃P 0.70)이 같은 논리의 *능동적 O-derived 구현*이다(문헌은 native 분해/코팅 — 메커니즘 위치가 다름).

---

## 7. 기계 물성과 chemo-mechanics

### 7.1 Vacancy paradox와 외부 판정 [Torii25]
황화물 argyrodite의 탄성에는 **clamped-ion(framework 동결) vs relaxed-ion(이온 이완)** 차이가 ~2×에 이르는 "vacancy paradox"가 있다(우리 comp1: clamped E 52.31 vs relaxed 22.06 GPa). Torii(Osaka, Sakuda/Hayashi)의 독립 full-DFT(PBE-D3, relaxed-ion)가 **E=27.4·G=10.0·C₁₁=47.4·C₄₄=10.4 GPa·ν=0.37·Zener A=1.09**를 보고하며, 이는 명백히 우리 **relaxed-ion 영역**(22/8)에 있고 clamped(52/20)의 ~2× 아래다 → **"clamped는 frozen-framework baseline, relaxed가 물리적"이 외부 독립 DFT로 확증**(method-artifact 아닌 real adjudication). 정직한 단서: Torii가 우리 relaxed보다 +23–39% 높은 것은 **D3 계통 강성**(C₁₂ +39%)이지 clamped/relaxed 2×와는 스케일이 다르므로 판정은 robust.

### 7.2 B0와 이방성
격자상수 일치(Torii 10.04 ≈ 우리 10.055 Å)로 동물질·동부피가 확정된다. 다만 **bulk modulus 절대값은 정의차**: Torii VRH B=34.7 vs 우리 BM-EOS B0=26.23 GPa는 (i) VRH 텐서평균 ≠ BM 곡률, (ii) D3 강성 때문이며, functional·정의를 맞추면 우리 relaxed **B_VRH 25.51 ≈ EOS 26.23(3% 이내)**이다. *직접 등치 금지.* 이방성: Torii의 vacancy-free A=1.09는 우리 control(1.07–1.14)을 외부 고정하고, 우리는 여기에 **modelc(vacancy+Cl-disorder) A=1.44**를 더해 "disorder→이방성"을 우리 고유 기여로 보인다.

### 7.3 전단 취성의 원자 기구
Torii는 인장에는 strain 0.2까지 견디나 **전단 ε=0.7%에서 파괴**하며, 그 원자 기구가 **Cl이 Li 쪽으로 끌려가 Li₄Cl 클러스터 형성 → PS₄ 황 음전하 약화 → layered gap**임을 보인다. 이는 우리가 *못 설명한* 낮은 C₄₄/G의 *왜*를 채우며([Kang26] chemo-mechanical 지붕과 연결), "우리가 보였다"가 아니라 Torii 인용으로 처리해야 한다. (참고 표: oxide E 150–200 vs sulfide LPSX 22.1–30.0 GPa[Bai20].)

---

## 8. 전자구조와 밴드 정렬

### 8.1 UPS 방법론 [Whitten23]
UPS(He I 21.22/He II 40.8 eV)는 가전자대·일함수 Φ·이온화에너지 IE를 잰다. **Φ = hν − SECO**(2차전자컷오프, 시료 음 바이어스 필수), **VBM/IE = 가전자대 onset 선형외삽**. 절연체는 대전 때문에 직접 못 하고 도전기판+박막두께 시리즈로 진단. UPS는 우리가 계산하는 산화관련 VBM/IE를 *어떻게 측정하나*의 방법 원전이며, 진공준위 절대기준을 주어 우리 slab-IP VBM 보정의 외부 앵커가 된다.

### 8.2 정적·operando 밴드엣지 [Banik22, Hikima22]
[Banik22]는 HAXPES로 **치환 무관 VBM 불변**(정적)을 보이고, [Hikima22]는 박막 ASSB operando HAXPES로 **충전 중 Fermi level 1.1 eV 하강 → n→p 전이 → Schottky/inversion → 고전압 충전 차단**(동적)을 보인다. 따라서 **[Whitten]UPS 기법 → [Banik]정적 VBM 불변 → [Hikima]operando VBM 운동**의 3단 계보가 우리 정적 0K VBM의 실험 카운터파트를 완성한다. **★ 수치 앵커**: [Hikima]의 **Li₃PO₄ Eg = 5.77 eV(실측 UPS) ≈ 우리 sei_products.json 5.73 eV(MP DFT)**, Δ0.04 — wide-gap 절연 산물의 외부 독립 실측. **단 [Hikima]는 oxide SE(LASGTP)·Li₂MnO₃이고 DFT 직접계산이 없어** 절대 VBM/gap을 우리 황화물과 1:1 비교 금지(프레임·방법·operando만 연결). 밴드엣지 n→p 전이는 *양극 산화*를 밴드로 본 것이지 *SE 분해 onset*이 아니다(§4.2 규율 재확인).

---

## 9. 계산 방법론

- **DFT-for-batteries [He19].** 전압/형성에너지/convex hull, NEB/AIMD 확산, DOS/gap/band alignment, 탄성/EOS의 표준 절차와 함정(PBE gap 과소+U/hybrid, k-point, magnetism, dispersion)을 정리. 우리 파이프라인(electronic.json·oxidation grand-potential·eos/elastic·li_transport)이 *표준 battery-DFT 관행을 따른다*는 인용처. **단 grand-potential ESW는 He19가 아니라 Mo–Ong–Ceder 2012가 원전.**
- **MLIP 대리 [Choi25].** SevenNet(E(3)-equivariant)으로 work-of-adhesion을 **비평형 SMD + Jarzynski + PMF**(rigid 분리가 아님)로 계산 → 우리 rigid-분리 W_ad의 100–1000× 과대(dangling-bond 인공일) 처방. 동급 MLIP이 bulk modulus·계면에너지를 DFT 5% 이내로 재현 → 우리 Nd₂O₃ B0(UMA 18.9 vs DFT 19.9 ≈5%)가 *MLIP 계열의 일반 정확도*임을 보이는 외부 앵커. **단 우리 UMA는 vacuum 민감(60 Å→10× 과대)이라 SMD는 OOD 위험.**
- **BVSE / grand-potential / interface_reactivity.** §2·§4·§5에서 본 대로 각각 [Rao11]·[Mo2012]·[Sundar25]가 방법 출처/표준성을 준다.

---

## 10. 우리 프로그램의 위치와 고유 기여

**우리가 외부에서 검증받은 것:**
1. 산화 결론(S-pin, comp1=modelc 2.14 V) ← [Banik22] (Mo+Zeier, 우리 방법 본가).
2. vacancy paradox(relaxed-ion이 물리적) ← [Torii25] full-DFT.
3. comp1 σ 차수 ← [Rao11] 실측 1.9 mS/cm.
4. SEI gap 순서·Li₃PO₄ 5.7 eV ← [Sundar25]·[Hikima22].
5. interface_reactivity 도구 표준성 ← [Sundar25].
6. inter-cage 율속·anion-site ← [Rao11]/[Liang25]/[Ishikawa25]/[Dyre04].
7. 5V "황화물 <2.5V" ↔ 우리 2.256 V ← [Son25].

**우리 고유 기여(문헌이 아직 못 한 것):**
- **47-도펀트 × 4축(안정·산화·이동·기계) *동시* 스크린**(단일 논문 부재).
- **grand-potential 전압분해**(밴드엣지 상한 너머의 실제 분해 onset)와 **Cl-rich 4축 정명**.
- **onset 옮기는 예외 도펀트**(B₂O₃ 등 M³⁺ 산화물, ≤0.2 V)의 식별.
- **Nd passivation 산물**(NdPO₄/NdCl₃ wide-gap)의 능동적 메커니즘.
- **vacancy→이방성**(modelc A=1.44; Torii가 못 본 vacancy 효과).
- **dual-metal 부격자 co-doping**·**oxyfluoride** novelty(synergy 가설).
- **dual-x 농도 regime**(Sc₂O₃ blocking 0.75@x0.25 → 0.25@x0.0625): 저농도 aliovalent→Li vacancy→σ 보존을 직접 확인(percolation threshold 위/아래 전환의 우리계 대응).

**blocking 2모드 통합 해석(§2.3 적용):** 우리 Nd σ-drop(σ300 0.52×, D 0.62×, **Ea 0.224≈불변**, prefactor 0.65× 지배)은 [Dyre04]/[Ishikawa25] 언어로 **connectivity/prefactor-blocking**(병목 *높이*가 아니라 *경로/창* 제거)이다. 단 우리 Nd는 *완만 감소*(망 유지)지 pc 붕괴가 아니다 — "Nd가 percolation 무너뜨림"은 over-claim.

---

## 11. 미해결 과제와 향후 방향
1. **기체 chempot 포함 계면 분해**(Zuo의 gas diversion, Son의 5V O-release 정량) — 우리 0K closed-hull 밖.
2. **무질서 E_above_hull**(DSC/TGA metastability) — 단일 ordered config 한계.
3. **Zr·Ti·F 포함 hull 확장** — [Cha25] dual-compatibility([LIC/LYC/LZC]×[NCM,LPSCl] 6계면)·[Son25] 불소계 5V를 우리 grand-potential로 재현하려면 필수.
4. **slab-IP 절대 VBM** ↔ UPS/HAXPES 정렬([Whitten]/[Hikima]).
5. **W_ad SMD+PMF**([Choi25]) 도입으로 절대 접착 스케일 신뢰.
6. **준층상 비등방**([Liang25])을 우리 등방 입방에서 어떻게/왜 못 재현하는지.

---

## 12. 적용 가능 항목 (우리 작업에 바로) — 우선순위
**[1순위·실행가치 높음]**
- **Zr/Ti-F hull 추가 → interface_reactivity 6계면**(Cha) + 불소계 5V(Son): *우리 그룹·외부 캡스톤 실험을 우리 DFT가 재현*.
- **B₂O₃ 등 예외 M³⁺ 산화물 staircase**(gabia `esw_cascade_batch`): "어떤 새 반응이 onset +0.22V 올리나" 명명 → Banik 차별화 정량.
- **(진행 중) 주기적 core-hole XPS**(Li₃PO₄ vs Li₃PS₄ P 1s): 클러스터가 못 잡은 +1.6 eV 시프트를 격자로 재현 → SEI XPS anchor를 *계산*으로.

**[2순위·방법 업그레이드]**
- W_ad에 SMD+PMF(Choi); slab-IP VBM ↔ UPS 절대정렬(Whitten); blocking을 percolation/hopping 어휘로 서술(Ishikawa/Dyre).
- LiBr/LiI를 sei_products.json에 *우리 MP 쿼리값으로* 추가(Li25 5.07/Rao) — halide-SEI-gap 시리즈 완성.

**[3순위·서사/deck]**
- 슬라이드: cathode 3-레버(4V급) + 5V 물질군 교체(Son) / "lever=interphase, not σ" 4중증거 / 이론 백본(blocking 2모드, Nd=connectivity) / S-pin 산화 + 예외 6 M³⁺ / vacancy paradox 외부 판정 / UPS→Banik→Hikima 밴드 3단 계보.

**전 항목 정직 가드레일:** 외부 절대값(σ/Ea/gap/B0/W_ad/VBM) ↔ 우리 값 *직접 등치 금지*(functional·정의·무질서·MLIP-scale 차이); 축 명명 필수(Cl-rich 4축·코팅≠도핑·4V급≠5V·밴드엣지≠분해onset·inter-layer≠inter-cage·analogy≠검증); 우리 고유 기여 명확화(§10).

---

## 참고문헌 (DOI)
- **[Rao11]** Rao & Adams, *Phys. Status Solidi A* 208, 1804 (2011). 10.1002/pssa.201001117
- **[Rao25]** Rao et al., *J. Mater. Chem. C* 13, 10733 (2025). 10.1039/d5tc00529a
- **[Liang25]** Liang et al. (Bolong Huang), *Small* 21, 2502078 (2025). 10.1002/smll.202502078
- **[Ishikawa25]** Ishikawa, Takae, Kurita, arXiv:2505.00362 (APS, 2025).
- **[Dyre04]** Dyre & Schrøder, *Rev. Mod. Phys.* 72, 873 (2000) / arXiv cond-mat/0407083.
- **[Li25]** Li et al., *Energy Storage Mater.* 77, 104221 (2025). 10.1016/j.ensm.2025.104221
- **[Ma24]** Ma et al., *J. Mater. Chem. A* (2024, USTB).
- **[Taklu21]** Taklu et al. (CuCl dual-doping, 2021).
- **[Banik22]** Banik, …, Mo, Zeier, "Can substitutions affect the oxidative stability…" (manuscript; DOI n/a).
- **[GG22]** Gil-González et al. (2022) — Cl-constricted ESW.
- **[Zuo22]** Zuo, …, Nazar, Janek, *Angew. Chem. Int. Ed.* 62, e202213228 (2023). 10.1002/anie.202213228
- **[Lu25]** Lu et al. (2025) — Cl-rich anode LiCl.
- **[Son25]** Son et al. (Seo/Nam/Jung), *Nat. Energy* 10, 1334 (2025). 10.1038/s41560-025-01865-y
- **[Cha24]** Cha, …, Jong-Won Lee, *J. Power Sources* 617, 235157 (2024). 10.1016/j.jpowsour.2024.235157
- **[Kang25]** Kang et al. (parasitic reaction benefit, ChemComm/우리 그룹).
- **[Kang26]** Kang et al. (intertwined electrochemo-mechanical review, 우리 그룹).
- **[Sundar25]** Sundar et al. (Zapol/Connell, Argonne), *Adv. Sci.* 12, e13191 (2025). 10.1002/advs.202513191
- **[Torii25]** Torii, …, Sakuda, Hayashi, *J. Phys. Chem. C* 129, 17882 (2025). 10.1021/acs.jpcc.5c05116
- **[Whitten23]** Whitten, *Appl. Surf. Sci. Adv.* 13, 100384 (2023). 10.1016/j.apsadv.2023.100384
- **[Hikima22]** Hikima, …, Kanno, *Commun. Chem.* 5, 52 (2022). 10.1038/s42004-022-00664-w
- **[He19]** He et al., "DFT for Battery Materials," *Energy Environ. Mater.* (2019).
- **[Choi25]** Choi, …, Seungwu Han, *ACS Appl. Electron. Mater.* 7, 11165 (2025). 10.1021/acsaelm.5c02157
- **[Bai20]** Bai et al., *J. Mater. Chem. A* 8, 25663 (2020). 10.1039/d0ta08472g
- **[Kim21]** Rupp 그룹 review (oxide–sulfide 계면). · **[KimICCF]/[KimCA]** 우리 그룹 동반 실험 2편.

> 개별 paper-level digest(각 150–320줄): `litdb/papers/*.md` · 1줄 인덱스: `kb/results/litdb_session_map_2026_06_26.md` · 산화 예외 figure: `docs/figures/cascade/cascade_oxidation_vs_banik.png`.
