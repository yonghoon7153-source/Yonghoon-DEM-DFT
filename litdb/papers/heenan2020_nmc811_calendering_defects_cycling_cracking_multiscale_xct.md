<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 꼴 = wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md (이 논문을 [17] 로 인용). 후보 표 N-20 · 정독 63. -->
# 상용 NMC811 양극 시트는 **사이클 전에 이미 입자 약 ⅓ 이 결함** (Material 1 30.2 % · 상용 LG MJ1 34.2 % · 분리막 (= 캘린더 롤) 쪽 > 50 %) — 저자 해석 = 원분말이 아니라 시트 인쇄 · 캘린더링 유래 (압력 미상) · 흑연 상대 4.5 V 5 사이클 뒤 2차입자 안 1차입자 사이 공극 13.5 → 19.6 % [판독 · 서로 다른 입자 한 개씩] · 1차입자 분리 ≈1 µm → 600 nm · Mn 이동 · 결정 무질서는 균열 정도와 무관 — 다중 분해능 X 선 CT (나노 126 · 32 nm · 마이크로 1.6 · 0.2 µm) + 싱크로트론 XRD/XRF — Heenan · Wade · Tan · Parker · Matras · Leach · Robinson · Llewellyn · Dimitrijevic · Jervis · Quinn · Brett · Shearing (*Adv. Energy Mater.* 10, 2002655 (2020))

> slug `heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct` · DOI `10.1002/aenm.202002655` · type `exp (multi-resolution lab X-ray CT of calendered commercial NMC811 sheets — nano-CT Zeiss Xradia 810 Ultra (Cr-Ka 5.4 keV) 126 nm and 32 nm voxels + micro-CT Zeiss Xradia 520 Versa 1.6 um and 0.2 um voxels — plus synchrotron nanoprobe XRD/XRF (Diamond I14, 19 keV, ~50 nm beam); liquid-electrolyte coin cells vs graphite, 5 cycles to 4.2-4.5 V; no modelling)` · PDF `bff6b9b1-20._Identifying_the_origins_of_microstructural_defects_such_as_cracking_within_Ni_rich_NMC811_cathode_particles_for_lithium_ion_batteries.pdf` (13 pp) + SI `623d3067-20._Sup_Identifying_the_origins_of_microstructural_defects_such_as_cracking_within_Ni_rich_NMC811_cathode_particles_for_lithium_ion_batteries.pdf` (8 pp) · digested `2026-11-12` · status ✅

> elements: Li, Ni, Mn, Co, O

> **읽은 범위**: 본문 13 쪽 전부 (텍스트 층 + 쪽 그림 래스터) · 참고문헌 34 편 전수 · **SI 8 쪽 전부** (1 쪽 = 표지 · 2 쪽 = 제목 · 3–8 쪽 = 그림 S1–S8 · **SI 에 표 · 본문 글 없음**).
> 그림 · 표 16 장 전부 크롭해 열어 봄 (§5.1) · 그림은 전부 300 dpi **래스터**라 그림 값은 픽셀 판독이다 → `litdb/figures/heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct/digitized.csv` (50 행).
> **라벨 규약**: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 (쪽 = PDF 쪽 = 인쇄 "(n of 13)") · [SI] = SI (SI 인쇄 쪽 = PDF 쪽 − 1 — 이 카드는 **PDF 쪽**으로 적는다) · [판독] = 그림 픽셀 판독 (방법 · 분해능 §3.7) ·
> [눈대중] = 눈금 사이를 눈으로 읽은 값 · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · §15) · [카드 해석] · [2차 인용] = 이 논문이 남의 값을 전한 것 (원문 미확인) · [미확인] = 본문 · SI 전수에 없음.
> ⚠ **이 논문에는 번호 붙은 식이 없다** (본문 · SI 전수). 정의식은 그림 6c 안의 r_I 하나뿐 (`eq_00a`).

---

## 0. ★ 고른 의도 대조 (후보 표 N-20 · 정독 63) — 결론 먼저

**고른 의도 (후보 표 '왜' 칸 그대로)**: *"조건 R7 (출발 상태) · l — Wheatcroft 가 "초기 사이클 입계 균열 · 캘린더링 중 전위 활주" 의 근거로 인용 (p.1 · p.6) → 압축 (캘린더링) 중 AM 의 전위 활주 = AM 소성 여부 · 출발 결함 ("무손상" 가정) 을 1 차 자료로 대조 · stallard2022 은 NMC811 2 차입자 기공 0.14 → 0.19 (5 사이클) 를 이 논문 값으로 적음 (L92)"* — 가리킨 카드 = `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` (L199) · `stallard2022_cathode_mechanical_properties_review` (L248 · L92).

| 의도의 문장 | 원문이 채우나 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| ① Wheatcroft 가 **"초기 사이클 입계 균열"** 의 근거로 인용 | **채움** (n 작음) | 결론 p.12: *"secondary particles crack predominantly at the boundaries between primary particles and are thought to be dominated by electrochemical expansion and contraction during de/lithiation"* · Fig. 7b: 4.5 V (흑연 상대) **5 사이클** 뒤 표면에서 통로 **최대 8 µm** (사이클 전 ≈2 µm · p.9) · 1차입자 사이 공극 13.5 → 19.6 % [판독 Fig. 7d] · 측정 가능 1차입자 평균 지름 **≈1 µm → 600 nm** (p.9 인쇄) — 조건: 액체 LiPF₆ EC:EMC 코인셀 · 25 °C · 0.5C 충전 / 1C 방전 · 3.0 V 에서 분해 뒤 나노 CT **32 nm** 복셀 · **2차입자 한 개씩 (n = 1 + 1)** |
| ② Wheatcroft 가 **"캘린더링 중 전위 활주"** 의 근거로 인용 | **없음** | 논문 전체에 'dislocation' 은 **한 번** (p.2): *"…the Ni–Li anti-site defects formed during operation may be a precursor for inter-granular cracking within NMC811,[19] and because each primary particle is expected to be a single crystal, or grain, this is also often described as the dislocation of primary particles, that is, the cracking and separation of primary particles."* — 여기서 dislocation = **1차입자의 어긋남 · 분리 (균열)** 이지 결정 전위가 아니고, 그것도 **운전 중** (Ni–Li 반자리 결함 [19]) 의 이야기다. slip · glide · 전위 이동 · NMC 소성 · '캘린더링 중' 전위 서술 **0 건** → 카드 문제 (L199 · §11-C) |
| ③ 압축 (캘린더링) 중 **AM 의 전위 활주 = AM 소성 여부** | **없음** | 이 논문의 '소성' 문장은 **알루미늄 집전체** 하나뿐 (p.4): *"several particles have been pressed into the current collector, suggesting that (at least locally) the calendaring pressure was high enough to exceed the yield point of Al and plastically deform the dense metal current collector sheet."* — AM 은 균열 (취성) 범주 (Table 1) 로만 기술된다. AM 소성의 1차 자료가 필요하면 정본의 다른 카드 (`stallard2022_nmc811_single_crystal_shear_strength_lithiation` 슬립 띠 · `wheatcroft2023_…` 팁 밑 1차입자 소성) |
| ④ **출발 결함 ("무손상" 가정)** 을 1 차 자료로 대조 | **채움** (압력 미상) | Table 1 (p.3 인쇄): 운전 전 (pristine · 캘린더링된 시트) **결함 없음 69.8 % (Material 1) · 65.8 % (상용)** → 결함 30.2 · 34.2 % [카드 산술] · 범주: 내부 공극 3.2 · 0.2 · 미세균열 7.6 · 9.2 · 두 쪽 (bisect) 6.3 · 7.0 · 여러 쪽 (multi-prong) 5.4 · 8.2 · prong & shatter 3.5 · 2.5 · 산산조각 (shatter) 3.2 · 7.0 % · 깊이: 분리막 쪽 > 50 % (p.4 인쇄 · Fig. 1c 판독 마지막 두 칸 56.6 · 64.7 %) · 원분말: *"minimal particle cracking"* [18] ([2차 인용] p.2) · 사이클 전 입자도 **완전 치밀 아님** — 1차입자 사이 공극 **13.5 %** [판독 Fig. 7d] · 통로 ≈2 µm · 기공 ≈500–900 nm (p.9) — 조건: 나노 CT **126 nm** 복셀 · 입자 **158 / 401** 개 · 캘린더링 변수 **저자도 모름** (p.4) · 액체계 시트 (결합제 · 탄소 · SE 없음) |
| ⑤ stallard2022 이 적은 **NMC811 2차입자 기공 0.14 → 0.19 (5 사이클)** | **일부** | 숫자는 **본문에 없고 그림에만** (Fig. 7c · 7d) — Fig. 7d 막대 [판독] **13.5 % (Raw) → 19.6 % (4.5 V)** (오차 막대 = 입자 안 깊이별 최소 · 최대 13.1–14.7 · 17.9–22.9 %) ≈ 0.14 → **0.20** · 리뷰의 0.19 는 판독보다 0.6 %p 낮다 (판독 분해능 0.07 %p) · 정의 = **2차입자 한 개 안의 1차입자 사이 공극** (32 nm 복셀 · 비국소 평균 필터 + 'bright' top-hat 분할) · **서로 다른 두 입자** (*"These are different particles"* p.9 · 하나는 사이클 없음 · 하나는 4.5 V 5 사이클 → 3.0 V) — 리뷰 문장의 "a … secondary particle increased" 처럼 **한 입자가 늘어난 값이 아니다** · 저자 경고: 나노입자가 공극처럼 보여 공극 분율이 **인위적으로 커질 수 있다** (p.11) · 대표성은 수십–수백 입자가 필요 (p.10) |
| (덧) 가리킨 둘 밖의 2차 인용 — `stallard2022_nmc811_single_crystal_…` L337 *"캘린더링 → 다결정 NMC 파쇄 · 미분화 (CT) — 압밀 압력 ↔ AM 파괴 (R7)"* | **일부** | 캘린더링 유래 파쇄 · 산산조각 (shatter = *"fragments (the size of primary particles)"*) 3.2 · 7.0 % ✓ · 압력 ↔ 파괴 관계는 **질문으로만** (*"is a certain critical calendaring pressure or electrode loading required in order to deteriorate a micro-crack into a shattered particle?"* p.4) — 압력 숫자 0 개 |

**가리킨 카드의 2차 인용 대조**:
- `wheatcroft2023_…` L199 *"초기 사이클 입계 균열 · 캘린더링 중 전위 활주 | p. 1, p. 6 | [17] T. M. M. Heenan … P. R. Shearing, Adv. Energy Mater. 2020, 10, 2002655."* — 서지 ✓ (원문과 같다) · 앞 절반 (초기 사이클 입계 균열) ✓ · **뒤 절반 (캘린더링 중 전위 활주) ✗** — 원문에 없다 (위 ②). Wheatcroft 원문의 그 문장은 이 트리에 PDF 가 없어 보지 못했다 [미확인] — 오역 ('dislocation' = 분리 → '전위') 이 Wheatcroft 원문인지 카드 요약인지 가르지 못한다. **그 카드는 고치지 않는다 → 카드 문제 1.**
- `stallard2022_cathode_…` L248 서지 ✓ (Heenan, T.M.M., Wade, A., Tan, C., Parker, J.E., Matras, D., Leach, A.S., Robinson, J.B., Llewellyn, A., Dimitrijevic, A., Jervis, R., et al. (2020) … *Adv. Energy Mater.* 10, 2002655 — 원문 저자 13 명 중 앞 10 명 + et al. = Quinn · Brett · Shearing) · L92 값 0.14 → 0.19 = 리뷰 문장 그대로 옮긴 것 (카드 잘못 아님) · 원문 그림과 대체로 같다 (위 ⑤) — **한정어 셋 (서로 다른 두 입자 · 그림 판독 값 · 32 nm 해상도 · 나노입자 경고) 이 빠짐** → 카드 문제 2 (경미 · 그 카드의 L284 · L376 · L459 도 같은 값을 쓴다).

**한 줄 판정** — 의도 다섯 가운데 **출발 결함 (④) 과 초기 사이클 입계 균열 (①) 은 채운다**: 캘린더링된 상용 NMC811 시트에서 **운전 전 입자의 ≈30 % 가 이미 결함** (126 nm 복셀로 보이는 균열 · 내부 공극) 이고, 사이클 전 2차입자 자체도 1차입자 사이 공극 ≈13.5 % 의 **다공체**다.
**AM 의 전위 활주 · 소성 (②③) 은 원문에 없다** — 'dislocation' 은 1차입자 분리의 다른 이름으로 한 번 쓰였고, 소성은 알루미늄 집전체에만 말했다. **0.14 → 0.19 (⑤) 는 숫자는 그림과 대체로 맞지만 '한 입자가 늘었다' 가 아니라 '서로 다른 두 입자 비교'** 다.
⇒ 우리 DEM 의 'AM t = 0 무손상' 가정은 **분말에서는 [18] 의 2차 인용으로 지지**, **압밀 뒤에는 이 논문이 반박** (압밀 · 캘린더링이 AM 의 ⅓ 을 깨뜨린다 — 우리 Auerbach 분류가 **만들어 내야 할 결과**이지 출발 조건이 아니다). 절대값 전이는 **안 된다** (액체계 롤 캘린더링 · 압력 미상 · SE 없음 · 126 nm 해상도) — 방향 · 깊이 분포 · 범주 비율만 '결과 전 대조 항목' 으로 쓴다 (§7.4 · §8).

---

## 1. 한 줄 요약

UCL Electrochemical Innovation Lab · Faraday Institution · Diamond 그룹이 **NEI 제 NMC811 양극 시트 (Material 1 · ≈30–40 µm · ≈2 mAh/cm²)** 와 **LG Chem INR18650 MJ1 셀의 양극 (Material 2 = '상용 비교' · ≈70 µm [그림 S3 축])** 을 X 선 CT 로 **전극 → 2차입자 → 1차입자 → 결정** 순서로 내려가며 본다.
① 운전 전 (캘린더링된 시트) 나노 CT (126 nm) 로 입자를 7 범주로 세어 **결함 30.2 · 34.2 %** · 분리막 쪽 (캘린더 롤과 닿은 면으로 추정) 에서 > 50 % → *"approximately one-third of particles being defective before operation"* (p.11).
② 흑연 상대 **4.2–4.5 V 상한 5 사이클** 뒤 전극 수준 (1.57 µm) 에서 고전압 시료의 박리 (시료 준비 탓으로 돌림) · 입자 수준 (≈0.2 µm) 에서 고전압 입자의 속 회색값 하락 → **저해상 회색값 분산이 결함 입자의 대리 지표** (200 → 1200 nm 로 묶어도 구분됨 · Fig. 2d).
③ 4.5 V 전극에서 꺼낸 2차입자 7 개를 나노 CT + 싱크로트론 XRD/XRF (Diamond I14 · 19 keV · ≈50 nm 빔) 로 → 평균 Ni:Mn:Co ≈83 : 7 : 9 · 입자 사이 · 입자 안 **Mn 변동 큼** (균열 양옆 4 → 6 %) · Mn ↔ c 격자상수 (R² 0.9) · r_I (R² 1.0) 상관 · 그러나 **균열 정도와는 상관 없음** (0.5C · 1–5 사이클).
④ 32 nm 나노 CT 로 같은 크기 (≈16–18 µm) 2차입자 두 개 (사이클 없음 ↔ 4.5 V 5 사이클) → 사이클 뒤 공극 13.5 → 19.6 % [판독] · 중심 쪽으로 증가 (균열이 중심으로 모임) · 1차입자 ≈1 µm → 600 nm (붙어 있던 1차입자의 분리).
⇒ 결론: 2차입자 균열은 **제조 (캘린더링) + 전기화학 팽창/수축에 의한 1차입자 분리** 가 지배하고 (무작위 결정 방위가 악화), Mn 화학은 결정 열화와 엮이지만 초기 균열과는 엮이지 않는다. **역학 시험 · 압력 · 모델 계산 없음.**

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Thomas M. M. Heenan** · Aaron Wade · Chun Tan · Julia E. Parker · Dorota Matras · Andrew S. Leach · James B. Robinson · Alice Llewellyn · Alexander Dimitrijevic · Rhodri Jervis · Paul D. Quinn · Dan J. L. Brett · **Paul R. Shearing\*** (교신 · p.shearing@ucl.ac.uk) — 13 명 (p.1) |
| 소속 | Electrochemical Innovation Lab, Dept. of Chemical Engineering, **UCL** (London) · **The Faraday Institution** (Harwell) · **Diamond Light Source** (Harwell; Parker · Matras · Quinn) (p.1) |
| 저널 | ***Adv. Energy Mater.* 2020, 10, 2002655** (Full Paper · 13 쪽 · 꼬리말 "(n of 13)") · 호 **47** 은 쪽 오른쪽 여백의 Wiley 다운로드 도장 *"16146840, 2020, 47, Downloaded from …"* 에서만 읽힌다 |
| DOI | `10.1002/aenm.202002655` (SI 표지도 같은 DOI · SI p.1) |
| 이력 | 접수 2020-08-17 · 수정 2020-10-01 · 온라인 2020-11-03 (p.12) |
| 라이선스 | Open access **CC BY** (p.1) |
| 자금 | Faraday Institution (EP/S003053/1 · FIRG001 · FIRG003) · EPSRC EP/M014045/1 · Diamond I14 빔타임 sp20841 · mg23858 · Royal Academy of Engineering (CiET1718\59) (p.12) |
| 데이터 | Material 2 의 영상 · 자료 = 공개 저장소 ([32] *Data Brief* 2020, 32, 106033 · p.12) · Material 1 자료 공개 여부 [미확인] |
| 이해상충 | 없음 (p.12) |
| 키워드 | batteries · cathodes · degradation · electric vehicles · microstructure · NMC811 · particle cracking (p.12) |
| 소재 | **NMC811 (LiNi₀.₈Mn₀.₁Co₀.₁O₂)** — Material 1 = **전극 시트로 구매 (NEI Corporation, Summerset, USA)** · Material 2 = **LG Chem INR18650 MJ1 셀 (NKON, Netherlands)** 에서 꺼낸 양극 · 그림 1 · 그림 S1–S3 외 **전부 Material 1** (p.12) · 시트의 조성 (활물질 · 결합제 · 탄소 비) · 캘린더링 압력 · 밀도 · 기공률 **[미확인]** |
| 셀 · 전해질 | 코인셀 (형식 [미확인]) · 음극 = NEI **흑연** · Celgard 분리막 · **1 M LiPF₆ in EC:EMC (3:7)** · Novonix 충방전기 + 25 °C 챔버 (p.12) — ⚠ **액체계 LIB · ASSB 아님 · SE 없음** |
| 연구유형 | 실험 영상 (실험실 X 선 나노 · 마이크로 CT) + 싱크로트론 나노프로브 XRD/XRF · **역학 시험 · 모델 계산 없음** |

## 3. 핵심 수치 ★

### 3.1 운전 전 결함 범주 — Table 1 (p.3 인쇄) + [카드 산술]

| 범주 (원문 정의 그대로) | Material 1 [%] | 상용 (Material 2) [%] | 상용 개수 [카드 산술 · k/401] |
|---|---|---|---|
| No defect — *"No obvious defects are visible"* | **69.8** | **65.8** | 264 |
| Internal void — *"An isolated void is located below the particle surface"* | 3.2 | 0.2 | 1 |
| Micro-crack — *"Small crack(s) that do not span the entire particle diameter"* | 7.6 | 9.2 | 37 |
| Bisect — *"A single large crack that splits the particle in two"* | 6.3 | 7.0 | 28 |
| Multi-prong — *"Two or more large cracks that split the particle into multiple sections"* | 5.4 | 8.2 | 33 |
| Prong & shatter — *"One or more large cracks that split the particle but with additional micro-cracks"* | 3.5 | 2.5 | 10 |
| Shatter — *"The particle has split into many small fragments (the size of primary particles) via multiple cracks"* | 3.2 | 7.0 | 28 |
| 합 [카드 산술] | **99.0** | **99.9** | **401** |

- 셈한 입자 (p.3 인쇄): **158 (Material 1)** · **401 (상용)** — *"counting the number of particles of each category along the electrode thickness"* (3D 자료 · 집전체 → 분리막).
- [카드 산술] 결함 = 100 − 결함 없음 = **30.2 · 34.2 %** (차 4.0 %p = 본문 *"approximately 4% more defective particles in the commercial material"* p.3 ✓) · 균열 다섯 범주 합 **26.0 · 33.9 %** · 쪼개짐급 (bisect + multi-prong + prong & shatter + shatter) **18.4 · 24.7 %** · shatter 비 7.0/3.2 = 2.19 (본문 *"more than double the number of shattered particles"* ✓) · 내부 공극 비 3.2/0.2 = 16 (*"an order of magnitude fewer"* ✓).
- ⚠ [카드 산술] **상용 열은 401 의 정수배와 정확히 맞지만 (합 401) Material 1 열은 158 의 정수배로 안 떨어진다** (69.8 → 110.3 · 5.4 → 8.53 · 3.5 → 5.53 개) — 합도 99.0 %. Fig. 1d 가 *"the average particle defect composition"* 이라 **깊이 칸 평균** 일 수 있다 (Fig. 1c 열 판독의 단순 평균 = 결함 30.8 % · Material 2 는 35.1 % — 표와 0.6 · 0.9 %p 차) — 계산법은 원문에 없다 [미확인].
- 내부 공극의 기원 (p.3): *"internal voids have been observed in raw powders before the production of coatings and have therefore been attributed to secondary particle manufacturing, rather than printing or calendaring.[18]"* — **합성 유래** (캘린더링 아님) · 상용 쪽이 한 자릿수 적다.

### 3.2 깊이 분포 (운전 전) — Fig. 1c · Fig. S3b [판독] + 본문 서술

| 깊이 칸 (집전체에서 µm · 축 글자) | Material 1 결함 % — Fig. 1c [판독] | 같은 자료 Fig. S3b [판독] | | 깊이 칸 (µm) | Material 2 (상용) 결함 % — Fig. S3b [판독] |
|---|---|---|---|---|---|
| 2 | 14.3 | 13.9 | | 2 | 25.4 |
| 6 | 12.9 | 12.4 | | 12 | 21.8 |
| 10 | 23.4 | 23.3 | | 22 | 34.0 |
| 14 | 10.1 | 9.9 | | 32 | 40.6 |
| 18 | **39.5** | 39.1 | | 42 | 36.5 |
| 22 | 20.3 | 19.8 | | 52 | 34.0 |
| 26 | 28.7 | 28.2 | | 62 | 32.0 |
| 30 | 37.1 | 36.6 | | 70 (분리막 쪽) | **56.3** |
| 32 | **56.6** | 56.4 | | | |
| 33 (분리막 쪽) | **64.7** | 64.4 | | | |

- 본문 (p.4 인쇄): *"both Material 1 and the commercial comparison exhibit more cracking toward the electrode-separator interface. This is most likely to be the surface in contact with the calendaring instrument during fabrication. For instance, over 50% of particles exhibit defects at the electrode-separator interface, for both materials. The degree of cracking is observed to decline away from the surface and then peak again toward the center of the electrode, before again declining toward the current collector."*
- ⚠ 깊이 칸 글자가 등간격이 아니다 (Material 1: 2 · 6 · … · 30 · **32 · 33**) — 칸 너비 · 칸 안 입자 수 [미확인]. 마지막 두 칸은 얇은 표면 층.
- 전극 두께 (그림 축 끝 글자): Material 1 ≈33 µm (본문 *"thin (≈30–40 µm)"* p.2) · Material 2 ≈70 µm (Fig. S3b) [인쇄 (축)].

### 3.3 사이클 뒤 전극 · 입자 수준 (Fig. 2 · Fig. S4)

| 양 | 값 | 쪽 · 표지 |
|---|---|---|
| 시료 | 같은 배치 (*"the same batch as Sample 1"* — 원문 'Sample 1' = Material 1) 코인셀 · 흑연 상대 · **형성 뒤 5 운전 사이클** · 상한 **4.2 · 4.3 · 4.4 · 4.5 V** · 3.0 V 에서 분해 | p.4 · p.12 [인쇄] |
| 전극 수준 영상 | 복셀 **1.57 µm** (본문 p.4 · 캡션) / **1.6 µm** (방법 p.12) · CT 용 원판 **1 mm** (10 mm 전극에서 펀칭) | 인쇄 |
| 관찰 | 4.4 · 4.5 V 시료: 집전체 박리 + 전극 전체 거시 균열 (Fig. S4) — *"these features were attributed to the sample preparation"* · 고전압 시료는 펀칭할 때 대부분 집전체에서 떨어짐 → *"potentially a binder issue, rather than just active material cracking"* | p.4 |
| 입자 수준 영상 | 복셀 **200 nm** (본문 p.4) / **206 nm** (Fig. 2 캡션) / **0.2 µm** (방법 p.12) | 인쇄 (반올림 차) |
| 관찰 | 표면 열화 뚜렷하지 않음 (거칠기 감소 가능) · 고전압 입자 다수의 **속 회색값 크게 하락** · 저전압 입자는 아님 | p.4 |
| 해상도 묶기 시험 (Fig. 2d) | 결함 입자 · 무결함 입자 각 하나의 선 주사 (≈0–12 µm) 를 **200 nm ↔ 1200 nm** 복셀로 — 결함 입자는 1200 nm 에서도 회색값 분산이 훨씬 크다 | p.4 · Fig. 2d |
| 시간 단축 (결론) | 결함 검출에 1–2 일 걸리던 CT 를 **≈2 h** 스캔으로 대체 가능 (수백 입자) | p.11 인쇄 |

### 3.4 4.5 V 전극에서 꺼낸 2차입자 7 개 (Figs. 3–6 · 나노 CT 126 nm + I14 XRD/XRF) — 그림 안 인쇄 값

| 입자 | 평균 회색값 (0–255 · Fig. 3c) | 등가 지름 d_e µm (Fig. 3e) | Ni % (Fig. 4b) | Mn % | Co % | r_I (Fig. 4c) | c/a (Fig. 4d) | I₀₀₃/I₁₀₄ (Fig. 4e) |
|---|---|---|---|---|---|---|---|---|
| 1 | 156 | 6.05 | 84.1 | 7.0 | 8.9 | 0.5 | 4.94 | 1.0 |
| 2 (Mn 덩어리 · Fig. 6 에서 뺌) | 154 | 8.07 | 83.3 | 7.7 | 9.1 | 0.4 | 4.98 | 0.7 |
| 3 | 154 | 8.07 | 83.4 | 7.2 | 9.4 | 0.4 | 4.98 | 2.7 |
| 4 | 153 | 2.52 | 83.1 | 7.4 | 9.5 | 0.3 | 4.96 | 1.5 |
| 5 | 152 | 4.54 | 83.2 [눈대중 — 막대 글자가 겹쳐 둘째 자리 흐림] | 7.7 | 9.1 | 0.2 | 4.97 | 3.8 |
| 6 | 148 | 4.54 | 84.4 | 6.6 | 9.0 | 0.8 | 4.96 | 3.2 |
| 7 | 147 | 4.04 | 83.6 | 7.3 | 9.1 | 0.3 | 4.96 | 3.1 |

- 순서 = 평균 회색값 순 (높을수록 결함 적음 · p.6). *"There does not appear to be a clear correlation between particle size and the defect severity. Therefore, at low C-rates (0.5C), particle sizes may not be of significant importance for secondary particle cracking."* (p.6) — n = 7 · d_e 2.5–8.1 µm.
- 평균 조성 *"Ni:Mn:Co ratio of ≈83:7:9 instead of 80:10:10"* (p.6 인쇄 · XRF 봉우리 넓이 비 · 단면적 · 형광 수율 보정 없음 p.12).
- XRD: r_I · c/a · I₀₀₃/I₁₀₄ 어느 것도 균열 정도와 상관 없음 (p.6) · 입자마다 회절 무늬 **≈40 000 개** 를 더해 정제 (p.6) · H2/H3 · 암염 세기는 *"very low quantities … qualitative"* (p.6 · Fig. 4f *"Qualitative – large error"*).
- Fig. 5 (입자 하나 · XRF-CT): Mn 은 표면 쪽으로 증가 · **미세균열 양옆에서 국소 Mn 4 → 6 %** (p.7 인쇄 · Fig. 5c Mn 4.7 → 6.5 % [눈대중]) · 중심 · 표면 · 홀로 붙은 1차입자 Ni ≈0.86 · 0.84 · 0.82 · Mn ≈0.05 · 0.07 · 0.09 · Co ≈0.09 [눈대중 Fig. 5b] · 입자 2 표면의 **Mn 풍부 덩어리** 는 NMC 보다 감쇠가 훨씬 작음 → 훨씬 덜 치밀 (p.7) — 기원 (제조 오염 ↔ 고전압 부산물) 은 4D 없이 못 가림.
- Fig. 6 (입자 2 제외 6 개): **최소 Mn ↔ c 격자상수 R² = 0.9** (c 14.276–14.324 Å [눈대중]) · **평균 Mn ↔ r_I R² = 1.0** (*"to 1 d.p."* p.7) · 그림 안 표지 *"NMC811 at 3.0 V vs. graphite"*.
- r_I 의 정의는 **그림 6c 안에만**: r_I = (I₀₀₆ + I₀₀₂)/I₁₀₁ (`eq_00a`) — 본문 정의 · 인용 없음 [미확인 — 첨자 (002) 가 의도한 반사인지 원문으로 확인 불가].

### 3.5 ★ 32 nm 나노 CT — 사이클 없음 ↔ 4.5 V 5 사이클 (Fig. 7 · p.9–11)

| 양 | 사이클 없음 ('Raw' · 초록) | 4.5 V × 5 → 3.0 V (빨강) | 표지 |
|---|---|---|---|
| 2차입자 | ≈16–18 µm · Material 1 · **Figs. 1–6 과 다른 입자** · 서로도 다른 입자 | 같음 | p.9 인쇄 |
| 표면에서 들어간 통로 | **≈2 µm** (그림 글자 *"1-2 µm Channels"*) | **최대 8 µm** | p.9 인쇄 · Fig. 7a/b |
| 큰 기공 | ≈500–900 nm (불균일) | 국소 군집 (*"localized clusters of more severe degradation"*) | p.9 |
| 깊이별 공극 (Fig. 7c, 1–7 µm) | 14.5 · 13.5 · 13.2 · 13.4 · 13.3 · 13.4 · 13.4 % — *"generally independent of the radial location"* | 17.7 · 18.3 · 18.7 · 19.2 · 19.4 · 20.5 · 22.7 % — 중심 쪽 증가 (*"the cracks converge toward the central core"*) | [판독] · p.9 |
| **평균 공극 (Fig. 7d)** | **13.5 %** (오차 막대 13.1–14.7) | **19.6 %** (17.9–22.9) | [판독] · 오차 막대 = *"maximum and minimum values for each particle"* (캡션) |
| 1차입자 지름 (Fig. 7e) | 평균 측정 가능 지름 **≈1 µm** · 점선 ≈1080 nm [판독] | **≈600 nm** · 점선 ≈660 nm [판독] | p.9 인쇄 |
| '붙은 (fused)' 1차입자 | 많음 — 경계를 못 가려 **둘을 하나로 셈** (*"two "fused" particles were considered as one"*) | *"far fewer "fused" particles"* | p.9 |
| Fig. 7f 표지 | *"143 nm ±30%"* · *"250 nm ±7%"* (붙은 1차입자 한 쌍 위 두 자) | — | 그림 안 인쇄 · 뜻 (무엇의 길이 · ± 의 정의) [미확인] |

- [카드 산술] 7c 일곱 점 평균 13.53 · 19.49 % ≈ 7d 막대 13.5 · 19.6 % · 7d 오차 막대 끝 ≈ 7c 최소 · 최대 → **7d = 7c 의 요약** (깊이 칸 평균 · 최소 · 최대) · 증가 +6.1 %p (× 1.45).
- 저자 한정 (p.11): *"there may be nano-particles that occupy what appears to be void-space at this resolution, artificially increasing the void-fraction. However, the quantification methods were identical for the two particles, therefore we can place high confidence in their comparison and relative changes observed on cycling."* · (p.10) *"ideally there should be tens or even hundreds of secondary particles … Maintaining this high resolution while also characterizing many secondary particles is unrealistic with the current imaging capabilities"*.
- 'Raw' 의 뜻 [카드 해석]: 그림 글자는 'Raw' 이나 본문은 *"imaged in the pristine state"* · *"no operational cycling"* · *"the same batch of Material 1"* (Material 1 = **전극 시트로 산 것**) → **원분말이 아니라 사이클 안 한 (캘린더링된) 시트의 입자**.

### 3.6 도입부 값 — [2차 인용] 또는 **출처 표기 없음** (인용 금지 수준)

| 값 | 원문 | 쪽 | 표지 |
|---|---|---|---|
| NMC811 전자전도도 **≈2.8 × 10⁻⁵ S/cm** · Li⁺ 확산계수 **10⁻⁸–10⁻⁹ cm²/s** | *"favorable rate capabilities (electronic conductivity ≈ 2.8 × 10−5 S cm−1 and Li+ diffusivity of 10−8 to 10−9 cm2 s−1)"* | p.2 | ⚠ **인용 번호 없음** — 리튬 상태 · 시료 형태 (입자 · 펠릿) 모름 |
| NMC 이론 용량 ≈270 mAh/g · NMC811 > 200 mAh/g | 인쇄 | p.2 | 2차 인용 · 일부 출처 없음 |
| 흑연 상대 4.2 V 에서 활물질 기준 NMC111 ≈500 · NMC811 > 600 Wh/kg | 인쇄 | p.2 | 출처 없음 |
| 산소 방출 전위 NMC811 ≈4.2 V (흑연 상대) ↔ NMC111 · 622 ≈4.6 V | 인쇄 | p.2 | [2차 인용] [11] Jung 2017 |
| 원분말 = 사이클 전 결함 해상 가능 · 균열 최소 | *"minimal particle cracking was observed at this stage in the particles' lifetimes (i.e., before printing into electrode sheets)"* | p.2 | [2차 인용] [18] (같은 그룹 · 카드 없음 — §14) |
| 탈리튬 때 층간 간격이 SoC 따라 커지다 높은 SoC 에서 붕괴 → 1차입자 사이 변형 | 인쇄 | p.2 | [2차 인용] [20] Märker 2019 |
| 내부 공극의 역학적 이점 (탈/리튬화 팽창 · 수축 응력 완화) | 인쇄 | p.3 | [2차 인용] [23] Mao 2019 |

### 3.7 판독 방법 · 오차 (digitized — TREND 전용 · 50 행)

- 원 래스터를 PDF 에서 그대로 꺼냄 (본문 그림 전부 1501 px 폭 / 360 pt = **300 dpi** · SI 그림 S3 1147 × 1263 px) → **y 축 눈금 표시 (축 왼쪽 짧은 검은 선) 중심**으로 선형 보정.
- Fig. 1c · S3b: 막대 열마다 초록 (결함 없음) 채움의 **아래 끝** → 결함 % = 100 − 초록 · 1 px = 0.35 %p (1c) — 같은 자료 두 그림 (1c ↔ S3b) 의 차 ≤ 0.5 %p.
- Fig. 7c: x 눈금 (1 µm 간격) ±9 px 창에서 표식 덩어리 — ▲ 는 세로 경계 상자 중심 · × 는 무게중심 · 1 px = 0.085 %p (▲ 의 무게중심 ↔ 상자 중심 차 ≤ 0.16 %p).
- Fig. 7d: 막대 윗변 검은 테두리 중심 · 오차 막대 끝 가로선 중심 · 1 px = 0.070 %p.
- Fig. 7e: 회색 점선 열 위치 · x 눈금 (250 nm 간격) 보정.
- 스크립트는 세션 scratchpad (커밋 안 함) · 값 = `digitized.csv` (그림 · 계열 · x · y · 방법 열).

## 4. 방법 ★

### 4.1 문제 설정 (p.1–2)
NMC811 은 다음 세대 차량용 양극 후보지만 결함 입자가 성능 손실과 이어진다. 문헌은 균열의 전구 기전을 여럿 든다 (격자 불변 전단 [12] · 전이금속 용출 [13] · 표면 상 재구성 [14,15] · Ni–Li 반자리 결함 [19] · 고 SoC 층간 붕괴 [20]).
원분말에는 균열이 적고 [18] 운전 뒤에는 많다 → **(1) 운전 전 전극에서 제조 유래 결함을 세고** (2) 상한 전압별 전극을 보고 (3) 2차입자 결함을 고배율로 정량 (4) 결정 · 화학 무질서와 견주고 (5) 1차입자 상호작용을 최고 해상도로 본다 — 전극 시트 → 2차 · 1차입자 → 결정 순서 (p.2).

### 4.2 시료 (p.2 · p.12)
- **Material 1** = NEI 전극 시트 (얇은 단층 · ≈30–40 µm · ≈2 mAh/cm² · p.2) — 활물질 · 결합제 · 탄소 비 · 캘린더링 조건 · 밀도 **[미확인]**.
- **Material 2 ('상용 비교')** = LG Chem INR18650 MJ1 셀의 양극 (두껍고 로딩 높음 · *"the calendaring requirements of such a thick, high-loading electrode"* p.4) — 단층 / 이층 여부는 결론 문장 (*"single- and double-layer fabrication designs"* p.11) 의 문맥으로만 읽힌다 [카드 해석].
- *"Although the exact calendaring parameters are not known to the authors"* (p.4) — 두 재료 모두 **캘린더링 압력 · 선하중 · 롤 간격 미상**.
- 사이클 시료 = Material 1 + NEI 흑연 (코인셀) · 4.5 V 전극에서 입자를 떼어 (*"extracted … re-mounted without the accompanying bulk material"* p.5 — 떼는 방법 [미확인]) 단독으로 영상.

### 4.3 전기화학 (p.12)
- 형성: CC **C/20** 충전 → **4.2 V** (흑연 상대) CV, 전류 < C/40 까지 → CC C/20 방전 → 3.0 V.
- 운전: CC–CV · 25 °C · 충전 **0.5C** (CV 끝 C/20) · 방전 **1C** → 3.0 V · **상한만 바꿈 (4.2 · 4.3 · 4.4 · 4.5 V)** · **5 사이클** 뒤 3.0 V 에서 분해 (p.4 · Fig. 2c 전압-시간 ≈20 h).
- *"To emulate as close to real-world application as possible, the NMC811 cathodes were cycled against graphite anodes (rather than Li metal)"* (p.4).

### 4.4 X 선 CT · 분할 (p.12)
- **나노 CT**: Zeiss Xradia **810 Ultra** · 회전 Cr 양극 · 준단색 **5.4 keV (Cr-Kα)** · 영역판 (zone-plate) 광학 · 복셀 **126 nm** (그림 1 · 3–6) · **32 nm** (그림 7).
- **마이크로 CT**: Zeiss Xradia **520 Versa** · W 양극 (구리 기판) · 다색 · *"characteristic emission peak at 58 keV (W-Kα)"* · 복셀 **1.6 µm** (그림 2a) · **0.2 µm** (그림 2b).
- 재구성: 평행 / 원뿔 빔 FBP (Zeiss "Reconstructor Scout-and-Scan") · 정량: Avizo Fire.
- 그림 3–6 회색값: 입자를 감싸는 구 경계 → 기공 · 활물질 회색값 자르기 분할 → Matlab 으로 활물질 복셀만의 히스토그램.
- 그림 7 분할: 비국소 평균 (non-local means) 필터 → **'bright' top-hat** 분할 (Avizo).
- 결함 범주 (Table 1) 셈: 3D 자료를 집전체 → 분리막으로 훑으며 범주별 입자 수 (판정은 사람 — 자동 분류 · 판정 기준 크기 (균열 폭 · 길이 문턱) **[미확인]**).

### 4.5 싱크로트론 (p.12)
Diamond **I14** 나노프로브 · 단색 **19 keV** · 빔 **≈50 nm** · 입자 전체를 래스터 · 회절 + 형광 동시 · 노출 **100 ms** · 회절 = Excalibur 3M (CeO₂ 보정) · 형광 = RaySpec SDD (후방 · xspress3 데드타임 보정) · 회절 무늬 합 → PyFAI 방사 적분 → **Topas 6** 정제 · XRF = Ni · Mn · Co 봉우리 넓이 비 (*"without correction for fluorescence cross-section or fluorescence yield differences"*) · DAWN.
그림 4 = **2D XRF 지도의 입자 전체 평균** · 그림 5 = **XRF-CT** (속 정보) (p.7).

### 4.6 통계
평균 · 오차 막대 (그림 3c = 입자 안 최대 · 최소 회색값 · 그림 7d = 입자의 최대 · 최소) · 선형 맞춤 R² (그림 6) · **검정 · 신뢰구간 없음** · 입자 수 158 / 401 (Table 1) · 7 (그림 3–6) · 2 (그림 7).

### 4.7 ★ 입자 처리 (우리 축과의 대응)
- 이 논문의 '입자' = **다결정 2차입자 (≈2.5–18 µm)** = 우리 DEM 의 AM 구 한 개 · 그 **안** 의 1차입자 (≈0.6–1 µm) 와 1차입자 사이 공극을 처음으로 정량.
- **역학 · 하중 · 압력이 없다** — 결함은 이미 만들어진 상태 (캘린더링 뒤 · 사이클 뒤) 를 사진으로 센 것이고, 기전 (캘린더링 · 팽창/수축 · 결정 방위) 은 저자 해석이다.
- frame [5] 로 읽으면: 우리 DEM 은 '입자 여러 개 · 접촉력 · 내부 없음', 이 논문은 '입자 안 구조 · 결과 상태 · 힘 없음' — 겹치는 곳은 **"압밀 뒤 깨진 AM 입자 비율 · 위치"** 하나다 (§7.4).

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Fig. 1** | 운전 전 Material 1: (a) 나노 CT 직교 단면 (집전체 → 분리막 화살표) (b) 결함 7 범주 그림 (No defects · Micro-crack · Bisected · Multi-prong · Prong & shatter · Shatter · Internal Void) (c) 깊이별 범주 비율 쌓은 막대 (칸 2–33 µm) (d) 평균 구성 원그래프 (69.8 · 7.6 · 6.3 · 5.4 · 3.5 · 3.2 · 3.2 %) | **결함 분류 꼴** — 우리 Auerbach/Lawn 사다리와 대응시켜 볼 수 있는 실측 범주 (§7.4) · 깊이 분포 = 롤 쪽 표면 집중 |
| **Fig. 2** | 사이클 뒤: (a) 전극 수준 3D (4.2 · 4.3 · 4.4 · 4.5 V · 1.57 µm · 축척 200 µm) (b) 입자 수준 (206 nm · 50 µm) (c) 4.2 · 4.5 V 이진 단면 + 전압-시간 (5 사이클 · ≈20 h) (d) 결함 · 무결함 입자의 선 주사 회색값 — 200 ↔ 1200 nm 복셀 | **저해상에서도 결함 입자 검출 가능** — 회색값 분산이 대리 지표 |
| **Fig. 3** | 4.5 V 전극에서 뗀 입자 7 개: (a) 3D (b) 회색값 히스토그램 (봉우리 이동 · 넓어짐 = 공극 증가) (c) 평균 회색값 156 → 147 (d) 표면에서 거리별 회색값 (0.25–4 µm) (e) 등가 지름 2.52–8.07 µm | 입경 ↔ 결함 정도 상관 없음 (n 7) |
| **Fig. 4** | 같은 7 입자: (a) 3D (b) XRF Ni · Mn · Co (c) r_I (d) c/a (e) I₀₀₃/I₁₀₄ (f) 암염 · H2/H3 세기 ('정성 · 큰 오차') | 결정 · 화학 지표가 균열 정도와 상관 없음 |
| **Fig. 5** | 입자 하나 (2): (a) 볼 곳 넷 (Particle · Surface · Core · Crack) (b) 중심 · 표면 · 홀로 붙은 1차입자 조성 (c) 균열을 가로지르는 Ni · Mn · Co (0.7–1.3 µm) (d) Mn 형광 · 전체 감쇠 지도 + Mn 덩어리 확대 (e) 덩어리 분리 | 균열 옆 Mn 상승 (4 → 6 %) · 덜 치밀한 표면 덩어리 |
| **Fig. 6** | 입자 2 를 뺀 6 개: (b) 최소 Mn ↔ c 격자상수 (R² 0.9) (c) 평균 Mn ↔ r_I (R² 1.0) · 그림 안 r_I 정의식 | r_I 정의 (`eq_00a`) |
| **Fig. 7** | 32 nm: (a) 사이클 없음 2차입자 — 3D · 단면 · 기공 골격 (1–2 µm 통로) (b) 4.5 V 5 사이클 — 같은 셋 (통로 최대 8 µm · 빨간 화살표 = 1차입자 사이 균열) (c) 표면에서 깊이별 공극 (d) 평균 공극 Raw ↔ 4.5 V (e) 1차입자 등가 지름 분포 (f) '붙은' 1차입자 한 쌍 | ★ **AM 2차입자 = 다공체** (사이클 전 13.5 % [판독]) · 사이클 뒤 1차입자 사이 분리 (Stallard 리뷰 0.14 → 0.19 의 원천) |
| **Table 1** | 운전 전 결함 범주 정의 + Material 1 · 상용 비율 | §3.1 |
| **Fig. S1** | Material 1 운전 전 나노 CT 단면 둘 (색 동그라미 = 결함 입자 · 축척 0–40 µm) | 범주 판정의 원자료 예 (색 범례는 그림에 없음) |
| **Fig. S2** | Material 2 (상용) 같은 꼴 둘 | 상용 쪽 균열 · 산산조각 예 |
| **Fig. S3** | Material 1 ↔ 2 나란히: (a) 단면 (b) 깊이별 범주 (Material 2 칸 2–70 µm) (c) 원그래프 (d) 범주 그림 | Material 2 깊이 분포 (§3.2) |
| **Fig. S4** | 마이크로 CT 단면 — 상한 4.2 V (파랑) · 4.5 V (빨강 · 박리 화살표) · 'Line' 측정 6 개씩 (4.2 V 54.6–57.33 · 4.5 V 51.46–60.59 — **단위 · 무엇을 잰 선인지 미기재**) | ⚠ 캡션 = *"prepared from Material 2"* ↔ 본문 = 사이클은 Material 1 만 (§11-A) |
| **Fig. S5** | I14 회절 검출기 2D 무늬 예 (점 모양 — 입자 하나 안 결정립 수 한정) | 단일 입자 회절 통계의 한계 그림 |
| **Fig. S6–S8** | I14 XRF 스펙트럼 — Mn (5.89 keV) · Co (6.93 keV) · Ni (7.49 keV) 봉우리 · 선 = 자료 번호 7 개 (83905–83919) | XRF 정량 원자료 |

### 5.1 크롭 색인 — `litdb/figures/heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct/`

도구 크롭 16 장 (본문 Fig. 1–7 + Table 1 + SI Fig. S1–S8) 을 **전부 Read 로 열어 확인** → **9 장 손으로 재크롭** (tab_1 = 쪽 거의 전체가 잡힘 · SI 그림 8 장 = 'WILEY-VCH' 로고 혼입 + 그림 아래 끝 (눈금자 숫자 · 축 이름) 잘림 — 원인: SI 캡션 블록 bbox 가 실제 캡션 글자보다 ≈12 pt 위에서 시작).
본문 그림 7 장은 원 래스터 전체가 들어가 그대로 · 도구 캡션 다섯 (Fig. 1 · 4 · 5 · 6 · 7) 에 이웃 본문이 섞여 원문 캡션 글자로 바꿈 (`caption_tool` 에 앞부분 보존). 재크롭 근거 = `figures.json` 의 `recrop` (자동 bbox = `auto_bbox`).
손 크롭 23 장 (`manual_crop`): 패널 2 · 그림 안 정의식 1 · 근거 문단 20. 다시 자른 것 = fig_S7 · fig_7d · eq_00a 각 1 회. **전체 쪽 그림 (`page_*`) 은 만들지 않았다.**
⚠ `--slug heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct --clean` 으로 재추출하면 재크롭 9 장이 자동 bbox 로 되돌아가고 손 크롭 23 장이 지워진다 (`pdf_map.tsv` 경고 같음).

| 파일 | 쪽 (PDF) | bbox (pt) | px | 확인 |
|---|---|---|---|---|
| `fig_1.png` | 3 | 45.0, 64.9, 555.4, 316.5 | 2128 × 1049 | ✅ a–d · 축 · 범주 그림 |
| `fig_2.png` | 5 | 45.0, 64.9, 555.1, 517.9 | 2126 × 1889 | ✅ a–d · 축척 · 범례 |
| `fig_3.png` | 6 | 42.2, 64.9, 552.3, 410.5 | 2127 × 1441 | ✅ a–e · 막대 글자 |
| `fig_4.png` | 7 | 45.0, 64.9, 555.4, 445.8 | 2128 × 1588 | ✅ a–f · 막대 글자 |
| `fig_5.png` | 8 | 42.2, 64.9, 552.5, 591.4 | 2128 × 2195 | ✅ a–e · 축척 |
| `fig_6.png` | 9 | 45.0, 64.9, 555.4, 336.8 | 2128 × 1134 | ✅ a–c · R² · 정의식 |
| `fig_7.png` | 10 | 42.2, 64.9, 552.5, 603.9 | 2128 × 2247 | ✅ a–f · 축척 · 범례 |
| `tab_1.png` | 3 | 47.0, 585.5, 551.0, 719.5 | 2101 × 559 | 🔧 **재크롭** — 자동 bbox (45.9, 11.9, 589.2, 771.1 · 284 dpi) 가 쪽 거의 전체 → 표 캡션 ~ 아래 괘선 |
| `fig_S1.png` | SI 3 | 117.9, 69.5, 477.1, 242.3 | 1497 × 721 | 🔧 **재크롭** — 로고 혼입 · 눈금자 '0 · 40 [µm]' 잘림 → 래스터 경계 + 2 pt |
| `fig_S2.png` | SI 3 | 116.1, 321.2, 479.1, 498.1 | 1514 × 738 | 🔧 **재크롭** — 눈금자 숫자 잘림 |
| `fig_S3.png` | SI 4 | 71.4, 69.5, 523.5, 566.3 | 1885 × 2071 | 🔧 **재크롭** — 로고 · 아래 끝 |
| `fig_S4.png` | SI 5 | 118.3, 69.5, 477.0, 553.2 | 1496 × 2016 | 🔧 **재크롭** — 로고 · 아래 끝 |
| `fig_S5.png` | SI 6 | 117.0, 69.5, 478.3, 382.6 | 1506 × 1306 | 🔧 **재크롭** — 로고 · 아래 끝 |
| `fig_S6.png` | SI 7 | 126.9, 69.5, 468.3, 356.5 | 1424 × 1197 | 🔧 **재크롭** — 로고 · 축 이름 잘림 |
| `fig_S7.png` | SI 7 | 121.7, 396.2, 473.3, 690.2 | 1466 × 1226 | 🔧 **재크롭 (2 회)** — 위 · 아래 끝 · 첫 재크롭에 S6 캡션 끝줄이 비쳐 다시 |
| `fig_S8.png` | SI 8 | 117.5, 69.5, 477.8, 372.4 | 1502 × 1263 | 🔧 **재크롭** — 로고 · 아래 끝 |
| `fig_1c.png` | 3 | 116.0, 180.0, 300.0, 312.0 | 767 × 550 | ✋ 패널 (깊이별 결함 비율) |
| `fig_7d.png` | 10 | 359.0, 380.5, 470.0, 489.0 | 464 × 453 | ✋ 패널 (평균 공극 Raw ↔ 4.5 V) · 2 회 (빨간 틀 선 제거) |
| `eq_00a_rI_factor_definition_fig6c.png` | 9 | 362.0, 240.2, 430.5, 269.5 | 381 × 164 | ✋ 그림 6c 안 r_I 정의식 (400 dpi) · 2 회 |
| `txt_p1_abstract_one_third_defective_separator.png` | 1 | 48.0, 230.5, 370.0, 482.5 | 1342 × 1051 | ✋ 초록 |
| `txt_p2_raw_powder_minimal_cracking_dislocation_meaning.png` | 2 | 46.0, 575.3, 294.5, 695.9 | 1037 × 503 | ✋ 원분말 균열 최소 [18] · 'dislocation' = 분리 |
| `txt_p2_aim_preexisting_defects_manufacturing.png` | 2 | 301.0, 156.7, 551.0, 222.9 | 1042 × 277 | ✋ 연구 목적 (제조 유래 기존 결함) |
| `txt_p2_calendering_tunable_material1_thin_2mAh.png` | 2 | 301.0, 531.3, 551.0, 674.2 | 1042 × 597 | ✋ Material 1 사양 |
| `txt_p3_158_401_particles_counted_along_depth.png` | 3 | 46.0, 454.3, 294.5, 574.9 | 1037 × 504 | ✋ 셈 방법 · 158 / 401 |
| `txt_p3_internal_voids_powder_origin_4pct_more.png` | 3 | 301.0, 410.3, 551.0, 574.9 | 1042 × 687 | ✋ 내부 공극 = 합성 유래 · 4 % |
| `txt_p4_calendering_params_unknown_al_yield.png` | 4 | 46.0, 69.3, 294.5, 189.9 | 1037 × 504 | ✋ 캘린더링 변수 미상 · Al 항복 |
| `txt_p4_separator_side_over50pct_one_third_precycling.png` | 4 | 46.0, 190.3, 294.5, 420.9 | 1037 × 962 | ✋ 분리막 쪽 > 50 % · 임계 압력 질문 · ⅓ |
| `txt_p4_cycling_5cycles_graphite_delamination_prep.png` | 4 | 46.0, 464.7, 294.5, 706.9 | 1037 × 1010 | ✋ 5 사이클 · 흑연 · 박리 = 시료 준비 |
| `txt_p6_greyscale_order_no_size_correlation_05C.png` | 6 | 46.0, 498.3, 294.5, 640.9 | 1037 × 595 | ✋ 입경 ↔ 결함 상관 없음 |
| `txt_p8_mn_disorder_not_correlated_cracking_1to5cycles.png` | 8 | 46.0, 630.3, 551.0, 717.9 | 2105 × 366 | ✋ Mn · 무질서 ↔ 균열 무관 (두 단) |
| `txt_p9_fig7_two_particles_16_18um_not_fully_dense_channels.png` | 9 | 46.0, 421.3, 294.5, 717.9 | 1037 × 1237 | ✋ 서로 다른 두 입자 · 치밀 아님 · 2 ↔ 8 µm |
| `txt_p9_void_converge_core_fused_primary_1um_to_600nm.png` | 9 | 301.0, 399.3, 551.0, 717.8 | 1042 × 1328 | ✋ 중심 수렴 · 붙은 1차입자 · 1 µm → 600 nm |
| `txt_p10_two_particles_representativeness.png` | 10 | 46.0, 663.3, 551.0, 717.9 | 2105 × 229 | ✋ 대표성 (수십–수백 필요 · 두 단) |
| `txt_p11_resolution_nanoparticles_inflate_void_fraction.png` | 11 | 46.0, 69.3, 294.5, 189.9 | 1037 × 504 | ✋ 해상도 · 공극 과대 가능 |
| `txt_p11_conclusion_calendared_one_third_defective.png` | 11 | 46.0, 597.3, 294.5, 695.9 | 1037 × 412 | ✋ 결론 — 캘린더링 뒤 ⅓ |
| `txt_p11_conclusion_no_size_corr_mn_fabrication_separation.png` | 11 | 301.0, 388.3, 551.0, 618.9 | 1042 × 962 | ✋ 결론 — 균열 = 제조 + 1차입자 분리 |
| `txt_p12_conclusion_cracks_at_primary_boundaries.png` | 12 | 46.0, 102.3, 294.5, 211.9 | 1037 × 457 | ✋ 결론 — 1차입자 경계 균열 · 결정 방위 |
| `txt_p12_materials_nei_lg_mj1_cycling_protocol.png` | 12 | 46.0, 309.7, 294.5, 537.7 | 1037 × 951 | ✋ 재료 · 사이클 조건 |
| `txt_p12_ct_voxels_126_32nm_micro_1p6_0p2um.png` | 12 | 46.0, 537.7, 294.5, 718.2 | 1037 × 753 | ✋ CT 장비 · 복셀 |

판독 원자료: 같은 폴더 `digitized.csv` (50 행 · 전부 `digitized` · 방법 열 포함).

## 6. Post-processing ★

- **결함 범주**: 3D 나노 CT 를 깊이 방향으로 훑으며 사람이 7 범주로 판정 (판정 문턱 · 판정자 수 · 재현성 [미확인]) · 저자: *"this is not intended as an exhaustive list"* (p.3).
- **회색값 대리**: 입자를 감싸는 구 → 활물질 복셀만의 히스토그램 · 평균 · 최대/최소 · 표면에서 거리별 평균 · 등가 지름 (그림 3) · 해상도 묶기 (200 → 1200 nm) 로 대리 지표 견고성 확인 (그림 2d · n = 결함 1 + 무결함 1).
- **32 nm 공극**: NLM 필터 → top-hat 분할 → 공극 분율 (깊이별 · 평균) · 기공 골격 지도 · 1차입자 분할 → 등가 지름 분포 (붙은 둘은 하나로).
- **XRD**: 입자당 ≈40 000 무늬 합 → PyFAI → Topas 6 (r_I · c · a · I₀₀₃/I₁₀₄ · 암염 · H2/H3) · **XRF**: 봉우리 넓이 비 (보정 없음) · 2D 지도 평균 / XRF-CT.
- **도구**: Zeiss Scout-and-Scan (재구성) · Avizo Fire · Matlab · PyFAI · Topas 6 academic · DAWN.

## 7. 우리 대비 ★ — AM 출발 상태 (조건 R7) · AM 입자 내부 공극 · Auerbach 파괴 분류

> 우리 값의 출처 = 정본 카드 (`wheatcroft2023_…` §4.8 · §7.3 · §13 — 작업 브랜치 `scripts/fracture_model.py` · `docs/data/case_master.csv` 를 그 카드가 읽은 값) 와 프로젝트 지시문의 frame (DEM E_eff 1.35 GPa · Heckel P_y 138 MPa · MPM E 1.53 · σ_y 0.30 · ν 0.49). 이 카드는 우리 코드 · 자료를 새로 읽지 않았다.

### 7.1 대조표

| 항목 | 이 논문 | 우리 (DEM · MPM) | 판정 |
|---|---|---|---|
| AM | 다결정 NMC811 2차입자 (≈2.5–18 µm) · 1차입자 ≈0.6–1 µm · 1차입자 사이 공극 13.5 % [판독 · 사이클 전] | AM_P = 다결정 NCM811 구 (D 10–12 µm) · **치밀 탄성 구** (E 140 GPa · ν 0.25) · MPM = 얼린 scaffold | 같은 부류 · ⚠ 우리 AM 은 **속이 꽉 찬 구** (내부 공극 0) |
| 출발 상태 | 원분말 = 균열 최소 [18 · 2차 인용] · 캘린더링된 시트 = **≈30 % 결함** | DEM 은 느슨한 분말에서 시작 (t = 0 무손상) → 300 MPa 압밀 | ✅ 분말 무손상 가정은 [18] 로 지지 · 압밀 뒤 결함은 **우리 계산이 만들어야 할 결과** |
| 압축 | 롤 캘린더링 (압력 · 선하중 · 롤 간격 **미상**) · 결합제 · 탄소 · **SE 없음** | 일축 금형 300 MPa · SE (LPSCl) 가 AM 사이를 채움 | ⚠ 하중 경로가 다르다 — SE 완충이 없는 액체계 시트 |
| 파괴 판정 | 사람이 7 범주로 셈 (126 nm 복셀로 보이는 균열) | 접촉별 Auerbach P_c = A·K²·R/E\* × Lawn 1 · 3 · 11 · 32 (사후 분류) | 범주 ↔ 사다리 대응은 해석 (§7.4) |
| 위치 | 롤과 닿은 면 (분리막 쪽) > 50 % · 가운데 봉우리 (Fig. 1c 18 µm 39.5 % [판독]) | (대응 출력 [미확인] — 우리 분류의 깊이별 분포를 아직 안 봄) | 결과 전 대조 항목 후보 |
| 사이클 | 액체 4.5 V × 5 → 1차입자 사이 공극 +6.1 %p · 1차입자 분리 | A10 `cycle_contact_ledger` poly 입계 void (ASSUMED-FORM) | 모양 참고만 (액체계 · 흑연 상대) |
| 역학 값 | **없음** (E · H · K_IC · 강도 · 압력 0 개) | — | 이 논문은 파라미터 출처가 아니다 |

### 7.2 ★★★ 판정 — 조건 R7 (AM 출발 상태 · 무손상 가정)
1. **분말 단계의 '무손상' 은 지지된다 (간접)** — 원분말에는 *"minimal particle cracking"* ([18] · 2차 인용 · 같은 그룹) · 이 논문 Table 1 의 내부 공극 (3.2 · 0.2 %) 만 합성 유래로 원분말에 이미 있다 (p.3).
2. **압밀 (캘린더링) 뒤의 '무손상' 은 성립하지 않는다** — 운전 전 시트에서 결함 30.2 · 34.2 % · 균열 26.0 · 33.9 % · 쪼개짐급 18.4 · 24.7 % [카드 산술 · Table 1]. 저자 해석 = 시트 인쇄 · 캘린더링 (*"once the active material is printed into a sheet and calendared, the fabrication-induced cracking can be severe"* p.11).
   ⇒ 우리 DEM 이 '압밀 뒤 AM 은 온전' 을 **가정**하면 안 되고, Auerbach 분류가 **만들어 낸 결과**로 다뤄야 한다 — 지금 구조가 그렇다 (사후 분류). 이 논문은 그 결과와 견줄 **실측 꼴** (범주 비율 · 깊이 분포) 을 준다.
3. **AM 소성은 이 논문으로 판단할 수 없다** — 원문에 NMC 소성 · 전위 서술이 없다 (§0 ② ③). 'AM 강체 · 탄성' 가정을 이 논문으로 **지지하지도 반박하지도** 않는다. 알 수 있는 것: 캘린더링 압력이 **알루미늄 항복을 넘을 만큼** 국소적으로 컸고, AM 은 그 Al 을 소성 변형시킬 만큼 단단했다 (p.4 — AM 이 하중을 집전체에 전달 · 조건 R1 의 정성 증거).
4. **2차입자는 치밀체가 아니다** — 사이클 전 1차입자 사이 공극 13.5 % [판독 · n = 1 · 32 nm] (§7.3).

### 7.3 ★★ 입자 내부 공극 ↔ 우리 ε_sphere (치밀 구) — `stallard2022_cathode_…` §9-5 의 질문에 1 차 자료
- 이 논문의 사이클 전 2차입자 (≈16–18 µm · 캘린더링된 시트 · 32 nm) 에서 1차입자 사이 공극 = **13.5 %** (깊이별 13.2–14.5 %) [판독 Fig. 7c · 7d].
- 실험 기공률을 **결정 진밀도** 로 계산하면 AM 속 공극도 '전극 기공' 에 들어간다. 우리 ε_sphere 는 AM 구를 꽉 찬 고체로 센다 → [카드 산술 · 가정] 전극 기공 차 ≈ φ_AM,env × 0.135 = **6.8 · 8.1 · 9.5 %p** (AM 외피 부피분율 0.5 · 0.6 · 0.7 일 때). 실험 쪽이 **입자 (외피) 밀도** 를 쓰면 차는 0.
- ⇒ **단계 0 에 결과 전에 등록할 항목**: 견줄 실험 기공률이 어느 밀도 기준인지 (결정 진밀도 ↔ 2차입자 외피 밀도 ↔ 펠릿 Archimedes) · 우리 랩 기준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정) 은 **SE 만의 값이라 이 문제와 무관** — 복합 양극 비교 때만 걸린다.
- ⚠ 한정어: n = 1 입자 · 32 nm 해상도 (더 작은 공극은 놓침 ↔ 나노입자가 공극처럼 보여 과대 — 저자 p.11) · NEI 공급 NMC811 (우리 공급사 [미확인]) · 사이클 전이지만 **캘린더링된 시트의 입자** (원분말 공극은 [미확인]).

### 7.4 ★ 7 범주 ↔ 우리 Lawn 사다리 — 결과 전 대조 항목 (해석 · 비준 대기)
| 이 논문 범주 (Table 1) | 뜻 | 우리 사다리 (`fracture_model.py` · `wheatcroft2023_…` §7.3) 와의 대응 [카드 해석] | Material 1 / 상용 % |
|---|---|---|---|
| Micro-crack | 지름을 다 가르지 않는 작은 균열 | microcrack (1 · P_c) – multicrack (3 · P_c) | 7.6 / 9.2 |
| Bisect | 큰 균열 하나 → 두 쪽 | fragmentation (11 · P_c) | 6.3 / 7.0 |
| Multi-prong | 큰 균열 둘 이상 → 여러 쪽 | fragmentation | 5.4 / 8.2 |
| Prong & shatter | 큰 균열 + 미세균열 | fragmentation – pulverization | 3.5 / 2.5 |
| Shatter | 1차입자 크기 조각들 | pulverization (32 · P_c) | 3.2 / 7.0 |
| Internal void | 표면 밑 고립 공극 | (파괴 아님 — 합성 유래) | 3.2 / 0.2 |

- 견줄 꼴: **입자 비율** (접촉 비율 아님) · **깊이 분포** (윗판 = 롤 쪽 표면 집중?) · **범주 비** (쪼개짐급 18–25 % ↔ 미세균열 8–9 %).
- 견주는 사람이 먼저 적을 것 (결과 전): 우리 출력의 '입자 단위' 정의 (입자의 최대 접촉 F/P_c? 접촉 수?) · 이 논문의 판정 해상도 (126 nm 복셀 — 그보다 가는 균열은 '결함 없음' 으로 셈) · 조건 차 (롤 캘린더링 · SE 없음 · 압력 미상).
- 우리 쪽 사전 정보 (정본 `wheatcroft2023_…` §7.4 · D16 · D17 의 값 — 이 카드가 다시 재지 않음): 코퍼스 AM_P–AM_P **중앙 접촉** F/P_c 10.6 (fragmentation 11 바로 아래) · 중앙 접촉이 우리 fragmentation (133 MPa) 을 넘는 케이스 26 % — **케이스 단위 중앙 접촉**이라 이 논문의 입자 비율과 같은 양이 아니다.

### 7.5 정본 다른 카드와의 긴장 (해상도 · 공정이 다르다)
- `wheatcroft2023_…` (SI XCT · 0.56 µm 복셀 · 균열 ≥ 2 µm 만 셈) = 비순환 전극 **0.7 %** (> 15 µm 입자 9.3 % · 10–15 µm 0 %) — 그 카드 §8 ⑤ 는 *"우리 크기에서는 가정이 방어된다 (≥ 2 µm 균열 기준)"*. 그런데 그 전극은 **무압연** (캘린더링 안 함) 이고 이 논문은 **캘린더링된 시트 + 126 nm 복셀** → 30 %. 두 값은 모순이 아니라 **공정 (압연 유무) 과 판정 해상도가 다른 두 측정** — 섞어 쓰지 않는다.
- `dang2019_…` · `wheatcroft2023_…` 의 낱알 압괴 강도 (평판 ≈190–210 MPa) 는 **얼마의 힘에 깨지나**, 이 논문은 **실제 공정 뒤 얼마나 깨져 있나** — 둘을 이으려면 캘린더링 압력이 있어야 하는데 이 논문에 없다.
- `stallard2022_nmc811_single_crystal_…` 의 단결정 기저면 슬립 (τ_C 86 → 39 MPa) 은 **단결정 · 무압연** · 이 논문은 다결정 · 슬립 서술 없음 — 'AM 소성' 근거는 그쪽에서만.

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나 (정독 지시서의 이름별)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 조건 차이 |
|---|---|---|
| **단계 0** (기공률 연산자 · 판정 기준 결과 전) | ★ AM 2차입자 **내부 공극 13.5 %** [판독] → 실험 기공률의 밀도 기준을 결과 전에 등록해야 하는 근거 (§7.3) · 공극 정의 (1차입자 사이 · 32 nm · top-hat) | 전극 기공률 값 **없음** (시트 기공률 · 밀도 미기재) · SE 없음 → 랩 기준 (순수 SE 10–13 % · 진밀도 1.64 g/cm³) 과 **같은 양이 아니다** |
| 단계 1 (3D 메모리) | 없음 | — |
| 단계 2 (2D MPM 코드 · 단위 시험) | 없음 | — |
| 단계 3 (2D 접촉 표현 시험) | 없음 | — |
| 단계 4 (3D 순수 SE · σ_y 보정) | 없음 | SE 없음 |
| **단계 5** (3D 복합 압축) | ★ **결과 전 대조 항목**: 압밀 뒤 깨진 AM 입자 비율 (균열 26–34 % · 쪼개짐급 18–25 % [카드 산술]) · 깊이 분포 (누르는 면 쪽 > 50 % · 가운데 봉우리) · 범주 비 (§7.4) — 방향 · 꼴만 | 롤 캘린더링 ≠ 일축 300 MPa · 압력 미상 · 결합제/탄소 (SE 완충 없음) · 126 nm 판정 · 입자 158 / 401 — 절대값 전이 **안 됨** |
| 단계 6 (탈압 · 되돌아옴) | 없음 | 하중 · 탈압 자료 없음 |
| 단계 7 (형상 · 피복 · 수송) | 흐름 밖: Mn 덩어리가 이온 경로를 돌게 해 tortuosity 를 키울 수 있다 (정성 · p.7) · 균열 = 새 표면 (정성) | 수송 값 0 개 |
| **후보 D0** (지금 DEM) | Auerbach 사후 분류 결과를 견줄 **실측 꼴** (§7.4) · 'AM 무손상 출발' 의 분말 단계 정당화 ([18] 2차 인용) | AM 강체 가정의 검증 없음 · 강도 · K_IC · E 0 개 |
| 후보 A′-0 · A · A′ (MPM AM 강체 / 입자별 속도장) | 간접: AM 의 ≈⅓ 이 압밀 중 깨진다 → '움직이는 강체 AM' 은 파괴를 못 그린다는 한계의 실측 크기 | MPM · 접촉 법칙 정보 없음 |
| 후보 B (입자별 FE · MPFEM) | 간접: 2차입자 = 1차입자 집합 + 13.5 % 공극 → 입자 내부를 해상하면 넣을 형상 정보 (1차입자 ≈1 µm · 붙은 쌍) | 역학 물성 없음 |
| 후보 C · C′ (MDR · 캡 접촉 DEM) | 없음 | — |
| 후보 M0 (균질화 압밀) | 없음 | — |
| U0–U6 (단위 시험) | 없음 (입자 하나 역학 시험 없음) | U3 · U5 꼴 자료 없음 |
| 조건 R1 (AM 이동 · 하중 분담) | 정성: 입자가 집전체에 박혀 Al 을 소성 변형 (p.4) · 두꺼운 고로딩 전극에서 *"particles stacking and forming localized stress peaks"* (가설 · p.4) = AM 하중 사슬 | 하중 분담 값 없음 |
| 조건 R2 – R6 | 없음 | — |
| **조건 R7** (AM 파괴) | ★ 출발 상태 (분말 무손상 [18] · 압밀 뒤 ≈30 % 결함) · 범주 정의 7 · 깊이 분포 · 사이클 뒤 1차입자 분리 · 입자 내부 공극 · 균열 기원 해석 (제조 + 팽창/수축 + 결정 방위 · Mn 화학 무관) | 파괴 하중 · 강도 · 압력 · K_IC 없음 · 'AM 전위 활주 / 소성' 없음 |
| 결과 전 대조 항목 | ① 압밀 뒤 AM 입자 결함 비율 · 범주 비 ② 누르는 면 쪽 집중 여부 ③ (복합 양극 기공률을 실험과 견줄 때) AM 내부 공극 몫 | 견줄 조건을 맞출 수 없음 — 방향 · 순서만 |

**우리 숫자와 나란히 놓기** (같은 양 아님 — 자리만):
- DEM E_eff 1.35 GPa · Heckel P_y 138 MPa · MPM E 1.53 · σ_y 0.30 · ν 0.49 = **SE (LPSCl) 의 모델 값** → 이 논문 (SE 없음) 과 견줄 자리 없음.
- AM: 우리 E 140 GPa 치밀 구 ↔ 이 논문의 13.5 % 다공 2차입자 — 다공체 강성 감소의 크기는 이 논문에 없다 (`stallard2022_cathode_…` 의 경험식 E = E₀e^(−βf_P) · β 값 없음).
- 차원 · 재료: 이 논문 = 3D 영상 · NMC811 (공급사 NEI · LG) · 액체계 LIB 시트 · 흑연 상대 사이클. 우리 = 3D DEM / 2D·3D MPM · NCM811 + LPSCl · ASSB.

## 9. 적용 인사이트 (우리 연구에 어떻게)

### ① ★★★ 'AM t = 0 무손상' 의 문장을 둘로 나눈다
원고 · SI · 보고에서 *"AM 은 처음에 무손상"* 을 쓸 때 **"압밀 전 분말 (Heenan 2020 [18] 의 2차 인용 · 이 논문 p.2)"** 로 한정하고, 압밀 **뒤** 는 *"캘린더링된 상용 NMC811 시트에서 사이클 전 입자의 약 ⅓ 이 이미 결함 (Heenan 2020 · 126 nm X 선 나노 CT)"* 을 우리 Auerbach 분류가 다뤄야 할 현상으로 적는다.

### ② ★★ 단계 0 등록 — 실험 기공률의 밀도 기준
복합 양극 기공률을 실험과 견주는 모든 표에 **"AM 2차입자 내부 공극 (≈13.5 %, Heenan 2020 Fig. 7d 판독, n = 1) 을 실험 쪽이 기공으로 셌는가"** 한 줄 · 우리 ε_sphere 와의 차 어림 φ_AM × 0.135 (§7.3).

### ③ ★★ AM 파괴 분류의 보고 꼴
우리 분류 결과를 **입자 단위 7 범주 꼴** (미세균열 · 두 쪽 · 여러 쪽 · 섞임 · 산산조각) 로도 내 보면 실측 문헌과 같은 언어로 견줄 수 있다 (§7.4 — 대응은 해석 · 비준 대기 · 코드 변경 아님).

### ④ ★ 흐름 밖: 저해상 결함 검출
우리 랩 CT · SEM 에서 결함 AM 비율을 셀 때 **입자 안 회색값 분산** 을 대리 지표로 (Fig. 2d — 1200 nm 복셀에서도 구분) — 수백 입자 통계를 ≈2 h 스캔으로 (p.11).

### ⑤ ★ 함정 목록 (이 논문을 인용할 때)
'dislocation' = 1차입자 분리 (결정 전위 아님) · 'Raw' = 사이클 안 한 시트 입자 (원분말 아님) · 0.14 → 0.19 = 서로 다른 두 입자 · 결함 비율은 판정 해상도에 묶인다 (126 nm ↔ Wheatcroft 0.56 µm) · NMC811 σ_e 2.8 × 10⁻⁵ S/cm 는 출처 없음.

## 10. 인용 가능 문장 (deck / paper 용)

- *"X-ray nano-CT (126 nm voxels) of calendered commercial NMC811 cathode sheets showed that, before any electrochemical operation, about one third of the secondary particles were already defective (30.2 % and 34.2 % in two electrodes), with more than half defective at the electrode–separator side, which the authors attribute to calendering (Heenan et al., Adv. Energy Mater. 10, 2002655 (2020))."*
- *"The same study reports that raw NMC powders show minimal cracking before electrode fabrication (citing Heenan et al., Adv. Sci. 7, 2000362 (2020))."* — ⚠ 2차 인용임을 병기.
- *"At 32 nm resolution, an uncycled NMC811 secondary particle from the same calendered sheet was not fully dense (void fraction between primary particles ≈13.5 %, read from Fig. 7d), compared with ≈19.6 % for a different particle after five cycles to 4.5 V vs graphite."* — [판독] · 서로 다른 입자 · n = 1 병기.
- ⛔ 쓰지 말 문장: *"calendering induces dislocation glide / plastic deformation in NMC811 (Heenan 2020)"* (원문에 없음) · *"NMC811 particle porosity increased from 0.14 to 0.19 (Heenan 2020)"* 를 **같은 입자 · 인쇄 값** 처럼 · *"30 % of AM particles crack at 300 MPa"* (압력 미상 · 롤 캘린더링 · 액체계).

## 11. 주의 / 한계 (over-claim 방지) — 비판적으로

**A. 원문 내부 불일치 (대조로 드러난 것)**
1. **그림 S4 캡션 = *"prepared from Material 2 cycled to different upper cut-off voltages"*** (SI p.5) ↔ 본문: 사이클 시료는 *"the same batch as Sample 1"* (p.4) · *"Apart from Figure 1 … all other work was conducted on Material 1"* (p.12). S4 의 'Line' 측정 (4.2 V 54.6–57.33 · 4.5 V 51.46–60.59 · 단위 미기재) 은 µm 라면 Material 1 (≈30–40 µm) · Material 2 (≈70 µm) 어느 쪽 두께와도 맞지 않는다 — 단위 · 무엇을 잰 선인지 [미확인].
2. **복셀 표기**: 그림 2a 1.57 µm (캡션 · p.4) ↔ 1.6 µm (p.12) · 그림 2b 206 nm (캡션) ↔ 200 nm (p.4) ↔ 0.2 µm (p.12) — 반올림 차.
3. **그림 2d '200 nm voxels'** ↔ 본문 *"two particles were chosen from the high-resolution images displayed within Figure 1"* (그림 1 = 나노 CT **126 nm** · p.12).
4. **Table 1 Material 1 열 합 = 99.0 %** (상용 99.9 %) · 상용 열은 401 의 정수배와 정확히 맞는데 Material 1 열은 158 의 정수배가 아니다 (69.8 · 5.4 · 3.5) [카드 산술] — 계산법 미기재.
5. 'Sample 1' (p.4) ↔ 'Material 1' (나머지 전부) — 이름 혼용.
6. 그림 7 범례 **'Raw'** ↔ 본문 *"pristine state"* · Material 1 = 전극 시트 (원분말 아님).
7. r_I 는 **그림 6c 안에만** 정의 (I₀₀₆ + I₀₀₂)/I₁₀₁ · 본문 정의 · 인용 없음.
8. 그림 3e 등가 지름에 같은 값이 둘씩 (8.07 · 8.07 · 4.54 · 4.54) — 설명 없음 (우연일 수 있다).
9. SI 저자 목록: *"Alice Llewelyn"* (SI p.2) ↔ *"Alice Llewellyn"* (본문) · 저자 순서 다름 (SI: Wade · Parker · Matras · Leach · Tan … ↔ 본문: Wade · Tan · Parker · Matras · Leach …).
- 사소: 그림 4 캡션 *"refection"* (reflection 의 오기) · 그림 S6–S8 축 *"Flourescence"* · *"kEV"*.

**B. 해석의 한계**
10. **통계가 작다** — 그림 7 = 입자 둘 (서로 다른 입자) · 그림 3–6 = 일곱 (모두 4.5 V · 사이클 전 대조 없음) · 그림 2d = 둘 · 검정 없음. 저자 스스로 대표성에 수십–수백 입자가 필요하다고 씀 (p.10).
11. **결함 판정은 해상도 · 사람 판정에 묶인다** — 126 nm 보다 가는 균열은 '결함 없음' · 판정 문턱 · 판정자 [미확인].
12. **캘린더링 기원은 추정** — 압력 · 롤 조건 모름 (p.4) · 원분말 대조는 2차 인용 [18] · 분리막 쪽 = 롤 쪽은 *"most likely"* (p.4).
13. **박리 · 거시 균열은 시료 준비 탓으로 돌렸다** — 4.4 · 4.5 V 결론의 일부는 결합제 문제 (p.4).
14. 사이클은 **액체계 · 흑연 상대 · 0.5C/1C · 5 사이클** — ASSB 로 크기 전이 금지. 입자 떼는 방법 미기재.
15. XRF 정량 = 봉우리 넓이 비 (보정 없음) · 단일 입자 회절 통계 한계 (p.6) · H2/H3 · 암염 = 정성.
16. **역학이 없다** — 균열 기원 (팽창 · 수축 · 결정 방위 · 응력 봉우리) 은 전부 해석 · 힘 · 응력 · 강도 측정 0.

**C. 이 묶음 필수 넷 (CURATOR_BRIEF 2-5)**
- (i) **DEM 한계 문장**: 없음 — 이 논문은 DEM · 모델 계산을 하지 않는다 (*"말 없음"*). 가장 가까운 문장 = 입자 쌓임이 국소 응력 봉우리를 만든다는 **가설** (p.4).
- (ii) **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회**: 말 없음 · 계산 없음. 소성은 Al 집전체 항복 한 문장 (p.4).
- (iii) **2D / 3D**: 측정은 3D CT · 표시는 2D 직교 단면 · 그림 4 = 2D XRF 지도의 입자 평균 ↔ 그림 5 = XRF-CT (속 정보) — 2D → 3D 전이에 대한 원문의 말 없음.
- (iv) **탈압 거동**: 다루지 않음 (하중 · 압력 실험 없음).

**D. 카드 문제 (가리킨 카드 · 고치지 않음 — 정독 출력 batch_63 끝 절과 같은 내용)**
- **카드 문제 1** — `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md` L199 *"초기 사이클 입계 균열 · 캘린더링 중 전위 활주 | p. 1, p. 6 | [17] T. M. M. Heenan …"* — 뒤 절반 *"캘린더링 중 전위 활주"* 는 이 논문에 없다 (§0 ②).
- **카드 문제 2 (경미)** — `stallard2022_cathode_mechanical_properties_review.md` L92 (+ L284 · L376 · L459) *"NMC811 이차입자 기공 0.14 → 0.19 (5 사이클)"* — 리뷰 문장을 그대로 옮긴 것 (카드 잘못 아님) · 원문은 그림 판독 값 (≈13.5 → 19.6 %) · **서로 다른 두 입자** · 32 nm · 나노입자 경고 — 한정어가 빠졌다.

## 12. 논증 흐름 (절별)

1. **도입 (p.1–2)** — 차량 주행거리 = 양극 용량 · NMC811 의 장점과 고전압 열화 · 균열 전구 기전 (반자리 결함 · 층간 붕괴 · 용출 · 표면 상) · 원분말 균열 최소 [18] → 운전 전 전극의 제조 결함부터 결정까지 길이 척도를 따라 내려간다.
2. **2.1 제조 결함 (p.2–4 · 그림 1 · 표 1 · S1–S3)** — 7 범주 · 158 / 401 입자 · 결함 30.2 · 34.2 % · 내부 공극 = 합성 유래 · 상용 쪽 shatter · multi-prong 많음 (두꺼운 고로딩의 캘린더링 · 입자 쌓임 응력 봉우리 가설) · 입자가 Al 에 박힘 · 분리막 쪽 > 50 % → 운전 전 ⅓.
3. **2.2 전극 수준 (p.4 · 그림 2 · S4)** — 흑연 상대 5 사이클 · 4.2–4.5 V · 고전압 박리 (시료 준비 · 결합제) · 입자 속 회색값 하락 · 저해상 대리 지표.
4. **2.3 입자 수준 (p.5–9 · 그림 3–6)** — 7 입자 회색값 순 · 입경 무관 · Mn 변동 (≈83 : 7 : 9) · 균열 옆 Mn · 표면 Mn 덩어리 · Mn ↔ c · r_I 상관 · 균열과는 단절.
5. **1차입자 (p.9–11 · 그림 7)** — 32 nm · 둘 다 치밀 아님 · 통로 2 → 8 µm · 공극 중심 수렴 · 붙은 1차입자 분리 (≈1 µm → 600 nm) · 해상도 · 대표성 한계 · 결정 방위가 응력 · 균열을 지배할 수 있음 (NMC111 과 같은 꼴).
6. **결론 (p.11–12)** — 제조 (캘린더링) 결함 ⅓ · 분리막 쪽 · 고전압 결합제 열화 · 저해상 결함 검출 · Mn 은 결정 열화와, 균열은 1차입자 경계 분리 (팽창 · 수축 · 결정 방위) 와 엮인다.

## 13. 용어 미니 사전

- **2차입자 / 1차입자**: 공침 NMC 의 수–십수 µm 응집체 / 그 안의 ≈0.5–1.5 µm 결정립 (이 논문 측정 ≈1 µm).
- **붙은 (fused) 1차입자**: 경계를 32 nm 해상도로 가를 수 없을 만큼 붙은 두 1차입자 — 하나로 셌다.
- **Bisect · Multi-prong · Prong & shatter · Shatter**: Table 1 의 쪼개짐 범주 (두 쪽 · 여러 쪽 · 큰 균열 + 미세균열 · 1차입자 크기 조각).
- **나노 CT (영역판)**: 실험실 X 선 현미경 (Zeiss 810 Ultra) — 영역판 (zone plate) 으로 초점 · 복셀 수십–백수십 nm.
- **복셀 (voxel)**: 3D 영상의 최소 부피 단위 (등방 복셀 길이로 해상도를 말한다).
- **부분 평균 (partial averaging)**: 복셀보다 작은 공극 · 균열이 섞여 그 복셀의 회색값이 낮아지는 효과 — 이 논문의 저해상 결함 대리 지표의 원리.
- **top-hat 분할**: 국소 배경보다 밝은 (또는 어두운) 작은 구조를 뽑는 형태학적 필터 분할.
- **XRF / XRD 나노프로브**: 50 nm 빔으로 형광 (원소) · 회절 (결정 구조) 을 동시에 재는 싱크로트론 측정.
- **r_I (R 인자 류)**: 층상 구조 정렬 지표 — 이 논문 정의 (I₀₀₆ + I₀₀₂)/I₁₀₁ (그림 6c) · 작을수록 육방 정렬이 좋다 (그림 6c 화살표).
- **H2/H3 · 암염 (rock-salt)**: 고 SoC 상 · 표면 재구성 상 (여기선 정성).
- **dislocation (이 논문의 뜻)**: *"the cracking and separation of primary particles"* — 결정 전위가 아니다.

## 14. 참고문헌 — 우리가 더 볼 것 (원문 목록 그대로 · 정본 카드 유무 = `papers/` 파일 목록 + grep)

| 번호 | 서지 (원문 목록 그대로) | 왜 | 카드 |
|---|---|---|---|
| [18] | T. M. Heenan, A. V. Llewellyn, A. S. Leach, M. D. Kok, C. Tan, R. Jervis, D. J. Brett, P. R. Shearing, *Adv. Sci.* **2020**, *7*, 2000362. | ★ 원분말 (전극 제조 전) 결함 · 균열 최소 · 내부 공극의 원전 — 조건 R7 의 '압밀 전 무손상' 근거 (이 논문은 2차 인용) | 없음 |
| [32] | T. M. M. Heenan, A. Jnawali, M. Kok, T. G. Tranter, C. Tan, A. Dimitrijevic, R. Jervis, D. J. L. Brett, P. R. Shearing, *Data Brief* **2020**, *32*, 106033. | ★ Material 2 (LG MJ1) 영상 원자료 공개 — 흐름 밖: 실측 3D 양극 구조 (AM 결함 · 패킹) 를 우리 DEM 대조에 | 없음 |
| [28] | A. Quinn, H. Moutinho, F. Usseglio-Viretta, A. Verma, K. Smith, M. Keyser, D. P. Finegan, *Cell Rep. Phys. Sci.* **2020**, *1*, 100137. | 결정 방위가 균열을 지배한다는 근거 (p.11) — R7 기전 | 없음 (`sharma2023_…` 가 인용만) |
| [17] | P. C. Tsai, B. Wen, M. Wolfman, M. J. Choe, M. S. Pan, L. Su, K. Thornton, J. Cabana, Y. M. Chiang, *Energy Environ. Sci.* **2018**, *11*, 860. | 단일 입자 나노 CT 2차입자 균열 (낮은 Ni NMC) — 이 논문이 비교한 원전 | 없음 (`lee2024_…` 가 다른 용도로 인용) |
| [23] | Y. Mao, X. Wang, S. Xia, K. Zhang, C. Wei, S. Bak, Z. Shadike, X. Liu, Y. Yang, R. Xu, P. Pianetta, *Adv. Funct. Mater.* **2019**, *29*, 1900247. | 내부 공극의 응력 완화 이점 — AM 내부 공극 · 역학 | 없음 |
| [16] | S. R. Daemi, C. Tan, A. Vamvakeros, T. M. Heenan, D. P. Finegan, M. Di Michiel, A. M. Beale, J. Cookson, E. Petrucco, J. S. Weaving, S. Jacques, *Phys. Chem. Chem. Phys.* **2020**, *22*, 17814. | 4D XRD-CT — '제조 결함 이해에 4D' (p.4) | 없음 |
| [19] | Q. Lin, W. Guan, J. Zhou, J. Meng, W. Huang, T. Chen, Q. Gao, X. Wei, Y. Zeng, J. Li, Z. Zhang, *Nano Energy* **2020**, *76*, 105021. | 'dislocation of primary particles' 문장의 근거 (Ni–Li 반자리 결함 → 입계 균열) | 없음 |
| [20] | K. Märker, P. J. Reeves, C. Xu, K. J. Griffith, C. P. Grey, *Chem. Mater.* **2019**, *31*, 2545. | 층간 간격 · SoC (A10 격자 변화) — `stallard2022_nmc811_single_crystal_…` §12 도 인용 (목록 연도 2017 로 표기) | 없음 |
| [31] | Z. Xu, M. M. Rahman, L. Mu, Y. Liu, F. Lin, *J. Mater. Chem. A* **2018**, *6*, 21859. | NMC111 전압 유도 균열 꼴 (NMC811 과 비교) | 없음 |

## 15. 🧮 파생 계산 원장 ([카드 산술] — 판독 = `digitized.csv`)

| # | 계산 | 결과 | 비고 |
|---|---|---|---|
| D1 | Table 1 합 | Material 1 **99.0** · 상용 **99.9** % | 원문 불일치 (§11-A4) |
| D2 | 결함 = 100 − 결함 없음 | **30.2 · 34.2** % (차 4.0 %p) | 본문 '≈4 %' ✓ |
| D3 | 균열 다섯 범주 합 · 쪼개짐급 넷 합 | 26.0 · 33.9 % / 18.4 · 24.7 % | §7.2 |
| D4 | 상용 k/401 | 264 · 1 · 37 · 28 · 33 · 10 · 28 (합 401) | 정수배 정확 |
| D5 | Material 1 × 158 | 110.3 · 5.06 · 12.0 · 9.95 · 8.53 · 5.53 · 5.06 | 69.8 · 5.4 · 3.5 정수 아님 |
| D6 | Fig. 1c 열 단순 평균 · S3b Material 2 평균 | 30.8 % · 35.1 % | 표 30.2 · 34.2 와 0.6 · 0.9 %p — '깊이 칸 평균' 가설 (미확인) |
| D7 | 비 | shatter 7.0/3.2 = 2.19 · 내부 공극 3.2/0.2 = 16 | 본문 서술 ✓ |
| D8 | Fig. 7c 평균 | Raw 13.53 · 4.5 V 19.49 % | 7d 막대 13.5 · 19.6 과 같음 |
| D9 | 공극 증가 | +6.1 %p · × 1.45 | Fig. 7d |
| D10 | 1차입자 점선 비 | 660/1080 = 0.61 | 본문 ≈1 µm → 600 nm (0.6) |
| D11 | 입자 내부 공극이 전극 기공에 더할 몫 φ × 0.135 | φ 0.5 · 0.6 · 0.7 → 6.8 · 8.1 · 9.5 %p | 가정 = 실험이 결정 진밀도 기준 (§7.3) |
| D12 | Stallard 0.19 ↔ 판독 19.6 % | 차 0.6 %p (판독 분해능 0.07 %p) | 0.14 ↔ 13.5 % 는 반올림 범위 |
| D13 | 전극 두께 (그림 축) | Material 1 ≈33 µm · Material 2 ≈70 µm | 본문 Material 1 ≈30–40 µm |

## 16. [미확인] 목록

- 캘린더링 압력 · 선하중 · 롤 간격 · 시트 밀도 · 시트 기공률 (두 재료 모두 — *"not known to the authors"*).
- Material 1 시트 조성 (활물질 · 결합제 · 탄소 비) · Material 1 자료 공개 여부.
- 결함 범주 판정 문턱 · 판정자 · Table 1 의 Material 1 비율 계산법 (깊이 칸 평균인가).
- 원분말 자체의 공극 · 결함 비율 (이 논문은 [18] 로만 말함).
- 그림 S4 시료 (Material 1 ↔ 2) · 'Line' 값의 단위 · 대상.
- 그림 7f 의 '143 nm ±30 %' · '250 nm ±7 %' 의 뜻.
- r_I 정의의 출처 · 첨자 (002).
- 입자 떼기 (extraction) 방법 · 코인셀 형식.
- NMC811 σ_e 2.8 × 10⁻⁵ S/cm · D_Li 10⁻⁸–10⁻⁹ cm²/s 의 출처 (원문에 인용 번호 없음).
- Wheatcroft 2023 원문이 [17] 을 인용한 문장 그대로 (이 트리에 PDF 없음) — 카드 문제 1 의 뿌리.

## 🔗 관련 카드

- `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` — 이 논문을 [17] 로 인용 (L199 = 카드 문제 1) · 같은 NMC811 2차입자의 **분할 하중** (무압연 전극 · XCT 0.56 µm 균열 0.7 %) ↔ 이 논문의 **캘린더링 뒤 결함 비율** (126 nm · 30 %).
- `stallard2022_cathode_mechanical_properties_review` — 이 논문을 [121] 로 인용 (L92 0.14 → 0.19 = 카드 문제 2 · 경미) · 입자 내부 기공 질문 (§9-5) 의 1 차 자료가 이 카드 §7.3.
- `stallard2022_nmc811_single_crystal_shear_strength_lithiation` — 이 논문을 [5] 로 인용 · 단결정 슬립 (AM 소성의 근거는 그쪽).
- `intergranular_cracking_nmc811_jmca2023` — 같은 그룹 (UCL · Heenan 공저 · 2023) 의 나노 CT 입계 균열 직접 관찰 (전기화학 유도).
- `lu2020_insitu_nanoct_calendering_microstructural_evolution` — 같은 그룹 · 같은 해 (Lu 외 · *Joule* 2020) · 나노 CT 안에서 누른 채 캘린더링 모사 (NMC111) — 이 논문의 '캘린더링 유래 결함' 을 공정 중에 본 쪽.
- `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` — 캘린더링 중 AM 파쇄를 in situ CT + DEM 명목 응력으로 (위험 입자 비율 0.2 → 20.31 %) — 이 논문 결함 비율과 같은 꼴의 계산 쪽.
- `dang2019_nmc111_secondary_particle_flat_punch_fracture_strength` — 2차입자 낱알 압괴 강도 (NMC111 · 평판).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
