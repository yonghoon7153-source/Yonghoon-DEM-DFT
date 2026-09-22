# ⏸ 병합 대기 — `chaney2024_two_step_sei_growth_argyrodite_li_metal`

> 2026-09-22 · 1저자 지시로 **`INDEX.md`·`comparison_vs_ours.md`·`db/literature/refs.json` 직접 수정 금지**(다른 에이전트가 병합 중). 넣을 내용을 여기 적어 둔다.
> **⛔ 커밋하지 않았다.** 건드린 파일은 `litdb/papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md` 와 이 파일, 그리고 `litdb/figures/chaney2024_…/`(크로핑 10장) 뿐이다.
>
> **§J 번호 = `J-37`.** 병합 시점(2026-09-22)에 `comparison_vs_ours.md` 를 직접 열어 확인한 마지막 번호가 **J-36 ([Wang22Res])** 였다 (J-33 morgan2021 · J-34 haruyama2014 · J-35 okuno2020 · J-36 wang2022). **병합자는 J-37 이 여전히 비어 있는지 다시 확인한다.**
>
> **표 칸 수·열 순서는 아래 블록마다 머리글을 실제로 읽고 맞췄다**:
> · `INDEX.md` = **3칸** `slug | 논문 | 축`
> · `📑 Reference key` = **4칸** `약칭 | 논문 (저자·년·저널) | digest/status | 유형`
> · `§E` = **4칸** `주장 | 출처 | 우리 | 일치`
> · `§H` = **3칸** `gap | 누가 필요로 함 | 보강책`
>
> 🔴 **이 편의 1순위 값어치는 `HZ-anode-b2o3-reaction-direction`(BLOCKED, 오늘 등록)의 *세 번째 독립 외부 확인* 이다** → ⑤ 블록.
> ⛔ **§A(이온전도)·§B(산화 4축)·§C(기계)·§D(전자구조) 에 넣지 않는다** — σ·D·Ea·C_ij·갭이 **한 개도 없다**. 들어갈 자리는 **§E · §H · §J-37** 셋뿐이다.
>
> 🎤 **talk 역링크 — 해당 없음.** `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `talks/lee2026_skku_mlip_materials_design.md` 하나이고 그 대기열에 이 논문이 **없다**(`chaney`·`two-step`·`mingo`·`golov` 전부 0건). 덱과 어긋나는 것도 없다.

---

## ① `INDEX.md` 에 추가할 행 (**3칸** — `| slug | 논문 | 축 |`)

> `## ✅ Digest 완료 (paper-level)` 절, **음극/계면 계열** 근처(=`wang2022_resistive_…` 바로 뒤)에 넣는 것이 자연스럽다.

| `papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md` **(본문 7 pp + SI 7 pp · ✅ 그림 9장 *전수* 실독 + 판독용 확대렌더 3장 · 표 1장은 의도적 텍스트 전사)** | **[외부·음극 SEI *성장 동역학*·★★★ 우리 음극 산물표 방향 판정의 외부 앵커 · ⛔물성 4축 아님(σ·D·Ea·갭·C_ij 전부 0건)]** **Gracie Chaney**, **Andrey Golov**, **Ambroise van Roekeghem**, **Javier Carrasco**, **Natalio Mingo\*** (**CEA LITEN** Grenoble + **CIC energiGUNE** Vitoria-Gasteiz + Ikerbasque), "**Two-Step Growth Mechanism of the Solid Electrolyte Interphase in Argyrodyte/Li-Metal Contacts**" (***ACS Appl. Mater. Interfaces* 16, 24624–24630 (2024)**, DOI `10.1021/acsami.4c02548` · 접수 2024-02-14 / 수락 2024-04-19 / 게재 2024-05-03 · refs 43 · `Fig. 1`–`4` + `Fig. S1`–`S5` + `Table S1` · CEA FOCUS batteries + ANR-22-PEBA-0002 · ⛔ **데이터·퍼텐셜 비공개**) — **`[Wang22Res]`(ref 33) 가 던진 숙제의 직접 응답**이다: 본문 축자 *"the authors call for subsequent investigations of the formation of those products and of the **full Li metal-SEI-LPSC interface, which is what we provide here**."*<br>**★★★ 핵심 셋**: ① **반응식이 축자로 `Li₆⁺P⁵⁺S₅²⁻Cl⁻ + 8Li⁰ → 5Li₂⁺S²⁻ + Li⁺Cl⁻ + Li₃⁺P³⁻`** — **Li 을 8개 *흡수*** 하고 **Li₂S 가 5몰 주생성물**이며 **원소 S 가 없다**. 단계적 P–S 절단 4단(`PS₄→PS₃→PS₂→PS→P`, 매 단계 2e⁻) = **f.u. 당 정확히 8 전자**, ✎*(우리 유도)* **S/Cl 비와 무관**(산화환원 중심이 P⁵⁺→P³⁻ 하나뿐). ② **two-step = ①비정질 먼저, ②결정화 나중**: Li 환원 → **비정질 과리튬화층**(α ∝ **log t**, Butler–Volmer Δη 제한 — *확산 제한이 아니다*) → 뒤늦게 **`5Li₂S·Li₃P·LiCl` 고용체**로 결정화(주장: √t @300·350 K / linear @400 K). **상분리 3상이 아니라 antifluorite 단일 고용체**라고 주장(✎*우리 검산*: `5Li₂S·Li₃P·LiCl` = **Li₁₄PS₅Cl** = 음이온 7 · Li 14 = **정확히 Li₂X 화학량론**, 전하 ±14 **중성** ⇒ **Li₂(S₅ₐ₇P₁ₐ₇Cl₁ₐ₇)**; SI 표기 `Li₂(SPCl)`. **총 화학량론은 3상 혼합과 동일 — 다른 것은 미세구조뿐**). ⚠ **이 고용체 주장은 이 편의 결과가 아니다** — 본문이 *"As **previously shown using AIMD**, our results **also** find …"* 라 적는다 ⇒ **원전은 ref 34 Golov & Carrasco 2023**. ③ **4단계 시간표**(400 K·1 bar·model II): **~5 ps** 얇은 비정질 → **5 ps~** 첫 결정핵 → **165 ps 전환율 71 %**(비정질 최대, 도메인 합체 시작) → **1 ns** 전부 환원. **figure-read**: 비정질 최대 **≈58 % @ ≈200–250 ps**, 10 ns 결정화도 **≈76 %(400 K)·≈70 %(300 K)**, **비정질 입계가 22–29 % 영구 잔존**(*"cannot expect 100 % crystallinity … defects and grain boundaries"*).<br>**방법**: **MTP (MLIP-2, level 8, R_cut 5.0 Å)** 단일 퍼텐셜 · 학습셋 **2,732 → 2,781 배열**(ref 21 AIMD 기반 + D-optimality 능동학습, 외삽등급 5.5→2.5 / 하한 1.5) · **10-fold CV RMS 에너지 18.36(train)/20.89(test) meV/atom**, **힘 오차 미보고** · **NPT + Nosé–Hoover thermostat&barostat** · **10 ns** · **dt 1 fs**(400 K/1 bar/seed 2 만 **0.5 fs**) · **300/350/400 K × 1 bar/1 kbar × 시드 2** = ✎**24 런** · **Li(110)/LPSC(110) 샌드위치**(계면 2면, 진공 없음) · **model I 7,956 원자(288 f.u. + 4,212 Li, 1,345 Å²) / model II 31,824 원자(1,152 f.u. + 16,848 Li, 5,380 Å²)** · 관측량 **α = (8N(P)+6N(PS)+4N(PS₂)+2N(PS₃))/8Z**, **P–S 배위 컷오프 3 Å**.<br>⛔ **없는 것 전수**: **두께(nm) 0회**(`"thick"` 3회는 전부 *남의 연속체 모형 서술*·*선 굵기*) · **σ/D/Ea/MSD 0** · **밴드갭·DOS 0** · **전자전도도 0** · **임피던스·면저항 0** · **NEB/Bader/COHP/ELF/phonon/탄성/BVSE/ESW 0** · **RDF·구조인자·XRD·퍼콜레이션 정량·클러스터 분석 0** · **도핑/조성축 0**(`Li₆PS₅Cl` 단일 조성, `dopant`·`doping` 0회) · **무질서 처리 0줄**(S/Cl 4a/4c 배열 수·선택기준 미기재) · **DFT 코드·범함수·ecut·k-점 0줄**(`VASP` 0 · `PBE` 0) · **MD 엔진 0줄**(`LAMMPS` 0) · **결정성 판정 알고리즘 0줄**(ref 34 참조만) · **전압·전류 0**(*"unbiased electrolyte/electrode contacts"*).<br>**✎ digest 재계산 5건(논문 미보고)**: (i) **두 모델은 두께가 같고 옆면만 2×2 다** — 면적비 4.00 = f.u.비 4.00 ⇒ **LPSC 슬랩 ≈5.1–5.4 nm(양 모델 동일)**, Li 금속 한쪽당 ≈3.2–3.4 nm (ii) **완전환원에 필요한 Li = Li 금속의 54.7 %** ⇒ 음극 여유가 1.8배뿐 (iii) **고용체 화학량론 검산** = Li₂X 정확 일치·전하중성 ✓ (iv) **부피 변화 +36 %**(전해질 대비) / **−19 %**(전해질+소모 Li 대비 = **순수축** ⇒ 실셀이면 인장·공극 방향인데 **NPT 라 원천 배제**) (v) **`Fig. 4` 유효지수 n ≈ 0.83/0.79/0.87**(300/350/400 K) — **주장된 0.5↔1.0 이분법이 데이터에 없다**.<br>🔴 **우리가 잡은 비판 12건 중 상위 5**: ① **MLIP 정확도가 결론 수준에 못 미친다** — 18.4/20.9 meV/atom 은 같은 MTP 를 쓴 `[Wang22Res]`(0.32–0.87)의 **21–65배**, fold 간 시험오차 **13.2↔33.3(2.5배)**, **힘 오차 없음**. 핵심 관측량이 **결정 vs 비정질 상대안정성**인데 그 차가 같은 자릿수일 수 있다 ② 🔴🔴 **"자기제한" 미증명** — `self-limiting` 0회이고 저자 용어는 *negative-feedback·stalls·clogging·percolation threshold*. 결론 근거인 **model II 6런은 전부 100 % 환원**(SI 축자 *"all our simulations for model II displayed **complete reduction**"*), 정지는 **7,956 원자 계·1 kbar·한쪽 시드**에서만. 논문이 인용한 400 K/1 kbar 사례는 **≈73–74 %에서 ≈200 ps–1 ns 일시 정지 후 ≈96 % 회복**이고, **끝까지 멈춘 유일한 런(300 K/1 kbar/seed 1, ≈73 % 에서 2 ns~10 ns 완전 평탄)은 논문이 언급조차 안 한다**(우리가 `Fig. S1` 확대렌더로 찾았다 · 같은 패널 seed 2 는 ≈98 % = **시드 간 25 %p**). 게다가 **전해질이 ≈5 nm 뿐**이라 *"막혀서 끝났나 다 먹어서 끝났나"* 를 **설계상 가를 수 없다** ③ **시간법칙 주장에 적합선·R²·잔차·반대축 검정이 전부 없고** 온도마다 **창이 다르다**(400 K 0–420 ps vs 300/350 K 0–702 ps). *"Above 400 K"* 는 **400 K 가 최고온인데** 쓴 표현 ④ **능동학습이 +53 배열(+1.9 %)뿐인데 `Fig. S3` y축을 2720–2790 로 잘라 포화 곡선처럼 보인다** ⑤ **결정성 판정이 재현 불가**(알고리즘·컷오프·문턱 0줄, 민감도 0) — 논문의 **모든 곡선**이 그 분류 위에 있다. (나머지: NPT 가 공극·응력 배제 / 실험 시간척도와의 다리 없음(✎ figure-read 성장률 **≈2.4 nm/ns @400 K**) / `Fig. S2` 열 머리글이 캡션과 모순 / "model II 에서 시드 의존 사라짐" 은 **면적 4배의 중심극한**과 구별 안 됨 · 시드 2개 / 무질서·격자·완화·DFT 설정 전무 / 고용체 주장이 ref 34 귀속).<br>**🔴 우리에게 불리한 것 4건**: (가) **0 V 반응식 방향 오류가 외부 3건째로 확인**(§⑤) (나) **`min_product_gap_eV`/`leaky_products` 가 "상분리 가정" 위에 있었다** — 이 편이 맞으면 **순수 Li₃P 상이 형성되지 않으므로 0.70 eV 가 무엇의 갭인지 불명**이고, 고용체 `Li₂(S,P,Cl)` 의 갭은 **어느 문헌에도 없다** (다) **"SEI = 결정성 부동태층" 이 과하다** — 실온 10 ns 에 **비정질 입계 ≈29 % 잔존**, 누설 경로는 결정 갭이 아니라 **입계**일 수 있고 우리는 그 축 값이 0건 (라) **우리는 반응하는 계면을 돌려 본 적이 0회**(우리 MD 는 벌크·조성고정·200 ps). **🔎 확보 후보 1순위 = ref 34 Golov & Carrasco *ACS Energy Lett.* 2023, 8, 4129**(고용체·결정성 판정법의 **진짜 원전** + **유일한 조성축 Se 치환**), 2순위 **ref 21 동 저자 *ACS AMI* 2021, 13, 43734**(계면 제작법·학습셋·DFT 설정 + **coated anode**). ⚠ **ref 11 Wenzel 2018 *Solid State Ionics* 318, 102** — `[Wang22Res]` digest 가 인용한 **Wenzel 2016** 과 **다른 논문일 수 있다**, 병합자 확인 요청. | **음극(Li 금속) SEI *성장 동역학* — 시간축 전용. 값은 α(t)·결정성(t) 두 곡선뿐** |

---

## ② `comparison_vs_ours.md` **§📑 Reference key** 행 (**4칸** — `| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |`)

| **[Chaney24SEI]** ★★★ **아르지로다이트‖Li 금속 SEI 의 *시간축* 원전 (우리 litdb 최초)** · 🔴 **우리 0 V 반응식 방향 오류의 3번째 독립 외부 확인** · ⛔⛔ **σ·D·Ea·갭·두께 0건 → A–D 물성 4축 진입 금지** | **Gracie Chaney**/**Andrey Golov**/**Ambroise van Roekeghem**/**Javier Carrasco**/**Natalio Mingo\*** (CEA LITEN Grenoble + CIC energiGUNE + Ikerbasque) 2024 ***ACS Appl. Mater. Interfaces* 16, 24624–24630** (DOI 10.1021/acsami.4c02548 · refs 43 · SI 7 pp `Fig. S1`–`S5`+`Table S1` · ⛔ 데이터·퍼텐셜 비공개) — "**Two-Step Growth Mechanism of the Solid Electrolyte Interphase in Argyrodyte/Li-Metal Contacts**". **MTP(MLIP-2 · level 8 · R_cut 5 Å) · NPT Nosé–Hoover · 10 ns · dt 1 fs · 300/350/400 K × 1 bar/1 kbar × 시드 2 · Li(110)/LPSC(110) 샌드위치 7,956 / 31,824 원자**. 🔑 **반응식 축자 `Li₆PS₅Cl + 8Li → 5Li₂S + LiCl + Li₃P`**(Li **흡수**, Li₂S 주생성물, 원소 S 없음) · **two-step = 비정질 먼저(log t) → 고용체 결정화 나중(√t/linear 주장)** · **산물은 상분리 3상이 아니라 antifluorite `Li₂(S₅ₐ₇P₁ₐ₇Cl₁ₐ₇)` 고용체**(⚠ 원전은 ref 34) · **비정질 입계 22–29 % 영구 잔존**. ⛔ **두께(nm) 0 · σ/D/Ea 0 · 갭/DOS 0 · 전자전도 0 · 도핑/조성축 0 · 무질서 처리 0줄 · DFT 코드·범함수 0줄 · `self-limiting` 0회** | ✅ `papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md` — 판정은 **§E 2행** + **§H 1행** + **§J-37**(기전·시간축 원전) | 계산 전용 (MLIP-MD. 실험 0회 · AIMD 0회(ref 21 에서 학습셋만 상속) · 후처리는 α·결정성 두 가지뿐) |

---

## ③ `comparison_vs_ours.md` **§E. 환원 / 음극(Li 금속) 계면** 에 추가할 행 (**2행** · 4칸 `주장 | 출처 | 우리 | 일치`)

| 주장 | 출처 | 우리 | 일치 |
|---|---|---|---|
| **⭐⭐⭐ 🆕 Li 금속 접촉 분해는 *Li 을 f.u. 당 정확히 8개 흡수* 하고 Li₂S 가 주생성물이다 — 방향과 산물이 동역학으로 직접 관측됐다** (2026-09-22 신설) — 본문 Appendix 축자 **`Li₆⁺P⁵⁺S₅²⁻Cl⁻ + 8Li⁰ → 5Li₂⁺S²⁻ + Li⁺Cl⁻ + Li₃⁺P³⁻`**. 근거는 **단계적 P–S 절단 4단**(`(PS₄)³⁻+2e⁻→(PS₃)³⁻+S²⁻` … `(PS)³⁻+2e⁻→P³⁻+S²⁻`), P 산화수 **+5→+3→+1→−1→−3**. ✎ *우리 유도*: 산화환원 중심이 **P⁵⁺→P³⁻ 하나뿐**이므로(S 는 이미 S²⁻, Cl 은 Cl⁻) **8 Li/f.u. 은 S/Cl 비와 무관** | **[Chaney24SEI]** Appendix *Tracking the Total Amount of Reduction* (MTP-MD 31,824 원자·10 ns·NPT·300–400 K. 관측량 α = (8N(P)+6N(PS)+4N(PS₂)+2N(PS₃))/8Z, **P–S 컷오프 3 Å**) | `anode_interface_b2o3.json` 0 V 행이 **Li 을 방출**하는 식이고(`… + 0.8 Li` / `… + 10 Li`) **Li₂S 가 없으며 원소 S 가 4.4 / 41 몰** 서 있다 → `HZ-anode-b2o3-reaction-direction` **BLOCKED**(2026-09-22 등록) | 🔴🔴 **우리가 틀렸다 — 외부 3건째 독립 확인.** `[Wenzel18]`(XPS·실험) · `[Wang22Res]`(Eq.8·열역학) 에 이어 **이번엔 동역학**이다(Li 이 실제로 들어가는 것을 10 ns 동안 센다). ⇒ **방향 오류를 "혹시 맞을 수도" 로 읽을 여지가 없다.** ✎ **고친 식의 *모양* 템플릿**(값 아님, 체로만 쓴다): `Li₅.₄PS₄.₄Cl₁.₆ + **8Li** → 4.4Li₂S + Li₃P + 1.6LiCl` · `Li₅₈B₂P₈S₄₁Cl₁₆O₃ + **72Li** → 41Li₂S + 8Li₃P + 16LiCl + 3Li₂O + 2LiB`(72 = 8×8 + 8). **거르는 규칙 한 줄: 0 V 식에서 Li 계수가 음수이거나 생성물에 원소 S 가 있으면 그 식은 틀렸다** |
| **⭐⭐ 🆕 SEI 는 "상분리된 Li₂S/Li₃P/LiCl 결정" 이 아니라 *antifluorite 고용체* 이고, 그나마 22–29 % 는 비정질 입계로 남는다** (2026-09-22 신설) — *"the crystalline products are **not a phase-separated mixture** … but a `5Li₂S·Li₃P·LiCl` **solid solution**, which corresponds to the **antifluorite structure type**"* (SI 표기 `Li₂(SPCl)`). ✎ *우리 검산*: = **Li₁₄PS₅Cl**, 음이온 7 · Li 14 ⇒ **정확히 Li₂X**, 전하 +14/−14 **중성** ⇒ **Li₂(S₅ₐ₇P₁ₐ₇Cl₁ₐ₇)**. **총 화학량론은 3상 혼합과 완전히 동일 — 다른 것은 미세구조뿐.** **figure-read 결정화도(10 ns)**: 400 K **≈76 %** · 350 K ≈75–80 % · 300 K **≈70 %**, 나머지는 **비정질 입계**(*"cannot expect 100 % crystallinity … defects and grain boundaries"*). XPS 방어: *"faces difficulties in distinguishing between **phase-separated domains or a singular solid solution**"* + Wenzel 의 *"unknown reduced P species"* ⚠ **양립 가능성 논증이지 고용체의 실험 증거가 아니다** · ⚠ **주장의 원전은 ref 34 Golov & Carrasco 2023**(본문 *"As previously shown using AIMD"*) | **[Chaney24SEI]** `Fig. 2`·`Fig. 3`·`Fig. S5` + 본문 p.2 (결정성 판정은 **ref 34 방법 — 알고리즘·컷오프·문턱이 이 편에 0줄**) | `sei_products.json` 역할 문턱(insulator ≥4 / marginal 2–4 / conductor <2 eV)과 `anode_interface_b2o3.json` 의 `min_product_gap_eV`·`leaky_products` — **둘 다 순수 이원화합물 갭**(Li₃P 0.70 · Li₂S 3.90 · LiCl 6.65 eV) | 🔴 **반박이 아니라 *라벨링 요구* 다.** 우리 판정축이 **"상분리 가정" 위에 서 있었다는 것이 드러났고, 우리는 그 전제를 한 번도 명시하지 않았다**(`method` 문자열·`_role_threshold` 어디에도 없다). ⇒ **앞으로 "상분리 가정 하" 라고 적는다.** 🟢 **동시에 우리 것이 하나 열린다**: **`Li₁₄PS₅Cl` antifluorite 고용체의 밴드갭은 이 편도, `[Wang22Res]` 도, 우리도 계산한 적이 없다 = 문헌 공백**. 우리는 이미 Li₂S·Li₃P·LiCl 계열 셀을 다뤄 봤으므로 **SQS + fixed-occ nscf(우리 표준)** 로 낼 수 있다 ⚠ **배열이 여럿이라 집계 규칙을 먼저 선언**해야 스칼라 갭이 정의된다 → **보고량 카드 먼저** |

---

## ④ `comparison_vs_ours.md` **§H. 우리가 아직 못 하는 것 (정직 목록)** 에 추가할 행 (**1행** · 3칸 `gap | 누가 필요로 함 | 보강책`)

| gap | 누가 필요로 함 | 보강책 |
|---|---|---|
| **🔴🔴 ⭐⭐ 우리 음극 서사에 *시간축* 이 없다 — 그리고 "SEI = 결정성 부동태층" 이라는 우리 그림이 문헌 기준으로 과하다** (2026-09-22 신설) | **[Chaney24SEI]** 가 눈금을 준다: SEI 는 **비정질로 먼저 생기고**(α ∝ log t, Butler–Volmer Δη 제한) **결정화는 별개의 느린 2단계**이며, 실온 10 ns 에도 **결정화도 ≈70 %·비정질 입계 ≈29 % 잔존**. 우리 음극 자산은 `anode_interface_b2o3.json`(grand-potential 산물표) **한 장뿐**이고 그것은 **④단계 이후의 평형 세계만** 말한다 — **초기 수백 ps 의 과리튬화 비정질상은 상도 전자구조도 아무도 계산 안 했다** | ① **표기부터**: 우리 갭 판정에 **"상분리 가정 하"** 라벨을 붙인다(무료·즉시) ② **문헌 공백을 우리가 딴다**: `Li₁₄PS₅Cl` antifluorite 고용체를 **SQS + fixed-occ nscf** 로 — ⚠ **보고량 카드(`kb/templates/estimand_card.md`) 먼저**, 배열 앙상블 집계 규칙을 결과 보기 전에 선언 ③ **계면 MD 능력 자체가 0 이다** — 우리 MLIP-MD 는 **벌크·조성고정·200 ps** 라 반응하는 계면을 돌린 적이 없다. 시작한다면 **앙상블을 NPT 로** 잡는다(✎ 반응 순부피 **−19 %**, NVT 면 그 수축이 응력으로 갇힌다) ④ ⛔ **이 편에서 두께·σ·Ea 를 가져올 수 없다 — 0건이다.** 두께 축의 눈금은 여전히 **우리도 문헌도 없다**(`[Wang22Res]` 0회 · `[Chaney24SEI]` 0회) |

---

## ⑤ 🔴🔴 **`HZ-anode-b2o3-reaction-direction` (BLOCKED) 에 대한 *세 번째 독립 외부 확인* — 원장 정정 *제안 문구* (내가 고치지 않았다)**

**무엇이 "세 번째 독립 확인" 인가 — 세 출처가 서로 다른 방법이라는 것이 핵심이다.**

| # | 출처 | 방법 | 방향 | Li₂S | 원소 S |
|---|---|---|---|---|---|
| 1 | **Wenzel 2018** (*Solid State Ionics* 318, 102 — 이 편 ref 11, 양 논문이 같이 인용) | **실험 XPS** | 흡수 | ✅ | ❌ |
| 2 | **`[Wang22Res]` Eq.8** (`litdb/papers/wang2022_resistive_…`) | **열역학**(문헌 소환 분해식) | 흡수 | ✅ | ❌ |
| 3 | 🆕 **`[Chaney24SEI]`** (이 편, Appendix 축자) | **동역학 — MLIP-MD 로 Li 이 실제로 들어가는 것을 10 ns 동안 센다** | **흡수 (+8)** | ✅ **5몰, 주생성물** | ❌ |
| — | **우리 `anode_interface_b2o3.json` 0 V** | MP grand-potential | 🔴 **방출 (−0.8 / −10)** | 🔴 **없다** | 🔴 **4.4 / 41 몰** |

⇒ **세 방법(실험·열역학·동역학)이 전부 같은 답을 주고 우리만 반대다.** 특히 3번은 *"평형이 그렇다"* 가 아니라 *"Li 원자가 전해질 쪽으로 들어가는 것을 세어서 8개였다"* 이므로 **방향에 대한 가장 직접적인 증거**다.

### ⑤-a. `db/properties/citation_hazards.json` — `HZ-anode-b2o3-reaction-direction` 의 `why` 에 **덧붙일 한 문장 (제안)**

> *"2026-09-22 추가 확인: `[Chaney24SEI]`(`litdb/papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md`)가 **동역학으로** 같은 방향을 준다 — MLIP-MD(31,824 원자·10 ns) Appendix 축자 `Li₆⁺P⁵⁺S₅²⁻Cl⁻ + 8Li⁰ → 5Li₂⁺S²⁻ + Li⁺Cl⁻ + Li₃⁺P³⁻`. 단계적 P–S 절단 4단(매 단계 2e⁻)으로 **f.u. 당 정확히 8 전자**이고, 산화환원 중심이 P⁵⁺→P³⁻ 하나뿐이라 **8 Li/f.u. 은 S/Cl 비와 무관**하다. ⇒ 실험(XPS·Wenzel) · 열역학(Wang/Canepa Eq.8) · **동역학(Chaney)** 세 방법이 일치한다."*

### ⑤-b. 같은 항목의 `fix` 에 **덧붙일 한 문장 (제안)** — 🔴 **이게 새로 생긴 것이다**

> *"⚠ 산물 **갭 판정**(`min_product_gap_eV`·`leaky_products`)은 **상분리 가정** 위에 서 있다. `[Chaney24SEI]` 는 아르지로다이트‖Li 금속 SEI 가 **antifluorite `Li₂(S,P,Cl)` 고용체**(= `Li₁₄PS₅Cl`, 음이온 7·Li 14 로 정확히 Li₂X)이고 **순수 Li₃P 상이 따로 형성되지 않는다**고 본다. 그 고용체의 밴드갭은 **어느 문헌에도 없다**. ⇒ `min_product_gap_eV = 0.70`(Li₃P) 은 **'상분리 가정 하의 값'** 이라고 라벨하고, 그 라벨 없이 '누설 산물' 이라고 단정하지 않는다. 추가로 `[Chaney24SEI]` 기준 **결정화도가 300 K 10 ns 에 ≈70 %** 이고 **비정질 입계가 ≈29 % 잔존**하므로, 갭 기반 누설 판정은 **결정립만** 다루고 **입계 경로는 다루지 않는다**."*

### ⑤-c. `tools/oxidation/anode_interface_stability.py` 재실행 뒤 **30초 검산용 체 (제안)**

기존 ⏭ 할 일(`evolution` 기록 + 방향 선언 + 재실행 → RESOLVED)은 그대로 두고, **합격 판정에 아래 두 줄을 게이트로 건다**:

```
0 V 행 합격 조건 (둘 다 만족해야 한다)
  ① 반응식의 Li 계수가 **양수(흡수)** 여야 한다.                ← 방향
  ② 생성물에 **원소 S 가 없어야** 하고 **Li₂S 가 있어야** 한다.  ← 산물 집합
  (참고 화학량론: P 하나당 8 Li. `Li₅.₄PS₄.₄Cl₁.₆` → 8 Li/f.u. · `Li₅₈B₂P₈S₄₁Cl₁₆O₃` → 72 Li)
```

⚠ **위 반응식 템플릿은 "정답" 이 아니다** — MP 의 실제 grand-potential 평형은 다른 상(`Li₃BO₃`·`B₆P` 등)을 고를 수 있다. **모양 점검용 체**로만 쓰고, 값은 도구 재실행 결과로 대체한다.
⛔ `pending_forbidden_phrases`(`"4.4 S + 0.8 Li"` · `"41 S + 10 Li"`)는 **그대로 둔다** — 이 pending 문서와 digest 도 그 문자열을 **교육 문장으로** 담고 있어, 지금 `forbidden_phrases` 로 승격하면 교차행 누출로 무관용 결속 시험이 깨진다(기존 `binding_scope_why` 판단과 동일).

### ⑤-d. `db/literature/refs.json` **추가 제안** (직접 고치지 않았다)

```json
{
  "id": "chaney2024",
  "authors": "Chaney, G.; Golov, A.; van Roekeghem, A.; Carrasco, J.; Mingo, N.",
  "title": "Two-Step Growth Mechanism of the Solid Electrolyte Interphase in Argyrodyte/Li-Metal Contacts",
  "journal": "ACS Appl. Mater. Interfaces",
  "volume": 16,
  "pages": "24624-24630",
  "year": 2024,
  "DOI": "10.1021/acsami.4c02548",
  "title_verified": "2026-09-22 (PDF 직독)",
  "key_content": "MTP(MLIP-2) MD, 31,824 atoms, 10 ns, NPT, 300-400 K, Li(110)/Li6PS5Cl(110) sandwich. Two-step SEI: Li-argyrodite redox -> amorphous over-lithiated layer (alpha ~ log t, Butler-Volmer chemical-potential limited), then slower crystallization into a 5Li2S*Li3P*LiCl antifluorite SOLID SOLUTION (not phase-separated). Reaction (verbatim): Li6PS5Cl + 8 Li -> 5 Li2S + LiCl + Li3P; stepwise P-S cleavage, 8 electrons per f.u. Crystallinity saturates at ~70-76% (amorphous grain boundaries persist). NO thickness(nm), NO sigma/D/Ea, NO band gap, NO electronic conductivity, NO composition axis.",
  "tags": ["argyrodite", "Li-metal anode", "SEI", "MLIP", "MTP", "MD", "interface", "solid solution", "antifluorite"]
}
```
⚠ **`title` 의 `Argyrodyte` 오타는 원문 그대로다** (ACS 게재본 제목이 그렇다). 고치지 말 것.
⚠ **ref 11 확인 요청**: 이 편은 Wenzel 을 ***Solid State Ionics* 318, 102–112 (2018)** 로 인용하는데, `[Wang22Res]` digest 는 **Wenzel 2016** 을 인용한다. **두 편이 다른 논문일 수 있다** — `refs.json` 에 Wenzel 이 이미 있으면 **연도·저널을 대조**한다.

---

## ⑥ `comparison_vs_ours.md` **§J-37** 블록 (신설 제안)

### J-37. 🔧 **기전·시간축 원전 — [Chaney24SEI] 가 음극 SEI 에 *시간* 을 넣는 방식, 그리고 그것이 우리 판정축에 요구하는 것** (2026-09-22 신설 제안)

📎 **출처: `papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md`**

**J-37-a. 우리가 이 논문에서 *못* 가져오는 것 (먼저 못박는다)**

| 양 | 이 논문 | 결론 |
|---|---|---|
| SEI **두께 (nm)** | ❌ **0회** — 성장곡선 y축은 **환원율 %** 다 | ⛔ 존재하지 않는 값 |
| **σ · D · Ea · MSD** | ❌ 이 계에서 **한 번도 안 잼**. *"poor ionic conductors"* 는 **ref 33 소환** | ⛔ 인용 금지 |
| **밴드갭 · DOS · 전자전도도 · 터널링** | ❌ — **MTP 는 고전 퍼텐셜이라 전자가 없다** | ⛔ 전자 누설 축에 **아무것도 못 준다** |
| **자기제한 두께** | ❌ 미증명(J-37-c) | ⛔ *"자기제한적임을 보였다"* 금지 |
| **시간법칙 지수 0.5 / 1.0** | ⚠ 주장만, 검정 없음 | ⛔ 인용 금지(J-37-d) |
| **조성축**(Cl·O·B 도핑) | ❌ **0건**, `Li₆PS₅Cl` 단일 | ⛔ Cl-rich 유불리에 **중립** |

**J-37-b. MD 규약 한 줄 대조** (판정 아님 — 나란히만)

| 항목 | [Chaney24SEI] | 우리 (modelc/lpsocl) |
|---|---|---|
| MLIP | **MTP 자체학습, level 8, R_cut 5 Å** | **UMA-s-1p1(omat) 범용 사전학습** |
| 학습 정확도 | **18.4 / 20.9 meV/atom** (RMS E) · **힘 미보고** | 외부 벤치마크 |
| 앙상블 | **NPT** + Nosé–Hoover (thermo+baro) | **Langevin NVT**, friction 0.02 |
| dt | **1 fs**(일부 0.5) | **2 fs** |
| 온도 | **300 / 350 / 400 K** | **600 / 800 / 1000 K** |
| 시간 | **10 ns** | prod **200 ps** |
| 원자수 | **7,956 / 31,824** | box331 **558** |
| 계면 | ✅ 샌드위치 2면 | ❌ 벌크 주기셀 |
| 반응 | ✅ 결합 절단 허용 | ❌ 조성 고정 |
| 무질서 | 🔴 **0줄** | ⭐ 배열 앙상블 규율 있음 |
| 오차막대 | 🔴 **없음**(시드 2) | ⭐ 멀티시드 규율 |
| 보고량 | **α(t) · 결정성(t)** | **MSD → D → σ(NE, Haven=1)** |

🔴 **겹치는 온도가 하나도 없다**(300–400 vs 600–1000 K) ⇒ **어떤 동역학 수치도 나란히 놓을 수 없다.**

**J-37-c. 🔴🔴 "자기제한" 을 어디까지 말할 수 있나 — 전수 조사**

논문 텍스트에 **`self-limiting` 0회**. 저자 용어는 *negative-feedback · stalls · clogging · percolation threshold*.

| 계 | 조건 | 정지? | figure-read |
|---|---|---|---|
| **model II** (31,824) | 3 T × 2열 = **6런** | ❌ **0건** | SI 축자 *"all our simulations for model II displayed **complete reduction**"* |
| model I (7,956) | 400 K / 1 kbar / seed 1 | ⚠ **일시** | ≈73–74 % 에서 **≈200 ps→1 ns 평탄**, 그 뒤 **≈96 % 회복** |
| model I | **300 K / 1 kbar / seed 1** | 🔴 **완전 — 논문 미언급** | **≈73 % 에서 2 ns~10 ns 완전 평탄**. 같은 패널 seed 2 는 **≈98 %**(시드 간 **25 %p**) |
| model I | 300 K / 1 bar | ❌ (느릴 뿐) | 10 ns 에 ≈85 / ≈91 %, 아직 상승 중 |

✎ **결정적 설계 한계**: 두 모델은 **두께가 같고 옆면만 2×2 다**(면적비 4.00 = f.u.비 4.00) ⇒ **LPSC 슬랩이 ≈5.1–5.4 nm 뿐**이고 **양쪽에서 먹으므로 한 계면이 최대로 먹을 수 있는 두께가 ≈2.6 nm** 다. ⇒ *"막혀서 끝났나, 다 먹어서 끝났나"* 를 **설계상 가를 수 없다.**
👉 **허용 서술**: *"결정층이 비정질 통로를 끊어 Li 유입을 막는 음의 되먹임을 제안하고, 작은 계의 일부 런에서 정지를 관측했다."* ⛔ **금지**: *"아르지로다이트 SEI 가 자기제한적임을 보였다."*

**J-37-d. 🔴 시간법칙 주장 — ✎ 우리 재독이 부정한다**

논문 주장: 300·350 K = **√t**(확산 제한) / *"Above 400 K"* = **linear**(계면 제한). ⚠ **400 K 가 최고온이다.**
`Fig. 4` 에 **적합선·R²·잔차·반대축 검정 0**, **온도마다 창이 다르다**(400 K 0–420 ps vs 300/350 K 0–702 ps).

✎ **2점 멱법칙 재독 (figure-read, 논문 미보고)**

| 패널 | 두 점 | **유효 지수 n** | 주장 |
|---|---|---|---|
| 300 K | (100 ps, 4 %) → (702 ps, 20 %) | **0.83** | 0.5 |
| 350 K | (100 ps, 7 %) → (702 ps, 32.5 %) | **0.79** | 0.5 |
| 400 K | (100 ps, 12 %) → (420 ps, 42 %) | **0.87** | 1.0 |
| 400 K 전반/후반 | | **0.70 → 1.03**(단일 지수 아님) | 1.0 |

🔴 **셋 다 n ≈ 0.8 로 뭉친다.** n = 0.5 라면 300 K 곡선이 100→702 ps 에서 **√7.02 = 2.65배**만 올라야 하는데 **실제 5.0배**(4 → 20 %) 오른다. ⇒ **0.5↔1.0 이분법이 데이터에 없다.** (내 y 읽기 오차 ±1–2 %p 로는 뒤집히지 않는다 — 그러려면 종점이 ≈10.6 % 여야 하는데 곡선은 분명히 ≈20 % 에서 끝난다.)
⛔ **인용 금지**: *"확산 제한 → 계면 제한 전이가 입증됐다."*

**J-37-e. ⭐⭐ 우리 판정축에 대한 요구 — "어떤 상이 생기나" 에서 "그 상들이 어떻게 배열되나" 로**

1. **`min_product_gap_eV`·`leaky_products` 에 "상분리 가정 하" 라벨을 단다** (⑤-b).
2. **누설 경로 후보가 하나 늘었다 — 비정질 입계(22–29 %).** 우리 `sei_products.json` 은 이미 `Li₃PO₄` 를 *"cuts GB electron percolation"* 으로 쓰고 있다 ⇒ **같은 언어인데 우리 쪽엔 값이 0건**이다.
3. **NPT 를 쓸 이유가 생겼다** — ✎ 반응 순부피 **−19 %**(전해질+소모 Li 대비; +36 % 는 전해질만 대비). NVT 면 그 수축이 **응력으로 갇혀** 공극·박리를 못 본다. ⚠ 부피값은 **`[Wang22Res]` `Table S1` PBE 격자**에서 왔다 — **자릿수 감각용, 수치 인용 금지**.
4. 🟢 **문헌 공백 하나를 우리가 딸 수 있다** — `Li₁₄PS₅Cl` antifluorite 고용체의 밴드갭. **SQS + fixed-occ nscf**(우리 표준). ⚠ **보고량 카드 먼저**(배열 앙상블 집계 규칙을 결과 보기 전에 선언).

**J-37-f. ⭐ 우리 MD 규율을 *지지* 하는 외부 사례 2건**

- **단일 시드 금지**: model I 300 K/1 kbar 에서 **시드 하나는 73 %, 다른 하나는 98 %**(25 %p). 우리 *"단일시드 1.33× 철회"* 규율과 같은 종류의 함정이고, **이 논문은 시드 2개로 결론을 낸다**.
- **"model II 에서 시드 의존이 사라진다" 는 해석이 과하다**: model II 는 model I 의 **옆면 2×2 복제**라 **면적 4배의 중심극한만으로 산포가 ≈2배 준다**. 퍼콜레이션 임계의 크기 의존과 **구별할 시험이 없다**.

**J-37-g. ⛔ 이 논문을 인용할 때 반드시 같이 다는 단서 4개**

① **고용체 주장의 원전은 ref 34 (Golov & Carrasco 2023)** — 본문이 *"As previously shown using AIMD"* 라 적는다. 이 편으로 귀속하면 잘못된 인용이다.
② **MLIP 오차 18.4 / 20.9 meV/atom** — 같은 MTP 를 쓴 `[Wang22Res]`(0.32–0.87)의 **21–65배**, **힘 오차 미보고**. 결정 vs 비정질 상대안정성이 이 오차와 같은 자릿수일 수 있다.
③ **결정성 판정이 재현 불가** — 알고리즘·컷오프·문턱 **0줄**, 민감도 **0**. 논문의 **모든 곡선**이 그 분류 위에 있다.
④ **DFT 설정 전무** — 코드·범함수·ecut·k-점 **0줄**(`VASP` 0 · `PBE` 0 · `LAMMPS` 0). 이 편만 읽고는 아무것도 재현할 수 없다.

---

## ⑦ 병합자 체크리스트

- [ ] `comparison_vs_ours.md` 에서 **J-37 이 여전히 비어 있는지** 확인(병합 시점 마지막 = J-36). 찼으면 다음 번호로 밀고 **digest §17·이 파일의 J 번호도 같이 고친다**.
- [ ] **§J-37 블록에 `📎 출처: papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md` 줄이 들어갔는지** 확인(⑥ 머리에 있다) — 없으면 `build_index.py` 가 미편입으로 센다.
- [ ] `INDEX.md` 행은 **3칸**이다(`slug | 논문 | 축`). ① 블록은 이미 3칸으로 접어 뒀다(`<br>` 사용).
- [ ] §E 행 **4칸**(`주장 | 출처 | 우리 | 일치`) · §H 행 **3칸**(`gap | 누가 필요로 함 | 보강책`) — 열 **순서**까지 맞춰 뒀다.
- [ ] ⑤ 의 원장 정정 **제안**은 **사람이 판단한다** — 내가 `db/` 를 고치지 않았다.
- [ ] ⑤-d 의 `refs.json` 항목 추가 시 **`Argyrodyte` 오타는 원문 그대로 둔다**.
- [ ] ⚠ **Wenzel 연도 확인** — 이 편 ref 11 = **2018** *Solid State Ionics* 318, 102 vs `[Wang22Res]` digest 인용 = **2016**. 다른 논문일 수 있다.
- [ ] `python3 tools/litdb/build_index.py --check` 로 미편입 0 확인.
- [ ] 병합이 끝나면 **이 파일을 지운다.**
