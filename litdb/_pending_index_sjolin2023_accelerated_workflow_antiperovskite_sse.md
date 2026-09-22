# 병합 대기 — `sjolin2023_accelerated_workflow_antiperovskite_sse`

> 작성 2026-09-22 (litdb-curator 세션). **이 세션은 `INDEX.md`·`comparison_vs_ours.md`·`db/` 를 건드리지 않았고 커밋도 하지 않았다.**
> 쓴 파일은 **① `litdb/papers/sjolin2023_accelerated_workflow_antiperovskite_sse.md`** 와 **② 이 파일** 둘뿐이다.
> (그 밖에 그림 폴더 `litdb/figures/sjolin2023_accelerated_workflow_antiperovskite_sse/` 를 표준 도구로 생성했다 — 아래 **④-3** 참조.)
>
> **⚠ §J 번호는 `J-39` 로 잡았다.** 근거: 병합본 `comparison_vs_ours.md` 에 **J-38(`[Schw21]`)까지 실재**함을 직접 확인(line 5394). J-39 는 전문 검색 결과 **0 hit**. 동시에 도는 에이전트가 J-39 를 먼저 쓰면 **번호만 바꾸고 내용은 그대로** 써도 된다 (블록 안의 자기참조는 머리 1줄뿐).

---

## ① `litdb/INDEX.md` — 추가할 행

**권장 위치**: `## ✅ Digest 완료 (paper-level)` (열 순서 **`slug | 논문 | 축`**)
— 근거: 이 편의 우리 쪽 값어치가 **스크리닝 깔때기 *구조* 축**이고, 같은 성격의 `[Basu26]`(line 137)이 이미 그 절에 `⛔물성 4축 비교 제외` 태그를 달고 들어가 있다.
**대안 위치**: `## ⚠ EXTERNAL …` (열 순서 **`slug | 논문 | 보관 이유 (analogy/vocabulary-only)`**) — `[Ziemke26AP]`(line 204)와 나란히 두고 싶으면 이쪽. **3열 문구를 그대로 써도 양쪽 헤더에 다 읽힌다.**

| slug | 논문 | 축 |
|---|---|---|
| `papers/sjolin2023_accelerated_workflow_antiperovskite_sse.md` ★★**스크리닝 깔때기 *구조* 원전 + 🔧 대리 NEB 방법 원전** | **[외부·반안정상 antiperovskite·⛔ 물성 4축 진입 금지(계 불일치)·DFT 전용(실험 0)]** ✅ **Benjamin H. Sjølin**/**Peter B. Jørgensen**/A. Fedrigucci/**Tejs Vegge**/**Arghya Bhowmik\***/**Ivano E. Castelli\*** (**DTU Energy** + EPFL THEOS), "**Accelerated Workflow for Antiperovskite-based Solid State Electrolytes**" (***Batteries & Supercaps* 6, e202300041 (2023)**, DOI `10.1002/batt.202300041` · **OA CC BY-NC** · NordBatt 2022 특집 · 본문 8 pp + refs 2 pp · 그림 8 + 표 2 · **SI 없음**(Materials Cloud 저장소로 대체) · EU **BIG-MAP** 957189 + BATTERY2030+ 957213 + VILLUM **DeepDFT**).<br>**계**: `X₃BA` **Pm-3m 5원자 셀**, X = **Li·Na·Mg**, B = H·B·C·N·O·F·P·S·Cl, A = 나머지 대부분 ⇒ **1317 조성**. `Fig. 1` 실독 = A 꼭짓점(1a)·B 체심(1b)·**X 면심(3c)**, X₆B 팔면체.<br>**★① 워크플로 6단 (`Fig. 3` 실독)**: **1317** →(구조적합 5조건: 각 90±2°·길이 0.5 Å·X–A 0.5 Å·X–B 0.5 Å·팔면체각 90±13°) **−502(38 %)**→ **815** →(**E_hull < 0.2 eV/at**, pymatgen+MP) **−701(86 %)**→ **114** →(**gap > 0.5 eV**, PBE relax 고유값 재사용) **−85(75 %)**→ **29** →(**ESW > 1 V**, GPPD) **−15**→ **14** →(**S-NEB top 10**) **−4**→ **10** CI-NEB.<br>**★ 가속의 정체 = 마지막 단 하나 (S-NEB)**: 정적 `CHGCAR` 를 퍼텐셜면 삼아 NEB(PyTorch-AutoNEB+string+Henkelman 접선, 20점·2000스텝·lr 0.5·모멘텀 0.1) → TS 좌표 X° → **2×2×2 슈퍼셀 SCF 2회(공공/TS)의 차**. 🔴 ***"neither of which are re-relaxed"* = 이온 이완 0** ⇒ **w_S = 0.470 은 빠진 이완의 역수**(우리 유도: 원 S-NEB/CI-NEB **평균 2.13 · 범위 1.36–3.31**). 속도 **10–30×**, **MAE 73 · SD 96 meV · MRE 20 %**(Li 56/Na 49/**Mg 171**).<br>**★ `Table 2` 14 후보**(E_hull/gap/ESW/E‡_S/E‡_NEB): `Li₃SI` 0.195/3.7/**2.52**/272/**175** · `Li₃FSe` 0.057/3.8/2.13/**124**/194 · `Li₃FTe` 0.065/3.0/1.58/166/198 · `Li₃HSe` 0.017/3.6/**1.01**/184/265 · `Li₃HTe` 0.012/3.1/1.03/224/293 · **`Li₃OCl` 0.145/4.9/2.86/424/380** · *`Li₃OBr`* 0.157/4.5/2.80/478/419 · `Na₃FSe` 0.044/2.0/1.58/227/279 · `Na₃SI` 0.172/2.5/2.01/292/313 · `Na₃OCl` 0.139/2.0/1.73/418/329 · `Na₃FTe` 0.022/2.1/1.40/298/355 · *`Na₃OBr`* 0.138/1.9/1.85/478/459 · *`Na₃OI`* 0.138/2.0/1.15/563/553 · *`Mg₃NAs`* 0.053/1.3/1.21/826/616 (*기울임* = S-NEB top 10 밖 4종 = **CI-NEB 하위 4종과 동일**).<br>**🔎 우리 유도(논문 미보고)**: 14종 **Spearman ρ = 0.925** 인데 **최대 순위이동 5칸이 하필 CI-NEB 1위 `Li₃SI`(→6위)** ⇒ *"집합은 같고 순서는 다르다"*.<br>**⛔ 이 논문에 없는 것**: **MD 0건**(`MSD`·`Arrhenius`·`Haven`·`Nernst` **전부 0회**, `temperature` 2회는 서론 산문) · σ 0 · D 0 · Ea 0 · **기계 0** · DOS/Bader/COHP/ELF/phonon 0 · **무질서 0**(`disorder`·`SQS`·`concentration` 0회) · **스핀 0**(`spin`·`ISPIN`·`+U` **0회**인데 A-자리에 전이금속 전열).<br>**🔴 비판 6**: ① **기준이 내부 이미지 1개짜리 CI-NEB**(Mg 만 3개) ⇒ *"73 meV = 정확한 장벽"* 으로 읽으면 안 된다 ② **본문이 `Fig. 7` 을 잘못 센다** — *"the 4 outliers"* 라는데 **실제 라벨은 6개**(figure-read 로 해소: 실패 4 = `Mg₃CTe`·`Mg₃CSe`·`Na₃PCd`·`Na₃PHg`, 전부 B-자리 C/P) ③ **w_S 가 in-sample**(held-out 0) + **실패 판정이 "visual inspection"**(알고리즘·문턱 0줄) ④ **ESW 를 두 겹으로 넓힌다** — 알칼리 산화물 제외 + **E_hull 만큼 에너지 인위 인하**(`Li₃SI` 0.20 eV/at) ⇒ 저자 스스로 *"metastable phase diagram"* ⑤ **ESW 폭만 싣고 상·하한 0** ⇒ 우리 `reduction_limit_V` 라벨 논쟁에 **정의 문장만** 대응 ⑥ **MP 스냅샷·entry 목록 미기재**(우리 `phase_set_id` 계약이 메우는 공백) · 코드 공개가 **미래시제**.<br>**🔴 우리에게 불리한 것 3**: ⓐ **우리 G4 BVSE 프록시는 어떤 기준에도 대 본 적이 없다**(그들은 MAE/SD/MRE/parity/ρ 를 공표) ⓑ **우리 깔때기에 전자절연 게이트가 없다**(그들은 갭이 75 % 를 죽이는 2위 필터) ⓒ **B-자리 P 의 S-NEB 실패율 76 %** = 우리 host 골격 중심이 P(PS₄³⁻) ⇒ 전하밀도 NEB 이식 전 `Fig. 8` 식 닫힌고리 검사 필수.<br>**⚠ 저자 자인**: *"찾은 후보는 전부 이미 알려진 것 — 이 조성·이 공간군에 새 SSE 후보는 없다"* (실험 앵커 **2점뿐**: `Li₃SI` 0.29 eV · `Li₃FSe` 0.18 eV; ESW 실험은 `Li₃SI` 10 V **1점**, 계산 2.52 V 와 **4배**).<br>✅ (2026-09-22 · 본문 10 pp 전독 · **그림 8/8 실독** · 표 2장은 PDF 텍스트 전사) | **축 = 스크리닝 깔때기 *구조* + 🔧 대리(surrogate) 수송 모델의 *오차예산* 원전.** ⛔ **물성 4축(A–D) 진입 금지** — 계가 다르고(산화/황/수소 antiperovskite ↔ 황화물 argyrodite) **E‡(0 K 단일 hop) 를 우리 Ea(유한온도 아레니우스) 옆에 놓을 수 없다**. `comparison_vs_ours.md` **§J-39** 의 `🔧 방법 원전` 블록에만 자리가 있다. 🔗 `[Ziemke26AP]`(같은 `Li₃OCl`, §J-7) 와 **3건 충돌** — 특히 **`Li₃OCl` E_hull = 0.145 eV/at**(ziemke 는 hull 0건) |

> ⚠ **3열 문구 재사용**: EXTERNAL 절에 넣을 경우 3열 머리는 `보관 이유` 다. 위 문구 앞에 *"보관 이유 = "* 만 붙이면 그대로 읽힌다 (내용이 이미 "왜 들고 있나" 로 쓰여 있다).

---

## ② `litdb/comparison_vs_ours.md` — **§📑 Reference key** 에 추가할 행

열 순서 **`약칭 | 논문 (저자·년·저널) | digest/status | 유형`** (line 13–14 확인).

| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |
|---|---|---|---|
| **[Sjolin23AP]** ★★ **스크리닝 깔때기 *구조* 원전** · 🔧 **대리 NEB(S-NEB) 방법 원전** · ⛔⛔ **물성 4축 진입 금지 — 계 불일치 + E‡↔Ea 범주 불일치** · ⚠ **ESW 가 두 겹으로 넓혀져 있다** | **Benjamin H. Sjølin**/**Peter B. Jørgensen**/A. Fedrigucci/**Tejs Vegge**/**Arghya Bhowmik\***/**Ivano E. Castelli\*** (**DTU Energy** + EPFL THEOS) 2023 ***Batteries & Supercaps* 6, e202300041** (DOI 10.1002/batt.202300041; OA CC BY-NC; NordBatt 2022 특집; 본문 8 pp · 그림 8 · 표 2 · **SI 없음** — Materials Cloud 대체; BIG-MAP 957189 · BATTERY2030+ 957213 · VILLUM DeepDFT) — "**Accelerated Workflow for Antiperovskite-based Solid State Electrolytes**". **`X₃BA` Pm-3m 5원자 셀 · X = Li/Na/Mg · 1317 조성**, **6단 깔때기 1317→815→114→29→14→10**(구조적합 −502 / **E_hull<0.2 eV·at⁻¹** −701 / **gap>0.5 eV** −85 / **ESW>1 V** −15 / S-NEB top10 −4). **가속 부품은 마지막 단 하나** = **S-NEB**(정적 CHGCAR 위 NEB → TS 좌표 → **미완화 2×2×2 슈퍼셀 SCF 2회 차이**), **10–30× · MAE 73 / SD 96 meV / MRE 20 %**(Li 56 · Na 49 · **Mg 171**), **w_S = 0.470**. `Table 2` 14후보(예: **`Li₃OCl` E_hull 0.145 · gap 4.9 · ESW 2.86 V · E‡_NEB 380 meV**, `Li₃SI` 0.195/3.7/2.52/**175 meV**). VASP·PBE·**MP pseudo 세트**·520 eV·**7×7×7→4×4×4**·F_max 0.02 eV/Å·rattle 0.01 Å·Gaussian 0.05 eV·`NG(XYZ)=50`. ⛔ **MD·σ·D·Ea·기계·DOS·무질서·스핀 전부 0건**. ⚠ **저자 자인: 신규 후보 0** | ✅ `papers/sjolin2023_accelerated_workflow_antiperovskite_sse.md` — 판정은 **§J-39** 의 `🔧 방법 원전` 블록**뿐** (A–D 물성 4축 행 **없음**) | **DFT 전용 스크리닝 (실험 0 · MD 0 · 온도 0)** |

---

## ③ `litdb/comparison_vs_ours.md` — 새 블록 (J-37/J-38 뒤, §K 앞)

> **번호 = J-39.** 앞 블록 J-38(`[Schw21]`) 바로 뒤, `## K. 🧪 수계 Zn 축` 앞에 넣는다.

```markdown
### J-39. 🔧★★ **깔때기 원전 — [Sjolin23AP] 의 "accelerated workflow" 가 정확히 무엇이고, 우리 cascade 와 어디가 겹치나** (2026-09-22 신설)

📎 **출처**: `papers/sjolin2023_accelerated_workflow_antiperovskite_sse.md` · 초안 `_pending_index_sjolin2023_accelerated_workflow_antiperovskite_sse.md`
🔗 형제: **§J-38(`[Schw21]`)** — ESW 정의·`reduction_V` 라벨 축은 그쪽이 정본이고, 이 블록은 **외부 관례 표본 1건을 더할 뿐**이다.
🔗 같은 물질: **§J-7 `[Ziemke26AP]`**(`Li₃OCl` 치환결함) — **3건 충돌**(J-39-f).

⛔ **A–D 물성 4축 표에 행을 만들지 않는다** — 계가 다르고(Pm-3m 5원자 antiperovskite ↔ F4̄3m 52원자 황화물 argyrodite),
   이 논문의 **σ·D·Ea·기계·DOS·무질서가 전부 0건**이며, 유일한 수송량 `E‡`(0 K 단일 hop 안장점)는
   우리 `Ea`(유한온도 아레니우스 기울기)와 **범주가 다르다**. (§J-7 머리말 규율: 값 없는/비교불가 행을 4축에 넣으면 표가 무의미해진다.)

**J-39-a. 우리가 이 논문에서 *못* 가져오는 것 (먼저 못박는다)**

| 양 | 이 논문 | 결론 |
|---|---|---|
| **σ · D · MSD · Haven** | ❌ `MSD`·`Haven`·`Nernst` **전문 0회**. 장벽을 전도도로 환산조차 안 한다 | ⛔ 존재하지 않는 값 |
| **Ea (아레니우스)** | ❌ `Arrhenius` **0회**. `temperature` 2회는 둘 다 서론 산문 — **전 계산 0 K** | ⛔ `E‡` 를 우리 Ea 옆에 놓지 마라 |
| **기계 (E/B/G·C_ij)** | ❌ 0건 | ⛔ 우리 G5 축에 **아무것도 못 준다** |
| **밴드갭 절대값** | ⚠ PBE + **smearing 0.05 eV 가 걸린 relax 런의 고유값 2개 차** (전용 nscf 아님). 저자 자인 *"일부 오분류 예상"* | ⛔ 우리 fixed-occ nscf 값(2.066/2.099)과 **같은 표 금지** |
| **ESW 값 [V]** | ⚠ **두 겹으로 넓혔다**(J-39-e) + **폭만, 상·하한 0** | ⛔ 수치 이식 금지. 가져오는 것은 **정의 문장 1줄** |
| **`w_S = 0.470`** | 그들의 *미완화* 2×2×2 슈퍼셀에 대한 경험 보정치 | ⛔ 다른 셋업으로 이식 금지 |
| **조성축(Cl·O·B 도핑)** | ❌ **0건** — 도핑 개념 자체가 없다(정비화학량 신조성 열거) | ⛔ Cl-rich 유불리에 **중립** |

**J-39-b. ★① 워크플로 전수 (`Fig. 3` 실독) — 단·기준·통과수**

| 단 | 기준 | 들어옴 → 남음 (잃음) | 엔진 |
|---|---|---|---|
| 0 Structural Relaxation | — | — → **1317** | VASP PBE 520 eV · 7×7×7 · F_max 0.02 eV/Å · rattle σ 0.01 Å · Gaussian 0.05 eV · `NG(XYZ)=50` |
| 1 Antiperovskite Structure Check | 각 **90±2°** · 셀길이 서로 **0.5 Å** · X–A **0.5 Å** · X–B **0.5 Å** · 팔면체각 **90±13°** (5조건 전부) | 1317 → **815** (**−502, 38 %**; 그중 ~50 은 힘 수렴 실패) | 기하 판정 |
| 2 Convex Hull | **E_hull < 0.2 eV/atom** | 815 → **114** (**−701, 86 %**) | pymatgen `phase_diagram` + **Materials Project** |
| 3 Band Gap | **gap > 0.5 eV** | 114 → **29** (**−85, 75 %**) | relax 고유값 재사용(비용 0) |
| 4 Electrochemical Stability | **ESW > 1 V** | 29 → **14** (**−15**) | **GPPD**(μ_Li/Na/Mg 스윕) |
| 5 **Surrogate NEB (S-NEB)** | **E‡_S 하위 10** | 14 → **10** (**−4**) | CHGCAR NEB + SCF 2회 |
| 6 CI-NEB | (검증층) | 10 → 10 | ASE CI-NEB + FIRE |

⚠ **도형과 본문의 어긋남 1건**: 도형은 S-NEB 가 **14** 를 받는다고 그리는데, 벤치마크는 **ESW 단에 *진입한* 29 중 28**(`Li₃PHg` 제외 — CI-NEB 중 Hg 클러스터 형성)에 대해 돌렸다. 즉 **벤치마크 비용이 깔때기 그림에 없다.**

**J-39-c. ★① 우리 cascade 와의 단별 대조 — 겹침 / 그들만 / 우리만**

우리 정본: `tools/cascade/build_screening_funnel.py` + `db/properties/cascade_screening_funnel_v2.json`(waterfall **89 → 89 → 84 → 45 → 28 → 1**) + `tools/oxidation/esw_cascade_batch.py` + `db/properties/oxidation_stability_cascade_v3_pinned.json`.

| | 축 | [Sjolin23AP] | 우리 | 판정 |
|---|---|---|---|---|
| 🔵 겹침 1 | 열역학 안정성 | **E_hull < 0.2 eV/at** (절대·MP·pymatgen) → 86 % 제거 | **G1** `Δe = E(doped)−E(host) < 0` (host 상대·UMA) → **89/89 통과 = `vacuous`** | ⚠ 같은 질문, 다른 좌표계. **그들 게이트는 일하고 우리 것은 안 한다**(우리 JSON 이 자백) |
| 🔵 겹침 2 | **grand-potential ESW** | GPPD, hull 위 μ 구간, 컷 1 V | **G2/G3**(같은 `get_element_profile` 계보, Zhu 2015 공유), 컷 window>0.05 V · ox≥2.14 V | ✅ 가계 동일. ⭐ **우리가 앞서는 점**: `phase_set_id` 해시로 경쟁상 집합 고정 — **이 편엔 MP 스냅샷 버전조차 없다** |
| 🟠 그들만 1 | **밴드갭 게이트** (>0.5 eV) | **114→29, 75 % 제거 = hull 다음 2위 필터** | ❌ 우리는 `electronic_insulation_diagnostic` = **`DIAGNOSTIC_ONLY — 게이트 아님`** (89종 전수 갭 없음 + 문헌 `gap_lit_eV` 를 게이트로 쓰면 큐레이션이 결과를 만듦) | 🔴 **없어서 안 하는 것이지 안 해도 돼서 안 하는 것이 아니다** |
| 🟠 그들만 2 | **대리 NEB → CI-NEB 2층 + 오차예산 공표** | MAE **73** / SD **96** meV / MRE **20 %** / parity 산점도(`Fig. 6`) / 실패 유형 분해(`Fig. 7`·`Fig. 8`) / **10–30×** | ❌ 우리 **G4 = BVSE 프록시 단독**, `arbitrariness_flag: true`, **어떤 기준에도 대 본 적 없음** | 🔴🔴 **이 논문이 우리를 이기는 유일한 칸** |
| 🟢 우리만 1 | **기계 G5** (E ≤ 48.2 GPa AND G/B ≤ 0.77) | ❌ 0건 | 28 → **1**(`WO₃`) = 최강 단 | ⭐ 우리 JSON 의 *"문헌 대응 없음(Xiao·Sendek 미시행, Kahle 명시 배제)"* 목록에 **네 번째 사례 추가** |
| 🟢 우리만 2 | **유한온도 MLIP-MD** (D·Ea·σ) | ❌ 전 계산 0 K | UMA-s-1p1 · 600/800/1000 K | ⭐ **범주 자체가 다르다** |
| 🟢 우리만 3 | **무질서 앙상블** | ❌ 개념 0(`disorder` 0회) — 단 그들 계는 **완전질서**라 원리상 불필요 | SQS/배열 앙상블 + 멀티시드 | ⚠ **면제이지 우월이 아니다.** 단 그들이 자인하듯 *"실제 쓰이는 조성 = 공공 있는 조성"* 이고 **그 문턱 앞에서 멈췄다** |

👉 **선점 판정 (한 문장)**: **선점되지 않았다** — 물체(정비화학량 신조성 열거 ↔ 고정 host 도핑)·수송엔진(0 K 단일 hop CI-NEB ↔ 유한온도 MLIP-MD)·축 구성(기계·무질서 0 ↔ 우리 G5+앙상블)이 전부 다르고, 겹치는 것은 *"다단 게이트 + grand-potential ESW"* 라는 **설계 관용구**뿐인데 그 관용구의 원전은 이 편이 아니라 **Zhu 2015 / Xiao 2019 / Sendek 2017** 이고 우리 funnel JSON 이 이미 그 셋을 `literature_analog` 로 인용한다. **다만 "싼 수송 대리자의 오차예산" 한 칸은 그들이 갖고 우리는 비어 있다.**

**J-39-d. ★③ MD 규약 한 줄 대조** (판정 아님 — 나란히만)

🔴 **먼저: 이 논문에는 MD 가 없다.** 왼쪽 열이 거의 전부 "없음" 인 것이 대조의 결론이다.

| 항목 | [Sjolin23AP] | 우리 (comp1/modelc/lpsocl) |
|---|---|---|
| AIMD vs MLIP | **둘 다 아님** (`AIMD` 1회 = 서론에서 "대안" 으로 이름만) | **MLIP-MD** UMA-s-1p1(omat) |
| 셀 / 원자수 | 단위격자 **5원자** · 장벽용 **2×2×2 = 40원자**(공공 1 → **39**) | box331 **558원자** |
| 온도 목록 | ❌ **전부 0 K** | **600 / 800 / 1000 K** |
| 온도당 시간 | ❌ 없음 | equilib 5 ps / prod **200 ps** |
| 앙상블·dt·thermostat | ❌ 없음 | **Langevin NVT** · dt **2 fs** · friction 0.02 |
| **MSD 적합 창** | ❌ 없음 (`MSD` 0회) | **2–50 ps 고정** |
| **절편 자유 여부** | ❌ 해당 없음 | **자유절편 D** |
| 다중원점 | ❌ 해당 없음 | 사용 |
| **Haven 처리** | ❌ `Haven`·`Nernst` **0회** — 환산 자체를 안 한다 | **NE, H_R = 1 명시 가정** |
| **아레니우스 점 개수** | ❌ **0점** | **3점** |
| 오차막대 | 동역학 해당 없음 / **장벽은 MAE·SD·MRE 로 공표** | 멀티시드(modelc 3-seed Ea 0.197±0.032) |
| 보고량 | **E‡ [meV]** = 0 K 단일 hop 안장점 | **MSD → D → σ(NE)**, Ea |

⇒ **겹치는 온도 0개 · 겹치는 보고량 0개** ⇒ 동역학 수치를 나란히 놓을 자리가 **존재하지 않는다**.

**J-39-e. ★⑤ ESW 조작적 정의 — 외부 관례 표본 (§J-38 보강)**

활자 그대로: *"Determination of the ESW can be achieved using **Grand Potential Phase Diagrams** … **The range of potentials, where the compound lies on the convex hull for that electrochemical potential range, is the ESW of the compound.**"* (기준쌍 Li/Li⁺ · Na/Na⁺ · Mg/Mg²⁺)

✅ **"hull 위에 머무는 μ 구간"** = 우리 언어의 **`evolution == 0` 구간** = `ocv_self_decomposition_V → oxidation_limit_V`
⇒ **`HZ-esw-reduction-limit-label` 의 `fix` 를 지지하는 외부 표본 3번째** (앞선 둘: `[Schw21]` 1.72/2.01 · `[Nolan18]` p.2022 정의 문장). **이 편에는 `max(V | evolution>0)` 류의 관례가 없다.**

⚠ 그러나 **그대로 못 쓰는 이유 3**:
1. **폭만 싣는다** — `Table 2` 의 `ESW [V]` 는 폭이다. `Li₃OCl` 2.86 V 가 0→2.86 인지 1.4→4.26 인지 **논문만으로 알 수 없다** ⇒ 우리 상·하한 라벨에 **직접 대응 불가**.
2. **두 겹으로 넓혔다**: ⓐ *"알칼리 금속 산화물로의 분해는 동역학적으로 억제되므로 **제외**했다 … 제외하면 **더 넓은 ESW**"* ⓑ *"물질이 hull 위에 있어야 하므로 **DFT 에너지를 E_hull 만큼 인위적으로 낮춘다(소수 2자리 올림)** … 따라서 여기 GPPD 는 일반적으로 **준안정 상도**"* — `Li₃SI` 은 **0.20 eV/at** 을 내렸다. **준안정도가 클수록 더 유리해지는 방향**이다 🔴
3. **그러고도 실험의 1/4**: `Li₃SI` 계산 **2.52 V** vs 실험 **10 V** [ref 62]. 저자 설명은 *"GPPD 는 순수 열역학이라 동역학적 억제를 못 담는다"*.

⭐ **우리에게 남는 질문**(§J-39-h-4): 우리 `esw_cascade_batch.py` 는 **이 조작 ⓑ 를 하지 않는다**. 도핑 조성 다수가 hull 위에 없을 텐데 — **그때 pymatgen 이 무엇을 돌려주는지 확인한 적이 있나?** 이 편은 그 문제를 만나 **명시적 조작으로 해결**했다. 우리는 **만났거나, 조용히 지나쳤다.**

**J-39-f. 🔗 `[Ziemke26AP]` 와의 충돌 3건** (같은 `Li₃OCl`, §J-7)

| # | 충돌 | [Sjolin23AP] | [Ziemke26AP] | 판정 |
|---|---|---|---|---|
| 1 | **host 가 얼마나 안정한가** | **E_hull = 0.145 eV/atom** (자기 컷 0.2 의 73 % 지점) | **hull 0건** — pristine 을 문제없는 host 로 놓고 **33 % 치환**을 얹는다 | ⭐ **[Sjolin23AP] 이 이긴다**(심사 통과·MP 상도 명시·값 존재) ⇒ ziemke 의 *"안정한 host 에 결함"* 서술이 **더 약해진다** |
| 2 | **Li 이동장벽** | **CI-NEB 380 meV**(2×2×2 공공 매개) · S-NEB 424 | **NEB 0건** — 스스로 *"needed"* | ⭐ ziemke 가 비워둔 칸이 **채워진다**. ⛔ 우리 db 이식은 여전히 금지 |
| 3 | **Li 자리 (3c vs 3d)** | `Fig. 1` 실독 = **면심 3c**, X₆B 팔면체 (A 원점 기준) | 본문 3d ↔ 자기 `Fig. 1` 3c 로 **자기모순**(ziemke digest §10-E) | ⭐ **ziemke digest §10-E 판정이 외부에서 지지된다** (⚠ 원점 선택 단서 필요) |

**J-39-g. 🔴 우리에게 불리한 결론 (별도로 센다)**

1. **우리 G4 에는 오차예산이 없다.** 그들은 MAE/SD/MRE/parity/ρ/실패유형을 전부 공표한다. 우리 `ionic_transport norm` 은 ⓐ 정본 softBV 가 아닌 **Adams-2003 파라미터** ⓑ `blocking<0.6` **상속 상수**가 G4 탈락 36종 중 **31종을 혼자 죽임** ⓒ `arbitrariness_flag: true` ⓓ **검증 0건**.
2. **전자 절연 게이트 부재** — 그들에겐 **2위로 강한 필터**(75 %)다.
3. **S-NEB 를 우리 계에 그대로 못 쓴다** — 그들 실측 **B-자리 P 실패율 76 %(전체 최악)**, 우리 host 골격 중심은 **PS₄³⁻ 의 P**.
4. **"스크리닝이 새 물질을 준다" 의 직접 반례** — 1317종·6단의 산물이 **이미 알려진 14종**. 우리가 쓸 수 있는 서술은 *"체계적 **재발견** + 순위"* 까지.
5. **G1 공허함이 외부 숫자 옆에서 더 선명해진다** (그들 hull 86 % ↔ 우리 89/89).
6. **실험 앵커를 세어 본 적이 없다** — 그들은 *"2점뿐"* 이라고 **스스로 적는다**.

**J-39-h. ⭐ 우리가 가져갈 것 (수치 0건, 전부 규율)**

1. ⭐⭐⭐ **싼 대리자에는 오차예산을 붙인다** — 최소형: 기존 MLIP-MD 챔피언 D 몇 종에 `bvs_li_proxy_score` 를 대고 **순위상관 하나만** 내도 지금보다 낫다. ⚠ **보고량 카드 먼저**(기준을 D 로 할지 Ea 로 할지 채널% 로 할지를 **결과 보기 전에**).
2. ⭐⭐ **"전하밀도 한 번 → 모든 경로 재사용"**(저자 결론) 이 **우리 무질서 앙상블과 맞물린다** — 배열 N 개에 SCF N 회로 배열 안 모든 hop 을 훑는 **정적 축**. ⚠ 먼저 `Fig. 8` 식 **닫힌고리 검사**를 우리 `Li₆PS₅Cl` CHGCAR(LOBSTER SCF 산출물, **이미 있다**)로 — **계산비 사실상 0 인 시험**이다.
3. ⭐ **깔때기를 그림 한 장으로**(`Fig. 3` 양식: 진입수 굵게 + 탈락수 빨강). 우리 `waterfall`(89/89/84/45/28/1)이 이미 그 데이터. ⛔ **`pool_provenance` 한 줄(*"큐레이션 풀 · 발견 깔때기 아님"*)을 그림에 박는다**.
4. ⭐ **문턱을 "어느 오류를 줄이려는 선택" 인지 선언한다** — 그들은 *"덜 제한적 기준으로 **위음성**을 줄인다"* 고 명시. 우리 `threshold_sensitivity` 에는 **방향 선언이 없다**.
5. **셀이 바뀌면 k-격자를 바꾼다**(7×7×7 → 4×4×4) — `[Ziemke26AP]` T3 규율의 **양성 사례 1건**.
6. **탈락자의 화학을 한 문단으로 해부한다** (그들: *"전하중성 불가가 최대 원인 · 통과자는 16·17족 조합"*). 우리는 *"왜 염화물이 0/19 냐"* 에 CSV 되읽기 말고 답이 없었다.

**J-39-i. ⛔ 이 논문을 인용할 때 반드시 같이 다는 단서 5개**

① **기준이 내부 이미지 1개짜리 CI-NEB** (Mg 만 3개) ⇒ *"73 meV = 정확한 장벽"* 으로 옮기면 안 된다 — **또 하나의 싼 근사 대비 오차**다.
② **`w_S = 0.470` 은 in-sample** (28종에서 적합, 28종에서 평가, held-out 0). 🟢 단 **랭킹 결론은 w 와 무관**하므로 *"top 10 집합 일치"* 는 유효하다.
③ **"같은 top 10" 은 집합에 대해 참, 순서에 대해 거짓** — ✎ 우리 재계산: **ρ = 0.925**, **최대 이동 5칸이 하필 CI-NEB 1위 `Li₃SI`(→6위)**.
④ **본문이 `Fig. 7` 을 잘못 센다** — *"the 4 outliers"* 인데 **라벨은 6개**. ✎ figure-read 로 해소: 실패 4 = `Mg₃CTe`·`Mg₃CSe`·`Na₃PCd`·`Na₃PHg`(전부 B-자리 C/P), 나머지 2(`Li₃SI`·`Na₃SI`)는 **ASD 최대(0.25·0.36 Å)의 구조 재조직 이탈점**.
⑤ **보고량 3층 미선언** — **스핀 0줄**(`spin`·`ISPIN`·`+U` **0회**인데 A-자리에 전이금속 전열이 있고, **701종 hull 탈락이 그 계산 위에 선다**) · **경로 선택 규칙 0**(구조검사 허용오차 ±2°/±13°/0.5 Å 라 통과 구조는 정확한 Pm-3m 이 아니며 hop 이 갈라진다) · **완화 basin 단일 시드**(rattle σ 0.01 Å). 무질서 축은 **구조적으로 면제**(정비화학량 완전질서)이지 우월이 아니다.
```

---

## ④ 원장 정정 제안 (문구만 — **이 세션은 `db/` 를 건드리지 않았다**)

### ④-1. `db/properties/citation_hazards.json` → `HZ-esw-reduction-limit-label` 의 `관련` 배열에 한 줄

> 제안 문구 (추가만, 기존 항목 유지):
> `"litdb/papers/sjolin2023_accelerated_workflow_antiperovskite_sse.md §4d — 외부 관례 표본 3번째. GPPD ESW 를 '화합물이 hull 위에 있는 μ 구간' 으로 정의(활자 그대로). 우리 fix 방향(evolution==0 구간)을 지지한다. ⚠ 단 이 편은 폭만 싣고 상·하한이 0이라 라벨 자체의 대응은 안 된다."`

**왜 제안만인가**: 이 세션의 권한이 `litdb/papers/` + 대기파일 둘뿐이다. 그리고 이 해저드는 **level BLOCKED** 라 손대는 것 자체가 1저자 결정 사항이다(원장 `fix` 에 *"조용히 고치지 않는다"* 가 박혀 있다).

### ④-2. `db/properties/cascade_screening_funnel*.json` → `gates[G4].literature_analog` 에 논문 1건 추가 제안

현재 `papers: ["xiao2019_cathode_coating_screening (Filter 6, CI-NEB E_m)", "kahle2020_ht_aimd_screening (pinball D(1000 K) 상위 200 → FPMD 132)"]`.

> 제안 추가: `"sjolin2023_accelerated_workflow_antiperovskite_sse (S-NEB top-10 랭킹 컷 + CI-NEB 검증층)"`
> 그리고 `mapping` 에 한 줄 보강 제안:
> `"⚠ 세 편 중 [Sjolin23AP] 만 대리자의 오차예산을 공표한다(MAE 73 / SD 96 meV / MRE 20 % / ρ 0.925 / parity 산점도 / 실패유형 분해). 우리 BVSE 프록시에는 그에 해당하는 수치가 0건이고 arbitrariness_flag=true 다 — 이것이 현재 G4 의 가장 큰 공백이다."`

⚠ **이건 게이트 값을 바꾸지 않는다** — 메타데이터만. 그래도 `db/` 이므로 **제안으로만** 남긴다.

### ④-3. ⚠ 그림 폴더가 **두 벌** 이다 (병합자가 구 폴더 정리)

**실측 경위 (2026-09-22, 이 세션):**
- 세션 시작 시점엔 **`litbd/figures/accelerated_workflow_antiperovskite_sse/`**(파일명 유래 slug)만 있었고, `_sources.json` 에도 그 키만 있었다. 그래서 규약 slug 로 `extract_figures.py --slug sjolin2023_… --pdf …`(⛔ `--clean` 안 씀)를 돌렸다.
- **그런데 그 사이 동시 세션의 커밋 `5d049f5d4`(schwietert2021 병합)가 `litdb/figures/sjolin2023_accelerated_workflow_antiperovskite_sse/` 11파일을 이미 넣어 두었다.**
- ✅ **충돌 없음**: 내 재추출 결과가 **바이트 동일**이었다 — `git hash-object litdb/figures/_sources.json` == `git rev-parse HEAD:…` (같은 blob), 그리고 `git status` 에 **그림 관련 변경 0건**. 즉 **이 세션은 그림 트리를 실질적으로 안 건드렸다**. (교차검증: `fig_3`·`fig_6`·`fig_7`·`tab_2` md5 가 구·신 폴더에서 동일.)
- 👉 **병합자 조치 (남은 일 하나)**: **구 폴더 `litdb/figures/accelerated_workflow_antiperovskite_sse/` 삭제 + `_sources.json` 에서 그 키 제거.** webapp `data.paper_figures(pid)` 는 **digest slug 로만** 폴더를 찾으므로(`webapp/data.py:6302`) 구 폴더는 **어떤 화면에도 안 걸리는 고아**이고, `papers_with_figures()` / 검색 색인 맵에만 **유령 항목**으로 남는다.
- ⛔ 이 세션은 삭제를 **하지 않았다** — 동시에 도는 에이전트가 참조 중일 수 있고, 내 권한 밖이다.

---

## ⑤ 병합 체크리스트

- [ ] `INDEX.md` — ① 행 추가 (`✅ Digest 완료` **또는** `⚠ EXTERNAL`. 열 머리 확인 후 3열 문구 조정)
- [ ] `comparison_vs_ours.md` `📑 Reference key` — ② `[Sjolin23AP]` 행 추가 (4열)
- [ ] `comparison_vs_ours.md` — ③ **§J-39** 블록을 **J-38 뒤 · `## K.` 앞**에 삽입 (⚠ 선점 시 번호만 교체)
- [ ] **A–D 물성 4축 표에는 행을 만들지 않는다** (명시적 판정)
- [ ] `properties/<prop>.md` — **해당 없음** (이식 가능한 물성값 0건)
- [ ] 🎤 talk 역링크 — **해당 없음** (`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md` 하나뿐이고 **이 논문은 그 대기열에 없다**. antiperovskite·Sjølin·S-NEB·Li₃OCl 전부 `litdb/talks/` 에서 **0 hit**)
- [ ] ④-1·④-2 원장 제안을 1저자에게 전달 (BLOCKED 해저드 + cascade 메타)
- [ ] ④-3 구 그림 폴더(`accelerated_workflow_antiperovskite_sse/`) 삭제 + `_sources.json` 키 제거
- [ ] ⚠ **열 밀림 주의** — 커밋 `5d049f5d4` 가 경고한 함정(칸 수가 같아 `--check` 가 못 잡는다). 이 파일의 ① 은 **3칸**(`slug|논문|축` *또는* `slug|논문|보관 이유`), ② 는 **4칸**(`약칭|논문|digest/status|유형`) 으로 **실제 헤더를 읽고** 맞췄다. 넣는 절의 머리를 **한 번 더** 확인할 것
- [ ] ⚠ `test_recent_digests_are_on_every_litdb_surface` — 이 digest 가 병합 전까지 **새 블로커**다 (`5d049f5d4` 시점 남은 블로커는 `lomeli2024` 하나였다)
- [ ] 병합 후 이 대기파일 삭제
