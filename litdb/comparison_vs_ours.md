# 🔬 문헌 ↔ 우리 DFT — 물성축별 분류 + 논문 reference

> 기준값: `our_dft_baseline.md`. **각 주장마다 [출처 논문] 명시.** digest 있는 논문은 `papers/<slug>.md` 링크.
> 사용법: 새 논문 digest 시 해당 축 표에 행 1개 추가(+출처). 산화 Q&A는 맨 아래 §Q&A 로그.
>
> **범위** — 이 문서는 **DFT 물성축**(이온전도도·산화안정성·기계·전자구조·계면·도핑)이다.
> DEM·MPM 논문은 축이 달라 여기 들어갈 자리가 없고 **`comparison_vs_ours_DEM.md`** 가 받는다.
> ⚠ 두 문서를 한 분모로 세면 "159편 중 98편 미언급" 같은 **가짜 미결**이 나온다(2026-08-06).
> 편입률은 트랙별로만 센다 — `python3 tools/litdb/build_index.py --check` 가 그렇게 찍는다.
> **현재: DFT 트랙 64/64 편입 (2026-08-06).**

## 📑 Reference key (출처 약칭)
| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |
|---|---|---|---|
| **[Nolan18Rev]** ⭐⭐⭐코팅 계산 계보 #7 = 계보 전체의 **어휘집** · ★ `anodic/cathodic limit` 의 **정의 문장**이 활자로 있는 편 | **Adelaide M. Nolan**/Yizhou Zhu/Xingfeng He/Qiang Bai/**Yifei Mo\*** (Univ. of Maryland) 2018 ***Joule* 2, 2016–2046** (2018-10-17, DOI 10.1016/j.joule.2018.08.017; 본문 26 pp + refs 5 pp, refs 156, 그림 11, **표 0·SI 0**) — "**Computation-Accelerated Design of Materials and Interfaces for All-Solid-State Lithium-Ion Batteries**" | `papers/nolan2018_computation_accelerated_design_review.md` (2026-09-12, 그림 **9/11 실독**) | 리뷰(외부) · 자체 계산 0 · **방법 원전** |
| **[Xiao20Rev]** ⭐⭐코팅 계산 계보 #8 = **계보의 채점표** · ★ 우리 ESW 정의를 *"worst-case 하한"* 으로 못박을 활자 · ⭐ **#1–#6 에 없던 우리 무대(황화물·아지로다이트)가 #7 과 함께 들어오는 편** | **Yihan Xiao**¹²/Yan Wang³/Shou-Hang Bo²⁴/Jae Chul Kim²⁵/Lincoln J. Miara³/**Gerbrand Ceder\***¹² (¹UC Berkeley MSE · ²LBNL MSD · ³**Samsung Research America** Advanced Materials Lab · ⁴UMich–SJTU JI · ⁵Stevens Inst.) 2020 *Nature Reviews Materials* **5**, 105–126 (DOI 10.1038/s41578-019-0157-5, 온라인 2019-12-09; inbox #112 본문 22 pp · **SI 없음** · refs 250) — "**Understanding interface stability in solid-state batteries**". ⛔⛔ **서지 정정**: 파일명 `Banerjee2020_…` 과 계보 카드의 *"Banerjee/Wang/Meng"* 은 **오기**다 — 1저자 **Xiao**, 교신 **Ceder**, "Wang" 은 Samsung 의 **Yan** Wang. **Meng 그룹이 아니므로 "Cronk 2026 과 같은 그룹" 연결은 무효**(관계는 그룹이 아니라 *전제↔검증*, digest §7f). **자체 계산 0·실험 0 = 순수 종합**. **핵심 기여 = 계면 모델 4층의 위계**: ① grand-potential ESW(**번호 붙은 식 (1)–(2)** + *"창 = hull 위에 정확히 놓인 전압 구간"* — ⚠ 이 문장 자체는 **[Nolan18](#7) p. 2022 에도 있다**; #8 의 차별점은 **번호 붙은 식 + worst/best-case 위상 선언**) = **최악 시나리오** / ② **topotactic**(식 3, Na₃PSe₄ **V_topo,ext 2.75 V**) = **최선 시나리오** / ③ pseudo-binary 혼합(식 4 = 우리 `InterfacialReactivity` 와 문자 그대로 동일, **Li·O 개방계 확장 명시**) = 최대 구동력 / ④ explicit 슈퍼셀·AIMD(<1 ns, 시작배치 민감 — 저자 자인). **황화물 판정**: S²⁻ 산화 **~2–2.5 V**, 창 1.5–2.5 V(LGPS 1.7–2.1 ref.65 **또는** 2.1–2.3 ref.64); **CV 의 0–5 V 주장은 반응면적 부족의 산물** — 탄소 복합 WE 로 재면 **2.1 V 산화·1.7 V 환원**(ref.97,98, `Fig. 3b`) · operando XPS 2.7 V(ref.99); **SE 는 전자경로에 닿는 모든 곳(집전체·도전재)에서 분해**된다(ref.69,70). **산화물 양극과 >300 meV/atom**, 기전 = **S↔O 교환**(P–O 596.6 vs P–S 346 kJ/mol) + **Li₃PO₄ 싱크**(생성E **−2.767 eV/atom**); Co 가 황화물로 **>50 nm** 확산(ref.47 STEM-EDS). ⭐ **「Argyrodites」 소절 있음(단 21줄 한 문단 — ⚠ #7 도 `Li₆PS₅Cl` 을 3회 명시하므로 "계보 최초" 는 아니다)**: Li₆PS₅Cl 산화산물 **원소 S·폴리설파이드·P₂S_x·LiCl**(예측 64,66,115 ↔ **XPS 관측 116,117**), Li 금속 대비 **Li₂S+Li₃P**(118), NCM622\|LPSCl 에서 **PO_x/SO_x 증가**(119 XPS+ToF-SIMS), **300 사이클 양호**(117), **Li₆PS₅Br 의 O 도핑이 안정성 개선**(120) — ⛔ **아지로다이트 고유 창·Ea·σ 수치는 0**, *"다른 황화물과 유사할 것"* 한 문장. **`Fig. 5a` 에 `LPSCl` 이 행·열 라벨로 직접 등장**(ref.67 재수록) → **본 digest 픽셀 정량화**(§12a): LPSCl\|LCO figure-read −308 ↔ **Xiao2019 Table S2 정본 −339**(LMO −424↔−421·LFPO −100↔−101 은 1–3 meV 일치) ⇒ **인용은 Xiao2019 SI 로**. **`Fig. 6` 18점 좌표 복원**(§12b, 검증 2건 통과: Li₃PS₄ 1.69 V·LLZO (0.09,2.97)↔[Zhu15] 0.05–2.91): 황화물 5점 산화한계 **1.91–2.36 V 띠**, 창 최광 = **할라이드 3.56 V**, σ 챔피언은 창이 0.03 V. **`Fig. 7` = 우리 O/B 축의 문헌 자리**: 조성 레버 5개 중 **공유결합 혼성(P–O·B–O)만 σ·환원·산화 3축 동시 개선**, 나머지 4개는 전부 산화를 희생. **Table 1** = 음이온×양이온 Li-대비 분류(stable/SEI former/MCI former) — **O·S 화학에서 란타나이드 안정 = 우리 Nd 도핑의 계열 수준 근거**. ⚠ **표지에 "There are amendments" 고지가 있으나 PDF 에 정정 내용 없음** · ⚠ **내부 불일치**: LLZO 창이 `Fig. 6`(0.09–2.97) ↔ `Fig. 4d`(0.43–3.41, ref.145 재수록) ↔ 본문(2.9 **또는** 3.2 V) **셋이 다름** · 🔴 **우리 원장과 충돌 1건**: 우리는 Li₃P = `conductor-LEAK`(gap 0.70 eV), 리뷰는 Li₃PO₄/Li·LiPON/Li 에서 **부동태 산물**(ref.222,73) · ⚠ `Fig. 3a` 축이 **vs Li-In** · ⚠ 할라이드 소절 없음(2019 시점) · ⚠ 기계·덴드라이트·젖음은 범위 밖 명시 | ✅ `papers/xiao2020_interface_stability_ssb_review.md` (2026-09-12, **그림 7장 전부 실독 + `Fig. 5a` 52셀·`Fig. 6` 18점·`Fig. 4d` 5막대 좌표 복원**) | **[외부]** 리뷰 (자체 계산 0 · 자체 실험 0) |
| **[Lu24]** ⭐양극 코팅 계산 계보 #9 — ⚠ **축이 다르다**(코팅 *선정 열역학* 이 아니라 **저온 −30 °C 계면 동역학**) · ⭐ **우리 계**(Li₆PS₅Cl + 고Ni) | **Pushun Lu**/**Sheng Gong**(공동 1저자)/…/Hong Li/**Fan Wu\*** (中国科学院物理研究所 **IOP CAS**) 2024 ***ACS Nano* 18, 7334–7345** (DOI 10.1021/acsnano.3c12797; 본문 12 pp + SI 8 pp) — "**Superior Low-Temperature All-Solid-State Battery Enabled by High-Ionic-Conductivity and Low-Energy-Barrier Interface**" | `papers/lu2024_lowtemp_assb_li2zro3_interface.md` (2026-09-12, 그림 **8/18 실독** — 안 본 7장은 전부 임피던스 절차 계열) | 실험 주도 + DFT/MLIP 보조 · 외부 |
| **[Cronk26]** | **Ashley Cronk**/X. Wang/J. A. S. Oh/S.-Y. Ham/**Shuang Bai**/P. Ridley/**M. Chouchane**/C.-J. Huang/…/**Jeong Beom Lee\***(LG Energy Solution)/**Y. S. Meng\*** 2026 ***Nat. Commun.* 17, 3298** (UCSD MSE·NanoEng + UChicago PME + LGES; DOI 10.1038/s41467-026-69750-0; OA CC-BY; 접수 2025-03-25/수리 2026-02-09) — "**A highly utilized and practical lithium-sulfur positive electrode enabled in all-solid-state batteries**". ⚠ inbox #104 파일명 "Bai2026" 은 오기(Shuang Bai 는 5저자) | ✅ 두 digest: `papers/cronk2026_lis_cathode_interphase_chemistry.md`(**계면화학·공정·복합체 σ — 이 표의 정본**) + `papers/cronk2026_lis_positive_electrode_geometry_fem.md`(기하/FEM → `comparison_vs_ours_DEM.md`) | exp (원자계산 0) |
| **[Liu24SbO]** | **Chong Liu**/**Tianran Zhang\***/R.Wang/B.Chen/**Dewen Wang**/T.Wang/Z.Yang/T.Liu/Q.Mao/T.Li/J.Zhang/X.Ma/**Xiangfeng Liu\*** 2024 ***Adv. Funct. Mater.* 2025, 35, 2412144** (中国科学院大学 **UCAS** + 中国原子能科学研究院 CIAE; DOI 10.1002/adfm.202412144, 접수 2024-07-09/온라인 2024-10-10) — "**Regulating p-Band Center of Sulfur in Li-Argyrodite to Stabilize Dual Solid–Solid Interface for Robust ASSLSB**". **레버 = Sb₂O₃ 공도핑** `Li₆P₁₋ₓSbₓS₅₋₂.₅ₓO₂.₅ₓCl` x=0.05 (Sb@P_4b + O@S_16e) ⇒ **S-p 밴드중심 ε_p −2.06 → −2.57 eV**. σ 2.6→**5.3 mS/cm** · 대칭셀 225 h→**4000 h** · CCD 0.6→**1.8 mA cm⁻²** · Li/S 풀셀 **932.6 mAh g⁻¹ 150 cyc 83.7 %**. ⚠ **ε_p 0.51 eV 정량 인용 금지** (`Fig. 5a` 의 LPSC PDOS 에 갭이 없어 **E_F 참조가 오염** — VBM 기준이면 figure-read ≈0.2 eV). **🔴 이 항목이 §I 에 걸린 이유**: 본문의 **「Li₂S 0.22 eV · LiF 0.67 eV」 는 자기 계산이 아니라 ref [30b] 소환값**이고, 그 [30b] 가 **[Lai20]** 이다 | ✅ `papers/liu2024_pband_center_sbo_dual_interface.md` | exp(NPD·XANES·TOF-SIMS·DRT) + **DFT 보조**(PDOS/p-band center·CI-NEB 1건·CDD) + CP2K AIMD 10 ps, 외부 |
| **[Lai20]** | **Chen Lai**/C.Shu/W.Li/L.Wang/X.Wang/T.Zhang/X.Yin/I.Ahmad/M.Li/X.Tian/P.Yang/**Wei Tang\***/**Naihua Miao\***(北航 — 계산 담당)/**G. W. Zheng\*** 2020 ***Nano Lett.* 20(11), 8273−8281** (西安交通大 + NUS + 北京航空航天大 + 上海空间电源 + IMRE A\*STAR; DOI 10.1021/acs.nanolett.0c03395, 원고ID `nl0c03395`, 접수 2020-08-20/게재 2020-10-27) — "**Stabilizing a Lithium Metal Battery by an In Situ Li₂S-modified Interfacial Layer via Amorphous-Sulfide Composite Solid Electrolyte**", 본문 9 pp + SI 22 pp. **🔴 이 항목의 존재 이유 = [Liu24SbO] ref [30b] 의 원출처** — 「Li₂S 0.22 eV · LiF 0.67 eV」 의 최종 귀속지. **✅ NEB 실재 확인**(SI `DFT calculation methods` 절 + `Fig. 3e/3f` MEP 실물 + `Fig. S11` "Present work") — VASP·PAW·GGA-PBE·520 eV·k-density 4/Å·진공 20 Å·**CI-NEB**(Henkelman 2000)·NEB 힘 0.05 eV/Å·`E_m = max(E_h−E_i), h>i`. ⛔ **슈퍼셀·원자수·이미지수·전하규약·슬랩두께 전부 미기재** ⇒ 우리 `v2/li2s` 와 **값 대 값 비교 금지**(§I·§E) | ✅ `papers/lai2020_li2s_interfacial_layer_amorphous_sulfide_cse.md` | exp(XPS·EIS·SEM·CV·풀셀) + **DFT 보조(CI-NEB·표면/계면 형성에너지)**, 외부 |
| **[Wang26IF]** | **Kangli Wang**/**W. G. Zeier**/**J. Janek**/**D. Mollenhauer\*** 2026 *Angew. Chem. Int. Ed.* **65**, e19663 (JLU Giessen + HIPOLE/HZB/FSU Jena + Münster; BMBF FestBatt 03XP0431; **OA**) — "**Interface Stability and Kinetics of Sulfide Electrolytes in all-Solid-State Batteries**": VASP-PBE/GGA+U + pymatgen **pseudo-binary(식 1–3) + grand-potential(식 4–5)** 로 계면 **6종** × (SE 7 · 양극 20 · 중간층/코팅 ~70 · a-Li_xSi 6) 전수 + **AIMD**(300 eV·Γ·NVT-Nosé·**80 ps**·dt 1 fs·500–1200 K) 로 **a-Li_xSi/Li₆PS₅Cl** 한 계의 계면 kinetics. **⚠ 실험 0건**(Janek·Zeier 공저인데도). **`zhu2015` 와 같은 기계의 2026년 대규모판.** ⛔ **수치표 0개**(결과가 전부 히트맵 색) · **산물 전자전도성 판정 0** · **W_ad·표면E·계면저항·두께 0** | ✅ `papers/wang2026_interface_stability_kinetics_sulfide_assb.md` | DFT 열역학 스크리닝 + AIMD (계산 100 %) |
| **[Ncube26]** ⭐⭐⭐ **§H "운동학 공백" 의 문헌 대응물** — 양극 CEI 를 *열역학이 아니라 시간·두께*로 친 유일한 digest · ⛔⛔ **LGPS/LCO 계 — A–D 물성 4축에 *수치로* 넣지 않는다**(아지로다이트 아님, 그리고 D 값 자체가 자기 그림과 재현 안 됨) | **Musawenkosi K. Ncube**(UIC)/**Pallab Barai**(ANL, 연속체)/S. C. Selvaraj/**L. A. Curtiss**/**Anh T. Ngo\***/**Venkat Srinivasan\*\*** (UIC 화공 + **Argonne National Lab** MSD/ACCESS/AMD) 2026 ***J. Energy Storage* 169, 122678** (DOI 10.1016/j.est.2026.122678; DOE-EERE **BMR**; 접수 2025-12-05/수리 2026-05-10; 본문 12 pp · **SI 미보유** · refs 84 · 그림 10 · 표 2) — "**Ionic interdiffusion at cathode\|solid-electrolyte interface: A machine learning–assisted multiscale investigation and mitigation strategies**". **계 = LCO\|LGPS** + 완화책 **LCO\|LNTO(LiNb₀.₅Ta₀.₅O₃)\|LGPS**. **5층 사다리**: DFT(VASP 5.4.4·PBE·PAW·600 eV·Γ·**U(Co)=5.9**) → AIMD(NVT-Nosé·300–900 K·±15 % 셀·≥5 ps·nat<300) → **DeePMD v2.2.7 DLP**(R_c 6 Å) → **MLMD**(LAMMPS·**nat>6000**·300 K·**3 ns**) → **1D phase-field + 2D 셀**. **이음매에 흐르는 것은 확산계수 단 하나**(`Fig. 1`). 소환값: 계면 D **Li 3e−12 / P 7e−12 / O 2e−12 / S 6e−13 / Ge 4e−14 / Co 8e−15 m²/s** · **두께 = 0.265·t^0.155**(*우리 역산: t = 초, 두께 μm*) → **24 h 에 >1 μm** · 압축 `figure-read ≈`**2.6 GPa @150 h** · V–Q `figure-read ≈` **LE 126 / LNTO 113 / LGPS 75 mAh/g** · Li↔Co 치환 **+0.144(LNTO) vs −1.109 eV(LGPS)** · W_ad **1.5605 vs 0.7306 eV/Å²**. **⛔ hull·ESW·NEB·COHP·DOS·자체 탄성계산·포논 전부 0 — 후처리가 MSD 하나뿐.** 🔴 **핵심 비판**: ① 상호확산이 **3면 중 1면**((010))에서만 ② `Fig. 5` PE·P 가 3.1 ns 까지 드리프트 ⇒ *"2 ns 평형"* 이 **자기 그림에 반박** (**`Fig. S5a` LNTO 가 "수렴한 PE" 를 보여주는 내부 대조군**) ③ **`Fig. 7` ↔ `Table 2` 재현 불가이고 불일치가 종 선택적** — 그들 창(0.4–1.9 ns) 안에서 그들 식(S9)으로 다시 계산해도 **Li 4× · P 2× · O 6× · S 20× vs Ge ≈330× · Co ≈560×** (= 보정 안 된 COM 드리프트의 지문) ⇒ **이 논문의 D 는 우리 문서에 소환값으로도 싣지 않는다** ④ 🆕SI **압력이 −3~+3 μm 전 도메인 균일**(순수상에도 2.64 GPa) ⇒ 성장지수 0.155 가 **1D 구속의 산물**일 수 있다 ⑤ 🆕SI **성능모델이 MLMD 의 D 를 안 쓴다**(`Table S3` κ_LGPS 1.0 S/m · D_Li,LCO 2e−14 **둘 다 문헌값**) ⇒ 같은 물질 Li 수송이 논문 안에 **두 값(≈50× 차)** 으로 공존 ⑥ 🆕SI **"부정합 <5 %" 는 평균** — 실제 **ε₁₁ = −8.94 %** ⑦ 🆕SI `Table S3` 캡션이 **"NMC\|LBCO\|LLZO"**(Barai 2021 복붙). ⚠ 연속체 층은 **맞춘 매개변수 4개**(열화분율 0.6 · i₀ ×0.15/×0.2 · 박리 30 %). ⚠ **전압·전류·SOC 없음**(완전 리튬화 LCO). ⛔ **초판 정정(2026-09-22)**: *"확산영역 검사를 안 했다"* 는 **철회** — SI 가 β 판정 + **적합창 0.4–1.9 ns**(표본간격 1·10 ps)를 명시한다. ⭕ **유일하게 값으로 이어지는 칸 = 탄성**(§C 신설행·§7d-2): `Table S2` 의 **E(LGPS) 20 GPa 출처가 [Deng16]** 이고, 그 논문 Li₆PS₅Cl 22.1 이 **우리 comp1 22.06 과 0.2 % 일치**(기검증) ⇒ **우리 SE 는 `Fig. S10e` 의 "박리 없음" 칸**(⛔ 칸만, MPa 이식 금지) | ✅ `papers/ncube2026_ionic_interdiffusion_lco_lgps_multiscale.md` (2026-09-22 초판 → **같은 날 SI 반영 개정**; 본문 **그림 9/10 + 표 2 실독**, **SI 텍스트 전문 + SI 그림 5/13 실독**) | **계산 100 %** (DFT+AIMD+MLIP-MD+1D상장+2D FEM) · 외부 · **운동학 축 전용 — 물성 4축 수치 비교 제외(단 §C 탄성 *분류* 만 예외)** |
| **[Zeng26Gar]** ⛔⛔ **산화물 가넷 — 물성 4축 진입 금지** · 🧭 흡착 보고량 *선언 공백* 의 표본 | **Ye Zeng**/**Yaqiong Zhu**(공동1)/Z.Hou/X.Gong/**Yanan Yang\***/**Tao Zhang\*** (**中国科学院 上海硅酸盐研究所 SICCAS** + UCAS) 2026 ***Energy Storage Mater.* (in press)** DOI `10.1016/j.ensm.2026.105526` · PII `S2405-8297(26)00658-6` · 접수 2026-06-15/수리 2026-09-11 · ⚠**Journal Pre-proof(VoR 아님)** — "**Unlocking the Naturally Chemical Stable Garnet Electrolytes via Lithium Site-Specific Decoupling Substitution**". **GaCl₃ 진공 기상 이온교환(15:100 질량비·10⁻³ Pa·250 °C 4 h)으로 가넷 LLZTO 의 *팔면체(96h/48e) Li 만* Ga³⁺ 로 치환** → `Li₆.₄La₃Zr₁.₄Ta₀.₆O₁₂ + 0.46 GaCl₃ → Li₅.₀₂Ga₀.₄₆La₃Zr₁.₄Ta₀.₆O₁₂ + 1.38 LiCl`. 소환값: σ_RT **4.95**(모체 4.62)×10⁻⁴ S/cm · Ea **0.34/0.35 eV** · 대기 **120일 Li₂CO₃ 무검출**(모체 48 h 에 σ −62 %) · **E_ads(NMP/La/(100)) −2.44 → −1.63 eV**. 계산 = **DMol³/MS 2019 · PBE · DNP(3.5) · ECP · 실공간절단 5.0 Å · DFT-D(버전 미기재)** 뿐 — **슬랩·진공·k-점·스핀·정의식 전부 미기재**. ⇒ **§J-7 `[Zeng26Gar]` 블록에만** 있다 (A–D 4축 금지) | **EXTERNAL / 가넷 / 방법 반면교사** |
| **[Ziemke26AP]** ⛔⛔ **산화물 antiperovskite · arXiv 프리프린트 — 물성 4축 진입 금지(넣을 값이 0건)** · 🧭 **치환결함 형식론의 *음성* 표본** | **Carson D. Ziemke**²³†/**Naveed Naemi**³/**Ha M. Nguyen**¹²⁵†\*/A. Dorhauer³/C. Garcia⁴/N. Narayanan²/Y. Xing¹⁴/J. Gahl²/T. W. Heitmann¹²³/**Carlos Wexler**¹³\* (**University of Missouri** MSEI + **MURR 연구용 원자로** + 물리천문 + 화공 · **VinUniversity** 하노이) 2026 **arXiv:2609.12300v1** [cond-mat.mtrl-sci] (2026-09-11 · **미심사**; 본문 19 pp + refs 4 pp · **SI 없음** · refs 37 · **그림 3장 · 표 2장**) — "**Ab initio Study of Substitutional Defects in Li₃OCl Solid Electrolyte for Li-ion Batteries**". ⚠ 표기 DOI `10.32469/10355/97710` 은 **기관 리포지터리 핸들(저널 DOI 아님)** ⇒ **원고·SI 인용 금지**. **중성자 변환 결함공학**(⁶Li+n→³H+α 940 barn · ¹⁰B+n→⁷Li+α+γ **3,840 barn** · ¹⁵⁷Gd 2.55×10⁵ barn)을 근거로 **H·He·B** + 통상 도펀트(Na·K·Mg·Ca·Ba·Al·Gd) **10종을 Li 자리에 치환**하고 QE vc-relax. 방법 = **QE(버전 미기재)·PBE·PAW PSLibrary v1.0.0(파일명 미기재)·ecut 100/400 Ry(4×)·5×5×5 MP 고정·BFGS 10⁻⁵ Ry/Bohr·Gaussian smearing 0.01 Ry**, `E_f = E_def − E_perf + E_Li − E_A`. **⛔ 물성값 0건** — σ·Ea·ESW·gap·DOS·C_ij·NEB·AIMD·Bader·COHP **전부 미시행**(저자 §4 자인). ⇒ **§J-7 `[Ziemke26AP]` 블록에만** 있다 | ✅ `papers/ziemke2026_li3ocl_substitutional_defects.md` (2026-09-22, **그림 3/3 전부 실독** + 표 2장 PDF 텍스트 전수 전사·산술 검산) | **EXTERNAL / 산화물 antiperovskite / ⛔프리프린트 / 방법 반면교사** |
| **[Tu27ML]** | **Junye Tu**/Chen/Xu/Qiu/Yang/Xue/**Ningbo Liao\*** 2027 *J. Mater. Sci. Technol.* **280**, 18–26 (温州大 Wenzhou Univ. 기전공학원 **단일기관**; NSFC 51675384·51202164; DOI 10.1016/j.jmst.2026.05.071, 온라인 **2026-06-12**) — "**A diffusion descriptor integrated machine learning approach toward the discovery of solid-state electrolytes for lithium metal batteries**": **CASTEP-PBE/ultrasoft 380 eV·3×3×1·진공 20 Å** 로 SSE 6종 × 도펀트 28종 = **174 Li/SSE 계면**의 γf·W_ad·E_ads·**CI-NEB E_B** 를 라벨화하고, **전해질 층을 얼린 '동결 모델'**(full 의 1/10 시간)에서 같은 양을 미리 계산해 기술자로 넣어 **GBRT/RF** 로 예측(γf **R² 0.99**·E_B **R² 0.93**) → 876 조합에서 21 후보 → **4종 DFT 재검증**. ⚠ **실험 0건 · 데이터/코드 공개 0 · AIMD 조건 전무.** ★ **우리 cascade ML 과 같은 영역이라 CV 규약 판정의 기준 사례**(J-8) | ✅ `papers/tu2026_diffusion_descriptor_ml_li_sse_interface.md` | DFT(계면 슬랩)+NEB+AIMD+고전 ML 회귀 (계산 100 %) |
| **[Jung26]** 🤝 **[공저 인접 — 한양 Y.Lee·J-W.Lee 참여, 우리 랩 저자 없음]** | **Jae Yup Jung**/**Seung Ho Choi\***/M. Ha/C.H. Baek/S.W. Nam/**Yeokyung Lee**/**Jong-Won Lee**/D.-J. Yoo/**Haesun Park\*** (중앙대 — DFT 담당)/**Min-Sik Park\***/**Woosuk Cho\*** (KETI 차세대전지 + 경희대 + 가천대 + 중앙대 + 고려대 + **한양대**) 2026 ***Adv. Funct. Mater.* 2026, e78249** (DOI 10.1002/adfm.78249; 접수 2026-06-05/수락 2026-08-31) — "**Enhancing the Mechanical Properties of Solid Electrolytes for Crack-Resistant Cathodes in All-Solid-State Batteries**": SiO₂ 공급원으로 **Si⁴⁺→P⁵⁺(4b)·O²⁻→S²⁻(16e) 공치환** → **Li₆.₁P₀.₉Si₀.₁S₄.₈O₀.₂Cl**. **DFT 는 `Fig. 2a` 한 장이 전부**(VASP PBE/PAW, ecut 700 eV, k 3×3×3, 52 at, pymatgen 전수열거→최저에너지 단일배열, **Murnaghan EOS 6점 V/V₀ 0.96–1.02, 격자고정+원자완화=relaxed-ion**) — **B₀ 만 산출, C_ij·G·ν 없음**. 나머지는 전부 실험(XRD·XPS·³¹P NMR·AFM QNM/나노인덴·EIS/DRT·단면 SEM 피복률·나노-XCT). | `papers/jung2026_sio2_cosubstitution_mechanical_argyrodite.md` (2026-09-22, 본문 그림 **6/6 실독** · **SI 그림 미보유**) | mixed (exp 주도 + DFT 보조) · **[공저 인접]** |
| **[Famprikis19]** | **Famprikis**/Canepa/Dawson/**M. S. Islam\***/**C. Masquelier\*** 2019 *Nature Materials* **18**, 1278–1291 (Amiens LRCS·RS2E + Bath) — "**Fundamentals of inorganic solid-state electrolytes for batteries**", 11 pp 튜토리얼 리뷰. **자체 계산·실험 0 → 전 수치가 소환값(2차 인용)**, 대부분 "≈" 반올림·오차 삭제. 4기둥 = **다중스케일 수송**(`Fig. 2` Å→cm 사다리) · **전기화학 안정성**(`Fig. 4`·`Fig. 5`·`Table 1`) · **역학**(`Fig. 6`·Box 1) · **공정**(`Fig. 7`). 우리 digest **5편을 직접 인용하는 허브**([Deng16]=ref110 · [Bucci17]=ref109 · [Bielefeld19]=ref68 · [Sakuda13]=ref58 · [Richards16]=ref65 · [Kraft]=ref29) | ✅ `papers/famprikis2019_fundamentals_inorganic_sse.md` | **review · 소환값 전용 — 절대값을 우리 표와 같은 칸에 넣지 않는다.** 축 정의·기전 근거로만 인용 |
| **[Mulks24]** | **Mulks** 2024 *Chem* **10**, 2724–2744 (단독 저자, RWTH Aachen) — "**Hard and soft electrons and holes**": HSAB 를 **전자/홀의 hard–soft** 로 확장한 개념화학(HSEH). **EHR** `f^(2,±)(r)` / **EHI** `f_k^(2,±)` = 전자수에 대한 밀도(또는 원자전하)의 **2차 유한차분**, 고정 기하 단일점 3회로 계산(ORCA·DSD-BLYP-D3BJ/def2-QZVPP//PBEh-3c·기체상·Hirshfeld). **양=hard·음=soft**. ⚠ **분자 유기·유기금속 전용 — 무기 고체/황화물 적용 선례 0건, 정량 예측 모델 아님**(저자 명시). `fan2026` 리뷰 §3.1 ref [80] 의 원전 | ✅ `papers/mulks2024_hard_soft_electrons_holes.md` | **[EXTERNAL] theory framework only — 물성 4축 수치 비교 제외** |
| **[Miao23]** | **Miao/Guan/Ma/Liangliang Li\*/Ce-Wen Nan\*** 2023 *Adv. Mater.* **35**, 2206402 (Tsinghua + USTC) — "**Role of Interfaces in Solid-State Batteries**", 21 pp **계면 전용 리뷰**. **자체 계산·실험 0**(본문에 DFT/first-principles/band gap/VBM **0회**) → **수치 행이 아니라 프레임 행으로만** 이 문서에 들어간다. 산출물 = **F1 계면 3층위** / **F2 Li·SE 계면 3유형**(열역학 안정·**MCI**·passivating SEI) / **F3 μ_c↔HOMO 정렬**(Fig 4c) + **Table 1·2·3**(압력↔성능 15행 / CAM 코팅 19행 / **Li‖SE 버퍼 27행**). **`fan2026_…ECERD2600097`(Nan 공저, 심사 중)의 3년 전 선행 리뷰** — digest §10 이 상속/신규/**누락**/상충을 전수 대조 | ✅ `papers/miao2023_role_of_interfaces_solid_state_batteries.md` | **review · 프레임 전용 — 물성 4축 *수치* 비교 제외** |
| **[Shin26]** | **Shin/Han/Kim**(공동1저자 3인)/…/**Sangdoo Ahn\***/**Sang Uck Lee\***/**Young Whan Cho\***/**Young Joo Lee\*** 2026 ***Small* 22, e73722** (KBSI + 중앙대 화학 + KIST 수소에너지소재 + **성균관대 화공 = 이상욱 랩**) — "**Enhancing Li⁺ Ion Transport via Dynamic Coupling With Borohydride Reorientation in Li₆PS₅X Argyrodites**". **⭐⭐ 우리 물질 그 자체**(Li₆PS₅X). `Li₇₋ₓ₋ᵧPS₆₋ₓ₋ᵧ(BH₄)ₓClᵧ` 3조성 σ 16.4/7.9/0.7 mS/cm(EIS). **BH₄⁻ 는 halide/free-S²⁻ 자리(4a·4d) 점유**. **coupling 을 3중으로 측정**(⁷Li↔¹¹B SLR Ea 일치 · 회전구속 AIMD D 2–3배↓ · hop 31건 중 28건 동반). 계산은 **AIMD(VASP/PBE/Γ/80원자/500–900 K)**, 무질서 = **BH₄ 배향 4배열 Boltzmann 가중**. ⚠ **계산 σ 는 자유 파라미터 2개(χ_c 0.6↔0.8, 차원 불성립 가중식)로 지탱** — 우리가 3자리 재현해 확정 | ✅ `papers/shin2026_bh4_reorientation_li_transport_li6ps5x.md` | **exp 주(EIS·XRD-Rietveld·MAS/SLR/PFG/EXSY NMR·SEM) + AIMD 보조** — **σ·D 절대값은 소환값, 계산 σ 는 인용 금지** |
| **[Lynch26GK]** 🔧방법 원전 · ⛔물성 4축 아님 | **D. Cory Lynch** (Wake Forest Univ. Physics, 지도 **N. A. W. Holzwarth**) **박사학위논문 2026-08** (234 pp; NSF DMR-2242959) — "A Computational Investigation of Solid Electrolyte Materials Using First Principles and Machine Learning Methodologies". **인용은 부록의 두 산출물로**: ① Lynch/Y.Li/**P. Canepa**/Holzwarth ***Phys. Rev. Materials* 8, 065401 (2024)** DOI `10.1103/PhysRevMaterials.8.065401` ② Lynch/**C.W.Tan**/**B. Kozinsky**/Holzwarth **preprint dated 2026-08-03, DOI 없음**. **계**: (thio)boracite 8종 · **Li₃.₂₅P₀.₇₅Si₀.₂₅O₄**(ML 시험대) · 아지로다이트 ZnO 3종(**미출판·중단**). **Allegro + LAMMPS NVE 2.8 ns × 속도 10 × 모델 5** 로 **full Green-Kubo σ** 와 **tracer** 를 같은 궤적에서 비교, **H_R = 0.53–1.03**. ⛔ 아지로다이트 물성값 0건 | ✅ `papers/lynch2026_greenkubo_mlip_conductivity_thesis.md` (2026-09-22, 그림 **11/20 실독**) | **[외부]** 계산 100 % (자체 실험 0) · **§J-7 방법 원전 전용** |
| **[Zuo]** | Zuo 2022 Angew — 양극 계면 chlorination | ✅ `papers/zuo2022_chlorination_cathode_interface.md` | exp |
| **[Qian26]** | Qian/Dean/Kochetkov/Chen/Huang/**Nazar** 2026 Angew (e9983580) — **SE 입자 유기(데칸산) 표면코팅**: 수분(39 % RH 2 h σ 91 %) + 양극(무코팅 NCM85 150cyc 96 %) + 음극(대칭셀 1000 h) 동시. **[Adeli]/[Zuo]와 동일 Waterloo/Nazar 그룹** | ✅ `papers/qian2026_decanoate_coating_lpscl_moisture_interface.md` | exp + DFT보조(슬랩 표면E·분자흡착) |
| **[Qian25]** | **Lanting Qian⁺**/**Yangyang Huang⁺**/Dean/**Kochetkov**/**B. Singh**/**Nazar\*** 2025 *Angew. Chem. Int. Ed.* **64**, e202413591 (Univ. Waterloo; BASF+NSERC; OA CC-BY) — "**Engineering Stable Decomposition Products on Cathode Surfaces…**": **LiPO₂F₂(LiPOF) 를 NCM85 입자에 1 wt% 용액코팅(~35 nm 비정질, 소결 0)**. 근거는 **convex-hull 3종**(element profile / 닫힌 pseudo-binary / grand-potential 계면반응, VASP+pymatgen+MP). **[Adeli]→[Zuo]→본 논문(2025)→[Qian26](2026)** = Waterloo/Nazar 라인 4번째, **[Qian26] 과 1저자 동일** | ✅ `papers/qian2025_lipo2f2_coating_stable_cei.md` | DFT(hull) + exp |
| **[Deng26PS]** | **Deng⁺/Tang⁺**/Lin/Chen/**Hui Li\***/Cao/Fang/Qian/Yang/**Xinping Ai\*** 2026 *Angew. Chem. Int. Ed.* **65**, e202520531 (武汉大 Wuhan Univ. + 武汉纺织大) — "**A Surface Non-Destructive Modification Strategy Addressing Moisture and Oxidation Instabilities of Sulfide SSEs**". **표면 S²⁻ 개시 DTD 개환중합 → ~10 nm poly(sulfate)(PS) 층**. exp 주 + **DFT 보조는 H₂O 흡착E 2값이 전부** (VASP 5.4.4·PBE·PAW·550 eV·**Γ-only**·**vdW 없음**·LPSC **(011) 슬랩(종단·크기·무질서 미기재)** vs **고립 삼량체**·**자리 샘플링 없음**). ⛔ **AIMD·NEB·COHP·DOS·Bader·ELF·ESW·탄성·phonon 전무.** **[Qian26] 과 같은 저널·같은 해·같은 문제의 자매 논문**이고 **둘 다 슬랩/흡착부 vdW 누락** — 이 분야 관행 (우리 차별화 지점) | ✅ `papers/deng2026_polysulfate_layer_moisture_oxidation_lpsc.md` | **exp 주(코팅·전기화학) — 소환값. DFT 값은 정성 방향까지만.** 축 ②(전자 접근 차단)·④(수분) |
| **[LiGaF]** | Yaru Li/**Dabing Li**/**Yang Li**/Zhang/Qi/**Li-Zhen Fan** (**USTB — [Fan26] 리뷰·[Li25] CuBr₂와 같은 연구실**), "**Dual-Functional Ga/F Co-Doped Argyrodite Sulfide Electrolytes for ASSLBs**" (**Energy Mater. Adv. 2026;7:0227**, DOI 10.34133/energymatadv.0227, 출판 2026-04-27) — `Li₅.₅₊₂ₓP₁₋ₓGaₓS₄.₅Cl₁.₅₋₃ₓF₃ₓ` x=4 %(=Li₅.₅₈P₀.₉₆Ga₀.₀₄S₄.₅Cl₁.₃₈F₀.₁₂), host=[Yang25]와 동일 Li₅.₅PS₄.₅Cl₁.₅. **한 염 두 도펀트 5번째**([Taklu]CuCl→[Liu23]MgF₂→[Li25]CuBr₂→[Yang25]La₂O₃→본편 GaF₃), 자기 선행 = **InF₃**(ref[4] AEM 2024, [Fan26]이 인용한 그것) | ✅ `papers/liyaru_gaf3_codoping_argyrodite.md` **(본문+SI 통합)** | exp + DFT보조(SE 슬랩 NEB·Li 금속 슬랩 NEB·H₂O 흡착E·이성분 DOS) |
| **[LiInF]** | **Dabing Li**†/Xinyu Liu†/**Yang Li**/Zhao/Wu/Qi/Gao/**Li-Zhen Fan** (**USTB — [Fan26] 리뷰·[Li25] CuBr₂·[LiGaF] GaF₃ 와 같은 연구실**), "**A Versatile InF₃ Substituted Argyrodite Sulfide Electrolyte toward Ultrathin Films for ASSLBs**" (**Adv. Energy Mater. 2024, 14(47), 2402929**, DOI 10.1002/aenm.202402929, 출판 2024-10-10) — `Li₅.₇₊₂ₓP₁₋ₓInₓS₄.₇Cl₁.₃₋₃ₓF₃ₓ`, host **Li₅.₇PS₄.₇Cl₁.₃**; **In→P 4b · F→Cl 4a**. **[LiGaF] 가 자리 배정을 이 논문에서 그대로 인용(ref [34]) = "한 염 두 도펀트" 계보의 앞칸** (InF₃ 2024 → GaF₃ 2026). ⭐ **[Fan26] 리뷰 §3.2 가 인용한 바로 그 논문(ref [97], Fig 4c)** — 리뷰어 노트 **A12·A13** 판정 근거. ⚠ 헤드라인 시료 둘: **x=0.02 σ 챔피언 5.6** vs **x=0.06 "LPSCInF" 안정성 주인공 σ 4.0 mS/cm**. **★ 본문 실물 재검증 `2026-08-06`(inbox #55)**: 교정 1(**"본문 800 h" 지적 철회** — 본문도 2000 h) · 신규 4(**⑯ 산화/환원 뒤바뀜**(→ §B 새 행) · **⑰ Li–In 표면에너지 0.40 eV Å⁻²=6.4 J m⁻² = Li 실측의 10–20배 단위오기** · **⑱ "carrier↑ + vacancy↑" 동시 주장 불가** — In³⁺→P⁵⁺ 는 Li 를 늘려 vacancy 를 *줄인다*; **우리 comp1→modelc 의 "Cl↑→Li↓→vacancy↑" 와 정반대 방향**이므로 **이 논문의 σ 상승을 vacancy 서사로 인용 금지**(§A) · **⑲ "Figure 4e"→실제 `Fig. 3e` 오지칭**) · 출처 정밀화 1(**In-only 7 / F-only 4.3 은 SI 가 아니라 본문 인쇄** ⇒ A13 논거 강화) | ✅ `papers/li2024_inf3_argyrodite_ultrathin_film.md` **(본문+SI 통합 · §14 재검증)** | exp 주 + DFT 보조(자리 E_f · 슬랩 NEB · Li/Li–In 슬랩 NEB · H₂O/유기용매 흡착E · PDOS) |
| **[Cronau]** | Cronau/Szabo/König/Wassermann/**Roling** 2021 ACS Energy Lett. 6, 3072 — "How to Measure a Reliable Ionic Conductivity? **The Stack Pressure Dilemma** of Microcrystalline Sulfide SE" (Marburg, Viewpoint 6 pp). 황화물 SE **6종 × 3 결정도 클래스**(비정질/유리세라믹/**미세결정**)를 stack pressure 0–500 MPa 로 스윕 — **미세결정만 50–250 MPa 에 두 번째 압력 의존 구간**(입자 간 gap 을 닫는 데 추가 압력이 필요) | ✅ `papers/cronau2021_stack_pressure_ionic_conductivity.md` | exp (측정법) |
| **[Trevi]** | Trevisanello/Ruess/Conforto/Richter/**Janek** 2021 Adv. Energy Mater. 11, 2003400 — 다결정(PC) vs 단결정(SC) **NCM811**: 입자 균열·활성표면적(Kr-BET)·Li 확산. ⚠ **액체전해질 셀**(1 M LiPF₆ EC:DEC) — ASSB 아님 | ✅ `papers/trevisanello2021_sc_pc_ncm_cracking_diffusion.md` | exp |
| **[Ke]** | Ke 2025 ESM — MgClO 음극 혼성 도핑 | ✅ `papers/ke2025_orbital_hybridization_mgclo.md` | exp+DFT |
| **[WangYO]** | Dewen Wang/Chong Liu(공동1)/**Xiangfeng Liu** 2025 Angew **VIP** (64, e202501411) — **Y₂O₃ 공도핑 argyrodite "electronic localization"** (UCAS·CSNS, **외부**): LPSC(=comp1)→**Li6.1P0.95Y0.05S4.925O0.075Cl**(본문 "S4.25O0.75"는 오타; Y@P4b 주장+O@S16e). σ ~2.75→**3.53 mS/cm**·Ea ~0.375→**0.34**·σ_e 6.33e-7→**1.55e-7**(⚠베이스라인이 타 문헌 pristine 대비 60–200×)·H₂S ~0.47→~0.30 cm³/g·CCD 0.7→**1.5**·대칭셀 **>4800 h**·LCO/Li-In 0.5C 1300cyc "100%"(LiDFOB-coated 별도 catholyte·저활용). 계면 Li₂S 21.3→9.9%/Li₃P 9.0→3.6%+**Li₂O 528.5 eV**(XPS depth+SIMS 3D+DRT). 기전=ELF/PDOS **d–p 혼성**+Madelung −166.51→−175.07 eV/atom(LOBSTER; COHP/COBI 계산 명시 후 미제시). ⚠**BVSE 1.11→0.61 eV "절반"을 σ 서사로 — 자기 실측 Ea(0.375/0.34)와 3× 불일치**; Y@P4b(형성E 2배열+constrained Rietveld)는 우리 M³⁺ cascade site-rule(26/26 **Li_24g**)과 정면 충돌. **[2차 픽셀 패스 2026-08-04]** 세 축이 새로 정해짐: **①축 D(전자구조) ✓✓ 정합** — 그들 Fig 5e PBE PDOS가 우리 **comp1 gap 2.066**(그림 실측 ≈2.07)·**VBM=S 3p 독점**(P-p는 S-p의 2%)·**LPSOCl의 O 2p 매몰**(O-p 무게 82%가 E<−2 eV)을 전부 독립 확인 → 우리 세 결과의 외부 교차검증 카드(단 DOS-threshold 판독이라 절대값 인용·db 편입 금지); **②그 대가로 논문 본문의 "p–p hybridization at the Fermi level"은 자기 그림에 반박됨**(p–p 결합상태는 −4.4 eV) — PDOS를 정성 그림으로만 쓰면 생기는 오류의 교보재; **③축 A(이온) ✓ 우리 쪽과 방향 일치** — σ 1.29×/ΔEa 0.040 eV는 **σ₀ 3.6× 감소**를 요구해 그들 "carrier 증가·채널 확장" 설명과 모순이고, 오히려 우리 cascade(M³⁺는 Li 이동도 거의 불변·Nd blocking 0.52×)와 같은 방향. **[3차 SI 실물 패스 2026-08-04]** 네 축이 더 정해짐: **④축 D(전자수송) — "σ_e 4× 감소"는 정의 의존**(Fig S9/S10 실측: 비 22×→1.8×, 기울기 기준은 **YO가 1.8× 높아 역전**; 보고값 재현 불가) → 우리 쪽 "베이스라인 이상 = 시료 품질 의심" **철회**(실측치는 [Li25] 1.02e-8·[Taklu] 8.75e-9와 같은 자릿수), 대신 **σ_e를 단일값으로 인용 금지**; **⑤site-rule 위상 변화 — 그들 Y@P 근거가 방법론적으로 무효**(조성이 다른 두 모델의 원자당 원자화E 비교, 전하 보상 없음) → **우리 cascade M³⁺ = Li_24g 를 반증하는 외부 계산은 존재하지 않는다**; 대립은 "우리 UMA 결과 vs 그들 constrained Rietveld"만 남고 검증 계산의 가치는 상승; **⑥축 A(이온) 재확인 — Fig S11 전셀 BVSE 등가면이 도핑 후 79.9→76.3 %로 감소**(빈 공간 1.67×) → 2차의 σ₀ 3.6× 감소와 **두 번째 독립 증거**, 우리 cascade(M³⁺는 이동도 거의 불변·Nd blocking)와 같은 방향; **⑦축 E(계면) 유지 — Fig S17 파이 각도 실측으로 Li₂S 21.3→9.9 % 헤드라인 확정**(합 110.3 %의 범인은 "89 %" 라벨) → 계면 XPS/SIMS 정량은 이 논문에서 **믿고 쓸 수 있는 부분**으로 확정. 기타: SI 안에 DFT 구조가 3개(O 자리 Cl/S·개수 2/5)라 우리 LPSOCl(O@S)과의 비교는 **방향성까지만** 유효; Li6.16P0.92In0.08S4.88O0.12Cl(AFM 2024)이 **같은 일반식의 선행 설계**; 우리 자기교정 1건(Fig S15 = LPSC 조기 단락 아님, 96 h 안정 후 종료) | ✅ `papers/wang2025_electronic_localization_yo_argyrodite.md` (§18·§19) | exp+DFT/BVSE보조 |
| **[GG]** | Gil-González 2022 ESM — constrained ESW (구속) | ✅ `papers/gilgonzalez2022_synergistic_cl_constricted_esw.md` | DFT+exp |
| [Wu] | Wu 2026 Nano Energy — calendar aging | 📄 db/properties/oxidation_stability.json | exp |
| **[Banik]** | Banik/Liu/Ohno/.../**Yifei Mo**/**Wolfgang Zeier** (Münster·Maryland·Kyushu·DESY) — "**Can substitutions affect the oxidative stability of Li₆₊ₓMS₅X?**" (M=P→Si/Ge, X=Cl→I). **답: 거의 안 바꾼다** — HAXPES VBM(불변)+광학 gap(>3 eV)+DFT **pDOS/COHP**+**grand-potential 분해창**+**stepwise CV**가 일관되게 **VBM=자유 S²⁻ + PS₄³⁻ 비결합 S 3p**임을 보임 → "S가 산화 onset을 pin → 단순 치환으론 황화물 SE 산화 안정성 개선 불가, 코팅/타 물질군 필요". **🔑🔑 우리 `axis_1`(intrinsic onset DRAW)·VBM≠onset·grand-potential 방법의 *외부·동방법·동그룹(Mo) 정답지*** | ✅ `papers/banik2022_substitutions_oxidative_stability_argyrodite.md` | DFT(phase-stability)+HAXPES+CV |
| **[Liu]** | Liu/Zhong/Wang/**Tu** 2022 AdvFM (32, 2207978) — Cl 치환 **결정화(annealing) + Li-metal 계면** (Zhejiang Univ., **외부**). σ 2.62→**8.0 mS/cm**(@450)·Ea **0.28**·Rietveld 4d 무질서 13.3→**61.7 %**·격자 9.85→9.81 Å. **음극 초점**: AIMD Li 확률밀도 **intra→inter-cage 활성화**(MSD 3×)·계면 P–S RDF PS₄ LPSCl 10 ps / Cl-rich **35 ps** 유지·**LiCl-rich SEI**(XPS). CCD 0.95→**1.40**·대칭셀 500 h·NCM811 full(Li) 30.6→**80.4 %**. ⚠ **≠ Zuo** | ✅ `papers/liu2022_cl_crystallization_interface_argyrodite.md` | exp+DFT/AIMD보조 |
| **[Lu]** | Lu 2025 CEJ — 음극 4d-Cl 자기분해 → LiCl interphase (gap 1.88/LiCl 6.22) | ✅ `papers/lu2025_tailoring_cl_rich_anode_licl.md` | exp+DFT |
| **[Liu23]** | Liu 2023 Angew — MgF₂ 공도핑 electron redistribution (redox-resistible, σ_e 8×↓) ⚠[Liu]≠이것(=Liu 2022 AdvFM) | ✅ `papers/liu2023_electron_redistribution_redox_resistible_mgf2.md` | exp+DFT |
| [Ma] | Ma 2026 J.E.S. — In doping, PBE gap 2.10→2.62 | ⬜ PDF | DFT |
| **[Li25]** | Li/G.Wu/L-Z.Fan/C-W.Nan 2025 ESM (77, 104221) — **CuBr₂ 이원(Cu+Br) 도핑** argyrodite (USTB·Tsinghua·Heze, **외부**): LPSC-P(Li₅.₅PS₄.₅Cl₁.₅)→LPSC-CB(Li₅.₈P₀.₉Cu₀.₁S₄.₅Cl₁.₃Br₀.₂). σ 5.3→**10.3 mS/cm**·Ea 0.295→**0.239**·gap 1.82→2.41·**σ_e 1.02e-8→3.35e-9 S/cm(실측)**·CCD 0.6→**1.9 mA/cm²**. 분해산물 gap(DFT) **LiCl 6.13/LiBr 5.07/Li₂S 3.04**; 물흡착 ΔE 0.29→**2.42 eV**(Cu–S>P–S, HSAB) | ✅ `papers/li2025_cubr2_dualdoping_argyrodite.md` | exp+DFT보조 |
| **[Taklu]** | Taklu/W-N.Su/She-Huang Wu/**Bing Joe Hwang** 2021 Nano Energy (90, 106542) — **CuCl 이원(Cu+Cl) 도핑** argyrodite (NTUST 대만·NSRRC, **외부**): **LPSC-P=Li₆PS₅Cl(=우리 comp1)**→LPSC-1=Li₆.₃P₀.₉Cu₀.₁S₄.₉Cl₁.₁. σ 1.11→**4.34 mS/cm**·Ea ~0.30→**0.25**·**σ_e 8.75e-9→1.49e-9 S/cm(실측, 최저)**·CCD 0.75→**3.0 mA/cm²**(4×, 2400 h@0.1). Cu→4b(P자리)·Cl→4a/4c·**48h-Li 거리 3.298→2.997 Å**. CV 분해전류 **160×↓**·"**8 V ESW**(⚠ vs In/InLi·carbon-composite=*kinetic*, intrinsic 아님)". **Cu₃PS₄ 형성**(HSAB soft-acid Cu)→oxophilicity↓→**H₂S 1.07→0.49 cm³/g**. ball-mill-free 고상·**full cell 없음**. **[Li25] CuBr₂의 4년 앞선 자매**(CuCl vs CuBr₂·stoich vs Cl-rich 모체·VASP/PAW Li-path) | ✅ `papers/taklu2021_cucl_dualdoping_air_stability_argyrodite.md` | exp+DFT보조(Li-path) |
| **[Ma24]** | Ma/**Ping Li**/Shi/Sun/Fu/Wang/Fang/Han/**Xuanhui Qu** 2024 JMCA (12, 27011) — **Sb-기반 argyrodite(LSSSI=Li₆.₄Sn₀.₆Sb₀.₄S₅I)를 P-기반 LPSC에 *구조통합*(Sn⁴⁺·Sb⁵⁺·I⁻ 삼중치환)** (USTB 北京科技大, **외부**): **LPSC-0=Li₆PS₅Cl(=우리 comp1)** → LPSC-0.05=Li₆.₀₂Sn₀.₀₂Sb₀.₀₃P₀.₉S₅Cl₀.₉₅I₀.₀₅. σ 3.4→**5.2 mS/cm**·Ea 0.29→**0.25**·**σ_e 3.4e-9→2.0e-9 S/cm(실측)**·CCD 0.5→**1.4 mA/cm²**(6000 h). **DFT Li 장벽 intra 0.873→0.496·inter 0.976→0.592 eV**(inter>intra). 음극 in-situ **LiI+Li-Sn/Sb 합금**·계면반응E −0.595→−0.539 eV/atom. 대기안정(**HSAB soft-acid Sn/Sb–S**): H₂S 1.38→~0.3 cm³/g·**공기노출 후 NCM811 180.7 mAh/g·200cyc 75.4 %**. NCM811@Li₂O 181 mAh/g·83.1 %. **gap·산화 onset 미보고**. **[Li25]CuBr₂·[Taklu]CuCl의 multi-doping 자매(같은 USTB·Ping Li/Fan 계열)**. ⚠ **DFT 파라미터 전부 미공개** | ✅ `papers/ma2024_sb_doping_lpsc_conductivity.md` | exp+DFT보조(Li-path, 파라미터 미공개) |
| **[Rao]** | Rao/Rempel/Jiang/Adeli/Yim/Houache/Abu-Lebdeh/**Chandra Veer Singh** 2025 JMCC (13, 10733) — **요오드(I) 치환 Cl–I 혼합 할라이드-rich argyrodite** *순수 DFT+AIMD(실험 0)* (Univ. Toronto·Anhui·Waterloo·NRC Canada, **외부**). Li₆₋ₓPS₅₋ₓCl₁.₅₋ₓIₓ. **Cl–Br 정면비교**: 상안정 E_hull Cl₁.₅ 28→**ClI₀.₅ 18 meV/atom**(I↓·Cl↑)·전극 호환 ΔE_D↓(LiI/I₂ 저형성E, S양극 최적)·**σ Cl–Br 동급**(등량). I/Cl=0.75:0.75서 **σ=23.5 mS/cm**(Li Voronoi 9.39 Å³·Ea **0.18**); I 과다(I₁.₅)서 5→4배위 회귀로 σ **4.3**. gap **Cl–I 2.32 > Cl–Br 2.19**(PBE). I⁻=가장 polarizable(Bader **Q_I −0.857 \|e\|**·전하밀도 최저)·**4a 강선호**(site ΔE **0.35** > Br 0.14 eV/atom). **🔑 산화 onset 미계산**(S-limited 예상, [Banik]과 정합) | ✅ `papers/rao2025_iodide_argyrodite.md` | DFT+AIMD(실험 0) |
| **[Rao11]** | Rao & Adams 2011 Phys. Status Solidi A (208, 1804–1807) — **"Studies of lithium argyrodite SE for ASSB"** *분야 origin 연구논문* (NUS Singapore, **외부**; ≠[Rao]=2025 iodide). Li₆PS₅X(**X=Cl,Br,I 전 할라이드**) **볼밀+550 °C/5 h 어닐**(Deiseroth 7일→25 h 단축) + **bond-valence(BVSE) 경험적 force-field**(DFT 아님). 결정질 σ **Cl 1.9/Br 6.8(10⁻³ 액체급)≫I 4.6×10⁻⁷**·임피던스 Ea Cl 0.38/Br 0.32/I 0.26·격자 a 9.85/9.98/10.14 Å. **BVSE 경로 위계**(Fig 2): intra-cage hexagon 0.15–0.18 → extended cage 0.22–0.25 → **inter-cage(dc 율속) 0.27–0.35 eV**. dc 장벽은 Cl/Br/I ~0.3 eV 비슷한데 σ는 I만 낮음=topology/connectivity 지배. **🔑 comp1(=Li₆PS₅Cl 동일조성) σ 외부 anchor(1.9 mS/cm)+우리 inter-cage 서사의 2011 1차 출처**. ⚠ BV=relaxation 무시(저자명시)·Ea 방법마다 갈림(NMR 0.04/임피던스 0.32/MD 0.30/BV 0.33) | ✅ `papers/rao2011_argyrodite_se_studies_bvse.md` | exp(합성/XRD/EIS)+BVSE force-field(외부) |
| **[Kraft]** ⭐ε∞/elastic 앵커 | Kraft/Culver/Calderon/Böcher/Krauskopf/Senyshyn/Dietrich/Zevalkink/Janek/**Wolfgang Zeier** 2017 JACS (139, 10909−10918, DOI 10.1021/jacs.7b06327, **not OA**) — **"Influence of Lattice Polarizability on the Ionic Conductivity in Li₆PS₅X (X=Cl,Br,I)"** *우리 조성 정확 동일*(comp1=Li₆PS₅Cl·**comp2=Li₆PS₅Cl₀.₅Br₀.₅**·comp5조성=Li₆PS₅I, F4̄3m 고용체 9종; JLU Giessen·FRM II·MSU, **외부**; **순수 실험, DFT 없음**). 중성자 Rietveld+synchrotron PDF+임피던스+**ultrasonic speed of sound(PE)+RUS 탄성텐서 C_ij**. **핵심 반전**: Cl→Br→I(더 분극성·큰 할라이드) 격자 무름(v_long 1480→1130 ms⁻¹ **−24 %**·Debye ν_D 2.45→1.90×10¹² Hz **−22 %**, Cl→Br₀.₅I₀.₅) → **E_A↓(0.46→0.30 eV)** *그런데* **prefactor σ₀도↓(2.7×10⁷→10³ KScm⁻¹, Meyer–Neldel 보상)** → 상쇄 → **σ 최적 = 중간강성 Cl₀.₅Br₀.₅(=comp2) ~2 mS/cm**(Cl 1.3e-3·**I ~1e-6** 3자릿수↓); 무질서 62→0 %(I⁻ 2.2 Å≫S²⁻ 1.84라 소멸)·a Vegard 9.86→10.14 Å·inter-cage 2.7→3.3 Å. **🔑🔑 우리 ε∞(전자분극성=Kraft *입력변수*)+elastic(기계무름=Kraft *측정대상*) 두 체인의 문헌 닻; prefactor 지배 = 우리 Nd σ-drop(D0 0.65×·Ea 불변) 앵커.** ⚠ 속도/Debye/E_A/σ/σ₀/점프거리=Fig figure-read(SI 표 없음)·**E_A=total(bulk+GB) 임피던스 0.46 ≫ 우리 bulk MD 0.253=방법차**·B/G 미보고(speed of sound/Debye/C_ij만=Torii n/a 상보) | ✅ `papers/kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md` | exp only(중성자/PDF/임피던스/PE·RUS, DFT 없음) |
| **[Klerk]** ⭐disorder-AIMD 원전 | **de Klerk**/Rosłoń/**Wagemaker** 2016 Chem. Mater. (28, 7955−7963, DOI 10.1021/acs.chemmater.6b03630) — **"Diffusion Mechanism of Li Argyrodite SEs … Halogen Disorder"** (TU Delft, **외부**; **순수 AIMD, 실험 0**; Kraft 2017보다 1년 앞). VASP/GGA-PBE/280 eV/**단위셀 52원자**/Γ-MD/100 ps/300·450·600 K; site-visit jump statistics(자리반경 0.9 Å)·σ_J(intercage rate·a=7.0 Å)+σ*(MSD)·f=D*/D_J<0.2. **점프 3종(doublet 1.9/intracage 2.25/intercage 가변) 중 intercage=율속**(rate ≤1/5·MD Ea 0.20–0.25 vs 단거리 0.10–0.14 eV). 🔑 **halogen 4a/4c(=4d) disorder = 거시 확산 필요조건**: all-4a(I형)=intercage 0(모든 T)·all-4c=doublet 붕괴; vacancy·halogen 가상조성(Li₆PS₆·Li₇PS₅Cl) 분리 → **둘 다 필요**; RDF **Cl 케이지 5 Li vs S 케이지 7 Li**(공공 응집→빈 doublet=intercage 착지점); **최적 Cl 분포 4a:4c=1:3(4c 75 %) — min-jump-rate 극대화: 450 K intercage 6.20 vs 3.12 ×10¹⁰ s⁻¹ = 1.99×(SI Table S2; σ_J 5.12/2.56=2.00×), σ_J 기준 300/600 K도 일관(1.79/1.59×)**; **Li₅PS₄X₂**(할로겐-rich) 600 K σ_J 5.91/4.47/3.76 ≈ Li₆PS₅Cl/Br 동급~상회(I₂ 포함)+공기/수분 안정 추정. ⚠ 75 %=Cl1.0·**분포당 단일 배열**·**σ_J(limiting-rate) 지표** 조건부(σ*_MSD는 600 K 0.91<1.01 **역전**=지표 의존; 2024 MTP-MLIP는 25 % 보고=방법 의존)·**SI 확보 2026-07-28(#32 Sup): Tables S1–S3 전문 digest §3b, 배열 좌표·Li 공공 규칙은 SI에도 없음 확정**·300 K 오차>값(Cl σ_J 0.89±1.29)·σ 절대값=bulk 상한(실측 대비 수 자릿수↑) | ✅ `papers/deklerk2016_diffusion_site_disorder_argyrodite.md` | DFT-AIMD(순수, 실험 0) |
| **[Adeli]** ⭐Cl-rich 실험 원전 | Adeli⁺/Bazak⁺(공동1)/K.H.Park/Kochetkov/Huq/**Goward**/**Linda F. Nazar** 2019 Angew (58, 8681–8686, DOI 10.1002/anie.201814222) — **"Boosting Solid-State Diffusivity and Conductivity … by Halide Substitution"** (Waterloo·McMaster·ORNL, **외부**; **자체 계산 0** — exp 중성자 TOF Rietveld+EIS+⁷Li PFG/MAS NMR 3축). **halogen-rich 고용체 Li₆₋ₓPS₅₋ₓCl₁₊ₓ(x≤0.5) 확립 원전 + Li₅.₅PS₄.₅Cl₁.₅ 중성자 점유율 원본**: a **9.8061(1) Å**·**4a-Cl 0.615(17)/4c-Cl 0.834(16)**(site disorder "S자리 Cl 점유" 61→**83 %**; ⚠ Adeli 4c=Kraft/우리 4d)·**Li 48h 0.456(16)**(=Li₅.₄₇ 공공 실측)·U_iso(Li) 0.075 Å²·LiCl 1.7 wt%. **σ(cold-press 2 t·In 블로킹·total·298 K)**: 2.5→4.2→5.6→**9.4±0.1 mS/cm**(~4×)·**소결 12.0±0.2**·σ_e 3×10⁻⁹(t≈1); **Ea EIS 0.34→0.29 ≡ PFG 0.35→0.29(1)**(이중 일치=GB 오염 반박); **PFG D*(300 K)=1.01×10⁻¹¹ m²/s**(LGPS PFG ~5배); **Haven ratio 0.3→0.23**(공공 매개 협동; c=4/cell 하한 규약). Vegard 수축 9.8598→9.8061 Å(=Li 공공). **고용한계 x=0.5 — x=0.6(=modelc 조성) LiCl 석출·σ 3.3**; Br-rich 불가(x=0.25 LiBr). 기작 3중 = 정전 약화(⁷Li "LiCl-like" 이동)+Li 공공+무질서; [Klerk] "할로겐 증량 σ 불변" MD 예측을 실험 4×로 반박·Li₅PS₄Cl₂ 대신 x=0.5 end member. ⚠ σ=total(195 K도 bulk/GB 미분리)·중성자 x=0.5뿐·평판 CV(Cl-rich 전류↓)는 [Zuo] 복합 CV(2×)와 정반대=방법 함정. **SI 실물 감사 2026-07-28**(inbox #33 Sup: Table S1–S3 전값 일치·D*/Ea 수치표 부재 확정, digest §3f) | ✅ `papers/adeli2019_halide_substitution_boosting_argyrodite.md` | exp(중성자 Rietveld+EIS+PFG/MAS NMR, 계산 0) |
| **[Luo22]** ⭐**T3 실험 앵커 원본** | **Shuting Luo**/…/**Lingyun Zhu\***/**Xing Zhang\*** 2022 *ACS Energy Lett.* **7**(9), 3064–3071 (칭화대 공정역학과 + 桂林电器科研 + 中科院 물리연, **외부**) — "**Nanostructure of the Interphase Layer between a Single Li Dendrite and Sulfide Electrolyte in ASSLBs**". **Li₆PS₅Cl(=comp1 조성) 안에서 자라 셀을 단락시킨 단일 Li 덴드라이트**를 뜯어내 **cryo-TEM(100 K)**: **25 °C 48 h = 단결정 Li₂S ~12 nm 균일** vs **60 °C = 다결정 Li₂S + 입계·전위 + ~3 nm 비정질** → R_SEI **4→13 Ω vs 2→204 Ω(100×)**. **⚠⚠ 이 논문의 모든 관측은 온도당 시야 1개·오차막대 0** (§11b) — **우리 계산값과 같은 칸에 넣지 않는다. 대조 기준 전용.** **60 °C 두께 숫자는 원논문에 없다.** `kim2026_…sei_reactive_md` 의 ref [49] = 이 논문 | ✅ `papers/luo2022_cryotem_li_dendrite_sulfide_interphase.md` | **exp 주(cryo-TEM/EIS/Raman) + AIMD 보조 — 실험 관측량. 수치는 대조 기준으로만** |
| [Semi] | "When Electrolytes Are Semiconductors" 2026 — HSE06 gap | ⬜ PDF | DFT |
| [Kaur] | Kaur elastic (JES 2022?, PDF#8 `ec2b0fc7` 미확인·미digest) — ⚠ 이 행에 있던 "2016 JES·SQS·E22.1/B28.7/G8.1"은 **Deng 2016 값의 오귀속**이었음(2026-07-28 원문 검증) → **[Deng16]으로 이관**. Kaur 실제 내용은 PDF 확인 후 재기입 | ⬜ PDF | DFT |
| **[Deng16]** ⭐SE 탄성 DFT 원전 | **Deng**/Z.Wang/Chu/Luo/**Shyue Ping Ong** 2016 JES (163(2), A67–A74, DOI 10.1149/2.0061602jes) — **"Elastic Properties of Alkali Superionic Conductor Electrolytes from First Principles Calculations"** (UCSD Ong 그룹, **외부**; **순수 DFT static elastic, 실험 0**). **23종 SICE full 탄성텐서 원전**: VASP/PAW/**PBEsol**(PBE·optB88-vdW 벤치 후 채택; **D3 없음**)/520 eV/k 1000·atom⁻¹/**strain-stress ±0.015 Å**(Le Page–Saxe, MP 교차검증; relaxed-ion 정황 판정 — 명시 없음)/VRH/Born/pymatgen. **Li₆PS₅Cl: C₁₁/C₁₂/C₄₄=39.9/23.1/7.8·B 28.7·G 8.1·E 22.1·ν 0.37·G/B 0.28(23종 중 최저=최연성)**; Li₆PS₅Br E 25.3·I 30.0. 물질군 순서 thiophosphate<antiperovskite<phosphate<NASICON<garnet<perovskite·황화물 E<50/B<40/G<20·Na<Li. **🔑🔑 "Deng=SQS" 귀속(torii digest·kb 개념문서·elastic.json) 원문 검증 결과 거짓 — SQS 단어 자체 없음, argyrodite는 "only the 24g sites are occupied" 완전 질서 모델(F4̄3m 유지=독립 Cᵢⱼ 3개), 전 조성 ordered/end-member 전략. Zener A도 미보고 — 인쇄 Cᵢⱼ 유도 시 0.93(0.92는 절사).** **🔑 E/G/C₄₄ ≈ 우리 relaxed-ion comp1(22.06/8.13/7.98)과 0.2–2 % 일치** = D3 없는 GGA+ordered+relaxed-ion의 최근접 외부 앵커. ⚠ **halide 경향(Cl→I E +36 % 경화)은 [Kraft]·[Kim2025]·우리 comp2(−9 %)와 정반대 = 경향 인용 금지**(단일 조성 절대값만); c-Na₃PS₄ C₄₄=δ0.05 % 특수 처리; PBE/optB88 전체값 SI(미보유 n/a) | ✅ `papers/deng2016_elastic_superionic_electrolytes_dft.md` | DFT(static elastic 23종, 실험 0) |
| **[Torii]** | Torii/Okita/Motohashi/**Sakuda**/**Hayashi** 2025 J. Phys. Chem. C (129, 17882) — **LPSCl(=comp1) full-DFT 기계물성·이방성** (Osaka Metropolitan Univ., **외부**). VASP/**PBE-D3**/**relaxed-ion**/stress-strain Cij/3×3×3 k. **E=27.4·B=34.7·G=10.0·ν=0.37·B/G=3.46(연성)·Zener A=1.09(등방)**; C₁₁/C₁₂/C₄₄=47.4/28.4/10.4. 인장 durable(ε~0.2 선형)·{100}>{111}>{110} strength; **전단 취성 ε=0.7 %**(Cl→Li→Li₄Cl→layered gap). Bader: P 최대변동(+1.32). **🔑🔑 우리 vacancy paradox의 *외부 full-DFT 판정*: Torii relaxed-ion이 우리 relaxed-ion(22.06/8.13) 영역, clamped(52.31/20.12) 아님** | ✅ `papers/torii2025_lpscl_mechanical_anisotropy_dft.md` | DFT(elastic+stress-strain+Bader) |
| **[Rupp]** | Kim/Balaish/Rupp 2021 AEM — oxide vs sulfide SE + 계면 landscape 리뷰 (63 pp) | ✅ `papers/kim2021_review_oxide_sulfide_se_interfaces.md` | review |
| **[Bai]** | Bai/Duan/Zhuang/Yang/Wang 2020 JMCA (8, 25663–25686) — **argyrodite *전용* field-map 리뷰**(China Automotive Battery Research Inst.·Beijing, **외부**; ≠[Rupp]=oxide/sulfide 광역). **6토픽**: 결정구조(3종 점프·**anion disorder 4a/4d→inter-cage 율속 장벽↓→superionic**·σ Br≈Cl≫I)·구조튜닝(**Cl/S↑→σ 10 mS/cm**·Si/Ge·Sb concerted·**단일=한측면/다중codoping=종합개선**)·합성(고상 vs 용액·UMA+RTA)·계면(음극 환원 ~1.7 V·양극 산화 CV>2.2 V/이론 S/S²⁻ **2.24 V**·분해 **Li₃PS₄+S+LiCl**·passivation ESW 확장)·대기안정(**HSAB Sn/Sb·O codoping**·"metal+O cooperate")·셀통합(failure mechanism·operando 필요). **🔑 우리 프로그램이 §구조·§구조튜닝(Cl-rich/cascade)·§대기 codoping(O/Nd)·§계면(grand-pot ESW) 네 칸에 *동시* 닻; outlook "multiple codoping=종합개선"이 우리 cascade의 *계산적 응답*.** ⚠ 2020=Cl-rich 4축·grand-pot 절차·MLIP·vacancy paradox 미존재(우리 너머) | ✅ `papers/bai2020_argyrodite_review_progress.md` | review |
| **[KimICCF]** ⭐우리그룹 | Kim/Cho/Y.M.Lee 2026 CEJ — ICCF(IL cavity filler) → σ 회복 155 % + 음극 in-situ LiF-rich SEI (한양대 Cho + Yonsei Lee) | ✅ `papers/kim2026_iccf_molten_salt_sei_lpscl_sheet.md` | exp(+분자 HOMO/LUMO·GeoDict) |
| **[KimCA]** ⭐우리그룹 | Kim/Y.M.Lee 2025 Battery Energy — SE 코팅 중 도전재(CA) 차원 효과: 0D Super P(나쁨) vs 1D VGCF(좋음, ≈CA無 dense). 양극복합체 σ_e·활성표면적·형상 (Yonsei Lee + DGIST) | ✅ `papers/kim2025_conductive_agent_se_coating_cathode.md` | exp(계산無) |
| **[Kang]** ⭐우리그룹 | Kang/Shin/Y.Lee/**Jong-Won Lee** 2026 ChemComm *Feature Article* — *Intertwined* electrochemo-mechanical degradation 리뷰 (한양대 우리 연구실 자체 리뷰, 18 pp). thesis = 전기화학 분해 ↔ 기계 불안정의 **양방향 되먹임 고리**; 진짜 적 = *heterogeneity*; 3대 완화 = SE도핑/CAM코팅/음극공학 | ✅ `papers/kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review.md` | review(우리그룹·자체데이터無) |
| **[Kang25]** ⭐우리그룹 | Kang/Y.Lee/Bae/**Jong-Won Lee** 2025 ChemComm (61, 16850) — NCM811에 **LPSCl(=comp1) conformal dry-coating** → 고전압 **기생반응을 *균일*화**(식1 `2Li₆PS₅Cl→P₂S₅+5S+2LiCl+10e⁻+10Li⁺`) → NCM 균질 chemical lithiation(SOC↓) → layered→rock-salt 억제 → R_int 4.3 Ω cm²·200cyc 유지율 **+15.0 %**. **이로움 = SOC-강하(코팅), passivation 아님** | ✅ `papers/kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb.md` | exp(계산無) |
| **[Whitten]** 📐methods | Whitten 2023 Appl. Surf. Sci. Adv. (13, 100384) — **UPS 실전·best-practice 튜토리얼**(외부, 단독저자, *재료결과無·계산無*). **물성축 비교대상 아님 — methods 레퍼런스**: UPS = 우리 DFT VBM/Φ/IE를 *측정하는 기법* + 산화안정성 valence-side 관측량 | ✅ `papers/whitten2023_ups_practical_best_practices.md` | methods(외부) |
| **[Hikima]** | Hikima/Shimizu/Kiuchi/Hinuma/Suzuki/Hirayama/Matsubara/**Ryoji Kanno** 2022 Commun. Chem. (5:52, DOI 10.1038/s42004-022-00664-w) — **박막 ASSB(Al\|Li₂MnO₃\|LASGTP\|Li₃PO₄\|Li)를 *반도체 소자*로 보고 *전체 밴드구조*(진공준위 절대 VBM/CBM/E_F/Φ)를 operando HAXPES+UPS+LEIPS로 작동 중 실측** (Tokyo Tech 칸노 그룹, **외부**). 충전 시 **Li₂₋ₓMnO₃ E_F ~1.1 eV drop→n→p 전이→Al계면 Schottky/inversion→고전압 충전차단**; 4단계(stage3=oxygen redox plateau); 과전압·LASGTP 전위창 확인. Eg Li₂MnO₃ 2.83/LASGTP 4.09/**Li₃PO₄ 5.77**. **🔑 우리 oxidation 보고서 §6(밴드엣지=band alignment 관측량)·[Whitten](기법)·[Banik](정적 HAXPES VBM)의 *operando 확장*** — "밴드엣지는 band-alignment/전위창용이고 *작동 중 움직인다*". 유일 *수치* 앵커 **Li₃PO₄ Eg 5.77≈우리 5.73**. ⚠⚠ **oxide(Li₂MnO₃/LASGTP)라 argyrodite VBM/Eg/산화 onset과 *수치* 등치 금지·DFT 직접계산 없음·밴드엣지≠분해 onset** | ✅ `papers/hikima2022_operando_band_structure_assb.md` | exp operando(DFT 직접계산無) |
| **[He19]** 📐methods | He/Yu/Li/**Yan Zhao** 2019 EEM (2, 264–279) — **"Density Functional Theory for Battery Materials"** DFT 방법론 백본 리뷰(외부, Wuhan; *argyrodite 아님·재료수치無·물성축 비교대상 아님*). **우리 정적 DFT 백본 *전부*의 표준 provenance**: PBE 주류·**PBE gap ~1 eV 과소→HSE 보정(Fig 8)**·Nernst V=−Δ_rG/nF + convex-hull(Ceder 평균전압)·**AIMD-MSD→D·σ**·NEB·CDD/DOS/PDOS/Bader·EOS·phonon·**§7 functional 벤치(SCAN 추천/HSE06=+U급/U는 TM-d/f localized 전용)**. **🔑 SE ESW=Goodenough HOMO/LUMO band-edge(Fig 7)만 — grand-potential(Mo2012)은 리뷰에 *없음* → 우리가 더 엄밀** | ✅ `papers/he2019_dft_for_battery_materials_review.md` | review(methods) |
| **[Sundar]** 🧪screening | Sundar/T.Kim/Lagunas/Mane/**Zapol**/**Connell** 2025 Adv. Sci. (12, e13191) — **LPSCl(=comp1) 입자에 바이너리 산화물 ALD 코팅** DFT 고처리량 스크린(외부, Argonne·UChicago; *코팅≠격자도핑*). 2-단계: ① 계면 분해 ΔE(**pymatgen InterfaceReactions = 우리 interface_reactivity와 동일**, 전해질·Li·양극 3계면) + HSE06 gap → ② 분해산물 Li-CI-NEB barrier + gap. **design rule = 예측력 있는 지표는 코팅 자체 안정성이 아니라 *계면 분해산물의 σ_ion/σ_e*** (우리 sei_products/Nd-cascade 철학과 동일 결). MgO=champion(σ_ion+25%·σ_e÷9·Li안정·CCD≤0.9 mA/cm²)·Al₂O₃ 재확인·ZrO₂ 실패(Zr₃O 1.4 eV·σ_e×2)·ZnO 역설(slab gap 0.4 eV·ZnS→σ_e↓0.17). LPSCl HSE06 gap **3.92 eV**(mix 0.32). **❗우리 47-dopant cascade ranking/descriptor와는 비교 금지(도핑 아님)** — 연결=방법론 거울 + 분해산물-전도도 철학 + sei_products gap 재확인 | ✅ `papers/sundar2025_oxide_coating_screening_lpscl.md` | DFT-screen+exp(외부) |
| **[Son]** | Son/Park/…/**D-H.Seo**(KAIST)/**K-W.Nam**(Dongguk)/**Yoon Seok Jung**(Yonsei) 2025 Nat. Energy (10, 1334–1346, DOI 10.1038/s41560-025-01865-y) — **"Five-volt-class high-capacity ASSB"** (외부; Yonsei 정윤석 ≠ 우리그룹 이용민). **5 V급 스피넬(LNMO 4.7 V·LCMO 5.3 V)을 ASSB에서 쓰려면 산화안정 차폐층 필요** — 황화물 **LPSCl "<2.5 V"**(본문 명시)·할라이드 **LYC 3.7 V·Zr-OCl 4.1 V**·**LiNbO₃ 3.86 V**(고전압 산소방출→**Mn₃O₄** 절연상) 전부 부족 → **새 불소계 SE LiCl–4Li₂TiF₆**(σ 1.7e-5 S/cm·산화안정 **>6.7 V**; Cl 치환·Li↑가 Li 채널 *확장*) 차폐. dry-coating LNMO 130 mAh/g·**2C 500cyc 75.2 %**·R_int 0.1 kΩ·cm²·**35.3 mAh/cm²(1.8 mm)**·LCMO 5.3 V·저전압확장 258 mAh/g. **🔑 우리 산화 서사의 *외부 실험 캡스톤***: LPSCl <2.5 V = 우리 grand-potential **2.256 V 정량 일치**·[Banik] S-pin "치환으론 못 늘림→타 물질군 필요"의 *실현*(불소계 5 V)·[Cha] 할라이드코팅 *전압천장(~4 V NCM급)* 명시. ⚠ Ti/F·Y/Zr = **우리 6원소 hull 밖**(grand-potential·AIMD·enumerate *방법*만 동일); modelc(Cl1.6)≠Son LPSCl(Cl1.5) | ✅ `papers/son2025_fivevolt_assb.md` | exp+DFT보조(grand-potential·AIMD·enumerate) |
| **[Cha]** ⭐우리그룹 | Cha/Yun/Kim/**Kang**/Cho/**Jong-Won Lee** 2024 J.Power Sources (617, 235157) — high-Ni NCM에 **할라이드 SE(LIC=Li₃InCl₆/LYC=Li₃YCl₆/LZC=Li₂ZrCl₆) 8–10 nm 코팅**으로 NCM-LPSCl(=comp1) 계면 부반응 억제. **핵심 = *dual compatibility*(NCM·LPSCl *양쪽* 호환)가 결정, σ 아님**: LIC(In) 양쪽 분해(In₂S₃)·LYC(Y) LPSCl과 분해(Y₂S₃)·**LZC(Zr⁴⁺) 양쪽 무분해=최고**. 계면저항 bare 74.4→LZC **20.1 Ω·cm²**·100cyc LZC **91.2 %**(LIC 80.8 < bare 83.1 < LYC 87.3). **우리 그룹 cathode-interface 3부작 *기원(2024)*** (→Kang25→Kang) | ✅ `papers/cha2024_dualcompatible_halide_ncm_lpscl_interface.md` | exp(계산無) |
| **[Perc]** 🧭theory | Ishikawa/Takae/Kurita 2025 (arXiv:2505.00362v2, APS) — **"Cooperative Ion Conduction Enabled by Site Percolation in Random Substitutional Crystals"**(외부·theory; LiₓPb₁₋₂ₓBiₓTe rock-salt 자체 MD, *argyrodite 아님·환원단위·물성축 수치비교 대상 아님*). **σ급등 문턱 = FCC site-perc pc≈0.2; 침투클러스터 이온만 mobile; cooperative knock-on(σ≫σ_NE)**. **우리 cascade의 *이론 백본*** — `dopant_blocking_fraction`=망 site-dilution / `migration_volume_fraction`=침투 저장벽 부피 / Nd-drop 0.52×=connectivity-blocking(Ea 불변) / dual-x=pc 위 유지 vs 밀기. [Dyre]의 percolation-*수송* 짝 = 이것의 percolation-*망* 짝 | ✅ `papers/ishikawa2025_site_percolation_cooperative_ion_conduction.md` | theory(외부, framework only) |
| **[Yang25]** | Yang/Y.Wang/Jiang/…/**Chuang Yu** 2025 Electrochim. Acta (535, 146619, DOI 10.1016/j.electacta.2025.146619) — **La₂O₃ 이원(La+O) 도핑 Cl-rich argyrodite** (HUST Wuhan·Guilin·Xidian, **외부**; 순수 exp, **계산 0**): **LPSC=Li₅.₅PS₄.₅Cl₁.₅ → Li₅.₅₈P₀.₉₆La₀.₀₄S₄.₄₄O₀.₀₆Cl₁.₅**(x=0.04 최적; La→4b(P자리)=LaS₄·O→PS₄=PS₃O·a 9.793→9.823 Å·x≥0.05 용해한계). **σ 희생** 9.58→**6.23 mS/cm**(0.65×)·Ea 0.238→0.254·σ_e **8.5×↑**(2.59e-9→2.2e-8); **[대기]** P–O 결합→H₂S 3.2→2.3 cm³/g·노출후 σ 39×·**500 °C 어닐 회복 43.5% vs 11.9%**; **[음극]** **CCD 0.9→3.1 mA/cm²(σ와 무상관 명시)**·대칭셀 25→**200 h**·SEI=**La⁰+LiCl**(결론 원문 "formation of La and LiCl") **+ 주장 "by-product LaCl₃ [LaCl₉] 1D 채널" = 가설(SI 12pp 정독 확정: 음극 XPS·La 3d·Cl 2p·반응식 전무; 유일 실측 La 계면종=양극 "LaSₓ" S15b)**; full 1C 500cyc **83.6%**(⚠ Li-In; 진짜 Li-금속 셀은 NCM712 100cyc 69.8%뿐)·CV 창 불변(Li/SE/SS planar 0–5 V 곡선겹침; 무계산 band-edge 단언)·Table S1 Rietveld=명목-고정 템플릿(La=P1 좌표·U_iso 동일→La@4b·PS₃O "가정"). **🔑🔑 우리 Nd₂O₃-modelc의 최근접 실험 자매(RE³⁺+O·Cl-rich·σ↔interphase trade)** | ✅ `papers/yang2025_lao_dualdoping_argyrodite_lacl3.md` | exp (계산 0) |
| **[Xu26NdO]** 🔴우선경쟁 | Chang Xu/Lei Zhu/…/Dengxu Wu/…/Hong Li/Liquan Chen/**Fan Wu** 2026 Nano Energy (157, 112246, DOI 10.1016/j.nanoen.2026.112246; **온라인 2026-07-27**, 본문 12 pp+SI 5 pp; inbox #57) — **Nd–O 공도핑 Cl-rich argyrodite = 우리 Nd₂O₃-modelc와 도펀트까지 같은 최초의 외부 실험** (IOP CAS·CASOL·China FAW·Li Auto, **외부**; 순수 exp, **계산 0** — [Yang25] La-O·[WangYO] Y-O에 이은 RE/M³⁺-O 3번째이자 "최근접 자매" 타이틀 승계): LPSC=Li₅.₃PS₄.₃Cl₁.₇ → **Li₅.₃₊₂ₓP₁₋ₓNdₓS₄.₃₋₁.₅ₓO₁.₅ₓCl₁.₇, x=0.025 최적**. σ 6.99→**8.75 mS/cm**(1.25×; x=0.1은 4.27=**0.61×**)·Ea 0.292→0.278·σ_e 4.2e-9→**9e-10**(4.7×↓, ⚠x=0/0.025 2조성만 측정인데 5조성 CCD와 "상관" 주장)·CCD 2.29→**6.62 mA/cm²**(계열 최고, Table S1)·대칭셀 **2000 h**(15→20 mV; LPSC ~178 h 단락)·H₂S 1.55→**0.67 cm³/g**(30 %RH·60 min·단일런)·드라이룸 12 h 51.6→69.5 %·LCO 1C 1000cyc **"95.4 %"**(figure-read: 분모=130th 피크 122.8, 초기 대비 ~100 %)·Ni90 1000cyc 84.9 %. **구조 주장 = Nd³⁺→P⁵⁺(4b)+O²⁻→S²⁻+2Li/Nd = 우리 Track2(컨트롤) 화학식** — 그러나 **Rietveld·격자상수·NMR·EXAFS 전무**(본문 "is inferred" 자인; XPS Nd 3d는 0.2 at% S/N 한계로 잔류 Nd₂O₃와 구분 불가·EDS 산점 도트); XRD 줌 figure-read **x=0→0.025 +0.3° 이동(≈1 % 수축, 내부표준 없음·과대 의심)** + §2.1 "lattice expansion"↔§2.2 "mild contraction" 자기모순. SEI "**Li–Nd alloy**"는 사이클 후 XPS 995 eV 소피크 1개+"plausible" 자인 — **Li–Nd 이원계 금속간화합물 미보고(비혼화) → 우리 hull 검증 표적(P2)**; "합금 함유 계면=전자절연" 주장은 내적 긴장. 그림-본문 불일치 3건: **Fig 2a x=0.025에 LiCl ♦**(본문 "x≥0.05")·**Raman 세기 "체계적 감소"**(그림에선 x=0이 최약, 무정규화)·**DRT D4는 NdO ~20 Ω > LPSC ~5 Ω**(본문은 LPSC 증가만 강조). **통계 0**: 오차막대·셀 반복수·EIS 등가회로·펠릿밀도 전부 미보고(그들 수치로 우리 유도 ~82 %TD); 노출 후 σ는 **재분쇄+재압축** 프로토콜(관대). **우리 유도 σ₀ 분해: σ비 1.252 = exp(0.014/kT) 1.73 × σ₀ 0.73 → prefactor 27 %↓ = "carrier 증가·채널 확장" 서사 자기모순**([WangYO]③ 패턴·우리 UMA D0 0.65×와 방향 일치); **고x 감쇠 0.61×@x=0.1 ↔ 우리 UMA 0.52×@x=0.2 수렴**([Yang25] 0.65×에 이은 2번째 실험 앵커); **σ_e 감소 = PI 실험(DC 분극)의 독립 재현** — 우리 "벌크 gap은 오히려 1.632로 축소, 감소는 O-유래 wide-gap interphase percolation" 해석(electronic.json)이 채울 공백(그들 무설명). 관찰 SEI Li₂O(528.5)·LiCl·Li₂S/Li₃P 억제 = 우리 sei_products.json 서사의 실험판. **⚠⚠ Paper#2 신규성 경보(2026-07-27 온라인): 인용 필수 + 차별화 = 자리판정 ΔE(Track1 vs Track2, P1)·gap 1.632/4f-무접촉·SEI hull(P2)·희석 MD(P4)** | ✅ `papers/xu2026_ndo_codoping_argyrodite.md` (§11 헛점·§13 계산제안) | exp (계산 0) |
| **[Jun26]** 🔌binder | Jun/Jeong(공동1저)/…/**Jeonghun Kim**/**Yoon Seok Jung** 2026 Nat. Commun. (17:156, DOI 10.1038/s41467-025-66851-0) — **"Electron-conductive binder for Si negative electrode enabling low-pressure ASSB"** (Yonsei 정윤석 그룹+**SK On**, **외부**; *argyrodite 물성 논문 아님 — ASSB Si 음극 폴리머 바인더, 물성 4축 수치비교 대상 아님, 계산 0*). **PPMA = PEDOT:P(SSₓ-co-MA_y)**(⚠ PMMA 아님) = PEDOT:PSS 폴리음이온에 maleic acid 공중합 → **"PEDOT:PSS 전도 기전 유지(GIWAXS π-π·Raman benzoid·S 2p 불변) + -COOH 접착 추가(peel <0.1→2.2 N/cm)"**. 기전 = 저압(5 MPa) 탈리튬화 시 **e⁻ 망 붕괴**(ex situ 3전극: PVDF 2.0e-3→4.3e-5 S/cm)를 전도성 바인더가 유지; 전극 σ_e 36,000×(5.5e-9→2.0e-4). 반쪽셀 80 vs 45%@50cyc·풀셀 5 MPa 0.5C 105 vs 76(⚠ 70 MPa 역전 131 vs 142)·**233 mAh 파우치 226 Wh/kg**. **🔑 우리 SDCP(자가도핑 PEDOT-계 바인더) 프로그램의 문헌 좌표** — 아래 🔌 note 참조 | ✅ `papers/jun2026_ppma_econductive_binder_si_lowpressure_assb.md` | exp(계산 0) |
| **[Han25]** 🔌binder·🧲estimand | Dong-Yeob **Han**/Masud/Yeongseok Kim(공동1저 3인)/…/**Youn Soo Kim\***/**Soojin Park\*** 2025 *Adv. Mater.* (**37, 2506266**, DOI 10.1002/adma.202506266, OA CC BY-NC; POSTECH 화학·신소재 + 동국대 + 경상국립대) — "**Ionically Conductive Elastic Polymer Binder for Ultrahigh Loading Electrode**": **NCM811 / 액체 카보네이트 / Li 금속** 계의 다기능 바인더 **ICEP = [P(AN-co-AMPS)]₂-b-PEO₄₆** (RAFT, x/y=[AN]/[AMPS] → ICEP-5/8/19). ⚠ **황화물 ASSB 아님 — 물성 4축(A–D) 수치비교 대상 아님**([Jun26]와 같은 취급). 실험 헤드라인: 신율 **283 %** vs PVDF 31.8 · SAICAS 응집/접착 **0.29/0.27 vs 0.07/0.04 N** · 피복 **≈7 nm** · 암염층 **3.1 vs 11.3 nm** · CEI 내층 **108 vs 283 s** · **62.4 mg cm⁻² / 12.5 mAh cm⁻²**, 94.6 %@60 cyc · 파우치 **377.6 Wh kg_cell⁻¹ / 1016.8 Wh L_cell⁻¹**(N/P 1.57, E/C 2.5 g Ah⁻¹). **🔑 우리 관심은 `Fig. 2g` 의 DFT 결합에너지 4점**: **CASTEP · PBE · spin-polarized · ultrasoft PP · TS-vdW · U(Ni 6.0/Co 3.4/Mn 3.9) · 300 eV · 표면 최적화 Γ-only · NCM811 (001) 8층 5×4(32Ni/4Co/4Mn, TM 2겹) · 하단 2층 고정 · 진공 >15 Å** — **전부 SI 에만 있고 본문엔 코드 이름조차 없다.** `E_bind = E_total − (E_molecule + E_slab)` (SI 식 5). 값(**전부 figure-read**) AN −0.162 / AMPS −1.819 / **AMPS(−H) −2.243** / PVDF −0.703 eV. **⭐ `(−H)` = 탈양성자 음이온이 아니라 H 가 슬랩으로 옮겨간 상태**(SI `Figure S13` 캡션 *"hydrogen transfer from ICEP_AMPS to the NCM811 (001) surface"*) ⇒ 조성 보존·총전하 0 ⇒ jellium/NELECT/짝이온이 **필요 없다**. **남는 하자는 전하가 아니라 스핀** — spin-pol+U 를 쓰면서 자기배열·환원 TM 상태 선택 규칙 0. **우리 산술 비판**: ICEP-8 은 AN:AMPS≈8:1 인데 **AN(−0.162)이 PVDF(−0.703)보다 약하다** → 단위당 가중 −0.347 < −0.703 ⇒ **"ICEP 가 PVDF 보다 강하게 붙는다"를 `Fig. 2g` 로 인용 금지**(인용 가능 한계 = "AMPS 단위 > PVDF 단위"). ⛔ 결합에너지 절대값·σ 절대값(전해질 함침막 값)·인성/필름 E 인용 금지 | ✅ `papers/han2025_icep_binder_ultrahigh_loading_ncm811.md` | exp + DFT 4점 (CASTEP) |
| **[Jeong25]** 🔌binder·🔴estimand-반면교사 | Yeong Hun **Jeong**/G. Won/S. Kim/M. S. Jo/S. Seo/D. Jeong(UMN)/**Jimin Shim\*** 2025 *Adv. Energy Mater.* (**15, e02765**, DOI 10.1002/aenm.202502765, OA CC BY-NC-ND; **서울대 화학교육과** + Univ. of Minnesota) — "**A Tough, Adhesive, and Protective Binder Shield for Stabilizing High-Nickel Cathodes in Lithium-Ion Batteries**": PVDF 를 **버리지 않고** ATRP 로 PAA 그래프팅(**20 mol%**, PVDFA 245 kDa) → 분지형 **PEI 로 전극 건조 중 in situ 가교**(PVDFA-N#, # = 아민 mol%/VDF). ⚠⚠ **NCM811 / 1.2 M LiPF₆ EC:EMC 3:7 +VC2+FEC10 / 2032 코인 / Li 금속·흑연 — 황화물 ASSB 아님, 물성 4축(A–D) 수치비교 대상 아님**([Han25]·[Jun26] 와 동일 취급). 실험 헤드라인(`figure-read` 다수): 필름 신율 **7.8→26.7 %** · UTS **18.5→42.5 MPa** · 인성 **1.1→9.0**(⚠ 축 **GJ m⁻³ 1000배 오류**) · 180° peel **41→182 gf mm⁻¹** · SAICAS(10 µm) **4.1→10.4** · 수명 **318→658 cyc**(300 cyc **80 %**) · **27–28 mg cm⁻²** PVDF 50 cyc 실패↔N5 >140 · **저바인더 2 wt%** PVDF 펀칭 박리 · 55 °C · 300 cyc 후 **내부 마이크로크랙 소멸** · Li 위 **Ni 5.4→3.0 ppb** · **CF_x:LiF 1:6.7→1:0.27** · TOF-SIMS **CEI 절반**. **🔑 우리 관심 = `Fig. 4f`·`Fig. S14` 의 DFT 9점**: **Gaussian 16 분자계산**(B3LYP/6-311++G(d,p)+D3(zero) → B3LYP/def2-TZVP 단일점, **CPCM ε=30.28**, `E_b=E_total−(E_A+E_B)`). **슬랩 0 · NCM 표면 0 · 스핀 다중도 0줄 · 전하상태 0줄 · BSSE 0 · 자세탐색 0 · 조각크기 미보정.** 값 Ni²⁺ −0.5/−3.6/−6.5 · Mn²⁺ −1.5/−4.5/−7.3 · Co²⁺ −1.5/−5.0/−9.5 eV. **⛔ 절대값·이온 간 순위 인용 금지** — **Irving–Williams 역전** + **PVDF 기준이 이온마다 3배 차이** ⇒ 같은 스핀/배위 branch 가 아니다. **🔁 중복**: PVDF→다기능 바인더·나노막 피복·TM 킬레이션·rock-salt 억제·CEI 박막화는 **[Han25] 선행·더 정량적**, graft+crosslink 이중개질은 **[Park26]**(ASSB) 선행 | ✅ `papers/jeong2025_tough_adhesive_binder_shield_ncm811.md` (2026-09-22, 크로핑 19장 중 **8장 실독**) | exp 주도 + 분자 DFT 9점 (Gaussian 16) |
| **[Shi17]** 🔋신규프로젝트 | Le Shi/Ao Xu/**Tianshou Zhao** (HKUST) 2017 ACS AMI (9, 1987) — **2D h-BN 계면층 / Li 금속 음극** dendrite 억제 기전 순수 DFT(**QE/PBE-D2/PAW** = 우리 h-BN@VGCF QE-periodic 툴체인 동일). 전자차단(2층 터널 **1.33/1.65 eV**)+under-cover 흡착(계면 **−2.3 eV**, **eq5=맨Li+맨hBN 흡착 합**)+균일확산(0.10~0.21 eV)×강성. 흡착E 기준=고립 Li 원자. **결함 면투과 미계산·비-argyrodite·신규프로젝트 방법(흡착 eq2·NEB) 레퍼런스** | ✅ `papers/shi2017_hbn_interfacial_layer_li_anode.md` | 순수 DFT(QE) |
| **[Liang]** | Liang/Sun/Yu/Wu/Xing/Kou/**Bolong Huang** 2025 Small (21, 2502078, DOI 10.1002/smll.202502078) — **"Unraveling Li-ion migration in *quasi-layered* argyrodite SE"** *순수 이론*(CityU HK / CAS Beijing, **외부**). **50% 4a/4c anion disorder → 준층상 "P2mm"**(abstract P2₁2₁2₁; ⚠표기불일치) 음이온 골격(S층/halide-cage/halide층/S-cage). **4c-halide 약결합(Cl–Li Mayer bond order ≤0.5×S–Li)+4a-S 고활성** → **inter-layer 비등방 전도**(σ_up halide층 > σ_down S층, **최대 2.07** @SnS₄·I). **inter-cage(=층간) jump = 거시 σ 율속**(NEB Ea **0.12** ≈ AIMD Arrhenius **0.088 eV**, Li₆PS₅Cl). σ Cl>Br>I(300K 0.245/0.175/0.147)·**PSe₄ 최고(1.18 S/cm)·GeS₄ 최저**(강결합). 2축(halide×cage-cation) 치환을 **Mayer bond order *균일성*** 과 상관. DOS disorder↑→저E이동(안정화)·**ELF 저영역=Li 궤적**·IRI 분산상호작용. **방법 제안: NEB(평균 퍼텐셜=implicit-solvent 유추)로 SSE Ea 직접계산**. GTH-PBE-q3(CP2K 시사); k/ecut/supercell/AIMD시간 **미공개**. ⚠ **준층상(4a/4c) ≠ 우리 cubic F-43m(4a/4d)** — **inter-layer≠inter-cage·σ_up/σ_down 비등방≠우리 등방**; σ=AIMD 외삽 절대값(과대 가능). **원리(anion-site 기전·connectivity 율속)만 공유, 수치/구조 직접등치 금지** | ✅ `papers/liang2025_quasilayered_argyrodite_li_migration.md` | DFT+AIMD+NEB+Mayer/ELF/IRI(외부, 실험0) |
| **[BZOx]** | **Choi**(Sookmyung)/**Chang**(Chung-Ang, 공동1)/…/**J.Kim**/**J.Moon**/**W-H.Ryu**(Yonsei) 2026 Small (0:e73805, DOI 10.1002/smll.73805) — **산소결핍 black ZrO₂₋ₓ(BZOx)를 dry mechanofusion으로 단결정 NMC811 입자에 ~8 nm conformal shell 코팅**(vs 화학양론 white ZrO₂=WZO 9.7 nm), LPSCl·3.0–4.3 V. headline: 첫 사이클 비가역 67.45→**45.84 mAh/g**·ΔV 0.3→**0.18 V**(WZO 0.73)·CE **77.5 %**·100cyc **126.69 mAh/g·80.4 %**·R_CA-SE 44.5/**192.9**/**55.2 Ω**·σ_e(DC 분극, 양극 펠릿) pristine **1.49e-4** → WZO **5.85e-6(÷25.5)** / BZOx **3.88e-5 S/cm(÷3.8)** = "charge-conductive"의 정량. **DFT(VASP·PBE+U Ni 6.2/Zr 5·520 eV·LiNiO₂(104)\|LPSCl(100) 슬랩)**: 계면-S pDOS LNO=E_F 직하 → Zr-산화물 접촉 시 **−1..−2 eV 하강(안정화)**; S–O 1.97→1.65 Å(SO₂ 시사) vs BZOx=Zr–S(SO₂ 억제). ⚠ rate 본문 vs SI 그래프 불일치(pristine 최고 가능)·BZOx\|LPSCl 분해 열역학 미계산·**DFT 모델 ZrO₁.₃₃ vs 실험 ZrO₁.₈**(3배 공공) | ✅ `papers/choi2026_bzox_dry_zro2x_nmc_shell_coating.md` | exp+DFT보조(계면 pDOS·결합길이, VASP PBE+U) |
| **[Wang22]** 🔥thermal | Shuo Wang/Yujing Wu/**Hong Li**/**Liquan Chen**/**Fan Wu** 2022 InfoMat (4(8), e12316, DOI 10.1002/inf2.12316, OA) — **"Improving thermal stability of sulfide SEs: An intrinsic theoretical paradigm"** (**IOP CAS 물리**, **외부**; ⚠ 교신 Fan Wu ≠ [Fan26]의 Li-Zhen Fan — 단 **[Fan26] ref 109 ★★★ = 이 논문**). **밀봉 석영관 황 석출 관찰**(새 측정법) + **결합에너지 서술자 Th′**={[Li]%×312.5+[P]%×346}×4+E_doped+k. 서열 **Li₂P₂S₆<Li₇P₃S₁₁(~300 °C)<Li₃PS₄(~400 °C)<Li₂PS₃<Li₆PS₅Cl(=comp1, 800 °C XRD 무변화·DSC 무피크·황석출 0)**; P₂S₃(P/S↑)로 Li₇P₃S₁₁ onset 334→384 °C; 도핑(Cu/Si/Sn/O) Li₃PS₄ 400→500 °C·**O 5 % σ 10×↓(0.077 mS/cm)**; 주기율표 Th′ 지도(최적 Zr·Mn·Fe·Cu·Si·Ni·Sn)+Li/P/S 삼원상도. **⚠ 자체 DFT 0**(Handbook 2원자 BDE+조성 산수+MP ΔH 소환)·Eq 5에 Li–Cl 항 부재(Cl=희석재 취급)·Cl-rich(1.5/1.6) 미측정 | ✅ `papers/wang2022_sulfide_thermal_stability_th_descriptor.md` | exp(황석출·XRD·DSC·Raman·EIS)+경험적 서술자(DFT 0) |
| **[Zhu20]** 💧moisture·📐method-계보 | **Yizhou Zhu**/**Yifei Mo** 2020 Angew (59, 17472–17476, DOI 10.1002/anie.202007621) — **"Materials Design Principles for Air-Stable Li/Na Solid Electrolytes"** (UMD, **외부**; **🔑 우리 grand-potential ESW 방법 원저자 그룹** — ref [2]=Zhu/He/Mo 2015·2016=우리 방법 원전, Mo=[Banik] 공저자). **가수분해(H₂S/HCl) 열역학 전수 지도**(MP hull+50 meV+NIST-JANAF 기체/OH; 자체 DFT는 4종 보조 — VASP PBE 520 eV): 46 M–S+52 Li–M–S+65 Na–M–S+14 Li–M–Cl(+M–Cl·Na–M–Cl Fig S1), **0.1 % H₂O(=RH ~3 %)·1 ppm H₂S/HCl** 조건. **Li₂S +0.225(조건부 안정)·Li₃PS₄→¼Li₃PO₄+H₂S −0.608 eV/H₂O(thiophosphate 과민성=인산염 구동력)**; 서열 Zn/Cd/Cu/Ag 최고≫Ga/Ge/Sn/Sb/Pb/Bi≫P⁵⁺·**B³⁺ 최악급**; Li함량↑⇒Li₂S 수렴; **염화물=수분안정(예외 P·B)·병목은 환원**; Fig 3 2축(가수분해×0 V 환원) 가이드차트 — **Li황화물 중 수분+환원 동시 만족 없음·RE(Nd 포함)=환원안정 최우수 doping 후보 명시·In³⁺ 수분 최고**. **3차 검증(본문 재투입 #54, 2026-08-06, digest §14): 중복·신규 0건**이나 그림 픽셀 검산으로 ① `Fig. 3` 색인 누락 복구 ② "`Fig 2` x축 = binary 값 오름차순" 서술 정정(실제는 논문 공유 고정 양이온 축, 단조 아님 — **우리 cascade 그림 캡션에 "값 순 정렬"이라 쓰면 같은 흠 복제**) ③ `Cr⁶⁺` = 데이터 없는 유령 라벨 확정. 온전한 회색 ○ 26개가 xlsx 전사값과 **≤0.002 eV 일치** → `db/properties/zhu2020_si_*.csv` 신뢰도 상향. **4차 검증(SI 재투입 `54. Sup)`, 2026-08-06, digest §15): 텍스트 신규 0건**(SI 반응 6종·세팅·수산화물 19종·Step 1–4 전수 재확인, 크롭 bbox 픽셀 재현)이나 ① **마지막 미판독 `Fig S2` 해소 → 이 논문 안 본 그림 0장**. Fig S2 = **Fig 2 의 겹침 없는 판**(화합물 1개=막대 1개; Li–M–S 52 화합물이 35 칸에 포개짐, Sb³⁺ 칸 0.25 eV 스프레드) — 막대 카운트 46/52/14 일치 + Na–M–S 는 **`NaScS₂ = +0.000` 이 높이 0 이라 64개만 보인다**(전사본 269행 4번째 교차검증) ② 🔴 **SI pseudopotential 목록이 자체 DFT 4종과 불일치**(`Li_sv,Na_pv,P,S` ↔ 필요 Li·Na·**As**·S·**Y**·**Cl**·**Zr**; k-mesh 도 없음) ⇒ **Li₃YCl₆ 0.886·Li₂ZrCl₆ 0.632 는 "저자 자체 계산 + 세팅 불완전 기재" 를 병기해 인용** — 하필 §3b.2 염화물 오프셋 판정의 그 둘이다(나머지 265종은 MP 소환이라 무관) ③ 🔴 `--clean` 가드 방향 반전(이제 inbox 엔 SI 만 → fig_1·2·**수동 bbox fig_3** 이 위험), `pdf_map.tsv` 갱신. ⚠ 열역학 only(kinetics 0)·**SI PDF + SI xlsx 전부 확보(대표반응 알고리즘 명세·LiCl +0.977/NaCl +1.532 · 269 화합물 전표 → `db/properties/zhu2020_si_hydrolysis_energies.csv` 99행 + `zhu2020_si_redox_reactions.csv` 170행; ⚠ 2026-08-05 이전 판의 "xlsx 미보유" 표기는 낡은 것)**·argyrodite 직접 계산 아님·본문 "electrochemical stability"=환원 전용(4.5 V 산화 전표는 SI xlsx에만) | ✅ `papers/zhu2020_air_stable_se_design_principles.md` | DFT-DB thermodynamics(실험 0, VASP 4종 보조) |
| **[Fan26]** 🗺️review·⚠미출판 | Yang Li/…/**Hong Liu**/**Ce-Wen Nan**/**Li-Zhen Fan** (USTB·Zhengzhou·Tsinghua; **[Li25]와 같은 그룹**), "**Stability Issues in Sulfide-Based ASSBs: From Material Properties to Electrode Interfaces**" — **황화물 ASSB 안정성 전축(全軸) 리뷰**(ECER-D-26-00097, Electrochem. Energy Rev. **투고 draft·DOI 없음**; 56 pp·refs 239·Fig 26; **자체 계산/실험 0**). 고유 5축(공기 HSAB·용매 donor-number·열 400–500 °C/계면 200–300 °C·전기화학 **LGPS 1.71–2.14 V**/산화 ~2 V S²⁻-우선/계면 3유형·기계 E 10–30 GPa/K_IC 0.2–0.4) + 양극(MCI·O-방출·화학-기계; 코팅·신규 CAM) + 음극(wedge-opening 덴드라이트·SEI 내 dead-Li·σ_e 내부석출·압력창; SE개질→in-situ 절연 SEI·인공 SEI·LiF/gradient). **Fig 24a/b = 우리 [Liu23]/[Li25] digest 그림** → 우리 계보가 리뷰 §5.2.2 정중앙. 미래 4방향(passive→**intrinsic stability**·동적 계면·저압·표준화). ⚠ 정성 리뷰(유지율 %·CCD 본문 부재)·draft 오타(σ 단위/refs 38=193 중복)·수치 이식 금지(전부 원전 소환) — 아래 🗺️ Landscape note [Fan26] 참조. 🔁 **[분류: Revision] 재정독 2026-08-06** — 판본은 초판과 동일(지문 5개 일치), 신규 소득은 그림 26/26 크로핑 + draft 결함 3건 + ⭐**Fig 6c 판독 LPSCl 안정 상단 `figure-read ≈2.3–2.4 V`(=우리 onset 2.256 V 와 정합)** | ✅ `papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md` | review(외부·미출판 draft) |
| **[Lee26]** 🤖ML·LMB(액체) | Doo Bong Lee/Jinwoo Park(공동1)/E.Kim/**Woong Kim** 2026 ESM (86, 104972, DOI 10.1016/j.ensm.2026.104972) — "**Interpretable enhanced-ECFP-guided deep learning for rational electrolyte design & CE prediction in LMB**" (고려대·가천대, **외부**; **⚠ 액체 전해질 리튬금속전지 — argyrodite/SE 아님·자체 DFT/MD 0·물성 4축 수치비교 대상 아님**). 문헌 **168개 Li–Cu 반쪽셀 CE** + **e-ECFP**(ECFP r=2 + salt/solvent 구분·substructure 빈도·**농도 가중**; 2×1025차원; 타깃 **LCE=−log₁₀(1−CE)**) + DNN(**test RMSE 0.16·R² 0.86**; Linear test 3.05 붕괴·RF/XGB 0.21–0.22) + **SHAP** → 설계규칙 "**용매 F-rich·고리형 에터=CE↑ / 카보네이트=↓ / 염은 저불소화 LiFSI**" → **1 M LiFSI/MeTHF:TTE(1:3)**: 예측 99.63 vs **실측 CE 99.72 %**(Aurbach)·σ 0.816 mS/cm·free FSI⁻ 0(CIP/AGG=LHCE형)·**LiF+Li₂O-rich 무기 SEI**(XPS)·최치밀 Li(SEM)·LFP 1C **500cyc 97 %**·평균 CE **99.97 %**. ⚠ CE=문헌 수집 라벨(프로토콜 정규화 불명)·규칙=기지 지식 재발견·저로딩/Li 대과잉·**DBE:Tol CE 99.88인데 유지율 꼴찌(σ 0.029)=CE 단일축 한계 자체 실증** — 아래 🤖 note 참조 | ✅ `papers/lee2026_eecfp_dnn_electrolyte_ce_lmb.md` | exp+ML(e-ECFP/DNN/SHAP, DFT 0) |
| **[Liu-hBN]** 🔋새프로젝트시드·Li-metal-anode | Xiaoyu Liu/…/**Yuejiao Chen**/**Libao Chen** 2022 Adv. Mater. Interfaces (9, 2200011, DOI 10.1002/admi.202200011) — "**Uniform Lithium Deposition Induced by Double Lithiophobic Sandwich Structure**" (Central South Univ., **외부**; **⚠ 황화물 SE 아님 · Li 금속 음극/Cu 집전체 위 lithiophobic h-BN 코팅 · 물성 4축 수치비교 대상 아님**). Cu에 **h-BN 분말(300 nm, 15 µm) 코팅** → DFT(**VASP/PBE/500 eV/Γ 2π·0.04/MP**) 흡착E 서열 **Li–h-BN −0.33**(약함=lithiophobicity) < **Li–Cu(111) −2.50** < **h-BN–Li–Cu(111) −3.16 eV**(샌드위치 최강, N→Li 전하이동 CDD) → Li가 h-BN·Cu *사이*로 파고들어 **"h-BN–Li–Cu" 평평 증착**. **기계강도 아님**(코팅 E 1.655 GPa ≪ Li 4.9). 대칭셀 **>500 h**(Cu 250 h 단락)·CE **>95 %/240cyc**·LFP full 1C 300cyc **73.3 vs 33.3 %**. **🔋 우리 새 ORCA 프로젝트(VGCF+h-BN 샌드위치, Li 흡착·확산)의 *방법 원형*** — 아래 🔋 project-seed note 참조. ⚠ 흡착E 정의식·Li 기준상태·vdW 미공개·**확산장벽 미계산**(abstract "barrier"=실험 overpotential)·nucleation overpotential 효과 미묘/혼재 | ✅ `papers/liu2022_hbn_lithiophobic_sandwich_li_anode.md` | exp + DFT(VASP 흡착E 3-모델+CDD, 외부) |
| **[Schlem20]** ⚠할라이드·귀속감사 | Schlem/Muy/Prinz/Banik/**Shao-Horn**/Zobel/**Wolfgang G. Zeier** 2020 AEM (10, 1903719, DOI 10.1002/aenm.201903719, OA; inbox #36 본문+SI 전독) — "**Mechanochemical Synthesis: A Tool to Tune Cation Site Disorder and Ionic Transport Properties of Li₃MCl₆ (M = Y, Er)**" (JLU Giessen·MIT·Bayreuth, **외부**; **⚠ 비-argyrodite — 삼방 P3̄m1 할라이드 SE**). 합성경로(볼밀 500 rpm·297cyc → 550 °C 어닐 1 min/1 h → 앰풀 1주)로 **M2–M3 양이온 자리무질서 2.5→88 %** 연속 조절(XRD Rietveld+PDF 이중정량, 점유율 전표 digest §3b·3c) → **σ 1.7×10⁻⁵→3.1×10⁻⁴ S/cm(18×)·Ea 0.49→0.41 eV**(EIS **total**·bulk/GB 분리불가 명시; Li₃YCl₆ 0.45–0.49 비단조). VASP-PBE 정적 defect-model(Ewald 사전선별→10개): 질서/반전/교대 **등에너지 ~1–2 meV/atom**·face-sharing만 +26 meV/atom = **무질서는 바닥상태 아닌 공정 몫**; 병목 삼각면적(5.88→6.18 Å²)↔Ea 상관(Fig S13); Er-on-Li antisite 배제. **[SI 실물 감사 2026-08-03]** 전값 일치 + ⚠ **Fig S13은 앰풀·1 h Ea가 본문 Fig 6d/Table S4와 뒤바뀐 채 인쇄**되고 저무질서 3점이 0.03 Å²에 밀집 → 병목–Ea 상관은 **BM 1점이 끄는 2-클러스터, 정량 인용 금지**(정의만 차용); Table S3의 **occ(M3)≡1−occ(M2) 구속**으로 M-site 비화학량론은 검정 불가. **[강화] Y 계열도 무질서 축에선 σ·Ea 4점 단조**(9.8/16.1/17.3/100 % ↔ σ 3.4/4.7/5.5/9.5×10⁻⁵ ↔ Ea 0.4925/0.4785/0.4465/0.4455) — 비단조는 '어닐 시간→무질서' 쪽. **🔑 '무질서=공정변수' 외부 실증 + [Cha] LYC(Li₃YCl₆) 배경물성. ⚠⚠ 이 DOI에 LPSCl 데이터·Ea 0.25/0.22 없음 → repo(li_transport.json·세미나 ref[3]·open_items #5) "Schlem 0.25/0.22 EXACT" 귀속 오류 확정 — digest §11b** | ✅ `papers/schlem2020_li3mcl6_cation_site_disorder.md` | exp(XRD/PDF/EIS) + DFT보조(정적 defect-model만, 수송계산 0) |
| **[Jun22]** ⭐랩 AIMD 원전·기술자 계보 출발점 | **Byeongsun Jun**/**Sang Uck Lee** 2022 JMCA (10, 7888–7895, DOI 10.1039/d1ta10964b) — "**Designing a descriptor for the computational screening of argyrodite-based SSE: uniformity of ion-cage size**" (**한양대 ERICA**; Jun은 이후 **현대차**, Lee는 이후 SKKU; **외부**; 순수 DFT+AIMD·실험 0; 본문 8 pp+ESI 20 pp 전독; KISTI KSC-2021-CRE-0017). **① AIMD 파라미터 원전** — [KimCSP] §주의9가 "cell size/spin/time step/temperature 는 ref 47 참조"로 넘긴 그 **ref 47**: VASP 5.4.1/PAW/**PBE(vdW 無·U 無)**/500 eV/완화 3×3×3·힘<0.02 eV/Å; **MD Γ-only·NVT Nosé–Hoover·dt 2 fs·600–1200 K 5~6점·단위셀 ~52원자(24 Li 전부 24g 완전점유)·배열×온도당 ≥3 시드 평균·자동종료 RSD(σ)<0.25 & 유효hop>250(He/Mo 2018)·무질서 ~100 ps vs 질서 ≥500 ps @800 K·pymatgen-diffusion** (⚠ **스핀만 원전에도 부재**). **② 기술자 = STD of Li-cage size** — free anion(4a/4c=우리 4d)→주변 Li 평균거리=케이지 반지름, 그 산포. **우리가 Table 1 18행 역공학 → "자리종류별 평균반경 집합의 다중도-비가중 모집단 SD(÷N)"로 ±0.0035 재현**(Table S3는 저대칭이라 개별케이지 SD, +0.013 계통 — 두 표 STD가 같은 양이 아닌데 Fig 5는 한 축에 혼재). 물리 = **"케이지는 큰 게 아니라 서로 비슷해야 좋다"**. enumlib 6배열(0/25/50×2/75/100 % X@4c)×3할로겐 + 할로겐 과잉 27배열 = **45배열 전수 AIMD**. ordered Ea 452/339 vs disordered 151–193 meV(Cl)·σ 3–7자릿수 갭; **Cl>Br>I 6배열 전부**; 최안정 **Cl 50 %/Br 25 %/I 0 %**(=I 4a 강선호, [Rao25]·[Klerk]과 3중 정합); Cl x 0→0.75 STD **0.1193→0.0615(−48 %)**. Table S4: **Li₆PS₅Cl 에서 HT 입방상 우위가 겨우 +2.99 meV/atom**. ⚠⚠ **σ_bulk 가중식 Eq(6–8)+χc^7.14 = [KimMTP] Eq S8–S11 의 원출처**이며 **Eq(7)은 차원 무의미**(단위 바꾸면 4.7×, 혼합규칙 선택이 3자릿수)·**σ 절대값 인용 금지**(PBE-AIMD; I σ 0.84 는 실험 대비 200–400× 과대)·**x=0.75(σ 29.04)는 실험 대조 0**·케이지 반지름의 **계산온도·Li 컷오프 미명시=엄밀 재현 불가**·Fig 5 **R²·오차막대 없음·σ 선형축**(우리 계산 ρ=−0.78·R²=0.44)·**같은 점유율 다른 배열 쌍에서 부호 3/3 오답**·Li 공공 배열은 최저E 1개만·인쇄 불일치 9건(온도 500 vs 600 K·I 50 % Ea "ᵇ27"→**227**). ⚠⚠ **본문(8 pp) 실물 독립 검증 2026-08-04 §20 (교정 3·신규 7; `tools/litdb/jun2022_fig_extract.py`)**: **★★Fig 5 의 모집단이 자기 Table 1 과 다르다** — 마커 픽셀 복원 결과 18배열 중 **16개만**, 빠진 둘이 **σ 최대 배열(Cl 50 % P2mm, 37.1 mS/cm — y축 상한 34.97 초과로 잘림)** 과 **Cl 100 %(STD 0.1336 인데 σ 0.12, 축 안인데 미작도)** = **기술자에 가장 불리한 두 좌표** → 제거 시 **Cl ρ −0.829 → −1.000·R² 0.394 → 0.769**(전체 R² 0.426 → 0.648) → ⛔ **Fig 5 인용 금지, Table 1/S3 원수치만** · **★★Fig 3 은 5배열**(범례 5줄, 50 % 중 P2₁22 만) → **σ 최대 배열은 본문 어느 그림에도 없다** · **★Fig 3a 축 검산이 §6·§8.3 을 교차검증**(Ea 449 vs 인쇄 452 meV; σ(χc=1) 1.71e−2 vs 1.62e−2 → **χc 0.8·지수 7.14·52원자 셀 동시 확인**) · **새 불일치 D10** §3.1 *"AIMD simulations **at 300 K**"* (§2 500–1200·Fig 3 600–1200 과 3중 어긋남) · **★"원전" 프레임 후퇴** — §2 가 셀·**스핀**·dt·온도·앙상블을 **refs 41–44 (Mo/Ong)** 로 위임 = `[KimCSP]` 와 같은 정형구 → **"수치의 원전은 여기, 근거의 원전은 Mo/Ong"**, **Q1(스핀) 다음 행선지 = Deng 2016 CM·Zhu 2018 ch.7** · **Fig 4(c) distinct-part 는 σ 10⁴ 배 차이를 구별 못 함 → T12 판정축은 self-part 한정**(`[Lee24MO]`·`[KimCSP]` 에 이어 3건 연속) · **D6 강화**(Fig 4a 패널 라벨이 문자 그대로 "4a-cage" → 그림이 본문 산문을 부인) · **D4 는 본문 *내부* 모순**(Table 2 PS₅.₇₅ ↔ 같은 본문 p.7 PS₄.₇₅). ✅ Table 1 18행×9열·Table 2·설정·ref 동정·**STD 역공학식 독립 재계산**·**ρ 3/3 재현** 전부 확인. ⚠⚠⚠ **ESI(20 pp) 실물 독립 검증 2026-08-04 §21 (교정 2·신규 12; `tools/litdb/jun2022_esi_verify.py`·`jun2022_esi_figS3_extract.py`)**: **★★Fig S6 의 x=0 패널도 범례 5줄** → **σ 최대 배열은 본문+ESI 어느 그림에도 없다**(Table 1 한 줄이 유일) · **★★할로겐 과잉에서 기술자가 시드 밴드 밖에서 틀린다** — 9조성군 중 4군 오답, 2군은 밴드 분리(**I x=0.25: STD 2.1배 작은 배열이 σ 3.0배 느림**), n=4 인 3군은 3/3 오답; **Table S3 만 보면 ρ −0.698·log R² 0.435(I 0.291)** → **§11-3 의 “못 매긴다”→“틀린다” 격상**. 기구 = **4c 를 X 로 100 % 채워 S²⁻ 케이지가 사라진 행**을 기술자가 “균일해졌다”로 오독 · **★★Table S3 σ 열을 Eq(6–8)에 액면대로 넣으면 최대 +64 % 틀린다** — **χc 보정을 되돌린 원값에 혼합 → 그 다음 ×χc^7.14** 라야 9/9 재현 → **“σ 에 상수 하나 곱하면 결론이 64 % 움직인다” = Eq(6–8) 이식 금지 근거가 가설에서 실증으로** · **✅χc^7.14 비판 교정** — ~~앵커가 지수를 결정~~ 철회. 앵커 잔차는 어떤 지수에서도 0 이고, **지수 7.14 는 실측 8점 선형피팅 7.19 로 재현되는 정직한 값**. 앵커가 하는 일은 **R² 0.616→0.971**(논문 R² 미보고). 같은 χc 에서 σ_exp/σ_calc 가 **8.8배** 갈림 · **Table 2 “STD −48 %” 크기 인용 금지** — 인구조사 효과 포함(자리종류 4개 배열이 x=0 4개 → x=0.75 **0개**). ⚖ **통제비교(4a=100 % X 가족)에서는 세 할로겐 모두 단조 감소 −24/−33/−16 % → 방향은 참**, 이 수치로 대체 · **Fig S6 Br·I 범례 오식 다발**(4c→4a·점유율·**요오드 패널에 Br**) → 규율 2단 확장 **표>그림>산문, 그림 안에서도 데이터>범례** · **최안정 4a 거동이 할로겐마다 다름** — Cl 은 항상 4a 의 1/4 을 S 에 내주고 **I 는 한 번도 안 내준다**(=[Rao25]·[Klerk] 3중 정합), Br 은 0.5–0.9 meV/atom 축퇴 · **D1 발생 기구 규명**(ESI 일반론 “500–2000 K” + 실제 “600–1200 K” 의 혼합) · **Fig S1 자동연장 = 궤적 연속, 시드 축은 별개** · **ESI 번호계≠본문 번호계** · **⚠D11(후보) Table 2 Br x=0 STD 만 안 닫힘**(계산 0.1668 vs 인쇄 0.1688, 11/12 는 ≤0.0001) → Q7. ✅ Table S1/S2/S3(27×11)/S4 전량 일치, **D7·D8·D9·D1 실물 확정**, Eq(7) 차원문제 ESI 원문 축자 확정, **kT 역산 → T=300 K 확정** | ✅ `papers/jun2022_argyrodite_ion_cage_size_descriptor.md` | DFT+AIMD(순수, 실험 0) |
| **[KimMTP]** | Ji Hoon Kim(SKKU)/Byeongsun Jun·현대차 5인/**Byung-Hyun Kim(한양대 ERICA ⚠우리그룹 아님)**/**Sang Uck Lee** 2024 Nano Energy (124, 109436, DOI 10.1016/j.nanoen.2024.109436) — "**Highly reliable and large-scale simulations of promising argyrodite SEs using a machine-learned moment tensor potential**" (**외부**; 순수 계산·실험 0; **inbox #35, 사용자 분류 `DFT`** — 본문+SI 정독, 본문+SI 실물 감사 완료 2026-07-28 전값 일치; SI 실물 = inbox #35 Sup 28 pp). Li₆PS₅X(Cl/Br/I) **6배열 4a/4c(=문헌 4a/4d) 무질서 전수 MTP-MLIP MD**(훈련 7200 스냅샷=6배열×±5% strain×AIMD 300–1200 K; R_cut 5 Å/lev_max 8; 3×3×3=1404원자·NPT 10 ns·350–500 K×2회): **functional 3종 학습 비교 → optB88-vdw만 site-disorder 재현**(σ80%bulk **4.19/0.55/2.46** PBE/PBE-D3/optB88 vs exp 2.3–2.5; PBE·D3는 100%-ordered를 3.7 mS/cm로 오판) · **ordered(0/100%) Ea 339–529 meV·σRT ≤0.12 vs disordered(25–75%) 151–256 meV·13–42 mS/cm**(MSD caged vs free) · 27셀 Boltzmann random supercell σ100% 11.5→**χc^7.14 보정 σ80% 2.3** · **PS₄ 회전 고정 시 D600K −50%(disordered)/−18%(ordered)** · **Σ5[100](021) tilt GB**(γ≈1.35 J/m²·active-learning MTP·**>13,860원자**): **D_GB 0.3× bulk·영향권 10–20 Å·Li 정전기 축적**(PS₄³⁻+S²⁻ 인접 음전하)·처방=고산화수 도핑(S 전하↓ inductive effect). ⚠ P_i(σ)∝exp(−Δσ/kT) heuristic·χ^7.14 경험 회귀·힘 MAE 표기 불일치(본문 0.02 vs Fig S3 0.066–0.075 eV/Å)·Table S1 I조성 Ea 복제 의심 | ✅ `papers/kim2024_mtp_argyrodite_disorder_gb.md` | MLIP(MTP)-MD+DFT+AIMD(실험 0) |
| **[KimSEI]** ⛔프리프린트 | Ji Seon Kim/Ji Hoon Kim(SKKU)/Byeongsun Jun·Yong Jun Jang(**현대차**)/**Sang Uck Lee** — "**Deciphering Li₂S-like SEI Formation Mechanism at Li/Argyrodite Anodic Interfaces via Large-Scale Machine-Learned Reactive Dynamics**" (**SSRN 6020397, peer-review 미통과** — 저널명 본문에 없음; **외부**; 순수 계산·실험 0; 본문 26 pp 정독, **SI 미확보**〔프리프린트 자체의 SI 링크가 공란〕; **본문 실물 독립 검증 2026-08-04** — inbox #3·폴더 `이상욱`, 교정 6·신규 14, **수치 변경 0**, digest §21). **[KimMTP]의 직계 계면판**(ref [35]로 인용) — ⚠ **단 상속 범위 정정**: [KimMTP]에서 온 것은 **optB88-vdW 선택 근거 + R_cut 6 Å/lev_max 16 뿐**이고, **passive+active 2단계 학습 전략 자체는 ref [26] = Holekevi Chandrappa/Ong, JACS 144 (2022) 18009** 인용이다. ⚠ **초록이 본문을 부인한다** — 초록 "sulfur coating is **demonstrated as a practical approach**" vs 본문·결론 "volatility·high reactivity 때문에 **not easily feasible**" (초록만 인용 금지). ⚠ **서론이 인용한 ref[16] He/Mo 2018 = "AIMD 확산 물성은 통계 분산이 커서 독립 시행 다회 필요"** 인데 정작 자기 D는 단일 시드 = **우리 3-시드 규율의 문헌 방패**. optB88-vdW 라벨 MTP(**R_cut 6 Å/lev_max 16**·훈련 5,400 스냅샷·**2000 K·±10 % 부피 strain 포함**·MAE <10 meV/atom·~0.1 eV/Å) + **active learning γ_select=2 / γ_break 10→5→2**(KimMTP 5/20 대비 최대 10배 엄격) → **Li(100)‖LPSC(100)** ~7,000원자·**NVT 350 K·20 ns**: 즉시 PS₄ 분해 → S-rich 비정질 ~6 nm → **~11 ns Li₂S-유사 결정 핵생성 → ~5 nm 성장**·**잔존 PS₄ 20→6층 plateau**; 상 동정 RDF 첫피크 ~2.5 Å(⚠이중 y축=위치만); **Li₃P·LiCl은 결정화 안 됨**(고립/미소 클러스터). 2단계 기구 = **①S가 먼저 골격(7 ns) → ②Li 침투가 결정화(11 ns)**; P는 Li 금속 내부(z>125 Å)까지 침투. **영역분해 D(350 K)**: 결정영역 **0.4e-7** / 잔여벌크 **1.1e-7** / pristine **1.6e-7**(=[KimMTP] Table S3 GB셀 벌크영역 값) → **비 0.36**. 대형(16 nm Li‖20 nm LPSC·50 ns): 개시 **~30 ns**·**~11 nm interphase** vs cryo-TEM ~12 nm(Luo 2022 ACS EL 7, 3064). **S 중간층 3 nm 처방**: SEI 11→6 nm·PS₄ 잔존 18→34층. ⚠ **시드 1·오차막대 0**·개회로/무전류·**영역분해 D 창 미명시**(역산: 벌크 전구간 vs 결정영역 11–20 ns만)·소형모델 저장고 고갈 가능·본문 내부 모순(11 nm=하한)·Δt/thermostat/프로덕션 무질서배열 미명시·2단계 기구는 Ren 2024 EES·Chaney 2024 ACS AMI 선행 有. **⛔ D 절대값 인용 금지**(비율 0.36·자릿수·구조 관측량만) | ✅ `papers/kim2026_li_argyrodite_sei_reactive_md.md` | MLIP(MTP) reactive MD + 훈련용 DFT/AIMD (실험 0, **프리프린트**) |
| **[Zhu15]** ⭐grand-potential ESW 원전 | **Yizhou Zhu**/Xingfeng He/**Yifei Mo** 2015 ACS AMI (7, 23685–23693, DOI 10.1021/acsami.5b07517 — ⚠구메모 5b01004는 오기; inbox #38 본문+SI) — "**Origin of Outstanding Stability in the Li Solid Electrolyte Materials**" (UMD, **외부**; **우리 grand-potential ESW 방법의 원전** — [Zhu20] ref[2]·[Kang] Fig1a ref49·[Banik]·[GG]·Schwietert 계보의 시조, Mo=[Banik] 공저자). VASP-PBE/MP-일관 파라미터/MP-2015 보정/**pymatgen grand-potential PD**: μ_Li(φ)=μ⁰_Li−eφ·E_D(φ)=E(equil)−E(SE)−Δn_Li·μ_Li·**red=최고 lithiation plateau/ox=최저 delithiation plateau**·0 K(PV/엔트로피 무시)·metastable SE는 **E_hull→0 규약**(LPSCl 83 meV/atom ordered config·무질서 50–60배열 최저). 14 SE+7 Li-binary+5 코팅 전수: **황화물 intrinsic 창 ~1.6–2.3 V**(LGPS 1.71–2.14·**Li₆PS₅Cl 1.71–2.01**·Li₃PS₄ 1.71–2.31·Li₇P₃S₁₁ 2.28–2.31=최협 0.03 V)·산화물 넓음(LLZO 0.05–2.91·LATP 2.17–4.21·LAGP 2.70–4.27); 0 V 환원 E_D **LPSCl −0.96 → Li₃P+Li₂S+LiCl**(황화물 −0.9~−1.7·LAGP −1.99·**LLZO −0.021=DFT 정확도 이하 자인**)·5 V 산화 LPSCl −1.33 → P₂S₅+S+**PCl₃**(LATP/LAGP ~−0.06 eV/atom). **"넓은 CV 창 = ① kinetic 과전압(절연 산물·non-Li 확산·O₂/N₂ 핵생성; metal-air 유추 >1 V) + ② 전자절연 분해산물 interphase passivation(μ_Li=μ̃_Li⁺+μ̃_e⁻, 절연층서 μ̃_e⁻ 급락→창 안; Li-binary=SEI) — 전도성 산물(Li–Ge 합금·Ti³⁺)=MCI→연속 분해" 서사의 원형** + coating=인공 SEI(황화물 anodic 2–2.3→~4 V; LiCoO₂ 3.9 V 라인) + 설계원리 "Ge/Ti 회피(Si/Sn/Al/Zn 유사 우려)·anion 무해·**Li-halide 도핑=σ+Li안정 동시**". **본문 9 pp + SI 10 pp 전문 실물 대조 완료(2026-08-03, digest §17·§18 — 불일치 0)**: SI Table S1 E_hull 전량(**Li₃PS₄·Li₄GeS₄·Li₂PO₂N만 0, 나머지 SE는 전부 E_hull→0 규약**·LPSCl 83 = Deiseroth 구조 ordered 자체 DFT, MP-id 없음)·**γ-Li₃PS₄ Pmn2₁을 최저다형으로 Li–P–S 상도에 추가**·S2 계단표 13종/S3 코팅 5종 전값·**Li₇P₂S₈I I 이탈 2.47 V vs LPSCl Cl 이탈 2.88 V(계 내부 Cl>I 0.41 V)**·**Li-binary 단독 anodic limit LiF 6.38>LiCl 4.21>Li₂O 2.90>LiI 2.46>Li₂S 2.00>Li₃P 0.85>Li₃N 0.45**(Fig 2a 픽셀 ±0.02 V, SI·−ΔH_f/F 양쪽 교차검증)·**Li₃PO₄만 환원 1계단(Li₃P+Li₂O)=양방향 passivating 코팅**(LiNbO₃→Nb·LiTaO₃→Ta·Li₂SiO₃→Li–Si는 양극 전용)·원문 내부 불일치 SI 판정(LiPON 환원 **0.68**·LAGP 산화 **4.27**·LiPON 5 V 산물 **PON**) | ✅ `papers/zhu2015_esw_grand_potential_origin.md` | DFT(MP-hull thermodynamics, 실험 0) |
| **[Rich16]** ⭐pseudo-binary 계면 원전 | **W.D. Richards**/Lincoln Miara/Yan Wang/Jae Chul Kim/**Gerbrand Ceder** 2016 Chem. Mater. (28, 266−273, DOI 10.1021/acs.chemmater.5b04082) — "**Interface Stability in Solid-State Batteries**" (MIT·Samsung SAIT·UCB·LBNL, **외부**; 순수 DFT+실험열화학 hull, 실험 0; **[Zhu15]와 두 달 간격 상보 쌍** — Zhu=SE 단독 창, Richards=전극과의 혼합). **전극\|전해질 pseudo-binary 형식화 원전**: 닫힌 `ΔE=min_{x∈[0,1]}{E_pd[xcₐ+(1−x)c_b]−xE[cₐ]−(1−x)E[c_b]}`(eq 2)·Li-개방 `ΔΦ`(eq 4, μ_Li=양극 평균전압)·`ΔΦ_no-mixing`(eq 5, 전위 몫 분리, \|ΔΦ\|≥\|ΔΦ_no-mix\|) = **우리 interface_reactivity의 원전**. 전해질 ~30종×양극 7종 산물 전표(SI S1–S9): thiophosphate\|산화물 양극 최대(~−0.5~−1.1 eV/atom figure-read; PO₄+TM황화물), **Li₆PS₅Cl** anodic `→S+Li₃PS₄+LiCl`(우리 2.256 V 반응 동일)·cathodic `→Li₄P₂S₆+Li₂S+LiCl`(P–P 중간체)·vs LiCoO₂ mixing `CoSCl+S+CoP₄O₁₁+CoS₂`·vs LiVS₂/Li₂S none; **"anodic 한계=Li₂S(S²⁻) 지배" 명문 = axis① 원조**; Li₃PS₄/Li₃PO₄/LiPON=**Li₂S/Li₂O+Li₃P 자가-passivation**(Li₃P=이온전도체); **"@V none이어도 mixing 반응" 클래스**(Li₂MgCl₄·LiAlCl₄ 전 양극 등)=전압창 단독 스크리닝 불충분·코팅 논리 근거; **Li₃PO₄·LiF만 전 조합 불활성**; 신규 셀 제안(Li₃PS₄\|LiVS₂·LiBH₄\|LiTiS₂)+이중 전해질(Li₃PS₄+Li₂MgCl₄, ⚠ eq 2 상호검증 미수행). **🆕 본문 실물 독립 재검증 2026-08-03(inbox #39, 폴더 `DFT`, digest §18) — 불일치 0 + 교정 1건**: 구 figure-read "황화물 창 1.7–2.1 V·[Zhu15] 1.71–2.01과 정합"은 **오독 → 철회**. 실측 **Li₆PS₅Cl 2.06–2.32·Li₃PS₄ 2.06–2.58·LGPS 2.06–2.41·Li₄SnS₄ 1.92–2.35 V**(본문 서술 "2–2.5 V"와 일치) ⇒ **Richards 2.32 ≳ 우리 2.256 > Zhu 2.01**. **신규 정량 전표**: Fig 2 전해질 **37종 창**(±0.03 V)·Fig 1c **binary 9종**(신규 Li₃P 0.92·LiI 2.80·LiBr 3.64·LiH 0.93)·Fig 4 **ΔΦ_no-mix/ΔΦ 84쌍**(±0.01 eV/atom; 84쌍 전부 \|ΔΦ\|≥\|ΔΦ_no-mix\| 성립 = 판독 무결성 + **SI 유래 §8 주장 다수를 본문 그림만으로 독립 확증**). 🔑 **Li₆PS₅Cl anodic 2.32 = Li₂S anodic 2.32(동일 픽셀) = S²⁻ 완전 pin**·**Li₂MnBr₄만 −0.23 V 창 축소**·**폴리음이온 +1.1~1.65 V**·**Li₄SnS₄\|LiCoO₂ −1.10/−1.10(mixing 이득 0) vs Li₃PS₄ −0.69/−0.97·LGPS −0.81/−1.02(mixing이 −0.2~−0.3 추가)** = 본문 "2-경로 열화"의 경로별 몫 분리·**LiNbO₃ 최대 반응은 LiTiS₂(−0.16)**(황화물 양극과 가장 반응적). **본문 신규**: **In 금속 음극이 명시 처방**·표준코팅 4종에 **LiTaO₃**·ref 45 = Han/**Zhu**/C.Wang **LGPS 단일물질 전지**([Zhu15]와 실험 앵커 공유)·ref 15 = 우리 `ong2013`·**연구비 SAIT 단독**(+SAIT 소속 공저자 2인)·functional **PBE 확정**(ref 32). ⚠ 0 K·계면E ~100 meV/atom 상한·**복원 수치는 "우리가 그림에서 읽은 값"이라고 명시할 것**(저자 제공 표 아님)·hull 2015 세대(Li₄P₂S₆/SCl entry 의존)·μ_Li=평균전압 고정(고SOC 가혹화 밖). **🆕 2026-08-03 SI 실물 전수 검증(digest §19)**: Tables S1–S9 **343행 화학 불일치 0**(Table S2↔S4–S9 중복 84쌍도 완전 동일 — 차이는 인쇄 항 순서뿐) + **Fig S1–S7 벡터 정확 판독으로 37 전해질 × 7 양극 = 259쌍 ΔΦ 전표**(±0.005 eV/atom; `tools/litdb/richards2016_si_figs.py` → `db/properties/richards2016_si_interface_reaction_energies.csv`). 🔑 **Fig 4에 없던 Li₆PS₅Cl 행 확보**(§19d) — `LiCoO₂ −0.97/−1.10`·`LiFePO₄ −0.52/−0.52`·`LiMnO₂ −0.51/−0.71`·`LiNiO₂ −0.49/−0.82`·`LiTiS₂ −0.03/−0.04`·`LiVS₂ 0/−0.01`·**`Li₂S 0.00/0.00`**; `Li₂S\|LiCoO₂`는 **−2.91 확정**. 교정 2건(§8c LiYF₄\|LiNiO₂ NiO 계수 3 누락 / §18f `LLZO\|LiFePO₄` no-mixing −0.21 → **−0.02**). **→ 본문·SI 모두 실물 대조 완료, digest 완결** | ✅ `papers/richards2016_interface_stability_pseudobinary.md` | DFT(hull 열역학+pseudo-binary, 실험 0) |
| **[Aykol14]** ⭐코팅 설계 열역학의 *원점*(액체 LIB·HF 축) · [Xiao19] 의 조부 | **Muratahan Aykol**/Scott Kirklin/**C. Wolverton\*** 2014 *Adv. Energy Mater.* **4**, 1400690 (Northwestern MSE 단일기관; DOI 10.1002/aenm.201400690, ⚠**OA 아님**; 연구비 Dow Chemical + DOE-EFRC CEES; 계산 프레임 **OQMD**; inbox #106 본문 11 pp + SI 4 pp 전독) — "**Thermodynamic Aspects of Cathode Coatings for Lithium-Ion Batteries**". ⚠⚠ **액체 LiPF₆ 전해질 LIB 전용** — 고체 전해질 언급 0, 적(敵)은 **HF**. 이원 산화물/불화물 쌍 **81종**을 VASP-PBE(520 eV·8000 kppra·PAW·ICSD·0 K·PV 무시)로 전수 계산해 **4속성 조합 설계도표**(−ΔH_s-HF · Ω_V · Ω_G · 불화물 전환전압)에 올림. 게이트 `0.30 ≤ −ΔH_s-HF ≤ 1.50 eV HF⁻¹` + `V(MₓF) ≤ 3.0 V` → **81→40→27**(본 digest 가 SI Table S1 81행 전수 재입력으로 **재현 확인**). 기존 코팅(Al₂O₃ 0.76·MgO 1.15·TiO₂ 0.41·ZrO₂ 0.59 eV HF⁻¹)이 상위 재현 → 틀 검증, 신규 예측 = **3가 d-block 산화물 Sc₂O₃·Ti₂O₃·V₂O₃·Cr₂O₃·Mn₂O₃·Y₂O₃**. 2차 기전 **LiF-scavenging** 29반응 제안(Li₃AlF₆ −0.118·Li₂TiF₆ −0.731 실험확인 / **Li₃ScF₆ +0.018 = 불안정**). 🔑 최대 소득 = **"HF 포획은 산물이 상온 안정 고체일 때만 보호가 된다"**(SiF₄·BF₃·PF₅ 기체 → SiO₂·B₂O₃·P₂O₅ 실패; P₂O₅ 는 HF 재생산). DFT 정확도 자기선언: ΔH **MAE 0.125 eV HF⁻¹** vs 실험 **CSU 0.055**, 전압 **±0.20 V**, **DFT+U 무의미**(0.157→0.149). ⛔ 우리 grand-potential ESW 의 조상 **아님**(μ 안 엶·산물 가정·eV per **HF** 정규화) — `papers/aykol2014_cathode_coating_thermodynamics.md` §6b | `papers/aykol2014_cathode_coating_thermodynamics.md` ✅ (2026-09-11, 본문 11 pp + SI 4 pp 전독 · 그림 6장 전량 실독 · **SI Table S1 81행 전수 재현**) | **코팅 설계 열역학 원점 · 계면 산물의 *물리상태* 게이트 · 가역 Li 손실 게이트 · 계보(→Aykol16→[Xiao19])** (순수 DFT 반응열역학, 실험 0) |
| **[Aykol16]** ⭐⭐코팅 HT 스크리닝의 *형식*을 만든 편(액체 LIB·HF 축) · [Aykol14] 의 직계 후속 · [Xiao19] 의 앞 세대 | **Muratahan Aykol**/Soo Kim/V. I. Hegde/D. Snydacker/Z. Lu/S. Hao/S. Kirklin/**Dane Morgan**(UW-Madison)/**C. Wolverton\*** 2016 *Nat. Commun.* **7**, 13779 (DOI 10.1038/ncomms13779, **OPEN**; 계산 프레임 **OQMD**; inbox #107 본문 12 pp + SI 6 pp + **CSV 2본 전수 분석**) — "**High-throughput computational design of cathode coatings for Li-ion batteries**". ⚠⚠ **액체 LiPF₆ 전용 · 적(敵)은 HF** (고체 전해질 언급 0). **깔때기**: OQMD 산소함유 ~130,000 → hull **5,225** → `E_d<3 & −E_c>3.5 V` **2,229** → 비방사성 & HHI<9000 **1,315** → **물리장벽 1,315 / HF-barrier(G≥0) 411 / HF-scavenger(−1.285<G<0 + 숨은 E_d(prod)<3 V) 583** → MOOP(weighted-sum + rank aggregation). **"안정"의 조작적 정의**: `E_d` = **hull 첫 상영역의 최고 계단 = 리튬화 개시**(평균 아님) · `E_c` = **양이온이 액체로 용출되는 전위**(NBS 수용액 표준산화전위 + 활동도 10⁻⁶, **DFT 아님**) · `G_s-HF` **eV per HF**. 기준 **vs Li/Li⁺**, DB **OQMD**. 결과: 물리·HF-barrier = 4d·5d 인산염(WO₃·TaPO₅·TaBO₄·ZrP₂O₇·Hf₂P₂O₉) / HF-scavenger = **Sc₂O₃ 1위·MgO 2위** + 규산염·붕산염(PCA 창에서 Si 4.1→≈24 %·B 3.8→≈14.5 %). 기존 코팅은 **탈락이 아니라 상위권**(Al₂O₃ 128·TiO₂ 139·ZnO 313·AlPO₄ 68위). 🔑 **Eq 4–6**: 코팅을 **양극과 먼저 평형**시키면(`LiCoO₂+αAl₂O₃→LiAlO₂+Co₃O₄+Li₂CoO₃`) 그 혼합물은 **더 이상 HF-scavenging 을 안 한다**(저자 표현 counter-intuitive). ⛔ **우리 db 와 섞지 않는다**: `E_c`(용출 전위) · `G_s-HF`(HF 없음 + **[Aykol14] 의 −ΔH_s-HF 와도 다른 양**) · `E_d` **값**(정의만 대조) · top-30 서열(F(x) 해상도 없음) — `papers/aykol2016_ht_cathode_coating_design.md` §13 | `papers/aykol2016_ht_cathode_coating_design.md` ✅ (2026-09-12, 본문 12 pp + SI 6 pp 전독 · **본문 그림 6장 전량 + SI Fig S1·S3·S4 실독** · **CSV 2본으로 깔때기·랭킹 독립 재현**) | **코팅 HT 스크리닝 형식(MOOP) · "안정"의 조작적 정의 · 계면 *평형 후* 기능 · 공급위험(HHI) 축 · 계보([Aykol14]→본편→[Xiao19])** (순수 DFT 반응열역학 + 실험 전기화학표, 실험 0) |
| **[Nolan19]** ⭐⭐⭐코팅 계산 계보 #4 = **Mo 그룹 본류** · 우리 `interface_reactivity` 의 **양극-SOC 적용 원전** · 우리 `2.256 V` 계보의 **형제 적용** | **Adelaide M. Nolan**/Yunsheng Liu/**Yifei Mo\*** (UMD MSE + Maryland Energy Innovation Inst.) 2019 *ACS Energy Lett.* **4**, 2444−2451 (DOI 10.1021/acsenergylett.9b01703; inbox #108 본문 8 pp + SI 8 pp + **Sup2 XLSX 1,896행**) — "**Solid-State Chemistries Stable with High-Energy Cathodes for Lithium-Ion Batteries**" (UMD, **외부**; **자체 DFT 0회·실험 0회** — **Materials Project** 에너지 + 유사이원 상평형 조합론만). 방법 조상 = **[Zhu16]** JMCA 4, 3253 + **[Zhu15]** + **[Rich16]**(형식화). 양극 **8상태** × 접촉 고체 **236종** = **1,888 쌍**. **"안정" = `E_d = 0` 불리언**(유사이원 상호분해에너지 최솟값, eV/atom, 끝점 준안정성 제거), **양극 리튬화·탈리튬화 각각**. ⛔ Ed 데이터셋에 **황화물 0·염화물 0** | ✅ `papers/nolan2019_chemistries_stable_high_energy_cathodes.md` (2026-09-12, **Sup2 XLSX 전수 재분석 포함**) | **[외부]** 순수 MP 반응열역학 (자체 DFT 0·실험 0) |
| **[Xiao19]** ⭐HT 코팅 스크리닝 원전·cascade 직계 조상 | **Yihan Xiao**/Lincoln Miara/Yan Wang(Samsung)/**Gerbrand Ceder** 2019 Joule (3, 1252–1275, DOI 10.1016/j.joule.2019.02.006, OA; inbox #37 본문+SI 전독) — "**Computational Screening of Cathode Coatings for Solid-State Batteries**" (UCB·LBNL·SAIT, **외부**; 순수 DFT HT, 실험 0; **[Zhu15] grand-potential + [Rich16] pseudo-binary를 10⁵ 규모 깔때기로 처음 게이트화** = 우리 cascade의 방법 직계 조상). **깔때기**: Li-함유 **104,082**(내부 DB: ICSD+data-mined) → F1 방사성 제외+**Eg>0.5 eV** 62,437 → F2 **E_hull<5 meV/atom** 1,600 → F3 **V_ox≥4.0 & V_red≤2.7 V**(양극 상한 4 V+황화물 창 2.2–2.7 겹침 조건) 302 → F4 **&#124;ΔE_rxt&#124;<100 meV/atom vs LPS+만충 NCM** 184(ICSD 106) → F5 폴리음이온 산화물 66 → F6 CI-NEB 6종 → **추천 LiH₂PO₄(E_m 0.33 eV)·LiTi₂(PO₄)₃(0.42·V_ox 4.59)·LiPO₃(0.40·V_ox 5.01)**; **붕산염 LiBa(B₃O₅)₃=화학안정 챔피언**(전 계면 −10~0 meV/atom·단 E_m 1.96 eV). 기전 = **비금속–O 공유결합→O 2p↓→V_ox↑+O–S 교환 반응성↓**(동일양이온 +phosphate +0.4~1.4 V·meta>pyro>ortho·B–O 806>P–O 597 kJ/mol) + **Li분율↑⇔V_ox↓ trade-off**(V_ox≥5 V→Li분율≤0.20; LiPO₃=0.20 스위트스폿). 소환값: **LPSCl/LCO ΔE_rxt −339(만충)/−493(반충)·LPSCl/NCM −330/−471·LPS/NCM −422 meV/atom**(산물 Li₃PO₄+Li₂S+Co₉S₈+Li₂SO₄+LiCl)·LPSCl ESW ~1.7–2.0 V(figure-read, [Zhu15] 동세대)·LLZO 2.9 V(실험 겉보기 4.0=kinetics)·3원 산화물 코팅 3.4–4.0 V. ⚠ 0 K kinetics 무시·NEB 프록시 실패 자기보고(LiPO₃ 0.40 vs exp 1.40 eV)·E_hull 5 meV 강컷(비정질 배제)·ΔE_rxt 닫힌계·2019 할라이드 보류·Samsung 특허 COI. **본문 실물 독립 재검증 2026-08-03: 불일치 0건**(digest §14) · **SI(Table S1–S6) 실물 독립 재검증 2026-08-03: 불일치 0건**(digest §15 — **ΔE_rxt 128셀 전량**(S2 76 + S3 52; 래스터 이미지 육안 대조)·Table S6 NEB 전 hop·Table S1 ESW 12값·S1 106행 집계). **SI에서만 나오는 신규 3점**: ⚠🔑 **기존 3원 산화물 코팅 3종(Li₂ZrO₃·LiNbO₃·LiTaO₃)이 Table S1에 부재 = 저자 자신의 filter 4 탈락**(LPS와 −115/−164/−139 meV/atom) — *현행 표준 코팅조차 못 넘는 게이트*라는 본문 미문장화 논거 / **불화물이 산화한계 최강**(ICSD 35종 전부 V_ox ≥4.99, LiBF₄ **7.15 V** > 폴리음이온 최고 6.23) → "폴리음이온 승"은 *안정성*이 아니라 **2019년 σ 문헌 부재**로 갈린 것(= 할라이드 보류 한계와 같은 뿌리) / 비폴리 생존 2종 정체 = Li₃V(H₄O₃)₄(4.17)·LiAl₅O₈(4.09) = 사실상 전멸. 정정 1건: NCM·LCO/LPSCl **반충 산물 = Li₂O 추가 + Li₂S 소멸**(SOC↑에서 계면이 더 산화적으로 열화) | ✅ `papers/xiao2019_cathode_coating_screening.md` | DFT HT-screening(hull+grand-potential+pseudo-binary+CI-NEB, 실험 0) |
| **[Nolan21]** ⭐⭐코팅 계산 계보 #5 = [Nolan19] 의 자기인용 후속, 무대 **가넷(산화물 SE)** · ★ **우리 grand-potential ESW 식이 이 계보에서 처음 인쇄된 편** | **Adelaide M. Nolan**/**Eric D. Wachsman**/**Yifei Mo\*** (UMD MSE + Maryland Energy Innovation Inst.) 2021 *Energy Storage Materials* **41**, 571–580 (DOI 10.1016/j.ensm.2021.06.027; DOE-EERE DE-EE0008858; inbox #109 본문 10 pp + SI docx(Fig S1–S9·Table S1–S4) + **Sup2/Sup3 XLSX 9시트**) — "**Computation-guided discovery of coating materials to stabilize the interface between lithium garnet solid electrolyte and high-energy cathodes for ASSBs**" (UMD, **외부**; **자체 DFT 0회·실험 0회** — **Materials Project** 에너지 + pymatgen + python-ternary, **ICSD id 보유 상만**; DFT 파라미터 **미기재**). 방법 = **[Nolan19]** 의 `E_d` 식 (1)–(4) 그대로 + **개방계 쌍둥이 식 (5)–(7)**. 대상 = LLZO(+LLSnO·LLNbO·LLTaO) × 양극 13상태 × 접촉물질(원소 66·이원 산화물 130·**Li 삼원 산화물 89**·사원 인산염/규산염/붕산염 ~85·삼원 할라이드 31). **"안정" = `|E_d| < 0.05 eV/atom` 문턱**(#4 의 불리언에서 **완화**) + 원소별 등급(Mg<0.003·Zr<0.005·Ti<0.03). ★ **Methods 식 (5) `μ_Li(φ)=μ⁰_Li−eφ`(기준 Li 금속) + 식 (6) `E_D^open`** = **우리 ESW 정의의 계보 내 첫 인쇄본**. ⛔ 그래도 *"limit ≡ E_D^open 이 0 을 벗어나는 φ"* 문장은 없고 φ 는 **3 V·5 V 두 점뿐** | ✅ `papers/nolan2021_garnet_cathode_coating.md` (2026-09-12, **Sup2/Sup3 XLSX 전수 재분석 + `Table 1`·`Table 2` 좌표 복원 + `Fig. S4`·`Fig. S5` 픽셀 캘리브레이션 포함**) | **[외부]** 순수 MP 반응열역학 (자체 DFT 0·실험 0) |
| **[Honrao21]** ⭐⭐코팅 계산 계보 #6 = 세트의 **분기점**(무대가 **음극**, 계면 반응에너지 0) · ★ **cathodic limit 을 *그림으로* 정의하는 유일한 편** | **Shreyas J. Honrao**(KBR Wyle/**NASA Ames**)/X. Yang/**B. Radhakrishnan\***/S. Kuwata/H. Komatsu/A. Ohma/M. Sierhuis(**Nissan**)/**John W. Lawson\*** 2021 *Sci. Rep.* **11**, 16484 (DOI 10.1038/s41598-021-94275-5, **OA**) — "**Discovery of novel Li SSE and anode coatings using interpretable machine learning and high-throughput multi-property screening**": MP Li 화합물 **15,446종** → softBV 3D 장벽 + **Li grand-potential 창**(8,924종) + `E_hull`·`E_g` → SE **>250** / **Li 음극 코팅 26종**(`Table S1`). GB 회귀 3개(장벽 R² 0.86 · 전위 0.95/0.92) + **SHAP·PFI**. **자체 DFT 0 · 자체 실험 0 · 공개 기계판독 데이터 0본** | digest ✅ `papers/honrao2021_interpretable_ml_sse_anode_coatings.md` (2026-09-12) | **[외부·계산 전용]** |
| **[Kim26HTS]** ⭐HT 코팅 스크리닝 현행판·[Xiao19] 후속·우리 cascade+M6 직접 대조군 | **Ji Hoon Kim**/Seunghyun Lee(한양대 ERICA)/**Sang Uck Lee** 2026 *Nano Convergence* (13:27, DOI 10.1186/s40580-026-00555-z, OA; 본문 13 pp + SI 21 pp 전독, **inbox #1 · 사용자 분류 폴더 `이상욱` · 본문 실물 독립 검증 2026-08-03 §13 = 교정 4·신규 10 · SI 실물 독립 검증 2026-08-03 §14 = 교정 6·신규 11**) — "**High-throughput discovery of Li₃Sc₂(PO₄)₃ as a protective coating for stabilizing mid-Ni NCM interfaces in ASSBs**" (성균관대 **이상욱 랩**; 순수 계산·실험 0). MP 17,230 → 8 → **Li₃Sc₂(PO₄)₃** + SevenNet 500 ps 계면 MD. **Table S1 88행 전수 기계 재입력 = `db/properties/kim2026_tableS1_88_candidates.csv`**(88행 × 11열; PDF 실물과 mp-ID 키 기계 대조 불일치 0) → 깔때기 컷 코드 재현 가능 | ✅ `papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md` | DFT+AIMD+MLIP |
| **[Lee24MO]** ⭐다성분 혼합-산화수 정본·우리 co-doping 캠페인 정면 대응 | **Ji Won Lee**/Ji Hoon Kim/Ji Seon Kim(SKKU)/현대자동차 5인/**Sang Uck Lee*** 2024 *JMCA* (12, 7272–7278, DOI 10.1039/d4ta00361f; 본문 7 pp + ESI 29 pp, **inbox #2 · 사용자 분류 폴더 `이상욱` · 본문 실물 독립 검증 2026-08-04 §11 = 교정 6·신규 16 · ESI 29 pp 실물 독립 검증 2026-08-04 §12 = 교정 4·신규 14**) — "**Design of multicomponent argyrodite based on a mixed oxidation state as promising SSE using moment tensor potentials**" (성균관대 **이상욱 랩** + **현대자동차**; 순수 계산·실험 0). 질서 모체 Li₆PS₅I 의 P 자리를 Li₅₊₂ₓ₊ᵧ[A]ₓ⁴⁺[B]ᵧ⁵⁺[C]₁₋ₓ₋ᵧ⁶⁺S₅[D] 로 열어 **84 구조 MTP-MD 전수**(ESI Table S2 전수 전사로 확정 = 12+18+18 = 48 + 군(4) 36 = **16 D₁.₀ + 15 D₁.₅ + 5 D₁.₇₅**). 최고 **Li₆.₅Si₀.₇₅W₀.₂₅S₅I 62.93 mS/cm·E_hull 2 meV/atom**. ⛔ **σ 절대값 인용 금지**(MTP 실험 대조는 0.001–**14.8** mS/cm 인데 본문이 파는 값은 **38–80**, 오차막대 0, **혼합할로겐 계는 MTP 검증 0개**) · ⛔ **계면·대기(Table S3/S4) 수치를 Cl-rich 논거로 이식 금지** — **할로겐을 분해하지 못한다**(Cl↔Br 7/8쌍, D₁.₅ 혼합비 7/7 완전동일) | ✅ `papers/lee2024_multicomponent_argyrodite_mixed_oxidation_mtp.md` | DFT+MLIP(MTP)+MD |
| **[Kim25CSP]** ⭐CSP·준안정 정본·덱 슬 26–29 원본 | **Ji Hoon Kim**/Ji Seon Kim/Yong Hui Kim(SKKU)/Byeongsun Jun·Yong Jun Jang(**현대차**)/**Sang Uck Lee*** 2025 *JACS* (147, 47381–47391, DOI 10.1021/jacs.5c15665; 본문 11 pp + SI 24 pp, **inbox #4 · 사용자 분류 폴더 `이상욱` · 본문 실물 독립 검증 2026-08-04 §19 = 자기철회 2·신규 8·Q2 해소 · SI 실물 독립 검증 2026-08-04 §20 = 정정 3·신규 21·MSD 궤적 40개 전수 전사**) — "**Machine Learning-Assisted CSP of SSEs Reveals Superior Ionic Conductivity in Metastable Edge-Sharing Phases**" (성균관대 **이상욱 랩**; 순수 계산·실험 0). MTP+USPEX+active learning CSP → 검증 14종 중 12 성공 → 표적 4조성(Li₂SiS₃·Li₂GeS₃·Li₄SiGeS₆·Li₄SiSnS₆) 각 10상. **핵심: 0 K 최안정 corner 상은 Li 가 갇혀 D≈0, 준안정 edge 상이 D_600K 를 2자릿수 이상 앞선다**. ⛔ **σ 인용 금지 — 이 논문은 σ 를 한 번도 계산하지 않는다**(본문 11 pp 어디에도 mS/cm 표기 없음; "3자릿수"는 ref 36 Huang JACS 2022 **실험 소환**). ⛔ **"SCAN 으로 검증됐다"는 본문 주장 인용 금지 — 자기 Fig 2a 가 반증**(Li₃PS₄ +8·Na₃PS₄ +23 meV/atom 부호 반전). ⚠ **"higher packing efficiency"(초록) 표현 이식 금지** — α 는 비전도 부피 분율이고 edge 가 **낮다**. **🔑 우리와의 관계 = "안 하기로 한 축"** — argyrodite PS₄ 는 고립 사면체라 corner/edge 축 자체가 정의되지 않는다. 이식: α **재구현 금지**(V_dead 알고리즘 미공개, 우리 BVSE 채널 % 가 우월) · **Li–(S,Cl)₄ 부피 + CSM 은 기존 궤적 후처리로 즉시 가능** · **van Hove = T12 승격 근거 2건째** · $S_{vib}$ 가 상 순서를 뒤집는다 → `ordered_vs_disordered.md` §9. **🗃 2026-08-26 저자 데이터저장소 실측(§21, `db/external/kim2025_csp_sse/`, ⛔LICENSE 없음·내부 전용)**: ⭐ **T14 참조구현 확정** — 그들의 CSM 은 SI eq 10–11 손구현이 아니라 **pymatgen `chemenv` `T:4` CSM**, Li–S₄ 부피는 **이웃 S 4개 `ConvexHull`**, **Li 자리별 궤적평균**(⇒ Fig. 5 의 원 하나 = Li 자리 하나) → 우리 **Li–(S,Cl)₄** 판은 `non_elements()` 에서 Cl 만 남기면 되고, **코드결함 C1/C3/C5 는 고쳐서** 이식 · ⛔ **α 재구현 금지 최종 확정** — V_dead 코드가 **저장소에도 없다**(문서 순환위임에 이어) · ✅ **Q6 부분 종결**(학습셋 train 863/1,391/1,038/1,104) · ✅ **AIMD 셀 규약 ~10 Å** 확보 · 🔬 **배포 CIF 40개 연결방식 독립 검증 36/40**, **M–M 거리 완전 이분(edge 2.96–3.28 vs corner 3.46–4.01 Å)** = 이 논문 중심축의 컷오프 비의존성 확인 + **Fig. 4e 의 d_c>d_e 최초 수치화** · 🔴 **Li₂GeS₃ #6·#7·#10 만 어긋난다 → Q9** (배포본은 edge 가 #7 하나뿐, Fig. 3c 는 6·10) ⇒ ⛔ **Li₂GeS₃ 는 배포자료로 재현 금지**(다른 3조성은 안전) · 🆕 **4조성 모두 edge 셀이 더 크다**(V/atom +1.2~6 %) ⇒ α 는 분자↓·분모↑ 양쪽에서 내려간다(논문 미언급, 주장 강화) | ✅ `papers/kim2025_csp_metastable_edge_sharing_sse.md` | CSP(USPEX+MTP+AL)+DFT+AIMD+phonon (실험 0) |
| **[Huang22]** ⭐**[Kim25CSP] 의 ref 36 = 우리 철회값 3건의 진짜 출처** · BVSE 외부 대조사례 | **Wenze Huang**/Matsui/Hori/Suzuki/Hirayama/Yonemura/Saito/Kamiyama/**Yuki Sasaki·Yongsub Yoon(Hyundai Mobility Japan R&D)**/**Saheum Kim(현대자동차 화성)**/**Ryoji Kanno\*** 2022 *JACS* (144, 4989–4994, DOI 10.1021/jacs.1c13178; **ACS AuthorChoice + CC-BY-NC-ND → 그림 재가공 금지**; 본문 6 pp + ESI 12 pp, **inbox #47 · 사용자 분류 폴더 `DFT` · 본문 실물 독립 검증 2026-08-04 §9 = 자기정정 11·신규 16 · ESI 실물 독립 검증 2026-08-04 §11 = 자기정정 6·신규 18**) — "**Anomalously High Ionic Conductivity of Li₂SiS₃-Type Conductors**" (도쿄공업대 Kanno 랩 + KEK; JST OPERA JPMJOP1862). Li₂S–SiS₂–P₂S₅ **13 조성** 탐색에서 새 정방정 **n-Li₂SiS₃**(P4₂2₁2, **고립 edge-shared (Si/P)₂S₆ 이량체**, Li1 4d 0.866/Li2 8g 0.552) → **σ 2.4 mS/cm @ 298 K**, corner-shared 무한사슬 e-Li₂SiS₃ 대비 **3자릿수**(실측 n/e = 1277×). 승온하면 **n→m→e** = **edge 가 저온상**([Kim25CSP] 의 '준안정 edge' 서사와 방향이 다르다). ⛔ **제1원리 계산 0** — 폴더는 `DFT` 지만 계산은 **경험적 bond-valence 단독** → DFT 벤치마크 인용 금지. ⛔ **Ea 0.28 eV 를 창 없이 인용 금지** — 280–375 K 한정이고 228–280 K 는 **0.347 eV**(ESI Fig S4 재구성). ⛔ **'85 % 밀도에서도 입계저항 작다'를 일반 서술로 쓰지 말 것** — 228 K 에선 **R_gb 가 36.3 %**. ⚠ **조성식이 논문 안에서 둘**(본문 Li₁.₈₂SiP₀.₀₃₆S₃ ↔ Table S1 Li₁.₉₇Si₀.₉₇P₀.₀₃S₃ = Rietveld 값). ✅ **구조 주장은 좌표만으로 전수 재현**(M–M 2.849 Å·S 2개 공유 = 고립 edge 이량체; Li1–Li2 2.396 Å edge / Li2–Li2 3.462 Å corner) | ✅ `papers/huang2022_li2sis3_anomalous_conductivity_bvse.md` | exp(XRD·중성자 Rietveld·EIS·CV·풀셀) + **BVSE(softBV)**; **DFT 0**, 외부 |
| **[Sendek17]** 🤖ML-스크리닝 대표작·TabPFN 선행 | **Sendek**/Qian Yang/Cubuk/Duerloo/**Yi Cui**/**Evan J. Reed** 2017 EES (10, 306–320, DOI 10.1039/c6ee02697d; inbox #40 본문 15 pp + SI 31 pp — 2026-08-03 양쪽 실물 전수 검증) — "**Holistic computational structure screening of more than 12 000 candidates for solid lithium-ion conductor materials**" (Stanford, **외부**; MP-DB 소환+로지스틱 회귀 — 자체 실험 0·자체 DFT는 SI S5 1건). **깔때기: MP Li-함유 12,831 → 전제조건[E_hull=0(1,472=최강 필터)·무TM·gap≥1 eV·V̂_ox=ΔG_f/xF≥4 V] 317 → 5-특징 LR P_LR>50% → 21종**(모델 단독 1,408 = **"전제조건이 전도도 스크린보다 세다"**). **ML 본체**: 실측 40종(σ≥10⁻⁴ 이진, 11/40 superionic; **부분점유 23종 = Bernoulli 점유+Metropolis 스왑 특징 기대값**)·특징 20종(위치·EN·반경만) **전수 조합 1,048,575** 중 LOOCV 최적 **5특징**(LLB+·SBI−·AFC−·LASD+·LLSD−; **전 단일특징 \|r\|≤0.3**)·**TMR=CVMR 10%·FP 18% vs X-랜덤 75%(4배 농축)·cR²_p 0.59**·신뢰지표 **d/ε/A**(PCA 훈련중심거리·LOO 분산·적용영역). 후보: 티오보레이트 5(**Li₅B₇S₁₃** — VASP-PBE-MD 900 K·Γ·499 eV·공공 5%: σ 3 S/cm·RT 외삽 0.026–1.6 S/cm)·**Li₃InCl₆/Li₃ErCl₆**(→2018+ 할라이드 SE 붐 사후 적중, [Cha]/[Schlem20] 직결)·LiLnS₂ 5(vdW 위험군 자인)·**LiCl=자인 FP**. bcc-패킹(Wang) "황화물 밖 비보편"·BV cross-material 스크린(LiAlSiO₄ 반례) 반박. **🔑 훈련 40 ≈ 우리 47 도펀트 체급 — LOOCV·5:1 절제·X-rand·d/ε/A = 우리 TabPFN(M1–M3) 방어 논리의 선례**. ⚠ "92.2%" 표기≠산술 97.5%(12,831→317)·P_LR=1.000 4종=mixed-anion 인공물(실질 16종)·**argyrodite 전무(DB 커버리지 천장)**·V̂_ox=상한이지 물성 아님. **📌 2026-08-03 본문 실물 독립 재검증(digest §16, 인박스 #40·폴더 `DFT`)**: 표 3종 332값 **불일치 0**·refs 113건 귀속 전건 확인 → 교정 2건(**훈련셋 = 39 조성 / 40 구조**, Li₃OCl V̂_ox 본문 3.438 V)·**"92.2%만 단독 오류" 증명**·**cR²_p는 n=5에서 최대가 아님(n=10 ≈0.70) ⇒ 모델 선택은 CVMR, cR²_p는 사후 유의성 검사**(M1 이식 시 역할 혼동 금지)·**Fig 4에 최악 외삽 후보 2종(d 5.149·6.852)이 축(0–5) 밖**(M3 그림 반면교사)·신규 "σ↔안정성 상충" 명문(낮은 Ea ↔ 작은 \|ΔG_f\| ↔ 높은 반응성). **📌 2026-08-03 SI 실물 독립 검증(digest §17)**: Table S1–S4 **1,822셀** + Fig S1–S5 이미지 판독 + SI refs 22건 → **digest 인용 46항목 불일치 0**, **미결 3건 전건 종결** — SI-로컬 ref 실명 확정(20=**Haven 1950**·21=Wada=본문95·22=Richards=[Rich16]) · **σ 문턱 모순 아님**(본문 5×10⁻⁶=중앙값 50/50 ↔ Fig S5 10⁻⁵=CVMR **피크** 40%; Table 1로 11/16/21 of 40 재현) · Li₃OCl V̂_ox 본문 3.438 vs SI 3.439 = 논문 자체 말자리 불일치. 교정 3건(LiAl₃Si₉(N₇O)₂ · Table S3 # 저신뢰 8→**12종** · Li₂B₂Se₅). ★ **Fig S4 축 라벨 전치** — 색 있는 행이 정확히 23개라 "40 구조 / 23 부분점유"를 그림이 독립 검증. ★ **eq S21·비용모형 자체 재현 성공**. ⚠ **SI 전문에도 MD 앙상블·시간·MSD 창 없음 = n/a 확정**(축 A 신규 행 참조) | ✅ `papers/sendek2017_ml_screening_12k_conductors.md` | MP-DB+통계학습(LR)+DFT-MD 1건(실험 0) |
| **[Fujimura13]** 🤖ML 1세대 원조 | Fujimura⁺/**Seko**⁺(공동1)/Koyama/Kuwabara/Kishida/Shitara/Fisher/Moriwake/**Isao Tanaka** 2013 AEM (3, 980–985, DOI 10.1002/aenm.201300060; inbox #42, SI 미보유, **본문 전문+Fig 1–4 실물 독립 검증 2026-08-03**: 교정 6·신규 5·미결 0) — "**Accelerated Materials Design of Lithium Superionic Conductors … and Machine Learning Algorithms**" (Kyoto·JFCC·Osaka City, **외부**; **비-argyrodite=γ-LISICON 산화물**, 자체 실험 0). **γ-Li₈₋cA_aB_bO₄(A=Zn/Mg/Al/Ga/P/As, B=Ge/Si) 92조성 HT-FPMD**(VASP/PBE/**Γ-only/300 eV**/16 f.u./NVT Nosé/2 fs/0 K 부피 고정, **1600 K 단일점**) **D₁₆₀₀ + Tc**(팔면체 Li 질서-무질서; 무작위 20배열 평균+점근사 엔트로피; **1150/750/380 K**, Zn↓=Tc↓) **+ V_dis**(정적 2684회)를 특징으로, **실험 σ 95점(문헌 취합)을 라벨로 가우시안-커널 SVR**(특징 D₁₆₀₀/Tc/V_dis/T·bootstrap HPO·**log σ 오차 0.373**≈×2.4) → **σ(373 K) 예측 지도 72 막대**(실물 재계수 ✓; **끝단 중복 포함 → 독립 58조성**, Li₄GeO₄ 6회 등장): **γ-Li₄GeO₄ 1위 ≈4.7×10⁻⁴ S/cm**(⚠ α로 결정화=γ 미합성; 원조 LISICON Li₃.₅Zn₀.₂₅GeO₄ 1.15×10⁻⁴의 **≈3.9배** = 본문 "a few×" 검산 일치)·차상위 Li₄SiO₄·**Li₃.₅P₀.₅Si₀.₅O₄** 등 **7화학식군=12조성**(σ>LISICON **AND** ΔF^S₁₆₀₀<0 — **이중기준 전수 교차검증 통과**). ⚠⚠ **예측폭 1.83 dec vs 자기오차 0.373 dec(비 4.9) → 1위 vs 2위 Li₄SiO₄ 격차 0.19 dec = 오차 이내, "1위" 순위 비분해**(원조 대비 0.61 dec만 유효). **🔑 물리 부산물**: D₁₆₀₀↮V_dis(전역 격자부피 통념 92조성 반증)·**p_Oct(팔면체 Li 점유율)=1차 인자**(2·3가 tie line 2 예외 자인 → **실물 판독: 예외의 정체는 포화**, p_Oct=0에서 D≈0.1×10⁻⁹ / p_Oct≳0.25에서 6–8×10⁻⁹ 포화 = **onset 기술자**)·**"Tc 아래 고온 외삽 무효"**(FPMD 외삽 실험 일치는 523–673 K만, <523 K 굴절=질서화). 검증=논문 내 0("in progress"만) | ✅ `papers/fujimura2013_ml_conductivity_origin.md` | DFT+AIMD(FPMD)+ML(SVR), 실험 0(라벨만 문헌) |
| **[Ong13]** ⭐조성족 스캔 원형·Ceder 4부작 1편 | **Shyue Ping Ong**/Yifei Mo/W.D.Richards(MIT)/Miara·H.S.Lee(Samsung SAIT)/**Gerbrand Ceder** 2013 EES (6, 148–156, DOI 10.1039/c2ee23355j; inbox #43 본문 9 pp·ESI 미보유; **본문 실물 독립 검증 2026-08-03** — digest §18) — "**Phase stability, electrochemical stability and ionic conductivity of the Li₁₀±₁MP₂X₁₂ (M=Ge,Si,Sn,Al,P; X=O,S,Se) family**" (**외부**; 순수 DFT+AIMD, 실험 0; **우리 cascade의 2013 조상 — [Zhu15]·[Rich16]·[Xiao19]의 제1편**, Mo·Richards·Miara가 후속 편 저자). LGPS 골격 **11조성** 3축 전수: **①hull** E_decomp 황화물 19–25(Al 60)/셀렌 16–19/**산화물 92–97 meV/atom(Li₃PO₄ 경쟁→합성 불가)**, 전 조성 metastable **②전기화학** HSE DOS(gap 순서 **O>S>Se** — 본문 수치 0, Fig 2 디지타이즈 **O ≈6.7/S ≈3.7/Se ≈2.3 eV**)+**VBM·CBM=음이온 상태** + **grand potential 2-포인트(0/5 V, onset 없음)**: 음극 전 조성 **Li₂X+Li₃P+LiₓM_y 합금**("전도성 SEI 가능·금속 산물 걱정")·양극 산화물만 **O₂ 방출**(황·셀렌=P₂S₅/PSe passivating) **③AIMD**(단위셀 50원자·Γ·280 eV·2 fs·NVT 0K부피·40–400 ps·600–1200 K 외삽·Haven=1 암묵) **σ300 Ge 13/Si 23/Sn 6/Li₉P₃S₁₂ 4/Li₁₁AlP₂S₁₂ 33 mS/cm = **8.25배 폭인데 전부 "오차 내 동일"**(M·캐리어 둔감, t-검정)·O 0.03(Ea 0.36±0.05, **433배↓ = 2.6자릿수**; 논문 Results "3자릿수"↔Discussion "2자릿수" 자기 불일치)·Se 24(불변)** + **격자 ±4% 스캔 비대칭**(−1%→σ÷10·−2%→10⁻⁶ vs +4%→×6; Ea 0.59→0.17) → **"S²⁻ 근최적·임계 채널크기"**; Zeo++ 채널 O 1.43–1.50/S 1.84–1.92/Se 1.96–1.97 Å(M 무영향). 기전 = **M–Li가 S²⁻로 스크리닝** + "이미 부분점유라 대부분 Li mobile". ⚠ 단일 Ewald 배열 전물성·Ea ±0.03–0.09→σ300 ×3–10 오차(순위 인용 금지)·onset 미계산(창 정량은 [Zhu15])·결론부 Li₁₂ 오타 | ✅ `papers/ong2013_lgps_family_substitution.md` | DFT+AIMD(실험 0) |
| **[Kahle20]** ⭐HT-MD 스크리닝 원전 | **Leonid Kahle**/Aris Marcolongo/**Nicola Marzari** 2020 EES (13, 928–948, DOI 10.1039/c9ee02457c; inbox #41 PDF쌍(본문 21 pp+SI 35 pp) **양쪽 실물 보유**·전독, 순번 #46; **폴더 `DFT`·본문 실물 독립 재검증 2026-08-03** — 방법 규율·깔때기·Ea 불일치 0, SI 유래 D 절대값 6건 교정(본문 Fig 5·7 legend 기준); **SI 실물 독립 검증 2026-08-03** — Table S1–S5 **883셀** + Fig legend **704 D값** + Fig S1/S2/S3 이미지 판독 → **불일치 0·미결 3건 전부 종결**, FPMD 창은 **"SI 명문 ≥20 ps 하한 + 그 위 물질별 custom"**으로 최종 확정, SI 자체 결함 3건 적발(Fig S12≡S13·**S85≡S93 중복 → 그룹 C 70종 중 1종은 MSD 그림 부재**·본문↔SI 750 K D 8종 중 7종 불일치=**동일 궤적을 블록만 달리 분해한 것으로 추정, 값 3–25%·오차막대 3× 변동**), 내부 불일치 4종→**7종**) — "**High-throughput computational screening for solid-state Li-ion conductors**" (EPFL THEOS·MARVEL, **외부**; 순수 계산·실험 0; AiiDA 전 계산 provenance·Materials Cloud 2019.0077/v1 공개). **ICSD+COD 전수 깔때기**: 유니크 4,963 → 원소/결합 필터 1,362 → PBE 절연체 1,016(전도준위 점유<1e-3 e 판정, gap 값 미사용) → vc-relax 971(부피 +4% 피크) → **pinball-MD 796(총 7.6 μs)** → FPMD 132(총 45 ns) → **신규 fast-ion 5종**(Li₅Cl₃O 0.33/0.27·Li₂CsI₃ 0.19(⚠host 전 T 유동)·LiGaI₄ 0.35(⚠vdW無 +19.5%→D3 −1.03%)·LiGaBr₃ 0.26·**Li₇TaO₆ 0.29±0.02 eV**=host 완전 안정 3D 최청정; LGPS 0.14±0.04 레퍼런스)+potential 40+**비전도 70(정직한 음성; 실험 모순 2건 명시)**+기지 39 재발견. **pinball**(Li-only **frozen-host+frozen-density**, 물리항 3-파라미터를 DFT 힘 5,000성분에 회귀, 스텝당 ~4자릿수↓) = **정량 D 실패(Fig 15 산포; 자인 4원인에 host 동결 포함)·랭킹 유효(quartile 성공률 71→36→33→21%·예측률 54%)**. **MD 통계 규율 원전**: MSD 기울기(eq 2; 총MSD/6t는 진동 오염)·**창 검증**(t' 5–40 ps 스캔→pinball 8–10 ps 고정; FPMD는 물질별 custom interval)·블록 분산 오차(mean±SE)·**자동 수렴 err(D)<1e-8 cm²/s or <5%**·1/T 등간격 4T·**Bayesian Ea 오차**·검출하한 1e-8 명문·**σ 환산 자체를 안 함**(D_tr만). ESW·기계 기준 의도적 미채택("interphase로 작동"·"dendrite=결함 지배"). ⚠ **부분점유 입구 제외 → LPSCl/LPSBr 풀 진입 불가**·질서 Li₆PS₅I=caged 해상불가([Klerk]·[Kraft] 삼각)·Γ-only·d_inner 6.5 Å FPMD=스크리닝 타협 | ✅ `papers/kahle2020_ht_aimd_screening.md` | DFT+pinball-MD+FPMD(실험 0) |
| **[Anderson24]** 🧪HT *실험* 도펀트 스크리닝·**우리 cascade의 가넷 실험판** | **Ethan Anderson**/Zolfaghar/Jonderian/Khaliullin/**Eric McCalla*** 2024 *Adv. Energy Mater.* (14, 2304025, DOI 10.1002/aenm.202304025, Open Access; 본문 12 pp + SI 17 pp 전독) — "**Comprehensive Dopant Screening in Li₇La₃Zr₂O₁₂ Garnet SE**" (McGill Univ., **외부**; **⚠⚠ 산화물 가넷 = 비-argyrodite → 물성 4축 A–F 어느 행에도 *수치* 편입 금지**; 자체 계산 0 = DFT 결함에너지는 ref[12] Miara/Ceder 2015 **인용**). **59 도펀트 × Li/La/Zr 3자리 = 177 시료**를 동일 HT sol–gel·동일 측정으로 6축 전수. **구조적으로만** 우리와 대조할 것: **(i) V_max가 59/59 축퇴(56종 3.9 V·3종 3.8 V) → 축을 ∫Idt(분해 전하량)로 갈아탐** = 우리 axis ①(S²⁻-limited onset, comp1=modelc **2.256 V 동일**)과 **동형의 논증**([Banik]/[Rich16] 명제의 실험 규모 확인) — ⚠ 절대전압 비교 금지(CV·액체전해질 kinetic vs 0 K grand-potential). **(ii) 깔때기 없음** — 컷은 SI Table S5 캡션 볼드 규칙 5개뿐이고 그중 host 앵커는 **∫Idt<1.39(=undoped 실측)** 하나; digest 재구성 결과 **5컷 순차 적용 시 생존자 0** → 저자들이 **codoping + "ML이 필요하다"**로 결론을 옮긴 이유 = 우리 가중 score·`codoping_ml_v2`의 외부 정당화. **(iii) 우리 정직성 장치 6종 중 1·2·3·4 대응물 없음, 5·6 부분**; 반대로 그들에게만 있는 3종(하한/구간 CCD 보고·미동정 상 공개 Fig S4·전해질 교차검증 Fig 6b–d)은 **우리가 이식할 것**. **(iv) σ_e→dendrite 인과 반박**(CCD는 저전압 안정성과 강상관·σ_e와 무상관) = 우리 B₂O₃/절연 SEI 서사에 대한 **외부 반례** → 발표 시 선제 방어 필요(반박점: 계면 액체 적심·σ_e 스팬 1자릿수·상대밀도 89–96 %). **(v) 원소 수렴 W·Sc** = 우리 cascade WO₃(G1–G5 유일 생존자)·Sc₂O₃(score 1위) + [Kim2026] Li₃Sc₂(PO₄)₃ — ⚠ **이유 다름, 원소 일치까지만**. **(vi) 우리 47종 양이온 원소 36종 중 32종이 이 59종 안** = 원소 수준 실험 sanity-check 참조표(부호·경향만) **🔴 2차 패스 2026-08-04 (SI 없이 본문 그림 픽셀 역판독, digest §19) 이 바꾼 것 3가지**: **(vii) 서술자는 *게이트*지 *순위기*가 아니다 — 이 논문으로 처음 수치화.** Fig 3c/3d 되읽기 결과, Miara 결함에너지가 고른 자리는 **실제로 3자리 중 cubic% 1위를 49/51 (96 %) 맞힌다**(꼴찌는 Mo 하나) — 즉 **"어느 자리에 넣나"는 진짜 예측력**. 그런데 **서술자의 *크기* 는 cubic% 를 전혀 예측 못 한다(BV mismatch ρ = −0.05 · 결함에너지 ρ = 0.00)**. → **우리 cascade에서 치환/결함 에너지를 가중 score 항으로 넣으면 안 되고 통과/탈락 게이트로만 써야 한다**는, 59 도펀트 실험으로 뒷받침된 설계 규칙. **(viii) 값싼 자리-적합 서술자(BV mismatch)는 DFT 대체재가 아니다** — argmin 일치율 **18/35 = 51 %**, **불일치 17건 중 15건이 한 방향(BV→Li / DFT→Zr)** = 편향된 동전던지기. 본문은 이걸 정성적으로만 자인한다. → **[Ren26] 의 Φ=z/r 붕괴(R²=0.065, Spearman −0.089)와 같은 결의 독립 사례** — 0-비용 정전기/기하 서술자는 사전필터까지이고 순위는 항상 더 비싼 축(우리는 Bader/ICOHP/BVSE 경로장벽)으로 매겨야 한다. **(ix) 이 논문 수치의 신뢰등급이 올라갔다** — 1차 digest(SI Table S5 전사)와 2차 패스(그림 픽셀)가 **서로 독립 검증**(garnet% |Δ| 중앙값 0.03 pp · cubic% 0.15 pp · σ_i 1.06×; ">10× 36종"·"저하 3종" 재현). ✅ **3차 패스 2026-08-04 (SI PDF 직접 재판독, digest §20) 이 그 미해결 4칸을 확정했다** — Table S5 가 텍스트 레이어라 기계 파싱됐고, 이로써 **①SI 손 전사 ②본문 그림 픽셀 ③SI 기계 파싱 세 경로가 서로를 검증**한다. `Rh↔Ho` 는 **우리 1차 digest 의 철자 오타**였고(논문 무결), `Y↔Yb` 는 **논문 자체의 Fig 4 오류**다 (Fig 3 이 59/59 전부 Table S5 와 같은 라벨 → **Table S5 채택: Y(La) σ_i 2.46e-5·σ_e 3.14e-8 측정됨 / Yb(La) 미측정**). **인용 금지 해제.** **(x) 그 결과 우리 쪽에 실제로 생긴 것 — Y 가 후보로 올라온다.** §8 의 '고전압 passivation 최강군 **Sc·Y·Dy·Er**'(∫Idt: Dy −0.05·Sc 0.36·**Y 0.53**·Er 0.57 ≪ undoped 1.39) 중 σ 가 있는 건 Dy·Sc·Y 셋이고(Er 결측), 그중 **저자 자신의 merit 컷 cubic>94 % 를 통과하는 건 Y 하나뿐**(Y 94.60 / Dy 93.83 / Sc 62.86). = **'산화 억제 상위군 + 고입방화'를 동시에 만족하는 유일 도펀트**. → 우리 cascade 의 **Sc₂O₃(score 1위)·WO₃(G1–G5 유일 생존자)** 옆에 **Y₂O₃ 를 나란히 놓을 외부 근거**가 생겼다 (⚠ 산화물 가넷 → **원소 수준 힌트까지만**, 수치 이식 금지 — [Kim2026] Li₃Sc₂(PO₄)₃ 와 같은 취급). 부수로 **본문 '>10× 36종' 은 엄격히 35종**(Ho 9.7× 반올림 포함해야 36)이고, **§3e 깔때기 59→19→6→1(Ga)→0 은 SI 표로 기계 재실행해도 그대로**다 (= 우리 가중 score 설계의 외부 방어 논거가 **저자 표 수준에서 확정**). 그리고 본문 문장 2개는 **철회**: "선호 site 는 >90 % cubic 이 대다수"(실측 42 %뿐, 중앙값 74.9 %) · "총 garnet 대체로 >95 %"(Fig 3a y축이 80 wt% 에서 잘려 Mo·Rh·Pd·Te 가 그림에서 사라진 상태의 인상). | ✅ `papers/anderson2024_llzo_comprehensive_dopant_screening.md` | 순수 실험 HT(PXRD/Rietveld·EIS·DC σ_e·CV-ESW·CCD), 자체 계산 0 |
| **[Ren26]** ⛔프리프린트·⚠할라이드 | **Yuan Ren\*** 외 8인(内蒙古科技大 Baotou) **Authorea 프리프린트(동료심사 전)**, DOI 10.22541/authorea.15005774/v1 — "**Regulation of the Lattice Dynamics of Li₂ZrCl₆ SEs via Low-Ion-Potential Element Doping**". **할라이드 Li₂₊ₓZr₁₋ₓMₓCl₆(M=Er/Nd)**. exp(볼밀 45 h·XRD/Rietveld·XPS·Raman·EIS·NCM811셀) + DFT/AIMD/NEB/**phonon VDOS**. σ_RT 0.227→**1.32/1.13 mS/cm**(≈5–6×)·NEB 0.658→0.370/0.417 eV·100 cyc 82.5 %. **🔑 우리 수확은 그들 결론이 아니라 *재분석* 3건**: ①**"ion potential" = Φ = Z/r (Shannon VI, pm⁻¹)** 정의 확정(Table S6 18계 **18/18 역산 일치**) → **`lee2024` inductive effect와 *같은 축·반대 부호·다른 인과경로***(그들 ref[29] JACS 2026이 곧 inductive effect인데 이 논문은 저-Φ 처방; **Bader/COHP 0건**) ②**서술자 붕괴**: Table S6 재분석 **R²=0.065·Spearman −0.089**(문헌 16쌍만 보면 −0.045), 같은 Φ=0.0781서 Ta 1.42 vs Nb 0.55(2.6×), **Li 함량이 더 나은 예측자(ρ +0.628)** ③**σ 격차=외삽 산물**: NE 역산으로 셀 72원자·N_Li=8(2+x)·**단일부피**·11/11 재현 확정 → D₀ 복원 → **Meyer–Neldel R²=0.93·E_MN 57 meV≈시뮬 kT**, **600–900 K 분산 2.3–3.6× → 300 K 외삽 29.6×**. ⚠ 본문 volcano ↔ SI Table S5 모순(Er 첫 도핑 σ **8.8× 하락**)·**Er x=0.25 이론/실험 방향 반대**·⟨ω⟩ 값 없음·E_hull/ESW/gap/탄성 0 | ✅ `papers/ren2026_li2zrcl6_low_ion_potential_doping.md` | exp + DFT/AIMD/NEB/phonon (**프리프린트**) |
| **[Wu26]** ⭐⭐계면 산물품질 최신·★★방법론 반례 | Xin Wu/Lixin Liang/…/**Shaochun Tang\***/**Guangjin Hou\***(DICP)/**Haoshen Zhou\***/**Ping He\*** (**Nanjing University**) 2026 *Angew. Chem. Int. Ed.* **65**, e23225, DOI 10.1002/anie.202523225 (**VIP**) — "**High-Conductivity Argyrodite Electrolyte with Self-Passivating Stability for Single-Electrolyte ASSLBs**". **`Li₅.₅P₀.₉₄Ta₀.₀₆S₄.₅Cl₀.₇₅Br₀.₇₅`** (Cl/Br 이중 할로겐 ΔS_conf/R 2.08 최대 + P-자리 Ta⁵⁺ 6 %). σ **12 mS/cm**(30 °C)·Ea 0.32→0.28 eV·σ_e 9.7e-9→1.4e-9·CCD 0.8→2.4 mA/cm²·대칭셀 >1600 h·1200 cyc 81 %·**10×6 cm² 파우치 200 cyc 96.4 %**. **핵심 = 계면 XPS 비대칭 CEI LiTaO₃ / SEI 금속 Ta⁰**. exp 강 + **계산층(밴드갭 스크리닝·NEB·AIMD·ICOHP·COMSOL) 절반 붕괴** — AIMD **300 K 20 ps 1시드**, Ta DFT 셀 **+22.8 % 부피(실험 +1.03 %)·x≈0.25(명목 4배)**, U/스핀 0, COHP 부호규약 붕괴, 계면 열역학 계산 0건, 오차막대 0 | ✅ `papers/wu2026_ta_argyrodite_selfpassivating.md` (감사 §4·§11) | exp 주 + DFT/AIMD 보조 + COMSOL |
| **[Ling26]** ⭐열수송 축 신규·★★계산감사 2호 | **Bingyue Ling**/**Kun Li**/Y.Meng/Z.Fang/K.Qian/**Xu Yang\***/G.Wang/B.Li/F.Kang/**Dong Zhou\*** (**칭화대 선전국제대학원** + Great Bay Univ. + UTS Sydney) 2026 *Angew. Chem. Int. Ed.* e1775824 — "**Dual Thermal Stabilization Toward Highly Safe and Durable ASSLMBs Based on Sulfide Electrolytes**". **전해질은 시판 `Li₆PS₅Cl` 그대로**(우리 comp1 과 같은 화학식), 바꾼 건 배치 두 곳: 음극쪽 **3층 `LPSC/LPSC–FG/LPSC`**(불소화 그래핀 10 wt%) + 양극쪽 도전재를 **산소공공 CuO₁₋ₓ** 로 교체. 본문 11 pp + **SI(.docx)** Fig S1–S31·Table S1–S4 전문. **DFT 는 산소흡착 막대 4개 + 계면 AIMD 10 ps 가 전부**(NEB/DOS/Bader/COHP 0건) | ✅ `papers/ling2026_dual_thermal_stabilization_fg_cuox.md` | exp 주도 + DFT/AIMD 보조 + COMSOL |
| **[Cho25AL]** ⭐⭐⭐**실험 능동학습 축 신설**·cascade 재설계 1순위 | **Min Young Cho⁺**/**Kyunglim Pyo⁺**/B. D. Lee/H. Kim/J. Shin/J. Y. Seo/**Woon Bae Park\***/**Kee-Sun Sohn\*** (세종대 나노신소재 + 순천대 프린티드일렉트로닉스) 2025 ***Small* 21, 2410008** (DOI 10.1002/smll.202410008) — "**Discovering Multi-Compositional Li-Argyrodite SSEs via Experimental Active Learning**". **PSO 5라운드 × 20 실합성**(대리모델·acquisition **없음** — 목적함수가 실제 EIS σ). 두 공간(P-free Ge-Si-Sb-I / P-included P-As-Sb-Si-I-Br) + **공정변수(소성온도·냉각률)를 결정변수에 포함**. 최적해 **Li₆.₄₂₅Ge₀.₂₅Si₀.₃₇₅Sb₀.₃₇₅S₄.₈I₁.₂ = 7.45 (관행) / 13.02 (가압) mS/cm**, 200 사이클 86 % (Si-Sb 2원계 61 %). 검증 = VASP PBE + Coulomb 전수열거(4×10⁸ 배열) + AIMD 250 ps. 🔴 **±3 % 재현성 주장이 자기 `Table S1` 과 모순**(3↔4라운드 19쌍 재측정 median 39 %·max 94 %) | ✅ `papers/cho2025_multicompositional_argyrodite_experimental_active_learning.md` | **exp 닫힌고리 AL** + DFT/AIMD 보조 — 축 **A**(σ) · **J-9**(방법론) |
| **[Jain26Rev]** | `papers/jain2026_ml_pipelines_solid_state_electrolyte_design.md` | Jain/Wang/**You**, *Mater. Horiz.* 13, 15–44 (2026) — SSE ML 파이프라인 **리뷰**(자체 계산 0). ⚠ **전 수치 2차 인용** |
| **[Ahn26CEJ]** 🔴**[우리 원고·미출판]**·자기감사 축 §L | D. Kim/J. Kang/T. Y. Lee(공동1저자 3인)/H. R. Shin/**Yonghoon An** (DFT 담당)/**Jong-Won Lee\*** (한양대 MSE + 배터리공학과 · SK On) 2026 ***Chem. Eng. J.* 투고본 (DOI 없음)** — "**Electrochemical precursor conversion for coupled control of Li nucleation and transport in anode-free all-solid-state batteries**". **AgNO₃–C–PVP 계면층**: PVP 카보닐–Ag⁺ 배위 → AgNO₃ 도메인 **53.4 ± 58.6 → 7.82 ± 2.61 nm**, 첫 충전 in-situ 전환 → **Ag–Li 자리 + Li₃N 계면상**. NCA anode-free 풀셀 **350 cy**(Ag–C 174 단락 · AgNO₃–C 125), 15 wt% 에서 **54.2 vs 35.4 %** (+18.8 %p). 계산 2갈래 = **1D 전기화학–크리프 모델**(`Fig. 3`) + **DFT Li adatom 확산**(`Fig. 5c–e`: Li₃N **0.118** vs LiC₆ **0.290 eV**, ≈59 %↓). ⛔ **물성 4축(A/B/C/D)에 넣지 않는다** — σ·ESW·탄성·밴드갭을 하나도 계산하지 않는다 | ✅ `papers/ahn2026_cej_agno3_pvp_li3n_anodefree.md` | **[우리 원고] 자기감사 전용** — exp 주도 + 연속체모델 + DFT(QE 2점 구속이완 · UMA-oc20 CI-NEB) |
| **[Yu26Pol]** ⚠**우리 계 아님(고분자 전해질)** · 🔧 **방법 반면교사 3건** (보고량 미정의 · MSD 진단 파손 · RDF 배위수 삼자 불일치) | **Dengfeng Yu**/H. Yuan/P. Ding/Y. Li/Q. Wu/H. He/**Yaoyu Ren\***/**Ce-Wen Nan\*** 2026 ***Adv. Energy Mater.* 2026, 0:e71556** (칭화대 新型陶瓷与精细工艺 国家重点实验室 + Ce-Wen Nan Academician Workstation, Qingtao (Wuhai) Energy — **교신저자 이름을 단 사내 워크스테이션**; NSFC 52394170·52394172·52388201·52372085 + 2023YFB2503902; DOI `10.1002/aenm.71556`, 수신 2026-05-08/수락 2026-08-31) — "**Composite Polymer Electrolytes With Hierarchical Confinement of Anions and Solvents for Stable Solid-State Li Metal Batteries**": PVDF+LiFSI(3:2)+DMF 6.2 wt% 에 **3D 다공 N-도핑 few-layer MoS₂ 7.5 wt%**(BET 75.13 m²/g) → σ30 **1.15 mS/cm**·t_Li⁺ **0.68**·2C **1550사이클 90.5 %**. 계산은 보조(CASTEP PBE 정적 7구성 + GROMACS GAFF/IFF 50 ns × 2상자) | `papers/yu2026_pvdf_mos2_anion_solvent_confinement.md` ✅ (2026-09-12) · 크로핑 34장 / **실독 7장 + 패널확대 3 + 수동렌더 1** | **[외부] 실험 주도 + 보조 계산 · ⛔ 물성 4축 A–D 제외(§J-7 방법 원전 블록에만)** |
| **[Meng26LZF]** ⚠**우리 계 아님(고분자 전해질)** · ⚠**Journal Pre-proofs(VoR 아님)** · 🧩 **`[Yu26Pol]` 의 PVDF 짝편** · 🔧 **방법 반면교사 4건** (보고량·참조상태 미선언 · 범함수 인용 어긋남 · XPS 3:2 제약 위반 · 다형 판별력 없는 기전 귀속) | **Wantao Meng**¹/**Yaojiang Yu**¹(동등기여)/J. Fan/Y. Wang/H. Xiao/Y. Sun/L. Li/J. Wei/F. Ye/**Yucheng Wen\***/**Meinan Liu\*** 2026 ***J. Energy Chem.* (in press)** (**광시대학교**(南宁) 자원환경재료학원 — 广西有色金属及特色材料加工重点实验室 외 4개 중점실 + **National Key Lab for Remanufacturing**(北京) + **Sci-Tech University**(杭州) 물리; NSFC **22379160** + 광시 Key R&D **Guike AB25069354** 외 5건; DOI `10.1016/j.jechem.2026.08.079` · PII `S2095-4956(26)00662-5` · Ref `JECHEM 5924`, 수신 2026-06-15/수락 2026-08-15; **데이터 공개 0**) — "**Phase ordering and interfacial stabilization enabling high-performance PVDF-based solid-state lithium metal batteries**": PVDF+LiFSI 에 **단사정 m-Li₂ZrF₆ 2 wt%** → (100) 면 F 배열이 β-PVDF 와 **불일치 0.71/1.09 %** 인 에피택시 템플릿으로 α→β 유도(FTIR **44.8→62.6 %**, GIWAXS **45.2→63.5 %**) ⇒ σ25 **0.29→0.86 mS/cm** · t_Li⁺ **0.25→0.66** · Li‖NCM811 **95.6 %@650cyc/4.3 V**·**93.0 %@300cyc/4.5 V**; 순환 중 **m→t-Li₂ZrF₆ 전환 주장**(🔴 제시된 XPS·TOF-SIMS 증거는 **두 다형을 구분할 수 없다**). 계산은 **흡착에너지 3점이 전부**(`E_ads = E_total−E_sub−E_molecular`; "CASTEP module within the MD framework" · NVT · 1 fs · 333.15 K · "PBE"; **cutoff·k·PP·셀·vdW·수렴·MD길이·시드 전부 미기재**). **`0.22/0.31 eV` 장벽·제조법·t-LZF 기준 BE 는 전부 [56] Xu et al. *Nature* 637, 339 (2025) 소환값** | `papers/meng2026_pvdf_li2zrf6_phase_ordering.md` ✅ (2026-09-15) · 그림은 **SI `.doc` PICF 레코드 32개 ↔ 인라인 `\x01` 32개 1:1 매핑**으로 추출(LibreOffice 가 이 `.DOC` 을 거부 → olefile + piece table) · **실독 10장 / 미판독 14장 / ⛔추출 실패 6장(S6·S7·S10·S12·S15·S16) / 본문 Fig 1–6 전부 미판독** | **[외부] 실험 주도 + 보조 계산 · ⛔ 물성 4축 A–D 제외(§J-7 방법 원전 블록에만)** |
| **[Li26FDI]** ⭐ 황화물/Li 금속 **인공 3성분 계면상** · ★ **`Li₃P = conductor-LEAK` 논쟁의 세 번째 입장**(우리 "전자 누설" ↔ `[Xiao20Rev]` "부동태" ↔ 이 편 "이온수송 불량") · 🔑 저자가 고른 대체재 **Li₃N 이 자기 `Fig. 1g` 최협갭**(figure-read ≈1.1 eV) = 우리 기준 같은 `conductor-LEAK` 칸 | **Xuebao Li**/Chao Zhao/Yueqing Peng/Kun Zeng/Shijie Han/Zekai Zhang/**Zhuangzhi Wu\***/**Dezhi Wang\*\*** (Central South University MSE + State Key Lab of Powder Metallurgy, 단일기관 7인) 2026 ***J. Energy Storage* 181, 124529** (DOI 10.1016/j.est.2026.124529; 수신 2026-06-10 / 수락 2026-08-26 / 온라인 2026-09-10; NSFC 52374407; inbox #115 본문 11 pp · **SI `.docx`** · refs 47 · 그림 6장 · 표 0장) — "**Functionally differentiated composite interphase enables stable sulfide-based all-solid-state lithium metal batteries**" | `papers/li2026_functionally_differentiated_interphase.md` (2026-09-12, 그림 **6/6 실독** · SI 는 `.docx` 라 이미지 없음 → **텍스트 206문단 전수 파싱**) | 실험 주도(SEM/EDS·XPS·AFM·CCD·대칭셀·풀셀) + **얇은 DFT**(VASP/PBE/PAW/520 eV; 계면 슈퍼셀 11 · DOS 7 · CI-NEB 6) · ⛔ **k-메시/셀/진공/vdW/스핀/이미지수/결함기구/무질서 전부 미기재 · 밴드갭 숫자 0 · 계면에너지 γ 정의만 있고 값 없음 · S 2p·P 2p XPS 0 · 순환 후 XPS 0 · σ·EIS·XRD 데이터 0** · 🔴 **초록 수치 오류 1건**(`77.1 over 1000 cycles` → 실제 ≈47) |
| **[Makino26Rev]** ⭐⭐ MLIP 방법론 지도 · ★ **우리 "정적 RMSE → 동역학 환산 금지" 판정의 문헌 근거** | **Keisuke Makino**¹/T. Kato¹/S. Terashima¹/Y. Matsuoka¹/**So Takamoto**²/**Chikashi Shinagawa**²/**Yusuke Asano**³/**Masanobu Nakayama**¹ (¹**나고야공업대 Advanced Ceramics** · ²**Preferred Networks** · ³**Matlantis**) 2026 ***Phys. Chem. Chem. Phys.* Accepted Manuscript** (공개 2026-09-10, CC-BY 4.0, **DOI 미부여** — 정식판 나오면 갱신; inbox #117 본문 번호 62 pp + SI xlsx; refs **216** · 그림 **10** · 표 **2**) — "**Machine-Learned Interatomic Potentials for Battery Materials: From Fundamental Methodology to Emerging Applications in Electrodes, Electrolytes, and Interfaces**". ⚠ **서지 주의 2건**: 파일명 `MACHIN1` 은 구글 알리미 토막 · 표지 1쪽의 *"Volume 19, 2017"* 은 **RSC 범용 커버 템플릿**(둘 다 서지 아님). **자체 DFT 0 · 자체 MLIP 학습 0 · 자체 실험 0 · 물성값 0** ⇒ **물성 4축 금지, `J-7` 전용**. 신규 산출 3개 = **분류 격자**(`Fig. 3`: A1 선형/A2 커널/A3 NN × B1 local-NN/B2 GNN, **우리 UMA = `B2/E(3)-equivariant`** 칸이나 **UMA 는 전문 0회**) · **주관 등급표 2개**(`Table 1`·`Table 2`) · **문헌 census 147편**(`Table S1`). ★★ 핵심 = **§3.5–3.7**: *"안정한 MD 를 보증하는 **균일한 힘-오차 문턱은 없다**"* · *"R²·RMSE = **내삽 정확도**뿐"* · uMLIP 힘 RMSE **0.12–0.17**(TM 없음) vs **0.4–0.5 eV/Å**(일부 TM) ⛔**정의(성분/벡터) 미표기** · *"uMLIP 은 전이상태 학습이 없어 **Ea 를 과소평가**"* · **전자수 고정 ⇒ 분해 개시전위 추출 불가**. 🔴 **`Fig. 9c`**: 같은 MLIP·같은 LLZO 에서 **결함 모델만으로 Ea 0.334→1.227 eV, σ(300 K) 10¹⁰ 배** ⇒ 우리 `absolute_sigma` 금지의 최강 근거. 🔴 **`Fig. 9f`**: `Li₆₋ₓPS₅₋ₓCl₁₊ₓ` × `S/Cl inversion %` 지도, 최대 ≈27 at x 0.4–0.5·inv 70–80 %, **문턱 `figure-read ≈ x 0.58`**(우리 modelc = x 0.6) ⛔**단위 미표기 + 캡션↔그림 방향 불일치 ⇒ 수치 이식 금지**. 🔴 **`Fig. 9a`**: eSNAP 이 α-Li₃N **−3 THz soft mode 를 놓침**(본문은 *"재현 양호"*). 🔴 **`Fig. 9b`**: β-Li₃PS₄ 결정 MSD 가 **1 μs 에 계단 4–5개**(비정질 대비 ≈300배 차) ⇒ 우리 comp1 확산영역 게이트 6/6 탈락의 물리적 설명. ⚠ **벤더 공저**(`Fig. 6a,b` 4칸 전부 PFP; UMA·SevenNet·MACE 정량 0). **본문↔그림↔SI 어긋남 7건**(🔴 `Fig. 7c` 가 `Fig. 7b`·SI(각 135편)와 불일치, **Electrolyte 26편 결손** — 우리 SI 147행 전수집계로 검출 · **없는 패널 `Fig. 5e`·`Fig. 9h` 인용**). ★ **SI `Table S1` 147편 중 우리 보유 4편(2.7 %)** | ✅ `papers/makino2026_mlip_battery_materials_review.md` (2026-09-13, **본문 그림 10/10 전부 실독** + 7패널 900 dpi 2차판독 · 표 2장은 관례대로 PDF 텍스트 복원 · **SI 147행 전수 재집계**) | **[외부] 리뷰 (자체 계산 0 · 자체 실험 0 · 물성값 0) — ⛔ 물성 4축 제외, `J-7 방법 원전` 전용** |
| **[Li26NaRev]** ⛔⛔ **Na 계 — 물성 4축 진입 금지** · ⭐ *"functionally partitioned architecture"* 어휘의 출처 · ★ `Fig. 13e–g` 에 **우리 `Li₆PS₅Cl`** 이 나온다(단 재인용) | **Lin Li**^{a,b}/Wenqian Tian^b/**Siwu Li\***^a/Miao Deng^b/Ziyu Lu^b/**Chuang Yu\***^{a,b} (^a 西安电子科技大 **Xidian University** 信息机电工程学院 · ^b 华中科技大 **HUST** 化学与化工学院) 2026 ***Chem. Sci.* Accepted Manuscript** (온라인 2026-09-08 · CC-BY 4.0 · ⛔ **DOI 미발급** — AM 자리표시자 `10.1039/x0xx00000x` · 본문 36 pp · **refs 147** · Fig 1–13 · Table 1–2 · **SI 없음**) — "**Interfacial Chemistry of Sulfide and Halide Solid Electrolytes in All Solid-State Sodium Batteries: From Single Electrolytes to Functionally Partitioned Architectures**". **⛔ 무대가 나트륨이다** — 전압은 전부 **vs Na⁺/Na**, 캐리어는 Na⁺(1.02 Å vs Li⁺ 0.76 Å). **자체 계산 0·자체 실험 0**(데이터가용성 문구 명시) ⇒ 모든 수치가 **재인용**. **핵심 명제**: 단일 무기 골격이 *"산화저항용 깊은 VBM 과 환원저항용 높은 CBM"* 을 동시에 못 가지므로 → **기능을 공간에 분할**(수송·산화저항·환원보호·**기계수용** 4기능). 근거 3편 = **ref 53 Goodwin 2024 ACS AMI**(같은 양극에 황화물 7–15 mAh/g vs 할라이드 이론용량 근접) · **ref 17 Wu 2021 *Nat. Commun.* 12, 1256**(NYZC0.75 1000+ 사이클) · **ref 51 Deysher 2022 ACS AMI**(염화물 계면상 ≈90 μm vs `Na₃PS₄` ≈10 μm). ★ **`Table 2` 19행 전부가 이미 분할구조**(음극쪽 황화물/NASICON 중간층 + 합금음극, 순수 Na 직접접촉 0건) ⇒ 리뷰의 기여는 발명이 아니라 **명명·원리화**. 🟢 **전이 가능**: 4기능 분해 · **산물 갭→자기부동태 vs MIEC 규칙**(`NaF` 11 / `Na₃P` 0.4 / `Na₃Sb` 0.68 eV ↔ 우리 `LiCl` 6.65 / `Li₂S` 3.90 / `Li₃P` 0.70 `conductor-LEAK`) · **음이온 동결 대조 MD**(`Fig. 6a`) · 중간층 사양(σ_ion>10⁻⁴ · σ_e<10⁻⁸ S/cm) · BVEL=우리 BVSE · DFT+VRH=우리 E_VRH · *"접합은 경계가 아니라 계면상 영역"*. 🔴 **전이 금지**: 모든 σ·Ea·전압창·탄성 GPa·D·산물갭·셀성능 — **특히 `Na₃PS₄` 1.2–2.5 V 를 우리 2.256/1.242 V 옆에**(우연 일치는 면제가 아니라 **부인 선언** 대상)와 **할라이드 15.31–29.57 GPa 를 우리 22.06/27.66 GPa 옆에**(⚠ 후처리가 VRH 로 같아서 제일 위험). ⛔⛔ *"Cl-rich 가 산화한계를 3.8 V 로 올린다"* **절대 금지** — 리뷰의 Cl 은 **골격**, 우리 Cl 은 **S 골격 부분치환**(우리 VBM 은 Cl 증가에도 S 3p, onset 2.256 V 불변). 🔴 **자기 그림이 본문을 부분 반증**: `Fig. 9d` 에서 3족·란타나이드 염화물 환원한계 **≈0.50–0.75 V < `Na₃PS₄` 1.15 V** 인데 리뷰는 족 간 분화를 언급하지 않는다(§10-6). ⚠ **본문↔그림 불일치 4건**(§10): `Y`↔`Yb` 혼동 · `Fig. 4a` 캡션이 2D 화학퍼텐셜 상도를 "stability window" 로 호명 · α-`Na₃PS₄` "impedance 10⁻⁶ Ω cm⁻¹" 단위오류 · ref 53 양극조성 2가지. ★ **후속 필수**: `Fig. 13e–g` 의 원출처 **ref 146 = H. Zhang et al., *Adv. Funct. Mater.* 2025, e10497**(`Li₄ZrCl₄O₂`\|`Li₆PS₅Cl` → `Li₃PO₄`+`Li₂S` 계면상) 을 **별도 digest** 해야 정량 인용 가능 | ✅ `papers/li2026_na_sulfide_halide_interface_review.md` (2026-09-13, 크로핑 **15장 중 7장 실독** — `Fig. 1`·`3`·`4`(+4a 1100 dpi 재렌더)·`6`·`8`·`9`(+9c·9d 재렌더)·`13`; ⛔ 안 본 것 `Fig. 2`·`5`·`7`·`10`·`11`·`12` · `Table 1`·`2` 는 **PDF 좌표 판독으로 전 셀 복원**) | **[외부]** 리뷰 · **Na 계** · 자체 계산 0 · 자체 실험 0 · **⛔ 물성 4축 수치 비교 제외** |
| **[Wang26LRM]** ⛔ **양극(Li-rich Mn) 리뷰 — 물성 4축 진입 금지** · 🔧 **스크리닝 문턱·대조군 설계 원전** · ★ 우리 `Li₆PS₅Cl` 이 실명으로 3회 나온다(단 전부 재인용) | **Xinru Wang**/**Keke Gao**/**Chunwen Sun\*** (中国矿业大学(北京) 化学与环境工程学院; Sun = IOP-CAS 박사 → TUM·NRC → **UT Austin Goodenough 포닥 2010–11** → 中西班牙能源材料联合实验室 소장) 2026 ***Chem. Commun.* Review Article** (DOI `10.1039/d6cc03421g`; 접수 2026-06-01/수리 2026-08-27/게재 2026-09-09; NSFC 52472271 + 2023YFE0115800; inbox #118 본문 **31 pp** · **refs 132** · Fig **1–15** · Table **1–2** · **SI 없음**) — "**Recent progress and perspectives of lithium-rich manganese-based cathodes for high-energy-density solid-state batteries**". **자체 DFT 0 · 자체 실험 0** (데이터가용성 *"No new data were generated or analysed in this study"*) ⇒ **전 수치 재인용**. ⛔ **주인공이 양극 `xLi₂MnO₃·(1−x)LiTMO₂` 다** — 31쪽 중 우리 축에 닿는 것은 **§3.2·§3.3·§4 의 ≈8쪽**뿐. 🟢 **전이 3건**: ① **`Fig. 15b` 깔때기 문턱 4개**(`E_hull=0` / `E_d≤2.8 V & E_c≥4.3 V` / `\|ΔE\|<100 meV/atom` / `E_a<0.5 eV`; 920→68→19→10) = **우리 A–D 4축과 1:1** ② **`Fig. 9c` 대조 양극 설계**(Ga-LLZO 를 LRM·NMC811 **양쪽에** 소결 → LRM 쪽만 `La(Ni,Mn)O₃` **26–30 %**·`Li₂ZrO₃` **10 %**, NMC811 쪽 단일산물 **8–16 %**; LLZO 잔존 **35→22 %** vs **25→26 %**) ③ **`Table 2` 열화 3분류**(기계/화학/전기화학 × 족별 severe–mild) — 우리 축 B 4분할과 **직교**. ★ 우리 계 언급 3건(**전부 재인용·방법 미표기 ⇒ 축 B① 데이터점 아님**): `Li₆PS₅Cl` **≈2.5 V 가역 산화분해 / 폴리설파이드 2.3 V 아래 환원**(ref 42 = **Du 2022 *ACS Energy Lett.* 7, 3006** — **별도 digest 필요**) · `Li₂MnO₃`\|`Li₆PS₅Cl` **3722 Ω**(ref 93, 면적 미정규화) · 산물 **`SO₄²⁻`·`SO₃²⁻`·`P₂Sₓ`**, **>4.4 V 생성·2.0 V 방전 후 잔존**(ref 94, `Fig. 13c` 실독). 🔴🔴 **§4.3 SCL 부호 오류 + 자기 그림과 모순**(본문 *"양극쪽 μ_Li 가 높아 Li⁺ 가 전해질→양극"* ↔ 두 문단 뒤 *"황화물 전해질의 μ_Li 가 높다"* ↔ `Fig. 13e` 는 **전해질쪽 Li 축적**) ⇒ 인용은 원출처 **ref 95 Nomura 2019 Angew.** 로. 🔴 **산화물 창 ">6 V"(§4.2, ref 없음)가 우리 [Xiao20Rev] LLZO `0.09–2.97 V`·[Zhu15] `0.05–2.91 V` 와 정면 충돌** ⇒ `Table 2` 창 4칸(ref 0건) **전부 인용 불가**. ⛔ **함정 2개**: 황화물 영률 **≈20 GPa**(+`Li₃YCl₆` 36.89·`Li₃InCl₆` 18.24, 전부 중문 ref 99 하나·방법 미표기)가 우리 **E_VRH 22.06/27.66** 와 우연 근접 · `Li₂MnO₃` **gap 1.89 eV**(functional 미표기)가 우리 **2.066/2.099** 와 우연 근접 — **둘 다 부인 선언 대상**. ⛔ **"Cl-rich 산화안정" 오용 금지**(리뷰 Cl = 골격 `Li₃InCl₆`, 우리 Cl = S 골격 부분치환 → VBM 여전히 S 3p, onset 2.256 V 불변). ⚠ **불일치 12건**: `Table 1` 이 **ref 66 행에 ref 42 값**(244.5·83 %/1000)을 넣고 ref 42 는 행이 없다 · ref 69 본문 221/0.1C ↔ 표 185.0/0.05C · **ICE 102 %** · **ref 64=82 중복** · **`Fig. 15b` 캡션이 그림과 전혀 다름** · ref 124(**B. Liu**)를 **"Aykol et al."** 로 오기(우리 `aykol2014`·`aykol2016` 보유로 즉시 검출) · ref 43(**C. Y. Chang**)을 **"Chen"** 으로 오기 · **`Fig. 4a` 캡션이 530.5 eV 성분 누락** · **초록 900 ↔ 서론 1000 Wh kg⁻¹** · **`Fig. 15d` 는 ML 아님(FDMNES 정방향)**. ⭐ **본문에 없고 그림에만 있는 값**: `Fig. 7c` LRM 자체 **σ_ion 6×10⁻⁸→6×10⁻⁶ · σ_e 7×10⁻⁷→7×10⁻⁵ S/cm**(각 ≈100배, `C2/m` 38→28 wt%) ⇒ **SE(≈10⁻³)보다 2–5 자릿수 낮다** · `Fig. 7e` **83 cyc 에 O 기여 128→58 · Mn 12→70 mAh/g** · `Fig. 14c` **무코팅 O2 대조군 61.07 %**(본문 미언급) ⇒ 격자 **+48.2 %p**/코팅 **+19.0 %p** · `Fig. 13d` `ClO⁻` 상한 **3.0→50**, `InO⁻` **2.5→60** · `Fig. 5c,d` **경로 B 만 1.21 Å 자유 O₂ 도달, 경로 A 는 1.30 Å `O₂⁻` 정지**(본문은 둘 다 O₂) | ✅ `papers/wang2026_lirich_mn_cathode_solid_state_review.md` (2026-09-13, 크로핑 **17장 중 8장 실독** — `Fig. 4`·`5`·`7`·`9`·`12`·`13`·`14`·`15`; ⛔ 안 본 것 `Fig. 1`·`2`·`3`·`6`·`8`·`10`·`11`; 표 2장은 **PDF 텍스트 전 셀 복원**) | **[외부]** 리뷰 · **양극계** · 자체 계산 0 · 자체 실험 0 · **⛔ 물성 4축 수치 비교 제외, `J-7 방법 원전` 전용** |
| **[Carrete23UQ]** ★ | **Jesús Carrete\***/H. Montes-Campos/R. Wanzenböck/**E. Heid**/**G. K. H. Madsen** 2023 ***J. Chem. Phys.* 158, 204801** (TU Wien + Univ. Santiago de Compostela + Univ. Porto; DOI 10.1063/5.0146905; **OA CC BY**; 데이터·코드 **Zenodo 10.5281/zenodo.7643625**) — "**Deep ensembles vs committees for uncertainty estimation in neural-network force fields**". NNFF(NeuralIL, Behler–Parrinello + spherical Bessel, r_cut 3.5 Å) 위에 **committee / bootstrap / deep ensemble** 3종을 같은 코드로 구현·대결. **결론이 저자에게 불리하다 — 같은 양을 잴 땐 committee 로 충분**(Spearman 0.90 vs 0.91). deep ensemble 의 유일한 승리 = **학습셋 품질 혼합 판별**(그것도 힘 채널). **Appendix = 힘 분산의 미분 불가능성 증명.** ⛔ **재료계 = EAN 이온성 액체 + SrTiO₃** — 우리와 공유 원소 O 하나뿐, **물성값 이전 0건** | ✅ `papers/carrete2023_deep_ensembles_vs_committees.md` | **MLIP 방법론 (계산 100 %) · 참조 DFT = GPAW LCAO/PBE/Γ-only** — **방법 원전 전용, 축 A–I 제외** |
| **[dK18MD]** ★★ | **N. J. J. de Klerk** / E. van der Maas / **M. Wagemaker\*** 2018 ***ACS Appl. Energy Mater.* 1, 3230−3242** (TU Delft; DOI 10.1021/acsaem.8b00457; CC-BY-NC-ND) — "**Analysis of Diffusion in Solid-State Electrolytes through MD Simulations, Improvement of the Li-Ion Conductivity in β-Li₃PS₄ as an Example**". **MD 궤적에서 확산 관련 8종을 뽑는 절차의 원전.** 우리에게 걸리는 축 = **H_R=1 선언 · tracer/jump 확산계수 분리 · 상관인자 f · 집단점프 정량 · 점프별·온도별 Ea(비아레니우스) · D 추정량 정의**. ⚠ **[dK16Arg] 와 다른 논문**(형제편). ⛔ **물질은 β-Li₃PS₄(Pnma) — argyrodite 아님 → 값 이식 전면 금지** | ✅ `papers/deklerk2018_diffusion_analysis_md_beta_li3ps4.md` | **방법 원전 (값은 있으나 다른 상) — 축 A–I 제외, J-7 로** |
| **[Liang26IF]** | **S. Liang**/Z.Xu/M.Sun/Q.Lu/T.Wu/B.Chen/Z.Li/Z.Zhou/L.Lu/**O.Minchukova**/**G.Rymski**/**A.Zhaludkevich**/**Bolong Huang\*** 2026 ***Battery Energy* 5, e70137** (홍콩城市大 화학 + 벨라루스 과학아카데미 재료연; DOI 10.1002/bte2.70137, CC-BY; 접수 2026-06-03/수락 2026-06-18) — "**Overcoming the Interface Bottleneck in Solid-State Batteries: Electrolyte Design, Interface Engineering, and Computational Discovery**", 본문 18 pp·Fig 1–6·Table 0·SI 없음·refs 110. **자체 계산·실험 0 → 전 수치가 소환값(2차 인용).** ⚠ **교신저자가 이 저널 편집장**(자진 공개·편집 배제). ⚠ **결함 8건/18 pp**(무출처 정량 다수 · `Fig. 5b` ↔ 본문 σ 비 1.6× vs 2.7× · `Fig. 4a` 비단조 침묵 · `Fig. 6l` "interfacial energy" 오귀속 · Ω cm³ 단위). **쓰는 곳 = 축 J-12(계면·개관) 하나.** ★ 소득 3: ① **Scholar 스니펫 "aliovalent doping 이 σ 를 낮춘다"는 이 논문에 없는 문장**(LLZO 절 + 황화물 절 + 할라이드 절 3곳 접합) ② **σ-하락 주장은 무출처 논평이고 숫자가 0개** ③ **슬랩·W_ad·strain 배분 규약 전수 0회** ⇒ B2 정의 안 줌 | ✅ `papers/liang2026_interface_bottleneck_solid_state_batteries.md` | **review · 소환값 전용 — ⛔ 물성 4축(A–D) 수치 비교 제외.** 축 정의·관행 확인·gap 문장 재료로만 |
| **[Liu26AB]** ⭐⭐ **"자리(site)를 선언하는 법"의 외부 선례**·cascade 재설계 §15 근거 | **Guangchen Liu**/**S. Yang**/**Yan Zhong\*** (**Worcester Polytechnic Institute**, IMPD Group — docx `Company` + 앱 About; gliu4@wpi.edu / yzhong@wpi.edu) — "**Substitutional Effects at A- and B-Sites in High-Entropy ABO₃ Perovskites: Insights from Machine Learning-Accelerated Simulations and Active Learning**". ⚠ **본문 PDF 미확보 — SI(9 pp·Fig S1–S5·Table S1–S3) + source-data csv(192행) + 코드저장소(`IMPDGroup/HEP-Explorer` @`e1003f2`, MIT, Zenodo 10.5281/zenodo.20075788) 만으로 작성.** 서지(화면 소환: *Sustain. Mater. Technol.* 2026)는 **미확인**이고 저장소 BibTeX 는 `journal={}`·`year={2025}`. **설계**: LaCoO₃ 기준으로 **A자리 = (La,A2..A5)CoO₃ / B자리 = La(Co,B2..B5)O₃** 두 화학식을 못박고 **host(La/Co)를 코드가 런타임 강제**(`app.py:342,356`), 후보집합은 **A{Ca,Sr,Ba,Ce,Pr,Nd,Sm,Gd} ∩ B{Ti,V,Cr,Mn,Fe,Ni,Cu,Zn} = ∅** 로 **자리 모호성을 사전 제거**. **400원자 SQS**(자리당 80) · 15–40 at.%(=12–32원자) · ΔS_conf>1.5R · **192 조성 × 5 SQS = 960 prototype/자리**. 라벨 = **Matlantis(PFP)**, 보고량 **4개 동일**(Ef eV/atom · Δ_lattice % · Δ_atomic Å · D cm²/s, D 는 **−D 로 저장**해 4목표 전부 minimize). 대리 = **Pyro BNN**(13→4, 2층, posterior 1000샘플), HPO = **Optuna 500 trial**(A 225/B 215 완료), 획득 = **EI·HVI·ParEGO·Pareto**, 구조생성 = **icet MC/SA**. 🔴 **convex hull·경쟁상·분해반응 0건 — "별도 상으로 빠지는 경우"를 판정에서 안 걸렀다**(requirements 에 pymatgen 없음, `y_train` 4열). 🔴 **Ef 의 기준상태(reference) 불명** · **자기·스핀 상태 선언 0** · **random arm/enrichment 0건** · Fig. S3 벤치마크는 **정연 17종 총에너지 parity**(동적범위 3 eV/atom)로 **타깃 Ef(산포 0.13/0.23)를 검증한 셈** · 5-fold 가 **행 단위**(1점 = 25행)라 그룹 누수 의심. **[재구성]** 학습셋 = **610점/자리**(초기 **420** = 6조성×70원소조 + **AL 190**), host 최소농도 점이 균등 대비 **3.35×/3.53×** 편중, **D 는 5 SQS 복제본이 610/610 전부 동일**(Ef·Δ 는 610/610 전부 다름) | ✅ `papers/liu2026_ab_site_substitution_high_entropy_perovskite_al.md` | **[EXTERNAL] MLIP(PFP)+BNN 능동학습, 실험 0회 · 산화물 페로브스카이트 — 물성 4축 수치 비교 제외.** 축 **J-9c**(방법론·설계문법) 전용 |
| **[Maginn19MD]** ★★ | **E. J. Maginn\***/**R. A. Messerly\***/D. J. Carlson/D. R. Roe/**J. R. Elliott** 2019 ***Living J. Comp. Mol. Sci.* 1(1), 6324** (Notre Dame + **NIST** + BYU + NIH + Akron; DOI 10.33011/livecoms.1.1.6324; **[Article v1.0], 2019-01-06**; LiveCoMS **living document** — 인용 시 버전 필수) — "**Best Practices for Computing Transport Properties 1. Self-Diffusivity and Viscosity from Equilibrium MD**". **EMD 로 D·η 를 뽑을 때의 체크리스트 원전.** 우리에게 걸리는 축 = **MSD 적합 구간 · 독립 복제 수 · 부트스트랩 CI · 확산영역 게이트 · 유한크기 · thermostat 선택**. ⛔ **고전 force field 기준 · 분자 액체 예제만 · 힘장 오차는 명시적 범위 밖 · 이온전도도는 후속편 예고** | ✅ `papers/maginn2019_best_practices_transport_selfdiffusivity_viscosity.md` | **규약 원전 (물성값 0건) — 방법 원전 전용, 축 A–I 제외** |
| **[Muy25Dop]** | **Sokseiha Muy\***/T. Le Mercier/M. Dufour/M.-D. Braida/A. A. Emery/**Nicola Marzari\*** 2025 ***Chem. Mater.* 37, 2395–2403** (**EPFL THEOS/MARVEL + Syensqo R&I**; DOI 10.1021/acs.chemmater.4c01049, **CC-BY 4.0**, CSCS s1073) — "**Optimizing Ionic Conductivity of Lithium in Li₇PS₆ Argyrodite via Dopant Engineering**". **⭐⭐ 우리 계열 정면**(황화물 argyrodite 도펀트 엔지니어링)이되 **모상이 할로겐 없는 Li₇PS₆** 다. QE-**PBEsol** + **AiiDA-defects** 로 고유결함 6 + 치환 24종 + 공도핑 144조합의 **300 K 평형 결함농도**(자기무결 Fermi 준위·안정영역 centroid μ·112원자 셀·k 2×2×2) → **DeePMD**(9조성 학습) 로 (Mg,Cl)·(Si,Cl) **≈91조성** σ·Ea 지도 → **Mg–Cl 4조성 합성·EIS**. **실험 Ea 0.36–0.38 eV**(⚠ 냉간압축 미소결 펠릿 total). **계산 σ·Ea 는 본문에 숫자가 0개** — 전부 `Fig. 5` 색지도이고 digest 가 컬러바 역변환으로 복원(`figure-read`). ⛔ **MSD 창·궤적길이·시드 수·앙상블·thermostat·dt·셀크기·오차막대가 전부 없다** ⇒ **σ·Ea 절대값 우리 표와 대조 금지**, 쓰는 것은 **방향과 방법**뿐 | ✅ `papers/muy2025_li7ps6_dopant_engineering_conductivity.md` | **DFT 결함열역학 + MLIP-MD(DeePMD) + exp(합성·XRD-FullProf·EIS)** — 값 이식 금지, 방향·방법 원전 |
| **[Ou26MS]** ⭐⭐⭐ | **Y. Ou**\*/L. Scholz\*/S. Keshav/Y. Ikeda/M. Kraft/S. Divinski/**R. Gómez-Bombarelli**/**W. G. Zeier**/**F. Fritzen**\*/**B. Grabowski**\* 2026 ***Nat. Commun.* 17, 8726** (U. Stuttgart + MIT + U. Münster + FZ Jülich; DOI 10.1038/s41467-026-76216-w; **OA CC BY**; 데이터 DaRUS 10.18419/DARUS-5959; 솔버 **LGPL-3.0**) — "**Microstructural insights into fast ion transport in solid electrolytes via multiscale modeling**". **Li₆PS₅X(X=Cl,Br,I) 다결정 Li 수송을 DFT→AIMD→local-AL MTP→MD(5.2만 원자)→FEM 으로 잇는다.** 실험 0. **우리와 재료계가 정확히 같은 유일한 "MLIP 학습 AL + 입계" 편**이고, **σ=Λ(ze)²D/k_BT 의 Λ 를 조성마다 다르게 잡는다**(Cl 2.181×10⁻² ↔ I 1.590×10⁻¹ Li Å⁻³, 7.29×) — 우리 NE(H_R=1) 규약의 외부 앵커이자 반례. **저자 배포 코드·TikZ 소스를 열어 본문과 대조한 결과 정정 10건**(digest §10) | ✅ `papers/ou2026_microstructural_multiscale_fast_ion_transport.md` | **MLIP(MTP)+DFT/AIMD+FEM (계산 100 %)** — 축 **A** · **J-9** · **신설 입계 축** |
| **[Wilson22BAL]** ★ | **N. Wilson**/D. Willhelm/**Xiaoning Qian**/**R. Arróyave\***/**Xiaofeng Qian\*** 2022 ***Comput. Mater. Sci.* 208, 111330** (Texas A&M 단일기관; DOI 10.1016/j.commatsci.2022.111330; **⛔ 비-OA · 코드·데이터 비공개**) — "**Batch active learning for accelerating the development of interatomic potentials**". **풀 기반(pool-based) 배치 능동학습**: 13,006 구조 풀에서 **에너지 불확실도(10-멤버 bagging) + 특징거리**의 가중합으로 **greedy 조건부**로 배치(10개)를 채운다. **⭐ D-optimality/leverage 를 쓰지 않는 model-agnostic 처방** — MTP γ 가 UMA 로 안 넘어가는 문제의 **유일한 우회로 원전**. ⛔ **재료계 = 단층 GeSe**(Li·P·S·Cl 0), **자체 DFT 0회**(라벨은 Yang 2021 DB 재활용), **물성값 이전 0건**, **비용 절감 실측 0건** | ✅ `papers/wilson2022_batch_active_learning_interatomic_potentials.md` | **MLIP 방법론 (계산 100 %) · 참조 DFT = VASP/PBE (남이 돌린 것)** — **방법 원전 전용, 축 A–I 제외** |
| **[Fang22PW]** ★★Haven 외부앵커·⚠조성 반대 | **Hong Fang\*** & **Puru Jena\*** 2022 ***Nat. Commun.* 13, 2078** (Virginia Commonwealth Univ. 물리, 2인) — "Argyrodite-type advanced lithium conductors and transport mechanisms **beyond paddle-wheel effect**", DOI `10.1038/s41467-022-29769-5`. **순수 계산**(CALYPSO PSO + VASP PBE/HSE06 + AIMD + NEB, 실험 0). 계: **Li₆POS₄(SH)** · **Li₆PS₅(BH₄)** · **Li₆.₂₅PS₅.₂₅(BH₄)₀.₇₅** · 기준 **Li₆.₂₅PS₅.₂₅Cl₀.₇₅**. digest `papers/fang2022_argyrodite_transport_beyond_paddlewheel.md` | ✅ `papers/fang2022_argyrodite_transport_beyond_paddlewheel.md` (2026-09-13 병합) | **[외부]** 계산(AIMD) · 자체 실험 0 · ⚠ 3·4열은 병합자 기입 |
| **[Jeon26Con]** | `jeon2026_concerted_li_motion_argyrodite_assi` — **argyrodite 협동 이동 + tracer/charge D 분리** (*JMCA* 2026, DOI 10.1039/d6ta04898f). 계 = **Li₆₊ₓAs₁₋ₓSiₓS₅I (As/Si + I, anion-ordered)** ⇒ 우리 comp1/modelc 와 **양이온·음이온·무질서 상태가 전부 다르다**. **값 이식 금지, 기전·방법만.** Haven 비는 **§J-7 방법 원전** 으로 간다 | ✅ `papers/jeon2026_concerted_li_motion_argyrodite_assi.md` (2026-09-13 병합) | **[외부]** 계산(AIMD/MLIP) · ⚠ 3·4열은 병합자 기입 |
| **[Wu26TMD]** ⛔⛔ **우리 축 아님 — 기각 기록** · 물성 4축 진입 금지 | **Na Wu**/K.Cui/Z.-Y.Wang/Z.-Y.Zou/J.-C.Bai/**D. Legut**(IT4Innovations·VSB)/**H.-Z. Tian\***(北航)/**Z.-J. Cao\***(西安交通大)/**T.-S. Wang\***(西北工业大·HKUST) 2026 ***Tungsten*** in press (DOI `10.1007/s42864-026-00404-w`; refs 113 · 22 pp · SI 없음) — "**Recent progress in intercalation engineering of transition metal dichalcogenides for energy storage and conversion**". **층상 vdW TMD 의 갭에 게스트를 끼워 넣는 전극·전기촉매 리뷰. 자체 계산 0 · 자체 실험 0**(저자 명시). `solid electrolyte`·`argyrodite`·`all-solid`·`NCM`·`hull`·`CoS2`/`NiS2` **전부 0회**, `VASP`/`PBE`/`k-point`/`cut-off` **0회**(DFT 12회 인용하고도 재현 불가) | ✅ `papers/wu2026_tmd_intercalation_engineering_review.md` · **§J-7 기각 기록** | 리뷰(2차) |
| **[Xu26XLS]** 🖥️ **HPC 방법 원전 · ⛔ 우리 기계로 불가 · 물성 4축 진입 금지(값 0건)** | **Qimen Xu\***/**Yu Zhang\***(공동1)/D.Ni/L.Gao/G.Feng/Q.Zheng/J.Liu/H.Lu/Z.Jia/W.Xue/S.Chandran/**T. Hoefler**(ETH Zurich)/**H. Fu**(칭화)/**Y. Lu**(중산) 2026 **arXiv:2609.13115v1 [cs.CE]** (NSCC-SZ; **미査読·DOI 없음**), "Extreme-Scale Linear-Scaling Kohn-Sham DFT at 100 Million Atoms: Bridging Quantum Simulations and Experiments" — **XLSDFT** = 밀도행렬 근시안성 + divide-and-conquer(코어+버퍼) + CheFSI 의 **O(N) 실공간 FD KS-DFT**. Si **1억/2억 원자** · **Li\|LGPS\|Li 계면 11,325,600 원자**(57×44×90 nm) 단일점 SCF + **XPS 깊이프로파일 대조** | `papers/xu2026_xlsdft_linear_scaling_100m_atoms.md` ✅ (2026-09-22) | **HPC/방법 (성능논문)** — 물성값 **0 건**. §J-7 🔧 방법 원전으로만. ⛔ **정확도 검증이 전문에 0 건**이라 "O(N) = 무손실" 근거로 인용 금지 |

---

> 🗺️ **Landscape note [Rupp]** (digest `papers/kim2021_review_oxide_sulfide_se_interfaces.md`): 우리 LPSCl/LPSCl1.6의 좌표계 논문. **oxide(garnet LLZO: σ~1 mS/cm·환원 0.05 V·산화 2.9 V·E 140–160 GPa·취성) vs sulfide(argyrodite Li₆PS₅X: σ~10⁻³·환원 1.7 V·산화 2.0–2.2 V·E~10–37 GPa·연성)** 의 head-to-head + 양극/음극 계면 카탈로그(Table 1·2·3·4, SI Table 1). 우리 숫자(ESW band·환원산물·연성)를 *검증*이 아니라 *문헌 줄에 정렬*하는 용도. **Cl-rich(LPSCl1.5/1.6) 자체는 안 다룸** → 우리 비교는 리뷰 너머의 기여.

> 🗺️ **Landscape note [Bai]** (digest `papers/bai2020_argyrodite_review_progress.md`): **argyrodite *전용* field-map** — [Rupp]가 oxide/sulfide *광역* 지도(좌표계 A)라면 [Bai]는 우리 모재(comp1=Li₆PS₅Cl·modelc=Cl-rich)가 한복판에 놓이는 *argyrodite 6토픽* 지도(좌표계 B). **우리 프로그램을 리뷰 토픽 칸에 정렬**:
> - **§2 결정구조** ↔ 우리 구조 baseline + AIMD inter-cage 율속: 리뷰 "**anion disorder(4a/4d)가 inter-cage jump 장벽↓→superionic**"(교과서 진술) = 우리 Cl-rich disorder D↑·Ea↓ 메커니즘과 정확 일치([Rao11]/[Perc]/[Dyre] 백본과 한 줄). halide trend σ Br≈Cl 10⁻³≫I 10⁻⁷(I 반경 過大)=[Rao11] 일치.
> - **§3 구조튜닝** ↔ **comp1→modelc(Cl-rich) + cascade co-doping**: 리뷰 "Cl/S↑→σ 10 mS/cm"·"Si/Ge·Sb로 lattice·vacancy·disorder 동시조절"·**"single substitution=한측면; double/multiple codoping=종합개선"**(p.25669) = 우리 47-dopant cascade 서사의 *리뷰 차원 정당화*. ⚠ 단 리뷰 치환예시는 전부 *σ↑* 방향; 우리 Nd는 *σ 0.52× 희생하고 passivation 얻는* stability-leaning(목적 방향 다름).
> - **§5 대기안정 codoping** ↔ 우리 O-doping/Nd₂O₃: 리뷰 **HSAB(Sn/Sb soft-acid→S선호) + O codoping(σ유지·대기안정) + "metal+O cooperate"**(p.25666–69, 25678) = 우리 Nd(metal)+O 공도핑의 *처방 틀*. ⚠ **"리뷰가 우리 Nd 검증"이 아니라 "우리 Nd가 리뷰 metal+O codoping 틀의 한 구체 실현"** — 리뷰 관측량=대기 질량/H₂S, 우리 Nd=전자절연 SEI/CEI(grand-pot·전자누출 차단), *관측량 다름*.
> - **§4 계면** ↔ 우리 grand-potential ESW/interface_reactivity: 리뷰 **음극 환원 ~1.7 V·양극 산화 CV>2.2 V/이론 S/S²⁻ 2.24 V·분해 Li₃PS₄+S+LiCl** = 우리 **산화 onset 2.14/2.256 V(S²⁻-limited, 0.1 V 정합)·분해산물 정확일치([Zuo] Eq1·[Banik] 동일)**. ⚠ 리뷰 "1.7 V"=Li/SE 계면 환원전위(ref101)이고 우리 1.24 V=grand-pot 환원한계(≈리뷰 同인용 Schwietert P/P⁵⁺ 1.08)라 *정의 달라 직접 등치 금지*; 리뷰엔 grand-pot *방법 자체* 없음(결과만 ref100/37 인용).
> **🔑 deck용**: "리뷰의 6토픽 중 **구조·구조튜닝(Cl-rich/cascade)·대기 codoping(O/Nd)·계면(grand-pot ESW) 네 칸에 우리 DFT가 atomistic 닻**; 리뷰 outlook이 부른 '**multiple codoping=종합개선·metal+O cooperate**'를 우리 cascade가 *계산적으로 선행 응답*." ⚠⚠ **2020 시점 한계 = 우리 기여 여지**: Cl-rich 4축(intrinsic onset·기계구속·계면·calendar; [Zuo]/[GG]/[Banik]2022·[Wu] 이후)·grand-potential *절차*·foundation MLIP·constrained-ESW·**vacancy paradox(relaxed vs clamped; [Torii] 외부확증)** 전부 리뷰 *너머*. 합성공정(§4)·operando 실패기전(outlook)·셀성능(Table 2·5)은 우리 DFT 밖→그룹 실험([KimICCF]/[KimCA]/[Cha])·그룹 리뷰([Kang])가 채움. Cl-rich 예시=**Cl1.5**(≠modelc 1.6); 절대 σ 비교 금지(UMA 3–5×, Ea·ratio만); 리뷰=문헌 컴파일(자체 계산 0).

> 🗺️ **Landscape note [Fan26]** (digest `papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md`, **⚠미출판 draft ECER-D-26-00097** · 🔁**[분류: Revision]**, 재정독 2026-08-06 — digest §17 로그): **황화물 ASSB '안정성' 축 field-map** — [Rupp]=oxide/sulfide 광역(좌표계 A), [Bai]=argyrodite 전용(좌표계 B), [Kang]=우리 그룹 electrochemo-mechanical(좌표계 C)에 이은 **좌표계 D: 안정성 taxonomy(고유 5축 + 양극 + 음극)**. 저자 그룹 = **[Li25] CuBr₂와 동일(USTB Fan/Tsinghua Nan)**, Fig 24a/b가 우리 [Liu23]/[Li25] digest 그림 → **우리 litdb 계보가 이 리뷰 §5.2.2(SE 개질→in-situ 절연 SEI)의 직계**. **우리 캠페인 6-매핑**:
> - **①산화(축 B①)** ↔ 리뷰 §3.4/4.1.1 "산화 개시 = S²⁻ 우선, 황화물 ~2 V, LGPS 1.71–2.14 V": 우리 grand-potential onset **2.256 V**(S²⁻-limited, comp1=modelc) 정합 + **free-S site-PDOS ⟨3p⟩ −1.1 eV = '어느 S가 먼저 산화되나'의 자리-분해 정량**(리뷰·[Banik]의 S-pin을 free-S(4d) vs PS₄-S까지 내려서 분해) — 리뷰는 이 해상도가 없음 = 우리 기여 여지.
>   - ⭐ **정합 강화 (2026-08-06 Fig 6c 실측)**: 리뷰 **본문**은 LPSCl 자체 산화전위를 글로 주지 않고 "황화물 ~2 V" 로만 뭉갠다. 그런데 **Fig 6c(ref 33 = Zhu/He/Mo grand-potential 상도)의 LPSCl 무반응 평탄부는 `figure-read ≈ 1.7–2.35 V`** 로, 상단이 **우리 2.256 V 와 ±0.1 V 안에서 만난다**. ⇒ "우리 onset 이 문헌 ~2 V 보다 높다"가 아니라 **리뷰가 인용한 바로 그 상도와 같은 값**이다. 인용 규율: **"~2 V" = 본문 요약치 / "≈2.3–2.4 V" = Fig 6c 판독치** 를 구분해 쓸 것.
> - **②공기/결합강화(축 B④·F)** ↔ 리뷰 §3.1 전략①(O 도핑→P–O; Fig 3a ΔE_ad LPSC −1.63→LPSOCF −1.19 eV; ref 83 = **Li₅.₅PS₄.₅Cl₁.₅ O-doping**=modelc 사촌)·"격자 결합에너지 강화"(InF₃ 예): 우리 **LPSOCl gap 2.231 eV(확장)+O 2p 매몰(깨끗한 엣지)**·**B–S 결합이 free-S를 −1.1→−2.15 eV로 안정화** = 같은 전략 칸의 전자구조 관측량 버전. ⚠ 가수분해(H₂O/H₂S 기체)는 우리 0K hull 밖 — "우리가 H₂S 억제 계산" 금지.
> - **③음극 SEI(축 E)** ↔ 리뷰 §5.2.2–5.2.3(할로겐/F/LiI 도핑→in-situ 전자절연 SEI; 이상 SEI 4조건 = 나노두께·저장벽 Li⁺·**전자절연**·기계적응): 우리 `db/properties/anode_interface_b2o3.json`·`b2o3_sei_gaps.json` = **조건③(전자절연)을 산물별 gap으로 정량 서열화** — 리뷰 rubric의 계산 구현. 리뷰 §5.1의 "분해산물 좁은 gap→전자침투→dead Li"(MD ref 178)·**ionization-level 서술자**(ref 180) = 우리 SEI-gap 지표의 형제 — 정식 벤치마크가 유망 후속.
> - **④이온전도(축 A)** ↔ 리뷰 할로겐 도핑 σ↑·플럭스 균질화·고엔트로피 ΔS_conf↔σ(Fig 24c): 우리 **BVSE Li-채널 부피 3.32/4.74/6.73 %(modelc→LPSOCl(+O)→+B₂O₃, iso0.5)**. ~~UMA-MD σ300 b2o3/modelc **동등**(멀티시드 1.08/0.82/1.15)~~ · ~~**B₂O₃ = σ를 깎지 않는(보존) 안정화 도핑**~~ · ~~리뷰 미래방향①("passive→intrinsic stability") 실현 사례로 포지셔닝 가능~~ ⛔ **철회 (2026-09-09 정정 · Codex BH P0-1)** — 아래 상자. (단일시드 1.33× 철회, SEMIFINAL 07-09 은 그대로 유효한 기록이다.) [Yang25] La-O σ 0.65× 는 **문헌 소환값**이라 우리 값과 같은 표에 놓지 않는다.
>
>   > ⛔ **σ 비는 `citable:false` 다** — `db/properties/canonical_registry.json` 의 `MD_sigma_ratio_{600,800,1000}K@b2o3_vs_modelc` (status `source_pending` · `comparison_group: md-sigma-ratio-v1__NON_CITABLE`).
>   > 금지된 것: `statistically_equivalent_transport` · `conductivity_preserved` · `equivalent_sigma` ·
>   > `any_ranking_claim` · `any_mechanism_claim` · `absolute_sigma` · `RT_extrapolation`.
>   > **위 문장 하나가 그중 넷을 동시에 어겼다**(동등·보존·기전/포지셔닝·RT).
>   > ⚠ **온도 오표기도 있었다** — 1.08/0.82/1.15 는 `b2o3_vs_lpscl16_conductivity.csv` 의
>   > **600/800/1000 K** 비이지 **300 K 값이 아니다**. "σ300" 은 틀린 이름이다.
>   > **말할 수 있는 것은 이 한 문장뿐** (레지스트리 `allowed_sentence` 축자):
>   > *"같은 3시드×3온도 집계에서 ΔEa 는 +0.002 eV 였고, 시드조합 산포 ±0.047 eV 가 두 추정치를
>   > **구분하지 못했다**. 고온 원궤적이 보존되지 않아 **비-Li 구조 상태는 평가되지 않았다**."*
>   > 원자료 CSV 가 직접 못박는다 — *"미평가 쌍의 '같음' 은 동등이 아니라 **구분 실패**다."*
>   > 그리고 2026-09-08 셀 회수로 사유가 하나 더 늘었다: 두 계를 **부피 2.00배 다른 셀**
>   > (b2o3 128원자 2436 Å³ vs modelc 62원자 1216 Å³)에서 재고 비를 냈다.
>   > b2o3 UMA-MD 축은 그 뒤 **전체 마감**됐다(`D-2026-09-07-b2o3-md-closure-retrospective`).
> - **⑤기계(축 C)** ↔ 리뷰 §3.5(E 10–30 GPa·K_IC 0.2–0.4 MPa·m¹ᐟ²·>3 µm 파쇄·<1 µm 완화): 우리 E_VRH 22.06/27.66 GPa(relaxed-ion) 범위 내 정합; 단 리뷰엔 relaxed/clamped 구분 없음(우리 vacancy-paradox가 더 세밀)·K_IC/입경은 우리 밖(H-리스트).
> - **⑥열(공백)** ↔ 리뷰 §3.3(고유 400–500 °C vs **계면 200–300 °C O-방출 발열**·P₂Sₓ 치밀층 발열 40–50 %↓·**Th₀/Th′ 조성-결합에너지 서술자** ref 109): **우리 미보유 축** — Th′를 B₂O₃/O 조성에 계산하는 것이 저비용 확장(H-리스트 추가).
>   - 🔥 **문헌 측 방향은 2026-08-06 재정독으로 잡혔다**(우리 계산은 여전히 0): **Fig 5c 발화 시험** — `Li₆PS₅Cl` · `LiSiPSCl` **400 °C 무발화** > `Li₃PS₄` · `Li₇P₃S₁₁` **300–400 °C 발화** > `Li₄SnS₄`(⚠ Li 아래첨자 저해상) **200–300 °C 반응**; **Fig 8a 열폭주 경로 배정** — LPS₃/LPS₇ = 기상 **GSR(200 °C)** vs **LPSCl/LGPS = 고상 SSR(300 °C)**; **Fig 5e Th′ 지도**(값은 [Wang22] 원전 digest 와 자릿수 일치) — 무도핑 기준 **641.75**, **B 660.96(+19) ≫ O 644.88(+3) ≫ Cl 600.34(−41)**. ⇒ 문헌 예측 요지 = **아지로다이트 호스트는 열축 강자 · Cl-rich 는 열축 손해 · B 도핑은 O 보다 6배 이득**. ⚠ 전부 **소환값**(우리 db 절대값과 혼용 금지), Eq 5 에 **Li–Cl 항 부재** 경고도 그대로 승계 → 방향만, 정량 인용 금지.
> **🔑 deck용**: "안정성 리뷰의 taxonomy(고유5축/양극/음극)에서 우리 DFT는 **산화-자리분해(free-S)·결합강화(B–S/P–O)·음극 SEI-gap 정량**, 그리고 **BVSE 채널 부피**(⛔ ~~σ 동시개선(B₂O₃)~~ — σ 비는 인용 불가, 위 상자) 네 칸의 atomistic 앵커; 리뷰가 부른 'passive→intrinsic stability' 전환을 우리 cascade/B₂O₃가 계산으로 선행." ⚠⚠ **규율**: 미출판 draft(수치·그림 변동 가능·인용은 원고번호로)·자체 데이터 0(모든 수치=원전 소환 → 절대값 이식 금지)·유지율 %/CCD 부재(정성)·draft 오타(Intro σ 단위 mS/cm·refs 38=193 중복)·"황화물 CCD 높다"(§2.3) 같은 우호 서술은 §5.1 자체 내용과 긴장 — 걸러 읽기.


> ⭐ **우리 그룹 동반 논문 note [KimICCF]** (digest `papers/kim2026_iccf_molten_salt_sei_lpscl_sheet.md`): **한양대 Kuk Young Cho + Yonsei Yong Min Lee** (우리 LPSCl DFT 계보)의 **실험** 논문. SE = **Li₆PS₅Cl(=우리 comp1)**. 격자 도핑이 아니라 **액체 cavity-filler(ICCF=IL [EMIM][TFSI]+LiTFSI+FEC)** 로 **(1) σ 회복(시트 1.44→2.23 mS/cm, 155 %, 펠릿 70 %)** + **(2) 음극 in-situ LiF-rich SEI**(XPS F1s 684 eV, Li₂S 억제) 달성. **🔑 두 개의 평행:** (a) **σ 손실 원인 = 공동(미세구조 34.2 %), bulk 결정 아님** → 우리 "σ_e/σ는 interphase·microstructure 레버, bulk 아님" 결론과 **양 날개**. (b) **LiF-rich SEI가 SE 분해 억제 = 우리 'electron-blocking(전자절연) interphase'(Li₂O/Li₃PO₄/NdPO₄/LiCl) 메커니즘의 실험 카운터파트** (LiF·LiCl·Li₂O 모두 wide-gap 절연 패밀리). DFT는 분자 HOMO/LUMO(B3LYP/6-311++G)+GeoDict digital-twin뿐 → **bulk 결정 DFT 수치 직접 대조는 부적절, 개념(목표·레버) 정렬 용도.** ⚠ Cl 1.0(comp1)만; modelc(Cl 1.6) 없음.

> ⭐ **우리 그룹 동반 논문 note [KimCA]** (digest `papers/kim2025_conductive_agent_se_coating_cathode.md`): **Yonsei Yong Min Lee + DGIST** (우리 LPSCl DFT 계보)의 또 다른 **순수 실험·전극공정** 논문. SE = **Li₆PS₅Cl(=우리 comp1**, POSCO JK, D50 1 µm), 양극 = LiNbO₃-NCM711. **격자 도핑이 아니라 양극 복합체 측** — SE를 CAM에 코팅할 때 **도전재(CA) 차원**이 코팅 형상·전자전도 경로를 지배함을 보임: **SE@CAM(CA無, dense, σ_e 3.3×10⁻² S/cm·185.3 mAh/g·CE 81.6 %)** vs **SE-SP@CAM(0D Super P, Super-P-rich, σ_e 1.0×10⁻⁵=3,000배↓·활성표면적 1.00→0.51·151.6 mAh/g)** vs **SE-VGCF@CAM(1D VGCF-embedded porous, σ_e 1.4×10⁻²=SE@CAM 수준 회복·183.5 mAh/g·CE 82.7 %·200 cyc 76.8 %)**. **🔑 핵심**: ASSB 성능 레버 = **코팅층 형상 + 전자전도 경로(CA 차원·mixing protocol)**, bulk 결정 아님 → 우리 "lever = interphase/microstructure, not bulk lattice" 결론의 **양극(cathode) 측 실험 보강**. ⚠ **계산 전혀 없음 → DFT 수치 직접 비교 절대 금지**; σ_e/σ_i 절대값도 device(복합양극) σ라 우리 bulk와 대상 다름. 비교는 **동일 SE(comp1) + 개념(레버=미세구조) + 같은 그룹 동반** 수준만. modelc(Cl 1.6) 없음.

> ⭐ **우리 그룹 리뷰 note [Kang]** (digest `papers/kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review.md`): **우리 연구실(한양대 Jong-Won Lee)이 직접 쓴 ChemComm Feature Article 리뷰** — 즉 *우리 DFT의 상위 세계관* 문서. **thesis: 황화물 ASSB의 진짜 병목은 "산화/환원 분해(전기화학)" 하나도 "균열/접촉손실(기계)" 하나도 아니라, 둘이 서로를 유발·가속하는 *양방향 되먹임 고리*(reaction→fragility→fracture→fresh-surface→re-reaction)** 이고, 따라서 "**chemical passivation *or* mechanical reinforcement가 아니라 *both simultaneously*** "가 필요. **진짜 적 = decomposition/stress 자체가 아니라 그들의 *heterogeneity*(공간 불균일).** 구조: §2 전기화학분해(양극4종=산화/CAM계면/CA-TPB/대기 + 음극3종=환원/dendrite, Nolan **Type1/2/3** 계면) → §3 기계분해(공동·접촉손실·CAM균열·Li100%·응력-dendrite) → **§4 coupling(되먹임)** → §5 **3대 완화(① SE도핑 ② CAM코팅 ③ 음극공학)** → §6 통합 chemo-mechanical 로드맵. **🔑 우리 DFT 매핑**: (a) **§5.1(b) O²⁻ 옥시설파이드(Li₆PS₄OCl, 전자누출↓·ECW확대·O–P>S–P) + §5.1(c) Li₃PO₄ buffer = 우리 Nd2O3/O-doping cascade의 리뷰 내 정당화** (우리 sei_products.json: O-derived Li₃PO₄ 5.73·Li₂O 5.24·NdPO₄ 5.55 eV가 conductive Li₃P 0.70 대체 = "reduced electron leakage"의 정량판). (b) **Nolan Type1/2/3(Fig5c) = 우리 SEI 전자절연 분류의 표준 프레임** (insulator≥4/conductor<2 eV 임계 = Type 정량판; Type3로 밀자 = cascade 목표). (c) **Fig1a ECW(ref49 Zhu/He/Mo)=우리 grand-potential 동일방법** (comp1 2.256 V 정렬); **Fig1b thermo vs kinetic ECW** = 우리 onset(thermo) vs 실험창(kinetic) 차이 그림. (d) **§6 트렌드3 "modifying one parameter alters others" = 우리 cascade의 stability↔Li-mobility blocking trade-off** 와 정확히 일치. ⚠ **정직한 한계**: 리뷰의 *핵심*(coupling 되먹임·heterogeneity)은 **우리 정적 bulk DFT 밖** — 우리는 고리의 *끝점*(분해화학 + bulk elastic)만 닻을 내림; 동역학은 그룹 phase-field(ref39=Kim/Park/Lee)·stack-pressure(ref120=Kang)·operando가 잇는다. 리뷰는 argyrodite를 **Li₆PS₅X 일반**으로만 다뤄 **Cl-rich(modelc) vs comp1 비교 없음**(=우리 기여 여지). 전부 2차 인용(자체 데이터無). self-cite 밀도 높음(refs 31·39·40·56·67·68·69·70·73·120) = 우리 그룹 강점이 곧 리뷰 강조점.

> ⭐ **우리 그룹 동반 논문 note [Cha]** (digest `papers/cha2024_dualcompatible_halide_ncm_lpscl_interface.md`): **한양대 Jong-Won Lee 그룹(+DGIST·KETI)의 cathode-interface 라인 *기원(2024)*** — Junhee Kang이 [Cha]·[Kang25]·[Kang] 세 논문 모두 참여(즉 [Cha]2024 → [Kang25]2025 → [Kang]2026 **3부작의 첫 편**). SE = **Li₆PS₅Cl(=우리 comp1)**, 양극 = single-crystalline LiNi₀.₈₃Co₀.₁₁Mn₀.₀₆O₂. **격자 도핑도(우리 cascade), SE-코팅도([Kang25]) 아니라 — *별도 할라이드 SE*(LIC/LYC/LZC)를 NCM 입자에 8–10 nm conformal 코팅**해 NCM-LPSCl 직접접촉을 차단. **🔑 핵심 발견 = "dual compatibility"**: 양극 복합체서 할라이드 코팅은 **NCM·LPSCl 두 상과 동시 접촉** → *양쪽 모두*와 호환돼야 함. **LIC(In→In₂S₃ 환원, 양쪽 분해) / LYC(Y→Y₂S₃, LPSCl과 분해) / LZC(Zr⁴⁺ 양쪽 무분해, 7일·100cyc 안정)** → **Li₂ZrCl₆만 dual compatible** → 계면저항 74.4→**20.1 Ω·cm²**(1/3.7)·100cyc **91.2 %**. **두 개의 정밀 정렬:** (a) **σ≠성능** — σ는 LIC(1.12)>LZC(0.51)>LYC(0.37)인데 성능은 LZC>LYC>**LIC(꼴찌, bare보다도 나쁨 80.8<83.1)**; 논문 명시 "interfacial resistance ... cannot be explained in terms of ionic conductivity" → **우리 'lever=interphase/microstructure, not bulk σ' 결론의 cathode-side 세 번째 실험증거**([KimICCF]sheet σ·[KimCA]양극 σ_e에 이어). (b) **dual-compatibility = 우리 `GrandPotentialInterfacialReactivity`(voltage-resolved) 도구의 *완벽한 적용 대상*** — LIC/LYC/LZC×{NCM,LPSCl} 6계면 호환성을 우리 도구가 in-silico 재현·예측 가능(왜 Zr⁴⁺만 견디나). ⚠ **정직한 한계**: (1) **계산 0** → DFT 수치 직접 비교 금지; (2) **Zr가 우리 Cl-Li-Nd-O-P-S hull에 없음** → LZC dual compatibility를 우리 grand-potential로 *아직* 정량 못 함(향후 Zr hull); (3) 호환 기전(Zr⁴⁺ passivation·In 환원)은 **정성적 환원전위 trend**이고 논문 스스로 "yet speculative"; (4) modelc(Cl-rich) 없음(comp1만). **이로움이 우리 Nd passivation과 같은 'wide-gap 절연 CEI'냐?** — *부분만*: LZC가 *새 저항층을 안 만든다*(compatibility)는 우리 "interphase가 부반응 차단" 프레임과 결이 같으나, 우리 Nd는 *능동적 절연 CEI 형성*, Cha는 *비반응성 코팅(no new interphase)* → **메커니즘 위치가 다름**(코팅 차단 vs 도핑 산물). "Cha=Nd passivation 실험증거"라고 하면 부정확.

> 🗺️ **Landscape note — 우리 그룹 cathode-interface 3부작 [Cha]2024 → [Kang25]2025 → [Kang]2026**: **세 논문 모두 Jong-Won Lee 교신 + Junhee Kang 참여 + SE=comp1(Li₆PS₅Cl)**, 고-Ni NCM–LPSCl **양극 계면**을 *서로 다른 레버*로 공략한다 — **[Cha]2024 = 양극활물질에 *별도 할라이드 SE* 나노코팅(LZC dual-compat)** / **[Kang25]2025 = 양극활물질에 *LPSCl 자체* conformal 코팅(기생반응 균일화·SOC강하)** / **[Kang]2026 = 그 위의 electrochemo-mechanical 통합 리뷰(coupling 지붕)**. **🔑 공통 결론 = "고전압 NCM-LPSCl 계면은 *어떻게 관리/차단하느냐*가 수명을 좌우"** (분해를 없애기보단 균일화·비반응 코팅·통합설계). **우리 DFT의 위치**: 세 편 다 *device/계면 화학*만 다루고 **atomistic 분해화학·전자구조는 우리 grand-potential·interface_reactivity가 채움** — 특히 [Cha]의 dual-compatibility(6계면)는 우리 voltage-resolved 도구로 *직접 in-silico 재현 가능*한 가장 깨끗한 적용 대상. → deck "우리 연구의 위치": **그룹 cathode-interface 3부작(코팅·기생·리뷰) 아래 우리 DFT(어떤 산물·왜 호환/비호환을 grand-potential로 정량)**.

> 🗺️ **Landscape note — 우리 그룹 4중 구도 [Kang]리뷰 × [KimICCF] × [KimCA] × 우리 DFT**: **[Kang] 리뷰가 *지붕*(세계관·로드맵)**, 나머지 셋이 *기둥* — (a) **우리 DFT(comp1/modelc/Nd/ESW/elastic/cascade) = 리뷰 §5.1(SE도핑) + coupling 고리의 전기화학·기계 *끝점* atomistic 닻**, (b) **[KimICCF](sheet σ회복·음극 in-situ LiF SEI) = 리뷰 §5.3(음극공학)·§3(미세구조 공동)의 실험**, (c) **[KimCA](양극 CA 차원·TPB) = 리뷰 §2.1.3(CA-derived 분해)·§5.2(CAM코팅·LNO-NCM)의 실험**(ref69가 곧 [KimCA]). **🔑 공통 결론**: 리뷰가 "electrochemo-mechanical을 *통합·균질성 중심*으로 설계하라 + multi-scale 계산×operando로 받쳐라"고 부르고, 우리 DFT가 그 multi-scale의 *atomistic 기둥*. → deck "우리 연구의 위치" 최종 슬라이드: **[Kang] coupling 고리(Fig16) 위에 우리 DFT(분해화학+elastic+O-doping interphase) + 두 동반실험(sheet/anode + cathode/TPB)을 얹으면 = 우리 그룹의 통합 chemo-mechanical 프로그램 한 장**.

> 🗺️ **Landscape note — 같은 그룹 3각 구도 [KimICCF] × [KimCA] × 우리 DFT**: 한 그룹(Yonsei Y.M.Lee + 한양대 Cho + DGIST) 안에서 ASSB의 전 영역이 **분업·수렴**한다 — **(a) bulk 격자·산화창·Li 이동도·환원산물 = 우리 DFT(comp1/modelc/Nd)**, **(b) 시트 σ 회복(공동 채움) + 음극 in-situ LiF-rich SEI = [KimICCF]**(sheet/anode-side), **(c) 양극 복합체 전자전도·코팅 형상(CA 차원) = [KimCA]**(cathode-side). 세 논문 모두 SE = **Li₆PS₅Cl(=comp1)**. **🔑 공통 결론**: ASSB의 실현 성능을 좌우하는 레버는 **bulk 결정이 아니라 미세구조·계면·전자전도**다 — [KimICCF]는 "σ 손실=공동(미세구조)·SEI=계면화학", [KimCA]는 "양극 성능=코팅형상·전자경로(CA 차원)", 우리 DFT는 "bulk는 wide-gap·S-limited onset·Cl이 σ↑/onset 불변 → 차별화 여지가 interphase에 있음". → deck "우리 연구의 위치" 슬라이드: **우리 DFT(bulk) + 두 동반 실험(cathode·sheet/anode) = '레버는 interphase/microstructure'에 양·음극 양면으로 수렴**. ⚠ 두 실험 논문 모두 **modelc(Cl-rich) 없음**(comp1만), [KimCA]는 **계산 0**(개념 비교만).

> 📐 **Methods-provenance note [He19]** (digest `papers/he2019_dft_for_battery_materials_review.md`): **우리 정적 DFT 파이프라인 *전부*가 표준 DFT-for-batteries 관행을 따른다는 단일 인용처** (He et al., EEM 2019 — 외부·Wuhan, *argyrodite 아님·재료수치無 → 물성 4축에 절대 넣지 않음, 수치 대조 금지*). 리뷰가 5축으로 종설한 방법이 우리 도구와 절별 1:1 대응한다:
> - **전자구조(§4.2–4.4)** ↔ 우리 `electronic.json`: 우리 PBE gap(comp1 **2.066**/modelc **2.099 eV**)·DOS/PDOS(VBM=S 3p 91–93 %, HAXPES 일치)·Bader(Li +0.877/P +4.686/S −1.807/Cl −0.914)·ELF(P–S 0.946 vs Li 0.07)·CDD = 리뷰 §4 표준 용법. **🔑 caveat 정당화**: 리뷰가 "**PBE는 gap을 ~1 eV 과소, HSE가 보정**"(Fig 8, Mg₃N₂ 0.91→1.92)을 명시 → 우리 "절대 gap 비교 금지·wide-gap만"이 변명이 아니라 **표준 인지**. Nd엔 **DFT+U(4f, U=8)** = 리뷰 "localized d/f엔 +U"; 우리 "4f-U 민감, trend robust"가 리뷰 "U는 semi-empirical"과 일치. **단 우리 hull은 GGA+U(SCAN 아님)** — 리뷰 1순위(SCAN)를 *미채택*(MP 정합·R²SCAN noise 회피 trade-off, 정직히 명시).
> - **전압/ESW(§3, Fig 7)** ↔ 우리 `oxidation_stability.json`: 리뷰의 **Nernst V=−Δ_rG/nF + convex-hull(Ceder 평균전압)**이 우리 OCV 1.72·환원 1.24·산화 onset 2.14(LiS4 제외 2.256) V의 *열역학 근간*. **🔑🔑 그러나 우리가 리뷰보다 *더 엄밀***: 리뷰는 SE 안정창을 **Goodenough HOMO/LUMO band-edge(Fig 7)** 로만 본다 — 우리는 **grand-potential 분해창(Mo2012)** 을 씀(band-edge는 분해창 2–3× 과대, Schwietert 2020; 우리 직접 증거 = comp1/modelc VBM +0.32 eV 다른데 onset 동일). → **"He19가 우리 grand-potential을 정당화한다"는 부정확**(리뷰엔 grand-potential 없음); 리뷰는 *average-voltage 근간*만, *절차*는 Mo2012(`oxidation_stability_VBM_vs_grandpotential_report` §7·11). 우리 황화물은 **TM-free라 U-모호성에서 자유**(리뷰 §7 "U는 TM-d 전용·산화물 formation엔 GGA가 나음"의 난맥 회피).
> - **이온수송(§5)** ↔ 우리 `li_transport.json`: 리뷰의 **AIMD-MSD→D, Arrhenius→Ea, NE→σ**(NEB는 단경로만, "AIMD가 D·σ까지 준다")가 우리 노선 그대로. comp1 **Ea=0.2532 eV**(⚠ 실험 LPSCl Ea 는 방법·시료마다 갈린다(EIS total 0.29–0.46 eV) — **Schlem 2020 귀속은 2026-07-28 철회**(그 DOI 는 Li₃MCl₆ 할라이드, LPSCl 값 없음) — '±0.003 eV 일치' 화법 사용 금지)·modelc 0.2235·D(600K) 3.09→7.90e-6. **🔑 caveat**: 우리는 AIMD를 **foundation MLIP(UMA-s-1p1)** surrogate로 — 리뷰엔 없는 영역(2019 이전). UMA가 **σ 3–5× 과대** → **절대 σ 금지, Ea·ratio만**; Nd는 4f 전이성 미검증(ratio만). 즉 리뷰의 "AIMD 정확도 기대"가 **우리 MLIP이 넘어야 할 바**.
> - **기계(§2 vdW경고)** ↔ 우리 `eos.json`/`elastic.json`: EOS B0 comp1 26.23/modelc 21.71 GPa·**relaxed-ion E_VRH 22.06→27.66** vs clamped 52.31(**vacancy paradox**). 리뷰의 "**vdW 필수·ion-relax 중요**"가 우리 PBE(22.06) vs 문헌 D3(27.4) 차이·relaxed vs clamped 2.4× 차이를 설명하는 표준 근거.
> - **phonon(§2.4)**: 우리 **미실시**(elastic eigenvalue 양수=기계안정만; 동역학 phonon 안정성 미판정) — 리뷰도 "비용 커 일부만"이라 *비표준 아님*(→ §H 후보).
> - **MLIP 교차검증**: 우리 UMA가 EOS선 DFT급(**Nd₂O₃ B0 UMA 18.9 ≈ cascade DFT 19.9**, ≈1 GPa)이나 **절대 σ는 3–5× 과대** → "에너지·EOS·Ea는 DFT 기준 통과, 절대 수송계수는 미달"이 우리 MLIP 운용규칙(리뷰의 DFT 정확도 기준에 비춤).
> **→ deck/paper 용법**: Methods 섹션에서 gap(PBE)·DOS·OCV(hull)·AIMD Ea/D·elastic 각각에 He19를 표준 근거로 인용; "우리 방법은 표준 DFT-for-batteries 관행을 따르되, SE 산화창은 리뷰의 band-edge가 아니라 *더 엄밀한* grand-potential(Mo2012)을 쓴다"가 정확한 1-liner. ⚠ **2019 리뷰 = r²SCAN·foundation MLIP·grand-potential 계면도구 누락** → 우리 신·심화 도구(UMA·constrained-ESW·interface_reactivity)의 표준성은 *후속 문헌*으로 별도.

> 🧪 **screening 레퍼런스 note — *코팅 ≠ 도핑, cascade ranking 비교 금지* (NOT comparable to our 47-dopant cascade)** [`papers/sundar2025_oxide_coating_screening_lpscl.md`]: **Sundar 2025 = LPSCl 입자에 *바이너리 산화물 ALD 코팅*을 DFT로 스크린**(외부 Argonne). 우리 cascade는 *격자 치환*(Nd/Mg/O/F), Sundar는 *표면 코팅 산화물 상* → **레버가 다르다. 도판트 랭킹·descriptor(stability↔mobility trade-off·BVSE bottleneck)와 1:1 대조 금지.** **연결은 정확히 두 곳뿐**: (a) **방법론 거울** — Sundar의 계면 분해 스크린 = **pymatgen `InterfaceReactions`** = 우리 `interface_reactivity`/`GrandPotentialInterfacialReactivity`와 *동일 알고리즘*(우리는 grand-potential 전압분해까지 확장 = 우리 우위). 외부 Argonne 그룹이 같은 도구를 쓴다 = 우리 계면 방법이 **분야 표준**. (b) **분해산물-전도도 철학** — Sundar 핵심 design rule "코팅 자체 안정성 < *계면 분해산물의 σ_ion/σ_e*" = 우리 "도판트 자체 < *분해산물/SEI*의 전자절연성(NdPO₄/Li₃PO₄/Li₂O wide-gap)"과 **같은 사고**. 그리고 Sundar HSE06 분해산물 gap(Li₂S<LiCl, LiAlS₂/MgS 큼)이 우리 sei_products.json(LiCl 6.65≫Li₂S 3.90)·[Li25](LiCl 6.13/Li₂S 3.04)·[Lu](LiCl 6.22) 순서를 **재확인**(축 D·G). **ZnO 역설**(bulk gap 3.4 eV → 1 nm slab 0.4 eV → 코팅 후 σ_e *오히려↓* ZnS 산물 때문) = 우리 "PBE gap은 과소·slab/disorder 민감 → 'wide-gap insulator'로만 쓴다" 규율의 외부 근거. ⚠ **MgO/Al₂O₃/ZrO₂/ZnO·LiAlS₂/MgS는 우리 6원소(Cl-Li-Nd-O-P-S) hull 밖** → 그 절대 ΔE/gap은 우리 hull로 재현 못 함, 정성 정렬만. **DFT+U 미명시·HSE mix 0.32(비표준)·무질서 처리 미명시** → §10 한계.

> 🔌 **전도성 바인더 note [Jun26] — *SDCP 프로그램의 문헌 좌표* (argyrodite 4축 수치비교 대상 아님)** [`papers/jun2026_ppma_econductive_binder_si_lowpressure_assb.md`]: **Jun/정윤석 2026 Nat. Commun. = PEDOT:P(SSₓ-co-MA_y)(PPMA) e⁻-전도성 바인더로 저압(5 MPa) Si-ASSB 실현** — 물성 4축(A–D) 표 *어느 행에도 수치로 넣지 않는다*(폴리머 바인더·음극 셀 논문, **계산 0**). 유일한 argyrodite 접점 = 상용 LPSCl(=comp1 조성, POSCO JK) **σ 4.2 mS/cm@30 °C** as-received anchor(우리 AIMD RT 외삽 ~3.35와 같은 10⁻³ 차수) + "electronically insulating SE" 사용(우리 wide-gap 프레임과 정성 일치, 절대 gap 비교 금지). **본론은 SDCP(자가도핑 PEDOT-계, `kb/projects/sdcp_master_v2_2026_07_11.md`) 대비 4-평행**: **(1) 설계 사다리** — 그들 = PEDOT:PSS **2상 유지** + 폴리음이온(PSS)에 MA 공중합(접착 추가); 우리 = 술폰산을 **티오펜 side chain에 공유결합(자가도핑)** → 별도 PSS 절연상 제거. 그들의 **PP/PMA 물리블렌드 대조군(상분리→급락, Supp 31)** = "물리혼합 < 공중합 < 자가도핑" 사다리 논증의 실험 근거. **(2) "전도 유지" 증거의 상보성** — 그들 = 구조(GIWAXS π-π 3.55 Å 동일·benzoid Raman·CV 후 S 2p 불변, 실험); 우리 = 전자구조(**Loewdin 백본 폴라론 지분 n=1 35%→n=2 33%(양 링 균등)→n=3 50.1%**, interior 선호 71 meV, H-제거 비용 n↑ 감소 — 계산). **(3) 전도-기능 트레이드오프의 sufficiency 논증** — 그들 필름 σ 10.6→5.8 S/cm 희생 후 "sufficient"(Si 10⁻⁶ 대비 ≫) 방어 = 우리 폴라론 지분 35–50% 방어 프레임으로 재사용. **(4) 산성기 표면 앵커링 + H→Li 교환** — 그들 -COOH↔Si-OH(실라놀) + 첫사이클 **-COOLi**(Li 1s XPS, 비가역) = 우리 **-SO₃ NCM 앵커링**(E_bind doped **−1.52 eV** QE Phase-B preview·neutral 대기; UMA 클린슬랩 −5.196 eV S–O 공유앵커)·**H↔Li 교환(operando SO₃Li)** 논거의 게재 전례. **⚠ 전이 금지 규율**: 음극(Si·0.01–1 V) vs 우리 양극(NCM·산화측) — 그들 "ASSB가 PEDOT:PSS를 안정화" 논거는 **환경(고체계면 국한) 기반**이라 우리 산화측·분자(자가도핑) 기반 주장에 자동 이전 불가; 90:10 vs 97:3 조성 교란·70 MPa 역전(PVDF 142>131)=**저압 전용 이점**; SE셀 CV "안정"엔 LPSCl 자체 환원(우리 grand-pot 환원한계 1.242 V 영역) 기여 미분리(우리 추론). **서론 4문단 스켈레톤**(P1 소재약속+실패물리 → P2 개념+깃발결과(숨은 조건) → P3 열화모드 열거→요구사양 → P4 Herein 기능배분 1문장+반직관 주장+정량+헤드라인) = 우리 SDCP 논문 서론 템플릿(digest §3·§14). **계산 0 = 우리 fragment 벤치마크(PTFE C₄H₂F₈/C₁₀F₂₂)·폴라론 해부의 신규성 공간.**
> 🧲 **바인더 흡착 *전하상태* note [Han25] ↔ [Kang25] — *SDCP `E_ads` estimand 의 문헌 대조군 2편* (둘 다 argyrodite 물성 4축 표에 넣지 않는다)** [`papers/han2025_icep_binder_ultrahigh_loading_ncm811.md`] · 전문 종합 = `kb/syntheses/binder_adsorption_charge_state_2026_08_29.md`: **같은 문제 — "음이온성 바인더기(−SO₃⁻ / −COO⁻)를 산화물 슬랩 위에서 어떻게 중성으로 다루나" — 를 두 논문이 서로 다른 방식으로 풀었다.** **(A) [Han25] ICEP = H 를 슬랩으로 옮긴다.** CASTEP DFT(전하 지정 가능)로 `ICEP_AMPS`(술폰산 온전, −1.819 eV)와 `ICEP_AMPS (−H)`(**양성자가 표면 O 로 이동**, −2.243 eV)를 나란히 계산. SI `Figure S13` 캡션이 *"hydrogen transfer"* 라고 못박아 **조성 보존·총전하 0** 확정. **(B) [Kang25] [`papers/kang2025_bollard_anchored_binder_dry_electrode.md`] (Adv. Mater. 2025, 37, 2416872, PAA-CMC 그래프트 PC + PTFE, NMC622 건식전극) = Na⁺ 짝이온을 넣는다.** ⚠ 🔴 **Kang 은 DFT 가 아니다** — SI p.7–8 *"deep-learning based DFT … **preferred potential (PFP) v3.0.0** as a universal NNP … **Matlantis**"* (Gaussian16 B3LYP 는 FTIR 진동수 배정 전용). 슬랩 NMC622 *R-3m* fully-lithiated 2×2×1, 진공 40 Å, 하반부 고정, ASE L-BFGS `fmax 0.01`, `E_ads = E_slab-binder − (E_slab + E_binder)`, MD NVT Langevin 400 K/10 ps/1 fs/friction 0.01, **회전 15 배열**. 값: **PC_2Na −2.24 / PC_1Na −1.12 / PC_0Na −0.37 / PTFE_dimer −0.09 eV**. **🔑 갈리는 지점은 '중성 유지' 가 아니라 '그 상태를 이름 붙여 선언했는가' 다** — Kang 은 상태 이름에 Na 개수를 박고 세 값을 본문에서 비교했고, ICEP 는 `(−H)` 를 **본문에서 한 번도 언급하지 않는다**(그림 라벨·캡션뿐, −2.243 eV 도 본문 부재). ⚠ 단 Kang 의 우위는 **"사후 명명" 까지** — SI `Fig S15` 배열 수 **8+3+4=15** 가 회전 수와 정확히 같아 라벨이 **이완 후 서술**임이 확정(사전 설계면 5/5/5). **🔴🔴 우리 SDCP 에 그대로 걸리는 함정 (Kang 쪽)**: 15 배열 전부 Na 가 2개이고 `1Na/0Na` 는 **표면 접촉 Na 수**다(본문 *"the **free Na site**"* 가 확정). 결합 모티프는 `–COO⁻ ··· Na⁺ ··· O²⁻` **양이온 브리지**이고 **유기 음이온기는 산화물에 직접 닿지 않는다** ⇒ −2.24 eV 는 "COO⁻ 결합" 이 아니라 **"Na⁺ 2개 결합"** 이다. ⇒ **"음이온기를 짝이온으로 중화하면 된다" 는 공짜가 아니다 — 짝이온을 넣는 순간 그것이 결합 자리가 되고 estimand 가 조용히 바뀐다.** 우리가 −SO₃⁻ 를 Li⁺ 로 중화하면 재는 것이 술포네이트 결합이 아니라 **Li⁺ 브리지**일 수 있다. 이것이 `db/properties/sdcp_doped_closed_2026_08_28.json` 재개조건 ①(**짝이온 확정**)이 왜 필요한지의 **실물 근거**다. **🔴 [Han25] 쪽 하자 = 자기상태 정책 부재**: `spin-polarized` + `U(Ni 6.0 eV)` 인데 H 이동으로 **TM 하나가 환원**된다. 그런데 FM/AFM 배열도, 환원 TM 의 스핀 선택도, 네 계가 같은 자기 branch 인지도 SI 에 **한 줄이 없다** — `kb/methodology/estimand_before_running_2026_08_28.md` 의 위험신호 3개(열린 껍질·자성 기판·산화환원 활성)가 전부 켜져 있고, 회신 O 문구대로 필요한 것은 "같은 U/NUPDOWN 값" 이 아니라 **같은 state-selection policy** 다. ⇒ **ΔE(AMPS→(−H)) = −0.424 eV 는 이름은 얻었지만 어느 상태에서 나왔는지 미정.** **⛔ 절대값 이식 금지**: 면이 다르고(ICEP **(001)** / Kang **(001) 2×2×1 NMC622** / 우리 **LiNiO₂ (104)**), 엔진이 다르고(CASTEP USPP / PFP NNP / VASP PAW), 기준·U·조각 크기가 전부 다르다. ⭕ 구조적으로 옮길 수 있는 것은 **부호 방향**(불소계 대조군 대비 극성 앵커기가 더 깊다: ICEP −1.819 vs PVDF −0.703 · Kang −2.24 vs PTFE −0.09 · 우리 −0.7675 vs C₁₀F₂₂ −0.4124)과 **대조군 설계 관행**뿐. **⚠ 우리가 아직 없는 양 (Gap)**: `(−H)` 막대는 우리 `U_PCET`(양성자-결합 전자이동)의 **산화물 슬랩 버전**에 해당한다 — **우리에겐 그게 없다.** 이 지적을 우리 계에 쓰려면 먼저 만들어야 하고, 만들 때는 `kb/templates/estimand_card.md` §1–3 에 **참조·전하·스핀 선택 규칙을 먼저 적고** `db/governance/decisions.json` 에 proposed 로 올린 뒤 들어간다(이 논문이 빠뜨린 것이 정확히 그 규칙이다). **⚠ 두 논문 다 오차막대·시드 없음**; Kang `Fig 4c` 는 축 단위 오기(라벨 kJ mol⁻¹, 범위 0.5~−2.5, 본문 −2.24 eV = −216 kJ/mol → 축에 안 들어간다). 우리 쪽 비교 우위: **자세 산포 14.6 meV · 상자 수렴 0.32 meV · PTFE 대조군 2종 × 자리 2종** 을 보고한 것은 우리뿐이다.
> 🛡 **전략 대결 note [Jeong25] — *제자리 생성(in situ) 보호상 ↔ 외부 도포(ex situ) 방패* · argyrodite 물성 4축 A–D 에 수치로 넣지 않는다** [`papers/jeong2025_tough_adhesive_binder_shield_ncm811.md`]: **같은 문제(고-Ni NCM811 계면 안정화)를 전략이 정반대인 두 방법이 푼다.** 우리 = Nd(+O) 도핑 SE 가 계면에서 **hull 이 고른 인산염을 제자리 생성**(보호율 = min(1, k·x/(1−x)), 맞춘 매개변수 0, 기전 = Nd 가 **Li 를 안 쓰는** 경로를 연다: NdPO₄ Li/P=0 vs Li₃PO₄ Li/P=3). 그들 = **밖에서 합성한 가교 고분자(PVDFA-N5)를 슬러리로 바른다**(가교밀도 # 를 사람이 고른다). **★ 갈라 읽어야 하는 것 — 그들의 "보호"는 두 기전이 섞여 있고 논문이 분리하지 않는다**: **(물리 축 = 피복·차단)** conformal 나노막(`Fig. S13`)이 전해질 분자의 NCM 접근을 막는다(XPS O/Ni ↓ · TOF-SIMS CEI 절반 · CF_x:LiF 1:6.7→1:0.27) ⇒ **우리와 직교·보완**(hull 논증은 *어떤 상이 생기나* 를 묻지 *전해질이 닿나* 를 묻지 않는다). **(화학 축 = 킬레이션)** −COOH·−NH− 가 용출 TM²⁺ 를 붙잡는다(ICP-MS Ni 5.4→3.0 ppb + DFT) ⇒ **약한 경쟁** — 둘 다 "계면 **화학**이 수명을 정한다" 지만 물리가 다르다(우리 = **상 안정성**, 그들 = **이온 포획**). **분해 실험(ablation)이 하나도 없어 두 기전의 배분을 논문 자신도 모른다.** ⚠⚠ **액체↔고체 전이 금지 4건**: ① **TM 크로스오버는 액체 고유 실패모드**(용매→분리막→음극 석출) — ASSB 엔 용매가 없다 ⇒ `Fig. 4d`·`Fig. 4e`(Li 덴드라이트) **이식 불가** ② **피복의 의미가 다르다** — 액체는 다 적시므로 "덮으면 막힌다"지만 고체 SE 는 **점 접촉**이라 접촉면적 문제로 바뀐다(우리 [Kang25우리그룹] *"기생반응은 불가피, **균일성**이 지렛대"* 가 여기서 갈린다: 액체 = **차단의 균일성**, 고체 = **접촉의 균일성**) ③ **LiPF₆→LiF+HF 사슬이 우리 계에 없다** — 우리 산화 onset 2.256 V 는 **S²⁻-limited** 라 F 화학과 무관 ⇒ `CF_x:LiF` 개념·수치 **전이 금지** ④ **바인더 함량의 대가가 다르다** — 그들 10 wt%(저바인더 실험도 2 wt%) vs 황화물 복합양극 통상 1–3 wt%, 게다가 절연 피복은 σ_ion 을 깎는다(**[Bielefeld20]** 가 정량화한 페널티) ⇒ "두껍게 잘 덮어라" 가 우리 계에선 곧장 손해. **🔴 진짜 전이 대상 = 보고량 반면교사**(`kb/syntheses/binder_adsorption_charge_state_2026_08_29.md` **3번째 사례**): [Han25] = 슬랩 CASTEP + H 이동 상태를 그림 라벨로만 명명 / [Kang25] = PFP NNP 슬랩 + Na 개수를 상태 이름에 박음 / **[Jeong25] = 슬랩도 없고 상태 이름도 없다(최하한)**. 위험신호 3개(열린 껍질 TM²⁺ · 산화환원 활성 · 집계규칙 부재)가 전부 켜졌고, 결과가 **Irving–Williams 경험칙까지 위반**한다(Co −9.5 > Mn −7.3 > Ni −6.5; 같은 리간드면 Ni>Co>Mn) + **PVDF 기준이 이온마다 −0.5/−1.5/−1.5 로 3배 차이** ⇒ *"선택·집계 규칙이 없으면 스칼라 보고량은 정의되지 않는다"*(회신 N)의 **눈에 보이는 증거**. **⭕ 우리 §E(이중 적합성)에 추가할 새 축 1개**: 우리는 보호상을 **차단막**으로만 본다 — 이 논문은 보호상이 **이온을 붙잡는(trapping)** 기능도 가질 수 있음을 보인다. **우리 Nd 인산염이 TM 을 붙잡는가?** 는 hull 계산으로 답이 안 나오는 질문이다(상 안정성 ≠ 이온 포획) ⇒ **kb 질문 카드 후보**. **⭕ 논증 형식 이식 1건**: *"접착력만으로는 수명이 설명되지 않는다"*(PVDFA 는 peel 3× 인데 수명 `fr≈`243 < PVDF 318) = **단일 지표 만능론의 자기 데이터 반증** — 우리 [Kang25우리그룹] *"균일성이 지렛대"* 와 **같은 형태**. ⚠ 단 저자의 "접착·인성이 **동시에** 지배" 는 **5점으로 문턱모델과 구분 불가** ⇒ 인용은 **반증 쪽만**. **🧱 DEM 축 부수 수확**: 시험 프로토콜 3종(필름 인장 **ASTM D638-M type V, 10 mm min⁻¹, n≥5** / **180° peel 30 mm min⁻¹**, 3M 양면테이프·롤러 2.0 kg / **SAICAS 깊이 10 µm**, 블레이드 1 mm·shear 45°/rake 20°/clearance 10°·5 µm s⁻¹×200 s, `P=F_h,avg/w`)가 **[Park26]**·**[Kang25binder]** 와 같은 세트로 **3편 수렴** ⇒ 우리 바인더 파라미터 캘리브레이션의 문헌 표준 절차로 고정 가능. **⛔ 인용금지**: 결합에너지 절대값·이온 간 킬레이션 순위 · 인성 절대값(GJ m⁻³ 는 1000배 오류) · CEI 절대두께(300/650 nm = **거칠기 지배**; XPS etch 는 **≈2 nm** 뿐인데 조정 없음) · GITT D_Li⁺(**10⁻⁶–10⁻³ cm² s⁻¹**, NCM 통상값보다 4–7 자릿수 높다) · 내부저항 Ω · TM ppb 를 [Han25] ppm 과 병치 · `Table S1`(조건 미정렬 저자 자체표) · `Fig. 4d` 를 "Ni·Mn·Co 모두 감소" 로(**Mn 은 0.5 vs 0.5 로 동일**).


> 🤖 **AI/ML·LMB note [Lee26] — *cascade 방법 참고 + wide-gap SEI 개념 앵커* (액체 전해질 LMB — 물성 4축 어느 행에도 수치 편입 금지)** [`papers/lee2026_eecfp_dnn_electrolyte_ce_lmb.md`]: **Lee/Woong Kim 2026 ESM = 액체 전해질 LMB의 CE를 e-ECFP(농도-가중 분자지문)+DNN+SHAP으로 예측·설계**한 논문(자체 DFT/MD 0) — argyrodite/황화물 SE와 **재료·상(相)이 다르므로** A–F 표 수치 비교는 전면 금지, 접점은 정확히 세 곳뿐. **(1) 축 E 개념 앵커 — 음이온 유래 LiF/Li₂O-rich 무기 SEI = 좋은 Li 계면**: SHAP이 뽑은 승리 공식(F-rich 용매·LHCE형 용매화)의 종착지가 **FSI⁻ 우선환원 → LiF+Li₂O-rich SEI → 최치밀 Li·CE 99.72 %**(XPS Fig 4d,e+SEM) — 우리 sei_products.json **wide-gap 절연 산물 패밀리**(LiCl 6.65·Li₃PO₄ 5.73·Li₂O 5.24 ≫ Li₂S 3.90 eV)와 **같은 설계 원리의 액체-LMB 실험판**([KimICCF] FEC→LiF·[Li25] LiCl/LiBr·[Lu] LiCl·[Ke] Li₂O 계보에 +1). deck 한 줄: "액체든 고체든 좋은 Li 계면의 답은 무기 wide-gap SEI로 수렴". 단 이 논문엔 gap 개념·수치 자체가 없음 — 개념 정렬만. **(2) cascade 방법 참고(47-dopant 파이프라인)**: ⓐ **surrogate+SHAP 해석 레이어** — 이미 계산된 cascade 축별 점수를 타깃, 도펀트 원소 서술자(전기음성도·반경·산화수·ICOHP류)를 입력으로 RF/XGB+SHAP을 얹으면 "어떤 도펀트 성질이 어떤 축을 움직이나" design rule 추출(추가 DFT 0·비용 ~0); ⓑ **LCE형 로그변환**(−log₁₀(1−x)) = 포화 지표(blocking fraction·유지율) 처리 기법; ⓒ **소표본 교훈** — n=168에서도 Linear는 test RMSE 3.05로 붕괴·DNN 이득은 트리 대비 소폭 → **n=47인 우리는 트리 기반+교차검증이 현실적**(DNN 비권장); ⓓ e-ECFP 자체는 SMILES 분자 전용이라 무기 결정에 **이식 불가**(무기판 대응 = 우리 원소/자리 서술자·[Wang22] Th′류) — "카테고리 구분+농도 가중" 발상만 차용. **(3) 벤치마크 소환값**: Li–Cu Aurbach **99.72 %**·풀셀 평균 **99.97 %** = ASSB가 넘어야 할 액체 최고급 CE 수준; σ 0.816 mS/cm(LHCE) = "SE와 액체가 같은 차수" 서사에 **문헌끼리** 차수 비교용. **⚠ 추가 규율**: 논문 자체 데이터가 **CE 단일축 최적화의 함정을 실증**(DBE:Toluene CE 99.88 %인데 σ 0.029 mS/cm·풀셀 계면저항 152.4 Ω로 유지율 꼴찌) — 우리 cascade가 σ축을 안정성 축과 *동시에* 드는 다축 설계의 외부 정당화 사례로 인용 가능. CE·σ·SEI 조성 전부 액체계 소환값(방법 명시 없이 이식 금지).

> 🤖 **ML-계보 note [Fujimura13] — *σ-예측 ML 1세대 원조(2013) · LISICON 산화물 = 물성 4축 어느 행에도 수치 편입 금지*** [`papers/fujimura2013_ml_conductivity_origin.md`]: **Fujimura/Seko/Tanaka 2013 AEM = 고온 FPMD 기술자 + 실험 σ 라벨을 커널 회귀로 묶어 저온(373 K) 전도도 지도를 그린 원조** — 우리와 재료가 다르므로(oxide LISICON vs 황화물 argyrodite) 수치는 전부 소환값, 접점은 아래 세 축 + 물리 보너스.
> - **(1) 세대 계보 한 줄(발표 슬라이드용)**: "**Fujimura 2013**(가우시안-커널 SVR — *사람이 설계한* 물리 기술자 4개(D₁₆₀₀/Tc/V_dis/T) + 실험 라벨 95점, γ-LISICON **단일 조성족 내 보간**, log σ 오차 0.373, γ-Li₄GeO₄ 제안) → **Sendek 2017**(로지스틱 분류 — **물질군 횡단** 스크리닝; 상세는 `papers/sendek2017_ml_screening_12k_conductors.md`) → **우리/랩 2026**(**TabPFN ICL** — 사전학습 prior가 기술자 설계 부담을 흡수, 47-dopant cascade·DEM 코퍼스 소표본 표형 회귀)". 1→3세대의 이동 = "기술자를 사람이 만든다 → 모델이 표를 그대로 먹는다"; 3세대 내내 불변 = **소표본 + 물리 기술자 + 측정 불가/저온 영역으로의 다리**라는 문제 구조.
> - **(2) '이론 기술자 + 실험 라벨' 혼합 vs 우리 layer-분리 규율(방법론 교훈)**: Fujimura의 혼합은 **특징=이론 / 라벨=실험으로 층이 분리된 "학습된 다리"** — 우리 "문헌값·우리값 혼합 금지"(=*같은 층*에 두 출처를 섞지 말 것)와 양립하는 허용 형식이다. 단 그들이 생략한 3종 = ① 라벨 출처 가중/정규화(95점=다그룹 취합, 산포는 스스로 자인 refs 2–6) ② 조성족 leave-out 등 외부 검증(bootstrap 내부오차뿐) ③ 기술자 계통오차 명시("theoretical data are … consistent with the experimental data"가 *가정*으로만 명문) — **우리 TabPFN 적용 시 반드시 추가할 체크리스트**. Fig 4 캡션 "iterative analysis" 절차 불투명 = 재현성 반면교사.
> - **(3) 일반화 범위 대비**: 그들 = γ 구조 고정·의사이원 고용체 **72조성 보간**(최상위 γ-Li₄GeO₄는 α로 결정화=합성 장벽 → **탐색공간 정의 자체가 함정일 수 있음**의 1세대 실증) vs 우리 = argyrodite host 고정 + **47-dopant 원소 횡단**(구조족 횡단은 Sendek 세대부터). 교훈 = "ML 스크리닝의 신뢰 반경 ≈ 훈련 분포 반경 + 탐색공간의 합성 가능성 필터(그들의 ΔF^S<0 필터가 원시형)".
> - **(물리 보너스, 축 A 관련 — framework note)**: ① **"Tc(질서화) 아래 고온 외삽 무효"** = 우리 Arrhenius **600/800/1000 K 3점·400/500 K 제외** 규율의 1세대 물리(disorder ensemble "ordered=frozen artifact" 방향과도 일치) ② **D₁₆₀₀↮V_dis** — "부피→σ" 논거는 **전역 격자부피(무관, Fujimura 반증)/국소 채널 부피([Rao] Voronoi·우리 BVSE `migration_volume_fraction`, 상관)** 를 구분해 쓸 것([Ma24] 격자팽창 서사에도 같은 경고) ③ **p_Oct(전도 부격자 점유율)=1차 인자** = [Perc] "carrier>pc"·[Adeli] Li 공공(48h 0.456) 서사의 2013 선례(단 그들 스스로 예외 명시 → 단일 기술자 과신 금지). **✎2026-08-03 Fig 3 실물 판독으로 정밀화 — p_Oct는 단조 구동인자가 아니라 "onset" 기술자**: p_Oct가 0을 지나는 구간(tie line 1 양 계열, V-IV tie line 2)에서만 D₁₆₀₀이 0.1→6×10⁻⁹로 급변하고, 이미 p_Oct≥0.25인 채 올라가는 구간(II-IV tie line 2 0.25→0.75 3배)에선 **6–8×10⁻⁹로 포화**해 무상관 — 논문이 "예외"로 남긴 것의 정체가 포화다. **우리 인용 문법: "운반자를 더 넣으면 빨라진다"(✗) → "운반자가 없으면 죽는다"(✓)** — [Perc] 퍼콜레이션 문턱 서사와 이 형태가 더 정확히 맞물림.
> - **(반면교사, 우리 TabPFN/cascade 산출물 규약)**: Fujimura는 예측 σ 지도를 **오차막대 없이** 막대그래프로 냈고, 그 결과 자기 오차(0.373 dec)보다 작은 1위–2위 격차(0.19 dec)가 12년간 "γ-Li₄GeO₄ 최적"으로 인용됐다. → **우리 예측 지도는 예측폭과 모델 오차를 같은 축에 표시하고, 개별 순위 대신 등급 밴드로 보고**한다.

> 🔋 **PROJECT-SEED note [Liu-hBN] — *새 계산 프로젝트: VGCF + h-BN lithiophobic 샌드위치 (ORCA) · 물성 4축 A–F 어느 행에도 수치 편입 금지*** [`papers/liu2022_hbn_lithiophobic_sandwich_li_anode.md`]: **Liu 2022 Adv. Mater. Interfaces = Cu 집전체에 lithiophobic h-BN 코팅 → Li 금속 음극 균일 증착** 논문(황화물 SE 아님·Li-metal-anode 축). **우리 argyrodite 산화(B)·이온전도(A)·기계(C)·전자구조(D) 축과 물성이 안 겹친다 → A–F 표에 안 넣음.** 대신 이 논문은 **우리 캠페인의 *새 계산 프로젝트 원형***이다 — 사용자가 **VGCF(흑연질 탄소) + h-BN + 그 둘의 double-layer 샌드위치를 ORCA로** 모델링해 **Li 흡착 차이(lithiophobicity) + Li 확산 차이**를 계산하려 함. 접점은 정확히 **방법(method)뿐, 수치 아님**.
> - **베낄 방법(=논문 DFT)**: **VASP/PBE/500 eV/Γ 2π·0.04 Å⁻¹/MP-smearing**로 3-모델 흡착E 서열 **Li–h-BN(001) −0.33**(약함=lithiophobicity) < **Li–Cu(111) −2.50** < **h-BN–Li–Cu(111) −3.16 eV**(샌드위치 최강) + **CDD**(N→Li 전하이동). Li가 h-BN *위*가 아니라 h-BN·Cu *사이*로 파고들어 "h-BN–Li–Cu" 평평 증착. 이 **흡착E 서열 + CDD**가 우리 ORCA 재현의 코어.
> - **우리 3-차이(=신규 기여 공간)**: ① 집전체 **Cu → VGCF(탄소)** — graphene basal면 Li 흡착은 pristine서 약함(h-BN −0.33 결), 결함/edge/층수가 결과 좌우 → "VGCF가 샌드위치서 Cu(−2.50) 역할을 하나?"가 우리 과학적 질문; ② **주기 slab(VASP) → 분자 cluster(ORCA)** — 유한 flake(가장자리 H-종단)로 전환, 절대 흡착E 논문 등치 금지·모델 *내부 서열*만; ③ **흡착만 → 확산장벽 추가** — 논문엔 **NEB/확산 없음**(abstract "reduce ... barrier"=실험 nucleation overpotential이지 계산값 아님) → 우리 Li migration-barrier 계산이 *논문 밖 신규*.
> - **우리 그룹 내부 다리(개념, 수치 아님)**: **VGCF 공유** — [KimCA](`kim2025_conductive_agent_se_coating_cathode.md`, 우리 그룹)가 1D VGCF를 SE-코팅 도전재로 씀(0D Super P보다 우수). 이번 원자단위 프로젝트가 *같은 VGCF*를 다룸 → 복합전극 거시실험(KimCA)과 원자 흡착/확산(신규)의 물질 연결. **흡착E/W_ad 방법 계보**: 우리 UMA W_ad·[Choi2025] MLIP 계면접착과 "총에너지 차 기반 계면E" 동과(단 DFT·cluster).
> **⚠ 규율**: (1) 논문 절대값(−2.50/−0.33/−3.16 eV)을 우리 argyrodite 값과 **절대 등치 금지** — 재료·축·계 전부 다름. (2) **흡착E 정의식·Li 기준상태(원자 vs bulk-Li)·vdW 미공개** → 우리 ORCA에선 이 셋을 *명시 고정*하고 리포트에 못박기(절대값 흔드는 method-artifact). (3) **nucleation overpotential 효과 미묘/혼재**(Cu와 비슷·고전류선 오히려↑) → "약한 결합→핵생성 장벽↓→균일" 서사는 데이터가 완전 지지 안 함; 이점 실체=공간 균일성+전자·화학 격리. (4) **기계강도 아님**(코팅 E 1.655 GPa≪Li 4.9) = 논문 novelty. (5) 물성 4축 편입 금지(방법 전이만) — 진전 있으면 이 note를 갱신.

> 🎤 **TALK note [YMLee26-DTBL] — *발표 덱 · 물성 4축 A–F 어느 행에도 넣지 않는다*** [`talks/lee2026_yonsei_dtbl_ai_electrode_digitaltwin.md`]: **이용민(연세대 DTBL) "AI를 활용한 전극 미세구조 디지털화 기술과 물리 기반 배터리 시뮬레이션"** (2026 Korean Battery Symposium, 8/21, 자료집 pp.259–278; 사용자 분류 `(미분류)`). **이 덱은 DFT/물성 축이 아니라 *전극 미세구조·제조공정* 축**이다 — 이온전도도(A)·산화(B)·기계(C)·전자구조(D)·환원(E)·도핑(F) 어디에도 **수치로 편입하지 않는다**. 실질 대조는 **`comparison_vs_ours_DEM.md`**(§B 전달 삼중항 · §E 검증 · §F 흡수목록). **덱 등급 규율은 `talks/README.md`**(papers/ 보다 한 단계 낮음).
> - **A축과 닿는 단 하나의 연결(개념, 수치 아님) = "Blinded Scale"**: 덱 슬 6이 **소재 수준 이온전도도 5.4×10⁻⁴ S/cm → 셀 내부(전극) 7.9×10⁻⁷ S/cm ≈ 3자릿수 강하**를 제시하고 그 격차를 **미세구조가 만든다**고 명명한다. ⇒ 우리 규율 **"문헌 σ(소재) 와 우리 σ_eff(전극) 를 같은 표에 넣지 않는다"** 의 *그룹 자체 근거*. ⚠⚠ **그 두 수치는 LLZO(산화물) 계열 인용값**이며 우리 LPSCl 값이 아니다 — **논리·비율만 쓰고 절대값은 A축 표에 넣지 말 것**. 인용 표기(`Nano Energy 79, 10545 (2021)`)도 논문번호 자릿수가 의심스러워 **레퍼런스 리스트 이식 금지**(digest §13-4).
> - **정본 위치**: 덱 결과의 거의 전부가 이미 `papers/` 에 있다 — `park2020_digitaltwin_assb_foundational.md` · `kim2024_digital_twin_acsenergyletters.md` · `lim2025_virtual_calendering_framework.md` · `song2025_electrochemo_mechanical_microelectrode_ees.md`. **덱↔논문 충돌 시 논문이 정본.**
> - **DFT 쪽으로 넘어올 가능성이 있는 항목 1건**: 슬 22 **"황화물 SE·폴리머는 측정 과정 자체가 구조를 왜곡한다"**(공기 부반응·열손상). 이건 *구조 획득*의 문제라 물성 4축은 아니지만, 우리 **대기안정(air/HSAB) 서사**와 물리적으로 같은 뿌리다. ⚠ 정본(Chem. Eng. J. 522 (2025) 167791 / AEM (2026) e05319) **미보유 → 인용 금지**.

> 🎤 **TALK note [SULee26-SKKU] — *발표 덱 · 물성 4축 A–F 어느 행에도 수치로 넣지 않는다*** [`talks/lee2026_skku_mlip_materials_design.md`]: **이상욱(성균관대 화공, CMS Lab) "기계학습 포텐셜 기반 소재 물성 해석 및 설계"** (2026년도 전지기술 심포지엄 기술세션 3-3, 8/21, 자료집 pp.279–296; **덱 실물 전 18 pp 독립 재판독 2026-08-03**, inbox 재투입, **사용자 분류 `(미분류)`**). **같은 물질(Li₆PS₅X)·같은 도구(MLIP)·다른 축의 정면 경쟁 그룹**이고, 덱의 5갈래 중 **넷은 이미 `papers/` 에 정본이 있다** — 이 정본들이 A–F 행의 인용원이고 **덱은 지도로만** 쓴다.
> - **정본 대응표**: 무질서→σ = `papers/kim2024_mtp_argyrodite_disorder_gb.md` [KimMTP] · 음극계면 SEI = `papers/kim2026_li_argyrodite_sei_reactive_md.md` [KimSEI, ⛔프리프린트] · 양극 코팅 스크리닝 = `papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md`(**17,230 Li·O 산화물 → Li₃Sc₂(PO₄)₃**) · CSP = `papers/kim2025_csp_metastable_edge_sharing_sse.md` + `papers/kim2025_li3ycl6_new_crystal_structure.md` · 기술자 계보 원전 = `papers/jun2022_argyrodite_ion_cage_size_descriptor.md` [Jun22]. **표면 가수분해(AFM revision)만 정본 미보유 = 덱이 유일 출처 → 원고 인용 금지.**
> - **A축(이온전도도)와 닿는 지점은 규율뿐, 수치 아님**: 그들 파이프라인은 10 ns NPT MTP-MD에서 **σ_RT 절대값을 직접 인용**하지만, [KimMTP] 정본이 **같은 물질에서 훈련 functional에 따라 σ가 8배 갈린다**(optB88만 무질서 의존성 재현)를 보였다 ⇒ **우리 "MLIP σ 절대값 인용 금지" 규율의 외부 정당화**. ⛔ 덱의 σ·D 절대값은 A축 표에 넣지 않는다(비율·자릿수만).
> - **⛔ 2026-08-03 재판독으로 철회된 우리 기록 3건** — 종전에 "덱이 틀렸다"고 적어둔 항목 중 **①"17,233 Li-P-S-O"(실제 덱 원문 `17,230 Li, O`) ②D 자릿수 오기(덱도 `×10⁻⁷`) ③"25 °C vs 80 °C"(실제 `25 °C / 60 °C`, 인용된 Luo 2022 cryo-TEM 그림 라벨)** 는 **덱이 아니라 우리 저해상도 전사의 오류**였다(digest §15b). ⇒ **규율은 유지**("수치는 논문에서, 덱은 지도"), **절차만 추가**: *덱을 오류로 기록하기 전에 덱 실물을 원해상도로 재판독한다*. 현재 유효한 덱-vs-실물 불일치는 **CSP 엔진 귀속(Rare Metals 2025 = CALYPSO+DFT인데 덱은 USPEX+MTP로 묶음)** 과 **Li₂SiS₃ σ '4자릿수'** 2건.
> - **덱에서만 얻는 방법 자산(수치 아닌 절차, 이식 대상)**: **γ_select = 2 / γ_break = 10↔5↔2 외삽등급** + 수렴 4조건(MD reliability 100 % · selected < 50 · MAE_E < 10 meV/atom · MAE_F < 0.3 eV/Å) · **반응좌표 기반 훈련·검증셋**(pre-mixing → reactants → TS → products, 유도좌표 D_S–H·D_O–P) · **영역분해 MSD**(계면/벌크 구획 D) · functional 3종 병렬학습. 실행 항목은 `kb/projects/symposium_2026_competitive_analysis.md` T1–T8.

> 🎤 **TALK note [Moon26-CAU] — *발표 덱 · 물성 4축 A–F 어느 행에도 수치로 넣지 않는다*** [`talks/moon2026_cau_llm_agent_battery_automation.md`]: **문장혁(중앙대 에너지시스템) "AI 기반 배터리 연구 자동화: LLM 기반 연구 분석에서 AI-Agent 전극 모델링까지"** (2026년도 전지기술 심포지엄 기술세션 3-4, 8/21, 자료집 pp.297–318; **덱 실물 전 22 pp 독립 재판독 2026-08-03**, inbox 재투입, **사용자 분류 `(미분류)`**; PDF 텍스트레이어 0 = 전면 스캔 → 슬라이드 단위 crop 통독 + 수치영역 3–8× 확대). **이 덱에는 우리 A–F 축에 넣을 물성값이 애초에 없다** — 본체는 **연구 공정 자동화(LLM·KG·다중 에이전트)** 이고, 유일한 물리 결과(슬 37–38 흑연 전극 rate)는 **미세구조 축**이라 실질 대조는 **`comparison_vs_ours_DEM.md`** 에 둔다. 덱 등급 규율은 `talks/README.md`.
> - **A/B축과 닿는 유일한 지점 = *수렴 검증(convergent validation)*, 수치 아님**: 슬 16 GNN 링크예측 **Case 1 "Soft-acid cation doping (HSAB: Sn/Sb/As) in sulfide SE → Low ionic conductivity [RESOLVED]"** 가 **우리 cascade `air_hsab` 축과 같은 명제**다. 우리는 물리 기술자 계산으로, 그들은 문헌 그래프 링크예측으로 같은 결론에 도달 = **독립 경로의 일치**. ⛔ "우리 계산이 그들 예측을 검증했다"는 인과·시점 주장 금지, *일치*까지만. ⚠ 재판독으로 확률까지 확보 — **P(resolved) 0.57 / P(not_resolved) 0.18 / P(unknown) 0.25** 로 **과반을 겨우 넘는 값**이니 "높은 확신"이라 쓰지 말고 확률을 병기할 것. Case 2 도 종전 기록의 `Li₆PS₅Cl` 이 아니라 **`Li₆PS₅A` (A = Cl/Br/I) 일반형**(P 0.55).
> - **⛔ 스택압 문장은 인용 금지**: 슬 16 KG-RAG 답변이 *"복합양극 황화물 ASSB는 **5–10 MPa** 저압에서도 안정 계면·용량유지 가능, **>20–100 MPa** 과압은 Li 침투·입자균열·계면열화"* 라고 말한다(근거 "Papers 1, 3, 7, 18, 19, 30"). **우리 스택압 정본**(`papers/cronau2021_...`·`doux2020_...`·`papers/lee2024_multiphysics_dem_fem_initial_pressure_assb.md`)**과 같은 명제지만, 이건 LLM 요약문이지 측정치가 아니다** — 숫자를 우리 문서·원고에 옮기지 말 것. 유용한 건 "그들 KG가 우리와 같은 질문을 이미 던지고 있다"는 사실뿐.
> - **⛔ 2026-08-03 재판독 — 우리 종전 digest 교정 16건 중 A–F 서술에 영향 있는 것 0건, 그러나 오류율은 높았다**: 수치성 항목 기준 약 1/4이 우리 전사 오류였다(5,680→**5,689**편 · 8,965.8→**8565.8 s** · 21.7→**21.2 mm** · arXiv 04746→**04748** · 30×38→**30×30 µm** · KG 관계타입 3종 · 3C 랭킹 1·2위 뒤바뀜). **덱이 실제로 틀린 건 2건**(슬 21 표 21700 vs 도면 4680, 슬 19 BatteryBERT 정답 라벨). ⇒ `talks/README.md` 3b 규율 재확인 + **절차 강화**: *스캔 덱은 페이지 통짜 렌더로 숫자를 읽지 않는다 — 슬라이드 단위 crop + 수치영역 확대가 기본*.
> - **지식층 평가 하향 조정 1건**: 종전에 "그들 KG엔 방법 맥락이 남는지 불명"이라 적었으나, 재판독한 neo4j 패널이 **`MetricResult`·`TestCondition`·`UNDER_CONDITION`·`MEASURED_AS`·`SHOWN_IN→FigurePanel`** 를 갖고 있다 = **실험 조건 맥락은 스키마 수준에서 보존**된다(노드 9,596 / 관계 18,145). 다만 property key가 `active_loading_mg_cm2`·`air_exposure_s` 처럼 **제조·측정 조건 중심**이라 *계산 방법 맥락*(functional·k-mesh·supercell·무질서 처리)까지 담는지는 여전히 불명. ⇒ **우리 T6 그래프층의 고유 확장은 `Method`/`Functional`/`kMesh` 노드타입**으로 잡는다(그들 스키마에 없는 칸).

> 🎤 **TALK note [Oh26-Pol] — *튜토리얼 덱 · 물성 4축 A–F 어느 행에도 수치로 넣지 않는다 (덱 수치 0건 이식)*** [`talks/oh2026_kecs_cell_polarization.md`]: **오승모(연세대 Battery Convergence Engineering + Min Tech) "셀 분극에 의한 이차전지의 성능" (2026 전지기술 심포지엄 Tutorial I, 8/20, 자료집 26 pp = 2-up 덱 48장, 텍스트레이어 0 = 전면 스캔, 녹취 83분 13초). 층위가 다르다 — 우리는 재료 내부(Å–nm, MLIP-MD), 이 덱은 소자(µm–cm, 실동작 전류). 그래서 `750/600/560 mAh`·`−282/−256/−26 kJ mol⁻¹`·`1.28/1.30/1.44 V`·`i₀ 2.2 µA`·`135 °C` 등 **덱 수치는 전부 튜토리얼 예시(출처 미표기)라 A–F 표에 넣지 않는다.** 대신 이 덱은 우리 계산량이 소자에서 *어느 항으로 들어가는지*를 명시 지정한다 — 그 다리 4개만 개념으로 남긴다.**
> - **★★ A축(이온전도)와 닿는 다리 = `R_SE = l/(κ·A)` (개념, 수치 아님)**: 덱 슬 44 가 `R_separator = l/(κ_separator·A)`, `R_solution = l/(κ_solution·A)` 로 **κ 와 셀 분극 사이의 유일한 통로**를 지정하고, 파란 박스로 **"What really matters is not the conductivity but the resistance !!"** 를 못 박는다(+ 구두 1:17:17 동일 취지). ASSB 에서는 **SE 가 분리막이자 catholyte** 라 우리 κ 가 `R_separator`·`R_catholyte` **양쪽에 동시에** 들어간다. ⇒ 우리 헤드라인 *"modelc(Cl-rich)가 comp1 대비 D 2.6×"* 는 **κ 축의 진술이고 셀 분극 축의 진술이 아니다** — `l`(SE 층 두께)·`A` 는 우리 계산에 **없다**. 덱 슬 45(젤리롤)가 그 실증: 비수계 전해질의 낮은 κ 를 **A↑·l↓ 기하로 상쇄**한다. 또한 우리 σ 는 주기셀 벌크값이라 **GB·기공·접촉·tortuosity = 0 인 상한**이고, 그 격차는 덱의 `R_others` 에 해당한다(§H "시트/펠릿 microstructure σ" 행 · [KimICCF] device σ ≠ bulk σ · [YMLee26-DTBL] 3자릿수 강하와 **같은 축**).
> - **★★ B축(산화안정)과 닿는 다리 = `E^a = E^a_eq + η_a` (해석 정정, 수치 아님)**: 덱 슬 23–25 가 충전 시 **anode 실제 전위 = 평형 + η_a**, cathode = 평형 − η_c 임을 유도한다. ⇒ ① 우리 `산화 onset 2.256 V` 는 **반쪽전지 전위(vs Li/Li⁺)** 이지 셀 전압이 아니다(덱 구두 20:22 *"풀셀의 평형전압 이런 말은 없어요"*) — 셀 공칭 4.2 V 와 **직접 빼지 않는다**. ② 우리 grand-potential ESW 는 **η = 0 평형 열역학**이므로 **고율 조건에서는 항상 낙관 쪽**이다. 정확한 문장: *"평형 기준 2.256 V 이상에서 열역학적으로 산화. 실제 셀에서는 anodic overpotential 만큼 더 일찍 그 조건에 도달한다."* ⚠ 단 **밀어주는 것은 η_a 이지 iR_total 이 아니다** — 둘을 뭉뚱그려 "다 더 가혹"이라 쓰면 과장.
> - **★ 우리 `Ea`/`D`/BVSE 의 소재(所在) 확정**: 덱은 두 과전압을 **끝까지 분리**한다 — 활성화 가지 `R_ct = RT/(i₀F)`, `i₀ = FAk⁰C_O*^(1−α)C_R*^α` [슬 42] vs 농도 가지 `R_mt = RT/(nF·i_L)`, `i_L ∝ D_O` [슬 43]. **우리 값은 전부 농도 가지**이고, **활성화 가지(k⁰·i₀·α·R_ct)는 우리 계산 0건**이다. ⇒ *"우리 NEB/Ea 가 낮으니 과전압이 낮다"* 는 **반만 맞는 문장**이다(임피던스의 `R_ct` 에 대해 우리는 아무 말도 못 한다). 덱 소환값 참고: *"solid-state bulk diffusion is **10³~10⁵** slower than in solution"* [슬 43, 6× 확정] — **출처 없는 소환값이라 인용 금지, 맥락용**.
> - **★ §H 공백의 소자 언어 동기 = `R_SEI`**: 덱 슬 46 — 노화·고온 셀에서 `R_SEI` 가 다른 저항을 압도하고 원인은 **더 두껍거나 더 치밀해져서**. 우리는 grand-potential 로 **산물**(`Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻`)과 **onset**(2.256 V)만 내고, `sei_products.json` 은 그 산물의 **결정상 gap(전자 절연성)** 만 본다 — **interphase 이온 저항률·두께 성장 kinetics·치밀도는 0건**. §H "Li 금속‖SE 계면 반응 MD(SEI 두께·상·성장 시간, `open_items` T3)" 행과 **정확히 같은 구멍**이며, 이 덱이 그 구멍이 수명·고온 이력에서 왜 지배항이 되는지를 소자 언어로 준다.
> - **⛔ 이 덱에서 우리 축으로 이식 금지**: ① **Levich 한계전류** `i_L,c = 0.62nFAD_O^(2/3)C_O*ω^(1/2)/ν^(1/6)` [슬 43] — **RDE(회전원판) 전용**이라 대류·ω 가 없는 고체전해질에 의미 없음 ② **PE 분리막 셧다운 135 °C** [슬 22] — ASSB 에 대응 기구 없음 ③ **`Q_rev = TΔS` / `E_cal`** [슬 33–35] — 우리는 0 K 근사라 엔트로피 항 자체가 없음 ④ **덱 슬 30 을 "실제 데이터"로 인용 금지**(구두 47:15 에서 그렇게 불렀으나 축 눈금·출처 없음) ⑤ **[말] 숫자 금지**(구두 ≈−280/−250/"플러스 1"/3.8 V 는 반올림·실언).
> - **⛔[불일치] 1건 · 덱 오타 3건 (재판독 확정)**: 슬 43 **ν 방향** — 덱 *"Minimize ν"*(식에서 분모) ↔ 구두 *"kinematic viscosity 이런 것들이 커야지만"*[1:15:00] ⇒ **덱 채택, 불일치로 기록**. 덱 오타: `Battery **Conflation** Engineering`(→Convergence, **8× 확정**) · `Activaton`(슬 29) · 슬 39 ΔG/ΔH 부호 문장(그림이 정본). 표기 흔들림: η 부호(슬 13 `+η_c` ↔ 슬 23/24 `−η_c`, **후자가 정본**) · `R_total` 분해 3종(슬 25/44/46) · Ni-Cd `E_cell` 1.28 V(E⁰차) vs 1.30 V(ΔG). **우리 1차 전사 오류도 1건 있었다 — 슬 9 삽입그림 `E_cal = 1.44 V` 를 `E_cell` 로 오독했고 8× 재판독에서 자체 정정**(`talks/README.md` §3b 실패 모드 재현).

## A. 이온전도도 — *Cl-rich가 빠르다 (전원 일치)*
| 주장 | 출처 | 우리 (comp1→modelc) | 일치 |
|---|---|---|---|
| **🔴🔴 이 논문의 Ea 는 우리 Ea 와 *같은 종류의 양이 아니다* — 나란히 쓰면 틀린다** — [Lu24] 의 `E_int` 는 **셀 임피던스 성분 R_int(=R_cei+R_ct) 의 온도의존**(EIS→DRT→등가회로→5점 Arrhenius, **SOC 20 % 고정**, ⌀10 mm 4층 펠릿)에서 나온 **계면 전하이동** 활성화에너지다: **60.19(맨 Ni90/LPSC) → 41.39(Li₂ZrO₃ 코팅) → 25.79 kJ mol⁻¹(Li₃InCl₆ 촉매질)** = 0.624 → 0.429 → **0.267 eV**. 우리 값은 **Li 자기확산계수 D 의 온도의존**(MLIP-MD, MSD 2–50 ps 창)이다. **위치(계면 vs 벌크)·대상(소자 vs 주기셀)·측정량(저항 vs D)이 전부 다르다** | **[Lu24]** `Fig. 4g,h,i` 범례 (★ 본문에 없는 `E_Rohm` 36.29/35.80/37.65 · `E_Rcc` 43.46/41.55/41.38 kJ mol⁻¹ 도 digest 가 그림에서 회수) | comp1 **0.2532 eV**(단일궤적, `HZ-comp1-Ea-diffusive-gate` **HOLD**) · modelc **0.197 ± 0.032 eV**(3-seed, canonical) · lpsocl_box331 **0.180 ± 0.002 eV**(canonical, **cell-conditioned** — `bulk_claim__cell_conditioned_only`·`RT_extrapolation` 금지) | ⛔⛔ **같은 표·같은 문장·같은 그림 전부 금지.** *"문헌 계면 0.43 eV 대비 우리 벌크 0.18 eV"* 류 문장 **금지**. 우리 0.180 을 **"벌크"** 라고 부르는 것도 금지(원장이 bulk claim 을 막는다). 🟢 **허용**: *"계면 전하이동 Ea(EIS)와 벌크 자기확산 Ea(MD)는 다른 양이며, [Lu24] 는 전자가 코팅으로 **낮아지는 방향**을 보였다"* — **방향만, 값 없이** |
| **★ 계면이 벌크보다 *느리다* 는 반대 사례 — [Wang26IF] 와 정면으로 갈린다** — 같은 셀에서 `E_Rint` **60.19** ≫ `E_Rohm`(주로 SE 벌크) **36.29 kJ mol⁻¹**. 그런데 계면을 고치면(③ LIC) **`E_Rint` 25.79 < `E_Rohm` 37.65 로 역전** → 율속이 계면을 떠나 **SE 입계(D1)** 로 간다(`Fig. 4f` D1 ≈ 385 Ω ≫ D3 ≈ 95 Ω, figure-read) | **[Lu24]** `Fig. 4d–i` | 우리는 **벌크만** 본다 (계면 Ea 축 없음) | ⭕ **방향만 소환.** [Wang26IF] 는 *"a-Li_xSi\|LPSCl 계면 12개가 전부 양쪽 벌크보다 **빠르다**(0.10–0.30 eV)"* 라 했다. 두 digest 를 같이 인용하면 **"계면은 계에 따라 빠를 수도 느릴 수도 있다 — 화학쌍이 정한다"** 가 된다. ⛔ 값 이식 금지(한쪽은 EIS 셀값, 한쪽은 MD 벌크값) |
| **⚠ interphase 의 *자체* 이온전도도가 코팅 판정을 뒤집는다 — 그런데 그 값들이 남의 논문이고 온도가 없다** — `Fig. 5` 논지의 절반이 문헌 σ 나열이다: Li₂S **7.51×10⁻¹¹** · Li₃PO₄ **3×10⁻⁷** · **Li₂ZrO₃ 7×10⁻⁵** · Li₃InCl₆ **1.13×10⁻³ S cm⁻¹**(마지막만 자체 측정 25 °C, `Fig. S10`). 🔴 **LZO 값이 계보 #3 [Xiao19](NEB Ea 0.48 eV, σ ~10⁻⁴ @ 598 K)의 상온 환산 ~2×10⁻⁸ 과 3,500배 어긋난다**(우리 산수, §10-C2) | **[Lu24]** 본문 p.6 + `Fig. S10` · 대조 **[Xiao19]** `Table 2`/`Table S6` | 우리는 σ 절대값 인용 자체가 금지다(`absolute_sigma` prohibition) | ⛔ **σ 4종 전부 이식 금지**(온도·결정성·시료형태 미기재). 🟢 **방향은 안전**: LZO 가 LIC 보다 낮다는 결론은 7×10⁻⁵ 가 맞아도, 10⁻⁸ 이어도 성립한다(후자면 **더 강해진다**) |
| **★★ `Li₂ZrO₃` 5판정 표가 닫혔다 (계보 카드 ④번 숙제)** — #2 [Aykol16] ⛔탈락(−E_c 3.150 < 3.5 V 컷) · #3 [Xiao19] 🟡기준물(NEB 0.48 eV) · #5 [Nolan21] ✅생존(창 0.34–3.41 V) · **#9 [Lu24] 🟡실험✅이지만 불충분**(계면 Ea −31 %, 계산 장벽 4종 중 **최저 0.14 eV**, 그러나 interphase σ 부족으로 LIC 에 진다) · **[Kang25](우리 그룹) ✅다른 축**(화학 패시베이션 + 균열 억제, 100th +54.4 mAh g⁻¹). **종합**: *"LZO 는 열역학·화학은 고치고 **자기 자신의 이온전도**에서 진다 ⇒ #2 의 σ 필터는 잘못된 이유로 옳았다"* | **[Lu24]**+**[Xiao19]**+**[Nolan21]**+**[Aykol16]**+**[Kang25]** | 우리 cascade 코팅 후보표에 **"코팅 자체의 σ" 열이 없다** | ⭕⭕ **작업거리 확정** — cascade 후보표에 코팅 σ(또는 BVSE 채널) 열 추가. §11c-1 |
| **★★ 볼밀 Li₂S/LPSCl(= 우리 계; 30:50 wt = x_Li₂S 0.778, 우리 지정점과 동일) 의 σ 는 논문에 없다 — Nyquist 만: R_lowf 1145 Ω(500 rpm 1 h) → 2675 Ω(10 h)** (Source Data `Fig. S10c`, Ti\|composite\|Ti, 75 MPa, 25 °C, 7 MHz–100 mHz). 같은 프로토콜의 S/LPSCl(σ **6.0×10⁻⁶ / 2.1×10⁻⁵ / 2.0×10⁻⁵** @0.5/1/10 h)·LPSCl 단독(**1.8×10⁻³ → 1.3×10⁻³ → 4×10⁻⁵**, 10 h 에 Li₂S+LPS 석출)·LPS(4×10⁻⁵) 펠릿에서 L=σ·R·A 로 역산한 두께가 **0.44–0.55 mm 로 일정** → 같은 두께면 Li₂S/LPSCl ≈ **5–6×10⁻⁵ (1 h) / ≈2.5×10⁻⁵ (10 h) S cm⁻¹** ≈ 촉매전해질의 1/40 (**digest 추정 — 논문값 아님**). ⚠ 밀링 전(mixed) Li₂S/LPSCl 의 σ 는 미측정 → *"밀링이 Li₂S 복합체 σ 를 올린다"* 는 증거는 **없다**; 0.5→1 h 에 3.5× 상승은 **S/LPSCl 에서만** | **[Cronk26]** `Fig. S4c,f`·`Fig. S8a`·`Fig. S10c` + Source Data(원본 xlsx `litdb/inbox/104. Sup1) …source_data.xlsx`; 전사 CSV 는 `litdb/inbox/104_source_data/` = 저장소 밖; 파생 요약표 `litdb/figures/cronk2026_lis_cathode_interphase_chemistry/source_data_derived.csv`) | 우리 ③ *"결정 Li₇PS₆ 는 LPSCl 보다 느리다(de Klerk 2016) → 비정질 경로만 열려 있다"* (`db/properties/lpscl_li2s_hull_layer0_2026_09_11.json` §7) — **2층 계산 전** | 🔶 **검증 안 됨(문헌 공백)**: 논문이 주는 것은 *비정질화된 Li₂S/LPSCl 이 작동한다*(723 mAh g⁻¹·CE 99.3 %·C/20·1 mg cm⁻²)와 *과밀링(10 h)이 해친다* 뿐. **Ea 0 · σ_e 0 · 계면상 단독 σ 0**. ⛔ 위 추정 σ 를 우리 UMA σ 와 한 칸에 두지 말 것(둘 다 절대값 인용 금지) |
| **★★ σ 값을 인용하기 전에 "EIS 프로토콜"을 먼저 물어야 한다 — 같은 시료가 1.3–1.9배 달라진다** — 한 논문 안에서 12 시료를 **두 프로토콜**로 다 쟀다: ①관행(295 MPa 성형 → **압력 빼고** 측정) ②가압([Zhou19] 방식, 측정 내내 가압). **digest 계산**(`Table S4` 12점 최소제곱): 단단한 P·Cl argyrodite(n=7) **기울기 1.181 · R² 0.986 · 배율 1.30–1.64**, 무른 P-free 요오드계(n=5) **기울기 2.010 · R² 0.776 · 배율 1.57–1.94**. 같은 A1 이 **7.45(관행) ↔ 13.02(가압)**. 저자 권고는 **관행 쪽**(무가압 구동 셀 현실) | **[Cho25AL]** `Fig. 3a–c` · `Table S4` (기울기·R²·배율은 **digest 재계산**, 논문은 "moderate/steeper" 정성 서술만) | 우리는 **실험 σ 가 없다** (MLIP-MD 의 D·Ea 만) — 대신 **문헌 σ 를 우리 표에 올릴 때 프로토콜 꼬리표를 강제**하는 근거로 쓴다 | ⚠ **비교 불가·규율로 사용.** 우리 절대 σ 인용 금지 규율(Nernst–Einstein Haven=1)과 같은 성격의 외부 근거 |
| **★ P 를 버리고 Ge-Si-Sb 3원 + I 로 가면 σ 는 Cl-rich LPSCl 을 넘는다 (그러나 환원 열역학을 내준다)** — 같은 저자 손으로 잰 기준물 **Li₆PS₅Cl 1.77 · Li₅.₅PS₄.₅Cl₁.₅ 5.04** vs **Li₆.₄₂₅Ge₀.₂₅Si₀.₃₇₅Sb₀.₃₇₅S₄.₈I₁.₂ 7.45** (전부 관행 프로토콜, 동일 실험실·동일 펠릿 조건) | **[Cho25AL]** `Table 1` · `Table S4` | 우리 축은 **Cl-rich 가 빠르다**(comp1 → modelc, D 2.6×)까지다 — **I-rich P-free 계는 우리 계보 밖** | 🔶 **방향 일치, 계열 다름.** "Cl-rich 가 빠르다"는 우리 결론과 모순 아님(같은 실험실에서 Cl 1.0→1.5 가 1.77→5.04 로 오른다). 다만 **P-free 요오드계는 별도 계보**이므로 우리 comp1/modelc 표에 섞지 않는다 |
| **★ 계면·표면 구역이 벌크보다 Li 가 *빠르다* — σ 게이트가 "손실만 보는 한쪽 필터"임을 드러내는 사례** — Li₆PS₅Cl **벌크 Ea 0.30 eV** ↔ **(001) 표면 slab-1(Li-rich) 0.23 · slab-2(S-rich) 0.28** ↔ **a-Li_xSi/LPSCl 계면 12개 전부 0.10–0.30 eV**. 반대로 **a-Li_xSi 표면은 벌크보다 느리다**(+0.02~+0.08 eV, Li 편석 때문) | **[Wang26IF]** `Fig. 6b` · `Fig. S23–S25` **범례 숫자**(figure-read 아님). 구역 정의 = **z 방향 2 Å(표면)/5 Å(계면), slab-2 만 3 Å/6 Å**, **80 ps 중 50 ps 이상 잔류한 Li 만** MSD 에 포함 | ⚠ **게이트 값 `D_rel_vs_host ≥ 0.90` 을 바꿀 근거는 아니다** — 이 논문은 *host 개질 전후*가 아니라 *같은 계의 벌크 vs 구역*을 비교한다(**분모가 다르다**). [Deng26PS] 의 **"σ 손실 7 % 허용 / 31 % 실패"** 같은 성능 경계는 이 논문에 **없다**(성능 데이터 자체가 0). ⇒ **게이트 0.90 유지.** 🔑 **다만 구조적 지적 1건**: 개질이 표면·계면을 만들어 D 를 *올릴* 수도 있는데 우리 게이트는 손실에만 벌금을 매긴다 ⇒ **"게이트는 손실 필터이지 이득 지표가 아니다"** 를 cascade 문서에 명시(T5). ✅ **방법론 소득**: 이 논문의 **구역별 MSD 분해**는 우리 파이프라인에 없다(우리는 셀 전체 평균) → **T1** |
| **⚠ Ea 절대값 대비 — real difference 아님(method-dependent)** — [Wang26IF] LPSCl **0.30 eV**, σ_300K **0.65 mS/cm** | **[Wang26IF]** `Fig. 6a` · SI 식 (6)–(8) | 우리 **comp1 0.253 / modelc 0.224 eV** (MLIP-MD UMA-s-1p1, 단일 궤적) | ⚠ **나란히 인용 금지.** 방법이 4중으로 다르다 — **AIMD-PBE vs MLIP-UMA** · **Nosé vs Langevin** · **80 ps vs prod 200 ps** · **MSD 창 미기재 vs 2–50 ps 고정**. 게다가 그들의 Arrhenius 는 **588–1250 K → 300 K 외삽**(1/T 로 2–4배)이고 **시드·오차막대가 0** 이다. ⛔ **σ 절대값 0.65 mS/cm 은 인용 금지**(MD+Haven=1, 우리 규율). ⚠ 그들 SE 7종 중 **LGPS 0.33 eV > LPSCl 0.30**, **Li₄SnS₄ 0.26 < LPSCl** 라는 순위가 나오는데 **실험 대조는 LPSCl 1종만** 한다 — 우리 db 에 그 두 계 실험값이 없으니 **"대조 부재"까지만 적는다** |
| **★ 표면 코팅이 σ 에 물리는 *허용 손실*의 실험 경계 — 우리 cascade σ 게이트의 외부 근거** — 같은 host(Li₆PS₅Cl) 에 poly(sulfate) 막 두께만 바꿔(DTD **0 / 0.05 / 0.1 / 0.4 M**, 12 h) 펠릿 σ **4.64 / 4.49 / 4.32 / 3.19 mS cm⁻¹** (**100 / 97 / 93 / 69 %**). 그런데 **10 C 1,000 사이클 성능은 0.1 M(144.1 mAh g⁻¹·92.1 %)이 최고**이고 **0.4 M 은 무너진다** ⇒ **σ 손실 7 % 는 허용, 31 % 는 실패**. 반응시간은 1→24 h 에서 σ 거의 불변(24 h 4.31 = 92.9 %) = **자기제한 반응** | **[Deng26PS]** `Fig. S4a,b,c` · `Fig. S5a,b,c` | ⛔ **값 이식 금지** — 그들은 **실험 펠릿 σ**, 우리는 **MLIP-MD D(600 K)**(comp1 3.09×10⁻⁶ / modelc 7.90×10⁻⁶ cm² s⁻¹) 라 단위·물리가 다르다. **이식 가능한 것은 값이 아니라 *상대 게이트*** — cascade 도핑 스크리닝의 σ 축을 "host 대비 D 감소 ≤10 %" 로 잡을 때의 **외부 실험 근거** | **△ 축이 다름 · 게이트 기준으로만 사용** |
| **⚠ "연속 10 nm 막 + σ 7 %만 손실 + σ_PS = 1.18×10⁻⁵ S cm⁻¹" 은 셋이 동시에 성립하지 않는다 (우리 정합성 계산)** — 접촉 1개당 ASR = t/σ_PS = **8.5×10⁻² Ω cm²**; 입자 ~1 µm(그들 TEM/SEM) 이면 코팅 기여/벌크 기여 = (t/d)(σ_LPSC/σ_PS) = 0.01 × (4.64×10⁻³/1.18×10⁻⁵) ≈ **3.9배** ⇒ **σ 가 1/5 로 떨어져야** 한다. 실측은 **−7 %** | **[Deng26PS]** `Fig. S13`(σ_PS, ⚠**LiTFSI 첨가값**) + `Fig. 1b`·`Fig. 2a`(입자크기) + `Fig. S4b`(σ) — **계산은 우리 것, 논문에 없음** | 해소 후보: (a) 2 ton(≈173 MPa) 압착에서 **연질막이 접촉점에서 배제**, (b) 막이 **불연속**, (c) 실제 계면 전도가 LiTFSI-free 측정보다 훨씬 좋다. **(a) 는 우리 DEM/접촉 축이 답할 수 있는 질문** | **⚠ 미해소 — `papers/deng2026…` §20-Q1** |
| **★★ X 자리를 BH₄⁻ 로 채우면 σ 가 0.7 → 16.4 mS/cm** — 조성 `Li₇₋ₓ₋ᵧPS₆₋ₓ₋ᵧ(BH₄)ₓClᵧ`, **BH₄⁻ 는 별도 자리가 아니라 halide/free-S²⁻ 가 공유하는 4a·4d 를 점유**(전하 −1 ⇒ **Cl 치환과 동일한 Li-공공 생성 기구**). SE-high `Li₅.₃₅PS₄.₃₅(BH₄)₁.₁₅Cl₀.₅`(X 자리의 57.5 %) 16.4 · SE-inter 7.9 · SE-low 0.7 mS/cm. 자리점유는 **Rietveld(F4̄3m) 와 ¹¹B MAS NMR 이 독립 확인** | **[Shin26]** `Table 1`·`Fig. 1f` — **EIS**(566 MPa 냉간가압 → 188 MPa·25 °C) | comp1 → modelc: **D 2.6배↑ · Ea↓** (Cl↑ → Li↓ → vacancy↑), MLIP-MD | ✅✅ **같은 host·같은 방향, 폭은 훨씬 큼.** *"X 자리 화학이 argyrodite σ 의 주 손잡이"* 의 **네 번째 독립 지지**. ⛔ **그들 σ 를 우리 값과 같은 줄에 놓지 않는다**(소환값·EIS vs MLIP-MD). 🔴 **BH₄ 는 우리 cascade 도펀트 축에 없다** — 자리·전하는 Cl 축의 자연 확장인데 **BVSE 에 Li–BH₄ R0 가 없어 정적 기술자로 원리적으로 못 잰다** |
| **★★ 폴리음이온 *회전* 이 Li⁺ 수송에 기여한다 — 3중으로 측정됨**: ①**실험** ⁷Li↔¹¹B SLR 활성화에너지가 3시료 모두 **0.01 eV 이내 일치**(0.27/0.28 · 0.29/0.30 · 0.35/0.34 eV)하고 시료 간 **평행 이동**; **³¹P(PS₄³⁻)만 0.16–0.18 eV 로 시료 무관**(음성 대조군) ②**인과** BH₄ **회전 구속 AIMD 에서 D(500 K) 2.0–3.0배 감소**(4배열 전부) ③**통계** 500 K·100 ps 에서 **Li hop 31건 중 28건(90.3 %)이 ±0.2 ps 안에 60° 초과 재배향 동반**. `Fig. 3f` = 같은 셀에서 **PS₄ 는 진동만, BH₄ 만 회전** | **[Shin26]** `Table 2`·`Table S9`·`Table S10`·`Fig. 3f` — SLR NMR + AIMD | ⛔ **회전 자유도가 우리 축에 아예 없다** (정적: 자리·채널·BVSE·blocking) | 🔴 **공백 확정.** 이식 경로는 있다 → **제안 T16**: 기존 UMA-MD 궤적(600/800/1000 K·200 ps)에서 **PS₄³⁻ 배향 자기상관 `C_ℓ(t)` → τ_rot → Ea_rot** 후처리 (**새 시뮬 0회**, T12 van Hove·T14 CSM 과 같은 계열). ⚠ 우리 host 엔 BH₄ 가 없어 **잴 수 있는 건 PS₄ 회전 = 이 논문이 "안 돈다"고 판정한 대상** ⇒ 신규가 되려면 **Cl 함량·O 치환 의존성**을 재야 한다. ⚠ **UMA 가 회전 장벽을 맞게 주는지 미검증**(T1 과 같은 검증 필요) |
| **★ 가압·소결이 σ 를 1.6배 올리고(16.4 → 26.1 mS/cm), 그 증가분이 *입계* 성분에서 온다** — PFG NMR 다성분 분해: SE-high **입내 9.8(82 %) / 입계 1.4(18 %)** → SE-high-hp **19.0(45 %) / 9.9(55 %)** ×10⁻¹² m²/s ⇒ **입계 D 7배·분율 3배**. 분말은 ln I–B 곡선이 굽고 Δ-의존(제한확산), 열간가압 후 **직선·Δ-무의존** | **[Shin26]** `Fig. 4a,b,d`·`Table S11` — **PFG NMR**(Diff50, Δ 20–70 ms, g 1.5–28 T/m) | 우리는 **주기셀 bulk** 만 계산(GB·접촉 미포함). DEM 축은 별도 | ✅✅ **`[Cronau]`(stack pressure dilemma)·`[Miao23]`(황화물 GB 는 무시할 만함)의 정량판이자 부분 반증** — 황화물에서도 **가공 상태가 σ 를 1.6배 바꾸고 그 원인이 입계로 정량 배정된다**. **우리 DEM 축의 실측 앵커.** ⚠ 평균 변위 (2Dt)^½ ≈ 0.9 µm ≈ 입자 크기라 Δ-의존이 나온다 |
| **★ 실험 활성화에너지 = ⁷Li SLR 0.27–0.35 eV · PFG 0.29–0.33 eV** (BPP 피팅 β≈1.3–1.4 = **상관운동**; 저온쪽 Ea,LT ≈ 0.11 eV 는 **intra-cage hop** 잠정 배정) | **[Shin26]** `Table 2`·`Table S4`·`Table S11` — SLR + PFG NMR | comp1 **0.253** / modelc **0.224** eV (MLIP-MD 단일궤적) · modelc 3-seed **0.197 ± 0.032** | 🔶 **우리 값이 계통적으로 낮다 — 그러나 방법 아티팩트일 가능성이 크다**: (i) 실험(NMR) vs MD (ii) 온도창 220–380 K vs 600–1000 K (iii) 순수 결정 vs 다상·다결정. ⛔ *"우리 Ea 가 낮다"* 를 **물리 주장으로 쓰지 말 것**. ⚠ 그들 `Fig. 4e` 는 **온도폭 47 K·점 5–6개**이고 **같은 SE-high 의 가공 산포(0.29/0.32/0.30)가 시료 간 차(0.29→0.31)보다 크다** |
| **★ Cl 자리 무질서가 Li₆PS₅Cl 의 σ 를 지배** — 4c(=4d) Cl 점유 0 % → **0.02** · 25 % → 45 · 50 % → **115–183** · 75 % → 60 · 100 % → **0.57** mS/cm (AIMD 600–1200 K → 300 K 외삽) | **[Shin26]** `Table S7`·`Fig. 3c` — ⚠ **Jun & Lee 2022 값 그대로**(= 우리 `jun2022` digest §8.2 의 `18.79 → 3.82`) | comp1 → modelc **D 2.6배↑** (Cl↑ → 무질서↑ → 빠름) | ✅ **방향 일치**(무질서가 빠르다). 🔴 **다만 10⁴ 배는 외삽 산물** — 시뮬레이션 온도(600–1200 K)에서는 **~4배** 뿐이다. **우리 T15 규율의 새 사례** |
| **⚠ 배열 앙상블을 하나의 σ_bulk 로 접는 문헌 관행 — 우리가 3자리까지 재현해 무엇을 하는지 확정했다.** `P(E)∝exp(−ΔE/kT)`·`P(σ)∝exp(−Δσ/kT)`·`σ_bulk=ΣPσ`·`σ_exp=σ_calc·χ_c^7.14`. 재현: **274.57 vs 논문 274.5 ✅ / 3.78 vs 3.82 ✅**. ⇒ `P(σ)` 는 **`mS/cm ÷ meV` = 차원 불성립**이고, 그 결과 **열역학 바닥상태(O1O1)가 가중치 0.0019 %, 최불안정(O2O1)이 84.8 %** ⇒ **σ_bulk ≈ σ_min, 열역학항은 사실상 무작동** | **[Shin26]** `Note S3`·`Eq. S4`–`S8` (상속원 = **[Jun22]**) | 우리: **결정화도 보정 없음 + σ 절대값 미인용** | ✅ **같은 병, 다른 약 — 우리 쪽이 방어적.** `jun2022` §10 N10 금지목록(*"χc^7.14 이식 금지 · Eq(6–8) 가중식 이식 금지 · σ 절대값 인용 금지"*)의 **재확인**. ⛔ **이 논문의 계산 σ 절대값(274.5 · 7.2 · 3.82 · 배열별 266–558 mS/cm) 인용 금지** |
| **⛔ "계산이 실험 σ 를 재현했다(7.2 vs 7.0)"·"BH₄ 계가 LPSCl 보다 2배 이상 빠르다" 는 자유 파라미터 2개의 산물** — χ_c 를 **BH₄ 계엔 0.6, Li₆PS₅Cl 엔 0.8** 로 따로 골랐고 **둘 다 미측정**. **같은 χ_c 를 쓰면 계산 비율은 항상 14.75배**(2배 아님). 비교 대상 σ_exp 7.0 도 **이 논문 시료가 아니라 Jang 2023** (이 논문 SE-high 는 16.4). raw σ_calc **274.5 = 실험의 39배** | **[Shin26]** `Table S5`–`Table S7` (우리 계산 §10.2) | 우리는 σ 절대값 인용 자체를 금지 | 🔴 **인용 금지 4건**(계산 σ 절대값 · "실험 재현" · "계산상 2배" · 가중식/χ_c 이식). **허용**: *"결정화도 파라미터를 조정하면 실험 자릿수와 맞출 수 있다"* 까지 |
| **⛔ 그들 AIMD 활성화에너지는 논문에 없고, 자기 표값으로 역산하면 0.13–0.17 eV = 자기 실험값의 절반** (`Table S9` D(500 K) + `Table S5` σ(300 K)→NE 역환산) | **[Shin26]** 우리 역산 (§10.3) | comp1 0.253 / modelc 0.224 eV | 🔴 **그들 계산부의 내부 불일치**(계산 0.13–0.17 vs 자기 NMR 0.27–0.35 / PFG 0.29–0.33) — 논문은 **한 줄도 언급 안 함**. **χ_c 는 온도무관 상수배라 Ea 를 못 고친다** ⇒ 낮은 Ea 가 500–900 K → 300 K 외삽 과대평가(39배)를 만들고 χ_c 가 그걸 사후에 지운다. ⇒ **우리 Ea 를 그들 계산 Ea 와 비교하지 말 것** |
| **⚠ config-variance 오차막대는 이 계보 어디에도 없다 — 네 번째 데이터점** (deklerk 배열당 단일 · kim2024 Boltzmann 가중 단일셀 · jun2022 반쪽 · **shin2026 = BH₄ *배향* 만 앙상블, Li 배치 단일, 시드 0, 오차막대 정의 미기재**) | **[Shin26]** `Note S3`·`Fig. S5` | 우리 disorder_ensemble (modelc 3-seed 등) | ✅ **우리 §3-2 카드 신규성 유지** — *"완전한 config-variance 오차막대"* 는 여전히 문헌 공백 |
| **★★ Nernst–Einstein(Eq.3) 의 유효성 유보를 리뷰가 명시** — `D = (u/q)k_BT = σ/(nq²)·H_R k_BT`, **Haven ratio H_R**. 그리고 *"there is **recent debate about the validity of equation (3)** in the case of solid electrolytes where the **migration of multiple charge carriers is highly correlated** and/or … **anisotropic migration pathways**"*(ref 39 = Marcolongo & Marzari, *PRM* 1, 025402) | **[Famprikis19]** §Atomic scale, Eq.(3) | 우리 σ = **NE, H_R = 1 가정** · CLAUDE.md **"σ 절대값 인용 금지, 비율도 멀티시드 판정만"** | **✅✅ 우리 규율의 문헌 근거**. 아르지로다이트는 리뷰가 말한 "highly correlated"(협동/interstitialcy hop)의 전형 ⇒ **H_R=1 은 근사이며 계통오차 방향 미상**. digest·원고에 각주로 명기 권장. ⚠ 리뷰 자신은 이 유보를 달고도 바로 다음 절에서 σ_macro 10 mS/cm 를 무유보로 인용(내부 불일치) |
| **σ·Ea 의 그룹 간 재현성이 약 1 자릿수까지 벌어진다** (Na₁₁Sn₂PS₁₂ 사례); 임피던스 성분 분해는 *"관측 정전용량에 근거한 **경험적 가설** 기반 추상모델 피팅"* 이라고 리뷰가 자인 | **[Famprikis19]** §Macroscopic scale (refs 59,60) | 우리 σ 절대값 비인용 규율 | **✅ 독립 도달한 같은 결론** — "문헌 σ 를 우리 값과 직접 비교하지 않는 이유"의 인용처. `miao2023` 의 "EIS 정전용량 배정은 largely empirical" 자백과 동일 계보 |
| **입계(GB) 효과는 "재료에 따라 다르고 **황화물 고체전해질에서는 무시할 만하다**"** (ref 54 = Ganapathy/Wagemaker). 일반적으로 GB 는 저항↑(양의 공간전하 반발 ref51 · 차단 불순물 싱크 ref53 · 결정립 misalignment 가 percolation 을 막음 ref52) | **[Famprikis19]** §Micro–meso | 우리는 **주기셀 bulk** 만 계산(GB 미포함) | **✅ 우리 bulk 계산의 문헌 방어선** — [Miao23]("냉간가압 100–300 MPa 에서 황화물 GB 는 수송을 크게 안 막는다")와 **독립 2번째 근거**. ⚠ 뒤집으면 **황화물에서는 GB 화학이 아니라 접촉 기하(기공·접촉면적)가 지배** ⇒ DEM 축의 정당화 |
| **⚠ 연질 골격의 "양날" — Ea 만 보면 안 된다**: 무른 음이온 골격(sulfide/selenide)은 ① **Ea ↓**(도움) 이지만 동시에 ② **포논 진동수 ↓ → 시도진동수 ν₀ ↓ 및 이동 엔트로피 ΔS_m ↓ → Eq.(2) prefactor σ₀ ↓**(해로움). ν₀ ↔ 음속 유래 **Debye 진동수** 상관(ref 29 = [Kraft]), Ea ↔ **포논 밴드센터**(INS, ref 31 = Muy) | **[Famprikis19]** §Atomic scale, Eq.(2) `σ₀ = z(nq²/k_B)e^{ΔS_m/k_B}α₀²ν₀` | 우리는 **Ea·D 만** 본다 (comp1 0.253 / modelc 0.224 eV, MLIP-MD 단일궤적; 3-seed 0.197±0.032). **σ₀·ν₀·ΔS_m 미계산** | **⚠ 우리 서사의 사각지대** — Cl-rich 의 Ea 이득이 σ₀ 손실로 얼마나 상쇄되는지 확인한 적 없다. **바로 채울 수 있는 칸**: 우리 phonon/ε∞ 라인으로 comp1 vs modelc **Debye 진동수** 비교(→ H-리스트 신규 항목) |
| **협동(interstitialcy) 이동은 장벽을 낮춘다 — 그리고 *두 거리*를 구분해서 라벨한다** — `Fig. 3c` **figure-read**(2026-08-06 확대 재확인): `E_m^interstitialcy`(준안정 사이트 기준)가 안정 사이트 기준 장벽의 **절반쯤**. 거리 라벨 둘 — **α₀ = 전하/결함이 옮겨간 거리(준안정→준안정)**, **α₀′ = 개별 이온의 변위(≈0.48 α₀)**. (본문은 "reduced migration energy" 만 서술, 두 거리는 그림 라벨로만 존재) | **[Famprikis19]** `Fig. 3c` (figure-read ≈) | 우리 modelc D 증가를 "Cl 무질서 + 공공"으로만 설명 | ✓ **기구 어휘 보강**. ⚠ **2026-08-06 정정 — 이 칸의 종전 결론("Eq.(2)의 α₀² 가 줄어 협동 이득이 상쇄된다")은 철회한다.** σ₀ 에 들어가는 α₀ 는 **전하가 옮겨간 긴 거리**이고 α₀′ 는 개별 이온 변위다 — 그림대로면 협동은 **장벽↓ + hop 거리 유지 = 순이득**이다. 남는 유보는 α₀ 가 아니라 **ΔS_m·ν₀**(아래 줄) 쪽 |
| **★★ 리뷰가 Molecular dynamics 를 "이온수송 *직접·정량* 프로브" 등급으로 분류한다** — `Fig. 2` 캡션: *"techniques utilized to **directly probe** ion transport (that is, **quantitatively determine the above descriptors**; in **dark blue**) and **complementary** methods used to aid interpretation (in **light blue**)"*. **진파랑 = NMR · Molecular dynamics · Impedance spectroscopy · Continuum modelling** / 연파랑 = 회절·PDF, 전자현미경, 진동분광 (figure-read, 픽셀 실측) | **[Famprikis19]** `Fig. 2` (figure-read) | 우리 σ·Ea 는 **UMA MLIP-MD** 산출 (MSD 2–50 ps, NE H_R=1) | ✅ **우리 MD 라인의 등급 근거** — Nature Materials 리뷰가 MD 를 NMR·임피던스와 **같은 칸(직접·정량)** 에 놓는다. 원고·deck 에서 MLIP-MD 를 "보조 계산" 이 아니라 **수송 서술자를 산출하는 1차 기법**으로 쓸 수 있다. ⚠ 단 이건 **방법 등급**의 근거일 뿐 **절대값 신뢰**의 근거가 아니다 — 같은 리뷰가 NE 유효성 유보(위 줄)와 σ 1자릿수 산포를 동시에 말한다. 우리 "σ 절대값 인용 금지" 는 그대로 |
| **★★ In/F 기여가 σ 축에서 실험적으로 분해된다 (dose-matched 2² 요인)** — 같은 host `Li₅.₇PS₄.₇Cl₁.₃` 에서 **pristine 4.8 / In-only(In₀.₀₂) 7.0 / F-only(F₀.₀₆) 4.3 / co-doped(x=0.02) 5.6 mS cm⁻¹** ⇒ **In 이 +2.2(+46 %) 올리고 F 가 −0.5(−10 %) 깎는다**; 가법예측 6.5 vs 실측 5.6 = **상호작용 −0.9(하가법)**. 외부 교차: **Li₆PS₅Cl₀.₃F₀.₇ = 0.71 mS/cm**(Table S2) · [LiGaF] Ga-only 6.4 / F-only 2.3 · [Liu23] Mg-only 3.51→MgF 1.70 | **[LiInF]** `Fig. S8a,b` + 본문 (In-only·F-only 조성이 co-doped x=0.02 의 In·F 량과 **정확히 일치**) | 우리 cascade 는 **양이온 단독 투입 축** — In-only 가 자연히 존재한다 ⇒ **F-only modelc(Cl 4a→F) 를 추가하면 우리도 같은 2² 를 계산 축에서 만들 수 있다**(digest §8e-③). σ 절대값 이식 금지 | **✓ (부호·순위만)** |
| **★ 실험 Arrhenius Ea 앵커 2번째** — `Li₅.₇PS₄.₇Cl₁.₃` 펠릿 EIS **Ea ≈0.303 eV**(x=0, figure-read) / **0.29 eV**(x=0.02, 본문 인쇄 최저값), x 증가 시 **0.337 eV 까지 단조 증가** | **[LiInF]** 본문 + `Fig. 2b` | [LiGaF] 0.28 eV(Li₅.₅PS₄.₅Cl₁.₅)와 **같은 자리**. 우리 MLIP-MD Ea(comp1 0.253 / modelc 0.224 단일궤적 · 3-seed **0.197±0.032**)가 더 낮은 것은 **입계 없는 벌크량**이라 방향 정합 | **✓ (방향)** |
| ⚠ **F 가 σ 를 깎는 기전(논문 서술)** — F⁻ 가 작고(r 119 pm) Li⁺ 와 정전인력이 강해 **"lower polarization rate"** + Li⁺ 배위 국소 왜곡 → **이동 장벽↑** | **[LiInF]** 본문 (+ref [24] Zhao *ACS EL* 2020) | ⭐ **[Fan26] 리뷰 §3.2 가 이 "polarization" 을 *안정성 이득*으로 옮겨 적었다** — 원문에서는 **σ 손해의 이유**다(digest §4d, 리뷰어 **A12**) | **⚠ 인과 역전** |
| **★ 실험 Arrhenius Ea 앵커 (조성 거의 동일)** — `Li₅.₅PS₄.₅Cl₁.₅` 펠릿 EIS **Ea 0.28 eV · σ 5.6 mS cm⁻¹ @25 °C** | **[LiGaF]** 본문 Fig 2A,B (Energy Mater. Adv. 2026;7:0227) | modelc `Li₅.₄PS₄.₄Cl₁.₆` MLIP-MD **Ea 0.224**(단일시드) / **0.197 ± 0.032**(3시드 사다리) · comp1 0.253 | **△ 방향 정합, 정량 일치 주장 금지** — 그들 값은 **벌크+입계 총합**, 우리는 **순수 벌크**라 우리가 낮아야 옳다(0.03–0.08 eV 차, 방향 ✓). 단 우리 Ea는 **600–1000 K 외삽**, 그들은 **25–80 °C 실측** → 원리적으로 같은 수가 아니다. 인용은 *"our bulk MD Ea lies ~0.05 eV below the experimental total-conductivity Ea of the same-composition Cl-rich argyrodite, as expected for a grain-boundary-free bulk quantity"* 까지만. **litdb에서 조성이 이 정도로 맞는 실험 Ea 앵커는 드물다** — 지금까지 우리 Ea는 내부 비교만 가능했다 |
| Cl↑ → σ 2.5→7–10 mS/cm, Ea 0.34→0.22 eV | [Zuo](2.9→7.0), [GG](AIMD peak 14.55 @Cl1.5), [Liu], Excel exp 다수 | D(600K) 3.09→7.90e-6, Ea 0.253→**0.224** | **✓✓** |
| **★ 실험 Arrhenius Ea 앵커 4번째 + Cl/Br 이중 할로겐 축** — `Li₅.₅PS₄.₅Cl₀.₇₅Br₀.₇₅` 펠릿 EIS **Ea 0.32 eV · σ 6.2 mS/cm(30 °C)**; P-자리 **Ta⁵⁺ 6 %** 로 **0.28 eV · 12 mS/cm(1.94×)**. Br 조성 스캔에서 σ 최대점(x=0.75)이 **ΔS_conf/R 최대점(2.08)** 과 일치 | **[Wu26]** `Fig. 2d–f` · `Fig. S3b` · `Table S8` | modelc `Li₅.₄PS₄.₄Cl₁.₆` MLIP-MD **Ea 0.224**(단일시드)/**0.197±0.032**(3시드) · comp1 0.253 | **△ 방향 일치·절대값 우리가 낮음**. 실험 Ea 밴드 **0.28–0.32 eV** 로 [LiGaF] 0.28·[Xu26] 0.292 와 수렴. 우리 값이 낮은 건 **단결정 주기셀(GB 없음) + 600 K↑ 외삽** — ⛔ 대소 비교 금지 |
| ⛔ **[Wu26] 의 cNEB 0.59 eV 는 그들 자신의 실험 Ea 와도 안 맞는다 — 단일 배열 NEB 의 구조적 한계** — 무도핑 inter-cage **0.59 eV** vs 자기 EIS **0.32**(1.8×) vs 자기 ⁷Li SLR NMR **0.14 eV**(4.2×). Ta 치환 후 0.35 eV 로 내려와 "실험과 맞는 것처럼" 보이는데, 그 Ta 셀은 **부피가 22.8 % 팽창**해 있다 | **[Wu26]** `Fig. 3g`(NEB) vs `Fig. 2f`(EIS) vs `Fig. 3f`(NMR) · `Fig. S12c`(부피) | 우리는 NEB 대신 **MLIP-MD 앙상블**(3시드·MSD 2–50 ps·MTO)로 Ea 를 낸다 | **⚠ 방법 교훈**: 무질서계에서 단일 배열 NEB 는 침투 장벽이 아니라 *그 배열의 그 경로* 값. **우리가 NEB 를 쓸 때 배열 앙상블이 필수인 외부 근거** |
| **★★ 실험 Arrhenius Ea 앵커 5번째 — 단, *우리가 고쳐서* 얻었다 (인쇄값이 ln10 배 작다)** — `Li₆PS₅Cl` 시판 펠릿 EIS 7점(298–358 K). **인쇄 Ea 12.04 kJ/mol(=0.125 eV, LPSC) · 12.42(=0.129, LPSC–FG)** ⇒ 픽셀 재적합(R²=0.9956/0.9958) 결과 **27.76 kJ/mol = 0.288 eV · 28.64 = 0.297 eV**, 재적합/인쇄 비 **2.306 · 2.306** vs **ln10 = 2.3026 (0.13 % 일치, 두 계 모두)** → **log₁₀σ 기울기에 ln10 을 안 곱한 것**이 확정. log σT 관례로는 **0.316 / 0.325 eV**. σ(298 K) **3.79 → 3.00 mS/cm (FG 가 −21 %)** — 본문은 σ 절대값을 한 번도 안 쓰고 "similar" 라고만 한다 | **[Ling26]** `Fig. S6a` (우리 재분석: digest §4.5·§11.1) | comp1 `Li₆PS₅Cl` MLIP-MD(UMA) **Ea 0.253**(단일궤적) · modelc 0.224 / 3-seed **0.197 ± 0.032** | **△ 방향 정합, 정량 일치 주장 금지** — 그들은 펠릿(벌크+입계) 실험, 우리는 입계 없는 벌크 MLIP-MD 를 600–1000 K 에서 외삽. 우리가 0.03–0.06 eV 낮은 것은 **예상된 방향**. 🔑 **[LiGaF] 0.28(Li₅.₅PS₄.₅Cl₁.₅) · [LiInF] 0.303/0.29(Li₅.₇PS₄.₇Cl₁.₃) · [Wu26] 0.32(Cl/Br) · [Ling26] 0.288(Li₆PS₅Cl, 재정정)** ⇒ **"argyrodite 실험 Ea ≈ 0.28–0.32 eV" 앵커가 4편으로 굳었다.** ⛔ **인쇄값 0.125 eV 인용 절대 금지** |
| 🔁 **로그 밑 혼동이 이 계열의 반복 결함 — 2번째 적발** | **[Ren26]** Fig 3d/3e y축 `ln(D)` 라벨인데 실제는 log₁₀(D) (digest §20) · **[Ling26]** `Fig. S6a` Ea 가 ln10 배 작음 | 우리 규약: Arrhenius 는 항상 **자유절편 D + MSD 창 2–50 ps 고정**, 기울기→Ea 변환 상수를 코드에 박아 `tools/convention_check.py` 로 감시 | **⚠ 문헌 Ea/D 를 인용하기 전에 축 라벨과 기울기를 반드시 자체 재적합할 것** — 두 편 모두 재적합해야 정상값이 나왔다 |
| ⛔⛔ **AIMD 300 K·20 ps 로는 확산 영역에 못 들어간다 — 정량 반례** — [Wu26] 은 `Fig. 3h` 에서 300 K·20 ps·1×1×2·1시드 AIMD 의 Li 확률밀도로 *"expanded and interconnected 3D percolating network"* 를 주장한다. **논문 자신의 NEB 장벽으로 20 ps 안 hop 기대값 ≤ 0.055회**(무도핑은 ≤3.5×10⁻⁵회), **실험 σ 12 mS/cm 로 역산해도 0.28회**; NE 로 계산한 **MSD(20 ps) ≈ 0.10 Å² (√MSD 0.32 Å)** = doublet 거리(≈2 Å)의 1/6 | **[Wu26]** SI 계산절 + `Fig. 3h` 캡션(*"1×1×2 cell … at 300 K"*) · 우리 검산 | 우리 규약 **600/800/1000 K · prod 200 ps · MSD 창 2–50 ps · MTO 정본 · 3시드** (~~β̄ ≥ 0.80~~ ⛔ **폐기 2026-08-27** — `HZ-beta-hard-gate` SUPERSEDED, 거짓탈락률 50 %. 현행 판정축은 **D_inc plateau · 창 안정성 · 홉 수**) (`db/properties/lpsocl_beta_registry.json` · `kb/concepts/beta-gate.md` §7-8b·§7-8e) | **⛔ 인용 금지**(그 그림은 확산이 아니라 열진동 번짐) + **★ 우리 온도 선택의 정량 방어선**. 우리는 상자만 3× 키워도 D 가 1.65–1.70× 움직이는 걸 봤다 (`kb/results/lpsocl_box_size_600K_2026_08_18.md`) |
| **RE³⁺+O 공도핑 σ의 농도 2-영역 — 희석(x=0.025) 1.25×↑ / 고농도(x=0.1) 0.61×↓** (6.99→8.75→4.27 mS/cm, Ea 0.292→0.278→0.312). 단 Arrhenius 분해(우리 유도)는 **희석 최적점에서도 σ₀ 0.73×(감소)** — 향상분 전부 Ea 항, "carrier +2Li/Nd·채널 확장" 서사와 자기모순. ⚠ 오차막대·반복수 0, LiCl 상분리 동반 | **[Xu26NdO]** Fig. 1d,f,g (exp, 계산 0) | 우리 UMA x=0.2 Track1(Nd@Li): σ300 **0.52×** = D0 0.65 × n_Li 0.90 × Ea 0.88 — **prefactor-지배 감소, 고농도 영역과 방향·크기 수렴**([Yang25] La-O 0.65×에 이은 2번째 실험 앵커, `li_transport.json` experimental_validation 후보). 희석(x≈0.025) 영역은 우리 미계산 — 대형셀 멀티시드 MD(P4) 후보 | **✓(고x·σ₀ 방향)·?(희석 극대)** |
| **🛡 우리 단결정 주기셀 계산의 문헌 방어선 (GB 기여)** — *"For the sulfide and halide SEs with high ionic conductivity, **the GBs do not create much hindrance to Li-ion migration**"* — 고변형성 덕에 **냉간가압 100–300 MPa**만으로 결정립이 밀착, 총 σ 10⁻⁴–10⁻² S/cm, GB 반원이 따로 안 생김. 대비: 산화물은 GB가 지배(LLTO 벌크 10⁻³ → **총 10⁻⁵ S/cm**; LATP 1자릿수↓; 예외 Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂ GB≈벌크≈10⁻⁴). ⚠ 저압(50 MPa)이면 기공률↑ → GB 임피던스↑ | **[Miao23]** §2.1 (+`Fig. 2a`) — **정성 서술, 자체 측정 아님** | 우리 BVSE·UMA-MD는 **전부 GB 없는 단결정 주기셀** | **○ 정당화 근거로만.** "황화물은 GB 기여가 작아 단결정 계산이 총전도도의 좋은 대리"라는 문장을 이 리뷰로 방어할 수 있다. ⚠ **[Kim24 MTP argyrodite GB]** digest(실제 GB 계산)와 **교차확인 후** 사용 — 리뷰 자신이 *"there are **few reports** on the effect of GBs in sulfide and halide SEs so far"* 라고 못박는다(= 근거가 얇다) |
| **σ↑·Ea↓ 레버 = Cl만이 아니라 *무질서+Li⁺-carrier 일반*** — **Cu²⁺/P⁵⁺ 헤테로치환(Li⁺ 추가·S²⁻ 전하밀도↓) + Br→4a/4d(음이온 무질서↑)** 도 σ 5.3→**10.3 mS/cm**·Ea 0.295→**0.239 eV**(LPSC-P→LPSC-CB). x>0.1 불순물(LiCl/CuCl₂/LiBr)서 σ↓(용해한계) | **[Li25]** (CuBr₂ dual-doping, exp+DFT) | D(600K) 3.09→7.90e-6, Ea 0.253→**0.224** (우리는 Cl만으로 같은 trend) | **✓ trend 일치, 기전 일반화**: "Cl↑"든 "Cu+Br"든 *무질서·extra-Li⁺*가 공통 레버 → 우리 comp1→modelc Ea drop와 같은 방향. 단 변수 다중(Cu·Br 분리 안 됨)·실험 EIS vs 우리 AIMD라 절대값 비교 금지. Excel exp#9(Cl/Br 24 mS/cm)와 같은 mixed-halide 줄 |
| **같은 레버, *우리 comp1 모체에서 직접* (Cu+Cl)** — **CuCl 이원 도핑**(Cu²⁺→P⁵⁺ 4b·Li⁺ 추가·24g bridge + Cl⁻→4a/4c 무질서 + **Li₆S cage 내 48h–48h 거리 3.298→2.997 Å 단축**) → **Li₆PS₅Cl 1.11 → 4.34 mS/cm**·Ea ~0.30→**0.25 eV**(x=0.1, 550 °C·15 h). x>0.1 불순물(Li₂S/LiCl)서 σ↓(Cu 용해한계, 화산형). ball-mill-free 고상 | **[Taklu]** (CuCl dual-doping, exp + DFT Li-path) | D(600K) 3.09→7.90e-6, Ea 0.253→**0.224** (우리 Cl만 modelc로 같은 trend) | **✓ trend 일치 + *모체가 우리 comp1과 동일(Li₆PS₅Cl)***: [Li25](Cl-rich 모체)와 달리 **출발 host가 comp1 그 자체** → "도핑이 σ↑·Ea↓" 비교축이 가장 깨끗. Cl만/Cu+Cl/Cu+Br **세 경로 모두 *carrier↑·anion-disorder↑·cage-Li 거리↓*** 공통 레버 = 우리 comp1→modelc 일반화. **48h-Li 거리 단축**은 우리 inter-cage hop 멘탈모델과 같은 그림. ⚠ 변수 다중(Cu·Cl 분리 안 됨)·실험 EIS vs 우리 AIMD·DFT functional 미상 → 절대값 비교 금지 |
| **σ↑·Ea↓ 레버 = halide 종류 아니라 *총량·비율·무질서·이동채널 부피*** — **Cl–I ≈ Cl–Br σ(같은 X/Cl 비율, 둘 다 ~10 mS/cm 등량)**; I/Cl=0.75:0.75 등량서 **σ=23.5 mS/cm·Ea 0.18 eV**(Li **Voronoi 다면체 부피 9.39 Å³ 최대=넓은 채널**); I 과다(I₁.₅)면 5→4배위 회귀로 부피↓→**σ 4.3**(화산형). Li₆PS₅Cl 1.33→Li₅.₅PS₄.₅Cl₁.₅ **18.86 mS/cm**(AIMD 300 K). 혼합 검증 Li₅.₄PS₄.₄Cl₁.₄I₀.₂ AIMD **15.79** ↔ 실험 17 | **[Rao]** (Cl–I, **순수 DFT+AIMD**, 실험 0) | D(600K) 3.09→**7.90e-6**·Ea 0.253→**0.224** (우리 Cl만으로 같은 trend) | **✓✓ trend 일치 + 기전 일반화**: Cl·Br·I 어느 할라이드든 *등량 비율·무질서·채널부피*가 σ 지배(halide 종류 아님). **🔑 Arrhenius 축은 같지만 힘 계산이 다름 — 상대는 AIMD, 우리는 MLIP-MD(UMA)** (그들 절대 σ 18.86은 고온 외삽 과대=우리 UMA 3–5× 과대와 같은 결, **Ea·비율만 신뢰**). **Li Voronoi 부피=σ** 상관 = 우리 `migration_volume_fraction`·cage descriptor와 동일 물리 |
| **σ↑·Ea↓ 레버 = halide 아니라 *양이온+음이온 다중치환 일반* (Sn⁴⁺·Sb⁵⁺·I⁻ 삼중)** — Sb-기반 LSSSI를 P-기반 LPSC에 *구조통합*: **Sn⁴⁺ aliovalent(Li⁺ carrier↑)+Sb/Sn–S가 S–Li 약화+격자팽창(a 9.851→9.967 Å)+무질서** → **Li₆PS₅Cl 3.4 → 5.2 mS/cm**·Ea 0.29→**0.25 eV**(LPSC-0→LPSC-0.05). DFT Li 장벽 intra **0.873→0.496**·inter **0.976→0.592 eV**(inter>intra=율속). x≥0.07 Sb₂S₃/SbSI 불순물서 σ↓(용해한계, 화산형) | **[Ma24]** (LSSSI Sn/Sb/I tridoping, exp+DFT보조) | **comp1 σ_NE 3.35 ≈ Ma LPSC-0 3.4**(우연 근접); D(600K) 3.09→7.90e-6, Ea **0.253→0.224** (우리 Cl만 같은 trend) | **✓ trend 일치, 기전 일반화 + 모체=comp1**: 모체 LPSC-0 = **Li₆PS₅Cl(=comp1)** 정확 동일 → "도핑이 Ea↓"(0.29→0.25)가 우리 Cl-rich(0.253→0.224)와 *서로 다른 도펀트인데 같은 방향*. **inter>intra hop = 우리 framework-immobile inter-cage 율속·[Perc]/[Dyre] 병목과 정성 일치**. ⚠ **DFT 파라미터(code/functional/k/무질서/NEB) 전부 미공개=재현불가**; 정적 단일경로 장벽(0.5–1.0 eV)≫우리 AIMD Ea(0.22–0.25) → 절대값 비교 금지(정적 단일경로 과대). 격자팽창 방향은 우리 Cl-rich(수축)와 *반대*. **[Taklu]/[Li25]와 같은 USTB·Ping Li 그룹의 multi-doping 자매** |
| **⚠ 반대방향 레버: RE³⁺+O 도핑은 σ를 *깎는다* (σ-비용)** — La₂O₃ x=0.04서 σ 9.58→**6.23 mS/cm(0.65×)**·Ea 0.238→**0.254 eV**(+0.016); x 시리즈 단조악화(0.02/0.05/0.10 → 6.78/5.15/3.45·0.249/0.259/0.289), x≥0.05 2차상 급락. 저자 기전: **P–O 강결합=국소장벽(엔탈피)↑** + La³⁺ 왜곡·공공=엔트로피↑ (TST 보상 서사) | **[Yang25]** (La₂O₃ dual-doping, exp) | **Nd₂O₃: σ300 0.52×·D 0.62×, Ea 0.224→0.227(불변)** — 우리도 RE-O 도핑=σ 희생 | **✓ 방향 일치(RE-O 도핑=σ 비용) — 우리 Nd σ-drop의 실험 자매**. 단 미시분해 다름: Yang은 Ea↑가 drop 절반 이상 설명(exp(−ΔEa/kT)≈0.54×≈관측 0.65×), 우리 Nd는 **Ea 불변·prefactor/connectivity blocking**([Perc]/[Dyre] 언어) — 자리(La@4b/P vs Nd@Li)·농도(x0.04 vs 0.2) 차이 가능성. 절대값 비교 금지(EIS vs MLIP-AIMD). σ↑ 도핑행([Li25]/[Taklu]/[Ma24])과 달리 **이 행 = "interphase를 사려고 σ를 파는" 도핑** — 축 E·F와 한 몸 |
| σ 기전 = inter-cage Li jump (Cl 4c 무질서) | [GG] (Li 확률밀도, Fig 1e,f) | 우리 percolation/inter-cage 분석과 동일 물리 | ✓ |
| **inter-cage = dc 율속의 *2011 BVSE 1차 출처* + comp1(Li₆PS₅Cl 동일조성) σ 외부 anchor** — Li₆PS₅X(Cl/Br/I) BVSE 경로 위계: intra-cage hexagon **0.15–0.18 eV**(빠름·non-limiting) → extended cage **0.22–0.25** → **inter-cage interstitial 0.27–0.35 eV = long-range(dc) 율속**. 결정질 σ **Cl 1.9 / Br 6.8 (10⁻³ 액체급) ≫ I 4.6×10⁻⁷**(3–4 자릿수); dc 율속 장벽은 Cl/Br/I 모두 **~0.3 eV로 비슷**한데 σ는 I만 낮음 → *경로 topology·carrier connectivity*가 지배(장벽 높이만 아님). anion disorder+interstitial 가용성이 inter-cage 연결을 켬 | **[Rao11]** (Rao&Adams 2011, **bond-valence 경험적 force-field**, exp 합성/XRD/EIS; `papers/rao2011_argyrodite_se_studies_bvse.md`) | comp1=**Li₆PS₅Cl 동일조성** σ AIMD RT 외삽 ~3.35 mS/cm ↔ **Rao 실측 1.9 mS/cm(같은 10⁻³ 차수)**; Ea AIMD **0.2532** vs Rao 임피던스 0.38/BV dc 0.35; D 3.09→7.90e-6·Ea 0.253→0.224(우리 Cl 증량) | **✓✓ 우리 inter-cage 서사의 *2011 1차 출처(BVSE 경로 해부)* + comp1 외부 실측 anchor**. [GG]/[Liu] AIMD 확률밀도와 *방법 다르나 같은 위계*. **단 BV Ea ≠ AIMD Ea(척도 다름)**: BV=relaxation 무시(저자 명시)·Ea 방법마다 갈림(NMR 0.04/임피던스 0.32/MD 0.30/BV 0.33)→우리 AIMD가 더 엄밀. Rao=*할라이드 종류* 축(Cl/Br/I), 우리 modelc=*Cl 함량* 축 → "disorder→inter-cage 연결→σ↑" *같은 레버, 다른 수단*. I=dc σ 약함은 [Rao2025](I=상안정/계면 레버지 전도 아님)와 일관. **σ는 어닐 결정질이 본질**(ball-milled trend는 I 최고로 반대=비정질 혼합) |
| **halide σ의 *격자 무름 축* — 무른 격자는 E_A↓ *AND* prefactor↓ → σ 최적은 *중간강성*(soft≠always better)** — Cl→Br→I(더 분극성) 격자 무름(speed of sound v_long 1480→1130 ms⁻¹ **−24 %**·Debye ν_D 2.45→1.90×10¹² Hz **−22 %**) → **E_A↓ 0.46→0.30 eV** *동시에* **prefactor σ₀↓ 2.7×10⁷→10³ KScm⁻¹**(Meyer–Neldel 보상, Fig S2) → **σ 최적 = Cl₀.₅Br₀.₅(=comp2) ~2 mS/cm**(Cl 1.3e-3·Br 1e-3·**I ~1e-6**). 순수 I는 무질서 0(I⁻ 2.2 Å≫S²⁻)→E_A 반등(0.38)→저전도. prefactor = carrier·a₀²·**attempt freq ν₀(∝ν_D)**·e^{ΔSm/k}(eq 6) | **[Kraft]** (2017 JACS, 중성자/PDF/임피던스/PE·RUS, **DFT 없음**, 외부) | comp1 MD Ea 0.253 *(멀티시드 진행 참고)*; comp2 σ/Ea 미측정(ε∞ 3.80·elastic 진행중); Nd σ-drop = **D0 prefactor 0.65×·Ea 불변** | **✓✓ 방향 일치 + prefactor 물리 앵커**: (1) 무름·무질서→Ea↓ = 우리 comp1→modelc(0.253→0.224) 방향; (2) **Kraft가 comp2(Cl₀.₅Br₀.₅)를 σ 최적으로 지목** = 우리 comp2 계산의 *기대 위치*; (3) **"prefactor가 σ를 지배·softer≠better"(σ₀ 4자릿수 변동) = 우리 Nd σ-drop이 Ea 아니라 D0(0.65×)로 설명되는 Meyer–Neldel 물리의 실측 앵커**. ⚠ **절대 E_A 비교 금지**: Kraft 0.46=*total(bulk+GB) 임피던스* ≫ 우리 bulk MD 0.253=**방법차**(GB포함; Schlem 0.25·Rao2011 0.38·NMR과도 층 다름), 방향만. 속도/Ea/σ₀=figure-read(SI 표 없음). Kraft=할라이드 *종류* 축(Cl↔Br↔I 교환) / 우리 modelc=Cl *함량* 축=별개 |
| **intra-cage→inter-cage 전이 = Cl-rich σ↑ 물리 (직접 시각)**: AIMD Li 확률밀도 — **LPSCl=Li₆S cage 안 갇힘 / Li₅.₅PS₄.₅Cl₁.₅=inter-cage 경로 활성화·전 방향 비편재화** (MSD ≈3× 등방). 무질서 정량 = Rietveld 4d S²⁻/Cl⁻ **13.3→61.7 %**(Klerk 예측 확인). σ as-milled도 2× (1.10→2.13), 최적 **8.0 mS/cm@450**(LPSCl 2.62@550). **단 LPSCl σ=결정화도만 / Cl-rich σ=결정화도+무질서** | **[Liu]** (Fig 2e–g·S5, exp+AIMD) | comp1→modelc D(600K) 3.09→**7.90e-6**(2.6×)·Ea 0.253→**0.224**; 우리 inter-cage 멘탈모델 | **✓✓ 우리 inter-cage 서사의 *문헌 그림 증거***. [GG] 확률밀도와 같은 물리. modelc도 SQS 아닌 단일배열(Liu=enumerate→lowest-Ewald, 우리와 같은 철학). 절대 σ는 EIS RT vs 우리 AIMD 외삽 → Arrhenius로만 |
| **halogen 4a/4c(=4d) site disorder = 거시 확산의 *필요조건* + 최적은 양 끝이 아닌 내부점(4c-Cl 75 %) — disorder-AIMD 원전** — Li₆PS₅Cl 인공 배열: **all-4a(I 모사)=intercage 점프 0**(케이지 고립, Li₆PS₅I가 모든 T에서 거시 확산 0인 이유=자리 분포)·**all-4c=doublet 붕괴(≈2×10⁹ s⁻¹)로 새 율속** → 두 자리 걸친 분포만이 3종 점프를 모두 살림. 분포 스캔(0/25/50/75/100 %, 450 K, SI Table S2 정밀값): intercage 단조↑(−/1.79/3.12/6.20/14.36×10¹⁰ s⁻¹)·doublet 단조↓(103.68→0.21)·intracage 평탄 → **min-rate 최대 = 75 %(4a:4c=1:3), 50:50 대비 limiting rate 6.20/3.12=1.99×·σ_J 2.00×**("σ 2배" 예측, 열처리로 실현 가능 ref Rao2013; σ_J 기준 300/600 K도 75 % 최고). 국소 기전 = **Cl 케이지 5 Li vs S 케이지 7 Li**(RDF, 공공이 Cl 옆 응집→빈 doublet 상존=intercage 착지점); vacancy vs halogen 가상조성 분리(Li₆PS₆·Li₇PS₅Cl) → **둘 다 필요**(intercage rate 유사, doublet/intracage만 상이). 할로겐-rich **Li₅PS₄X₂**(4a+4c 완전 X)는 σ ≈ Li₆PS₅Cl/Br(**I₂도!**) | **[Klerk]** (2016 AIMD 원전, VASP/PBE/52원자/100 ps, 실험 0; `papers/deklerk2016_diffusion_site_disorder_argyrodite.md`) | **comp2 disorder ensemble**(같은 52원자 단위셀, Cl·Br↔free-S 라벨스왑 d=0.5/1.0×**cfg 3개**, UMA anneal 700 K 20 ps+FIRE relax 후 NVT 600/800/1000 K 200 ps; ordered champion Ea 0.276 ≥ comp1 0.253) · disorder_ensemble comp1 **d=0.5 Ea 0.177±0.027**(ordered frozen artifact 1.17) · **li_percolation F\* comp1 0.191 → modelc 0.078 eV**(600 K Li-밀도 PMF: anti-site가 inter-cage 평탄화) | **✓✓ 방향·물리 정면 일치 + 방법론 원형**: ① "ordered/한쪽-몰림=frozen"(all-4a intercage 0)을 우리 d=0 아티팩트·comp2 ordered가 독립 재현; ② 그들 min-jump-rate 극대화 = 우리 F* 최소화(같은 inter-cage 병목의 rate vs PMF 두 척도); ③ vacancy+halogen 합작 = 우리 dual_mechanism(장벽↓+prefactor·carrier↑). **⚠ 캐비앳 3**: (a) 그들=진짜 AIMD(힘=DFT) vs 우리=MLIP-MD(UMA) — "둘 다 AIMD" 금지, σ·Ea는 소환값(σ_J 300 K ≈1 S/cm=bulk 상한, 실측 대비 수 자릿수↑=우리 UMA 3–5× 과대와 같은 캐비앗 계보); (b) **75 % 최적은 분포당 단일 배열·σ_J(limiting-rate) 지표 조건부 — σ*_MSD는 600 K 역전(0.91<1.01)·2024 MTP-MLIP(INDEX 계산#8)는 25 % 보고=지표·방법 의존** → 안전 인용은 "양 끝 나쁨·중간 최적"까지(우리 relaxed multi-config ensemble이 이 single-config 모호성을 겨냥; un-relaxed 스왑 σ₃₀₀ ~70 mS/cm 아티팩트 v1 사례가 위험 실증); (c) Klerk Ea 0.20–0.25=eq2(ν₀=10¹³ 가정 로그 변환)≠아레니우스 기울기 → 우리 0.253/0.224와 정의 다름, 서열만; (d) **σ_J는 τ_min(3종 최솟값) 한 값만으로 환산**됨을 우리가 eq3+5 재조립으로 확정(2026-08-03 SI 재검증, 11 케이스 1–4 % 일치) — **doublet이 율속인 all-4c에도 케이지-간 7.0 Å를 그대로 적용**하므로 100 % 배열 σ_J(450 K 0.18)는 상한 환산값(실변위 1.9 Å 기준 ≈1/13.6). all-4c 인용은 절대값 말고 **"75 % 대비 σ_J 28× 낮음"** 형태로 |
| **Cl *함량* 축의 실험 원전 — σ ~4×·Ea↓·D*↑·협동성↑, 단 고용한계 x=0.5** — Li₆₋ₓPS₅₋ₓCl₁₊ₓ: σ(cold-press 2 t·total·298 K) 2.5→4.2→5.6→**9.4±0.1 mS/cm**(x=0.5, 거의 지수적)·**소결 12.0±0.2**; **Ea EIS 0.34→0.29 ≡ PFG 0.35→0.29(1)**(이중 측정 일치 = bulk-지배 트렌드 근거); **PFG D*(300 K)=1.01×10⁻¹¹ m²/s**(LGPS PFG의 ~5배 실측); **Haven ratio 0.3→0.23**(x=0.375→0.5 구간서 하락 = 공공 매개 협동 강화; c=4/cell 하한 규약); 기작 3중 = 정전 약화(⁷Li MAS "LiCl-like")+Li 공공(48h 0.456)+자리 무질서(61→83 %). **x>0.5 LiCl 석출 → x=0.6(=우리 modelc 조성) σ 3.3 급락** — 단 후속 공정(박막 10.8·RTA·Nazar 2024 Cl1.7 11.4–17)은 넘어섬 = **고용한계·무질서 = 공정 변수** | **[Adeli]** (2019 실험 원전, 중성자+EIS+PFG; `papers/adeli2019_halide_substitution_boosting_argyrodite.md`) | comp1→modelc **D(600 K) 3.09→7.90×10⁻⁶ cm²/s(2.6×)·Ea 0.253→0.224**(MLIP-MD 단일궤적); 우리 σ 환산 = NE(**Haven=1**) — H_R 미계산 | **✓✓ 우리 comp1→modelc 축(Cl *함량*)의 실험 원판** — [Kraft]=할라이드 *종류* 축·[Klerk]=disorder-AIMD·**[Adeli]=Cl 함량 실측**으로 3축 완성. Ea 방향·크기급 일치(실측 Δ−0.05 vs 우리 Δ−0.029; **Adeli Ea는 PFG 짝으로 bulk-급 신뢰 → Kraft total 0.46보다 우리 bulk MD에 훨씬 근접한 문헌층**). **🔑 Haven 0.23–0.3 = 우리 "NE 절대 σ 인용 금지" 규율의 실측 근거**(협동 이동 시 σ_true≈σ_NE/H_R≈3–4×σ_NE; 단 H_R 절대값은 캐리어-수 규약 의존 → 우리 MD Haven 계산 시 규약 명시 후 대조). ⚠ **modelc 조성(Cl1.6)은 이 공정 고용한계 밖**(LiCl 석출 실측) — 우리 셀은 "단일상 가정" 명시 필수; 절대값 혼합 금지(EIS total vs MLIP-MD bulk); SOF(4a 0.615/4c 0.834)는 modelc decorate 정량 대조의 ground truth(액션) |
| **inter-cage jump = 거시 σ 율속 (NEB+AIMD 동시·이론 4번째 근거) + anion-site 결합차수 기전** — **준층상 argyrodite(P2mm)**서 inter-cage(=층간) hop이 거시 σ 율속(**NEB Ea 0.12 ≈ AIMD 0.088 eV**, intra-cage·doublet < inter-cage). **왜 = 4c-halide 약결합(Cl–Li Mayer bond order ≤0.5×S–Li)+4a-S 고활성** → halide-cage 층 궤적 widening·연결↑ → **σ_up(halide층) > σ_down(S층), 최대 2.07**(SnS₄·I). σ Cl>Br>I·**PSe₄ 최고(약결합)·GeS₄ 최저(강결합·고원자가)**. 2축 치환 σ ↔ **Mayer bond order 균일성** 상관 | **[Liang]** (Bolong Huang 2025, **순수 DFT+AIMD+NEB+Mayer/ELF/IRI**, 실험0) | comp1→modelc D(600K) 3.09→7.90e-6·Ea 0.253→**0.224**; MLIP-MD Ea 0.2532(⚠ Schlem 귀속 철회 2026-07-28 — 실험 LPSCl Ea 0.29–0.46 eV 범위); 우리 inter-cage 멘탈모델·`migration_volume_fraction` | **○ *원리* 일치 (anion-site 기전·inter-cage 율속) — *수치/구조 직접등치 금지***. **🔑 [Rao11]BVSE(inter-cage dc 율속)·[Perc]site-perc(망 연결)·[Dyre]hopping(병목)에 *이론 4번째 근거*(AIMD 궤적+NEB)**. anion-site 결합차수 기전 = 우리 "S/Cl이 어느 자리에 → σ"의 *Mayer 정량판*. ⚠ **준층상(4a/4c)≠우리 cubic F-43m(4a/4d)**: **inter-layer≠inter-cage·비등방≠등방**; Liang Ea 0.088/0.12 = 준층상 halide층의 *유난히 낮은* 값(≠우리 0.25 입방평균·≠Rao11 0.27–0.35)=widening+외삽+방법차. σ=AIMD 고온외삽 절대값(1.18 S/cm=과대, 우리 UMA과대와 동급)→**Ea·ratio·trend만**. halide 트렌드 Cl>Br>I는 [Rao11] 결정질 σ(I 최저)와 *방향 일치* |
| **Li₆PS₅Cl = S²⁻/Cl⁻ 완전 disordered → 가장 빠른 Li⁺** (Cl이 X=Cl,Br,I 중 disorder 최대) | **[Rupp]** p.9 | comp1→modelc D↑·Ea↓ (Cl-rich 빠름) | **✓ 구조적 근거** (Cl disorder = σ↑ 원인) |
| AIMD setup (300 eV/Γ/NVT) | [GG] | 동급 | ✓ 방법 정합 |
| **device σ ≠ bulk σ: 손실 원인 = 미세구조(공동), bulk 결정 아님** (시트 1.44 ↔ 펠릿 3.2 mS/cm; 공동 채우면 2.23=155 %) | **[KimICCF]** (Li₆PS₅Cl=comp1, GeoDict digital-twin) | 우리 bulk AIMD RT-외삽 σ ≫ 실현 σ | **🔑 개념 평행**: 우리 "σ는 interphase·percolation 변수"와 일치. **둘 다 "bulk 잠재력 ≫ device σ"** → 미세구조가 병목. 절대값 직접 비교는 금지(bulk 단결정 vs 시트 실측) |
| **device 전자전도 σ_e = 코팅 형상·도전재 분포가 지배(양 아니라 연결성)** — 양극 복합체 σ_e가 3,000배 변동(3.3×10⁻²↔1.0×10⁻⁵ S/cm), 활성표면적 1.00↔0.51; **CA 차원(0D Super P 나쁨 / 1D VGCF 좋음)** 이 레버 | **[KimCA]** ⭐ (Li₆PS₅Cl=comp1, 계산無) | 우리 bulk σ_e 미측정(gap 2.066/2.099 eV=wide-gap insulator); device σ_e 못 봄 | **🔑 개념 평행(양극측)**: ASSB 성능 레버 = 코팅 형상·전자전도 경로(미세구조), bulk 결정 아님 → 우리 "lever=interphase/microstructure" 결론의 cathode-side 보강. ⚠ **계산 0 → DFT 수치 비교 금지**; σ_e 절대값도 device(복합양극)라 우리 bulk와 대상 다름 |
| **device 계면저항 = 코팅 *화학 호환성*이 지배, σ 아님** — 할라이드 코팅 σ는 LIC 1.12 > LZC 0.51 > LYC 0.37 mS/cm인데 계면저항은 **LZC 20.1 < LYC 30 < LIC 55 ≪ bare 74.4 Ω·cm²**(역경향)·수명도 LZC 91.2 > LYC 87.3 > bare 83.1 > **LIC 80.8 %**(σ 1등이 꼴찌). 논문 명시 "cannot be explained in terms of ionic conductivity" | **[Cha]** ⭐ (Li₆PS₅Cl=comp1, 계산無) | 우리 σ=bulk AIMD; device 계면저항 못 봄 | **🔑 개념 평행(양극측, 세 번째)**: 성능 레버 = 계면 *화학 호환성*(dual compatibility), bulk σ 아님 → [KimICCF](sheet σ)·[KimCA](양극 σ_e)에 이어 "lever=interphase, not bulk σ"의 **cathode-side 세 번째 실험증거**. ⚠ **계산 0 → DFT 비교 금지**; Zr 우리 hull에 없음 |
| **σ는 *국소 hop이 쉬운가*가 아니라 *운반망이 침투(percolate)하는가*가 지배** — 운반이온 농도 x>site-perc 임계 pc(FCC≈0.2)서 σ 급등, 침투클러스터 이온만 mobile (σ≫σ_NE 2 orders=cooperative knock-on) | **[Perc]** (외부·theory framework only, `papers/ishikawa2025…md`) | 우리 cascade=random-substitution 그 자체; `migration_volume_fraction`=침투 저장벽 부피, `dopant_blocking_fraction`=망 site-dilution | **🔑 framework 평행 (NOT numeric)**: 우리 "σ=connectivity 변수, 국소 hop 아님"의 *이론 백본*. **단 pc=0.2 우리계 직접이식·우리 mS/cm 등치 금지**(rock-salt/Te vs argyrodite/PS₄·미니멀 퍼텐셜·환원단위); 아래 framework note 참조 |
| **무질서 6배열 *전수* MTP-MD: ordered=사실상 부도체·disordered=superionic (3–4자릿수 갭) + "MLIP σ 절대값=훈련 functional 각인"** — Li₆PS₅X 6배열(0/25/50×2/75/100% X@4c): **ordered(0·100%) Ea 339–529 meV·σRT ≤0.12 mS/cm vs disordered(25–75%) 151–256 meV·13–42 mS/cm**(Cl; MSD caged vs free); 같은 7200 훈련 스냅샷을 functional만 바꿔 학습하면 **σ80%bulk 4.19(PBE)/0.55(PBE-D3)/2.46(optB88-vdw) = 8배 갈림**, PBE·D3는 100%-ordered를 3.7로 오판 → optB88만 site-disorder·실험(2.3–2.5) 동시 재현. 27셀 Boltzmann random supercell **σ100% 11.5 → χc^7.14 결정화도 보정 2.3**. **PS₄ 회전·진동 고정 시 D600K −50%(disordered)/−18%(ordered)** = 음이온 동역학이 Li 확산 증폭(단 순위는 배열이 결정) | **[KimMTP]** (MTP-MLIP 3×3×3·NPT 10 ns·350–500 K, 실험 0; `papers/kim2024_mtp_argyrodite_disorder_gb.md`) | disorder_ensemble: **ordered d=0 frozen(Ea artifact 1.17)·disordered d=0.5 Ea 0.177±0.027 eV**; comp1(준질서 자연셀) 0.253→modelc 0.224; modelc σ_NE ~14 mS/cm(**절대값 인용 금지 규율**) | **✓✓ 방향 정면 일치 + 우리 규율의 외부 정면 증거**: ① ordered=frozen/disordered=fast 이분법을 6배열 전수로 정량 — [Klerk] AIMD와 같은 결론의 MLIP 규모화판(단 최적 배열 Klerk 75% vs KimMTP-optB88 25% = **방법 의존**, "양 끝 나쁨·중간 최적"까지만 안전) ② **functional별 σ80% 8배 = "MLIP-MD 절대 σ는 훈련 PES 각인" → 우리 UMA 절대 σ 불인용·Ea/비율만 규율의 외부 근거** ③ 원값 11.5 vs 실험 2.3 gap을 χ^7.14 경험 보정으로 해소 = 우리는 미보정+불인용(같은 병, 다른 약; χ식 이식 금지) ④ **⚠ 모델 완전질서 Ea 0.45–0.53 eV ≫ 우리 comp1 0.253** → comp1 값은 '실험 LPSCl(내재 무질서 60–70%)'급이지 '완전질서 모델'값이 아님 — li_transport의 "Schlem ordered 0.25 일치" 앵커도 같은 주의 필요(Schlem 원문 미확보·위시리스트 유지) ⑤ PS₄ 회전은 우리 framework-immobile(병진만 확인)과 모순 아님(회전≠병진) — 우리 UMA 궤적에 S-궤적+PS₄-고정 분석 이식 가능(도구 아이디어) |
| **GB = σ 지연의 원자적 기원: Li *정전기 축적* (구조붕괴 아님)** — active-learning MTP로 **Σ5[100](021) tilt GB(γ≈1.35 J/m², tilt<twist 최저)** >13,860원자·NPT 350 K·10 ns: **D_GB 5.4×10⁻⁸ = 0.3× bulk 1.8×10⁻⁷ cm²/s**·영향권 **10–20 Å**·전 방향 감소; PS₄/단일음이온 골격은 유지되고 대신 GB의 **PS₄³⁻+S²⁻ 인접 음전하가 Li을 bulk→Far→Near→GB로 순차 유입·축적**(Li count 열지도·Li–Li RDF 첫피크 단축); 축적 진행 시 D 추가 하락(bulk-영역 D 100 ps 3.4e-7→10 ns 1.6e-7 = **단시간 MD는 D 2× 과대**); 처방 제안 = **고산화수 도핑으로 S 전하↓(solid-electrolyte inductive effect)** | **[KimMTP]** (`papers/kim2024_mtp_argyrodite_disorder_gb.md`) | **우리 GB 계산 없음(bulk 전용)** — [KimICCF]/[KimCA]/[Cha] "lever=미세구조/계면" 실험 3종; cascade는 S 전하(Bader)·ICOHP를 이미 디스크립터로 보유 | **✗ 우리 공백 축의 계산판 + 🔑 처방 접점**: "bulk σ ≫ device σ"의 원자적 메커니즘(정전기 Li 트랩·10–20 Å)을 MLIP 규모화로 보인 논문 — 우리 bulk-only 결과 서술 시 "GB 지연 기원은 [KimMTP] 계산 참조"로 인용. 처방(고산화수→S 전하↓)은 우리 cascade Bader/ICOHP 언어와 직결 = "우리 도핑 스크린이 GB Li-축적 완화에도 닿을 수 있다"는 문헌 다리. ⚠ 단일 GB 모델(다결정 평균 아님)·Li 축적 10 ns 미수렴(D 하한 아님)·γ figure-read → GB D 절대값 이식 금지 |
| **⚠(할라이드 교차-화학) '무질서=공정변수'의 실험 실증 + "Schlem 0.25" 귀속 감사** — 삼방 Li₃ErCl₆/Li₃YCl₆: 합성경로(볼밀→550 °C 어닐 1 min/1 h→앰풀 1주)만 바꿔 **양이온 M2–M3 자리무질서 2.5→88 %**(XRD Rietveld+PDF 이중정량) 연속 조절 → **σ 1.7×10⁻⁵→3.1×10⁻⁴ S/cm(18×)·Ea 0.49→0.41 eV**(EIS **total**·bulk/GB 분리불가 명시). VASP-PBE 정적: 질서/반전/교대 배열 **등에너지 ~1–2 meV/atom**(face-sharing 강제 배열만 +26 meV/atom 벌점) = 실현 배열은 공정 몫; 병목 삼각 전이면적 5.88→6.18 Å²↔Ea 상관(Fig S13 — **⚠ SI 실물 감사 2026-08-03: 저무질서 2점 Ea가 본문과 뒤바뀌어 인쇄 + 3점이 0.03 Å²에 밀집 = BM 1점이 끄는 2-클러스터, 상관을 정량 인용하지 말 것**); **유익한 M2–M3 무질서 ↔ 유해한 M-on-Li antisite(Wang/Mo) 구분**(후자는 실험 배제). **[강화] Y 계열도 무질서 축에선 σ·Ea 4점 단조**(무질서 9.8/16.1/17.3/100 % ↔ σ 3.4/4.7/5.5/9.5×10⁻⁵ S cm⁻¹ ↔ Ea 0.4925/0.4785/0.4465/0.4455 eV) — 비단조인 축은 '어닐 시간→무질서'(5 min 16.1 < 1 h 17.3 %) → **"공정축 말고 구조 서술자축으로 그려라"는 플롯 문법 교훈**(우리 σ·Ea를 4d-Cl 점유·BVSE 채널%·site-PDOS에 대해 그리는 관행의 외부 근거) | **[Schlem20]** (2020 AEM 1903719, exp+DFT 정적, **⚠비-argyrodite 할라이드**; `papers/schlem2020_li3mcl6_cation_site_disorder.md`) | 우리 disorder_ensemble comp1 **d=0(frozen, artifact 1.17)→d=0.5 Ea 0.177±0.027**; modelc 4d-Cl decorate 12.5 %; enumerate→lowest-Ewald 동일 노선; BVSE 채널%·migration_volume(병목 서술자 짝) | **✓ 프레임·방향(무질서↑→σ↑·Ea↓) 일치 — 단 할라이드·양이온 무질서 vs 우리 argyrodite·음이온 무질서 = 물질군/부격자 다름 + EIS total vs MLIP bulk = 수치 등치 이중 금지**. **⚠⚠ 귀속 감사(digest §11b)**: repo가 이 DOI를 "LPSCl ordered 0.25/Cl-rich 0.22"의 원전으로 인용해 왔으나(li_transport.json `Schlem_2020_LPSCl_ordered`·세미나 ref[3]·`kb/open_items.md` #5) **그 수치는 이 논문에 없음(전 Ea 0.41–0.49 eV)** → "EXACT MATCH" 앵커 사용 중지·원전 재확보 필요. 참고로 새로 확보된 LPSCl 실험층도 0.25/0.22가 아님([Adeli] EIS≡PFG 0.34→0.29·[Kraft] total 0.46) = **LPSCl Ea는 방법·시료마다 갈리는 층위 — "±0.003 eV 일치" 화법 자체가 비방어적** |
| **cross-material 통계학습이 집은 σ 서술자 = *Li–Li 연결망 + 공유성 부격자* (단일 서술자 전멸)** — 실측 40종·전 결정구조 LR 5특징: **LLB+(Li–Li 이웃 多)·LLSD−(Li–Li 距 短)** = 고차원 Li 연결망, **SBI−(부격자 공유결합성**; "이온성↑=안정성↑·전도도↓ 역설" 명시**)**, AFC−(음이온 저배위 — bcc 명제는 5특징 중 1·단독 r=−0.06으로 "황화물 밖 비보편" 반박), LASD+(얕은 Li–음이온 포켓); **20특징 전원 단일 \|r\|≤0.3** = 단일 기하 서술자 스크리닝 불가. + **BV cross-material 산화물 스크리닝 정면 반박**(BV-유망 495종 중 모델 양성 1.6%; **LiAlSiO₄ = BV 유망·실측 1.4×10⁻⁵ 음성 예제**) | **[Sendek17]** (LR 5-feature·훈련 40종; `papers/sendek2017_ml_screening_12k_conductors.md`) | 우리 `migration_volume_fraction`(채널 부피)·`dopant_blocking_fraction`(연결망 희석)·inter-cage 율속·[Perc] site-percolation 백본; **BVSE = within-host 상대 프록시**(원본 주기셀·채널%)로만 사용 | **○ 프레임 일치 (cross-material 통계 ↔ 우리 within-host 물리)**: "σ = Li 연결망+공유성 경로"는 우리 percolation/inter-cage 서사·[Kraft] 공유성 전도경로와 결 동일 — 단 그들 특징은 **정적 기하·전 물질군 선형결합**이라 우리 argyrodite 내부 서술자와 수치 이식 금지(그들 스스로 "인과 아닐 수 있음·특징풀 바뀌면 교체 가능" 자인). **🔑 "BV로 물질 *간* σ 순위 매기기 금지"(LiAlSiO₄ 반례) = 우리 BVSE 규율의 외부 근거** — 우리는 같은 이유로 BVSE를 host 내부 상대 비교에만 씀. **★ 2026-08-03 본문 실물 재검증에서 근거가 한 단계 강화**(digest §16f-5): 이 논문의 감사의 글이 **Prof. Stefan Adams (NUS)** 의 질문·논평에 사의를 표하는데, Adams는 본문 refs 111–113(bond-valence 알고리즘)의 저자이자 **우리 BVSE가 쓰는 softBV 파라미터(Li–S 2.105/Cl 2.249/O 1.466, b=0.37)의 원저자**다 ⇒ "BV cross-material 스크리닝의 한계"는 **BV 창시자가 검토한 상태에서 출판된 반박**이지 외부인의 오해가 아니다. 우리 규율("BVSE는 within-host 상대 프록시·원본 주기셀 값만 정량")을 방어할 때 이 한 줄을 같이 붙일 것 |
| **σ는 골격 양이온(M)에 둔감·음이온(X)에 민감 + 격자 반응 비대칭("S²⁻ 근최적") — 조성족 스캔의 2013 원전** — LGPS 골격 AIMD: **σ300 Ge 13/Si 23/Sn 6/Li₉P₃S₁₂ 4/Li₁₁AlP₂S₁₂ 33 mS/cm = "시뮬레이션 오차 내 동일"**(t-검정; Ea 0.18–0.26, ±0.03–0.09 eV — isovalent도 aliovalent(캐리어 Li₉↔Li₁₁)도 무영향) vs **O 치환 σ 0.03(Ea 0.36, 433배↓=2.6자릿수)·Se 24(불변="임계 채널크기")**; 격자 등방 스캔 **−1%→σ÷10·−2%→×10⁻⁶ vs +4%→×6**(Ea 0.59→0.17); Zeo++ 채널 O −20%/Se +7%·M 무영향. 기전 = **M–Li 상호작용이 S²⁻로 스크리닝**(M은 Li 망과 절연) + **"이미 부분점유 조성이라 대부분 Li mobile"**(캐리어 포화) | **[Ong13]** (2013 AIMD, 실험 0; `papers/ong2013_lgps_family_substitution.md`) | 우리 cascade에서 수송을 움직인 레버는 **전부 비-M 축**: Cl 증량(D600 3.09→7.90e-6, Ea 0.253→0.224)·Nd@Li(σ300 0.52×, connectivity/prefactor)·O@S([Wang22] σ 10×↓ 실험 줄·BVSE 채널 축소); BVSE 채널% = Zeo++ 기하판의 에너지 후속 | **✓✓ 이분법("골격 양이온=불감 / 음이온·Li 망=민감")이 우리 도펀트 분류의 상위 규칙으로 작동** — 단 우리는 Ge/Si/Sn 골격 스왑 자체는 미스캔("재현했다" 금지, "모순 없음"까지만). **⚠ 이식 금지 2건**: ① **캐리어 둔감은 LGPS 특수** — argyrodite는 Li 공공이 1차 레버([Adeli] 48h 0.456 실측·Haven↓, 우리 modelc Li₅.₄) = 조성족 바뀌면 캐리어 축 민감도 역전; ② **격자수축→σ↓는 조성고정 기하효과** — Cl-rich는 수축(9.8598→9.8061 Å)에도 σ 4×↑([Adeli]·우리) = 공공·무질서가 기하를 압도, "격자상수 단독 σ 예측자 아님"([Kraft] prefactor 상쇄와 한 줄). 절대 σ 비교 금지(그들 AIMD 고온외삽 ±수배 오차 vs 우리 MLIP-MD). **★ 우리 σ-규율의 문헌 방패(2026-08-03 실물 검증)**: 이 논문은 **진짜 AIMD**로 얻은 황화물 5종의 σ300 **8.25배 폭(4↔33 mS/cm)을 전부 "오차 내 동일"로 판정**했다 — Ea ±0.03–0.09 eV가 300 K 외삽에서 ×4.7 이상을 만들기 때문. 우리가 단일시드 1.33×를 철회한 것(SEMIFINAL 2026-07-09)이 과민이 아니라 **분야 원전이 세운 기준**임을 한 줄로 방어 가능 |
| **HT-FPMD 통계 규율 원전 — "창을 검증하고, 블록으로 오차 재고, 수렴까지 자동 연장하고, 못 풀면 Ea를 포기한다"** — D=MSD **기울기**(eq 2; 총MSD/6t는 열진동 오염으로 비확산계 과대, Fig S2)·**피팅 창 자체를 데이터로 검증**(t'=5/10/20/30 vs 40 ps 스캔: 5 ps=ballistic/cage 과대→10 ps부터 위양성 급감, Fig S3 → pinball 8–10 ps 고정 채택; **FPMD는 SI 명문 "at least 20 ps" 하한 + 그 위 물질별 custom interval**, 그림 예시 20–30 ps — 2026-08-03 본문·SI 실물로 최종 확정)·오차=**독립 블록 분산→mean±SE**·**AiiDA 워크플로가 err(D)<1×10⁻⁸ cm²/s or <5% of mean까지 자동 연장**(pinball 물질·온도당 NVE 8-분기 1.5–18.4 ns)·온도=1000 K 게이트→750/600/500 K(**1/T 등간격 4점**)·**Ea=최저온(500 K) 해상 시에만 Arrhenius 피팅+Bayesian 오차 전파**·검출하한 D=1e-8 명문("100 ps론 LLZO 500 K[D 2e-7]도 못 본다" 논증)·**σ 환산 자체를 안 함**(전편 D_tr만 보고) | **[Kahle20]** (FPMD 45 ns+pinball 7.6 μs; `papers/kahle2020_ht_aimd_screening.md` §5) | 우리 규율(CLAUDE.md·tools/ionic/): MSD **2–50 ps 고정창**·600/800/1000 K 3점(400/500 K 제외 판정 명문)·**멀티시드 판정**(600 K 3-시드; 단일시드 1.33× 철회 SEMIFINAL)·NE(Haven=1) **σ 절대값 비인용** | **✓✓ 같은 정신의 두 구현 — 항목별 우열이 갈림**: 창 길이(2–50>8–10 ps)·**FPMD 창 일관성**(우리 전 물질 고정 vs 그들 물질별 custom)·**무질서 처리(ensemble vs 단일 질서 배열)**·시드-간 분산은 **우리가 엄격**; per-material **자동 수렴판정·창 검증 절차(Fig S3)·Bayesian Ea 오차**는 **그들이 엄격**(이식 후보 2건: 우리 2–50 ps 창의 t'-스캔 1회 검증 + Ea Bayesian 오차 산출); "σ를 아예 안 만드는" 태도는 우리 절대값-비인용의 상위 극단(블록=궤적 내 오차·시드=궤적 간 오차로 **상보**). **★ 2026-08-03 SI 대조로 드러난 제3 축 = 블록 분해 임의성**: 본문 그림과 SI 그림이 **같은 궤적·같은 창을 블록만 달리 쪼개** 750 K D를 3–25%, 오차막대를 최대 3× 다르게 냈다(8종 중 7종; Li₇TaO₆만 일치) — **양쪽 다 안 잡는 축**이라 우리 이식 항목에 **블록 수(4/8/16) 감도 점검** 1건 추가. **★ 궤적 길이 배분은 우리가 위**: 그들 FPMD T_sim은 43.6–726.4 ps로 16배 차이 나고 **그룹 B 저온이 특히 짧다**(Li₄Re₆S₁₁ 500 K 87.1 ps = 그룹 A 500 K의 1/8) → A/B 경계에 "덜 돌린 것"이 섞임(우리는 전 조성·전 온도 200 ps 동일). 정답은 "동일 하한 + 미수렴 시 자동 연장"의 합집합. ⚠ 그들 FPMD=진짜 AIMD(PBE·Γ-only·d_inner 6.5 Å) vs 우리=MLIP-MD(UMA) — "둘 다 AIMD" 화법 금지 |
| **frozen-host surrogate(pinball)는 "랭킹까지만" — 정량 D는 실패 (host·전하밀도 동결의 대가)** — pinball(Li-only·host+밀도 동결·3-파라미터 DFT-힘 회귀·~4자릿수↓)로 796종 D(1000 K) 스크린 후 FPMD 대조(Fig 15): **정량 상관 빈약**(저자 자인 4원인: local항·무작위변위 피팅·**밀도 동결**·**"host 동결이 예상보다 클 수 있다"**) but **분류기로는 유효** — pinball-D 상위 quartile의 **71%**가 FPMD D>1e-7 cm²/s 달성(2/3/4분위 36/33/**21%** 단조감소)·스크리닝 예측률 54%·[Sendek 2019 CM] 무작위 14% 발생률과 수확(84/796) 정합 계산 | **[Kahle20]** (`papers/kahle2020_ht_aimd_screening.md` §4) | 우리는 정반대 철학: UMA **전 원자** MLIP(host 동역학 포함) + disorder ensemble은 host를 **anneal 700 K+FIRE로 적극 이완**; cascade도 UMA-상대 랭킹→DFT 검증 2단(절대값 비인용) | **🔑 "surrogate=랭킹, 물성값=상위 이론" 위계의 외부 원전 + frozen-host 리스크의 정량 교차점**: [KimMTP] **PS₄ 회전·진동 고정 시 D(600 K) −50%(disordered)/−18%(ordered)** = pinball류 host-동결 근사가 argyrodite에서 D를 절반까지 왜곡할 수 있음의 독립 정량(단 pinball 오차는 계 의존·Fig 15는 양방향 산포 — "항상 과소" 아님). 우리 UMA 절대 σ 비인용([KimMTP] functional 각인)과 같은 결론에 **다른 원인(물리 근사 vs 학습 오차)**으로 도달 — 두 인용을 쌍으로 쓰면 "surrogate 절대값 불신·랭킹 신뢰"가 방법 불문 일반 규칙임을 보이는 문헌 2각 |
| **경쟁 기술자 ①: "케이지는 큰 게 아니라 *서로 비슷해야* 좋다" — `STD of Li-cage size`** — free anion(4a/4c=우리 4d) 주위 Li 평균거리 = 케이지 반지름, **그 산포(STD)가 작을수록 σ↑**. 4a-cage>4c-cage 항상·X⁻케이지>S²⁻케이지 항상 → X를 작은 4c에 넣으면 크기차↓ → **inter-cage 통행 활성**. ordered(0/100 % X@4c) Ea **452/339** vs disordered(25–75 %) **151–193 meV**(Cl)·σ 3–7자릿수 갭; Cl x 0→0.75서 **STD 0.1193→0.0615(−48 %)**·σ 단조↑; σ 순서 **Cl>Br>I 6배열 전부**(S²⁻와 이온반경 근사한 할로겐이 빠름). **★기술자 성능은 논문이 보고하지 않아 우리가 45배열 원수치로 계산**: Spearman **ρ=−0.78**·선형 **R²=0.44**·log R²=0.62; ordered 6개를 빼도 ρ=−0.72(=단순 이진분류기가 아님). **⛔ 단 같은 점유율(50 %)·다른 배열 쌍에서 부호 3/3 오답**(Cl 0.0638→23.3 vs 0.0931→**37.1** mS/cm; Br·I 동일) — 차이가 대체로 **시드 min–max 밴드 안** = **분해능이 시드 잡음과 동급 → 배열 층위에선 무효, 조성/도핑 층위에서만 유효**. ⛔⛔ **2026-08-04 본문 실물 검증**: 그 **반례 두 개가 상관 그림(Fig 5)에 없다** — σ 최대 배열(Cl 50 % P2mm, 37.1)은 **y축 상한 34.97 위로 잘렸고**, Cl 100 %(STD 0.1336인데 σ 0.12)는 **축 안인데 미작도**. 둘을 빼면 Cl 순위상관이 **−0.83 → −1.00(완전)**, R² 0.39 → 0.77. **기술자 성능은 Fig 5 가 아니라 Table 1/S3 로만 말해야 한다**. ⛔⛔⛔ **2026-08-04 ESI 실물 검증(§21)에서 유보가 깨졌다**: 위 “시드 밴드 안” 단서는 **x=0 에만** 해당한다. **할로겐 과잉(Table S3)에서는 밴드 밖 오답이 나온다** — 9조성군 중 **4군**에서 최소 STD 배열이 최속이 아니고 **2군은 [min,max] 가 분리**: **I x=0.25 는 STD 가 2.1배 작은 배열(0.0896)이 σ 는 3.0배 느리다**(2.03 [1.63, 2.44] vs 6.10 [4.07, 9.35]), Br x=0.25 는 1.9배. 실질 시험대인 **n=4 조성군 3개는 3/3 오답**. 기구 = 오답 3건 모두 **4c 를 X 로 100 % 채워 S²⁻ 케이지가 통째로 사라진 배열**이라 **“케이지 종류가 없어진 것”을 “균일해진 것”으로 읽는다**. 그리고 **Table S3 만의 상관은 ρ −0.698·log R² 0.435(I 계열 0.291)** — 45배열 ρ −0.78 은 x=0 ordered 배열의 σ 자릿수 갭이 떠받친 값이다. → **정확한 결론 갱신: 조성 층위에서는 유효, 배열 층위에서는 x=0 에서 “못 매기고” 할로겐 과잉에서 “틀린다”.** ⚖ 단 **통제비교(4a=100 % X 가족)에서는 STD 가 세 할로겐 모두 단조 감소(−24/−33/−16 %)** — **기술자의 물리 자체는 살아 있다**; 인용 금지 대상은 Table 2 의 “−48 %” 라는 **크기**(배열 인구조사 효과 포함)다 | **[Jun22]** (Jun & S.U.Lee JMCA 2022, 한양 ERICA; 순수 DFT+AIMD·실험 0; `papers/jun2022_argyrodite_ion_cage_size_descriptor.md`) | **BVSE 채널 %**(정적·전역·free-volume; iso 0.5서 LPSCl1.6 3.32 → +O 4.74 → +B₂O₃ 6.73 %) + **F\*** 0.191→0.078 eV + **blocking fraction** | **△ 부분 일치 — 그리고 *어긋나는 조건이 결과다***: ① **comp1→modelc 축에서 STD는 개선(0.1193→~0.07) 방향인데 우리 BVSE 채널 %는 −15 %** = 우리 **static-channel paradox**의 반대편. 즉 **Jun STD는 F\* 편, BVSE 채널 %와는 반대 편**(STD가 AIMD로 실제 Li 위치를 보기 때문이지 기하 우월이 아님) ② **큰 음이온을 한쪽 자리에 몰면 갈린다** — Table 1의 **최대 케이지(I⁻@4a, r=3.11 Å)가 최저 σ**. 같은 긴장이 [Rao25](Li Voronoi 9.39 Å³=넓은 채널=좋음) ↔ [Jun22](큰 케이지=나쁨) 사이에 있고, **화해점 = "크기가 아니라 균일도"** ③ **STD엔 연결성 항이 없다**(완전 국소 통계) → "케이지는 균일한데 목이 막힌" 구조를 못 거른다 = 우리 F\*·`dopant_blocking_fraction`이 잡는 축 ④ **정의역**: argyrodite 4a/4c 골격 필요 → 우리 47종 중 **치환형(O·Nd)만 계산 가능, 개재·코팅형(B₂O₃/Sc₂O₃/WO₃…)은 정의 불가** → **BVSE 채널 %가 여전히 유일한 전수 축**. ⑤ 정량 접점: **x 0→0.6 σ 배율 ≈4–5× ≈ 우리 comp1→modelc ×4**(둘 다 비율·엔진 다름) ⑥ 우리 `tools/comp1_v3/voronoi_volume_disorder.py`가 **사촌 도구**(같은 "국소 산포=무질서" 발상, 중심만 원자 vs free-anion) → **후처리 4축(STD·채널 %·F\*·Voronoi std) 교차검증이 최저비용 검증**. ⛔ **σ 절대값·χc^7.14·Eq(6–8) 가중식 이식 금지**(§ digest 14) |
| **⛔ 문헌 "σ_bulk" 는 자유노브 2개의 산물 — 배열 앙상블을 한 숫자로 접는 관행의 해부** — 배열별 σ를 $P_i=P_i(E)P_i(\sigma)$, $P_i(E)\propto e^{-\Delta E/kT}$, $P_i(\sigma)\propto e^{-\Delta\sigma/kT}$ 로 가중 합산 후 **σ_exp=σ_calc·χc^7.14**(결정화도 80 %) 적용 → Li₆PS₅Cl **σ_bulk 18.79 → σ^0.8 3.82 mS/cm**(실험 2.3–3.1). **★우리 검산**: (a) **Eq(7)은 차원 무의미** — Δσ(mS/cm)를 kT(meV)로 나눔; 같은 σ를 **S/cm로 쓰면 18.79→87.6 (4.7×)** = **단위 선택이 결과를 결정** (b) 혼합규칙 선택이 3자릿수를 가름 — 조화평균(=자기들이 말한 "가장 느린 영역이 율속"의 물리적 형태) **0.12** / 논문 **18.79** / E-가중만 **87.8** mS/cm → **서사는 병목인데 식은 병렬** (c) 즉 실험 일치는 "E-가중만 쓰면 6–8× 과대"를 **차원무의미 kinetic 가중(4.7×) + χc^7.14 경험보정(4.9×)** 두 노브가 정확히 상쇄한 결과 (d) χc^7.14 회귀는 **8점·R² 없음·(1,1) 앵커가 지수를 결정** (e) Table S1 자체에 산술오류 1건(50 %/ΔE=11 행 P_i(σ) 0.0028, 식대로면 8.4e-4) | **[Jun22]** ESI Section B, Eq 6–8·Fig S2·S3·Table S1·S2 (= **[KimMTP] Eq S8–S11 의 원출처**) | **σ 절대값 인용 금지 + 결정화도 보정 없음**; 우리는 배열 앙상블을 **접지 않고 cfg 산포를 오차막대로 보고**(disorder_ensemble d=0.5/1.0 × cfg0/1/2) | **✓✓ 우리 규율이 옳다는 외부 해부 증거**: 문헌이 "실험과 잘 맞는다"고 말하는 σ_bulk 는 **물리 결과가 아니라 두 노브의 산물**이다. → ① **우리 "σ 절대값 인용 금지"의 세 번째 근거**([KimMTP] functional 8배·[Lee24] AIMD 840배에 이어 **"가중·보정식 자체"**) ② **"앙상블을 한 숫자로 접는 것" 자체가 정보 손실**임을 보임 → 우리 config-variance 오차막대의 방법론적 정당화 ③ ⛔ χc^7.14·Eq(6–8) **이식 금지** 재확인(원출처 확인 완료) |
| **⚠ 단일시드 판정 금지의 *외부 정량* 근거 — 같은 구조·같은 온도에서 σ가 몇 배 흔들리는가** — 배열·온도당 **≥3회 독립 AIMD**(ESI "Ensemble average", Fig S1 Run 1…4) 후 실온 외삽 σ 의 **[min, max]** 보고. 우리 환산: **무질서 배열 1.3–2.5× / 완전질서 배열 3.2–262×**(Li₆PS₅I 0 % X@4c = **262×**, Li₆PS₅Cl 0 % = 18×). 즉 **가장 느린 배열이 통계적으로 가장 못 믿을 배열**인데, 같은 논문의 σ_bulk 가중식은 바로 그 배열에 최대 가중(P=0.6482)을 준다 | **[Jun22]** Table 1 min–max (AIMD, 45배열) | modelc **3-seed** Ea 0.197±0.032 eV(600 K 시드); 단일시드 1.33× 우세 주장 **철회 사례**(SEMIFINAL 2026-07-09); comp1/modelc Ea 는 **온도당 단일 궤적**(오차막대 없음) | **✓✓ 규율 정합 + 우리 공백 1건 노출**: ① "MD σ 는 단일 궤적으로 판정 불가"가 **AIMD 에서도 참**임을 문헌 수치로 확인 — 우리 철회 사례의 외부 방증 ② **느릴수록 통계가 나쁘다**는 비대칭은 우리 disorder_ensemble 의 **ordered/frozen 쪽 값**(artifact 1.17 eV)에도 그대로 적용 → ordered 기준선은 시드를 더 써야 한다 ③ ⚠ **우리 comp1/modelc Ea 는 온도당 단일 궤적**이다 — 이 논문 기준(≥3 시드)에 못 미친다. 멀티시드 판정엔 modelc 3-seed 만 쓰는 현 규율 유지 |
| **⚠⚠ "다성분·고엔트로피 → σ↑" 인과의 실험적 반증 — *배열 엔트로피가 아니라 원소 정체성과 치밀화가 지배*** — LGPS 4d(Ge) 자리 **Si·Ge·Sn·Ti·W 등몰 5원소 치환**(Li₁₀ 고정·**전부 4가** = aliovalent/평균 산화수 효과를 설계로 제거), 10조성 전수 실험. **판정 4건**: ① **ΔS_config = ln n 재표기**(1.0986/1.3863/1.6094 R = ln3/4/5 정확), **자리 공유 P1(occ 0.5) 포함 시 1.498 R < 1.5 R 문턱 아래**(우리 재계산) — 열역학 검증(ΔG/E_hull) 전무 ② **ΔS 동일(1.3863 R)한 사원 3종의 σ 가 1.89 / 3.52 / 4.70 mS/cm 로 2.5배 스프레드**, 가르는 변수는 **"Ge 가 있는가"**(Ge 없는 SiSnWTi 최저) → **원소 정체성 > 엔트로피** ③ 헤드라인 3.0→**13.24 mS/cm** 는 **화학(냉간 3.0→5.73, ×1.9) × 공정(열간가압 ×2.3)** 의 곱이며 **pristine LGPS 열간가압 대조군 부재**·**상대밀도 11시료 전부 미보고**·문헌 소결 LGPS(12) 대비 **+10 %** ④ 초록의 "lowers the migration barrier" 는 **자기 Table S2 가 반증**(Li₁₀SnP₂S₁₂ 단독 Ea 0.26 < 오원 0.27, 헤드라인 시료 0.31, 문헌 LGPS 0.25). **lee2024 두 기구 모두 배제** — dynamic lattice: **셀부피 956.5→951.5 Å³ 수축**(본문 "statistically averaged" 자인, 최대부피 Sn 이 σ 최저) / inductive(평균장): **전부 4+·Li₁₀ 고정으로 구조적 불가** → 남는 제3 기구 = **"동일 산화수 다원소의 국소 불균일(분산)"** 이나 **Bader·PDOS·COHP 전무**(실험 증거는 ³¹P NMR 광폭화·Raman PS₄³⁻ 이동·S 2p 어깨뿐) | **[Zhou26]** (`papers/zhou2026_high_entropy_lgps_multicationic.md` §4·§8·§9) ⚠ **LGPS 골격 = 비-argyrodite → 수치 비교 제외, 논리축만** | 우리 cascade **codoping 1081쌍**에는 aliovalent 효과와 국소 불균일이 **섞여 있다**(LODO 누수 R² +0.089→−0.255). 우리 σ 규율(절대값 인용 금지·비율도 멀티시드 판정만)은 그대로 유지 | **🔑🔑 우리 co-doping 캠페인에 직접 이식 3건**: ① **isovalent-only 서브셋 재학습**(교란변수 제거 — 이 논문이 실험으로 한 통제를 우리는 데이터 슬라이싱으로) ② **"기술자 값 동일·원소 다름" 대조쌍 자동생성** — ΔS 가 같은데 σ 가 2.5배 벌어진 #7/#8/#9 가 인과를 한 줄로 무너뜨렸다; 우리 기술자에도 같은 tie-control 이 필요 ③ **Bader/ICOHP 의 *분산* σ(Q_S) 를 신규 기술자로** — lee2024 는 **평균**(S −1.48→−0.84 e⁻)을 썼고 Zhou2026 은 **분산**을 주장했으나 정량하지 못했다. **우리 파이프라인은 자리별 값을 이미 뽑으므로 비용 ≈ 0 이고, 이건 두 논문이 비운 칸이다.** 부수: "치밀화 ×2.3 > 화학 ×1.9" 는 **[KimICCF]** "σ 병목 = 미세구조"의 세 번째 독립 증거 |
| **⚠ AIMD 실패모드의 *반대편* 사례 — 너무 차갑고 너무 짧아도 D 는 자릿수로 틀린다** — VASP/PBE-D3/Γ/400 eV/NVT **250·300·350 K / 15 ps / dt 1 fs**(셀크기·무질서 배열 **미기재**·시드 1). **우리 재검증 2건**: (a) **SI Fig 6 의 세 데이터점(ln D = −21.886/−22.218/−22.916 at 1/T = 0.002857/0.003333/0.0040)으로 3점 회귀하면 Ea ≈ 0.078 eV** — 같은 그림에 인쇄된 **"Ea = 0.15 eV" 와 2배 불일치**; (b) **D(300 K) 를 Nernst–Einstein 역산(20 Li/cell, V 953.5 Å³, Haven=1) 하면 σ ≈ 2.9×10² mS/cm = 실측 13.24 의 ~22배**. 원인은 Fig 2d 가 직접 보여준다 — **250 K MSD 는 2–10.5 ps 동안 0.45 Å² 평탄(케이지 rattling) 후 단발 계단**, 즉 확산 평균이 아니라 hop 하나다. 그 점이 3점 아레니우스의 **저온 앵커**다. ✏ **2026-08-04 독립 재현 + 격상(§20.3)**: SI 없이 **본문 Fig 2d MSD 를 직접 적분**해도 D(300 K)=2.60×10⁻⁶ cm²/s → **σ_NE = 339 mS/cm = 실측의 26배**(SI Fig 6 경로와 다른 그림·다른 경로로 같은 결론). 그리고 **Ea 는 창 하나에 종속된다** — 250 K 곡선을 **14 ps 까지 쓰면 0.064 eV, 단발 hop 직전인 12 ps 에서 끊으면 ≈0.16 eV(2.5배)**. **즉 이 3점으로는 Ea 가 결정되지 않고, 인쇄된 0.15 eV 도 우리가 재계산한 0.078 eV 도 창 선택의 산물이다** | **[Zhou26]** §7c ↔ **[Lee24]** ESI Table S1 (AIMD 가 Li₆PS₅I σ 를 **840×** 과대) | 우리: **MSD 창 2–50 ps 고정 · 600/800/1000 K(400/500 K 제외 판정) · prod 200 ps · 3-시드** | **🔑🔑 두 사례가 규율의 양쪽 끝을 채운다**: [Lee24] = **너무 뜨거움**(고온 외삽으로 840배), [Zhou26] = **너무 차갑고 짧음**(15 ps @250 K 로 ~22배). 정확한 명제는 **"AIMD/MD 의 온도·시간 창이 그 물질의 hop rate 와 맞지 않으면 D 는 자릿수로 틀린다"** 이며, 이는 **MLIP 냐 AIMD 냐와 무관**하다. → 우리 200 ps·3-시드·고정창 규율의 문헌 근거가 **2개(양방향)** 가 됐고, 동시에 **"우리 600–1000 K 창은 외삽이 길다"** 는 우리 쪽 약점도 같은 저울에 올려야 함이 분명해졌다 |
| **⚠ NEB 로 "장벽이 낮아졌다"를 주장할 때의 잡음 하한** — 다성분 조성의 Li 이동 프로파일: **최대 장벽 0.181 → 0.165 eV (−0.016 eV, −9 %)** 이지만 **경로의 나머지 대부분 구간에서 오히려 상승**(image 2–6, 12–15, 17–20). 직전 최저점 기준 유효 정방향 장벽은 0.158 → 0.147 eV(**−0.011**). 조건: **힘 수렴 0.03 eV/Å · 배열 1개 · AIMD(VASP)와 다른 코드(CASTEP)**. ✏ **2026-08-04 픽셀 복원 교정 2건**: (i) **이미지 수는 22 vs 22 로 같다**(초록이 x+1 오프셋되어 그려졌을 뿐) — "22 vs 23 불일치" 철회; (ii) **부차봉우리는 "새로 생긴" 것이 아니다** — 국소 봉우리 개수가 **3 대 3 으로 동일**하고, 원래 있던 부봉이 **0.0515→0.0882(+71 %)·0.0531→0.1052(+98 %)** 로 두 배 가까이 **자란** 것이다. → 본문의 "LGPS 는 single-peak, HE 는 multi-peak" 대조 자체가 성립하지 않는다 | **[Zhou26]** §7d (figure-read) | 우리 NEB 는 Li₃N 계열에만. argyrodite 는 MLIP-MD Ea(comp1 0.253 / modelc 0.224, modelc 3-seed **0.197±0.032**) | **🔑 규칙 도출 (2026-08-04 보강)**: **NEB 개선폭이 (a) 힘 수렴 기준 (b) 배열간 분산 중 큰 쪽보다 작으면 주장하지 않는다.** 그리고 **"multi-peak 화" 를 주장하려면 대조군의 봉우리 개수를 먼저 세라** — 여기서는 3 대 3 으로 같았고, 실제로 바뀐 것은 부봉의 *높이*(+71 %/+98 %)였다. 우리 modelc 3-시드 오차막대 ±0.032 eV 가 바로 그 하한이고, 이 논문의 −0.016 eV 는 그 절반이다. "multi-peak 지형 = 유리" 서사도 **prefactor 감소**(우리 `kraft2017` Meyer–Neldel 축)를 함께 보지 않으면 성립하지 않는다 |
| **⚠⚠ 헤드라인 σ 를 인용하기 전에 *그림의 온도 격자*를 먼저 확인하라 — 5 °C 가 Ea 를 30 % 움직인다** — 초록·결론이 **"13.24 mS cm⁻¹ at 25 °C"** 라고 쓰지만, Fig 2a 아레니우스의 실측은 **10 °C 격자**(…, 40, 30, 20, 10, 0, −10 °C)라 **25 °C 에는 마커가 아예 없다**. 픽셀 복원: **30 °C ≈ 13**, **20 °C = 9.31**, **0 °C = 3.11**(본문 3.10 ✓ = 축 교정 신뢰도 0.3 %), **25 °C 내삽 ≈ 10.9**, 회귀선 위 25 °C 값은 **8.85**. 결과: 초록의 두 σ 를 **25 °C 로 읽으면 Ea = 0.408 eV(σ) / 0.432(σT)** 로 인쇄된 **0.313 과 30–38 % 어긋나는데**, **30 °C 로 읽으면 0.345** 로 판독오차 안에서 맞는다(회귀선 기울기 자체는 **0.3133 eV** = 라벨과 완전 일치). **즉 틀린 것은 데이터도 회귀선도 아니고 "25 °C" 라는 온도 꼬리표다.** 부수: 같은 논문의 대칭셀·풀셀은 전부 **25 °C** 라 **σ 와 셀 데이터의 온도가 5 °C 다르다** | **[Zhou26]** §20.1 (본문 Fig 2a 픽셀 복원, `tools/litdb/zhou2026_fig_extract.py`) | 우리 σ 규율: **절대값 인용 금지 · 비율도 멀티시드 판정만.** 실험 σ 를 우리 표에 올린 적 없음 | **🔑 절차 채택**: 문헌 σ_RT 를 digest 에 적을 때 **(i) 그 값이 그림의 *데이터점*인지 회귀선 값인지, (ii) 측정 온도 격자에 그 온도가 실제로 있는지** 를 확인하고, 없으면 **"(내삽)" 또는 실제 측정 온도를 병기**한다. 이번 사례는 **σ 값 자체는 정직한데 온도 라벨 하나로 σ–Ea 정합이 깨진** 경우다 — 우리가 문헌 σ·Ea 쌍을 이식할 때 가장 조용히 새는 구멍 |
| **⛔⛔ 아레니우스 그림에서 Ea 를 읽기 전에 *y축이 선형 눈금인지* 확인하라 — 이 논문은 아니었다** — SI Fig 6(AIMD ln D vs 1/T)의 주눈금 3개는 픽셀 간격이 **220.5 px / 220.5 px 로 똑같은데**, 그 눈금에 적힌 값 간격은 **0.332 / 0.698(비 2.10)** 이다. 즉 **데이터 세 값(−21.886 / −22.218 / −22.916)을 그대로 커스텀 눈금 라벨로 찍고 등간격에 배치**했다. 세 마커는 (1/350, 1/300, 1/250) 위에 정확히 얹혀 있으므로 **데이터는 정직**한데, **그 위에 그려진 빨간 "Linear fit" 직선과 옆에 적힌 "Ea = 0.15 eV" 는 그려진 기하와 아무 관계가 없다.** 세 점의 최소제곱은 **0.0785 eV**(구간별 0.060 / 0.090) = **인쇄값의 1.91배 차**. **축이 데이터를 곧게 보이도록 그려져 있었다** | **[Zhou26]** §21.0-② (SI Fig 6 원본 1298×798 픽셀 복원, `tools/litdb/zhou2026_si_verify.py figS6`) | 우리 아레니우스(600/800/1000 K 3점)는 **CSV 를 db/properties/ 에 동시 등록**하므로 그림-데이터 분리가 원리적으로 불가능하다 | **🔑 절차 채택 2건**: ① 문헌 그림에서 기울기를 읽을 땐 **눈금 간격 ÷ 값 간격이 일정한지 먼저 검산**한다(2줄 코드). ② 우리 그림에도 **Origin 커스텀 눈금 라벨을 데이터 값으로 찍지 않는다** — 하우스 스타일에 명문화. 이 사례는 **"figure-read Ea 가 틀린 게 아니라 그림이 틀린"** 첫 사례다 |
| **⚠⚠ 문헌 Ea 는 *적합창*을 밝히지 않으면 0.05 eV 가 그냥 움직인다 — 실측 16점 재적합으로 확인** — SI Fig 3-11(열간가압 Nyquist **16패널**, −50…100 °C **10 °C 격자**)의 패널 축을 캘리브레이션해 σ(T) 16점을 복원(30 °C **13.21** vs 인쇄 13.24 = −0.2 %, 20 °C 9.16, 0 °C 3.13 vs 인쇄 3.10 → **세 점 독립 일치**). 그 16점을 σ = A e^(−Ea/kT) 로 재적합하면 **전체창(−50…100 °C) 0.3116 eV**(= 인쇄 0.313 ✓ 재현), **실온창(+20…+60 °C) 0.2667**, **영하 가지(−50…0 °C) 0.3249** — **창 하나로 0.06 eV**. 아레니우스가 **곡선**인데 전체창 R²(0.9945)가 그 곡률을 가린다. 게다가 **반원은 −20 °C 아래에서만 분해**되므로 전체창 Ea 는 "반원이 보이는 저온"과 "스파이크만 있는 고온"을 한 직선에 올린 값이다(EIS 상한 100 kHz) | **[Zhou26]** §21.1 (`tools/litdb/zhou2026_si_verify.py fig311`) | 우리 MLIP-MD 규율은 **600/800/1000 K 3점 고정 + 400/500 K 제외 판정 + MSD 창 2–50 ps 고정**으로 창을 미리 못 박아 뒀다 — 이 논문이 겪은 문제를 **설계로 회피**하고 있다 | **🔑 이식 2건**: ① 문헌 Ea 를 db 에 적을 때 **적합창(T 범위·점수)을 필수 필드로** 병기한다. 창이 없으면 "창 미표기"라고 쓴다. ② **같은 논문 안에서 Ea 가 두 값(0.31 / 0.27)으로 나오는 것이 반드시 오기는 아니다** — Table S5 의 0.27 은 hot/cold 혼합이 아니라 **실온창 값**일 가능성이 더 크다. 우리도 창을 안 밝히면 같은 혼란을 만든다 |
| **⚠ XPS 성분 라벨은 *이중항 간격*으로 검산하라 — 스핀궤도 분리가 안 맞으면 그 성분은 화학이 아니라 피팅이다** — SI Fig 8c(Ti 2p, 시료의 ~0.4 at%)는 4성분을 얹고 "Ti⁴⁺"·"Ti⁰" 로 라벨했다. 픽셀 복원: **"Ti⁴⁺" 쌍 458.84 / 464.60 → 분리 5.76 eV ✓**(Ti 2p SO 5.7), 그러나 그 위치는 **TiS₂(456.0–457.0)가 아니라 TiO₂(458.8)** 다. **"Ti⁰" 쌍 455.49 / 459.95 → 분리 4.46 eV ✗** — 어떤 Ti 2p 이중항도 아니고(5.7–6.1), Ti 금속 2p₃/₂ 는 453.9 다. 원 데이터 산포가 봉우리 높이와 맞먹는다 ⇒ **"금속 Ti 존재"가 아니라 노이즈 위 과적합.** 같은 그림에서 **Sn 3d₅/₂ = 486.57 = 교과서적 Sn⁴⁺** 라, 본문이 인쇄한 485.0 은 **자기 SI 보다 1.6 eV 낮은 전사 오류**였다(우리가 걸었던 "Sn 환원" 플래그 **철회**) | **[Zhou26]** §21.2 (SI Fig 8 은 **결합에너지 숫자·성분비·기준선이 하나도 인쇄돼 있지 않다** — 값은 전부 픽셀 복원) | 우리 XPS 는 아직 문헌 대조용으로만 쓴다 | **🔑 절차 채택**: 문헌 XPS 성분을 digest 에 옮길 때 **(i) 이중항 분리가 원소의 SO 값과 맞는가, (ii) 위치가 산화물인가 황화물인가**를 두 줄로 검산한다. 이번 회차는 그 검산 하나로 **우리 플래그 1건을 철회하고 1건을 하향**시켰다 — **문헌 비판도 검산 없이 쌓으면 우리 쪽이 틀린다** |
| **⚠ 전기화학 셀 주장의 최소 자기정합 검산 — EIS(Ω) 와 정전류 분극(V) 은 I·R 로 서로 맞아야 한다** — Li\|LM₀.₂PS\|Li **0.5 mA cm⁻²**, Φ10 mm(0.785 cm²) ⇒ **I = 0.393 mA**. inset Nyquist 는 **1st ≈70 → 45th ≈110 → 98th ≈175 Ω 로 2.5배 상승**하는데 본 패널 분극은 **±1.8 V(≈110 h) → ±0.25 V(정상) 로 7배 하강**한다. I·R 예측은 27 → 69 mV 뿐이라 **정상상태 ±250 mV 를 설명하려면 R ≈ 640 Ω, 초기 ±1.8 V 는 ≈4.6 kΩ** 가 필요 — **3.6~66배 어긋난다.** 저자도 *"impedance spectra cannot be directly converted into the instantaneous galvanostatic polarization voltage"* 라 자인하나 원인은 설명하지 않는다. ⚠ **정전류에서 분극이 단조 감소하는 것은 soft-short(전자 누설 성장)의 고전적 서명**이기도 하다 | **[Zhou26]** §20.5 (Fig 6b 본 패널 ↔ inset) | 우리는 셀 실험이 없다(계산 전용). 임피던스 해석 축은 `kim2025_impedance_decoupling_tlm_assb` | **🔑 채택할 검산 한 줄**: 대칭셀 논문을 digest 할 때 **ΔV_관측 vs I·R_EIS 를 반드시 나눠 본다.** 두 값이 자릿수로 어긋나면 (a) 같은 셀·같은 시점이 아니거나 (b) soft-short 이거나 (c) EIS 가 저항의 일부만 본다 — 셋 중 무엇인지 논문이 말하지 않으면 **"1200 h 안정" 같은 수명 주장은 한 칸 내려 잡는다.** 이 논문에서 **가장 강한 주장(Li 금속 내성)의 가장 약한 고리**가 정확히 여기였다 |
| **⚠⚠ 고온 AIMD 외삽이 *조성 서열 자체를 만들어낼* 수 있다 — 감사 절차 3종** — Li₂₊ₓZr₁₋ₓ(Er/Nd)ₓCl₆ 11조성의 AIMD(**600–900 K 4점·50 ps·Li 16–21개·단일시드·단일배열**) 결과를 재분석: **①NE 역산**(SI eq5 σ=nq²D/kT)으로 셀 72원자·N_Li=8(2+x)·**11조성 단일부피 1547.8 Å³** 확정(11/11 σ 0.03–0.24 % 재현) → **②D₀ 복원 → Meyer–Neldel ln D₀ vs Ea: R²=0.93, E_MN=57 meV**(=kT@665 K, **시뮬 온도창 한복판**) → **③온도별 분산: 600–900 K 실측구간 D max/min = 2.3–3.6× 인데 300 K 외삽 시 29.6×**. 즉 **"6배 향상·volcano·최적조성" 서열이 전부 외삽 증폭**. 논문은 He/Mo 2018[31]을 *MSD>5 Å² 판정*에만 쓰고 **불확실도는 버렸다** | **[Ren26]** §6.3·§6.7 (⛔프리프린트·⚠할라이드, **재분석은 우리 것**) | 우리 규율이 이미 방어: **MSD 창 2–50 ps 고정·prod 200 ps·600/800/1000 K 3점·modelc 3-seed(Ea 0.197±0.032)·σ 절대값 인용 금지·비율도 멀티시드 판정만**(단일시드 1.33× 철회 사례) | ✓✓ **우리 절차의 외부 반례 검증** — 이 3종 감사(NE 역산·D₀/MNR·온도별 분산)를 **앞으로 모든 AIMD-σ 논문에 적용**할 표준으로 채택 권고. **✏ 2026-08-04 2차 패스에서 원인이 특정됐다(§20.2–20.3)** — 외삽 증폭의 정체는 "짧은 고온창"이 아니라 **Methods 에 없는 다섯 번째 온도점(500 K)** 이었다. Fig 3d/3e 마커를 픽셀로 전수 추출하니 12/12 계열에 1000/T=2.000 점이 있고, 600–900 K 외삽선 대비 **±1.3 dex 로 양쪽 산포**(정보 0)한다. 가장 긴 x-팔에 놓인 그 잡음점이 11개 계열의 적합선을 전부 같은 축으로 회전시켰다 — **이것이 E_MN=57 meV 보상선(R²=0.93)이 그토록 깨끗했던 이유다.** |
| **⛔⛔ 아레니우스 그림을 인용하기 전에 ①y축 규약 ②Methods 에 없는 온도점 둘 다 확인하라 — 한 점이 헤드라인 Eₐ 를 만들었다** — Li₂₊ₓZr₁₋ₓErₓCl₆ 의 Fig 3d/3e 를 600 dpi 로 재보니 **(i) y축 라벨이 `ln(D)` 인데 실제 그려진 양은 log₁₀(D)** — 그려진 적합선 기울기가 인쇄 Eₐ 를 **4자리까지 재현하는 게 log₁₀ 규약에서만**(Er0.125 0.3842·Nd0.25 0.2046·Nd0.5 0.2818 완전일치), ln 으로 읽으면 11개 전부 정확히 ×1/2.303 어긋나고 D≈10⁻³ cm²/s(기체급)라는 불가능한 값이 된다. **(ii) Methods 는 600/700/800/900 K 4점이라고 쓰는데 그림에는 500 K 점이 12/12 계열에 있다**(SI Table S5 에도 없다). **(iii) 헤드라인 조성 Li₂.₅Zr₀.₅Er₀.₅Cl₆ 은 D(500 K)=2.89e-6 > D(600 K)=1.69e-6 — 냉각하니 1.7배 빨라진다(활성화 과정에서 불가능).** 그 점을 빼고 600–900 K 4점만 재적합하면 **Eₐ 0.163 → 0.372 eV**(pristine 0.230 → 0.332). **결정적 확인: 재적합 0.372 eV 가 같은 논문의 NEB Oct–Tet 장벽 0.370 eV 와 0.5 % 로 일치한다** — 즉 이 조성에서 "정적 NEB 가 AIMD 보다 2.27배 크다"는 격차는 NEB 가 과대해서가 아니라 **AIMD Eₐ 가 눌려 있었기 때문**이다 | **[Ren26]** §20.1–20.3 (본문 Fig 3d/3e 마커·적합선 픽셀 복원, `tools/litdb/ren2026_fig_verify.py`; ⛔프리프린트·⚠할라이드, **재분석은 우리 것**) | 우리 규율: **600/800/1000 K 3점 · 400/500 K 제외 판정 명문(CLAUDE.md)** · MSD 창 2–50 ps 고정 · Ea 오차막대 600 K 3-시드 · 아레니우스 CSV 를 db/properties/ 에 동시 등록 | **🔑🔑 우리 "400/500 K 제외" 규율의 가장 직접적인 외부 증거.** 종전 사례들은 "저온이 짧으면 부정확해진다"였는데([Zhou26] 15 ps@250 K ~22×), 이건 **저온점 하나가 부호까지 뒤집어 Eₐ 를 2.3배 깎은** 사례다. **🔑 절차 채택 2건**: ① 문헌 아레니우스에서 Eₐ 를 옮길 때 **그림의 마커 개수를 세어 Methods 의 온도점 수와 대조**한다(불일치 시 인용 보류). ② **y축 규약은 라벨을 믿지 말고 "적합선 기울기 → 인쇄 Eₐ" 역산으로 판정**한다 — ln/log₁₀ 은 2.303배라 육안으로 안 걸린다. 이 두 절차는 [Zhou26] §21.0-②(눈금 간격÷값 간격 검산)와 같은 가족이고, 셋을 묶으면 **"문헌 아레니우스 그림은 축 규약·눈금 선형성·점 개수 세 가지를 검산한 뒤에만 인용한다"** 가 된다 |
| **⚠⚠⚠ 세 번째 실패모드 — *온도점이 하나뿐*이면 σ_RT 는 MD 가 아니라 가정이 만든다** — Li₅B₇S₁₃ DFT-MD(VASP/PBE/PAW·**499 eV·Γ-only·2 fs·100원자·Li 공공 5%**): **900 K 단 1점**에서 D=1.31 Å²/ps 를 얻고, 일반 확산식(eq S21)에 **가정한 prefactor**(a=3.673 Å·ν₀=10 ps⁻¹ from VACF·j=1/6·f=1)와 **가정한 캐리어 분율**(공공 p_occ·z=0.135 / 격자간 =1)을 넣어 Ea 를 *역산* → 같은 prefactor 로 σ(293 K) 를 *재계산*. **우리 재검증(digest §17e-1): eq S21 을 직접 풀어 0.0652 / 0.2205 eV 로 원문 0.065 / 0.22 를 소수 셋째 자리까지 재현** — 즉 전사 오류는 없고, 문제는 **RT 값에 온도 의존성에 대한 MD 정보가 0** 이라는 구조다(메커니즘 가정만으로 **61배**: 0.026 ↔ 1.6 S/cm). 게다가 **SI 31 pp 전문에도 앙상블·서모스탯·총 MD 시간·평형화·MSD 적합 창·시드 수가 전혀 없다(= n/a 확정)** ⇒ D 자체가 재현 불가 | **[Sendek17]** SI §S5·eq S21–S22 (`papers/sendek2017_ml_screening_12k_conductors.md` §8·§17c-3; **재현 계산은 우리 것**) | 우리 규율: **600/800/1000 K 3점 아레니우스 · MSD 창 2–50 ps 고정 · prod 200 ps · 600 K 3-시드 · σ 절대값 인용 금지** | **🔑 [Lee24]=너무 뜨거움(840×) · [Zhou26]=너무 차갑고 짧음(~22×) 에 이어 [Sendek17]=*온도점이 하나* 라는 세 번째 축이 채워졌다.** 세 사례를 묶으면 명제는 **"MD 로 σ_RT 를 말하려면 (i) 복수 온도점 (ii) 검증된 MSD 창 (iii) 시드 분산 셋 다 있어야 하고, 하나라도 빠지면 자릿수로 틀린다"** 로 정리된다 — 우리 3점·고정창·멀티시드 규율이 정확히 이 셋이다. ⚠ 인용 시: 이 논문의 "Li₅B₇S₁₃ σ_RT 0.026–1.6 S/cm" 는 **"DFT-MD 가 superionic 급임을 시사" 이상으로 쓰면 안 되고**, 결정 좌표를 재사용하려면 원 출처는 본문 ref 95(Wada 유리)가 아니라 **SI ref [4] Krebs 1993**(Z. Anorg. Allg. Chem. 619, 293) 이다 |
| **⚠⚠ 외삽 증폭의 *두 번째 독립 사례* — 이번엔 논문이 시뮬레이션 온도의 MSD 를 인쇄해 놔서 *직접 검산*이 된다** — **[KimLYC]** Fig 4 의 MSD 5패널을 축 프레임 검출 후 곡선별 픽셀 판독(2026-08-04): 600 K 총 MSD(=a+b+c, 두 패널에서 인쇄된 Overall 과 98.5/98.6·92.3/92.2 로 검산됨, 정밀도 ±1 Å²) 은 **hcp_1 102.7 · hcp_2 114.8 · hcp_3 98.5 · ccp_1 92.3 = ±12 % 안**인데, 300 K 외삽 σ 는 **12.6 / 10.2 / 18.8 / 3.4 = 5.5×** 로 벌어지고 **hcp_2 는 600 K 최속인데 300 K 에선 밑에서 둘째 = 순위가 뒤집힌다**. 외삽이 만든 배율은 ccp_1 **0.30×** · hcp_3 **1.55×**. 그런데 논문은 Fig 4 를 그 서열의 *설명*으로 제시하며 *"…**Thus**, the ionic conductivity of hcp_2 is slightly lower than that of hcp_1"* 이라 쓴다 — **총합은 hcp_2 가 크다**. 서열을 매개하는 **Ea 는 본문 13 pp 에 한 개도 인쇄돼 있지 않다**(Fig S5 그림만). 같은 논문의 antisite 축도 동일 — pristine 총 MSD **103** vs 1-antisite **≈108**(하락 없음; c 가 깎인 만큼 a 13→25·b 21→26 이 보상)인데 σ 는 12.6→3.6, 그리고 **"blocked c" 패널은 새 MD 가 아니라 pristine 에서 c 만 지운 사후처리**(a=13·b=21 이 자릿수까지 동일, Overall **34 = 21+13**) | **[KimLYC]** §20a·§20c-N1·N2·N3 (본문 13 pp 실물 독립 검증 2026-08-04) ↔ **[Ren26]** 위 행 (같은 현상, 그쪽은 우리 NE 역산으로 복원) | 우리: **600/800/1000 K 3점 · MSD 창 2–50 ps 고정 + 다중 시간원점 · prod 200 ps · 3-시드(Ea 0.197±0.032) · σ 절대값 인용 금지** | **🔑🔑 [Ren26] 은 우리가 *복원*해야 했지만 이번은 논문이 *증거를 인쇄해 놓고 반대 결론을 썼다*.** → **T15 신설**: 순위·비율 주장에는 **외삽 σ 와 시뮬레이션 온도의 D 를 반드시 병기**하고, 두 서열이 어긋나면 **그 불일치 자체를 결과로 보고**한다. 우리 **Nd σ-drop 0.52×(Ea 0.224≈0.227 불변)** 판정에 즉시 적용 — prefactor 지배 서사가 600 K D 에서도 보이는지 확인해야 한다. 부수: **방향분해 MSD 를 도입할 때 총합 MSD 를 같은 패널에 병기**할 것(그들이 병기했기에 우리가 검산할 수 있었다 — 그 점만은 좋은 관행) |
| **서술자 축 — "z/r(이온퍼텐셜)"은 inductive effect와 *같은 축을 가리키지만 부호·크기를 주지 않는다*** — Φ=Z/r(Shannon VI, pm⁻¹)로 18개 Li₂ZrCl₆ 치환계를 정렬해도 σ 분산의 **6.5 %만 설명**(r=−0.255, ρ=−0.089; 문헌 16쌍만 ρ=−0.045). 같은 Φ=0.0781서 **Ta 1.42 vs Nb 0.55**(2.6×), Φ≈0.056서 **Zr 0.28 vs Al 1.13**(4×). 최저 Φ 구간(Ca 0.020→0.58)이 최고 σ도 아님 → **실제 형태는 완만한 volcano(Φ≈0.030–0.040에 고전도군)**, 논문 주장(단조 음상관)은 자기 표에서 미지지. **Li 함량이 3배 나은 예측자(ρ=+0.628)**이며 Φ와 Li 함량은 aliovalency 때문에 r=−0.715로 기계적 반상관 | **[Ren26]** §4.2·§4.5 (⛔프리프린트) ↔ **[Lee24]** §3a(Bader Q_S −1.48(Si⁴⁺) vs −0.84(W⁶⁺)) | 우리 cascade = **Bader·ICOHP(Li–Cl −1.86/−2.10, LOBSTER)** 전자구조 서술자 + ML 교호작용 | ✓ **우리 서술자 방어 논거**: z/r 은 **0-비용 사전필터**로만 채택(극단값 배제), **랭킹 지표로는 금지**. 방향·크기는 여전히 Bader/ICOHP에서만 나온다 |
| **⚠⚠ 경쟁 기술자 ②의 채택 *보류* — "Li–Li 연결망 ≤3.5 Å"은 국소 클러스터와 퍼콜레이션을 구분하지 못한다** — **[Kim26HTS]** 가 HT 깔때기 5단계로 쓴 구조 기반 수송 대리지표(결정구조에서 Li–Li 거리 ≤3.5 Å 연결의 개수·최대 연결 Li 수). **서술자 정당화용으로 저자들이 고른 Fig S2 3종이 오히려 한계를 드러낸다**(2026-08-03 SI 실물 판독, digest §14c-6): **Li₆PS₅Cl = 분리된 케이지 4개** · Li₇La₃Zr₂O₁₂ = 단일 3D 그물 · Li₁₀GeP₂S₁₂ = 1D 사슬 — 그런데 **RT σ 는 LPSCl 이 셋 중 최상급**이다. 원인은 argyrodite 의 율속 단계인 **케이지 간 점프가 ~4 Å 로 3.5 Å 컷 밖**이라 통째로 안 보이는 것. (같은 랩 **[KimLYC]** `kim2025_li3ycl6` 의 Li–Li 인접거리 3.2–3.5 Å 서술자도 같은 가족·같은 한계). **2026-08-04 [KimLYC] 본문 실물 검증에서 독립 경로로 같은 결론에 도달**(§20c-N5): 그 서술자는 **논문 자신의 표에서 비단조**다 — hcp_4 **3.2 Å** > hcp_3 **2.2 Å** 인데 σ 는 2배(38.5 vs 18.8)이고, hcp_2 는 *"considerably short in all directions"* 인데 hcp_1(3.0/3.8 Å)보다 낮다. 실제로 설명되는 것은 **ccp_1(전방향 3.8 Å)이 최하위라는 것 하나뿐**이고 나머지는 **차원성**이 지배한다. 그런데도 본문은 *"the differences in diffusivity and ionic conductivity … **can be attributed to these variations in channel size**"* 로 닫는다 | 우리 **BVSE Li proxy**(`tools/comp1_v3/`, 전위장 기반 채널%)와 **같은 자리를 채우는 독립 서술자**라 두 번째 축으로 매력적이지만 — **우리 황화물 풀에 그대로 이식하면 argyrodite 계열이 구조적으로 과소평가된다.** | **⛔ 조건부 보류.** 이식하려면 (a) 컷을 **4.0–4.5 Å 로 올리거나** (b) **퍼콜레이션 판정을 붙인** 뒤에만 BVSE 채널%와 같은 질문의 답이 된다. 두 지표가 어긋나는 도펀트를 찾으면 그 자체가 결과(§10-2). **부수 규율(§14c-5, Fig S4 LiCaPO₄ 실물)**: MLIP/AIMD 의 Li MSD 를 읽기 전에 **골격 원소 MSD 가 평평한지 먼저 확인**할 것 — LiCaPO₄ 는 골격 O 가 Li 와 거의 겹쳐 올라가(Li ~2–3, O ~2.5 Å²) **Li 전도가 아니라 구조 붕괴 신호**인데 논문은 구분하지 않는다. 우리 `tools/figures/fig_msd_hosts.py` 계열은 원소별로 그리기는 해도 **명문 게이트가 없다** |
| **⚠⚠ 랩 계보 4편 연속 "반쪽 앙상블" — *주인공 축의 배열 분산을 버린다*** — **[Lee24MO]** 는 P 자리 **양이온** 조합을 파는 논문인데 *"For defined x and y ratio, **we selected the most stable structure** among all possible mixed cation combinations"* (본문 p.7273) 로 **[A]/[B]/[C] 배열은 최저E 1개**만 쓰고, **6배열 랜덤 앙상블은 음이온 S²⁻/(Cl,Br)⁻ 무질서에만** 적용한다(p.7275). 즉 **버린 쪽이 하필 이 논문의 주인공 축**이다. `jun2022`(음이온 앙상블·Li 공공 1개) → `kim2024` → `kim2025`(enumlib 열거 후 최안정 1개) → `[Lee24MO]` **4편 연속 같은 패턴**. | **[Lee24MO]** §11-N3 (본문 실물 2026-08-04) · [Jun22] · [Kim25CSP] | `disorder_ensemble` = **배열 앙상블 + 배열간 분산을 오차막대로 보고** | **우리 우위 — config-variance 신규성의 3번째 정량 근거** |
| **⚠ 문헌 그림의 "군 전체 성능" 문구는 *상위 4점*의 것 — 다성분화 자체가 아니라 *모서리 조성*이 번다** — **[Lee24MO]** Fig 2 박스 "[C]⁶⁺ small quantity → σ_RT **> 27**"·"[B] or [C] small quantity → **> 10**" 은 **각 군 18점 중 4점**(idx 27–30 / 45–48)에만 참이고 나머지 14점은 0–6 mS/cm; 같은 꼬리 구간의 idx 43·44 조차 6.5·7.7 로 10 미만. 게다가 **군(4-2) 박스 "38 < σ_RT < 82" 는 논문 자신의 오기**(실측 ≈51–81, 38 대는 군(4-1)). **정확한 요약 = "[A] 최대·[C] 최소 모서리 4점만 좋다"** | **[Lee24MO]** §11-C1~C3 (Fig 2·4 마커 실측) | 우리 co-doping 1081쌍 ML 대리 — **"다성분화 = 개선" 가정을 쓰지 않는다** | **문헌 해석 교정 (우리 프레이밍 유지)** |
| **기구 2축 중 *하나만* 데이터가 있다 — inductive effect(정량) vs dynamic lattice effect(주장)** — **[Lee24MO]** 의 [C]⁶⁺ inductive effect 는 Fig 3(d) 에 **S 전하 Si⁴⁺ −1.48 → W⁶⁺ −0.84 e⁻** 로 수치가 있으나(⚠**전하 분할 방식 미명시** → 우리 Bader 와 같은 축 금지, **부호·순서만**), [A]⁴⁺ dynamic lattice effect 는 **본문·Fig 1–4·Table 1 전체에 격자상수·셀부피가 0회** 등장하고 근거가 ref 19–24 소환뿐이다. → **두 기구를 대등하게 인용하면 안 된다** | **[Lee24MO]** §11-N7·C5 (Fig 3d 원해상도 판독) | 우리 Bader/ICOHP 축 (`electronic.json`) — 분할 방식 명시 | **부호·순서만 정합 · 절대값 비교 금지** |
| **van Hove 상관함수 = "갇힘 vs 자유" 판별 도구 (T12 원전) — 단 컬러 정규화 기준을 명시해야 쓸 수 있다** — **[Lee24MO]** Fig 3(e) 가 4계를 거리–시간 지도로 갈라 보이지만, 실물에서는 **네 패널 전부 ~3.5 Å 케이지 띠가 살아 있고** 고전도체는 그 위에 **장거리 꼬리가 추가**되는 형태다(“전 거리에 분산”은 과장). 4패널 컬러바가 모두 **0–1 정규화인데 기준 미표기 → 패널 간 절대 비교 불가**, 시간축은 ~480 ps(본문 "over 500 ps"). ⛔⛔ **2026-08-04 [Jun22] 본문 실물 검증에서 축이 갈렸다 — self-part 만 판별력이 있다**: Fig 4(b) **self-part** 는 세 배열을 확실히 가르지만(ordered 두 패널 *"Caged Li-ions"* ↔ 50 % *"Inter-cage diffusion"*, ⚠ 띠 중심은 5 Å 이 아니라 **~4 Å**, 5 Å 은 상한), **Fig 4(c) distinct-part 세 패널은 육안으로 거의 동일**하다 — **σ 가 0.0033 ↔ 23.3 mS/cm (10⁴ 배)** 인데도. → **G_d 는 "협동 모드가 있다"는 정성 관찰일 뿐 빠른 계·느린 계를 가르지 못한다.** **[Lee24MO]**·**[Kim25CSP]** 에 이어 **3건 연속 같은 방향** | **[Jun22]** §20.7 · **[Lee24MO]** §11-N8 · [Kim25CSP] · [Kim25LYC](§2 에 적고 결과 미게재) | 우리 MSD 파이프라인에 **없음** → `kb/open_items.md` **T12** | **우리 공백 — 도입 시 ① 판정축은 self-part 한정 ② 컬러 정규화 기준 명시 필수** |
| **⛔⛔ 계면·대기 pseudo-binary 수치가 *할로겐을 분해하지 못한다* — 문헌 안정성 값을 Cl-rich 논거로 이식하기 전 반드시 확인할 것** — **[Lee24MO]** ESI Table S3/S4 **85행 전수 전사**(→ `db/properties/lee2024_si_84_structures.csv`, 코드 `tools/litdb/lee2024_si_tables_transcribe.py`) 결과: 같은 양이온 골격에서 **Cl↔Br 만 바꾼 8쌍 중 7쌍의 계면 3값(LNO/NCM811/Li)이 소수점까지 완전동일**(나머지 1쌍도 LNO·NCM 동일, Li 만 −456.89 vs −465.89 = **자릿수 전위 오식 의심**), **D₁.₅ 혼합비 뒤집기(Cl₁.₀Br₀.₅↔Cl₀.₅Br₁.₀) 7/7 완전동일**, **I/Cl/Br 3종이 통째로 같은 골격 4개**. LNO 열은 85행에 **고유값 31개뿐**이고 **W↔Mo·Ge↔Sn 도 구분 못 한다**. **그런데 같은 묶음의 σ_RT 는 최대 3.18× 차이**(Li₆.₅Si₀.₇₅W₀.₂₅S₅: I 62.93 / Br 19.82 / Cl 22.79 mS/cm) | **[Lee24MO]** §12-C2 (ESI 실물 독립 검증 2026-08-04) | 우리 `air_hsab` 는 정성 tier — **비교 대상이 없다** | ⛔ **T11(pseudo-binary ΔE_H₂S)에서 '그들 값 이식' 선택지 소멸 → 직접 계산 필수로 승격.** 우리 축은 **Cl-rich** 인데 이 논문 값은 Cl 을 Br·I 와 분해하지 못한다. 단 **양이온 축 결론(ΔE_H₂S 평균 Ge +0.404 / Sn +0.321 / **Si −0.095 eV**, 대기안정 30/30·12/12·**4/30**; 군(1) 내 P계 −0.120 vs Sb계 +0.183)은 전수 검산으로 참** — 다만 **σ↔ΔE_H₂S 순위상관 ρ=+0.04(무상관)** 이라 trade-off 는 [A] 고정 시에만 성립 |
| **⚠⚠ MSD 적합 창을 안 정하면 생산길이 50배도 못 구한다 — *창 고정 + 다중 시간원점*이 우리가 문헌보다 나은 지점*** — **[Lee24MO]** ESI: 생산이 **NPT 10 ns**(우리 NVT 200 ps 의 **50배**)인데 eq S1 은 **원점 통과 `D = MSD/(6t)`** 로 **적합 창도 절편도 없다**. Fig S5(a) 군(1) Li₅.₇₅P₀.₇₅W₀.₂₅S₅I 는 **초기 ~200 ps 에 11 Å² 케이지 plateau** 를 깔고 10 ns 에 겨우 **26 Å²** → 이 추정자는 **plateau 42% 를 확산으로 계상해 D 를 과대평가**한다. 게다가 **Fig S4 픽셀 실측 결과 온도 창이 계마다 다르다**: 군(2)·(3) 은 350–500 K **7점**(본문대로)인데 **군(1) 은 425–600 K 8점**이고 **본문·캡션에 언급이 없다**(그 계만 300 K 외삽 거리 125 K 더 김) | **[Lee24MO]** §12-C4·N8·N10 · [Kim25CSP] HT-FPMD 창 검증 규율과 같은 축 | 우리: **MSD 창 2–50 ps 고정 + 다중 시간원점 평균**(`tools/ionic/msd_refit_window.py`, 2026-08-04) · 600/800/1000 K **3점 공개** · 3-시드 | **🔑 우리 우위 축**: 길이는 밀리지만 **추정자·창 규율은 우리가 낫고, 온도 창을 공개한다.** 원고에서 MSD 규율을 방어할 외부 근거. **동시에 T13(생산 200 ps 타당성 재검토) 신설** — 느린 계의 유효 hop 수 점검 |
| **🔑 CSM(다면체 왜곡)은 *연결방식이 아니라 D* 를 따라간다 — 이 논문의 인과사슬 중 살아남는 고리** — **[Kim25CSP]** 는 `edge-sharing → 왜곡 ↑ → D ↑` 를 팔지만, **Fig 5b(Li₄SiGeS₆) 700 dpi 재판독에서 첫 화살표가 끊긴다**: 가장 왜곡된(CSM 5.5–6.0, 흰색) 상은 edge 가 아니라 **corner rank 8·9·10** 이고, 하필 그 셋이 **Fig 3d 에서 corner 7개 중 유일하게 D≠0**(0.64/0.22/0.14 ×10⁻⁵ cm²/s). edge(rank 5)는 CSM 3–4.5 로 중간. 즉 본문 주장 *"edge-sharing phases in **both compositions** … CSM values are relatively higher"* 는 **Li₄SiGeS₆에서 거짓**이고, **CSM↔D 상관만 남는다**(논문에 상관계수·회귀·오차막대는 **전무** — 전부 육안) | **[Kim25CSP]** §11-6·§19 N5 (본문 실물 독립 검증 2026-08-04) | 우리 host 에는 **corner/edge 축이 정의되지 않는다**(argyrodite PS₄ = 고립 사면체) → 연결방식 축은 애초에 이식 불가 | **⭐ 우리에게 유리한 정정.** CSM 이 "연결방식의 부산물"이었다면 우리 계엔 쓸모가 없었을 텐데, **연결방식과 무관하게 D 를 따라가는 독립 기술자**로 드러났다 → **Li–(S,Cl)₄ CSM 을 기존 UMA-MD 궤적에 후처리(§10c 항목 C)** 하는 근거가 강화. 단 **조성 횡단 검증은 논문에 없다** → 47종엔 "농도별 상대 지표"로만 |
| **⚠ 문헌 기술자를 이식하기 전에 *정의 문장 자체*를 읽을 것 — α 는 한 문단 안에서 뜻이 뒤집힌다** — **[Kim25CSP]** p 47388: *"packing ratio (α), which quantifies proportion of the crystal volume occupied by structural features that **hinder** Li-ion mobility"* → 바로 다음 문장 *"This parameter represents the fraction of lattice space **available** for Li-ion transport"* (정반대). 게다가 **초록·본문이 낮은 α 를 "higher packing efficiency" 라 부른다** — 표준 결정학의 채움률과 방향이 반대라 **그대로 옮기면 뒤집힌 문장이 된다** | **[Kim25CSP]** §19 N2·N3 (2026-08-04) | 우리 **BVSE 채널 %**(above-min ≤ iso, ~0.25 Å voxel)는 **정전 퍼텐셜 기준 + 알고리즘 공개** | **우리 우위 유지 — α 재구현 금지 판정 보강.** 다만 언어는 빌린다: "채널 %" → **"Li-accessible volume vs dead volume"**(§10d 항목 G). 인용 시 **"낮은 packing ratio α"** 로만 쓰고 *"packing efficiency"* 는 쓰지 않는다 |
| **🔴 문헌의 D 를 인용하기 전에 *MSD 궤적 그림*을 볼 것 — 이 논문 D 의 절반은 확산이 아닌 것에 붙은 숫자다** — **[Kim25CSP]** SI Fig S4–S7 의 **MSD 궤적 40개 전수 판독**(2026-08-04): ① **계단형(1회 hop 후 정체) 6건에 D 를 매겼다** — Li₂SiS₃ r8(22–30 ps 계단 후 8.5 Å² 정체)·Li₂GeS₃ r7·Li₄SiGeS₆ **r7(10 ps 도달 후 50 ps 완전 정체 = 확산이 아니라 초기 완화)**·r6·Li₄SiSnS₆ r6·r8 ② **MSD 가 감소하는 구간 2건**(Li₂SiS₃ r5 52 ps 78 → 58 ps 72 Å²; Li₄SiSnS₆ r5 12 ps 4.5 → 16 ps 2.0) — 앙상블/다중 시간원점 평균 MSD 는 **단조증가해야 한다** ③ **40 궤적 중 1개는 60 ps 가 아니라 ~42 ps**(Li₄SiSnS₆ rank 5, **edge**) ④ **MSD 정의식(SI eq 5)이 제곱의 차** $\langle r(t+t_0)^2-r(t_0)^2\rangle$ 로 적혀 있다(올바른 것은 차의 제곱 $\langle [r(t+t_0)-r(t_0)]^2\rangle$) ⑤ 끝 10 ps 에 변위 절반이 몰린 궤적 2건 → **60 ps 가 짧다는 증거가 그림 안에 있다.** 우리가 MSD 끝값→`D=MSD/6t` 로 환산하면 **14 중 13 이 Fig 3 판독과 ±40 % 안** → Fig 3 의 D 는 **전 구간 원점통과 추정자**임이 사실상 확정 | **[Kim25CSP]** §20-M1~M5·§20d (SI 실물 독립 검증 2026-08-04) · [Lee24MO] §12-C4 (같은 랩, 원점통과 `D=MSD/6t`) | 우리: **MSD 창 2–50 ps 고정 + 다중 시간원점 평균**(`tools/ionic/msd_refit_window.py`) · equilib 5 ps 분리 · 600/800/1000 K 3점 · **3-시드 오차막대** · **σ·D 절대값 인용 금지 규율** | **🔑🔑 우리 우위 축이 하나 더 늘었다.** 종전 근거는 [Lee24MO](적합 창 없음)였는데, **같은 랩의 JACS 논문에서 MSD 가 실제로 감소하는 그림**이 나왔다 — *"단일 시간원점 MSD 는 문헌 최상위 저널에서도 비물리적 구간을 만든다"* 는 **직접 인용 가능한 외부 근거**. 원고 Methods 에서 다중 시간원점 평균을 방어할 때 쓴다 |
| **⚠ '2 자릿수 이분법'은 4조성 중 2조성에서만 성립한다 — 인용 시 단서 필수** — **[Kim25CSP]** 의 간판 주장(*"edge 가 corner 보다 D 가 at least 2 orders of magnitude 높다"*)은 **Li₂SiS₃·Li₂GeS₃ 에서만 깨끗**하다(corner 전원 순수 진동). SI MSD 원자료 실측: **Li₄SiGeS₆** 최고 corner **r8 = 28 Å²/60 ps** vs 유일 edge **r5 = 32 Å²** → **1.6배** · **Li₄SiSnS₆** 최고 corner **r6 = 11.5** vs 약한 edge **r5 = 14@42 ps** → **2.6배**. 즉 **4원계로 가면 이분법이 무너진다**. 자유에너지도 같은 패턴 — Fig S8 교차온도가 Li₂SiS₃ 360 K·Li₂GeS₃ 480 K 인데 **Li₄SiGeS₆ 는 방향이 반대**(280 K **위**에서 corner 우세, 영점에너지 효과)·**Li₄SiSnS₆ 는 1000 K 까지 교차 없음** → *"고온에서 edge 가 유리"* 도 **2/4** | **[Kim25CSP]** §20-M6·M13·§20d (2026-08-04) | 우리는 **host 고정**이라 이 축 자체가 없다(argyrodite PS₄ = 고립 사면체) — 그러나 **"조성이 하나 늘면 구조–수송 규칙이 깨진다"** 는 교훈은 우리 **47종 × 3농도 횡단 일반화**에 그대로 적용된다 | **인용 규율**: *"2자릿수"* 는 **Li₂SiS₃·Li₂GeS₃ 한정**으로만 쓰고, 4원계는 *"수배"*. *"준안정 edge 가 고온에서 접근 가능"* 도 **2조성 한정**. ⭐ 우리 자신에게 주는 경고이기도 하다 — **단일 조성에서 세운 구조–수송 규칙을 47종에 그대로 밀지 말 것** |
| **🔑 기술자는 *따로* 가 아니라 *동시에* 걸어야 한다 — CSM 단독 회귀는 반드시 깨진다** — **[Kim25CSP]** Fig S12(α·Li–S₄ 부피·CSM) 를 Fig 3 의 D 와 rank 별로 겹쳐 읽으면 **논문이 한 번도 말하지 않은 패턴**이 나온다: **Li₄SiSnS₆ rank 9(corner) 는 CSM 이 전 표본 최고(≈6, 전부 흰색)인데 D = 0** — 차이는 **Li–S₄ 부피가 5.0–5.7 Å³ 로 최저**라는 것뿐이다. 반대로 D>0 인 rank 2·5·6·10 은 **전부 부피 7.0+ ∧ CSM ≥3**. Li₂GeS₃ 도 동일 — 최고 D(r10, 2.6)는 **부피 高 ∧ CSM 高**, r7·r9 는 **CSM 高인데 부피 低/분산 → D≈0**. ⇒ 경험 규칙 **D > 0 ⟺ (Li–S₄ 부피 ≳ 7 Å³) ∧ (CSM ≳ 3)**, 이 표본 예외 1건(Li₄SiSnS₆ r3 mixed, 경계). ⚠ **우리 판독이지 논문 주장이 아니다** — 표본 ~20 구조·육안 색 판독·상관계수 전무 | **[Kim25CSP]** §20e (SI 실물 독립 검증 2026-08-04) · §19-N5 의 다음 단계 | **`kb/open_items.md` 항목 H(신설)**: §15-C(Li–(S,Cl)₄ 부피 + CSM 을 기존 UMA-MD 궤적에 후처리)를 **두 지표 각각의 회귀가 아니라 (부피 문턱) ∧ (CSM 문턱) 2차원 격자 분류**로 재설계. 문턱은 우리 host 에서 새로 잡는다 | **⭐ 이번 SI 회차에서 실무적으로 가장 값나가는 항목.** 그냥 이식했으면 단일 회귀로 갔다가 rank 9 같은 표본에서 깨졌을 것이다. **가설로만 쓰고 47종 검증 후 주장한다** |
| **⚠ '전수 스크리닝'의 검증 커버리지 감사 — MLIP 논문은 *검증한 계*와 *파는 계*가 다를 수 있다** — **[Lee24MO]** 84 구조 전수 MTP-MD 라지만: ① **MTP 정확도 검증(Fig S3)은 7계뿐이고 혼합할로겐(군 4-2/4-3) 계는 0개** — 논문이 파는 최고성능 38–80 mS/cm 이 전부 거기서 나온다 ② **MTP 가 실험과 맞는다고 확인된 구간은 0.001–14.8 mS/cm** (Table S1 MTP 열 실제 범위) ③ **군(1)–(3) 48구조는 전부 I 기반이라 음이온 배열도 1개** — 6배열 앙상블은 **군(4) Cl/Br 36개에만** 적용됐다(Note S5) ④ Fig S3 패널 (d) 는 본문이 선언한 경계를 **깬다**(5.1 meV/atom > 5, 0.10 eV/Å > 0.09) + **7패널 전부 힘 단위 'meV/Å' 오식**(본문 eV/Å, 1000배) | **[Lee24MO]** §12-N4·N6·N7 | 우리 cascade 도 대리모델 구간 밖 외삽 위험 동일 → **T1(UMA 외삽/검증 대리지표)** | **σ 절대값 인용 금지 규율의 3겹 근거 확보.** 우리 파이프라인에도 **'검증된 구간 vs 주장하는 구간' 명시란**을 넣을 것 |
| **🔴 실험 논문의 단일 Ea 도 창을 확인해야 한다 — *본문 그림이 저온점을 축 밖에 두는* 사례** — **[Huang22]** 는 σ_RT 2.4 mS/cm·**Ea 0.28 eV** 를 초록·본문·결론에 세 번 싣지만, ESI **Fig S4 에는 9 온도(228/240/260/280/298/300/325/350/375 K)의 Nyquist 원자료**가 있고 **본문 Fig 4b 에는 5점(280–375 K)만** 실렸다 — x축이 1000/T = 2.6–3.6 이라 228/240/260 K (4.386/4.167/3.846)는 **축 밖**이고 본문은 적합 창을 밝히지 않는다. 우리가 9패널을 600 dpi 로 픽셀 판독해 재구성하니(R = 3476/1524/437.1/162.8/65.30/62.67/27.73/14.93/11.79 Ω) **고온 가지 0.278 eV(280–375 K, 잔차 0.085 dec) vs 저온 가지 0.347 eV(228–280 K, 잔차 0.012 dec)**, **교점 298.5 K** — 즉 **꺾임이 정확히 실온에 있다**. 고온선을 아래로 외삽하면 실측 σ 를 **228 K 2.30배 · 240 K 1.94배 · 260 K 1.45배 과대평가**한다. 저온 가지 잔차가 2.9 % 라 잡음이 아니다. (교정 검증 4중 통과 — Fig S4 R(228) 3476 Ω ↔ Fig S5 등가회로 3530 Ω 1.5 % · Fig 4b 5점 온도 ↔ Fig S4 패널 온도 ≤0.2 K · 펠릿 두께 5점 역산 편차 4 % · 그 두께로 σ(298) 2.44e-3 ↔ 초록 2.4e-3) | **[Huang22]** §11 E1 (ESI 실물 독립 검증 2026-08-04) · 코드 `tools/litdb/huang2022_si_figs.py` | 우리: **600/800/1000 K 3점 + 400/500 K 제외 판정을 CLAUDE.md 에 명문화** · MSD 창 2–50 ps 고정 · Ea 오차막대 600 K 3-시드 | 🔑 **우리 창 규율의 외부 방어 근거가 계산이 아니라 *실험*에서 나왔다.** 종전 사례([Lee24MO] 원점통과 D, [Kim25CSP] 단일 60 ps, [KimLYC] 외삽 증폭)는 전부 시뮬레이션이었는데, 이건 **JACS 실험 논문이 자기 ESI 원자료의 절반을 본문 그림 밖에 둔** 사례다. **인용 규율: 문헌 Ea 를 옮길 때 창을 함께 적고, 창이 없으면 옮기지 않는다.** 그리고 '실온 σ 가 높다'와 '저온에서도 그렇다'는 별개다 — **이 물질은 실온 아래에서 Ea 가 0.35 eV 로 올라간다** |
| **⚠ BVSE·채널% 가 *원리적으로* 못 보는 것 — Li–Li 배제. 그리고 우리 BVSE 는 그들 BVSE 와 *양이 다르다*** — **[Huang22]** 의 n-Li₂SiS₃ 를 Table S1 좌표에서 P4₂2₁2 대칭연산으로 직접 전개해 보면 **Li1–Li2 = 2.396 Å**(Li1 당 2쌍, 셀당 8쌍) · **Li2–Li2 = 2.687 Å**(셀당 4쌍)인데 정련 점유율이 **g(Li1) + g(Li2) = 0.866 + 0.552 = 1.418 > 1** 이다 — 2.4 Å 쌍이 배타적이려면 합이 1 이하여야 한다. 평균장으로 세면 **셀당 5.04 접촉 < 2.75 Å**(셀 안 Li 는 7.88개). 논문은 부분점유를 *"average distribution … characteristic of superionic conductors"* 로만 쓰고 **Li–Li 거리를 한 번도 보고하지 않는다.** softBV 계열 BVSE 는 **고정 골격 + 시험이온 1개** 문제라 이 배제를 구조적으로 볼 수 없다. ⚠ 별개로 **함수형이 다르다**: 그들은 *"transferable **Morse-type** SoftBV force field"* → **eV 단위 에너지**(그래서 0.228/0.367 eV 를 실험 Ea 와 같은 축에서 비교한다), 우리 `tools/comp1_v3/bvse_faithful_cubic.py` 는 `bvs += exp((R0−d)/b)` 뒤 **BVSE = (BVS−1)² = 무차원**(cube 헤더도 `valence^2`) | **[Huang22]** §11 E10·E18 (ESI 실물 독립 검증 2026-08-04) · 코드 `tools/litdb/huang2022_si_struct.py` | 우리: `tools/comp1_v3/` softBV(Li–X R0 = S 2.105 / Cl 2.249 / O 1.466, b 0.37), BVSE = (BVS−1)², ~0.25 Å voxel, 채널 % = above-min ≤ iso | **① 한계 서술에 이 사례를 넣는다** — 채널 % 는 *한 개의* Li 가 지날 수 있는 부피이지 *동시에 몇 개가* 지날 수 있는지가 아니다. Li 농도가 높은 계일수록 과대평가 방향이다. **② 축 혼동 금지** — 우리 채널 % 를 그들 eV 장벽과 같은 축에 놓지 말 것. **경로·순위 비교는 유효, 장벽 크기 비교는 무효.** **③ 해상도 확인 항목 유지** — 그들 0.1 Å vs 우리 0.25 Å |
| **⚠ BVSE 장벽 절대값을 σ 개선 서사로 쓴 출판 사례 — 자기 실측과 3× 불일치** — **[WangYO]** Y₂O₃ 5% 공도핑(Y@P4b 주장)으로 σ 2.75→3.53 mS/cm(+28%)·Ea 0.375→0.34 eV(실측, 그림 판독)인데, 기전 근거로 **BVSE 랜드스케이프 최대값 1.11→0.61 eV "절반"**을 헤드라인. ① 개선 *후* BVSE 값(0.61)이 개선 *전* 실측 Ea(0.375)보다 크다 ② 입력=Rietveld 셀에 **이산 Y/O decorate 정렬 스냅샷**(라벨 Y2·O70; 관례셀 Y 1개면 P의 25%=실험 5배 과도핑) ③ P⁵⁺→Y³⁺는 전하 −2라 BVSE 정전항이 국소 하강하는 게 반자동(방법 내재 편향) ④ 배열 앙상블·iso-level·경로 정의 미공개 | **[WangYO]** Fig 2d,e·S11 (softBV 계열 플랫폼+SoftBV 0.1 Å) | 우리: BVSE=(BVS−1)² 무차원·채널%만·원본 주기셀·**장벽 절대값/순위 인용 금지**; cascade **bvs_li_proxy 0.83–0.92로 M³⁺ 종류 무관 균일**(Y₂O₃ 포함, UMA·modelc host — "M³⁺가 Li 이동도를 절반 낮춘 장벽으로 올린다"는 그림과 방향 상충, 단 사이트 모델이 P vs Li로 다름) | **[Huang22] §11 E10·E18과 같은 계열의 반면교재 2호** — softBV-eV 장벽을 실험 Ea 축에 올리는 관행. 우리 규율(채널%-only) 한계 서술에 인용 |
| **A ⚠ HT 스크리닝이 쓰는 *이동장벽 프록시*(softBV)는 우리 Ea 와 같은 표에 못 놓는다 — 그리고 폴리모프로 2.1× 흔들린다** | (규율 — 우위 아님) | **[Honrao21]** `Table S1`·`Table 4`·`Fig. S8` | 그들 값은 **경험적 softBV**(BV 미스매치 → Morse 환산, **구조 완화 없음**, 단일 폴리모프)이고 논문 자신이 *"softBV barriers should not be used to directly estimate the ionic conductivity"* · *"tend to be overestimated"* 라고 적는다. ⇒ 우리 `Ea`(**comp1 0.253 / modelc 0.224 eV**, UMA-s-1p1 MLIP-MD 600/800/1000 K, MSD 2–50 ps)와 **다른 양**. ★ **결정적 실측**: 같은 `LiCl` 이 **0.349 eV**(mp-1185319, `Table S1`) ↔ **0.735 eV**(mp-22905, `Table 4`) = **2.11×** — 그런데 그들 SE 게이트가 **0.5 eV** 라 **구조 선택이 통과/탈락을 가른다**. ⇒ 우리 BVSE 규율(*"정량·순위는 원본 주기셀 값만"*)의 **외부 실증**. `Fig. S8` parity 는 0–0.5 eV 구름이 **y=x 위**(저장벽 양의 편향, figure-read)로, SHAP `f(x)` > softBV 관계와 같은 방향(0.198>0.185 · 0.134>0.122 · 0.127>0.109) |
| **A ⛔⛔ 문헌 HT 깔때기가 *우리 계와 현대 할라이드 SE 를 잃는 두 지점* — 이유가 전도도가 아니다** | **우리 우위(범위)** | **[Honrao21]** 본문 Screening 절 · `Table 4` #6 | ① **`E_hull ≤ 30 meV/atom` 게이트**: *"the argyrodite `Li₆PS₅I` is identified, but **`Li₆PS₅Br` and `Li₆PS₅Cl` are excluded due to their higher E_hull values**"* (LGPS 도 **32 meV** 로 탈락, `Li₁₀SiP₂S₁₂` 는 통과) ⇒ **`comp1`·`modelc` 가 후보 목록에 없다** — 물질이 나빠서가 아니라 **아지로다이트가 본질적으로 Cl/S 자리무질서 물질**이라 정렬 근사가 hull 위로 올라가기 때문. ② **`0.5 eV` softBV 문턱**(본문 표현 *"arbitrary cutoff"*): `Li₃YBr₆` **0.55** · `Li₃ScCl₆` **0.56** · `Li₃InCl₆` **0.59** 가 전부 *"just above"* 로 탈락 — **`Li₃InCl₆` 는 같은 논문 `Table 4` 에서 DFT-MD 가 σ>10⁻⁴ S/cm 로 판정한 물질**이다(**자기 데이터 안의 위음성**). ⇒ 원고의 *"문헌 스크리닝이 우리 물질을 빠뜨린다"* 를 쓸 때 **이 두 원인을 이름으로 댄다**: 무질서를 못 담는 `E_hull` · 완화를 못 담는 BV 프록시 |
| **A ✅ 계보 안에서 전도도 축을 *1차 게이트*로 세운 유일한 편 — [Aykol16]·[Nolan21] 의 함정을 둘 다 피한다** | (계보 판정 — 우위 아님) | **[Honrao21]** SE `3D ≤0.5 eV` · 코팅 `3D ≤1 eV` | **[Aykol16]** 은 `−E_c>3.5 V` 로 **전도체를 잘랐고**(`Li₂ZrO₃`·`LiAlO₂`), **[Nolan21]** 은 **전도도를 아예 안 봤다**(`Table S4` 가 스스로 `10⁻¹⁵`~`10⁻¹⁸` S/cm 를 싣고 방어는 *"nm 두께면 된다"* 한 줄). **[Honrao21]** 은 전도도를 **요구**한다 — ⇒ *"게이트가 Li 전도체를 배제하는가"* 의 답은 **편마다 다르고, 세 가지 서로 다른 함정이 있다**: ⓐ 전도체 절단 ⓑ 전도도 무시 ⓒ **전도도는 봤는데 프록시·준안정성으로 잃음**(본 편) |
| **★★ "Li 가 많이 움직인다" 는 σ 의 대리지표가 아니다 — 총 점프 수는 그대로인데 σ 가 2×10³ 배 달라진다** — AIMD 700 K 기준 총 기본점프 수가 x=0 (≈60) 과 x=0.75 (≈65 Å⁻³ns⁻¹, `Fig. 6b` figure-read) 로 거의 같고, 케이지 **안** 점프(T5↔T5·T5↔T2)가 x=0 에서 전체의 **>98 %** 다. σ 를 만드는 것은 **케이지 경계를 넘는 극소수 점프**뿐이며 그 300 K 빈도만 **2.0×10⁶ 배**(digest 검산 ✓) 바뀐다 | **[Jeon26Con]** `Fig. 6a–c` · `Table 4` · `Table S7` | 우리 표준 보고는 **MSD·D·Ea** 뿐이지만, 도구는 이미 있다 — `tools/ionic/aimd_jump_stats.py` 가 **케이지 중심(자유 음이온) 기준 inter-cage hop 율**과 van Hove Gs(r,Δt) 를, `cage_jump_descriptors.py` 가 intra/inter-cage 48h–48h 거리를 낸다. ⚠ 다만 **"총 점프 수 대비 케이지간 비율" 로 묶어서 보고한 적이 없고**, BVSE 채널%(`tools/comp1_v3/`)와 **짝지어진 적도 없다** | 🔑 **규율로 채택 후보.** MSD 총량·확률밀도 부피·BVSE above-min 부피는 **연결성(percolation) 지표가 아니다.** `Fig. 6a` 의 "끊어진 케이지 → 연결된 3D 망" 이 그 시각화 — 우리 BVSE 그림과 같은 메시지의 MD 판 |
| **★ 협동 이동은 "빈도"만 도펀트로 조절되고 "성질"은 안 바뀐다 (⇒ cascade 축이 하나 생긴다)** — 700 K, x = 0→0.75 전 구간에서 참여 Li 수 **2–6**(평균 3.31–4.50)·지속시간 **0.03–3.40 ps** 가 x 에 **거의 무관**하고, 바뀌는 것은 **사건 빈도**(T5→T4→T5 3.7×10⁻³ → 0.25 Å⁻³ns⁻¹)와 **성공률(10 % → 37.4–41.9 %)** 이다. 지렛대는 **국소 음이온 전하**(S₁₆ₑ −0.93 → −1.45 e; 확산 경로 주변 S 가 0.49–0.62 e 더 보유) | **[Jeon26Con]** `Table S8` · `Table S9` · `Fig. 2a` · `Fig. S10/S11`(본문 인용) | 우리 도핑 캠페인(Nd/O·B₂O₃ 등)은 **Ea·D 만 본다** — "성공률"·"협동 사건 빈도" 를 관측량으로 쓴 적 없다. Bader·ICOHP 는 이미 낸다 | 🔶 **방향만 이식.** 값은 As/Si+I 계라 금지. 우리 쪽 번역 = *"도펀트는 협동을 만들지 않는다 — 이미 있는 협동 사건의 성공률을 올린다"* ⛔ 단, 이 논문의 참여 Li 수·지속시간은 **그룹화 문턱이 SI 에 없어 재현 불가** ⇒ 관측량으로 채택하려면 **우리가 문턱을 정의해야 한다** |
| **★★★ Li 함량을 고정해도 Cl 이 많을수록 빠르다 — "전도도를 올리는 것은 Li 개수가 아니라 음이온 부격자다"** — DeePMD-MD ≈91조성 지도의 **등-Li 선(Li = 7 − 2·Mg − Cl)** 을 따라 읽으면, **Li = 5.5 로 고정한 세 점** (Cl 1.5/Mg 0) · (Cl 1.0/Mg 0.25) · (Cl 0.5/Mg 0.5) 에서 **σ(300 K) = 44.0 → 29.7 → 7.7 mS/cm (5.7×)**, **Ea = 0.191 → 0.202 → 0.238 eV (+47 meV)** (`figure-read`, digest 가 `Fig. 5` 컬러바를 픽셀 역변환). 실험도 같은 방향 — Mg 도핑 4조성에서 Cl 1.0 → 1.5 로 갈수록 σT 가 올라간다(`Fig. 6`) | **[Muy25Dop]** `Fig. 5`(Mg–Cl 패널) · `Fig. 6` · digest §3.2 | 우리는 comp1(Cl 1.0) → modelc(Cl 1.6) 에서 **D 2.6×↑ · Ea↓** 를 본다. ⚠ 우리 두 조성은 **Li 함량이 같지 않다**(6.0 vs 5.4) ⇒ 우리 데이터만으로는 "Li 수 효과"와 "Cl 효과"가 **분리돼 있지 않다** | ✅ **방향 일치 + 우리가 못 한 분해를 대신 해 준다.** 🔑 **이식 1건**: 우리도 **등-Li 조성쌍**(예: Li 5.4 를 고정한 Cl/Mg 또는 Cl/vacancy 짝)을 한 쌍이라도 계산하면 *"Cl-rich 가 빠른 것은 Li 를 빼서가 아니다"* 를 **우리 손으로** 말할 수 있다. ⛔ σ 절대값(7.7–44 mS/cm)은 소환값이고 규약 부재라 우리 표와 같은 칸에 넣지 않는다 |
| **⚠ Cl 상한 1.5 — 그 위는 "이차상이 생기기 시작하는" 영역이다** — MD 조성 격자의 Cl 상한을 **1.5 로 잘랐고**, 근거로 Gautam 2021(`Li₇₋ₓPS₆₋ₓClₓ` 중성자회절)을 든다. 하한도 잘랐다 — **Cl ≥ 0.25(Mg 계) / 0.5(Si 계)**, 이유는 *"순수 Li₇PS₆ 의 입방상은 RT 에서 불안정"* | **[Muy25Dop]** 본문 §3.3 | **우리 modelc = Li₅.₄PS₄.₄Cl₁.₆ 은 Cl = 1.6 으로 이 범위 밖이다** | ⚠ **경계 정보로 반드시 기록.** 이 논문의 σ·Ea 지도를 우리 조성까지 **외삽하지 않는다.** 그리고 우리 modelc 를 "단상" 으로 전제하는 서술이 있다면 **외부 근거가 필요**하다(우리 XRD 없음) |
| **★★ 우리와 *같은 규약*의 Haven 비를 낸 유일한 argyrodite-계 AIMD — 그리고 저자도 그 보정을 σ 에 적용하지 않았다** — 본문 *"The inverse of Haven ratios … are **1.3 and 1.5**"* (Li₆POS₄(SH) / Li₆.₂₅PS₅.₂₅(BH₄)₀.₇₅) ⇒ **H_R = 0.769 / 0.667**, **σ_true = 1.30× / 1.50× σ_NE** (digest 계산). Methods 의 σ 식은 **tracer D 를 그대로** NE 에 넣는다 = **H_R = 1 규약**. ⛔ **Li₆.₂₅PS₅.₂₅Cl₀.₇₅ 의 H_R 은 보고 안 됨** ⇒ *"우리 계에서 σ 가 몇 배 틀리나"* 는 **이 논문으로 답할 수 없다** | **[Fang22PW]** 본문 p4 + Methods (`D_c` 정의식) | 우리 **NE, H_R = 1 고정** · 자체 실측 **0.84 ± 0.06**(⚠`citable:false`) | **✓ 규약 동일 · 값 같은 대역** |
| **⚠ Ea·D 대비 — real difference 아님(조성 *방향*·힘계산 둘 다 다름)** — [Fang22PW] **Li₆.₂₅PS₅.₂₅Cl₀.₇₅ (S-rich, Cl 0.75)**: Ea **0.210 eV**(700/600/500 K **3점**), σ₃₀₀K **14 mS/cm**(3점 외삽), **figure-read D(600 K) ≈ 5×10⁻⁶ cm²/s**. 그들은 **AIMD(VASP PBE)**, 우리는 **MLIP-MD(UMA-s-1p1)** | **[Fang22PW]** `Fig. 1C` (표 + Arrhenius, figure-read) | 우리 comp1 **0.253 eV / 3.09×10⁻⁶** · modelc **0.224 eV(단일궤적) / 0.197±0.032(3-seed) / 7.90×10⁻⁶** cm²/s | **~ 자릿수 일치, 일치 주장 금지** |
| **★ "billiard-ball" — 국소(intra-cage) 확산이 Li–Li 반발로 릴레이돼 장거리 전도를 만든다. 클러스터 없이 *할로겐 argyrodite 에서도* 성립** — `Fig. S11`(Li₆.₂₅PS₅.₂₅Cl₀.₇₅ @500 K) 결합 Event 3개가 **전부 S_d(할로겐 자리의 S²⁻) 주변**에서 발생, 연쇄 간격 **~0.6–3 ps**. ⛔ **트리거가 S_d 라는 점이 우리와 반대다** — modelc 는 Cl 을 S 자리에 넣은 계라 **S_d 가 원리적으로 없다**. 기전 자체(Li–Li 반발 릴레이)는 도관 종류와 무관하므로 **우리 궤적에서 따로 확인할 문제** | **[Fang22PW]** `Fig. S11` + Discussion 4요인 | 우리 `aimd_jump_stats.py`·`cage_jump_descriptors.py` 로 확장 검출 가능 (Eq.(1) 3-파라미터 필터 미구현) | **미검증 (우리 축으로 안 재봄)** |
| **★★★ A-Jiang-1. MD 로 뽑은 Ea 는 힘 엔진과 무관하게 실험보다 0.05–0.09 eV 낮다 — 그리고 그건 입계 탓이 아니다** — Jiang **AIMD(DFT 힘)** Li₆PS₅Cl **0.282** vs 실험 0.34 (**−0.058**) · Li₅.₅PS₄.₅Cl₁.₅ **0.244** vs 0.29 (**−0.046**). [Wang25DPA] 전용 MLIP −0.084. **Adeli 의 PFG-NMR(벌크·무전극) Ea 가 EIS 와 오차 내 일치**(0.35 vs 0.34 · 0.29 vs 0.29) ⇒ **GB 로 설명 불가** | **[Jiang22Se]** `Fig. 3` + 본문 §3.2.1 · 실험은 **[Adeli]** Table (EIS·PFG) | comp1 **0.2532 eV**(⚠ provisional · `blocking_gate=diffusive_regime_gate`, **gate_outcome = not_assessed** · `cite_until_beta_gate_passes`) vs 실험 0.34 ⇒ **−0.087**; modelc **0.2235**(단일시드 앵커) / **0.197 ± 0.032**(3-seed) vs 0.29 ⇒ **−0.067 / −0.093** | ✅✅ **다섯 추정치가 전부 같은 방향·같은 크기.** ⇒ **힘 엔진(DFT / 전용 MLIP / 범용 MLIP)이 아니라 *프로토콜* 이 원인**이라는 가설을 이 편이 크게 밀어 준다(Wang25 digest 가 제기한 그 질문의 답 쪽). **용의자**: 고온 외삽 · 짧은 궤적 · 단일 무질서 배열 · 비확산 저온점 포함 · 단일 아레니우스 직선 |
| **★★ A-Jiang-2. σ 가 실험과 5 % 내로 맞는 것은 검증이 아니라 두 편향의 상쇄** `digest 계산 (원논문 미보고)` — ① Ea 0.05 eV 저평가 ⇒ 298 K σ **×7.0 과대** ② Haven=1 (Adeli 실측 **H_R 0.23–0.30**) ⇒ σ **0.23–0.30× 과소**. 곱 ≈ **×1.8**, 나머지는 AIMD 산포 안 | **[Jiang22Se]** σ 2.592/8.916 vs **[Adeli]** 2.5/9.4 · H_R 은 **[Adeli]** ⁷Li PFG | 우리도 **Nernst–Einstein Haven=1** · σ 절대값 **인용 금지**(CLAUDE.md) | ✅ **우리 금지 규율의 정량 근거.** 그리고 **Haven=1 가정의 크기가 3.3–4.3배**라는 숫자를 처음 확보 ⇒ 앞으로 σ 를 낼 일이 생기면 **H_R 을 보고량 카드에 명시**한다 |
| **★★ A-Jiang-3. Cl-rich 가 빠른 이유의 시각적 증거 = inter-cage 연결** — `Fig. S4` 500 K · 120 ps Li 궤적밀도: **Li₆PS₅Cl 은 서로 끊긴 케이지형 3덩어리**(inter-cage 미연결), **Li₅.₅PS₄.₅Cl₁.₅ 는 셀 관통 연결망**. MSD 도 정합(`Fig. S2a` 500/600 K 평탄 vs `Fig. S3a` 600 K부터 선형) | **[Jiang22Se]** `Fig. S4a,b` · `Fig. S2a` · `Fig. S3a` | 우리 BVSE 채널% · percolating bottleneck · comp1→modelc D 2.6×↑ | ✅✅ **우리 서사와 같은 물리, 더 좋은 그림.** ⇒ **우리도 같은 형식을 낸다**(궤적은 이미 있다). **[Liu]**(AdvFM 2022, intra→inter-cage 활성화)·**[deklerk2016]** 와 3중 정합 |
| **★★ A-Jiang-4. 그런데 바로 그 그림이 저들의 아레니우스를 무너뜨린다** — `Fig. S4a` 가 500 K 에서 Li₆PS₅Cl 이 **확산영역이 아님**을 보여주는데, 500 K 와 600 K 가 6점 아레니우스에 **그대로 들어간다** | **[Jiang22Se]** `Fig. S4a` ↔ `Fig. S2f` | 우리 **확산영역 게이트**(D_inc plateau · 창 안정성 · 홉 수; β 하드게이트는 2026-08-27 폐기) · 600/800/1000 K 3점(400/500 K 제외 판정) | ✅✅ **우리 게이트의 존재 이유를 외부 논문이 실물로 보여준다.** 우리가 400/500 K 를 뺀 판정이 옳았다는 근거 |
| **★ A-Jiang-5. Se 는 σ 를 올린다 — 그러나 크기는 방어되지 않는다** — Li₆ 계열 2.592→15.397 (**5.94×**, ⛔ 논문은 "7-fold"), Li₅.₅ 계열 8.916→19.286 (**2.16×**); Ea 0.282→0.203 / 0.244→0.144 eV | **[Jiang22Se]** `Fig. 3a,b` (값이 그림에 인쇄됨) | comp2 실측: `MD_Ea_eV_ordered` **0.2755 ± 0.0327**(3 seed) vs anion-disorder 앙상블(3 config) = ⚠ **정밀 인용 금지**, *"ordered 보다 낮다"* 까지 · **config 산포 45 %** | 🔶 **부호는 신뢰, 크기는 불가.** 저들 Se 전체 효과(Li₆ 계열 **0.079 eV**)가 **우리가 잰 배열 효과와 같은 자릿수이거나 그보다 작다** ⇒ 조성별 Ea 추세에 **Se 효과 + 배열 효과가 분리 안 된 채 섞여 있다** |
| ⛔ **A-Jiang-6. Ea 0.144 eV / 0.203 eV 는 인용 금지** — `Fig. S3e` 픽셀 측정: 파랑(Li₅.₅PS₁.₅Se₃Cl₁.₅, 범례 0.144)이 초록(무도핑, 0.244)보다 1000 K 에서 **0.45 decade 위** → 500 K 에서 **0.14 decade 위** ⇒ **기울기가 더 급하다 = Ea 가 ~0.06 eV 더 커야 한다**(축 보정 불필요한 상대 읽기). `Fig. S2f` 의 Li₆PSSe₄Cl(0.203)도 같은 반전 | **[Jiang22Se]** `Fig. S2f` · `Fig. S3e` (digest §10-9 픽셀 측정) | — | ⛔ **자기 그림과 범례가 어긋난다.** 다른 계산에서 온 값인지, 피팅 구간이 다른지 논문이 말하지 않는다 |
| ⚠ **A-Jiang-7. AIMD 규약 미기재 목록** — timestep · Nosé 질량 · **MSD 창** · 피팅 구간 · 절편 자유/강제 · 시드 수 · 오차막대 정의 · Haven 비 **전부 없다**. 있는 것: NVT-Nosé · 6온도(500–1000 K, `Fig. S2f`/`S3e` 마커로 확정) · 120 ps · Γ · 300 eV · 1 K/fs 가열 | **[Jiang22Se]** 본문 §2 + `Fig. S2f`/`S3e` | **MSD 창 2–50 ps 고정 · 자유절편 · 600/800/1000 K · equilib 5 ps + prod 200 ps · modelc 3-seed** | ⛔ **이 한 줄이 위 표 전체를 "추세·부호" 로 제한한다.** 단 **A-Jiang-1 의 Ea 결손은 규약 미기재와 무관하게 성립**한다(그들 값 vs 그들이 인용한 실험값의 차이라서) |
> 인사이트: 우리 AIMD가 실험·문헌 trend 재현 → 신뢰. 절대 σ는 RT 외삽이라 Arrhenius로 비교. **[KimICCF]: 같은 그룹 실험이 "σ 병목은 bulk가 아니라 미세구조(공동)" 를 직접 보여줘 우리 'lever=interphase' 결론을 실험으로 보강** (GeoDict σ 1.96/2.10 sim ≈ 1.95/2.17 exp). **[KimCA]: 같은 그룹이 양극 측에서 "device σ_e·성능은 코팅 형상·도전재 차원(미세구조)이 지배, bulk 아님" 을 직접 보여줘 같은 결론을 cathode-side로 확장** (CA 양 아니라 분포·연결성; Super P 과잉이 오히려 σ_e 3,000배↓). → **[KimICCF](sheet/anode) + [KimCA](cathode σ_e) + [Cha](cathode 계면 호환성) = 우리 'lever=interphase/microstructure, not bulk σ' 결론에 *세 우리 그룹 실험*이 수렴** (특히 [Cha]는 σ와 성능이 *역경향*인 가장 깨끗한 반례: σ 1등 LIC가 성능 꼴찌).**

> 🧭 **Framework note — *수송이론 어휘* (transport-theory vocabulary, NOT a materials comparison)** [외부/theory `papers/dyre2004_hopping_models_ion_conduction_noncrystals.md`]: **Dyre & Schrøder hopping-model 리뷰**(비결정질 유리·고분자; **argyrodite 아님 — 결정질**). 위 표 *어느 행에도 수치로 들어가지 않음*, "일치" 금지. **site-percolation 논문의 *수송 짝*** — "Li가 *어떻게 hop하나*(σ(ω)·Arrhenius Ea·Haven)"의 표준 vocabulary만 제공. 핵심 어휘 4개: **(1) inter-cage hop = percolation 병목 = dc Ea 율속** (Dyre §3·Fig 2: "무한히 멀리 가려면 percolation cluster 위 *최대 병목 장벽*을 넘어야"; intra-cage는 빠름·non-limiting) — 우리 D(600K) comp1 3.09→modelc 7.90e-6·Ea 0.253→0.224을 "Cl-rich disorder가 inter-cage 병목을 낮춤"으로 *서술*. **(2) 우리 Haven H_R≈0.3–0.7<1 = correlated/concerted hopping = RBM이 *비상호작용으로 끈* 영역**(Dyre §6 한계 #1: "Coulomb+self-exclusion 넣으면?") — RBM=independent baseline, 우리=correlated 보정. **(3) Nd σ-drop 0.52×(D 0.62×)을 hopping 언어로 = "*Ea(0.224→0.227, 사실상 불변)가 아니라* percolation 경로/prefactor를 좁히는 blocking"** (우리 prefactor-dominant 분해 D0 0.65×와 정합; Liu2013 `dopant_blocking_fraction`="창 좁힘"과 같은 방향). **(4) disorder→Arrhenius성** (우리 disorder_ensemble: ordered=600–800K frozen→Ea artifact 1.17; disordered Ea=0.177) ↔ Dyre "*넓은* 장벽 분포일 때*만* percolation이 단일 병목 골라 Arrhenius dc"(분포 좁으면=ordered 오히려 Arrhenius 붕괴). ⚠ **검증 0·수치 전이 0**: argyrodite=결정질 vs 논문=noncrystals; RBM=비상호작용 최소모델(우리 Li⁺=correlated). "disorder→Ea↓"는 Dyre가 증명 안 함(Arrhenius*성*만; Ea*값* 하강은 Minafra/Kraft 추가물리). σ_NE over-experiment는 Haven *반대부호*(설명 안 됨). 무차원 σ̃ vs 우리 eV·S/cm — **절대 같은 표·"일치" 금지**. 순수 해석 어휘.
>
> 🧭 **Framework note — *site-percolation 운반망 이론* (theory backbone, NOT a materials comparison)** [외부/theory `papers/ishikawa2025_site_percolation_cooperative_ion_conduction.md`]: **Ishikawa/Takae/Kurita** — 무질서 치환 결정 LiₓPb₁₋₂ₓBiₓTe rock-salt를 *자체 고전 MD*(WCA+Coulomb)로 풀어 **"장거리 σ = 운반이온이 *site-percolate*할 때만 켜짐"** 을 증명(σ가 x≈0.2서 급등 = FCC site-perc 임계 pc≈0.2 일치; 침투클러스터 이온만 mobile; σ≫σ_NE 2 orders → cooperative knock-on). 위 표 *어느 행에도 수치로 들어가지 않음*("일치" 금지), **단 [Dyre]의 *짝* — Dyre가 "hop은 percolation 병목이 율속"의 *어휘*라면, 이 논문은 "운반*자리*가 percolate해야 망이 생긴다"의 *임계 개념*.** **🔑 우리 cascade에의 4-매핑** (random substitution = 바로 이 계): **(1) tier2 `dopant_blocking_fraction` = 운반 Li 망에서 자리를 빼는 *site-dilution*(점유율 p↓)** → "high-valence dopant가 Li 자리 차단 → σ↓"를 *percolation 임계* 언어로(p가 pc로 접근하면 σ가 *선형*이 아니라 *문턱형*으로 떨어질 수 있음). **(2) `migration_volume_fraction`(BVSE 병목 부피) = *침투하는 저장벽 부피*** (Sec.IV: 실재계는 "저장벽 영역이 percolate할 때 고전도"). **(3) Nd σ-drop 0.52×(D 0.62×) = connectivity/prefactor blocking** — li_transport.json: Nd는 **Ea 0.227≈modelc 0.224 *불변* + D0 prefactor 0.65×·n_Li 0.90× 지배** → 이 논문의 "σ는 *국소 hop장벽이 아니라 망 connectivity*가 지배"와 정확히 같은 방향(= [Dyre] note (3)·sibling 결론과 교차일치). **단 우리 Nd drop=*완만 감소*(망 유지 하 점유율 부분↓), pc 아래 *붕괴* 아님** — "Nd가 percolation 무너뜨림"이라 하면 over-claim. **(4) dual-x(Sc₂O₃ blocking 0.75@x0.25 → 0.25@x0.0625) = "pc 위 유지 vs pc로 밀기"** — 저치환(x0.0625)이 운반망을 pc 위에 두어 σ 보존, 과치환(x0.25)이 망을 차단(Fig.3 0.15/0.20/0.25 침투전환의 우리계 대응 후보). ⚠ **검증 0·수치 전이 0**: 모델계 다름(rock-salt 큰 Te²⁻ vs argyrodite PS₄·S²⁻/Cl⁻)·**pc=0.2 값 직접이식 금지**(저자 Sec.IV: 일반계는 국소구조·CSRO가 장벽 지배·pc≠site-perc)·미니멀 퍼텐셜(공유결합·polarizability 빠짐)·환원단위 σ(σ₀=0.34 S/cm)는 우리 mS/cm와 *다른 척도*·우리 dopant blocking=*화학적*(전하보상·결합변화) vs 논문 dilution=*기하적*. **개념/임계 프레임만** — "우리 LPSCl pc=0.2"·"Nd가 pc 아래 붕괴"·환원단위 σ 등치 전부 금지. anion disorder(S²⁻/Cl⁻ 4a/4d)→σ↑도 "disorder가 percolating path를 연다"는 *정신*만 공유(다른 부격자). 순수 이론 백본.
>
> 🧭 **구조-분지 caveat note — *준층상 ≠ 우리 입방* (principle-only, NOT a numeric comparison)** [외부/이론 `papers/liang2025_quasilayered_argyrodite_li_migration.md`]: **Liang/Bolong Huang 2025** = argyrodite **Li 이동**을 *처음부터* 이론으로 푼 논문이라 위 표(axis A)에 행으로 들어가지만(inter-cage 율속 클러스터), **구조 분지가 우리와 다르다는 점이 가장 중요한 caveat**. **Liang = 준층상 orthorhombic "P2mm"**(저자표기; abstract P2₁2₁2₁ — 표준 P2mm#25≠P2₁2₁2₁#19, 본문 다수표기 P2mm 채택)**, anion 4a/4c, 50% disorder가 *층상* 음이온 골격(S층/halide-cage/halide층/S-cage)을 만듦**; **우리 comp1/modelc = cubic F-43m(#216), anion 4a/4d, S²⁻/Cl⁻ 4a↔4d 교환·등방**. **🔑 전이 가능한 것 = *원리 2개***: (1) **anion-site 기전** — "어느 음이온이 어느 자리에 앉느냐가 Li 이동을 지배"(우리 S/Cl on 4a/4d ↔ Liang 4c-halide 약결합·4a-S 고활성), Liang은 이를 **Mayer bond order**(Cl–Li ≤0.5×S–Li)로 *정량* = 우리 anion-site 서사의 *결합차수 평행본*; (2) **connectivity 율속** — inter-cage(Liang은 inter-*layer*)가 거시 σ 율속(NEB 0.12 ≈ AIMD 0.088 eV), [Rao11]BVSE·[Perc]site-perc·[Dyre]hopping과 *같은 율속 단계*의 *AIMD 궤적+NEB 4번째 근거*. **⚠ 전이 금지**: (a) **inter-layer ≠ inter-cage** — Liang 층간 = *비등방*(σ_up/σ_down≤2.07), 우리 cage간 = *등방*; "Liang이 우리 inter-cage를 검증"이라 하면 틀림. (b) **Ea 수치 직접등치 금지** — Liang 0.088/0.12 = 준층상 halide층의 *유난히 낮은* 값(widening+AIMD 외삽+방법차)이라 우리 0.25(입방평균)·[Rao11] 0.27–0.35와 *직접 비교 위험*. (c) **σ 절대값 금지** — AIMD 고온(500/700/900K) 외삽이라 Cl σ=1.18 S/cm 등 과대(우리 UMA-MLIP σ 3–5× 과대와 동급 caveat), trend·ratio만. (d) **실험 0** — P2mm 준층상 argyrodite가 *실재*하는지(합성·XRD) 미검증; disorder를 *강제* 구성한 모델. (e) **산화/gap/기계 = 범위 밖**(n/a) — Liang은 *Li 이동*만, axis B/C/D와 교집합 없음. **dual-x 평행**: Liang 2축(halide×cage-cation) σ↔Mayer-uniformity 상관 = 우리 dual-x(Sc₂O₃ 0.75@x0.25→0.25@x0.0625)·cascade 디스크립터 탐색의 *방법 거울*(개념만).
>
> ⚠ **유추 전용 note — *재료 비교 아님* (NOT a materials comparison)** [EXTERNAL `papers/liu2013_cage_methane_adsorption_hydrate_nucleation.md`]: **가스 수화물(물 cage + 메탄) 논문** — argyrodite 아님, 위 표 *어느 행에도 들어가지 않음*, 수치 대조 금지. **전이 가능한 *개념 멘탈모델* 하나만**: Liu 2013은 classical-MD PMF로 "**cage 면(window) 크기가 guest의 trap-vs-cross를 자유에너지 장벽으로 결정**"(면 4→6각 흡착 E_a 11.7→21.3 kJ/mol↑, **7각부터 guest 통과=inter-cage 확산**)을 보였다. 이를 우리 Li⁺ **inter-cage hopping**을 *말로 설명*하는 비유로만 차용 — 우리 cascade **`migration_volume_fraction`(BVSE bottleneck volume)= "유효 창 크기"**, **tier2 `dopant_blocking_fraction`= "dopant가 inter-cage 창을 좁혀 장벽↑"**(우리의 high-valence dopant blocking·stability↔mobility trade-off, Nd-doping σ300 0.52×/D 0.62× drop을 *왜*로 직관화: dopant가 bottleneck 위/근처에 앉아 창 조임). **검증 0·수치 전이 0** — 다른 시스템(물cage/CH₄ vs PS₄/Li⁺)·다른 결합(vdW·H-bond vs 이온 정전)·다른 방법(MD PMF, 258.5 K·30 MPa vs 우리 BVSE 0 K 정전 / AIMD MSD / NEB). kJ/mol 메탄 흡착 ≠ eV Li hop 장벽 — **절대 같은 표·"일치"로 인용 금지**. 순수 사고 틀.

> 📐 **methods 레퍼런스 note — *재료 비교 아님* (NOT a materials comparison)** [`papers/whitten2023_ups_practical_best_practices.md`]: **Whitten 2023 = UPS(자외선 광전자분광) 실전 best-practice 튜토리얼** (외부·단독·*재료결과無·계산無*). 위/아래 어느 물성축 표에도 *행으로 넣지 않는다*, 재료 수치 대조 금지. **단 하나의 연결 = "우리 계산값을 *어떻게 측정하나*"**: UPS는 우리 DFT가 내놓는 **VBM(S 3p)·일함수 Φ·이온화에너지 IE**를 *실험으로 재는 바로 그 기법*. **🔑 PRIMARY = 산화안정성 valence-side 관측량**: 산화=가전자 전자 빼기 → **깊은 VBM/IE(IE 큼)↔높은 산화 onset**. UPS가 그 밴드엣지 관측량(VBM/IE)을 측정 → 우리 **grand-potential 산화 onset·VBM-vs-grand-potential 분석**(`kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md` §6)의 *valence-side 짝*. **단 위계 명시**: UPS 밴드엣지 = 상한(분해창을 2–3배 과대) ≫ CV/LSV(우리 2.14 V 실험짝) ≥ grand-potential(진짜 분해 onset, S²⁻-limited). 우리 자체증거(보고서 §8): comp1/modelc는 **VBM 달라도 onset 동일(2.14 V)** → UPS-VBM 단독을 "산화창"으로 읽으면 틀림(band alignment로만). dopant 스크리닝(`oxidation_stability_cascade.csv`: 대부분 2.14 V S²⁻-limited, B2O3만 2.317 V로 limiting reaction 이동) test에 UPS(VBM/IE)+CV(onset)가 "VBM 깊이↔onset"이 *언제* 연동하나 판별. **referencing 미묘함**(`concepts/dos_vbm_efermi_methods.md`): DFT 절대 VBM은 셀-기준(절연체 E_F=smearing artifact)이라 비교불가 → **UPS는 분광기 E_F/진공준위 절대기준** 제공 → 우리 **slab-IP 보정 VBM**의 외부 앵커. **XPS(코어=화학상태, 우리 ORCA ΔSCF)와 상보**: XPS=무슨 상, UPS=그 상의 VBM/Φ=밴드정렬/전자이동(같은 장비서 He 램프 추가). Φ/VBM=밴드정렬·정공주입장벽 = 우리 "wide-gap 절연 SEI가 전자차단" 서사의 실험 관측량(단 σ_e 절대값은 별도). ⚠ UPS=표면민감(~1–2 nm)·수직이온화·절연체 직접불가(도전기판 박막+바이어스 필요)·VBM만(CBM은 IPES). **methods 논문이므로 "우리 재료와 일치" 주장 금지 — 연결은 측정-방법 매핑뿐.**


**📎 [Wang25DPA] §A 보강 표 (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_wang2025_pretrained_deep_potential_sulfide_sse.md` §②.

**[Wang25DPA] `wang2025_pretrained_deep_potential_sulfide_sse` — MLIP-MD 로 낸 소환값 (Fig. 6c,d / S10 / S11)**

| 항목 | [Wang25DPA] (MLIP-MD, DPA-SSE) | 우리 (UMA-s-1p1 MLIP-MD) | 판정 |
|---|---|---|---|
| **Ea, Li₆PS₅Cl** | `figure-read ≈ 0.24 eV` (실험 `≈0.324`) | comp1 **0.253 eV** ⚠단일궤적 | 🔵 **0.013 eV 차 — 놀랍게 가깝다.** 그런데 **둘 다 실험보다 0.07–0.08 eV 낮다** ⇒ **같은 방향·같은 크기의 빗나감.** 모델 공통 결함일 수도, **MLIP-MD 로 Ea 를 뽑는 방식(짧은 궤적·NE·Haven=1)의 공통 결함**일 수도 있다. 후자면 **모델을 바꿔도 안 낫는다** — 별도 조사 항목 |
| **Cl-rich σ 추세** | Li₆₋ₓPS₅₋ₓCl₁₊ₓ x=0→0.7 에서 7.8→15.7 mS/cm (**≈2.0×↑**) | comp1→modelc **D 2.6×↑**, Ea↓ | ✅ **방향 일치, 같은 자릿수.** ⚠ **D 비와 σ 비는 다른 양**(V·T 인자) — 직접 등치 금지 |
| **우리 modelc 조성(x=0.6)** | 논문이 안 찍음. 0.5(11.8)–0.7(15.7) 보간 **≈13.7 mS/cm** `digest 계산 (원논문 미보고)` | ⛔ 우리는 σ 절대값 인용 금지 | ⛔ **참고만.** db 미등록 |
| **Br 치환** | 같은 x 에서 Cl 보다 σ 높음(x=0.7: 18.6 vs 15.7). 논문 설명 = 배열 엔트로피(*"possibly"*) | 우리 Br 계 없음 | 🔵 미탐색 축 |
| **★ O 도핑** | `Fig. S11` Li₅.₅PS₄.₅₋ₓOₓCl₁.₅: σ **단조 감소** 11.8→7.0 (x 0→0.30, **−41%**); 실험 9.5→6.0 (x 0→0.25, **−37%**) | LPSOCl 은 **전자구조(gap 2.2309 eV)가 정본**, MD 전도도는 별도 | 🔴 **경고.** **문헌은 O 도핑이 전도도에 불리하다고 말한다**(계산·실험 합치). 우리 +O/+B₂O₃ 를 "개선"으로 쓰려면 **어느 축인지 반드시 명시** — 수분/산화 안정성이지 이온전도가 아니다. `Fig. S11` 캡션이 그 트레이드오프를 그대로 씀 |
| **무질서 = 수송 on/off** | `Fig. 6b`: LPSCl 질서상 MSD 가 `≈11.5 Å²` 에서 **포화**(D→0), 무질서상만 선형(5 ns 에 `≈38 Å²`). 무질서가 `≈7.5 meV/atom` **더 안정** | 우리도 무질서 배열 사용 | ✅ **정성 일치.** ⚠ 논문은 **무질서 배열 생성법을 안 밝힌다**(`50%@4c` 라벨뿐) ⇒ **우리 처리와 정량 대조 불가** |
| **MSD 창** | **미기재** (`D = lim MSD/6t` 정의만) | **2–50 ps 고정·자유절편** | ⛔ **이 한 줄이 위 표 전체를 "추세만" 으로 제한한다** |
| **σ 산출** | Nernst–Einstein, **Haven=1**, `σ₀T^m`, m=−1 | 동일(NE, Haven=1) | ✅ 같은 관례 — 그래서 **같은 방향으로 틀릴 수 있다**(digest §13-10) |

**⛔ [Wang25DPA] 에서 축 A 로 옮기면 안 되는 것**
1. **σ·D 절대값** — 셀·궤적·시드·MSD 창 미기재.
2. *"DPA-SSE 는 실험을 정확히 재현한다"* — `Fig. 6c` 는 5계 중 4계에서 **1.6–2.8× 과대**다.
3. **LGPS 계열 값 전부** — 우리 계가 아니다.
4. `Fig. S5a` 의 개별 분해에너지 — **범례 10색 순환으로 점 특정 불가**.

**📎 [Ou26MS] §A 보강 표 (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_ou2026_microstructural_multiscale_fast_ion_transport.md` §2-b.

| 항목 | **[Ou26MS]** | 우리 | 판정 |
|---|---|---|---|
| Ea (Li₆PS₅Cl 벌크) | **0.3843**(질서) / **0.1985**(25 %) / **0.2162**(50 %) / 0.2158(75 %) / 0.3407(100 %) eV — MTP-MD, α≡1 강제, 3–5 ns 창 | **comp1 0.253 eV** (UMA-MD, 단일 궤적, 2–50 ps 자유절편) | 🔶 **같은 자릿수, 정량비교 금지.** 우리 0.253 이 그들 25 %(0.198)~50 %(0.216) 위·질서(0.384) 아래 ⇒ 우리 comp1 배열이 **부분 무질서처럼 거동**한다는 정성 해석까지만. 힘장·창·추정기 전부 다르다 |
| Ea (Cl-rich) | ⛔ **대응 조성 없음** (그들 축은 화학량론 고정 S↔Cl 교환) | modelc 0.224 (3-seed 0.197±0.032) | 🔴 **비교 불가.** ⚠ 우리 3-seed 산포 ±0.032 가 그들 25 %↔50 % 차이(0.018)보다 크다 |
| D (600 K, 질서 Li₆PS₅Cl 벌크) | **1.724×10⁻⁶ cm²/s** | comp1 **3.09×10⁻⁶** / modelc 7.90×10⁻⁶ | 🔶 우리 comp1 이 그들 **질서** 벌크의 1.8× (그들 50 % 무질서 600 K 벌크값은 미공개) |
| **D_GB / D_bulk** | 질서 Cl **8.79↑** · 25/50/75 % **0.19/0.44/0.38↓** · 100 % 2.85↑ · 질서 Br **64.06↑** · 질서 I **59.25↑** · (LLZO 소환 **9.29×10⁻⁴**) | 🔴 **없다** | 🔴 **우리에게 없는 양.** ⚠ 이식하려면 **GB 폭 2.5 nm 가정**이 딸려온다 |
| **D_macro / D_bulk (입도 의존)** | 50 % 무질서 Cl 300 K: **0.568(5.9 nm) / 0.788(23 nm) / 0.942(100 nm) / 0.993(1 µm) / 0.999(5 µm)** | 🔴 없다 | ⭐⭐ **우리 "벌크 상한" 주석을 정밀화하는 값.** ⇒ *"우리 D 는 **치밀 µm-다결정 상한**(입계 손실 <1 %)"* |
| σ (RT, 50 % 무질서 Li₆PS₅Cl) | 예측 **29.47 mS/cm**(치밀,∞) · QENS 31.01(1.07×) · EIS 최대 4.73(6.2×)·중앙값 0.77(38×) | ⛔ **σ 절대값 인용 금지**(우리 규약) | 🔴 **한 표에 올리지 않는다.** 그들 값도 Λ 가정이 들어간 유도값 |
| Ea vs 음이온 반경 | **질서 벌크 0.799 eV/Å, R²=0.998** (⚠ GB 는 비선형) | 해당 없음 | ⭕ **설계 규칙으로 인용 가능** — 단 "질서 벌크에서만" |
| Meyer–Neldel | **ln D₀ = 8.4605 Ea + 7.1184, R²=0.93, E_MN=118.2 meV** (그림 주석) | 🔴 없다 | ⭕ **기존 궤적 후처리로 즉시 계산 가능** (T1 이식) |
| 격자상수 a (Li₆PS₅Cl) | 본문 **10.28 Å** ↔ 배포 MD 셀 **10.044 Å** (2.4 % 불일치) | comp1 ≈ 10.04–10.055 Å (PBE-D3) | 🟰 **배포 셀과 우리가 사실상 같다.** ⛔ 본문 10.28 을 인용하지 않는다 |

**📎 [Liu26FIRE] §A 보강 표 (5열 별표) (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_liu2026_ai_ready_finetuning_solid_solid_interfaces.md` §②-a.

| 문헌 | 계 | 문헌값 | 우리값 | 판정 |
|---|---|---|---|---|
| **[Liu26FIRE]** `liu2026_ai_ready_finetuning_solid_solid_interfaces` ⚠preprint | **LPSCl 벌크** (계면 아님) | MLIP-MD **σ 0.75 mS/cm** / 자체 EIS **0.89 mS/cm** · **D 4.29×10⁻¹¹ m²/s** · MSD 창 **50–200 ps** · **온도 미기재** · 오차막대 0 | ⛔ 우리 절대 σ 인용 금지 규율 · D 3.09×10⁻⁶ cm²/s **@600 K** · MSD 창 **2–50 ps** · 600 K **3-seed** | 🔴 **직접 비교 불가**. ① 저쪽 MD 온도 미상 ② 창이 다름 ③ 인쇄 D↔인쇄 σ 가 NE 로 **89배** 어긋남(우리 검산) ⇒ **소환값으로도 이식 금지**. ✅ 얻을 것은 **σ_MD vs σ_EIS 를 같은 논문에서 −16 % 로 맞춘 워크플로**뿐 |

**📎 [dK18MD] §A 주석 (값 없음) (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_deklerk2018_diffusion_analysis_md_beta_li3ps4.md` §2-c.

> ⚠ **[dK18MD] 는 이 표에 값을 넣지 않는다** (β-Li₃PS₄, 다른 상). 다만 이 축의 서술 규율 하나를 문헌으로 고정한다:
> **"도핑 개선 배율(D_rel)은 온도의 함수다"** — 같은 설계가 450 K 14× · 600 K 3.2× · 750 K 1.3× 로 무너진 실측이 있다([dK18MD] `Fig. 6` + digest 계산).

**📎 [Jang25As] §A 각주 (표 행 아님) (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_jang2025_thioarsenate_argyrodite_mlip_mechanism.md` §④.

> **[Jang25As] 각주 — Li₆PS₅Cl 의 무질서 열역학** (`Fig. 2b`, 전부 `figure-read ≈`, 판독오차 ±2 meV/atom):
> Ehull(반전 0/25/50/75/100 %) ≈ **24.5 / 23 / 28 / 33 / 34.5 meV/atom**.
> **9조성 중 Li₆PS₅Cl 만 25 % 가 0 % 보다 낮다** — *"적당한 무질서가 열역학적으로 유리"* 의 계산 근거이고,
> `adeli2019` 실측 4d-Cl 점유(0.834)·`deklerk2016` 75 % 최적과 같은 방향이다.
> ⚠ **소환값**: 상도 DB·pymatgen 사용 여부 **미기재**, 그리고 **Li₆PS₅Cl 이 어느 배열에서도 ≈23 meV/atom
> 아래로 안 내려간다**(실제로는 상용 재료) ⇒ **계통 오프셋이 있다.** 절대값 인용 시 이 단서를 붙인다.

**📎 [Fang22PW] BH₄ 계열과 묶어 읽으라는 주석 (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_fang2022_argyrodite_transport_beyond_paddlewheel.md` §5.

§A 에는 이미 `shin2026` 발(**BH₄⁻ 회전이 Li 수송에 기여**, 회전구속 MD 에서 **D 2.0–3.0배 감소**, 31 hop 중 28개가 ±0.2 ps 동반) 행들이 있다.
그 옆에 다음 주석을 붙이면 좋다:

> 🧭 **paddle-wheel 축은 우리 litdb 안에서 갈려 있다 (2026-09-09).**
> **[Fang22PW]**(AIMD, 관찰) = *"회전은 Li 운동의 **반응**이지 원인이 아니다"* ↔ **`shin2026`**(NMR + AIMD, **개입**) = *"회전이 hop 과 인과적으로 맞물린다"*.
> **개입 실험을 한 쪽(shin)의 증거가 더 강하다** (digest §12.4 우리 평가).
> 단 **두 결론이 반드시 모순은 아니다** — Fang 의 *responsive* 성분(Li 통과 시 클러스터가 비켜 주며 장벽↓)은
> **회전을 구속하면 사라지므로** shin 의 "구속 시 D 2–3배 감소" 를 그대로 설명한다.
> 진짜 쟁점은 *"회전이 있어야 빠른가"*(둘 다 예)가 아니라 **"회전이 hop 을 *개시*하는가"** 다.
> ⚠ 서지 확인 필요: `shin2026` digest §2.2 참조표의 **"[50] Fang & Jena 2020 Nat. Commun."** 은
> 제목 서술이 이 논문(**2022**)과 정확히 일치한다 — **연도가 어긋났을 가능성**.
## B. 산화안정성 — **4축 분리 (축 명명 없이 말하면 틀림)**
| 축 | 우위 | 출처 | 우리 값 / 재현 |
|---|---|---|---|
| **B① 산화 onset — *정의 문장의 인용처*** | comp1/modelc **2.256 V** (grand-potential, LiS₄ 제외, MP2026) | **[Xiao20Rev]** 식 (1) `μ_Li = μ⁰_Li − eV` + 식 (2) `Φ = E − n_Li μ_Li` + **정의 문장**: *"the electrochemical stability window … corresponds to the range of voltages over which it is stable (**exactly on the grand potential convex hull**)"*, Li 제외 조성 `c − n_Li` 에서 최소화. **위상도 명시**: *"represents the **worst-case scenario** (no kinetic stabilization)"*, 핵생성 과전압은 전환전극 수준(수백 mV) | ✅ **같은 양·같은 기준·같은 정의.** ⛔ 값 비교 금지 — 리뷰 인용값은 2015–16 hull 세대(황화물 1.5–2.5 V). 🔑 **우리 2.256 V 를 "최악 시나리오 하한" 으로 기술할 근거가 여기 생겼다** ⇒ Zuo CV 2.5–2.7 V·Cronk dQ/dV 2.70 V 와의 0.3–0.5 V 차가 **모순이 아니라 동역학 여유**로 설명된다. ⛔ **우리에게 층 ②(topotactic, 식 3)가 없다 — 상한이 없다** |
| **B③ cathode 계면 — *우리 계가 이름으로 찍힌 첫 그림*** | comp1\|LiCoO₂ **−0.3227 eV/atom** (`InterfacialReactivity(use_hull_energy=True)`, MP2026; 산물 Co₉S₈·Li₂SO₄·Li₃PO₄·Li₂S·LiCl, min @ x=0.5302) | **[Xiao20Rev]** `Fig. 5a` 의 **LPSCl 행 × LCO 열** (ref.67 재수록). 본 digest 픽셀 복원 **figure-read −308 meV/atom** (NCM −298 · LMO −424 · LFPO −100) — **정본은 [Xiao19] Table S2 −339 / −330 / −421 / −101**. 본문 일반화: 황화물↔산화물 양극 **>300 meV/atom**, 기전 **S↔O 교환 + Li₃PO₄ 싱크(−2.767 eV/atom)** | ✅✅ **같은 양 + 같은 계 + 같은 도구**(리뷰가 *"explicit feature in the Materials Project"* 로 지목). 우리 **−322.7** vs 정본 **−339** = **16 meV/atom 차, hull 세대(MP2026 vs MP2018) 로 설명 가능한 범위** ⇒ **계보에서 우리 *조성 그대로*(Li₆PS₅Cl\|LiCoO₂) 가 문헌값과 1:1 대조되는 첫 지점** (⚠ [Nolan18](#7) 이 주는 −0.41 eV/atom 은 **Li₃PS₄**\|LCO 이지 아지로다이트가 아니다). ⛔ figure-read −308 은 인용하지 않는다(§12a: 연노랑 구간 판독 민감도 절반) |
| **B② 산화 분해산물 — *예측 ↔ 실험 관측*** | `interface_reactivity` comp1\|LCO 산물 5종 **Li₃PO₄ · Li₂SO₄ · Li₂S · LiCl · Co₉S₈**; onset 반응 `Li₆PS₅Cl → Li₃PS₄ + LiCl + **S** + 2Li⁺ + 2e⁻` | **[Xiao20Rev]** ⓐ **아지로다이트 산화산물 = 원소 S·폴리설파이드·P₂S_x·LiCl** (예측 ref.64,66,115 ↔ **XPS 관측 ref.116,117 Auvergniot 2017 ×2**) ⓑ **PO₄³⁻·SO₄²⁻ 폴리음이온** (ToF-SIMS ref.78,119) ⓒ **TM 황화물 Co₉S₈·MnS·CoNi₂S₄** (XRD·TEM ref.107, 300 °C) ⓓ **Li₃PO₄ 는 XRD 로 직접 관측**(ref.107) ⓔ S–S 가교 XPS 가 충전에 자라고 방전에 줄어든다(`Fig. 3c`, ref.102) | ✅✅ **우리 산물 5종이 전부 리뷰 안에 예측으로 있고, 그중 Li₃PO₄·SO₄²⁻·Co₉S₈계·LiCl 4종은 실험 관측까지 붙는다** ⇒ **계보 전체에서 우리 산물 목록이 실험과 연결되는 첫 지점**. ⚠ **P₂S₅ 는 XPS 로 직접 관측된 적 없다**(대신 S–S) — 우리 산물 서술에서 "관측됨" 을 일괄 적용 금지 |
| **B① 실측 kinetic onset — dQ/dV "SSE ox." 영역 IV 시작 2.70 V · 본문 "high oxidative tendency of LPSCl at 2.3 V vs Li/Li⁺" · CV(0.1 mV/s) LPSCl/C 산화 피크 ≈2.5 V(figure-read)**; 완전산화 산물 **S + LiCl + P₂S₅**, 중간체 **LPS**(`Li₂S + Li₄PS₄ ⇌ Li₂.₅PS₄ + S + 3.5 Li⁺/e⁻`, Q_rev ≈ 350 mAh g⁻¹) | (우위 아님 — **정합 확인**) | **[Cronk26]** `Fig. 3a–d`·`Fig. S13`·p6 (LPSCl 80 : C 20 wt%, Li-In, 75 MPa) | 우리 grand-potential 산화 onset **2.14 / 2.256 V**(comp1, LiS₄ 제외) · [Zuo] Eq1 `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li`. ✓ **산물(S + LiCl + Li₃PS₄ 중간체)·순서 정합**. ⚠ 2.3–2.7 vs 2.14–2.26 은 **정의가 다르다** — 그들은 탄소 20 wt% 복합체의 동전위 실측(kinetic onset, 과전압·dQ/dV 문턱 포함), 우리는 0 K 열역학; 0.1–0.5 V 차를 실차이로 읽지 말 것 |
| **B① ★★ 독립 grand-potential 구현이 우리 산화 onset 을 재현한다 — LPSCl ESW `1.78 – 2.30 V`** | (우위 아님 — **검증**) | **[Wang26IF]** `Fig. S2` — 논문은 이 값을 **숫자로 안 적는다**. 우리가 **400 dpi 픽셀 캘리브레이션**(막대 양끝 ↔ 축 0 V/6 V)으로 잰 것, 오차 ±0.03 V. 같은 그림의 다른 값: Li₃PS₄ 1.78–2.44 · **Li₇P₃S₁₁ 2.36–2.37(창이 사실상 0)** · Li₄GeS₄ 1.70–2.44 · Li₄SnS₄·Li₁₀SnP₂S₁₂ 1.80–2.39 · LGPS 1.78–2.44 · **Li₂S 0.00–2.30** | 우리 canonical **산화 onset 2.256 V**(LiS4 제외, `Li₆PS₅Cl → Li₃PS₄+LiCl+S+2Li⁺+2e⁻`) ⇒ **차 0.05 V = 실질 일치**. 서로 **독립 구현**(다른 MP hull 세대·다른 무질서 처리·다른 phase-set 필터)인데 같은 자리 ⇒ **축 B① 외부 검증 1건 추가**. 비교군 [Zhu15] 는 **1.71–2.01 V** (산화한계가 0.29 V 낮다) — 원인 후보 = hull 세대 / **E_hull→0 규약 사용 여부 미기재** / 무질서 배열. **판정 불가 → digest Q1**. 🔑 **부수 소득**: 같은 그림의 **Li₂S 상한 2.30 V 가 LPSCl 상한과 정확히 같다** ⇒ **그들 계산에서도 S²⁻ 가 pin 한다**는 **간접** 증거(⚠ 우리가 두 막대를 겹쳐 읽은 것 — **논문의 진술이 아니다**). ⚠ **환원 쪽은 어긋난다**: 그들 **1.78 V** ↔ 우리 `reduction_limit_V` **1.242** / `ocv_self_decomposition_V` **1.717** — **1.717 쪽이 [Zhu15] 1.71·[Wang26IF] 1.78 과 같은 자리**다. 두 필드의 정의 확인 필요 → **digest Q3** |
| **B③ ★ 계면 분해산물 목록이 우리 `interface_reactivity` 와 4종 완전 일치** (LPSCl 쪽 산물 빈도표) | (우위 아님 — **교차검증**) | **[Wang26IF]** `Table S2` **18행(LPSCl 블록) 전수 집계 — ⚠ 우리가 만든 표이지 논문의 진술이 아니다**: **LiCl 14/18 · Li₃PO₄ 12 · Li₂SO₄ 10 · Li₂S 7 · Ni₃S₂ 7 · Co₉S₈ 5 · MnS₂ 5 · MnO 5 · Li₄P₂O₇ 4**. **Li₂S 는 방전상태 행에만, Li₂SO₄·Li₂O 는 충전상태 행에** 나온다(= [Xiao19] SI 실물 판독과 같은 패턴). 인산염 산물의 **산화 사다리** `Li₃PO₄ → Li₄P₂O₇ → LiPO₃ → NiP₄O₁₁` 이 충전상태와 함께 오른쪽으로 이동 | 우리 `oxidation_stability.json` `nd2o3_interface_reactivity`(vs LiCoO₂) = **Li₃PO₄·Li₂S·LiCl·Li₂SO₄**+폴리설파이드 ⇒ **4종 완전 일치**, 갈림은 **Co₉S₈ ↔ 폴리설파이드** 하나뿐(= [Xiao19] 가 이미 **hull entry 세대 차이**로 판정한 그 지점, [Wang26IF] 는 **Co₉S₈ 쪽**) ⇒ **T3: 우리 entry 세트 갱신 시 Co₉S₈ 가 나오는지 확인.** ⚠⚠ **그런데 이 논문은 산물의 전자전도성을 한 번도 보지 않는다** — Ni₃S₂·Co₉S₈·**금속 Ni**(L₀.₅NCA 행)를 내놓고도 MCI 축을 언급조차 안 한다. **"부동태 vs 혼합전도" 판정의 출처는 [Zhu15] §6 이지 이 논문이 아니다** — ⛔ 인용 시 출처를 갈아 끼울 것 |
| **B(신설 언어) 열화 삼분법 — "무엇이 지배하는가"를 전압축 위에서 가른다** | (개념 이식) | **[Wang26IF]** §2.2 끝 + `Fig. 2` **청록 점 문법**(*"점 = 물질 자기분해가 계면반응보다 더 음수"*): (i) **계면반응 지배**(예: LNCA·L₀.₅NCA/LPSCl 은 2–4.5 V 전 구간) (ii) **물질 자기분해 지배**(예: Li₂S/LPSCl 전 구간; **3.75 V 에서 LPSCl 자기분해 > MnO₂ 계면반응**) (iii) **혼합**(전압에 따라 뒤바뀜) | ⭕ **이식 가능** — 우리는 축 B 를 "onset" 한 단어로 뭉쳐 쓴다. 이 3분법을 붙이면 *"우리 2.256 V 는 (ii) 자기분해 축의 개시"* 라고 정확히 말할 수 있다. ⛔ **단 그 3.75 V 산물 목록 `Li + P₂S₇ + SCl + S₈` 은 인용 금지** — "Li"가 산물로 적혀 있고 P₂S₇·SCl 은 비표준 조성식이며 `Table S2` 에 대조 항목이 없다 |
| **B② ⚠ 이 논문은 축② 를 전혀 못 준다 (기록용)** | — | **[Wang26IF]** — σ_e 측정·DOS·Bader·band gap **전부 없음**. 계면 저항·두께·성장속도도 **전수 검색 0건** | 우리 gap(comp1 2.066 / modelc 2.099 / +B₂O₃ 1.9671 / LPSOCl 2.2309 eV)과 **비교 대상 없음**. ⇒ **축 D 가 이 논문에 대해 우위인 드문 경우**. 산화물 중간층 축은 `Fig. S11`(LPSCl/interlayer 전기화학) figure-read 정성만: **Li₂O 최악**(전 전압 최암흑) · Al₂O₃/SiO₂/할라이드 안전 · **Li₃BO₃·Li₃B₁₁O₁₈ 중간군**. ⛔ **B₂O₃ 는 재료 목록에 아예 없다 — "+B₂O₃ 가 괜찮다"의 근거로 쓰지 말 것** |
| **B① ★★ LSV 산화 개시 ≈2.85–2.9 V vs Li⁺/Li (figure-read) — kinetic overshoot 진영 *4번째* 실측표, 그리고 "표면 개질로는 onset 이 안 움직인다"의 직접 증거** | (우위 아님 — **표면 개질이 axis① 을 못 건드린다**는 판정) | **[Deng26PS]** `Fig. 3a` (LSV 0.1 mV/s, **VGCF:SE = 1:1 wt**, 0–5 V, µA 절대값·면적 정규화 없음) — 우리 600 dpi 확대 재판독: **LPSC 개시 ≈2.85–2.9 V / PS-LPSC ≈2.95–3.0 V (거의 동일)**, 피크 **3.43 V(≈210 µA) → 어깨 ≈83 µA (2.5×↓)**, LPSC 2차 피크 **4.22 V** 뒤 **단조 감소**(부동태화/고갈), **≈4.6 V 에서 교차 → 그 위로는 PS-LPSC 전류가 더 크다**, PS-LPSC **4.91 V 신규 산화 피크** | 우리 grand-potential **onset 2.256 V**(LiS4 제외)/2.14 V(포함) ⇒ **overshoot +0.6~0.65 V**. [Ling26] ≈3.05 · [LiGaF] 2.5 · [Qian26] 2.5 V 에 이은 **4번째 점** — 문헌 LSV 는 항상 우리 평형값 위. **🔑 이 논문의 값은 그중 유일하게 "같은 host 에 개질만 한 전후쌍"이라, onset 이동이 아니라 *전류 억제* 임을 분리해 준다.** ⛔ **"PS 코팅이 전기화학 창을 넓혔다" 인용 금지** (초록·결론은 "below 4.6 V" 단서를 뗀 채 "greatly enhancing oxidation stability" 라고 쓴다) |
| **B② ★★ 전자 접근 차단이 산화 억제의 *본체* 라는 실측 — 우리에게 없는 축(σ_e)** | **개질 우위** (axis② = 반응 *속도·양*) | **[Deng26PS]** `Fig. 3b`·`Fig. S11` — DC 분극(Al\|SE\|Al, 0.1–0.5 V 5점 선형): **σ_e 5.69×10⁻⁹ → 7.84×10⁻¹⁰ S cm⁻¹ (7.3×↓)**. 본문: *"inhibits interfacial **electron transfer**, thereby … improving the oxidative stability"* | ⛔ **우리 축에 σ_e 가 없다.** 우리는 **band gap** 만 있다(comp1 2.066 / modelc 2.099 / **+B₂O₃ 1.9671** / LPSOCl 2.2309 eV). gap 과 σ_e 는 다른 양(gap = 캐리어 생성 문턱, σ_e = 농도×이동도). ⚠ **경고**: **+B₂O₃ 는 gap 이 host 보다 *낮다*** ⇒ 이 논문 논리대로면 **σ_e 가 오히려 오를 위험**. "+B₂O₃ 가 산화안정에 좋다"를 말하려면 축을 명명하고 **결함준위·캐리어 축을 따로 확인**해야 한다 (**우리 쪽 추론이지 이 논문의 진술 아님**) → §H |
| **B③ ★ 사이클 후 산화 *산물* 의 XPS 앵커 — 우리 첫 분해식의 원소 S 가 실제로 검출된다** | **개질 우위** (산물 생성 자체가 없음) | **[Deng26PS]** `Fig. 6a,b` (S 2p / P 2p, 사이클 전후 × 2시료 4단): bare LPSC 만 **S⁰ 166.5 · Li₂SO₄ 168.9 · P₂Sₓ 132.7 eV** 신규(PS₄³⁻ 161.2 는 잔존 = 완전분해 아님). + `Fig. 6c,d`(100 cyc 후 **S 편석 + 균열**, 대조 `Fig. S22` 는 사이클 전 둘 다 균일) + DRT `Fig. 6f,g` **R_CEI 6.1 → 22.9 Ω** vs 개질 **2.7 Ω** | ✅ **방향 일치.** 우리 comp1 첫 분해식 `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻` 의 **원소 S** 가 166.5 eV 로 실검출. **Li₂SO₄ 는 NCM 의 O 가 참여한 2차 산화**라 우리 0-압력 상평형엔 없다 = **우리 계산의 경계**. ⚠ **화학종 절대 동정은 약하다** — 같은 BE(166.5 vs 166.6 / 168.9 vs 169.1)를 시료에 따라 다르게 배정한다(순환논증). **인용은 "bare 에만 신규 성분이 난다"는 *변화* 까지** |
| **B④ ★ 수분 축 — 표면 개질의 정량 앵커 2번째 ([Qian26] 다음)** | **개질 우위** | **[Deng26PS]** `Fig. 3c,d,e`: **13 % RH** 펠릿 노출(0.5/1/2/4 h, 노출 후 **80 °C 진공 12 h** 건조 뒤 측정) → σ 유지율 **bare 15/2/1/0.5 % vs PS 89/83/77/35 %**; 셀 1 h 노출 용량유지 **78.5 % → 98.2 %**(`Fig. 3g,h`). DFT `Fig. 3f`: H₂O E_ads **−0.972 eV (LPSC (011) 슬랩) vs −0.199 eV (P-DTD 삼량체)** | ⛔ **우리 축에 가수분해/H₂O 흡착이 없다.** [Zhu20](벌크 가수분해 열역학 177종) 와 [Qian26](표면E 0.40–0.72 J m⁻²) 사이의 **빈 칸** = 우리 기여 여지. ⚠ **[Qian26] 과 직접 비교 금지 — RH 가 39 % vs 13 % 로 3배 다르다.** ⚠ **H₂S 미측정**([Taklu21] 은 1.07→0.49 cm³ g⁻¹ 실측) ⇒ 이 논문의 "가수분해 억제" 기구 증거는 **σ 유지 + DFT 2점이 전부** |
| **⚠ B④ 의 DFT 는 방법 편향이 결론 방향과 같다 — 배율 인용 금지** | (판정 아님 — **방법 감사**) | **[Deng26PS]** SI p.4 `Computational details` 전문(11줄): VASP 5.4.4 · PBE/PAW · 550 eV · **k = 1×1×1** · **vdW 보정 없음** · LPSC 는 **(011) 슬랩**(종단·층수·진공·원자수·**무질서 처리 전부 미기재**) · 폴리머는 **고립 삼량체 분자** · **흡착 구성 1개씩** | ① **주기 결정 슬랩 vs 고립 분자**를 같은 축에 놓았다 → 실제 비정질 폴리머 표면의 협동 수소결합이 빠짐 ⇒ |E_ads| **과소평가** ② **PBE 에 분산력 없음** → 유기-H₂O 쪽 **또 과소평가**. **두 편향이 같은 방향(폴리머를 더 소수성으로)** ⇒ **4.9배는 상한**. ⛔ **배율·절대값 인용 금지, 정성 방향까지만.** 📎 **[Qian26] 도 슬랩/흡착부 vdW 누락** — 같은 저널·같은 해 **두 편 연속** ⇒ **관행. 우리가 PBE-D3 + 주기 폴리머 표면 + 자리샘플링 + [Adeli] 무질서 decorate 로 다시 하면 그 자체가 기여** |
| **B① ★ LSV 산화 개시 ≈2.6–2.7 V vs Li⁺/Li (figure-read) — kinetic overshoot 진영 3번째 표** | (우위 아님 — **평형 vs 동역학 간극**의 세 번째 실측) | **[Ling26]** `Fig. S31`(LSV 0.1 mV/s, `Li₆PS₅Cl`) · `Table S4`. Table S4 는 "50 μA 도달 전위" 정의로 LPSC **3.5 V** 라 적었으나 **Fig. S31 실측 50 μA 도달은 ≈3.05 V**(3.5 V 는 *피크* 위치) → **정의와 값 불일치**. 개질계는 4.2 V | 우리 grand-potential **onset 2.256 V**(LiS4 제외)/2.14 V(포함), 첫 분해식 `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻` ⇒ **overshoot +0.35~0.45 V** — [LiGaF] CV 2.5 V·[Qian26] 2.5 V 와 같은 자리. ⚠⚠ **이 LSV 는 SE\|C 반쪽셀이 아니라 *풀셀* 이다**(SI 명시) → **NCM 탈리튬 전류 혼입**; 3.5 V 의 129 μA 피크는 양극 산화 피크일 공산이 크다. ⛔ **"modified LPSC ESW = 4.2 V" 인용 금지** |
| **★★ B① 의 *기전* — 음이온 이온화 퍼텐셜 사다리** | (우위 아님 — **왜 S 가 pin 하는가**의 근거) | **[Famprikis19]** §Electrochemical stability (ref 65 = [Richards16]): *"The high-voltage oxidation stability … is largely set by the **anion framework** and specifically its propensity to give up electrons, typically **limited by the anion with the lowest ionization potential**, following the order **N³⁻ < P³⁻ < H⁻ ≪ S²⁻ < I⁻ < O²⁻ < Br⁻ < Cl⁻ ≪ F⁻**"* | **Li₆PS₅Cl 에서 사다리 최하 음이온 = S²⁻** (Cl⁻ 은 훨씬 위) ⇒ **Cl 을 늘려도 창의 상한은 S 가 pin** — 우리 comp1·modelc **onset 동일 2.256 V** 의 기전 설명이 그대로 완성. **✅✅ axis① "S²⁻-limited" 의 1차 문헌 근거** ([Banik] 실험/HAXPES·[GG]·[Rupp] 계산에 이은 **개념 원전**). ⚠ 이 사다리는 **0-pressure bulk 열역학 축**이지 계면·기계구속·무질서 축이 아니다 — "Cl-rich 산화안정" 은 **여전히 축 명명 필수**. 또한 사다리는 O²⁻ 를 I⁻ 와 Br⁻ **사이**에 놓는다(= 산화물이 요오드화물보다는 안정, 브롬·염화물보다는 덜 안정). **사다리의 논리대로면 S²⁻ 가 조금이라도 남아 있는 한 O 치환도 onset 을 크게 못 옮긴다** — 우리 matched 2×2 결과(11종, `oxidation_matched_factorial.json`)도 **이동폭이 작다**는 점에서는 방향이 맞는다(D_plain 1.893–2.356 V, host 2.140). ⛔ 2026-08-16 정정: 여기 근거로 붙어 있던 "우리 B₂O₃ **+0.18 V**"는 **철회** — 그 +0.177 은 chain 조성 `Li₁₇B₂P₄S₁₆Cl₅O₃` 의 값이고 같은 자리 plain 조성 `Li₁₈B₂P₄S₁₇Cl₄O₃` 는 **2.034 V(−0.106)** 로 **부호가 반대**다. ⚠ 단 이건 **우리 쪽 해석**이지 리뷰의 진술이 아니다(리뷰는 O-도핑 argyrodite 를 다루지 않는다) |
| **⚠ 계산 안정창은 속도론적 안정화를 못 담는다 (구조적 한계 2가지)** | (방법 지적) | **[Famprikis19]** §Electrochemical stability + `Table 1` 직후: *"(1) the construction of **phase diagrams depends on previous knowledge of the stable crystalline phases** and (2) **stabilizing kinetic effects are not captured explicitly**"*; 분해 구동에 필요한 **과전압 ≈ ±0.5 V**(Na₃PS₄, ref 83) | 우리 grand-potential onset 2.256 V vs 실험 CV overshoot **2.5 V**([LiGaF]·[Qian26]·[WangYO] 3점) = **+0.24~0.36 V** | **✅ 격차의 정체를 리뷰가 명명해 준다** — "계산창이 좁게 나오는 것은 오차가 아니라 **속도론적 여유가 빠졌기 때문**". ⚠ 동시에 (1) 은 **우리 phase set 선택(LiS4/SCl₃/Li₅PS₄Cl₂ 제외)의 임의성**을 겨눈다 — 미지의 상은 원리적으로 못 본다 |
| **⚠ "가장 잘 통하는 전해질이 가장 쉽게 분해된다"** — 필요한 과전압의 크기가 **전해질 내 하전종 이동도** 와 연결된다는 가설(ref 86) | (경향 서술) | **[Famprikis19]** §Electrochemical stability | 우리 modelc(Cl-rich, D 2.6×↑) 는 onset 동일하나 **분해량·산물이 다름**(Zuo Eq2 거동) | ⚠ **σ↑ ↔ 안정성↓ trade-off 의 리뷰급 진술** — 우리 Cl-rich 서사에서 "빠르면서 안정" 을 주장할 때 반드시 마주치는 반론. 단 리뷰도 **가설로만** 제시(정량 없음) |
| ⚠⚠ **[Famprikis19] `Fig. 5b` 의 ΔG 부호 오식 — 인용 전 교정 필수** | (수치 아님 — **그림 오류**) | **[Famprikis19]** `Fig. 5b` (figure-read, 2026-08-06 확대 확인): **(2) Kinetic stabilization 에 `ΔG > 0` 이라고 인쇄**돼 있다. 그런데 같은 그림 캡션은 *"(2) **kinetically stabilized decomposition**"*, 본문은 *"**Given that reactivity is favoured**, the kinetics and consequently the extent of reaction are governed by the interfacial transport properties. If either is impeded, the reaction is blocked and the interface becomes kinetically stabilized"* 라고 한다 | 우리 ESW 서사는 **속도론적 여유**로 계산창(onset 2.256 V)과 실험 CV overshoot(2.5 V)의 격차를 설명한다 — 즉 **(2) 시나리오를 직접 쓴다** | **`ΔG < 0` 이어야 맞다.** ΔG>0 이면 정의상 (1) Intrinsic stability 이고, 리뷰가 든 예(LiPON 분해 → Li₃PO₄+Li₃N, garnet 20 meV/atom 불안정)도 전부 "분해가 일어나되 멈춘다" 쪽이다. **⇒ 이 패널을 슬라이드·원고에 그대로 옮기면 오류를 승계한다.** 3시나리오 도식을 인용할 때는 **캡션·본문 문구를 인용하고 그림 부호는 고쳐 그릴 것** |
| **화학적 공격 축 (유기용매) — 우리 4축에 없던 5번째 칸** | **InF₃ 공도핑 우위** (σ 보존 co **91.3/82.5/71.2 %** vs pristine **62.5/43.7/20.8 %**; toluene/DCM/EtOAc, polar index 2.4/3.4/4.3, **1:1 질량·1 h·25 °C**) | **[LiInF]** `Fig. 4a`·`Fig. S23` + DFT `Fig. 4b,c`(toluene E_ad **−0.41 → −0.12 eV**)·`Fig. S24`(자리 스캔 **P −1.85 ≪ S −1.31 < Li −1.04 < Cl −0.66 eV** = **P 가 표적**) | **우리 산화 4축(①S²⁻ onset ②Cl 분해량 ③계면 ④무질서)과 다른 축이다** — 전기화학 산화가 아니라 **친핵 공격(화학)**. 우리 grand-potential ESW 는 이 축을 아예 안 본다 ⇒ **축 이름을 반드시 붙일 것**. ⚠ **vdW 보정 없는 PBE 로 방향족(toluene) 흡착** = 절대값 신뢰 불가(digest §11-①) |
| ⚠ **CV "창 확대" 주장의 실체 = onset 이동이 아니라 진폭 감소** | (우위 판정 아님 — 방법 지적) | **[LiInF]** `Fig. 2d`(0.1 mV/s, Li/SE/SE+C 7:3): LPSC 산화 **≈2.6 V**·환원 **1.2 V**, co-doped 는 **같은 위치에서 전류만 급감** | 우리 grand-potential 창(환원 **1.242** / 산화 **2.256 V**, LiS4 포함 2.14)과 대면 **CV kinetic overshoot ≈ +0.35 V** — [LiGaF] 2.5 V·[Qian26] 2.5 V 와 같은 자리(**3번째 데이터점**). ⚠ 단 **이 논문의 CV 는 창을 넓혔다는 증거가 아니다** |
| ⚠ **B① 원문 오기 — "양이온의 *환원*이 *산화* 한계를 정한다"** | (우위 판정 아님 — **인용 시 반드시 교정**) | **[LiInF]** p.5 원문: *"the **reduction of cations** largely determines the **oxidative limit** of sulfide SEs.[20]"* 하고는 바로 다음 문장부터 **환원 안정성**(Ge⁴⁺·P⁵⁺·Sb⁵⁺ 대비 In³⁺)만 논한다. 인용된 [20]=**[Zhu20]** 도 **가수분해·환원** 논문이라 산화 한계의 근거가 못 된다 | **우리 축과 정면 충돌** — 황화물 산화 한계는 **S²⁻ 가 pin**(우리 comp1=modelc **onset 2.256 V 동일**, VBM=S 3p 96–97 %; [Famprikis19] 이온화퍼텐셜 사다리·[Banik] pDOS/COHP 로 이미 확립). **양이온 종은 *환원*(음극) 한계를 움직이지 산화 한계를 못 움직인다.** ⇒ **[LiInF] 의 "In³⁺ → 산화 개선" 사슬은 이 오기 위에 서 있다** — 우리 원고·리뷰 코멘트로 옮길 때는 **"In 은 환원 축, 산화 축은 여전히 S²⁻"** 로 고쳐 인용할 것 (digest §11-⑯, 2026-08-06 inbox #55 실물 재검증) |
| **B① CV kinetic overshoot — 독립 2번째 데이터점** | (방법 대조 — 우위 판정 아님) | **[LiGaF]** 본문 Fig 2D: Li/SE/SE+**VGCF** semi-blocking, **0.1 mV/s** → **산화 피크 ~2.5 V · 환원 피크 ~1.0 V**(vs Li/Li⁺), pristine은 <0.5 V에서 환원전류 급증(→Li₃P·Li₂S·LiCl) | 우리 grand-potential: 환원 **1.24 V** · 산화 onset **2.14 V**(LiS4 포함) / **2.256 V**(LiS4 제외, [GG] phase set) | **✓ 양 끝 모두 kinetic 지연 방향** — 산화 **+0.24~+0.36 V**, 환원 **−0.24 V**. **[Qian26] 2.5 V와 같은 자리**라 서로 독립인 두 실험이 같은 값을 준다. ⚠ 카본복합(VGCF) CV라 [Adeli] "평판 vs 카본복합" 함정·[Kang] thermodynamic vs kinetic ECW 프레임이 그대로 적용. **⛔ 논문의 "ultra-wide potential window stability" 해석은 받지 말 것** — 보인 것은 *같은 전위에서 전류가 작아진 것*(속도론적 패시베이션)이지 창 확대가 아니다 |
| **B① CV kinetic — 독립 3번째 데이터점 (Y/O 공도핑도 onset 불변)** | (방법 대조 — 치환은 onset을 못 움직임 재확인) | **[WangYO]** Li/SE/SE+C 0.1 mV/s: LPSC·YO 모두 **산화전류 개시 >2.48 V**(라벨 S²⁻→S⁰·P⁰→P⁵⁺) — 도핑 후에도 **onset 동일, 전류 크기만↓**. 환원은 <1.83 V에서 YO 전류↓ | 우리 2.256 V(S²⁻-limited)+kinetic overshoot ≈0.2 V로 정합; **[Banik] "치환으로 onset 불변(S-pin)"의 실험 재확인**·[Son25] "<2.5 V"와 한 줄. "산화 안정성 개선" 아니라 **분해 전류 감소**로 읽어야 |
| **B① intrinsic 0-pressure onset** | **무승부** (S²⁻-limited, 둘 다 2.256 V) | [GG] K_eff=0 = **1.70–2.40 V**; **[Rupp]** LPSCl DFT **2.01 V**(→Li₃PS₄+S+LiCl) / **2.2 V** vs LCO(→LiCl+Li₄P₂S₆+Li₂S); **[Banik]** stepwise CV: LPSCl·Si-Li₆PS₅I·Ge-Li₆PS₅I **onset 모두 유사**(Fig 2d, mole-정규화) + grand-potential 창 4조성 ~1.7–2.4 V(Li⁺/Li) 유사(Fig 3c) | 우리 grand-potential OCV 1.717 / **onset 2.256**(LiS4 제외, GG set; 포함 시 2.14) → **✓✓ 재현**, GG 2.40과 격차 0.14 V, [Rupp] 2.0–2.2 V band와 정합. **🔑 [Banik] = 우리 "치환 무관 onset 동일"의 *외부·동방법(grand-potential)·동그룹(Mo) 정답지*** (단 Banik 치환축 = P→Si/Ge·Cl→I *교환*; 우리 modelc = Cl *증량* → 같은 결론·다른 레버) |
| **B① 메커니즘: 왜 안 변하나 = S가 VBM을 pin** | **무승부** (S²⁻가 산화 한계 고정) | **[Banik]** pDOS+COHP(Fig 4): **VBM = 자유 S²⁻ + PS₄³⁻ 비결합 S 3p**; Cl 3p는 VB 깊이, I 5p는 엣지지만 I⁻/I₂ redox는 ESW 무관(Table S3); CB=P–S 반결합 → 치환은 **gap 크기(CB 위치)만** 바꿈. "**Sulfur = Achilles' heel**" | 우리 `VBM_vs_grandpotential_report` §8: comp1/modelc **VBM +0.32 eV 다른데 onset 동일 2.14 V** (둘 다 VBM=S 3p 96–97%, ICOHP P–S −5.94/−6.0, ELF P–S 0.946/0.944) → **✓✓✓ 동일 메커니즘** ("S가 VBM·산화 onset pin"). Banik COHP(P–S 결합 깊이, 비결합 S=VBM)가 우리 ICOHP/ELF 해석을 외부 확증 |
| **B① 밴드엣지(VBM/HAXPES) ≠ 분해 onset** | (방법 구분) | **[Banik]** band-edge(HAXPES)=상한/주도원소, phase-stability(grand-potential)=실제 분해 전압을 **명시 분리**(intro·Fig 1b) + **이론창<실험창**(kinetics·중간상; Fig 1c) | 우리 report 핵심과 동일: **VBM=과대상한, grand-potential=실제 onset, 실험창=kinetic으로 더 넓음**. **✓✓✓ 동일 프레임** — Banik이 HAXPES(VBM 불변)+CV(onset 불변)로 우리 "VBM 달라도 onset 동일"의 *상보·실험* 증거. (단 Banik HAXPES는 절대 VBM을 공통척도서 직접 측정 = 우리 DFT 절대 VBM 비엄밀의 보완) |
| **B① 밴드엣지는 *band-alignment 관측량*이고 *작동 중 움직인다* (operando)** | (방법·차원 확장; 우리 밖) | **[Hikima]** 박막 ASSB를 *반도체 소자*로 보고 **operando HAXPES+UPS+LEIPS**로 *전체 밴드구조*(진공준위 절대)를 작동 중 측정 → 충전 시 **Li₂₋ₓMnO₃ E_F ~1.1 eV drop→n→p 전이→Al계면 Schottky/inversion→고전압 충전차단**; 밴드를 **band alignment·전위창·band bending**에 씀(분해 onset 아님) | 우리 oxidation 보고서 §6 **용도구분 그대로**: 밴드엣지=band alignment용(상한)·산화 onset=grand-potential/CV. **✓✓ 동일 프레임의 *operando 실험판*** — [Whitten](기법)→[Banik](정적 VBM 불변)→**[Hikima](operando VBM 운동)** 3단 계보. 우리 정적 VBM(comp1 2.128/modelc 2.445, 비엄밀)을 *작동 중 운동*으로 확장(우리 H목록). ⚠⚠ **재료가 oxide(Li₂MnO₃/LASGTP)라 argyrodite 산화 onset/VBM 절대값과 *수치* 등치 금지** — 연결은 프레임·방법·operando이지 수치 아님. 이 논문은 *band alignment/운동*이지 *분해 onset*이 아니므로 "operando 산화 onset"으로 읽기 금지 |
| **B① 방법: indirect (de)lithiation** | (우리 못 봄) | **[Rupp]** §2.5.2: LPSCl→**Li₄PS₄Cl/Li₁₁PS₅Cl 중간상** 거쳐 분해 → 실험창 ~1.25–2.5 V로 넓어 보임 (Schwietert/Wagemaker) | 우리 onset이 실험보다 낮은 이유 = indirect/passivation/kinetics의 **방법 근거** |
| **B① 실험 1st-cycle 산화 개시 — 독립 4번째 데이터점 (Ta 도핑도 onset 을 못 움직인다)** | (방법 대조 — 우위 판정 아님) | **[Wu26]** `Fig. 4a` (Li\|SE\|SE+KB, 0.1 mV/s): **1st cycle 산화가 OCV 2.45 V 부터 시작**, 피크 ≈3.4–3.5 V(+16 µA, figure-read). 환원 개시 **0.76 V** | 우리 grand-potential: 산화 **2.256 V**(LiS4 제외) / 환원 1.242 V / OCV 1.717 V | **✓ 좋은 일치** — 1st-cycle 실측 개시 2.45 V ↔ 우리 2.256 V, kinetic overshoot **+0.19 V** ([LiInF] 2.6·[LiGaF] 2.5·[WangYO] >2.48 V 와 같은 자리). **Ta 6 % 를 넣어도 onset 위치는 안 움직인다** = S²⁻-limited 재확인 |
| ⚠ **"실용 ESW 0.1–4.3 V" 는 3rd-cycle 부동태 창이다 — 우리 열역학 창과 같은 표에 넣지 말 것** | (인용 규율) | **[Wu26]** `Fig. 4a`: 1st→2nd→3rd 로 분해전류가 급감한 뒤 **3rd cycle 접선 외삽**으로 0.1/4.3 V 를 읽는다. 논문 스스로 *"practical"*·*"self-passivating"* 이라 명시(`Fig. 4b,c`) | 우리 창 = **0 압력 grand-potential**(2.256 / 1.242 V) | **⛔ 축 혼용 금지.** 단 논문의 프레임(*열역학 불안정 → 산물이 좋으면 실용창 확장*)은 **우리 B③ = [Zuo22] 논리와 동일** |
| **B③ cathode 계면 — *레버 = 도펀트가 만드는 CEI 산물*(Ta → LiTaO₃)** | **Ta-도핑 승** (CEI) | **[Wu26]** `Fig. 4f` XPS Ta 4f: pristine TaS₄³⁻ 26.5 → **CEI LiTaO₃ 27.4/25.5 eV** + ToF-SIMS TaO₃⁻ 가 표면 60 s 내 급감(`Fig. 4g`) | ★ **우리가 예측한다**: `cascade_interface_90.jsonl` grand-potential 2.5 V — `Ta₂O₅` 계 → **0.1921 LiTaO₃**, O-free `TaCl₅` 계(`Li24TaP3S15Cl9`) → **0.1176 LiTaO₃ + 1.059 LiCl + 0.3529 Li₃PO₄** (vs LiCoO₂) | **✓✓ 외부 검증 3번째**([Zuo22]·[Sundar25] 다음). ★ **논문이 안 밝힌 산소 출처를 우리 반응식이 지목한다 — LiCoO₂/NCM 격자산소.** 즉 "좋은 CEI" 의 대가는 **양극 산소 방출** |
| **B② 기계 구속 window** | **Cl-rich 승** | [GG] K_eff=20 LPSCl1.5 **0.80–4.30 V** (Cl 산물 고몰부피→strain) | 우리 `constrained_esw.py`가 trend 재현(modelc 더 넓어짐) → **✓** |
| **B① ★★ "Cl 은 산화 onset 을 옮기지 않는다" 의 실험 확증 — 같은 두 조성으로** | (우위 아님 — **우리 S²⁻-pin 검증**) | **[Zuo]** `Fig. S2` CV 겹침(SE/C, C65 20 wt%, 0.05 mV/s): **"all maxima appear at the same potentials"** — Li₆PS₅Cl 피크 figure-read ≈**2.85 V**, Li₅.₅PS₄.₅Cl₁.₅ ≈**2.75 V vs In/InLi**, 곡선 모양 동일 ⇒ 논문 결론 *"the oxidation mechanism is similar"*. 분해 반응식도 **Eq1 `Li₆PS₅Cl→LiCl+Li₃PS₄+S+2Li⁺+2e⁻`** / **Eq2 `Li₅.₅PS₄.₅Cl₁.₅→1.5LiCl+Li₃PS₄+0.5S+Li⁺+e⁻`** | **✓✓✓ 우리 `constrained_esw_cl_scan.json`(k_eff=0): Cl 0.5/1.0/1.5/1.6 전부 산화 onset 2.256 V — Cl 함량에 완전 무감(S²⁻-limited)**, 그리고 **comp1 onset 반응이 Zuo Eq1 과 문자 그대로 일치**(`Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2 Li`), modelc 는 `→Li₃PS₄+1.6LiCl+0.4S+0.8Li` = Eq2 거동. **이 논문은 DFT 를 하지 않으므로 우리 grand-potential 이 그 이론부를 독립 재현한 것**. **⛔ 측정창 정렬 주의(2026-09-11)**: Zuo CV 범위는 **2.0–3.7 V vs In/InLi = 2.6–4.3 V vs Li⁺/Li**(논문 환산 **+0.6 V**)인데 우리 onset 2.256 V vs Li⁺/Li = **1.656 V vs In/InLi** ⇒ **우리 onset 은 그들 창 하한보다 0.34 V 아래라 CV 로는 원리적으로 못 본다**. 두 시료가 창 시작점에서 이미 전류를 흘리는 것이 그 정합 증거이고, **"실험 onset 2.0 V vs 우리 2.256 V" 식 병기는 기준전극 혼용 오류**. 본문의 "lower oxidation onset for Cl1.5" 는 **전류 크기 차이**지 열역학 onset 이 아니다 |
| **B① 분해 "양" 은 우리 축이 아니다 — 그리고 σ 로 설명 가능한 범위 안이다** | (우위 판정 금지 — 방법 경고) | **[Zuo]** SE/C 복합 CV `Fig. 1a,b`·`Fig. S2` **figure-read 피크 32 vs 47 nA cm⁻² ≈1.5×**(⚠ 본문은 *"approximately twofold"* 라 쓰지만 2× 가 되는 곳은 **2.0–2.2 V 개시구간뿐**, 3.65 V 에선 ≈1.1× 로 수렴) · GITT **3 V vs In/InLi 이하** 분해용량 figure-read **112 vs 163 µAh(1.45×)**·**이상은 193 vs 195 µAh(동일)**(`Fig. S4a`) · ToF-SIMS S⁻ **6.7 vs 10.4배**·Cl⁻ **5.1 vs 6.7배**(`Fig. 1c,d`) · DSC **535/532 → 523/493 °C**·TGA **315 °C** 부터 손실(`Fig. S3`) | 우리 0 K grand-potential 은 **onset 과 산물만** 준다 — 분해 *양·속도* 는 계산 축이 없다(interface ΔE 차 0.008 eV/atom = noise). **🔑 전류비 1.5× < σ 비 2.4×** ⇒ **단위 전도도당 반응성은 오히려 Cl-rich 가 낮다** ⇒ **⛔ 어느 방향으로도 "Cl-rich 가 intrinsic 하게 더 반응성" 주장 금지**(기존 digest 의 "2× ≈ σ 2.4×" 서술을 2026-09-11 그림 실독으로 1.5× 로 정정). **DSC/TGA metastability 는 우리 공백** — 조성간 E_above_hull(SQS) 축 미구축. ⚠ 평판 CV([Adeli])는 **정반대 겉보기**(Cl-rich 전류 더 작음)를 주므로 **측정계 명시 없이 인용 금지**(§B "겉보기 CV 의 측정계 함정" 행 참조). ⚠ Zuo Cl **1.5** ≠ modelc Cl **1.6**([Adeli] 고용한계 밖; `Fig. S1` 에 이미 LiCl 2차상) |
| **B③ cathode 계면 — *레버 = Cl 함량* (정전압 홀드 조건 한정)** | **Cl-rich 승 (⚠ 조건부·교락 있음)** | **[Zuo]** ⭐⭐ **우리 comp1(Li₆PS₅Cl) vs modelc 계열(Li₅.₅PS₄.₅Cl₁.₅)을 그 두 조성 그대로 비교한 유일한 실험 대조군** (*Angew.* 2023, 62, e202213228; **원자계산 0**). **3.7 V vs In/InLi(=4.3 vs Li⁺/Li) 30 h 홀드**: R_cat=√(R_ct(R_el+R_ion)) √t 기울기 **13.2 → 8.9 Ω h⁻⁰·⁵**(`Fig. 2d`) · 0.5 C 50cyc **133 → 145 mAh/g**·CE **77 → 79 %**(`Fig. 3`). 산물: 60 h 홀드 후 **PO₃⁻ 8.1 vs 4.0 ×10⁵**(`Fig. 4c`, pristine 2.2≈2.3 로 기준선 깨끗) · 100 사이클 ROI **POₓ −40 %·Sₓ +43 %·SOₓ ±0 %**(`Fig. S11`) · **DEMS O₂ 6.7≈6.8 µmol/g_NCM(동일)인데 SO₂ figure-read ≈5.7×**(`Fig. 6`) = **gas diversion** | 우리 grand-potential이 [Zuo] Eq1/Eq2 분해 stoichiometry 재현 → **✓ 화학**. **+ Zuo ToF-SIMS 종(PO₃⁻/SO₃⁻/Sₓ⁻/Cl⁻) = 우리 interface_reactivity 산물(Li₃PO₄/Li₂SO₄/폴리설파이드/LiCl, vs LiCoO₂) = `xps_reference_sei.csv` anchor(133.3/168.0/160.2/198.6) 1:1** (`papers/zuo2022…md` §11b, 2026-06-26). 단 "phosphate *양*↓·폴리설파이드↑"는 SIMS-fold라 우리 정적 hull(comp1 −0.3227 ≈ modelc −0.3308 eV/atom, **Δ0.008 = noise**)로 비율 못 가름. **⛔⛔ 2026-09-11 그림 실독으로 추가된 결박 3개**: ① **R_cat 은 정의상 R_ion 을 품는다** — Cl-rich σ 가 2.4× 높아 기울기 비 1.48 은 **수송만으로도 설명 가능**(논문 스스로 "Gerischer 라 R_ct 와 수송 분리 못 함" 자인) ⇒ **8.9/13.2 을 "계면 화학 우열" 로 단독 인용 금지**; ② **조건 의존이 결론을 뒤집는다** — 카본계 GITT(`Fig. S4b`)는 **>3 V 에서 Cl-rich 저항이 더 빨리 증가**, 갈바노 사이클링(`Fig. 3d,e`)은 figure-read 로 **Cl-rich 반원 성장이 더 큼**(Δ≈90 vs ≈71 Ω), C/20·45 °C DEMS 셀은 **CE 73.6 vs 82.7 %(우리 산수)로 Cl-rich 9 %p 열세**. 논문 자신이 "`Fig. 2` 는 홀드=화학열화 조건, 사이클링은 전기화학분해 조건" 이라 경계를 긋는다; ③ **"phosphate 가 저항원" 의 물리는 논증되지 않았다**(Li₃PO₄ 는 코팅 전도체·S/폴리설파이드는 절연) — 우리 **LPSOCl(+O)** 서사가 "phosphate 형 계면이 유리" 로 갈 때 마주칠 반론이자, 이 논문 자체의 약점. **+ [Liu] 독립 확증**(NCM811 full): cycled NCM/LPSCl이 oxidized S(sulfate/sulfite)·oxidized P 더 많고 argyrodite 적음 → R_cat 142.8 < 276 Ω·CE↑(Fig 5d–f). 같은 방향이나 Liu는 "less oxidized solid"만, Zuo의 gas/polysulfide diversion 메커니즘은 없음 |
| **B③ cathode 계면 — *레버 = SE 코팅*** (Cl 함량 아님) | **SE-coated 승** | **[Kang25]** ⭐ R_int 4.3 Ω cm²·200cyc 유지율 **+15.0 %**·OCV 강하 +10.1 mV; 식1 `2Li₆PS₅Cl→P₂S₅+5S+2LiCl+10e⁻+10Li⁺` → NCM811 균질 chemical lithiation(SOC↓) | 우리 grand-potential이 식1 산화분해(P₂S₅계+S+LiCl)를 **voltage-resolved로 재현·검증** (2.14 V S²⁻→폴리설파이드 … 3.06 V 원소 S). **단 이로움 = SOC-강하(코팅 균일화)이지 passivation 아님** → Nd(절연 CEI)와 *다른 physics* (§B 주석·§D) |
| **B③ cathode 계면 — *레버 = SE 입자 **유기** 코팅(전자 절연)*** (Cl 함량 아님; 코팅 대상 = **SE 입자**) | **DA-coated LPSCl 승** | **[Qian26]** ⭐ 데칸산(C10 지방산) **2 wt% / 25 nm conformal** 용액코팅(고온소결 0) + **무코팅 NCM85** · Li–In · 2.8–4.3 V: 초기 **CE 60→83 %**·첫충전 **<3.5 V sloping(=LPSCl 산화) 소실**·1C **55→104 mAh/g**·**150cyc 61→96 %**·**R_cathode(EIS+TLM, 150cyc) 461→104 Ω(4.4×)**·4.6 V 110cyc 91 %·21 mg/cm² 3.2 mAh/cm²; ToF-SIMS **SO₂⁻/SO₃⁻/PO₂⁻/PO₃⁻ 대폭↓**·XPS 원소S(163.1 eV)↓·FIB intragranular crack↓ | **🔑🔑 기전이 우리 축분리와 정확히 일치 — 저자 자인**: CV bare **anodic onset 2.5 V**를 DA가 억제하는 이유를 "**electronically insulating** DA layer → **limits electron transfer**"로 명시, 즉 **열역학 창 확대가 아니라 전자 전달 차단**. → 우리 **B① 무승부(S²⁻-pin, comp1=modelc 2.256 V)** + **B③은 전자 절연 CEI가 레버**([Nd]/[B₂O₃] 서사)의 **외부·실험·독립 증거**. 우리 grand-potential onset **2.256 V < 실험 apparent 2.5 V**(kinetic 격차 0.24 V, [GG] 2.40·[Rupp] 2.0–2.2 밴드와 한 줄). 분해 산물도 **phosphate/sulfate/원소S = 우리 interface_reactivity 산물**과 1:1([Zuo] Fig4·5·[Liu]와 **3편 독립 확증**). ⚠ σ는 **판다**(Table S3: 1 wt% 1.4 → 2 wt% 1.3 → 5 wt% 0.7 → 10 wt% 0.2 mS/cm; **bare 절대값 미제시**) — "무손실 코팅" 아님. ⚠ 유기물은 우리 MP hull 밖 → **코팅 자체의 열역학 판정 불가**, 우리는 "전자 절연" 기전 정합까지만 |
| **B③ cathode 계면 — *레버 = 양극 입자 **무기염** 코팅(용액·무소결)*** (Cl 함량 아님; 코팅 대상 = **CAM 입자**) | **LiPOF-coated NCM85 승** | **[Qian25]** ⭐ **LiPO₂F₂ 1 wt%** DMC 용액코팅 → **~35 nm 비정질 conformal**(HRTEM), **100 °C 증발만·소결 0** + 상용 LPSCl(σ 2.2 mS/cm) · Li–In · 2.8–4.3 V · 0.2 C: **ICE 64.6→81.6 %**(첫충전 잉여 ≈48 mAh/g 소멸 = LPSCl 산화 몫, figure-read) · dQ/dV **3.0–3.2 V "Argyrodite decomposition" 혹 소멸** · 0.1/1 C **152/51→180/85 mAh/g** · **200 cyc 56.0→81.4 %** · 고로딩 25.6 mg/cm² **4.4 mAh/cm² 200 cyc 77 %** · **R_cathode(EIS+TLM) 200→90 Ω·cm²** · **S 2p 산화-S(163.2 eV) 소멸**(bare 는 thiosulfate·polythionate 까지) · ToF-SIMS **SOₓ⁻ 급감** · FIB 균열 완화. **2 wt% 는 손해**(80 cyc 92 % 지만 초기 167 vs 182 mAh/g, ICE ≈78.6 % figure-read) → **두께 최적점 존재** | **🔑 우리 축분리와 정합 — 코팅은 onset 을 안 옮긴다.** 저자들은 LPSCl 의 ~2.5 V 산화한계를 **전제로 깔고** "그 위에서 어떻게 버티나"만 묻는다 → **B① 무승부(우리 2.256 V S²⁻-pin) · 이득은 전부 B③**. `[Qian26]`(SE 입자 유기코팅)·`[Deng26PS]`(표면개질)·`[Kang25]`(SE 코팅)·`[Cha]`(할라이드 코팅)·`[BZOx]`(양극 산화물 코팅)에 이어 **레버 6번째인데 여섯 편 모두 B① 을 못 움직인다** — 이 자체가 우리 서사의 문장. ⚠ **복합양극에 카본 없음**(SE:CAM 2:8) → `[Zuo]`(CV 에 C65 20 wt%)와 **분해 "양" 직접비교 금지**. ⚠ 초록 82 % vs 도면 81.4 % 불일치 — **81.4 %** 로 인용 |
| **B③ ★★ 계면 산물 열역학이 우리 `interface_reactivity.py` 를 *문자 그대로* 재현 — LPSCl 자기분해식** | (우위 아님 — **독립 재현**) | **[Qian25]** `Fig. 1b` x=1.0 회색 점선("Decomposition"): **Li₆PS₅Cl → Li₃PS₄ + Li₂S + LiCl**, 구동력 **figure-read ≈ −83 meV/atom**. 방법 = pymatgen `InterfacialReactivity`, MP hull, meV/atom, 끝점 hull-평형 규약 | 우리 `db/properties/interface_reactivity_results.json` 의 x=1.0 kink 가 **`Li6PS5Cl -> Li3PS4 + Li2S + LiCl`** — **산물 3종 문자열까지 일치**. ⛔ **−83 meV/atom 은 이식 금지**: 우리는 `energy_mode: hull`(조성의 hull 에너지 = e_above_hull ≡ 0)을 쓰고, 그들은 **어느 S/Cl 배열인지 안 밝힌 LPSCl 구조 1개**의 에너지를 썼다(참고: MP 실엔트리 `mp-985592-GGA` 는 e_above_hull **1.5663 eV/atom** = 무질서 미보정 인공물). **정의도 구조도 다르다** |
| **B③ ★ 계면반응 크기의 자릿수 기준선 (코팅\|양극도 크게 반응한다)** | (기준선 — 우위 판정 아님) | **[Qian25]** `Fig. 1e,f` **figure-read ≈**: NCM\|LiPOF **2.8 V −395 meV/atom**(CoO+NiO+Li₃PO₄+LiF) / **4.3 V −108**(Li₂NiF₄+CoO₂+MnO₂+Ni₃(PO₄)₂). LPSCl\|LiPOF 는 **2.8 V −43 / 4.3 V −96** | 우리 `interface_reactivity_results.json`: LiCoO₂\|comp1 **−323** / LiCoO₂\|modelc **−331 meV/atom** → **같은 자릿수(수백 meV/atom)**. ⛔ **값 대소 비교 금지** — 양극도 계도 functional/U/MP 버전도 다르고, 그들은 **끝점 규약이 Fig 1b(닫힌)와 1c–f(grand) 사이에서 다르다**. "코팅이든 SE 든 산화물 양극과는 수백 meV/atom 급으로 반응한다" 까지만 |
| **⚠ B③ 게이트 문턱 \|ΔE_rxn\|<100 meV/atom 의 *귀속*이 한 편 어긋난다 (인용 규율)** | (판정 아님 — **서지 교정**) | **[Qian25]** 본문: *"reaction energies … less than 100 meV/atom, which has been used as an indicator for low chemical reactivity"* + **ref [7] = [Rich16]** | 우리 실물 검증 digest 기준 — **[Rich16] 의 100 meV/atom 은 "무시한 계면에너지의 상한"**(Δγ 0.5 J/m²·원자층 두께)이고, **반응성 게이트로서의 \|ΔE_rxt\|<100 meV/atom 은 [Xiao19] filter 4**(= [Qian25] 자신의 ref [33]). 숫자·계보는 맞지만 **인용처가 한 편 밀렸다**. 🔑 그리고 두 뜻이 **수치적으로 겹친다**는 사실이 규율을 준다 — **게이트 바로 위/아래 물질의 순위는 우리가 무시한 항의 크기 안에 있다**(우리 [Rich16] digest §16 과 동일 결론). (부수: [Qian25] ref [7] 페이지 **255–273** 은 오기, 실물 **266–273**) |
| **⚠ B③ "분해산물이 전자절연" 주장을 논문 자기 표가 절반만 지지** | (판정 아님 — **인용 범위 제한**) | **[Qian25]** `Table S1`(SI, 텍스트): LiF **8.7** · LiCl **6.3** · Li₃PO₄ **5.8** · Li₄P₂O₇ 5.6 · Li₂NiF₄ 4.7 · P₂O₃F₄ 5.8 · SOCl₂ 3.6 · Ni₃(PO₄)₂ 3.4 · **P₂S₅ 2.6** · **LiPO₃ 2.5** · **P₂S₇ 2.1** · CoO/CoO₂ **0.6** · MnO₂ **0.5** eV | 우리 `sei_products.json` 문턱(**절연 ≥4 / marginal 2–4 / 전도 <2 eV**)으로 재면 **2.8 V 대표 산물 세트에 든 P₂S₇(2.1)·LiPO₃(2.5)는 marginal**, NCM 쪽 CoO/CoO₂/MnO₂ 는 **전도체**. → 인용은 **"LiF·LiCl·Li₃PO₄ 가 절연"** 으로 좁힐 것. ⛔ **gap 절대값 혼용 금지**: 같은 "MP GGA gap" 인데 **LiCl 그들 6.3 vs 우리 6.65 eV**(Δ0.35) = MP DB 버전/엔트리 차이. ⛔ Table S1 **전압창도 우리 ESW 표에 붙이지 말 것** — 출처가 refs [7,32,33] 소환값과 자체 DFT 추정의 **혼합인데 매핑이 없다** |
| **⚠ B③ 계산 NCM ≠ 실험 NCM (조성 불일치, 논문이 언급조차 안 함)** | (판정 아님 — **인용 시 교정**) | **[Qian25]** `Fig. 1e,f` x축 **figure-read**: DFT 입력은 **LiMn₀.₀₈₃Co₀.₀₈₃Ni₀.₈₃O₂**(=12-포뮬라 정수치환 정황) 인데 실험 CAM 은 **LiNi₀.₈₅Mn₀.₁Co₀.₀₅O₂**(BASF NCM85). **Co 0.083 vs 0.05 = 1.7배** | Fig 1e 대표 산물에 **CoO** 가 들어 있으므로 **"NCM85 와 반응해 CoO 가 생긴다"로 인용하면 과대**. 우리가 NCM 계 계면반응을 돌릴 때도 **입력 조성을 반드시 명기**해야 한다는 사례 (우리 `estimand_card` §1 "무엇을 재는가" 위반 유형) |
| **B③ cathode 계면 — *레버 = 할라이드 코팅의 dual compatibility*** (Cl 함량 아님) | **dual-compat 할라이드(LZC) 승** | **[Cha]** ⭐ 할라이드(LIC/LYC/LZC) 8–10 nm 코팅; **LZC=Li₂ZrCl₆만 NCM·LPSCl 양쪽 호환**(7일 무분해) → 계면저항 74.4→**20.1 Ω·cm²**·100cyc **91.2 %**; LIC(In₂S₃)·LYC(Y₂S₃) 비호환·**LIC는 bare보다 나쁨(80.8<83.1)** | 우리 grand-potential이 bare NCM-LPSCl 분해(phosphate·P₂Sₓ·Li₂S, Cha XPS Fig5e)를 **재현**(우리 산화 staircase P₂S₇·S·폴리설파이드·LiCl). **단 LZC dual compatibility(Zr⁴⁺ passivation)는 Zr가 우리 hull에 없어 *아직* 정량 못 함** → 향후 Zr hull + interface_reactivity. **이로움 = *새 저항층 안 만듦*(비반응성 코팅)이지 능동적 절연 CEI 형성(Nd) 아님** → §B 주석·§D, "Cha=Nd 실험증거"는 부정확 |
| **B① 황화물 SE 산화 한계 = 5 V 직접접촉 불가** (intrinsic) | **황화물 패배 (실험 명문화)** | **[Son]** ⭐외부 본문 "sulfide SEs … limited electrochemical stability (**<2.5 V** vs Li/Li⁺)"(intro) + Fig 3b 막대 + Fig 3a CV | 우리 grand-potential **2.256 V**(S²⁻-limited, LiS4 제외; 포함 2.14) → **✓✓✓ 정량 일치** — Nature Energy 본문 "<2.5 V"가 우리 thermo onset과 부합. **우리 계산이 5 V 논문의 출발 전제를 수치로 뒷받침** |
| **B③ cathode 계면 — *레버 = 산화안정 차폐 SE 교체*** (Cl 함량도 코팅도 아님; *물질군 교체*) | **불소계 차폐(LiCl–4LTF) 승** | **[Son]** ⭐외부 황화물(<2.5)·할라이드(LYC 3.7·Zr-OCl 4.1)·기존산화물코팅(LiNbO₃ 3.86, 산소방출→Mn₃O₄) 전부 5 V 불가 → **불소계 LiCl–4Li₂TiF₆**(σ 1.7e-5·**>6.7 V**) 차폐 → LNMO 2C 500cyc **75.2 %**·R_int 0.1 kΩ·cm² | 우리 hull 밖(Ti/F·Y/Zr) → 수치 재현 불가, **방법(grand-potential ESW)만 동일**. **[Cha] 할라이드코팅 전압천장(~4 V NCM)** 을 Son이 명시(할라이드도 5 V 불가) → 우리 그룹 코팅 서사는 4 V급·5 V는 물질군 교체. **고전압 산소방출→절연상(Mn₃O₄)** = [Zuo]/[Kang25] O-release와 결 동일 |
| **B③ cathode 계면 — *레버 = charge-conductive 산화물 CAM 코팅*** (Cl 함량 아님; 코팅 대상 = **양극 입자**) | **산소결핍 BZOx 승** (동일 화학 stoich WZO는 패) | **[BZOx]** Small 2026: 단결정 NMC811에 dry-mechanofusion ZrO₂₋ₓ **~8 nm** shell → **첫 사이클 비가역 67.45→45.84 mAh/g·ΔV 0.3→0.18 V(WZO 0.73)·CE 77.5 %·100cyc 126.69 mAh/g(NMC 109.2)·R_CA-SE 55.2 vs WZO 192.9 Ω**·σ_e 보존(÷3.8 vs WZO ÷25.5)·50cyc XPS **POₓ(134.6·135.3 eV)는 bare에만**(코팅 2종 SE 분해 완화); DFT(VASP PBE+U·LiNiO₂(104)\|LPSCl(100)): 계면 S 상태 **E_F 직하(bare)→−1..−2 eV 하강(Zr-산화물 접촉)** + S–O 1.97→1.65 Å(SO₂ 경로) vs BZOx=Zr–S(SO₂ 억제) | **✓ 계면 S 안정화 관측량 = 우리 free-S site-PDOS(⟨3p⟩ −1.1→B–S −2.15 eV) 지표의 계면판**(우리=정량·창 고정, 그들=음영 정성; 이제 방법 공개(PBE+U·520 eV)라 우리 slab 파이프라인으로 직접 재현·정량화 가능 = 기여 기회) + **50cyc XPS S 2p 자리분해(S²⁻ 159.9/PS₄³⁻ 161.5·162.7/산화종 163.7·164.5 eV) = 우리 "free-S 먼저 산화" 서사의 실험 관측량 포맷**. **🔑 [Sundar] ZrO₂-실패와 모순 아님 — 코팅 대상이 판정을 뒤집는다**: SE 입자 코팅은 σ_e↓가 선([Sundar]: ZrO₂→Zr₃O 금속성·σ_e×2=실패) vs CAM 코팅은 σ_e 보존이 선([BZOx]: 같은 '환원 Zr 산화물=전도성' 물리가 여기선 설계 특징; 저자들도 E_g<0.5 eV 코팅=SE 분해 촉진이라는 창 논리(0.5–2.25 eV)로 인지). 이 논문 내 stoich WZO 실패(÷25.5)도 Sundar의 stoich-ZrO₂ 부정과 나란(단 기전 다름: σ_ion/Zr₃O vs 전자 절연 장벽). **⚠ BZOx\|LPSCl 분해 열역학(Zr₃O/Li₆Zr₂O₇ 형성 여부) 여전히 미계산(정적 pDOS+결합길이뿐; 이완 중 Zr–S 결합 형성 자체가 계면 화학 활성의 증거)** — 우리 interface_reactivity(Zr hull 추가 시)로 in-silico 판정 가능한 열린 질문; **DFT BZOx 모델=ZrO₁.₃₃(실험 ZrO₁.₈의 3배 공공)** 주의. ⚠ 유지율 %만은 WZO 최고(85.8>80.4, 저용량 통계)·rate는 본문(1C ~140) vs SI 판독(~103, pristine 최고) 불일치 → "WZO 대비 우위"까지만. ⚠ 양극 펠릿 σ_e(10⁻⁴–10⁻⁶)는 SE bulk σ_e anchor(10⁻⁸–10⁻⁹, §D)와 물리량 다름 — 혼용 금지. B③ 레버 3종([Cha] 할라이드 dual-compat / [Kang25] SE 코팅 균일화 / [BZOx] charge-conductive 산화물)에 "무엇을 코팅하나" 변수 추가 |
| **B① 겉보기 CV 전류의 측정계 함정 (평판 vs 카본복합)** | (방법 경고 — 우위 판정 금지) | **[Adeli]** 평판 Li\|SE\|SS CV(1 mV/s, RT): **Cl-rich(x=0.5) 양극전류가 더 작고 2차 스캔서 소멸**("낮은 황화물 함량·격자 S→절연 S 자기제한" 해석; Fig S10) ↔ **[Zuo]** 카본복합(SE+20 wt% C65, 0.05 mV/s) CV: **Cl-rich 전류 2×**. 같은 물질쌍(Li₆PS₅Cl vs Li₅.₅PS₄.₅Cl₁.₅)·정반대 겉보기. Adeli 스스로 "CV studies can be misleading" 자인 | 우리 grand-potential onset **comp1=modelc 2.256 V 동일(S²⁻-limited)** = 어느 쪽 CV와도 모순 아님(onset=thermo, 전류량=kinetic·접촉면적·스캔속 변수). **평판 CV는 분해 과소평가**([Taklu] 행의 Dewald 계열 경고와 동일) → **"Cl-rich가 anodic 안정"([Adeli])도 "Cl-rich가 더 분해"([Zuo])도 측정계 명시 없이 인용 금지** — 분해 "양" 축의 본대는 [Zuo](증폭계+ToF-SIMS/DEMS) |
| **B④ thermal(고유) — 측정법 + 조성 서술자 Th′** | **argyrodite(comp1) 압승** (Li–P–S 내) | **[Wang22]** 황석출+밀봉관: **Li₆PS₅Cl(=comp1) 800 °C XRD 무변화·DSC 무피크·황석출 0** ≫ Li₃PS₄(~400 °C 분해, 2Li₃PS₄→2Li₂PS₃+Li₂S+S) > Li₇P₃S₁₁(~300 °C, →Li₃PS₄+2Li₂PS₃+S); **Th′**={[Li]%×312.5+[P]%×346}×4 서술자가 서열·P₂S₃/도핑 개선 트렌드 재현; **O 도핑 = 열안정 +100 °C·σ 10×↓**(Li₃PS₄ 기준) | 우리 열안정 계산 축 **없음**([Fan26] §7 ✗공백과 동일) — 단 **Eq 5를 우리 조성에 적용(우리 산수): comp1 ≈683 > modelc ≈656 kJ/mol = Cl-rich 열 열세 예측** → [Zuo] DSC/TGA(Cl1.5 융점↓·TGA 315 °C)·[Wu] calendar 90 °C와 **방향 일치** (⚠ Eq 5는 Li–Cl 항 부재 = Cl을 S% 희석재로만 취급 → 방향만, 정량 금지). **O trade-off는 우리 기전과 상보**: 그들 "POS₃가 Li⁺ 속박·Ea↑" = 우리 ICOHP P–O −8.43(P–S 대비 +41 %)·O@PS₄ −0.67 eV/O의 실험판([Yang25] La+O σ 0.65×와 한 줄). **향후: Th′-ICOHP**(Handbook BDE→우리 ICOHP 가중 교체, Li–Cl·P–O 항 자연 포함)로 조성군 열축 스크리닝 = [Fan26]이 부른 "즉시 이식"의 우리식 구현 |
| **B④ moisture — 레버 = O(P–O 결합) 격자도핑** (Cl 함량 아님) | **La-O doped 승** | **[Yang25]** La₂O₃ x=0.04: H₂S 3.2→**2.3 cm³/g**(15 min 포화)·노출후 σ 9.98e-2 vs 2.53e-3(39×)·**500 °C 어닐 회복 43.5% vs 11.9%**·물침지 150 s 격렬반응 억제. 기전 주장 = **P–O가 P–S보다 절단 강함 + PS₃O³⁻=물리흡착(vs PS₄³⁻=화학흡착)** — 단 O 1s/Raman 無, ref 인용 수준 | 우리 **ICOHP P–O −8.43 vs P–S −5.98(+41%)·O@PS₄ site-preference −0.67 eV/O·500 K AIMD P–O 자발형성** = Yang P–O 주장의 *유일한* 원자단위 정량 근거 → **✓✓ 상호보완**(그들=관측, 우리=기전). ⚠ 가수분해 자체(기체 H₂O/H₂S)는 우리 0K hull 밖 — "우리가 H₂S 억제를 계산했다" 금지, P–O 결합강도·O 자리선호까지만 |
| **B④ moisture — *레버 = SE 입자 표면 유기코팅*** (조성 아님) | **유기 코팅 승** (조건부) | **[Qian26]** ⭐ 데칸산 2 wt%/25 nm: **39 % RH 2 h** 노출 후 XRD 무변화(bare는 **즉시 Li₂O₂+LiCl**)·**σ 1.13 mS/cm·유지율 91 %**·S2p 불변(bare는 163.2 eV 원소S 급증). 기전 **2중**: ① **소수성 C10 알킬 물리장벽**, ② **코팅 반응이 만든 산화-S 부동태**(코팅 직후 이미 S⁰ 163.2·thiosulfate 166.6 존재, P 2p 신호 소멸=표면 피복). + **Table S4 = 표면개질 LPSCl 11종 수분 문헌지도**(OScA/Se-doped/ZSM-5/LPSBI-Bromo/**UDSH**/OPA/g-C₃N₄/PBS/F-PDMS/Al₂O₃-ALD) | 우리 **가수분해 축 계산 0** — [Zhu20] 레시피가 있어도 **유기 코팅은 MP hull 밖**이라 이 레버는 구조적으로 우리 도구 밖. 다만 **XPS S 산화 사다리 5점(160.2 Li₂S / 161.6 PS₄³⁻ / 163.2 S⁰ / 166.6 thiosulfate / 168.0 sulfate)** 중 3점이 우리 `xps_reference_sei.csv` anchor와 **정확 일치**, **thiosulfate 166.6 = 신규 anchor 후보**. ⚠ **Table S4는 순위표 아님**(RH <1–50 %·시간 30 min–3일 제각각, 저자 자인) — UDSH(33 %/5 h/86 %)가 더 가혹한 조건. ⚠ 최장 노출 **2 h** → 드라이룸 실사용(수 시간~일) 주장엔 데이터 부족 |
| **B④ moisture — 가수분해 열역학 *원전 지도*** (조성·cation 전수) | **thiophosphate(P⁵⁺) 최악 / 산물 LiCl·Li₂S는 무해~조건부 안정** | **[Zhu20]** MP-hull grand-potential(μ_H₂O·μ_H₂S; 0.1 %/1 ppm): **Li₃PS₄→¼Li₃PO₄+H₂S ΔG=−0.608 eV/H₂O**(자발, P₂S₅보다 나쁨 = **초안정 인산염 구동력**이 H₂S 엔진) vs **Li₂S +0.225(조건부 안정)·LiCl 등 염화물 거의 전부 안정 — LiCl+H₂O→LiOH+HCl +0.977 eV/H₂O(SI 정확값, LiCl-buffer 수분 불활성의 정량 인용치)**; Li함량↑⇒Li₂S 수준 수렴; HSAB 서열 정량화(Zn/Cd/Cu/Ag≫Ga/Ge/Sn/Sb/Bi≫**P·B 최악**) | 우리 **가수분해 축 계산 0**(늘 "기체 H₂O/H₂S는 0K hull 밖") — **단 [Zhu20] SI가 절차를 완전 명세**(MP hull+50 meV + NIST-JANAF 기체 μ(Δμ=k_BT ln x) + **대표반응=pseudo-binary S–O 프로파일 최저 ΔG(tracer-H₂O 극한)·hydroxide는 pseudo-oxide 삽입**) → 우리 파이프라인으로 즉시 구현 가능, comp1/modelc/LPSOCl/+B₂O₃/Nd 조성의 ΔG_hyd 후속(§H). **기전 정합**: 그들 "인산염 구동력" = 우리 **ICOHP P–O −8.43 ≫ P–S −5.98·O@PS₄ −0.67 eV/O**의 열역학판 → **O-doping(LPSOCl)=가수분해 구동력을 합성 단계서 선지불**([Yang25] P–O 관측·[Wang22] O 열안정과 한 줄). **⚠ B³⁺=가수분해 최악급(S계·Cl계 모두)** → +B₂O₃ 조성은 B–O 배위 유지 여부가 수분 리스크 관건(산화축 이득과 축-분리 필수). ⚠ 인용 시 조건(0.1 % H₂O) 병기 — Li₂S도 습도 올리면 뒤집힘 |
| **B① thermodynamic vs kinetic ECW 프레임** | (개념) | **[Kang]** Fig1b: full-cell **thermodynamic / kinetic / predicted ECW** 구분 (kinetic passivation이 창을 넓게 보이게) | 우리 grand-potential onset 2.256 = **thermodynamic ECW**; 실험창(>3 V) = kinetic. **✓ 우리 "실험창이 왜 넓나"의 정확한 그림** (Fig1a ref49 Zhu/He/Mo = 우리와 동일 grand-potential 방법) |
| **B③ CAM/SE 계면 비호환 산물** | **Cl-rich 무관(조성 일반)** | **[Kang]** Fig3b,c (Banerjee ref51 AIMD): LPSCl–delithiated NCA → **LiCl·Li₃PO₄·NiS₂** 자발형성; 고SOC O방출→SOₓ | 우리 interface_reactivity·sei_products.json도 LiCl·Li₃PO₄ 예측 → **✓ 일부 같은 산물**(NiS₂는 우리 6원소 hull에 Ni 없어 못 봄) |
| **B① 방법 *원전* (grand-potential ESW 형식) + 창 경계 맵핑** | (방법 계보 — 우위 판정 없음) | **[Zhu15]** ⭐: μ_Li(φ) construction·plateau 창 정의·**LPSCl 1.71–2.01 V**(red: P+Li₂S+LiCl(+5 Li) / ox: **Li₃PS₄+S+LiCl(−2 Li)**)·"true(thermo) vs nominal(kinetic 과전압+passivation) 창" 원형·coating anodic 2–2.3→~4 V | **✓✓✓ 형식 동일** — esw_grand_potential/cascade_batch = pymatgen `get_element_profile` = 같은 construction·같은 창 정의(hull 세대만 2015→2026). **경계 맵핑(2026-07-28, digest §10b)**: ① **Zhu red 1.71 ≡ 우리 `ocv` 1.717**(같은 hull 경계 Li₃PS₄+5Li→P+4Li₂S; **Δ0.007 V — 11년 DB 세대 차에도 불변**) — "Zhu 1.71 vs 우리 red 1.24"는 **라벨 관례 차**(pymatgen row=field 저전압 끝 vs Zhu 표=고전압 끝; 우리 red_V 1.242=심화환원 P→LiP₇ 경계=Zhu 1.30)·물리 불일치 아님 → **문헌 대조 시 Zhu-관례 환원전위는 우리 ocv_V(1.717)로 병기**; ② **Zhu ox 2.01 → 우리 2.14(PLAIN)/2.256(GG set)** — onset 반응은 GG-set과 **동일**(−2 Li·원소 S=Zuo Eq1), 전압만 MP2020 S-보정+LiS₄ entry로 +0.13~0.25 V(환원측 경계는 양변 sulfide라 S-보정 상쇄=DB-robust, 산화측은 S²⁻→polysulfide/S⁰로 비상쇄=DB-민감 — **산화 onset은 hull 세대·보정·entry set 명시 없이 이식 금지** 규율의 근거 완성). **+ cascade collapse 판정(window<0.05 V, Fe/Co/Ni/Mn 회피)의 원전 근거**: Zhu 설계원리 "환원 쉬운 cation=창 좁힘+전도성 산물로 passivation도 실패" — 단 같은 원전이 LLZO −0.021 eV/atom을 "DFT 정확도 이하=inconclusive"로 자인 → **collapse는 회피 필터로만, <0.05 V끼리 미세 순위 금지** |
| **B③ cathode 계면 — *열역학 형식화 원전(pseudo-binary)*** | (방법 원전 — 우위 판정 아님) | **[Rich16]** eq 2(닫힌)/eq 4(Li-개방, μ_Li=양극 평균전압)/eq 5(no-mixing 분리)로 양극 7×전해질 ~30 전 조합 산물·구동력 표준화(SI S1–S9): thiophosphate\|layered oxide 최대(PO₄·TM황화물 형성; LiCoO₂/LiNiO₂ 최악·LiFePO₄도 불안정, figure-read ~−0.5~−1.1 eV/atom)·산화물 전해질 0~−0.3·**Li₃PO₄·LiF 전 조합 불활성**·**"@V none ≠ mixing none" 클래스**(Li₂MgCl₄·LiAlCl₄ 전 양극·LiNbO₃\|LiNiO₂→Li₃NbO₄+NiO — LNO도 고-Ni엔 화학적 무결 아님); 분해E↔수명 상관(LiTiS₂ 셀 50+cyc·LiBH₄\|LiCoO₂ 저항증가·LiCoO₂/Li₂S–P₂S₅ P·Co 상호수송 ref49) | 우리 **interface_reactivity = 이 형식의 pymatgen 직계**(`nd2o3_interface_reactivity` 등; [Sundar]도 동일 도구) → **✓✓ 방법 원전 확보**. Li₆PS₅Cl\|LiCoO₂ 산물: 그들 `CoSCl+S+CoP₄O₁₁+CoS₂`(평균전압 μ, 심탈리튬) vs 우리 `Co₉S₈+Li₃PO₄+Li₂S+LiCl+Li₂SO₄`(−0.32~−0.33 eV/atom) = **같은 형식·다른 μ_Li/hull 세대 → μ 명시 없이 산물 등치 금지**. 그들 양이온 예외(Li₂MnBr₄ Mn²⁺ 산화 창축소·Zn/Cd/In/Al 저전압 금속 환원) = **우리 collapse/late-TM 회피 판정과 동일 물리의 양면**(산화측 새 채널+환원측 MCI) — 단 Richards엔 자동 collapse 플래그 없음(우리 기여); 계면E 무시 상한 ~0.1 eV/atom → 미세 \|ΔΦ\| 조합의 부호/순위 확정 인용 금지 |
| **B③ ★ Li₆PS₅Cl의 양극별 계면 구동력 — *문헌 최초 수치 확보*** | (문헌 기준선 — 우위 판정 아님) | **[Rich16] SI Fig S3 벡터 정확 판독(2026-08-03 SI 실물 검증, digest §19d; ±0.005 eV/atom)** — 본문 Fig 4에는 Li₆PS₅Cl 행이 **없고** SI Fig S3에만 있다. `ΔΦ_no-mixing / ΔΦ` (eV per non-Li atom): **LiCoO₂ −0.97/−1.10** · LiFePO₄ −0.52/−0.52 · LiMnO₂ −0.51/−0.71 · **LiNiO₂ −0.49/−0.82** · LiTiS₂ −0.03/−0.04 · LiVS₂ 0/−0.01 · **Li₂S 0.00/0.00**. 같은 표의 이웃: Li₃PS₄ −0.69/−0.97 · LGPS −0.81/−1.01 · Li₄SnS₄ −1.10/−1.10 · Li₂S −2.91/−2.91 (@LiCoO₂) | 우리 `nd2o3_interface_reactivity`(vs LiCoO₂) **−0.32~−0.33 eV/atom** — **절대값 비교 금지**(μ_Li·hull 세대·정규화 기준이 다름). 대신 **구조적으로** 쓸 것. **🔑 세 가지 구조적 판정**: ① **argyrodite는 "혼합 없이도" 황화물 중 최심급**(−0.97) — LPSCl 열화의 **88 %가 mixing 이전에 이미 확정**(LiCl까지 소모돼 S–Cl 화학으로 가기 때문 = 우리 staircase 3.326 V SCl 단계와 같은 화학) ⇒ **"코팅으로 화학 접촉만 막아도 전위 노출분은 남는다"**가 이 논문 자체의 수치로 성립. ② **혼합 몫이 LFP 0.00 → LCO −0.13 → LMO −0.20 → LNO −0.33로 단조 증가** = 우리 **고-Ni 주의보의 정량 근거**(산물 Ni₃S₄+NiCl₂+Li₄P₂O₇). ③ **LPSCl\|Li₂S = 정확히 0.00/0.00** — Li–S 계에서 argyrodite는 열역학적으로 무해. ⚠ 2015 hull·figure 복원값·평균전압 μ 고정 |
| **B③ cathode 코팅 후보 발굴 — *HT 게이트 스크리닝 원전(funnel)*** | (방법 계보 — 우위 판정 아님; **폴리음이온 산화물 승**이 그들 결론) | **[Xiao19]** ⭐: [Zhu15] ESW+[Rich16] Eq 4를 **104,082종 깔때기로 게이트화** — Eg>0.5 eV(62,437)→E_hull<5 meV/atom(1,600)→**V_ox≥4.0 & V_red≤2.7 V**(302; 통과율 폴리음이온 26.5 % vs 비폴리 7.8 %·"기타" 1/439 전멸=음이온 화학이 지배)→**&#124;ΔE_rxt&#124;<100 meV/atom vs LPS+만충 NCM**(184)→폴리음이온(66)→NEB 6종→**LiH₂PO₄·LiTi₂(PO₄)₃·LiPO₃** 추천·붕산염 LiBa(B₃O₅)₃ 화학안정 챔피언. **LPSCl(=comp1) 소환값: /LCO −339(만충)/−493(반충)·/NCM −330/−471 meV/atom**, 산물 Li₃PO₄+Li₂S+Co₉S₈+Li₂SO₄+LiCl; SSE 반응성은 반충전이 악화·코팅은 완화(Li₃PO₄-형성이 양극 Li 필요) | 우리와 3중 접점: ① LPSCl ESW ~1.7–2.0 V(figure-read)=[Zhu15] 동세대 → 우리 1.717/2.14–2.256과 정합(hull 세대 규율 그대로); ② LCO 반응 산물 **Li₃PO₄·Li₂SO₄·LiCl 공통**(우리 interface_reactivity; 그들 Li₂S+Co₉S₈ vs 우리 폴리설파이드 = entry 세대) — **우리도 ΔE_rxt 절대값(meV/atom) 열 병기하면 1:1 완성**; ③ **O-공유결합→V_ox↑ 기전(meta>pyro>ortho·B–O 806 kJ/mol) = 우리 ICOHP P–O −8.43(P–S −5.98 대비 +41 %)의 문헌 원리판 — ⛔ **2026-08-16 철회**: 여기 붙어 있던 "우리 B₂O₃ onset **+0.18 V**"는 이 원리의 우리 쪽 실증이 아니다. 그 +0.177 V 는 chain generator 조성 `Li₁₇B₂P₄S₁₆Cl₅O₃` 의 값이고, **같은 자리 plain 조성** `Li₁₈B₂P₄S₁₇Cl₄O₃` 는 **2.034 V = host(2.140) −0.106** 으로 오히려 내려간다(legacy DFT-deep 셀 `Li₅₈P₈S₄₁Cl₁₆B₂O₃` 도 2.03 V). Xiao 의 O-공유결합 원리는 **코팅 물질 골격 자체**에 대한 것이고 우리는 **host 격자에 산화물을 소량 넣은 것** — 같은 명제가 아니다 (digest §7d)**. **+ SI 재검증(2026-08-03)에서 나온 2점**: ① **기존 3원 산화물 코팅 3종(Li₂ZrO₃·LiNbO₃·LiTaO₃)이 저자 자신의 filter 4를 통과 못 함**(LPS와 −115/−164/−139 meV/atom → Table S1 106종에 부재) — 우리 코팅/도판트 서사에서 "LiNbO₃가 표준이니 기준선"이라 쓸 때 **그 표준이 열역학 게이트를 못 넘는다**는 반대 근거로 인용 가능; ② **불화물이 V_ox 최강**(35종 전부 ≥4.99 V, LiBF₄ 7.15) — 폴리음이온 승리는 안정성이 아니라 **σ 문헌 부재**로 갈린 판정이라, 우리 F-variant 도판트(O/F-degenerate 판정) 논의에 "F는 산화안정 축에서 최상위, 병목은 이동성"이라는 문헌 지지로 사용. ⚠ NCM(Ni/Mn) 우리 hull 밖 → −330/−471은 소환값(재현 불가); V_ox 절대값은 2018-세대 내부 DB — 현대 hull과 혼용 금지 |
| **B① 음이온 축 재분리 — *F와 Cl은 같은 "할라이드"가 아니다*** | **F 압승 / Cl은 하위군** (산화한계 축 한정) | **[Xiao19]** Table S1 106행 전수(2026-08-03 Sup1 정식 SI 실물 파싱, digest §16): **불화물 35종 V_ox 중앙값 6.53 V**(범위 4.99–7.15) vs **염화물 10종 4.29 V**(4.25–4.51, 5군 중 비폴리 산화물 다음으로 낮고 가장 좁은 밴드). **LiF 6.39 vs LiCl 4.25 = 같은 Li 염에서 음이온만 바꿔 +2.14 V.** 부수: F군은 이봉분포 — 상위 29종 6.32–7.15, 하위 5종 중 **4종이 Cr 함유**(TM이 V_ox를 깎는다) | **우리 Cl-rich 서사의 축 명명에 직접 쓰임**: Cl은 σ·격자 극성률([Kraft17])과 계면 무반응성(ΔE_rxt 0급)에 기여하지만 **산화 한계를 올리는 음이온은 아니다** — 우리 onset이 조성 무관 **S-limited 2.256 V**로 고정되는 것과 모순 없고, [GG]/[Banik]의 "Cl은 창을 못 넓힌다"와 같은 방향. F-variant 도판트 논의에서는 반대로 "F는 산화 축 최상위, 병목은 이동성"으로 인용 |
| **B③ SOC 비대칭 — *탈리튬에서 반응이 켜지는 유일한 음이온 = Cl*** | **Cl 함유 = 고SOC에서 불리** (부호 전환의 의미, 크기 아님) | **[Xiao19]** Table S1 전수: `|ΔE_rxt(반충 NCM)| > |ΔE_rxt(만충 NCM)|`인 물질이 **106종 중 7종뿐이고 7종 전부 Cl 함유**(Cl 함유 12종 중 7 / Cl 비함유 94종 중 0). **LiCl·LiCsCl₂·LiRbCl₂는 만충 정확히 0.000 → 반충 −13~−17 meV/atom**. 나머지 폴리음이온은 반대로 반충에서 완화(Li₃PO₄ 형성이 양극 Li를 요구) | **🔑 실무 지침**: 우리 `interface_reactivity`를 **만충 LCO 하나로만** 돌리면 Cl의 위험이 *구조적으로* 안 보인다 — **반충(탈리튬) 양극 entry를 반드시 병행**해야 함(digest §11-4a 갱신). ⚠ 절대값은 −13~−23 meV/atom로 작다 — "위험"은 순위·부호 전환의 뜻이지 크기의 뜻이 아님 |
| **B③ 코팅 분해산물의 *전자전도성* — 기존 3원 산화물이 더 나쁘다** | **폴리음이온(LiPO₃) 승 / LiNbO₃·LiTaO₃·Li₂ZrO₃ 패** | **[Xiao19]** Table S5 실물(2026-08-03): **LPSCl/LiNbO₃ → Li₂S, LiCl, Li₅(NbS₂)₇, 원소 S, Li₃PO₄** · **LPSCl/LiTaO₃ → TaS₃, Li₂(TaS₂)₃, Li₃TaS₄, Li₃PO₄, LiCl** · **LPSCl/Li₂ZrO₃ → Li₂ZrS₃ 포함** vs **LPSCl/LiPO₃ → Li₃PS₄+LiCl+Li₃PO₄(전부 절연성)** | [Sundar]의 "**산물의 전도도가 진짜 지표**" 비판이 정확히 여기서 실물화 — 우리 `sei_products` gap 축과 같은 논리. §15b-2(3원 산화물이 저자 자신의 filter 4 탈락)와 합쳐 **현행 표준 코팅 비판의 이중 논거** |
| **B① 게이트 관점 — 형성E 상한 V̂_ox=ΔG_f/xF로도 황화물 SE 전멸** | (게이트 설계 — 우위 판정 아님) | **[Sendek17]** V̂_ox(완전 원소분해 상정 **상한**; Fig S1에서 [Rich16] 엄밀 DFT V_ox 대비 "2건 근소 예외 빼고 항상 ≥" 확인, [0,3] V 구간 정확) ≥ 4 V 게이트: bcc-유망 황화물 **Li₁₀Ge(PS₆)₂ 3.2·Li₇P₃S₁₁ 3.5·Li₃AsS₃ 2.8 V 탈락**(전도도가 아니라 산화안정에서 죽음); Li₃OCl 3.44·Li₆MgBr₈ 3.86도 탈락(모델은 옳게 양성) | 우리 grand-potential onset **2.256 V**(S²⁻-limited, 축①) — V̂_ox는 hull 분해 onset이 아니라 **의도된 과대 상한**(같은 표 금지) | **✓ 방향 정합·수치 이식 금지**: "황화물 산화한계 낮음"의 제3 계산 계보(상한식으로도 <4 V) = [Zhu15] 1.7–2.3 V·[Rich16] S-지배·우리 2.256·[Son] "<2.5 V"와 같은 줄기 — 단 V̂_ox 절대값(LGPS 3.2 등)은 상한이라 onset과 등치 금지. **+ 깔때기 교훈: "전제조건(안정·gap·ESW)이 전도도 스크린보다 후보를 세게 걸러냄"(모델 단독 1,408 vs 깔때기 21)** = 우리 cascade가 값싼 열역학 게이트를 앞단에 두는 순서의 문헌 근거 |
| **B① 방법 前史 — 2-포인트 grand potential + "intrinsic redox 단독 평가는 위험" 원문** | (방법 계보 — 우위 판정 없음) | **[Ong13]** (2013, [Zhu15]의 전신): μ_Li 두 극단(μ⁰ / μ⁰−5 eV)의 평형상만 — **onset 전압 없음**. 5 V: 산화물 MₓPᵧO_z+**O₂ 방출**("장기 안정성 심각") vs 황화물 GeS₂/P₂S₅/S("유리질 전도체=passivating 가능", ref 7 "실험 >5 V 창=passivation"의 조성족 확장); **HSE gap(intrinsic) 최고인 산화물이 계면(Table 3)에선 최악 → "전극 화학호환이 동등 이상으로 중요"** 명문 + "gap은 창의 상한일 뿐(외부 기준전위 정렬 모름)" | 우리 onset 스캔(1.717/2.256 V)은 [Zhu15] 직계 — Ong13은 산물만 주는 전신. **산물 화학은 3세대 연속**: LGPS 0 V Li₁₅Ge₄+Li₂S+Li₃P·5 V GeS₂+P₂S₅+S가 [Zhu15]와 동일(11년 hull 세대 불변의 앞 사례). **"gap=상한≠onset" = 우리 VBM≠onset·B①/B③ 분리 규율의 2013 원문**([Banik] 분리 프레임의 조상). ⚠ "Ong13이 LGPS 창 1.7–2.1 V 계산" 인용은 오귀속([Zhu15] 몫); Li 불안정 최초 예측도 Mo2012(ref 7) |
> - 우리 ESW는 **B①만** 봄(S-limited 구조적). 분해 *양*([Zuo] CV 2×)·metastability(DSC/TGA)·기체는 못 잡음.
> - **🔑 [Banik] (외부·Zeier+Mo, 이 논문) = B① 전체(onset·메커니즘·방법)의 외부 정답지**: "P→Si/Ge·Cl→I 치환은 산화 onset 못 옮긴다(VBM=S 3p가 pin)"를 HAXPES+grand-potential+CV 3중 교차로 실증. **우리 axis_1(comp1=modelc onset 2.14 V·VBM 달라도 동일)·VBM≠onset·grand-potential 방법이 모두 외부·동그룹(Mo=우리 인용 Mo2012 저자)으로 검증됨.** ⚠ 그러나 **Banik 명제를 *절대화* 금지**: (a) Banik 치환축 = MS₄/할라이드 *동족 교환*만 → 우리 Cl *증량*(modelc)·격자 *산화물 도판트*(cascade)는 안 봄; (b) **우리 cascade는 onset을 *옮기는* 소수 예외 발견** — B₂O₃(ox 2.317 V, +0.18)·Cr₂O₃/Sc₂O₃/In₂O₃/Ga₂O₃(2.356)·Y₂O₃(2.282)이 *새 산화-한정 반응*을 만듦(대부분은 2.14 pin). 즉 "**iso-structural 치환은 S-onset 불변(Banik=우리 다수)**, **이질 산화물 도판트는 onset 소폭(≤0.2 V) 이동 가능(우리 예외)**" — 단 어느 경우도 *S backbone* 산화는 못 늦춤(Banik의 S-pin은 backbone 수준서 robust). → deck: Banik이 닫은 "치환=산화창 불변"을 출발점으로, 우리는 (i) Cl-rich 4축(B②③④), (ii) 예외 도판트, (iii) Nd O-doping passivation을 *우리 기여*로 분리.
> - **[Banik] 결론 "코팅/타 물질군 필요" = 우리 그룹 cathode-interface 라인([Cha]/[Kang25]/[Kang])·[Sundar] ALD 코팅 스크린의 *문제설정*을 외부 정당화**: intrinsic SE 산화창은 치환으로 못 늘리므로(S-pin), 실전 고전압은 *계면 관리*(코팅·passivation)로 간다는 서사 완성.
> - **🔑 [Rao] (외부·I 치환 DFT, 이 논문) = "I는 산화 onset 레버 아님"의 *침묵 증거* + [Banik] 보강**: Rao는 Cl–I argyrodite를 상안정(E_hull)·전극 호환(ΔE_D)·σ로만 평가하고 **산화 onset(V)은 *전혀 계산/주장 안 함*** → I의 셀링포인트가 산화창이 아님을 *논문 구성 자체*가 말함. **I⁻/I₂가 Cl⁻보다 쉽게 산화됨에도** (a) 소량 I(x≤0.5)면 **S²⁻가 여전히 다수 → S-limited 유지**가 더 가능(Banik의 S-pin), (b) "I가 onset 낮춘다"는 *가설*로만(우리 grand-potential I-chemsys로 미확인). **밴드갭은 오히려 Cl–I(2.32)>Cl–Br(2.19)이나** VBM character 미분석·PBE라 "I 전자절연/산화안정 우수"로 읽기 금지(I p가 VBM 위로 오면 *오히려* 산화 쉬울 수도). → **deck: Cl·Br·I 어느 할라이드든 intrinsic onset은 S-pinned 무관(Banik+Rao 침묵), I 효과는 *다른 축*(σ 채널·상안정 E_hull·계면 ΔE_D)**. 반드시 축 명명.
> - **[Kang] 리뷰**: 산화 ~2.0–2.5 V(Fig1a)·thermo vs kinetic ECW(Fig1b)·계면 비호환 산물(Fig3 LiCl/Li₃PO₄/NiS₂)로 **우리 산화 프레임을 우리 그룹 리뷰가 직접 정렬**. O-doping(§5.1b)이 ECW *확대*(CV 관찰=kinetic)라 서술 ↔ 우리 Nd hull은 intrinsic 창 *narrows*(thermo) → **다른 축**(둘 다 맞음, 명명 필수).
> - **[Kang25] (우리 그룹 실험, 이 논문)**: "이로운 기생반응" = 고전압 LPSCl 산화분해[식1]가 NCM을 **균일 재리튬화(SOC↓)** → layered→rock-salt 억제 → +15.0 % 유지율. **🔑 우리 narrative와의 두 가지 정밀 정렬**: ① 식1 산물(P₂S₅계+S+LiCl) = **우리 grand-potential 산화분해와 동일 화학** → *같은 그룹 실험이 우리 계산을 (간접) 검증*; ② **그러나 이로움의 *메커니즘*은 SOC-강하(코팅 균일화)이지 wide-gap 절연 CEI가 아님** → 우리 **Nd passivation(NdPO₄/NdCl₃ 절연 e⁻차단)과 *다른 physics*** (Kang 산물 중 LiCl만 절연, P₂S₅·S·폴리설파이드는 전도성). **"Kang = Nd passivation 실험증거"라고 하면 틀림**; 둘은 *상보적 두 레버*(코팅=SOC관리 / 도핑=절연CEI). 변수도 Cl이 아니라 *SE 코팅 유무* → 4축 Cl표에 넣지 말 것.
> - **[Cha] (우리 그룹 실험, 2024 — cathode-interface 라인 *기원*)**: NCM에 **할라이드 SE(LIC/LYC/LZC) 나노코팅**으로 NCM-LPSCl 계면을 *차단*. 결정 변수 = **dual compatibility**(코팅이 NCM·LPSCl *양쪽*과 무분해) — **LZC=Li₂ZrCl₆**만 만족(7일 무분해)·LIC(In₂S₃)·LYC(Y₂S₃) 비호환. **🔑 우리 narrative와 두 정밀 정렬**: ① **σ≠계면저항**(σ LIC>LZC>LYC인데 계면저항 LZC≪LIC·LIC는 bare보다도 나쁨) = 우리 "lever=interphase, not bulk σ"의 cathode-side 증거(축 A에도 등재); ② **dual-compatibility(6계면)=우리 `GrandPotentialInterfacialReactivity` 도구의 완벽한 적용대상**(왜 Zr⁴⁺만 견디나 in-silico). **그러나 이로움 메커니즘 ≠ Nd passivation**: Cha=*비반응성 코팅(no new interphase)*, Nd=*능동적 wide-gap 절연 CEI 형성* → 위치 다름(레버 A=[Kang25]SE코팅·B=[Cha]할라이드코팅·C=우리 SE도핑, 셋 다 *다른* 레버). **변수 = Cl 함량 아니라 *코팅 할라이드 종류* → 4축 Cl표에 넣지 말 것**(이 표는 cathode-interface 레버 행으로만). ⚠ Zr 우리 hull 부재 → 정량은 향후.
> - **🔑 [Son] (외부·Nat. Energy 2025, 이 논문) = B① 황화물 산화 한계의 *외부 실험 캡스톤* + 코팅/물질군 서사 완성**: Son이 본문에서 "황화물 SE <2.5 V"·"할라이드 ~4.3 V부터 분해"를 *명문화*하고, 5 V급 LNMO/LCMO를 위해 **새 불소계 SE(LiCl–4Li₂TiF₆, >6.7 V)를 차폐층**으로 도입(2C 500cyc 75.2 %·35.3 mAh/cm²). **세 정렬**: (a) **우리 grand-potential 2.256 V(S²⁻-limited) ↔ 본문 "<2.5 V" 정량 일치** — 우리 thermo onset이 *Nature Energy 출발 전제*를 수치로 뒷받침; (b) **[Banik] S-pin "치환으론 못 늘림→코팅/타 물질군 필요"의 *실현*** — Son이 *타 물질군(불소계)* 으로 5 V 달성(Banik은 SE intrinsic, Son은 차폐층 = 같은 결론 다른 구현); (c) **우리 그룹 [Cha] 할라이드 dual-compat 코팅의 *전압 천장* 명시** — 할라이드(LYC/Zr-OCl)조차 ~4 V서 분해 → [Cha]는 NCM 4 V급엔 유효하나 **5 V급(LNMO)엔 부족** → 우리 코팅 서사를 "4 V급 계면관리"로 정확히 위치, 5 V는 *물질군 교체* 영역. ⚠ **절대화·과확장 금지**: 불소계(Ti/F)·할라이드(Y/Zr)는 우리 6원소 hull 밖 → 6.7 V·4 V 수치는 *Son이 계산*한 것이지 우리 재현 아님(방법만 동일); "우리가 5 V 차폐 SE를 검증했다"식 금지. 황화물 한 줄(<2.5 V↔2.256)만 우리 값과 엄밀 정합.
> - **🔑 [Qian25] (외부·Nazar 2025, 이 논문) = "코팅은 *그 자체*가 아니라 *분해산물*로 심사한다" 의 절차화 + 우리 계면열역학 도구의 외부 대조군**: LiPON 선례(*"LiPON 이 고전압 양극과 호환되는 건 그 분해산물 Li₄P₂O₇·LiPO₃·P₄O₁₀ 가 산화안정하기 때문"*, ref [7]=[Rich16])를 **설계 원리로 일반화**해 LiPO₂F₂ 를 골랐다. 계산 3층 = **① 코팅 혼자의 창**(`get_element_profile`) → **② SE 와 섞였을 때**(닫힌 pseudo-binary) → **③ 작동전압에서**(grand-potential, μ_Li 2점 고정) — **우리 `esw_grand_potential.py` + `interface_reactivity.py` + `interface_reactivity_v2.py` 와 같은 클래스·같은 순서**다. **🔑 우리 쪽 정보량이 더 많다**: 그들은 2.8/4.3 V **두 점 스냅샷**인데 우리 v2 는 **전압축을 훑어 산물 세트가 바뀌는 kink 전압**을 낼 수 있다 — 이 논문이 못 낸 값이고 우리 그림의 차별점. ⚠ 반대로 **재현성은 그들이 아래**다: 계산 절이 **11줄**이고 functional·U·PAW·MP 버전·**MP2020 음이온보정**(황화물+산화물+불화물 혼합 hull 에 필수)·**LPSCl S/Cl 배열**·NCM 고용체 배열이 **전부 미기재** → 우리 `estimand_card` 규율의 *"admissible state 가 여럿인데 선택 규칙이 없다"* 전형. 우리 원고 SI 는 이 수준이면 안 된다. ⚠ **자기 게이트의 4배(−395 meV/atom)를 근거 없이 "속도론이 막는다"로 넘기는 논증**은 우리가 하면 안 되는 견본(검출한계 미제시 → "없다" 가 아니라 "못 봤다").
> - **🔑 [Qian25] 에서 F 축 경고 하나**: `Fig. 1f`(4.3 V) 는 **F 가 TM 으로 갈아타 Li₂NiF₄** 를 만든다고 예측한다. LiF(gap 8.7 eV)는 최고의 절연 CEI 지만 **고전압에서 F 가 TM 불화물로 이동**하는 경로가 있다 → 우리 cascade 의 **F 계열 도판트 검토에 이 게이트를 반드시 넣을 것**.
> - **deck 결론**: "전도도 이득이 산화창 손해 없이(B①–③ 중립~유리), 비용은 shelf-life(B④). **양극 계면은 별도 레버로 관리** — 4 V급은 코팅·도핑([Cha]할라이드 dual-compat / [Kang25]SE코팅 균일화 / 우리 cascade SE도핑), **5 V급은 산화안정 차폐 SE 물질군 교체([Son] 불소계 LiCl–4LTF)**. 황화물 intrinsic 산화창은 어느 경우도 못 늘림(우리 2.256 V·Banik S-pin·Son <2.5 V)." 축·레버·전압대 명명 필수.
> - **⚠ "넓은 ESW" 문헌 over-claim 주의 (carbon-composite kinetic ≠ thermodynamic)**: **[Taklu]** "**8 V ultra-wide ESW**"(CuCl 도핑, Fig 3b)는 **(a) In/InLi 기준**·**(b) carbon-composite CV의 *kinetic/접근성*** 측정 — 황화물 *intrinsic* 산화 onset이 아님. Cu가 bridging-S를 *kinetically* 안정화(분해전류 160×↓)하는 건 사실이나, **thermodynamic 산화창은 여전히 S²⁻-limited ~2.3 V**([Banik] VBM=S 3p·우리 grand-potential 2.256 V). → **"CuCl/도핑이 산화창을 N V로 넓혔다"는 인용 금지** — "carbon-composite 셀 kinetic 분해전류 감소"로만. (Dewald ref49 "planar는 분해 과소평가"를 저자도 인용하나 composite 8 V도 동일 함정.) — **동일 함정 3번째 사례 [Zhou26]**: LGPS 고엔트로피 조성의 *"decomposition potential exceeds 5 V"* (Fig 2b)는 **Li \| SE \| 스테인리스 blocking, 카본 없음, 1 mV/s 단일 스윕** — [Adeli]가 경고한 **평판 셀 = 분해 *과소*평가** 유형이다([Taklu]는 carbon-composite = *과대*, 방향은 반대지만 둘 다 kinetic). **LGPS 계의 열역학 창은 `fan2026…review` 기준 1.71–2.14 V** 이고 Ge⁴⁺ 환원 때문에 argyrodite 보다 오히려 좁다. → **"고엔트로피가 5 V 안정성을 준다"는 인용 금지**; 쓰려면 "blocking-electrode CV 에서 5 V 까지 유의 faradaic 전류 미검출(동역학적)"로만. **⚠ 단 [Zhou26]의 Li *금속 측* 주장(CCD 2.5 vs 1.6 mA/cm²·대칭셀 1200 h·풀셀 100 cyc)은 대조군이 있고 조건이 HE 에 불리했으므로 별개로 신뢰 가능** — B축(산화)이 아니라 E축(환원/음극)의 값이다.
> - **LiS4 단서**: 우리 onset 2.14 vs [GG] 2.40 차이 = LiS4(mp-995393) 포함 탓 → 제외 시 2.26 (정합↑).
> - **🧬 계보 note [Xiao19] — 게이트 1:1 벤치마크 (우리 cascade 발표용; 풀 표는 digest §7c)**: 대상부터 다름 주의 — Xiao=**코팅 물질 발굴**(104,082 풀), 우리=**host 도판트 스크리닝**(modelc 계열 4 f.u. 셀; **91 화합물 계획 → 270 슬롯 완주 → base 90종**. ⚠ 흔히 쓰던 "47종"은 **2026-06-29 취합 경계**지 물리 게이트가 아니다 — `cascade_v23_all_20260629_47species.csv`. 그리고 x002/x005/x010 은 농도가 아니라 **라벨**로, 전부 generator loading 0.25 다) → 수치 이식 금지, *게이트 설계*만 대비. **계승 3축**: 상안정(그들 E_hull<5 meV/atom 절대-hull boolean ↔ 우리 stable 0.25 가중·UMA-상대 de_post_anneal) · grand-potential ESW(그들 V_ox≥4.0/V_red≤2.7 절대 문턱 ↔ 우리 ox 0.30 가중+**window>0.05 V collapse 게이트**(late-TM 회피) — S-limited host라 절대 문턱 대신 미세이동·창붕괴 좌표계) · 이온전도 프록시(그들 CI-NEB 6/66종만·LiPO₃ 0.40 vs exp 1.40 eV 실패 자기보고 ↔ 우리 BVS proxy 전수 — 단 **G4 는 세 라벨 평균이 아니라 x005 한 점**이고, ⛔ **MLIP-MD 검증은 v23 에서 0/270 미실행**(stage 10). 즉 동역학 축은 **그들만 있고 우리는 비어 있다**). **우리 추가 3축**: 기계 soft 0.20+ductile 0.15(=가중 35 %, Xiao 전무) · 테마 12+1 조합+co-doping 교호작용 ML · UMA-상대 엔진(그들 "HT에 ab initio 전도는 과비용" 자인 공백의 해법). **우리 공백 2축**: **양극(NCM/LCO) 반응성 게이트**(&#124;ΔE_rxt&#124;<0.1 eV/atom·만충/반충 — §H 보강책) · 10⁵ 후보 풀. **스코어링 철학 차**: 순차 boolean 깔때기(경계 정보 소실; LiCoPO₄류 일괄 탈락) vs 가중 score=0.30 ox+0.25 stable+0.20 soft+0.15 ductile+0.10 window(순위·trade-off 보존; 대신 가중치 자의성 리스크). ⛔ **승인된 current ranking 은 0종** — 47종 시대의 1위(Sc₂O₃ 0.813)는 superseded 스냅샷이라 결과로 인용 금지. ⚠ **배치 잡음**: 같은 종 3점의 흩어짐 ÷ 종간 SD 가 **E_young 1.10 · BVS 2.81** — 그 두 축(G5 soft·G4)의 순위는 물질 차이가 아니다. 발표 1-liner: "우리 cascade는 Xiao 2019 깔때기의 게이트 축(상안정·ESW·전도 프록시)을 계승하되, boolean을 가중 score로 바꾸고 기계·조합·ML 축을 추가했다 — 양극 반응성 게이트와 10⁵ 풀은 그들 고유."
> - **🧬 계보 note [Sendek17] — ML-스크리닝 원조 vs Xiao 깔때기 vs 우리 cascade (3자 한 줄씩; 풀 표는 digest §11–12)**: **Sendek 2017** = 12,831 → 물리 4게이트(317) → **ML 분류기**(5-특징 LR) → 21 — *전도도를 데이터로 게이트화한 원조*(전 물질군 발굴; argyrodite는 DB에 없어 못 봄). **Xiao 2019** = 104,082 → 물리 6게이트(NEB까지) → 3 — *전부 물리 게이트·ML 없음*(코팅 발굴). **우리 cascade** = **270 슬롯(base 90종)** → 가중 score+게이트 → TabPFN (⛔ MLIP-MD 검증은 **0/270 미실행**) — *host-내 연속 스코어+교호작용 ML*. **🔑 TabPFN(M1–M3)·랩 PPT 발표 앵커 문장**: "소표본 ML 재료 스크리닝은 Sendek et al.(EES 2017)이 실측 40종·5특징 로지스틱 회귀(LOOCV 오분류 10%)로 MP 12,831종을 21종으로 압축하며 정립한 노선 — 훈련 40 ≈ **우리 ML 학습 표본 47종**(codoping_ml_v2 stage1 n=47 — 캐스케이드 풀 90종이 아니라 2026-06-29 취합 스냅샷이다, 인용 시 구분 필수)으로 체급이 같아, 그들 방어 절차(LOOCV·5:1 특징 절제·X-randomization·d/ε/A 적용영역)가 우리 방어 논리의 직계 선례이고, 우리 TabPFN 루프는 같은 체급에 2026 엔진(사전학습 ICL)을 얹은 후속이다." **이식 3종**: X-rand+cR²_p → M1 정직성 지표 / d·ε·A → M3 winner's-curse 불확실성 페널티 / **enrichment 화법**("정확도 90%" 대신 "랜덤 대비 4배 농축·FP 18%", base rate 명시) → cascade/TabPFN 적중률 보고 표준. ([Fujimura13]이 있으면 계보는 **Fujimura13(1세대: 물리 특징+SVR 회귀·92조성) → Sendek17(2세대: 기하 특징+LR 분류·12,831 전수) → 우리 TabPFN(3세대: 특징공학 최소·사전학습 ICL)** 3단으로 확장)
> - **🧬 계보 note [Kahle20] — 발굴 깔때기 3대 계보 완성 (Sendek=ML / Xiao=게이트 / Kahle=물리 MD)**: **Sendek17** = MP 12,831 → 물리 4게이트 317 → **ML 분류기**(5-특징 LR) → 21 — 전도도를 *데이터*로 게이트화 / **Xiao19** = 104,082 → 물리 6게이트(hull·grand-potential ESW·ΔE_rxt·CI-NEB) → 3 — 전도도를 *정적 프록시*로 / **Kahle20** = ICSD+COD 4,963 → 절연체 1,016 → **pinball-MD 796(7.6 μs) → FPMD 132(45 ns)** → 신규 5+40 — 셋 중 유일하게 전도도를 **동역학 그 자체(D)**로 게이트화(대가 = surrogate 근사·부분점유 제외). 상호 검증 고리: Kahle이 [Sendek 2019 CM] 무작위 14% 발생률로 자기 수확(84/796)의 통계 정합을 직접 계산했고, **Li₂B₂S₅(perthioborate)는 Sendek·Kahle 이중 지목** 후보. **우리 cascade의 위치문(발표용)**: "발굴(discovery) 3축 — ML(Sendek)·정적 게이트(Xiao)·동역학(Kahle) — 이 모두 *무질서 물질*을 못 다뤘다(Sendek=DB 커버리지 천장·Xiao=코팅 대상·**Kahle=부분점유 입구 제외로 LPSCl/Br 진입 불가**). 우리는 그 사각지대인 *무질서 host(argyrodite)의 within-host 개질*에 있고, disorder-ensemble이 세 깔때기가 공유한 '질서 단일 배열' 한계를 정면으로 메운다."
> - **🔬 [Kahle20] SI 실물 검증(2026-08-03)에서 나온 인용 가능 신규 정량 2건** (둘 다 **논문 자체는 언급하지 않는 값 — "our reading of their SI"로 귀속할 것**): ① **비전도/전도 경계의 실제 갭** — 그룹 C 70종의 1000 K D_Li 최대가 **3.9e-7 cm²/s**(LiNbO₃, Fig S121)이고 70종 전부 1e-6 미만인 반면, 그룹 B 1000 K 최저는 **1.2e-6**(LiB(SO₄)₂, Fig S51) → **약 3배의 빈 구간**이 존재 = "분류 커트라인이 임의가 아니라 데이터에 난 틈"이라는 이 스크리닝 최강의 방어 수치(단 T_sim 43.6–726 ps 편차 유보는 유효). ② **질서 argyrodite 무확산의 결정적 지문** — Li₆PS₅I(Fig S14) D_Li가 **1000 K 5.8e-6 ≈ 750 K 5.9e-6**으로 **온도 역전**, 즉 아레니우스가 성립 안 함 → 저자가 "해상 불가"라 부른 것은 통계 부족이 아니라 **애초에 확산이 아닌 신호를 D로 환산한 것**. 우리 β=dlogMSD/dlogt 게이트가 잡는 바로 그 상황이며, [Klerk] all-4a intercage 0 · [Kraft] σ(I)~1e-6 · comp5 관찰과 함께 **4자 정합**을 수치로 완성한다.

| **B① 분해산물(SEI/CEI)의 anodic 한계 — Li-binary 서열** | (판정 아님 — 산물 축 기준선) | **[Zhu15]** Fig 2a **픽셀 정량 재독(2026-08-03 실물 재검증, ±0.02 V)**: 모든 Li-binary가 **0 V부터 안정**(Li 금속측) + 산화 상단 **LiF 6.38 > LiCl 4.21 > Li₂O 2.90(dashed 3.32) > LiI 2.46 > Li₂S 2.00 > Li₃P 0.85 > Li₃N 0.45 V**. ⚠ **LPSCl 계에서 Cl이 PCl₃로 빠지는 2.88 V는 P₂S₅/S 공존 화학**이지 LiCl 자체 한계(4.21)가 아님 | 우리 `sei_products` gap 분류(전자절연 판정)의 **열역학 짝** — 아직 우리 hull로 재산출 안 함(할 일). **🔑 우리 서사에 쓰는 방식**: "LiCl-SEI/CEI는 **4.2 V까지 산화 안정 + 0 V까지 환원 안정**(MP-2015 hull) → Cl은 양끝 모두에서 **무해한 종단 산물**" = E축 LiCl-SEI([Lu]/[Liu]/[Li25])와 B③ Cl-rich 방어를 **하나의 열역학 문장**으로 묶는 근거. ⚠ MP-2015 값이라 우리 MP-2026 hull 재계산·병기 필요(§10b의 세대 감도 규율 그대로 적용). **(2026-08-03 SI 실물 검증 후 보강)** 같은 캘리브레이션이 SI 실물값을 Δ0.01 V로 맞혔고(LPSCl dashed 2.89↔SI 2.88 · Li₇P₂S₈I 2.48↔SI 2.47 · 코팅 5종 ±0.03), 열화학 교차검증(−ΔH_f/n_LiF: LiF 6.39 · LiCl 4.24)도 통과 → **Li-binary 서열은 SI에 표가 없어도 ±0.02 V로 인용 가능** |
| **B① 할라이드 산화 서열 — *계 내부* Cl vs I (binary 단독값과 구분)** | **Cl 승 (+0.41 V)** | **[Zhu15] SI Table S2(f)·(g) 실물(2026-08-03)**: 같은 argyrodite-계열 프레임에서 **Li₆PS₅Cl은 2.88 V에서 Cl→PCl₃**, **Li₇P₂S₈I는 2.47 V에서 I→I₂**(둘 다 P₂S₅+S 공존 상태의 마지막 계단 = 완전 delithiation) | **우리 Cl-rich 서사에 직접 쓸 수 있는 유일한 "동일 프레임 할라이드 대조"**. ⚠ 두 값 모두 **계 내부(P–S 공존) 화학**이라 Li-binary 단독 서열(LiCl 4.21 > LiI 2.46, Δ1.75 V)과 **크기가 다름 — 인용 시 어느 축인지 반드시 명시**. 우리 modelc(Cl 증량)는 I 치환축이 없어 직접 대조 불가 → 문헌 인용으로만 |
| **B① ★ "argyrodite anodic = Li₂S anodic"이 *두 독립 hull에서 각각 성립*** | **무승부 → 관계의 hull-불변성 확보** | **[Rich16] Fig 1c·Fig 2 픽셀 정량(2026-08-03 본문 실물 재검증, ±0.03 V)**: Li₂S **2.32** ↔ Li₆PS₅Cl anodic **2.32**(동일 픽셀, mixing 확장 0.00 V) / **[Zhu15]**: Li₂S **2.00** ↔ LPSCl **2.01**(Δ0.01). 두 논문은 **데이터 소스가 다름**([Zhu15] 순수 MP-2015 DFT hull vs [Rich16] NIST-JANAF·Kubaschewski **실험 열화학 하이브리드**) — Li-binary 절대값은 **할라이드만 0.02 V 일치**(LiF 6.38/6.37·LiCl 4.21/4.23)하고 **Li₂S 2.00/2.32·LiI 2.46/2.80·Li₂O 2.90/3.10으로 Richards가 0.2–0.34 V 높다** | **🔑 우리 axis ① 문장의 격상 근거**: 절대 onset(우리 **2.256** / Rich **2.32** / Zhu **2.01**)은 hull 세대·소스에 0.3 V 흔들리지만, **"S²⁻가 창 상단을 pin한다"는 *관계*는 두 독립 소스에서 각각 재현**. → 원고에선 "관계는 소스-불변, 절대값은 소스-의존"을 **한 문단에 같이** 쓸 것. ✅ **미수행 액션(값싼 검산)**: 우리 MP-2026 hull에서 **Li₂S 단독 anodic limit**을 뽑아 **2.256 V와 일치하는지** 확인 → 일치 시 3번째 hull 재현으로 문장 확정. ⚠ 아직 안 했으므로 "3세대 불변"이라 쓰지 말 것. 또한 우리 2.256이 실험열화학 하이브리드(2.32)에 0.07 V까지 근접 = MP-2026 보정이 2015 순-DFT보다 실험쪽에 가깝다는 방증 |
| **B① 창 확장 = "최약 binary + mixing energy"의 정량 지도** | (기준선 — 판정 아님) | **[Rich16] Fig 2 픽셀 전표 37종(2026-08-03, digest §18d)**: 확장분(전해질 anodic − 해당 binary anodic) = **Li₆PS₅Cl·Li₂MgCl₄·Li₂ZnCl₄·Li₂CdCl₄·Li₃InBr₆·Li₂ZnBr₄·Li₂MgBr₄·LLZO 전부 0.00 V**(mixing 확장이 측정 한계 이하) / Li₃PS₄ +0.26·LGPS +0.09·Li₄SnS₄ +0.03 / **폴리음이온 대확장** LiTi₂(PO₄)₃ **+1.65**·LiGe₂(PO₄)₃ +1.36·LiNbO₃ +1.20·Li₃PO₄ +1.10·LiBH₄ +0.98 / **유일한 음수 = Li₂MnBr₄ −0.23 V**(Mn²⁺ 산화가 새 채널을 염) | **우리 cascade 두 규칙의 문헌 정량 배경**: (a) **폴리음이온 코팅이 창이 넓은 이유**가 +1.1~1.65 V로 수치화 — [Xiao19] 폴리음이온 산화물 필터(F5)의 열역학 근거. (b) **late-TM 회피**: Li₂MnBr₄만 창이 *줄어드는* 유일 사례 = 우리 Fe₂O₃/CoO/MnO collapse(0.004–0.039 V)와 같은 물리의 2016년 원형. (c) **제2 양이온 = 환원 불안정**도 수치화(binary는 cathodic 전부 0.00 V인데 Li₂CdCl₄ 2.20·Li₃InBr₆ 2.21·Li₂ZnCl₄ 2.08·LiAlCl₄ 1.70 V) → "σ 올리려 양이온 넣으면 음극측을 잃는다"의 표 근거 |
| **B③ 코팅 선택의 환원측 조건 — 양극 전용 vs 양방향** | **Li₃PO₄만 양방향** | **[Zhu15] SI Table S3 실물(2026-08-03)**: 환원 계단·산물 — **Li₃PO₄ 0.69 V 단 1계단 → Li₃P+Li₂O(둘 다 전자절연 Li-binary)**; LiNbO₃ 0.55 V→**Nb 금속**, LiTaO₃ 0.35 V→**Ta 금속**, Li₂SiO₃ 0.10 V→**Li₂₁Si₅ 합금**, Li₄Ti₅O₁₂ 0.018 V→**Ti 서브옥사이드** | **[Sundar]/[Cha] 코팅 스크린의 환원측 게이트로 그대로 쓸 판정**: "산화 상단(3.7–4.2 V)만 보고 코팅을 고르면 안 된다 — 음극/저SOC 노출 시 Nb·Ta·Ti·Si계는 금속·합금(=MCI)으로 가고 passivation이 꺼진다". 우리 `sei_products` gap 분류의 **코팅판 확장 항목**(아직 미산출 — 할 일) |
| **B③ 코팅 게이트에서 구속을 거는 쪽 = 양극이 아니라 황화물 SE** | **SE(LPSCl) 쪽이 지배** | **[Kim26HTS]** §9 + **Fig 2c 축 비대칭(2026-08-03 본문 실물)**: 265종 산점도의 y축 ΔE_rxn(NCM523) = −100…0 인데 x축 ΔE_rxn(LPSCl) = **−400…0**, 점들이 y≈0 선에 몰림. 본문도 *"many materials exhibited stable interfaces with the NCM523, a substantial fraction fail to maintain stability against LPSC"*. 대표값: Li₂TiO₃ 0/−60.1 · Li₃NbO₄ 0/−96.1 · Li₂CO₃ 0/−83.8 (meV/atom). **✅ SI 실물로 확정(2026-08-03 §14a)** — 근거 7행(Li₂TiO₃ 0/−60.12 · Li₃TaO₄ 0/−47.80 · Li₃NbO₄ 0/−96.12 · Li₂SO₄ 0/−99.22 · LiSrBO₃ 0/−95.69 · Li₂CO₃ 0/−83.80 · Li₃Na₅Ti₅O₁₄ 0/−96.10)이 Table S1 원표와 전량 일치 | **우리 M6는 양극(LiCoO₂/Li₀.₅CoO₂)만 계산**해 "89/94 통과·unique_kill 0 = vacuous"라 판정했다 → **게이트의 성질이 아니라 우리 축이 절반이었던 것**. `coating vs Li₆PS₅Cl` 축 추가 후 재판정(`open_items` T9) |
| **B③ ⚠ "계면 안정 코팅"으로 인용하면 과장 — 최종 후보가 8종 중 계면 꼴찌** | (인용 규율) | **[Kim26HTS]** Fig 3c + Table S1(2026-08-03 §13-N2): 최종 선택 **Li₃Sc₂(PO₄)₃ = −37.30**(NCM523, 8종 최악)/**−24.69**(LPSCl) = 합산 최악. **Li₃PO₄는 0/0**인데도 탈락. 결정타는 계면 열역학이 아니라 **Li 전도도**(γ상 0.2 mS/cm). 더욱이 ΔE_rxn −37.3 이 분해산물(Ni₃O₄·Sc₂O₃·Li₃PO₄)까지 명시하는데 같은 계면의 **298 K·500 ps MD는 "negligible reactivity"** — 논문이 정합성 논의를 하지 않는다. **🔑 SI 가 그 역설의 물리적 뒷면을 준다(§14c-4, Fig S4 실물)**: 1000 K·200 ps AIMD 에서 Li MSD 가 **Li₃Sc₂(PO₄)₃ ~175 Å² vs 2위 Li₃B₁₁O₁₈ ~8**(20배 이상 절벽), **Li₃PO₄ 는 최하위 ~0.3** — 계면이 0/0 인 물질이 전도체가 아니었던 것 | **닫힌계 ΔE_rxn 과 실온 MD 는 서로 다른 질문의 답**이다. 우리 M6(열역학)와 T3(MD)를 같은 문장에서 근거로 묶지 말 것. **인용 화법 교정**: "엄격 기준으로 8종을 골랐다"가 아니라 **"고전압·저반응 상위군에서 AIMD 로 유일한 전도체를 찾았다"** |
| **B③ ★ 깔때기 문턱은 *부등호 방향과 유효자리*까지 적어야 재현된다 — 컷 민감도 동반보고 규율** | (방법 규율 — 우위 판정 아님) | **[Kim26HTS]** SI Table S1 88행 전수 재입력 후 **논문이 글로 적은 6단계 컷을 코드로 재적용**(2026-08-03 §14c-1·2·3, 우리 재현): 논문 문구 그대로 **`V_ox ≥ 4 V AND ΔE_rxn ≥ −50`** 을 걸면 최종 후보가 **8종이 아니라 9종**(추가 = **Li₄B₇ClO₁₂** mp-1222565, V_ox 가 표에 `4` 로만 인쇄·ΔE −21.62/0·gap 5.87) — **strict `> 4.00` 이라야 Table S2 8종과 정확히 일치**. 민감도(strict 기준): **ΔE −40/−50/−60 → 8/8/8**(생존자 최악 −37.3 ↔ 탈락자 최선 −62.1, 그 사이가 비어 robust) vs **V_ox 3.99/4.00/4.05 → 10/9/8**(**0.01 V 로 답이 바뀌는 칼끝**). Li₂NaPO₄ 는 **ΔE 0/0 인데 V_ox 3.99** 로 탈락 | 우리 `tools/cascade/` 게이트 문서·코드에서 **`>=` 와 `>` 를 같은 기호로 통일**하고 **컷별 민감도(±)를 게이트 보고서에 동반 출력**할 것. §10-3(컷 계층화 인용)의 **실행 조건**. 부수 소득: **Li₄B₇ClO₁₂ = 붕산염 + Cl** 로 우리 cascade 6위 B₂O₃ 축과 Cl-rich 축에 동시에 닿는 유일 후보(그들 8종의 붕산염 3종은 전부 Cl 없음) → 우리 풀에 넣어볼 가치 |
| **B③ 코팅 설계 열역학의 *원점* — ⚠ 액체 LIB·HF 축 (우리 황화물 SE 와 무대가 다르다)** | (계보 — 우위 판정 아님; **수치 이식 불가**) | **[Aykol14]** ⭐: 코팅을 **4속성**(HF 포획 −ΔH_s-HF · 부피 Ω_V · 무게 Ω_G · **가역 Li 손실**)으로 형식화하고 이원 산화물/불화물 **81쌍** 전수 DFT. 게이트 `0.30 ≤ −ΔH_s-HF ≤ 1.50 eV HF⁻¹`(하한 = **양극 자신의 HF 공격 발열** LiCoO₂/LiNiO₂ −0.32·LiFePO₄ −0.28·LiMn₂O₄ −0.29·**LiMnO₂ −0.65**, Table 2 GCLP 산물) + `V(MₓF) ≤ 3.0 V` → **81→40→27**. 소환값(eV HF⁻¹): Al₂O₃ **0.76**·MgO 1.15·ZrO₂ 0.59·TiO₂ 0.41·Sc₂O₃ 0.89·Y₂O₃ 1.05·**B₂O₃ 0.28**·SiO₂ 0.34·P₂O₅ 0.25·Li₂O 1.70 | ⛔ **우리 값과 같은 표에 놓지 않는다** — ① **eV per HF**(공격분자 1몰당) vs 우리 **eV/atom**·**V vs Li** ⇒ 환산 불가, ② **OQMD** hull(우리는 MP), ③ **닫힌계 0 K 반응엔탈피**(우리는 μ_Li 개방 grand potential), ④ **우리 계엔 HF 가 없다**. 🔑 가져오는 것은 **문법 하나**: *"코팅은 반응 산물이 **상온 안정 고체**일 때만 보호가 된다"* — SiO₂→SiF₄·B₂O₃→BF₃·P₂O₅→PF₅ **전부 기체**라 실험에서 실패했고(Kim 2003 서열 + Cho 2003 P₂O₅ **악화**), Nb₂O₅/Ta₂O₅ 는 MF₅ **융점<100 °C** 로 탈락. ⚠ **"Aykol 도 B₂O₃ 를 버렸다"를 우리 B₂O₃ 논거로 쓰면 안 된다** — 그 사유(BF₃ 기체)가 우리 계에 존재하지 않는다 (digest §7d) |
| **B③ ★★ 우리 계면 파이프라인에 *없는* 게이트 3개 — 앞의 둘은 추가 계산 0 으로 붙는다** | **[Aykol14]+[Aykol16] 우위(방법)** | **[Aykol14]** §3.3.2·Fig. 4·본문 3.3.3: ① **생성물 물리상태 게이트**(기체·저융점 산물이면 보호막이 안 된다) ② **가역 Li 손실 게이트**(`V(MₓF) ≤ 방전 하한 3.0 V` — **81 중 31종(38 %)이 여기서 탈락**; 본 digest 가 Table S1 로 복원한 수). 그리고 **게이트는 *진화 후* 상에 건다** — 불화물 전환전압이 모(母)산화물보다 **1.0–1.5 V 높다**(복원 평균 1.16·중앙값 1.30 V) | ① 우리 `interface_reactivity`(pymatgen hull, `use_hull_energy=True`)는 **모든 상을 고체로 취급**한다. comp1/LiCoO₂ 산물 `Co₉S₈+Li₃PO₄+Li₂S+LiCl+Li₂SO₄`(min ΔE **−0.3227 eV/atom**)는 전부 고체라 통과하지만, **[Zuo] DEMS 는 SO₂ 기체를 실측**한다 ⇒ **hull 이 못 보는 기체 채널이 실재** → 도판트 표에 *기체 산물 표시 열* 필요. ② 우리는 ESW 환원 한계(**1.242 V**)만 보고 **계면상이 Li 를 얼마나 삼키는지**는 안 센다 — 우리 반응식에 이미 들어 있다(`0.5155 Li₂S + 0.2577 Li₃PO₄ …`) ⇒ **Li 소모 몰수/반응원자 열은 파싱만으로 추가 가능**. ③ **[Aykol16] 본문 Eq 5–6 이 2014 를 수정**: 코팅을 **양극과 먼저 평형**시키면 `LiCoO₂+αAl₂O₃→(1−4α)LiCoO₂+2αLiAlO₂+αCo₃O₄+αLi₂CoO₃` 이 되고, 그 혼합물에 HF 를 때리면 **LiAlO₂ 는 안 줄고 LiCoO₂ 만 소모** ⇒ *"완전 반응한 Al₂O₃ 코팅은 더 이상 HF-scavenger 가 아니다"*(저자 표현 **counter-intuitive**). 우리 번역: comp1/LCO 평형 산물 중 **Li₃PO₄·LiCl 은 절연**·**Co₉S₈ 은 전자전도체** — *"이 CEI 가 스스로 passivate 하나, 전자경로를 깔아 분해를 잇나"* 는 **아직 우리 표에 없는 질문**이다([Xiao19] SI 의 *기존 3원 코팅 분해산물이 전자전도성 TM 황화물* 행과 동일 질문). (digest §7c) |
| **B① 방법 계보 판정 — [Aykol14] 는 우리 grand-potential ESW 의 조상이 *아니다*** | (계보 규율 — 우위 아님) | **[Aykol14]** vs **[Zhu15]/[Xiao19]**: Aykol 은 **μ 를 열지 않고**(닫힌계), **산물을 가정**하며(코팅 반응 Eq 4·7·8·15; GCLP 는 **양극+HF 반응에만**), 전압은 **평균 전환전압** `V = −ΔH/ne`(중간상 무시) 다. "안정 구간"도 **구간이 아니라 문턱 2개**(−ΔH 상·하한 + V ≤ 3.0 V) | 우리 산화 onset **2.256 V**(comp1·modelc, LiS₄ 제외)는 `get_element_profile(Li)` = **μ_Li 스캔의 개시 전압**이고 원전은 Mo/Ong/Ceder 2012 → **[Zhu15]** → HT 화 **[Xiao19]**. ⇒ **Aykol 은 그 계보에 없다**(같은 科, 다른 屬). 접점은 둘뿐: ⓐ `V = −ΔH/ne` 변환의 공통 조상 Aydinol/Ceder 1997, ⓑ **U 값 계보가 같다**(Wang/Maxisch/Ceder 2006 — 우리 MP GGA+U 와 동일 세트, 단 Aykol 은 시험 후 **미채택**: MAE 0.157→0.149 로 개선폭이 실험 CSU 0.070 의 1/10). ⚠ **평균 전환전압 ≤ 개시 전압**이므로 그들 Li-손실 게이트는 체계적으로 **관대**하다 (digest §6b·§10-2) |
| **B① ★★ 그 판정의 *재판정* — [Aykol16] 에서 환원축은 뒤집히고 산화축은 강화된다** | (계보 규율 — 우위 아님) | **[Aykol16]** Eq 1–3 · `Fig. 2b` 실독: #1 의 네 근거 중 **둘이 무효화**된다 — ① 산물을 **더 이상 가정하지 않는다**(`[…]_min` = **hull 최소화**, 우리 `use_hull_energy=True` 와 같은 원리) ② 전압이 **평균이 아니라 개시**다(`E_d` = 희박 δLi 삽입 시 hull **첫 상영역의 최고 계단**; `Fig. 2b` figure-read ≈0.75 V ↔ CSV Li₂TiO₃ **0.748 V**). 저자 스스로 *"the Li chemical potential will be at its lowest value among all possible values along the composition path"* 라고 **μ_Li 로 설명**한다 | 🟢 **환원축**: **`E_d` 는 우리 `reduction_limit_V` 1.242 V 와 *같은 종류의 양*이다**(hull 첫 상영역 리튬화 개시). ⇒ 원고에서 *"우리 ESW 는 문헌 코팅 스크리닝과 같은 틀"* 이라고 쓸 때 **환원측에 한해** [Aykol16] 을 같이 인용할 수 있다. 🔴 **산화축**: **`E_c` 는 우리 2.256 V 와 대응물이 *아니다*** — 고체의 탈리튬 분해가 아니라 **양이온이 액체 전해질로 용출**되는 전위이고, 뼈대가 **NBS 수용액 표준산화전위 + 활동도 10⁻⁶ Nernst**(DFT 아님)다. **우리 계엔 용매가 없다** ⇒ **2.256 V 의 직계는 여전히 [Zhu15]/[Xiao19]**. ⚠ **값 비교는 환원축에서도 금지**(OQMD≠MP, ΔG(298 K)≠0 K, 대상물질 다름) — **정의 대조까지만** (digest §6b·§7b·§7e) |
| **B③ ★★ "안정"의 조작적 정의가 *한 논문 안에서도* 갈린다 — 절대 문턱 vs 양극 상대 문턱** | (규율 — 우위 아님) | **[Aykol16]**: 일반 MOOP 는 **절대 문턱** `E_d < 3 V & −E_c > 3.5 V`(`Fig. 1`). 그런데 **양극을 화학공간에 넣은 `Table 2` 분석은 기준이 바뀐다** — 양극 **자신의 E_c**(LiCoO₂ **−3.152 V**)와 비교하고 **±0.12 V 버퍼**(활동도 2자릿수 ⇒ `0.0592/z·log K`)를 준다. **본 digest 실측: `Table 2` 의 LiCoO₂ 최적 코팅이 *전원* 일반 게이트 `−E_c>3.5 V` 를 탈락**(Li₂CaSiO₄ 3.362·CaIn₂O₄ 3.361·SrHClO 3.465·SrHfO₃ 3.324·SrZrO₃ 3.185·SrLi₂SiO₄ 3.352). 저자도 두 목록이 *"not necessarily similar materials"* 라고 인정 | ⚠ **인용 규율**: [Aykol16] 의 추천 물질을 쓸 때 **`Fig. 5`(절대 문턱) 산물인지 `Table 2`(양극 상대) 산물인지 반드시 명시**한다. 우리 축 번역 — **보호자는 피보호자보다 더 반응성이어야 한다**: `G_s-HF(coating) < G_s-HF(cathode)`. LiCoO₂ **−0.87** ⇒ 후보의 **30 %**만 자격 / LiMn₂O₄ **−0.49** ⇒ **51 %** (본 digest 재현 **69.6 %/49.1 %** = 본문 "70 %/50 %" 정확 일치). ⇒ 🔑 **우리 `interface_reactivity` 표에 `host` 기준선(comp1/LCO **−0.3227 eV/atom**) 열을 그어 *"host 보다 나아졌나"* 를 판정으로 삼는다**(추가 계산 0) (digest §3e·§7c②) |
| **B③ ⚠ [Aykol16] 이 [Aykol14] 의 *산물 물리상태 게이트*를 잃어버렸다 — 우리 공백의 근거가 하나 늘었다** | **[Aykol14] 우위(방법)** | **[Aykol14]** 는 SiF₄·BF₃·PF₅ **기체**와 MF₅ **저융점**을 **손으로** 걸러냈다. **[Aykol16]** 은 전면 자동화하면서 **이 검사를 안 넣었다** — 그 결과 **휘발성 옥시할라이드가 top-30 에 앉아 있다**(HF-barrier: `WCl₂O₂` 2위·`WBr₄O` 11위·`MoCl₄O` 14위·`MoBr₂O₂` 19위·`NbCl₃O` 23위 / 물리장벽: `WCl₂O₂` 8위). 게다가 **SiO₂·B₂O₃·P₂O₅ 는 후보 CSV 에 아예 없다**(금속 함유가 암묵 조건) ⇒ *"문제가 없다"* 가 아니라 **"문제가 안 보인다"** | 우리 `interface_reactivity`(pymatgen hull)도 **모든 상을 고체로 취급**한다. comp1/LCO 산물 `Co₉S₈+Li₃PO₄+Li₂S+LiCl+Li₂SO₄` 는 전부 고체라 통과하지만 **[Zuo] DEMS 는 SO₂ 기체를 실측**한다 ⇒ **hull 이 못 보는 기체 채널이 실재**. **두 세대(2014→2016)에서 이 게이트가 사라지는 것을 확인했으므로, 우리 도펀트 표의 *기체·저융점 산물 표시 열* 은 "있으면 좋은 것"이 아니라 *계보가 반복해서 빠뜨린 자리*다** (digest §10-4) |
| **B① ★★★ 계보 확정 — [Nolan19] 는 우리 *두 양을 둘 다* 갖고 있다 (계보 8편 중 처음)** | (계보 판정 — 우위 아님) | **[Nolan19]**: ① 헤드라인 **E_d** = 유사이원 상호분해에너지 최솟값(끝점 준안정성 제거, **eV/atom**, 음수=반응) — SI "Computation methods" 4단 식 ② **anodic/cathodic limit** = `Fig. S7`·`Fig. S8`·`Fig. S9`·`Fig. S10` 의 축, **vs Li/Li⁺** | 🟢 **E_d ↔ 우리 `interface_reactivity`** = **같은 양 + 같은 구현**(pymatgen `InterfacialReactivity(use_hull_energy=True)` 의 `get_kinks()` 최솟값이 SI 식 그대로다 — 정규화 1원자/f.u.·부호·DB(MP) 전부 일치). 🟢 **anodic limit ↔ 우리 `2.256 V`** = 같은 grand-potential·같은 기준전극. ⚠ **그러나 이 논문은 anodic limit 의 정의를 적지 않는다** — SI 참고문헌 3개([Zhu16]·[Zhu15]·[Jain13])로 **인용 승계**하고 값도 XLSX 에 없다(boxplot **figure-read** 뿐). ⇒ **판정: 우리 2.256 V 의 직계 원전은 여전히 [Zhu15]→Mo/Ong/Ceder 2012 이고 [Nolan19] 는 그 계보의 *형제 적용*이다.** 반면 **`interface_reactivity` 의 귀속이 세 층으로 정리된다 — 형식화 [Rich16] → *mutual*(끝점 준안정성 제거) 판 [Zhu16] → **양극 SOC 두 상태 전수 적용 [Nolan19]**.** 우리는 `use_hull_energy=True` 를 쓰므로 **[Zhu16]/[Nolan19] 판**이다(기존 [Rich16] 등재는 유효 — 층이 다르다). **[Aykol] 두 편 "다른 양" 판정은 유지**되고, 계보 가지에 [Nolan19] 가 추가될 뿐이다 |
| **B③ ★★ "안정"의 조작적 정의 — [Nolan19] 는 *전압도 구간도 아닌* 스칼라 위의 불리언** | (규율 — 우위 아님) | **[Nolan19]** SI: `C_pb(x)=x·C_cat+(1−x)·C_contact`(둘 다 **1원자/f.u. 정규화**) → `E_pb(x)` 선형보간 → `ΔE_D(x)=E_eq−E_pb` → **끝점 준안정성 제거** `ΔE_D,mutual` → **`E_d = min_x`**. **"안정" ⇔ `E_d = 0`**, 그것도 **양극의 리튬화·탈리튬화 두 이산 상태 각각에서**. μ_Li 연속 스캔 아님. 기준전극은 E_d 에 **없다**(에너지지 전압이 아니다). DB = **Materials Project**(⚠ [Aykol] 의 OQMD 아님). 0 K·PV 무시 | ⛔ **[Aykol16] 의 `E_d`(단위 **V**, 리튬화 개시전압)와 기호만 같고 단위부터 다르다** — 우리 표에서 `E_d^{Nolan}`/`E_d^{Aykol}` 로 구별해 쓴다. 우리 4개 양의 자리: `oxidation_limit 2.256 V`(grand-potential onset) · `reduction_limit 1.242 V` · `ocv 1.717 V` · `interface_reactivity −0.3227 eV/atom` ⇒ **마지막 하나만** [Nolan19] 의 헤드라인과 같은 양 |
| **B② ⛔ 우리 LPSCl/LPSOCl 은 [Nolan19] 의 *목록에 없다* — 황화물 0·염화물 0** | (경계 규율 — 우위 아님) | **[Nolan19]** Ed 데이터셋 **236종에 황화물 0종·염화물 0종·티오인산염 0종**(S 함유는 `Li₂SO₄`·`Li₂S₂O₇` 산소산염뿐). 염화물은 `Fig. S7`·`Fig. S8` 의 *chlorides* boxplot 에만 나오고 **Ed 도 데이터도 없다** — 출처는 자매논문 Wang/Bai/**Nolan**/Liu/Gong/Sun/Mo *Angew* **2019**, 58, 8039 (ref 63) | 우리 계를 이 지도에 얹는 유일하게 정당한 축 = **anodic limit**. `figure-read ≈`: oxides 중앙 **3.7**(수염 최저 **2.45**) · phosphates **4.6** · **chlorides 4.35** · fluorides **6.7** V. ⇒ **우리 2.256 V 는 그들 산화물 분포의 최저 수염보다도 아래**다. ⛔ *chlorides 4.35 V* 를 우리 값 옆에 놓지 말 것 — **Li–M–Cl 할라이드**(Li₃YCl₆ 계열)이고 우리 onset 은 **S²⁻ 가 pin** 한다. ⇒ 정직한 서술: *"[Nolan19] 는 우리 SE 를 옹호하는 근거가 아니라 **우리가 넘어야 할 기준선**"* |
| **B② 🔑🔑 우리 LPSCl\|LiCoO₂ 계면 *산물* 2종이 [Nolan19] 목록의 1·2위다 — CEI 자기부동태화 서사의 문헌 다리** | **정합(교차 관찰)** | **[Nolan19]** Sup2 XLSX 전수(본 digest §12b): **8 양극상태 전부 `E_d=0` 인 물질은 236종 중 단 2종 — `Li₂SO₄`·`BeO`(0.85 %)**. 7/8 은 5종(`CsLi(B₃O₅)₂`·`LiNO₃`·`Li₂SeO₄`·`ZrO₂`·`HfO₂`), **`Li₃PO₄` 는 6/8**(MNO −11.5·CP −1.1 meV/atom) | 우리 `interface_reactivity_results.json` 최발열 반응 산물 = `Co₉S₈ + **Li₂SO₄** + **Li₃PO₄** + Li₂S + LiCl` ⇒ **산화물 성분 2종이 정확히 그들 1·2위**. ⚠ **`Li₂S`·`LiCl`·`Co₉S₈` 는 그들 축에서 미평가** — 그러므로 *"산화물 성분에 한해"* 라고 범위를 박고 쓴다. ⚠ 이건 **우리 계산 + 그들 데이터의 교차 관찰**이지 [Nolan19] 의 주장이 아니다 |
| **B② 🔑 우리 계 물질 직격 — `B₂O₃`·`Li₂O` 의 양극 상호반응 (⛔ 우리 db 절대값과 같은 표 금지)** | (문헌 소환값) | **[Nolan19]** Sup2 XLSX (meV/atom): **`B₂O₃`** LCO **−56.8** / L₀.₅CO −16.0 / **LNO −85.9** / L₀.₅NO −58.1 / LMNO −10.9 / **MNO 0** / LCP −16.5 / CP −16.3 · **`Li₂O`** MNO **−218.9** / **CP −334.4** · `Al₂O₃` LCO −19.9·CP −82.6 · `LiNbO₃` LNO −16.6·CP −64.9 · `LiTaO₃` LNO −12.7·CP −68.8 · `LiTi₂(PO₄)₃` LCO −51.4·LNO −86.1 | **`B₂O₃` 읽기**: 우리 `+B₂O₃` 계는 **Ni-rich 층상 쪽에서 위험**(−86)하고 **고전압 인산염·탈리튬 스피넬 쪽에서는 무난**(0…−16). 우리 `b2o3_esw.json` 의 산화 **2.03 V** 와는 **다른 축**(자기분해 ↔ 양극 상호반응)이다. **`Li₂O` 읽기**: 탈리튬 양극과 데이터셋 최악급 ⇒ 음극쪽 환원산물이 양극쪽으로 넘어가면 안 된다는 열역학 근거. ⛔ MP hull **세대가 다르다**(2019 ↔ 우리 2026 pinned `GGA_GGA+U`) — **정의 대조·방향까지만** |
| **B③ ★★ [Nolan19] 이 지목한 우리 공백 2건 — 둘 다 추가 DFT 0~1 로 메워진다** | **[Nolan19] 우위(방법)** | **[Nolan19]** 전 데이터의 결론: **탈리튬(충전) 상태가 병목**. Ed=0 비율 LCO **81 %** → L₀.₅CO 54 % → **MNO 3 %** → CP 8 %(Li 삼원 산화물). 그리고 `Fig. S3` 로 **LNO ≈ NMC111 ≈ NCA** 프록시를 별도 검증 | **① 우리는 `LiCoO₂` 한 상태만 봤다** — `tools/oxidation/interface_reactivity.py --contacts LiCoO2 Li0.5CoO2 CoO2 C` 한 줄이면 충전상태 열이 생긴다. **② `oxidation_stability.json` 의 caveat *"LiCoO₂ proxy (experiment may use NCM)"* 의 방향이 확정됐다 — LCO 프록시는 반응성을 *과소평가*한다**(같은 접촉물질에 대해 LNO 의 \|E_d\| 가 일관되게 크다). caveat 문구를 강화할 근거 |
| **B③ ⚠ [Nolan19] 도 [Aykol14] 의 *산물 물리상태 게이트*를 복원하지 않았다 (계보 카드 물음의 답)** | **[Aykol14] 우위(방법)** | **[Nolan19]** 상평형 문자열에 **`O₂` 가 고체와 같은 자격**으로 빈번히 등장한다(예 `LiNiO₂+B₂O₃ → O₂, Li₃B₇O₁₂, Ni₃BO₅`; `LiTi₂(PO₄)₃+LiNiO₂ → O₂, TiO₂, Li₃PO₄, Ni₃O₄`). 0 K·PV 무시 | 계보 카드가 *"#4–#7(Mo 라인)이 이 게이트를 복원하는지 확인할 것"* 이라고 물었다 → **#4 의 답은 "복원하지 않았다"**. ⇒ 우리 `interface_reactivity` 산물 파싱에 붙일 열이 이제 **셋**이다: ⓐ 기체·저융점 상 표시 ⓑ Li 소모 몰수 ⓒ **양극 유래 상이 산물에 있는가**(코팅이 양극을 탈리튬시키는가 — [Nolan19] Eq 1 의 `Co₃O₄`, Eq 4 의 암염 `NiO`) |
| **B③ ⚠ "산화한계가 높으면 양극과 안정" 은 [Nolan19] 자기 그림에 반례가 있다 — 범위를 붙여야 쓴다** | (비판 — 우위 아님) | **[Nolan19]** 결론 문단은 일반 원리처럼 쓴다(*탈리튬 양극 ≥4.5 V > 대부분 산화물 산화한계 3.5–4 V*). 근거는 **`Fig. S10`(LiCoPO₄ 상대·Li–M–O 만·M 4족 ≈14점)**: anodic **3.9–4.05 V** 군 `E_d ≈ −0.002…−0.023` ↔ **2.5–3.0 V** 군 `−0.08…−0.118` (**figure-read**) | 그런데 **`Fig. S9b`**(전 계군·LiCoO₂ 상대)에서 **가장 짙은 = 가장 반응성 큰 점이 anodic 6.5–7.4 V 구간(불화물)에 몰려 있다.** ⇒ 상관은 **산화물 안에서, 탈리튬 고전압 양극 상대일 때만** 성립한다. ⛔ 우리가 *"우리 onset 2.256 V 가 낮아서 계면반응이 크다"* 를 이 논거로 뒷받침할 때 **이 범위 조건을 반드시 붙인다**(그리고 그건 외삽이지 그들의 계산이 아니다) |
| **B③ ⚠ [Nolan19] 의 공개 데이터가 논문 산출물의 *부분집합*이다 — `Table S1` 40종 중 8종이 XLSX 에 없다** | (재현성 비판) | **[Nolan19]** `Table S1` 1열(LCO&L₀.₅CO 안정) **40종** ↔ Sup2 XLSX 재현 **32종**. 없는 8종 = `LiClO₄·Li₅IO₆·LiAuO₂·Li₂PdO₃·Li₂PtO₃·LiReO₄·LiCuO₂·LiBiO₃`. `Fig. S1` 의 y 범위는 **−0.44 eV/atom** 까지 가는데 XLSX 최솟값은 **−0.29** — 같은 이야기. 또한 **`Fig. 2` 전이금속 패널 행 라벨 ↔ XLSX 물질이 3종 맞바꿈**(그림 `Li₂NiO₃·Li₂PdO₃·LiAgO₂` ↔ XLSX `Li₂CuO₂·Li₅FeO₄·LiFeO₂`; 700 dpi 확대 판독). 이 논문은 **`Fig. 4` 라벨 오류 정정본 전력**(2019-09-23)이 있다 | ⛔ 그 8종을 **검증값으로 인용 금지**. ⛔ `Fig. 2` 의 **색에서 값을 읽지 말 것**(−80 meV/atom 근처 포화) — **XLSX 를 쓴다**. ✅ 반대로 **본문이 인쇄한 7개 값은 XLSX 와 소수점까지 일치**했다(본 digest §12a) — 문제는 값이 아니라 **범위**다. ⚠ MP 세대·functional·U·k-mesh 가 **전부 미기재** → 원리적 재계산 불가. **우리 pinned 파이프라인이 이 점에서는 낫다** |
| **B③ ★ Li 함량 규칙의 정량화 — SOC 로 상관 *부호가 뒤집힌다*** | (문헌 재분석 — 우리 소득) | **[Nolan19]** `Fig. S1` 은 이것을 색으로만 보여준다. 본 digest 가 XLSX 196종으로 Pearson r 계산: **LiCoO₂ +0.32 · LiNiO₂ +0.37**(Li 많을수록 **덜** 반응) ↔ **MNO −0.60 · CoPO₄ −0.61**(Li 많을수록 **더** 반응) | 물리: 리튬화 양극은 **Li 를 뺏기고**(저-Li 접촉물질이 위험), 탈리튬 양극은 **Li 를 뽑아간다**(고-Li 접촉물질이 위험). ⇒ *"단일 코팅으로 양 SOC 를 다 만족시키기 어렵다"* 의 수치 근거. 우리 cascade 후보 필터에 **접촉물질 Li 분율**을 SOC 별로 반대 방향 가중하는 근거가 된다 |
| **B① ★★★ 전압축 계보 — [Nolan21] 이 #4 가 생략한 *식*을 인쇄한다 (우리 2.256 V 의 정의가 이 계보 안에 처음 활자로)** | (계보 판정 — 우위 아님) | **[Nolan21]** Methods: **식 (5) `μ_Li(φ) = μ⁰_Li − eφ`**(φ 는 **Li 금속 기준**) · **식 (6) `E_D^open(C,φ) = E_eq(C,μ_Li) − E(C) − Δn_Li·μ_Li(φ)`** · 식 (7) mutual 개방계판. ⛔ 그래도 *"anodic limit ≡ E_D^open 이 0 을 벗어나는 φ"* 라는 **문장은 없고**, 인가 φ 는 **3 V·5 V 두 점뿐**(연속 스캔 아님) | 우리 `constrained_esw_cl_scan`(ox **2.256** / red **1.242 V**)은 `get_element_profile(Li)` = **같은 식의 연속 스캔**이고 기준도 같다(vs Li/Li⁺). ⇒ 계보 정리: **형식화 Mo/Ong/Ceder 2012 → [Zhu15] 값·창 → [Xiao19] HT 게이트화 → [Nolan19] 그림 축뿐 → [Nolan21] *식 인쇄***. **직계 원전은 여전히 [Zhu15]** 지만, 원고에서 *"우리 onset 은 코팅 문헌 계보와 같은 틀"* 이라고 쓸 때 **가리킬 활자가 생겼다** |
| **B① ★★ 그 식의 *수치*도 있다 — 다만 본문이 아니라 XLSX 열이다 (89종 ESW 한계표)** | (문헌 소환값 · ⛔ 우리 값과 같은 표 금지) | **[Nolan21]** `Sup2 XLSX` 의 `ternary-oxides_*` 시트에 **`cathodic limit`·`anodic limit` 열**이 89종 전부 있다(단위 **μ_Li eV**, `φ = −μ_Li/e`). 본문·SI 어디에도 설명이 없다. 본 digest 검증 3단: ① `LiCoO₂` −1.82199/−3.64086 → **1.82–3.64 V** ② `Fig. S5` 막대 픽셀판독 −1.817/−3.651 = **1 px 이내 일치** ③ **`Li₃PO₄` 0.69–4.20 V 가 [Zhu15] 인쇄값 0.68–4.21 V 재현** | 소환값(V): **`Li₂SO₄` 1.57–4.66** · **`Li₃PO₄` 0.69–4.20** · `Li₂CO₃` 1.27–4.10 · `LiAlO₂` 0.22–3.77 · **`Li₂ZrO₃` 0.34–3.41** · `LiNbO₃` 1.74–3.87 · `Li₄P₂O₇` 2.30–4.29 · `LiPO₃` 2.43–5.02 · 89종 anodic **중앙값 3.57**(1.11–5.23). 🔑 **우리 작업거리 1건(추가 DFT 0)**: 우리 `tools/oxidation` 으로 `Li₃PO₄` 를 돌려 **0.69/4.20 이 나오는지** 보면 우리 파이프라인이 Mo 그룹 인쇄값을 재현하는지가 한 번에 갈린다 — **계보 8편 중 이 대조가 가능한 첫 편**([Nolan19] 은 값이 없었다) |
| **B③ ★★ 선정 규칙이 #4 에서 *완화*됐다 — 불리언 → 문턱, 그리고 "약간의 반응은 접착에 좋다"** | (규율 — 우위 아님) | **[Nolan21]** `Table 2` 기준 = **`\|E_d\| < 0.05 eV/atom`**(LLZO 와도 NMC·d-NMC 와도) + 금속열 원소별 등급(**Mg<0.003 · Zr<0.005 · Ti<0.03**) + 본문 *"a limited amount of minor reaction may be beneficial … strong chemical bonding"*(ref 68 Yoon Co-boride). 본 digest 집계: **Ed=0 3상태 전부 = 16/89(18 %) → \|Ed\|<0.05 = 53/89(60 %) = 3.3배** | ⇒ *"안정"* 의 조작적 정의가 **같은 저자·같은 기계에서 2년 만에 바뀐다.** 우리 cascade 문턱(`ΔE_rxt` 100 meV/atom, [Xiao19] 승계)을 인용할 때 **어느 세대의 문턱인지 명시**해야 한다. 그리고 *"약간의 반응 = 접착"* 은 우리 `interface_reactivity` 를 **0 이 최선**으로 읽던 관행에 대한 반론이다 — 다만 [Nolan21] 도 접착에너지를 계산하지는 않는다(주장뿐) |
| **B③ ⚠ 그 완화가 Li 전도체를 자르지는 않는다 — 대신 *전도도를 아예 안 본다* (함정의 종류가 다르다)** | **(비판 — 우위 아님)** | **[Nolan21]**: `Li₂ZrO₃`(Ed LLZO −0.0029 / NMC 0 / d-NMC −0.0165)·`LiAlO₂`(0/0/0) **둘 다 최종 후보로 생존** ⇒ **[Aykol16] 이 `−E_c > 3.5 V` 로 이 둘을 잘라버린 함정은 #5 에 없다**. ⚠ 그런데 `Table S4` 가 후보들의 **실측 σ 를 스스로 싣는다**: **`LiAlO₂` ≈10⁻¹⁵ · `γ-Li₃PO₄` 10⁻¹⁸ · `Li₂SnO₃` 3.1×10⁻¹² · 최고가 `Li₃BO₃-Li₂CO₃` 유리 7.6×10⁻⁷ S/cm**(⛔ 온도 혼재: Li₈ZrO₆ 454 K · LiNbO₃ 650 K · LiAlO₂ 는 *"Fig. 4 에서 외삽"*) | 🔑 **구조적 이유**: 두 제약(LLZO 와 안정 ⇒ μ_Li 높아야 / d-NMC 와 안정 ⇒ μ_Li 낮아야)이 후보를 **`Li₂O–MOₓ` 타이라인 위 닫힌껍질 광대역 산화물**로 몰고, 그게 곧 **Li⁺ 이동도가 낮은 물질군**이다 — **선택하는 성질과 원하는 성질이 반대 방향**이다. 논문 방어는 *"nm 두께면 된다"* 한 줄(목표 면저항·허용 두께·터널링 정량 **0**). ⇒ 우리 cascade 는 **전도도 축을 이미 갖고 있다** — 이 지점이 우리 쪽 우위이고, 문헌 인용 시 *"열역학 단일축 스크리닝"* 이라고 범위를 박아야 한다 |
| **B② 🔑🔑 우리 계면 산물 `Li₂SO₄`·`Li₃PO₄` 가 *두 번째* 독립 데이터셋에서도 최상위 — 그리고 창이 모체보다 2 V 넓다** | **정합(교차 관찰)** | **[Nolan21]** Sup2/Sup3 XLSX 전수(본 digest §12b): **LLZO·NMC 111·d-NMC 111 세 상태 전부 `E_d = 0` 인 Li 삼원 산화물은 89종 중 16종**(`Li₂CO₃`·`Li₂CrO₄`·`Li₂MnO₃`·`Li₂NiO₃`·**`Li₂SO₄`**·`Li₂SnO₃`·**`Li₃PO₄`**·`Li₃TaO₄`·`Li₃VO₄`·`Li₄WO₅`·`LiAlO₂`·`LiClO₄`·`LiCoO₂`·`LiGaO₂`·`LiIO₃`·`LiNO₃`) | 우리 `interface_reactivity_results.json` 최발열 산물 = `Co₉S₈ + **Li₂SO₄** + **Li₃PO₄** + Li₂S + LiCl`. [Nolan19](양극 8상태, SE 없음)에 이어 **전혀 다른 SE(가넷) 상대로도** 이 둘이 최상위다. 게다가 같은 XLSX 의 창이 **Li₃PO₄ 4.20 V · Li₂SO₄ 4.66 V** 로 **모체 SE(우리 2.256 V)보다 2 V 이상 높다** ⇒ *"계면에서 생기는 산화물 산물 자체가 모체 황화물보다 훨씬 넓은 창을 갖는다"* 의 문헌 다리가 **둘**이 됐다. ⚠ 그들 수치는 **정성 근거로만**(hull 세대·계 다름) |
| **B③ ★★ `Li₂ZrO₃` 가 계보 안에서 죽었다 살았다 한다 — "필터가 결론을 만든다"의 문헌 사례 (우리 계 직격)** | (규율 — 우위 아님) | **[Aykol16]** `−E_c>3.5 V` 로 **탈락** ↔ **[Nolan21]** `Table 2` Zr 행 최종열 **생존**(`ZrO₂`·`Li₆Zr₂O₇`·`Li₂ZrO₃`, 창 0.34–3.41 V) ↔ **[Lu24]**(계보 #9) 는 **바로 그 `Li₂ZrO₃` 를 `Li₆PS₅Cl`\|Ni90 계면에 실제로 코팅**해 계면 Ea **0.624 → 0.429 eV**(60.19 → 41.39 kJ/mol) | ⇒ 같은 물질이 **필터 설계에 따라 세 번 다르게 판정**된다. 우리 cascade 대조표에 `Li₂ZrO₃` 한 행을 놓고 **[Aykol16] ⛔ / [Nolan21] ✅ / [Lu24] 실험 ✅** 세 칸을 나란히 두면 *"게이트를 바꾸면 후보가 바뀐다"* 를 한 줄로 보인다. ⛔ [Lu24] 의 Ea 는 **EIS 계면 전하이동**이고 우리 0.180 eV 는 **벌크 확산** — 같은 표 금지 |
| **B③ ★ "갈등 상대는 양극이 아니라 *충전된* 양극" — 본문보다 한 단계 날카로운 정량 (본 digest 재분석)** | (문헌 재분석 — 우리 소득) | **[Nolan21]** 본문은 *"Li 많으면 LLZO 와 안정 / 적으면 NMC 와 안정"* 이라고 색으로만 말한다. 본 digest 가 XLSX 89종을 **LLZO 자신의 Li 분율 7/24 = 0.292** 로 갈랐다 — `E_d = 0` 비율: **Li-poor(n=46) LLZO 45 % · NMC 52 % · d-NMC 52 %** ↔ **Li-rich(n=43) LLZO 76 % · NMC 93 % · d-NMC 34 %** | ⇒ Li-rich 로 가면 **LLZO 와 45→76 %(좋아짐) · 리튬화 NMC 와 52→93 %(*더* 좋아짐) · 탈리튬 NMC 와 52→34 %(나빠짐)**. **갈등은 "양극" 이 아니라 "충전 상태의 양극" 하고만 생긴다.** ⚠ Pearson r 은 이 구조를 못 잡는다(LLZO +0.572 / NMC +0.291 / **d-NMC −0.002** — zero-inflated 분포 + 양쪽 꼬리가 모두 Li-poor). ⇒ 우리 스크리닝 보고에서도 **r 만 내지 말고 중앙값·통과비율을 같이 낸다** |
| **B③ ⚠ [Nolan21] 도 [Aykol14] 의 *산물 물리상태 게이트*를 복원하지 않았다 + 개방계 산물에 `Li` 금속이 인쇄된다** | **[Aykol14] 우위(방법)** | **[Nolan21]** `Fig. S9a`(**5 V**, Li-Nb-O vs LLZO) 산물 = `LaNbO₄, **Li**, O₂, ZrO₂` · `Table S2`(μ_Li −2.75 ~ −4 eV) 산물 = `… **Li**, Li₂NiO₃, Li₂O …` · `Table 1` `Li₀.₅CoO₂` 산물 = `**O₂**, La₂O₃, LiCoO₂, La₂Zr₂O₇` | 산화 조건에서 금속 Li 가 나올 수는 없다 — **개방계 Li 저장조의 표기**다(우리는 같은 자리를 `Li⁺ + e⁻` 로 쓴다). ⇒ ⛔ **그들의 산물 목록을 그대로 옮기면 물리적으로 틀린 문장이 된다.** 그리고 계보 카드가 #4 에 물었던 *"Mo 라인이 물리상태 게이트를 복원하나"* 의 답이 **#5 에서도 "아니오"** 다 — 우리 `interface_reactivity` 산물 파싱에 붙일 열(ⓐ 기체·저융점 표시 ⓑ Li 소모 몰수 ⓒ 저장조상 제외)의 근거가 셋으로 늘었다 |
| **B③ ⚠ 그림·본문·공개데이터가 어긋난다 7건 — 그중 3건은 인용할 때 실제로 걸린다** | (재현성 비판) | **[Nolan21]** 본 digest 실독/대조: ① **`Fig. 3` 오른쪽 주기율표 인셋 군번호가 전부 1씩 어긋남**(Zn 을 11 로 인쇄, 실제 **12**; B/Al/Ga 12→**13**, C/Si/Ge 13→**14**, N/P 14→**15**. 왼쪽 인셋 4/5/6 은 정확 — 4× 확대 확인) ② **본문 최종 원소 목록 21종에 `Zr` 누락**(`Table 2` 는 22행, Zr 최종열이 차 있다) ③ *"전압 걸면 LLZO-코팅이 나빠진다"* 에 **자기 반례**(`Fig. S9a` Nb₂O₅ −0.135→**−0.03** · LiNbO₃ −0.072→−0.047 로 **좋아진다**; 나빠지는 건 Li-rich `Li₈Nb₂O₉` 0→−0.057 뿐) ④ **`Fig. 1` 이 89종 중 67종만** 그리고 **빠진 22종 중 5종이 자기 최우수 16종**(`LiClO₄`·`LiIO₃`·`Li₂MnO₃`·`Li₂NiO₃`·`LiCoO₂`) — **숨은 필터 미기재**([Aykol16] `Fig. 1` 과 같은 패턴) ⑤ `Fig. 1` 열이 `NMC,3V` ↔ `d-NMC,5V` 로 **비대칭인데 캡션이 안 밝힘** ⑥ **Ta 오기 3건**(Sup3 에 `Li₄WO₅`(W 화합물)·`LaTaO₃`(Li 없음), `Table 2` 에 `La₃TaO₄`(존재하지 않는 상)) ⑦ *"LCO 가 LLZO 와 가장 안정"* 인데 리튬화 상태는 **LiCoO₂=LiNiO₂=LiMnO₂=0 동률** | ②는 **`Li₂ZrO₃` 를 놓치게 만든다**(우리 계 직격), ③은 그대로 인용하면 **틀린 일반화**, ⑥은 **Ta 계 결론 사용 금지** 사유. ✅ 공정: **그림 주석 ↔ XLSX 4/4 일치**(`Al₂O₃` −0.094 · `Nb₂O₅` −0.135 · Al 원소 −181 meV/atom · `Fig. S5` LiCoO₂ 1 px 이내) — [Nolan19] 의 `Table S1` 8종 결손 같은 문제는 **없다** |
| **B② ⛔ 가넷 무대다 — 우리 황화물과 *같은 기계·다른 계*. 이식 가능한 것은 문법 4개뿐** | (경계 규율 — 우위 아님) | **[Nolan21]** 실패 모드 = **LLZO 가 Li 를 *잃는다*** → `La₂Zr₂O₇` + `LaMO₃`/`La₂MnCoO₆` + 리튬화 TM 산화물. `Table 1`(본 digest 좌표 복원, meV/atom): LiCoO₂/LiNiO₂/LiMnO₂ **0** · Li₀.₅CoO₂ −21 · Li₀.₅NiO₂ −35 · LiMn₂O₄ −60 · MnO₂ −123 · **NMC111 −87→d-NMC111 −132** · 622 −63→−117 · 811 −38→−80. `Fig. S5` μ_Li 창(figure-read): **LLZO 0→3.17 V** vs **d-NMC111 3.50–4.02 V** = **겹치지 않는다** | 우리 LPSCl 실패 모드는 **S²⁻ 산화**(→ `Li₂SO₄`·`Li₃PO₄`·`Co₉S₈`·`LiCl`)이고 창은 **1.242–2.256 V** 로 위아래가 다 잘려 있다(가넷은 음극쪽이 공짜). 공정도 다르다(가넷 600–800 °C 동시소결 ↔ 황화물 냉간가압) · 환경축도 다르다(CO₂→Li₂CO₃ ↔ H₂O→H₂S). **이식 가능 문법 4개**: ① μ_Li 불일치 프레임(`Fig. S5` 형식으로 **우리 값만** 그리면 "왜 코팅이 필요한가" 한 장) ② **코팅은 점이 아니라 조성영역**(우리 cascade 에 "조성 여유" 열) ③ 양 끝 SOC 를 둘 다 걸기 ④ 문턱형 게이트. ⛔ **이식 불가**: E_d 절대값 · LLZO 창 0→3.17 V([Zhu15] 는 **0.05–2.91 V** — 같은 계보 안에서도 **0.26 V** 흔들린다) · `Table 2` 후보 목록(전부 산화물) · `Fig. S4` halides 중앙 **−0.164 eV/atom**(**Li-M-할라이드 vs LLZO** 이지 우리 Cl 이 아니다 — `Fig. S3` 의 Cl 화합물은 `LiAlCl₄`·`LiGaCl₄`·`CsLiCl₂` 셋뿐이고 **황화물·현대 할라이드 SE 는 0종**) · `Table S4` σ |
| **B① ★★★ cathodic limit 의 *조작적 정의*가 계보에서 처음 그림이 됐다 — 그리고 그 정의로 재면 우리 대응 필드가 갈린다** | (계보 판정 · ★ **digest Q3 에 증거 1건**) | **[Honrao21]** `Fig. S2`(본 digest **픽셀 캘리브레이션**) + `Fig. 1`·`S4` 마커 | `Fig. S2` 캡션이 창을 *"the voltage range corresponding to **zero Li uptake**"* 로 정의하고, 계단마다 산물을 활자로 적는다 ⇒ **cathodic limit = Li uptake 0 평탄구간의 *아랫변***. 본 digest 픽셀 판독: `Li₃PS₄` **1.702 – 2.360 V**, 그 아래 `Li₂S+P`(1.262–1.702, uptake 5) → `Li₂S+Li₃P`(0–0.867, uptake **8**), 위로 `LiS₄+P₂S₇`(2.360–3.775) → `P₂S₇+S`. 그리고 **`Li₆PS₅I`(아지로다이트) `V_red` = 1.722 V**(figure-read). ⇒ **그 자리에 있는 우리 값은 `ocv_self_decomposition_V` 1.717 V 이고 `reduction_limit_V` 1.242 V 는 그 양이 아니다** ([Zhu15] 1.71 · [Wang26IF] 1.78 · [GG] K_eff=0 1.70 과 같은 자리). ⚠ **아직 판정 아님** — 할로겐이 다르고(I vs Cl)·hull 세대가 다르고·**우리 코드의 `reduction_limit_V` 정의를 아직 안 열어 봤다**. **작업거리(추가 DFT 0)**: `tools/oxidation` 의 `get_element_profile` 로 comp1 **Li uptake 프로파일 전체**를 `Fig. S2` 형식으로 그려 1.242 V 가 어느 계단인지 확정 |
| **B① ⚠ 그렇다고 정의의 *활자*가 여기로 옮겨오지는 않는다 — 본 편 식 (4) 는 오히려 흐리다** | **[Nolan21] 우위(정의)** | **[Honrao21]** 식 (4) ↔ **[Nolan21]** Methods 식 (5)(6) | 본 편 식 (4) 는 `eφ = E − μ_Li·N_Li` 로 **grand potential Φ 와 전극전위 eφ 를 한 줄에 뭉갠다**(우변은 에너지, 좌변은 전하×전압). `μ_Li = μ⁰_Li − eφ`(Li 금속 기준)가 **없다**. 식 (2) 도 조판에서 **지수 기호가 빠져** `S_ij=(R₀−R_ij)/b` 로 인쇄돼 있다. ⇒ **우리 2.256 V 정의의 인용처는 계속 [Nolan21] 식 (5)(6)**([Zhu15]→Mo/Ong/Ceder 2012 직계). **본 편은 그 정의의 *그림판*을 제공하는 편**으로만 쓴다 |
| **B① ★★ grand-potential 기계의 *재현성* 교차검증 3건 전원 통과 (서로 다른 논문·다른 구현·다른 hull 세대)** | (검증 — 우위 아님) | **[Honrao21]** `Fig. 1`·`Fig. S5` 픽셀 ↔ **[Nolan21]** Sup2 XLSX ↔ **[Zhu15]** 인쇄값 | `Li₃PO₄` **0.690**(figure-read) ↔ [Nolan21] **0.69** ↔ [Zhu15] **0.68** · `Li₂SO₄` **≈1.55** ↔ [Nolan21] **1.57** · `Li₇La₃Hf₂O₁₂` **0.469**(figure-read) ↔ 같은 논문 `Table S1` **0.470**. ⇒ **0.02 V 안에서 일치** = *"우리 2.256 V 는 같은 기계에서 나온 값"* 주장의 **세 번째 독립 보강**. ⛔ 값 이식은 여전히 금지 — **기계의 재현성만** |
| **B② ⛔ 그들 `Li₃PS₄` 창(1.702–2.360 V)을 우리 2.256 V 옆에 놓으면 안 된다 — phase set 이 다르다** | (경계 규율 — 우위 아님) | **[Honrao21]** `Fig. S2` 산화 첫 구간 활자 | 그들 산화 첫 산물이 **`LiS₄` + P₂S₇** 다 — **우리가 Gil-González 2022 phase set 을 따라 명시적으로 제외하는 바로 그 MP 상**(제외 시 우리 onset **2.256**, 포함 시 **2.14 V**). ⇒ *"phase set 선택이 anodic limit 을 바꾼다"* 는 우리 규율의 **문헌 실물 사례**. 조성도 다르다(Li₃PS₄ vs LPSCl) ⇒ **같은 표 금지, 정의·산물 순서 대조까지만** |
| **B③ ⚠ [Aykol14] 의 *산물 물리상태 게이트*는 6편 연속 미복원 — 게다가 본 편은 `LiS₄` 까지 산물로 인쇄한다** | **[Aykol14] 우위(방법)** | **[Honrao21]** 방법 전체(물리상태 언급 0) | 계보 답안 확정: #2 미복원 · #4 미복원(`O₂`) · #5 미복원(`O₂` + **`Li` 금속**) · **#6 미복원**(언급 자체가 0; 15,446종에 산화물·질화물이 대다수인데 `O₂`·`N₂` 취급을 한 줄도 안 적는다). ⇒ 우리 `interface_reactivity` 산물 파싱에 붙일 열은 계속 **ⓐ 기체·저융점 표시 ⓑ Li 소모 몰수 ⓒ 저장조상 제외** 셋이고, 여기에 **ⓓ 의심 MP 상 플래그**(`LiS₄` 류)가 추가된다 |
| **B③ ⚠ 계보의 *숨은 필터*가 #6 에서도 반복 — 이번엔 원소 필터와 목록 비공개 둘 다** | (재현성 비판 — 우위 아님) | **[Honrao21]** Screening 절 · `Fig. S3`–`S6` | ① *"we filter out **most** compounds with d- and f-block elements"* — **"most" 의 규칙이 없다**. 실제로 **Ti·Sc·Zn·Y·Zr·Hf·Ta·La·Pr·Tb·Er·Bi 가 살아남는다**(`Table S1` 에 `Li₈HfO₆`·`LiErO₂`·`Li₇La₃Hf₂O₁₂`·`Li₆Hf₂O₇`; `Fig. S4` 에 `Li₂Ta₂(OF₂)₃`·`Li₄ZrF₈`·`Cs₂LiPrI₆`) ⇒ **깔때기 재현 불가**. ② 본문 *"over 250"* ↔ `Fig. S3–S6` 마커 **137개**(본 digest 계수) — *"expanded results"* 가 **절반 남짓**. ③ **기계판독 데이터 공개 0본**(*"available upon request"*) — [Aykol16] CSV 2본·[Nolan19]/[Nolan21] XLSX 와 정면 대비. ⇒ 계보 패턴([Aykol16] `Fig. 1`·[Nolan21] `Fig. 1`)의 **세 번째 사례**이고 **가장 심하다** |
| **B③ ★★★ 독립 pseudo-binary 구현이 우리 `interface_reactivity` 를 값까지 재현한다 (vs LiCoO₂)** — Jiang: Li₆PS₅Cl **−302.12** · Li₅.₅PS₄.₅Cl₁.₅ **−308.41 meV/atom**, 산물 `LiCl + Li₃PO₄ + Co₉S₈ + Li₂SO₄ + Li₂S`. 탈리튬 Li₀.₅CoO₂ 에서 −434.98 / −443.75 | (우위 아님 — **교차검증**) | **[Jiang22Se]** Tables S8·S9 (x_m 포함) | 우리 `db/properties/oxidation_stability.json` → `/nd2o3_interface_reactivity_2026_06_17/min_dE_rxn_eV_per_atom_vs_LiCoO2`: **comp1 −0.3227 · modelc −0.3308 eV/atom**, 산물 `Co₉S₈ + Li₃PO₄ + Li₂S + LiCl + Li₂SO₄`. ⇒ **산물집합 완전 일치 · 값 7 %(20 meV/atom) 이내 · Cl-rich 페널티 크기까지 일치(+6.3 vs +8.1 meV/atom)**. ⚠ 우리 값은 **`canonical_registry` 미등록** — 인용 시 그 사실을 밝힌다. ⚠ 우리 caveat 유지(LiCoO₂ 는 NCM 대용, 열역학만, CEI 부동태 속도론 미포함) |
| **B③ ★ 접촉 상대가 바뀌면 Cl-rich 의 순위가 뒤집힌다** — LiCoO₂ 에서는 Cl-rich 가 더 반응적(−308.41 < −302.12)인데 **LiFePO₄ 에서는 확실히 유리**(−87.52 vs −99.75). FePO₄ 에서도 Cl-rich 유리(−177.68 vs −196.86) | **양극에 따라 다름** | **[Jiang22Se]** Tables S10·S11 · `Fig. 6` | 우리는 **LiCoO₂ 하나만** 봤다 ⇒ **우리 "Cl-rich 가 양극 계면에 약간 불리" 결론은 LCO 조건부**다. **[Zuo]** CV 서사와도 LCO 조건부로만 정합. ⇒ ★ **cascade S6 단에 "접촉 상대를 먼저 고정하고 상대별 문턱을 둔다" 를 넣는 근거** |
| **B③ ⚠ Se 도핑은 계면을 *악화*시킨다 — 제목과 반대** | **무도핑 호스트 우위** | **[Jiang22Se]** Tables S8–S11: LCO −302→−328 · LFP −100→−119 · FePO₄ −197→−215 (Li₀.₅CoO₂ 만 −435.0→−432.7 로 평평 = 잡음) | 우리 축과 직접 겹치지 않음(우리는 Se 를 안 봄). ⇒ **"σ 만 보는 스크리닝의 위험" 교보재로 사용.** 제목의 "improved interfacial compatibility" 는 **LGPS 340·Li₃PS₄ 405 meV/atom 대비**일 뿐이고 **무도핑 호스트도 그 비교를 통과**한다 |
| **B② ⚠ 이 논문은 축① · 축② 를 전혀 안 준다 (기록용)** | — | **[Jiang22Se]** — **ESW 0건 · Li 금속(음극) 계산 0건 · σ_e 0건 · E_above_hull 0건 · 계면 슈퍼셀 0건**. 계면은 **조성 수준 열역학**뿐 | 우리 onset(comp1·modelc 동일 **2.256 V**, S²⁻-limited)과 대조 불가. ⇒ ⛔ **이 편으로 "Se 가 산화안정성을 어떻게 한다" 를 말할 수 없다** |
| **B⑤ 🆕 가수분해 기전 — *우리 계 정면, 그런데 redox 가 아니다*** | (우위 아님 — **새 축 개설**) | **[Kim26Moist]** `papers/kim2026_moisture_surface_degradation_lpscl_dryroom.md` — Li₆PS₅Cl(001) 슬랩 DFT(VASP/PBE-D3(BJ)/520 eV/슬랩 k 3×3×1). **첫 반응 자리 = PS₄ 의 S(16e)**, `Esub` **−2.915 vs 자유 S(4d) −2.535 eV/O**. H₂O 흡착이 이웃 P–S 를 **2.246 → 2.993 Å / ICOHP −3.847 → −0.481 eV** 로 끊는다. 5단계(흡착→치환→**다면체 회전**→O-농화 표면→**부피수축 상분리**) · 실측 σ **3.13 → 2.00 mS/cm(−36.1 %, 3일, dry-room 이슬점 −60~−70 °C)** | ⚠ **우리에겐 이 축의 계산이 0건이다.** 표면 축은 전부 UMA 슬랩(vacuum 30 Å)이고 **DFT 흡착 파이프라인이 없다**. ⛔ 문헌 수치를 우리 원장으로 이식하지 않는다 — 가져오는 것은 **설계도**(자리 정의 4a/4d/16e · μ_O/μ_S 자리분해 치환 · LOBSTER ICOHP · 층 정의)뿐 |
| **B⑤ 방향 대조 — 우리 `o2_muO_screen` 과 *어긋나지 않는다* (그 이상은 못 쓴다)** | (우위 아님 — **경계 긋기**) | **[Kim26Moist]** P–O 형성이 구동력이라 PS₄ 의 S 부터 치환 · 최종 산물에 `Li₃PO₄` · **[Hyun25Han]** `PS₃O` 옥시설파이드 생성이 열역학적으로 선호 | 🔴 **`db/properties/o2_muO_screen_lpscl_2026_09_07.json` 는 `citable: None`** — 도구가 대상 상의 에너지 entry 없이 `get_element_profile` 만 호출해 **명목 조성의 0 K hull assemblage 변화**를 쟀고, 카드가 **⛔ "'P 가 먼저 산화된다' — 기전 주장이라 지지 안 됨"** 을 명시적으로 부인했다. 게다가 **화학이 다르다**(우리=O₂ 저장소 연 산화 / 문헌=H₂O 개시 가수분해)·**차원이 다르다**(벌크 조성 vs 표면 5층). ⇒ **허용 문구는 "방향이 어긋나지 않는다" 까지.** ⛔ *"우리도 같은 것을 봤다"* 금지. ⛔ **우리 Δμ_O −2.917 eV 와 그들 Esub −2.915 eV/O 를 나란히 놓지 않는다**(숫자만 닮음 — 최대 인용사고 위험) |
| **B⑤ 🔴 같은 양이 1.02 eV 갈린다 — *보고량 미정의의 외부 실물 표본*** | (우위 아님 — **방법 감사**) | **[Kim26Moist]** `E_ads(H₂O, LPSCl(001)) = −2.347 eV` vs **[Hyun25Han]** `−1.328 eV`. **둘 다 VASP·PBE-D3·520 eV·슬랩 k 3×3×1** 인데 **무질서**(정렬 vs 50 % S–Cl 혼합)·**종단**(둘 다 미기재)·**이완 구속**(전 이온 자유 vs 벌크 고정)·**흡착 자리 정의**("P–S 자리 근방" vs "Li atop")·**D3 감쇠**(BJ vs zero)가 다르다 | ✅ **우리 규율이 이긴다.** `kb/templates/estimand_card.md` §1–3 을 **던지기 전에** 채우는 규율(2026-08-28)과, 회신 N 의 판정 기준 *"admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라 보고량은 정의되지 않는다"* 의 **교과서적 외부 사례**다. ⛔ **두 E_ads 를 한 표에 놓지 않는다.** ⇒ 우리가 DFT 흡착을 열 때 **①무질서 배열 ②표면 종단 ③이완 구속 ④흡착 자리 ⑤vdW 감쇠** 를 카드에 먼저 적는다 |
| **B⑤ ⚠ 자유 S 의 역할이 두 축으로 갈린다 — "어디서 시작하나" ≠ "총량을 누가 키우나"** | (개념 이식) | **[Kim26Moist]** 개시는 **16e**(−2.915 vs −2.535 eV/O)인데, PS₄ 가 O 로 바뀐 뒤 **자유 S 의 ΣICOHP(Li–S) 가 −5.434 → −4.903 → −4.440 eV** 로 약해지고 그 S 가 O₂ 와 만나 **Li₂SO₃/Li₂SO₄** 가 된다. 실측이 짝이다 — 25일 XPS 에서 **Li₂S 5.71 → 1.08 %** / **SOₙ²⁻ 0 → 53.8 %** | ⭕ **우리 free-S ⟨3p⟩ 축(site-PDOS)은 지금까지 "어디서 시작하나" 만 물어 왔다.** 이 편은 **자유 S 를 2차 활성화 자리**로 놓는다 ⇒ 우리 축에 **"2차 활성화" 칸**을 여는 근거. ⚠ **가설 생성까지** — 우리는 수분 반응을 계산한 적이 없다 |
| **B⑤ 🆕 가수분해의 *전자적 원인* — E_F 근처 비결합 S 3p lone pair** | (우위 아님 — **기전 근거**) | **[Hyun25Han]** `papers/hyun_han_argyrodite_moisture_degradation_design_principles.md` — LPSCl(001) PDOS/COHP: PS₄ 의 S 가 **E_F 바로 아래에 비결합 3p 로브**를 남긴다(S 의 전기음성도가 낮아 π 전자를 P⁵⁺ 에 못 준다). 그 로브가 OH·H 를 문다 ⇒ **H₂S 생성 律速 ΔG_L = 0.534 eV**. **예비흡착 O\* 가 그 로브를 먹으면 ΔG_L 1.034 eV(≈2배)**, 예비흡착 H₂O 는 수소결합망으로 **0.298 eV(−44 %)** | ⭕ **우리 free-S ⟨3p⟩ / VBM-S 서사와 *같은 전자상태*를 가리킨다.** 우리는 그 상태를 **산화**(VBM 성분·ESW S-limited) 서술자로만 써 왔는데, 이 편은 **가수분해** 서술자로 쓴다 ⇒ **하나의 전자상태, 두 개의 열화 축**. ⚠ **가설 생성까지** — 우리는 수분 반응을 계산한 적이 0건이다. ⛔ ΔG_L 을 **"장벽/Ea" 라고 부르지 않는다**(계단의 최대 오르막 한 칸이지 전이상태가 아니다) · ⛔ 우리 MLIP-MD Ea 와 **같은 표 금지** |
| **B⑤ ⚠ 도펀트 선택 규칙 — *우리 Nd 논지에 대한 외부 견제*** | (규칙 이식 · 값 이식 금지) | **[Hyun25Han]** 선택 규칙 = **① d 궤도를 가질 것 ② P⁵⁺ 보다 산화수가 높을 것**(LMCT 로 비결합 S-3p 제거). **V⁵⁺ 0.648 / Mo⁶⁺ 2.264 / W⁶⁺ 2.393 eV** vs 무도핑 0.534. 반대로 **In³⁺ 는 "산화수가 낮아 전자 끌기가 약해 In–S 가 P–S 보다 약하다"**(`Fig. S10`). 15족 **As 0.491 · Sb 0.555 = 무효**, **Bi 1.956 은 S–S 경로** | ⚠ **우리 Nd/O 공치환과 방향이 어긋난다** — **Nd³⁺ 는 f 원소이고 산화수가 낮다** = 이 규칙의 반대편이고, In³⁺ 에 대한 그들의 경고와 같은 방향이다. 🔴 그리고 **`db/properties/ndo_passivation_argument_2026_09_14.json` 이 이미 적어 둔 반대 증거**(Nd 가 **CBM 에 27.8 %** → 전자 쪽으로 나빠진다 · Nd₂S₃ 갭 0.76 eV → 부동태 아님 · ESW 창이 **좁아진다**)와 **같은 방향**이다. ⚠ **그 카드는 `status: proposed · citable: false`** 이고, **Nd 는 P 자리 도핑이 아니다** ⇒ 규칙을 **직접 적용하지 않는다.** ⛔ *"그러니 Nd 는 수분에도 나쁘다"* 로 확장 금지 — 우리도 그들도 그 계산을 한 적이 없다 |
| **B⑤ ⭕ 우리가 못 보던 보호 기구 — S–S 결합** | (개념 이식 — **새 서술자 후보**) | **[Hyun25Han]** Bi⁵⁺ 도핑이 BiS₄ 사면체를 깨고(왜곡지수 **0.160**, 나머지 5종은 0.007–0.018) S 를 밀어내 **이웃 S 와 S–S 결합**을 만든다 ⇒ 그 S 는 3p 를 이미 써서 중간체를 못 문다 ⇒ **ΔG_L 1.956 eV(3.66×)** | ⭕ **우리 원장에서 S–S/폴리설파이드는 항상 *분해 산물*이었다** — ESW 계단 첫 칸의 `LiS4`(`our_dft_baseline.md`), μ_O 스크린의 폴리설파이드. **표면의 S–S 가 보호 기구일 수 있다**는 반대 방향은 우리에게 없던 칸이다 ⇒ `kb/questions/` 카드 후보. ⚠ **먼저 확인할 것**: 그들의 S–S 판정 창이 **1.8–3.0 Å 로 지나치게 넓다**(S₈ 는 2.06 Å, 3.0 Å 은 사실상 vdW 접촉). 직접 증거는 `Fig. S8` 전하밀도 차인데 **우리는 그 그림을 못 봤다** ⇒ **그림 확인 전 인용 금지** |

> 🖼 **프레임 주석 (수치 비교 아님 · 축 B)** — **[Miao23]** `Fig. 4c` = **μ_c ↔ HOMO 정렬 도식**: 양극 화학퍼텐셜 μ_c 가 황화물 **HOMO 위**면 안정, **아래**면 산화 → CEI 생성; 그 **CEI(또는 코팅)의 HOMO 가 μ_c 보다 낮아야** 자기제한("Stable"), 높으면 "Unstable"(연속 반응). **이 리뷰에 무기 SE 의 ESW 수치는 0개**(유일한 ESW 값은 폴리머 버퍼층의 **5.1 V vs Li/Li⁺**) → **B 축 수치 행 없음**. 우리 grand-potential 계단(onset **2.256 V** S²⁻-limited → 2.385 → 3.326 V)이 **같은 물리의 정량판**이며, 발표에서 두 장을 나란히 놓으면 "단일 준위 만화 → 상 경계 계단"의 전환을 한 컷으로 보여줄 수 있다. ⚠ 두 가지 규율: ① **HOMO/LUMO 는 분자 용어** — 고체는 VBM/CBM(축 D 주석 참조) ② 이 리뷰는 **열역학/속도론을 안 가른다**(후속 `fan2026` §3.4 는 가른다) → "Cl-rich 산화안정"은 **축 명시 필수** 규율 그대로.

> 🕰 **운동학 주석 (수치 비교 아님 · 축 B③ 의 *시간축* 짝, 2026-09-22 신설)** — **[Ncube26]** 은 우리 **B③ `comp1|LiCoO₂ −0.3227 eV/atom`** 과 **같은 양극(LCO)** 을 쓰지만 SE 가 **LGPS** 이고, 무엇보다 **묻는 양이 다르다**: 우리는 *"반응이 얼마나 유리한가"*(0 K hull, eV/atom), 그들은 *"그래서 몇 시간에 몇 μm 가 되나"*(MLMD → 1D phase-field, μm/h). ⇒ **두 값은 같은 표에 놓을 수 없다** — 단위도 물질계도 다르다. **가져올 수 있는 것은 위상(phase) 관계 하나**: 우리 −0.3227 eV/atom 은 `[Xiao20Rev]` 규율대로 **worst-case 구동력 하한**이고, **[Ncube26]** 이 보여주는 것은 그 구동력이 **실제로 상온 ns 안에 실현될 수 있다**는 것이다 — ⚠ 단 **3면 중 1면((010))에서만** 실현됐다. ⇒ **허용 서술**: *"0 K hull 이 주는 큰 음의 반응에너지는 면 의존적이지만 실제 상온 동역학으로 실현될 수 있다(외부 MLMD)."* ⛔ **금지**: 그들의 D·두께·용량 수치를 우리 B③ 옆에 적는 것 · *"우리 −0.3227 이 24 h 에 1 μm 를 뜻한다"* 식의 환산(그들 D 자체가 자기 그림과 재현 안 됨). 상세 = `papers/ncube2026_ionic_interdiffusion_lco_lgps_multiscale.md` §7a·§10.

## C. 기계적 물성 — *값이 functional·정의 의존*
| 주장 | 출처 | 우리 | 비고 |
|---|---|---|---|
| **★★★ 🆕 우리 E_VRH 가 "계면 박리하나" 라는 *다른 축의 판정*으로 이어진다 — 사슬이 끊기지 않는 드문 경우** (2026-09-22 신설) | **[Ncube26]** `Table S2`·`Table S3`: 연속체에 **E(LGPS) = 20 GPa** 를 쓰고 출처를 **ref 13 = [Deng16]** 으로 명시. 그 20 은 [Deng16] Table III 의 **LGPS E = 21.7 GPa 를 반올림**한 것. → 그 E 로 돌린 2D 모델이 **`Fig. S10e`: 최대 인장응력 LE ≈8 · LGPS ≈50 · LLZO ≈500 · LNTO/LGPS ≈400 MPa** 를 내고, 그림이 직접 **"No interfacial delamination"**(LE·LGPS) vs **"delamination possible"**(LLZO·LNTO) 로 라벨한다 | comp1 **E_VRH 22.06** / modelc **27.66 GPa** (relaxed-ion). **그리고 [Deng16] 의 Li₆PS₅Cl E = 22.1 / G = 8.1 이 우리 comp1 22.06 / 8.13 과 이미 0.2 / 0.4 % 로 일치 판정돼 있다**(`papers/deng2016_…md` §7) | ✅✅ **중간 고리가 우리 값과 0.2 % 로 맞아서 방법 사슬이 이어진다**: 우리 22.06 ≈ Deng LPSCl 22.1 ≈ Deng LGPS 21.7 → Ncube 채택 20 → **≈50 MPa → "박리 없음" 칸.** ⇒ **우리 아지로다이트(comp1·modelc 둘 다)는 Ncube 분류의 *무른·안전* 칸이고 LLZO/LNTO 칸이 아니다.** ⛔⛔ **옮기는 것은 "칸" 이지 MPa 가 아니다** — 50 MPa 는 LCO 이방성 팽윤·2D 격자 방위 무작위·그들 경계조건의 산물이다. ⚠ 유보 4: ① Ncube 는 자기 출처와도 어긋난다(Deng ν = 0.37 인데 Ncube 는 **ν = 0.3 "가정"**, 21.7→20 반올림) ② **박리 문턱이 도출된 게 아니라 4점을 눈으로 가른 것**이고, 정작 자기가 계산한 **W_ad 를 강도로 환산하지 않았다** ③ **분류에 쓸 탄성량을 고정해야 한다** — 우리 comp1→modelc 는 **E_VRH 는 오르고(22.06→27.66) B₀ 는 내린다(26.23→21.71)**. **Ncube 축은 Young's modulus** ⇒ **E 로 분류했음을 명시** ④ 우리 SE 는 Ncube 계산에 **들어간 적이 없다**(그는 LGPS 를 돌렸다) — *"우리 계가 안전하다고 계산됐다"* 금지, *"같은 탄성 밴드라 그의 안전 칸에 든다"* 까지 |
| ⛔ **"LPSC Young's modulus 3.97 GPa" 는 우리 값과 같은 표에 놓으면 안 된다 — 물리량이 다르다** — AFM QNM/DMT 로 **냉간가압 펠릿 표면**을 300 nm 압입한 접촉강성이다. Li 금속 4.5 / pristine LPSC **3.97** / Li 접촉 LPSC 계면상 **2.29** / FG 펠릿 4.59 / Li 접촉 FG 계면상 **7.69** GPa. ⚠ 탄성률 맵 컬러바 하한이 **−3.1 GPa(음의 탄성률)** 이고 **팁 반경·스프링상수·모델 미기재** → 절대값 검증 불가 | **[Ling26]** `Fig. 3e,f` · `Fig. S14` | 우리 relaxed-ion **E_VRH 22.06(comp1) / 27.66(modelc)** · B₀ 26.23 / 21.71 GPa · **[Torii]** DFT-D3 E 27.4 · **[Sakuda]** 실험 유리 18–25 GPa | **✅ 쓸 수 있는 건 *비율* 뿐**: Li 접촉 후 LPSC 계면 **0.58× 연화**, FG 계면 **1.68× 경화**. 🔑 그리고 그 비율로 보면 **Monroe–Newman 기준에서 pristine LPSC(3.97) < Li(4.5) 로 애초에 미달**이고 FG 계면상(7.69)도 Li 의 **1.7배**라 통상 요구치 2배에 못 미친다 ⇒ **이 논문의 덴드라이트 억제는 기계가 아니라 *편향(deflection)* 으로 읽는 게 정직하다**(Fig. 3b,c 가 그렇게 보여준다) |
| ⭕ **독립 그룹 CASTEP-PBE 전단탄성률: LPSCl G = 7.36 · Li₃PS₄ 12.51 · Sn-LPSCl 8.59 · LLZO 58.86 · LiPON 41.26 GPa** (참조 Li 금속 4.2 GPa, Monroe–Newman 2× 기준) | **[Tu27ML]** 본문 §3.1 (⚠ **계산법 한 줄도 없다** — clamped/relaxed·유한변형 여부 미기재) | comp1 **G_VRH 8.13** (relaxed-ion) / **20.1** (clamped-ion) · modelc **10.61** · lpsocl **13.58** · comp2 **7.47** GPa | 🔑 **7.36 이 우리 relaxed-ion 8.13 과 9.5 % 이내로 맞고 clamped-ion 과는 2.7배 어긋난다** ⇒ **'clamped-ion 은 argyrodite 탄성률을 계통적으로 과대평가' 판정의 3번째 외부 정합.** ⚠ 단 **논문이 방법을 안 밝혔으므로 정합이지 검증이 아니다.** ⭕ 부수: 논문 자신의 2× 기준으로 **LPSCl 7.36/4.2 = 1.75 는 미달**인데 본문은 8종을 뭉뚱그려 *"strong ability to inhibit lithium dendrites"* 라 쓴다 — 우리 값으로는 comp1 1.94(미달)·**modelc 2.53(통과)** 이라 **"Cl-rich 가 Monroe 기준을 처음 넘긴다"** 는 서술이 가능해진다 (⚠ Monroe 기준 자체가 등방탄성 가정이라 논쟁적이고, 우리 값도 0 K relaxed-ion) |
| **★★★ soft thiophosphate glass 실측 E ≈ 20 GPa · G ≈ 7 GPa** (Li₂S–P₂S₅, 나노인덴테이션) | **[Famprikis19]** Box 1 (**ref 108 = McGrogan et al. *Adv. Energy Mater.* 7, 1602011 (2017), "Compliant yet brittle"**) | **relaxed-ion** comp1: **E_VRH 22.06 / G_VRH 8.13 GPa**; **clamped-ion** comp1: 52.31 / 20.12 | **✅✅ vacancy-paradox 판정의 *네 번째 외부 앵커*** — relaxed-ion 과 **+10 %(E)·+16 %(G)**, clamped-ion 은 **2.4×(E)·2.9×(G)** 어긋나 배제. [Deng16](PBEsol 계산)·[Torii](PBE-D3 계산) + `elastic.json` 기존 실측 메모(**~23 GPa, He et al. / G ~8 GPa**)에 더해 **재료가 다른(유리) 독립 실측**이 같은 자리를 가리킨다. ⚠ **"첫 실측 앵커" 라고 쓰면 틀린다.** ⚠ **유보 3**: ① 재료가 다르다(**Li₂S–P₂S₅ 유리** vs 결정질 argyrodite), ② hot-press 시편이라 **잔류 기공·GB 포함 → 진짜 단결정보다 낮게 나올 여지**(우연 일치 가능성), ③ 리뷰가 "≈" 로만 인용하고 오차·시편밀도 없음. **⇒ "실험이 우리를 검증했다" 금지. "같은 자릿수이고 clamped-ion 은 배제된다" 까지만.** 참고 E/G 비: 실측 2.86 / relaxed 2.71 / clamped 2.60 → **비율은 판별력 없음, 절대값에서만 갈린다** |
| **산화물 끝점: 단결정 garnet E ≈ 150 GPa · G ≈ 60 GPa**; 가장 무른 끝: **LiBH₄ G ≈ 4 GPa** | **[Famprikis19]** Box 1 (ref 147 = Yu 2016 *Chem. Mater.* 28, 197 / ref 148 = Ahmad 2018 *ACS Cent. Sci.*) | 우리 argyrodite E_VRH 22–28 GPa | ✅ **스펙트럼 고정** — 우리는 4–150 GPa 스펙트럼의 **무른 끝**. [Kang] "sulfide SE 20–30 vs oxide CAM 150–200 GPa 변형 불일치" 서사와 같은 자리 |
| **⚠ "무르다 ≠ 안 깨진다"** — *"such soft materials (for example, **lithium thiophosphate glasses**) **remain brittle and prone to fracture on stress**"*(ref 108) | **[Famprikis19]** §Mechanics | 우리 B/G 3.14(comp1)·2.21(modelc) = "연성" 판정 | **⚠ 우리 B/G 연성 결론의 한계 표시** — B/G(Pugh)는 **소성 변형능**의 지표이지 **균열 저항**의 지표가 아니다. [Deng16] "argyrodite = 가장 연성" 과 이 문장을 같이 인용해야 정직하다. **리뷰는 두 명제를 병치만 하고 화해시키지 않는다**(어느 조건에서 연성이 취성을 이기는지 판정 없음 — 그 판정은 `fan2026` >3 µm 파쇄 / <1 µm 완화) |
| **★ K_Ic 를 "결정 인자로 부상" 이라 격상해 놓고 수치를 하나도 안 준다** + 판정: *"**Unlike the elastic moduli, fracture toughness is heavily dependent on microstructural parameters** (densification, grain size, impurities, pre-existing cracks, porosity)"* / *"DFT can provide estimations for the **elastic moduli** … However, the **fracture toughness … will need to be determined experimentally**"* | **[Famprikis19]** §Mechanics·`Fig. 6` (**ref 109 = [Bucci17]** 사이클 유도 파괴 → 임피던스↑·용량손실 / **ref 110 = [Deng16]** = "DFT 로 탄성 낼 수 있다"의 유일 근거) | 우리 K_Ic: **없음**. litdb 유일 소환값 = **[Fan26] 0.2–0.4 MPa·m¹ᐟ²** (그것도 재인용) | **❌ 이 논문에서 K_Ic 수치 소득 0 — 그러나 부정 결과가 유용하다**: 리뷰가 **"K_Ic 는 DFT 의 산출물이 아니다"** 라고 못박으므로 **우리 캠페인의 K_Ic 공백은 누락이 아니라 방법론적 경계**. ⇒ K_Ic 는 **DEM/CZM 의 *입력 파라미터*로 sweep** 하는 것이 옳은 처리(ref 109 = 우리가 이미 가진 `bucci2017…czm`). **⚠ 이 논문을 K_Ic 의 *수치 출처*로 인용 금지 — 개념 출처로만** |
| **γ_xfc 정의**: *"the **chemical interfacial energy**, corresponding to the **difference in bonding and coordination at the interface compared with the bulk**"*; 접착 3성분 = γ_xfc + **격자 misfit 변형** + **계면 전하재배치 정전인력**. **σ_adh**(박리에 필요한 압력) ↔ **Li/LLZO 계면저항** 직접 상관 실증 | **[Famprikis19]** §Mechanics·`Fig. 6` (ref 107 = Wang & Sakamoto *JPS* 377, 7 (2018); ref 106 = Han 2016 wettability) | `db/properties/adhesion.json` **γ_SE(comp1) 1.211 J/m²** · **W_ad(v2 melt) 1.107 ± 0.027 J/m²** | ⚠ **정의는 정확히 우리 W_ad(Dupré) 다 — 그러나 리뷰에 수치가 없어 대조 불가**. 얻은 것은 **개념 다리 하나**: *"mechanical strength ↔ effective ionic transport across interfaces"* ⇒ 우리 **W_ad → σ_adh 환산**을 하면 기계량이 계면저항이라는 측정량과 연결된다(**H-리스트 신규**). ⚠ 우리 rigid-분리 W_ad 는 dangling-bond 인공일로 과대(`adhesion_calibration_decision_2026_05_17.md`) → 환산 전 SMD-PMF 계열 보정 필요 |
| **★ Monroe–Newman 전단탄성률 기준은 *무기* SE 에 적용되지 않는다** — 이론(ref 146 = **Ahmad & Viswanathan, *PRL* 119, 056003 (2017)**) + 실험(ref 12: **E ≈ 20 GPa 유리부터 E ≈ 150 GPa garnet 까지 전 구간에서 Li 가 자란다**). 오히려 **더 무른** 무기 SE/계면상(LiBH₄ G≈4 GPa)이 균질 전착에 유리할 수 있다는 반대 주장까지 병기 | **[Famprikis19]** Box 1 | 우리 G_VRH comp1 8.13 / modelc — (relaxed-ion) | **🔑 위 331행 미결 항목("Monroe–Newman 과 K_Ic 가 대체인지 보완인지 미정")에 답이 붙는다 — [Famprikis19] 는 "대체" 쪽**: Monroe 기각 → **파괴역학(K_Ic)+미세구조**로 이동. [Miao23] 이 인용한 "G ≥ 2G_Li" 는 **고분자 기준의 무기 전용(轉用)** 이며 2019년에 이미 기각됐다. **⇒ 우리 G 값으로 "덴드라이트 억제 기준 만족" 이라고 쓰면 안 된다**(기존 경고 강화). ⚠ 단 리뷰 스스로 *"currently unclear which factor is the most crucial"* 로 닫으므로 **"무르면 좋다"로도 결론 금지** |
| **Li 금속 항복강도 ~0.8 MPa**(ref 144 = Masias 2019, elastic+plastic+**creep**); 금속음극은 **MPa 급 압축응력** 하 → **항상 소성**. Li 몰부피가 **어떤 무기 SE 보다 ~10× 커서** 국소 팽창·응력 유발 | **[Famprikis19]** Box 1 | 우리 Li 금속 역학 **미계산** | ⚠ **DEM 축 소득** — Li 접촉모델의 σ_y 앵커. 우리 DFT 축에는 대응 칸 없음(H-리스트) |
| **CCD ≤ 0.3 mA/cm²**(실계면적, 상온, 대부분 무기 Li SE) vs **경쟁 목표 3–10 mA/cm²**; 파괴 2단계 = ① 입계·공극 우선 핵생성(계면 불균일 → 전류 핫스팟) → ② 균열이 결정립·입계·공극 따라 전파 + Li 침투 → 단락 → Joule 발열 Li 용융 → 전압 진동 | **[Famprikis19]** Box 1 (refs 10,12,137,143,149,150) | 우리 축 밖 (device) | ✓ **덴드라이트 서사의 정량 프레임**. ⚠ **"wedge-opening" 이라는 용어는 이 리뷰에 없다** — `fan2026` 의 wedge-opening 은 후속 어휘. 두 서술은 같은 현상(균열 후단 Li 주입)을 다른 이름으로 부른다 |
| **Li₆PS₅Cl C₁₁/C₁₂/C₄₄=39.9/23.1/7.8·B=28.7·G=8.1·E=22.1·ν=0.37** (PBEsol, **ordered Li@24g — SQS 아님**, strain-stress·relaxed-ion 정황) | **[Deng16]** Table III (구 라벨 "[Kaur]/SQS"는 오귀속 — 2026-07-28 원문 검증으로 교정) | **relaxed-ion** comp1: C₁₁ 37.67/C₁₂ 20.43/C₄₄ 7.98/B 25.51/G 8.13/**E 22.06**/ν 0.356 | **✅✅ E·G·C₄₄ 0.2–2 % 일치 — 우리 relaxed-ion의 *최근접* 외부 앵커** (D3 없는 GGA+ordered+relaxed-ion 4축 정렬; [Torii] D3는 +24 %). B·C₁₂만 +12–13 %=PBEsol 격자 압축. functional 사다리(B): PBE 25.51 < PBEsol 28.7 < PBE-D3 34.7. ⚠ E 0.2 % 일치는 부분 우연(C₄₄·C₁₁−C₁₂만 근접) → "±수 %"로 인용 |
| **Zener A: 논문 미보고** — 인쇄 Cᵢⱼ 유도 시 Cl **0.93**(0.92는 절사)·Br 1.07·I 1.16 | **[Deng16]** (유도값 — [Torii] Table 1 "0.92"의 원출처) | comp1 relaxed 1.144(1st triplet)/**avg-Cᵢⱼ 0.926**·clamped 1.073; modelc relaxed **1.441** | ordered 3자(Deng 0.93·Torii 1.09·우리 1.14) 전원 **A≈1 등방** — A−1 부호는 방법 노이즈(우리 triplet 산포 1.14↔0.75가 문헌 간 격차보다 큼, elastic.json 규율). **문헌에 SQS/무질서 탄성 계산 자체가 없음이 확정** → "disorder→A 1.44"는 우리 고유 기여 강화 |
| **halide 치환 경향: Cl→Br→I로 *경화*** (C₄₄ +53 %·E 22.1→25.3→30.0) | **[Deng16]** Table III | comp2(Cl₀.₅Br₀.₅) E 20.03(**−9.2 % 연화**)·B −18 %; [Kraft] 음속 −24 %·[Kim2025] Br↑→E↓ 실험 | **✗ Deng만 고립된 반대 방향** — 실험 2건+우리 동일프로토콜 DFT 전부 "큰 할라이드=연화". 원인 후보=Li@24g 고정 배치+음이온 무질서 0 가정(Kraft의 Cl→I Li 재배치·무질서 소멸을 모델이 못 봄). **⚠ Deng의 halide *경향* 인용 금지 — 단일 조성 절대값만 소환** |
| **Li₆PS₅Cl G/B=0.28 = 23종 SICE 중 최저(최연성)**; thiophosphate 전체 G/B<0.5·산화물 0.5–0.6·antiperovskite ~0.7(취성); 황화물 E<50/B<40/G<20 GPa·냉간가압 충분 | **[Deng16]** Table III·Fig 1·obs.1/2/6 | comp1 relaxed B/G 3.14·comp2 2.79·modelc 2.21 (전원 ductile) | **✅ "argyrodite=가장 연성 좌표"의 정량 원점** — [Rupp]/[Kang] 리뷰 "soft SE 20–30 GPa·연성"의 6–9년 앞선 1차 계산 근거. cascade mechanical_soft/ductility 테마 인용처. Monroe–Newman으론 전 SICE dendrite 차단(min G 7.9)이나 **Nagao 균열 지배를 저자 자신이 명시** — [Rupp] "G 하나로 결론 금지"와 한 줄 |
| **E=27.4·B=34.7·G=10.0·C₁₁/C₁₂/C₄₄=47.4/28.4/10.4·ν=0.37·B/G=3.46·Zener A=1.09** (full-DFT, PBE-D3, **relaxed-ion**) | **[Torii]** Table 1 | **relaxed-ion** comp1: E 22.06/B 25.51/G 8.13/C₁₁ 37.67/C₁₂ 20.43/C₄₄ 7.98/ν 0.356/A 1.144 — **vs clamped** comp1: E 52.31/B 43.59/G 20.12/C₁₁ 74.23/C₄₄ 18.98/A 1.073 | **🔑🔑 PARADOX 판정: Torii는 우리 *relaxed-ion* 영역** (E·G·C₁₁·C₄₄·ν 모두 Δ+23~30 %=D3) — **clamped(≈2× 큼) 아님**. → 외부 full-DFT가 "clamped 과대평가" 진단 독립 확증. Δ는 *계통적 D3 강성*(전 Cᵢⱼ +23~39 %, C₁₂가 최대→B), relaxed/clamped 류 *질적* 차이 아님 |
| **★ 할라이드 치환의 격자 무름 *실측* (speed of sound·RUS·Debye) — 우리 "할라이드가 modulus에 둔감?" 가설 판정** — Cl→Br→I(더 분극성·큰 할라이드) **speed of sound −24 %**(v_long 1480→1130 ms⁻¹)·**Debye ν_D −22 %**(2.45→1.90×10¹² Hz), Cl→Br₀.₅I₀.₅; 순수 I 무질서 0→소폭 반등. RUS 탄성텐서 C₁₁/C₁₂/C₄₄ 측정(표 미공개). **밀도보정 시 전단 C₄₄ ~−15~30 %**(우리 추정: d Cl 1.86→I 2.29 g/cm³) | **[Kraft]** (2017 JACS, PE·RUS·중성자, **DFT 없음**, 외부; **Torii "sound velocity·Debye 미보고(n/a)"의 상보**) | comp1 relaxed E_VRH 22.06/B_VRH 25.51/G_VRH 8.13/C₄₄ 7.98 GPa·EOS B0 26.23; **comp2(=Kraft Cl₀.₅Br₀.₅) elastic 진행중** | **판정(정직·조건부)**: (1) **강한형태("할라이드가 강성 거의 안 바꿈") 기각** — full-exchange speed of sound/Debye −15~24 %, 밀도보정 C₄₄ ~−15~30 %=할라이드가 강성을 *유의*하게 무르게 함; (2) **약한형태("P–S 골격이 baseline, 할라이드는 2차 변조") 지지** — comp1→**comp2(50 %Br)는 speed of sound ~−8 %·Debye ~−6 %만**, 상당분 밀도효과(v∝√(C/ρ), ρ↑); (3) **comp2 elastic이 comp1 대비 ~5~10 % 연화(B/G 소폭↓)면 Kraft 정합**, 0이면 약한 긴장→k/relaxed-ion/무질서 점검. ⚠ **Kraft는 B/G 미보고**(speed of sound/Debye/C_ij만)→"Kraft B/G X %" 인용 금지, 우리 대조는 *음속/Debye/C₄₄*. **modelc(Cl-rich)는 Kraft 밖**(Li 공공/무질서 축≠할라이드 교환; 우리 modelc E_VRH 27.66↑는 C₄₄/disorder 효과, Kraft 연화와 다른 기전) |
| **B(VRH)=34.7 GPa** + 평형 a=10.04 Å | **[Torii]** | **BM-EOS B0 comp1 26.23**; relaxed B_VRH 25.51; clamped B_VRH 43.59. a=10.0551 Å | **✅ 부피 일치**(a Δ0.02 %=같은 packing) **but B 절대값 Torii +32 %**: (i) VRH-B ≠ BM-EOS B0 정의차(우리 relaxed B_VRH 25.51 ≈ EOS B0 26.23, 3 % 이내), (ii) **D3가 C₁₂ +39 %→B↑**. ⚠ **Torii VRH B 34.7 ↔ 우리 EOS B0 26.23 등치 금지** — functional 맞추면(우리 PBE B_VRH 25.51) 정합 |
| **Zener A=1.09 (등방, vacancy-free LPSCl)** | **[Torii]** (ordered single config) | comp1 relaxed A=1.144 / clamped 1.073 (등방); **modelc relaxed A=1.441 / clamped 0.416** (disorder→이방) | **✅ vacancy-free=등방 외부 확정** → 우리 elastic.json "anisotropy = the only Cij-level fingerprint of vacancy/disorder"의 *대조군 고정*. Torii는 vacancy 조성 안 함 → "disorder가 A를 키운다"는 *우리 고유 기여* |
| **전단 취성 ε_fracture=0.7 %** (Cl→Li 이동→Li₄Cl→layered gap); 인장은 ε~0.2까지 durable; strength {100}8.8>{111}6.2>{110}5.9 GPa | **[Torii]** Fig 7·3·Table 3 | 우리 elastic = C₄₄/G(낮음)·B/G(연성)만; **전단 응력-변형 *미계산*** | **그들 고유 기여 = 우리 모듈러스의 *메커니즘***. 낮은 C₄₄/G의 "왜 취성"을 원자수준(Cl 이동)으로 줌. [Kang]§3 chemo-mech 취성과 연결. ⚠ 우리 데이터엔 fracture 곡선 없음 → "우리가 보였다" 금지, Torii 인용 |
| E 21.3→21.6 (Cl0→1.5 거의 불변) | Excel calc#12 (별개 논문) | 우리 E_VRH 22→27.7 (변동) | 무질서/protocol 차이 |
| **sulfide 연성(B/G 1.25–2.5, E~10–37 GPa, 냉간가압) vs oxide 취성(E 100–200 GPa, K_IC 0.8–1.6)** | **[Rupp]** SI Table 1·§2.4 | 우리 B/G·연성 결론 동일 | **✓ "왜 황화물" deck 1슬라이드** (연성=부피변화 수용·intimate contact) |
| **sulfide SE E 20–30 GPa(소성변형으로 응력 수용) vs oxide CAM E 150–200 GPa → 변형 불일치=공동/접촉손실/균열** | **[Kang]** §3.1.1/§3.1.3 (refs101–103) | 우리 E_VRH·EOS B0 (comp1 26.2/modelc 21.7 GPa BM-EOS); DFT 0K E_VRH comp1≈modelc 52.3 | **✓ landscape 정렬** (우리=soft SE 줄). ⚠ **vacancy paradox**: DFT 0K가 Cl-rich 강성 못 잡음(리뷰 "20–30 GPa·연성" 추상화의 *방법 의존성*을 우리가 노출) |
| **CAM 부피변화 6–8%·이방성 → SE microgap·균열·접촉손실(chemo-mechanical)** | **[Kang]** §3.1.2/§3.1.3 (ref103) | 우리 elastic = SE 측 응력 수용 능력(연성)만; CAM 부피변화·접촉손실은 device 스케일 | △ **우리 bulk DFT 밖** (phase-field ref39·우리그룹이 다리) |
> 📐 **methods 레퍼런스 note — *재료 비교 아님* (NOT a materials comparison)** [`papers/choi2025_mlip_cu_taxn_interfacial_adhesion.md`]: **Choi 2025 = Cu/비정질-TaₓN(반도체 Cu배선 확산방지막) 계면 work-of-adhesion W_ad를 MLIP로 계산하는 방법론 논문**(외부·다른재료). 위/아래 어느 물성축 표에도 *행으로 넣지 않는다*(Cu·Ta·N 우리 hull 부재, W_ad 절대값 3–7 J/m² ↔ 우리 LPSCl/NCM W_ad는 *물리 무관*, "그들 5 우리 2" 류 비교 금지). **연결 = "우리 W_ad/UMA를 *어떻게 계산·검증하나*"의 방법 매핑뿐**: (1) **🔑 W_ad 산출법** — 그들은 **비평형 SMD(steered MD) 당김 → Jarzynski 지수평균 → PMF plateau = W_ad**. 우리 Stage11 `(E_sep−E_int)/A` rigid-분리는 **dangling-bond 인공일로 절대값 100–1000× 과대**(`kb/methodology/adhesion_calibration_decision_2026_05_17.md`: 실험 0.2–0.4 vs 우리 45–225 J/m²) → **SMD-PMF가 그 과대의 정공 처방**(분리경로를 동역학으로 밟아 인공 단절 회피). 우리 v30u binding-curve(Morse well-depth) 적분이 SMD-PMF와 같은 물리량임을 인용 가능. (2) **🔑 UMA 신뢰 외부 앵커** — 동급 **E(3)-equivariant MLIP(SevenNet)가 bulk modulus·계면에너지를 DFT 5%이내·force MAE<0.3 eV/Å**로 재현 → 우리 **UMA wad/elastic**(Nd₂O₃ B0 UMA 18.9 vs DFT 19.9 GPa ≈5%)가 *MLIP 계열의 일반 정확도*임을 보여주는 제3자 검증. (3) **종별 결합밀도 descriptor** — 그들 Cu-Ta/Cu-N 카운트 = 우리 **Li-O/Cl-O density(v14–26, R=+0.82/−0.91)**의 독립 확증("에너지보다 결합밀도가 robust"). (4) **비정질 샘플링** — MQA ensemble(조성당 10구조)+slab-anneal+SMD = 향후 **amorphous SEI W_ad 템플릿**. ⚠ **정직한 한계**: UMA는 SevenNet과 달리 **vacuum 민감**(`kb/methodology/adhesion_energy.md`: 30 Å OK / 60 Å→10× 과대) → SMD가 vacuum 생성하므로 **UMA-SMD는 OOD 위험**(셀확장·구속 신중; SevenNet은 slab/surface 학습으로 회피). force MAE 0.3 eV/Å는 *큰 효과(family/route/x)*엔 충분하나 *미세 조성차*(intra-Li5.4 Δ<0.005)엔 부족 — 우리 분해능 한계와 호응. **방법 논문이므로 "우리 재료와 일치" 주장 금지 — 연결은 W_ad-계산·MLIP-검증 방법 매핑뿐.**
| ⚠ argyrodite **E 92–100 / G 38–43 GPa** (단일 ref) | **[Rupp]** SI Table 1 | 우리 E_VRH 22–28 | **✗ outlier — 인용 금지** (같은 표 glass 13–28·LGPS 37과도 어긋남) |
| Monroe-Newman: dendrite 억제 **G_SE > ~2 G_Li (≈6.8–8.5 GPa)**, 단 무기SE엔 불충분(K_IC·grain·σ_e가 변수) | **[Rupp]** §2.4/§4.2 | 우리 G_VRH·B/G → dendrite 다리 | 우리 elastic→dendrite 연결 시 **G 하나로 결론 금지** |
| **LPSCl "~30 GPa" (탄성계수) vs 지방산 코팅 0.1–2 GPa** — 소프트 코팅이 스택압 하에서 변형·void 억제·저압(35 MPa) 작동 논거 | **[Qian26]** (문헌 통념값 인용, **원전 미명시**) | 우리 **E_VRH comp1 22.06 / modelc 27.66 GPa**(DFT relaxed-ion) | **✓ 정합** — modelc 27.66이 그들 "~30"과 사실상 동일. ⚠ 그들 값은 출처 없는 round number → **"우리 값이 검증됐다" 금지**, 우리 DFT가 통념대로 나온다는 sanity check까지만. **부수 관측: 펠릿 공극률 10.1 → 6.9 %(2 wt% DA, Fig S15)** = 표면 윤활 치밀화(Liu ACS Energy Lett. 2025 동일 현상) → **우리 DEM 압축 모델의 입자 표면 마찰 파라미터 실측 앵커** |
> 📐 **스케일 사다리 note — *DFT 축 재료비교 아님* (2026-08-19 추가)** [`papers/wang2026_dryprocess_thick_cathode_failure_ncm94.md`]: **Wang & Wang 2026 (JMCA, DOI 10.1039/d6ta04392e) SI Fig S3** 이 **건식 황화물 복합 양극막**(NCM94:LPSCl:VGCF:PTFE = 80:18:1:1)의 **AFM 힘–거리 Young's modulus 를 3점 실측**한다: **3.056 / 2.248 / 1.263 GPa** (평균 ≈2.19, 산포 2.4×). **위 표에 행으로 넣지 않는다** — 이것은 **SE 단결정 탄성상수가 아니라 다상+공극 복합막의 국소 압입 응답**이라 우리 relaxed-ion C_ij 와 *같은 물리량이 아니다*. 그래도 이 축에 기록하는 이유는 **E 사다리의 맨 아래 칸을 실측으로 채우기 때문**이다: **결정 LPSCl (우리 relaxed-ion E_VRH 22.06 / [Deng16] 22.1 / [Torii] 27.4) → thiophosphate 유리 실측 ≈20 ([Famprikis19] ref108) → [Qian26] 통념 "~30" → 건식 *복합막* 실측 1.3–3.1 GPa**. ⇒ 같은 재료계인데 **형태(단결정 → 복합 다공막)만으로 한 자릿수**가 떨어진다. **🔑 우리에게의 뜻**: DEM/MPM 축의 연화된 **E_eff 1.35(DEM)/1.53(MPM) GPa** 가 *임의의 fudge* 가 아니라 **실측 가능한 복합막 강성 밴드 안**에 놓인다는 첫 같은-공정 문헌 근거. ⚠⚠ **금지**: "우리 1.35 가 실측 2.19 와 일치" — 두 값은 **다른 대상**(입자 접촉강성 vs 막 압입)이고, 논문은 **접촉모델·팁반경·ν 를 공개하지 않아** 절대값이 방법 의존이며, **3점 산포가 2.4×** 다. **허용**: *"자릿수·밴드 정합"* 까지. 상세는 DEM 축 `comparison_vs_ours_DEM.md` §C.
| **★★ O 치환의 *상대* 경화 — 우리 `lpsocl` 의 독립 외부 확증**: 그들 O 단독 **Li₆PS₄.₇₅O₀.₂₅Cl (O 1개/52 at, f.u.당 0.25) B₀ 23.66 → 26.48 GPa = +2.82 GPa / +11.9 %** | **[Jung26]** `Fig. 2a` (VASP PBE, Murnaghan, relaxed-ion) | **modelc → lpsocl** (Li₂₇P₅S₂₁OCl₈, O 1개/62 at, f.u.당 0.20) **21.71 → 24.71 GPa = +3.00 GPa / +13.8 %** (`b0-dft-bm3-v1`, `lpsocl_eos_dft_result.json`) | ✅✅ **일치 — 우리 O-도핑 경화 판정의 첫 외부 독립 근거.** 코드(VASP/QE)·모체(Cl 1 / Cl 1.6)·셀(52/62 at)·EOS 형태(Murnaghan/BM)가 다 다른데 **상대 ΔB₀ 가 +12 % vs +14 %** 로 맞는다. 1저자 인용정책(2026-09-18 상대차만)과 같은 결. ⛔ **절대값 병치 금지** — 모체가 다르다. ⚠ 양쪽 다 **B₀′ 를 못 쓴다**(우리 0.5 = 좁은 격자, 그들 미보고) ⇒ **B₀ 만** |
| **B₀ functional/코드 사다리에 PBE(vdW 없음) 칸 추가**: Li₆PS₅Cl **23.66 GPa** | **[Jung26]** `Fig. 2a` (k 3×3×3, 6점 **비대칭** V/V₀ 0.96–1.02) | comp1 **B_VRH 25.51**(relaxed-ion C_ij) · **BM-EOS B₀ 26.23** | **사다리: [Jung26] PBE 23.66 < 우리 PBE 25.51–26.23 < [Deng16] PBEsol 28.7 < [Torii] PBE-D3 34.7.** Δ(우리−Jung) **−10 %** 는 **실질 차이가 아니라 방법 산포** — ① 그들 V₀ ≈1035 Å³(figure-read) vs 우리 1016.6(+1.8 %), ② Murnaghan vs BM3 + **압축 쪽에 4점 몰린 비대칭 격자**, ③ 코드·PAW·k. ⛔ *"우리가 문헌보다 높다"* 류 방향성 주장 금지 |
| **Si 단독 치환 B₀ 23.66 → 27.79 GPa (+17.5 %)** — 우리에게 없는 축 | **[Jung26]** `Fig. 2a` | **우리 Si 도핑 계 없음** | 🆕 **새 정보이나 조건부.** ⛔ **전하보상이 기재되지 않았다** — 논문 식 `Li₆Si₀.₂₅P₀.₇₅S₅Cl` 은 형식전하 **셀당 −1**(실험은 `Li₆.₁` 로 보상하는데 모델은 Li₆ 고정)이라 중성 셀이면 **가전자대 정공 1개**다. figure-read **B₀×V₀ 곱**으로 보면 O 단독은 pristine 대비 **−0.6 %**(= 순수 부피효과)인데 **Si 계만 +12 %** 로 튄다 ⇒ 정공 수축 인공일 가능성. **우리 Nd/O 도핑에도 같은 지적이 올 수 있다 — 전하보상 규약을 명시할 것** |
| ⚠ **AFM 실측 E: 같은 시료가 16.6(QNM) vs 28.6(Oliver–Pharr) GPa = 1.72× 로 갈린다**. LPSiSOCl 은 21.2 / 37.6 GPa, 경도 1.34 → 1.56 GPa, 잔류압입 46.4 → 35.7 nm | **[Jung26]** `Fig. 2b` · `Fig. S6`(⚠ 그림 미보유, 값은 본문 활자) | comp1 **E_VRH 22.06 GPa**(DFT relaxed-ion) | ⚠ **우리 표에 절대값 넣지 않는다.** 그들 두 값이 **우리 DFT 를 사이에 두고 갈린다**(16.6 < 22.06 < 28.6) ⇒ 검증도 반증도 아니다. **팁반경·스프링상수·접촉모델·시료 기공률 전부 미기재**, Oliver–Pharr 는 **ν=0.30 가정**(argyrodite 문헌·우리 값은 0.35–0.37 ⇒ E 가 더 내려간다). `Fig. 2b` 맵은 **컬러바가 10⁰–10² GPa 로그**라 16.6/21.2 를 눈으로 못 가르고, 본문이 근거로 든 **히스토그램이 그 그림에 없다**. ✅ **쓸 수 있는 건 *비율*(+28 % / +31 %) 뿐** — [Ling26] 과 같은 처리 |
| ⛔ **"Si/O 공치환이 골격을 가장 강하게 보강한다" 는 그들 자신의 그림이 안 받친다** — `Fig. 2a` 서열은 **Si 단독 27.79 > 공치환 26.70 > O 단독 26.48 > pristine 23.66** | **[Jung26]** `Fig. 2a` vs 초록·본문 서술 | — | ⚠ **인용 시 서열을 그대로 옮길 것.** 실험이 x=0.1 공치환을 고른 실제 이유는 **σ 와 상순도**(`Table S1`·`Fig. 1b`)이지 B₀ 가 아니다 — 논문이 그 논리를 명시하지 않는다. 부수: **V₀ 가 단일원자 치환에 −11 % 까지 움직이고**(O 단독 919 Å³ < LPSCl 실험부피 958 Å³), **패널 간 E₀ 가 같은 "O 1개 추가"에 −15.31 vs −3.45 eV** 로 ≈12 eV 어긋난다(figure-read, ±0.03). **논문에 V₀/E₀/B₀′ 표가 없어 검증 불가** |
| **기계 ↔ 이온 트레이드오프의 실측 교환비**: B₀ **+12.8 %** · E_AFM **+27.7 %** 를 사는 대가로 **σ 1.63 → 1.23 mS cm⁻¹ = −24.5 %** (x=0.2 −28 %, x=0.3 −60 % + Li₃PO₄/LiCl 2차상) | **[Jung26]** `Table S1` · `Fig. 1b,c` | 우리 실험 σ 없음. lpsocl MD Ea **0.2867 eV**(provisional, `md-ea-multiseed-v1`) vs modelc **0.2235 eV**(canonical, `md-ea-singleseed-anchor-v1`) | ⛔ **우리 Ea 로 이 실험을 설명하지 말 것** — 두 값은 **다른 `comparison_group`** 이라 원장이 직접 순위비교를 금지한다. ✅ 쓸 수 있는 것: **문헌 쪽 교환비(−25 % σ 당 +13 % B₀)를 소환값으로** 인용. ⚠ 논문은 −24.5 %를 *"slightly lower"* 라 쓴다(과소서술) — 율속(0.1–2 C) 무차이는 **이 셀이 전도도 율속이 아니었다**는 뜻이지 σ 손실이 작다는 뜻이 아니다. **Ea 미측정** |
| **B₀ 만 있고 C_ij·G·ν·Zener A 가 없다** | **[Jung26]** Experimental §4.5 | comp1 full 6×6 C_ij(E_VRH 22.06/G_VRH 8.13/ν 0.356/A 1.144) · lpsocl(K 27.82/G 13.58/E 35.04, `elastic-dft-relaxedion-lpsocl-standalone`) · **`modelc_2x` relaxed-ion 진행중(gabia, LOBSTER 뒤로 정지)** | ✅ **우리 공백이 아니라 문헌 공백이다** — 치환 argyrodite 의 *전단*·*이방성* 을 준 논문이 아직 없다. **"O/Cl 이 B 는 올리는데 G 는?"** 이 미답. `modelc_2x` 가 끝나면 그 자리를 우리가 채운다 |
> 차이 원인: relaxed vs clamped-ion, PBE vs PBEsol/D3 → 절대 E/B ±수 GPa. **비교 전 functional·ion-relax 맞출 것.** B/G 연성 결론만 robust. **[Rupp] argyrodite E절대값(92–100)은 outlier — 무시.**
> 🔑🔑 **VACANCY PARADOX — 외부 full-DFT 판정 (2026-06-26, `papers/torii2025_lpscl_mechanical_anisotropy_dft.md`)**: **[Torii]** = 우리 comp1(Li₆PS₅Cl)을 *정면으로* VASP/PBE-D3/**relaxed-ion**/stress-strain Cij로 계산한 유일한 외부 논문 → **그들 E=27.4·G=10.0·C₁₁=47.4·C₄₄=10.4·ν=0.37이 우리 *relaxed-ion* comp1(22.06/8.13/37.67/7.98/0.356)에 *전부* 가깝고(Δ+23~30 %), 우리 *clamped-ion*(52.31/20.12/74.23/18.98/0.300)과는 ~2× 차이.** ⟹ **"clamped-ion이 argyrodite 탄성을 ~2× 과대평가, relaxed-ion이 물리적"이라는 우리 진단이 외부 full-DFT로 독립 확증.** Δ(+25 %)는 *계통적 D3 강성*(전 Cᵢⱼ +23~39 %, C₁₂ 최대→B)일 뿐 relaxed/clamped 류 *질적* 2× 차이 아님 → 판정 robust. **B**: 부피·격자상수 일치(a 10.04≈10.055)이나 절대 B는 Torii VRH 34.7 vs 우리 BM-EOS B0 26.23(+32 %=정의차+D3); **우리 relaxed B_VRH 25.51 ≈ EOS B0 26.23(3 %)** 이므로 functional 맞추면 정합. **A**: Torii(vacancy-free)=1.09 등방 → 우리 "disorder=유일한 Cij 지문" 대조군 외부 고정. **전단**: Torii ε_fracture 0.7 %(Cl→Li₄Cl)=우리 낮은 C₄₄/G의 원자기구(우리 미계산 → 인용). **deck용 1-liner**: "외부 full-DFT(Torii, PBE-D3 relaxed-ion)가 우리 relaxed-ion 값을 ±25 %(=D3)로 재현하고 우리 clamped를 ~2× 거부 → relaxed-ion이 옳다."
> 🧭 **ε∞ ↔ polarizability ↔ modulus 개념 구분 note (`papers/kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md` §9·§12)**: **[Kraft]** 논지 "polarizable anion → soft lattice → σ"의 인과사슬을 우리 두 계산 체인에 정확히 매핑. **(1) "polarizability"의 정체** = Kraft에겐 *입력 변수*(할라이드 전자 분극성 화학 트렌드 α(Cl⁻)<α(Br⁻)<α(I⁻); **Kraft는 α도 ε∞도 측정 안 함**, 트렌드로 라벨만), *측정한 것*은 **기계적 무름**(speed of sound·Debye·C_ij). **(2) 우리 ε∞**(DFPT/ph.x epsil; comp2 ≈3.80, n∞≈1.95) = **전자 유전율 = 전자 분극성의 거시 발현(Clausius–Mossotti)** = Kraft의 *입력 물리량과 같은 것*(우리가 *계산해서 채움*). Br(comp2)>Cl(comp1) 분극성 → comp2 ε∞>comp1 예상 = Kraft 트렌드 방향 정합. **(3) 우리 elastic/Debye/phonon** = **기계적 무름** = Kraft가 *실제로 잰 메커니즘 물리량*. **🔑 핵심**: ε∞(전자)와 modulus(기계)는 *다른* 물리량 — Kraft 논지는 "둘이 *상관*"이지 "같다"가 아님. 인과사슬에서 **ε∞=원인(전자), elastic/Debye=결과(기계)**. **∴ ε∞와 elastic을 *나란히* 돌리는 게 옳음**(중복 아님·상보). **⚠ 완전대응 caveat**: Kraft의 "lattice polarizability"(Li⁺ 지날 때 음이온+골격 *동적* 변형)는 **정적 유전율 ε₀=ε∞+이온(격자)기여**에 더 가까움 → 우리 **ε∞는 전자(clamped-ion) 부분만 = 부분 대리**; E_A·prefactor를 지배하는 *연화 크기*는 ε∞가 아니라 **Debye/phonon/elastic**이 줌(prefactor σ₀ ∝ attempt freq ν₀ ∝ ν_D). "ε∞ 높다 → σ 높다"로 단독 결론 금지 — 무름(elastic/Debye)과 무질서(disorder)가 실제 σ 레버.
> 📌 **[Deng16] 귀속 교정 note (2026-07-28, `papers/deng2016_elastic_superionic_electrolytes_dft.md` §7.1)**: 원문 실물 검증 결과 **"Deng 2016 = SQS"는 거짓** — 논문 전체에 SQS/ATAT/enumeration 언급이 없고, argyrodite는 **"only the 24g sites are occupied" 완전 질서 모델**(전 조성 "end members, ordered" 전략). **Zener A=0.92도 논문에 없음** — 인쇄 PBEsol Cᵢⱼ(39.9/23.1/7.8)에서 유도하면 **0.929≈0.93**(0.92는 절사; [Torii] Table 1 표기 추정). 수치 자체(C/B/G/E/ν)는 [Torii] 재인용과 원문이 **전부 일치** — 틀린 건 SQS 라벨과 A 반올림뿐. **파급**: ① litdb의 LPSCl 탄성 계산은 **전원 ordered**(Deng 24g·Torii·우리 comp1) → A≈1 산포(0.93 vs 1.09 vs 1.14)의 원인 후보는 무질서 처리가 아니라 **functional(PBEsol/PBE-D3/PBE)·Li 배치·절사**; ② 무질서/SQS 탄성 계산은 문헌 공백 → modelc A=1.44(disorder 지문)는 우리 고유 기여로 강화; ③ `kb/concepts/ordered_vs_disordered.md` §6(문헌 지형 표·경계 사례 경고)·`db/properties/elastic.json` `deng2016_reference`("comp1_SQS")·`papers/torii2025…md`(§3.1/§4/§10 "Deng SQS")는 **원문 기준 수정 필요** (Torii 논문 자체의 오인용인지 우리 digest 독해 오류인지는 Torii PDF 재확인 필요 — 현재 미보유).

> ⚙ **Monroe–Newman 주석 (수치 이식 금지 · 축 C)** — **[Miao23]** §4.2.2 가 기준을 **명시 인용**한다: 덴드라이트 억제에는 버퍼층의 **전단탄성률 G ≥ 2 × G(Li)**. 실증 사례 **LiPON G ≈31 GPa vs Li ≈3.4 GPa (≈9배)** → 덴드라이트 미관측. 같은 절이 *"σ_e 가 낮고 **탄성률이 높으면** 덴드라이트가 어렵다"* 로 두 임계 인자를 못박는다. ⚠ **우리 E_VRH(comp1 22.06 / modelc 27.66 GPa, relaxed-ion PBE)로 "Monroe 기준 만족"이라고 말하면 안 된다** — 기준은 **G(shear)**, 우리 값은 **E(Young)** 이고, 리뷰는 relaxed/clamped·functional 구분이 없으며 다결정·GB 도 미포함. G 를 따로 뽑고 다결정 평균을 취해야 성립. 🔀 **후속 리뷰와의 상충**: `fan2026` 은 덴드라이트를 **wedge-opening**(균열 후단 Li 주입)으로 설명하며 **Monroe–Newman 을 언급하지 않고** 기계 지표를 **K_IC 0.2–0.4 MPa·m¹ᐟ²** 로 갈아탄다 → 두 기준이 대체인지 보완인지 미정(리뷰어 코멘트 후보, digest §10④).

> 🧪 **[자체·공저] note (2026-08-19)** [`papers/lee2026_mechanical_halogen_argyrodite_drycoating.md`] —
> Y. Lee 외, **Yonghoon An 제2저자(계산 담당)**, 교신 Jong-Won Lee, *ACS Nano* 2026
> (DOI 10.1021/acsnano.6c09375). **할로겐 치환 아르지로다이트의 기계 물성을 conformal dry coating 관점에서**
> 다루고, 계산 보조로 **MLIP/DFT 계면 W_ad + FEM 충돌 + 기하 coverage 모델**을 쓴다.
> ⚠⚠ **`Fig. 6` 은 우리 계산인데 논문의 Eq. (1) 로 재현되지 않는다** — 식에 **`− α·ΔW_strain` 항이 빠져 있다**
> (α = 1.0, dW = 0.44). **리비전·후속 인용에서 그 식을 그대로 쓰면 안 된다.**
> 이 축(C)에 값으로 편입하지 않는 이유: W_ad 규약이 우리 `adhesion` 계열(z-scan 결합곡선, phase1/v30u)과
> 달라 **같은 표에 놓으면 규약이 섞인다.** 방법·서사 참조용으로만 둔다.


**📎 [Jiang22Se] §C 보강 표 (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_jiang2022_se_doped_lpscl_high_throughput_dft.md` §④.

| 항목 | **[Jiang22Se]** | 우리 | 판정 |
|---|---|---|---|
| Cl 증가 시 **체적탄성률** | 28.63 → **16.16 GPa (−44 %)** | B₀ 26.233 → 21.71 GPa (**−17 %**, 같은 `comparison_group: b0-dft-bm3-v1`) | 🔶 **부호 일치, 크기 2.6배 차.** ⚠ 저들은 **탄성 계산법을 아예 안 밝혔다**(응력-변형? VRH? relaxed vs clamped ion?) ⇒ **다른 양일 수 있다.** 게다가 단일 배열·자유완화 삼사정계 셀(각 87–92°) |
| Cl 증가 시 **Young** | 28.60 → 26.47 GPa (−7 %) | E_VRH 22.06 → 27.66 GPa (+25 %) | ⛔ **비교 금지** — 우리 두 값이 **다른 `comparison_group`** 이다(`…comp1comp2-v1` vs `…modelc-standalone`). 레지스트리 note: *"네 조성을 한 묶음으로 자동 순위화하면 안 된다"* |
| 전단 G / Li 금속 대비 | 10.72 / 10.78 GPa, *"Li 금속의 2배 ⇒ 덴드라이트 억제"* | (VRH G 는 이 표에 안 올린다) | ⚠ 논문 내부 모순: Tatsumisago 를 인용해 *"E 는 작아야 좋다"* 해 놓고 결론은 *"B 가 큰 Li₆PS₅Cl 이 역학적으로 적합"* — 두 기준이 반대 방향인데 정리하지 않는다 |

**📎 [Liu26FIRE] §C 보강 표 (5열 별표) (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_liu2026_ai_ready_finetuning_solid_solid_interfaces.md` §②-b.

| 문헌 | 계 | 문헌값 | 우리값 | 판정 |
|---|---|---|---|---|
| **[Liu26FIRE]** ⚠preprint | **LPSCl 벌크** | **E_MLIP ≈ 26 GPa** (figure-read, `Fig. 4` B) vs **E_AFM ≈ 40 GPa** · **ν 0.34** vs ref 0.37 | **E_VRH(comp1) 22.06 GPa** (DFT relaxed-ion) · modelc 27.66 | 🟠 **우리 DFT(22.1) 와 저쪽 파인튜닝 MLIP(26) 이 서로 가깝고, 저쪽 "실험"(40) 만 둘 다에서 멀다** ⇒ 차이의 주범은 모델이 아니라 **측정량**: AFM 공간평균은 **다결정 펠릿의 기공·입계 + 접촉모델(Hertz/DMT)** 을 타므로 **단결정 DFT C_ij 와 같은 양이 아니다**. ⛔ *"우리 E 가 실험보다 낮다"* 를 이 논문으로 논증 금지. ✅ **실측 앵커는 계속 `lee2026`(AFM-FS, 우리 랩) 이 정본** |
## D. 전자구조 / band gap — *방법 의존, 절대 비교 금지*
| 주장 | 출처 | 우리 | 비고 |
|---|---|---|---|
| ⭕ **독립 그룹 CASTEP-PBE 밴드갭: Li₆PS₅Cl 2.293 eV (간접 Γ→Q) · Li₃PS₄ 2.164 · LLZO 3.982 · LiPON 5.587 eV** (+ Sn/C/Ta 도핑 시 전부 하락: 1.588 / 4.721 / 3.422) | **[Tu27ML]** `Fig. 1` 밴드구조 — **800 dpi 재렌더로 Q 점 CBM 확인**(화살표와 밴드 정합, DOS-threshold 아님) | comp1 **2.066** / modelc **2.099** / +B₂O₃ **1.9671** / LPSOCl **2.2309** eV (fixed-occ nscf 고유값) | ⭕ **차이 0.227 eV = 우리 baseline 의 ±0.2–0.3 eV 흔들림 창 안** ⇒ **method-dependent, real difference 아님.** ✅ 말할 수 있는 최대치: *"독립 그룹이 다른 코드(CASTEP/ultrasoft/380 eV)로 낸 PBE 갭도 2.3 eV 대이고 우리와 같은 구간 = 둘 다 wide-gap 절연체"*. ⛔ *"우리가 0.23 eV 낮다"* 류 방향성 주장 금지 — 코드·PP·컷오프·**무질서 규약(이 논문은 S/Cl 4a·4c 무질서를 한 번도 언급 안 함)** 이 전부 다르다. ★ PDOS(650 dpi figure-read): 총 무게는 **S 가 압도적**(본문 *"dominated by the S atom"* 은 맞다)이나 **E_F 최근접 뾰족 봉우리는 Cl 3p ≈−0.3 eV**(≈41 electrons/eV) — 우리 판정(VBM = S 3p 89.5 %)과 **모순은 아니고 강조점이 다르며, 그 차이가 S/Cl 배열 규약에서 올 수 있다** |
| **PDOS 밴드갭 LPSC 1.78 → LPSCInF 2.75 eV** (PBE) | **[LiInF]** `Fig. 2e,f` | comp1 **2.066** / modelc **2.099** / +B₂O₃ **1.9671** / LPSOCl **2.2309** eV (**fixed-occ nscf VBM/CBM 고유값**) | ⛔ **직접 비교 금지.** ① 그들은 **DOS 문턱 판독**(통상 ~0.3 eV 과소) ② **k-mesh 미기재** ③ 무질서 **단일 배열** ④ 조성 다름 ⑤ **DFT 도핑 In 25 % = 실험의 4–12 배**. **PBE argyrodite 에서 2.75 eV 는 이례적으로 크다** — In³⁺→P⁵⁺ 가 Li 를 2 개 더 넣는데 그림의 E_F 가 VBM 에 붙어 있다. **"둘 다 wide-gap 절연체" 수준까지만 공유** |
| ⚠ **원소분해 PDOS 가 없다** — VBM/CBM character 를 논문이 밝히지 않는다 | **[LiInF]** | comp1/modelc **둘 다 VBM = S 3p (89.5 %)**, 자리분해 mean-3p(−8..0 eV): free-S **−1.14** < B–S −2.15 ≈ PS₄-S −2.23 < Cl −2.99 < O −3.64 | **우리 정보 우위 칸.** 이 논문은 "갭이 넓어졌다"만 말하고 **어느 상태가 어디로 갔는지** 못 말한다 — In 5s·F 2p 의 위치가 미지 |
| PBE gap **LPSCl 1.88 / LiCl 6.22 eV** | [Lu] | comp1 2.066 / modelc **2.099** (PBE) | 무질서·Γ-only k ±0.2–0.3 scatter. LiCl 6.22 = 전자절연 interphase 기준 |
| **LPSCl HSE06 gap 3.92 eV** (mix 0.32) + **분해산물 gap: Li₂S < LiCl, LiAlS₂/MgS 큼**(σ_e 억제 산물) | **[Sundar]** | comp1 2.066 / modelc **2.099** (PBE); sei_products LiCl 6.65 / Li₂S 3.90 | **△ gap 절대값 비교 금지**(PBE vs HSE06+mix 0.32; [Semi] HSE 3.30보다도 높음=mixing 의존). **✓ 분해산물 gap *순서*(LiCl≫Li₂S, wide 산물=절연 interphase)는 재확인** ([Li25]/[Lu]/sei_products와 한 줄). **ZnO 역설**(slab gap 0.4 eV·ZnS 산물 σ_e↓) = 우리 "PBE 과소·slab/disorder 민감 → wide-gap insulator만" 규율의 외부 근거 |
| PBE 2.10→2.62 (In 도핑) | [Ma] | — | In 0.52 eV↑인데 σ_e 1.2×만 변(=defect-controlled) |
| ★★ **PBE gap 2.12 → 2.66 eV (Ta 도핑) + 같은 시료 σ_e 실측 9.7×10⁻⁹ → 1.4×10⁻⁹ S/cm** — **갭이 논거인데 자기 데이터가 그 인과를 부정한다**: 진성 캐리어면 n_i ∝ exp(−E_g/2kT) 이므로 ΔE_g = +0.54 eV 는 **3.4×10⁴배 감소**를 예측하는데 실측은 **6.9배** (우리 계산) | **[Wu26]** `Fig. 2a`(스크리닝) · `Fig. S13`(DC 분극 1 V/1800 s) | comp1 **2.066** / modelc **2.099** / +B₂O₃ 1.9671 / LPSOCl 2.2309 (fixed-occ nscf 고유값) — **[Wu26] 무도핑 2.12 ↔ 우리 modelc 2.099, Δ 0.02 eV** | **⚠ 4자릿수 불일치 = σ_e 는 defect/GB 지배** ([Ma] In 0.52 eV↑↔1.2× 와 **완전 동형, 두 번째 표**). ⇒ **우리 §[E]/[F] "Cl-rich 계면 열화의 원인에서 전자전도도를 배제" 논증의 독립 외부 증거.** gap 2.12 ≈ 2.099 일치는 **우연**(둘 다 PBE·단일 배열·판독법 미기재) — "wide-gap insulator"까지만 |
| ⛔ **[Wu26] 의 15원소 밴드갭 순위표(Mo 0.001 … Ta 2.66 eV)는 인용 불가** | **[Wu26]** `Fig. 2a` · `Fig. S5` | — | **DFT+U·스핀 분극이 SI 에 한 글자도 없다.** Mo(4d)/W(5d)/Ce(**4f**)/Fe(d⁵)/Cr(d³) 는 U·스핀 없이 계산 불가 → 하위 5개는 "갭"이 아니라 금속/4f 오류. Ta·Nb 만 **d⁰·P⁵⁺ 동가**라 우연히 맞다. 게다가 범례가 **`Li_y`** 인데 M 별 y 를 안 준다(figure-read) = **재현 불가**. Fig. S5 k-path 는 **삼사정계** = 대칭 완전 붕괴 |
| gap **1.82→2.41 eV** (CuBr₂ 도핑) + **σ_e 실측 1.02×10⁻⁸→3.35×10⁻⁹ S/cm**(3×↓, CCD와 역상관) | **[Li25]** (PDOS + DC분극) | comp1 2.066 / modelc **2.099** (PBE); σ_e 미측정 | △ **"도핑이 gap 확대→σ_e↓" 방향 일치**(우리 comp1→modelc gap 거의 불변과 대비; Cu/Br이 더 강한 전자구조 변화). **σ_e 3×↓ = gap+0.59 + Cu/Br carrier 복합**(gap만 분리 불가, [Ma]와 같은 주의). gap 절대값(LPSC-P 1.82<우리 2.066)은 functional·k·무질서 미상 → 비교 금지 |
| PBE gap **Cl–I 2.32 > Cl–Br 2.19 eV** (I 치환이 gap을 *넓힘*; Li₅.₅PS₄.₅ClI₀.₅ vs ClBr₀.₅) | **[Rao]** (band structure, **순수 DFT**) | comp1 2.066 / modelc **2.099** (PBE) | △ **"wide-gap insulator" 수준만 정렬** — **🔑 우리계와 가장 직접 비교**(둘 다 PBE·argyrodite). 그들 2.19/2.32 > 우리 2.066/2.099 = 4a/4d 처리·k·total halogen(1.5 vs 1.0/1.6) 차. **⚠ gap 크다고 "I 전자절연/산화안정 우수" 금지** — VBM character 미분석·PBE; [Banik] VBM=S 3p라 **I 5p가 VBM 위로 오면 *오히려* 산화 쉬울 수도**(gap≠산화창). "larger bandgap desirable"은 그들 일반론(dendrite 저항)이지 우리 비교축 아님 |
| PBE 2.45 / **HSE06 3.30** | [Semi] | (우리 PBE 2.07) | PBE는 ~1 eV 과소 → "wide-gap insulator"만 |
| VBM = S 3p (HAXPES + DFT pDOS/COHP) — **자유 S²⁻ + PS₄³⁻ 비결합 S 3p**가 VBM; Cl 3p 깊이·I 5p 엣지(but ESW 무관); CB=P–S 반결합 → 치환은 **gap(CB)만** 변경 | **[Banik]** (Fig 3b·4, Fig S6) | comp1/modelc PDOS VBM=S 3p 96–97%; ICOHP(P–S) −5.94/−6.0; ELF(P–S) 0.946/0.944 | **✓✓ 재현·심화** — Banik COHP가 우리 "VBM=비결합 S 3p"의 *왜*를 외부 확증. **🔑 산화 onset 함의(축 B로): VBM=S → onset S-limited(치환 무관)** |
| **산화 onset ≈ 음이온 p-band(VBM) 깊이**: S 3p(얕음)→LPSCl 2.256 V vs O 2p(깊음)→LLZO **2.88 V (+0.63)** | [Rupp] + **우리 LLZO grand-potential**(`papers/kim2021…md` §LLZO) | comp1 VBM=S 3p, onset 2.256 | **✓ VBM character가 onset 지배** (S²⁻→S⁰ vs O²⁻→peroxide) |
| PS₄ "gap" ~2.0 → MgS₄ ~4.2 eV (도핑이 gap 확대) | [Liu23] | comp1 2.066 ≈ 그들 LPSC ~2.0 (우연) | MP smear 0.2 + PDOS 분리 추정, 엄밀 gap 아님; **MgS₄ 구조 자체 부실(§12b)** |
| **bulk σ_e(실측) = 8.16×10⁻⁹ S/cm** (Mg/F 도핑 시 1.03×10⁻⁹, 8×↓) | [Liu23] (DC분극) | 우리 미측정 | **slide25 σ_e 논의 실측 기준값** |
| **bulk σ_e(실측) = 1.02×10⁻⁸ S/cm**(LPSC-P) → **3.35×10⁻⁹**(CuBr₂ 도핑) | **[Li25]** (DC분극) | 우리 미측정 | **slide25 σ_e 두 번째 실측 anchor**([Liu23]와 같은 ~10⁻⁸–10⁻⁹ S/cm 줄). 도핑이 σ_e↓→CCD↑ 직접 보임(Fig 3b) |
| **bulk σ_e(실측) = 8.75×10⁻⁹ S/cm**(LPSC-P=Li₆PS₅Cl) → **1.49×10⁻⁹**(CuCl 도핑, 최저) | **[Taklu]** (DC분극, 1 V SUS\|SE\|SUS) | 우리 미측정 | **slide25 σ_e 세 번째 실측 anchor** ([Liu23] 8.16e-9·[Li25] 1.02e-8과 같은 ~10⁻⁸–10⁻⁹ S/cm 줄, **모체가 우리 comp1=Li₆PS₅Cl이라 LPSC-P 8.75e-9가 우리 bulk σ_e의 가장 직접적 실측 기준**). **σ_e↔CCD 역상관 직접**(Fig 4b: σ_e 최저 ↔ CCD 3.0 최고)·(P/Cu)S₄ rigid화가 σ_e↓ |
| **분해산물 밴드갭(DFT PDOS): LiCl 6.13 / LiBr 5.07 / Li₂S 3.04 eV** (wide-gap halide가 절연 계면) | **[Li25]** (산물 PDOS) | sei_products.json: **LiCl 6.65 / Li₂S 3.90** (MP); LiBr 없음 | **✓✓ 독립 검증** — 외부 그룹 DFT가 우리 "LiCl≫Li₂S, wide-gap halide=전자절연 SEI" 순서·논리 재현. **LiBr(5.07)은 우리 db에 없던 값**(Br계 도핑 시 추가 가치). [Lu] LiCl 6.22와도 정합 |
| **할라이드-SEI gap 시리즈 LiCl 6.65 / LiBr ~5.07 / LiI ~6 eV** — I-bearing argyrodite 계면 분해산물 = **LiI(LiFePO₄와)·I₂(FePO₄와)**, 저형성E(E_f LiI −1.39 eV/atom) → ΔE_D↓(계면 우호) | **[Rao]** (계면 ΔE_D; **LiI gap은 논문 미계산**) | sei_products.json LiCl 6.65; [Li25] LiBr 5.07; **LiI ~6.4** ([Rupp] "buffer LiI gap 6.4 eV") | **△ 맥락 추가만** — **🔑 LiI도 wide-gap 절연 패밀리**(LiCl 6.65/LiBr 5.07/LiI ~6.4)이나 **[Rao]는 LiI 절연성을 *주장 안 함***(LiI를 *저형성E 계면산물*로만 다룸, gap 미계산=n/a in paper). "Rao가 LiI 절연계면 보였다" 금지. I의 셀링포인트 = 상안정·계면 ΔE_D이지 전자절연 아님. LiI gap anchor는 [Rupp] 6.4 eV(우리 내부)서 옴 |
| sulfide = "wide-band-gap" (구체 LPSCl gap 미제시; buffer LiI gap 6.4 eV) | **[Rupp]** | comp1 2.066 / modelc **2.099** (PBE) | 리뷰 gap 절대값 無 → "wide-gap insulator" 수준만 일치(비교대상 자체 없음) |
| **interphase는 전자절연이어야 self-limiting** (LPO ALD로 LLZO σ_e 10⁻⁸→10⁻⁹ → dendrite 억제) | **[Rupp]** Fig 13·17 | (우리 σ_e 논의 frame) | [Ke]Li₂O·[Lu]LiCl·[Liu23]LiF 절연 interphase 논리의 **landscape 근거** |
| **Li₃PO₄ Eg = 5.77 eV** (UPS IP 8.48 − VBM, *실측*; 실셀 buffer로 LASGTP 환원 보호) + **operando 밴드정렬**(진공준위 절대 VBM/CBM/E_F, 충전 중 운동) | **[Hikima]** Fig 2·3·4 | sei_products.json **Li₃PO₄ 5.73 eV**(MP DFT); 우리 DFT 절대 VBM=정렬 미보정(비엄밀)·slab-WF 포기 | **✓✓✓ Li₃PO₄ Eg 5.77≈5.73 (Δ0.04 eV) = wide-gap 절연 buffer/SEI 산물의 *외부 독립 실측 앵커*** (Nd cascade·[Rupp] LPO ALD "전자차단 buffer" 논리 실측 근거; 실셀이 Li₃PO₄를 실제 buffer로 씀). **+ operando 밴드정렬(UPS+LEIPS, 진공준위 절대)이 우리 DFT 절대-VBM 비엄밀·slab-WF 포기의 *실험 해법***. ⚠ **LASGTP Eg 4.09는 oxide SE라 우리 sulfide 2.07과 *수치* 비교 금지**([Rupp] "oxide wide-gap·sulfide 좁은 gap" 정렬만) |
| **KS gap = σ_e *게이트*(상한-σ_e 보증)로만 — 절대값 비교 금지 철학의 HT 원조** — E_gap≥1 eV 게이트: 진성 반도체 근사(eq 1, Si 파라미터)로 gap 0.5 eV→σ_e 0.61·1.12→4×10⁻⁶·2 eV→1.8×10⁻¹³ S/cm 스케일 감각 제시 + **"semi-local DFT gap 2배+ 과소(Chan–Ceder ref 24)" 명시** → KS gap을 순위/절대값이 아니라 **전자절연 게이트**로만 사용(12,831종 전수) | **[Sendek17]** (MP KS gap; `papers/sendek2017_ml_screening_12k_conductors.md`) | comp1 2.066/modelc 2.099 eV(PBE fixed-occ nscf) — "wide-gap insulator 수준만 비교" 규율 | **✓ 철학 동일**([Xiao19] Eg>0.5 하한 게이트와 같은 줄) — cross-DB KS gap은 게이트·수준 판정 전용. 우리 조성은 그들 게이트(≥1 eV) 통과 체급. ⚠ 그들 E_gap 수치(Table 3: LiCl 6.25·Li₃ErCl₆ 5.211 등)는 MP-2016 세대 GGA — 우리 sei_products(LiCl 6.65)와 혼용 금지(같은 "wide-gap halide" 결만) |
| **HSE DOS: gap 순서 O>S>Se + VBM·CBM 모두 음이온 상태(M 무관)** — 조성족 관찰, gap 수치 미제시(LGPS 3.6 eV는 Mo2012 소환값); 트렌드 기원 = 음이온 p-준위가 주기율표 아래로 상승 | **[Ong13]** (HSE, non-spin) | comp1/modelc PDOS **VBM=S 3p 96–97%**; PBE 2.066/2.099 | **✓ [Banik] "VBM=S 3p가 onset을 pin"의 2013 조성족 조상** (단 자리분해·COHP 없음 — 조성 수준). gap 절대값 비교 원리적 불가(그들 수치 없음 + HSE vs 우리 PBE) → "wide-gap + 음이온 밴드엣지" 수준만. **"gap=창 상한≠onset" 명시가 이 논문부터** — [Rupp] "음이온 p-band 깊이=onset 지배" 행의 전사 |
| **"electronic localization"(ELF/PDOS d–p 혼성+Madelung)으로 σ_e 4×↓·계면 안정 설명** — Y-4d/S-3p 혼성이 S 전자 국재화→Li→S 전자전달 억제 주장. Madelung PS₄ −166.51 vs YS₄ −175.07 eV/atom(LOBSTER/Glasser) | **[WangYO]** Fig 5 | comp1 2.066/modelc 2.099 eV(PBE fixed-occ nscf); 그들 gap 미보고 | **△ 서사 과잉**: ① ELF 국재화="Y–S가 P–S보다 이온성" 교과서 사실의 재명명 ② Madelung은 형식전하 다른 유닛(PS₄³⁻ vs YS₄⁵⁻) 비교 ③ σ_e 4×↓와 벌크 혼성의 인과 다리 없음(σ_e는 결함 지배) + **베이스라인 6.33e-7 S/cm가 [Adeli]3e-9·[Taklu]8.75e-9·[Yang25]2.59e-9 대비 60–200×** ④ COHP/ICOHP 계산 명시 후 미제시(P–S 공유결합이 더 강하게 나왔을 개연성). gap·국재화 절대치 이식 금지 |
> 인사이트: ① **모델 간 gap scatter(1.88 vs 2.10)는 σ_e 차이를 설명 못 함** — [Ma]는 gap +0.52인데 σ_e 1.2×만(=defect/carrier 지배, slide25 틀). ② 단, **큰 전자구조 변화(도핑)는 σ_e를 바꿈** — [Liu23]는 Mg/F로 σ_e 8×↓(gap 확대 + LiF + carrier 변화 복합, gap만 분리 불가). → "작은 모델 scatter ≠ σ_e / 큰 도핑 변화 = σ_e 가능", 두 경우 구분.
>
> 📐 **방법론 주석 (수치 비교 아님)** — `[EXTERNAL·비-argyrodite]` **[Spencer22]** (`papers/spencer2022_review_tco_band_structure_oxides.md` §15, 본문 실물 검증 2026-08-03). 산화물 리뷰라 **이 축 표에 수치 행을 넣지 않는다**. 다만 이 축의 규율 자체를 지지하는 외부 선례 4건: ① **추출 컨벤션이 갭을 만든다** — β-Ga₂O₃ 동일 결정에서 *흡수 onset* vs *타원계측(엑시톤 포함)* 이 방향별 **+0.595 / +0.815 / +0.93 eV** 계통 차(Table LV) = 우리 "**DOS-threshold 판독 금지, fixed-occ nscf VBM/CBM 고유값만**"(~0.3 eV 과소) 규율의 **동형 외부 판례**. ② **하이브리드 갭은 자유 파라미터의 단조함수** — CuO 에서 GGA+U 의 **U=5/7/9 → 0.91 / 1.48 / 2.11 eV**, 리뷰가 "실험에 가까워질 때까지 U 를 올린다"는 절차를 그대로 기술 → 위 표의 "[Sundar] HSE06 mix 0.32 / [Semi] HSE 3.30 = mixing 의존이라 절대값 비교 금지" 규율의 최강 근거. ③ **피팅 모델의 자유도 배분도 갭을 움직인다** — β-Ga₂O₃ 3전이에서 결합에너지를 *이방적으로 자유롭게* 둔 Mock(120/230/180 meV)과 *270 meV 하나로 고정*한 Sturm 이 같은 물질에서 Eg 를 0.1 eV 단위로 다르게 냄. ④ **결정 갭은 절연성의 상한일 뿐** — α-Al₂O₃ 벌크 8.8–9.9 eV 가 **ALD 비정질 막에선 6.2–6.8**, γ-Al₂O₃ 는 벌크 8.7 → **박막 2.5 eV**(갭 내 결함준위). → 우리 `sei_products.json`(LiCl 6.65 / Li₃PO₄ 5.73 / Li₂S 3.90, 전부 **MP 결정 DFT**)로 "wide-gap 산물 = 전자절연 interphase"를 말할 때, 실제 SEI 는 비정질·결함투성이라는 **상한 단서**를 함께 붙일 것. ⚠ 이 리뷰의 **β-Ga₂O₃ ε∞ 는 인용 금지**(Ref 44 하나에서 Table VII/XII/LIV 세 값이 서로 다름 — [Kraft] ε∞ 체인엔 Schubert APL 2016 원문 사용).

> 🧪 **개념 프레임워크 주석 (수치 비교 아님 · 축 D/B 공통)** — `[EXTERNAL·비-argyrodite·비-배터리]` **[Mulks24]** (`papers/mulks2024_hard_soft_electrons_holes.md`, Chem 10, 2724–2744, 2024). **분자 유기화학 논문이라 이 축 표에 수치 행을 넣지 않는다** (σ·Ea·ESW·C_ij·band gap 이 논문에 하나도 없음). 보관·참조 이유 셋:
> **① 우리 규율의 외부 판례(축 D 방법론)** — 저자 자신의 감도 시험(SI Table S2, cyanide CN⁻)에서 **범함수를 double-hybrid(DSD-BLYP-D3BJ) → PBE 로 바꾸면 축약 전자기술자(EHI) 크기가 41 % 축소**(HF 22 %·B3LYP 34 %)되지만 **부호(soft/hard 배정)는 4개 범함수 모두 불변**. 기저 의존은 상대적으로 관대(6-31G* 13 %, def2-TZVP 2.6 % vs def2-QZVPP). → **"semi-local DFT 로 얻은 전자구조 기술자는 순위·부호만 인용, 절대값 비교 금지"** 라는 우리 규율의 *동형 외부 판례*이며, 같은 축의 [Spencer22] 밴드갭 판례(추출 컨벤션·U 값·피팅 자유도가 갭을 움직임)와 나란히 놓인다. 덧붙여 **전하 분할 스킴 민감성**: 같은 SI(Tables S4–S5)에서 **pyridine 의 "가장 soft 한 원자"가 Hirshfeld 에서는 N, Mulliken 에서는 C2 로 바뀐다** → 우리가 Bader 로 무언가를 축약할 때 **분할 스킴 자체가 결론을 바꿀 수 있다**는 경고(우리 Bader 는 세 번째 스킴이라 자체 검증 필요).
> **①-b ★ 2026-08-06 SI 실물 3차 검증(§14c) — 판례는 살고, 인용 조건이 하나 붙는다.** SI 실물(사용자 분류 폴더 `DFT`, 업로드 `53. Sup3)` 82 pp = 본문+SI 중복본)로 SI 표를 기계 전수 검산했다. **판례의 심장인 Table S2 는 전부 실물과 일치**한다 — PBE **41.2 %** · HF **21.7 %** · B3LYP **33.8 %** 축소, **부호는 4범함수 불변**. 기저 13.2 %(6-31G\*)도 일치. Tables S1·S2 의 상대차 열은 규약 `Δ = ref − X, rel = Δ/ref` 로 **5행 전부 소수 6자리까지 재현**된다. → **"순위·부호만 인용" 판례는 그대로 선다.** ⚠ **다만 같은 SI 의 두 표는 신뢰하면 안 된다**: **(i) Table S6(용매)** — 본문이 "O **+8 %**, S **+2 %** 로 solvation 영향이 작다"고 쓰는데, 유일하게 공개된 기체상 값(Table S7)과 대조하면 실제는 **O +17 % / S +4 %** 로 **약 2배**다(S6 의 rel 열만 S1/S2 규약으로 재현되지 않음 = 미공개 기준 run). 우리가 "용매 효과는 작더라"를 이 논문 근거로 쓸 일이 생기면 **반드시 두 값을 병기**한다. **(ii) Table S3(기하 선택)** — Δ 열 3행 + 셀 2개가 틀렸고(**14′ O·16′ O 는 부호까지 반대**), 인쇄된 표만 읽으면 저자의 "EHI 순서 불변" 결론이 16′ 에서 깨져 보인다. **SI 원표(S23/S25/S32/S33)로 고쳐 계산하면 순서는 그대로** — **결론은 살고 표가 틀렸다.** → **이 논문에서 수치를 가져올 땐 인쇄된 요약표(본문 Table 1·SI Tables S3/S6)가 아니라 원자별 원표(SI Tables S7–S33)를 1차 출처로 쓴다** (§14b 의 Table 1 오타 4건과 **같은 종류의 흠이 SI 에도 있다**는 것이 이번 검증의 요지).
> **② 개념 어휘(축 B 산화 서사)** — Mulks 의 핵심 주장은 **"전자 하나를 빼는 것(SET·라디칼)과 전자 쌍을 빼는 것(2전자 화학)은 *다른 자리*를 고른다"**(Fig. 6 benzo[a]pyrene: **Pt 전극에서의 1전자 산화 = hard 채널** → C6 라디칼 양이온(ρ_α=0.26) vs **효소 O₂ 에폭시화 = soft 채널** → C7/C8). 우리 축① 는 **grand-potential(=2e⁻·열역학·닫힌 고체 hull, onset 2.256 V, S²⁻-limited)** 로 보고, 첫 홀이 앉는 자리는 **site-PDOS/⟨3p⟩ centroid·ICOHP** 로 본다 — 이 둘이 **원리상 다른 질문**이라는 것을 분자계에서 명시적으로 보여준 문헌. **어휘·프레이밍만 차용, 수치 전이 0.**
> **③ 리뷰 심사 근거** — `papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md` §3.1 ref [80] 의 원전. **판정: 무기 고체·황화물에 적용된 선례가 이 논문 안에 0건**(전부 이산 분자/이온/유기금속·기체상·ORCA 분자코드; 유일한 결정 유래 종 27 조차 *"simplification of the structure in the solid state"* 로 분자 축소; 주기계 Fukui 는 ref [29] Cerón 2020 로 **인용만**), **정량 예측 모델도 아직 아님**(저자 명시 *"Further studies are needed to establish quantitative relationships"*; 적용범위를 **FMO 지배·early TS** 로 자기제한 — 우리 관심 반응인 **가수분해(P–S 절단, late TS + 표면 + 양성자 이동)** 는 저자가 "안 된다"고 한 부류). ⚠ **EHR/EHI 에 대응하는 우리 관측량은 없다** — 이식하려면 하전 슈퍼셀 N±1/N±2 + 유한크기(Makov–Payne/FNV) 보정 + polaron 국재화 통제 + Bader 축약 자체검증의 4겹 신규 작업이 필요하므로 현 우선순위에서 **개념 인용에 그친다**. **"HSEH 로 황화물 가수분해를 설명한다"는 문장은 우리가 먼저 쓰지 않는다** (우리도 가수분해를 계산한 적 없고, 그 논문도 하지 않았다).

> 🔤 **용어 규율 주석 (수치 비교 아님 · 축 D)** — **[Miao23]** 은 고체 황화물 SE 의 밴드엣지를 **HOMO/LUMO**(분자 용어)로 부른다(`Fig. 4c` + 본문 10회). 고체는 **VBM/CBM** 이며 밴드폭·상태밀도가 있다. 단일 준위 만화는 (i) **무질서로 밴드엣지가 흔들리는 효과** (ii) 산화가 특정 **자리**에서 먼저 일어나는 효과를 원리적으로 표현할 수 없다 — 우리 자리분해 mean-3p(**free-S −1.14 < B–S −2.15 ≈ PS₄-S −2.23 < Cl −2.99 eV**)가 정확히 그 자리를 채운다. 🔑 **심사 함의**: `fan2026` §4.1.3 의 HOMO 용법은 오타가 아니라 **이 2023 리뷰에서 확립된 그룹 관례**다 → 리뷰어 노트 **B2** 는 *"틀렸다"* 가 아니라 *"고체 절에서는 VBM/CBM 으로 쓰고, 분자 유래 틀을 쓸 때 그 사실을 한 번 명시해 달라"* 로 써야 한다.


**📎 [Jiang22Se] §D 보강 표 (2026-09-13 병합)**
> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_jiang2022_se_doped_lpscl_high_throughput_dft.md` §④.

| 항목 | **[Jiang22Se]** | 우리 | 판정 |
|---|---|---|---|
| PBE 갭 (밴드 고유값) | Li₆PS₅Cl **2.16** · Li₅.₅PS₄.₅Cl₁.₅ **1.99 eV** (`Fig. 1c,d`, E_F=VBM) | comp1 **2.066** · modelc **2.099 eV**(⚠ `method_integrity_flag` 미해소) | 🔶 **절대값 0.09–0.11 eV 차 = 방법·셀·배열 잡음 안.** **Cl 증가 시 부호가 반대**(저들 −0.17, 우리 +0.033)지만 **둘 다 우리 baseline 이 정한 ±0.2–0.3 eV 창 안** ⇒ **"둘 다 2 eV 급 wide-gap" 까지만.** ✅ 방법 종류는 같다(DOS-threshold 아님) |
| **★ Se 가 갭을 1 eV 깎는다** | Li₆ 계열 2.16 → **1.14** (x=4, **−1.02 eV**) · Li₅.₅ 계열 1.99 → **1.22** (x=3, −0.77 eV) | 우리 무질서/방법 잡음 ±0.2–0.3 eV | ✅ **잡음의 3–4배 = 실질 효과로 읽어도 된다.** ⇒ **우리 도펀트 스크리닝의 "전자절연 유지" 단(S4)에 문턱을 걸 실물 근거.** 논문은 이 함의를 **전혀 다루지 않는다**(σ_e·ESW·환원 전부 없음) — 우리가 다루면 차별점 |
| VBM 성격 | `Fig. 5a`: Li₅.₅PS₄.₅Cl₁.₅ 의 **VBM = S 압도적**, Cl·Li 미미. CB 하단 S/P 혼합, Li 는 5 eV 위 | modelc PDOS v2: **VBM = S 3p (1.84)**, CBM = S 3p(반결합)+P 3s, **Li 무시가능** | ✅✅ **다른 코드·다른 셀·다른 배열에서 같은 그림.** **[Banik]**(VBM=자유 S²⁻+PS₄ 비결합 S 3p)·**[WangYO]** 와 함께 3중 확증 |
| Bader (Li) | Li₆PS₅Cl 0.856 → Li₅.₅PS₄.₅Cl₁.₅ **0.864 (+0.008)**. Se 4개 넣으면 0.856→0.853 (**0.003 \|e\|**) | v2: comp1 0.877 → modelc **0.883 (+0.006)** | ✅ **Cl-rich 가 Li 를 더 이온적으로 만든다 — 방향·크기 일치.** ⛔ 다만 **저들이 0.003 \|e\| 를 "Coulomb 인력 약화" 근거로 쓴 것은 인용 금지**(Bader 잡음 수준) |
## E. 환원 / 음극(Li 금속) 계면 — **⚠ Cl-rich 유불리 문헌 충돌 (자리 점유가 변수)**
| 주장 | 출처 | 우리 | 일치 |
|---|---|---|---|
| **E 환원 산물의 *역할* — 🔴 우리 원장과 충돌** | `sei_products.json`: **Li₃P gap 0.70 eV = `conductor-LEAK`** (무도핑 음극 누설 산물, O 도입이 Li₂O 로 대체) · Li₂S 3.90 eV `marginal` · LiCl 6.65 `insulator` | **[Xiao20Rev]** Li₃PO₄/Li → **Li₃P + Li₂O** 이고 *"**These reaction products are passivating** and can enable the stable cycling of Li symmetric cells"*(ref.222 XPS 확인); LiPON/Li → Li₃P+Li₂O+Li₃N 이 *"not only **block electron conduction** but also permit Li-ion diffusion"*(ref.73,174,175). Li₂S 는 **Li-안정 이원상 = SEI 후보**로 분류 | 🔴 **같은 상을 반대로 읽는다.** 둘 다 성립 가능 — 부동태 여부는 밴드갭만이 아니라 **연속성·두께·이웃 상**에 달렸다. ⇒ **우리 문장 "Li₃P 는 전자를 샌다" 에 조건절을 달아야 한다**(단독 상 · 연속층 여부). ⛔ 무조건문으로 쓰면 이 리뷰와 정면 충돌 · **[2026-09-13 보강]** `[Li26FDI]` 가 고른 대체재 **Li₃N 을 우리 표에 등재했다**: MP 최소 E_hull 항목 **α P6/mmm 0.984 eV**(mp-2251), β P6₃/mmc **1.218**(mp-2341) — **둘 다 2 eV 아래라 다형을 어느 쪽으로 잡아도 우리 기준 `conductor-LEAK`** 다 (그 논문 Fig.1g figure-read ≈1.1 eV 가 둘 사이). ⇒ **그들의 Li₃N 대체는 우리 전자누설 기준으로는 개선이 아니다** — 이는 그들이 틀렸다는 뜻이 아니라 **다른 축(이온수송)을 말하고 있다**는 읽기를 뒷받침한다. ⛔ 이 조회는 ①우리 vs ②`[Xiao20Rev]` 문헌 논쟁을 끝내지 **못한다** — 부동태는 갭만으로 안 정해진다(연속성·두께·이웃 상)는 그쪽 반론에 답한 것이 아니다 |
| **★ LPSCl 첫 환원 단계 실측 — dQ/dV 피크 1.15 V(LPSCl) · 1.3 V(Li₃PS₄₊ₙ) · LPS/C 는 LPSCl/C 보다 높은 전위에서 환원(S12)**; 환원식 `Li₆PS₅Cl + Li⁺/e⁻ → Li₂S + Li₄PS₄ + LiCl` (Q_red 100–115 mAh g⁻¹, 1–3 V 창, 1 V 컷오프) | **[Cronk26]** `Fig. 3c`·`Fig. S12`·p6 | 우리 comp1 hull 계단 **1.24 V** 단계(+5 Li·P) · 0 V 종단 `Li₃P + 5Li₂S + LiCl` | ✓ **첫 환원 전위 0.1 V 이내 정합(1.15–1.3 vs 1.24)·산물(Li₂S + LiCl + Li-rich 티오포스페이트) 정합**. ⚠ 방법 다름(실측 kinetic vs 0 K hull); 그들은 1 V 컷오프라 Li₃P 단계 미관측 |
| **★★ "Li₂S SEI 는 Li 가 잘 통한다" 의 문헌 근거 실체 = *얇은 층 관통* CI-NEB 0.22 eV (**벌크가 아니다**)** — VASP/PBE CI-NEB 로 **여분 Li 한 개가 Li₂S 슬랩을 위→아래로 뚫는 6단 경로** = **0.22 eV**, 같은 방식의 LiF 층 = **0.67 eV**. 본문이 층을 고른 이유를 자인: *"**bulk** Li₂S shows **low** Li ion conductivity … the **nanoscale** Li₂S SEI exhibits **high** … **For these reasons**"* | **[Lai20]** `Fig. 3e`·`Fig. 3f`·`Fig. S11` (← **[Liu24SbO]** ref [30b] 의 원출처) | 우리 `db/properties/sei_neb.json` `v2/li2s` = **0.305 eV** · 벌크 반형석 **3×3×3**(λ₁ 12.1 Å) · **V_Li⁻ + jellium (q = −1)** · **최근접 c→c 단일홉 2.8526 Å** · 7 images · QE · `scientific_status: provisional_single_cell` · `absolute_citable: false` | ⛔ **비교 불가 — 값 대 값 표를 만들지 않는다.** 다섯 축 중 **①셀**(슬랩+진공 20 Å, 크기 미기재 ↔ 벌크 주기셀) **②전하규약**(⛔ 한 줄도 없음, figure-read 로 **여분 Li = 침입형·중성 추정** ↔ **하전 공공 q=−1**) **③홉정의**(막 관통 다중홉 ↔ 격자 내 단일홉) 가 어긋난다. ④CI 는 양쪽 다지만 **이미지 수 미기재**(figure-read 7점)·**힘 임계 0.05 vs 0.01 eV/Å = 5배 느슨** ⑤**PBE 만 공통**(VASP/PAW ↔ QE). **⇒ 이 논문은 우리 0.305 에 대해 반증도 지지도 아니다** |
| **↳ 그 대신 *진짜 문헌 짝*을 이 논문이 가리켜 준다** — [Lai20] `Fig. S11` 은 **"Li₂S"(벌크, 문헌)** 막대와 **"Li₂S layer"(자기값 0.22)** 막대를 **분리해** 그렸고, 벌크 쪽 출처가 SI ref **[27] Moradabadi & Kaghazchi, *Appl. Phys. Lett.* 2016, 108, 213906 — "Thermodynamics and kinetics of **defects in Li₂S**"** (**figure-read Cal. ≈0.45 eV** / Exp. ≈0.74 eV, ref [28] Lin/Dudney/Liang *ACS Nano* 2013) | **[Lai20]** `Fig. S11` **figure-read** (막대 누적/겹침 규칙 **미기재** ⇒ 겹침으로 읽었다, **잠정**) | 우리 `v2/li2s` 0.305 eV — **결함 매개 홉**이라 [27] 과 *같은 종류의 양*일 가능성이 있다 | ⚠ **다음 할 일**: [27] 원문 확보 → **전하 규약·셀 크기** 확인 후 다섯 축 재대조. ⛔ 그 전까지 **≈0.45 를 우리 값과 나란히 놓지 않는다**(figure-read 이고 원문 미확인) |
| **★ SEI 상 *선택성* 을 계면 형성에너지 부호·크기로 서열화한다 — Li\|Li₂S 가 Li\|LiF 보다 4–5배 더 음수** — 맨 Li 표면 γ 는 전부 **양수**(Li(100)/(110)/(211) = **0.47 / 0.50 / 0.55 J m⁻²**) 인데 계면은 전부 **음수**: Li\|LiF **−0.084 / −0.078 / −0.096**, **Li\|Li₂S −0.39 / −0.29 / −0.44 J m⁻²**. 정의 `γ_ie = [E_A\|B − (E_A + E_B)] / S` (계면 1개라 2 로 안 나눔; 표면은 `γ_se = ΔE/2S`) | **[Lai20]** `Table 1` · `Fig. 4`(Li(hkl)\|LiF(200) / Li(hkl)\|Li₂S(111) 6모델) | 우리 `interface_reactivity`(grand-potential) 는 **어떤 상이 생기나**까지만 답하고 **어느 상이 먼저 깔리나**는 답하지 않는다 | ✅ **방법 이식 가치 있음** — 값싼 정량 서열화 경로. ⚠ 단 γ_ie<0 은 *"그 상이 **이미 존재할 때**"* 의 조건부이고 **그 상이 생기는 반응이 자발적이라는 뜻이 아니다**(논문이 이 구분을 흐린다). ⛔ J m⁻² 값을 우리 eV 단위 형성에너지와 같은 표에 넣지 말 것 |
| **★ Li 금속 대신 a-Li_xSi 를 쓰면 PS₄³⁻ 붕괴가 억제된다 — 그리고 Si 를 넣을수록 더 억제된다** — 298 K AIMD 배위수(80 ps): **순수 Li/LPSCl 은 P–S 가 2.4 → 0.6 으로 무너지고 Li–P 4 → 7.4 · Li–S 4.6 → 5.8 로 신생**(= PS₄³⁻ 해체). **a-Li₄.₄₀Si 는 P–S 3.05 → 2.15**, **a-Li₀.₅₀Si 는 3.7 에서 변화 없음**. **Li–Cl 은 전 조성에서 진동만 하고 추세가 없다**(= Cl 은 반응에 안 낀다) | **[Wang26IF]** `Fig. 8`(9쌍 × 2계면 × 7계) · 열역학 쪽은 `Fig. 5`(Si 많을수록 반응에너지 덜 음수) | 우리는 음극쪽 계산을 안 한다(축 E 는 문헌 위주). ⇒ **직접 대응 없음** | ⭕ **기록·이식 후보.** 🔑 **트레이드오프가 논문 안에서 갈라져 있다** — 열역학은 *Si 많을수록 안정*, kinetics 는 *Si 많을수록 느림*(bulk Ea 0.26 → 0.42 eV, σ 8.9 → 0.3 mS/cm figure-read) ⇒ **최적이 중간(x≈2.33–3.25)** 인데 논문은 이 결론을 안 쓴다. ⚠ **개념적 구멍**: a-Li_xSi 의 x 는 **SOC 그 자체**(충방전 중 0↔4.4 왕복)인데 논문은 x 를 독립 설계변수처럼 다룬다. ⛔ **배위수 절대값 인용 금지** — t=0 의 P–S 가 3.0–3.7(온전한 PS₄³⁻ 면 4)이고 **컷오프가 SI 어디에도 없다**. **변화량만** 쓴다. ⛔ *"Li–Si 배위수 4~9"* 는 **Li₀.₅₀Si(≈2.6)를 뺀 서술**. ⛔ 계면상 **σ 27.2 mS/cm** 은 이 논문 값이 아니라 **ref 60 소환값**(공저 K. Wang, 자기인용 가능성)이고 같은 문단의 **ref 61(실험)은 반대 방향** |
| **표면 poly(sulfate) 막이 CCD 를 1.0 → 1.6 mA cm⁻² 로 올린다 (1.6×)** — Li\|SE\|Li 대칭셀, **10 MPa**, 1 h 계단. figure-read: bare 는 ≈10.5 h(≈1.0–1.2 mA cm⁻² 단계), 개질은 ≈16 h(≈1.6–1.8 단계)에서 전압 붕괴 | **[Deng26PS]** `Fig. S12` · 🔴 **y축 라벨 오류**(*Specific capacity (mAh g⁻¹)* 로 인쇄돼 있으나 값 범위(−0.06~+0.05)와 실험 종류상 **Voltage (V)** 여야 함) | ⛔ **우리 축에 CCD 가 없다**(탄성 E_VRH 22.06/27.66 GPa 는 다른 양 — 같은 칸에 넣지 않는다). 📎 **[Taklu21] CCD 0.75→3.0** · **[Nd–O] 2.29→6.62 mA cm⁻²** 와 **같은 지표의 3번째 점**이지만 **셀 형상·압력·계단폭이 제각각이라 절대값 비교 금지**. ⚠⚠ **결정적 단서: 이 CCD 개선은 실제 풀셀에서 쓰이지 않는다** — 풀셀은 **이층 펠릿(LiIn ‖ LPSC 70 mg ‖ PS-LPSC 30 mg ‖ 양극)** 이라 **음극쪽은 두 셀 다 맨 LPSC** 다(SI p.2) |
| **Nd–O 공도핑 → CCD 2.29→6.62 mA/cm²·대칭셀 2000 h(15→20 mV)·사이클 후 SEI = Li₂O(528.5 eV)+LiCl+**Li₂S/Li₃P 억제** + "Li–Nd alloy"(XPS 995 eV 소피크, "plausible" 자인)** — 계면 모식도(Fig 7f)는 본문 스스로 "rational speculation" | **[Xu26NdO]** Fig. 3·Fig. 7 (exp; 사이클 후 XPS 시료준비 미기술) | **Li₂O·LiCl·Li₃P-대체 3항목 = 우리 sei_products.json 서사의 실험판**(O-유래 절연상 Li₂O 5.24/Li₃PO₄ 5.73 eV가 전도성 Li₃P 0.70 대체 = 전자누출 차단). **"Li–Nd alloy"는 우리 staircase 산물에 없고 Li–Nd 이원계 화합물 미보고 → mp-api hull 판정(P2, 수 분)으로 지지/반박 가능**; 금속상 함유 계면의 "전자절연" 주장은 불연속 분산일 때만 성립(형상 증거 없음) | **✓(산물 3종)·✗검증표적(alloy)** |
| **★ 환원 한계 = (비이동) 양이온의 전자친화도이며, 그 값이 *결합 상태에 좌우된다*** — *"a phosphorus atom will be **reduced more easily if weakly bonded to sulfur** compared with when **strongly bonded to oxygen**, as exemplified by the increased stability of **Li₃PO₄ compared with Li₃PS₄**"*; 나아가 **환원 안정성 ↔ 폴리음이온 단위의 결합 강성(bond stiffness)** 이 LISICON 계열에서 **실험적으로 상관**(ref 31 = Muy, INS 포논 밴드센터) | **[Famprikis19]** §Electrochemical stability (ref 65 = [Richards16]) | 우리 환원 한계 **1.242 V** / OCV 1.717 V (grand-potential); O-도핑 라인 **LPSOCl**(gap 2.2309)·**+B₂O₃**; ICOHP(Li–Cl) comp1 −1.86 / modelc −2.10 | **✅ 우리 O-도핑·B₂O₃ 전략의 물리 근거가 리뷰급 문장으로 있다**(O 가 P 결합을 강화 → 환원 저항↑). ⚠ **직결 인용 금지 지점**: 우리 ICOHP 는 **Li–X 결합**이고 리뷰가 말하는 것은 **폴리음이온 내부(P–S / P–O) 결합 강성** — **다른 결합이다.** 대응시키려면 **P–S·B–S·P–O ICOHP 를 따로 뽑아야** 한다(H-리스트). [Fan26] 의 B–S −2.15 가 이 칸의 유일한 소환 대응값 |
| **Li₃PS₄ 의 Li 금속 환원 경로 2단계** (Eq.5): `2Li₃PᵛS₄ + 2e⁻ + 2Li⁺ ↔ **Li₄P₂ᴵⱽS₆** + 2Li₂S` → `Li₄P₂S₆ + 14e⁻ + 14Li⁺ → **2Li₃P + 6Li₂S**`; **부분 가역** 사례 존재(Li₁₀GeP₂S₁₂ 단일물질 셀, ref 82) | **[Famprikis19]** Eq.(5) (refs 65,79–81) | 우리 0 V 분해식 `Li₃P + 5 Li₂S + LiCl` | ✅ **최종 산물 일치**(Li₃P + Li₂S). 리뷰는 **중간체 Li₄P₂S₆** 를 명시 — 우리 grand-potential 은 전압 스텝별 산물을 주므로 **중간 단계 대조 가능**. ⚠ 리뷰에는 Cl 항이 없다(Li₃PS₄ 기준) |
| **계면 3시나리오 중 "속도론적 안정화" 의 교과서 예 = LiPON** — Li₃PO₄ + Li₃N 으로 분해되어 **nm 급·전기화학적 안정·이온전도성** 계면상 형성 → 분해가 배터리 성능에 **무시할 수준**. **최악 = MCI**(전자·이온 둘 다 통과 → 무한 성장 → 단락) | **[Famprikis19]** `Fig. 5b` (ref 94) | 우리 SEI 축(`sei_products.json`, B₂O₃·Nd) | ✅ **우리 SEI 목표의 판정 기준**: "분해를 막는다"가 아니라 **"이온전도 O · 전자절연 O 인 유한두께 계면상을 만든다"**. [Miao23] F2 분류(안정/MCI/passivated)의 원형이 여기다 |
| **InF₃ 공도핑 → CCD 1.0 → 2.5 mA cm⁻² · 대칭셀 2000 h@0.5 / 1000 h@1 mA cm⁻²** (pristine 은 **75 h 에 단락**), 분극 **23→101 mV** vs **22 mV 평탄** | **[LiInF]** `Fig. 3a–d`·`Fig. S12`–`S15` | 우리 0 V 분해식 `Li₃P + 5 Li₂S + LiCl` | 순환 XPS 가 **LiF(F 1s 684.8) + Li–In alloy(In 3d 441.3/448.1) + In⁰(443.0/450.7)** 를 동정 — **F 가 절연 SEI, In 이 합금**이라는 분업. ⚠ F 1s 이동 **0.3 eV** 는 전하보정 오차 수준이고 In⁰/Li–In 성분은 In³⁺ 대비 **소수** |
| **σ_e ↓ ↔ CCD ↑ 역상관 — litdb 4번째 표(진영 5:1)** — σ_e **1.77×10⁻⁸ → 2.94×10⁻⁹ S/cm(6×↓, x=0.06 최소)** ↔ CCD **1.0 → 2.5(최대, 같은 x)**, 전 구간 **완전 거울상** | **[LiInF]** `Fig. S11`(+`Fig. 2c`) | 우리: modelc·+B₂O₃·LPSOCl 전부 **N(E_F)=0 완전 절연** | 진영 ✓[Taklu]·✓[Liu23]·✓**[LiInF]**·✓[Li25]·✓[LiGaF] vs ✗[Yang25]. **⚠ 본편은 In/F 를 안 갈랐지만, [LiGaF] 의 DC 분극 대조(F-only·co-doped 만 전류 0, Ga-only 는 pristine 과 동일)로부터 "σ_e 를 낮추는 것은 F" 라는 이식 가능한 가설** (추론임을 명시할 것) |
| **★ 2D 중간층으로 덴드라이트를 *막는* 게 아니라 *꺾는다* — 우리 h-BN/VGCF 인프라와 직접 대응** — 3층 `LPSC/LPSC–FG/LPSC`(FG 10 wt%). **CCD 0.7 → 1.5 mA/cm²**, BSEM 에서 덴드라이트가 FG 층을 따라 **옆으로 평균 193.75 μm**(n=9, 셀 3개) 눕는다. ToF-SIMS/XPS 로 FG 층 표면 **LiF 농화**(심도 따라 감소), LPSC 내부는 **Li–S**(취성) | **[Ling26]** `Fig. 3a–d` · `Table S1` · `Fig. S11`–`S13` | 우리 `tools/vgcf_hbn/`(VGCF·h-BN 계면 NEB/CDD 빌더) + `shi2017_hbn`·`liu2022_hbn` digest | **✅ 우리 인프라 그대로 CF 한 종만 추가하면 h-BN vs CF vs VGCF 3종 비교가 된다**(할 일 #2). ⚠ FG 는 σ 를 **21 % 깎는다**(§A) — "무손실"이 아니다 |
| **★★ 우리 SEI gap 사다리의 *맨 위 칸이 비어 있다* — LiF** — 이 논문의 음극쪽 서사 전체가 "Li₂S/Li₃P(저갭) → **LiF**(고갭) 로 SEI 를 갈아치운다" 이고, 근거가 ToF-SIMS(LiF⁻≫Li₂P⁻>LiS⁻)·XPS F 1s·AIMD(Li–F 결합수 6→99 in 10 ps) 3중이다 | **[Ling26]** `Fig. 3d` · `Fig. 3g` · `Fig. S13` | 우리 `sei_electronic.json` fixed-occ nscf gap: **LiCl 6.2603 > Li₂O 4.986 > Li₂S 3.4379 > Li₃P 0.7092 eV** — **LiF 칸 없음** | ⛔ **공백 확정.** [LiGaF] 가 외부 PBE 로 **LiF 7.4 eV** 를 준다(우리 LiCl 6.2/Li₂S 3.4/Li₃P 0.7 과 서열 일치). ⇒ **할 일 #1 = LiF 를 `sei_electronic`·`sei_formation_voltage`·`sei_neb` 에 추가.** ⚠ 단 이 논문의 Li 1s 는 55.05/55.15 eV **단일 성분**이라 LiF 를 분해하지 못한다(SI 스스로 인정) — **LiF 증거는 F 1s 뿐** |
| ★★ **SEI 에 *금속* 이 박힌다 — 우리 닫힌계 반응식이 남의 XPS 를 맞췄다** — Ta 도핑 SE 를 Li 금속과 순환시킨 SEI XPS = **금속 Ta⁰ (Ta 4f 24.4/22.4 eV)** + Li₂S(161.3/160.0) + Li₃P(130.0/129.3) + **LiCl**(200.3/199.6) + LiBr(69). CCD 0.8→**2.4 mA/cm²**, 대칭셀 278 h 단락 → **>1600 h(<60 mV)** | **[Wu26]** `Fig. 4d–f` · `Fig. S14` · `Fig. 5a` · `Fig. S15/S17/S18` | ★ **우리 `cascade_stability_axes.csv` 닫힌계 0 V**: `0.1667 TaCl₅ + 0.8333 Li → 0.1667 **Ta** + 0.8333 **LiCl**` (ΔE −930.3 meV/atom) · `0.1667 Ta₂O₅ + 0.8333 Li → 0.1667 Li₅TaO₅ + 0.1667 **Ta**` (−487.3). `cascade_interface_li.jsonl` 도핑 argyrodite: `→ Ta₂P + Li₂S + Li₂O + Li₃P + LiCl` | **✓✓ 산물 적중 + ⚠ 해석은 우리가 반대**. `cascade_product_gaps.json`: **Ta 0.0 eV(금속) · Ta₂P/TaP 0.0 · Li₂(TaS₂)₃/TaS₃ 0.0** vs **LiTaO₃ 2.388 · Li₅TaO₅ 3.902**. 논문은 Fig. 1b 에서 SEI 가 *"electronic insulation"* 이어야 한다고 선언해 놓고 **자기 XPS 가 금속 Ta⁰ 를 본다** — 그걸 COMSOL 로 "Li flux 균일화"라고 긍정 해석하는데 그 COMSOL 은 입력이 없다(Table S12 단일 세트). **⇒ 우리 693 반응 중 69 % 금속 산물 경고의 실물 사례.** ⇒ **비대칭/구배 도핑(양극쪽 Ta, 음극쪽 회피)** 설계 아이디어 |
| **Li 금속 표면 확산: 순수 Li(100) 0.38 → Li–In alloy(110) 0.17 eV** (Li–In(100) 0.23; 합금 표면E (100) 0.50 / (110) 0.40 / (111) 0.51 eV Å⁻²) | **[LiInF]** `Fig. 3g,h`·`Fig. S19` | — | [LiGaF] 의 **Li(100) 0.38 → Li–Ga(110) 0.11 eV** 와 **pristine 값이 완전히 같다(0.38)** = **같은 그룹이 같은 계산을 재사용**. ⚠ 두 논문 모두 **4×4 Li(100) vs 1×1 M-도핑 (110)** 비교라 **3 변수 동시 변경** |
| **★ F2 Li/SE 계면 3분류 = 우리 SEI-gap 지표의 "표준 어휘"** — ① **열역학 안정**(새 상 없음; *"most desired, but is **extremely rare**"*) ② **MCI**(mixed electronically & ionically conducting interphase — 전자가 통해 **SE나 음극이 소진될 때까지 성장**; *"completely unacceptable"*) ③ **passivating SEI**(이온전도·전자절연 → 자기제한). Li에 열역학 안정한 것은 **LiF·LiCl·LiBr·Li₂O·Li₂S·LiH·Li₃N 뿐**(σ 낮아 얇은 보호층 용도). **Li₆PS₅Cl·Li₇P₃S₁₁은 "benign"** — *"none of their reduction products is highly electronically conductive"* | **[Miao23]** §4.2.1 — **정성 정의만, 판정 계산법 없음** (동일 분류가 `fan2026` §3.4 에 그대로 상속) | comp1/modelc 0 V 분해 **Li₃P + Li₂S + LiCl** = 전부 wide-gap → ③ 계열 · `db/properties/b2o3_sei_gaps.json`(산물별 gap 서열) + `interface_reactivity`(T9 47종; **LPSCl vs Li −541.5** = ①이 아님) | **✓✓ 우리가 정량판을 갖고 있다.** 리뷰의 ②/③ 이분법에 **연속 좌표(gap)** 를 부여 → SEI json 에 `interface_type` 열 추가가 즉시 가능(새 계산 0). ⚠ **절대 임계값 금지** — PBE 과소·무질서 민감이라 **같은 방법 내 순위**로만 |
| **★ Table 3(Li‖SE 버퍼 27행) = 우리 gap 서열의 외부 대조군** — 버퍼 재료가 **LiF 8행 · Li₃N 4행**(+Li₂O·LiCl 계열) = 리뷰가 말하는 "이상적 SEI"의 실체는 대부분 **wide-gap 이성분 Li 염**. 황화물 SE 행: LGPS+**Ag** 1000 h · LGPS+**Li₅.₅PS₄.₅Cl₁.₅ 1800 h** · Li₃PS₄+Li_xSiS_y **2000 h** · Li₇P₃S₁₁+LiF 200 h; 할라이드: **Li₃YCl₆ + Li₆PS₅Cl 1000 h** | **[Miao23]** Table 3 (Li‖Li 대칭셀 지속시간 [h] — **전류밀도·용량·온도가 행마다 제각각**) | 우리는 같은 산물군을 **gap** 으로 줄세움 | **○ 순위 대조 후보.** "실험이 오래 버틴 버퍼일수록 우리 gap 서열 상위"가 성립하면 지표의 외부 검증. ⚠ **조건이 제각각이라 정량 회귀 금지 — 순위 일치 여부만** |
| **🔎 modelc 사촌 조성의 *두 번째 용도*: Cl-rich argyrodite가 LGPS의 음극 버퍼** — **Li₅.₅PS₄.₅Cl₁.₅** 층이 LGPS‖Li 대칭셀을 **1800 h** 지탱(0.25 mA cm⁻² & 0.25 mAh cm⁻²). 같은 논리로 **Li₃YCl₆‖Li 를 Li₆PS₅Cl 로 보호** — LPSCl 계면상은 전자전도가 나빠 자기제한이지만 Li₃YCl₆는 혼성전도라 **계속 자란다** | **[Miao23]** Table 3 (ref [178]·[183]) | **modelc = Li₅.₄PS₄.₄Cl₁.₆** — 사실상 같은 조성. 우리 환원 한계 **1.242 V** · 0 V 산물 Li₃P/Li₂S/LiCl(전부 전자절연) | **✓ 우리 서사 확장 근거** — Cl-rich 를 "빠른 SE"만이 아니라 **"음극에서도 자기제한적"** 으로 말할 수 있다(우리 환원·SEI gap 이 그 근거). ⚠ 문헌 지속시간(h)은 소환값, 우리 값과 같은 표에 넣지 않는다 |
| 분해창 환원 <1.7 V / 산화 >2.1 V | [Ke] (인용), [GG] | ESW 환원 **1.24 V** / 산화 **2.14 V** | 산화 ✓(2.1≈2.14); 환원 같은 결 |
| LPSCl(1.5) 환원 산물 = Li₂S+Li₃P **+LiCl** | [Ke], [GG], **[Lu]**, **[Liu23]** | comp1/modelc 0V → Li₃P+Li₂S+**LiCl** | **✓ 동일 chemistry** ([Liu23]도 PS₄→Li₂S+Li₃P) |
| **Li₆PS₅X 환원전위 1.7 V vs Li → Li₃P+Li₂S+LiX (passivation)** | **[Rupp]** Table 3 (in-situ XPS+EIS) | comp1/modelc 환원 1.24 V → Li₃P+Li₂S+LiCl | **✓ 동일 chemistry**, 전위 절대값은 방법차(우리 0-pressure vs 인용 indirect/실험). **LiX=LiCl이 passivation 산물** = modelc Cl-rich 이점 단서 |
| **황화물 환원 ~1.7 V·0 V 산물 Li-binary의 *계산 원전* + passivation 가능/불가 이분법(산물 전자절연성)** | **[Zhu15]** (2015; [Ke]/[GG]/[Lu]/[Bai]/[Rupp]가 인용하는 "~1.7 V·Li₃P+Li₂S+LiCl"의 1차 출처) | LPSCl red 1.71 V(→P+Li₂S+LiCl)·0 V **Li₃P+Li₂S+LiCl, E_D −0.96 eV/atom**; **Li-binary 산물(Li₂S/LiCl/LiI/Li₂O/Li₃N/Li₃P)=0 V 안정+전자절연→passivation**(LiPON·Li₃PS₄·Li₇P₂S₈I Li-호환의 근원) vs **전도성 산물(Li–Ge 합금·Ti³⁺ 티타네이트)=MCI→연속 분해**(LGPS/LATP/LAGP/LLTO); "Li-halide 도핑=σ+Li안정 동시" 처방 명시 — comp1/modelc 0 V 산물 **정확 동일**(Li₃P+5Li₂S+LiCl, +8 Li)·환원 onset 경계=우리 ocv 1.717 V(§B 맵핑) | **✓✓✓ E축 전체의 2015 원형** — LiCl-SEI 서사([Lu]/[Liu]/[Li25])·Nolan Type1/2/3([Kang])·우리 sei_products.json gap 분류가 전부 이 이분법의 후손(우리=gap 수치로 정량화). ⚠ Zhu passivation 판정=산물 상식 heuristic(σ_e/gap 계산 0) |
| **도핑 route**: PS₄³⁻의 Li-유발 redox 분해를 **Mg(s-p 혼성, S 전자풍부→전자이동 차단)+F(in-situ LiF 절연층)** 로 억제 (MgS₄는 무분해) | **[Liu23]**(MgF₂), [Ke](MgClO) | modelc 환원산물 = 그들이 억제하려는 분해산물 | 별도 축(조성 아닌 *도핑*); cascade 동기 |
| interphase **LiCl = 전자절연(gap 6.22) + 저Li⁺장벽(0.05) + 연성(Poisson 0.23)** → 좋은 buffer | **[Lu]** Fig6 | modelc가 LiCl 생성 → Lu의 "good passivator"로 해석 | **✓ 우리 LiCl 산물에 의미 부여** |
| **in-situ LiF-rich SEI(액체 처방 FEC→LiF)가 SE 분해(Li₂S) 억제 → 균일 Li flux·dendrite 억제** (XPS F1s 684 / S2p Li₂S↓; overpot 154→55 mV; CCD 0.8→1.5) | **[KimICCF]** Fig 5 | comp1/modelc native 환원산물 = Li₂S/Li₃P/LiCl (그중 Li₂S=전자전도 우려) | **🔑 = 우리 'electron-blocking interphase' 메커니즘의 실험 카운터파트**. 우리 DFT=어떤 산물이 절연(LiF/LiCl/Li₂O/Li₃PO₄/NdPO₄), 이들=그 절연 SEI를 액체 처방(FEC)으로 **in-situ 형성**. LiF·LiCl·Li₂O·Li₃PO₄ = wide-gap 절연 패밀리 일관. ⚠ σ_e 실측 아님(간접추론) |
| **도핑 route(CuBr₂)가 음극에 wide-gap *LiCl@LiBr* native 절연층 형성 → Li₂S/Li₃P 전도성 분해 억제** (cycled XPS LiCl 56.3·LiBr 56.9; LPSC-P는 Li₂S 160.2·Li₃P 신규·심한 분해). **σ_e↓(1.02e-8→3.35e-9)→CCD↑(0.6→1.9 mA/cm²)·3000 h** | **[Li25]** Fig 4·5 | comp1/modelc native 환원산물 = Li₃P+Li₂S+LiCl (LiCl=절연·Li₂S=전도 우려) | **🔑 = 우리 'wide-gap 절연 interphase' 패밀리 또 하나**(LiF[KimICCF]/Li₂O[Ke]/LiCl[Lu]/LiF[Liu23]에 **LiBr 추가**). 우리 환원산물 LiCl(절연)이 정확히 이들 메커니즘. **단 이 절연층은 도핑이 만든 *native 분해산물*(LiCl/LiBr), Nd는 *능동 O-derived 산물* → 위치 다름**. σ_e↔CCD 역상관은 우리 "SEI 전자절연=dendrite 레버"의 실측 증거 |
| **도핑 route(CuCl)는 *다른 레버* — 분해산물 절연이 아니라 *모체 SE 자체*를 (P/Cu)S₄로 rigid·저-σ_e화 → 애초에 Li₂S/Li₃P를 *덜 생성*** (cycled XPS: LPSC-P Li₂S 160.9·LiCl 56.38·P₂Sₙ 163.52 *강* / LPSC-1 분해 미미·(P/Cu)S₄ 무손상; time-resolved EIS R/R₀ LPSC-P 지수증가 vs LPSC-1 평탄). **σ_e↓(8.75e-9→1.49e-9)→CCD↑(0.75→3.0 mA/cm²)·2400 h@0.1·>200 h@3** | **[Taklu]** Fig 7·5·4b | comp1/modelc native 환원산물 = Li₃P+Li₂S+LiCl (동일 chemistry) | **△ 목표 같음(dendrite 억제)·레버 *위치 다름***: [Li25]·우리 cascade=**절연 분해산물**(LiCl/LiBr/Li₂O/Li₃PO₄)이 e⁻ 차단인데, [Taklu]=**모체를 분해저항화**(애초에 Li₂S 적게). 즉 "산물을 절연으로" vs "모체를 robust로" 두 갈래. 환원 chemistry(Li₂S/Li₃P/LiCl)는 우리와 동일. σ_e↔CCD 역상관(Fig 4b)=dendrite 레버 실측. ⚠ full-cell 미검증·50 °C·저면적용량(0.5 mAh/cm²) |
| **도핑 route(La₂O₃)의 음극 SEI = La⁰ + LiCl (+주장 LaCl₃ 1D 채널)** — CCD 0.9→**3.1 mA/cm²**(**σ와 무상관** 명시: σ 최고인 undoped가 CCD 최저)·대칭셀 25→**200 h**·σ_e는 오히려 8.5×↑(2.59e-9→2.2e-8). 결론 원문 "mitigates dendrite formation by … **the formation of La and LiCl**"; "by-product **LaCl₃** [LaCl₉] 1D 채널" 도식(Fig 3i,j)은 **가설**(SI 정독 확정: 음극 XPS·La 3d·Cl 2p·반응식 전무) | **[Yang25]** (La₂O₃ dual-doping, exp) | **우리 Nd hull 지도**(`tools/oxidation/esw_nd_result.txt`): **V=0 산물 = 0.3Li₂O+0.8Li₃P+4.1Li₂S+0.2NdP+1.6LiCl — RECl₃ 없음**; Li가 RECl₃ 치환(NdCl₃+3Li→3LiCl+Nd⁰, 발열 ~−1 eV급); **NdCl₃는 ≥2.62 V 산화 산물로만**(gap 4.30) | **🔑🔑 화해 판정**: Yang의 *데이터가 지지하는* 음극 화학(**La⁰+LiCl**) = **우리 치환반응 산물과 정확히 동일** → 정합. 유일한 긴장 = "LaCl₃가 Li 계면에 잔존" 도식 — Li 직접접촉이면 우리 지도와 모순, **gradient SEI**(Li면 La⁰/LiCl·바깥 고전위층만 LaCl₃; Yao Nature ref38의 원그림)로만 양립. 합성-형성 LaCl₃ 주장도 없음(벌크=LaS₄/PS₃O 고용체) → 충돌 시나리오 자체가 부재. **σ_e↑에도 CCD↑** = [Taklu]/[Li25] "σ_e↓→CCD↑"의 역방향 사례 → "bulk σ_e는 결정변수 아님, interphase 화학이 결정". ⚠ 우리 hull은 **Nd 전용**(La 미포함) — 화학 유추 강하나 정량 이식 금지, La-hull 후속 1건이면 문장 그대로 검증 |
| **도핑 route(GaF₃)에서 *두 도펀트 역할이 실험적으로 분리된다*: F=전자차단·σ비용 / Ga=이온·합금** — **DC 분극(0.4 V, Fig S8): F-doped·Ga-F co-doped만 정상전류 ~0 µA, Ga-only는 pristine과 동일(~0.08 µA)**; σ **pristine 5.6 / Ga-only 6.4 / co-doped 4.5 / F-only 2.3 mS cm⁻¹**(F가 σ를 깎음 — [Liu23] Mg-only 3.51→MgF 1.70과 동형; **본문이 감소를 인정**). **σ_e 1.68e-8→5.0e-9 S cm⁻¹ ↔ CCD 0.4→1.8 mA cm⁻² 가 x=0–10 % 전 구간 단조 역상관, 둘 다 x=4 %에서 극값**(Fig S10). 순환 200 h 후 음극 XPS: **pristine → LiCl**(S13) / **co-doped → LiF**(S14). 자체 DOS: **LiF 7.4 > LiCl 6.2 > Li₂S 4.2 > Li₃P 1.1 eV**(S15) | **[LiGaF]** (exp + DFT보조) | comp1/modelc 0 V 환원산물 = Li₃P+5Li₂S+**LiCl**; `sei_products.json` LiCl 6.65 / Li₂S 3.90 / **Li₃P 0.70(누설)**, **LiF는 우리 파일 미등록** | **🔑🔑 σ_e↔CCD 역상관 진영의 4번째 표**([Taklu]·[Li25]·[Liu23] 편, [Yang25]가 유일 반례) — 그것도 **단일 비교가 아니라 6점 조성 곡선**이라 가장 강한 형태. **pristine→LiCl 은 우리 열역학 예측과 동일 화학**이고 F가 그 위에 **더 넓은 갭 산물 LiF**를 얹는다 = 우리 wide-gap 절연 interphase 패밀리(LiCl/Li₂O/Li₃PO₄/NdPO₄)에 **LiF 추가**. ⚠ 흡착E·표면 NEB 절대값은 이식 금지(§F·§D) |
| **0 V 환원 반응에너지 cation 전수 지도**: P⁵⁺=최악(수분·환원 둘 다)·Sn/Ge/As/Sb=환원 1.0–1.5 V 희생·**RE(Sc/Y/란타나이드, Nd 포함)=Li 황화물 중 환원안정 최우수 + "doping candidate" 명시**·Li황화물엔 수분+환원 동시 만족 조성 없음(Fig 3a) | **[Zhu20]** (grand-potential 0 V lithiation — 우리와 동일 스킴·동일 원저자 그룹) | 우리 환원한계 1.242 V·0 V 산물 Li₃P+Li₂S+LiCl(P⁵⁺ 환원 = 정확히 Zhu의 P 최악 판정); **Nd cascade의 RE 선택 = Zhu 2020 계산 선례와 정합**(환원측) | **✓ 방법·화학 정합 + Nd 외부 지지(환원측)**. ⚠ 수분측은 Li–RE–S 음수(민감, **정확값 LiNdS₂ −0.273**) → "RE가 대기안정 준다" 금지 — [Yang25]의 대기 개선은 O(P–O) 몫으로 분리(RE=환원/interphase 몫). Zhu 본문 "electrochemical stability"=이 환원축 전용. **⭐ 2026-08-05 SI xlsx 전사로 추가된 것**: 0 V 반응에너지 **전 269 화합물 정확값** + 본문이 논의조차 안 한 **4.5 V 산화 + ESW 창(cathodic/anodic limit, V)** (`db/properties/zhu2020_si_redox_reactions.csv`). 우리 계 앵커: **Li₇PS₆(Cl 없는 argyrodite 모체) 1.708–2.129 V** · Li₃PS₄ **1.708–2.369 V** · Li₇P₃S₁₁ 2.291–2.320 V · 염화물 anodic **4.0–4.2 V**(Li₃InCl₆ 4.176·Li₂ZrCl₆ 4.013). ⚠ **우리 comp1 1.242 V와 직접 비교 금지** — Li₇PS₆는 Cl이 없어 다른 물질이다(차이는 조성·구조·상집합 탓이지 방법 탓이 아님). 올바른 용법은 **검산 앵커**: 우리 ESW 파이프라인에 Li₃PS₄를 넣어 1.708–2.369가 재현되는지(§H A6) |
| **Nolan Type 1/2/3 Li/SE 계면 분류** (1=열역학안정 passivating / 2=MIEC 성장형 / 3=전자절연 kinetic SEI) | **[Kang]** Fig5c (Nolan ref47) | comp1/modelc 환원산물 Li₃P+Li₂S+LiCl → **Type 3 목표**; sei_products.json gap 분류(insulator≥4/marginal2–4/conductor<2 eV) | **🔑 = 우리 SEI 전자절연 논리의 표준 프레임**. 우리 gap 임계 = Type 분류의 *정량판*. Nd cascade = "conductive Li₃P(0.70)를 wide-gap Li₂O(5.24)/Li₃PO₄(5.73)로 → Type3 강화" |
| **dendrite는 *환원 SEI*의 전자구조가 좌우(pristine bulk 아님)** | **[Kang]** Fig6c (Hao ref90 계산) | 우리 bulk σ_e(gap 2.07 wide insulator)만; SEI 산물 gap은 sei_products.json | **✓ bulk σ_e 한계 명시** — dendrite 진짜 레버는 SEI 전자절연성(우리 sei_products.json) |
| 계면E Li/LPSCl −2.68 ≪ LiCl/LPSCl −0.19 J cm⁻² (LiCl buffer가 Li-S 자발반응 차단) | **[Lu]** Fig6a | 우리 계면 slab 미계산(gap H) | 차용 가능 |
| **[Lu] 견해**: 4d-Cl 90 % 자기분해 → LiCl passivation → **Cl-rich가 음극 유리** (CCD 0.96, 800h) | **[Lu]** | modelc Cl-rich, 4d 점유↑ 추정 → 부합 | Cl-rich ✓(조건부) |
| **[Liu] 견해(AIMD kinetic)**: Cl-rich 환원 분해가 *더 느림* — 계면 P–S RDF(300 K, 50 ps): PS₄³⁻(2.02 Å) **LPSCl 10 ps서 깨짐 / Cl-rich 35 ps 유지**; LiₓPᵧ(2.5 Å) LPSCl이 더 빨리·많이 형성. + **LiCl-rich SEI**(post-mortem XPS LiCl↑·Li₂S↓·PS₄ 131.9 eV↓) → CCD 0.95→**1.40 mA/cm²**·대칭셀 500 h(R 65→600 vs 34→50 Ω). **Cl-rich 음극 유리** | **[Liu]** (Fig 4·S10) | 우리 grand-potential = **0V 환원산물만**(Li₃P+Li₂S+**LiCl**, thermo) — 분해 *속도* 못 봄 | **△ 보완(kinetic)·[Lu]와 동맹**: 우리=어떤 산물(thermo, 동일 화학)·Liu=얼마나 빨리(kinetic). LiCl=절연(우리 sei_products 6.65 eV)이 Liu "LiCl SEI 이점"에 의미부여. **우리 H목록 '음극 분해 동역학'을 메우는 외부 AIMD 증거** |
| **[Adeli] 관측(초기·약한 증거)**: Li 대칭셀 **0.25 mA/cm²·1.0 mAh/cm²**서 Cl-rich(x=0.5)가 Li₆PS₅Cl과 **동등~약간 우수**(±~12 mV 안정, ~160 h; 전해질 0.7 mm)·易환원 금속(Ge/Sn) 부재 강조 | **[Adeli]** (Fig S8, 2019) | comp1/modelc 환원산물 동일(Li₃P+Li₂S+**LiCl**) | **○ [Lu]/[Liu] "Cl-rich 음극 유리" 진영의 최초 데이터점** — 단 CCD·임피던스 추적·post-mortem 없음 = 약한 증거(본대는 [Liu] AIMD-RDF/XPS·[Lu] 4d-Cl 자기분해). LiCl-rich SEI 서사의 전사(前史)로만 인용 |
| **Li\|황화물 계면 산물의 pseudo-binary 원전 = 캠페인 ① 기대산물 사전**: Li₃PS₄·Li₃PO₄·LiPON은 Li 금속에 불안정하나 **Li₂S/Li₂O+Li₃P 자가-passivation**(Li₃P=이온전도체, LiPON\|Li in-situ XPS ref42 관찰); argyrodite 첫 환원 `2Li₆PS₅Cl+2Li→Li₄P₂S₆+4Li₂S+2LiCl`(**P⁵⁺→P⁴⁺ P–P 중간체**; hull-entry 의존 — [Zhu15] 계단엔 없음); 저전압 황화물 양극(LiTiS₂ μ)서도 `→5Li₂S+P+LiCl` 환원 | **[Rich16]** Table S1·S5 (+**[Zhu15]** 0 V 종점 Li₃P+Li₂S+LiCl·E_D −0.96 eV/atom) | 우리 esw 0 V 산물 동일(Li₃P+5Li₂S+LiCl) → **캠페인 ①(UMA Li\|도핑SE MD, `mlip_next_campaigns_2026_07.md`)의 기대-산물 리스트 확정**: 종점 **Li₂S·Li₃P·LiCl**(+도핑 분기 Li₂O/LiF) + 중간체 후보 **Li₄P₂S₆(P–P RDF)·P⁰/LiP₇** = DFT 스팟체크 세트 (digest §13 표) | **✓✓ 열역학 종점 3자(Richards·Zhu·우리) 일치 — 문헌=무엇이 되나, 우리 MD=경로·속도·self-limit 여부**. ⚠ Li₄P₂S₆는 Richards hull에만 → "있으면 보너스" 관측 목표로만 |
| **음극(0 V) 산물 = Li₂X + Li₃P + LiₓM_y 합금 — "전도성 SEI 형성 가능·금속성 산물은 걱정(interphase 성장)" 조성족 일반화(2013)** — 전 11조성 공통(Ge→Li₁₅Ge₄·Si→Li₂₁Si₅·Sn→Li₁₇Sn₄·Al→Li₃Al₂; M-무함유 Li₉P₃S₁₂만 Li₂S+Li₃P) | **[Ong13]** (2-포인트 grand potential; Mo2012 LGPS 단일 → 여기 조성족 → [Zhu15] 절연 SEI/MCI 이분법 정량의 중간 고리) | comp1/modelc 0 V **Li₃P+Li₂S+LiCl** — **M-무함유 P계라 금속 합금 산물 자체가 없음** | **✓ 계보 — [Zhu15] E축 원형 행의 前史**: "금속성 산물 걱정"(Ong13) → "전도성 산물=MCI=passivation 실패"([Zhu15])로 정량화. **argyrodite가 LGPS 대비 음극 유리한 이유(합금 없음·전 산물 Li-binary)의 원조 논거** — 우리 sei_products gap 분류의 2단계 조상 |
| **⭐ 열역학 3산물 중 *Li₂S만 결정화한다* — 나머지는 비정질/고립 클러스터** (반응 MD): Li‖LPSCl 20 ns 궤적에서 계면 결정영역의 RDF 첫피크 ~2.5 Å·시각 정합이 **Li₂S(Fm3̄m)** 와 일치하는 반면, **Li–P/Li–Cl RDF는 고차 피크가 없고**(장거리 주기성 부재) local-environment/cluster 분석에서 Li₃P-유사·LiCl-유사 모티프는 **고립되거나 아주 작은 클러스터로만** 존재. 같은 창에서 Li₂S-유사 환경 개체수가 유의하게 높음 | **[KimSEI]** ⛔프리프린트 (Fig 3b·3c·S7·S8) | 우리 grand-potential 0 V 산물 = **Li₃P + 5 Li₂S + LiCl**(열역학, 상 분리 가정) | **🔑🔑 화학은 일치·*상태*가 신규 정보**: 열역학은 세 상을 등가로 예측하지만 동역학은 **Li₂S만 결정, Li₃P/LiCl은 비정질**이라 말한다. ① 우리 `sei_products.json`은 **결정상 gap**(Li₂S 3.04/LiCl 6.65/**Li₃P 0.70**)으로 절연 판정을 하는데, **비정질 Li₃P의 gap은 결정값과 다를 수 있다 → 우리 판정의 가정 하나가 노출** (후속 계산 후보). ② P가 **Li 금속 내부 z>125 Å까지 침투**(Fig S9a) = grand-potential이 못 보는 **고용체/오염 경로**. ⚠ 프리프린트·시드 1개 |
| **⭐ Li‖LPSCl SEI 2단계 형성 + *자기 부동태화의 구조적 반쪽*** (반응 MD, 350 K): 접촉 즉시 PS₄ 분해 → **S-rich 비정질 ~6 nm** → **~11 ns 에 그 안에서 Li₂S 결정 핵생성 → ~5 nm 성장**; 기구는 **①S가 먼저 골격 형성(7 ns) → ②Li 침투가 결정화(11 ns)** 순 — ⚠ **단 0단계가 앞에 있다**: 초록 원문이 *"**Li insertion** destabilizes PS₄ tetrahedra"* 라 **분해의 트리거는 Li 삽입**이다(Li가 두 번 작용). "S가 먼저"는 **PS₄ 분해 이후** 단서를 붙여 인용할 것. **★ 핵생성 위치 확정(2026-08-04 z 역산)**: 초기 계면 z≈105 Å·Li–S 배위 급증 z≈75 Å·P 침투 z>125 Å 을 모델 두께로 검산하면 **LPSC 0–105 Å / Li 105–165 Å** 로 전부 정합 → **결정 Li₂S 핵은 계면이 아니라 LPSC 쪽 ~3 nm 안쪽에서 시작**하고 부분 비정질 Li₂S-유사 영역이 계면 너머 Li 쪽 2 nm까지 걸친다(결론의 "LPSC 쪽 핵생성 → Li 쪽 성장"과 일치). **잔존 PS₄ 층수 20→6에서 plateau(11 ns)** = 결정층 등장과 분해 정지의 동시성; **층 간격 ≈0.5 nm = a/2** 로 검산됨(소형 20층/10 nm·대형 40층/20 nm 동일 환산 → 18층=9 nm·34층=17 nm). 대형계(16 nm Li‖20 nm LPSC·50 ns): 개시 ~30 ns·**~11 nm interphase**(실험 cryo-TEM ~12 nm, Luo 2022 ACS EL 7, 3064와 **자릿수** 일치) | **[KimSEI]** ⛔프리프린트 (Fig 2·3a·4·5) | **우리 음극 계면 반응 MD 완전 공백** (`kb/open_items.md` **T3**). 우리는 정적 grand-potential 산물(thermo)만 | **✗ 우리 공백 = T3의 프로토콜 원본** + **🔑🔑 결정적 상보성**: MTP는 **고전 퍼텐셜 = 전자가 없다** → 이 "self-passivating"은 **구조적 격리**이지 **전자 차단이 아니다**. 실제 부동태화의 지배 기구(=[Zhu15] Li-binary 절연산물·[Kang] Nolan Type 3·[Li25]/[Taklu] σ_e↔CCD)는 **이 MD가 원리적으로 볼 수 없는 축**이고, 우리 `sei_products.json` gap 분류가 정확히 그 반쪽 → **경쟁 아닌 두 조각**. ⚠ **시드 1개·오차막대 0**(핵생성=확률과정, 11/30 ns 차이에 통계 의미 부여 불가)·**개회로 무전류**(서론이 인용한 Narayanan 2022는 제목이 "current density 효과"인데 미다룸)·소형모델은 20층 중 14층 소모 = **저장고 고갈**과 부동태화 구분 못 함·본문 내부 모순(§3.3 "억제" vs §3.4 "continued decomposition") → **11 nm는 하한**·2단계 기구는 Ren 2024 EES/Chaney 2024 ACS AMI 선행 有 |
| **⭐ 생성된 SEI가 모체보다 *느리다* (영역분해 D)**: 같은 셀 안에서 **결정 SEI 영역 0.4e-7 vs 잔여 LPSC 벌크 1.1e-7 cm²/s (@350 K) = 비 0.36**; 잔여 벌크는 pristine(1.6e-7, [KimMTP] 소환)과 같은 자릿수 → *"계면 반응이 미반응 벌크의 Li 수송은 크게 건드리지 않는다"* | **[KimSEI]** ⛔프리프린트 (Table 1·Fig 3d) | 우리 MLIP-MD는 **bulk 단일 영역**만 (D 600 K comp1 3.09e-6 / modelc 7.90e-6, MSD **2–50 ps 고정 창**) — 구획 마스크 없음(**T5**) | **✗ 공백(T5) + ⚠ 반면교사**: 우리 역산 결과 **두 D가 서로 다른 창에서 나왔다**(벌크=0–20 ns 전구간 / 결정영역=**11–20 ns만**; 논문은 창을 명시하지 않음). 파란 곡선이 선형이라 **결론은 유지**되나, 같은 그림에서 0–11 ns 창을 쓰면 "SEI가 벌크보다 3배 빠름"이 나온다 → **구획이 시뮬 도중 정체성을 바꾸면(비정질→결정) 영역분해 MSD는 창에 극도로 민감**. **우리 T5 설계 규칙**: ①마스크를 **시간분해**로 ②**창 명시** ③상전이 구획은 **전이 전/후 분리 보고**. **⛔ D 절대값을 우리 db와 같은 표/플롯에 올리지 말 것**(온도·엔진·창 전부 다름) — 비율 0.36만 |
| **⭐ 계면 반응을 *설계*로 유도: S 중간층 → Li₂S 조기 핵생성 → SEI 박막화** (개념 실험): Li와 LPSC 사이에 **~3 nm 원소 S** 삽입 → Li이 LPSC 접촉 전에 Li₂S를 먼저 형성 → 50 ns 후 **SEI 11 → 6 nm**, **잔존 PS₄ 18 → 34층**(반응 전선 ~40 ns 안정화) | **[KimSEI]** ⛔프리프린트 (Fig 5b·5d·5e) | 우리 처방 축은 **도판트 cascade 47종**(조성 레버) — **중간층/코팅 레버는 없음** | **△ 문제설정 다름 + 인용 조건부**: "국소적으로 S가 풍부한 환경을 만들면 Li₂S 부동태화가 앞당겨진다"는 **설계 원리**까지만 인용 가능. **⛔ "S 코팅이 실용 해법"으로 확장 금지** — 논문 스스로 원소 S는 휘발·반응성 때문에 비현실적이라 인정하고, 대안(surface sulfidation·S 첨가제)은 **계산하지 않았다**. ⚠⚠ **그런데 이 논문의 초록은 정확히 그 금지된 확장을 한다**("sulfur coating is **demonstrated as a practical approach**", 2026-08-04 실물 확인) → **초록 인용 금지, 본문·결론 문장을 쓸 것**. 공정한 지표는 두께(출처가 다른 물질이 섞임)가 아니라 **PS₄ 잔존 층수(18 vs 34)** |
| **Y/O 공도핑 → 음극 환원분해 억제 + in-situ Li₂O interphase** — 계면 XPS depth: Li₂S 21.3→**9.9%**·Li₃P 9.0→**3.6%**·**Li₂O 528.5 eV**(SIMS LiO⁻ 균일층); CCD 0.7→**1.5 mA/cm²**·대칭셀 >4800 h·DRT로 SEI(10⁻⁴ s)/SSE(10⁻⁶ s) 파괴 시점 분리(1.6 vs ≥2.4 mAh/cm²) | **[WangYO]** Fig 3,4 | comp1/modelc 0 V 산물 **Li₃P+Li₂S+LiCl**(grand-potential)·환원한계 1.242 V | **✓ 같은 chemistry, 개선의 실체는 kinetic passivation**(열역학 계산 없음·5% 치환이 환원전위를 못 바꿈·Y-only/O-only 대조 부재). Li₂O = [Lu]LiCl·[Li25]LiBr와 같은 **wide-gap 절연 interphase 가족**(축 E 서사) — [Yang25] La-O와 동일 결("음극 이점=산물 interphase") |
| **[GG] 견해**: 과안정 LPSCl1.5는 self-limiting ✗ → **moderate Cl(1.0)이 유리** (다층 전략) | [GG] | — | Cl-rich ✗ |
| **⭐⭐ 계면상의 온도 의존은 *화학종*이 아니라 *나노구조*가 바뀌는 것** — 25 °C·60 °C 둘 다 산물은 **Li₂S 하나**인데, **25 °C = 단결정 ~12 nm 균일**(FFT 이산 스팟·0.33 nm (111) fringe) / **60 °C = 다결정 + 입계·전위 + 바깥 ~3 nm 비정질**(FFT 호). 임피던스가 그대로 따라간다: R_SEI **4→13 Ω(확산律速, 위로 볼록)** vs **2→204 Ω(100×, 반응律速 0–72 h → 확산律速 72–120 h)**, 벌크(14.4 Ω/~500 µm)의 **14배** | **[Luo22]** `Fig. 1a–c`·`Fig. 2a,b` (exp, cryo-TEM+EIS) | 우리 `sei_products.json` 은 **상별 gap**(Li₂S **3.90** marginal / LiCl 6.65 절연 / Li₃P 0.70 누설)만 준다 — **입계·결정립 개수는 우리 지표에 없다** | ➕ **상보(경쟁 아님)** — Luo 는 *구조*(입계), 우리는 *전자*(gap). "입계가 왜 나쁜가"의 전자 쪽 절반이 우리 것. ⇒ **T3 관측량에 "결정립 개수/배향 분산" 추가**(z–t 밀도 열지도만으로는 안 잡힘) |
| **⭐ 열역학 3산물 중 실험도 Li₂S 만 본다** — cryo-TEM 은 **Li₂S(111) 0.33 nm 하나만** 지수화, Raman 은 **372 cm⁻¹(표준 Li₂S 대조)** 만 신규. **Li₃P·LiCl 은 검출 안 됨** — 저자 설명은 *"양이 너무 적어 글러브박스/UHV 의 미량 H₂O·O₂ 에 소모된다"*(Li–P) 와 *"자기 AIMD 의 Li–Cl RDF 에 변화가 없다"*(LiCl) | **[Luo22]** `Fig. 2a`·`Fig. 1e`·`Fig. S2`·`Fig. 3e,i` | comp1/modelc 0 V 분해식 = **Li₃P + 5Li₂S + LiCl**(grand-potential) | ✅✅ **모순 아니라 삼중 수렴** — (i) 이 실험, (ii) [KimSEI] MTP 반응 MD("Li₂S만 결정화, Li₃P·LiCl 은 비정질/고립"), (iii) 우리 열역학(3산물 예측)이 **서로 다른 이유로 같은 그림**. ⇒ **T3 성공 판정 1순위를 "두께"가 아니라 "Li₂S 만 결정화하는가"로 잡는다** |
| **⚠ 실험 앵커의 무게 — `~12 nm` 에는 오차막대가 없다** — 온도당 **덴드라이트 1개·시야 1개·측정 화살표 1개**(`Fig. S3a` 노란 박스 → `Fig. 2a`), `±`·s.d.·`n =`·히스토그램 **0건**, 본문 표기는 항상 `∼`. **60 °C 총두께는 논문에 숫자가 아예 없다**(비정질 ~3 nm 뿐). 게다가 두 시료는 **온도만 다르지 않다** — 전착 **0.4 vs 0.6 mA cm⁻²**, 단락까지 전하 **~0.16 vs ~0.6 mAh cm⁻²(≈4×)** (`Fig. S4`, 논문 미논의) | **[Luo22]** §11b 불확도 감사 · `Fig. S3`·`Fig. S4` | T3 미착수. 비교 대상 = [KimSEI] MTP **~11 nm @50 ns**(시드 1개·오차 0·자체 판정 "11 nm 는 하한") | 🔴 **"11 vs 12 nm 정량 일치" 인용 금지.** 허용은 **"같은 자릿수(10 nm 급)"** 까지 — 양쪽 다 N=1 이고 기하(덴드라이트 껍질 vs 평면 슬랩)·시간(48 h vs 50 ns)·온도(298 vs 350 K)가 다르다 |
| **⚠ 실측 대상이 "묻힌 계면"이 아니라 "뜯어낸 껍질"** — FIB 단면이 아니라 **기계적 박리 → 분말 긁기 → lacey carbon grid**. `Fig. 2a` 가 라벨한 것은 **Interphase layer 와 Li Metal 뿐이고 LPSCl 은 시야에 없다**. 박리 때 계면상 일부가 전해질 쪽에 남았을 가능성은 평가되지 않았다 | **[Luo22]** SI Experimental · `Fig. 2a` (우리 figure-read) | T3 계획은 **양쪽이 붙어 있는 상태**의 Li(100)‖LPSCl(100) | ⚠ **~12 nm 는 원리적으로 하한**일 수 있다. 우리 T3 두께는 "분리 전" 값이므로 **같은 양이 아니다** — 대조 시 반드시 명시 |
| **⚠ Bader 로 잰 인공 SEI 6종 차단력: LiF 가 거의 무용, Li₂S 자신도 30 %만** — 500 K·10 ps 후 **전해질 순전하(\|e\|, figure-read)** **None 18.5 / LiF 13.0 / Li₂S 12.2 / Li₅AlO₄ 9.5 / Li₃PO₄ 8.9 / ZnO 4.3 / BN 0.5**; 저자 결론 = 환원안정성 **질화물 > 산화물 > 황화물 > 불화물** | **[Luo22]** `Fig. 4a–g` (AIMD 보조) | 우리 SEI gap 사다리: **LiCl 6.65 > Li₃PO₄ 5.73 > Li₂O 5.24 > Li₂S 3.90 ≫ Li₃P 0.70 eV** (`sei_products.json`) — **LiF 칸은 아직 비어 있다**(§E 기존 행) | 🔴 **방향이 반대로 보이지만 두 지표가 다른 것을 잰다** — 우리 것은 **전자 누설**(gap), Luo 것은 **원자 상호확산**(Bader/구조). ⛔ **그리고 이 서열을 그대로 인용하면 안 된다**: 인공 SEI 두께가 **5–6 Å(1–2 격자)** 뿐이고, **LiF 는 Li 금속에 열역학적으로 안정**한 대표 물질인데 "Li–F 가 깨졌다"고 나온다 = **두께 인공물 의심**. ⇒ 우리 LiF 행은 **유지**하되 "두께 의존성 미검증" 단서를 붙인다 |
| **★★★ 계보 8편 중 *유일하게 음극 코팅*을 다룬 편 — 축이 뒤집힌다(절반만) + 계면이 사라진다** | **[Honrao21]** `Fig. 1`·`S3`–`S6`(x축 전부 `Reduction potential`) · `Table S1` | 우리 `reduction_limit_V` **1.242** / `ocv_self_decomposition_V` **1.717 V** | 🟡 **축은 뒤집힌다**: 스크리닝 그림 5장 전부의 x축이 **환원전위**이고 코팅 판정이 **`V_red = 0 V` 불리언**(문턱 아님). 산화한계는 *"창 ≥1 V"* 로 **강등**. **[Nolan21]** 이 `E_d=0` → `\|E_d\|<0.05` 로 *완화*했던 흐름과 **반대**다 — `Fig. 1` 픽셀에서 **LLZO 가 0.050 V 라서 코팅 목록에서 빠진다**. ⛔ **그러나 우리 1.242 V 가 주역이 되지는 않는다**(축 B 의 정의 항 참조 — 그 자리는 1.717 V). ⛔⛔ **가장 큰 뒤집힘은 계면이 사라진 것**: `E_d`·pseudo-binary **0건**. 본문이 *"stability against Li metal on one side, and **the electrolyte on the other**"* 로 코팅 요건을 양면 선언해 놓고 **전해질 쪽 면을 한 번도 계산하지 않고**, Li 쪽조차 *"자기 창의 아랫변이 0인가"* 라는 **단독 물성**으로 대신한다 ⇒ **이 편을 "코팅 선정 방법"으로 인용할 수 없다** |
| **★★ 그들 판정 결과 = Li 금속 코팅 26종, 그중 *할라이드가 15종(58 %)*. ⛔ 우리 db 절대값과 같은 표 금지** | **[Honrao21]** `Table S1` 전수(digest §3a) | (대응값 없음 — 우리는 코팅 스크리닝을 안 했다) | 🟢 **문헌 소환값 표로만**: `Sr₄Li(BN₂)₃` 0.109 eV/1.39 V · **`Li₂O` 0.259/2.90** · **`Li₂S` 0.262/2.13** · `Li₂Se` 0.327/1.89 · **`LiCl` 0.349/4.25** · `LiBr` 0.350/3.14 · `LiI` 0.352/2.47 · `LiYO₂` 0.411/2.92 · `Li₇La₃Hf₂O₁₂` 0.470/3.02 · **`LiF` 0.536/6.36**. ★ **창은 양이온이 아니라 음이온이 정한다** — Cl 계 3종 전부 **4.25**, I 계 5종 전부 **2.35**, Br 계 2.96/3.14 (준안정이면 **분해산물의 창으로 치환**하는 그들 규약의 직접 귀결). ★ **트레이드오프**: 장벽 최저 4종의 창은 1.39–2.90 인데 창 최대 `LiF`(6.36)의 장벽은 **0.536 으로 자기 SE 게이트 밖** ⇒ **"통하면서 넓은" 코팅이 이 데이터에 없다**(논문 미언급). 🔑 **`Li₂S` 창 2.13 V** 는 우리 **S²⁻-limited 산화 onset** 서술의 외부 보강 1점(⛔ 같은 표 금지) |
| **⚠⚠ 질화물 서사가 결과와 반대다 — *"이 논문은 질화물 코팅을 지지한다"* 로 인용하면 틀린다** | **[Honrao21]** 서론(ref 57 Zhu 2017) · `Fig. S6` 캡션 ↔ `Table S1` | — | 🔴 **본문↔결과 어긋남**: 서론이 *"nitrides have a significantly lower reduction potential … making them more suitable for anode coatings"* 라 하고 `Fig. S6` 캡션도 *"Nitrides have the lowest reduction potentials"* 라 하는데, **`Table S1` 26종 중 질화물은 `Sr₄Li(BN₂)₃`·`Li₂CN₂` 둘뿐**이고 `Fig. S6` 에서 `V_red=0` 에 선 질화물 **6종**(`Li₃N` 0.284 · `Li₃BN₂` 0.267 · `Li₃AlN₂` 0.415 · `Li₂SiN₂` 0.405 · `Li₃ScN₂` 0.438 · `Li₃YN₂` 0.465, 전부 figure-read)이 **전원 목록에 없다**. 원인은 *"창 ≥1 V"* 게이트일 것이 거의 확실하나(질화물 산화한계 ~1 V) **논문이 한 줄도 설명하지 않는다**. 같은 유형: **`Li₉S₃N`**(초록 헤드라인 후보 · `V_red`=0.000 · 장벽 0.185)도 `Table S1` 에 없다 |
| **★ `Li₃PS₄` 환원 4계단 = 우리 환원 경로 서술의 외부 확인 1건** | **[Honrao21]** `Fig. S2` (본 digest 픽셀 판독) | 우리 `oxidation_stability.json` `reduction_identical` 주석 | 🟢 **일치**. 그들 계단: **1.702**(창 아랫변) → 1.262 → 1.156 → 0.926 → **0.867** 아래 `Li₂S + Li₃P`(uptake 8). 본문은 *"uptakes Li to form Li₂S and P"* 라고 **한 문장으로 뭉개지만**, 그림은 **P 의 단계적 리튬화**(P → LiP → Li₃P)를 계단으로 보여 준다 — 우리 주석 *"P⁵⁺ → P³⁻/P⁰ (Li₃PS₄ → P → LiP → Li₃P), S²⁻ 는 Li₂S 로 남고 LiCl 동반"* 과 **순서가 같다**. ⛔ 값(V)은 이식 금지(조성·phase set 다름), **경로 순서만** |
| **★ `Li₆PClO₅`(= Li₆PO₅Cl, 산소 아지로다이트) `V_red` 0.690 V — 황화물 아지로다이트(1.722)보다 1.03 V 낮다** | **[Honrao21]** `Fig. 1`·`Fig. S5` (figure-read ≈, ±0.03 V) | 우리 **LPSOCl(+O)** 계 (canonical gap 2.2309 eV) | 🟡 **방향만 가져온다**: O 치환이 **cathodic limit 을 크게 내린다**(= Li 금속에 더 안정) 는 문헌 단서 **1점**. ⛔ **값 이식 금지** — ㉠ 전(全) O 치환 끝점이라 우리 부분 치환과 조성이 다르고 ㉡ 단일 점이며 ㉢ figure-read 다. 참고로 같은 그림의 `Li₃PO₄` 0.690 은 [Nolan21] 0.69·[Zhu15] 0.68 과 일치하므로 **그림의 계측 자체는 신뢰할 만하다** |
| **🔴🔴 Li₃P 논쟁에 *세 번째 입장*이 들어왔고, 그 오진이 대체재 선택을 오염시켰다** — 이 편은 Li₃P 를 *"**poor ionic transport capability**"* 로 규정한다(서론 유일 등장 1회, refs 13–15 재인용, **자체 측정·계산 0**). 우리(전자 누설)와도 `[Xiao20Rev]`(부동태 산물)와도 다르다. 그리고 그 진단을 따라 *"이온이 빠른 상"* 으로 **Li₃N**(CI-NEB **0.0103 eV**)을 골랐는데, **저자 자신의 `Fig. 1g` 가 Li₃N 을 다섯 코팅 중 최협갭으로 그린다** (figure-read 전도대 개시 ≈**1.1 eV** ‖ LiF ≈9.7 · LiBr ≈7.0 · LiCl ≈5.9 · Li₂O ≈4.4) | **[Li26FDI]** `Fig. 1g`·`Fig. 1h–l` + 서론 (⚠ 갭은 **논문 미인쇄**, 우리 DOS-문턱 figure-read — 우리 규율상 정본 아님) | `sei_products.json` 분류 **`insulator ≥4 / marginal 2–4 / conductor <2 eV = e⁻ leak`** · `sei_electronic.json` fixed-occ nscf: **Li₃P 0.7092**(*"좁은 갭"*) · Li₂S 3.4379 · Li₂O 4.986 · LiCl 6.2603 · Li₃PO₄ 5.9121 | 🔴 **우리 기준을 그대로 대면 Li₃N 도 `conductor-LEAK` 다** — Li₃P(0.70)와 같은 칸. ⇒ 이 설계가 도는 이유는 *"Li₃N 이 전자를 막아서"* 가 아니라 **LiF 가 Li 와 Li₃N 사이에 끼어서**(`Fig. 5g` 적층 순서)다. **즉 이 논문은 우리 "층 분업" 판정을 반박한 게 아니라 *전제로 깔고 우회*했다** — 정작 저자는 그렇게 말하지 않는다. ⭕ 저자도 구멍은 안다: *"the DOS result of Li₃N **only indicates the absence of significant interfacial electronic states** … whereas its role as a fast Li⁺-transport phase **cannot be inferred from DOS analysis alone**"* |
| **🔴 LiCl 이동장벽이 우리 표 안의 `[Lu]` 와 ≈10배 갈린다 — 우리 "LiCl = 저장벽 buffer" 행에 충돌 표기가 필요하다** — 이 편의 CI-NEB: **LiCl 0.4800 · LiBr 0.5615 · LiF 0.6367 eV** 이고, 본문이 명시적으로 못박는다 — *"LiCl/LiBr should be understood primarily as **interfacial homogenization components rather than rapid ion-conduction phases**"* | **[Li26FDI]** `Fig. 1i,k,l` (VASP CI-NEB, 10⁻⁵ eV / **0.02 eV Å⁻¹**) ↔ **[Lu]** `Fig. 6` (LiCl **0.05 eV**) | 우리 `sei_neb.json` = **`retracted: true`, `n_citable: 0`** (`v3/licl` 은 `Ea_forward_eV: None` 미완) → **우리는 심판을 못 본다** | 🔴 **두 문헌이 10배 갈리고 원인을 특정할 수 없다** — 양쪽 다 **결함 기구(공공 vs 침입형)를 안 밝혔다**(이온결정에서 이 둘은 통상 수 배 차이). ⚠ 앞으로 `[Lu]` 의 "LiCl 저장벽" 을 인용할 때 **이 충돌을 병기**한다. ⭕ 부수 소득: **"할라이드 SEI 가 Li⁺ 를 잘 통한다" 는 통념을 저자가 자기 계산으로 부인**한 드문 활자 |
| **LiF/LiCl–LiBr/Li₃N 3성분 인공 계면상 → CCD 0.398→3.581 mA cm⁻²(9×) · 대칭셀 800 h@0.398 · 풀셀 1 C 1000 사이클** (LiFSI@DME → LiCl/LiBr@THF → TMEDA 3단 습식, 총두께 **≈60 μm**) — 단성분: LiF-rich 1.393(3.5×) · Li₃N 0.796(2×) · LiCl/LiBr 0.597(1.5×) | **[Li26FDI]** `Fig. S8`–`S11` · `Fig. 5b` · `Fig. 6e` · `Table S1` | comp1/modelc 0 V 분해식 **Li₃P + 5 Li₂S + LiCl**(grand-potential) · `sei_products.json` 음극쪽 처방(O 도입 → Li₂O 로 Li₃P 대체) | 🟡 **방향은 같다**(전자차단 상을 Li 쪽에 깔면 CCD 가 오른다 — §E 진영 `[Li25]`·`[Wu26]`·`[LiInF]`·`[WangYO]`·`[Xu26NdO]` 와 동형). ⛔ **그러나 우리 산물 5종(Li₃PO₄·Li₂SO₄·Li₂S·LiCl·Li₃P) 관측은 0/5 다** — 이 논문엔 **S 2p·P 2p XPS 가 한 장도 없고 순환 후 XPS 도 0건**이며, 등장하는 LiCl 은 *분해산물이 아니라 뿌린 코팅*이다. 같은 축의 `[Li25]`·`[Wu26]`·`[WangYO]` 가 순환 후 XPS 로 Li₂S/Li₃P/LiCl 를 직접 잡은 것과 비교해 **명확한 열위**. 🔴 성능 인용 시 **초록의 `77.1 over 1000 cycles` 를 그대로 옮기면 틀린다** — 1000번째는 **≈47 mAh g⁻¹**(Table S1 유지율 61.2 % 검산 + `Fig. 6e` figure-read ≈48) |
> **🔑 화해 (정직)**: 같은 LPSCl1.5인데 [Lu]는 "Cl-rich 유리", [GG]는 "moderate 유리"로 정반대. 둘 다 **"전자절연 passivation(LiCl) 형성 = dendrite 억제 관건"** 엔 동의. 차이는 **Cl '양'이 아니라 Cl '자리(4d)'**: [Lu]의 high-4d-Cl은 metastable(E_hull +15.2)이라 자기분해→LiCl, [GG]의 조성-평균 관점은 이 자리 불안정성을 못 봄. → **deck 결론: "음극엔 Cl-rich 무조건 유리 ✗ / 전자절연 LiCl interphase 형성되면 ✓, 형성 여부는 4d-Cl 점유가 좌우"**. (상세 = `papers/lu2025_tailoring_cl_rich_anode_licl.md` §13)
> **+ [Yang25] 합류 (RE-도핑 route, 2026-07-14)**: La-O 도핑도 결국 같은 결 — **음극 이점의 실체는 전자절연 LiCl(+RE⁰) interphase**이고(결론 원문 "La and LiCl"), 그 위에 얹힌 "LaCl₃ 1D 채널" 서사는 무증거 가설(SI 정독 확정). 우리 nd hull이 이 계열의 열역학 문법을 제공: **Li 접촉면에 RECl₃는 못 산다(→LiCl+RE⁰), RECl₃는 ≥2.6 V 산화측 전용** — RE-doped 논문의 음극 도식을 읽을 때 항상 이 문법으로 교정.

## F. 도핑 (계면 전자구조 엔지니어링)
| 주장 | 출처 | 우리 연결 |
|---|---|---|
| **★ 도판트 선택의 *계열* 근거 — `Table 1` 이 음이온 X × 양이온 M 을 Li 금속 대비 **stable / SEI former / MCI former** 로 분류한다** (Li–M–X 상도 근거, ref.224·233 + MP). **O 화학·S 화학 모두 "lanthanide series" 가 stable 열**에 있다 | **[Xiao20Rev]** `Table 1` | 우리 **Nd 도핑**(Nd₂O₃ → NdPO₄·NdOCl·NdCl₃ 등 광갭 산물)의 계열 수준 지지. 🟡 **Nd 개별 검증이 아니다** — ⛔ *"Nd 가 안정하다고 문헌이 말한다"* 로 쓰지 말고 **"란타나이드 계열이 O·S 화학에서 Li 금속 대비 안정으로 분류된다"** 로 쓴다. (⚠ 원 MERGE-BLOCK 은 4열이었고 이 표는 3열이라 **MERGE 때 열을 재배치**했다 — 내용은 그대로) |
| **★★ InF₃(In³⁺+3F⁻) 이원 공도핑 — "한 염 두 도펀트" 계보의 *자리 배정 원본*(2024)이자 A13 판정 논문**: **In→P_4b**(E_f **+0.32** vs Li48h −0.49 / Li24g −0.79 eV, `Fig. S4a`; XPS InS₄⁵⁻ + Raman In–S 310 cm⁻¹) · **F→Cl_4a**(E_f **+0.81** vs Cl4d +0.64 ≫ PS₄-S −1.56 / InS₄-S −1.24, `Fig. S4b`). 성적(x=0.06): σ 4.8→**4.0**(−17 %) · σ_e **6×↓** · CCD **2.5×↑** · H₂S **3.82→1.16 cm³/g** · 용매 σ 보존 **3.4×↑** ⇒ **"σ 를 팔아 3 축(대기·용매·Li 금속)을 산다"** — [Yang25]·[LiGaF] 와 같은 트레이드 **3번째 정량 사례** | **[LiInF]** (**[LiGaF] 가 이 자리 배정을 ref [34] 로 그대로 인용**) | **🔑 자리 충돌 3번째**: 우리 `doping_cascade_trivalent_M3.json` 은 **3가 champion 26 종 전원 Li_24g · P_4b 0 건**. ⇒ **In@P_4b vs In@Li_24g 총에너지를 우리 규율로 재는 계산이 [Yang25](La)·[LiGaF](Ga) 에 이어 세 번째로 요청됨 — 한 번에 처리**(digest §8e-①) |
| **★★ 이 계열에서 In/F 기여가 *두 축에서* 실제로 분해된 유일 사례 — 그리고 두 축의 부호가 반대다** | **[LiInF]** `Fig. S8`(σ, 실험 dose-matched) + `Fig. S22`(H₂O 흡착, 계산 4 슬랩) | **σ 축: In↑(4.8→7.0) / F↓(4.8→4.3)** ↔ **수분 축: F(−0.15 eV) > In(−0.12 eV)**, 공도핑 −0.32 eV = **초가법 +0.05**. ⚠ **유기용매·CCD·Li 금속 축은 pristine vs co-doped 2 점뿐 = 미분리** — **[Fan26] 리뷰가 인용한 축이 하필 미분리 축**. ⇒ 리뷰어 **A13** 은 "분리를 요구" 가 아니라 **"축마다 담당 원소가 뒤집히는데 통합 문장이 그것을 지운다"** 로 쓸 것(digest §13) |
| **★ [Fan26] 리뷰 인용문 *"enhances lattice bond energy and reduces polarizability"* 는 원 논문에 없다** — 원문 전수검색: `polarizability` **0회** · `bond energy` **0회** · `lattice energy` **0회**. 원문의 "lower **polarization rate**" 는 **F⁻ 가 σ 를 깎는 이유(불이익)** | **[LiInF]** vs **[Fan26]** §3.2 Q9 | **리뷰어 A12 확정.** "lattice bond energy" 에 대응할 정량량이 이 논문에 **존재하지 않는다** — 가장 가까운 것은 (a) 정성 HSAB (b) 자리 형성E (c) **분자–표면 흡착E**(격자 결합에너지가 아님). **우리는 같은 양을 ICOHP 로 잰다** ⇒ In–S vs P–S ICOHP 가 리뷰에 붙일 우리 답(digest §8e-②) |
| **★ In 선택의 근거가 [Zhu20] 이고, 우리 SI 전수 전사본으로 직접 검산된다** — 본문 ref [20] = P. Zhu & Y. Mo, *Angew* 2020, 59, 17472 | **[LiInF]** 본문 + **[Zhu20]** `db/properties/zhu2020_si_hydrolysis_energies.csv` | 이성분 가수분해 ΔE(양수=공기 안정, 46 종): **In₂S₃ +0.599(9위) > Sb₂S₃ +0.535 > SnS₂ +0.441 > Ga₂S₃ +0.362(18위) > Li₂S +0.225(22위) > P₂S₅ −0.156(25위)** ⇒ **P→In = +0.755 eV 개선, 논문 주장과 방향 완전 일치**. **In > Ga** 는 그룹이 InF₃(2024)→GaF₃(2026) 순으로 간 것과 정합. ⚠ 논문의 "In³⁺ = highest stability" 는 **9 위**라 부정확(1–8 위 Au₂S·Cu₂S·ZnS 는 환원 안정성에서 탈락) ⚠ **이성분 프록시**(`kb/open_items.md` #11) |
| **⚠ 우리 `+B₂O₃` 와 "동형 기전"인가 — *논리 형태까지만* 맞다 (판정)** | **[LiInF]** vs 우리 B₂O₃ | **✓ 논리 동형**(취약 단위를 강결합으로 묶는다) / **✗ 축이 다르다**: 취약점이 **P⁵⁺(친핵 공격)** vs **free-S²⁻(산화)**, 관측량이 **분자–표면 흡착E** vs **자리분해 PDOS ⟨3p⟩+산화 onset**, 그리고 **[Zhu20] 대기 축에서 In₂S₃ +0.599(9/46위) ↔ B₂S₃ −0.901(44/46위) = 정반대**. ⇒ **[Fan26] digest 의 "✓ 동형 기전" 항목에 반드시 축 단서를 달 것** — B 는 산화 축을 고치고 **대기 축은 최하위군**이다 |
| ⚠ **`Fig. 4f` 만화가 실제 조성을 지운다** — x=0.06 에서 사면체의 **94 % 가 여전히 PS₄** 인데 "PS₄ 분해 / InS₄ 무분해" 로 그린다. 정작 `Fig. S24b` 는 co-doped 계에서도 **"P-site"** 흡착을 계산한다 ⇒ 개선의 실체는 **"In 이 이웃 P 의 전자환경을 바꿨다"(2차 근접 효과)** | **[LiInF]** | 이 구분이 없으면 **왜 6 % 면 되는가(스케일링)** 를 설명할 수 없다. **우리 B–S 도 같은 질문을 받는다** — B 2 개가 free-S 를 어디까지 안정화하는지 **거리 의존성**을 우리가 답할 수 있다(site-PDOS) |
| **Y₂O₃(Y³⁺+O²⁻) 공도핑 — "한 염 두 도펀트" 6번째**([Taklu]CuCl→[Liu23]MgF₂→[Li25]CuBr₂→[Yang25]La₂O₃→[LiGaF]GaF₃→본편) → σ+28%·σ_e↓·H₂S↓·CCD 2×·Li₂O interphase. **Y@P(4b)+2Li carrier 주장**(형성E Δ0.0123 eV/atom 2배열+constrained Rietveld) | **[WangYO]** | **⚠ 우리 cascade와 site-preference 정면 충돌**: v23 M³⁺ 26/26 전원 **Li_24g**(O@S_16e; **Y₂O₃ 포함**, host=modelc, UMA) — Y@P면 +2Li(carrier↑), Y@Li면 −2Li(donor-blocking)로 **σ 기전 부호가 반대**. 방법·host 의존이라 어느 쪽도 확정 아님 → **comp1 host에서 Y@4b vs Y@24g 동일기준 DFT 검증 계산 후보 1순위**(`doping_cascade_trivalent_M3.json` site_rule 참조). cascade bvs_li_proxy 0.83–0.92(M³⁺ 무관 균일)와 "장벽 절반"도 상충 |
| MgClO(Mg+Cl+O) 공도핑 → 계면 metallic→gapped (s-p/p-p 혼성) → 환원 분해 차단 | [Ke] | **우리 cascade(Mg/Cl/O/F 도판트 스크리닝)의 직접 문헌 동기 ①** |
| **MgF₂(Mg+F) 공도핑** → 음극 redox 억제(실험: CCD 0.6→1.4, σ_e 8×↓). ⚠메커니즘("MgS₄ 사면체 s-p 혼성, Mg@P자리")은 **구조모델 under-determined**(lab XRD로 Mg@P vs Mg@Li 구분 불가, 자기 ELF는 이온결합, 반경상 Mg→Li) → `papers/liu2023…md` §12b | **[Liu23]** | cascade 동기 ②는 **실험적 방향**(Mg 도핑이 음극 도움)만; *기전*은 미확정으로 인용 |
| **CuBr₂(Cu양이온+Br음이온) 이원 공도핑** → σ↑(10.3)·gap↑(2.41)·σ_e↓·CCD↑(1.9)·대기안정 *동시*. Cu²⁺/P⁵⁺(Li⁺추가·S²⁻전하밀도↓)·Br→4a/4d(무질서); **HSAB: soft Cu–S>P–S → 가수분해 저항**(물흡착 ΔE 0.29→2.42 eV) | **[Li25]** (exp+DFT) | cascade는 **양이온+음이온 동시** 도판트도 스크리닝 대상(Mg/Cl/O/F 외 Cu/Br 추가); 우리 **결합강도→안정**(oxophilicity·ICOHP P–O −8.43) 논리의 다른 화학 사례 | **cascade 동기 ③(양이온+음이온 동시)**: "어떤 *쌍*이 σ·전자절연·대기안정을 동시에 주나"의 외부 사례. **단 변수 다중(Cu·Br 분리 안 됨)·DFT 파라미터 미명시 → 정성 동기로만**. 대기안정(가수분해 ΔE)은 우리 0K hull 밖(기체상 X) |
| **CuCl(Cu양이온+Cl음이온) 이원 공도핑 — dual-doping *원조*(2021)** → σ↑(4.34)·σ_e↓(1.49e-9)·CCD↑(3.0)·대기안정 *동시*. Cu→4b(P자리)·Cl→4a/4c·48h-Li 거리↓; **(P/Cu)S₄ rigid framework + Cu₃PS₄ 형성**(HSAB soft-acid Cu→oxophilicity↓→**H₂S 1.07→0.49 cm³/g**) | **[Taklu]** (exp + DFT Li-path) | cascade 양이온+음이온 동시 도판트 스크리닝 대상; **CuCl 단일 염으로 Cu·Cl 동시 공급** = "한 염으로 두 도펀트"(metal-halide MCl/MBr 형태 co-doping 후보 근거); oxophilicity descriptor의 또 다른 실증 | **cascade 동기 ③의 *원조 사례* (모체가 우리 comp1=Li₆PS₅Cl)**: [Li25] CuBr₂의 4년 선행. **단 [Li25]는 wide-gap 분해산물(LiCl/LiBr) 절연이 음극 레버인데, [Taklu]는 *모체 (P/Cu)S₄ rigid화*가 레버**(메커니즘 다름, 축 E 참조). 대기안정 산물 **Cu₃PS₄를 XRD로 동정**(li2025 ΔE보다 산물 증거 구체적). ⚠ 변수 다중(Cu·Cl 분리 안 됨)·DFT functional 미상·"8 V ESW"는 kinetic over-claim(축 B 주의)·가수분해는 우리 0K hull 밖 |
| **RE₂O₃(La+O) 이원 공도핑 — 우리 Nd₂O₃의 최근접 실험 자매** → σ 희생(0.65×)·대기안정(P–O)·CCD 3.4×·500cyc 83.6% *동시*; **La₂O₃ 단일 염으로 RE³⁺+O²⁻ 동시 공급**(La→4b "가정"·O→PS₄). 같은 그룹 M-O 시리즈: Sn-O(ref15)·Sb/Bi-O(refs34,35)·**Nb-O**(EA 509,145341)·La-O(본편) = [Bai] "metal+O cooperate" 처방의 실험 계열 | **[Yang25]** (exp, 계산 0) | **우리 Nd₂O₃ cascade가 이 시리즈의 4f-RE 칸 + 열역학 지도(hull) 층**: σ300 0.52×(같은 비용)·O@PS₄ −0.67 eV/O·ICOHP P–O −8.43(그들 P–O 주장의 기전)·SEI/CEI 산물 지도(La⁰+LiCl↔우리 치환반응; NdPO₄/NdCl₃ ≥2.45/2.62 V 양극 passivator). **자리 차이 주의: La@4b(P, +2Li/La) vs 우리 Nd@Li(3Li→Nd)** — 둘 다 확증 부족(그들 명목-고정 Rietveld·우리 모델 선택) → site-preference 계산으로 판정 가능 = 후속 |
| **Nd₂O₃(Nd+O) 이원 공도핑 — "한 염 두 도펀트" 7번째([Taklu]CuCl→[Liu23]MgF₂→[Li25]CuBr₂→[Yang25]La₂O₃→[LiGaF]GaF₃→[WangYO]Y₂O₃→본편)·우리 도펀트와 동일 원소 최초** → σ 1.25×(x=0.025)·σ_e 4.7×↓·CCD 2.9×·H₂S 2.3×↓·풀셀 1000cyc *동시* — [Yang25] La-O의 "σ 희생(0.65×)" 없이 σ까지 얻었다는 주장이 차별점(단 통계 0·LiCl 상분리 동반·희석 x라 직접 비교 불가). **Nd@P(4b) 배정은 무증거**("is inferred" 자인·Rietveld/a/NMR/EXAFS 0) — [WangYO] Y@P(방법론 무효 판정)·[Yang25] La@4b(명목-고정 템플릿)에 이은 **관행적 P-site 가정 계보 3번째, 증거 강도는 셋 중 최약** | **[Xu26NdO]** (exp, 계산 0) | **우리 cascade site-rule(26/26 M³⁺=Li_24g, 0 P_4b)·Track1 vs Track2 ΔE 대결(P1, Track1 relax 완료·Track2 2–3배열만 신규)이 유일한 정량 판정** — 그들 명목식이 우리 Track2 컨트롤과 동일하므로 Paper#2에서 "실험 관찰 ↔ 계산 자리판정" 구도로 인용·차별화. σ_e 4.7×↓는 PI 실험의 독립 재현 = 우리 "벌크 gap 1.632로 축소·감소는 interphase percolation" 해석(electronic.json)이 채울 공백 | **경쟁·자리충돌** |
| **GaF₃(Ga³⁺+3F⁻) 이원 공도핑 — "한 염 두 도펀트" 5번째 사례이자 *역할 분해가 가장 깨끗한* 사례**: Ga→**P_4b**(GaS₄⁵⁻; 증거는 **XPS S 2p 162.9/161.7 eV** + 자기인용 InF₃ 논문 — **⛔ [정정] Raman 284 cm⁻¹는 본문이 x>6 % 불순물상으로 귀속하므로 자리 증거가 아니다**)·F→**Cl 4a/4d**(occ 0.04/0.08, ⚠명목 고정). 전하균형 자기정합(+2 Li/Ga → Li 5.5→5.58; **Rietveld Li 합 = 5.58 검산 일치**). 자기 선행 = **InF₃**(ref[4] AEM 2024) → **MX₃ = 3가 금속 + 할로겐 동시 공급** 계열 | **[LiGaF]** | cascade에 **Ga는 Ga₂O₃ 형태만**(de −0.59 = 3가 중 최약, score 0.55–0.56 하위), **F는 LiF/MgF₂/ScF₃/YF₃/NdF₃만** — **MX₃(3가+할로겐) 칸이 비어 있다** → GaF₃·InF₃ 추가 후보 | **🔑 자리 충돌 = 지금 계산으로 끝낼 수 있는 질문**: 문헌 5편([Taklu]Cu·[Liu23]Mg·[Li25]Cu·[Yang25]La·본편 Ga)이 전부 **M→P_4b**를 전제하는데, 우리 `doping_cascade_trivalent_M3.json`은 **3가 champion 26종 전원 Li_24g·P_4b 0건**(그리고 파일 자체가 "**NO DFT yet**" 자인). 양쪽 근거가 다 약함(그들=Rietveld 고정+자기인용 / 우리=UMA 스크리닝 단독) → **Li_24g vs P_4b × 동반음이온 O vs F 의 2×2 형성E DFT**면 판정 + "동반 음이온이 자리를 바꾸나"까지 동시 응답. [Yang25]에 이은 **두 번째 동일 요청** |
| **F 도핑의 기전은 "창 확대"가 아니라 *전자 차단 + LiF SEI*** — DC 분극에서 F 함유 시료만 σ_e가 0으로, 순환 후 LiF 검출, 자체 DOS로 **LiF 7.4 eV = 후보 산물 중 최광폭** | **[LiGaF]**, **[Liu23]**(MgF₂→LiF), **[KimICCF]**(FEC→LiF) | 우리 `sei_products.json`(LiCl 6.65·Li₂O 5.24·Li₃PO₄ 5.73·NdPO₄ 5.55)에 **LiF 행 없음** | **✗ 우리 파일의 실제 공백** — F계 도판트가 cascade에 5종 있는데 정작 그 대표 산물 LiF의 갭 칸이 비었다. **즉시 보완 가능**(MP 조회 1건) |
| **⚠ H₂O 흡착E는 *논문마다 부호규약·표면종단·vdW가 달라* 절대값 교차인용 불가** — [LiGaF] `ΔE=E_surf+E_H2O−E_복합체`, **양수↑=흡습↑**, 값 0.22–0.64 eV(공도핑 0.33/0.22로 ≈절반, 단 **여전히 양수=소수성 아님**) / [Fan26] 리뷰 **−1.63 → −1.19 eV**(음수 규약) / [Li25] **0.29 → 2.42 eV**(또 다른 규약). 셋 다 **종단 미기재**, [LiGaF]는 **vdW도 미기재** | **[LiGaF]**, [Fan26], [Li25] | 우리 수분(가수분해) 축 = **0K hull 밖 공백**([Zhu20] 랭킹 소환만) | **✗ 공백 + 방법 처방**: 우리가 하면 **[Qian26] Table S2의 LPSCl 저지수 종단 6종(γ 0.40–0.72 J/m²)** 위에서 계산 → **종단을 통제한 최초의 물-흡착 비교**가 된다. **문헌 3편의 흡착E를 같은 표에 올리는 것은 금지** |
| **HSAB 대기안정 도핑의 *열역학 원전*: cation별 가수분해 ΔG(eV/H₂O) 전수 지도** — [Taklu] CuCl(Cu=후기TM 최상위)·[Li25] CuBr₂·[Ma24] Sn/Sb·[Bai] "HSAB Sn/Sb" 처방이 전부 이 지도 위 칸; **In³⁺=수분 최고+환원 양호(미개척 후보 명시)**·후기TM Zn/Cd/Cu/Ag 최고·**B³⁺ 최악** | **[Zhu20]** (2020, 경험칙→정량화) | 우리 cascade에 **수분축 열 추가의 랭킹 원판**(Fig 2·S2 판독; 정확값 전표는 SI xlsx 미보유) + 우리 도판트 중 **B(+B₂O₃)는 Zhu 지도상 수분 최악급 → B–O 배위 유지 확인 필수**; Cu/Zn/In 계열은 수분 가점. ⚠ Li–M–S 대표 화합물 기준(argyrodite 고용체 아님) — 우리 조성 값은 우리가 직접 계산(§H) |
| SEI = 전자절연(Li₂O 8.37 eV)+친리튬(LiMg) | [Ke] | 우리 **Li₃N**(음극 interphase) 연구와 같은 패밀리 |
| 도판트 음극 호환성 descriptor: 계면 binding energy(J/m²), E_F metallic 여부 | [Ke] | 우리 cascade 평가에 차용 가능 |
| **음이온 자리(4d) Cl 점유 엔지니어링** → 자기분해 LiCl interphase (원소도핑 아닌 *자리* 레버) | **[Lu]** | modelc Cl-rich의 4a/4d 분포 명시하면 Lu와 직접 연결 |
| **interphase 품질 descriptor 3종**: 전자 gap 넓음 + Li⁺장벽 낮음 + Poisson 연성 | **[Lu]** Fig6d | Ke binding-E와 묶어 음극 interphase 평가셋 완성 |
| **O²⁻ 옥시설파이드 도핑(Li₆PS₄OCl/Li₆.₂₅PS₄.₂₅Cl₀.₇₅): 전자누출↓·ECW확대·O–P>S–P·대기내성↑·기계순응 SEI** | **[Kang]** §5.1(b) Fig13c,d (refs128–130) | **우리 Nd2O3/O-doping cascade** (sei_products.json: Li₃PO₄ 5.73·Li₂O 5.24·NdPO₄ 5.55 eV가 Li₃P 0.70 대체; eos modelc_nd B0 18.9) | **🔑🔑 우리 cascade의 리뷰 내 직접 정당화**. 리뷰 "reduced electron leakage" = 우리 wide-gap O-derived 산물 정량. ⚠ 우리 hull: intrinsic 창 narrows(kinetic passivation) — 리뷰 CV ECW확대와 *다른 축* |
| **Li₃PO₄ buffer: CAM 산소방출 억제 + 기계약한 sulfate 형성 방지 + 고전압 parasitic↓** | **[Kang]** §5.1(c) Fig13e (ref128) | Nd cascade: Li₃PO₄가 bulk-GB·cathode passivation으로 persist(0.69–3.06 V) | **✓ 동일 역할** (우리 직접 hull staircase가 실증) |
| **BH₄⁻ 도핑: CCD 2.6→7.3 mA/cm², 얇은 tri-layer SEI(Li₃P/LiBH₄/Li₂S) 기계순응·전자절연** | **[Kang]** §5.1(a) Fig13a,b (ref127) | (우리 미계산) — doping cascade 47종 스크리닝의 동기 | 우리 cascade가 "어떤 도판트가 전자절연 SEI를 주나" 예측하는 방향성 동기 |
| **"한 변수 고치면 다른 변수 바뀐다 → 통합 설계 필요"** (도핑이 σ·기계·ECW·SEI 동시 변경) | **[Kang]** §6 트렌드3 | 우리 **cascade v23**: stability↔Li-mobility blocking trade-off, 기계+안정성 동시 스크리닝(47 dopant) | **🔑 방법 일치** — 우리 cascade의 trade-off 설계가 곧 리뷰 "modifying one parameter alters others"의 계산 구현 |
| **HT 게이트 스크리닝 방법 원전 + "V_ox↔Li 함량" trade-off 정량**: 깔때기(104,082→184→3종)·게이트 임계값(Eg 0.5/E_hull 5 meV/V_ox 4.0·V_red 2.7/ΔE_rxt 100 meV)·**Li분율↑⇔V_ox↓**(V_ox≥5 V→Li분율≤0.20, Fig 7)·O-공유결합 위계(meta>pyro>ortho·B–O 806 kJ/mol) | **[Xiao19]** ⭐ (코팅 *물질* 스크리닝 — 도핑 아님) | **우리 cascade의 게이트 골격 원전**(§B 🧬 note·digest §7c 1:1 표): 계승=상안정·grand-potential ESW·전도 프록시 / 우리 추가=기계 35 %·테마 조합·co-doping ML·UMA-상대 / 우리 공백=양극 반응성 게이트·10⁵ 풀. **그들 "V_ox↔Li분율" trade-off = 우리 stability↔blocking trade-off의 동형 구조**(레버만: 조성 Li분율 vs 도판트 blocking). ⚠ [Sundar]와 같은 규율 — 코팅≠도핑, 랭킹/수치 force-fit 금지; **붕산염 3축 분리**(산화·계면 화학안정↑[Xiao 코팅물질 한정 — ⛔ **우리 B₂O₃ +0.18 V 는 2026-08-16 철회**, 같은 자리 plain 조성은 2.034 V 로 host 아래] / Li 이동성↓ 위험[Xiao LiBa(B₃O₅)₃ E_m 1.96 eV] / 가수분해 최악급[Zhu20]) 없이 "B가 좋다" 금지 |
| **★★ RE³⁺ 도핑의 *계산* 선례 — [Xu26NdO]·[Yang25]·[WangYO] 가 전부 계산 0건인 자리를 이 편이 유일하게 채운다. 단 계가 다르다(할라이드)**: RE³⁺(Er/Nd) 를 **Zr 8면체 자리**에 넣고(`Fig. 2a` 다면체 갤러리 4개 전부 8면체), 전하보상은 **화학식에 Li 원자를 도펀트당 1개 실제 추가 → 중성 셀**(N_Li=8(2+x), 우리 σ 역산 11/11 재현으로 확정). **배경전하·공공 스킴·결함형성E·전하보정 0건.** ⛔ **보상 Li 를 어느 자리에 넣었는지는 미기재** — 배열 열거·SQS·선택규칙 없이 조성당 배열 1개 | **[Ren26]** §21.1 (⛔프리프린트·⚠할라이드 Li₂ZrCl₆) | **우리 `ndo_lpscl16` 과 회계 방식이 같다**: `Cl₆Li₂₆Nd₂O₃P₂S₁₅`(+42/−42) · `Cl₈Li₃₁Nd₂O₃P₃S₁₉`(+52/−52) 둘 다 **정확히 중성**, 모(母) 대비 **P 2개↓·Li 4개↑ = +2 Li/Nd**(그들은 +1 Li/도펀트). ⇒ **"중성 셀 + 명시 Li 추가"는 문헌 표준이고 이 편이 외부 선례다.** ⛔ **자리 논쟁은 이 편이 해결해 주지 않는다** — 그들의 Zr 8면체는 우리 argyrodite 의 P(4b, **사면체**) 나 Li(24g/48h) 어느 쪽과도 등가가 아니다. `doping_cascade_trivalent_M3.json`(M³⁺ 26/26 = Li_24g, P_4b 0건) vs Rietveld `Nd8@(½,½,½)=P자리` 의 충돌은 **여전히 우리 DFT 로만 판정된다** |
| **⚠⚠ 그 계산 선례가 *반례 카탈로그*이기도 하다 — RE³⁺ 도핑 계산을 설계할 때 피해야 할 4가지**: ①보상 Li 자리 미문서화 → **matched-x 에서 Er↔Nd 우열이 통째로 뒤집힌다**(x≤0.375 Nd ×4.9–21.0 압승 / x≥0.5 Er ×10–16 압승, 한 계열 σ 진동 Er 34.8배·Nd 14.7배; 50 ps·Li 16–21개·단일시드·배열 1개) ②**open-4f + DFT+U 인데 U 값·스핀·점유행렬 정책 전부 미기재** → 조성 선택 근거인 E_coh 가 **비단조**(Er 계단 −0.46/−0.45/−0.41/**−1.46**/+0.51, 튀는 계단이 곧 선택된 조성) ③**VDOS 3패널이 정규화가 달라 비교 불가**(모드 수 5.6 % 차인데 진폭 4.2–4.6배, 지지구간은 도핑계가 더 넓다 = ∫g=3N 과 모순) + **Cl 밴드 상단 ≈5.0–5.1 (arb.) 불변** ④**질량 효과 미분리**(Zr→Er/Nd 는 k 불변이어도 M-투영 모드 −26.1 %/−20.5 %) | **[Ren26]** §21.3 · §21.5 · §21.6 (재분석은 **우리 것**) | **우리 `ndo_lpscl16` 보고량 카드가 이미 이 4개를 막고 있다 — 유지 근거로 쓴다**: ①→ **G1(6점 전부)·G2(두 셀이 다른 배열이면 *선택 실패로 보고*)·G3(<50 meV 면 "구별 불가")** ②→ **frozen-4f**(`Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF`, z=11) + "Nd 4f 주장 전면 금지" ③④→ 우리는 아직 VDOS 축이 없다. **열 때 질량 정규화를 처음부터 넣는다** — 우리 계는 **P(30.97)→Nd(144.24), ω ×0.463 (−53.7 %)** 로 그들보다 질량 항이 훨씬 크다 |

## G. ✅ 우리 계산이 문헌을 *검증*하는 지점 (강점)
| 우리 결과 | = 문헌 | 출처 |
|---|---|---|
| **Li₂S–Li₆PS₅Cl 조성선에 안정한 중간 결정상 없음 — 분해 산물 {Li₃PS₄, LiCl, Li₂S} 가 전 x 에서 동일** (UMA + MP-DFT 교차, 0층 2026-09-11, ⚠ post-hoc) | = 볼밀(500 rpm·1 h) Li₂S/LPSCl(x=0.778) 에서 **새 결정상 0** — 아지로다이트 XRD 피크 소멸·Li₂S 만 결정, XANES LCF 로 **LPSCl 절반이 LPS(Li₃PS₄)-like**, Raman PS₄³⁻ 425→~420. 즉 우리 ① 의 결정 평형 산물이 실험에서 **XRD-무음(비정질) 형태로** 나타난다. ⚠ **LiCl 관측·언급 0(Cl 행방 미보고)·Li₇PS₆ 언급 0** → 우리 ②(준안정 Li₇PS₆ + LiCl, −38.4 meV/atom)는 **지지도 반증도 아님**(결정 Li₇PS₆ 는 아지로다이트 패턴이라 피크 소멸과 양립 불가 → 결정형은 배제, 비정질형은 미판정) | **[Cronk26]** `Fig. S10a,b`·`Fig. 4f`·`Table S5` |
| **0 V 환원 분해식 `Li₃P + 5 Li₂S + LiCl`** — 세 산물 **전부** | = 순환 200 h 후 Li\|LPSC 계면 XPS에서 **Li₂S(S 2p 159.2 eV) + Li₃P(P 2p 130.9 eV) + LiCl** 전수 동정 (⚠ 정성 동정이지 화학량론 검증은 아님) | **[LiGaF]** 본문 Fig 4A,B |
| **onset 반응 (LiS4 제외)** `Li6PS5Cl→Li3PS4+LiCl+S+2Li` | = **[Zuo] Eq1 정확히 일치** (2 e⁻, 원소 S) | [Zuo] |
| modelc onset `→Li3PS4+1.6LiCl+0.4S+0.8Li` | = [Zuo] Eq2 거동 (전자 적게·LiCl 많이) | [Zuo] |
| 0-pressure ESW (OCV 1.717, onset **2.256** LiS4 제외) | = K_eff=0 (1.70–2.40), 격차 0.14 V | [GG] |
| **comp1 hull staircase 전 구간** (0 V Li₃P+5Li₂S+LiCl → 1.24 V +5 Li·P → 1.72 neutral Li₃PS₄+Li₂S+LiCl → 2.14/2.256 ox → 고전압 Cl 산화 종단) | = **[Zhu15] SI Table S2(f) 계단과 단계별 동일 화학**(0.87 +8 / 1.30 / **1.71 red≡우리 1.717** / 2.01 ox −2 Li / 2.88 PCl₃) — 환원측 경계 Δ0.007 V 불변·산화측만 DB 세대(MP2020 S-보정·LiS₄)로 +0.13~0.25 V | **[Zhu15]** (방법 원전의 계단을 우리 2026 hull이 현대판 재검증 — 산물 화학은 세대-불변, 산화 전압은 보정-민감) |
| 구속 ESW Cl-rich 확대 trend | = K_eff=20 거동 | [GG] |
| AIMD Ea/D Cl-rich 빠름 | = 실험 σ trend | [GG][Zuo][**Liu**] |
| **inter-cage 활성화 = Cl-rich σ↑ 물리** (우리 percolation·D↑) | = AIMD Li 확률밀도 intra→inter-cage 전이·MSD 3× (Cl-rich가 cage 사이 통로 개방) | **[Liu]** Fig 2e–g (직접 시각 증거) |
| VBM = S 3p (산화 onset을 S가 pin) | = HAXPES(VBM 불변) + DFT pDOS/COHP(비결합 S 3p=VBM, CB=P–S 반결합) + grand-potential 창 불변 + CV onset 불변 → "치환 무관 onset" | **[Banik]** (외부·Zeier+Mo; 우리 axis_1·VBM≠onset·grand-potential 방법의 동방법·동그룹 정답지) |
| **SEI 산물 밴드갭 위계 `sei_products.json`** (LiCl 6.65 > Li₂S **3.90** > Li₃P 0.70; 임계 insulator≥4 / marginal 2–4 / conductor<2) | = **외부 독립 PBE DOS가 순서·등급 완전 재현**: **LiF 7.4 > LiCl 6.2 > Li₂S 4.2 > Li₃P 1.1 eV**. 절대값 ±0.5 eV는 방법차(자체 PBE DOS 판독 vs MP 엔트리) | **[LiGaF]** Fig S15 — 우리 Nolan Type-3 절연-interphase 분류의 첫 외부 대조군. **단 우리 파일엔 LiF가 없다**(그들이 채워줌). ⚠ **내부 정정 필요**: 본 파일 §E 여러 행이 인용하는 "Li₂S **3.04**"는 `sei_products.json` 정본 **3.90**과 불일치(3.04는 `b2o3_sei_gaps.json`의 Li₃BS₃ 3.05 혼동 추정) — **4 eV 임계 바로 아래/위를 가르는 숫자**라 판정이 뒤집힌다 |
| 환원 산물 Li₃P+Li₂S+**LiCl** (LiCl = 전자절연 passivator) | = LPSCl(1.5) 환원; LiCl이 음극 passivation. **[Liu] = AIMD/XPS로 PS₄³⁻→LiₓPᵧ 환원 + LiCl-rich SEI 직접 관측 + Cl-rich가 *더 느린* 환원(kinetic)** | [Ke][GG][**Lu**][**Liu23**][**Li25**][**Liu**] |
| ★★ **Ta 계면 산물 2종을 양쪽 다 맞췄다** — 닫힌계 0 V `0.1667 TaCl₅+0.8333 Li → **Ta** + LiCl` / grand-potential 2.5 V vs LiCoO₂ `→ **LiTaO₃** + LiCl + Li₃PO₄` | = **[Wu26] XPS: SEI = 금속 Ta⁰(24.4/22.4 eV) + LiCl + LiBr + Li₂S + Li₃P · CEI = LiTaO₃(27.4/25.5 eV) + P₂S₅ + 원소 S** (+ ToF-SIMS TaO₃⁻/Ta⁺ 3D 분포) | **[Wu26]** (`cascade_stability_axes.csv` · `cascade_interface_{90,li}.jsonl` · `cascade_product_gaps.json`) |
| **`cascade_product_gaps.json` 이 계면 비대칭을 정량화** (LiTaO₃ 2.388 eV 절연 / Ta 0.0 eV 금속 / Li₅TaO₅ 3.902 / TaP·Ta₂P·TaS₃ 0.0) | = **[Wu26] 이 CEI 는 LiTaO₃, SEI 는 Ta⁰ 로 실측** ⇒ **같은 도펀트가 양극쪽엔 절연 CEI, 음극쪽엔 금속 SEI 를 만든다**는 우리 예측을 실험이 확인 | **[Wu26]** + `sei_products.json` 위계 |
| **sei_products.json 절연산물 순서 LiCl(6.65)≫Li₂S(3.90)** = "wide-gap halide=전자절연 SEI" | = 외부 그룹 독립 DFT PDOS **LiCl 6.13/LiBr 5.07/Li₂S 3.04 eV** (같은 순서) | **[Li25]** (+[Lu] LiCl 6.22) |
| **sei_products.json 절연산물 순서 LiCl(6.65)≫Li₂S(3.90)** = "wide-gap 산물=전자절연 interphase" | = 독립 HSE06 분해산물 gap **Li₂S < LiCl** (+ LiAlS₂/MgS 특히 큼) — 또 하나의 외부 DFT가 같은 순서 재확인 | **[Sundar]** |
| **계면 분해 분석 방법 = pymatgen `InterfaceReactions`** (우리 `interface_reactivity`/`GrandPotentialInterfacialReactivity`) | = Sundar가 12 산화물×3계면을 *동일 도구*로 스크린 → 우리 계면 방법이 **분야 표준**임을 외부 Argonne 그룹이 입증 (우리는 grand-potential 전압분해까지 = 우위) | **[Sundar]** |
| **"electron-blocking interphase가 분해 차단" 메커니즘** (우리 중심 주장) | = **LiF-rich SEI가 SE 분해(Li₂S) 억제** (실험 XPS) → 같은 그룹이 실험 입증 | **[KimICCF]** ⭐ |
| **"σ 병목 = interphase/microstructure, bulk 결정 아님"** | = 시트 σ 손실 원인 = 공동(34.2 %), 채우면 155 % 회복 | **[KimICCF]** ⭐ |
| **O-doping interphase가 전자절연(wide-gap)으로 e⁻ leak 차단** (우리 Nd cascade) | = §5.1(b) 옥시설파이드 "reduced electron leakage"·O–P>S–P; §5.1(c) Li₃PO₄ buffer | **[Kang]** ⭐ (우리 그룹 리뷰가 직접 전략으로 추천) |
| **SEI 전자절연성 = passivation/dendrite 억제 관건** (sei_products.json gap 분류) | = Nolan **Type1/2/3**(Fig5c); dendrite는 환원 SEI 좌우(Fig6c) | **[Kang]** ⭐ (개념 프레임; 우리가 gap 수치로 정량) |
| **산화 onset = grand-potential(thermo), 실험창은 kinetic** | = Fig1a(ref49 동일방법)·Fig1b thermo vs kinetic ECW | **[Kang]** ⭐ |
| **고전압 산화분해 산물 = P₂S₅계 + 원소 S + LiCl** (우리 voltage-resolved staircase) | = **식1** `2Li₆PS₅Cl→P₂S₅+5S+2LiCl+10e⁻+10Li⁺` (완전산화) → NCM 균질 chemical lithiation | **[Kang25]** ⭐ (우리 그룹 실험이 우리 grand-potential 분해화학을 간접 검증; 단 이로움=SOC-강하≠passivation, Nd와 다른 physics) |
| **황화물 SE 산화 onset "<2.5 V"** (우리 grand-potential 2.256 V, S²⁻-limited) | = Nature Energy *본문 명문화* "sulfide SEs … <2.5 V vs Li/Li⁺"(intro) + Fig 3a CV·3b 막대 → 5 V급 양극은 황화물 직접접촉 불가 → 불소계 차폐 SE 필요 | **[Son]** (외부·정량 일치; 우리 thermo onset이 5 V 논문의 출발 전제를 *수치로* 뒷받침. 단 차폐 SE 6.7 V·할라이드 4 V는 Son 계산=우리 hull 밖, 우리 재현 아님) |
| **bare NCM-LPSCl 분해산물 = phosphate + P₂Sₓ + Li₂S** (우리 산화 staircase·interface_reactivity) | = post-mortem XPS(P 2p phosphate·P₂Sₓ, S 2p Li₂S) bare NCM cycling 후 | **[Cha]** ⭐ (우리 그룹 실험이 우리 분해화학 간접 검증; **단 LZC dual-compat=Zr⁴⁺ passivation은 Zr 우리 hull 부재로 *아직* 미정량** → 향후 Zr hull) |
| **dual-compatibility(코팅이 두 상 모두와 무분해)를 voltage별 정량** = `GrandPotentialInterfacialReactivity` 도구의 적용대상 | = LIC/LYC/LZC × {NCM, LPSCl} 6계면 호환성(LZC만 dual) | **[Cha]** ⭐ (우리 도구가 *왜 Zr⁴⁺만 견디나*를 in-silico 재현 가능 = 우리 그룹 실험을 우리 DFT가 *검증·확장*할 미래 지점; **현재는 Zr hull 없어 미실행**) |
| **Li 접촉 시 RECl₃ 불가 → 산물 = RE⁰(RE-P상)+LiCl** (nd hull V=0: NdP+LiCl+Li₂S+Li₂O+Li₃P, NdCl₃ 없음; NdCl₃+3Li→3LiCl+Nd 치환) | = **결론 원문 "the formation of La and LiCl"** + "lithium-induced reduction of La³⁺ to La⁰" — La-O 도핑 실험이 *데이터로 지지하는* 음극 화학이 우리 치환 예측과 동일 (반면 "LaCl₃-at-anode" 도식은 SI 포함 무증거 가설 → gradient SEI 외층으로만 양립) | **[Yang25]** (⚠ 우리 hull=Nd 전용, La는 화학 유추; La-hull 계산이 남은 확인 1건) |
| **P–O 결합이 O-doped argyrodite 안정성 레버** (ICOHP P–O −8.43 ≫ P–S −5.98·O@PS₄ −0.67 eV/O·AIMD P–O 자발형성) | = La-O 도핑의 대기안정 개선(H₂S↓·회복률 43.5 vs 11.9%)을 "P–O가 강하고 PS₃O는 물리흡착"으로 설명 — 단 그들 분광증거 0(O 1s/Raman 無) → **우리 계산이 그 주장의 유일한 원자단위 근거** | **[Yang25]** (가수분해 기체상 자체는 우리 hull 밖 — 결합강도·자리선호까지만) |
| **XPS SEI anchor 3점 (Li₂S 160.2 · PS₄³⁻ 161.6 · Li₂SO₄ 168.0 eV)** | = **[Qian26]** 실측 S 2p₃/₂ (수분 섹션 161.6/163.2/166.6/168 · 계면 섹션 160.2/161.1/163.1) — **3점 0.1 eV 이내 일치** + **thiosulfate 166.6 eV = 우리 테이블에 없던 중간 산화-S anchor 획득** | [Qian26] |
| **"산화 안정성 개선의 레버 = 전자 절연이지 창 확대 아님"** (우리 Nd/B₂O₃ 절연 CEI 서사) | = **[Qian26] 저자 자인**: "electronically insulating DA layer **limits electron transfer**" → *practical* oxidative stability. 열역학 onset은 안 건드림 = **B①/B③ 축분리의 외부 실험 증거** | [Qian26] |

## H. ⚠️ 우리가 아직 못 하는 것 (정직 목록 → 향후)
| gap | 누가 필요로 함 | 보강책 |
|---|---|---|
| **⭐⭐⭐ 양극 CEI 의 *운동학* — 우리는 0 K hull 평형만이다. "얼마나 빨리 · 얼마나 두껍게 · 연속적인지" 를 못 말한다** (2026-09-22 신설) | **[Ncube26]** 이 **그 칸을 통째로 채우는 형태**로 존재한다: MLMD(nat>6000·3 ns·300 K) 로 LCO\|LGPS 상호확산을 **직접 보고**, 거기서 뽑은 D 를 **1D phase-field** 에 먹여 `두께 = 0.265·t^0.155`(t=초, μm) → **24 h 에 >1 μm**, 그 두께를 **2D 셀 모델**의 전하전달저항·활물질 손실로 환산해 **첫 방전 용량 126→75 mAh/g**(figure-read)까지 잇는다. **이음매에 흐르는 것이 확산계수 하나뿐**이라는 설계(`Fig. 1`)가 우리가 베낄 수 있는 형태다 | ⛔ **그들의 D·두께 수치는 이식 금지**(§Reference key [Ncube26] 비판 ①②③ — MSD 가 확산영역이 아니고 `Table 2` 와 재현도 안 된다). **가져오는 것은 *구조* 뿐**: ① **MLMD → D → 상장 → 셀** 4단 사다리 ② 상변수 판정(>0.95/<0.05) ③ 되먹임 고리(부피팽창 → 압축응력 → D↓ → 성장 감쇠, 지수 <0.5 = damped). **우리 쪽 최소 실행 = 새 MD 0회**: 기존 UMA 궤적에 **z-분해 원소 밀도 열지도 · RDF 시간추적 · 층별 잔존 PS₄ 수**를 붙이면 그들이 3 ns 6000원자에서 뽑은 것(**MSD 하나**)보다 이미 많다 — §H 의 **T3 프로토콜(Li‖SE)이 같은 형태로 이미 설계돼 있으니 양극 쪽에 재사용**. ⚠ **정책 충돌을 먼저 푼다**: 연속체는 **절대 D** 를 요구하는데 우리 인용정책(2026-09-18)은 **상대차만**이다 ⇒ 무차원화(`D/D_bulk` 만 넘기고 D_bulk 는 실험 σ 로 고정)를 **계산 전에** 결정할 것 |
| **⭐⭐ 계면 *기계* 축 자체 — CEI 문서군에 delamination·stiffness 가 단 한 건도 없다** (2026-09-22 신설, 전수 grep 확인) | **[Ncube26]** 의 **결론 문장 자체**가 이 축이다: 화학적 상호확산을 **100 % 막은** LNTO 중간층조차 용량의 10 % 를 못 찾고(`figure-read` 126→113 mAh/g), 그 잔차를 설명하려면 **30 % 계면 박리**를 넣어야 한다. 이유는 LNTO 가 LGPS 보다 훨씬 **단단**해서 방전 중 계면 인장응력이 커지기 때문. **🆕 SI 로 눈금이 생겼다** — `Fig. S10e` 최대 인장응력 4점: **LE ≈8 · LGPS ≈50 · LLZO ≈500 · LNTO/LGPS ≈400 MPa**, 그림이 직접 **"No delamination"**(앞 둘) / **"delamination possible"**(뒤 둘)로 라벨. 그 판정을 만든 입력이 `Table S2` 의 **E(LGPS) 20 GPa [= Deng16]** vs E(LCO) 200 GPa | 🔴 **우리 §2b 보호율에 직접 걸린다** — 보호율 `min(1, k·x/(1−x))` 는 **화학적 소모 경로만** 센다. ⇒ **즉시 조치(계산 0회)**: 원고에 **범위 선언** 한 줄 — *"본 지표는 P-매개 TM 소모 경로에 한정되며 계면 기계·수송 손실은 포함하지 않는다."* ⇒ **선택 조치가 이제 정량 질문이 됐다**: 눈금이 **E ≈20–30 GPa = 안전 칸 / ≳10² GPa = 박리 칸** 이므로, Nd-인산염 3상(NdPO₄/LiNd(PO₃)₄/NdP₅O₁₄)의 **C_ij** 를 기존 elastic 파이프라인으로 내면 **우리 CEI 산물이 어느 칸인지 처음 말할 수 있다**(⛔ 지금은 값이 없으므로 주장 금지). ⚠ **선결** — 보고량이 *"연속 코팅층의 박리"* 인지 *"나노분산 2차상의 응력 집중"* 인지 먼저 선언(후자면 C_ij 만으로 부족) + **분류 탄성량을 E 로 고정**(우리 E_VRH 와 B₀ 는 comp1→modelc 에서 방향이 반대다). ⚠ [Ncube26] 의 W_ad 절대값(25.0/11.7 J/m², 우리 환산)은 **우리 rigid-분리 과대 밴드와 같은 종류**라 대조군으로 못 쓴다 — **비 2.14× 만**. ⭐ **그리고 그들이 안 이은 다리가 우리 §H "W_ad → σ_adh" 항목 그 자체다** — 그들은 W_ad 를 계산해 놓고 박리 판정엔 안 썼고 4점을 **눈으로** 갈랐다(문턱이 도출이 아니라 선언). 그 다리를 우리가 이으면 **≈50 / ≈400 MPa 이 맞대볼 상대편 숫자**가 된다 |
| **⭐⭐ 계면 관측량의 *면내(in-plane) 분산* — 우리 3×3×1 슬랩은 면내 표본이 1개라 원리적으로 못 잰다** (2026-09-22 신설) | **[Xu26XLS]** `Fig. 6d` 의 **xy 투영 맵**이 그 양을 실물로 보여준다: **같은 계면거리 x 에서도 y 방향으로 뚜렷한 얼룩·줄무늬**(Li\|LGPS\|Li 11,325,600 원자, 면내 44 × 57 nm). 저자 자신이 *"the calculation additionally resolves **in-plane heterogeneity** that is difficult to access experimentally"* 라 명시 | ⛔ **우리가 지금 못 한다 — 얼버무리지 않는다.** 우리 계면값은 **면내 단일표본**이고 오차막대가 면내 분산을 담고 있지 않다. ⚠ 보강책이 "큰 셀"은 **아니다**(그건 20,480 노드 얘기다). 현실적 경로는 **UMA-MD 로 면내 큰 셀을 돌려 국소 지표의 면내 분산만 재고, DFT 는 대표 자리 몇 곳만** 찍는 2단 구조다. **아직 계획 없음 — 공백으로 등재만 한다** |
| **⭐ 전자전도도 σ_e — 우리는 band gap 만 있고 σ_e 가 없다** | **[Deng26PS]** `Fig. 3b` 가 **산화 억제의 *본체* 를 σ_e 로 지목**한다(5.69×10⁻⁹ → 7.84×10⁻¹⁰ S cm⁻¹, 7.3×↓). [Taklu21] 도 σ_e 1.49×10⁻⁹ S cm⁻¹ 를 dendrite 억제 근거로 든다 | ⚠ **우리 +B₂O₃ gap 1.9671 eV 는 host 2.066 보다 *낮다*** — gap≠σ_e 이지만 **좁아지는 방향은 σ_e 상승 위험**. ⇒ **결함준위·캐리어 축**(도펀트 유래 gap 내 준위, 유효질량, 정공 국재화)을 열어야 "+B₂O₃ 가 산화안정에 유리" 를 방어할 수 있다. 최소 실행: 도핑계 **PDOS + 결함준위 위치** 확인 |
| **⭐ H₂O 흡착·가수분해 축 (표면)** | **[Deng26PS]** `Fig. 3f`(E_ads −0.972 / −0.199 eV) · **[Qian26]** `Table S2`(표면E 0.40–0.72 J m⁻²) · **[Zhu20]**(벌크 가수분해 ΔG 177종) | **우리는 이 축이 0 이다.** 그리고 **두 선행 논문 모두 슬랩/흡착부에 vdW 가 없다** ⇒ **PBE-D3 + 주기 폴리머·비정질 표면 + 자리/피복률 샘플링 + [Adeli] 중성자 점유율 decorate** 로 하면 그 자체가 기여. 우리에겐 이미 **UMA melt-quench 비정질 표면 파이프라인**(`adhesion.json` γ_SE comp1 1.211 J m⁻²)이 있다 |
| **⭐ 계면 부착일 W_ad — cascade 스크리닝의 빈 축** | **[Deng26PS]** 는 W_ad 도 표면E 도 계산하지 않는다. 대신 **계면 저항 관측 사다리**를 준다(R_CEI 6.1→22.9 Ω · **1사이클째부터 R_Diffusion 21.7 vs 7.7 Ω** = 출발선 자체가 다름) | W_ad 의 **계산 대조군은 [Qian26] γ_SE 표**이고, **[Deng26PS] 는 "계면이 나빠지면 셀에서 이렇게 보인다"는 관측 앵커**로만 쓴다. ⛔ 두 논문의 역할을 섞지 말 것 |
| **⭐ Arrhenius prefactor σ₀ (= ν₀·ΔS_m·α₀²) — 우리는 Ea·D 만 본다** | **[Famprikis19]** Eq.(2) `σ₀ = z(nq²/k_B)e^{ΔS_m/k_B}α₀²ν₀` + **"연질 골격의 양날"**(Ea↓ 대신 ν₀·ΔS_m↓); **[Kraft]**(ν₀ ↔ Debye 실측); **[Ren26]** ⟨ω⟩ | **위 490행(포논/VDOS 축)과 같은 작업으로 동시에 채워진다** — VACF→VDOS→⟨ω⟩·Debye 를 comp1 vs modelc 로 내면 "Cl-rich 의 Ea 이득이 σ₀ 손실로 얼마나 상쇄되는가" 가 처음으로 답해진다. ⚠ 현재 우리 서사("Cl-rich = Ea↓ = 빠름")는 **prefactor 를 암묵적으로 불변 가정** 하고 있다 — 원고에 이 가정을 명시하거나 계산으로 제거할 것 |
| **⭐ W_ad → σ_adh(박리 압력) 환산 — 기계량을 계면저항이라는 *측정량*에 연결하는 다리** | **[Famprikis19]** §Mechanics (**ref 107 = Wang & Sakamoto**: σ_adh ↔ Li/LLZO 계면저항 **직접 상관 실증**); DEM 축(JKR/DMT pull-off) | 우리 `adhesion.json` 은 **에너지(J/m²)** 만 갖고 **응력(MPa)** 이 없다. 환산에는 접촉모델(JKR: σ_pull-off = 3πΔγ/2R 등)과 **입자 반경 R** 이 필요 ⇒ **DEM 쪽에서 R 을 주고 DFT 쪽에서 Δγ 를 주는 자연스러운 접점**. ⚠ 선결: 우리 rigid-분리 W_ad 의 dangling-bond 과대(`adhesion_calibration_decision_2026_05_17.md`, 실험 0.2–0.4 vs 우리 45–225 J/m²) 보정 — v2 melt-quench W_ad 1.107 J/m² 계열을 쓸 것 |
| **폴리음이온 내부 결합강성 ICOHP (P–S / P–O / B–S) — 우리는 Li–X 만** | **[Famprikis19]** *"stability against reduction has been experimentally correlated with **bond stiffness of polyanion units**"*(ref 31 Muy); **[Fan26]** B–S −2.15 | LOBSTER 재실행 시 **P–S·P–O·B–S 페어를 출력에 추가**하면 끝(구조·SCF 재사용). 이걸 해야 우리 O-도핑/B₂O₃ 서사가 **리뷰가 지지하는 서술자**와 같은 축에 놓인다. ⚠ 현재 "ICOHP(Li–Cl) −1.86/−2.10" 로 환원 안정성을 말하면 **리뷰의 문장과 다른 결합을 인용**하는 것 |
| **입자 스케일 이산역학(DEM)이 산출하는 접촉면적·기공률 ↔ 우리 DFT 물성의 연결** | **[Famprikis19]** `Fig. 2` — **`Contact area` 를 서술자로 그려 놓고 그것을 계산하는 방법 바가 사다리에 없다**(MD 는 nm 에서 끝, 위는 곧장 continuum); **ASR = t/σ 기여는 "복합체 단위부피당 접촉면적"에만 의존**(ref 68 = [Bielefeld19]) | ⭐ **이것은 gap 이라기보다 우리 repo(DEM-DFT)의 존재 이유** — digest §6.2 에 **DEM 입력 매핑표**를 만들어 뒀다(k_n←E_VRH, k_t←G_VRH, JKR Δγ←W_ad, σ_y(Li)=0.8 MPa[ref144], 파쇄←**K_Ic 공백**, 혼합제약 **φ_SE 25–50 %**[ref68]). **아직 없는 입력 3가지 = SE 입자 σ_y · K_Ic · 마찰계수 µ** → 조달 문헌 **ref 75(Froboese/Kwade, 미세구조↔σ 실측)·ref 137(Shen/Hatzell, 기공 연결성 토모그래피)·ref 144(Masias, Li 탄소성·크리프)** 전부 litdb 미보유 |
| 기체상(SO₂/O₂) 포함 계면 분해 | [Zuo] R_int 메커니즘 | 기체 chempot + NCM O-release |
| **가수분해(수분) 축 — B④ moisture ΔG_hyd 계산 0** | **[Zhu20]**(레시피 원전 + **정답지**), [Yang25] H₂S 실측, [Taklu]/[Li25] HSAB 주장, [Fan26] 공기축 | **⭐ 2026-08-05 격상 — 절차 + 정답지 둘 다 확보**: [Zhu20] SI가 Step 1–4를 명세하고, **SI xlsx 269 화합물 전표를 전사**했다(`db/properties/zhu2020_si_hydrolysis_energies.csv` 99행 + `zhu2020_si_redox_reactions.csv` 170행 — **문헌 소환값**). 레시피: MP hull(+50 meV) + NIST-JANAF 기체(H₂O/H₂S/HCl) 실험 μ + 수산화물 19종 실험 ΔH + 부분압 `Δμ=k_BT ln x`(0.1 %=RH ~3 % / 1 ppm) + pseudo-binary S–O 프로파일 → 최저 ΔG 대표반응(hydroxide는 pseudo-oxide 삽입). **검산 앵커 순서**: A1 `½Li₂S+H₂O→½H₂S+LiOH` **+0.225** → A2 `LiCl+H₂O→HCl+LiOH` **+0.977**(⚠ xlsx 1.335는 HCl 보정 누락) → A3 `2LiOH→Li₂O+H₂O` **+0.413** → A4 `¼Li₃PS₄+H₂O→H₂S+¼Li₃PO₄` **−0.608**(xlsx −0.594) → A5 **Li₇PS₆ −0.682**(argyrodite 모체) → A6 Li₃PS₄ **ESW 1.708–2.369 V**. A1–A3 통과가 선결. 그 뒤 comp1/modelc/**LPSOCl/+B₂O₃/Nd**. 예상: O-doped ΔG 덜 음수(구동력 선지불)·산물에 Li₃PO₄. ⚠ **B가 급소** — B₂S₃ −0.901·Li₃BS₃ −0.893·BCl₃ −0.120(환산 −0.834) = **S계·Cl계 양쪽 최악**, 방어선은 'B가 B–O로 남는가'. ⚠ **`air_hsab` 정성 tier 승급 시**: 이름부터 재정의(`air_dGhyd`) — Zhu 데이터가 **HSAB로 설명 안 되는 산화수 반전**(Sb³⁺ +0.535 vs Sb⁵⁺ −0.167)을 보인다; 대상도 범주 불일치(우리는 도판트 **산화물** 47종, Zhu는 **황화물/염화물**); **Mg·Co·Ni는 Zhu 표에 없음**; 큐레이션/소환값 칸은 게이트 승격 금지(`screening_roadmap` §8). ⚠ **우리는 아직 0건** — '우리가 가수분해를 계산했다' 금지 |
| **⭐ 격자동역학(포논) 축 자체 — 우리는 정적 탄성(C_ij)·EOS(B₀)뿐, VDOS/Debye/⟨ω⟩ 0건** | **[Kraft]**(음속 v_long 1480→1130 ms⁻¹·Debye ν_D 2.45→1.90×10¹² Hz를 *실험*으로 잰 뒤 **Meyer–Neldel 상쇄**로 "soft≠always better" 확립) · **[Torii]**(sound velocity·Debye **미보고 n/a**로 남긴 칸) · **[Ren26]**(⛔프리프린트, **원소분해 VDOS + ⟨ω⟩ 정의**를 실제로 쓴 예) | **⟨ω⟩ = ∫ω·g(ω)dω / ∫g(ω)dω (VDOS 1차 모멘트)** 를 채택 — **DFPT 없이 UMA-MD 궤적의 속도자기상관(VACF)→FFT 후처리만으로 나온다**(궤적은 `tools/ionic/`에 이미 있음). comp1/modelc/+Nd/+B₂O₃/LPSOCl **원소분해 ⟨ω⟩** 를 내면 (a) elastic 축(E_VRH 22.06→27.66)과 (b) σ 축(Ea 0.253→0.224)을 **하나의 물리량으로 연결**하고, **[Kraft]의 실험 Debye ν_D의 계산 대응물**이 된다. ⚠ 도입 시 **UMA 포논 영역 검증(QE-DFPT 스팟체크 1건) 필수**(UMA는 LPSCl MD에만 검증됨). ⚠ **[Ren26]의 "연화=σ↑" 단조 서사는 [Kraft]가 우리 물질에서 실험으로 반증한 형태** — 우리는 *상쇄(prefactor)* 까지 함께 봐야 한다 |
| **⭐⭐ 열수송 축 자체 — 우리 db 에 열확산도/열전도도 칸이 아예 없다** | **[Ling26]** 이 축을 SE 설계변수로 세운다: LPSC 필름 α **0.174(면내)/0.189(축) mm² s⁻¹**, FG 10 wt% 로 면내만 **0.901 (5.2×)**, 축은 0.167 로 불변; FG 단독 α ~2.5 & σ_e 2.4e-8 S/cm; 무기 SE 전부 α<0.81; GO/rGO 는 σ_e>1e-5 로 단락 위험. LPSC k = α·ρ·C_p ≈ **0.22 W m⁻¹K⁻¹**(우리 환산) | **보강책**: `db/properties/thermal.json` 신설(문헌 소환값 전용, 우리 계산값과 분리) + 장기적으로 phonon/Green-Kubo 축(현재 우리는 VDOS 자체가 0건 — 위 격자동역학 gap 과 같은 뿌리). ⚠ **[Ling26] 의 COMSOL 절대값은 쓰지 말 것** — 그들 자신의 j·σ·α 로 역산하면 중심 승온이 1.60 °C 인데 그림은 8.3 °C (5.2배 과대, digest §4.4) |
| **셀 레벨 열/안전 계측(ARC·DSC-MS·관통/가열 남용) — 우리는 전혀 없다** | **[Ling26]** ARC 100 % SOC 파우치 **T₁ 161.3→171.2 / T₂ 174.6→196.0 °C**(단 **T₃ 509.4≈509.2 = 총 발열 불변 → *지연*이지 *완화*가 아님**); DSC-MS 로 O₂ 방출이 **~200 °C** 에 나오는 것(=Ni90 격자산소)이 방아쇠임을 특정 | **보강책**: 우리 축은 **계산 쪽 대응물**(NCM O-release chempot + 기체상 포함 계면 분해, 위 '기체상(SO₂/O₂)' gap 과 같은 항목)으로만 접근 가능. **T₁/T₂/T₃ 라는 언어는 우리 원고에 도입 가능** |
| **축분해 MSD (a/b/c) — 우리는 등방 총합만** | **[Kim2025]**(방향분해 MSD가 핵심 관측량, 1D vs 2D 판정) · **[Ren26]**(Fig 3a–3c·**Fig S7–S17 11조성×4온도 전수**; pristine LZC = **1D(c축)** → 도핑 시 **2D(Er)/준-3D(Nd)** 승급 = *우리 해석*) | 코드 몇 줄. **modelc(rhombo-62)·슬랩·GB 등 이방성 셀에서 즉시 정보**. 🔑 두 할라이드 논문이 공통으로 준 교훈 = **"1D 망은 p_c=1이라 blocker 하나로 절단, 3D 망은 점진 감쇠"** → 우리 `dopant_blocking_fraction`·Nd σ-drop(0.52×, Ea 불변)이 *자릿수 절단이 아닌 이유*의 물리 |
| 무질서 E_above_hull (metastability) | [Zuo] DSC/TGA, [Wu], **[Liu]**(LiCl/thio-LISICON annealing window) | SQS/enumerate E_hull (Cl-rich 2차상 = modelc Cl1.6 위험) |
| 음극 환원 분해 *동역학*(속도) — 우리는 grand-potential 산물(thermo)만 | **[Liu]** AIMD 계면 P–S RDF 시간추적(PS₄ 10 ps vs 35 ps) | **이미 [Liu]가 외부 AIMD로 제공** → 우리 thermo onset에 kinetic 짝. 향후 우리도 Li//argyrodite AIMD RDF 가능(셋업 동급: VASP/PBE/NVT/Γ) |
| **⭐ Li 금속‖SE 계면 반응 MD 자체 — SEI 두께·상·성장 시간 (완전 공백, `open_items` T3)** | **[KimSEI]** ⛔프리프린트 (Li‖LPSCl 20/50 ns·~7,000원자·Li₂S 결정화 11 ns·11 nm interphase) · [Liu] AIMD(50 ps, 개시만) · `papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md`(SevenNet 7net-0 **사전학습 그대로** 500 ps 양극측 계면 MD = 우리 UMA 무-finetune 전략의 선례) | **T3 프로토콜 3줄 확보** — ①Li(100)‖LPSCl(100) 직접접촉, ~3 nm² 횡단면 × (Li 6 nm‖LPSCl 10 nm) ~7,000원자, NVT 350 K, **≥20 ns**(핵생성이 11 ns라 200 ps로는 아무것도 안 보임) ②1차 관측량 = **잔존 PS₄ 층수 vs 시간**(z-bin + P–S 거리컷; D 아님 — **층 간격 ≈0.5 nm=a/2 로 nm 환산 가능**), 2차 = **z–t 원소 밀도 열지도**; **구획 마스크는 "계면 ±d"가 아니라 LPSC 쪽 0–5 nm 를 독립 bin 으로** 잡을 것 ← 결정 핵생성이 **계면에서 LPSC 쪽 ~3 nm 안쪽**에서 시작하므로(2026-08-04 z 역산) 계면 중심 마스크로는 핵생성을 놓친다. **초기 접촉 간격·평형화 프로토콜을 명시**할 것 ← [KimSEI]는 *"two well-aligned crystalline phases in direct contact"* 라고만 쓰고 이완 절차가 한 줄도 없어 "즉시 시작되는 분해"가 초기 배치 의존일 수 있다 ③우리 규율 = **시드 ≥3**(그들 1)·핵생성 개시 시각 산포를 결과로·**D 절대값은 목표에서 제외, 비율만**·착수 전 게이트로 **1 ns UMA MD → 20 ps 스냅샷 → QE single-point 대조**(=[KimSEI] Fig S3 재현) 통과 필수 ← **UMA는 Li 금속‖황화물 반응 영역에서 검증된 적 없음**(Li₃N 편향 전례) |
| **MLIP 외삽 관리(스냅샷이 훈련영역 밖인지) — 우리 UMA는 판정 장치 자체가 없음 (`open_items` T1)** | **[KimSEI]** γ_select=2 / γ_break **10→5→2**(단계적 조임, 최종 γ_break=γ_select) · **[KimMTP]** γ_select=5 / γ_break=20 | **수치 확보 완료 — 단 γ는 MTP 전용**(선형 moment-tensor 기저 위의 maxvol/D-optimality 정의; UMA는 비선형 등변 GNN이라 정의 자체가 없다) → **숫자 이식 금지, 논리 구조만 이식**. ⚠ **출처 주의(2026-08-04)**: [KimSEI] §2.4 의 γ 도입 문단에는 **인용이 0건**이다(형식론은 Supplementary Note 1 지시). γ 정의를 우리 문서에 쓸 때는 [KimSEI]가 아니라 **원전 [32] Shapeev, Multiscale Model. Simul. 14 (2016) 1153 · [39] Gubaev, Comput. Mater. Sci. 156 (2019) 148** 을 직접 인용할 것: ①불확실성 대리지표를 하나 정한다 ②**선별 문턱과 중단 문턱을 분리**한다 ③중단 문턱을 조여 가며 **"프로덕션 궤적 전체가 문턱 안"** 을 수렴 판정으로 쓴다. 우리 대리지표 후보 = UMA↔QE 힘 오차(표본 스냅샷)·에너지보존/온도 드리프트 이상치·다중 모델 앙상블 불일치 |
| **비정질 상의 전자구조 — `sei_products.json`은 결정상 gap만 사용** | **[KimSEI]** (Li₃P·LiCl이 결정화하지 않고 비정질/고립 클러스터로만 존재) | 우리 절연 판정(insulator ≥4 / marginal 2–4 / **conductor <2 eV**)이 **결정 Li₃P 0.70 eV**에 기대고 있는데, 실제 SEI 안의 Li₃P는 비정질일 수 있다 → **비정질 Li₃P(및 Li₂S) gap 스팟체크**가 우리 SEI 전자절연 서사의 가정 검증 |
| **시트/펠릿 microstructure σ(공동·percolation) — 우리는 bulk 단결정 AIMD만** | **[KimICCF]** (device σ ≠ bulk σ) | **GeoDict digital-twin**(GrainGeo+ConductoDict, contact 0.07 + biphasic 0.08 Ω·cm²) = bulk↔device σ 다리 |
| 음극 in-situ SEI *실측* 산물·전자절연성 | **[KimICCF]** XPS LiF/Li₂S | 우리 grand-potential 환원산물 예측의 실험 카운터파트(이미 [KimICCF]가 제공) |
| ~~LiS4 제외 ESW~~ ✅ **완료 (2026-06-23)** | [GG] phase set | onset 2.256 V, comp1 rxn=Zuo Eq1 정확 일치 (`our_dft_baseline.md` §ESW 상세) |
| 구속 ESW 절대값(full Lagrange) | [GG] K_eff=20 정량 | constrained_esw 2nd-order |
| defect/σ_e 정량 | slide25 틀 | Freysoldt defect calc |
| slab IP / absolute VBM | UPS 절대 기준 | slab+vacuum |
| **γ_SE(표면에너지) 외부 검증 — 우리 `adhesion.json` γ_SE는 UMA melt-quench 비정질 표면, 외부 대조군 0이었음** | **[Qian26]** ⭐ **부분 해소** — VASP PBE 520 eV·pymatgen 슬랩으로 **LPSCl 저지수 표면E 6종 공개**(Table S2): **(010) Li₅SCl 0.40 J/m²(최저)** · 010-Li 0.44 · 011-Li₄S₂ 0.48 · 010-S 0.70 · 010-Li₇SCl 0.72 | 우리 γ_SE **comp1 1.211 / comp2 1.189 / comp3 0.565 / comp4 0.450 / comp5 0.470 J/m²** — **Li-결손(Cl-rich) 조성이 그들 0.40–0.5 밴드에 안착**(comp1만 3× 높음), 그들도 **Li 과잉 종단(Li₇SCl 0.72) > Li 결손(Li₅SCl 0.40)** = 우리 "공공이 표면E를 낮춘다"와 **같은 부호**. **보강책**: `adhesion_v5`(crystalline slab MQA, in_progress)에 **(010) Li₅SCl 종단 명시 포함** → 우리 비정질 표면이 결정질 최저면보다 비싼 게 물리인지 방법 artifact인지 판정. ⚠ 방법 3중 상이(PBE-DFT 결정질 vs UMA 비정질·종단 정의·비화학량론 μ 처리 유무) → **"검증됨" 금지, 같은 자릿수·같은 방향까지만** |
| **Zr 포함 hull (할라이드 코팅 LIC/LYC/LZC dual-compatibility 정량)** | **[Cha]** ⭐ (LZC=Li₂ZrCl₆ vs NCM/LPSCl 6계면) | Zr 추가 chemsys(Cl-Li-Zr-…)로 `GrandPotentialInterfacialReactivity` voltage-resolved — 왜 Zr⁴⁺만 견디고 In/Y는 분해하나 in-silico 재현 |
| **양극(NCM/LCO) 반응성 게이트 — cascade에 ΔE_rxt(vs 양극) 열 없음** (만충/반충 SOC-resolved 포함) | **[Xiao19]** Filter 4(&#124;ΔE_rxt&#124;<0.1 eV/atom vs LPS+만충 NCM)·Table S2/S3, **[Rich16]** eq 2/4, [Cha] dual-compat | pymatgen InterfaceReactions로 cascade CSV에 **ΔE_rxt(vs LCO) 열 추가**(우리 hull 내 즉시 가능; 정답지=Xiao LPSCl/LCO **−339/−493 meV/atom** 재현) → 이후 Ni/Co/Mn chemsys 확장으로 NCM·만충/반충까지 — 도핑이 양극 반응성을 개선/악화하는지 cascade 축으로 편입 |
| **⭐ D 의 확산영역 게이트가 없다** (β 폐기 후 공백) | **[Maginn19MD]** §5.2.2 — **log-log MSD 기울기 ≈ 1** 과 **√MSD > L/2** 를 확산영역 판정의 조건으로 요구. **🆕 2026-09-22 [Ncube26] SI 반영 — *대조 규약*이 들어왔다.** ⛔ **초판 정정**: 이 칸은 처음에 *"[Ncube26] 은 게이트 없이 간 반면교사"* 라고 적었는데 **틀렸다.** 그들 SI 는 `MSD ∝ t^β` 의 **β ≈ 1** 판정을 하고 **표본간격 1 ps·10 ps** 로 평가해 **적합창을 ~0.4–1.9 ns 로 잘랐다**. ⇒ **형식은 우리 게이트와 같다.** **남는 것은 더 센 형태다**: ① β 정의식이 **기울기가 아니라 비 `log(MSD)/log(Δt)` 로 인쇄**돼 어떤 단위계에서도 1 이 안 나온다 ② **게이트를 통과했다는 결과가 `Table 2` 와 안 맞고, 불일치가 종 선택적**이다(*우리 산수*, 그들 창 안에서: Li 4× · P 2× · O 6× · S 20× vs **Ge ≈330× · Co ≈560×**) — **정지한 골격종만 터지는 것 = 보정 안 된 COM 드리프트의 지문** ③ 뿌리는 **평형 미달**(`Fig. 5` PE·압력 단조 드리프트), 그리고 **같은 논문 `Fig. S5a`(LNTO)가 "수렴한 PE" 를 보여줘 내부 대조로 판정된다** | **비용 0.** 기존 `tools/ionic/msd_diffusive_check.py` 에 `slope_2_50ps` 한 열 추가(새 파일 금지). 이게 없으면 "2–50 ps 가 확산영역이다" 라는 **전제 자체가 미검증**이고, 그 위의 Ea·D_rel 은 전부 그 전제에 얹혀 있다. **🆕 [Ncube26] SI 가 주는 것 3개**: ⓐ **창 비교 대상** — 그들 적합창 **400–1900 ps** vs 우리 **2–50 ps**. **우리 창 상한이 그들 창이 시작도 안 한 시각이다.** 계·물질·온도가 달라 우열은 아니지만, *"확산영역 시작 시각은 계마다 자릿수로 다르다"* 는 외부 실측 근거 ⇒ **우리 창 검증의 시급도를 올린다** ⓑ **표본간격을 2개(1·10 ps)로 잡아 비교**하는 관행 — 비용 0, 그대로 이식 ⓒ ⭐ **역검산 조항 신설**: 게이트 통과가 최종 표를 보증하지 않는다. **보고하는 D 를 원자료 MSD 로 되돌려 확인**하는 단계를 규약에 넣는다(그들은 이걸 안 해서 600× 를 놓쳤다). **그리고 게이트를 MSD 에만 걸지 말 것** — MD 보고에 **PE·압력 드리프트 동봉**(정상상태가 아니면 기울기 검사만으로 못 잡는다) |
| **⭐ MSD 창 선택이 만드는 D_rel 변동폭을 보고하지 않는다** | **[Maginn19MD]** §4.2.2·§5.2.3 — *"critical to quantify the degree of variability … that arises from assumptions in the data analysis, e.g., the time interval over which the Einstein slope is computed"* | 우리는 **절대 Ea 의 창 효과 242 meV** 를 안다(원장). **그런데 보고량인 `D_rel` 의 창 민감도는 잰 적이 없다** — 242 meV 는 D_rel 에 그대로 옮겨오지 않는다(비에서 상쇄될 수 있다). ⇒ **시간구간 부트스트랩(§6.3.1 이식)으로 `D_rel` 의 창 CI 를 내는 것이 최우선**. 새 MD 0회 |
| **⭐ D 의 유한크기 의존을 한 번도 안 봤다** | **[Maginn19MD]** §5.1.2 — D 의 크기 효과는 **"significant … must be accounted for"**, CO₂ 에서 ≈10 %(figure-read 로는 최소 셀이 D∞ 를 **≈15 % 과소**) | ⛔ **YH 식 이식 금지**(η 요구 + 유체역학 backflow 전제 → 고체 골격계에 전제 불성립). ⭕ 논문의 **첫 번째 방법**은 그대로 유효: 600 K 에서 host·design 을 **2×2×2 / 3×3×3** 두 크기로. 목표는 D∞ 가 아니라 **`D_rel` 이 크기에 둔감함을 보이는 것** — 그것만 보이면 우리 보고량이 방어된다 |

---

## I. 🔎 출처 재귀속 — *우리가 써 온 숫자를 원문에서 되짚은 결과*

> 이 축은 **물성 비교가 아니라 인용 감사**다. 우리 생산식·baseline 에 주석으로 달려 있던
> 출처를 PDF 실물로 되짚었더니 **숫자와 논문이 어긋난** 사례를 모은다.
> `/benchmarks` 의 **덱 정정 원장**(외부 자료가 틀린 경우)·**판정 이력**(우리 판정이 틀린 경우)과
> 같은 계열이고, 여기는 **"출처 라벨이 틀린 경우"** 다.
> ⚠ 셋 다 공통 규율 — **값을 지우지 않고 라벨을 고친다.** 값 자체가 합리적일 수 있고,
> 그때 문제는 "틀린 값"이 아니라 **"근거가 없는 값"** 이다.

| 우리가 쓰던 것 | 붙어 있던 출처 | 원문 실물 | 판정 | 조치 |
|---|---|---|---|---|
| `Li₂S 이동장벽 = 0.22 eV` · `LiF = 0.67 eV` (우리 `sei_neb` 논의에서 **문헌 앵커 후보**로 오르내리던 쌍) | **[Liu24SbO]** 본문 p.8 → ref **[30b]** (제목 없는 AFM 양식) | ✅ **원출처는 실재하고 서지도 정확하다** — **[Lai20]** *Nano Lett.* **2020, 20(11), 8273−8281**(저자 14명·순서·교신 3인까지 일치, DOI 10.1021/acs.nanolett.0c03395). 그리고 **Lai 는 진짜로 CI-NEB 를 했다** — SI 에 계산 방법 절이 실재하고(`CI-NEB`·Henkelman 2000·힘 0.05 eV/Å), `Fig. 3e/3f` 에 MEP 곡선 실물(각 7점 + 구조 인셋), `Fig. S11` 이 그 값을 **"Present work"** 로 표기한다. **⇒ 인용 사슬은 3단이 아니라 2단에서 끝난다.** ⛔ **그러나 그 0.22 는 벌크 Li₂S 가 아니라 "Li₂S ***layer***" 관통 장벽**이고, **Lai 자신이 `Fig. S11` 에서 벌크 Li₂S(figure-read Cal. ≈0.45 eV)를 별개 막대로 그려 구분했다** | ⚠ **라벨 오류 — 값이 틀린 게 아니라 *대상*이 틀렸다.** "문헌 Li₂S 장벽" 이 아니라 **"Lai 의 나노 Li₂S *층 관통* 장벽"** 이다. (§I 의 앞선 건들은 *그 논문이 그 양을 재지 않은* 형태였는데, 이번 건은 **쟀지만 우리가 생각한 양이 아닌** 형태다 — 새 유형) | ① 인용 시 **"through a thin Li₂S **layer**"** 를 반드시 유지 ② 우리 `v2/li2s` 0.305 eV 의 문헌 짝을 **[Lai20] → Moradabadi & Kaghazchi *APL* 2016, 108, 213906** 으로 **교체** ③ 다섯 축 판정은 `papers/lai2020_li2s_interfacial_layer_amorphous_sulfide_cse.md` §11 에 고정 ④ [Liu24SbO] §6.4 에 역링크 추가 완료 |
| `σ_grain = 3.0 mS/cm` ("Cronau 2022 Li₆PS₅Cl **single-crystal**") | **[Cronau]** | ⛔ 그 숫자가 **논문에 없다.** 단결정을 **측정한 적이 없고**("single crystal" 단어 자체가 논문에 없음), 측정한 argyrodite 는 **Li₆PS₅Br**(Cl 아님). 연도도 2021(2022 아님, DOI 1c01299 동일) | **오귀속 — 라벨만 부정확, 값은 방어 가능** | 라벨을 *"LPSCl grain-interior 프로젝트 채택값 — 근거: Cronau **2021** µC-Li₆PS₅**Br** 고압 plateau 2.0–2.4 mS/cm + cold-press/소결 LPSCl 문헌 1–6 종합. ⚠ 단결정 직접측정 아님"* 으로. `lpscl_electrolyte_params.md` 의 "single-crystal digit NOT verified (proxy)" 플래그는 이로써 **닫힌다** |
| `Cronau(r_SE)` sub-µm 3-시그모이드 (breakpoint 0.5/0.3/0.1/0.03 µm, plateau 1.0/0.90/0.65/0.33) | **[Cronau]** | ⚠ 논문이 다루는 축은 **결정도 클래스 × stack pressure** 이지 **반경**이 아니다. breakpoint 수치는 논문에서 **도출된 적이 없다** | **느슨한 귀속 — 방향만 지지** | 인자를 **재명명**: 방향(미세결정·sub-µm → σ↓)만 [Cronau] 근거, **수치는 프로젝트 채택값**으로 분리 표기 |
| `σ_S = 10 / σ_P = 5 mS/cm` (NCM 단결정이 다결정의 2배라는 **전자**전도 엔드포인트) | **[Trevi]** | ⛔ 이 논문은 **σ_e 를 SC/PC 로 측정한 적이 없다.** 본문·SI·표·그림 어디에도 숫자로 없다. 잰 것은 **D_Li · BET 활성표면적 · R_ct** 뿐이고 전부 **액체전해질 셀** | **오귀속 (논문은 이 질문에 무관)** | σ_AM 엔드포인트를 **material-specific INPUT 으로 전환**(LOCKED 해제). "SC vs PC 전자전도 방향"은 **이 논문 밖에서** 결정할 열린 문제로 남긴다 |
| `NCM(r) = 1/(1+(r/2 µm)^1.5)` (입자크기·내부 GB 보정) | **[Trevi]** | ✅ 방향은 지지 — 단 **기구가 다르다**: PC 는 1차 충전부터 균열 → **액체가 균열로 침투** → 활성표면적↑·R_ct↓ 로 **겉보기 D_Li 가 1자릿수 이상 뛴다**. 침투 효과를 빼면 **본질 D_Li 는 SC·PC 동일** | **부분 정당화 — 단 '전자전도'가 아니라 '확산·동역학'** | 인자의 물리를 *전자전도*가 아니라 *확산 경로 단축·유효 표면적*으로 다시 쓴다. ⚠ **ASSB 전사 주의**: 이 논문의 셀은 **액체전해질**이라 "균열→침투→표면적↑" 이 그대로 성립하지 않는다(고체는 균열에 스며들지 못한다) |

**이 축이 주는 규율 한 줄** — *숫자를 인용할 때 "누가 말했나"가 아니라 **"그 논문이 그 양을 실제로 쟀나"**,
그리고 **"쟀다면 그게 내가 생각한 그 양인가"** 를 확인한다.*

**유형이 둘로 갈렸다 (2026-09-01 [Lai20] 건으로 확장):**
- **유형 A — 안 쟀다.** [Cronau]·[Trevi] 건: 저자·연도는 맞는데 **그 논문이 그 물리량을 측정한 적이 없다.**
  서지가 맞다는 것이 값의 근거가 되지 않는다.
- **유형 B — 쟀는데 다른 양이다.** [Lai20] 건: 논문은 **진짜로 CI-NEB 를 돌렸고 값도 그 논문 것이 맞다.**
  틀린 것은 **대상**이다 — 우리는 "벌크 Li₂S 장벽" 으로 읽었고 논문이 잰 것은 "나노 Li₂S **층 관통**" 이다.
  ⚠ **유형 B 가 더 위험하다.** 유형 A 는 원문을 펴면 값이 아예 없어서 즉시 걸리지만, 유형 B 는
  **원문에 그 숫자가 그대로 인쇄돼 있어 검증을 통과한 것처럼 보인다.** 서지 확인만으로는 못 잡고,
  **다섯 축(셀·전하규약·홉정의·CI/이미지·코드/범함수)** 을 대조해야 걸린다.

---

## J. 🤖 MLIP·ML 방법론 — *우리 모델을 재는 축* (2026-08-19 신설)

> 📎 **번호 배정 2026-09-13 병합** — 2026-09-09 초안 9건이 J-11/J-12/J-13 을 서로 겹쳐 요구했다 (J-11 은 09-12 에 [Honrao21] 이 선점).
> 배정: **J-12** [Basu26MFB](초안 J-11) · **J-13** [Aqib26MFAL](초안 J-12) · **J-14** [Muy25Dop](초안 J-12) · **J-15** [Liang26IF](초안 J-12) ·
> **J-16** [Wang25DPA](초안 J-11) · **J-17** [Zhao21HECS](초안 J-13) · **J-18** UQ 축(초안 [Carrete23UQ] "J-11 신설"+[Maginn19MD] 2-d) · **J-19** GB 축(초안 [Ou26MS] 2-d).
> J-9 소절: **J-9c** [Hu26ICAL] · **J-9d** [Liu26AB] · **J-9e** [Ou26MS] · **J-9f** [Wilson22BAL] (초안 4건 전부 "J-9c").
> ⚠ 절 순서는 번호순이 아니다 (J-8 이 J-7 앞, J-11 이 J-9 앞 — 종전부터). 각 신설 절 머리의 📎 줄이 초안 출처다.

> A–I 는 **물성 값**을 문헌과 맞대는 축이다. 이 축은 다르다 — **우리 계산기 자체**를 잰다.
> 값이 아니라 **방법의 신뢰구간**을 다루므로, 여기 숫자를 물성 표로 옮기면 안 된다.
> 신설 이유: 2026-08-19 에 MLIP 방법론 논문 3편 + ML 방법론 학위논문 1편이 한꺼번에 들어왔고,
> 그중 하나가 **우리가 직접 측정할 수 있는 DFT 라벨 데이터셋**을 공개했다.

### J-0. 이 축의 출처 (약칭 → digest)

| 약칭 | slug |
|---|---|
| **[UMA]** ★ | `uma2026_family_of_universal_models_for_atoms` — **우리 엔진의 원논문** (arXiv:2506.23971 v2) |
| **[PET-MAD]** | `petmad2026_lightweight_universal_interatomic_potential_mad` |
| **[Zhang npj]** | `zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill` |
| **[Lai]** | `lai2025_haml_li_metal_lpscl_interface_doping_seFO` |
| **[Kauwe 2021]** | `kauwe2021_ml_materials_properties_dissertation_sparks` |
| **[Shapeev16]** 🔧 | `shapeev2016_moment_tensor_potentials` — **MTP 수학 원전** (Multiscale Model. Simul. 14, 1153). ⚠ **물성값 0 · 텅스텐 전용** → 아래 **J-7** 에만 등장, A–D 축 금지 |
| **[Park24]** 🔧 | `park2024_sevennet_parallel_gnn_md` — **SevenNet 원전 · GNN-IP 공간분할 병렬화** (JCTC 20, 4857). **우리 UMA 와 같은 등변 GNN 계열 = T1b 대조군**. ⚠ **물성값 0 · SiO₂/Si₃N₄ 전용** → 아래 **J-7** 에만 등장, A–D 축 금지 |
| **[Chang26Sel]** 🔧 | `chang2026_performance_based_mlip_selection_sse` — **argyrodite 에서 직접 잰 사전학습 MLIP 선정 벤치마크** (*Chem. Mater.* **38**, 3133 (2026) · Solid Power Inc.). 피고 5종 = EqV2·DPA3·ORB v2·**SevenNet**·MACE, **전부 MPtrj/PBE** · ⛔ **UMA 없음**. ⚠ **물성값 인용 불가**(σ·D 는 PBE 편향 + 400 K 외삽 + 단일시드, Ea 는 단위 오기) → 아래 **J-7** 에만, A–D 축 금지. ★ **우리 계(Li₆PS₅Cl)로 직접 잰 몇 안 되는 방법론 편** |
| **[Hu26ICAL]** 🔧 | `hu2026_foundation_model_surrogates_active_learning` — **능동학습 대리모형 벤치마크(ICAL / TabPFN)** (**arXiv:2603.12567v3**, 2026-03-24, **동료심사 전**). 🔴 **"foundation model" = TabPFN(표 데이터용 in-context 트랜스포머)이지 MLIP 이 아니다** — 원자·구조·힘·DFT **전무**. ⚠ **물성값 0**(σ·Ea·ESW·탄성·gap 전무; 이 논문의 "electrical conductivity" 는 **Cu 합금 %IACS**) → 아래 **J-9c** 와 **J-7** 에만 등장, A–D 축 금지. 모델 원전은 우리가 이미 보유 → `hollmann2025_tabpfn_tabular_foundation_model` |
| **[Kurn26UQ]** 🔧 | `kurniawan2025_comparative_ensemble_uq_nnip` — **MLIP 앙상블 UQ 벤치마크** (*MLST* 2026, in press, DOI 10.1088/2632-2153/ae9fb4). ⚠ **물성값 0 · 탄소 동소체 전용** → 아래 **J-7** 에만 등장, A–D 축 금지. ⚠ slug 의 `2025` 는 오기 — **인용은 2026** |
| **[Tompa26FT]** 🔧 | `tompa2026_finetuning_mlip_foundation_strategies` — **MLIP 파운데이션 fine-tuning 전략 벤치마크** (**arXiv:2606.12704v1**, 2026-06-10, **동료심사 전**). Tompa/Varga-Umbrich/**Batatia**/Elena/Bernstein/**Csányi** = **MACE 그룹 본인**, 구현이 `mace ≥3.15` 에 머지됨. ⚠ **물성값 0**(σ·Ea·ESW·탄성·gap 전무) → 아래 **J-7** 에만 등장, A–D 축 금지. ★ **벤치마크 5계 중 #1 이 Li₆PS₅Cl** — 우리 계로 직접 잰 수치가 있는 드문 방법론 편 |
| **[Zaby26σ]** 🔧 | `zaby2026_reliable_conductivity_estimates_md` — **MD 로 σ 를 낼 때의 통계 원전** (*ChemPhysChem* 2026, 27:e70477, DOI 10.1002/cphc.70477, OA). ⚠ **계가 이온액체·에테르 액체전해질 · 황화물 0회 · 물성값 0** → 아래 **J-7** 에만 등장, A–D 축 금지. ⚠ **NE 오차의 부호가 [Adeli19] 와 반대** — §J-7 의 부호 경고를 반드시 같이 인용 |
| **[Aqib26MFAL]** | `papers/aqib2026_multifidelity_active_learning_alloy_design.md` — **다중충실도 능동학습(MTGP-ICM + 비용가중 EI/KG/LCB)** (M. Aqib/K. Ravikiran/L. Li/**V. Prasad**, Univ. of Alberta, ***Mater. Des.* 263, 115520 (2026)**, CC BY-NC). 계 = **Fe-Ni-Co-Cr-V-Cu 합금 717 조성**(Rao 2022 *Science* 데이터 재사용), 목표 = **CTE 최소화 단일 스칼라**. ⚠ **자체 DFT·MD·실험 0회 — 순수 알고리즘 벤치마크.** ⛔ **황화물 아님·물성값 0개 ⇒ 물성 4축(A–D)에 수치로 넣지 않는다.** 쓰는 곳은 **§J-12 하나**. ★ **공개 코드(`github.com/aqibm08/MFAL_HEA`)로 논문 서술을 검증한 유일한 편이고, 9건이 안 맞았다** |
| **[Basu26MFB]** | `basu2026_multifidelity_bandit_dopant_screening_funnel` — **다중충실도 밴딧 + 3단 DFT 검증 깔때기** (**arXiv:2604.10157v1**, 2026, 단독저자·미심사). 계 = **산화물 반도체 5종(ZnO·TiO₂·SrTiO₃·SnO₂·MgO) 격자 치환 도핑**, 목표물성 = **밴드갭 2.0 eV**. ⛔ **황화물 아님 — 물성 4축(A–D)에 수치로 넣지 않는다.** 쓰는 곳은 **§J-11(파이프라인 구조·다중충실도) 하나**. 자체 DFT **583계산 1차 근거**(J-10 `[Jain26Rev]` 의 2차 인용과 층위가 다르다) |
| **[Imbalzano21]** 🔧 | `imbalzano2021_committee_uq_md_thermodynamic_averages` — **committee UQ → 열역학 평균 전파 원전** (EPFL COSMO, ⚠ **PDF 에 저널·DOI 없음**). ⚠ **물성값 0 · 물/펩타이드/페놀/Ga 전용** → 아래 **J-7** 에만 등장, A–D 축 금지. 🔴 **동역학량(D·수송) 0회 — 우리 D 인용 금지** |
| **[Wu26MLIF]** 🔧 | `wu2026_ml_driven_electrolyte_interface_design_review` — **ML×(전해질+계면) 리뷰** (Wu/Wang 외, 샤먼대, ***Adv. Funct. Mater.* 2026, 0:e78357**, DOI `10.1002/adfm.78357`; 34 pp · Fig 16 · Table 5 · refs 148 · SI 없음). ⚠ **자체 계산 0 · 자체 실험 0 — 전량 2차 인용** → 아래 **J-20** 에만 등장, **A–D 물성축 금지**. 🔴 이 편의 값은 수치가 아니라 **우리 hull 방법에 대한 두 개의 비판**과 **§4.6 계면 설계규칙 번역표**다 |

### J-0b. ★★ [UMA] 우리 계산기의 사양서 — 원논문 대조 (2026-08-25 신설)

> J-1 이하가 **"우리 엔진을 외부 논문으로 재는"** 축이라면, 이 소절은 **엔진 자신이 뭐라고 적혀 있는가**다.
> ⚠ **확증편향 주의**: 이건 우리가 이미 쓰고 있는 도구의 자기 소개서다. 유리한 줄만 뽑지 않기 위해
> **"논문이 안 한 것"을 먼저 적는다.**

**⛔ 논문이 검증하지 않는 것 (전문 34쪽 문자열 전수 검색)**

| 우리가 이 엔진으로 재는 것 | 논문의 검증 | 근거 |
|---|---|---|
| **확산계수 D** | ⛔ **없음** | `diffus*` **0회** |
| **이온전도도 σ** | ⛔ **없음** | `ionic` **0회** · `conductiv` 3회는 **전부 thermal** |
| MSD·아레니우스·Green–Kubo·NE | ⛔ 없음 | — |
| 온도 상한 / 골격 융해 | ⛔ 없음 | thermostat·앙상블 논의 자체가 없음 |
| **장벽(NEB/전이상태)** | ⛔ **없음** | — |
| 황화물·할로겐화물 계 | ⛔ **없음** | `lithium`·`sulfide`·`halide` **각 0회** |
| **MD 관련 유일한 검증** | ✅ **NVE 에너지 보존 ✓/✗ 한 칸** (수치 없음) | `Table 4`·`Table 16` |

**⇒ 판정**: **우리 규율 *"σ 절대값 인용 금지 · 비율도 멀티시드 판정만"* 은 보수적인 게 아니라
논문 근거의 공백을 정확히 메우는 것이다.** MD 프로토콜(Langevin NVT · dt 2 fs · friction 0.02 ·
5 ps + 200 ps · MSD 창 2–50 ps · 600/800/1000 K)은 **전부 우리 규약이고 논문 무보증**이다.

**✅ 논문이 실제로 보증하는 것 — 그리고 우리 값과의 위치**

| 항목 | [UMA] 보고 | 우리 | 판정 |
|---|---|---|---|
| 엔진 정체 | **UMA-S-1.1 = UMA-S 와 동일 아키텍처** (`Table 1` 각주) · 150 M 총 / **6 M 활성** · 32 experts · 4 블록 · L_max 2 · 6 Å 컷오프 | 동일 체크포인트 | ✅ 본문 표를 우리 모델에 대응시킬 근거 확보 |
| **참조 DFT (`omat`)** | **VASP / PAW / PBE** (OMat24 설정) ⚠ MP 와 의사퍼텐셜 버전이 달라 벤치마크용엔 **MPtrj+sAlex 추가 파인튜닝** | 우리 DFT = **QE / USPP / PBE** (60/480 Ry) | **범함수 같음, 구현 다름** ⇒ 총에너지 직접 비교 금지 |
| 재료 힘 MAE | **62.8 meV/Å** (WBM) · 83.7 (HEA) · 57.1 (OMat24 val) | **30.0 meV/Å** (Li₃PS₄ 243구조, **PBEsol 라벨**) | ⚠ **빼지 말 것** — 모집단·라벨 범함수가 다르다 (아래 상세) |
| 재료 E MAE | 20.2 meV/atom (저자 "실용 목표" 10–20) | 13.5 meV/atom (참조보정 후, R² 0.620) | 같은 자릿수 |
| **탄성** | **G_vrh MAE 9.47 · K_vrh 5.16 GPa** | E_VRH 22.06↔27.66 · B₀ 26.23↔21.71 GPa (**DFT**) | ⛔ **UMA 로 탄성 조성차 주장 금지** — 오차가 우리 신호와 같은 자릿수 |
| 에너지 보존 | NVE ✓ (S·M) / ✗ (**L**) | 유한차분 프로브 0.198 % @ δ=0.005, δ 의존성 확인 | ✅ **독립 이중 확인** |
| 속도 스케일링 | 100→1,000원자에서 **원자당 3.6배** 저렴 (`Table 3`) | 52→416원자 **4.5배** (kgy 실측) | ✅ 같은 현상 ⇒ **셀 확대 처방 지지** |
| 밴드갭·DOS | ⛔ 출력 자체가 없음 | PBE fixed-occ nscf 정본 | 섞일 여지 없음 |

**⚠ 힘 MAE 30.0 vs 62.8 을 나란히 쓸 때의 3줄 면책** (원고 투입 시 필수)
1. **라벨 범함수가 다르다** — 우리 벤치는 **PBEsol**(PET-MAD 배포), 논문은 **PBE**(OMat24).
2. **모집단이 다르다** — WBM 은 무기결정 전수, 우리는 **한 조성(Li₃PS₄) 3상**뿐. 좁은 분포에서 작게 나오는 건 당연.
3. **최악값 축이 다르다** — 우리 최악 힘 0.477 eV/Å(평균의 16배), 논문은 최악값 미보고.
⇒ 방어 가능한 문장: *"UMA-s-1p1 의 힘 오차는 논문이 재료 전반에서 보고한 50–85 meV/Å 대와 같은
자릿수이고, 우리가 직접 잰 황화물 부분집합에서는 그 범위 안쪽(30 meV/Å)이다."*

**★★ 부록 G — 우리가 쓰는 바로 그 버전의 병리 (Li₃N 금지 조항의 외부 근거)**

원문(Appendix G): *"Previous versions of UMA (**1 and 1.1**) struggled with this task and showed
**unphysical behavior** at times. In particular, **the OMat task produced large energy fluctuations
beyond the bonding region**."*

- `Fig. 7` 실측(figure-read): `omat` diatomic 곡선이 결합영역 밖에서 **+50 ~ +165 eV** 짜리 혹을 만든다
  (Fe–O ≈ +163 @ 3.5 Å → +78 @ 4.3 Å → +140 @ 5.0 Å · Mg–Mg ≈ +155 @ 4.8 Å · O–O ≈ +138 @ 4 Å).
- 1.2 에서 해소(`Fig. 8` = diatomic 데이터 **없이도** 매끈 ⇒ 원인은 데이터가 아니라 **학습 절차**).
  **`Table 26` 에 1.1 행이 없어 우리 버전의 diatomic 오차는 수치로 존재하지 않는다.**
- ⚠ **과잉 해석 금지**: diatomic 은 **진공 속 원자 2개** = OMat24(주기 벌크)의 극단 OOD.
  **"UMA 가 벌크 LPSCl MD 에서 100 eV 를 튀긴다"는 뜻이 아니다.** 지목하는 위험 영역은
  **저배위·진공·해리 방향** — 슬랩+adatom, 계면 초기배치, NEB 양 끝 이미지.

**⇒ ⛔ Li₃N 금지(2026-06)와의 관계 — 정직하게**
- **논문에 직접 예고는 없다.** Li₃N·질화물·특정 화학계 경고 **0건**, §6 한계는 두 문단뿐.
- **그러나 간접 근거 두 겹**: ① 부록 G 가 **우리 버전·우리 task** 를 지목 ② §6 장거리 한계
  (*"흡착질이 7 Å 에서 출발하면 상호작용하지 않는 독립 구조 2개로 본다"*). **우리 Li₃N 은 슬랩+adatom
  (진공 15 Å)** 이었다 = 두 경고가 겹치는 자리.
- ⇒ **금지 판정 자체는 여전히 우리 실측에만 근거한다. 다만 붙일 인용문이 생겼다**:
  *"저자 스스로 UMA 1.1 의 `omat` task 가 결합영역 밖에서 비물리적임을 보고했다
  (arXiv:2506.23971v2, Appendix G, Fig. 7)."*

**⇒ 다음 실험 (DFT 0회 · ~10분 · 비대칭적으로 싸다)**
`omat` task 로 **Li–N · Li–P · Li–S · Li–Cl · Li–O · P–S** diatomic 스캔(0.7–6 Å).
Li–N 이 `Fig. 7` 같은 혹을 내면 **금지 기전 확정**, Li–S/Li–Cl 이 매끈하면 **LPSCl 사용 근거 추가**.
(Zhang npj 도 "Li–Li diatomic turning point" 를 신뢰성 3종 세트에 넣었다 — 도구 계보가 같다.)

**⚠⚠ b2o3 −6.63 eV 사례 — 기록 정정**
*"UMA 선호를 DFT 가 뒤집었다"* 로 회자돼 왔으나, `kb/methodology/b2o3_doping_chemistry.md`
§6d–§6e 원문은 **반대**다: UMA(9,880 전수 relax, base 4종 전부) = **BS₄ + O→P**,
DFT(QE PBE 64원자) = 같은 결론을 **ΔE −6.63 eV** 로 확정. 문서 표현 그대로 **"UMA + HSAB + DFT 3중 일치"**.
**뒤집힌 것은 UMA 가 아니라 (a) HSAB 휴리스틱 §6c 와 (b) 원논문 `Fig. 1b` 의 "BO unit" 가정**이다.
⇒ ① 이 사례는 **UMA 의 반증이 아니라 자리선호 축의 긍정 사례**다.
② 다만 **에너지 해상도 규율은 그대로**: `Table 2` 의 20 meV/atom 은 64원자에서 **1.3 eV** 규모이고,
b2o3 top motif 간 차이는 **~2 meV/atom** 이었다 — **UMA 로 못 가른다.**
③ 그리고 이 건은 **벌크 주기계 내부 치환**이라 부록 G·§6 어느 경고에도 안 걸린다
⇒ **"분포 밖 외삽 때문에 위험했다" 는 서사는 성립하지 않는다.** 위험했던 건 **해상도**였다.

**★ 외부 감사와 짝지어 읽기** — 같은 날 들어온 `kalikadien2026_uma_tm_catalyst_conformer_ranking`
(*J. Phys. Chem. A* 2026, 130, 1897)는 **같은 UMA-S-1.1** 을 `omol` task·single-point 로 감사했다:
**집계 R² 0.96–0.97 / RMSE 2.4–4.9 kJ/mol 인데 리간드별 랭킹 신뢰율은 84 %→53 %(강직→유연),
61 %(Ru)→44 %(Mn)** 로 무너지고, **실패는 ΔE ≲ 2–5 kJ/mol(≈21–52 meV) 근접축퇴 영역에 몰린다.**
⇒ 두 논문을 겹치면 **"평균 오차는 훌륭하고, 그 평균이 감추는 것은 근접 후보 간 순위"** 라는 한 문장이 된다.
우리 쪽 같은 얘기 3건: b2o3 top motif **~2 meV/atom**(§J-0b 위) · 우리 벤치 **최악 힘 = 평균의 16배**(J-1) ·
Kauwe 2021 §2.5(J-4). ⇒ **UMA 는 후보를 좁히고, 판정은 DFT** 규율의 외부 재확인.
⚠ 단 그쪽은 **`omol`·single-point·유기금속** — 힘·이완·MD·장벽 0. **우리 `omat` MD 로 직수입 금지.**

**⇒ 1.1 → 1.2 판단: 갈아타지 않는다.**
1.2 가 더 정확하고 빠른 건 맞다(WBM 힘 62.8→54.2, HEA E 24.9→17.2, 1k원자 16→24 steps/s).
그러나 **우리 db 전체(comp1·modelc·b2o3·LPSOCl·cascade 3,615행)가 1.1 위에 있고, 우리 규율이
"절대값 금지·비율만" 이라 비율의 기반 통일이 유일한 자산**이다. 게다가 1.2 는 `fairchem>2.16.0` 요구.
⇒ **처방: committee 멤버로 1.2 를 추가**한다. 1.1↔1.2 불일치가 곧 **"부록 G 병리가 우리 계에 걸리나"의
직접 측정**이고, PET-MAD 추가보다 **표적이 정확하다**(env 하나만 더).

### J-1. ★★ 우리 실측 — UMA 힘 정확도 (외부 데이터, DFT 0회)

| 지표 | 우리 UMA-s-1p1(omat) | 같은 test set 공표값 |
|---|---|---|
| **힘 MAE** | **30.0 meV/Å** (Li 13.2 · P 36.8 · S 40.9) | PET-MAD 기저 **63.9** · LoRA(N=1940) **39.2** · bespoke(N=1940) **35.6** |
| 에너지 (원소별 참조보정 후) | 13.5 meV/atom | — |
| 상대에너지 RRMSE | **2.4 %** ⚠ | (Zhang npj: MACE-MP-0 의 CI-NEB 전이상태 **22.8 %**) — ⚠ **이 두 수를 비교하지 말 것.** 우리 2.4 % 는 첫 구조 기준 ΔE 인데 test 가 16–64원자 혼합이라 **분모가 크기 차이로 부풀어** 있다(약한 지표, 코드 재독으로 확인 2026-08-20). 그들 22.8 % 는 같은 셀 안 전이상태 ΔE(~0.1–1 eV)다. 우리 쪽 정직한 수치는 RMSE 0.688 eV |
| 학습 여부 | **이 데이터 학습 안 함** | LoRA·bespoke 는 **1940구조 학습** |

- 데이터: PET-MAD 배포 `Li3PS4/` (train 1940 / test 243, 16–64원자, α/β/γ, **PBEsol** 라벨)
- 값: `db/properties/mlip_bench_li3ps4_uma.json` · 도구 `tools/mlip/bench_against_dft.py`
- 판정 카드: `kb/results/uma_force_accuracy_li3ps4_2026_08_19.md`

**⇒ 판정**: ⛔ **"UMA 가 황화물에서 PES 를 무르게 본다"(sulfide PES softening) 는 근거가 없다.**
preflight 이 알리바이로 쓰던 문구를 **철회한다.**

**⚠ 이 벤치가 닫지 못하는 것 (반드시 같이 인용)**
1. **응력을 안 잰다** (데이터셋에 stress 라벨 없음) ⇒ **cascade 부피 편향(+32.7 %) 은 별건**이다.
2. **장벽을 안 잰다** ⇒ **NEB 0.528 vs MD 0.253 (109 %) 격차의 남은 후보는 경로 선택**이다.
3. **Cl 이 없다** — 조성이 Li₃PS₄ 이고, PET-MAD MAD-bench 1562구조에도 Li+P+S 동시 구조가 0개다
   ⇒ **아르지로다이트·Cl 무질서로의 전이를 이 벤치가 보증하지 않는다.**
4. **공표값의 분할을 우리가 직접 확인하지 않았다** (배포 parity 데이터 재계산에 의존) ⇒ 원고 투입 전 확인 필수.
5. **최악 힘 0.477 eV/Å = 평균의 16배.** 꼬리를 평균으로 덮지 말 것 (J-4 참조).

### J-2. 축 A(이온전도)로 넘어가는 것 — **값이 아니라 스케일만**

| 문헌 | 값 | 우리에게 무엇인가 |
|---|---|---|
| **[PET-MAD]** Li₃PS₄ β상 Ea | 0.323(PET-MAD) / 0.356(bespoke) / 0.317(Gigli 2024) eV — ⚠ **배포 원수치로 우리가 회귀, 논문 미보고** | 조성이 달라 **값 비교 금지**. 가져오는 건 **"모델 선택 계통차 ≤0.036 eV"** 라는 스케일뿐 — **우리 시드산포 ±0.032 와 동급** ⇒ "단일시드 1.33× 철회"(SEMIFINAL 2026-07-09)의 외부 지지 |
| **[PET-MAD]** σ 추정자 | **Green–Kubo 전하 flux**(교차상관 포함), 768원자, 3–4 ns, 16 온도점 | 우리 **NE Haven=1**, 52원자, 200 ps, 3점 ⇒ **"σ 절대값 인용 금지" 규율의 외부 근거** |
| **[Zhang npj]** Li₃YCl₆ 셀크기 | 소형(1×1×2) 외삽 σ_RT ~2.0 vs 대형(3×3×6, 1620원자) ~0.3 mS/cm (실험 0.51) — **400 K 이상에선 일치** | **"절대값 금지·비율만"** 의 정량 근거. **고온 비율 비교는 방어된다** |
| **[Lai]** 벌크 Li₆PS₅Cl | Ea ≈ 0.30 eV (600–1200 K 4점, `Fig. S10` 픽셀 적합) · D(600 K) ≈ 2.0×10⁻⁶ cm²/s | ↔ 우리 comp1 **0.253 eV / 3.09×10⁻⁶**. 둘 다 MLIP 고온외삽이라 **비교 가능** — 우리가 1.6× 빠르고 Ea 0.05 낮다. ⚠ 저쪽 MSD 창·Haven 미기재, **1200 K 포함**(우리 상한 1000 K) |

⚠⚠ **[Zhang npj] 온도 상한 경고**: MACE-MP-0 이 **LGPS 골격을 1050–1500 K 에서 인위적으로 녹인다**
→ 저자가 1500 K 샘플링을 기각하고 **1050 K** 로 낮췄다. **우리 아레니우스 1000 K 앵커가 그 선 바로 아래다.**
⇒ **기존 궤적에서 비-Li 골격(P·S·Cl) MSD 평탄화를 600/800/1000 K 에서 확인해야 한다** (새 DFT 0, 미착수).

### J-3. 축 D(전자구조)·E(환원/음극)로 넘어가는 것

- **[Lai] ★★ 우리 우위 카드**: 저쪽은 SEI 산물로 **Li₃P** 를 지목하면서 *"상대적으로 안정한 SEI"* 라 쓰는데
  **전자구조 계산이 전무하다.** **우리 Li₃P 0.71 eV (fixed-occ nscf)** 가 반론이다 — **Li₃P 는 전자를 못 막는다.**
  `anode_interface_b2o3.json` 의 min-gap 판정과 **같은 결론에 동역학 증거가 붙는다.**
- **[Lai] 산물 일치**: Li₃P·Li₂S·LiCl ↔ 우리 grand-potential (LPSCl1.6 @0 V → Li₃P + LiCl + S)
  ⇒ **우리 열역학 예측이 외부 동역학으로 확인된 첫 사례** (축 G 로도 승격 후보).
- **⭐ [Lai] O 자리가 우리와 정면으로 다르다** — 저쪽 O 는 **자유음이온 자리·Li 6배위**(`Fig. S2f`),
  우리 LPSOCl 은 **PS₃O, P–O 1.559 Å**(골격 자체가 옥시설파이드).
  ⇒ **같은 이름 다른 물질. "O 도핑이 계면반응을 촉진한다"를 우리 LPSOCl 에 이식 금지.**
- **[PET-MAD] 해당 없음** — 밴드갭·DOS 를 다루지 않는다. 패키지의 **PET-MAD-DOS 는 별도 논문·PBEsol** 이라
  우리 PBE fixed-occ nscf 정본(2.066 / 2.099 / 1.9671 / 2.2309 eV)과 **섞지 않는다.**

### J-4. ML 방법론 감사 — **[Kauwe 2021] 기준선 vs 우리 cascade predictor**

| 항목 | 문헌 (§2·§6) | 우리 (cascade predictor) | 판정 |
|---|---|---|---|
| 분할 | **종 단위 그룹 분할 필수**, 같은/비슷한 데이터의 train-test 동거 금지 | 랜덤 5-fold 가 캐노니컬 (GroupKFold/LOCO 는 계산만) | ❌ **누출**. 랜덤 CV 상한 **0.986** → 새-도펀트(LOCO) **0.220**, Pugh **0.020** |
| 특징 | **CBFV** (원소 물성 avg/range/var) | 도펀트 one-hot + 상수 2개 | ❌ 외삽 근거 이전 불가 |
| 작업 형식 | 상위 1 % 탐색은 **분류**가 회귀보다 우월 (precision 0.56 vs 0.39–0.44) | 6타깃 전부 회귀 | ❌ 목적–형식 불일치 |
| 베이스라인 | 무작위(6 %) → 최근접이웃 → 모델 사다리 | `DummyRegressor` 구현은 있으나 **미보고** | ⚠ 절반 |
| 불확실도 | 시드 5개 ±σ 음영 | 단일 시드 (`random_state=42`) | ⚠ **우리 MSD 멀티시드 규율과도 불일치** |
| 학습↔적용 분포 | PCD 적용 시 0.1 % 미만만 검출 = 분포 어긋남을 **명시적으로 보고** | winner 622–681행 학습 → 3,615행+신규에 적용 | ❌ **같은 구조의 실패 위험** |
| 재현성 | 소스·데이터·가중치·하이퍼·시드·환경파일 전량 | provenance/시드/CSV ✅, held-out test·HP 기록·그림 ❌ | ⚠ 부분 |

> **J-1 의 "최악 힘 = 평균의 16배"가 이 표와 같은 얘기다** — *평균 RMSE 가 낮아도 목표 물성이 틀릴 수 있다*(§2.5).

### J-5. 도구·인프라 판정 (재료 비교 아님)

- **[PET-MAD] committee 4번째 멤버로 최적.** `tools/ionic/mlip_committee.py` 의 기존 3종 중
  **MACE-MP-0·SevenNet-0 이 둘 다 MPtrj** 라 상관돼 있고, 상관된 멤버는 불일치를 과소평가한다.
  PET-MAD 는 **데이터(MAD)·범함수(PBEsol)·아키텍처(비등변 transformer)가 전부 탈상관**이다.
  ⚠ **별도 conda env 필수** (`metatrain==2025.10` 하드핀 → gabia UMA env 오염 금지) ·
  기준선 재교정 필수(PBEsol×PBE 혼합이라 불일치 바닥이 올라간다) · **파인튜닝본 투입 금지**
  (`Table S3`: LoRA 후 MAD 기저 성능 **3–19배 악화**).
- **⭐ γ 게이트 문제 — 두 논문이 같은 구멍을 가리킨다.** HAML 의 전부는 **γ(Maxvol 외삽등급)** 로
  *"모델이 자기가 모른다고 말하면 MD 를 멈추고 DFT 로 돌아가는"* 것인데 **UMA 에는 이 신호가 없다**(단일 모델).
  그런데 PET-MAD 는 **`calculate_uncertainty=True` 한 줄로 LLPR 불확실도**를 준다
  ⇒ **PET-MAD 를 committee 에 넣는 것이 곧 γ 대용품이다.**
- **[Zhang npj] fairchem 은 UMA 파인튜닝을 공식 지원한다** —
  `create_uma_finetune_dataset.py --uma-task=omat --regression-tasks efs` → `fairchem -c …yaml`.
  **LoRA 는 fairchem 에 없고**(전체 파라미터만), `freeze_backbone` 은 head-only 라 단거리 PES 교정에 부적합.
  **stress(`efs`) 학습이 cascade 부피 편향(+32.7 %) 교정의 후보** — 모델이 **3,615회 재사용**되므로
  cascade 가 옳은 표적이고, **SEI 장벽 4개(20 d → 10–18 d, ~2×)에는 수지가 안 맞는다.**
- **[PET-MAD] 셀 크기**: `Fig. 3` 좌단에서 **30–60원자는 원자당 비용이 아니라 스텝당 오버헤드가 지배**한다
  ⇒ 우리 52원자 → 416원자(2×2×2)면 **통계 8배·벽시계 2–3배**. 400/500 K 를 버려야 했던
  단일궤적 잡음을 거의 공짜로 완화한다. **엔진 무관 처방**, 실측 1회로 판정 (미착수).
- **[Lai] HAML 비용 — 우리 계 환산** (⚠ VASP 실측 112원자 3.80 h/ps 를 N³ 로 늘린 **추정**):
  Li\|LPSCl 3,800 코어시간 · Li\|**LPSOCl** 4,900 · Li\|**b2o3** 18,000 (300 ps 기준).
  **첫 할 일은 우리 QE 로 112원자 MD 10스텝 벽시계를 재는 것** — 그 숫자 하나면 표 전체가 우리 값이 된다.
- ⛔⛔ **[Lai] UMA 사용 전 필수 관문**: 이 계면의 주 생성물 **Li₃P 는 Li₃N 과 같은 Li-rich 프닉타이드**이고
  **UMA 는 Li₃N 사용 금지 판정(2026-06)** 을 받았다.
  ⇒ **Li₃P 벌크 UMA 검증(격자·형성E·힘 RMSE vs QE) 없이는 이 계면에 UMA 를 못 쓴다.** 타협 불가, 제일 싸다.

### J-6. ⛔ 이 축에서 **인용하면 안 되는 것**

- **[Lai] 도핑 결론 전체** — 자기 SI 가 반증한다. `Fig. S14a` 에서 PS₄ 가 제일 빨리 깨지는 건
  **무도핑**(≲1 ps < F 13 < Se 18)이라 본문의 *"dopants accelerate interfacial reactions"* 와 **반대**다.
  `Fig. 5f` 무도핑 Li–S 막대는 0 ps 와 280 ps 가 **픽셀 단위로 동일**하고,
  `Fig. S15` "average CN"(Li–S 17~19)은 **Li–S 배위 상한 8** 을 넘어 물리적으로 불가능하다
  (종별 CN 을 더한 것으로 보인다).
- **[Zhang npj] RRMSE 22.8 % 를 우리 UMA 에 숫자로 이식하는 것** — 표본이 **MACE-MP-0 단일**이고
  UMA 는 시험하지 않았다. **정성 경고로만.** (실제로 J-1 은 UMA 가 그 표본보다 힘에서 **5배 정확**함을 보인다.)
- **[PET-MAD] σ·Ea 절대값** — Green–Kubo·768원자·PBEsol 이라 우리 규약과 다르다. **스케일만.**
- **[UMA] "황화물 고체전해질에서 검증됐다" · "이온전도도를 재현한다" · "UMA 로 잰 Ea 는 DFT 급"**
  — **셋 다 논문에 근거가 0 이다**(§J-0b 검색표). 커버리지 근거는 `Fig. 1` 히트맵뿐인데
  **축에 원소 라벨이 없어 Li–S/Li–Cl 쌍을 읽을 수조차 없다.** 말할 수 있는 최대치는
  *"Li·P·S·Cl 이 OMat24 89원소 안에 있다"* 까지.
- **[UMA] 공개 재료 벤치마크 수치(F1 0.913 · κ_SRME 0.204 · 탄성 MAE)를 "우리가 돌리는 그 모델의
  성능" 으로 인용하는 것** — 그 표들은 **MPtrj+sAlex 파인튜닝본** 값이고(`Table 4`·`Table 14` 캡션),
  **HuggingFace 배포 `uma-s-1p1` 이 그 가중치와 같은지 논문이 명시하지 않는다.**
- **[UMA] 부록 G 병리를 "우리 벌크 MD 가 틀렸다" 로 확대하는 것** — diatomic 은 진공 2원자,
  우리 MD 는 주기 벌크다. **지목 범위는 저배위·진공·해리 경로까지.**
- **[UMA] "저자가 경고하지 않았으니 안전하다" 는 추론** — §6 한계가 **두 문단**뿐이고
  **자기 부록의 최악 결과(부록 G)조차 §6 에 반영돼 있지 않다.** 이 논문에는 특히 위험한 추론이다.
- **[Lai] 우리 시간척도 비판을 그대로 적용하는 것** — ⭕ **Lai 는 Wu 2026 의 함정을 피했다.**
  de Klerk 앵커로 528 ps = intercage **93 사건**(Wu 의 20 ps = 3.5).
  정확한 우리 입장은 **"300 K AIMD 가 안 되는 게 아니라 20 ps 가 안 되고 300 ps 는 된다"** 다
  ⇒ **Wu(반례) + Lai(정례)** 를 나란히 놓으면 우리 시간척도 규율의 교과서 쌍이 된다.

### J-8. ★★★ CV 규약 판정 — **[Tu27ML] R²=0.99 vs 우리 cascade LODO −0.18** (2026-08-28 신설)

> **왜 이 블록이 있나**: 2026-08-25 에 우리 대리모델이 정직한 CV 에서 졌다고 판정했고
> (`db/properties/cascade_audit_ml_validation.csv`), 그때 결론이 *"−0.18 은 우리 ML 이 나쁜 게 아니라
> **우리 CV 가 정직한 것**"* 이었다. **[Tu27ML] 은 우리와 같은 영역(싼 기술자 → 비싼 DFT 라벨)에서
> 0.99 를 보고한다.** 그 0.99 가 어느 범주인지를 여기서 확정한다.
> 상세는 `papers/tu2026_diffusion_descriptor_ml_li_sse_interface.md` §7.

| 항목 | **[Tu27ML]** | 우리 cascade predictor | 판정 |
|---|---|---|---|
| **분할** | **랜덤 90/10** — 그룹 언급 0건(전수 검색 `group`·`stratif`·`leave-one` 0) | **LOOCV(쌍) / LODO(도펀트 통째) / L2DO** | 🔴 **범주 다름** |
| **CV 의 용도** | *"10-fold CV **on the training set**"* = **하이퍼파라미터 탐색 전용** | 일반화 성능 추정 | 🔴 **CV 점수를 성능으로 안 쓴다** |
| **보고 점수** | γf **0.99**(GBRT, MAE 0.12) · E_B **0.93**(RF) · 학습곡선 CV γf ≈0.98–0.99·E_B ≈0.90–0.94 (`Fig. S1` figure-read, **랜덤 폴드**) | 쌍 LOOCV **0.0892** · **LODO −0.1805** · L2DO **−0.2548** | ⛔ **병치 금지** |
| **라벨 잡음** | **≈ 0** — DFT 결정론값, ±10⁻³–10⁻⁴ (`Table 1`) ⇒ **R² 상한이 사실상 1.0** | MLIP-MD D — 시드·창 의존(modelc Ea 3-seed **0.197±0.032**) ⇒ **상한 자체가 낮다** | 🔴 **같은 척도 아님** |
| **라벨 범위 vs 결정구간** | γf 축 **−16~+10**(폭 26) / E_B 축 **0~3** vs 실제 결정구간 **0.069–0.30**(폭 0.23) ⇒ **100배** | Pareto 축은 정규화 | 🔴 **R² 범위 인플레이션** |
| **입력↔라벨 관계** | 🔴 **`Freeze γf`(36.52 %)·`Freeze E_B`(28.67 %) = 라벨의 동결판** ⇒ 사실상 **델타 러닝**인데 **동결값만의 베이스라인 미보고** | 기술자(BVSE·기하)가 라벨(MD D)과 **다른 물리량** | 🔴 **[Tu27ML] 쪽이 더 후하다** |
| **화학군 정보** | 🔴 **one-hot 6종**(#25–30). **LLZO 단독이 γf 예측의 10.63 %** ⇒ 랜덤 분할에서 **공짜 점수** | 도펀트 one-hot (같은 병) | 🔴 **양쪽 다 병 — 우리만 벌점을 매긴다** |
| **모구조 파생물 분리** | 🔴 안 함 — 174 = 6×29 라 같은 SSE 의 29 파생물이 train/test 로 갈린다 | LODO 가 정확히 이걸 막는다 (낙차 **0.089 → −0.181 = 0.27**) | 🔴 |
| **prospective 검증** | ⭕ **있다** — `Table 2` **n=4**, ML→DFT 재계산. γf Δ 0.003–0.140 / **E_B Δ 0.009–0.035 eV** | ⛔ **0/270 미실행** | ⭕ **[Tu27ML] 이 낫다** (표본은 얇아도 **고리를 닫았다**) |
| **음성 사례** | ⛔ 21 중 4 만 검증, 실패 0건 보고 | — | ⚠ |
| **enrichment / p-값** | ⛔ **계산 불가** — 분모 *"over 876 datasets"* 가 분해되지 않는다(174=6×29 는 떨어지는데 876/6=146) | ✅ **1.22, p=0.426**(유의하지 않음) + ordering 3.35, p=0.0099(retrospective) | ⭕ **우리가 낫다** |
| **축 공선성 보고** | 🔴 *"low multicollinearity"* 라 쓰는데 `Fig. 3` 에 **\|r\|=1.00 쌍이 둘**: (#6 Freeze Adhesion, #9 Adsorption) · (#22 Li Numbers, #25 LLZO). 제거 후 개수 미기재 | ✅ 유효 4축 **\|ρ\| ≤ 0.32**, \|ρ\|>0.85 없음 (`axis_corr_csv.py --pareto`) | ⭕ **우리가 낫다** |
| **빈 축 / 정보 0 축** | 🔴 `Freeze W_ad` = **`\|E_ads\|/(2A)` 의 상수배**(우리 검산, 소수 4자리) ⇒ 정보 0 비트인데 신규 3종에 포함 | 🔴 `sigma_300K_S_cm_NE`·`wad_J_m2_mean` **0 % 채움**(2026-08-28 발견) | 🔴 **양쪽 다 병** |
| **절제(ablation)** | γf 만 `Fig. S1i`–`l`, **수치 0** · **E_B(제목의 기술자)는 절제 자체가 없다** | ⛔ 축 절제 미실행 | ⚠ **양쪽 다 부족** |
| **학습곡선** | ⭕ `Fig. S1a`–`h` (n=20→140) | ⛔ 낸 적 없음 | ⭕ **[Tu27ML] 이 낫다** |
| **Dummy 베이스라인** | ⛔ 없음 | ⛔ 구현만 있고 미보고 | ⚠ **양쪽 다 없다** |
| **시드 반복·오차막대(ML)** | ⛔ 없음 | ⛔ 단일 시드 `random_state=42` | ⚠ **양쪽 다 없다** |
| **중요도 방법** | 🔴 **ridge regressor** — 예측은 트리 앙상블인데 중요도는 선형. SHAP/permutation 없음. 공선성 있으면 계수가 임의로 갈린다 | — | 🔴 |
| **데이터·코드 공개** | ⛔ 전무 (학습셋 174 중 8행만 공개) | ✅ CSV + provenance + sha256 | ⭕ **우리가 낫다** |

> ### 🔑 판정
> **[Tu27ML] 의 0.99 는 우리가 2026-08-25 에 "범주가 다르다"고 판정한 세미나 0.99 와 같은 범주다.**
> 5가지 인플레이션 요인(랜덤 폴드 · 잡음 0 라벨 · 범위 100배 · 라벨의 싼 버전이 입력 · one-hot 화학군)이
> **모두** 걸린다. ⛔ **우리 LODO −0.1805 와 같은 표·같은 슬라이드에 놓지 않는다.**
> 정확한 문장: **"자를 다르게 댄 값이다. 우리가 더 가혹한 자를 골랐다."**
>
> ⚖ **그러나 [Tu27ML] 이 우리를 앞서는 것이 셋 있다** — 되먹임 고리를 실제로 닫았고(n=4),
> 학습곡선을 냈고, 절제를 시도는 했다. **우리는 셋 다 0 이다.** 비판만 옮기면 그대로 되돌아온다.

**이식 항목 (계산 0회, 전부 기존 CSV 재분석)**

| # | 항목 | 근거 |
|---|---|---|
| **T3-a** | 🔑 **"싼 기술자만 썼을 때의 R²" 베이스라인 보고.** 우리도 BVSE 기술자 → MD D 라벨 구조인데 **BVSE 만으로의 R² 를 낸 적이 없다.** [Tu27ML] 의 최대 공백을 우리가 먼저 메운다 | §7.2-④·§6.1 |
| **T3-b** | Dummy/최근접이웃 **베이스라인 사다리** 보고 ([Kauwe 2021] J-4 가 이미 지적, [Tu27ML] 도 안 함) | J-4 + J-8 |
| **T3-c** | **도펀트 one-hot → 원소물성(CBFV) 교체 실험.** [Tu27ML] 에서 원소 기술자 6종이 E_B 예측의 22 % 를 차지한다(전기음성도 12.15 · 반지름 5.09 · 녹는점 4.97 %). one-hot 은 새 도펀트에 원리적으로 0 벡터라 LODO 에서 불리하다 | §6.9·§6.7 |
| **T3-d** | **축 절제 실험** — 유효 4축을 하나씩 빼고 Pareto front 변화 측정 | §7.3-3 |
| **T3-e** | **학습곡선**(n vs CV score) 보고 | §7.3-2 |
| **T-새** | **일함수를 계면 캠페인 기술자로.** [Tu27ML] E_B 예측 2위(18.91 %)이고 슬랩 SCF 후처리라 **추가 계산 0** | §6.4 |

**⛔ 이 축에서 인용하면 안 되는 것 (J-6 에 추가)**

- ⛔ **[Tu27ML] 의 R² 0.99 / 0.93 을 네 조건 없이 인용하는 것** — ① 랜덤 90/10 ② 라벨 잡음 ≈0
  ③ 라벨 범위 폭 26(γf)·3(E_B) ④ 입력에 라벨의 동결판. 넷을 다 붙여야 문장이 참이 된다.
- ⛔ **[Tu27ML] 0.99 를 우리 LODO −0.18 과 나란히 놓는 것** — 다른 자다.
- ⛔ **[Tu27ML] 의 "동결 기술자가 정확도에 필수임이 절제로 확인됐다"** — γf 만·수치 없음,
  **E_B 는 절제 자체가 없다**. `Fig. S1j`(GBRT 절제)는 `Fig. 4b`(전체)와 **육안 차이가 거의 없다**.
- ⛔ **[Tu27ML] 의 "21개 신규 후보"** — 3종(Ta-LLZO·Sn-LPS·Sn-LPSCl)이 학습셋 자신이다(`Table S4`
  값이 `Table 1` 과 반올림까지 동일). **18종**으로 고쳐 쓴다.
- ⛔ **[Tu27ML] 의 D·Ea·σ 절대값 전부** — `Table S6`(Ea,D₀)가 `Table 3` 과 **8계 중 6계에서 정확히
  10배 불일치**하고, Ea 0.02–0.03 eV 가 **자기 NEB 0.069–0.30 eV 의 1/5–1/10** 이며,
  `Fig. 6e` MSD 가 **8계×3온도 전부 원점부터 완전 직선**(케이지 고원 없음)이고,
  **500 K 는 Li 융점 453.7 K 위**다. `Table S7` σ 는 식·캐리어밀도가 없어 재현 불가이고
  **σ 순위가 D 순위와 다르다**.
- ⛔ **[Tu27ML] 의 `Table S3` 문헌 MAE 비교** — 단위·타깃이 다른 값(0.12 / 2.72 / 16.23 / 91.98)을
  한 열에 세워 놓았다.

**★★ 회전 자유도 — 문헌 공백 확정 (T16 근거 보강)**

**[Tu27ML] 의 기술자 30종에 다원자 음이온의 회전·재배향·libration 이 없다.**
확인: `Fig. 3` 범례 30항목 전수 대조 + 본문·SI 전문에서 `rotation`/`reorient`/`libration`/`paddle`/
`correlation function` 검색 **0건**. 기하 기술자는 `Cell Volume`·`Model Density` **둘뿐**이고,
자유부피·퍼콜레이션·병목반지름·BVSE·무질서 배열 통계도 **전부 없다**.
⇒ **우리 T16**(`kb/methodology/ps4_libration_dopant_2026_08_28.md`: PS₄ 는 500–1000 K 에서 재배향
**0/71**, 전부 원뿔 안 흔들림 · **+O 가 원뿔을 −0.5° 좁힌다**)이 **문헌 공백 기여**임을
**[Shin26] 에 이어 두 번째로 확인**했다.
⚠ 정직하게: **[Tu27ML] 은 계면, 우리 T16 은 벌크**다. *"같은 문제에서 우리가 낫다"* 가 아니라
*"인접 문제에서 이 논문에 없는 축을 우리가 갖고 있다"* 가 정확한 표현이다.

**우리 이동도 기술자와의 정면 비교 (요청 항목)**

| 항목 | 우리 | **[Tu27ML]** | 판정 |
|---|---|---|---|
| 기술자 | `migration_volume_fraction`(20³ 격자 BVS ∈[0.8,1.2] 비율) · `bvs_li_proxy_score`(`std×(1−\|mean−1\|)`) | `Freeze Barrier`(동결 CI-NEB) · `Work Function` · `SSE Band Gap` | — |
| **비용** | **DFT 0회 · 초 단위** (완화 구조 xyz 하나면 끝) | **DFT 5–7회**(NEB 이미지) / 1회 / SSE당 1회 | ⭕ **우리가 3–4자릿수 싸다** |
| 물리 충실도 | 정전기 근사 — 공유결합성·분극·격자완화 못 봄 | **실제 안장점 높이** | ⭕ **[Tu27ML] 이 위** |
| 대상 | **벌크 통로 기하 + 자리에너지 균일도** | **계면 관통 장벽** | 🔵 **다른 대상 — 겹치지 않는다** |
| 독립성 | \|ρ\| ≤ 0.32 (4축) | `Freeze Barrier` 최대 \|r\| = **0.39** (30개 중 가장 독립적) | ⭕ **양쪽 다 양호** |
| 퍼콜레이션 개념 | ✅ 있다 | ⛔ 없다 (기하 기술자 2개뿐) | ⭕ **우리가 낫다** |
| 계면 축 | ⛔ 없다 (전부 벌크) | ✅ 있다 | ⭕ **[Tu27ML] 이 낫다** |

⇒ **상충 관계이지 우열이 아니다.** 싸고 거친 것(우리) vs 비싸고 정확한 것([Tu27ML]),
벌크(우리) vs 계면([Tu27ML]). **스크리닝 앞단은 우리 쪽, 최종 몇 개 가리기는 그쪽 방식이 맞다.**

### J-7. 🔧 방법 원전 — *물성값이 없어서 표에 못 넣는 편* (2026-08-26 신설)

> ⛔ **이 블록의 논문들은 A–D 물성 4축 표에 넣지 않는다.**
>
> ⚠ **2026-09-13 기준 재진술.** 절 이름은 *"물성값이 없어서"* 인데 **그게 더는 기준이 아니다** —
> `[Wang26IF]` 는 처음부터 값이 있었고(그래서 예외 문구가 붙어 있었다), 2026-09-13 에 들어온
> `[Yu26Pol]`·`[Makino26Rev]`·`[Li26NaRev]`·`[Wang26LRM]` **넷 다 값이 많다.** 이름을 믿고 *"여긴 값 없는 편만"*
> 이라고 읽으면 틀린다.
>
> **실제 기준은 하나다 — *우리 물성 4축과 수치로 섞지 않는다*.** 그 이유는 두 가지다:
> (i) **값이 0건**이라 행을 만들면 전부 `n/a` 가 된다 (원래 사유) ·
> (ii) **값은 있는데 계·캐리어·정의가 달라** 같은 표에 놓는 순간 복사될 때 단서가 안 따라간다
> (`[Yu26Pol]` 고분자 · `[Li26NaRev]` Na 계 · `[Makino26Rev]` 리뷰 재인용 · **`[Wang26LRM]` 양극계**). §K(수계 Zn)와 같은 사유다.
>
> 여기 있는 것은 **우리가 쓰는 방법의 정의 원본** 이거나 **방법 반면교사**다.
> ⛔ 절 이름은 안 바꿨다 — 앵커(`J-7`)를 가리키는 곳이 여럿이라 이름을 바꾸면 그 참조가 끊긴다.

**[Wang26IF] `wang2026_interface_stability_kinetics_sulfide_assb` — 계면 슬랩 모델 제작 규약**
(⚠ 이 논문 자체는 ESW·Ea 값이 있어 **축 A·B·E 에 이미 행이 있다.** 여기는 *방법* 부분만 따로 둔 것)

| 항목 | [Wang26IF] §SI-1 (`Fig. S1` 7단계) | 우리 (`run_cathode_interface.py` v6 분리법) | 판정 |
|---|---|---|---|
| 격자 정합 | **a·b 를 SE 값(10.26 Å)에 고정, c 만 `V/(a×b)` 로 결정 후 DFT 로 c 만 완화** | rigid stack (양쪽 격자 그대로 겹침) | ⭕ **이식 후보 (T2)** — 부정합을 c 한 방향으로만 흡수 |
| 비정질상 준비 | **1500 K 15 ps 융해 → 0.5 K/fs 급랭 → DFT 완화** (dt 2 fs, NVT-Nosé) | UMA 3000 K melt-quench | △ 온도·속도가 다르다 |
| 슬랩 이완 | 진공 15 Å → **800 K 12 ps → 600 K 12 ps → 300 K 6 ps → 0 K DFT** (3단 어닐) | 500 K anneal + LBFGS (1단) | ⭕ **이식 후보 (T2)** — dangling-bond artifact 완화 방향 |
| **W_ad 산출** | ⛔ **하지 않는다.** 계면 12개를 만들어 DFT 완화까지 해 놓고 `E_int − E_A − E_B` 를 **면적으로 나누지 않았다** | Stage 11: `W_ad=(E_sep−E_int)/A` → **45–225 J/m²** (실험 0.2–0.4 대비 100–1000× 과대, **2026-08-28 축 보류**) | 🔴 **앵커 없음 확정** — 본문+SI 전수 검색에서 `adhesion`·`surface energy`·`interface energy`·`J/m`·`separation`·`cleav` **전부 0건**. ⇒ **이 논문으로 `wad_J_m2_mean` 을 되살릴 수 없다.** 유일한 외부 DFT 앵커는 여전히 **[Qian26] γ_SE 0.40–0.72 J/m²** 뿐이고, 실험 앵커는 **Sundar 2025 W_ad 0.2–0.4 J/m²** 뿐이다 |
| 표면 종단 | LPSCl **(001) 두 종단만** (Li-rich `slab-1` / S-rich `slab-2`) — **선택 근거 없음**, 다른 저지수 면 미시도 | [Qian26] 은 **저지수 6종**을 계산(0.40–0.72 J/m²) | ⚠ [Wang26IF] 는 **열역학 종단 비교가 아니라 동역학 종단 비교**(Ea 0.23 vs 0.28 eV)다 — [Qian26] 의 표면E 종단 비교와 **다른 축이니 섞지 말 것** |
| 구역별 MSD | **z 방향 2/3 Å(표면)·5/6 Å(계면) 구역 + "80 ps 중 50 ps 이상 잔류" 필터** | **셀 전체 평균만** (구역 분해 없음) | ⭕ **이식 후보 (T1)** — 우리 창 2–50 ps 는 유지하고 구역 분해만 추가 |

**[Shapeev16] `shapeev2016_moment_tensor_potentials` — MTP 의 수학 원전**
(*Multiscale Model. Simul.* **14**(3), 1153–1173, 2016 · 단독저자 · **텅스텐 W 단일 원소만** · 물성값 0)

| 항목 | [Shapeev16] (MTP) | 우리 (UMA-s-1p1, omat) | 판정 |
|---|---|---|---|
| 파라미터 선형성 | `V(u) = Σ_{α∈A} c_α B̃_α(u)` — **계수에 완전 선형** | **비선형 등변 GNN** | 🔴 구조적 차이 |
| 설계행렬 `X` | `Xc = g` 로 명시 존재 (에너지+힘 과결정계) | **없다** | 🔴 **maxvol/D-optimality 가 정의될 무대 자체가 없다** |
| 정확도 손잡이 | 기저 수 `#A` → **(#A)^−0.227** 대수수렴 (`Fig. 5`) | **없음** (사전학습 고정) | 🔴 우리는 정확도를 **살 수 없다** ⇒ T1 필수 |
| 과적합 진단 | **16-fold CV**, fit↔CV 간격 (MTP₁ Δ20 % / MTP₂ Δ1.4 %) | 단일 시드, held-out 없음 | ⚠ **[Kauwe 2021] J-4 와 같은 구멍** (두 번째 독립 선례) |
| 오차 보고 | 힘 RMSE **+ 데이터 힘 RMS(1.505 eV/Å) 로 정규화한 %** | 절대 eV/Å 만 (J-1) | ✅ **계산 0회로 이식 가능** |
| 화학종 | **단일 원소 가정**. 다성분은 §6 결론의 식 한 줄 | Li·P·S·Cl·O·B·Nd | 🔴 정리들이 우리 계를 안 덮는다 |
| 장거리 정전기 | **없음**. 저자가 *"Coulomb 이 있는 하전·분극계는 (2.2) 밖"* 명시 | UMA 도 단거리 (명시적 Ewald 없음) | ⚠ **같은 가정을 공유** — MTP 만의 흠이 아니다 |
| R_cut | **4.9 Å** (일반론 5–10 Å) | UMA 기본 | ⚠ 이온성 황화물엔 짧다. Lee 랩 argyrodite MTP 는 **6 Å** |

**🔴 이 축에서 제일 중요한 한 줄 — γ 원전 정정 (2026-08-26)**

- **Shapeev 2016 에 γ(extrapolation grade)는 없다.** 전문 21 pp 전수검색:
  `active learn` 0 · `maxvol` 0 · `D-optimal`/`optimality` 0 · `extrapolat` 0 · `grade` 0 · `uncertain` 0.
- ⚠⚠ **함정**: 이 논문에도 `γ` 기호가 나오는데 **ℓ₂ 정칙화 파라미터**다
  (`Table 5.1`: MTP₁ **3·10⁻⁹**, MTP₂ **0**). 덱 슬 16 의 `γ_select 2 / γ_break 10↔5↔2` 와 **무관**.
- 이 논문이 정본인 것은 **γ 의 전제**까지다 — 선형 기저(`M_{μ,ν}` → `B_α`) + 설계행렬 `X`.
  **γ 자체의 원전은 후속 논문**(**Podryabinkin & Shapeev 2017**, Comput. Mater. Sci. 140, 171–180 유력.
  ⚠ 서지만 확인, **본문 미확인** — 받아서 읽은 뒤 확정).
- ⇒ **`kim2026_li_argyrodite_sei_reactive_md` §19 N10 의 "γ 정의는 Shapeev 2016 을 쓸 것" 은 틀렸다.**
- `lev_max`/`level` 도 이 논문에 **없다** (여기 손잡이는 `deg(B_α) ≤ N` + `#α`/`μ`/`ν` 상한).
  `level` 명명은 **Novikov 2021 MLIP package** 쪽 — 개념 계보와 용어 출처를 갈라 적을 것.

**⛔ [Shapeev16] 에서 인용하면 안 되는 것**
- **"MTP 가 GAP 보다 168배 빠르다" 를 우리 계로 이식하는 것** — 텅스텐 **단일 원소**·`R_cut 4.9 Å`·
  2016년 노트북 단일코어·**precomputation 과 이웃목록 구성 제외** 조건이고, GAP 은 저자가 재최적화하지 않고
  [26] 공개값을 쓴 **비대칭 비교**다. **상한값으로만.**
- **"MTP 는 DFT 로 수렴함이 증명됐다"** — Thm 3.2 의 대상은 **타이트바인딩**이고, Kohn–Sham DFT 수렴은
  저자 스스로 *"증명하지 않았고 수치로 관측만 했다"* 고 적는다.
- **(#A)^−0.227 을 MTP 의 상수로 쓰는 것** — 저자 명시 *"보편상수가 아니라 DB 에 의존"*.
- **argyrodite MTP 결과의 근거로 이 논문을 대는 것** — **다성분 확장은 이 논문에 없다**(미래 연구로 식만).

---

**[Park24] `park2024_sevennet_parallel_gnn_md` — GNN-IP 공간분할 병렬화 + SevenNet 원전**
(*J. Chem. Theory Comput.* **20**, 4857–4868, 2024 · Park/Kim/Hwang/**Han**, 서울대 MDIL ·
벤치마크 계 = **α-quartz SiO₂ + 비정질 Si₃N₄** · 배터리·Li·황화물 **0회** · 물성값 0)

> ★ **이 편은 T1b 대조군으로 받았다** — SevenNet 은 **NequIP 기반 등변 GNN = 우리 UMA 와 같은 계열**.
> 🔴 **결론: T1b 는 닫히지 않는다.** 이 논문은 **PES softening 을 재는 실험을 하나도 안 했다**
> (NVE·드리프트·고온 스냅샷 재평가·포논·탄성·D/Ea **전부 0**).

| 항목 | [Park24] SevenNet-0 | 우리 (UMA-s-1p1, omat) | 판정 |
|---|---|---|---|
| 계열 | **등변 GNN** (NequIP) | **등변 GNN** (eSEN + MoLE) | ✅ **같은 계열** ⇒ 대조가 성립 |
| **훈련셋** | **M3GNet 데이터셋** = MP 결정 **이완 3스텝**. 저자 명시 *"액체·비정질은 훈련셋에 없다"* | **OMat24** (1.008억 구조, **AIMD·Rattled 포함**) | 🔴 **다르다. 비평형 방향으로 우리가 더 넓다** ← T1b 핵심 |
| cutoff / 층 수 | **5 Å / 5층** ⇒ 유효 수용영역 **25 Å** | **6 Å** / 층 수 **미기록** | 🔴 **우리 T 를 모른다** — 슬랩 두께 설계 전에 확인 필수 |
| 파라미터 | **0.84 M** (GNoME 16.24 M → 19배 축소) | **150 M / 6 M active** | 🔴 자릿수 차 ⇒ 비용·표현력 비교 금지 |
| **F MAE (평형 근처)** | **0.070 eV/Å** (MP 결정 test set) | **n/a — 우리는 재 본 적이 없다** | 🔴 **우리 공백** ⇒ T1 필요 |
| E / stress MAE | 25 meV/atom · **0.68 GPa** (M3GNet 은 35 / **0.41**) | n/a | ⚠ **응력은 M3GNet 이 1.7배 낫다** — 저자 미언급 |
| MD 엔진 | **LAMMPS 다중 GPU** (Nosé–Hoover NVT) | **ASE 단일 GPU** (Langevin NVT) | 🔴 **우리에겐 다중 GPU 경로가 없다** |
| 고온/비평형 검증 | **비정질 Si₃N₄ 구조 지표 하나**(g(r)·g(θ)·배위수) | 없음 | ⚠ **둘 다 에너지 보존 검사 0** — 우리만의 흠이 아니다 |

**🔑 T1b 에 얻은 것 — 정황 2개(반대 방향) + 경고 1개**
- ① **결정만 학습한** 같은 계열 모델이 **5000 K 초가열 → 급랭**을 구조적으로 통과했다.
  덱 슬 8 의 기구(*평형 근처 편중 → 고에너지 연화*)가 결정적이라면 **더 좁게 학습한 쪽이 먼저** 무너져야 했다.
- ② **평형 근처 힘 정확도는 GNN 0.070 vs MTP 0.073 eV/Å 로 동급**(덱 슬 14).
  덱의 **0.57 eV/Å**(슬 22)은 **fine-tuned + 반응계**라 계 탓일 가능성이 커진다
  ⇒ *"GNN 계열은 원래 힘을 거칠게 본다"* 는 읽기는 **이 표로 지지되지 않는다**.
- ⚠ **경고**: 비정질 생성에서 "골격 연화"는 **원리적으로 안 보인다**(목표 상태가 이미 무질서).
  우리 b2o3 판정 지표(**결정 골격 log-log MSD β ≥ 0.60 @700 K**)를 이 논문 실험으로는 검출 불가.
⇒ **T1b 는 우리가 직접 돌린다**(b2o3 vdW-DFT 재이완). 다만 **값싼 최소판**이 하나 생겼다:
  700 K 스냅샷 UMA 단일점 vs DFT 힘 MAE — 합격선 눈금 **≲0.1 = MTP 급 / ≳0.5 = 반응계 fine-tune 급**.

**🔧 T3 비용 산정 (우리 산술 · 논문 주장 아님)**
논문 실측 `112,000 원자 · 60 ps · 12.7 h · 8×A100` ⇒ **1.58×10⁶ atom·ps/day per A100**
(교차검증 `14,000 원자 · 12.5 h · 1 GPU` = 1.61×10⁶, 효율 0.98 과 일치).
⇒ **T3-small(7,000원자 × 20 ns) ≈ 89 A100-day**(8장이면 ~14일, 단 875원자/GPU 는 저이용) ·
**T3-large(50 ns) ≈ 500 A100-day**. ⇒ **왜 이상욱 랩이 계면 20/50 ns 를 MTP 로 돌렸는지의 속도 쪽 답**
(**Q-T2 의 절반만** 닫힌다 — PES 품질 쪽은 이 논문이 답하지 않는다).

**⛔ [Park24] 에서 인용하면 안 되는 것**
- **"SevenNet 이 MACE 보다 빠르다"** — `Fig. S2` 는 **다른 계·다른 출처**를 겹쳐 그렸다
  (SevenNet=Si₃N₄ 448원자/GPU vs MACE=고엔트로피 합금 500원자/GPU, MACE 값은 ref 32 문헌값).
- **"NequIP 대비 2배"를 일반화** — 32채널·4층·l_max 3·r_c 4 Å·4,608원자·SiO₂ 조건이고 **LAMMPS 버전도 다르다**.
- **"80 % 병렬효율"을 무조건** — **4,608 원자/GPU 조건**. 448 원자/GPU 에서는 **0.79** 로 떨어진다.
- **"GNN 이 비평형에서 검증됐다"** — 검증된 것은 **구조 지표 하나**뿐이다.
- **황화물 이온성 계로의 이식** — 벤치마크는 **공유결합 네트워크**(SiO₂·Si₃N₄), 관측량은 **정적 구조**,
  시간창은 **60 ps**. 우리 축(이온 수송 D/Ea, 20–50 ns, 자리무질서)과 **겹치는 데가 없다.**

**⚠ 우리가 실측한 본문–그림 불일치** (§10-1): 본문 §4.2 의 강스케일링 하한 **"13.1"** 은
`Fig. 5a` 의 **64채널** 점이다. **32채널·2층은 `figure-read ≈ 9.6`**(같은 보정으로 본문 15.4 를 15.29 로 재현).
논문 결론(*"최고 모델도 이상의 절반"*)은 유효하나, **2층 모델의 강스케일링은 본문 인상보다 나쁘다.**

---

**[Nolan18Rev] `nolan2018_computation_accelerated_design_review` — anodic/cathodic limit 의 *정의 문장* · 계면 `ΔH_D` 의 계 대조**
(⚠ 이 논문은 **자체 물성값이 0** 이다. 아래 수치는 전부 **소환값(2차 인용)** 이라 4축 표 행을 만들 수 없다.)

| 항목 | [Nolan18Rev] *Joule* 2, 2016–2046 | 우리 | 판정 |
|---|---|---|---|
| **`anodic/cathodic limit` 의 정의** | ★ **p. 2022 문장**: *"the potentials at which the reduction and the oxidation reactions become thermodynamically favorable, respectively"* (Equation 4 `μ_Li(φ)=μ⁰_Li−eφ` 직후) | `oxidation_limit_V` / `reduction_limit_V` (pymatgen `get_element_profile` 의 상평형 전이 경계) | ✅ **정의 확보** — 계보 8편 중 이 문장이 있는 유일한 편. ⛔ 단 **연산 규칙(`E_D^open ≠ 0` 인 최초 φ)은 여전히 어디에도 없다** → 우리 원고는 우리 정의를 스스로 명시해야 한다 |
| **ESW 의 정의** | *"the gap between the reduction and oxidation potentials based on the Gibbs free energy difference"* + *"different from the band gap or HOMO–LUMO gap; HOMO–LUMO is an **upper bound**"* (p. 2022, ref 65–67) | `window_V` 0.898 V (2.14−1.242) · gap 2.066/2.099 eV | ✅ **우리 "gap 과 ESW 를 섞지 말라" 규율의 문헌 근거**. gap(2.07–2.10 eV) ≫ 창(0.90–1.01 V)인 것은 결함이 아니라 정의상 당연 |
| **계면 `ΔH_D`(= `E_d`) 의 양** | `Fig. 2C`·`Fig. 9B`: 두 상 pseudo-binary 를 혼합분율로 최소화한 **eV/atom**, 음수 = 반응성 | `interface_reactivity_results.json` `min_reaction_energy_eV_per_atom` | ✅ **같은 양** (단위·부호·구성 동일) |
| **소환 대조값** (⛔ 우리 값 옆에 나란히 쓰지 말 것 — 계·hull 세대가 다르다) | `Li₃PS₄`\|`LiCoO₂` **−0.41** → \|`Li₀.₅CoO₂` **−0.56** → **@5 V −1.27** eV/atom (p. 2035, 원출처 ref 70 [Zhu16]) · 산물 `Li₃PO₄+Li₂SO₄+Li₂S+Co₉S₈` | comp1\|`LiCoO₂` **−0.3227** · modelc **−0.3308** · nd **−0.3285** · 산물 `Co₉S₈+Li₂SO₄+Li₃PO₄+Li₂S+LiCl` | 🟢 **산물 4종 완전 일치**(우리 쪽에 `LiCl` 추가 = Cl 이 있어서) ⚠ 값 비교 금지 |
| ★ **개방계 확장의 정량 동기** | **닫힌 −0.41 → 5 V 개방 −1.27 = 3.1×** | 우리는 **닫힌계(OCV)만** 돌린다 | 🔴 **공백**. pymatgen 에 grand-potential 모드가 이미 있으므로 비용 ≈ 0 → **보고량 카드 대상**(φ 선택 규칙을 먼저 선언해야 함, 회신 N) |
| ⛔ **`1.717 V` 함정** | `Fig. 6A` 의 **1.72 V = LGPS 의 환원한계**(첫 리튬화 plateau, P⁵⁺ 환원) | 우리 **1.717 V = `Li₆PS₅Cl` 의 중성 자기분해 OCV** (`→ Li₃PS₄+Li₂S+LiCl`) | 🔴 **숫자만 같고 다른 양·다른 물질.** 나란히 쓰면 **잘못된 문헌 지지**. 우리 환원한계 1.242 V 와 비교할 소환값은 **1.7 V**(argyrodite, p. 2031) — 0.46 V 차, [Rich16] 의 `Li₄P₂S₆` roster 문제와 같은 구조 |
| **AIMD/MD 통계 규율** | *"the error bound of extrapolated RT ionic conductivity can be as large as **two orders of magnitude**"* + *"…significantly larger if **fewer data points** are used to fit the Arrhenius plot"* + *"should consider… the **Haven ratio**"* (p. 2020, 원출처 ref 39) | σ 절대값 인용 금지 · Arrhenius **3점**(600/800/1000 K) · Haven = 1 | ✅ **금지 규율의 문헌 정당화 확보** ⚠ **동시에 우리를 겨눈다** — `Fig. 5C` 의 AIMD 는 **8점(500–1250 K)** 이다. 3점을 쓴 이유(400/500 K 제외 판정)를 원고에 명시할 것 |
| **NEB 단독 주장 금지** | *"knowledge of the energy barriers alone is **inadequate to support claims** about high ionic conductivity"* (p. 2019) | 우리 BVSE·NEB 단독 서술 | ✅ 그대로 인용 가능 |
| **코팅의 anodic 여유** | `Fig. 11B` figure-read: `LiNbO₃` 3.86 · `LiTaO₃` 3.83 · `Li₂SiO₃` 3.70 · `Li₄Ti₅O₁₂` 3.61 · **`Li₃PO₄` 4.21** vs `LiCoO₂` 선 **3.90 V** | 우리 코팅 논의 | 🔴 ⛔ **본문의 "창 2–4 V → 양극에 안정"(p. 2039)은 인용 금지 — 자기 그림이 반증한다.** 대체 문장: *"코팅은 황화물 SE(2.42 V) 대비 +1.2~1.8 V 여유를 벌지만 LCO 전위에선 `Li₃PO₄` 외 여전히 근소 초과"* ⇒ **[Xiao19] 의 "기존 코팅 3종이 자기 게이트 탈락" 과 동형 결론, 다른 경로** |
| **type 1/2/3 계면 분류** | `Fig. 10`(p. 2037; 원출처 ref 63·70·120) — 1 본질안정 / 2 MIEC(계속 성장, 회피) / 3 SEI(e⁻ 절연·Li⁺ 전도, 목표) | 우리 `sei_products` 전자구조 판정 | ✅ **프레임 확보** — "왜 산물의 밴드갭을 보는가" 의 상위 서사 |
| ⛔ **Nd/La 논거 불가** | `Fig. 8` 의 **La³⁺·Nd³⁺·Eu³⁺·Cu²⁺·Yb³⁺ 칸은 두 패널 모두 마커 0개** | 우리 Nd 도핑 축 | 🔴 **이 그림에서 Nd 를 읽어 오면 안 된다** — 데이터가 없다 |
| **스코프** | 황화물 **완전 포함**(LGPS 주인공, `Li₆PS₅Cl` 본문 3회) · **염화물 SE 0회** · Cl 치환 효과 0줄 · 탄성 0 · MLIP 0 | comp1/modelc (Cl-rich 축) | 🟡 **#4·#5 와 달리 우리 계를 직접 다룬다**. 그러나 **Cl-rich 축은 여전히 문헌 공백** |


**[Xiao20Rev] `xiao2020_interface_stability_ssb_review` — 계면 모델 **4층의 위계** + CV 함정의 원인·처방**
(⚠ 이 논문은 ESW·계면반응 값이 있어 **축 B·E·F 에 이미 행이 있다.** 여기는 *방법* 부분만 따로 둔 것.
 ⚠ 원 MERGE-BLOCK 은 3열 한 행이었다 — **`우리`·`판정` 두 칸은 MERGE 때 우리 원장에서 채웠다.**)

| 항목 | [Xiao20Rev] | 우리 | 판정 |
|---|---|---|---|
| **★★ 계면 모델 4층의 위계** | ① **ESW = worst-case** / ② **topotactic = best-case** / ③ **pseudo-binary = 최대 구동력**(Li·O 개방 확장) / ④ **explicit·AIMD = 국소 재배열**(<1 ns · 시작배치 민감) | 우리는 **①(`constrained_esw_cl_scan` 2.256 V)** 과 **③(`interface_reactivity` −0.3227 eV/atom)** 만 계산한다. ②·④ 는 안 한다 | 🔑 **우리 두 값의 위계가 정해졌다** — 2.256 V 는 **하한**(worst-case), −0.3227 은 **최대 구동력**이다. ⛔ 한 문장에 둘을 "안정성" 으로 뭉뚱그리지 않는다 |
| **CV 함정의 원인과 처방 3** | ⓐ **탄소 복합 WE 로 반응면적 확대** — 평면전극 10 nm 층은 0.1 mV/s 에서 **~0.3 µA/cm²** 밖에 안 나온다 / ⓑ **cutoff 전류 금지** → 전류 급증 전위 + 산화산물의 **환원 피크**로 읽는다 / ⓒ **Li 대극·기준극 금지** → In·Au 대극 + In·Ag₃SI/Ag 기준극 **3전극** + TEM·XPS 보강 | 우리는 CV 를 하지 않는다(계산만) | ⬜ **해당 없음 — 그러나 문헌 CV 값을 인용할 때 이 셋을 확인한다.** ⓒ 가 바로 우리가 밟은 함정이다: Zuo 2023 의 CV 창이 **vs In/InLi** 라 우리 값이 창 아래 0.34 V 로 보였다 |
| **`Fig. 1` = 양극 복합체 계면 12칸 목록** | 양극 복합체에서 생길 수 있는 계면을 12칸으로 나눈 표 | — | ⬜ **우리가 안 본 칸을 색칠할 틀.** 향후 사용 |


**[Lu24] `lu2024_lowtemp_assb_li2zro3_interface` — ① 계면 Li site-energy 프로파일 ② 범용 MLIP 의 계면 실패 ③ DRT 5피크 사전**
(⚠ 이 논문은 σ·Ea 값이 있어 **축 A 에 이미 행이 있다.** 여기는 *방법* 부분만 따로 둔 것)

| 항목 | [Lu24] | 우리 | 판정 |
|---|---|---|---|
| **NEB 가 안 되는 계면의 대안** | `E_total = Σ E_i` 분할 → Li 원자별 site energy 를 **계면 법선 z 로 프로파일** → 95th 포락선의 max−min 을 "장벽" 으로 | 우리는 계면에 NEB 를 시도조차 못 했다 | 🟡 **개념은 이식 후보, 실행은 안 됨** — ⛔ **안장점을 안 넘으므로 migration barrier 가 아니다**(자리에너지 차 ≤ 진짜 장벽). NEB 와 대조한 계가 **0개**다. 우리가 쓴다면 **벌크에서 NEB 교차검증 필수** |
| **MLIP 게이지** | 계면 4종에 **각각 따로 fine-tune** 한 4개 모델로 얻은 0.14/0.17/0.28/0.48 eV 를 **한 줄에 세운다** | — | 🔴 **그대로 따라 하면 안 된다.** 고치는 법: 4계면+각 벌크를 **한 데이터셋으로 공동 fine-tune**(게이지 공유) 또는 각 계에 **자체 벌크를 기준자로 삽입** |
| **★★ 범용 사전학습 MLIP 의 이종계면 실패** | `Table S2`: 사전학습 M3GNet 의 계면 에너지 **R² = 0.02 / 0.11 / 0.01 / 0.18** → fine-tune 후 **0.98 / 0.95 / 0.97 / 0.98** | UMA-s-1p1 을 **fine-tune 없이** LPSCl MD 에 쓴다(벌크는 검증된 표준) | ⭕⭕⭕ **가장 값어치 있는 이식.** *"벌크에서 되던 범용 MLIP 이 이종계면에서 무너진다"* 의 외부 실측. **작업**: 우리 계면 DFT 스냅샷에 UMA 를 얹어 에너지 상관 R² 를 본다(반나절). 결과가 어느 쪽이든 **우리 계면 계산 신뢰구간을 정한다** |
| **계면 제작 규약** | pymatgen `CoherentInterfaceBuilder` · 면적 ≤ 400 Å² · 총 원자 < 500 · 성분당 Li **4층 이상** · LiNiO₂ **(101)** 고정 · **부정합을 표로 보고**(1.1 / 4.8 / 2.4 / 3.9 %) | `run_cathode_interface.py` = **rigid stack**(격자 그대로 겹침), 부정합을 **보고하지 않는다** | ⭕ **이식 후보 (T2)** — 최소한 **부정합 수치를 보고하는 습관**. ⚠ 다만 [Lu24] 셀은 z 가 **16–35 Å 로 2배 이상 들쭉날쭉**해 finite-size 가 교락됐다(가장 큰 장벽 0.48 eV 가 가장 얇은 셀에서 나왔다) — **두께를 맞추는 것이 먼저** |
| **무질서 처리** | Ni 5 % → Co, 5 % → Mn **무작위 단일 배열**, 반복 0회 | comp2 실측: 배열에 따라 Ea 가 **0.275 ↔ 0.151 eV**(1.8배) | 🔴 **우리가 훨씬 엄격하다.** [Lu24] 의 0.14 vs 0.17 차이는 **배열 노이즈 안**일 수 있다 — 이 단서 없이 인용 금지 |
| **EIS 분해** | **DRT**(모형 없는 역변환) + `Table 1` 5피크 귀속(D1 SE 입계 / D2 접촉 / D3 CEI / D4 전하이동 / D5 확산, τ = RC = 1/2πf). 귀속은 *"empirically·may·possibly"* | 우리 그룹 **[Kim25TLM]** = **modified TLM**(물리 모형 먼저) | ⭕ **짝으로 묶는다**: *"봉우리에 이름 붙이는 두 방식 — 모형 없는 분해(DRT) vs 모형 있는 분해(TLM)"*. DRT 는 **귀속을 해 주지 않는다**는 점이 핵심 |


> ⚠ **A–D 물성 4축 표에는 넣지 않는다.** 계가 고분자 전해질이라 σ·ESW·탄성·gap 어느 행에도
> 올릴 수 없다(값이 있어도 **정의가 다른 양**이라 `n/a` 보다 나쁘다 — 숫자가 있어 오인된다).
> (선례: §K 수계 Zn 축, §L 자기감사 축 — 둘 다 4축 밖에 따로 뒀다.)

**[Yu26Pol] `yu2026_pvdf_mos2_anion_solvent_confinement` — ⛔ *물성 전이 금지·방법 반면교사 3건*** (2026-09-12 신설)

> ⚠ **우리 계가 아니다.** PVDF+LiFSI 고분자 전해질 + MoS₂ 필러. σ·Ea·D·LSV 창 **전부 소환값이고
> 우리 원장과 정의가 다르다.** 아래는 *값* 이 아니라 *규율* 만 가져오는 블록이다.

| 항목 | [Yu26Pol] | 우리 | 판정 |
|---|---|---|---|
| **보고량 정의** | `Fig. 3`d 가 `Li⁺–X`(2체)와 `Li⁺–X on MoS₂`(**3체**)를 **같은 축 한 그림**에 놓는다. SI 식은 `E_tot−(E_slab+E_mol)` **2분할뿐** — 어느 분할인지 선언 없음. admissible 분할 **4가지** | `kb/templates/estimand_card.md` §1–3 을 **던지기 전에** 채운다 (2026-08-28 채택) | ✅ **우리 승 — 외부 실물 사례로 카드에 인용 가치** (우리 SDCP 8회 반려와 동일 병이 AEM 을 통과했다) |
| **vdW 보정** | ⛔ **없음**. 층상 MoS₂ 위 물리흡착인데 PBE 순정. 주장하는 차이(0.07·0.29 eV) < 누락 보정 크기(0.2–0.5 eV). ⚠ 정작 **MD 의 RESP 전하 계산엔 D3(BJ) 를 썼다** | 우리 흡착 축은 functional·보정 명시가 게이트 | ✅ 우리 승 |
| **하전종 처리** | Li⁺·FSI⁻ 를 다루며 **배경전하·셀크기·전하상태 선언 0건**. `Li⁺–FSI⁻ = −0.29 eV`(쿨롱항만 ≈7 eV) 가 그 증상 | 명시 규율 | ✅ 우리 승 |
| **MSD 창** | **미기재**. 역산 결과 R-CPE=원점통과 `MSD/6t`(8.47 vs 인쇄 8.4×10⁻⁹, 1 % 일치) / PPE=자유절편 추정(2.30 vs 인쇄 2.0) ⇒ **두 곡선에 다른 규약** | **2–50 ps 고정·자유절편**, `tools/convention_check.py` 로 0위반 강제 | ✅ **우리 승 (규율 존재 자체가 차이)** |
| **확산영역 검증** | `Fig. S14`d 축 파손(`Log(MSD)` 눈금이 0~−600). PPE 50 ns RMS 변위 **2.6 Å**(≈Li–O 1결합), 기울기 **0.89<1** ⇒ **PPE D 는 수렴 안 됨** | 창 고정 + 로그기울기 | ✅ 우리 승 |
| **시드·오차막대** | **1 시드 추정, 오차막대 0** | 멀티시드만 판정 (단일시드 1.33× **철회**, SEMIFINAL 2026-07-09) | ✅ 우리 승 |
| **아레니우스 점 수** | **7점** (293–353 K, EIS 실측) | **3점** (600/800/1000 K, MLIP-MD) | ⭕ **그들 승** — 우리 3점은 기울기 불확실도를 못 준다. (실험이라 유리한 건 맞지만 지적은 유효) → **점 수 명시 + 5점 확장 검토**(제안, 판정 아님) |
| **궤적 길이** | **50 ns** (dt 1 fs, 고전 역장) | prod **200 ps** (dt 2 fs, MLIP) | ⭕ 그들 승(계가 느려 필요). **우리가 비정질·고분자로 갈 때의 현실 척도** |
| **RDF 배위수 검산** | ⛔ **안 함** — 본문·`Fig. 3`e·`Fig. 3`f **삼자 불일치**. 물질수지(`N_Li×CN ≤ N_lig×O_per_lig`)를 대면 본문 PPE 값이 **DMF O 하나당 Li 3.92개**를 요구해 탈락 | 현재 **우리도 안 한다** | 🔴 **T1 이식 — `tools/ionic/` RDF 경로에 assert 한 줄.** 이 한 줄이 "그림 라벨 오배정" 을 원천 차단한다 |
| **모델↔실험 정합** | 성능 이유로 든 **다공성(BET 22×)·N-도핑**이 **DFT 모델에 둘 다 없다**(MD 엔 N만). ⇒ 계산은 "기저면 일반론" 까지만 | 우리 무질서 처리(SQS/enumerate)는 선언 규율 | ✅ 우리 승 |

**⛔ [Yu26Pol] 에서 우리 축으로 이식 금지 (전수)**
1. ΔE 7개 전부(`Fig. 3`d·`Fig. S13`) — 보고량 미정의 + vdW 누락 + 전하 미기재 + 물리적 불가값 2개
2. `Fig. 2`e ESP — 본문은 *"MoS₂ 표면 음전위"*, 그림은 컬러바(−0.02~+0.08) 상 **주황/빨강=양전위**. 주장과 그림이 반대
3. PPE `D = 2.0×10⁻⁹ cm²/s` 및 "4.2배" 비율 — 확산영역 미도달
4. 배위수 4개의 **귀속** — 삼자 불일치. **총 CN 4.24→3.26 만** 인용 가능, 그것도 *"음이온 우위 역전"* 이 아니라 **"용매 이탈"** 로 서술
5. `4.47 V` 를 "전기화학 안정창" 으로 — 10 µA 임의 문턱 + 본문(4.04) ↔ `Fig. S19`(4.25) 불일치. ⛔ **우리 grand-potential onset 2.256 V 와 같은 표 금지**
6. 🔴🔴 **`Ea = 0.23 eV` 를 우리 `modelc 0.224 eV` 옆에** — 숫자만 같고 양이 다르다(EIS 겉보기 σ-활성화 ↔ MD Li 호핑). **이 편의 제1 인용사고 위험**
7. "CASTEP" 이상의 코드 해석 — *"CASTEP + PAW + 520 eV"* 는 자기모순(CASTEP 은 PAW 코드가 아니고 520 eV 는 VASP/MP 관용값)


(⚠ 이 논문은 §E 에 이미 행 3개가 있다. 여기는 **값이 아니라 규약**만 따로 둔 것이다.)

**[Meng26LZF] `meng2026_pvdf_li2zrf6_phase_ordering` — ⛔ *물성 전이 금지 · `[Yu26Pol]` 의 짝편*** (2026-09-15 신설)

> ⚠ **우리 계가 아니다.** PVDF+LiFSI 고분자 전해질 + **m-Li₂ZrF₆ 2 wt%** 불화물 필러.
> σ·Ea·t_Li⁺·LSV 창 **전부 소환값이고 우리 원장과 정의가 다르다.**
> ⚠ **Journal Pre-proofs** — Version of Record 아니다. 인용 시 지위를 밝힌다.
> 아래는 *값* 이 아니라 *규율* 만 가져오는 블록이다.

| 항목 | [Meng26LZF] | 우리 | 판정 |
|---|---|---|---|
| **보고량 정의** | `Fig. S14` 의 `FSI⁻ / m-Li₂ZrF₆ = −5.21 eV` 가 **주기 셀**(그림에 점선 상자)인데 **전하 상태·배경전하 보정·스핀 선언이 0건**. 중성 라디칼이면 스핀, 음이온이면 jellium 보정이 필요한데 **어느 쪽인지도 안 밝혔다**. 게다가 설정은 **NVT MD**(1 fs, 333.15 K)인데 식은 **정적** `E_tot−E_sub−E_mol` — **프레임 선택/집계 규칙 없음** | `kb/templates/estimand_card.md` §1–3 을 **던지기 전에** 채운다 (2026-08-28 채택) | ✅ **우리 승 — 외부 실물 사례 2번.** 우리 SDCP 흡착에너지 **8회 반려의 P0(참조·스핀/전하 미선언)와 같은 층위**다. ⛔ 우리 db 숫자는 끌어오지 않는다 — **구조만** |
| **범함수·분산보정 확정** | 🔴 **SI §2 의 인용 3개 중 2개가 어긋난다**: *"CASTEP module within the MD framework"* 에 **Grimme D3(BJ)**(*J. Comput. Chem.* 32, 1456), *"GGA-**PBE**"* 에 **PW91**(Chevary/Perdew, *PRB* 46, 6671) ⇒ **어느 GGA 인지, D3 를 썼는지 판독 불가** | functional + vdW 명시가 인용 게이트 | ✅ **우리 승 — 이 하자 하나로 E_ads 3개가 전부 인용 불가가 된다** |
| **계산 사양 공개도** | ⛔ cutoff · k-점 · 의사포텐셜 · 셀/원자수 · 수렴문턱 · MD 길이 · 시드 · 슬랩두께/진공 **전부 미기재**. 적힌 것은 NVT / 1 fs / 333.15 K / "PBE" 뿐 | 전 항목 명시 + 스크립트·db 공개 | ✅ 우리 승. (비교: `[Yu26Pol]` 은 **520 eV / 2×3×1 / 10⁻⁶ eV / 0.001 eV/Å** 은 적었다 — **Meng 이 더 얇다**) |
| **≈−5 eV 흡착 이상치** | `FSI⁻/m-LZF = −5.21 eV` 를 *"strong chemisorption"* 이라 서술하는데, **`Fig. S14` 그림에는 새 결합이 안 보이고 FSI 가 표면 위에 떠 있다**. 불화물 표면 통상치(−0.3~−1.5 eV)의 3–15배 | 기하↔에너지 정합을 보고량 카드에서 미리 묻는다 | 🔴🔴 **`[Yu26Pol]` 의 `MoS₂/DMF = −4.59 eV` 와 같은 실패 모드다** — 두 편 모두 **물리흡착 자세 + 화학결합 규모 에너지 + 전하/셀/vdW 미선언**. ⇒ **분야 관행일 가능성**(§digest 7b-bis). 우리 가설이고, 입력파일 비공개라 확인 불가 |
| **비교량 정규화** | α(−0.23) ↔ β(−0.71) 를 같은 막대그래프에 놓는데 **단량체당/접촉면적당 정규화 없음 + 두 모델이 같은 크기라는 선언 없음**. 게다가 β는 평면 지그재그라 **접촉면적만으로도** 더 세게 붙는다 — 그 자명한 기여와 "격자정합" 기여를 **분리하지 않았다** | 같은 축에 놓는 두 값은 같은 분모를 갖는지 먼저 선언 | ✅ 우리 승 |
| **XPS 피팅 하드 제약** | 🔴 `Fig. S5` 의 **Zr 3d 스핀-궤도 이중선 면적비가 3:2 를 역방향으로 위반**(3d₃/₂ 를 ~3× 크게; 필요한 것은 3d₅/₂ 가 1.5×). 분리폭 2.26 eV 도 문헌 2.4 보다 작다 | 현재 **우리도 XPS 인용 시 이 체크를 안 한다** | 🔴 **T1 이식 — 우리 XPS 앵커표(§interface_reactivity 계열)에 "이중선 3:2 · 5/2 가 낮은 BE" 검산 한 줄.** `[Lai20]`·`[Zuo22]` 앵커를 다시 쓸 때 적용 |
| **다형(polymorph) 주장의 판별력** | 🔴🔴 *"m-Li₂ZrF₆ → t-Li₂ZrF₆ 전환 confirm"* 의 근거가 **XPS BE** 와 **TOF-SIMS `ZrF⁻`** 뿐이다. 같은 조성·같은 Zr⁴⁺·같은 ZrF₆ 배위의 **다형 코어준위 이동은 <0.5 eV** 인데 제시된 새 성분은 **182.5/180.1 eV = ~5.4 eV 아래**이고 논문 스스로 **"Li–Zr–O"**(산화물)라 부른다. `ZrF⁻` 는 어떤 Zr–F 상이든 준다. **SEI 의 XRD/SAED/라만 격자모드는 안 했다** | 우리 `interface_reactivity` / LPSCl@Li₂S 계면상 트랙 | 🔴🔴 **T1 이식 — "어떤 측정/계산이 이 상을 *유일하게* 지목하나" 를 계면상 주장 전에 적는다.** 이 편은 그 물음 없이 기전을 귀속했고, 그 결과 **`0.22/0.31 eV` 적용 근거와 "전기장 구동"(무전류 대조군 없음)이 함께 흔들린다** |
| **소환값 vs 자체 계산** | **이 논문이 계산한 이동장벽은 0개.** `0.22 eV`(벌크)·`0.31 eV`(입계)·m-LZF 제조법·t-LZF XPS 기준 BE **넷 다 [56] Q. Xu et al., *Nature* 637, 339 (2025)** | 우리는 소환값과 자체값을 `canonical_registry` 에서 분리 | ✅ 우리 승. ⛔ *"Meng 2026 이 0.22 eV 를 보였다"* 는 **오인용**. **[56] 확보가 1순위** |
| **아레니우스 검증 가능성** | Ea 0.37→**0.26 eV**(EIS 25–80 °C). 🔴 원자료 `Fig. S15`·`Fig. S16` 을 **우리가 못 뽑았다**(`.doc` 내장 형식) ⇒ **점 수·선형성 미검증**. VTF 곡률 검토도 논문에 없음 | 3점(600/800/1000 K) + 600 K 3-시드 오차막대 | ⚠ **양쪽 다 약하다.** (비교: `[Yu26Pol]` 은 **7점**이 그림에 보였다) |
| **벤치마크 표의 조건 명시** | ⭕ **`Table S1` 캡션이 시험조건(0.1 mA cm⁻², 0.1 mAh cm⁻²)을 명시** — 9편 비교가 apples-to-apples | 우리 비교표 관행 | ⭕ **그들 승 (관행으로 채택할 것).** 단 **Li 450 µm ⇒ 반쪽사이클 DOD 0.11 %**(digest 산술)와 **CCD 미측정**은 표에 없다 |
| **격자정합 논증의 검산 가능성** | ⭕ b **4.875 ↔ 4.91 Å**(−0.71 %) / c **2.588 ↔ 2.56 Å**(+1.09 %) — **독자가 재검증할 수 있는 형태**이고 β-PVDF 쪽 값은 표준값과 일치 ✓. 🔴 단 m-LZF 쪽은 **공간군·격자상수·구조 출처 미기재**라 검증 불가 | 우리 구조는 항상 출처(ICSD/MP id 또는 완화 구조 경로) 병기 | ⭕/🔴 **절반은 그들 승(형식), 절반은 우리 승(출처)** |
| **대조군 교란** | 막 형태가 **다공(PVDF) ↔ 치밀(PVDF-LZF)** 인데 **치밀도만 같게 한 대조군 없음** | — | 🔴 **`[Yu26Pol]` 과 똑같은 교란** — PVDF 계 두 편이 공유하는 구조적 약점 |
| 데이터 공개 | ⛔ 없음 ("요청 시") — 구조파일·궤적·입력파일 비공개 | 우리 db + 스크립트 | ✅ 우리 승 |

**⛔ [Meng26LZF] 에서 우리 축으로 이식 금지 (전수)**
1. **E_ads 3개 전부** (`−0.23` / `−0.71` / `−5.21 eV`) — 범함수 확정 불가 + vdW 불명 + 정적/동적 미선언 + 정규화 미선언 + 참조·전하·스핀 미선언
2. 🔴🔴 **`0.22 eV` / `0.31 eV` 를 "이 논문의 결과" 로** — **[56] 소환값**이다. 그리고 **우리 modelc `Ea = 0.224 eV` 옆에 두지 않는다** (숫자만 같고 물질·방법·저자가 전부 다르다 — **이 편 제1 인용사고 위험**)
3. **`4.78 V` 를 "전기화학 안정창" 으로** — 판정 문턱 미기재. ⛔ **우리 grand-potential onset 2.256 V 와 같은 표 금지**
4. **"m→t 전환" 을 확정 사실로** — 제시된 증거는 두 다형을 구분할 수 없다. 쓸 수 있는 것은 *"순환 후 Zr 화학환경이 크게 바뀌었고 저자들은 이를 t-Li₂ZrF₆ 로 귀속했다"* 까지
5. **Li 대칭셀 수명 "2100 h" 또는 "2180 h" 중 하나만** — 논문 안에서 갈린다(초록 2100 ↔ 본문·결론·`Table S1` 2180). 둘 다 적거나 안 적는다. 조건(0.1 mA cm⁻²·0.1 mAh cm⁻²·Li 450 µm)도 함께
6. **5 C "초기 용량 92 mAh/g"** — `Fig. S23` 첫 방전점은 **figure-read ≈163 mAh/g**. "80 %" 는 **후-형성 기준**
7. **FTIR β 분율과 GIWAXS β 분율의 일치를 "교차검증" 으로** — **같은 양이 아니다**. Lambert–Beer 식은 α/β 2상 가정이고 840 cm⁻¹ 는 β·γ 공유 밴드인데 GIWAXS 는 γ 를 17–19 % 로 본다. 인용은 *"두 방법 모두 β 상 증가를 보인다"* 까지
8. **σ·Ea·인장강도(MPa)를 우리 아지로다이트 값(GPa 결정 탄성 / MD Ea)과 같은 표에**
9. **"CASTEP 이라고 적혀 있다" 이상의 코드 해석**


**[Li26FDI] `li2026_functionally_differentiated_interphase` — ① CCD 계단 보고 규약(반면교사) ② NEB 끝점 축퇴 게이트 ③ 계면 CDD 의 isovalue 규약**

| 항목 | [Li26FDI] | 우리 | 판정 |
|---|---|---|---|
| **★★ CCD 보고 규약** | 보고값 8개가 **전부 `0.199 mA cm⁻²` 의 정수배**(n = 2/3/4/7/11/18). 즉 "마지막 통과 계단" 인데 **4자리 유효숫자**(3.581)로 인쇄 | 우리는 CCD 실험이 없다 | 🔴 **반면교사.** 계단시험 보고량은 **①계단 크기 ②마지막 통과 ③실패 계단 ④전극 면적** 을 같이 적어야 한다. 이 논문은 **전극 면적을 안 밝혀** 0.199 의 출처(전류÷면적)조차 특정 불가. `kb/templates/estimand_card.md` 의 "보고량 정의" 항목 후보 |
| **★★ NEB 끝점 축퇴** | `Fig. 1j`(Li₃N 0→**−0.0082**) · `Fig. 1m`(LPSCl 0→**−0.152 eV**) **둘 다 끝점 비축퇴** — 그런데 정방향 장벽만 보고. LPSCl 역방향은 ≈**0.40 eV** | `db/properties/sei_neb.json` 은 결과마다 **`endpoints_symmetry_equivalent`** 를 저장하고 False 면 blocking | ⭕⭕ **우리 게이트가 더 엄격하다.** 우리 NEB 캠페인은 `retracted`(n_citable 0)이지만 **이 게이트만은 살아 있다** — 방법론 카드에 쓸 만한 자산 |
| **★ NEB 수렴 하한** | 힘 허용 **0.02 eV Å⁻¹** 로 **0.0103 eV**(Li₃N, 이미지 간격 ≈0.44 Å → 허용오차 ≈0.009 eV)·**0.0166 eV**(LPSCl intra-cage, 간격 ≈0.6 Å → ≈0.012 eV)를 보고 | — | 🔴 **장벽 ≈ 오차.** 게다가 CI-NEB 는 사슬당 **한 이미지만** 안장점으로 올리므로 부차 극대(0.0166)는 수렴 안장점이 아니다. ⛔ *"Li₃N 이 Li₂O 보다 23배 빠르다"* 식 비율 인용 금지 |
| **★ 계면 CDD 규약** | 차등전하밀도 11패널에 **isovalue 미표기 · 적분(Bader) 0 · 평면평균 Δρ(z) 0** → 패널 간 "뚜렷/완만" 비교가 정량이 아니고, 실제로 **본문 서열이 그림 인상과 어긋난다**(우리 판독: Li₂O·Li₃N 로브가 LiF 보다 크다) | 우리 CDD 그림(하우스 스타일) | ⭕ **우리 규약으로 못박자**: CDD 에는 **isovalue + Bader 적분 전하**를 항상 병기. 바른 예는 `[Luo22]` (Bader 로 전해질 순전하 정량) |
| **★ 전자차단 주장의 필요조건** | "전자차단" 을 **각 상의 단일상 DOS** 로만 논증. **밴드정렬·일함수·Schottky 장벽·계면 PDOS 전부 없음**. 게다가 7패널이 **각자 E_F 에 정렬**돼 공통축이 아니다 | 우리 `sei_products.json` 갭 사다리도 **정렬이 아니라 갭**이다 | 🟡 **우리에게도 같은 구멍이 있다.** 계면 전자주입은 갭이 아니라 **정렬**이 정한다 → 우리 SEI 전자차단 주장에 **슬랩 일함수라도 붙이는** 것이 다음 숙제 |
| **⛔ 미기재 전수** | k-메시 · 슈퍼셀 크기/원자수 · 진공층 · vdW · 스핀 · NEB 이미지 수 · **결함 기구(공공/침입형)** · **S²⁻/Cl⁻ 무질서 처리** · 계면/DOS 계산의 수렴기준 · 시각화 도구 | 우리는 `protocol_hash`/`protocol_payload` 에 전량 박는다 | 🔴 **재현 불가.** 특히 **아지로다이트 무질서 미처리**가 치명적이다 — 우리 comp2 실측으로 배열에 따라 Ea 가 **0.275 ↔ 0.151 eV**(1.8배). `Fig. 1m` 끝점이 −0.152 eV 인 것 자체가 **특정 단일 배열**의 증거 |
| **사장된 방법 2건** | SI 식 **(S1) 계면에너지 γ** 정의만 있고 **값이 어디에도 없음** · SI 물리분석절의 **XRD** 도 **데이터 0장** | — | ⚠ 성분 선택의 **열역학 근거가 통째로 비어 있다**. 우리가 이 편을 "계면에너지로 코팅을 골랐다" 로 인용하면 **틀린다** |


★ 넣을 절 = **「### J-7. 🔧 방법 원전 — 물성값이 없어서 표에 못 넣는 편」**
    (기존 [Wang26IF]·[Shapeev16] 블록 **뒤에** 아래 블록을 통째로 추가)

**[Makino26Rev] `makino2026_mlip_battery_materials_review` — MLIP *검증 규율*의 원전**
(*PCCP* Accepted Manuscript 2026, 공개 09-10 · 나고야공대 + **Preferred Networks/Matlantis** 공저 · refs 216 · **자체 계산 0 · 물성값 0**)

| 항목 | [Makino26Rev] | 우리 (UMA-s-1p1, omat) | 판정 |
|---|---|---|---|
| **정적 오차 → 동역학 정확도** | ⛔ **다리를 놓지 않는다.** §3.5 *"안정한 MD 를 보증하는 **균일한 힘-오차 기준은 없다**"*(Morrow 2023, ref 95) · §3.6 *"진단 그림이 재는 것은 참조 분포에 대한 충실도 = **내삽 정확도**뿐"*(ref 130) | 회신 BP Q2: *"두 정적 점의 RMSE → MD 산포·Ea 오차막대로 **직접 환산 불가**"* | ✅✅ **완전 일치 — 우리 판정의 외부 권위.** 원고·회신에서 *"과하게 조심한다"* 는 반론의 답 |
| **검증 대안 처방** | **5개**: ⓐ 준평형 / ⓑ 격자·좌표 강제변위 / ⓒ NEB 전이상태 근방 **3구간 오차 분리 보고** + ⓓ 성질 수준(장벽·아레니우스 기울기·**포논**·**RDF**) | ⓐⓑ 미실시 · ⓒ 미실시 · 포논 **미보유** · RDF **보유** | ⭕⭕ **이식 후보 (T1, 추가 DFT 0회)** — ⓐ+ⓑ+RDF 는 UMA 단일점만으로 오늘 가능 |
| **힘 오차 지표의 정의** | ⛔ **정의 0건.** 인용 4수치 전부 성분 RMSE / 벡터 RMSE 구분 없음 (`Fig. 6c` 만 MAE 표기) | 원소별 `F_mean` + 전체 `F_RMSE` + cos 각도 분리 기록 | 🔴 **정의 미상 ⇒ 우리 0.0948 eV/Å(S)과 같은 칸 금지.** 맞추려면 ±√3 |
| **uMLIP 힘 오차 수준** | **0.12–0.17 eV/Å**(전이금속 없는 계) / **0.4–0.5 eV/Å**(일부 TM 화학공간) — ref 127. 단일계 특화 NequIP 는 **6.5 meV/Å**(Li₆.₇₅P₃S₁₁) | 정적 1점 원소별: Li 0.0141 · P 0.0151 · Cl 0.0186 · **S 0.0948** eV/Å | 🟢 **자릿수 방어 성립** — 우리 S 값은 문헌 uMLIP 범위의 **아래쪽**. *"우리 UMA 가 유별나게 망가졌다"* 는 근거 없음. ⛔ 단 정의 미상이라 **표 병치 금지** |
| **원소별 오차 분해** | ⛔ **없음.** 전이금속 유무 2분이 전부. **황(S) 앵커 0건** | 원소별 분해 **있음** | 🔴 **외부 확증 못 얻음.** 가장 가까운 대리 = `Fig. 6c` **K₂₄Li₁₆P₂₄Sn₈ @1000 K 힘 MAE `figure-read ≈ 198→50 meV/Å`** (7×10⁴→9×10⁷ 데이터) |
| **uMLIP 의 Ea 편향** | *"uMLIP 은 **전이상태 학습 데이터가 없어 활성화에너지를 과소평가하는 경향**"* → NEB 구조를 넣어 fine-tune 해야 회복(ref 183) | 우리 Ea 는 전부 **fine-tune 없는 UMA-MD** 산 | 🔴🔴 **직격.** `kb/open_items.md` 에 *"UMA Ea 방향편향: 미측정, 문헌 일반진술상 **과소** 방향"* 등재 필요 |
| **MD 프로토콜 규약** | ⛔ **없음.** 전문 `seed` **0건** · `300 K` 0건 · MSD 시간창 0건 · Haven 1건(성질명으로만) · Arrhenius 2건 | 창 2–50 ps 고정 · D=기울기/6 · 600/800/1000 K 3점 · 3–4 시드 · NE(Haven=1) | 🟢 **충돌 없음 — 우리가 앞서 있다.** 리뷰가 표준을 못 세운 자리다 |
| **고온 아레니우스 외삽** | ref 173: *"AIMD 의 RT σ 과대평가 원인 = **고온 단일-아레니우스 가정 + RT 외삽** (+ PBE 격자상수 과대)"*. MTP 로 **300–800 K** 장시간 MD 를 돌리자 기전 전이가 드러남 | 600/800/1000 K 3점 · **RT 외삽 금지** 규율 보유 (`RT_extrapolation` prohibition) | 🟠 **우리 규율이 이미 막고 있다.** 남은 부담은 *"세 점이 한 기전인가"* — `lpsocl_box331` 의 사전등록 ±0.050 eV 마진(segment 차 −0.024 eV)이 그 대응 |
| **σ 절대값 / 결함모델 지배** | `Fig. 9c`(LLZO, ref 179): **같은 MLIP·같은 물질**에서 결함 모델만 바꿔 **Ea 0.334→1.227 eV**, **σ(300 K) 2.102×10⁻⁴→7.236×10⁻¹⁵ S/cm** | `prohibitions: absolute_sigma` 전 계 적용 · `MD_sigma_ratio_*` 는 `citable: false` | ✅✅ **우리 금지규율의 최강 외부 근거.** 문헌은 σ 절대값을 그대로 싣는 관행이고, `Fig. 9c` 가 그 관행의 위험을 자기 데이터로 증명한다 |
| **MLIP 계면 붕괴** | §3.6·§3.7: 계면·비정질·반응은 **자유도가 방대해 학습 확보가 훨씬 어렵다**(정성 진술, **수치 0**) | — | 🟡 **[Lu24] `Table S2` 가 훨씬 세다** (사전학습 M3GNet 계면E **R² 0.01–0.18** → fine-tune 0.95–0.98). ⇒ **계면 축의 정량 근거는 계속 [Lu24], 이 리뷰는 정성 보강** |
| **역할 분담 워크플로** | `Fig. 10h`: 구조는 **MLIP-MD**, 전자구조는 **QM** (Li\|LLZO 공간전하 폭 **1.1 nm**) | 우리 DOS/gap 은 **정적 완화 구조 1개**에서만 | ⭕ **이식 후보 (T2)** — UMA-MD 스냅샷 위 QE nscf ⇒ **유한온도 gap 분포** (우리 "gap 은 무질서 민감" 규율과 같은 방향) |
| **구역 분해 MSD** | `Fig. 10c`: 계면 법선 **MSD_z 분해 + 체류 필터**로 Li 를 4분류 | 셀 전체 평균만 | ⭕ **이식 후보 (T1)** — **[Wang26IF] 에 이어 두 번째 독립 출처** ⇒ 우선순위 상향 |

**⛔ [Makino26Rev] 에서 인용하면 안 되는 것**
- **`Fig. 9f` 의 σ 값(색막대 0–27)** — **단위가 그림에 없다**, 출처는 ref 187(미확보), **무질서 정의(`S/Cl site inversion %`)가 우리 d 파라미터와 같다는 보장이 없다**, 게다가 **캡션과 그림의 방향이 어긋난다**(캡션 *"문턱 넘으면 증가"* ↔ 그림 *"문턱 오른쪽 고inversion 에서 붕괴"*). ⇒ **지형(비단조·내부 최적)까지만.**
- **`Fig. 6b` 의 5.4 meV/atom 을 "PFP/uMLIP 정확도"로** — 3000 K DFT-MD 스냅샷 **재채점 1건**이고, 같은 리뷰 §3.6 이 그런 시험의 한계를 적는다. **우리 δΔE 1.34 % 도 같은 이유로 성과가 아니다**(레지스트리 기존 금지와 일치).
- **`Table 1`·`Table 2` 의 등급을 근거로 모델을 고르는 것** — 캡션이 *"저자의 주관적 판단"* 이라고 자백한다.
- **`Fig. 7c` 의 census 숫자** — SI 대비 **25편(18 %) 결손**. census 를 인용하려면 **SI `Table S1`**(우리 §12 재집계)을 쓴다.
- **"Li₃N 에서 MLIP 이 soft mode 를 놓친다 ⇒ UMA 도 그렇다"** — `Fig. 9a` 는 **eSNAP(A1 계열)** 이야기다. *"Li₃N 은 MLIP 이 어려워하는 계"* 까지만.


> 📌 **왜 물성 4축(A–D)이 아니라 J-7 인가 — 두 가지 이유를 합친 것이다.**
> ① **J-7 의 기존 사유**(*"σ·ESW·탄성·gap 이 0건이라 행을 만들면 전부 `n/a` 로 채워져 표가 무의미해진다"*)는
>    이 편에 **절반만** 맞는다 — 이 리뷰에는 σ·ESW·탄성이 **많다**. 다만 **전부 재인용이고 전부 Na 값**이다.
> ② 그래서 진짜 이유는 **§K(수계 Zn) 와 같은 것**이다: *"⛔ 물성 4축과 **수치로** 섞지 않는다."*
>    A–D 표에 행을 만들면 **Na 숫자가 우리 Li 숫자 옆에 물리적으로 놓이고**, 6개월 뒤 누군가 그 표를 복사할 때
>    단서가 따라가지 않는다(우리 화면규율: *"근처에 ⛔ 표지를 두는 것은 결속이 아니다"*).
> ③ **대안 제안**: Na 계 논문이 2편 이상 들어오면 **`## M. 🧂 Na 계 축 — ⛔ 물성 4축과 수치로 섞지 않는다`** 를
>    §K 와 같은 양식으로 신설하는 것이 맞다. **지금은 1편뿐이라 절을 새로 파면 반쯤 빈 절이 된다** → J-7 블록으로 둔다.

**[Li26NaRev] `li2026_na_sulfide_halide_interface_review` — ⛔⛔ Na 계 리뷰 · 물성 4축 진입 금지 · 방법/프레임만**
(*Chem. Sci.* 2026 Accepted Manuscript, DOI 미발급 · Xidian+HUST · refs 147 · **자체 계산 0 · 자체 실험 0**)

> ⛔ **이 블록의 값은 전부 나트륨(Na) 값이고 전압은 vs Na⁺/Na 다.** 우리 comp1/modelc 와 **같은 표에 놓지 않는다**.
> 여기 있는 것은 *"그 양을 어떻게 정의하고 어떻게 재는가"* 뿐이다. 값 대조가 필요하면 **그 자체가 금지 신호다.**

| 항목 | [Li26NaRev] 가 쓰는 정의 | 우리 정의 | 판정 |
|---|---|---|---|
| 전압-상평형 staircase | `Na uptake per f.u.` vs `Voltage` + 전압구간별 상평형 (`Fig. 3a`·`8a`; ref 48 Ong / ref 94 Qie) | `get_element_profile` μ_Li 스캔 staircase | 🟢 **같은 양** — 축이 그대로 겹친다. ⛔ 값은 기준전극(vs Na⁺/Na)·hull 세대·제외상 정책이 달라 대조 불가 |
| 계면 반응에너지 | *"chemical compatibility as a screening criterion"* 로 산화물 버퍼층 선별 (`Fig. 10e`; **ref 48 = Tang/Ong 2018**) | `interface_reactivity` = pymatgen `InterfaceReactions` (Richards 2016 계보) | 🟢 **같은 양의 계보**(Ong 판 vs Ceder 판, 같은 구현). ⛔ **리뷰가 ΔE_D 수치를 하나도 인쇄하지 않는다** — 순서 정보만 |
| 2변수 화학퍼텐셜 상도 | **(μ_Na, μ_S) 2D 상도** (`Fig. 4a`; ref 73 Jalem) — μ_Na 와 μ_S 를 **둘 다 연다** | μ_Li **1변수**만 스캔(나머지는 hull 이 고정 = 폐쇄계) | 🟡 **우리에게 없는 양.** 틀린 게 아니라 **질문이 다르다** — S 가 교환되는 무대(Li–S 전환형 양극)에선 우리 2.256 V 가 μ_S 고정 하의 값임을 상기시킨다 → **질문으로만 전이** |
| MD 확산 + **음이온 동결 대조** | `D₈₀₀K` AIMD, **`Unrestricted Cl-motion` vs `Frozen Cl-motion` 두 계열**(`Fig. 6a`; ref 17 Wu/Ong) | UMA MLIP-MD, MSD 창 2–50 ps, 600/800/1000 K 3점 | ⭕ **이식 후보 (T1)** — 동결 대조 설계를 `tools/ionic` 플래그로. 보고량은 **비율** `D(frozen)/D(free)` (절대값 금지 규율 회피). ⛔ D 값 전이는 이온·온도·엔진 **삼중 불일치** |
| BVEL / BVSE | *"bond valence energy landscape"* 로 **경로 연결성** 판정 (`Fig. 6c`; ref 96) | `tools/comp1_v3` BVSE=(BVS−1)², softBV R₀ S 2.105/Cl 2.249/O 1.466, b=0.37, ~0.25 Å voxel, 채널%=above-min ≤ iso | 🟢 **같은 도구·같은 질문.** ⛔ 리뷰에 R₀·b·voxel·iso 가 없어 **정량 대조 불가** |
| 탄성 | DFT C_ij → **Voigt–Reuss–Hill** + K-means 군집, Na 이온전도체 ~40종 (`Fig. 8d`; **ref 46 Torii 2026**) | `E_VRH` (DFT elastic C_ij) + `B₀`(EOS BM3) | ⚠⚠ **후처리가 문자 그대로 같고 값 범위도 겹쳐서 제일 위험하다.** `NaTaCl₆` 15.31 · `Na₂ZrCl₆` 21.65 · `NaAlCl₄` 17.68 · `Na₃ErCl₆` 29.57 GPa ↔ 우리 22.06/27.66 GPa. **Na 염화물 vs Li 황화물이다.** 🟢 쓸 수 있는 최대치 = *"황화물·할라이드는 산화물(100–150 GPa)보다 한 자릿수 무르다"* 는 **정성 계열** |
| 산물 갭 → 부동태 판별 | `NaF` ≈11 eV = 자기부동태 / `Na₃P` ≈0.4 · `Na₃Sb` ≈0.68 eV = **MIEC 부식** | `sei_products` 갭: `LiCl` 6.65 ≫ `Li₂S` 3.90 · `Li₃P` = **`conductor-LEAK`, 0.70 eV** | 🟢 **규칙 전이 가능** (터널링 지수감쇠는 원소 무관). ★ **`Li₃P` 0.70 ↔ `Na₃P` ≈0.4 eV 가 같은 역할** = 이 편에서 가장 직접적인 대응. ⛔ 값은 각자 계산본 사용 |
| 계산 파라미터 | ⛔ **전편 0건** — functional·cut-off·k-mesh·supercell·무질서 처리·DFT+U 하나도 없다 | (우리는 전부 기록) | 🔴 **인용한 DFT 값의 비교가능성을 독자가 판정할 수 없다.** 이 리뷰를 통해 값을 인용하지 말고 **원출처로 내려가야 한다** |
| ASR 기준 | ⛔ **저자들이 "존재하지 않는다"고 명시** + *"보편적일 수 없다(면적용량·전류·온도·스택압·전압효율 의존)"* | 우리도 없다 (슬랩 W_ad 축은 2026-08-28 보류) | 🟢 **공백이 일치한다.** 저자들의 "보편적일 수 없다" 논거는 우리 **보고량 카드** 규율과 같은 사고 → `estimand_card.md` 작성 시 인용 가능 |

**🔴 이 편에서 발견한 것 중 우리 축 E(환원/음극)에 직접 걸리는 것**
`Fig. 9d`(ref 116, `Na₃MCl₆` 26종) 를 **직접 읽으면** 리뷰 본문의 *"할라이드는 음극에 더 나쁘다"* 가 **양이온 족에 따라 뒤집힌다** —
3족(`Sc`·`Lu`·`Y`) **0.55–0.75 V** · 란타나이드 6종 **0.50–0.55 V** 는 `Na₃PS₄` **1.15 V** 보다 **낮다**(= 더 버틴다).
3d TM(`Cr`·`V`) 2.10 V, 13/15족(`Al`·`In`·`Bi`) 1.50–2.25 V 만 더 높다. 리뷰는 이 족 간 분화를 **한 줄도 언급하지 않는다**.
⇒ 우리 §E 의 *"Cl-rich 유불리 문헌 충돌"* 은 **"열역학 onset" 과 "산물의 전자전도성" 이라는 서로 다른 축을 섞어서** 생긴다.
**환원 논의에도 축 명명이 필요하다** (산화 4축 규율의 환원판). ⛔ 단 위 V 값은 **figure-read · Na · vs Na⁺/Na** 라 인용 금지.

**⛔ 이 블록에서 인용하면 안 되는 것**: 모든 σ·Ea·전압창·탄성 GPa·D·산물갭·셀 성능값 · **특히**
*"우리 2.256 V ↔ `Na₃PS₄` 2.5 V"*, *"우리 1.242 V ↔ `Na₃PS₄` 1.2–1.5 V"*(우연 일치 — **부인을 선언**한다),
*"우리 E_VRH 22/27.7 GPa ↔ 할라이드 15–30 GPa"*, *"Cl-rich 가 산화한계를 3.8 V 로 올린다"*
(⛔⛔ 리뷰의 Cl 은 **골격**, 우리 Cl 은 **S 골격에 부분치환** — 끌어오면 우리 S²⁻-limited 판정을 스스로 부정한다).

**[Wang26LRM] `wang2026_lirich_mn_cathode_solid_state_review` — ⛔ 양극 리뷰 · 물성 4축 진입 금지 · *문턱·대조군 설계*만** (2026-09-13 신설)
(*Chem. Commun.* 2026 Review, DOI `10.1039/d6cc03421g` · 中国矿业大学(北京) · refs 132 · **자체 계산 0 · 자체 실험 0** · 크로핑 17장 중 8장 실독)

> ⛔⛔ **이 편의 주인공은 양극 `xLi₂MnO₃·(1−x)LiTMO₂` 다. 우리는 전해질 `Li₆PS₅Cl` 을 한다.**
> 31쪽 중 우리 축에 닿는 것은 **§3.2(황화물)·§3.3(할라이드)·§4(4대 난제)의 ≈8쪽뿐**이고,
> 나머지 23쪽(음이온 산화환원 4가설·ICE·전압감쇠·전압이력·O2/O3 적층·단결정화·탭밀도)은
> **우리 계에 대응 개념이 아예 없다** — 억지로 잇지 않았다 (digest §7f).
> 그리고 **자체 계산이 0건**이라 아래 "이 논문" 칸은 전부 **재인용(소환의 소환)** 이다.
> 여기 있는 것은 *"그 양을 어떻게 정의하고 무엇과 비교하는가"* 뿐이다.

| 항목 | [Wang26LRM] 가 쓰는 정의 | 우리 정의 | 판정 |
|---|---|---|---|
| **스크리닝 문턱** | `Fig. 15b`(ref 124) **4단 AND 게이트**: `E_hull = 0 meV/atom` → **`E_d ≤ 2.8 V & E_c ≥ 4.3 V`** → **`\|ΔE\| < 100 meV/atom`** → **`E_a < 0.5 eV`**. 통과율 **920 → 68 → 19 → 10** (7.4 %→2.1 %→1.1 %). ⚠ **문턱값은 전부 `figure-read`** — 본문에 하나도 없다 | 우리 4축: hull 게이트 없음 / 산화 onset **2.256 V**·환원 **1.242 V** / `interface_reactivity` comp1\|LCO **−322.7 meV/atom** / Ea **0.253·0.224 eV** | ⭕ **T1 이식 후보 — 우리 cascade 게이트 설계의 문헌 앵커.** litdb 에 *숫자 문턱이 박힌* 선례가 거의 없다. ⛔ **값 그대로 적용 금지**: 이 문턱은 **양극 코팅재** 기준이다(전해질인 우리 계는 `E_c` 2.256 < 4.3 과 `\|ΔE\|` 322.7 > 100 으로 2단·3단 탈락 — 당연하다) |
| **계면 반응성 측정** | `Fig. 9c`(ref 77) **Rietveld 상분율** — Ga-LLZO 를 **LRM(LNM) 과 NMC811 양쪽에** 700/800/900 °C 3 h 공소결. **LRM 쪽만** `La(Ni,Mn)O₃` **26–30 %** + `Li₂ZrO₃` **10 %**(900 °C), **NMC811 쪽은 단일 생성물 8–16 %**. 잔존 LLZO **35→22 %**(LRM) vs **25→26 %**(NMC811) | `InterfacialReactivity(use_hull_energy=True)` 계산 ΔE, comp1\|`LiCoO₂` **−0.3227 eV/atom** (산물 `Li₃PO₄`·`Li₂SO₄`·`Li₂S`·LiCl·`Co₉S₈`) | ⭕⭕ **T2 이식 후보 = 이 편 최대 소득.** 양(계산 ΔE vs 실측 wt%)은 다르지만 **질문이 같고**, 저쪽은 **대조 양극을 같이 걸어 상대화**한다. ⇒ **우리도 `Li₆PS₅Cl`\|LCO 를 `Li₆PS₅Cl`\|NMC 와 *쌍으로* 보고해야 "얼마나 나쁜가"가 선다** ([Xiao20Rev] `Fig. 5a` 가 이미 행렬이므로 칸만 채우면 된다). ⛔ wt% 값 이식 금지 |
| **열화 분류 어휘** | `Table 2` 하단 3행 — **기계 / 화학 / 전기화학** 열화를 족마다 **severe·moderate·mild** 로 배정 (산화물 = 기계 severe·나머지 mild / **황화물 = 화학·전기화학 둘 다 severe·기계 mild** / 할라이드 = 전부 moderate·기계 mild / 고분자 = 전기화학 severe) | 우리 축 B 는 **산화 안쪽 4분할**(①S²⁻ onset ②분해량/산물 ③계면 ④무질서) | ⭕ **T3 이식 — 직교라 충돌 없이 붙는다.** 우리 축 B 4분할은 전부 *"산화"* 내부 분할이고, 이건 *"열화의 종류"* 분할이다. ⇒ 우리 서술에 *"2.256 V 는 **전기화학 열화 축**의 개시이고, **화학 열화(ROS) 축은 우리 계산 밖**"* 을 한 줄 붙일 수 있다 |
| **우리 모델 밖 채널** | §3.2 마지막 + §4.2: **양극이 방출한 반응성 산소종(ROS)이 S²⁻ 를 화학적으로 산화** → `SO₄²⁻`·**`SO₃²⁻`**·`P₂Sₓ` (>4.4 V 생성, **2.0 V 방전 후에도 잔존 = 비가역**, ref 94 · `Fig. 13c` 실독 확인). + *"방전 하한이 충분히 낮지 않으면 절연 산물이 **비가역 축적**"*(ref 42) | 우리 grand-potential 은 **전압 하나만 변수**다. 산물 목록에 `Li₂SO₄` 는 있으나 **`SO₃²⁻` 는 없고**, **방전 하한 의존성은 아예 안 본다** | 🔴 **우리 계산의 경계를 명명해 준다 → §H 에 한 줄 값어치.** *"우리 ESW 는 양극발 ROS 를 반응물로 넣지 않는다 — 황화물 분해의 화학 채널이 빠져 있다."* ⛔ 단 **수치는 전부 재인용**이라 앵커로는 못 쓴다 |
| **도전재 판정 격자** | `Fig. 14f`(ref 68) — **전자경로/이온경로를 따로 채점**: Bare = 전자 ✗ / 이온 ✗ · **탄소 도입 = 전자 ✓ / 이온은 여전히 ✗**(사유도 동일하게 *"Interfacial electrochemical oxidation of SSE"* 로 인쇄). + §5.4 *"과량 도전탄소는 고전압에서 SE 분해를 심하게 유발"* | `papers/cho2024_conflicting_roles_conductive_additive.md` | ⭕ **같은 결론의 독립 도해.** *"도전재가 좋다/나쁘다"* 대신 **어느 경로에 좋고 어느 경로에 나쁜지**를 분리하는 **판정 양식**을 가져온다 |
| **효과 분해(factorial)** | `Fig. 14c`(ref 108) **1C 750 cyc 3곡선**: LATP@O3 **31.89 %** · **P-O2 무코팅 61.07 %**(⚠ **본문이 언급하지 않는 대조군**) · LATP@O2 **80.05 %** ⇒ 격자효과 **+48.2 %p** / 코팅효과 **+19.0 %p** | 우리 matched 2×2 factorial (`oxidation_matched_factorial.json` 11종) | ⭕ **설계 사고가 같다** — 두 레버를 교차시켜 각각의 기여를 분리. ⛔ % 값 이식 금지(양극 사이클 성능) |
| **"창(window)" 의 정의** | ⛔ **grand-potential 계산 0건.** `Table 2` 의 창 4칸(**wide / <3.0 V / >4.0 V / <4.5 V**)은 **ref 0건·방법 0건**. 유일하게 방법이 붙은 창은 `Fig. 12c` 의 **LSV 실측**(고분자)이고, 그 *"5.0 V"* 도 **전류 문턱을 안 밝힌다**(`figure-read`: PPS-PE 는 5.5 V 에서도 ≈0.04 mA cm⁻², PEO-PE 는 ≈4.4–4.5 V 부터 상승) | 우리 `get_element_profile` grand-potential — 정의·phase set·제외종까지 명시 | 🔴 **우리 축 B① 에 아무것도 못 준다.** 정의가 없는 문장은 확인이 못 된다 |
| **계산 파라미터** | ⛔ **전편 0건** — functional·cut-off·k-mesh·supercell·DFT+U·**무질서 처리** 하나도 없다. 특히 §2.1 이 **2상 vs 고용체 논쟁에 2쪽**을 쓰면서 **인용한 DFT 가 어떤 배열을 썼는지 한 줄도 없다** | 우리는 배열·k-mesh·functional 을 전부 기록 | 🔴 **재현 불가.** [Li26NaRev] 와 **같은 패턴**(리뷰가 계산 조건을 안 적는다) |

**🔴 이 블록에서 발견한 것 중 우리 축에 직접 걸리는 오류 2건**

1. **§4.3 공간전하층(SCL) — 부호가 틀렸고 자기 그림과도 어긋난다.**
   본문 첫 문장 *"**양극쪽** Li 화학퍼텐셜이 높아서 Li⁺ 가 **전해질 → 양극** 으로 이동하고 **전해질쪽이 고갈**된다"* 는 **부호가 반대**다(μ 가 높은 쪽에서 낮은 쪽으로 흐른다). 두 문단 뒤에는 *"**황화물 전해질**의 μ_Li 가 본질적으로 높아 구동력이 크다"* 로 **전제가 뒤집힌다**. 그리고 `Fig. 13e`(실독)는 **전해질 블록 안, 계면 근처에 Li-ion 이 빽빽하게 쌓인 그림**이라 본문의 *"전해질쪽 고갈"* 과도 반대다.
   정합적 물리는 **2번 전제 + 1번 결론**(황화물 μ_Li 높음 → Li⁺ 가 SE→양극 → **SE 쪽에 고갈층**)이다.
   ⇒ ⛔ **이 절을 우리 슬라이드·원고로 옮기면 부호 오류를 승계한다. SCL 인용은 원출처 ref 95(Nomura 2019 *Angew.*)로.** 우리도 SCL 축이 없어 남의 서술에 의존하는 자리라 특히 위험하다.

2. **산화물 창 ">6 V" 가 우리 원장과 정면 충돌.**
   §4.2: *"Oxide solid electrolytes possess an ultra-wide electrochemical stability window **exceeding 6 V**"* — **ref 없음**.
   우리 litdb: **[Xiao20Rev] `Fig. 6` LLZO = 0.09–2.97 V**, **[Zhu15] = 0.05–2.91 V** (둘 다 grand-potential).
   ⇒ **">6 V" 는 차단전극 CV 관행값이지 열역학 창이 아니다.** 산화물 칸이 이 지경이면 **같은 표의 황화물 칸(<3.0 V)도 같은 계보**이므로, `Table 2` 의 창은 **4칸 전부 인용 불가**로 처리한다.

**⛔ 이 블록에서 인용하면 안 되는 것 (전수)**
① **황화물 영률 ≈20 GPa** (+`Li₃YCl₆` **36.89** · `Li₃InCl₆` **18.24** · 산화물 100–200 — 전부 **중문 ref 99 하나**, 방법 미표기, 유효숫자 표기도 불일치) — ⚠⚠ **우리 E_VRH 22.06/27.66 GPa 와 우연히 붙어 보인다. 우연 일치는 면제가 아니라 부인 선언 대상.**
② **`Li₂MnO₃` gap 1.89 eV** (ref 43, functional 미표기) — **다른 물질**인데 우리 2.066/2.099 와 자릿수가 같다.
③ **`Li₆PS₅Cl` ≈2.5 V 산화분해**(ref 42) 를 축 B① **5번째 kinetic 데이터점으로 세는 것** — 방법 미표기 재인용이다. **원출처 `Du 2022 ACS Energy Lett. 7, 3006` 을 별도 digest 해야 센다.**
④ **계면저항 3722 Ω**(ref 93) — 면적·온도·셀 형상 미표기. 저항은 Ω cm² 없이는 무의미.
⑤ **부피변화 0.088 %**(LRM, 4.8 V) — LRM 치고 비정상적으로 작고 측정법 미표기. 게다가 §4.4 의 *"반복 부피변화가 균열을 만든다"* 서사와 긴장.
⑥ **`Table 1` 15행 셀 성능 전부 · `Table 2` 상단 6행(σ·창·온도·비용) 전부** — 전자는 조립·압력·면적용량 지배, 후자는 ref 0건.
⑦ **`Fig. 7c` σ 절대값** — 우리 규율상 σ 절대값 금지 + 재인용 + 측정법 미표기. **자릿수 간격만** 쓴다(LRM 10⁻⁸–10⁻⁵ ≪ SE ≈10⁻³ S cm⁻¹ ⇒ **복합양극 이온 병목은 SE 가 아니라 활물질 쪽**).
⑧ ⛔⛔ **"Cl-rich 가 산화에 강하다"를 이 리뷰로 뒷받침하는 것** — 리뷰의 Cl 은 **골격**(`Li₃InCl₆` 에 S 가 없다), 우리 Cl 은 **S 골격 부분치환**. 우리 VBM 은 Cl 을 1.0→1.6 으로 늘려도 **S 3p 이고 onset 은 2.256 V 로 불변**. 할라이드가 강한 이유는 **S 가 없어서**다.
⑨ **ICE·전압감쇠·전압이력·탭밀도·O2/O3** — 전부 **양극 고유 지표**, 전해질에 대응 개념 없음.

**📌 후속 (digest §11-1)**: 이 편이 가리키는 **원출처 2편을 직접 들여와야** 수치가 살아난다 —
**① ref 42 = W. Du *et al.*, *ACS Energy Lett.* 2022, 7, 3006** (`Li₆PS₅Cl` 2.5 V 가역 산화분해 + **2.3 V 아래 방전 환원** + `Fig. 7c` σ 원전) ·
**② ref 94 = Y. Yang *et al.*, *ACS Appl. Mater. Interfaces* 2023, 15, 30060** (S/P K-edge XAS — 우리 산물 목록의 실험 앵커, **`SO₃²⁻` 의 출처**).
차순위 **ref 83 = N. Hu *et al.*, *Adv. Energy Mater.* 2024, 14, 2303797** ("공간적 비동기 활성화" + LRM/VGCF/LPSCl 분산).



**[Wu26TMD] `wu2026_tmd_intercalation_engineering_review` — ⛔⛔ 층상 TMD 전극/촉매 리뷰 · 물성 4축 진입 금지 · **기각 기록**** (2026-09-22 신설)
(*Tungsten* 2026 in press, DOI `10.1007/s42864-026-00404-w` · 西北工业大 + IT4Innovations/VSB + 北航 + 西安交通大 + HKUST · refs 113 · **자체 계산 0 · 자체 실험 0**(저자 명시) · 크로핑 8장 중 **그림 6장 전수 실독**)

> ⛔⛔ **이 편은 §J-7 의 다른 항목과 성격이 다르다 — *방법 원전*도 *방법 반면교사*도 아니고, "우리 축이 아님" 을 근거와 함께 못 박은 기각 기록이다.**
> 무대는 **층상 vdW TMD**(MoS₂·WS₂·TaS₂·NbS₂·VS₂·NbSe₂·MoSe₂·MoTe₂·ZrTe₂·CrS₂·SnSe₂)에 게스트를 끼워 넣는
> **전극·전기촉매** 공학이다. 전해질이 아니고, 고체계면이 아니고, 열역학 안정성 창 얘기가 아니다.
> 전수 검색: `solid electrolyte` **0회** · `argyrodite` **0회** · `all-solid` **0회** · `NCM`/`LiCoO2` **0회** ·
> `hull` **0회** · `CoS2`/`NiS2`/`pyrite` **0회** · `VASP`/`PBE`/`k-point`/`cut-off` **0회**(DFT 는 12회 인용).
> 여기 두는 이유는 하나다 — **같은 PDF 가 다시 들어왔을 때 두 번 읽지 않기 위해서.**

| 1저자 지목 갈래 | 판정 | 근거 |
|---|---|---|
| ① TMD 가 황화물 → 우리 CEI 산물(`CoS₂` 3082 · `NiS₂` 3286 · `Co₉S₈` 342 · `Nd₂S₃` 81 …)의 전자구조 배경? | **❌ 기각** | 우리 산물은 **파이라이트(CoS₂·NiS₂) · 펜틀란다이트(Co₉S₈) · 히즐우다이트(Ni₃S₂) · 티오스피넬(Co₃S₄·Ni₃S₄) · 희토류황화물(Nd₂S₃·NdS₂)** = **전부 비층상 3D**. 이 리뷰의 TMD 는 **vdW 갭이 있는 층상**만. `Co₉S₈` 만 2회 나오는데 **MoS₂ 를 올려 키우는 받침대**로만 쓰이고 자체 전자구조 서술 0 ⇒ *"둘 다 금속 황화물"* 은 화학식 수준 동어반복 |
| ② intercalation(주입) ↔ 우리 §2b(SE 가 양극 TM 을 인산염으로 소모) 개념 대조? | **△ 한 줄만** | 접점은 ref [81] *"Na-MoS₂ 는 conversion 반응 ΔG 가 **더 높아** MoS₂→Mo+Na₂S 해리를 열역학적으로 억제"* **단 한 문장**. 형식은 우리 질문(*"도핑이 계면 열역학을 양성 산물 쪽으로 기울이나"*)과 같다. ⛔ **그러나 ΔG 수치·반응식·범함수 전부 없고**, 기구가 다르다 — 저쪽은 **단일상 자기분해**를 자리점유+전자공여로 막는 것, 우리는 **두 상 사이 화학퍼텐셜 부정합**이 구동하는 계면반응. **틀로만 유효, 인용은 원논문 [81] 직독 후에만** |
| ③ 게스트/도펀트 선택 규칙 ↔ 우리 3가 스크리닝? | **❌ 규칙이 없다** | 리뷰의 유일한 선택규칙 문장이 **부정문**이다: *"이온 원자가만으로 일반화해서는 안 된다 — 이온반경·배위환경·삽입농도·호스트격자에도 의존하므로."* 정량 서술자·문턱·깔때기 **0건**. ⚠ **3가는 ref [45] 의 6종 목록에 `Al³⁺` 로 한 번 나오고 결과가 안 적혀 있다** — 3가가 등장하는 유일한 자리에서 침묵. 우리 게이트(형성E→hull→ESW→수송)가 훨씬 엄격하다 |
| ④ 우리가 인용할 2차 출처? | **❌ 없음** | refs 113 중 **황화물 SE 0편 · 아지로다이트 0편 · ASSB 계면 0편 · 양극 코팅 0편**. 가장 일반적인 것이 층상삽입 총론 4편([8][9][10][17])인데 우리 원고 어느 문장에도 붙을 자리가 없다 (TMD 삽입 리뷰를 아지로다이트 CEI 논문에 달면 non-sequitur) |

**⛔ 4축 표에 못 넣는 이유 — 행별로**

| 축 | 이 편이 가진 것 | 왜 못 넣나 |
|---|---|---|
| A 이온전도 | **전자전도도** 6.83×10⁴ S cm⁻¹(Ge₀.₃₃NbS₂) · 110 S cm⁻¹(탈용매화 Fe-WS₂) | **이온 σ 가 아니다.** 같은 표에 놓으면 복사될 때 단서가 안 따라간다 |
| A 이온전도 | 캐리어 활성화E **18 meV** | **전자 캐리어**의 활성화E. 우리 Li⁺ Ea 0.224–0.253 eV 와 자릿수가 10× 다르고 **다른 양**이다 |
| A 이온전도 | Zn²⁺ 확산장벽 **0.23 eV**(MoSe₂-IL) | ⚠⚠ **우리 modelc Ea 0.224 eV 와 우연히 붙어 보인다 — 우연 일치는 면제가 아니라 부인 선언 대상.** 캐리어(Zn²⁺≠Li⁺)·호스트(층상 vdW≠3D 골격)·방법(미표기≠UMA MLIP-MD) 셋 다 다르다 |
| B 산화안정 | **없음** — grand-potential 0건, LSV 0건, 안정성 창 논의 자체가 없다 | 대응 개념 부재 |
| C 기계 | **없음** — 탄성상수·모듈러스 0회 | 〃 |
| D 전자구조 | Ga-MX₂ `figure-read ≈`**1.6 eV** 직접전이(`Fig. 3b`) | functional 미표기 + 물질이 다르다(few-layer MX₂). ⛔ *"둘 다 wide-gap"* 조차 못 쓴다 — **삽입 후 금속이 된다** |

**🔧 그래도 기록할 가치가 있는 것 2건 (값 이식 아님)**

1. **`Fig. 3c` — "얼마나" 가 아니라 "어떻게 배치됐나"가 물성을 가른다.**
   같은 게스트 농도에서 **용매화 / 탈용매화 / 표면근방 농축** 3배치가 1T′-WS₂ 전도도를 가른다(탈용매화가 110 S cm⁻¹ 로 최고).
   ⇒ 우리가 아지로다이트 S/Cl **무질서 배열**마다 gap 이 ±0.2–0.3 eV 흔들린다고 경계해 온 것과 **정신이 같다**.
   **외부 방증일 뿐 수치 이식 아님.** 그리고 이 편엔 배열을 다루는 **방법이 0**(SQS·enumerate·cluster expansion 0회)이다 —
   §3.1 이 `Fe_xNbSe₂` 게스트 규칙화 문턱(x=0.14 무질서 → 0.19·0.23 `2a₀×2a₀` 규칙, `Fig. 2b`)을 논하면서도 전부 실험 관측 재인용이다.

2. **리뷰가 계산조건을 안 적는 병증의 *세 번째이자 최악* 표본.**
   [Li26NaRev]·[Wang26LRM] 에 이어 세 번째인데, 앞의 둘은 최소한 계 이름과 대조군은 붙어 있었다.
   이 편은 **코드·범함수·vdW 보정·k-mesh·슬랩·전하분할 전부 0** 이다.
   특히 **층상 vdW 물질 리뷰인데 vdW 보정 언급이 0회**이고, 전하이동 `0.7 e⁻`(CoCp₂→WS₂)를 인용하면서
   **어떤 전하분할(Bader/Mulliken/Hirshfeld/Löwdin)인지 안 밝힌다** — 분할마다 값이 배로 갈리는 양이다.
   ⇒ 우리 원고·SI 의 "계산조건 전량 기재" 관행의 **대조 표본**.

**🔴 그림을 실제로 봐서 잡은 결함 3건** (digest §10)

① **`Fig. 4b` 범례 "600 cycles" vs 본문 "6000 사이클" — 10× 불일치.** 이 사이클 수는 **인용 금지**.
② **`Fig. 5b`·`Fig. 5d` 는 본문 주장을 뒷받침하지 못한다.** 본문은 이 두 패널을 근거로 *"확산 에너지장벽이 현저히 감소"*([81]) ·
   *"계산된 확산장벽을 낮췄다"*([90]) 라고 쓰는데, **두 패널 다 경로 기하만 있고 에너지 축이 없다.** 장벽 수치는 본문·표·그림 어디에도 없다
   ⇒ *"삽입이 확산장벽을 낮춘다"* 를 이 리뷰로 인용하면 **근거 없는 주장을 승계**한다.
③ **`Fig. 5c` 서술이 그림보다 관대하다.** 본문 *"VS₂-NS 는 거의 변하지 않았다"* vs `figure-read` ≈1900 → ≈2900 Ω (오히려 악화 쪽).

**⛔ 이 블록에서 인용하면 안 되는 것 (전수)**
① **`Table 2` 1행 `1526 mAh g⁻¹`**(Mg²⁺-1T-MoS₂ LIB) — MoS₂ 4전자 conversion 이론용량 **≈670** 의 **2.3 배**. 본문조차 이 값을 안 든다.
② **본문↔`Table 2` 불일치 3건** — [37] `1049.8@3C/1000cyc 853.03` vs 표 `916.73/500cyc@1C` · [97] `1 A g⁻¹ 400cyc` vs 표 `0.1 A g⁻¹ 100cyc` ·
   **[35] `126` vs 표 `122`@5 A g⁻¹ (같은 조건인데 값이 다르다)**.
③ **`Table 1` 함량 `3.23 at%` 가 MoS₂/MnP 와 TaS₂/Pd 두 계에 중복** — 전사 오류 의심.
④ **`Table 1` 을 계 간 순위표로 읽는 것** — `Pd₀.₁TaS₂` 는 본문에서 최고 사례로 격찬받는데 표에서 **과전압이 가장 나쁘다(241 mV)**.
   각 행의 비교 대상이 *같은 논문 안의 대조군*이라 행끼리 비교가 성립하지 않는데 **표에 그 경고가 없다**.
⑤ **`Fig. 3e` 의 `T_c ~3.8 K`** — 저항 onset 값이다. 같은 그림의 반자성 삽입도는 `figure-read ≈`**2.5 K** ⇒ **리뷰의 선택적 인용**.
⑥ **ΔG_H* · 흡착E · 전하이동 · 확산장벽 전부** — 코드·범함수·vdW·참조상태 미표기라 **조건 없이 인용 불가**.
⑦ ⛔⛔ **"층상 황화물이니 우리 CEI 황화물 산물과 같은 계열" 이라고 쓰는 것** — 구조군이 다르다(위 ①행).

**📌 후속 — 지금은 아니다.** 우리 축이 **고체 Li–S 로 확장되거나** conversion ΔG 틀을 실제로 쓰려 할 때만 원출처를 꺼낸다:
**ref [81]**(Cen, Na-MoS₂ conversion ΔG 억제) · **ref [37]**(Wang, `Fig. 6c` Li₂S 분해장벽 원전 — `figure-read ≈`**0.87**(2H) vs **0.40/0.45 eV**(1T′)) ·
**ref [106]**(Liu, Fe-MoS₂-C, Li₂S 석출 883 s·110.2 mAh g⁻¹) · **ref [107]**(Jin, Zn-MoS₂, Li₂S/Li₂S₄/Li₂S₆ 흡착E −3.480/−2.260/−1.313 eV).
⛔ **넷 다 액체전해질 Li–S 이고 호스트가 MoS₂ 다** — 우리 고체 LPSCl 축에 값을 그대로 옮길 수 없다.


> 📎 **2026-09-13 병합 이하 21 항목** — 2026-09-09 큐레이터 8개 동시 실행분의 `_pending_index_*.md` ②③ 블록을 조율 세션이 옮겼다. 항목 순서는 슬러그 알파벳순이지 중요도가 아니다.


**[Alg26FT] `alghamdi2026_finetuning_strategies_li_diffusion_mace` — "fine-tune 이 D 를 실제로 개선하나"의 정량 원본 (코드 실물 확보)**
(⛔ 물성값은 **LiF** 침입형 Li 의 D·Ea 뿐. A–D 4축 행 금지. 아래는 **판정**과 **우리 위치**뿐이다.
⚠ 전부 **소환값** — MACE·LiF·300–500 K 의 값이다. 우리 UMA·LPSCl 수치와 섞지 않는다.)

| 항목 | [Alg26FT] 가 보이는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| **파운데이션 모델을 그대로 쓸 때 D** | **450 K −49 % · 500 K −42 %** (기준=DeePMD 4만점) | **UMA-s-1p1 고정, fine-tune 없음** | 🔴 **우리가 정확히 그 자리에 있다.** ⇒ **우리 D 절대값은 배(倍) 단위 계통불확실도를 안는다** ⚠ 다른 모델·다른 물질이므로 *"우리도 2배 틀린다"* 로 옮겨 쓰지 말 것 |
| **같은 상황의 Ea** | **0.22 vs 0.24 eV (−0.02, 8 %)** — 오차막대와 겹침 | modelc **0.224 eV** (단일 궤적) / 3-seed **0.197±0.032** | 🔴 **"Ea 가 잘 맞으니 모델이 좋다"가 깨진다.** Ea 8 % 안에 들면서 D 는 2배 틀린 실측 사례 |
| **오차가 실리는 자리** | **D₀** — 두 MACE 모델 모두 기준의 **정확히 1/3**. 장벽항이 반대로 1.7–2.8배 ⇒ **상쇄** (digest 계산) | — | 🔵 **D₀ 계통오차는 같은 모델 분자/분모에서 상쇄될 여지가 있다** = 우리 `D_rel` 에 유리한 유일한 정황 |
| **★ 비(ratio) 둔감성** | ⛔ **대조 자체가 없다.** 계가 끝까지 LiF 하나 — host/design 쌍 부재 | 보고량 `D_rel(design,host)` @600 K (비준) | ⚠ **지지도 반박도 없음.** 우리가 직접 시험해야 한다. **비관 요인**: 기준 대비 비가 300 K 1.57 → 500 K 0.84 로 **1.9배 움직이고 423 K 에서 부호가 바뀐다** ⇒ **D_rel 이 자동으로 안전하지 않다** |
| **fine-tune 이 D 를 바꾸는 폭** | **1.26–2.17배** (온도 의존, digest 계산). 전략까지 바꾸면 같은 물질에서 **≈6배** | — | 🔴 **"MACE 계열"이라는 이름만으로 D 를 인용하면 5배가 흔들린다.** 우리 **σ 절대값 비인용 규율의 외부 근거** |
| **아키텍처 이식성** | MACE (equivariant MPNN, r_max 6.0 · L=1 · 128 ch) | **UMA-s-1p1 (omat)** | ⚠ **경계 명확히**: 데이터 전략 결론(조성 > 양, 리플레이 수확체감, 라벨 150–300점)은 **아키텍처 무관하게 이식 가능**. **수치(49 %·1/3 D₀·423 K)는 이식 불가** |
| **omat 계열 단서** | 본문 한 줄: **MACE-OMAT-0 이 기준 D 에 더 가깝다** (비평형 구조 多) | 우리 체크포인트가 **omat** | 🟢 **우리에게 유리한 유일한 단서.** ⛔ 그러나 **수치가 `Fig. S7`(SI)에만 있고 우리는 SI 미확보** ⇒ **정량 인용 불가, "그런 보고가 있다"까지** |
| **thermostat** | **Nosé–Hoover τ=0.1 ps** | **Langevin τ≈0.51 ps** | 🔴 **여기서 우리가 진다.** [Mag19] §4.1.1 기준 NH 는 **속도 스케일링 계열 = 0.1–10 ps 전 범위 안전**, Langevin 은 **속도 무작위화 계열 = τ 0.1–1 ps 에서 D 를 극적으로 낮춤**. ⛔ *"저들 τ 가 0.1 ps 라 위험"* 은 **틀린 비판** |
| **MSD 창 규율** | **없다.** 논문·repo 어디에도 창·시간원점·절편 규약이 없다 (`compute msd` 0건, 분석 코드 0개) | **2–50 ps 고정 · 자유절편 OLS** | ✅ **우리가 낫다.** ⛔ 그래서 **`Table 3` 의 ± 를 우리 ± 와 같은 등급으로 나란히 놓지 마라** |
| **복제의 성격** | **서로 다른 초기구조** (NH 결정론적, `velocity create` 없음 — repo 실측) | **Langevin 난수 시드 3** | 🔵 **다른 것을 재고 있다.** 초기조건 앙상블 vs 열욕 난수 앙상블. 둘 다 필요 |
| **궤적 길이** | **3–9 ns × 2–4 복제** | **200 ps × 3 시드** | ⚠ **직접 비교 금지.** 저쪽은 1001원자에 **이동 이온 1개**(희박 결함), 우리는 Li 수십 개. [McC25D] 기준 유효통계 = 입자수 × 창수라 원자 수가 상당 부분 벌충 |
| **라벨 예산 (우리가 하려면)** | FT1 **156** / FT2 **144** 구조 + **동수 검증셋** ⇒ **DFT 288–312회**. 학습 4.5 h(A100×8, 1800점) / 6 s per epoch(300점) | 0 | 🔵 **견적이 나왔다.** ⚠ 경로 A(남의 DeePMD 데이터 재사용, 새 DFT 0회)는 **우리 계에 해당 공개 데이터가 없어 불가** → **경로 B 뿐** |
| **데이터 설계 원칙** | **조성 > 양**: 침입형 700 동일, **bulk 10 → 100 만으로** 기준의 1.5–3.8배 → 일치. bulk 부족 시 **리플레이 10,000점도 무효** | — | 🟢 **이식 가능한 결론.** 우리가 fine-tune 한다면 **"host bulk 구조를 충분히 넣어라"** 가 첫 규칙 |
| **망각 대책** | **multi-head + MPtrj 리플레이**(원소 85종 범용 — repo 실측). pt 100–1000 이 최적, **10000 에서 후퇴** | 해당 없음 (fine-tune 안 함) | 🔵 **하게 되면 pt≈1000 에서 시작.** ⚠ 논문은 망각을 **D 하나로만** 측정 — 원 도메인 성능 미측정이라 **정칙화와 구분 안 됨** |
| **Haven** | knock-off 로 **전하변위 = 원자변위 2배** → **H_r ≠ 1 인정하고 계산은 미룸** | **NE, Haven=1 가정 · σ 절대값 비인용** | ✅ **우리 규율이 옳다는 또 하나의 외부 근거.** LPSCl 도 협동 뜀 계 ([Jeon26]·[Ish25]) |
| **긴 궤적 안정성 검증** | 3–9 ns 에서 **에너지 드리프트·불안정 없음**을 명시 검사 | b2o3 **골격 creep** 로 MD 전도도 축 마감 | 🔵 **같은 종류의 검사.** 우리가 200 ps 에서 잡은 것을 저들은 9 ns 에서 확인 |

**⛔ 이 논문에서 인용하면 안 되는 것 (요약)**
1. `Fig. 2` **범례의 D₀·부호** — 오류 2건 확정. `Table 3` 만.
2. *"fine-tuning 이 D 를 DFT 에 가깝게 만든다"* — **D 의 DFT 기준값이 이 논문에 없다.**
3. *"fine-tuning 이 D 를 개선한다"* 를 **온도 단서 없이** — 300–350 K 에서는 악화된다.
4. *"이 논문이 힘 MAE–D 해리를 보고했다"* — 힘 MAE 를 **하나도 보고하지 않았다.**
5. `Fig. 3` 의 **미세한 순위차**(pt=1000 vs 10000 등) — 복제 2개, 상대오차 ~50 %.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_alghamdi2026_finetuning_strategies_li_diffusion_mace.md` ## ② .</sub>


**[Carrete23UQ] `carrete2023_deep_ensembles_vs_committees` — 불확실도 추정기의 정의 원본 + 우리에게 없는 양의 이름**

> ⛔ **σ·Ea·D·ESW·탄성·gap 이 0건**이다. 여기 있는 것은 **우리가 "불확실도"라고 부르는 것이 무엇인지**를 정의하는 원본이다.

| 항목 | [Carrete23UQ] | 우리 | 판정 |
|---|---|---|---|
| 불확실도의 층위 | **모델 앙상블 분산** (committee 10 / bootstrap 10 / deep ensemble 10) | **단일 모델(UMA-s-1p1) · 멀티시드 MD 3-seed** | 🔴 **다른 양이다.** 우리 `Ea 0.197 ± 0.032 eV`(modelc 600 K 3-seed) 의 ±0.032 는 **열적 샘플링 산포**이고 [Carrete23UQ] 의 σ 는 **epistemic(모델) 분산**이다. ⇒ **우리에겐 epistemic 불확실도 추정치가 아예 없다** — 이 문장을 축 J 에 명시적으로 박아 둔다 |
| 힘 불확실도를 얻는 법 | ① 앙상블 멤버들의 힘 분산 ② 전용 σ²_f 헤드 | 없음 | **Appendix 가 지름길이 없음을 증명**: `σ²_f = ∂²⟨δE(X)δE(Y)⟩/∂X∂Y|_{X=Y}` — **두 점 공분산**이 필요한데 set-pooling 구조는 한 점만 낸다. ⇒ 우리가 σ_f 를 원하면 **committee 를 만드는 길뿐** |
| 가장 싼 실행안 | — | **UMA 체크포인트 복수(1.1 / 1.2 / 크기 다른 것)를 committee 로 묶어 같은 구조의 힘 분산 측정** | ⭕ **이식 후보 (T1)** — **DFT 0회 · 추가 학습 0회**. `uma2026` digest §⑥ 의 *"1.2 를 committee 멤버로 추가"* 와 같은 방향이고 **이 논문이 그 형식의 원전** |
| 전역 힘 불확실도 집계 | `σ_f = √(n⁻¹ Σ_atoms σ²_f)` — **RMS 집계**. 최댓값·softmax·90 백분위수를 전부 시험했으나 **이긴 사례 없음** | 해당 없음 | ⭕ **정의 채택 후보** — 우리가 committee 를 만들면 이 집계식을 그대로 쓴다 (최댓값 쓰지 않기) |
| 공간분해 진단 | **층별 오차/불확실도 violin**(`Fig. 10`) — 표면↔중심 **6 자릿수** 스팬 | 셀 전체 평균만 | ⭕ **이식 후보 (T2)** — 계면 슬랩에서 "MLIP 가 어느 층에서 틀리나". ⚠ **원자 단위로는 못 짚는다**(`Fig. 11`: 오차 최악 원자 ≠ 불확실도 최악 원자) |
| 능동학습 획득함수 | `L_adv = σ²_f · exp(−E_pot/k_BT)`, T=500 K, **Powell 국소 최대화**, 초기 Gaussian 변위 σ=0.1 Å | Stage 00–12 **순차 게이트**(싼 것 먼저) | 🔶 **다른 형식** — 탐색×타당성을 **곱 하나**로. §J-10 이 비판한 가중합 스칼라의 대안. ⚠ **국소 최적화라 전역 탐색을 대체 못 한다**(2회차 수확체감 — 출발점 다양성 필수) |
| rattle 데이터 생성 | 질량가중 Gaussian, θ_D = 418.5 K, T = 500 / 1000 K | 해당 없음 | ⭕ **처방 채택 시 주의**: **논문 인쇄식 `분산 = 3T/(k_Bθ_D)` 는 차원 불성립**. 실제로 쓰인 것은 **`⟨u²⟩ = 3ħ²T/(m k_Bθ_D²)`** (digest 재계산으로 0.5 % 확인). **논문 식을 그대로 코딩하면 안 된다** |
| 참조 DFT 등급 | **GPAW LCAO, PBE, Γ-only** | QE, PBE, PAW, k-mesh 수렴 | ⚠ **우리 기준으로 성긴 참조.** 이 논문의 "DFT ground truth" 를 우리 정본과 같은 등급으로 놓지 않는다 |
| MD 열욕 | **Nosé–Hoover chain(5)**, τ=100 fs, Δt **1 fs**, 298 K, 80 ps | **Langevin**, friction 0.02, Δt **2 fs**, equilib 5 ps / prod 200 ps | ⚠ 결정론적 chain ↔ 확률적 Langevin. **80 ps 내내 σ 가 단조 증가**(=평형이 아니라 탐색 지속)라는 관찰이 **우리 5 ps 평형화를 다시 보게 만든다** — 단 이건 **가설이지 판정이 아니다**(계·열욕·온도 전부 다름). 확인은 무료: 우리 궤적에 골격 MSD/σ 시계열 |

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_carrete2023_deep_ensembles_vs_committees.md` ### 2-b..</sub>


**[Chang26Sel] `chang2026_performance_based_mlip_selection_sse` — *어떤 사전학습 MLIP 를 골라야 하나* 의 argyrodite 실측**
(*Chem. Mater.* **2026**, 38, 3133–3144 · DOI 10.1021/acs.chemmater.5c02352 · **Solid Power Operating Inc.** 3인 ·
⛔ 코드·데이터 미공개 · **물성값 인용 불가**)

> 🔑 **이 편에서 가져오는 것은 값이 아니라 "판정축"이다.**
> 그리고 그 판정축이 **우리 UMA 선택을 부분적으로 방어해 준다** — 다만 **UMA 자체는 이 논문에 없다.**

| 항목 | [Chang26Sel] | 우리 (UMA-s-1p1 omat) | 판정 |
|---|---|---|---|
| **피고 목록** | EqV2(direct) · DPA3(cons.) · ORB v2(direct) · **SevenNet-l3i5(cons.)** · MACE(cons.) | **UMA-s-1p1** | ⛔ **UMA 없음.** 가장 가까운 `eqV2 S DeNS` 도 **MPtrj + direct** ⇒ 우리와 양쪽이 다르다 |
| **사전학습 코퍼스** | **전부 MPtrj** (ORB v2 만 +Alexandria) | **OMat24** | ⚠ `wang2025` 때와 **같은 세대 문제**. OMat24 가 MPtrj softening 을 개선했다는 우리 기록(`db/external/omat24/README.md`)이 있으므로 **결론 직수입 금지** |
| **★ 참조 범함수** | **PBE** (VASP 520 eV, MP 설정) | DFT 정본 **PBE**(QE/USPP) / MLIP 벤치 라벨 **PBEsol**(PET-MAD) | 🟡 DFT 축은 같은 계열이라 **정성** 비교 가능 · 🔴 **MLIP 벤치는 라벨이 달라 수치 비교 불가** |
| **★★ 1차 판정축 = 힘의 보존성** | 비보존(ORB v2·EqV2) → 1100 K 10 ps **+425 / +590 meV/atom 드리프트** (`Fig. S3`, `figure-read ≈`) · 보존(SevenNet·DPA3) → **≈0** | **UMA-S = 보존적**, NVE ✓ (`uma2026…` Table 1/4/16) + 우리 **유한차분 프로브 0.198% @ δ=0.005** | ⭕⭕ **우리가 합격 쪽이다.** *"우리는 이 논문이 탈락시킨 범주가 아니다"* 는 **정당한 방어** |
| **정적 지표의 변별력** | ⛔ **없다.** 5모델 전부 MAE < 10 meV/atom | 우리 J-1 = 힘 MAE 30.0 meV/Å | ⚠ **"MAE 가 낮으니 안전" 논증은 이 논문이 직접 부정한다.** 우리 J-1 도 같은 한계를 이미 적어 놨다(장벽·응력 미측정) |
| **평가설계** | **거친 Li₇PS₆ 프로토타입 → 전이완 → 채점**. 이완된 MP 구조로 채점하면 리더보드 재현일 뿐 | 우리 벤치는 **주어진 구조에 단일점 힘/에너지** | ⭕ **이식할 가치 있음** — 우리 벤치에 없는 축 |
| **MD 온도창** | **700 / 900 / 1100 / 1300 K**, 300 K 는 **외삽** | **600 / 800 / 1000 K** | 🟡 우리가 더 낮다 = caging 위험이 더 크다 |
| **★★ MSD 피팅 창** | **τ > 100 ps**. 근거 = `Fig. S1b` 에서 **700 K 완전정렬 배열이 τ≈10–70 ps 에 평탄부** | **2–50 ps 고정** | 🔴 **정면 충돌.** 단 그쪽은 **가장 느린 배열**이고 우리 modelc 는 빠르다 ⇒ **"확인할 것"이지 "이미 틀린 것"이 아니다.** **comp1 600 K 가 최고 위험 조합** |
| σ 산출 | pymatgen NE, **Haven = 1** (우리 역산 2% 이내 확인) | NE, Haven=1 | ⭕ **동일** |
| 시드·오차막대 | **시드 1** · MSD 의 x,y,z **3성분 SEM**(독립표본 아님) | modelc 600 K **3-시드** (Ea 0.197±0.032) | ⭕ **우리가 낫다.** `mccluskey2025`·`pranami2015`·`maginn2019` 가 3성분 SEM 의 과소평가를 지적 |
| **자리무질서(4a/4c) DFT 정답** | `Table 3` ΔE meV/atom: **100%4a = 0** · 75% = **3.28** · 50% = 24.73/27.52 · 25% = 22.48 · **0%4a = 39.72** | ⛔ **우리는 안 쟀다** | 🔴 **A1 — DFT 0회로 UMA 를 채점할 수 있는 외부 정답** |
| **추론 비용** (52원자, 1100 K) | ORB v2 462 ATS / SevenNet 117 / DPA3 80 / EqV2 51 atom-steps/s ⇒ **ORB v2 가 SevenNet 의 4.0배** | — | ⚠ 이 논문은 **4배 느린 쪽을 물리적 일관성 때문에 골랐다.** 하드웨어 미기재라 절대값 인용 금지 |
| **학습 범함수 ↔ σ** | ref 53(r2SCAN 학습 SevenNet) **~5 mS/cm** vs ref 52(PBE 학습 같은 아키텍처) **~44 mS/cm @350 K** | 우리 규율: **σ 절대값 인용 금지** | ⭕⭕ **우리 `mlip_committee.py` 규율의 독립 재확인** |

**⛔ 이 편에서 인용하면 안 되는 것**
1. **`14.67 mS/cm` 앙상블 평균** 및 *"실험 ~5 mS/cm 와 3배 이내"* — **Boltzmann 가중이 per-atom** 이다.
   우리 재현: per-atom → **14.666**(정확 일치) · 셀당(×52) → **0.065 mS/cm**. **225배.**
2. **`Table 3` 의 Ea 를 meV 단위로** — **eV 다** (`Fig. 3b` 인쇄값 0.41 ± 0.02 eV 가 증거).
3. **σ·D 절대값 전부** (PBE 편향 + 700 K→300 K 외삽 + 단일시드).
4. *"모든 MLIP 이 10 meV/atom 안"* 을 **UMA 로 확장** — UMA 는 시험되지 않았다.
5. *"MACE 는 argyrodite 부적합"* — **MACE 는 MD 시험을 안 받았다**.
6. **`Fig. 1a`/`Fig. S2a` 의 표본수 209/206** — 실제 158(`Table 1`) / 282(`Table S4`).
7. **`Fig. 3a` 의 절대 세로 오프셋** — 참조보정이 없어 해석 불가(우리 `bench_against_dft.py` docstring 참조).

**⇒ 우리가 지금 할 수 있는 것 (전부 DFT 0회)**

| # | 할 것 | 근거 | 비용 |
|---|---|---|---|
| **A1** | UMA 로 `Table 3` 6배열 ΔE 재현 → **UMA 가 Cl 4a 선호를 맞추나** | 논문 DFT 값이 인쇄돼 있다 | UMA relax 6회 |
| **A2** | UMA NVT 10 ps @1100 K, Li₆PS₅Cl 52원자 **총에너지 드리프트** | `Fig. S3` 와 직접 겹치는 시험 | 낮음 |
| **A3** | 기존 궤적으로 **log-log MSD** → 2–50 ps 가 확산영역인지 | `Fig. S1b` 가 제기한 유일한 실질 위협 | **재분석만** |

⛔ **A1–A3 는 기존 도구 확장으로 한다**(`tools/mlip/bench_against_dft.py` · `tools/ionic/`) — 새 파일 금지(코드 규율).
⛔ **A5(6배열 UMA-MD σ 비율) 같은 새 물리량은 `kb/templates/estimand_card.md` 를 먼저 채운다.**

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_chang2026_performance_based_mlip_selection_sse.md` ## ③ .</sub>


**[dK18MD] `deklerk2018_diffusion_analysis_md_beta_li3ps4` — 우리 `σ = NE(H_R=1)` 이 *무엇을 버리는가*를 이름 붙여 주는 원본**

> ⛔ **물성값은 있으나 β-Li₃PS₄(Pnma) 값이다.** argyrodite 4축에 수치로 넣지 않는다.
> ⛔ **이 편은 H_R 을 정량하지 않는다.** 여기 있는 것은 *"H_R=1 이 무엇을 가정하는 것인지"* 와 *"그 가정이 나쁠 이유의 간접 증거"* 다.
> ⛔ **`f = D*/D_J` 를 Haven 비로 옮겨 적으면 틀린 인용이다** — Murch 표준표기로 `H_R = f / f_I` 이고, 이 논문 `Fig. 9` 가 바로 `f_I ≠ 1`(집단성 30–80 %)이라고 말한다.

| 항목 | [dK18MD] | 우리 | 판정 |
|---|---|---|---|
| **σ 환산 가정** | eq 2 + *"assuming that the Haven ratio is equal to one"* + 출처(Marcolongo–Marzari 2017) | 같은 가정, **문장·출처 없음** | ✅ **형식으로는 살아남는다.** 이 편을 **선언 선례**로 달 수 있다. ⛔ 정량 정당화로는 못 쓴다 |
| **charge(집단) D_σ** | ⛔ **계산 안 함.** 식도 없다 | ⛔ 계산 안 함 | ⛔ **양쪽 다 구멍.** 채우려면 우리가 `⟨\|Σ_i Δr_i\|²⟩/(2dNt)` 를 돌려야 한다 (비용은 D\* 와 동일, **비싼 것은 통계**) |
| **상관인자 f = D\*/D_J** | 정의(eq 7)만, **β-Li₃PS₄ 값 미보고** | 없음 | 🟡 **형제편 [dK16Arg] 에 우리 물질계 실측이 있다: Li₆PS₅Cl 600 K σ\*/σ_J = 1.01/4.66 → f ≈ 0.22.** 우리도 낼 수 있다(홉 계수 확장) |
| **집단성 정량** | `Fig. 9` 450 K 6–24 % / **600 K 30–55 %** / 750 K 65–80 % (figure-read). ⚠ 정의(4.5 Å, 1/ν\*) 의존 — 저자 스스로 경고 | 없음 | ✅ **가져온다 (조건부 인용).** 우리 운영온도에서 교차항 무시가 나쁘다는 **간접** 근거. ⛔ 부호·배율은 못 준다 |
| **D 추정량** | **전 궤적 단일점** MSD(t_tot)/(2dt_tot), 원점강제 | **2–50 ps 창 자유절편 OLS** | ⛔ **다른 양이다.** digest 계산: 같은 600 K 궤적에서 **≈1.7배** 차이(3.2e-6 vs 1.9e-6). **한 표에 병치 금지**, 병치해야 하면 열 이름에 추정량을 적는다 |
| **확산영역 게이트** | 문장 1줄(*"displacement significantly larger than the vibration amplitude"*), **수치·적용 0** | `D_inc` plateau + 창 안정성 + 홉 수, `MSD_MIN_A2 = 3.0 Å²` | ✅ **우리가 더 엄격하고, 저자 데이터가 우리 게이트에 걸린다** (450 K β-Li₃PS₄ 총 MSD ≈ 3.3 Å², 면간 점프 0건) |
| **방향분해 MSD** | ✅ `Fig. S1` (1계·1온도). **a·c 는 ~230 ps 뒤 완전 평평**, 총 96 Å² 중 **33 %가 죽은 방향** | ⛔ 총 MSD 만 | ⛔ **우리가 진다.** 표준 출력에 넣을 것 (비용 0) |
| **골격 진단** | ⛔ **0건.** 종별 MSD 없음 · COM/drift 언급만 · 750 K "Li 부격자 melting" 을 알면서 게이트로 안 씀 | ✅ `--framework` β(경보) + b2o3 마감 선례 | ✅ **우리가 압도적으로 앞선다.** 이 논문에는 b2o3 를 잡을 장치가 하나도 없다 |
| **Ea 의 온도의존** | ✅ **정량**(`Fig. S4`·`S5`): Li₃PS₄ 4b–4c **0.240→0.185→0.124 eV(−48 %)** · **Li 공공 조성만 율속 장벽 평평**(0.286/0.290/0.295) | 600/800/1000 K **3점 아레니우스 단일 Ea** | ⛔ **우리 방식이 이 논문 §2.5 에 정면 비판당한다.** ⇒ `modelc 0.197 ± 0.032 eV` 는 **"600–1000 K 구간의 유효 Ea"** 로만 서술. ★ 부수 판정: **Ea 의 온도의존 자체는 이상한 게 아니다** — b2o3 를 죽인 것은 구간 Ea 비단조가 아니라 **골격 β** 였다 |
| **thermostat** | 100 fs 마다 **속도 재조정** | **Langevin friction 0.02 (τ ≈ 0.51 ps)** | ⛔ **우리가 불리하다.** [Maginn19MD] §4.1.1 이 속도스케일링 계열은 NVE 구분불가, **Langevin/Andersen 은 강결합(0.1–1 ps)에서 D 를 극적으로 낮춘다**고 이름을 대서 경고 |
| **시드/복제** | (조성,온도)당 **궤적 1개**, 오차는 같은 궤적 **10등분 블록**(무상관 가정 미검증). **D\* 는 오차막대 없음** | 시드 3 | 🟡 우리가 낫지만 [Maginn19MD] 문턱(≥20)에는 둘 다 미달 |
| **무질서 처리** | ⛔ 조성당 **단일 배열** (실험 점유를 "최대한 근사" + Li–Li 거리 최대화) | comp2 disorder ensemble (라벨스왑 d-level · cfg 0/1/2) | ✅ **우리가 앞선다** |
| **보고량 `D_rel` @600 K** | 개념상 동일. **digest 계산 D_rel: Br 14×(450 K) → 3.2×(600 K) → 1.3×(750 K)** · O 750 K **0.87×** | 비준 보고량, cell-conditioned | ✅ **살아남고, 경고를 받는다**: **비 자체가 온도의 함수**다. ⇒ ① 600 K D_rel 을 상온 σ 비로 읽지 않는다(우리 규율과 일치, 문헌 근거 확보) ② **한 온도의 도펀트 순위를 다른 온도로 옮기지 않는다** ③ 무너지는 이유 = 고온에서 Li 부격자가 녹아 **설계로 만든 사이트 정렬이 사라진다** |

**⛔⛔ b2o3 축 — 이 편이 하는 일과 하지 않는 일**

> **하지 않는 일**: `db/properties/b2o3_md_closed_retrospective_2026_08_25.json`(비준 `D-2026-09-07-b2o3-md-closure-retrospective`)의 판정을 **건드리지 않는다.** 이 편에는 골격 게이트도, 문턱값도, MLIP 편향 진단도, 궤적 보존 규약도 **없다.** 재개 경로는 여전히 **전향적 사전등록 카드 하나뿐**이다.
> **하는 일**: 그 카드가 요구할 수 있는 **후보 항목 4개**를 제안한다 (digest §8.3) —
> **+D1** `f = D*/D_J` 를 **골격 오염의 직접 지표**로 (Li 가 골격과 함께 병진하면 변위는 늘고 홉은 안 느니 **f 가 위로 튄다**; 골격 MSD 게이트와 **논리적으로 독립**, 추가 계산 0)
> **+D2** 고정 사이트 격자에서 **사이트 할당률이 시간에 따라 단조 감소하면 골격이 움직인 것** (이진 시험)
> **+D3** **방향분해 MSD 필수 제출** — 세 방향 모두 `D_inc` plateau 를 보여야 3D D 를 보고 (b2o3 는 면내 7 Å 슬랩이라 이방성이 구조적)
> **+D4** 골격 원자(P·S·B·O)에 **진동진폭 분포**를 돌려 비-Gaussian 꼬리 검사 (미검증 — 우리가 시험해야 함)
> ⛔ 넷 다 *"이 논문의 도구를 우리 문제에 돌려 쓴다"* 이지 *"이 논문이 우리 결과를 검증한다"* 가 아니다.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_deklerk2018_diffusion_analysis_md_beta_li3ps4.md` ### 2-b..</sub>


**[Gra25UQ] `grasselli2025_uncertainty_era_ml_atomistic` — 불확실도 어휘·판정선의 정의 원본**
(⛔ 물성값 0건. A–D 4축 행 금지. 아래는 **정의**와 **우리 위치 판정**뿐이다.)

| 항목 | [Gra25UQ] 가 정의하는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| **불확실도 4겹** | ①epistemic ②aleatoric ③**오설정**(§2.9) ④**표집/통계**(§2.8) | 축 2개(모델 / 시드·궤적) | 🔵 **재라벨 필요** — 아래 두 행 |
| **시드·궤적 축** | ④ *"the statistical one due to a poor sampling (i.e. too short trajectories)"* (§2.8) | 600 K **3-seed**, MSD 2–50 ps, `Ea 0.197±0.032 eV` | ✅ **깨끗이 일치.** 이름표 그대로 채택 |
| **모델 축 (`force_contrast`)** | §2.2 앙상블은 멤버가 **"equivalent models"**(같은 데이터 부분표집 / **훈련 시드**·MC dropout)여야 한다 | UMA(OMat24) · MACE-MP-0(MPtrj) · SevenNet-0(MPtrj) = **아키텍처도 훈련셋도 다름**, **M=3** | 🔴 **①epistemic 이 아니다.** 실질 **③오설정 대조 + §3.2 위원회 OOD 프록시** ⇒ ⛔ *"epistemic uncertainty"* 로 부르지 말 것 |
| **캘리브레이션 하한** | 식 (27) 편향보정 ⇒ **최소 M = 4** (`(M−3)/(M−1)`=0 at M=3 → `α²=−1/3<0`) | **M = 3** | 🔴 **단위 있는 σ 원리적 불가.** 우리 "절대 σ 인용 금지"의 **식 근거 확보**(종전엔 경험 관례) |
| **aleatoric 칸** | 잡음 없는 관측(=DFT 라벨)에서는 모든 편차가 **모델 편향** (Heid ref 34) | DFT 라벨 = 결정론적 | ✅ **우리 계엔 ② 칸이 없다.** `Fig. 3a` 빨간 상자 해당 없음 |
| **"시드"의 의미** | §2.2 의 시드 = **훈련 시드**(앙상블 멤버 생성) | 우리 시드 = **MD 초기속도 시드** | ⚠ **다른 것.** 섞어 쓰면 §2.2 와 §2.8 이 뒤엉킨다. UMA 는 고정 체크포인트라 **훈련시드 축이 원리적으로 없다** |
| **관측량 전파 도달점** | 힘/E → **차이량**(상관 덕에 작음) → **정적·열역학 평균**(식 31 reweighting, 궤적 1개) | — | ✅ **정적 지표(RDF·배위수·⟨E⟩)에는 지금 당장 위원회 오차막대 가능** |
| **수송계수 전파** | 🔴 *"rigorous theory"* **부재**. 현재는 **멀티궤적 brute-force 뿐** | `D_rel` = 확산계수 비 = **수송계수** | 🔴 **우리 3-seed 가 문헌이 아는 전부.** 뒤처진 게 아니라 **분야 한계**. 단 그것은 ④만 재고 **①은 시드를 늘려도 안 채워진다** |
| **`D_rel` 이 비(ratio)인 것** | §2.8(c): ML 오차는 가까운 배치에 **고도로 상관** ⇒ **차이의 불확실도 ≪ 절대값** | 설계/host 를 **같은 모델**로 | ✅ **설계 정당화.** ⚠ 저자 논증 대상은 **에너지 차이**이고 수송계수 비가 아니다 — **유추임을 밝히고 인용** |
| **단일 uMLIP UQ 처방** | **마지막층 Laplace, 식 (14)**, 추론 부담 거의 0 (§4.1, ref 142) | 없음 | 🔵 **다음 계산 1순위.** 라벨 검증셋 후보 = `db/properties/mlip_bench_li3ps4_uma.json` (PET-MAD Li₃PS₄ 243구조 PBEsol) ⚠ **Cl 부재 = "critical subdomain underrepresented"** |
| **UMA = MoE 분류** | §2.3.2 가 **ref 40 (Wood et al., UMA)** 을 MoE 사례로 인용, 식 (25) 제공 | UMA-s-1p1 | ⛔ **식 (25) 를 UMA 에 적용 금지** — 식은 전문가별 독립 데이터셋·`G⁽ᵏ⁾`·`α⁽ᵏ⁾` + Zeni 라우팅 전제. **UMA 라우팅 구조를 이 리뷰가 확인해 주지 않는다** |
| **오설정 = 우리 봉인 논증** | 앙상블 전원이 같은 틀린 예측에 합의 → **인위적으로 낮은 σ**, **전역 캘리브레이션으로 불가** | 봉인 `mlip_applicability`: *"점수와 검증이 같은 퍼텐셜이라 함께 틀리면 상관은 오히려 좋아진다"* | ✅ **독립 도달 확인.** 우리 논증이 문헌 표준과 동일 |
| **전이성 3분류** | Phase / Temperature(**고온→저온 일반화 양호**) / Compositional(**새 원소 외삽은 맞춤기법 없이 어렵다**) | 상(결정↔무질서) · 600–1000 K · 도판트 30종 | ⚠ **세 갈래 동시**. 세 번째가 저자들이 어렵다고 한 그것 ⇒ 봉인의 *"UMA 내부 순위로만"* 이 옳다 |
| **OOD 판정법** | ⛔ convex hull(고차원 붕괴 + **비볼록 구멍 오판**, `Fig. 4`) / ✅ **적응 k-NN 밀도(식 32)+TwoNN 내재차원** · GMM NLL · 하우스도르프 | 없음 | 🔵 후보 — cascade 조성공간이 비볼록일 위험 |
| **γ(외삽등급) 원전** | §3.5.2: *"original paper by **Podryabinkin and Shapeev**"* (ref 108, *CMS* 140, 171, 2017) | `talks/lee2026_skku…` §99-10 3b′ 의 재귀속 후보 | ✅ **같은 방향의 외부 증언** ⚠ **리뷰 경유** — 1차 근거 아님 |
| **γ 비선형 일반화 귀속** | **Gubaev 2018, *JCP* 148, 241727** (ref 113) | `tools/ionic/mlip_committee.py` = **Gubaev 2019, *CMS* 156, 148** | ⚠ **서로 다른 논문.** 원문 미확인 ⇒ **도구 귀속 안 바꾼다** |

**⛔ [Gra25UQ] 에서 인용하면 안 되는 것**
1. 리뷰가 요약한 **2차 수치** 전부 — 전이성 관행 문턱(**10 meV/atom · 100 meV/Å**), γ 문턱(**≲1 / ≫1**),
   앙상블 통상 크기(**5–10**), Kellner–Ceriotti 물의 **N·√N**, DeePMD **3층×240**. 전부 `[리뷰경유]`.
   → 원 논문 확인 전 **우리 표의 1차 근거 금지**.
2. *"이 리뷰가 방법 A 가 B 보다 낫다고 했다"* — **저자 자신의 정량 비교가 0건**이다.
3. `Fig. 6`·`Fig. 7` 의 축 값(eV/atom 등) — **합성 데이터로 판단**(확인은 못 함).
4. **이 논문으로 "우리 UMA 결과가 신뢰할 만하다"를 주장** — 이 논문은 재는 법을 말하지 우리 점수를
   말하지 않는다. **오히려 우리가 ①을 안 재고 있다는 것을 드러낸다.**

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_grasselli2025_uncertainty_era_ml_atomistic.md` ## ② .</sub>


**[He23Hal] `he2023_halogen_chemistry_solid_electrolytes` — 우리가 쓰는 argyrodite 용어·프레임의 표준 서술**

| 항목 | [He23Hal] 의 정의/서술 | 우리 | 판정 |
|---|---|---|---|
| **free-anion 자리 표기** | **4a / 4d**, **케이지 중심 = 4d** (`Fig. 4b` 범례 + `Fig. 4c`) | 우리·`deklerk2016` digest = **4a / 4c(=4d)** | ✅ **매핑 확정.** 원고·발표는 **4a/4d 로 통일**(Nat. Rev./Kraft/Wang P. 관례). ⛔ 한 문장에 4c 와 4d 를 섞지 말 것 |
| **점프 3종 정의** | **doublet(48h–24g–48h) · intra-cage(48h–48h) · inter-cage(48h–48h)**, inter-cage 가 거시 수송 지배 (`Fig. 4d`, 본문-refs 132–134) | 동일 정의(de Klerk 계보) | ✅ 용어 일치 — 우리 MSD/점프 분석의 표준 어휘로 채택 |
| **무질서 → 수송 on/off** | all-Cl@4a → inter-cage **0** / all-Cl@4d → doublet 급락 / 최적 **4a:4d = 1:3** (본문-ref 135) | comp2 ordered(d=0) frozen 아티팩트가 같은 물리; disorder ensemble d-level 스캔 | ✅✅ **우리 comp2 설계의 문헌 프레임.** ⚠ **"최적 %" 숫자는 인용 금지** — 원전은 분포당 단일 배열·단위셀·100 ps 이고 2024 MTP-MLIP 재검은 25 % 를 보고한다. 안전 인용 = *"중간 무질서에 최적이 존재(양 끝은 나쁘다)"* |
| **Cl-rich 가 빠른 이유** | **에너지 지형(무질서·4d 음전하↓·24g 점유↑)** — *"not caused by Li deficiency"* (본문-refs 138·162) | 우리는 지금 **disorder + vacancy** 로 서술 | ⚠ **서사 교정 권고**: "무질서가 주, vacancy 는 동반" 으로. 문헌 표준은 vacancy 설명을 **명시적으로 배제**한다 |
| **Cl/S 무질서의 구조적 근거** | **Cl⁻ 167 pm vs S²⁻ 170 pm (3 pm)** / Br +12 / I +36 pm (`Fig. 2a`) | 우리 comp1·modelc 의 S/Cl 자리교환 decorate | ✅ **한 줄 근거 확보** (⚠ Shannon 반경 — 리뷰가 출처를 안 밝힘) |
| **24g 점유율** | `Fig. 5a` 가 **σ 의 중간 지표로 명시** | 미측정 | ⭕ **이식 후보 (T1)** — UMA 궤적에서 싸게 뽑히는 양. **문헌 기전을 우리 데이터로 직접 시험** |
| **산화 onset** | **수치 0건.** 정성 서술의 비교쌍은 **LPS vs LPSX**(argyrodite 내부 Cl 1.0↔1.6 아님) | comp1·modelc **동일 2.256 V (S²⁻-limited)** | 🔴 **표면상 상충 — 실제로는 다른 비교쌍.** 섞지 말 것. 우리 편은 **[Banik]**(S 가 VBM pin)이 지지하고, 리뷰 스스로 본문-ref 167(=**[Yun23]**)로 ESW 확장 주장을 되돌린다 |
| **수분/공기** | argyrodite 정량 **0건**. F@Li₃InCl₆ 의 **σ↓ + 수분보호↑** 사례만(본문-112) | LPSOCl / +B₂O₃ 축 | ⚠ **[Wang25DPA] `Fig. S11`(O 도핑 σ −41 %)과 상충하지 않지만 지지도 안 한다.** 같은 *모양*의 트레이드오프를 다른 화학에서 제공 ⇒ **간접 지지**. 근거로 쓸 것은 **본문-ref 154(Li G. 2022 AFM, `Li₅.₅(P₀.₉Sn₀.₁)(S₄.₂O₀.₂)Cl₁.₆`)** |
| **Li 금속 계면** | `Fig. 7d` `Li₆PS₅Cl→Li₁₁PS₅Cl→{Li₂S,LiCl,S}→{Li₃P,LiCl,Li₂S}` + **전자 차단(자기제한)** vs `Fig. 7c` Li₃MX₆ **혼합전도 폭주** | grand-potential 환원한계 1.242 V / OCV 1.717 V | ✅ **정성 정합**(산물 계열 동일). ⛔ 전압 대 전압 비교 불가(리뷰에 수치 없음) |
| **modelc 의 물리적 정체** | 본문-ref 185(Zeng 2022): **과잉 Cl 의 다수는 입계 LiCl 나노쉘**, 격자 치환은 소수 | modelc = Cl 1.6 **전량 격자 치환** 단결정 셀 | 🔴 **모델 한계 명시 의무.** *"실험 Cl-rich 시료의 모델"* ❌ → *"a fully lattice-substituted Cl-rich model / the bulk-lattice limit"* ⭕ |
| **희토류 도핑** | *"still at an early stage … roles of the different rare earths need to be further explored"* (p838) | `ndo_lpscl16`(Nd·O) | ✅ **우리 gap 문장의 외부 근거.** 원고 서론에 거의 원문 인용 가능 |
| 밴드갭 / 기계 | **0건 / 0건**("deformability" 정성) | comp1 2.066 · modelc 2.099 eV / E_VRH 22.06→27.66 GPa | **n/a — 비교 대상 없음** |

**⛔ [He23Hal] 에서 우리 쪽으로 옮기면 안 되는 것**
1. **`Table S1` 의 σ·Ea 값 전부** — 압력 44행 미기재, 조건 미상. **ML 학습 라벨로도 금지.**
2. **"4a:4d = 1:3 최적"의 숫자** — 방법 의존(2024 MTP-MLIP 는 25 %). 정성 문장까지만.
3. **`Fig. 6` 의 어떤 점도** — 양극·음극·로딩이 전부 다른 14개 셀. 전해질 순위를 말할 수 없다.
4. **"할로겐이 ESW 를 넓힌다"** 를 **argyrodite 내부 Cl 조성 효과로 옮기는 것** — 비교쌍이 다르다.
5. **본문 ref 번호로 `Table S1` 값을 인용하는 것** — SI 는 별도 번호 체계다.
6. 🔴 **본문 p832 의 "Li₆PS₅I ≈ 10⁻⁶ S cm⁻¹"** — 자기 `Table S1`(2.2×10⁻⁴)과 **220× 모순**.
   Li₆PS₅X 의 σ 대비가 필요하면 **`Table S1` 값만** 쓰고, **기전은 `deklerk2016`(all-4a → inter-cage 0)로** 인용한다.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_he2023_halogen_chemistry_solid_electrolytes.md` ## ② .</sub>


**[Imbalzano21] `imbalzano2021_committee_uq_md_thermodynamic_averages` — committee 불확실도를 궤적 평균까지 전파하는 통계 원전**
(EPFL COSMO, Grasselli & Ceriotti 교신 · ⚠ **PDF 에 저널·DOI·arXiv 없음**, pdfTeX 2020-11-10 preprint ·
계: 물·삼펩타이드·메탄술폰산/페놀·액체 Ga — **Li·황화물·아르지로다이트 0건, 물성값 0건**)

> ★ **왜 이 편이 MLIP 불확실도 축 3편 중 제일 중요한가**: 다른 UQ 논문이 **힘·에너지 오차**에서 멈추는데
> 이 편은 그걸 **궤적 평균까지 전파**한다. 우리 D 는 MSD 기울기 = 궤적 평균이라 겉보기 구조가 같다.
> **그런데 겉보기만 같다** — 아래 표 마지막 두 행이 그 이유다.

| 항목 | [Imbalzano21] | 우리 (UMA-s-1p1 단일 모델) | 판정 |
|---|---|---|---|
| committee 구성 | 전체 훈련셋을 **복원 없이 부분표집** → M 모델 독립학습 (⚠ 실제로는 계마다 다름: Ga DOS 는 300/394 부분표집, 삼펩타이드는 **초기화 시드 + 90/10 CV 분할만**) | **단일 파운데이션 모델. committee 자체가 없다** | 🔴 **σ_V·α·재가중 전부 실행 불가** |
| committee 크기 M | 4(펩타이드·물·Ga PM) · 5(산/페놀) · **64**(Ga DOS OM) · 16(부록 α 분석) | 이종 3종(UMA/MACE-MP-0/SevenNet-0) = **M=3** · 시드 3 | 🔴 **`E[1/ς²]=(M−1)/(M−3)` 이 M=3 에서 발산 ⇒ 우리는 하한 미달** |
| 최소 M | **4 하드 하한**, 비선형 전파 시 **6 권고** (Appendix A) | — | ⇒ **PET-MAD/UMA-1.2 4번째 투입은 "권장" 이 아니라 "하한 도달"** (§J-5 처방의 정량 근거) |
| 교정 α | 로그우도 최대화. **α = 2.1**(물) · **4.08**(산/페놀) · 1.0(펩타이드). **전부 ≥1 ⇒ raw 산포는 참오차를 2–4배 과소추정** | **α 를 잴 수 없다** — 참조 DFT 검증셋도, UMA 훈련분포(OMat24)도 우리에게 없다 | ⚠ **우리 committee 불일치는 "하한" 으로만 말한다.** *"불일치가 작았으니 안전하다"* 는 결론을 **이 논문이 지지하지 않는다** (`b2o3_committee_2026_09_07.json` 허용선과 정확히 양립) |
| 전파 방식 | `Eq. 22` 재가중(정확) → 계 크기에 **지수적**으로 통계효율 붕괴 ⇒ **`Eq. 24` CEA 선형화** | — | ⭕ **개념만 이식.** CEA 는 `⟨a⟩_{V^(i)} ≈ ⟨a⟩_V̄ − β⟨a(V^(i)−V̄)⟩_V̄` — **선형화이지 재가중이 아니다** |
| 분산 분해 | **`σ̃² ≈ σ_a² + σ_V²`** — 관측량모델(OM) + 퍼텐셜모델(PM). `σ_V ≈ β·std_i[Cov(a, V^(i)−V̄)]` | 우리 D 에는 **σ_a 항이 없다**(D 는 학습된 관측량이 아니라 궤적의 범함수) ⇒ 모델 불확실도는 **전부 σ_V 형** | 🔴 **그런데 그게 정확히 못 재는 항이다** |
| 비교 대상 | `Fig. 8` 액체 Ga DOS 에서 σ_a 가 σ_V 를 지배 (figure-read: 원자가띠에서 σ_V ≈ σ_a 의 1/3–1/2) — 그래도 저자는 *"σ_V is sizeable"* | — | ⇒ **관측량 모델을 아무리 잘 학습해도 퍼텐셜 쪽 항이 남는다**. 우리는 그 항만 있는데 못 잰다 |
| **관측량 종류** | **정적 배위평균뿐** — g(r) · Δμ/T_m · 자유에너지 프로파일 · 유한온도 DOS | **D = MSD 기울기 (동역학량)** | 🔴🔴 **여기서 갈라진다.** 전문 grep: `diffusion`·`transport`·`MSD`·`mean square`·`Green–Kubo`·`time-correlation`·`conductivity`·`viscosity` **전부 0회**. "correlation function" 6회는 전부 **radial** |
| **동역학 확장 가능성** | 논의 없음 | — | 🔴 **원리적으로 불가.** 재가중은 *"어떤 배열을 얼마나 자주 보나"* 를 고치지 *"그 배열에서 다음 순간 어디로 가나"* 를 못 고친다. `V` 를 바꾸면 힘이 바뀌어 **궤적 자체가 갈라진다** ⇒ ⛔ *"Imbalzano 를 따라 D 에 committee 불확실도를 붙였다"* 는 문장 **금지** |
| 시드/궤적 통계 축 | ⛔ **형식화 없음.** 정성 언급 3회뿐 (*"comparable"* · *"larger than the statistical error"* · *"somewhat scattered"*) | modelc Ea 3시드 **0.197±0.032 eV** · 단일시드 1.33× 철회(SEMIFINAL 2026-07-09) | ⇒ **우리 시드축을 이 논문이 도와주지 않는다.** 우리 규율이 이 논문보다 이 축에서 **앞서 있다** |
| 비선형 유도량 | `Fig. 6` T_m = 선형적합의 **근**(=계수의 비) → **멤버별 적합 → 멤버별 T_m^(i) → 산포**. `Fig. 7` 대칭 Δp → `−kT log` → **비대칭 구간** | 우리 Ea = Arrhenius **로그 기울기**, D_rel = **비** | ⭕ **절차만 이식**: 멤버별로 끝까지 계산 후 산포. ⚠ **M=1 이라 모델축에선 실행 불가**, 시드축 짝짓기는 **정당화되지 않는다**(다른 계·다른 궤적. 시드번호가 같은 것은 난수열이 같을 뿐 물리적 상관이 아니다) |
| 온도 의존 | `Eq. 28` 에 **β = 1/k_BT 가 앞에 붙는다** — 같은 공분산이면 고온일수록 σ_V 가 작다 | 600/800/1000 K | ⚠ 우리 온도가 이 방향으로는 유리하다. 단 **공분산 자체가 고온에서 커질 수 있어 순효과는 미정** (내 관찰, 논문 미논의) |

**🔴 이 축에서 제일 중요한 두 줄**

1. **우리 D 오차막대의 이름이 틀렸다.** 이 논문이 형식화한 분해(`σ_a` + `σ_V` vs 통계)로 재면,
   우리가 지금 낼 수 있는 것은 **통계(시드/블록) 오차막대**이고 **모델 불확실도가 아니다**.
   ⇒ `db/properties/` 와 원고 캡션의 *"uncertainty"* 를 **`seed/statistical spread`** 로 명시한다
   (우리 **Q7** 판정 — *"창 4개의 max−min 은 불확도가 아니다"* — 과 같은 계열의 정정).
2. **이 논문의 통계를 우리 이종 committee 에 이식하면 안 된다.** 가정 셋이 다 깨진다:
   (i) **같은 `y_ref`** — OMat24 vs MPtrj 로 훈련셋·DFT 설정이 달라 세 모델의 target 이 같은 함수가 아니다.
   (ii) **교환가능** — MACE-MP-0 과 SevenNet-0 이 **둘 다 MPtrj** 라 상관, 실질 표본은 3이 아니라 ≈2 클러스터
        (§J-5 가 이미 지적한 것과 같은 얘기).
   (iii) **가우시안** — 참조라벨이 없어 검증 불가.
   ⇒ 남는 것은 **순서적 신호**(이 배열이 다른 배열보다 합의 밖이다)뿐이고, 그게 정확히
   `tools/ionic/mlip_committee.py analyze` 가 하는 일이다. **이 논문은 그 도구를 정당화해 주지 않는다** —
   오히려 M=3 · 상관 · 비교환성을 **전부 지적하는 쪽**이다.
   ⭕ 다만 **한 가지는 우리 편**: α 논리가 *"committee 산포는 절대오차가 아니라 교정이 필요한 대리지표"* 라고
   말하므로, 문턱을 **상대적으로만** 쓰고 기준선을 **별도 표본**에서 잡는 우리 방식이 이 논문 정신과 맞다.

**⚠ 우리 도구 표기 정정 (2026-09-09, 코드 재독)**
`tools/ionic/mlip_committee.py` 의 **`force_contrast` 는 이종 committee 가 아니다.**
`cmd_force_contrast`/`contrast_from_forces` 는 **한 엔진(기본 UMA)의 예측을 파일 안 DFT 라벨과 비교**해
골격 힘오차를 내고 그것을 **test 계 / control 계의 비 R** 로 만든다
(카드 `db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json`).
**이종 3종 committee 는 `sample` → `predict --engine {uma,mace,sevennet}` → `analyze` 경로**이고,
[Imbalzano21] 과 대응하는 것은 **`analyze`** 쪽이다. 위 표는 `analyze` 기준으로 읽는다.

**🔧 우리 산술 (논문 주장 아님)**
- 편향 배율 `√[(M−1)/(M−3)]`: M=4 **1.73** · 5 1.41 · 6 **1.29** · 8 1.18 · 16 1.07.
- M 표본 SD 의 상대오차 `1/√(2(M−1))`: M=3 **50 %** · 4 40.8 % · 6 31.6 %.
  ⇒ **3점으로 낸 ± 는 그 자신이 ±50 % 다.**
- `Fig. 9` 자체검산: figure-read M=16 무편향 α ≈ 2.77 을 참값으로 `Eq. A1` 에 넣으면
  M=4 편향판 4.88 (그림 4.6), 역변환 무편향 2.61 (그림 2.62) — **식과 눈금 판독이 자기일관적**.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_imbalzano2021_committee_uq_md_thermodynamic_averages.md` ## ③ .</sub>


**[Jang25As] `jang2025_thioarsenate_argyrodite_mlip_mechanism` — 음이온 무질서에 좌표를 붙이는 법 (ΔS_conf)**
(*J. Mater. Chem. A* **13**, 33203–33211, 2025 · **As/Br 계**라 우리 물성값과 겹치는 칸 0개 · Ea·D **논문에 없음**)

> ⛔ **σ 를 우리 db 옆에 놓지 않는다** — 참조 PES(**optB88-vdW** vs 우리 PBE 계열)·**MSD 창 미기재**(vs 우리 2–50 ps)·
> 셀(**3,328** vs 62원자)이 **세 겹으로** 다르다. 그리고 CLAUDE.md 가 우리 σ 절대값 인용을 금지한다.
> 아래는 **방법·좌표계·설계**만 옮긴 것이다.

| 항목 | [Jang25As] | 우리 (`tools/modelc_v3/disorder_ensemble_diffusion.py` + `pipeline_v2`) | 판정 |
|---|---|---|---|
| **무질서 파라미터** | **f = 4d 의 할로겐 분율** — **자리 점유수 = 상태변수** | **d = 2·n_swaps / n_free_sites** — 기준 배열로부터의 **거리**, 상태변수 아님 | 🔴 **개념이 다르다.** modelc 에서 `d = 0.4` 하나에 **ΔS 0.673R 46 % + 1.001R 54 %** 가 섞인다 ⇒ **라벨을 `(f, ΔS_conf)` 로 바꿔야 한다** |
| **정량 지표** | **ΔS_conf = −R{Σ_4a x lnx + Σ_4d x lnx}** (식 4). 계산비용 0(해석식) | ⛔ **없다** | ⭕ **즉시 이식 (T0, 계산 0회).** **우리 축 최초의 정량 지표** |
| **우리 셀 좌표** (신규) | — | **modelc f = 0.60 · ΔS = 0.673R = 5.60 J mol⁻¹K⁻¹** / **comp1 f = 0 · 0.000R** `digest 계산` | 🔵 최근접-P 거리로 자유음이온 10자리를 **5:5 로 이분**(간격 0.33 Å), 자유 S²⁻ 둘이 근거리 무리 = 4d |
| **우리 셀의 도달범위** | — | 62원자 셀은 **3준위뿐**: f 0.6/0.8/1.0 → ΔS **0.673 / 1.001 / 0.673R**, 배열 **10/25/10 = 45** | ✅ **45 = `modelc.json` `halogen_screening.n_configs` 와 정확히 일치** ⇒ 전수열거는 이미 끝났고 **44개를 버렸을 뿐** |
| **엔트로피 최적 반전율** | x=0 에서 **50 %** | 일반해 **f\* = (1+x)/2** ⇒ **modelc(x=0.6) 은 80 %** `digest 계산 (원논문 미보고)` | 🔴 **50 % 를 우리 계로 이식 금지.** 논문의 50 % 는 x=0 특수해다 |
| **실험 기준점** | — | `adeli2019` 중성자(Cl1.5, 4a-Cl 0.615/4d-Cl 0.834) → **ΔS = 1.116R = 그 조성 최대의 95–99 %** `digest 계산` | 🔴🔴 **우리 셀은 자기 최대의 67 %.** **계산 셀이 실제 물질보다 훨씬 정렬돼 있다.** ⚠ 조성이 Cl1.5 vs Cl1.6 로 다르다는 단서 병기. ⛔ *"그래서 우리 σ 가 과소다"* 는 **아직 못 하는 말** |
| **배열 선택 규칙** | Ehull 축 = 단위셀 전수 + **최저에너지 1개** / MD 축 = **⛔ 미기재** | **45개 전수 → 최저에너지 1개** (`best_s_indices=[1,4]`) | ⚠ **같은 규칙, 같은 편향** — 최저에너지는 **저무질서 끝**이다. 저들은 그래도 MD 축을 33준위로 벌렸고 **우리는 안 벌렸다** |
| **배열당 반복** | **1런, 오차막대 0** | **3-시드** (600 K 3-seed Ea 0.197±0.032 eV) | 🔵 **우리가 낫다.** 단 **배열은 셋이 공유**(`--v0_xyz` 공유·`--disorder_levels 0.0`) ⇒ **우리 오차막대는 "한 배열 안의 산포"** |
| **★ 산포 죽이는 지렛대** | **셀크기** (`Fig. S4`: 52원자 5런 MSD `≈55–107 Å²` **2×** → 3,328원자 `≈70–73` **4 %**) | **시드** (62원자에 3-시드) | 🔴 **우리 62원자가 정확히 그 2× 영역이다.** ⇒ **우리 3-시드 산포가 물리인지 유한크기 잡음인지 지금은 구분 불가.** ⚠ 저들은 300 K·우리는 600 K 라 **이 논문이 우리 산포 크기를 정하지는 않는다** — `modelc_2x_V0.xyz`(558원자)로 우리가 직접 재야 한다 |
| **MSD → D** | 식 `D = ⟨Δr²⟩/(2dt)`, **창·절편·다중원점 전부 미기재**. D 값 자체를 **한 번도 안 적음** | **2–50 ps 고정 · 자유절편 · `msd_multi_origin`** | ⛔ **정량 대조 원천 봉쇄** |
| **확산영역 게이트** | ⛔ 없음 (`Fig. 6a` 는 10 ns 케이지간 점프 0 인데 σ 0.9 보고) | `tools/ionic/msd_diffusive_check.py` (미통과 시 HOLD) | 🔵 **우리가 확실히 낫다** |
| **σ 산출** | NE, **Haven = 1 (암묵)** | NE, **Haven = 1 (명시)** | ✅ 같은 관례 ⇒ **같은 방향으로 틀릴 수 있다** (`adeli2019` 실측 Haven 0.3→0.23) |
| **MTP R_cut** | **6 Å** | — | ✅ **§J-7 [Shapeev16] 블록의 *"Lee 랩 argyrodite MTP 는 6 Å"* 와 같은 값** — 아르지로다이트 MTP 관행 6 Å 의 두 번째 데이터점 |
| **학습셋 설계** | 결정(4 T × 3 strain) + **비정질 융해-급랭** + 전구체 4종 = 12,390 | 사전학습 UMA 그대로 | 🔵 **fine-tune 을 하게 되면 이 구성이 참고표**(비정질·변형을 일부러 넣는다) |

**⭕ [Jang25As] 에서 이식할 것 (T0 = 계산 0회)**
1. **ΔS_conf 좌표계** — `disorder_ensemble_diffusion.py` 에 `--report-sconf` 플래그로 붙인다
   (새 스크립트 금지, 기존 도구 확장). config 레코드에 **`f`·`dS_conf_over_R`·`n_Cl_4d`** 기록.
2. **`Fig. 2a` 바이올린 표현법** — 배열 45개의 Ehull/D 를 점 하나가 아니라 **분포**로 그린다.
3. **`Fig. 7a` 형식의 (반전 × 조성) 등고선** — 우리 Cl-rich 계열도 같은 지도를 그릴 수 있다.

**🔴 [Jang25As] 대조로 드러난 우리 도구 결함 3건** (digest §9-1 · §16-5)
| # | 무엇 | 크기 |
|---|---|---|
| 1 | `make_disordered()` 의 `c_pick` 이 **모든 Cl 8개**에서 뽑는다 → **자유-S(4d) ↔ Cl(4d) 스왑은 항등연산** | 단일 스왑의 **3/8 = 37.5 %** 가 무효 |
| 2 | `d` 라벨 하나에 물리적으로 다른 상태가 섞인다 | `d=0.4` 에서 ΔS 0.673R **46 %** + 1.001R **54 %** |
| 3 | docstring *"modelc only 1/8 anti-site"* | 실제는 **8 Cl 중 3개가 4d** 이고 그건 무질서가 아니라 **화학량론 강제 최소반전 f = x = 0.6** (4a 5자리에 Cl 8개는 안 들어간다) |

**⛔ 이 축에서 인용하면 안 되는 것**
1. **σ 절대값을 우리 db 옆에** — 참조 PES·MSD 창·셀 세 겹 차이 + CLAUDE.md 금지.
2. *"엔트로피가 전도도를 결정한다"* — **인과 미검증**. `Fig. 5c` 는 두 갈래이고 상관계수가 없다.
3. *"최적 반전율은 50 %"* — **x=0 특수해**이고, 같은 P/Cl 계 문헌이 25/50/75 %, 실험 실측은 83 % 로 갈린다.
4. *"계산이 실험과 잘 맞는다"* — 겹치는 두 조성에서 **3.3×·6.3× 과대**.
5. *"Br(→Cl) 을 더 넣으면 빨라진다"* — **반전율과 교란**된 진술.
6. 이 논문의 **"안정성"을 우리 산화안정 4축과 섞는 것** — 여기서 안정성은 **오직 열역학 Ehull** 이다.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_jang2025_thioarsenate_argyrodite_mlip_mechanism.md` ## ③ .</sub>


#### J-7-N. ★★★ **[Jeon26Con] — Haven 비를 궤적에서 직접 재는 법 (규약 자유) + 묶음 3편 재정렬** (2026-09-09 신설)

**(a) 이 편이 채우는 빈칸**
우리 σ 는 **NE, Haven H_R = 1 고정**이다. 그 오차를 재려고 모은 3편 중 **유일하게 (i) 우리와 같은 argyrodite 골격이고
(ii) tracer 와 charge D 를 *같은 궤적에서 직접* 분리**한 편이다.

| 출처 | 계 | 방법 | 원 보고 H_R | 캐리어 수 규약 |
|---|---|---|---|---|
| **[Adeli19]** | Li₆₋ₓPS₅₋ₓCl₁₊ₓ | 실험 PFG-NMR + EIS 역산 | 0.23–0.3 | ⚠ **c = 4 Li/cell (저자 명시 하한)** |
| **[Zaby26σ]** | IL·LiFSI 액체 | 고전 MD (EH·GK) | 1.3–2.1 | 전 이온 (모호성 없음) |
| **[Jeon26Con]** | Li₆₊ₓAs₁₋ₓSiₓS₅I | **AIMD, 집단 MSD 직접** | **1.83 / 0.53 / 0.64 / 0.77** | **없음 (H 에서 n 약분)** |

**(b) 재현에 필요한 규격 전부** (`Table S10` · SI "Tracer and collective diffusion")
- `MSD_σ(τ) = 1/[N(N_t−n)] · Σ_j |Σ_i (r_i(t_j+τ) − r_i(t_j))|²` — **합을 먼저, 제곱을 나중에.** 정규화는 **1/N** (1/N² 아님)
- `MSD_tr` 도 **같은 multi-time-origin** 으로 다시 계산 (본문 `Fig. 5`/`Table 3` 의 단일 origin 값과 다르다)
- `D = MSD(τ)/6τ` — **원점 통과 현(chord)**. ⚠ **우리는 자유절편 기울기 2–50 ps** ⇒ **추정자가 다르다**
- `τ_max = 총 시뮬 시간의 1/2` (여기선 250 ps / 500 ps)
- **unwrapped 좌표 필수** (wrap 되면 벡터합이 깨진다)
- 도구 `pymatgen-analysis-diffusion` (ref 48 Deng 2017) · multi-origin 근거 ref 58 (He/Mo 2018)
- `H = D_tr/D_σ = σ_NE/σ_col`, `σ_col = n q² D_σ/(k_B T)`

**(c) ★★ digest 계산 — 규약을 맞추면 묶음의 그림이 바뀐다** *(원논문 미보고 · 우리 대조)*
[Adeli19] 는 `D_σ = k_B T·σ/(c q²)` 이므로 `H_R ∝ c`. c: 4 → 전 Li(22–24/cell) 로 옮기면 **H_R 이 5.5–6배**:

| | 원 보고 | **전-Li 규약 환산** | NE 는 |
|---|---|---|---|
| [Adeli19] x=0 (Li₆PS₅Cl) | ~0.3 | **≈1.8** | 과대 |
| [Adeli19] x=0.5 | 0.23 | **≈1.3** | 과대 |
| [Zaby26σ] | 1.3–2.1 | 1.3–2.1 | 과대 |
| [Jeon26Con] x=0 | 1.83 | 1.83 | 과대 |
| **[Jeon26Con] x=0.25–0.75** | **0.53–0.77** | 0.53–0.77 | **과소** |

⇒ **규약을 맞추면 4개 중 3개가 H_R ≈ 1.3–2.1 (NE 과대) 로 모이고**, 유일한 이탈자가 [Jeon26Con] 의 Si-치환 조성인데
그것이 하필 **집단 MSD 통계가 가장 미심쩍은 값들**이다.

⚠⚠ **과신 금지 3**: ① [Adeli19] σ 는 cold-press **total** 이라 GB 가 σ 를 깎으면 H_R 이 **부풀려진다** ⇒ 진짜 bulk 는 1.3–1.8 **미만**
(다만 Ea(EIS)≈Ea(PFG) 이므로 GB 가 *장벽*은 안 건드린다 — 앞지수만) ② [Adeli19] 의 c=4 는 임의값이 아니라 저자의 물리 논거
(케이지간 점프가 장거리 수송을 지배) ⇒ 전-Li 가 **더 옳다는 뜻이 아니라 같은 자를 써야 한다는 뜻** ③ 온도가 다르다(1000 K vs 270–340 K).

**⇒ 판정 (변경 없음)**: **"H_R = 1 은 근사가 아니라 미측정이고, 오차의 부호조차 우리 계에서 확정돼 있지 않다."**
다만 **약한 사전(prior)** 이 생겼다 — *규약을 맞추면 argyrodite 에서도 H_R > 1 쪽 증거가 더 많다*. **인용할 결론이 아니라 직접 잴 이유다.**

**(d) ⛔ [Jeon26Con] 에서 인용 금지**
- "argyrodite 의 Haven 비는 0.53–0.77 이다" — **1000 K 1점 · 오차막대 0 · 단일 궤적 · Li 24–27개**
- `Fig. S14` 에서 **x=0 의 charge MSD 는 150 ps 이후 포화**(확산 아님)한데, **H>1 을 만드는 유일한 점이 그것**
- 저자 자신이 **계산한 H 를 300 K σ 에 반영하지 않았다** (digest 계산: 반영 시 12.9 → 16.8 mS/cm 로 실험 8.1–10.4 에서 **멀어진다**)
- σ·D·Ea **절대값 전부** (As/Si+I·anion-ordered 계). ⚠ Ea 0.219 eV 가 우리 modelc 0.224 와 가까운 것은 **우연** — 방법도 계도 다르다

**(e) ✅ 우리가 할 것 — 도구가 이미 거의 다 있다 (digest §12 와 동일)**
> 🔎 **기존 도구 조사 결과 (CLAUDE.md 코드 규율 사다리 ②)**: `tools/ionic/` 에 이미 있다 —
> `msd_origin.py`(MSD→Arrhenius, **최소상 언랩 `df -= np.round(df)` 내장**, `T*/traj.xyz` 를 직접 읽음) ·
> `msd_diffusive_check.py`(**확산영역 인용 게이트**, `no-value`/`HOLD` 2층 판정) ·
> `msd_refit_window.py`(재계산 없이 창 스윕) · `aimd_jump_stats.py`(**케이지 중심 기준 inter-cage hop 율** + van Hove Gs) ·
> `cage_jump_descriptors.py`(intra/inter-cage 48h–48h 거리). ⇒ **새 파일을 만들 이유가 없다.**

1. **보고량 카드 먼저** (`kb/templates/estimand_card.md`): 추정자(현 vs 자유절편)·τ 창·시드 집계·**폐기 기준**을 **결과 보기 전에** 못박는다.
   폐기 기준은 새로 정의할 필요 없다 — **`msd_diffusive_check.py` 의 `no-value`/`HOLD` 2층 판정을 MSD_σ 에 그대로 적용**한다.
   (**[Jeon26Con] `Fig. S14` 의 x=0 곡선이 정확히 그 도구의 `no-value` 사례다** — 좋은 시험 표본)
2. **`tools/ionic/msd_origin.py` 에 `--collective` 플래그** 추가 (MSD_σ = (1/N)⟨\|ΣΔr\|²⟩, multi-origin, τ_max = T/2).
   ⚠ **`msd.json` 으로는 안 된다** — 거기엔 tracer MSD 시계열만 있고 좌표가 없다. **집단 MSD 는 반드시 `T*/traj.xyz` 에서.**
3. 파일럿(무료): 기존 comp1·modelc **1000 K 궤적**으로 MSD_σ 를 그려 `Fig. S14` 식 포화가 나오는지 본다 → 나오면 1번 게이트 발동
4. 추정자 두 벌(현 / 자유절편 2–50 ps)로 H 를 다 내서 **추정자 의존성**부터 보고
5. 본계산: **배열 시드 + 속도 시드 8–16개 × 500 ps–1 ns**. ⚠ 우리 현행 3-seed 는 **속도 시드만·배열 고정**이라 집단항엔 부족
   🔑 **H_R 의 병목은 힘 정확도가 아니라 독립 궤적 수다 ⇒ 이 논문이 AIMD 로 못 한 것(조성당 500 ps × 1개)을 UMA 로 살 수 있다**
6. (별건, 값싸다) **§A 의 "총 점프 수는 그대로, 케이지간만 바뀐다"를 우리 계에서 재현** — `aimd_jump_stats.py` 가 이미 inter-cage hop 율을 낸다
7. (사용자 승인 후) `adeli2019` digest §3c 에 **전-Li 규약 환산 ≈1.3–1.8** 을 각주로 추가

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_jeon2026_concerted_li_motion_argyrodite_assi.md` ## ④ .</sub>


**[Kurn26UQ] `kurniawan2025_comparative_ensemble_uq_nnip` — UQ 를 *채점하는 지표* 의 원전**
(*Mach. Learn.: Sci. Technol.* **2026**, in press · Kurniawan/Wen/**Tadmor**/Transtrum · **탄소 동소체 전용 · 물성값 0**)

> 🔑 **우리가 이 편에서 가져오는 것은 값이 아니라 "채점표"다.** 지금 우리에게는
> **committee 불일치를 채점할 지표가 하나도 없다** — 이 논문이 그 다섯 개를 준다.

| 항목 | [Kurn26UQ] | 우리 (`tools/ionic/mlip_committee.py`) | 판정 |
|---|---|---|---|
| **σ(불확실도)의 정의** | **동일 아키텍처·동일 데이터** 앙상블 100멤버의 표준편차 (bootstrap/dropout/random-init/snapshot 4종) | **이종 3모델**(UMA-OMat24 / MACE-MP-0-MPtrj / SevenNet-0-MPtrj) 프레임별 원자당 힘 RMS 불일치의 **쌍별 최댓값**, 평균 힘 크기로 정규화 | ⚠ **부류가 다르다** — 우리 것은 ③ random-init 의 **일반화판**(변동 출처 = 아키텍처+훈련셋). ⇒ 우리 σ 는 **epistemic + 훈련셋 계통차의 혼합**이고 이 논문에는 그 항이 없다. **σ 해석 직수입 금지** |
| **잔차(정확도)의 정의** | DFT 라벨 대비 에너지·힘 residual/MAE/RMSE | `force_contrast`: UMA vs DFT 라벨, 골격 `dF_frame`·상대 `dF/F_ref`·`cos θ` | ⭕ **같은 축이다** |
| **M1 패리티 도식** | `Fig. 6`: y=|오차|, x=σ, **log-log**, KDE 등고, **회색 삼각 = underconfident** | ⛔ **없다** | ⭕⭕ **T1 이식 1순위** — `analyze` 와 `force_contrast` 산출 JSON 을 **프레임 키로 조인**하면 새 도구 없이 그려진다 |
| **M2 순서 지표** | `Pearson(residual, σ)`. **all-data: bootstrap 0.76 / dropout 0.40 / random-init 0.32 / snapshot 0.30** | ⛔ **없다** | ⭕⭕ **우리 값의 눈금이 생긴다.** 우리 committee 가 0.3 대면 *"이 논문의 약한 방법들과 동급"*, 0.7 대면 *"bootstrap 급"* |
| **M3 크기(보정) 지표** | `MAE` vs `⟨σ⟩` 병렬. bootstrap 힘 **⟨σ⟩ ≈ MAE/3 = 과소확신**, dropout **⟨σ⟩ ≥ MAE = 보정 양호** | ⛔ **없다** | ⭕⭕ **M2 와 우승자가 반대로 나온다** ⇒ 우리도 **둘 다** 봐야 한다. 하나만 보고 *"우리 σ 는 쓸 만하다"* 라고 쓰면 이 논문이 이미 반증한 종류의 주장 |
| **M4 coverage** | DFT 참값이 ±1σ 안인가 (`Fig. 8`, 정성) | ⛔ 없다 | 🟡 우리는 참값이 드물어 적용 제한 |
| **M5 외삽 추적** | ★ **오차곡선 vs σ띠를 외삽좌표에 겹치고 PCA 내삽영역을 음영** (`Fig. 11`·`Fig. 13`) | ⛔ 없다 | ⭕⭕⭕ **우리 판 = x축을 온도(600/800/1000 K) 또는 PCA 거리로.** *"σ 가 고온 외삽을 따라가는가"* — **§J-2 [Zhang npj] 1050 K 골격융해 경고의 감시 지표** |
| **사후 보정** | **일부러 안 함** (raw ensemble spread) | 해당 없음 | ⚠ 우리도 raw 로 시작하되 **"보정 안 했다"를 명시** |
| **비용 보고** | ⛔ 벽시계·GPU 시간 **0건**. 정성 결론 하나: **snapshot ≈ random-init 인데 학습 1회 vs 100회** | 추론 3회(3모델) | ⭕ **fine-tune 하면 snapshot 이 공짜** — 체크포인트 저장 한 줄 |
| **단일 파운데이션 모델 적용성** | 논외(4종 다 자체 학습) | **UMA 단일** | 🔴 **bootstrap·random-init 불가**(OMat24 훈련셋 부재) · **MC dropout 조건 불일치**(UMA 는 dropout 학습 아님) · **snapshot = fine-tune 시 가능** · **PCA 외삽 진단 = DFT 0회로 지금 가능** |

**🔴 이 편이 닫지 못하는 것 — 반드시 같이 인용**
1. **계가 탄소 단일원소**다. 다원소·이온성·**부분점유 무질서**계로의 전이는 **시험된 적 없다**.
2. **훈련셋 4,788구성**으로 좁다 ⇒ 파운데이션 모델의 내삽영역과 **자릿수가 다르다**.
   기구(외삽하면 σ 가 먹통)는 전이 가능성이 있어도 **빈도·문턱은 전이되지 않는다**.
3. **MD 를 안 돌린다** ⇒ **궤적 시간평균 `D`·`Ea`·NE `σ_ionic` 의 UQ 를 다루지 않는다.**
   → **`imbalzano2021_committee_uq_md_thermodynamic_averages` 가 그 층위의 정본.**
   ⚠ 부분 다리: diamond **포논**에서 *"wide uncertainty bounds fail to capture the true values"*
   = *"힘 σ 가 괜찮아도 유도량에서 깨진다"* — **정성 경고로만**, 정량 이식 금지.
4. **OOD 프로브가 부피 스캔 한 축**뿐. **우리 위험(고온 무질서·Li 도약 안장점·계면)을 대표하지 않는다**
   ⇒ `E(a)` 스캔을 LPSCl 로 그대로 베끼면 안 된다(그리고 무질서계는 **배열 선택·집계 규칙을 카드에 먼저** 선언).
5. **오차막대가 없다.** `Fig. 7a` 의 0.31 vs 0.34 차이는 유의성 불명. **0.76 vs 0.30–0.40 만 인용한다.**
6. **테스트셋으로 모델을 선택하고 그 테스트셋으로 채점**했다(검증셋 없음) ⇒ ID 성능에 낙관편향.

**⛔ 이 축에서 인용하면 안 되는 것 (→ §J-6 에도 추가)**
- ⛔ *"이 논문이 committee(단순 앙상블)가 제일 낫다고 했다"* — **아니다. 승자를 못 정했다.**
  *"복잡한 추정기가 단순 committee 를 일관되게 못 이긴다"* 는 **[37] Carrete 2023** (*J. Chem. Phys.* 158, 204801)
  의 결론이고 이 논문은 그걸 **인용**했을 뿐이다.
- ⛔ *"이 논문이 GP·conformal 과 비교했다"* — **앙상블 4종만.**
- ⛔ *"이 논문이 D·이온전도도의 UQ 를 다뤘다"* — **MD 를 안 돌린다.**
- ⛔ **힘 RMSE 3.35–5.56 meV/Å**(탄소·ACSF-MLP·PBE)를 **우리 UMA Li₃PS₄ 30.0 meV/Å**(황화물·등변 GNN·PBEsol)
  와 같은 표에 놓는 것 — **단위만 같고 계·기술자·functional 이 전부 다르다.**

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_kurniawan2025_comparative_ensemble_uq_nnip.md` ## ③ .</sub>


**[Liu26FIRE] `liu2026_ai_ready_finetuning_solid_solid_interfaces` — 계면 MLIP 파인튜닝 레시피**
(⚠ **arXiv preprint, 동료심사 안 됨** · **SI 미확보** · **계면 물성 검증 0건**)

| 항목 | [Liu26FIRE] 가 답하는가 | 우리 현재 | 판정 |
|---|---|---|---|
| **★★ 계면 구조를 어떻게 만드나** (격자정합·변형률·종단·배향·gap·표본수) | ❌ **본문에 0줄** (`strain`/`lattice`/`termination`/`slab`/`vacuum` 전부 0회) | `run_cathode_interface.py` — SE 를 NCM xy 에 **한쪽 몰빵 변형**, `GAP=2.5 Å` 고정, `VACUUM=30 Å`, xy-shift 5 seeds, strain 0.2/1.1/3.3 % | 🔴 **B2 에 이식할 항목 0개.** 이 편은 *"계면을 어떻게 짓나"* 가 아니라 *"지어진 계면에서 프레임을 어떻게 고르나"* 를 푼다 |
| **B2 미정의(회신 BJ) 를 닫아 주나** | ❌ | `X_B2(M) = W_ad(NCM‖LPSCl:M) − W_ad(NCM‖LPSCl)` = 🔴 **미정의** (admissible state 다수·선택규칙 없음·`rng` 미지정으로 `Wad_std` 재현 불가) | 🔴 **안 닫힌다.** 🔵 단 **"고르지 말고 분포로 정의"** 방향은 얻는다 → `median{W_ad} ± MAD, n=k` + strain 배분·gap·종단을 **결과 보기 전에 선언** |
| **★★ 계면에서 무엇을 검증하나** | 🔴 **힘·에너지 RMSE 에서 멈춘다.** W_ad·계면저항·계면 Li 이동 전부 0. **계면층/벌크층 분리 RMSE 도 없다** | `adhesion.json` γ_SE 1.211 J/m² · Wad v2 1.107±0.027 | 🔴 **대조군 없음.** ⇒ **우리가 계면 MLIP 을 하면 `RMSE(계면층)/RMSE(벌크층)` 분리 보고를 반드시 넣는다** (이 편의 최대 결함을 우리가 피하는 방법) |
| **★ 계면 fine-tune 이 필요한가 / UMA 를 그냥 믿어도 되나** | 🔴 **답 없음.** **UMA·fairchem·OMat 0회**. 게다가 **MACE-MP-0 zero-shot 의 계면 오차 자체를 안 쟀다** (`Reference` 막대는 **문헌의 다른 전용 MLIP** 값) | UMA-s-1p1(omat) — **벌크 규약으로만** 검증, 계면 미검증 | ⛔ *"파인튜닝 없이는 계면에서 못 쓴다"* 인용 불가. 🔵 **약한 방향 신호**: 6계 중 **황화물 2계가 파인튜닝 후에도 최악**(43·54 meV/Å) ⇒ 황화물 계면이 이 종류 모델에 어렵다. **우리 계는 직접 재는 수밖에**: `force_contrast`(UMA/MACE/SevenNet M=3)를 **계면 구조에서** 돌리는 것이 GPU 0 에 가장 가까운 진단 (⚠ grasselli2025 판정대로 **epistemic 이 아니라 오설정 대조**) |
| **★ 필요한 라벨 수** | ✅ **여기는 답이 있다**: 종잣값 **20–50** perturbed → 후보 풀 **~20,000**(라벨 불필요) → 최종 **500–4,000 프레임**. 수렴은 계 의존(단순 500 / 다상 1000–2000) | 계면 라벨 캠페인 없음 | ✅ **실무 수치 확보**: **DFT 라벨 500–2,000점 + 종잣값 20–50점** |
| **★ GPU 비용** | 🔴 **답 없음** — 하드웨어 미기재, **DFT 라벨링 비용 부재**. 있는 것은 파인튜닝 **13–18 h @ n=4000** 과 표본추출 **2–3 min**(=**0.3–0.4 %**) 뿐 | — | 🔴 **예산 산정 불가.** ✅ 얻는 것: **표본추출은 공짜** |
| **능동학습** | ❌ 안 씀. 결론의 미래과제 한 문장뿐 | `force_contrast` M=3 | ✅ **우리가 오히려 앞선다** (grasselli2025 §4.1 축) |
| **replay (이 편의 유일한 알고리즘 신규성)** | ✅ **6계 전부에서 vanilla 보다 낫다** (E 1.2–3.4× · F 1.2–2.0×), 통제된 A/B | 파인튜닝 안 함 | 🔵 **우리가 언젠가 파인튜닝하면 replay 는 기본값으로 넣는다** ⚠ **replay 비율이 논문에 없다**(SI) |
| **SOAP→PCA→K-means 표본추출** | ✅ 레시피 명확 · 비용 0.3–0.4 % · ⚠ 하이퍼(r_cut/n_max/l_max/PC수/k) **전부 미기재** | 없음 | 🔵 **바로 이식 가능**(의존성 `dscribe` 1개). **커버리지 그림(전체 풀 회색 + 선택 표본 색)** 은 우리도 즉시 그릴 수 있는 유일한 "학습셋 대표성" 시각화 |
| **규모 상한 (우리가 인용 가능한 유일한 정량)** | ✅ MLIP **3456 원자** / DFT-MD **~576–600 원자**(메모리) · MACE 1.3→1.4 s/step vs VASP 1.0→195 | 우리 계면 슬랩 300–624 원자 | ✅ **우리 셀 크기가 DFT 한계 바로 위**라는 것을 외부 수치로 방어 가능 ⚠ 16 원자에선 VASP 가 더 빠르다(교차 30–60) |
| **우리 계와의 겹침** | Li‖Li₆PS₅Cl(우리 comp1 + Li 금속) · Li₃PS₄‖Li₃B₁₁O₁₈(황화물‖**붕산염 코팅** = 우리 B₂O₃ 축) | Stage 11 = **황화물 SE ‖ 산화물 양극(LiNiO₂)** | 🔴 **우리 주축(SE‖NCM)은 이 논문에 없다** |

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_liu2026_ai_ready_finetuning_solid_solid_interfaces.md` ### ②-c.</sub>


**[Liu26FT] `liu2026_finetuning_umlip_tutorial` — U-MLIP fine-tuning 절차의 실무 원전 (MACE 전용)**
(⛔ 우리 계 물성값 0건. A–D 4축 행 금지. 아래는 **절차·수치 규모·판정**뿐이다.)

| 항목 | [Liu26FT] 가 주는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| **다루는 모델** | MACE-MP-0b3 · MACE-MPA-0 · MACE-OMAT-0 (**셋뿐**) | **UMA-s-1p1 (omat), fairchem, 고정 체크포인트** | 🔴 **아키텍처 불일치.** `UMA` 는 Table I 한 줄, 실험 0건. ⚠ **MACE-OMAT-0 ≠ UMA** |
| **fine-tune 실행 가능성** | `run_train.py` 가 `model_foundation.r_max`·`.interactions[0]` 를 읽고 MACE 블록에 가중치 복사 | UMA = eSEN 체크포인트 | 🔴 **아키텍처 하드락. 이 도구로 UMA fine-tune 불가** (repo 실측) |
| **옮길 수 있는 것** | 데이터 준비(extxyz·90/10·`IsolatedAtom` E0s·rattle 0.1–1.0 Å+MC 필터·2단계 부트스트랩·1–2원자 셀로 반발영역) · **힘 가중을 크게** · lr 1e-3 근처 U자 · batch ≤20 · **RMSE 로 끝내지 말고 물성으로 재검증** | — | ✅ **레시피는 전부 이식 가능** |
| **못 옮기는 것** | `--swa_*`·`--freeze`·`--lora*`·`--pt_train_file`·`--num_samples_pt`·`start_swa=max_epochs//4*3` 자동규칙 | — | 🔴 MACE 종속. fairchem 쪽을 **따로 확인해야 한다**(이 논문은 무언) |
| **힘 RMSE 규모** | LGPS **fine-tune 후 14.88–16.15 meV/Å** (Table IV, 소환값) | `mlip_bench_li3ps4_uma.json`: **44.58 meV/Å**(zero-shot, Li₃PS₄ 243구조) | ⚠ **직접 비교 금지**(계·DFT설정·테스트셋 전부 다름). 자릿수만: **44.58/15.3 ≈ 2.9×** (digest 계산) |
| **zero-shot 출발점** | Si OOD **126.07** · LiCl/GaF₃ **179.2** · C/cBN **171.3** meV/Å | 우리 **44.58** meV/Å | ✅ **우리 출발점이 그들보다 훨씬 좋다** ⇒ 🔴 **그들의 9–10× 개선을 우리에게 기대하면 안 된다.** 상한은 **≈3×** |
| **fine-tune 이득의 조건** | 에너지: 전 구간 ✅ / **힘: 데이터 ≲30% 일 때만** — 75·100% 에선 **scratch 가 이긴다**(Fig. 4b figure-read) | — | 🔴 **본문 주장(*consistently*)이 자기 그림에 반증됨.** 갈라 인용 |
| **필요 라벨 규모** | ≈590 프레임(풀의 10%)에서 힘 RMSE ≈18.3 meV/Å; 5895 프레임(100%)에서 ≈14.85 = **10× 데이터로 19%** | Cl 라벨 **0** | 🔵 **파일럿 규모 근거 확보.** ⛔ **우리는 Cl 라벨이 없어 시작선에도 못 서 있다** |
| **탄성 연화 (PES softening)** | 파운데이션 **C₁₁ −45%·C₄₄ −52%·B −20%**(Mo, Table VI) → FT 로 회복 | 우리 E_VRH·B₀ 는 **DFT** 산출 | ✅ **DFT 값은 fine-tune 과 무관 — 안 끊긴다.** 이 행은 *MLIP 의* 연화 경고로만 |
| **연화 교정의 방향** | GSFE: 파운데이션 −60% → **FT 는 +12~14% 과대**(figure-read, Fig. 7) | — | 🔴 **"되돌린다"가 아니라 "지나쳐 되돌린다".** 슬 8 A1 인용문 수정 필요 |
| **일반화 저하(=우리 3번 질문)** | ⛔ **재지 않았다.** Si "OOD" 는 **구조** OOD(훈련·테스트 모두 Si). 사전학습 분포 되돌림 평가 **0건** | +B₂O₃ · Nd–O 공도핑 결과 다수 | 🔴 **우리에게 제일 치명적인 결측.** B/O/Nd 는 진짜 **화학** OOD ⇒ **대가를 우리가 직접 재야 한다** |
| **대가 측정기** | 없음 | `mlip_bench_li3ps4_uma.json` 243구조(Cl 없음) | 🔵 **우리는 이미 갖고 있다** — fine-tune 후 이 셋으로 되돌려 재면 그게 곧 forgetting 계측 |
| **M ≥ 4 committee** | 파일 최대 150개 가능하나 **EMA 평활 · 100-epoch 간격(→최대 2개) · stage1/2 목적함수 불일치 · 순환 LR 부재** 로 준독립성 4중 위반 | `force_contrast` M=3 (이종) | 🔴 **`grasselli` 식 (27) 의 M≥4 출구가 이 문서로는 안 열린다.** 400+ epoch·EMA off·순환 LR 이라는 **별도 설계**가 필요 |
| **학습 비용** | ⛔ **wall-clock 0줄.** step 수만 digest 계산 ≈2.2×10⁵ | — | 🔵 파일럿 첫 측정항목 = **우리 GPU 의 1 step 시간** |
| **MD 추론 가속** | cuEquivariance: 2900원자 **1.94×**(5084→2619 s/10k step), scaling 0.76→0.41. **128원자에선 더 느림** | 우리 셀 400–1000원자 | ✅ **이득 구간 안**. ⚠ 논문 본문의 *"3–10×"* 는 자기 표와 안 맞음 |
| **비교군 보존** | Table IV 에 **zero-shot 행이 없어** LGPS 개선폭을 알 수 없다 | — | 🔵 **우리는 반복하지 않는다** — fine-tune 전 대조 잡을 먼저 돌린다 |

**⛔ [Liu26FT] 에서 인용하면 안 되는 것**
1. **절대 에너지 RMSE 전부** — Fig. 2(2.4–3.2 meV/atom)와 Table IV/V/X(0.25–0.35)가 **정확히 10× 어긋나고**
   PDF 로 어느 쪽이 옳은지 확정 불가. **상대 개선폭(10.7% 등)만** 쓴다.
   (특히 LiCl/GaF₃ 의 **0.09 meV/atom** 은 DFT 수렴오차보다 작아 물리적으로 의심스럽다.)
2. *"이 튜토리얼로 UMA 를 fine-tune 할 수 있다"* — **UMA 실험 0건 + 아키텍처 하드락**.
3. *"fine-tuning 은 항상 scratch 보다 낫다"* — **Fig. 4b 가 75·100% 힘 RMSE 에서 반증**.
4. *"fine-tuning 이 일반화를 향상시킨다"를 우리 B₂O₃/Nd 계열에 적용* — 그 근거는 **동일 원소 내 구조 OOD**뿐이다.
5. Table VI 의 **본문 퍼센트**(45.91/56.88/48.27→2.58/14.77/3.45) — 기준(실험)이 표(DFT)와 다르고
   **표에 실험 열이 없으며** C₄₄ 는 오타로 보인다. 인용하려면 **표의 DFT 기준 열**을 쓴다.
6. Table VII 의 GSFE 오차를 **"개선"으로만** 서술 — 부호가 뒤집혀 **과대평가로 넘어간 것**이다.
7. 논문의 *"cuEquivariance 가 3–10× 빠르다"* — 자기 Table VIII 실측은 **최대 1.94×**.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_liu2026_finetuning_umlip_tutorial.md` ## ② .</sub>


**[Maginn19MD] `maginn2019_best_practices_transport_selfdiffusivity_viscosity` — 우리 D 의 *통계* 불확실도를 정의하는 원본**

> ⛔ **σ·Ea·D·ESW·탄성·gap 0건.** 여기 있는 것은 우리 `Ea 0.197 ± 0.032 eV` 의 **±0.032 가 무엇인가**를 정의하는 원본이다.
> ⛔ **형제 4편(#78–81)과 재는 양이 다르다**: 저 넷은 **모델(epistemic)** 분산, 이 편은 **궤적 유한성(random)** 분산.
> **복제를 무한히 늘려도 모델 편향은 안 줄어든다** — 논문 §4.2.3 첫 문단이 힘장에 대해 직접 그렇게 쓴다.

| 항목 | [Maginn19MD] | 우리 | 판정 |
|---|---|---|---|
| **MSD 적합 구간** | *"only the **middle**"* · 단시간(케이지)·장시간(잡음) 배제. **⛔ 수치 기준 없음** — *"we are unaware of an objective approach"*. 대신 **보고 3종**: 선택법 · **그 선택이 만드는 D 변동폭** · 기울기 적합 불확실도 | **2–50 ps 고정 · 자유절편 OLS** | 🟡 **절반**. 취지 일치·자유절편 ✅. 그러나 **변동폭을 안 보고한다** — 우리는 그 값을 이미 안다(**창 효과 Ea 242 meV**, `tools/convention_check.py` · `kb/concepts/msd_reading.md`) ⇒ **242 meV > 주장 효과 90 meV** 인데 규약 고정으로 처리했다. ⛔ **논문을 우리 창의 근거로 인용하면 오독** |
| **자유절편 vs 원점강제** | `Table 1`: `D = (1/2d_α) lim (d/dt)⟨MSD⟩` — **미분형** | 자유절편 OLS `MSD = c + 6Dt` | ✅ **직접 방어된다.** 도함수는 절편을 안 본다 ⇒ `MSD/(6t)` 원점강제가 규약 위반 (2026-08-11 β 게이트 사태의 뿌리와 같은 병) |
| **독립 복제 수** | 부트스트랩 **N_reps ≥ 20** 에서 최신뢰 · SEM ∝ 1/√N · **10 ≈ 단일 장기런** · **30–40 ≡ 100**(점도) | **시드 3** | ⛔ **미달.** 산술 결정타: **시드 3 → 복원추출 다중집합 10가지** ⇒ "수백 회 반복" 해도 분포가 아니라 이산 점 10개. **논문식 복제 부트스트랩은 시드 3에서 실행 불가.** ⚠ 완화: 저자가 *"even if only a few"* 를 허용(단 *rough estimate* 로 부를 것) + D 는 **N 분자 평균**이 가능해 η 보다 정밀(§4.2.1) — ⛔ 그래도 **분자 평균은 복제를 대체 못 한다**(같은 궤적·같은 열욕·같은 무질서 배열 = 독립 표본 아님) |
| **확산영역 진입 판정** | ① **log-log MSD 기울기 ≈ 1** ② **√MSD > r_G(하한) · > L/2(상한)** (⚠ 문서 내 세 곳이 L/2 · "~L" 로 불일치) ③ 점점 긴 런 계열로 D 변화 확인. **"ergodicity" 단어 0회** | **β 게이트 폐기 후 공백** | ⛔ **가장 큰 구멍이자 가장 싼 수리.** ①은 **비용 0** — 기존 MSD 로그에서 계산. ⭕ **처방(T1)**: `tools/ionic/msd_diffusive_check.py` 에 `slope_2_50ps` 한 열 추가 (**새 파일 금지** — 기존 도구 확장). ②는 r_G 가 단원자 Li 에 없어 **그대로 못 온다** → 하한을 Li–Li 최근접/점프거리로, 상한을 L/2 로 치환 ⚠ **이 치환은 우리 판단이지 논문 권고가 아니다** |
| **유한크기 효과** | **"significant … must be accounted for"**. CO₂ ≈10 %. ① D vs N^(−1/3) 외삽 ② **YH `D∞ = D(L)+k_BTξ/(6πηL)`, ξ=2.837298** (입방 + η 별도) | **점검 0회** | ⛔ **명시적 결손.** 단 **YH 직접이식 ❌**: 식이 η 를 요구하는데 결정성 SE 의 "전단점도" 는 잘 정의되지 않고, 보정의 물리가 **유체역학 backflow** 라 골격이 운동량을 흡수하는 우리 계에 전제가 안 선다. ⭕ **처방(T2)**: 600 K 에서 host·design 각각 **2×2×2 / 3×3×3** 두 크기만 → 목표는 D∞ 가 아니라 **D_rel 이 크기에 둔감한지** 확인 |
| **thermostat** | **NVE > NVT ≫ NPT.** 속도 스케일링(Berendsen·SR·NH)은 τ 0.1/1/10 ps 전 범위에서 NVE 와 구분 불가. ⛔ **속도 무작위화(Andersen·Langevin) + 강결합(τ = 0.1 및 1 ps) → D 극적 감소·η 증가** | **Langevin NVT, `friction=0.02`(ASE 단위) ⇒ τ ≈ 0.51 ps** | ⛔⛔ **이름을 대서 경고받은 조합.** ⚠ 근거는 **분자 액체** 기준이라 고체 hopping 으로의 전이는 미검증. ⚠ 우리 보고량이 **비**라 곱셈 편향이 상쇄될 여지가 있으나 **증명된 적 없다**. ⭕ **처방(T3, 최저비용)**: 600 K 에서 γ = 0.002/0.02/0.2 **대조 잡** — D 는 움직이는데 **D_rel 이 안 움직이면** 상쇄 가정이 실측으로 뒷받침된다 |
| **런 길이** | §4.3: **점점 긴 런의 계열**로 D 가 변하는지 본다. `Fig. 4`: **느린(저온) 계일수록 창을 늘려야** | prod 200 ps(600 K) / 100 ps(800·1000 K), 창은 **양쪽 다 2–50 ps** | 🟡 **판정 불가 — 점검을 안 했다.** ⚠ 800/1000 K 에서 상한 50 ps 는 **런의 T/2** (⚠ `lag ≤ T/4` 는 **우리 kb 관례**이지 이 논문 규칙이 아니다 — 논문의 "절반 이하"는 §5.3.2 의 *GK 시간원점 lag* 얘기다) |
| **시간원점 다중화** | 식 정의의 일부(`⟨…⟩_{t₀}`). 전제: **δt₀ > 상관시간** | 하고 있다 (`msd_origin.py`) | ✅ 축은 있다. ⚠ **δt₀ > 상관시간 확인 기록이 없다** |
| **3차원 평균의 덤 진단** | `D = ⅓(D_xx+D_yy+D_zz)`, **세 성분 산포 = crude 불확실도**, 비대각 ≈ 0 확인 | 평균은 하되 **산포를 안 본다** | ⭕ **공짜 진단 미수확 (T0)** — 후처리만으로 시드 3에서도 즉시 얻는 불확실도 하한 |
| **비(ratio) 의 불확실도** | ⛔ **다루지 않는다** (비·상대확산 언급 0건) | 보고량 = `D_rel = D*(design)/D*(host)` @600 K | ⚪ **논문 밖.** digest §9 의 **paired bootstrap**(design·host 에 같은 시드 집합 `S_b` 를 적용해 매 반복 `R_b` 를 만들고 2.5/97.5 백분위) 은 **§4.2.3+§6.3.1 의 우리 확장**이며 그렇게 표기해야 한다. 독립 가정 오차전파는 **공통 성분을 두 번 세어 CI 를 과대추정**한다. ⚠ 짝짓기 전제 = design 시드 k ↔ host 시드 k 대응 (`aimd_mlip.py` 는 `seed = args.seed + T_K` — 같은 `--seed` 로 돌렸는지 **미확인**) |
| **창 민감도 × 복제 수** | `Fig. 13` figure-read: N_reps 1 → 30 에서 **창이 만드는 산포 ≈0.8 → ≈0.06 ×10⁻³ Pa·s (≈13배 축소)**. 단일런에서는 **음의 점도**까지 나온다 | 창 고정 + 시드 3 | ★★ **이 논문의 최대 소득.** *"창을 어떻게 고르나"* 와 *"복제를 몇 개 돌리나"* 는 **한 질문**이다. ⭕ **처방(T4)**: 창 자체는 두고 **시간구간 부트스트랩**(§6.3.1) 을 MSD 에 이식 — start ∈ [1,10] ps, end ∈ [30,60] ps 를 수백 회 무작위 추출해 **D_rel 분포**를 내고 2.5/97.5 백분위 보고. **새 MD 0회, 후처리만.** ⚠ 그 CI 는 "통계 + 창 선택" 합산폭이므로 그렇게 이름 붙일 것 |

**⛔ 이 축에서 인용하면 안 되는 것 (`J-6` 에도 반영 권장)**
- *"Maginn et al. 이 2–50 ps 창을 권고한다"* / *"우리 창은 Maginn 규약을 따른다"* — **거짓.** 논문은 창 수치를 주지 않는다.
- §6.3.1 의 *"5 to 50 ps"* 를 우리 2–50 ps 의 방증으로 쓰기 — **점도(Einstein η)** 얘기이고 저자가 *"less theoretically rigorous"* 라 깎은 관행이다. 숫자 일치는 물리적 관련이 없다.
- *"YH 보정을 적용했다"* — 우리 계에 적용 불가(위 표 참조).
- *"Maginn 규약대로 σ 를 냈다"* — **이온전도도는 이 편에 없다** (후속편 예고만).
- 시드를 늘려 CI 가 좁아진 것을 *"D 가 정확해졌다"* 로 쓰기 — 좁아지는 건 **통계 축뿐**이다.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_maginn2019_best_practices_transport_selfdiffusivity_viscosity.md` ### 2-b..</sub>


**[McC25D] `mccluskey2025_accurate_diffusion_coefficients_uncertainties` — D\* 추정기·오차막대의 정의 원본 (코드 실물 확보)**
(⛔ 물성값 LLZO D\* 1건뿐. A–D 4축 행 금지. 아래는 **절차**와 **우리 위치 판정**뿐이다.)

| 항목 | [McC25D] 가 정하는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| **적합 모델** | 직선 + **자유 절편** (`fit_intercept=True` 기본) | 직선 + **자유 절편** | ✅ **일치** |
| **회귀** | **근사 베이지안(≈GLS)**, Σ′ 사용 | **OLS** | 🔴 **핵심 격차** |
| **D 값의 편향** | OLS/WLS/GLS **중심값 동일** (`Fig. 1`·`Fig. S6`) | — | ✅ **우리 D 는 안 틀린다.** ⛔ *"우리 D 가 과대/과소"* 서술 금지 |
| **OLS 오차막대** | 자기 σ 를 **1/9–1/26** 로 보고 | 우리는 `stderr` 를 **안 쓴다** — 오차막대는 **시드 3개 산포** | ✅ **관행은 무사.** 시드 산포 = 논문이 *"정직하지만 비싸다"* 고 부른 그 방법 |
| **정밀도(효율)** | GLS 가 OLS 보다 σ 3.9–4.6배 좁음 | — | 🔴 **여기서 진다** (아래 두 행) |
| **MSD 시간원점** | **multi-origin 기본** (모든 원점 평균) | **single-origin** (정본 `msd_per_elem_A2`, `aimd_mlip.py::compute_msd_per_element`) | 🔴 **분산 8.7× 손실**(digest 계산). **MD 0 스텝으로 회수 가능** — `msd_multi_origin` 이 이미 있다 |
| **N′ᵢ (독립 관측 수)** | **겹치지 않는** 창 수 × 입자 수 = **N_atoms·N_t/i** | `msd_multi_origin` 이 저장하는 `norig = nt−L` = **겹치는 원점 수** | ⚠ **가중에 쓰면 짧은 lag 에서 독립성 최대 L배 과대계상.** 지금은 가중에 안 쓰므로 사고는 없다 — **쓰기 전에 고쳐라** |
| **총 손실** | — | (single-origin + OLS) | 🔴 **var 비 87×** ⇒ **우리 D 한 점 = kinisi 한 점의 1/87** (digest 계산, N=48 합성. **한 자릿수로만**) |
| **시드 수 — 정밀도** | 궤적 1개로 충분 | **3** | 🔴 **kinisi 1회의 1/29.** multi-origin 만 켜도 3 → *10 상당*. **정밀도 목적의 시드 증설은 가장 비싼 길** |
| **시드 수 — 추정** | 다루지 않음 | **3** | 🔴 [Gra25UQ] 식 (27) 이 **M≥4** 요구 + 3개의 sd 는 상대오차 **50 %** ⇒ `Ea 0.197±0.032` 의 `±0.032` 는 **±50 % 짜리 숫자**. **3 → 5 권고**(정밀도가 아니라 추정 때문) |
| **적합 창 하한** | LLZO **10 ps** (ballistic·subdiffusive 제거). **선택 규율은 안 준다** | **2 ps** | ⚠ **근거 약함.** `Fig. 3` 이 **i,j ≲ 5–10 에서 Σ′ 이 분산을 2배 이상 과대**함을 보인다 = 우리 하한이 그 구역. 우리 LPSOCl 600 K 절편은 **MSD@50 의 18.2 %** 인데 이 모델은 **절편 없는 자유확산** 전제 ⇒ **`start_dt` 2/5/10 ps 스캔 필요** |
| **적합 창 상한** | **없음**(궤적 끝까지). 논의도 없음 | **50 ps** | ✅ **정당하다 (우리가 메운 공백).** digest 계산: 같은 200 ps 궤적에서 kinisi 2–50 sd 1.63e-7 vs 2–200 1.77e-7 → **±11 % 안에서 구별 불가.** 단 **보고 σ̂ 는 좁은 창에서 더 보수적**(3.05× vs 1.46×) |
| **창 고정 규율** | *"set by the user"* — **규율 없음** | **전 계·전 온도 2–50 ps 고정** | ✅ **우리가 낫다.** [Kahle20] 의 물질별 custom 이 본문↔SI 불일치를 낳은 선례 |
| **분산 추정법** | **재스케일 채택 / 블록 재규격화 기각** (SI S-II: 블록은 잡음↑·**체계적 과소**) | (해당 없음 — 우리는 분산을 안 낸다) | 🔵 **[Kahle20] 이식 후보 강등**: 우리가 적어둔 *"블록 수 4/8/16 감도 점검"* 은 **애초에 열등한 추정기의 감도**를 재는 일 |
| **복제 궤적 합치기** | `dtype='identical'` → **N′ᵢ 합산** | 시드별 개별 적합 후 산포 | 🔵 **둘 다 내라.** 합산 = 정밀도, 산포 = 통계오차 추정. **서로 다른 것** |
| **Arrhenius** | `kinisi.arrhenius` — **D 분포 → Ea 분포**, `extrapolate(T)`, Arrhenius vs super-Arrhenius **베이지안 evidence** | 600/800/1000 K **3점 선형회귀** | 🔵 **이식 후보 1순위.** [Kahle20] 의 *"Bayesian Ea 오차"* 와 같은 방향이고 **여기엔 코드가 있다** |
| **σ(이온전도도)** | **안 한다** (D\* 만) | NE(Haven=1), **절대값 비인용** | ✅ **정신 일치.** ⚠ σ 로 넘어가면 Haven 계통오차가 통계오차를 압도 → **비인용 규율 그대로 유효** |
| **비(ratio) 전파** | 🔴 **안 다룬다** (*"ratio"* 는 `Fig. 3` 캡션 1회) | **보고량이 `D_rel`** | 🔴 **우리가 붙여야 한다.** ↓ 아래 별도 블록 |
| **불확실도 축** | [Gra25UQ] 분류의 **④ 표집/통계만** | `D_rel` 오차막대 | ⚠ **축 명시 필수.** ⛔ *"kinisi 썼으니 우리 D 가 믿을 만하다"* 는 오용 — **궤적이 옳다는 전제 위의 통계**다 |
| **이식 가능성** | MIT · pip · **from_ase** · numpy<2 · 5.2 s/궤적 | 기존 궤적 파일 존재 | ✅ **MD 0 스텝으로 즉시 가능.** 차단요소 2건은 회피법 확인됨 |

**★ 비(ratio) 전파 — 논문이 안 주므로 우리가 정의한다 (digest 계산으로 검증)**

design 과 host 는 **다른 궤적 = 독립** ⇒ 1차 전파는 **상대 표준편차의 제곱합**:
> **(σ[D_rel]/D_rel)² = (σ[D\*_des]/D\*_des)² + (σ[D\*_host]/D\*_host)²**

더 나은 방법 = **사후표본 나눗셈**(kinisi 가 D 를 3200 표본으로 준다. 각각 무작위 치환 후
원소별 나눗셈 → 비의 사후분포. 정규근사 불필요, 비대칭 꼬리 보존).

검증 (참 비 1.60, 독립 궤적쌍 12회, digest 계산):

| 항목 | 값 |
|---|---|
| 평균 r̂ | 1.6091 (편향 **+0.57 %**) |
| 진짜 산포 sd(r̂) | **0.0449 (2.79 %)** |
| 표본나눗셈 사후 sd | 0.0580 (3.6 %) → 보고/진짜 **1.29**(보수적, ±0.27) |
| 제곱합 검산 | 1.88 % ⊕ 2.28 % = **2.96 %** vs 관측 **2.79 %** ✅ |

**우리가 추가로 붙여야 할 것**
1. **`P(D_rel > 1)` 을 사후분포에서 직접 보고** — 비준 판정이 "1보다 큰가"이므로 이게 가장 정직한 보고량
2. **cell-conditioned 유지** — 같은 무질서 배열 안에서만 비를 만든다
3. **모델오차 축은 분리 표기** — `force_contrast` 를 이 σ 와 **합치지 마라**(다른 축, 상관 구조 미지)
4. **Arrhenius 는 `StandardArrhenius` 에 D 분포를 넘긴다**
5. ⚠ **σ(NE) 로 가면 이 오차막대는 무의미** — Haven=1 계통오차 지배

**⛔ [McC25D] 에서 인용하면 안 되는 것**
1. **LLZO D\* ≈0.9×10⁻⁵ cm²/s 를 우리 값과 나란히** — 다른 물질·다른 T(700 K)·**고전 힘장**(DIPPIM)이다.
2. **"부트스트랩"** — 논문에 그 단어가 0회. `MSDBootstrap` 은 레거시 작명이고 기본값은 리샘플링 없음.
3. **"AIMD/DFT"** — LLZO 는 **고전 MD**(METALWALLS+DIPPIM). 이 논문에 DFT 는 한 줄도 없다.
4. **`Fig. 6` 의 WLS/GLS 선을 "실무 성능"으로** — 512회 반복의 **수치 분산/공분산**을 쓴 **이상적 참조선**이다.
   실무 비교는 **OLS vs kinisi(초록)** 만 정당하다.
5. **σ̂/σ ≈1 을 우리 계에 그대로** — 검증계 2개가 **둘 다 Σ′ 가정에 유리**(격자 RW=가정 그 자체,
   LLZO=700 K 얕은 cage). **caged·느린 계 미검증.**
6. **digest 계산의 87× 를 "우리 실측"으로** — **합성 브라운 걸음** 값이다. 실제 cage 상관에서는
   multi-origin 이득(8.7×)이 줄 수 있다. **"수십 배"가 안전한 서술.**

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_mccluskey2025_accurate_diffusion_coefficients_uncertainties.md` ## ② .</sub>


**[Ren26] `ren2026_li2zrcl6_low_ion_potential_doping` §21 — aliovalent RE³⁺ 도핑 계산의 설계 규약 (⛔프리프린트·⚠할라이드, 값 이식 금지)**

| 항목 | [Ren26] 이 한 것 | 우리 `ndo_lpscl16` 규약 | 판정 |
|---|---|---|---|
| **치환 자리** | Zr⁴⁺(8면체) → Er³⁺/Nd³⁺, `Fig. 2a` 로만 제시 | Rietveld `Nd8@(½,½,½)` = **P⁵⁺(사면체) 자리**. ⚠ UMA 어닐 후 Nd 는 사면체를 못 지키고 **S 4–6 + Cl 케이지**로 풀린다 | ⚠ **비교 불가** — 배위수(6 vs 4)·반경비(1.36× vs **5.78×**)가 다르다. cf. `kb/methodology/name_vs_substance_2026_09_09.md` |
| **전하보상** | **화학식에 Li 추가, 중성 셀** (+1 Li/도펀트). 배경전하 없음 | **동일 방식** (+2 Li/Nd). 전하합 6구조 전부 0 | ⭕ **선례 성립 — 우리 스킴 유지** |
| **보상 Li 자리** | ⛔ **미기재.** 열거·SQS·선택규칙 0 | ⚠ **우리도 카드에 안 적혀 있다** (§3 위험요인은 O 배열 3종만 열거) | 🔧 **우리 할 일 (A)** — "Li 배치는 열거하지 않은 자유도"를 한계로 명시 |
| **4f 처리** | **open-4f + DFT+U**, U 값·스핀·NUPDOWN·점유행렬 정책 **전부 미기재** | **frozen-4f** (4f in core, z_valence 11) + **"Nd 4f 주장 전면 금지"** | ⭕ **우리 쪽이 방어 가능** — 같은 셀 안 ΔE 라 얼린 4f 가 상쇄된다. 그들 방식은 배열별 4f basin 차가 ΔE 에 수백 meV 가짜 신호를 넣어 **G3 컷(50 meV)을 무의미하게** 만든다 |
| **자성 상태 선언** | ⛔ 없음 | ⚠ 카드 §3 **"미판정 — nspin 을 못 박지 않았다"**(자칭 가장 약한 자리) | 🔧 **우리 할 일 (B)** — `scf.in` 6점의 `nspin`/`starting_magnetization` 동일성 확인 후 카드 기입. cf. SDCP phaseB "제약된 기준 ↔ 자유로운 대상" 사고 |
| **배열 선택 규칙** | ⛔ 없음 ("structural optimization" 한 줄) | **G1 6점 전부 · G2 두 셀 불일치 시 선택 실패 보고 · G3 <50 meV 구별 불가** | ⭕ **우리 장치가 정확히 그 공백을 막는다.** 이 편은 **G2·G3 의 존재 이유를 보여주는 외부 실증 사례** |
| **σ 파이프라인** | AIMD 50 ps · 600–900 K 4점 · **단일시드·배열 1개** · MSD 창 미기재 · 절편 미기재 · NE(Haven=1) → 300 K 외삽 | prod 200 ps · 600/800/1000 K 3점 · **멀티시드 판정** · **MSD 창 2–50 ps 고정** · **자유절편** · NE(Haven=1) | ⭕ Haven 규약만 같고 나머지는 우리가 엄격. **매 항목이 §21.6 의 순위 뒤집힘에 기여한다** |
| **⟨ω⟩ / VDOS** | 식만 정의, **값 0**. 3패널 정규화 불일치 · 질량 효과 미분리 | **축 자체가 없다** | 🔧 **채택 후보(중기)** — `tools/ionic/` UMA-MD 궤적에 **VACF→VDOS→⟨ω⟩**. ⛔ **질량 정규화를 처음부터** (우리는 P→Nd 로 ω ×0.463) + UMA 포논 검증용 QE-DFPT 스팟체크 1건 |

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_ren2026_li2zrcl6_low_ion_potential_doping.md` ### 2-2..</sub>


**[Tompa26FT] `tompa2026_finetuning_mlip_foundation_strategies` — *파운데이션 MLIP 를 어떻게 fine-tune 하는가* 의 원전**
(**arXiv 2606.12704v1** · 2026-06-10 · **preprint, 동료심사 전** · Cambridge MACE 그룹 + STFC + US NRL · **물성값 0**)

> 🔑 **우리가 이 편에서 가져오는 것은 값이 아니라 "레시피와 그 대가"다.**
> 그리고 **벤치마크 5계 중 첫 번째가 Li₆PS₅Cl** 이라서, 드물게 **우리 계로 직접 잰 방법론 수치**가 있다.
> ⚠ 다만 §2.1 이 *"LPSC 는 OMat24 에 흔한 종류라 이 계만으로는 방법 간 구분이 어려울 것"* 이라고 **미리 못박는다**
> — **우리 계는 이 논문에서 "차이가 제일 안 보이는 자리"** 다.

| 항목 | [Tompa26FT] | 우리 (UMA-s-1p1 omat, 고정 체크포인트) | 판정 |
|---|---|---|---|
| **엔진** | MACE (등변 MPNN), 4.7–9.1 M 파라미터 | **UMA-s-1p1**, fairchem | ⚠ **아키텍처가 다르다.** 저자 명시: *"모든 실험이 MACE … 타 아키텍처 일반화는 미검증"* ⇒ **결론 직수입 금지** |
| **사전학습 도메인** | **OMat24**(주) vs MPTraj(비교군) | **OMat24 계열**(omat task) | ⭕⭕ **우리가 좋은 쪽에 있다.** `Fig. 3a`: 우리 계에서 MPTraj계 F MAE ≈0.105 vs OMat계 ≈0.045 eV/Å (`figure-read ≈`, **2–3배**) |
| **fine-tune 여부** | 7전략 비교 | **0회** | 🔴 우리는 `Fig. 17` 의 **`OMat (found.)` 회색 violin** 자리. **이 논문 권고 #1 을 이미 충족** |
| **fine-tune 의 이득 (우리 계)** | argyrodite OOD **F MAE ≈0.043 → ≈0.030 (30%)** · **E MAE ≈1.8 → ≈1.6 meV/atom (거의 0)** | — | 🔴 **이득이 작다.** 500 PBE 점을 써서 30% |
| **fine-tune 의 대가 (우리 계)** | **비-argyrodite F MAE ≈0.045 → naive ≈0.075 (1.7배 악화), 꼬리 0.08→0.24** | 우리 **+B₂O₃ · Nd–O** 가 그 방향 | 🔴🔴 **"기존 결과와 비교가 끊긴다"의 정량.** ⇒ **plain LPSCl 로만 fine-tune 하면 도핑계가 나빠질 수 있다** |
| 그 대가를 없애는 법 | **pseudolabel replay** → 비-argyrodite ≈0.042 로 **파운데이션 수준 유지** | — | ⭕ **replay 면 끊김 ≈0.** 비용 = 학습 compute **3–15배** |
| **replay 데이터 조달** | `Fig. 15`·Appendix E: **원소일치 OMat24 / 무작위 MPTraj 10k / 결합 = 전부 동일**, 라벨은 파운데이션이 자체 생성 | OMat24 원본 미보유 | ⭕⭕ **원 사전학습 데이터 없이 된다.** 우리에게 결정적 |
| **필요 라벨 수** | **LPSC 500(PBE, 단일조성)** · ice MD안정 **25** · NaCl RDF **96 에서 포화** · Sɴ2 **60** | `mlip_bench_li3ps4_uma.json` = **243 구조** (⚠ `elements: [Li,P,S]` — **Cl 없음**) | 🟡 **자릿수가 같다.** 단 **Cl 포함 라벨을 새로 만들어야** 한다 (새 계산 ⇒ **보고량 카드 먼저**) |
| **E₀ (원자기준에너지)** | **model-aware reestimation** (식 6) 필수. **averaging 금지** — force RMSE 2–3배 악화, 게다가 **단일조성이면 rank-deficient** | `mlip_bench_li3ps4_uma.json` 이 **선형 원소보정**(Li 0.09312 / P 0.03104 / S 0.12416 eV/atom, **fit R² 0.620**) 사용 = **바로 그 averaging** | 🔴 **우리가 지금 쓰는 방식이 이 논문이 금지한 것.** ⭕ **식 (6)은 아키텍처 무관 ⇒ UMA 에 즉시 이식 가능** — **이 논문에서 우리가 바로 쓸 수 있는 유일한 수식** |
| **MD 안정성 판정** | ①정온 **250 ps** 완주 ②**50→800 K 램프 50 ps** (`Table 1`) | MSD 창 **2–50 ps**, 600/800/1000 K | ⭕⭕ **우리보다 훨씬 긴 완주시험.** `Table 1` 은 *"검증 RMSE 정상 + MD 붕괴"* 를 E₀ 하나로 만들어낸 사례 ⇒ **b₂o₃ creep 과 같은 계열** |
| **PES 병리 진단 (RSS)** | PyXtal 10조성×50 = **500구조**, relax–rattle **3회**, 4기준. 파운데이션 **0.1 GPa 8.6% · 50 GPa 10.0%** | ⛔ **없다** | ⭕⭕⭕ **DFT 0회로 지금 실행 가능한 최우선 이식 항목** |
| **"더 학습하면 더 낫다"** | ⛔ **틀린다.** replay 없는 방법은 **데이터↑ 이면 PES hole↑** (naive 50 GPa 9.4→34.4%, LoRA 7.8→**57.4%**) — **in-domain 정확도는 개선되는 와중에** | — | 🔴 **우리 직관과 반대. 규율로 박을 것** |
| **ZBL pair repulsion** | **전 모델에 명시적으로 들어 있는데도** 구멍 발생 ⇒ **many-body 반발 기여의 붕괴** | — | ⚠ *"단거리 항 넣었으니 안전"* 이 성립 안 함 |
| **UQ / 앙상블** | ⛔ **전혀 없다** (`snapshot` 0 · `uncertainty` 0 · `committee` = 참고문헌 제목만) | 이종 committee **M=3** | 🔴 **이 편은 UQ 논문이 아니다.** M≥4 경로는 우리가 **유도**한 것 (아래) |
| **수송계수(D·Ea·σ)** | ⛔ **없다.** MD 를 돌리지만 안정성·RDF 만 | 우리 보고량 본체 | 🔴 **층위가 다르다** → `imbalzano2021_…` 가 그 층위 정본 |

**🔗 UQ 3편과의 접속 — 우리가 유도한 것 (논문 주장 아님)**

| 물음 | [Tompa26FT] 가 주는 것 | 판정 |
|---|---|---|
| **M≥4 를 채울 재료가 생기나** | 🟡 **간접**. 학습이 **수백~1000 epoch**(`Fig. 12` 2단계 전환 = epoch 500) ⇒ 100-epoch 간격이면 5–10 스냅샷. **aq. NaCl 에서 seed 1–3 이 실제로 돌아갔다**(`Table 4`) | **시드 다중 fine-tune 이 가장 방어 가능** |
| 시드 산포는 얼마인가 | `Table 4` NaCl F RMSE: **42.44±5.28 / 43.79±5.03 / 41.54±4.76 meV/Å** ⇒ **std ≈ 평균의 10–12%** | ⚠ 이건 **재현성 산포**이지 UQ 용 σ 가 아니다 |
| 🔴 **방해 요소는 없나** | **있다 — EMA.** `Table 7` EMA decay **0.999(naive) / 0.9999(multihead)**. 0.9999 ≈ 최근 10⁴ 스텝 평균 ⇒ **스냅샷들이 서로 거의 같아진다(유효 M→1)**. 그런데 논문은 **EMA 를 올리는 것이 안정적 fine-tuning 에 필수**라고 한다 | 🔴🔴 **"정확도용 설정"과 "UQ용 설정"이 충돌한다.** 이 긴장은 **tompa 에도 UQ 3편에도 없다 — 우리가 새로 세운 것** |
| Grasselli 식 (27) 의 독립추출 조건을 만족하나 | ⛔ **어느 논문도 판정 안 함** | 🔴 **열린 질문으로 남긴다** |

**🔴 이 편이 닫지 못하는 것 — 반드시 같이 인용**
1. 🔴 **동료심사 안 됐다** (arXiv v1). 게재본에서 수치·그림이 바뀔 수 있다.
2. 🔴 **전 실험이 MACE 다.** 저자 스스로 한계로 적음 ⇒ **UMA 이전성 미검증**.
   그리고 **LoRA·pseudolabel replay·E₀ reestimation 의 구현은 `ACEsuit/mace` 3.15+ 전용**,
   **fairchem 대응물은 이 세션에서 확인 못 했다.**
3. 🔴 **`Fig. 10` 의 축 단위가 패널 간 1000배 어긋난다**(a: meV/Å · b: eV/Å, 두 값 모두 알려진 MACE-OMat
   힘오차와 안 맞음) ⇒ **forgetting 은 "파운데이션 대비 배율"로만 인용**.
4. 🔴 **`Freeze (5)`/`Freeze (6)` 라벨이 §2.3 의 두 정의와 매핑되지 않는다.** 한쪽은 `Fig. 11` 최악(+40.8%p)인데
   본문은 *"readout-only 는 반발벽을 보존한다"* 고 쓴다 ⇒ **Freeze 계열은 이 논문으로 선택할 수 없다.**
5. 🔴 **우리 계(LPSC)의 RSS hole% 가 없다.** *"LPSC 에도 적용했다"* 는 서술만 있고 `Fig. 11`·`Fig. 16` 은 **NaCl 뿐**.
6. 🔴 **오차막대가 aq. NaCl 에만 있다.** Sɴ2 는 명시적 *"single run"*, **LPSC·ice·SPICE 는 시드 반복 0**
   ⇒ `Fig. 7b` 의 "naive ≈0.075 vs pseudolabel ≈0.042" 가 시드 노이즈보다 큰지 **논문이 보증하지 않는다**
   (violin 은 *평가구조 간* 산포이지 *시드 간* 산포가 아니다).
7. 🔴 **LPSC 500 구성의 샘플링·온도·Cl/S 부분점유 처리가 전부 미기재.** 우리 계의 본질적 자유도(무질서)가 통째로 빠짐.
8. 🔴 **비-argyrodite 평가셋의 N·조성 미기재** — 우리가 제일 무겁게 쓰는 숫자가 거기서 나온다.
9. 🔴 **GPU 시간·epoch 수·batch 크기 어디에도 없다.** compute 보고 = *"multihead 는 naive 대비 3–15배"* 한 줄.
   ⇒ **"UMA fine-tune 에 몇 시간 드나"에 이 논문은 답하지 않는다.**
   유추 가능한 것 하나: *"Li 모델은 **NVIDIA A100** 에서 학습"*(나머지는 GH200/MI300A) = **A100 1장 규모**.
10. **RSS 는 단거리 반발벽만 본다.** 저자 명시 — *"경쟁 상들의 상대안정성이 틀리는 종류의 PES artefact 는
    다른 진단이 필요하다."* 🔴 **우리 b₂o₃ 골격 creep 은 오히려 그쪽에 가깝다** ⇒ `Fig. 11` 이 우리 creep 을
    예측한다고 쓰면 안 된다.

**⛔ 이 축에서 인용하면 안 되는 것 (→ §J-6 에도 추가)**
- ⛔ *"이 논문이 fine-tuning 이 이온전도도/확산장벽 예측을 개선한다고 보였다"* — **σ·D·Ea 를 한 번도 계산하지 않는다.**
- ⛔ *"이 논문이 snapshot ensemble / UQ 를 다뤘다"* — **한 번도 안 다룬다.** 우리 §12-F 는 **유도**다.
- ⛔ *"naive fine-tuning 은 catastrophic forgetting 을 일으키지 않는다"* — **정반대다.**
  논문의 주장은 *"초기 실패의 원인이 naive 의 본질적 결함이 아니라 약한 파운데이션·잘못된 E₀·불안정 학습이었다"* 이고,
  **SPICE forgetting 은 naive 가 여전히 ≈4×10³ 배로 최악**이다.
- ⛔ **`Fig. 10` 의 절대 force RMSE 값** (축 단위 불일치 — 위 3번).
- ⛔ **LPSC F RMSE 18.4 meV/Å**(MACE-OMat-0-medium · PBE · Li₆PS₅Cl · fine-tune 후)를
  **우리 UMA Li₃PS₄ F MAE 30.0 / RMSE 44.6 meV/Å**(UMA-s-1p1 · PET-MAD 라벨 · **Cl 없음** · zero-shot)와
  같은 표에 놓는 것 — **모델·계·라벨·평가셋이 전부 다르다.** *"자릿수가 같다"* 까지만.
- ⛔ **`figure-read ≈` 값을 본문 명시값처럼 쓰는 것.** `Fig. 3a`·`Fig. 4a`·`Fig. 7b`·`Fig. 17`·`Fig. 10` 의 숫자는
  **전부 violin 중앙부 판독**이고 본문에 숫자가 없다(순위·정성 서술만). **±10–20% 오차 가정.**
  **인쇄된 숫자는 `Fig. 11` 과 `Table 1–9` 뿐이다.**

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_tompa2026_finetuning_mlip_foundation_strategies.md` ## ③ .</sub>


**[Wilson22BAL] `wilson2022_batch_active_learning_interatomic_potentials` — 배치 능동학습 획득함수의 정의 원본**

> ⛔ **σ·Ea·D·ESW·탄성·gap 이 0건**이고 재료계도 겹치지 않는다(GeSe). 여기 있는 것은
> **"배치를 어떻게 고르는가"의 식**이고, 그것 하나가 이 편의 전부다.
> ⭐ **`[Shapeev16]` 블록 바로 아래 놓는 것이 맞다** — `[Shapeev16]` 이 *"우리가 못 쓰는 길(선형 설계행렬)"*
> 을 정의하고, 이 편이 *"그 가정 없이 가는 길"* 을 정의한다. 두 블록을 붙여 놓아야 축이 보인다.

| 항목 | [Wilson22BAL] | 우리 (`tools/ionic/mlip_committee.py` · cascade Stage 07/08) | 판정 |
|---|---|---|---|
| **불확실도 정의** | **query-by-bagging** — 같은 모델을 라벨셋 **80 % 부표본**으로 `N_M`=10회 재학습, 예측 에너지의 **표본표준편차**(식 1, Bessel `N_M−1`) | **이종 committee** UMA-s-1p1(OMat24) / MACE-MP-0(MPtrj) / SevenNet-0(MPtrj), **M=3** | 🔴 **재는 것이 다르다.** 배깅 = **데이터 표집 분산**, 우리 = **아키텍처+훈련셋 편향**이 섞인 것. **숫자를 나란히 못 놓는다** |
| **선형 설계행렬 `X` 의존** | ⛔ **없다.** 저자 명시 *"model-agnostic … estimates the uncertainty internally by using the predictions from multiple models"*. Podryabinkin 2017[28]·Gubaev 2019[27] 은 **인용만 하고 미채택** | 쓸 수 없음(`X` 부재 — `[Shapeev16]` 블록) | ⭕⭕ **이 축에서 제일 큰 소득.** `mlip_committee.py` docstring 의 장벽이 **이 처방엔 존재하지 않는다** ⇒ **UMA 이식 가능** |
| **획득함수** | `S_i = α(U_i/Ū) + β(D_i/D̄)`, **α=0.9 / β=0.1**, Ū·D̄ = 미라벨 전체 평균 | 없음 (순차 게이트만) | ⭕ **이식 후보 (T1, 계산 0회).** 평균정규화 덕에 α·β 가 단위 없이 의미를 갖는다 |
| **배치 다양성** | **greedy 조건부** — 하나 뽑을 때마다 **D 만** 재계산(U 는 배치 내 고정). ⇒ **top-k 아님** ✔ | 없음 | ⭕ 이식하되 **🔴 식을 고쳐서**: `D_i = Σ_j‖·‖`(합) → **`min_j‖·‖`**. 합은 배치 후반에 중복 페널티가 **1/j** 로 희석된다(digest §10-①) |
| **배치 크기 k** | **10 고정.** 근거 = *"DFT 를 병렬로 던지려고"* 정성 동기뿐, **민감도 시험 없음** | 정의 안 돼 있음 | 🔶 **논문의 10 을 베끼지 않는다** — 우리는 **KISTI QOS 동시제출 한도**로 정하는 것이 정직하다 |
| **특징공간 χ⃗** | **수제 121차원, 라운드 간 고정**(AGNI 2체 24 + 3체 96 + 상수 1) | 없음 | 🔴 **UMA 임베딩은 fine-tune 마다 좌표계가 바뀐다** ⇒ **동결 서술자**(SOAP 또는 고정 readout)를 따로 둬야 라운드 간 거리가 비교된다 |
| **특징의 입도** | **원자평균**(digest 추론: 표적 = 원자당 에너지 + 구조당 121차원) | — | 🔴 **국소 희소 사건이 묻힌다.** 도펀트/계면은 `[Ou26MS]` 의 **`--al_mode=nbh`(원자환경 AL)** 쪽이 맞다 |
| **불확실도 채널** | **에너지만.** 힘 불확실도는 계산조차 안 한다 | 우리 보고량은 **D·Ea**(힘/궤적) | 🔴 간극. 에너지 산포가 힘·D 오차의 대리인지 **이 논문이 답하지 않는다** → `[Carrete23UQ]` 축 |
| **재학습 경제성** | `N_M × N_B` = **시드당 3,000회 KRR 피팅**이 무료 | UMA 재학습 = **fine-tune 필요** | 🔴 **진짜 이식 장벽은 알고리즘이 아니라 비용이다.** 저자도 §4 에서 *"NN 은 비싸진다"* 인정 |
| **시드 반복 보고** | ⭕ **`N_S`=10, 모든 그림에 산포** | 🔴 단일 궤적(Ea 3-seed 뿐) | ⭕⭕ **형식 이식 1순위** (`our_dft_baseline.md` 의 상시 약점) |
| 힘 RMSE 눈금 | **0.157–0.255 eV/Å** | MTP 자체학습 0.073 · SevenNet-0 0.070 | 🔴 **그들 모델이 2–4× 부정확** ⇒ AL 이득이 파운데이션 정확도 영역에서도 남는지 **미검증** |

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_wilson2022_batch_active_learning_interatomic_potentials.md` ### 2-b..</sub>


**[Zaby26σ] `zaby2026_reliable_conductivity_estimates_md` — σ 를 *추정하는 절차* 의 원전**
(*ChemPhysChem* **27**, e70477, 2026 · Zaby/Ingenmey/Lourenço/Zhang/Da Silva/Brehm/**Maginn**/**Kirchner** ·
계 = **[EMIm][DCA] 이온액체 + LiFSI/DME 에테르 전해질** · **황화물·고체전해질 0회 · 온도 1점 · DFT 0회 · 물성값 0**)

> 🔑 **우리가 이 편에서 가져오는 것은 σ 값이 아니라 "σ 를 보고량으로 성립시키는 조건" 이다.**
> 그리고 그 조건 대비 **우리 Stage 10 σ 파이프라인이 어디서 죽는지**의 눈금.

| 항목 | [Zaby26σ] | 우리 (`tools/doping/run_md_sigma.py` · `tools/ionic/run_comp1_seeds.sh`) | 판정 |
|---|---|---|---|
| **σ 의 정의** | **집단**: EH(집단 MSD 기울기) 또는 GK(전하전류 ACF 적분). NE 는 **근사**로만 | **NE 단독**, `σ = n q² D /(k_B T)`, **H_R = 1** | 🔴 **부류가 다르다.** 우리 것은 그들 분류의 `σ_NE` 이고 **cross 항이 0으로 가정돼 있다** |
| **NE 오차의 크기** | ionicity **0.48–0.76** ⇒ NE **1.31–2.08× 과대** (cross 가 self 의 30–52 %) | 미측정 | 🔴 **크기는 이식 금지** (액체 값). 🟡 **"미측정" 이라는 사실만 이식** |
| **NE 오차의 부호** | **과대** (cross < 0) | 미측정 | 🔴🔴 **[Adeli19] 실측 H_R 0.23–0.3 은 반대 부호**(σ_실측 > σ_NE) ⇒ **부호조차 우리 계에서 미확정.** *"NE 라서 과대"* 라고 쓰면 틀린다 |
| **적합창** | 로그기울기 자동 검출(MSDiff v0.2.0). **고정 tail 은 σ 를 1.6–2.8× 낮춘다** (1.0 M: 자동 60 ps–24 ns → 2.03 vs tail 15–30 ns → 0.73 S m⁻¹) | **`fit_start = n_frames//2`**(도핑/σ 경로) / `--fit_window_ps 2 50`(이온 경로) | 🔴 **도핑 경로가 직격.** ⛔ **2.8× 는 집단 MSD 값이라 우리 self-MSD 로 못 옮긴다** — **방향(과소)만**. ⚠ 부수 발견: **한 repo 에 D 정의가 둘** |
| **시간원점** | **다중 원점 + 그 산포를 적합 가중치로** (§2.3.1) | **단일 원점** (`⟨‖r(t)−r(0)‖²⟩`) | 🔴 **정량 페널티는 이 논문에 없다**(원점 스캔 실험 0건). 판정 근거는 구조적 — **ΔMSD(τ) 가 없어 오차가중·자동창·χ²_red 를 실행할 수 없다** |
| **replica 정의** | **새 PACKMOL 박스 10개**(배열+속도 모두 다름, 밀도는 통일) | ✅확인 **동일 `--v0_xyz` + 속도 시드만** (`--n_configs 1 --disorder_levels 0.0`) | 🟡 §2.3.1 의 *"and/or"* 로는 통과하나, `Fig. 7`·`Table 3` 의 **위상공간 피복 논거는 배열 다양성에서 온다** ⇒ 우리 오차막대는 **within-replica 쪽** |
| **replica 수** | **10**. ⛔ 최소치를 처방하지 않음(*"defined independently for every simulated material"*) | **3** (600 K 만) | 🟡 self 량이면 부분 생존 · 🔴 집단 σ 면 부족 |
| **불확실도 산출** | **역분산 가중평균 + χ²_red 재조정**(Eq. 27) + **부트스트랩**. 단일 궤적 분할은 SE 를 **1.33–1.52× 과소**(6/6) | `linregress` 의 SE (점들이 상관 → 무의미) | 🔴 **죽는다.** ⭕ **χ²_red 재조정은 계산 0회로 이식 가능** — 시드 3개 σ_r 만 있으면 된다 |
| **궤적 길이** | EH **100 ns**, GK **0.1 ns + 1 fs 속도 저장**(이상적 비교 궤적 **900 GB**) | **200 ps** | 🔴 **집단 σ 는 우리 자원에서 열지 않는다** (판정) |
| **써모스탯** | Nosé–Hoover 계열(TGNH)만 | **Langevin (friction 0.02)** | ⚠ **이 논문이 다루지 않는 위험.** Langevin 은 운동량 비보존 ⇒ 집단 전하전류에 열욕이 개입한다. **⚠ 우리 가설이지 논문 주장 아님.** self MSD 영향은 훨씬 작다 |
| **셀 크기** | self D **+9–10 %**(125→1000쌍), YH 보정 **+12–41 %**. **total σ 는 cross 상쇄로 검출 불가** | 계마다 원자 수 통일 규약 **없음** | 🔴 **새 제약**: D_tr 랭킹으로 가면 **후보계 원자수를 고정**해야 한다 |
| **좌표계** | σ_tot·self 는 무관(self 는 열역학 극한에서), **cross·수송수는 의존**(t(Li⁺) 부호 반전) | 해당 없음(단일 가동종) | 🟡 우리가 cross 를 재기 시작하면 그때 필요 |
| **온도 의존 / Ea** | **0건** (단일 온도) | 600/800/1000 K Arrhenius | 중립 — **이 논문은 우리 Ea 축에 대해 아무 말도 하지 않는다** |
| **MLIP 검증** | 서론 언급뿐, 실험 0건 | UMA-s-1p1 | 중립 — ⛔ *"MLIP σ 가 검증됐다"* 의 근거로 쓸 수 없다 |

**★★★ Stage 10 판정 (Q10 — σ 를 랭킹 축에서 뺄 것인가)**

> **조건부 지지.** 이 논문은 *"σ 를 쓰지 마라"* 가 아니라 *"σ 는 집단량이라 이만큼의 통계 예산을 요구한다"* 를 말한다.

- **지지 ①** `Fig. 8`·`Fig. 9`: **self 기반 양의 SE 가 집단 양의 1/10.** σ_NE 는 상관깊이 1→30 ns 에서 **−1.8 %·SE 평평**,
  σ_EH 는 **−8 %·SE ×3.1**. self 항은 크기 추세를 **판정할 수 있고** total 은 **판정할 수 없다** ⇒ *"랭킹은 판정 가능한 양으로"*.
- **지지 ②** ionicity 가 **같은 물질계 안에서 1.4배 범위**(IL 0.542–0.760 / LiFSI 0.480–0.610)로 움직인다.
  = **[Adeli19] 의 *"Cl 함량 x=0→0.5 에서 H_R 1.34배 변동"* 과 같은 논증을 계산 쪽에서 반복**한 것.
  ⇒ H_R=1 고정 σ 로 도펀트를 줄 세우면 순위 안에 **미지의 조성 의존 인자**가 들어간다.
  (⚠ 1.4배·1.34배는 각각 그 논문의 계 값 — **논증 구조만** 가져온다.)
- **지지 ③** 우리 예산은 그들 요구의 **1/500(200 ps vs 100 ns) · 1/10(replica 1 vs 10)** 이고,
  게다가 **반증된 tail 적합 + 단일 시간원점**을 쓴다 ⇒ 보고량 규율 언어로 **집계 규칙 없는 스칼라 σ**.
- **반대/중립** — ① 이 논문은 σ 를 **살리려고** 쓴 논문이다 ② **D_tr 도 공짜가 아니다**(크기 9–10 %, YH 12–41 %)
  ⇒ 원자수 통일이라는 새 제약 ③ 재료계가 다르다 — 액체에서는 반대 부호 이온이 함께 움직여 σ 를 깎지만
  argyrodite 에서는 Li–Li 협동 이동이 σ 를 **키울** 수 있다(= [Adeli19] H_R<1).

⇒ **인용 문장은 *"NE 가 틀려서"* 가 아니라 *"우리 계산 예산에서 σ 는 정의된 보고량이 아니고, 같은 궤적에서 D_tr 은 정의된다"*.**

**⛔ [Zaby26σ] 에서 인용하면 안 되는 것**
- **어떤 σ·D 절대값의 이식** — 고전 CL&P(ol) 액체, 353/333 K.
- **"NE 는 σ 를 과대평가한다" 를 argyrodite 에 적용** — [Adeli19] 실측이 **반대 부호**.
- **"2.8× 과소" 를 우리 self-MSD D 에 적용** — 그 수치는 **집단 MSD** 값이다.
- **"replica 10개 필요" 를 규칙화** — 저자가 계마다 다르다고 명시.
- **"권고 상관깊이 10 %" 를 우리 2–50 ps 창의 근거로** — 100 ns 기준 비율이다. 200 ps 에 곱하면 20 ps 인데 그 산술에 물리적 근거가 없다.
- **ionicity 0.48–0.76 을 "액체의 보편값" 으로** — 계 2종·온도 1점.
- **이 편을 "MLIP σ 의 검증" 으로** — MLIP 실험 0건.

**⚠ 우리가 실측한 논문 내부의 미봉합** (digest §16-B): 실험 기준선이 있는 **5개 비교 중 3개에서 NE 가 실험에 더 가깝다**
(IL CL&P Δ+0.49 vs EH Δ−1.70 / IL CL&Pol Δ+1.96 vs Δ−2.08 / LiFSI 3.5 M Δ−0.17 vs Δ−0.54).
저자는 **3.5 M 에서만** 오차상쇄를 인정하고 `Fig. 2` 상단의 같은 현상에는 침묵한다.
⇒ 이 논문의 주장은 **정확도 논증이 아니라 추정량 논증**이다. 그 구분을 흐리고 인용하면 데이터가 안 받쳐준다.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_zaby2026_reliable_conductivity_estimates_md.md` ## ③ .</sub>

**[Lynch26GK] `lynch2026_greenkubo_mlip_conductivity_thesis` — MLIP 로 full Green-Kubo σ 를 실제로 수렴시킨 편 (2026-09-22 신설)**

> **D. Cory Lynch** 박사학위논문(Wake Forest, 지도 **N. A. W. Holzwarth**, 2026-08, 234 pp).
> 인용은 부록의 두 산출물로: **PRM 8, 065401 (2024)**(boracite) · **preprint dated 2026-08-03**(Green-Kubo, **DOI 없음**).
> ⛔ **물성 4축 금지** — 우리 계(아지로다이트)에서 잰 σ·Ea·gap·탄성이 **0건**이다.
> 시험계는 **산화물 `Li₃.₂₅P₀.₇₅Si₀.₂₅O₄`(132원자, 질서배열 2개)** 이고, 아지로다이트 절은 **미출판·중단**이다.

**a. 규약 대조 — 우리 MLIP-MD 스택 vs 이 논문**

| 축 | **[Lynch26GK]** | 우리 (UMA 스택) | 판정 |
|---|---|---|---|
| MLIP | **Allegro** 전용학습(24.5 k–91 k params, r_cut 6.0 Å) | **UMA-s-1p1(omat)** 범용·무파인튜닝 | 🔀 노선 자체가 다르다 |
| 앙상블 | **NVE** (써모스탯 없음 — *재현성* 목적, 부피고정→고압 자인) | **Langevin NVT**(friction 0.02) | ⚠ Langevin 은 **집단 전하흐름에 잡음 주입** ⇒ full σ 를 재면 우리가 불리 |
| dt | **0.5 fs** | **2 fs** | ⚠ 4배 — UMA 로 검증된 값이나 **GK 용으로는 미검증** |
| 생산 길이 | **2.8 ns** | **200 ps** | 🔴 **14배** |
| 온도 | 목표 350/450/550 K (**실측 T̄ 373/470/565 K**) | **600/800/1000 K** | 🔴 우리는 그들이 *"Lyapunov 로 못 믿겠다"* 한 550 K 보다 **전부 위** |
| 적합 | Λ(τ) 를 **`f₀+f₁/τ` 로 τ→∞ 외삽** | **MSD 2–50 ps 고정창 OLS** | 🔴 **보고량이 다르다** (극한 vs 고정창) |
| 블록 표본 | **모든 τ 에 M≈10⁵ 고정** | **단일 시간원점** | 🔴 `[McC25D]` 판정과 같은 방향 |
| 시드 | **초기속도 10 × 모델 5** | 속도 3(600 K) · 모델 1 | 🔴 양쪽 다 부족 |
| σ 정의 | **full GK(교차항 포함) + tracer 둘 다** | **tracer + NE, H_R = 1** | 🔴 그들이 *"불충분"* 이라 한 쪽만 쓴다 |
| MSD 기준계 | **골격 전하중심 `r_corr(t)` 를 뺀다**(full 과 논리일관 목적) | 빼지 않는다 | ⚠ 그들도 *"대개 작다"* — 우리 쪽 크기는 **미측정** |
| 학습데이터 | FPMD 100/400/600/900 K **1:1:2:2** · **낮은 tol 로 뽑고 엄격 tol 로 재계산** · E·F·**응력** 필수 · **close-pair ~400 추가** | 해당 없음(범용 모델) | ★ **재계산 규율**은 우리가 파인튜닝할 날 그대로 베낄 것 |
| 무질서 | **대칭 유지 질서배열 손열거** (아지로다이트는 24g 완전점유 vs 48h 50 % 두 출발) | **disorder_ensemble** | ✅ **우리가 낫다** |
| 하드웨어 재현성 | CPU 고정(AMD) · **AMD↔Intel 은 ~1 ps 뒤 갈림** · **GPU 는 매 런 다름** | GPU(UMA) — **미점검** | ⚠ 우리가 안 본 축 |

**b. ★★ Haven 비 — 우리 db 의 부호 논쟁에 표본 하나 추가** *(고체 vs 액체의 갈림이 이 편으로 더 굳는다)*

| 출처 | 계 | **H_R = σ_tr/σ_full** | σ_full/σ_tr | 방법 |
|---|---|---|---|---|
| **[Adeli]** | Li₆₋ₓPS₅₋ₓCl₁₊ₓ | **0.23 – 0.30** | 3.3 – 4.3 × | 실험(⁷Li PFG + EIS) |
| **[Fang22PW]** | Li₆POS₄(SH) / Li₆.₂₅PS₅.₂₅(BH₄)₀.₇₅ | 0.769 / 0.667 | 1.30 / 1.50 × | AIMD |
| **[Lynch26GK]** ← 신규 | Li₃.₂₅P₀.₇₅Si₀.₂₅O₄ (**산화물**) | **0.53 – 1.03** (모델평균 0.60–0.77) | **1.0 – 1.9 ×** | **MLIP full GK** |
| 우리 자체 | modelc | 0.84 ± 0.06 (`citable:false`) | 1.19 × | MLIP |
| **[Zaby26σ]** | 이온액체 · 에테르 전해질 | **1.3 – 2.1** | 0.5 – 0.8 × | 고전 MD |

⇒ **판정 갱신**: **고체 Li 전도체는 지금까지 전부 H_R < 1**(= tracer/NE 가 σ 를 **과소**평가),
**액체만 H_R > 1**. `[Zaby26σ]` 의 *"NE 는 과대"* 를 우리 계로 옮기지 말라는 앞선 판정에 **한 표 더**.
단 크기가 **1.2–4.3 배**로 여전히 벌어져 있어 **σ 절대값 인용 금지는 유지**되고,
우리 자체 0.84 는 이 분포 안에 무난히 든다.

**c. 🔴 digest 재계산 — 원논문이 보고하지 않은 모델 시드 산포** *(`Table VII`/`VIII`/`IX` 의 5개 값으로 낸 표본통계)*

| 양 (구조 S1) | 350 K 목표 (T̄ 373 K) | 550 K 목표 (T̄ 565 K) |
|---|---|---|
| σ_full 범위 | **1.56 – 6.70 mS/cm** | 52.19 – 77.11 |
| **max/min** | **4.29 ×** | 1.48 × |
| CV = sd/mean | **49.2 %** | 14.7 % |
| σ_tr CV | 38.2 % | 5.5 % |

- **이건 초기속도 10개를 이미 평균한 뒤 남은 산포다** — 즉 **순수 MLIP 학습 시드 효과**.
  (S2 는 1.80 ×·CV 30.1 % 로 덜하다. 두 값을 같이 인용할 것.)
- **E_a^full 모델 산포**: S1 **226.34 – 388.03 meV(sd 60.0)** · S2 241.11 – 322.47(sd 32.2).
  ⛔ 논문이 보고한 오차막대(±41.32 / ±13.53 meV)는 **실제 모델 산포보다 1.45× / 2.38× 작다**.
- ★ **저온의 역설 (논문이 짚지 않은 것)**: 저자 결론은 *"저온이 Lyapunov 를 줄여 안전하다"* 인데,
  **같은 표의 모델 간 산포는 저온에서 3배 커진다**. 물리적으로 자연스럽다 — 저온에선 2.8 ns 안의 hop 수가 적다.
  ⇒ 정확한 명제 = **"저온은 τ-수렴을 사고 hop 통계를 판다."**

**d. 🔧 우리 파이프라인에 그대로 걸리는 것 3건**

1. **우리 2–50 ps 창이 평탄부 안인지 한 번도 확인 안 했다.** `Fig. 11` 실독: 그들 계의 Λ^tr 은
   **τ ≈ 200 ps 에서야 평평**해진다(373 K). 우리는 온도가 높아 더 빠를 것이나 **잰 적이 없다.**
   ⇒ **액션**: modelc 600 K 궤적 하나에서 `MSD(τ)/(6τ)` 를 τ = 2 → 200 ps 로 그려 평탄 시작점을 잰다.
   **`tools/ionic/` 기존 도구에 τ-스캔 플래그 추가**(새 파일 금지 — 코드 규율 사다리 ③).
2. **우리 온도격자(600/800/1000 K)는 full σ 를 재기 시작하면 부적절**하다.
   ⛔ 단 **tracer D 에는 이 논문이 불리한 근거를 주지 않는다** — 그들 Λ^tr 은 550 K 에서도 수렴했다.
   정확한 명제: *"위험한 것은 **full σ 를 잴 때**다."*
3. **모델 시드 산포를 우리는 구조적으로 못 본다** (UMA 하나만 쓴다).
   ⛔ 이것을 *"우리는 안정적"* 으로 읽으면 안 된다 — **재지 않은 것**이다.
   우리 쪽 대응물은 **모델 committee**(`[Wang25DPA]`·`[Chang26]`·`[Carrete23UQ]` 축)이고,
   이 편이 그 축에 **"모델 시드만으로 4.3배"** 라는 정량 근거를 하나 보탠다.

**e. ✅ 우리 규율을 지지하는 것**

- **`Fig. 10` vs `Fig. 11` 실독**: 같은 궤적·같은 τ 인데 **교차항 하나가 수렴성을 가른다** —
  full 은 550 K 에서 τ=1400 ps 까지 약 **6배 산포**, tracer 는 세 온도 다 τ≈200 ps 에 평탄.
  ⇒ 우리가 **tracer 만 재고 σ 절대값을 안 쓰는 선택**은 이 논문 기준으로 **정합적**이다.
- **`Fig. 5` 실독**: 900 K 에서 **고장이 ~900 ps 뒤 시작해 1.4 ns 에 폭주**했다.
  우리 prod 200 ps 는 이런 고장을 **구조적으로 못 본다** ⇒ **고온 장시간 스크리닝 1회를 계당 게이트로** (저비용).
- **ESW 부동태화 논증**(PRM 2024): 계산 창 **2.369 V** ↔ 실험 **4.3 V** 의 괴리를
  *"분해산물이 전자절연성이라 자기제한"* 으로 설명 — **우리 "grand-potential ESW = worst-case 하한" 규율의 독립 선례**.
  ★ 도구도 같다(**pymatgen grand canonical potential**, 0–5 V 균일 스캔).
- **황화물 anodic 한계 2.117 – 2.491 V**(B–S 골격) ↔ **우리 comp1/modelc 2.256 V**(P–S 골격).
  ✅ **같은 대역, 같은 기전(S²⁻ 산화 = 축 ①)**. ⛔ 골격이 달라 **값 대 값 인용 금지** — "황화물이면 2.1–2.5 V 대"까지만.

**f. ⛔ [Lynch26GK] 에서 인용하면 안 되는 것**

- **σ·E_a·H_R 절대값을 아지로다이트 문장에** — 산화물 인산/규산염 · 132원자 · 질서배열 2개.
- **`Table 5.4` 의 ΔE_F(−2.3/−3.6/−3.4 eV)를 도핑 선호도 근거로** — 셀당 총에너지이고 **전구체 집합이 서로 다르다**.
  *digest 재계산*으로 균형반응을 복원해야 한다:
  `Li₂₄P₄S₂₀Cl₄ + ZnO → Li₂₂P₄S₁₉Cl₄ZnO + Li₂S` = **−1.3 eV/셀**(결론은 살아남음) ·
  `Li₂₂P₄S₁₉Cl₄ZnO + LiCl → Li₂₁P₄S₁₈Cl₅ZnO + Li₂S` = **+0.2 eV/셀 = +4 meV/atom**(**분해능 밖**, "Cl-rich 불리" 로 읽지 말 것).
- **§5.4 를 "Si 도핑" 으로** — 절 제목과 `Fig. 16` 캡션이 Zn 을 "silicon" 이라 적은 **템플릿 잔재**다(그림 실독으로 확인).
- **§1.4.2 의 ZnO 선행연구 [26]** — 그 [26] 은 **MEGNet 논문**(Chen/Ye/Zuo/Zheng/**Ong**, *Chem. Mater.* 31, 3564 (2019))이다.
  저자·연도만 맞는 **인용 충돌** ⇒ 우리 규율 *"인용 역할 확인 후 삽입"*(2026-07 Kim/Cui 교훈)의 정확한 재현.
- **이 논문의 LPSCl 기준선** — Deiseroth 2011 재수록(`Fig. 20` figure-read **E_A 0.38(2) eV**, RT σ ≈ **1.3×10⁻⁶ S/cm**)이라
  **현대 최적화 LPSCl(1–10 mS/cm)보다 3 자릿수 낮다**.
- **"close-pair 400개" 를 규칙화** — 저자 근거가 *"정성적으로 실패 수가 줄어 보인다"* 뿐이다(대조군·n 없음).
- **"검증오차 = 내삽능력"** — 10점 산점도, R² 미보고, 같은 WS 에서 ΔE 가 **1–53 meV** (`Fig. 9` 실독).
- **a = 9.8/9.7 Å 를 PBEsol 평형격자로** — *"실험과 일치시키려 cubic 으로 구성 후 **격자벡터 고정** 이온완화"* 라
  계산값인지 실험 입력값인지 논문이 구분하지 않는다.

**🔎 확보 후보 (이 편 경유)**
- ref [88] **Jang, Rajagopal, Kang, Ryu (2023) *J. Alloys Compd.* 957, 170273** — `Li₆₋₂ₓZnₓPS₅₋ₓOₓCl` 실험.
  **우리 Nd/O 도핑 축의 Zn/O 대조군**이 될 수 있다. 미보유.
- ref [20] **Kaup, Bishop, Assoud, Liu, Nazar (2021) *JACS* 143, 6952** — Li₆B₇S₁₃I, 제목에
  *"argyrodite-like lithium substructure"*. **boracite ↔ 아지로다이트를 잇는 고리**이자 [Adeli]/[Zuo] 와 같은 Nazar 그룹. 미보유.
- ref [23] **Deng, Eames, …, Grey, Masquelier, Islam (2015) *JACS* 137, 9136** — 시험계 원전(Li₄SiO₄–Li₃PO₄). 미보유.

<sub>> 📎 2026-09-22 litdb-curator 신설 · 그림 20장 크로핑 중 **11장 실독** · digest `papers/lynch2026_greenkubo_mlip_conductivity_thesis.md`</sub>



**[Hu26ICAL] `hu2026_foundation_model_surrogates_active_learning`** — 능동학습 **대리모형·획득함수·UQ 캘리브레이션 지표**의
방법 원전. **물성값 0.** 본문 판정은 **§J-9c** 에 있다(AL 축이라 그쪽이 본진). 여기서는 두 가지만 남긴다:
① **`AUSE`** = σ 의 **순서**만 쓰는 스케일 불변 UQ 품질 지표 ⇒ 우리 committee(M=3, 절대 σ 금지)에 **적용 가능한 유일한 것**.
② **획득함수 6종의 수식**(`Table 1`, β·ξ 포함)은 **두세 줄짜리라 직접 구현**한다 — 저자 코드는 미공개다.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_hu2026_foundation_model_surrogates_active_learning.md` ## ④ .</sub>


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

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_liang2026_interface_bottleneck_solid_state_batteries.md` ## ④ .</sub>

**[Zeng26Gar] `zeng2026_ga_llzto_site_specific_substitution` — ⛔⛔ 산화물 가넷 · 물성 4축 진입 금지 · **흡착 보고량 "선언 공백" 의 표본**** (2026-09-16 신설)

> ⛔ **Li₆.₄La₃Zr₁.₄Ta₀.₆O₁₂(LLZTO) 가넷이다.** 골격(O²⁻)·열화기전(Li⁺/H⁺ 교환 + Li₂CO₃)·전압눈금이
> 우리 황화물 아지로다이트와 다르다. **σ 4.95×10⁻⁴ S/cm · Ea 0.34 eV · E_ads −1.63/−2.44 eV 전부 4축 진입 금지.**
> 여기 두는 이유는 §J-7 의 (ii) 사유다 — *값은 있는데 계가 달라 같은 표에 놓으면 단서가 안 따라간다.*

**(1) 이 편의 실제 소득 — `estimand_card §3` 여섯 물음의 외부 대조표**

우리는 SDCP 흡착에서 **여덟 번** 반려됐고, 받은 지적은 전부 *"맞는 양을 재고 있나"* 였다.
이 논문은 **그 여섯 칸을 하나도 선언하지 않고 E_ads 두 개를 보고하고 통과했다.** 차이는 실력이 아니라 **계의 위험도**다.

| `estimand_card §3` 물음 | [Zeng26Gar] | 우리 SDCP | 판정 |
|---|---|---|---|
| SCF 해가 하나인가 | ⛔ 선언 없음 | ⛔ 여럿 (basin 다수) | 이 논문은 **닫힌 껍질이라 운이 좋았다** |
| 열린 껍질(홀전자) | ⛔ 선언 없음 — 단 La³⁺(4f⁰)·Zr⁴⁺(4d⁰)·Ta⁵⁺(5d⁰)·Ga³⁺(3d¹⁰)·O²⁻·NMP 전부 무자성 | 🔴 **doublet (홀전자 O)** | **여기가 갈린 지점** |
| 기판 자성 | ⛔ 선언 없음 (무자성 개연) | 🔴 **AFM 슬랩** | " |
| 산화환원 활성 | ⛔ 선언 없음. ⚠ E_ads −2.44 eV 는 화학흡착 영역인데 **흡착 전후 전하이동 미보고** | 🔴 **LiNiO₂ 활성** | 이 논문도 **여기는 위험지대**였다 |
| 참조가 같은 전자상태인가 | ⛔ **분자 참조 박스 조건 0건** | 🔴 실측 사고: 기준 `NUPDOWN=1` 강제 ↔ 복합체 `NUPDOWN=−1` 자유 (2026-08-28) | **둘 다 못 했다** |
| 흡착 전후 보존 가정 | ⛔ 선언 없음 | 카드에 명시 중 | 우리가 앞선다 |
| **집계 규칙** | ⛔ **미정의** — 본문은 "La **sites**"(복수)라 쓰고 값은 **계당 하나**. 최저인지·대표인지·유일 시도인지 없음 | 선언 필요 | 🔴 **이 축에서는 이 논문의 보고량이 정의되지 않았다** |

**(2) 슬랩 규약 — 본문 41 pp + SI(.docx 전문 XML) 전수 스캔 결과**

계산 서술은 **본문 §2.5 한 문단(≈10줄)이 전부**고 **SI 는 계산 문장 0건**이다
(`slab`·`adsorption`·`DFT`·`Dmol`·`k-point`·`spin`·`vacuum`(계산 맥락) **전부 0 hit**).

| 항목 | [Zeng26Gar] | 비고 |
|---|---|---|
| 있는 것 | **DMol³ / Materials Studio 2019 · GGA-PBE · DNP(3.5 basis file) · ECP · 실공간 궤도절단 5.0 Å · DFT-D(버전 미기재) · 수렴 E 10⁻⁵ Ha / F 0.002 Ha·Å⁻¹ / x 0.005 Å / SCF 10⁻⁵ Ha** | ⚠ **평면파 cutoff 가 아니다** — 원자중심 수치기저 코드 |
| 표면 | ✅ **(100)**, 흡착종 **NMP**, 자리 **La** | 선택 근거·표면에너지 비교 **없음** |
| 슬랩 두께 · 진공 · 셀크기 · 원자수 | ⛔ **0건** | `Fig. 5e/5f` 는 **하단이 패널 경계에서 잘려** 층을 셀 수 없다 |
| 구속층 · 쌍극자 보정 | ⛔ **0건** | ⚠ NMP 는 쌍극자가 큰 분자 + 한쪽면 흡착 = 비대칭 슬랩인데 보정 선언 없음 |
| E_ads 정의식 · 분자 참조 박스 | ⛔ **0건** | 부호 규약도 암묵 |
| 자세 탐색 수 · 집계 규칙 | ⛔ **0건** | 위 (1) |
| k-점 · U · 전하보상 · 무질서 처리 | ⛔ **0건** | 가넷 Li 부분점유(96h 0.35 / 24d 0.56)를 어떻게 정수로 내렸는지 없음 |
| 모형 조성 | ⛔ 불명 — `Fig. 5e/5f` 범례에 **Ta 도 Ga 도 없다**(Li·La·Zr·O·C·H·N 뿐) | LLZTO 인지 Ta-free LLZO 인지 **논문으로 확정 불가** |

⇒ **이 편을 슬랩 규약 원전으로 쓸 수 없다.** 그 자리는 여전히 **[Wang26IF]**(§J-7 첫 블록) 다.
**[Liang26IF](슬랩 규약 0건) 에 이은 네 번째 음성 결과** — *"슬랩 구성 규약을 적는 관행이 분야에 없다"* 의 증거가 하나 더 늘었다.

**(3) 반대로 이 편이 우리에게 주는 것 2개**

- ⭕⭕ **T1 — 계산 한 숫자를 "이진 공정 관측"에 붙였다.** `E_ads(NMP) −2.44 → −1.63 eV` 를
  **"PVDF–NMP 슬러리가 겔이 되는가"**(`Fig. S20`·`Fig. S27`)라는 눈에 보이는 관측에 대응시켰다.
  ⇒ 우리 SDCP 는 **조건은 완벽했는데 대응 관측이 없었다.** 카드 §1 에 *"이 값이 맞히면 무엇이 달라지나"* 를
  관측 가능한 형태로 적는다. **(이 축에서는 이 논문이 우리보다 낫다.)**
- ⭕ **T1 — "성능과 열화가 같은 결정학적 자리에 묶이면 조성 튜닝으로 못 푼다"** 는 진단틀.
  우리 계로 옮기면 *"S²⁻ 자리(ESW **S-limited** 2.256 V)와 수분 가수분해 표적이 같은 자리인가?"* 가 된다 —
  **아직 우리가 안 물어본 질문**이다 (`kb/questions/` 카드 후보).

**(4) ⛔ 이 편에서 우리 축으로 이식 금지 (digest §10 에 근거 전문)**

| 금지 | 사유 (내가 검산) |
|---|---|
| "공공 분율 8.70 → 35.66 %" (`Fig. 3c`) | 증가분 **26.96 %p = `Table S2` 의 Ga 점유율 0.2696 과 정확히 일치** ⇒ **Ga 가 앉은 자리를 빈자리로 센 것**. 새 Li 공공은 이 셈에서 0 이고 Eq. 1(Ga 0.46당 공공 0.92)과도 어긋난다. ⚠ 우리 tier2 `dopant_blocking_fraction` 계열이 같은 함정을 안 밟았는지 확인할 것 |
| 계산 이동장벽 (`Fig. 3d`) | figure-read **1.67–1.92 eV = 자기 실험 Ea(0.34/0.35 eV)의 약 5배** · 두 곡선 **종점이 0.9 eV 다름**(같은 상태로 안 끝남) · **방법명(NEB/LST-QST) 미기재** · `Fig. S9/S10` 은 **단일 이온 궤적**인데 본문은 "collective migration mode 유지" 주장 |
| "Bader charge" 0.52 → 0.72 (`Fig. 5g`) | **DMol³ 는 Bader 를 기본 제공하지 않는다**(Mulliken·Hirshfeld). 산화물 La 의 Bader 는 보통 **+2.0~+2.2 |e|** 인데 값이 0.5–0.8 ⇒ **Hirshfeld 의심**. ⛔ 우리 Bader/ICOHP 축과 **같은 표 금지** |
| La PDOS "하향 이동" (`Fig. 5h`) | 두 패널의 **에너지 기준정렬 미기재**. 그림대로면 Ga-LLZTO 의 **La 5d 전도띠가 E=0 을 가로지른다(=금속)** — 가넷 절연체에서 불가. 심준위 La 5s/5p 가 2–4 eV 이동하는 것도 화학효과로 보기엔 크다 |
| ICP wt% (`Table S1`) | LLZTO 행 합 **103.4 wt%** · Zr **42.99 wt%** (화학식 이론값 ≈14.4) ⇒ 오기. 인용 가능한 것은 **Ga 0 → 10.20 wt%** 와 Li 감소의 *방향*뿐 |
| 본문 pH "12.32" | `Fig. 4e` 로 인용돼 있으나 그 그림은 **13.06 → 13.30**(픽셀 교정, 같은 방법으로 읽은 Ga-LLZTO 9.81/10.63 이 본문 9.83/10.64 와 ±0.02 일치). **12.32 의 실제 출처는 `Fig. S13`**(분말 fresh, figure-read 12.35) |

<sub>> 📎 2026-09-16 신설 — `litdb/papers/zeng2026_ga_llzto_site_specific_substitution.md` §5·§8·§11 요약.</sub>




**[Ziemke26AP] `ziemke2026_li3ocl_substitutional_defects` — ⛔⛔ 산화물 antiperovskite · ⛔ arXiv 프리프린트 · **치환결함 형식론의 *음성* 표본**** (2026-09-22 신설)

> ⛔ **Li₃OCl antiperovskite 다** (Pm3̄m, **5원자/셀**, 폴리음이온 없음, Li 자리 **1종**).
> 우리 아지로다이트(F4̄3m, 52원자, PS₄³⁻ + free S²⁻ + Cl⁻, Li **24g/48h 다중분할**)와 **자리 위상이 대응되지 않는다** —
> 그 계에는 P_4b 같은 대체 자리가 **존재하지 않으므로 자리 선호 논쟁 자체가 없다.**
> ⛔ **그리고 넣을 값이 애초에 0건이다** — σ·Ea·ESW·gap·DOS·C_ij **전부 미계산**. §J-7 의 (i) 사유 그대로다.
> ⛔ **arXiv v1 · 심사 전 · 저널 DOI 없음** ⇒ 원고·SI 인용 금지.

**(1) 이 편을 받은 이유 — 1저자의 질문과, 이 편이 그 질문에 답하지 못한다는 사실**

1저자 지정 읽기축은 명확했다: *"우리는 도펀트 스크리닝을 hull 기반 반응에너지로만 했고 **'M³⁺ 가 정말 격자에 들어가나'** 는 아직 못 답했다(Shannon 반경을 대리지표로 썼을 뿐). 이 논문이 그 표준 방법을 보여주면 그게 제일 값있는 수확이다."*

**이 편은 그 표준을 보여주지 않는다.** 표준 치환결함 형식론의 층위를 하나도 수행하지 않고, 저자들이 §4 에서 자인한다 — *"without explicit charged-defect corrections, finite-temperature contributions, or dilute-limit extrapolation."*

| 표준 결함 형식론의 층 | [Ziemke26AP] | 우리 현재 (`ndo_lpscl16` / cascade) |
|---|---|---|
| 전하상태 `q` 선언 | ⛔ **0건** | ⛔ 0건 (우리도 중성 셀) |
| `E_f(q, E_F)` 도표 | ⛔ 0건 | ⛔ 0건 |
| 하전결함 보정(Freysoldt/Kumagai) | ⛔ 0건 (자인) | ⛔ 0건 |
| **화학퍼텐셜 경계**(Li-rich↔Li-poor) | ⛔ 0건 (`chemical potential` 전문 0 hit) | ⭕ **우리는 MP hull grand-potential 로 다른 방식으로 답한다** |
| 전하보상 스킴 | ⛔ **0건** — Mg²⁺·Al³⁺·Gd³⁺ 를 Li⁺ 자리에 **보상 없이** 넣는다 | ⭕ **화학식 수준 중성**(`Cl₆Li₂₆Nd₂O₃P₂S₁₅` = +42/−42, +2 Li/Nd) |
| 묽은극한 | ⛔ **33.3 % 치환** | ⚠ 우리도 묽은극한 아님 — **단 우리는 그걸 "조성" 이라 부르고 그들은 "결함" 이라 부른다** |
| 스핀/열린껍질 | ⛔ 0건 — **Gd 4f⁷(S=7/2)를 비편극 PBE, U 없음, 4f 원자가/코어 미기재** | ⭕⭕ **frozen-4f**(`Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF`, z=11) + *"Nd 4f 주장 전면 금지"* |

⇒ **"M³⁺ 가 격자에 들어가나" 의 표준은 결국 우리가 세워야 한다.** litdb 에서 가장 가까운 셋(**[Ren26]** 할라이드 · **[Anderson24]** LLZO · 본 편 antiperovskite)이 **계도 형식론도 서로 다르다.**

**(2) 🔴 검산으로 잡은 것 7건 (전부 논문 본문·표에서 재현 가능)**

| # | 항목 | 내용 |
|---|---|---|
| **A** | 🔴🔴 **형성에너지 부호 해석이 자기 정의식과 반대** | Eq.(1) `E_f = E_def − E_perf + E_Li − E_A` 는 표준형이라 **양수 = 비용**. `Table 2` 는 전부 양수이므로 **He 4.54 · B 4.57 = 가장 싼 치환**, **H 20.00 = 가장 비싼 치환**. 그런데 본문은 He 를 *"one of the **least favorable**"*, B 를 *"**less favorable**"*, H 를 *"strong energetic **driving force for incorporation**"* 이라 읽는다 — **"큰 양수 = 더 안정" 이라는 반전 규약**이 §3.2.2·§4 를 관통한다. ⚠ 대안가설(표값이 `−E_f`)이면 **Eq.(1)과 표가 안 맞는다** — 어느 쪽이든 내부 불일치. ⇒ **어떤 값도, 어떤 순위도 인용 불가** |
| **B** | 🔴🔴 **"1×1×1 supercell" 이 슈퍼셀이 아니다** | Li₃OCl 구조원 = **5원자**(Li 3+O 1+Cl 1). Li 1개 치환 = **Li 자리의 33.3 %**, 화학식 **Li₂AOCl = 정렬 합금**. 논문은 **결함 농도를 숫자로 한 번도 안 적는다**(`concentration` 은 *"consistent defect concentration"* 한 번뿐). 게다가 이종원자가를 **보상 없이** 넣어 잉여 전하가 띠로 흡수 ⇒ **계가 금속화**, 그래서 *"Gaussian smearing … for metallic systems"* 가 필요했다(논문 자신의 한 줄이 증거) ⇒ **1가(절연) vs 2·3가(금속)를 같은 표에서 비교하는 것이 원리적으로 불가** |
| **C** | 🔴🔴 **부피가 물리적으로 불가능** | B 치환 `V = 9.05 Å³/5원자 = **1.81 Å³/원자**` — 다이아몬드 **5.67**, 오스뮴 **13.98** 보다 조밀. 기하로도 `a=b=**1.76 Å**` 라 **주기 이미지 Cl···Cl 이 1.76 Å**, 이는 **Cl₂ 공유결합 1.988 Å 보다 짧고** Cl⁻ 지름 3.62 Å 의 절반 이하. 기전: **QE vc-relax 는 시작 셀의 평면파 기저를 고정**하는데 ΔV 가 **−85 %~+189 %** 이고 **최종 셀 재실행 여부 미기재** ⇒ `Table 1` 격자·부피·대칭 열 **전부 인용 불가** |
| **D** | ⚠ **크기 논증이 Shannon 이 아니라 *반데르발스* 반경** | `Table 1` 각주가 *"atomic radii (**van der Waals**) … from NCBI"* 명시. 값 전수대조 = Bondi/PubChem vdW. 그래서 **B³⁺(Shannon 27 pm, IV)가 표에서 192 pm 로 Li(182)보다 크게** 나온다 — 정작 §3.2.1 의 B 서사("강한 B–O 앵커")는 **B 가 작아서** 생기는 현상이다. **⇒ 우리 Shannon 대리지표가 이 편보다 낫다. 낮춰 부를 필요 없다** |
| **E** | 🔴 **본문 좌표가 `Fig. 1` 과 모순 (그림 실독으로 잡음)** | §2 는 Li 를 **(0,0,½)·(0,½,0)·(½,0,0) = 3d 모서리중심**에 두면서 **치환 자리를 (½,½,0) = 3c 면심**이라 적는다 — **치환 자리가 자기 Li 목록에 없다**. 3d 에 Li 를 두면 Li₆**Cl** 팔면체가 되는데 **`Fig. 1` 은 Li₆O 팔면체를 그리고 범례에 그 이름을 박았다** ⇒ **그림이 맞고 본문 좌표가 틀렸다**. 추가: Pm3̄m 은 **d(Li–O) ≡ a/2** 를 대칭으로 강제 ⇒ a=3.884 면 **1.942 Å** 인데 표는 **1.99**(=a 3.98) ⇒ **pristine 행 자기모순**, 그 행이 모든 ΔV 의 기준이다 |
| **F** | 🔴 **"작은 셀로 충분" 논증 5구멍** | ① Eq.(2)의 `E⁽¹⁾/L` 은 **하전**결함 Makov–Payne **단극자 보정**인데 결함을 **중성으로** 다룬다(중성이면 선도항이 1/L³) ② 셀 3종의 **공공농도가 27배**(33.3→4.2→1.2 %)인데 E_f 는 **1.5 %만** 움직인다(14.714→14.550→14.496) ③ **k-격자 동반 축소 여부 미기재** — 5×5×5 고정이면 k-밀도가 27배 달라 "유한크기 수렴" 이 k-수렴과 뒤섞인다 ④ 선행 근거인 LiBO₂ 는 셀↑에 E_f 가 **올라가는데**(6.87→6.91→6.98) Li₃OCl 은 **내려간다** — **부호가 반대인데 같은 근거로 쓴다** ⑤ `Fig. 3` "지수적 비용"(C₀ 0.2029 CPU·h, L₀ 4.1083 Å)은 **3점이라 멱법칙과 구별 불가**(실제 DFT 는 O(N³)=O(L⁹)). ⇒ **우리가 "작은 셀 스크리닝" 을 정당화할 때 이 논문을 인용하면 안 된다** |
| **G** | ⚠ **산술 오기 + 대조 회피** | `Table 1` Na 의 **V = 76.62**(4.21³ = **74.62**, ΔV 27 % 는 74.62 와 맞음) · K 의 **ΔV = 163 %**(148.04/58.58 → **152.7 %**, 10 %p 틀림). 그리고 **자기가 인용한 Emly[18]·Zhang[19]·Lu[17] 가 같은 물질의 Li 결함 에너지를 계산했는데 자기 값(14.39–14.714 eV)과 한 번도 대조하지 않는다** |

**(3) ⭕ 반대로 이 편이 우리에게 주는 것 — 수치 0건, 규율 6개**

| # | 이식 | 우리 쪽 상태 |
|---|---|---|
| **T1** | **결함이라 부르려면 농도를 숫자로 적는다** | `ndo_lpscl16` 은 조성식으로 x 가 드러나 이미 막혀 있다. **앞으로 "Nd 결함 형성에너지" 라고 쓸 땐 x 를 병기**한다 |
| **T2** | **부피가 크게 바뀌는 vc-relax 는 최종 셀에서 재실행**(QE Pulay) | 우리 도핑계는 부피 변화가 작을 것으로 보이나 **명시 확인·기록** 필요 (⚠ 현재 규약에 이 줄이 없다) |
| **T3** | **셀 크기가 다르면 k 를 *밀도*로 고정**(격자수 고정 금지) | 이 편은 유효 `Δk = 2π/(5a)` 가 **0.227(Ca)~0.714(B) Å⁻¹ = 3.1배 불균일** ⇒ 도펀트 비교가 등가 조건이 아니다. **우리 Track1 vs Track2 처럼 셀이 다른 계를 비교할 때 직결** |
| **T4** | **열린 껍질은 스칼라 보고량이 정의되는지 먼저 묻는다** | 🔑 **우리 frozen-4f Nd 결정의 외부 반례 1건 확보** — 이 편의 Gd(4f⁷)가 비편극·U 없음·4f 처리 미기재다. `kb/templates/estimand_card.md` §3 "열린 껍질" 칸의 실물 표본 |
| **T5** | **이온결정 치환의 크기 논증은 Shannon 이온반경** | 이미 우리가 그렇게 한다 — **이 편이 그 선택이 옳았다는 음성 대조군** |
| **T6** | **표를 실으면 산술 자기일관 검산**(V ↔ a·b·c, ΔV ↔ V/V₀) | 이번에 오기 2건을 이 검산으로 잡았다. 우리 Origin-ready CSV 규약이 같은 역할 |

**(4) ⛔ 이 편에서 우리 축으로 이식 금지**

| 금지 | 사유 |
|---|---|
| `Table 2` 형성에너지 **값·순위 전부** (H 20.00 / Na 8.69 / K 8.14 / He 4.54 / Ba 7.81 / Ca 8.09 / Mg 7.18 / B 4.57 / Gd 7.44 / Al 6.21 eV) | (2)-A 부호 반전 + (2)-B 전하보상 0건 |
| `Table 1` 격자·부피·**ΔV**·대칭 (−85 %~+189 %) | (2)-B 33 % 치환 + (2)-C vc-relax 기저 |
| **"Li–O 신장 = 빠른 Li 전도" 기술자** | **저자 스스로 미검증 선언** — *"NEB 와 대규모 MD 로 검증돼야 한다"* |
| **"1×1×1 로 충분" 논증** 및 `Fig. 2`/`Fig. 3` 적합식 | (2)-F 다섯 구멍 |
| **Li 공공 14.39 / 14.496 / 14.550 / 14.714 eV** | 33 % 공공 + 중성/하전 혼선 + 자기 인용문헌과 미대조 |
| **σ·Ea·gap·ESW·C_ij** | 애초에 계산 0건 |
| **원고·SI 인용 자체** | arXiv v1 미심사 + 저널 DOI 없음(기관 핸들) |

<sub>> 📎 2026-09-22 신설 — `litdb/papers/ziemke2026_li3ocl_substitutional_defects.md` §7·§10·§11 요약. 그림 3/3 실독.</sub>


**[Xu26XLS] `xu2026_xlsdft_linear_scaling_100m_atoms` — O(N) KS-DFT 의 *조건과 대가* · ⛔ 우리 기계로 불가** (2026-09-22 신설)

> **arXiv:2609.13115v1 [cs.CE]** (2026-09-11, **미査読·DOI 없음**) · Qimen Xu\*/Yu Zhang\*(공동1) … **T. Hoefler**(ETH)/**H. Fu**(칭화)/**Y. Lu**(중산) · NSCC-SZ.
> ⛔ **물성 4축 진입 금지 — 사유 (i) 값이 0 건이다.** σ·Ea·ESW·C_ij·밴드갭 전부 `n/a`. DOS/PDOS 를 계산하고도 **갭 값을 보고하지 않는다**.
> ⛔ **축 E(환원/Li 금속 계면)에도 행을 만들지 않는다** — 계면 환원이라는 *현상*은 우리 축과 같지만 **물질이 LGPS(Ge⁴⁺ 중심)** 라 우리 argyrodite 와 다르고, 결과가 **정성 관찰 + 오차막대 없는 `figure-read` 2 % 차이**뿐이다.
> 여기 두는 이유는 하나 — **1저자가 던진 네 질문("O(N) 이 언제 성립하나 · 정확도 대가가 뭔가 · 실험 대조 프로토콜이 옮겨오나 · SE 계를 썼나")에 근거로 답하는 편**이기 때문이다.

**a. 우리 스택 대조 — 규모·방법·관측량**

| 항목 | [Xu26XLS] | 우리 | 판정 |
|---|---|---|---|
| 계 크기 | Si **1억/2억** · Li\|LGPS\|Li **11,325,600**(57×44×90 nm) | 120–400 원자, **생산 상한 160** | 🔴 10⁴–10⁵ 배 |
| 기계 | LineShine **20,480 노드** (노드당 ARMv9 LX2 ×2 = **608 코어** + HBM 64 GB / DDR 512 GB) | RTX3090 1대(kgy) · A6000 1대(gabia), **HPC 없음** | 🔴 **재현 불가** |
| **실제로 대각화하는 국소 문제** | 부분영역 **N_s^α ≈ 640 상태 · N_d^α ≈ 200,000 격자점** ⇒ **O(10²) 원자** (Si 환산 320(상태) / 185(격자) — 논문이 코어크기를 안 적어 1.7× 이상 못 좁힘) | **120–160 원자** | ⭕⭕ **같은 자리다.** 큰 계는 이 단위를 *많이* 푸는 것이지 *크게* 푸는 것이 아니다 ⇒ **우리 셀 크기를 방어하는 근거** |
| 처리량 | **노드당 5,120 원자 / SCF 71.2 s** (`Fig. 5` 캡션) | — | 코어수만으로 gabia 환산 **≈170 원자**. ⚠ 그들 코어는 SME 행렬유닛 + HBM 이라 실제 우리 쪽은 **더 낮다** |
| 이산화 | 실공간 **FD 12차**, h ≈ 0.5(Si)/0.4(LGPS) Bohr, **ONCV**, **Γ점만**, **스핀 무시** | QE **평면파** ecutwfc 70/560, k-격자, PAW/USPP | 🔴 수렴 손잡이가 다르다 (**h ↔ ecut 환산식 없음**) |
| 범함수 | **"GGA" 라고만** (PBE 인지 PBEsol 인지 **미기재**) | PBE | ⚠ 대조 불가 |
| 스미어링 σ = k_BT | **값 미기재** | — | 🔴 금속계 버퍼 적정성을 **독자가 판정할 수 없다** |
| SCF 문턱 | 상대 밀도잔차 **5×10⁻⁴** (두 계 공통) | — | ⚠ 느슨한 편 + 근거 없음 |
| XLSDFT 로 한 일 | **단일점 SCF 1회.** 구조최적화 0 · MD 0 · NEB 0 · **힘 값 보고 0** | — | 구조는 전부 **DeePMD MLFF-MD** 가 만들었다 |

**b. ★ O(N) 이 성립하는 조건 — 갭은 필요조건이 아니다 (1저자 질문 ①의 답)**

- 원문 §V-A1: *"for insulating **as well as metallic** systems **at finite temperature** [32],[33], the density matrix decays exponentially, `|D(x,x′)| ≲ exp(−|x−x′|/ξ)`, whereas the individual KS orbitals ψₙ may be fully delocalized."*
- ⇒ 조건은 **"갭이 있을 것"이 아니라 "밀도행렬 감쇠길이 ξ 가 버퍼 반경보다 짧을 것"**. 넓은 갭 → ξ 짧음(유리) · 금속 → σ 가 작을수록 ξ 길어짐(불리).
- **우리 계(PBE gap 2.066 / 2.099 eV)는 이 방법이 가장 잘 듣는 쪽 끝에 있다** — 이 논문이 다룬 Si(≈1 eV급)·Li 금속(0)보다 유리하다. 🔴 **그런데 그게 우리에게 이득이 아니다** — 이유는 c·d.
- ⚠ **ξ 값도 σ 값도 버퍼 수렴시험도 이 논문에 없다** ⇒ *"우리 계면 버퍼 얼마면 되나"* 를 여기서 못 가져온다. (그 답은 인용 [35] Suryanarayana, *CPL* **679**, 146 (2017) *"On nearsightedness in metallic systems …aluminum"* 쪽으로 보이나 **우리는 그 논문을 읽지 않았다 — 서지만 확인**.)

**c. 🔴🔴 정확도 대가 — 이 논문은 그 질문에 답하지 않는다 (1저자 질문 ②의 답)**

- 전문 검색: `benchmark` **0회**, 3차 스케일링 코드와의 대조 **0건**, 오차 보고 표·그림 **0개**, **R_buffer 수렴시험 0건**. *"retaining DFT accuracy"*(초록)는 **주장이지 측정이 아니다.**
- 🔴 더 나쁜 것: **금속 포함계(Li/LGPS)에 더 *작은* 버퍼 8.0 Bohr**, **순수 반도체 Si 에 더 큰 9.2 Bohr** — 근시안성 이론이 요구하는 방향과 **반대**이고, 논문은 설명하지 않는다(정황상 h=0.4 Bohr 의 비용 제약).
- **구조적으로 무엇이 없어지는지는 정식화에서 읽힌다** (이게 우리에게 진짜 중요한 부분):

| 양 | 이 정식화에서의 지위 | 우리 영향 |
|---|---|---|
| **ICOHP / COHP / COBI** | 🔴 **자리가 없다.** COHP 는 두 원자 궤도쌍의 **비대각 `H_μν`** 를 요구하는데, 이 정식화는 부분영역 고유값 `λ^α_n` + **대각** 투영가중치 `c^α_n`·`P^α_{n,I,lm}` 만 조립한다 (Eq. 13–16). LOBSTER 가 필요로 하는 것을 이 코드는 만들지 않는다 | 🔴🔴 **우리 전자구조 축의 중심 지표가 통째로 빠진다** (`comp1 ICOHP(Li–Cl) −1.86` / `modelc −2.10` 같은 값을 이 노선으론 못 낸다) |
| **밴드갭** | DOS 는 **전역 H 의 스펙트럼이 아니라 부분영역 H^α 고유값 모음**이다. 논문은 갭을 보고하지도 않는다 | 🔴 우리 규율(**fixed-occ nscf VBM/CBM 고유값**)로 정의할 방법이 없다 |
| 밴드분산 / k-분해 | **없다** (Γ점만, Eq. 1 명시) | 🔴 원리적 불가 |
| 스핀 분해 | **없다** (스핀 무시, Eq. 1 명시) | 🔴 열린껍질·라디칼·자성계 불가 |
| PDOS | ⭕ 있다 (Eq. 14–16) — 이 논문이 실제로 낸 **유일한** 전자구조 관측량 | ⭕ |
| Bader · 정전기퍼텐셜 | §III 이 *"native 로 계산"* 한다고 **주장만** 하고 **결과가 없다** | ⚠ 미확인 (그래서 digest `methods:` 태그에서 Bader 제외) |

⇒ **판정: 우리가 DFT 를 쓰는 이유(ICOHP·밴드갭·PDOS 성격) 중 둘이 이 노선에서 사라진다. 우리 기계가 작아서가 아니라 방법의 성질이다.**

**d. 🔴 "Bridging … Experiments" 는 추세 일치까지다 (1저자 질문 ③의 답)**

| | 실험 | 계산 |
|---|---|---|
| 양 | Ge 3d · P 2p **XPS 결합에너지** (eV) | **E_F 이하 점유 PDOS 적분** (무차원) |
| 공간축 | Ar⁺ **스퍼터 시간** 0/20/50 분 | **x (nm)** 25–65.5 |
| 겹쳐 그림 / 맞춘 숫자 | **없음 / 없음** | |

- 초록 *"in **quantitative** agreement"* ↔ 본문 *"The consistent interface-to-bulk **trend** validates…"* — **강도가 다르다**. 대조된 것은 **부호/추세**다.
- **스퍼터시간 → 깊이(nm) 환산이 없다** ⇒ 두 축이 원리적으로 안 만난다. **XPS 엔 `O 2s` 가 뚜렷한데 모델 LGPS 엔 O 가 없다**(조성 불일치).
- 신호 크기 `figure-read ≈`: Ge 벌크 **8.06** → 계면 **8.22** (Δ ≈ **2.0 %**) · P **3.41 → 3.47** (Δ ≈ **1.8 %**), **산점 퍼짐이 Δ 의 4–5배**, **오차막대·통계 없음**.
- ⛔ **우리 XPS anchor 논증(`Li₂S 160.2 / PS₄³⁻ 161.6 / Li₂SO₄ 168.0 eV`)의 근거로 이 편을 쓰면 안 된다** — 그쪽은 결합에너지끼리 맞춘 것이고 이쪽은 아니다.
- ⭕ **옮겨올 것은 구조 하나**: *"실험이 주는 축(깊이 프로파일)이 무엇인지 먼저 정하고, 계산도 그 축으로 낸다."* 진짜 정량 대조를 하려면 **core-level 결합에너지/화학적 이동을 계산**해야 하고 그건 이 논문이 **하지 않은** 일이다.

**e. ⭕ 이 편에서 실제로 가져오는 것 3개**

| # | 가져오는 것 | 등급 |
|---|---|---|
| 1 | **MLIP(구조) → DFT(전자구조) 분업의 최대규모 선례.** §IV-A: *"MLFFs … provide near-DFT accuracy for atomic forces and energies at millions of atoms **but yield no electronic-structure observables**: band alignment, charge transfer, and projected DOS are entirely inaccessible."* ⇒ 우리 **UMA-MD + QE** 노선의 외부 정당화 | ⭕⭕ **인용 1문장** (계산 0회) |
| 2 | **물질-마스크 SCF 전처리** `(−∇²+κ²(x))R̃ₖ = −∇²Rₖ`, **κ²(x)=s(x)·k²_TF,Li** — 금속(Li) 영역에서만 Thomas–Fermi 스크리닝 ON, 절연 LGPS 에서 OFF. 우리 CLAUDE.md 의 *"local-TF/저β 믹싱"* 의 **공간 마스크판** | ⭕ **T2 (개념만)** — ⚠ 새로 구현할 것이 아니라 **QE `mixing_mode='local-TF'` 를 이미 켜고 있는지 입력파일에서 확인**(계산 0회, 규율 사다리 ③) |
| 3 | **면내 불균일성** (`Fig. 6d` xy 맵) — 같은 계면거리에서 y 방향으로 값이 크게 흔들린다 | ⭕ **§H 에 등재 완료** (2026-09-22). **우리가 못 하는 것이고 얼버무리지 않는다** |

**f. 🔴 우리 검산 — 논문에 없는 수 (⚠ 소환값이 아니라 우리가 나눈 파생값이다)**

| 검산 | 값 | 무엇을 말하나 |
|---|---|---|
| 200M/100M **s/SCF 비** | 143.7 / 71.2 = **2.018** | 같은 20,480 노드에서 원자 2× → 시간 2.02× ⇒ **진짜 O(N) 이다.** 이 편에서 제일 깨끗한 증거 |
| 헤드라인 지속성능의 **피크 대비** | 157.9 / 2,470 Pflop/s = **6.4 %** (노드 피크 = 2×60.3 Tflop/s) | dense-LA 만 48 %(proj)·53 %(rot). **체비셰프 필터링(0.97 flop/byte, 메모리대역 한계)가 전체를 끌어내린다** |
| Li/LGPS 지속 HBM 대역 / 피크 | 0.186 / 5.74 = **3.2 %** (Si 는 **50.7 %**) | **16배 차.** 실제 재료 문제는 벤치마크 결정보다 훨씬 나쁘게 돈다 — 논문은 표에 넣고 **한 문장도 논의하지 않는다** |
| **원자당 비용** LGPS vs Si | (36.4/11.33)/(71.2/104.86) = **4.7×** | 화학 복잡도·금속성·미세격자(h 0.4 vs 0.5)의 대가 |
| Li/LGPS **단일점 SCF 1회 비용** | 20,480 × 6,936.2 s ≈ **39,500 node-h ≈ 2.4×10⁷ core-h** | ⚠ **노드수가 논문에 없다** — §VII-B 의 대역 외삽이 20,480 을 쓰므로 그렇게 가정. 재현·비용비교가 원천적으로 막혀 있다 |
| Si 런의 초기화+I/O 비중 | 100M **54 %**(584 s) · 200M **56 %**(1,275 s) | 기록 런은 wall time 절반 이상이 계산이 아니다 |
| **버퍼 오버헤드** | `Fig. 3` figure-read **푸는 부피 / 보관 부피 ≈ 40×**; 숫자로도 코어가 부분영역의 **5.1 %(Si) / 3.2 %(LGPS)** (정육면체 가정) | **O(N) 은 공짜가 아니라 큰 상수를 내고 산 지수다** |

**g. ⛔ 이 축에서 인용하면 안 되는 것**

| 금지 | 사유 |
|---|---|
| *"O(N) DFT 는 정확도 손실 없이 3차 스케일링과 같다"* | 🔴 **이 논문에 정확도 수치가 0 건**이다 (c) |
| *"DFT 가 XPS 와 정량 일치했다"* | 🔴 축·단위가 다르고 겹쳐 그린 적이 없다. 본문 자신이 *"trend"* 라 쓴다 (d) |
| **157.9 Pflop/s** 를 "DFT 가 이만큼 빨라졌다" 로 슬라이드에 쓰는 것 | 20,480 노드 **피크의 6.4 %**. 노드수 없이 쓰면 오도 (f) |
| "저원자가 Ge/P 농축" 을 **우리 argyrodite** 환원 서술의 근거로 대는 것 | **물질이 다르다** (LGPS 의 Ge⁴⁺ ↔ 우리는 Ge 없음). *중심 양이온이 환원된다*는 일반 서술까지만 |
| 이 편의 DOS/PDOS 를 **우리 LOBSTER/ICOHP 축과 같은 것**으로 다루는 것 | 정식화가 다르다 — 비대각 `H_μν` 부재 (c) |
| 그들의 **MLFF 정확도**를 우리 UMA 논의에 끌어오는 것 | **검증 수치가 0 건**이다 (학습 프레임수·힘 RMSE·앙상블·dt·길이 전부 미기재). 우리는 `mlip_bench_li3ps4_uma.json` 힘 MAE **30.0 meV/Å** 를 갖고 있다 — **이 축은 우리가 낫다** |
| "LGPS" 관련 구조·조성 수치를 이 편에서 가져오는 것 | **화학식(Li₁₀GeP₂S₁₂)조차 전문에 한 번도 안 나온다.** 공간군·격자상수·원소별 원자수·Li 무질서 처리 전부 미기재 |

<sub>> 📎 2026-09-22 신설 — `litdb/papers/xu2026_xlsdft_linear_scaling_100m_atoms.md` §4·§9·§12·§15 요약. 크로핑 6장 중 5장 실독(`Fig. 4` 는 LX2 다이 배치도라 의도적 미독, `Fig. 5` 는 자동크롭 실패 → 수동 bbox). ⛔ **당장 할 계산 없음** — 이식 가능한 것은 인용 1문장 + 계산 0회 점검 2줄뿐.</sub>



#### 🔧 방법 원전 — 시드 · 독립궤적 · MSD 오차 추정

**`pranami2015_estimating_error_diffusion_coefficients_md`** (JCTC 2015) — LJ 유체 + 프랙탈 응집체, 물성값 없음.

| 이 논문이 요구하는 것 | 우리 현행 | 판정 |
|---|---|---|
| δ 를 R_SD(τ,δ) 로 측정, **δ ≥ τ** (겹치지 않는 시간원점) | δ = 저장간격 **0.1 ps** 고정, τ ≤ 50 ps → **겹침 500배** | ❌ 미준수 |
| MSD~τ 회귀가 뱉는 D 오차는 **무효** (정규성 W=0.87 p<1e-4 · 등분산 위반) | 오차막대를 **시드**에서 낸다 (600 K 3-시드) | ✅ 준수 |
| 오차는 **MIS(다중 독립 시뮬레이션)** 의 D 표본에서 t-CI | 시드 3 | ⚠ 목적별 (아래) |
| D 표본의 **정규성 검정** 후 t-CI | 한 적 없음 (3점으론 불가) | ❌ 불가 |
| 등분산 깨지면 **WLS** | MSD 창 2–50 ps **등가중 OLS** | ❌ 미준수 |
| 유한크기 **D vs 1/L** 외삽 | 셀 크기 **1개** → 보정 불가 | ❌ 불가 |

**시드 산포 비교** (CV = σ/μ):
| 계 | CV | 출처 |
|---|---|---|
| LJ 유체 N=1000 (100 시드) | **0.11 %** | 논문 SI §2 (소환값) |
| LJ 유체 N=125 (100 시드) | **0.20 %** | 논문 SI §2 (소환값) |
| 프랙탈 응집체 1개 (10 시드) | **2.7–4.1 %** | Table 3 역산 *(digest 계산)* |
| **우리 MLIP-MD (Li in argyrodite)** | **≈ 22 %** | 3-seed×3-T 재시드 *(digest 계산)* |

**🔴 우리 시드 3개 판정** *(digest 계산 — 이 논문의 Step 5 식 + 우리 실측 CV 22.1 %)*:
- 단일 D 의 3시드 95 % CI 반폭 = **±63 %** (LPSCl1.6 600 K 실측)
- 비(ratio)의 3시드 95 % CI = **×[0.61, 1.65]** (폭 2.7배)
- ⇒ **R ≥ 2 (자릿수·2배급) 주장 → 3시드로 충분**
- ⇒ **R ≈ 1.33 급 주장 → 계당 6–8 시드 필요**
- ⇒ **"동등하다" 주장 → 수십 개 필요** ⇒ 반드시 **"구별되지 않는다(not distinguished)"** 로 표현
- ⇒ 철회된 **단일시드 1.33× 는 0.91 σ** (= 순수 시드 잡음). 2026-07-09 철회가 **사전에 계산 가능했다.**
- ⛔ 이 논문은 **비(ratio)의 오차를 다루지 않는다** — 위 비 계산은 우리가 붙인 로그공간 전파다.
- ⛔ 유한크기 보정식은 **hydrodynamic** 기원이라 고체 전해질 Li 홉핑에 **이식 금지**.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_pranami2015_estimating_error_diffusion_coefficients_md.md` ## ② .</sub>

### J-11. ★★★ **해석가능 ML 감사 — [Honrao21] SHAP·PFI vs 우리 cascade predictor** (2026-09-12 신설)

> ⚠ **[Honrao21] 자체는 축 A·B·E 에 이미 행이 있다**(softBV 장벽·grand-potential 창). 여기는 **ML 방법 부분만** 따로 둔 것이다.
> ⛔ **그들 R²(장벽 0.86 · 전위 0.95/0.92)를 우리 cascade 숫자와 같은 표에 놓지 않는다** — 규약이 다르다(그들 **자기 DB 내부 랜덤 90:10 × 20회**, 우리 **LODO**). [Tu27ML] R²=0.99 ↔ 우리 LODO −0.18 선례(§J-8)와 **정확히 같은 함정**이다.

| 항목 | **[Honrao21]** | **우리 cascade predictor** | 판정 / 우리 작업거리 |
|---|---|---|---|
| **모델** | scikit-learn **GradientBoosting**(주) + RandomForest(비교). 표적 3개 = **독립 모델 3개** | (cascade 단계별 대리모델) | 🟢 같은 계열. 이 편은 *"앙상블은 소·중규모 혼합형 표 데이터에 강하고 스케일링이 필요 없다"* 는 **선택 이유를 명시**한다 — 우리 문서에도 그 한 줄이 필요하다 |
| **검증 규약** | 격자탐색 + **10-fold CV** → **20회 랜덤 90:10** 평균, **held-out test 만** 보고. ⛔ **표준편차 없음** | **LODO**(leave-one-dopant-out) | 🔴 **비교 불가**. 랜덤 분할은 같은 화학족이 train/test 에 흩어져 **낙관 편향**. ⇒ 그들 R² 는 **우리 지표와 같은 표 금지** |
| **특징 — 구조** | **22개**(`Table 1`): `Li` 분율 · `LNC`·`LLB`·`SNC`(4 Å 이웃수) · `SBI`·`ENS` · `LLSD`·`LASD`·`AASD` · `NDV` · `OP_1..3`(Warren–Cowley) · **`DLFS`**(Zeo++ 최대 자유구) · `SLPW` · **`SPF`**(부격자 충전율) · `MPE` · **`XRD_1..5`**(pymatgen 패턴 PCA, 분산 0.65) | (조성·도펀트 기술자 중심) | ⭐ **가져올 후보 4개**: **`SPF`·`DLFS`·`Li` 분율·`SNC`**. 우리 **BVSE 채널%** 와 *같은 물리를 다른 축으로* 재는 스칼라라 **기술자 열로 바로 붙는다**. ⚠ 우리 계는 무질서 ⇒ **배열 평균**이 필요(그들은 단일 폴리모프) |
| **특징 — 조성** | **28개**(`Table 2`): 원소물성 8종 ×{평균·최대·범위}=24 **+ 신설 산화상태 특징 4개** — `Σ\|V_i − min{V_i}\|`, `Σ\|max{V_i} − V_i\|`, 그리고 각각에 **Pauling 전기음성도 가중** | — | 🔑 **이 4개가 이 논문의 진짜 발명**. *"이 원소가 더 산화/환원될 여지가 있나"* 를 숫자로 만든 것이고, `Fig. 4b` 에서 **산화전위 PFI 2위(0.203)** 로 올라온다(환원에서는 4위) ⇒ **산화·환원의 비대칭이 데이터에서 나온다** |
| **해석 도구** | **SHAP**(개별 예측 분해, base 1.490 eV, `Fig. 2`·`S9`) + **PFI**(시험셋 R² 하락, `Fig. 3`·`4`). **불순도 기반 중요도를 명시 거부**(*"always computed on the training set … strongly biased towards high cardinality features"*), 상관 특징은 **클러스터링 후** PFI | — | ✅ **이 두 판단은 그대로 채택할 만하다**(불순도 중요도 거부 · 상관 클러스터링). 우리 cascade 감사 문서에 같은 규율을 박는다 |
| **PFI 결과 (장벽)** | **`SPF` 0.31 압도 1위** → `Li` 0.134 → `XRD_1` 0.098 → `DLFS` 0.096 → `SNC` 0.093 → `ENS` 0.066 (figure-read) | — | ⭐ *"Li 이동은 부격자가 공간을 얼마나 먹었나로 결정된다"* — 우리 BVSE 채널% 서사와 **같은 물리, 다른 언어** |
| **⛔ 해석가능성 *검증*** | **사실상 없다.** 인과 근거는 **치환 일화 2건**뿐: LSiPO 0.305 → LSnPO **0.518** / LSiPS **0.457** | — | 🔴 **두 건 모두 깨져 있다**: ① *"**by simply changing the SPF**"* — Si→Sn 치환은 `ENS`·`SNC`·`AASD`·`MPE`·`XRD_1..5` 를 전부 바꾼다. 한 특징만 바꾼 벡터는 **물리적으로 존재할 수 없는 입력** ② `LSiPS 0.457` 은 **모델 출력이 아니라 softBV 계산값**(`Fig. 1` 마커 **0.456**, 본 digest 픽셀) — 본문이 구분하지 않는다 ③ n=2, 통계·반례탐색 0 ④ 표적이 softBV 라 맞아도 *"모델이 프록시를 잘 흉내 낸다"* 까지다. ✅ **공정하게**: 논문 스스로 *"PFI analysis and Shapley explanations do not necessarily provide causality"* 라고 **물러선다** — 주장 크기는 정직하고 **검증이 없을 뿐** |
| **⚠ 자기 SI 의 약한 반증** | `Fig. S10` Pearson 히트맵에서 **`SPF`–`E^b` 상관이 옅다**(`E^b` 행에 진한 칸이 없다, figure-read) | — | PFI 1위인데 **선형 상관은 약하다** = 비선형·상호작용 지배. 본문은 *"the same positive and negative correlations"* 라고 **부호만** 확인하고 넘어간다 ⇒ **"중요도 ≠ 단조 관계"** 의 사례로 인용 가능 |
| **⛔⛔ 가장 큰 구멍 — 게이트와 지표가 어긋난다** | 코팅 판정은 **`V_red = 0 V` 불리언**인데 훈련은 **회귀**. `Fig. S11a` 3.2× 확대에서 **`DFT = 0` 축에 수직 띠** — 진짜 0 V 인 화합물이 **최대 ≈0.8 V 까지 예측**된다(figure-read) | 우리도 후보를 **통과/탈락**으로 거른다 | 🔴🔴 **이 회귀 모델로는 자기 논문의 코팅 스크리닝을 재현할 수 없다.** 그런데 **분류 지표(정밀도·재현율)를 한 번도 보고하지 않고**, 26종 재현 시험도 없다. ⇒ 🔑 **우리에게 즉시 적용되는 규율**: **게이트가 불리언이면 회귀 R² 는 그 게이트의 성능을 보증하지 않는다.** 우리 cascade 도 선별 단계마다 **선별 과제 자체의 지표**(재현율/정밀도 또는 순위상관)를 따로 낸다 |
| **재현성** | ⛔ **기계판독 데이터 0본.** 15,446행 DB·250+ SE 목록·특징 생성 스크립트 전부 *"available upon request"* | — | [Aykol16] CSV 2본 · [Nolan19]/[Nolan21] XLSX 와 **정면 대비**. 계보 6편 중 **가장 닫혀 있다** |
| **⚠ 논문 내부 불일치** | **초록 ↔ `Table 5` 가 R² 의 축을 서로 뒤집어 적는다**(초록 *"0.95 and 0.92 on the **oxidation and reduction**"* ↔ 표 **환원 0.95 / 산화 0.92**) | — | **축을 지정해 인용하면 50 % 확률로 틀린다.** *"환원·산화 각각 0.95·0.92(논문 내부 불일치)"* 로 쓰거나 축을 말하지 않는다 |

### J-9. ★★★ **능동학습(AL) 축 — [Cho25AL] 실험 PSO · [Ma25AL] GP-EI vs 우리 cascade** (2026-09-09 신설)

> **두 편 합본 판정 (2026-09-09).** 같은 날 두 편이 같이 들어왔고, 둘을 겹쳐 놓아야 답이 나온다.
> **[Cho25AL]** 은 argyrodite 실험 AL — **재료계가 우리와 같고 대리모델이 아예 없다**.
> **[Ma25AL]** 은 액체 전해질 AL — **재료계는 다르지만 루프가 상세하고 Source Data 가 공개돼 재계산이 됐다.**
>
> 🔑 **겹쳐서 나오는 것 하나**: 두 편 다 *"AL 이 랜덤보다 낫다"* 를 증명하지 않았다 —
> [Cho25AL] 은 그 수치를 안 냈고(우리가 Table S1 에서 재계산해 **4.5×**, 원시 15× 는 공정변수 교락),
> [Ma25AL] 은 enrichment·랜덤 arm·귀무모형이 **0건**이다. 그런데 **[Ma25AL] 의 대리모델은
> out-of-sample 설명분산이 ≤ 0** 이었고(우리 재계산), **[Cho25AL] 은 대리모델 없이도 4.5× 를 냈다.**
> ⇒ **좋은 예측기는 이 루프의 전제가 아니다.** 우리 `LODO −0.1805` 는 착수를 막는 이유가 못 된다.
> ⛔ 단, 두 편이 굴러간 공통 이유가 **라벨이 실측**이라는 것이고 **그게 우리에게 없다** —
> 우리 라벨은 UMA-MD 대리값이라 AL 이 MLIP 편향을 학습·**증폭**한다.
> (그래서 [Cho25AL] 이 준 답: **대리모델을 빼고 MD 를 오라클로 직접 쓰면 편향이 상수로 남는다.**)
>
> ⚠ 아래 두 소절의 표는 **각자 자기 논문의 열**로 읽는다. 세 열로 합치지 않은 이유는
> 두 편의 축이 실제로 다르기 때문이다 — [Cho25AL] 에는 acquisition·불확실도 행 자체가 없고,
> [Ma25AL] 에는 공정변수·엘리트 승계 행이 없다. 억지로 한 표에 넣으면 빈 칸이 판정처럼 보인다.

#### J-9a. [Cho25AL] — 실험 PSO 닫힌고리 (대리모델 없음)

> **왜 이 블록이 있나**: 2026-09-09 litdb 219편 전수 대조(`kb/reviews/litdb_dopant_sota_2026_09_09.md`)의
> 결론 하나가 *"능동학습 축이 219편에 없다"* 였다. 정확히는 **계산 내부 AL**(MTP 불확실도 query —
> `kim2025_csp…`, `kim2026_li_argyrodite_sei_reactive_md`)만 있었고 **오라클이 실험인 닫힌 고리**가 없었다.
> [Cho25AL] 이 그 구멍이다. 상세는 `papers/cho2025_multicompositional_argyrodite_experimental_active_learning.md`.
>
> ⚠ **먼저 기대치 교정**: 이 논문의 "active learning" 에는 **대리모델도 acquisition function 도 없다.**
> 저자 본인이 *"can also be applied in **non-machine learning** contexts"*, *"PSO-assisted experimentation"*
> 이라고 쓴다. 우리가 배울 것은 **통계가 아니라 루프 구조**다.

| 항목 | **[Cho25AL]** | 우리 cascade | 판정 |
|---|---|---|---|
| **대리모델** | ⛔ **없음** (학습되는 회귀기 0개) | ridge + 상호작용 distillation | — 범주 다름 |
| **acquisition** | **PSO 속도식** = w·관성 + c₁·(전역최고−x) + c₂·(개인최고−x). ⛔ **w·c₁·c₂ 값 미공개** | Pareto front 선별(1회) | 🔴 **양쪽 다 재현 불가 요소 보유** |
| **배치·라운드** | **20 × 5 라운드 × 2 공간 = 200 실합성** (+예비 30 +단순화 6) | **273 후보 1회 통과**(라운드 개념 없음) | 🔴 우리는 **열린 고리** |
| **중단 조건** | **예산 소진** (수렴 아님) — *"terminated after the fifth round because of the high-cost"* | 없음 | — |
| **오라클** | **실제 합성 + EIS** (라운드당 20회) | **UMA MLIP-MD** (설계당 수 시간) | ⭕ **우리 오라클이 100배 싸다** — 라운드를 못 돌 이유가 없다 |
| **오라클 잡음 계측** | ⭕ **설계로 박음** — 엘리트 복제본을 라운드마다 재합성, **>5 % 어긋나면 그 라운드 전체 재측정** | 🔶 modelc 600 K **3-seed 0.197±0.032** 일회성 | ⭕ **이들이 낫다** (규칙이 루프 안에 있다) |
| ↳ **그 계측의 실제 결과** | 🔴 **본문 "±3 % 이내" ↔ `Table S1` 3↔4라운드 19쌍 재측정 median 39 % · max 94 %**(3-18 4.02→0.23) | — | 🔴 **이들 실패 — 규칙을 발동시키고 발동 안 했다고 썼다** |
| **랜덤 대조군** | 🔶 **1라운드가 실측 랜덤 표본**(n=20, 같은 공간) — 병렬 팔은 없음 | ⛔ 없음(사후 순열검정만) | 🔶 **이들이 조금 낫다** |
| **enrichment** | ⛔ **논문 미보고.** digest 재계산: hit(σ≥3) **1/20 → 15/20 = 15×**, **공정 고정 시 1/6 → 15/20 = 4.5×** | ⭕ ordering **3.35× (p=0.010)** · discovery **1.22× (p=0.426)** | ⭕ **우리가 숫자를 냈다** — 단 ⛔ **두 수를 같은 표에 놓지 마라** (이들 것은 자기상관 시계열 앞뒤 비교, 우리 것은 독립 순열검정) |
| **prospective 검증** | ⭕⭕ **루프 전체가 prospective.** 예측→합성→측정이 5번 닫혔다 | ⛔ **0/270** | ⭕⭕ **이들이 압도적** |
| **group-out CV / p-값 / estimand 카드** | ⛔ 전부 없음 | ⭕ LODO −0.1805 · 순열 p · `cascade_d_rel_estimand_2026_09_08.json` | ⭕ **우리가 낫다** |
| **설계변수에 "공정" 포함** | ⭕ **소성온도·냉각률** — 5라운드 20/20 이 **450 °C+급랭**으로 수렴 | ⛔ 조성만 (셀·배열·시드는 잡음 취급) | ⭕ **이들이 낫다 — 우리 대응물은 셀·배열·시드다** |
| **무질서 처리** | **Coulomb(Ewald) 전수열거 → 하위 30 → DFT 재채점 → 최저 1개**. A3 는 **4.06×10⁸ 배열** 전수. 도구 = Okhotnikov 2016 `supercell` | 실험 점유 decorate / 단일 배열 | 🔶 **방법은 훔칠 가치 있음.** ⚠ 단 **최종 MD 는 배열 1개** = 우리와 같은 병 |
| **MSD 회귀 창** | **250 ps 전체, 원점 포함 단일 회귀**(Deng 2017). 5×50 ps 분할(He 2018)도 해봤으나 *"고온 분산이 크다"*고 기각 | **2–50 ps 고정 창 + 자유절편** | 🔴 **정면 반대.** `Fig. S5` 600 K 곡선에 **평탄부·계단**이 보인다 → 전체 회귀는 방어 곤란. 단 **우리 창이 짧아 분산은 우리가 크다** = 편향/분산의 다른 지점 |
| **데이터 공개** | ⭕ SI 에 **200 엔트리 전수**(조성·공정·σ) + PSO 코드 GitHub | ⭕ CSV + provenance + sha256 | ⭕ 양쪽 다 |

> ### 🔑 판정
> **우리는 정직한 평가를 가졌고, 이들은 닫힌 고리를 가졌다.**
> 부러워할 것은 이들의 통계가 아니라 *"예측을 실행해서 확인까지 갔다"* 는 사실 하나다.
> 그리고 이들의 실패(±3 % 주장 ↔ SI 39 %)가 우리에게 주는 교훈은 **"잡음 계측 장치를 넣는 것만으로는
> 부족하고, 발동 이력을 로그로 남겨야 한다"** 이다.
>
> ### 🛠 우리 좌표로 옮기면 (cascade 재설계 후보 — 아직 판정 아님)
> - **① host 재측정을 라운드마다.** `D_rel = D*(design)/D*(host)` 는 이미 host 를 분모에 두므로,
>   라운드마다 host 를 **새 시드로 다시 돌리는 비용은 MD 1~3개**다. 그것이 우리의 "엘리트 복제본" 이다.
> - **② 1라운드를 의도적으로 랜덤 20개로.** 그러면 랜덤 팔이 *실측으로* 생기고, 이후 모든 라운드의
>   hit rate 를 거기에 나눌 수 있다 — 우리 `discovery 1.22×, p=0.426` 의 약점(랜덤 팔 부재)이 사라진다.
> - **③ 대리모델을 빼고 MD 를 오라클로 직접.** 이 논문은 **surrogate 없이** 4.5× 를 냈다.
>   우리 예측기 LODO −0.18 은 **AL 을 막는 이유가 아니다** — surrogate 를 쓰면 UMA 편향이 *학습·증폭*되지만,
>   오라클 직접 방식에서는 편향이 **상수로 남는다** (`kb/reviews/litdb_dopant_sota_2026_09_09.md` §안 C ① 에 대한 부분 답).
> - **④ 설정을 설계변수로 승격.** 그들의 소성온도 = 우리의 셀·배열·시드. 그들 이득의 절반 이상이 거기서 왔다.
>
> ### ⛔ 이 블록에서 우리 4축으로 넘기면 안 되는 것
> - **AIMD σ₃₀₀K 15.79/15.49/11.41 mS/cm** — 250 ps 전체 회귀 + 1200 K 포함 + 단일 궤적 + 조성 근사(A1_calc ≠ A1).
>   우리 D·Ea 와 같은 표 금지.
> - **ESW 0.022 V / 산화 2.025 V / 환원 2.003 V** — 경쟁상 86종 중 **49종이 GNoME 가상구조**다.
>   우리 2.256/1.242 V 와 **0.2 V 차이**로 읽으면 안 된다 (상 집합이 다르다).
>   🔶 다만 **"P → Sb/Ge/Si 치환은 환원 열역학 창을 통째로 내준다"** 는 방향성은 살아 있다 — §E 후보.
> - **band gap** — `Fig. 4a` **figure-read ≈ 2.2 eV**, 논문에 수치 없음. "둘 다 wide-gap" 이상 금지.

---

---

#### J-9b. [Ma25AL] — GP + EI 순차 베이지안 (액체 전해질, Source Data 재계산)

> **왜 이 블록이 있나**: litdb 219편 전수 대조(`kb/reviews/litdb_dopant_sota_2026_09_09.md`) 결론이
> *"능동학습(AL) 축이 통째로 없다"* 였다. **[Ma25AL]** 이 그 공백을 메우는 첫 편이다.
> ⚠ **재료계가 다르다** — 액체 전해질 용매 ↔ 고체 도펀트. 여기서 가져오는 것은 **루프의 기계 부품과
> 보고 서식**뿐이고, **물성값은 한 줄도 넘어오지 않는다.**
> 상세는 `papers/ma2025_active_learning_electrolyte_solvent_screening_anodefree.md` §4·§6.2·§8·§9.

**[Ma25AL]** = Ma, Kumar, Wang, Amanchukwu, *Nat. Commun.* **16**, 8396 (2025), DOI 10.1038/s41467-025-63303-7.

| 항목 | **[Ma25AL]** | 우리 cascade predictor (`db/properties/codoping_ml_v2_meta.json`) | 판정 |
|---|---|---|---|
| 탐색공간 | **380,000** 분자 (열거된 상용 DB) | **1,081 쌍** (47 도펀트 파생) | 🔵 **2.5 자릿수 차 — 체제가 다르다** |
| 깔때기 비율 (실측/공간) | **1.9 × 10⁻⁴** | 계획 6.5 × 10⁻² | 🔵 바늘찾기 vs 순서매기기 |
| base rate | ⛔ **미정의** (공간 전체 라벨 없음) | ⭕ **3.7 %** (40/1081) | ⭕ **우리가 낫다** |
| 라벨의 정체 | ⭕⭕ **실측** (Cu‖LFP 20사이클, 2셀 평균) | 🔴 휴리스틱 점수 / UMA-MD 대리값 | ⭕⭕ **[Ma25AL] 이 압도** |
| 라벨 잡음 | 5.6–8.2 % (3–4 반복, 명시) | Ea 3-시드 0.197 ± 0.032 (≈16 %) | ⚠ 양쪽 다 큼 |
| 대리모델 | GP × 4 (RBF+ESS/Matérn-3/2/RQ/Pairwise) + **BMA** | ridge / 교호작용 ridge | — |
| 불확실도 | GP posterior → BMA 집계 (`σ_aggr`, 식 S11) | LODO 47 재적합 예측 표준편차 ε | — |
| **획득함수** | **EI** (배치 7 만 greedy) | ⛔ **없음** (사후 랭킹만) | 🔴 **우리 공백** |
| 배치 크기 | ~10 (**근거 미기재**) | 미정 | ⚠ 양쪽 다 근거 없음 |
| 라운드 수 | **7** | 0 | 🔴 |
| **검증 형식** | **배치 통째 hold-out (out-of-batch)** | **LODO / L2DO** (도펀트 통째) | 🟢 **같은 정신** |
| 랜덤 폴드 사용 | 🟠 5-fold in-batch (그룹 무시) | 🟠 pair-LOOCV (도펀트 누수 +0.344) | ⚠ 양쪽 다 병 |
| 보고 지표 | **RMSE 만** — R²·상관 0건 | R² (LODO/L2DO/pair) | ⭕ **우리가 낫다** |
| **함의 out-of-sample R²** | **≤ 0** (⚠ **우리 재계산** — out-of-batch RMSE 0.256–0.429 vs 라벨 std 0.227–0.249) | **−0.1805** | 🟢 **같은 체급** |
| enrichment / p-값 | ⛔ **0건** (랜덤 arm·귀무모형·hit rate 전부 없음) | ⭕ ordering **3.35× (p=0.010)** · discovery **1.22× (p=0.426)** | ⭕⭕ **우리가 낫다** |
| 클래스 농축 | 🟠 간접만 (에테르 % vs base 2.5 %) — **배수 환산 안 함**. 우리 환산: 1.19→13.17→0.59→5.05→7.71→**9.26×** | ⭕ base rate 보유 | 🟠 |
| **사전등록** | ⛔ 없음 — 획득함수(EI→greedy)·Cl 배제·배치크기 전부 캠페인 중 결정 | ⛔ 없음 (1.22·3.35 도 **전부 사후**) | ⚠ **양쪽 다 병 — 우리만 고칠 기회** |
| **prospective 고리 폐쇄** | ⭕⭕ **72회** (사고 만들고 재고 되먹임) | ⛔ **0회** | ⭕⭕ **[Ma25AL] 이 압도** |
| 음성 사례 | ⭕⭕ **전면 공개** — 실패는 0 배정, 배치 1 은 **14개 전부 0** | ⛔ 미보고 | ⭕⭕ **[Ma25AL] 이 낫다** |
| 중단 조건 | 🟠 사후 — 실질은 "구매가능 후보 고갈" + top-5000 **중복률 71.65 %** | ⛔ 없음 | 🟠 |
| 코드·데이터 공개 | ⭕ MIT (notebook + checkpoint) | ⭕ CSV + provenance + sha256 | ⭕ 양쪽 다 |

> ### 🔑 판정
> **[Ma25AL] 은 "AL 이 랜덤보다 낫다"를 증명하지 않았다. 증명하려 하지도 않았다.**
> 대신 **"AL 루프를 72번 돌려 실제로 새 물질을 냈다"** 를 증명했다. 둘은 다른 주장이다.
>
> 🔴 **그리고 그 루프의 대리모델은 out-of-sample 설명분산이 ≤ 0 이었다** (우리 재계산, 원논문 미보고).
> ⇒ **우리 LODO −0.1805 는 "우리 모델이 못났다"가 아니라 이 영역의 정상 체급이다.**
> ⛔ 단, 이것을 *"그러니 그냥 돌리면 된다"* 로 읽으면 안 된다. 그들 루프가 굴러간 다섯 이유는
> ① **실측 라벨** ② 획득가능성 필터 ③ 클래스 수축 ④ 사람의 화학 거부권 ⑤ 실패의 0-배정이고,
> **①이 우리에게 없다.** 우리 라벨은 UMA-MD 대리값이라 AL 이 MLIP 편향을 **증폭**한다.

**이식 항목 (계산 0회 — 전부 보고 서식·규칙)**

| # | 항목 | 근거 |
|---|---|---|
| **M-1** | ⭐⭐ **RMSE 를 라벨 std 와 반드시 병기.** [Ma25AL] 이 R² 를 안 냈기 때문에 R² ≤ 0 이 원문에서 안 보였다 | §6.2 발견 3 |
| **M-2** | ⭐⭐ **연속 라운드 top-K 중복률을 중단 조건으로 사전등록.** 라벨 0개로 계산된다 (그들 실측 0.26 → 71.65 % 에서 실제로 멈췄다) | Fig. 2e |
| **M-3** | ⭐⭐ **배치 통째 hold-out 을 유일한 성능 지표로** (= 우리 LODO 의 라운드판). 랜덤 폴드 금지 | Fig. S2b |
| **M-4** | ⭐ **"추천 분포" vs "획득 분포"를 따로 보고** — 필터가 클래스를 왜곡하는 양을 드러낸다 | Fig. 2c vs 2d |
| **M-5** | ⭐ **클래스 농축을 base rate 대비 배수로 보고.** 우리는 base rate 3.7 % 를 **이미 갖고 있다** | Fig. 2c + 우리 값 |
| **M-6** | **획득 가능성 필터를 점수와 분리** (그들 구매가능/가격/리드타임 = 우리 합성가능성/cost_tier/공기안정) | 본문 획득규칙 ①③ |
| **M-7** | **적용범위 = 순위 컷** (top-K, 상한 2K). argmax 금지. 우리 `d≤2, ε` 위에 한 겹 더 | 본문 획득규칙 ③ |
| **M-8** | **테스트한 후보 영구 제거** | Methods |
| **M-9** | **대리모델 여러 개의 성능 스프레드 보고** (그들 커널 4종). 앙상블 하나로 뭉개지 않는다 | Fig. S2a |
| **M-10** | **실패 라벨 처리 규칙을 라운드 0 에 확정** ⚠ 단 우리 D_rel 은 **비(ratio)** 라 "0 배정"이 척도를 파괴한다 → **검열 라벨/탈락 플래그**로 | 본문 + 우리 카드 |
| **M-11** | **사람의 화학 거부권을 규칙으로 명문화하되 사전등록** (그들 Cl 배제는 사후라 궤적을 오염시켰다) | 본문 획득규칙 ④ |

**⛔ 이 축에서 인용하면 안 되는 것 (J-6 에 추가)**

- ⛔ **[Ma25AL] 을 "AL 이 랜덤 대비 N배"의 근거로 인용** — 그런 수치가 논문에 **없다**. enrichment·hit rate·랜덤 arm 0건.
- ⛔ **[Ma25AL] 의 "BMA 가 단일 모델보다 낫다"** — 논문이 수치로 보인 적이 **없다.** 보고된 "Average" 는
  **4개 커널 오차의 산술평균**이라 정의상 최선 커널보다 크고, 이는 BMA 에 대한 증거도 반증도 아니다.
  **BMA 예측기 자체의 RMSE 가 부재**하므로 *"BMA 가 도움이 됐는가"* 는 이 논문으로 **판정 불가**다.
- ⛔ **[Ma25AL] 의 SHAP 부분구조 순위** (f⁶ 0.3151 vs f⁴ 0.2998) — 차이 5 % 가 **자기 반복 std 5.6–8.2 % 안**이고,
  근거 모델이 **가장 과적합된 RQ 커널**이다.
- ⛔ **[Ma25AL] 의 물성 절대값 전량** (σ 0.67–3.51 mS/cm · D_Li · t_Li 0.47–0.53 · C20 mAh/g) — **액체 전해질 소환값**.
  argyrodite A–D 물성 4축 표에 넣지 않는다.
- ⛔ **[Ma25AL] 의 "1 million electrolytes"** — Fig. 1c 깔때기 종점은 **380,000** 이고 1 M 의 출처가 본문에 없다.
  인용하려면 **380 k** 를 쓴다.
- ⛔ **[Ma25AL] 의 라운드 개선을 "AL 의 효과"로 단정** — Cl 배제·합성 화합물 투입·greedy 전환 **세 개입과 교락**.
  배치 7 을 빼면 우리 Fisher 검정 p 가 2.4e-4 → 0.036 으로 약해진다.

**⚠ 우리 재계산임을 반드시 병기해야 하는 수치** (원논문에 없다 — 전부 Source Data 재분석)
`out-of-sample R² ≤ 0` · `Fisher p = 2.4e-4 / 0.036` · `에테르 농축 9.26×` · `배치별 화합물 수 14/11/7/9/11/11`
· `F5DEE C20 119.9` · `50사이클 정규화 종점 F5DEE 0.704 > 7-16 0.678 > 7-1 0.676 > 7-15 0.669 > 6-3 0.667`
· `"Average" = 4커널 산술평균` · `SHAP 시점 라벨 분자 88개`

---


> 📎 2026-09-13 병합 — J-9c–f 는 초안 4건이 **전부 "J-9c" 를 요구**해 슬러그 알파벳순으로 c·d·e·f 를 배정했다.

#### J-9c. [Hu26ICAL] — TabPFN 대리모형 AL 벤치마크 (2026-09-09 신설)

> 🔴🔴 **먼저 층위를 못박는다.** 이 편의 *"foundation model"* 은 **UMA·MACE 가 아니라 `TabPFN`** 이다.
> **UMA 는 오라클(라벨 생산자), TabPFN 은 설계표 위 대리모형** — 둘은 경쟁하지 않고 위아래로 겹친다.
> ⇒ ***"UMA 를 AL 대리모형으로 쓰자"는 이 논문으로 정당화되지 않는다. 기각.***
>
> 🔑 **그런데 우리에게 유리한 사실이 있다** — **TabPFN 원전 digest 를 이미 갖고 있고**
> (`hollmann2025_tabpfn_tabular_foundation_model`, *Nature* 637, 319–326), **우리 랩 BML 에 실사용 경험이 있다**
> (`talks/yang2026_ncm_radial_microstructure_ml` — ⛔ `citable=no`, 여기서는 "역량 존재"만 쓴다).
> ⇒ **새 기법 도입이 아니라 다른 층에 재사용하는 것**이다.

| 항목 | [Hu26ICAL] | 우리 cascade (`cascade_d_rel_estimand_2026_09_08.json`, active) | 판정 |
|---|---|---|---|
| **오라클** | **데이터셋 조회** — 비용 0 · 잡음 0 · 결정론 | **UMA-MD** — 설계당 GPU 수시간 · **시드 잡음 있음** | 🔴🔴 **가장 큰 차이.** 이 논문 세계에는 라벨 잡음 모델이 아예 없다 |
| 탐색 공간 | 495–3,148 (라벨 이미 전부 있음) | **227 설계** → front **39** (30 dopant) | 🟡 우리가 1자릿수 작다 |
| **보고량** | **전역최적 발견까지의 추가 평가 수** (극단값 탐색) | **`D_rel(600 K, 2–50 ps, cell-conditioned)` 의 값·CI · 순위 안정성 · ρ̂+CI+유효표본수** | 🔴 **다른 양이다.** 이 지표를 우리 카드에 넣을 수 없다 |
| 초기셋 | **물성 최저 K%**(결정론적) ⇒ **순수 외삽 과제** | front 39 = **점수 상위**(예측기가 고른 것) | 🔴 **정반대 방향** |
| 목표 | **Top-1 단일목적** | **4축** (행별 `score = 3m+b` 후 집계) | 🔴 **다목적을 안 한다**(저자 future work) ⇒ [Jain26Rev] 의 스칼라화 비판은 **그대로 남는다** |
| **batch** | **1** (`Fig. 2` 캡션 G) · 배치 확장 **0** · 다양성 **선언만** | **병렬 GPU 큐** (배치가 자연) | 🔴 **안 맞는다.** 배치 AL 근거는 다른 문헌에서 |
| 대리모형 σ | **TabPFN 분위수** `(q97.5−q2.5)/3.92` — 단일 모델 | ⛔ **설계표 위 대리모형 자체가 없다.** 우리 σ 는 **힘 층위** 이종 committee **M=3** | ⚠ **층위가 다르다** — 서로 대체하지 않는다 |
| **M≥4 (Grasselli 식 27)** | ⭕ **이 층위에선 제약이 발생하지 않는다** (앙상블이 아니므로 M 이 정의되지 않음) | 힘 층위 M=3 문제는 **그대로 남는다** | ⚠ **우회가 아니라 다른 σ.** "M 문제를 풀었다"고 쓰면 안 된다 |
| UQ 지표 | **NLL · PICP · MPIW · AUSE** | ⛔ 없음 (절대 σ 금지라 캘리브레이션을 못 잰다) | ⭕⭕ **`AUSE` 는 스케일 불변 ⇒ 우리도 잴 수 있다** (아래) |
| 예측기 품질 문턱 | **R² 0.18 로도 굴러갔다** (`Table 6`) | **LODO −0.1805** / 쌍 LOOCV 0.0892 | ⭕ **착수를 막는 이유가 못 된다** — [Ma25AL] 과 **독립 두 번째 증거** |
| 통계 규율 | ⛔ 검정·CI·부트스트랩 **0건** · TabPFN 반복 **1회**(오차막대 없음) | ρ̂ + **Fisher 95% CI** + **블록 부트스트랩** + 유효표본수 + **사전 검정력 고지** | ⭕⭕ **우리 규율이 더 엄격하다.** 이 논문은 우리 카드 §7 무효조건 여러 개에 걸린다 |
| **순환 검증** | 없음 (라벨이 참값) | 🔴 점수도 UMA, 검증 D 도 UMA-MD | 🔴 **이 논문은 그 문제를 다루지 않는다** |
| 랜덤 팔 | ⛔ **없다** | — | 🔴🔴 **[Cho25AL]·[Ma25AL] 에 이어 세 편 연속 결손** |

**🔑 우리가 실제로 가져오는 것 (값이 아니라 지표와 설계 규칙)**

| # | 가져올 것 | 근거 | 강도 |
|---|---|---|---|
| 1 | **AUSE 를 우리 committee 에 이식** — σ 내림차순으로 5%씩 버리며 남은 평균 힘오차 곡선 vs oracle 곡선의 면적. **σ 의 순서만 쓰고 절대 크기를 안 쓴다** ⇒ *"절대 σ 인용 금지"*·*"M=3 캘리브레이션 불가"* 를 **둘 다 우회** | `Table 5`·`Table 6` 의 지표 정의 | ⭕⭕⭕ **오늘 실행 가능. DFT 새 계산 0회** (⚠ 값을 원고에 실을 거면 보고량 카드 먼저) |
| 2 | **획득함수는 문헌 이식 금지 — 우리 계에서 스윕**. 단 **보고 지표 밖에서** 고른다 | §4.3(6종이 계마다 뒤집힘) + §12-4(이 논문의 selection-on-test) | ⭕ 강함 |
| 3 | **`LODO −0.1805` 는 AL 착수를 막지 않는다** | `Table 6`(R² 0.18) + [Ma25AL] | ⭕ 강함 (독립 2편) |
| 4 | **초기 라벨 = 풀의 10–20%** (227설계면 23–45; 우리 front 39 = 17%) | §3.1·§4 저자 명시 | 🟡 중간 (다른 재료계) |
| 5 | **랜덤 팔 필수** | §12-5 | ⭕⭕ 가장 강함 (세 편 연속 결손) |
| 6 | **bracketing 을 설계변수로** — 초기셋이 목표 영역을 괄호로 감싸는지 | 원전 `hollmann2025` §3 *"외삽 취약"* + `Fig. 5a` 506→111 급전환 | 🟡 **우리 해석.** 논문은 무작위 초기화 대조를 **안 했다** |

**🔴 이 편이 닫지 못하는 것 — 반드시 같이 인용**
1. 🔴 **동료심사 안 됐다** (arXiv v3, DOI 자리표시자 잔존).
2. 🔴🔴 **"8 out of 10 datasets" 가 자기 `Table 4` 와 안 맞는다 — 세면 7/10** (TabPFN 7 · Gauss 2 · RF 1).
3. 🔴🔴 **헤드라인 52% / 29.77% 는 "TabPFN 이 이긴 4개" 평균**이다 (역산 확인: 52.00% / 29.775%).
   **10개 전체면 vs GP ≈39.0% · vs RF ≈12.8%** (우리 계산). 초록·결론에는 그 단서가 없다.
4. 🔴 **본문 AUSE(GP, Cu) `15.58` vs `Table 5` `5.58` 불일치** ⇒ 그 값 인용 금지.
5. 🔴 **랜덤 팔 0건** ⇒ *"AL 이 무작위보다 X배"* 를 이 논문으로 말할 수 없다.
6. 🔴 **문제 인스턴스가 데이터셋당 사실상 1개** (초기셋 결정론적 + init_ratio 증가 시 중첩)
   ⇒ *"승률 90%"* 는 독립 20시행이 아니라 **강상관 20비교**. 우리 카드가 금지한 계수 방식이다.
7. 🔴 **획득함수를 보고 지표 위에서 선택** + hybrid 2종이 TabPFN 전용이라 **비대칭 다중비교**.
8. 🔴 **기전 검증이 이긴 데이터셋 2개에서만** — 진 3개의 NLL·AUSE 없음.
9. 🔴 **TabPFN 오차막대 부재를 *"tight error bars"* 라고 서술** (1회 실행이라 산포를 잴 수 없다 — 순환).
10. 🔴 **재현 불가**: 코드 미공개 · LTC 데이터 비공개 · GP 커널/RF 하이퍼파라미터/라이브러리 버전/**라이선스 전부 미기재**.
11. 🔴 **초기화 규칙이 논문 안에서 자기모순** (*"bottom K%"* ↔ *"randomly"*).
12. 🔴 **초록의 *"electrolyte materials"* 데이터셋이 논문에 없다** · §2.3 의 **ChEMBL 10종도 결과에 0회**.

**⛔ 이 축에서 인용하면 안 되는 것 (→ §J-6 에도 추가)**
- ⛔ *"파운데이션 모델이 AL 대리모형으로 검증됐으니 **UMA 를 대리모형으로** 쓰자"* — **층위가 다르다.**
  UMA 는 조성 벡터를 받지 않고, σ 를 내지 않으며, `D_rel` 을 단일 forward 로 못 낸다.
- ⛔ *"52% 절감"* 을 단서 없이 — **TabPFN 이 이긴 4개 데이터셋 평균**이다.
- ⛔ *"8/10 에서 이겼다"* — **7/10 이다**.
- ⛔ *"AL 이 무작위보다 낫다"* 를 이 논문 근거로 — **랜덤 팔이 없다**.
- ⛔ *"전해질 AL 논문"* — **전해질 데이터셋이 없다**.
- ⛔ *"배치 다양성 전략을 제시했다"* — **선언 한 줄뿐, 구현·평가 0**. batch=1 이라 구조적으로도 불가.
- ⛔ *"거짓음성이 없음을 보였다"* — **거짓음성이 발생할 수 없는 설정**이다.
- ⛔ *"M≥4 문제를 풀었다"* — **다른 층위의 다른 σ** 다. 힘 층위 M=3 은 그대로 남는다.
- ⛔ 이 논문의 **"electrical conductivity"(Cu 합금 %IACS)** 를 우리 **이온전도도(mS/cm)** 와 같은 표에 놓기.
- ⛔ `figure-read ≈` 값을 본문 명시값처럼 쓰기 — `Fig. 3–5` 곡선 값은 전부 눈금 판독(±10–15%).

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_hu2026_foundation_model_surrogates_active_learning.md` §③.</sub>

---

#### J-9d. [Liu26AB] — **다목적 AL (EI/HVI/ParEGO) + "자리 선언" 의 외부 선례** (2026-09-09 신설)

> **왜 이 블록이 있나**: §J-9a·b 는 *"AL 루프를 어떻게 도는가"* 였다. **[Liu26AB] 는 그 앞 칸**
> — *"애초에 무엇을 바꾸는 질문인가"* 를 우리보다 엄격하게 선언한 편이다.
> 2026-09-09 회신 BJ 가 우리 cascade 에 **NO-GO** 를 내면서 사유 1번으로 지목한 것이
> *"'도핑' 데이터가 사실은 **코팅 후보 자체의 hull** 이었다"* 였고, 회신이 권한 방향은
> *"**실제 치환 조성·농도·자리·전하보상과 접촉 상대를 먼저 고정**"* 이다.
> **[Liu26AB] 는 그중 '자리·농도' 를 화학식과 코드로 못박은 실물 사례다.**
>
> ⚠ **재료계가 다르다** — 산화물 ABO₃ 페로브스카이트의 **O²⁻ 확산**, 1000–2000 K.
> **물성값은 한 줄도 넘어오지 않는다.** 넘어오는 것은 **설계 문법과 보고 서식**뿐이다.
> ⚠ **본문 PDF 미확보.** 아래 `[재구성]` 은 저자 공개 `x/y_train_*.pkl` 을 우리가 역변환한 값이다.
> 상세는 `papers/liu2026_ab_site_substitution_high_entropy_perovskite_al.md` §3·§5·§6·§15.

| 항목 | **[Liu26AB]** | 우리 cascade (v2 재설계 중) | 판정 |
|---|---|---|---|
| **자리(site) 선언** | ⭕⭕ **화학식으로 못박음** — `(La,A2..A5)CoO₃` / `La(Co,B2..B5)O₃`. 코드가 host 를 런타임 강제(`app.py:342,356`) | ⛔ **없다** — 회신 BJ 반려 사유 1번 | 🔴 **저들이 압도. 이 한 칸이 배울 전부다** |
| **자리 모호성 해소** | ⭕ **후보집합 교집합 ∅** (A: Ca·Sr·Ba·란타넘족 / B: 3d TM) — 사후 판정이 아니라 **설계로 발생을 막음** | ⛔ 미정의 (예: O 는 S_16e·S_4a4c 양쪽 후보) | 🔶 **우리는 분할이 불가능** ⇒ `design_id` 분기로 풀어야 함 (§15.2) |
| **묻는 질문 유형** | **격자 치환(단상)** 하나로 고정 | ⛔ 선언 안 함 → 실데이터는 **별도 상** 반응 | 🔴 우리 P0 |
| **별도 상 배제 게이트** | ⛔ **없음** — hull·경쟁상·분해반응 **0건**(requirements 에 pymatgen 없음) | ⛔ 없음 | ⚠ **양쪽 다 없다 — 저들을 따라 해도 안 풀린다** |
| **형성E 기준상태** | 🔴 **불명.** Ef 평균 A −1.629 / B −2.203 eV/atom 인데 정의식이 자료 어디에도 없다 | 🔴 v1 이 바로 이것 때문에 죽었다 | ⚠ **같은 병** |
| **농도창 정당화** | ⭕ 15–40 at.%, ΔS_conf>1.5R, `Fig. S1` 로 그림 정당화 + **192조성 전수 검증**(우리 재확인: 최저 1.50479R) | 🔶 조성별 임의 | ⭕ **서식 이식 대상 (L-1)** |
| **후보공간 동결** | ⭕ `data_all.pkl` **10,626** ordered 조성 아티팩트 | ⭕ `cascade_all_302_*.json` | 양쪽 다 |
| **무질서 처리** | ⭕ **SQS 조성당 5개** (자리당 960 prototype) | 🔴 **설계당 구조 1개** | 🔴 저들이 낫다 |
| ↳ 그 앙상블을 확산에 썼나 | 🔴 **[재구성]** D 는 5복제본이 **610/610 전부 동일**(1회 계산 후 복사). Ef·Δ_lattice 는 610/610 전부 다름 | — | ⚠ **저들도 확산에서는 우리와 같은 병** |
| **보고량** | ⭕ **4개를 두 자리에 동일 적용**, 모델만 분리(`model_A`/`model_B`) | ⭕ `D_rel` 단일 | ⭕ **양쪽 다 옳다 — 이 원칙을 명문화할 것** |
| 방향 정규화 | ⭕ 4목표 전부 **minimize**(D 는 −D 로 저장) | 🔶 미정 | ⭕ **이식 (L-3)** |
| **보고량 카드** | ⛔ 없음 (Ef 기준·자기상태 미선언) | ⭕ `cascade_d_rel_estimand_2026_09_08.json` **active** | ⭕⭕ **우리가 낫다** |
| **자기/스핀 상태 선언** | ⛔ **0건** — B pool 이 Mn·Fe·Co·Ni·Cu, A pool 에 Ce·Pr·Nd·Sm·Gd(f전자), 모체는 스핀전이로 유명한 LaCoO₃ | ⭕ 카드 §3 가 강제 | ⭕⭕ **우리가 낫다** — *"admissible state 여럿 + 집계규칙 없음 ⇒ 스칼라 보고량 미정의"* 의 교과서적 위반 |
| **대리모델·불확실도** | ⭕ **Pyro BNN** posterior 1000샘플 mean±std, `σ~Gamma(0.5,1)` 로 aleatoric 분리 | 🔶 ridge + LODO 재적합 산포 ε | 🔶 **저들 방식이 낫다 — 30줄 이식 대상 (L-4)** |
| **획득함수** | ⭕ **EI · HVI · ParEGO** + Pareto (다목적) ⛔ 조합·전환 규칙 본문 미확보 | ⛔ 없음(사후 랭킹) | 🔴 우리 공백 (§J-9 와 동일 결론) |
| **초기집합 / 배치 / 라운드** | **[재구성]** 초기 **420점/자리**(= 등몰 + 5코너, 6조성 × 70원소조; SI `Table S1` 미리보기 6행과 일치) · 최종 **610점** · **AL 추가 190점(31.1 %)**. ⛔ 배치·라운드·중단조건 **본문 미확보** | 273 후보 1회 통과(라운드 개념 없음) | 🔶 **초기집합 = 코너 설계** 는 훔칠 가치 있음 |
| **탐색 비율** | 610 / (70×10,626 = 743,820) = **0.082 %** | 계획 6.5×10⁻² | 🔵 체제 다름 |
| **random arm / enrichment** | ⛔ **0건** | ⭕ ordering 3.35× (p=0.010) · discovery 1.22× (p=0.426) | ⭕⭕ **우리가 낫다** — §J-9 의 세 번째 같은 사례 |
| **CV 규약** | 🔴 랜덤 **5-fold(행 단위)** — 1점 = 25행(5 SQS×5 T) ⇒ 그룹 누수 의심. val MSE **7.43e-2(A)/6.70e-2(B)** (표준화 단위) | ⭕ **LODO / L2DO** | ⭕⭕ **우리가 낫다** (§J-8 판정 승계 — **반례 사례로 인용 가능**) |
| **적용범위 선언** | ⛔ 없음. **[재구성]** host 최소농도(15 at.%) 점이 균등 대비 **3.35×(A)/3.53×(B)** 편중인데 앱은 **10,626 전역**에 예측 | 🔶 `d≤2, ε` 규칙 | ⭕ 우리가 낫다 |
| **오라클 검증** | 🔴 `Fig. S3` **정연 17종 총에너지 parity** (동적범위 3 eV/atom) 로 **타깃 Ef(산포 0.13/0.23 eV/atom)** 를 정당화. **MAE/RMSE 0건 · SQS 검증 0건 · D 검증 0건** | 🔴 `force_contrast` M=3 | ⚠ **양쪽 다 얇다.** 단 *"검증량 = 사용량"* 원칙 위반은 저들이 더 크다 |
| **라벨의 정체** | MLIP(PFP) 대리값 | UMA MLIP-MD 대리값 | ⚠ **양쪽 다 같은 병** |
| **코드·데이터 공개** | 🔶 **추론 앱만** (MIT, 커밋 1개, 테스트 0). 시뮬레이션·AL·학습 코드 **0줄** | ⭕ CSV + provenance + sha256 | 🔶 |

> ### 🔑 판정
> **[Liu26AB] 는 "무엇을 바꾸는가" 를 우리보다 훨씬 엄격하게 선언했고, "그것이 존재하는가" 는
> 우리만큼 안 물었다.** 두 게이트는 독립이다.
> ⇒ **`G-site-1`(자리 선언) 만 저들에게서 베끼고, `G-site-2`(치환체 존재 판정) 는 우리가 새로 만든다.**
> 그 게이트가 요구하는 것은 계산이 아니라 **선언 하나**다 — *"μ_M 의 저장소(reservoir)가 무엇인가."*
> 그것을 안 적으면 E_subst 는 정의되지 않고, 그것이 정확히 **[Liu26AB] 의 Ef 기준상태 불명**이며
> 정확히 **우리 v1 이 죽은 이유**다.

**이식 항목 (계산 0회 — 전부 설계·보고 서식)**

| # | 항목 | 근거 |
|---|---|---|
| **L-1** | ⭐⭐ **농도창을 그림 하나로 정당화하고, 창 안 전부가 조건을 만족함을 전수 검증** | `Fig. S1` + 우리 재검증 192/192 |
| **L-2** | ⭐⭐ **후보공간을 아티팩트로 동결** — 나중에 "공간이 몇 개였나" 로 다투지 않는다 | `data_all.pkl` 10,626 |
| **L-3** | ⭐⭐ **다목적을 전부 minimize 로 정규화**(우리는 −D_rel) 후 Pareto | `app.py:151` |
| **L-4** | ⭐⭐ **posterior predictive std 를 대리모델 출력에 포함**(BNN 30줄) — ridge 의 ε 대체 | `app.py:16–60,145–150` |
| **L-5** | ⭐⭐⭐ **host 강제 검증을 런타임 계약으로** — 선언과 다르면 **잡을 던지지 않는다** | `app.py:342,356` → 우리 `substitute_compound.py` |
| **L-6** | ⭐⭐⭐ **`substitution_mode: lattice \| separate_phase \| additive` 를 보고량 카드 필수 필드로** | §5.3 대응표 |
| **L-7** | ⭐ **자리마다 다른 보고량을 쓰지 않는다 — 양은 같게, 모델만 나눈다** | `model_A`/`model_B` |
| **L-8** | ⭐ **초기집합을 "코너 + 등몰" 로 설계**(6조성×원소조) — AL 이 내부를 채우게 | §6.3 `[재구성]` |

**⛔ 이 축에서 인용하면 안 되는 것 (J-6 에 추가)**

- ⛔ **[Liu26AB] 를 "고엔트로피 페로브스카이트 조성을 발견했다" 로 인용** — **hull·별도상 판정 0건**이므로
  존재성 주장이 논문에 **없다**. 정확한 서술은 *"조성-물성 대리모델을 만들었다"*.
- ⛔ **[Liu26AB] 의 Ef·Δ_lattice·Δ_atomic·D·Ea 절대값 전량** — 산화물 페로브스카이트 O²⁻,
  1000–2000 K. **argyrodite A–D 물성 4축 표에 넣지 않는다.** 특히 **[재구성] Ea (A 0.304 / B 0.219 eV)**
  는 우리 600/800/1000 K 3점 Ea 와 캐리어·온도창·MSD 규약이 전부 다르다 (B자리에는 **Ea < 0 인 점도 있다**).
- ⛔ **[Liu26AB] 앱의 `C (S/cm)`** — `D2C`(`app.py:217–222`)가 Nernst–Einstein 의 **캐리어 농도 c 를 빠뜨리고
  `/100` 을 넣어** c = 0.01 mol/cm³ 로 고정한 값이다. **조성 의존성이 없다.** 어떤 형태로도 인용 금지.
- ⛔ **[Liu26AB] 를 "MLIP 가 DFT 대비 N배 빠르다" 의 근거로 인용** — `Fig. S2` 는 **128원자 초과가 외삽(점선)**,
  하드웨어 미기재, 벤치 계가 **Cu₄Mg₄ 금속**(목표계 아님), VASP 설정이 매우 빡빡(ENCUT 1.75×·5000 pra).
- ⛔ **[Liu26AB] 의 val MSE 를 일반화 성능으로 인용** — 랜덤 5-fold 가 **행 단위**이고 1점 = 25행이다.
  out-of-composition / out-of-quartet 성능은 **보고되지 않았다**.
- ⛔ **[Liu26AB] 를 "AL 이 랜덤보다 N배" 의 근거로 인용** — random arm·enrichment·hit-rate **0건**
  (`[Cho25AL]`·`[Ma25AL]` 과 정확히 같은 공백).
- ⛔ **서지 인용 자체를 조심** — **본문 PDF 미확보**. 저널·권·페이지·DOI 미확정이고 저장소 BibTeX 는 비어 있다.
  원고 reference list 에 넣기 전에 **본문 확보 필수**.

**⚠ 우리 재계산임을 반드시 병기해야 하는 수치** (원논문·SI 에 없다 — 전부 공개 pkl/csv 재분석)
`초기집합 420 / 최종 610 / AL 190 점(31.1 %)` · `host 최소농도 편중 3.35×·3.53×` ·
`D 가 5 SQS 복제본에서 610/610 동일` · `Ef 평균±sd A −1.6286±0.1285 / B −2.2030±0.2255 eV/atom` ·
`Δ_lattice A 4.471±2.842 / B 5.913±2.950 %` · `Δ_atomic A 1.1244±0.8260 / B 1.4254±0.8751 Å` ·
`D@1000K 중앙 A 8.06e-7 / B 6.68e-7 cm²/s (A/B 1.21)` · `Arrhenius Ea A 0.304±0.114 / B 0.219±0.092 eV` ·
`원소별 주변효과 8×2 표` · `T 수준 {1000,1250,1500,1750,2000} K` · `Z 오름차순 15250/15250` ·
`csv 192행 = 전수 열거 · 최저 ΔS_conf 1.50479R` · `ordered 공간 10,626`

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_liu2026_ab_site_substitution_high_entropy_perovskite_al.md` §② (초안 J-9c → J-9d).</sub>

#### J-9e. [Ou26MS] — MLIP 학습 AL (물질탐색 AL 아님) (2026-09-09 초안 · 2026-09-13 병합, 초안 J-9c → J-9e)

> **왜 여기 놓나**: J-9a([Cho25AL])·J-9b([Ma25AL])는 **물질 발굴** AL 이고,
> [Ou26MS]·[Carrete23UQ]는 **퍼텐셜 학습** AL 이다. **둘은 다른 종(種)이다** —
> 앞의 둘은 *후보를 랭킹*하고, 뒤의 둘은 *라벨을 어디에 쓸지*를 고른다.
> ⛔ **우리 `discovery enrichment 1.22× (p=0.426)` 를 이 편과 같은 표에 놓지 마라** — 분모가 다르다.
> **[Ou26MS] 가 특별한 이유 하나: 재료계가 우리와 정확히 같다(Li₆PS₅X).** [Carrete23UQ]는 EAN·SrTiO₃다.

| 항목 | [Ou26MS] | [Carrete23UQ] | 우리 |
|---|---|---|---|
| 불확실도 | **D-optimality 외삽등급 γ (단일 모델)** | **앙상블 분산** (committee/bootstrap/DE) | 🔴 없음 |
| acquisition | MaxVol `select_add`, γ_select **1.4**, 채택 임계 γ>**1.7** | `σ²_f·exp(−E/k_BT)`, Powell | 순차 게이트 |
| 오라클 | **DFT (VASP/PBE)**, 저정밀 이완 + 고정밀 단일점 2단계 | DFT (GPAW) | UMA-MD (대리) |
| 배치 | **라운드당 MD 샘플러 4개(독립 시드)**, level 당 최대 100 반복 | — | — |
| **중단조건** | ⭐ **①** MD 에서 더 이상 샘플이 안 나오면 **②** **목표 물성(GB 에너지·D)이 충분히 정확하면 level 상승 중지** | 오차 수렴 | 예산 |
| 대조군 | ⭕ **global-AL, 각 5회 반복** | ⭕ 추정기 3종 | ⛔ 없음 |
| **라벨 절감 (digest 재계산)** | **총 DFT 라벨 441 vs 2372 = 5.4×** (사전학습 6.4× · AL 획득 1.8×) · AL 라운드 6.2 vs 51.2 = **8.3×** · **level 6 에서 94 % 획득** | — | — |
| 일반화 시험 | ⭕ **Table S1** — 🔴 **할라이드 간 전이 실패**(Br 27.71 meV/atom vs 자체 기준 <10) | 표면 확장 | LODO R² −0.1805 |
| 사전등록 | ⛔ 없음 | ⛔ 없음 | ⛔ 없음 |

**⇒ J-9 에 추가할 판정 2줄**
- **J9-h ⭐⭐ 중단조건을 "보고량 수렴"으로 잡는 형식의 외부 선례가 생겼다.**
  *"optimized … guided directly by the target material properties rather than fitting or validation error"*
  — 우리 **보고량 카드**(`kb/templates/estimand_card.md`) 규율과 같은 철학에 독립적으로 도달했다.
- **J9-i ⭐ 국소구조 추출 라벨링(30 000 원자 → >200 원자 주기셀)** = 우리가 계면/도핑 슬랩 DFT 라벨이
  필요해질 때 비용을 2자릿수 줄이는 처방. **정확한 알고리즘이 `cut2box.py` 에 있다**
  (box 16 Å 시작 +0.2 증가 · 보호영역 6.5 Å · 화학량론 맞을 때까지 **최근접거리가 짧은 경계원자부터 삭제** ·
  d≥1.6 Å · 저정밀 DFT 이완 후 고정밀 단일점 1회).
  ⚠ 재사용 시 확인: `box_final` 이 16 Å 고정인데 `box_length` 는 커질 수 있어 PBC 되접힘 가능(clamp 코드가 주석 처리돼 있다).

**⛔ 이 축에서 [Ou26MS] 로 하면 안 되는 것**
- ⛔ **"AL 이 랜덤 대비 N배" 근거로 인용** — 랜덤 arm 이 없다. 대조군은 **global-AL** 이지 랜덤이 아니다.
- ⛔ **γ 임계 1.4/1.7/5 를 UMA 에 이식** — D-optimality 활성집합은 **MTP 같은 선형-파라미터 모델 전용**이다.
- ⛔ **"5.4× 절감"을 우리 캠페인 예산에 그대로 적용** — 그건 **local-AL vs global-AL** 비교이지 AL vs 무작위가 아니다.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_ou2026_microstructural_multiscale_fast_ion_transport.md` §2-c.</sub>

#### J-9f. [Wilson22BAL] — 풀 기반 배치 AL (선형모형 가정 없음) (2026-09-09 초안 · 2026-09-13 병합, 초안 J-9c → J-9f)

> **왜 여기 놓나 (네 번째 형식)**: J-9a `[Cho25AL]` = 실험 PSO(대리모델 없음) · J-9b `[Ma25AL]` = GP-EI
> 순차 · `[Ou26MS]` = MTP γ 기반 **생성형** local-AL. **이 편은 풀 기반 *선택형* 배치 AL** 이다.
> ⭐ **우리 도펀트 cascade 는 구조적으로 이 형식에 가장 가깝다** — 후보 풀을 먼저 만들어 놓고 시작한다.

| 항목 | **[Wilson22BAL]** | [Ou26MS] | [Carrete23UQ] | 우리 |
|---|---|---|---|---|
| AL 종류 | **풀 기반 선택형(batch)** | 생성형 on-the-fly(local) | 생성형 적대적 | 순차 게이트 |
| 불확실도 | **bagging 앙상블 σ_E, M=10** | **D-optimality γ (단일 모델)** | 앙상블 분산 | 🔴 없음 |
| **선형모형 의존** | ⛔ **없음 (model-agnostic)** | ⭕ **있음 (MTP 전용)** | ⛔ 없음 | — |
| acquisition | `0.9·U/Ū + 0.1·D/D̄` | MaxVol, γ_select 1.4 / 채택 >1.7 | `σ²_f·exp(−E/k_BT)` | 없음 |
| **배치 다양성** | ⭐ **greedy 조건부 + 가산형 거리 보상** (top-k 아님) | 배치 개념 대신 라운드당 4 독립시드 | — | — |
| 배치 크기 | **10**, 근거·민감도 **없음** | — | — | — |
| 오라클 | **DFT(PBE)** — ⚠ **이미 라벨된 풀에서 꺼냄** | DFT(VASP) 실제 실행 | DFT(GPAW) | **UMA-MD 대리값** |
| **중단조건** | 🔴 **고정 예산 3,000 구조** | ⭐ **목표 물성 수렴** | 오차 수렴 | 예산 |
| **무작위 대조군** | ⭕⭕ **있다 — AL·random 각 10 시드** | ⛔ 없음(대조군 = global-AL) | ⛔ 없음 | ⛔ 없음 |
| **top-k 대조군(β=0)** | 🔴 **없다** | — | — | — |
| 절감 배수 | 🔴 **논문에 없다.** digest 도출 **≥3×**(힘 RMSE, `Fig. 4a`) | 5.4×(사전학습 6.4 × 획득 1.8) | — | — |
| 거짓음성 시험 | 🔴 없음 (미표집 RMSE·parity 이상치 부재 = **간접 증거만**) | — | — | — |
| 시드 반복 | ⭕ **10** | 5(MTP 산포) | 12(MD 궤적) | 3(Ea 600 K) |

**⇒ J-9 에 추가할 판정 3줄**

- **J9-j ⭕⭕ "AL 이 랜덤보다 낫다"를 실제로 대조한 첫 편이다.** J-9 머리의 판정
  *"두 편 다 AL 이 랜덤보다 낫다를 증명하지 않았다"* 의 **첫 예외**. 다만 이겨 낸 것은
  **평균 정확도가 아니라 시드 재현성**이다(digest §10-②) — **인용할 때 그 단서를 뗄 수 없다.**
- **J9-k ⭐⭐ 배치 다양성 강제의 최소 처방을 얻었고, 그 결함까지 같이 얻었다.**
  greedy 조건부는 가져오되 **거리항을 합 → min 으로 바꾼다.** 그리고 **`β=0`(top-k) arm 을
  우리가 넣어야 한다** — 논문에 없어서 *"다양성 항이 값을 하는가"* 가 미해결이다.
- **J9-l 🔴 중단조건은 이 편에서 가져오지 않는다.** 고정 예산은 우리가 이미 하는 것이고,
  `[Ou26MS]` 의 목표물성 수렴 + 우리 **보고량 카드**(`kb/templates/estimand_card.md` §4:
  검증 게이트를 **결과 보기 전에** 박는다)가 둘 다보다 앞선다.

**J-9f-M. M 판정 한 덩이 (초안 2-d — 큐레이터 1순위 위치가 J-9 였다)**

> ⚠ **먼저 정직하게: 이 논문은 우리 M 문제를 풀어 주지 않는다.** M=10 을 **근거 없이** 썼고
> (선택 이유가 논문에 **없다**), **M 민감도 실험도 없다**. 아래는 이 편 + 기존 판정을 겹쳐 세운 것이다.

**M-1. 질문을 둘로 쪼갠다 — 이 편이 그 구분을 실물로 보여준다.**

| 용도 | M=3 이 되는가 | 근거 |
|---|---|---|
| **(a) 랭킹** (argmax 로 다음 라벨 고르기) | 🔶 **된다, 단 잡음이 크다** | [Wilson22BAL] 이 하는 것이 정확히 이것 — **캘리브레이션 0**. **Grasselli 식 (27) 의 `M≥4` 는 캘리브레이션 요건이지 랭킹 요건이 아니다** |
| **(b) 정량 보고** (σ 를 값으로 쓰거나 오차와 대조) | ⛔ **안 된다** | 식 (27) 에서 `(M−3)/(M−1)=0` → `α² = −1/3 < 0`. **기존 판정 유지** |

**M-2. 판정 초안 3줄**

1. **⭕ M=3 으로 지금 진행해도 되는 용도가 있다 — 배치 랭킹.**
   ⛔ 단 **σ 값을 문장에 쓰지 않고**(기존 인용금지 유지), **근소차는 무작위로 처리**하며
   그 자리를 **다양성 항(2-b 의 min 거리)** 에 맡긴다. M 이 작을수록 거리항의 상대 가치가 커진다.
2. **🔶 올린다면 목표는 `M≥4` 가 아니라 "잡음 절반"이다.**
   🔎 digest 계산(가우시안 잔차, 표본표준편차의 상대표준오차 `1/√(2(M−1))`):
   **M=3 → 50.0 % · M=4 → 40.8 % · M=10 → 23.6 %.**
   ⇒ **3→4 는 9 %p 뿐** — *"M=4 로 올려 캘리브레이션한다"* 는 형식만 만족하고 실익이 적다.
   할 거면 **M ≈ 8–10**(= Wilson 자리)까지 가야 의미가 있다.
3. **⭐ 이 편이 연 것은 M 의 숫자가 아니라 *멤버 제조법* 이다 — bagging.**
   우리 M=3 은 **이종 파운데이션이 3개뿐**이라서 3 이다. Wilson 의 M=10 은 **같은 모델을
   데이터 80 % 부표본으로 10번 학습**해 만든다 — **새 아키텍처가 필요 없다.**
   ⇒ `[Tompa26]` 으로 UMA fine-tune 경로가 열리면 **부표본 M개 fine-tune** 으로 M 을 늘릴 수 있고,
   **⭐ 이 경로는 "높은 EMA(0.999~0.9999)가 snapshot ensemble 을 죽인다"는 우리 긴장을 우회한다** —
   배깅 멤버는 **독립 학습런**이라 EMA 평균이 멤버 간 차이를 지울 수 없다.
   **snapshot 이 아니라 bagging 이 답이다.**
   ⚠ 대가 = 라운드마다 M회 fine-tune(재학습 비용이 새 병목). 절충안 = **N 배치마다 한 번만 committee 갱신**
   — ⛔ **이 절충의 타당성은 논문에 없다. 우리가 시험해야 한다.**

**M-3. ⛔ 이 편으로 답할 수 없는 것 (명시해서 남긴다)**
- M 을 몇으로 해야 하는가 → **논문에 없다.**
- 에너지 앙상블 산포가 **힘·D** 오차의 좋은 대리인가 → **논문에 없다**(에너지만 쓴다).
- 파운데이션 정확도 영역(0.07 eV/Å)에서도 AL 이득이 남는가 → **논문 밖**(그들 모델은 0.157–0.255).
- **committee 가 조밀하면 정확한가 → 아니다.** `Fig. 5` 가 반례다(digest §10-③):
  **시드 산포는 이미 사라졌는데 평균 포논은 아직 이동 중**(`figure-read` ≈1.2 → ≈1.35 THz).
  ⇒ ⛔ **"우리 3개 모델이 일치했다"를 정확도 근거로 쓰지 않는다** — 기존 규율 재확인.

**J-9f-⛔. 이 편으로 하면 안 되는 것 (초안 2-e)**

- ⛔ **"AL 로 DFT 를 N배 아꼈다" 근거로 인용** — 그 배수가 논문에 **없고**, **DFT 를 실제로 돌리지도 않았다**
  (라벨을 기존 DB 에서 꺼냈다). core-hour·wall-clock **0건**.
- ⛔ **"배치 다양성 항이 top-k 보다 낫다"로 인용** — `β=0` ablation 이 **없다**.
- ⛔ **"AL 퍼텐셜이 더 정확하다"** → **"더 재현적이다"** 로만. `Fig. 3b` 에서 **random 상위 시드가 이긴다.**
- ⛔ **DFT 세팅(k-mesh·ecut·PAW) 근거로 인용** — 이 논문에 **없다**(Yang 2021 을 봐야 한다).
- ⛔ **물성 4축(A/B/C/D) 표에 행 만들기** — 물성값 **0건**이라 전부 `n/a` 가 된다.

<sub>> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_wilson2022_batch_active_learning_interatomic_potentials.md` §2-c·2-d·2-e.</sub>

### J-10. ★★★ 파이프라인 구조 판정 — **[Jain26Rev] 문헌 깔때기 vs 우리 Stage 00–12** (2026-09-09 신설)

> ⚠ **왜 J-9 가 아니라 J-10 인가**: J-9 는 **능동학습 루프**(오라클을 어떻게 고르나) 축이고,
> 이 절은 **깔때기 구조**(무엇을 어떤 순서로 자르나) 축이다. 같은 날 들어왔지만 다른 질문이다.
> [Jain26Rev] 는 226편 **리뷰**라 1차 근거가 아니다 — 여기 수치는 **리뷰 경유**이고,
> 원 논문을 확보하기 전에는 우리 표의 1차 근거로 쓰지 않는다.

> **왜 이 블록이 있나**: 2026-09-09 `kb/reviews/litdb_dopant_sota_2026_09_09.md` 가 219편 전수 대조로
> *"우리 Stage 00–12 에 문헌 최전선이라 부를 스테이지가 0개"* 라고 판정했다. **[Jain26Rev]** 는
> RSC *Materials Horizons* 의 SSE-ML 파이프라인 **리뷰**로, "어떤 구조가 표준으로 인정받나" 의 지도다.
> 상세는 `papers/jain2026_ml_pipelines_solid_state_electrolyte_design.md`.
>
> ⚠ **리뷰 규율**: 이 편은 자체 계산/실험 **0건**이다. 아래 수치는 전부 **[리뷰 경유]** 2차 인용이고
> **우리 표에 1차 근거로 쓰지 않는다.** 원 논문(Xie158 · Lee155 · Wan159 · Du178 · Ataya150 ·
> Maevskiy148 · Gigli163)을 따로 먹여야 1차가 된다.

**J-9-a. 깔때기 순서 대조**

| 순서 | **[Jain26Rev] Fig. 3** (figure-read 임계값) | 우리 Stage | 판정 |
|---|---|---|---|
| 1 | Thermodynamic stability — `E_f < 0.1` · `E_hull < 0.2 eV/atom` | **09e** (맨 뒤) | 🔴 **위치 역전 + 무력**(T10 실측 탈락 0종). Chen2024 는 이 단에서 **98.2 %** 를 자른다 |
| 2 | Electronic conductivity — 밴드갭 (⚠ 그림 표기 `E_gap < 0.5 eV/atom` = 부호·단위 오류) | **없음** (gap 은 진단만) | 🔴 **우리에게 없는 단** |
| 3 | Electrochemical stability — `μ < 4.0 eV` | **09f** — `esw_check.py` 가 스스로 *"NOT real ESW"* 선언 | 🔴 **이름만 대응 = 실질 없음** |
| 4 | Mechanical stability — `G > 8.5 GPa` | **07 + 08** (사실상 1–2번째, no-MD 예산 **75–85 %**) | 🔴 **문헌은 4번째.** 13개 캠페인 중 기계를 1차 게이트로 쓴 것은 **2건**뿐 |
| 5 | Ionic conductivity — `σ > 10⁻⁴ S/cm` | **10** — `D_rel_vs_host ≥ 0.90` (상대비) | 🟡 **보고량 형식이 다르다.** 문헌 표와 같은 칸에 못 놓는다 |
| 6 | Final evaluation — **DFT/AIMD validation** | **09d** (DFT 정적) | 🟡 문헌은 마지막에 **AIMD 로 σ 재측정**(Chen2025 · Lee2025 · Sun50) |
| — | (없음) | **03 winners · 04 anneal · 06 rerank** | ⚠ **문헌 깔때기에 대응 단이 없다** |
| — | 계면(전극 적합성)은 §5.2 요구사항에만, **깔때기에는 없음** | **11 W_ad** (현재 미실행) | ⚠ 문헌도 게이트로 안 쓴다 |

**J-9-b. 🔑 세 가지 문헌 공백 — 우리 자리 확정**

| # | 공백 | [Jain26Rev] 근거 (전수 검색) | 우리 보유 |
|---|---|---|---|
| **1** | **단별 제거율** | 13개 스크리닝 캠페인 중 단별 생존수 공개 **2건** — Chen2024 `32 M → ~589 k`(98.2 %), Dong `43,732 → 1,764`(96.0 %, 두 축 합산). 나머지 11건은 **입력수·최종 후보수만** | `litdb_dopant_sota_2026_09_09.md` §3.2 가 이미 **91 → 45 → 36 → 13** 계산 완료. **형식만 맞추면 새 보고형식** |
| **2** | **게이트 순서 근거** | 유일한 원칙이 **"싼 것 먼저"**(§3.1.3 *"initial screening … followed by conductivity prediction"* · §4.2 *"fast and inexpensive filters"*). **순서 민감도 연구 0건**. Fig. 3 의 6단 순서는 본문 설명 **전무** | 우리도 없다 — **격차 0.** 단 우리는 07+08 이 예산 75–85 % 를 먹으면서 **자르는 양이 0** 이라 "싼 것 먼저" 원칙에도 위배 |
| **3** | ⭐ **group-out 검증** | LOGO-CV 는 **Table 3 한 셀 + §5.4 한 문단**의 **권고**뿐. 근거 인용 **[188] = Zhao/del Cueto/Troisi, *Digit. Discov.* 1, 266–276 (2022) = 유기·분자 재료 논문**. 본문·SI 전수(직접 실행): `LOGO-CV` **2**(Table 3 셀 + §5.4 본문) · `leave-one-group-out` **1**(같은 자리 풀네임) · `randomly split` 1(종래 CV 를 **비판**하는 문장) · **`scaffold` 0 · `k-fold` 0 · `random split` 0** · `computational holdouts` 2(**중복 인쇄된 같은 문단**) · SI 전 항목 **0**. R² 보고 5건(0.964 / 0.85 / 0.633→0.802 / 0.86–0.87 / 94 %·89 %) **전부 분할 방식 미기재** | **쌍 LOOCV 0.0892 → LODO −0.1805 → L2DO −0.2548 (낙차 0.27)** 실측 보유 ⇒ **⭐ 선두 자리** |

> ### 🔑 판정
> **[Jain26Rev] 는 깔때기의 *모양*을 표준화했지만 깔때기의 *성능 회계*를 표준화하지 못했다.**
> 리뷰 스스로 *"lack of standardized evaluation metrics have hindered systematic progress"* 라고 쓰면서
> 자기 요약표에서도 그 지표를 요구하지 않는다. **단별 제거율 · 순서 근거 · hit rate · group-out** 네 칸이
> 그대로 비어 있고, 그중 **group-out 은 우리가 이미 숫자를 갖고 있다.**
>
> ⚖ **그러나 [Jain26Rev] 가 정리한 문헌이 우리를 앞서는 것이 넷 있다** —
> ① **Pareto front 집계**(Lee2024 · Lee2025 둘 다 4차원. 우리 09a 는 가중합 스칼라이고 리뷰가 그 형태를
> 명시적으로 비판한다) ② **능동학습**(Lee2024: 18,133 → **DFT 144회**; Choi: R² 0.633→0.802 를
> **1,600 vs 무작위 2,800**) ③ **최종 AIMD 재검증** ④ **폐루프에 실험 노드**.
> **비판만 옮기면 그대로 되돌아온다.**

**J-9-c. 이식 항목 (전부 계산 0 또는 기존 궤적 후처리)**

| # | 항목 | 근거 |
|---|---|---|
| **J9-a** | **Stage 09a 를 가중합 → 4차원 Pareto 로.** 문헌 SSE 다목적 표준이 Pareto 다(Lee2024 antiperovskite · Lee2025 Na-argyrodite). CLAUDE.md *"스칼라 보고량 미정의"* 판정과도 일치. **기존 CSV 재집계, 계산 0** | digest §6.10·§8-① |
| **J9-b** | **단별 제거율 표를 보고형식으로 고정** — (입력수, 통과수, 통과율, GPU-h) 5열. 문헌 13건 중 2건만 하는 것 | digest §6.5·§8-② |
| **J9-c** | **MD 검출하한을 He 2018 형식으로 선언** — TMSD ≥ **450 Å²**(RSD ~50 %) / > **4150 Å²**(RSD ~20 %), ~50 / ~460 유효 hop. Ea 0.2–0.3 eV → 450–700 K, Ea > 0.5 eV → >1150 K. **기존 200 ps 궤적 후처리, 계산 0** | digest §3.3·§8-④ |
| **J9-d** | **surrogate hit rate 보고** — Stage 02 순위 4분위 × Stage 10 결과. 문헌 유일 선례가 **Maevskiy 상위 10 중 8**. **계산 0** | digest §6.4·§8 |
| **J9-e** | **Haven=1 라벨링** — Dai2022 `H_R 0.1–0.4` + Gigli2024 `NE 가 σ 를 2배 넘게 과소평가` + adeli2019 `H_R 0.235–0.315` **3중 반증**. 규약을 바꾸는 게 아니라 우리 σ 에 "H_R=1 가정" 을 **라벨로 단다** | digest §6.7·§7 |
| **J9-e′** 🆕 | **★★ Haven 문헌이 갈리는 것은 *규약*이지 물리가 아니다 (2026-09-09, [Fang22PW] 로 판정 보강)** — **[Fang22PW]** 는 **우리와 동일 규약**(H_R ≡ D\*/D_σ, D_σ = 집단좌표, **캐리어 = 셀 내 전 Li**)의 AIMD 로 **1/H_R = 1.3·1.5 ⇒ H_R = 0.77·0.67** 을 보고한다 (본문 4쪽 한 문장). **우리 gen1 실측 0.84 ± 0.06 과 같은 대역**이다. 반면 **[Adeli] 의 0.23–0.3 은 캐리어를 c = 4 Li/셀(저자가 "하한"이라 명시)로 잡은 값**이고, Li₆PS₅Cl 관용셀의 Li 는 **24개**다 — `D_σ = k_BT σ/(c q²)` 이므로 **c 규약 하나로 H_R 이 6배 움직인다**(digest 계산: 0.23 → ~1.4). ⇒ **[Adeli] 0.23 과 [Fang22PW] 0.67–0.77 을 "문헌이 갈린다" 로 병치하면 안 된다 — 비교 자체가 성립하지 않는다.** ⇒ **MD 규약(캐리어=전 Li)으로 좁히면 문헌·우리 실측이 모두 H_R ≈ 0.7–0.85, 즉 보정 20–50 %** 이고, 이는 **300 K 외삽 밴드(6–14배)·펠릿 GB(1.3–3배)보다 훨씬 작다**. ⛔ 그래도 **"H_R=1 이라서 상한" 은 여전히 틀렸다** — 방향은 **과소** 쪽이다 (2026-09-07 부호 정정 유지). ⛔ **σ_NE 에 1/H_R 을 곱해 "보정된 σ" 를 만들지 않는다** (σ 절대값 인용 금지 불변) | [Fang22PW] digest §13.2 · 초안 `_pending_index_fang2022…` §3 (2026-09-13 병합) — ⚠ J9-e 원문은 위 행 그대로 보존 |
| **J9-f** | **무질서 배열 선택 근거로 Ataya[150] 인용** — Coulomb 배열선택이 DFT 완화 후 최저에너지를 놓쳐 **ESW 3.1 vs 정답 2.5 V**, 오차 **최대 0.67 eV**. 해법 = SOAP-KRR **DFT 완화 40구조**. 우리 Stage 03 per-group Top-1 문제를 문헌 언어로 말해 준다 | digest §6.4·§8-⑤ |
| **J9-g** | **능동학습은 게이트가 아니라 "비싼 라벨" 에 붙인다** — 문헌 3건 전부 그렇다. 우리 07+08(예산 75–85 %)이 그 자리 | digest §6.9·§8-⑥ |

**⛔ 이 축에서 인용하면 안 되는 것 (J-6 에 추가)**

- ⛔ **[Jain26Rev] 의 어떤 수치도 1차 근거로 인용 금지** — 자체 계산/실험 0건, 전부 2차 인용이고
  원 논문의 방법 조건(범함수·k-mesh·창·무질서 처리)이 소실돼 있다.
- ⛔ **Fig. 3 의 임계값을 "분야 합의 기준" 으로 인용 금지** — 그림에만 있고 본문 근거가 없다.
  게다가 **밴드갭 칸이 `E_gap < 0.5 eV/atom` 로 부호·단위 모두 틀렸다**(내가 그림을 보고 확인).
- ⛔ **σ 목표값을 하나로 인용 금지** — 같은 리뷰 안에서 §4.1 `>1 mS/cm` vs §5.2 `≥10⁻⁴ S/cm` vs
  Fig. 3 `>10⁻⁴ S/cm` 로 **10배 갈린다.**
- ⛔ **[Jain26Rev] 경유 CHGNet 서술 인용 금지** — CHGNet 설명이 **ref 106**(= Park의 HDBSCAN Na 군집화
  논문)을 달고 있다. **오인용이다.**
- ⛔ **"폐루프 성공사례 5건" 을 그대로 세지 말 것** — **ref 154 와 ref 218 이 동일 논문**
  (Chen et al., *JACS* 2024, 146, 20009)인데 §4.2 와 §5.5 에서 서로 다른 사례처럼 등장한다.
- ⚠ **[Jain26Rev] 의 §3.4 말미 문단과 §4.1.1 말미 문단은 4문장 그대로 중복 인쇄**돼 있다.
  하필 그 문단이 이 리뷰의 검증 철학 문단이라 "강조" 로 오독하기 쉽다.

**⭐ 원문 확보 우선순위 (이 리뷰 경유로만 아는 것들)**

| 순위 | 원 논문 | 왜 |
|---|---|---|
| 1 | **[188] Zhao, del Cueto, Troisi, *Digit. Discov.* 1, 266–276 (2022)** | LOGO-CV 프로토콜 원전. **우리가 "SSE 최초 group-out" 을 주장하려면 필독** |
| 2 | **[178] Du et al., arXiv 2502.09970 (2025)** | Li₆PS₅Cl S/Cl 무질서 ↔ 확산경로 연결성 + **uMLIP 학습공간 밖 일반화 실패** — 우리 UMA 미검증 항목 직격 |
| 3 | **[155] B. D. Lee et al., *J. Mater. Chem. A* 13, 10462 (2025)** | **Na-argyrodite 4,375 → 4D Pareto → 15 → AIMD → 5.** 우리 캐스케이드와 가장 가까운 선례 |
| 4 | **[158] Xie, Honrao, Lawson, *Chem. Mater.* 36, 9320 (2024)** | **BV-KMC 로 ~50,000 → 329.** BVEL 위 GCN 이 원자구조 모델보다 낫다 — 우리 Stage 05 정당화/개선 |
| 5 | **[150] Ataya, McCalla, Khaliullin, *J. Phys. Chem. C* 128, 14149 (2024)** | 무질서 배열 선택 오류로 ESW 0.67 eV 과대 — 우리 Stage 03 문제의 문헌 언어 |
| 6 | **[159] Wan et al., *J. Energy Chem.* 88, 28 (2024)** | **LGPS 2,208 치환 도펀트 캐스케이드** — 우리 273 의 직접 비교군 |
| 7 | **[163] Gigli, Tisi, Grasselli, Ceriotti, *Chem. Mater.* 36, 1482 (2024)** | **NE 가 σ 를 2배 넘게 과소평가** + paddle-wheel 반박 — 우리 Haven=1 규약 반증 |
| 8 | **[148] Maevskiy et al., *Phys. Rev. Res.* 7, 023167 (2025)** | 문헌 유일 hit rate(상위 10 중 8) + frozen-framework 서술자 |


### J-12. ★★★ 깔때기 **판정 계약** 과 다중충실도 전환 — **[Basu26MFB] 1차 근거** (2026-09-09 신설)

> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_basu2026_multifidelity_bandit_dopant_screening_funnel.md` §③. 초안 번호 `J-11` → **`J-12`** 배정. 본문 안의 옛 번호 자기참조는 초안 번호다.

> ⚠ **왜 J-10 이 아니라 J-11 인가**: J-10 `[Jain26Rev]` 는 **깔때기의 *모양***(어떤 단을 어떤 순서로)
> 축이고, 이 절은 **각 단의 *판정 계약***(무엇을 재서 어떤 문턱으로 누구를 버리나) + **두 fidelity
> 사이 전환 규칙** 축이다. 그리고 결정적으로 **층위가 다르다** — J-10 은 226편 리뷰라 2차 인용이고,
> **[Basu26MFB] 는 자체 DFT 583계산을 가진 1차 근거**다 (단 preprint·단독저자).
>
> **왜 이 블록이 있나**: `kb/reviews/codex_BJ_prompt_cascade_redesign_2026_09_09.md` 가 **NO-GO** 를
> 냈고 반려사유 #3 이 *"깔때기의 각 단이 무엇을 판정하고 무엇을 통과시키는지 선언돼 있지 않다"* 였다.
> [Basu26MFB] 는 제목에 *three-tier DFT validation funnel* 을 달고 나온 **가장 가까운 외부 선례**다.
> 상세는 `papers/basu2026_multifidelity_bandit_dopant_screening_funnel.md` §12.

**J-11-a. 🔴 판정 — 이 논문의 깔때기도 아무도 탈락시키지 않는다**

| | Tier 1 | Tier 2 | Tier 3 | (Tier 4, 이름 없음) |
|---|---|---|---|---|
| **질문** | 이 후보의 갭이 대략 얼마인가 | d-전자 국재화를 빼서 정성적으로 틀렸나 | 미완화 기하가 만든 가짜 준위인가 | PBE+U 가 맞나 |
| **입력** | 풀 전체 (16~2,256) | Tier 1 중 **d-electrons > 0** | Tier 1 중 **radius mismatch > 20 %** | 재분류 5계 |
| **방법** | PBE-SCF 40 Ry, 2×2×2 k | PBE+U(Dudarev) 45 Ry, SCF-only | 이온완화 45 Ry, 3×3×3 k, F<5e-3 | HSE06 |
| **판정량** | E_g → reward(식 1) | ΔE_g (0.5 eV 금속선 교차) | ΔE_g (완화 전후) | ΔE_g |
| **문턱** | 금속 `E_g≤0.01`→r=−5 · 목표창 2.0±0.6 eV | ⛔ **없음** (재라벨) | ⛔ **없음** (재라벨) | 없음 |
| **탈락 수** | ⛔ **0** (93.9 %는 SCF 수렴률) | ⛔ **0** (5계 중 3계 재라벨) | ⛔ **0** (14/34 수렴, 1계 재라벨) | 0 |
| **단당 비용** | 8–120 분(4코어) | 64코어 VPS 8 ranks | **≤3 h 타임아웃**(실패도 3 h 소모) | ≤6 h 타임아웃 |
| **라우팅 비용** | — | **0** (표값 d-전자 수) | **0** (Shannon 반경) | — |

> **[Basu26MFB] 의 funnel 은 selection(선별)이 아니라 re-scoring(재채점)이다.**
> 비용을 줄이는 것은 깔때기가 아니라 **bandit** 이다.
> `kb/methodology/name_vs_substance_2026_09_09.md` 의 **여섯 번째 사례**이고, 이번엔 외부 논문이다.
> ⇒ **우리 규율로 승격 제안**: 깔때기의 각 단은 `(판정량, 문턱, 입력수, 탈락수, GPU-h)` **5칸을 채운다.**
> 못 채우면 그 단은 게이트가 아니라 **주석(annotation)** 이므로 그렇게 부른다.

**J-11-b. ✅ 이 편에서 1차 근거로 쓸 수 있는 것 4**

| # | 항목 | 근거 | 우리 쪽 자리 |
|---|---|---|---|
| **B-1** | **PBE 단독이 10계 중 4계(40 %)를 정성 오분류**하고, 그 오류가 **d-전자 비국재화(PBE+U 로만)** 와 **기하 왜곡(완화로만)** 이라는 **서로 못 잡는 두 부류**로 갈린다 | Table S7 · Fig. 3 · Fig. 4 — ZnO:V +3.693 / ZnO:Cu −2.832 / SrTiO₃:Fe −1.993 / SrTiO₃:In 0.81→3.48 | 우리 host 에는 열린껍질 TM 이 없어 U 를 안 썼다. **도펀트로 TM(Fe·Co·Ni·Mn·Cr·Cu)을 넣는 순간 같은 문제가 생긴다** — 현재 우리 캐스케이드에 그 단이 없다 |
| **B-2** | **비용 0 라우팅** — `d-electron count > 0` · `ionic radius mismatch > 20 %` 가 표값이라 **DFT 이전에 계산 가능** | Fig. 1 · §2.2 | 우리 대응물 3개(전부 GPU 0): **(a) 열린껍질/산화환원 활성** → spin-pol + U 필요 여부 · **(b) 반경 부정합** vs 치환 대상(Shannon: P⁵⁺ 0.17 / Li⁺ 0.76 / S²⁻ 1.84 / Cl⁻ 1.81 Å) → 완화 필수 여부 · **(c) 이가원자가 여부** → **전하보상 계약** 필요 여부 |
| **B-3** | **같은 다중충실도 전환 로직을 GP+EI 에 붙이면 절감이 정확히 0** (MF-BO-EI **DFT분율 1.00**, surrogate 호출 **0**). 기전: **GP 불확실성은 국소**라 EI 가 고르는 후보의 σ 가 항상 문턱 위 / **선형 밴딧 불확실성만 V_t 축적으로 전역 감소** | Fig. S6b · Table S11 · §2.4 | **우리에게 직격이다.** UMA(싼 것)와 DFT(비싼 것)를 섞으려면 acquisition 이 **국소 불확실성**을 보면 안 된다 — 안 그러면 UMA 가 **발동조차 안 한다** |
| **B-4** | **범용 NNP 는 밴드갭 순위를 못 준다** — MACE-MP-0 단일점 25구조가 QE 갭과 **host 내 Spearman ρ≈0, p>0.4** | §"Relationship to NNPs" | 우리 J-2·J-3 의 *"UMA 로 전자구조를 판정하지 않는다"* 규율에 **외부 실측 방증**. 표본 25구조라 약하지만 방향은 명확 |

**J-11-c. ⚠ 이 편에서 인용하면 안 되는 것 (J-6 에 추가)**

- ⛔ **밴드갭 절대값 전면 인용 금지** — 다른 계·다른 코드·**k-grid 2×2×2**. Table S12 실측으로
  **ZnO:Al 이 2³ 3.397 → 4³ 1.243 eV (Δ2.15 eV)**. 우리 canonical gap(comp1 2.066 / modelc 2.099,
  fixed-occ nscf 고유값)과 **같은 표에 놓지 않는다.** 게다가 이 논문의 갭 판독은 `pw.out` 파싱이라
  우리 규율(DOS-threshold 금지, fixed-occ nscf VBM/CBM)과 **판독 방식 자체가 다르다.**
- ⛔ **"81 % DFT 절감" 을 우리 캐스케이드 비용 근거로 인용 금지** — ① **밴드갭 한 축**에서 나온 수치고
  ② DFT 분율이 계·풀에 따라 **15–64 %** 로 흩어지며(Table S13: MgO 24 % ~ TiO₂ 64 %)
  ③ **최소 예산 아래에서는 이득이 0 이거나 음수**다(Table 3 8 % 예산: MF-OFUL SR **0.723** vs
  Random **0.308** — Random 이 이긴다).
- ⛔ **"밴딧이 GP-BO 보다 낫다" 로 인용 금지** — Table S11 의 **MF-MES SR 0.035 vs MF-OFUL 0.043,
  p = 0.57 동률**이다. 남는 우위는 **성능이 아니라 비용**(O(d²) vs O(n³); 실측 275 s vs 6 s per run).
  헤드라인 Fig. 2 는 **MF-MES 를 빼고 그렸다.**
- ⛔ **Lyapunov 안정성 보장을 "대리모델 오차 누적이 없다" 의 근거로 인용 금지** —
  Fig. 5a 에서 **L(t) 가 0→≈133 단조증가**하고 Φ(t)도 t≈20 최소 ≈1 에서 ≈24 로 되올라간다
  (둘 다 figure-read). **ΔL 을 그린 그림이 논문에 없다.** 그리고 조건 `ε² < 5.0` 은
  **대리모델 MAE ≈1.3 이 보상 목표창 폭(0→1)보다 큰데도 통과**시키므로 사실상 vacuous.
- ⛔ **"HSE06 가 PBE+U 를 검증했다" 로 인용 금지** — MAD 0.15 eV 는 **SrTiO₃:Fe(Δ1.34 eV)를 뺀
  2계 평균**이고, Fig. 4b 는 x축이 PBE+U 인데 5점 중 2점이 `(no U)` = **PBE 값과 섞여 있다.**
  그리고 **Tier 3 유일 재분류(SrTiO₃:In)를 HSE06 이 부인한다**(금속, gap 미검출).
- ⛔ **"Cu 계가 목표 밴드갭 창으로 모인다" 인용 금지** — Fig. 7 실측으로 **Cu 함유 마커 최소 6개가
  E_g < 0.4 eV 의 near-metallic 바닥**에 있고(figure-read), 목표창 안 점은 **하나(Sc₁Cu₁ 1.50 eV)** 뿐이다.
  게다가 **본문 최적 Y₂Cu₂(1.84)·2위 Al₁Cu₂(2.40)가 그 그림에 없다** (제목은 "96 unique candidates",
  캡션은 529 캠페인 — **그림과 캡션이 다른 데이터셋**으로 보인다).
- ⚠ **Tier 2 계산 수를 인용하지 말 것** — Fig. 1 **7** / Methods **16** / Table S10 **14계 나열** /
  본문 *"9 doped + 2 undoped = 11 전부 수렴"* (†표시는 9개). **어느 것도 서로 안 맞는다.**
- ⚠ **금속 문턱이 두 개다** — reward 식은 `E_g ≤ 0.01 eV`, 그림 판정선은 **0.5 eV**.
  *"insulator → metallic 재분류"* 서술은 **그림 기준**이지 알고리즘 기준이 아니다
  (ZnO:Cu PBE+U 0.36 eV 는 reward 상 금속이 아니다).

**J-11-d. 🔑 우리 cascade 재설계 T0–T3 초안 (이 편 + Codex BJ 반려사유에서 유도)**

> 설계 원칙: **각 단은 `(판정량, 문턱, 입력수, 탈락수, GPU-h)` 5칸을 채운다.**
> 못 채우면 그 단은 게이트가 아니라 주석이므로 그렇게 부른다. ([Basu26MFB] 가 이걸 안 해서
> funnel 이 아닌 것을 funnel 이라 불렀다.)

| 단 | 묻는 질문 | 판정량 · 문턱 | 비용 | 근거 |
|---|---|---|---|---|
| **T0** | *"이 후보는 격자 치환인가, 별도 코팅상인가, 첨가 2상인가"* | `estimand_card.md` §1–3 통과 = §3 여섯 물음에 "아마" 가 **0개**. 명시 필수: **자리**(Li 24g/48h · P · S 4a/4d/16e · Cl) · **농도 x 의 실측 정의**(라벨 아님 — 우리 F1) · **전하보상 계약**(실패 시 구조 폐기 — 현재 `substitute_compound.py:365` 는 불균형 구조를 남긴다, Codex P0-Q8) · **집계 규칙** | **0** | Codex BJ 반려사유 #1 · CLAUDE.md §계산 규율 |
| **T1** | *"열역학적으로 애초에 자리가 있나"* + 라우팅 | 게이트①: grand-potential **`window_V < 0.05 V` → 탈락** · 게이트②: **산화 onset < host 2.14 V → 탈락**(⚠ **축① S-limited onset** 이라고 축 이름을 붙여 말한다). ⛔ **hull 게이트는 넣지 않는다**(우리 실측 kill 0 = vacuous; [Basu26MFB] 도 hull 을 게이트로 안 쓴다) — 대신 **"vacuous 임을 결과로 보고"**. 라우팅 플래그 3종(B-2) 동시 산출 | **0** | [Basu26MFB] B-2 · 우리 `build_screening_funnel.py` G2/G3 |
| **T2** | *"싼 물리로 순위를 매길 수 있나"* | **D_rel(600 K) = D\*(design)/D\*(host)** (비준 `D-2026-09-08-cascade-d-rel-estimand`) + 정본 R0 **BVSE 채널%**. 문턱은 **결과 보기 전에** 박는다. **선행조건**: 우리 계에서 **UMA 오차가 판정 마진보다 작은지 먼저 잰다** ([Basu26MFB] 는 이걸 안 하고 썼다 — MAE 1.3 > 마진 1.0) | GPU 소량 | [Basu26MFB] §10.3 의 반면교사 |
| **T3** | *"비싼 물리가 그 순위를 지지하나"* | 대상 = T2 통과분의 **top-K + 불확실성 상위 K′** — **양방향**이다([Basu26MFB] 결론: *"검증은 위양성(top-K)과 위음성(고불확실) 양쪽"*). 판정량은 카드에서 선언한 것(B1 산물 Li 장벽 등). **타임아웃·수렴률을 결과로 보고**하고, **수렴 실패가 특정 계열에 몰리면 거짓 음성으로 별도 보고**(Ni 사례 = 우리 F2) | 비싸다, 소수만 | [Basu26MFB] §2.2·§2.6 · Codex BJ F2 |

**전 축 금지 (재확인)**
- ⛔ 3축을 **가중합 스칼라**로 집계하지 않는다(`combine_rankings.py`, 이미 🔴). **[Basu26MFB] 는
  단일 축이라 이 문제를 만난 적이 없다 — 이 편을 근거로 스칼라 집계를 정당화할 수 없다.**
  (논문 Discussion 도 multi-output bandit 을 *future work* 로 남겼다.)
- ⛔ σ 를 순위 지표로 쓰지 않는다 (Haven 비 계통편차 1.34배, J-7).
- ⛔ 서로 다른 종 집합(47 / 89)의 집계를 섞지 않는다 (Codex BJ 반려사유 #2).
- ⛔ **UMA 가 UMA 를 검증하는 경로 금지** — 라운드마다 DFT 재채점을 섞는다.
  [Basu26MFB] 의 Ridge 는 최소한 **DFT 라벨로 적합**했다. **우리 UMA↔UMA 는 그보다 나쁘다**(Codex Q3).

**J-11-e. ⭐ 원문 확보 우선순위 (이 편 경유로만 아는 것)**

| 순위 | 원 논문 | 왜 |
|---|---|---|
| 1 | **[13] Takeno et al., *PMLR* 119, 9334 (2020) — MF-MES** | 이 논문에서 **MF-OFUL 과 동률(p=0.57)로 나온 유일한 GP 방법**. 우리가 UMA↔DFT 를 섞으려면 *"acquisition 이 국소가 아니라 **전역 최대값에 대한 정보**를 보게 하는 법"* 의 원전 |
| 2 | **[10] Baird & Sparks, *Digital Discovery* (2024) — MF-BO best practices** | 우리 T2↔T3 전환 규칙의 규범 문헌 |
| 3 | **[29] Freysoldt et al., *Rev. Mod. Phys.* 86, 253 (2014)** | **하전 결함 보정** 원전. [Basu26MFB] 가 인용만 하고 **안 쓴** 바로 그 문헌이고, **우리는 반드시 써야 한다**(이가원자가 도핑 = Li 빈자리 변화 = 전도 기구) |


### J-13. ★★★ 다중충실도 AL — **층 정의의 근거** 를 묻는다 · `[Basu26MFB]` 의 독립 견제 (2026-09-09 신설)

> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_aqib2026_multifidelity_active_learning_alloy_design.md` §③. 초안 번호 `J-12` → **`J-13`** 배정. 본문 안의 옛 번호 자기참조는 초안 번호다. [Basu26MFB] 는 **J-12** 다.

> **왜 이 절이 있나**: `kb/reviews/codex_BJ_prompt_cascade_redesign_2026_09_09.md` 가 **NO-GO** 를
> 냈고, 우리는 재설계 뼈대로 `[Basu26MFB]`(J-11)를 받았다. **한 논문 위에 캠페인을 통째로 짓는 것이
> 우리가 반복해 온 실패**이므로, **독립된 두 번째 multi-fidelity AL 사례**를 붙여 대조했다.
> **결과: `[Aqib26MFAL]` 은 `[Basu26MFB]` 를 확인해 주지 않는다.** 두 편은 서로 독립적으로
> **같은 것을 빠뜨렸고**, 갈리는 지점에서는 **`[Basu26MFB]` 가 옳다.** 상세는
> `papers/aqib2026_multifidelity_active_learning_alloy_design.md` §12.

**J-12-a. 🔴 판정 — "층 감소" 가 알고리즘의 결정이 아니라 손으로 박은 스케줄이다**

| | 논문의 서술 | **공개 코드의 실제** |
|---|---|---|
| 점(후보) 선택 | `α = w_EI·EI + w_KG·KG + w_LCB·LCB` | 동일 ✅ (부호만 `−lcb`) |
| **층(fidelity) 선택** | *"비용가중 획득함수로 **(x, t)** 를 선택"* (§2.5.3) | ⛔ **`p_HF = 0.7 − 0.4·progress` 난수 추첨** (`MFAL.py:180-208`, progress<0.1 · >0.9 에 각각 +0.15) |
| 결과로 보고된 HF 비율 | **0.55–0.65** (`Fig. S15`) | = **그 스케줄의 기대값**(평균 ≈0.60, figure-read) |
| 저자 자신의 검증 통계 | *"이론 전략 vs 관측 전략 상관 **0.0874** ⇒ 적응형 비용 기전의 효율을 확인"* | **무상관은 확인이 아니라 부인**이다 |

> ⇒ **`[Aqib26MFAL]` 의 "multi-fidelity" 는 배분 학습이 아니라 배분 처방이다.**
> `kb/methodology/name_vs_substance_2026_09_09.md` 에 **일곱 번째 사례**로 올릴 만하다
> (J-11 의 *funnel = re-scoring* 에 이어, 여기서는 *cost-aware selection = fixed schedule*).

**J-12-b. 🔴 이득의 분해 — 논문은 안 했고, 우리가 하면 획득 몫이 ≈0 이다**

| 성분 | 크기 | 근거 |
|---|---|---|
| (a) **MF 구조 자체**(층 간 정보 전이 덕) | **≈ 0** | 저자 숫자: 개선/단위비용 **HF 0.007508 vs LF 0.007103 = 1.06** ⇒ **무차별**. 무차별이면 어떤 혼합비든 예산당 결과가 같다 |
| (b) **싼 층을 스케줄로 많이 쓴 것** | **절감 전부** | J-12-a |
| (c) **회계 방식** | 56.4 % → 실제 **53.6 %** | **56.4 = 100 − 43.6** = 저정확도를 **공짜**로 셌다. 1:20 을 실제 적용하면 평가당 0.436×20+0.564×1 = 9.284 vs 20 |

> ⚠ **`[Ou26MS]` 선례보다 극단적이다** — 그쪽은 **총 라벨 절감 5.4× 중 AL 이 새로 획득한 몫이 1.8×**
> (`papers/ou2026_…md` §9-B: 평균 획득 100 vs 179 = 1.8× / 총 라벨 441 vs 2372 = 5.4×) 로 **분해가 되지만**,
> 여기서는 **획득 몫이 사실상 0** 이고 애초에 분해할 표가 논문에 없다.
> ⇒ **우리 규율로 승격 제안**: 캐스케이드 이득을 보고할 때 **(a)/(b) 를 분리한 표를 함께 낸다.**
> **(a) 를 재려면 "같은 층 비율을 무작위로 배분한 대조군" 이 필요하다 — 두 논문 어느 쪽에도 없다.**

**J-12-c. ⚖ `[Basu26MFB]` 대조 — 일치하는 것 5 / 갈리는 것 6**

**일치 (⇒ 우리가 새로 해야 한다는 뜻이지, 믿어도 된다는 뜻이 아니다)**
1. **둘 다 싼 층이 비싼 층의 라벨로 학습된 회귀다** (Basu: Ridge / Aqib: GP-on-30%). **독립 물리가 아니다.**
   ⇒ **우리 UMA↔DFT 는 두 편과 성격이 다르다.** UMA 는 독립 물리라 **계통오차가 DFT 와 무상관일 수 있고, 그 경우를 두 편 다 다루지 않는다.**
2. **둘 다 아무 후보도 탈락시키지 않는다** (Basu = 재채점, Aqib = 학습셋 증강). ⇒ Codex BJ 반려사유 #2 가 **흔한 병**임은 확인되지만 **해법은 둘 다 안 준다.**
3. **둘 다 거짓 음성 감사를 안 한다.**
4. **둘 다 단일 스칼라 목적** ⇒ 우리 4축 trade-off 의 답은 어느 쪽에도 없다.
5. **둘 다 순차(batch=1)** ⇒ 배치 다양성 강제 설계를 어느 쪽도 안 준다.
6. **둘 다 전수(exhaustive)를 대조군에 안 넣는다** — Aqib 의 공간은 **717점**이고 **무작위도 432회면 최적을 찾는다**(`Fig. S6`, figure-read). **우리 풀(47/89/273)은 더 작다.**

**갈리는 것 (⇒ 우리가 골라야 한다. 6개 중 5개에서 `[Basu26MFB]` 가 옳다)**

| 쟁점 | `[Basu26MFB]` | `[Aqib26MFAL]` | 우리 채택 |
|---|---|---|---|
| 층 전환 트리거 | **불확실도 폭 > 문턱**(측정 기반) + 주기적 강제 | **확률 스케줄**(손) | **Basu** — 측정 기반이어야 사후 감사가 된다 |
| acquisition 종류 | 선형 밴딧 UCB — **절감이 실제로 난다** | EI/KG/LCB 혼합 — **절감이 acquisition 에서 안 난다** | **Basu.** 그리고 Basu 의 음성 대조(**MF-BO-EI DFT분율 1.00**)가 **Aqib 의 결과를 설명한다** — EI 계열은 국소 불확실도를 보므로 싼 층이 발동 안 하거나, 발동시키려면 **스케줄로 강제**해야 한다. **Aqib 이 후자를 했다** |
| 비용비 | **실측 벽시계** 10⁶–10⁷ | **가정 상수 5:1 / 20:1** | **Basu** — 비용은 재는 것이지 정하는 것이 아니다 |
| top-K 재검증 | ✅ 있고 실제로 잡았다(`Table S8` step 18–20) | ⛔ 없다 | **Basu** |
| 코드↔논문 일치 | 미검증(프록시 403) | **9건 불일치**(digest §10.2) | ⚠ **Aqib 의 알고리즘 서술을 그대로 이식 금지** |
| 대리모델 오차 vs 판정 마진 | 오차 > 마진인데도 **게이트에 씀** | 오차 R² 0.55 인데 **게이트로 안 써서 사고를 피함** | **Aqib 의 "안 쓴 것" 이 결과적으로 안전했다** → J-12-d |

**J-12-d. ✅ 이 편에서만 나오는 것 — "꼬리 해상도 사전시험" (우리 T2 게이트 전제조건)**

> `Fig. S7` 이 가르친 것: **R² 0.5526 짜리 저정확도 층이 목표 구간에서는 완전히 눈이 멀 수 있다.**
> figure-read — **예측값이 ≈2.2 아래로 사실상 내려가지 않는다. 목표는 0.1 이다.**
> 이 층을 게이트로 썼다면 **진짜 최적을 확실히 버렸다.** 논문이 사고를 피한 것은 설계가 좋아서가
> 아니라 **게이트를 안 만들었기 때문**이다.

**⇒ 우리 규율로 신설 제안 (T2 를 켜기 전 1회, GPU 소량):**
1. 이미 **DFT 로 판정한 후보 N개**(10–20 으로 충분)를 고른다.
2. 같은 후보를 **싼 층(UMA 이완 / UMA-MD D_rel)** 으로 잰다.
3. parity plot 을 그리되 **R² 를 보지 않는다.** 두 가지만 본다:
   - **(a) 해상도** — 싼 층의 예측이 **우리 문턱 근방까지 실제로 값을 만드는가.** 안 만들면 **게이트 자격 없음.**
   - **(b) 상위 K 안의 Spearman ρ** — ⚠ **전체 ρ 가 아니라 목표 영역 상위 K 안에서.**
     (전체 ρ 로 속은 사례가 둘 있다: 이 편의 **GP σ ρ = −0.072 인데 AL 은 이겼다**, `[Basu26MFB]` 의 **MACE-MP-0 ρ ≈ 0**.)
4. **(a) 실패 → 그 층은 게이트가 아니라 주석(annotation)** 으로 격하하고 그렇게 부른다. **(b) 실패 → 순위용으로도 못 쓴다.**
5. 시험 결과를 **결과 보기 전에** 문턱과 함께 `kb/templates/estimand_card.md` §4 에 적는다.

> ⚠ **이 절차는 두 논문 어느 쪽에도 없다.** Aqib 은 우연히 피했고, Basu 는 게이트가 없어 문제를 못 만났다.
> **우리가 새로 넣는 것이다.**

**J-12-e. ✅ 부수적으로 1차 근거로 쓸 수 있는 것 2**

| # | 항목 | 근거 | 우리 쪽 자리 |
|---|---|---|---|
| **A-1** | **대리모델의 불확실도 보정과 AL 성능은 분리될 수 있다** — GP 사후분산 vs 실제오차 **Spearman ρ = −0.072**(RF 는 +0.673, coverage gap 7.1 vs 3.6)인데도 **GP 기반 AL 이 100 독립런 내내 RF 기반보다 우수**(표준편차 0.009 vs 0.126, 누적regret 81.38 vs 111.62) | `Fig. S8` + §3.2.3 (figure-read + 본문) | J-7(σ 를 순위 지표로 쓰지 않는다) 을 **강화**한다. 단 저자 해명(*"보정보다 순서"*)은 **자기모순**이므로 인용하지 않는다 — ρ 자체가 순서 통계량인데 ≈0 이다. **우위의 원천은 σ 가 아니라 μ 로 보는 게 옳다** |
| **A-2** | **최적화 진단 지표 5종 세트** — simple regret(S6) · cumulative regret(S7) · spatial diversity(S8) · convergence speed `T_p`(S9, 10/5/1 %) · half-life λ. 코드 `AL_GPR.py:232 additional_metrics()` 에 한 함수로 구현 | SI §CMA-ES + repo | 우리 캐스케이드 성능 보고 양식. ⚠ **전부 후향(true optimum 을 안다) 전제**다 — 우리는 전향이므로 **"예산별 최고값 곡선 + 사후 top-K 재검증"** 으로 개작해야 한다 |

**J-12-f. ⛔ 이 축에서 인용하면 안 되는 것 (J-6 에 추가)**

- ⛔ **CTE 값 전면 인용 금지** — 우리 계와 무관하고, **논문이 CTE 의 온도조차 명시하지 않는다**(Rao 2022 원전이 300 K 라고 서론에서 인용할 뿐). 조성 단위도 `Table S2`(atomic fraction) ↔ `Table S4`(wt.%) 가 **충돌**한다.
- ⛔ **"theoretical minimum CTE" / "True Optimum 0.100" 표현 금지** — 코드 `true_min = np.min(y)` 이고 `y` 는 **CTE<0 을 버린 뒤**의 풀이다(원 데이터 최소 −1.07). **필터링된 데이터셋 최솟값**이지 이론값이 아니다.
- ⛔ **"55–65 % HF 로 동등 성능" 을 우리 예산 근거로 인용 금지** — 그 비율은 결과가 아니라 **코드에 박힌 스케줄**이다(J-12-a).
- ⛔ **"56.4 % 비용 절감" 인용 금지** — 저정확도를 공짜로 센 회계다. 실제 53.6 %(J-12-b).
- ⛔ **"five-fold 속도 향상" 인용 금지** — 산출식이 어느 판본에도 없고, 유일한 근거 그림(`Fig. S6` random search)이 **본문에서 한 번도 인용되지 않으며** 스크립트도 미공개다.
- ⛔ **"MFAL 이 단일정확도와 동등한 해 품질" 인용 금지** — **MFAL 의 최종 simple regret 도 표준편차도 논문에 없다.** 단일정확도 4조합은 `Table S13` 에 전부 있는데 MFAL 만 없다. 게다가 `Fig. 6` 평균 곡선은 **iteration ≈71 에서 ≈0.3–0.35 로 끊긴다**(figure-read) — 단일정확도 GPR-LCB 의 0.105 와 3배 차이다.
- ⛔ **`Fig. 8` 캡션의 "nearly identical trajectories" 인용 금지** — figure-read 로 **적색(단일정확도)이 iter 10–75 에서 일관되게 아래**다(iter 25 ≈2.2 vs ≈2.9, iter 50 ≈0.55 vs ≈0.85).
- ⛔ **ML 모델 R²/RMSE 5종 인용 금지** — 게재본과 preprint 사이에서 **SVR(0.877→0.8663) 과 RFR(0.866→0.8773) 이 사실상 맞바뀐다.** 반올림으로 설명되지 않는다.
- ⚠ **식 (17) 을 그대로 옮기지 말 것** — 최소화 문제에서 **LCB 항 부호가 틀렸다**(코드 `−lcb` 가 옳다).
- ⚠ **"RBF 커널" 로 인용하지 말 것** — MFAL 코드는 **Matérn 5/2 ARD** 다.
- ⚠ **`Fig. 3` 을 "GPR-LCB 가 가장 빠르다" 의 근거로 쓰지 말 것** — figure-read 로 **그 스케일에서 EI/LCB 평균 곡선이 구별 불가**다. 그 주장을 지탱하는 것은 `Table S10`(43 vs 60 iter) 이다.


### J-14. ★★★ 깔때기 판정계약 — **[Muy25Dop] = 우리 물질계에서의 1차 근거** (2026-09-09 신설)

> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_muy2025_li7ps6_dopant_engineering_conductivity.md` §④. 초안 번호 `J-12` → **`J-14`** 배정. 본문 안의 옛 번호 자기참조는 초안 번호다.

> **J-11 `[Basu26MFB]` 과의 층위 차이**: Basu 는 **산화물 반도체·밴드갭 한 축·arXiv preprint·단독저자** 다.
> **[Muy25Dop] 는 황화물 argyrodite·이온전도·Chem. Mater. 심사통과·EPFL+기업 6인** 이고,
> 무엇보다 **도핑을 실제로 격자 치환으로 다룬다.** 우리 반려사유 ①·②를 **같은 물질계에서** 잰다.
> 상세는 `papers/muy2025_li7ps6_dopant_engineering_conductivity.md` §12.

**J-12-a. ✅ 반려사유 ①(격자치환 vs 별도상) — 이 편이 정답 형태다**

| | [Muy25Dop] | 우리가 반려당한 것 |
|---|---|---|
| 대상 | **112원자 supercell 안의 Wyckoff 자리 치환** (Li 24g/48h · P 4b · S 16e/4a/4d) | **코팅 화합물 자체의 hull** (`0.5714 Sc₂O₃ + 0.4286 Li₆PS₅Cl → …` = 별도 상 반응) |
| 농도 | **출력**(형성에너지 + 자기무결 E_F → Boltzmann). 입력은 "결함 1개" | **라벨**이었고 실측 정의 없음 (Codex F1) |
| 전하보상 | **가정하지 않는다** — 모든 결함 × 모든 q 를 놓고 전하중성(eq 2)으로 E_F 를 푼다 | `substitute_compound.py:365` 가 **불균형 구조를 그대로 남긴다** (Codex P0-Q8) |
| 자리 분해 | S 자리를 **16e(S1·S2·S3) / 4a(oct) / 4d(tet) 5개로 분해**해 보고(`Fig. S6`) | 자리 선언 자체가 없었다 |

🔑 **T0 로 승격**: 도펀트 항목은 **(자리 Wyckoff, 농도의 실측 정의, 전하보상 계약, 계약 위반 시 처분)**
4칸을 채운다. 전하보상 계약은 **① 자기무결 E_F(비싸다)** 또는 **② 선언된 화학량(싸다)** 중 하나를
T0 에서 고르고 **단마다 바꾸지 않는다.**

**J-12-b. ⛔ 반려사유 ②(단별 판정계약) — 이 편도 실패한다**

| | 단 1 고유결함 | 단 2 단일치환 | 단 3 공도핑 | 단 4 수송(MD) | 단 5 실험 |
|---|---|---|---|---|---|
| 판정량 | 300 K 평형농도 | 300 K 평형농도 | 300 K 평형농도(공도펀트 하) | σ(300 K), Ea | σ(T), Ea, XRD |
| **문턱** | ⛔ 없음 | ⛔ 없음 | ⛔ 없음 | ⛔ 없음 | ⛔ 없음 |
| 입력 수 | 6 | **24** | **108 + 36** | **≈91 조성** | ≥5 조성 |
| **탈락 수** | 0 | **11** (막대가 축 아래 — **문턱이 아니라 그림 판독**) | **0** | 0 | 0 |
| 다음 단으로 | — | **3종**(Mg·Si·Cl) — ⚠ **순위 1등이 아니다** | **0 — 아래로 안 흐른다** | 4조성 | — |
| 비용 | ⛔ 안 밝힘 | ⛔ 안 밝힘 | ≈0 (단일도펀트 에너지 재사용) | ⛔ 안 밝힘 | — |

> **Basu 와 병이 다르다**: Basu = *"탈락 0, 실체는 재채점"*.
> **Muy = "탈락은 있는데 문턱이 없고, 계산한 단 하나(공도핑 144칸)가 아래로 안 흐른다."**
> ⇒ **R4 로 승격**: *계산한 단이 아래로 안 흐르면 그 단은 결론이 아니라 부록이다. 흐르는 경로를 도식에 그린다.*

**J-12-c. 🔴🔴 R2 — 판정량의 눈금이 목표 도핑량과 자릿수가 다르면 그것은 "순위표" 다**

a = 9.87 Å · Z = 4 ⇒ **1/f.u. = 4.16×10²¹ cm⁻³**. `Fig. 3` 픽셀 실측 vs 실제 합성 조성:

| 종 | 계산 평형농도 | 실제 조성 | 간극 | 논문의 서술 |
|---|---|---|---|---|
| Cl_S | 10^4.6 | Li₆PS₅Cl, x=1 | **17.0 decade** | *"쉽게 치환된다"* |
| Mg_Li | 10^4.9 | x=0.125 (**자기가 합성**) | **15.8 decade** | *"쉽게 Li 를 대체"* |
| Ge_P | 10^−13.9 | x≈0.3 (인용) | **35.0 decade** | *"합성 보고와 **일치**"* |
| Ca_Li | 10^−8.0 | x=0.1 (인용, σ 10.2 mS/cm) | **28.6 decade** | *"**실용 농도로 도핑 가능**"* |
| F_S(+Si) | 10^−3.2 | (제안) | **23.8 decade** | *"**최초의 F-도핑 argyrodite** 가능"* |

**112원자 셀에 결함 1개가 이미 10^20.7 cm⁻³** 이다 ⇒ 보고된 모든 농도(최대 10^14)는
**모델이 표현할 수 있는 최소치보다 6–34 decade 아래**다. 이 수들은 **형성에너지 순위**이지 농도가 아니다.
그런데 본문은 같은 크기의 수를 **정반대로 읽는다**(Ge −13.9 "일치" ↔ F −11.5 "불가", 2.4 decade 차).

> **R2**: 새 게이트를 만들 때 **판정량의 눈금과 목표 도핑량(우리는 x = 0.05–0.3 = 10^20–10^21 cm⁻³)이
> 같은 자릿수인지** 먼저 확인한다. 아니면 그 단은 게이트가 아니라 **순위표**라고 부른다.

**J-12-d. 🔴 R3 — 전하보상 계약을 파이프라인 전 단에서 하나로 고정한다**

[Muy25Dop] 의 두 반쪽이 **정반대 규약**을 쓴다:
- **결함 절반**: 전하보상을 가정하지 않는다. §1 전체가 *"Cl 하나당 Li 하나"* 가정을 반박하는 논증이다.
- **MD 절반**: `Li₇₋₂ₓ₋ᵧMgₓPS₆₋ᵧClᵧ` — **바로 그 가정을 하드코딩한다.** 저자는 이 충돌을 언급하지 않는다.

⇒ 결함 절반의 결론이 전도도 절반에 **되먹임되지 않았다.** 우리 T0 카드가 막아야 할 정확한 실패 모드다.

**J-12-e. ✅ 방법으로만 가져오는 것 3 + ⛔ 금지 목록**

| # | 가져오는 것 | 근거 | 우리 자리 |
|---|---|---|---|
| **M-1** | **공도핑을 O(N) 으로 푸는 트릭** — 결함끼리 직접 상호작용하지 않는다고 두면, 공도핑 효과가 **전부 자기무결 E_F 이동**에 담긴다 ⇒ **두 도펀트가 든 supercell 을 계산할 필요가 없다** | §3.2.3 · `Fig. 4` | 우리 이중도핑 후보 조합이 폭발할 때 **단일 도펀트 에너지만으로 조합을 스캔**할 수 있다. ⚠ 가정(직접상호작용 무시)을 반드시 명시 |
| **M-2** | **MLIP 참조 범함수를 NPT 격자상수 vs 실험으로 먼저 검증**한다 (싸다) | `Fig. S7` — PBEsol ≈0 % · **PBE-no-vdW +1.89 %(부피 +5.8 %)** · PBE-D3 +0.04 % | 우리는 안 하고 있다. UMA 의 유효 격자상수를 우리 계에서 한 번 재는 것만으로 **부피 편향 크기**를 안다 |
| **M-3** | **자기무결 Fermi 준위 + 안정영역 centroid μ** 로 결함농도를 내는 틀 (AiiDA-defects, 오픈소스) | §2.2 · eq 1–5 | 우리 이가원자가 도펀트(Mg·Ca·Zn on Li)의 **전하보상 계약을 계산으로 정하고 싶을 때** 쓸 수 있는 유일한 정론. ⚠ 비싸고, **우리 x 범위(희석극한 밖)에서는 부적합**(J-12-c) |

**⛔ 금지 (J-6 에 추가)**
- ⛔ **계산 σ·Ea 절대값 인용 금지** — **MSD 창·궤적길이·시드 수·앙상블·thermostat·dt·MD 셀크기·오차막대**가
  전부 없다. 게다가 논문에 **숫자가 인쇄돼 있지 않아** 전부 `figure-read` 다.
- ⛔ **결함농도 절대값 인용 금지** — 순위로만. 근거는 J-12-c (13–36 decade 간극).
- ⛔ **"Si 를 낮게 유지하면 빠르다" 인용 금지** — `Fig. 5` 역변환 실측으로 **Cl=1.5 면 σ 가 Si 에 거의 무관**
  (Si 0 → 0.5 에서 58.1 → 61.6 mS/cm), 저-Cl 에서는 **Si 가 많을수록 빠르다**(15.1 → 40.4).
  헤드라인은 **Mg 에서만** 성립한다.
- ⛔ **"Si–F 공도핑으로 F-도핑 argyrodite" 인용 금지** — 근거 농도가 **10^−3.2 cm⁻³** 다.
- ⛔ **"할로겐은 8면체(4a) 자리만 차지한다" 를 우리 무질서 서사에 쓰지 않는다** — 저자 스스로
  실험과 안 맞는다고 적고 *"동결된 준안정"* 으로 설명한다. 그리고 **자기 MD 구조모델은
  Cl 을 tet 에 더 많이 놓는다**(`Fig. S5`, Cl=1.0 에서 tet ≈0.62 > oct ≈0.375, `figure-read`).
- ⛔ **AiiDA 재현성 주장을 이 논문으로 인용 금지** — **provenance DB 가 공개되지 않았고
  Data availability 문 자체가 없다.** 도구(AiiDA-defects)는 오픈소스이고 그건 별개다.
- ⚠ **blind prediction 사례로 인용 금지** — Mg 조성은 **2023년 특허**(WO 2023110697 A1 /
  WO 023111083 A1, 발명자에 Muy·Marzari)로 선행 출원돼 있다.
- ⚠ **실험 Ea 0.36–0.38 eV 를 bulk Ea 로 인용 금지** — **미소결 냉간압축 펠릿 + EIS 상한 1 MHz**,
  bulk/GB 분리 서술 없음 ⇒ **total** 이다.

**J-12-f. ★★ MLIP Ea 가 실험보다 낮은 방향 — 세 번째 점 (J-7·§A 와 연결)**

| 계산 | Ea | 대조 실험 | 차 |
|---|---|---|---|
| **[Wang25DP]** DPA-SSE (DeePMD, PBEsol) | `figure-read ≈0.24` | ≈0.324 (문헌) | −0.084 |
| **우리 comp1** (UMA-s-1p1) | **0.2532** (⚠ provisional·1시드·게이트 not_assessed) | ≈0.324 (문헌) | −0.071 |
| **[Muy25Dop]** 자체학습 DeePMD (PBEsol) | `figure-read ≈0.209` | **0.38 (자기 실험, total)** | −0.171 |

> ⚠ **세 번째 점을 앞의 둘과 같은 줄에 놓지 않는다**: ① 대조 실험이 다르다(자기 미소결 펠릿 total 0.38
> vs 문헌 ≈0.324 — 0.324 에 대면 −0.115 로 줄어든다) ② **적합창이 다르다**(계산 625–1250 K vs 실험 253–333 K;
> `[Zhou26]` 실측으로 **창 하나에 0.06 eV** 가 움직인다) ③ 계산값이 `figure-read` 다.
> **말할 수 있는 것**: *"argyrodite MLIP-MD 의 Ea 가 실험보다 낮게 나오는 사례가 서로 다른 세 모델
> (UMA · DPA-SSE · 자체학습 DeePMD)에서 반복되고, 세 경우 모두 **Nernst–Einstein + Haven = 1** 이며
> 세 경우 모두 **저온 실측창 바깥에서 적합**했다."*
> ⇒ **모델 문제가 아니라 규약 문제일 수 있다**는 가설을 강화한다. `kb/questions/` 카드 후보.


### J-15. ★★★ **순위의 기준점 — [Liang26IF] "도핑이 σ 를 낮출 수 있다" vs 우리 G3/G4 앵커 비대칭** (2026-09-09 신설)

> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_liang2026_interface_bottleneck_solid_state_batteries.md` §③. 초안 번호 `J-12` → **`J-15`** 배정. 본문 안의 옛 번호 자기참조는 초안 번호다.

> 발주 질문: *"우리 cascade 는 '도핑=개선'을 암묵 전제한다. 이 리뷰가 그 반증인가?"*
> **답: 스니펫이 시사한 만큼은 아니다. 그러나 우리 게이트에 실재하는 구조적 결함 하나를 정확히 비춘다.**

#### J-15-1. 리뷰가 실제로 말한 것 (⛔ 스니펫과 다르다)

| 스니펫 조각 | 실제 절 | 물질계 | σ 방향 | 숫자 |
|---|---|---|---|---|
| "exquisitely sensitive to aliovalent doping" | **§2.1 (p.2)** | **LLZO 가넷** | ⬆ **올린다** | 1–2 × 10⁻³ S cm⁻¹ |
| "lowering the ionic conductivity relative to pristine Li₆PS₅Cl" | **§2.2 (p.4)** | **Y-도핑 LPSCl** | ⬇ 내린다 | ⛔ **없음** |
| "high-throughput screening rapidly explored" | **§2.3 (p.5)** | 반-페로브스카이트 | — | ⛔ 없음 |

- **σ↑ 사례 9건 : σ↓ 사례 1건**, 그리고 **숫자는 올리는 쪽에만 있다.**
- σ↓ 주장은 **인용이 없다** — `[32]`(Wang, *Angew* 2025)는 앞 문장(사이클 성능)에 붙어 있다.
- ⇒ ⛔ **"도핑이 σ 를 낮추니 후보를 줄이자"는 이 리뷰로 정당화되지 않는다.**

#### J-15-2. 🔴 그래도 남는 것 — 우리 게이트의 **앵커 비대칭**

| 게이트 | 정의 | host 앵커 |
|---|---|---|
| G3 oxidation | `ox_V ≥ **2.14 V (host)**` (`build_screening_funnel.py: HOST_OX_V`) | ✅ **있다** |
| **G4 li_transport** | `norm > 0.30`, norm = `("bvs_x005", **+1**)` 의 **도펀트 풀 내 min-max** (`build_cascade_themes.py:295`) | ❌ **없다** |

⇒ **깔때기는 host 앵커를 쓸 줄 안다. 이온수송 축만 안 쓴다.**
전원이 host 보다 나빠도 최상위는 norm 1.0 을 받는다. **리뷰의 Y 사례가 정확히 그 사각지대다.**
그리고 리뷰가 지목한 기구 — *"Li⁺ 확산채널 주변 **국소 배위환경의 수축**"* — 은
**우리 BVS proxy 가 재는 바로 그 양**이다. **관측량은 맞고 기준점이 없다.**

#### J-15-3. 요구 3가지 (근거 있는 것만)

| # | 요구 | 근거 | ⛔ 안 하는 것 |
|---|---|---|---|
| ① | G4 에 **host 참조 부호**를 넣어 `bvs_x005(dopant) < bvs_x005(host)` 인 후보에 **`σ-regression` 플래그** | ★1 (문헌에 σ 하락 사례 존재, 정성) | **탈락시키지 않는다** — 리뷰의 Y 사례도 4800 h 라는 이득을 같이 보고한다. 필요한 건 탈락이 아니라 **가시성**. **문턱 제안 안 함**(리뷰에 크기 없음) |
| ② | 도펀트마다 **`intent: ionic \| electronic \| mechanical \| interfacial`** 선언 → intent 축 이득과 타 축 손실을 같은 화면에 | ★4 (σ↑ 9건은 캐리어/무질서/bottleneck 겨냥, σ↓ 1건은 전자구조 겨냥). 우리 `combine` 은 기하평균이라 **부호 뒤집힌 trade-off 를 지운다** | **교환율 제안 안 함** (리뷰에 근거 0) |
| ③ | 농도 3점(x=0.02/0.05/0.10)을 **평균하기 전에 단조성 검사**, 비단조면 `argmax` 병기 | **문헌 실측**: `Fig. 4a` **ALO5 0.25 → ALO10 0.45 → ALO20 0.35 mA cm⁻²** 비단조 + 본문이 침묵. ★1 의 *"insufficient ↔ excessive Y"* 창 | 이미 `audit_label_scatter.py` 가 재는 것 — **이 리뷰는 문헌 사례를 준다** |

#### J-15-4. ⛔ 이 축에서 인용하면 안 되는 것

- LPSCl **3–5** / LPSBr **6–8** / LPSI **~1 mS cm⁻¹** — **무출처**이고 **LPSI 가 통상치보다 2–3 자릿수 높다**
- LLZTO GB 개질 **×2.7** — 그림(`Fig. 5b`)이 **1.6×** 를 보이고 절대값이 3 자릿수 어긋난다
- "Y 도핑이 σ 를 N배 낮춘다" 류 — **숫자가 리뷰에 없다**
- 이 리뷰의 어떤 값도 `canonical_registry.json` · `cascade_stability_axes.csv` 에 **넣지 않는다**
- ⚠ **`cascade_stability_axes.csv` 는 코팅 후보 데이터이지 도핑체가 아니다**
  (`codex_BJ_prompt_cascade_redesign_2026_09_09.md` 철회블록) — **이 리뷰의 도핑 논의를 그 CSV 에 연결하지 않는다**

#### J-15-5. ✅ 반대로 이 축에서 **쓸 수 있는** 것

- *"DFT 2.1–2.5 V vs 실셀 3.5–4.2 V = 속도론적 부동태화"* **[28]** ← **우리 onset 2.256 V 가 이 대역 안**
  (⚠ *"같은 값"* 아니라 *"같은 대역"*. 리뷰는 상집합·압력·함수형을 안 밝힌다)
- *"high electronic conductivity, rather than mechanical properties, is the root cause of internal dendrite
  formation"* **[72]** Han 2019 ← **우리 modelc PDOS(CBM 에 Li 부재)의 so-what 받침**
- *"grand potential phase diagram 이 계면 열역학의 **the standard** 도구"* **[91]** ← **우리 T9 선택의 관행 근거**
- ★ gap 문장 재료 12건 (digest §14) — 특히 *"interface-centric paradigm demands continued investment in the
  **first-principles modeling of interface thermodynamics**"* = **우리 B2 작업의 정당화**


### J-16. ★★★ **황화물 전용 사전학습 MLIP — UMA 의 대체·committee·대조군 판정** ([Wang25DPA], 2026-09-09 신설)

> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_wang2025_pretrained_deep_potential_sulfide_sse.md` §③. 초안 번호 `J-11` → **`J-16`** 배정. 본문 안의 옛 번호 자기참조는 초안 번호다.

> 계기: UQ 3편(Grasselli / Carrete / Kurniawan)이 공통으로 *"단일 파운데이션 모델로는 committee 를
> 못 만든다"*(Grasselli 식 27 은 **M ≥ 4**)를 짚었고, 우리 이종 committee(UMA / MACE / SevenNet)는
> **훈련 코퍼스가 달라 §2.2 "equivalent models" 전제가 깨진다**(§J-1 · [Gra25UQ]).
> **[Wang25DPA] 는 그 빈칸을 메우는가?** — 세 갈래로 나눠 판정한다.

**갈래 ①: UMA 의 대체인가** → 🔵 **조건부 후보. 단 그 판정을 이 논문이 해 주지 않는다.**

| 근거 | 내용 |
|---|---|
| ⛔ **UMA 는 이 논문에서 시험되지 않았다** | 피고는 **DPA-2-MP · MACE-MP-0a(small) · M3GNet-MP-2021.2.8 · CHGNet · ORB-v2** = **전부 MPtrj 세대**. ⇒ *"범용 MLIP 가 장벽을 1/3 로 본다"* 는 **말할 수 있고**, *"따라서 UMA 도"* 는 **말할 수 없다** |
| ✅ 커버리지는 우리 계에 유리 | `Fig. 1` 1층에 **Li₆PS₅Cl 포함** · `Fig. S10a` 가 **우리 modelc 조성계열**(x=0.6 이 0.5–0.7 사이) · `Fig. S11` 이 **우리 O 도핑계** |
| ⚠ **b2o3 는 반대다** | **B–O 결합이 41계 어디에도 없다**(B 는 B–S 만, O 는 Li₂O 만). `Fig. 4a` 는 **Li–B–S 삼원(Li₂B₂S₅)조차 zero-shot 162.65 meV/atom 로 무너짐**을 보인다 ⇒ **b2o3 에 zero-shot 으로 들이대면 UMA 보다 나쁠 공산이 크다** |
| ❌ **Nd 는 범위 밖** | 란탄족이 15원소에 없다. type map 확장 가능 여부는 이 논문 밖 |
| ⚠ **비용이 판을 지배한다** | 사전학습 원본 `≈8.6×10⁻³` s/step·atom = **MACE-ft 보다도 46× 느림**. 우리 558원자 셀 환산 **200 ps 1런 ≈5.6일 · 9런 ≈50일** (`digest 계산`, 교차 하드웨어) ⇒ **규약에 그대로 못 꽂는다.** 증류하면 **≈18.8 ns/day = 9런 ≈2.3시간**, 즉 **UMA(252 ps/day) 대비 ~75× 처리량** |

**갈래 ②: committee 네 번째 멤버인가** → ⛔ **부적격.**

| Grasselli §2.2 전제 | UMA-s-1p1(omat) | DPA-SSE | 깨지나 |
|---|---|---|---|
| 같은 아키텍처 | equivariant 계열 | **DPA-2 (attention)** | ⛔ |
| 같은 훈련 분포 | OMat24 (범용) | **황화물 전용 54,771 프레임** | ⛔ |
| **같은 참조 PES** | **PBE 계열** | **PBEsol** | ⛔⛔ **결정적** |

> **한 줄 판정**: 두 모델이 **서로 다른 참조 PES 를 향해** 학습됐으므로 **둘의 불일치는 epistemic
> uncertainty 가 아니라 PBE−PBEsol 계통 오프셋을 포함한다.** committee spread 를 오차막대로 환산하는
> 순간 그 오프셋이 "불확실도"로 둔갑한다 ⇒ **우리 이종 committee 문제가 완화되는 게 아니라 축이 하나 는다.**
> ⚠ 저자 반론(*"PBE↔PBEsol 은 moderate shift 이고 fine-tune 이 흡수"*, 근거 `Fig. 5a,b` 의 두 범함수
> NEB 경로 일치)은 **fine-tune 하는 경우에만** 유효하다. 그리고 그 근거는 **LGPS 두 경로**에서만 확인됐다.

> ✅ **그러나 합법적 길이 하나 열린다**: 훈련 데이터가 **공개**돼 있으므로(AIS Square dataset id 217,
> 54,771 프레임) **같은 데이터·같은 아키텍처로 시드만 바꿔 M ≥ 4** 를 학습하면 Grasselli 전제를
> **정확히 만족하는 committee** 다. 값싼 변형: **증류 학생 모델을 시드만 바꿔 4–8개**(교사가 라벨을
> 공짜로 찍으므로 **DFT 추가 0**). ⚠ **그 committee 가 재는 것은 "학생이 교사를 못 따라간 분산"이지
> "교사가 DFT 에서 틀린 오차"가 아니다** — 두 층을 절대 섞어 부르지 않는다.

**갈래 ③: UMA 검증의 독립 기준인가** → ✅ **최적. 이것이 이 논문의 우리에 대한 실사용처다.**

| 우리 계 | DPA-SSE 를 심판으로 | 이유 |
|---|---|---|
| **comp1 / modelc** | ✅ **적격** | Li₆PS₅Cl 은 훈련 1층, Cl-rich 는 `Fig. S10a` 로 일반화 실증 |
| **LPSOCl (O 도핑)** | ✅ **적격** | `Fig. S11` 에 직접 대응 계가 있다 |
| **+B₂O₃** | ⛔ **부적격** | **B–O 결합 미커버.** ⚠ 특히 `db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json`(**봉인 2026-09-08, results_seen=false**)에 DPA-SSE 를 세 번째 심판으로 넣고 싶어질 텐데 — **넣으면 안 된다.** UMA(OMat24)는 B₂O₃ 를 봤을 공산이 크고 DPA-SSE 는 확실히 못 봤으므로, 둘의 불일치가 *"누가 맞나"*가 아니라 *"누가 그 결합을 봤나"*를 잰다. **⛔ 그 봉인 카드는 어떤 경우에도 수정하지 않는다** — DPA-SSE 는 **별도 카드**로 붙인다 |
| **Nd–O** | ❌ **범위 밖** | 란탄족 없음 |

**⇒ 실행 사다리 (digest §11-4 전문)**

| 단계 | 내용 | 비용 | 전제 |
|---|---|---|---|
| **0** | AIS Square model **id 266** / dataset `Solid_State_Electrolyte` **id 217** / Bohrium 노트북 **71679486918** 접근·라이선스·**type map 에 Cl·O·B 실재** 확인 | 반나절 · 계산 0 | ⛔ 못 받으면 아래 전부 무의미 |
| **0.5** ★★ | **§J-1 의 PET-MAD Li₃PS₄ test 243구조**(`db/properties/mlip_bench_li3ps4_uma.json`, 도구 `tools/mlip/bench_against_dft.py`)에 **DPA-SSE 를 그냥 태운다**. **라벨이 PBEsol = DPA-SSE 모국어** | 몇 시간 · **DFT 0회** | ⚠ **공정한 대결 아님** — `Fig. 1` 2층에 Li₃PS₄ 로 보이는 항목이 있어 **DPA-SSE 에겐 훈련 근처, UMA 에겐 외부**. *"훈련셋 안이면 얼마나 좋은가"* 를 잴 뿐. ⛔ **§J-1 의 30.0 과 논문의 30.28 을 나란히 놓지 마라 — test set 이 완전히 다르다** |
| **1** | 우리 궤적 스냅샷에 UMA·DPA-SSE 단일점. **표본 규칙은 b2o3 봉인 카드 §4 의 결정적 규칙 재사용**(700 K, s2·s3, 2–50 ps 창 등간격 5프레임). 보고량은 **절대 \|ΔF\| 가 아니라 비** | 하루 | ⛔ **b2o3 제외.** ⛔ **봉인 카드 수정 금지 — 새 카드로** |
| **2** | Step 1 에서 가장 갈린 **20–40 프레임에 PBE·PBEsol 단일점을 둘 다** | 1–2일 (kgy CPU) | 이게 없으면 **PBEsol 모델을 PBE 자로 재는 것** |
| **3** | ① `Fig. 5a,b` 형식 **NEB 3자 대결**(UMA · DPA-SSE · 우리 DFT) → *UMA 가 base 무리(1/3 장벽)인가* 한 장 판정 ② `Fig. S3` 형식 **500 K NVE 100 ps 드리프트** → **우리 UMA 가 보존형 힘을 쓰는가** | 2–3일 | ★ ②는 **지금 당장 할 수 있는 최저비용·최고가치**. Langevin NVT 는 비보존성을 **가려 준다** |
| **4** | 증류 → 우리 규약 재실행 | 1–2주 | ⚠ **두 개의 σ·Ea 가 생긴다.** `comparison_group` 과 정본 규율을 **결과 보기 전에** 정한다 |
| **5** | 시드만 바꾼 학생 M ≥ 4 = 합법 committee | 선택 | ⚠ 증류 분산 ≠ 모델 오차, 카드에 먼저 명시 |

**🔴 [Wang25DPA] 가 §J-1 에 주는 직접 소득**
> §J-1 의 명시적 한계 **#3 — *"Cl 이 없다 … 아르지로다이트·Cl 무질서로의 전이를 이 벤치가 보증하지
> 않는다"*** 를 이 논문이 **정면으로 메운다**: Li₆PS₅Cl/Br/I 가 훈련 1층이고, **Cl-rich 시리즈**(`Fig. S10a`)와
> **O 도핑 시리즈**(`Fig. S11`)까지 시험됐다. ⚠ 단 *"Cl 이 있다"* 와 *"Cl 이 충분하다"* 는 다르다 —
> `Fig. 1` heatmap 의 **Cl 칸이 옅고**, `Fig. S1` 에서 **LPSCl 만 두 개의 이상 신호**를 낸다(§13-3).

**⛔ 이 축에서 인용하면 안 되는 것**
1. *"이 논문이 UMA 를 시험해서 나쁘게 나왔다"* — **UMA 는 시험 대상이 아니다.**
2. `Fig. 7` 의 속도값을 **우리 하드웨어 약속으로** 쓰는 것 — V100+12코어 vs A6000, **자릿수 판정용**.
3. 논문 σ·D 를 **우리 db 절대값과 같은 표에** 놓는 것 — MSD 창·시드·셀 미기재.
4. *"DPA-SSE 가 UMA 보다 정확하다"* — **아무도 그 비교를 하지 않았다.** Step 0.5–3 이 그 시험이다.
5. `Fig. S2` 를 *"호핑 장벽 에너지 과소평가의 증거"* 로 — **eV/atom 축이라 장벽 스케일을 못 담는다.**
   그 증거는 **`Fig. 5a,b`** 다.


### J-17. 🔧 방법 원전 — **descriptor 표현(representation)** · argyrodite 전용 (2026-09-09 신설)

> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_zhao2021_hecs_descriptors_argyrodite_activation_energy.md` §②③. 초안 번호 `J-13` → **`J-17`** 배정. 본문 안의 옛 번호 자기참조는 초안 번호다.

> ⛔ **A–D 물성 4축 표에 넣지 않는다.** σ·ESW·탄성·gap **0건**, Ea 는 **BVSE 라벨**이라 우리 MLIP-MD Ea 와
> 다른 양이고 조성 귀속조차 논문에 없다. 여기 있는 것은 **"argyrodite 를 무엇으로 기술할 것인가" 의 정의 원본**이다.
> 짝 블록: **J-11 `[Basu26MFB]`** = *예산을 어디에 쓰나(탐색)*, **여기 `[Zhao21HECS]`** = *무엇으로 기술하나(표현)*.

**[Zhao21HECS] `zhao2021_hecs_descriptors_argyrodite_activation_energy`** — Q. Zhao / M. Avdeev / L. Chen / **S. Shi\*** (Shanghai Univ MGI + ANSTO), *Sci. Bull.* **66**, 1401–1408 (2021), DOI `10.1016/j.scib.2021.04.029`. **입방 Li-argyrodite 50종 · 32 descriptor · PLS 4성분 · 라벨 = BVSE(SPSE)**. ⛔ DFT·AIMD·NEB·실험 **전부 0건**.

| 항목 | [Zhao21HECS] | 우리 (현행 / 계획) | 판정 |
|---|---|---|---|
| **표현 골격** | **Global(셀: 조성·구조) ⊃ Local(케이지: 전도경로·이온분포·특수이온)** 2층 × 5범주 → 32 스칼라 (`Fig. 1`·`Fig. 2b`) | cascade 는 **descriptor 를 하나도 안 정했다** (Codex BJ NO-GO 반려사유와 별개로 표현 자체가 공백) | ⭕⭕ **이식 후보 — 이 골격을 v0 로 채택 제안** (digest §13.2) |
| **argyrodite 자리 라벨** | **A=4a 음이온 · B=4b 양이온 · C=4c(=4d) 자유음이온 · E=16e (BE₄ 의 음이온) · Li=48h/24g** — 4a·4c 를 **`special ions` 독립 범주로 승격**(r_A·EN_A·r_C·EN_C, **4개 전부 VIP>0.8**, r_C 공동4위 1.29) | 우리 O-모티프 실측(`ndo_lpscl16_o_motif_estimand_2026_09_09.json` ⑨): **P–O 결합 3/3 = E(16e)** vs **P–O 0/3, Li/Nd 케이지 = A/C** | ⭕⭕ **1:1 대응 성립.** HECS 표현이 우리 두 O-모티프를 **구분할 수 있다** — 조성-only descriptor 는 불가 |
| **무질서 처리** | ⭐ **초격자를 안 만든다.** 부분점유 CIF 를 그대로 두고 **점유율·배위엔트로피 스칼라로 압축**(OCC×3, Sconf×4) | **실제 배열을 만든다** (단일배열 또는 disorder ensemble, 예: `comp2_disorder_ensemble` d=0.50 3config) | ⚠ **정반대 노선.** 섞으면 안 된다 — 배열마다 계산해 앙상블로 낼지, 점유율에서 직접 낼지 **보고량 카드에 먼저 못박아야** 한다 |
| **입력 구조** | **실험 정련 CIF** (본문 *"to preserve the experimentally determined structure information"*) | **DFT-이완 V0 셀** (comp1_V0_k444 등) | ⛔ **다른 축.** 같은 descriptor 라도 값이 다르다 ⇒ 논문 값과 직접 비교 금지 |
| **중요도 측정** | **PLS 의 VIP**, 컷 **0.8 (JMP 기본값)**. SHAP·permutation 아님 | (미정) | ⚠ **컷 1.0(표준)을 쓰면 Sconf 3인방이 탈락** — 헤드라인이 컷 선택에 걸려 있다. 우리가 쓸 땐 **컷을 결과 보기 전에** 정한다 |
| **다중공선성** | 심각 (`Fig. S2`: **a↔v = 1.00** · r_anion↔a/v ≈0.95 · r_anion↔D_Li-B ≈0.92) → 그래서 PLS 를 골랐다고 밝힘 | — | ⚠ **VIP 를 개별 descriptor 의 인과 기여로 읽으면 안 된다.** 상위 4개가 사실상 한 변수 |
| **BN(병목 크기) 정의** | 🔴 **계산식이 없다.** 논문 서사의 중심(전략 ①"broaden bottleneck size")인데 Table S2 는 이름만. 축 범위 `figure-read` intra ≈0.44–0.72 Å · inter ≈0.487–0.62 Å (Li⁺ 반경보다 작아 **여유반경**으로 보임 — 우리 해석) | **BVSE 채널 %** (above-min ≤ iso, 0.25 Å voxel, **원본 주기셀만**, `tools/comp1_v3/`) — **정의가 문서화돼 있다** | ⭕ **우리 쪽이 낫다.** BN 자리를 우리 채널% 로 대체 |
| **Sconf 정의** | 🔴 **식·단위 규약 없음.** `figure-read` 축 0–33 J/(K·mol) 인데 per site / per f.u. / per cell 불명 | (미정) | 🔴 **우리가 못박아야** — `−R Σ pᵢ ln pᵢ` × 자리당 원자수, 규약 기록 |
| **반경·EN·분극률 표** | 🟡 **어느 표인지 안 밝힘** ("Pauling EN" 만 명시) | (미정) | ⚠ 우리가 정하면 **논문 값과 절대 비교 불가** ⇒ 내부 일관성만 |
| **검증** | 80/20 hold-out **1회**(40/10) + LOOCV(성분수 선택용). **group-out 없음 · 반복분할 없음 · 외삽 검증 0건 · 시드 미기재** | 우리 실측: **쌍 LOOCV 0.0892 → LODO −0.1805 → L2DO −0.2548** (group-out 낙차 0.27) | ⛔ **우리가 앞선다.** 그들 0.82 는 무작위 분할값이고 group-out 이면 크게 내려갈 것으로 보아야 한다 |
| **보고 성능** | R² 훈련 0.887 / 시험 **0.820** · RMSE 0.02 eV | — | ⛔ **시험 0.820 은 논문 자신의 Eq.(5) 정의를 안 지킨다 — 정정 0.7661** (0.820 = Pearson r²). **자기 LOOCV Q² = 0.65877** 이 가장 정직한 값인데 성능으로 안 쓴다 |
| **라벨** | **BVSE (SPSE)** — 파라미터 전부 미기재 | **MLIP-MD Ea** (UMA-s-1p1, 600/800/1000 K, MSD 2–50 ps) + 별도 **BVSE(bvlain)** | ⛔⛔ **여기가 결정적 결렬점** — 아래 |

**⛔⛔ 결정타 — 이 논문의 타깃이 우리 조성축에서 이미 뒤집혀 있다**

| 계 | BVSE(bvlain) E_3D | MLIP-MD Ea | 방향 |
|---|---|---|---|
| comp1 `Li₆PS₅Cl` | **0.2734 eV** | 0.2532 eV (단일시드) | |
| modelc `Li₅.₄PS₄.₄Cl₁.₆` | **0.4785 eV** | 0.197 ± 0.032 eV (3시드) | **완전 역전** |

출처 `db/properties/bvse_bvlain_ev_4sys.json` · **`⚠_VERDICT_ranking_forbidden`**: *"가족 내 랭킹은 MD와 역전 … vacancy paradox(점유-무관 지도)가 eV 단위에서도 그대로 재현된 것. → σ/Ea 순위 인용 금지."* 그리고 `kb/concepts/bvse.md` §9: **comp1→modelc 는 "채널부피 −15 % 인데 σ ×4 ↑"** 이고 원인은 **vacancy/무질서 = 점유-무관 지도의 원리적 사각**.
⇒ Zhao 의 VIP 가 **Li 관련 8개를 전부 컷 아래로 떨어뜨린 것**은 물리 발견이 아니라 **이 사각의 지문**이다.
⇒ **판정: descriptor 표현은 채택 후보, 라벨(BVSE)과 학습된 모델은 우리 Cl-rich 랭킹에 사용 금지.**

**⭕ 유일하게 방법론적으로 정당한 숫자 대조 — BVSE ↔ BVSE**
우리 comp1 BVSE E_3D **0.2734 eV** vs 이 논문 Li₆PS₅Cl BVSE **≈0.322 eV**(⚠ **우리 추론** — `Fig. 7` 상한 0.322 가 Table S1 라벨 격자값 0.322265625 와 정확 일치). 차이 **≈49 meV**. ⚠ 코드(bvlain vs SPSE)·파라미터·구조(DFT-이완 vs 실험정련)·percolation 차원 정의가 전부 달라 **"같은 자릿수" 까지만**. ⛔ 이 값을 우리 MLIP-MD Ea 와 같은 표에 넣지 않는다.

**★ 설계 추천이 우리 조성족을 이름 그대로 지목한다**
`Fig. 7` 전략 ①"작은 음이온 치환" 의 1번 예시가 **`Li₆₋ₓPS₅₋ₓCl₁₊ₓ` (Ea < 0.322 eV)** — 우리 modelc `Li₅.₄PS₄.₄Cl₁.₆` 와 **같은 족**이다. ⚠ 단 **예측 Ea 숫자는 논문에 없고**(상한은 모체 라벨값), **`r_anion` 축에서 우리 조성이 그들 훈련 범위 왼쪽 경계 밖**이다(digest §7.1) ⇒ **"문헌이 우리 조성을 유망하다고 예측했다" 는 문장은 쓸 수 없다.** 쓸 수 있는 것은 *"같은 설계 방향(Cl 증가 → r_anion 감소)을 독립적으로 제안한다"* 까지.

**축 J 안의 상호참조 (초안 ③ — 번호는 초안 당시: J-11=[Basu26MFB]→지금 J-12, J-13=이 편→지금 J-17)**

- **J-9 `[Cho25AL]`·`[Ma25AL]`** = 능동학습 루프 — **오라클(라벨)을 어떻게 고르나**
- **J-10 `[Jain26Rev]`** = 깔때기 모양 — **무엇을 어떤 순서로 자르나** (⚠ 리뷰라 2차 인용)
- **J-11 `[Basu26MFB]`** = 각 단의 판정 계약 + fidelity 전환 규칙 (⚠ preprint·단독저자)
- **J-13 `[Zhao21HECS]`(이 편)** = ⭐ **표현(representation) — 후보를 무엇으로 기술하나.**
  argyrodite 전용 descriptor 목록으로는 **우리 corpus 유일**이고, **자리(4a/4b/4c/16e/48h) 분해**가 있는 것도 이것뿐이다.
  ⚠ 단 **DFT 0건 · 라벨이 BVSE · 재현 불가** — "원전" 은 *표현*에 한정된다.

**확보 후보 (이 논문의 참고문헌, 우리 미보유)**

| ref | 서지 | 왜 필요한가 |
|---|---|---|
| **[28]** | He B, Chi S, Ye A, et al., **"High-throughput screening platform for solid electrolytes combining hierarchical ion transport prediction algorithms"**, *Sci. Data* **7**, 151 (2020) | ⭐⭐ **이 논문 라벨 50개 전부의 출처.** BVSE 설정(R₀·b·voxel·percolation 정의)이 여기 있을 가능성이 높다 — Zhao 본문에는 **하나도 없다**. 공개 웹 `matgen.nscc-gz.cn/solidElectrolyte/` |
| **[30]** | Farrés M, Platikanov S, Tsakovski S, et al., **"Comparison of the variable importance in projection (VIP) and of the selectivity ratio (SR) methods"**, *J. Chemometr.* **29**, 528 (2015) | VIP 컷오프(0.8 vs 1.0)와 상관군 안 중요도 분배의 규범 문헌. 우리가 VIP 를 쓸 거면 **컷을 결과 전에 정하는** 근거로 필요 |
| **[38]** | Wang Z, Shao G, **"Theoretical design of solid electrolytes with superb ionic conductivity: alloying effect on Li⁺ transportation in cubic Li₆PA₅X chalcogenides"**, *J. Mater. Chem. A* **5**, 21846 (2017) | argyrodite 합금화의 **계산(DFT) 축** — Zhao 가 BVSE 로만 다룬 같은 조성공간을 DFT 로 본 편 |

**이미 보유한 인용 관계 (역링크만 걸면 됨)**

| ref | 우리 digest |
|---|---|
| [20] Fujimura 2013 | `papers/fujimura2013_ml_conductivity_origin.md` |
| [25] Sendek 2017 | `papers/sendek2017_ml_screening_12k_conductors.md` (⭐ 소표본 방어 절차는 Sendek 이 우월 — Zhao 는 X-randomization·부트스트랩 **0건**) |
| [34] Deiseroth 2008 | (미보유 — argyrodite 원전) |
| [35] Kraft 2017 | `papers/kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md` (⭐ `PL_anion` descriptor 의 물리 근거) |


### J-18. 🔧 불확실도(UQ) 축 — **통계(random) 축과 모델(epistemic) 축은 다르다** (2026-09-13 병합 신설 · 초안 [Carrete23UQ] 2-c "J-11 신설 제안" + [Maginn19MD] 2-d)

> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_carrete2023_deep_ensembles_vs_committees.md` §2-c. + `_pending_index_maginn2019_…` §2-d. 초안이 "J-11" 로 부른 절이 이것이다 (J-11 은 2026-09-12 에 [Honrao21] 이 먼저 가져갔다). 정본 목록: 통계 축 [Maginn19MD]·[Pranami15]·[McC25D]·[Zaby26σ] · 모델 축 [Imbalzano21]·[Carrete23UQ]·[Kurn26UQ]·[Gra25UQ] — 각 편의 본문은 J-7.

형제 4편 pending 이 이미 제안한 대로 `J-11. 불확실도` 를 만든다면, 절 머리에 **두 축 분리 선언**을 박아 둘 것:

> **J-11 은 두 축이다. 섞으면 틀린다.**
> · **통계(random) 축** — 궤적이 유한해서 생기는 요동. 정본 = **[Maginn19MD]**. **복제·시간원점·창 선택**으로 줄어든다.
> · **모델(epistemic) 축** — MLIP 가 틀려서 생기는 편향. 정본 = **[Imbalzano21] · [Carrete23UQ] · [Kurniawan25] · [Grasselli25]**. **복제로는 안 줄어든다.**
> 우리 `Ea 0.197 ± 0.032 eV`(modelc 600 K 3-seed) 의 **±0.032 는 통계 축이고, 모델 축 추정치는 우리에게 아예 없다.**

> 오늘 들어온 불확실도 4편(#78 · **#79 = 이 편** · #80 · #81)이 하나의 축을 이룬다.
> 이 편이 그중 **유일하게 end-to-end**(추정기 구현 → MD 감시 → 재학습 → 능동학습 → 표면 확장)라
> **축의 뼈대로 삼기 적합**하다. 형제 에이전트가 #78/#80/#81 을 넣을 자리를 여기로 모을 것.

**J-11 이 답해야 하는 질문 = "우리는 UMA 가 이 계에서 얼마나 확신하는지 재고 있나?" → 지금은 아니다.**

| 우리가 지금 가진 것 | 이 축이 말하는 이름 | 빈 칸 |
|---|---|---|
| 3-seed MD 산포 `Ea 0.197 ± 0.032 eV` | **열적 샘플링 산포** (aleatoric 도 epistemic 도 아님) | — |
| 없음 | **epistemic σ** (모델 앙상블 분산) | 🔴 **비어 있다** |
| 없음 | **σ_f 공간분해** (층·원자별) | 🔴 **비어 있다** |
| UMA 힘 MAE 30.0 meV/Å (§J-1) | **평균 정확도** | ⭕ 있음 — 단 [Carrete23UQ]·[Zhang26] 둘 다 *"평균이 좋아도 특정 양은 틀린다"* 를 보인다 |

**이 축에서 ⛔ 하면 안 되는 것**
- **σ 를 신뢰구간으로 읽기.** `Fig. 7` 에서 학습범위 밖 실제 오차 **≈40 eV Å⁻¹** 를 띠(**±4–6**)가 전혀 못 감싼다. *"몇 σ 안에 참값"* 문장을 이 논문으로 지지할 수 없다.
- **서로 다른 퍼텐셜을 σ 로 비교하기.** AL 이 돌면 **σ 가 실제 오차보다 빨리 준다**(저자 자인) ⇒ comp1 과 modelc 를 UMA σ 로 비교하면 안 된다. **우리 기존 규율(σ 절대값 인용 금지·비율도 멀티시드 판정만)의 외부 근거가 바로 이것.**
- **원자 단위로 "고σ 원자만 보강" 전략 쓰기** (`Fig. 11` 반례).
- **[Carrete23UQ] 의 어떤 물성값도 우리 표에 올리기** — 재료계가 다르다.


### J-19. 🆕 미세구조·입계(GB) 축 — [Ou26MS] (2026-09-13 병합 신설 · 초안 ou 2-d "J-12 후보")

> 📎 병합 2026-09-13 병합 — 초안 `_pending_index_ou2026_microstructural_multiscale_fast_ion_transport.md` §2-d. 절 번호는 병합자가 배정했다 (초안: "J-12 후보").

> **우리에게 통째로 없는 축이고, 이 편 하나로 열 수 있다.**
> 질문: *"우리 D_bulk 와 실험 σ 사이의 격차 중 입계 몫은 얼마인가?"* → **답: µm 입도에서 1 % 미만.**

| 우리가 지금 가진 것 | 이 축의 이름 | 빈 칸 |
|---|---|---|
| D_bulk (comp1 3.09e-6 / modelc 7.90e-6 @600 K) | **벌크 자기확산** | ⭕ 있음 |
| 없음 | **D_GB (입계 확산)** | 🔴 비어 있음 (이식하면 폭 2.5 nm 가정이 딸려온다) |
| 없음 | **D_macro (다결정 유효)** | 🔴 비어 있음 — **`PolycrystalDiffusion`(LGPL-3.0)으로 라벨 0개 sweep 가능** |
| 없음 | **공극·접촉 항** | 🔴 비어 있음 — 이 논문도 FE 로 안 풀고 후보정 배수(3모델이 10× 갈린다) |
| DEM 펠릿 축 (별도 repo 축) | **분말 압축·공극률** | 🔶 있으나 DFT 축과 연결 안 돼 있음 ← **여기가 다리다** |

**이 축의 판정 3줄 (지금 바로 원고에 쓸 수 있는 것)**
1. **입계는 µm 입도에서 무시해도 된다** (D_macro/D_bulk = 0.993 @1 µm, 0.942 @100 nm).
2. **벌크 예측이 QENS 와는 1.07× 로 맞고 EIS 와는 6–38× 어긋난다** ⇒ 격차의 주인은 **펠릿**이다.
3. ⛔ **"GB 가 없으니 우리 D 를 실험 σ 와 직접 비교해도 된다"로 읽으면 안 된다** — 공극·접촉 항이 남아 있고,
   그 항의 크기는 이 논문에서도 모델에 따라 **10× 갈린다**.

### J-20. 🔴 **계면 방법 감사 — [Wu26MLIF] 가 우리 0 K hull 을 어떻게 평가하나** (2026-09-22 신설)

> 📎 출처: `papers/wu2026_ml_driven_electrolyte_interface_design_review.md` (논문 에이전트, 2026-09-22).
> ⛔ **이 편은 자체 값이 0 이다.** 물성 4축(A–D)에 한 줄도 넣지 않는다. 여기는 **방법 축**이다.
> ⚠ 이 리뷰의 **모든 숫자는 2차 인용**이고, 확인된 것만도 **조건 탈락 1건 · 참고문헌 오귀속 1건 ·
> 본문↔그림 불일치 1건**이 있다 (아래 4). **원전 확인 없이 옮기지 마라.**

**1. 우리 방법을 정면으로 때리는 두 문장** (이것이 이 편의 본체다)

| # | 리뷰 원문 요지 | 위치 | 우리한테 유효한가 |
|---|---|---|---|
| ① | *"**Reliance on convex-hull thermodynamics alone limits the realism of such models**"* — 현재 모델들이 이상적 화학량론을 가정하는데 실제 전해질은 조성 자유도가 크고, 고성능 상당수가 **준안정상**이라 합성 시 운동학 제어가 필요하다는 맥락 | §2.5 | 🟡 **부분 유효.** 리뷰가 겨냥하는 것은 *후보물질 생성* 쪽 능동학습이다. 우리는 hull 을 **계면 반응산물 선택**(Richards 식 grand-potential)에 쓰고, 보호율 식은 **산물의 P/Nd 비**만 쓰지 에너지 절대값을 안 쓴다 ⇒ 껍질 오차에 1차적으로 둔감. ⛔ **그러나 면제가 아니다** — 산물 *집합* 자체가 hull 로 골라지고, hull 밖 준안정 중간상(LPSCl 의 Li₄PS₄Cl/Li₁₁PS₅Cl, §B [Rupp])은 우리 반응식에 **아예 안 나온다** |
| ② | *"정적 계면형성에너지만으로는 계면이 실제로 쓸 만한지 결정할 수 없다"* + *"계면 열화의 **속도와 최종 형태**는 열역학 구동력보다 **운동학 인자**가 더 지배한다"* | §4.3 (근거 [132] Guo *JMCA* 13, 38919 (2025)) | 🔴 **완전 유효.** 우리 `GrandPotentialInterfacialReactivity` 는 **0 K 평형 반응에너지 하나**만 낸다 — 시간축이 없다. 그리고 §B 에 **이미 증거가 있다**: 우리 산화 onset **2.256 V** vs 실측 kinetic onset **2.5–2.9 V**(독립 4–5개 표) — 그 격차가 리뷰가 말하는 **운동학 여유**다 |

**🔑 그런데 리뷰는 hull 폐기를 요구하지 않는다** — *"계면 평가 논리를 정적 열역학 기준에서
**운동학과 기능을 함께 저울질하는 종합 기준으로** 진화시킨다"* 다. 즉 **hull 은 여전히 1단 필터**이고
그 위에 (a) 부동태화 여부 (b) 중간층의 이온/전자 성격 (c) 성장 시간법칙이 얹혀야 한다.
⇒ **우리 방어 문장은 "hull 은 틀리지 않았다" 가 아니라 "hull 은 *어떤 반응이 일어나는가*까지만
답하도록 설계된 도구이고, 우리는 그 답만 주장한다" 여야 한다.**

**2. 🟢 우리 프레이밍을 리뷰 언어로 번역해 주는 3분법** (§4.3)

> *"계면은 안정/불안정의 2분법이 아니라 최소 **3분법**으로 갈라야 한다 — **(i) 진짜 불활성 안정 ·
> (ii) 보호층을 만드는 부동태 · (iii) 계속 반응해 장벽층을 두껍게 하는 활성.**
> 전고체전지에서 공학적으로 값있는 것은 **두 번째**다."*

⇒ 우리 Nd 도핑 주장이 정확히 **(ii) 칸**이다 (*"분해를 없애는 게 아니라 분해 산물을 바꾼다"*).
**원고에서 우리 기여의 칸을 이 문장으로 선언할 수 있다.**

**3. 🔴 §4.6 "원자단위 양 → 실험 조절변수" 번역표 — 우리 빈칸 진단**

| 원자단위 양 | 리뷰의 설계규칙 | 원전 | 우리 |
|---|---|---|---|
| 계면 형성/반응 에너지 | 조성→반응성 지도 · **저반응성 설계영역** · 코팅 후보 발굴 | [139] Park *Adv. Sci.* e76305 (2026): **809 Li 화합물 × 10 산화물 양극 × 7 황화물 전해질** + 비지도 군집 | 🟢 **같은 층위** — 단 Park 은 **ex-situ 코팅 선택**, 우리는 **in-situ 도펀트 보호상** |
| **Δμ_Li + 공간전하** | 산화물 양극 + 황화물 SE = 강한 내장전계 → **nm 규모 Li 고갈** ⇒ 황화물 양극 또는 **유전 완충층** | ⚠ **리뷰가 ref 를 안 붙였다** | 🔴 **없다.** 우리 grand-potential 은 μ_Li 를 **공간 무관 스칼라**로 다룬다 |
| 확산 위상 | 공소결 중 **Li 화학량론 제어** (Li-poor 종단 = Co 상호확산 심각) | [137] Kim LLZO\|LCO | ⛔ 없음 (우리 BVSE 채널% 가 정적 사촌) |
| SEI 4단 + 시간법칙 | **이온전도·전자절연 중간층**이 되게 · 혼합전도층 두꺼워지지 않게 | [130][131] | ⛔ 없음 |
| **전자누설 (SEI 밴드갭)** | *"조성만이 아니라 **전자구조**를 제어하라"* ⇒ **갭을 넓혀** 전자누설 차단 | [135] An *ACS Nano* 19, 14262 (2025) | 🟡 **갭은 있다** (comp1 2.066 / modelc 2.099 eV) — 지금까지 "wide-gap insulator" 라는 말밖에 못 붙였는데 **기능적 의미가 생긴다** |
| W_ad (접착·응력) | MLIP **steered-MD** 로 정량 · **결정면 배향 의존** (Cathode(100)/SSE(100) 우수) ⇒ **화학 수정과 독립인 설계 레버** | [140] Shin *JPS* 653, 237670 (2025) | ⛔ 없음 (§H 의 W_ad 빈칸과 동일) |
| 분해 경로 | 코팅 **4조건 동시 만족**: 분해 구동력 제거 · **Li 경로 보존** · 양이온 상호확산 차단 · **전자절연 유지** | [132] Guo | 🟡 **산물까지만** (1·4 만 부분) |

**최종 매핑 (리뷰 §4.6 결론)**: 원자단위 관측량 → 실험 조절변수 **5개** =
**코팅 조성 · 코팅 두께 · 계면 화학량론 · 결정면 배향 · 접촉압력**.
⇒ 우리 CEI 기여는 **"코팅 조성"** 칸이고, **"코팅 두께"** 칸이 우리에게 비어 있다는 것이 같은 문장에서 드러난다.

**4. 🔴 우리 보호율 식이 약해지는 지점 — "덮을수록 좋다" 의 반례**

우리 보호율 `min(1, k·x/(1−x))` 는 **단조 증가**이고 **대가 항이 없다**. 리뷰가 주는 반대 증거:

| 양 | 값 | 출처 |
|---|---|---|
| a-LiF 코팅 임계두께 | **≈1 nm** — 넘으면 규칙 Li–F 사면체 생성 → Li⁺ 수송 방해 | [47] Hu *AFM* 34, 2402993 (2024), **LCO/Li₆PS₅Cl · DeePMD** |
| D_Li (5 Å) | (0.056 ± 0.003) ×10⁻⁵ cm²/s | `Fig. 15a` (figure-read: 범례) |
| D_Li (10 Å) | (0.063 ± **0.037**) ×10⁻⁵ cm²/s ⚠ **오차가 값의 59 %** | 같음 |
| D_Li (20 Å) | (0.017 ± 0.003) ×10⁻⁵ cm²/s — **5 Å 대비 3.3×↓** | 같음 |
| 사면체 개수 | 5 Å **0** → 20 Å **86** | `Fig. 15b` |

⛔ **"1 nm 가 임계점" 은 3점 보간 해석이다** — 오차막대가 5 Å 값을 덮는다. 깨끗한 진술은 *"20 Å 에서 3.3× 감소"*.
⛔ **창이 다르다**: 이 D 는 **10 ns 전구간** MSD 이고 우리 규약은 **2–50 ps 고정**이다 → **값 비교 금지**.
⇒ **우리가 할 일**: 생성 몰수 × 몰부피 ÷ 비표면적으로 Nd 인산염 층을 **nm 로 환산**해 1 nm 이하임을 보인다
(계산 없이 산수로 된다). 안 되면 §Limitations 에 *"피복 면적분율만 다루며 두께 최적점은 다루지 않는다"* 로 명시.

**5. 🟠 "Li 예산" 이라는 이름 — 동명이물 주의**

| | [Wu26MLIF] §4.6 | 우리 |
|---|---|---|
| Li 를 움직이는 것 | **공간전하 / 내장전계**(정전기) | **분해 산물의 화학량론**(Li₃PO₄ Li/P=3 vs NdPO₄ Li/P=0) |
| 어디서 | 계면 **nm 대역의 공간분포** | 반응식 안 — **공간 없음** |
| 결과 | Li 고갈층 → 임피던스 | Li 을 덜 쓰는 경로가 열림 → 산화 대가 감소 |
| 처방 | 황화물 양극 또는 **유전 완충층** | **Nd 도핑** |

⇒ **선행 중복 아니고 상보적**이다. 단 **이름을 그대로 쓰면 리뷰어가 공간전하 문헌을 들고 온다**
⇒ 원고에서는 **"분해 화학량론 구동 Li 재분배"** 로 이름을 분리한다.

**6. uMLIP 로 계면을 대체할 때의 정확도 상한** (`Fig. 11`, InterOptimus [125] · **전부 figure-read**)

| 계 | 모델 | r_s | MAE (J m⁻²) | ΔX̄ (Å) |
|---|---|---|---|---|
| Li₂S\|Ni₃S₂ | ORB / 7Net | 0.95 / 0.92 | **0.1** / 0.31 | 0.08 / 0.06 |
| LiF\|NCM | ORB / 7Net | 0.88 / **1.0** | **0.61** / 0.46 | 0.07 / 0.09 |
| **Li₃PS₄\|Li** | ORB / **7Net** | 1.0 / **0.83** ⬅최저 | 0.2 / 0.37 | 0.21 / **0.51** ⬅최대 |

⇒ **순위는 살고(r_s 0.83–1.0) 절대값은 안 산다(MAE 0.1–0.61).** 그리고 **우리 계에 제일 가까운
황화물 SE‖Li 칸이 가장 나쁘다.** ⚠ 본문(§4.2)은 이를 *"rigorously validated"* 라 쓰고 **캡션은 모델이
2종(ORB/7Net)이라는 사실 자체를 안 적는다** — **본문↔그림 불일치**. 사양: **uMLIP 로 후보 정렬까지,
절대값이 필요하면 DFT.**

**7. ⛔ 이 편에서 **인용하면 안 되는 것** (§J-6 에 준함)**

- **σ 13.02 mS/cm** (§2.5) — **프로토콜 탈락**. 우리 `cho2025…` digest: **가압유지 13.02 / 관행 7.45**.
- **`Table 3` uMLIP 등급** — `Moderate/High/Top-tier` **서수 라벨뿐, 숫자 0**. "벤치마크" 로 인용 금지.
  정량이 필요하면 원전 [76] Du *ACS Mater. Lett.* 7, 3403 (2025) 또는 `chang2026…` digest.
- **본문 [118] 인용** — LLZO 이중도핑 근거로 달린 [118] 이 *Mater. Lett.* SrVO₃ **음극 나노입자** 논문이다
  (`Table 5` 는 같은 내용에 [112] 를 인용). **명백한 오귀속.**
- **"Chaney 가 4단계로 구분" (§4.3)** — [130] 의 **제목이 "Two-Step Growth Mechanism"** 이다.
  4단계를 인용하려면 **[131] Ren *EES* 17, 2743 (2024)** 를 보고 쓴다.
- **"ML 이 재료발견의 중심 허브가 되었다"** — `Table 1` 의 3요소를 동시에 구현한 사례가 **리뷰 안에 없다**.
  전망 문장이지 결론이 아니다.
- **`Fig. 12` 의 "입계에서 Li 환원"** — 컬러바가 **0.50–0.55 e** 뿐이다. **부분전하 0.05 e 이동**이지
  Li⁰(1.0 e) 이 아니다. ⚠ **우리도 Bader/CDD 논법을 쓰므로 같은 함정** — 스케일 폭 명시 규율.

**8. 🔴 UMA 의 자리 — 이 리뷰 지형에 **없다****

전문 `UMA` **0회** · `Meta` **0회**. `Table 3` 6종(M3GNet·CHGNet·MACE-MP-0·SevenNet-MF-ompa·MatterSim-v1·Orb-v3)
· 본문 §2.3 열거 · 인용 벤치 [76](12종) 어디에도 없다. ⛔ 우리 `chang2026…`(argyrodite 5종 벤치)에도 없다.
⇒ **UMA 선택은 원고에서 정당화해야 한다.** 답할 재료는 §J-1 에 이미 있다 —
`db/properties/mlip_bench_li3ps4_uma.json` **힘 MAE 30.0 meV/Å**(리뷰가 적은 범용 대역 **40–80 meV/Å** 아래,
전용 대역 **<50** 안). ⚠ **리뷰 값은 RMSE, 우리 값은 MAE — 같은 통계량이 아니다.** 대역 비교로만 쓴다.
🟢 리뷰 자신의 처방(*"모델 선택은 가정하지 말고 **검증**해야 한다"*)을 **우리는 자기 계에서 직접 재서 만족**한다.

**9. 🟢 positioning — 이 리뷰가 우리 약점을 **필드 공통 난제**로 규정해 준다** (§5.1 "스케일 통합")

> *"벌크 전도도·단일 계면 형성에너지·국부 확산경로 는 **아무리 정확해도** 완전지 셀의 용량유지·율특성·
> 수명에 **직접 연결되지 않는다.**"*

⇒ 원고 문장 초안: *"이 연구는 계면 반응의 **열역학 층위**를 다루며 소자 수준 성능으로의 외삽을 주장하지
않는다. 최근 리뷰가 지적하듯 [Wu 2026], 원자 수준 양과 소자 응답 사이의 간극은 아직 메워지지 않았다.
우리가 주장하는 것은 **도펀트 선택이 계면 분해 경로를 예측 가능하게 바꾼다**는 것이고, 그 예측은
**맞춘 매개변수 없이** 이루어진다."*

**10. 🟢 §H(우리가 못 하는 것)에 이 편이 주는 규모 기준**

| 우리 공백 | 리뷰가 준 기준 | 출처 |
|---|---|---|
| MLIP 검증 2단 (**VDOS**) | *"application-oriented validation"* 3단 사다리: 구조(RDF·격자·**EOS**) → 동역학/기계(**VDOS**·탄성) → 응용(MSD·D·Ea·상전이T) | §2.3 |
| 무질서 앙상블 규모 | **30 000 배열** 샘플 · Li₆PS₅Cl 최적창 **37.5–50 %** | [80] Chen *Chem. Mater.* 37, 591 (2025) |
| 비정질 셀 크기 | **>1000 원자** 여야 실험 Ea 재현, **125 원자면 부분결정화** | [106] Li *JCP* 147, 214106 (2017) |
| 계면 MD 규모 | 12 160 ~ 36 000 원자 · 2–10 ns (증류 NNP 는 **120 000 원자 · 10 ns · 1주**) | [131][133][146] |
| 입계 | 13 860 원자 · 135 Å, Li 축적 폭 **≈20 Å** | [94] Kim *Nano Energy* 124, 109436 (2024) |

⚠ **입계 항은 §J-19 [Ou26MS] 가 이미 판정했다** — µm 입도에서 GB 기여 **1 % 미만** ⇒ 우리 단결정 가정은 방어된다.
그리고 리뷰의 [128] 은 **그 편의 arXiv 판(2510.18630)** 이다 (우리는 게재판 *Nat. Commun.* 17, 8726 보유).

## K. 🧪 **수계 Zn 축 (신규, 2026-09-03)** — ⛔ 물성 4축과 *수치로* 섞지 않는다

> 출처: `talks/do2026_bml_alzib_preconditioning.md` — **Kyungrok Do, BML 주간 세미나 2026-09-02**
> (무음극 Zn–I₂, N/P≈1, Cu 집전체 pre-conditioning). **논문 아님 · 미출판 · 외부 인용 금지.**
>
> **왜 A/B/C/D 표에 안 넣는가**: 이온(**Zn²⁺ ≠ Li⁺**) · 전해질(**2 M ZnSO₄ 수용액 ≠ 고체 SE**) ·
> 전극(**집전체 위 금속 전착 ≠ 복합양극/SE 벌크**) · 측정량(**CE·CCD·OCV ≠ σ/Ea/ESW/E_VRH/gap**)이
> 전부 다르다. **σ·Ea·ESW·gap 겹침이 문자 그대로 0건**이다. 4축 표에 한 줄이라도 넣으면
> 우리 db 절대값과 발표 소환값이 같은 좌표계에 놓인다 — 그게 정확히 CLAUDE.md 가 금지한 것.

### K-1. 발표자 값 (⚠ 전부 **발표 소환값**. 우리 `db/properties/*` 와 같은 표에 놓지 말 것)

| 지표 | bare Cu | pre-conditioned Cu | 조건 |
|---|---|---|---|
| Aurbach 평균 CE | 77.75 % / 75.86 % | **98.14 % / 98.82 %** | 0.5 mAh 전착 + 0.1 mAh ×9 · (ZnSO₄ / +0.2 M ZnI₂) |
| Aurbach 평균 CE | 96.55 % / 95.66 % | 98.49 % / 98.63 % | 5 mAh 전착 + 1 mAh ×9 |
| CCD (10 mAh cm⁻²) | **4C** 단락(ZnSO₄) · **2C** 단락(+ZnI₂) | **10C 까지 안정** | 계단식 1C→10C |
| OCV plateau (부식) | ~10 min | **~3–4 h** | 0.1 mAh cm⁻² 전착 후 휴지 |
| 하프셀 수명 (5 mA cm⁻²·1 mAh cm⁻²) | 597 cyc(ZnSO₄) · 868 cyc(+ZnI₂) | 1584 cyc · **2700 cyc** | — |
| 풀셀 Cu‖AC | — | **1.48 mAh cm⁻², 600 cyc 75.0 %** (10 mA cm⁻²) · 1.13 mAh cm⁻², 400 cyc 89.9 % (20 mA cm⁻²) | 2 M ZnSO₄ + 0.2 M ZnI₂ |

### K-2. ✅ **우리 계산이 문헌(발표)을 *답한* 첫 지점 — C1 상 지문표**

> `db/properties/zn_cu_phase_fingerprint_2026_09_03.json` (2026-09-03, `tools/xrd/phase_fingerprint.py`,
> Cu Kα₁, **실험 문헌 격자상수** — DFT 이완값 아님)

발표자 자인 **G1**: *"The reflection near 43° cannot be unambiguously assigned to Zn owing to overlap with Cu"*
→ **우리 답: 그 판단이 맞다. 그리고 더 잘 찍어도 안 갈린다.**

| 우리 결과 | 값 |
|---|---|
| 42–44° 안의 반사 수 | **8개**, 폭 **1.469°** |
| Cu(111) ↔ Zn(101) 간격 | **0.097°** (43.318 vs 43.221) |
| 그 사이에 끼는 상 | **CuZn-β′(110) 43.282** — 슬 18 이 "suggest" 한 바로 그 합금 |
| **진단창 (Cu 반사 0개)** | **31–39°** — Zn(002) 36.29 · Cu₅Zn₈ 31.85/34.98/37.89 · CuZn₅(100) 37.94 · ZnO 31.77/34.42/36.26 · Cu₂O(111) 36.42 |
| ZHS | 43° 부근 **주선 없음** (기저면 2θ ≈ 8–11°) → 43° 논쟁의 후보가 아님 |
| CuI(220) | 42.208° = Cu(111) 에서 **1.11°** → 풀셀 CuI 귀속(슬 24)은 신뢰 가능 |

⇒ **실험 쪽 다음 액션은 "43° 를 더 잘"이 아니라 "GI-XRD 를 31–39° 창에"** 다.
⛔ **이 계산이 못 하는 것**: Rietveld 정량 아님 · 무작위 배향 가정(전착 Zn 은 002 texture) ·
어느 상이 *실제로* 생기는지 안 말함(속도론 없음) · Cu₅Zn₈ 는 위치 전용(강도 null) · ZHS 미계산.

### K-3. 남은 계산 후보 — **여기 쓰지 않는다**

C2(zincophilicity 서술자) · C3(HER ΔG_H\*) · C4(갈바닉 Φ) · C5(Zn²⁺ 용매화·Marcus λ, ORCA) ·
C6(Zn(002) Wulff) · C7(MD)와 각각의 **"못 하는 것"**, 착수 게이트 4개, 권장 순서는 전부
📄 **`kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md`** 에 있다. **중복 서술 금지.**
권장 순서에서 **C1 은 완료**, 다음은 **C2+C3 한 묶음**.

### K-4. ⚠ 이 축을 열 때의 우리 규율

- **UMA 는 수계 Zn 전해질에서 검증 영역 밖**이다 (검증 영역 = LPSCl 계열; Li₃N 편향 선례 2026-06).
  **MLIP 단독 판정 금지** — 스크리닝 → DFT 앵커.
- **estimand 카드 먼저.** "합금 위 Zn 결합에너지"는 *조성 × 종단면 × 피복률* 을 선언하기 전엔
  **정의되지 않은 scalar** (SDCP 8회 반려의 그 함정).
- **금속 smearing(ISMEAR/SIGMA·degauss)을 state-selection policy 로 선언**하고 결과 보기 전에 게이트로 박는다.
- 인용문헌 5편(**NML 2022 14:208 · EES 2024 17:7372 · Nat. Commun. 2026 17:7363 ·
  AFM 2026 36:e23442 · EES 2025 18:10180**) 중 **AFM(Zhu) 만 인입 중**, 나머지 4편은 litdb 미보유.
  특히 **EES 2024 17:7372 는 C5 의 비교 대상 원전**이라 확보 전엔 λ 를 계산해도 대조할 곳이 없다.


### K-5. 📄 논문 축 — **[Zhu26Zn]** 이 들어왔다 (2026-09-03, 논문 에이전트)

> `papers/zhu2026_zhs_precoverage_quasi_anode_free_zn.md` — R. Zhu, T. Yabu, C. Yang, S. Yao, H. Yang,
> A. Nasu, M. Matsui, **H. Kobayashi\*** (홋카이도대/상하이교통대), "Pre-Coverage of Side Reaction Sites
> Enables Quasi-Anode-Free Rechargeable Aqueous Zinc Batteries", ***Adv. Funct. Mater.* 2026, 36, e23442**
> (DOI 10.1002/adfm.202523442, online 2025-11-24).
> ⇒ **§K-4 의 "AFM(Zhu) 만 인입 중" 이 해소됐다.** 나머지 4편은 여전히 미보유.
> 이 논문은 **덱 슬 6(G2)의 원출처**이자 **정본**이다 — 덱과 어긋나면 논문이 이긴다.
> **두 번째 수계 Zn digest**: `papers/cho2026_eipc_zn_anode_azib.md` (코팅막 축, [Cho26Zn]).
> **세 번째**: `papers/wu2026_dilute_electrolyte_zn_calendar_aging.md` (**calendar aging 축**, [Wu26Zn]) → **§K-10~K-12**.
> ⛔ 세 편은 전해질이 전부 다르다 — CE 를 같은 표에 놓지 않는다.

**논문값 (⚠ 발표 소환값과 섞지 말 것 — §K-1 표와 *다른 계*다: 1 M ZnSO₄, 요오드 없음, 탄소 코팅 Cu)**

| 지표 | Cu | CuGr | CuStr | **CuGrStr** |
|---|---|---|---|---|
| 평균 CE (10 mA cm⁻²·1 mAh cm⁻², 2000 cyc) | 99.86 % | 99.88 % | 99.89 % | **99.94 %** |
| 4 mAh cm⁻² | 단락 | 단락 | — | **99.74 %** (150 cyc) |
| GC H₂ 부피 % (`Fig. S13`, figure-read) | 3.31 | 4.29 | **0.55** | **0.28** |

무음극 CE 문턱(`Fig. 1a`): 200 cyc 80 % 유지 → **>99.9 %** · 500 cyc → **>99.95 %**.
QAF 셀 **≈520 Wh kg⁻¹**(⚠ 본문 표현은 *theoretical*) · 57 cyc 92 % 유지, 감쇠 원인은 **ZMO 양극**.

### K-6. ★★ G2 판정 — **"Cu 표면합금"은 논문에서 *측정된 적이 없다***

덱 슬 6 의 *"For Cu substrate, formation of surface alloy layer exerted a greater influence than ZHS …
**not systematically investigated**"* 를 원문에서 확인한 결과:

- 본문 전체에서 **"alloy" 는 2회**뿐이고 **둘 다 조건법**이다 —
  *"only during the early stage **might** the current refer to a UPD or a surface alloying process"* ·
  *"The improvement in CuStr **likely** arises not from ZHS passivation but from the formation of a
  surface alloy layer …[15]"* ([15] = Hao 외, *AFM* **2020**, 30, 2001263 — 우리 litdb 미보유).
- **합금에 대한 자기 측정 0건**: Cu 쪽 XRD 없음(`Fig. 2h` 는 CuGr 전용) · Cu 2p 화학상태 분해 없음 ·
  **Cu 2p 깊이프로파일 없음**(`Fig. S22` 는 O 1s·Zn 2p 만 4시료) · CuStr 단면 EDS 없음(`Fig. S7` 단면은
  CuGrStr 전용) · UPD 정량 없음 · **DFT 에 Cu 표면 0건**.
- 논문의 Cu 논리는 실제로 **기하 논증**이다(`Fig. S8a`): 평판 Cu 는 ZHS 가 표면을 통째로 덮어 **해롭고**,
  "약한 3D" 탄소는 ZHS 가 생겨도 Zn 활성자리가 남는다. 합금은 *"그래도 CuStr 가 조금 좋아지니
  원인이 무언가 있어야 한다"* 는 **소거법의 결론**으로만 등장한다.

> ⚠ **덱 표현 정정**: 논문은 *"Cu 에서 합금이 ZHS 보다 크다"* 를 **잰 적이 없다**. 논문이 말한 것은
> **"탄소에서는 ZHS 가 유익, Cu 에서는 ZHS 가 유해 → 남은 개선분은 합금 때문일 것"** 이다. 부호가 다르다.

⇒ **§K-3 의 권장 다음 단계(C2+C3 한 묶음)가 문헌 공백을 그대로 겨냥한다는 것이 확인됐다.**

### K-7. C1 ↔ 논문 대조 (§K-2 의 보강)

| 항목 | [Zhu26Zn] | 우리 C1 |
|---|---|---|
| ZHS | **PDF#00-039-0690** 으로 동정 (`Fig. 2h`, CuGr 기판). ⚠ **2θ·격자상수 본문 미기재** | ⛔ 미계산(수화수 n 미정). 기저면 2θ ≈ 8–11° |
| 43° 부근 | ⛔ **없음** — Cu/CuStr 쪽 회절 데이터 자체가 0건 | 8상 1.469° 폭 (§K-2) |

**★ 두 줄 결론**
1. **우리 C1 이 유일하게 못 푼 상(ZHS)을 이 논문이 PDF 카드로 특정했다** — 그 카드의 **수화수 n·격자상수**를
   확보하면 C1 의 ZHS 항이 닫힌다. (논문 자체에는 2θ 도 격자상수도 없다.)
2. **ZHS 문제와 43° 문제는 다른 2θ 창의 문제다.** ZHS = 저각(8–25°) · 합금 = **31–39° 진단창**.
   섞어 말하면 틀린다 — 협업 상대에게 줄 실험 처방도 그래서 둘로 갈린다.

### K-8. C3(ΔG_H\*) ↔ 논문 대조 — **유일하게 직접 겹치는 축**

논문의 계산 집합(`Fig. S1`, `Fig. S2`) = **ZHS · 금속 Zn · 완전 그래핀 · 결함 그래핀** 4종.
**Cu · CuZn · Cu₅Zn₈ · CuZn₅ · CuI 는 하나도 없다** ⇒ 우리 C2/C3 이 채울 자리가 그대로 남아 있다.

| 계 | 논문 ΔG (figure-read `Fig. S2`) | 우리 C3 계획 |
|---|---|---|
| Gr(5×5)-H | **+2.618 eV** | 계획 없음 |
| Gr(5×5)(D)-H | **−0.216 eV** | 계획 없음 |
| 금속 Zn · ZHS | 값은 `Fig. 1c`(본문 그림, **우리가 못 본 그림**)에만 — **인용 불가** | Zn(0001) ✅ |
| **Cu · Cu–Zn 합금 · CuI** | ⛔ **없음** | ✅ **우리만** |

**⛔ 절대값 이식 금지 — 이유가 강하다**: 이 논문은 **계산 방법을 어디에도 적지 않았다.**
code · 범함수 · vdW · 유사퍼텐셜 · k-mesh · cutoff · 슬랩두께/진공 · 스핀 · 용매모델 ·
**ΔG 의 ZPE/TΔS 보정 여부와 H 기준(½H₂ vs H⁺+e⁻)** 이 전부 미기재이고, 본문 전문에
`DFT`·`VASP`·`first-principles`·`PBE`·`k-point`·`plane-wave`·`pseudopotential`·`force field` 가 **0건**이다
(`functional` 은 "functional groups", `cut-off` 는 전압 컷오프로만 나온다 — 계산 의미의 용례 0건)
(MD 도 마찬가지 — code·force field·물 모델·앙상블·길이 전부 미기재, `Fig. S9c` RDF 는 **원자쌍 라벨조차 없다**).
⇒ 우리 ΔG_H\* 를 2.618 / −0.216 eV **옆에 나란히 그리면 CLAUDE.md "방법 명시 없이 이식 금지" 위반**이다.
**살아남는 것은 정성 순서뿐**: 결함 그래핀 > Zn > 완전 그래핀 ≈ ZHS.

**✅ 대신 쓸 수 있는 실험 앵커** (C3 의 1차 게이트 후보): GC H₂ %(§K-5 표) · HER LSV(포화 K₂SO₄, 4 mV s⁻¹,
`Fig. 3b`) · 정전위 0 V vs Zn 20 h 누적전하(`Fig. 3c`).
⚠ **면적 규약 경고**: GC 는 **셀 총량**, ΔG_H\* 는 **자리당 열역학**이다. 게다가 논문 자신이
본문(기하면적 LSV)에서는 *"그래핀 코팅이 bare Cu 보다 HER 이 적다"* 고 쓰는데 `Fig. S13`(GC 총량)은
**CuGr 4.29 % > Cu 3.31 %** 로 **반대**다 — 그 화해(GNP BET 25.239 m² g⁻¹)를 논문이 하지 않았다.
⇒ 우리 순위와 대조할 땐 **어느 규약인지 반드시 명명**할 것.

### K-9. 🔧 [Zhu26Zn] 에서 **방법으로만** 가져오는 것 + ⛔ 금지 목록

| 항목 | 논문 | 우리 활용 |
|---|---|---|
| **operando XRD 계단 정전위** | 정전류가 아니라 **25/50 mV 스텝 · 각 전위 1 h 유지 · 뒤 30 min 수집** | ⭕ 협업 상대의 **GI-XRD 설계(G1)** 에 제안 가능한 형식 |
| **quasi-in-situ SEM/XPS 위치추적** | 반응을 **1 mm 디스크로 국한** + 스테이지 위치기억 재촬영 (operando 아님, 저자 명시) | ⭕ 같은 자리 추적 설계 |
| **DRT 로 R_ct1·R_ct2 분리** | `Fig. S12`·`Fig. S16` | `kim2025_impedance_decoupling_tlm_assb` 와 동일 계보 |

⛔ **인용 금지**
- 논문의 CE·H₂ %·에너지밀도·ΔG 를 `our_dft_baseline.md` / `db/properties/` 황화물 값과 **같은 표**에.
- ΔG **2.618 / −0.216 eV** 를 우리 ΔG_H\* 와 같은 축에 (방법 미상 → 축이 다르다).
- `Fig. S12` 의 **14.05 / 20.65 / 18.70 / 17.25** — 인쇄 단위가 **J mol⁻¹ K⁻¹(엔트로피 차원)** 인데
  Arrhenius 기울기를 되짚으면 **kJ mol⁻¹** 규모다. **순서만** 쓴다.
- **"520 Wh kg⁻¹"** 를 실측 셀 에너지밀도로 (본문은 *theoretical*).
- **§K-1 의 발표 소환값과 §K-5 의 논문값을 같은 표에** — 전해질(2 M ZnSO₄+ZnI₂ vs 1 M ZnSO₄)·기판·
  프로토콜이 전부 다르다. ⛔ 방향은 **논문 → talk** 단방향.

### K-10. 📄 세 번째 편 — **[Wu26Zn]** calendar aging 축이 들어왔다 (2026-09-08, 논문 에이전트)

> `papers/wu2026_dilute_electrolyte_zn_calendar_aging.md` — H. Wu, B. Liu, D. Zhao (공동1저자 3인),
> **D. Cheng**(DFT), … **P. Sautet**, **Y. Li\*** (UCLA), "Dilute electrolytes for suppressing metal anode
> corrosion during calendar aging and cycling in aqueous zinc batteries",
> ***Nat. Commun.* (2026), Article in Press**, DOI `10.1038/s41467-026-75100-x`.
> 🎤 이 논문이 **`talks/do2026_bml_alzib_preconditioning.md` §11.3(b)** 의 결론
> — *"우리가 계산할 양은 **calendar 축**에 걸어야 한다"* — **의 문헌 앵커**다. 덱은 citable=no, 논문이 정본.

**논문값** (⚠ **§K-1(덱)·§K-5([Zhu26Zn]) 와 같은 표에 놓지 말 것** — 전해질이 셋 다 다르다:
2 M ZnSO₄+ZnI₂ / 1 M ZnSO₄ / **0.1 M ZnSO₄ + 0.5 M Li₂SO₄ + 5 vol% DMF in D₂O**)

| 지표 | 1 M ZnSO₄ 대조 | **1Z5L (본 논문)** | 조건 |
|---|---|---|---|
| 24 h calendar 유지 | 64.4 % | **98.4 %** | 1 mAh cm⁻²·1 mA cm⁻²·25 °C·graphite |
| 7 d 유지 | (2 M/Cu) 3 % | **84.9 %** | ⚠ 대조만 **Cu 기판** — §K-11 |
| 기판별 24 h | 72.0 / 26.9 / 72.3 % | **98.0 / 97.2 / 93.7 %** | graphite / Ti foil / Cu foam |
| 온도별 24 h | 79.9 / 72.0 / 40.6 % | **98.8 / 98.0 / 96.1 %** | 4 / 25 / 45 °C |
| 하프셀 CE | 23 cyc 에서 급락 | **99.7 %** (220 cyc) | 1 mA/1 mAh cm⁻² |
| 대칭셀 | <100 h | **>1,500 h** | 〃 |
| Zn‖LMO 4 C | — | **3,300 cyc · 평균 CE 99.8 %** | ⚠ 궤적 비단조 — §K-11 |
| pH (농도) | 3 M **3.5** · 1 M 5.3 · 0.3 M 6.02 | **0.1 M 6.5** · 0.01 M 7.04 | `Fig. 2c` Source Data |
| **TGC 손실 분해** | — | 연속사이클 **Zn⁰ 0.50 / 부식 0.003 %**<br>24 h 정지 후 **Zn⁰ 0.65 / 부식 0.85 %** | ★ 이 논문 최고 데이터 |

> ★ **TGC 행이 이 축에서 제일 중요하다.** *"사이클 손실 = 고립 Zn⁰, calendar 손실 = 화학부식 Zn²⁺"* 라는
> **기구 분리를 실험이 직접 쟀다.** ⇒ 우리 **C3(HER)·C4(갈바닉)의 검증 게이트는 사이클 CE 가 아니라
> 정지 상태 부식률**(j_corr · OCV plateau · TGC 부식분율)에 걸어야 한다는 것이 문헌으로 확정됐다.

### K-11. 🔴 **[Wu26Zn] 계산 층위 판정 — "CG-MD" 가 아니다** + 우리 축 매핑

**MD 가 0건이다.** CG-MD·all-atom MD·AIMD·MLIP·continuum 전부 없고 **전량 0 K 정적 DFT**다.

| 층위 | 이 논문 |
|---|---|
| VASP · **PBE + D3** · PAW · **400 eV** · **4×4×1 Γ** | ✅ |
| **Zn(002) 3층 (4×4) = 48 Zn**, 아래 1층 고정 / 위 2층+흡착종 이완 | ✅ |
| 명시적 물 **2층**(분자 개수 미기재, figure-read ≈ 20) + Zn 이온 1개(**최적화 결과 CN = 4**) | ✅ |
| **VASPsol** 선형 PB (ε 78.4, Debye **3.0 Å = 1 M**) | ✅ |
| **EChO 정전위(surface charging) −0.8 V vs SHE** — 이완·TS 둘 다 | ✅ **이 논문의 방법론적 강점** |
| **CI-NEB → dimer** (0.05 eV/Å), 경로당 **9점**(RC 0–8) | ✅ |
| 앙상블·온도·시간·시드 | ❌ **전부 해당 없음. 경로당 배열 1개, 오차막대 없음** |
| **RDF · 배위수 · MSD · D · 용매화 껍질 조성** | ❌ **0건** |

계산값: Volmer 장벽 **pure H₂O 1.207 / Zn 1st shell 0.601 / Zn 2nd shell 0.700 eV**,
ΔE **0.622 / 0.167 / 0.165 eV** (`Fig. 2a` Source Data 원값) · **−ICOHP(O–H) 3.94 → 2.30 eV** (`Fig. S1c,d` 인쇄값).

**우리 축 매핑** (스코핑 카드 C1–C7 기준):

| 우리 후보 | [Wu26Zn] 와의 관계 |
|---|---|
| **C3 (HER ΔG_H\*)** | ★ **업그레이드 목표점.** 우리 C3 카드가 자인한 한계 4개 중 **3개(속도론 없음·EDL 전기장 없음·명시적 물 없음)** 를 이 방식이 정면으로 해소한다. 단 §K-12 대로 **지금 우리 장비로는 못 돌린다** |
| **C4 (갈바닉 Φ)** | ★ 우리 카드가 *"암시적 용매 판을 따로 세워야 한다"* 고만 적어 둔 자리에 **구체 사양**(ε 78.4, Debye 3.0 Å, surface charging)을 준다 |
| **C5 (Zn²⁺ 용매화 / Marcus λ)** | ⭕ 상보. 우리는 ORCA 클러스터+CPCM, 이 논문은 **표면 위 −ICOHP(O–H)**. **같은 질문의 두 번째 관측창** |
| **C7 (MD / EDL 조성)** | ❌ 도움 안 됨 — 이 논문에 MD 가 없다. 오히려 *"MD 없이 정적 DFT 만으로 이만큼 주장했다"* 의 사례이자 그 **위험 사례**(§K-12 비판 1) |
| C1 (상 지문) | ⭕ `Table S3` 의 **ZnO d-spacing 7면**(측정 ± 불확도 vs 표준)이 우리 지문표 ZnO 행과 직접 대조 가능 |
| C2 · C6 | 겹침 **0** |

### K-12. 🔧 [Wu26Zn] 에서 **방법으로만** 가져오는 것 + ⛔ 금지 목록

> ⚠ 이 블록은 **물성 4축 표가 아니라 방법 원전 블록**이다. 이 논문은 σ·Ea·ESW·E_VRH·gap 을
> **하나도 계산하지 않았다** — 4축에 넣을 행이 없다.

| 항목 | 논문 | 우리 활용 |
|---|---|---|
| **정전위 슬랩(surface charging)** | EChO + VASPsol, −0.8 V vs SHE | ⭕ **C3/C4 의 최종 사양.** ⚠ 우리는 QE → Environ 으로 옮기면 **다른 방법**이 된다(값 대조 금지) |
| **−ICOHP(O–H) 를 물 반응성 서술자로** | 3.94 → 2.30 eV | ⭕ 우리 LOBSTER 파이프라인(`lobster_nscf`)에 **결합만 바꿔** 재현 가능. 축소판(2층 슬랩+물 1층)은 우리 GPU 로 돌아간다 |
| **조건 스윕 설계**(`Fig. 4c–e`) | 기판 3 × 전착용량 3 × 온도 3, 각 3–5 반복 | ⭕ 협업 상대(BML)에게 줄 **calendar 실험 처방 골격** |
| **하이브리드 프로토콜**(`Fig. 4f,g`) | 5 cyc 마다 2 h 휴지, 100 % SOC | ⭕ calendar 를 **셀 수준에서** 재는 유일한 형식 |
| **TGC 3분할**(가역/Zn⁰/부식 Zn²⁺) | HCl 적정 → H₂ GC-MS, m/z 5 | ⭕ C3/C4 게이트의 **정량 대상** |
| **첨가제 선정 지도**(`Fig. S6b`, DN–ε) | 비양성자성 · DN ≳16 · ε ≳27 | ⭕ 우리 ZnI₂ 계 첨가제 논의의 **좌표축 통일** |

⛔ **인용 금지**
- 이 논문의 **CE·용량유지·j_corr·pH** 를 `our_dft_baseline.md` / `db/properties/` **황화물 값과 같은 표**에.
- 이 논문의 CE 를 **§K-1(덱, citable=no)·§K-5([Zhu26Zn]) 와 같은 표**에 — 전해질이 셋 다 다르다.
- **−ICOHP 3.94 / 2.30 eV** 를 우리 **ICOHP(Li–Cl) −1.86 / −2.10** 옆에 —
  ⓐ 부호 규약 반대(우리 ICOHP 음수 vs 저들 −ICOHP 양수) ⓑ 결합종 다름(O–H 공유 vs Li–Cl 이온)
  ⓒ **COHP 코드 미기재**(LOBSTER 인지 불명) ⓓ 적분 하한 창 미기재. **정성 방향만.**
- **Volmer 장벽 절대값**(1.207/0.601/0.700 eV) — **단일 배열·0 K·ΔE(ZPE 없음)**. **차이(−0.6 eV)만** 쓴다.
- **`Table S1` ΔG(−0.724 / −0.543 kcal/mol)** 을 "이 논문 DFT 결과" 로 — 캡션 각주가 **인용(ref 7)** 을 가리킨다.
- **"KIE 를 DFT 로 확인"** — **O–D 계산 0건.** KIE 는 순수 ZPE 효과라 ΔE 만으로는 원리상 안 나온다.
- **"용매화 껍질 조성"** — 측정된 적 없음(RDF·배위수 0건). 모델 **CN=4** vs 도식 **CN=6**.
- **"저비용 전해질"** — 용매 **전량이 D₂O(99.96 % D)** 인데 비용 분석이 논문에 없다.

⚠ **우리가 Source Data 로 직접 잡은 불일치 3건** (그림 판독 추정 아님):
1. `Fig. 2c` 에 **4 M 점(24 h 62.8 ± 4.8 %)이 빠져 있다** — Source Data 에는 있고, 3 M(52.2 ± 10.7 %)보다 **높아** 단조성을 깬다. 언급 없음.
2. `Fig. 4b` 7일 곡선은 **1Z5L = graphite / 대조 = Cu** 로 **기판이 다르다**(Source Data 열 이름에만 표기, 캡션에 없음). 같은 논문 `Fig. 4c` 가 기판만으로 72.0 % ↔ 26.9 % 를 보여준다 ⇒ **비교 불공정**.
3. `Fig. 5e` "3,300 cyc 80 % 유지" 는 **비단조 궤적**을 감춘다: 방전용량 **64.1(cyc 1) → 68.4(cyc 301) → 42.4(cyc 1001) → 47.5 mAh g⁻¹(cyc 3517)**. 최종/초기 = **74 %**.

🖥 **재현 가능성 판정**: ⛔ **우리 장비로 불가.** VASPsol·EChO 부재(우리는 QE) + 원자 ~110/가전자 ~740 ·
기약 k ~8–16 · 정전위 외부루프 × NEB 7이미지 ⇒ gabia A6000 **단일 GPU 수 개월**(그동안 UMA 동시실행 금지).
가능한 축소판은 ① CHE ΔG_H\*(= 현행 C3) ② 2층 슬랩+물 1층 정적 COHP(O–H) ③ ORCA λ(기존 C5) 셋뿐이고,
**셋 다 이 논문과 다른 보고량**이다. 착수하려면 **보고량 카드 + 게이트(양성 대조: 순수 물 장벽 재현)** 를 먼저.

---

## L. 🔴 **자기감사 축 — 우리 CEJ 투고본** (2026-09-07 신설) — ⛔ "문헌 vs 우리" 가 아니다

> **[Ahn26CEJ]** = `papers/ahn2026_cej_agno3_pvp_li3n_anodefree.md`
> D. Kim/J. Kang/T.Y. Lee/H.R. Shin(공동1저자 3인), **Yonghoon An (DFT 담당)**, 교신 Jong-Won Lee (한양대)
> "Electrochemical precursor conversion for coupled control of Li nucleation and transport in
> anode-free all-solid-state batteries", **Chem. Eng. J. 투고본 (DOI 없음, 2026-09-07 업로드)**

### L-0. 이 축을 여는 규율 (다른 축과 다르다)

이건 **외부 문헌이 아니라 우리 원고**다. 따라서:

- ⛔ **"소환값" 규율이 적용되지 않는다.** Fig. 5c–e / Table S2 의 DFT 수치는 `db/properties/diffusion.json`·
  `li3n_barrier_origin.csv`·`li3n_barrier_fig_origin.csv` 와 **같은 계보**다 — 남의 값이 아니다.
- ⛔ **물성 4축(A 이온전도 / B 산화안정 / C 기계 / D 전자구조) 표에 넣지 않는다.**
  이 논문은 σ·ESW·탄성·밴드갭을 **하나도 계산하지 않는다**. 넣을 칸이 없다.
- ✅ 대신 여기서 하는 일은 **감사**다: *원고가 주장하는 수치가 우리 정본과 같은가, 그리고
  원고가 기술한 방법이 그 수치를 실제로 낼 수 있는가.*
- ⛔ **방향은 원고 → db 가 아니다.** 불일치가 나오면 **원고를 고친다**(우리 db 가 정본).
  단 L-2 의 db 내부 분열(0.287 vs 0.28968)은 db 쪽을 정리해야 하는 예외다.

### L-1. ✅ 값 대조 — 원고 vs 우리 정본 (전부 일치)

| 원고 주장 | 값 | 어디 | 우리 정본 | 판정 |
|---|---|---|---|---|
| Li₃N(001) Li adatom 확산장벽 | **0.118 eV** | `Fig. 5e` · `Table S2` · Highlights | `diffusion.json` `li3n_001_p0_2point_constrained_dft_2026-07-15` = **0.1182**; `li3n_barrier_origin.csv` `DFTpoint_eV` max **0.11820** | ✅ 일치 |
| E_ads 흡착최소 | **−2.988 eV** | `Fig. 5c` | `li3n_barrier_fig_origin.csv` `onN_min4` **−2.9877** (converged) | ✅ 일치 |
| E_ads 안장영역 | **−2.870 eV** | `Fig. 5c` | `li3n_barrier_fig_origin.csv` `bridge_saddle3` **−2.8695** (converged) | ✅ 일치 |
| 감소율 | **≈59 %** (2.46×) | Results | 방어카드 A-7 "0.118 eV / ≈59 %, 비율 2.46×" | ✅ 일치 (확정결정 반영) |
| 진공 | **≈15.7 Å** | `Table S2` | 방어카드 A-2 "→ 15.7 Å" | ✅ 일치 (수정 반영) |
| 자리 이름 미사용 (`Minimum`/`Saddle`) | — | `Fig. 5c,d` | 방어카드 C-2·C4·C7 "자리 명명 금지" | ✅ 일치 (노출 차단됨) |
| LiC₆(0001) 장벽 | **0.290 eV** | `Fig. 5e` · `Table S2` | `li3n_barrier_origin.csv` `LiC6_DFT_eV` max **0.28968** | ✅ 값은 일치 / ⚠ 계보는 L-2 |

**⇒ 숫자는 하나도 안 틀렸다.** 문제는 전부 **방법 귀속과 그림 표현**에 있다.

### L-2. 🔴 P0 — 방법 귀속 2건 (여기가 이 감사의 전부다)

| # | 무엇 | 근거 | 조치 |
|---|---|---|---|
| **P0-1** | **`Fig. 5d` 가 Li₃N 을 실선 연속 MEP 로 그리고, 캡션에서 "*Symbols in (d) denote DFT-calculated configurations and the lines are guides to the eye*" 가 빠졌다.** 계산한 Li₃N 점은 **2개**뿐이고 곡선은 *폐기된* mirrored-spline NEB 형상 × 진폭재조정(`Li3N_guide_eV` = `li3n_neb_fit_optimal.csv` × 0.1182/0.10201, 편차 5e-7) | `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md` (status **확정**) 이 캡션 문장과 **"실선 금지·점선"** 을 못 박았다 | 캡션 두 문장 복원 + Li₃N 곡선 **점선화**. LiC₆ 는 실측 7점이니 **심볼을 찍어** 캡션과 짝 맞추기 |
| **P0-2** | **Methods §4.6 이 LiC₆ 를 "CI-NEB + UMA-oc20" 로만 기술하고 QE 단일점 단계를 빠뜨렸다.** 그 경로 **단독** 우리 값은 **0.241 eV** 이지 0.290 이 아니다. 반면 `Table S2` 는 QE 파라미터 7행을 **gridSpan=2 로 두 열 병합**(원본 XML 실측)해 "LiC₆ 도 QE" 라고 말한다 → **표와 Methods 가 서로 다른 말** | `kb/methodology/li_adatom_neb_protocol.md` §OUTCOME: UMA-oc20 CI-NEB **0.241** / DFT-SCF on UMA 기하 **0.287**. 방어카드 A-4 는 "LiC₆(CI-NEB **+ DFT 단일점**)" 를 요구했는데 **뒷절반 미반영** | §4.6 에 한 문장 추가: *"Single-point DFT calculations were then performed on the resulting NEB image geometries using the same plane-wave settings as for Li₃N (Table S2)…"* |

**노출 지점**: Highlights 가 "*Li₃N lowers the Li-adatom diffusion barrier **from 0.290 to 0.118 eV**.*"
라고 **아무 단서 없이** 쓴다. §4.6 만 읽은 리뷰어에겐 **MLIP 값 − DFT 값**으로 보인다.
방어카드가 준비한 반박 문구("MLIP 기하 위 DFT 단일점 → TS 가 매끄러워짐 → 이 비율은 **보수적 하한**")는
옳지만 **원고 어디에도 없다**. 문헌 정합값 **0.133** 도 원고·SI 전문에서 **0회**.

### L-3. 🟠 P1 — `0.290` 의 계보 + db 내부 분열

`li3n_barrier_origin.csv` 직접 검산:

| 항목 | 값 |
|---|---|
| 스플라인 최대 | **0.28968 eV @ xi = 0.4100** ← 원고의 0.290 |
| 7 이미지 **실계산점** | 0.0000 / 0.1684 / 0.2816 / **0.2866** / 0.2762 / 0.1594 / **−0.0222** |
| 실제 최고 계산점 | **img3 = 0.2866 eV** |
| `diffusion.json` 헤드라인 | **0.287** |

⇒ ① 보고값 0.290 은 **계산된 이미지가 아니라 이미지 사이 스플라인의 오버슛**이다.
⇒ ② **우리 db 안에서 값이 갈라져 있다**(0.287 vs 0.28968) — 이건 **db 쪽을 정리해야 하는 예외**다.

영향은 작다(58.8 % vs 59.3 % — 결론 불변). **그러나 P0-1 을 고쳐 "심볼 = 계산된 배치" 라고 캡션에
쓰는 순간, 막대(0.290)와 심볼 최대(0.2866)가 그림 안에서 모순**이 된다.
**⇒ P0-1 과 P1 은 반드시 같이 고친다.** 권장: **0.287 로 통일**(계산점 기반이라 방어가 쉽다).

### L-4. ✅ 금지규율 전수검사 — **위반 0건**

| 규율 | 원고 해당 문장 | 판정 |
|---|---|---|
| **⛔ UMA 를 Li₃N 에 사용 금지** (2026-06 결정론적 편향) ← 최우선 확인 | **없다.** §4.6 은 Li₃N 을 **QE 두 점 구속이완**으로 명시. UMA-oc20 은 **LiC₆ 에만** | ✅ **통과**. 폐기값 **0.054 / 0.237 은 원고에 0회** |
| ⛔ MD σ 절대값 인용 금지 · 비율도 멀티시드만 | MD/MSD/Nernst–Einstein/σ 계산이 **아예 없음** (`mS cm⁻¹`·`molecular dynamics` 전문검색 0회) | ✅ 해당 없음 |
| ⛔ `b2o3_vs_lpscl16_conductivity.csv` FORBIDDEN 문구 (`statistically equivalent transport` / `conductivity preserved` / `equivalent sigma` / 순위·기전) | 전문검색 **0회** | ✅ 해당 없음 |
| ⛔ b2o3 UMA-MD 축 전체 인용 불가 (2026-08-25, 0.222 eV 포함) | 전문검색 **0회** | ✅ 해당 없음 |
| ⛔ Band gap = fixed-occupations nscf VBM/CBM 만 (DOS-threshold 금지) | 밴드갭·DOS 계산 **없음** | ✅ 해당 없음 |
| BVSE 정량·순위는 원본 주기셀만 | BVSE 없음 | ✅ 해당 없음 |

> **요점**: 위험은 **"금지값을 인용했다"가 아니라 "방법 귀속이 불완전하다"** 에 있다.
> 2026-09-07 Codex BH P0-1 이 kb 카드에서 잡아낸 종류의 위반(FORBIDDEN 문구 재현)은 **이 원고엔 없다.**

### L-5. 🔧 방법 원전으로만 가져오는 것 (물성값 없음 → 4축 표에 안 넣는다)

| 항목 | 원고 | 우리 활용 |
|---|---|---|
| **재료–방법 궁합 규칙** | Li₃N = 구속이완(NEB 실패) / LiC₆ = CI-NEB | 새 SEI 표면(Li₂O·LiF·Li₂CO₃) 칠 때 **먼저** `kb/methodology/li_adatom_neb_protocol.md` 표 보고 방법 선택 |
| **DRT 3-피크 분해** (R_SE / R_interface / R_CT,Li–Ag) | `Fig. 6d`, Ciucci–Chen 베이지안 [44] | 우리 LPSCl 반쪽셀에서 반원이 겹칠 때 계면 vs 전하전달 분리 — 아직 우리가 안 쓰는 도구 |
| **ΔE_t = E₀⁺ − E_τ** (펄스내 분극) | `Fig. 6b`, 정의 `Fig. S9` | GITT 펄스에서 준평형 말고 **전이 분극**만 뽑는 깔끔한 정의 |
| **압력–온도 크리프 지도** | `Fig. 3e`, 10–30 MPa × 30–60 °C | **우리 스택압 규율 20 MPa 와 같은 창** → 우리 셀에서 크리프 지배 여부를 바로 읽음 |
| **operando 압력 자체검증** | `Fig. 7a` 240 kg / ⌀13 mm = **17.7 MPa** vs 본문 20 MPa | 셀 압력 보고 시 하중↔압력 환산을 도식에 같이 두는 관례 |

⛔ **인용 금지 / 주의**
- **`Fig. 3d` 의 j_creep,eq (0.39/0.10/0.08 mA cm⁻²) 를 재현값으로 쓰지 말 것** — Table S1 값으로
  Eq. (2) 를 풀면 Coble 지배(NH 대비 ~2.4×10³)라 10 nm/100 nm 가 **2.0×** 여야 하는데 그림은 **4.8×** 다.
  차이는 본문이 **크리프율→전류밀도 변환식을 안 준** 데서 온다 ⇒ **논문만으로 재현 불가**.
- **`Fig. 4` 의 EDS Ag 맵을 8 nm vs 53 nm 도메인 증거로 쓰지 말 것** — SEM-EDS 상호작용 부피(~µm)가
  그 스케일을 못 가른다. 그 그림이 보여 주는 건 **µm 스케일 균일성**뿐.
- **CCD "2.0 mA cm⁻²" 를 임계값으로 쓰지 말 것** — 두 온도 모두 그 값에서 **시험이 종료**된다 → **≥2.0**.
- 이 원고의 실험값(η_nuc·ΔP·용량유지율)을 `db/properties/` 계산값과 **같은 표에** 놓지 말 것.

### L-6. 미해소 (리비전 대비 — kb 에서 그대로 살아 있는 것)

| kb 항목 | 내용 | 상태 |
|---|---|---|
| **C2** 슬랩 두께 수렴 | 우리 4층(135+1) vs 문헌 6층. **미실행** | 🟠 가장 약한 지점 |
| **C3** 전역 최소 | 4층 슬랩에 min4 보다 **0.085 eV 낮은 2N-bridge pocket** → 엄밀 escape barrier 는 **0.2035 eV** | 🟠 C2 의 6층 테스트가 동시에 결판 |
| **C6** 안장점 정체 | 계산된 TS 가 최근접 hop(2.107 Å) 직선 위 **xi = 1.20** — 그 hop 의 안장(N–N 다리)은 **계산된 적 없다**. 계산하면 0.118 보다 **낮아질 수 있다**(= 주장이 강해진다) | 🟠 서술은 "saddle-region" 이라 방어 범위 안 |
| **Gap 1** | **6층 243원자 2점 테스트** — C2·C3 를 한 번에 닫는 유일한 실험 | ⬜ 미실행. 리비전까지 시간 있으면 지금 걸어야 함 |
| 등록부 | 0.118 / 0.287 이 `db/properties/canonical_registry.json` **42 entries 안에 없다** | ⬜ 투고본 headline 수치는 등록 대상 (CLAUDE.md 마감규율) |

---

## 🗨️ Q&A 로그
> 슬라이드·결과를 보며 나온 질문/답 누적. "Q&A 작성해줘" 트리거.

### Q1 · 2026-06-23 · LPSCl vs LPSCl1.6 산화안정성 누가 더 좋나? "우리 동일"과 문헌이 다르면 이유? (slide 27 ESW)
**한 줄 답**: 단일 승자 없음 — **축을 명명**해야 함. 우리 "동일"은 intrinsic onset(B①) 한정 정답, 문헌의 "다름"은 우리 ESW가 안 보는 다른 축(B②③④).
- 우리 grand-potential ESW = **intrinsic 0-pressure onset**. 첫 산화 S²⁻→S₂²⁻(황)는 **comp1·modelc 두 무도핑 조성이 공유** → 그 둘 사이에서 동일. [GG] K_eff=0이 검증. ⛔ 이걸 "**조성 무관**"으로 일반화하면 안 된다(2026-08-16 정정) — 도펀트 없는 host 도 −Li−S+Cl 을 네 번 반복하면 **2.356 V 로 점프**하고(Li₂₀P₄S₁₆Cl₈), 도핑 조성 D_plain 은 **1.893–2.356 V** 로 벌어진다 (`db/properties/oxidation_matched_factorial.json`).
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

### Q3 · 2026-06-26 · [DUPLICATE 처리] "Impact of Chlorination … Electrolyte/Cathode Interface" 재업로드 — Zuo 2022와 동일 논문 + Zuo SIMS종 ↔ 우리 XPS anchor 교차검증
**한 줄 답**: 새 PDF(`82ea256b/7dd4f5c1`)는 **이미 digest된 Zuo 2022 Angew(`papers/zuo2022_chlorination_cathode_interface.md`)와 *동일 논문*** (제목·저자 9인·Angew 62, e202213228·DOI 10.1002/anie.202213228 모두 일치). **신규 파일 생성 안 함** — 기존 digest가 이미 reference-depth(15절). 대신 사용자 요청 중 *유일하게 빠졌던* **XPS anchor 교차검증**만 기존 digest에 §11b로 추가.
- **중복 확인**: PDF 8쪽 전부 정독 → σ 2.9/7.0·R_cat 13.2/8.9·CE 77/79%·215/165→215/170·50cyc 133/145·O₂ 6.7/6.8·Reaction 1–3·DSC 535/532→523/493·Fig 1–7 모두 기존 §3·§5와 *글자 단위 일치*. 다른 버전 아님.
- **Zuo SIMS종 → 우리 산물 → XPS BE 1:1** (§11b 표): **PO₃⁻=Li₃PO₄(P 2p 133.3)** · **SO₃⁻=Li₂SO₄(S 2p 168.0)** · **Sₓ⁻=폴리설파이드(LiS4→S staircase; Li₂S 끝점 160.2)** · **Cl⁻=LiCl(Cl 2p 198.6)**. → Zuo가 ToF-SIMS로 본 4종 = 우리 `oxidation_stability.json nd2o3_interface_reactivity` 산물 4종(**Co9S8+Li₃PO₄+Li₂S+LiCl+Li₂SO₄** vs LiCoO₂) = 우리 `xps_reference_sei.csv` *기존* anchor. **세 도구가 같은 계면 화학 지목** = 독립 교차검증.
- **정직한 경계**: Zuo의 *핵심 주장*(Cl-rich가 phosphate/sulfate **적게**·폴리설파이드/SO₂ **많게**)은 *상대 fold*라 우리 정적 hull(dE comp1 −0.3227≈modelc −0.3308, 0.008=noise)·정적 XPS BE로는 **양/비율 못 가름** — "어떤 산물"만 검증, "얼마나"는 SIMS/DEMS 전용. comp1/modelc Cl-rich 산화는 **B③(계면 cycling)축 한정** Cl-rich 우위, intrinsic onset(B①)은 무승부(2.256 V 동일).
연결: `papers/zuo2022_chlorination_cathode_interface.md` §11b · §B③ · `db/properties/oxidation_stability.json`(Zuo block + nd2o3_interface_reactivity) · `db/properties/xps_reference_sei.csv` · INDEX `82ea256b/7dd4f5c1` 행.
