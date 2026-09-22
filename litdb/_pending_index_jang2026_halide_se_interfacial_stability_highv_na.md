# ⏳ pending — `jang2026_halide_se_interfacial_stability_highv_na` 의 INDEX / comparison 반영분

> 2026-09-22, litdb-curator. **이번 세션은 `INDEX.md` · `comparison_vs_ours.md` · `db/` 직접 수정 금지 + 커밋 금지** 지시라
> 아래 블록만 만들어 둔다. **조율 세션이 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/jang2026_halide_se_interfacial_stability_highv_na.md`
> 그림: `litdb/figures/jang2026_halide_se_interfacial_stability_highv_na/` (**PNG 17장** = 본문 `Fig. 1`–`8` + SI `Fig. S1`–`S2` + `Table 1` + `Table S1`–`S7`)

## 📌 §J 번호 배정 — **J-40**

`comparison_vs_ours.md` 를 **직접 열어** 확인했다 (grep `^### J-3[6-9]|^### J-4[0-9]`):
- 실재하는 마지막 번호 = **J-38** (`[Schw21]`, line 5394). J-36 `[Wang22Res]` · J-37 `[Chaney24SEI]` 가 그 앞.
- **J-39 는 `_pending_index_sjolin2023_accelerated_workflow_antiperovskite_sse.md` 가 이미 잡았다** (그 파일 7행·37행·40행).
- **J-40 은 `comparison_vs_ours.md` 0 hit · 전 `_pending_index_*.md` 0 hit** ⇒ **이 논문은 `J-40` 으로 잡는다.**

⚠ **동시에 도는 에이전트가 있으면 넣기 직전에 한 번 더 본다.** 충돌 시 **번호만 바꾸면 된다** — 블록 안의 자기참조는 제목 1줄 + 상호참조 2줄뿐이다.

## ✅ 사전 점검 결과
- **🎤 talk 역링크 없음**: `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md` 하나뿐이고 그 대기열 6건에 이 논문 **없음**. `litdb/talks/` 전체에 `Jang`·`Na₂ZrCl₆`·`ASSSIB`·`halide solid electrolyte` 검색 **0건**. ⇒ **양방향 작업 없음.**
- **`litdb/properties/` 디렉터리가 없다** (`INDEX.md` 머리말이 명시) ⇒ properties 갱신 대상 없음.
- **`--clean` 금지 지시를 지켰다.** 기존 `figures/<폴더>/` 17장을 그대로 쓰고 **재추출하지 않았다.** `figures.json` 의 `sources` 가 **지정된 두 파일 정확히 그것**임을 확인했다 (다른 논문 혼입 0).
- 🔧 **도구 결함 아님 / 운영 이슈 1건**: **그림 폴더 slug 가 digest slug 와 다르다.** 폴더 = `jang2026_halide_se_interfacial_stability_highv_na`(파일명 기반), digest = `jang2026_halide_se_interfacial_stability_highv_na`(관례 `<firstauthor><year>_<topic>`). ⇒ **webapp 이 `figures/<slug>/` 로 찾으면 그림이 안 붙는다.** 아래 ④-4 에 rename 제안을 뒀다 (**직접 안 고쳤다**).
- **⛔ A–D 물성 4축 표 진입 없음**: 이 논문의 물성값은 **전부 Na 계**다(전압은 vs Na/Na⁺, 계면에너지는 Na 양극 상대). 우리 Li 축에 행을 만들면 **전부 `n/a`** 다. ⇒ 규율대로 **`🔧 방법 원전` 블록(§J-40)에만** 둔다.

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

> 표 머리 **직접 확인함**: line 25 `## ✅ Digest 완료 (paper-level)` / line 26 **`| slug | 논문 | 축 |`** / line 27 `|---|---|---|` ⇒ **정확히 3칸.** 아래 행도 3칸이고 길이는 `<br>` 로 접었다.

```markdown
| `papers/jang2026_halide_se_interfacial_stability_highv_na.md` **(본문 10 pp + SI 16 pp 통합)** | **[외부·Na 계·할라이드 SE·⛔⛔ 물성 4축 *수치* 진입 금지(이온종·기준전극·양극 전부 불일치) · 🔴🔴 `HZ-esw-reduction-limit-label` 의 *세 번째* 외부 눈금이자 **가장 강한** 것]** ✅ **Myeongcho Jang**/**Eunji Kwon**/**Chelin Jeon**/**Sooyeon Kim\***(명지대 화학)/**Seungho Yu\***(**KIST** 에너지저장연구센터) — "**Interfacial Stability and Design Strategies for Halide Solid Electrolytes in High-Voltage All-Solid-State Sodium-Ion Batteries**" (***Small Methods* 10(3), e02179 (2026)**, DOI `10.1002/smtd.202502179`; **CC BY-NC**; 접수 2025-11-01 / 수정 2025-12-26 / 수락 2026-01-04; KIST 2E33941·2E33943 + NRF RS-2024-00404414·RS-2024-00427700 + **KISTI KSC-2025-CRE-0062**; `Fig. 1`–`8` + `Table 1` + `Fig. S1`–`S2` + `Table S1`–`S7`; refs 38).<br>**⛔⛔ 자체 DFT 0건·자체 실험 0건** — `Methods` 축자 *"Crystal structures, formation energies, and convex-hull stabilities were **obtained from the Materials Project**"* + *"using **pre-computed** first-principles thermodynamic information"*. **범함수·ecut·k점·슈퍼셀·DFT+U·스핀·무질서 처리가 논문에 한 줄도 없는 것이 오기가 아니라 구조다.** 저자들이 직접 한 것 = **pymatgen 후처리 + scikit-learn PCA/K-means**.<br>**🔴🔴 ★ 이 digest 의 1호 산출물 — 우리 ESW 버그의 *구조적* 외부 눈금**: 본문 p.2 축자 *"**Within the electrochemical stability window, the decomposition energy remains zero** but increases upon reaching the reduction and oxidation potentials"* + `Table S3` 이 **전 분해 사다리를 ΔE_D 열과 함께** 인쇄 + `Fig. 2e–h`·`Fig. S1d–f` 의 y축이 **`Na uptake per f.u.`**(−1…+5, `← Sodiation` / `Desodiation →` 화살표) ⇒ **정의가 ① 에너지(ΔE_D=0) ② 교환량(uptake=0) 두 겹으로 중복 선언**돼 있고 **그림에서 두 평탄이 정확히 겹친다**(실독). **7/7 전수에서 0 평탄 바로 왼쪽 계단의 uptake 가 양수**(1 / 2.5 / 1.5 / 0.85 / 0.3 / 0.7 / 1.5) ⇒ **`red = max(V\|evolution>0)` 이 한 계단 아래를 준다는 직접 증거.** ✎ 어긋남 Δ = **0.11–1.10 V, 중앙 0.12 · 평균 0.31**(`Na₂ZrCl₆` 1.69↔1.57 = 0.12 / `NaTaCl₆` 2.17↔1.81 = 0.36 / **`NaAlCl₂.₅O₀.₇₅` 1.49↔0.39 = 1.10**) — **우리 cascade 중앙 +0.475 V 가 이 범위 안**이다 ⇒ *"버그 크기 = 그 계 환원 사다리의 마지막 계단 폭"*, **계마다 달라서 순위까지 흔든다**.<br>**⭐⭐⭐ 그리고 수정이 싸다**: `Table S2` 가 *"환원 전위"*=**가장자리 숫자**, *"환원 전위에서의 평형상"*=**아래 계단 산물**로 쓰는 이중 관례(7/7 일관)와 우리 json 이 **1:1** 이다 — 우리 **`ocv_V`(1.717 V) 가 저들 환원 전위**이고 우리 **`reduction_V`(1.242 V) 행의 반응식이 저들 "평형상" 칸**이다 ⇒ **재계산 없이 `window_V = ox − ocv` + 필드 rename 으로 끝난다**(전제: 교환-0 행이 2개 이상인 계가 cascade 에 있는지 먼저 센다).<br>**★ ESW 전수**(`Table S2`, **vs Na/Na⁺** — ⛔ 값 이식 금지): `Na₂ZrCl₆` **1.69/3.75** · `Na₀.₇La₀.₇Zr₀.₃Cl₄` 1.68/3.76 · `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` 1.69/3.77 · `NaTaCl₆` **2.18**(⚠`Table S3` 은 2.17)/3.76 · `NaAlCl₂.₅O₀.₇₅` **1.49**/3.76 · `NaTaOCl₄` 2.13/3.76 · `Na₀.₅ZrCl₄F₀.₅` 1.69/3.76. **산화 7종이 3.75–3.77 에 몰리는 이유를 저자가 활자로 준다 — *"oxidative decomposition consistently involves the formation of `NaCl₃`"*** ⇒ ⭐ **우리 comp1/modelc 가 둘 다 2.256 V 인 것(S²⁻-limited)과 *같은 구조*: 한 음이온이 산화 변을 독점한다.** 황화물 참조(본문): `Na₃SbS₄` **1.66** · `Na₃PS₄` **2.05** · `Na₁₁Sn₂PS₁₂` **1.91** (환원 한계는 `Fig. 1` **figure-read ≈** 1.63 / 1.25 / 1.2 뿐 — 본문 미보고; ⚠ **`Na₃SbS₄` 창이 figure-read ≈ 0.05 V** 인데 서술 없음).<br>**⭐⭐ ★ 2호 산출물 — 우리 §B 축 명명 규율의 *이온종 독립* 실증**: 본문 헤드라인 *"fluorination … increasing the potential from **3.92 to 4.18 V**"* 인데 **열역학 산화 onset 은 3.75 → 3.76 = +0.01 V** 다. ✎ 우리가 `Table S3` 로 재구성한 실체 = **onset 이후 ΔE_D 기울기가 −0.148 → −0.055 eV/V 로 2.7배 완만**해진 것. ⇒ ***"할로겐 치환은 축①(onset)을 안 건드리고 축②·③을 건드린다" 가 Li-황화물(comp1→modelc, Δonset 0.000 V)과 Na-할라이드에서 똑같이 성립한다.***<br>**★ 3호 — 동역학 연장창의 레시피를 ✎ 우리가 복원·검산했다**: 문턱 **`ΔE_D > −25 meV/atom`**(근거 문장 **0**), `Table S3` 인접 2행 **선형보간**으로 **7종 중 6종을 ±0.01 V 재현**(`Na₂ZrCl₆` 3.92 ✅정확 · `Na₀.₇La₀.₇Zr₀.₃Cl₄` 4.06 ✅ · `NaTaCl₆` 4.06 ✅ · `NaAlCl₂.₅O₀.₇₅` 4.15 ✅ · `Na₀.₆₂₅Y…` 4.13↔4.12 · `NaTaOCl₄` 4.02↔4.03 · ⚠`Na₀.₅ZrCl₄F₀.₅` 4.22↔4.18 ⇒ **`Table S3` 이 모든 breakpoint 를 싣지는 않는다**).<br>**★ 계면축(pseudo-binary)** — ✎ **저들 식 (2) ΔE_D,mutual 이 pymatgen `InterfacialReactivity(use_hull_energy=True)` 와 대수적으로 동일**함을 우리가 유도(= `E_eq(mix) − [x·E_hull(A)+(1−x)·E_hull(B)]`) ⇒ **보고량이 우리 `nd2o3_interface_reactivity` 와 같다**(⛔ 값은 여전히 이식 금지). `Fig. 3` **10 SE × 14 양극 = 140 셀 전수**(할라이드 98셀을 `Table S4` 와 **98/98 대조 일치** ⇒ 황화물 42셀 판독 신뢰): ✎ 계열평균 **Polyanionic −80.6 / P2 −141.7 / O3 −223.3**(할라이드 7종), 황화물 3종 **−72.5 / −226.0 / −254.0**.<br>**🔴🔴 임무⑥ 불리·반례 — 논문이 안 말하는 것**: ✎ **`Na₃PS₄` 를 빼면 황화물 평균이 P2 −188.7 / O3 −204.9 로 뛰고, O3 에서 `Na₃SbS₄`(−200.5)·`Na₁₁Sn₂PS₁₂`(−209.3) 가 할라이드 7종 범위(−194.5 … **−255.0** `NaTaCl₆`) *안*에 들어온다** · ✎ **Polyanionic 에서는 황화물(−72.5)이 할라이드(−80.6)보다 낫고 140셀 최선값이 `Na₃PS₄`‖`Na₃V₂(PO₄)₃` = −47** ⇒ ⛔ ***"할라이드가 황화물보다 양극 계면에서 안정하다" 는 P2 에서만, 그리고 `Na₃PS₄` 한 계가 끌고 가는 서술이다.***<br>**⛔ 슬랩 0장** — 면지수·진공·이완자유도·원자수·W_ad·Bader·공간전하 **전부 0회**, 저자 자인 *"does not explicitly capture atomic-scale interface structures or kinetic barriers"*. **NEB/AIMD/MLIP/DOS/COHP/ELF/포논/탄성/BVSE 전부 0건.**<br>**★ 코팅 스크리닝** 12 800 →(중원소·**Li/K/Rb/Cs 제외**·gap<0.5 eV 제외) 7 995 →(`E_hull=0`) →(red<2.5 V & ox>3.5 V) **289** → PCA/K-means 4군 → **엄격 11종**(평균<50·최대<60 meV/atom) / **실용 25종**(최대<110·원소≤4). 대표 `NaB₃O₅`: `Na₂ZrCl₆`‖O3 −213/−224 → **−33/−34**, HSE‖코팅 **−19**. ⛔ **Li 가 원천 제외**돼 목록은 우리 축에 못 옮긴다.<br>**🔴 비판 10건**: ① 동역학 기둥이 **근거 없는 25 meV/atom 문턱 하나** (장벽·과전압 대조 0) ② **결론이 본문을 뒤집는다** (*"does not fully cover"* → *"broadly cover"*; `Table S1` 최고 컷오프 **4.6 V** vs 열역학 3.76 V) ③ **비정질/유리 전해질을 결정 MP 엔트리로** 계산(원전 제목에 *glass*·*amorphous* 가 박혀 있고 헤드라인 F 치환이 하필 그 계) ④ 황화물을 **3종 평균으로만** 제시해 반례를 덮음 ⑤ **PCA–K-means 가 게이트가 아니다** — ✎ 최종 11종 = **Group B 10 + Group A 1**, 실용 25종은 A·B 혼합, 실제 선별은 숫자 문턱; **k=4 근거 0**(elbow/silhouette/seed/표준화 전부 미기재); `Fig. 5b` **본문의 Group A 서술이 값과 뒤바뀜**(SE 쪽 ✎−94.8 을 *"slightly negative"*); ✎ **`Fig. S2` 의 mutual 보정이 이 논문 안에서 한 번도 작동 안 함**(세 부류 전부 hull 위 *가정* ⇒ 식(2)≡식(1)); **`NaB₃O₅` 산화 3.54 V = 25종 중 최저**라 4.4–4.6 V 양극창을 코팅 자신이 못 버팀 ⑥ **내부 불일치 11건**(`NaTaCl₆` 2.18↔2.17 · `Fig. 2b,f` 라벨 **"`Na₂TaCl₆`"** 오기 · `Table S3` `Na₀.₅ZrCl₄F₀.₅` **1.04 V 행 중복** · **`Na₂B₈O₁₃` 이 `Table S6`↔`S7` 에서 환원산물·산화전위·산화산물 3칸 모두 불일치**하고 S7 의 산화산물 `B₆O, Na₃B₇O₁₂` 는 **`NaB₃O₅` 행의 *환원* 산물 복붙 + O₂ 없이 B₆O 라 화학적으로 불가능** · `Na₆Mg(SO₄)₄` 4.11↔4.12 · 필터 (iii) 서술이 **세 번 다름** · *"below −110 meV/atom"* 부호 오용 · `Principle component` 오기 · *"~1 mS cm⁻¹"* 인데 **`Na₂ZrCl₆` 0.018** 포함 4종이 1/3 미만 · Acknowledgements≡Funding 중복) ⑦ **층상 TM 산화물 14종에 무질서·스핀·U 선언 0** (보고량 규율 위험신호 3개 동시 점등) ⑧ **실험 대조 0건**(자기인용 2편의 *"good agreement has been reported"* 한 문장뿐, 저자도 *"experimental studies on Na-halide SEs remain limited"*) ⑨ 코팅 후보에 **수화물 3종 + Cd 1종** ⑩ **재현 불가**(289종 수치·중간목록·코드·MP 스냅샷 전부 없음).<br>**🔑 우리 접점 4**: (i) **ESW 정의·방향표기의 *정례*** — `[Schw21]`(방향이 뒤집힌 반례)의 정확한 대칭 (ii) **`ΔE_D(V)` 열이 우리 `esw_*.json` 에 없다**는 공백을 드러냄(§H 신규) (iii) **계면 보고량이 이미 같다** = 우리 `interface_reactivity` 의 계보 근거 1건 추가 (iv) ✎ **"반응이 만들 상을 미리 깔아라"** — 할라이드‖폴리음이온 산물 `NaZr₂(PO₄)₃` 가 그대로 코팅 추천 목록에 있다(논문은 이 연결을 안 짓는다).<br>**그림 17장 중 7장 실독**(`Fig. 1`·`Fig. 2`·`Fig. 3`·`Fig. 5`·`Fig. 8`·`Fig. S1`·`Fig. S2`); **안 본 것 = `Fig. 4`**(워크플로 — 숫자가 본문·Methods 에 전부 활자)·**`Fig. 6`·`Fig. 7`**(코팅 heatmap — 범위는 본문, 전위·산물은 `Table S6`/`S7` 텍스트; ⚠ **개별 코팅 셀값은 이 digest 에 없다**); 표 7장은 **PDF 텍스트 전사**(그게 정확). 🔧 운영 이슈 1건: **그림 폴더 slug(`jang2026_halide_se_interfacial_stability_highv_na`)가 digest slug 와 달라 webapp 링크가 끊긴다** → rename 제안만(직접 안 고침) | **🔧 방법 원전 = ESW 조작적 정의 + 방향표기 정례 + pseudo-binary 계면 보고량 · ⛔⛔ A–D 물성 4축 *수치* 진입 금지**(Na 계 · vs Na/Na⁺ · 양극 불일치 ⇒ 행이 전부 n/a) — **판정은 `comparison_vs_ours.md` §J-40 한 블록뿐**. 🔗 형제 = **§J-38 `[Schw21]`**(같은 축, Li 계, **방향표기 반례**) · **§J-39 `[Sjolin23AP]`**(같은 축 ESW 관례 표본) |
```

---

## ② `litdb/comparison_vs_ours.md` — **📑 Reference key** 표에 추가할 행

> 표 머리 **직접 확인함**: line 12 `## 📑 Reference key (출처 약칭)` / line 13 **`| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |`** / line 14 `|---|---|---|---|` ⇒ **정확히 4칸.**
> 약칭은 **`[Jang26NaHSE]`** 로 잡았다 (`[Jang23ZnO]` 와 구분됨 — 다른 논문이다).

```markdown
| **[Jang26NaHSE]** 🔴🔴 **`HZ-esw-reduction-limit-label` 의 *세 번째이자 가장 강한* 외부 눈금** · ⛔⛔ **Na 계 + 할라이드 SE → A–D 물성 4축 *수치* 진입 금지** · ⛔ **자체 DFT 0건 (MP 사전계산값 + pymatgen 후처리)** · ⭐ **방향표기의 *정례*(= `[Schw21]` 반례의 대칭)** | **Myeongcho Jang**/**Eunji Kwon**/**Chelin Jeon**/**Sooyeon Kim\***(명지대 화학)/**Seungho Yu\***(**KIST** 에너지저장연구센터 + UST) 2026 ***Small Methods* 10(3), e02179** (DOI `10.1002/smtd.202502179`; 접수 2025-11-01 / 수정 2025-12-26 / 수락 2026-01-04; **CC BY-NC**; KIST 2E33941·2E33943 + NRF(MSIT) RS-2024-00404414·RS-2024-00427700 + **KISTI KSC-2025-CRE-0062**; 본문 10 pp · SI 16 pp · refs 38 · 본문 그림 8 + 표 1 · SI 그림 2 + 표 7) — "**Interfacial Stability and Design Strategies for Halide Solid Electrolytes in High-Voltage All-Solid-State Sodium-Ion Batteries**". **교신 Yu 의 계면-코팅 계산 3부작 3편**(ref 27 = Chun–Shim–Yu *ACS AMI* 14, 1241 (2021) Li 염화물 · ref 28 = Chun 외 *Appl. Surf. Sci.* 616, 156479 (2023) Na 코팅). 방법 원전 = **ref 25 Xiao–Miara–Wang–Ceder *Joule* 3, 1252 (2019)** · ref 33 Zhu–He–Mo *JMCA* 4, 3253 (2016) · ref 35 Richards 외 *Chem. Mater.* 28, 266 (2016). **계 = Na 할라이드 SE 7종**(`Na₂ZrCl₆`·`Na₀.₇La₀.₇Zr₀.₃Cl₄`·`Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅`·`NaTaCl₆`·`NaAlCl₂.₅O₀.₇₅`·`NaTaOCl₄`·`Na₀.₅ZrCl₄F₀.₅`) **× Na 양극 14종**(폴리음이온 2 + P2 6 + O3 6) + 황화물 참조 3종. ⛔ **자체 DFT·자체 실험 0건** — *"obtained from the **Materials Project**"* + *"**pre-computed** first-principles thermodynamic information"* ⇒ **범함수·ecut·k점·슈퍼셀·U·스핀·무질서 전부 미기재(구조적)**, **MP 판본·스냅샷·MP2020 보정 여부도 0**. 소환값(**전부 vs Na/Na⁺ — ⛔ Li 축 이식 금지**): ESW 환원 **1.49–2.18** / 산화 **3.75–3.77 V**(전 계 `NaCl₃`-limited) · 동역학 연장창(**`ΔE_D > −25 meV/atom`**, 근거 0) 산화 **3.92–4.18 V** · 황화물 산화 `Na₃SbS₄` **1.66** / `Na₃PS₄` **2.05** / `Na₁₁Sn₂PS₁₂` **1.91** · 계면 ΔE_D,mutual 할라이드 ✎평균 **−80.6(폴리) / −141.7(P2) / −223.3(O3)**, 황화물 ✎**−72.5 / −226.0 / −254.0** · 코팅 후 **−19 … −35** · 스크리닝 12 800→7 995→**289**→**11/25**종. **🔴🔴 우리에게 값진 것**: 창의 조작적 정의가 ***"the decomposition energy remains zero"*(본문 p.2) + `Table S3` 의 ΔE_D 열 + `Fig. 2e–h` 의 y축 `Na uptake per f.u.`** 로 **두 겹 중복 선언**돼 있고, **7/7 전수에서 0 평탄 바로 아래 계단의 uptake 가 양수** ⇒ **`max(V\|evo>0)` 이 한 계단 아래를 준다는 직접 증거**(✎ Δ = **0.11–1.10 V, 중앙 0.12**). ✎ **저들 식 (2) = pymatgen `use_hull_energy=True`(대수 동일)** ⇒ 계면 보고량이 우리와 같다. 🔴 **비판**: 동역학 기둥이 **근거 없는 문턱 하나** · **결론이 본문을 뒤집음**(*"does not fully cover"*→*"broadly cover"*, 양극 최고 4.6 V) · **비정질/유리 SE 를 결정 MP 엔트리로** · ✎ **황화물 3종 평균이 반례를 덮음**(`Na₃PS₄` 제외 시 O3 −204.9 로 할라이드 범위 안) · ✎ **PCA–K-means 가 게이트가 아님**(최종 11 = Group B 10 + A 1, k=4 근거 0, `Fig. 5b` Group A 서술이 값과 뒤바뀜) · ✎ **mutual 보정이 한 번도 작동 안 함**(전부 hull 위 *가정*) · **슬랩 0장 · NEB/AIMD/DOS/COHP/ELF/포논/탄성/BVSE 0건** · **실험 대조 0건** · 내부 불일치 11건(`Table S6`↔`S7` 의 **`Na₂B₈O₁₃` 산화 행은 화학적으로 불가능** 등) · **재현 불가**(수치·코드·스냅샷 전무) | ✅ `papers/jang2026_halide_se_interfacial_stability_highv_na.md` (2026-09-22; **그림 17장 중 7장 실독** — `Fig. 1`·`2`·`3`·`5`·`8`·`S1`·`S2`; 안 본 것 `Fig. 4`·`6`·`7`; 표 7장은 PDF 텍스트 전사; `Fig. 3` 할라이드 98셀을 `Table S4` 와 **98/98 대조 일치**). 판정은 **§J-40 한 블록뿐** — ⛔ **A–D 물성 4축 진입 없음**(Na 계라 행이 전부 n/a) | **계산 100 %** (MP 데이터 + pymatgen 후처리 + PCA/K-means · **자체 DFT 0 · 실험 0 · 아르지로다이트 0 · Li 계 0**) · 외부 |
```

---

## ③ `litdb/comparison_vs_ours.md` — 본문 블록 **1개** (§J-40)

> **왜 A–D 물성 4축 표가 아닌가**: 이 논문의 물성값은 **전부 Na 계**다 — 전압은 **vs Na/Na⁺**(Li 기준으로 상수 오프셋 변환 불가), 계면에너지는 **Na 양극 상대**, 코팅 목록은 **Li 를 원천 제외한 스크리닝**의 산물이다. §A(이온전도)·§C(기계)·§D(전자구조)는 **자체 계산 0건**이라 행을 만들 값 자체가 없다. ⇒ 규율대로 **`🔧 방법 원전` 블록**으로만 둔다.
> **넣을 자리**: `### J-39`(`[Sjolin23AP]`, 대기 중) **뒤**, `## K. 🧪 수계 Zn 축` **앞**.

```markdown
### J-40. 🔧🔴🔴 **방법 원전 — [Jang26NaHSE] 가 ESW 창을 *두 겹으로* 정의하는 법, 그리고 그것이 우리 `reduction_V` 버그를 7/7 로 재현해 보이는 경위** (2026-09-22 신설)

📎 **출처**: `papers/jang2026_halide_se_interfacial_stability_highv_na.md` · 초안 `_pending_index_jang2026_halide_se_interfacial_stability_highv_na.md`

⛔ **A–D 물성 4축 표에 행을 만들지 않는다** — 값이 **전부 Na 계**다(전압 vs Na/Na⁺ · 양극 Na 층상산화물 · 코팅 스크리닝이 **Li 를 명시적으로 제외**). §A·§C·§D 는 **자체 계산 0건**. ⇒ 이 블록 하나가 판정 전부다.
🔗 **형제 블록**: **§J-38 `[Schw21]`** — 같은 축(ESW 조작적 정의)의 **Li 판**이고 **방향 표기가 논문 안에서 뒤집히는 반례**였다. **이 편은 정확히 그 대칭(정례)이다.** · **§J-39 `[Sjolin23AP]`** — ESW 관례 표본 1건.

**[Jang26NaHSE] `jang2026_halide_se_interfacial_stability_highv_na` — Na 할라이드 SE 7종의 창과 고전압 양극 계면을 MP+pymatgen 으로만 푼 편**
(⛔ 전부 **소환값**이고 **전부 Na 계**다. **자체 DFT 0건** — MP 사전계산값을 후처리한 값이다. 우리 `db/properties/` 절대값과 섞지 않는다.)

**J-40-a. 우리가 이 논문에서 *못* 가져오는 것 (먼저 못박는다)**

| 대상 | 왜 못 가져오나 | 규율 |
|---|---|---|
| **모든 전압** (1.49–2.18 / 3.75–3.77 / 3.92–4.18 V) | **vs Na/Na⁺** 기준. Li 계와 **상수 오프셋 변환되지 않는다**(기준이 각각 그 금속, 화학계가 다름) | ⛔ 수치 이식 금지 |
| **모든 계면 에너지** (−47 … −405 meV/atom) | 이온·양극·MP 판본이 전부 다르다 | ⛔ 우열 판정 금지. **자릿수 점검까지만** |
| **코팅 11/25종 목록** | 필터 (i) 이 *"alkali metals other than sodium (e.g., **Li**, K, Rb, Cs)"* 를 **제외**한다 ⇒ Li 화합물이 후보군에 **원천적으로 없다** | ⛔ *"이 논문이 `Li₃BO₃`/`LiB₃O₅` 를 추천했다"* 는 **불가능한 문장** |
| **"실효 산화 4.1 V"** | 근거 없는 `−25 meV/atom` 문턱의 산물. 장벽 0 · 과전압 실측 대조 0 | ⛔ 인용 금지(J-40-e) |
| **결론 절 *"broadly cover the operating potential range of cathodes"*** | 본문 p.2 는 *"**does not fully cover**"* 라 쓴다. `Table S1` 최고 컷오프 **4.6 V** vs 열역학 3.76 V | ⛔ 결론 쪽 인용 금지 |
| **"할라이드 > 황화물 (계면)"** | ✎ `Na₃PS₄` 한 계가 끌고 가는 서술(J-40-f) | ⛔ 일반화 금지 |
| **양극 간 10–20 meV/atom 서열** | 층상 TM 산화물 14종에 **무질서·스핀·U 선언 0** | ⛔ 서열 판정 금지 |

**J-40-b. 🔴🔴 ESW 조작적 정의 — 우리 버그의 *세 번째* 외부 눈금이자 가장 강한 것**

| 눈금 | 계·이온 | 정의가 활자로 | 방향 표기 | 우리 버그가 보이나 |
|---|---|---|---|---|
| ① **[Zhu15]** | LPSCl · Li | (우리 기록 1.71–2.01 V) | — | ⚠ **값만** ⇒ 간접 |
| ② **[Schw21]** (§J-38) | LPSC 외 11종 · Li | ✅ *"decomposition potential **closest to the stable SE phase**"* | 🔴 **`Table 2` 머리글이 값과 뒤집혀 인쇄됨** | ⚠ 값 대조 ⇒ 간접 |
| ③ **[Jang26NaHSE]** | Na 할라이드 7종 | ✅✅ *"**Within the electrochemical stability window, the decomposition energy remains zero** but increases upon reaching the reduction and oxidation potentials"*(본문 p.2) + **`Table S3` 이 전 사다리를 ΔE_D 열과 함께 인쇄** | ✅✅ **그림의 축**: `Fig. 2e–h`·`Fig. S1d–f` y축 = **`Na uptake per f.u.`**(−1…+5), `← Sodiation` / `Desodiation →` | 🔴🔴 **7/7 에서 직접 보인다** |

⭐ **③이 강한 이유는 값이 아니라 *구조*를 인쇄했기 때문이다** — 우리 필터를 저들 표에 그대로 적용해 틀리는 것을 확인할 수 있다.
🔑 **정의가 두 겹으로 중복 선언**돼 있다: **① ΔE_D = 0** (에너지) **② uptake = 0** (교환량). **`Fig. 2a` 의 `ESW` 음영과 `Fig. 2e` 의 0 평탄이 픽셀 단위로 겹친다**(실독). ⇒ **한쪽이 틀리면 눈에 보인다.** `[Schw21]` 은 이 중복이 없어서 뒤집힌 채로 인쇄됐다.

**J-40-c. 🔴🔴 7종 전수 — `max(V | evolution > 0)` 이 한 계단 아래를 준다**

| SE | 가장자리(= 저들 환원 전위) | **우리 버그가 잡을 값** | **✎ 어긋남 Δ** | 0 평탄 바로 아래 계단의 uptake (`figure-read ≈`) |
|---|---|---|---|---|
| `Na₂ZrCl₆` | **1.69** | 1.57 (`ZrCl₃, NaCl`) | **0.12 V** | **1** |
| `Na₀.₇La₀.₇Zr₀.₃Cl₄` | **1.68** | 1.57 | **0.11 V** | 0.3 |
| `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` | **1.69** | 1.57 | **0.12 V** | 0.7 |
| `NaTaCl₆` | **2.17** (⚠`Table S2` 는 2.18) | 1.81 (`Ta₂Cl₅, NaCl`) | **0.36 V** | 2.5 |
| `NaAlCl₂.₅O₀.₇₅` | **1.49** | 0.39 (`NaCl, Al₂O₃, Al`) | 🔴 **1.10 V** | 1.5 |
| `NaTaOCl₄` | **2.13** | 1.86 | **0.27 V** | 1.5 |
| `Na₀.₅ZrCl₄F₀.₅` | **1.69** | 1.57 | **0.12 V** | 0.85 |
| **우리 LPSCl (comp1·modelc)** | **1.717** (= `ocv_V`) | **1.242** (= `reduction_V`) | **0.475 V** | +5 |

⇒ ✎ **Δ 범위 0.11–1.10 V · 중앙 0.12 · 평균 0.31.** **우리 +0.475 V 가 이 범위 안**이다 ⇒ *"우리만 유난히 크게 틀렸다"* 가 아니라 **"버그 크기 = 그 계 환원 사다리의 마지막 계단 폭"**.
🔴🔴 **그래서 이 버그는 절대값뿐 아니라 *계 간 순위*도 흔든다** — 사다리가 성긴 계(Al 1.10 V)와 촘촘한 계(Zr 0.12 V)가 **1 V 가까이 다르게** 틀린다. ⇒ `HZ-esw-reduction-limit-label`(**BLOCKED**) 판정을 **강화**한다. ⛔ **정정 전 `window_V` 로 매긴 cascade 서열은 전부 무효로 본다.**
✅ **산화 쪽은 우리 규칙이 맞다** — 저들 산화 가장자리 행은 **첫 산화평형**을 이름표로 달아 교환량이 음수이므로 `ox = min(V | evo < 0)` 에 포착된다. **비대칭의 원인은 사다리 이름표 규약**이지 우리 실수의 두 번째 종류가 아니다.

**J-40-d. ⭐⭐⭐ 그리고 수정이 싸다 — 우리 도구는 이미 정답을 갖고 있다**

`Table S2` 는 **숫자와 산물의 출처를 일부러 다르게** 쓴다(7/7 일관, 우리 대조):

| 저들 양식 | LPSCl(comp1) 의 값 | 우리 `esw_lis4excluded.json` 의 칸 |
|---|---|---|
| **환원 전위 (숫자)** | **1.717 V** | 🔴 **`ocv_V`** ← 이름이 `OCV` 로 붙어 있다 |
| *"환원 전위에서의 평형상"* (= **아래 계단** 산물) | `5 Li₂S + LiCl + P` | **`reduction_V`(1.242 V) 행의 반응식** |
| **산화 전위 (숫자)** | **2.256 V** | ✅ `oxidation_onset_V` |

⇒ ⭐ **재계산이 아니라 이름 바꾸기 + `window_V` 재유도로 끝난다** (cascade 356 행 재실행 불필요):
`window_V : ox − red → ox − ocv` · `reduction_limit_V → first_reduction_products_V` · `ocv_self_decomposition_V → reduction_limit_V`
⚠ **전제조건 1개**: `esw_cascade_batch.py:419` 의 `ocv = min(V | |evo| ≤ 1e-6)` 은 **교환-0 행이 하나일 때만** 가장자리를 준다. 이 논문 7종도 LPSCl 도 하나였다. **cascade 356 행에서 교환-0 행이 2개 이상인 계가 있는지 먼저 세는 것**이 fix 의 선행 작업이다.

**J-40-e. ⭐ 동역학 연장창 — ✎ 우리가 레시피를 복원했고, 그것이 논문 헤드라인 하나를 무너뜨린다**

문턱 = **`ΔE_D > −25 meV/atom`**(본문 p.2, **근거 문장 0 · 인용 0 · 장벽 계산 0**). ✎ `Table S3` 인접 2행 **선형보간**으로 **7종 중 6종을 ±0.01 V 재현**(`Na₂ZrCl₆` 3.92 ✅ · `Na₀.₇La₀.₇Zr₀.₃Cl₄` 4.06 ✅ · `NaTaCl₆` 4.06 ✅ · `NaAlCl₂.₅O₀.₇₅` 4.15 ✅ · `Na₀.₆₂₅Y…` 4.13↔4.12 · `NaTaOCl₄` 4.02↔4.03 · ⚠ `Na₀.₅ZrCl₄F₀.₅` 4.22↔4.18).

🔴🔴 **그 검산이 드러낸 것**: 본문 *"fluorination … increasing the potential from **3.92 to 4.18 V**"* 인데 **열역학 산화 onset 은 3.75 → 3.76 = +0.01 V** 다. ✎ 실제로 바뀐 것은 **onset 이후 ΔE_D 기울기 −0.148 → −0.055 eV/V (2.7배 완만)**.
⭐⭐ **이것이 우리 §B 축 명명 규율의 *이온종 독립* 외부 실증이다** — 우리 `comp1`→`modelc` 에서 **Cl 증량이 onset 을 0.000 V 움직인다**(2.256 V 고정, S²⁻-limited). 저들은 **Cl→F 가 onset 을 +0.01 V 움직인다**(`NaCl₃`-limited). ⇒ ***"할로겐 치환은 축①(onset)을 안 건드리고 축②·③(분해 양·속도·산물)을 건드린다" 가 Li-황화물과 Na-할라이드 양쪽에서 성립한다.***
🔑 **같은 구조의 세 번째 얼굴**: 저들 산화 한계 7종이 **3.75–3.77 V 에 몰리는 이유가 활자로 있다** — *"oxidative decomposition **consistently involves the formation of `NaCl₃`**"*. **한 음이온이 산화 변을 독점한다.** 우리 S²⁻-limited 와 **같은 현상**이다.
⛔ **단 25 meV/atom 을 그대로 베끼지 않는다.** 우리가 문턱을 쓰려면 **`[Du22LMR]`·`[Wei23LNO]`·`[Deng26PS]` 의 실측 과전압(0.05–0.45 V)에서 역산**하는 쪽이 정직하고, **보고량 카드를 먼저** 채운다.

**J-40-f. 🔴 할라이드 vs 황화물 — 통설이 어디서 깨지나 (✎ 논문이 안 말하는 것)**

| 축 | 판정 |
|---|---|
| **① 산화 창 (열역학)** | ✅ **통설이 크게 이긴다** — 할라이드 **3.75–3.77** vs 황화물 **1.66 / 1.91 / 2.05 V** = **+1.7 … +2.1 V**. 논쟁 여지 없음 |
| **③ 양극 계면 (화학)** | 🔴 **반쯤 깨진다** — ✎ 계열평균: **폴리음이온 할라이드 −80.6 vs 황화물 −72.5 (황화물 우세)** · **P2 −141.7 vs −226.0 (할라이드 우세)** · **O3 −223.3 vs −254.0** 인데 **`Na₃PS₄` 를 빼면 황화물이 P2 −188.7 / O3 −204.9 로 뛰고, O3 에서 `Na₃SbS₄`(−200.5)·`Na₁₁Sn₂PS₁₂`(−209.3) 가 할라이드 7종 범위(−194.5 … −255.0) *안*에 들어온다** |

⇒ ⛔ **"할라이드가 황화물보다 양극 계면에서 안정하다" 는 P2 에서만, 그리고 `Na₃PS₄` 한 계가 끌고 가는 서술이다.** 140셀 최선값이 **`Na₃PS₄`‖`Na₃V₂(PO₄)₃` = −47** 이라는 것도 본문에 없다.
🔑 **할라이드 고유 산화 채널**(`Table S4` 98행, 우리 정리): ① **음이온 교환**(양극 O ↔ SE Cl → `ZrO₂`/`Ta₂O₅`/`Al₂O₃` + `NaCl`) ② **Cl 의 추가 산화 → `NaClO₄`**(황화물 계면엔 없는 종, 그리고 **과염소산염은 산화제**다 — 논문은 표에 적기만 하고 함의를 논하지 않는다) ③ **TM 염화**(`NiCl₂`·`Na₂CoCl₄`·`NaFeCl₄`·`VCl₃`). ⭐ **우리 `comp1|LCO` 의 `LiCl`(할로겐 배출) ↔ 저들 `NaCl`, 우리 `Li₂SO₄`(음이온의 추가 산화) ↔ 저들 `NaClO₄`** — **구조가 대응한다.**

**J-40-g. ⭐ 계면 보고량이 이미 같다 (✎ 우리 대수 유도)**

저들 식 (2): ΔE_D,mutual = ΔE_D(A,B,x) − xΔE_D(A) − (1−x)ΔE_D(B)
✎ 전개하면 = **E_eq(mix) − [x·E_hull(A) + (1−x)·E_hull(B)]** = **pymatgen `InterfacialReactivity(use_hull_energy=True)` 와 대수적으로 동일**. 둘 다 **혼합비 x 전 구간 최댓값**을 보고한다.

| | 우리 | 이 논문 |
|---|---|---|
| 보고량 | hull 기준 pseudo-binary, x 최댓값 | **같은 것** |
| 값 | `comp1\|LiCoO₂` **−322.7 meV/atom** (min @ **x = 0.5302**) | `Na₃PS₄\|O3` ✎평균 **−352** · 최악 `Na₃PS₄\|NaNi₀.₅Fe₀.₅O₂` **−405** |
| **x 를 기록하나** | ✅ **한다** | 🔴 **본문·표 어디에도 없다** — `Fig. 8` 에서만 읽힌다 (`figure-read ≈` HSE‖코팅 **x 0.07** / 양극‖HSE **x 0.35**) |
| MP 판본·상 배제 | ✅ **MP2026 · 배제 3상 명시** | 🔴 **전부 미기재** |

⇒ ⭕ **쓸 수 있는 문장**: *"우리 `Li₆PS₅Cl`‖`LiCoO₂` 의 −0.32 eV/atom 은 **같은 보고량**으로 계산된 Na 황화물‖O3 의 −0.31 … −0.41 eV/atom 과 같은 크기 범위에 있다"* — **자릿수·부호 점검까지.**
⛔ **쓰면 안 되는 문장**: *"우리 값이 저들 할라이드(−0.22)보다 나쁘다"* — 이온·양극·MP 판본이 달라 **우열 판정이 아니다**.
⚠ **그리고 범위에서는 우리가 밀린다** — 저들은 **140 셀 × 14 양극 + 코팅 12 800 종 스크리닝**을 냈고 우리는 소수 짝뿐이다. ⭕ **우리가 나은 두 칸은 `x` 기록과 MP 판본 명시뿐**이다.

**J-40-h. ⛔ 계면 기하 — 슬랩은 0장이다 (우리 v5 와 대조점 없음)**

| 항목 | [Jang26NaHSE] | 우리 v5 |
|---|---|---|
| 슬랩 / 면지수 / 진공 / 이완자유도 / 원자수 | ⛔ **전부 0회** | ✅ 전부 선언됨 |
| W_ad · Bader · 공간전하층 | ⛔ **0회** (`[Haru14]` 계보 인용조차 없다) | — |
| 대신 있는 것 | **pseudo-binary ΔE_D,mutual** | 우리도 있음 |
| 저자 자인 | ✅ *"does not explicitly capture **atomic-scale interface structures** or kinetic barriers"* · *"bulk **crystalline** phases … may exhibit **amorphous, nanocrystalline, or metastable** phases"* · *"without accounting for … **moisture sensitivity**"* | — |

⇒ **이 세 자인이 이 논문에서 제일 정직한 자리다** — 인용할 때 반드시 같이 옮긴다.

**J-40-i. ⚠ 반면교사 — 스크리닝 깔때기의 군집이 게이트가 아니다**

✎ 최종 **엄격 11종 = Group B 10 + Group A 1**, **실용 25종은 A·B 혼합**(`Table S5` 대조). 실제 게이트는 *"평균<50 · 최대<60"* / *"최대<110"* 이라는 **같은 ΔE_D,mutual 에 건 숫자 문턱**이다. **k=4 근거 0**(elbow·silhouette·seed·표준화 미기재), `Fig. 5b` **본문의 Group A 서술이 값과 뒤바뀐다**(SE 쪽 ✎−94.8 을 *"slightly negative"* 라 씀; 실제로 낮은 쪽은 양극 ✎−26.3).
⇒ **`[Park26ML]` §J-22-3(*"선택 기준이 실제로는 하나뿐이었다"*)과 같은 구조의 2호 사례.**
✎ **추가**: `Fig. S2` 가 설명하는 mutual 보정이 **이 논문 안에서 한 번도 작동하지 않는다** — SE·양극을 *"assumed to be … on the convex hull"* 로 두고 코팅은 `E_hull=0` 으로 걸렀으므로 세 부류 전부 ΔE_D = 0 ⇒ **식 (2) ≡ 식 (1)**. 특히 **`Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂` 같은 다원 비화학량론 조성을 "hull 위" 로 *가정*한 것**이 결과 전체에 들어 있다.

**J-40-j. ⭐ 이식 후보 1건 — "반응이 만들 상을 미리 깔아라"**

✎ 할라이드‖폴리음이온 양극의 분해산물이 **`NaZr₂(PO₄)₃`·`TaPO₅`·`LaPO₄`·`YPO₄`**(인산염/NASICON)이고 그래서 구동력이 절반 이하다. **그리고 그 `NaZr₂(PO₄)₃` 가 최종 코팅 추천 25종에 그대로 들어 있다.** 논문은 이 연결을 **짓지 않는다**.
⇒ **우리 축으로 옮기면**: `comp1|LiCoO₂` 산물 5종(`Li₃PO₄`·`Li₂SO₄`·`Li₂S`·`LiCl`·`Co₉S₈`) 중 **열역학적으로 안정한 것을 코팅 후보로 되먹임**하는 한 줄 검사. **`Li₃PO₄` 는 이미 우리 코팅 표에 있다** ⇒ 산수 한 번으로 확인 가능한 가설이다.
```

---

## ④ 정정 / 신설 제안 문구 (조율 세션이 판단할 것)

> 아래는 **제안**이다. 내가 직접 고치지 않았다. **`db/` 는 손대지 않았다.**

### ④-1. `db/properties/citation_hazards.json` — `HZ-esw-reduction-limit-label` 의 **근거 보강** (재판정 아님)

> 이미 **BLOCKED** 로 등록돼 있다(line 199, 2026-09-22). **level 변경 제안 없음.** `evidence`/`what` 에 **세 번째 눈금**을 덧붙이자는 제안이다.

```
추가 제안 문구 (evidence 항목):
"[Jang26NaHSE] (Small Methods 10, e02179 (2026)) 가 Na 할라이드 7종에서 같은 관례를 두 겹으로 인쇄한다 —
 본문 p.2 'the decomposition energy remains zero' + Table S3 의 ΔE_D 열 + Fig. 2e–h 의 y축 'Na uptake per f.u.'.
 7/7 전수에서 창의 아래 가장자리 바로 밑 계단의 uptake 가 양수이므로 max(V|evolution>0) 은 한 계단 아래를 준다.
 어긋남 Δ = 0.11–1.10 V (중앙 0.12), 우리 cascade 중앙 +0.475 V 가 그 범위 안.
 ⇒ 버그 크기 = 그 계 환원 사다리의 마지막 계단 폭이므로 계 간 순위도 흔든다.
 출처: papers/jang2026_halide_se_interfacial_stability_highv_na.md §3b·§4-3·§7-3"
```

### ④-2. `tools/oxidation/*.py` — **수정 제안** (⛔ 코드 안 고쳤다)

> ⭐ **핵심: 재계산이 아니라 rename + 재유도다.** cascade 356 행을 다시 돌릴 필요가 없다.

```
esw_cascade_batch.py:435   window_V = ox − red        →   ox − ocv
esw_cascade_batch.py:      reduction_limit_V          →   first_reduction_products_V   (= Table S2 의 "평형상" 칸)
esw_cascade_batch.py:      ocv_self_decomposition_V   →   reduction_limit_V            (= Table S2 의 "환원 전위" 칸)
constrained_esw.py:91–93   동일 (red/ox 반환 라벨)
```
**⚠ 선행 작업 1건 (이것 없이 적용 금지)**: `ocv = min(V | |evo| ≤ 1e-6)` 은 **교환-0 행이 하나일 때만** 가장자리를 준다.
⇒ **cascade 356 행에서 교환-0 행이 2개 이상인 계가 있는지 먼저 센다.** (이 논문 7종·LPSCl 은 전부 1개였다.)
**⚠ 선행 작업 2건**: `kb/templates/estimand_card.md` §1–3 — *"환원 한계 ≡ Li 교환량이 0 에서 벗어나기 시작하는 가장 높은 φ"* 를 **결과 보기 전에** 적는다 (`[Schw21]` digest §7-8 이 이미 요구한 것, **중복 제안 아님**).

### ④-3. `comparison_vs_ours.md` **§H** 신규 행 — ⭐ **이 논문이 새로 드러낸 공백**

> 표 머리 **직접 확인함**: line 1008 `## H. ⚠️ 우리가 아직 못 하는 것 (정직 목록 → 향후)` / line 1009 **`| gap | 누가 필요로 함 | 보강책 |`** / line 1010 `|---|---|---|` ⇒ **3칸.**

```markdown
| **🔴 🆕 우리 ESW 출력에 `ΔE_D(V)` 열이 없다 — 창을 *에너지로* 교차확인할 수단이 없고, 동역학 연장창을 정의할 수도 없다** (2026-09-22 신설) | **[Jang26NaHSE]** `Table S3` 이 전 분해 사다리를 **(임계전위, ΔE_D[eV/atom], 평형상)** 세 열로 인쇄한다. 그 두 번째 열이 있어서 저들은 ① 창 판정을 **ΔE_D = 0 으로도** 할 수 있고(= `Na uptake = 0` 과 **중복 선언** ⇒ 라벨이 틀리면 눈에 보인다) ② **`Fig. 2a` 형 프로파일**을 그릴 수 있고 ③ **문턱 기반 동역학 연장창**(`ΔE_D > −25 meV/atom` ⇒ 산화 +0.16 … +0.42 V)을 정의할 수 있다. 우리 `db/properties/esw_lis4excluded.json` 의 `steps` 는 **`[전압, evolution, 반응식]` 세 칸뿐**이라 셋 다 못 한다 — 그리고 **중복 선언이 없었기 때문에 `reduction_V` 라벨 오류가 3개월 넘게 살아남았다**(`HZ-esw-reduction-limit-label`) | **① `ΔE_D(V)` 열을 `esw_*.json` `steps` 에 추가** (각 breakpoint 에서 SE 의 hull 거리). ⛔ **던지기 전 보고량 카드** — *"ΔE_D ≡ 그 μ_Li 에서 SE 조성의 평형에너지 − SE 자신의 에너지, eV/atom"* 을 먼저 적는다. **② 그림 표준 변경**: `Li uptake per f.u.` 계단과 `ΔE_D(V)` 프로파일을 **같은 x축으로 나란히** 그린다(= `[Jang26NaHSE]` `Fig. 2` 양식) — **둘이 어긋나면 눈에 보인다**. **③ 동역학 문턱은 베끼지 않는다** — 저들 25 meV/atom 은 **근거 문장이 0**이다. 우리가 쓰려면 **`[Du22LMR]`·`[Wei23LNO]`·`[Deng26PS]` 의 실측 과전압(0.05–0.45 V)에서 역산**한다. 📎 출처: `papers/jang2026_halide_se_interfacial_stability_highv_na.md` §4-2·§7-8·§12-3 |
```

### ④-4. 🔧 **운영 — 그림 폴더 rename 제안** (직접 안 고쳤다)

```
litdb/figures/jang2026_halide_se_interfacial_stability_highv_na/
      →  litdb/figures/jang2026_halide_se_interfacial_stability_highv_na/
```
**이유**: 폴더 slug 가 **파일명 기반**이라 digest slug(`<firstauthor><year>_<topic>` 관례)와 다르다. webapp 이 `figures/<slug>/` 로 찾으면 **이 digest 의 그림 17장이 전부 안 붙는다**. 파일 내용은 그대로 두고 디렉터리만 옮기면 된다(또는 심볼릭 링크). `figures.json` 안의 `slug` 필드도 같이 고친다.
⚠ 같은 종류의 불일치가 다른 digest 에도 있는지는 **확인하지 않았다** — `tools/litdb/extract_figures.py --audit-src` 계열에 **slug 일치 검사**를 붙이는 것이 근본 대책으로 보인다.

### ④-5. ⛔ **중복 제안하지 않은 것** (다른 대기 파일이 이미 올렸다)

- `our_dft_baseline.md` L20 의 *"환원 한계 1.242 V / OCV 1.717 V"* 라벨 교체 → **`_pending_index_schwietert2021_…md` 가 이미 제안**했다. 이 논문은 **그 제안의 근거를 하나 더할 뿐**이다.
- `kb/open_items.md` 의 *"Zhu15 3.4× 감사"* 갱신 → 동일.
- `db/governance/decisions.json` 의 *"환원 한계" 보고량 카드* 신설 → 동일.
- ⇒ **조율 세션은 그쪽 파일의 문구를 쓰고, 여기서는 ④-1 의 `evidence` 한 줄만 덧대면 된다.**
