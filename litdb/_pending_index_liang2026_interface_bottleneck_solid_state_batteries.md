# ⏳ pending — `liang2026_interface_bottleneck_solid_state_batteries` 의 INDEX / comparison 반영분
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09, litdb-curator. **이번 세션은 `INDEX.md` · `comparison_vs_ours.md` 직접 수정 금지** 지시라
> 아래 블록만 만들어 둔다. **사람이(또는 조율 세션이) 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/liang2026_interface_bottleneck_solid_state_batteries.md`
> 그림: `litdb/figures/liang2026_interface_bottleneck_solid_state_batteries/` (**PNG 6장 = 본문 Fig 1–6 전부. SI 없음. 표 0개**)
>
> ✅ **서지 확인함 (의뢰서 추정이 맞았다, 단 저자 수 정정)**: 표지 —
> S. Liang, Z. Xu, M. Sun, Q. Lu, T. Wu, B. Chen, Z. Li, **Z. Zhou, L. Lu, O. Minchukova,
> G. Rymski, A. Zhaludkevich, B. Huang\***, "Overcoming the Interface Bottleneck in Solid-State
> Batteries: Electrolyte Design, Interface Engineering, and Computational Discovery",
> ***Battery Energy* 2026; 5:e70137**, DOI `10.1002/bte2.70137`, CC-BY.
> ⇒ slug `liang2026_interface_bottleneck_solid_state_batteries` **그대로 확정.**
> ✏ 의뢰서의 *"Z. Li 외"* → 실제로는 **저자 13인**이고 뒤 5인이 **벨라루스 과학아카데미** 소속이다.
>
> ✅ **PDF 2개 판정**: `f7870077-…` 와 `643be538-…` 은 **sha256 동일**
> (`7c884b0d49a406f185ca61fce1d00b65a59dd8a267e81e48b9878dd17e88913b`), 크기 2,672,869 B, 18 pp 동일.
> ⇒ **완전히 같은 파일.** 정본 = `f7870077-…`. 차이 없음.
>
> ✅ **talk 역링크 점검함**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` →
> `litdb/talks/lee2026_skku_mlip_materials_design.md` 하나뿐이고, **이 논문은 그 대기열에 없다**
> (그 큐는 MTP/SevenNet/SKKU 계열). ⇒ **역링크 작업 없음.**
> 단 그 큐의 **#4 Merchant2023 GNoME** 를 이 리뷰가 `[93]` 으로 인용하고 `Fig. 6k,l` 로 재수록한다 — 교차참조만.
>
> ⭐ **부수 소득**: 이 리뷰의 `Fig. 6a–f` 원전 **[91]** 은 우리가 **이미 digest 해 뒀다**
> (`papers/qian2025_lipo2f2_coating_stable_cei.md`, INDEX 25행). 두 세션의 figure-read 가
> **8/9 항목 일치**(2.8 V 최소만 −47 vs 원전 −43). ⇒ **`Fig. 6` 인용은 리뷰가 아니라 qian2025 로.**

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

```markdown
| `papers/liang2026_interface_bottleneck_solid_state_batteries.md` | **[외부·**리뷰(2차 인용 전용)**·⛔ 물성 4축(A–D) 비교 전면 제외 · ★ 계면·개관 축 J-12 + ★★ "도핑=개선" 전제 반증 조사]** ✅ **Shipeng Liang·Zhehan Xu·Mingzi Sun·Qiuyang Lu·Tong Wu·Baian Chen·Zikang Li·Ziqi Zhou·Lu Lu**(홍콩城市大 화학) + **O. Minchukova·G. Rymski·A. Zhaludkevich**(벨라루스 과학아카데미 재료연) + **Bolong Huang\***, "**Overcoming the Interface Bottleneck in Solid-State Batteries: Electrolyte Design, Interface Engineering, and Computational Discovery**" (***Battery Energy* 2026, 5:e70137**, DOI 10.1002/bte2.70137, CC-BY; 접수 2026-06-03/수락 **2026-06-18 = 15일**; 본문 **18 pp · Fig 1–6 · Table 0개 · SI 없음 · refs 110**). ⚠ **Bolong Huang 은 *Battery Energy* 편집장이자 공저자**(논문이 자진 공개, 편집 결정 배제). **자체 계산·실험 0건 — 모든 수치가 소환값.** **★ 이 편을 먹은 이유 = Scholar 스니펫의 *"aliovalent doping … lowering the ionic conductivity relative to pristine Li₆PS₅Cl"* 가 우리 cascade 의 "도핑=개선" 전제를 반증하는지 확인하려고.** **🔴 판정 ①: 그 스니펫은 논문에 없는 문장이다 — 세 곳을 이어 붙인 것.** 「exquisitely sensitive to aliovalent doping」은 **p.2 §2.1 LLZO(산화물)** 이고 거기서 도핑은 **σ 를 올린다**(Zr⁴⁺→Ta⁵⁺/Nb⁵⁺/W⁶⁺/Te⁶⁺ 로 Li 빈자리 → **1–2×10⁻³ S cm⁻¹**); 「lowering the ionic conductivity…」는 **p.4 §2.2 Y-도핑 Li₆PS₅Cl(황화물)**; 「high-throughput screening rapidly explored」는 **p.5 §2.3 반-페로브스카이트**. **🔴 판정 ②: σ-하락 주장에 인용이 없다** — `[32]`(D. Wang et al., *Angew* **64**, e202501411, 2025)는 **바로 앞의 사이클 성능 문장**(대칭셀 >4800 h·풀셀 1300 cyc·유지 100 %)에 붙어 있고, *"stronger Y–S bonding … contracts the local coordination environment … typically lowering the ionic conductivity"* 블록 **전체가 무출처 = 리뷰 저자의 논평**. **🔴 판정 ③: 숫자가 없다** — Y 의 **자리·농도·배수·절대값 전부 미기재**, 부사 `typically` 뿐. 도핑창도 *"insufficient ↔ excessive(Y₂S₃ 입계 석출)"* 정성뿐. ⇒ **"도핑이 σ 를 낮춘다"를 이 리뷰로 인용 불가. `[32]` 원문 확보가 전제.** **🔴 판정 ④: σ 를 *올리는* 사례가 9건 대 1건으로 압도**(LLZO aliovalent · Ga/Al@Li · **high-entropy argyrodite Si/Ge/Sn@P+Cl ≈8 mS/cm [26]** · Yb³⁺ bottleneck 최적화 [35] · **F-도핑 가넷 GB [74]** · medium-entropy 가넷 **1.52×10⁻³** [81] · **Li₃Ta₃O₄Cl₁₀ 옥시할라이드 13.7 mS/cm·4.9 V [106]** · high-entropy 클로라이드 4.6 V 5000 cyc **91.9 %** [107] · 반-페로브스카이트 ML [38]) — **그리고 숫자는 올리는 쪽에만 있다.** **가르는 기준**: 리뷰가 **규칙으로 선언하지 않는다.** 명시된 것은 원리 한 줄(*"highly polarizable, weakly binding anionic framework 가 Li⁺ 수송을 돕고 산화문턱을 낮춘다"* §5.1)이고, 사례를 놓고 보면 **σ↑ 9건은 캐리어/빈자리·자리에너지 분포 폭·bottleneck 크기를 겨냥**했고 **σ↓ 1건은 전자구조를 겨냥**했다(=이온 부분계는 부작용) — **문턱·기술자·판정식 없음.** **★6 파이프라인 감사(Basu26 형 "탈락 0" 검사)**: 소개된 **9개 파이프라인 중 문턱을 밝힌 것 1개**(`[100]` H. Liu, *J. Power Sources* **658**, 238376: Extra Trees + **168 순수 → 149,480 도핑후보 → 963 생존(0.64 %)**, 필터 **σ>10⁻⁴ S/cm · gap>4 eV · E_hull<50 meV/atom · tolerance factor**, ⚠ **필터별 분해 없음** 그리고 리뷰가 **"jointly filtering"** 이라 명시 = 순차 게이트가 아니라 **동시 교집합** ⇒ 단별 탈락 수가 애초에 정의 안 됨), **생존 수만 밝힌 것 1개**(`[93]` GNoME **2.2 M → 384,000 → 736 실험확인**, 문턱 미기재), **단별 탈락 수를 밝힌 것 0개** ⇒ **이 리뷰로는 Basu 형 병리를 진단할 수 없다(원문 필요).** 다만 GNoME 의 **r²SCAN 재검증 84 % stable / 16 % unstable**(`Fig. 6l`)은 후보 선별이 아니라 **사후 재채점**이라는 점에서 Basu Tier 2/3 와 같은 층위. **★7 계면 정량**: 쓰는 것 5종 = ① **대전위 pseudo-binary ΔE_rxn(meV/atom, 전위 고정)** ② ESW ③ **CCD/임계 스트리핑 전류** ④ 면적비저항 ⑤ XPS Clₓ⁻ 면적. **⛔ 슬랩 규약은 한 줄도 없다** — 전수 키워드 스캔 `slab` 0 · `vacuum` 0 · `termination` 0 · `mismatch` 0 · `work of adhesion`/`W_ad`/`adhesion` 0 · `surface energy` 0 · `supercell`/`k-point`/`cutoff` 0, `strain` 실질 2회(둘 다 계면규약 아님), **`interfacial energy` 2회는 둘 다 오귀속**(§10-2). ⇒ **우리 B2(계면) 🔴 미정의 에 정의를 주지 않는다.** 주는 것은 ⓐ *"grand potential phase diagram 이 **the standard** tool"* 이라는 관행 확인 ⓑ **같은 코팅재가 상대(LPSCl/NCM)×전위(0/2.8/4.3 V) 6조합에서 −47~−395 meV/atom 으로 8배 흩어지고 산물도 매번 바뀐다** ⇒ **"코팅재 X 의 계면안정성"은 스칼라로 정의되지 않는다**(estimand_card 판정기준에 걸림). **📊 소환 수치**(전부 2차): LGPS **12 mS/cm**[24 Kamaya2011] · LPSCl **3–5** / LPSBr **6–8** / LPSI **~1 mS/cm** ⚠**셋 다 무출처, LPSI 는 통상치보다 2–3 자릿수 높다 — 근거로 쓰지 말 것** · 황화물 DFT 산화 **2.1–2.5 V** vs 실셀 **3.5–4.2 V**(속도론적 부동태화)[28] · 할라이드 **>4.3 V**[37] · 국소왜곡 **4.25→4.4 V**[36] · **임계 스트리핑 전류 0.2 mA/cm² @3 MPa (Li\|LPSCl\|Li)**[59 Kasemchainan2019] · 임계 플레이팅 LLZO ≈0.6 / LPSCl 0.2–1.0 mA/cm²[70] · 황화물 E **20–40 GPa** vs LLZO ~150[무출처] · 스택압 최적창 황화물 **3–10** / 할라이드 **5–20** / 가넷 **~0–30 MPa**[81,82] · Li\|LLZO 고유 전하이동저항 **~10⁻¹ Ω cm³**(⚠단위 원문대로)[82–85 Krauskopf] · SCL **10–50 nm**[21] · Li₂CO₃ **5–10 nm**[19] · LLZO GB σ **벌크의 1/10²–1/10³**[18]. **⭐ 우리 조성 직접 등장 1회**: *"sulfide electrolytes (**Li₅.₄PS₄.₄Cl₁.₆**) form a redox-active interphase enabling reversible cycling"*(p.11, Al 음극 대비) ← **[88]** J. Cui et al., *ACS AMI* **17**, 22014 (2025) = **우리 modelc 조성의 계면 실험 문헌 — 확보 대상**. **✅✅ 우리와 가장 강한 접점**: **[72]** Han et al., *Nat. Energy* **4**, 187 (2019) *"**high electronic conductivity, rather than mechanical properties, is the root cause of internal dendrite formation**"* ← 우리 modelc PDOS v2 의 *"CBM 에 Li 기여 무시 가능(S 3p 반결합+P 3s) ⇒ 전자환원이 Li 자리에서 핵생성 안 함"* 의 **문헌 받침**. **⚠ 결함 실측 8건 / 18 pp**: ① 핵심 정량 진술 다수 무출처 ② **`Fig. 6l` 축이 "Phase-separation energy" 인데 본문은 "interfacial energies" 라 부른다 — 리뷰에서 "interfacial energy" 가 나오는 유일한 자리가 오귀속**(Merchant [93] 은 계면에너지를 계산한 적 없다) ③ **`Fig. 5b` 가 본문과 안 맞는다** — figure-read 1000/T=3.3 에서 pristine ln(σT)≈**−7.90** ALO10≈**−7.45** ⇒ **비 ≈1.6×** 인데 본문은 **×2.7 (2.59→6.92×10⁻⁴ S/cm)**, 게다가 ln(σT)≈−7.5 는 σ~10⁻⁶ S/cm 급이라 **3 자릿수 어긋남** ⇒ **두 값 다 인용 금지** ④ **`Fig. 4a` 비단조성을 본문이 침묵** — 그림은 **pristine 0.15 / ALO5 0.25 / ALO10 0.45 / ALO20 0.35 mA cm⁻²** 인데 본문은 양 끝 두 개만 인용, **ALO20<ALO10 = "더 두껍게 하면 도로 나빠진다"를 안 적는다** ★우리 3점 평균 관행의 반면교사 ⑤ `Fig. 2a` 의 5 nm(20 µm bar) vs 10 nm(1 µm bar) 배율이 20배 달라 본문의 두께 비교를 그림으로 확인 불가 ⑥ 면적비저항 단위가 **Ω cm³** (2회) ⑦ `Fig. 2a` 는 **Li(음극) 계면 연구인데 §3.1 양극 계면 절에 배치** ⑧ `Fig. 6` 캡션 `(e)` 중복 + *"American **Society** of Chemistry"* 오기(2회). **📌 그림 6장 전부 크로핑·전부 육안 판독**(SI 없음, 표 0개; 2단 조판이지만 그림이 전폭+캡션 하단이라 크로핑 오차 0). **✅ 원전 교차검증**: `Fig. 6a–f` 원전 `[91]` = **우리가 이미 보유·digest 한 `qian2025_lipo2f2_coating_stable_cei`** — 두 세션 figure-read **8/9 일치**(LiPOF 창 2.6–4.9 V · 무전위 −145@x≈0.5 → Li₃PO₄+LiF+LiCl+P₂S₅ · 4.3 V −95/−96@x≈0.07 · NCM 2.8 V −395 · 4.3 V −108), **2.8 V 만 −47 vs 원전 −43**. ⇒ **`figure-read ≈` 표기의 재현성 실측치 ±1–4 meV/atom**, 그리고 **리뷰는 원전이 가진 정보를 잃는다**(x=1.0 LPSCl 자체분해 −83 meV/atom → Li₃PS₄+Li₂S+LiCl = **우리 `interface_reactivity_results.json` x=1 kink 와 문자 그대로 일치**하는 대목, SOCl₂ 의 속도론 배제, 게이트 \|ΔE_rxn\|<100 meV/atom 을 **전부 안 옮긴다**) ⇒ **`Fig. 6` 은 리뷰 말고 qian2025 를 인용한다.** **★8 리뷰가 "아직 모른다"고 적은 것 12건** — 대표: *"no inorganic SSE has yet demonstrated dendrite-free plating at >5 mA cm⁻² and >5 mAh cm⁻²"* · *"whether grain boundaries should be amorphous or crystalline remains actively debated"* · AIMD 는 *"sufficient for screening but insufficient for quantitative prediction"* · 다가이온 계면 *"mechanistic understanding remains limited"* · ★ *"This interface-centric paradigm demands continued investment in the **first-principles modeling of interface thermodynamics** and the atomic-scale understanding of interfacial ion transport"*(= **우리 B2 작업의 정당화 문장**). **⛔ 우리 규율**: 이 리뷰 값은 `canonical_registry.json`·`cascade_stability_axes.csv` 에 **넣지 않는다**. 그리고 **이 리뷰의 도핑 논의를 `cascade_stability_axes.csv` 에 연결하지 않는다** — 그 CSV 는 **코팅 후보** 데이터이지 도핑체가 아니다(`kb/reviews/codex_BJ_prompt_cascade_redesign_2026_09_09.md` 철회블록) | **축 J-12(계면·개관·리뷰) · ⛔ 물성 4축(A–D) 비교 제외** — cascade 순위 규칙(host 앵커) 재설계의 문헌 근거 |
```

---

## ② `litdb/comparison_vs_ours.md` — **§📑 Reference key** 에 추가할 줄

```markdown
| **[Liang26IF]** | **S. Liang**/Z.Xu/M.Sun/Q.Lu/T.Wu/B.Chen/Z.Li/Z.Zhou/L.Lu/**O.Minchukova**/**G.Rymski**/**A.Zhaludkevich**/**Bolong Huang\*** 2026 ***Battery Energy* 5, e70137** (홍콩城市大 화학 + 벨라루스 과학아카데미 재료연; DOI 10.1002/bte2.70137, CC-BY; 접수 2026-06-03/수락 2026-06-18) — "**Overcoming the Interface Bottleneck in Solid-State Batteries: Electrolyte Design, Interface Engineering, and Computational Discovery**", 본문 18 pp·Fig 1–6·Table 0·SI 없음·refs 110. **자체 계산·실험 0 → 전 수치가 소환값(2차 인용).** ⚠ **교신저자가 이 저널 편집장**(자진 공개·편집 배제). ⚠ **결함 8건/18 pp**(무출처 정량 다수 · `Fig. 5b` ↔ 본문 σ 비 1.6× vs 2.7× · `Fig. 4a` 비단조 침묵 · `Fig. 6l` "interfacial energy" 오귀속 · Ω cm³ 단위). **쓰는 곳 = 축 J-12(계면·개관) 하나.** ★ 소득 3: ① **Scholar 스니펫 "aliovalent doping 이 σ 를 낮춘다"는 이 논문에 없는 문장**(LLZO 절 + 황화물 절 + 할라이드 절 3곳 접합) ② **σ-하락 주장은 무출처 논평이고 숫자가 0개** ③ **슬랩·W_ad·strain 배분 규약 전수 0회** ⇒ B2 정의 안 줌 | ✅ `papers/liang2026_interface_bottleneck_solid_state_batteries.md` | **review · 소환값 전용 — ⛔ 물성 4축(A–D) 수치 비교 제외.** 축 정의·관행 확인·gap 문장 재료로만 |
```

---

## ③ `litdb/comparison_vs_ours.md` — **§J-11 다음에 넣을 새 절 `### J-12`** ★ (여기가 본체)

> ⚠ **왜 A–D 물성 4축이 아닌가**: CLAUDE.md/curator 규율 —
> *"방법론 원전(물성값이 없는 편)은 물성 4축 표에 넣지 않는다."* 이 논문에는 **우리 계의 자체 측정·계산값이 0개**다.
> 소환값을 A·B·C·D 에 넣으면 우리 값과 섞인다. **A–D 어디에도 줄을 추가하지 않는다.**
> ⚠ 그리고 J-12 는 **J-10(깔때기 모양)·J-11(각 단의 판정 계약)과 층위가 다르다** — J-12 는
> **순위 규칙의 *기준점*(host 앵커)** 이다.

```markdown
### J-12. ★★★ **순위의 기준점 — [Liang26IF] "도핑이 σ 를 낮출 수 있다" vs 우리 G3/G4 앵커 비대칭** (2026-09-09 신설)

> 발주 질문: *"우리 cascade 는 '도핑=개선'을 암묵 전제한다. 이 리뷰가 그 반증인가?"*
> **답: 스니펫이 시사한 만큼은 아니다. 그러나 우리 게이트에 실재하는 구조적 결함 하나를 정확히 비춘다.**

#### J-12-1. 리뷰가 실제로 말한 것 (⛔ 스니펫과 다르다)

| 스니펫 조각 | 실제 절 | 물질계 | σ 방향 | 숫자 |
|---|---|---|---|---|
| "exquisitely sensitive to aliovalent doping" | **§2.1 (p.2)** | **LLZO 가넷** | ⬆ **올린다** | 1–2 × 10⁻³ S cm⁻¹ |
| "lowering the ionic conductivity relative to pristine Li₆PS₅Cl" | **§2.2 (p.4)** | **Y-도핑 LPSCl** | ⬇ 내린다 | ⛔ **없음** |
| "high-throughput screening rapidly explored" | **§2.3 (p.5)** | 반-페로브스카이트 | — | ⛔ 없음 |

- **σ↑ 사례 9건 : σ↓ 사례 1건**, 그리고 **숫자는 올리는 쪽에만 있다.**
- σ↓ 주장은 **인용이 없다** — `[32]`(Wang, *Angew* 2025)는 앞 문장(사이클 성능)에 붙어 있다.
- ⇒ ⛔ **"도핑이 σ 를 낮추니 후보를 줄이자"는 이 리뷰로 정당화되지 않는다.**

#### J-12-2. 🔴 그래도 남는 것 — 우리 게이트의 **앵커 비대칭**

| 게이트 | 정의 | host 앵커 |
|---|---|---|
| G3 oxidation | `ox_V ≥ **2.14 V (host)**` (`build_screening_funnel.py: HOST_OX_V`) | ✅ **있다** |
| **G4 li_transport** | `norm > 0.30`, norm = `("bvs_x005", **+1**)` 의 **도펀트 풀 내 min-max** (`build_cascade_themes.py:295`) | ❌ **없다** |

⇒ **깔때기는 host 앵커를 쓸 줄 안다. 이온수송 축만 안 쓴다.**
전원이 host 보다 나빠도 최상위는 norm 1.0 을 받는다. **리뷰의 Y 사례가 정확히 그 사각지대다.**
그리고 리뷰가 지목한 기구 — *"Li⁺ 확산채널 주변 **국소 배위환경의 수축**"* — 은
**우리 BVS proxy 가 재는 바로 그 양**이다. **관측량은 맞고 기준점이 없다.**

#### J-12-3. 요구 3가지 (근거 있는 것만)

| # | 요구 | 근거 | ⛔ 안 하는 것 |
|---|---|---|---|
| ① | G4 에 **host 참조 부호**를 넣어 `bvs_x005(dopant) < bvs_x005(host)` 인 후보에 **`σ-regression` 플래그** | ★1 (문헌에 σ 하락 사례 존재, 정성) | **탈락시키지 않는다** — 리뷰의 Y 사례도 4800 h 라는 이득을 같이 보고한다. 필요한 건 탈락이 아니라 **가시성**. **문턱 제안 안 함**(리뷰에 크기 없음) |
| ② | 도펀트마다 **`intent: ionic \| electronic \| mechanical \| interfacial`** 선언 → intent 축 이득과 타 축 손실을 같은 화면에 | ★4 (σ↑ 9건은 캐리어/무질서/bottleneck 겨냥, σ↓ 1건은 전자구조 겨냥). 우리 `combine` 은 기하평균이라 **부호 뒤집힌 trade-off 를 지운다** | **교환율 제안 안 함** (리뷰에 근거 0) |
| ③ | 농도 3점(x=0.02/0.05/0.10)을 **평균하기 전에 단조성 검사**, 비단조면 `argmax` 병기 | **문헌 실측**: `Fig. 4a` **ALO5 0.25 → ALO10 0.45 → ALO20 0.35 mA cm⁻²** 비단조 + 본문이 침묵. ★1 의 *"insufficient ↔ excessive Y"* 창 | 이미 `audit_label_scatter.py` 가 재는 것 — **이 리뷰는 문헌 사례를 준다** |

#### J-12-4. ⛔ 이 축에서 인용하면 안 되는 것

- LPSCl **3–5** / LPSBr **6–8** / LPSI **~1 mS cm⁻¹** — **무출처**이고 **LPSI 가 통상치보다 2–3 자릿수 높다**
- LLZTO GB 개질 **×2.7** — 그림(`Fig. 5b`)이 **1.6×** 를 보이고 절대값이 3 자릿수 어긋난다
- "Y 도핑이 σ 를 N배 낮춘다" 류 — **숫자가 리뷰에 없다**
- 이 리뷰의 어떤 값도 `canonical_registry.json` · `cascade_stability_axes.csv` 에 **넣지 않는다**
- ⚠ **`cascade_stability_axes.csv` 는 코팅 후보 데이터이지 도핑체가 아니다**
  (`codex_BJ_prompt_cascade_redesign_2026_09_09.md` 철회블록) — **이 리뷰의 도핑 논의를 그 CSV 에 연결하지 않는다**

#### J-12-5. ✅ 반대로 이 축에서 **쓸 수 있는** 것

- *"DFT 2.1–2.5 V vs 실셀 3.5–4.2 V = 속도론적 부동태화"* **[28]** ← **우리 onset 2.256 V 가 이 대역 안**
  (⚠ *"같은 값"* 아니라 *"같은 대역"*. 리뷰는 상집합·압력·함수형을 안 밝힌다)
- *"high electronic conductivity, rather than mechanical properties, is the root cause of internal dendrite
  formation"* **[72]** Han 2019 ← **우리 modelc PDOS(CBM 에 Li 부재)의 so-what 받침**
- *"grand potential phase diagram 이 계면 열역학의 **the standard** 도구"* **[91]** ← **우리 T9 선택의 관행 근거**
- ★ gap 문장 재료 12건 (digest §14) — 특히 *"interface-centric paradigm demands continued investment in the
  **first-principles modeling of interface thermodynamics**"* = **우리 B2 작업의 정당화**
```

---

## ④ `litdb/comparison_vs_ours.md` — **§J-7 `🔧 방법 원전` 블록에 한 줄 추가**

> ⚠ J-7 은 이미 **[Wang26IF] 로 "W_ad 외부 앵커 없음"** 을 확정해 뒀다. 이 리뷰가 **세 번째 음성 결과**다.

```markdown
**[Liang26IF] `liang2026_interface_bottleneck_solid_state_batteries` — 계면 슬랩 규약 ⛔ 전무 (음성 결과)**

18 pp 전수 키워드 스캔: `slab` **0** · `vacuum` **0** · `termination` **0** · `mismatch` **0** ·
`adhesion`/`work of adhesion`/`W_ad` **0** · `surface energy` **0** · `supercell`/`k-point`/`cutoff` **0** ·
`strain` 실질 **2**(둘 다 계면규약 아님) · `interfacial energy` **2**(⚠ **둘 다 `Fig. 6l` 의 "phase-separation
energy" 를 잘못 부른 것**). ⇒ **2026년 계면 전문 종설이 슬랩 구성 규약을 한 줄도 다루지 않는다.**
**우리 B2 미정의는 우리 게으름이 아니라 분야의 공백**이라는 세 번째 증거
([Wang26IF] 계면 12개를 만들고도 W_ad 미산출 · [Qian26] γ_SE 0.40–0.72 J/m² 가 유일 DFT 앵커 · 여기).

**반대로 이 리뷰가 B2 에 주는 것 1개 (그림에서 읽은 우리 판단)**: `Fig. 6b–f` 는 **같은 코팅재**를
**상대(LPSCl/NCM) × 전위(0/2.8/4.3 V) 6조합**에서 각각 계산하고, 최소 반응에너지가
**−43 ~ −395 meV/atom (8배)** 로 흩어지며 **산물 조성도 매번 바뀐다**
(원전값 = `qian2025_lipo2f2_coating_stable_cei`). ⇒ **"코팅재 X 의 계면 안정성"은 스칼라로 정의되지 않는다.**
`kb/templates/estimand_card.md` 의 판정기준(*admissible state 가 여럿인데 선택·집계 규칙이 없으면
스칼라 보고량은 정의되지 않는다*)에 그대로 걸린다 ⇒ **B2 는 `ΔE_rxn(상대, 전위)` 로 인자를 선언한 뒤에야
보고량이 된다.** (리뷰가 이 말을 하지는 않는다.)
```

---

## ⑤ 후속 작업 제안 (사람 판단 필요)

1. **`[32]` D. Wang et al., *Angew* **64**, e202501411 (2025) 확보** — ★1 σ-하락 주장을 검증할 유일한 경로.
   지금 상태로는 우리 원고·덱 어디에도 그 주장을 쓸 수 없다.
2. **`[88]` J. Cui et al., *ACS AMI* **17**, 22014 (2025) 확보** — **`Li₅.₄PS₄.₄Cl₁.₆`(=modelc) 가 이름으로
   등장하는 유일한 계면 실험 문헌.**
3. **G4 host 앵커** — `bvs_x005` 를 무도핑 host 에 대해 **같은 파이프라인으로** 한 번 계산해야 한다
   (지금은 host 값이 없다). ⚠ **cascade 재설계가 Codex BJ 에서 NO-GO 상태**이므로
   이 제안은 **재설계 A′ 안에 넣을 항목**이지 지금 단독 착수 대상이 아니다.
