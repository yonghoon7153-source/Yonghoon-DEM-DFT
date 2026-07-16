# 📚 LITDB — DEM+MPM ASSB 압밀·전달 문헌 인덱스

> 갱신: 2026-07-16 (+**📌 Li(Yang) 2026 ECER 심사중 원고 — 황화물 ASSB 안정성 총설, 사용자 요청 최상단 고정**). 이전 2026-07-10 (+**★★ Duquesnoy 2023 (Franco/ARTISTIC) = 우리 5-Phase 비전의 published archetype** — 물리시뮬→Sobol DOE→SISSO→베이지안 다목적최적화→실험검증; §LIB 제조 DEM 섹션). 이전 2026-07-08 (+Kang(Jihyeon)2025 bollard-anchored binder + Han2025 ICEP 이온전도 탄성 binder digest — 전도성-바인더 자매 2편, SDCP 앵커). ★ **종합 리뷰(60편) = `docs/literature_review_dem_mpm_assb.md`** (분류표 + 섹션별 review +
> DEM/MPM 적용리스트 + MPM 수식계보 + Stage-2 닫음 + 결론).  각 논문 상세는 `papers/<slug>.md` (digest), 우리 대비는 `comparison_vs_ours.md`,
> 기준값은 `our_dem_baseline.md`. 수치 CSV는 `docs/data/<slug>_*.csv`.

Status 범례: ✅ digest 완료 · ⬜ PDF만(미digest) · 📄 메타만

## 📌 최상단 고정 (사용자 요청 2026-07-16) — 황화물 ASSB 안정성 총설 리뷰 (심사중 원고)

> ⚠ **PROVENANCE: 미출판 심사중 원고** — Electrochemical Energy Reviews 투고 원고 **ECER-D-26-00097**
> (Editorial Manager 4분할 PDF 113p, `docs/literature_coverage/pdfs/Li_2026_ECER-D-26-00097_*_part1..4.pdf`).
> 인용은 "manuscript under review"로만; **수치는 대부분 2차인용** → 실제 cite는 digest §3 표의 1차문헌(ref#)으로.

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **📌 Li (Yang) 2026** (USTB Fan Li-Zhen* + Tsinghua Nan Ce-Wen) | **ECER-D-26-00097 (심사중 Review)** | 황화물 SE 전반(LPSCl·LGPS·Li₇P₃S₁₁·Li₃PS₄) vs oxide/polymer/halide + NCM/신규 CAM/음극 전군 | ★ **안정성 총설(재료물성→전극계면)**: 고유 5축 — 공기(H₂S/HSAB·E_ad LPSC −1.63→LPSOCF −1.19 eV) · 용매(극성/donor-number 공격→건식 정당화) · 열(고유 400–500 °C ↔ NCM O-방출 200–300 °C; **성형압↑→계면 P₂Sₓ층→발열 −40–50 %**) · 전기화학(**LGPS 창 1.7–2.1 V·산화 ~2 V**; SCL은 부차·부산물이 직접) · **기계(E 10–30 GPa·K_IC 0.2–0.4 MPa·m^½·임계입경 ~3 µm↔서브µm 협조변형)**; 양극계면 4겹(산화분해→O-방출 양방향→준위/SCL→**chemo-mech 균열**) + 전략(조성 이온-전자 균형[143]·**carbon 부피점유[147]=우리 랩 Kim2024 인용!**·구배[149,152=A7]·압력→porosity↓접촉↑but tortuosity↑이방[151]·코팅 t/σ 딜레마[154]·신규 CAM 할라이드/FeS₂/S-Se); 음극계면(덴드라이트 wedge-opening[177]·**stack-pressure 창 void 수축/안정/성장 상도[188–191]**·CCD·흑연 결정도·Si 300 %·합금 σ_y-정합 압력[210 상대밀도 vs σ/σ_y]·인공 SEI/LiF); 미래 4(고유안정·동적계면·**저압/무가압**·표준화); 면용량 1–2→**>3 mAh/cm²**(SDCP 3.18 위치); 239 refs·Fig 26 — 구조→수송 정량은 [140 Bielefeld,150,151,152] 4편 인용뿐 = **우리 파이프라인 공백 증명** | review (원고; 자체 sim/exp 없음) | ✅ | `li2026_sulfide_stability_review_ecer` |

## ★★★ 필독 / MUST-READ (랩 자체 논문 — 모델 trend 기준) ★★★

> **우리 랩(Hanyang, Jong-Won Lee) 논문 7편 — 모델이 따라가야 할 실험 trend의 기준점.** 우리 DEM+MPM은 이들이
> 정하는 실험 방향에 정렬해야 한다.
>
> ★ **랩 DEGRADATION-MAP (Yun2023 capstone이 통합 — 2축 × 균열 3-driver):**
> - **계면반응 축 (R_int↑, 황화물 산화분해):** Yun2023(LPSCl=계면반응) · Kim2025(R_ct ~20×, 정밀 TLM) · Cho2024(도전재 매개)
> - **이온수송/기계 축 (R_ion↑·균열):** Yun2023(LIC 할라이드=압력하 SE균열) · Kang2025·Kang2023(NCA 입계균열)
> - **균열 3-driver:** **크기**(Kang2025, 큰 10µm 입자) × **음극strain**(Kang2023, Li-In ΔP) × **결정도**(Jung2023, PC>SC)
> - **입자 기반:** Jung2023 단결정 SC-NCM (CAM균열 배제 → SE 열화 분리)
> 같은 황화물-계면 산화분해가 *균열*(Kang)·*R_ct↑*(Kim/Cho)·*SE균열*(Yun-LIC)로 발현.  공통저자 사슬(Junhee Kang·
> Siwon Kim·Hong Rim Shin)이 hub.  ⇒ **우리 DEM+MPM = 그 *구조→수송 σ* 절반** (structure-σ=우리 / mechanics=Kang·Jung /
> kinetics=Kim·Cho / 종합=Yun).  ★ **우리 미보유(frame[5] 공백): SE 취성균열·R_ct/C_dl/확산·사이클 chemo-mech**
> (backlog D6 + A1; `papers/yun2023_*` 종합).

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **⭐필독 Kang & Shin 2025** (Jong-Won Lee 그룹, Hanyang + Samsung SDI) | ACS Appl. Mater. Interfaces 17, 60558 | **NCA LiNi₀.₈₈Co₀.₀₉Al₀.₀₃O₂ + LPSCl + Super P** (72:27:1 wt%) | ★★ **랩 trend 기준.** bimodal(3+10µm) NCA = 패킹↑(펠릿 0.74→0.68mm·부피로딩 1.1×·R_ele 33.9 Ω·cm² 낮음) **BUT 큰 10µm 입자 사이클 균열** → 유지 **47.7%(B)/67.3%(U)@100cyc**; 균열 driver = **NCA/LPSCl 계면분해→Li 농도·응력 *구배*(c_Li 구배 10µm이 3µm 대비 ~10×), 큰 입자일수록 심함**; ★**가압(stack 200/fab 400MPa)응력(수백 MPa)≪확산응력(GPa)→압력 균열기여 미미**; FEM = **Voronoi 다결정 + cohesive-zone damage(0→1)**, ε_d=Ω/3·Δc_Li(Ω=5.9% 부피변화); **E_NCA=175·E_LPSCl=22.1**(=Bazzoun/우리24); EIS-TLM **R_ion 불변·R_int(113→502)·R_w(70→353) 급등**=균열 시그니처; **LZO 6–8nm 비정질 코팅**→XPS 부산물(Li₂Sₙ163.0·PO₄³⁻134.4eV) 억제·120cyc 안정·R_w +1.2만(50→100) | exp + FEM (electrochemo-mechanical) | ✅✅ (가장 자세) | `kang2025_toughened_bimodal_nca_lzo` (papers) + `docs/data/kang2025_bimodal_nca_lzo_anchors.csv` |
| **⭐필독 Kim, Kang, Park, Lee 2025** (Jong-Won Lee 그룹, Hanyang; **Junhee Kang = Kang2025 공통저자 = 자매논문**) | Electrochim. Acta 542, 147413 | **NCM811 LiNi₀.₈Co₀.₁Mn₀.₁O₂ + LPSCl + Super P** (62:37:1/72:27:1/82:17:1 wt%) + 할라이드 **LZC Li₂ZrCl₆** | ★★ **랩 trend 기준 — *EIS-TLM 임피던스 분해*의 방법론 기준점 (Bazzoun·Minnmann 에 이은 3번째 TLM 앵커 + SAME LAB).** **modified TLM**(두 레일 z₁이온/z₃전자 + crossrail z₂계면 사다리망)으로 **Li⁺/전자 수송·계면 전하전달 R_int(=R_ct)·이중층 C_dl·고상확산(Warburg) 을 *동시 분해*** (= 우리 Kirchhoff/Holm σ-솔버의 실험 카운터파트, 단 우리는 z₁만 계산 → R_ct·C_dl·확산은 **우리 미보유 칸**); **2 BC**(ion-block=전하전달 X·이중층만 / e-block=전하전달 O·R_ct 분리); **bulk σ_ion LPSCl 1.6 = Minnmann 1.6**(신뢰보강)·**LZC 할라이드 0.51**(낮은 σ·안정 계면); ★**GB 가 bulk 와 동급/더 큼**(R_i,bulk 9.3 vs R_i,gb 25.6 @62wt%)+온도 더 민감 = 우리 Cronau(r_SE) GB 인자 정당화; ★**uncoated R_ct = LNO-coated 의 ~20×**(62: 22→453 Ω·cm²)=NCM811/LPSCl 산화분해 = **Kang2025 분해→균열의 *kinetics* 짝**(같은 계면, 역학 vs 반응속도); **82wt% 최저 R_ion·R_ct·R_w**(densify+electroactive area↑); ★**T-스윕 E_a 서열 R_ct≫GB>확산>bulk**=우리 *미보유* 온도축; 할라이드 LZC=낮은 σ·낮은 R_ct(안정)=**Varkey halide cross-check** | exp + equivalent-circuit (modified TLM) | ✅✅ (가장 자세) | `kim2025_impedance_decoupling_tlm_assb` (papers) + `docs/data/kim2025_tlm_kinetics_anchors.csv` |
| **⭐필독 Kim 외 2024** (Lee+Sun+Cho; Hanyang+KETI) | Adv. Funct. Mater. 34, 2409318 | NCM + LPSCl + 도전carbon | ★ **도전 carbon이 SE domain 부피점유**(ρ0.67≪SE1.86)→SE분율↓·σ_ion≈1/10@>90wt%AM + carbon표면 LPSCl 산화분해; **σ_e↑/σ_ion↓ trade-off**; **fiber>sphere**. = 우리 CBD/Stage-2(A3/A4)·Bielefeld2020 실험앵커 | exp | ✅ | `kim2024_carbon_volumetric_occupation_se_domain` |
| **⭐필독 Cho 외 2024** (Lee; Kang2025 ref[13]) | Electrochim. Acta 481, 143990 | NCM811 + LPSCl + VGCF + 할라이드 LZC | ★ **VGCF 양면성**(임피던스 분해): 저-f_AM σ_e↓이득 ↔ **고-f_AM(88wt%=SE-poor) σ_ion차단·tortuous·SE-resistive상**→유해; LZC 완화. = σ_e/σ_ion trade-off + Kim2025 TLM 자매 | exp | ✅ | `cho2024_conflicting_roles_conductive_additive` |
| **⭐필독 Kang 외 2023** (Lee; ref[27]) ⚠1저자 **Kang**(slug kim2023) | Energy Storage Mater. 63, 103049 | NCA + LPSCl + Li-In/LTO | ★ **고-strain 음극(Li-In ΔP±3.8MPa)→dynamic 접촉→NCA/LPSCl 이종성→입계균열**(Li-In 붕괴 vs LTO 75.6%/200cyc); Kang2025의 *외부* 균열driver 짝; **E_LPSCl=22.1 출처**; R_int5.9×·R_w8.1× | exp+FEM | ✅ | `kim2023_chemomech_failure_highstrain_anode` |
| **⭐필독 Jung 외 2023** (Lee+Cho+Park; ref[30]) | Chem. Eng. J. 470, 144381 | **SC vs PC NCM**(Ni0.82) + LPSCl | ★ **단결정 SC(monolith·GB-less·경도8.6×) > 다결정 PC(GB+void=병목+균열)**: 5C유지 74 vs 41.6%. = 우리 **AM_P/AM_S(다/단결정) 구분 + Auerbach 결정도축 + σ_e Trevisanello GB** 실험근거 | exp+FEM | ✅ | `jung2023_single_crystal_ncm_morphology` |
| **⭐필독 ★최애 Yun 외 2023** (Lee+Moon; **capstone**) | Energy Storage Mater. 59, 102787 | SC-NCM + LPSCl vs 할라이드 **LIC**(Li₃InCl₆) | ★★ **degradation 종합편**: 임피던스 분해로 **LPSCl=계면반응(R_int+187%) · LIC=이온수송(압력하 SE균열, modulus41→20GPa)** 분리 → 랩 6편을 *2축 degradation-map*으로 통합; SSRM/FS + FEM SE-균열; E_LPSCl 22.1~32.8 범위 | exp+FEM | ✅✅ | `yun2023_deciphering_degradation_halide_vs_sulfide` |

## DEM/MPM 압밀 · 전달 (composite ASSB)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **Lee 2025** | Nat. Commun. 16, 4200 | **LPSCl + NCM811/82 + VGCF + PTFE** (= 우리 소재·도전제 전부) | **실험**(no sim) **건식 co-rolling 박막**(SSE 50µm + 양극 80wt%AM 5mAh/cm²); ★★**저작동압 2 MPa>80% 500cyc**(75 MPa>95%) = robust 융합 계면(계면 void 75→2 MPa: free 4.0→15.5 vs co 1.9→3.5); 제조 500 MPa·작동 2/5 MPa **명시 분리**(=fab-vs-operating, Doux/Minnmann 합류); ★PTFE 0.5/2/5 wt%→σ_e 34/4.5/0.011·σ_i 0.069/0.024/0.007; ★binder-VGCF fibril망(=우리 CBD); ★PC-NCM 깨짐/SC-NCM 무손상; 310 Wh/kg·805 Wh/L | exp | ✅✅ | `lee2025_corolling_dryprocess_lpscl_ptfe` (papers) + `docs/lit_lee2025_corolling_dryprocess_assb` (공정/압력) |
| **Bazzoun 2026** | J. Power Sources 661, 238682 | **LPSCl + NMC811** | DEM+FEM+RNM σ_eff,ion; 실험 0.137/0.101/0.065 mS/cm @f_CAM 70/75/80; RNM=Holm/Kirchhoff; E_SE=22.1 | DEM+FEM+RNM | ✅ | `bazzoun2026_dem_fem_rnm_ionic` |
| **Varkey 2026** | Adv. Powder Tech. 37, 105338 | halide Li₃YBrCl₆ + NMC811 | multi-contact 탄소성 DEM; separator floor 21% / cathode 37% @350MPa; E_SE=10.58; CONTACT-소성만(구) | DEM | ✅ | `varkey2026_multicontact_elastoplastic_dem` |
| **So 2021** | J. Power Sources 508, 230344 | LPS(Li₂S–P₂S₅) + Si음극 | 3D DEM(소성 cold-press, **H-cap real E=24**); rel.density 0.30→**0.98**@600MPa, φ_SE^crit=0.13, AM-AM 응력 5.9 GPa | DEM | ✅ | `so2021_dem_mold_pressure_assb_coldpress` |
| **So 2022** (Magnus So, Kyushu — So2021 자매 방법론편) | MethodsX 9, 101857 (OA) | **LPS/LiCoO₂ ASSB** | ★ **DEM 접촉LAW 정의편(So2021 짝).** rate-기반 소성/점탄성(Maxwell h_eq) + **경도캡 F_th=H·A_con** + **소결 fusion-bond** + porosity→0 특이점 막는 **area/spring factor**. 우리 대비 **transport 솔버 0**(σ 없음); ★그들 우위 = **소결 + 점탄성 creep**(우리 미보유) + 경로A LAW 완전스펙. ⚠Table1 E_AM 오라벨(199 GPa=LiCoO₂, LPS 아님) | DEM (ASSB 압밀+소결) | ✅ | `so2022_dem_contact_model_assb_compaction_sintering` (+CSV) |
| **Huang 2025** (Surrey, C-Y Wu) | J. Energy Storage 114, 115692 | **LCO + LLZO (산화물)** | ★ **DEM(Hertz 강체구) microstructure + 3D Lattice-Boltzmann 열전도** → ETC 0.41–4.02 W/m·K; porosity/부피분율/입경 결정·tortuosity 비무시 → **3차 다변수(3-τ) 회귀 R²=0.985**(단일 scaling 불가)·EMT 실패 ±28–61% = 우리 **multi-pathway σ_thermal 독립 교차검증**(다른 방법+산화물, frame[4]). 우리 대비 = 우리 σ-삼중항 1채널(Kirchhoff/Holm)+즉시 Ridge predictor(LOOCV 0.90), 그들 thermal-only LBM 재계산; 그들 우위 = 공간 온도장(hotspot map). ⚠산화물≠황화물(절대 ETC 전이금지) | DEM+LBM (thermal) | ✅ | `huang2025_dem_lbm_heat_conduction_composite_cathode` (+CSV) |
| **Martin & Bouvard 2003** | Acta Mater. 51 | soft+hard 구 혼합 | DEM 냉간압밀; 2-메커니즘(force-network K_h + excluded-volume 과변형), Storåkers 소성접촉, 거시응력 E₂/E₁=10→100서 <3% | DEM | ✅ | `martinbouvard2003_dem_composite_cold_compaction` |
| **Bouvard 2000** | Powder Technol. 111, 231 | 경(세라믹)+연(금속) 혼합 | 압밀 2체제(재배열/연-변형) + percolation 임계 vs 크기비(0.32@r=1→0.18@r=2); SE+AM dip 원형 | exp+theory | ✅ | `bouvard2000_hard_soft_powder_densification` |

## LIB 제조 DEM + LIGGGHTS 레퍼런스 (제조공정 peer — 이온위상 역전 / frame[5] 독립확인)

> ★ **모두 강체구 + 접촉소성만(형상소성 無) = frame[5] 독립확인**(우리 MPM이 메우는 *형상-morphology 절반*이 LIB-DEM peer 전체에 빠짐).  이온위상 역전: LIB는 pore=전도체(Bruggeman, 압밀↑→σ↓), 우리 ASSB는 SE망=전도체(Holm, 압밀↑→σ↑).

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **★★ Duquesnoy 2023** (Franco/ARTISTIC, Amiens; = 우리 5-Phase 비전의 *published archetype*) | Energy Storage Mater. 56, 50 | **NMC111 LIB 습식** 양극(+CBD) | ★★ **우리 프로젝트 전체(설계수치→ML full-metric 예측→미세구조→최적화/역설계→실험)를 *한 논문에* 구현.** 물리시뮬(**CGMD 슬러리→CBD-shrink 건조→DEM 캘린더링**, LAMMPS)→**Sobol(+Saltelli) DOE**(174건 space-filling)→**SISSO**(symbolic regression: 물성=Σc_i·d_i, 3-descriptor, l₀; 각 물성 R² **0.91–0.985**)→**베이지안 다목적최적화**(GP + **GP-Hedge**(LCB+EI+PI) acquisition + 스칼라화 **C_f=¼[Σy²_min+Σ(1−y)²_max]**, 등가중, 300-iter)→역설계 **최적 AM/SC/CD = 90.4/58.1/28.4 %**(min τ·max σ_e·max active-surface·max density)→**실물 전극 제작·EIS 검증**(calendered 30 %: density 2.6·τ 1.8·porosity 29 %). ★ 입력=**AM%·SC%(슬러리 solid content)·CD%(두께감소율=우리 λ_dz)**; 물성추출=**TauFactor(τ)·GeoDict(σ_e 연속체)·Python(active-surface AM-pore·porosity)**. ⚠**LIB 습식→이온위상 반전**(pore=이온전도체, τ가 이온 proxy — σ_ionic/σ_thermal·접촉망·MPM 소성 morphology **없음**)=frame[5] 거울(**그들=최적화 loop 소유 / 우리=구조→σ 기계론 소유**). rigid-구형 캘린더링(형상소성無)=Varkey/Bazzoun와 같은 frame[1] 3중확증. ⇒ **흡수 1순위: Sobol DOE·SISSO 폼-교차검증·GP-Hedge BO·스칼라화 = Phase 3–5 청사진** | mixed (CGMD+DEM sim + SISSO ML + 베이지안 다목적최적화 + exp) | ✅✅ (가장 자세) | `duquesnoy2023_ml_multiobjective_manufacturing_optimization` (papers) + `docs/data/duquesnoy2023_manufacturing_optimization.csv` |
| **Sangrós 2019** (TU-BS; Sangrós 2020 Part-I 선행) | Powder Technol. 349, 1 | NMC111 LIB | ★ **Thornton–Ning 탄소성 접촉(항복비 YR=8.59e-3·x **나노압입 측정** R²=0.89) + 명시 binder BOND** → 캘린더링(porosity 0.522→0.217, ≤15%)·CN·broken-bond·**점탄성 spring-back ~17%**(실험 불가측). **전도도 솔버 0**(σ는 2020). 우리 대비 σ-삼중항·MPM 형상소성 부재. ★그들 우위: 나노압입-앵커 **항복캡 LAW(eqs1-6 = 경로A LIB 선례)** + binder bond(A3) + spring-back | DEM (mech-only) | ✅ | `sangros2019_dem_calendering_lib_electrode` (+CSV) |
| **Lyu 2025** (Shanghai U.) | Int. J. Electr. Power Energy Syst. 165, 110521 (OA) | NCM811 LIB | ★ **3D DEM 건조+캘린더링 연속**(solvent=fluid-substitution, **CBD=moment 전달 parallel-bond**) → 3단계 건조·calender porosity 57→22%·σ_zz≈−165<σ_xx −130 MPa. **수치 σ 0**(정성 σ_e만). 우리 대비 Kirchhoff/Holm 삼중항 = peer 중 최대 transport 격차. ★그들 우위: 건조/solvent + CBD parallel-bond(A3 청사진, PTFE 굽힘강성 최적합) | DEM (drying+calendering) | ✅ | `lyu2025_3d_dem_drying_calendering_lib` (+CSV) |
| **Shenouda 2020** (LLNL) | LLNL-TR-813736 | 금속분말 AM | ★ **LIGGGHTS-PUBLIC 튜토리얼 + AM 분말유동**(angle-of-repose vs CED, R²=0.98). 순수 Hertz(소성無)·transport無·접촉망 dump 없음. 우리 코드 입문 레퍼런스; 차용가능 `fix check/timestep/gran`·`move/mesh wiggle`(진동치밀화). corpus 최대 novelty 격차(튜토리얼) | DEM (LIGGGHTS tutorial/AM) | ✅ | `shenouda2020_dem_metal_powder_am_liggghts_tutorial` |
| **Bosch Padrós 2014** (Swansea MSc) | MSc thesis (ZC2E) | 모래/일반 | LIGGGHTS 접촉이론(Hertz/JKR/DMT eqs)+정성 검증(sand-impact·drum); SJKR(=우리 --coh). 가역 Hertz(우리 hooke/hysteresis 아님)·transport無·소성無·DEM/FEM 커플링 **미달성(저자 명시)** = 우리 7 differentiator의 *baseline-floor* 대조 | DEM (LIGGGHTS MSc) | ✅ | `boschpadros2014_dem_liggghts_msc_thesis` |

## 구조-모델링 peer (microstructure generation + percolation/접촉 — 우리 DEM 구조 파이프라인의 직접 비교)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **★ Bielefeld 2019** | J. Phys. Chem. C 123, 1626 | NCM-811/622 + LPS (사실상 재료-무관: shape/size/overlap만) | ★ **GeoDict 구조-모델링 (Janek 그룹) — 우리와 *가장 가까운* 구조-모델링 peer.** **stochastic placement**(AM 구 no-overlap + SE polyhedra overlap, 사후 겹침조정) → **Hoshen-Kopelman** percolation(이온/전자 cluster)·utilization·active interface.  ★ **σ는 *안 풂*(percolation 존재+cluster 부피까지; constriction=ref36 Greenwood future work)**·**단봉 PSD**(bi/tri-modal 보류)·porosity/조성/입경=*입력*.  p_c(전자)=**7.83·ln(d)+36.67 vol%**(Fig6)·β=**0.41**(3D site-perc, Fig4)·이상조성 **62/38·66/34·72/28 vol%@porosity 5/10/20%**·전자한계<69·이온한계>79 vol%(Fig7)·good-perf porosity **~21%**(Fig9, ≠압밀floor 의미). carbon-free(=Strauss ref13). ⇒ **top-down/placement** — 우리 bottom-up/압축+σ삼중항+MPM이 *비운 칸* 채움; Bazzoun2026(같은 그룹 RNM σ)이 후속으로 σ 추가.  ★ **backlog-B3 verbatim 확인**(β=0.41 Fig4·p_c=7.83·ln d+36.67 Eq8). ⚠β=0.41은 *3D-perc strength* 지수 = universality-class만; 우리 √(φ−φc)의 0.5(mean-field)와 동일시 금지 | continuum (GeoDict, voxel percolation) | ✅(papers, docs 노트 대체) | `bielefeld2019_microstructural_modeling_composite_cathode` (papers; 레거시 dup `docs/lit_bielefeld2019_microstructural_modeling_composite_cathodes.md` 대체) + `docs/data/bielefeld2019_percolation.csv` |
| **★ Bielefeld 2020** ⚠(위시리스트 "2022"=오기, 실제 **2020**) | ACS Appl. Mater. Interfaces 12, 12821 | NCM811 + LPSCl(σ_bulk 2.7 mS/cm); σ-검증계는 LCO+LGPS | ★ **Bielefeld 2019의 *σ-추가 후속편*(같은 1저자·GeoDict).** 2019가 미룬 **σ_eff,ion + τ²**를 GeoDict **flux-PDE**(EJ-HEAT 연속체, ∇·(−σ∇φ)=0)로 *풀고*, ★ **바인더(CBD) 영향**(SE 이온망 차단)까지 추가.  ★ σ-method = **연속체 flux-PDE** → **point-contact constriction(Holm/Greenwood) *없음* = σ 상한**(AM/SE 면접촉저항 40 Ω·cm²만; SE-SE 좁힘 빠짐); Bazzoun/우리가 constriction 되돌림.  σ_eff 0.07–0.62 mS/cm·**Kato재구성 0.68 vs 실측 0.73**(검증 1점, LCO+LGPS)·τ² 2→10·**Bruggeman 4× 과소**(Fig2, =우리 R_brug 근거)·**5% void가 20% void 대비 σ 2×**(Fig4)·작은 AM→σ↓τ²↑(이온 장애물; 우리 작은 SE→σ↑와 *반대 채널·같은 그림*).  ★ **바인더 V(B):V(AM) 0.05/0.10 → σ_eff급감·τ² 4.2→6.4→10·active interface −17~43%/−29~82%(고-AM 비선형)**(Fig5, interfacial meniscus 배치) = 우리 CBD/voxel σ-블로킹(SuperP 0.0168<VGCF 0.0298)·#271 Hong PTFE·Lee2025 직접 cross-check.  단봉+trimodal 1케이스(1:1:2 de Larrard) → **dip 미측정**(porosity 15% 고정). C-rate Table1(SE<5 mS/cm thick 불가, 타깃 10). ⇒ **그룹-진화 가운데토막: 2019(σ없음)→2020(연속체σ+바인더)→Bazzoun2026(RNM/constriction σ)→우리(삼중항+MPM)** | continuum (GeoDict, voxel flux-PDE σ_ion) | ✅(docs) | `docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md` + `docs/data/bielefeld2020_sigma_binder.csv` |

## 패킹 기하 (geometric packing — Furnas dip 근거)

| 논문 (제1저자 년) | 저널 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|
| **McGeary 1961** | J. Am. Ceram. Soc. 44(10) | 강체 구(금속 shot) bimodal/multimodal 충전 62.5→86→90→95.1%, 임계비 **7:1**(0.154·d_c); **소성변형 없음** = Furnas-dip 기하 원전 | exp | ✅ | `mcgeary1961_bimodal_sphere_packing` |

## 실험 1차 앵커 (EIS-TLM / 측정값)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **★ Minnmann 2021 JES** | J. Electrochem. Soc. 168, 040537 | **NCM-622 + LPSCl** (= 우리 소재계) | ★★ **우리 porosity/σ_ion/τ 앵커의 진짜 출처.** EIS-TLM 1차 측정: **복합 porosity 14 % (13–17 %, dry-mix 380 MPa)** · **σ_ion,eff 0.17 mS/cm @ 42 vol% NCM** · **τ_ion 2.07 (=√(τ²=4.3))** · σ_el,eff 0.56 (τ_el²=7.4) · LPSCl bulk 1.6 mS/cm · NCM 전자 10 mS/cm. CAM vol% 25–61 스윕(CAM↑→σ_ion↓/τ↑), 42 vol% 154 mAh/g 최적; carbon-free 고-CAM; fine SE→σ_ion,eff↑(packing/τ). | exp (EIS-TLM+cycling) | ✅(docs) | `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md` |
| **★ Doux 2020** | Adv. Energy Mater. 10, 1903253 | **LPSCl + Li-metal** (+LNO-NCA full cell) (= 우리 SE) | ★ **작동압(operating) vs 제조압(fabrication) 앵커.** Li 대칭셀 단락시간: **75→0, 25→48, 20→190, 15→272, 10→474, 5 MPa→∞(>1000h)** → 최적 작동 **5 MPa**(≥25 단락, Li가 SE 공극으로 creep=기계적 단락). 임피던스 **500→32 Ω(@25 포화), release 비가역(110→50)**. ★ 펠릿 **porosity 18 %(rel.dens 82.1 %)@370 MPa** = 강체-구 floor 실험 확증. σ_pellet 2–2.5 mS/cm. full cell 229 cyc/80.9 %@5 MPa. ⚠ Li-metal 단락 논문 → SE 압력-역학만 전사 | exp (in-situ P-cell + XCT/XRD) | ✅(docs) | `docs/lit_doux2020_stack_pressure_assb.md` |
| **★ Cronau 2021** | ACS Energy Lett. 6, 3072 | sulfide SE 6종 (µC-Li₆PS₅**Br** 등, **단결정·Cl 측정 無**) | ★ **stack pressure 가 σ *측정* 신뢰성을 좌우**(측정 protocol). σ_grain=3.0 출처판정: 본 논문 아님(µC-Br plateau ~2.4 + 타 LPSCl 종합); Cronau(r_SE)=결정도/GB 인자(breakpoint 미지지). 제조압 400–500 + 작동 5–50 MPa 권고 | viewpoint (exp) | ✅(docs) | `docs/lit_cronau2021_stack_pressure_ionic_conductivity.md` |
| **★ Sakuda 2013** | Sci. Rep. 3, 2261 | **75/80Li₂S·25/20P₂S₅ glass**(=Li₃PS₄ 조성 유리, **NOT LPSCl**) + LiCoO₂ 셀 | ★ **황화물-기계물성 고전 + 우리 두 토대 앵커의 원전.** (1) **E_SE 18–25 GPa, 75Li₂S·25P₂S₅=24**(초음파, stated) = 우리 real-bulk 24 의 출처(E_eff 1.35/1.53 = 그 연화 프록시); (2) "**상온 가압소결**"(산화물과 달리 냉간 치밀, Fig2·3 입계소멸) = 우리 cold-press+MPM void-fill 물리 토대. 밀도: **stated ">90 %@>350 MPa"**(porosity<10), ~87 %@300 = **Fig2a digitized 추세**. σ 냉간 0.31/bulk 0.34 mS/cm. ⚠ glass≠LPSCl → 물리·E 전이 OK, σ·밀도 절대값 전이 금지 | exp (밀도-P + 초음파E + EIS + 셀) | ✅(docs) | `docs/lit_sakuda2013_sulfide_mechanical_property.md` |
| **★ Minnmann 2024 JES** (Janek 그룹; Minnmann 2021 후속, Editors' Choice OA) | J. Electrochem. Soc. 171, 060514 | **Li₃PS₄·0.5LiI glass composite + NCM** (⚠ LPSCl 아님=분리막만) | ★ **FIB-SEM 토모그래피 microstructure→performance 시각화.** 작은 SE(ball-mill d50 7.4/4.9/5.9µm)→균질↑·porosity↓·active interface↑·τ_ion↓: porosity **6–10%**(geom 11–20)@380 MPa·σ_ion 0.05→0.11·σ_el 15→10·coverage 20→50%·CAM util 62→77%. **frame[4] TREND 앵커**(글래스≠LPSCl→절대전이 금지; LPSCl 절대값은 Minnmann2021); pore-less τ = porosity가 *이온*만 지배(우리 σ_ionic-porosity vs σ_e-porosity 무관 정당화); densification_porosity_db.csv에 3행 추가 | exp (FIB-SEM + cycling) | ✅ | `minnmann2024_microstructure_porosity_visualization` (+CSV) |
| **★ Reisacher 2023** (Aalen IMFAA, OA) | Batteries 9, 595 | **LPSCl + C65 carbon** (= 우리 정확한 SE) | ★ **전자 percolation 임계 p_c≈4 wt% C65**(BET 62 m²/g 지배, 밀도 아님). <p_c 이온지배(σ_eff≈순SE 6.6e-5 S/cm, 온도활성) / >p_c 전자 ohmic(3→5wt% σ 3자리↑→0.1 S/cm). **LPSCl=우리 SE → 재료보정 없이 전이** = backlog A4 carbon-gate 앵커(70wt%AM은 1.2wt% C65로 percolate); Bielefeld AM p_c(7.83·ln d+36.67)의 *carbon* 짝. ⚠AM-free matrix·2 MPa 저압(절대σ 전이금지, 임계/step/sign만); E_a 0.41 eV ≠ Bielefeld β 0.41(우연) | exp (EIS percolation) | ✅ | `reisacher2023_percolation_sulfide_carbon_matrix` (+CSV) |

## 사이클 파괴 · 계면 역학 (frame[5] — 우리 *압밀* Auerbach의 *사이클* 짝; 우리 미보유칸)

> ★ **driver 구분 필수**: 우리 Auerbach = *압밀 접촉응력*(AM-AM, 압력 지배); 아래 = *사이클 intercalation strain*(Vegard, 압력항 없음/미미).  우리 MPM J2(연성)은 SE *취성* 균열·계면 박리 불가 → de Vaucorbeil continuous-damage/cohesive-MPM(backlog D6)이 구현경로.

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **Bucci 2017** (MIT, Chiang/Carter) | J. Mater. Chem. A 5, 19422 | SE-무관(E_SE 14–200 GPa 스윕) | ★ **ASSB 기계신뢰성 *최초* 정량**: electro-chemo-mechanical FEM + **cohesive-zone(CZM)** SE 균열(Vegard 팽창 driver). 균열방지 = 팽창<**7.5%** AND G_c≥**4 J/m²**(𝒢<1000 규칙); ★**연한 SE(E~15)일수록 균열↑**(비선형 kinematics, 산화물>황화물 통념 반박). 우리 압밀-Auerbach의 *사이클* 짝(미보유). ⚠E_SE 15=실재료 사이클 modulus≠우리 E_eff 1.35(압밀 프록시)—혼동금지(비교는 우리 real 24↔그들 sulfide 14–25, argyrodite 18.5 최근접) | FEM+CZM | ✅ | `bucci2017_chemomech_failure_assb_cycling_czm` (+CSV) |
| **Bucci 2018** (MIT+Bosch) | Phys. Rev. Mater. 2, 105407 | SE-무관(E 20–200 스윕) | ★ **1D 방사 cohesive 계면 *delamination* 모델.** 팽창 ~7.5%서 박리개시(입경 무관)·연한 SE(E<25)+γ>5 J/m²는 25%까지 수용·임계반경 ~50–500 nm; **박리→ASR 임피던스↑**(50% 박리서 first-passage ×2.75). 우리 Stage-E AM-SE coverage의 *사이클 파괴*(B6 시간축); LPSCl E≈22<25 임계 = 우리 ductile-LPSCl 프레임 보강 | 1D analytic (cohesive) | ✅ | `bucci2018_mechanical_instability_interface_delamination` (+CSV) |
| **NMC811 입계균열 2023** (UCL EIL/Faraday; Parks 외) | J. Mater. Chem. A 11, 21322 (OA) | polycrystalline NMC811 | ★ **직접관찰(X-ray 나노-CT, 동일입자 pristine→4.5V)**: **입계균열 중심핵 4V 발생→방사전파**(c-strain 0.015→4.1V 붕괴 spike); driver=이방 격자strain GB응력(압력항 無); 2차입자 +19% 팽창(=균열-void, ΔV의 ~92%). **결정도축 *다결정 균열* 직접 실험증거**(Jung2023 단결정 대비짝). 우리 압밀-Auerbach와 driver 다름. ⚠+19%는 잔류응력 일부(100% echem 아님); C/50서 size상관 미미(R²0.49) | exp (nano-CT + phase-field) | ✅ | `intergranular_cracking_nmc811_jmca2023` (+CSV) |

## 설계 Perspective (정성 — 수치 앵커 아님)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **Minnmann 2022** | Adv. Energy Mater. 12, 2201425 | NCM/LFP/LMO/conv + sulfide/halide SE (우리 LPSCl+NCM 설계공간) | ★ **설계 Perspective(1차데이터 아님)**; porosity/σ **측정값 0개**(전부 정성); 설계임계만: CAM 60–70 vol% 최적·3–5 µm CAM·작은 SE+큰 CAM/SE비·tailored PSD·SE 고tortuosity(C(τ) 정당화)·§5.4 결합 mech-echem-thermal 모델 호명. **★ 우리 "Minnmann porosity 14 %/13–17 %/τ 2.07" 앵커는 이 논문 아님 → Minnmann 2021 JES 040537 / Sakuda 2013** (digest §0) | review | ✅(docs) | `docs/lit_minnmann2022_designing_cathodes_solidstate.md` |
| **Deysher/Meng 2022** (UCSD/UChicago, LGES) | Mater. Today Phys. 24, 100679 | **NMC \| LPSCl \| Si/Li** (우리 소재계) | ★ **transport+mechanics 리뷰**(1차데이터 0, 전부 인용→§10 1차인용 금지경고): 복합 cathode 이온/전자 수송한계 ↔ 부피변화/void형성/접촉손실 커플; 앵커 인용 **<20% porosity 풀-활용(Bielefeld)·370 MPa 재가압 용량회복(Koerver)·5 mA/cm² 80%@500cyc NCM811+LPSCl(Tan)·6.8 mAh/cm²(Lee)**. 리뷰가 *호명*한 정량 transport+기계모델 = 우리 DEM σ-삼중항↔MPM이 *실현*(미래방향 6개 중 4개 충족, 사이클·계면 2개 공유) | review | ✅ | `deysher2022_transport_mechanical_aspects_assb_review` (+CSV) |

> ★ **PROVENANCE 확정 (2026-06-26, Minnmann 2021 PDF 직접 확인):** porosity 13–17 %·σ_ion_eff 0.17·τ_ion 2.07 = **Minnmann *2021 JES* 040537**(NCM622+LPSCl, **압밀 380 MPa**, EIS-TLM **측정 40 MPa**, **42 vol% NCM** 기준). 세 앵커 전부 PDF 본문서 stated 확인 (τ_ion 2.07 = √(tortuosity factor τ²=4.3) — τ vs τ² 구분 필수). 밀도 앵커 = **Sakuda 2013**(75Li₂S·25P₂S₅ **glass**, ≠LPSCl): **stated ">90 %@>350 MPa"(porosity<10)** — "**87 %@300 MPa**"는 **Sakuda Fig2a 에서 digitized 한 추세값**(±, 본문에 300 MPa 정밀값 **없음**); pure-SE 10 % = 우리 MPM 보정 수렴값(Minnmann 논문은 *복합* porosity만 줌, pure-SE 아님). 2022 AEM Perspective는 **정량 데이터 없음.** + `refs.bib @Minnmann2021`이 엉뚱한 040502/abf3a3을 가리킴 → **040537/abf8d7**로 정정 권고. 저자 = Philip Minnmann, **Lars Quillman**, Simon Burkhardt, Felix H. Richter, Jürgen Janek.

## 통합된 기존 노트 (→ papers/ digest로 흡수)
- `docs/lit_varkey2026_multicontact_dem.md` (한국어 노트) → `papers/varkey2026_*` ✅ + `docs/data/{densification_porosity_db,varkey2026_ionic_vs_pressure}.csv`
- `docs/lit_bazzoun2026_dem_fem_rnm.md` (한국어 노트) → `papers/bazzoun2026_*` ✅ + `docs/data/bazzoun2026_sigma_ionic.csv`
- **Lee 2025** (실험 앵커) → `papers/lee2025_*` ✅ (σ·CBD·파괴 관점) + **`docs/lit_lee2025_corolling_dryprocess_assb.md`** ✅ (★ **공정(co-rolling) + 저작동압 2 MPa + fab-vs-operating** 관점, Doux/Minnmann 압력구분 합류) + `docs/data/lee2025_transport_anchors.csv` (PTFE% σ 페널티 + 조성별 σ + bulk 앵커); CBD 검증 → `docs/cbd_morphology_roadmap.md`
- `docs/literature_coverage/` json DB: contact_mechanics_db, coverage_db, packing_regime_db (수치 참조용 유지)

## 접촉모델·소성 이론 (DEM contact LAW + MPM 소성 — 2026-06-26 일괄 digest 14편)
> ★ **층위 지도 = `contact_models_layer_map.md`** (우리 hooke/hysteresis·Stage-E·18×연화·f_AM·ε_sphere·J2가 어디 anchor되는지 + 경로A 스펙).  아래는 slug 목록.

| 층 | 논문 | slug |
|---|---|---|
| **A no-cap 이력 (=우리 모델)** | Luding 2008 (★우리 LAW 정의서) · EEPA(Thakur 2014) · Pasha 2014 | `luding2008_cohesive_frictional_contact_models` · `thakur2014_eepa_adhesive_elastoplastic_dem` · `pasha2014_linear_elastoplastic_adhesive_contact` |
| **B 항복캡 (=경로 A LAW)** | Thornton–Ning 1998 (★경로A) · (So 2021 digest됨) | `thorntonning1998_adhesive_elastoplastic_contact` |
| **C FEM EP 기준** | Kogut–Etsion 2002(CEB 대체) · Jackson–Green 2005(H가변) · Mesarovic–Fleck 2000(異種=AM-SE) | `kogutetsion2002_ep_sphere_rigid_flat` · `jacksongreen2005_fem_elastoplastic_hemispherical_contact` · `mesarovicfleck2000_dissimilar_elastoplastic_indentation` |
| **D 자기상사 소성면적** | Storåkers 1997 (A=2πc²rh, pile-up 1.4) | `storakers1997_similarity_inelastic_contact` |
| **E 점착 이론** | DMT 1975 (★SE=DMT 체제, 2πRγ) | `dmt1975_adhesion_contact_deformation` |
| **MPM 소성 (snow→sand→J2)** | Stomakhin 2013(snow box) · Klár 2016(sand DP=DPC원전) · de Vaucorbeil 2020(MPM 리뷰) | `stomakhin2013_mpm_snow_elastoplastic` · `klar2016_dp_sand_animation` · `devaucorbeil2020_mpm_after_25_years_review` |
| **배터리 DEM peer** | Sangrós 2020 · Ngandjong 2021 (LIB; 이온위상 역전) | `sangros2020_lib_electrode_dem_mech_elec_ionic` · `ngandjong2021_dem_calendering_digital_twin` |

## 주제별 종합 문서
- `elasto_plastic_feasibility.md` — elasto-plastic 접촉모델 실행가능성·적용·우리 모델 대비 장단점
  (Varkey/So/M&B 종합; ★ So 2021 H-cap = 18× 연화 대체 경로).
- **`WISHLIST.md`** — ★ elasto-plastic 접촉/소성 논문 **agent 투입 대기열**(분야 무관 *정전* 우선:
  Tabor·Johnson·CEB·Mesarovic–Fleck·Walton–Braun·Luding·Thornton–Ning…).  2026-06-26 발견(Hertz가
  실제 hooke/hysteresis 접촉력 재현 못 함; `docs/mpm_wallP_conditional_troubleshooting.md` §12)이 동기.  **위시리스트 100% 소진(14편 digest).**
- **★ `contact_models_layer_map.md`** — 접촉모델 14편을 우리 모델 기준 **층위 지도**(no-cap=우리/캡=경로A/FEM기준/
  자기상사/점착/MPM 계보)로 종합 + **경로 A 구현 스펙**(real E + p_y캡 → 18×연화 제거 시험).

## 추가 digest — INDEX 미반영분 일괄 정리 (2026-06-30, "INDEX 마무리")
> papers/ 60편 + docs/lit_*.md 33편 중 **위 섹션에 아직 안 올라온 17편**을 주제별로 일괄 등록.
> 각 행 = 방법·핵심 + **우리 모델 어디에 먹이나(feeds)**.  (정밀 재배치는 추후; 여기 등록 = 누락 0.)

**구조·percolation·전달 peer (우리 DEM 접촉망/σ 교차검증)**
| 논문 (제1저자 년) | 핵심 + feeds | type | slug |
|---|---|---|---|
| **Chen 2011** | 다분산 복합전극 *해석적* percolation 미시모델(CN·percolation·TPB·σ_inter/intra·hydraulic pore 닫힌식) → 우리 CN·percolation→σ 논리의 해석 peer(B3 인접) | analytic | `chen2011_percolation_micromodel_composite_electrode` |
| **Zhang 2024** (Powder Tech.) | DEM **전기-기계 접촉 결합** 모델(접촉변형↔전기전도) → 우리 Kirchhoff/Holm 접촉-σ의 DEM-side 결합 peer | DEM (contact+electrical) | `electromechanical_contact_model_particulate_systems` |
| **Nisar 2024** (Comp. Part. Mech.) | 부분소결 다공체 유효 σ_e DEM **저항망(sinter-neck conductance)** → 우리 Holm/Kirchhoff σ_e 저항망의 소결-neck peer | DEM (resistor network) | `nisar2024_dem_effective_electrical_conductivity_sps` |
| **TauFactor** (Cooper) | voxel 미세구조에서 Laplace 정상확산 풀어 **tortuosity factor τ 직접 계산** MATLAB 툴 → 우리 τ_Laplace/voxel τ의 독립 교차검증 도구(우리 dump에 직접 실행 가능) | tool (MATLAB) | `taufactor_tortuosity_factor_tomography_tool` |

**DEM 제조·압밀 (ASSB/LIB 공정 peer)**
| 논문 (제1저자 년) | 핵심 + feeds | type | slug |
|---|---|---|---|
| **Schneider 2023** (Adv. Energy Mater.) | t-Li₇SiPS₈ **입자크기·압력→수송물성**, DEM 압밀+Heckel+FVA σ → 우리 Cronau(r_SE) SE-size 인자 + σ-vs-porosity(압밀) 검증(**B5/B6**) | DEM+exp | `schneider2023_particle_size_pressure_transport` |
| **Frankenberg 2024** | ASSB 복합양극 **고강도 믹서** 공정 DEM(coarse-graining + force-scaling) → 분산/혼합 공정(A5 dispersion 인접) | DEM (mixing) | `frankenberg2024_dem_high_intensity_mixer_assb` |
| **Schreiner 2020** | LIB calendering DEM(EDEM+EEPA 탄소성+Bonding Potyondy–Cundall, 3-모듈) → 캘린더링 제조 DEM peer | DEM (calendering) | `schreiner2020_dem_calendering_lib` |
| **wet-processing resolved-AM** | ASSB 양극 *습식*(슬러리→건조→압연), **실제형상(resolved multisphere) AM**을 nano-CT서 추출해 DEM 제조 → resolved-grain 제조 peer | DEM (wet, resolved) | `wet_processing_resolved_am_ssb_cathode_manufacturing` |
| **Lim 2025** (Small) | **Virtual Calendering Framework**: 3D-재구성 양극 가상 캘린더링 + 전극설계 최적화 → 우리 압밀·구조 파이프라인의 가상-캘린더링 peer | framework | `docs/lit_lim2025_virtual_calendering_framework.md` |

**CBD · binder · carbon morphology (Stage-2 A3/A4/A7)**
| 논문 (제1저자 년) | 핵심 + feeds | type | slug |
|---|---|---|---|
| **Bak 2024** (Chem. Eng. J.) | **바인더 z-분포 제어** 다층 모델전극 + digital-twin → **A7 graded-z**(carbon:binder z축) | exp+model | `docs/lit_bak2024_binder_distribution_multilayer.md` |
| **Koo 2025** (Energy Storage Mater.) | anti-solvent **MWCNT 감싼 단결정 SC-NCA dry** 양극(99.6 wt%, 4.0 g/cc) → CBD carbon morphology(#275 선행) | exp | `docs/lit_koo2025_cnt_wrapped_sc_nca_dry_cathode.md` |
| **Koo 2026** (Joule, #275) | **연속 SWCNT sheath** 두꺼운 dry 전극 = 우리 CBD **SuperP-vs-VGCF "discrete=gap-filler, 연속=backbone"의 실험 증명** + 제3 morphology(sheath) | exp+digital-twin | `docs/lit_koo2026_swcnt_sheath_thick_electrode.md` |
| **★ Kang(Jihyeon) 2025** (Adv. Mater. 37, 2416872; 중앙대+현대차 — ⚠랩 Junhee Kang 아님) | ★ **"bollard hitch" 앵커 바인더 = 우리 SDCP의 개념-클래스 독립 선례.** NMC622+SuperP+PTFE+**PC(PAA-g-CMC)** LIB **건식전극**: PC가 NMC 표면에 **Na⁺-매개 화학흡착**(MLP-DFT E_ads **−2.24 eV**(2Na)≫극성 −0.37≫**PTFE vdW −0.09**; 400K NVT-MD로 PTFE 탈착 4.2→6.6 Å vs PC계류 4.5–4.9 Å) + **Na–F −0.35 eV**로 PTFE fibril 계류 → **PTFE 2→0.6 wt%(>70%↓)**로 30 mg/cm²(4.0 mAh/cm²@2C)·**90 mg/cm²=15.6 mAh/cm²**; 바인더 필름 σ_ion PTFE 4.88e-6→PC_PTFE **1.31e-4 S/cm(27×)**·peel **1.68×**(0.96/0.57 N/cm)·양극 σ_e 1.30 S/cm(분산효과); 혼합 STD 16.52→4.28(ballmill×3)=**A5 dispersion 앵커**; retention 83 vs 51%(PTFE)@100cyc·PTFE계 NMC 파쇄. feeds: **A4′ SDCP**(이온성≫극성≫vdW 사다리 = doped≫neutral 방향 외부확인; MD hold-test 이식; SDCP+PTFE 콤보 후보) + **A3 coh 앵커**(peel·R_ct) + **A5** + `--ptfe-fibril` 하한(0.6 wt%). ⚠ LIB 액체 — porosity 역전(25.9%/22.3% 중의적·τ1.30) 절대 전이 금지 | exp + MLP-DFT/MD (molecular) | ✅ | `kang2025_bollard_anchored_binder_dry_electrode` (papers) + `docs/data/kang2025_bollard_binder_anchors.csv` |
| **★ Han 2025** (Adv. Mater. 37, 2506266; POSTECH Soojin Park — Kang(Jihyeon)2025의 *습식* 자매편) | ★ **이온전도 탄성 binder ICEP** [P(AN-co-AMPS)]₂-b-PEO₄₆ (RAFT ~100 kDa; ⚠**액체 LIB 습식** NCM811+LiPF₆+Li — ASSB 아님): 필름 **σ_ion 0.135 mS/cm**(swollen 추정; PVDF 0.065; ★Kang(J) PC_PTFE 0.131과 사실상 동값 = 전도-binder 클래스 ~0.1 mS/cm 수렴)·연신 **283 %**(PVDF 31.8)·flow ~2.7 MPa(digitized)·필름 E 6.03 GPa(압입)↔인장 ~10–25 MPa(**3-decade 프로브 차** — MPM에 6 GPa 금지)·**SAICAS 0.29/0.27 N ≈290/270 N/m**(PVDF 4–7×)·DFT NCM811(001) AMPS −1.8~−2.2 eV≫PVDF −0.70·**NCM811 위 ~7 nm coat형**(vs PVDF aggregate·PTFE fibril = 3-morphology)·전극압입 **E 1.57 GPa**(≈우리 MPM champion 1.53 밴드의 실측 동반자)·**62.4 mg/cm²=12.5 mAh/cm² 크랙-프리**(PVDF 31.7 하락·40.7 균열/박리)·62.4서 94.6 %@60cyc·rock-salt 3.1 vs 11.3 nm(nano-CT 균열 억제)·z-Raman E_g/A₁g 균일(PVDF 바닥 미반응 0.84)·파우치 377.6 Wh/kg·1016.8 Wh/L. feeds: **W2 binder-σ 새 클래스**(binder-voxel σ_b>0; film-ASR t/σ: 7 nm 전도-coat ≈5e-3 Ω·cm² 무시 ↔ 절연-coat ≥10³ 차단 — 우리 유도) + **A3 --coh 앵커**(σ_coh~2.7 MPa·peel 270 N/m 상한측) + **coat=sub-voxel 계면성질/fibril=resolved 시딩 규칙** + **SDCP 물성 템플릿**(σ≳0.1·연신≳200 %·2-Tg). ⚠porosity/조성/캘린더링 SI-only·건조균열 driver는 습식 전용 | exp + DFT(흡착) | ✅ | `han2025_icep_conductive_elastic_binder` (papers) + `docs/data/han2025_icep_binder_anchors.csv` |

**kinetics / impedance + 공정 review + 저압 설계**
| 논문 (제1저자 년) | 핵심 + feeds | type | slug |
|---|---|---|---|
| **Choi 2024** (ACS AMI) | 복합양극 **계면 임피던스 정식화(TLM 등가회로)** → 고에너지·고출력 설계규칙; 우리 geometric ASR 위에 **kinetics 칸**(R_ct/이중층/Warburg, 미보유) 추가 경로 | exp+TLM | `interfacial_impedance_formulation_assb_cathode` |
| **Liu 2025** (review) | **건식공정(DPT)** 총설(DPC/분무/압출/**PTFE 섬유화**) LIB → A3 CBD + 압밀 프로토콜(co-rolling) 공정 맥락 | review | `liu2025_dry_processing_high_energy_li_batteries_review` |
| **Zhou 2025** (ACS Energy Lett.) | **저압 장수명** 복합양극 microstructure 설계(tailored) → 작동압-구조-수명 설계 peer | exp | `tailored_cathode_microstructure_low_pressure_assb` |
| **Yoo 2026** (Energy Storage Mater.) | **porosity-구배** 건식 흑연 전극 + 변형성 Primer Layer → **A7 Phase-5 graded-z** | exp | `docs/lit_yoo2026_porosity_gradient_dry_electrode.md` |

**사이클 파괴 frame[5] (우리 압밀-Auerbach의 사이클 짝, 미보유칸)**
| 논문 (제1저자 년) | 핵심 + feeds | type | slug |
|---|---|---|---|
| **Alabdali·Ngandjong** | ⭐ **사이클 응력 DEM**(SSB 전극 cycling 기계응력) → frame[5] *사이클* driver(우리 *압밀* DEM의 시간축 짝, A10) | DEM (cycle stress) | `dem_mechanical_stresses_ssb_electrode_cycling` |

**docs/lit_*.md 실험·디지털트윈 앵커 (우리 소재계/축 — 행 누락분)**
| 논문 (제1저자 년) | 핵심 + feeds | type | slug |
|---|---|---|---|
| **★ Hong 2026 #271** (sulfide binder DT) | LPSCl+NCM **PTFE void −6.4%p**(28.7→22.3 vol%)·σ_ion 0.064(=Pwd 74%, 차단−치밀화 상쇄)·retention 94.6% → **σ_ionic 절대 앵커 + A3 binder + whatif_additives(W2) PTFE** | exp+DT | `docs/lit_hong2026_sulfide_cathode_binder_digitaltwin.md` |
| **★ Hong 2026 #285** (CBD viscoelasticity) | PTFE/CBD **점탄성 spring-back**(RT+4/HT+1µm/3주)·단결정 rigid-AM 정당화 → 우리 rate-indep J2의 *시간축 한계*(#7/#10) | exp+DMA | `docs/lit_hong2026_cbd_viscoelasticity_springback.md` |
| **★★ Oh 2026 #266** (bimodal) | ASSB **bimodal Furnas dip 정량 1:1**(He pycnometry 8.83%@CAM7:3, σ_ion peak)·σ_e **poly(13.7)≫single(2.45)** → 우리 a9_50 dip 검증 + **σ_e 방향(A1/#11)** | exp | `docs/lit_oh2026_bimodal_composite_cathode.md` |
| **Oh 2026 #284** (carbon-coat SiOx) | CBD **이온/전자 balance**(중간-C 최적)+분산 정량(SSRM/work-of-adhesion) → **A5 dispersion CoV / E1·E2** | exp | `docs/lit_oh2026_carbon_coating_siox_ion_electron_balance.md` |
| **★ Park 2020 #22** (foundational DT) | 계보 시조 LiNbO₃-NCM711+LPSCl+NBR; **NCM 90wt% σ_eff,ion 계산불가(LPSCl 퍼콜 단절)** = 우리 SE-no-perc degenerate 1:1·dead-AM 회피대 | exp+DT | `docs/lit_park2020_digitaltwin_assb_foundational.md` |
| **★ Trevisanello 2021** (SC/PC NCM) | 단·다결정 NCM **균열·Li확산·BET·R_ct**(★ **σ_e 측정 無** — A1 mis-attribution 출처); SC 0.84>PC 0.17 m²/g | exp | `docs/lit_trevisanello2021_sc_pc_ncm_cracking_diffusion.md` |

**papers/ DEM 공정·민감도 + 주변 (행 누락분)**
| 논문 (제1저자 년) | 핵심 + feeds | type | slug |
|---|---|---|---|
| **Bazzoun 2025** | DEM **파라미터 민감도**(friction 지배)·high-f_CAM rigid-sphere 불일치 → 경로A/Stage-E dense-regime 가이드(**D1/B4**) | DEM | `bazzoun2025_dem_parameter_sensitivity_assb_cathode` |
| **Lee 2024** | **multiphysics DEM+FEM 초기압력** ASSB → 압력→구조→역학 커플 peer | DEM+FEM | `lee2024_multiphysics_dem_fem_initial_pressure_assb` |
| **Mun 2025** (review) | **건식전극 기술** 총설(co-rolling/PTFE) → A3 CBD + 압밀 프로토콜 공정 맥락 | review | `mun2025_dry_electrode_technology_assb_review` |
| **Shi 2019** | **고-AM 로딩 × 입자크기** ASSB → 조성·크기-packing peer | exp/DEM | `shi2019_high_am_loading_particle_size_assb` |

**docs/lit_*.md 디지털트윈·바인더·주변 (행 누락분, 정성/주변축)**
| 논문 (제1저자 년) | 핵심 + feeds | slug |
|---|---|---|
| **Choi 2024** | digital-twin echem 리뷰 → positioning | `docs/lit_choi2024_digital_twin_review_echem.md` |
| **Song 2025** | electrochemo-mech 미세전극(**Perzyna-Ludwick 점소성**) → A3/#17 | `docs/lit_song2025_electrochemo_mechanical_microelectrode_ees.md` |
| **Lee 2023** | SiC-SPE digital-twin ASSB | `docs/lit_lee2023_sicspe_digitaltwin_assb.md` |
| **Nam 2026** | DPE(dry-process electrode) microstructure 리뷰 | `docs/lit_nam2026_dpe_microstructure_review.md` |
| **Kim 2026a** | A3D 공기전극 microstructure-transport | `docs/lit_kim2026_a3d_air_electrode_microstructure_transport.md` |
| **Kim 2026b** | charge-engineered CNF 바인더 | `docs/lit_kim2026_charge_engineered_cnf_binder.md` |
| **Park 2026a** | ceramic-PP 분리막 | `docs/lit_park2026_ceramic_pp_separator.md` |
| **Park 2026b** | thiol-ene SBR 바인더 ASSB | `docs/lit_park2026_thiolene_sbr_binder_assb.md` |
| **Choi 2026** | elastomeric Li-metal 음극 | `docs/lit_choi2026_elastomeric_li_metal_anode.md` |
| **Cho 2026** | EIPC Zn 음극 AZIB (수계, 주변) | `docs/lit_cho2026_eipc_zn_anode_azib.md` |

**동일-저자 *별개* 논문 (위 행과 다른 paper — 행 누락분)**
| 논문 (제1저자 년) | 핵심 + feeds | slug |
|---|---|---|
| **So 2021b** (≠ cold-press) | ⭐ **사이클 열화 DEM** — Fabrication & Degradation of ASSB → frame[5] 사이클 driver(A10) | `so2021_dem_fabrication_degradation_ductile_particles` |
| **So 2022b** (≠ 접촉모델) | **SE-코팅(core-shell) vs 입자-혼합** DEM 냉간압밀 — tortuosity·AM damage·percolation → **A4 se_coating_interface** 직접 peer | `so2022_dem_compaction_coated_particles_assb` |
| **Sangrós 2020b** (≠ LIB) | **ASSB(폴리머 SSB) 전자 전도경로** DEM — A* 경로탐색 + 실린더 → 우리 σ_e 경로/percolation peer | `sangros2020_dem_electrical_conductive_paths_assb` |
| **Kim 2024b** (ACS Energy Lett., ≠ carbon-점유) | **Digital Twin Battery Modeling & Simulations** 동료심사 → 우리 DEM+MPM 스케일 positioning | `docs/lit_kim2024_digital_twin_acsenergyletters.md` |
| **★ Kim 2025b** (Battery Energy, ≠ TLM) | **SE-coating CA(Super P 0D vs VGCF 1D)**: SE-SP σ_e **1.0e-5(3-decade 붕괴)** vs VGCF 1.4e-2; σ_ion SP 최저 → ★ **whatif_additives(W2) thinky-SuperP 붕괴 앵커 + A4** | `docs/lit_kim2025_conductive_agent_se_coating_assb.md` |

## 현황
papers/ digest **64편** (+**📌 Li(Yang)2026 ECER-D-26-00097 심사중 원고** 황화물 안정성 총설 — 최상단 고정, 2026-07-16; +**Duquesnoy2023** ML 다목적최적화 archetype, 2026-07-10; +Kang(Jihyeon)2025 bollard·Han2025 ICEP 전도성-바인더 자매 2편, 2026-07-08) + docs/lit_*.md **33편** ✅ — **2026-06-30 INDEX 마무리 완료**: 4개 일괄 섹션으로 **모든 digest 파일이 slug로 findable** (검증 통과, 누락 0).  이전 "41편"/슬러그 stale 정정.  ⚠ 같은 (저자,년)에 *별개 논문*이 여럿(So2021/2022·Sangrós2020·Kim2024/2025) → slug로 구분.  **랩 자체논문 7편**(필독): Kang&Shin2025(역학/균열)·Kim·Kang·Park·Lee2025(EIS-TLM)·Kim2024(carbon점유)·Cho2024(VGCF양면성)·Kang2023(음극strain균열)·Jung2023(단결정NCM)·**Yun2023(degradation 종합 capstone)**.  **접촉모델·소성 14편**(`contact_models_layer_map.md`): Luding·EEPA·Pasha·Thornton–Ning·Kogut–Etsion·Jackson–Green·Mesarovic–Fleck·Storåkers·DMT·Stomakhin·Klár·de Vaucorbeil·Sangrós·Ngandjong.  **기존 7편**: Lee2025·Bazzoun·Varkey·So2021·Martin-Bouvard2003·Bouvard2000·McGeary1961.
**★ #17-29 batch 13편 (2026-06-27):** DEM/ASSB — So2022(접촉+소결)·Huang2025(DEM+LBM 열); LIB제조 DEM+LIGGGHTS — Sangrós2019(Thornton-Ning+bond)·Lyu2025(건조+CBD parallel-bond)·Shenouda2020(LIGGGHTS튜토리얼)·Bosch2014(LIGGGHTS MSc); 구조모델링 — Bielefeld2019(percolation, B3 verbatim 확인, docs노트 대체); 실험앵커 — Minnmann2024(FIB-SEM)·Reisacher2023(LPSCl+C65 p_c≈4wt%); 사이클파괴 frame[5] — Bucci2017(CZM)·Bucci2018(delamination)·NMC811입계균열2023(nano-CT); 리뷰 — Deysher2022.
+ docs/ digest: **Minnmann 2021 JES**(★ porosity/σ_ion/τ 앵커 진짜 출처, EIS-TLM) · Minnmann 2022(설계 Perspective)
· **★ Doux 2020**(작동압 vs 제조압 LPSCl 앵커, porosity 18 %@370 MPa) · **Cronau 2021**(stack pressure σ-측정 protocol)
· **★ Sakuda 2013**(황화물-기계물성 고전; E_SE 24 GPa 원전 + "상온 가압소결" 원전; 밀도 stated >90 %@>350 MPa)
· **★ Bielefeld 2019**(★ 우리와 가장 가까운 *구조-모델링 peer*; GeoDict stochastic-placement percolation, Janek 그룹;
  σ 안 풂·단봉 PSD·porosity=입력 → top-down/placement; p_c=7.83·ln(d)+36.67·β=0.41·이상조성 62/38~72/28 vol%; CSV `docs/data/bielefeld2019_percolation.csv`)
· **★ Bielefeld 2020**(⚠위시리스트 "2022"=오기, 실제 **2020**; ★ Bielefeld 2019의 *σ-추가 후속편*, 같은 1저자·GeoDict;
  2019가 미룬 **σ_eff,ion+τ²를 flux-PDE(EJ-HEAT 연속체)로 풀고 바인더(CBD) 영향 추가**; σ-method = **연속체 PDE → constriction 없음=σ상한**;
  Bruggeman 4× 과소·5% void→σ 2×·**바인더 V(B):V(AM) 0.05/0.10→σ급감·τ² 4.2→10·active interface −17~82%**(우리 CBD/voxel σ-블로킹 cross-check);
  **그룹-진화: 2019(σ없음)→2020(연속체σ+바인더)→Bazzoun2026(RNM/constriction)→우리**; CSV `docs/data/bielefeld2020_sigma_binder.csv`).
**Stack-pressure 3종 압력 구분 완성:** 제조(fab ~300–490 MPa: Minnmann 380 / Doux·Cronau 370–490) ≠ 측정/작동(stack ~5–70 MPa:
Doux 5 최적 / Minnmann 측정 40 / Cronau sputter 5–10·WC 30–50). 데이터 `docs/data/doux2020_stack_pressure.csv`,
`cronau2021_stack_pressure_ionic.csv`, `minnmann2021_sigma_tau_porosity.csv`.
새 PDF 업로드 후 "논문 에이전트 실행해줘"로 추가.
