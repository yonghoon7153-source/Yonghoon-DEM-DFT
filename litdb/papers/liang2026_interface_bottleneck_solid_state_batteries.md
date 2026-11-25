# Overcoming the Interface Bottleneck in Solid-State Batteries: Electrolyte Design, Interface Engineering, and Computational Discovery — Liang et al. (*Battery Energy* 2026)

> slug `liang2026_interface_bottleneck_solid_state_batteries` · DOI `10.1002/bte2.70137` · type `review (2차 인용 전용)` · PDF `f7870077-103._Battery_Energy__2026__Liang…pdf` (= `643be538-…` 동일 파일) · digested `2026-09-09` · status ✅
> elements: Li, La, Zr, O, P, S, Cl, Br, I, Ge, Y, In, Yb, Ta, Nb, W, Te, Ga, Al, F, Si, Sn, Na, Mg, Zn, Ca, Ni, Co, Mn, Ti, B, Ba, Sc
> methods: DFT, AIMD, ESW, XPS
> ⚠ **`methods:` 는 이 리뷰가 *소개하는* 기법이다 — 리뷰 저자는 계산을 한 건도 수행하지 않았다** (§4).
> ⛔ **리뷰다. 이 파일의 수치는 전부 2차 인용이다.** 각 값에 원 출처(ref 번호 + 저자·연도·저널)를 붙였다.
> 우리 원장(`db/properties/*`)에 이식 금지. `comparison_vs_ours.md` 물성 4축(A–D)에도 넣지 않는다 — 방법·개관 축만.
> ✅ **talk 역링크 점검함**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md` 하나뿐이고 **이 논문은 그 대기열에 없다**(그 큐는 MTP/SevenNet/SKKU 계열). ⇒ 역링크 작업 없음. 단 그 큐의 **#4 Merchant2023 GNoME** 를 이 리뷰가 `[93]`으로 인용하고 `Fig. 6k,l` 로 재수록한다.

---

## 0. ★ 발주 질문 즉답 — Scholar 스니펫 판정

### 0-0. 🔴 먼저: **그 스니펫은 논문에 존재하지 않는 문장이다**

의뢰서에 인용된 Google Scholar 스니펫

> *"…is exquisitely sensitive to **aliovalent doping**. Substitution of … **lowering the ionic conductivity relative to pristine Li₆PS₅Cl** — a … design and high-throughput screening rapidly explored…"*

는 **한 문장이 아니라 세 곳을 이어 붙인 것**이다. 원문에서 서로 **다른 절 · 다른 물질계**에 있다.

| 스니펫 조각 | 실제 위치 | 실제 물질계 | 도핑의 σ 방향 |
|---|---|---|---|
| "exquisitely sensitive to **aliovalent doping**. Substitution of Zr⁴⁺ by…" | **p.2, §2.1 Oxide Electrolytes (Garnet-Type LLZO)** | **LLZO (산화물 가넷)** | ⬆ **올린다** (1–2 × 10⁻³ S cm⁻¹ 까지) |
| "…lowering the ionic conductivity relative to pristine Li₆PS₅Cl" | **p.4, §2.2 Sulfide Electrolytes** | **Y-도핑 Li₆PS₅Cl (황화물)** | ⬇ **내린다** |
| "…design and high-throughput screening rapidly explored…" | **p.5, §2.3 Halide Electrolytes** | **반-페로브스카이트 할라이드** | 언급 없음 |

⇒ **"aliovalent doping 이 σ 를 낮춘다"는 문장은 이 논문에 없다.** 있는 것은
**"Y 도핑(전자국재화 목적)이 LPSCl 의 σ 를 낮춘다"** 이고, 같은 논문이 바로 앞 절에서
**"aliovalent 도핑이 LLZO 의 σ 를 올린다"** 고 쓴다. 스니펫만 보고 "리뷰가 도핑=개선을 반증했다"
로 읽으면 **논문의 절반을 뒤집어 읽는 것**이다.

그래도 **우리 전제에 대한 반증 사례는 실재한다** — 아래 ★1–★5.

---

### ★1. 그 문장 통째로 (p.4, §2.2 Sulfide Electrolytes: LGPS and Argyrodite Systems)

> "In parallel, Wang et al. demonstrated a fundamentally different approach: electronic localization within the sulfide lattice. By introducing yttrium doping into argyrodite Li₆PS₅Cl, they created localized electronic states that prevent the long-range electron percolation responsible for electrolyte decomposition at the lithium anode, enabling stable cycling for over 4800 h in symmetric cells and 1300 cycles with 100% capacity retention in full cells **[32]**. This strategy reframes the stability problem, such that rather than engineering the interface alone, the bulk electronic structure of the electrolyte itself can be tuned to suppress degradation.
> **However, this electronic-localization strategy entails inherent trade-offs. The stronger Y–S bonding that pins electrons locally simultaneously contracts the local coordination environment around Li⁺ diffusion channels, typically lowering the ionic conductivity relative to pristine Li₆PS₅Cl—a manifestation of the fundamental stability-versus-conductivity dilemma. Furthermore, the doping level is tightly constrained: insufficient Y fails to disrupt the long-range electron percolation network, while excessive Y precipitates Y₂S₃-type impurity phases at grain boundaries that introduce resistive secondary interfaces.**"

(위치: p.4 왼쪽 단 하단 → 오른쪽 단, `§2.2` 마지막에서 두 번째 문단. 굵게 표시가 핵심 블록.)

### ★2. 어느 치환이 σ 를 낮추나 — 원소·자리·농도·배수

| 물음 | 리뷰가 적은 것 |
|---|---|
| 원소 | **Y (이트륨)** |
| host | Li₆PS₅Cl (argyrodite) |
| **자리** | **적혀 있지 않다.** "introducing yttrium doping into argyrodite Li₆PS₅Cl" 뿐 — P 자리인지 Li 자리인지 격자간인지 **명시 없음** |
| **농도** | **적혀 있지 않다.** 정성적으로 *"insufficient Y ↔ excessive Y"* 창이 있다고만 하고 **창의 값이 없다** |
| **얼마나 낮추나** | ⛔ **숫자가 하나도 없다.** 배수·절대값·Ea 변화 **전부 없음**. 부사 `typically` 만 붙어 있다 |
| 전하보상 | 언급 없음 |
| 과다 도핑의 부작용 | **Y₂S₃ 형 불순물이 입계에 석출 → 저항성 2차 계면** (정성) |

⇒ **★2 는 "리뷰에 없다"가 정답이다.** 방향(↓)만 있고 크기가 없다.

### ★3. 그 주장의 원 출처 — **없다** (이게 이번 조사의 가장 중요한 소득)

- 인용부호 `[32]` 는 **σ 하락 문장이 아니라 바로 앞의 *사이클 성능* 문장**(4800 h / 1300 cycles)에 붙어 있다.
- σ 하락을 말하는 **"However, this electronic-localization strategy entails inherent trade-offs…" 블록 전체에 인용이 하나도 없다.**
- ⇒ **이것은 리뷰 저자의 무출처 논평(unreferenced editorial commentary)이다.** 계산도 실험도 아니다.

참고로 `[32]` 자체는:
> **[32]** D. Wang, C. Liu, R. Wang, et al., "Electronic Localization Enables Long-Cycling Sulfides-Based All-Solid-State Lithium Batteries," ***Angew. Chem. Int. Ed.*** **64**, no. 19 (2025): e202501411.

리뷰가 `[32]` 에서 옮긴 것은 **실험 셀 성능뿐**(대칭셀 >4800 h, 풀셀 1300 cycles·용량유지 100 %).
`[32]` 원문이 σ 를 얼마나 낮췄다고 보고했는지는 **이 리뷰로는 알 수 없다** — 확인하려면 Angew 원문을 따로 확보해야 한다.
⛔ **따라서 "Y 도핑이 σ 를 X배 낮춘다"는 문장을 우리 원고에 쓸 수 없다.** 쓸 수 있는 것은
*"한 리뷰가 전자국재화 도핑의 σ 대가를 정성적으로 지적한다"* 까지다.

### ★4. σ 를 **올리는** 치환도 같이 적었나 — **적었다. 그것도 훨씬 많이.**

| # | 계 | 치환 | σ 결과 | 원 출처 |
|---|---|---|---|---|
| 1 | **LLZO** | Zr⁴⁺ → **Ta⁵⁺·Nb⁵⁺·W⁶⁺·Te⁶⁺** (aliovalent) → Li 빈자리 생성·cubic 안정화 | **1–2 × 10⁻³ S cm⁻¹** 까지 (액체의 2–5배 이내) | 무출처(본문 §2.1 일반 서술) |
| 2 | **LLZO** | Li⁺ 자리 **Ga³⁺·Al³⁺** → cubic 안정화 | (수치 없음) | 무출처. cf. **[10]** Murugan 2007 *Angew* 46, 7778 = 도가니 Al 로 cubic 안정화 시 **~3 × 10⁻⁴ S cm⁻¹** |
| 3 | **Argyrodite** | P 자리 **다중양이온 (Si, Ge, Sn)** + 할라이드 자리 **Cl 공도핑** (high-entropy) | **≈ 8 mS cm⁻¹** + 급속충전 electro-chemo-mechanical 안정성 | **[26]** W. Li et al., *Adv. Funct. Mater.* **34**, 2312832 (2024) |
| 4 | **할라이드** | M³⁺ = **Yb³⁺**(작은 이온반경) → bottleneck 을 최적 중간값으로 | "particularly high conductivities" (수치 없음) | **[35]** J. Wu et al., *Adv. Funct. Mater.* **35**, 2416671 (2025) |
| 5 | **가넷 GB** | **F 도핑**(표면+입계) | GB 이온전도 ↑ + 파괴인성 ↑ | **[74]** Y. Wang et al., *Adv. Funct. Mater.* **34**, 2404434 (2024) |
| 6 | **가넷** | **medium-entropy** 조성 | **1.52 × 10⁻³ S cm⁻¹** (RT) | **[81]** M. Umair et al., *Energy Storage Mater.* **81**, 104484 (2025) |
| 7 | **결정성 옥시할라이드** | **O²⁻/Cl⁻ 음이온 혼합** (Li₃Ta₃O₄Cl₁₀) | **13.7 mS cm⁻¹** + 산화안정 **4.9 V** | **[106]** F. Zhao et al., *Science* **390**, 199 (2025) |
| 8 | **클로라이드** | **high configuration entropy** | 4.6 V·5000 cycles·**91.9 %** 유지 (할로겐 산화 억제) | **[107]** D. Li et al., *Angew* **64**, e202419735 (2025) |
| 9 | **반-페로브스카이트** | ML 유도 조성설계 + 할로겐 치환 | "이온전도·계면상용성 향상" (수치 없음) | **[38]** C. Lin et al., *J. Energy Storage* **125**, 116990 (2025) |

⇒ **σ 를 올리는 사례 9건 vs 내리는 사례 1건.** 그리고 **올리는 쪽에만 숫자가 있다.**

**무엇이 두 경우를 가르나 — 리뷰가 *기준*을 주는가?**

**기준이라 부를 만한 것을 주기는 하는데, 서술적 이분법이지 판정 규칙이 아니다.** 두 겹으로 읽힌다.

1. **명시된 물리 원리** (§5.1, p.14, 인용 없음):
   > "The inverse correlation between ionic conductivity and electrochemical stability arises from a physical principle: **a highly polarizable, weakly binding anionic framework facilitates Li⁺ transport but also lowers the oxidative decomposition threshold.**"

   ⇒ **결합을 세게 하면 σ 를 잃고, 안정성을 얻는다.** Y–S 결합 강화가 정확히 그 사례다.

2. **암묵적 이분법** — 리뷰의 사례들을 놓고 보면 갈림은 **"도펀트가 무엇을 겨냥했나"** 다:
   - **σ 를 올린 9건**은 전부 *(a)* **캐리어/빈자리 농도**를 바꾸거나(aliovalent Zr→Ta/Nb/W/Te), *(b)* **자리에너지 분포를 넓히거나**(할라이드 자리무질서·high-entropy·"more disordered phases exhibit faster ion transport due to the broadening of the site-energy distribution" §2.3), *(c)* **bottleneck 크기를 최적점으로** 옮긴다(Yb³⁺).
   - **σ 를 내린 1건**은 도펀트의 목적이 **전자구조**였다 — 전자 국재화. 이온 부분계는 **부작용으로** 건드려졌다.

⛔ **그러나 리뷰는 이 이분법을 규칙으로 선언하지 않는다.** 문턱도, 기술자(descriptor)도,
"이 조건이면 σ 가 내려간다"는 판정식도 **없다.** 사례 나열 + 한 문장짜리 원리 진술까지다.

### ★5. ⇒ 우리 cascade 순위 방향에 무엇을 요구하나

→ **§16 (문서 끝) 에 근거와 함께 따로 썼다.** 요지 세 줄:
1. 우리 **G4(li_transport)에는 host 앵커가 없다** — `("bvs_x005", +1)` 은 *도펀트 풀 안에서만* min-max 정규화한다. 반면 **G3(oxidation)은 host 2.14 V 에 앵커돼 있다.** 깔때기가 앵커를 쓸 줄 아는데 이온 축만 안 쓴다.
2. 리뷰가 지목한 σ 하락 기구는 **"Li⁺ 확산채널 주변 국소 배위환경의 수축"** 이다 — 우리 BVS proxy 가 재는 것이 바로 그 국소 환경이다. 관측량은 맞고, **비교 기준점이 틀렸다.**
3. **숫자는 못 가져온다** (★2·★3). 문턱을 제안할 근거가 리뷰에 없다.

---

## 1. 한 줄 요약

무기 고체전해질 3계열(산화물 가넷 LLZO / 황화물 LGPS·argyrodite / 할라이드 Li₃MX₆)을
**"계면"이라는 단일 렌즈**로 다시 정렬한 종설 — *"이제 문제는 Li 를 통하는 물질을 찾는 것이 아니라,
그 물질이 셀 안에서 수천 사이클을 견디게 하는 계면을 설계하는 것"* 이고, 그 설계의 가속기로
DFT 대전위 상평형도 → AIMD → GNN/LLM 폐루프를 배치한다. 계산 편은 **소개**만 하고
**계면 계산의 규약(슬랩·strain·종단·vacuum)은 한 줄도 다루지 않는다.**

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | **Shipeng Liang¹, Zhehan Xu¹, Mingzi Sun¹, Qiuyang Lu¹, Tong Wu¹, Baian Chen¹, Zikang Li¹, Ziqi Zhou¹, Lu Lu¹, Olga Minchukova², Gregori Rymski², Aliaksandr Zhaludkevich², Bolong Huang¹\*** |
| 소속 | ¹ Dept. of Chemistry, **City University of Hong Kong** · ² Scientific-Practical Materials Research Centre, **National Academy of Sciences of Belarus**, Minsk |
| 교신 | Bolong Huang (b.h@cityu.edu.hk) |
| 저널/년 | ***Battery Energy*** **2026; 5:e70137** (2026, vol.5, issue 4) |
| DOI | `10.1002/bte2.70137` |
| 접수/수정/수락 | 2026-06-03 / 2026-06-16 / **2026-06-18** (수락까지 **15일**) |
| 라이선스 | CC-BY (open access), © 2026 The Author(s), Xijing University + John Wiley & Sons Australia |
| 분량 | 본문 **18 pp** · **Figure 1–6** (SI 없음) · **Table 0개** · **refs 110** |
| 연구유형 | **Review (종설)** — 원 계산·원 실험 **0건** |
| 키워드 | all-solid-state battery, argyrodite, garnet, grain boundary engineering, halide electrolyte, high-entropy electrolyte, interface, lithium dendrite, machine learning |
| 이해상충 | ⚠ **Bolong Huang 은 *Battery Energy* 의 Editor-in-Chief 이자 이 논문의 공저자다.** 논문이 스스로 밝히고, 본인은 편집 결정에서 배제됐다고 적었다 |

### 2-1. ⚠ 업로드 PDF 2개 판정 — **완전히 동일한 파일이다**

```
sha256  7c884b0d49a406f185ca61fce1d00b65a59dd8a267e81e48b9878dd17e88913b   f7870077-103._Battery_Energy…pdf
sha256  7c884b0d49a406f185ca61fce1d00b65a59dd8a267e81e48b9878dd17e88913b   643be538-103._Battery_Energy…pdf
크기 2,672,869 B (동일) · 18 pp (동일) · Wiley 워터마크 다운로드 스탬프까지 동일
```
⇒ **바이트 단위로 같다.** 초록·쪽수 대조 불필요. 정본으로 `f7870077-…` 를 썼고,
`litdb/inbox/103._Battery_Energy__2026__Liang__…pdf` 로 복사해 그림을 크로핑했다.
**두 파일 사이 차이는 없다.**

## 3. 핵심 물성 — ⛔ **전부 2차 인용** (원 출처 병기)

> ⛔ 아래 어느 값도 우리 `db/properties/*` 에 넣지 않는다. 원고에 쓸 때는 **원 출처를 직접 인용**하고
> "Liang 2026 리뷰 경유"임을 밝힌다.

### 3-1. 이온전도도 (RT)

| 계 | σ | 원 출처 |
|---|---|---|
| LLZO (as-discovered, cubic, 도가니 Al 안정화) | **~3 × 10⁻⁴ S cm⁻¹** | **[10]** Murugan, Thangadurai, Weppner, *Angew* **46**, 7778 (2007) |
| LLZO (계통적 도핑 후) | **1–2 × 10⁻³ S cm⁻¹** | 무출처(리뷰 서술) |
| LLZO **입계** | 벌크보다 **2–3 자릿수 낮음** | **[18]** C.C. Wang et al., *J. Power Sources* **602**, 234394 (2024) |
| **LGPS** | **12 mS cm⁻¹** | **[24]** Kamaya et al., *Nat. Mater.* **10**, 682 (2011) |
| argyrodite 계열 일반 | ~1–10 mS cm⁻¹ | **[11]** Deiseroth et al., *Angew* **47**, 755 (2008) |
| **Li₆PS₅Cl** | **~3–5 mS cm⁻¹** | ⚠ **무출처** |
| **Li₆PS₅Br** | **~6–8 mS cm⁻¹** (단 안정성 열세) | ⚠ **무출처** |
| **Li₆PS₅I** | **~1 mS cm⁻¹** (Li 자리무질서 제한) | ⚠ **무출처** |
| Li₃YCl₆ / Li₃YBr₆ | **10⁻⁴ – 10⁻³ S cm⁻¹** | **[34]** Asano et al., *Adv. Mater.* **30**, 1803075 (2018) |
| high-entropy argyrodite (Si,Ge,Sn@P + Cl) | **≈ 8 mS cm⁻¹** | **[26]** W. Li et al., *AFM* **34**, 2312832 (2024) |
| medium-entropy Li-가넷 | **1.52 × 10⁻³ S cm⁻¹** | **[81]** Umair et al., *ESM* **81**, 104484 (2025) |
| **Li₃Ta₃O₄Cl₁₀ (결정성 옥시할라이드)** | **13.7 mS cm⁻¹** ← 리뷰가 인용한 최고값 | **[106]** F. Zhao et al., *Science* **390**, 199 (2025) |
| Li₃PO₄ (ALD 코팅재) | ~10⁻⁶ S cm⁻¹ | **[50]** J. Kim et al., *J. Am. Ceram. Soc.* **107**, 3134 (2024) |
| LLZTO GB complexion (Al₂O₃ ALD) | **2.59 → 6.92 × 10⁻⁴ S cm⁻¹ (×2.7)** | **[18]** ⚠ **`Fig. 5b` 그림과 안 맞는다 → §10-3** |
| 가넷 "grain-fusion" | 총 σ **> 10⁻³ S cm⁻¹** | **[74]** |

⚠ **Li₆PS₅Cl/Br/I 세 값은 인용이 없다.** 특히 **Li₆PS₅I ~1 mS cm⁻¹** 는 통상 보고치(10⁻⁶–10⁻⁵ S cm⁻¹ 급)보다
**2–3 자릿수 높다.** 우리 축 A(할로겐 순서) 논의에 **이 세 값을 근거로 쓰면 안 된다.**

### 3-2. 산화안정성 / ESW

| 계 | 값 | 방법 | 원 출처 |
|---|---|---|---|
| 황화물 일반 | **DFT 산화 2.1–2.5 V** vs 실셀 운전 **3.5–4.2 V** (= 속도론적 부동태화로 설명) | DFT | **[28]** Chai et al., *ChemSusChem* **17**, e202301268 (2024) |
| argyrodite | ~2.5 V | DFT | **[37]** Tan et al., *AEM* **15**, 2403986 (2025) |
| Li₃YCl₆ / Li₃InCl₆ | **> 4.3 V** | DFT | **[37]** |
| 할라이드 국소격자왜곡 | **~4.25 → ~4.4 V** | 실험+DFT | **[36]** Z. Song et al., *Nat. Commun.* **15**, 1481 (2024) |
| **LiP(OF)₂ (코팅 후보)** | **2.6 – 4.9 V** (`Fig. 6a`, **figure-read ≈**) | DFT 대전위 | **[91]** Qian, Nazar et al., *Angew* **64**, e202413591 (2025) |
| Li₃Ta₃O₄Cl₁₀ | 산화 **4.9 V** 까지 | — | **[106]** |
| Li 금속에 열역학적으로 안정한 것 | **LiF, Li₂O, Li₃N, Li₃P 정도의 일부 2원 화합물뿐** | DFT 대전위 상평형도 | 리뷰 §3.2.1 (무출처 일반화) |

### 3-3. 기계·계면 정량

| 항목 | 값 | 원 출처 |
|---|---|---|
| 황화물 Young's modulus | **20–40 GPa** | 리뷰 §2.2 (무출처) |
| LLZO | **~150 GPa** | 리뷰 §2.2 (무출처) |
| 할라이드(Li₃InCl₆, Li₂ZrCl₆) | **~20–35 GPa** | **[81, 82]** |
| **임계 스트리핑 전류** Li/Li₆PS₅Cl/Li @3 MPa | **0.2 mA cm⁻²** | **[59]** Kasemchainan et al., *Nat. Mater.* **18**, 1105 (2019) |
| 임계 **플레이팅** 전류 LLZO | ≈ **0.6 mA cm⁻²** | **[70]** |
| 임계 플레이팅 전류 Li₆PS₅Cl @3–7 MPa | **0.2–1.0 mA cm⁻²** | **[70]** |
| **CCD** Li\|LLZTO\|Li, 25 °C, 무외압, 0.05 mA cm⁻² step | **pristine 0.15 → ALO10 0.45 mA cm⁻²** (본문) · **ALO5 0.25 / ALO20 0.35** (`Fig. 4a`, **figure-read**) | **[18]** |
| CCD, PEO-LiTFSI/LATP(5 wt%) ~8 µm 중간층 | **1.0 → > 1.6 mA cm⁻²**, 60 °C·0.2 mA cm⁻² 에서 **~2800 h** | **[33]** Xiao et al., *Mater. Lett.* **362**, 136221 (2024) |
| CCD, glass-network garnet (50Li₂O–38B₂O₃–12SiO₂ 3D 망) | **> 2 mA cm⁻²** | **[20]** J. Liu et al., *Small* **21**, 2410471 (2025) |
| Li₃PO₄ 코팅 두께/면저항 | **5–10 nm** → **~5–10 Ω cm³** ⚠ 단위 표기 그대로 (Ω cm² 여야 자연스럽다 → §10-6) | **[50]** |
| Li\|LLZO 고유 전하이동저항 | **~10⁻¹ Ω cm³** ⚠ 같은 단위 문제 | **[82–85]** Krauskopf, Zeier, Janek |
| Li₂CO₃ 부동태막 | **~5–10 nm** | **[19]** |
| SCL(공간전하층) 산화물/산화물 | **10–50 nm**, 국소 Li⁺ 농도 **수 자릿수** 감소 | **[21]** |
| LAZO(Li_xAl_yZn_zO) 표면층 on LiNiO₂ | **~4 nm**, 셀 **> 400 Wh kg⁻¹**, **> 500 cycles** | **[58]** L. Wang et al., *Nat. Nanotechnol.* **19**, 208 (2024) |
| TiO_x 중간층 화학량론 | **1.5 ≤ x ≤ 2** (혼합 이온-전자 전도체) | **[51]** Götz et al., *ChemSusChem* **17**, e202401026 (2024) |
| 최적 스택압 창 | 황화물 argyrodite **3–10 MPa** · 할라이드 **5–20 MPa** · 가넷 **~0 (lithophilic 코팅 시) ~ 10–30 MPa** | **[81, 82]** |
| Na vs Li 융점 | 98 °C vs 181 °C | **[87]** |
| Li-Si 이론용량 | 3579 mAh g⁻¹ | **[79]** |
| 양극 부피변화 | 층상산화물 **~2–7 %** | 리뷰 §3.1 (무출처) |

### 3-4. ⭐ 우리 조성이 **직접** 등장하는 한 곳

> p.11, §3.2.4: "…Cui et al. recently demonstrated that the **Al/halide interface fails via continuous reductive decomposition of the halide electrolyte, producing indium metal accumulation** that physically blocks ion transport at the anode/electrolyte interface **[88]**. In contrast, **sulfide electrolytes (Li₅.₄PS₄.₄Cl₁.₆) form a redox-active interphase enabling reversible cycling.**"

**[88]** J. Cui, Z. Wang, J. Tan, et al., *ACS Appl. Mater. Interfaces* **17**, 22014 (2025).

⇒ **`Li₅.₄PS₄.₄Cl₁.₆` = 우리 `modelc` 와 같은 조성식**(`db/compositions/modelc.json`).
리뷰 전체에서 우리 계가 이름으로 나오는 유일한 자리이고, 맥락은 **Al 음극 대비**다.
"redox-active interphase" 라는 표현만 있고 **수치는 없다**.

## 4. DFT/계산 방법 ★ — **리뷰는 계산을 하지 않는다**

- **code / version**: **n/a** — 원 계산 0건
- **functional (+vdW)**: **n/a**. 본문 전체에서 함수형 언급은 **PBE 1회뿐**이고, 그것도 인용문 안이다 —
  *"higher-fidelity r2SCAN … compared to the commonly used PBE, which is known to underestimate formation and interfacial energies"* (p.13, GNoME **[93]** 소개). ⚠ 이 문장 자체가 틀렸다 → §10-2
- **pseudo / PAW**: **n/a**
- **k-points / ecut / supercell / nat**: **n/a** — 키워드 스캔 결과 `supercell` 0회, `k-point` 0회, `cutoff` 0회, `VASP` 0회, `pymatgen` 0회
- **DFT+U**: **n/a**
- **AIMD**: 리뷰가 *소개*하는 형태로만 —
  > "AIMD simulations … integrated over **picosecond-to-nanosecond** trajectories, provide a direct and parameter-free prediction of the lithium-ion diffusion coefficient. The ionic conductivity is obtained via the **Nernst-Einstein relation**. When applied to known electrolytes such as LLZO, LGPS and argyrodites, AIMD **reproduces experimental conductivities within the same order of magnitude**. This level of accuracy sufficient for screening purposes but **insufficient for quantitative prediction**. The computational cost of AIMD limits the accessible simulation cell to **a few hundred atoms** and the simulation time to **tens to hundreds of picoseconds**." (p.12, cf. **[3]** Famprikis et al., *Nat. Mater.* **18**, 1278)

  ⇒ ensemble·thermostat·timestep·MSD 창 **전부 없음.** Haven ratio 언급 없음.
- **MLIP**: ⛔ **한 번도 안 나온다.** `MLIP`·`machine-learned interatomic potential`·`neural network potential` **0회**.
  ML 은 **성질 예측 대리모델(GNN·Extra Trees·CNN)과 LLM** 으로만 등장하고, **힘장(force field)으로서의 ML 은 이 리뷰에 없다.**
  ⇒ 우리 UMA-MD 축(J)과 겹치지 않는다.
- **무질서 처리 (SQS / enumerate / 단일배열)**: ⛔ **0회.** `SQS` 0, `special quasirandom` 0.
  무질서는 **물리 현상으로만** 다뤄진다(할라이드 양이온 무질서 ↔ 자리에너지 분포 폭 ↔ σ; argyrodite S/X 무질서).
  **계산에서 무질서를 어떻게 표본하는가는 한 줄도 없다.**
- **특이사항**: 대신 이 리뷰가 계산 쪽에서 실제로 **개념적으로** 밀고 있는 것 3개
  1. **DFT 대전위 상평형도(grand potential phase diagram)를 계면 열역학의 표준 도구**로 못 박음 —
     *"DFT-based grand potential phase diagrams have become the standard computational tool for predicting the thermodynamic stability of electrolyte/electrode interfaces"* **[91]**
  2. **operando 실험 ↔ 제일원리의 공동검증(co-validation)을 "gold standard"** 로 선언 — **[92, 95]** Quérel/Williams
  3. **메조스케일 다리**: phase-field(균열↔수지상 "wait-and-go" **[96]** Xue et al., *JMPS* **202**, 106197) +
     FEM phase-field fracture(복합양극 **[97]** Taghikhani et al., *JMPS* **198**, 106060)

## 5. Figure set ★

> ✅ **6장 전부 크로핑했고 6장 전부 눈으로 봤다** (리뷰의 전체 그림 수 = 6). 안 본 그림 없음.
> 크로핑 도구의 알려진 버그 2건(2단 조판 혼입 / 캡션이 위인 판형에서 밀림)은 **이 논문에서 발생하지 않았다** —
> Wiley 2단 조판이지만 그림이 전부 **단 전폭(full-width)** 이고 캡션이 그림 **아래**라 앵커가 정확히 맞았다.

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a–c | 3계열 결정구조 도해: (a) LLZO — LaO₈ 12면체 + ZrO₆ 8면체 골격, Li(1)O₄ 사면체 24d / Li(2)O₆·Li(3)O₆ 8면체 96h; (b) **Li₆PS₅X** — PS₄ 사면체(회색), S(회색 구), **I(흰 구)**, Li1/Li2 다중자리(검은 점 구름); (c) 할라이드 3형 — Li₃YCl₆ **hcp-orthorhombic** / Li₃YCl₆ **hcp-trigonal** / Li₃InCl₆ **ccp-monoclinic** | (b) 가 **X = I 로 그려져 있다**(캡션은 "X represents Cl, Br, and I") — 우리 Cl-rich 그림과 나란히 놓을 때 **같은 계열이라고 뭉개면 안 된다**. (c) 의 **hcp↔ccp / ordered↔disordered 3형 대비**는 우리가 "무질서가 자리에너지 분포를 넓힌다"를 그림으로 설명할 때 바로 쓸 수 있는 표준 도해 |
| 2a | LICGC 단면 SEM 4패널: (A) 5 nm 시료 **20 µm 스케일바**, (B) 10 nm 시료 **1 µm**, (C)(D) 각각 확대 **1 µm**. 어두운 영역 = 전해질 벌크로 자라 들어간 신생상 | ⚠ **(A)와 (B)의 스케일바가 20배 다르다** — 본문의 *"얇은 중간층일수록 신생상이 더 두껍다"* 를 **이 두 패널을 눈으로 비교해서는 확인할 수 없다**(figure-read). 우리가 두께 비교 그림을 만들 때의 반면교사 |
| 2b | Li₃PO₄(LPO) 아레니우스: **Ln(σT) [K·S/cm] vs 1000/T [1/K]**, ALD 300(파랑)·ALD 275(검정)·H/T 600(빨강) + 문헌선 4개 | 🔴 **측정점(원)은 1000/T ≈ 1.55–1.85(≈540–645 K)에만 있고, 선은 3.1(≈322 K)까지 외삽이다**(figure-read). ⇒ 본문의 "Li₃PO₄ σ ~10⁻⁶ S cm⁻¹" 는 **고온 외삽값**이다. **우리가 코팅재 σ 를 인용할 때 같은 함정** |
| 2c | LiNiO₂ vs LNO-4.5PO 의 **dQ/dV [mAh/V] vs V (3.0–4.4 V)**, 1st/2nd/50th/100th/200th. 점선 상자 = **H2–H3 전이(≈4.1–4.35 V)** | ⚠ 재수록된 두 패널에 **LNO / LNO-4.5PO 라벨이 없다** — 어느 쪽이 코팅체인지 캡션 순서에만 의존한다(figure-read). 우리 dQ/dV 류 그림에는 패널 내 라벨을 반드시 넣을 것 |
| 3a | **Kasemchainan 보이드 서사** [59]: pristine → 여러 번 스트리핑(**void formation**) → 이후 플레이팅 초기(**lateral Li growth**, 초기 수지상 전파) → 플레이팅 중반 → 플레이팅 종료(**occluded voids**) → 추가 스트리핑(**접촉 손실 증가**) | 우리 계(Li\|Li₆PS₅Cl)를 명시한 도해다. **"수지상은 플레이팅이 아니라 *스트리핑*에서 시작된다"** 를 한 장으로 설명 — 세미나 슬라이드용 |
| 3b | **Cl 2p XPS (203→195 eV)** 4패널: HE-LIC 사이클 전/후, LIC 사이클 전/후. 사이클 후 **Clₓ⁻ 산화종(주황 성분)** 이 **LIC 에서 뚜렷하게 크고 HE-LIC 에서는 미량** | ★ **우리 "Cl-rich 산화" 축의 실험 관측량**이 이것이다. figure-read ≈ Cl⁻ 주 doublet **~197.8 / 199.4 eV**, 산화 Clₓ⁻ 성분 **~199 / 200.5 eV**. 본문 서술과 그림이 **일치**하는 몇 안 되는 경우 |
| 4a | **CCD 4패널** Li 대칭셀, 0.05 mA cm⁻² step, Voltage ±0.20 V vs Time 0–24 h: **Pristine 0.15 · ALO5 0.25 · ALO10 0.45 · ALO20 0.35 mA cm⁻²** | 🔴 **비단조다 — ALO20 이 ALO10 보다 나쁘다.** 본문은 **0.15 와 0.45 두 값만 인용하고 이 비단조성을 언급하지 않는다**(figure-read). ★ **"더 많이 = 더 좋다"가 성립하지 않는 실측 사례** — ★5 논의의 실험 대응물 |
| 4b | 사이클 수명 막대 [×10³ h]: **LLZO 570 · S-LLZO 740 · F-LLZO 12,000 h** + 표면/GB 불소화 도해(전자 차단) | figure-read. **12,000 h ≈ 500일** 은 대칭셀 값이고 셀 수준 수명이 아니다 — 인용 시 반드시 조건을 붙일 것 |
| 5a | zero-Na-excess 계면 **층상화(stratification)**: MgF₂ + 2Na → 2NaF + Mg 전환반응 → SSE 쪽 **전자차단/이온전도** 층 + Al 쪽 **sodiophilic** 층. HRTEM 에 NaF(보라)·Mg(초록) 도메인, **10 nm 스케일바** | ★ **"계면상을 하나의 층이 아니라 *경사(graded) 다층*으로 설계한다"** 는 개념 원형. 우리가 코팅 후보를 고를 때 *단일 상 하나*로 판정하는 현재 틀의 대안 |
| 5b | **LLZTO 총 이온전도 아레니우스**: ln(σT) [S cm⁻¹ K] vs 1000/T (2.8–3.3), Pristine/ALO5/ALO10/ALO20 | 🔴 **본문 수치와 안 맞는다** — figure-read 로 1000/T=3.3 에서 pristine ≈ **−7.90**, ALO10 ≈ **−7.45** ⇒ **비 ≈ 1.6×**, 본문은 **2.7×**. 게다가 ln(σT)≈−7.5 는 σ ~10⁻⁶ S cm⁻¹ 급이라 본문의 **6.92 × 10⁻⁴ S cm⁻¹** 와 3 자릿수 어긋난다 → §10-3 |
| 6a | **LiP(OF)₂ 전기화학 안정창**: Li per Formula Unit vs V (0–7 V). 녹색 창 **2.6 ↔ 4.9 V**; 왼쪽 환원산물 **LiF, Li_xP, LiP_yO_z**, 오른쪽 산화산물 **P₂O₃F₄, Li_xO** | ★ **우리 ESW 그림과 같은 양식**(대전위 프로파일). 우리 comp1/modelc onset 2.256 V 그림을 이 형식으로 다시 그리면 문헌 독자에게 즉시 읽힌다 |
| 6b–d | **Li₆PS₅Cl ↔ LiP(OF)₂ pseudo-binary 상호반응에너지** [meV/atom] vs x: (b) 전위 없음 최소 ≈ **−145** @x≈0.5 → **Li₃PO₄, LiF, LiCl, P₂S₅**; (c) **2.8 V** 최소 ≈ **−47** @x≈0.62 → LiF, LiPO₃, LiCl, P₂S₇; (d) **4.3 V** 최소 ≈ **−95** @x≈0.07 → P₂O₃F₄, SOCl₂, LiPO₃ (전부 figure-read) | ★★ **이것이 이 리뷰가 제시하는 유일한 "계면 정량"이다** — 그리고 **우리 T9 4상대 계면반응(Richards/Ong 2016 pseudo-binary)과 정확히 같은 구성**이다. 다만 **전위를 3개 값에서 끊어 보여주는 것**은 우리가 안 하고 있다. ✅ **원전을 우리가 이미 갖고 있다 → §5-1 교차검증** |
| 6e,f | **NCM(LiMn₀.₀₈₃Co₀.₀₈₃Ni₀.₈₃O₂) ↔ LiP(OF)₂**: (e) 2.8 V 최소 ≈ **−395 meV/atom** @x≈0.41 → CoO, NiO, Li₃PO₄, LiF; (f) 4.3 V 최소 ≈ **−108** @x≈0.6 → Li₂NiF₄, CoO₂, MnO₂, Ni₃(PO₄)₂ (figure-read) | **양극 쪽 구동력이 SE 쪽보다 4–8배 크다**(−395 vs −47 @2.8 V). 우리 cascade 가 SE 축과 양극 축을 **같은 스케일로 정규화**하고 있다면 그 자체가 물리적으로 왜곡이다 |
| 6g–j | Quérel/Williams **operando XPS ↔ 반응속도 모델**: 정규화 표면종 농도 vs 시간(0–300 s), 결합에너지 이동 vs 시간. NZSP\|Na_xPO_y 는 −0.25 eV 로 포화, NZSP_polished 는 **−1.25 eV** 까지 (figure-read) | **"DFT 로 경로 후보를 만들고 operando 시계열로 어느 경로가 지배적인지 고른다"** 의 실물 예. 우리가 계면 보고량을 정의할 때의 **검증 형식** 후보 |
| 6k,l | **GNoME [93]**: (k) 고유원소 수(2–6)별 distinct prototypes, **4원소에서 >20,000 최대**, GNoME(진보라) ≫ Materials Project(연파랑); (l) **r²SCAN vs PBE 상분리에너지** 산점도, **Stable 84 % / Unstable 16 %** | ⚠ (l) 축 이름이 **"Phase-separation energy"** 다 — 본문은 이것을 "interfacial energies" 라고 부른다. **그림이 본문을 부인한다** → §10-2 |

### 5-1. ✅ `Fig. 6a–f` 는 **우리가 이미 원전을 갖고 있다** — figure-read 교차검증 성공

`Fig. 6a–f` 의 원전 **[91]** 은 `litdb/papers/**qian2025_lipo2f2_coating_stable_cei.md**` 로
**이미 digest 돼 있다** (= 업로드 `99737a54-73. engineering Stable Decomposition Products…pdf`,
Qian⁺/Huang⁺/Dean/Kochetkov/Singh/**Nazar\***, *Angew* **64**, e202413591). 표지 대조 완료.

⇒ **내가 이 리뷰의 재수록 그림에서 읽은 값을, 우리가 원전에서 읽어 둔 값과 맞춰 봤다.**

| 항목 | 이 리뷰 `Fig. 6` (내 figure-read) | 우리 qian2025 digest (원전 figure-read) | 판정 |
|---|---|---|---|
| LiPOF 안정창 | **2.6 – 4.9 V** | **2.6 – 4.9 V** | ✅ 일치 |
| LPSCl↔LiPOF 무전위 최소 | **≈ −145** @x≈0.5 | **≈ −145** @**x = 0.52** | ✅ 일치 |
| 산물 (무전위) | Li₃PO₄, LiF, LiCl, P₂S₅ | Li₃PO₄+LiF+LiCl+P₂S₅ | ✅ 일치 |
| **2.8 V** 최소 | ≈ **−47** @x≈0.62 | **−43** @x≈0.62 | ⚠ **원전값 −43 이 정확하다** (재수록본에서 4 meV/atom 과다 판독) |
| 산물 (2.8 V) | LiF, LiPO₃, LiCl, P₂S₇ | LiPO₃+LiF+LiCl+P₂S₇ | ✅ 일치 |
| **4.3 V** 최소 | ≈ **−95** @x≈0.07 | **−96** @x≈0.08 | ✅ 일치 (1 meV/atom) |
| 산물 (4.3 V) | P₂O₃F₄, SOCl₂, LiPO₃ | LiPO₃+P₂O₃F₄+**SOCl₂**(원전이 *속도론으로 배제*한다고 명시) | ✅ 일치 + **원전이 해석을 준다** |
| NCM↔LiPOF 2.8 V | ≈ **−395** | **≈ −395** | ✅ 일치 |
| NCM↔LiPOF 4.3 V | ≈ **−108** | **≈ −108** | ✅ 일치 |

**여기서 얻는 것 3가지**
1. **우리 figure-read 관행이 ±1–4 meV/atom 안에서 재현된다** — 서로 다른 세션이 서로 다른 판형
   (원전 vs 리뷰 재수록)에서 읽었는데 8/9 항목이 맞았다. **`figure-read ≈` 표기의 신뢰도 실측치**다.
2. **리뷰가 원전보다 정보를 잃는다.** 원전 digest 는 `x=1.0 회색 점선 = LPSCl 자체 분해 ≈ −83 meV/atom
   → Li₃PS₄+Li₂S+LiCl`(★ **우리 `interface_reactivity_results.json` 의 x=1 kink 와 문자 그대로 일치**)와
   **SOCl₂ 를 속도론으로 배제**한다는 해석을 담고 있는데, **리뷰는 둘 다 옮기지 않는다.**
   ⇒ **리뷰를 인용하지 말고 `[91]` 원전(=우리 qian2025 digest)을 인용한다.**
3. **계면 게이트의 원전이 확인된다**: 우리 qian2025 digest 가 이미 잡아 놨듯
   `|ΔE_rxn| < 100 meV/atom` 게이트의 **실제 원전은 Xiao 2019 filter 4** 이고,
   Qian 논문 본문은 그것을 다른 ref 로 잘못 귀속한다. **Liang 리뷰는 게이트 값 자체를 아예 안 옮긴다.**

## 6. Post-processing ★

리뷰가 **소개**하는 후처리 (수행한 것이 아님):

| 기법 | 리뷰에서의 역할 | 도구/구현 | 수치화 방식 |
|---|---|---|---|
| **DFT 대전위 상평형도 (grand potential)** | ★ 계면 열역학의 **표준 도구**로 명시. 두 용도: ① 전해질의 ESW(`Fig. 6a`) ② 전해질\|코팅 및 전해질\|양극의 **상호반응에너지**(`Fig. 6b–f`) | 명시 없음 (관행상 pymatgen `PhaseDiagram`/`GrandPotentialPhaseDiagram`) | **meV/atom**, pseudo-binary x 축, **최소 반응에너지 지점**에 별표 + 산물 목록. 전위 고정값(0 / 2.8 / 4.3 V) 별로 재계산 |
| **AIMD → Nernst–Einstein** | σ 예측. **"자릿수까지만 맞는다"** 고 스스로 한계 선언 | 명시 없음 | D → σ. **MSD 창·Haven ratio·시드 수 전부 미기재** |
| **XPS(비계산) 깊이 프로파일 / 피크 분해** | ① 할라이드\|Li 분해경로(M³⁺ 환원 + LiCl 생성) **[40]** ② **Cl 2p Clₓ⁻ 산화종**을 계면 열화의 지표로(`Fig. 3b`) ③ operando 시계열을 모델과 맞물림(`Fig. 6g–j`) | — | 피크 면적·결합에너지 이동(eV) |
| **GNN 고처리량 스크리닝** | 2.2 M → 384 k → 736 (GNoME) | Materials Project 학습 | §12 표 참조 |
| **Extra Trees + 다중필터** | 반-페로브스카이트 149,480 → 963 | — | §12 표 참조 |
| **phase-field / FEM** | 수지상-균열 결합(`wait-and-go`), 복합양극 파괴 | — | 응력·균열경로 |
| **LLM 문헌마이닝·클러스터링** | MOF 전해질 XRD/BET/EIS/NMR 군집 → 합성-구조-물성 규칙 추출 | — | 정성 |

⛔ **리뷰에 전혀 없는 후처리**: **NEB / CI-NEB · Bader · COHP-ICOHP · COBI · LOBSTER · ELF · BVSE · phonon · elastic tensor(C_ij) · EOS**.
키워드 스캔 0회 확인. ⇒ 우리 후처리 스택 중 **대전위 ESW 하나만** 이 리뷰와 겹친다.

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

> ⚠ **리뷰 대 우리 계산의 직접 비교는 원칙적으로 성립하지 않는다** — 리뷰에는 방법 라벨이 없다.
> 아래는 **"같은 양을 말하는가 / 방향이 맞는가"** 수준의 대조이고, **수치 일치를 주장하지 않는다.**

| 항목 | 이 리뷰 (2차 인용) | 우리 (comp1 / modelc) | 판정 |
|---|---|---|---|
| **산화 onset** | 황화물 DFT **2.1–2.5 V**, argyrodite **~2.5 V** **[28, 37]** | **2.256 V** (LiS4 제외 GG set) — comp1·modelc **동일**, S²⁻-limited | ✅ **실질 일치.** 우리 2.256 V 가 리뷰가 인용한 2.1–2.5 V 대역 **안**에 있다. ⚠ 단 리뷰는 상집합(phase set)·LiS4 처리·압력을 안 밝히므로 **"같은 값"이 아니라 "같은 대역"**까지만 |
| **DFT ↔ 실셀 괴리 설명** | *"DFT 2.1–2.5 V vs 실셀 3.5–4.2 V = **속도론적 부동태화**"* | 우리도 grand-potential 0-압력 열역학값 — 속도론 없음 | ✅ **같은 프레이밍.** 우리 원고의 "onset 은 열역학 하한이다" 문장에 **리뷰 인용을 붙일 수 있다** |
| **Cl 의 역할** | *"smaller Cl⁻ introduces favorable site-energy distributions for Li⁺ hopping"*, 할로겐 정체가 Li 부분격자 무질서를 지배 | 우리: **Cl 증가 → D↑(2.6×), Ea↓** / **onset 은 불변**(S²⁻-limited) — Cl 은 onset 이 아니라 *분해 양·산물·계면* 에 작용 | ✅ **방향 일치**, 그리고 **우리 쪽이 더 분해돼 있다.** 리뷰는 "Cl 이 σ 에 좋다"까지만 가고 **onset 불변**은 말하지 않는다 |
| **할로겐 σ 순서** | **Br (6–8) > Cl (3–5) > I (~1 mS cm⁻¹)** ⚠ 셋 다 무출처 | 우리는 **X 정체가 아니라 Cl 함량**(comp1 → modelc)을 변수로 잡았다 | ⚠ **다른 변수다 — 충돌이 아니다.** 그리고 리뷰의 Li₆PS₅I ~1 mS cm⁻¹ 는 통상치보다 높아 **근거로 못 쓴다** |
| **기계적** | 황화물 **20–40 GPa**, LLZO ~150 GPa (무출처) | comp1 **E_VRH 22.06** / modelc **27.66 GPa** (relaxed-ion, PBE) | ✅ **우리 값이 리뷰 대역 하단에 정확히 든다.** ⚠ 리뷰가 clamped/relaxed·함수형을 안 밝히므로 **"대역 안"까지만**. 우리 B₀(comp1 26.23 / modelc 21.71)와는 축이 다르다 |
| **전자구조 / band gap** | ⛔ **황화물 gap 값 없음.** 반-페로브스카이트 스크리닝 필터로 **"band gap > 4 eV"** 가 한 번 나올 뿐 **[100]** | comp1 **2.066** / modelc **2.099 eV** (fixed-occ nscf 고유값) | ⚠ **비교 불가.** 4 eV 는 다른 물질계의 **스크리닝 문턱**이지 물성값이 아니다. 우리 gap 은 PBE 과소평가 + 무질서 민감 → **"wide-gap insulator"** 수준 서술만 |
| **전자전도가 수지상의 근원** | ★ **[72]** Han et al., *Nat. Energy* **4**, 187 (2019): *"high electronic conductivity, **rather than mechanical properties**, is the root cause of internal dendrite formation"* | 우리 modelc PDOS v2: **CBM 에 Li 기여 무시 가능**(S 3p 반결합 + P 3s), *"전자 환원이 Li 자리에서 핵생성하지 않는다"* | ✅✅ **가장 강한 접점.** 리뷰가 "전자 누설이 수지상을 만든다"를 3대 기구 중 하나로 세워 놨고, **우리 PDOS 가 그 축에서 우리 계가 왜 유리한지를 말한다.** 원고 §전자구조의 *so-what* 을 리뷰로 받칠 수 있다 |
| **우리 조성 직접 언급** | `Li₅.₄PS₄.₄Cl₁.₆` 가 **Al 음극 대비**에서 *"redox-active interphase enabling reversible cycling"* **[88]** Cui 2025 | = 우리 **modelc** | ⭐ **확보할 원문 1순위.** 우리 조성의 계면 거동을 실험으로 다룬 유일한 접점 |
| **MLIP / 무질서 표본** | ⛔ **둘 다 없다** | 우리: UMA-s-1p1 MLIP-MD + 무질서 배열 처리 | ➖ **접점 없음.** 이 리뷰는 우리 J 축(MLIP 방법론)에 아무것도 주지 않는다 |
| **계면 보고량(B2) 정의** | ⛔ **슬랩·strain·종단·vacuum 0회** (§13) | 우리 B2 = 🔴 **미정의** | ❌ **리뷰가 정의를 주지 않는다.** 기대했던 것을 못 얻었다 |

**방법 의존성 경고 (차이를 주장하기 전에)**
- 리뷰의 값 중 **함수형·k-mesh·이완조건이 밝혀진 것은 0개다.** 따라서 위 표의 ✅ 는 전부
  *"대역이 겹친다"* 이지 *"값이 같다"* 가 아니다.
- 특히 **산화 onset 2.1–2.5 V** 는 상집합 선택(LiS4 포함 여부)에 우리 실측으로 **0.12 V** 가 움직인다
  (2.256 → 2.14). 리뷰의 대역 폭(0.4 V)이 그보다 넓어 **구분력이 없다.**

## 8. 적용 인사이트

1. **★ 순위 규칙에 host 앵커를 넣는다** — §16.
2. **대전위 계면반응을 *전위별로* 끊어 보고한다.** `Fig. 6b–d` 가 같은 쌍(LPSCl↔LiP(OF)₂)을
   **0 V / 2.8 V / 4.3 V** 세 번 계산해 최소 반응에너지와 **산물 조성이 전위에 따라 바뀌는 것**을 보여준다
   (−145 → −47 → −95 meV/atom, 산물도 P₂S₅ → P₂S₇ → P₂O₃F₄). 우리 T9 는 현재 **전위 하나**로 판정한다.
   ⇒ **"전위별 산물 스위치"를 우리 코팅 판정에 추가할 수 있다** (계산 비용은 상평형도 재구성뿐).
3. **양극 축과 SE 축의 구동력 스케일이 다르다.** figure-read 로 2.8 V 에서 NCM↔코팅 **−395** vs
   LPSCl↔코팅 **−47 meV/atom** — **8배**. 우리 `cascade_stability_axes.csv` 도 `dE_LCO_full` 과
   `dE_LPSCl` 을 같은 단위로 나란히 놓는데, **정규화해서 기하평균에 넣으면 이 8배 스케일차가 사라진다.**
4. **`Fig. 4a` 의 비단조성**(ALO5 0.25 → ALO10 0.45 → **ALO20 0.35**)은 우리가 도펀트 **농도 3점**
   (x=0.02/0.05/0.10)을 평균해서 쓰는 관행에 대한 경고다. **최적점이 중간에 있으면 평균은 그것을 지운다.**
   (이미 `audit_label_scatter.py` 가 같은 걱정을 하고 있다 — 이 리뷰가 **문헌 실측 사례**를 준다.)
5. **`Fig. 3b` Cl 2p Clₓ⁻ 지표**를 우리 "Cl-rich 산화" 서사의 **실험 대응물**로 인용한다.
   우리는 계산으로 *"Cl 은 onset 이 아니라 분해 양·산물에 작용한다"* 고 말하는데,
   HE-LIC vs LIC 의 Clₓ⁻ 면적 차이가 정확히 *"산물 쪽 차이"* 를 실험으로 보여준다.
6. **확보할 원문 — 2건 (1건은 이미 갖고 있었다)**
   - **[32]** D. Wang, C. Liu, R. Wang et al., *Angew* **64**, e202501411 (2025) —
     **★ 1순위.** ★1 σ-하락 주장을 검증할 **유일한** 경로. 리뷰는 사이클 수명만 옮겼고 σ 수치를 안 옮겼다.
   - **[88]** J. Cui, Z. Wang, J. Tan et al., *ACS AMI* **17**, 22014 (2025) —
     **우리 조성 `Li₅.₄PS₄.₄Cl₁.₆` 가 이름으로 등장하는 유일한 문헌**(Al 음극 대비, "redox-active interphase").
   - ✅ **[91]** Qian, Nazar et al., *Angew* **64**, e202413591 (2025) — **이미 보유·digest 완료**:
     `litdb/papers/qian2025_lipo2f2_coating_stable_cei.md` (= 업로드 `99737a54-73. …`). §5-1 교차검증 참조.
     ⇒ **`Fig. 6a–f` 를 인용할 때는 이 리뷰가 아니라 우리 qian2025 digest 를 인용한다.**

## 9. 인용 가능 문장 (deck / paper 용)

- "Recent reviews frame the interface — not the bulk conductivity — as the limiting factor for practical solid-state batteries, arguing that the next generation will be defined by interface engineering rather than by the discovery of a single 'super-electrolyte' [Liang et al., *Battery Energy* 2026, 5:e70137]."
- "Sulfide argyrodites are predicted by DFT to oxidize at 2.1–2.5 V vs Li⁺/Li while cells routinely operate at 3.5–4.2 V; this gap is attributed to kinetic passivation by the interfacial decomposition layer [Liang 2026, citing Chai et al. 2024]." — **우리 2.256 V 를 이 대역에 놓는 문장으로 쓸 수 있다.**
- "High electronic conductivity, rather than mechanical properties, has been identified as the root cause of internal lithium dendrite formation in solid electrolytes [Liang 2026, citing Han et al., *Nat. Energy* 2019]." — **우리 PDOS(CBM 에 Li 부재) so-what 의 문헌 받침.**
- "DFT-based grand potential phase diagrams have become the standard computational tool for predicting the thermodynamic stability of electrolyte/electrode interfaces [Liang 2026]." — **우리 T9 방법 선택의 관행 근거.**
- ⚠ **쓸 수 없는 문장**: *"도핑이 이온전도도를 낮춘다"* 를 이 리뷰로 인용하는 것.
  근거가 **무출처 논평**이고(★3) 숫자가 **없다**(★2). 쓰려면 **[32] 원문을 확보해야 한다.**

## 10. 주의 / 한계 ★ — 비판

이 리뷰는 **폭이 넓고 정리가 깔끔하지만, 검증 가능성이 낮다.** 실측한 결함을 순서대로 적는다.

**10-1. 🔴 핵심 주장에 인용이 없다.** ★1 의 σ-하락 블록 전체가 무출처다(★3).
같은 패턴이 반복된다 — Li₆PS₅Cl/Br/I 의 σ 세 값(무출처), 황화물 20–40 GPa / LLZO 150 GPa(무출처),
LLZO 도핑 후 1–2 × 10⁻³ S cm⁻¹(무출처), 양극 부피변화 2–7 %(무출처).
**리뷰에서 인용 없는 정량 진술은 그 리뷰 저자의 기억이다.** 우리는 그것을 인용할 수 없다.

**10-2. 🔴 `Fig. 6l` 이 본문을 부인한다 — "interfacial energies" 오귀속.**
본문(p.13): *"By employing higher-fidelity r²SCAN calculations for **interfacial energies**, they achieve more
reliable stability predictions compared to the commonly used PBE, which is known to underestimate formation
and **interfacial** energies."*
그런데 같은 쪽 캡션은 *"(l) Validation by r²SCAN shows that **84 % of discovered binary and ternary crystals
retain negative phase separations**"* 이고, **그림의 축 이름도 "Phase-separation energy"** 다(figure-read).
Merchant et al. **[93]** 은 **상분리에너지(=hull 안정성)** 를 r²SCAN 으로 재검증한 것이지 **계면에너지를 계산한 적이 없다.**
⇒ **이 리뷰에서 "interfacial energy" 라는 말이 등장하는 유일한 자리가 오귀속이다.**
★7 의 답이 "없다"가 되는 이유의 절반이 여기 있다.

**10-3. 🔴 `Fig. 5b` 가 본문 수치와 안 맞는다.**
본문: LLZTO 총 이온전도 **2.59 → 6.92 × 10⁻⁴ S cm⁻¹ (×2.7)** **[18]**.
그림 figure-read(1000/T = 3.3): pristine ln(σT) ≈ **−7.90**, ALO10 ≈ **−7.45** ⇒ **Δ ≈ 0.45 → 비 ≈ 1.6×**.
게다가 절대값이 안 맞는다 — ln(σT) = −7.45 이면 T=303 K 에서 **σ ≈ 2 × 10⁻⁶ S cm⁻¹** 로,
본문의 6.92 × 10⁻⁴ 보다 **3 자릿수 낮다**. 고온단(1000/T=2.83)에서는 비가 **1.17×** 로 더 작다.
원인 후보: 원 논문 **[18]** 의 축 라벨 오기 / 본문값이 다른 시료·다른 측정(RT EIS)에서 온 것.
**이 리뷰만으로는 판별 불가** ⇒ **×2.7 도 1.6× 도 인용하지 않는다.**

**10-4. 🟠 `Fig. 4a` 의 비단조성을 본문이 침묵한다.**
그림은 **0.15 / 0.25 / 0.45 / 0.35 mA cm⁻²** 네 값을 다 보여주는데 본문은 **양 끝 두 개만** 인용한다.
**ALO20 이 ALO10 보다 나쁘다**는 사실 — 즉 **"코팅을 더 두껍게 하면 도로 나빠진다"** — 이
리뷰의 서사(*"GB complexion 이 CCD 를 3배로"*)에 불편해서 빠진 것으로 보인다.
⚠ 이것은 **★4/★5 와 같은 구조의 오류**다: **개선축이 단조라고 암묵 가정하기.**

**10-5. 🟠 `Fig. 2a` 로는 본문의 두께 비교를 확인할 수 없다.**
5 nm 시료(A)는 **20 µm** 스케일바, 10 nm 시료(B)는 **1 µm** — 배율이 20배 다르다.
*"10 nm 시료의 계면상은 각 방향 ~4 µm 만 뻗는다"* 는 문장을 **B 패널(1 µm 시야)에서 읽을 수 없다.**

**10-6. 🟠 면적 저항 단위가 `Ω cm³` 로 적혀 있다** (2회: Li₃PO₄ 코팅 ~5–10 Ω cm³, Li\|LLZO ~10⁻¹ Ω cm³).
면적비저항은 **Ω cm²** 다. 원 논문의 표기인지 리뷰의 오타인지 불명 ⇒ **그대로 인용 금지**.

**10-7. 🟠 `Fig. 2a` 는 음극 계면 연구인데 §3.1(양극-전해질 계면)에 배치돼 있다.**
**[51]** Götz et al. 의 제목이 *"Characterization of the **Lithium**/Solid Electrolyte Interface…"* 이고,
리뷰 본문도 *"at the **lithium**/solid electrolyte interface"* 라고 쓰면서 그 문단을 양극 절 안에 뒀다.
구조 편집의 실수.

**10-8. 🟠 캡션 번호 오기.** `Fig. 6` 캡션이 *"(e) Thermodynamic evaluation … between NCM and LiPOF at
(e) 2.8 and (f) 4.3 V"* — `(e)` 가 두 번 나온다(`(e and f)` 여야 함).
`Fig. 2`·`Fig. 6` 캡션의 저작권 표기 *"American **Society of Chemistry**"* 는 **American Chemical Society** 의 오기.

**10-9. 🟡 심사 15일 · 편집장이 공저자.** 접수 2026-06-03 → 수락 2026-06-18.
논문 스스로 이해상충을 밝히고 배제 조치를 적었으므로 절차상 문제는 없지만,
**위 10-1 ~ 10-8 의 밀도(18쪽에 8건)와 무관하지 않다고 본다.**

**10-10. ⛔ 우리 쪽 규율.** 이 리뷰의 어떤 값도 `db/properties/canonical_registry.json` 에 넣지 않는다.
`comparison_vs_ours.md` 에서도 **물성 4축(A–D) 금지**, **방법·개관 축(J-12 신설안)** 에만 둔다 — §17.

---

## 11. 절별 상세 (본문 순서대로 · 숫자 전부)

### §1 Introduction (p.1–2)
- LIB 팩 수준 **250–300 Wh kg⁻¹** 한계 **[1, 2]**; ASSB 는 셀 수준 **> 500 Wh kg⁻¹** 가능 **[3, 4]**.
- 중심 명제: *"The central obstacle … is **the interface problem**."* 액체는 젖고 부피변화를 유체로 흡수하지만
  고체는 **강체 구속 계면**이라 모든 불연속이 이온수송 저해 또는 열화 핵생성점이 된다 **[1, 5]**.
- 결합된 파손 연쇄: 계면 분해반응 → 임피던스 상승 / 스트리핑 보이드 → 전류 집중 → 수지상 / 양극 상호확산.

### §2.1 산화물 가넷 LLZO (p.2–3)
- LLZO 첫 보고 **[10]** Murugan 2007: cubic **~3 × 10⁻⁴ S cm⁻¹**, 알루미나 도가니 유래 **Al 도핑**으로 cubic 안정화.
- 구조: LaO₈ 12면체 + ZrO₆ 8면체 골격, Li 는 **사면체 24d** 와 **찌그러진 8면체 96h**; 전도는 **빈자리 매개 hopping**, 사면체 → 8면체 bottleneck (`Fig. 1a`) **[4, 9]**.
- ★ **aliovalent 도핑 문단** (= 스니펫 조각 1): Zr⁴⁺ → **Ta⁵⁺/Nb⁵⁺/W⁶⁺/Te⁶⁺** 가 Li 빈자리를 넣어 cubic 안정화 + 캐리어 농도 최적화; Li⁺ 자리 **Ga³⁺/Al³⁺** 도 cubic 안정화 ⇒ **1–2 × 10⁻³ S cm⁻¹**, "액체의 2–5배 이내".
- Cheng et al. **[15]**: LLZO 의 구조·전도도 최적화는 **성숙 단계**, 분야는 고온 소결 후막 → **저온 공정 박막·유연 LLZO-폴리머 복합**으로 이동 중.
- 입계: GB σ 가 벌크보다 **2–3 자릿수 낮다** — Li₂CO₃·LiOH 저항성 2차상 **[18]**; Li₂CO₃ 는 미량 CO₂/H₂O 로 자발 생성돼 **~5–10 nm** 부동태막 **[19]**.
- 대응 2계열: ① GB complexion 자체를 겨냥한 첨가제(**Li₃PO₄, Li₃BO₃, Al₂O₃**) → 비정질 입계막 ② **3D 전자절연 망**을 2차상으로 **[20]**.
- 표면: 같은 Li₂CO₃ 가 용융 Li 젖음을 막아 고저항 Li/LLZO 계면 → 연마·산 에칭·분위기 어닐링. 그리고 **높은 강성 때문에 소성변형으로 부피변화를 못 받아** 보이드·접촉 손실 **[3, 21, 22]**.

### §2.2 황화물 LGPS·argyrodite (p.3–4)
- LGPS **[24]** Kamaya 2011: **12 mS cm⁻¹**. 구조 = LiS₄ 사면체·LiS₆ 8면체의 1D 사슬이 (Ge₀.₅P₀.₅)S₄ 정방 골격으로 연결된 준등방 3D 경로, Li 가 채널에 **비편재(준연속 분포) = 결정 골격 안의 액체형 부분격자**.
- **핵심 개념**: 골격 음이온 **분극률 ↔ σ**. S²⁻ 가 O²⁻ 보다 분극률이 커 Li⁺–골격 정전상호작용이 약해지고 이동장벽이 낮다 — *"softer, more polarizable anionic lattices facilitate faster ion transport"* **[3]**.
- argyrodite (`Fig. 1b`): S²⁻ fcc 골격 + P⁵⁺ 사면체(PS₄³⁻) + Li 다중 부분점유 자리의 **cage 형 경로**. **X⁻ 가 별도 결정자리를 차지하고, 그 정체가 Li 부분격자 무질서 → σ 를 좌우** **[25, 26]**.
- σ: Cl **~3–5**, Br **~6–8**(안정성 열세), I **~1 mS cm⁻¹**(자리무질서 제한). 큰 I⁻ 는 격자를 늘리고, 작은 Cl⁻ 는 **Li hopping 에 유리한 자리에너지 분포**를 만든다 **[1, 27]**. ⚠ **세 값 무출처**.
- 산화: DFT **2.1–2.5 V** vs 실셀 **3.5–4.2 V** → **속도론적 부동태화**로 설명하되 그 층은 사이클 중 계속 자라 용량감소·임피던스 상승 **[28]**. 고온 사이클 열화 기구는 **[29]** Ando et al., *Battery Energy* **2**, 20220052 (2023): 양극 SE 산화 + 음극 SE 환원의 순차 진행.
- 수분: **[30]** Nikodimos et al., *ACS Energy Lett.* **9**, 1844 (2024) — Lewis 산 첨가제(트리페닐카베늄 BF₄, 트리틸륨 PF₆, TCNE)로 표면 부동태화 → **H₂S 발생 80 % 이상 감소**.
- 조성공학 **[31]**: ① **high-entropy argyrodite** (P 자리 Si/Ge/Sn + 할라이드 자리 Cl 공도핑) → **≈8 mS cm⁻¹** + 급속충전 안정성 **[26]**; 배후 원리 = **배치 엔트로피로 고전도상 안정화, 사이클 중 상전이 억제**.
  ② ★ **전자국재화** (Y@LPSCl) **[32]** — ★1 문단.
- 기계: 황화물 **20–40 GPa** vs LLZO **~150 GPa** ⇒ 냉간압축으로 상대밀도 **> 90 %** 달성 가능(고온 소결 불필요)하지만 스택압에서 **크리프·압출**에 취약. Li/황화물 계면의 기계적 변형이 수지상 거동의 결정인자 **[33]**.

### §2.3 할라이드 Li₃MX₆ (p.4–5)
- 2018 이후의 신생 계열 **[12]**. 첫 보고 **[34]** Asano 2018: **Li₃YCl₆·Li₃YBr₆ 10⁻⁴–10⁻³ S cm⁻¹**, 높은 변형성 + **보호코팅 없이 4 V급 양극과 양립**.
- 구조 공간: M³⁺ = **Y, In, Sc, Er, Yb, Ho** × X⁻ = Cl, Br, I; hcp 음이온 골격의 **ordered ↔ disordered 변종** (`Fig. 1c`).
  ★ **"More disordered phases … exhibit faster ion transport due to the broadening of the site-energy distribution"** **[35, 36]** — ★4 의 (b) 기구.
- Li₃YCl₆ 의 **새 결정구조**가 보고돼 *"예측 σ 와 측정 σ 의 불일치"* 를 설명. **Yb 계**: 작은 이온반경 → 조밀 골격 → Li⁺ bottleneck 이 **최적 중간값**(고정 양이온은 배제, Li⁺ 는 빠르게 통과) **[35]**.
- ★ **산화안정성이 이 계열의 정체성**: Li₃YCl₆·Li₃InCl₆ **> 4.3 V**(DFT) ≫ argyrodite ~2.5 V ⇒ **LiCoO₂·NMC·Co-free LiNiO₂ 와 코팅 없이 직접 페어링** **[37]**.
- **[36]** Song 2024: M³⁺ 주변 **국소 격자왜곡**으로 산화 onset **~4.25 → ~4.4 V** ⇒ *"안정성은 벌크 조성의 열역학적 성질만이 아니라 **국소 배위환경**으로 조절 가능하다"*.
- **[38]** Lin 2025 (= 스니펫 조각 3): 반-페로브스카이트 할라이드에 **ML 조성설계 + 고처리량 스크리닝**으로 후보 라이브러리를 훑어 유망종 다수 식별. ⚠ **숫자 0개.**
- 약점: 수분 가수분해(HCl·HBr 발생) — In 계가 Y 계보다 강건 **[39]**; **Li 금속 대비 환원 불안정** — Li 가 M³⁺ 를 환원하고 **LiCl** 이 주 분해산물, 생성된 계면상이 **혼합 이온-전자 전도체**라 환원이 계속돼 두꺼워짐 **[40]** (XPS 깊이 프로파일).
  ⇒ 결론: **할라이드는 만능이 아니라 하이브리드 셀의 *양극 쪽* 전해질** **[37]**.

### §3.1 양극-전해질 계면 (p.5–8)
- 4대 요구: 화학적 안정 / 3.0–4.5 V 전기화학 안정 / 낮은 계면저항 / 부피변화(층상 **2–7 %**) 수용 **[43–45]**.
- **SCL(공간전하층)** — Takada 나노이온학 틀 **[46, 47]**. Li 화학퍼텐셜 차 → Li⁺ 재분배 → 전해질 쪽 **Li 고갈층**.
  산화물/산화물(LiCoO₂/LLZO): **10–50 nm**, 국소 Li⁺ **수 자릿수** 감소 **[21]**.
  황화물: 유전상수가 커 화학퍼텐셜 차를 부분 차폐 → SCL 완화 **[48]** ⇒ *"황화물 ASSB 의 양극 계면저항이 산화물보다 낮은 이유의 하나"*.
  할라이드: ① 높은 벌크 Li⁺ 농도 → Debye 차폐길이 nm 급 ② 할라이드 음이온과 산화물 양극의 화학퍼텐셜이 더 가까움 ⇒ SCL 더 약함. **단 > 4.3 V 에서 Cl⁻ 산화분해가 SCL 밖의 별도 열화경로를 연다** **[49]**.
- **상호확산**: 양극 → 전해질(Co, Mn, Ni), 전해질 → 양극(La, Zr, P, Ge). 고온 공소결에서 활성화.
  **[50]** Kim 2024: **ALD Li₃PO₄** 등각 코팅이 700 °C 공소결에서 Co/La 상호확산 + 상호분해를 억제(`Fig. 2b`).
  ★ **핵심 통찰**: *"코팅재가 좋은 이온전도체일 필요가 없다"* — Li₃PO₄ σ ~10⁻⁶ S cm⁻¹ 이지만 **5–10 nm** 두께라 기여 면저항이 **~5–10 Ω cm³**(원문 단위)로, 그것이 막아 주는 훨씬 두꺼운 상호확산층 저항에 비해 무시 가능.
- 코팅 2노선: **ALD/MLD**(옹스트롬 두께 제어; Al₂O₃, TiO_x, ZnO, LiAlO₂, LiNbO₃, Li₃PO₄, LiPON **[55]**) vs **습식·졸겔**(LiNbO₃, Li₄Ti₅O₁₂, Li₃BO₃) — 박막/마이크로셀은 ALD, 분말 공정은 습식 **[56, 57]**.
- **[51]** Götz: TiO_x(**1.5 ≤ x ≤ 2**)가 혼합 이온-전자 전도체로 전하이동을 돕고 Li/SSE 직접접촉을 막는다 (`Fig. 2a`).
- **Co-free LiNiO₂**: 표면반응성·구조불안정이 심하다 **[52]**. 이중 인산염 개질은 사이클 안정성을 크게 올리지만 **H2–H3 전이를 부분 억제해 용량 활용률이 떨어진다**(`Fig. 2c`).
  **[58]** L. Wang, *Nat. Nanotechnol.* **19**, 208 (2024) — **"outside-in"**: LNO 입자 표면을 Al·Zn 으로 농화해 **LAZO(Li_xAl_yZn_zO) ~4 nm** 층 형성(등각 코팅 + 근표면 도핑의 결합) → 고SOC 계면분해·산소손실 억제, LGPS 로 **> 400 Wh kg⁻¹**, **> 500 cycles**.
- 할라이드 양극계면: 코팅 불필요. **[36]** 의 HE-LIC vs LIC **Cl 2p XPS**(`Fig. 3b`) — HE-LIC 은 사이클 후에도 pristine 과 거의 같고 고결합에너지 미세 피크(**Clₓ⁻ 산화종**)만 → 임피던스 소폭 상승; LIC 은 피크 형상이 변하고 **Clₓ⁻ 가 넓게** 자라 → 계면저항 급증·용량 급감.

### §3.2 음극-전해질 계면과 수지상 (p.8–11)
- **§3.2.1 열역학 vs 속도론**: μ_Li ≈ **−3.04 V vs SHE**. DFT 대전위 상평형도를 **수백 조성**에 돌린 결과
  **Li 금속에 열역학적으로 안정한 것은 LiF·Li₂O·Li₃N·Li₃P 같은 일부 2원 화합물뿐** — LLZO·LGPS·**모든 argyrodite** 는 불안정하고 SEI 로 **속도론적 부동태화**될 뿐.
  ★ 그런데 **고체에서는 그 부동태화 패러다임이 취약하다**: 액체는 SEI/용액 계면에 반응물을 대류로 보충해 조밀·자기제한 막이 되지만, 고체는 부피구속 때문에 SEI 성장이 내부응력을 낳고 **균열 → 신선면 노출 → 추가 분해** 의 **기계화학 루프**를 만든다 **[28]**.
- **[63]** Shinde: Li·Na·K·Mg·Zn·Al·Ca 7종 음극 일반원리 — *"금속이 무를수록 소성변형으로 접촉을 유지하지만 크리프 유도 형태변화에는 더 취약"*.
- **§3.2.2 수지상 3기구** — **Monroe–Newman 판정(분리막 전단탄성률 > Li 의 2배)은 고분자용이고 고탄성률 무기 SSE 에는 적용 불가** **[67–69]**.
  1. **보이드 유도 필라멘트** **[59]** Kasemchainan 2019 (`Fig. 3a`): 스트리핑 시 Li 제거 속도 > 크리프 보충 속도 → 계면 미세 보이드. **임계 스트리핑 전류 = Li/Li₆PS₅Cl/Li, 3 MPa 에서 0.2 mA cm⁻²** 로 낮고, 이것이 실셀의 율속 인자인 경우가 많다(임계 플레이팅 전류보다 낮음, 스택압 의존 강함). 보이드 가장자리에서 국소 전류밀도가 **임계 플레이팅 전류(LLZO ≈0.6, LPSCl 0.2–1.0 mA cm⁻² @3–7 MPa)** 를 넘겨 필라멘트 개시 **[70]**.
  2. **입계 침투**: 다결정 LLZO 에서 GB 의 전자전도가 벌크보다 높아 GB 에 도달한 Li⁺ 가 **전해질 내부에서 환원** → 필라멘트 → 팁 응력이 GB 균열 전파. **[72]** Han 2019 *Nat. Energy*: operando **중성자 깊이 프로파일(NDP)** 로 전자전도성 전해질 **내부**의 Li 석출을 직접 가시화 — ★ *"기계적 성질이 아니라 **높은 전자전도**가 내부 수지상의 근원"*.
  3. **전자전도 유도 내부환원**: 균열·보이드 없이도 내부 핵생성. **[18]** Wang: GB complexion 개질(ALD 유전층)로 이 경로를 억제 → **CCD 0.15 → 0.45 mA cm⁻²** (`Fig. 4a`; Li\|LLZTO\|Li, 25 °C, 펠릿 **~15 MPa** 압축이나 **외부 스택압 없이**, **0.05 mA cm⁻² 증분**). **[75]** Xiong: 입계에 **강유전 BaTiO₃** 를 넣어 내부 전기장으로 전자는 밀어내고 Li⁺ 는 통과.
  ⇒ *"세 기구가 동시에 작동하므로 단일 대책으로 안 된다."*
- **§3.2.3 완화**: 인공 SEI 중간층 **[33]**(PEO-LiTFSI/LATP 5 wt%, **~8 µm** → CCD **1.0 → >1.6 mA cm⁻²**, 60 °C 0.2 mA cm⁻² 에서 **~2800 h**) / MOF 유도체 **[77]** / **계면상 층상화** **[78]**(`Fig. 5a`: MgF₂ + 2Na → 2NaF + Mg, SSE 쪽 전자차단-이온전도층 + 음극 쪽 혼합전도층의 **경사 계면상**) / **합금 음극**(Li-In, Li-Si, Li-Mg, Li-Al; Li-Si 이론용량 **3579 mAh g⁻¹** **[79]**) / **압력**(제조압 vs 스택압이 **다르고 때로 상반된다** **[80]**; 최적창은 전해질별 — 황화물 **3–10**, 할라이드 **5–20**, 가넷 **~0–30 MPa** **[81, 82]**) / **불소화** **[74]**(F-LLZO 사이클 수명 `Fig. 4b`).
- **[82–85]** Krauskopf: **Li\|LLZO 고유 전하이동저항은 ~10⁻¹ Ω cm³ 로 매우 낮다** ⇒ 실전 전류밀도를 제한하는 것은 **속도론이 아니라** 측면 Li 성장·Li 금속 내 빈자리 확산·전기화학-기계적 파괴. ★ *"Li/SSE 계면 문제는 kinetic 이 아니라 morphological·mechanical 이다"*.
- **§3.2.4 Li 너머**: Na 는 Li 와 정성적으로 유사(융점 98 vs 181 °C → RT 크리프 빠름 → 자가치유 가능성) **[87]**. 다가이온(Mg, Zn, Al, Ca)은 전하밀도가 커 골격과 강하게 상호작용, 계면 전하이동이 느리다 — **기구 이해가 아직 제한적** **[63]**.
  Zn: 하이드로겔/폴리머 전해질은 성숙했으나 수지상 문제. Ca: 이온절연 부동태막 + Ca²⁺ 전도체 희소. **Al: 할라이드와 특유의 비양립** — **[88]** Cui 2025: Al/할라이드는 할라이드의 **연속 환원분해**로 실패하고 **In 금속이 축적돼 이온수송을 물리적으로 차단**. ★ 대조적으로 **황화물(Li₅.₄PS₄.₄Cl₁.₆)은 redox-active 계면상을 형성해 가역 사이클** (§3-4).

### §3.3 입계 (p.11)
- 동기 3가지: GB σ ≪ 벌크 / 수지상이 GB 를 따라 전파 / GB 가 수분·오염의 진입로.
- **[18]** Wang GB complexion 실물 레시피: 그린 펠릿에 **ALD Al₂O₃** → **1150 °C 소결** → 알루미나가 표면 Li₂CO₃ 를 분해하고 Li₂O 와 반응해 **서브마이크론 γ-LiAlO₂ + 나노 complexion** 형성, 대기 중 Li₂CO₃ 재생 억제. 결과: 총 σ **×2.7 (2.59 → 6.92 × 10⁻⁴ S cm⁻¹)**, CCD **3배 (0.15 → 0.45)**, Li 젖음성 유지 (`Fig. 5b`) ⚠ §10-3.
  ⇒ *"GB 공학은 이온·전자 수송을 **함께** 다뤄야 한다 — 수지상 핵생성 기구에서 둘이 결합돼 있다."*
- **[75]** field-responsive GB(압전/강유전 GB 상 → 내부장으로 전자만 배척) = **이온·전자 GB 수송의 분리**.
- **[20]** glass-network garnet: **50Li₂O–38B₂O₃–12SiO₂** 유리상이 GB 에 연속 3D 골격 → 장거리 전자 퍼콜레이션 차단, 이온경로는 보존 ⇒ **CCD > 2 mA cm⁻²** (미개질 LLZO 의 **10배 이상**, 황화물과 경쟁 가능).
- ★ **미해결**: *"The question of whether grain boundaries should be **amorphous or crystalline** remains actively debated."* 비정질 GB = 등방수송·변형수용 but σ 낮음; 결정 GB = σ 높음 but 파세팅·균열. 절충안 **"grain-fusion"** → 총 σ **> 10⁻³ S cm⁻¹** + 높은 CCD **[74]**.

### §4 계산·AI (p.11–14) → §12 표
### §5 전망 (p.14–15) → §14 목록

---

## 12. ★6 "Computational Discovery" 절이 정리하는 파이프라인 — **단·판정량·문턱·탈락 수**

> ⚠ 의뢰 취지(Basu 2026 의 *"3단 깔때기인데 어느 단에서도 탈락 0, 실체는 재채점"*)로 검사했다.
> **결론: 이 리뷰로는 그 검사를 할 수 없다 — 리뷰가 단별 탈락 수를 하나도 보고하지 않기 때문이다.**

| # | 파이프라인 | 원 출처 | 단(tier) 구조 | 판정량 | **문턱** | **탈락 수** |
|---|---|---|---|---|---|---|
| 1 | **GNoME (GNN 대규모 스크리닝)** | **[93]** Merchant, Batzner, Schoenholz, Aykol, Cheon, Cubuk (Google DeepMind), *Nature* **624**, 80 (2023) | 명시된 단 구조 **없음**. 리뷰는 3개 수를 나열: **2.2 M 후보 → 384,000 stable → 736 실험 확인** (+ 45,500 novel prototypes, XtalFinder) | 안정성(상분리에너지) | ⛔ **문턱 미기재** (E_hull 값 없음) | ⚠ **"탈락"으로 보고되지 않음.** 2.2 M − 384 k 는 *예측 결과*이지 게이트 통과/탈락 장부가 아니다. **단별 수 없음** |
| 1b | 위의 **r²SCAN 재검증** | 동 | 2차 fidelity 재계산 | 상분리에너지 부호 | 음수 유지 여부 | **16 % 가 부호를 못 지킨다**(= Stable 84 %, `Fig. 6l`). ★ **리뷰 전체에서 "탈락률"에 가장 가까운 유일한 수** |
| 2 | **반-페로브스카이트 ML 스크리닝** | **[100]** H. Liu, Z. Chen, J. Hu, X. Liu, J. Wu, J. Lin, *J. Power Sources* **658**, 238376 (2025) | ① Extra Trees 를 **실험 σ 데이터셋**에 학습 ② **단계적 A/B 자리 치환**으로 **168 순수조성 → 149,480 도핑후보** 확장 ③ **동시(joint) 필터** | σ, band gap, E_hull, tolerance factor | ★ **유일하게 명시**: **σ > 10⁻⁴ S cm⁻¹** · **gap > 4 eV** · **E_above_hull < 50 meV/atom** · tolerance factor | **생존 963종** (149,480 중 **0.64 %**). ⚠ **필터별 분해는 없다** — 어느 문턱이 몇 개를 죽였는지 리뷰에 없다 |
| 3 | **다중스케일 위상학습 초이온전도체 탐색** | **[99]** D. Chen, B. Wang, S. Li et al., *JACS* **147**, 20888 (2025) | 원자/결정/**미세구조(입계)** 3스케일 기술자 결합 | (미기재) | ⛔ **없음** | ⛔ **없음** |
| 4 | **반-페로브스카이트 ML + HTS** (= 스니펫 조각 3) | **[38]** C. Lin, L. Zhang, Y. Dong, *J. Energy Storage* **125**, 116990 (2025) | "extensive candidate libraries" | (미기재) | ⛔ **없음** | ⛔ **없음.** *"identified several promising"* 뿐 |
| 5 | **end-to-end ML 파이프라인** | **[101]** V. Jain, Z. Wang, F. You, *Mater. Horiz.* **13**, 15 (2026) | 데이터 통합(DFT+실험+문헌마이닝) + **불확실성 정량** + **능동학습 우선순위화** | — | ⛔ **없음** | ⛔ **없음.** 리뷰의 소득은 *"모델 선택만큼 **파이프라인 구조**가 정확도를 좌우한다"* 라는 명제 |
| 6 | **2D CNN + 물리정보 기술자 (수지상 형태 예측)** | **[102]** Z. Zhao et al., *Battery Energy* **4**, e70015 (2025) | 스크리닝 아님(예측) | 수지상 형태·성장 | — | 순수 데이터기반 대비 **정확도 ~20 % 향상** |
| 7 | **LLM 특성화 군집화 (MOF 전해질)** | **[103]** Z. Xi, X. Xu, H. Gao, G. Wang, *Materials Today* **93**, 103225 (2026) | 기보고 MOF 복합체 **수백 편**의 XRD/BET/EIS/NMR 을 LLM 이 군집·해석 → 숨은 상관 → 신규 조성에서 실험검증 | 합성-구조-물성 규칙 | ⛔ **없음** | ⛔ **없음** ("hundreds" 만) |
| 8 | **AI 생태계 비전** | **[104]** Z. Wang, W.G. Zeier, F. You, *Sci. Adv.* **11**, eaea0638 (2025) | LLM 문헌마이닝 + GNN 물성예측 + 물리정보 ML 계면안정성 + 로봇실험의 폐루프 | — | — | — (비전) |
| 9 | **디지털 트윈** | **[105]** J. Lee et al., *Battery Energy* **2**, 20220061 (2023) | 물리기반 FEM(이온수송·전극속도론·역학) + 실험(EIS·사이클·열) 연속 갱신 | 열화기구 분해·잔여수명 | — | — |

### 12-1. ★ 판정

- **9개 파이프라인 중 문턱을 밝힌 것 = 1개** (`[100]`), **생존 수를 밝힌 것 = 2개** (`[93]`, `[100]`),
  **단별 탈락 수를 밝힌 것 = 0개.**
- ⇒ **Basu 2026 형 병리("어느 단에서도 탈락 0")를 이 리뷰로는 진단할 수 없다.** 진단하려면
  `[93]`·`[100]` 원문을 직접 봐야 한다. **의뢰 지시대로 "탈락 수 없다"고 적는다.**
- 다만 **구조적으로 같은 냄새**가 나는 곳이 하나 있다: `[93]` 의 **r²SCAN 재검증**은
  84 % 를 "통과"시키는데, 그 84 % 는 **후보를 걸러내려고 돌린 게 아니라 이미 발표한 결과를
  사후 검증한 것**이다. **탈락이 아니라 재채점**이라는 점에서 Basu 의 Tier 2/3 와 같은 층위다.
- ⚠ 리뷰가 `[100]` 의 필터를 **"jointly filtering"** 이라고 명시한 것은 오히려 중요하다 —
  **순차 게이트(funnel)가 아니라 동시 교집합**이다. 우리 cascade 는 순차 게이트로 짜여 있고,
  순차/동시 선택은 **각 단의 탈락 수를 정의할 수 있는가**를 가른다.
  ⇒ **동시 교집합에서는 "단별 탈락 수"가 애초에 정의되지 않는다.** 이것도 답의 일부다.

---

## 13. ★7 계면 저항·계면 상용성을 무엇으로 정량하나 — **그리고 슬랩 규약은 다루지 않는다**

### 13-1. 리뷰가 실제로 쓰는 계면 정량량 (5종)

| 정량량 | 어디서 | 값의 예 | 우리 대응 |
|---|---|---|---|
| ① **대전위 pseudo-binary 상호반응에너지** `ΔE_rxn` [meV/atom] vs x, **전위 고정** | `Fig. 6b–f` **[91]** | LPSCl↔LiP(OF)₂: **−145**(무전위) / **−43**(2.8 V, 원전값) / **−96**(4.3 V); NCM↔LiP(OF)₂: **−395**(2.8 V) / **−108**(4.3 V) — §5-1 에서 원전과 교차검증 | ★ **우리 T9 `dE_LPSCl`·`dE_LCO_full` 과 같은 구성**(닫힌계 pseudo-binary, Richards/Ong 2016 eq 2). **게이트 `\|ΔE_rxn\| < 100 meV/atom` 은 리뷰가 안 옮긴다** — 원전은 Xiao 2019 filter 4 |
| ② **전기화학 안정창** (대전위 Li-content vs V) | `Fig. 6a` **[91]** | LiP(OF)₂ **2.6–4.9 V**, 양쪽 분해산물 명시 | 우리 ESW(comp1/modelc onset 2.256 V) |
| ③ **CCD / 임계 스트리핑 전류** [mA cm⁻²] | `Fig. 4a`, §3.2.2 | 0.15/0.25/0.45/0.35; 0.2 @3 MPa; >1.6; >2 | ⛔ 우리 축 없음 (실험량) |
| ④ **면적비저항** [원문 Ω cm³] | §3.1, §3.2.3 | Li₃PO₄ 코팅 ~5–10; Li\|LLZO 고유 ~10⁻¹ | ⛔ 우리 축 없음 |
| ⑤ **XPS 산화종 피크 면적** (Clₓ⁻) | `Fig. 3b` **[36]** | 정성 (HE-LIC 미량 ↔ LIC 뚜렷) | 우리 "Cl-rich 산화 산물" 축의 실험 대응물 |

### 13-2. 🔴 슬랩 규약 — **한 줄도 다루지 않는다** (키워드 전수 스캔)

의뢰가 지목한 항목을 본문 전체에서 검색한 결과:

| 키워드 | 히트 | 비고 |
|---|---|---|
| `slab` | **0** | |
| `vacuum` | **0** | |
| `termination` | **0** | |
| `mismatch` / `lattice mismatch` | **0** | |
| `strain` (strain 자체) | **실질 2** | 둘 다 계면규약 아님: *"mechanical strain without fracture"*(비정질 GB), *"strain-accommodating architectures"*(가넷 음극). 나머지 11 히트는 전부 `constrained/constraint` 의 부분문자열 |
| `work of adhesion` / `W_ad` / `adhesion` | **0** | |
| `interfacial energy` | **2** | ⚠ **둘 다 §10-2 의 오귀속 문장 안**. 실제 대상은 phase-separation energy |
| `surface energy` | **0** | |
| `supercell` / `k-point` / `cutoff` / `coherent interface` | **0 / 0 / 0 / 0** | (`coherent` 2회는 *"coherent artificial interface"*, *"coherent emerging picture"* — 결정학적 정합이 아님) |
| `epitax` | **1** | *"epitaxial interlayers"* — 전망 절의 나열 한 단어 |

⇒ **★7 의 답: 이 리뷰는 계면 상용성을 *닫힌계 대전위 열역학* 으로만 정량하고,
명시적 계면 원자모형(슬랩)을 만드는 규약은 전혀 다루지 않는다.**

### 13-3. 그래서 우리 **B2(계면) 보고량 🔴 미정의** 에 무엇을 주는가

**정의는 안 준다. 그러나 두 가지를 준다** — 둘 다 쓸 만하다.

1. **커뮤니티 기본값의 확인**: *"DFT-based grand potential phase diagrams have become **the standard**
   computational tool for predicting the thermodynamic stability of electrolyte/electrode interfaces"* **[91]**.
   ⇒ **우리 T9(닫힌계 pseudo-binary)가 관행에서 벗어난 선택이 아니라는 것**을 리뷰로 받칠 수 있다.
   ⛔ 단 이것은 *"슬랩을 안 만들어도 된다"* 는 허가가 아니다 — **다른 양을 재는 것**이고, 리뷰도 그 구분을 하지 않는다.
2. **보고량을 나눠야 한다는 실측 근거**: `Fig. 6b–f` 는 **같은 코팅재**를 두고
   **접촉 상대(LPSCl vs NCM) × 전위(0 / 2.8 / 4.3 V)** 의 **6가지 조합**을 각각 계산한다.
   최소 반응에너지가 −47 ~ −395 meV/atom 으로 **8배** 흩어지고 **산물 조성도 매번 바뀐다**.
   ⇒ **"코팅재 X 의 계면 안정성"은 스칼라로 정의되지 않는다.**
   `kb/templates/estimand_card.md` 의 판정 기준(*admissible state 가 여럿인데 선택·집계 규칙이 없으면
   스칼라 보고량은 정의되지 않는다*)에 정확히 걸린다.
   ⇒ **B2 는 `ΔE_rxn(상대, 전위)` 로 인자를 선언한 뒤에야 보고량이 된다.**
   (리뷰가 이 말을 하지는 않는다 — **그림에서 읽은 우리 판단**이다.)

---

## 14. ★8 이 리뷰가 "아직 모른다"고 적은 것 — 원고 gap 문장 재료

> 전부 원문 표현 그대로 옮겼다(위치 병기). 원고의 *"~는 아직 확립되지 않았다"* 문장에 바로 쓸 수 있다.

| # | 미해결 진술 | 위치 |
|---|---|---|
| 1 | **"no inorganic solid electrolyte system has yet demonstrated dendrite-free lithium plating at the current densities (> 5 mA cm⁻²) and areal capacities (> 5 mAh cm⁻²) required for fast-charging applications"** | §5.1, p.14 |
| 2 | **"Breaking this conductivity-stability correlation is a high-priority research direction."** (분극성 높은 골격 ↔ 낮은 산화문턱의 역상관) | §5.1, p.14 |
| 3 | **"The question of whether grain boundaries should be amorphous or crystalline remains actively debated."** | §3.3, p.11 |
| 4 | 다가이온(Mg, Zn, Al, Ca) 계면: **"This is an area where fundamental mechanistic understanding remains limited."** | §3.2.4, p.10 |
| 5 | AIMD: 실험 σ 를 **자릿수까지만** 재현 — **"sufficient for screening purposes but insufficient for quantitative prediction"**; 셀 수백 원자·수십~수백 ps 제약 | §4.1, p.12 |
| 6 | 무음극(anode-free): **"the demands on cycle life, coulombic efficiency, and interfacial stability remain extreme"** | §5.2, p.15 |
| 7 | 폐루프 AI: **"significant infrastructure and workflow challenges remain in building the unified AI ecosystems"** | §5.2, p.15 |
| 8 | 수지상: **"The multi-mechanism nature of dendrite growth implies that no single mitigation strategy will suffice."** | §5.1, p.14 |
| 9 | Y 도핑 창: *"the doping level is **tightly constrained**"* — 그런데 **창의 값이 없다** ⇒ 실질적으로 미지 | §2.2, p.4 |
| 10 | 할라이드: 수분 민감 + Li 대비 환원 불안정 ⇒ **"positioning them as cathode-side electrolytes in hybrid cell designs rather than as universal solutions"** | §2.3, p.5 |
| 11 | Li₃YCl₆ 의 새 결정구조가 **"rationalizes discrepancies between predicted and measured conductivities"** ⇒ 예측≠측정 불일치가 최근까지 미해결이었음 | §2.3, p.5 |
| 12 | 계면 중심 설계: **"This interface-centric paradigm demands continued investment in the first-principles modeling of interface thermodynamics and the atomic-scale understanding of interfacial ion transport."** ← ★ **우리 B2 작업의 정당화 문장으로 그대로 쓸 수 있다** | §5.1, p.14 |

---

## 15. 기술 미니 용어집 (이 digest 를 읽는 데 필요한 만큼)

- **Aliovalent doping (이가원자가 치환)**: 원래 자리 이온과 **전하가 다른** 이온으로 치환하는 것.
  전하중성을 맞추려면 빈자리나 격자간 이온이 **반드시** 생긴다 — 그래서 σ 를 바꾸는 가장 직접적인 손잡이다.
  LLZO 의 Zr⁴⁺ → Ta⁵⁺ 는 Li 빈자리를, Li⁺ → Ga³⁺ 는 Li 빈자리 2개를 만든다.
  (반대말 **isovalent** = 같은 전하로 치환, 빈자리 안 생김.)
- **Grand potential phase diagram (대전위 상평형도)**: Li 를 저장조(reservoir)로 두고 **Li 화학퍼텐셜 μ_Li 를
  독립변수로 삼은** 상평형도. μ_Li ↔ 전압이 1:1 대응하므로 *"이 전압에서 이 물질이 무엇으로 분해되나"* 를 준다.
  우리 ESW(comp1 2.256 V)와 `Fig. 6a` 가 같은 도구.
- **Pseudo-binary interface reaction energy**: 두 상 A·B 를 `x·A + (1−x)·B` 의 **닫힌계 혼합물**로 놓고
  x 를 훑으며 **가장 음의 반응에너지**를 찾는 것 (Richards/Ong 2016). 실제 계면 원자배열을 만들지 **않는다**
  — 그래서 싸고, 그래서 계면 **구조** 정보를 못 준다. `Fig. 6b–f` 가 이것.
- **Space charge layer (SCL, 공간전하층)**: Li 화학퍼텐셜이 다른 두 상이 닿으면 Li⁺ 가 재분배되며
  전해질 쪽에 **Li 고갈 나노층**이 생긴다. 유전상수가 클수록(황화물·할라이드) 차폐돼 약해진다.
- **Grain boundary complexion**: 입계를 "결함"이 아니라 **자체 열역학적 평형을 갖는 준-상(quasi-phase)** 으로
  보는 개념. 조성·두께가 온도·조성에 따라 정해지므로 **설계 대상**이 된다.
- **CCD (critical current density, 임계전류밀도)**: 대칭셀에서 전류를 계단식으로 올릴 때 **단락(전압 붕괴)** 이
  나는 전류밀도. 수지상 저항성의 표준 실험 지표. **스택압·온도·전류 증분에 강하게 의존**하므로
  조건 없이 값만 인용하면 안 된다 (`Fig. 4a` 는 25 °C·외압 없음·0.05 mA cm⁻² 증분).
- **임계 스트리핑 전류**: CCD 의 사촌. **플레이팅이 아니라 스트리핑**에서 Li 크리프 보충이 못 따라가
  보이드가 생기기 시작하는 전류. **보통 임계 플레이팅 전류보다 낮아 진짜 율속인자**인 경우가 많다.
- **High-entropy electrolyte**: 한 부분격자에 여러 원소를 섞어 **배치 엔트로피 −TΔS_config** 로
  고대칭·고전도 상을 안정화하는 전략. 야금학에서 왔다.
- **r²SCAN**: meta-GGA 함수형. PBE 보다 생성에너지·상분리에너지를 잘 준다.
  GNoME 가 최종 검증에 쓴 것이 이것(`Fig. 6l`).

---

## 16. ★★ §우리 cascade 방향에 주는 것 — ★1–★5 근거 초안

> ⛔ **먼저 못 하는 것부터**: 이 리뷰는 σ 하락의 **크기를 주지 않고**(★2), **출처도 없다**(★3).
> 따라서 아래 어디에도 **수치 문턱을 제안하지 않는다.** "리뷰에 없다"가 답인 항목은 그렇게 적었다.

### 16-1. 확인된 우리 쪽 사실 (코드에서 읽은 것)

| 게이트 | 정의 | **host 앵커** |
|---|---|---|
| **G1** structural | `Δe < 0` | 상대적(부호) |
| **G2** window | `window_V > 0.05 V` | 절대 |
| **G3** oxidation | `ox_V ≥ **2.14 V (host)**` ← `HOST_OX_V = 2.14` | ✅ **있다** (`build_screening_funnel.py`) |
| **G4** li_transport | `ionic_transport norm > 0.30`, 그 norm 은 `("bvs_x005", **+1**)` 의 **도펀트 풀 내 min-max** (`build_cascade_themes.py:295`) | ❌ **없다** |
| **G5** mechanical | `E ≤ median & G/B ≤ median` | 풀 내 중앙값 |

⇒ **깔때기는 이미 host 앵커를 쓸 줄 안다(G3). 이온수송 축만 안 쓴다.**

### 16-2. 리뷰가 요구하는 것 3가지 (근거 있는 것만)

**① G4 에 host 참조 부호를 넣는다 — 순위가 아니라 *방향*을 먼저 판정한다.**
- 근거: ★1 — 도핑이 σ 를 **host 아래로** 내릴 수 있다는 사례가 문헌에 존재한다(정성).
- 현재 G4 는 **도펀트끼리의 상대순위**만 본다. 전원이 host 보다 나빠도 최상위는 norm 1.0 을 받는다.
- 제안: `bvs_x005` 를 **무도핑 host 값과 같은 파이프라인으로 계산해 기준점으로 놓고**,
  `bvs_x005(dopant) < bvs_x005(host)` 인 후보에 **`σ-regression` 플래그**를 단다.
  ⚠ **탈락시키자는 말이 아니다** — 리뷰는 σ 를 내리는 도핑에도 **정당한 이유**(전자국재화 → 4800 h)가
  있을 수 있음을 같은 문단에서 보여준다. 필요한 것은 **탈락이 아니라 가시성**이다.
- **문턱은 제안하지 않는다** — 리뷰에 크기가 없다(★2). *"host 미만이면 표시"* 라는 **부호 규칙**까지만.

**② 도펀트마다 "무엇을 겨냥했는가"를 선언하게 한다 (declared purpose).**
- 근거: ★4 — σ 를 올린 9건은 전부 **캐리어 농도 / 자리에너지 분포 폭 / bottleneck 크기**를 겨냥했고,
  σ 를 내린 1건은 **전자구조**를 겨냥했다. 리뷰가 이 이분법을 **규칙으로 선언하지는 않지만**(★4),
  사례 배열이 일관되게 그 방향이다.
- 우리 조합기(`combine`)는 테마 norm 의 **기하평균**이다 — **부호가 뒤집힌 trade-off 를 평균이 지운다.**
  전자절연(`electronic_insulation`)을 노려 뽑은 도펀트가 이온수송에서 손해를 봐도, 기하평균은
  "적당히 괜찮은 후보"로 돌려준다. **그 손해가 의도된 대가인지 사고인지 구분이 안 된다.**
- 제안: 도펀트 레코드에 `intent: ionic | electronic | mechanical | interfacial` 을 넣고,
  **intent 축에서의 이득과 다른 축에서의 손실을 같은 화면에 나란히** 보이게 한다.
  ⛔ **교환율(몇 % σ 를 몇 eV gap 과 바꾸는가)은 제안하지 않는다 — 리뷰에 근거가 없다.**

**③ 농도 3점 평균을 최적점 탐색으로 바꾼다.**
- 근거 (문헌 실측): `Fig. 4a` 의 **ALO5 0.25 → ALO10 0.45 → ALO20 0.35 mA cm⁻²** — **비단조**이고
  본문은 이것을 언급조차 하지 않는다(§10-4). 그리고 ★1 의 Y 도핑도 *"insufficient ↔ excessive"* 창을 말한다.
- 우리는 `x = 0.02 / 0.05 / 0.10` **3점 산술평균**을 G1·G5 에 넣고 있다
  (`build_screening_funnel.py` 의 `load_champion_by_x` 주석이 이미 이 위험을 지적한다).
- **최적점이 x=0.05 에 있으면 평균은 그것을 깎고, 최적점이 끝에 있으면 평균은 그것을 부풀린다.**
- 제안: 3점을 **평균하기 전에 단조성 검사**를 하고, **비단조면 `argmax` 와 그 값을 함께 기록**한다.
  (이미 `audit_label_scatter.py` 가 "3점 평균 대신 하나만 써도 순위가 얼마나 움직이나"를 재고 있다 —
  **이 리뷰는 그 감사에 문헌 실측 사례를 준다.**)

### 16-3. ⛔ 이 리뷰로 **하면 안 되는 것**

- *"도핑은 σ 를 낮출 수 있으니 도핑 후보를 줄이자"* — **근거 없음.** 리뷰의 사례는 **9:1 로 σ 상승 쪽**이다(★4).
- *"Y 계 도펀트를 배제하자"* — **근거 없음.** Y 사례는 무출처 논평이고(★3), 같은 문단이
  **4800 h / 1300 cycles** 라는 이득도 같이 보고한다.
- *"σ 하락 허용 폭을 N % 로 잡자"* — **리뷰에 없다**(★2).
- 이 리뷰의 어떤 수치도 `cascade_stability_axes.csv` 나 `canonical_registry.json` 에 넣지 않는다.
- ⚠ 그리고 **`cascade_stability_axes.csv` 자체가 코팅 후보 데이터이지 도핑체 데이터가 아니다**
  (`kb/reviews/codex_BJ_prompt_cascade_redesign_2026_09_09.md` 머리 철회블록).
  **이 리뷰의 도핑 논의를 그 CSV 에 연결하지 않는다** — 두 개는 다른 질문이다.

### 16-4. 한 문장 요약

> **리뷰가 우리 깔때기에 요구하는 것은 "도핑을 의심하라"가 아니라 "무엇에 대해 좋아졌는지를 선언하고,
> host 를 기준점으로 두라"이다.** 순위는 그대로 둬도 된다 — 다만 **기준점 없는 순위는 방향을 잃는다.**

---

## 17. `comparison_vs_ours.md` 반영안 → 별도 파일

⛔ 이번 세션은 `INDEX.md` · `comparison_vs_ours.md` **직접 수정 금지** 지시라
**`litdb/_pending_index_liang2026_interface_bottleneck_solid_state_batteries.md`** 에 초안만 만들었다.
요지: **물성 4축(A–D) 금지**, **`### J-12` (계면·개관 축) 신설 + `🔧 방법 원전` 블록**으로만 반영.
