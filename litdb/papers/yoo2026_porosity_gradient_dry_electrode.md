# Yoo 2026 (Energy Storage Materials, ENSM 105331) — Porosity-구배 건식 흑연 전극 + 변형성 Primer Layer

> slug `yoo2026_porosity_gradient_dry_electrode` · DOI `10.1016/j.ensm.2026.105331` · type `MPM` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_yoo2026_porosity_gradient_dry_electrode.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Hyundong Yoo†, Jaejin Lim†, Jun Ho Hwang, Seungeun Oh, Yong Min Lee\*, Hansu Kim\*,
"Porosity-Gradient Dry-Processed Graphite Electrode with Deformable Primer Layer for Boosting
Fast-Charging Capability of Lithium-ion Batteries", *Energy Storage Materials* (2026),
DOI 10.1016/j.ensm.2026.105331 (PII S2405-8297(26)00463-0, ENSM 105331).
Journal Pre-proof. 접수 2026-05-04, 수정 2026-06-17, 게재확정 2026-06-23. Published by Elsevier B.V.

**소속:** Hanyang University (Dept. of Energy Engineering + Dept. of Battery Engineering, 김한수)
+ Yonsei University (Dept. of Chemical & Biomolecular Engineering, 이용민 = **Digital Twin Battery
Lab**). †H. Yoo와 J. Lim 동등기여. 교신 yongmin@yonsei.ac.kr / khansu@hanyang.ac.kr.
지원: NRF (MSIT, RS-2024-00349600) + 일부 삼성전자. **이해상충: Yoo/Hwang/Kim 특허출원 중(licensing 예정).**

**소재계:** **천연흑연(natural graphite) 음극** + **PTFE 바인더**(건식) / SBR+CMC(습식) +
**PVDF/PAA/CMC primer layer**; 전해질 1M LiPF₆ EC/EMC 3:7 + 10 wt% FEC; full-cell은 **NCM523**(=
LiNi₀.₅Co₀.₂Mn₀.₃O₂) 양극. ★ **우리 LPSCl sulfide ASSB가 아니다** — 일반 LIB 흑연/액체전해질 건식전극.
이 그룹(이용민 연세대 DTBL)의 **#286** 논문 — `docs/literature_yonsei_dtbl_2026.md` 항목 갱신본.

DB 동반 파일: 없음(생성 안 함). 주요 수치는 본 MD 본문 표에 모두 정리.
SI 동영상 2개 존재(`01._video1teries.mp4`, `01._video2teries.mp4` = 전극 변형/primer movie,
**기계 판독 불가** → 이름만 기록). SI 텍스트(Fig S1–S26 캡션 + Note S1/S2 + Table S1–S4)는 디제스트 반영.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**Primer layer(PL)의 기계 변형성**(PVDF가 가장 무름, E≈6.3/16 MPa)을 binder 선택만으로 조절하면,
**라미네이션/캘린더링 중 비대칭 응력**이 발생해 **추가 공정 없이 자발적으로 z-방향 porosity 구배**
(위쪽 다공·아래쪽 치밀)가 생긴다. 가장 무른 **PVDF-PL이 가장 가파른 구배**(top↔bottom 평균
**24.5%p** vs WPE 5.6%p)를 만들고, 이 구배가 **장거리 pore 연결성↑ + tortuosity↓**(1.86 vs WPE 3.09)
→ **농도분극↓ + 3C 급속충전 용량↑(305 vs 258 mAh/g) + Li plating 억제**로 이어진다.
검증은 **3D XCT + FIB-SEM 토모그래피 + pore network model(PNM) + 재구성 3D 기반 전기화학 시뮬**.

**우리 hook(가장 중요):** 이 논문은 우리가 **아직 안 한 Phase 5(z-방향 layered/porosity-gradient
합성)의 실험·토모그래피 청사진**이다. 그리고 그들이 토모그래피로 **tortuosity·coordination·pore
연결성을 정량화하는 방법**은 우리 `voxel_conductivity` / `extract_2d_microstructure`(z-band) /
`mpm3d` 미세구조에 **직접 이식 가능**하다. 단 소재가 **흑연/액체전해질**이라 **절대 transport 값은
우리 LPSCl로 전이되지 않는다** — 가져올 것은 **설계 개념·측정 방법·정성 추세**다.

---

## 1. 배경 / 동기 (Introduction, p.4–5)

- EV 보급 → **충전시간 단축**이 병목. 흑연 음극은 cyclability·안정성은 좋으나 **고전류·후막(thick)
  전극에서 Li plating + 용량열화**가 급속충전을 막음.
- 기존 해법: 표면공학(Al₂O₃/TiO₂₋ₓ/그래핀 코팅, 산·염기 표면처리) → Li⁺ 동역학 개선·plating 억제하나
  **벌크 이온수송 제약은 못 풂**. 미세구조 엔지니어링(laser patterning, magnetic alignment,
  freeze casting) → pore 구조로 수송·분극 개선하나 **공정 복잡·고비용·확장성 한계**.
- ★ **수직 porosity 구배**(위>아래) 개념이 주목받음: 전해질 침투↑ + through-plane Li⁺ percolation↑ →
  rate↑ + Li plating 완화(참고문헌 14–19, 21). 그러나 기존 구배 전극은 **다층 슬러리 코팅 / 3D
  templating** 의존 → 산업라인 적용 어려움.
- **건식공정(dry-processed, PTFE 피브릴화)**이 친환경·확장성 대안: **NMP(독성 용매) 제거 + 건조시간·
  에너지↓ + 낮은 바인더 함량 + PTFE 나노피브릴 형태 덕에 유리한 pore 구조**. 실용에선 건식 전극 필름과
  금속 집전체 사이에 **conductive carbon + binder PL**을 끼워 접착·전기접촉 확보. ★ **이 PL의 기계
  물성이 라미네이션 중 응력 분포를 바꿔 전극 내부 미세구조를 바꿀 수 있다** — 이게 이 논문의 가설.
- **가설(명시):** PL의 기계 변형성을 binder 화학(서로 다른 탄성계수 — **PAA / CMC / PVDF**) 선택으로
  조절하면, **건식전극 라미네이션 중 수직 graded porosity가 자발적으로 형성**된다. → 추가 공정 없는
  단일단계·확장 가능 경로.

**약어 정리:** WPE = wet-processed electrode(습식, 비교군). DPE = dry-processed electrode(건식).
PL = primer layer(집전체↔전극 접착·도전 중간층). DPE@PAA-PL / @CMC-PL / @PVDF-PL = 각 PL binder.

---

## 2. 소재 & 제작 (Experimental Section, p.22–25)

### 2.1 전극 설계 (공통)
- **흑연:** 천연흑연, 평균입경 **15.5 µm**(습/건식 동일).
- **DPE:** 흑연 : PTFE = **98 : 2 wt%**. mass loading **~10.2 mg/cm²** (≈ areal capacity **3.5 mAh/cm²**),
  밀도 **1.5 g/cm³**, 라미네이션 후 두께 **~68–70 µm**.
- **WPE:** 흑연 : SBR : CMC = **96 : 2 : 2 wt%**, DI water, doctor blade, Cu 집전체(20 µm), 80 °C 30 min
  건조 → roll press 두께 70 µm(밀도 ~1.5 g/cm³) → 120 °C 2 h 진공건조. (mass loading·areal capacity·
  밀도를 DPE와 동일하게 맞춤.)
- **PL:** conductive carbon(Super P Li, Imerys) : binder = **90 : 10 wt%**. mass loading **0.4 mg/cm²**,
  코팅직후 두께 **20 µm** → **DPE 라미네이션 후 8–9 µm로 압축**. binder: **PAA**(Mw 100,000, Sigma) /
  **CMC**(Daiichi Kogyo) → DI water; **PVDF**(Mw ≥ 1,000,000, KF9300 KUREHA) → **NMP**.
  건조 80 °C 30 min + 진공(PAA·CMC 120 °C, PVDF 200 °C) 2 h.

### 2.2 건식 전극 제작 공정 (Fig 1a)
1) **Powder mixing & kneading** — 흑연+PTFE 분말을 planetary mixer(20 min, 2000 rpm) → **기계전단으로
   PTFE 피브릴화**. 2) **Laminating** — homemade roll-to-roll 전단기로 30 min 전단 → **self-standing
   건식 필름**(목표 loading ~10.2 mg/cm²), 이를 PL 코팅된 Cu에 **실온 롤프레스 라미네이션**. 3)
   **Calendering** — 목표 두께 ~70 µm(밀도 1.5 g/cm³)로 캘린더링.
   ★ PL이 없으면 건식 필름↔집전체 접착이 약해 **박리(delamination) → 접촉저항↑ + 전자공급 저해**(Fig 1a
   "Delaminated, weak adhesion"); 잘 설계된 PL은 견고한 계면 형성(Fig 1a "Well-adhered").

### 2.3 셀
- **Half-cell:** 2032 coin, Li foil 상대전극, PE separator, 전해질 1M LiPF₆ EC/EMC 3:7(v/v) + 10 wt% FEC,
  36 h aging. TOSCAT-3000, CC-CV, 0.005–1.5 V vs Li/Li⁺. formation 0.1C. cycle: charge 0.5C / discharge 1C.
  rate: charge 0.5/1/2/3/5C, discharge 1C.
- **Full-cell:** **NCM523**(LiNi₀.₅Co₀.₂Mn₀.₃O₂) : Super P : PVDF = **80 : 10 : 10 wt%**, Al(15 µm),
  N/P ratio ~1.1 (loading ~20 mg/cm², areal capacity ~3.15 mAh/cm²), 4.2–2.8 V. (SI Note S1은 NCM**622**
  full-cell ICE 평가도 별도 수행 — 아래 §SI.)
- **SC-EIS:** symmetric cell(blocking), VMP-300, 진폭 10 mV, 10 mHz–600 kHz, 전압섭동 10 mV.

---

## 3. 핵심 메커니즘 — 왜 변형성 PVDF-PL이 porosity 구배를 만드는가

**(1)** PL은 라미네이션 중 **기계적 지지층(mechanical support layer)** 역할. **(2)** binder 화학마다
PL의 탄성계수가 다름(PAA > CMC > PVDF, **PVDF가 가장 무름**). **(3)** 기계적으로 더 무른 PL은
라미네이션 시 **집전체 근처(아래) 영역에서 PL의 소성변형**으로 **비대칭 압축** → **아래쪽이 더 조밀하게
패킹**되고 **위쪽은 상대적으로 덜 압축**됨 → **자발적 수직 porosity 구배**(top porous, bottom dense).
**(4)** 더 무른 PVDF-PL일수록 변형이 커 **가장 가파른 구배** + AM↔PL **접촉면적 확대**(아래 Fig 5d).
→ 이것이 DPE@PVDF-PL의 더 뚜렷한 porosity 구배의 직접 원인(p.9 본문 해석).

⇒ 우리 식으로: **"무른 중간층의 소성변형이 위↔아래 압축 비대칭을 만들어 z-방향 밀도구배를 self-
organize한다."** 이건 압축역학(우리 MPM 영역)과 z-layered 미세구조(우리 Phase 5)의 **실험 실증**.

---

## 4. 섹션별 결과 — 모든 수치

### 4.1 Porosity-구배 구조 (§2.2, Fig 2, p.7–10)

**전체 porosity (Mercury Intrusion Porosimetry, MIP — Fig S2):**
- WPE·DPE 모두 **32.2 – 33.3%**로 유사. WPE가 약간 높지만 유의하지 않음.
- ★ **핵심:** 전체 porosity는 같아도 **내부 분포(z-구배)는 라미네이션 비대칭응력으로 다르다** → 이걸
  XCT로 봄.

**3D XCT (Xradia 620 versa, 80 kV, 40×, pixel 250 nm, domain 300×300 µm²; DragonFly 재구성, Fig 2a,b):**
- pore 도메인을 **top / middle / bottom** 3층으로 분할.
- **WPE:** top·middle·bottom porosity가 **거의 균일**.
- **모든 DPE:** top → bottom으로 porosity **감소**(구배). local porosity는 **1.25 µm 간격**으로 두께방향
  추정(Fig 2b).
- ★ **DPE@PVDF-PL = 가장 가파른 구배**: **top↔bottom 평균 porosity 차이 = 24.5%p** (WPE는 **5.6%p**).
  → PVDF-PL이 4배 이상 가파른 구배.

**Micro-indentation (SAICAS-DN, 원통팁 Ø600 µm, rate 0.1 µm/s, stop 0.45 N=1.6 MPa, 비압연 PL, Fig 2c–e, S4):**
- 압축계수(compression modulus)·탄성계수(elastic modulus) 모두 **PAA > CMC > PVDF** 순으로 감소.
- ★ **PVDF-PL이 가장 무름: 압축계수 6.31 MPa, 탄성계수 15.99 MPa.** PAA-PL·CMC-PL은 **약 2배 더 높음**.
  → PVDF-PL이 압축응력 하에서 **가장 쉽게 변형** → 구배형성에 유리(앞 §3).

**SC-EIS 이온저항·tortuosity (Fig 2f–i):** 대칭셀 EIS에서 **식 (1)**로 추정:
```
τ² = R_ion · A · ε · κ / (2d)        (식 1)
```
(τ=이온 tortuosity, R_ion=다공전극 이온저항, A=전극면적, ε=porosity, κ=전해질 bulk 이온전도도, d=두께.)
- ★ **DPE들이 WPE보다 R_ion·tortuosity 둘 다 낮음** → DPE의 Li⁺ 수송이 더 효율적.
- DPE 사이에서도 tortuosity가 **DPE@PAA-PL > DPE@CMC-PL > DPE@PVDF-PL** 순 감소 → **porosity 구배가
  가파를수록 tortuosity↓** → Li⁺ 수송 촉진. (정량 절대값은 본문 미기재; 후속 FIB-SEM 확산시뮬에서
  WPE 3.09 / PAA 1.98 / PVDF 1.86으로 확정 — §4.3.)

### 4.2 전기화학 & 급속충전 (§2.3, Fig 3·4, p.10–14)

**Formation-cycle 초기 충전용량 (half-cell, Fig 3a):**
| 전극 | 초기 충전용량 (mAh/g) | ICE |
|---|---|---|
| WPE | **311** | **92.7%** |
| DPE@PAA-PL | **313** | **86.7%** |
| DPE@CMC-PL | **343** | **86.9%** |
| DPE@PVDF-PL | **355** | **85.0%** |
- WPE 311은 일반 흑연(340–360)보다 낮음 → **불리한 pore 구조로 느린 Li⁺ 수송 → 첫 사이클 흑연 불완전
  리튬화**. DPE는 구배가 가팔라질수록 초기 충전용량↑(**porosity 구배 ⇒ 더 완전한 리튬화**).
- ★ **DPE의 ICE는 더 낮음**(85–87% vs WPE 92.7%) → 원인은 **PTFE 탈불소화(defluorination)**(아래 dQ/dV·
  SI Note S1).

**dQ/dV (Fig S5):** WPE는 **0.8–1.0 V SEI 형성 반응만**. DPE는 SEI(0.8–1.0 V) + **추가 반응 0.2–0.8 V** =
**Li⁺에 의한 PTFE 탈불소화 → LiF + 비정질탄소** 생성(참고문헌 31,33,34,44–46). → DPE의 낮은 ICE 원인.

**Cycle 안정성 (Fig 3b):** WPE·DPE 모두 **100 사이클 안정**(급격 열화 없음, 0.5C charge/1C discharge,
0.005–1.5 V, mass loading 10.2 mg/cm²). → 낮은 ICE·PTFE 분해가 장기 cyclability를 망치지 않음.

**급속충전 rate capability (half-cell, Fig 3c,d):**
- ★ **DPE@PVDF-PL 3C 방전용량 = 305 mAh/g @ 3C (10.5 mA/cm²)** vs **WPE 258 mAh/g**. (모든 DPE가 WPE 능가.)
- **CC vs CV 분해(Fig 3d):** 총용량(CC+CV)은 0.5/1/2/3C 전 범위에서 PL 종류 무관하게 비슷. 하지만 **CC
  단독용량**은 차이 큼 — **3C에서 CC 용량: DPE@PVDF-PL 80.2 / DPE@PAA-PL 66.2 / DPE@CMC-PL 66.6 / WPE
  23.3 mAh/g**. → **PVDF-PL의 porosity 구배가 3C 초과 급속충전(=CC구간 더 많이 채움)에 유리**.

**Full-cell (NCM523, Fig 4):**
- 초기 방전용량 / ICE: DPE@PAA-PL **151.1 / 84.5%**, DPE@CMC-PL **146.1 / 81.1%**, DPE@PVDF-PL
  **149.5 / 83.6%**, WPE **159.7 / 89.1%**. → DPE ICE가 낮음(PTFE 탈불소화) → **0.1C 저율에선 DPE 용량 <
  WPE**. 그러나 **전류↑ → DPE 충전용량이 WPE 초과**, **PVDF-PL(가장 뚜렷한 구배)에서 차이 가장 큼**(Fig 4b).
- **SOC(=CC구간으로 도달한 충전상태), 3C (Fig 4c):** ★ **DPE@PVDF-PL = 27.89%** vs WPE 14.31%,
  DPE@PAA-PL 15.89%, DPE@CMC-PL 20.33%. (3C에서 CC SOC: PVDF 29% / CMC 20% / PAA ~16% / WPE 14%; CV가
  나머지 72/80/84/86% — Fig 4c 막대 라벨.) → **가파른 구배일수록 CC로 더 많이 충전 = 급속충전 우수**.

**Li plating 억제 (3C 충전 후 전극표면 SEM, Fig 4d–g):** WPE 대비 **모든 DPE에서 Li plating 완화**,
**DPE@PVDF-PL에서 가장 효과적으로 억제**. SC-EIS의 **최저 이온저항(PVDF-PL)** → 급속충전 하 더 효율적
Li⁺ 수송 + **셀 분극↓ → plating 억제**(참고문헌 14–19, 15). (insets = 충전후 코인셀 광학사진.)

### 4.3 재구성 3D 미세구조 분석 (§2.4, Fig 5, p.15–17) — ★ 우리가 이식할 핵심 방법

**FIB-SEM 토모그래피 (Crossbeam 350, ZEISS; **800장**, ion milling **75 nm 간격**, **pixel 46.52 nm**,
domain **60×60 µm²**; FFT+non-local means 필터, trilinear 스케일, greyvalue threshold + watershed +
**CNN 분할** → 3D 재구성):**
- XCT(pixel 250 nm)보다 **고해상(46.52 nm)** → pore 망 더 정밀 분석. WPE·DPE@PAA·@PVDF 재구성.
- **PL 변형 직접 관찰(Fig 5a–c):** bare Cu 표면은 평탄(변형 없음); **PAA-PL·PVDF-PL은 뚜렷하게 변형된
  표면형태**. 2D topological map(Fig 5c)에서 표면 최대↔최소 높이차: ★ **PVDF-PL = 12.1 µm (PAA-PL 7.8 µm
  보다 55% 큼)**, bare Cu는 유의미한 변형 없음.
- **AM↔PL 접촉면적(Fig 5d, normalized contact area):** PL 기계변형 덕분 **PVDF-PL은 bare Cu 대비 +45%**,
  **PAA-PL은 +27%**. → 확대된 계면 접촉면적이 **DPE/PL 기계접착강도↑**에도 기여(SI Note S2, SAICAS).
- **Porosity 분포(Fig 5e):** FIB-SEM 기반도 XCT와 **유사한 z-구배** 재확인(고해상에서도 구배 존재; FIB-SEM
  46.52 nm vs XCT 250 nm). → 구배가 측정해상도 artifact 아님을 교차확인.

**Li⁺ 확산 시뮬 → tortuosity (GeoDict 2023, Fig S15·S16, 식 2):**
```
D_e,eff = (ε_e / τ_e²) · D_e          (식 2)
```
(D_e,eff=유효확산계수, ε_e=전해질 부피분율, τ_e=pore 도메인 tortuosity, D_e=전해질 고유확산계수.)
경계조건 Δc=1 mol/m³, Dirichlet(두께방향 y, xz 평면 일정농도), Fick's law, FVM solver, 전해질
EC/EMC(3:7) + 1M LiPF₆ 고유확산계수 입력.
- ★ **tortuosity: DPE@PVDF-PL = 1.86 (최저) < DPE@PAA-PL 1.98 < WPE 3.09 (최고).** → PVDF-PL의 Li⁺
  percolation 경로가 가장 덜 우회 → SC-EIS(Fig 2i) 추세와 일치.

**Pore Network Model(PNM) — pore 연결성 (MATLAB, watershed 2σ Gaussian, Fig 5f–h, S17–S19):**
- **Coordination number(이웃 연결 pore 수, Fig S17):** ★ **DPE@PVDF-PL 4.20, DPE@PAA-PL 4.44** ≫ **WPE
  2.94**. → DPE의 더 발달한 **국소 pore 연결성**; 원인 = **낮은 바인더 함량(2 wt%) + PTFE 1D 나노피브릴
  형태**(WPE는 4 wt% + 부피큰 SBR/CMC binder 도메인). (Fig S17은 equivalent pore radius도 제시.)
- **Connectivity matrix(장거리 연결성, Fig 5f–h, S18·S19):** 각 pore를 Cartesian 좌표로 인덱싱, 연결된
  pore 쌍을 점으로 표시. 대각 밴드폭↑ = 물리적으로 먼 pore 연결확률↑ = **장거리 연결성↑**.
  밴드폭 순서 **DPE@PVDF-PL > DPE@PAA-PL > WPE**. 정규화 밴드폭 표준편차: ★ **PVDF-PL 0.1581 >
  PAA-PL 0.1309 > WPE 0.0976**(큰 표준편차 = pore 연결이 더 넓은 거리분포 = 더 강한 장거리 연결성).
  → **DPE@PVDF-PL이 가장 긴 interpore 연결** → 급속충전 하 Li⁺ 수송 유리.
- ⚠ 저자 caveat: 본 전극은 **중간 areal capacity ~3.5 mAh/cm²**에서 평가; **더 높은 loading/두께에서
  이 좋은 장거리 연결성이 유지되는지는 향후 과제**(두께↑ → Li⁺ 수송 제약 심화 가능).

### 4.4 재구성 3D 기반 전기화학 시뮬 (§2.5, Fig 6, p.18–20) — half-cell 모델

**모델 (Fig S12, Table S1–S3; BESTmicro solver, Fraunhofer ITWM; GeoDict 2023로 half-cell 가상구성):**
Cu 집전체 + Li metal + separator + **재구성 3D 흑연 복합전극** + Cu 집전체. **3C rate, 0.005 V cutoff,
CC → CV(0.3C cutoff current 종료)**. 지배방정식: charge conservation + electroneutrality + mass
conservation + **Fick's law + Ohm's law + Butler-Volmer**(Table S1). c_max는 흑연 0.1C(0.35 mA/cm²)
실측용량으로 이론계산; E_eq·σ_s·D_s·BV rate constant k는 문헌; 전해질 파라미터 EC/EMC(3:7) + 1.15 M
LiPF₆ @298.15 K 문헌/보간.

**주요 시뮬 결과:**
- **3C CC 용량(Fig S20):** DPE@PVDF-PL 최고 > DPE@PAA-PL > WPE → **실험 half-cell(Fig 3d)과 잘 일치**.
- **Li⁺ 농도분포(활물질 내, Fig 6a–c, S21):** WPE는 흑연 내 전반적으로 낮은 Li⁺(수송·계면반응 불충분 →
  급속충전 시 흑연 완전 리튬화 안 됨). DPE@PAA·PVDF는 훨씬 높은 Li⁺; ★ **DPE@PVDF-PL은 전극 바닥영역까지
  높은 Li⁺ → 두께방향 Li⁺ 농도구배가 가장 작음** → **공간적으로 더 균일한 전기화학 반응**.
- **Overpotential 분해(Fig 6d–f, S22):** CC-CV 종료 시 활성화 과전압 분포 — DPE@PVDF-PL이 **top 영역
  과전압 최저**. deconvolution: **Li⁺ 확산(전해질·활물질) 과전압이 DPE↔WPE를 가르는 핵심**. ★
  **DPE@PVDF-PL이 전해질·활물질 양쪽에서 과전압 최저 → 전체 과전압 최소** → 분극↓ → 3C 용량 우수 +
  Li plating 완화. + **변형 PL로 넓어진 AM↔PL 계면**이 **PL→흑연 전자공급도 더 균일**(Fig S23 전류밀도분포).
- **전해질 Li⁺ 농도 시공간분포(Fig 6g–i, S24):** ★ **DPE@PVDF-PL이 충전 내내 가장 균일한 전해질 Li⁺**.
  Li⁺ depletion region(LDR)·excess region(LER)이 모든 전극에 생기나 **LDR↔LER 농도차는 WPE에서 최대**.
  **LDR/LER 형성 onset 시각: WPE 70 s / DPE@PAA-PL 150 s / DPE@PVDF-PL 160 s** (DPE가 늦게 = 더 오래
  분극 없이 버팀). **CV 시작 후 농도분극 지속시간: DPE@PAA-PL 180 s, DPE@PVDF-PL 80 s, WPE 434 s** →
  PVDF-PL이 농도분극을 가장 빨리 해소. ⇒ **변형 PVDF-PL의 우수한 pore 구조가 Li⁺ 농도분극을 가장 효과적
  완화**(Fig 7 개념도).

### 4.5 실용 trade-off & 에너지밀도 (p.20–21, Fig S26·Table S4)

- ★ **빠른 이온수송 ↔ 셀 에너지밀도 trade-off**: porosity↑ → 전해질 침투·Li⁺ 수송↑(분극↓)이지만 **과도한
  porosity / 불충분한 치밀화는 부피에너지밀도(VED) 제약**. 10-stack 3.3 Ah 파우치(graphite‖NCM) 가정,
  흑연 밀도 **1.5 → 1.7 g/cm³** 증가 시 **VED 612 → 642 Wh/L(+5%)**, porosity는 **28.6 → 19.1%** 감소
  (Fig S26). PL이 유한두께로 셀부피에 기여 → **전극 치밀화 + PL 두께 최적화가 실용 에너지밀도 유지에 중요**.
- ★ **공정 지속가능성 caveat:** 본 PVDF-PL은 **NMP 슬러리 캐스팅**으로 제작(dry mass loading 0.4 mg/cm²로
  낮고 3 min에 빠르게 건조 — Fig S25; 80 °C, NMP-PL은 2 min 미흡/3 min 핸들링가능/30 min 충분건조). 그래도
  **NMP 사용은 건식공정의 친환경 이점을 일부 훼손** → 향후 **수계 슬러리(기능성 binder) / 무용매 계면코팅**
  필요.

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.7):** (a) DPE 제작공정(powder mixing+kneading → laminating → calendering) + PL의 접착·도전
  중간층 역할(박리 vs well-adhered 대비; AM/conductive agent/PTFE fibril/PL/CC + 전자경로·접착강도 화살표).
  (b) PAA/CMC/PVDF binder 분자구조와 PAA-PL/CMC-PL/PVDF-PL. → **건식공정 + PL 개념도**(우리 공정 맥락).
- **Fig 2 (p.10):** (a) 재구성 3D XCT 구조 + top/middle/bottom 종단면 pore 분포(WPE·PAA·CMC·PVDF). (b)
  **두께방향 porosity 분포(1.25 µm 간격)** — DPE 구배 vs WPE 평탄, **PVDF 가장 가파름(24.5%p)**. (c) micro-
  indentation stress-strain, (d) 압축계수, (e) 탄성계수(PVDF 6.31/15.99 MPa 최저). (f) 대칭셀 모식, (g)
  EIS Nyquist, (h) 이온저항, (i) **이온 tortuosity**(DPE<WPE). → ★ **z-구배 정량 + 무른PL→구배 인과 + EIS
  tortuosity**(우리 Phase 5 + τ 검증 직접대응).
- **Fig 3 (p.12):** half-cell — (a) 초기전압곡선(311/313/343/355 mAh/g), (b) 100사이클 안정, (c) rate
  capability(0.1–5C; **3C 305 vs 258 mAh/g**), (d) **CC vs CV 막대**(3C CC 80.2 vs 23.3 mAh/g). → 급속충전
  성능 증거.
- **Fig 4 (p.14):** full-cell(NCM523) — (a) 초기전압, (b) rate, (c) **CC/CV SOC 막대**(3C CC 29%/PVDF vs
  14%/WPE), (d–g) **3C 충전 후 전극표면 SEM**(Li plating: WPE > PAA > CMC > PVDF, PVDF 최저). → Li plating
  억제 시각증거.
- **Fig 5 (p.17):** ★ FIB-SEM 토모그래피 — (a) 취득 모식 + WPE/PAA/PVDF 재구성 3D(graphite·pore·binder·CC
  분할). (b) bare Cu/PAA-PL/PVDF-PL 재구성 3D(변형). (c) **2D topological map**(높이차 PVDF 12.1 µm). (d)
  **정규화 AM↔PL 접촉면적**(PVDF +45%). (e) **top/mid/bottom porosity**(XCT vs FIB-SEM). (f–h) **PNM
  connectivity matrix**(WPE/PAA/PVDF; 밴드폭 PVDF>PAA>WPE). → ★ **토모그래피 정량 방법 전체**(우리 이식 대상).
- **Fig 6 (p.19):** 재구성 3D 전기화학시뮬 — (a–c) **활물질 내 3C CC종료 Li⁺ 3D맵**(PVDF 바닥까지 충전).
  (d–f) **deconvoluted overpotential vs 용량**(전해질·활물질 확산 과전압이 핵심; PVDF 최저). (g–i) **전해질
  Li⁺ 시공간분포(SOC×depth)**(PVDF 가장 균일; LDR/LER). → ★ **토모그래피→전기화학시뮬**(우리 Phase 4 연결).
- **Fig 7 (p.21):** 개념도 — WPE(균일 porosity, 급속충전 시 위쪽만 충전=불균일 SoC) vs porosity-구배
  DPE@PVDF-PL(변형 PVDF-PL → 위 다공·아래 치밀 → Li⁺ 균일 충전). → ★ **porosity-구배 설계 철학 1장 요약**.

### SI Figures (S1–S26) + Notes
- **Fig S1:** DPE@PAA/CMC/PVDF-PL 단면 SEM(세 DPE 두께·외형 유사 — 구배는 내부분포 차이지 외형 아님).
- **Fig S2:** MIP 곡선 + pore size 분포(WPE·DPE, 전체 porosity 32.2–33.3%).
- **Fig S3:** XCT 3D + 2D 분할 pore + 재구성 3D(세그멘테이션 절차).
- **Fig S4:** micro-indentation(SAICAS) 광학상 + 모식 + bare Cu/PAA/CMC/PVDF-PL 힘-변위곡선.
- **Fig S5:** dQ/dV(WPE = SEI만; DPE = SEI + PTFE 탈불소화 0.2–0.8 V).
- **Fig S6:** precycling 전압곡선(WPE vs DPE@PVDF-PL; DPE에 PTFE side-reaction plateau).
- **Fig S7:** **XPS**(formation 후) — C 1s·F 1s(WPE vs DPE@PVDF-PL). PTFE 탈불소화 산물(LiF 685.6 eV,
  CH₂-CF₂-CH₂ 290.9/688.0 eV, CHF-CF₂ 689.5 eV, 잔류 PTFE 292.5/690.0 eV) 확인.
- **Fig S8:** PTFE 함량 2/1/0.5 wt% top-view SEM(함량↓ → PTFE 나노피브릴망 덜 발달).
- **Fig S9:** PTFE 2/1/0.5 wt% full-cell(NCM622) precycling + **ICE vs PTFE 함량**.
- **Fig S10:** **SAICAS cohesion strength**(bulk, mid-thickness) vs PTFE 함량(0.5 wt%는 2 wt%의 35.1%).
- **Fig S11:** FIB-SEM 토모 + 활물질 분할 + WPE/PAA/PVDF 재구성 3D.
- **Fig S12:** **FIB-SEM 기반 half-cell 모델**(흑연복합전극+Cu CC+Li metal+separator) + 지배방정식 + 3C
  CC-CV 프로토콜.
- **Fig S13:** SAICAS 측정 절차(adhesive·cohesive) 카메라 이미지.
- **Fig S14:** **SAICAS adhesion/cohesion** — bulk cohesion(세 DPE 유사) / **DPE/PL adhesion(PVDF 최고:
  PAA보다 60.3%↑, CMC보다 34.6%↑ — 변형으로 접촉면적↑ → 기계 anchoring**) / PL/CC adhesion(유사, 약간 PAA>CMC>PVDF).
- **Fig S15:** **이온 확산 시뮬 지배방정식·경계조건**(D_e,eff). **Fig S16:** **FIB-SEM 기반 이온 tortuosity**
  (1.86/1.98/3.09).
- **Fig S17:** PNM **coordination number** + **equivalent pore radius**(평균 CN: PVDF 4.20/PAA 4.44/WPE 2.94).
- **Fig S18:** PNM 모식 + coordination number 정의/종류 + connectivity matrix 작도법.
- **Fig S19:** connectivity matrix overlay(WPE/PAA/PVDF) + 정규화 밴드폭 분포(표준편차 0.1581/0.1309/0.0976).
- **Fig S20:** 3C CC·CV 용량(실험 vs 시뮬) 비교. **Fig S21:** CC후/CC-CV후 활물질·전해질 Li⁺ 농도.
- **Fig S22:** CC-CV후 활성화 과전압 분포. **Fig S23:** CC-CV후 **CC·PL 3D 전류밀도 분포**.
- **Fig S24:** 3C 충전중 전해질 Li⁺ depth방향 분포(WPE/PAA/PVDF). **Fig S25:** NMP-PL 건조 사진(2/3/30 min).
- **Fig S26:** **VED·GED vs 전극밀도**(1.5→1.7 g/cm³ → VED 612→642 Wh/L, porosity 28.6→19.1%).
- **Table S1:** 3D 전기화학모델 지배방정식. **Table S2:** 파라미터(전해질농도 1.15 M, c_max,AM 29513
  mol/m³, σ_s,AM 0.93275 S/m, σ_s,graphite 2120 S/m, D_e 3.8346e-10 m²/s, D_s,AM 2e-14 m²/s, t₊ 0.250,
  BV rate const 8.1e-6, T 298.15 K). **Table S3:** 기호집. **Table S4:** VED/GED 계산 파라미터(10-stack
  3.3 Ah 파우치 → GED 217 Wh/kg, VED 612 Wh/L).
- **SI Note S1 (PTFE 탈불소화):** 첫 formation에서 PTFE 비가역 탈불소화 → LiF+비정질탄소(XPS 확인, Fig S7).
  **NCM622 full-cell**(NCM622:PVDF:CB 96:2:2, loading 18.7 mg/cm², 밀도 3.4 g/cm³, N/P~1.1): **DPE ICE
  82–83% vs WPE 88–89%; DPE 초기 방전 ~162 mAh/g vs WPE ~178(−10%)**. **PTFE 함량↓(2→1→0.5 wt%) → side-
  reaction plateau↓, 초기방전 162→173 mAh/g, ICE → ~87.8%(0.5 wt%)**. 그러나 **0.5 wt%는 cohesion이 2
  wt%의 35.1%로 약해짐(SAICAS)** → **PTFE 함량은 전기화학(ICE)↔기계강건성 사이 최적화 필요**.
- **SI Note S2 (SAICAS adhesion/cohesion):** bulk cohesion(mid-thickness, depth ~35 µm)은 세 DPE 유사
  (조성·loading 동일, mid porosity도 유사). **DPE/PL 계면 adhesion은 PVDF-PL이 최고**(PAA보다 60.3%↑,
  CMC보다 34.6%↑) — PVDF가 보통 PAA/CMC보다 결합력 약함에도 → **변형으로 늘어난 접촉면적·기계 anchoring**
  덕분(Fig 5d). PL/CC adhesion은 유사(약간 PAA>CMC>PVDF). ⇒ PVDF-PL의 기계강도는 충분.

---

## 6. 기술 미니용어집 (우리 맥락)

- **DPE / WPE:** 건식(PTFE 피브릴화, 무용매) / 습식(슬러리 코팅) 전극.
- **Primer Layer (PL):** 집전체↔전극 사이 conductive carbon+binder 박막(0.4 mg/cm², 8–9 µm 압축후).
  이 논문의 **주인공 변수** — 기계 변형성으로 구배 유도.
- **Porosity gradient (구배):** z(두께)방향 porosity 비균일(위 다공·아래 치밀). **전체 porosity는 같아도
  분포가 다름** — MIP(전체) vs XCT/FIB-SEM(z분포)로 구별.
- **Tortuosity (τ):** Li⁺ 경로의 우회도. EIS(식 1) + 확산시뮬(식 2, D_e,eff=ε/τ²·D_e) 두 방법. **낮을수록
  좋음**. 우리 τ_Laplace,eff / τ_Dijkstra와 대응.
- **Coordination number(PNM):** 한 pore에 연결된 이웃 pore 수(국소 연결성). **Connectivity matrix
  bandwidth:** 장거리 pore 연결성(밴드폭↑=먼 pore도 연결). 우리 percolation/CN 대응(단 **pore-network**
  관점 — 우리는 particle-contact 관점이라 쌍대(dual)).
- **CC / CV SOC:** 정전류로 도달한 충전상태(CC SOC↑ = 급속충전 우수) vs 이후 정전압 보충. **급속충전
  지표는 CC구간 비중.**
- **Concentration polarization(농도분극):** 급속충전 시 전해질 Li⁺ 고갈(LDR)·과잉(LER)으로 생기는 분극 →
  Li plating 유발. 구배가 이를 완화.
- **PTFE defluorination(탈불소화):** Li⁺이 PTFE를 환원 → LiF+비정질탄소. DPE ICE를 낮춤(85–87% vs 92.7%).
  우리 `additives.py`의 PTFE 상은 **기계/부피**만 모델 — 이 **전기화학 부반응은 우리 미반영**(향후 ICE 손실 항).
- **SAICAS:** 미세블레이드로 깊이별 절삭 → adhesion/cohesion 정량(우리 --coh / binder cohesion 측정법 대응).
- **MIP / XCT / FIB-SEM:** 수은압입(전체 porosity·pore size) / X선 CT(250 nm, 큰 도메인 z분포) / FIB-SEM
  (46.52 nm, 고해상 pore망·재구성 3D).

---

## ★ 7. 비교 vs 우리 DEM+MPM (frame [1]–[5])

⚠ **대전제(맨 먼저):** 이 논문은 **흑연 음극 + 액체전해질 일반 LIB**다 — 우리 **LPSCl sulfide ASSB
(고체전해질, 무전해질 contact-network)**가 **아니다**. 따라서:
- **절대 transport 값은 전이 불가.** 그들의 τ(1.86–3.09), σ는 **전해질이 채운 pore**의 ion 확산이고, 우리
  σ_ionic은 **SE 입자 접촉망**의 Kirchhoff/Holm 전도다 — 물리 메커니즘 자체가 다름(pore-filled liquid vs
  solid contact). 그들의 D_e,eff = ε/τ²·D_e(Bruggeman류)는 **전해질 도메인** 공식이지 SE-backbone 공식이 아님.
- 가져올 것은 **(a) 설계 개념(z-porosity 구배), (b) 측정/정량 방법(토모그래피 tortuosity·PNM·connectivity),
  (c) 정성 추세(구배↓tortuosity↓분극)** — **수치 앵커가 아니다.** (LPSCl 수치 앵커는 Bazzoun #
  `docs/lit_bazzoun2026_dem_fem_rnm.md`에서 가져옴.)

### (a) Phase 5 z-layer / porosity-gradient 합성 — ★ 가장 강한 연결
- **그들:** binder 변형성으로 **z-방향 porosity 구배(top porous, bottom dense, Δ24.5%p)**를 자발 형성 →
  토모그래피로 1.25 µm 간격 두께방향 porosity 프로파일 정량(Fig 2b).
- **우리:** Phase 5 = layered composite cathode (z-stacking, smooth interface). `extract_2d_microstructure.py`
  는 이미 **z-band stratified placement (K=8 bands, line 668)** + **tortuosity-driven pore elongation
  (line 826, aspect=1.3+2.0·clip((τ−1))) ** 보유. → **그들의 "두께방향 porosity 프로파일"이 정확히 우리
  Phase 5 z-band별 목표 porosity의 published 실증**.
- **ACTION:** 우리 Phase 5 z-stacking을 **단일 균일 porosity가 아니라 z-band별 porosity 구배**로 합성하는
  것이 실험적으로 정당함(이 논문). 우리 합성 출력에 **"두께방향 porosity(z) 프로파일"** metric을 추가하고,
  이 논문의 **top↔bottom Δporosity**를 layered-synth 검증 추세로 채택. (그들은 흑연이므로 절대 Δ24.5%p가
  아니라 **"위>아래 단조 구배 + 가파를수록 tortuosity↓"** 추세만 이식.)

### (b) σ_ionic ↔ tortuosity (τ_Laplace,eff) physics
- **그들:** **2가지 독립 tortuosity 측정** — (i) **EIS 식 (1)** `τ²=R_ion·A·ε·κ/(2d)`, (ii) **확산시뮬 식
  (2)** `D_e,eff=ε/τ²·D_e`(GeoDict FVM, FIB-SEM 재구성). 두 방법이 같은 순서(PVDF<PAA<WPE) → **교차검증**.
- **우리:** σ_ionic 폼이 `... · C(τ)` (τ_Laplace,eff / τ_Dijkstra), 우리 τ는 **particle-contact 망의
  geometric/Laplace tortuosity**. **그들 τ는 pore(전해질) 도메인의 확산 tortuosity** — 우리와 **쌍대(dual,
  pore vs solid)**. 그래도 **"τ↓ → 수송↑"의 부호·역할은 동일**.
- ★ **frame[4] 교차검증 가치:** 그들이 **EIS-derived τ(식 1) ↔ 토모-확산시뮬 τ(식 2)**를 같은 시료에서
  대조한 것은, **우리가 σ_ionic 폼의 C(τ)에 어떤 τ(Laplace vs Dijkstra)를 쓸지** 결정할 때 **2-방법 교차
  검증 템플릿**이 됨. (우리는 솔버=ground truth라 EIS 실측 τ가 없음; 그들 식 1은 우리가 실측 τ를 얻는 경로.)
- ⚠ **주의:** 그들 식 (2)는 **Bruggeman형 ε/τ²** — 우리 σ_ionic은 `√(φ−φc)·CN²·√cov·f_p³`로 percolation/
  contact 물리라 **형태가 다름**(전해질 연속체 vs 입자 접촉). 직접 폼 차용 금지; **개념(τ가 수송 게이트)만**.

### (c) 건식전극 + PTFE additive (우리 `additives.py` PTFE 상)
- **그들:** PTFE 피브릴(1D 나노피브릴) → **낮은 바인더 함량(2 wt%) + 발달한 pore 연결성**(CN 4.20 vs WPE
  2.94 — PTFE 1D 형태 + 부피큰 SBR/CMC 도메인 부재 덕). 또 **PTFE 탈불소화 → LiF+비정질탄소 → ICE↓**
  (85–87% vs 92.7%; full-cell 82–83% vs 88–89%).
- **우리:** `additives.py`가 **PTFE 피브릴을 roll-shear-drawn 1D fibril web**(PTFE_D=0.25 µm, L=40 µm,
  curl≈0.4, constant-volume drawing)으로 모델 → **이 논문의 "PTFE 1D 나노피브릴 → pore 연결성↑" 형태를
  기계/기하로는 이미 반영**. (#271 PTFE-void↓와 함께 PTFE additive 검증.)
- ★ **갭(우리가 안 하는 것):** **PTFE 탈불소화 전기화학 부반응**(LiF 생성·ICE 손실)은 우리 미모델. 우리
  PTFE 상은 **부피/기계/전자블로킹**만. → 향후 full-cell/ICE 예측을 한다면 **PTFE 함량 → ICE 손실 항**(이
  논문: 2 wt% −6%p ICE, 0.5 wt% 회복하나 cohesion 35%로 붕괴) 추가 후보. (단 우리는 ASSB라 PTFE 탈불소화
  관련성 낮음 — 일반 LIB 확장 시에만.)
- **frame[5] 분업 확인:** 그들은 **PTFE를 형태(pore 연결)+전기화학(탈불소화)**으로 다루지만 **DEM 접촉망
  σ도, MPM 소성 morphology도 없음** — pore-network/실험 쪽. **우리 DEM(접촉 σ)+MPM(소성)이 그들에게 없는
  입자스케일 메커니즘**.

### (d) 그들 토모그래피(3D XCT/FIB-SEM) vs 우리 voxel_conductivity / mpm3d 미세구조 — ★ 방법 이식
- **그들:** **FIB-SEM(46.52 nm, 800장, CNN 분할) → 재구성 3D → GeoDict(τ, D_e,eff) + PNM(MATLAB: CN,
  connectivity matrix) + BESTmicro 전기화학시뮬**. 다중스케일(XCT 250 nm 큰도메인 + FIB-SEM 46.52 nm 정밀).
- **우리:** `voxel_conductivity.py`(voxel 기반 σ), `mpm3d_compaction.py`(MLS-MPM 3D 미세구조,
  `--am-scaffold`/`--se-dump`로 실제 DEM 위치 import), `viz_mpm_continuum`(3D 메쉬, COMSOL-separable).
  우리도 **실제 미세구조 → 정량 → 시뮬** 파이프라인 보유.
- ★ **이식할 구체:**
  1) **z-방향 porosity 프로파일 추출(1.25 µm 간격)** — 우리 mpm3d/voxel 출력에 **top/mid/bottom +
     fine-bin(z) porosity** 리포트 추가(그들 Fig 2b 방식). 우리 `mpm3d_calibration.md`엔 단일 porosity만 있음.
  2) **PNM(pore network) coordination number + connectivity matrix bandwidth** — 우리는 **particle-contact
     CN**(Z_SE-SE)만; **pore-side CN/connectivity**는 없음. 이 **pore-network 관점**은 **수송 병목을 pore
     쪽에서 보는 보완 지표** → `voxel_conductivity`에 watershed pore 분할 + connectivity matrix 추가 후보.
  3) **확산-시뮬 tortuosity(GeoDict류 ε/τ²)** — 우리 σ_ionic은 contact-Kirchhoff. 우리 voxel에 **pore-
     도메인 Laplace 확산 τ**(그들 식 2)를 병행 계산하면 **contact-σ ↔ pore-τ 교차검증**(frame[4]).
- ⚠ **우리가 더 가진 것:** 그들은 **pore 도메인 연속체 확산**만; 우리는 **explicit 입자 접촉망 σ(ionic/e/
  thermal triad) + Stage-E 소성 접촉면적 + fracture-Holm + MPM 소성 morphology**. 그들 토모는 **고정
  미세구조 정량**이지 **압축역학 예측은 못함**(post-mortem 구조). 우리 DEM+MPM은 **압력→미세구조→σ를 예측**.

### (e) 농도분극 (Phase 4 PyBaMM 연결)
- **그들:** **재구성 3D 기반 BESTmicro 전기화학시뮬**로 농도분극·과전압·Li⁺ 분포·CC/CV SOC를 정량(Fig 6,
  S20–S24). LDR/LER onset/지속시간까지(WPE 434 s vs PVDF 80 s).
- **우리:** Phase 4 = 예측수치 → 2D 이미지; PyBaMM 연결은 로드맵(Phase 4 연결점). 그들은 **미세구조→전기
  화학 성능(분극)**을 BESTmicro로 닫음 — **우리 Phase 4(미세구조→전기화학) 청사진**.
- ★ **ACTION:** 우리가 합성한 미세구조(또는 mpm3d 3D)를 **DFN/P2D(PyBaMM) 또는 그들식 3D FVM**에 넣어
  **농도분극·CC SOC**를 뽑는 게 Phase 4의 다음 단계 — 이 논문이 **흑연계에서의 reference workflow**(3C
  CC-CV, 0.005 V cutoff, 0.3C 종료, Butler-Volmer + Fick). 단 **ASSB는 전해질 농도분극이 아니라 SE
  contact/입계 저항**이 지배 → 우리는 **PyBaMM의 전해질 항 대신 SE-network σ를 effective transport로**
  넣어야 함(직접 차용 아닌 적응).

### 비교 요약표
| 축 | Yoo 2026 (흑연/액체) | 우리 (LPSCl ASSB) | 이식/교훈 |
|---|---|---|---|
| 소재 | 천연흑연 + 액체전해질 | LPSCl SE + NMC811 | ⚠ 절대값 전이불가 |
| 구배 | binder변형 → z-porosity 구배 자발 | Phase 5 z-band(미실증) | ★ 설계개념·z-프로파일 metric 이식 |
| tortuosity | EIS(식1)+확산시뮬(식2), pore도메인 | C(τ) contact, Laplace/Dijkstra | 2-방법 τ 교차검증 템플릿 |
| 미세구조 | XCT 250nm + FIB-SEM 46.52nm 재구성 | voxel/mpm3d, DEM scaffold | z-porosity + PNM connectivity 추가 |
| 전기화학시뮬 | BESTmicro 3D FVM(BV+Fick) | Phase 4(PyBaMM 예정) | 흑연계 reference workflow |
| PTFE | 1D피브릴 pore↑ + 탈불소화 ICE↓ | additives.py PTFE 기계/부피만 | 탈불소화 ICE손실 항(일반LIB 확장시) |
| 우리 고유 | (없음) | DEM 접촉 σ triad + MPM 소성 + fracture | 그들엔 입자스케일 예측 없음 |

---

## ★ 8. 우리 작업에 넣을 가장 날카로운 인사이트 3가지

1) **z-방향 porosity 구배는 "버그가 아니라 설계 자유도"다 — Phase 5를 균일이 아닌 graded로.**
   전체 porosity가 같아도(32–33%) z-분포만 위 다공·아래 치밀로 바꾸면 tortuosity 3.09→1.86, 3C CC용량
   23→80 mAh/g(half-cell)으로 급변. → 우리 layered 합성(z-band K=8)은 **band마다 다른 목표 porosity**로
   가야 하고, 출력에 **"두께방향 porosity(z) 프로파일"** + **top↔bottom Δporosity** metric을 추가해야 함.
   (메커니즘: 무른 중간층 소성변형 → 압축 비대칭 → 우리 **MPM 압축 + scaffold**로 재현 가능한 물리.)

2) **토모그래피 정량 3종 세트(확산-τ, PNM coordination, connectivity-matrix bandwidth)를 우리
   voxel/mpm3d에 이식 — 특히 pore-side 지표.** 우리는 particle-contact CN(Z_SE-SE)만 있고 **pore 관점
   연결성**이 없다. 그들 PNM(watershed pore 분할 → CN + connectivity matrix 정규화 밴드폭 표준편차)은
   **수송 병목을 pore 쪽에서 정량하는 보완축**이고, **확산-시뮬 τ(ε/τ²·D_e)**는 우리 contact-σ와 **frame[4]
   교차검증**이 된다. → `voxel_conductivity`에 pore-network + 확산-τ 추가 → contact-σ ↔ pore-τ 일치도 측정.

3) **frame[5] 재확인 + 우리 우위 명확화:** 이 논문은 **토모그래피 + 연속체 확산/전기화학시뮬**로 강하지만
   **입자스케일 압축역학 예측이 없다**(post-mortem 고정 미세구조). 우리 DEM+MPM은 **압력→미세구조→σ를
   예측**하고 **소성 morphology·explicit 접촉 σ triad·fracture**까지 간다. ⇒ **이상적 워크플로 = 우리
   DEM+MPM이 미세구조를 생성/예측 → 그들식 토모-정량(τ/PNM)으로 검증 → 그들식 3D 전기화학시뮬(BESTmicro/
   PyBaMM)로 농도분극 닫기.** 이 논문은 우리 파이프라인의 **출력단(검증·전기화학) 청사진**이지 입력단
   경쟁자가 아니다.

### 보너스 실행 항목
- **#286 인덱스 갱신**(아래 완료): web-abstract 수준 → 검증 수치(24.5%p 구배, τ 1.86/1.98/3.09, CN 4.20/
  4.44/2.94, 3C 305 vs 258, PVDF 6.31/15.99 MPa, ICE 85–87% vs 92.7%)로 교체.
- **그들 식 (1) EIS-τ**를 우리가 **실측 tortuosity를 얻는 경로**로 기록(현재 우리는 외부 실측 τ 없음 —
  Bazzoun이 σ 앵커를 줬듯, 이 논문류 EIS가 τ 앵커 후보, 단 흑연이라 LPSCl 직접앵커는 아님).
- ⚠ **혼동 금지:** Bazzoun(#, LPSCl, frame[4] σ 앵커)과 이 논문(#286, 흑연, **방법/설계 청사진**)은 역할이
  다르다. 이 논문은 **수치 앵커가 아니라 z-구배 설계 + 토모 정량 방법 + 전기화학시뮬 workflow** 공급원.
