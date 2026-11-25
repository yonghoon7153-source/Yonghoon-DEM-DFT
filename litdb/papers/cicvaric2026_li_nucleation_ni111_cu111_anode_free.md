<!-- digest 표준 양식 (paper-level STANDALONE). 2026-11-24 작성 — 병렬 실행: 이 파일과 litdb/figures/<slug>/ 만 썼다
     (INDEX · comparison · pdf_map 은 메인 세션이 병합 · git 은 안 건드렸다).
     ① 크롭 14장 (본문 그림 10 + SI 그림 2 + 표 2) 중 그림 12장 전부 실독 · 표 2장은 PDF 텍스트로 전사
     ② Fig. 8 · Fig. 9 막대 값 · Fig. 10 장벽 값은 그림에 인쇄된 숫자 — 본문 ± 서술 (+0.29/+0.30 · +0.12/+0.20 · +0.46/+0.50 · 0.16 eV) 과 산술 대조해 일치
     ③ 우리 산수 = SI 표면 원자 밀도의 (111) 기하 재계산 · UPD 전하 → Li 면밀도 · 의사형 1ML 변형 · 금속 Li 기준 환산 · C_SEI → 두께 · 홉 수 검산
        (tools/sei/collect_neb.py::hop_check 로 냄 · 교과서 상수 2 개 (E_coh(Li) 1.63 eV · bcc Li a 3.51 Å) 는 논문 밖 값이라 쓰는 곳마다 표시)
     ④ 1저자 질문 "친Li 판정을 흡착 에너지로 했나 · 점착/젖음각으로 했나" = §0 에 박음 · W_ad 보고서 §7 연결 = §7b · §8 -->

# Electrochemical and computational insights into lithium nucleation at Ni(111) and Cu(111) surfaces for anode-free Li-metal batteries — Cicvarić et al. (*J. Mater. Chem. A* **2026**, 14, 16784–16795)

> slug `cicvaric2026_li_nucleation_ni111_cu111_anode_free` · DOI `10.1039/d6ta00180g` · type `mixed — exp (CV · 정전위 EIS · AFM) + DFT (VASP PBE+D3(BJ) 흡착 에너지 · CI-NEB · PDOS)` · PDF `litdb/inbox/nicu2026_li_nucleation_ni111_cu111_main.pdf` (본문 12 pp · 그림 10 · 표 2 · refs 55) + `litdb/inbox/nicu2026_li_nucleation_ni111_cu111_SI.pdf` (SI 4 pp · 그림 S1–S2 · 단층 덮임 유도) · digested `2026-11-24` · status ✅ · 태그 **[외부]** · ⛔ 물성 4축(A–D) 진입 금지 — 계가 액체 전해질 | Cu·Ni 단결정이다

> elements: Li, Cu, Ni
> methods: DFT, PBE, PAW, PDOS, NEB

> **저자**: Katarina Cicvarić (TUM) · Lars Mannich (TUM) · Susana Suttor (TUM + **BMW AG**, München) · Wang Hu (TUM) · Vitaly Alexandrov (Univ. of Nebraska–Lincoln, Chemical and Biomolecular Engineering) · **Aliaksandr S. Bandarenka\*** (TUM 물리학과 Physics of Energy Conversion and Storage, Garching — 교신) · 투고 2026-01-07 · 수락 2026-03-03 · 출판 2026-03-12 · **OA CC BY 4.0** · 자금 DFG Excellence Cluster "e-conversion" (EXC 2089/1 – 390776260) + TUM Laura Bassi 장학금 · 데이터 "교신저자에게 요청 시" (**DFT 구조 파일 비공개**) · 저자 기여 절 없음 → 누가 DFT 를 했는지 PDF 에 없다.
> (Jeff Sakamoto 는 저자가 아니다.)
>
> **계보 (PDF 안에서 확인되는 것만)**: 같은 그룹 Cu(111) 편 = ref 25 (Cicvarić *et al.*, *J. Phys. Chem. C* 130, 1096 (2026)) — **k_app 유도와 덮임별 흡착 계산법은 거기 있고 이 논문은 "our prior publication" 이라며 넘긴다** → 이 논문 = 그 방법의 Ni(111) 확장. 같은 그룹 ref 31 (펄스 전류 형성, *Phys. Chem. Chem. Phys.* 26, 14713 (2024)). 대조 문헌: ref 22 (= ref 50, **같은 논문이 두 번 인용됨**) Pande & Viswanathan *ACS Energy Lett.* 4, 2952 (2019) — Ni(111) 흡착이 더 세서 Cu(111) 장벽이 더 낮다 (BEP) → 이 논문 NEB 가 반박 · ref 16 Kim *et al.* *Energy Environ. Sci.* 17, 6521 (2024) — Cu(111) 장벽이 이 논문과 "very good agreement" (수치는 본문에 없음).
>
> 🎤 **관련 발표**: 없음 — talks 인입 대기열 (`talks/lee2026_skku_mlip_materials_design.md`) 미등재 · `kb/` 언급 0 (2026-11-24 grep).
>
> **이 digest 를 연 이유**: W_ad 보고서 (`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` **§7 "Li 친화성 정량화"**) 의 세 지표 — ① Li 원자 흡착 에너지 · ② Li 금속 점착 → 젖음각 · ③ 합금 구동력 — 중 이 논문이 무엇을 주는지 확인하고, ① 에 금속 (111) 기준점을 댄다. (우리 W 값은 이 문서에 싣지 않는다 — 위치만.)

> **본 그림 (2026-11-24)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` `Fig. 7` `Fig. 8` `Fig. 9` `Fig. 10` `Fig. S1` `Fig. S2` — **크롭 그림 12장 중 12장**. 표 `Table 1` · `Table 2` 는 이미지로 안 보고 PDF 텍스트로 전사했다.
> `Fig. 8` · `Fig. 9` 막대 값과 `Fig. 10` 장벽 값은 **그림에 인쇄된 숫자**라 figure-read 가 아니다 (본문 ± 서술과 산술 일치 확인). 그 밖에 그림에서만 읽은 값 = **`figure-read ≈`** · 우리가 계산한 값 = **`우리 산수`**.
> **본문과 어긋난 그림 셋**: `Fig. 6` (본문 "two orders of magnitude" ↔ figure-read **10–40×**) · `Fig. 5` (Cu·Ni 차이 주장 ↔ **오차 막대가 모든 전위에서 겹침**) · `Fig. 2c` (y 축 "related to a single site" ↔ 나머지 세 패널 "average site"). → §10.

---

## 0. 이 digest 를 읽는 법 — 친Li 를 무엇으로 판정했나 (1저자 질문)

> 🔑🔑 **친Li (lithiophilicity) 판정은 Li 원자 흡착 에너지 하나로 했다. 점착 에너지 (W_ad) 도 젖음각도 계산하지 않았고, 측정하지도 않았다.**

| 묻는 것 | 이 논문 | 위치 |
|---|---|---|
| 판정 문장 | *"Ni(111) exhibits higher lithiophilicity than Cu(111) as the adsorption energy on the former is lower (more negative values)"* | 초록 · p.16789 |
| 흡착 에너지 정의 | **E_ads = E_nLi@surf − E_surf − n × E_Li** · E_Li = *"the single Li atom"* = **고립 (기상) Li 원자** · 세 항 모두 "extrapolated to 0 K" 총에너지 | §4.4 (p.16793) |
| 쓰인 세 층 | ① 단일 Li 원자 4 자리 (`Table 1`) ② 1층 덮임 θ 0.04 → 1 의 평균 흡착 (`Fig. 8`) ③ 1ML Li 위 둘째 층 (`Table 2` · `Fig. 9`) + 확산 장벽 (`Fig. 10`) | p.16789–16791 |
| Li 금속 슬랩 \| 기판 **점착 에너지** | **없음** | — |
| **젖음각** (계산 · 측정) | **없음** | — |
| **금속 Li 기준** (핵생성 에너지 · E_coh(Li)) | **없음** — E_coh(Li) 를 안 낸다 ⇒ *"Li 가 자기 자신보다 기판에 더 붙나"* 를 이 논문 숫자만으로는 못 읽는다 (§3f 우리 산수 · §10-③) | — |
| **합금 구동력** | **없음** — Cu · Ni 는 Li 와 합금을 만들지 않는 집전체 (서론: 0–3 V vs Li/Li⁺ 에서 *"electrochemically inactive"*) | p.16784 |
| 실험 쪽 친Li 신호 | **UPD 덮임** (CV 피크 전하 적분): Cu ≈ ⅓ ML · Ni ≈ 1 ML (SI p.S2) — 이것도 젖음이 아니다 · ⚠ 그 Γ 값에 산술 문제 (§10-①) | `Fig. 1` · SI |
| 보조 근거 | PDOS d-band (`Fig. 7`) · NEB 장벽 (`Fig. 10`) | p.16790–16791 |

⇒ **W_ad 보고서 §7 의 세 정량화 중 ① (흡착 에너지) 만 이 논문에 있다.** ② 점착 → 젖음각 · ③ 합금 구동력은 0 이다. 이 논문이 "친Li" 라고 부르는 것은 **고립 원자 기준 흡착 에너지의 크기 순서**이고, 그 순서조차 **둘째 층에서는 뒤집힌다** (§3h).

---

## 1. 한 줄 요약

Cu(111) · Ni(111) 단결정 위 Li 초기 석출을 −5…−25 mV (vs Li/Li⁺) 정전위 3600 s 동안 EIS 로 따라가면 **Ni 쪽 겉보기 속도계수 k_app 가 Cu 보다 2–4× 낮고** (figure-read 2.2–3.9×) AFM 상 **입자가 더 크고 매끈하다** (추세선 기준 · 오차 막대는 전부 겹침). DFT (VASP · PBE + D3(BJ)) 는 **고립 Li 원자 기준 흡착 에너지가 Ni(111) 에서 0.12–0.28 eV 더 음수**라 Ni 가 "더 친Li" 라 하고, **1ML Li 위 둘째 층에서는 반대로 Cu 가 0–0.12 eV 더 세게 잡으며 장벽도 Cu 20 vs Ni 12 meV** 라 Ni 위에서 Li 가 기존 덩어리로 옆으로 잘 모인다고 엮는다. ⚠ 친Li 판정은 **흡착 에너지 하나** — 점착 · 젖음각 · 금속 Li 기준 · 합금이 전부 없고, 장벽은 전부 kT 아래라 (홉 대기 ≈ 0.2 ps · 우리 산수) 저자 스스로 *"slow surface diffusion processes may not be the predominant source of dendritic growth"* 라고 쓴다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 비교 쌍 | **Cu(111) vs Ni(111) 단결정** (MaTeck GmbH · 지름 15 mm × 두께 3 mm · HDPE 홀더 구멍 13 mm → 노출 **1.3 cm²**) |
| 전해질 | **1 M LiPF₆ in EC : EMC 3 : 7 (wt)** (E-Lyte) · 25 °C |
| 셀 | 3 전극 — WE 단결정 · CE **LFP** (Al 위 83 µm LiFePO₄, PI-KEM, 지름 14 mm 원판, 홀더 구멍 12 mm) · RE **Li 금속** · Ar 글러브박스 (MBraun MB 200B) · PalmSens4 |
| 던지는 질문 | 무음극 Li 금속 전지 (AFLMB) 집전체로 **Ni 가 Cu 보다 나은가** — 초기 Li 석출의 국소 속도 (k_app) · 형상 · SEI · 원자 단위 흡착 / 확산 |
| 문헌 갭 | Cu 는 원자 ~ 거시 단위로 많이 연구됨 (Cu(111) 수평 · 균일 성장 · Cu(001) 장벽 > Li(001) · 입계 확산 · 층간 확산) · **Ni 위 Li 석출은 "largely unexplored"** · Pande & Viswanathan 은 Ni(111) 흡착이 더 세서 Cu(111) 장벽이 더 낮다고 예측 |
| 집전체 물성 (서론, 문헌 인용) | 전자 전도도 Cu ≈ 59 > Ni 14.4 > Ti 2.5 > SS 1.4 (×10⁶ S m⁻¹) · 열전도 Cu ≈ 400 > Ni ≈ 90 > SS 15–25 > Ti ≈ 22 W m⁻¹ K⁻¹ · Ni = 넷 중 인장강도 최고 · *"the lowest cost (in 2025)"* (ref 12 = 2023 Ni 박막 논문 · ⚠ §10-⑫) · Ni 가 LiPF₆ 탄산염 전해질에서 Cu 보다 부식 저항 (refs 13 · 14) |
| 단결정을 쓴 이유 | 입계 · 결함 효과를 빼려고 — 대신 **다결정 박 (입계 · 자연 산화막) 으로의 이전은 미검증**이라고 결론에서 스스로 적는다 |
| 선행 | 같은 그룹 Cu(111) 편 (ref 25) — 이 논문 Cu 쪽 결과는 그 기준점 위에 있다 |

---

## 3. 핵심 수치 총정리 ★

> 전위는 전부 **vs Li/Li⁺** (Li 금속 RE). "과전압" = 인가 정전위 −5…−25 mV 다 (갈바노스태틱 핵생성 과전압이 아니다 — §4b).

### 3a. SEI 형성 CV · UPD (`Fig. 1` · SI p.S2)

| 항목 | Cu(111) | Ni(111) | 출처 |
|---|---|---|---|
| SEI 형성 CV | 10 회 · 3.55 ↔ 0 V · **50 mV s⁻¹** · OCV 에서 0 V 쪽으로 시작 | 같음 | p.16785 · §4.2 |
| 1st scan 귀속 | Menkin 2021 따라: 2.5–3.1 V CuF₂ 환원 (→ LiF + Cu) · 2.5–1.5 V Cu 산화물 환원 · CuₓO 리튬화 · LiF · ≈ 0.5 V Li₂CO₃ → Li₂C₂ + Li₂O | **문헌 귀속 없음** — *"we assume that SEI components are forming, with an additional UPD-related peak at ca. 1.0 V"* | p.16785 |
| 1st scan 환원 피크 | `figure-read ≈` 2.2 V (−188 µA) · 1.9 V 어깨 · 1.1 V · **0.45 V (−160 µA)** | `figure-read ≈` 2.0 V (−111 µA) · 1.55 V (−110) · 1.05 V (−72) · **0.52 V (−120)** · 0.3 V (−85) | `Fig. 1a,b` |
| 안정 SEI 도달 | 2nd 회 이후 | 1st 회 이후 | p.16785 |
| 안정 회차 UPD | 환원 **≈ 0.5 V** · 산화 (탈리) **≈ 0.9 V** (`figure-read ≈` 0.82 V, +22 µA) | 약한 **2.3 · 2.0 · 1.1 · 0.8 V** + 뚜렷한 **0.25 V** (`figure-read ≈` −57 µA) · 산화 **≈ 0.5 · ≈ 1.6 V** (`figure-read ≈` +28 · +40 µA) — *"multiple UPD stages represent different modes of adsorption"* | p.16785 · `Fig. 1` |
| UPD 전하 Q_exp | **≈ 100 µC** (환원 피크) | **≈ 300 µC** (환원 · 산화 둘 다) | p.16785 |
| 단층 전하 Q_ML (SI) | Γ_ML = 1.39×10¹⁵ cm⁻² / N_A = 2.31×10⁻⁹ mol cm⁻² → ×F×1.3 cm² = **290 µC** | 1.48×10¹⁵ → 2.46×10⁻⁹ → **310 µC** | SI p.S2 (1.39 / 1.48 값 자체의 출처는 안 적혀 있다 · 식에 달린 각주 i 는 분자 촉매 리뷰 · §10-①) |
| **θ = Q_exp/Q_ML (논문)** | **≈ ⅓** | **≈ 1** | SI |
| ⚠ θ — (111) 기하 밀도로 다시 (`우리 산수`) | 4/(√3 a²), a = 논문 DFT 3.63 Å → **1.75×10¹⁵ cm⁻²** → Q_ML 365 µC → **θ ≈ 0.27** | a = 3.52 Å → **1.86×10¹⁵** → 388 µC → **θ ≈ 0.77** | §10-① |
| Li 면밀도 (`우리 산수`) | Q_exp → **4.8×10¹⁴ cm⁻²** = bcc Li(110) 면의 0.42 층 | **1.44×10¹⁵ cm⁻²** = Li(110) 면의 **1.25 층** · 조밀 육방 Li 층의 1.15 층 | bcc Li a = 3.51 Å (교과서 · 논문 밖) |

> 🔑 Ni 의 "full monolayer" 는 **기판 원자 1 : Li 1 (의사형) 단층** 정의다. 같은 전하를 **Li 금속 자신의 조밀면으로** 세면 1 층을 넘는다 (1.15–1.25 층 · 우리 산수) — 300 µC 가 전부 Li UPD 라면 단층 흡착으로 설명하기 어렵다 (§10-②).

### 3b. 겉보기 속도계수 k_app (`Fig. 2`)

> k_app(t, E) = √(2D) · A_W(t, E) / R_CT(t, E) (식 1) · D = 1×10⁻¹⁰ m² s⁻¹ (EC:EMC 속 Li⁺, ref 29 문헌값 · 고정) · A_W = Warburg 계수 · R_CT = 전하이동 저항 · 전위당 26 스펙트럼 / 3600 s.
> 단위 1e−2 cm s⁻¹. 캡션: *"average k_app … after stabilisation (2000 s) with standard deviation as error bars"* → **2000 s 이후 점들의 평균과 그 산포**로 읽힌다 — 반복 시료 사이 편차라는 말은 없다 (반복 실험 자체가 미기재).

| 전위 | Cu(111) 평균 k_app (`figure-read ≈`) | Ni(111) (`figure-read ≈`) | Cu / Ni (`우리 산수`) |
|---|---|---|---|
| −5 mV | **1.59 ± 0.06** | **0.403 ± 0.017** | **3.9** |
| −10 mV | 0.70 ± 0.04 | 0.323 ± 0.016 | 2.2 |
| −15 mV | 0.585 ± 0.04 | 0.207 ± 0.015 | 2.8 |
| −20 mV | 0.59 ± 0.07 | 0.168 ± 0.008 | 3.5 |
| −25 mV | 0.47 ± 0.10 | 0.154 ± 0.007 | 3.1 |

- 본문 *"Compared to Cu(111), values of k_app are 2 to 4 times lower and show a more linear decrease with increasing potential"* — 그림과 맞다.
- **Cu 는 −5 → −10 mV 사이에서 한 번에 ≈ 2.3× 떨어지고** 그 뒤는 완만 · Ni 는 거의 직선으로 감소.
- 시간 거동 (본문 + `figure-read ≈`): Cu −5 mV 는 0 s ≈ 1.22 → **≈ 300 s 최대** (한 점 ≈ 2.0, 추세선 ≈ 1.85) → 3600 s ≈ 1.55 로 완만히 감소 · 나머지 전위는 **≈ 500 s 까지 떨어진 뒤 평탄** (−10 ≈ 0.72 · −15 ≈ 0.62 · −20 ≈ 0.60 · −25 ≈ 0.47). Ni −5 mV 1.18 → 300 s ≈ 0.6 → 3600 s ≈ 0.39 · −10 mV 0.72 → ≈ 0.47 → ≈ 0.29 · −15 mV 0.34 → ≈ 0.22 → ≈ 0.21 · **−20 · −25 mV 는 처음부터 ≈ 0.17 · ≈ 0.16 평탄**.
- 해석 (논문): k_app = (n₁k₁ + … + nᵢkᵢ)/n_total (식 2, 자리 가중 평균) → 과전압 · 시간이 늘면 **느린 (덜 활성) 자리 기여가 커져** k_app 가 준다 + 전극 근처 **이온 고갈층**.

### 3c. 형상 — AFM 입자 면적 · 거칠기 (`Fig. 3` · `Fig. 4` · `Fig. 5`)

| 전위 | 입자 면적 Cu / Ni (µm², `figure-read ≈`) | 평균 거칠기 Cu / Ni (nm, `figure-read ≈`) |
|---|---|---|
| SEI 만 (석출 전) | — | **≈ 26 / ≈ 19** (본문 명시) |
| −5 mV | (Ni 표식에 가림) / 0.027 | 27 / 22 |
| −10 mV | 0.05 / 0.07 | 26 / 11 |
| −15 mV | 0.15 / 0.14 | 37 / 18 |
| −20 mV | 0.145 / 0.16 | 31 / 18 |
| −25 mV | 0.21 / **0.31** | 38 / 31 |

- 오차 막대 (`figure-read ≈`): 면적 ±0.02–0.18 µm² · 거칠기 ±6–21 nm — **모든 전위에서 Cu · Ni 막대가 겹친다**. 무엇의 표준편차인지 (입자 수 · 영상 수) 캡션에 없다.
- 본문 결론 *"Li deposits on Cu(111) have a smaller grain size and are rougher"* 는 **두 선형 추세선의 차이**다. −15 mV 에서는 면적이 오히려 Cu ≥ Ni.
- 거칠기 차 (Li 석출 후 ≈ 5–15 nm) 는 **SEI 만 있을 때 이미 있던 차 (≈ 7 nm)** 와 같은 크기다 (§10-⑦).

### 3d. SEI 커패시턴스 C_SEI (`Fig. 6` · `Fig. S1` · `Fig. S2`)

| 전위 | Cu(111) C_SEI (×10⁻⁵ F, `figure-read ≈`) | Ni(111) C_SEI (×10⁻⁴ F, `figure-read ≈`) |
|---|---|---|
| −5 mV | 0.5 → ≈ 0.85–1.03 (**시간에 따라 상승**) | 1.74 → ≈ 1.0 |
| −10 mV | ≈ 0.53 → ≈ 0.45 | 1.67 → ≈ 0.98 |
| −15 mV | ≈ 0.33 → ≈ 0.30 | 1.64 → ≈ 1.0 |
| −20 mV | ≈ 0.43 → ≈ 0.29 | 1.26 → ≈ 0.92 |
| −25 mV | ≈ 0.27 → ≈ 0.25 | 1.23 → ≈ 1.04 |

- 본문 *"SEI capacitance on Cu(111) is lower by **two orders of magnitude** than that on Ni(111), signifying the formation of a thicker SEI film"* ↔ **2000 s 이후 비는 ≈ 11× (−5 mV) … ≈ 40× (−25 mV) = 1.0–1.6 자릿수** (`figure-read ≈` · `우리 산수`).
- 면적당 (`우리 산수`, 1.3 cm²): Ni ≈ **77 µF cm⁻²** · Cu ≈ 1.9–6.9 µF cm⁻².
- 평판 막으로 읽으면 (`우리 산수` · C = ε_r ε₀ A / d · **ε_r = 10 가정 — 논문에 없음**): Ni **≈ 0.1 nm** · Cu ≈ 1.3–4.6 nm → Ni 쪽 값은 막 두께로 읽을 수 없는 크기다 (§10-⑥).
- EEC 적합 RMS 편차 *"typically in the range of a few percent"* (SI).
- Cu 는 −5 → −10 mV 에서 제일 크게 떨어지고 −15 mV 이후 안정 · Ni 는 −5…−15 mV 에서 초반 하강 후 안정, −20 · −25 mV 는 처음부터 거의 안정 (본문 · 그림 일치).

### 3e. DFT — 맨 (111) 면 위 단일 Li 원자 (`Table 1`)

| 자리 | **배위 (자리 이름)** | Cu(111) (eV) | Ni(111) (eV) | Ni − Cu |
|---|---|---|---|---|
| top | 1 | −2.51 | −2.79 | −0.28 |
| bridge | 2 | −2.62 | −2.88 | −0.26 |
| hollow (hcp) | 3 | **−2.63** | **−2.89** | −0.26 |
| hollow (fcc) | 3 | **−2.63** | **−2.89** | −0.26 |

- 기준 = **고립 Li 원자** · 이 비교에서는 **Li 를 z 방향으로만 이완** (§4.4).
- **배위 (CLAUDE.md 규칙)**: 결합 자리는 정상 (111) 테라스의 1 · 2 · 3 배위 자리다 — **단글링 본드 · 결함 자리가 아니다**. 구조 파일은 비공개 ("요청 시") 라 이완 뒤 Li–M 거리 · 높이는 **미확인**.
- 자리 주름 (`우리 산수`): top − hollow = Cu 0.12 · Ni 0.10 eV · bridge − hollow = 0.01 / 0.01 eV (소수 2 자리 반올림 안) → `Fig. 10a` 장벽 13 / 11 meV 와 정합.
- 가장 안정한 자리 = hollow (hcp = fcc, 2 자리 표기에서 같음) → 이후 1ML 의 첫 층 Li 는 **fcc hollow** 에 둠 (*"selected for simplicity"*).
- **금속 Li 기준 환산** (`우리 산수` · 교과서 실험값 **E_coh(Li) = 1.63 eV/원자 — 논문 밖 · 그들의 PBE+D3 E_coh 는 n/a**): hollow 에서 Cu ≈ **−1.00** · Ni ≈ **−1.26 eV** (bulk Li 보다 그만큼 안정). D3 는 금속 Li 응집에도 더해지므로 **차수 확인용**이다.

### 3f. DFT — 1층 덮임 θ 의존 (`Fig. 8`)

> "average adsorption energy" — 식에는 1/n 이 없지만 θ = 1 값 (≈ −2 eV) 으로 보아 **Li 1 개당 평균**이다 (§10-⑫). 셀은 θ 별로 적혀 있지 않다 — 아래 셀 열은 **분수에서 가장 작은 셀로 우리 추정**.

| θ | 셀 (우리 추정) | Cu(111) | Ni(111) | Ni − Cu (`우리 산수`) |
|---|---|---|---|---|
| 0.04 | 1/25 · p(5×5) | **−2.63** | **−2.89** | −0.26 |
| 0.11 | 1/9 · p(3×3) | −2.57 | −2.84 | −0.27 |
| 0.25 | 1/4 · p(2×2) | −2.45 | −2.72 | −0.27 |
| 0.33 | 3/9 · p(3×3) | −2.46 | −2.69 | −0.23 |
| 0.5 | 2/4 · p(2×2) | −2.17 | −2.39 | −0.22 |
| 0.75 | 3/4 · p(2×2) | −2.07 | −2.24 | −0.17 |
| 0.89 | 8/9 · p(3×3) | −2.12 | −2.24 | −0.12 |
| 1 | 1×1 | **−2.05** | **−2.19** | −0.14 |

- 본문 차이값 (그림 숫자와 산술 일치): θ 0.33 → 0.5 **+0.29 (Cu) · +0.30 eV (Ni)** = 최대 변화 · θ 0.5 → 1 +0.12 · +0.20 · θ 0.04 → 0.5 +0.46 · +0.50.
- **θ 0.04 → 1 전체 변화 = +0.58 (Cu) · +0.70 eV (Ni)** (`우리 산수`) — **Cu–Ni 차 (0.12–0.28 eV) 의 2–5 배**. 흡착 에너지 지표의 값은 "어느 자리 · 어느 덮임" 에서 재느냐가 재료 차이보다 크다.
- 비단조 두 곳: Cu θ 0.25 → 0.33 (−2.45 → −2.46) · θ 0.75 → 0.89 (−2.07 → −2.12) — 셀이 p(2×2) ↔ p(3×3) 로 바뀌는 자리다 (배치 · 셀 효과로 보임 · 논문은 언급 없음).
- 해석 (논문): θ 0.33 → 0.5 의 급변 = *"transition toward an energetically less favourable close-packed state"* · 원인은 Li 와 Cu/Ni 의 *"non-negligible lattice mismatch"*.
- 의사형 1×1 Li 의 압축 (`우리 산수` · 논문 DFT a + 교과서 bcc Li a 3.51 Å): Li–Li 거리 Cu 2.567 Å · Ni 2.489 Å vs bcc Li 최근접 3.040 Å → **−15.6 % · −18.1 %** · 면밀도는 Li(110) 면의 **1.53× · 1.62×** → Li 자신의 조밀면에 해당하는 덮임은 θ ≈ **0.65 (Cu) · 0.62 (Ni)** 다. θ ≥ 0.75 는 금속 Li 보다 빽빽한 층이다 (§10-④).
- 금속 Li 기준 (`우리 산수`, E_coh 1.63 eV): θ = 1 에서 Cu ≈ −0.42 · Ni ≈ −0.56 eV — 1층 완성까지는 여전히 bulk Li 보다 안정.

### 3g. DFT — 1ML Li 위 둘째 층 (`Table 2` · `Fig. 9`)

`Table 2` — 1ML Li@M(111) 위 단일 Li 원자 (자리는 1ML 이 유지하는 fcc(111) 면 기준 · z 만 이완):

| 자리 | 1ML Li@Cu(111) | 1ML Li@Ni(111) |
|---|---|---|
| top (첫 층 Li 바로 위) | **−2.06** | **−2.03** |
| bridge | −2.04 | −2.01 |
| hollow (hcp) | −2.03 | −2.01 |
| hollow (fcc) | −2.04 | −2.01 |

- 자리 차이는 **20–30 meV** (*"nearly equivalent for all sites and almost independent of the underlying substrate"*). top 이 *"slightly more energetically preferred"* 라 둘째 층은 **첫 층 Li 꼭대기 (top)** 에 쌓았다 → θ = 1 둘째 층은 **AA 적층** Li 이중층이 된다 (§10-④).
- 첫 층 θ = 1 Li 와 비교 (본문): **Cu 는 차이 없음** (둘째 층 −2.06 vs 첫 층 −2.05) · **Ni 는 첫 층이 0.16 eV 더 낮다** (−2.19 vs −2.03) → *"The lower adsorption strength of the second Li layer could facilitate lateral diffusion of Li adatoms"*.

`Fig. 9` — 둘째 층 평균 흡착 에너지:

| θ (둘째 층) | 1ML Li@Cu(111) | 1ML Li@Ni(111) | Ni − Cu (`우리 산수`) | 금속 Li 기준 Cu / Ni (`우리 산수`, E_coh 1.63) |
|---|---|---|---|---|
| 0.04 | −2.06 | −2.01 | +0.05 | −0.43 / −0.38 |
| 0.11 | −2.00 | −2.00 | 0.00 | −0.37 / −0.37 |
| 0.25 | −1.99 | −1.96 | +0.03 | −0.36 / −0.33 |
| 0.33 | −1.99 | −1.98 | +0.01 | −0.36 / −0.35 |
| 0.5 | −1.78 | −1.70 | +0.08 | −0.15 / −0.07 |
| 0.75 | −1.72 | −1.63 | +0.09 | −0.09 / 0.00 |
| 0.89 | −1.72 | −1.66 | +0.06 | −0.09 / −0.03 |
| 1 | **−1.69** | **−1.57** | **+0.12** | **−0.06 / +0.06** |

- 🔑 **순서가 뒤집힌다**: 첫 층에서는 모든 θ 에서 Ni 가 더 세고 (0.12–0.28 eV), **둘째 층에서는 모든 θ 에서 Cu 가 같거나 더 세다** (0–0.12 eV). θ ≤ 0.33 에서는 기판 무관 (−1.96…−2.06) · θ 0.33 → 0.5 에서 다시 급변.
- 논문 해석: Cu 와 Li 의 격자 부정합이 상대적으로 작아 (Cu a 3.63 > Ni 3.52) 고덮임에서 압축 변형이 덜하다 → Cu 위 둘째 층이 더 유리.
- 금속 Li 기준으로 보면 (`우리 산수`): **둘째 층 완성 (θ = 1) 은 bulk Li 와 거의 같은 에너지** (Cu −0.06 · Ni +0.06 eV) — 즉 이 모형에서 둘째 층부터는 기판의 '친Li' 가 사실상 사라진다. Ni 위 θ = 1 이 bulk Li 보다 약간 불리하다는 것은 UPD 가 1 층 근처에서 멈춘다는 실험과 방향이 맞는다 (단 E_coh 가 논문 값이 아니라 ±수십 meV 수준의 부호 판정은 하지 않는다).
- 표–그림 교차 점검 (`우리 산수`): Ni 둘째 층 단일 원자 — `Table 2` top **−2.03 (z 만 이완)** vs `Fig. 9` θ 0.04 **−2.01 (전 방향 이완)**. 이완을 더 풀었는데 0.02 eV 높다 → 셀이 다르거나 **수치 잡음이 ≈ 0.02 eV**. Cu 는 둘 다 −2.06 으로 같다. 첫 층은 `Table 1` hollow 와 `Fig. 8` θ 0.04 가 Cu · Ni 모두 일치.

### 3h. DFT — 표면 확산 장벽 CI-NEB (`Fig. 10`) + 홉 수 검산

| 경로 | Cu(111) | Ni(111) | 홉률 비 Ni/Cu (298 K, `우리 산수`) |
|---|---|---|---|
| 맨 (111) 면 (hollow → hollow, bridge 경유) | **13 meV** (`figure-read ≈` 그림 표식 14) | **11 meV** | 1.08× |
| 1ML Li 위 (첫 층 Li top → 이웃 top, `figure-read`) | **20 meV** | **12 meV** | 1.37× |

- 셀 p(5×5) · CI-NEB **중간 상 5 개** (그림 상 번호 1–7 = 끝점 2 + 중간 5) · 곡선은 대칭 · Ni 1ML 끝점 7 은 `figure-read ≈` 0.5 meV (0 이 아님).
- 본문: 맨 면은 *"nearly identical"* → Pande 의 BEP 예측 (Cu 가 더 낮다) 과 **불일치** · Kim *et al.* (ref 16) 의 Cu(111) 값과는 *"very good agreement"* (수치 미기재) · 1ML 위에서 Cu 장벽이 *"nearly double that of Ni(111)"* (실제 비 20/12 = **1.67×**) · Ni 는 *"remains unchanged"* (11 → 12 meV).
- 저자 스스로: *"all are found to be lower than the thermal energy at room temperature k_BT ≈ 0.026 eV. Hence, slow surface diffusion processes may not be the predominant source of dendritic growth"*.
- **홉 수 검산** (`tools/sei/collect_neb.py::hop_check` · ν₀ 10¹³ s⁻¹ **가정** · 298 K · 확산계수 · 전도도가 아니다):
  - 11 meV → Γ ≈ 6.5×10¹² s⁻¹ · 평균 대기 ≈ 0.15 ps · 3600 s 동안 N ≈ 2.3×10¹⁶ 회
  - 12 meV → Γ ≈ 6.3×10¹² s⁻¹ · 대기 ≈ 0.16 ps
  - 13 meV → Γ ≈ 6.0×10¹² s⁻¹ · 대기 ≈ 0.17 ps
  - 20 meV → Γ ≈ 4.6×10¹² s⁻¹ · 대기 ≈ 0.22 ps · 3600 s 동안 N ≈ 1.7×10¹⁶ 회
  - ⇒ 두 면 모두 사실상 장벽 없는 확산이고, Cu–Ni 장벽 차 8 meV 는 홉률 1.37× 다. **2.2–3.9× 의 k_app 차이 (10²–10³ s 시간 척도) 를 이 장벽으로 설명할 수 없다** — 차수에서 안 맞는다 (§10-⑤).

### 3i. DFT 기타 · 서론 수치

| 항목 | 값 | 비고 |
|---|---|---|
| 격자상수 (DFT) | **Cu 3.63 Å · Ni 3.52 Å** | *"very good agreement with other DFT"* (refs 45 · 46) · D3 포함 여부 미기재 |
| 표면 에너지 (5 층 수렴) | **Cu(111) 1.31 J m⁻² · Ni(111) 1.92 J m⁻²** | refs 49–51 과 *"good agreement"* · D3 포함 여부 미기재 |
| D(Li⁺, EC:EMC) | 1×10⁻¹⁰ m² s⁻¹ | ref 29 (Capiglia 1999) · 모든 전위 · 두 금속에 같게 |
| 노출 면적 | 1.3 cm² | 13 mm 구멍 (`우리 산수` π·0.65² = 1.33 cm²) |

---

## 4. DFT / 계산 방법 ★

| 항목 | 이 논문 | 미기재 · 주의 |
|---|---|---|
| **code** | **VASP** (refs 40 · 41) | 판 미기재 |
| **functional** | **GGA-PBE** | — |
| **vdW** | **DFT-D3 + Becke–Johnson 감쇠 (D3(BJ))** — *"for all adsorption energy and surface diffusion calculations"* | **3 체 (ATM) 항 미기재** · 격자상수 · 표면 에너지 계산에 D3 를 켰는지 미기재 |
| **pseudo** | **PAW** (Li · Cu · Ni) | Li 의 1s 를 원자가로 넣었는지 (Li_sv) 미기재 |
| **ecut** | **500 eV** (총에너지 수렴) | — |
| SCF / 힘 | SCF 10⁻⁶ eV · 힘 < **10⁻² eV Å⁻¹** | 힘 기준 0.01 eV/Å 는 10 meV 단위 장벽 차를 가르기에 빠듯하다 |
| **smearing** | *"extrapolated to 0 K"* (σ → 0 외삽 에너지) | 방식 · 폭 미기재 |
| **spin** | **Ni 계만 스핀 분극** | Cu 계 비스핀 · **고립 Li 원자 기준의 스핀 처리 미기재** (§10-⑬) |
| **슬랩** | (111) 면 · **5 층** · **위 3 층 이완 · 아래 2 층 고정** · **진공 15 Å** | **쌍극자 보정 미기재** (한쪽 면에만 Li → 비대칭 슬랩) |
| **면내 셀 · k 점** | **p(2×2) ↔ Γ 13×13×1 · p(3×3) ↔ Γ 9×9×1 · p(5×5) ↔ Γ 5×5×1** | 셀 × k ≈ 25–27 로 **k 밀도는 일관** (`우리 산수`) · θ 별 셀 · 배치는 미기재 |
| **Li 흡착 자리** | top · bridge · hcp · fcc (`Table 1` · `Table 2`) — 자리 비교에서는 **Li 를 z 로만 이완** | 고대칭 자리라 z 만 이완은 대칭 구속과 거의 같다 |
| **덮임** | 1층 θ = 0.04 · 0.11 · 0.25 · 0.33 · 0.5 · 0.75 · 0.89 · 1 (`Fig. 8`) · 1ML Li (fcc hollow, 의사형 1×1) 위 둘째 층 같은 θ (`Fig. 9`) · 덮임 계산에서는 **Li 전 방향 이완** | **θ 당 배치 1 개** — 열거 · 앙상블 없음 · 다원자 배치 (예 θ 0.5 의 2 Li 자리) 미기재 |
| **흡착 에너지 정의** | **E_ads = E_nLi@surf − E_surf − n × E_Li** · E_Li = 고립 Li 원자 · 0 K 외삽 | 평균은 /n 으로 보임 (식에 없음) · 고립 원자 상자 크기 미기재 · **금속 Li 기준 (E_coh) 없음** |
| **확산 장벽** | **CI-NEB** · p(5×5) · **중간 상 5** (refs 52–55) | 스프링 · 수렴 기준 · 경로 끝점 정의 (그림으로만) 미기재 |
| **전자 구조** | PDOS (Li s · p · 기판 d) — `Fig. 7` | d-band 중심 수치 · 일함수 · Bader · 전하 밀도 차 **없음** |
| **무질서 처리** | 해당 없음 (단결정 + 흡착 원자) — **배치 선택은 단일 배치** | — |
| AIMD · MLIP · DFT+U | **없음** | — |

> **우리 틀과의 첫인상**: PBE + D3(BJ) · 평면파 · (111) 슬랩 · Γ 중심 k 라 **W_ad 트랙과 같은 계열**이다. 결정적으로 다른 것은 보고량 (고립 원자 기준 eV/Li vs 우리 W J/m²) 과 Li 모형 (원자 ~ 의사형 1ML vs Li 금속 슬랩) — §7b.

## 4b. 전기화학 · 형상 방법 ★ (핵생성 과전압 · 임피던스)

- **핵생성 과전압 — 안 쟀다.** 갈바노스태틱 석출의 전압 골 (η_nucleation) 이 없다. 이 논문의 "overpotential" 은 **Li RE 기준 정전위 −5 · −10 · −15 · −20 · −25 mV** 이고, 정전위 과도전류 · **석출 전하량도 싣지 않았다**.
- **SEI 형성**: CV 10 회 · 3.55 ↔ 0 V · 50 mV s⁻¹ (§4.2).
- **임피던스 (time-scan EIS)**: PalmSens4 · 교류 **1 mV** · **0.1 Hz – 100 kHz** · 전위당 **3600 s 동안 26 스펙트럼** (스펙트럼당 ≈ 138 s · `우리 산수`) · Kramers–Kronig 확인 · 회로 적합 · 파라미터 추출 = **EIS Spectrum Analyser** (ref 39 = 교신저자의 하이브리드 적합 알고리즘).
- **등가회로** (`Fig. S1`): **R_u – (C_SEI ‖ R_SEI) – (C_DL ‖ (R_CT – W))** · 이상 커패시터 (CPE 아님) · W 는 *"diffusion in both the electrolyte and the SEI layer, a distinction the physical model cannot make"* (SI).
- **k_app** = √(2D) · A_W/R_CT (식 1, 상세 유도는 ref 25) · D 고정 1×10⁻¹⁰ m² s⁻¹ · 자리 가중 평균 해석 (식 2).
- **석출 뒤**: 3.55 – 0 V CV 로 탈리 산화 피크 확인 → 그 산화 전위를 걸어 석출 Li 를 벗김 · 석출 뒤 단결정은 EMC 로 헹굼.
- **UPD 덮임**: θ = Q_exp/Q_ML · Q_ML = zFΓ_ML A · Γ_ML = N_atom/N_A (*"1 adsorbate atom occupies 1 surface atom"*) (SI p.S2).
- **AFM**: Bruker Multimode 8 · **tapping** · NCHV 탐침 (42 N m⁻¹) · 0.1 Hz 주사 · 높이 색 0–260 nm · 막대 1 µm (`figure-read ≈` 영상 폭 ≈ 5 µm) · 거칠기 · 입자 면적 = **Gwyddion** (ref 32).
- **미기재**: 단결정 **표면 전처리** (어닐 · 연마 · 세정) · **반복 실험 수** · 전위 순서와 **같은 결정 재사용 여부** · 석출 전하 · C_DL · R_SEI · R_u 값 · `Fig. S2` 가 26 개 중 어느 시점 스펙트럼인지 · AFM 통계의 표본 정의.

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나 · 실제로 본 것) | 우리 활용 |
|---|---|---|
| 1a | Cu(111) SEI 형성 CV 10 회 (x 0–3.6 V vs Li/Li⁺ · y −200…+50 µA · 범례 1st–10th). 1st 회 ≈ 2.2 V (−188 µA) · ≈ 0.45 V (−160 µA) 큰 환원, 2nd 회부터 ≈ 0.5 V 환원 / ≈ 0.82 V 산화 한 쌍만 남는다 (figure-read) | 실험 쪽 '친Li' 신호 = UPD 전위 (Cu ≈ 0.5 V). DFT 흡착 에너지와 같은 축에 올리려면 금속 Li 기준 환산이 필요 (§3e) |
| 1b | Ni(111) 같은 조건 (y −125…+75 µA). 1st 회 2.0 · 1.55 · 1.05 · 0.52 · 0.3 V 환원 · 1st 산화 ≈ 0.95 V (+78 µA). 안정 회차 = ≈ 0.25 V 뚜렷한 환원 + 약한 굴곡 · 산화 ≈ 0.5 · ≈ 1.6 V (figure-read) | Ni UPD 가 더 높은 전위 · 더 큰 전하. ⚠ 2.3 · 2.0 V 'UPD' 귀속은 논문 자신의 DFT 규모 (금속 Li 기준 ≲ 1.3 eV, 우리 산수) 와 안 맞는다 (§10-②) |
| 2a | Cu(111) k_app(t) · 5 전위 · 0–3600 s · y ×10⁻² cm/s "related to an average site" · 점선 = 눈대중 안내선 | k_app 절대값은 가정 D 에 매인다 — 이식 금지 · 시간 거동만 |
| 2b | Cu 평균 k_app (2000 s 뒤) vs 전위: 1.59 → 0.70 → 0.585 → 0.59 → 0.47 ×10⁻² cm/s (figure-read) · 오차 = 시간 산포 SD | −5 → −10 mV 에서 한 번에 2.3× 하락 |
| 2c | Ni(111) k_app(t) · y 축 라벨이 **"related to a single site"** (2a · 2b · 2d 와 다름) | 라벨 불일치 (§10-⑩) |
| 2d | Ni 평균: 0.403 → 0.323 → 0.207 → 0.168 → 0.154 ×10⁻² cm/s (figure-read) — Cu/Ni 2.2–3.9× | 논문의 핵심 실험 비교 |
| 3a–g | Cu(111) AFM: as-received (평평) · SEI 형성 · −5…−25 mV 석출 (높이 0–260 nm · 막대 1 µm). 전위가 커질수록 작은 입자 밀도 증가 · **−20 mV 에 대각선 선 결함을 따라 입자가 줄지어 있다** (figure-read · 본문 언급 없음) · −25 mV 에 ≈ 200 nm 높이 덩어리 몇 개 | 단결정 테라스에서도 **선 결함이 핵생성 자리를 먼저 차지**하는 직접 사례 — "단결정이라 결함 효과 배제" 는 완전하지 않다 |
| 4a–g | Ni(111) AFM 같은 조건. 입자 수가 적고, −20 mV 에 ≈ 200 nm 덩어리 하나 · −25 mV 에 가지 친 큰 덩어리 (주황 ≈ 200–230 nm) | "더 매끈" 은 평균 거칠기 기준이다 — 키 큰 덩어리는 Ni 에도 있다 |
| 5a | 입자 면적 vs 전위 · Cu 0.05 → 0.21 · Ni 0.03 → 0.31 µm² (figure-read) · 선형 추세선 둘 · **오차 막대 모든 전위에서 겹침** | 정성 추세만 · 석출량으로 정규화 안 됨 (§10-⑦) |
| 5b | 평균 거칠기 · Cu 26–38 · Ni 11–31 nm (figure-read) · 오차 겹침 · SEI 만일 때 이미 26 vs 19 nm (본문) | 차이의 상당 부분이 SEI 바탕 차 |
| 6a | Cu C_SEI(t) · 0.25–1.03 ×10⁻⁵ F · −5 mV 만 시간에 따라 상승 · 나머지 평탄 (figure-read) | — |
| 6b | Ni C_SEI(t) · 1.74 → ≈ 1.0 ×10⁻⁴ F 감쇠 (figure-read) → Cu 대비 10–40× (본문은 "two orders") | 막 두께로 읽으면 Ni ≈ 0.1 nm (ε_r 10 가정, 우리 산수) — 이 원소를 SEI 막으로 읽는 해석이 약하다 (§10-⑥) |
| 7a,b | Li 원자 흡착 PDOS (x −4…+4 eV − E_F · y ±2 states/eV 에서 잘림 · 위 = 스핀 ↑ · 아래 = ↓). Cu d 밴드 −4…−1.5 eV 로 E_F 아래에 떨어져 있고, Ni d 밴드는 E_F 를 걸치며 ↑/↓ 비대칭 (자성). **Li s · p 는 E_F 아래에서 거의 0** · Ni 에서 +3.05 eV 에 좁은 Li 상태 (↓) · Cu 에서 ≈ +2.9 eV 작은 Li p 혹 (figure-read) | d-band 위치 차이는 보인다. 그러나 Li 상태가 E_F 아래에 거의 없어 Li 는 전자를 내준 (이온성) 상태로 보인다 — d-band 반결합 채움 논증보다 일함수 · 전하이동이 자연스러운 서술자 (§10-⑪) |
| 8 | 1층 평균 흡착 에너지 막대 (θ 0.04–1 · 라벨 인쇄) · Cu −2.63 → −2.05 · Ni −2.89 → −2.19 eV · 모든 θ 에서 Ni 가 더 음수 | **흡착 에너지 지표의 덮임 의존 (0.58 / 0.70 eV) 이 재료 차 (0.12–0.28 eV) 보다 크다** — W_ad 보고서 §7 ① 한정 문구의 정량 근거 |
| 9 | 1ML Li 위 둘째 층 막대 · Cu −2.06 → −1.69 · Ni −2.01 → −1.57 eV · **모든 θ 에서 Cu ≥ Ni (순서 반전)** · 그림 속 첫 층 Li = 노랑, 둘째 층 = 초록 | 단일 원자 흡착 지표가 **층에 따라 순서를 뒤집는** 실례 — 어느 층 · 덮임에서 쟀는지 선언 없이 '친Li 순위' 를 내면 안 된다 |
| 10a | 맨 면 NEB (상 1–7 · y 0–0.03 eV): Cu 13 · Ni 11 meV · 그림 속 경로 = hollow → bridge → 이웃 hollow | < kT · 홉 대기 ≈ 0.2 ps (우리 산수) — 금속 (111) 위 장벽은 순서 지표가 못 된다 |
| 10b | 1ML Li 위 NEB: Cu 20 · Ni 12 meV · 끝점이 첫 층 Li (노랑) 꼭대기 · Ni 곡선 끝점 7 ≈ 0.5 meV (figure-read) | 차이 8 meV = 홉률 1.37× — k_app 2–4× 와 차수가 안 맞는다 |
| S1 | 등가회로 R_u – (C_SEI ‖ R_SEI) – (C_DL ‖ (R_CT – W)) | W 가 전해질 · SEI 확산을 못 가른다 (SI 자인) → k_app 는 D 가정에 매인다 |
| S2 | Nyquist (점 = 측정 · 점선 = 적합). Cu: Z′ ≤ 25 kΩ · 합쳐진 호 · 저주파 끝에서 적합이 벗어남 (−20 mV) · Ni: Z′ ≤ 12 kΩ · 반원 지름 ≈ 1.7 → 2.7 → 4.6 → 8.0 → 9.7 kΩ (−5 → −25 mV, figure-read) + **거의 수직인 저주파 꼬리** | R_CT 가 과전압과 함께 **커진다** (Butler–Volmer 와 반대) · Ni 꼬리는 45° Warburg 보다 축전 성격 → 두 금속의 W 가 같은 물리인지 불확실 (§10-⑧) |
| Table 1 | 맨 (111) 면 단일 Li 원자 4 자리 (top · bridge · hcp · fcc) · Cu −2.51 / −2.62 / −2.63 / −2.63 · Ni −2.79 / −2.88 / −2.89 / −2.89 eV | 배위 1 · 2 · 3 · 3 · 정상 테라스 · 고립 원자 기준 — **대조 잡 표적** (우리 Ag(111) 계산 때 Cu(111) fcc 한 점) |
| Table 2 | 1ML Li 위 단일 Li 원자 · Cu −2.06 / −2.04 / −2.03 / −2.04 · Ni −2.03 / −2.01 / −2.01 / −2.01 eV | 자리 차 20–30 meV = 이 논문 수치 잡음 크기 (`Table 2` ↔ `Fig. 9` Ni 0.02 eV 역전) |

---

## 5b. 그림별 상세 — 보고 나서 확인한 것

1. **`Fig. 1`** — 두 패널 모두 10 회가 거의 겹친다 (1st 회만 크게 다름). Cu 는 2nd 회의 0.5 V 환원이 −58 µA 로 3rd 회 이후 (−38…−42 µA) 보다 깊다 — 본문 *"After the 2nd cycle, a stable SEI is formed"* 와 맞다. Ni 는 2nd 회부터 이미 겹친다 (*"stable SEI is formed after the first cycle"*). 0 V 꼭짓점 전류는 Cu ≈ −20 µA · Ni ≈ −30 µA 로, 0 V 까지만 훑어 bulk 석출 피크는 없다. Ni 의 2.3 V 'UPD' 굴곡은 이 그림 해상도에서 2.0 V 굴곡과 따로 분간하기 어렵다.
2. **`Fig. 2`** — 네 패널 모두 y 가 ×10⁻² cm/s 로 같은 단위인데 범위가 다르다 (Cu 0.4–2.0 · Ni 0.1–1.2). 2b · 2d 의 y 라벨은 "P[k_app cm/s (related to an average site)]" — "P[…]" 의 뜻은 캡션에 없다. 2a 의 −5 mV 300 s 한 점 (≈ 2.0) 은 추세선 위로 튄 점이다.
3. **`Fig. 3` · `Fig. 4`** — 두 그림 모두 같은 색 축 (0–260 nm) 이라 직접 비교된다. Cu 는 −15 mV 부터 **작은 입자가 화면 전체에 깔리고**, Ni 는 같은 전위에서 **듬성듬성**하다 — "Ni 쪽 핵 수가 적다" 는 영상으로 보인다. 다만 이 차이는 면적 · 거칠기 통계 (`Fig. 5`) 보다 영상에서 더 분명하고, 통계는 오차가 크다. 석출물이 Li 인지 (SEI 입자인지) 를 화학적으로 확인하는 측정 (XPS · EDS) 은 없다.
4. **`Fig. 5`** — 추세선은 Ni 가 기울기가 크다 (면적) · Cu 가 위에 있다 (거칠기). 점 하나하나는 오차 막대 안에서 구분되지 않는다.
5. **`Fig. 6`** — 두 패널의 y 단위가 **한 자릿수 다르다** (1e−5 vs 1e−4). 같은 축에 올리면 Ni 최저 (≈ 0.9×10⁻⁴) 와 Cu 최고 (≈ 1.03×10⁻⁵) 사이가 ≈ 9×, Ni 최고와 Cu 최저 사이가 ≈ 70× 다. "두 자릿수" 는 최대 – 최소 쌍에서만 가깝다.
6. **`Fig. 7`** — Cu 패널도 ↑/↓ 가 대칭으로 그려져 있다 (Cu 계는 비스핀이라 같은 곡선을 거울로 그린 것으로 보인다). d-band 중심 숫자는 없다.
7. **`Fig. 8`** · **`Fig. 9`** — 막대 끝에 숫자가 인쇄되어 있다 (위 표 = 그 숫자). 삽입 그림은 θ 0.04 (원자 1 개) · 중간 · θ 1 (전면) 의 개념도이고, θ 별 실제 배치를 보여주지 않는다.
8. **`Fig. 10`** — 곡선은 상 1 ↔ 7 대칭 · 최고점 = 상 4. 삽입 그림은 경로 겹쳐 그리기 (끝점 진초록 · 중간 연초록).
9. **`Fig. S2`** — Cu 는 −5 · −10 mV 에서 −Z″ ≈ 5 kΩ 수준 호가 Z′ 15 kΩ 까지 이어지고, −15 mV 이상은 ≈ 10 kΩ · Ni 는 반원 + 저주파 수직 상승이 깔끔하게 갈린다. 적합선은 Ni 에서 잘 맞고 Cu 는 저주파 끝에서 벗어난다.

---

## 6. Post-processing ★

- **무엇**: ① EIS 등가회로 적합 → A_W · R_CT → k_app (식 1) · C_SEI ② CV 피크 전하 적분 → UPD θ ③ AFM 높이 영상 → 거칠기 · 입자 면적 ④ DFT 흡착 에너지 (자리 · 덮임 · 층) ⑤ CI-NEB 장벽 ⑥ PDOS (Li s · p, 기판 d).
- **도구**: EIS Spectrum Analyser (K-K 확인 포함) · Gwyddion · VASP. PDOS 투영 · NEB 후처리 도구 (VTST · pymatgen 등) 는 미기재.
- **수치화 · 기록**: 흡착 에너지 = 막대 라벨 소수 2 자리 (eV) · 장벽 = 그림 라벨 meV 정수 · k_app · C_SEI · AFM = 점 그림 (표 없음 · 원자료 비공개) · 오차 = 시간 산포 SD (k_app) · 미정의 SD (AFM).
- **우리가 다시 낼 수 있는 것**: 표 둘과 막대 라벨은 그대로 전사 가능 (위 §3e–§3h). 나머지는 figure-read 뿐이다.

---

## 7. 우리 대비

### 7a. argyrodite 기준선 (comp1 / modelc · `our_dft_baseline.md`) — 겹치는 물성 없음

| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| 이온전도 · Ea | n/a (액체 전해질 · Li⁺ D 는 문헌 고정값) | MLIP-MD | 비교 대상 없음 |
| 산화 안정 (ESW) | n/a | grand-potential | 없음 |
| 기계 | n/a | C_ij · EOS | 없음 |
| 전자구조 | 금속 표면 PDOS 만 | SE 띠틈 | 없음 |

⇒ **물성 4축 (A–D) 어느 행에도 수치로 넣지 않는다.** 이 논문은 W_ad 트랙 (§7 Li 친화성) 의 **방법 원전 · 금속 (111) 기준점**이다.

### 7b. W_ad 트랙 — 보고서 §7 "Li 친화성 정량화" 와 같은 점 / 다른 점

> 우리 쪽 정본 = `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §7 · 부록 A (우리 W 값은 여기 싣지 않는다 — 위치만).

| 항목 | 이 논문 | 우리 (W_ad 트랙) | 같음 / 다름 · 이유 |
|---|---|---|---|
| 범함수 | PBE | PBE | **같음** |
| 분산 | D3(BJ) · 흡착 · NEB 전부 · 3 체 미기재 | D3(BJ) 2 체 헤드라인 · ATM 3 체는 민감도 열 | **거의 같음** — 3 체 처리를 모르니 0.0x eV 단위 비교는 보류 |
| 코드 · 의사퍼텐셜 | VASP · PAW | 평면파 (QE 경로) | 다름 — 같은 계를 돌려 차이를 재야 함 (대조 잡 · §8-③) |
| 금속 모형 | (111) 5 층 · 아래 2 층 고정 · 진공 15 Å | Ag(111) 3 층 (3 → 4 층 점검) · 분리 끝점 10 Å | 비슷 — 둘 다 (111) 테라스 |
| k | Γ 13 / 9 / 5 for p(2×2) / p(3×3) / p(5×5) | 2×2 정합 셀 9×9×1 (12×12×1 점검) | 비슷한 밀도 |
| 스핀 | Ni 만 스핀 분극 | Ag · C 비자성 | n/a |
| **보고량** | **E_ads (eV / Li) · 고립 Li 원자 기준** | **W_sep (J/m²) · 고정 기하 분리 에너지** | **다른 양** — 단위 · 기준 · 정의가 다 다르다 |
| **Li 모형** | 원자 1 개 → **의사형 1×1 단층** (기판 격자에 맞춰 15.6 / 18.1 % 압축) · θ 당 배치 1 | §7 ② 제안 = **Li 금속 슬랩** (Li(100) · Li(110)) · 정합 셀 · 변형 · registry 선언 | **다름** — 의사형 1ML 은 Li 금속이 아니다 |
| 금속 Li 기준 | **없음** | §7 ② 제안 = 같은 방법 · 같은 Li 면의 γ_Li | 이 논문 값을 젖음으로 옮길 다리가 없다 |
| 젖음각 | 없음 | §7 ② Young–Dupré (제안) | — |
| 합금 | 없음 (Cu · Ni 비합금) | §7 ③ (Ag–Li) 제안 | — |
| 실험 대조 | UPD 덮임 · k_app · AFM | §7 "실험 (증착 과전압 · 접촉각) 과 함께" | UPD 전하가 하나 더 쓸 수 있는 실험 손잡이 — 단 귀속 조심 (§10-①②) |

### 7c. 진짜 차이 vs 방법 인공물 (논문 안의 Cu–Ni 비교)

| 비교 | 크기 | 판정 |
|---|---|---|
| 1층 단일 원자 흡착 Ni − Cu | −0.26…−0.28 eV (모든 자리) | **부호는 그럴듯하다** (Ni 는 E_F 근처 d 상태 · 더 큰 일함수 — 후자는 논문 밖 일반 지식). 크기는 Cu 비스핀 / Ni 스핀 + 고립 원자 기준의 스핀 처리 미기재라 **수십 meV 단위로는 확정 못 함** |
| 1층 덮임 따라 Ni − Cu | −0.27 → −0.12 eV | θ ≥ 0.75 는 금속 Li 보다 빽빽한 의사형 층 — **모형 상태** |
| 둘째 층 Cu − Ni | 0…0.12 eV (Cu 가 셈) | **의사형 변형 차이 (Ni 가 더 압축) 가 주 원인일 수 있다** — 저자도 격자 부정합으로 설명. 실험 UPD 는 Cu 에서 ⅓ ML 이라 Cu 쪽 1ML 기판 자체가 가정이다 |
| NEB 장벽 차 | 2 meV (맨면) · 8 meV (1ML 위) | **방법 잡음 크기** (힘 0.01 eV/Å · 중간 상 5 · 표–그림 0.02 eV 역전) — 차이로 쓰지 않는다 |
| k_app Cu/Ni | 2.2–3.9× | 실험값이지만 D 가정 · W 해석 · 반복 없음 · 전위 순서 미기재 — **방향은 일관되나 기전 귀속은 미확정** |
| C_SEI Ni/Cu | 10–40× | 실험값 · **"두 자릿수" 아님** · 막 두께 해석은 Ni 에서 0.1 nm 라 성립 어려움 |

---

## 8. 적용 인사이트 (W_ad 보고서 §7 · 우리 계산에)

1. **§7 ① 한정 문구에 숫자를 댄다.** 보고서는 *"원자 하나라서 '젖음' 을 직접 말하지는 않고, 자리와 덮임 정도에 따라 값이 바뀐다"* 고 적었다. 이 논문이 그 크기를 준다: **덮임 0.04 → 1 에서 흡착 에너지가 0.58 / 0.70 eV 움직이고, 이것이 Cu–Ni 차 (0.12–0.28 eV) 보다 크며, 둘째 층에서는 순서가 뒤집힌다** (`Fig. 8` · `Fig. 9`). ⇒ 우리가 ① 을 낼 때는 **자리 · 덮임 · 층을 선언한 X(상태)** 로만 낸다 (보고량 카드 규율 — admissible state 가 여럿이면 선택 규칙이 먼저).
2. **금속 Li 기준 열을 같이 낸다.** 고립 원자 기준 값만으로는 "Li 가 자기 자신보다 기판에 붙나" 를 판정 못 한다. 같은 계산 틀에서 bcc Li 벌크 1 원자 에너지를 같이 내서 **vs Li metal 열**을 싣는다. 이 열은 곧 **UPD 전위 어림 (U ≈ −ΔE/e)** 과 같은 축이라 실험 (UPD · 핵생성 과전압) 과 바로 맞댈 수 있고, §7 ② 의 γ_Li 와도 같은 기준이다.
3. **대조 잡 하나**: 우리 Ag(111) 위 Li 흡착을 계산할 때 **같은 설정으로 Cu(111) fcc hollow 단일 원자 한 점**을 같이 돌려 이 논문 −2.63 eV (VASP PAW · PBE+D3(BJ) · 고립 원자 기준 · p(5×5)) 와 견준다. 허용 차이는 **결과 보기 전에** 정한다 (의사퍼텐셜 · 3 체 항 · 고립 원자 처리 차이를 감안해서).
4. **확산 장벽을 네 번째 지표로 넣지 않는다 — 적어도 금속 (111) 위에서는.** 11–20 meV 는 kT 아래 · 홉 대기 ≈ 0.2 ps 라 재료를 가르지 못한다. 넣으려면 홉 수 검산 한 줄을 같이 싣는다 (CLAUDE.md 규칙).
5. **§7 ② (Li 슬랩 정합 셀) 를 짤 때 변형 선언이 핵심이다.** 의사형 1×1 Li 는 Cu · Ni 에서 15.6 / 18.1 % 압축 · Li(110) 면보다 1.5–1.6× 빽빽하다 (우리 산수). Ag(111) (a ≈ 4.09 Å, 교과서 · 논문 밖) 는 1×1 Li 의 압축이 더 작을 것이므로, Cu/Ni 의 '1ML' 결과를 Ag 로 옮겨 생각하면 안 된다 — 정합 셀의 변형률 · 면밀도를 표에 같이 적는다.
6. **UPD 전하를 덮임으로 바꾸는 산수는 Γ 를 기하에서 다시 계산한다** (§10-①). 실험 동료가 같은 방식으로 Ag 위 UPD 를 세면 같은 함정이 생긴다.
7. **'친Li' 와 '좋은 집전체' 를 같은 말로 쓰지 않는다.** 이 논문은 더 친Li 인 Ni 에서 k_app 가 더 낮고 성장이 더 수평이라고 엮는다 — 단일 지표 (흡착 세기) 가 성장 모드를 정한다는 연결은 이 논문 안에서도 증명되지 않았다 (§10-⑤).

---

## 9. 인용 가능 문장 (덱 · 원고용 · 랩 출처 표기)

- "On pristine Cu(111) and Ni(111), PBE+D3(BJ) adsorption energies of a single Li adatom referenced to the isolated Li atom are −2.63 and −2.89 eV at the hollow sites (*J. Mater. Chem. A*, 14, 16784 (2026))."
- "In the same work, the average Li adsorption energy weakens by 0.58 eV (Cu) and 0.70 eV (Ni) from θ = 0.04 to θ = 1, which exceeds the Cu–Ni difference, and the order reverses for the second Li layer." *(0.58 / 0.70 은 그 논문 `Fig. 8` 막대 값의 차 — 우리 산수라고 각주)*
- "Lithiophilicity in that study is ranked by adsorption energy alone; adhesion and wetting are not evaluated."
- "Calculated Li surface-diffusion barriers on Cu(111) and Ni(111) (11–20 meV) lie below *k*_B*T* at room temperature, as the authors note."
- ⛔ 쓰지 않을 문장: "Ni(111) is more lithiophilic and therefore wets Li better" (젖음 미계산) · "SEI on Ni is two orders of magnitude thinner" (그림은 10–40× · 두께 해석 불성립) · "Ni(111) supports a full Li monolayer by UPD" (Γ 산술 문제 · 귀속 불확실).

---

## 10. 주의 / 한계 (over-claim 방지)

1. **🔴 SI 의 표면 원자 밀도가 (111) 기하와 안 맞는다.** fcc(111) 면밀도 = 4/(√3 a²) → 논문 자신의 DFT 격자 (3.63 / 3.52 Å) 로 **1.75 / 1.86 ×10¹⁵ cm⁻²** 인데 SI 는 **1.39 / 1.48 ×10¹⁵** 를 쓴다 (≈ 21 % 작음 · `우리 산수` · 실험 격자로도 1.77 / 1.86). 1.39 / 1.48 값 자체의 출처는 적혀 있지 않고, 그 식에 달린 각주 i 는 **인공광합성 분자 촉매 리뷰 (Langmuir 2024)** 다. 두 값의 비 (1.065) 는 (a_Cu/a_Ni)² (1.064) 와 맞는다 (`우리 산수`) — 그래서 **Ni/Cu 덮임 비 (≈ 3×) 는 이 오차에 안 흔들리고, 절대 θ 만 흔들린다**. 기하 밀도로 다시 세면 **θ ≈ 0.27 (Cu) · ≈ 0.77 (Ni)** — "⅓ vs full monolayer" 의 대비 (≈ 3×) 는 남지만 **"Ni 에서 완전 단층"** 은 성립하지 않는다. DFT 가 θ = 1 을 가정한 근거 (*"in good agreement with the experimental results for Ni"*) 가 약해진다.
2. **🔴 Ni 'UPD' 귀속.** ① 안정 회차 UPD 를 2.3 · 2.0 V 부터 센다 (p.16785) — 그런데 논문 자신의 DFT 를 금속 Li 기준으로 바꾸면 (교과서 E_coh 1.63 eV · `우리 산수`) 흡착 세기는 θ → 0 에서 Ni ≈ 1.26 eV · Cu ≈ 1.00 eV, θ = 1 에서 0.56 / 0.42 eV 다 → **UPD 는 ≲ 1.3 V 규모**여야 하고 2.3 · 2.0 V 는 그 밖이다. ② 단결정 **표면 전처리가 기술되어 있지 않다** — Cu 쪽에서 스스로 1.5–2.5 V 를 Cu 산화물 환원 · 리튬화로 귀속하면서 Ni 쪽 같은 영역은 UPD 로 센다 (자연 NiO 가능성 미논의). ③ 같은 논문 안에서 **"first UPD peak at ca. 1.0 V"** (DFT 절) 와 **"starting with weak peaks at 2.3 … V"** (2.1 절) 가 어긋난다. ④ 적분 구간 미기재. ⑤ Ni 300 µC = Li 면밀도 1.44×10¹⁵ cm⁻² = **Li 자신의 조밀면 1.15–1.25 층** (`우리 산수`) — 전부 Li UPD 라면 단층 흡착을 넘는다. ⇒ Ni 의 300 µC 에는 비-UPD (SEI · 산화물) 전하가 섞였을 가능성이 크다.
3. **친Li = 고립 원자 기준 흡착 에너지 하나.** 금속 Li 기준 · 점착 · 젖음 · 핵생성 에너지가 없다. 0.12–0.28 eV 차이가 "젖음이 좋다 · 성장이 균일하다" 로 가는 다리는 이 논문에 없다.
4. **의사형 1ML 모형.** Li–Li 2.57 / 2.49 Å (bcc Li 3.04 Å 대비 −15.6 / −18.1 % · `우리 산수`) · Li(110) 면보다 1.53 / 1.62× 빽빽 → θ ≥ 0.75 와 둘째 층 전체가 **Li 가 실제로 취하지 않을 압축 상태** 위에서 계산됐다. 둘째 층은 첫 층 꼭대기 (top) 에 쌓아 **AA 적층**이고, 그 top 선호는 20–30 meV 로 수치 잡음 크기다. θ 당 배치 1 개 (열거 없음).
5. **장벽 → k_app 인과는 차수에서 안 맞는다.** 장벽 전부 < kT (홉 대기 0.15–0.22 ps) · Cu–Ni 차 8 meV = 홉률 1.37× · k_app 차는 2.2–3.9× 이고 10²–10³ s 척도다. EIS 의 k_app (R_CT · A_W) 는 표면 확산을 재는 양이 아니다. 저자도 *"slow surface diffusion processes may not be the predominant source"* 라고 인정한다. "nearly double" = 실제 1.67×.
6. **C_SEI 해석.** "two orders of magnitude" ↔ figure-read 10–40×. Ni ≈ 77 µF cm⁻² 은 평판 막으로 ≈ 0.1 nm (ε_r 10 가정 · `우리 산수`) 라 막 두께 신호로 읽을 수 없다 — 이 원소가 다른 과정 (흡착 의사용량 · 이중층) 을 잡았을 가능성. SEI 뒤 AFM 거칠기 (26 vs 19 nm) 를 두께의 근거로 쓰는 것은 **거칠기 ≠ 두께**. 초록의 *"we show that Ni(111) exhibits higher corrosion resistance"* 는 직접 측정 (부식 전류 · XPS · 질량) 없이 C_SEI 와 문헌으로 추론한 것이다.
7. **AFM 통계.** 면적 · 거칠기 오차 막대가 모든 전위에서 겹친다 · 표본 정의 없음 · **석출 전하량을 안 실어서** 같은 전위에서도 Cu (k_app 가 큼) 와 Ni 의 석출량이 같은지 모른다 → 입자 크기를 석출량으로 정규화하지 못했다. 거칠기 차는 SEI 바탕 차 (≈ 7 nm) 와 같은 크기. 석출물의 화학 확인 (Li 인지) 없음.
8. **k_app 방법.** D 를 문헌값 하나로 고정 (√D 로 절대값이 움직인다) · W 가 전해질 · SEI 확산을 못 가른다 (SI 자인) · Ni 의 저주파 꼬리는 거의 수직 (축전형) 이고 Cu 는 호에 가깝다 → **같은 W 원소가 두 금속에서 같은 물리인지 불확실**하고, 그러면 Cu/Ni 비도 순수 속도 차이가 아닐 수 있다 · R_CT 가 과전압과 함께 **커진다** (단순 Butler–Volmer 와 반대 — 논문은 느린 자리 기여로 설명) · 오차 = 한 번의 런 안 시간 산포.
9. **반복 · 순서 미기재.** 결정당 1 개 · 반복 수 · 전위 순서 · 같은 결정 재사용 여부가 없다. Cu −5 mV 는 k_app (다음 전위의 2.3×) · C_SEI (상승 거동) 둘 다 튀는데, 첫 런 효과인지 가를 수 없다.
10. **`Fig. 2c` y 축 라벨** "related to a single site" — 다른 세 패널은 "average site". 오기로 보이나 확인 불가.
11. **PDOS · d-band 논증은 정성적.** d-band 중심 · 일함수 · Bader · 전하 밀도 차가 없다. 그림에서 Li s · p 상태가 E_F 아래에 거의 없다 → Li 는 이온성으로 붙는 것으로 보이고, 그러면 반결합 채움 (d-band 모형, 공유 결합용) 보다 **일함수 · 전하이동**이 자연스러운 설명이다.
12. **잔실수.** 흡착 에너지 식에 1/n 이 없다 (그림은 평균) · ref 22 와 ref 50 이 **같은 논문** (Pande & Viswanathan 2019) · *"Ni … the lowest cost (in 2025)"* 의 근거가 2023 박막 논문 하나 — 금속 시세로는 Ni 가 Cu 보다 비싸다 (논문 밖 상식 · 확인 필요).
13. **스핀 · 쌍극자 · 고립 원자.** Ni 만 스핀 분극 · 고립 Li 원자 (홀전자 1) 의 스핀 처리와 상자 크기 미기재 — 두 금속에 같은 E_Li 를 썼는지 모른다 (같지 않으면 Cu–Ni 차에 계통 오차). 한쪽 면 흡착 비대칭 슬랩인데 쌍극자 보정 언급 없음.
14. **다결정 박으로의 이전**은 미검증 (결론 자인 — 입계 · 자연 산화막).

---

## 11. 기법 미니 용어집

| 용어 | 뜻 (이 논문 문맥) |
|---|---|
| **UPD (underpotential deposition)** | Li⁺/Li 평형 전위보다 **양의 전위**에서 Li 가 기판 위에 한 층 (이하) 흡착되는 것. 기판–Li 결합이 Li–Li (금속) 결합보다 세야 일어난다 → U_UPD ≈ −ΔE_ads(vs Li 금속)/e (용매화 · 엔트로피 무시) |
| **θ (덮임)** | DFT: Li 수 / 기판 표면 원자 수 (θ = 1 = 1×1 의사형) · 실험: Q_exp / Q_ML |
| **k_app (겉보기 속도계수)** | √(2D) · A_W/R_CT — Randles 회로에서 Warburg 계수와 전하이동 저항의 비로 낸 표준 속도상수 꼴 (농도가 약분됨). 여러 자리 속도의 가중 평균 (식 2) |
| **A_W (Warburg 계수)** | 확산 임피던스 Z_W = A_W (1 − j)/√ω 의 크기 계수 (Ω s⁻½) |
| **time-scan EIS** | 정전위를 건 채 일정 간격으로 스펙트럼을 연속 측정해 파라미터의 시간 변화를 보는 방식 (비정상 상태라 K-K 확인이 필요) |
| **C_SEI** | 등가회로의 SEI 커패시턴스 — 평판 막이면 ε_r ε₀ A / d 라 두께에 반비례 |
| **CI-NEB** | 끝점 사이 상 (image) 을 스프링으로 잇고, 최고점 상을 안장점으로 올려 보내 장벽을 찾는 방법 |
| **d-band 모형 (Hammer–Nørskov)** | 전이금속 d 밴드 중심이 E_F 에 가까울수록 흡착종–금속 반결합 상태가 덜 채워져 결합이 세다는 서술자 — 공유성 흡착 (O · H · CO …) 에서 잘 맞는다 |
| **D3(BJ)** | Grimme 분산 보정 + Becke–Johnson 감쇠 — 2 체 항 (기본) · 3 체 ATM 은 선택 |
| **의사형 (pseudomorphic) 단층** | 흡착층이 기판 격자를 그대로 따르는 1×1 층 — 흡착종 자신의 격자와 다르면 변형된 상태 |
| **흡착 에너지 vs 핵생성 에너지 vs 점착 → 젖음** | 각각 원자 1 개의 결합 (기준 = 고립 원자 또는 금속 Li) · 금속 Li 대비 첫 핵의 자유에너지 · Li 금속 덩어리와 기판의 계면 분리 일 (W) 을 2γ_Li 와 견준 값 (Young–Dupré cos θ = W/γ_Li − 1) — **이 논문은 첫째 (고립 원자 기준) 만** |
| **홉 수 검산** | Γ = ν₀ exp(−Ea/kT) (ν₀ 10¹³ s⁻¹ 가정) · 평균 대기 1/Γ — 장벽과 "빠르다 · 느리다" 서술의 차수 모순을 거른다 (확산계수 아님) |

---

## 12. 참고문헌 중 우리 축 후보 (다음에 먹일 것 · 서지는 이 PDF 참고문헌 목록 그대로)

| ref | 서지 | 왜 | litdb |
|---|---|---|---|
| 25 | K. Cicvarić *et al.*, *J. Phys. Chem. C* 130(2), 1096–1104 (2026), DOI 10.1021/acs.jpcc.5c07557 — Li nucleation on single crystal copper | 이 논문 k_app 유도 · Cu(111) 덮임 계산의 원전 | 없음 |
| 16 | M. H. Kim *et al.*, *Energy Environ. Sci.* 17(18), 6521–6532 (2024), DOI 10.1039/d4ee01766h — horizontal Li growth on single crystal Cu(111) foil | Cu(111) 장벽 대조 · 실제 박 (foil) 단결정 | 없음 |
| 37 | D. Petersen *et al.*, *Mater. Horiz.* 11(23), 5914–5945 (2024), DOI 10.1039/D4MH00529E — anode-free post-Li metal batteries | 이 논문이 '친Li → 균일 핵생성' 의 근거로 인용 | 없음 |
| 8 | Y. Zhang *et al.*, *ChemElectroChem* 11(4), e202300739 (2024), DOI 10.1002/celc.202300739 — current collectors, conventional → all-solid-state | 전고체 집전체 쪽 | 없음 |
| 6 | S. Huo *et al.*, *Adv. Mater.* 36(47), 2411757 (2024), DOI 10.1002/adma.202411757 — anode-free LMB feasibility | 무음극 전반 | 없음 |
| 22 (= 50) | V. Pande, V. Viswanathan, *ACS Energy Lett.* 4(12), 2952–2959 (2019), DOI 10.1021/acsenergylett.9b02306 — computational screening of current collectors | 흡착 · 핵생성 에너지 · BEP 장벽 스크리닝 — §7 ① 과 '핵생성 에너지' 를 가르는 원전 | 없음 |
| 17 | G. Li *et al.*, *J. Phys. Chem. C* 127(33), 16297–16303 (2023), DOI 10.1021/acs.jpcc.3c03096 — crystal facet selectivity of Cu current collector | 면 의존 DFT | 없음 |
| 36 | K. Yan *et al.*, *Nat. Energy* 1, 16010 (2016), DOI 10.1038/nenergy.2016.10 — selective deposition via heterogeneous seeded growth | 핵생성 과전압 · 합금 씨앗 — §7 ③ 쪽 | 없음 |
| 38 | M. Jäckle *et al.*, *Energy Environ. Sci.* 11(12), 3400–3407 (2018), DOI 10.1039/C8EE01448E — self-diffusion barriers as dendrite descriptors | 장벽 서술자 원전 | 없음 |

> **같은 배치 (2026-11-24 · `litdb/_curation/batch_2026_11_24/batch.json`) 에서 이 편과 이어 읽을 것** — 이 논문에 없는 §7 ② · ③ 쪽이다 (링크는 그 digest 들이 정본에 들어간 뒤 확인):
> `seymour2021_void_suppression_interfacial_adhesion_vacancy_transport` (점착 W_adh 와 2γ_metal 비교 — §7 ②) · `yang2021_flat_li_stripping_lithiophilic_interface_design` (친Li 계면 설계 — 점착 기준) · `lu2026_li_ag_interface_thermodynamics_kinetics` (Li–Ag — §7 ③) · `fuchs2023_cu_llzo_anode_free_li_growth_modes` (Cu 집전체 | 고체 전해질 위 Li 성장 모드 — 이 논문의 액체 전해질 Cu 와 대조).

---

## 🔗 이어 읽기 · 바로잡기 (2026-11-24b 묶음)

> 같은 날 둘째 묶음 12 편 (`litdb/_curation/batch_2026_11_24b/batch.json`) 의 끝 보고에서 이 카드에 걸리는 것만 모았다 (2026-11-24). 위 본문은 고치지 않았다 — 겹치면 이 절이 우선한다.

- Cu 막 실험 쪽: 얇은 Cu 막 아래 Li 기둥이 Cu 를 들어 올린다 (가넷 · operando SEM · 첫 CE ≈20 %) → `ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism` · 금속 층 친Li 성 화산형에서 Cu 가 가장 낮다 (CCD 0.26 mA cm⁻² · 가넷) → `chu2026_solubility_guided_interlayer_li_plating_stripping_garnet`.
