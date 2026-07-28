# Park 2026 (Chemical Engineering Journal 532 (2026) 174523, DOI 10.1016/j.cej.2026.174523) — 초박막 세라믹(Al₂O₃ 스퍼터) 코팅 건식 이축연신 PP 분리막(C-DB-PP): 이온수송 ↔ 내부단락저항 균형 (Li metal battery)

> slug `park2026_ceramic_pp_separator` · DOI `10.1016/j.cej.2026.174523` · type `DEM` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_park2026_ceramic_pp_separator.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Kwang Tae Park^a,†, Seungyeop Choi^b,†, Jun Pyo Seo^b, Rakhwi Hong^a, Minjae Kwon^a,
Joo Sung Lee^c, **Yong Min Lee\*** (yongmin@yonsei.ac.kr), "Ultra-thin ceramic-coated dry-biaxially
stretched polypropylene separator achieving balanced ionic transport and short-circuit resistance in
lithium metal batteries", *Chemical Engineering Journal* **532** (2026) 174523, DOI
10.1016/j.cej.2026.174523. 접수 2025-12-07 / 수정 2026-01-27 / 게재확정 2026-02-22 / online 2026-02-23.
†Kwang Tae Park·Seungyeop Choi 동등기여.

**소속:** (a) Dept. of Battery Engineering, **연세대(Yonsei)** — 제1저자 K.T. Park / 교신 Y.M. Lee;
(b) Dept. of Chemical & Biomolecular Engineering, **연세대** — S. Choi, J.P. Seo, **Y.M. Lee**;
(c) UPEX R&D Center(천안) — J.S. Lee(분리막 공급사).

★★ **LEAD = Yong Min Lee(연세대 DTBL) 교신(주도).** DTBL #273 항목.  단 **주제 = 분리막(separator)** 이라
우리 sulfide-ASSB 복합양극 DEM+MPM과 **셀 구성요소 자체가 다르다** → **TIER-4(· 타 component) 유지**.
이 그룹의 핵심 디지털트윈 양극 논문(#266/#271/#285/#286)과 달리 **분리막 막공학**이며, 우리 양극 압축·
수송 모델에 꽂히는 곳이 없다.

**소재계:** ★ **분리막(separator) = 건식 이축연신 폴리프로필렌(DB-PP, UPEX UPDP09, porosity 64%)** + 그 위
**RF 마그네트론 스퍼터링으로 증착한 나노스케일 Al₂O₃ 초박막(~22.7 nm, 바인더-free) = C-DB-PP**.  대조군 =
습식 이축연신 PE(WB-PE, SEMCORP SV9, porosity 47%) + 건식 단축연신 PP(DU-PP, SENIOR SD212F, porosity 44%).
셀 = **Li metal anode(200/40/800 µm Li) ‖ NCM622 양극**(L&F, 96:2:2), 액체전해질 **1.15 M LiPF₆ in EC/EMC
(3:7 v/v) + 10 wt% FEC**(대칭셀 2 wt% FEC).  full-cell 3.0–4.3 V, 0.5C 충전/2C 방전.
★★ **우리 LPSCl sulfide ASSB가 아니다** — **분리막 막(membrane) + Li metal 음극 + 액체전해질 LIB**다.
우리 프로젝트(sulfide ASSB **복합양극** 압축 + 접촉망 수송, DEM + MPM)와 **셀 구성요소(분리막 vs 양극)·소재
(PP/PE 고분자막·Al₂O₃·액체전해질 ≠ LPSCl SE/NMC811)·물리(연신 고분자막 다공·세라믹 코팅·덴드라이트 차단 ≠
입자 압축·접촉전도)가 전부 다르다.**

**한 줄 핵심 변수:** **분리막의 "고다공(64%) × 저토르투오시티(등방 기공망)"이 균형 이온수송을 주고, 초박막
세라믹 코팅이 젖음성·Li flux 균질성을 올려 내부단락(ISC) 저항을 보강한다** — DB-PP의 flow/응력유도 결정화
이축연신으로 만든 등방 다공구조가 σ_ionic을 올리되(다공·낮은 Gurley) 그 높은 기공연결성이 덴드라이트 침투
경로도 되어 단락에 취약해지는데, ~22.7 nm Al₂O₃ 코팅이 구조를 안 바꾸고(porosity·두께 유지) 계면만 안정화.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 (낮은) 관련성

**건식 이축연신 PP 분리막(DB-PP, porosity 64%)은 등방 고다공·저토르투오시티로 우수한 이온전도(0.982 mS/cm,
WB-PE 0.768·DU-PP 0.689 능가)와 균질 Li flux를 주지만 높은 기공연결성 탓에 덴드라이트 침투에 취약(T_sc
46 h ≪ WB-PE 300 h)하다.  그 위에 RF 스퍼터링으로 ~22.7 nm Al₂O₃ 초박막을 등각 코팅하면(C-DB-PP) porosity·
두께·Gurley를 거의 안 바꾼 채 젖음성↑(접촉각 103.5°→80.7°, 전해질 흡수 92.8%→145%)·Li flux 균질화·내부단락
저항↑(T_sc 46→77 h, +67.4%)·이온전도 추가↑(0.982→1.254 mS/cm, +27.7%) → Li‖NCM622 full-cell 600 cycles
후 70% 이상 유지(DB-PP는 400 cycles 후 급락)를 달성한다.**

**우리 프로젝트 관련성(낮음, TIER-4):** 이 논문은 **분리막(separator) 막공학**(연신 고분자 다공막 + 세라믹
스퍼터 코팅 + 덴드라이트 차단) + **Li metal 음극 + 액체전해질 LIB**이다 — 우리 **LPSCl sulfide ASSB의
연속체/접촉망 DEM+MPM 복합양극 압축·수송**과 셀 구성요소(분리막 vs 양극)·소재(PP/PE/Al₂O₃/액체 ≠ LPSCl SE/
NMC811)·물리(고분자막 연신 다공·세라믹 코팅·도금 덴드라이트 ≠ 고체입자 압축·접촉전도)가 전부 다르다.
**Yong Min Lee가 교신(주도)이나** 주제가 우리 도메인(양극 디지털트윈)과 어긋난다.  유일한 (먼) 접점은
**한 줄**: "분리막 porosity(64%)·tortuosity↓ → 균형 이온전도(σ_ionic)"는 우리가 모델하는 porosity-tortuosity-
conductivity 논리와 **같은 정성 물리**이나, 이는 **연신-고분자 분리막 멤브레인**의 다공이지 우리 **입상 압축
복합양극**의 다공이 아니다 → **transport/σ/porosity 절대앵커가 아니다**(그건 Bazzoun(LPSCl)·Varkey(halide)·
Minnmann(LPSCl cold-press)·#266이 담당).  **관련성을 부풀리지 않는다.**

---

## 1. 배경 / 동기 (Introduction, p.1)

- **Li metal 음극(LMA)의 약속과 문제.** Li metal = 이론용량 **3,860 mAh g⁻¹**(2,061 mAh cm⁻³), 산화환원
  −3.04 V(vs SHE) → 차세대 고에너지밀도 후보. 그러나 **불균일 덴드라이트 성장·SEI 불안정**으로 실용화 제약.
- **분리막의 역할 재조명.** 분리막은 전극 간 전자접촉을 막고 Li⁺ 수송을 가능케 하는 얇은 다공막.  특히
  **균일·낮은 토르투오시티 기공망 + 기계강건성(천공/인장강도)**이 균질 Li flux·ISC 위험↓·고율·안전에 중요.
- **기존 폴리올레핀 분리막 한계.** 상용 폴리올레핀 분리막은 본질적 소수성 → 젖음·안정성 불량.  완화책으로
  **슬러리 코팅 두꺼운 세라믹층(CCL, µm급)**을 입히면 분리막 질량·두께·Gurley↑ → 에너지밀도·출력 희생.
- **본 연구(명시):** **flow/응력유도 결정화 건식 이축연신 PP(DB-PP)** 로 고다공·저토르투오시티 기공망을
  만들어 저저항·고율을 확보하되, **나노스케일 Al₂O₃ 코팅을 RF 스퍼터링(바인더-free, 초박막)** 으로 입혀
  DB-PP 본연 기공구조를 보존한 채 계면을 안정화 → **이온수송 ↔ 내부단락저항의 균형**.  Li‖Cu·Li‖Li 대칭셀로
  도금/탈리 가역성, Li‖NCM622 full-cell로 율속·사이클 평가.

**약어:** DB-PP=dry-biaxially stretched PP(건식 이축연신 PP); DU-PP=dry-uniaxially stretched PP(건식 단축);
WB-PE=wet-biaxially stretched PE(습식 이축 PE); C-DB-PP=세라믹(Al₂O₃) 코팅 DB-PP(최종); CCL=ceramic
coating layer; ISC=internal short circuit(내부단락); T_sc=short-circuiting time(단락시간); MD/TD=machine/
transverse direction; GSM=gram per square meter(평량); LSV=linear sweep voltammetry; E/C=electrolyte-to-
capacity ratio.

---

## 2. 소재 & 제작 (Experiments, p.2)

### 2.1 분리막 (DB-PP / 대조군 + Al₂O₃ 스퍼터 코팅)
- **DB-PP(UPEX UPDP09, porosity 64%):** flow/응력유도 결정화 — 캐스팅 단계 급랭·연신 시 **사슬정렬·MD 결정성장**
  → 후속 이축연신으로 **균열 없이** 다공.  잘 정렬된 고분자 사슬의 이축연신 → **MD·TD 모두 등방 다공**(고연결).
- **대조군:** WB-PE(SEMCORP SV9, porosity 47%) — 희석제 추출·상분리 다공(균일 상호연결); DU-PP(SENIOR
  SD212F, porosity 44%) — 단축연신 → MD 한 방향 정렬 다공(비등방).
- ★ **Al₂O₃ RF 마그네트론 스퍼터링(→ C-DB-PP):** Al₂O₃ 타깃(직경 80 mm, 기판서 150 mm), Ar(99.999%) 7×10⁻³
  Torr, 냉각(열 손상 억제), pre-sputter 50 W/30 min(잔류물 제거) → 본 증착 **10 W/10 min(한 면씩 양면)**.
  → **초박막·바인더-free Al₂O₃ 코팅 분리막 = C-DB-PP**.  Al₂O₃층 두께 **~22.7 nm**(Si wafer 위 stylus
  profilometer, Fig S3).
- **특성평가:** 기공분포 = capillary flow porometer; 이온전도 σ = SUS/분리막/SUS 코인셀 EIS(5 MHz–50 kHz,
  10 mV), **σ = l/(R_b·S)** (l=두께, S=SUS 전극면적); 열수축 = 160 °C/30 min, **shrinkage(%) = (A_before−
  A_after)/A_before ×100**; 기계물성 UTM; 표면 FE-SEM·접촉각(DSA, DI water)·공기투과 Gurley(densometer)·
  XPS; 전기화학안정성 LSV(산화 0–6 V, 1 mV/s; 환원 OCV–0 V, 0.05 mV/s).

### 2.2 셀 조립 (p.3)
- **Li‖NCM622 full-cell(CR2032):** NCM622(14 mm) ‖ Li metal(200 µm, 16 mm), 분리막 18 mm.  양극 면적용량
  **2.7 mAh cm⁻²**, 로딩 15.5 mg cm⁻²(밀도 3.0 g cm⁻³).  전해질 1.15 M LiPF₆ EC/EMC(3:7) + 10 wt% FEC.
  formation 0.1C + stabilization 3 cycles → 0.5C 충전/2C 방전·3C/3C; 율속 0.5–10C 방전(0.5C 충전 고정).
- **Li‖Cu 셀:** Li(200 µm) ‖ Cu(12 µm), 0.5 mA cm⁻²·0.5 mAh cm⁻²(장수명·CE); **T_sc 측정 = 800 µm Li‖Cu,
  0.5 mA cm⁻² 연속 도금 → 급격 전압강하까지 시간**(덴드라이트 유발 내부단락 지표).
- **Li‖Li 대칭셀:** Li(200 µm) 양쪽, 1.15 M LiPF₆ EC/EMC(3:7) + 2 wt% FEC; 율속 0.5–10C·1 mAh cm⁻², 장수명
  0.5 mA cm⁻²·0.5 mAh cm⁻².
- **단층 파우치셀:** NCM622(4.8×4.8 cm², 2.0 mAh cm⁻²) ‖ 40 µm Li(5.0×5.0 cm²), Al 파우치, **E/C ≈ 3 g Ah⁻¹**
  lean 조건.

---

## 3. 핵심 메커니즘 — 2단 논리

**(1) DB-PP 등방 고다공·저토르투오시티 → 균형 이온전도 + 균질 Li flux.** 건식 이축연신의 등방 다공망(MD·TD)
은 (i) **낮은 평량(GSM 2.95) + 낮은 Gurley(16 s/100mL)** → 전해질 침투·Li⁺ 수송 효율↑ → **최고 이온전도
0.982 mS/cm**(WB-PE 0.768 > DU-PP 0.689); (ii) Li‖Cu 1st 도금 SEM에서 **smooth·compact 다공성 Li**(WB-PE/
DU-PP는 mossy·덴드라이트) → 균질 핵생성/성장.  ★ 그러나 **양날의 검**: 그 높은 기공연결성이 **덴드라이트
침투의 쉬운 통로** → T_sc 급감(46 h ≪ WB-PE 300 h / DU-PP 308 h, 이론 331 h의 15% 미만).  즉 **이온수송과
ISC 저항이 trade-off** — 균형이 핵심.

**(2) 초박막 Al₂O₃ 스퍼터 코팅 → 구조 보존 + 계면 안정화(ISC 저항 보강).** ~22.7 nm Al₂O₃를 등각 코팅(C-DB-PP)
하면 (i) **기공구조 보존** — porosity·두께(8.9 µm)·GSM(2.98)·Gurley(17)·기공직경(78.1→79.0 nm) 거의 불변
(코팅이 기공망을 막거나 좁히지 않음); (ii) **젖음성↑** — 접촉각 **103.5°→80.7°**, 전해질 흡수 **92.8%→145%**
→ 이온전도 추가↑ **0.982→1.254 mS/cm(+27.7%)**; (iii) **Li flux 균질화** — 핵생성 과전위↓(DB-PP 27 mV →
C-DB-PP 20 mV), Cu 위 dense·granular Li, 덴드라이트 침투 SEM상 억제 → **T_sc 46→77 h(+67.4%)·EIS상 ISC
지연**; (iv) **열안정성↑** — 160 °C/30 min 후 면적유지 88.8%→95.1%.

⇒ 우리 식으로: **분리막 다공(porosity·tortuosity) → 이온전도 + flux 균질성**이라는 porosity-수송 논리.
단 주체가 **연신-고분자 분리막 멤브레인**(우리가 안 다루는 셀 구성요소)이고, 세라믹 코팅·덴드라이트 차단·
도금 형상은 **음극측 도금·계면화학**이다.  우리 모델은 **양극측 입자 압축·접촉 σ**이며 분리막·도금·덴드라이트를
다루지 않는다.  **개념(porosity↓tortuosity→수송)만 멀리서 인접**, 수치·메커니즘·폼 차용 없음.

---

## 4. 섹션별 결과 — 핵심 수치 (Results, p.4–10)

### 4.0 헤드라인 표 (Table 1, Table 2)

**Table 1 — 분리막 물리·이온전도 (대조군 비교):**
| 분리막 | 두께(µm) | GSM(g m⁻²) | Gurley(s/100mL) | R_b(Ω) | 이온전도도(S) | σ_ionic(mS cm⁻¹) | porosity(%) |
|---|---|---|---|---|---|---|---|
| WB-PE | 9.2 | 4.52 | 71 | 0.596 | 1.68 | 0.768 | 47 |
| DU-PP | 12.9 | 6.52 | 236 | 0.931 | 1.07 | 0.689 | 44 |
| **DB-PP** | **8.9** | **2.95** | **16** | **0.451** | **2.22** | **0.982** | **64** |

**Table 2 — Al₂O₃ 코팅 효과 (DB-PP → C-DB-PP):**
| 분리막 | 두께(µm) | GSM | Gurley | R_b(Ω) | 이온전도도(S) | σ_ionic(mS cm⁻¹) |
|---|---|---|---|---|---|---|
| DB-PP | 8.9 | 2.95 | 16 | 0.451 | 2.22 | 0.982 |
| **C-DB-PP** | **8.9** | **2.98** | **17** | **0.353** | **2.83** | **1.254(+27.7%)** |

| 지표 | 값 | 비고 |
|---|---|---|
| **DB-PP porosity** | **64%** | 등방 고다공(WB-PE 47·DU-PP 44 대비) |
| **Al₂O₃ 코팅 두께** | **~22.7 nm**(바인더-free 스퍼터) | Si wafer stylus, Fig S3 (분리막 자체 두께 8.9 µm) |
| **기공 평균직경** | WB-PE **45.3** / DU-PP **26.2** / DB-PP **78.1** / C-DB-PP **79.0 nm** | capillary flow porometer (Fig 1b–d, S6) |
| **σ_ionic 순서** | **DB-PP 0.982 > WB-PE 0.768 > DU-PP 0.689 mS/cm** | Table 1 |
| **σ_ionic 코팅증분** | **0.982 → 1.254 mS/cm (+27.7%)** | C-DB-PP(젖음성↑, Table 2) |
| **접촉각(DI water)** | WB-PE 100.2° / DU-PP 105.5° / DB-PP 103.5° → **C-DB-PP 80.7°** | Fig 1e, 5c (코팅으로 친수화) |
| **전해질 흡수율** | WB-PE 80.7 / DU-PP 79.2 / DB-PP 92.8 / **C-DB-PP 145.0 %** | SI Table S1 |
| **열수축(160°C/30min 후 면적유지)** | WB-PE **17.8%** / DU-PP·DB-PP **85.2·88.8%** / **C-DB-PP 95.1%** | PP Tm 165°C > PE 130°C; CCL 효과 |
| **T_sc(800µm Li‖Cu 단락시간)** | WB-PE **300** / DU-PP **308** / DB-PP **46** → **C-DB-PP 77 h(+67.4%)** | 이론 완전소모 331 h; Fig 3c·7b |
| **핵생성 과전위** | DB-PP **27 mV** → C-DB-PP **20 mV** | 1st Li 도금(Fig S9) |
| **Li‖NCM622 사이클 유지율** | **C-DB-PP >70% @600 cycles** vs **DB-PP 400 cycles 후 급락** | 0.5C/2C, Fig 8b |

### 4.1 분리막 형상·기공 (Fig 1, 대조군)
- **SEM(Fig 1a):** WB-PE = 균일 상호연결 다공(추출·상분리); DU-PP = MD 단방향 정렬 다공(비등방); **DB-PP =
  MD·TD 등방 다공**(이축연신, 더 등방·기계균형 기공망).
- **기공분포(Fig 1b–d):** 평균직경 WB-PE 45.3 / DU-PP 26.2 / **DB-PP 78.1 nm**(최대 79.3 nm) — DB-PP가 가장
  큰 기공.  접촉각(Fig 1e) 100.2/105.5/103.5° — 폴리올레핀 공통 소수성(유사).
- **열수축(Fig S1):** WB-PE 17.8%만 유지(심한 수축), DU-PP·DB-PP 85.2·88.8% 유지(PP Tm 165°C가 PE 130°C
  보다 높아 열안정).  DB-PP는 **이축 수축**(양방향), DU-PP는 단방향 수축.

### 4.2 Li 도금/대칭셀 (Fig 2, 4)
- **Li‖Cu CE(Fig 2a,b):** DB-PP는 WB-PE 수준 사이클(고이온전도에도 80 cycles 후 CE 요동 → 고이온전도가
  사이클 안정으로 직결되진 않음).  1st 도금 nucleation overpotential은 DB-PP가 낮음.
- **Li 형상(Fig 2c,d):** WB-PE·DU-PP = mossy·덴드라이트(불균일); **DB-PP = smooth·compact 다공성 Li**
  (등방 다공이 균질 flux → 균일 핵생성/성장).
- **Li‖Li 율속·장수명(Fig 4a,b):** 저전류 평탄(유사 계면동역학); 고전류(10 mA cm⁻²)에서 WB-PE·DU-PP 분극
  급증 vs **DB-PP 저과전위 유지**(고이온전도).  단 0.5 mA cm⁻² 장수명은 큰 차이 없음(Fig 4b).
- **Li 단면(Fig 4c):** 10 cycles 후 다공 Li층 두께 WB-PE 81 / DU-PP 69 / **DB-PP 47 µm**(가장 얇고 치밀,
  41% 감소) → dense·균일 도금.

### 4.3 단락(ISC) 저항 — 핵심 trade-off (Fig 3)
- **T_sc(800µm Li‖Cu 연속도금, Fig 3a–c):** 800 µm Li 완전소모 이론시간 331 h.  WB-PE 300·DU-PP 308 h(이론
  근접, 우수 내단락); **DB-PP 46 h(이론의 15% 미만, 급격 단락)** — 고기공연결성이 덴드라이트 침투 통로.
- **Li 침투 SEM(Fig 3d,e):** 50 h 도금 후 DB-PP 기공으로 **현저한 덴드라이트 Li 침투**; WB-PE·DU-PP는 원래
  기공구조 유지(막힘 없는 침투 경로 차이).
- ⇒ **DB-PP의 고다공·고연결성은 이온수송에 유리하나 덴드라이트 침투에도 유리 → 상용 분리막은 이온수송·
  단락저항의 최적 균형이 핵심**(논문 핵심 thesis).

### 4.4 세라믹 코팅 효과 C-DB-PP (Fig 5, 6, 7)
- **구조 보존(Fig 5b, Table 2, S5,S6):** Al₂O₃ ~22.7 nm 등각 코팅, GSM·Gurley·기공분포(78.1→79.0 nm) 유지
  → 기공망 미차단.  XPS(Fig S4): Al–O 결합(74.3 eV, Al₂O₃) + C 1s C–O/O–C=O(스퍼터 산소가 PP 사슬 일부
  절단·반응).  EDS(Fig S5): Al 균일분포.
- **젖음성↑(Fig 5c):** 접촉각 **103.5°→80.7°**, 전해질 흡수 92.8→145%(SI) → **σ_ionic 0.982→1.254(+27.7%)**.
- **열안정성↑(Fig S7):** 160°C/30min 후 면적유지 88.8→95.1%(세라믹 CCL).
- **Li‖Cu/대칭셀(Fig 6):** C-DB-PP가 DB-PP보다 안정 CE·저과전위·dense granular Li.  핵생성 과전위 DB-PP
  27 → C-DB-PP 20 mV.  50 h 도금 후 EIS(Fig S10): DB-PP는 50 h에 임피던스 급락(내부전자 단락경로) vs
  C-DB-PP는 WB-PE/DU-PP 수준 고임피던스 유지(ISC 지연).
- **T_sc 보강(Fig 7a,b):** **46→77 h(+67.4%)** — 구조 불변에도 젖음성·균질 도금 향상이 단락 지연.  Li 침투
  SEM(Fig 7c,d): DB-PP는 관통 덴드라이트, C-DB-PP는 균질 형상 유지.  단면(Fig S11): C-DB-PP가 더 얇고 치밀.

### 4.5 Li‖NCM622 full-cell + 파우치 (Fig 8)
- **율속(Fig 8a):** C-DB-PP가 3C 이상 고율에서 최고 방전용량(젖음성·이온전도↑로 분극↓).
- ★ **장수명(Fig 8b):** 0.5C 충전/2C 방전 — **C-DB-PP >70% 유지 @600 cycles**; **DB-PP는 400 cycles 후
  급격 용량열화**.  WB-PE·DU-PP도 600 cycles 전 열화.  → 균질 Li flux + 장기 안정성에 분리막 균형이 핵심.
- **Post-mortem(Fig 8c, S15):** 50 cycles 후 Li 표면 — WB-PE·DU-PP loose·heterogeneous, DB-PP denser,
  **C-DB-PP가 가장 균일·compact**.  EDS(S15): SEI 원소(C/O/F/P) 비율은 DB-PP·C-DB-PP 유사 → 개선은 **균질
  Li flux 분포** 기여(SEI 화학 자체 변화 아님).  EIS(S14): 분리막 종류가 R_SEI/R_ct에 큰 영향 없음.
- **3C/3C(Fig S16) + lean E/C≈6(Fig S17):** C-DB-PP가 모두 최고 유지율(전해질-제한 조건에서 효과 증폭).
- **파우치(Fig 8d–f):** 40 mAh NCM622 ‖ 40 µm Li, E/C≈3 g Ah⁻¹ — C-DB-PP 70 cycles 안정 유지·CE → 실용성.

### 4.6 결론 모식 (Fig 8g)
- **종래 분리막**: 비등방 다공·고토르투오시티 → 불균일 Li flux → 덴드라이트.  **DB-PP**: 등방 다공·저토르
  투오시티 → 더 균일 flux but 덴드라이트 침투 취약.  **C-DB-PP**: + 초박막 세라믹 → 최균일 flux + 덴드라이트
  침투 저항 → 균형.

---

## 5. 그림 한 장씩 — 무엇을 보이고 (우리는 안 씀)

### 본문 Figures
- **Fig 1:** 대조군 분리막 — (a) top-view SEM(WB-PE 등방·DU-PP 단방향·DB-PP 이축 등방), **(b–d) 기공분포
  (45.3/26.2/78.1 nm)**, (e) 접촉각(100.2/105.5/103.5°).
- **Fig 2:** Li‖Cu — (a) CE 100 cycles, (b) 1st V-t곡선(과전위), **(c,d) Cu 위 1st Li SEM(WB-PE/DU-PP mossy
  vs DB-PP smooth)**.
- **Fig 3:** ★ ISC trade-off — (a) 800µm Li‖Cu 모식, (b) 연속도금 V-t(급강하=단락), **(c) T_sc(300/308/46 h,
  이론 331)**, (d,e) 50h 도금 후 Li 침투 SEM(DB-PP 관통).
- **Fig 4:** Li‖Li 대칭 — (a) 율속(고전류 DB-PP 저분극), (b) 0.5mA 장수명, **(c) 10cyc 후 Li 단면(81/69/
  47 µm — DB-PP 최박)**.
- **Fig 5:** ★ C-DB-PP — (a) 스퍼터 제작 모식, **(b) DB-PP vs C-DB-PP SEM(구조 보존)**, **(c) 접촉각 103.5
  →80.7°**.
- **Fig 6:** C-DB-PP 도금 — (a) Li‖Cu CE, (b) Cu 1st Li SEM, (c) Li‖Li 율속, (d) 10cyc 후 단면 SEM
  (DB-PP 47 vs C-DB-PP 37 µm).
- **Fig 7:** ★ ISC 보강 — (a) 800µm Li‖Cu V-t, **(b) T_sc 46→77 h(+67.4%)**, (c,d) 50h 도금 후 Li SEM
  (C-DB-PP 균질).
- **Fig 8:** ★ full-cell — (a) 율속 0.5–10C, **(b) 0.5C/2C 사이클(C-DB-PP >70%@600 vs DB-PP 400cyc 급락)**,
  (c) 50cyc 후 Li SEM, (d–f) 40 mAh 파우치(E/C≈3), **(g) Li 도금 모식(종래/DB-PP/C-DB-PP flux 균질도)**.

### SI 주요(스킴)
- **S1** 160°C 노출 사진(WB-PE/DU-PP/DB-PP); **S3 Al₂O₃ 두께 ~22.7 nm(stylus)**; **S4 XPS C1s·Al2p
  (Al–O 결합)**; S5 EDS(C·Al); **S6 C-DB-PP 기공분포**; **Table S1 전해질 흡수 80.7/79.2/92.8/145.0%**;
  S7 160°C 사진(DB-PP/C-DB-PP); **S9 1st 도금 과전위 27 vs 20 mV**; **S10 임피던스 진화(50h 후 DB-PP 급락)**;
  S11 Li 단면; S12 LSV(전기화학안정); S14 R_SEI/R_ct(분리막 영향 작음); **S15 Li EDS(SEI 원소 유사)**;
  S16 3C/3C 사이클; S17 lean E/C≈6 사이클.

---

## 6. 기술 미니용어집 (우리 맥락)

- **분리막(separator):** 전극 사이 다공 멤브레인 — 전자절연 + Li⁺ 이온 통로.  ★ **우리가 안 다루는 셀
  구성요소** — 우리는 **복합양극**(NMC811+LPSCl)만 모델(압축·접촉망).  분리막은 우리 파이프라인에 없음.
- **건식 이축연신(dry-biaxial stretch) PP:** flow/응력유도 결정화 + 양방향 연신으로 만든 등방 다공 PP막
  (균열 없는 다공).  porosity 64%.  vs 습식(추출·상분리 PE)·단축(MD 정렬 PP).  = 고분자막 공정(우리 입자
  패킹과 무관).
- **토르투오시티(tortuosity) / Gurley:** 기공 경로 굴곡도 / 공기투과 저항(낮을수록 덜 굴곡·고투과).  ★ 개념
  적으로 우리 σ_ionic C(τ) 항의 τ와 **같은 물리량(porosity-tortuosity-conductivity)**이나, 여기선 **연신-
  고분자 분리막 멤브레인** τ이지 우리 **입상 압축양극** τ가 아니다 → 수치/폼 차용 금지.
- **RF 마그네트론 스퍼터링 / Al₂O₃ CCL:** 진공 플라즈마로 ~22.7 nm 세라믹 박막 등각 증착(바인더-free).  =
  분리막 표면 박막코팅 공정(우리 입자 모델에 대응 없음; 우리 `--coh`는 SE 입자 부착이지 막코팅 아님).
- **T_sc(short-circuiting time) / ISC:** 연속 Li 도금 중 덴드라이트가 분리막을 관통해 내부단락 일으키기까지
  시간(분리막 덴드라이트 차단성 지표).  우리 ASSB transport엔 분리막·도금 덴드라이트 축 없음.
- **핵생성 과전위 / Li flux 균질도:** Li 도금 핵생성 추가전위(낮을수록 균질) / 표면 전류분포 균질성.  =
  음극측 도금 동역학(우리 양극 입자 압축·접촉전도와 다른 물리).
- **E/C ratio(electrolyte-to-capacity) / 전해질 흡수율:** 액체전해질 투입량 정규화 / 분리막 전해질 함습량.
  ★ **우리 ASSB는 액체전해질·분리막이 없다**(고체전해질 자체가 분리막+이온전도체).  전이 불가.

---

## ★ 7. 비교 vs 우리 DEM+MPM — 짧고 정직하게 (TIER-4 / 주변부, 모델 영향 0)

⚠ **대전제:** 이 논문은 **분리막(separator) 막공학**(건식 이축연신 PP 다공막 + Al₂O₃ 스퍼터 코팅 + 덴드라이트
차단·Li 도금) + **Li metal 음극 + 액체전해질 LIB**다.  우리 모델은 **LPSCl sulfide ASSB의 연속체/접촉망
DEM+MPM 복합양극 압축 + 수송(Kirchhoff/Holm σ triad)**다.  **셀 구성요소(분리막 vs 양극), 소재(PP/PE 고분자
막·Al₂O₃·액체전해질 ≠ LPSCl SE/NMC811/무전해질), 물리(고분자막 연신 다공·세라믹 코팅·도금 덴드라이트 ≠ 고체
입자 압축·접촉전도)** 가 전부 다르다.  **Yong Min Lee가 교신(주도)이나** 주제가 우리 도메인(양극 디지털트윈
#266/#271/#285/#286)과 어긋나는 **분리막 멤브레인** 논문 → TIER-4.  **수치 σ/porosity 앵커가 절대 아니다** —
그건 Bazzoun(LPSCl)·Varkey(halide)·Minnmann(LPSCl cold-press)·#266이 담당한다.  **관련성을 부풀리지 않는다.**

### 유일한 (먼) 접점 — 한 줄
- ★ **"분리막 porosity(64%)·tortuosity↓ → 균형 이온전도(σ_ionic)"가 우리가 모델하는 porosity-tortuosity-
  conductivity 논리와 같은 정성 물리.**  그러나 그들의 다공은 **연신-고분자 분리막 멤브레인**(추출/연신으로
  형성, 단일상 고분자, σ_ionic 0.7–1.25 mS/cm 액체전해질 함습)이고, 우리는 **입상 LPSCl SE의 압축 패킹
  다공**(rearrangement + 소성 void-fill, σ_ionic 고체 SE 접촉망 Kirchhoff/Holm)이다 — 셀 구성요소·재료·
  형성기구·전도매질(액체-함습 막 vs 고체 입자접촉) 모두 다르다.  **정성 개념만 인접일 뿐 수치·폼·메커니즘
  전이 없음.**  transport/압축/porosity/σ 어느 앵커도 아니다.

### 우리 우위 / frame[5] (간단)
- 그들: **분리막 막공학(연신 고분자 다공·세라믹 스퍼터 코팅)·Li 도금 균질화·덴드라이트 차단·내부단락(T_sc)
  + 액체전해질 LIB full-cell.**  강력하지만 **양극 입자 압축역학 없음·explicit 접촉 σ triad(ionic/e/thermal)
  없음·소성 입자 morphology 없음·압력→미세구조→σ 예측 없음**(우리 DEM+MPM 영역).
- 우리: **압력→미세구조→σ(ionic/e/thermal) 예측 + MPM 소성 void-fill/morphology + voxel FV + fracture.**
  그들 분리막 멤브레인은 우리 양극 입자 모델과 **셀 구성요소가 달라 상보조차 아님.**
- ⇒ **이 논문은 우리 파이프라인의 입력단도 출력단도 아니다.** 순수 문헌 맥락(분리막 막공학 + porosity-
  tortuosity-수송이라는 먼 정성 인접).  **모델 하자/검증/앵커 어느 것도 아님 — TIER-4 유지.**

### 비교 요약표
| 축 | Park 2026 (#273, 세라믹 코팅 PP 분리막·액체) | 우리 (LPSCl ASSB, DEM+MPM) | 판정 |
|---|---|---|---|
| 셀 구성요소·소재 | **분리막 멤브레인**(PP/PE·Al₂O₃ 코팅) + 액체 LIB | LPSCl SE+NMC811 **복합양극** 입자 접촉망 | ⚠ 구성요소부터 다름 — 전이불가 |
| 핵심 물리 | 고분자막 연신 다공·세라믹 코팅·덴드라이트 차단·Li 도금 | 입자압축·접촉 σ·소성 void-fill | ✗ 대응 안 됨 |
| porosity/tortuosity | 연신 고분자막 다공 64%·저-τ(이온수송) | 입상 압축 SE 패킹 다공(rearrange+void-fill) | 정성개념만 인접·형성기구/매질 다름·전이 無 |
| σ_ionic | 액체-함습 막 0.768/0.689/0.982/1.254 mS/cm | 고체 SE 접촉망 Kirchhoff/Holm(Bazzoun 앵커) | 같은 "σ_ionic" 명칭이나 매질·물리 무관 |
| 수치 앵커 | ✗ (분리막·액체·도금) | Bazzoun/Varkey/Minnmann/#266 | **앵커 아님** |

---

## ★ 8. 우리 작업에 넣을 인사이트 — 정직하게 없음

1) **모델 영향 0 — 순수 문헌 맥락(아카이브 완전성 항목).** 이 논문은 우리 DEM+MPM transport/압축 어디에도
   꽂히지 않는다(분리막 막공학 + 액체 Li metal LIB).  가치는 **"DTBL Yong Min Lee 교신 논문 카탈로그
   완전성"** + **"분리막 porosity-tortuosity→이온수송이라는 정성 물리가 우리 σ_ionic C(τ)에 멀리서 개념
   인접"** 이라는 배경 인지뿐.  **수치·폼·메커니즘 전이 없음.**

2) **분리막 다공 ≠ 우리 양극 압축 다공(혼동 금지).** 그들 porosity(64%) = **연신-고분자 분리막 멤브레인의
   추출/연신 다공**; 우리 porosity = **입상 LPSCl SE의 압축 패킹·소성 void-fill 다공**.  셀 구성요소(분리막
   vs 양극)·형성기구(연신 vs 압축)·전도매질(액체-함습 vs 고체 입자접촉) 모두 다르다.  σ_ionic 명칭이 같아도
   물리가 무관 → 절대값/τ-폼 차용 금지.

3) **세라믹 스퍼터 코팅·덴드라이트 차단·T_sc는 우리 영역 밖.** Al₂O₃ 박막코팅·내부단락 시간·도금 형상은
   **분리막/음극측 계면공학**이다.  우리는 양극측 입자 압축·접촉 σ만 다루며 분리막·도금·덴드라이트 축이 없다.

### 보너스 실행 항목
- **#273 인덱스 갱신**(완료): 1줄 카탈로그 행을 검증 수치로 보강(DB-PP porosity 64%·σ_ionic 0.982 →
  C-DB-PP 1.254 mS/cm(+27.7%)·Al₂O₃ ~22.7 nm·T_sc 46→77 h(+67.4%)·접촉각 103.5→80.7°·열수축유지 88.8→
  95.1%·full-cell >70%@600 cycles; LEAD=Y.M.Lee 교신).  **TIER-4(· 타 component) 유지.**
- ⚠ **역할 구분(혼동 금지):**
  - **#273(이 논문, 세라믹 코팅 PP 분리막·액체):** **분리막 막공학 + porosity-tortuosity 정성 인접.** 모델 영향 0, TIER-4.
  - **#280(Choi, 탄성 Li metal anode·액체):** 음극 도금 계면공학 + 응력완화 테마 먼 인접(TIER-4).
  - **#284(Oh, SiOx/흑연·액체):** CBD ion/electron trade-off 독립확증 + 분산정량(SSRM/W_adh).
  - **#285(Hong, 단결정 NCMA·액체):** rigid-AM 검증 + 점탄성 spring-back 미구현 한계.
  - **#286(Yoo, 흑연·액체):** Phase 5 z-구배 + 토모 정량(τ/PNM).
  - **σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann·#266이 담당.**
- 분리막 데이터(연신 고분자막 porosity·τ·Gurley, 액체 σ_ionic)는 우리 입상 양극 모델과 무관 → 파싱·DB화
  불필요(노트만 유지).
