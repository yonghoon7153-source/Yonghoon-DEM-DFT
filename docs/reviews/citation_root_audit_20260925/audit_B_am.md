# 감사 B: 활물질(NCM/NMC 역학·파괴·크기·전자전도) + VGCF 문헌 귀속

> ⛔ **기록 사본** — 2026-09-25 읽기 전용 감사 에이전트 보고 원문 (scratchpad → 리포 이전 09-26).  판정의 정본은 원장 `docs/reviews/claims.json` (`CL-90` · `CL-91`) 과 `findings.json` `SELF-51` 이다.  인용 금지 등록부의 문자열은 `⟦CL-xx …⟧` 로 바꿔 적었다.  file:line 은 감사 기준 커밋 기준이라 지금 줄 번호와 다를 수 있다.  종합 = `docs/reviews/citation_root_audit_20260925.md`.


- 작성: 2026-09-25. 읽기 전용 감사이며 리포는 수정하지 않았다.
- 대상: `claude/stoic-knuth-NObVQ`. 감사 중 부모 세션이 커밋을 두 개 올려 HEAD가 바뀌었다.
  - 시작 시점: `bd6d5efa2` + 미커밋 수정.
  - 종료 시점: `171934433` (SELF-51 1단계, Wang 2020 정정) → `b037d765c` (2단계, σ_grain 출처 정정).
  - 표의 file:line은 `b037d765c` 기준이다. 커밋으로 줄이 밀린 CLAUDE.md와 generate_fitting_report.py는 다시 확인했다.
- 정본 카드: `origin/claude/friendly-meitner-lldvar` @ `f9f834cd0`. fetch는 하지 않았다.
- 보조 근거: PyBaMM `Chen2020.py` 소스 사본(`scratchpad/pb/pb/pybamm/input/parameters/lithium_ion/Chen2020.py`). 정본 카드는 아니므로 B까지만 올린다.
- 상태 코드:
  - V: 정본 카드에 그 재료의 그 값이 있다.
  - M: 논문은 있으나 그 값·재료·서지가 아니다.
  - B: 논문 실재는 검색으로 확인했으나 값은 확인하지 못했다.
  - F: 찾을 수 없다.
  - C: 고전 법칙을 인용한 경우.
  - U: 판정할 수 없다.
- 검색 스니펫에서만 본 숫자는 모두 "검색 요약 — 미확인"으로 적었다.
- ⛔ 금지 등록부에 오른 문자열(CL-90 논문의 기사 번호·지어진 제목)은 이 보고서에 적지 않는다.

---

## 0. 요약

**판정한 (인용 → 값/주장) 쌍은 66개다: V 15 · M 19 · B 8 · F 12 · C 1 · U 11.**

**가장 나쁜 5개**

1. **K_IC 쌍 — Liu 2020 "Nat. Energy 5, 304" (단결정 1.0 MPa·m^½)과 Quinn 2020 "Joule 4, 2466" (다결정 0.3). 판정 F.**
   - 이 두 값이 AM_S/AM_P 파괴 대비(P_c 약 11배)를 결정한다.
   - Liu의 좌표는 Nat. Energy 5권 299–308쪽 안에 떨어지는데, 그 쪽은 Lee Y.-G. 외 2020(Ag–C 음극 전고체)이다. 이 논문은 리포 `docs/paper/refs.bib`의 Lee2020으로 이미 인용돼 있다.
   - 원고 절(`paper_brittle_caveat.md`), 웹앱 툴팁, 반박 노트에 퍼져 있다.
2. **"실험 검증" 표 — Lim 2018 "Nano Lett. 18, 2087", de Vasconcelos 2019 "Acta Mater. 178, 35", Quinn 2020. 판정 F.**
   - 단계 비율 60–75 / 15–25 / 5–10 / 1–5 %가 이 세 인용에 기대고 있다.
   - 원고 문장 *"Every stage falls within the experimentally observed range … not obtained by parameter tuning … independent literature sources"*는 근거가 0이다.
3. **Lawn "1998" 책 §3.4 / Table 3.4 — A = 200, 단계 배수 1/2/5/10 → 1/3/11/32. 판정 M(서지) + B.**
   - 책 2판은 1993년 판이다. 1998년 저작은 별개 논문(J. Am. Ceram. Soc. 81, 1977)이다.
   - 압입 파괴는 책의 8장이다. 3장은 비선형 균열선단장이다(검색 요약 — 미확인).
   - 힘 배수는 δ 배수를 1.5승한 내부 유도값이다.
   - 이 배수들이 σ Stage D/E 보정, UI, LaTeX 초안(또 다른 배수 세트)에 퍼져 있다.
4. **Trevisanello 2021 과잉 귀속 묶음 (M, 40줄 이상).**
   - 이 논문은 σ_e를 잰 적 없는 액체 LIB 논문이다(정본 카드가 명시).
   - 그런데도 다음 값들의 출처로 붙어 있다: AM_P ×0.65, β = 1.5 "fit/측정", σ_AM 50 "단결정", "5–12 µm", microcrack ×0.85.
   - 저널과 제목도 틀리게 적혀 있다.
5. **Wang 2022 κ 유령 인용 (F, 30줄/12파일).**
   - 06-26에 리포 스스로 PHANTOM으로 판정했지만, κ 인자 0.50 등의 출처로 UI·가이드·LaTeX·반박 노트에 그대로 남아 있다.
   - 같은 계열로 Park 2024 "AEM 14: 2301245" (F 의심)가 있다.

**그 밖의 주의 사항**

- 원장 `CL-50`(live)이 아직 *"Wang 2018 NMC bulk 5×10⁻⁵ S/cm"*라고 적고 있다. 정본 카드는 그 값이 논문에 없다고 적는다(M).
- `grade_engine.py`의 "Lee 2025 ACS EL" 수치는 실제로는 Oh 2026 ACS Energy Lett. 11, 2103의 수치다(M).
- **정본 카드 자체의 오귀속**이 하나 있다. `kim2024_carbon_volumetric_occupation_se_domain` L166이 우리 복셀 σ_ionic 값 0.0168/0.0298을 "Lee 2025 σ_e"로 적고 있다(M).

**뿌리 (자세한 것은 §2)**

- `session_01KxPF3N83esrzqzya11hFMK` (04-29 01:20 → 05-04) 한 세션이 파괴 배치 전체를 만들었다.
  - `00368b5ea`: 이름 첫 등장.
  - `dba9db01a`: K_IC, Lawn §3.4, E = 150 "Xu 2017".
  - `17e8a6c78`: 6분 만에 값만 140으로 바뀌고 라벨은 그대로.
  - `b1c8262fe`: 가짜 좌표.
  - `0a040f2b0`: 문헌 표.
  - `726b6bbb2` / `d68871c70`: 원고 절.
  - `573a07187`: 툴팁.
  - `4fdfde6e7` / `c5fb6f294` / `e241675f1`: Trevisanello·Wang 2022 인자.
  - `148d0f5fb`: 반박 노트의 서지 좌표.
- `session_01AE6H8brQNyGYQLfq4X8Yq7` (05-28 → 06-03)이 σ_e 폼에 Trevisanello를 확대 귀속했다.
- 세션 링크가 없는 05-06 ~ 05-25 커밋들과 `session_01H191Ni4xzj9H5ftstAm7Ft` (06-25 → 08-19)가 추가분을 넣었다.
- `σ_AM = 50 mS/cm "NCM811 literature"`는 **import(04-24) 시점에 이미 있었다.**

---

## 1. 귀속 표

"쓰인 곳"은 대표 위치와 개수이며, 개수는 `git grep`로 litdb·docs/data·audit json을 제외하고 센 것이다.

### A. 04-29 파괴 배치 — `scripts/fracture_model.py` 참고문헌 블록 + `scripts/build_literature_reference.py` 표 전 행 (+ 파생 문서)

| # | 인용 | 붙은 값 / 주장 | 쓰인 곳 (대표, 개수) | 상태 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| A1 | Auerbach 1891, *Ann. Phys. Chem.* 43, 61 | 원뿔균열 개시하중 P_c ∝ r (Auerbach 법칙) | fracture_model.py:3,39 · paper/refs.bib:24 | **C** | 검색: Wiley "Absolute Härtemessung", Ann. Phys. 1891, 43권 61–100쪽. 서지 정확, 법칙 인용이라 수용한다. 상수 A = 200은 A3에서 따로 본다 | `dba9db01a` 04-29 04:58 |
| A2 | Lawn 1998 *"Fracture of Brittle Solids" 2nd ed., Cambridge* | 서지 자체 | fracture_model.py:40 · Lawn 1998 전체 64줄/26파일 | **M (서지 혼성)** | 검색: 2판은 CUP **1993**(ISBN 0521409721). "Lawn 1998"은 별개 논문 *J. Am. Ceram. Soc.* 81, 1977–1994 ("Indentation of ceramics with spheres: a century after Hertz")이고, `docs/paper/refs.bib`의 Lawn1998은 이 논문을 가리킨다. 코드 주석은 책과 1998년을 섞었다 | `dba9db01a` 04-29 |
| A3 | Lawn 1998 §3.4 | A = 200 ("as-prepared"; low-flaw 50 · rough 500), 단계당 factor-of-two | fracture_model.py:26,67 · single.html:2240,2262,2293 · paper_brittle_caveat.md:114,133,236,284,301,391 (A = 200은 13줄/3파일) | **B (위치 불일치)** | 두 저작 모두 실재하나 수치는 확인하지 못했다. Auerbach·압입 파괴는 책의 8장 "Indentation fracture"다(Cambridge Core 장 페이지 제목). 3장은 "Continuum aspects of crack propagation II: nonlinear crack-tip field"다(검색 요약 — 미확인). 따라서 "§3.4" 표기는 목차와 맞지 않는다 | `dba9db01a` |
| A4 | Lawn 1998 Table 3.4 | δ 배수 1/2/5/10 → 힘 배수 1/3/11/32 (intact→pulverization 5단계) | fracture_model.py:29-35,70,149 · STAGE_E_ASR_GUIDE.md:222,259 · viewer3d_data.py:41,204 · webapp/app.py:1364 (21줄/11파일) | **B (위치 불일치) + 내부 유도** | 코드 자신이 fracture_model.py:149-151에 *"(3/2)-power images of the δ-multipliers (1, 2, 5, 10)"*라고 적는다(2^1.5 = 2.83, 5^1.5 = 11.2, 10^1.5 = 31.6). 따라서 힘 배수는 별도 문헌 표가 아니다. δ 배수의 원 출처는 확인하지 못했다 | `dba9db01a` (δ) · `726b6bbb2` 04-29 08:34 (힘) |
| A5 | Lawn 1998 | 파단 접촉이 micro-asperity로 전도를 약 60 % 유지 · β_Fe "partial-Holm" | generate_comparison_plots.py:6131 · generate_fitting_report.py:660,693 · sigma_e_stage21_history.md:72 | **U** | 세라믹 압입 파괴 저작에서 전지 접촉의 전도 잔존율 수치를 확인할 방법이 없다 | `a58593227` 06-01 · `1547b028a` 06-03 |
| A6 | Lawn 1998 | "cone-crack 실험" severe ≤ 50 % envelope | run_network_full_corrections.py:558 · webapp/app.py:147,10615 | **U** | A5와 같다 | `9a13628aa` 05-13 |
| A7 | Liu 2020, *Nat. Energy* 5, 304 | 단결정 NCM K_IC 1.0 (0.8–1.4) MPa·m^½ · SC/PC 비 2.5–5 · "robustness ~10×" | fracture_model.py:18,42 · build_literature_reference.py:14,61,69 · paper_brittle_caveat.md:159,462,549 · Reviewer_Defence_Notes.md:153,684 · single.html:2233,2329 (21줄/6파일) | **F** | 검색 결과 Nat. Energy 5권 299–308쪽은 Lee Y.-G. 외 2020(Ag–C 음극 전고체)이고, 304쪽은 그 논문 안이다. "Liu 2020 단결정 NCM K_IC" 논문은 좌표·주제로 4회 검색했으나 찾지 못했다 | `00368b5ea` 04-29 01:20 (이름) · `dba9db01a` (K_IC 1.0) · `b1c8262fe` 05:12 (좌표) · `148d0f5fb` 05-04 (반박 노트 서지) |
| A8 | Liu 2020 · Wang 2022 | 단결정 facet 형상인자 f_AM_S = 1.10 ("측정값 기반") | dem_analysis_core.py:24 · single.html:2126,2140 | **F** | A7과 B13 참조 | `00368b5ea` · `573a07187` 04-30 |
| A9 | Quinn 2020, *Joule* 4, 2466 | 다결정 NCM K_IC 0.3 (0.2–0.5) MPa·m^½ | fracture_model.py:19,43 · single.html:2221,2256,2323 · paper_brittle_caveat.md:159 · Reviewer_Defence_Notes.md:156,686 (Quinn 전체 32줄/6파일) | **F** | Joule 4권 11호(2237–2522쪽)에서 Quinn 논문을 찾지 못했다(검색 3회). 실재하는 Quinn 2020은 Quinn, Moutinho, … Finegan, *Cell Rep. Phys. Sci.* 1, 100137로, NMC532 입자의 EBSD 결정립 구조 논문이다(검색 요약). K_IC 수치를 담고 있는지는 확인하지 못했다 | `dba9db01a` · `b1c8262fe` · `148d0f5fb` |
| A10 | Quinn 2020 (+Lim 2018) | multi-crack 5–10 % "(SEM)" · 분쇄 2–5 % / severe 1–5 % | build_literature_reference.py:11,43,47 · paper_brittle_caveat.md:449-450,537-538 · single.html:2190,2202,2208 | **F** | A9와 같다 | `0a040f2b0` 04-29 07:38 · `573a07187` |
| A11 | Quinn 2020 · Lim 2017 | 다결정 표면적 +40 % (f_AM_P = 1.40), "직접 측정값" | dem_analysis_core.py:23 · single.html:2134 | **F** (Quinn) / B (Lim 2017) | 실재하는 Lim 2017은 *Sci. Rep.* 7, 39669(NCM811 균열 기원)로, 제1원리~phase-field **계산** 논문이다(검색 요약). "직접 측정"이라는 서술과 성격이 맞지 않는다. 1.40은 확인하지 못했다 | `00368b5ea` |
| A12 | de Vasconcelos 2019, *Acta Mater.* 178, 35 | 압축 후 microcrack 15–25 % · 파괴인성 측정법 · PC K_IC 0.2–0.5 | fracture_model.py:44 · build_literature_reference.py:12,51,65 · paper_brittle_caveat.md:448,536 · single.html:2184,2208 (7줄/4파일) | **F** | 이 좌표는 검색 3회로 찾지 못했다. de Vasconcelos의 2019년 실재 논문은 *Exp. Mech.*(액체 중 in-situ 나노인덴테이션, 검색 결과 링크)이며, 이 값의 출처라는 근거는 없다 | `b1c8262fe` · `0a040f2b0` |
| A13 | Lim 2018, *Nano Lett.* 18, 2087 | 200 MPa 적층압에서 2차입자 분쇄 · severe 1–5 % · intact 60–75 % ("implied") | build_literature_reference.py:9,43,55 · paper_brittle_caveat.md:447,456,501,535,543,584 · single.html:2202 (12줄/3파일) | **F** | 좌표·주제 검색 2회로 찾지 못했다 | `0a040f2b0` · `d68871c70` 04-29 11:34 ("implied") |
| A14 | Xu 2017, *Phys. Rev. X* 7, 041038 | NCM811 나노인덴테이션 (E, H) | fracture_model.py:45 · build_literature_reference.py:15 (`171934433`에서 JES로 정정됨) | **F** | 검색 결과 PRX 7, 041038은 콜로이드 확산영동 논문(2017-11-16)이다 | `b1c8262fe` · `0a040f2b0` (PRX 약칭) |
| A15 | Xu 2017 (실재: *J. Electrochem. Soc.* 164, A3333) | E_NCM811 130–165 GPa · E_AM 140 "NCM811 나노인덴테이션" · ν ≈ 0.25 | build_literature_reference.py:71-74 · paper_brittle_caveat.md:163,327,459,545 · Reviewer_Defence_Notes.md:114 · nca_material_preset.md:19 | **B** (+ 재료 M) | 논문은 실재한다(IOP). 대상은 **NMC532**다(검색 요약: SOC·사이클별 E·H·계면 강도). 따라서 "NCM811" 라벨은 맞지 않는다. 범위와 ν는 확인하지 못했다. ★ 이력 증거: `dba9db01a`(04:58)에서 "Xu 2017 (NCM811 nanoindentation)"은 **E = 150 GPa**에 붙어 있었는데, `17e8a6c78`(05:04)에서 값만 140으로 바뀌고 라벨은 남았다. 값이 논문에서 온 것이 아니라는 뜻이다 | `dba9db01a` · `17e8a6c78` · `726b6bbb2` · `148d0f5fb` (ν) |
| A16 | Wang 2020, *JPS* 470 (원장 CL-90) | NCM 경도 5–8 / 6 GPa (이후 E 140, LPSCl 24로 번짐) | `171934433`에서 9곳 정정 | **F** | 원장 CL-90 (live). 이번 검색에서도 JPS 470의 해당 논문을 찾지 못했다 | `b1c8262fe` · `0a040f2b0` |
| A17 | Bielefeld 2020 "J. Electrochem. Soc." | "relaxation-included DEM, max overlap 5 %", cap δ/R 0.04–0.05 | build_literature_reference.py:18 + max_dr_R_with_cap 행 · paper_brittle_caveat.md:44,87,135,302,777,852 | **M** | 정본 `bielefeld2020_effective_ionic_conductivity_binder`는 *ACS AMI* 12, 12821이다(JES 아님). GeoDict 확률 배치 모델로, *"AM = 겹침 없는 구, SE = 겹침 허용 convex polyhedra"*(L106–107). DEM·relaxation·5 % cap은 없다. 2019 카드 L70은 *"DEM 접촉법칙: 없음"* | `0a040f2b0` |
| A18 | Wang 2023 "J. Power Sources 555" | DEM 최대 δ/R 0.05–0.15 (+ "softened E가 표준 DEM 관행") | build_literature_reference.py:19 + max_dr_R_typical 행 · paper_brittle_caveat.md:44,135,777 · Reviewer_Defence_Notes.md:78 | **F (의심)** | 제목 없이 좌표만 있고, 검색 2회로 찾지 못했다. 리포 자체 감사(`gap_audit_r3_repair_20260917.md` ⓔ)도 "출처 0건"으로 판정했다 | `0a040f2b0` |
| A19 | Minnmann 2021 "Adv. Energy Mater. 11" | "DEM with relaxation, max overlap 0.08" (0.06–0.10) | build_literature_reference.py:20 + max_dr_R_with_relax 행 · paper_brittle_caveat.md:44,87 | **M** | 정본 `minnmann2021_jes_charge_transport_bottlenecks`: *J. Electrochem. Soc.* 168, 040537, *"type experiment (EIS-TLM + cell cycling)"*. DEM 논문이 아니다 | `0a040f2b0` |
| A20 | Sakuda 2013 | σ_grain 2.5–3.5 mS/cm, "Li6PS5Cl single-crystal ultrasonic" | build_literature_reference.py (tabor_se 1행) | **M** | 정본 `sakuda2013_sulfide_mechanical_property`: 소재는 75Li₂S·25P₂S₅ **유리**로 *"우리 LPSCl argyrodite 아님"*(L23). 초음파는 **E** 측정법이다(L56). σ는 0.31(냉간)/0.34 mS/cm(L57) | `0a040f2b0` |
| A21 | Sakuda 2013 | 냉간 펠릿 σ 0.25–0.40 mS/cm, "Li6PS5Cl, GB-dominated" | 같은 표 2행 | **M** | 값대는 유리의 0.31/0.34와 맞지만 소재 귀속이 틀렸다 | `0a040f2b0` |
| A22 | Sakuda 2013 | H_SE 0.7–1.0 GPa, "Li6PS5Cl hardness, default 0.85" | 같은 표 3행 · Reviewer_Defence_Notes.md:20 ("Sakuda 0.6 GPa") | **M** | 카드에는 경도 값이 없다(E·σ·밀도만 있음). 소재도 유리다 | `0a040f2b0` |
| A23 | Sakuda 2013 | SE 형상인자 1.05 ("quenched glass near-spherical") | dem_analysis_core.py:25 | **U** | 카드에 형상인자가 없다 | `00368b5ea` |

### B. AM 전자·열전도 결정립 인자 (Trevisanello · Wang 2022/2021 · Park 2024 · Wang 2018 · Amin)

| # | 인용 | 붙은 값 / 주장 | 쓰인 곳 | 상태 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| B1 | Trevisanello 2021 | σ_S = 10 / σ_P = 5 mS/cm ("Trevisanello 10/5") | 잔존: **CLAUDE.md:2311, 2313**. 코드와 다른 문서는 A1(06-30)에서 정정됐다 | **M** | 정본 `trevisanello2021_sc_pc_ncm_cracking_diffusion` L30–34: *"이 논문은 벌크 전자전도도(σ_e)를 단결정/다결정에 대해 측정한 적이 전혀 없다… D_Li, BET, R_ct 뿐이며 모두 액체전해질 셀"* | `eed0b9581` 05-28 · `b4f62e852` 06-03 |
| B2 | Trevisanello 2021 | AM_P σ_e ×0.65 ("다결정 σ_e 35 % 낮음") · 크기표 0.75/0.65/0.55/0.45 · Stage D microcrack ×0.85 (Heenan 2020과 병기) | run_network_full_corrections.py:14,138,178 · run_network_fracture_stagewise.py:13-14 · single.html:2408-2409 · Reviewer_Defence_Notes.md:135 · STAGE_E_ASR_GUIDE.md:79,130-139 · webapp/app.py:1150,1277,2143 | **M** | L30–34와 같다(σ_e 측정 없음) | `4fdfde6e7` 04-30 10:52 (0.85) · `c5fb6f294` 11:47 (0.65) · `e241675f1` 11:50 (크기표) · `2900b6b0a` 05-06 (UI) · `84573970d` 05-08 ("35 %") |
| B3 | Trevisanello 2021 | NCM(r) = 1/(1+(r/2)^1.5), β = 1.5를 "Trevisanello fit / 측정 / GB scaling / exact lock"으로 표기 | CLAUDE.md:2367,2412 · sigma_e_stage21_history.md:30,52 · generate_fitting_report.py:610,685,727 · electronic_locked_exponent_screen.py:7,133,231 · seminar_deck/build.js:369 · seminar_20260806_script.md:219 (26줄/14파일) | **M** | L265–267: *"β=1.5라는 지수의 정량 fit이 본 논문에 없다… '"Trevisanello β=1.5"는 출처 과장'"*. 정성적 방향(큰 PC가 불리)만 지지하며, 기전도 전자 GB가 아니라 확산·표면적이다(L270–273). CLAUDE.md:2265의 "supports the NCM(r) GB DIRECTION"은 방향은 맞고 기전은 틀렸다 | `90a789825` 06-01 · `1547b028a` / `3aa171ed2` 06-03 |
| B4 | Trevisanello 2021 | σ_AM = 50 mS/cm "NCM811 single-crystal" | electronic_locked_sigma_test.py:2,9,98 · voxel_conductivity.py:93,467 | **M** | L30–34에 더해, A&C 카드 L68: *"σ_AM = 50 mS cm⁻¹ ⛔ 밖 (위), 3.6× 위"* | `037316133` 06-02 |
| B5 | (출처 없는 "literature") | σ_AM = 50 mS/cm, "NCM811 literature reference / grain interior" | CLAUDE.md:1616 · network_conductivity.py:57 · electronic_nested_cv.py:23,43,97 · generate_comparison_plots.py:5798 · single.html:2000 (13줄/9파일) | **U** | 출처가 특정돼 있지 않다. 정본 실측 카드 범위 밖이다: Wang 2018 NMC811 4.1 mS/cm(20 °C), A&C 최대 13.8 mS/cm | **import 시점부터 존재** `660600a44` 04-24 |
| B6 | Trevisanello 2021 | "reference is for typical NMC secondary (5–12 µm)" | run_network_full_corrections.py:159 | **M** | L260: *"PSD: SC 입자반경 ≈0.3–1.2 µm, PC 입자반경 ≈1–5 µm(중앙 ~2 µm)"* | `e241675f1` |
| B7 | Trevisanello 2021 | 다결정 1차입자 ~0.1–1 µm | extract_2d_microstructure.py:219,1277 · export_comsol_2d.py:699 | **U** | 카드에 1차입자 크기가 없다 | `86e8e35c1` 05-25 |
| B8 | Trevisanello 2021 | 저널 "*Adv. Funct. Mater.*" · refs.bib 제목 "…intra-particle gas evolution and lattice oxygen release" | STAGE_E_ASR_GUIDE.md:139 · docs/paper/refs.bib:61-72 | **M (서지)** | 카드 L14–17: *Adv. Energy Mater.* 11, 2003400. 제목은 "…Quantifying Particle Cracking, Active Surface Area, and Lithium Diffusion" | `84573970d` 05-08 · `c66f9ae94` 05-08 |
| B9 | Trevisanello 2021 (+ Oh 2026) | "SC vs poly R_ct: SC ≈40 % 낮음" | rint_reference_growthlaw_design.md:75 | **M** | Trevisanello L189–194: 액체 셀에서 PC R_ct는 70→15 Ω로 붕괴하고, SC는 4.2 V 이후 R_ct가 **증가**한다. Oh 2026 L287: CAM0:10(단결정만)의 계면 D2가 "매우 큼" | `cf3fa953f` 07-20 |
| B10 | Trevisanello 2021 / "Bielefeld 2022" | f_AM^cc(집전체 연결 AM 분율) 개념 | single.html:2005 | **M (개념)** | Trevisanello는 액체 LIB라 그런 지표가 없다. "Bielefeld 2022"는 refs.bib에서 JPCC 123, 1626 (= 2019 카드)의 연도를 잘못 적은 것이다 | `9e24233ef` 05-06 |
| B11 | Trevisanello 2021 | 액체 셀 PC R_ct ≈70 → 15 Ω | ncm_sc_poly_electrochem_anchors.md:47 | **V** | 카드 L189 | — |
| B12 | Trevisanello 2021 | SC D 1e-11–1e-10 cm²/s · PC 1e-10–1e-9 | ncm_sc_poly_electrochem_anchors.md:27-28 · SC 프리셋 3e-15 m²/s | **V (SC) / U (PC)** | L179: *"본 연구 SC NCM: 2×10⁻¹¹ cm²/s (x=0.4)"*. PC는 "방전 D̃^app가 충전보다 ≥1자릿수"라는 내용만 있고 절대 밴드는 없다 | — |
| B13 | Wang 2022 (refs.bib: *Energy Storage Mater.* 49, 77–87, placeholder) | κ: AM_P ×0.50 (0.30–0.65) · "phonon GB로 κ 50 % 낮음" · SE 크기 무관 · ASR_th 1–10 K·cm²/W | STAGE_E_ASR_GUIDE.md:80,153,157,162,402,407 · single.html:2414-2416,2432,2465,2596 · webapp/app.py:1150,1292,2145 · run_network_full_corrections.py:34,183,1197 · Reviewer_Defence_Notes.md:137 · paper/main.tex:75,122,202,324 · README.md:8 (30줄/12파일) | **F** | 리포 스스로 06-26에 PHANTOM으로 판정했다(refs.bib 주석, `stage2_model_audit_vs_literature.md:211`). 이번 검색에서도 찾지 못했다. 정본의 Wang 2022 카드 두 장은 SE–알칼리금속 계면 논문과 황화물 열안정성 논문으로, NCM κ와 무관하다 | `00368b5ea` (형상) · `c5fb6f294` / `e241675f1` 04-30 (κ) · `19e03e9fb` 05-06 (ASR_th) · `c66f9ae94` 05-08 (bib) |
| B14 | Wang 2021 | "단결정 NMC 1–5 µm에서 σ 일정" · Stage D multicrack ×0.40 "~60 % σ_e 손실" (Jiang 2021과 병기) | run_network_full_corrections.py:155 · run_network_fracture_stagewise.py:18 | **U** | 저자·연도만 있는 stub이다. 리포 감사(`stage2_model_audit_vs_literature.md:213`)도 "resolve 안 되는 stub"으로 판정했다 | `4fdfde6e7` · `e241675f1` 04-30 |
| B15 | Park 2024, *Adv. Energy Mater.* 14: 2301245 | AM_P σ_e 크기인자 0.45–0.75, "NCM internal-GB density" | Reviewer_Defence_Notes.md:136,680 | **F (의심)** | 이 좌표는 검색에서 찾지 못했다. 검색상 2301245는 *Energy Technol.* 12권의 다른 논문 번호다(검색 요약 — 미확인) | `148d0f5fb` 05-04 |
| B16 | Wang 2018, *JPS* 393, 75 | NCM811 pristine σ_e 4.1×10⁻³ S/cm (20 °C, DC) · NMC532 1.3×10⁻³ · E_a 0.25 eV | manuscript_draft/build.js:357-359 · si_table_response_20260925.md:62,78 | **V** | 카드 `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` L20, L35 | — |
| B17 | Wang 2018 | "NMC bulk 5×10⁻⁵ S/cm — 독립 출처" | **docs/reviews/claims.json CL-50 (status live) L1579** · codex_review_request_everything_else_20260819.md:220 | **M** | 카드 L25: *"5 × 10⁻⁵ S cm⁻¹, 이 논문 어디에도 없다 (본문·그림·SI 전수)"*. build.js는 정정됐지만 원장 CL-50은 그대로다(si_table_response는 "사용자 결정 대기"로 기록) | `181a39718` 08-19 |
| B18 | Amin & Chiang 2016, *JES* 163, A1512 | 5.0×10⁻⁸ → 1.4×10⁻² S/cm (30 °C, x 0→0.75) · NMC532 x = 0에서 1.9×10⁻⁶ | build.js:356-359 · week_plan_manuscript_20260825.md:119 | **V** | 카드 `aminchiang2016_nmc_electronic_ionic_transport_vs_li` L56, L62 | — |
| B19 | Amin 2015 (NCA, *JES* 162, A1163) | NCA σ_e: 리튬화 상태 1e-4 → 충전 상단 1e-2 S/cm | mpm_webapp_payload.py:2040 · nca_material_preset.md:42 | **B** | 논문은 실재한다. 검색 요약 "~10⁻⁴ → ~10⁻² S cm⁻¹ over x = 0–0.6"은 미확인이며, 카드가 없다 | `b474ce25b` 06-26 |
| B20 | Oh 2026 (#266) Table S15 — 내 키 밖이지만 인접 | σ_NCWA 13.7 · σ_NCM 2.45 mS/cm를 "측정한" 값으로 서술 | lit_trevisanello2021_…:237 · stage2_model_audit_vs_literature.md:27,230 · generate_comparison_plots.py:5819 · a1_sigma_e_direction_closeout.md:32 | **M (성격)** | 정본 `oh2026_bimodal_composite_cathode` L364 *"Table S13–S15 — **시뮬 파라미터**"* 아래 L373–374에 있는 값이다. 측정값이라는 명시가 없다 | `d47ac4afa` 06-25 |

### C. AM 크기·확산 — Chen 2020

| # | 인용 | 붙은 값 / 주장 | 쓰인 곳 | 상태 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| C1 | Chen 2020, *JES* 167, 080534 (LG M50) | 양극 입자반경 5.22 µm · D_s 4×10⁻¹⁵ m²/s · c_max 63,104 · m_ref 3.42×10⁻⁶ · NMC811 OCP · 창 x0/x100 | ncm_sc_poly_electrochem_anchors.md:30,41,59 · step4_pybamm_anchor.py:7,49,88 · step4_curve_from_log.py:21 · mpm_webapp_payload.py:2060 · viewer3d.js:191 (Chen 2020 전체 47줄/23파일) | **B** | 논문은 실재한다(IOP·Zenodo). 값은 PyBaMM `Chen2020.py`와 일치한다(L139 m_ref, L289 c_max, L290 D_s, L294 반경). 정본 카드는 없다 | `474082457` 07-21 등 |
| C2 | "PyBaMM Chen2020" | k_SEI = 1×10⁻¹² m/s를 "계수 앵커"로 사용 | rint_reference_growthlaw_design.md:119 | **M (출처층)** | 같은 PyBaMM 파일 docstring(L213–224): *"SEI parameters are example parameters for SEI growth from … Ramadass2004, Ploehn2004, Single2018, Safari2008, Yang2017 … does not claim to be representative"*. Chen 2020 논문의 값이 아니다 | `cf3fa953f` 07-20 |

### D. 사이클 chemo-mechanics (Kang & Shin · Bucci · Parks)

| # | 인용 | 붙은 값 / 주장 | 쓰인 곳 | 상태 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| D1 | Kang & Shin 2025 (*ACS AMI*, 10.1021/acsami.5c14519) | E_NCA 175 GPa(assumed) · 부피변화 5.9 % · 유지율 67.3/47.7 % · R_int 113.5→501.8 (4.4×) · R_w 70.7→353.4 · U-NCA 56.0→84.5 (1.51×) · σ_c 100 MPa · G_c 1 J/m² · D_s 3×10⁻¹⁴ · i0 10 A/m² | a10_cycle_chemomech_design.md:25,39,45 · cycle_rint_synthesis.py:45-52 · step4_dyn.py:35,2806 · nca_material_preset.md:9 | **V** | 카드 `kang2025_toughened_bimodal_nca_lzo` L60, 62, 67, 90–95, 102–104, Table S4 L117–131 | — |
| D2 | Kang & Shin 2025 | "3 µm 입자 damage ~0.4" | a10_cycle_chemomech_design.md:39 | **U** | 카드 L72는 *"10 µm 여러 입계에서 →1; 3 µm는 낮음"*이며, 0.4라는 값은 없다 | `0822e6adf` 07-21 |
| D3 | Bucci 2017 (*JMCA* 5, 19422) | δ0 5 nm · δcr = 20δ0 = 100 nm (Table 2) · 균열 방지 조건 ΔV ≤ 7.5 % & G_c ≥ 4 J/m² · ΔV 3 %에서 개시 · 𝒢 < 1000 · argyrodite 18.5 GPa / K_IC 0.23 · (파생) G_c 2.8 ± 1.8 | cycle_contact_ledger.py:5,342,624-625 · a10_cycle_chemomech_design.md:34-37 | **V** (G_c는 K²/E 파생) | 카드 L15, 19, 76–79, 102, 128–129 | — |
| D4 | Bucci 2018 (*PRM* 2, 105407) | 박리 개시 반경 ~2.5 % / 부피 ~7.5 % · 연속 50 % 박리 시 FPT ×2.75 · γ > 5 J/m² (E_se < 25 GPa) · 충전 = 수축 | a10_cycle_chemomech_design.md:27,38 · adhesion_agc_interlayer_20260923.md:146 | **V** | 카드 L37–39, 54, Eq(1) L95 | — |
| D5 | Parks 2023 (*JMCA* 11, 21322) | 4.5 V 충전 후 2차입자 +19 % (최대 +28 %) 팽창 · 균열부피 ~9 % (최대 16 %) | a10_cycle_chemomech_design.md:24 | **V** | 카드 `intergranular_cracking_nmc811_jmca2023` L34, L86–87 | — |

### E. 복합체 σ_e · VGCF (Lee 2025 · Kim 2024/2025 · Kang 2025 · Ozkan · Endo)

| # | 인용 | 붙은 값 / 주장 | 쓰인 곳 | 상태 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| E1 | Lee 2025 (*Nat. Commun.* 16, 4200) | 조성 80:17:3:0.5, 75 MPa DC → σ_e 34 mS/cm (co-roll 33) · PTFE 0.5/2/5 wt% → σ_e 34/4.5/0.011, σ_ion 0.069/0.024/0.007 · LPSCl 2.19 · 제조 500 / 작동 2 MPa · fibril이 계면을 가로지름 | CLAUDE.md:21,300,305 · lee_abs_sigma_e_prereg_20260923.md:21 · sdcp_manuscript_anchors.md:220 · table_s3 문서 (Lee 2025 전체 78줄/37파일) | **V** | 카드 `lee2025_corolling_dryprocess_lpscl_ptfe` L20, 23, 32–35, 38, 45, 55, 61 | — |
| E2 | Lee 2025 (*EES*, dual-fibrous PTFE) | PTFE rope Ø 0.248 µm (→ PTFE_D 0.25) | audit1_ground_truth.md:124 등 | **V** | 카드 `lee2025_dual_fibrous_ptfe_dry_electrode` L20 | — |
| E3 | "Lee 2025 ACS EL" | bimodal P:S 7:3 최적 · 87.8 % @200 cyc | grade_engine.py:294-296,324,434,1159 · GRADING_STORY.md:44 | **M (저자·연도)** | 이 수치는 정본 `oh2026_bimodal_composite_cathode`, 즉 *ACS Energy Lett.* 11, 2103–2114 (2026)의 것이다. L18, L62–63: *"CAM7:3 … 87.80% retention @200 cyc"* | `bd6cb50cc` 05-22 |
| E4 | **정본 카드** `kim2024_carbon_volumetric_occupation_se_domain` L166 | *"자매 논문 Lee 2025 (VGCF 섬유 vs SuperP 구; SuperP 0.0168 < VGCF 0.0298 mS/cm σ_e)"* | 정본 카드 (이 브랜치 동결 스냅샷에서는 L162) | **M (정본 안의 오귀속)** | 이 두 수는 **우리 복셀 σ_ionic 시뮬레이션** 값이다(`docs/cbd_morphology_roadmap.md:145-152`: *"our voxel … VGCF 0.0298 > SuperP 0.0168 … ionic"*). 논문 값도 아니고 σ_e도 아니다. Lee 2025 카드 두 장 어디에도 0.0168/0.0298은 없다 | `18805fa6e` 06-26 → 정본으로 승격 |
| E5 | Kim 2024 (*AFM* 34, 2409318) | σ_e 38.6/54.8/65.2 mS/cm (AM 80/85/90 wt%, C 3 wt%, 517 MPa, DC) · C 1 wt%에서 5.1 (5.08/5.18) · AM 90 wt%에서 σ_ion 0.014 (0.0138) | CLAUDE.md:305 · sdcp_manuscript_anchors.md:222 · week_plan_manuscript_20260825.md:78 · sigma_vgcf_anchoring_program_20260829.md:114 | **V** | 카드 L54, L60, L162 | — |
| E6 | Kim 2024 (*ACS Energy Lett.* DT review) | 리튬화 von Mises 1.10/1.48/2.44/4.19 MPa · "domains of tens of micrometers" | positioning_in_dt_lineage.md:392,405 | **V** | 카드 `kim2024_digital_twin_acsenergyletters` L329–330, L401 | — |
| E7 | Kim 2025 (*Battery Energy*) | SE-SP@CAM 1.0×10⁻⁵ · SE@CAM 3.3×10⁻² · SE-VGCF@CAM 1.4×10⁻² S/cm · CA 2.9 wt% · 370 / 50 MPa · VGCF Ø ~150 nm, L ~10 µm | additives.py:853,855 · grade_engine.py:1687,1754-1755,1806 | **V** | 카드 `kim2025_conductive_agent_se_coating_cathode` L51, 52, 57, 86–89 | — |
| E8 | Kim 2025 (*Electrochim. Acta* 147413, TLM) | R_ct uncoated/coated ~13–20× · 두께 47.5/45/40 µm · 250/433 MPa | coating_presets.py:11,50 · mpm_wallP_conditional_troubleshooting.md:417 | **V** | 카드 `kim2025_impedance_decoupling_tlm_assb` L107, 114, 397. 단, 정적 R_ct 비를 "CEI 성장 억제배수"로 쓰는 것은 해석을 옮긴 것이다 | — |
| E9 | Kang 2025 (*Adv. Mater.*, bollard) | PTFE 전극 σ_e 0.58 S/cm (4-probe, 무가압) | manuscript_sdcp_sigma_e_mechanism.md:428 | **V** | 카드 `kang2025_bollard_anchored_binder_dry_electrode` L83, L150 | — |
| E10 | Ozkan 2010 (*Carbon* 48, 239) | VGCNF 단섬유 E 180 → 245 GPa | si_table_response_20260925.md:157,173 · vgcf_e_sensitivity_prereg_20260925.md:5,42,126 · session_20260923_progress.md:237 | **B** | 논문은 실재한다(Ozkan·Naraghi·Chasiotis, DOI 10.1016/j.carbon.2009.09.011). 값은 검색 요약 — 미확인. 리포도 "PDF 미확인"으로 정직하게 적고 있다 | — |
| E11 | Endo 2001 (*Carbon*, "VGCFs: basic properties…") | 단섬유 저항률 탄화 1e-3 / 흑연화 1e-4 Ω·cm · "Endo 5e-5" | sdcp_manuscript_anchors.md:217 · step3_sigma_network.md:19 · session_20260923_progress.md:240 | **B** (1e-3/1e-4) · U (5e-5) | 논문은 실재한다. 1e-3/1e-4는 검색 요약 — 미확인. 5e-5는 검색에서도 보이지 않았다 | `d7bcc0edd` 08-19 ("Endo 5e-5") |
| E12 | Showa Denko VGCF-H 카탈로그 | 분말 0.012 Ω·cm = 83 S/cm · Ø 150 nm | CLAUDE.md:311 · manuscript_draft/build.js:369 · claims.json CL-47 | **U (문헌 아님)** | 카드가 없다. Ø ~150 nm · L ~10 µm는 Kim 2025 카드 L51로 V가 가능하다 | — |

### F. 기타 배정 키

| # | 인용 | 붙은 값 / 주장 | 쓰인 곳 | 상태 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| F1 | Park 2023 (*AEM* 13, 2203861; LiDFBOP 유래 CEI) | 계면 R ∝ √t (코팅/첨가제) vs 파라볼릭 (bare) · 기울기 25.73 Ω·h^-0.5 | b1_chem_fade.py:26-47,311 · cycle_degradation_law.py:54,119,540 · step5 문서·템플릿 (33줄/9파일) | **B** | 논문은 실재한다(Wiley, 2023-03-09). 리포가 이미 "[B] = search snippet"으로 표기하고 있어 일관된다 | — |
| F2 | Park 2023 (+ Ohno 2020, Yoon 2025) | 황화물 양극 porosity 목표 10–15 % | grade_engine.py:12,100 | **U** | 어느 Park 2023인지 알 수 없다. 위의 CEI 논문과 주제가 다르다 | `41f3a9d9a` 05-20 |
| F3 | Oh 2025 (*MSE R* 164, 100970) | φ(z) 두께방향 전위 그림 "Fig 4e 문법" (수치 귀속 없음) | step3_phi_profile_plot.py:2 · mpm_webapp_payload.py:2292,2393 · viewer3d.js:3374-3432 · rint_anchor_db_research.md:148,167 | **U** | 검색 3회로 찾지 못했다. 정본의 primer 카드는 Nam 2026 *ACS Energy Lett.*로, 다른 논문이다 | `128d3ac50` 07-17 |
| F4 | `docs/paper/main.tex` (05-08 LaTeX 초안) | "five Lawn-stages \citep{Lawn1998} … σ multiplier (1.0, 0.9, 0.5, 0.2, 0.05)" | main.tex:309-312 | **U** | Lawn의 저작이 전도 배수를 준다는 근거가 없다(미확인). 코드의 Stage D 배수 (1.00/0.85/0.40/0.10/0.02)와도 맞지 않는다 | `c66f9ae94` 05-08 |

**키별 한 줄 판정**

| 판정 | 키 |
|---|---|
| **F** | Liu 2020 · Quinn 2020 · de Vasconcelos 2019 · Lim 2018 · Xu 2017 PRX 좌표 · Wang 2020 · Wang 2022 (κ) · Park 2024 · Wang 2023 (의심) |
| **M** | Lawn "1998" 책 서지 · Trevisanello 2021 과잉 귀속 묶음 · "Lee 2025 ACS EL" (→ Oh 2026) · 표 안의 Bielefeld 2020 / Minnmann 2021 / Sakuda 2013 행 · Chen 2020의 k_SEI · CL-50의 Wang 2018 |
| **B** | Xu 2017 JES (단, NMC532) · Lawn 수치 · Chen 2020 · Ozkan 2010 · Endo 2001 · Amin 2015 · Park 2023 √t · Lim 2017 |
| **V** | Wang 2018 · Amin & Chiang 2016 · Kang & Shin 2025 · Kang 2025 bollard · Bucci 2017/2018 · Parks 2023 · Lee 2025 (Nat. Commun., EES) · Kim 2024 · Kim 2025 · Trevisanello의 R_ct·SC D·PSD |
| **U** | Oh 2025 · Park 2023 porosity · Wang 2021 |
| **C** | Auerbach 1891 |

---

## 2. 뿌리 — 검증 없는 귀속이 처음 들어온 커밋

### R0. import 시점 (2026-04-24 `660600a44`)

- `σ_AM = 50 mS/cm (NCM811 literature reference)` / `SIGMA_AM_ELECTRONIC = 0.05`가 이미 있었다. 출처는 적혀 있지 않았다(B5).
- 이때 "Trevisanello"는 Minnmann 2022 인용의 공저자 이름으로만 등장했다. Trevisanello 귀속은 전부 그 뒤에 생겼다.

### R1. `session_01KxPF3N83esrzqzya11hFMK` — 04-29 ~ 05-04, "04-29 배치". 이번 감사에서 F 대부분의 뿌리

| 커밋 | 시각 (UTC) | 들어온 것 |
|---|---|---|
| `00368b5ea` | 04-29 01:20 | SHAPE_FACTOR. **"Quinn 2020", "Liu 2020", "Lim 2017", "Wang 2022" 이름의 첫 등장** (1.40/1.10/1.05, Sakuda 2013 포함) |
| `dba9db01a` | 04:58 | `viewer3d_data.py`: Auerbach와 **Lawn 1998 §3.4 / Table 3.4**, A = 200, δ 배수, K_IC 1.0 (Liu) / 0.3 (Quinn), **E = 150 GPa "Xu 2017 (NCM811 nanoindentation)"** |
| `17e8a6c78` | 05:04 | E_AM 150 → **140으로 값만 변경**, "Xu 2017" 라벨은 유지(→ "Xu 2017 / project-wide convention") |
| `b1c8262fe` | 05:12 | `fracture_model.py` 참고문헌 블록. **가짜 좌표** Nat. Energy 5, 304 / Joule 4, 2466 / Acta Mater. 178, 35 / PRX 7, 041038 / Wang 2020 JPS 470, 그리고 de Vasconcelos |
| `0a040f2b0` | 07:38 | `build_literature_reference.py`. Lim 2018 Nano Lett., 단계 비율 범위, E 130–165, H 5–8, Bielefeld 2020 "JES", Wang 2023 JPS 555, Minnmann 2021 "AEM", Sakuda 3행. 머리말은 *"Sources (all open-access or institutional access)"* — 실재하지 않는 좌표에 "접근했다"고 적었다 |
| `726b6bbb2` | 08:34 | 힘 배수 1/3/11/32, 원고 caveat Section 2 ("Xu 2017, NCM811 nanoindentation") |
| `d68871c70` | 11:34 | 원고 Section 3 검증 표 ("Lim 2018 (implied)", *"independent literature sources … without any per-case fit"*) |
| `573a07187` | 04-30 05:26 | 웹앱 툴팁 (Quinn·Liu·Lim·de Vasconcelos 범위, f 1.40/1.10 "측정값 기반") |
| `4fdfde6e7` | 04-30 10:52 | Stage D σ 배수. **"Trevisanello 2021" 첫 등장** (microcrack 0.85, Heenan 2020과 병기), Jiang 2021 + Wang 2021 (0.40), Min 2024 (0.10) |
| `c5fb6f294` | 04-30 11:47 | Stage E의 AM_P σ_e 0.65 (Trevisanello), κ 0.50 (Wang 2022) |
| `e241675f1` | 04-30 11:50 | 크기표, "Trevisanello reference 5–12 µm", "Wang 2021 SC 1–5 µm" |
| `bd4d6fe0b` | 05-04 | CL-90 원장 기록: Wang 2020 → "NCM E_AM = 140" |
| `148d0f5fb` | 05-04 11:41 | 반박 노트 서지: *Nat. Energy* 5: 304, *Joule* 4: 2466, **Park 2024 AEM 14: 2301245**, ν 0.25 (Xu 2017) |

### R2. 세션 링크 없는 커밋 — 05-06 ~ 05-25, 같은 흐름이 이어짐

| 커밋 | 날짜 | 들어온 것 |
|---|---|---|
| `2900b6b0a` | 05-06 | UI: AM_P 0.65 "Trevisanello", "size-invariant per Wang 2022" |
| `9e24233ef` | 05-06 | f_AM^cc "Trevisanello / Bielefeld 2022" |
| `19e03e9fb` | 05-06 | ASR_th 1–10 "Wang 2022" |
| `c66f9ae94` | 05-08 | LaTeX 초안: refs.bib의 Trevisanello 제목 오기, Wang2022 placeholder, Bielefeld2022 연도 오기, main.tex Lawn 배수 |
| `84573970d` | 05-08 | STAGE_E 가이드: Trevisanello "Adv. Funct. Mater.", "35 % 낮음", Wang 2022 "ESM" |
| `9a13628aa` | 05-13 | Lawn "severe ≤ 50 %" |
| `41f3a9d9a` | 05-20 | Park 2023 porosity |
| `bd6cb50cc` | 05-22 | "Lee 2025 ACS EL" |
| `86e8e35c1` | 05-25 | Trevisanello "1차입자 0.1–1 µm" |

### R3. `session_01AE6H8brQNyGYQLfq4X8Yq7` — 05-28 ~ 06-03, σ_e 폼 확정 과정

| 커밋 | 날짜 | 들어온 것 |
|---|---|---|
| `eed0b9581` | 05-28 | σ_S/σ_P (σ_AM_eff 10/5)를 Trevisanello로 귀속 |
| `a58593227` | 06-01 | "micro-asperity ~60 % (Lawn 1998)" |
| `90a789825` | 06-01 | "Trevisanello 2021 (β=1.5 fixed)" |
| `037316133` | 06-02 | σ_AM 50 "Trevisanello single-crystal" |
| `1547b028a` · `3aa171ed2` · `b4f62e852` | 06-03 | "Trevisanello fit / 측정 / GB scaling", "Trevisanello 10/5" |

### R4. `session_01H191Ni4xzj9H5ftstAm7Ft` — 06-25 ~ 08-19, 이 계열의 세션

| 커밋 | 날짜 | 들어온 것 |
|---|---|---|
| `d47ac4afa` | 06-25 | Oh 2026 Table S15의 시뮬 입력을 "측정"으로 서술 |
| `18805fa6e` | 06-26 | kim2024 카드의 "Lee 2025 0.0168/0.0298" (나중에 정본으로 승격) |
| `128d3ac50` | 07-17 | Oh 2025 MSE R |
| `cf3fa953f` | 07-20 | k_SEI "PyBaMM Chen2020", "SC R_ct ≈40 % 낮음" |
| `0822e6adf` | 07-21 | Kang&Shin "3 µm ~0.4" |
| `181a39718` | 08-19 | CL-50 "Wang 2018 5×10⁻⁵" |
| `d7bcc0edd` | 08-19 | "Endo 5e-5" |

### 뿌리에서 보이는 패턴 (이력 증거)

- **라벨이 값을 따라가지 않았다.** `dba9db01a` → `17e8a6c78` 사이 6분 동안 "Xu 2017"이 150 GPa에서 140 GPa로 옮겨 붙었다.
- **"문헌 배수"가 내부 산술이다.** 힘 배수 1/3/11/32는 δ 배수 1/2/5/10의 3/2승이며, 코드 주석이 스스로 그렇게 적는다.
- **가짜 좌표가 실재 논문과 충돌한다.** Liu 2020의 "5, 304"는 리포 자신이 인용하는 Lee 2020 Nat. Energy 5, 299–308 안에 있다. Xu 2017의 PRX 좌표는 콜로이드 논문이다.
- **같은 세션**이 04-29 하루(01:20–11:34)에 코드 주석 → 문헌 표 → 원고 절로, 이어 04-30 툴팁과 05-04 반박 노트로 자기인용 사슬을 만들었다. 그 결과 원고의 "독립 문헌" 문장이 성립하지 않는다.

---

## 3. 대체 — 정본 카드(V)만. 없으면 "원문 필요"

| 잘못된 귀속 | 대체 |
|---|---|
| K_IC(SC) 1.0 (Liu 2020) · K_IC(PC) 0.3 (Quinn 2020) · 비 2.5–5 | **원문 필요.** 정본에 NCM K_IC 수치 카드가 없다. 방향(단결정이 다결정보다 기계적으로 강함)만 V로 받칠 수 있다: `jung2023_single_crystal_ncm_morphology` L60 *"입자 경도 SC 972.7 / PC ~113.3 MPa (micro-indenter)"*. 단 이것은 K_IC가 아니라 입자 압궤 강도다. (참고: 검색상 후보는 Joule 2022 리뷰 "Mechanical properties of cathode materials for lithium-ion batteries"이며, 카드가 없어 미확인이다) |
| 단계 비율 intact 60–75 / microcrack 15–25 / multi 5–10 / severe 1–5 % (Lim 2018 · de Vasconcelos 2019 · Quinn 2020) | **원문 필요.** 접촉 단위 단계 비율을 주는 정본 카드가 없다. 양이 다른 V 앵커만 있다: `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` L86–87 (압연 후 균열/NMC 7.13 %, 원분말 0.12 % → 압연 기원; 액체 LIB NMC811) · `intergranular_cracking_nmc811_jmca2023` L86–87 (4.5 V 충전 후 균열부피 ~9 %, 최대 16 %) · `lee2025_corolling_dryprocess_lpscl_ptfe` L89 (SI Fig 8: PC는 500 MPa에서 균열 증가, SC는 없음 — 정성). 따라서 "모든 단계가 문헌 범위 안"이라는 비교 형식은 대체물로 유지할 수 없다 |
| Lawn "1998" §3.4 / Table 3.4 — A = 200, 배수 1/2/5/10 → 1/3/11/32, factor-of-two | **원문 필요.** 책 2판은 1993 CUP, 1998은 *J. Am. Ceram. Soc.* 81, 1977이며 둘 다 카드가 없다. 최소한 1/3/11/32는 "1/2/5/10의 3/2승(내부 유도)"으로 표기해야 한다 |
| E_AM 140 GPa ("Xu 2017 NCM811" / Wang 2020) | 측정값은 **원문 필요**(Xu 2017의 실재 대상은 NMC532). 모델 입력 관행으로는 V가 있다: `lee2024_multiphysics_dem_fem_initial_pressure_assb` L61 *"E_CAM (NMC) 144 GPa, stated"* · `bazzoun2025_dem_parameter_sensitivity_assb_cathode` L43 *"E_CAM 161.5 GPa (범위 123–200), stated Table 3"* · `intergranular_cracking_nmc811_jmca2023` L317 *"1차입자 E_p = 150 GPa"* (phase-field 입력). 셋 다 **측정이 아니라 입력값**이다 |
| H_AM 6 GPa / 5–8 GPa (Wang 2020) | **원문 필요.** 정본 모델 관행 `so2022_dem_compaction_coated_particles_assb` L45는 *"H_AM (NCM hardness) 11.2 GPa, Cheng [37], stated Table 1"*이다(재인용이며 우리 6 GPa와 다름) |
| ν_AM 0.25 (Xu 2017) | **원문 필요.** 정본의 모델 입력은 0.30이다(`bazzoun2026_dem_fem_rnm_ionic` L22 *"ν_CAM 0.30"*, Parks L317 ν = 0.3) |
| f_AM_P 1.40 / f_AM_S 1.10 (Quinn · Lim 2017 · Liu · Wang 2022) | **원문 필요.** 참고용 V: Trevisanello L132–137 (PC 구기하 0.17 vs 측정 BET ≈0.2 m²/g) · `jung2023_…` L63 (BET SC 0.23 / PC 0.28 m²/g). 인자 자체는 우리가 유도해야 한다 |
| DEM overlap 규약 (Wang 2023 0.05–0.15 · Bielefeld 2020 5 % cap · Minnmann 2021 0.08) | V: `giannis2021_stress_based_multicontact_dem` L93 *"Hertz theory is applicable only … upper limit of δ/r ≤ 0.1 (10 %)"* (stated) · `so2021_dem_mold_pressure_assb_coldpress` L36 (평형 overlap ratio h_ov/4R_eff 중앙 ~0.07 @400 MPa, SE–SE ≈0.10, AM–AM ≈0.007; digitized) · `bielefeld2019_microstructural_modeling_composite_cathode` L57 (확률 배치의 잔존 AM 겹침 ~1 vol% @65 vol% AM) |
| Sakuda 2013 → LPSCl 단결정 σ · 펠릿 σ · 경도 · 형상 1.05 | 내 범위 밖(Sakuda/Cronau 담당 감사). Sakuda 카드로 쓸 수 있는 것은 "75Li₂S·25P₂S₅ 유리의 E 18–25 GPa(초음파), σ 0.31/0.34 mS/cm"뿐이다 |
| σ_S 10 / σ_P 5 · AM_P ×0.65 · σ_AM 50 (Trevisanello, 또는 출처 없는 "literature") | 값 자체는 "코퍼스 적합 endpoint / 가정"으로 표기한다. 문헌 맥락 V: `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` L20 (NMC811 4.1×10⁻³ S/cm, 20 °C, DC) · `aminchiang2016_nmc_electronic_ionic_transport_vs_li` L62 (5.0×10⁻⁸–1.4×10⁻² S/cm, SOC 의존) |
| NCM(r) β = 1.5 "Trevisanello fit" | Trevisanello 카드 L268–270의 권고대로 쓴다: *"Trevisanello가 보인 '큰 다결정 = 내부GB·표면적 페널티' 정신을 따른 경험 지수 (β=1.5, 우리 corpus fit)"* |
| "Trevisanello reference 5–12 µm" | Trevisanello L260: PC 반경 ≈1–5 µm (중앙 ~2 µm), SC 반경 ≈0.3–1.2 µm |
| 다결정 1차입자 0.1–1 µm (Trevisanello) | `jung2023_single_crystal_ncm_morphology` L66: *"PC 1차입자 크기 ~600 nm (FESEM, stated)"* |
| Trevisanello 저널·제목 | 카드 L14–17: *Adv. Energy Mater.* 11, 2003400 (2021), "Polycrystalline and Single Crystalline NCM Cathode Materials—Quantifying Particle Cracking, Active Surface Area, and Lithium Diffusion" |
| Stage D/E 파괴 σ 배수 (0.85 · 0.40 · 0.10 · 0.02, 그리고 main.tex의 1.0/0.9/0.5/0.2/0.05) | **원문 필요.** 그때까지는 "가정"으로 표기한다 |
| κ 결정립 인자 AM_P 0.50 / 0.30–0.65 · ASR_th (Wang 2022) | **원문 필요.** 정본에 NCM 단결정/다결정 κ 카드가 없다 |
| AM_P 크기인자 0.45–0.75 (Park 2024) · "SC 1–5 µm σ 일정" (Wang 2021) | **원문 필요** |
| "SC R_ct ≈40 % 낮음" | 정본에는 반대 방향이거나 정성적 내용만 있다: Trevisanello L189–194 (액체: PC R_ct 70→15 Ω, SC는 증가), Oh 2026 L287 (단결정만인 전극의 계면 D2 매우 큼). 수치는 **원문 필요** |
| CL-50 "Wang 2018 NMC bulk 5×10⁻⁵" | `wang2018_…` L25 (그 값 없음) → 실제 값은 Wang 2018 NMC811 4.1×10⁻³ S/cm (20 °C, L20) |
| "Lee 2025 ACS EL" (87.8 % @200 cyc, P:S 7:3) | `oh2026_bimodal_composite_cathode` L18, L62–63 — *ACS Energy Lett.* 11, 2103–2114 (2026) |
| 정본 kim2024 카드의 "Lee 2025: SuperP 0.0168 < VGCF 0.0298 mS/cm σ_e" | 실험 방향은 V: `kim2025_conductive_agent_se_coating_cathode` L86–90 (σ_i SE-SP@CAM 0.9×10⁻⁴ < SE-VGCF@CAM 1.6×10⁻⁴ S/cm; σ_e 1.0×10⁻⁵ vs 1.4×10⁻² S/cm). 0.0168/0.0298은 "우리 복셀 σ_ionic"으로 다시 표기해야 한다 |
| Chen 2020 값들 (5.22 µm · 4e-15 · 63104 · 3.42e-6 · OCP · 창) | **원문 필요.** 논문 카드가 없고, 현재 근거는 PyBaMM 소스 일치(B)뿐이다 |
| k_SEI 1×10⁻¹² m/s (PyBaMM Chen2020) | **원문 필요.** PyBaMM이 가리키는 출처(Ramadass2004 · Ploehn2004 · Single2018 · Safari2008 · Yang2017)의 카드가 없다 |
| Kang & Shin "3 µm ~0.4" | 카드 L72의 *"3 µm는 낮음"*으로만 쓸 수 있다 |
| Oh 2025 MSE R · Park 2023 porosity 10–15 % | **원문 필요** (서지부터 확인) |
| VGCF 단섬유 E 180–245 GPa (Ozkan) · 저항률 1e-4 / 5e-5 Ω·cm (Endo) · 카탈로그 0.012 Ω·cm | **원문 필요** (카드 없음). VGCF-H 기하 Ø ~150 nm · L ~10 µm만 V: `kim2025_conductive_agent_se_coating_cathode` L51 |

---

## 4. 부수 발견·주의

1. **정본 카드도 틀릴 수 있다 (E4).** `kim2024_carbon_volumetric_occupation_se_domain` L166은 우리 시뮬레이션 값을 다른 논문의 다른 채널 값으로 적고 있다. 정본 카드를 V의 근거로 삼을 때도 카드 안의 **남의 논문 언급**은 V가 아니다.
2. **원장 `CL-50`(live) 잔존 (B17).** 원고 생성기 `build.js`는 09-25에 정정됐지만 원장 본문은 그대로다. `si_table_response_20260925.md`는 이를 "비준 대기"로 기록하고 있다.
3. **`CLAUDE.md:2311, 2313`의 "Trevisanello 10/5" (B1)** — A1 정정(06-30)에서 빠진 잔존분이다.
4. **`docs/paper/` (05-08 LaTeX 초안)에 서지 오류 셋과 배수 불일치 하나가 있다.**
   - refs.bib의 Trevisanello 제목이 틀렸다.
   - Wang2022는 placeholder다.
   - Bielefeld2022는 2019 논문의 연도를 잘못 적었다.
   - main.tex의 Lawn 단계 σ 배수(1.0/0.9/0.5/0.2/0.05)가 코드 Stage D(1.00/0.85/0.40/0.10/0.02)와 다르다.
5. **`paper_brittle_caveat.md` 검증 문장.** *"Every stage falls within the experimentally observed range … This agreement is not obtained by parameter tuning: K_IC, E, and the Lawn multipliers were taken from independent literature sources (Liu 2020, Quinn 2020, Xu 2017, Lawn 1998)"*는 근거가 전부 F/B/M이므로 문장 자체가 철회 대상이다. 같은 문서 L44의 "typical literature DEM values 0.05–0.15 (Wang 2023; Minnmann 2021) and an explicit cap of 0.05 in Bielefeld 2020"도 A17–A19에 따라 성립하지 않는다.
6. **정정 범위.** 부모 세션의 SELF-51 커밋(`171934433`, `b037d765c`)은 Xu 2017 좌표, Wang 2020, σ_grain 출처를 고쳤다. 그러나 같은 04-29 블록의 Liu 2020 · Quinn 2020 · de Vasconcelos 2019 · Lim 2018 · Lawn §3.4/Table 3.4 · Bielefeld/Wang 2023/Minnmann/Sakuda 행은 그대로다. 같은 배치이므로 같은 처리가 필요하다.
7. **내 키 밖이라 판정하지 않은 것.**
   - Heenan 2020 (*AEM* 10, 2002655): 실재 확인(B), 0.85 배수의 근거인지는 미확인.
   - Jiang 2021 · Min 2024 · Tanaka 2017 · Yang 2022 (반박 노트의 κ SE) · Sun 2017 · Ryu 2018 (main.tex): 미조사.

---

## 5. 검색 출처 (존재 확인용; 숫자는 모두 "검색 요약 — 미확인")

- Nat. Energy 5, 299–308 (Lee Y.-G. 외 2020): https://www.nature.com/articles/s41560-020-0575-z
- Quinn 외 2020, *Cell Rep. Phys. Sci.* 1, 100137 (EBSD): https://www.sciencedirect.com/science/article/pii/S2666386420301417
- Joule 4권 11호 (2237–2522쪽): https://www.sciencedirect.com/journal/joule/vol/4/issue/11
- Xu, Sun, de Vasconcelos, Zhao 2017, *JES* 164, A3333: https://iopscience.iop.org/article/10.1149/2.1751713jes
- Phys. Rev. X 7, 041038 (콜로이드 확산영동): https://doi.org/10.1103/PhysRevX.7.041038
- de Vasconcelos 외 2019, *Exp. Mech.* (in-situ nanoindentation): https://link.springer.com/article/10.1007/s11340-018-00451-6
- Lim 외 2017, *Sci. Rep.* 7, 39669: https://www.nature.com/articles/srep39669
- Lawn, *Fracture of Brittle Solids* 2판 (CUP 1993): https://www.cambridge.org/core/books/fracture-of-brittle-solids/B1EC1413BDBA1DCF49E1665D4B0A20F3
- 8장 Indentation fracture: https://www.cambridge.org/core/books/abs/fracture-of-brittle-solids/indentation-fracture/FC23138EFA9742E00DC36C0F2BE2F83A
- Lawn 1998, *J. Am. Ceram. Soc.* 81, 1977: https://ceramics.onlinelibrary.wiley.com/doi/pdfdirect/10.1111/j.1151-2916.1998.tb02580.x
- Auerbach 1891: https://onlinelibrary.wiley.com/doi/10.1002/andp.18912790505
- Ozkan 외 2010, *Carbon* 48, 239: https://www.sciencedirect.com/science/article/abs/pii/S0008622309005788
- Endo 외 2001 VGCF: https://www.sciencedirect.com/science/article/abs/pii/S0008622300002955
- Chen 외 2020, *JES* 167, 080534: https://iopscience.iop.org/article/10.1149/1945-7111/ab9050
- Amin & Chiang 2016: https://iopscience.iop.org/article/10.1149/2.0131608jes
- Amin 외 2015 (NCA): https://iopscience.iop.org/article/10.1149/2.0171507jes
- Park 외 2023, *AEM* 2203861: https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aenm.202203861
- Heenan 외 2020, *AEM* 2002655: https://advanced.onlinelibrary.wiley.com/doi/10.1002/aenm.202002655
- Joule 2022 리뷰 (대체 후보, 미확인): https://www.cell.com/joule/fulltext/S2542-4351(22)00139-8
- Primer 논문 (Nam 외, ACS Energy Lett. 11, 5149): https://pubs.acs.org/aelccp/article-abstract/11/7/5149/5169903/Revisiting-Primer-Layer-Design-for-Robust-Dry?redirectedFrom=fulltext
