# Dry-Crafted Charge-Conductive ZrO₂₋ₓ Cathode Shell Coating for High-Performance Sulfide-Based Solid-State Batteries — Choi/Chang/…/J.Kim/J.Moon/W-H.Ryu (Small 2026)

> slug `choi2026_bzox_dry_zro2x_nmc_shell_coating` · DOI `10.1002/smll.73805` (Small 2026, 0:e73805; Received 2026-01-27 / Accepted 2026-05-09) · type `exp(코팅·전기화학) + DFT보조(계면 슬랩 pDOS·결합길이)` · PDF `inbox/28. Dry-Crafted…pdf`(본문 10 pp) + `inbox/28. Sup) …pdf`(SI 10 pp, Fig S1–S8+Table S1) · digested `2026-07-16` (SI-only digest 같은 날 본문 확보로 통합 업그레이드) · 태그 **[외부]** · 사용자 분류 폴더 `DFT`
> ← supersedes `bzox_dry_zro2x_nmc_shell_coating_sulfide_assb.md` (SI-only 구판; 스텁으로 대체)

---

## 0. 판 이력 / 이 digest를 읽는 법
- **2026-07-16 오전: SI 전용본만으로 1차 digest** (저자·저널·방법·headline 전부 n/a). **같은 날 본문 PDF 확보 → 본 문서로 통합 업그레이드.** SI 그래프 판독 근사치(±5 mAh/g 단서)는 §3.6에 그대로 승계하되 본문 텍스트 수치와 구분 표기.
- 구판의 "웹 확인 사항" 2건은 본문에서 **둘 다 확정 → 본문 출처로 승격**: ① 자매 선행논문 = 본문 ref 23 **Choi et al., JMCA 2024, 12, 30667 (DOI 10.1039/D4TA05179C)** — 같은 1저자(Yoo Jung Choi)의 black zirconia LIB 논문, 본 논문은 그 ASSB 확장판 맞음. ② 양극 = **단결정(single-crystalline) LiNi₀.₈Mn₀.₁Co₀.₁O₂** (키워드·abstract 명시; Fig 3 패널 라벨 "SNMC"=single-crystalline NMC).
- 우리 litdb 내 위치: **[Sundar] ZrO₂-"실패" 판정과의 코팅-대상 교차 분석**(§7)이 핵심 축. B③(양극 계면 레버) 논문.

## 1. 한 줄 요약
산소결핍 **black ZrO₂₋ₓ(BZOx)** 를 **solvent-free dry mechanofusion**으로 단결정 NMC811 입자에 **~8 nm conformal shell** 코팅 → 화학양론 white ZrO₂(WZO)가 전자 절연 장벽(σ_e ÷25.5, ΔV 0.73 V, R_CA-SE 192.9 Ω)이 되는 것과 달리 BZOx는 전하 수송을 보존(σ_e ÷3.8, ΔV 0.18 V, R 55.2 Ω)하면서 LPSCl 계면 부반응(POₓ/SOₓ/폴리설파이드)을 억제 — **초기 CE 69.6→77.5 %, 100 cyc 유지율 70.6→80.4 %**. VASP DFT+U 계면 슬랩(LNO/WZO/BZOx | LPSCl)의 계면-S pDOS·결합길이로 "계면 S 안정화 + SO₂ 발생 억제" 기전 뒷받침.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 저자 | **Yoo Jung Choi**(Sookmyung, 공동1저) · **Hongjun Chang**(Chung-Ang, 공동1저) · Sungbin Jang(KIER Ulsan) · Woonbae Sohn(KBSI) · Juho Lee(UNIST/DGIST) · **Jinsoo Kim**(KIER/DGIST, 교신) · **Janghyuk Moon**(Chung-Ang, 교신 — DFT 파트) · **Won-Hee Ryu**(Yonsei 배터리공학, 교신) |
| 저널/년/DOI | **Small 2026**, 0:e73805, **10.1002/smll.73805** (Wiley; Hanyang Univ. Library 경유 2026-07-07 다운로드) |
| 재료 | 코팅: **BZOx = 산소결핍 black ZrO₂₋ₓ**(자체 합성) vs **WZO = 화학양론 white ZrO₂**(Sigma-Aldrich 99%) · 양극: **단결정 LiNi₀.₈Mn₀.₁Co₀.₁O₂**(SMLAB, ~5 µm) · SE: **LPSCl(Li₆PS₅Cl)** · 음극: Li metal 40 µm |
| 유형 | exp 주도 + DFT 보조(계면 pDOS·결합길이; NEB·AIMD 없음) |
| 펀딩 | NRF RS-2023-00208983 · KETEP/MOTIE RS-2022-KP002721 · MOTIE RS-2024-00409900 · KIST 26E0321 |

## 3. 핵심 수치 (전부 본문/SI 소재 명시)
### 3.1 합성·코팅 (본문 §4.1)
- **BZOx 합성**: PVP 0.6 g + 에탄올 27 g + zirconium acetate 용액 12 g + acetic acid 5 g → 350 rpm 밤샘 교반 → 공기 350 °C 1 h 하소 → **H₂/Ar(5 % H₂) 600 °C 4 h 환원 어닐**. (JMCA 2024 ref 9·23 프로토콜 승계)
- **Mechanofusion**: Hosokawa Micron **Nob-Mini**, 코팅재:NMC = **3:97 wt**, 블레이드-벽 간극 1 mm, **2000 rpm 10 min → 4000 rpm 30 min** 2단.
- **코팅 두께 (HR-TEM, Fig 2a,b)**: WZO **~9.7 nm** / BZOx **~8.1 nm** — conformal·ultrathin (통상 산화물 코팅 수십–수백 nm 대비). EDS Ni/Zr/O 균일분포.
- **Zr 3d XPS (Fig 2k,l)**: WZO 184.1(3d₃/₂)/181.74(3d₅/₂) eV; BZOx는 추가 shoulder **180.68 eV = 환원 Zr⁽⁴⁻ˣ⁾⁺** → 산소공공 형성 증거. O 1s 533.2 eV shoulder(공공 자리 흡착 OH⁻/O₂; Fig S3).
- **XRD (본문 §2.1 텍스트)**: "BZOx = **monoclinic** 단상, WZO = **monoclinic+tetragonal 혼상**" — ⚠ 구판 digest의 SI Fig S1 판독(WZO tetra+mono / **BZOx tetragonal 단상·broad, PDF 00-027-0997 ZrO₁.₈ 카드**)과 상 배정이 어긋남(§10-4). PDF 카드 매칭은 SI 판독 유지, 상 이름은 본문 텍스트를 병기.
- BZOx **밴드갭 0.5–2.25 eV** (선행논문 인용값): 저자들의 설계 논리 = E_g<0.5 eV는 σ_e 과다→**SE 표면 분해 촉진**(ref 11 = Xiao/Ceder Joule 2019 코팅 스크린), 절연은 rate 손해 → **mixed ionic-electronic 중간창**이 CAM 코팅 적정.

### 3.2 첫 사이클 (0.1 C, **1 C = 200 mA g⁻¹**, 3.0–4.3 V, 25 °C; Fig 3a–d)
| 시료 | 충전 | 방전 (mAh g⁻¹) | 비가역 손실 | **ΔV (hysteresis)** | **초기 CE** |
|---|---|---|---|---|---|
| NMC (pristine) | 222.03 | 154.58 | 67.45 | 0.3 V | 69.6 % |
| NMC-WZO | n/a | 121.2 | 73.31 | **0.73 V** | 62.3 % |
| **NMC-BZOx** | 203.41 | **157.57** | **45.84** | **0.18 V** | **77.5 %** |
> WZO는 방전 초입 IR drop 급증(절연 장벽). 비가역 손실 = SE 분해 + 양극 표면 O ↔ SE의 P/S 반응(POₓ⁻/SOₓ⁻ 저항종·rock-salt 층).

### 3.3 장기 사이클 (100 cyc, 0.1 C; Fig 3e)
| 시료 | 100 cyc 방전용량 | 유지율 | CE 거동 |
|---|---|---|---|
| NMC | 109.2 mAh g⁻¹ | 70.6 % | 낮음 |
| NMC-WZO | (초기 ~100) | **85.8 %** | 중간 — 단 첫 80 cyc 동안 가역용량이 NMC보다 낮음(고저항·저활성) |
| **NMC-BZOx** | **126.69 mAh g⁻¹** | 80.4 % | **최고** |
> ⚠ **유지율 %만 보면 WZO가 최고(85.8)** — 단 절대용량이 낮아서(Li 이용량↓·부피변화↓) 생긴 통계. BZOx의 승리는 **절대용량 + CE + hysteresis** 조합. "BZOx가 유지율 최고"라고 쓰면 틀림(§10-2).
- dQ/dV 100 cyc (Fig S4): NMC·BZOx 피크 이동 미미(가역성 유지); WZO는 산화 3.8→3.75 V·환원 3.63→3.7 V 이동 = **지연 활성화**(절연 코팅 고과전압 → 사이클 진행하며 활성).

### 3.4 계면저항 EIS (7 MHz–100 mHz, 10 mV; 등가회로 R_SE+R_CA-CA+R_CA-SE+R_AN-SE+CPE_W; Fig 4a,b)
| (첫 사이클 후) | NMC | NMC-WZO | NMC-BZOx |
|---|---|---|---|
| R_CA-CA (복합체 이온) | 2.3 Ω | 3.76 Ω | 2.8 Ω |
| **R_CA-SE (지배항)** | 44.5 Ω | **192.9 Ω** | **55.2 Ω** |
> 사이클 전엔 3종 모두 저저항(냉압 접촉 양호). BZOx는 Li-free 조성인데도 CA-CA가 NMC급.

### 3.5 σ_e (DC 분극 200 mV, **30 °C**; Fig S6 + 본문 §2.3)
| 시료 | I (mA) | R (Ω) | L (mm) | A (cm²) | **σ_e (S/cm)** | vs pristine |
|---|---|---|---|---|---|---|
| SNMC | 1.083 | 184.67 | 0.364 | 1.326 | **1.49×10⁻⁴** | 1× |
| SNMC@WZO | 0.035 | 5714.2 | 0.444 | 1.326 | **5.85×10⁻⁶** | **÷25.5** (절연 장벽) |
| SNMC@BZOx | 0.245 | 816.3 | 0.419 | 1.326 | **3.88×10⁻⁵** | **÷3.8** (전도 보존; WZO 대비 6.6×) |
> ⚠ 이것은 **코팅 NMC 펠릿의 σ_e**(10⁻⁴–10⁻⁶) — SE bulk σ_e anchor([Liu23] 8.16e-9 / [Li25] 1.02e-8 / [Taklu] 8.75e-9)와 물리량 다름, 혼용 금지. SE는 σ_e↓가 선, CAM 코팅은 σ_e 보존이 선.

### 3.6 GITT (2nd cyc, 0.2 C 펄스 10 min + 이완 60 min, 3.0–4.3 V; Fig 4c,d + Fig S7)
- 과전압: NMC **49.3** / **WZO 97.7** / **BZOx 46.2 mV** — BZOx가 bare급, WZO는 2배.
- D_Li⁺: V_m·S 불확실성 때문에 **정규화 D_Li⁺·S²·V⁻²** 로만 비교(절대값 없음) — 충전 시 WZO 최저·NMC≈BZOx; 방전 시 3종 유사 → **WZO 병목은 σ_ion이 아니라 σ_e** 라고 저자 해석.

### 3.7 rate (Fig S5) — ⚠ 본문 주장과 SI 그래프 판독이 안 맞음
- **본문 텍스트**: "1.0 C에서 BZOx **~140** mAh g⁻¹ 유지 vs WZO **~115** 로 급락", BZOx의 rate 우위는 산소공공의 전자·이온 전도 촉진 덕. **pristine NMC는 rate 비교 문장에서 언급 자체가 없음.**
- **SI Fig S5 그래프 판독 (구판, ±5 mAh g⁻¹)**: 0.1C ~152/~127/~148 → 1C **~115(NMC)/~80(WZO)/~103(BZOx)** → 0.1C 회복 ~140/~115/~132. **전 구간 pristine 최고, BZOx 근접 2위.**
- 두 기록의 1C 절대값이 ~35 mAh g⁻¹ 어긋난다(§10-1). 안전한 인용 = "**BZOx는 WZO 대비 rate 우위, pristine 대비는 동급-이하**(코팅의 kinetic 비용 최소화)". 구판이 SI에서 기록한 1C=180 mA/g도 본문 정의(200)와 불일치 — 본문 200을 canonical로.

### 3.8 사이클 후 계면 화학 (ex situ XPS, 50 cyc @0.2 C; Fig 5a,b)
| 스펙트럼 | 피크 배정 | 결과 |
|---|---|---|
| S 2p | **S²⁻ 159.9** / PS₄³⁻ 161.5·162.7 / **폴리설파이드·산화종 163.7·164.5 eV** | pristine NMC: S²⁻ 감소(SE 산화) + 산화종 최다; WZO·BZOx 모두 산화종 억제 |
| P 2p | P₂S₅ 133.1·P₂Sₓ 133.9 / **POₓ 134.6·135.3 eV** | POₓ(phosphate 파편, 양극 O ↔ SE 부반응 산물)는 **pristine NMC에만 존재** — 코팅 2종 모두 SE 분해 완화 |

## 4. DFT/계산 방법 ★ (본문 §4.4 — 구판 "전부 n/a"에서 전면 교체)
| 항목 | 값 |
|---|---|
| code | **VASP** |
| functional | **GGA-PBE** + **DFT+U**(Dudarev): **Ni U=6.2, J=0** / **Zr U=5, J=1 eV** (vdW 보정 언급 없음) |
| pseudo | **PAW** |
| ecut | **520 eV** |
| k-points | **3×3×1**(이완) / **9×9×3**(전자구조), Monkhorst–Pack |
| 수렴 | SCF 10⁻⁴ eV; 힘 **<10⁻² eV/Å** (그러나 같은 절 말미엔 "<0.001 eV/Å" — 본문 내 불일치, §10-6) |
| 벌크 모델 | LiNiO₂: 40 Li/40 Ni/80 O · LPSCl: **F-43m**, 단위셀 24 Li/4 P/20 S/4 Cl (=4 f.u.; Materials Project 정합) — **4a/4d 무질서 처리 언급 없음 = 단일 ordered 배열** |
| 계면 모델 | **LiNiO₂(104) \| LPSCl(100)** 슬랩 3종: LNO-LPSCl **188원자** / WZO-LPSCl **176** / BZOx-LPSCl **152** |
| 코팅 모델 | WZO = 36 Zr + 72 O (**tetragonal P4₂/nmc**) / **BZOx = 36 Zr + 48 O → ZrO₁.₃₃ (x=0.67)** — 공공 배치·앙상블 방법 n/a |
| NMC 프록시 정당화 | LiNiO₂ 사용 이유를 명시 서술: 3.0–4.3 V에서 Ni가 O 2p 전자구조 지배, **Mn⁴⁺ 불활성·Co³⁺/Co⁴⁺는 더 고전압** → 표면 redox엔 Ni만 (refs 23, 30, 31 = Ceder surface-densified·Yoon boride 계열 관례) |
| 검증 | 최적화 구조의 XRD 패턴을 실험과 대조(정성) |
| 산출물 | **계면 S vs 격자(lattice) S 원자분해 pDOS** (E−E_F −5..+2 eV 창) + **이완 전후 결합길이**(S–O, Zr–S, P–Cl) |
| 없음 (n/a) | AIMD·NEB(본 논문)·Bader·COHP·grand-potential·계면 분해 ΔE·MLIP. **Li 이동장벽 BZOx 0.8 / WZO 1.4 eV는 선행논문(ref 23, JMCA 2024) 소환값** — 이 논문에서 계산한 게 아님 |

### DFT 결과 요지 (Fig 5c,d + Fig S8)
1. **결합길이**: LNO-LPSCl 이완 중 S–O **1.97→1.65 Å** 단축(양극 표면 O가 SE의 S를 포획), WZO-LPSCl S–O 2.02→1.74 Å = **SO₂ 기체 분해 산물 형성 시사**(ref 25 Ma/Janek). **BZOx-LPSCl은 Zr–S + P–Cl 상호작용** = 단순 SO₂ 방출 너머의 복잡한 계면 화학·**SO₂ 억제**.
2. **계면-S pDOS**: LNO-LPSCl = 계면 S 피크가 **E_F 직하**(불안정·산화 취약); WZO-LPSCl = **−1..−2 eV로 하강**(Zr 혼성 → S 안정화); BZOx-LPSCl = **Zr–S·S–O 상호작용 최강** → S-유발 열화 억제. ⚠ 구판(SI-only)은 "WZO도 E_F 직하"로 읽었으나 **본문 서사는 WZO도 전자적으론 S를 안정화**(WZO의 결격은 절연성·SO₂) — 본문 기준으로 교정.

## 5. Figure set ★
### 본문
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | Mechanofusion 3단계(전단대류→packing-milling→fusion) 모식도 + NMC/LPSCl 계면 만화: 비코팅 = **µ_Li⁺ 유발 ion-insulating space-charge layer**, BZOx = O 공공 경유 전하수송 | space-charge 완화 주장은 **모식도뿐, 직접 측정 없음**(§10-8). dry-coating 공정도 참고용 |
| 2 | HR-TEM 두께(9.7/8.1 nm)·EDS 맵·Zr 3d XPS(Zr⁽⁴⁻ˣ⁾⁺ 180.68 eV) | 산소공공의 표준 지문 세트(색·XRD 카드·Zr 3d shoulder·O 1s 533 eV) — 단 **x 정량은 없음** |
| 3 | 첫 사이클 전압곡선(ΔV 0.3/0.73/0.18 V)·초기 CE 막대(69.6/62.3/77.5 %)·100 cyc 사이클링 | **headline 성능의 원천.** SNMC 라벨 = 단결정 확정 |
| 4 | EIS Nyquist+등가회로(R_CA-SE 44.5/192.9/55.2 Ω)·GITT(과전압 49.3/97.7/46.2 mV·정규화 D_Li) | 코팅 kinetic 비용의 정량 분해(이온 vs 전자) 모범 — WZO 병목=σ_e 판정 논리 |
| 5 | 사이클 후 S 2p/P 2p XPS + **DFT 계면 구조·계면/격자 S pDOS**(LNO vs BZOx 본문, WZO는 S8) | **S 2p 자리분해(S²⁻/PS₄³⁻/산화종) = 우리 free-S vs PS₄-S site-PDOS의 실험 관측량 쌍**(§7) |
### SI (구판 승계)
| Fig | 내용 | 비고 |
|---|---|---|
| S1 | WZO/BZOx SEM·XRD(PDF 카드 00-065-0728 ZrO₂ vs **00-027-0997 ZrO₁.₈**)·분말 색 inset | 상 이름은 본문과 어긋남(§10-4); 카드 매칭 자체는 유효 |
| S2 | NMC 3종 입자 SEM (~5 µm 단결정, 코팅 후 표면 매끈) | 기계 손상·균열 없음 |
| S3 | O 1s XPS(Li₂CO₃ ~531.5 / TM-O ~529 / O_c 533.2 eV) | 공공 지문(정량 아님) |
| S4 | dQ/dV 1–100 cyc | WZO 지연 활성화 판독 근거 |
| S5 | rate 0.1→1C→0.1C | ⚠ §3.7 불일치 건 |
| S6 | DC 분극 σ_e 표 | §3.5 |
| S7 | GITT 원자료 | §3.6 |
| S8 | 계면 3종 구조+pDOS 전체(WZO-LPSCl 포함) | §4 |
| Table S1 | 코팅 전략 비교(절연 산화물 장벽 / 이온전도 ALD·PVD 고비용 / 본 연구 dry·charge-conductive·residue-free) | 자기 위치 선언(수치 없음) |

## 6. Post-processing ★
- **원자분해 pDOS** (계면 S vs 격자 S; VASP, −5..+2 eV 창, 관심영역 색 음영 — **음영 창 선택 기준·정량 지표는 여전히 없음**).
- **이완 전후 결합길이 추적** (S–O/Zr–S/P–Cl) → 분해 산물(SO₂) 형성 여부의 프록시로 사용 — 열역학 ΔE 없이 기하만으로 판정하는 방식(§10-7).
- NEB/Bader/COHP/grand-potential/ELF/AIMD = 없음. Li 장벽은 선행논문 소환.

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
> 이 논문 = **축 B③(양극 계면 레버 = CAM 코팅)**. intrinsic onset(축①) 논문 아님 — 축 명명 필수. 서론의 "sulfide SE HOMO 1.7–2.3 V vs Li/Li⁺ → 고전압서 산화"(refs 4, 5)는 **우리와 같은 Zhu/He/Mo 계열 인용** = 우리 grand-potential onset 2.256 V와 같은 전제에서 출발.

| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| **계면 S 전자상태 안정화 = 성공 지표** | 계면-S pDOS: LNO 계면 E_F 직하 → Zr-산화물 접촉 시 −1..−2 eV 하강 (PBE+U, 음영 정성) | **free-S site-PDOS ⟨3p⟩ −1.1 eV → B–S 결합 −2.15 eV** (−8..0 eV 창 고정, 정량) | **✓ 같은 관측량 패밀리** — "E_F 근처 S 3p를 밀어내리기". 그들=계면 접촉상, 우리=벌크 도핑. 같은 PBE 계열이라 정성 비교 가능하나 그들은 창·평균·수치 없음 → **우리 정량 프로토콜이 위** |
| **S 자리분해의 실험 쌍** | **XPS S 2p 분해: S²⁻ 159.9 / PS₄³⁻ 161.5·162.7 / 산화종 163.7·164.5 eV** (50 cyc 후) | free-S(4d) vs PS₄-S site-PDOS·xps_reference_sei.csv anchor | **✓✓ "어느 S가 먼저 산화되나"를 실험(XPS 자리분해)+계산(계면 pDOS) 양면으로** — 우리 서사의 외부 실험-계산 병행 사례 |
| **DFT 방법 재현성** | VASP·PBE+U(Ni 6.2/Zr 5)·PAW·520 eV·k 3×3×1→9×9×3·원자수 명시 = **골격은 재현 가능** | QE·PBE·fixed-occ nscf | 구판 "방법 0 공개"에서 대폭 개선. **남는 구멍**: LPSCl 4a/4d 무질서(단일 ordered), BZOx 공공 배치법, 슬랩 정합/변형률, 진공층, smearing → 계면 pDOS 재현은 반쯤만 가능 |
| 산화 관리 전략 | onset을 옮기는 게 아니라 **계면 반응을 코팅으로 관리**(B③) | onset 2.256 V(S²⁻-limited, 축①) + Nd/B 도핑 | ✓ [Banik] "치환으론 못 늘림 → 코팅 필요"의 코팅 측 실례. [Cha](할라이드 dual-compat)·[Kang25](SE 코팅 균일화)와 나란한 **제3 레버 = charge-conductive 산화물** |
| SE 산화 전제 | 서론 "sulfide SE 1.7–2.3 V vs Li/Li⁺, 고전압 산화" (Zhu/Mo 인용) | grand-potential onset 2.256 V | ✓ 같은 전제·같은 방법 계보 인용 — 수치 재계산은 안 함 |
| σ_e | 코팅 NMC 펠릿 10⁻⁴–10⁻⁶ S/cm | SE bulk anchor 10⁻⁸–10⁻⁹ | **물리량 다름 — 혼용 금지** |
| 무질서 처리 | LPSCl 단일 ordered F-43m 셀 | disorder ensemble·±0.2–0.3 eV 민감성 관리 | 그들의 계면 pDOS 피크 위치는 배열 의존 가능성 — 정성 인용까지만 |

### 🔑 [Sundar] ZrO₂-"실패" 판정과의 교차 분석 (본문 반영 갱신)
표면상 충돌([Sundar]: ZrO₂ 실패 — SE 입자 ALD 코팅, Zr₃O/Li₆Zr₂O₇ Li-절연 장벽 1.4 eV·σ_e×2 vs 이 논문: ZrO₂₋ₓ 성공)이지만 **모순이 아니라 상보**:
1. **코팅 대상이 반대 → 요구 물성이 반대**: SE 입자 코팅(Sundar)의 선 = 전자 절연 + Li 전도 / CAM 입자 코팅(이 논문)의 선 = 전자·이온 모두 전도. "ZrO₂ 좋다/나쁘다"는 **무엇을 코팅하는지 없이는 무의미** — 이 대구는 본문의 설계 논리(E_g<0.5 eV 코팅은 SE 분해 촉진 ← Xiao/Ceder ref 11)로 **저자들 스스로도 인지**: BZOx의 셀링포인트가 "적당히만 전도(0.5–2.25 eV)"라는 창 논리.
2. **화학양론 축은 상호 지지**: Sundar의 실패 기전(환원 Zr 산화물 Zr₃O = 금속성)이 이 논문의 전제(산소결핍 = 전도성)를 독립 확인. 이 논문 내 stoich WZO 실패(σ_e ÷25.5·ΔV 0.73 V)도 Sundar의 stoich-ZrO₂ 부정과 나란(기전은 다름: Li-절연 산물 vs 전자 절연 장벽).
3. **⚠ 남는 진짜 질문 — 본문에서도 미해결**: BZOx가 LPSCl과 **화학 분해**(Zr₃O·Li₆Zr₂O₇ 형성)를 안 하나? 본문 DFT는 정적 슬랩 pDOS+결합길이뿐, **분해 열역학 ΔE·산물 계산 없음**. 오히려 이완 중 **Zr–S 결합이 형성**된다는 것 자체가 계면이 화학적으로 활성이라는 뜻(저자들은 "안정화"로 프레임). 게다가 DFT 모델은 **ZrO₁.₃₃(x=0.67)** — XRD ZrO₁.₈(x≈0.2)의 3배 공공 농도로, 반응성을 실제보다 과대/과소 어느 쪽으로든 왜곡 가능. → **우리 interface_reactivity(Zr hull 추가 시)로 in-silico 판정 가능한 열린 질문** 유지.

## 8. 적용 인사이트
1. **계면 S pDOS 정량화 = 우리 기여 기회 (구판 유지·강화)**: 이 논문이 음영으로만 보인 "계면 S 하강"을 우리 slab 파이프라인(verified-carry + local-TF 믹싱)으로 LPSCl|코팅 계면에서 **⟨3p⟩ 중심을 −8..0 eV 창 정량**하면, 벌크 free-S(−1.1)·B–S(−2.15 eV)와 같은 자로 계면까지 잰 수치 서열이 된다. 이제 그들 방법(PBE+U·520 eV·(104)|(100))이 공개됐으므로 **직접 재현·반박·확장이 가능**해짐.
2. **"코팅의 선악은 코팅 대상이 정의" (B③ 명문화)**: [Sundar](SE: σ_e↓ 선) ↔ 이 논문(CAM: σ_e 보존 선). B③ 레버 3종([Cha]/[Kang25]/[BZOx])에 "코팅 대상 + 요구 σ_e 방향" 변수 등재 완료(comparison B③ 행).
3. **XPS S 2p 자리분해 = free-S 서사의 실험 관측량**: S²⁻(159.9) vs PS₄³⁻(161.5·162.7) vs 산화종(163.7+)의 사이클-후 소장 추적은 우리 "free-S가 먼저 산화" site-PDOS 예측을 검증할 표준 실험 포맷 — 우리 xps_reference_sei.csv와 결 맞춤.
4. **산소공공 gap-state 엔지니어링의 역방향(구판 유지)**: 우리 O-doping(LPSOCl 2.2309 eV, O 2p 매몰)은 산화물 성분을 넣어 안정화, 이들은 산화물에서 O를 빼서 전도 확보 — "결함/조성이 gap-state·σ_e 지배"의 양면.

## 9. 인용 가능 문장 (deck/paper용)
- "Choi et al. (Small 2026) applied a dry-mechanofusion ZrO₂₋ₓ shell (~8 nm) on single-crystalline NMC811, retaining cathode electronic conduction (σ_e ÷3.8 vs ÷25.5 for stoichiometric ZrO₂) and cutting first-cycle irreversible loss (45.8 vs 67.5 mAh g⁻¹) and voltage hysteresis (0.18 vs 0.30 V) against LPSCl — reframing cathode coatings from 'insulating barrier' to 'charge-conductive interface stabilizer'."
- "Their interface-S pDOS criterion (interfacial sulfur states at E_F for bare NMC|LPSCl, pushed to −1..−2 eV under Zr-oxide contact; VASP PBE+U) is the interfacial analogue of our quantitative free-S site-PDOS descriptor (⟨3p⟩ −1.1 → −2.15 eV upon B–S bonding)."
- "Taken together with Sundar et al. (Adv. Sci. 2025), the ZrO₂ verdict is target-dependent: on the *electrolyte*, oxygen-deficient/metallic Zr suboxides are the failure mode (electron leakage); on the *cathode*, the same oxygen-vacancy conductivity is the design feature — Choi et al.'s own band-gap window argument (0.5 < E_g < 2.25 eV) concedes exactly this trade-off."

## 10. 주의/한계 (over-claim 방지)
1. **⚠⚠ rate 수치 불일치**: 본문 "1C에서 BZOx ~140 vs WZO ~115 mAh g⁻¹"는 우리 SI Fig S5 판독(NMC ~115 / WZO ~80 / BZOx ~103)과 ~35 mAh g⁻¹ 어긋나고, **본문은 rate 비교에서 pristine을 아예 언급 안 함**(그래프상 pristine 최고). 1C 정의도 본문 200 vs 구판 SI 기록 180 mA g⁻¹. rate 인용은 "BZOx > WZO, pristine 대비 동급-이하"까지만.
2. **유지율 % 프레이밍**: 최고 유지율은 WZO(85.8 %)다. BZOx(80.4 %)의 승리는 절대용량·CE·hysteresis. 결론부 "achieved an improvement of 80.4 % in capacity retention"은 오독 유발 문구.
3. **DFT BZOx 모델 = ZrO₁.₃₃**: 실험 지문(XRD ZrO₁.₈ 카드, x≈0.2)의 **3배 산소결핍**. 공공 배치·앙상블 n/a. pDOS 결론이 공공 농도에 얼마나 민감한지 미검증.
4. **상 배정 혼선**: 본문 "BZOx monoclinic 단상 / WZO mono+tetra 혼상" vs SI Fig S1 우리 판독(BZOx tetragonal 단상·ZrO₁.₈ 카드) vs **DFT WZO 모델 = tetragonal P4₂/nmc**(본문 실험 WZO는 혼상이라며). 상-모델 정합이 성글다 — 상 이름 인용 시 원문 재확인.
5. **BZOx|LPSCl 분해 열역학 미검증**: 정적 pDOS+결합길이뿐(ΔE·산물·AIMD 없음). Zr–S 결합 형성은 "안정화"와 "반응성"의 양날 — [Sundar]-류 Zr₃O/Li₆Zr₂O₇ 경로는 여전히 열린 질문. "DFT가 BZOx 안정성을 증명"은 과대, "계면 S 상태 하강 + SO₂ 경로 억제를 시사"까지.
6. **본문 내 수렴 기준 모순**: 힘 수렴 "<10⁻² eV/Å"와 "<0.001 eV/Å"가 같은 §4.4에 공존. 원자수 합산도 슬랩 구성 세부(진공·정합) 없이는 재구성 불가.
7. **Li 장벽 0.8 eV는 소환값**: BZOx 0.8 / WZO 1.4 eV는 선행논문(ref 23) 결과이며, 0.8 eV도 절대값으론 높은 장벽(8 nm 초박막이라 통과 가능하다는 암묵 논리). 이 논문에서 재계산 안 함.
8. **space-charge layer 완화는 모식도 주장**: Fig 1 만화 외 직접 관측 없음.
9. **산소결핍 x 정량 부재**: Zr⁽⁴⁻ˣ⁾⁺ shoulder·색·카드 매칭뿐(XPS 면적비·TGA·EPR 없음).
10. **σ_e 혼용 금지**: §3.5 주석 — 양극 펠릿 값이지 SE bulk 값 아님.
11. LPSCl **단일 ordered 배열**: 4a/4d 무질서 미처리 — 계면 pDOS 피크 위치는 배열 의존 가능(우리 gap 규율 ±0.2–0.3 eV 민감성과 같은 계열).

## 11. 기법 용어 미니사전 (구판 승계)
- **Mechanofusion (dry coating)**: 고속 회전 챔버의 전단·압축력으로 게스트 나노입자를 호스트 입자 표면에 무용매 융착. 여기선 Hosokawa Nob-Mini, 1 mm 간극, 2단 rpm — ALD(기체·~nm conformal)와 달리 용매·후어닐 불필요. [Kang25] dry-coating과 같은 계열.
- **Black ZrO₂₋ₓ**: 산소공공 gap-state(Zr³⁺/공공 준위)로 가시광 전영역 흡수(검정)+전자전도 — "black TiO₂"류 defect engineering의 Zr판. 여기선 PVP-보조 열분해+H₂ 환원 어닐로 합성.
- **DC polarization (σ_e)**: 이온 차단 조건 정전압(여기선 200 mV, 30 °C) → 정상상태 전류로 전자전도 분리. σ_e = L/(R·A).
- **GITT**: 전류 펄스+휴지 반복으로 열역학 전위(ΔE_s)와 과전압(ΔE_τ) 분리 → D_Li 산출; 여기선 V_m·S 불확실성 때문에 정규화 D·S²·V⁻² 사용.
- **dQ/dV**: 전압별 미분용량 — 상전이 피크 이동/감쇠로 분극 성장·(WZO의) 지연 활성화 추적.
- **O 1s O_c (533.2 eV)**: 산소공공 자리 흡착 OH⁻/O₂ 계열 지문(정량 아님).
- **space charge layer**: 산화물 양극/황화물 SE 접촉 시 µ_Li⁺ 차이로 Li⁺가 재분포해 생기는 이온 결핍층 — 여기선 코팅 정당화 프레임(직접 측정 없음).
