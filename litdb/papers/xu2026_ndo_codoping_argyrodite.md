# High-air-stability lithium superionic conductor with excellent Li-metal compatibility for superior all-solid-state Li batteries — Chang Xu (Nano Energy 2026)

> slug `xu2026_ndo_codoping_argyrodite` · DOI `10.1016/j.nanoen.2026.112246` · type `exp (계산 0)` · PDF `litdb/inbox/57. NdO_LPSCl1.7 …` + `57. Sup) …` (inbox #57) · digested `2026-08-11` · status ✅
> elements: Li, P, S, Cl, O, Nd
> methods: XPS, Raman

## 1. 한 줄 요약
**우리 Nd₂O₃ 캠페인의 최근접 외부 경쟁/자매 논문.** IOP CAS(Fan Wu·Hong Li·Liquan Chen 그룹)가 Cl-rich argyrodite **Li₅.₃PS₄.₃Cl₁.₇(LPSC)** 에 **Nd–O 공도핑**(Li₅.₃₊₂ₓP₁₋ₓNdₓS₄.₃₋₁.₅ₓO₁.₅ₓCl₁.₇, 최적 x=0.025 = "LPSC-NdO")을 넣어 σ 6.99→**8.75 mS/cm**, CCD 2.29→**6.62 mA/cm²**, H₂S 1.55→**0.67 cm³/g**, LCO 풀셀 1000사이클 95.4%를 보고 — 단, **계산 0·Rietveld 0·오차막대 0**이고 핵심 메커니즘(Nd@P-site 치환, Li–Nd alloy SEI)은 전부 추정이다. 그들의 구조 모델은 정확히 **우리 Track 2(Nd→P, 컨트롤) 화학식**이고, 우리 cascade site-rule(26/26 M³⁺ = Li_24g)과 정면 충돌한다.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 저자 | Chang Xu, Lei Zhu, Chuang Yi, Xinhui Zeng, Dengxu Wu, …, Hong Li, Liquan Chen, **Fan Wu***(교신) |
| 소속 | IOP CAS Beijing(Key Lab Renewable Energy)·CASOL Energy·Yangtze River Delta Physics Research Center·USTC Suzhou·China FAW·Beijing Chehejia(Li Auto)·Eastern Inst. Tech. Ningbo |
| 저널 | Nano Energy **157** (2026) 112246 — 접수 2026-05-12 / 수정 07-17 / 게재확정 07-25 / 온라인 **07-27** |
| 조성 | Li₅.₃₊₂ₓP₁₋ₓNdₓS₄.₃₋₁.₅ₓO₁.₅ₓCl₁.₇ (x = 0, 0.025, 0.05, 0.075, 0.1); 최적 **x=0.025 = Li₅.₃₅P₀.₉₇₅Nd₀.₀₂₅S₄.₂₆₂₅O₀.₀₃₇₅Cl₁.₇** |
| 베이스라인 | LPSC = Li₅.₃PS₄.₃Cl₁.₇ (같은 그룹 Liu/Fan AFM 2022, ref [58] 계보) |
| 연구유형 | **순수 실험** (DFT/BVSE/MD 전무; 메커니즘은 HSAB 서사) |

⚠ **캠페인 경보**: 우리 Paper#2(Nd₂O₃@modelc Li₅.₄PS₄.₄Cl₁.₆)와 도펀트(Nd₂O₃)·모체 계열(Cl-rich argyrodite)이 같은 외부 논문이 2026-07-27 온라인 공개됨. 신규성 주장 시 이 논문과의 차별점(자리 판정 계산·전자구조/SEI 메커니즘·frozen-4f)을 반드시 명시해야 한다.

## 3. 핵심 물성 (수치 — 전부 소환값, 우리 db와 혼합 금지)
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| σ(RT) 시리즈 | **6.99 / 8.75 / 5.85 / 5.31 / 4.27 mS/cm** (x=0→0.1) | SS\|SSE\|SS, 냉간압축 펠릿(360 MPa, ⌀10 mm, t=0.680 mm, 80 mg) | 오차막대 없음·등가회로 미공개(Nyquist 스파이크 절편 판독으로 보임, Fig. 1c) |
| Ea 시리즈 | **0.292 / 0.278 / 0.283 / 0.295 / 0.312 eV** | 25–75 °C 6점 Arrhenius | 산포 존재(figure-read), R²·오차 미보고 |
| σ_e | 4.2×10⁻⁹ → **9×10⁻¹⁰ S/cm** (4.7× 감소) | DC 분극 0.5 V, 25 °C | **x=0, 0.025 두 조성만 측정** |
| CCD | **2.29 / 6.62 / 4.84 / 2.80 / 2.04 mA/cm²** | Li 대칭셀, 0.25 mA/cm² 스텝·30 min, 20 MPa | x=0.05–0.1 원곡선은 Fig. S3 |
| 대칭셀 | LPSC 단락 ~165–178 h ↔ NdO **>2000 h** (15→20 mV) | 1 mA/cm², 1 mAh/cm² | Fig. 3c,e,f |
| H₂S | 1.55 → **0.67 cm³/g** (60 min) | 150 mg 분말, 4 L 챔버, 30 % RH | 단일 런, Fig. 4a |
| 노출 후 σ | 30%RH: 1.12(16%) ↔ **4.81(55%)**; 드라이룸 60 min: 5.54(79%) ↔ 7.19(82%); 12 h: 3.61(52%) ↔ **6.08(69.5%)** | 노출 후 **재분쇄+재압축** 후 EIS | 12 h는 Fig. S4 |
| 풀셀 LCO | NdO 1C 1000cyc **117.2 mAh/g·"95.4%"** ↔ LPSC 300cyc 102.7·83.5% | LCO:SSE:VGCF=60:35:5, 2.5–4.2 V, 20 MPa, 1C=0.5 mA/cm² | "95.4%"의 분모는 130th 피크 122.8 (아래 §11-10) |
| 풀셀 Ni90 | NdO 1000cyc 154.2·**84.9%** ↔ LPSC 300cyc 단락·57.2% | 70:28:2, 2.7–4.3 V, 1C=0.89 mA/cm² | 레이트 0.2→10C: 224.3→93.2 mAh/g |
| gap / ESW / 기계 | **n/a** — 측정·계산 없음 | | |

## 4. DFT/계산 방법 ★
- **없음.** code/functional/pseudo/k-points/AIMD/MLIP/무질서 처리 전부 해당 없음.
- 메커니즘 논증은 (i) HSAB(경산-경염기 P–O 결합 강화), (ii) aliovalent 치환 산수(Nd³⁺→P⁵⁺, O²⁻→S²⁻, +2 Li/Nd), (iii) "Nd³⁺가 Li에 환원되어 Li–Nd alloy" 서사 — 셋 다 **계산·정량 근거 없이 문헌 인용과 개념 논리로만** 서 있다.
- → 우리 파이프라인이 채울 공간이 그대로 비어 있음 (§13).

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 합성 모식도 (Li₂S+P₂S₅+LiCl+**Nd₂O₃** → BM 800 rpm 20 h → 480 °C 15 h) | PI 합성 레시피와 직접 대조 가능한 조건 |
| 1b | **"제안" 구조 모델** — P/Nd 혼합 파이·S/O 파이·Cl 파이로 그린 argyrodite. Nd@P(4b)는 그림으로만 주장 | 우리 Track 2 화학식과 동일 스킴; 점유율 정련 없음 = 헛점 §11-1 |
| 1c | RT Nyquist 5조성 — 전부 반원 없는 스파이크, 절편 ~10(x=0.025)–21 Ω(x=0.1) figure-read | 등가회로 미공개 증거; 절편 순서는 1d와 일치 |
| 1d | σ 막대 6.99/8.75/5.85/5.31/4.27 — **오차막대 없음** | 소환값; 통계 부재 헛점 |
| 1e | DC 분극 (x=0, 0.025만): 4.2e-9 / 9e-10 S/cm | σ_e 감소 = PI 실험과 같은 방향 (§7) |
| 1f | Arrhenius 6점×5조성 — 점들이 fit 선에서 눈에 띄게 벗어남(figure-read) | Ea 오차 미보고; 우리 유도 σ₀ 분해의 입력 |
| 1g | Ea 곡선 0.292→0.278→0.312 | 소환값 |
| 2a | XRD 5조성 + 29–33° 줌. * film(폴리이미드)·**♦ LiCl** 마커. 줌의 점선 가이드: x=0(~30.05°)→x=0.025(**~30.4°, +0.3° 이상 우이동** figure-read)→x=0.05–0.075 좌회귀→x=0.1 소폭 우 | **♦가 x=0.025에도 찍혀 있음** — 본문 "x≥0.05부터 LiCl"과 불일치 (§11-3); +0.3° ≈ ~1% 수축은 x=0.025치고 과대 — 내부표준 없음 (§11-2) |
| 2b | Raman 5조성 + 420 cm⁻¹ 줌 (PS₄³⁻) | 본문 "x 증가 시 세기 체계적 감소" ↔ 그림에선 **x=0이 가장 약해 보임**(figure-read, 정규화 언급 없음) — §11-11 |
| 2c | LPSC-NdO pristine XPS: S 2p(PS₄³⁻)·P 2p(PS₄³⁻)·**Cl 2p(LiCl 성분 존재)**·O 1s(Li–O–P 531.8 대피크+P=O 534 소)·**Nd 3d(970–1000 eV, 노이즈 큰 raw + 다중피크 fit)** | Nd 0.2 at%로 S/N 낮음(figure-read) — Nd³⁺ "존재"만 입증, 자리·잔류 Nd₂O₃ 구분 불가 |
| 2d | SEM+EDS (LPSC vs NdO): O는 입자와 공위치, **Nd는 산점 도트** | μm-scale·도트 수준 — 격자 편입 증거로 불충분 |
| 3a,b | CCD 계단: LPSC 2.29 / NdO 6.62 mA/cm² (6.62 이후 NdO 전압 스파이크 반복 figure-read) | CCD 6.62 = Table S1 기준 산화물-공도핑 중 최고 |
| 3c,e,f | 대칭셀 2000 h: LPSC 33.8 mV→~178 h 단락; NdO 15→20 mV | 소환값 |
| 3d,g | 사이클 중 EIS 3D: NdO Z' 0–80 Ω 안정 ↔ LPSC 0–600 Ω 성장 | |
| 3h | CCD 막대 5조성 | "σ_e와 상관" 주장은 σ_e 2조성 측정으로 뒷받침 안 됨 (§11-6) |
| 3i,j | DRT: D1(GB+접촉, τ~1e-6 s)·D2/D3(전하이동·계면 수송)·D4(τ~1 s) | **D4 진폭은 NdO(~20 Ω)가 LPSC(~5 Ω)보다 큼**(figure-read) — 본문은 언급 안 함 (§11-13) |
| 4a–g | 30 %RH: H₂S 곡선·노출후 Nyquist/σ·Raman·XRD(LPSC만 열화+LiCl/Li₄P₂S₆ ♦) | H₂S 프로토콜(150 mg/4 L/30 %RH) 표준적; §11-9 |
| 4h,i | 드라이룸(-30 °C dp) 60 min σ | |
| 4j | **노출 셀 사이클**: LPSC 초기 ~72 mAh/g→100cyc "55.3%" 단락 ↔ NdO ~112→500cyc 50.8% (figure-read: 초기 용량 자체가 40 mAh/g 차이) | 비교 시점 불일치(100 vs 500 cyc) — §11-12 |
| 4k | 노출 후 Ea: 0.33 vs 0.30 eV | |
| 5a–g | LCO 풀셀: 레이트(1C에서 NdO 121>LPSC 92)·1000cyc 95.4%·전압 프로파일 | 95.4% 분모 주의 (§11-10); 0.2C에선 LPSC(161)>NdO(156) figure-read |
| 5h–j | 셀 모식도·사이클 후 EIS: NdO 91.28 Ω ↔ LPSC 346.8 Ω | |
| 6 | Ni90 풀셀: 레이트 0.2–10C·1000cyc 84.9% vs 57.2%·EIS 215.5 vs 406.2 Ω | 페이지 렌더로만 확인(크롭 미열람) |
| 7a–d | **사이클 후 계면 XPS**: LPSC = Li₂S(~160 eV) 대·Li₃P(~128) 명확 ↔ NdO = Li₂S 소·Li₃P 거의 없음; NdO에 Li₂O(528.5)·Li–O–P(531.5); Nd 3d에 **"Li–Nd alloy" 라벨 소피크 ~995 eV** | Li₂O·LiCl·Li₂S/Li₃P 억제는 우리 grand-potential SEI 서사와 정합; **Li–Nd alloy는 열역학적으로 의심** (§11-7) |
| 7e | 사이클 후 Li 표면 SEM: LPSC 거침 ↔ NdO 매끈 | 명암 조건 상이 |
| 7f | 계면 모식도 — 본문 스스로 "**rational speculation**"이라 명기 | 인용 시 "저자 자인 추정"으로 |
| S1 | x=0.05/0.075/0.1 EDS — Nd 편중 심화 | 고농도 불균일 근거 |
| S2 | pristine LPSC XPS (S/P/Cl 2p) | 대조군 |
| S3 | x=0.05/0.075/0.1 CCD 원곡선 (4.84/2.80/2.04) | |
| S4 | 드라이룸 12 h: 6.99→3.61 ↔ 8.75→6.08 mS/cm | |
| Table S1 | 산화물-공도핑 sulfide 횡비교: Sb-O 7.0/5.2 · Y-O 3.53/1.5(=[WangYO]) · Sn-O 5.71/2.9 · Sc-O 4.53/0.3 · Zn-O 2.25/1.4 · Bi-O 7.93/2.5 · In-F 5.6/2.5 · **Nd-O 8.75/6.62(본 논문)** (σ mS/cm / CCD mA/cm²) | 우리 cascade 논문의 문헌 비교표 원천 — PDF 텍스트로 전사 |

## 6. Post-processing ★
- **DRT** (relaxation-time 분포): Matlab DRT tool로 대칭셀 EIS 분해 — D1(τ≈10⁻⁷–10⁻⁶ s, 입계+물리 접촉), D2·D3(10⁻⁶–10⁻¹ s, 전하이동+계면 이온수송), D4(10⁻¹–10⁰ s, 벌크 Li 확산/계면 반응층). 정규화·피팅 파라미터 미공개.
- EIS→σ: 등가회로 미공개(스파이크형 Nyquist라 절편 판독 추정). Arrhenius는 25–75 °C 6점 선형 fit.
- XPS 피팅: 성분 라벨만 표기, 피크 위치/FWHM/면적 표 없음. 사이클 후 계면 XPS의 **시료 준비법(박리/스퍼터/이송) 미기술**.

## 7. 우리 DFT 대비 (comp1 / modelc / Nd 캠페인) → `our_dft_baseline.md`
| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| 모체 | Li₅.₃PS₄.₃Cl₁.₇ (Cl 1.7, LiCl 상분리 동반) | modelc = Li₅.₄PS₄.₄Cl₁.₆ (Cl 1.6) | **최근접 자매 조성.** 그들 XRD에 LiCl ♦가 x=0.025부터 보임 → 실제 argyrodite상 Cl < 1.7 가능성 = Cl 1.6~1.7 용해한계 문헌과 정합, 우리 modelc(1.6) 선택 보강 |
| **Nd 자리** | **Nd³⁺→P⁵⁺(4b) "inferred"** + O²⁻→S²⁻, +2Li/Nd — 우리 Track 2와 동일 화학식 스킴 | **cascade site-rule: 26/26 M³⁺ champion = Li_24g** (0 P_4b) + Track 1(Nd→Li, −3Li/Nd) UMA relax 완료; Track 2는 "불안정 입증용 컨트롤"(예상 ΔE +1–3 eV/Nd) | **정면 충돌 — 단 그들 직접 증거 0** (Rietveld·NMR·EXAFS 없음). [WangYO] Y@P4b·[Yang25] La@4b와 같은 "관행적 P-site 가정" 계보. 우리 Track1 vs Track2 formation-energy 대결이 유일한 정량 판정이 된다 (§13-P1) |
| σ (도핑 효과) | x=0.025에서 **1.25×↑**(6.99→8.75); x=0.1에선 **0.61×↓**(4.27) | UMA-MD(x=0.2, Track1): σ300 비 **0.52×↓** (D0 0.65 × n_Li 0.90 × Ea 0.88) | **고농도에선 수렴**(그들 0.61×@x=0.1 ↔ 우리 0.52×@x=0.2, 방향·크기 일치). 희석 극대(1.25×@0.025)는 우리가 계산 안 한 영역 — 단 아래 σ₀ 분해가 그들 서사를 흔든다 |
| σ₀ 분해 (우리 유도) | σ비 1.252 = exp(ΔEa/kT) **1.73** × **σ₀비 0.73** → 향상분 전부 Ea에서, **prefactor는 27% 감소** | 우리 x=0.2: 감소분의 지배 인자가 **D0 prefactor 0.65×** (Ea 불변) | **prefactor 감소 방향 일치** — 그들 "carrier 증가(+2Li/Nd)·채널 확장" 서사는 σ₀ 증가를 요구하므로 **자기 데이터와 모순** ([WangYO] ③과 동일 패턴) |
| Ea | 0.292→0.278 (Δ−0.014 eV) | Track1 x=0.2: 0.224→0.227 (Δ+0.003) | 둘 다 \|Δ\|≤0.015 — "장벽 거의 불변" 수준. 그들 Δ−0.014는 fit 산포(오차 미보고) 대비 유의성 불명 |
| σ_e | 4.2e-9→**9e-10** (4.7×↓) | PI 실험(DC 분극)도 Nd₂O₃ 도핑 시 감소; 우리 DFT는 **벌크 gap이 오히려 축소**(2.184→1.632 eV, Nd 5d) → 감소는 벌크가 아니라 **계면/percolation**(O-유래 Li₃PO₄ 5.73·NdPO₄ 5.55·Li₂O 5.24 eV 상이 입계 전자망 절단) | **독립 랩 외부 재현** — 우리 "σ_e 감소는 interphase 효과" 해석의 실험 지지 1건 추가. 그들은 감소 관찰만 하고 메커니즘 무설명 → 우리 해석이 채울 공간 |
| 음극 SEI | Li₂O·LiCl·(Li–Nd alloy 주장)·Li₂S/Li₃P 억제 | grand-potential: 도핑 시 O-유래 **Li₂O(5.24)·Li₃PO₄(5.73)**·LiCl(6.65)가 전도성 Li₃P(0.70 eV) 대체 = 전자누출 차단 | **Li₂O·LiCl·Li₃P-억제 3항목 정합** (그들 XPS가 우리 SEI json의 실험판). **Li–Nd alloy는 우리 산물 목록에 없음** — MP에 Li–Nd 금속간화합물 부재(비혼화 경향)로 열역학적 의심 → §13-P2 검증 표적 |
| gap | n/a (미측정) | Nd₂O₃@modelc **1.632 eV**(DFT+U, 120-atom/k661; matched 무도핑 2.184) — 4f 갭 무접촉, narrowing은 Nd 5d/호스트 이동 | 비교 불가 — 그들이 안 한 것. 우리 고유 축 |
| 산화 onset/ESW | n/a | comp1=modelc **2.256 V** (S²⁻-limited) | 비교 불가 |
| 대기(H₂S) | 1.55→0.67 cm³/g | **우리 축 밖** (0 K hull, 가수분해 미계산 — "우리가 H₂S 억제 계산" 금지) | 문헌 맥락은 [Zhu20] 열역학 지도(thiophosphate 과민·O/P–O 강화)로만 연결 |

## 8. 적용 인사이트
- ① **Paper#2 서론/디스커션에서 이 논문을 반드시 인용**하고, 차별점을 "실험 관찰 ↔ 계산 메커니즘"으로 세운다: 그들이 비워 둔 (a) Nd 자리 판정(Track1 vs Track2 ΔE), (b) σ_e 감소의 벌크-아님 증명(gap 1.632 축소 + 계면상 gap), (c) Li–Nd alloy 열역학 검증 — 전부 우리 결과가 이미/거의 있다.
- ② 그들 **고농도 σ 감소(0.61×@x=0.1)와 우리 UMA 0.52×@x=0.2 수렴**은 li_transport.json `experimental_validation`([Yang25] 0.65×)에 추가할 두 번째 외부 실험 앵커.
- ③ Table S1은 우리 cascade 논문의 문헌 비교표 시드 — Nd-O가 산화물-공도핑 계열 중 σ·CCD 최고라는 포지셔닝은 우리 도펀트 선택의 사후 정당화로 쓸 수 있다(소환값 규율 유지).
- ④ 대칭셀 2000 h·CCD 6.62·풀셀 1000cyc 프로토콜(0.25 mA/cm² 스텝·30 min, 20 MPa)은 PI 실험 설계의 벤치마크 프로토콜로 이식 가능.

## 9. 인용 가능 문장 (deck/paper용)
- "Xu et al. (Nano Energy 2026) demonstrated Nd–O co-doped Li₅.₃PS₄.₃Cl₁.₇ with σ = 8.75 mS/cm and CCD = 6.62 mA/cm², but assigned Nd to the P(4b) site by inference only — no refinement, NMR, or calculation; our formation-energy comparison directly tests this assignment."
- "The measured electronic-conductivity drop upon Nd–O doping (4.2×10⁻⁹→9×10⁻¹⁰ S/cm) reproduces the direction seen in our companion experiments; our DFT shows the bulk gap actually narrows (2.184→1.632 eV), locating the suppression at O-derived wide-gap interphases rather than in the bulk."
- "Their own Arrhenius data decompose into an activation-energy gain offset by a ~27 % prefactor loss — inconsistent with the claimed carrier-density mechanism, but consistent with our MLIP-MD finding that Nd–O doping suppresses the diffusion prefactor."

## 10. 주의/한계 (over-claim 방지)
- 이 논문의 수치는 전부 **소환값** — 우리 db 절대값(σ, gap, Ea)과 같은 표에 섞지 않는다. 특히 UMA 절대 σ 비교 금지(비율만).
- "그들이 우리 site-rule을 반증했다"고 쓰지 말 것 — 그들의 Nd@P는 **증거 없는 가정**이라 반증 능력이 없다(아래 §11-1). 대립 구도는 "우리 UMA/DFT vs 그들 무증거 가정"이다.
- 대기안정성은 우리 계산 축 밖 — H₂S 수치는 문헌 맥락으로만.
- 95.4%/2000 h/6.62 같은 헤드라인 수치는 분모·시점·통계 조건(§11)을 병기해 인용.

---

## 11. ★ 헛점 분석 (전용 섹션 — 본문/SI 출처 구분)
> 요청 규율: "본문 없음 · SI 있음/없음"을 항목마다 명시. SI는 5쪽(Table S1 + Fig. S1–S4)이 전부라 방법론 보강 자료가 사실상 없다.

**(1) Nd 도핑 자리 — 직접 증거 전무 (가장 큰 헛점)**
- 본문: Fig. 1b는 "proposed structural model"이고, 본문 §2.1 원문이 스스로 "Nd³⁺ **is inferred** to substitute for P⁵⁺"라고 쓴다. 근거로 제시된 것은 ① XRD 피크 이동(정성, §11-2), ② Raman PS₄³⁻ 세기 감소(§11-11), ③ XPS Nd 3d "Nd³⁺ 존재"(§2.2) 셋뿐.
- **XRD Rietveld 정련: 본문 없음 · SI 없음.** 격자상수 a, 점유율, R-factor가 논문 전체에 단 하나도 없다. 점유율 정련 없이 4b-site 배정은 성립 불가.
- XAS/EXAFS: 없음. ³¹P MAS NMR( P-site 치환이면 PS₄ 신호 변화로 가장 민감): 없음. 중성자: 없음.
- XPS Nd 3d(Fig. 2c)는 Nd³⁺ "존재"만 — **잔류 Nd₂O₃(명목 0.0125 mol/fu, XRD 검출한계 이하)와 구분 불가.** figure-read: raw 산포가 커서(Nd ~0.2 at%) 다중피크 fit은 장식적.
- EDS(Fig. 2d)는 10 μm 스케일 산점 도트 — 격자 편입 vs 나노분산 Nd₂O₃ 구분 불가. 오히려 Fig. S2(SI)의 x≥0.05 EDS는 Nd 편중을 보여줘 "균일 고용" 주장의 상한이 낮음을 시사.
- ⇒ **Nd@P·O@S·+2Li 모델 전체가 명목 조성 산수** 위에 서 있다. 우리 cascade(26/26 Li_24g)와 충돌하지만, 그들 쪽 증거가 0이라 이 논문은 site 논쟁에서 **증거 능력이 없다** ([WangYO]의 constrained-Rietveld보다도 약함).

**(2) 격자상수·피크 이동의 정합성**
- 본문 없음 · SI 없음: a(Å) 값 자체가 없다. 취득 불가 항목.
- figure-read (Fig. 2a 줌): x=0→0.025에서 30° 부근 피크가 **+0.3° 이상 우이동** — Bragg 산수로 Δd/d ≈ −1%. x=0.025(치환 2.5%)치고 과대하다 ([Yang25] La x=0.04이 +0.31%). 내부표준(Si 등)·zero-shift 보정 언급 없음, 폴리이미드 필름 마운트 — 시편 높이 오차 가능성 배제 불가.
- 본문 내 자기모순: §2.1은 향상 요인을 "(i) **lattice expansion** which widens the Li⁺ migration pathways"라 쓰고, §2.2는 "At x ≤ 0.025 … **mild lattice contraction**"이라 쓴다. 같은 최적 조성에 대해 팽창·수축이 공존.
- figure-read: x=0.1 피크는 x=0.075보다 다시 우측 — "x>0.025는 팽창 지배" 서술과도 깔끔히 안 맞는 비단조 거동.

**(3) LiCl 상분리 — 조성 표기 vs 실제 화학량론**
- 본문 텍스트: "Once x ≥ 0.05, the solid solubility limit is breached, causing LiCl impurity precipitation."
- ↔ **Fig. 2a에는 x=0.025 패턴에도 ♦(LiCl) 마커가 찍혀 있고**(figure-read), pristine LPSC-NdO의 Cl 2p XPS(Fig. 2c)에도 LiCl 성분이 피팅되어 있다. 즉 **최적 조성부터 이미 2상**.
- Cl 1.7 명목 + LiCl 석출 ⇒ argyrodite 실상의 Cl은 1.7 미만(용해한계 1.6–1.7 문헌과 정합). **명목 조성 기반의 모든 화학량론 논증(+2Li/Nd 포함)의 기반이 흔들린다.** ICP/정량 조성 분석: 본문 없음 · SI 없음.
- 우리에겐 호재: 실제 argyrodite상이 Cl≈1.6대라면 modelc(1.6)와의 비교 적합성은 오히려 올라간다.

**(4) 전도도 향상 주장의 통계 처리 — 사실상 부재**
- 셀 반복수: 본문 없음 · SI 없음 (조성당 n=1로 읽힘). 오차막대: σ(Fig. 1d)·Ea(Fig. 1g)·CCD(Fig. 3h)·H₂S(Fig. 4a) 전부 없음.
- EIS 등가회로·피팅 파라미터: 본문 없음 · SI 없음. Fig. 1c가 반원 없는 스파이크라 절편 판독으로 보이나 방법 미기술.
- 펠릿 상대밀도 미보고 — 그들 자신의 수치(80 mg, ⌀10 mm, t=0.680 mm)로 유도하면 **ρ≈1.50 g/cm³ ≈ ~82 %TD**(우리 유도; modelc 이론밀도 1.82 g/cm³ 기준) — 냉간압축 표준 수준이지만, 1.25× 차이를 논하는 논문이 밀도 산포를 통제·보고하지 않았다.
- Arrhenius fit: 6점, figure-read로 fit 선 이탈이 보이는데 R²·신뢰구간 없음. Δσ(1.25×)·ΔEa(0.014 eV)가 펠릿 재현성 산포보다 큰지 판정할 데이터가 논문에 없다.

**(5) σ₀(prefactor) 모순 — 그들 자신의 수치로 유도**
- σ비 8.75/6.99 = 1.252, ΔEa = −0.014 eV → exp(ΔEa/kT₂₉₈) = 1.73. 따라서 **σ₀비 = 1.252/1.73 = 0.73** — prefactor 27 % 감소.
- "carrier density 증가(+2Li/Nd)·채널 확장" 메커니즘이라면 σ₀는 증가해야 한다. **향상분 전체가 Ea 항이고 prefactor는 역행** — 본문 어디에도 이 분해가 없다. ([WangYO] ③·우리 UMA D0 0.65×와 같은 패턴 — §7)

**(6) σ_e–CCD 상관 주장의 외삽**
- §2.3: "CCD values first increase then decrease, which correlates with their electronic conductivity [11,58]" — 그러나 σ_e는 **x=0과 0.025 두 조성만 측정**(Fig. 1e). 나머지 3조성의 σ_e는 미측정인데 5조성 CCD 추세와 "상관"이라 주장 — 문헌 인용으로 외삽한 것. 본문 없음 · SI 없음(추가 σ_e 데이터).

**(7) "Li–Nd alloy" 계면상 — 열역학·분광 양쪽에서 의심**
- 유일 근거: 사이클 후 Nd 3d XPS(Fig. 7d)의 **~995 eV 소피크 하나** + 본문 "suggesting … the **plausible** formation of Li–Nd alloy"(자인된 추정). 참조 스펙트럼·기준물질 없음.
- 열역학: Li–Nd 이원계는 안정 금속간화합물이 보고되어 있지 않다(상호 비혼화 경향; MP에도 Li–Nd 화합물 부재 — §13-P2에서 hull로 명시 검증). Nd³⁺→Nd⁰ 환원이 일어나더라도 산물은 "합금"이 아니라 Nd 금속 분산일 가능성.
- 내적 긴장: 금속상(합금)이 포함된 계면을 "ionically conductive but **electronically insulating**"이라 주장(서론·§2.6) — 금속상이 연속이면 전자 차단과 모순, 불연속 분산이어야만 성립하는데 그 형상 증거 없음.
- 사이클 후 계면 XPS의 시료 준비(박리? 스퍼터? 이송 중 공기 차단?)가 실험부에 없음 — 깊이·오염 통제 불명. Fig. 7f 모식도는 본문 스스로 "rational speculation".

**(8) Raman 근거의 자기모순**
- 본문: "PS₄³⁻ 420 cm⁻¹ 피크 세기가 x 증가에 따라 체계적으로 감소 = P⁵⁺→Nd³⁺ 치환 증거."
- figure-read (Fig. 2b): 정규화 언급이 없는 적층 스펙트럼에서 **x=0의 피크가 오히려 가장 약해 보이고**, x=0.025–0.1은 비슷하거나 더 강하다. 무정규화 Raman 세기 비교는 애초에 정량 근거가 못 된다. 세기 정량표: 본문 없음 · SI 없음.

**(9) 공기안정성 측정 프로토콜**
- 명시된 것(본문 4.2): 150 mg 분말·4 L 밀폐 챔버·30 %RH·10 min 간격·60 min; 드라이룸 dew point −30 °C 60 min/12 h. 이 부분은 관례 수준으로 적절.
- 약점: ① H₂S 곡선 단일 런(재현성 없음); ② 노출 후 σ는 분말을 **재분쇄·재압축 후** 측정 — 표면 열화층을 벌크에 희석하는 관대한 프로토콜(펠릿 그대로 측정보다 유리); 명시는 되어 있으나 비교 논문들과 프로토콜 차이 논의 없음; ③ 60 min 시점 LPSC 곡선은 아직 상승 중(figure-read) — 포화값 아님; ④ 온도 미기재.

**(10) 풀셀 성능 수치의 분모·부하**
- "95.4 % after 1000 cycles": figure-read(Fig. 5e) — 용량이 130th에 122.8로 **상승 후** 1000th 117.2. 117.2/122.8 = 0.954 ⇒ **분모가 초기가 아니라 130th 피크**. 초기(~113–117) 대비면 ~100 %가 되는 활성화 곡선. 관행상 흔하지만 분모 명시가 없다.
- 부하: 5 mg 복합양극(LCO 60 %) / 0.785 cm² ⇒ **~3.8 mg_LCO/cm² ≈ 0.5 mAh/cm²**(우리 유도) — 저부하 셀. 20 MPa 운전은 preload 360 MPa 성형 후.
- 노출 셀 비교(Fig. 4j): LPSC "55.3 %"는 100cyc 시점, NdO 50.8 %는 500cyc 시점 — **시점 불일치 비교**. 그리고 노출 후 NdO 셀도 초기 ~112→500cyc ~57로 꾸준히 감쇠(절대 성능은 좋지 않음).

**(11) DRT 서술의 선택성**
- 본문: D4(τ≈10⁻¹–10⁰ s)가 "pristine LPSC에서 remarkable increase". figure-read(Fig. 3i,j): LPSC의 D4는 ~3–7 Ω 수준이고, **NdO의 D4가 ~15–20 Ω로 오히려 크다**(안정적이긴 함). LPSC의 실제 성장은 D1/D2. "NdO의 큰 D4 = 두꺼운(안정) 계면층?" 같은 불리한 해석 가능성은 논의되지 않음. DRT 정규화·역산 세팅: 본문 없음 · SI 없음.

**(12) SI가 채워주지 못한 것 총정리 (조율자 체크리스트 회신)**
| 항목 | 본문 | SI |
|---|---|---|
| XRD Rietveld (a·점유율·R-factor) | 없음 | **없음** |
| EIS 등가회로·피팅 파라미터·셀 반복수·오차막대 | 없음 | **없음** |
| XPS 원 스펙트럼+피팅 | Fig. 2c(NdO)·Fig. 7(사이클 후) — 파라미터 표 없음 | Fig. S2(LPSC pristine S/P/Cl 2p)만 — 파라미터 표 없음. XAS 없음 |
| 합성 상세 | 본문 4.1에 충실(BM 800 rpm·20 h·1:20 / 480 °C·15 h·1 °C/min / Ar <0.1 ppm / 400-mesh) | 추가 없음. **펠릿 밀도는 양쪽 다 없음**(우리 유도 ~82 %TD) |
| 조성 그리드 전체 | 본문에 전 5조성(σ·Ea·CCD·XRD·Raman) | S1(EDS 고농도)·S3(CCD 원곡선)·S4(12 h 드라이룸)·Table S1(문헌 횡비교) |

## 12. ★ 우리가 취득할 것 (전부 소환값 — db 절대값과 분리)
1. **합성 조건** (PI 실험 대조용): Nd₂O₃ 직접 투입 고상법 — BM 800 rpm/20 h/BPR 1:20(지르코니아), 480 °C/15 h/승온 1 °C/min, Ar <0.1 ppm, 400-mesh. 우리 Nd₂O₃@modelc 합성 조건과 나란히 놓을 레시피.
2. **조성 그리드·최적점**: x = 0–0.1(0.025 간격), 최적 **x=0.025** — 실험 최적이 희석 영역임을 기록(우리 계산 x=0.2와 스케일 갭 → §13-P4의 동기).
3. **σ·Ea 시리즈**(소환): 6.99/8.75/5.85/5.31/4.27 mS/cm · 0.292/0.278/0.283/0.295/0.312 eV — 고x 감쇠(0.61×@x=0.1)는 우리 UMA 0.52×@x=0.2의 **두 번째 실험 앵커**([Yang25] 0.65× 다음) → `li_transport.json` experimental_validation에 추가 후보.
4. **σ_e 감소**(소환): 4.2×10⁻⁹→9×10⁻¹⁰ S/cm — PI 관찰과 같은 방향의 독립 재현 → 우리 "interphase/percolation" 해석(electronic.json) 지지 실험 1건 추가.
5. **CCD 시리즈**(소환): 2.29/6.62/4.84/2.80/2.04 mA/cm² + 프로토콜(0.25 mA/cm² 스텝·30 min·20 MPa).
6. **대기·드라이룸 수치**(소환): H₂S 1.55→0.67 cm³/g(30 %RH·60 min); σ 유지율 30 %RH 16 %↔55 %, 드라이룸 60 min 79 %↔82 %, 12 h 51.6 %↔69.5 %; 노출 후 Ea 0.33↔0.30 eV. ⚠ "재분쇄+재압축 후 측정" 프로토콜 병기 필수.
7. **Table S1 횡비교표**: 산화물-공도핑 계열 σ/CCD (Sb-O·Y-O·Sn-O·Sc-O·Zn-O·Bi-O·In-F·Nd-O) — cascade 논문 비교표 시드. Nd-O가 계열 최고 σ·CCD.
8. **SEI 관찰종**(소환): Li₂O(528.5 eV)·LiCl·Li₂S/Li₃P 억제 — 우리 sei_products.json 서사의 실험판. "Li–Nd alloy"는 **검증 표적**으로만 취득(사실로 등재 금지).
9. **격자상수: n/a** — 논문에 없음(취득 불가). 필요 시 Fig. 2a 피크각의 figure-read 근사만 가능하나 내부표준 부재로 권장하지 않음.
10. **임계 도핑 농도**(소환): 용해한계 서술 x≥0.05(단 그림은 x=0.025부터 LiCl ♦) — "x_c는 0.025–0.05 사이 어딘가, 논문 내 자기불일치"로 기록.

## 13. ★ 계산 제안 (우선순위·서버·예상 비용)
> 원칙: 이 논문이 **계산 없이 주장한 것**을 우리 파이프라인으로 판정한다. 기존 자산(Track1 relax 완료 cfg141·gap 1.632·4f-갭 무접촉·sei_products.json·nd_gap_reference_mp.json 7종·cascade 47종)과의 겹침/보완을 명시.

| 순위 | 과제 | 그들 주장 → 우리 판정 | 파이프라인 | 자산 겹침 | 서버·비용 |
|---|---|---|---|---|---|
| **P1** | **Nd 자리 대결: Track1(Nd@Li) vs Track2(Nd@P) formation energy** | "Nd³⁺→P⁵⁺"(무증거) → ΔE_form 정량으로 지지/반박 | UMA 프리스크린(배열 2–3개) → QE PBE(+U 8 eV·frozen-4f 병행) relax·total E | `modelc_nd_doped.json`에 Track2 설계 완료(128-atom, 예상 +1–3 eV/Nd)·Track1 relax **이미 완료** → **Track2 2–3배열만 신규** | gabia A6000: UMA 수 분 + DFT relax 배열당 ~12–24 h → **1–3일**. Paper#2 반박 데이터의 핵심 |
| **P2** | **Li–Nd "alloy" 열역학 판정** | "Nd³⁺ 환원→Li–Nd alloy"(XPS 소피크) → Li–Nd 이원 hull에 화합물이 있는가 + Nd-도핑 SE의 0 V lithiation 산물에 Nd⁰/합금이 나오는가 | mp-api Li–Nd hull 조회 + 기존 grand-potential staircase(`sei_products.json` 2026-06-24) 재독 → 필요 시 run_nd_sei.sh 확장 | **거의 완성** — 우리 staircase에 Li–Nd 합금 없음(Li₂O·LiCl·Li₃P 대체 서사) | gabia(MP_API_KEY): **수 분–1 h**. 비용 최저·반박력 최고 |
| **P3** | **BVSE: Nd@Li vs Nd@P 배열의 Li 채널 %** | "채널 확장·steric barrier 감소" → 기하·정전기적으로 채널이 넓어지는지 막히는지 | tools/comp1_v3 BVSE(softBV R0: S 2.105/Cl 2.249/O 1.466, 원본 주기셀 정량 규율) — Track1 cfg141 vs Track2 relax 셀 | cascade bvs_li_proxy 0.92(Nd 상위)와 교차 | 로컬/kgy CPU: 셀당 **수십 분**. 그림 1장( channel% 비교) 즉시 산출 |
| **P4** | **희석 농도 UMA-MD**: x≈0.025 상당(대형 셀 Nd 1–2개) 멀티시드 σ 비율 | "x=0.025에서 1.25×↑" → 희석 극대가 재현되는가, σ₀·Ea 분해는 | UMA-s-1p1 Langevin NVT·dt 2 fs·2–50 ps MSD 창·600/800/1000 K×3시드(표준 규율; 비율만 인용) | 우리 x=0.2 결과(0.52×)의 농도축 보완 — 그들과 유일하게 겹치는 미계산 영역 | gabia/kgy GPU: 3T×3seed×~200 ps, 대형 셀(≥300 atom) — **3–7일 벽시계**(순차). ⚠ UMA Nd-4f 전이성 캐비앳 병기 |
| **P5** | **Track2 배열 fixed-occ gap**: Nd@P가 밴드엣지에 뭘 하나 | (그들 무주장 — 우리 보완) Nd@P면 Nd 5d/4f가 CBM/갭에 더 개입하는지 → 자리별 전자구조 지문 | QE scf+fixed-occ nscf(우리 canonical 레시피), PDOS | gap 1.632(Track1)·4f 무접촉 판정과 직접 비교 — "자리가 전자구조 지문을 남긴다"면 XPS/광학으로 실험 판정 제안 가능 | KISTI/gabia: relax 재활용 시 nscf **수 시간–1일** |
| **P6** | **Nd 계면상 gap 정합**: NdOCl·Nd₂O₃·NdS·Nd⁰ vs Li 접촉 반응 | "계면은 이온전도·전자절연" → 산물별 gap(NdS 0 eV 금속!)으로 전자절연 주장 조건부 판정 | 기존 nd_gap_reference_mp.json(7종) + interface_reactivity_v2 | **frozen-4f 검증표적 7종과 동일 상 목록** — 재계산 시 우리 숫자로 대체 | gabia: 조회 수준 **~1 h**; frozen-4f 재계산은 별도 트랙(계획 존재) |
| P7 | CI-NEB: Nd 근방 vs 원거리 Li hop 장벽 | "steric barrier 감소" 직접 검증 | UMA-NEB 프리스크린 → QE CI-NEB(대표 경로 1–2개) | P3 BVSE가 싼 대체 — NEB는 확증용 | KISTI: 경로당 **수 일** — P3 결과가 뾰족할 때만 |

- **우선순위 논리**: P2(수 분, Li–Nd alloy 반박 = 논문 §2.6 서사의 급소) → P1(Paper#2 핵심 차별화, 절반 완료) → P3(싸고 그림이 됨) → P4(희석 영역 공백 메움) → P5/P6 → P7.
- **이미 가진 것과의 겹침 요약**: gap 1.632 eV(Track1)·4f-갭 무접촉·SEI gap 서사(Li₂O/Li₃PO₄/LiCl vs Li₃P)·cascade site-rule은 **신규 계산 없이도** 이 논문의 σ_e 무설명·SEI 무근거·자리 무증거 세 공백을 채우는 디스커션 재료다. 신규 계산이 필요한 것은 Track2 ΔE(P1)와 희석 σ(P4) 둘이 본질.

## 14. 본 그림 / 안 본 그림 (투명성 기록)
- **크롭을 직접 열람(Read)**: `fig_1, fig_2, fig_3, fig_4, fig_5, fig_7` (6/12).
- **페이지 렌더로만 확인**(크롭 미열람): `fig_6`(Ni90 풀셀 — 수치는 본문 텍스트로 확보), `fig_S1, fig_S2, fig_S3, fig_S4`(SI 5쪽 전체를 페이지 단위로 열람).
- **이미지로 안 읽음**: `tab_S1` — 표는 PDF 텍스트로 전사(규율).
- 그림–본문 불일치 발견 3건: ① Fig. 2a x=0.025의 LiCl ♦ ↔ 본문 "x≥0.05"; ② Fig. 2b Raman 세기 "감소" 주장 ↔ x=0이 가장 약해 보임; ③ Fig. 3i,j D4 서술의 선택성(NdO D4가 더 큼). 상세는 §11.
