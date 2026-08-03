# Phase stability, electrochemical stability and ionic conductivity of the Li₁₀±₁MP₂X₁₂ (M = Ge, Si, Sn, Al or P, and X = O, S or Se) family of superionic conductors — Ong/Mo/Richards/Miara/Lee/Ceder (Energy Environ. Sci. 2013)

> slug `ong2013_lgps_family_substitution` · DOI `10.1039/c2ee23355j` · type `DFT+AIMD (순수 계산, 실험 0)` · PDF **본문 `litdb/inbox/43. Phase stability, electrochemical stability and ionic conductivity of the Li10±1MP2X12 …pdf`(9 pp = 148–156)** · **ESI 미보유**(논문이 참조하는 ESI는 별도 파일 — 안정상 전체 목록·이완 구조 상세·σ 환산식은 n/a) · (inbox #43) · **사용자 분류 폴더 `DFT`** · digested `2026-07-28` · **본문 실물 독립 검증 `2026-08-03`(§18 — 전문 텍스트 추출 + Fig 1–5·Eq 1–2 이미지 판독, Fig 2 DOS 3패널 픽셀 디지타이즈; 교정 5건·신규 적발 9건·미결 3건)** · status ✅ **(본문 실물 대조 완료 — ESI만 미보유)**
> elements: Li, Ge, Si, Sn, Al, P, S, O, Se
> methods: DFT, AIMD, DOS, ESW
> **저자**: Shyue Ping Ong, Yifei Mo, William Davidson Richards (MIT DMSE) · Lincoln Miara, Hyo Sug Lee (Samsung SAIT, Cambridge MA) · **Gerbrand Ceder*** (MIT) · Energy Environ. Sci. 2013, **6**, 148–156 · Received 2012-06-15 / Accepted 2012-10-01 / Published online 2012-10-02
> 자금: Samsung SAIT + TeraGrid(PSC)·NERSC(DOE DE-AC02-05CH11231)

---

## 0. 이 digest를 읽는 법 (우리 캠페인에서의 위치) ★
**조성족(組成族) 치환 스크리닝의 원형 — 우리 47-도펀트 cascade의 2013년 조상이다.** Kamaya 2011이 LGPS(Li₁₀GeP₂S₁₂, σ=12 mS/cm)를 보고한 지 1년 만에, Ceder 그룹+Samsung이 **같은 구조 골격에서 양이온 M(Ge→Si/Sn/Al/P)×음이온 X(S→O/Se)를 계산으로 전수 교환**해 "무엇을 바꾸면 무엇이 변하나"를 상안정·전기화학안정·σ 3축으로 처음 표준화했다. 유명한 결론 두 줄 — **"σ는 골격 양이온에 둔감하고(스크리닝), 음이온에 민감하다(채널 기하)"**, **"S²⁻ 크기가 이 골격에서 근최적"** — 이 여기서 나왔고, Zeo++ 채널크기·격자 스케일링 스캔은 우리 BVSE 채널%·migration_volume 논리의 직계 조상이다.

**Ceder 열역학 4부작의 제1편**: 이 논문(2013, *조성족 스캔* — 2-포인트 grand potential) → **[Zhu15]**(2015, *창 정량* — μ_Li(φ) 전 구간 스캔; UMD Mo가 이 논문 공저자) → **[Rich16]**(2016, *전극 계면* pseudo-binary; Richards도 이 논문 공저자) → **[Xiao19]**(2019, *HT 코팅 깔때기*) → **우리 cascade**(2026, host-도펀트 47종 가중 score). 즉 우리 파이프라인의 세 축(상안정 hull / grand-potential ESW / 수송 프록시→MD 검증) 전부가 이 논문의 3축 구성(E_decomp / band gap+grand potential 2-point / AIMD)을 현대화한 것이다.

## 1. 한 줄 요약
LGPS 골격에서 M=Ge/Si/Sn(+aliovalent Al/P)×X=O/S/Se를 DFT(상안정·HSE DOS·Li grand potential 2-포인트)+AIMD로 전수 평가 — **등가 양이온 치환은 상안정·전기화학·σ 모두 거의 못 바꾸고(Li₁₀SiP₂S₁₂ 23·Li₁₀SnP₂S₁₂ 6 vs LGPS 13 mS/cm, 오차 내 동일), 음이온 치환이 지배 변수**(O: E_decomp>90 meV/atom 불안정+σ 0.03 mS/cm 3자릿수↓ / Se: σ 소폭↑·안정성↓)이며, 격자 스케일링 스캔(−4~+4%)의 **비대칭 반응**(수축 −1%에 σ 1/10, 팽창 +4%에 6×뿐)으로 **"S²⁻가 이 골격의 근최적 크기, 임계 채널크기 존재"**를 결론 — Ge의 비용 문제는 Si/Sn으로 풀리지만 황화물의 공기민감성은 산화물 치환으로 못 푼다.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 저자/기관 | Ong·Mo·Richards·Ceder*(MIT) + Miara·Lee(Samsung SAIT) — Ong=pymatgen 창시자([Deng16] UCSD行 전), Mo=이후 UMD([Zhu15]·[Banik]), Richards=[Rich16] 1저자, Miara=[Rich16]·[Xiao19] 공저 |
| 저널 | Energy Environ. Sci. 2013, 6, 148–156 (9 pp) |
| DOI | 10.1039/c2ee23355j |
| 유형 | 순수 계산 (VASP DFT + AIMD; 자체 실험 0) |
| 대상 | **Li₁₀±₁MP₂X₁₂ 11조성**: (Si,Ge,Sn)×(O,S,Se) 9 + Li₉P₃S₁₂ + Li₁₁AlP₂S₁₂ (Al/P는 황화물만) — ⚠ M×X 전조합 15가 아니라 **aliovalent는 S 한정 → 총 11조성** |
| 동기 | LGPS의 두 약점 — ① Ge 희소·고가 ② 황화물 공기/수분 민감 — 을 같은 구조 안에서 치환으로 풀 수 있나? |
| 선행 | ref 7 = Mo/Ong/Ceder 2012 Chem. Mater. 24, 15–17 (LGPS 단일물질 1차 계산: metastable·**Li 금속에 불안정·고전압 분해**·gap 3.6 eV·">5 V 실험창=passivation(Li₂S 또는 P₂S₅)"·a–b면 확산 2경로) — **"Li 금속 불안정" 최초 예측은 이 논문이 아니라 ref 7**; 본 논문은 그것을 조성족 전체로 일반화 |

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| **σ(300 K) 조성족** | LGPS **13** / Si **23** / Sn **6** / Li₉P₃S₁₂ 4 / Li₁₁AlP₂S₁₂ 33 / **O 0.03** / Se 24 mS/cm | AIMD Arrhenius 외삽 | **황화물 5종은 "오차 내 동일"이 논문 판정** (aliovalent는 t-검정) |
| **Ea 조성족** | 0.21±0.04(Ge)/0.20±0.03(Si)/0.24±0.03(Sn)/0.26±0.09(P)/0.18±0.06(Al)/**0.36±0.05(O)**/0.19±0.04(Se) eV | 〃 | O만 유의 상승 |
| **E_decomp(상안정)** | 황화물 19–25(Al 60) / 셀렌화물 16–19 / **산화물 92–97** meV/atom | PBE hull, 0 K | 전 조성 metastable; 산화물만 "합성 불가" 판정 |
| 격자 스케일링 | −4/−2/−1/0/+2/+4% → Ea 0.59/0.47/0.28/0.23/0.19/0.17 eV·σ 4.6e-8/4.8e-6/1.7/13/44/75 mS/cm | LGPS 등방 스케일, AIMD | **비대칭**: −1%에 σ÷10, −2%↓에 6자릿수↓; +4%에 ×6뿐 |
| 채널크기(Zeo++) | O 1.43–1.50 / S 1.84–1.92 / Se 1.96–1.97 Å | Li 제거 후 최대 통과 구 | O는 S보다 ~20%↓, Se ~7%↑; **M 효과 미미** |
| band gap | **본문 수치 0 — 순서 O > S > Se만 서술**. Fig 2 디지타이즈(2026-08-03): **O ≈ 6.7 / S ≈ 3.7 / Se ≈ 2.3 eV** (±0.15, DOS onset 정의) | HSE, non-spin | LGPS 3.6 eV는 ref 7 소환값 — 우리 디지타이즈 3.7과 정합(교차검증 통과). VBM·CBM 모두 음이온 상태 |
| ESW onset | **n/a — 이 논문은 onset 미계산** | grand potential은 0 V·5 V **2-포인트만** | 창 onset 정량은 [Zhu15]가 처음 (LGPS 1.71–2.14 V) |
| 기계 물성 | n/a | — | 범위 밖 ([Deng16]이 LGPS/LSiPS/LSnPS 탄성 후속) |

## 4. DFT/계산 방법 ★ (2013년 관행의 표준 명세 — 서베이 §3 대비용)
### 4a. 공통
- **code**: VASP + PAW (refs 10–11). 기법별로 functional·셋업을 분리 선택했다고 명시 ("vastly different requirements … carefully selected").
- **무질서 처리 (★ 이 논문의 핵심 기술 절차)**: 정련 LGPS(P4₂/nmc)는 Li 자리+Ge/P 자리 부분점유 → **pymatgen(ref 18, 당시 "submitted") Ewald 정전에너지 기준(ref 17)으로 배열 정렬**. 이상화 전하 Li⁺¹/Ge⁺⁴/P⁺⁵/S⁻². **정전에너지 최저 30개 배열 → DFT 이완** → 최저 정전 배열은 정방 P4₂/mc 유지지만 **DFT 바닥상태는 P1(정방에서 미세 왜곡)이고 모든 LMPX에서 정전-최저 구조보다 ~10 meV/atom 낮음** → 이후 전 분석은 이 DFT-GS(P1) 사용. RT에서는 Li 무질서로 더 높은 대칭이 실현될 것과, 비교는 "similar orderings 간 상대 안정성"이라 유효함을 명시.
- **파생 구조**: isovalent LMPX = DFT-GS에 M/X 직접 치환. **aliovalent(Al³⁺/P⁵⁺ + Li 보상)는 정전 정렬 후 최저 1개 배열만 DFT** (배열 다중 계산 안 함 — 비용 명시). SQS 없음 — 전 조성 **단일 질서 배열** 노선.
### 4b. 상안정 (phase diagram)
- Li–M–P–X 4원 상도 (refs 12–13 = Ong 2008 Chem. Mater./2010 Electrochem. Commun. — grand-potential phase diagram 형식의 자기 원전). 상 공간 채우기: **ICSD 전 등재상 + Holzwarth LixPySz 컴파일(ref 15) + Li–M–X/Li–P–X 기지상의 O↔S↔Se 상호치환 파생상**(Li–P–Se·Li–M–Se가 미개척이라 치환 생성으로 커버) — 우리 hull의 "entry set이 결과를 좌우한다" 규율의 원형적 자각.
- **PBE, spin-polarized, k-밀도 ≥ 500/(셀 원자수)**. E_decomp = 조성 고정 분해반응 에너지의 음수/원자.
### 4c. 전기화학 안정성 — 2-트랙 (이후 [Zhu15]·[Banik]·우리 B①의 전신)
1. **Intrinsic(불활성 전극) = band gap**: 반국소 DFT의 gap 과소평가를 피해 **HSE screened hybrid**(refs 20–23)로 전 조성 DOS. HSE 비용 때문에 **non-spin-polarized**. "gap은 외부 기준전위에 대한 정렬을 모르므로 창의 **상한**일 뿐"이라고 명시 (= 우리 "VBM/gap ≠ onset" 규율의 2013 원문).
2. **전극과의 화학 안정성 = Li grand potential 상도**: μ_Li = μ⁰_Li(Li 금속 음극)과 **μ⁰_Li − 5 eV(5 V 만충 양극)** — **두 극단점에서만** 평형상 평가. 전압=−μ_Li. "Li 교환 반응 경로만 보고, 양극 비-Li 원소와의 반응은 미고려" 자인 (→ 그 공백을 [Rich16] pseudo-binary가 채움). **전 구간 φ 스캔·onset 전압은 없음** — 그건 [Zhu15]의 기여.
### 4d. AIMD (Li 확산) — 2013년 프로토콜 전문
- **PBE**, 비용 절감용 **저컷오프: 산화물 400 / 황화물 280 / 셀렌화물 270 eV**, **Γ-only 1×1×1**, non-spin.
- **셀 = LMPX 단위셀 1개**(원자수는 논문 미기재 — Table 2 부피와 Z=2 f.u.로부터 **50원자로 산술 추정**, 인용 시 "추정" 명시); 2×2×1 초격자 수렴 테스트로 "단위셀로 충분" 판정. 부피·초기좌표 = 상안정 계산의 완전 이완 셀 (**NVT 고정 부피 = 0 K DFT 부피** — 열팽창 미반영).
- Verlet, **Δt = 2 fs**. 절차: ① 100 K Boltzmann 초기속도 → ② 목표온도(600–1200 K)로 **velocity scaling 1000 스텝(2 ps) 승온** → ③ **Nosé–Hoover NVT 5000 스텝(10 ps) 평형화** → ④ **확산 생산 40–400 ps, D 수렴까지** 연장. **용융 또는 M–X 결합 파괴가 관찰된 온도점은 제외** — Li₁₁AlP₂S₁₂·Li₉P₃S₁₂는 1000/1100/1200 K 제외(Al–S/P–S 파괴), Li₁₀GeP₂Se₁₂는 1000–1200 K 제외(용융). (**⚠ 초판의 "Fig 5에 1000/T=2.0(=500 K) 데이터점이 보인다"는 오독 — 2026-08-03 800 dpi 재판독 결과 우측 프레임(=2.0)에 닿는 것은 *피팅 직선의 외삽*뿐이고 마커는 없다. Fig 3·4·5 모두 동일. 온도창은 본문대로 600–1200 K.**)
- **★ d=3(등방 3D)을 정당화하는 서론의 4단 논증** (초판 누락 — 이 논문에서 방법 선택의 근거가 되는 유일한 문헌 사슬):
  ① **Kamaya 2011[6]**: LGPS 확산은 c축 **1D** 경로라 제안 — 근거는 직접 측정이 아니라 **큰 이방성 열인자 + 1D 채널 내 Li 무질서**(간접 추론). LiS₄ 사면체 Li가 c축 확산을 담당하고 **LiS₆ 팔면체 Li는 확산에 비활성**이라는 가설도 함께.
  ② **Mo/Ong/Ceder 2012[7]**(= ref 7, 자기 선행): AIMD로 c축 고속 확산을 확인하되 **a–b면에 추가 경로 2개**를 발견 — c축만큼 쉽지는 않지만 전체 성능에 기여.
  ③ **Adams & Prasada Rao 2012[8]**: 결합원자가 기반 Morse 힘장 고전 MD로 **약한 이방성**이라는 독립 결론.
  ④ **Malik/Bazant/Ceder 2010[9]**: 실제로 쓸 만한 거리를 수송하려면 **1차원 초과 차원이 필요**하다.
  → 그래서 d=3. 즉 **"LGPS는 1D다"라는 통설을 이 그룹이 2012–2013에 이미 정면으로 수정**했고, 그 위에서 등방 D를 쓴 것 (§14의 "d=3 등방 취급" 한계는 여전히 유효하지만, 그것이 무지의 소산은 아님).
- **D = ⟨[r(t)]²⟩/(2d·t), d=3** (전 조성 3D 취급 — LGPS 준1D 논쟁을 알면서도; ref 7·Adams ref 8이 a–b면 경로 확인했으므로 3D 평균이 정당하다는 입장). MSD는 **개별 Li 추적(self/tracer-D)** + 시간원점 ensemble 평균; "교차상관 없으면 center-of-mass D와 동일" 언급 = **암묵적 Haven=1** (σ 환산식 자체는 본문 미기재, ESI 추정 — 우리 NE(Haven=1) 관행의 조상).
- **Arrhenius 다점(600–1200 K) 선형 피팅 → 300 K 외삽**, Ea 오차막대는 피팅 표준오차(±0.03–0.09 eV), aliovalent 판정에 **t-통계 검정** 사용.

## 5. 결과 I — 상안정·구조 (Table 1·2)
### 5a. Table 1 전량 — Li₁₀±₁MP₂X₁₂ 조성의 평형 분해 + E_decomp (meV/atom)
| M | X | 평형 분해 조합 | E_decomp |
|---|---|---|---|
| Si | O | Li₄SiO₄ + 2Li₃PO₄ | 92 |
| Ge | O | Li₄GeO₄ + 2Li₃PO₄ | 96 |
| Sn | O | 0.33Li₈SnO₆ + 0.67Li₂SnO₃ + 2Li₃PO₄ | 97 |
| Si | S | Li₄SiS₄ + 2Li₃PS₄ | 19 |
| Ge | S | Li₄GeS₄ + 2Li₃PS₄ | **25** |
| Sn | S | Li₄SnS₄ + 2Li₃PS₄ | 25 |
| Al | S | Li₅AlS₄ + 2Li₃PS₄ | 60 |
| P | S | 3Li₃PS₄ | 22 |
| Si | Se | Li₄SiSe₄ + Li₄P₂Se₆ + Li₂Se + Se | 16 |
| Ge | Se | Li₄GeSe₄ + Li₄P₂Se₆ + Li₂Se + Se | 16 |
| Sn | Se | Li₄SnSe₄ + Li₄P₂Se₆ + Li₂Se + Se | 19 |
- **전 조성 열역학 불안정(metastable)**. 황·셀렌화물 ≤25 meV/atom(Al만 60) = "엔트로피로 안정화되거나 metastable로 합성 가능" / **산화물 >90 meV/atom = "합성 자체가 어려울 것"** — 이유는 **초안정 Li₃PO₄가 조성 경쟁 상을 지배**하기 때문 (우리·[Zhu20]의 "인산염 구동력"과 같은 화학).
- 평형 조합의 규칙성: 산화물·황화물 = **Li₄MX₄ + Li₃PX₄** (Sn–O만 예외: Li₄SnO₄가 Li₈SnO₆+Li₂SnO₃에 불안정); 셀렌화물 = Li₄MSe₄ + **Li₄P₂Se₆+Li₂Se+Se**(Li₃PSe₄ 자체가 불안정). Li₄SnS₄는 당시 갓 합성 보고(Kaib 2012, ref 28)됐고 계산도 안정 예측 — hull 예측력의 셀프 검증 사례.
- **★ Li₉P₃S₁₂ 행(22 meV/atom)은 다른 10행과 성격이 다르다 (2026-08-03 신규 적발)**: 분해 조합 "3Li₃PS₄"는 **조성이 원물질과 완전히 동일**하다(Li₉P₃S₁₂ ≡ 3×Li₃PS₄). 즉 이 22 meV/atom은 *다상 분해* 에너지가 아니라 **LGPS 골격 배열 vs Li₃PS₄ 바닥 다형(β/γ)의 다형 에너지차**다. 나머지 10행(진짜 2–4상 분해)과 한 표에서 같은 척도로 읽으면 안 된다. 논문은 이 구분을 하지 않는다. → **인용 시**: "P-치환체는 hull 위 22 meV/atom" 대신 "**Li₃PS₄ 다형보다 22 meV/atom 높은 골격 배열**"이 정확.
- **양이온은 안정성에도 거의 무영향**(Al 제외) — "M 둔감"의 상안정판. ⚠ 단 **Al만은 이 규칙의 반례이자 trade-off의 예시**: 채널크기 1.92 Å로 황화물 중 **최대**(→ Ea 최저 0.18·σ 최고 33)인데 동시에 E_decomp **60 meV/atom으로 황화물 중 최악**(다른 황화물의 2.4–3.2배). **"채널을 넓히는 치환은 상안정을 판다"** — 논문이 두 표를 연결해 말하지 않은 관찰이고, 우리 도펀트 cascade의 σ↔hull 가중 score가 정확히 이 trade-off를 수치화하려는 것이다.
- 참고: LGPS E_hull 25는 [Zhu15]의 21 meV/atom(MP-2015)과 정합; comp1(Li₆PS₅Cl) 83(ordered, [Zhu15])·Cl1.5 28([Rao])과 같은 "황화물 SE = 수십 meV/atom metastable" 줄.

### 5b. Table 2 전량 — 이완 구조 + Zeo++ 채널크기
| M | X | a/b/c (Å) | V (Å³) | 채널크기 (Å) |
|---|---|---|---|---|
| Si | O | 6.985/6.990/10.649 | 520 | 1.43 |
| Ge | O | 7.151/6.976/10.709 | 534 | 1.46 |
| Sn | O | 7.499/6.821/10.966 | 561 | 1.50 |
| Si | S | 8.566/8.848/12.920 | 979 | 1.84 |
| Ge | S | 8.561/8.847/12.929 | **979** | **1.84** |
| Sn | S | 8.666/8.950/13.133 | 1018 | 1.86 |
| Al | S | 8.722/8.567/13.662 | 1021 | **1.92** |
| P | S | 8.817/8.817/12.660 | 984 | 1.87 |
| Si | Se | 9.040/9.381/13.630 | 1155 | 1.97 |
| Ge | Se | 9.054/9.400/13.690 | 1164 | 1.96 |
| Sn | Se | 9.084/9.434/13.797 | 1181 | 1.97 |
(각도 α/β/γ는 90±2° 내 — P1 미세 왜곡. 원표에 전값 있음.)
- 부피: **V_O/V_S 실측 0.531/0.545/0.551**(Si/Ge/Sn) (경식구 추정 (r_O/r_S)³=0.407; Shannon r: O²⁻ 126/S²⁻ 170/Se²⁻ 184 pm), **V_Se/V_S 1.180/1.189/1.160**(추정 1.268) — "부피 차의 상당분은 음이온 반경 몫" (⚠ **원문 "around 53–55% smaller"는 서술 오류** — 0.53–0.55는 *비율*이고, 실제 *감소폭*은 **44.9–46.9 %**다. 셀렌화물 쪽 "16–19% larger"는 반대로 감소폭이 아니라 증가폭이라 정확 → 같은 문장 안에서 두 표현의 기준이 다르다. 인용 시 "부피가 S의 53–55 % 수준"으로 고쳐 쓸 것).
- **채널크기 = Zeo++(refs 30–31)로 Li 전부 제거 후 골격을 통과할 수 있는 최대 자유 구의 지름**: 음이온이 지배(O −20%/Se +7% vs S), **M은 미미** — Al–S만 1.92 Å로 황화물 중 최대(Li₁₁AlP₂S₁₂의 소폭 높은 σ·낮은 Ea를 "부분적으로" 설명하는 데 사용).

## 6. 결과 II — band gap (Fig 2, HSE DOS)
- 전 조성 DOS가 M에 무관하게 유사 → Li₁₀GeP₂X₁₂ 3종만 게재. **gap 순서: LMPO > LMPS > LMPSe** (본문·표에 **수치 0**, LGPS 3.6 eV만 ref 7 소환).
- **★ Fig 2 픽셀 디지타이즈(2026-08-03, 600 dpi)**: 세 패널 모두 x축 눈금(0/2/4/6/8 eV)과 점선(=0 eV)을 검출해 122.75 px/eV로 보정한 뒤, 0 eV 오른쪽 첫 유색 화소를 CBM onset으로 판독 —

| X | VBM(판독) | CBM onset | **HSE gap** |
|---|---|---|---|
| O | −0.05 eV | +6.73 eV | **≈ 6.7 eV** |
| S | −0.07 | +3.68 | **≈ 3.7 eV** |
| Se | −0.14 | +2.31 | **≈ 2.3 eV** |

  (VBM이 0에서 −0.1 eV 안쪽으로 밀린 것은 Gaussian smearing 꼬리 — 즉 **점선 = VBM 정렬**이고 gap ≈ CBM 값. 디지타이즈 오차 ±0.15 eV.) **검증 포인트: S 판독 3.7이 ref 7(Mo 2012)의 LGPS HSE gap 3.6 eV와 일치** → 판독 스케일 자체가 교차검증됨. **초판의 figure-read "O ~5 / Se ~2.8"은 둘 다 오독(교정 §18.1-1).** 격차는 O→S 3.0 eV, S→Se 1.4 eV로 **음이온 p 준위 상승이 gap을 지배**한다는 저자 서술과 정량적으로 정합.
- **VBM·CBM 모두 음이온 상태가 지배 — 음이온 화학과 무관하게**. 트렌드 기원 = 주기율표 아래로 갈수록 음이온 원자가 p-준위 상승. **= [Banik] "VBM=S 3p가 산화 onset을 pin"의 9년 전 조상** (단 여기선 자리 분해·COHP 없음, 조성 수준 관찰).
- gap의 지위: "전기화학 창의 **상한**"(ref 19) — O-치환은 intrinsic redox 안정성 최고, Se 최저. **그러나 §8의 반전이 이 논문의 백미** (intrinsic만 보면 틀린다).

## 7. 결과 III — 전극 화학 안정성 (Table 3, 2-포인트 grand potential)
### Table 3 전량 — μ_Li 두 극단의 평형상
| M | X | 5 V 양극 (μ⁰−5 eV) | Li 음극 (μ⁰) |
|---|---|---|---|
| Ge | O | GeP₂O₇, **O₂** | Li₁₅Ge₄, Li₂O, Li₃P |
| Si | O | SiP₂O₇, **O₂** | Li₂₁Si₅, Li₂O, Li₃P |
| Sn | O | SnP₂O₇, **O₂** | Li₁₇Sn₄, Li₂O, Li₃P |
| Ge | S | GeS₂, P₂S₅, S | Li₁₅Ge₄, Li₂S, Li₃P |
| Si | S | SiS₂, P₂S₅, S | Li₂₁Si₅, Li₂S, Li₃P |
| Sn | S | SnPS₃, P₂S₅, S | Li₁₇Sn₄, Li₂S, Li₃P |
| Al | S | AlPS₄, P₂S₅, S | Li₃Al₂, Li₂S, Li₃P |
| P | S | P₂S₅, S | Li₂S, Li₃P |
| Ge | Se | Ge₄Se₉, PSe, Se | Li₁₅Ge₄, Li₂Se, Li₃P |
| Si | Se | SiSe₂, PSe, Se | Li₂₁Si₅, Li₂Se, Li₃P |
| Sn | Se | SnPSe₃, PSe, Se | Li₁₇Sn₄, Li₂Se, Li₃P |
- **음극(0 V)**: 전 조성 **Li₂X + Li₃P + LiₓM_y 합금**으로 환원. 핵심 문장 둘 — ① 이 산물들은 "비교적 좋은 Li⁺ 전도" → **"Li에 불안정하지만 전도성 SEI(solid electrolyte interphase) 형성은 가능"** — SE 분해층을 SEI로 명명한 이른 사례; ② **"금속성 산물의 존재가 걱정스럽고 interphase가 시간에 따라 두꺼워질 수 있다"** — 2년 뒤 [Zhu15]의 **MCI(전도성 산물=passivation 실패=연속 분해) 이분법의 맹아**. 단 여기선 전자절연/전도 구분·μ̃_e⁻ 논리는 아직 없음.
- **양극(5 V)**: **음이온이 운명을 가름** — 산화물은 **MₓP_yO_z + O₂ 기체 방출**("장기 안정성에 심각") vs 황·셀렌화물은 **P₂S₅/PSe** = "좋은 유리질 이온전도체가 될 수 있어 **passivating할 수 있다**"(ref 33 Mizuno) — ref 7의 "실험 >5 V 창=passivation" 가설의 조성족 확장.
- ⚠ **onset 전압 없음**: 5 V 극단의 평형상만 있고 "몇 V부터 분해되나"는 없다. LGPS 환원 1.71 V·산화 2.14 V는 **[Zhu15]가 처음 정량** (같은 계보, 산물은 연속: 이 논문 0 V 산물 Li₁₅Ge₄+Li₂S+Li₃P = [Zhu15] 0 V와 동일; 5 V 산물 GeS₂+P₂S₅+S = [Zhu15] 5 V와 동일 — **11년·DB 세대를 넘는 산물 화학 불변**의 또 한 사례).

## 8. 결과 IV — AIMD σ: "M 둔감·X 민감"의 수치 근거 (Table 4, Fig 3–4) ★
### Table 4 전량 — Ea + σ(300 K)
| 조성 | Ea (eV) | σ(300 K, mS/cm) |
|---|---|---|
| Li₁₀GeP₂S₁₂ (LGPS) | 0.21 ± 0.04 | 13 |
| Li₁₀SiP₂S₁₂ | 0.20 ± 0.03 | 23 |
| Li₁₀SnP₂S₁₂ | 0.24 ± 0.03 | 6 |
| Li₉P₃S₁₂ | 0.26 ± 0.09 | 4 |
| Li₁₁AlP₂S₁₂ | 0.18 ± 0.06 | 33 |
| Li₁₀GeP₂O₁₂ | **0.36 ± 0.05** | **0.03** |
| Li₁₀GeP₂Se₁₂ | 0.19 ± 0.04 | 24 |
- **"M 둔감"의 정확한 근거**: ① isovalent(Fig 3a): Ge/Si/Sn Arrhenius 선이 겹침, **"Ea와 σ(300 K)가 전 Li₁₀MP₂S₁₂에서 시뮬레이션 오차 내 동일"** — 중앙값은 23/13/6으로 4×를 갈라 보이지만, Ea ±0.03–0.04 eV가 300 K 외삽에서 ~e^(±0.04/kT)≈×4.7 오차를 만들므로 구분 불가가 맞다. ② aliovalent(Fig 3b): P/Al이 기울기 변화는 더 커 보이나 **t-통계 검정으로 Li₉P₃S₁₂·Li₁₁AlP₂S₁₂의 Ea·σ가 LGPS와 유의차 없음** → **"LGPS 부근 Li⁺ 농도에서 캐리어 농도 효과는 작다"**. Al의 소폭 우위(0.18 eV/33)는 채널크기 1.92 Å(최대)로 "부분 설명".
- **"X 민감"의 수치**: **O = Ea +0.15 eV(0.36), σ 0.03 mS/cm** — ⚠ **비율은 13/0.03 = 433× = 2.6 자릿수**다. 논문은 Results에서 "three orders of magnitude lower"(σ)라 하고 Discussion에서는 "two orders of magnitude"(D)라 해 **자기 문장끼리도 안 맞는다**(§18.2-5). 인용은 "**2–3 자릿수**" 또는 "**약 430배**"로. — "황화물≫산화물" 일반 관찰(LISICON vs thio-LISICON, refs 34–36)과 정합, 원인 = 음이온 크기·분극성 + **채널크기 20%↓**(Table 2 Voronoi/Zeo++ 분석 재인용). **Se = 개선 미미**(0.19±0.04, 24 — LGPS와 오차 내 동일) → **"임계 확산 채널크기가 존재하고, 그 이상에서는 커져도 이득 없다"**.
- σ(LGPS 300 K)=13 mS/cm ≈ Kamaya 실험 12 mS/cm — 2013년 AIMD 외삽의 대표적 성공 사례로 이후 문헌이 반복 인용.

## 9. 결과 V — 격자 스케일링 스캔 (Table 5, Fig 5): "S²⁻ 근최적"의 직접 실험 ★
LGPS를 **등방 스케일 −4~+4% 6점**으로 강제 변형해 AIMD 반복:
| Δa (%) | Ea (eV) | σ(300 K, mS/cm) |
|---|---|---|
| −4 | 0.59 | 4.6×10⁻⁸ |
| −2 | 0.47 | 4.8×10⁻⁶ |
| −1 | 0.28 | 1.7 |
| 0 | 0.23 | 13 |
| +2 | 0.19 | 44 |
| +4 | 0.17 | 75 |
- **비대칭이 결론의 전부**: 수축 −1%만으로 σ 1/10, −2% 이상이면 6자릿수 붕괴 / 팽창은 +4%를 다 줘도 ×6. Ea는 0.59→0.17 eV 단조.
- 해석: **"LGPS의 Li 확산 채널은 이미 '최적' 크기 근처 — 더 큰 음이온(Se)으로든 인공 팽창으로든 키워봐야 이득이 작다"** → 요약의 "size of S²⁻ is near optimal". Se 결과(§8)와 자기일관.
- **⚠ Table 5는 이 논문에서 통계적으로 가장 약한 표다 (2026-08-03 실물 판독으로 확정)**:
  ① **온도점이 strain당 4개뿐**(Fig 5a 마커 재계수: 1000/T ≈ 0.85 / 1.12 / 1.35 / 1.70 ≈ 1180/890/740/590 K). Fig 3·4의 LGPS는 8–9점인데 여기선 절반 이하.
  ② **Table 5에는 오차막대가 아예 없다** — Table 4는 전 행 ±0.03–0.09 eV를 붙였는데 Table 5는 Ea를 맨값으로만 준다. Fig 5b 막대에도 error bar 없음(Fig 4b는 있음).
  ③ 그 결과 **같은 물질 LGPS의 Ea가 Table 4에서 0.21±0.04, Table 5(0 %)에서 0.23** — 피팅 세트(9점 vs 4점) 차이. σ는 양쪽 13 mS/cm로 동일.
  → **인용 규율**: −4~+4 % 스캔의 *경향*(단조·비대칭)은 인용해도 되지만 **개별 Ea 값(0.28/0.47/0.59 …)을 ±없는 확정값처럼 쓰지 말 것**. 특히 +2 %/+4 %의 0.19/0.17 eV는 0 %의 0.21±0.04 오차막대 안에 완전히 들어간다 — **"팽창 쪽 이득"은 사실상 통계적으로 유의하지 않다**(저자가 Se에 대해 스스로 내린 판정과 같은 논리를 격자 스캔에도 적용하면 그렇다).

## 10. Discussion 통합 — 논증 흐름
1. **산화물 LGPS는 희망 없음(3중 사형선고)**: E_decomp>90(Li₃PO₄ 경쟁, 합성 불가) + 확산 2자릿수↓(음이온 작고 딱딱, 채널 20%↓) + **5 V 양극 접촉 시 O₂ 방출**. "Oxides are easier to handle, but little hope for an oxide version of LGPS."
2. **Se도 답 아님**: σ 이득 미미(임계 채널) + intrinsic redox 최저(gap 최소). → **S가 스위트스폿** — 격자 스캔이 기하적으로 재확인.
3. **양이온은 마음대로 바꿔라(좋은 소식)**: σ·anodic/cathodic 안정성 모두 불변. **이유 = "M–Li 상호작용이 M을 둘러싼 S²⁻에 의해 스크리닝"** — M은 Li 부격자와 전기적으로 절연되어 있다. 이것이 "M 둔감"의 물리.
4. **캐리어 농도 둔감(놀라운 소식)**: 다른 전도체(LLTO·NASICON)는 Li 농도로 σ가 자릿수 단위로 변하는데 여긴 아니다 — **"Li₁₀MP₂X₁₂는 이미 부분점유 조성이라 대부분의 Li가 mobile"** (= 포화 캐리어 체제). "그런데도 Ge 외 버전이 아직 보고 안 된 게 놀랍다" — [문맥, 논문 밖: 직후 Li₁₀SnP₂S₁₂(Bron 2013)·Si계가 실제 합성되어 예측이 실증됨.]
5. **★ 방법론적 유산 — "intrinsic redox만으로 평가하면 위험하다"**: HSE DOS(산화물 gap 최대=intrinsic 최고)와 Table 3(산화물만 O₂ 방출=실전 최악)의 **정면 충돌**을 명시하며 "전극과의 화학 호환성이 동등하거나 더 중요" — **B①(intrinsic)/B③(계면) 축 분리의 2013 원문**. 우리 4축 분리 규율·[Banik] band-edge vs phase-stability 분리·[Rich16] 전체 기획이 이 문단의 후손.

## 11. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md` ★★
### 11a. 방법 계보 판정
| 요소 | Ong 2013 | 우리 | 판정 |
|---|---|---|---|
| 상안정 | PBE hull, ICSD+치환 파생 entry, E_decomp | MP-2026 hull(GGA/GGA+U 혼합, MP2020 보정), E_hull/de_post_anneal | ✓ 같은 construction, entry·보정 세대만 상이 — "entry set 자각"은 2013부터 |
| ESW | **2-포인트**(0 V/5 V) 평형상만 + HSE gap 상한 | **전 구간 onset 스캔**(get_element_profile, [Zhu15] 직계) | **전신-후신 관계** — onset 수치 비교는 원리적으로 불가(그들 n/a). 산물 화학은 연속(황화물 0 V: Li₂S+Li₃P+합금) |
| 수송 | AIMD(진짜 DFT 힘), 단위셀 50원자·Γ·2 fs·NVT(0 K 부피)·40–400 ps·600–1200 K 외삽 | **MLIP-MD**(UMA-s-1p1) 52원자·2 fs·Langevin NVT·200 ps·600/800/1000 K 3점·MSD 2–50 ps 고정·멀티시드 | △ **힘 계산 축이 다름**("둘 다 AIMD" 금지 — 그들이 진짜 AIMD). 셀 크기·시간 스케일은 한 세대 차이인데 프로토콜 뼈대(승온→평형→생산→Arrhenius 외삽→저T 제외)는 동일 계보 |
| 무질서 | Ewald 30배열→DFT GS **단일 배열**로 전 물성 | comp1/modelc 자연 배열 + disorder_ensemble(멀티 cfg)·decorate | 우리가 [KimMTP]/[Klerk] 이후 세대 — 단일 배열의 한계는 §14 |
| σ 환산 | tracer-D, "교차상관 없으면 등가"(암묵 Haven=1), 환산식 본문 부재 | NE(Haven=1) 명시 + **절대값 인용 금지** 규율([Adeli] Haven 0.23–0.3 실측 근거) | ✓ 같은 근사의 조상 — 우리는 한계를 규율화한 점만 다름 |
| gap | HSE(수치 미제시, 순서만), "gap=창의 상한" 명시 | PBE 2.066/2.099(fixed-occ nscf), "wide-gap만 비교" 규율 | ✓ **"gap≠onset" 규율의 원문 확보** — 절대값 비교는 양쪽 다 불가(그들 수치 없음·우리 PBE) |
### 11b. 물리 대조 — 4개 축
1. **"M 둔감·X 민감" ↔ 우리 cascade 수송 축**: **정합 — 단 우리 도펀트는 그들의 'M'이 아니다.** Ong의 M은 **S²⁻로 스크리닝된 4b형 골격 양이온**(Li 망 비접촉) → 둔감이 당연. 우리 cascade에서 수송을 움직인 레버는 전부 **Li 부격자·음이온 부격자·병목을 직접 건드리는 것들** — Cl 증량(음이온 무질서·공공: D 2.6×·Ea 0.253→0.224), O@S(음이온: BVSE 채널 축소·[Wang22] σ 10×↓ 실험 줄), Nd@Li(σ300 0.52×, connectivity blocking) — 즉 **Ong의 이분법(골격 양이온=불감/음이온·Li 망=민감)이 우리 47-도펀트 결과의 상위 규칙으로 그대로 작동**한다. ⚠ 우리는 Ge/Si/Sn 골격 스왑 자체는 스캔 안 했으므로 "우리가 M-둔감을 재현했다"고는 말하지 말 것 — "우리 결과가 그 규칙과 모순되지 않고, 민감 축이 전부 비-M 축이었다"까지가 정직.
2. **캐리어 둔감(LGPS) ↔ 캐리어 민감(argyrodite)**: **구조 의존 — 이식 금지.** Ong: Li₉/Li₁₀/Li₁₁ 변화에도 σ 불변("이미 부분점유·대부분 mobile"). argyrodite는 반대로 **Li 공공이 레버**([Adeli] 48h 0.456 실측·Haven↓, 우리 modelc Li₅.₄). 조성족이 다르면 캐리어 축의 민감도가 뒤집힌다 — LGPS 결론을 argyrodite에 수평 이식하면 틀림.
3. **채널 기하(Zeo++ 자유 구·임계 채널크기) ↔ 우리 BVSE 채널%**: **직계 조상.** 그들 = Li 제거 골격의 **기하학적** 최대 통과 구(정적, 에너지 무시) + "임계 크기" 개념; 우리 = softBV **에너지** 등고(above-min ≤ iso)의 채널 부피%·migration_volume_fraction + percolation 임계([Perc]) — 같은 질문("병목이 얼마나 넓나")의 기하판→에너지판 진화. 그들 "임계 채널크기 존재, 그 이상 무이득" = 우리 "채널%가 문턱 넘으면 σ 포화" 직관의 원조.
4. **격자 수축 → σ 붕괴(Ong) ↔ Cl-rich 격자 수축 + σ↑(우리/[Adeli])**: **표면 모순, 실제는 변수 분리.** Ong의 −1%→σ÷10은 **조성 고정·등방 압축**(순수 기하 효과). 우리 comp1→modelc·[Adeli] x=0.5는 격자가 9.8598→9.8061 Å(−0.5%) 수축하지만 **조성이 함께 변해** 공공↑·무질서↑·정전 약화가 기하 손해를 압도. → **"격자상수 단독은 σ 예측자가 아니다"** — Ong 자신의 결론(채널크기, M 무관)과 [Kraft](무름 vs prefactor 상쇄)까지 합치면, 격자·강성·기하는 전부 2차 변수이고 **점유·무질서·connectivity가 1차**라는 것이 세 문헌+우리의 합류점.

## 12. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | LGPS 결정구조 **2뷰**(좌 = a축 투영 b–c면 / 우 = c축 투영 a–b면). 그려진 다면체는 **적 (Ge₀.₅P₀.₅)S₄ + 청 PS₄ 사면체 둘뿐** — 본문이 말하는 **LiS₆ 팔면체·LiS₄ 사면체는 도면에 다면체로 표시되지 않는다**(Li는 구로만). 완전점유 Li = 녹색 구 / 부분점유 Li = 녹-백 반구 | LGPS 골격 소개 표준도 — 우리 argyrodite cage 그림의 대구. ⚠ "Fig 1이 LiS₆ 팔면체를 보여준다"고 쓰면 오기 |
| 2a–c | Li₁₀GeP₂X₁₂(X=O/S/Se) HSE DOS — gap 순서 O>S>Se, 밴드엣지=음이온 | "VBM=음이온" 조성족 관찰의 원전 도판 — [Banik] Fig 3b의 조상 |
| 3a,b | Arrhenius: (a) Ge/Si/Sn 겹침 (b) Ge/P/Al — 고온점 제외 표기 | **"M 둔감" 한 장 증거** — 우리 도펀트-σ 슬라이드의 반례·대구 소재 |
| 4a,b | Arrhenius O/S/Se + Ea 막대(0.36/0.21/0.19) | **"X 민감" 한 장 증거** — O-doping σ 비용([Wang22]·[Yang25] 줄)의 계산 원조 |
| 5a,b | 격자 ±4% Arrhenius + Ea 막대(0.59→0.17) | **비대칭·S²⁻ 근최적** — 우리 채널%/migration_volume 서사의 원전 그림 문법 |
| T1–T5 | 상기 전량 표 | E_decomp·채널크기·σ 표는 조성족 비교의 소환 사전 |

## 13. Post-processing ★
- **무엇**: ① hull E_decomp(조성 고정) ② Li grand potential 2-포인트 평형상 ③ HSE DOS/gap ④ AIMD MSD→D→Arrhenius→σ(300 K) ⑤ Zeo++ 채널크기(최대 자유 구) ⑥ 격자 스케일링 가상실험 ⑦ t-검정.
- **도구**: pymatgen(Ewald 정렬·상도; 당시 "submitted"라 이 논문이 pymatgen 초기 실전 응용), VASP, Zeo++.
- **수치화·기록**: 조성당 [E_decomp, 평형조합 / 음극·양극 평형상 / Ea±err, σ(300 K)] 표준행 — 우리 cascade CSV 스키마(조성당 hull·onset·σ 프록시 행)의 원형 포맷.

## 14. 주의/한계 (over-claim 방지) — 비판적으로
- **onset 없는 ESW**: 2-포인트(0/5 V) 평형상뿐 — "이 논문이 LGPS 창 1.7–2.1 V를 계산했다"고 인용하면 **오귀속**(그건 [Zhu15]). Li 금속 불안정 최초 예측도 ref 7(Mo 2012)이 먼저.
- **단일 질서 배열의 전 물성**: Ewald-최저 계열 1개(aliovalent는 정말 1개)로 상안정·AIMD 전부 — [KimMTP]가 보인 "배열에 따라 Ea 0.15–0.53 eV" 스케일의 감도를 2013엔 볼 수 없었다. E_decomp 수십 meV/atom 차이(예: Al 60 vs 25)는 배열 선택에 흔들릴 수 있는 크기.
- **AIMD 통계의 한계**: 단위셀 50원자·Γ-only·저컷오프(280 eV)·40–400 ps·고온 외삽. Ea 오차 ±0.03–0.09 eV → **300 K σ는 ×3–10 오차** — "Si 23 > Ge 13 > Sn 6"의 중앙값 순위를 인용하면 안 되고(저자도 "오차 내 동일"), 반대로 **"오차 내 동일" 판정 자체가 큰 오차막대의 산물**이기도 하다(Sn 6 vs Al 33의 5.5×도 "not significant"). 멀티시드 없음.
- **NVT = 0 K 부피 고정**: 열팽창 무시 — 고온일수록 채널을 실제보다 좁게 시뮬레이션. 격자 스캔(§9)의 절대 Ea에도 같은 계통 오차.
- **d=3 등방 취급**: LGPS 준1D 이방성(c-축 우세)을 평균 — 방향 분해 D 없음(ref 7·Adams가 근거이긴 함).
- **용융 제외의 비대칭**: Al/P(1000–1200 K 제외)·Se(1000–1200 K 제외)는 저온 소수점 피팅 → 해당 Ea 오차가 특히 큼(P ±0.09). "Se가 S와 동일"의 통계력도 그만큼 약함.
- **σ 환산식 미기재**(본문): NE 추정이나 명시 없음(ESI 미보유로 미확인) — Haven 보정 없음은 확실.
- **HSE gap 수치 미제시**: DOS 그림뿐 — "Ong 2013의 LGPS gap"으로 3.6 eV를 쓰면 그것은 ref 7(Mo 2012) 값의 소환.
- **결론부 오타**: "Li₁₂SiP₂S₁₂ and Li₁₂SnP₂S₁₂" — Li₁₀의 인쇄 오류(요약·본문과 대조 시 자명). 소환 시 Li₁₀으로 교정해 인용.
- **Eq. (2)의 인쇄 오류**(§18.2-1): MSD가 *차의 제곱*이 아니라 *제곱의 차*로 조판돼 있다 — 그대로 옮겨 쓰지 말 것.
- **참고문헌 3건 서지 오류**(§18.2-7): ref 16(PBE→PBE0 논문), ref 27(권 162), ref 28(권 8). **이 논문을 경유한 재인용 금지** — 원전 확인 후 인용.
- **Table 5는 오차막대 없는 4점 피팅**(§18.2-2) — 격자 스캔의 개별 Ea를 확정값처럼 인용하면 안 되고, 팽창 쪽(+2/+4 %) 이득은 통계적으로 유의하지 않다.
- **채널크기=정적 기하**: 이완 정지 구조의 자유 구 — 동적 격자 요동·분극(soft-lattice, [Kraft])은 미반영. "채널크기→σ"는 O처럼 극단 차이에서만 설명력.
- 5 V 양극 = μ_Li 극단의 추상 — 실제 양극 상(NCM 등)과의 혼합 반응은 미고려(자인; [Rich16]이 채움).

## 15. 적용 인사이트 (내 연구에 어떻게)
1. **계보 문장(발표·원고용)**: "우리 cascade는 Ong 2013의 조성족 3축 스캔(hull/전기화학/AIMD)을 argyrodite host의 도펀트 축으로 옮긴 것 — [Zhu15] onset 스캔·[Rich16] 계면·[Xiao19] 깔때기를 거쳐, boolean이 아닌 가중 score와 기계·조합 축을 더했다."
2. **"M 둔감·X 민감" = 우리 도펀트 분류의 상위 규칙**: 도펀트 효과를 보고할 때 "어느 부격자를 건드리나"(골격 양이온=스크리닝/음이온·Li 망=민감)로 먼저 분류하면 Ong 2013과 한 줄로 정렬된다 — 세미나 Q&A 방어선.
3. **격자상수·채널 기하는 2차 변수**: Ong(등방 스캔)+우리/[Adeli](Cl-rich 수축+σ↑)를 한 슬라이드에 놓으면 "격자상수↔σ 상관을 단독 인용하지 말라"는 규율이 그림으로 완성된다.
4. **"intrinsic redox만 보면 위험"(§10-5)**: 우리 B축 4분리(축 명명 강제)의 2013 원문 — B① 대 B③ 분리를 문헌으로 정당화할 때 1차 인용처.
5. **★ 우리 MLIP-MD 규율("σ 절대값 인용 금지, 비율도 멀티시드 판정만")의 문헌 방패**: 이 논문의 황화물 5종 σ(300 K)는 **4 → 33 mS/cm, 8.25배 폭**인데 저자는 전부 "오차 내 동일"로 판정했다(Ea 오차 ±0.03–0.09 eV가 300 K 외삽에서 ×4.7 이상을 만들기 때문). **진짜 AIMD로도 σ 비율 8배가 유의하지 않다** — 우리가 단일시드 1.33×를 철회한 결정(SEMIFINAL 2026-07-09)이 과민한 게 아니라 **이 분야의 원전이 이미 세운 기준**임을 한 줄로 보일 수 있다. 리뷰어 방어용 1순위 인용처.
6. **서베이 §3(AIMD 관행) 기준점**: 단위셀·Γ·2 fs·NVT(0 K 부피)·40–400 ps·600–1200 K 외삽·용융 제외 = 2013 표준 명세 — 우리 MLIP-MD 프로토콜(200 ps·3점·멀티시드·MSD 창 고정)이 무엇을 개선했는지의 대조표 재료.

## 16. 인용 가능 문장 (deck/paper용)
- "Isovalent cation substitution leaves the LGPS framework's stability, electrochemical behavior and Li⁺ conductivity essentially unchanged because the M–Li interaction is screened by the surrounding S²⁻ — transport is governed by the anion/Li sublattice, which is precisely the axis our dopant screening perturbs."
- "Ong et al. (2013) established the asymmetric lattice response of LGPS (−1% lattice → 10× lower σ; +4% → only 6× higher) and concluded that S²⁻ is near-optimal — the geometric ancestor of our BVSE channel-percentage descriptor; our Cl-rich results show composition can override geometry (lattice contracts yet σ rises)."
- "The paper's own HSE-DOS-vs-grand-potential contradiction — oxides have the widest intrinsic gap yet evolve O₂ against a charged cathode — is the 2013 origin of the rule that intrinsic redox stability alone must never be used to rank electrolytes."

## 17. 기법 용어 미니사전
- **E_decomp(equilibrium decomposition energy)**: 조성 고정 시 hull 평형 조합으로 분해되는 반응에너지의 음수/원자 — E_hull과 동일 물리(안정=0).
- **2-포인트 grand potential**: μ_Li 두 극단(μ⁰, μ⁰−5 eV)에서만 열린계 평형상을 보는 축약형 — 전 구간 스캔([Zhu15])의 전신. 산물은 주고 onset은 못 준다.
- **Ewald/정전 정렬(electrostatic ordering)**: 부분점유 자리에 이상화 이온전하를 놓고 Ewald 합이 낮은 배열부터 DFT 후보로 — enumeration 시대 이전의 표준 무질서 처리(우리 lowest-Ewald 노선의 원조).
- **Zeo++ 채널크기(largest free sphere)**: 이동 이온을 제거한 골격의 Voronoi 네트워크에서 통과 가능한 최대 구 지름 — 기하학적 병목 지표(에너지 무시).
- **velocity scaling / Nosé–Hoover**: 승온(속도 재배율)과 평형·생산(확장 라그랑지언 열욕) 단계의 온도 제어 — 우리 Langevin과 다른 열욕 계열.
- **tracer(self) D vs center-of-mass D**: 개별 이온 MSD vs 무게중심 MSD — 교차상관(협동 이동) 없으면 동일 = Haven ratio 1 가정의 다른 표현.
- **t-통계 검정(여기서의 용법)**: 두 Arrhenius 피팅 기울기(Ea)의 차이가 표준오차 대비 유의한지 판정 — "aliovalent 무영향" 결론의 통계 도구.
- **HSE(screened hybrid)**: 단거리 정확 교환 혼합으로 PBE gap 과소를 보정한 functional — 이 논문에선 gap "순서" 판정용.

---

## 18. 본문 실물 독립 검증 (2026-08-03)

**방법**: `litdb/inbox/43. Phase stability…pdf`(9 pp = 148–156) 전문을 pypdf로 추출해 §1–17 전 주장과 1:1 대조 + **PyMuPDF 450–800 dpi 크롭 재판독 8매**(Fig 1 / Fig 2 패널 a·b,c / Fig 3a,b / Fig 4a,b / Fig 5a 좌·우 / Table 3 / Eq 1–2) + **Fig 2 DOS 3패널 픽셀 디지타이즈**(축 눈금 검출 → 122.75 px/eV 보정 → CBM onset 판독). digest 초판(2026-07-28)은 INDEX 기록상 **첫 페이지만 실물 대조**된 상태였음. **ESI는 여전히 미보유** — Li–M–P–X 전 안정상 목록·이완 구조 상세·σ 환산식은 이번에도 확인 불가.

### 18.1 교정 5건
| # | 위치 | 초판 | 실물 | 성격 |
|---|---|---|---|---|
| 1 | §6 | Fig 2 figure-read "O **~5** eV / S ~3.6 / Se **~2.8**" | 디지타이즈 **O 6.73 / S 3.68 / Se 2.31** | **O가 1.7 eV, Se가 0.5 eV 오독.** S 판독이 ref 7의 3.6 eV와 맞아떨어져 스케일 자체는 검증됨 → O·Se 오독이 확정 |
| 2 | §4d | "Fig 5에 1000/T=2.0(=500 K) 지점도 보임 — 본문 600–1200 K와 불일치" | 800 dpi 재판독: **2.0에 닿는 것은 피팅 직선의 외삽뿐, 마커 없음**(Fig 3·4·5 전부 동일) | **오독 — 불일치 자체가 없었다.** 온도창은 본문대로 600–1200 K |
| 3 | §5b | "V_O/V_S 0.53–0.55, 원문 '53–55% smaller'는 오기적 서술" | 방향은 맞았으나 수치 부재 → **실제 감소폭 44.9–46.9 %**, 비율 0.531/0.545/0.551 | 정밀화 + 같은 문장 내 Se 쪽("16–19% larger")은 기준이 반대라는 점 추가 |
| 4 | §8 | O의 σ "3자릿수↓" (논문 Results 표현 그대로 채택) | 13/0.03 = **433× = 2.6 자릿수**. 논문 Discussion은 같은 사실을 "**two** orders"라 서술 | **논문 자체의 내부 불일치를 초판이 검증 없이 승계**. 인용은 "2–3 자릿수/약 430배" |
| 5 | §4d·§12 | AIMD 셀 "**50원자**" 단정 / Fig 1 "LiS₆ 팔면체" | 원자수는 **논문 미기재**(우리 산술 추정) / Fig 1에 그려진 다면체는 **(Ge₀.₅P₀.₅)S₄·PS₄ 둘뿐**, LiS₆는 본문 서술일 뿐 도면에 없음 | 논문값과 우리 추정의 경계 흐림 |

### 18.2 신규 적발 9건 (논문 미서술 또는 초판 누락)
1. **Eq. (2)가 인쇄상 틀렸다** — 논문은 ⟨[r(t)]²⟩ = (1/N)Σᵢ⟨[**r**ᵢ(t+t₀)]² − [**r**ᵢ(t₀)]²⟩ 로 인쇄했다. 이건 *제곱의 차*이고, MSD의 정의는 *차의 제곱* ⟨|**r**ᵢ(t+t₀) − **r**ᵢ(t₀)|²⟩ 이다. 600 dpi 수식 이미지로 확인(추출 오류 아님). 실제 구현(pymatgen DiffusionAnalyzer 계열)은 당연히 올바른 식일 것이므로 **조판 오류**로 판단하되, **이 식을 그대로 옮겨 쓰면 안 된다**. Eq. (1) D = ⟨[r(t)]²⟩/(2dt) 는 정상.
2. **Table 5(격자 스캔)의 통계적 취약성** — strain당 **온도점 4개뿐**(Fig 5a 마커 재계수; Fig 3·4의 LGPS는 8–9점), **오차막대 전무**(Table 4는 전 행에 ±). 그 결과 LGPS Ea가 Table 4 0.21±0.04 ↔ Table 5 0.23으로 갈린다. **+2 %/+4 %의 0.19/0.17 eV는 0 %의 오차막대 안** → "팽창 쪽 이득"은 유의하지 않다. → §9
3. **Li₉P₃S₁₂의 E_decomp 22는 다형 에너지지 분해 에너지가 아니다** — 분해 조합 3Li₃PS₄가 원조성과 동일. Table 1의 나머지 10행과 같은 척도로 읽으면 안 된다. → §5a
4. **Al의 채널–안정성 trade-off** — 채널 1.92 Å(황화물 최대, Ea 최저 0.18·σ 최고 33) ↔ E_decomp 60(황화물 최악, 타 황화물의 2.4–3.2배). 논문은 두 표를 연결하지 않는다. → §5a
5. **"three orders"(Results) vs "two orders"(Discussion)** 내부 불일치. 실제 2.6 자릿수. → 18.1-4
6. **d=3 선택의 4단 문헌 논증**(Kamaya 1D 가설[6] → Mo 2012 a–b면 2경로[7] → Adams 약이방성[8] → Malik ">1D 필요"[9])이 서론에 온전히 있는데 초판이 §4d 한 줄로 압축했다. **"LGPS=1D"를 이 그룹이 이미 2012에 수정**했다는 점이 중요. → §4d
7. **참고문헌 3건의 서지 오류** — (a) **ref 16**: 본문은 "Perdew–Burke–Ernzerhof (PBE) GGA"라 쓰고 ref는 *J. Chem. Phys.* **1996, 105, 9982**를 가리키는데 이건 **PBE0 혼합비 근거 논문**이고 PBE GGA는 *PRL* 1996, 77, 3865다. (b) **ref 27**(Mercier, *J. Solid State Chem.* 1982): 권 **162**로 적혀 있으나 1982년 JSSC 권은 41–45대 — 권 번호 오류. (c) **ref 28**(Kaib, *Chem. Mater.* 2012): 권 **8**로 적혀 있으나 2012년 Chem. Mater.는 24권. **우리 원고에서 이 3개를 이 논문을 통해 재인용하면 오류가 전파된다** — 반드시 원전 확인 후 인용.
8. **Table 3의 P–S 행만 합금이 없다** — 본문의 일반화 "음극 평형상은 Li₂X + Li₃P + Li\_xM\_y **합금**"에서 Li₉P₃S₁₂(M=P)는 합금 항이 없이 Li₂S + Li₃P뿐. 유일한 예외이자, **금속성 산물이 없는 유일한 조성**(= 저자가 "metallic products가 걱정된다"고 한 문제에서 자유로운 유일한 후보)인데 논문이 짚지 않는다.
9. **EES 특유의 "Broader context" 박스**(초록 아래)가 별도로 있고, 거기서 논문의 프레이밍이 가장 선명하다: "LGPS의 두 한계(Ge 비용 / 황화물 공기·수분 민감) 중 **첫째는 Si·Sn으로 풀리고 둘째는 산화물 치환으로 안 풀린다**". 인용문 소스로 유용.

### 18.3 확인만 되고 변경 없음 (주요 항목)
- 서지: EES 2013, **6**, 148–156 · DOI 10.1039/c2ee23355j · Received **15 June 2012** / Accepted **1 Oct 2012** / Published online **2 Oct 2012** · Samsung SAIT 자금 + TeraGrid(PSC)·NERSC(DE-AC02-05CH11231) ✓ 저자·소속(MIT DMSE / Samsung SAIT Cambridge MA)·교신 gceder@mit.edu ✓
- **Table 1 전 11행**(분해 조합 + E_decomp 92/96/97/19/25/25/60/22/16/16/19) ✓ 화학량 균형 자체 검산 통과(Sn–O 행 0.33Li₈SnO₆+0.67Li₂SnO₃+2Li₃PO₄ → Li 9.98·Sn 1·O 11.99 ✓; 셀렌화물 행 Li 10·P 2·Se 12 ✓)
- **Table 2 전 11행**(a/b/c/α/β/γ/V/채널) ✓ · 채널 파생비 재계산: O는 S 대비 **19.4–22.3 % 작고**, Se는 **5.9–7.1 % 크다**(논문 "~20 %"·"~7 %" ✓) · Shannon r 126/170/184 pm 및 (r_O/r_S)³=0.40·(r_Se/r_S)³=1.26 ✓
- **Table 3 전 11행**(양극 5 V / 음극 0 V 평형상) — 이미지 판독으로 전량 대조 ✓
- **Table 4 전 7행**(Ea±/σ300) ✓ · Fig 4b 막대 판독(O 0.36 / S ≈0.21 / Se ≈0.19 + 오차막대) = Table 4 ✓
- **Table 5 전 6행**(Ea 0.59/0.47/0.28/0.23/0.19/0.17 · σ 4.6e−8/4.8e−6/1.7/13/44/75) ✓ · Fig 5b 막대 판독 일치 ✓ · 파생 검산: −1 % → 7.6배↓(논문 "an order of magnitude" ✓), −2 % → 6.4 자릿수↓(논문 "more than six orders" ✓), +4 % → 5.8배↑
- 계산 셋업 전부: VASP[10]+PAW[11] · 상안정 **PBE·spin-polarized·k밀도 ≥500/원자수** · HSE[20,21]**non-spin** · AIMD **PBE·Γ-only 1×1×1·non-spin·컷오프 산화물 400/황화물 280/셀렌화물 270 eV·Δt 2 fs·Verlet·100 K Boltzmann 초기속도 → velocity scaling 1000스텝(2 ps) 승온 → Nosé–Hoover NVT 5000스텝(10 ps) 평형 → 생산 40–400 ps·2×2×1 수렴테스트** ✓
- 무질서 처리: Ewald 이상화전하(Li +1/Ge +4/P +5/S −2)[17] → **정전 최저 30배열 DFT 이완** → 최저 정전배열은 **P4₂/mc** 유지, **DFT 바닥상태는 P1**이고 정전최저보다 **~10 meV/atom 낮음**(전 LMPX 공통) · aliovalent는 **최저 1배열만** DFT ✓
- entry set: **ICSD**[14] + Holzwarth Li\_xP\_yS\_z 컴파일[15] + O↔S↔Se 상호치환 파생 ✓ · pymatgen[18] "submitted" ✓ · Zeo++[30,31] "Li 전부 제거 후 통과 가능한 최대 자유 구" ✓(Results에선 같은 것을 "Voronoi analysis"로 부름 — Zeo++가 Voronoi 기반이라 모순 아님)
- 전기화학 2-트랙: gap = "창의 **상한**"이고 외부 기준전위 정렬 미상[19] ✓ / grand potential은 **μ⁰\_Li 와 μ⁰\_Li − 5 eV 두 점만**, 전압 = −μ_Li, "**Li 교환 경로만 보고 양극 비-Li 원소와의 반응은 미고려**" 자인 ✓ — **onset 전압 없음 확정** ✓
- 용융/결합파괴 제외: Li₁₁AlP₂S₁₂·Li₉P₃S₁₂ = 1000/1100/1200 K 제외(Al–S/P–S 파괴), Li₁₀GeP₂Se₁₂ = 1000/1100/1200 K 제외(용융) — Fig 3b·4 캡션 및 마커 배치로 확인 ✓
- 결론부 **"Li₁₂SiP₂S₁₂ / Li₁₂SnP₂S₁₂" 오타** ✓ (초록·본문·Table 4는 전부 Li₁₀) · Kamaya 실험 12 mS/cm ✓ · ref 7 = Mo/Ong/Ceder Chem. Mater. 2012, **24**, 15–17(LGPS gap 3.6 eV·Li 금속 불안정 최초 예측) ✓
- 물리 서술: "M–Li 상호작용은 M을 둘러싼 S²⁻에 스크리닝된다" ✓ / "Li₁₀MP₂X₁₂는 이미 부분점유라 대부분의 Li가 mobile → 캐리어 농도 둔감" ✓ / "Ge 외 버전이 아직 보고 안 된 게 놀랍다" ✓ / **HSE gap 순위와 Table 3 분해가 정면 충돌(산화물 gap 최대인데 O₂ 방출)하므로 intrinsic redox만으로 평가하면 위험** ✓ (§10-5 = 우리 B축 분리의 원문, 확정)
- 초판 §8의 오차 산술 재검산: e^(0.04/kT₃₀₀) = e^1.547 = **4.7배** ✓ / Sn 6 vs Al 33 = **5.5배** ✓

### 18.4 미결 3건 (ESI 확보 시에만 종결 가능)
- **σ 환산식** — 본문 어디에도 Nernst–Einstein 식·캐리어 밀도·Haven 비 언급이 없다. D → σ(300 K) 13 mS/cm 로 가는 경로가 본문만으로는 재현 불가. (Haven 보정을 **안 했다는 것**은 "tracer D를 쓴다 + 교차상관 없으면 등가[26]" 서술로 확정.)
- **Li–M–P–X 전 안정상 목록**(논문: "all stable phases … are tabulated in the ESI") — E_decomp 값의 entry-set 의존성을 우리가 재판정할 수 없다.
- **이완 구조(P1) 좌표** — "Please see the ESI for details on the relaxed structures". 무질서 배열 1개에 전 물성이 걸려 있는데(§14) 그 배열을 우리가 재현할 수 없다.
