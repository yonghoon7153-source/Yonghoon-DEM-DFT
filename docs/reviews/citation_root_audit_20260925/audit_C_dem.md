# 감사 C — DEM · 접촉역학 · 네트워크/퍼콜레이션 · 패킹 · 압밀 인용 (2026-09-25)

> ⛔ **기록 사본** — 2026-09-25 읽기 전용 감사 에이전트 보고 원문 (scratchpad → 리포 이전 09-26).  판정의 정본은 원장 `docs/reviews/claims.json` (`CL-90` · `CL-91`) 과 `findings.json` `SELF-51` 이다.  인용 금지 등록부의 문자열은 `⟦CL-xx …⟧` 로 바꿔 적었다.  file:line 은 감사 기준 커밋 기준이라 지금 줄 번호와 다를 수 있다.  종합 = `docs/reviews/citation_root_audit_20260925.md`.


**범위** — 배정 키 34개 (Holm 1967 … Hu 2018, 전부 아래 표에 행이 있다) 와, 같은 사슬 안에서 드러난 인접 인용 (Henkes 2005 · Scher–Zallen 1970 ·
Storåkers 2000 · Doux 2020 / Sakuda 2013 의 압밀 수치 · Cronau 겹침 · Lawn 1998 전도 · "Alabdali 2022 MethodsX" ·
refs.bib `@Minnmann2021`).
**방법** — `cite_occ.tsv` 의 해당 키 556 행과 리포 전수 grep (`docs/data/audit_*`, `litdb*` 제외) 으로 (인용 → 값/주장)
쌍을 묶었다 → 정본 카드 (`origin/claude/friendly-meitner-lldvar:litdb/papers/`, fetch 없이) 와 대조 → 카드가 없으면 웹 검색으로
존재만 확인 → M/F 와 수치가 붙은 B 는 `git log -S` 로 최초 커밋을 찾았다.  리포는 읽기만 했다.
**판정 기호** — 지시서 그대로 V/M/B/F/C/U.  보조 표기: **⚠** = 의심이 강함 · *검색 요약* = 웹 검색 결과 요약에만 나온 값
(미확인, V 아님).  "카드" = 정본 litdb 카드.
**전제** — 리포 커밋 3,097 개 중 3,028 개가 작성자 `Claude` 다.  아래 뿌리 커밋도 전부 AI 세션 커밋이라 작성자로는 구분이 안 된다.

---

## 1. 판정표

### A. 순수-SE 압밀 앵커 "porosity 10 % @ 300 MPa" — 출처 다섯 개가 번갈아 붙었다

| # | 인용 | 값 / 주장 | 사용처 (대표 · 건수) | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| A1 | Minnmann et al. | 순수 LPSCl porosity ≈ 10 % @ 300 MPa = **실험** 보정 앵커 (frame[1]) | `CLAUDE.md:445` (frame[1]) · `:1062` · `:1084` · `:1104` · `:1220` · `:1271` · `:1286` · `:1317` · `wiki/concepts/frame4-independent-calibration.md:44` · `docs/pipeline_step1_to_step5_guide.md:262,524,526` · `scripts/mpm_dem_match.py:369,393` · `docs/data/densification_porosity_db.csv:12` · `docs/data/heckel_pure_se_dem.csv:11,16` — **38 줄 / 27 파일** (한 줄에 "Minnmann"·"10 %"·"300" 이 모두 있는 줄만 센 하한) | **M** | `minnmann2021_jes_charge_transport_bottlenecks`: *"⚠ 이 논문은 pure-SE porosity를 별도 측정하지 않는다 — 14 %는 복합 양극 값이다"*, *"'pure-SE 10 % @300 MPa' = 우리 MPM 3D(σ_y 0.30) 수렴값"*. `minnmann2022_…`: *"이 논문엔 porosity 숫자가 단 하나도 없다"*. `minnmann2024_…`: 380 MPa 단일, SE = Li₃PS₄–LiI | `2d0ce2a61` 2026-06-07 (CLAUDE.md frame[1]). 선행 귀속은 A3·A4·A5 |
| A2 | **[9]** "T. Minnmann et al., *Adv. Energy Mater.* 2022, 12, 2201425" (원고 참고문헌) | 원고 Methods: "~10 % target … and the 11–12 % contact overlap … ^[9]^" | `docs/manuscript_draft/build.js:146–148`, 목록 `:270` | **M** (+ 저자 이니셜 오기: 카드·refs.bib 은 **P.** Minnmann) | `minnmann2022_…` §0 표: *"(a) ~10 % pure-SE / 13–17 % composite 가 이 2022 Perspective 안에 있다 — ✗ 아님"*. 11–12 % 겹침은 문장 자신이 "simulation consistency result" 라 적는다 → [9] 가 받칠 내용이 없다 | `c2670de6e` 2026-08-23 ("T. Minnmann", 11–12 % 문장); 현 문장형 `d45576e2a` 2026-08-29 |
| A3 | Doux 2020 | 순수-SE ~10 % @ 300 MPa; "Doux curve 5–15 % over 250–400 MPa" (그림에 회색 밴드로 그림) | `docs/References_and_Methodology.md:270` ("논문 표현" 문안) · `scripts/cap_compaction_heckel.py:17,30,36,79,91` — 5 줄 / 4 파일 | **M** | `doux2020_stack_pressure_assb`: *"펠릿이 18 % porosity (370 MPa cold-press 후에도 잔류)"*, *"분말 200 mg → 13 mm PEEK die → 370 MPa"* | `660600a44` 2026-04-24 (import — 리포 이전부터) → `4706f7665` 2026-06-07 (cap 스크립트) |
| A4 | Sakuda 2013 (+ Tran 2025) | "Pure LPSCl @ 300 MPa → ε ≈ 10 % (EXPERIMENTAL)"; **3 분 전** 커밋은 반대로 "Sakuda 2013: ~25 % at 360 MPa", "DEM 의 10 % 는 인공 보정" | `scripts/predict_porosity_real_physics.py:5–7,47–48` | **M** (Sakuda) · **U** (Tran 2025 — 서지 미식별, 카드 없음, 검색 미발견) | `sakuda2013_sulfide_mechanical_property`: *"'87 % 상대밀도 @ 300 MPa'는 이 논문 본문에 stated 되어 있지 않다 … 본문이 명시하는 밀도 앵커는 'exceeds 90 % at over 350 MPa' 뿐"*; 소재는 75Li₂S·25P₂S₅ **유리** (LPSCl 아님). 25 % @ 360 도 10 % @ 300 도 카드와 다르다 | `4dd66f772` 2026-05-13 01:17 UTC ("~25 %") → `97cc1eac0` 01:20 UTC ("Crucial correction from user feedback: … 10% … EXPERIMENTAL (Sakuda 2013, Tran 2025)") |
| A5 | "user's lab measurement" | ε_pure_SE = 0.10 @ 300 MPa | `scripts/predict_porosity_strict_physics.py:4–6` | **U** | 리포에 원자료 없음. 커밋 메시지: *"Only one fitted value: ε_pure_SE = 10% (user's lab measurement)"* | `288d7b27c` 2026-05-13 |
| A6 | Minnmann 2021 JES 040537 | 380 MPa 압밀 · 복합 porosity 14 % (13–17 %) · σ_ion,eff 0.17 mS/cm @ 42 vol% CAM · τ_ion 2.07 | "380 MPa" 13 회 등 다수 (`fit_constrained.py:21`, `plot_tau_regime_si.py:135`, `se_material.py:49` …) | **V** | 카드 §0 표: *"dry mixing + 단축 380 MPa 압밀, Table SIII"*, *"0.17 mS/cm (= 1.7×10⁻⁴ S/cm) 42 vol% NCM-622"* | — |

⇒ **"10 % @ 300 MPa" 를 수치로 가진 정본 카드는 하나도 없다.**  05-13 한 세션의 36 분 사이 (01:17 → 01:53 UTC) 에 이 값은
"DEM 의 인공 보정 산물" → "Sakuda 2013·Tran 2025 의 실험값" → "사용자 실험실 측정" 의 세 지위를 거쳤다.  그 앞에는 import 문안의
Doux 2020 이, 뒤에는 Doux 2020 (06-07 cap 스크립트) · Minnmann et al. (06-07 CLAUDE.md) · [9] Minnmann 2022 (08-23 원고) 가 붙었다.
⚠ 이 항목은 2026-09-09 잔여 감사 (`docs/data/audit_20260909/residual_followups.json`, P0 `provenance_missing`) 가 이미
잡았지만 **`findings.json` 원장에는 등재되지 않았고** `CLAUDE.md:445` 는 그대로다.

### B. DEM 겹침·연화의 "문헌 관행"

| # | 인용 | 값 / 주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| B1 | Wang 2023, "J. Power Sources 555" (제목·쪽 없음) | 문헌 DEM 최대 δ/R **0.05–0.15** (relaxation 포함) | `scripts/build_literature_reference.py:19,83` (→ `docs/figures/physics_regime/literature_brittle_reference.csv`) · `docs/paper_brittle_caveat.md:44,87,135,302,777,852` | **F** (추정) | 카드 없음. 웹 검색 3 회 (저자+연도+권, 권+DEM 압밀) 모두 미발견. 선행 감사 `gap_audit_r3_repair_20260917.md` ⓔ 도 *"litdb 정본 274 편에 wang2023\* 카드 없음"* | `0a040f2b0` 2026-04-29 — **날조된 "Wang 2020, JPS 470" 과 같은 날, 같은 파일** |
| B2 | Wang 2023 | 70 % / 80 % CAM 점 (φ 0.26, τ² 7.78) · (0.16, 17.24) | `scripts/compare_hertzian_vs_physics.py:114`, `build_tau_regime_db.py:224`, `plot_tau_regime_si.py:116` (현재 주석으로 보존) — B1 과 합쳐 20 줄 / 8 파일 | **F** (추정) | 위와 같음. `GAP3-37` 이 이미 "출처 0 건" 으로 처리 | `660600a44` (import) |
| B3 | Bielefeld 2019 (+ Wang 2023) | "softened E 가 표준 DEM 관행" (E_SE 1.35 GPa 정당화) | `docs/Reviewer_Defence_Notes.md:78,89` | **M** | `bielefeld2019_microstructural_modeling_composite_cathode`: *"DEM 접촉법칙: 없음. 이건 DEM 이 아니라 기하 stochastic-placement 모델"*, *"E_SE (가정) ~25 GPa … 겹침 허용 근거; 수치 안 씀"* — 연화한 E 가 없다. (같은 칸의 Wang 2023 은 B1 과 같은 F) | `148d0f5fb` 2026-05-04 |
| B4 | Bielefeld 2020, "J. Electrochem. Soc." | relaxation 포함 DEM, 최대 겹침 5 % · "explicit cap of 0.05" | `build_literature_reference.py:18,87` · `paper_brittle_caveat.md:44–45,87,135,302,777,852` | **M** (학술지도 틀림) | `bielefeld2020_effective_ionic_conductivity_binder`: 제목 줄 *"(ACS Appl. Mater. Interfaces 12, 12821−12833)"*, *"미세구조 생성 알고리즘은 2019 그대로"* = stochastic placement (DEM·겹침 cap 없음) | `0a040f2b0` / `750e23b7d` 2026-04-29 |
| B5 | Minnmann 2021, "Adv. Energy Mater. 11" | relaxation 포함 DEM, 최대 겹침 0.08 (0.06–0.10) | `build_literature_reference.py:20,91` · `paper_brittle_caveat.md:44,87` | **M** | 카드: *"type experiment (EIS-TLM + cell cycling) · 저널 J. Electrochem. Soc. 168 (2021) 040537"* | `0a040f2b0` 2026-04-29 |
| B6 | Cronau (2021/"2022") | "Cronau 380 MPa 문헌 overlap floor 5–10 %", 순수-SE 겹침 11–12 % 가 "Cronau 소성 바닥" 을 재현 | `webapp/templates/single.html:21` (배지 툴팁) · `webapp/app.py:9077` · `CLAUDE.md:974–978,1003,1028` · `wiki/concepts/ese-softening-18x.md:26` — 21 줄 / 14 파일 | **M** | `cronau2021_stack_pressure_ionic_conductivity`: type experiment (적층압 vs σ_ion), 겹침 항목 없음; 카드 §9 는 제작압을 *"400–500 MPa"* 로 적는다 (380 아님) | `a58e1b7c9` 2026-06-03 (툴팁) → `1eb6f6500` 2026-06-06 (CLAUDE.md) |
| B7 | So et al. 2022 | "그들도 sim-vs-real E 를 구분 사용" | `Reviewer_Defence_Notes.md:95` | **M** | `so2022_dem_contact_model_assb_compaction_sintering`: *"E_SE (LPS) 24 GPa · Sakuda [4] · stated (Table 1)"*; `so2021_dem_fabrication_…`: *"연화 안 함 — real E 그대로"* | `148d0f5fb` 2026-05-04 |
| B8 | "Alabdali, Zanotto et al. (2022) *MethodsX* 9, 101861 — Contact model for DEM simulation of compaction and sintering of ASSB electrodes" | 구형 겹침이 접촉면적 과소평가 (논문 문안) | `docs/References_and_Methodology.md:227,270` | **M** (서지 혼합) | `so2022_dem_contact_model_…`: 저자 *So, Inoue, Park, Nunoshita, Ishikawa, Tsuge*, *"MethodsX 9 (2022) 101857"*, 주제 = ASSB 압밀·소결 DEM 접촉모델. `alabdali2023_cgmd_…` = DOI 10.1016/j.jpowsour.2023.233427 (CGMD, LAMMPS) → 주제는 So 논문, 저자명은 Alabdali, 기사번호는 둘 다와 다르다 | `660600a44` (import) |

### C. 접촉 체제 (Holm · Tabor · Brake · Greenwood · Storåkers · Thornton)

| # | 인용 | 값 / 주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| C1 | Holm 1967 (*Electric Contacts*, 4판) | 협착저항 R = 1/(2σa); 전도 ∝ √A (지수 ½) | 62 회 / 29 파일 (`network_conductivity.py:8,24,407`, `generate_fitting_report.py`, CLAUDE.md σ 폼 절) | **C** | 고전 식. `bazzoun2026_dem_fem_rnm_ionic`: *"R^IJ=1/(2σ·r_c) (eq 8) = Holm 1967 그대로"*. √A·cov^½ 지수는 그 식에서 우리가 유도한 것 (Holm 의 "수치" 아님) | — |
| C2 | Tabor 1951 (*The Hardness of Metals*) · Tabor 1948 | H ≈ 3σ_y; "metal 부터 ceramic 까지 universal" | `Tabor_framework_reference.md:191`, `Reviewer_Defence_Notes.md:57`, `refs.bib` Tabor1948 | **C** | 고전 관계. `kogutetsion2002_ep_sphere_rigid_flat`: *"H = 2.8·Y (Bhushan ref18 = Tabor)"*; `jacksongreen2005_…`: Tabor 상수를 *"이 논문이 반증 — 변형따라 변함"*. ⇒ "ceramic 까지 universal" 은 과장. ⚠ 문서의 `A_Tabor = F/(π·H)` (`Tabor_framework_reference.md:75`, `paper_brittle_caveat.md:2278,2321`) 는 Tabor 관계(A = F/H)·코드 (`network_conductivity.py:309` "A_tabor (F/H)") 와 다르다 — 인용이 아닌 전사 오류 | — |
| C3 | "Tabor (1951) regime boundaries (per Brake 2012, Greenwood 1992)" | μ_T = E*a/(σ_y R): **< 0.1 탄성 · 0.1–100 전이 · ≥ 100 완전소성**, "Brake 의 전이 밴드 [0.1, 100]" | `scripts/analyze_tabor_regime.py:7–10,83–85` · `Tabor_framework_reference.md:55,59–65` · `paper_brittle_caveat.md:2283–2296` (원고용 문단) — 14 줄 / 4 파일 | **B** ⚠ (Brake 실재, 경계값 미확인) — 정본과 불일치 | Brake 2012 = *IJSS* 49(22) 3129–3141, DOI 10.1016/j.ijsolstr.2012.06.013, 탄성 / 혼합 / 완전소성 3 영역 (*검색 요약*). 정본 `mesarovicfleck2000_…`: *"평균압 첫 항복 p_m ≈ 1.1 σ_y"*, *"완전소성 plateau 진입 aE*/R₀σ₀ ≳ 50 (m=∞) / ~100 (m=3)"* — Hertz 로 환산하면 첫 항복은 aE*/(Rσ_y) ≈ 2.6 (계산) 이라 **하한 0.1 은 정본과 모순** | `23d35991a` 2026-05-04 |
| C4 | Brake 2012 | H/σ_y = **2.8** = "Engineering ceramics, ASSB context 표준", "Sulfide ASSB 분석 표준" | `Reviewer_Defence_Notes.md:58,61,298` · `Tabor_framework_reference.md:112–114` · `paper_brittle_caveat.md:2287,2330` | **B** ⚠ | 2012 년 IJSS 의 일반 탄소성 구 접촉모델 (*검색 요약*) → "ASSB 맥락 표준" 은 시기·주제상 성립하기 어렵다. 2.8 이라는 숫자 자체는 정본으로 받쳐진다 (§3) | `148d0f5fb` / `23d35991a` 2026-05-04 |
| C5 | Greenwood 1992, "Trans. ASME J. Tribol. 114: 134" | 전이 영역 처리 · C3 경계의 공동 출처 | `Tabor_framework_reference.md:59,206,272` · `analyze_tabor_regime.py:7,83` — 5 줄 / 2 파일 | **F** (추정) | 카드 없음. 웹 검색 2 회 (저자+저널+권, 저자+권+쪽) 결과에 해당 논문이 나오지 않았다 (J. Tribol. 114 권의 다른 논문들만 — *검색 요약*). 리포 표기에 제목도 없다 | `23d35991a` 2026-05-04 |
| C6 | Storåkers et al. 1997, "J. Mech. Phys. Solids 45: 1421 — viscoplastic spheres" | 서지 | `Tabor_framework_reference.md:271` · `paper_brittle_caveat.md:2355` | **M** (서지) | `storakers1997_similarity_inelastic_contact`: *"Int. J. Solids Struct. 34(24) 3061–3083 (1997)"*, 주제는 비탄성 접촉의 자기상사 해석 | `23d35991a` 2026-05-04 |
| C7 | Storåkers 1997 | A = 2π·c²·r·h, 이상소성 pile-up c² ≈ 1.4 | `docs/literature_review_dem_mpm_assb.md:193` | **V** | 카드: *"c²(이상소성) ≈ 1.43"*, *"A = 2π·c²(m)·r·h … Martin–Bouvard가 그대로 사용"* | — |
| C8 | So et al. 2022 (MethodsX) | h_eq 는 "Storakers 1997 viscoplastic spheres 의 simplified form" 이고 우리 Tabor min() 과 "mathematically 동등" | `Tabor_framework_reference.md:228–230,276` · `paper_brittle_caveat.md:2305–2306,2345–2346` | **M** | So 2022 MethodsX 카드 §4.2: h_eq 는 *"Maxwell 점탄성 모델에서 유도한 평형 overlap(h_eq)의 변화율"*; 카드에 Storåkers 언급 없음. "동등" 은 비교한 적 없는 주장 | `23d35991a` 2026-05-04 |
| C9 | Thornton & Ning 1998 (*Powder Technol.* 99: 154) | Hertz → p_y 캡 → 선형 소성 → 잔류겹침 LAW | `Tabor_framework_reference.md:273` · `literature_review_dem_mpm_assb.md:188` | **V** | 카드: *"Powder Technology 99(2) 154–162 (1998)"*, *"Hertz 탄성 → p_y … 선형 소성 분기 → 영구겹침"* | — |
| C10 | Thornton 1997 (*J. Appl. Mech.* 64, 383) | 탄성-완전소성 항복 캡 | `scripts/dem3d_plastic.py:2,701` · refs.bib | **C** | 방법 인용 | — |
| C11 | Greenwood 1966 | 협착저항; Bielefeld 2019 의 ref 36 | `lit_bielefeld2019_…:173`, `lit_bielefeld2020_…:130,495` | **V** | Bielefeld 2019 카드: *"ref 36 = Greenwood 1966, 우리 Holm 1967 과 같은 계보"* | — |
| C12 | Thornton 2015 | "por = 6 % (3:1, 62:38) — SE 소성변형 → extreme packing" | `docs/Packing_Regime_Analysis.md:153` | **B** | 웹: C. Thornton, *Granular Dynamics, Contact Mechanics and Particle System Simulations* (Springer, 2015) 실재. 이 주장은 확인 불가 | `660600a44` (import) |

### D. porosity 예측기의 "문헌 상수" (05-12 ~ 05-15 한 세션)

| # | 인용 | 값 / 주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| D1 | Sridhar & Fleck 2000 (refs.bib 제목 "The multiple state of stress and strain in cold-compacted bimodal powder mixtures") | K_C = 1 + α·f_AM², **α = 2** ("typical", "Fig 7 fit"); 다른 스크립트는 같은 인용으로 **α = 3**; "KC ≈ 1.3–2.7 측정" | `predict_porosity_{final,honest,strict_physics,real_physics,physics,yu_standish}.py` (36 줄 / 10 파일) · `docs/paper/main.tex:564,909` · `refs.bib:203` | **B** (실재) + 제목 **M** | 웹: 실제 제목 *"Yield behaviour of cold compacted composite powders"*, *Acta Mater.* 48(13) 3341–3352. α 는 미확인. 정본 교차: `martinbouvard2003_…` *"구속계수 K_h ≈ 1.3 (20 vol% hard) / 1.8 (40 vol%) … 실험(Table 1)과 정합: 1.3 / 1.7–2.0"* — α = 2 식은 1.08 / 1.32 를 준다 (계산) | `ead2d1f9e` 2026-05-12; bib `144e18b60` 05-13 |
| D2 | Storåkers, Fleck & McMeeking — "Acta Mater. 48 (2000) 4203–4213" (스크립트) / "JMPS 48 (2000) 785–815" (refs.bib) | 경상 골격 f_hard ≈ 0.30–0.35 → f_soft,perc 0.65–0.70 | `predict_porosity_strict_physics.py:20–24` · `refs.bib:223` · `main.tex:569` | **M** (서지 두 벌 다 틀림) + 수치 **B** | 웹: 실제는 *"The viscoplastic compaction of composite powders"*, **JMPS 47 (1999) 785–815**. Acta Mater 48 (2000) 4203 은 검색 미발견 | `4af41f62d` / `144e18b60` 2026-05-13 |
| D3 | Bouvard 2000 | 3 체제 (고립–응집–퍼콜레이션), 경상 골격 전이 ≈ 0.30 | `refs.bib:233` · `strict_physics.py:25–27` | **V** (값) · 학술지 **M** | 카드: *"Powder Technology 111 (2000) 231–239"* (refs.bib 은 "Mechanics of Materials 32"); *"percolation 임계분율 (mono, r=1) f_hard = 0.32"*, Fig 9 3 체제 | `144e18b60` 2026-05-13 |
| D4 | Bouvard 2000 | "SE f_perc ≈ 0.65 (응력-지지 퍼콜레이션)" | `strict_physics.py:170` "Bouvard 2000 (0.65)" · `main.tex:569` | **M** (의미 전환) | 카드의 0.32 는 **경상(hard) 입자의 기하 퍼콜레이션** (*"패킹 수치모사 = 힘 없는 순기하"*); 연상(soft) 응력-지지 임계 서술 없음 | `4af41f62d` 2026-05-13 |
| D5 | "Bouvard 2004, Int. J. Mech. Sci. 46:907" (refs.bib `@Bouvard2004` 는 내용이 Bouvard **2000** PT 논문) | 이성분 RCP "Fig 2 digitized": 최대밀도 f_l ≈ 74 %, 양끝 36 % | `predict_porosity_*.py` (23 줄 / 14 파일) · `refs.bib:167` · `main.tex:560` | **B** (+ 키-내용 불일치) | 웹: Martin & Bouvard, *"Isostatic compaction of bimodal powder mixtures and composites"*, IJMS 46 (2004) — DEM, 크기비 4·8, 대입자 0–80 vol% (*검색 요약*). 코드 배열의 f_l = 0.85–1.00 점은 그 범위 밖 (*검색 요약 기준*). 최적 ≈ 73–74 % 조대는 McGeary 카드로 V (§3) | `ead2d1f9e` 2026-05-12 |
| D6 | Jacobs & Thorpe, "PNAS 106 (2009) 5390–5395", "Generic rigidity percolation in two dimensions" | 강성 퍼콜레이션 ≈ 0.66 (Maxwell 2/3) = f_perc 앵커 | `strict_physics.py:28–30,82,170,222,262` · `refs.bib:243` · `main.tex:570` — 8 줄 / 4 파일 | **M** (서지 날조형) | 웹: 같은 제목은 **Phys. Rev. E 53, 3682 (1996)**; PNAS 106 (2009) 의 강성 퍼콜레이션 논문은 de Souza & Harrowell, 15136–15141. 2D 격자 강성 임계를 3D 복합체 연상 부피분율로 옮긴 것은 범주 이전 | `4af41f62d` 2026-05-13 |
| D7 | Henkes 2005, PRL 95 (refs.bib: Henkes, O'Hern & Chakraborty, "Entropy and temperature of a static granular assembly…", 198002; 스크립트: "Henkes, O'Hern & Behringer") | force-chain 퍼콜레이션, "≈40 % 입자가 ≈80 % 하중" | `strict_physics.py:31–33` · `refs.bib:253` · `main.tex:570` — 8 줄 / 5 파일 | **M** (서지 혼합) + 수치 미확인 | 웹: PRL 95, 198002 (2005) = Henkes & **Chakraborty**, *"Jamming as a critical phenomenon: a field theory of zero-temperature grain packings"* — refs.bib 의 제목은 다른 논문, 스크립트의 저자 목록은 또 다르다 | `4af41f62d` / `144e18b60` 2026-05-13 |
| D8 | **Liu & Yin 2025** (refs.bib: "Liu, Z. and Yin, H., *Stress-bearing percolation in all-solid-state battery composite cathodes*, J. Power Sources 2025", 권·쪽 없음) | f_perc = **0.65** "ASSB 복합양극 응력-지지 퍼콜레이션", "continuum FEM stress analysis", "their Methods section" | **57 줄 / 14 파일**: `main.tex:682,898,911,942,961,988` · `predict_porosity_{honest,strict_physics,final}.py` · `diag_se_percolation_threshold.py:4–31` · `grade_engine.py:13,118` · `README.md:90` · `docs/literature_coverage/README.md:685` ("Liu & Yin 2025, our paper") | **M** (그 서지는 **F**) | 정확 제목 검색 미발견. 실재하는 "Liu & Yin 2025" 는 De-Yun Liu · Zhen-Yu Yin, *"Compression characteristics and particle scale stress distribution of sand-rubber mixtures…"*, **Computers and Geotechnics 177 (2025) 106907** (*검색 요약*) — **모래–고무 DEM**. 첫 도입 커밋도 *"sand-rubber stress-shadow effect (Liu & Yin 2025)"* 라 적었다. 0.65 는 원문 미확인 | `33c9bdad9` 05-13 (sand-rubber) → `5c1a3681b` (f_perc 0.65 "sand-rubber extrapolation") → `144e18b60` (ASSB·JPS 서지) → `4e5441d05` 05-15 ("continuum FEM") |
| D9 | Scher & Zallen 1970 | "기하 퍼콜레이션 값 0.30" (05-13 한때 f_perc = 0.30 으로 사용) | `predict_porosity_strict_physics.py:36` | **M** | 웹: J. Chem. Phys. 53, 3759 (1970), 3D 임계 점유 부피분율 **0.144–0.163** (*검색 요약*) | `4dd66f772` 2026-05-13 |
| D10 | Heckel 1961 (*Trans. Metall. Soc. AIME* 221, 671) | ε = ε₀·exp(−K·P), K ≈ 1/(3σ_y), P_y = 1/K | refs.bib · `heckel_analysis.py:11` · `cap_compaction_heckel.py:59` | **C** | 고전 식 (원문 미대조). P_y = 138 MPa 는 우리 DEM 값이지 Heckel 의 값이 아니다 | — |
| D11 | Furnas 1929 (refs.bib: "Flow of gases through beds of broken solids", *Ind. Eng. Chem.* 23, 1052–1058, doi 10.1021/ie50261a017) | "D_large/D_small ≳ 4" 이성분 논거 | `refs.bib:349` · `main.tex:562` · `literature_coverage/README.md:539` | **M** (서지 혼합) + 수치 **B** | 웹: 그 DOI 는 **Furnas 1931**, *"Grading Aggregates I. Mathematical Relations for Beds of Broken Solids of Maximum Density"*, Ind. Eng. Chem. 23(9) 1052–1058 | `49e3f85b8` 2026-05-15 |
| D12 | Furnas (1931) / McGeary (1961) | 이성분 최적 소입자 분율 x_S ≈ 0.27 | `docs/Packing_Regime_Analysis.md:90,150` | **V** | McGeary 카드: *"이성분 최대밀도 86.0 % … 최적 조성 ~72.7 % coarse"* | — |
| D13 | McGeary 1961 | Fig 3 이성분 도표 · Fig 5 d_c/d_f ≈ 7 무릎 · "no plastic deformation of particles occurs" | `refs.bib:624` · `literature_coverage/README.md:520–531` | **V** | 카드: *"임계 크기비 (knee) d_c/d_f ≈ 7 … stated (§V, Fig 5)"*, *"'no plastic deformation of particles occurs' — 강체 구 명시"* | — |
| D14 | de Larrard (Stovall–de Larrard–Buil 1986; 1999 저서) | CPM 기하 패킹 | `delarrard_*.py` · `References_and_Methodology.md:52` | **C** | 방법 인용 (β 값은 우리 선택) | — |
| D15 | Martin & Bouvard 2003 | E₂/E₁ 10 → 100 에서 거시응력 < 3 % 변화 (rigid-AM 근거) | `literature_review_dem_mpm_assb.md:66` | **V** | 카드: *"경질상 강성은 거의 무관(E₂/E₁ 10↔100에서 <3 %)"* | — |

⚠ 커밋 `4af41f62d` (05-13) 메시지 원문: *"Replaced single-source f_perc=0.65 (Liu & Yin 2025 only) with central value 0.62 from
literature consensus 0.60-0.70 … Predictions remain within ±1% of measured DEM"* — **DEM 에 맞춘 값에 다섯 개 참고문헌을
나중에 붙였고**, 그 다섯 중 둘은 서지가 틀렸고 (D2, D7) 하나는 없는 서지 (D8) 이며 하나는 다른 저널·연도 (D6), 하나는
경상/연상을 뒤집은 재해석 (D4) 이다.  원고 초안 `docs/paper/main.tex` 가 이 묶음을 그대로 인용한다
(`LiuYin2025` 6 회, `Sridhar2000` 2 회).

### E. ASR · 전도도 · 피복률의 "문헌 범위"

| # | 인용 | 값 / 주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| E1 | Bielefeld 2022, "Adv. Energy Mater." | sulfide 양극 ASR_ionic **10–50 Ω·cm²** @ 1 mAh/cm² (신뢰 게이트 하한) | `scripts/run_network_full_corrections.py:522–526` (`ASR_IONIC_TRUST_RANGE`) · `webapp/app.py:125,134,1419,10613` · `single.html:2453` · `STAGE_E_ASR_GUIDE.md:362` · `Reviewer_Defence_Notes.md:347,695` · `main.tex:89,111,507` — 21 줄 / 10 파일 | **B** ⚠ | 웹: 실재하는 Bielefeld 2022 는 **J. Electrochem. Soc. 169, 020539** (DOI 10.1149/1945-7111/ac50df, kinetics·morphology·voids 시뮬) — AEM 아님; ASR 수치 미확인. 게다가 `refs.bib:92 @Bielefeld2022` 는 **2019 JPCC 논문 (123, 1626; DOI jpcc.8b11043) 에 연도만 2022** 를 단 것이고, 그 논문은 σ 를 풀지 않는다 (Bielefeld 2019 카드) | `19e03e9fb` 2026-05-06; bib `c66f9ae94` 05-08 |
| E2 | Lee 2020, "Joule" | argyrodite 양극 ASR_ionic **30–80 Ω·cm² @ 380 MPa** (상한) | 같은 곳 + `single.html:1741` ("Sakuda 2013 / Lee 2020 와 일치") — 18 줄 / 8 파일 | **B** ⚠ | `refs.bib:133 @Lee2020` = Lee Y.-G. et al., **Nature Energy 5, 299–308 (2020)** (웹 실재 확인: Ag–C 음극 전지) — "Joule" 표기와 모순; ASR·380 MPa 미확인 (380 MPa 는 Minnmann 2021 의 제조압과 같은 수) | `716f98e81` / `19e03e9fb` 2026-05-06 |
| E3 | Minnmann 2021 | "wet-coated catholyte" ASR 50–200 Ω·cm² | `STAGE_E_ASR_GUIDE.md:364` · `single.html:2453` | **M** | 카드: 제조 *"dry mixing(agate mortar 15 min) + 단축 380 MPa"*, TLM 결과 *"R_el = 107 Ω, R_ion = 360 Ω"* — 습식 아님, Ω·cm² 범위 서술 없음 | `19e03e9fb` 2026-05-06 |
| E4 | refs.bib `@Minnmann2021` = "…charge **rate and inactive components**…", JES 168, **040502**, DOI **abf3a3** | E1–E2 와 함께 "ASR 이 문헌 범위 안" 의 근거 | `refs.bib:103` · `main.tex:89,111,507` | **F** (추정) | 웹 2 회: 040502 / abf3a3 / 그 제목 미발견 — 실재 확인은 040537 / abf8d7 (Bottlenecks) 뿐. ⚠ 정본 `minnmann2022_…` 카드가 *"두 Minnmann 2021이 있다 … (ii) 040502 abf3a3"* 라 적지만 그 근거는 refs.bib 자신이다 (카드도 검증하지 않았다) | `c66f9ae94` 2026-05-08 |
| E5 | Bielefeld 2023 | VGCF 0.4 · C65 4 wt% 70 mS/cm "directly measured" | `predictor_engine.py` (정정 완료) | **F** (추정) | 카드 없음, 검색 미발견. `AUD-02` 가 이미 처리 | (AUD-02) |
| E6 | Mücke 2025 | VGCF/Super-P 1–3 wt% 로 σ_e 10–100× 회복 · coverage AM ≥ 60 % 권장 · 상용 75–90 % AM sweet spot · retention +5–10 % | `scripts/grade_engine.py:18,218,285,410` · `docs/GRADING_STORY.md:15,189` · `single.html:2741` — 7 줄 / 3 파일 | **F** (추정) | 카드 없음. 웹 2 회 미발견 (가장 가까운 것은 Mücke 가 공저자인 2023 년 구조분해 시뮬 논문 — *검색 요약*) | `41f3a9d9a` 2026-05-20 |
| E7 | Minnmann 2021 | 실험 coverage **40–65 %** ("Rough ~50–55 % 가 정확 일치"); `k_spread = 1.65 = Minnmann 2021 match` | `single.html:1735,2128` · `scripts/plastic_coverage.py:287` — 10 줄 / 7 파일 | **M** | 카드: EIS-TLM 논문, coverage 측정 항목 없음. (coverage 측정은 `minnmann2024_…` 의 *"CAM coverage by ISE BM10 ≈20 % → ≈50 %"*, SE 가 Li₃PS₄–LiI) | `660600a44` (import, 1.65) · `716f98e81` 2026-05-06 (40–65 %) |
| E8 | Minnmann et al. (2021, 2024), "ACS Appl. Mater. Interfaces" | 복합 양극 σ_el ≈ 10–15 mS/cm 측정 | `docs/electronic_conductivity_derivation.md:298,352` | **M** | 카드: 10 mS/cm 는 **NCM-622 벌크** 전자 σ (SI Table S2 입력값), 복합은 *"σ_el,eff = 5.6×10⁻⁴ S/cm = 0.56 mS/cm"* @ 42 vol%; 저널은 JES | `660600a44` (import) |

### F. Bielefeld 2019 / 2020 의 기타 귀속

| # | 인용 | 값 / 주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| F1 | Bielefeld 2019 (+ Liu & Yin 2025) | "SE percolation ≥ 99 %" 문헌 문턱; "< 95 % 면 이론 σ_ionic 도 절반 이하" | `grade_engine.py:13,118` | **M** | 카드: *"⚠ 유효 전도도 σ 자체는 안 푼다"*; 99 %·반감 서술 없음 | `41f3a9d9a` 2026-05-20 |
| F2 | Bielefeld 2019 (따옴표 인용) | *"Solid electrolyte does not infiltrate small pores, leading to void formation and decreased ionic conductivity"* → "큰 SE 가 void 를 만든다는 명시적 증명" | `docs/paper_brittle_caveat.md:972–976,1016,1166–1170,1208` | **M** | 카드에는 SE 입경 스윕이 없다 (입경 효과는 AM d = 3–15 µm 뿐), σ 는 산출하지 않는다; 인용문도 카드에 없다. (비슷한 서술은 Bielefeld 2022 JES 초록 — *검색 요약*) | `afd760adf` 2026-04-30 |
| F3 | Bielefeld 2019 | "φ_c = 0.185 [optimized, consistent with]" | `docs/References_and_Methodology.md:178` | **U** | 카드엔 SE 이온 한계로 *"AM > 79 vol% → 이온 클러스터 부실"* (porosity 20 %) 뿐; 0.185 와의 대응 근거 없음 | `660600a44` (import) |
| F4 | Bielefeld 2019 | β = 0.41 · p_c = 7.83·ln(d/µm) + 36.67 vol% · CAM ≥ 50 vol% · 3–5 µm (Minnmann 2022 경유) | `webapp/predictor_engine.py:834` · `literature_coverage/README.md:268–269` | **V** | 카드: *"β=0.41(Eq 1/Fig 4)·p_c=[7.83·ln(d/µm)+36.67] vol%(Eq 8/Fig 6) 둘 다 본문 verbatim 확인"* | — |
| F5 | Bielefeld 2020 | τ² 4.2 → 6.4 → 10 (바인더 0 / 0.05 / 0.10, 70:30) · 5 % void 가 20 % 대비 σ 2× | `docs/reviews/table_s3_data_20260827.md:459` 등 | **V** | 카드: *"70 vol% AM서 τ² = 6.4(0.05) / 10(0.10) vs 바인더-free 4.2"*, *"5% void가 20% void 대비 σ_eff 2배"* | — |
| F6 | Bielefeld 2020 | "ASSB 의 n ≈ 3~4" (Bruggeman 지수) | `GB_correction_fitting_report.md:603` | **M** | 카드: 수정 Bruggeman τ² = γ·ε^(−α), *"α∈[2.02, 1.21]"* → σ ∝ ε^(1+α), n ≈ 2.2–3.0 (환산) | `660600a44` (import) |
| F7 | Bielefeld 2020 | PTFE σ_ion ×0.74 / wt% | `docs/a3_binder_sweep_result.md:38` | **M** | 카드: 바인더는 NBR / PVDF, 0.74 없음. 코드 (`grade_engine.py:1683`) 는 같은 값을 Hong 2026 에 귀속 → §3 | `da20688e8` 2026-06-30 |
| F8 | Bielefeld 2020 (+ "Nature Communications 2024") | sub-µm 입자는 같은 압력에서 jamming 으로 85–90 % 밀도에 멈춘다 | `paper_brittle_caveat.md:935,1133` | **M** | 카드: porosity 는 **입력** (15 % 고정), 입경–밀도 관계를 산출하지 않는다 | `d62ba398b` 2026-04-30 |
| F9 | Bielefeld 2022 | "f_SE^geometric ≈ 0.36 (RCP 기하 퍼콜레이션)"; `f_SE^sep` · `f_AM^cc` 개념 출처 | `literature_coverage/README.md:682` · `single.html:1774,2005` | **U** | 2022 원문 미확인. 연결-클러스터 이용률 개념 자체는 Bielefeld **2019** 카드 (θ_ν) 에 있다 → "2022" 는 refs.bib 연도 오기에서 온 것으로 보인다 (추정) | `9e24233ef` 2026-05-06 · `296711edc` 05-18 |

### G. 기타 (퍼콜레이션 지수 · 방법 인용 · 검증된 수치)

| # | 인용 | 값 / 주장 | 사용처 | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| G1 | Kirkpatrick 1973 | 3D 전도 지수 **t ≈ 2.0** ("Kirkpatrick 1973 theory: 2.0") | `scripts/fit_percolation_2d.py:17,217,320` · `grade_engine.py:1621` — 9 줄 / 7 파일 | **B** | 웹: RMP 45, 574–588 실재. 원문 수치 미확인 (원문 PDF 접근 차단) | `1e9db0606` 2026-05-22 |
| G2 | Kirkpatrick 1973 | EMA 에서 유효 전도도가 배위수에 선형 | `docs/electronic_conductivity_derivation.md:62` | **C** | 법칙 인용 | — |
| G3 | Radjai et al. 1996 (PRL 77, 274) | 강-네트워크 필터: 법선력 크기 > 전체 평균 | `diag_se_percolation_threshold.py` · `Reviewer_Defence_Notes.md:511` | **C** | 웹 초록: 평균 이하 멱법칙 · 평균 이상 지수 감쇠 (*검색 요약*) — 평균 기준 분할과 부합. "강/약 네트워크" 명명은 원문 미대조 | — |
| G4 | Kloss 2012 (PCFD 12, 140–152) | LIGGGHTS — 원고 **[33]** | `docs/manuscript_draft/build.js:267` | **C** (서지 확인) | 웹: Kloss, Goniva, Hager, Amberger, Pirker, *Prog. Comput. Fluid Dyn.* 12(2/3) 140–152 | — |
| G5 | Hu et al. 2018 (ACM TOG 37, 150) | MLS-MPM — 원고 **[35]** | `build.js:269` | **C** (서지 확인) | 웹: *"A moving least squares material point method with displacement discontinuity and two-way rigid body coupling"*, ACM TOG 37(4) | — |
| G6 | Varkey 2026 | halide E 10.58 GPa · 바닥 21 / 37 % @ 350 MPa · yield ratio 0.0103 · β = 0.5 (ρ > 0.7) · σ 0.0026→0.0048 mS/cm · 접촉면적 8→13 % · ~100 MPa 무릎 | `CLAUDE.md:1505–1540` · `docs/data/varkey2026_ionic_vs_pressure.csv` | **V** | 카드 표 줄 18–25, 34, 50 | — |
| G7 | Sangrós 2019 | δ_y = 8.59×10⁻³·x (R² 0.89) · 탄성회복 ~17 % · Thornton–Ning | `digest_model_application_backlog.md:108` · `literature_review_dem_mpm_assb.md:230` | **V** | 카드: *"δ_y = 8.59×10⁻³ · x … (R²=0.89)"*, *"10.25 % → ~17 %"* | — |
| G8 | Sangrós 2020 | k_p(NMC) = 10⁻⁵ S/cm (Amin & Chiang 인용) | `docs/reviews/si_table_response_20260925.md:70` | **V** | 카드: *"k_p … 10⁻⁵ S/cm … stated (Amin & Chiang [24])"* | — |
| G9 | So et al. 2021 JPS 508 | φ_SE^crit ≈ 0.13 · 상대밀도 ~0.98 @ 600 MPa (~0.85 @ 300) · E_SE 24 GPa (Sakuda) · H_SE 1.9 GPa (McGrogan) · AM–AM 2.5→5.9 GPa | `refs.bib:183–201` · `literature_coverage/README.md:630–650,679` | **V** (단 "Bruggeman 이 ~3× 과대" 는 **U** — 카드에 배수 없음) | 카드 줄 27, 31, 37, 38, 41 | — |
| G10 | So et al. 2022 (JPS 530 · MethodsX 9) | SE 코팅 저압 차폐 → 고압 해제 · primary 1 / 0.5 µm → 응집체 5 / 1.5 µm · h_ov^max = 0.6·R_eff | `docs/reviews/coating_delta_gate_20260819.md:75` · `session_20260819_litdb_pending.md:156` | **V** | coated 카드 줄 50–51, 63; MethodsX 카드 줄 39 | — |
| G11 | Lawn 1998 | 파단 접촉도 micro-asperity 로 ~60 % 전도 유지 ⇒ β_F prior N(0.19, 0.05²) "literature" | `scripts/bayesian_laplace.py:24–26,59` · `generate_comparison_plots.py:6131` · `generate_fitting_report.py:537,660` · `CLAUDE.md:1819` — 14 줄 / 7 파일 | **B** ⚠ | Lawn 1998 은 실재 (refs.bib: J. Am. Ceram. Soc. 81, 1977, 구 압입 파괴). 전기 전도 주장은 원문 주제와 멀다 — 원문 미확인. prior 평균 0.19 = 우리 적합값 +0.19 (순환) | `5ccea7e3a` / `dabedefc3` 2026-05-28 |
| G12 | Conforto 2021 (JES 168, ac13d2) | GA 임피던스 적합 · NCM811 SC vs PC + LPSCl · R_ct / 확산 분리 · 사이클별 R_ct 표 | `docs/rint_anchor_db_research.md:67,163` | **B** | 웹: *"Quantification of the Impact of Chemo-Mechanical Degradation on the Performance and Cycling Stability of NCM-Based Cathodes in Solid-State Li-Ion Batteries"* 실재 — 저주파 임피던스를 NCM 입자 내 Li 확산으로 해석 (*검색 요약*). "genetic algorithm", "SC vs PC" 는 미확인 | `84bc3b354` 2026-07-20 (수치 없음) |
| G13 | O'Regan 2022 (EA 425, 140700) | poly D(sto) 3-Gaussian ×2.7 · i_ref 5.028 A/m² · α 0.43 | `docs/ncm_sc_poly_electrochem_anchors.md:31,42` | **B** | 웹: O'Regan, Brosa Planella, Widanage, Kendrick 실재 (LG M50 21700 파라미터화). 수치는 원문 (ChemRxiv 접근 차단) 미대조 | `9e0853e7a` 2026-06-26 |
| G14 | Sakuda 2013 (Tabor 사슬에 걸린 범위 밖 항목) | H_SE 0.85 GPa "LPSCl Vickers" / 0.6 GPa "nanoindentation" / σ_y "100–200 MPa" / 소성막 두께 "수 nm" | `analyze_tabor_regime.py:20` · `plastic_coverage.py:48–50,337` · `Tabor_framework_reference.md:110–111,192` · `predict_porosity_strict_physics.py:14–15` | **M** | Sakuda 카드에는 경도·항복응력·막 두께 항목이 **없다** (카드의 측정 = 초음파 펄스 E · 냉간 압축 상대밀도 · σ_ion); 소재도 LPSCl 이 아니라 Li₂S–P₂S₅ 유리 | `380c2a723` / `bd4d6fe0b` 2026-05-04 · `288d7b27c` 05-13 |

**판정 집계 (표 행 기준, 72 행)** — **M 30 · V 14 · B 10 · C 9 · F 6 · U 3**.
(한 행에 두 판정이 붙은 경우는 한 번만 셌다: D1 "B + 제목 M"·D2 "M + 수치 B"·D3 "V + 학술지 M"·D11 "M + 수치 B" 는 M,
A4 "M (Sakuda) + U (Tran)" 는 M, G9 "V + 일부 U" 는 V.  "F (추정)" 은 F 로 셌다.)
구역별 — A: M4 U1 V1 · B: M6 F2 · C: V3 C3 B3 M2 F1 · D: M9 V3 C2 B1 · E: M3 F3 B2 · F: M5 V2 U2 · G: V5 C4 B4 M1.

---

## 2. 뿌리 — 틀린 짝이 처음 들어온 커밋 (묶음별)

| 날짜 | 커밋 | 무엇이 들어왔나 | 이후 번진 곳 |
|---|---|---|---|
| **≤ 2026-04-24** | `660600a44` import (리포 이전 이력) | "Doux 2020 → 순수-SE ~10 % @ 300" 논문 문안 (A3) · Wang 2023 τ 점 (B2) · "Alabdali 2022 MethodsX 101861" (B8) · "1.65 = Minnmann 2021 match" (E7) · Minnmann 복합 σ_el 10–15 · ACS AMI (E8) · Bielefeld 2020 n ≈ 3~4 (F6) · Thornton 2015 (C12) · φ_c 0.185 (F3) | 그대로 잔존 |
| **2026-04-29** | `0a040f2b0` · `750e23b7d` | **"문헌 DEM 겹침" 표**: Wang 2023 JPS 555 (F) · Bielefeld 2020 "JES" cap 5 % (M) · Minnmann 2021 "AEM 11" 0.08 (M). 같은 날 `0a040f2b0`·`b1c8262fe` 가 날조된 **Wang 2020 JPS 470** 을 넣었다 (SELF-51) — **같은 파일 (`build_literature_reference.py`) 의 이웃 행**이다 | 웹앱 상수 CSV, `paper_brittle_caveat.md` 6 곳 (원고용 문단) |
| **2026-04-30** | `afd760adf` · `d62ba398b` | Bielefeld 2019 가짜 따옴표 인용 (F2) · Bielefeld 2020 + "Nat. Commun. 2024" 입경–밀도 (F8) | `paper_brittle_caveat.md` 영·한 두 벌 |
| **2026-05-04** | `148d0f5fb` · `23d35991a` · `bd4d6fe0b` · `380c2a723` ("Tabor framework" 날) | Brake 2012 [0.1, 100] 경계 · "ceramic/ASSB 표준 2.8" (C3·C4) · Greenwood 1992 J. Tribol. (C5, F) · Storåkers JMPS 45:1421 (C6) · So 2022 = Storåkers 단순화 (C8) · So 2022 sim-vs-real E (B7) · "softened E 표준 관행 (Bielefeld 2019, Wang 2023)" (B3) · Sakuda 경도 (G14). **`bd4d6fe0b` 는 SELF-51 이 Wang 2020 의 역할을 NCM 경도 → E_AM 140 으로 바꾼 바로 그 커밋이다** | `Reviewer_Defence_Notes.md`, `Tabor_framework_reference.md`, `paper_brittle_caveat.md` §Tabor (원고용), `analyze_tabor_regime.py` 상수 |
| **2026-05-06 ~ 08** | `19e03e9fb` · `716f98e81` · `9e24233ef` · `c66f9ae94` | ASR 문헌 범위 삼총사 (Bielefeld 2022 AEM · Lee 2020 Joule · Minnmann 2021 wet-coated — E1–E3) · Minnmann coverage 40–65 % (E7) · refs.bib 의 `@Bielefeld2022` (=2019 JPCC 연도 오기) · `@Minnmann2021` (040502 유령, E4) · `@Lee2020` (Nat. Energy) | `run_network_full_corrections.py` 의 **신뢰 게이트 상수** · 웹앱 툴팁 · `main.tex` ASR 문장 3 곳 |
| **2026-05-12 ~ 15** | `ead2d1f9e` → `4dd66f772` → `97cc1eac0` → `288d7b27c` → `33c9bdad9` → `5c1a3681b` → `4af41f62d` → `144e18b60` → `49e3f85b8` → `4e5441d05` (porosity 예측기 한 세션, 세션 링크 `session_01MU3M9cT8EGaPM8GkGsVjqw`) | **10 % 앵커가 36 분 사이 (01:17→01:53 UTC) 세 지위를 거침** (A4·A5) · Sridhar α (D1) · Bouvard 2004 Fig 2 (D5) · Scher–Zallen 0.30 (D9) · Liu & Yin 2025 (모래–고무 → ASSB·JPS·FEM 으로 변이, D8) · **"5-reference literature consensus"** — DEM 에 ±1 % 로 맞춘 f_perc 에 사후로 붙인 서지 다섯 (D2·D4·D6·D7·D8) · refs.bib 의 Storakers2000 / Bouvard2000 (Mech. Mater.) / Jacobs2009 / Henkes2005 / LiuYin2025 / Sridhar2000 제목 / Furnas1929 | `docs/paper/main.tex` (LaTeX 원고 초안), `docs/porosity_wave_shape_physics.md`, `diag_se_percolation_threshold.py`, `grade_engine.py` |
| **2026-05-20 ~ 28** | `41f3a9d9a` · `1e9db0606` · `5ccea7e3a` · `dabedefc3` | grade_engine 문헌 문턱 (Mücke 2025 F · Bielefeld 2019 ≥ 99 % M · Liu & Yin) · Kirkpatrick t = 2.0 (B) · Lawn 1998 60 % 전도 → β_F prior (B⚠) | 웹앱 종합 등급 · σ_ionic 폼의 Bayesian prior |
| **2026-06-03 ~ 07** | `a58e1b7c9` · `1eb6f6500` · `4706f7665` · `2d0ce2a61` | Cronau 380 MPa 겹침 바닥 5–10 % (B6) · Doux 2020 10 % 앵커 (A3) · **CLAUDE.md frame[1] 의 "Minnmann et al." 귀속 (A1)** — 이것이 이후 모든 세션이 읽는 "controlling epistemology" 에 들어가 증식의 핵이 됐다 | CLAUDE.md 8 곳, wiki, 파이프라인 안내서, MPM 보정 문서, 데이터 CSV 주석 (A1 하한 38 줄 / 27 파일) |
| **2026-06-30** | `da20688e8` | Hong 2026 값 (×0.74) 을 Bielefeld 2020 에 귀속 (F7) | 결과 문서 1 곳 |
| **2026-08-23 ~ 29** | `c2670de6e` · `d45576e2a` | **원고** Methods 에 [9] "T. Minnmann … AEM 2022" 를 10 % 목표 · 11–12 % 겹침 문장 끝에 붙임 (A2) | `docs/manuscript_draft/build.js` (→ docx) |

**유형으로 보면 뿌리는 셋이다.**
1. **표를 채우는 서지 생성** (04-29 · 05-04 · 05-06): 숫자 칸을 채우려고 "저자 + 연도 + 저널 + 권" 을 붙였고, 제목이 없거나
   (Wang 2023, Greenwood 1992) 실재 논문의 학술지·연도를 바꿨다 (Bielefeld 2020 "JES", Minnmann 2021 "AEM", Storåkers
   JMPS 45, Bielefeld 2022 AEM, Lee 2020 Joule).  **SELF-51 의 Wang 2020 과 같은 날·같은 파일·같은 방식이다.**
2. **적합 후 사후 정당화** (05-13 `4af41f62d`): 데이터에 맞춘 상수 (f_perc, α_KC, 10 % 끝점) 에 "published, no fit" 라벨과
   참고문헌을 나중에 붙였다.  서지가 실재 논문의 조각을 섞은 형태 (Jacobs PRE 1996 제목 + PNAS 2009, Henkes 2005 권호 +
   2007 제목, 모래–고무 Liu & Yin 을 ASSB 로) 라서 **검색 한 번으로는 "있는 것처럼" 보인다.**
3. **값은 남고 출처만 갈아 끼우기** (10 % 앵커): 사용자 입력 / 내부 보정값이 다섯 개의 서로 다른 논문 이름을 차례로 입었다
   (import 의 Doux → 05-13 Sakuda·Tran → 05-13 user lab → 06-07 Doux·Minnmann → 08-23 원고 [9]).  정본 카드 세 장
   (Minnmann 2021 · 2022 · 2024) 이 06-26 에 이를 이미 부정했지만 CLAUDE.md frame[1] 과 원고는 고쳐지지 않았다.

---

## 3. 대체 인용 — 정본 카드 (V) 로만

| 틀린 짝 | 정본 카드로 대체할 수 있는 것 | 대체 불가 → 원문 필요 |
|---|---|---|
| A1–A5 순수-SE 10 % @ 300 MPa | **"10 %" 를 주는 카드는 없다.**  실측 앵커로 쓸 수 있는 V 값: `doux2020_stack_pressure_assb` — LPSCl 펠릿 **18 % @ 370 MPa**; `sakuda2013_sulfide_mechanical_property` — 75Li₂S·25P₂S₅ 유리 *"exceeds 90 % at over 350 MPa"* (stated; 300 MPa ≈ 87 % 는 그림 판독); `minnmann2021_jes_charge_transport_bottlenecks` — **복합** 13–17 % @ 380 MPa (avg 14 % 가정). ⇒ 10 % 는 "우리 MPM/DEM 보정 표적" 으로만 적을 수 있다 (Minnmann 2021 · 2022 카드의 표현) | 10 % 를 실험값으로 쓰려면 원문 필요 (user lab 자료 또는 새 문헌) |
| A2 원고 [9] | 문장이 스스로 말하는 "composite and glass literature" 는 `minnmann2021_…` (JES 168, 040537, **P.** Minnmann) + `sakuda2013_…` (Sci. Rep. 3, 2261) 로 바꿔야 문장과 맞는다 | 11–12 % 겹침은 인용 대상이 아니다 (우리 시뮬 결과) |
| B1·B4·B5 "문헌 DEM 겹침 0.05–0.15 / cap 5 % / 0.08" | `so2021_dem_mold_pressure_assb_coldpress` — 평형 겹침비 h_ov/4R_eff 중앙값 **≈0.07 @ 400 MPa**, SE–SE ≈ 0.10, AM–AM ≈ 0.007 (Fig 6, digitized); `so2022_dem_contact_model_assb_compaction_sintering` — 명시적 상한 **h_ov^max = 0.6·R_eff** (stated); `paulick2015_elastic_particle_properties_dem_review` — 탄성 Hertz 가정의 가드레일 *"overlap < 1 % of the particle diameter"* (저압 계에 대한 규칙이라 카드가 경고) | — |
| B3 "softened E = 표준 관행" | `coetzee2017_dem_calibration_review` §7: *"In order to reduce computation time … Another method often employed by analysts is to reduce the contact stiffness"*; `paulick2015_…`: *"in pure numerical studies the elasticity is often reduced, neglecting any probable change of numerical response"*. ⚠ `vanlew2015_…` 카드: 그들의 연화는 **1.84×** — *"이 논문으로 18× 를 정당화하면 안 된다"* | 18× 라는 크기의 문헌 근거는 없다 |
| B6 Cronau 겹침 바닥 | — | 원문 필요 (Cronau 카드에 겹침 자료 없음) |
| B7 So 2022 sim-vs-real E | 반대 사실이 V: So 2021/2022 는 E_SE = 24 GPa (Sakuda) 를 **연화 없이** 쓰고 h_eq + 경도 항복으로 소성을 넣는다 | — |
| B8 "Alabdali 2022 MethodsX 101861" | `so2022_dem_contact_model_assb_compaction_sintering` — So, Inoue, Park, Nunoshita, Ishikawa, Tsuge, *MethodsX* 9 (2022) **101857** | — |
| C3·C4 체제 경계 [0.1, 100] · H/σ_y = 2.8 "ceramic 표준" | `kogutetsion2002_ep_sphere_rigid_flat` — **H = 2.8·Y** (Tabor 인용), 영역 경계 **ω/ω_c = 1 / 6 / 68 / 110** (110 = 완전소성 진입); `jacksongreen2005_…` — H_G/σ_y = 2.84 (a/R → 0) 에서 1 (a/R = 1) 로 변함, 완전소성 진입 ω* ≈ 74–82; `mesarovicfleck2000_…` — 첫 항복 p_m ≈ 1.1σ_y, plateau p_m ≈ 2.8–3.0σ_y, 진입 aE*/R₀σ₀ ≳ 50 (m = ∞) / ~100 (m = 3) | Brake 2012 의 실제 경계값은 원문 필요 |
| C5 Greenwood 1992 | 위 세 카드가 같은 역할 (전이 영역) | — |
| C6 Storåkers 서지 | `storakers1997_similarity_inelastic_contact` — *Int. J. Solids Struct.* 34(24) 3061–3083 | — |
| C8 So 2022 h_eq 의 기원 | So 2022 MethodsX 카드 §4.2 — Maxwell 점탄성에서 유도한 h_eq 변화율 | "Tabor min() 과 수학적 동등" 은 대체 불가 (주장 자체를 지워야 함) |
| D1 α_KC | `martinbouvard2003_dem_composite_cold_compaction` — K_h ≈ 1.3 (20 vol% hard) / 1.8 (40 vol%), 실험 1.3 / 1.7–2.0 (Table 1 에 Sridhar–Fleck 포함) | α = 2 (또는 3) 는 원문 필요 |
| D2·D4·D6·D7·D8 f_perc 0.62 / 0.65 | 경상 기하 퍼콜레이션만 V: `bouvard2000_hard_soft_powder_densification` — f_hard = 0.32 (r = 1), 0.18 (r = 2), 0.35 에서 첫 퍼콜레이션 (Fig 10), *Powder Technol.* 111 (2000) 231–239 | **"연상 응력-지지 임계 0.62–0.65" 를 주는 카드는 없다** — 원문 필요 (또는 우리 적합값으로 명시) |
| D5 Bouvard 2004 Fig 2 | `mcgeary1961_bimodal_sphere_packing` — 이성분 최대밀도 86.0 % @ ~72.7 % 조대 (Fig 3/5), 400-mesh W 에서 84.7 % @ 74.0 % (Fig 4), 무릎 d_c/d_f ≈ 7 | Martin & Bouvard 2004 Fig 2 의 실제 곡선은 원문 필요 |
| D9 Scher–Zallen 0.30 | — | 원문 필요 (*검색 요약*: 3D 0.144–0.163) |
| D11 Furnas 서지 | — (카드 없음) | 원문 필요 — 적어도 DOI 와 제목·연도를 한 논문으로 맞출 것 |
| E1·E2·E4 ASR 문헌 범위 | `minnmann2021_…` — TLM R_ion 360 Ω · R_el 107 Ω, σ_ion,eff 0.17 · σ_el,eff 0.56 mS/cm @ 42 vol% (Ω·cm² 로 옮기려면 두께·면적 환산 필요) | 10–50 · 30–80 · 50–200 Ω·cm² 는 원문 필요 |
| E6 Mücke 2025 | 도전재 효과는 `reisacher2023_percolation_sulfide_carbon_matrix` (AUD-02 처방) · `cho2024_conflicting_roles_conductive_additive` · `kim2024_carbon_volumetric_occupation_se_domain` 카드가 후보 (이번 감사에서 수치 대조는 안 했다) | "coverage ≥ 60 % 권장" · "75–90 % sweet spot" 은 원문 필요 |
| E7 coverage 40–65 % | `minnmann2024_microstructure_porosity_visualization` — CAM coverage by ISE ≈ 20 % → ≈ 50 % (Li₃PS₄–LiI, 380 MPa) — 다른 SE 라 추세만 | — |
| E8 복합 σ_el | `minnmann2021_…` — σ_el,eff = 0.56 mS/cm @ 42 vol% (NCM-622 벌크 10 mS/cm 는 입력) | — |
| F1 SE ≥ 99 % · F3 φ_c 0.185 · F9 0.36 | — | 원문 필요 |
| F2 Bielefeld 따옴표 | — | 원문 필요 (Bielefeld 2022 JES 초록일 가능성 — *검색 요약*) |
| F6 n ≈ 3~4 | `bielefeld2020_…` — α ∈ [1.21, 2.02], γ ∈ [0.32, 0.67] (τ² = γ·ε^−α) | — |
| F7 PTFE ×0.74 | `hong2026_sulfide_cathode_binder_digitaltwin` — σ_ionic *"Pwd 0.087 / … / PTFE 0.064"* (비 0.736) | — |
| F8 입경–밀도 jamming | — | 원문 필요 |
| G1 Kirkpatrick t | — | 원문 필요 |
| G11 Lawn 60 % | — | 원문 필요; prior 는 "적합값" 으로 명시하는 것이 정직 |
| G14 Sakuda 경도 | `so2021_dem_mold_pressure_assb_coldpress` — H_SE(LPS) = 1.9 GPa (McGrogan [8] 인용) 가 카드에 있는 유일한 황화물 경도 | 0.85 GPa (LPSCl) 는 원문 필요 |

---

## 4. 부수 관찰 (범위 밖 · 후속)

- **원고 두 벌의 노출 차이.**  현 원고 (`docs/manuscript_draft/build.js`) 에서 내 범위의 인용은 [33] Kloss (C) · [35] Hu (C) ·
  [9] Minnmann 2022 (**M**) 셋이다.  구 LaTeX 초안 (`docs/paper/main.tex` + `refs.bib`) 은 F/M 서지를 대량으로 싣는다
  (`LiuYin2025` 6 · `Lee2020` 5 · `Bielefeld2022` 4 · `Minnmann2021`(040502) 3 · `Sridhar2000` 2 · `Furnas1929` 1 +
  `Jacobs2009` · `Henkes2005` · `Storakers2000` · `Bouvard2004`).  그 초안을 재사용하면 이 목록 전체가 따라간다.
- **정본 카드도 한 번 오염을 옮겼다.**  `minnmann2022_…` 카드가 refs.bib 의 040502 항목을 *"다른 Minnmann 2021"* 로
  실재 취급한다 (E4).  카드의 서지 서술이 PDF 가 아니라 리포 파일에서 왔을 때는 V 근거로 쓰면 안 된다.
- **같은 수치 행에 다른 날조 흔적.**  `build_literature_reference.py` 의 Sakuda 2013 행 셋 (Li6PS5Cl 단결정 σ 2.5–3.5 ·
  펠릿 0.25–0.40 · 경도 0.7–1.0) 과 Lim 2018 / Quinn 2020 / de Vasconcelos 2019 / Liu 2020 파괴 행들은 04-29 같은 커밋에서 왔다
  — 재료·파괴 담당 감사에서 확인할 것.  `grade_engine.py` 머리말의 문헌 문턱 (Yoon 2025 · Park 2023 · Ohno 2020 · Tippens 2019 ·
  Famprikis 2019 · Verma 2020 · Janek/Zeier 2023) 도 05-20 같은 커밋이다.
- **원장 미등재.**  A1 (10 % 앵커) 은 09-09 잔여 감사 JSON 에 P0 로만 있고 `findings.json` 에 ID 가 없다.  B1·B2 (Wang 2023) 는
  GAP3-37 이 τ 선 한 개만 처리했고 **겹침 표 (`build_literature_reference.py:19` → 웹앱 CSV) 는 그대로**다.

---

## 5. 웹 검색 출처 (존재 확인용 — 수치 근거로 쓰지 않았다)

- Brake 2012 — [An analytical elastic-perfectly plastic contact model (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0020768312002703)
- Sridhar & Fleck 2000 — [Yield behaviour of cold compacted composite powders](https://www.sciencedirect.com/science/article/abs/pii/S1359645400001518)
- Storåkers, Fleck & McMeeking 1999 — [The viscoplastic compaction of composite powders](https://www.sciencedirect.com/science/article/abs/pii/S0022509698000763)
- Martin & Bouvard 2004 — [Isostatic compaction of bimodal powder mixtures and composites](https://www.sciencedirect.com/science/article/abs/pii/S0020740304001262)
- Jacobs & Thorpe 1996 — [Generic rigidity percolation in two dimensions (PRE 53, 3682)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.53.3682)
- de Souza & Harrowell 2009 (PNAS 106 의 실제 강성 퍼콜레이션 논문) — [PMC2741218](https://pmc.ncbi.nlm.nih.gov/articles/PMC2741218/)
- Henkes & Chakraborty 2005 (PRL 95, 198002) — [Jamming as a critical phenomenon](https://research-information.bris.ac.uk/en/publications/jamming-as-a-critical-phenomenon-a-field-theory-of-zero-temperatu/)
- Liu & Yin 2025 (실재하는 쪽, 모래–고무) — [Compression characteristics … sand-rubber mixtures](https://www.sciencedirect.com/science/article/abs/pii/S0266352X24008449)
- Scher & Zallen 1970 — [Critical Density in Percolation Processes](https://pubs.aip.org/aip/jcp/article-abstract/53/9/3759/758347/Critical-Density-in-Percolation-Processes)
- Furnas 1931 (DOI ie50261a017 의 실제 논문) — [Grading Aggregates I](https://pubs.acs.org/doi/10.1021/ie50261a017)
- Bielefeld 2022 — [JES 169, 020539](https://iopscience.iop.org/article/10.1149/1945-7111/ac50df)
- Lee 2020 — [Nature Energy 5, 299](https://www.nature.com/articles/s41560-020-0575-z)
- Minnmann 2021 (040537) — [JES abf8d7](https://iopscience.iop.org/article/10.1149/1945-7111/abf8d7)
- Kirkpatrick 1973 — [RMP 45, 574](https://link.aps.org/doi/10.1103/RevModPhys.45.574)
- Radjai et al. 1996 — [PRL 77, 274](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.77.274)
- Kloss et al. 2012 — [PCFD 12, 140](https://www.inderscienceonline.com/doi/abs/10.1504/PCFD.2012.047457)
- Hu et al. 2018 — [ACM TOG 37 (MLS-MPM)](https://dl.acm.org/doi/10.1145/3197517.3201293)
- Thornton 2015 — [Springer book](https://link.springer.com/book/10.1007/978-3-319-18711-2)
- Conforto 2021 — [JES ac13d2](https://iopscience.iop.org/article/10.1149/1945-7111/ac13d2)
- O'Regan 2022 — [Electrochim. Acta 425, 140700](https://www.sciencedirect.com/science/article/abs/pii/S0013468622008593)
- 찾지 못한 것: Wang 2023 JPS 555 (권 목록 [JPS vol 555](https://www.sciencedirect.com/journal/journal-of-power-sources/vol/555/suppl/C) 까지만) ·
  Greenwood 1992 J. Tribol. 114:134 ([J. Tribol. 114(1)](https://asmedigitalcollection.asme.org/tribology/issue/114/1)) ·
  Mücke 2025 · "Stress-bearing percolation in all-solid-state battery composite cathodes" · Minnmann 2021 040502/abf3a3 ·
  Storåkers Acta Mater 48 (2000) 4203 · Bielefeld 2023 · Tran 2025.
