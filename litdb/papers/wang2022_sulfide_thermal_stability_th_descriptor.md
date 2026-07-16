# Improving Thermal Stability of Sulfide Solid Electrolytes: An Intrinsic Theoretical Paradigm — Wang et al. (InfoMat 2022)

> slug `wang2022_sulfide_thermal_stability_th_descriptor` · DOI `10.1002/inf2.12316` · type `exp + 경험적 결합에너지 모델 (자체 DFT 0 — ⚠ 사용자 분류 폴더는 'DFT')` · PDF `litdb/inbox/29. InfoMat - 2022 - Wang - ….pdf` (inbox #29, 사용자 분류 `DFT`) · digested `2026-07-17` · status ✅
> **저자**: Shuo Wang / Yujing Wu / **Hong Li** / **Liquan Chen** / **Fan Wu**(교신, IOP CAS 물리연구소·Tianmu Lake Inst.) — InfoMat 2022;4(8):e12316, open access
> **⚠ 저자 구분**: 교신 **Fan Wu(吴凡, IOP CAS 물리)** ≠ [Fan26] 리뷰의 **Li-Zhen Fan(USTB)**. 단 **[Fan26] 리뷰의 ref 109 ★★★ = 바로 이 논문** (Th₀/Th′ 서술자 원전) — fan26 digest §15가 "즉시 이식" 후보로 지목했던 그 논문.

---

## 0. 이 digest를 읽는 법
이 논문은 **"황화물 SE의 '고유(intrinsic)' 열안정성을 (a) 어떻게 측정하고 (b) 어떻게 조성만으로 예측하나?"** 에 답한다. 답: (a) **밀봉 석영관 + 황(S) 석출 실시간 관찰**(부식성 황화물이 장비를 못 망가뜨리게), (b) **결합에너지 가중 스칼라 서술자 Th/Th′** — 격자 내 모든 Li–S·P–S 결합에너지 합을 원자수로 정규화한 값. 핵심 물리 한 줄: **"S 비율이 낮고 Li/P 비율이 높을수록(=결합당 에너지가 클수록) 열분해가 늦다."** 검증은 Li₇P₃S₁₁ 화학량론 조절(P₂S₃ 치환)과 Li₃PS₄ 도핑(Cu/Si/Sn/O)의 XRD·DSC·Raman.
**⚠ 방법 정체**: "theoretical paradigm"이라 부르지만 **자체 DFT/AIMD는 전혀 없음** — CRC Handbook의 **기체상 2원자 결합에너지**(Li–S 312.5 / P–S 346 kJ/mol) + 조성 백분율 산수 + Materials Project 반응엔탈피 *소환*. 서술자로서의 가치와 이 한계(§10)를 분리해서 읽을 것.

## 1. 한 줄 요약
황화물 SE의 열안정성을 **황 석출 실시간 관찰(밀봉 석영관)** 로 서열화(Li₆PS₅Cl ≫ Li₃PS₄ > Li₇P₃S₁₁)하고, **조성-가중 결합에너지 서술자 Th′**(= {[Li]%×312.5 + [P]%×346}×4 + E_doped + k)가 이 서열과 P₂S₃/도핑 개선 트렌드를 재현함을 보임 → **주기율표 전 원소 도핑 스크리닝**(최적: Zr·Mn·Fe·Cu·Si·Ni·Sn)과 **Li/P/S 삼원 열안정 상도**를 제시.

## 2. 메타
| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| S. Wang, Y. Wu, H. Li, L. Chen, **F. Wu** (IOP CAS Beijing) | InfoMat 2022, 4(8), e12316 (접수 2021-12-17 / 게재 2022-03-14) | 10.1002/inf2.12316 | Li₃PS₄ · Li₇P₃S₁₁ · **Li₆PS₅Cl(=comp1)** · LSPS-Cl(Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃) · Li₄SnS₄ · Li₇P₃S₁₁-X%P₂S₃ · Li₃PS₄-X%M(M=Cu,Si,Sn,O) | exp(황석출·XRD·DSC·Raman·EIS) + 경험적 결합에너지 서술자 Th/Th′ (자체 DFT 0) |

## 3. 핵심 물성 (수치 총정리)
| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| **열안정 서열 (황 석출, Fig 1)** | **Li₆PS₅Cl > Li₄SnS₄ > LSPS-Cl > Li₃PS₄ > Li₇P₃S₁₁** | RT–900 °C 밀봉관 | 반정량(원 크기=석출량) |
| **열안정 서열 (종합, §2.5)** | **Li₂P₂S₆ < Li₇P₃S₁₁ < Li₃PS₄ < Li₂PS₃ < Li₆PS₅Cl** | XRD+DSC+문헌 | Li₂P₂S₆/Li₂PS₃는 문헌 소환 |
| Li₇P₃S₁₁ 분해 T | **~300 °C** → Li₃PS₄ + 2Li₂PS₃ + S | XRD·황석출 | ΔH=160 kJ/mol (MP 소환) |
| Li₃PS₄ 분해 T | **~400 °C** → (2Li₃PS₄→) 2Li₂PS₃ + Li₂S + S | XRD | ΔH=286 kJ/mol (MP 소환); >700 °C 완전 분해·휘발 |
| **Li₆PS₅Cl 분해 T** | **800 °C까지 불순물 피크 0** (900 °C는 Ar 셋업 한계로 미측정) | XRD | 600 °C부터 석영관 부식(할로겐) |
| LSPS-Cl 황 석출 | 600 °C부터 | Fig 1 | LGPS 650 °C 분해 문헌과 정합 |
| Li₄SnS₄ | 700 °C부터 황색 석출(SnS₂+S 추정) | Fig 1 | Li₄SnS₄→2Li₂S+SnS₂ ΔH=31 kJ/mol (MP) |
| DSC Li₃PS₄ | 상전이 onset **250**/peak **257 °C**·**44.59 J/g**; 분해 **360–400 °C**·**38.6 J/g** | 2 °C/min, ≤450 °C | |
| DSC Li₇P₃S₁₁ | 상전이 **220**/peak **234.1 °C**·**36.3 J/g** | 〃 | |
| DSC Li₆PS₅Cl | **발열/흡열 피크 없음** (전 구간) | 〃 | |
| Li₇P₃S₁₁-X%P₂S₃ 분해 onset | X=0→30: **334→384 °C** (peak 378→412) | DSC | 결정화 onset 220→255 (peak 232→268) |
| Li₇P₃S₁₁ XRD 분해 onset | X=0: 300 °C → X=5: **400 °C** | XRD(Li₂PS₃ 32.5° 마커) | |
| Li₃PS₄-도핑 분해 T | Si/Sn/O: **400→500 °C**; Si 40 %: 600 °C까지 무분해; Cu: Li₂PS₃ 마커 부재 | XRD | Cu는 대신 Li₂S·CuS 불순물 |
| σ (Li₃PS₄ 도핑) | 저농도 Cu/Si/Sn **~1.02 mS/cm**(↑); **5 % O → 0.077 mS/cm (10×↓)** | EIS RT, 800 MPa 펠릿 | O→POS₃가 Li⁺ 끌어 Ea↑ |
| 결합에너지 (모델 입력) | **E[Li–S]=312.5 / E[P–S]=346 kJ/mol** | CRC Handbook (기체상 2원자) | Th′의 유일한 에너지 입력 |
| σ 소환값 | Li₂P₂S₆ 7.8×10⁻¹¹ / Li₂PS₃ 1.6×10⁻¹⁰ S/cm (300 K) | 문헌 | 두 상은 SE 아님(비교용) |
| Th′ 도핑 지도 (Fig 3, kJ/mol) | 무도핑 Li₃PS₄ 기준 **P=S=Li 641.75**; **Y 678.341·Sc 674.682·Zr 674.765·La 696** 최고급 / **Cl 600.337·I 598.756·F 601.797** 최저급; Si 662.740·Sn 655.086·Cu 653.283·Ni 658.839·Fe 657.580·Mn 654.469·O 644.882·B 660.963 | Eq 5 + E_doped | 할로겐 도핑=악화 예측 주의(§10) |

## 4. 이론 — Th / Th′ 서술자 (논문의 "paradigm")
- **가정**: 열분해 = 결합의 절단·재구성 → 고유 열안정성은 **국소 다면체([LiS₄]·[PS₄]·[PS₃]·[P₂S₇]·[P₂S₆])를 이루는 결합의 종류·에너지·개수**가 결정.
- **Eq 1–2 (Th, extensive)**: `Th = Σ E[Li–S] + Σ E[P–S]` — 격자 내 전 결합에너지 합. 다면체별 항으로 전개.
- **Eq 3 (Th′, 정규화)**: `Th′ = ∂Th/∂N = {N[LiS₄]E[LiS₄] + N[PS₃]E[PS₃] + N[P₂S₇]E[P₂S₇] + N[PS₄]E[PS₄] + N[P₂S₆]E[P₂S₆]}/N_Total + k` — N_Total=단위셀 원자수(정규화 인자), **k=에너지 보정 인자**(다면체 연결방식 차이: 예. γ-Li₃PS₄=동방향 정렬 vs β=지그재그; 온도 균일 전제 하에 무시).
- **Eq 4–5 (실용형, Li₃PS₄류)**: [LiS₄]·[PS₄] 모두 결합 4개 → `Th′ = {[Li]%×E[Li–S] + [P]%×E[P–S]}×4 + k = {[Li]%×312.5 + [P]%×346}×4 + k`. **도핑 시** `+E_doped` 항 추가(Fig 3 머리식).
- **입력 경로 2개**: ① 조성(원자 %)만으로 Eq 5 ② Raman으로 다면체 점유비를 실측해 Eq 3.
- **명시적 한계(저자 스스로)**: 열역학 예측만 — **kinetics(입도·열전도도·적층압력·결함) 제외**. 결함=반응 사이트, 저열전도=국소 과열, 압력=접촉 촉진.
- **선행 이론과 차별**: HSAB(Tsukasaki: Sn=soft acid → Li₄SnS₄>Li₃PS₄)는 Li₂PS₃·Li₇PS₆의 고안정을 설명 못함 → 결합 카운팅이 더 일반적이라는 주장.

## 5. 결과 — 섹션별 상세

### 5.1 새 측정법: 황 석출 실시간 관찰 (Fig 1)
- **왜 새 방법?** DSC/TG/ARC는 황화물의 부식성(H₂S) 때문에 장비 손상; 열분해 중 **단체 황 석출**(휘발·인화·폭발성; 2Li+S→Li₂S ΔH=−435 kJ/mol) 자체를 기존 기법으론 못 봄.
- **셋업**: SE를 석영관에 밀봉 → 한쪽 끝 가열, 반대쪽 냉매 유동 냉각 → 휘발한 S·분해산물이 저온부에 응축(재반응 차단) → 카메라 기록.
- **결과 (RT–900 °C)**: Li₃PS₄ 뚜렷한 석출 없음(~400 °C서 미량); Li₇P₃S₁₁ **~300 °C부터 명확 석출**·온도↑에 따라 증가; **Li₆PS₅Cl 900 °C까지 석출 0**; LSPS-Cl 600 °C부터; Li₄SnS₄ 700 °C부터(황색; SnS₂+S 혼합 추정).
- 서열: **Li₆PS₅Cl > Li₄SnS₄ > LSPS-Cl > Li₃PS₄ > Li₇P₃S₁₁**.

### 5.2 검증 ①: Li₇P₃S₁₁ 화학량론 조절 (Fig 2)
- 전략: P₂S₅ 일부를 **P₂S₃로 치환**(Li₇P₃S₁₁-X%P₂S₃, X=0,5,10,20,30) → P/S 비↑ → Eq 5의 [P]%↑ → Th′↑ 예측.
- **XRD (200–600 °C 열처리)**: 분해 마커 = Li₂PS₃ 주피크 ~32.5°. X=5만으로 분해 onset **300→400 °C**·Li₂PS₃ 피크 약화. X↑일수록 억제 강화. **부작용**: X 크면 결정상 비율↓·Li₂S 출현(과잉 결함이 격자 주기성 파괴); X=20·30은 열처리 시 고결정 Li₂PS₃ 직접 생성.
- **DSC (≤450 °C 장비한계)**: 2단 발열 모두 고온 이동 — 1단(결정화) onset 220→255 °C·peak 232→268 °C; 2단(분해→Li₃PS₄→Li₂PS₃) onset **334→384 °C**·peak 378→412 °C. → **P/S↑가 Li₇P₃S₁₁·Li₃PS₄ 둘 다 안정화** = Eq 5 실증.
- **Raman**: 380 cm⁻¹=[P₂S₆]⁴⁻ / 405=[P₂S₇]⁴⁻ / 420=[PS₄]³⁻. P₂S₃↑에 따라 [PS₄]³⁻ → [P₂S₇]⁴⁻·[P₂S₆]⁴⁻ 전환(중심 P 수 불변). [PS₄]³⁻ 안정성 < [P₂S₆]⁴⁻ → 전환 자체가 안정화 기구. Li₇P₃S₁₁ 원시료엔 [P₂S₆]⁴⁻ 피크 없음 → Li₂PS₃는 분해 산물(가정과 정합).
- **Fig 2D 종합**: XRD·DSC 분해온도(좌축)와 Th′(우축, ~600→750 스케일)가 같은 단조 증가 — 원자비 막대 S% 52→44 / P% 14→17 / Li% 33→39 (X=0→30).

### 5.3 검증 ②: Li₃PS₄ 도핑 (Fig 3·4)
- **Fig 3 = 주기율표 전 원소 Th′ 스크리닝** (`Th′={[Li]%×312.5+[P]%×346}×4+E_doped+k`, kJ/mol; 붉을수록 안정). 전이금속 + IV·V·VI 주족이 유리; 비용·독성·방사성·매장량 고려 최적 후보 = **Zr, Mn, Fe, Cu, Si, Ni, Sn**. (라레어스 La 696·Y 678 등이 수치 최고, 할로겐 F/Cl/I ~600 최저.)
- **실험 (Li₃PS₄-X%M, M=Cu/Si/Sn/O; 200–600 °C 열처리 XRD, Fig 4A)**:
  - **Cu**: Li₂PS₃ 마커 피크 전무(분해 억제) — 단 Cu가 P 자리 점유하며 **Li₂S·CuS 불순물** 생성(복잡한 원자가).
  - **Si**: 분해 400→**500 °C**; **Si 40 %면 600 °C까지 무분해** (Nazar Li₃.₂₅Si₀.₂₅P₀.₇₅S₄의 β-상 600 °C 안정화와 정합 — 그쪽 해석은 격자부피↑).
  - **Sn**: 최대 40 %(원자반경); ≥20 %서 Sn₂S₄·Li₂S 상 출현; 분해 400→500 °C.
  - **O**: S 자리 치환 → Li·P 원자 %↑ → 분해 400→**500 °C**.
- **DSC (5 % 도핑, Fig 4B)**: 300 °C 이후 분해 발열피크 전부 소멸; 곡선 평탄화 순 **Cu > Si > Sn > O** = Eq 5 예측 순서와 정합(저자 주장). Sn 저농도는 상전이 260→250 °C 강하(전도도 향상 신호).
- **EIS (Fig 4C)**: σ(Li₃PS₄) 기준 ~0.5 mS/cm대 → 저농도 Cu/Si/Sn **~1.02 mS/cm**(≈2×↑); **5 % O는 0.077 mS/cm (10×↓)**. 과잉 양이온 도핑은 다시 ↓(Li₂S·주기성 파괴). 기구: O→**POS₃** 단량체가 Li⁺ 인력↑→Ea↑→σ↓; Cu/Si/Sn은 P⁵⁺보다 큰 반경→채널 확장 + 이가(aliovalent) 치환→공공/전자 보상→σ↑.
- **🔑 트레이드오프 명시**: O 도핑 = 열안정 ↑ + σ 10×↓ (양이온 도핑은 둘 다 ↑ 가능).

### 5.4 검증 ③: LixPySz 전 계열 밀봉 가열 (Fig 5)
- **셋업 차이**: Fig 1(분리형: S를 저온부로 빼냄)과 달리 **진공밀봉 석영관을 머플로 중앙에 수평 거치**(분해산물 휘발·편석 방지, >3 h 유지) — Thio-LISICON(Li₃PS₄)/Thio-LISICON II(Li₇P₃S₁₁)/Argyrodite(Li₆PS₅Cl) 3종.
- **Li₃PS₄**: 백→흑갈(400–500 °C 급변)→800 °C 흑+백색 결정 혼합; XRD ~400 °C서 Li₂PS₃; >700 °C 완전 분해·휘발(산물 특정 불가).
- **Li₇P₃S₁₁**: ~300 °C 분해(Li₃PS₄+Li₂PS₃); 색 급변은 500–600 °C(지연 이유: 1 mol당 백색 Li₃PS₄ 1 + Li₂PS₃ 2 생성).
- **Li₆PS₅Cl**: **800 °C까지 결정구조 유지·불순물 피크 0**(회갈색 변색만); 600 °C부터 석영 부식(할로겐) → 900 °C 미측정. "ultra-high thermal stability".
- **문헌 소환 2상**: Li₂P₂S₆(꼭짓점 아닌 co-vergence 링크, 합성 ~270 °C, 화학안정성 낮음, σ 7.8e-11) / Li₂PS₃(**P–P 결합** 보유, 합성 >450 °C, 분해 >700 °C 추론, σ 1.6e-10). → 종합 서열 **Li₂P₂S₆ < Li₇P₃S₁₁ < Li₃PS₄ < Li₂PS₃ < Li₆PS₅Cl**.
- **Fig 5E**: 조성 막대(Li/P/S %) + XRD/DSC/Th′ 3지표 병렬 — Th′가 실험 서열 재현. (캡션 주의: Li₄P₂S₆·Li₂P₂S₆는 타 실험·문헌 추론; Li₆PS₅Cl·Li₄P₂S₆는 DSC 측정범위 탓에 실제로 더 안정할 것.)
- **Fig 5F**: **Li/P/S 삼원상도에 Th′ 색지도** — S↑=악화, Li·P↑=개선(P 기여가 더 가파름: E[P–S] 346 > E[Li–S] 312.5). 설계 가이드라인 제시.

### 5.5 일반화 (Fig 6, §2.6)
- "performance–structure–rule" 3층: 셀 안전경계=최약 성분(Barrel principle) → SE 열안정=구조(결정→다면체→결합) → **Th′ ∝ 결합에너지, 절편=k (근사 선형)**.
- 무기 결정질 SE 전반(산화물·황화물·할라이드·보로하이드라이드)으로 확장 가능 주장.

## 6. 실험 방법 (재현용)
- **합성**: 고에너지 볼밀(유성밀, ZrO₂ 50 ml 자·10 mm 볼; Li₂S Alfa >99.9 % + P₂S₅ Macklin 99 %) + 석영관 밀봉 **200 °C/10 h 소결**. 도핑 전구체 CuS·SiS₂·SnS₂·P₂O₅ 등. 전 과정 Ar 글러브박스(O₂·H₂O <0.1 ppm).
- **열처리**: 진공밀봉 석영관, 머플로(글러브박스 내), 목표온도 >3 h 유지 후 냉각·측정.
- **DSC**: Netzsch, 밀봉 도가니, RT–450 °C, **2 °C/min**, Ar 글러브박스 내.
- **EIS**: Zennium pro, 8 MHz–0.1 Hz, 5 mV; 100 mg 분말 → φ10 mm ~**800 MPa** 냉간압축 펠릿, SUS 대칭전극.

## 7. DFT/계산 방법 ★ (정직 버전)
- **code/functional/pseudo/k-points/ecut/supercell/DFT+U/AIMD/MLIP/무질서 처리: 전부 없음 (n/a)** — 이 논문에 제일원리 계산이 **0건**.
- "이론"의 실체: ① **CRC Handbook 기체상 2원자 결합에너지** E[Li–S] 312.5 / E[P–S] 346 kJ/mol (+도핑원소 E_doped) ② 조성 백분율 가중합 ③ 정규화(N_Total) ④ 보정항 k(무시).
- **Materials Project 소환 3건**(반응엔탈피): Li₄SnS₄→2Li₂S+SnS₂ **+31**; 2Li₃PS₄→2Li₂PS₃+Li₂S+S **+286**; Li₇P₃S₁₁→Li₃PS₄+2Li₂PS₃+S **+160 kJ/mol** — MP hull(=DFT) 값을 인용만 함.
- **⚠ 사용자 분류 'DFT' 폴더이지만 계산논문 아님** — 우리 입장에선 "서술자(descriptor) 논문 + 열분해 실험 anchor"로 취급.

## 8. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1A | 황 석출 분리 셋업(가열단+냉각단 밀봉 석영관) 도식 | 황화물 열분해 관찰의 장비-부식 우회 아이디어 |
| 1B | 5종 SE 황 석출 in-situ 사진 + 온도별 원 크기 도표 | **Li₆PS₅Cl(=comp1) 무석출 900 °C** — comp1 열안정 실험 anchor |
| 2A | Li₇P₃S₁₁-X%P₂S₃ XRD (200–600 °C; 28–34° 확대) | Li₂PS₃ 32.5° = 열분해 마커 피크 관례 |
| 2B | DSC 2단 발열의 X-의존 고온 이동 | onset/peak 수치(§5.2) |
| 2C | Raman 다면체 지문 (380/405/420 cm⁻¹) | **[P₂S₆]/[P₂S₇]/[PS₄] Raman 배정표** — 우리 (유리)상 분석 시 재사용 |
| 2D | XRD·DSC·Th′ 3지표 vs X 종합 | 서술자-실험 정합 제시 양식(우리 cascade 그림에 차용 가능) |
| 3 | **주기율표 Th′ 도핑 지도** (Li₃PS₄ 기준, kJ/mol 명기) | 우리 47-dopant cascade와 *다른 축*(열)의 전 원소 스크리닝 선례; [Fan26] Fig 5e의 원본 |
| 4A | Li₃PS₄-X%M(Cu/Si/Sn/O) XRD 온도 시리즈 | O 도핑: 분해 400→500 °C (우리 O-doping 서사의 열 축 근거) |
| 4B | 도핑 5 % DSC (피크 소멸; Cu>Si>Sn>O) | |
| 4C | Nyquist + σ vs 도핑량 | **O 5 % → σ 0.077 mS/cm(10×↓)** — O 도핑 σ-비용 정량 |
| 5A–D | 밀봉관 가열 사진·XRD 온도열·DSC 3종 비교 | Li₆PS₅Cl 800 °C 무분해 XRD; DSC J/g 수치 |
| 5E | 조성막대+XRD/DSC/Th′ 병렬 | [Fan26] Fig 5d 계열의 원본 데이터 |
| 5F | **Li/P/S 삼원 Th′ 상도** | 조성→열안정 지도 발상; 우리 조성군 배치 가능 |
| 6 | performance–structure–rule 도식 (Th′–결합에너지 선형, 절편 k) | deck용 "intrinsic thermal stability" 개념도 |

## 9. Post-processing ★
- **XRD 마커-피크 판독**: 분해 여부를 산물(Li₂PS₃ ~32.5°) 주피크 출현으로 이진 판정 — 온도 시리즈로 onset 온도화.
- **DSC 정량**: onset/peak 온도(°C) + 적분 발열량(J/g)을 상전이/분해 2단으로 분리 기록.
- **Raman 다면체 점유**: 380/405/420 cm⁻¹ 피크 강도로 [P₂S₆]⁴⁻/[P₂S₇]⁴⁻/[PS₄]³⁻ 비율 추적 → Eq 3의 N_i 입력용(정량 피팅은 안 함, 정성).
- **Th′ 산출·플롯**: Eq 5 산수 → (i) X-시리즈 꺾은선(Fig 2D·5E, 실험지표와 병렬) (ii) 주기율표 히트맵(Fig 3) (iii) 삼원상도 색지도(Fig 5F).
- 도구 언급 없음(pymatgen 등 n/a) — 전부 스프레드시트 수준 산수.

## 10. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md`
| 항목 | 이 논문 | 우리 | 차이/이유 |
|---|---|---|---|
| **comp1(Li₆PS₅Cl) 열안정** | **800 °C까지 XRD 무변화·DSC 무피크·황석출 0** (실측) | 열안정 계산 축 **없음** (0 K hull·ESW·elastic·AIMD만) | 우리 공백 — [Fan26] §7 "✗ 공백(H-리스트)"과 동일 판정. 이 논문이 comp1의 **고유 열안정 실험 anchor** |
| 분해산물 화학 | Li₇P₃S₁₁→Li₃PS₄+2Li₂PS₃+S; 2Li₃PS₄→2Li₂PS₃+Li₂S+S (XRD+MP ΔH) | 우리 grand-potential 산화분해(전압축)는 Li₃PS₄·S·LiCl 계열 — **열축(T) 분해와 다른 변수** | 산물 family(폴리음이온 축합+S 방출)는 닮았지만 구동력이 V vs T — 등치 금지 |
| 서술자 철학 | 조성-가중 **결합에너지 스칼라**(Th′) | 우리 site-PDOS ⟨3p⟩·ICOHP(결합별 −pCOHP 적분) | **ICOHP가 Th′의 엄밀판**: 그들 Handbook 2원자 BDE ↔ 우리 격자 내 실제 결합(P–S −5.94/−6.0, P–O −8.43, Li–Cl −1.86/−2.10). Th′를 우리 ICOHP 가중으로 재구성하면 방법 업그레이드 가능 |
| O 도핑 효과 | 열안정↑(400→500 °C) + **σ 10×↓**(0.077 mS/cm; POS₃가 Li⁺ 속박) | O@PS₄ site-preference −0.67 eV/O·ICOHP P–O −5.98 대비 +41 %·LPSOCl gap 2.2309 eV(fixed-occ) | **정합(기전 상보)**: 그들 "POS₃ 강결합"=우리 P–O ICOHP 정량과 같은 방향. σ-비용도 [Yang25] La+O 0.65×와 한 줄(단 5 % O in Li₃PS₄ vs 우리 argyrodite 조성 — 수치 이식 금지) |
| 도핑 스크리닝 | 주기율표 Th′(열축; 최적 Zr·Mn·Fe·Cu·Si·Ni·Sn) | 47-dopant cascade(산화 onset·SEI gap·σ·blocking — 열축 없음) | **직교 축**: 우리 cascade에 Th′ 열축 열(column) 추가 가능(입력=조성 %뿐이라 비용 ~0) |
| Th′를 우리 조성에 적용(※우리 산수, 논문 수치 아님) | Eq 5 그대로: comp1 {0.4615×312.5+0.0769×346}×4 ≈ **683** vs modelc {0.4355×312.5+0.0806×346}×4 ≈ **656 kJ/mol** | — | **Th′는 Cl-rich(modelc)를 더 불안정으로 예측** — [Zuo] DSC/TGA(Cl1.5 융점↓·TGA 315 °C)·[Wu] calendar 90 °C(Cl-rich 열세)와 방향 일치. 단 Eq 5는 **Li–Cl 결합 항이 아예 없음**(Cl=S% 희석재 취급) → 방향만 취하고 정량 인용 금지 |
| band gap | n/a (전자구조 없음) | comp1 2.066/modelc 2.099 eV (fixed-occ nscf) | 비교 대상 없음 |
| 이온전도 σ | Li₃PS₄계 실측(≤1.02 mS/cm) | 우리 σ는 MLIP-MD 비율만(절대값 인용 금지 규율) | 조성 다름 — anchor로도 안 씀 |

## 11. 적용 인사이트 (내 연구에 어떻게)
1. **열안정 축을 공짜로 연다**: Th′(Eq 5)는 입력이 조성 %와 결합에너지뿐 → **comp1/modelc/B₂O₃/O-doped/Nd 조성군에 즉시 계산 가능** — [Fan26] digest가 "즉시 이식(★★★ ref 109)"으로 지목한 그 도구의 원전 확보. 업그레이드 경로: Handbook BDE 대신 **우리 LOBSTER ICOHP**(격자 내 실제 결합세기)로 가중치를 교체한 "Th′-ICOHP" — 방법상 그들보다 엄밀해지고 Li–Cl(−1.86/−2.10)·P–O(−8.43) 항도 자연 포함.
2. **comp1 열안정 실험 anchor**: "Li₆PS₅Cl은 800 °C까지 XRD 무변화·DSC 무피크·황석출 0(Wang, InfoMat 2022)" — deck의 안전성 슬라이드에 소환값으로 쓸 수 있는 가장 직접적인 문장. 단 Cl-rich(1.5/1.6)는 이 논문이 안 다룸 → Cl-rich 열안정은 [Zuo] DSC/TGA·[Wu] calendar 소환으로 보완(방향: Cl-rich 열세).
3. **O 도핑의 축별 장부 정리**: 열안정 +100 °C(이 논문) / σ 10×↓(이 논문) / 대기안정 ↑([Yang25]·[Bai] HSAB) / 산화 onset 소폭 이동 가능(우리 B₂O₃ +0.18 V) — "O는 σ를 내주고 안정성 3축(열·대기·계면)을 사는 도펀트"라는 다축 서사가 문헌 3개+우리 계산으로 닫힘.
4. **분해 마커 관례 차용**: 열처리 XRD에서 Li₂PS₃(32.5°) 마커-피크 이진판정 + Raman 380/405/420 cm⁻¹ 다면체 배정 — 향후 우리(또는 랩) 열처리 시료 판독 프로토콜로 그대로 사용 가능.

## 12. 인용 가능 문장 (deck/paper용)
- "Sealed-tube decomposition experiments show argyrodite Li₆PS₅Cl retains its crystal structure up to 800 °C with no sulfur evolution, the highest intrinsic thermal stability among Li–P–S electrolytes (Wang et al., InfoMat 2022)."
- "A composition-weighted bond-energy descriptor (Th′) reproduces the experimental thermal-stability ranking Li₂P₂S₆ < Li₇P₃S₁₁ < Li₃PS₄ < Li₂PS₃ < Li₆PS₅Cl — lower S fraction and higher Li/P fraction mean later decomposition."
- "Oxygen doping of Li₃PS₄ raises the decomposition temperature from 400 to 500 °C but costs an order of magnitude in ionic conductivity (0.077 mS/cm) — thermal stability and transport trade off through the same P–O(S) bonding."

## 13. 주의/한계 (over-claim 방지) — 비판적으로
- **"이론"의 실체는 결합 카운팅 산수**: 기체상 2원자 BDE(Li–S 312.5/P–S 346)를 이온-공유 혼성 격자에 그대로 이식 — Madelung/배위수/격자 이완 전부 무시. Eq 5는 사실상 **S%의 단조 감소 함수**(Li와 P 가중치 차 ~10 %뿐) → "S 적을수록 안정"이라는 자명한 상관을 재포장한 측면. 서열(순위)용으로만, 에너지 절대값 인용 금지.
- **k(보정항) = 미정 fudge factor**: 다형(α/β/γ) 구분·다면체 연결방식이 전부 k에 흡수·무시됨 — 같은 조성 다형의 열안정 차이는 이 모델이 원리적으로 못 가름.
- **할로겐 처리 불능**: Eq 5에 Li–Cl 항 없음 — Fig 3에서 Cl 도핑 Th′=600.3(최저급 "악화")인데 실험 최고 안정은 **Cl 함유 Li₆PS₅Cl**. Li₆PS₅Cl의 고안정을 모델은 Li%(46 %)로만 설명 — **Cl의 역할이 서술자 사각지대**. Cl-rich(우리 modelc) 예측에 쓸 때 이 편향 필수 명시.
- **검증의 순환성 부분 존재**: 도핑 실험 4종(Cu/Si/Sn/O)은 전부 "개선" 방향 — Th′가 악화를 예측한 원소(예. Zn 628·F 601)를 도핑해 *악화를 실증*한 대조군이 없음. DSC "곡선 평탄화 순 Cu>Si>Sn>O"도 반정량.
- **kinetics 부재(저자 인정)**: 실측 분해 T는 승온속도(2 °C/min)·입도·밀봉압 의존 — 열역학 서술자와 onset 온도의 직접 대응은 근사.
- **명명 혼선**: "Li₂PS₃"(P–P 결합, 합성 >450 °C; ref 54는 **Li₄P₂S₆** NMR 결정학) — 조성상 Li₂PS₃≡Li₄P₂S₆인데 Fig 5E에는 Li₄P₂S₆와 Li₂PS₃가 별도 항목처럼 병기, Li₂P₂S₆와의 구분도 문헌 소환 의존. 상 이름 인용 시 원문헌(Dietrich 2016/2017) 재확인 필요.
- **황 석출 서열은 반정량**(사진 원 크기): Fig 1 서열에서 Li₄SnS₄>Li₃PS₄인데 본문은 "Li₃PS₄·Li₆PS₅Cl이 최고 안정"이라고도 서술 — 내부 서열이 관찰량(석출 vs XRD)에 따라 미세하게 흔들림.
- **[Fan26] 연결 주의**: fan26 리뷰의 "결정질 황화물 400–500 °C 유지"는 블랭킷 서술 — 이 원전에선 **Li₇P₃S₁₁이 300 °C**부터 분해(조성 의존). 리뷰 표기 "Th₀"는 리뷰 자체 표기이고 원논문 기호는 **Th(extensive)·Th′(정규화)**.
- **MP ΔH는 소환값** — 우리 hull 수치와 섞지 말 것(방법·보정 미상). σ 절대값(1.02/0.077 mS/cm)도 Li₃PS₄ 볼밀 시료 기준 — argyrodite에 이식 금지.

## 14. 기법 용어 미니사전
- **Th / Th′**: 격자 내 전 결합에너지 합(extensive) / 그것을 총 원자수로 나눈 정규화 서술자(+보정 k). 클수록 열분해에 강하다고 가정.
- **에너지 보정 인자 k**: 다면체 연결방식(꼭짓점/모서리 공유, 정렬 방향) 차이의 에너지를 흡수하는 절편 — 본 논문에선 무시.
- **황 석출(sulfur precipitation) 관찰**: 밀봉 석영관 한쪽 가열·한쪽 냉각으로 분해 황을 저온부에 응축시켜 육안/카메라 정량하는 이 논문 고유 기법.
- **DSC onset/peak**: 발열 시작/최대 온도; 여기선 1단=결정화, 2단=분해.
- **Raman 다면체 지문**: [P₂S₆]⁴⁻ 380 / [P₂S₇]⁴⁻ 405 / [PS₄]³⁻ 420 cm⁻¹ — 티오포스페이트 축합도 판별.
- **HSAB**: hard-soft acid-base — soft acid(Sn 등)가 soft base(S²⁻)와 강결합한다는 정성 규칙; 이 논문이 넘어서려는 선행 프레임.
- **Barrel principle(리비히 최소량 법칙 판)**: 셀 안전경계=가장 불안정한 성분이 결정.
