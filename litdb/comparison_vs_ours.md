# 🔬 문헌 ↔ 우리 DFT — 물성축별 분류 + 논문 reference

> 기준값: `our_dft_baseline.md`. **각 주장마다 [출처 논문] 명시.** digest 있는 논문은 `papers/<slug>.md` 링크.
> 사용법: 새 논문 digest 시 해당 축 표에 행 1개 추가(+출처). 산화 Q&A는 맨 아래 §Q&A 로그.

## 📑 Reference key (출처 약칭)
| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |
|---|---|---|---|
| **[Zuo]** | Zuo 2022 Angew — 양극 계면 chlorination | ✅ `papers/zuo2022_chlorination_cathode_interface.md` | exp |
| **[Ke]** | Ke 2025 ESM — MgClO 음극 혼성 도핑 | ✅ `papers/ke2025_orbital_hybridization_mgclo.md` | exp+DFT |
| **[GG]** | Gil-González 2022 ESM — constrained ESW (구속) | ✅ `papers/gilgonzalez2022_synergistic_cl_constricted_esw.md` | DFT+exp |
| [Wu] | Wu 2026 Nano Energy — calendar aging | 📄 db/properties/oxidation_stability.json | exp |
| [Banik] | Banik 2022 ACS AEM — HAXPES VBM=S | ⬜ PDF | exp |
| [Liu] | Liu 2022 AdvFM — Cl 결정화/계면 | ⬜ PDF | exp |
| **[Lu]** | Lu 2025 CEJ — 음극 4d-Cl 자기분해 → LiCl interphase (gap 1.88/LiCl 6.22) | ✅ `papers/lu2025_tailoring_cl_rich_anode_licl.md` | exp+DFT |
| **[Liu23]** | Liu 2023 Angew — MgF₂ 공도핑 electron redistribution (redox-resistible, σ_e 8×↓) ⚠[Liu]≠이것(=Liu 2022 AdvFM) | ✅ `papers/liu2023_electron_redistribution_redox_resistible_mgf2.md` | exp+DFT |
| [Ma] | Ma 2026 J.E.S. — In doping, PBE gap 2.10→2.62 | ⬜ PDF | DFT |
| [Semi] | "When Electrolytes Are Semiconductors" 2026 — HSE06 gap | ⬜ PDF | DFT |
| [Kaur] | Kaur 2016 JES — elastic SQS E22.1/B28.7/G8.1 | ⬜ PDF | DFT |
| [JPCC] | First-Principles Mech&Aniso 2025 — D3 E27.4/B34.7/G10.0 | 📄 Excel | DFT |
| **[Rupp]** | Kim/Balaish/Rupp 2021 AEM — oxide vs sulfide SE + 계면 landscape 리뷰 (63 pp) | ✅ `papers/kim2021_review_oxide_sulfide_se_interfaces.md` | review |
| **[KimICCF]** ⭐우리그룹 | Kim/Cho/Y.M.Lee 2026 CEJ — ICCF(IL cavity filler) → σ 회복 155 % + 음극 in-situ LiF-rich SEI (한양대 Cho + Yonsei Lee) | ✅ `papers/kim2026_iccf_molten_salt_sei_lpscl_sheet.md` | exp(+분자 HOMO/LUMO·GeoDict) |
| **[KimCA]** ⭐우리그룹 | Kim/Y.M.Lee 2025 Battery Energy — SE 코팅 중 도전재(CA) 차원 효과: 0D Super P(나쁨) vs 1D VGCF(좋음, ≈CA無 dense). 양극복합체 σ_e·활성표면적·형상 (Yonsei Lee + DGIST) | ✅ `papers/kim2025_conductive_agent_se_coating_cathode.md` | exp(계산無) |
| **[Kang]** ⭐우리그룹 | Kang/Shin/Y.Lee/**Jong-Won Lee** 2026 ChemComm *Feature Article* — *Intertwined* electrochemo-mechanical degradation 리뷰 (한양대 우리 연구실 자체 리뷰, 18 pp). thesis = 전기화학 분해 ↔ 기계 불안정의 **양방향 되먹임 고리**; 진짜 적 = *heterogeneity*; 3대 완화 = SE도핑/CAM코팅/음극공학 | ✅ `papers/kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review.md` | review(우리그룹·자체데이터無) |
| **[Kang25]** ⭐우리그룹 | Kang/Y.Lee/Bae/**Jong-Won Lee** 2025 ChemComm (61, 16850) — NCM811에 **LPSCl(=comp1) conformal dry-coating** → 고전압 **기생반응을 *균일*화**(식1 `2Li₆PS₅Cl→P₂S₅+5S+2LiCl+10e⁻+10Li⁺`) → NCM 균질 chemical lithiation(SOC↓) → layered→rock-salt 억제 → R_int 4.3 Ω cm²·200cyc 유지율 **+15.0 %**. **이로움 = SOC-강하(코팅), passivation 아님** | ✅ `papers/kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb.md` | exp(계산無) |
| **[Cha]** ⭐우리그룹 | Cha/Yun/Kim/**Kang**/Cho/**Jong-Won Lee** 2024 J.Power Sources (617, 235157) — high-Ni NCM에 **할라이드 SE(LIC=Li₃InCl₆/LYC=Li₃YCl₆/LZC=Li₂ZrCl₆) 8–10 nm 코팅**으로 NCM-LPSCl(=comp1) 계면 부반응 억제. **핵심 = *dual compatibility*(NCM·LPSCl *양쪽* 호환)가 결정, σ 아님**: LIC(In) 양쪽 분해(In₂S₃)·LYC(Y) LPSCl과 분해(Y₂S₃)·**LZC(Zr⁴⁺) 양쪽 무분해=최고**. 계면저항 bare 74.4→LZC **20.1 Ω·cm²**·100cyc LZC **91.2 %**(LIC 80.8 < bare 83.1 < LYC 87.3). **우리 그룹 cathode-interface 3부작 *기원(2024)*** (→Kang25→Kang) | ✅ `papers/cha2024_dualcompatible_halide_ncm_lpscl_interface.md` | exp(계산無) |

---

> 🗺️ **Landscape note [Rupp]** (digest `papers/kim2021_review_oxide_sulfide_se_interfaces.md`): 우리 LPSCl/LPSCl1.6의 좌표계 논문. **oxide(garnet LLZO: σ~1 mS/cm·환원 0.05 V·산화 2.9 V·E 140–160 GPa·취성) vs sulfide(argyrodite Li₆PS₅X: σ~10⁻³·환원 1.7 V·산화 2.0–2.2 V·E~10–37 GPa·연성)** 의 head-to-head + 양극/음극 계면 카탈로그(Table 1·2·3·4, SI Table 1). 우리 숫자(ESW band·환원산물·연성)를 *검증*이 아니라 *문헌 줄에 정렬*하는 용도. **Cl-rich(LPSCl1.5/1.6) 자체는 안 다룸** → 우리 비교는 리뷰 너머의 기여.

> ⭐ **우리 그룹 동반 논문 note [KimICCF]** (digest `papers/kim2026_iccf_molten_salt_sei_lpscl_sheet.md`): **한양대 Kuk Young Cho + Yonsei Yong Min Lee** (우리 LPSCl DFT 계보)의 **실험** 논문. SE = **Li₆PS₅Cl(=우리 comp1)**. 격자 도핑이 아니라 **액체 cavity-filler(ICCF=IL [EMIM][TFSI]+LiTFSI+FEC)** 로 **(1) σ 회복(시트 1.44→2.23 mS/cm, 155 %, 펠릿 70 %)** + **(2) 음극 in-situ LiF-rich SEI**(XPS F1s 684 eV, Li₂S 억제) 달성. **🔑 두 개의 평행:** (a) **σ 손실 원인 = 공동(미세구조 34.2 %), bulk 결정 아님** → 우리 "σ_e/σ는 interphase·microstructure 레버, bulk 아님" 결론과 **양 날개**. (b) **LiF-rich SEI가 SE 분해 억제 = 우리 'electron-blocking(전자절연) interphase'(Li₂O/Li₃PO₄/NdPO₄/LiCl) 메커니즘의 실험 카운터파트** (LiF·LiCl·Li₂O 모두 wide-gap 절연 패밀리). DFT는 분자 HOMO/LUMO(B3LYP/6-311++G)+GeoDict digital-twin뿐 → **bulk 결정 DFT 수치 직접 대조는 부적절, 개념(목표·레버) 정렬 용도.** ⚠ Cl 1.0(comp1)만; modelc(Cl 1.6) 없음.

> ⭐ **우리 그룹 동반 논문 note [KimCA]** (digest `papers/kim2025_conductive_agent_se_coating_cathode.md`): **Yonsei Yong Min Lee + DGIST** (우리 LPSCl DFT 계보)의 또 다른 **순수 실험·전극공정** 논문. SE = **Li₆PS₅Cl(=우리 comp1**, POSCO JK, D50 1 µm), 양극 = LiNbO₃-NCM711. **격자 도핑이 아니라 양극 복합체 측** — SE를 CAM에 코팅할 때 **도전재(CA) 차원**이 코팅 형상·전자전도 경로를 지배함을 보임: **SE@CAM(CA無, dense, σ_e 3.3×10⁻² S/cm·185.3 mAh/g·CE 81.6 %)** vs **SE-SP@CAM(0D Super P, Super-P-rich, σ_e 1.0×10⁻⁵=3,000배↓·활성표면적 1.00→0.51·151.6 mAh/g)** vs **SE-VGCF@CAM(1D VGCF-embedded porous, σ_e 1.4×10⁻²=SE@CAM 수준 회복·183.5 mAh/g·CE 82.7 %·200 cyc 76.8 %)**. **🔑 핵심**: ASSB 성능 레버 = **코팅층 형상 + 전자전도 경로(CA 차원·mixing protocol)**, bulk 결정 아님 → 우리 "lever = interphase/microstructure, not bulk lattice" 결론의 **양극(cathode) 측 실험 보강**. ⚠ **계산 전혀 없음 → DFT 수치 직접 비교 절대 금지**; σ_e/σ_i 절대값도 device(복합양극) σ라 우리 bulk와 대상 다름. 비교는 **동일 SE(comp1) + 개념(레버=미세구조) + 같은 그룹 동반** 수준만. modelc(Cl 1.6) 없음.

> ⭐ **우리 그룹 리뷰 note [Kang]** (digest `papers/kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review.md`): **우리 연구실(한양대 Jong-Won Lee)이 직접 쓴 ChemComm Feature Article 리뷰** — 즉 *우리 DFT의 상위 세계관* 문서. **thesis: 황화물 ASSB의 진짜 병목은 "산화/환원 분해(전기화학)" 하나도 "균열/접촉손실(기계)" 하나도 아니라, 둘이 서로를 유발·가속하는 *양방향 되먹임 고리*(reaction→fragility→fracture→fresh-surface→re-reaction)** 이고, 따라서 "**chemical passivation *or* mechanical reinforcement가 아니라 *both simultaneously*** "가 필요. **진짜 적 = decomposition/stress 자체가 아니라 그들의 *heterogeneity*(공간 불균일).** 구조: §2 전기화학분해(양극4종=산화/CAM계면/CA-TPB/대기 + 음극3종=환원/dendrite, Nolan **Type1/2/3** 계면) → §3 기계분해(공동·접촉손실·CAM균열·Li100%·응력-dendrite) → **§4 coupling(되먹임)** → §5 **3대 완화(① SE도핑 ② CAM코팅 ③ 음극공학)** → §6 통합 chemo-mechanical 로드맵. **🔑 우리 DFT 매핑**: (a) **§5.1(b) O²⁻ 옥시설파이드(Li₆PS₄OCl, 전자누출↓·ECW확대·O–P>S–P) + §5.1(c) Li₃PO₄ buffer = 우리 Nd2O3/O-doping cascade의 리뷰 내 정당화** (우리 sei_products.json: O-derived Li₃PO₄ 5.73·Li₂O 5.24·NdPO₄ 5.55 eV가 conductive Li₃P 0.70 대체 = "reduced electron leakage"의 정량판). (b) **Nolan Type1/2/3(Fig5c) = 우리 SEI 전자절연 분류의 표준 프레임** (insulator≥4/conductor<2 eV 임계 = Type 정량판; Type3로 밀자 = cascade 목표). (c) **Fig1a ECW(ref49 Zhu/He/Mo)=우리 grand-potential 동일방법** (comp1 2.256 V 정렬); **Fig1b thermo vs kinetic ECW** = 우리 onset(thermo) vs 실험창(kinetic) 차이 그림. (d) **§6 트렌드3 "modifying one parameter alters others" = 우리 cascade의 stability↔Li-mobility blocking trade-off** 와 정확히 일치. ⚠ **정직한 한계**: 리뷰의 *핵심*(coupling 되먹임·heterogeneity)은 **우리 정적 bulk DFT 밖** — 우리는 고리의 *끝점*(분해화학 + bulk elastic)만 닻을 내림; 동역학은 그룹 phase-field(ref39=Kim/Park/Lee)·stack-pressure(ref120=Kang)·operando가 잇는다. 리뷰는 argyrodite를 **Li₆PS₅X 일반**으로만 다뤄 **Cl-rich(modelc) vs comp1 비교 없음**(=우리 기여 여지). 전부 2차 인용(자체 데이터無). self-cite 밀도 높음(refs 31·39·40·56·67·68·69·70·73·120) = 우리 그룹 강점이 곧 리뷰 강조점.

> ⭐ **우리 그룹 동반 논문 note [Cha]** (digest `papers/cha2024_dualcompatible_halide_ncm_lpscl_interface.md`): **한양대 Jong-Won Lee 그룹(+DGIST·KETI)의 cathode-interface 라인 *기원(2024)*** — Junhee Kang이 [Cha]·[Kang25]·[Kang] 세 논문 모두 참여(즉 [Cha]2024 → [Kang25]2025 → [Kang]2026 **3부작의 첫 편**). SE = **Li₆PS₅Cl(=우리 comp1)**, 양극 = single-crystalline LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂. **격자 도핑도(우리 cascade), SE-코팅도([Kang25]) 아니라 — *별도 할라이드 SE*(LIC/LYC/LZC)를 NCM 입자에 8–10 nm conformal 코팅**해 NCM-LPSCl 직접접촉을 차단. **🔑 핵심 발견 = "dual compatibility"**: 양극 복합체서 할라이드 코팅은 **NCM·LPSCl 두 상과 동시 접촉** → *양쪽 모두*와 호환돼야 함. **LIC(In→In₂S₃ 환원, 양쪽 분해) / LYC(Y→Y₂S₃, LPSCl과 분해) / LZC(Zr⁴⁺ 양쪽 무분해, 7일·100cyc 안정)** → **Li₂ZrCl₆만 dual compatible** → 계면저항 74.4→**20.1 Ω·cm²**(1/3.7)·100cyc **91.2 %**. **두 개의 정밀 정렬:** (a) **σ≠성능** — σ는 LIC(1.12)>LZC(0.51)>LYC(0.37)인데 성능은 LZC>LYC>**LIC(꼴찌, bare보다도 나쁨 80.8<83.1)**; 논문 명시 "interfacial resistance ... cannot be explained in terms of ionic conductivity" → **우리 'lever=interphase/microstructure, not bulk σ' 결론의 cathode-side 세 번째 실험증거**([KimICCF]sheet σ·[KimCA]양극 σ_e에 이어). (b) **dual-compatibility = 우리 `GrandPotentialInterfacialReactivity`(voltage-resolved) 도구의 *완벽한 적용 대상*** — LIC/LYC/LZC×{NCM,LPSCl} 6계면 호환성을 우리 도구가 in-silico 재현·예측 가능(왜 Zr⁴⁺만 견디나). ⚠ **정직한 한계**: (1) **계산 0** → DFT 수치 직접 비교 금지; (2) **Zr가 우리 Cl-Li-Nd-O-P-S hull에 없음** → LZC dual compatibility를 우리 grand-potential로 *아직* 정량 못 함(향후 Zr hull); (3) 호환 기전(Zr⁴⁺ passivation·In 환원)은 **정성적 환원전위 trend**이고 논문 스스로 "yet speculative"; (4) modelc(Cl-rich) 없음(comp1만). **이로움이 우리 Nd passivation과 같은 'wide-gap 절연 CEI'냐?** — *부분만*: LZC가 *새 저항층을 안 만든다*(compatibility)는 우리 "interphase가 부반응 차단" 프레임과 결이 같으나, 우리 Nd는 *능동적 절연 CEI 형성*, Cha는 *비반응성 코팅(no new interphase)* → **메커니즘 위치가 다름**(코팅 차단 vs 도핑 산물). "Cha=Nd passivation 실험증거"라고 하면 부정확.

> 🗺️ **Landscape note — 우리 그룹 cathode-interface 3부작 [Cha]2024 → [Kang25]2025 → [Kang]2026**: **세 논문 모두 Jong-Won Lee 교신 + Junhee Kang 참여 + SE=comp1(Li₆PS₅Cl)**, 고-Ni NCM–LPSCl **양극 계면**을 *서로 다른 레버*로 공략한다 — **[Cha]2024 = 양극활물질에 *별도 할라이드 SE* 나노코팅(LZC dual-compat)** / **[Kang25]2025 = 양극활물질에 *LPSCl 자체* conformal 코팅(기생반응 균일화·SOC강하)** / **[Kang]2026 = 그 위의 electrochemo-mechanical 통합 리뷰(coupling 지붕)**. **🔑 공통 결론 = "고전압 NCM-LPSCl 계면은 *어떻게 관리/차단하느냐*가 수명을 좌우"** (분해를 없애기보단 균일화·비반응 코팅·통합설계). **우리 DFT의 위치**: 세 편 다 *device/계면 화학*만 다루고 **atomistic 분해화학·전자구조는 우리 grand-potential·interface_reactivity가 채움** — 특히 [Cha]의 dual-compatibility(6계면)는 우리 voltage-resolved 도구로 *직접 in-silico 재현 가능*한 가장 깨끗한 적용 대상. → deck "우리 연구의 위치": **그룹 cathode-interface 3부작(코팅·기생·리뷰) 아래 우리 DFT(어떤 산물·왜 호환/비호환을 grand-potential로 정량)**.

> 🗺️ **Landscape note — 우리 그룹 4중 구도 [Kang]리뷰 × [KimICCF] × [KimCA] × 우리 DFT**: **[Kang] 리뷰가 *지붕*(세계관·로드맵)**, 나머지 셋이 *기둥* — (a) **우리 DFT(comp1/modelc/Nd/ESW/elastic/cascade) = 리뷰 §5.1(SE도핑) + coupling 고리의 전기화학·기계 *끝점* atomistic 닻**, (b) **[KimICCF](sheet σ회복·음극 in-situ LiF SEI) = 리뷰 §5.3(음극공학)·§3(미세구조 공동)의 실험**, (c) **[KimCA](양극 CA 차원·TPB) = 리뷰 §2.1.3(CA-derived 분해)·§5.2(CAM코팅·LNO-NCM)의 실험**(ref69가 곧 [KimCA]). **🔑 공통 결론**: 리뷰가 "electrochemo-mechanical을 *통합·균질성 중심*으로 설계하라 + multi-scale 계산×operando로 받쳐라"고 부르고, 우리 DFT가 그 multi-scale의 *atomistic 기둥*. → deck "우리 연구의 위치" 최종 슬라이드: **[Kang] coupling 고리(Fig16) 위에 우리 DFT(분해화학+elastic+O-doping interphase) + 두 동반실험(sheet/anode + cathode/TPB)을 얹으면 = 우리 그룹의 통합 chemo-mechanical 프로그램 한 장**.

> 🗺️ **Landscape note — 같은 그룹 3각 구도 [KimICCF] × [KimCA] × 우리 DFT**: 한 그룹(Yonsei Y.M.Lee + 한양대 Cho + DGIST) 안에서 ASSB의 전 영역이 **분업·수렴**한다 — **(a) bulk 격자·산화창·Li 이동도·환원산물 = 우리 DFT(comp1/modelc/Nd)**, **(b) 시트 σ 회복(공동 채움) + 음극 in-situ LiF-rich SEI = [KimICCF]**(sheet/anode-side), **(c) 양극 복합체 전자전도·코팅 형상(CA 차원) = [KimCA]**(cathode-side). 세 논문 모두 SE = **Li₆PS₅Cl(=comp1)**. **🔑 공통 결론**: ASSB의 실현 성능을 좌우하는 레버는 **bulk 결정이 아니라 미세구조·계면·전자전도**다 — [KimICCF]는 "σ 손실=공동(미세구조)·SEI=계면화학", [KimCA]는 "양극 성능=코팅형상·전자경로(CA 차원)", 우리 DFT는 "bulk는 wide-gap·S-limited onset·Cl이 σ↑/onset 불변 → 차별화 여지가 interphase에 있음". → deck "우리 연구의 위치" 슬라이드: **우리 DFT(bulk) + 두 동반 실험(cathode·sheet/anode) = '레버는 interphase/microstructure'에 양·음극 양면으로 수렴**. ⚠ 두 실험 논문 모두 **modelc(Cl-rich) 없음**(comp1만), [KimCA]는 **계산 0**(개념 비교만).

## A. 이온전도도 — *Cl-rich가 빠르다 (전원 일치)*
| 주장 | 출처 | 우리 (comp1→modelc) | 일치 |
|---|---|---|---|
| Cl↑ → σ 2.5→7–10 mS/cm, Ea 0.34→0.22 eV | [Zuo](2.9→7.0), [GG](AIMD peak 14.55 @Cl1.5), [Liu], Excel exp 다수 | D(600K) 3.09→7.90e-6, Ea 0.253→**0.224** | **✓✓** |
| σ 기전 = inter-cage Li jump (Cl 4c 무질서) | [GG] (Li 확률밀도, Fig 1e,f) | 우리 percolation/inter-cage 분석과 동일 물리 | ✓ |
| **Li₆PS₅Cl = S²⁻/Cl⁻ 완전 disordered → 가장 빠른 Li⁺** (Cl이 X=Cl,Br,I 중 disorder 최대) | **[Rupp]** p.9 | comp1→modelc D↑·Ea↓ (Cl-rich 빠름) | **✓ 구조적 근거** (Cl disorder = σ↑ 원인) |
| AIMD setup (300 eV/Γ/NVT) | [GG] | 동급 | ✓ 방법 정합 |
| **device σ ≠ bulk σ: 손실 원인 = 미세구조(공동), bulk 결정 아님** (시트 1.44 ↔ 펠릿 3.2 mS/cm; 공동 채우면 2.23=155 %) | **[KimICCF]** (Li₆PS₅Cl=comp1, GeoDict digital-twin) | 우리 bulk AIMD RT-외삽 σ ≫ 실현 σ | **🔑 개념 평행**: 우리 "σ는 interphase·percolation 변수"와 일치. **둘 다 "bulk 잠재력 ≫ device σ"** → 미세구조가 병목. 절대값 직접 비교는 금지(bulk 단결정 vs 시트 실측) |
| **device 전자전도 σ_e = 코팅 형상·도전재 분포가 지배(양 아니라 연결성)** — 양극 복합체 σ_e가 3,000배 변동(3.3×10⁻²↔1.0×10⁻⁵ S/cm), 활성표면적 1.00↔0.51; **CA 차원(0D Super P 나쁨 / 1D VGCF 좋음)** 이 레버 | **[KimCA]** ⭐ (Li₆PS₅Cl=comp1, 계산無) | 우리 bulk σ_e 미측정(gap 2.066/2.098 eV=wide-gap insulator); device σ_e 못 봄 | **🔑 개념 평행(양극측)**: ASSB 성능 레버 = 코팅 형상·전자전도 경로(미세구조), bulk 결정 아님 → 우리 "lever=interphase/microstructure" 결론의 cathode-side 보강. ⚠ **계산 0 → DFT 수치 비교 금지**; σ_e 절대값도 device(복합양극)라 우리 bulk와 대상 다름 |
| **device 계면저항 = 코팅 *화학 호환성*이 지배, σ 아님** — 할라이드 코팅 σ는 LIC 1.12 > LZC 0.51 > LYC 0.37 mS/cm인데 계면저항은 **LZC 20.1 < LYC 30 < LIC 55 ≪ bare 74.4 Ω·cm²**(역경향)·수명도 LZC 91.2 > LYC 87.3 > bare 83.1 > **LIC 80.8 %**(σ 1등이 꼴찌). 논문 명시 "cannot be explained in terms of ionic conductivity" | **[Cha]** ⭐ (Li₆PS₅Cl=comp1, 계산無) | 우리 σ=bulk AIMD; device 계면저항 못 봄 | **🔑 개념 평행(양극측, 세 번째)**: 성능 레버 = 계면 *화학 호환성*(dual compatibility), bulk σ 아님 → [KimICCF](sheet σ)·[KimCA](양극 σ_e)에 이어 "lever=interphase, not bulk σ"의 **cathode-side 세 번째 실험증거**. ⚠ **계산 0 → DFT 비교 금지**; Zr 우리 hull에 없음 |
> 인사이트: 우리 AIMD가 실험·문헌 trend 재현 → 신뢰. 절대 σ는 RT 외삽이라 Arrhenius로 비교. **[KimICCF]: 같은 그룹 실험이 "σ 병목은 bulk가 아니라 미세구조(공동)" 를 직접 보여줘 우리 'lever=interphase' 결론을 실험으로 보강** (GeoDict σ 1.96/2.10 sim ≈ 1.95/2.17 exp). **[KimCA]: 같은 그룹이 양극 측에서 "device σ_e·성능은 코팅 형상·도전재 차원(미세구조)이 지배, bulk 아님" 을 직접 보여줘 같은 결론을 cathode-side로 확장** (CA 양 아니라 분포·연결성; Super P 과잉이 오히려 σ_e 3,000배↓). → **[KimICCF](sheet/anode) + [KimCA](cathode σ_e) + [Cha](cathode 계면 호환성) = 우리 'lever=interphase/microstructure, not bulk σ' 결론에 *세 우리 그룹 실험*이 수렴** (특히 [Cha]는 σ와 성능이 *역경향*인 가장 깨끗한 반례: σ 1등 LIC가 성능 꼴찌).**

> ⚠ **유추 전용 note — *재료 비교 아님* (NOT a materials comparison)** [EXTERNAL `papers/liu2013_cage_methane_adsorption_hydrate_nucleation.md`]: **가스 수화물(물 cage + 메탄) 논문** — argyrodite 아님, 위 표 *어느 행에도 들어가지 않음*, 수치 대조 금지. **전이 가능한 *개념 멘탈모델* 하나만**: Liu 2013은 classical-MD PMF로 "**cage 면(window) 크기가 guest의 trap-vs-cross를 자유에너지 장벽으로 결정**"(면 4→6각 흡착 E_a 11.7→21.3 kJ/mol↑, **7각부터 guest 통과=inter-cage 확산**)을 보였다. 이를 우리 Li⁺ **inter-cage hopping**을 *말로 설명*하는 비유로만 차용 — 우리 cascade **`migration_volume_fraction`(BVSE bottleneck volume)= "유효 창 크기"**, **tier2 `dopant_blocking_fraction`= "dopant가 inter-cage 창을 좁혀 장벽↑"**(우리의 high-valence dopant blocking·stability↔mobility trade-off, Nd-doping σ300 0.52×/D 0.62× drop을 *왜*로 직관화: dopant가 bottleneck 위/근처에 앉아 창 조임). **검증 0·수치 전이 0** — 다른 시스템(물cage/CH₄ vs PS₄/Li⁺)·다른 결합(vdW·H-bond vs 이온 정전)·다른 방법(MD PMF, 258.5 K·30 MPa vs 우리 BVSE 0 K 정전 / AIMD MSD / NEB). kJ/mol 메탄 흡착 ≠ eV Li hop 장벽 — **절대 같은 표·"일치"로 인용 금지**. 순수 사고 틀.

## B. 산화안정성 — **4축 분리 (축 명명 없이 말하면 틀림)**
| 축 | 우위 | 출처 | 우리 값 / 재현 |
|---|---|---|---|
| **B① intrinsic 0-pressure onset** | **무승부** (S²⁻-limited, 둘 다 2.256 V) | [GG] K_eff=0 = **1.70–2.40 V**; **[Rupp]** LPSCl DFT **2.01 V**(→Li₃PS₄+S+LiCl) / **2.2 V** vs LCO(→LiCl+Li₄P₂S₆+Li₂S) | 우리 grand-potential OCV 1.717 / **onset 2.256**(LiS4 제외, GG set; 포함 시 2.14) → **✓✓ 재현**, GG 2.40과 격차 0.14 V, [Rupp] 2.0–2.2 V band와 정합 |
| **B① 방법: indirect (de)lithiation** | (우리 못 봄) | **[Rupp]** §2.5.2: LPSCl→**Li₄PS₄Cl/Li₁₁PS₅Cl 중간상** 거쳐 분해 → 실험창 ~1.25–2.5 V로 넓어 보임 (Schwietert/Wagemaker) | 우리 onset이 실험보다 낮은 이유 = indirect/passivation/kinetics의 **방법 근거** |
| **B② 기계 구속 window** | **Cl-rich 승** | [GG] K_eff=20 LPSCl1.5 **0.80–4.30 V** (Cl 산물 고몰부피→strain) | 우리 `constrained_esw.py`가 trend 재현(modelc 더 넓어짐) → **✓** |
| **B③ cathode 계면 cycling** | **Cl-rich 승** | [Zuo] R_cat 8.9<13.2, CE 79>77% (산물 양호) | 우리 grand-potential이 [Zuo] Eq1/Eq2 분해 stoichiometry 재현 → **✓ 화학** |
| **B③ cathode 계면 — *레버 = SE 코팅*** (Cl 함량 아님) | **SE-coated 승** | **[Kang25]** ⭐ R_int 4.3 Ω cm²·200cyc 유지율 **+15.0 %**·OCV 강하 +10.1 mV; 식1 `2Li₆PS₅Cl→P₂S₅+5S+2LiCl+10e⁻+10Li⁺` → NCM811 균질 chemical lithiation(SOC↓) | 우리 grand-potential이 식1 산화분해(P₂S₅계+S+LiCl)를 **voltage-resolved로 재현·검증** (2.14 V S²⁻→폴리설파이드 … 3.06 V 원소 S). **단 이로움 = SOC-강하(코팅 균일화)이지 passivation 아님** → Nd(절연 CEI)와 *다른 physics* (§B 주석·§D) |
| **B③ cathode 계면 — *레버 = 할라이드 코팅의 dual compatibility*** (Cl 함량 아님) | **dual-compat 할라이드(LZC) 승** | **[Cha]** ⭐ 할라이드(LIC/LYC/LZC) 8–10 nm 코팅; **LZC=Li₂ZrCl₆만 NCM·LPSCl 양쪽 호환**(7일 무분해) → 계면저항 74.4→**20.1 Ω·cm²**·100cyc **91.2 %**; LIC(In₂S₃)·LYC(Y₂S₃) 비호환·**LIC는 bare보다 나쁨(80.8<83.1)** | 우리 grand-potential이 bare NCM-LPSCl 분해(phosphate·P₂Sₓ·Li₂S, Cha XPS Fig5e)를 **재현**(우리 산화 staircase P₂S₇·S·폴리설파이드·LiCl). **단 LZC dual compatibility(Zr⁴⁺ passivation)는 Zr가 우리 hull에 없어 *아직* 정량 못 함** → 향후 Zr hull + interface_reactivity. **이로움 = *새 저항층 안 만듦*(비반응성 코팅)이지 능동적 절연 CEI 형성(Nd) 아님** → §B 주석·§D, "Cha=Nd 실험증거"는 부정확 |
| **B④ calendar/thermal/moisture** | **Cl-poor(LPSCl) 승** | [Wu] 90℃ retention L6 68%>L55 48% | 범위 밖(우리 못 봄) |
| **B① thermodynamic vs kinetic ECW 프레임** | (개념) | **[Kang]** Fig1b: full-cell **thermodynamic / kinetic / predicted ECW** 구분 (kinetic passivation이 창을 넓게 보이게) | 우리 grand-potential onset 2.256 = **thermodynamic ECW**; 실험창(>3 V) = kinetic. **✓ 우리 "실험창이 왜 넓나"의 정확한 그림** (Fig1a ref49 Zhu/He/Mo = 우리와 동일 grand-potential 방법) |
| **B③ CAM/SE 계면 비호환 산물** | **Cl-rich 무관(조성 일반)** | **[Kang]** Fig3b,c (Banerjee ref51 AIMD): LPSCl–delithiated NCA → **LiCl·Li₃PO₄·NiS₂** 자발형성; 고SOC O방출→SOₓ | 우리 interface_reactivity·sei_products.json도 LiCl·Li₃PO₄ 예측 → **✓ 일부 같은 산물**(NiS₂는 우리 6원소 hull에 Ni 없어 못 봄) |
> - 우리 ESW는 **B①만** 봄(S-limited 구조적). 분해 *양*([Zuo] CV 2×)·metastability(DSC/TGA)·기체는 못 잡음.
> - **[Kang] 리뷰**: 산화 ~2.0–2.5 V(Fig1a)·thermo vs kinetic ECW(Fig1b)·계면 비호환 산물(Fig3 LiCl/Li₃PO₄/NiS₂)로 **우리 산화 프레임을 우리 그룹 리뷰가 직접 정렬**. O-doping(§5.1b)이 ECW *확대*(CV 관찰=kinetic)라 서술 ↔ 우리 Nd hull은 intrinsic 창 *narrows*(thermo) → **다른 축**(둘 다 맞음, 명명 필수).
> - **[Kang25] (우리 그룹 실험, 이 논문)**: "이로운 기생반응" = 고전압 LPSCl 산화분해[식1]가 NCM을 **균일 재리튬화(SOC↓)** → layered→rock-salt 억제 → +15.0 % 유지율. **🔑 우리 narrative와의 두 가지 정밀 정렬**: ① 식1 산물(P₂S₅계+S+LiCl) = **우리 grand-potential 산화분해와 동일 화학** → *같은 그룹 실험이 우리 계산을 (간접) 검증*; ② **그러나 이로움의 *메커니즘*은 SOC-강하(코팅 균일화)이지 wide-gap 절연 CEI가 아님** → 우리 **Nd passivation(NdPO₄/NdCl₃ 절연 e⁻차단)과 *다른 physics*** (Kang 산물 중 LiCl만 절연, P₂S₅·S·폴리설파이드는 전도성). **"Kang = Nd passivation 실험증거"라고 하면 틀림**; 둘은 *상보적 두 레버*(코팅=SOC관리 / 도핑=절연CEI). 변수도 Cl이 아니라 *SE 코팅 유무* → 4축 Cl표에 넣지 말 것.
> - **[Cha] (우리 그룹 실험, 2024 — cathode-interface 라인 *기원*)**: NCM에 **할라이드 SE(LIC/LYC/LZC) 나노코팅**으로 NCM-LPSCl 계면을 *차단*. 결정 변수 = **dual compatibility**(코팅이 NCM·LPSCl *양쪽*과 무분해) — **LZC=Li₂ZrCl₆**만 만족(7일 무분해)·LIC(In₂S₃)·LYC(Y₂S₃) 비호환. **🔑 우리 narrative와 두 정밀 정렬**: ① **σ≠계면저항**(σ LIC>LZC>LYC인데 계면저항 LZC≪LIC·LIC는 bare보다도 나쁨) = 우리 "lever=interphase, not bulk σ"의 cathode-side 증거(축 A에도 등재); ② **dual-compatibility(6계면)=우리 `GrandPotentialInterfacialReactivity` 도구의 완벽한 적용대상**(왜 Zr⁴⁺만 견디나 in-silico). **그러나 이로움 메커니즘 ≠ Nd passivation**: Cha=*비반응성 코팅(no new interphase)*, Nd=*능동적 wide-gap 절연 CEI 형성* → 위치 다름(레버 A=[Kang25]SE코팅·B=[Cha]할라이드코팅·C=우리 SE도핑, 셋 다 *다른* 레버). **변수 = Cl 함량 아니라 *코팅 할라이드 종류* → 4축 Cl표에 넣지 말 것**(이 표는 cathode-interface 레버 행으로만). ⚠ Zr 우리 hull 부재 → 정량은 향후.
> - **deck 결론**: "전도도 이득이 산화창 손해 없이(B①–③ 중립~유리), 비용은 shelf-life(B④). **양극 계면은 별도 레버(코팅·도핑)로 관리** — [Cha]할라이드 dual-compat / [Kang25]SE코팅 균일화 / 우리 cascade SE도핑." 축·레버 명명 필수.
> - **LiS4 단서**: 우리 onset 2.14 vs [GG] 2.40 차이 = LiS4(mp-995393) 포함 탓 → 제외 시 2.26 (정합↑).

## C. 기계적 물성 — *값이 functional·정의 의존*
| 주장 | 출처 | 우리 | 비고 |
|---|---|---|---|
| E=22.1/B=28.7/G=8.1 (SQS) | [Kaur] | E_VRH 22.06(comp1) | functional/SQS 차이 |
| E=27.4/B=34.7/G=10.0, B/G=3.46(연성) | [JPCC] (PBE-D3) | E_VRH 27.66(modelc), B0 26.23→21.71 | D3라 절대값↑ |
| E 21.3→21.6 (Cl0→1.5 거의 불변) | Excel calc#12 | 우리 E_VRH 22→27.7 (변동) | 무질서/protocol 차이 |
| **sulfide 연성(B/G 1.25–2.5, E~10–37 GPa, 냉간가압) vs oxide 취성(E 100–200 GPa, K_IC 0.8–1.6)** | **[Rupp]** SI Table 1·§2.4 | 우리 B/G·연성 결론 동일 | **✓ "왜 황화물" deck 1슬라이드** (연성=부피변화 수용·intimate contact) |
| **sulfide SE E 20–30 GPa(소성변형으로 응력 수용) vs oxide CAM E 150–200 GPa → 변형 불일치=공동/접촉손실/균열** | **[Kang]** §3.1.1/§3.1.3 (refs101–103) | 우리 E_VRH·EOS B0 (comp1 26.2/modelc 21.7 GPa BM-EOS); DFT 0K E_VRH comp1≈modelc 52.3 | **✓ landscape 정렬** (우리=soft SE 줄). ⚠ **vacancy paradox**: DFT 0K가 Cl-rich 강성 못 잡음(리뷰 "20–30 GPa·연성" 추상화의 *방법 의존성*을 우리가 노출) |
| **CAM 부피변화 6–8%·이방성 → SE microgap·균열·접촉손실(chemo-mechanical)** | **[Kang]** §3.1.2/§3.1.3 (ref103) | 우리 elastic = SE 측 응력 수용 능력(연성)만; CAM 부피변화·접촉손실은 device 스케일 | △ **우리 bulk DFT 밖** (phase-field ref39·우리그룹이 다리) |
| ⚠ argyrodite **E 92–100 / G 38–43 GPa** (단일 ref) | **[Rupp]** SI Table 1 | 우리 E_VRH 22–28 | **✗ outlier — 인용 금지** (같은 표 glass 13–28·LGPS 37과도 어긋남) |
| Monroe-Newman: dendrite 억제 **G_SE > ~2 G_Li (≈6.8–8.5 GPa)**, 단 무기SE엔 불충분(K_IC·grain·σ_e가 변수) | **[Rupp]** §2.4/§4.2 | 우리 G_VRH·B/G → dendrite 다리 | 우리 elastic→dendrite 연결 시 **G 하나로 결론 금지** |
> 차이 원인: relaxed vs clamped-ion, PBE vs PBEsol/D3 → 절대 E/B ±수 GPa. **비교 전 functional·ion-relax 맞출 것.** B/G 연성 결론만 robust. **[Rupp] argyrodite E절대값(92–100)은 outlier — 무시.**

## D. 전자구조 / band gap — *방법 의존, 절대 비교 금지*
| 주장 | 출처 | 우리 | 비고 |
|---|---|---|---|
| PBE gap **LPSCl 1.88 / LiCl 6.22 eV** | [Lu] | comp1 2.066 / modelc 2.098 (PBE) | 무질서·Γ-only k ±0.2–0.3 scatter. LiCl 6.22 = 전자절연 interphase 기준 |
| PBE 2.10→2.62 (In 도핑) | [Ma] | — | In 0.52 eV↑인데 σ_e 1.2×만 변(=defect-controlled) |
| PBE 2.45 / **HSE06 3.30** | [Semi] | (우리 PBE 2.07) | PBE는 ~1 eV 과소 → "wide-gap insulator"만 |
| VBM = S 3p (HAXPES) | [Banik] | 우리 PDOS VBM=S 3p | **✓ 재현** |
| **산화 onset ≈ 음이온 p-band(VBM) 깊이**: S 3p(얕음)→LPSCl 2.256 V vs O 2p(깊음)→LLZO **2.88 V (+0.63)** | [Rupp] + **우리 LLZO grand-potential**(`papers/kim2021…md` §LLZO) | comp1 VBM=S 3p, onset 2.256 | **✓ VBM character가 onset 지배** (S²⁻→S⁰ vs O²⁻→peroxide) |
| PS₄ "gap" ~2.0 → MgS₄ ~4.2 eV (도핑이 gap 확대) | [Liu23] | comp1 2.066 ≈ 그들 LPSC ~2.0 (우연) | MP smear 0.2 + PDOS 분리 추정, 엄밀 gap 아님; **MgS₄ 구조 자체 부실(§12b)** |
| **bulk σ_e(실측) = 8.16×10⁻⁹ S/cm** (Mg/F 도핑 시 1.03×10⁻⁹, 8×↓) | [Liu23] (DC분극) | 우리 미측정 | **slide25 σ_e 논의 실측 기준값** |
| sulfide = "wide-band-gap" (구체 LPSCl gap 미제시; buffer LiI gap 6.4 eV) | **[Rupp]** | comp1 2.066 / modelc 2.098 (PBE) | 리뷰 gap 절대값 無 → "wide-gap insulator" 수준만 일치(비교대상 자체 없음) |
| **interphase는 전자절연이어야 self-limiting** (LPO ALD로 LLZO σ_e 10⁻⁸→10⁻⁹ → dendrite 억제) | **[Rupp]** Fig 13·17 | (우리 σ_e 논의 frame) | [Ke]Li₂O·[Lu]LiCl·[Liu23]LiF 절연 interphase 논리의 **landscape 근거** |
> 인사이트: ① **모델 간 gap scatter(1.88 vs 2.10)는 σ_e 차이를 설명 못 함** — [Ma]는 gap +0.52인데 σ_e 1.2×만(=defect/carrier 지배, slide25 틀). ② 단, **큰 전자구조 변화(도핑)는 σ_e를 바꿈** — [Liu23]는 Mg/F로 σ_e 8×↓(gap 확대 + LiF + carrier 변화 복합, gap만 분리 불가). → "작은 모델 scatter ≠ σ_e / 큰 도핑 변화 = σ_e 가능", 두 경우 구분.

## E. 환원 / 음극(Li 금속) 계면 — **⚠ Cl-rich 유불리 문헌 충돌 (자리 점유가 변수)**
| 주장 | 출처 | 우리 | 일치 |
|---|---|---|---|
| 분해창 환원 <1.7 V / 산화 >2.1 V | [Ke] (인용), [GG] | ESW 환원 **1.24 V** / 산화 **2.14 V** | 산화 ✓(2.1≈2.14); 환원 같은 결 |
| LPSCl(1.5) 환원 산물 = Li₂S+Li₃P **+LiCl** | [Ke], [GG], **[Lu]**, **[Liu23]** | comp1/modelc 0V → Li₃P+Li₂S+**LiCl** | **✓ 동일 chemistry** ([Liu23]도 PS₄→Li₂S+Li₃P) |
| **Li₆PS₅X 환원전위 1.7 V vs Li → Li₃P+Li₂S+LiX (passivation)** | **[Rupp]** Table 3 (in-situ XPS+EIS) | comp1/modelc 환원 1.24 V → Li₃P+Li₂S+LiCl | **✓ 동일 chemistry**, 전위 절대값은 방법차(우리 0-pressure vs 인용 indirect/실험). **LiX=LiCl이 passivation 산물** = modelc Cl-rich 이점 단서 |
| **도핑 route**: PS₄³⁻의 Li-유발 redox 분해를 **Mg(s-p 혼성, S 전자풍부→전자이동 차단)+F(in-situ LiF 절연층)** 로 억제 (MgS₄는 무분해) | **[Liu23]**(MgF₂), [Ke](MgClO) | modelc 환원산물 = 그들이 억제하려는 분해산물 | 별도 축(조성 아닌 *도핑*); cascade 동기 |
| interphase **LiCl = 전자절연(gap 6.22) + 저Li⁺장벽(0.05) + 연성(Poisson 0.23)** → 좋은 buffer | **[Lu]** Fig6 | modelc가 LiCl 생성 → Lu의 "good passivator"로 해석 | **✓ 우리 LiCl 산물에 의미 부여** |
| **in-situ LiF-rich SEI(액체 처방 FEC→LiF)가 SE 분해(Li₂S) 억제 → 균일 Li flux·dendrite 억제** (XPS F1s 684 / S2p Li₂S↓; overpot 154→55 mV; CCD 0.8→1.5) | **[KimICCF]** Fig 5 | comp1/modelc native 환원산물 = Li₂S/Li₃P/LiCl (그중 Li₂S=전자전도 우려) | **🔑 = 우리 'electron-blocking interphase' 메커니즘의 실험 카운터파트**. 우리 DFT=어떤 산물이 절연(LiF/LiCl/Li₂O/Li₃PO₄/NdPO₄), 이들=그 절연 SEI를 액체 처방(FEC)으로 **in-situ 형성**. LiF·LiCl·Li₂O·Li₃PO₄ = wide-gap 절연 패밀리 일관. ⚠ σ_e 실측 아님(간접추론) |
| **Nolan Type 1/2/3 Li/SE 계면 분류** (1=열역학안정 passivating / 2=MIEC 성장형 / 3=전자절연 kinetic SEI) | **[Kang]** Fig5c (Nolan ref47) | comp1/modelc 환원산물 Li₃P+Li₂S+LiCl → **Type 3 목표**; sei_products.json gap 분류(insulator≥4/marginal2–4/conductor<2 eV) | **🔑 = 우리 SEI 전자절연 논리의 표준 프레임**. 우리 gap 임계 = Type 분류의 *정량판*. Nd cascade = "conductive Li₃P(0.70)를 wide-gap Li₂O(5.24)/Li₃PO₄(5.73)로 → Type3 강화" |
| **dendrite는 *환원 SEI*의 전자구조가 좌우(pristine bulk 아님)** | **[Kang]** Fig6c (Hao ref90 계산) | 우리 bulk σ_e(gap 2.07 wide insulator)만; SEI 산물 gap은 sei_products.json | **✓ bulk σ_e 한계 명시** — dendrite 진짜 레버는 SEI 전자절연성(우리 sei_products.json) |
| 계면E Li/LPSCl −2.68 ≪ LiCl/LPSCl −0.19 J cm⁻² (LiCl buffer가 Li-S 자발반응 차단) | **[Lu]** Fig6a | 우리 계면 slab 미계산(gap H) | 차용 가능 |
| **[Lu] 견해**: 4d-Cl 90 % 자기분해 → LiCl passivation → **Cl-rich가 음극 유리** (CCD 0.96, 800h) | **[Lu]** | modelc Cl-rich, 4d 점유↑ 추정 → 부합 | Cl-rich ✓(조건부) |
| **[GG] 견해**: 과안정 LPSCl1.5는 self-limiting ✗ → **moderate Cl(1.0)이 유리** (다층 전략) | [GG] | — | Cl-rich ✗ |
> **🔑 화해 (정직)**: 같은 LPSCl1.5인데 [Lu]는 "Cl-rich 유리", [GG]는 "moderate 유리"로 정반대. 둘 다 **"전자절연 passivation(LiCl) 형성 = dendrite 억제 관건"** 엔 동의. 차이는 **Cl '양'이 아니라 Cl '자리(4d)'**: [Lu]의 high-4d-Cl은 metastable(E_hull +15.2)이라 자기분해→LiCl, [GG]의 조성-평균 관점은 이 자리 불안정성을 못 봄. → **deck 결론: "음극엔 Cl-rich 무조건 유리 ✗ / 전자절연 LiCl interphase 형성되면 ✓, 형성 여부는 4d-Cl 점유가 좌우"**. (상세 = `papers/lu2025_tailoring_cl_rich_anode_licl.md` §13)

## F. 도핑 (계면 전자구조 엔지니어링)
| 주장 | 출처 | 우리 연결 |
|---|---|---|
| MgClO(Mg+Cl+O) 공도핑 → 계면 metallic→gapped (s-p/p-p 혼성) → 환원 분해 차단 | [Ke] | **우리 cascade(Mg/Cl/O/F 도판트 스크리닝)의 직접 문헌 동기 ①** |
| **MgF₂(Mg+F) 공도핑** → 음극 redox 억제(실험: CCD 0.6→1.4, σ_e 8×↓). ⚠메커니즘("MgS₄ 사면체 s-p 혼성, Mg@P자리")은 **구조모델 under-determined**(lab XRD로 Mg@P vs Mg@Li 구분 불가, 자기 ELF는 이온결합, 반경상 Mg→Li) → `papers/liu2023…md` §12b | **[Liu23]** | cascade 동기 ②는 **실험적 방향**(Mg 도핑이 음극 도움)만; *기전*은 미확정으로 인용 |
| SEI = 전자절연(Li₂O 8.37 eV)+친리튬(LiMg) | [Ke] | 우리 **Li₃N**(음극 interphase) 연구와 같은 패밀리 |
| 도판트 음극 호환성 descriptor: 계면 binding energy(J/m²), E_F metallic 여부 | [Ke] | 우리 cascade 평가에 차용 가능 |
| **음이온 자리(4d) Cl 점유 엔지니어링** → 자기분해 LiCl interphase (원소도핑 아닌 *자리* 레버) | **[Lu]** | modelc Cl-rich의 4a/4d 분포 명시하면 Lu와 직접 연결 |
| **interphase 품질 descriptor 3종**: 전자 gap 넓음 + Li⁺장벽 낮음 + Poisson 연성 | **[Lu]** Fig6d | Ke binding-E와 묶어 음극 interphase 평가셋 완성 |
| **O²⁻ 옥시설파이드 도핑(Li₆PS₄OCl/Li₆.₂₅PS₄.₂₅Cl₀.₇₅): 전자누출↓·ECW확대·O–P>S–P·대기내성↑·기계순응 SEI** | **[Kang]** §5.1(b) Fig13c,d (refs128–130) | **우리 Nd2O3/O-doping cascade** (sei_products.json: Li₃PO₄ 5.73·Li₂O 5.24·NdPO₄ 5.55 eV가 Li₃P 0.70 대체; eos modelc_nd B0 18.9) | **🔑🔑 우리 cascade의 리뷰 내 직접 정당화**. 리뷰 "reduced electron leakage" = 우리 wide-gap O-derived 산물 정량. ⚠ 우리 hull: intrinsic 창 narrows(kinetic passivation) — 리뷰 CV ECW확대와 *다른 축* |
| **Li₃PO₄ buffer: CAM 산소방출 억제 + 기계약한 sulfate 형성 방지 + 고전압 parasitic↓** | **[Kang]** §5.1(c) Fig13e (ref128) | Nd cascade: Li₃PO₄가 bulk-GB·cathode passivation으로 persist(0.69–3.06 V) | **✓ 동일 역할** (우리 직접 hull staircase가 실증) |
| **BH₄⁻ 도핑: CCD 2.6→7.3 mA/cm², 얇은 tri-layer SEI(Li₃P/LiBH₄/Li₂S) 기계순응·전자절연** | **[Kang]** §5.1(a) Fig13a,b (ref127) | (우리 미계산) — doping cascade 47종 스크리닝의 동기 | 우리 cascade가 "어떤 도판트가 전자절연 SEI를 주나" 예측하는 방향성 동기 |
| **"한 변수 고치면 다른 변수 바뀐다 → 통합 설계 필요"** (도핑이 σ·기계·ECW·SEI 동시 변경) | **[Kang]** §6 트렌드3 | 우리 **cascade v23**: stability↔Li-mobility blocking trade-off, 기계+안정성 동시 스크리닝(47 dopant) | **🔑 방법 일치** — 우리 cascade의 trade-off 설계가 곧 리뷰 "modifying one parameter alters others"의 계산 구현 |

## G. ✅ 우리 계산이 문헌을 *검증*하는 지점 (강점)
| 우리 결과 | = 문헌 | 출처 |
|---|---|---|
| **onset 반응 (LiS4 제외)** `Li6PS5Cl→Li3PS4+LiCl+S+2Li` | = **[Zuo] Eq1 정확히 일치** (2 e⁻, 원소 S) | [Zuo] |
| modelc onset `→Li3PS4+1.6LiCl+0.4S+0.8Li` | = [Zuo] Eq2 거동 (전자 적게·LiCl 많이) | [Zuo] |
| 0-pressure ESW (OCV 1.717, onset **2.256** LiS4 제외) | = K_eff=0 (1.70–2.40), 격차 0.14 V | [GG] |
| 구속 ESW Cl-rich 확대 trend | = K_eff=20 거동 | [GG] |
| AIMD Ea/D Cl-rich 빠름 | = 실험 σ trend | [GG][Zuo][Liu] |
| VBM = S 3p | = HAXPES | [Banik] |
| 환원 산물 Li₃P+Li₂S+**LiCl** (LiCl = 전자절연 passivator) | = LPSCl(1.5) 환원; LiCl이 음극 passivation | [Ke][GG][**Lu**][**Liu23**] |
| **"electron-blocking interphase가 분해 차단" 메커니즘** (우리 중심 주장) | = **LiF-rich SEI가 SE 분해(Li₂S) 억제** (실험 XPS) → 같은 그룹이 실험 입증 | **[KimICCF]** ⭐ |
| **"σ 병목 = interphase/microstructure, bulk 결정 아님"** | = 시트 σ 손실 원인 = 공동(34.2 %), 채우면 155 % 회복 | **[KimICCF]** ⭐ |
| **O-doping interphase가 전자절연(wide-gap)으로 e⁻ leak 차단** (우리 Nd cascade) | = §5.1(b) 옥시설파이드 "reduced electron leakage"·O–P>S–P; §5.1(c) Li₃PO₄ buffer | **[Kang]** ⭐ (우리 그룹 리뷰가 직접 전략으로 추천) |
| **SEI 전자절연성 = passivation/dendrite 억제 관건** (sei_products.json gap 분류) | = Nolan **Type1/2/3**(Fig5c); dendrite는 환원 SEI 좌우(Fig6c) | **[Kang]** ⭐ (개념 프레임; 우리가 gap 수치로 정량) |
| **산화 onset = grand-potential(thermo), 실험창은 kinetic** | = Fig1a(ref49 동일방법)·Fig1b thermo vs kinetic ECW | **[Kang]** ⭐ |
| **고전압 산화분해 산물 = P₂S₅계 + 원소 S + LiCl** (우리 voltage-resolved staircase) | = **식1** `2Li₆PS₅Cl→P₂S₅+5S+2LiCl+10e⁻+10Li⁺` (완전산화) → NCM 균질 chemical lithiation | **[Kang25]** ⭐ (우리 그룹 실험이 우리 grand-potential 분해화학을 간접 검증; 단 이로움=SOC-강하≠passivation, Nd와 다른 physics) |
| **bare NCM-LPSCl 분해산물 = phosphate + P₂Sₓ + Li₂S** (우리 산화 staircase·interface_reactivity) | = post-mortem XPS(P 2p phosphate·P₂Sₓ, S 2p Li₂S) bare NCM cycling 후 | **[Cha]** ⭐ (우리 그룹 실험이 우리 분해화학 간접 검증; **단 LZC dual-compat=Zr⁴⁺ passivation은 Zr 우리 hull 부재로 *아직* 미정량** → 향후 Zr hull) |
| **dual-compatibility(코팅이 두 상 모두와 무분해)를 voltage별 정량** = `GrandPotentialInterfacialReactivity` 도구의 적용대상 | = LIC/LYC/LZC × {NCM, LPSCl} 6계면 호환성(LZC만 dual) | **[Cha]** ⭐ (우리 도구가 *왜 Zr⁴⁺만 견디나*를 in-silico 재현 가능 = 우리 그룹 실험을 우리 DFT가 *검증·확장*할 미래 지점; **현재는 Zr hull 없어 미실행**) |

## H. ⚠️ 우리가 아직 못 하는 것 (정직 목록 → 향후)
| gap | 누가 필요로 함 | 보강책 |
|---|---|---|
| 기체상(SO₂/O₂) 포함 계면 분해 | [Zuo] R_int 메커니즘 | 기체 chempot + NCM O-release |
| 무질서 E_above_hull (metastability) | [Zuo] DSC/TGA, [Wu] | SQS/enumerate E_hull |
| **시트/펠릿 microstructure σ(공동·percolation) — 우리는 bulk 단결정 AIMD만** | **[KimICCF]** (device σ ≠ bulk σ) | **GeoDict digital-twin**(GrainGeo+ConductoDict, contact 0.07 + biphasic 0.08 Ω·cm²) = bulk↔device σ 다리 |
| 음극 in-situ SEI *실측* 산물·전자절연성 | **[KimICCF]** XPS LiF/Li₂S | 우리 grand-potential 환원산물 예측의 실험 카운터파트(이미 [KimICCF]가 제공) |
| ~~LiS4 제외 ESW~~ ✅ **완료 (2026-06-23)** | [GG] phase set | onset 2.256 V, comp1 rxn=Zuo Eq1 정확 일치 (`our_dft_baseline.md` §ESW 상세) |
| 구속 ESW 절대값(full Lagrange) | [GG] K_eff=20 정량 | constrained_esw 2nd-order |
| defect/σ_e 정량 | slide25 틀 | Freysoldt defect calc |
| slab IP / absolute VBM | UPS 절대 기준 | slab+vacuum |
| **Zr 포함 hull (할라이드 코팅 LIC/LYC/LZC dual-compatibility 정량)** | **[Cha]** ⭐ (LZC=Li₂ZrCl₆ vs NCM/LPSCl 6계면) | Zr 추가 chemsys(Cl-Li-Zr-…)로 `GrandPotentialInterfacialReactivity` voltage-resolved — 왜 Zr⁴⁺만 견디고 In/Y는 분해하나 in-silico 재현 |

---

## 🗨️ Q&A 로그
> 슬라이드·결과를 보며 나온 질문/답 누적. "Q&A 작성해줘" 트리거.

### Q1 · 2026-06-23 · LPSCl vs LPSCl1.6 산화안정성 누가 더 좋나? "우리 동일"과 문헌이 다르면 이유? (slide 27 ESW)
**한 줄 답**: 단일 승자 없음 — **축을 명명**해야 함. 우리 "동일"은 intrinsic onset(B①) 한정 정답, 문헌의 "다름"은 우리 ESW가 안 보는 다른 축(B②③④).
- 우리 grand-potential ESW = **intrinsic 0-pressure onset**. 첫 산화 S²⁻→S₂²⁻(황)는 두 조성 공유 → 조성 무관 = 동일. [GG] K_eff=0이 검증.
- "Cl-rich 덜 안정"([Zuo] CV·DSC/TGA) = (a) 무질서 metastability(우리 ideal 밖), (b) kinetics/접근성(2×≈σ비 2.4×), (c) CV apparent onset. **열역학 onset은 동일**([Zuo] "same peak potentials").
- "Cl-rich 더 안정"([GG] 구속, [Zuo] 계면) = B②③, 우리 0-pressure가 구조적으로 제외.
- **결론**: intrinsic 무승부 / 계면 Cl-rich 우위([Zuo]) / shelf-life Cl-rich 열위([Wu]). 축 명명 필수.
연결: §B · `our_dft_baseline.md` · `papers/zuo2022_chlorination_cathode_interface.md` §11 · `papers/gilgonzalez2022_synergistic_cl_constricted_esw.md` §10.

### Q2 · 2026-06-23 · CDD 색이 직관과 반대로 보이는 이유 (Li 노랑 / S²⁻ 파랑 / Cl⁻ 무색)
**원리**: CDD `Δρ=ρ_SCF−ρ_atom` 기준은 **중성 자유원자**(이온 아님). 색 = "중성원자 대비 증감", **절대 전하 아님**.
- **Li⁺ → 노랑(축적)**: 2s를 내주면 남은 **1s 코어가 가림↓로 수축** → 핵 위 밀도↑ (PP가 1s 가전자 포함, zval=3). 데이터: 핵 위 +0.044.
- **free S²⁻ → 파랑(결핍)**: 2e⁻ 얻지만 **soft → 구름 바깥 팽창** → 중성 S(compact) 대비 안쪽 결핍. 얻은 전자는 diffuse 바깥(+0.001, 등치면 미달→안 보임). 데이터: 핵 −0.004 / 바깥 +0.001. (lone pair는 ELF에서 노랑, CDD에선 중성도 3p 있어 안 부각)
- **Cl⁻ → 무색(≈0)**: 중성 Cl(3p⁵)≈Cl⁻(3p⁶), 전자 1개 차 + **hard/compact 3p(고전기음성도)라 팽창 거의 없음** + P–Cl 공유결합 없음 → |Δρ|~0.001(최약) → 구름 없음.
- **P–S → 노랑(P쪽)+파랑(S쪽) 짝**: 공유결합 재배치(강한 신호).
**한 줄**: CDD = 절대 전하 아니라 **중성원자 대비 재배치** → Li 수축(노랑)·S²⁻ 팽창(파랑)·Cl⁻ 무변화(무색)·P–S 공유(짝).
연결: `our_dft_baseline.md` · slide 24(CDD) · `papers/zuo2022_chlorination_cathode_interface.md`(분해화학).
