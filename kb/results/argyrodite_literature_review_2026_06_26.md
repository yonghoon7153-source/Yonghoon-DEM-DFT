# Argyrodite 황화물 고체전해질 — 문헌 종합 리뷰 + 우리 DFT 프로그램 적용 맵 (2026-06-26)

이번 세션에 litdb로 정리한 ~24편을 **과학 섹션별로 분류**하고, 우리(한양대 argyrodite DFT) 프로그램이 각 축에서 어디에 서는지 + **무엇을 적용할 수 있는지**를 종합한다. 개별 digest: `litdb/papers/`, 1줄 인덱스: `kb/results/litdb_session_map_2026_06_26.md`.
태그: **[우리]** = 우리 그룹 · **[외]** = 외부 · **[이론]/[방법]** = theory/methods.

---

## 0. Field map — argyrodite Li₆PS₅X 연구의 6축
황화물 argyrodite SE 연구는 6축으로 정리된다: **(1) 구조·Li수송 · (2) 도핑·전도도 · (3) 산화/전기화학창 · (4) 양극 계면 · (5) 음극 계면 · (6) 기계·전자구조.** 우리 프로그램은 이 6축 *전부*를 DFT(grand-potential ESW · BVSE · elastic · interface_reactivity)+MLIP cascade로 다루며, 이번 문헌이 각 축을 **외부에서 검증/맥락화**해줬다. 핵심: *"S²⁻가 산화·전도·기계를 동시에 지배 — backbone은 못 바꾸고, 레버는 무질서·계면·passivation."*

---

## 1. 구조 & Li⁺ 수송 (intra/inter-cage, percolation, hopping)
**문헌**: Rao 2011[외] (BVSE 원조) · Rao 2025[외] (Cl/Br/I) · Liang 2025[외] (quasi-layered) · Ishikawa 2025[이론] (percolation) · Dyre 2004[이론] (hopping).

- **율속 = inter-cage hop**: Rao 2011이 BVSE로 intra-cage(0.15–0.18 eV, 빠름) → **inter-cage interstitial(0.27–0.35 eV) = dc 율속**을 처음 보임. Ishikawa(percolation pc≈0.2)·Dyre(hopping 병목=dc Ea)가 이론으로 뒷받침: **장거리 σ는 *국소 장벽*이 아니라 *경로 connectivity*가 지배**.
- **σ는 halide 종류보다 총량·채널부피**: Rao(Cl 1.9≈Br 6.8 ≫ I 4.6×10⁻⁴ mS/cm)·우리 comp1→modelc(Ea 0.253→0.224)가 같은 메커니즘(무질서+운반자).
- **우리 위치**: `migration_volume_fraction`(BVSE 병목 부피)·`dopant_blocking_fraction`이 *바로 이 inter-cage 창*을 잰다. Rao 2011 σ=1.9 mS/cm = comp1의 **외부 실측 anchor**(우리 AIMD ~3.35 = 같은 10⁻³ 차수, UMA 3–5× overshoot).

## 2. 도핑 & 전도도 향상 (halide / cation / multi-doping)
**문헌**: Li 2025[외] CuBr₂ · Ma 2024[외] Sn/Sb/I · Taklu 2021[외] CuCl · Rao 2025[외] I → **USTB multi-doping 삼형제 + halide**.

- **공통**: 다중치환(양이온+음이온)이 σ·Li호환·대기안정을 *동시* 개선. Ea↓ 방향이 우리 Cl-rich와 일치(다른 도펀트, 같은 무질서·운반자 물리).
- **soft-acid 안정화**: Cu/Sn/Sb–S 결합(HSAB)이 PS₄ 보호 → 대기안정 = 우리 **O-도핑 P–O bonding-lock**(ICOHP +41%)과 같은 "강한 음이온-host 결합이 분해 저항" 원리(다른 화학).
- **우리 위치/차별**: 우리 cascade는 47-도펀트 *산화물* 위주 + 4축(안정·산화·이동·기계) 동시 스크린. 문헌은 *황화물/할라이드 soft-acid* → **메커니즘 다름, force-fit 금지**. 단 "multi-doping 동시개선"의 외부 실험 평행선.

## 3. 산화 안정성 & 전기화학창 (★ 우리 핵심축)
**문헌**: **Banik 2022[외] (Mo+Zeier)** · GilGonzalez 2022[외] · Zuo 2022[외] · Lu 2025[외].

- **★ S-pin 명제 (Banik = 외부 정답지)**: VBM = 비결합 S 3p → **S가 있는 한 치환은 산화 onset 못 옮긴다**. 교신 Yifei Mo = *우리 grand-potential 방법(Mo-Ong-Ceder 2012) 원저자* → **우리 결론(comp1=modelc 2.14 V, cascade 47개 대부분 S²⁻-pin)을 방법 본가가 독립 발표.** COHP가 우리 ICOHP/ELF 확증.
- **우리 차별 (Banik이 닫은 문 위)**: ① Cl-rich 4축(아래) ② **onset 옮기는 예외 도펀트 = 전부 M³⁺ 산화물**(Sc/Cr/In/Ga₂O₃ 2.356·B₂O₃ 2.317·Y₂O₃ 2.282, +0.14~0.22 V; S-backbone은 여전히 pin) ③ Nd passivation. *(figure: `cascade_oxidation_vs_banik.png`)*
- **Cl-rich 산화 4축 정명** (섞으면 틀림): **①intrinsic onset**(무승부, 2.14V S²⁻) · **②기계구속**(GilGonzalez, Cl-product 고몰부피 strain이 창 확장) · **③양극 cycling**(Zuo, gas diversion으로 얇은 CEI) · **④음극**(Lu, LiCl passivation).

## 4. 양극 계면 (high-voltage)
**문헌**: Cha 2024[우리] dual-halide · Kang 2025[우리] parasitic · Sundar 2025[외] coating · Zuo 2022[외].

- **3-레버**: Cha=할라이드코팅(차단) / Kang25=SE코팅(기생반응 균일화) / 우리 cascade=SE도핑(절연CEI). 지붕 = Kang26 리뷰.
- **"lever = interphase, not σ"**: Cha(σ 1등이 수명 꼴찌)·KimICCF·KimCA·Li2025(σ_e실측) = **4중 증거**.
- **Sundar coating 스크린 = 우리 interface_reactivity와 동일 도구**(pymatgen InterfaceReactions); 분해산물-σ 철학이 우리 sei_products gap 순서(LiCl 6.65≫Li₂S 3.90) 재확인. 우리는 grand-potential 전압분해까지 확장 = 우위.

## 5. 음극 계면 (Li metal / dendrite)
**문헌**: Liu 2022[외] Cl-결정화 · Lu 2025[외] LiCl passivation · Kim 2026[우리] ICCF.

- "전자절연 SEI = dendrite 레버": σ_e↓→CCD↑(Li2025 실측 그래프). 우리 Nd cascade의 wide-gap passivation(NdPO₄/Li₃PO₄/Li₂O)과 같은 논리, 단 우리는 *능동적 O-derived 산물* vs 문헌의 *native 분해/코팅*.

## 6. 기계 물성 & chemo-mechanical
**문헌**: **Torii 2025[외] (★ vacancy paradox 판정)** · Kang 2026[우리] 리뷰(지붕).

- **★ Torii = 우리 vacancy paradox 외부 full-DFT 판정**: relaxed-ion E=27.4/G=10.0 → 우리 relaxed(22/8)에 산다, clamped(52/20)의 2× 아래 → **"clamped는 frozen-framework baseline, relaxed가 물리적"이 확증**. (B0 동물질·절대값은 D3+정의차.)
- **전단취성 원자기구**: Cl→Li₄Cl→layered gap(ε=0.7%) = 우리 낮은 C₄₄/G의 *왜*(우리가 못 설명한 부분, Torii 인용). Kang26 chemo-mechanical 지붕과 연결.

## 7. 전자구조 & band alignment / 방법론
**문헌**: Whitten 2023[방법] UPS · He 2019[방법] DFT-for-batteries · Choi 2025[방법] MLIP adhesion · (#25 operando — 진행).

- **UPS = 산화안정성 valence-side 실측**: VBM/IE = 산화 onset 관측량(단 밴드엣지=상한, 진짜 onset은 grand-potential). 우리 VBM-vs-grandpotential 리포트의 방법 원전.
- **He 2019 = 우리 방법 백본**: band gap·ESW·NEB/AIMD·EOS/elastic이 표준 battery-DFT임을 인용.
- **Choi MLIP W_ad = SMD+PMF**: 우리 rigid-분리 100–1000× 과대의 처방; 동급 MLIP B0 DFT 5%내 = 우리 Nd₂O₃ B0(UMA 18.9 vs DFT 19.9) 신뢰 앵커.

---

## ★★ 8. 우리가 적용할 수 있는 것 — 설명 + LIST

### A. 지금 바로 인용 (외부 검증 확보) — 논문/deck에 박기
1. **Banik 2022 → 산화 결론**: "comp1=modelc onset 2.14 V, 치환 무관(S-pin)"을 **Mo(방법 본가)+Zeier(실험)** 으로 외부 앵커. *우리 차별 = 예외 M³⁺ 산화물 + Nd passivation + 4축.*
2. **Torii 2025 → vacancy paradox**: "clamped 2× 과대, relaxed가 물리적"을 외부 full-DFT로 못박음. deck "paradox" 슬라이드 인용처.
3. **Rao 2011 → σ anchor**: comp1 실측 σ=1.9 mS/cm(우리 AIMD 같은 차수).
4. **Sundar 2025 → 도구 표준성**: 우리 interface_reactivity(InterfaceReactions)가 Argonne도 쓰는 분야 표준.

### B. 방법 채택 (우리 파이프라인 업그레이드)
5. **W_ad에 SMD+PMF 도입**(Choi) — 우리 rigid-분리 과대(45–225 vs 실험 0.2–0.4 J/m²) 해결. cascade wad 우승자 top-3만 UMA-SMD로 교차검증.
6. **slab-IP VBM ↔ UPS 절대정렬**(Whitten) — DFT 절대 VBM 비교불가 문제를 UPS 진공준위 기준으로 앵커(우리 H-목록 "slab IP" 과제와 일치).
7. **percolation/hopping 어휘로 blocking 서술**(Ishikawa/Dyre) — "Nd σ-drop = Ea-blocking 아니라 connectivity-blocking" 정밀 서술(우리 prefactor-dominant 분해와 일치). 단 *완만감소지 pc붕괴 아님*.

### C. 확장 / 다음 계산·실험 (gap 메우기)
8. **B₂O₃ 등 예외 M³⁺ 산화물 staircase**(gabia `esw_cascade_batch`) — "어떤 새 반응이 onset +0.22V 올리나" 명명 → Banik 차별화 정량.
9. **Zr-hull interface_reactivity**(Cha) — LIC/LYC/LZC×{NCM,LPSCl} 6계면 → "왜 Zr⁴⁺만 dual-compatible" 재현 = 우리 그룹 실험을 우리 DFT가 검증.
10. **LiBr·LiI를 sei_products.json에 정식 추가**(Li2025 5.07 / Rao) — halide-SEI-gap 시리즈 완성(현 LiCl 6.65·Li₂O만). *단 우리 MP 쿼리로 동일 functional 값을 뽑아 넣기*(외부값 직접 혼입 금지).
11. **comp1을 PBE-D3로 한 번**(Torii 비교) — Torii +25% 강성이 정말 전부 D3인지 직접 검증(우리 PBE vs Torii PBE-D3 동일 functional 정렬).
12. **dual-doping synergy 실측 후보**(Ma/Li/Taklu) — 우리 cascade synergy_pairs(Ta⊕Gd 등)의 실험 평행선; soft-acid(Cu/Sn/Sb) vs 우리 산화물 경로 비교.

### D. deck/논문 슬라이드 (synthesis, 바로 사용)
13. **cathode 3-레버** (Cha/Kang25/cascade) 한 장.
14. **"lever=interphase, not σ"** 4중 증거 한 장.
15. **이론 백본**: blocking 2모드(Ea vs connectivity), Nd=connectivity 한 장.
16. **S-pin 산화 + 예외 6 M³⁺ 산화물** (`cascade_oxidation_vs_banik.png`).
17. **vacancy paradox 외부 판정** (Torii relaxed vs clamped).

### 정직 가드레일 (전 항목 공통)
- 외부 절대값(σ/gap/Ea/B0/W_ad) ↔ 우리 값 **직접 등치 금지** — functional·정의·무질서·UMA-scale 차이. **방향·순서·메커니즘**만 정렬.
- 축 명명 필수(특히 Cl-rich 산화 4축, 코팅≠도핑, analogy≠검증).
- 우리 *고유* 기여 명확히: 47-도펀트 4축 동시 스크린 · grand-potential 전압분해 · vacancy→이방성 · Nd passivation 산물 · dual-metal 부격자 novelty.

---

## 진행 중 (완료 시 섹션 반영)
- **#26 Liang** (quasi-layered, §1) · **#24 review** (§0 field-map 보강) · **#25 operando band** (§7) · **#27 5V ASSB** (§3·§4).
> 4편 들어오면 본 리뷰 해당 섹션에 1–2줄씩 추가 예정.
