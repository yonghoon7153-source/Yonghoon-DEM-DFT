# Electron Redistribution Enables Redox-Resistible Li₆PS₅Cl towards High-Performance ASSLBs — Liu et al. (Angew. Chem. Int. Ed. 2023)

> slug `liu2023_electron_redistribution_redox_resistible_mgf2` · DOI `10.1002/anie.202302655` · type `exp + DFT(VASP/PBE)` · PDF `da9a7f39…Electron_Redistribution…pdf` (+ SI `6488e8eb…`) · digested `2026-06-23` · status ✅
> **저자**: Chong Liu, Butian Chen, **Tianran Zhang***, Jicheng Zhang, Ruoyu Wang, Jian Zheng, Qianjiang Mao, **Xiangfeng Liu*** (Center of Materials Science & Optoelectronics Eng., **University of Chinese Academy of Sciences (UCAS)**, Beijing) · Angew. Chem. Int. Ed. **62** (2023) e202302655 · Received 21 Feb / Accepted 29 Mar 2023

---

## 0. 이 digest를 읽는 법 (핵심 + litdb 내 위치)
이 논문의 핵심 주장: **LPSCl의 PS₄³⁻ 사면체가 Li 금속에 *전자를 빼앗겨* 분해(→Li₂S+Li₃P)하는 게 음극 불안정의 근원**이다. 그러면 **PS₄의 전자구조를 바꿔 전자를 못 주게(redox-resistible) 만들자**가 해법. **Mg+F 공도핑(=MgF₂)** 으로: ① **Mg가 P를 치환(MgS₄ 사면체)** → Mg(3s)–S(3p) **s–p 혼성**으로 S 주위 전자를 풍부하게 → Li로의 전자이동 차단(PS₄ gap ~2.0→MgS₄ ~4.2 eV); ② **F가 Cl을 치환** → 충방전 중 계면에 **LiF self-limiting 층**(고계면에너지·전자절연) 형성 → dendrite 억제. 결과 **LPSC-MF = Li₆.₃P₀.₉Mg₀.₁S₅Cl₀.₈F₀.₂**, CCD 1.4 mA cm⁻²(2.3×), 대칭셀 1800 h, LCO‖Li 93.3 %@100cyc.

> 🔗 **litdb 내 위치**: 이건 **음극·환원·도핑 축**으로, **[Ke] MgClO 논문과 같은 패밀리**(둘 다 Mg + s-p 혼성으로 S 주위 전자 풍부화 → Li 전자이동 차단). → **우리 cascade(Mg/Cl/O/F 도판트 스크리닝)의 두 번째 직접 문헌 동기.** [Ke]는 MgClO, 여기는 MgF₂.

## 1. 한 줄 요약
PS₄³⁻의 Li-유발 redox 분해가 음극 불안정의 근원 — **Mg(P 치환, s-p 혼성으로 전자이동 차단) + F(Cl 치환, in-situ LiF 절연층)** 공도핑으로 LPSCl을 **redox-resistible**하게 만들어 CCD 0.6→**1.4 mA cm⁻²(133 %↑)**, 대칭셀 90 h→**1800 h**, σ_e **8×↓**, LCO‖Li **93.3 %@100cyc(0.2C)** 달성.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 조성 | base = LPSC(Li₆PS₅Cl); 도핑 = **Li₆₊₃ₓP₁₋ₓMgₓS₅Cl₁₋₂ₓF₂ₓ** (x=0/0.1/0.2/0.3); **최적 x=0.1 = Li₆.₃P₀.₉Mg₀.₁S₅Cl₀.₈F₀.₂ = "LPSC-MF"** |
| 주제 | **음극(Li metal) redox 저항성** (전자구조 변조) — Cl-rich가 아니라 *도핑* 전략 |
| 핵심 메커니즘 | (a) **Mg→P(4b) 치환, MgS₄ 사면체, Mg(s)-S(p) 혼성** → S 주위 전자 풍부 → Li 전자이동 차단; (b) **F→Cl 치환 → in-situ LiF 절연층**(고계면에너지) |
| 동기 | 황화물 SE는 Li 환원 시 PS₄³⁻(공유 P-S, 2p-2p 혼성)가 친핵성 Li에 전자 빼앗겨 분해 → Li₂S+Li₃P(혼합 이온-전자 전도체) → 계속 분해·dendrite. **PS₄의 redox 활성 자체를 억제**하는 SE는 거의 미연구 |

## 3. 핵심 물성 (수치 총정리)
| 물성 | LPSC-MF (x=0.1) | LPSC (pristine) | 조건 / 출처 |
|---|---|---|---|
| **이온전도도 σ** | **1.70 mS cm⁻¹** (Mg-only면 3.51) | 2.91 mS cm⁻¹ | 25 ℃ EIS, Fig 2c (F가 σ 낮춤: F-Li 정전기↑) |
| 활성화E Ea | **0.32 eV** | 0.30 eV | Arrhenius, Fig 2c (거의 동일) |
| **전자전도도 σ_e** | **1.03×10⁻⁹ S cm⁻¹** | **8.16×10⁻⁹ S cm⁻¹** (≈8× 높음) | DC 분극, Fig 2d |
| **CCD** | **1.4 mA cm⁻² (133 %↑)**; 50 ℃ **5.2 (5.2×)** | 0.6 mA cm⁻²서 단락 | 25 ℃, Fig 3a/S12 |
| 대칭셀 수명 | **>1800 h @0.1 (η 8.3 mV)**; 1000 h @0.5 | ~90 h서 단락 (η 7.5 mV) | Fig 3b,g |
| 격자상수 a / V | **9.86266 Å / 969.711 Å³** | 9.85128 Å / 956.047 Å³ | Rietveld (팽창=Mg 큰 반경) |
| R_p / R_wp | 7.27 / 8.95 % | 5.56 / 8.36 % | Fig 1a,b |
| **PS₄ vs MgS₄ "gap"(전자이동)** | **MgS₄ ~4.2 eV** (Mg-s/S-p) | **PS₄ ~2.0 eV** (P-p/S-p) | PDOS, Fig 5e,f,g |
| Mg 자리 선호 | **P(4b) ΔE=−1.20937** < Li(48h) −1.20363 eV/atom | — | DFT, Fig S2 |
| 풀셀 LCO‖Li 1차방전/CE | **113.0 mAh g⁻¹ / 92.6 %** | 82.9 / 85.5 % (40cyc후 단락) | 0.1C, Fig 6b,c |
| 풀셀 유지율 | **92.2 %@100cyc(0.1C); 93.3 %@100cyc(0.2C); 86.2 %@0.5C** | 급락 | Fig 6c,f |
| 율속 | **121.8/112.9/105.2/94.2/84.3 mAh g⁻¹** (0.05–1C) | 0.5C서 붕괴 | Fig 6d |

## 4. DFT/계산 방법 ★ (SI p.3)
- **code**: VASP · **functional**: GGA-PBE · **pseudo**: PAW
- **ecut**: **400 eV** (plane-wave)
- **smearing**: **1차 Methfessel-Paxton, width 0.2 eV** (← 절연체에 0.2 eV는 다소 큼; E_F·gap은 정성적)
- **dipole correction**: z 방향(계면 slab)
- **k-points**: **3×3×3** (우리·GG·Lu보다 조밀 — slab인데 3×3×3은 비교적 촘촘)
- **수렴**: SCF **10⁻⁵ eV**, 힘 **<0.03 eV/Å**
- **supercell/도핑**: **2×2×1 LPSCl supercell**에 **1 Mg + 2 F를 1 P + 2 Cl 자리에 치환** (= x=0.1 모형). Li/LPSC, Li/LPSC-MF 계면 slab.
- **무질서 처리**: 명시적 SQS 아님 — 단일 치환 배열 + 계면.

> 방법 한계(정직): **MP smearing 0.2 eV**는 절연체엔 큼 → "gap ~2.0/~4.2 eV"는 **PDOS상 전도대-가전자대 분리 추정치**(엄밀 band gap 아님). 우리 comp1 gap 2.066과 LPSC ~2.0이 우연히 잘 맞지만 **절대 비교는 주의**.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| Scheme 1 | LPSC(PS₄ redox→Li₂S/Li₃P/dendrite) vs LPSC-MF(억제) | 음극 분해 메커니즘 모식 |
| 1a,b | XRD Rietveld (LPSC vs LPSC-MF, F-43m) | a 9.851→9.863 Å 팽창 |
| 1c | 결정구조 (P/Mg 4b, Cl/S/F 4a/4d) | **F가 음이온 자리(4a/4d), Mg가 P자리(4b)** |
| 1d | SEM/EDS (P,Mg,S,Cl,F 균일분포) | Mg·F 고용 확인 |
| 1e | 농도별(x=0–0.3) XRD + 피크이동 | x>0.1서 불순물(Li₂S/LiCl/Li₄P₂S₆) |
| 2a,b | Nyquist + Arrhenius | σ·Ea |
| 2c | σ·Ea vs x | x=0.1이 σ·dendrite 최적 |
| **2d** | **σ_e (DC분극): LPSC 8.16e-9 vs LPSC-MF 1.03e-9** | **bulk σ_e 기준값 + 8×↓** |
| 3a | CCD (LPSC 0.6 단락 vs LPSC-MF 1.4) | 음극 안정성 핵심 |
| 3b–g | 1800 h plating/stripping, 시간분해 EIS | 장기 안정 |
| 4a | **CV (반차단셀)**: LPSC 2.4 V(ox)/0.8 V(red)/<0.5 V(Li 환원) vs LPSC-MF 억제 | redox-resistible 정량 |
| 4b,c | **ex-situ Raman**: LPSC Li₂S 493.8 cm⁻¹ 성장 vs LPSC-MF 무 | 분해 억제 직접증거 |
| 4d,e | XPS S2p(Li₂S 160.3)·P2p(Li₃P 130.5): LPSC-MF 무 | 계면 분해산물 없음 |
| 4f | **F1s: in-situ LiF 684.7 eV (etch↑ 증가)** | LiF 절연층 형성 |
| 4h,i | 단락후 Li 표면: LPSC mossy / LPSC-MF smooth | dendrite 억제 |
| **5a,b** | Li/LPSC(PS₄ 분해) vs Li/LPSC-MF(MgS₄ 무분해) 계면 | 원자수준 분해/무분해 |
| **5c,d** | **ELF**: LPSC P-S 공유 / LPSC-MF Mg→S 전자 재분포 | ELF 활용 예 (O 아닌 Mg) |
| **5e** | **PDOS**: LPSC(P-p,S-p @E_F) vs LPSC-MF(Mg-s,S-p; S 도전대 +shift) | s-p 혼성 직접증거 |
| 5f,g | 전자이동 모식 ΔE: PS₄ ~2.0 / MgS₄ ~4.2 eV | gap 확대 = 전자이동 차단 |
| 5h | redox 과정: PS₄+Li→분해 / MgS₄+Li→무분해 | 메커니즘 종합 |
| 6 | 풀셀 LCO‖Li (113 mAh/g, 93.3 %@100cyc) | 응용 성능 |

## 6. 결과 — 섹션별 상세

### 6.1 구조: Mg→P(4b), F→Cl(4a/4d) (Fig 1)
- LPSC-MF = **Li₆.₃P₀.₉Mg₀.₁S₅Cl₀.₈F₀.₂** (x=0.1). XRD Rietveld → cube argyrodite **F-43m**, PDF#34-0688. **a 9.85128→9.86266 Å, V 956.047→969.711 ų** (Mg가 P보다 큰 이온반경 → 격자 팽창, Bragg 법칙으로 피크 저각 이동).
- ⁷Li MAS NMR: 단일 peak, 위치 이동 없음(Fig S1) → 두 시료 Li 환경 동일, Mg·F 성공적 고용.
- **DFT 자리선호(Fig S2)**: Mg at Li(48h) ΔE=−1.20363/−1.20243 vs Mg at **P(4b) −1.20937 eV/atom**(최저) → **Mg는 P 자리 선호** (XRD와 일치).
- 농도 시리즈: x>0.1(>10 % 도핑)서 불순물(Li₂S/LiCl/Li₄P₂S₆/미지상) — 용해도 한계. x=0.3서 P₂S₆⁴⁻ Raman ~384.6 cm⁻¹.

### 6.2 전도도: σ는 약간↓, σ_e는 8×↓ (Fig 2)
- σ: LPSC **2.91 → LPSC-MF 1.70 mS cm⁻¹**(약간↓). **F 도핑이 σ를 낮춤**(F-Li 정전기 인력 > Cl-Li). 단 **Mg만 도핑하면 3.51 mS/cm**(Li⁺ 농도↑·채널 확장). → 둘 합쳐 적정 도핑서 고σ 유지. Ea 0.30→0.32 eV(거의 무변).
- **σ_e(Fig 2d, DC분극)**: LPSC **8.16×10⁻⁹ → LPSC-MF 1.03×10⁻⁹ S cm⁻¹ (≈8× 낮음)**. 낮은 σ_e → dendrite 억제. **(우리 slide25 σ_e 논의의 실측 bulk 기준값으로 인용 가능)**

### 6.3 음극 안정성: CCD·장기 cycling (Fig 3)
- **CCD**: LPSC는 0.6 mA cm⁻²서 비가역 강하(단락). LPSC-MF는 **1.4 mA cm⁻²(1.4 mAh cm⁻²)서도 안정 (133 %↑)**. LiF층(고계면에너지+저σ_e)이 원인. x=0.2/0.3보다 x=0.1 우수(σ 때문). **50 ℃서 5.2 mA cm⁻²(5.2×)**, 보고된 황화물 중 최상위(<3.0).
- 장기(Fig 3b): LPSC η 7.5 mV, ~90 h서 급강(단락). LPSC-MF **>1800 h, η 8.3 mV 안정**. Fig 3g: 0.5 mA cm⁻² 1000 h.

### 6.4 redox-resistible 직접 증거 (Fig 4)
- **CV(반차단셀)**: LPSC ~2.4 V(산화 PS₄³⁻)·0.8 V(환원), <0.5 V서 Li 환원전류(→Li₃P/Li₂S/LiCl). LPSC-MF는 2.4/0.8 V 전류 + <0.5 V 환원전류 **모두 크게 감소** → redox-resistible.
- **ex-situ Raman(LCO/SE/Li)**: LPSC는 2.8 V 충전부터 **Li₂S 493.8 cm⁻¹** 등장·성장. LPSC-MF는 전 전압서 **무시 가능** → 분해 억제.
- **XPS**: LPSC 계면 S2p **Li₂S 160.3 eV** + P2p **Li₃P 130.5 eV** 신규. LPSC-MF는 cycling 후에도 **Li₂S/Li₃P 신호 없음**. Li1s: LPSC는 Li-SSE+LiCl(56.0 eV), LPSC-MF는 **in-situ LiF(54.8)** + Li-SSE(55.6).
- **F1s(Fig 4f)**: Li/LPSC-MF 계면 **LiF 684.7 eV**, etch 깊이↑ 따라 증가 → in-situ LiF 절연층.
- SEM(4h,i): 단락후 LPSC=Li-sulfide mossy 응집 / LPSC-MF=매끈.

### 6.5 DFT: 왜 redox-resistible인가 (Fig 5)
- **계면 slab(5a,b)**: Li/LPSC — PS₄가 Li와 만나 **붕괴**(Li-S 형성, P-S 파괴 → Li₂S). Li/LPSC-MF — **MgS₄는 무분해**(Mg가 S-Li 상호작용 억제).
- **ELF(5c,d)**: LPSC는 P·S 주위 전자(PS₄ 공유). LPSC-MF는 **Mg→주변 S로 전자 재분포**.
- **PDOS(5e)**: LPSC는 **P 2p·S 2p가 E_F 근처**(p-p 혼성 → PS₄ 지배), 전도대-가전자대 분리 **~2.0 eV** → P·S 전자이동 쉬움 → 친핵성 Li가 S에 전자 줘 PS₄ 파괴. LPSC-MF는 **Mg s밴드 + S p밴드가 E_F**, S 밴드 대부분 E_F 아래, S 도전대 **양의 이동 + gap ~4.2 eV** → **s-p 혼성이 S 주위 전자 풍부화 → Li→S 전자이동 차단**.
- **Mg는 P 전자구조 자체는 안 바꿈**(Fig S22 P p-band ≈ LPSC, ELF P-S 공유 동일) → **redox 저항성은 Mg에 의한 *전자 재분포*에서 기인**(PS₄ 고유 전자구조 변조).

### 6.6 풀셀 (Fig 6)
- LCO/LPSC-MF/Li: **113.0 mAh g⁻¹·CE 92.6 %**(0.1C). 100cyc **92.2 % 유지**(0.077 %/cyc). **93.3 %@100cyc(0.2C), 86.2 %(0.5C)**. 율속 0.05–1C서 121.8→84.3 mAh g⁻¹. LCO/LPSC/Li는 82.9 mAh/g·CE 85.5 %, **40cyc후 단락**.

## 7. 전체 논증 흐름
Scheme1(PS₄ redox가 문제) → Fig1(Mg→P, F→Cl 구조) → Fig2(σ 약간↓이나 σ_e 8×↓) → Fig3(CCD 1.4, 1800h) → Fig4(CV·Raman·XPS·F1s: 분해억제 + LiF층) → Fig5(DFT: Mg s-p 혼성이 전자이동 차단 + MgS₄ 무분해) → Fig6(풀셀).

## 8. Post-processing ★
- **XRD Rietveld**(Fullprof) → 격자상수·자리·불순물.
- **DC 분극** → **σ_e**(핵심 descriptor).
- **CV(반차단셀)** → redox 전류 정량.
- **ex-situ Raman**(532 nm) → Li₂S 493.8 cm⁻¹ 추적.
- **XPS depth profiling**(ESCALAB 250Xi) → 계면 Li₂S/Li₃P/LiF/LiCl.
- **DFT**: 계면 slab 분해/무분해, **ELF**(전자 국재), **PDOS**(s-p vs p-p 혼성, gap), 자리선호 ΔE.

## 9. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
| 항목 | Liu 2023 | 우리 | 차이 / 이유 |
|---|---|---|---|
| base 분해 (Li 환원) | LPSC → **Li₂S + Li₃P (+LiCl)** | comp1 0V → **Li₃P+Li₂S+LiCl** | **✓ 동일 chemistry** |
| LPSC "gap" | PS₄ ~2.0 eV (PDOS 분리) | comp1 2.066 (PBE band gap) | 우연 일치(정의 다름·MP smear 0.2) — 절대비교 금지 |
| **σ_e (bulk)** | **LPSC 8.16×10⁻⁹ S cm⁻¹** | 우리 미측정(slide25 논의) | **우리 σ_e 논의의 실측 기준값** |
| 전략 | **Mg(P)+F(Cl) 도핑** → 전자구조 변조 | 우리 modelc = Cl-rich(무도핑) | 다른 레버 (도핑 vs 조성) |
| DFT setup | VASP/PBE, 400 eV, 3×3×3 k, 2×2×1 sc | VASP/PBE, bulk+AIMD | 큰 틀 동일, 우리가 더 정밀(k·U·LOBSTER) |
| 도핑 자리 | Mg→P(4b), F→Cl(4a/4d) | (우리 cascade 도판트 자리 결정에 참고) | — |

## 10. 적용 인사이트 (내 연구에 어떻게)
1. **cascade의 두 번째 문헌 동기([Ke]와 쌍)**: [Ke](MgClO)·[Liu](MgF₂) 둘 다 **Mg + s-p 혼성으로 S 전자 풍부화 → Li 전자이동 차단**. → 우리 **Mg/Cl/O/F 도판트 스크리닝**이 "임의 선택"이 아니라 **두 Angew/ESM 논문이 독립 검증한 방향**임을 deck에 명시 가능.
2. **descriptor 차용**: redox 저항성 = (a) **PDOS gap 확대**(2.0→4.2), (b) **σ_e 감소**(8×), (c) **ELF상 S 전자 풍부화**, (d) 계면 slab **무분해**. → 우리 cascade 평가지표 세트(Ke binding-E, Lu gap·Li⁺장벽·Poisson과 묶기).
3. **σ_e 기준값**: slide25(전자전도) 논의에 **LPSC bulk σ_e = 8.16×10⁻⁹ S cm⁻¹**(실측) 인용. 도핑으로 1.03×10⁻⁹까지 낮춤 = "σ_e는 도핑/defect로 조절"이라는 우리 논지(defect-controlled) 보강.
4. **우리 환원 산물 해석**: 우리 comp1 0V → Li₃P+Li₂S+LiCl = Liu가 "음극 불안정의 분해산물"로 지목한 바로 그것 → "왜 음극 보호가 필요한가"의 근거.
5. **ELF 활용 사례 추가**: 사용자 ELF 질문(같은 조성서 ELF 보는지/언제 쓰나)에 대한 또 다른 답 — **도핑 전후 같은 골격(MgS₄ vs PS₄)에서 ELF로 전자 재분포 시각화**. [Ke](결합E)·[Liu](전자국재) 두 ELF 용례.

## 📝 서술용 motivation 문단 (한글 — 논문 intro 기반, deck/thesis 재사용)
> 이 논문 intro(p.1, Scheme 1 직전)의 핵심 동기를 한글로 정리한 문단. citation 표시 [5][6][7]은 **이 논문(Liu 2023)의 자체 reference 번호** (재번호 금지 — thesis에 옮길 땐 본인 ref로 교체).

그러나 sulfide-SE의 실용화에 있어 핵심적인 한계 중 하나는 금속 Li 전극에 대한 낮은 (전기)화학적 안정성이다.[5] Sulfide-SE는 친핵성(nucleophilic) Li 금속에 의해 전기화학적으로 환원되기 쉬우며, Li/sulfide-SE 계면에서 이온-전자 혼합전도성 계면상(mixed ion-electron conducting interphase; Li₂S, Li₃P 등)을 생성한다.[6] 이 제어 불가능한 기생 계면반응(parasitic interfacial reaction)은 sulfide-SE의 지속적인 분해를 유발하고, sulfide-SE 표면 또는 내부로의 리튬 덴드라이트 성장을 촉진하여 전지의 사이클 성능을 저하시킨다.[7]

> 영문 원문(대조): "one of the critical limitations for the practical applications of sulfide-SE is their poor (electro)chemical stability towards metallic Li electrode.[5] The sulfide-SE is prone to electrochemical reduced by nucleophilic Li metal, generating the mixed ion-electron conducting interphases (Li₂S, Li₃P, etc.) at the Li/sulfide-SE interface.[6] This uncontrollable parasitic interfacial reaction causes the continuous decomposition of sulfide-SE and promotes the lithium dendrites growth into or inside the sulfide-SE, which deteriorates the battery cyclic performances.[7]"

### [11]→[12] 문단 (intro 후반 — PS₄³⁻ redox 가설 + 본 연구 동기)
> citation [11][12]은 **이 논문(Liu 2023) 자체 reference 번호** (thesis 옮길 땐 본인 ref로 교체).

실험과 계산에 근거할 때, Li/sulfide-SE에서의 계면 기생반응(interfacial parasitic reaction)은 sulfide-SE 내 PS₄³⁻ 사면체(tetrahedron)와 Li 금속 간의 자발적이고 비가역적인 산화환원 반응(spontaneous irreversible redox reaction)에서 비롯되는 것으로 추정되며(Scheme 1),[11] 이는 전해질의 구조적 붕괴(structural collapse)와 분해를 야기한다. PS₄³⁻ 사면체는 공유결합성 P–S 결합(2p–2p 오비탈 혼성화)으로 구성되어 있어, 전자가 풍부한(electron-rich) Li 원자에 의해 쉽게 공격받아 Li–S 및 Li–P 상호작용을 생성한다. 그 결과 생성되는 분해 산물 — 전자전도성(electron-conducting) Li₂S와 불규칙한(irregular) Li₃P를 포함 — 은 Li/전해질 계면에서 지속적이고 심각한 열화를 초래한다.[12] 이러한 맥락에서, 우리는 sulfide-SE의 계면 안정성 향상이 PS₄³⁻ 사면체의 산화환원 활성(redox activity)을 억제하는 데 달려 있을 수 있다고 추정한다. 그러나 우리가 아는 한, 산화환원 특성을 조절하여 산화환원 저항성(redox-resistible) sulfide-SE를 구축하는 연구는 거의 수행된 바 없으며, 여전히 큰 도전 과제로 남아 있다.

## 🔑 [5]→[7] 문제의 메커니즘 (anode 환원 불안정 → MIEC → non-self-limiting)
> 위 motivation 문단의 메커니즘을 단계로 분해. **핵심 문제는 양극이 아니라 *음극(Li metal)* 쪽 환원 불안정성.**

**문제 제기**: sulfide-SE의 핵심 한계 = **Li metal에 대한 환원 불안정성** (← anode가 문제). 메커니즘이 명확:

1. **Li metal = 강한 친핵체(nucleophile)** → S에 전자를 밀어넣음 (electron donation to S)
2. → **sulfide-SE가 환원 분해** → **Li₂S, Li₃P** 같은 **MIEC(mixed ion-electron conductor, 혼합 이온-전자 전도) 계면상** 생성
3. → 이 MIEC 계면상은 **self-limiting이 안 됨** — *전자전도성*이라 전자가 계면상을 통과해 SE로 계속 공급됨 → **반응이 멈추지 않고 진행** → 리튬 **덴드라이트 성장** → **사이클 열화**

> **🔗 litdb 통합 통찰 (self-limiting의 조건)**: 해법의 본질 = **MIEC 계면상을 *전자절연* passivation으로 바꾸기**. 전자절연이면 전자 공급이 끊겨 반응이 스스로 멈춤(self-limiting). litdb의 음극 논문들이 전부 이 원리:
> - **[Liu23] (본 논문)**: Mg(s-p 혼성)로 전자이동 차단 + **LiF**(전자절연) interphase
> - **[Lu]**: 4d-Cl 자기분해 → **LiCl**(gap 6.22 eV, 전자절연) interphase
> - **[Ke]**: MgClO 도핑 → **Li₂O**(8.37 eV) 전자절연 SEI
> → 즉 "음극 안정 = 계면상이 *전자절연*이라 self-limiting 되느냐"가 단일 판정 기준. (Li₂S/Li₃P = MIEC = 실패 / LiF·LiCl·Li₂O = 절연 = 성공). 상세 `../comparison_vs_ours.md` §E.

## 11. 인용 가능 문장 (deck/paper용)
- "The anode-side instability of LPSCl originates from Li-induced redox decomposition of the PS₄³⁻ tetrahedron (→ Li₂S + Li₃P); Mg substitution on the P site redistributes electrons (Mg-s/S-p hybridization) to block electron transfer from Li, widening the PS₄→MgS₄ electronic gap from ~2.0 to ~4.2 eV (Liu 2023, Angew)."
- "Mg-based doping to suppress anode-side reduction is independently supported by **two studies**: MgClO (Ke 2025, ESM) and MgF₂ (Liu 2023, Angew) — both invoke Mg s-p hybridization enriching electrons around S — directly motivating our Mg/Cl/O/F dopant cascade."
- "The bulk electronic conductivity of LPSCl is **8.16×10⁻⁹ S cm⁻¹** (Liu 2023), reduced ~8× by Mg/F doping — consistent with σ_e being defect/dopant-controlled rather than band-gap-controlled."
- "Our comp1 0 V reduction products (Li₃P + Li₂S + LiCl) are exactly the decomposition species Liu et al. identify as the source of anode parasitic reactions."

## 12. 주의/한계 (over-claim 방지)
- abstract는 "**1s–2p hybridization**"이라 쓰나, 본문/Fig 5는 **valence Mg(3s)–S(3p) s–p 혼성**을 기술 — 1s/2p는 코어준위라 결합 불가, **느슨한 표기**로 봄(s-p로 해석).
- "gap ~2.0/~4.2 eV"는 **MP smearing 0.2 eV + PDOS 전도대-가전자대 분리 추정** → 엄밀 band gap 아님, 우리 2.066과 우연 일치(절대비교 금지).
- σ는 도핑으로 **낮아짐**(2.91→1.70) — Cl-rich(우리 modelc, σ↑)와 **트레이드오프 방향 반대**. "redox 저항성↑ 대신 σ 약간 희생".
- 풀셀 성능(CCD·retention)은 스택압(10 MPa)·Li 두께(100 µm)·LCO 로딩(2 mg cm⁻²) 의존.
- DFT는 **결정상 계면 slab** — 실제 비정질 SEI·입계 미포함.

## 12b. 🔴 구조모델 신뢰도 비판 — "MgS₄가 P자리" 가정의 under-determination (2026-06-24)
> 이 논문의 **모든 메커니즘(Fig 5)은 "Mg가 P(4b)자리를 대체해 MgS₄ 사면체를 만든다"는 *가정된 구조*에 의존**한다. 그 가정 자체가 부실. (실험 성능 CCD↑·사이클·σ_e↓는 별개로 진짜.)

### ① "MgS₄ 사면체"가 화학적으로 무리 (+ 자기 ELF와 모순)
- **결합 성격 정반대**: PS₄³⁻ = P(χ2.19)–S(χ2.58), Δχ~0.4 → **공유결합**, 진짜 분자형 사면체 음이온([PO₄]³⁻·[SO₄]²⁻ 류). Mg–S = Mg(χ**1.31**)–S, Δχ~1.3 → **이온결합**; 실제 MgS는 **rock-salt(NaCl형) Mg 6배위 이온결정**, 분자형 사면체 아님.
- **자기 데이터가 반증**: Fig 5c(LPSC)는 P–S 사이 전자 공유(covalent), **Fig 5d(LPSC-MF)는 Mg가 S로 전자를 *내주고* S 주위 국재 = 전형적 이온결합 신호**. → 그들 ELF가 "MgS₄ = PS₄ 같은 공유 사면체" framing을 스스로 부정.
- **전하 극단**: [PS₄]³⁻ → [MgS₄]⁶⁻ (Mg²⁺+4S²⁻). 6− 국재 음이온은 비현실적.
- **솔직한 재서술**: 닫힌껍질 Mg²⁺(redox 비활성)이 redox 활성 P⁵⁺ 자리를 대체하면 그 자리 redox가 주는 건 당연 — "MgS₄ 사면체" 특수 framing 불필요.

### ② Rietveld가 under-determined → "가정→fit→메커니즘" 순환구조
- **lab XRD(Cu Kα, Smartlab)만 사용** (중성자 ✗). X-ray 산란 ∝ Z이라:
  - **Mg(12) vs P(15)** 차이 ~20%, **도핑 10%**라 그 자리 산란 변화 **~2%** → lab XRD로 거의 안 보임.
  - **Li(3)는 X-ray에 사실상 투명** → Mg@P vs Mg@Li 구분 불가(둘 다 비슷하게 fit).
  - 부분점유·무질서 site 多 → refinement under-determined (R_wp 8.4/9.0%도 특별히 좋지 않음).
- **격자팽창(a 9.851→9.863) 근거도 다인자**: (i) Mg 위치 + (ii) +3 Li(Li₆₊₃ₓ) + (iii) F⁻(<Cl⁻) 치환이 동시작용 → "Mg가 P 대체"로만 귀속하는 건 단순화.
- **이온반경상 오히려 Mg→Li자리**: Shannon(4배위) P⁵⁺ **0.17** / Mg²⁺ **0.57** / Li⁺ **0.59** Å → Mg²⁺≈Li⁺(거의 일치), P⁵⁺와는 3.4× 차이. 논문 DFT도 Mg@Li가 Mg@P보다 **~6 meV/atom 높을 뿐**(사실상 degenerate).
- **순환구조**: Mg@P *가정* → Rietveld 기각 못 함(감도 無) → DFT 간신히 손듦 → 그 **가정 구조를 Fig 5 DFT 입력**으로 사용 → "MgS₄ redox 저항" 결론. **결론이 가정의 하류** = 입력 틀리면 메커니즘 전체 붕괴.
- **검증할 기법 전무**: 중성자회절·**Mg K-edge EXAFS/XANES**(배위수·Mg–S 거리 직접)·PDF·²⁵Mg NMR 안 함. (대조: **[Lu]는 NPD 사용** → 자리 주장이 훨씬 단단.)

### 결론 (인용 시 가이드)
- ✅ **인용 가능**: 실험 성능(CCD 0.6→1.4, 대칭셀 1800 h, σ_e 8.16→1.03×10⁻⁹), "Mg 도핑이 음극 redox를 억제한다"는 *현상*.
- ⚠ **인용 금지/주의**: "**MgS₄ 사면체가 PS₄처럼 redox 저항**"이라는 *구체 메커니즘* — under-determined 구조 위 over-interpretation. deck엔 **"Mg 도핑 → 음극 안정 (기전은 미확정)"** 수준까지만.

## 13. [Ke] ↔ [Liu] 비교 (Mg-도핑 음극 패밀리)
| 항목 | [Ke] MgClO (ESM 2025) | [Liu] MgF₂ (Angew 2023) | 공통/차이 |
|---|---|---|---|
| 도판트 | Mg + Cl + O | Mg + F | **Mg 공통** |
| 핵심 혼성 | s-p / p-p (Mg-S, O 관여) | **Mg(s)-S(p) s-p** | 둘 다 s-p로 S 전자 풍부화 |
| 메커니즘 | 계면 metallic→gapped, 환원분해 차단 | PS₄→MgS₄ gap 2.0→4.2, Li 전자이동 차단 | **동일 패밀리** |
| LiF/추가 | Li₂O(8.37 eV) 전자절연 | **in-situ LiF**(F 도핑) | 절연 interphase 공통 |
| descriptor | 계면 binding E(2.14→5.03 J/m²) | σ_e 8×↓, gap 2.0→4.2 | 둘 묶어 cascade 평가셋 |
| 우리 연결 | cascade 동기 ① | cascade 동기 ② | **두 독립 논문이 같은 방향 검증** |

## 14. 기법 용어 미니사전
- **redox-resistible**: SE가 Li와 만나도 *전자를 안 줘서* 분해(redox)에 저항하는 성질. 이 논문의 신조어급 핵심.
- **electron redistribution**: 도판트(Mg)가 골격 내 전자를 재배치해 특정 원자(S) 주위를 전자-풍부하게 만드는 것.
- **s-p hybridization (Mg-S)**: Mg 3s와 S 3p 궤도가 섞여 결합. S 주위 전자밀도↑ → Li로의 전자 수용 차단.
- **σ_e (전자전도도)**: DC 분극으로 측정. 낮을수록 dendrite/전자누설 억제. LPSC bulk = 8.16×10⁻⁹ S/cm.
- **self-limiting LiF interface**: F 도핑이 충방전 중 계면에 만드는 LiF 절연막. 고계면에너지로 Li 균일증착 + 전자차단.
- **MgS₄ vs PS₄ tetrahedron**: Mg가 P 자리를 대체해 만든 사면체. PS₄는 Li에 분해되나 MgS₄는 무분해(DFT).
