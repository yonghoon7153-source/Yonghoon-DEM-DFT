<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. -->
# 다결정 NMC811 2차입자의 **입계 인장강도 745 MPa (Weibull, n = 3) · 인장 영률 165 ± 7 GPa · 나노압입 영률 138 ± 24 GPa (n = 29)** — FIB push-to-pull 미세인장 + SEM-DIC, 입계(intercrystalline) cracking 지배 — Sedlatschek · Gertlowski · Weber · Broeckmann (*J. Power Sources* 681, 240276 (2026))

> slug `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` · DOI `10.1016/j.jpowsour.2026.240276` · type `exp (micromechanics: FIB push-to-pull micro-tensile + SEM-DIC, Berkovich nanoindentation CSM/Oliver-Pharr, flat-punch compression, EBSD/TKD/STEM; FEM (Abaqus) specimen design)` · PDF `a4510882-1-s2.0-S0378775326010268-main.pdf` (9 pp, 본문만) · SI 미확보 (시편 기하 1 · 동영상 3 · 원자료 1) · digested `2026-09-25` · status ✅

> elements: Li, Ni, Co, Mn, O

> **읽은 범위**: 본문 9쪽 전부 (텍스트 추출 + 참고문헌 48편 전수) · 그림 8장 전부 크롭해 육안 확인.
> **라벨 규약**: `stated` = 본문에 숫자로 적힘 (쪽 표기) · `figure-read ≈` = 그림에서 읽음 (TREND 전용) ·
> `derived(ours)` = 우리가 논문 숫자로 한 산술 (§13 원장) · `2차 인용` = 이 논문이 **다른 논문 값을 전한 것** (원문 미확인).
> SI (Supplementary material 1–5) 는 없다 — SI 에 의존하는 내용은 전부 "SI 미확인" 으로 적었다.

---

## 0. ★ 이 카드를 연 질문 (SELF-51) — 결론 먼저

우리 원고 SI Table S2 의 *"NCM811 Young's modulus 140 GPa"* 출처가 **실재가 확인되지 않는 인용**
(원장 CL-90 · ⛔ 인용 금지 — "Wang 2020, *J. Power Sources* 470")이었고, 이 논문을 교체 출처로 쓰려 한다.
웹 검색 요약에 보이던 숫자를 **원문으로 대조한 결과**:

| 확인 항목 | 원문 | 판정 |
|---|---|---|
| 다결정 NMC811 나노압입 **E = 138 GPa, SD 24 GPa** | p. 4 §3 마지막 문단: *"29 indentations were processed and resulted in a Young's modulus of 138 GPa and a standard deviation of 24 GPa."* | ✅ 일치 |
| 압입 **29 회** · 최대하중 **5 mN** · 깊이 **≈150 nm** | p. 4 §3: *"The applied maximum indentation load of 5 mN resulted in indentation depths of approximately 150 nm."* | ✅ 일치 |
| (요약에 없던 한정어 ①) 포아송비 | p. 4 §2.5: *"A Poisson's ratio of 0.32 was assumed for NMC [43]"* | **ν = 0.32 가정** (측정 아님) |
| (한정어 ②) 방법 | p. 4 §2.5: Berkovich · CSM (압입 변형률속도 0.2 s⁻¹) · Oliver–Pharr [41] · reduced modulus 를 **표면으로 외삽해 기판효과 보정** [42] | 원문 그대로 |
| (한정어 ③) 압입 위치 | p. 2 §2.1: 전극을 Ar 이온 연마한 **단면** ("to allow for nanoindentation and EBSD") · p. 4: *"the elastically deformed zone covered several primary particles"* | **2차입자 단면 = 다결정 집합체** 값 (1차입자 한 개 값 아님) |
| (한정어 ④) 시료 상태 | p. 2: *"a commercial NMC811 electrode"* · p. 6: *"In this study, lithiated NMC was examined."* | 공급사 **n/a** · 사이클 이력 **n/a** (균열은 "electrode manufacturing process" 기원으로 기술) |
| 경도 H (자체) | 보고 없음 | **n/a** |
| 2차입자 113 / 139 / 143 GPa | p. 2: 있음 — 단 **NMC532** (NMC811 아님), 2차 인용 [27][28][29] | ⚠ 재료가 다르다 |
| "소결 NMC532 177.5 ± 19.5 GPa" | 본문·참고문헌 전수 검색 — **없음** | ⛔ 이 논문 값 아님 |

**한 줄 판정**: E_AM = 140 GPa 는 **다결정 NMC811 (우리 AM_P)** 에 대해 이 논문으로 방어된다 (나노압입 평균의 +1.4 %,
Hertz 가 실제로 보는 E/(1−ν²) 로는 −2.9 %). ⚠ 우리 **AM_S (단결정 규약)** 는 이 논문이 잰 대상이 아니다.
K_IC 는 이 논문이 **재지 않았다** (0.271 MPa√m 을 Sharma 2023 에서 빌려 씀). 자세한 판정은 §7.

---

## 1. 한 줄 요약

RWTH Aachen 그룹이 상용 NMC811 전극의 **2차입자 내부에서 직접 FIB 로 깎은 push-to-pull 미세인장 시편**
(게이지 ≈2.7 µm × 500 nm × 1.3 µm, 1차입자 ≈0.6 µm 가 폭 방향으로 몇 개)을 SEM 안에서 당기고 Pt 점 2개의 DIC 로
변형률을 재서, 다결정 NMC811 의 **입계 수준 인장강도 (Weibull σ_ch = 745 MPa, m = 6.91, n = 3)** · **인장 영률
165 ± 7 GPa** · **파괴변형률 ≈0.4 %** 를 처음 보고하고 나노압입 (**138 ± 24 GPa, n = 29**) 으로 교차검증했다.
압축·인장 모두 **취성 + 입계 파괴 지배** (EBSD 로 드문 입내 파괴 2 grain, STEM 으로 게이지 안 전위밀도 약간 증가).
문헌 K_I = 0.271 MPa√m 을 빌려 G_crit = 0.53 J m⁻², **입계 강성 S_gb = 521 GPa µm⁻¹** 를 **유도**했다.
입자 통째 압축 (Brazilian 유사) 강도 문헌값 (≈170–210 MPa) 보다 **≈4× 높은** 이유 = 단축 응력 상태 · 표면 거칠기 · 크기 효과.
⇒ 우리에게는 **(i) AM 영률 입력의 교체 출처, (ii) 입자 내부(sub-particle) 파괴 모델의 첫 정량 입력 세트** 다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Tobias Sedlatschek**\* (a,b; 교신) · Leonhard Gertlowski (a,b) · Felix Weber (b) · Christoph Broeckmann (a,b) |
| 소속 | a Institute for Materials Applications in Mechanical Engineering (IWM), RWTH Aachen University · b Institute of Applied Powder Metallurgy and Ceramics at RWTH Aachen e.V. (둘 다 Augustinerbach 4, 52062 Aachen) |
| 저널 | *Journal of Power Sources* **681** (2026) **240276** (9 pp) |
| DOI / PII | `10.1016/j.jpowsour.2026.240276` / S0378775326010268 |
| 이력 | 접수 2026-01-20 · 수정 2026-04-15 · 채택 2026-04-28 · 온라인 2026-05-08 |
| 라이선스 | Open access, **CC BY 4.0** |
| 자금 · 이해상충 | 특정 연구비 **없음** (stated) · 이해상충 없음 |
| 데이터 | *"Data will be made available on request."* · SI 5종 (①변형 전 시편 기하 ②압축 동영상 A ③압축 동영상 B ④인장 동영상 ⑤대표 하중–변위 원자료) — **미확보** |
| 소재 | 상용 **NMC811** (LiNi₀.₈Co₀.₁Mn₀.₁O₂) **전극** — 고분자 바인더 포함 (p. 2). 전극 종류(액체계 LIB 여부)는 명시 안 됨, 도입부 맥락은 액체전해질. 공급사 n/a · 사이클 이력 n/a · "lithiated" |
| 연구유형 | 실험 미세역학 (FIB push-to-pull 미세인장 + SEM-DIC, 나노압입, flat-punch 압축, EBSD/TKD/STEM) + FE (Abaqus) 시편 설계 |
| 원문 키워드 | Nickel rich cathode · Particle compression · Interface characterization · Geometry optimization · Finite element simulation |
| 감사 표기 | 시편 기하 최적화 Changrun Wu · 이온 연마 Alexander Schwedt · 나노압입 Lina Schwering · EBSD master pattern Siyang Wang · EBSD 분석 Kai Donnerbauer · FIB Malte Schmachtenberg |

## 3. 핵심 수치 ★

### 3.1 헤드라인 (전부 stated — 쪽 표기)

| 물성 | 값 | 조건 | 쪽 | 비고 |
|---|---|---|---|---|
| **나노압입 E** (다결정 2차입자 단면) | **138 GPa, SD 24 GPa, n = 29** | Berkovich, CSM 0.2 s⁻¹, P_max 5 mN → h ≈150 nm, Oliver–Pharr, E_r 표면 외삽 보정, **ν = 0.32 가정** | p. 4 (§2.5 방법 · §3 결과) | 탄성영역이 1차입자 여러 개를 덮음 = 미세인장과 비슷한 시험 체적 |
| **미세인장 E** | **172 · 168 · 156 GPa → 평균 165, SD 7 GPa (n = 3)** | 4 시편 중 1 개 제외 (Fig. 6a 회색) | p. 4 §3 | SD 7 = 모집단 SD (표본 SD 는 8.3 — §13) |
| **파괴응력 = 입계 강도** | **840 · 685 · 562 MPa** | 같은 3 시편, 취성 (소성 선행 없음) | p. 4 §3 | 파단면 = 입계 (Fig. 6b, TKD Fig. 8) |
| **Weibull (2-모수, MLE)** | **σ_ch = 745 MPa, m = 6.91** | n = 3 | p. 5 §4, Eq. (2) | 저자: *"to be interpreted with caution"* · m 6.91 = 소표본으로 산포 큼 |
| 파괴변형률 | **≈ 0.4 %** | | p. 5 §4 | 화학변형 (최대 ~10 % [45]) 보다 훨씬 작음 |
| 게이지 변형률속도 (DIC, 파단까지 평균) | **19.4 · 24.4 · 25.1 × 10⁻⁶ s⁻¹** | 비교: 화학변형 10 % · 1C → **27.8 × 10⁻⁶ s⁻¹** [45][46] | p. 5 §4 | ⇒ "1C 약간 미만" 의 변형률속도 |
| G_crit (입계, **유도**) | **0.53 J m⁻²** | 평면응력 G = K²/E (Irwin [48]), **K = 0.271 MPa√m 차용 [23]**, E = 138 GPa | p. 6 Eq. (3) | Han [39] 추정 0.46–0.69 J m⁻² 와 "good agreement" |
| **입계 강성 S_gb** (**유도**) | **521 GPa µm⁻¹** | S_gb = σ²/(2G), σ = σ_ch = 745 MPa (선형탄성 + 취성 가정) | p. 6 Eq. (4) · 초록 | *"can … be used in cohesive elements … when the grain boundary thickness is known"* |
| 1차입자(grain) 지름 | **598 ± 305 nm** | EBSD | p. 2 §2.1 | |
| 2차입자 지름 | **< ≈19 µm** (lognormal 적합 99 백분위) · 대부분 **< ≈10 µm** (80 백분위) | SEM (Tescan Clara) | p. 2 §2.1 | 거의 구형 |
| 게이지 치수 | ≈ **2.7 µm (L) × 500 nm (W) × 1.3 µm (t)** | 시편마다 실측해 응력 계산 | p. 3 §2.4 | |
| FE 응력 균일성 | 게이지 한쪽 모서리 최대 σ_vertical ↔ 반대쪽 최소 차이 **3.7 %** | 가상 1000 MPa, 선형탄성, E 138 | p. 3 §2.3 | 굽힘 제거 설계의 성능 지표 |
| 힌지 하중 분담 | 파괴하중의 **< 5 %** | 파단 뒤 재하중으로 힌지 강성만 측정 | p. 7 §4 | 일부 시편은 힌지가 파단 |
| DIC 분해능 | SEM 이론 **0.9 nm** · 실측 노이즈 **≈ < 3 nm** · 최대변위 **≈12–15 nm** → 노이즈 **≈20–25 %** | Savitzky–Golay 필터 (원자료 SI 5 — 미확인) | p. 7 §4 | 횡변형률은 분해능 아래 → **ν 측정 불가** |
| 경도 H (자체) | **n/a** | — | — | 이 논문은 자기 H 를 보고하지 않는다 |
| 파괴인성 K_IC (자체) | **n/a** | — | — | 측정 안 함 — 0.271 은 [23] 차용 |
| 포아송비 ν (자체) | **n/a** | — | p. 4 · p. 7 | 0.32 = [43] 가정값 |

### 3.2 시편 · 장치 · 시험 조건 (stated)

- **시료**: 상용 NMC811 전극. **Ar 이온 연마** (Jeol SM-09010 Cross Section Polisher) — 나노압입·EBSD 용. 표면 반응층은
  연마기 ↔ SEM **이송시간 최소화**로 피함 (p. 2).
- **장치 공통**: Tescan Clara SEM + **Bruker Hysitron PI 89 SEM PicoIndenter** (in situ). FIB = FEI Helios NanoLab G3 CX.
- **압축 파괴시험 (정성)**: FIB 로 2차입자 단면 연마 → **flat punch Ø 5 µm**, 최대변위 **5 µm**, 하중시간 **15 s**, 동영상.
  입자는 전극의 **고분자 바인더가 제자리에 붙잡는다** (p. 2 §2.2).
- **미세인장**: FIB 제작. *"Large and defect-free particles were chosen"* · 제작 중 결함이 보이면 **폐기** (p. 3).
  Pt 점 2개를 게이지 상·하단에 → 상대이동을 **ImageJ** 로 추적 (DIC) → Savitzky–Golay 필터. 게이지 하중은
  **모멘트 평형** `F_TS = F_Indenter · d_Hinge–Tip / d_Hinge–TS` (Eq. 1, 후처리 불요). **conospherical tip (반경 1 µm,
  Synton MDP)**, 압입기 변위속도 **0.37 nm s⁻¹**. 첫 시험은 시편 전체를 화면에 (SI 4 동영상), 이후는 **게이지만** 화면에
  넣어 변위 분해능을 높였다. 사후 SEM · **STEM** · **TKD**.
- **나노압입**: diamond **Berkovich** (Synton MDP). tip area function 을 **fused silica** 로 보정. **CSM**, 압입 변형률속도
  **0.2 s⁻¹**, **P_max 5 mN**. Oliver–Pharr [41] → reduced modulus → **표면으로 외삽**해 기판효과 보정 [42] (같은 1저자의
  LiFePO₄ 통계적 나노압입 논문) → ν = 0.32 [43] 로 E. *"Targeted"* = SEM 안에서 위치를 골라 찍음. n = 29.
- **FE (시편 설계)**: Abaqus **2.5D** (얇은 두께의 평면 모델), 선형 hexahedral · reduced integration, **선형탄성**
  (취성 예상), **E = 138 GPa** (나노압입값). 게이지에 가상 **1000 MPa** 가 걸릴 때 변형 해석. 한쪽 **고정**, 다른 쪽
  **힌지** = 구속 기준점과의 kinematic coupling. 하중 = **원호 세그먼트** (구형 팁 모사). 게이지 위·아래 팔의 강성을
  형상으로 맞춰 **굽힘 모멘트 제거** (Kiener 비대칭 기하의 결함 수정). FE 의 ν = **n/a (미기재)**. 변형 전 기하 = SI 1 (**미확인**).
- **EBSD**: spherical indexing (**OIM 9**), master pattern = Wang et al. [44]. 소수 오지수 점은 **[0 4 4 1] 축 90° pseudosymmetry
  보정**. 대상 = 제조 과정에서 이미 균열이 난 입자.

### 3.3 그림에서 읽은 값 (figure-read ≈, TREND 전용 — 인용 금지 정밀도)

- **Fig. 4b** (단면 입자 압축): 첫 하중 급락 ≈ **35–36 mN @ ≈1.1–1.2 µm** → ≈22 mN @ ≈1.45 µm → 재상승 ≈42 mN @ ≈3.5 µm →
  최대 ≈58 mN @ 5 µm → 제하 곡선이 ≈4 µm 에서 0 (잔류변위 ≈4 µm). ⚠ **저자 스스로 정량 불가 선언** (p. 4: 불규칙 단면 형상 ·
  유연한 주변 (바인더) · 내부 결함 미상 → *"no quantitative results could be derived"*).
- **Fig. 6a**: 제외된 **회색 곡선 끝 ≈ 990 MPa @ ≈0.46 %** (할선 ≈213 GPa — derived from figure-read). 검은 곡선 끝 변형률
  ≈0.49 / 0.41 / 0.36 % (stated σ/E 와 일치, §13). 네 곡선 모두 **거의 선형**, 저응력 (≲100 MPa) 에서 서로 겹친다.
  축: 응력 0–1300 MPa · 변형률 0–0.7 %.
- **Fig. 3**: 색 척도 σ_vertical **−1600 … +1000 MPa** — 상한이 1000 이라 **1000 초과 집중은 그림으로 구분 불가**. 게이지 = 균일 적색.
  압축 집중 = 하중점 노치 · 힌지 모서리 (청색).
- **Fig. 7 · 8** (같은 시편): 파단 위치 = 게이지 **상단 필렛 부근** (화살표; TKD 에서 상부 팔에 grain 두어 개짜리 그루터기가 남음).
  게이지 폭을 가로지르는 grain ≈ 2 개 (TKD).
- **Fig. 2a**: 다수 2차입자에 **이미 균열** (제조 기원), 일부 입자 내부에 기공.

### 3.4 ★ 이 논문이 **인용한** NMC 기계물성 값 (2차 인용 — 원문 미확인) + 서지 (참고문헌 목록 그대로)

> 매핑은 본문 문장 그대로다. 특히 113 / 139 / 143 GPa 는 *"Vasconcelos et al. [27,28] and Xu et al. [29] measured 113 GPa,
> 139 GPa and 143 GPa in NMC532, respectively."* (p. 2) 의 **"respectively" 순서**로 [27]→113, [28]→139, [29]→143 이다.
> 경도도 같은 문장 순서 (*"indentation hardnesses of 7.8 GPa, 8.9 GPa and 8.6 GPa"*).

| 값 (이 논문이 전하는 것) | 재료 · 방법 (이 논문의 기술) | 참고문헌 (p. 8–9, 원문 그대로; 아래첨자 x,y,z 는 평문으로 옮김) |
|---|---|---|
| **249 GPa (in-plane) · 210 GPa (out-of-plane)** | NMC811 **결정**, 제일원리 | [22] K. Min, E. Cho, Intrinsic origin of intra-granular cracking in Ni-rich layered oxide cathode materials, Phys. Chem. Chem. Phys. 20 (9045) (2018) http://dx.doi.org/10.1039/c7cp06615e. |
| **230 GPa (E) · 14.2 GPa (H) · 0.271 MPa√m (압입 인성, pop-in 해석)** | 본문: *"nanoindentation on NMC811 **pellets**"* — ⚠ 참고문헌 제목은 *"**single crystalline** NMC"* | [23] N. Sharma, D. Meng, X. Wu, L.S. de Vasconcelos, L. Li, K. Zhao, Nanoindentation measurements of anisotropic mechanical properties of single crystalline NMC cathodes for li-ion batteries, Extrem. Mech. Lett. 58 (2023) http://dx.doi.org/10.1016/j.eml.2022.101920. |
| *"moduli as low as 168 GPa"* (셋 합쳐서) | 제일원리 (조성·방향 여럿) | [24] H. Sun, K. Zhao, Electronic structure and comparative properties of LiNixMnyCozO2 cathode materials, J. Phys. Chem. C 121 (2017) 6002–6010, http://dx.doi.org/10.1021/acs.jpcc.7b00810. · [25] X. He, X. Ding, R. Xu, Anisotropic mechanical properties of LiNixMnyCo1−x−yO2 cathodes for li-ion batteries: A first-principles theoretical study, Acta Mater. 267 (2024) http://dx.doi.org/10.1016/j.actamat.2024.119751. · [26] J. Liu, W. Lin, Z. Wang, Y. Wang, T. Chen, J. Zheng, Elastic mechanics study of layered Li(NixMnyCoz)O2, Phys. Rev. Journals Energy 3 (2024) http://dx.doi.org/10.1103/PRXEnergy.3.013012. (저널명은 인쇄 그대로 — DOI 로는 PRX Energy) |
| **113 GPa · H 7.8 GPa** | **NMC532** 다결정 2차입자 | [27] L.S. de Vasconcelos, N. Sharma, R. Xu, K. Zhao, In-situ nanoindentation measurement of local mechanical behavior of a li-ion battery cathode in liquid electrolyte, Exp. Mech. 59 (2019) 337–347, http://dx.doi.org/10.1007/s11340-018-00451-6. |
| **139 GPa · H 8.9 GPa** | **NMC532** 다결정 2차입자 | [28] L.S. de Vasconcelos, R. Xu, J. Li, K. Zhao, Grid indentation analysis of mechanical properties of composite electrodes in li-ion batteries, Extrem. Mech. Lett. 9 (2016) 495–502, http://dx.doi.org/10.1016/j.eml.2016.03.002. |
| **143 GPa · H 8.6 GPa** ← **우리 "Xu 2017" 의 실체** | **NMC532** 다결정 2차입자 | [29] R. Xu, H. Sun, L.S. de Vasconcelos, K. Zhao, Mechanical and structural degradation of LiNixMnyCozO2 cathode in li-ion batteries: An experimental study, J. Electrochem. Soc. 164 (13) (2017) A3333–A3341, http://dx.doi.org/10.1149/2.1751713jes. |
| 인성 **추정** (0.271 과 *"good agreement"*) · *"H/3 로 인장강도 추정 불가"* 논거 | 리뷰 | [30] J.C. Stallard, L. Wheatcroft, S.G. Booth, R. Boston, S.A. Corr, M.F.D. Volder, B.J. Inkson, N.A. Fleck, Mechanical properties of cathode materials for lithium-ion batteries, Joule 6 (5) (2022) 984–1007, http://dx.doi.org/10.1016/j.joule.2022.04.001. |
| **188 MPa** (평균 파괴 인장강도) | **NMC111** 다결정 입자, flat punch | [32] D. Dang, Y. Wang, Y.-T. Cheng, Fracture behavior of single LiNi0.33Mn0.33Co0.33O2 particles studied by flat punch indentation, J. Electrochem. Soc. 166 (13) (2019) A2749–A2751, http://dx.doi.org/10.1149/2.0331913jes. |
| **207 MPa** | **NMC811** 다결정 입자, SEM in situ | [38] L. Wheatcroft, A. Bird, J.C. Stallard, R.L. Mitchell, S.G. Booth, A.J. Nedoma, M.F.L.D. Volder, S.A. Cussen, N.A. Fleck, B.J. Inkson, Fracture testing of lithium-ion battery cathode secondary particles in-situ inside the scanning electron microscope, Batter. & Supercaps 6 (5) (2023) http://dx.doi.org/10.1002/batt.202300032. |
| **172.8–210.6 MPa** · G 추정 **0.46–0.69 J m⁻²** | **NMC811** 미세구조별 입자 | [39] J. Han, R. Ghosh, F. Lin, K. Zhao, Microstructure informed mechanical properties and chemomechanical degradation of battery cathode particles, Exp. Mech. (2025) http://dx.doi.org/10.1007/s11340-025-01222-w. |
| **ν = 0.32** (가정값의 출처) | NMC | [43] J.-M. Lim, H. Kim, K. Cho, M. Cho, Fundamental mechanisms of fracture and its suppression in Ni-rich layered cathodes: Mechanics-based multiscale approaches, Extrem. Mech. Lett. 22 (2018) 98–105, http://dx.doi.org/10.1016/j.eml.2018.05.010. |
| 화학변형 **"of the order of 10 %"** | 단위격자 팽창/수축 | [45] A. Wade, A.V. Llewellyn, T.M.M. Heenan, C. Tan, D.J.L. Brett, R. Jervis, P.R. Shearing, First cycle cracking behaviour within Ni-rich cathodes during high-voltage charging, J. Electrochem. Soc. 170 (7) (2023) 070513, http://dx.doi.org/10.1149/1945-7111/ace130. |
| 1C 변형률속도 27.8 × 10⁻⁶ s⁻¹ 의 근거 | (PVDF 바인더 미세역학 논문) | [46] A.H. Iyer, P. Gupta, P. Gudmundson, A. Kulachenko, Measuring microscale mechanical properties of pvdf binder phase and the binder-particle interface using micromechanical testing, Mater. Sci. Eng. A 881 (2023) http://dx.doi.org/10.1016/j.msea.2023.145352. |
| 크기 효과 | ⚠ **Li 금속** 소규모 강도 논문 (NMC 아님) | [47] C. Xu, Z. Ahmad, A. Aryanfar, V. Viswanathan, J.R. Greer, Enhanced strength and temperature dependence of mechanical properties of li at small scales and its implications for li metal anodes, PNAS 114 (1) (2016) 57–61, http://dx.doi.org/10.1073/pnas.1615733114. |
| 기판효과 보정법 | 같은 1저자의 LiFePO₄ 통계 나노압입 | [42] T. Sedlatschek, M. Krämer, J.S.-L. Gibson, S. Korte-Kerzel, A. Bezold, C. Broeckmann, Mechanical properties of heterogeneous, porous LiFePO4 cathodes obtained using statistical nanoindentation and micromechanical simulations, J. Power Sources 539 (2022) http://dx.doi.org/10.1016/j.jpowsour.2022.231565. |

⚠ **이 논문에 없는 것** (전수 확인): *"소결 NMC532 177.5 ± 19.5 GPa"* 는 본문·참고문헌 어디에도 없다. *"Liu 2020 Nat. Energy"* ·
*"Quinn 2020 Joule"* (우리 K_IC 주석의 출처) 도 없다 — **"Quinn" 은 [9] G.D. Quinn et al., A novel test method for measuring
mechanical properties at the small-scale: the theta specimen, Ceram. Eng. Sci. Proc. 26 (2) (2005) 117–126 (시험법 논문)** 으로만
등장한다. 이 논문이 인용하는 Joule 논문은 [30] Stallard 2022 하나다.

## 4. 방법 ★ (실험 + FE 시편 설계)

### 4.1 문제 설정 — 왜 새 시편 기하가 필요했나 (p. 1–2, Fig. 1)
- 미세인장은 두 계열: **direct-pull** (Fig. 1a; 직관적이나 전용 장비·그립·정렬 문제) vs **push-to-pull** (어느 나노압입기로든 가능).
- push-to-pull 은 다시 ⓐ **전용 장치**에 시편을 얹는 방식 — Ganesan [5,6] (Fig. 1b; 적층제조판 [13]) · Hysitron [7] (Fig. 1c),
  1D·2D 재료에 확립 — 과 ⓑ **시편 자체를 push-to-pull 형상으로 깎는** 방식 — 두꺼운 단면까지 설계 자유. ⓑ 의 계보:
  theta 시편 (Durelli 1962 [8] → Quinn 소형화 [9], Fig. 1d; 리소그래피 [16] · FIB [17] · 적층제조 [18,19]) · Ding 의 열린 C 형 [10]
  (Fig. 1e) — 둘 다 **하중이 틀과 게이지로 나뉘어 게이지 하중을 직접 못 재고**, 게이지 변위 ≠ 인가 변위 → SEM 영상 **DIC** 가 필요 [20].
  Kiener [11] 의 **비대칭 전-FIB** 기하 (Fig. 1f) — 응력 상태·힌지 영향 미검토. Schwiedrzik [12] 의 **대칭** 기하 (Fig. 1g) —
  파괴인성용, 게이지 전체가 균일하지 않음.
- GB 강성은 일반적으로 **텐서**이고 결정 방위차에 의존 [21] → *"currently no grain boundary stiffness and strength data for NMC
  under uniaxial tensile load is available"* (p. 2, 저자 인식).

### 4.2 압축 파괴시험 (정성, Fig. 2b · Fig. 4)
flat punch 로 FIB 단면 입자를 눌러 **실시간으로 단면을 관찰**. 결과 = **입계 파괴** + **바인더 박리** + 기존 작은 균열에서 큰 균열
성장 (SI 3) + 하중 급락 = **취성**. 정량은 포기 (형상·주변·내부 결함).

### 4.3 시편 기하 최적화 (FE, Fig. 3)
Kiener 기하의 **비대칭 → 게이지에 굽힘 모멘트** (비균일·비단축) 를 없애려고, 게이지 **위·아래 팔의 강성을 형상으로 맞춰**
팔의 변형이 굽힘을 상쇄하게 했다. 결과: 게이지 양 모서리 σ_vertical 차 3.7 % · 실험 중 시편 변형·회전 매우 작음 → 단축 하중.
⚠ 가정: **선형탄성** — 소성하는 재료에서는 게이지 응력 상태가 균일·단축에서 벗어날 수 있다 (저자 한계 1).

### 4.4 미세인장 + DIC (Fig. 6 · 7 · 8)
하중은 모멘트 평형 (Eq. 1) 으로, 변위는 Pt 점 DIC 로. 게이지 치수는 시편별 실측. 결과는 선형 → 급파단.
**4 곡선 중 1 곡선 제외** (*"may be due to the pronounced anisotropy of NMC and the small number of grains involved"*).

### 4.5 나노압입 (검증용)
§3.2 조건. 깊이 150 nm 이지만 **탄성영역은 훨씬 커서 1차입자 여러 개를 덮으므로 시험 체적이 미세인장과 비슷** → 두 E 가
비교 가능하다는 논리 (p. 4).

### 4.6 사후 분석
- **STEM** (Fig. 7): 가시적 소성 없음. 단 게이지 밖 기준 위치보다 **전위밀도 약간 증가** (사각형 2곳) → 1차입자의 **제한된 소성**
  신호. 단결정 NMC 에서는 소성이 **입내 균열의 개시 기구**라 중요. ⚠ **전·후 같은 위치 비교 불가** (최소 두께 제약) → 저자 "caution".
- **TKD** (Fig. 8): 입계 파괴 확인, 파단면 근처·게이지 전체에 **격자 왜곡 없음**.
- **EBSD** (Fig. 5): 제조 균열 입자에서 균열 대부분이 **입계를 따라감**, 드물게 **입내** (파단 양쪽 방위가 같은 grain 2개).
- **FIB 비정질화**: STEM·TKD 에서 의미 있는 비정질화 없음. 표면: 길이방향 줄무늬만 약간, **가로 노치 없음**.

### 4.7 입계 물성 도출 (p. 5–6)
1. 게이지 안 grain 수가 적고 파단면이 하중에 수직이라 가정 → **측정 파괴응력 = 파단면 위 입계들의 평균 입계 강도**.
2. 평면응력 가정: `G_crit = (K_I^crit)² / E` (Eq. 3, Irwin [48]), **K_I^crit = 0.271 MPa√m [23] (차용)** · E = 138 → **0.53 J m⁻²**.
3. `G_crit = ∫σ dδ = ½σδ = σ²/(2 S_gb)` (Eq. 4, 선형탄성 + 취성) , σ = σ_ch = 745 MPa → **S_gb = 521 GPa µm⁻¹**.
4. 리튬화 의존: *"Under the hypothesis that the lithium ions are stored in the crystal and not at the grain boundaries, it is assumed
   that the grain boundary strength varies little with the lithiation state"* — **가설, 미검증**. 탈리튬화로 결정이 약해지므로 grain
   변화와 GB 변화를 분리하기 어렵다고 저자가 인정.

### 4.8 ★ 입자 처리 (우리 축과의 대응)
- **이 논문이 재는 대상 = 우리 DEM 구 하나의 "안"**: 다결정 2차입자 = grain (≈0.6 µm) + 입계 (GB) 의 집합체.
- **이 논문의 모델 쪽 처리**: 시편 설계 FE = **균질 등방 선형탄성 연속체** (grain·GB 해상 없음) · 입계 물성 = GB 를 **선형 스프링 →
  급락 (취성)** 1-자유도 cohesive 로 봄 · 강도 통계 = 2-모수 Weibull (체적 결함 통계). **형상 소성 없음** (전위밀도 약간 증가뿐).
- **우리 DEM**: AM = **탄성 구** (LIGGGHTS `youngsModulus` 1.4e8 micro-unit = **140 GPa**, `poissonsRatio` **0.25**; AM_P·AM_S **같은 값**),
  **내부 grain/GB 없음**. 파괴 = 접촉 δ 또는 F 에 대한 **사후 분류** (Auerbach cone-crack 개시, K_IC 기반, `scripts/fracture_model.py`) —
  입자 형상 변화·파편 생성 없음. **우리 MPM**: AM = **동결 scaffold** (역학 응답 0).
- ⇒ 이 논문의 대상은 **우리 두 모델 어디에서도 해상되지 않는 스케일** — `comparison_vs_ours_DEM.md` **§G (sub-particle)** 축이다.
  frame [5] 로 말하면: 이 논문은 **입자 내부 역학의 반쪽**만 갖고, 전극 스케일 (패킹 · 수송 · 압밀) 반쪽은 **없다**.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Fig. 1** | 미세인장 방법 분류 (a) direct-pull (b) Ganesan 전용 장치 (c) Hysitron 전용 장치 (d) theta 시편 (Durelli · Quinn) (e) Ding C 형 (f) Kiener 비대칭 전-FIB (g) Schwiedrzik 대칭 — 적색 = 게이지 | GB 수준 역학이 필요할 때의 방법 지도. ⚠ "Quinn" 은 **theta 시편 시험법** 이지 NCM 인성 출처가 아니다 (우리 K_IC 주석과 혼동 금지) |
| **Fig. 2** | (a) Ar 이온 연마 전극 BSE 상 — 구형 2차입자, **다수에 제조 균열**, 일부 내부 기공 (스케일 10 µm) (b) FIB 단면 입자 (점선) + flat punch + 하중 방향, 바인더 영역 (작은 화살표) (스케일 3 µm) | 상용 캘린더링 전극 입자는 **처음부터 균열이 있다** → 우리 "t = 0 에 AM 무손상" 가정은 낙관적. 2차입자 PSD 백분위 (§3.1) |
| **Fig. 3** | 최적화 push-to-pull 기하의 FE σ_vertical 등고선 (변형 20배 확대). 게이지 균일 ≈1000 MPa, 좌하단 힌지(삼각 지지), 우측 고정, 상단 노치에 하중 | 시편 설계를 FE 로 검증하는 습관 (우리 d_h/dx 해상도 게이트와 같은 부류). 수치는 우리 모델에 안 넘어온다 |
| **Fig. 4** | (a) 압축 후 단면 입자: **입계 파단면 (A)** · 개별 1차입자 (B) · **바인더 박리 (C)** (b) 하중–변위: ≈35 mN 부근 급락 = "Fracture" (figure-read) → 재상승 → 5 µm 에서 제하 | 압축 (캘린더링·압밀과 같은 하중 부호) 에서도 **입계로 부서진다** = 우리 A10 "poly = 입계 내부 void" 가정과 같은 방향. 바인더 박리 → 전자 경로 소실 (σ_e) 기구 (저자 p. 5) |
| **Fig. 5** | EBSD IPF 지도 (범례 0001 · 1–100 · 1–210 · 0–110; 스케일 2 µm), 제조 균열 경로 (점선) + **입내 파괴 grain 2개** (화살표) | 입계 지배 · 입내 드묾의 증거. grain 크기 척도 (≈0.6 µm) |
| **Fig. 6** | (a) 응력–변형률 4 곡선 (선형 → 급파단, × = 파단점; 회색 = 제외) (b) 인장 파단면 SEM — **grain 면이 드러난 입계 파단** (스케일 200 nm) | E · σ_f 의 원천. **파단까지 선형** → 선형 cohesive 법칙 가정의 근거 |
| **Fig. 7** | 인장 후 게이지 STEM — 점선 = 게이지 윤곽 (의도적 오프셋), 화살표 = 파단면 (상단), 사각형 2 = **전위밀도 증가 영역** (스케일 200 nm) | NMC grain 은 완전 취성이 아니다 (제한된 소성). 압밀 응력에서 AM 을 탄성으로 두는 우리 처리에는 영향 없음 |
| **Fig. 8** | 인장 후 게이지 TKD — 파단면 2개 (화살표), 입계 파괴, 격자 왜곡 없음 (스케일 200 nm) | 입계 파단 확인 · 게이지 안 grain 배열 (폭 방향 ≈2 개, figure-read) |

### 5.1 크롭 색인 — `litdb/figures/sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile/`

자동 크롭 (`tools/litdb/extract_figures.py`, 300 dpi) 8장 **전부 열어서 확인** — 캡션 혼입 0 · 패널 라벨/축/범례/스케일바 잘림 0 →
수동 재크롭 **불필요**. 이 논문에는 **표가 없다** (표 크롭 대상 0).

| 파일 | 쪽 | bbox (pt, x0 y0 x1 y1) | px | 확인 |
|---|---|---|---|---|
| `fig_1.png` | 2 | 31.6, 49.8, 298.0, 175.6 | 1111 × 525 | ✅ a–g 7 패널 라벨 전부 |
| `fig_2.png` | 3 | 31.6, 49.5, 298.0, 422.1 | 1111 × 1553 | ✅ a/b · 스케일바 10 µm / 3 µm |
| `fig_3.png` | 3 | 300.6, 61.7, 567.0, 208.9 | 1111 × 614 | ✅ 색막대 σ_vertical [MPa] 전 구간 |
| `fig_4.png` | 4 | 300.6, 49.4, 567.0, 427.8 | 1111 × 1577 | ✅ a/b · 축 Load [mN] / Displacement [µm] |
| `fig_5.png` | 5 | 31.6, 49.1, 298.0, 336.5 | 1111 × 1199 | ✅ IPF 범례 · 2 µm |
| `fig_6.png` | 5 | 300.6, 49.5, 567.0, 402.8 | 1111 × 1473 | ✅ a/b · 축 Stress [MPa] / Strain [%] · 200 nm |
| `fig_7.png` | 6 | 31.6, 49.5, 298.0, 498.7 | 1111 × 1872 | ✅ 200 nm · 사각형 2 · 화살표 |
| `fig_8.png` | 6 | 300.6, 49.5, 567.0, 540.5 | 1111 × 2047 | ✅ 200 nm · 화살표 2 |

## 6. Post-processing ★

- **응력**: 모멘트 평형 레버비 (Eq. 1) × 압입 하중 ÷ 시편별 실측 단면적 — 힌지 몫 (< 5 %) 은 보정 안 함 (오차로 기술).
- **변형률**: Pt 점 2개의 상대이동 (ImageJ) = 가상 신율계 (virtual extensometer [20]) → Savitzky–Golay 평활. 노이즈 20–25 % 를
  "곡선이 거의 선형 + 노이즈 무작위" 로 정당화 (원자료 SI 5 **미확인**).
- **E**: 응력–변형률 기울기 — **적합 구간 미기재 (n/a)**.
- **강도 통계**: 2-모수 Weibull, **MLE** (Eq. 2). 우리 재계산이 **m = 6.911, σ_ch = 744.8 MPa** 로 재현 (§13).
- **입계 물성**: Irwin G = K²/E (평면응력) → 선형 cohesive S = σ²/(2G). 우리 재계산 **G 0.5322 · S 521.5 GPa µm⁻¹** 재현.
- **나노압입**: Oliver–Pharr + CSM + reduced modulus 표면 외삽 + ν 가정. **개별 압입값 분포 · 깊이 프로파일 · E_r · 팁 상수 보고 없음**.
- **변형률속도**: DIC 파괴변형률 ÷ 파괴 시각 → 1C 화학변형률속도 (10 %/3600 s) 와 비교.
- **결정학**: EBSD (OIM 9 spherical indexing + pseudosymmetry 보정) · TKD · STEM.
- **도구**: Abaqus (FE) · ImageJ (DIC) · OIM 9 (EBSD). 플롯 도구 n/a.

## 7. 우리 대비 ★ — DEM AM 입력 · 파괴 모델 (→ `our_dem_baseline.md` 는 정본에 값 없는 자리표시; 우리 값은 **작업 브랜치** 코드·CLAUDE.md 기준)

### 7.1 대조표

| 항목 | 이 논문 | 우리 (작업 브랜치) | 판정 |
|---|---|---|---|
| **E_AM — AM_P (다결정)** | 나노압입 **138 ± 24 (n = 29)** · 인장 **165 ± 7 (n = 3)** | **140 GPa** (`input_real_*.liggghts` `youngsModulus peratomtype 1.4e8 1.4e8 0.135e7` = AM_P · AM_S · SE; `fracture_model.E_AM`) | ✅ **나노압입 평균 +1.4 %** (z = 0.08; 평균의 95 % CI [128.9, 147.1] 안) · 인장 평균 대비 −15 %. 저자는 둘을 *"comparable"* 로 본다 |
| **E_AM — AM_S (단결정 규약)** | **잰 적 없음**. 인용: 제일원리 168–249 · [23] 230 (치밀/단결정) | **140 GPa** (type 2, AM_P 와 같은 값) | ⚠ **이 논문으로 방어 불가** — 인용값 기준 1.2–1.8× 부드럽다 (§7.3) |
| **ν_AM** | 측정 불가 · **0.32 가정** [43] | **0.25** (`fracture_model.NU_AM` "ceramic", 출처 없음) | ⚠ 출처 없음 — 그러나 Hertz 가 보는 **E/(1−ν²)** 는 149.3 vs 153.7 GPa = **−2.9 %** (ν 가정과 무관한 비교, §13) |
| E* AM–AM | (138, 0.32) → **76.9 GPa** (derived) | (140, 0.25) → **74.7 GPa** | −2.9 % |
| E* AM–SE (E_SE,eff 1.35, ν 0.30) | 1.4693 GPa (derived) | 1.4689 GPa | **−0.03 %** — AM 값은 AM–SE 접촉에 사실상 무관 |
| **K_IC — poly** | **측정 안 함.** 0.271 MPa√m 차용 [23] | **0.3** (`K_IC_AM_P`, 주석 "Quinn 2020 Joule 4, 2466" — 감사에서 찾을 수 없음) | 수치는 **+11 %** 근접. 그러나 이 논문은 **출처가 될 수 없다** (2차 인용) |
| **K_IC — single** | — (0.271 이 [23] 제목대로 단결정 값이라면 그것) | **1.0** (`K_IC_AM_S`, 주석 "Liu 2020 Nat. Energy 5, 304" — 찾을 수 없음) | ⚠ 이 논문이 인용한 **유일한 인성값과 3.7×** 차 (§7.4) |
| **H_AM** | 자체 **n/a**. 인용: **7.8 / 8.9 / 8.6** (NMC532 2차입자) · **14.2** (NMC811 펠릿) | `am_load_balance_jam.py` 기본 **4.0** (주석 "NCM811 압입 경도 문헌대 ≈ 3~6", 역산 3.83–3.85) · `fracture_model.H_AM` **6.0** (informational, 출처 미확인) | ⚠ **인용 4값 전부 우리 문헌대 3–6 밖** (§7.5) |
| 입계 강도 | **745 MPa** (Weibull m 6.91, n 3) · 파괴변형률 0.4 % | 없음 (파괴는 접촉 K 기반) | 새 입력 — 입계 해상 모델용 (§7.6) |
| 입자 단위 강도 | 인용 172.8–210.6 (NMC811) · 207 (NMC811) · 188 (NMC111) MPa | 없음 | DEM 입자 파쇄 기준의 적절한 스케일 (원문 확인 후) |
| 파괴 모드 | **입계 지배** (압축·인장), 입내 드묾 | A10: SC = 계면 debond · **poly = 입계 내부 void** (`cycle_contact_ledger --poly-mode expand-void`) | ✅ poly 가정과 같은 방향 |
| 소재 · 전해질 | 상용 NMC811 **전극** (액체계 맥락), 리튬화 상태 | NCM811 + LPSCl ASSB | 고체 기계물성이라 **값 전이 가능** — 단 공급사·1차입자 크기·내부 기공이 다를 수 있다 |

### 7.2 ★ E_AM = 140 GPa 판정 — **AM_P 에 대해 교체 출처 확보, 재계산 불요**
- 140 은 나노압입 평균 138 에서 **+1.4 %** (1σ 의 0.08 배). 인장 165 와는 −15 % 이지만, 논문 안에서도 두 측정이 **+20 % 벌어져**
  있고 저자가 "comparable" 로 본다 ⇒ 이 논문 하나로 정해지는 다결정 NMC811 집합체 E 의 폭은 **[138, 165] GPa**.
- **ν 가정이 달라도 비교가 무너지지 않는 이유** (derived(ours), §13): 나노압입이 실제로 제약하는 양은 (팁 순응성을 뺀 뒤)
  **E/(1−ν²)** 이고, Hertz 접촉 강성도 **같은 조합** E* = E/(2(1−ν²)) 으로 들어간다. 이 논문의 (138, 0.32) 는 **153.7 GPa**,
  우리 (140, 0.25) 는 **149.3 GPa** → **−2.9 %**. 같은 측정을 ν = 0.25 로 다시 표현하면 E = **144 GPa**.
- 영향 범위: AM–SE 접촉은 E_SE,eff (1.35 GPa) 가 지배해 **−0.03 %** (무의미). 남는 것은 **AM–AM 접촉**(힘사슬 강성 ·
  Auerbach P_c) 에서 −2.9 % 뿐. ⇒ SELF-51 의 *"값 자체는 측정 범위 안이라 재계산 불요 — 틀린 것은 출처다"* 와 정합.
- ⚠ 한정: 두 값 모두 **치밀·무결함 영역**의 값이다 (인장 = "large and defect-free particles", 압입 깊이 150 nm). 내부 기공·제조 균열을
  가진 **2차입자 통째**의 유효 강성은 더 낮을 수 있고 (Fig. 2a), 이 논문은 그것을 재지 않았다 (압축 시험은 정성).

### 7.3 ⚠ AM_S (단결정 규약) 는 이 출처 밖
우리 규약은 AM_S = 단결정 NCM · AM_P = 다결정 NCM 인데 (K_IC 도 둘로 나눈다), DEM 입력은 **둘 다 140 GPa** 다. 이 논문이 전하는
치밀/단결정 계열 값은 **제일원리 168–249 GPa · [23] 230 GPa** 로, 다결정 2차입자 값 (113–165) 보다 **높다** — 저자 본문:
*"Experimentally measured moduli on polycrystalline secondary particles are even lower"* · *"the modulus of sintered pellets is higher"*.
AM_S 를 200–230 GPa 로 올리면 AM_S–AM_S 의 Auerbach **P_c 는 ×0.70–0.61, δ_c 는 ×0.62–0.52** (derived, §13) — 압밀 거동에는
영향이 작지만 (AM–SE 지배) **AM_S 파괴 분류에는 1차 효과**. ⇒ Table S2 에 AM 이 하나의 행이라면 **"다결정 NCM811"** 이라고
한정해 적고, AM_S 는 별도 근거가 생길 때까지 "Assumed (same as polycrystalline)" 로 둔다.

### 7.4 ★ K_IC 1.0 / 0.3 판정 — **이 논문은 출처가 아니라 포인터다**
- 이 논문은 K 를 **재지 않는다**. p. 2: *"The indentation toughness of NMC811 was measured through the analysis of pop-in events …
  to 0.271 MPa√m [23] which is in good agreement with an estimation made by Stallard et al. [30]."* p. 6 에서 그 값을 **입계 K** 로
  빌려 G · S_gb 를 유도한다.
- 수치: 우리 **poly 0.3** 은 0.271 과 **+11 %** — Auerbach P_c ∝ K² 라 0.271 로 바꾸면 **P_c ×0.816 (−18 %)**, E/(1−ν²) 까지 바꾸면
  **×0.793**; δ_c ∝ K^(4/3) 라 **×0.873 / ×0.840** (derived, §13).
- ⚠ **single 1.0 과의 긴장**: [23] 의 제목은 *"… of **single crystalline** NMC cathodes"* 다. 0.271 이 단결정 압입 인성이라면
  우리 AM_S 의 1.0 은 그 **3.7×**, P_c 로 **×13.6** 과대다. 그러나 본문은 [23] 시료를 *"NMC811 pellets"* 로 적고 있어 **어느 쪽인지
  이 논문으로는 판정 불가** — [23] 원문이 필요하다.
- 원장 연결: 우리 주석의 *"Liu 2020 Nat. Energy 5, 304"* · *"Quinn 2020 Joule 4, 2466"* 은 이 논문에 **없다**. 이 논문의 Joule 인용은
  **[30] Stallard 2022 (Joule 6 (5) 984–1007)** 이고 "Quinn" 은 **theta 시편 시험법 (2005)** 이다 — 이름·저널이 비슷해 보인다는 이유로
  옛 주석을 [9] 나 [30] 으로 **"고치면" 안 된다** (그 논문들이 그 값을 줬는지 모른다).
- ⇒ **처방**: K_IC 두 값은 [23] Sharma 2023 · [30] Stallard 2022 원문을 digest 할 때까지 **"Assumed"**. 이 카드를 K_IC 의 출처로
  인용하지 말 것 (2차 인용 = SELF-51 이 막으려는 바로 그 경로).

### 7.5 ⚠ H_AM — 우리 "NCM811 압입 경도 문헌대 ≈ 3–6 GPa" 와 이 논문이 인용한 경도가 **겹치지 않는다**
- 이 논문이 전하는 NMC 경도: **7.8 · 8.9 · 8.6 GPa** (NMC532 다결정 2차입자, [27]–[29]) · **14.2 GPa** (NMC811 펠릿, [23]). 자체 H 없음.
- 우리: `scripts/am_load_balance_jam.py` `--h-am` 기본 **4.0 GPa** — help 문구 *"AM 압입 경도 (GPa). ★문헌 앵커 … NCM811 계 문헌대 ≈ 3~6"*,
  `docs/am_load_balance_and_se_curve_20260805.md` 의 *"같은 모델 역산 H_AM = 3.85 GPa — 문헌대 3–6 안 ✓"*, 그리고
  `docs/mpm_platen_kinematic_stop_defect.md` 의 *"0.30/0.0747 = 4.0 GPa ≈ NCM 압입 경도"*.
- 비: 인용 최저값 7.8 이 우리 문헌대 **상한 6 의 1.30×**, 기본값 4.0 의 **1.95×**, 역산 3.85 의 **2.03×** (derived). **네 값 중 어느 것도
  3–6 안에 없다.** 문헌대 3–6 의 출처는 SELF-51 계보에서 확인되지 않았다.
- 해석 (우리 판단): 하중분담 모델의 H_AM 은 물리적으로 **"AM 크라운이 버티는 접촉 평균압"** 이다. 다결정 2차입자는 치밀 영역
  압입 경도보다 **낮은 압력에서 입계로 부서질 수** 있다 (이 논문 Fig. 4 가 압축 입계 파괴를 보인다) → 4 GPa 가 **입자 스케일
  유효 지지압**으로 방어될 여지는 있다. 그러나 그러면 그것은 **"문헌 앵커 압입 경도"** 가 아니고, *"H_AM 은 문헌에서 오므로
  비순환"* 이라는 그 모델의 핵심 논거가 약해진다.
- 영향 한정: 그 모델은 이미 *"H_AM 0.5~40 GPa 에서 전부 PASS = VACUOUS"* 로 기록돼 있어 **두께 예측 수치에는 영향이 작다.**
  흔들리는 것은 **"역산값이 문헌대 안" 이라는 교차검증 문장**이다 ⇒ 보류 권고 (§8 ②).
- ⚠⚠ **그 모델 자신의 사전등록 규칙이 걸린다**: `am_load_balance_jam.py` docstring — *"`--invert` … → 문헌값과 비교용 (LPSCl-NCM 계
  NCM811 압입 경도 문헌대 ≈ 3~6 GPa). **역산값이 그 밴드 밖이면 모델이 틀린 것.**"* [27]–[29] 원문이 7.8–8.9 GPa 를 확인하면
  (그리고 NCM811 2차입자도 같은 층이면) 역산 3.83–3.85 는 **그 규칙으로 기각**이다 — 우리 판단이 아니라 **등록된 판정선**이 그렇게 말한다.
  남는 길은 둘: 규칙을 적용하거나, H_AM 이 애초에 "압입 경도" 가 아니었음을 인정하고 (위 해석) **런 전에** 판정선을 다시 등록하는 것.

### 7.6 ★ 입계 강도는 우리 파괴 모델의 앵커가 될 수 있나 — **"그대로는 아니다, 층을 맞추면 된다"**
1. **현재 DEM 파괴 모델 (Auerbach) 에는 직접 안 들어간다.** 그 모델은 `P_c = A·K_IC²·R/E*` (에너지/인성 기준) 이고 강도 σ 를 쓰지 않는다.
   이 논문의 K 관련 수치 (G 0.53) 는 **빌린 K 를 되돌린 것**이라 K_IC 의 독립 앵커가 아니다 (§7.4).
2. **강도 기반 입자 파쇄 기준**을 DEM 에 넣는다면 써야 할 스케일은 **입자 단위 강도** (인용 172.8–210.6 · 207 · 188 MPa) 다.
   745 MPa 는 **결함 없는 ≈1.8 µm³ 체적의 입계 강도**이고, 저자 스스로 입자 통째 시험이 ≈4× 낮은 이유를 응력 삼축성 · 거친 표면 ·
   크기 효과로 설명한다. m = 6.91 로 체적만 스케일하면 10–19 µm 입자에서 **2.3–3.0×** (derived, §13) — 같은 자릿수.
   ⇒ **745 는 입자 파쇄 기준의 상한 (무결함 극한)** 으로만.
3. **입계를 해상하는 모델**이라면 (문헌 Voronoi 다결정 CZM — `kang2025_toughened_bimodal_nca_lzo` 계열 · 우리 A10 poly 내부 void 의
   미래 판) 이 논문은 **바로 쓸 수 있는 견인–분리 세트**를 준다: σ_c = 745 MPa · G_c = 0.53 J m⁻² · 초기 강성 S = 521 GPa µm⁻¹ ·
   파괴 개구 δ_c = 2G/σ ≈ **1.43 nm** (derived). ⚠ G · S 는 빌린 K 에 매여 있고 (S ∝ σ²E/K²), 평면변형률로 두면 G 0.48 · S 581.
4. **A10 사이클 서사와의 정합**: 파괴변형률 ≈0.4 % ≪ 화학변형 (저자 "order of 10 %") → *"한 사이클에 일부 입계가 끊기고 응력이
   풀렸다가 다음 사이클에 다시 쌓여 또 끊긴다"* (p. 5) = 우리 A10 의 poly 입계 내부 void 누적 가정과 **같은 기구**. 개시 기준 후보로
   **0.4 %** 를 등록할 만하다 (값 전이는 액체계·리튬화 상태 한정어와 함께).

### 7.7 원고 SI Table S2 인용 문장 초안
- **행 값 칸**: `140` (model input) — **Ref 칸**: Sedlatschek et al. 2026 (measured 138 ± 24 GPa)
- **각주 / 본문 문장 (영문)**:
  > *"Young's modulus of polycrystalline NCM811 secondary particles measured by nanoindentation: 138 ± 24 GPa (Berkovich tip, continuous
  > stiffness measurement, P_max = 5 mN, h ≈ 150 nm, n = 29, ν = 0.32 assumed); in situ micro-tensile tests on the same material gave
  > 165 ± 7 GPa (n = 3) [Sedlatschek et al., J. Power Sources 681 (2026) 240276]. The DEM uses E = 140 GPa (ν = 0.25), whose contact
  > modulus E/(1−ν²) lies within 3 % of the value implied by the nanoindentation data."*
- ⛔ **쓰지 말 것**: *"140 GPa (Sedlatschek 2026)"* — **140 이라는 숫자는 이 논문에 없다.** 그렇게 적으면 S5 (σ_ion 3.0 을 원문에
  없는 논문에 붙임) 와 **같은 오귀속을 새로 만든다.**
- ⚠ 같은 표의 **ν_AM = 0.25** 행은 이 논문이 근거가 **아니다** (저자는 0.32 를 가정) → "Assumed" 표기. AM_S 가 따로 있다면 §7.3.

### 7.8 다른 정본 카드가 쓰는 CAM 영률 — 이 측정 밴드에 대면 (값은 각 카드의 기록)

| 카드 | CAM · 값 | 이 논문 밴드 [138 (압입), 165 (인장)] 대비 |
|---|---|---|
| 우리 DEM | NCM811 **140** (ν 0.25) | 안 (AM_P) |
| `bazzoun2026_dem_fem_rnm_ionic` | NMC811 **161.5** (ν 0.30) | 안 (두 평균 사이) |
| `bazzoun2025_dem_parameter_sensitivity_assb_cathode` | NMC532 161.5 (스윕 123–200) | 안 — 단 NMC532 |
| `intergranular_cracking_nmc811_jmca2023` | 1차입자 E_p **150** (phase-field FEM, Voronoi 400 grain, ν 0.3) | 집합체 밴드 값이 **grain 에** 쓰였다 — GB 를 별도 순응 요소로 넣지 않는 한 집합체 강성은 맞는 자릿수, GB 스프링을 **함께** 넣으면 이중계상 (§8 ④) |
| `kang2025_toughened_bimodal_nca_lzo` | NCA **175** | 위 (재료 다름) |
| `galvezaranda2024_time_dependent_dl_calendering_microstructure` | AM **200** (ν 0.3) | 위 |
| `asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing` | NCM622 **230** | [23] 펠릿 값과 같은 층 (치밀) |
| `bucci2017_chemomech_failure_assb_cycling_czm` | AM **100** (FEM 입력, Table 2) | 아래 |
| `he2026_dem_calendering_inhomogeneity_areal_density` | NCM **47** (그 카드: 미출처) | 크게 아래 (압입 평균의 0.34×) |

## 8. 적용 인사이트 (우리 연구에 어떻게)

### ① ★★★ SELF-51: E_AM 140 GPa 의 교체 출처 — **AM_P 한정으로 확정 가능**
§7.7 문장으로 Table S2 를 고친다. 값은 그대로 (재계산 0). 원장에는 *"다결정 NCM811 나노압입 138 ± 24 (n = 29) — 140 은 모델 입력"* 으로.
AM_S 행/주석은 따로 한정 (§7.3).

### ② ★★★ H_AM "문헌대 3–6 GPa" 재검토 — 이 논문이 인용한 NMC 경도 4값이 **전부 그 밖**이다
`am_load_balance_jam.py` 의 *"문헌 앵커 · 비순환"* 논거와 *"역산 3.85 = 문헌대 안 ✓"* 판정이 기대는 밴드의 출처가 없다.
두 갈래: (a) [27]–[29] 원문을 확보해 **압입 경도**로 문헌대를 다시 세우거나 (그러면 역산값이 밴드 밖 → 모델 **자신의 등록 규칙**
*"역산값이 그 밴드 밖이면 모델이 틀린 것"* 으로 기각, §7.5),
(b) H_AM 을 **"입자 스케일 유효 지지압 (입계 파쇄 포함)"** 으로 재명명하고 "문헌 앵커" 문구를 뺀다. 어느 쪽이든 **판정 문장 보류**.
(모델의 두께 수치는 VACUOUS 기록대로 H_AM 에 둔감 — 영향은 논거 층.)

### ③ ★★ K_IC — 교체 출처는 [23] · [30] 원문에 있다 (이 카드가 아니다)
digest 요청 대상: **Sharma et al., *Extreme Mech. Lett.* 58 (2023) 101920** (단결정인가 펠릿인가 · 0.271 의 정의) · **Stallard et al., *Joule* 6
(2022) 984** (추정 인성). 그 전까지 `K_IC_AM_S = 1.0` 은 이 논문이 전하는 유일한 인성값과 3.7× 어긋난다는 **경고를 달아** 둔다.

### ④ ★★ 집합체 모듈러스 vs grain 모듈러스 — **층을 섞지 말 것**
138–165 는 **입계를 포함한 집합체** 값이다. 입자를 한 덩어리로 보는 우리 DEM 에는 이게 맞다. 그러나 **grain 을 해상하고 GB 스프링을
따로 넣는** 모델 (A10 poly 의 미래 판 · 문헌 phase-field) 에 이 값을 grain 에 넣으면 GB 순응성을 **두 번** 센다. 우리 산술로
S_gb × d_grain ≈ 312 GPa 를 grain E 168–249 와 직렬로 두면 **≈125–139 GPa** 가 나와 측정 집합체 값과 같은 자릿수다 (§13, 예시용).
⇒ 입계 해상 모델의 grain 에는 **치밀/단결정 값 (인용 168–249)**, 균질화 입자에는 **138–165**.

### ⑤ ★ DEM 입자 파쇄를 강도 기준으로 넣는다면 — 745 가 아니라 **입자 단위 ≈170–210 MPa** (원문 확인 후)
Weibull 체적 스케일링 (m 6.91) 만으로 2.3–3.0× 가 나오므로 745 → 입자 단위의 ≈4× 차이는 크기가 설명의 절반 이상을 차지한다
(§13, 예시용). 우리 Auerbach 임계는 **단일 입자 압축 시험과 대조된 적이 없다** — 그 대조의 앵커가 [32] · [38] · [39] 다.

### ⑥ ★ A10 poly 내부 void 개시 앵커 후보 — 파괴변형률 ≈0.4 % · 입계 지배
압축·인장 모두 입계 파괴 · 파괴변형률 0.4 % · "사이클마다 일부 입계가 끊김" 서사 = `cycle_contact_ledger --poly-mode expand-void` 의
ASSUMED-FORM 에 붙일 수 있는 **첫 정량 한정어**. ⚠ 리튬화 상태 1점 · 액체계 전극 맥락.

## 9. 인용 가능 문장 (deck / paper 용)

- *"Polycrystalline NCM811 secondary particles fail in a brittle, predominantly intergranular manner under both compression and uniaxial
  tension; micro-tensile tests on FIB push-to-pull specimens machined inside the particles give a Weibull characteristic grain-boundary
  strength of 745 MPa (m = 6.91, n = 3) and a fracture strain of ≈0.4 % (Sedlatschek et al., J. Power Sources 681 (2026) 240276)."*
- *"The NCM811 modulus used in our DEM (140 GPa) is within 1.5 % of the nanoindentation modulus of polycrystalline NCM811 secondary
  particles (138 ± 24 GPa, n = 29); because Hertzian contact stiffness depends on E/(1−ν²), our contact modulus differs by 2.9 %
  regardless of the Poisson ratio assumed in the indentation analysis."* (두 번째 절은 **우리 산술** — 논문 주장 아님을 병기)
- *"Grain-boundary strength measured at the micrometre scale (745 MPa) is about four times the whole-particle crushing strength reported
  for NMC secondary particles (≈170–210 MPa), which the authors attribute to stress triaxiality, surface roughness and a size effect."*

## 10. 주의 / 한계 (over-claim 방지) — 비판적으로

1. **n = 3** (4 중 1 제외). Weibull σ_ch · m 이 3 점에서 나왔다 — 저자도 "caution". 제외된 곡선이 **가장 강하고 가장 뻣뻣한** 쪽이라
   (figure-read ≈990 MPa · 할선 ≈213 GPa) 제외는 **E 와 σ_ch 를 모두 낮추는 방향**이다. 넣으면 σ_ch ≈835 MPa · m ≈5.4 · 평균 E ≈177
   (derived from figure-read, TREND 전용). 제외 근거 (이방성 · grain 수 적음) 는 **모든 시편에 똑같이** 해당하는 설명이다.
2. **SD 7 GPa = 모집단 SD** (ddof 0). 표본 SD 는 **8.3 GPa** (§13). 사소하나 n = 3 에서는 구분할 것.
3. **G_crit · S_gb 는 측정값이 아니다.** 빌린 K (0.271, [23]) 에 매여 있고 (S ∝ σ²E/K²), 그 K 는 참고문헌 제목상 **단결정 NMC 의
   압입 인성** (pop-in) — 즉 **입내 벽개 인성**일 가능성이 크다. 그것을 **입계**에 쓰는 것은 "입계가 약한 고리" 라는 논문 자신의 전제와
   어긋난다. 평면응력 선택 (평면변형률이면 G 0.48 · S 581) 도 ±10 %.
4. **[23] 의 기술 불일치**: 본문 "NMC811 pellets" ↔ 제목 "single crystalline NMC". 230 GPa · 14.2 GPa · 0.271 을 인용하려면 [23] 원문 필수.
5. **크기 효과 인용 [47] 은 Li 금속 논문**이다 (NMC·세라믹 아님). 세라믹의 Weibull 체적 논증은 정량으로 제시되지 않았다
   (우리 산술 2.3–3.0×, §13).
6. **파단 위치**: STEM·TKD 한 시편에서 파단이 **게이지 상단 필렛 부근** (figure-read). FE 는 게이지 폭 방향 균일성 (3.7 %) 만 정량했고
   **필렛 응력집중은 보고 안 함** — 색 척도가 1000 MPa 에서 잘려 그림으로도 판별 불가.
7. **선택 편향**: *"large and defect-free"* 입자만, 제작 중 결함이 보이면 폐기 → 강도는 **무결함 입계망** 값이다. Fig. 2a 가 보이듯
   실제 전극 입자 다수는 제조 균열을 이미 갖고 있다.
8. **시료 정보 부족**: 공급사 · 조성 분석 · 사이클 이력 · 전극 배합 **n/a**. 리튬화 상태 한 점. "입계 강도는 리튬화에 거의 무관" 은 **가설**.
9. **1C 변형률속도 논증**은 화학변형 10 % 를 균일 선형변형으로 본 **크기 차수 논증**이다. 입계를 여는 것은 결정 방위 불일치로 생기는
   **이방성 변형 차**이지 전체 부피변화가 아니다 (우리 논평). 게이지 실제 변형률속도는 압입기 명목값 (0.37 nm/s ÷ 2.7 µm) 의
   **14–18 %** 뿐이다 (derived) — 변위 대부분이 팔·힌지·팁 접촉으로 간다 = DIC 가 필수인 이유.
10. **DIC 노이즈 20–25 %** — E 가 거의 선형인 곡선의 필터링에 기댄다 (원자료 SI 5 **미확인**). 횡변형 측정 불가 → ν 는 끝내 가정.
11. **나노압입 보고가 얇다**: 개별 압입값 분포 · 깊이 프로파일 · H · E_r · 팁 상수 없음. SD 24 GPa (17 %) 에는 grain 이방성 · 기공 · 입계가
    섞여 있고, "기판효과" 보정 (E_r 표면 외삽) 의 세부는 [42] 로 미뤘다.
12. **ASSB · LPSCl 아님**: 기계 상수만 넘어온다. 수송 · 압밀 · 적층압 정보 **0**.
13. **frame 정리**: 실험 논문이라 rigid-vs-plastic 모델 artifact 는 없다. 대신 **스케일 artifact** 가 있다 — 이 논문의 모든 수치는
    **입자 내부 (sub-particle)** 층이고, 우리 DEM (내부 없는 구) · MPM (동결 AM) 어느 쪽도 그 층을 해상하지 않는다.

## 11. 논증 흐름 (절별)

1. **도입 (p. 1–2)** — 균열이 NMC811 용량 손실의 주요 경로 (새 표면의 반응층 · 활물질 고립 · 임피던스 증가). 균열은 주로 입계를 따른다
   → 입계 물성이 필요. 미세인장 방법 지도 (Fig. 1) 와 각 기하의 결함. 문헌 E (DFT 168–249 · 펠릿 230 · 2차입자 113–143) · H · K ·
   입자 단위 강도 (Brazilian 유사, 172.8–210.6) 정리 → **"균일 단축 인장 하의 입계 강도는 없다"**.
2. **재료·방법 (p. 2–4)** — 상용 전극 · 압축 정성 시험 · FE 로 굽힘 없는 push-to-pull 기하 설계 (Fig. 3) · DIC 미세인장 · 나노압입 검증.
3. **결과 (p. 4)** — 압축: 입계 파괴 + 바인더 박리 + 취성 (Fig. 4). EBSD: 균열 대부분 입계, 드물게 입내 (Fig. 5). 인장: 선형 → 취성 파단,
   840/685/562 MPa · 172/168/156 GPa (Fig. 6). STEM: 전위밀도 약간 증가 (Fig. 7). TKD: 입계 파괴 · 격자 왜곡 없음 (Fig. 8).
   나노압입 138 ± 24 GPa (n = 29).
4. **논의 (p. 4–7)** — 변형률속도 = 1C 약간 미만 · 인장 E ≈ 압입 E ≈ 문헌 2차입자, 펠릿보다 낮음 → 방법 신뢰 · 파괴변형률 0.4 % ≪
   화학변형 → 사이클마다 입계가 조금씩 끊김 · Weibull 745 / 6.91 · 입자 강도의 ≈4× (삼축성 · 표면 · 크기) · G 0.53 · S_gb 521 ·
   리튬화 가설 · 단결정 NMC 는 더 작은 시편 필요 · FIB 비정질화 없음 · 힌지 < 5 % · DIC 노이즈 · 한계 (선형탄성 설계 · 최소 두께 ·
   국소성 · 통계 부족).
5. **결론 (p. 7)** — 입계 강도·강성이 NMC 품종의 기계 강건성 척도, 입계 강도를 높이면 입계 균열 열화가 준다. 방법은 다른 재료
   계면에도 적용 가능.

## 12. 용어 미니 사전

- **push-to-pull**: 압입기가 **누르는** 운동을 시편 기하가 게이지의 **인장**으로 바꾸는 방식. 전용 장치형 · 일체형 (시편 자체를 깎음).
- **theta 시편**: θ 모양의 닫힌 틀 가운데 가로막대가 게이지인 일체형 push-to-pull 기하 (Durelli 1962, Quinn 소형화).
- **힌지 (hinge)**: 이 기하에서 한쪽 블록이 회전하는 얇은 연결부. 하중 일부를 나눠 지므로 몫을 재야 한다 (< 5 %).
- **DIC (digital image correlation)**: 영상의 표지점/무늬 이동을 추적해 변위·변형률을 재는 법. 여기서는 Pt 점 2개 = **가상 신율계**.
- **Savitzky–Golay 필터**: 국소 다항식 적합으로 노이즈를 줄이는 평활 필터 (모양 보존).
- **CSM (continuous stiffness measurement)**: 압입 중 작은 진동을 얹어 깊이에 따라 접촉 강성을 연속 측정 → E(h), H(h).
- **Oliver–Pharr**: 제하 강성과 접촉 면적 함수로 **reduced modulus E_r** · 경도 H 를 얻는 표준법.
- **reduced modulus E_r**: 1/E_r = (1−ν²)/E + (1−ν_i²)/E_i (i = 압입자). 시료의 **E/(1−ν²)** 만 제약한다 — ν 를 가정해야 E 가 나온다.
- **기판효과 (substrate effect)**: 얇은/둘러싸인 대상 아래·주변의 다른 재료가 측정 강성을 오염시키는 것. 여기선 E_r 을 표면으로 외삽해 보정.
- **Weibull 분포**: P(σ) = 1 − exp[−(σ/σ_ch)^m]. σ_ch = 63.2 % 파괴 확률 강도 (특성강도), m = Weibull 계수 (클수록 산포 작음).
- **MLE**: 최대우도 추정.
- **intercrystalline (입계) / transcrystalline (입내) 파괴**: 균열이 grain 사이 경계를 따라가는가 / grain 을 가로지르는가.
- **EBSD / TKD / STEM**: 후방산란 전자회절 (표면 방위 지도) · 투과 Kikuchi 회절 (얇은 시편 고분해능 방위 지도) · 주사투과전자현미경.
- **pseudosymmetry 보정**: 층상 결정에서 거의 같은 회절 패턴을 주는 방위들 사이의 오지수를 특정 회전 관계로 바로잡는 것.
- **G_crit (임계 에너지해방률)**: 균열이 자라는 데 드는 단위 면적당 에너지. 평면응력 G = K²/E, 평면변형률 G = K²(1−ν²)/E.
- **입계 강성 S_gb (interface stiffness)**: 입계를 견인–분리 스프링으로 볼 때의 초기 기울기 (응력 / 개구, Pa m⁻¹). cohesive 요소의 입력.
- **cohesive (zone) 요소**: 계면을 견인–분리 법칙으로 표현하는 FE 요소 — 강도 (σ_c) · 파괴에너지 (G_c) · 초기 강성을 받는다.
- **Brazilian 시험 (유사)**: 구/원판을 두 판으로 눌러 내부에 인장을 만들어 강도를 재는 간접 인장 시험. 응력이 다축·비균일.
- **삼축성 (triaxiality)**: 정수압 성분 / 편차 성분 비. 다축 인장일수록 취성 파괴가 이르다.
- **FIB 비정질화**: 이온빔 가공이 시편 표면을 비정질로 망가뜨려 기계 측정을 오염시키는 현상.

## 13. 🧮 파생 계산 원장 (`derived(ours)` — 논문 숫자만으로 한 우리 산술, 스크립트 재실행 가능)

| # | 계산 | 결과 | 비고 |
|---|---|---|---|
| D1 | Weibull 2-모수 MLE 재계산 (840, 685, 562 MPa) | **m = 6.911 · σ_ch = 744.8 MPa** | 논문 6.91 · 745 **재현** |
| D2 | Weibull 평균 σ_ch·Γ(1+1/m) vs 산술평균 | 696.4 vs 695.7 MPa | 정합 |
| D3 | 인장 E 통계 (172, 168, 156) | 평균 **165.33** · SD(ddof 0) **6.80** · SD(ddof 1) **8.33** GPa | 논문 "SD 7" = 모집단 SD |
| D4 | 파괴변형률 σ/E | 0.488 · 0.408 · 0.360 % (평균 0.419) | "≈0.4 %" 정합 · Fig. 6a 판독과 일치 |
| D5 | 게이지 신장 = 2.7 µm × σ/E | 13.2 · 11.0 · 9.7 nm | "최대변위 ≈12–15 nm" 와 대체로 정합 (가장 약한 시편은 그 아래) |
| D6 | G = K²/E (0.271, 138) · 평면변형률 판 | **0.5322** J m⁻² (논문 0.53) · 0.4777 (ν 0.32) | |
| D7 | S_gb = σ²/(2G) | **521.5 GPa µm⁻¹** (반올림 G 0.53 을 쓰면 523.6) · 평면변형률 G 면 581 | 논문 521 = 반올림 전 G 사용 |
| D8 | 파괴 개구 δ_c = 2G/σ = σ/S | **1.43 nm** | cohesive 입력 예시 |
| D9 | 나노압입 평균의 표준오차 · 95 % CI (t 2.048, n 29) | SE 4.46 · **[128.9, 147.1] GPa** · z(140) = 0.083 | 140 은 CI 안 |
| D10 | 140 vs 138 / 165 · 165 vs 138 | +1.45 % / −15.2 % · +19.6 % | |
| D11 | E/(1−ν²): 논문 (138, 0.32) vs 우리 (140, 0.25) | **153.74 vs 149.33 GPa → −2.87 %** · 같은 측정을 ν 0.25 로 → E 144.1 | 압입이 제약하는 양 = Hertz 가 쓰는 양 |
| D12 | E* AM–AM · AM–SE (E_SE,eff 1.35, ν 0.30) | AM–AM 76.87 vs 74.67 · AM–SE 1.46934 vs 1.46892 GPa | AM–SE 차 0.03 % |
| D13 | Auerbach 감도 (P_c ∝ K²/E*, δ_c ∝ K^(4/3) E*^(−4/3)): poly K 0.3→0.271 | P_c ×0.816 (K) · ×0.971 (E*) · **×0.793 (둘 다)**; δ_c ×0.873 · ×0.962 · **×0.840** | `scripts/fracture_model.py` 식 그대로 |
| D14 | AM_S 를 치밀/단결정 값으로 (ν 0.25 고정): E 168 / 200 / 230 / 249 | P_c ×0.833 / 0.700 / 0.609 / 0.562 · δ_c ×0.784 / 0.622 / 0.516 / 0.464 | 인용값 기준 가상 |
| D15 | AM_S K 1.0 → 0.271 (+ E 230) | P_c **×0.073** (×0.045) · δ_c ×0.175 (×0.090) | [23] 이 단결정이라는 전제 하의 가상 |
| D16 | 절대 P_c 예시 (A 200, R_min 2.5 µm, E* 74.67) | K 0.3 → 0.603 mN · 0.271 → 0.492 mN · 1.0 → 6.70 mN (R_min 5 µm 면 ×2) | 단일 입자 압축 시험과 대조된 적 없음 |
| D17 | 직렬 grain + GB 순응성 (예시): 1/E_agg = 1/E_grain + 1/(S_gb·d), S_gb·d = 521.5 × 0.598 = 312 GPa | E_grain 210 / 230 / 249 → **125.5 / 132.4 / 138.5 GPa**; d ± 1σ (0.293–0.903 µm) 에서 E_grain 230 → 91.8–154.5 | 1D 직렬 · 이방성·기공 무시 · S_gb 자체가 빌린 K 에 매임 — **자릿수 점검용** |
| D18 | Weibull 체적 스케일링 (m 6.91): V_gauge = 2.7 × 0.5 × 1.3 = 1.755 µm³ vs 구 d 10 / 19 µm | 체적비 298 / 2046 → 강도비 **2.28 / 3.01** · 4× 에 필요한 체적비 ≈14,500 | 균일 응력 체적 가정 — Brazilian 유효 체적은 더 작다 (과대 추정 쪽) |
| D19 | 인용 경도 ÷ 우리 H_AM | 7.8 → 1.95× (÷4.0) · 1.30× (÷6.0) · 2.03× (÷3.85); 14.2 → 3.55× · 2.37× · 3.69× | 4값 모두 3–6 밖 |
| D20 | 게이지 변형률속도: 실측 ÷ 명목 (0.37 nm s⁻¹ ÷ 2.7 µm = 1.37 × 10⁻⁴ s⁻¹) | **0.142 · 0.178 · 0.183** | 압입기 변위의 ≈82–86 % 가 게이지 밖으로 |
| D21 | 제외 곡선 포함 (figure-read 990 MPa) Weibull MLE | m ≈ **5.4** · σ_ch ≈ **835 MPa** · 평균 E ≈177 (할선 ≈213 포함) | figure-read 입력 — TREND 전용 |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
