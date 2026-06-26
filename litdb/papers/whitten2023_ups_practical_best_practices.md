# Ultraviolet photoelectron spectroscopy: Practical aspects and best practices — Whitten (Appl. Surf. Sci. Adv. 2023)

> slug `whitten2023_ups_practical_best_practices` · DOI `10.1016/j.apsadv.2023.100384` · type `methods (외부 tutorial, 계산無·재료결과無)` · PDF `82ea256b-…01._Ultraviolet_photoelectron_spectroscopy….pdf` · digested `2026-06-26` · status ✅
> **저자**: James E. Whitten (단독, Dept. of Chemistry, University of Massachusetts Lowell, MA, USA) · Applied Surface Science Advances **13** (2023) 100384 · open access CC BY-NC-ND
> **태그**: `[외부]` `methods` — UPS(자외선 광전자분광) 실전 best-practice 튜토리얼. **argyrodite 논문 아님 · 우리 그룹 아님 · 재료 수치 비교 대상 아님.** 보관 이유 = UPS는 우리 DFT가 계산하는 **VBM·일함수(Φ)·이온화에너지(IE)** 를 *실험으로 재는 바로 그 기법*. "우리 계산값을 어떻게 측정하나"의 레퍼런스/치트시트.

---

## 0. 이 digest를 읽는 법 (왜 이걸 먹였나)
이 논문은 **재료 결과가 아니라 "UPS 스펙트럼을 어떻게 의미 있게 얻고 어떻게 제대로 보고하나"** 의 실전 가이드다. 따라서 일반 digest 양식(σ/Ea/ESW…)이 아니라 **best-practice 체크리스트**로 정리한다. 목표: 이 MD를 읽으면 = UPS 일함수·VBM 추출 cheat-sheet를 손에 든 것.

우리에게 중요한 단 하나의 연결: **UPS = valence-side(가전자대) 측정.** 우리 DFT가 내놓는 (a) **VBM 위치**(`db/properties/electronic.json`, S 3p), (b) **일함수 Φ**(slab 진공준위 기준 — 우리는 아직 미계산), (c) **이온화에너지 IE = Φ + (E_F−VBM)** 를 **실험으로 재는 방법**이 정확히 UPS다. 우리 XPS core-hole 작업(`db/properties/xps_reference_sei.csv`, ORCA ΔSCF)이 *코어준위=화학상태*를 보는 것과 짝을 이뤄, UPS는 *가전자대+일함수=밴드정렬/전자이동*을 본다. 둘을 합치면 SEI/계면의 전자구조 전모.

> ⚠ **정직선언**: 이건 methods 논문이다. 우리와의 연결은 "**이것이 우리가 계산한 VBM/Φ를 *측정하는 방법*이다**"이지 **재료 수치 일치/불일치가 아니다.** comparison_vs_ours 물성 4축(A 이온/B 산화/C 기계/D 전자)에 **행으로 넣지 않는다**(§7). 단 §6(UPS↔CV↔DFT 위계)는 우리 oxidation 보고서가 이미 쓰고 있는 그림이라 거기에 닻을 내린다.

---

## 1. 한 줄 요약
**UPS는 He 방전램프(He I 21.22 eV / He II 40.81 eV)로 가전자대 전자를 광이온화해 표면의 가전자대 구조·일함수(Φ)·이온화에너지를 재는 기법.** 스펙트럼 얻기는 쉬우나 *의미 있게* 얻기는 어렵다 — 핵심 난관은 **시료 표면 청정·표면 대전(charging) 제거·시료 바이어스**. 이 논문은 (i) **2차전자컷오프(SECO)+바이어스로 Φ 측정**, (ii) **가전자대 onset 선형외삽으로 VBM/IE 측정**, (iii) **램프 안정화·대전 진단·기준선/관례** 의 실전 절차와 함정을 제공한다.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 저자 | James E. Whitten (단독), UMass Lowell, Dept. of Chemistry |
| 저널/년 | Applied Surface Science Advances **13** (2023) 100384 |
| DOI | 10.1016/j.apsadv.2023.100384 (open access) |
| 유형 | **방법론 튜토리얼/리뷰** (실측 예시 spectra 포함, **DFT·재료 신물성 없음**) |
| 범위 | 금속·반도체·흡착층·공액고분자 박막의 UPS 가전자대 측정 + 일함수 측정 + 데이터 제시 best-practice |
| 명시적 제외 | ARUPS(각분해)·싱크로트론·final-state effects·band bending 이론·스펙트럼 이론모델링 (참고문헌만 안내) |
| 키워드 | Helium lamp, Photoemission, UPS, UV light, Valence band, Work function |

## 3. UPS가 재는 것 & 광전자 과정 (3-단계 모델, Fig 1) ★
**원리**: 깊은 UV 광자(hν)가 시료에 입사 → 가전자대(core가 아니라 **valence**) 전자를 진공준위 위로 들뜸. XPS와 차이 = UV는 저에너지라 **코어 대신 가전자대** 전자를 방출.

**3-단계(Fig 1a–c)**:
1. **들뜸(a)**: hν가 가전자대 전자를 E_VAC 위로 → 가전자대의 근사 반영(들뜬 분포).
2. **수송(b)**: 표면으로 가는 도중 일부가 운동에너지를 잃음 → **2차전자(secondary electrons)** 생성. 잃는 양은 경로에 의존.
3. **방출(c)**: 진공준위 위 전자만 탈출 → 검출기는 **직접방출 가전자 + 2차전자**의 합을 본다. 저KE쪽은 2차전자가 지배.

**관측 스펙트럼 = 가전자대 신호 + 2차전자 배경.** 2차전자가 차단되는 저운동에너지 끝 = **SECO(secondary-electron cutoff, 2차전자컷오프)**.

**핵심 식 (금속/도전성 기판 위 흡착물에 유효)**:
$$\boxed{\Phi = h\nu - \text{SECO}} \quad (\text{Eq.1, SECO} = E_{\text{cutoff}}\text{를 } E_F \text{기준으로})$$
- **E_F 기준은 분광기(spectrometer)의 Fermi level** — 시료가 분광기와 전기적 평형(접촉)일 때만 시료=분광기 E_F. 평형 안 되면 측정 E_F ≠ 시료 E_F (중요한 함정).
- 등가로 스펙트럼 폭 $w$(=SECO에서 E_F까지 폭)로: $\Phi = h\nu - w$ (Eq.6). 두 식은 SECO를 어디에 두느냐의 차이.

**광원(He 램프)**:
- **He I = 21.22 eV** (2p→1s, 중성 He). 가장 흔함. 위성선 He Iβ/Iγ = 23.09/23.75/24.05 eV(수%) → 반도체 갭 근처 약한 위성구조 주의(빼줘야 함).
- **He II = 40.81 eV** (이온화 He). 더 높은 압력·낮은 강도, 더 표면민감. 위성 He IIβ 48.37 eV.
- 선폭 ~3 meV(원자전이라 매우 좁음) → **UPS 에너지분해능은 광원이 제한요인이 아님**(분석기·시료 불균일이 제한). 대조: 단색화 Al Kα FWHM ~0.35 eV.

## 4. ★★ BEST-PRACTICE 핵심 1 — 일함수(Φ) 측정 (SECO + 바이어스)
**왜 바이어스가 필요한가 (Φ 측정의 심장)**:
- 저KE 2차전자(특히 SECO 근방)는 운동에너지가 거의 0 → 분석기까지 못 가거나 미주(stray) 전기장에 휘어 **컷오프가 안 보임**. 분석기 일함수에 묻힘.
- 시료에 **음의 바이어스** $V_{\text{Bias}}$ (보통 **−5 ~ −12 V**)를 걸면 방출전자에 그만큼 운동에너지를 더 줘서 저KE 부분이 분석기로 들어와 측정됨. → **SECO를 깨끗이 띄우는 게 Φ 측정의 전제.**
- 바이어스원: **배터리(안정·전류적음)** 또는 **안정 DC 전원**(전압 가변 가능 → 분해능 최적화). +단자=장비 ground, −단자=시료 stub. 디지털 전압계로 정확히 읽어야.

**측정 절차 (Whitten 권장, Fig 4 flowchart)**:
1. 시료를 측정위치+바이어스 → 램프 점화·압력/전류 조정·**~10 min 안정화**.
2. 운동에너지 스캔(또는 평균) 취득 → **SECO 위치 기록**.
3. 2차 스캔 취득 → **SECO 동일하면 램프 안정**(다르면 불안정/대전).
4. 금속·도전성 반도체: 위에서 얻은 스펙트럼 신뢰.
5. 공액고분자/저도전 박막: **낮은 광강도**로 한 번 더 → SECO 달라지면 **표면 대전**(더 얇은 박막/낮은 강도로).

**가장 직접적인 Φ 측정 = 운동에너지 vs 광전자수 플롯에서 (바이어스 뺀) SECO 값을 읽기.** Whitten 명시: "the most straightforward method is to prepare a plot of photoemission intensity versus kinetic energy (with any applied bias subtracted). The work function will then be the SECO value."

**관례·변환 (E_F 기준 ↔ 진공준위 기준)**:
- 데이터는 보통 운동에너지로 취득 → 결합에너지로: $BE = h\nu - KE - V_{\text{Bias}}$ (Eq.3, 바이어스 부호 보존; 분광기 일함수는 보정 가정).
- 진공준위 기준으로 그리면 "**Ionization Energy(IE)**" 축; 이때 **SECO는 광자에너지(21.22 eV)와 같아짐** (Fig 6d에서 SECO=21.22 eV 확인). 흡착물을 기체상/이론과 비교할 때 IE 기준이 편리.
- $IE = BE + (h\nu - \text{SECO})$ (Eq.4) ; 결합해서 $IE = 2h\nu - KE - V_{\text{Bias}} - \text{SECO}$ (Eq.5).

**Φ 측정의 함정 (Whitten이 경고)**:
- **불균일("patchy")·거친·전기장 artifact 표면 → 가짜 2차 SECO**(예: TiO₂(110) Fig 7에서 ~16.9 *와* ~17.3 eV 두 컷오프; Helander et al. 논의). 어느 SECO를 쓸지 주관성 → 시료 청정·평탄·시료면이 분석기 입구에 수직이도록.
- **반도체 Φ는 재료뿐 아니라 표면구조·청정도에 의존** (금속은 "전자 빼는 최소E"=Φ지만 반도체는 가전자대 top이 일반적으로 E_F 아래라 그 단순정의 안 통함).
- **Kelvin probe와 비교**: Kelvin probe는 *상대* Φ(접촉전위차)·비접촉·대기가능이나 기준시료 필요. UPS와 일반적으로 잘 일치하나 단결정에서도 수백 mV 차 가능(W(110)+피리딘 예: UPS ΔΦ −2.3/−2.0 eV ↔ Kelvin −2.0/−1.9 eV, Fig 8).
- **XPS로 Φ 측정 비권장**: KE 스케일이 광자E 전구간(0~1486 eV)에서 선형이어야 하는데 그 정밀도가 측정정밀도를 제한 → "XPS is not generally recommended for surface work functions". UPS가 표면 Φ에 적합.

## 5. ★★ BEST-PRACTICE 핵심 2 — VBM / 이온화에너지(IE) 측정 (가전자대 onset 선형외삽)
**무엇**: 가전자대의 *낮은 결합에너지 끝(leading edge)* = **VBM(valence band maximum)** 또는 "valence band edge". 도전성 시료면 **E_F 기준**, 반도체면 진공준위 기준 IE로도.

**방법 = 선형외삽(linear extrapolation / tangent)**:
- 가전자대 onset에 **접선을 긋고 배경(≈0 counts)과의 교점**을 VBM/IE로 읽음.
- 예 (논문 실측):
  - **금(Au, Fig 5b)**: E_F 기준 가전자대(d-band)와 SECO. Φ = 21.2 − 16.8 = **4.4 eV** (다결정 Au 통상 5.3–5.5 eV보다 낮음 = 시료 dirty 경고).
  - **TiO₂(110)(Fig 7)**: 가전자대 edge **3.7 eV**(E_F 기준), SECO 16.9 eV → IE = 3.7 + (21.22−16.9) ≈ **8.0 eV** (vs vacuum). Φ(TiO₂) ≈ 21.2 − 16.9 = **4.3 eV**.
  - **α-sexithiophene(Fig 6)**: HOMO onset(=가전자대 top) E_F 기준 **~0.9 eV** = "hole injection barrier"(유기소자 핵심 파라미터). IE 기준 피크 8.0/6.4/5.6 eV(티오펜 π) — 진공준위 기준으로 그려야 일함수 다른 시료끼리 같은 IE 피크가 정렬됨.

**오차/주의 (어디서 오나)**:
- **E_F의 유한 sharpness**: 0 K 가전자대 top 정의지만 유한온도+분광기분해능으로 **E_F가 약간 번짐**(금속 DOS가 전도대로 살짝 새 보임). E_F edge = Fermi함수 ⊗ Gaussian(분해능) convolution으로 모델 가능.
- **표면오염이 갭 내/근처 약한 상태를 만듦** → 반도체 갭 근처 작은 DOS 측정 시 큰 간섭, **빼줘야**.
- **He I vs He II**: He II는 더 표면민감 + 단면적 비 달라짐 → 같은 시료라도 가전자대 상대강도 변함(궤도성격 판별엔 유용).
- **검출깊이(sampling depth)**: IMFP λ ~5–10 Å(KE 40–50 eV, IMFP 최소 근방). 3λ ≈ **10–20 Å** = 검출깊이, He II는 약간 더 얕음. Beer-Lambert $I=I_0\exp(-d\cos\theta/\lambda)$ (Eq.2) — θ=0에서 깊이 λ/2λ/3λ가 신호의 ~63/86/95%. → **UPS는 극표면 민감**(시료 청정 결정적).

## 6. ★ BEST-PRACTICE 핵심 3 — 청정·대전·램프·기준·관례
**시료준비·표면대전 (insulator의 적):**
- **UPS는 절연체에 직접 못 씀** — 방출 전자가 만든 비보상 양전하 buildup이 예측불가 전기장 → 저KE 전자 궤적/KE를 망쳐 측정불가. (XPS는 flood gun 보정 가능하지만 UPS 저KE 영역엔 부적합.)
- **시료 stage를 ground 대비 음으로 바이어스** + **금속/도전 기판 위 박막**으로 측정. 두꺼운 절연막은 대전 → 더 얇게.
- 공액고분자/나노입자 박막: **도전층(Au/ITO)에 *상부면*을 silver paint로 연결**(기판 뒷면 아님). 핀홀 없는 연속막(spin-coat 농도조절), 적정두께(예: P3HT 350 Å, poly(3-hexylthiophene) 적정 ~1000 Å 미만). 박막 두께 여러 개 측정해 **대전 없음 확인**.
- **대전 진단 3종**: (a) **두께 시리즈** — 200/400 Å 스펙트럼 동일하면 정상, 더 두꺼워 저KE shift/소멸 시 대전; (b) **광강도 변화**(Al 필터로 ×1/10) — SECO/모양 안 변하면 대전없음(Fig 4 우측분기); (c) **바이어스 전압 변화**(배터리 대신 가변전원) — 여러 바이어스서 SECO 동일하면 전기장 영향 없음.
- 합성반도체(ZnO·TiO₂ 등 wide-gap oxide)는 결함·sputter·환원처리로 도전성↑면 metal처럼 측정 가능.

**He 램프 운전 (실전 노하우):**
- 차동배기(2단)로 분석실 압력 ≪ 방전부. 점화: 방전부 ~1 Torr·고전압 ~5 kV로 "strike". 점화 후 압력 낮춤, **peach색 글로우 = He I**.
- He II 키우려면 He 유량↓ → 글로우 peach→white→pale blue, **소멸 직전 최저압이 He II 최대**. 단 He II 안정유지 어려움(가열 outgassing·He 순도 의존). 100% He II는 비현실적; 보통 He I 지배.
- 분석실 He I 운전압 ~low 10⁻⁷ Torr. 단 큰 단면적+21.22 eV → **검출기 과부하 주의**(gain 낮춰 시작). 저자 램프(UVL-Hi/VG Microtech): He I 1 kV·30 mA.
- 위치·압력 미세변동이 큰 스펙트럼 변화 → **여러 spot 측정으로 재현성 확인**, 보통 **스캔 5회 평균**.

**에너지 기준·교정·분해능:**
- **기준 = 청정 금속(Au/Ag)의 E_F** (sharp Fermi edge). 분광기 E_F = 시료 E_F (접촉 평형 가정).
- 통상 종합분해능: **UPS ~100–200 meV**, XPS ~500 meV(전용장비는 더 좋음). UPS 분해능 제한 = 광원(매우 좁음) 아니라 **분석기(pass energy)+시료 불균일**.
- 분석기: 현대는 **CHA(반구형, HSA/hemispherical sector)** 주류, FAT(고정분석기투과, 일정 pass energy=일정 분해능) 권장, pass E 1~수백 eV(작을수록 분해능↑·투과↓). UPS는 KE 폭 좁아(5–30 eV) 가장 작은 pass E 불필요. CMA(원통거울)도 가능하나 분해능·S/N 열위.

**데이터 제시 관례 (Whitten의 reporting 권고):**
- **abscissa 명확히 라벨**: "Binding Energy"(E_F 기준) vs "Ionization Energy"(진공준위 기준) — 캡션/본문에 *어느 기준인지* 반드시 명시(일함수 다른 시료 비교 시 IE 기준 아니면 같은 궤도가 안 정렬).
- BE를 양수/음수로 쓰는 관례 혼재(궤도가 E_F 아래라 음수 쓰는 저자도) — 둘 다 허용, 일관성.
- **보고 시 반드시 포함(논문 권장 체크리스트)**: ① 시료준비/마운트, ② 분광기 제조사·모델·광원·광자E·pass E(CHA·FAT 여부), ③ base pressure·UPS 중 압력, ④ 시료면–분석기입구 각도·**시료 바이어스**, ⑤ 분광기 교정법, ⑥ E_F/진공 기준 명시, ⑦ SECO·HOMO/VBM onset 결정법.

## 7. 우리 DFT/실험과의 연결 ★★ — **PRIMARY: 산화안정성 (valence-side 관측량)**
> **한 줄 프레임: UPS = 산화안정성을 지배하는 VBM/IE(이온화에너지)를 *실험으로 재는 기법* — 우리 grand-potential 산화분석의 valence-side 짝.** 깊은 VBM(큰 IE, 가전자 전자를 빼기 어려움) ↔ 높은 산화 onset / 더 산화안정한 전해질. UPS는 우리 DFT가 계산하는 *산화 관련 VBM*과 *산화 onset*을 **bracket**하는 실험 probe다.
>
> **이건 재료 수치 비교가 아니라 측정-방법 매핑이다** — "우리가 계산한 산화 관련 VBM/onset을 *어떻게 측정하나*". comparison_vs_ours 물성축(A/B/C/D)에 행으로 넣지 않는다(methods 논문이므로). 단 **우리 oxidation 보고서가 이미 UPS↔CV↔DFT 위계를 명시적으로 쓰고 있어**(`kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md` §6) 그 그림의 *방법론 원전*으로 닻을 내린다.

### 7-1. ★ UPS = 산화안정성의 valence-side 관측량 (VBM/IE 깊이 ↔ 산화 onset)
**물리 (왜 UPS가 산화안정성과 직결되나):**
- **산화 = 가전자대에서 전자를 빼는 사건.** 그 난이도를 정하는 양이 **이온화에너지 IE**(= 진공준위−VBM, "가전자 전자 하나 빼는 데 드는 에너지"). 분자 직관으로는 **−E(HOMO) ≈ IP**(Koopmans, 수직 이온화) → **VBM/IE가 깊을수록(IE 큼) 산화 onset이 높음 = 더 산화안정.**
- **UPS가 재는 양 = 바로 이 VBM/IE다** (§5: 가전자대 onset 선형외삽 → VBM(E_F 기준) 또는 IE(진공준위 기준)). 즉 **UPS는 산화안정성의 *밴드엣지 관측량*을 직접 측정하는 실험기법**. 우리 보고서 §6 "UPS가 실제로 재는 것 = VBM + Φ → IE = 수직이온화 = 밴드엣지"가 정확히 이 논문의 Eq.4/§3.1.
- **우리 DFT의 VBM이 그 계산판**: comp1 **VBM = S 3p** (`electronic.json`: comp1_v3 VBM 2.48 eV·gap 1.76 / modelc_v3 VBM 2.72·gap 1.82, QE PBE k=6×6×6, S 3p ~91%). **UPS VBM onset 외삽 = 우리 PDOS VBM(S 3p)의 실험 카운터파트.** 산화의 *화학적 주역*(S²⁻→폴리설파이드)이 곧 VBM 성격(S 3p)이라는 우리 결론을, UPS가 "VBM=S-유래 상태, IE 깊이"로 실측해 받쳐줄 수 있다.

**그러나 — UPS(밴드엣지)와 grand-potential(분해열역학)은 산화안정성의 *두 다른 정의*이고, 둘 다 필요 (보고서 핵심):**
- 우리 보고서(`…VBM_vs_grandpotential…`)의 thesis = **분해형 고체전해질의 산화 onset은 VBM(밴드엣지)이 아니라 grand-potential 분해창으로 본다.** 이유: 재료가 *밴드엣지에 닿기 전에 상으로 분해*하므로, **밴드엣지(VBM/UPS) 창은 실제 열역학 분해창을 2–3배 과대평가**(Schwietert 2020 Nat. Mater.: "band-gap window"(과대) vs "decomposition window"(실제) 분리).
- **그래서 UPS는 산화안정성의 어느 부분을 주나** — *밴드엣지(상한·낙관적) 관측량*. **위계** (보고서 §6 그대로): grand-potential(가장 좁음/보수적·진짜 분해 onset) ≤ CV/LSV(passivation으로 약간 넓어짐, 우리 2.14 V의 실험짝) ≪ **UPS 밴드엣지(가장 넓음/낙관적)**.
- **UPS가 우리 두 관점을 *adjudicate(판정)*하는 법**: UPS는 (a) **측정된 VBM/IE** → 우리 **DFT VBM 검증**(같은 밴드엣지 양)과 (b) 그 측정 VBM이 **실제 산화 onset(CV)와 얼마나 벌어지나** → "밴드엣지 창이 분해창을 얼마나 과대평가하나"를 *실험으로 정량*. 즉 UPS-VBM vs CV-onset 격차 = 우리 보고서가 주장한 "밴드엣지 ≫ 분해창"의 실측 증거.

### 7-2. ★ 우리 자체증거가 "UPS-VBM 단독 ≠ 산화안정성"을 보여줌 — 그리고 dopant 스크리닝 test
- **보고서 §8의 결정적 데이터**: comp1/modelc는 **VBM이 다른데(절대 VBM Δ~0.32 eV)도 산화 onset이 둘 다 2.14 V로 동일**(grand-potential, S²⁻→폴리설파이드 limited). → **UPS로 VBM만 재서 "Cl-rich가 산화창 0.3 V 다르다"고 읽으면 틀림.** 산화는 밴드엣지 위치가 아니라 *S²⁻ 분해화학*이 결정. UPS-VBM은 **band-edge 관측량이지 분해 onset이 아님**을 우리 두 시료가 자체증명.
  - (주의: 위 ~0.32 eV는 절대 VBM(정렬 미보정·§7-3). `electronic.json` 수렴 k-mesh에선 comp1/modelc gap이 1.76 vs 1.82로 거의 같음(Δ−0.06) — 밴드갭은 Cl 함량에 둔감. 어느 쪽이든 **onset 동일(2.14 V)**이라는 결론은 robust.)
- **★ dopant 스크리닝에 UPS가 주는 깨끗한 test** (`db/properties/oxidation_stability_cascade.csv`): 우리 cascade는 dopant별 grand-potential 산화 onset을 갖는다 — 대부분 **2.14 V(=S²⁻-limited, dopant가 limiting reaction을 안 바꿈)**, 그러나 일부는 *limiting reaction 자체를 바꿔* onset이 오름: 예 **B2O3 ox=2.317 V**(undoped 2.14 대비 +0.18). **여기서 UPS의 역할**: "VBM을 깊게 만든다고 알려진 dopant가 *실제로 측정 산화 onset을 올리나*"를 UPS(VBM/IE) + CV(분해 onset)로 *동시에* test. 두 가지 결과로 갈림 —
  - dopant가 **VBM은 깊게(UPS IE↑) 했는데 grand-potential onset은 그대로(2.14, S²⁻ limited)** → 우리 보고서 결론 재확인(밴드엣지≠분해 onset, S²⁻가 lim).
  - dopant가 **limiting reaction을 바꿔 onset↑(B2O3형)** → 이땐 VBM 깊어짐과 onset↑이 *함께* 가는지 UPS로 검증 → "VBM 깊이 ↔ 산화안정"이 *언제* 성립하는지(limiting chemistry가 anion p-band일 때) 판별.
  - → **UPS = 우리 cascade onset(분해열역학)과 VBM(밴드엣지)이 dopant마다 같이 가나 따로 노나를 실험으로 가르는 도구.** (cf. comparison §D 인사이트: "작은 gap scatter ≠ σ_e / 큰 도핑변화 = 전자구조 바뀜" — 산화 onset도 동형: dopant가 limiting reaction을 바꿔야 VBM↔onset 연동.)
- **VBM 성격이 onset을 지배하는 일반법칙** (comparison §D, [Rupp]+우리 LLZO): **산화 onset ≈ 음이온 p-band(VBM) 깊이** — S 3p(얕음)→LPSCl onset 2.256 V vs **O 2p(깊음)→LLZO 2.88 V (+0.63)**. 이건 정확히 "VBM 깊을수록 산화안정"의 cross-material 증거이고, **UPS가 S 3p vs O 2p VBM 깊이를 실측**해 받친다. → 우리 O-doping(Nd₂O₃) 동기("O가 들어가면 VBM이 깊은 O 2p 쪽으로")의 *실험 관측량*이 UPS VBM/IE.

### 7-3. ★ DFT-VBM ↔ UPS-VBM 기준(referencing) 미묘함 (concepts/dos_vbm_efermi_methods.md와 직접 연결)
우리 `concepts/dos_vbm_efermi_methods.md`의 두 핵심 경고가 UPS로 *해결*되는 지점:
- **(a) DFT 절대 VBM은 셀마다 0점(셀 평균전위)이 달라 비교 불가** → 공통 기준 정렬(core-level/slab 진공준위) 필요. **UPS는 이 문제를 실험으로 우회**: UPS는 **분광기 E_F(또는 진공준위)라는 절대 외부기준**에 직접 잰다. 즉 UPS는 우리가 DFT에서 못 가진 "절대 기준 VBM"을 제공 → DFT VBM 검증의 외부 앵커.
  - 단 매핑 시: DFT VBM(E_F 기준, 절연체 E_F는 smearing artifact!)을 UPS(E_F 기준 또는 진공준위 IE)와 비교하려면 **기준을 맞춰야** — 우리 노트대로 절연체 DFT E_F는 못 쓰므로, **slab IP(진공준위−VBM)를 계산해 UPS의 IE와 비교**하는 게 엄밀(우리 H-목록의 "slab IP / absolute VBM" 항목과 정확히 같은 미래작업).
- **(b) PBE는 gap ~1 eV 과소·무질서 ±0.2–0.3 scatter** → 우리 gap(comp1 1.76 PBE)은 "wide-gap insulator" 수준으로만. UPS는 **점유측(VBM)만** 직접 줌(빈자리 CBM은 **IPES/역광전자분광** 필요). 따라서 UPS+IPES 합쳐야 실험 gap; UPS 단독으론 VBM만 검증.
- **함정 공유**: UPS VBM = **표면민감(~1–2 nm)·수직(vertical) 이온화** → 표면오염/band bending에 취약, adiabatic 분해와 또 다름(보고서 §6 caveat). DFT bulk VBM과 직접 등치 전에 표면효과 고려.

### 7-4. (보조) XPS(코어) ↔ UPS(가전자대+Φ) 상보성 — 우리 core-hole 작업과 짝
- 우리 XPS 작업: `db/properties/xps_reference_sei.csv` + **ORCA ΔSCF core-hole**(P 2p 131.7→133.3 phosphate, S 2p 161.6, Nd 3d5/2 982.5 …) — **코어준위=화학상태/원소환경**(O-doping 전환·Nd³⁺ 생존)을 본다.
- **UPS = 같은 광전자분광의 valence-side 대응**: 가전자대 구조 + **일함수 Φ**(코어준위로는 못 봄) → **밴드정렬/전자이동**. XPS가 "어떤 결합·산화상태"라면 UPS는 "그 상이 전극과 어떻게 밴드정렬되고 전자가 어디로 흐르나".
- **합치면 SEI/계면 전자구조 전모**: (XPS) SEI 산물이 무엇이고(Li₃PO₄·NdPO₄·LiCl…) → (UPS) 그 산물층의 VBM/Φ가 어디라 전자가 차단/통과되나. 우리 sei_products.json의 wide-gap 절연산물(LiCl 6.65·Li₃PO₄ 5.73·Li₂O 5.24 eV) 논리는 **UPS로 VBM/Φ를 재서 "정공주입장벽이 깊다=전자적으로 막힌다"로 실험검증**할 대상.
- 실용 메모: XPS와 UPS는 *같은 장비*에서 가능(He 방전램프를 기존 XPS 분광기에 차동배기로 붙임) → 우리 협업 XPS 측정에 UPS를 *덧붙이기* 쉬움(논문 결론 "not difficult to add a differentially pumped UV lamp on an existing XPS").

### 7-5. (보조) 일함수 Φ ↔ 우리 "전자차단 SEI / σ_e가 dendrite 레버" 서사
- 우리 핵심 주장(slide 25, comparison §D/E): **wide-gap 절연 SEI(LiF/LiCl/Li₂O/Li₃PO₄/NdPO₄)가 전자를 막아(σ_e↓) dendrite 억제** (Nolan Type 3, [Kang] 리뷰 프레임; [KimICCF] LiF·[Li25] LiBr·[Lu] LiCl 실험).
- **Φ(일함수)와 VBM은 밴드정렬을 정한다** → 절연 SEI가 Li 금속/전극과 만나는 면의 **밴드오프셋·정공/전자 주입장벽**을 UPS Φ+VBM이 *직접 측정*. 즉 "이 SEI가 전자를 막나"의 실험 관측가능량 = **UPS로 잰 Φ·VBM(+IPES CBM)으로 만든 밴드정렬도**.
- 외부 사례(INDEX exp #20): **LiTaOCl₄ Φ 3.96 eV → S 치환 LiTaO₀.₅S₀.₅Cl Φ 4.54 eV** (Φ 튜닝으로 밴드정렬 조절) = UPS Φ가 SE 설계변수로 쓰이는 실제 예. 우리가 SEI/SE의 Φ를 *계산(slab)*하고 UPS로 *검증*하면 같은 무대.
- **단 honest**: Φ는 밴드정렬을 정하지 σ_e(전자전도도) 절대값을 직접 안 준다 — σ_e는 결함/carrier 지배(우리 slide25 교정·[Ma] gap+0.52인데 σ_e 1.2×만). UPS Φ/VBM은 *band-alignment 레버*, σ_e는 별도(defect calc/DC분극). 둘 섞지 말 것.

## 8. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 실전 교훈 |
|---|---|---|
| **1 (a,b,c)** | UPS 3-단계 모델: 들뜸(a)→2차전자 생성(b)→관측=가전자+2차 합(c). E_VAC·E_F·Φ·w·SECO·hν 정의 도식 | **Φ=hν−SECO, w=가전자대폭** 의 그림판. 우리 보고서 §6 "UPS가 재는 것"의 원전 도해 |
| **2** | He I UPS를 Binding Energy(좌, E_F 기준) vs Ionization Energy(우, 진공준위 기준) 두 축으로 동시 플롯. SECO·Φ·E_VAC·E_F 표시 | **기준 두 가지(E_F vs vacuum) 변환 핵심.** 진공준위 기준이면 SECO=hν. DFT VBM(E_F)↔UPS IE 매핑 시 필수 |
| **3 (a,b)** | 청정 Ag foil, He 램프 정상압 vs 저압 → He I/He II 비율 변화(a, KE축); He I+He II 겹쳐(b, BE축) Ag 4d. He II S/N 나쁨 | He II는 약하고 표면민감 — 압력으로 He I/II 조절. 측정조건 진단 예 |
| **4** | **신뢰 UPS 절차 flowchart**: 안정화(10min)→SECO 기록→2차스캔 SECO비교(램프안정)→금속/도전: 신뢰 / 고분자: 저강도 재측정(SECO 다르면 대전) | **우리 협업 UPS 측정 시 그대로 쓸 체크리스트.** 램프안정·대전진단의 표준절차 |
| **5 (a,b,c)** | 다결정 Au 130K. (a) KE축 2차전자peak+d-band, (b) BE축+접선으로 SECO 16.8→**Φ 4.4 eV**(=21.2−16.8, dirty 경고), (c) E_F 근방 확대(가전자대 top 약간 E_F 위로 번짐) | **선형외삽 Φ 측정 실측 예 + Φ 4.4<5.3–5.5(통상)=시료 dirty 진단.** Au E_F = 우리 에너지 기준 |
| **6 (a,b,c,d)** | α-sexithiophene/Au 40Å. (a) BE 전체, (b) E_F 근방 inset **HOMO onset 0.9 eV=hole injection barrier**, (c) 진공컷오프 SECO=17.17 eV, (d) **IE축 재플롯 → SECO=21.22 eV** π피크 8.0/6.4/5.6 eV | **HOMO onset=정공주입장벽**(유기소자); 진공준위 기준 변환 실측. 우리 절연 SEI "정공주입장벽 깊다=전자차단" 측정틀 |
| **7 (a,b)** | sputter-clean TiO₂(110) wide-gap oxide. (a) SECO 16.9 + **가전자대 edge 3.7 eV**→IE 8.0 eV, (b) 가전자대 edge 확대. 두 SECO(16.9·17.3) 불균일 artifact | **반도체 VBM(가전자대 edge) 외삽 실측** + **불균일 표면이 가짜 SECO를 만드는 함정**. 우리 oxide(LLZO 등)/SEI 측정 시 주의 |
| **8 (a,b)** | W(110)±피리딘(흡착) 90K. SECO 16.3(clean)/18.6(chemi)/18.3(multi) → Φ 4.9/2.6/2.9 eV. 흡착이 Φ 2.3/2.0 eV 낮춤 (Kelvin probe 2.0/1.9와 비교) | **흡착층이 Φ를 크게 바꾸는 실측** + **UPS vs Kelvin probe 교차검증**. SEI/계면층이 Φ(밴드정렬) 바꾸는 직접 예 |

## 9. Post-processing / 측정 후처리 ★
- **SECO 결정**: 저KE 컷오프에 **접선 외삽** → 배경 교점. 불균일 시 다중 컷오프 주의(어느 걸 쓸지 명시).
- **Φ 산출**: $\Phi = h\nu - \text{SECO}$ (바이어스 뺀 KE축에서 직접) 또는 $\Phi=h\nu-w$.
- **VBM/HOMO/IE 결정**: 가전자대 onset 접선 외삽(E_F 기준 VBM, 진공준위 기준 IE). $IE=BE+(h\nu-\text{SECO})$.
- **E_F edge 모델링**: Fermi함수 ⊗ Gaussian(분광기분해능) fit으로 E_F 위치·분해능 추출.
- **기준 변환**: $BE=h\nu-KE-V_{\text{Bias}}$ ; IE축이면 SECO=hν로 셀프체크.
- **도구**: 표준 광전자분광 분석기(CHA/FAT) 데이터 + 스프레드시트/피크피팅. (논문은 특정 SW 권장 없음; ARUPS/이론모델링·band-bending은 범위 밖.)
- **기록 방식**: Φ(eV)·VBM/HOMO onset(eV, 기준 명시)·SECO(eV)·바이어스(V)·pass E·각도·압력 — §6 reporting 체크리스트.

## 10. 주의/한계 (over-claim 방지) ★
- **이건 methods 논문**: 재료 신물성 0·DFT 0. **comparison_vs_ours 물성축에 행 추가 금지**, 우리 재료와 수치 "일치/불일치" 주장 금지. 연결은 "측정-방법 매핑"뿐.
- **UPS≠산화안정성**: UPS VBM은 band alignment용. 분해형 SE 산화 onset은 grand-potential/CV (우리 보고서 §6 위계). "UPS로 산화창" = 우리가 명시적으로 거부한 프레임 → **이 논문은 그 거부의 방법론적 근거**(UPS가 재는 건 수직 이온화=밴드엣지, 분해창 아님).
- **표면·수직 측정**: UPS ~1–2 nm 표면민감 + vertical ionization → bulk DFT VBM·adiabatic 분해와 직접 등치 금지. 표면오염/band bending 보정 필수.
- **절연체 직접 불가**: 우리 SE(wide-gap)/SEI는 절연성 → 대전 때문에 **도전기판 위 박막·바이어스·박막두께 시리즈** 없이는 측정불가. (우리가 실측 추진 시 가장 큰 실무장벽.)
- **VBM만, CBM 아님**: UPS=점유측. 실험 gap엔 **IPES/역광전자** 필요. UPS 단독으론 우리 gap(1.76/1.82) 검증 못 하고 VBM만.
- **Φ는 σ_e 아님**: Φ/VBM=밴드정렬, σ_e=결함/carrier. UPS로 "전자차단 정도(σ_e)"를 직접 못 잼 — 밴드정렬·주입장벽까지만.
- **단색화 안 한 He 램프 위성선**(He Iβ/Iγ 23.1/23.75/24.05 eV)이 갭 근처 약한 위성 → 미세 가전자대 분석 시 빼야.
- 단독저자·tutorial → "best practice"는 **저자 실험실 관행 중심**(VG Scientific MKII ESCALAB/UVL-Hi). 장비·시료별 세부는 다를 수 있음(저자도 "in the author's experience" 명시).

## 11. 인용 가능 문장 (deck/paper용)
- "UPS is the experimental measurement of the valence-band maximum / ionization energy that governs oxidative stability — a deeper VBM (larger IE, harder to remove a valence electron) corresponds to a higher oxidation onset — so UPS brackets, on the valence side, exactly what our grand-potential oxidation onset and VBM-vs-grand-potential analysis compute." [Whitten 2023, our oxidation report §6]
- "The band-edge (VBM/UPS) view of oxidation is an upper bound: it overestimates the thermodynamic decomposition limit of a solid electrolyte by 2–3×, so UPS reports the measured VBM (to validate our DFT VBM) while the actual oxidation onset is the grand-potential decomposition window (CV experimentally) — consistent with LPSCl and Cl-rich LPSCl1.6 sharing an identical 2.14 V onset despite different VBMs." [Whitten 2023 + our oxidation report §6/§8]
- "Because the absolute DFT VBM is cell-referenced (and the insulator Fermi level is a smearing artifact), UPS provides the external absolute reference (spectrometer E_F / vacuum level) against which a slab-IP–corrected DFT VBM should be validated." [Whitten 2023 + concepts/dos_vbm_efermi_methods.md]
- "XPS (core levels = chemical state, our ORCA ΔSCF) and UPS (valence band + work function = band alignment / electron transfer) are complementary photoemission measurements on the same instrument; together they give the full electronic-structure picture of an SEI." [Whitten 2023]
- "A wide-gap insulating SEI blocks electron transfer by setting a deep hole-injection barrier — exactly the UPS observable (Φ + VBM, e.g. HOMO-onset = hole-injection barrier) that brackets our electron-blocking-SEI / σ_e-dendrite story." [Whitten 2023 + comparison §D/E]

## 12. 기법 용어 미니사전
- **UPS** (Ultraviolet Photoelectron Spectroscopy): UV 광자(He I/II)로 **가전자대** 전자 광이온화 → 가전자대 구조·Φ·IE 측정. (XPS=X선→코어준위.)
- **He I / He II**: He 방전 발광선, **21.22 / 40.81 eV**. He I 흔함, He II 더 표면민감·약함.
- **SECO** (Secondary Electron Cutoff, 2차전자컷오프): 스펙트럼 저KE 끝, 진공준위 위로 막 탈출하는 가장 느린 전자. **Φ=hν−SECO**. 진공준위 기준 플롯이면 SECO=hν.
- **2차전자(secondary electrons)**: 수송 중 KE를 잃은 전자 → 저KE 배경 지배. SECO를 만드는 주역.
- **일함수 Φ (work function)**: 진공준위−E_F. 금속=전자 빼는 최소E. SECO+바이어스로 측정. 표면구조·청정도 의존.
- **VBM / valence band edge / HOMO onset**: 가전자대 top(점유 최고준위). 선형외삽으로. 유기에선 **HOMO onset=hole injection barrier(정공주입장벽)**.
- **IE (Ionization Energy)**: 진공준위 기준 가전자대 위치. $IE=BE+(h\nu-\text{SECO})$. 일함수 다른 시료 비교 시 IE 기준 사용.
- **시료 바이어스 $V_{\text{Bias}}$**: 시료에 음전압(−5~−12 V) → 저KE 2차전자에 KE 더해 SECO를 분석기로. Φ 측정 전제.
- **표면대전(charging)**: 절연체서 비보상 양전하 → 전기장 → 저KE 전자 망침. UPS가 절연체에 직접 못 쓰는 이유.
- **CHA/HSA (반구형분석기)** · **FAT(고정분석기투과, 일정 pass E)** · **CMA(원통거울)**: 전자 운동에너지 분석기 종류. UPS는 CHA-FAT 주류.
- **IMFP λ / 검출깊이**: 비탄성평균자유행로 ~5–10 Å, 3λ≈10–20 Å=검출깊이. UPS 극표면 민감(Beer-Lambert Eq.2).
- **IPES(역광전자분광)**: UPS의 짝, **빈자리(CBM)** 측정. UPS+IPES = 실험 밴드갭.
- **Kelvin probe**: 비접촉 *상대* Φ(접촉전위차). UPS Φ 교차검증용(단결정서도 수백 mV 차 가능).
