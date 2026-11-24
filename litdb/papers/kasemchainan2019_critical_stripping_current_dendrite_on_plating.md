<!-- digest 표준 양식 (paper-level STANDALONE) — 2026-11-24 litdb-curator (배치 2026-11-24b #10 · 병렬 실행 · 공유 파일 (INDEX · comparison · pdf_map) 은 메인 세션이 합친다).
     그림 크롭 13 장 (본문 그림 6 + SI 그림 7): 도구 그대로 6 장 (Fig. 3 · S2 · S4 · S5 · S6 · S7) · 손작업 7 장 = Fig. 4 손 크롭 (도구 '영역 없음' — 벡터 도식) + 다시 자름 6 장
     (Fig. 1 · Fig. 2 · Fig. 5 = 위쪽 판 라벨 · 눈금 잘림 / Fig. 6 = c·d 아래 띠만 / Fig. S3 = e·f 한 줄만 / Fig. S1 = 위 글자 섞임). 사유는 figures.json `recrop` · `manual_crop`.
     13 장 중 12 장을 크롭으로 열어 봤다 · Fig. S1 (XRD) 만 SI 쪽 렌더로 봤다. 판독값 49 행 = litdb/figures/<slug>/digitized.csv.
     값 표지: 본문 숫자 = 쪽 병기 · 그림에서만 읽은 값 = 'figure-read ≈' · 논문 숫자로 우리가 계산한 값 = '✎ 우리 산수' · 해석 = '[우리 해석]'.
     쪽 표기 = 저널 쪽 1105–1111 (Methods 는 온라인 전용 쪽이라 'Methods' 로 적는다) · SI 쪽 = SI PDF 쪽 (p.1 표지 · p.2 Fig. S1 … p.8 Fig. S7).
     우리 점착 (W) 값은 싣지 않는다 — 위치만 (`db/properties/adhesion.json` · W_ad 보고서 2 절). -->

# Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells — Kasemchainan, Zekoll, Spencer Jolly, Ning, Hartley, Marrow & Bruce (*Nat. Mater.* 18, 1105–1111 (2019))

> slug `kasemchainan2019_critical_stripping_current_dendrite_on_plating` · DOI `10.1038/s41563-019-0438-9` · type `exp (Li|Li₆PS₅Cl|Li 2 · 3 전극 대칭셀 · 스프링 클램프 적층압 0.5 / 3 / 7 MPa · 정전류 사이클 + 단일 도금 · 박리 계단 · ex situ SEM 단면 · in situ XCT · EIS · XPS · Na|Na-β″-alumina 대조) — DFT · MD · 연속체 수치해석 없음` · PDF `litdb/inbox/kasemchainan2019_critical_stripping_current_main.pdf` (본문 8 pp) + `litdb/inbox/kasemchainan2019_critical_stripping_current_SI.pdf` (SI 8 pp — Fig. S1–S7) · digested `2026-11-24` · status ✅ · 태그 **[외부]**
> elements: Li, P, S, Cl, Na
> methods: XPS

> **저자**: Jitti Kasemchainan ¹ ² · Stefanie Zekoll ¹ ² · Dominic Spencer Jolly ¹ · Ziyang Ning ¹ · Gareth O. Hartley ¹ · James Marrow ¹ · **Peter G. Bruce\*** ¹ ² ³ (교신 · peter.bruce@materials.ox.ac.uk) — ¹ Department of Materials, University of Oxford · ² The Faraday Institution (Harwell Campus, Didcot) · ³ Department of Chemistry, University of Oxford
> 접수 2019-02-04 · 수락 2019-06-18 · 온라인 2019-07-29 · 권호 2019-10 · 자금 Faraday Institution (FIRG007 · FIRG008) · EPSRC (SUPERGEN Energy Storage Hub EP/L019469/1 · Enabling Next Generation Lithium Batteries EP/M009521/1 · 장비 EP/M02833X/1) · Henry Royce Institute (EP/R010145/1) · 이해상충 없음 · 기여: J.K. 전 과정 · S.Z. SEM · D.S.J. 전기화학 · Z.N. Li₆PS₅Cl 합성 + in situ XCT · 집필 · 지도 P.G.B. · 자료 Oxford Research Archive DOI `10.5287/bodleian:gA47ppAz9` (안 받아 봤다).
>
> **litdb 이웃 (링크만)**: [`wang2019_li_se_interface_dynamics_stack_pressure_current_density`](wang2019_li_se_interface_dynamics_stack_pressure_current_density.md) (같은 질문 · 가넷) · [`masias2019_li_metal_elastic_plastic_creep_properties`](masias2019_li_metal_elastic_plastic_creep_properties.md) (Li 항복 · 크리프 — 이 논문 ref 38) · [`seymour2021_void_suppression_interfacial_adhesion_vacancy_transport`](seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md) (W ≥ 2σ 공극 문턱) · [`fuchs2023_cu_llzo_anode_free_li_growth_modes`](fuchs2023_cu_llzo_anode_free_li_growth_modes.md) · [`sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance`](sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance.md) (이 논문 ref 14)
> **LPSCl 쪽 이웃**: [`shi2026_argyrodite_stack_pressure_viscoplastic_deformation`](shi2026_argyrodite_stack_pressure_viscoplastic_deformation.md) · [`kim2026_operando_void_detection_single_frequency_impedance`](kim2026_operando_void_detection_single_frequency_impedance.md) · [`tron2023_lpscl_ccd_ambient_pressure`](tron2023_lpscl_ccd_ambient_pressure.md) · [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) · 개념 이웃 [`chatterjee2025_diffuse_interface_metal_anode_void_model`](chatterjee2025_diffuse_interface_metal_anode_void_model.md) · [`yang2021_atomistic_li_stripping_plating_interface_md`](yang2021_atomistic_li_stripping_plating_interface_md.md)

> **본 digest 에서 실제로 본 그림 (2026-11-24)**: 크롭으로 하나씩 연 것 **12 장** — `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` · `Fig. S2` `Fig. S3` `Fig. S4` `Fig. S5` `Fig. S6` `Fig. S7`.
> 크롭을 안 연 것: `Fig. S1` (XRD) — SI 쪽 렌더 (첫 훑기) 로만 봤다. 본문 8 쪽 · SI 8 쪽은 전부 쪽 렌더로도 읽었다.
> 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했고 (±1–2 mV 정도), 숫자 전부가 `digitized.csv` 에 있다.

---

## 0. 이 digest 를 읽는 법

읽기 축 셋:
1. **W_ad 보고서 8-1 (문턱) · 8-4 (공극 · 적층압 · 균열)** — 이 논문은 점착을 재지 않는다. 대신 *"Li | Li₆PS₅Cl 셀에서 먼저 무너지는 것은 박리 쪽이고, 박리 공극이 다음 도금의 덴드라이트를 부른다"* 는 실패 순서를 준다 → 8-1 의 '공극을 막는다' 문턱이 셀에서 드러나는 양은 **박리 임계 전류 (CCS)** 다 (§7b).
2. **DEM · 연속체 눈금** — 압력 · 접촉 면적 · 공극 분율이 숫자로 없다. '크리프가 공극을 메우는 속도' 를 DEM 접촉 모형과 같은 눈금에 놓을 수 있나 → **이 논문 숫자만으로는 못 놓는다** · 이유 여섯과 쓸 수 있는 변환 셋 (§7c).
3. **CCS 숫자의 정의** — 아래 상자. 이걸 놓치면 숫자를 한 계단 틀리게 옮긴다.

> ⚠⚠ **CCS 숫자가 논문 안에 두 벌 있다.**
> · 초록 · 서론 (p.1105): *"0.2 and 1.0 mA cm⁻² at 3 and 7 MPa"* = **공극 · 덴드라이트 없이 돈 가장 높은 시험 전류** (2 전극 100 사이클로 확인 — `Fig. 6a` · `Fig. 6c`).
> · 2 전극 절 (p.1109): *"cycled below and above the CCS thresholds of 1.0 mA cm⁻² at 3 MPa and 2.0 mA cm⁻² at 7 MPa"* · `Fig. 5` 서술 (p.1108): *"severe at 1.0"* · *"threshold is higher at 2.0"* = **처음 실패한 시험 전류**.
> ⇒ 문턱 자체는 그 사이다: **3 MPa 0.2 < CCS ≤ 1.0 · 7 MPa 1.0 < CCS ≤ 2.0 mA cm⁻²**. 도금 쪽도 같은 꼴이다: **2.0 < CCP ≤ 3.0** (두 압력 같음).
> ⚠ **조건마다 셀 하나 · 오차 막대 · 반복 없음.** SE 펠릿의 밀도 · 두께 · 이온전도도와 **운전 온도는 미기재**다 (EIS 에만 −1 °C · 25 °C).

---

## 1. 한 줄 요약

Li | Li₆PS₅Cl | Li 3 전극 셀로 도금과 박리를 갈라 보니 **박리 쪽 임계 전류 (CCS) 가 도금 쪽 (CCP) 보다 낮았다.** CCS 를 넘겨 벗기면 Li 쪽 계면에 공극이 생기고, 도금이 그 공극을 일부만 가두며 메워서 공극이 사이클마다 쌓인다 → 접촉 면적이 줄어 국부 전류가 오르고 → **전체 전류가 CCP 보다 낮아도 결국 도금 때 덴드라이트로 단락**된다. 적층압을 3 → 7 MPa 로 올리면 CCS 가 오르고 (안전 전류 0.2 → 1.0 · 실패 전류 1.0 → 2.0 mA cm⁻²) CCP (2.0) 는 그대로라서, 저자는 Li 공급이 확산보다 **크리프** 로 이뤄진다고 결론짓는다 — 다만 그 판정은 압력 의존 하나에 기대고 정량 비교는 없다 (§10-⑤).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | **Li \| Li₆PS₅Cl \| Li** (자체 합성 · 소결 펠릿 ⌀5 mm · Li ⌀2 mm × 40 µm) · 대조 **Na \| Na-β″-alumina \| Na** (Ionotec ⌀10 mm · SI `Fig. S7`) |
| 동기 (p.1105) | 99 % 치밀 세라믹도 도금 덴드라이트로 단락 (refs 2–12) · LLZO 의 덴드라이트 전류 *"can be as low as 0.6 mA cm⁻²"* (refs 6 · 13–15) · 박리 중 공극으로 접촉 상실 (refs 16–24) · **2 전극 셀로는 도금과 박리를 가를 수 없다** (refs 22 · 25) · 한쪽 극을 고압 성형한 2 전극 셀 연구 (ref 26) 가 박리 분극에서 공극 역할을 짚었다 |
| 왜 argyrodite (p.1105) | 황화물이 산화물보다 전도도가 높고 여러 회사가 상용화에 쓴다 (refs 27–30) · 다른 고전도 황화물보다 **덜 깨진다** (ref 31 — DFT 탄성) · Li 와 **동역학적으로 안정한 계면** (이 논문 XPS) |
| 던지는 질문 | ① 박리 · 도금 각각에 임계 전류가 있나 ② 박리 공극이 도금 덴드라이트로 어떻게 이어지나 ③ 적층압은 무엇을 바꾸나 ④ 계면으로 Li 를 대는 것은 확산인가 크리프인가 |
| 이 논문의 답 | ① 있다 — **CCS < CCP** ② 공극 누적 → 접촉 ↓ → 국부 전류 ↑ → 도금 덴드라이트 ③ 압력이 CCS 를 올리고 CCP 는 안 바꾼다 ④ 크리프 (압력 의존이 근거 · 첫 박리에선 확산도 거든다) |
| 연구 유형 | 실험만 (전기화학 · 현미경 · 분광) — 계산 0 |

**계보 (이 논문 참고문헌 기준)**:
- 공극 · 박리 쪽 선행: ref 22 Koshikawa et al. 2018 *J. Power Sources* 376, 147 (LLZO 계면 Li 용해/석출 중 R_ct 변화) · ref 26 Krauskopf, Hartmann, Zeier & Janek 2019 *ACS Appl. Mater. Interfaces* 11, 14463 (LLZO · 박리 공극 · 고압 성형 기준극).
- Li 공급 · 역학: ref 36 Wang, Wolfenstine & Sakamoto 2019 *Electrochim. Acta* 296, 842 (Li|LLZO 온도 의존 flux balance — 공급 유속 = 확산 + 크리프) · ref 38 Masias, Felten, Garcia-Mendez, Wolfenstine & Sakamoto 2019 *J. Mater. Sci.* 54, 2585 (Li 항복 0.81 MPa · litdb `masias2019_…`) · ref 37 Nemat-Nasser & Hori 1987 *J. Appl. Phys.* 62, 2746 (항복 위에서도 공극이 타원체로 남는다).
- Li | 황화물 반응: refs 33–35 Wenzel et al. 2018 *Solid State Ionics* 318, 102 · Wu et al. 2018 *ACS AMI* 10, 10076 · Zhu, He & Mo 2015 *ACS AMI* 7, 23685 (litdb `zhu2015_esw_grand_potential_origin`).
- LLZO CCD 쪽: refs 13 · 14 Sharafi et al. 2017 (*J. Mater. Chem. A* 5, 21491 · *Chem. Mater.* 29, 7961 — 뒤의 것이 litdb `sharafi2017_…`).
- 후속 (같은 그룹 · 이 digest 에서 본문 안 봄): Spencer Jolly et al. 2020 *ACS AMI* 12, 678 (Na | Na-β″-alumina 압력 · 공극 — 본문 p.1110 이 예고한 '더 자세한 Na 연구') · Spencer Jolly et al. 2021 *ACS AMI* 13, 22708 (argyrodite 공극의 온도 의존 — Crossref 로 서지 확인) · Ning et al. 2021 *Nat. Mater.* 20, 1121 · Ning et al. 2023 *Nature* 618, 287 (Ning = 이 논문 4 저자).

---

## 3. 핵심 수치 총정리 ★

### 3a. 셀 · 재료 (Methods · p.1105 · p.1106)

| 항목 | 값 | 출처 |
|---|---|---|
| Li₆PS₅Cl 합성 | Li₂S · P₂S₅ · LiCl (Sigma-Aldrich) 화학량론 · 1 g + ZrO₂ 볼 (⌀10 mm) 50 g · 두 병 · Fritsch PULVERISETTE 7 premium line **600 rpm · 14 h** → ⌀5 mm 다이 1 t 성형 → 흑연 포일로 감싸 진공 석영관 봉입 → **예열 600 °C · 15 min** → 식혀서 갈아 → ⌀5 mm 1 t 재성형 → 봉입 → **300 °C · 15 min** (소결) → 1200 grit SiC 연마 · Ar 글러브박스 (O₂ · H₂O < 1 ppm) | Methods |
| 성형압 | 본문 *"cold pressing the powder at 500 MPa"* · 진공 < 10⁻⁵ mbar (p.1105) · ✎ 1 t / ⌀5 mm = 499 MPa (같다) | p.1105 · Methods |
| 상 확인 | 분말 XRD (Rigaku SmartLab · Cu Kα₁ · Kapton 밀봉 · 10–70° · 0.01° · 실온) — 아지로다이트 입방 피크 (`Fig. S1` 은 15–60° 만 그림) · 리트벨트 · 불순물 분석 없음 | Methods · `Fig. S1` |
| **펠릿 밀도 · 두께 · 이온전도도** | **미기재** (n/a) — 지름 5 mm 만 | — |
| Li 전극 | 200 µm 박 · 칼로 표면층 제거 · ⌀5 mm 를 **10 t** 로 눌러 **40 µm** → ⌀2 mm 원판 둘을 펠릿 양면에 동심으로 압착 (압착 하중 미기재) · ✎ 10 t / ⌀5 mm = 4.99 GPa (명목 · 처음 지름 기준 — 눌리며 퍼지므로 실제는 낮다) | Methods |
| 3 전극 | ⌀0.5 mm Li 기준극을 작업극 **옆 (같은 면)** 에 (`Fig. 1a`) | Methods · `Fig. 1a` |
| 전극 면적 | ✎ π (0.1 cm)² = 0.0314 cm² → 1.0 mA cm⁻² = 31.4 µA | ✎ |
| 패키지 · 압력 | 진공 밀봉 파우치 · Cu 박 집전체 · **스프링 클램프** · 압전 로드셀 (OMEGA) 로 **맞추고 쟀다** · Methods 는 **3 · 7 MPa** 만 (본문 · `Fig. S5` 에 **0.5 MPa** 도 있다) · XCT 셀은 Deben CT5000 하중 장치 (3 MPa) | Methods · p.1108 · `Fig. 3` |
| ⚠ 압력의 기준 면적 | **미기재** — Li ⌀2 mm 면적이면 3 MPa = ✎ 9.4 N · SE ⌀5 mm 면적이면 ✎ 59 N (**6.25 배**) | ✎ |
| 운전 온도 | **미기재** (사이클 · 계단 시험) · EIS 시간 변화만 25 °C · 4 성분 Nyquist 는 −1 °C (`Fig. S2`) | `Fig. S2` 캡션 |
| 사이클 용량 | 반주기 **1.0 mAh cm⁻²** (≈5 µm Li · ✎ 4.85 µm) · Gamry Interface-1000 · 단일 계단 (`Fig. 5`) 은 도금 1.0 · 박리 2.0 mAh cm⁻² 까지 | Methods · `Fig. 5` |
| 휴지 | Methods 무언급 · `Fig. S4` 에 반주기 사이 **0 mV 구간 figure-read ≈ 0.45 h** | `Fig. S4` |
| EIS | 2 전극만 · 5 mV · 1 MHz–1 Hz · ZView · 회로 R0 + (R1‖CPE1) + (R2‖CPE2) + (R3‖CPE3) = bulk · GB · SEI · CT (`Fig. S2a`) | Methods · `Fig. S2` |

### 3b. ★★ CCS · CCP — 적층압별 (정의 · 판정 · 반복 · 오차)

| 적층압 | CCS — 초록 · 서론 값 (p.1105) = 안전하게 돈 값 | CCS — 본문 'threshold' (p.1108 · p.1109) = 처음 실패한 값 | ✎ 시험값 괄호 | [우리 해석] `Fig. 5` 판독으로 좁힌 괄호 | CCP (p.1105 · p.1108) | 셀 · 오차 |
|---|---|---|---|---|---|---|
| **0.5 MPa** (< Li 항복 0.81) | — | 1.0 에서 빨리 실패 (`Fig. S5`) | CCS < 1.0 | — | — | 셀 1 · 없음 |
| **3 MPa** | **0.2** (2 전극 100 사이클 `Fig. 6a`) | **1.0** (*"severe"* `Fig. 5c` · 3 전극 `Fig. 1b` 8 번째 단락 · 2 전극 `Fig. 6b` 단락) | **0.2 < CCS ≤ 1.0** | 0.5 < CCS < 1.0 | **2.0** (3.0 에서 분극 감소 · 4.0 은 figure-read ≈0.47 mAh cm⁻² 에서 단락 `Fig. 5a`) → **2.0 < CCP ≤ 3.0** | 조건마다 셀 1 · 오차 없음 |
| **7 MPa** | **1.0** (3 전극 100 사이클 `Fig. 1c` · 2 전극 100 사이클 `Fig. 6c`) | **2.0** (*"threshold is higher at 2.0"* `Fig. 5d` · 3 전극 `Fig. 1d` 10 번째 · 2 전극 `Fig. 6d` 10 번째 단락) | **1.0 < CCS ≤ 2.0** | 1.0 < CCS < 1.5 | **2.0** (`Fig. 5b` 3.0 · 4.0 분극 감소) → **2.0 < CCP ≤ 3.0** | 조건마다 셀 1 · 오차 없음 |
| Na \| β″-alumina · 4 MPa | (숫자로 안 적음) | (숫자로 안 적음) | `Fig. S7a`: 0.5 평탄 · 1.0 상승 → **0.5 < CCS ≤ 1.0** | — | — | 셀 1 |

**정의 · 판정 (논문 그대로)**:
- **CCS** (p.1108): *"the current density above which Li is stripped faster than it is replenished at the Li/SE interface, resulting in void formation."* 재는 법 = 3 전극 **단일 박리** (`Fig. 5c,d` · 2.0 mAh cm⁻² 까지) 의 분극이 전하와 함께 오르나 · 확인 = 2 전극 사이클 (`Fig. 6`). **수치 판정 기준 (dV/dQ 문턱 · 상대 상승률 등) 은 없다** — *"severe"* · *"threshold"* 같은 말뿐.
- **CCP** (p.1108): *"overall current densities on plating up to 2.0 mA cm⁻² are possible, but 3.0 mA cm⁻² shows a reduction in polarization with charge passed characteristic of dendrite formation"* — 판정 = 도금 분극의 크기가 전하와 함께 **줄면** 덴드라이트 (면적 증가 · 부분 단락) · 수치 기준 없음.
- **단락**: |V| 가 갑자기 0 쪽으로 떨어짐 (`Fig. 1b` 8 번째 · `Fig. 5a` 4.0 · `Fig. 6b` 8 번째 · `Fig. 6d` 10 번째).
- **용량 의존**: 계단 시험은 박리 2.0 mAh cm⁻² (✎ 9.7 µm) · 사이클은 1.0 — CCS 는 '속도' 로 정의됐지만 **잰 값은 정해진 용량 창 안의 값**이다.
- [우리 해석] `Fig. 5c,d` 의 첫 1 mAh cm⁻² 안 상대 상승을 같은 잣대로 보면 (figure-read · digitized.csv): 3 MPa 0.5 ≈ +14 % · 1.0 ≈ +47 % / 7 MPa 1.0 ≈ +9 % · 1.5 ≈ +34 % · 2.0 ≈ +32 % (2.0 은 1 mAh 뒤에 폭주). **저자가 '아래' 로 둔 7 MPa 1.0 (+9 %) 과 3 MPa 0.5 (+14 %) 가 비슷하다** → 3 MPa 의 '0.2' 는 보수적인 값이고 (0.5 는 2 전극으로 안 돌렸다), 같은 잣대면 괄호가 3 MPa (0.5, 1.0) · 7 MPa (1.0, 1.5) 로 좁아진다. 판독 오차 (±1–2 mV / 7 mV) 가 커서 정량 입력은 아니다.

### 3c. 3 전극 사이클 (`Fig. 1` · p.1106 · p.1108)

| 조건 | 결과 (본문) | figure-read ≈ (우리 판독) |
|---|---|---|
| **3 MPa · 1.0 mA cm⁻²** (`Fig. 1b`) | 첫 도금 **12 mV** 평탄 · 첫 박리 끝 **19 mV** · 7 번째 박리 끝 **130 mV** · 도금 평균 **13 mV** · **8 번째 사이클 단락** (p.1106) | 2–6 번째 박리 끝 ≈25 · 31 · 40 · 58 · 102 mV (범례가 2–6 을 한 색으로 묶어 순서는 값 순으로 둠) · 도금 −12 ~ −17 mV · 8 번째 도금 ≈0.43 mAh cm⁻² 에서 ≈−20 → ≈−3 mV |
| **7 MPa · 1.0** (`Fig. 1c` · 100 사이클) | 분극이 전하 · 사이클에 거의 무관 (p.1108) | 박리 ≈+9 → +8 · 도금 ≈−9 mV |
| **7 MPa · 2.0** (`Fig. 1d`) | 첫 박리 약간 상승 (일부 공극) · 처음 몇 사이클 박리 분극 증가 · 그 뒤 **도금 분극이 첫 도금보다 작아지고** 박리 시작 분극도 첫 박리보다 낮아짐 · 9 번째 도금 끝 SEM 에 덴드라이트 · **10 번째 뒤 단락** (p.1108) | 박리 끝 1 · 2 · 3 · 4 · 6 · 9 번째 ≈22.5 · 25 · 29 · 34 · 36 · 38 mV · 도금 1 번째 ≈−19.5 평탄 → 6 · 9 번째 ≈−33 / −30 → −9 · 10 번째 ≈−10 → −2 (바늘) |
| **3 MPa · 1.0 · WE / CE 동시** (`Fig. S4`) | 첫 반주기 CE (박리) 분극 상승 · 그 뒤 **CE 분극이 WE 보다 약간 큼** (공극이 더 많다는 해석) (p.1108) | WE 박리 끝 ≈16–18 · CE ≈20–22 mV (4 사이클) · 반주기 사이 0 mV ≈0.45 h |
| **0.5 MPa · 1.0** (`Fig. S5`) | 셀 만들기도 어려움 · 첫 사이클부터 분극 감소 (접촉 개선 **+** 덴드라이트) · 다음 박리 분극 큼 · 빨리 실패 · 마지막 박리 뒤 Li 가 심하게 떨어짐 (p.1108) | 박리 끝 1 · 2 번째 ≈75 · 95–100 mV · 3 번째 ≈+12 → +25 / −35 → −15 mV |

### 3d. 2 전극 사이클 (`Fig. 6` · p.1109–1110)

| 조건 | 결과 (본문) | figure-read ≈ · ✎ |
|---|---|---|
| 3 MPa · **0.2** | 100 사이클 · 분극 거의 불변 | ±7 mV → ✎ ASR ≈35 Ω cm² |
| 3 MPa · **1.0** | 분극이 오르다 단락 | 1 번째 +35 / −25 → −38 mV (✎ ≈35 Ω cm²) · 6 · 7 번째 박리 시작 ≈100 · 112 mV · 아래 가지 끝 ≈−138 · < −160 mV · 8 번째 ≈0.34 mAh cm⁻² 에서 −28 → −15 mV (단락) |
| 7 MPa · **1.0** | 100 사이클 · 분극 변화 없음 | ±18 mV → ✎ ≈18 Ω cm² |
| 7 MPa · **2.0** | 덴드라이트 · 실패 | 1 번째 +42 / −40 · 9 번째 +73 / −65 mV · 10 번째 ≈0.92 mAh cm⁻² 에서 −54 → 0 mV (단락) |

> ✎ 7 MPa 셀의 총 ASR (≈18–20 Ω cm²) 이 3 MPa 셀 (≈35) 의 절반쯤이다 — 셀이 달라서 압력 효과인지 셀 차이인지는 못 가른다 (논문 언급 없음). EIS 도 같은 방향 (§3e).

### 3e. EIS (`Fig. S2` · `Fig. S6`)

| 그림 | 값 | 비고 |
|---|---|---|
| `Fig. S2a` (−1 °C · 2 전극) | figure-read ≈ 고주파 시작 13 · 저주파 최소 70 · CT 꼬리 78 Ω cm² | 4 성분 회로를 **실온 자료 전부에 썼다** 고만 하고 **맞춘 값 표는 없다** |
| `Fig. S2b` (25 °C) | R_SEI+CT figure-read ≈ 6.1 (0 h) → 7.2 (25 h) → 8.4 (87 h) → 9.3 (168 h) → 9.2 Ω cm² (262 h) · 본문: 100 h 에 최종값의 10 % 안 (p.1105) | 셀 전체 (두 계면) 인지 한 계면인지 미기재 |
| `Fig. S6a` (3 MPa · 1.0 · 7 사이클) | 저주파 최소 figure-read ≈ 27.5 (1) → 29–37 (2–5) → 49 (6) → 55 Ω cm² (7) · 고주파 시작 14–17 · ✎ 호 폭 13.5 → 38.5 (≈2.9 배) | 본문: 3 MPa 는 임피던스 증가 (p.1110) |
| `Fig. S6b` (7 MPa · 1.0 · 100 사이클) | 사이클 전 · 50 · 100 번째가 겹침 · 최소 ≈14.5–15 · 시작 ≈10.5–11.5 · ✎ 호 폭 ≈4 Ω cm² | 7 MPa 는 증가 없음 (p.1110) · ⚠ 캡션이 없는 'Fig. 7' 을 가리킨다 (본문 `Fig. 6` 이 맞다) |

### 3f. XPS — Li 접촉 250 h 뒤 펠릿 표면 (`Fig. S3` · p.1105–1106)

- 본문: *"the interface is dominated by the presence of Li₂S, with much smaller amounts of Li₃P and other compounds with the XPS signature of phosphosulfides"* → 환원 산물이 안정하고 (Li₂S) 더 분해를 막아 **동역학적으로 안정한 계면 임피던스** (p.1106).
- 그림 (figure-read): P 2p — Li₆PS₅Cl 이중선 ≈131.8 / 132.6 eV 에 접촉 뒤 '환원 P' ≈130.5 · Li₃P ≈127–128 eV 작은 성분 · S 2p — 접촉 뒤 Li₂S (≈160.4 eV) 성분이 주 피크와 맞먹게 커짐 · 'PS' 작은 성분 ≈163 eV · Cl 2p — 모양 변화 없음 (LiCl 성분을 따로 맞추지 않았다).
- ⚠ 본문은 *"phosphorus, sulfur and lithium XPS"* 라 했는데 SI 는 **P 2p · S 2p · Cl 2p** (Li 1s 없음) · Methods 의 C 기준 *"384.8 eV"* 는 ✎ C 1s 관례값 284.8 eV 의 오타로 보인다 · Li₂S 를 *"ionic conductors"* 라 부른 것은 느슨하다 (이 논문에 Li₂S 전도도 값은 없다).

### 3g. Na \| Na-β″-alumina \| Na 대조 (`Fig. S7` · p.1110 · Methods)

- 재료: Ionotec ⌀10 mm · 400 → 2500 grit 탈이온수 연마 · Ar 400 °C 열처리 · Na 100 µm · ⌀5 mm 전극 · ⌀1 mm 기준극 · 압력은 Li 셀과 같은 방법 (그림 4 MPa).
- `Fig. S7a` (3 전극 · 4 MPa · 박리 2 mAh cm⁻²): figure-read ≈ 0.2 → 8–10 mV 평탄 · 0.5 → 25–32 평탄 · **1.0 → 95–187 · 1.5 → 105–275 mV 상승** → ✎ Na CCS 괄호 **(0.5, 1.0]** mA cm⁻².
- `Fig. S7b` (2 전극 · 0.1 · 100 사이클 · 반주기 0.5 mAh cm⁻²): ±10 mV 평탄 · `Fig. S7c` (1.5 · 20 사이클): 19 번째 시작 분극이 3 V 상한에 닿고 20 번째 아래 가지가 −1.0 V 까지 · 캡션: 분극 증가 · 단락.
- 본문: *"A more detailed study of the Na/Na-β″-alumina interface is underway"* (p.1110) → 후속 Spencer Jolly 2020 (§2 계보).
- ⚠ Na 반주기 용량 0.5 mAh cm⁻² 는 그림 축으로만 알 수 있다 (본문 · Methods 무언급).

### 3h. ✎ 우리 산수 — 논문 숫자를 DEM · 연속체 눈금으로 옮겨 본 것 (digitized.csv 아래 6 행)

| 양 | 식 · 입력 | 값 |
|---|---|---|
| 1 mAh cm⁻² 의 Li 두께 | V_m = 6.941 / 0.534 = 13.0 cm³ mol⁻¹ | **4.85 µm** (논문 '≈5 µm' 재현) |
| 박리 후퇴 속도 (계면 Li 소모 속도) | v = j V_m / F | 0.2 → **0.27** · 0.5 → 0.67 · 1.0 → **1.35** · 1.5 → 2.02 · 2.0 → **2.69 nm s⁻¹** (1.0 mA cm⁻² = 4.85 µm h⁻¹) |
| ⇒ CCS 괄호를 '압력이 Li 를 계면에 대는 속도' 괄호로 | 위 v 로 바꿈 | **3 MPa 0.27–1.35 nm s⁻¹ · 7 MPa 1.35–2.69 nm s⁻¹** |
| 전류 변형률 (wang2019 식 2 꼴) | ε̇_j = v / l₀ · l₀ = 40 µm | 0.2 → 6.7 × 10⁻⁶ · 1.0 → 3.4 × 10⁻⁵ · 2.0 → 6.7 × 10⁻⁵ s⁻¹ |
| 겉보기 압력 지수 k (j_CCS ∝ P^k · 3 → 7 MPa = × 2.33) | k = ln(비) / ln(7/3) | 초록 값 0.2 → 1.0 (×5) **k ≈ 1.9** · 본문 'threshold' 1.0 → 2.0 (×2) **k ≈ 0.8** · 괄호 양 끝 0.2 → 2.0 (×10) **k ≤ 2.7** |
| 벌크 거듭제곱 크리프라면 | j ∝ P^n · n = 6.56 (masias2019) | (7/3)^6.56 ≈ **259 배** — 관측 (×2–×10) 보다 26 배 이상 크다 |
| 벌크 크리프 법칙에 명목 압력을 넣으면 | ε̇ = A′σⁿ · A′ = 7.73 × 10⁻³ s⁻¹ MPa⁻ⁿ (masias2019 카드 재회귀 · 0.2–0.6 MPa 창 밖 외삽) | 0.81 MPa → 1.9 × 10⁻³ · 3 MPa → **≈10 s⁻¹** · 7 MPa → **≈2.7 × 10³ s⁻¹** — 40 µm 박이 몇 초에 납작해질 속도라 그대로는 못 쓴다 (wang2019 카드와 같은 관찰) |
| 거꾸로 ε̇_j 를 내는 응력 | σ = (ε̇_j / A′)^(1/n) | 0.2 → 0.34 · 1.0 → **0.44** · 2.0 → 0.49 MPa — 적층압의 1/7–1/16 |

[우리 해석] 마지막 두 줄은 **'계면 공극을 메우는 Li 가 받는 유효 응력은 명목 적층압이 아니다'** 를 뜻한다. 40 µm × ⌀2 mm (지름 / 두께 = 50) 박이 집전체와 SE 사이에 끼어 있으면 응력 상태가 정수압에 가깝고, 공극을 메우는 흐름을 모는 편차 응력은 두께 · 마찰 · 점착 · 공극 모양이 정한다 — 이 논문에는 그 입력이 없다 (§7c).

### 3i. 홉 수 검산 (CLAUDE.md 규율 — 차수 검산이지 확산계수 · 크리프 속도가 아니다)

이 논문은 장벽 값을 하나도 안 준다. 아래 셋은 **litdb 이웃에서 가져와 §7 에서 인용하는 값**이라 검산을 같이 싣는다. ν₀ = 10¹³ s⁻¹ (가정) · T = 298 K (가정 — 이 논문 운전 온도 미기재).
- 크리프 활성화 Q = 37 kJ mol⁻¹ = 0.383 eV (wang2019 `Table S1` → LePage 2019 · 이 논문 값 아님): Γ ≈ **3.3 × 10⁶ s⁻¹** · 평균 대기 ≈ 0.31 µs · 1 h 반주기 동안 N ≈ 1.2 × 10¹⁰.
- Li 공공 자기확산 E^f + E^m = 0.506 + 0.053 = 0.559 eV (seymour2021 카드 · 그 논문 ref 38 소환값): Γ ≈ **3.5 × 10³ s⁻¹** · 평균 대기 ≈ 0.28 ms · 1 h 에 N ≈ 1.3 × 10⁷.
- Li 자기확산 50 kJ mol⁻¹ = 0.518 eV (banerjee2020 리뷰 카드): Γ ≈ **1.7 × 10⁴ s⁻¹** · 평균 대기 ≈ 58 µs · 1 h 에 N ≈ 6.2 × 10⁷.

⇒ 셋 다 상온 · 1 h 에 사건이 10⁷–10¹⁰ 번이다. 본문의 *"Li deformation/creep is expected to be relatively slow"* (p.1108) 는 **사건 하나의 장벽이 높다는 뜻이 아니라, 계면까지 나르는 거시 유속 (거리 · 구동력) 이 박리 유속보다 작다는 뜻**으로만 읽힌다. 이 검산과 차수에서 부딪히지 않는다.

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 합성 (Methods)
§3a 표 첫 세 줄 그대로. 600 °C 15 분 → 분쇄 → 재성형 → 300 °C 15 분은 일반적인 아지로다이트 열처리 (수 시간) 보다 매우 짧다 — 결정도 · 입계 상태를 판단할 자료 (리트벨트 · 밀도 · σ) 가 없다.

### 4b. 셀
- 2 전극: ⌀2 mm × 40 µm Li 두 장을 ⌀5 mm 펠릿 양면에 동심 압착 · Cu 박 · 진공 파우치 · 스프링 클램프 3 / 7 MPa (+ 0.5 MPa).
- 3 전극: 위 + ⌀0.5 mm Li 기준극 (작업극 옆 같은 면 · `Fig. 1a` 평면도 — SE 원판 가장자리 쪽).
- XCT 셀: Xradia 안에서 Deben CT5000 로 3 MPa · Gamry 1010E 로 그 자리 충방전.

### 4c. 전기화학
- 정전류 · 반주기 1.0 mAh cm⁻² · 시작은 작업극 도금 (p.1106).
- 단일 계단 (`Fig. 5`): *"three-electrode cells were constructed and subjected to single plating and stripping at increasing current densities"* (p.1108) — **전류마다 새 셀인지, 한 셀로 전류를 올렸는지 미기재**. 0.1 · 0.2 박리 곡선은 2.0 mAh cm⁻² 까지 안 갔다 (figure-read ≈0.9 · ≈1.78 에서 끝).
- EIS: 2 전극 · 5 mV · 1 MHz–1 Hz · ZView.

### 4d. SEM
초음파 칼 (SONOTEC · 텅스텐 카바이드 날) 로 셀째 자름 → Cu 테이프 홀더 → 기밀 이송 (Gatan) → Zeiss Merlin. 냉각 · FIB 없음 · 압력을 푼 뒤 자른 단면.

### 4e. XCT
Zeiss Xradia Versa 510 · 1 · 3 · 5 번째 박리 뒤 2D 단면 (`Fig. 3`) · 화소 크기 · 재구성 · 분할 조건 미기재.

### 4f. XPS
소결 펠릿에 Li 250 h 접촉 → 칼로 Li 제거 → Cu 테이프 → 기밀 이송 → VG CLAM4 9 채널 분석기 (이온펌프 UHV) · CasaXPS · C 기준 *"384.8 eV"* (✎ 오타 의심).

### 4g. Na 셀
§3g.

### 4h. 해석 틀 (전부)
식은 하나다 (p.1106): **J_Li diffusion + J_Li creep < J_Li⁺ migration** 이면 공극 (J = 유속). 세 유속 어느 것도 값 · 식 · 매개변수가 없다. 근거로 든 물성은 Li 항복 0.81 MPa (ref 36 · ref 38 — §10-⑮) 와 '항복 위에서도 공극이 타원체로 남는다' (ref 37) 둘뿐이다.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 상 · 계면 안정 (`Fig. S1` · `Fig. S2` · `Fig. S3` · p.1105–1106)
XRD 는 입방 아지로다이트 피크 (별표) 만 표시한다. Li 와 맞붙인 2 전극 셀의 R_SEI+CT 는 6 → 9 Ω cm² 로 오르다 100 h 쯤 최종값의 10 % 안에 든다 (`Fig. S2b`). 250 h 뒤 XPS 에 Li₂S 가 주된 산물로 보이고 Li₃P · 환원 P 는 작다 (`Fig. S3`). 저자 결론: Li₆PS₅Cl 은 Li 와 열역학적으로 안정하지 않지만 (refs 33–35) **동역학적으로 안정한 계면**을 만든다 — 그래서 이 논문의 분극 변화를 계면 화학이 아니라 **접촉 (공극)** 으로 읽는다.

### 5.2 셀 도식 (`Fig. 1a`)
옆모습: 위 Li (WE) · 옆 작은 Li (RE) · 가운데 Li₆PS₅Cl · 아래 Li (CE) · 위아래 압력 화살표. 평면도: 큰 주황 원 (SE) 가운데 회색 원 (WE) · 가장자리 작은 회색 원 (RE). ⇒ RE 는 WE 와 **같은 면**에 있다 (§10-⑬).

### 5.3 3 MPa · 1.0 mA cm⁻² 사이클 (`Fig. 1b`) ★
가로축은 면적 용량 0–1.0 mAh cm⁻², 박리 가지는 화살표대로 1.0 → 0 으로 그려서 **x = 0 이 박리 끝**이다. 첫 도금 12 mV 평탄 · 첫 박리는 같은 전위에서 시작해 끝에 19 mV · 7 번째 박리 끝 130 mV 까지 사이클마다 오른다 (figure-read 2–6 번째 ≈25 · 31 · 40 · 58 · 102 mV). 도금은 사이클이 지나도 −12 ~ −17 mV 로 낮다 (평균 13 mV). 8 번째 도금 도중 figure-read ≈0.43 mAh cm⁻² 에서 |V| 가 ≈20 → ≈3 mV 로 떨어진다 = 단락. **박리와 도금의 분극이 이렇게 비대칭인 것은 2 전극 셀로는 못 봤다** (p.1106 · ref 22) — 이 논문의 첫 관찰이다.

### 5.4 박리 — 공극 (`Fig. 2a` · `Fig. 3` · p.1106) ★
- SEM (`Fig. 2a`): 원래 계면과 첫 도금 뒤는 Li 와 SE 가 촘촘히 맞닿아 있다. 저자는 첫 박리 뒤 *"some void formation is evident"* 라 하는데 **이 배율 그림에서 우리는 공극을 가려낼 수 없었다** (칼 자국 같은 세로 줄무늬가 보인다). 6 번째 박리 뒤에는 계면을 따라 검은 틈이 이어진다 (*"substantial detachment"*) — 그림에서 분명하다.
- XCT (`Fig. 3`): 3 MPa · 1.0 · 1 · 3 · 5 번째 박리 뒤 단면 셋 (축척 막대 50 µm). 위쪽 Li 띠와 SE 사이 계면의 흰 화소가 a → c 로 늘어난다 (*"voids increase in number and length"*). 분할 · 공극 분율 숫자는 없다.
- 해석 (p.1106): 접촉 면적이 줄면 같은 전체 전류 (1.0) 에서 국부 전류가 올라 박리 분극이 오른다. 공극 조건 = J_diff + J_creep < J_Li⁺. *"pressure-dependent measurements suggest that creep rather than diffusion dominates … although diffusion may play a more important role on initial stripping"* (p.1106–1107).

### 5.5 도금 — 삼중점 옆 성장 · 갇힌 공극 (`Fig. 2a` 7th plating · `Fig. 4` · p.1107) ★
- SEM: 7 번째 도금 끝에는 6 번째 박리 때의 공극이 대부분 사라지고 접촉이 첫 사이클 수준으로 돌아온다. 대신 Li **안쪽** 에 큰 렌즈꼴 공극 (figure-read ≈20–28 µm × ≈7 µm · 축척 막대 10 µm 를 2 배 확대해 잼 · 왼쪽에 ≈6 × 2 µm 작은 것 하나 더) 이 계면에서 떨어져 갇혀 있다 (= occluded void). [우리 해석] 두께 ≈7 µm 는 반주기 하나의 Li (✎ 4.85 µm) 보다 커서, 여러 사이클에 걸쳐 쌓인 공극이라는 저자 해석과 크기가 맞는다. 빨간 틀 삽입도 'Li dendrite' 는 위치 · 배율이 안 적혀 있다 (구멍 많은 그물 꼴).
- 기전 (p.1107 · `Fig. 4`): 도금에는 Li⁺ 와 전자가 같이 필요하다 → Li 와 SE 가 맞닿은 곳뿐 아니라 **Li · SE · 공극이 만나는 삼중점**에서 시작해 공극의 자유면을 따라 **옆으로 얇은 Li 막**이 자란다 → 막이 공극을 계면에서 잘라 Li 속에 가둔다 → 적은 전하로도 SE 면이 다시 덮여 접촉이 처음과 비슷해진다 → **도금 초반에 분극이 빨리 떨어지고 그 뒤 낮게 유지**된다. 5 µm 도금이 공극을 다 메우지는 못하고, 못 메운 것은 계면에서 밀려나 갇힌다.
- `Fig. 4` (실독): 여섯 칸 — Pristine (평평한 접촉) → After several strippings (Li 쪽 반원 공극 · 'Void formation') → Early in the subsequent plating (공극 가장자리의 회색 얇은 Li · 'Lateral Li growth' 화살표 · SE 안으로 가지 친 선 = 'Initial dendrite propagation') → Middle of the plating (얇은 Li 층이 SE 면을 덮음 · 공극 일부는 Li 로 참) → End of plating (Li 안에 떨어진 타원 공극 둘 = 'Occluded voids' · SE 안 가지) → After further stripping (공극이 다시 계면에 드러나 더 큼 · 'Increase in contact loss upon further void growth'). ⇒ 도식은 **덴드라이트가 도금 초반, 공극 가장자리의 삼중점에서 시작**한다고 그린다.
- 같은 이유로 도금 후반과 다음 박리 초반의 분극이 둘 다 낮다 — 박리가 시작될 때는 접촉이 도금 끝과 같고, 계면 쪽 Li 층이 벗겨져 갇힌 공극이 드러나야 분극이 오른다 (p.1107).

### 5.6 사이클 누적 → 도금 덴드라이트 (p.1107 · `Fig. 4`)
도금이 공극을 다 못 메우므로 공극이 사이클마다 쌓이고, 박리 분극이 사이클과 함께 오른다. 사이클이 쌓인 뒤 첫 도금에서는 접촉이 나빠 **국부 도금 전류가 커져 덴드라이트**가 생긴다 → 7 번째 도금 SEM 의 덴드라이트 · 8 번째 단락.

### 5.7 7 MPa · 1.0 (`Fig. 1c` · `Fig. 2b` · p.1108)
100 사이클 동안 분극이 전하 · 사이클에 거의 무관하다 (figure-read ±8–9 mV). 100 번째 박리 끝 SEM 에 공극 없이 Li 가 SE 면을 고르게 덮고 있다 — 그림에서도 틈이 안 보인다.

### 5.8 7 MPa · 2.0 (`Fig. 1d` · `Fig. 2c` · p.1108)
초반은 3 MPa · 1.0 과 비슷하다 (첫 박리 약간 상승 · `Fig. 2c` 1st stripping 단면에 얇은 틈). 몇 사이클 뒤 도금 분극이 첫 도금보다 작아지고 (figure-read 6 · 9 번째 ≈−30 → −9 mV), 박리 시작 분극도 첫 박리보다 낮다. 9 번째 도금 · 박리 뒤 SEM 에 'Li dendrites' 화살표가 SE 안 깊이 어두운 영역을 가리킨다. 저자 해석: 덴드라이트가 SE 를 파고들며 Li/SE 면적을 늘려 분극을 낮추다가, 다 건너가면 단락 — **10 번째 사이클 뒤**.

### 5.9 작업극 · 상대극 (`Fig. S4` · p.1108)
두 극을 같이 기록하면 거동이 비슷하고 CE 분극이 조금 더 크다 → 공극은 두 극 모두에 생기고 덴드라이트도 두 극에서 올 수 있다. 저자: 대칭셀에서 어느 극이 먼저냐는 중요하지 않다 — 완전 셀에는 금속 음극이 하나뿐이다. ⚠ 같은 조건 (3 MPa · 1.0 · 3 전극) 인데 `Fig. 1b` 의 2–4 번째 박리 끝 ≈25–40 mV 보다 `Fig. S4` WE 는 ≈16–18 mV 로 낮다 (figure-read) — 셀 사이 편차가 두 배쯤이다 (§10-③).

### 5.10 두 임계 전류 (p.1108) ★
CCS · CCP 정의 (§3b). *"If CCP is higher than CCS (which is the case here and is likely to be the case generally), then, despite the overall current density being lower than the critical current for dendrite formation, dendrites, short circuit and cell failure are inevitable; it is only a question of how many cycles will be possible before failure. Of course if CCS > CCP then the former has no role in triggering dendrite formation."*

### 5.11 단일 계단 (`Fig. 5` · p.1108) ★★
- 도금 (`Fig. 5a,b` · 1.0 mAh cm⁻²): 1.0 · 2.0 은 평탄 (figure-read 3 MPa ≈−12 · −27 mV / 7 MPa ≈−8.5 · −19.5 mV) · **3.0 은 |V| 가 전하와 함께 줄어든다** (3 MPa ≈−39 → −20 · 7 MPa ≈−33 → −20 mV) = 덴드라이트 신호 → *"This is independent of pressure"*. 4.0 은 3 MPa 에서 figure-read ≈0.47 mAh cm⁻² 에 −12 → −1 mV 계단 (단락) · 7 MPa 에서는 ≈−52 → −9 mV 로 매끄럽게 줄 뿐 1 mAh 안에 계단이 없다 — 4.0 에서는 두 압력이 다르게 보인다 (저자 언급 없음).
- 박리 (`Fig. 5c,d` · 2.0 mAh cm⁻²): 3 MPa — 0.1 ≈1.5 · 0.2 ≈3 · 0.5 ≈7 → 9 mV · **1.0 ≈15 → 22 (1 mAh) → 29 (1.25) → > 60 mV (1.5)** (*"severe"*). 7 MPa — 0.5 ≈5.5 → 7 · 1.0 ≈11 → 15 · 1.5 ≈14.5 → 28 · **2.0 ≈19 → 25 (1 mAh) → 52 mV (2.0)** (*"threshold is higher at 2.0"*).
- 저자: 3 · 7 MPa 모두 Li 항복 (0.81 MPa) 위인데도 공극이 생긴다 — 공극 생성은 박리 전류가 모는 동적 과정이고 Li 변형 · 크리프는 상대적으로 느리다 · 항복 위에서도 압력이 구형 공극을 타원체로 바꿀 뿐 다 닫지 못한다 (ref 37).
- 저자 제안 (p.1110): *"the single stripping experiment shown in Fig. 5c,d is a viable method for quantifying the CCS at different pressures"*. [우리 해석] 판정 기준을 수치로 정하지 않은 채 제안한 방법이라, 같은 그림을 같은 잣대로 읽으면 초록 값과 한 계단 다른 괄호가 나온다 (§3b 마지막 줄).

### 5.12 항복 아래 0.5 MPa (`Fig. S5` · p.1108)
*"At this pressure the absence of deformation made it a challenge to even form a cell."* 첫 사이클부터 분극이 줄고 (저자: 도금 Li 로 접촉이 좋아짐 **+** 나쁜 접촉에서 국부 전류가 커져 덴드라이트), 다음 박리 분극이 크고 셀이 빨리 죽는다. 마지막 박리 뒤 SEM: 계면 전체를 따라 Li 가 떨어진 틈 (figure-read ≈5–8 µm · 축척 20 µm) · SE 안 세로 균열 하나도 보인다 (저자 언급 없음). ⚠ 캡션 제목은 *"Cycling under 4 MPa pressure"* 인데 그림 범례 · 본문은 **0.5 MPa** 다.

### 5.13 2 전극 (`Fig. 6` · `Fig. S6` · p.1109–1110)
CCS 아래 · 위로 돌렸다 (§3d). 3 MPa · 0.2 와 7 MPa · 1.0 은 100 사이클 평탄, 3 MPa · 1.0 과 7 MPa · 2.0 은 분극이 오르다 단락. 2 전극에서는 아래 가지에 WE 도금과 CE 박리가 같이 들어가서 (✎), 3 전극 `Fig. 1b` 와 달리 6 · 7 번째 아래 가지 분극도 −140 ~ < −160 mV 로 커진다. EIS: 3 MPa 는 사이클마다 호가 커지고 (`Fig. S6a`) · 7 MPa 는 100 사이클 동안 겹친다 (`Fig. S6b`).

### 5.14 Na (`Fig. S7` · p.1110)
같은 현상 (CCS 위에서 분극 증가 · 단락) 이 Na | Na-β″-alumina 에서도 보인다 — *"the results apply to other solid electrolyte interfaces"* 의 근거. 세부는 §3g.

### 5.15 CCS 의 예측성 · 국부 전류 (p.1110)
- 전체 전류가 CCS 를 살짝 넘으면 실패까지 여러 사이클이 걸리고 분극 변화도 작아서, **사이클 곡선만 보고는 끝까지 돌지 예측하기 어렵다** — 단일 박리 실험을 쓰자.
- *"Critical current or potential"*: 공극은 접촉 부위에서 빠져나가는 Li⁺ 유속이 들어오는 Li 유속을 넘을 때, 즉 **계면 국부 임계 전류** 위에서 생긴다. *"The overall current density at which voids form will be the same as the critical current density at the interface, provided there are no blocking layers at the interface resulting in constriction resistances. For simplicity we have assumed that this is the case here."* 막힘층이 있으면 전체 전류 기준 CCS 는 더 낮아진다. 국부 전류는 과전압과 묶여 있어 과전압을 덴드라이트 판정 기준으로 쓸 수도 있다.

### 5.16 결론 (p.1110)
CCS 아래에서 돌려야 한다 — 도금 문턱 아래여도 그렇다. CCS 위에서는 공극 누적 → 접촉 감소 → 국부 전류 증가 → 도금 덴드라이트 · 단락이 '언젠가' 온다. 적층압이 CCS 를 정하는 핵심 변수고, 높은 전류에는 높은 압력이 필요하다. *"Further possible factors such as surface chemistry, microstructure, adhesion and mechanical properties of both Li metal and solid electrolyte may warrant investigation as impacting the critical current density on stripping."* 초록: *"Considerable pressure may be required to achieve even modest power densities in solid-state cells."*

---

## 6. 메커니즘 종합 — 저자 논리 사슬과 우리 읽기

1. **박리**: 계면에서 Li⁺ 로 빠져나가는 유속 > 확산 + 크리프로 계면에 오는 Li 유속 → Li 쪽 계면에 공극 (p.1106).
2. 공극 → 접촉 면적 ↓ → 같은 전체 전류에서 **국부 전류 ↑** → 박리 분극 ↑ (`Fig. 1b` · `Fig. 2a` · `Fig. 3`).
3. **도금**: 삼중점 (Li · SE · 공극) 에서 시작한 옆 방향 얇은 Li 막이 SE 면을 다시 덮고 공극을 Li 속에 가둔다 → 도금 분극은 낮다 (`Fig. 4` · `Fig. 2a`).
4. 다음 박리에서 갇힌 공극이 다시 드러나고 커진다 → **사이클마다 누적**.
5. 사이클이 쌓인 뒤 첫 도금: 접촉이 나빠 국부 도금 전류 > CCP → **덴드라이트 → 단락** (`Fig. 1b` 8 번째 · `Fig. 1d` 10 번째).
6. **압력**: 크리프 공급 ↑ → CCS ↑ (`Fig. 5c,d`) · CCP 는 압력 무관 (`Fig. 5a,b`).
7. ⇒ CCS < CCP 이면 전체 전류가 CCP 아래여도 결국 실패 — 운전 전류의 실제 상한은 CCS 다.

[우리 해석]
- 6 의 '크리프 (확산 아님)' 판정은 **압력 의존 하나**에 기댄다. 그런데 관측된 압력 의존 (k ≈ 0.8–1.9 · 괄호 끝까지 넓혀도 ≤ 2.7) 은 벌크 거듭제곱 크리프 (n = 6.56 → k ≈ 6.6) 와 차수가 다르다 (§3h). **선형에 가까운 압력 의존**은 응력 구동 확산 (확산 크리프 · 공공 흐름이 응력에 1 차) · 압력에 따른 초기 접촉 면적 차 (`Fig. 6` · `Fig. S6` 의 7 MPa 셀 ASR 절반) · 구속 · 마찰이 정하는 유효 응력으로도 나온다. 확산과 크리프를 가르는 시험은 **온도 의존**이다 (같은 그룹 후속 Spencer Jolly 2021 — 안 봄).
- LLZO 에서 같은 질문을 한 wang2019 도 겉보기 지수 ≈1 (σ_crit ∝ j^≈1) 을 냈다 — **계가 다른 두 실험이 둘 다 '벌크 크리프 지수보다 훨씬 약한 압력 의존'** 을 보인다. 숫자를 섞지 않고 이 '모양' 만 같이 쓸 수 있다 (§7d).
- 3–5 의 기전은 그림 (SEM · XCT) 이 정성적으로 받친다. 갇힌 공극 (`Fig. 2a` 7th plating) 은 분명하다. '덴드라이트' 판정은 SEM 명암뿐이다.

---

## 7. 우리와의 대조 ★★ (우리 W 값은 위치만 — `db/properties/adhesion.json` · W_ad 보고서 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` 2 절)

### 7a. 우리 DFT 기준선 (`../our_dft_baseline.md`) — 겹치는 값이 거의 없다

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 이온전도 σ · Ea | **없음** (EIS 회로는 4 성분인데 맞춘 값 표가 없다) | MLIP-MD Ea · D (상대차 정책) | n/a — 비교 불가 |
| 산화 · ESW | 없음 | grand-potential ESW | n/a |
| 기계 (SE) | *"less brittle than the other highly conducting sulfides"* (p.1105 · ref 31 = litdb `deng2016_elastic_superionic_electrolytes_dft`) — 값 없음 | E_VRH · B₀ (`our_dft_baseline.md`) | 정성 문장뿐 — 우리 값을 이 문장의 근거로 쓰려면 deng2016 카드의 정의 (취성 지표 · 범함수) 를 먼저 맞춘다 |
| 전자구조 | 없음 | PBE gap | n/a |
| **Li 접촉 환원 산물** | XPS 250 h: **Li₂S 우세** + Li₃P · 환원 P · phosphosulfide 소량 · Cl 2p 변화 없음 (LiCl 따로 안 맞춤) (`Fig. S3`) | 우리 0 V 산물표의 반응식 문자열은 **BLOCKED** (`HZ-anode-b2o3-reaction-direction` — 방향이 뒤집혀 Li₂S 가 빠져 있다 · `db/properties/anode_interface_b2o3.json`) | **문헌 산물 쪽 (Li₂S + Li₃P) 과 같은 방향** — 우리 반응식 오류를 다시 확인할 뿐 새 판정이 아니다. 이 논문 XPS 는 원장이 든 Wenzel 2018 (이 논문 ref 33) 과 **같은 방법 (XPS) 의 독립 측정**이다 — 원장의 '두 방법 (XPS · MLIP-MD)' 셈은 그대로 |
| Li 금속 점착 W | 없음 — 결론에서 '점착' 을 CCS 의 다음 변수로만 든다 (p.1110) | W_ad (Li 쪽은 보고서 7 절 제안 단계) — 값은 위치만 | 같은 줄에 놓을 값 없음 |

### 7b. W_ad 보고서 8-1 · 8-4 와 맞춰 보기

- **8-1 ('잘 붙는다' ≠ '공극을 막는다')** — 이 논문은 실제 셀에서 **박리 쪽 (CCS) 이 먼저 막히고, 그 공극이 도금 덴드라이트를 부른다**는 순서를 보였다 (`Fig. 1b` · `Fig. 4` · `Fig. 5`). ⇒ 8-1 의 공극 억제 문턱 (W/2γ_Li ≥ 1) 이 셀에서 겨냥하는 양은 **CCS** 다 (CCP 가 아니다). 정량 연결은 없다 — 이 논문은 점착을 재지 않았다.
  · 이 논문 XPS 의 계면은 Li₂S 우세다. seymour2021 카드의 Li₂S W/2σ ≈ 0.40 (그 카드 ✎ · 비정합 평균 · VASP-PBE · 우리 W 와 다른 방법) 과 이으면 '이 계면은 공공을 붙잡는 쪽' — 공극이 생긴 관측과 방향이 맞다 [우리 해석 · 두 논문 연결].
- **8-4 첫 문단 ('Li 금속은 적층압 아래에서 늘 흐른다')** — 이 논문은 3 · 7 MPa (항복 0.81 위) 에서도 공극이 생겼고 (p.1108), 0.5 MPa (항복 아래) 에서는 셀을 만들기도 어려웠다 (`Fig. S5`). 흐름 응력은 변형 속도에 따라 바뀐다는 보고서 문장과 맞물린다: 박리 등가 변형 속도 (✎ 3.4 × 10⁻⁵ s⁻¹ · 1.0 mA cm⁻²) 에서 벌크 크리프 법칙의 흐름 응력은 ✎ ≈0.44 MPa 다.
- **8-4 ('필요한 적층압은 전류와 함께 커진다')** — LLZO (wang2019) 와 같은 방향의 **LPSCl 원전**이다: 3 MPa 안전 0.2 · 실패 1.0 / 7 MPa 안전 1.0 · 실패 2.0 mA cm⁻².
- **8-4 ('LPSCl|Li 계면도 같은 방향이다')** — 이 문단의 kim2026 (0.4 MPa 공극 · 5 MPa 무) · shi2026 (8 MPa 에서 몇 시간에 공극 축소) 보다 앞선 원전이고, '박리 공극 → 다음 도금 덴드라이트' 라는 실패 연결을 처음 보였다.
- **8-4 ('공극을 다시 메우는 것은 속도 문제다')** — 이 논문 p.1108 *"The generation of voids is a dynamic process driven by the stripping current, whereas Li deformation/creep is expected to be relatively slow"* 가 같은 말이다.
- **8-4 균열 문단** — 이 논문의 덴드라이트 판정은 SEM 명암뿐이고 균열 개시 · 전파는 안 봤다. Li 로 찬 균열 (Matter 2, 1025) 과 같은 줄에 쓰지 않는다 (같은 그룹의 균열 쪽 후속은 Ning 2021 · 2023).
- **8-4 압력 단계** — 이 논문은 '실험실 셀' 단계 (3–7 MPa) 다.

### 7c. ★ DEM 접촉 모형과 같은 눈금에 놓을 수 있나 — **이 논문 숫자만으로는 못 놓는다**

못 놓는 이유:
1. **접촉 면적 · 공극 분율을 숫자로 안 쟀다** — SEM 단면 한 장 · XCT 2D 단면 셋 · EIS 호 폭뿐이고 분할 · 정량이 0 이다.
2. **압력이 조립 때 한 번 맞춘 명목값**이다 (스프링 클램프 · 압전 로드셀) — 운전 중 압력 기록이 없고, 어느 면적으로 나눈 값인지도 없다 (Li ⌀2 mm 와 SE ⌀5 mm 사이 ✎ 6.25 배).
3. **대상이 다르다** — 우리 DEM 은 SE 입자 충전 · 기공 · 입자끼리 접촉 (정적 접촉 법칙) 을 만든다. 이 논문의 공극은 **Li 금속 안, Li|SE 평면 계면**의 공극이고, 메우는 것은 Li 의 **시간 의존 유동** (크리프 · 소성) 이다. DEM 접촉 법칙에는 시간 의존 Li 유동이 없다 (masias2019 카드 · `comparison_vs_ours_DEM.md` §I-16 ① 과 같은 지적).
4. **응력 눈금이 안 맞는다** — 벌크 크리프 법칙에 명목 적층압을 넣으면 ε̇ 가 10–10³ s⁻¹ 로 터지고, 박리 변형 속도를 내는 응력은 적층압의 1/7–1/16 이다 (§3h). 공극 옆 Li 가 받는 편차 응력은 Li 두께 (40 µm) · 지름 / 두께 (50) · Li|집전체 · Li|SE 마찰과 점착 · 공극 모양이 정하는데 셋 다 없다.
5. **SE 쪽 입력이 없다** — 펠릿 밀도 · 기공 · 표면 거칠기 (1200 grit 연마만) · 두께가 없어서, DEM 이 줄 수 있는 '처음 접촉 분율' 을 이 셀과 맞출 근거가 없다.
6. **기록 안 된 프로토콜 변수** — `Fig. S4` 의 반주기 사이 휴지 (figure-read ≈0.45 h) · 온도. shi2026 은 영전류 유지가 CCD 를 두 배 넘게 올린다고 보고했다 — 휴지는 크리프 회복 시간이라 CCS 를 바꿀 수 있다.

그래도 쓸 수 있는 변환 (✎ · **대조 표적으로만** — 보정 표적이 아니다):
- **CCS 괄호 → Li 공급 속도 괄호**: 3 MPa 0.27–1.35 nm s⁻¹ · 7 MPa 1.35–2.69 nm s⁻¹ (§3h). Li 점소성 접촉 법칙을 넣은 연속체 · DEM 이라면 '이 압력에서 계면 공극 앞면이 닫히는 속도' 를 이 괄호와 견줄 수 있다.
- **국부 전류 = 전체 전류 / 접촉 분율** (p.1110 의 우리 식 꼴 · 막힘층 없음 가정): DEM 이 접촉 분율 φ_c 를 주면 j_local = j / φ_c. 이 논문은 φ_c 를 안 줬으니 보정은 못 한다.
- **겉보기 압력 지수 k ≈ 0.8–1.9 (≪ 6.56)**: 우리 모형이 n = 6.56 벌크 크리프 + 명목 압력으로 이 압력 의존을 못 맞춰도 모형 실패로 읽지 않는다 — wang2019 (LLZO) 와 같은 결론이다. 설명해야 할 것은 '거의 선형인 공급' 이다.
- (쓰지 않는 것) EIS 호 폭 비 (`Fig. S6a` 1 → 7 번째 ≈2.9 배) 를 접촉 분율 비로 읽으려면 R ∝ 1/A (전류 수축 무시) 가정이 든다 — 정량 입력으로 안 쓴다.

### 7d. litdb 이웃과 맞춰 보기 — 숫자가 맞나 · 정의가 같나

| 이웃 | 계 · 질문 | 그쪽 숫자 | 정의 차이 | 이 논문과 |
|---|---|---|---|---|
| [`wang2019_…`](wang2019_li_se_interface_dynamics_stack_pressure_current_density.md) (*Joule* 3, 2165) | Li \| Ta-LLZO \| Li · 하중 제어 · 단방향 박리 | 임계 적층압 **0.4 / 1.2 / 2.0 MPa @ 0.1 / 0.2 / 0.4 mA cm⁻²** · Li 750 µm · 조건당 셀 1 | **전류 고정 · 압력 계단** (0.4 MPa · 5 h 단) — 이 논문은 **압력 고정 · 전류 계단** (1–2 mAh) | 방향 같음 (압력 ↑ → 허용 박리 전류 ↑) · 겉보기 지수 wang ≈1 · 이 논문 0.8–1.9 — **둘 다 벌크 6.6 과 멀다** · 숫자 직접 비교 금지 (LLZO 는 Li 와 안정 · Li 두께 ≈19 배 · 정의 다름) |
| [`masias2019_…`](masias2019_li_metal_elastic_plastic_creep_properties.md) (*J. Mater. Sci.* 54, 2585) | Li 금속 역학 | σ_y **0.73–0.81 MPa** (인장 · 0.2 % · 1.2 × 10⁻³ s⁻¹) · n **6.56** (인장 0.2–0.6 MPa) | 이 논문은 0.81 만 쓰고 출처를 ref 36 · ref 38 로 다르게 단다 · 항복은 속도 의존 (✎ 박리 등가 속도에서 ≈0.44 MPa) | '3 · 7 MPa > 항복 → Li 가 흐른다' 는 맞다 · 얇은 박의 구속 · 마찰 아래 편차 응력은 별개 문제 (§3h) |
| [`seymour2021_…`](seymour2021_void_suppression_interfacial_adhesion_vacancy_transport.md) (*J. Mater. Chem. A* 9, 19901) | DFT 판정식 W ≥ 2σ_m | Li₂S W/2σ ≈ 0.40 · Li₃P ≈ 0.66 (그 카드 ✎) · '~1 mA cm⁻² 에 ~10 MPa 필요' (refs 28 · 29 · 34) | **열역학 문턱** (공공이 계면에 모이나) 대 이 논문의 **운동학 문턱** (공급 < 소모) | 이 논문 XPS 의 Li₂S 우세 계면은 Seymour 문턱 미달 → 공극 쪽과 맞다 · ⚠ seymour2021 카드가 ref 28 (= 이 논문) 에 단 두 귀속을 원문에서 확인할 것: '~10 MPa @ ~1 mA cm⁻²' 은 이 논문 값이 아니다 (7 MPa 에서 1.0 이 돈다) · 'Li/LLZO 에서 큰 압력 없이 공극' 의 근거로도 안 맞는다 (이 논문은 LPSCl · LLZO 실험 0) |
| [`fuchs2023_…`](fuchs2023_cu_llzo_anode_free_li_growth_modes.md) (*Adv. Energy Mater.* 13, 2203174) | Cu \| LLZO 무음극 · 0 MPa · 첫 충전 핵생성 | 16 µAh cm⁻² · 50–1000 µA cm⁻² · 핵 = Cu–LLZO 직접 접점 · 두꺼운 CC 아래 ≈2 µm 틈 | 도금 쪽 · 박리 없음 | 숫자는 안 겹친다 · **기전이 짝을 이룬다**: 이 논문 '삼중점 (Li · SE · 공극) 에서 시작해 공극 자유면을 따라 옆으로 자라는 Li 막' (`Fig. 4`) ↔ Fuchs '핵은 CC–SE 직접 접점' — 둘 다 이온 · 전자 길이 만나는 자리에서 시작 |
| [`sharafi2017_…`](sharafi2017_llzo_surface_chemistry_li_wetting_interfacial_resistance.md) (*Chem. Mater.* 29, 7961) | Li \| LLZO 젖음 · R_int · CCD | CCD **0.3 mA cm⁻²** (상온 · 0.01 → 1 계단 · 2 전극) · R_Li–LLZO **2 Ω cm²** · 그 논문 `Fig. 5b` 문헌 CCD 0.01–0.15 | **2 전극 CCD = 박리 · 도금이 섞인 값** (이 논문이 짚은 한계) | 이 논문 서론 *"LLZO … can be as low as 0.6 mA cm⁻² (refs 6, 13, 14, 15)"* 의 ref 14 가 바로 sharafi2017 인데 거기 값은 **0.3** (그 논문이 모은 문헌은 더 낮다) → '0.6' 을 하한으로 읽으면 틀린다 · R_int 2 (LLZO) 대 이 논문 R_SEI+CT ≈6–9 Ω cm² (LPSCl · SEI 포함 · figure-read) — 계가 달라 같은 줄 금지 |
| (LPSCl) [`shi2026_…`](shi2026_argyrodite_stack_pressure_viscoplastic_deformation.md) (*Matter* 9, 102767) | Li \| LPSCl \| Li · 3–8 MPa CCD + 영전류 유지 | 무유지 CCD **1.8–2.4** · 8 MPa · 5 h 유지 최고 **4.8 mA cm⁻²** | 2 전극 계단 CCD | 이 논문 CCP 2.0 (단일 도금 · 3 · 7 MPa) 과 무유지 CCD 의 자릿수가 같다 · 유지가 CCD 를 올린다 = '공극 회복은 시간 문제' 라는 이 논문 그림과 같은 방향 |
| (LPSCl) [`kim2026_operando_…`](kim2026_operando_void_detection_single_frequency_impedance.md) (*ACS Electrochem.* 2, 384) | Li₆PS₅Cl 무음극 박리 공극 operando −Im(Z) | 0.4 MPa · 0.4 mA cm⁻² → 공극 신호 · 5 MPa → 없음 | 단일 주파수 임피던스 · in situ Li | 방향 같음 — 0.4 MPa 는 이 논문 0.5 MPa (빠른 실패) 쪽 · 5 MPa · 0.4 는 이 논문 괄호 (3 MPa 0.2–1.0 · 7 MPa 1.0–2.0) 사이에서 안전 쪽 |
| (LPSCl) [`tron2023_…`](tron2023_lpscl_ccd_ambient_pressure.md) | 상압 0.20–0.28 MPa LPSCl CCD | **0.023–0.19 mA cm⁻²** | galvanodynamic · 2 전극 | 항복 아래 압력에서 낮은 임계 전류 — 이 논문 0.5 MPa 빠른 실패 (`Fig. S5`) 와 같은 방향 |
| (LPSCl) [`doux2020_…`](doux2020_stack_pressure_assb.md) | Li \| LPSCl \| Li · 5–75 MPa | 5 MPa > 1000 h 무단락 · 25 MPa ≈48 h · 75 MPa 압착 즉시 단락 (펠릿 상대밀도 87 %) | 압력 **상한** | '압력이 높을수록 좋다' 에는 상한이 있다 — 높은 압력은 Li 를 SE 기공으로 크리프시켜 단락시킨다 · 이 논문은 7 MPa 까지만이고 펠릿 밀도가 미기재라 그 상한을 이 셀로 옮길 근거가 없다 |

---

## 8. DFT/계산 방법 ★

**없다 — 실험 논문이다.** 템플릿 칸 (code · functional · pseudo · k-points · ecut · supercell · DFT+U · AIMD · MLIP · 무질서 처리) 전부 n/a. 이 논문의 '이론' 은 유속 부등식 하나 (§4h) 와, 공극 붕괴 역학 문헌 (ref 37) · Li 항복 (refs 36 · 38) 인용뿐이다. DFT 는 참고문헌 ref 31 (Deng 2016 — 탄성) · ref 35 (Zhu, He & Mo 2015 — 안정창) 으로만 들어온다.

## Post-processing

| 무엇 | 도구 | 수치화 · 기록 |
|---|---|---|
| 정전류 전압–면적 용량 곡선 | Gamry Interface-1000 (XCT 셀은 1010E) | 분극 상승 · 하강 · 계단의 **정성 판정** (수치 기준 없음) |
| EIS 등가회로 맞춤 | ZView · R0 + 3 × (R‖CPE) | 맞춘 값은 R_SEI+CT 시간 변화 (`Fig. S2b`) 만 그림으로 · 표 없음 |
| XPS 피크 맞춤 | CasaXPS · C 기준 '384.8 eV' (오타 의심) | 성분 이름만 · 면적비 · 결합 에너지 표 없음 |
| XCT | Zeiss Xradia Versa 510 · Deben CT5000 | 2D 단면 셋 · 분할 · 공극 분율 없음 |
| SEM 단면 | 초음파 칼 · Zeiss Merlin | 정성 (명암) |
| 자료 공개 | Oxford Research Archive `10.5287/bodleian:gA47ppAz9` | 이 digest 에서 안 받아 봤다 |
| (우리 쪽) | 그림 판독 · 산수 | `litdb/figures/kasemchainan2019_critical_stripping_current_dendrite_on_plating/digitized.csv` (49 행) |

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 3 전극 셀 도식 — 옆모습 (WE · RE · CE · 압력 화살표) + 평면도 (SE ⌀5 mm · WE ⌀2 mm · RE ⌀0.5 mm 가 WE 옆 같은 면) | RE 위치 한계 (§10-⑬) · 우리 실험 짝의 셀 설계 참고 |
| 1b | 3 MPa · 1.0 mA cm⁻² 3 전극: 도금 12 mV 평탄 · 박리 끝 19 → 130 mV (7 번째) · 8 번째 도금 단락 (figure-read ≈0.43 mAh cm⁻²) | **박리 · 도금 비대칭의 원 그림** — 보고서 8-1 · 8-4 '박리가 먼저 막힌다' 근거 |
| 1c | 7 MPa · 1.0 · 100 사이클 — 분극 ±8–9 mV 불변 (figure-read) | 압력으로 CCS 를 넘긴 예 · 안전 전류 1.0 의 근거 |
| 1d | 7 MPa · 2.0 — 초반 박리 분극 상승 · 뒤 사이클 도금 분극 감소 (덴드라이트 면적) · 10 번째 단락 | '분극이 줄면 덴드라이트' 판정의 예 · CCS < 2.0 |
| 2a | SEM 단면 3 MPa · 1.0: 원래 · 1 번째 도금 · 1 번째 박리 · 6 번째 박리 (계면 틈) · 7 번째 도금 (Li 안 갇힌 공극 + 'Li dendrite' 삽입도) | 갇힌 공극의 직접 증거 · 1 번째 박리 '일부 공극' 은 이 그림으로 확인 안 됨 |
| 2b | SEM 7 MPa · 1.0 · 100 번째 박리 끝 — 공극 없이 고른 접촉 | 압력이 공극을 막은 정성 증거 |
| 2c | SEM 7 MPa · 2.0: 1 번째 도금 · 1 번째 박리 (얇은 틈) · 9 번째 도금 · 박리 ('Li dendrites' 화살표 — SE 안 어두운 영역) | 덴드라이트 판정 = 명암뿐 (§10-⑨) |
| 3a–c | in situ XCT 2D 단면 (3 MPa · 1.0) — 1 · 3 · 5 번째 박리 뒤 계면 흰 화소 증가 (축척 50 µm) | 공극 누적의 in situ 정성 증거 · 정량 없음 (§10-⑩) |
| 4 | 기전 도식 6 칸 — 박리 공극 → 삼중점 옆 Li 막 → 갇힌 공극 → 다시 드러나 커짐 · 초반 덴드라이트 가지 | **보고서 8-4 · DEM 개념 그림** — 국부 전류 · 접촉 상실의 순서 |
| 5a,b | 단일 도금 1.0–4.0 mA cm⁻² (3 · 7 MPa) — 3.0 에서 \|V\| 감소 = CCP 신호 · 3 MPa 4.0 은 ≈0.47 mAh cm⁻² 단락 · 7 MPa 4.0 은 계단 없음 (figure-read) | CCP 2.0 < · ≤ 3.0 의 근거 · 압력 무관 주장 |
| 5c,d | 단일 박리 0.1–2.0 mA cm⁻² (2.0 mAh cm⁻² 까지) — 3 MPa 1.0 폭주 · 7 MPa 2.0 폭주 · 첫 1 mAh 상대 상승 figure-read (digitized.csv) | **CCS 괄호의 원 자료** · 같은 잣대 재판독 (§3b) · 겉보기 압력 지수 (§3h) |
| 6a–d | 2 전극 사이클 — 3 MPa 0.2 (100 사이클 ±7 mV) · 3 MPa 1.0 (8 번째 단락) · 7 MPa 1.0 (±18 mV) · 7 MPa 2.0 (10 번째 단락) | '안전 전류' 의 2 전극 확인 · ✎ ASR 35 대 18 Ω cm² |
| S1 | 소결 (300 °C) 펠릿 분말 XRD — 입방 아지로다이트 피크 표시 (15–60°) | 상 확인만 (크롭은 안 열고 쪽 렌더로 봄) |
| S2 | (a) −1 °C Nyquist + 4 성분 회로 (bulk · GB · SEI · CT) · (b) 25 °C R_SEI+CT 6 → 9 Ω cm² · 100 h 안정 | 계면 '동역학적 안정' 근거 · 맞춘 값 표 없음 |
| S3 | XPS P 2p · S 2p · Cl 2p — 원래 대 Li 250 h: Li₂S 성분 커짐 · 환원 P · Li₃P 작음 · Cl 2p 변화 없음 | 우리 0 V 산물 반응식 (BLOCKED) 의 문헌 쪽 확인 (§7a) |
| S4 | 3 전극 WE · CE 전압 동시 기록 (3 MPa · 1.0) — CE 가 조금 더 큼 · 반주기 사이 0 mV 휴지 ≈0.45 h (figure-read) | 휴지라는 기록 안 된 변수 (§10-⑯) · 셀 간 편차 (§10-③) |
| S5 | (a) 0.5 MPa · 1.0 3 전극 — 빠른 실패 · (b) 마지막 박리 뒤 계면 전체 틈 + SE 균열 (캡션 제목은 '4 MPa' 오기) | 항복 아래 압력의 실패 예 · 보고서 8-4 압력 단계 |
| S6 | EIS (a) 3 MPa · 1.0 · 7 사이클 — 호 커짐 (최소 ≈27.5 → 55 Ω cm²) · (b) 7 MPa · 1.0 · 100 사이클 — 겹침 (≈15) (캡션의 'Fig. 7' 은 본문 `Fig. 6`) | 접촉 상실의 임피던스 신호 · 정량 입력은 아님 |
| S7 | Na \| Na-β″-alumina — (a) 4 MPa 단일 박리 0.2–1.5 (1.0 부터 상승) · (b) 0.1 · 100 사이클 평탄 · (c) 1.5 · 20 사이클 실패 | 다른 계에도 CCS 가 있다는 대조 · Na 값은 LPSCl 로 옮기지 않는다 |

---

## 10. 비판 — 이 논문의 약한 곳 ★

① **CCS 숫자가 두 벌이다** (§3b 상자) — 초록 · 서론의 0.2 / 1.0 (안전하게 돈 값) 과 본문 2 전극 절의 'CCS thresholds 1.0 / 2.0' (처음 실패한 값). 둘 다 문턱 자체가 아니라 문턱을 끼운 시험값이다. 2 차 인용 (litdb 이웃 셋 — §17) 은 전부 초록 쪽을 옮겼다.
② **판정 기준이 정성적이다** — 'severe' · 'threshold' 뿐이다. 같은 그림을 같은 잣대 (첫 1 mAh 상대 상승) 로 읽으면 3 MPa 0.5 (+14 %) 와 저자가 '아래' 로 둔 7 MPa 1.0 (+9 %) 이 비슷한데, 3 MPa 의 CCS 는 0.2 로 적혔다 (figure-read · 판독 오차 큼).
③ **조건마다 셀 하나 · 오차 · 반복이 없다.** 같은 조건 (3 MPa · 1.0 · 3 전극) 의 두 셀이 4 번째 박리 끝 분극 ≈40 (`Fig. 1b`) 대 ≈16–18 mV (`Fig. S4`) 로 두 배 차이가 난다 (figure-read) — 저자 언급 없음.
④ **단일 계단 실험의 이력** — 전류마다 새 셀인지 한 셀로 올렸는지 없다. 한 셀이면 앞 계단의 공극이 뒤 계단을 바꾼다. 0.1 · 0.2 박리는 2.0 mAh 까지 안 갔다.
⑤ **'creep rather than diffusion' 은 압력 의존 하나로 내린 판정이다** — 세 유속의 값 · 식이 없고 정량 비교가 0 이다. 관측된 겉보기 압력 지수 (0.8–1.9) 는 벌크 거듭제곱 크리프 (6.56) 와 차수가 다르고, 선형에 가까운 압력 의존은 응력 구동 확산 · 초기 접촉 면적 · 유효 응력으로도 나온다 (§6). 가르는 시험 (온도 의존) 이 없다. 서론의 *"demonstrating that Li metal creep is the primary mechanism"* (p.1105) 은 과하다.
⑥ **압력 정의가 비어 있다** — 기준 면적 (Li ⌀2 mm vs SE ⌀5 mm · 6.25 배) · 운전 중 압력 변화 (스프링 클램프 · Li 가 얇아지고 공극이 생기면 바뀐다) · 0.5 MPa 는 Methods 에 없다.
⑦ **운전 온도 미기재** — 크리프 · 확산 모두 온도에 민감하다 (상온 Li 는 T/T_m ≈ 0.66).
⑧ **SE 펠릿의 밀도 · 두께 · 이온전도도 미기재** — 덴드라이트가 '깊이' 들어갔다는 판단 (`Fig. 2c`) · 압력 상한 (doux2020) · DEM 대조를 다 막는다.
⑨ **SEM 단면의 한계** — 초음파 칼로 자른 단면 (무른 Li 는 번지거나 공극이 생기고 닫힐 수 있다) · 압력을 푼 뒤 · 셀 하나의 한 자리 · 'Li dendrite' 는 명암 판정 · 7 번째 도금 삽입도의 위치 · 배율 미기재 · 첫 박리의 '일부 공극' 은 그림으로 확인되지 않는다 (우리 판독).
⑩ **XCT 의 한계** — 2D 단면 셋 · 화소 크기 미기재 · Li 와 공극이 둘 다 X 선 감쇠가 낮아 대비가 약하다 · 분할 · 공극 분율이 없다.
⑪ **EIS 의 한계** — 4 성분 회로의 맞춘 값 표가 없다 · R_SEI+CT 가 두 계면 합인지 한 계면인지 없다 · `Fig. S6` 캡션이 없는 'Fig. 7' 을 가리킨다.
⑫ **XPS 서술 불일치** — 본문 'phosphorus, sulfur and lithium' 대 SI 의 P · S · Cl (Li 1s 없음) · C 기준 '384.8 eV' (오타 의심) · Li₂S 를 'ionic conductor' 라 부름 · 250 h 한 시점.
⑬ **기준극 위치** — RE 가 WE 와 같은 면 옆에 있어서 WE–RE 전위에 SE 저항과 전류 분포 변화가 섞일 수 있다 (CE 쪽 공극 · 덴드라이트가 WE 신호를 바꿀 수 있다). 저자는 `Fig. S4` 로 WE · CE 가 비슷하다는 것만 보였다.
⑭ ***"cells can be cycled indefinitely"*** (p.1105) — 보인 최대는 100 사이클이다.
⑮ **인용 · 캡션 잔실수** — Li 항복 0.81 MPa 의 출처를 같은 쪽에서 ref 36 (첫 번) · ref 38 (두 번째) 로 다르게 단다 (값의 원전은 ref 38 Masias) · `Fig. S5` 제목 '4 MPa' 대 범례 · 본문 0.5 MPa · 서론 'LLZO as low as 0.6' 의 ref 14 는 0.3 (§7d).
⑯ **휴지 (rest) 가 기록 안 됐다** — `Fig. S4` 에 반주기 사이 0 mV ≈0.45 h (figure-read) 가 있는데 Methods 무언급이다. `Fig. 1` · `Fig. 6` 사이클에도 휴지가 있었는지 알 수 없다. 휴지는 크리프 회복 시간이라 CCS 를 바꿀 수 있다 (shi2026).
⑰ **0.5 MPa 해석** — '분극 감소 = 접촉 개선 **+** 덴드라이트' 두 해석을 한 문장에 같이 둔다 — 가르는 자료가 없다.
⑱ **XRD 로 '조성 확인'** (p.1105) — XRD 는 상을 확인할 뿐 조성을 확인하지 않는다 (리트벨트 · 원소 분석 없음).

---

## 11. 우리 원장 매핑 (요약표)

| 우리 원장 · 문서 | 이 논문이 주는 것 | 판정 |
|---|---|---|
| `db/properties/anode_interface_b2o3.json` (`HZ-anode-b2o3-reaction-direction` BLOCKED) | XPS 산물 Li₂S + Li₃P (LiCl 은 안 갈림) | 문헌 산물 쪽 하나 더 (XPS) — 우리 반응식 방향 오류 재확인 · 새 판정 아님 |
| `db/properties/adhesion.json` · W_ad 보고서 2 절 · 7 절 | 점착 정량 0 · '점착' 을 CCS 의 다음 변수로 언급 (p.1110) | 값 연결 없음 · 보고서 8-1 · 8-4 문장 근거 (§7b) |
| `litdb/our_dem_baseline.md` | — | 자리표시 (값 0) — DEM 대조는 이 브랜치에 근거 문서가 없다 |
| `comparison_vs_ours.md` §E | 새 행 후보 (박리 쪽이 먼저 막힌다 · CCS 두 벌) | 메인 세션이 합친다 |
| `comparison_vs_ours_DEM.md` §I | 새 블록 후보 (I-15 wang2019 · I-16 masias2019 · I-22 shi2026 이웃) | 메인 세션이 합친다 |

---

## 12. 적용 인사이트 ★

① **보고서에서 '공극 억제 문턱' 을 말할 때 짝지을 실험량은 CCS 다** — 이 논문에서 셀을 먼저 무너뜨린 것은 박리 공극이었다. W 를 CCP (도금 덴드라이트 전류) 와 직접 잇는 서술은 피한다.
② **DEM 에 Li 상을 넣는다면** 시간 의존 Li 점소성 접촉 법칙이 필요하다. 그 법칙을 명목 압력 + 벌크 n 6.56 으로 두면 이 논문 압력 의존을 못 맞춘다 — 대조 표적은 공급 속도 괄호 (3 MPa 0.27–1.35 · 7 MPa 1.35–2.69 nm s⁻¹) 와 겉보기 지수 0.8–1.9 다.
③ **국부 전류 = 전체 전류 / 접촉 분율** — DEM 접촉 분율을 국부 전류로 바꾸는 서술의 문헌 근거 (p.1110 · 막힘층 없음 가정을 같이 적는다).
④ **우리 쪽 실험 짝이 CCS 를 잰다면** 이 논문이 비운 것을 채운다: 3 전극 + 단일 박리 계단 · 판정 기준을 미리 수치로 (예: 첫 1 mAh 안 상대 상승 x %) · 전류마다 새 셀 · 휴지 · 압력 기준 면적 · 운전 중 압력 · 온도 · 펠릿 밀도 기록 · 조건당 셀 여럿.
⑤ **압력 창** — 0.5 MPa (항복 아래) 는 실패 · 3–7 MPa 는 CCS 가 압력과 함께 오름 · 25 MPa 이상 (doux2020 · 펠릿 87 %) 은 Li 가 SE 기공으로 크리프해 단락. 상한은 SE 기공률이 정한다 — DEM 이 기공률을 주는 쪽이라 이 창을 같이 볼 수 있다 [우리 해석 · 두 논문 연결].

---

## 13. 인용 가능 문장 (영문 초안 · 랩 표기 *Nat. Mater.*, 18, 1105 (2019).)

- "In Li|Li₆PS₅Cl|Li cells, the critical current for stripping lies below that for plating: voids accumulate on stripping at current densities well below the plating limit, and dendrites then form on a later plating step (*Nat. Mater.*, 18, 1105 (2019))."
- "At 3 MPa, cells cycled stably at 0.2 mA cm⁻² but failed at 1.0 mA cm⁻²; at 7 MPa, they cycled stably at 1.0 mA cm⁻² and failed at 2.0 mA cm⁻², while the plating limit (2.0 mA cm⁻²) did not change with pressure (*Nat. Mater.*, 18, 1105 (2019))."
- "Voids formed at the Li|Li₆PS₅Cl interface even at stack pressures above the yield strength of Li (*Nat. Mater.*, 18, 1105 (2019))."
- ⛔ 쓰지 말 것: "CCS = 0.2 mA cm⁻²" 처럼 압력 · 정의 없이 숫자 하나 · "creep, not diffusion, supplies Li to the interface" 를 확정 사실로 · "cells can be cycled indefinitely below the CCS".

---

## 14. 주의 / 한계 (인용 규율)

- CCS 를 숫자로 옮길 때는 **압력과 정의 (안전하게 돈 값인지 처음 실패한 값인지)** 를 같이 쓴다. 권장 꼴: *"stable at 0.2 (3 MPa) and 1.0 mA cm⁻² (7 MPa); failure at 1.0 and 2.0 mA cm⁻²"*.
- 조건마다 셀 하나 · 오차 없음 — '값' 이 아니라 '괄호' 로 쓴다.
- LPSCl 값이다 — LLZO (wang2019 · sharafi2017 · fuchs2023) · Na (이 논문 `Fig. S7`) 값과 섞지 않는다.
- 운전 온도 미기재 — 'room temperature' 로 적지 않는다 (EIS 에 25 °C 만 있다).
- 압력은 조립 때의 명목값이고 기준 면적이 없다.
- 'creep dominates' 는 저자 해석이다 — 정량 근거가 없다.
- 덴드라이트 판정은 SEM 명암이다.
- 우리 W 값과 같은 줄에 놓지 않는다 (이 논문에 W 가 없다) · 문헌 수치를 우리 db 절대값과 섞지 않는다.

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 (이 digest 에서) |
|---|---|
| CCS (critical current for stripping) | 이보다 큰 전류로 벗기면 계면에 Li 를 대는 속도가 못 따라와 Li 쪽에 공극이 생기는 전류 밀도 |
| CCP (critical current for plating) | 이보다 큰 전류로 입히면 덴드라이트가 생기는 전류 밀도 |
| CCD (critical current density) | 흔히 2 전극 대칭셀에서 전류를 올려 가며 단락이 나는 전류 — 박리 · 도금이 섞인다 (이 논문이 가르려 한 것) |
| 3 전극 셀 | 작업극 (WE) · 상대극 (CE) · 기준극 (RE). WE–RE 전위로 한 극의 분극만 본다 |
| 분극 (polarization) | 전류를 흘릴 때 전위가 평형에서 벗어난 크기 (여기선 mV) |
| 면적 용량 (mAh cm⁻²) | 단위 면적당 흘린 전하. Li 1 mAh cm⁻² ≈ 4.85 µm |
| 적층압 (stack pressure) | 셀을 위아래로 누르는 압력 — 여기선 스프링 클램프로 맞춘 명목값 |
| 항복 강도 | 영구 변형이 시작되는 응력 — 상온 Li 는 0.73–0.81 MPa (인장 · 변형 속도 10⁻³ s⁻¹) |
| 크리프 | 일정 응력에서 시간에 따라 계속 변형되는 것. 거듭제곱 크리프는 ε̇ ∝ σⁿ (Li n ≈ 6.56 · 전위 상승) · 확산 크리프는 ε̇ ∝ σ (원자 확산이 나른다) |
| 공극 (void) · 갇힌 공극 (occluded void) | 박리로 계면 Li 쪽에 생긴 빈 공간 · 도금 막이 덮어서 계면에서 떨어져 Li 속에 남은 공극 |
| 삼중점 | Li · SE · 공극 (또는 기공) 이 만나는 선 — Li⁺ 와 전자가 같이 닿는 자리 |
| 전류 수축 (constriction) 저항 | 접촉이 일부뿐이면 전류가 좁은 곳으로 몰리며 생기는 추가 저항 |
| EIS · Nyquist · CPE | 작은 교류로 주파수별 저항을 재는 법 · −Z″ 대 Z′ 그림 · 이상적이지 않은 축전기 소자 |
| XCT | X 선 단층 촬영 — 감쇠 차로 내부를 본다 (Li · 공극 둘 다 감쇠가 낮다) |
| XPS | X 선 광전자 분광 — 표면 수 nm 의 화학 상태 |
| SEI | 고체전해질과 Li 사이에 생긴 반응층 (여기선 Li₂S 우세) |

---

## 16. 이어 먹일 문헌 — litdb 대조 2026-11-24 (최근 2 년 먼저 · Crossref 메타로 서지 확인 · 본문 안 봄)

| # | 논문 | 왜 | litdb · 목록 |
|---|---|---|---|
| 1 | Neudecker, Mauersberger & Jossen · *J. Electrochem. Soc.* 173, 220508 (2026) — "Modeling Current Constriction at the Lithium Anode Interface in Solid-State Battery Cells" · DOI 10.1149/1945-7111/aebfc9 | 이 논문이 '없다고 가정한' 전류 수축 — DEM 접촉 → 국부 전류 변환의 모델 쪽 | 없음 · 목록 없음 |
| 2 | Banerjee, Vishnugopi, Lin & Mukherjee · *Adv. Sci.* e78028 (2026 · 권 미정) — "Mechanistic Insights Into Instability From Single Void Dynamics at the Lithium Metal‐Solid Electrolyte Interface" · DOI 10.1002/advs.78028 | 공극 하나의 성장 · 닫힘 동역학 | 없음 · 목록 없음 |
| 3 | Banerjee, Vishnugopi & Mukherjee · *Adv. Sci.* 13, e15827 (2026) — "Probing the Impact of Vacancy Diffusion on Void Dynamics at the Lithium Metal–Solid Electrolyte Interface" · DOI 10.1002/advs.202515827 | 이 논문이 정량 안 한 '확산 쪽' | 없음 · 목록 없음 |
| 4 | Duan, Feng, Lin, Ye, Li, Wen, Chen & Wei · *Adv. Sci.* 13, e17361 (2026) — "Thickness‐Dependent Creep in Lithium Layers of All‐Solid‐State Batteries under Stack Pressures" · DOI 10.1002/advs.202517361 | 40 µm 박의 크리프는 벌크와 다르다 (§3h 의 응력 눈금 문제) | 없음 · 목록 없음 |
| 5 | Kravchyk, Klimpel & Kovalenko · *Matter* 8, 102376 (2025) — "Critical current density measurements of Li/solid-state electrolyte anodes: Time for a rethink" · DOI 10.1016/j.matt.2025.102376 | CCD · CCS 측정 정의 · 프로토콜 (§10-①②) | 없음 · 목록 없음 |
| 6 | Qu, Huang, Chen, Fu, Chang, Li, Gao & Lin · *ACS Appl. Mater. Interfaces* (2025 · acsami.5c10071 · 권 · 쪽 미확인) — "How Stacking Pressure and Temperature Regulate Lithium Plating and Stripping in Solid-State Lithium Metal Batteries" · DOI 10.1021/acsami.5c10071 | 압력 × 온도 지도 — 크리프 대 확산을 온도로 가르는 쪽 | 없음 · 목록 없음 |
| 7 | Li G., … Xu Z. · *Adv. Mater.* 37, 2417770 (2025) — "Decoding Chemo‐Mechanical Failure Mechanisms of Solid‐State Lithium Metal Battery Under Low Stack Pressure via Optical Fiber Sensors" · DOI 10.1002/adma.202417770 | 운전 중 압력 · 변형 측정 — 이 논문의 '압력은 조립 때 한 번' 빈칸 | 없음 · 목록 없음 |
| 8 | Spencer Jolly, Ning, Hartley, Liu, Melvin, Adamson, Marrow & Bruce · *ACS Appl. Mater. Interfaces* 13, 22708 (2021) — "Temperature Dependence of Lithium Anode Voiding in Argyrodite Solid-State Batteries" · DOI 10.1021/acsami.1c06706 | **같은 그룹 직계 후속** — 이 논문 결론 (크리프) 을 온도로 시험한 쪽 (2021 이라 최근 2 년 밖) | 없음 · 목록 없음 |

이미 `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` 에 있는 것 (다시 안 넣음): Roach et al. 2025 *Eur. J. Mech. A/Solids* 113, 105710 (Li 크리프 공극 연속체) · Li K. 2025 *ACS AMI* 17, 3146 · Haslam 2025 *Adv. Energy Mater.* 15, 2403614 · Ning 2021 *Nat. Mater.* 20, 1121 · Ning 2023 *Nature* 618, 287 · Krauskopf 2019 *ACS AMI* 11, 14463 (이 논문 ref 26) · Spencer Jolly 2020 *ACS AMI* 12, 678 (이 논문이 예고한 Na 후속) · Lewis 2021 *Nat. Mater.* 20, 503.
그 밖 (≤ 2024 · 목록 없음): 이 논문 ref 36 Wang, Wolfenstine & Sakamoto 2019 *Electrochim. Acta* 296, 842 (Li|LLZO flux balance — 공급 = 확산 + 크리프 틀의 원전 · 🏷 Jeff Sakamoto 공저).

---

## 17. litdb 안에서 이 논문을 인용하는 카드 — 숫자 대조 (2026-11-24 · 남의 digest 는 안 고쳤다)

| 카드 | 거기 적힌 것 | 이 논문과 |
|---|---|---|
| `yang2021_flat_li_stripping_lithiophilic_interface_design` (156 · 209 행) | Li/Li₆PS₅Cl J_C 2 × 10⁻⁴ (3 MPa) · 1 × 10⁻³ A cm⁻² (7 MPa) | 맞다 (초록 쪽 '안전 값') |
| `liang2026_interface_bottleneck_solid_state_batteries` (196 행) | 임계 스트리핑 전류 @3 MPa 0.2 mA cm⁻² | 맞다 (초록 쪽) |
| `deysher2022_transport_mechanical_aspects_assb_review` (93 행) | strip 0.2 (3 MPa) / 1.0 (7 MPa) · plate 2.0 | 맞다 (초록 쪽) |
| `banerjee2020_interfaces_interphases_assb_review` (173 행) | 0.5 · 3 · 7 MPa · 7 MPa 1 mA cm⁻² 100 사이클 불변 · 2 mA cm⁻² 단락 · 유속 균형 | 맞다 |
| `seymour2021_void_suppression_interfacial_adhesion_vacancy_transport` (53 · 203 · 293 · 533 행) | ref 28 = 이 논문 → '~1 mA cm⁻² 에 ~10 MPa' · 'Li/LLZO 는 큰 압력 없이 공극' | ⚠ 둘 다 이 논문 값 · 계와 안 맞는다 (§7d) — 원 논문 문장 확인 필요 |
| `wang2019_li_se_interface_dynamics_stack_pressure_current_density` (38 행) · `comparison_vs_ours_DEM.md` I-15 · `cronau2022_wet_milling_particle_size_ionic_conductivity` (76 행) | 'Kasemchainan 2019 — 카드 없음' | 이제 있다 → 메인 세션이 링크로 바꿀 자리 |
| `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` · `chatterjee2025_…` · `sandoval2025_…` · `he2023_halogen_chemistry_solid_electrolytes` · `yang2021_atomistic_…` | 공극 → 갇힌 공극 → 누적 · CCS/CCP 용어 · 삼중점 도금 | 기전 서술이 맞다 (`Fig. 4`) |
| `tron2023_…` (316 행) · `lee2022_thin_insitu_li_void_rewetting_llzo` (500 행) · `wang2024_hot_pressed_lpscl_pressure_invariant_conductivity` (299 행) | 참고문헌 목록의 한 줄 | 해당 없음 |
