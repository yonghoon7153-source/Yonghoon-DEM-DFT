<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 기준 = zuo2022_chlorination_cathode_interface.md
     2026-11-24 litdb-curator (병렬 세션 — INDEX · comparison · pdf_map 같은 공유 파일은 메인 세션이 합친다).
     그림: 크롭 31 장 = 도구 27 (Fig. 1–17 · Fig. S1–S10) + 손 4 (tab_1 · tab_2 · tab_S1 · fig_A1 — figures.json `manual_crop`).
     크롭으로 직접 본 것 11 장 (§0 끝 목록). 나머지는 PDF 쪽 렌더 (저해상도) 로만 봤다.
     코드: 공개 저장소 souravmat-git/MOOSE-BatModelling 커밋 3e44674 (얕은 클론 · 읽기 전용) 의 입력 9 개 · 소스 4 개를 줄 단위로 대조 (§5).
     ⚠ "우리 계산" · "우리 추론" = 논문이 보고하지 않은 것을 이 digest 가 Table 1 · 코드 값에서 유도한 것. -->

# A Diffuse-Interface Model for Predicting the Evolution of Metallic Negative Electrodes and Interfacial Voids in Solid-State Batteries with Homogeneous and Polycrystalline Solid Electrolyte Separators — Chatterjee, Tonks, Gardner & Sessim (*J. Electrochem. Soc.* **2025**, 172, 070522)

> slug `chatterjee2025_diffuse_interface_li_anode_void_model` · DOI `10.1149/1945-7111/aded38` · type `phase-field · continuum FEM (MOOSE) · electrochemical multiphysics — 계산 전용 (실험 0 · 원자단위 계산 0)` · PDF `litdb/inbox/difint2025_void_diffuse_interface_main.pdf` (25 쪽 · 1 쪽은 표지 광고 · Fig. 1–17 · Fig. A·1 · Table I–II) + `litdb/inbox/difint2025_void_diffuse_interface_SI.pdf` (SI 17 쪽 · Fig. S1–S10 · Table S.1) · 코드 `github.com/souravmat-git/MOOSE-BatModelling` @ `3e44674` · digested `2026-11-24` · status ✅ · 태그 **[외부]**
> elements: Na
> methods: — (phase-field · FEM · MOOSE 는 용어집 목록 밖)

> **저자**: **Sourav Chatterjee**\* ¹˒² · **Michael Tonks**\* ¹ · William Gardner\* ³ · Marina Sessim\* ³ — ¹ Dept. of Materials Science and Engineering, University of Florida (Gainesville) · ² Materials Science Division, Lawrence Livermore National Laboratory · ³ QuantumScape Battery, Inc. (San Jose) · \* 이메일 표기 4 명 모두 (자료 요청 창구는 SC · MT) · 투고 2024-12-22 · 수정 2025-05-23 · 게재 2025-07-23 · 지원 = **QuantumScape 하청 연구비** + LLNL 계약 DE-AC52-07NA27344 (Chatterjee) · 이해상충 없음 선언
>
> **사전 공개판**: arXiv 2412.17147 (메인 세션이 준 정보 — 이 PDF 에는 표기 없음). 이 digest 는 JES 출판본 기준이다. SI 의 절 참조 (*"Section 4.1.1"* · *"Section 2.3"* 등) 는 번호 없는 JES 판과 안 맞는 옛 번호가 남은 것이다.
>
> **코드**: 공개 저장소 `souravmat-git/MOOSE-BatModelling` (README · `src/` · `include/` · 예제 입력 `single_void/` · `multiple_voids/` · `perfect/`). 이 digest 는 커밋 **`3e44674`** (2025-05-14, *"Update Na_stripping_void_lowGB_CC.i"* · 얕은 클론이라 이력은 이 한 커밋뿐) 을 읽었다. 로컬 읽기 전용 사본 `/home/user/souravmat-git/moose-batmodelling` (litdb 밖 · 복사 안 함). 아래 `파일:줄` 은 그 사본 기준이다.
>
> ⚠ **slug 의 `li_anode` 는 이름일 뿐이다** — 논문이 실제로 푼 계는 **Na 금속 | Na-β″-alumina (NBA)** 이고 Li 는 한 번도 계산하지 않았다 (결론의 *"equally applicable for simulating electrode and/or void evolution … in Li-metal SSBs"* 는 주장뿐). slug 는 메인 세션이 정한 고정값이라 그대로 둔다.
>
> **계보**: Plapp 2011 (grand-potential 상장 원리, ref 48) · Aagesen 2018 (다상 · 다성분 grand-potential, ref 50) · Moelans 2011 (다상 보간 h · α · m 공식, ref 53) → Bhave … Tonks 2023 *J. Nucl. Mater.* (용융염 부식 전기화학 상장, ref 51 — 이 틀의 직계) → **본 논문** (Na 전고체 셀 박리 · 도금 + 계면 공극 + 다결정 SE). 공극 상장의 직전 선례 = Zhao, Wang & Martínez-Pañeda 2022 *JMPS* (ref 36 · Li/LLZO · 전극 두께 고정) · 날카로운 계면 = Agier … Fleck 2022 *Acta Mater.* (ref 35) · 표면 확산 = Barai … Srinivasan 2024 *Chem. Mater.* (ref 37).

---

## 0. 이 digest 를 읽는 법 — 우리 축 (DEM-DFT · 계면 점착 W)

우리가 이 논문에서 알고 싶은 것은 하나다 — *"공극 모델은 계면 에너지 · 점착을 **어디에 어떤 꼴로** 받고, 그 값이 결과를 얼마나 바꾸나."* (W_ad 보고서 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §7 의 *"Li 증착 · 공극 모델에 Li–벽 접촉각 같은 입력이 있으면 …"* 의 실제 사례 점검.)

> 🔑 **답 (§4g · §5d).**
> ① 이 모델에 들어가는 계면 에너지는 **γ = 0.22 J m⁻² 하나**뿐이다 (`Table 1` · 출처 = Materials Project, ref 77). aux/금속 · 공극/금속 · aux/공극 **세 확산 계면에 똑같이** 쓴다 (`α = (3/4)γ l_w` · `m = 6γ/l_w` · 교차항 계수 1.5 공통).
> ② **금속 | SE 계면 Γ_ed/el 은 상장 밖의 날카로운 고정 경계**다. 거기엔 계면 에너지도, 점착 W 도, 접촉각도 없다. 상장 변수는 그 경계에서 **자연 경계조건 (법선 기울기 0)** 을 받는다 — 코드 `[BCs]` (`single_void/Na_stripping_void_homogeneous_CC.i:498–539`) 에 ξ_v · ξ_m · ξ_a 조건이 **하나도 없다**.
> ③ 기울기 0 경계에서 확산 계면은 벽과 **90° 로 만난다** → Young–Dupré (`W = γ(1 + cos θ)`) 로 읽으면 **W(Na | NBA) = γ = 0.22 J m⁻² 가 암묵적으로 박혀 있는** 셈이다 (**우리 추론 · 논문에 없음**). 논문도 Eq. 19 가 *"does not consider the contact angle between the void, metal electrode and the SE separator"* 라고 스스로 적는다.
> ⇒ 우리 W 를 넣으려면 **Γ_ed/el 에 젖음 경계조건을 새로 넣어야 한다** (코드 수정 · §5d). 지금은 넣을 칸이 없다.
> ④ **민감도**: 논문은 γ · W 를 바꿔 보지 않았다 (n/a). 바꿔 본 것은 계면 폭 l_w (`Fig. A·1` · 0.5 → 0.7 µm 에서 반공극 −13 %) · GB 전도도 (≤ 10 %) · 전류밀도 (C_crit 0.78 → 0.58 mAh cm⁻²) 셋이다. 차수 어림으로는 0.5 mA cm⁻² 에서 모세관 (γ) 구동력이 전류 구동 확산 퍼텐셜 차의 **공극 규모 (r ≈ 5 µm) 에선 ≈0.4 %**, **가장자리 규모 (곡률 반경 ≈ l_w) 에선 수 % – 20 %** 다 (§10-⑥ · 우리 어림) — 이 체제에선 W 가 전체 성장 속도보다 **가장자리 기하 · 국소 속도**에 들어갈 것이다.

> **본 digest 에서 크롭을 직접 본 그림 (2026-11-24)**: `Fig. 1` `Fig. 7` `Fig. 8` `Fig. 9` `Fig. 10` `Fig. 11` `Fig. 13` `Fig. 15` `Fig. 16` `Fig. S4` · Fig. A·1 — **11 장**. `Fig. 12` 는 크롭을 따로 열지 않았지만 **`Fig. 10` 과 같은 이미지 객체**다 (PDF xref 108 · §10-① — 그래서 사실상 본 셈).
> 크롭은 안 보고 **PDF 쪽 렌더 (저해상도) 로만 본 것**: `Fig. 2`–`Fig. 6` · `Fig. 14` · `Fig. 17` · `Fig. S1`–`Fig. S3` · `Fig. S5`–`Fig. S10`. 거기서 쓴 수치는 본문 명시값이거나 그림 안 글자 라벨 (예: *27.1 µm*) 이고, 곡선에서 읽은 값은 `figure-read ≈` 로 적었다.
> 표 (`Table 1` · `Table 2` · `Table S1`) 는 PDF 텍스트로 전사했다 (이미지로 안 읽음). ⚠ 논문 표기는 Table **I** · **II** · **S.1** 이다 — 웹앱 그림 링크가 아라비아 숫자만 잡아서 이 digest 는 `Table 1` · `Table 2` · `Table S1` 로 적는다.

---

## 1. 한 줄 요약

**grand-potential 다상 상장** (aux · Na 금속 · 공극 3 상, Ω_ed) 을 **날카로운 고정 금속 | SE 경계** 너머의 SE 전하 보존 (Ω_el) 과 묶어, **전극 두께 변화와 계면 공극 진화를 한 번에** 푼 Na | Na-β″-alumina 2D 모델이다 (MOOSE · 코드 공개). 완벽 계면이면 두께는 Faraday 그대로 변하고 (`Table 2` · 날카로운 계면 모델과 0.1–3.5 % 차), 계면 공극은 **계면을 따라 팬케이크로** 자란다 — 성장 속도는 공극 **가장자리에 몰린 Na 플럭스** (`figure-read ≈` 3.1–4.3 × i_app/F) 에 비례하고 **시간에 따라 가속**한다 (선형이 아님). 도금 땐 공극이 0.31–0.53 h 안에 사라진다. 다결정 SE 의 GB 전도도 (κ_gb/κ_g = 0.067 · 1 · 10) 는 공극 크기를 **국소적으로 ≤ 10 %** 만 바꾸고, 다공극은 전류가 클수록 빨리 합쳐져 **임계 박리 용량 C_crit 가 0.78 (0.1 mA cm⁻² 외삽) → 0.58 mAh cm⁻² (0.6 mA cm⁻²)** 로 준다.

⚠ 전부 **2D · 300 K · 역학 (적층압 · 크리프) 없음 · 전하이동 저항 없음 · 공극 핵생성 없음 (공극을 처음부터 심음)**. 실험과의 정량 대조는 **Li/LLZO 문헌값 한 점** (C_crit 이 22 % 낮다) 뿐이고, 같은 Na | NBA 실험 (ref 28 · CCS 1.5–2.5 mA cm⁻² @ 4–9 MPa) 과는 대조하지 않았다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 계 | **Na 금속 음극 | Na-β″-alumina (NBA) 세라믹 분리막** · 반쪽셀 (양극은 격자화 안 함 · 오른쪽 경계에 전류만 건다) |
| 영역 | **Ω_ed** = aux 상 + Na 금속 + 공극 (상장 3 변수 + 확산 퍼텐셜 + 전위) · **Ω_el** = SE (전위만) · 사이 **Γ_ed/el** = 날카로운 고정 경계 (`Fig. 1a`) |
| aux 상 | 집전체와 금속 사이 "빈 자리" 를 나타내는 가상 상. 금속이 줄면 aux/금속 확산 계면이 오른쪽으로 움직인다 (`Fig. 1b`) — **움직이는 금속|SE 계면을 추적하지 않으려고** 고안한 장치 |
| 던지는 질문 | (i) 완벽 계면 박리 · 도금 중 Na 두께 변화 (ii) 계면 공극 진화 + 전극 두께를 **동시에** (iii) SE GB 전도도가 박리 · 도금 속도 · 공극 이동 · 합쳐짐 속도에 주는 영향 |
| 문헌 공백 (저자) | 연속체 공극 모델 (Zhao 2022 · Agier 2022 · Barai 2024) 은 **균질 SE · Li/LLZO** · 전극 두께 고정. Narayan & Anand 2020 은 공극 없음 · Jang 2022 는 액체 전해질. GB 를 넣은 상장 (ref 42) 은 공극 · 음극 진화가 없다. **Na 전고체 셀 박리 · 도금 시뮬레이션은 처음** (저자 주장) |
| 동기 (서론) | 공극 → 계면 저항 ↑ · 전류 집중 → 다음 도금에서 덴드라이트 (CCS < CCP 이면 CCS 가 사이클 상한) · Na 금속이 Li 보다 크리프 저항이 낮아 CCS 가 높다 (ref 15 · 32) · Na | NBA 에서 CCS 1.5–2.5 mA cm⁻² @ 4–9 MPa (Jolly 2020, ref 28) |
| 연구 유형 | 계산 전용 · 연속체 상장 + 유한요소 (MOOSE phase-field module · Newton + LU) · 2D · 실험 0 |
| PI 배지 | 공저 아님 — 저자 4 명 (UF · LLNL · QuantumScape) 에 없다. 참고문헌 ref 14 · 16 · 17 · 18 · 23 에 'J. Sakamoto' 로만 나온다 |
| 공개 | 입력 파일 + 사용자 정의 소스 (GitHub) · 자료는 요청 시 (SC · MT) · 보조 동영상 S1–S6 (이 inbox 에는 없음) |

---

## 3. 핵심 수치 총정리 ★

> `figure-read` = 그림에서 읽은 값 (본문 미명시). **우리 계산** = Table 1 · 코드 값으로 이 digest 가 낸 값.
> 모든 값은 **Na | NBA · 2D · 300 K · 이 모델의 출력**이다 — 실험값이 아니다.

### 3a. 입력 매개변수 (`Table 1` 전사 + 우리 파생값)

| 기호 | 값 (Table 1) | 단위 | 출처 (ref) | 우리 계산 (300 K) · 비고 |
|---|---|---|---|---|
| T · R · F · z · k_B | 300 · 8.314 · 96487 · 1 · 8.62×10⁻⁵ | K · J/(mol K) · C/mol · — · eV/K | — | k_BT = 0.02586 eV |
| v_m (Na 몰부피) | 23.78 | cm³/mol | — | SI S.2 의 날카로운 계면 비교는 M_w/ρ = 22.98/0.9688 = **23.72** cm³/mol 을 쓴다 (값이 0.3 % 다르다) |
| **γ** (계면 에너지) | **0.22** | J/m² | **77 = Materials Project** (Jain 2013) | 어느 면 · 가중인지 **미기재**. aux/금속 · 공극/금속 · aux/공극 **공통** |
| l_w (확산 계면 폭) | 0.5 | µm | — (저자 선택) | **GB 폭도 같은 0.5 µm** (실제 GB 의 ≈10³ 배 · 저자) |
| α = (3/4)γ l_w | — | J/m | 53 | **8.25×10⁻⁸ J/m** |
| m = 6γ/l_w | — | J/m³ | 53 | **2.64×10⁶ J/m³** |
| L_φ (상장 동역학 계수) | 10⁻⁴ | m³/(J s) | — (저자 선택) | *"diffusion-limited rather than reaction-limited"* 로 고른 값 · 코드에 주석 처리된 thin-interface 식으로는 **2.3×10⁻⁸** (§5c-⑥) |
| c_v^eq (평형 공공) | e^(−2.0) · e^(−0.157/k_BT) | — | 78 (Sullivan & Weymouth 1964) | **3.12×10⁻⁴** · 형성 엔트로피 항 = **−2.0 k_B** (코드 이름 `vibrational_entropy`) |
| c_Na^eq,a · ^eq,m · ^eq,v | 10⁻⁸ · 1 − c_v^eq · 10⁻⁸ | — | — | c_Na^eq,m = **0.99969** |
| A^a/f_c · A^m/f_c · A^v/f_c (포물선 계수) | 310 · 11 · 310 | — | — (저자 선택 · *"no experimental data"*) | f_c = RT/v_m = **1.049×10⁸ J/m³** → A^m = 1.15×10⁹ · A^v = 3.25×10¹⁰ J/m³ |
| D_Na^m (Na 금속 자기확산) | 6.33×10⁻¹³ | m²/s | 79 (Mundy 1971) | 코드는 3 항 Arrhenius 로 계산 (§5b) — **6.330×10⁻¹³** 재현 |
| D_Na^v · D_Na^a | 0 · 6.33×10⁻¹³ | m²/s | — | aux 확산 = 금속과 같게 둠 |
| σ_m · σ_v · σ_a (전자 전도) | 2.1×10⁵ · 2.1×10⁻⁹ · 2.1×10⁵ | S/cm | 80 (West) | σ_v = 10⁻¹⁴ σ_m (`Fig. S4a`) · σ_a = σ_m (0 V 경계를 aux 왼쪽에 걸려고) |
| E_g · E_gb (NBA 활성화) | 0.20 · 0.35 | eV | 74 (Heinz 2021) | |
| K_g · K_gb (전지수 인자) | 8.537×10³ · 4.786×10³ | (S K)/cm | 74 | |
| κ_g^el = (K_g/T) e^(−E_g/k_BT) | — | S/cm | 74 | **1.25×10⁻² S/cm = 12.5 mS/cm** (`Fig. S4b` 색막대 0.012 와 일치 · `Fig. S1` SE 전위강하 7.4×10⁻⁵ V @ 0.5 mA cm⁻² 와 일치) |
| κ_gb^el (Table 1 그대로) | — | S/cm | 74 | **2.1×10⁻⁵ S/cm → κ_gb/κ_g = 1.7×10⁻³** ⚠ 본문 · 그림이 쓰는 **0.067 이 아니다** (§5c-①) |
| Δx · l_c · τ · f_c | l_w/3 · 10⁻⁹ m · l_c²/D_Na^m · RT/v_m | µm · m · s · J/m³ | — | Δx = **0.167 µm** · τ = **1.58×10⁻⁶ s** (1 h = 2.28×10⁹ τ) |
| 영역 | 50 µm (x) × 80 µm (y) · SE 18.5 µm | — | — | Ω_ed = 31.5 µm · 격자 300 × 480 QUAD4 (코드) |
| 초기 Na 두께 | 28.6 µm (박리 · 공극 · 순환) · 5.6 µm (완벽 계면 도금) | µm | — | |
| 공극 초기 | 반원 r = 4.8 µm (단일) · 반지름 다른 7 개 (다공극) | µm | — | 다공극은 코드상 4 개가 반원이 아니다 (§5c-⑤) |

> **Faraday 기준 두께 속도 (우리 계산)**: v = i·v_m/(zF) → **0.887 µm h⁻¹ per 0.1 mA cm⁻²** (v_m 23.78) · 0.885 (M_w/ρ 23.72 — `Table 2` 의 "Sharp" 열은 이쪽).

### 3b. 완벽 계면 · 균질 SE — 박리 · 도금 3 h (`Fig. 2`–`Fig. 4` · `Table 2`)

| i_app [mA cm⁻²] | ±0.1 | ±0.2 | ±0.3 | ±0.5 |
|---|---|---|---|---|
| 날카로운 계면 (S.4 · Faraday) [µm/h] | ∓0.885 | ∓1.770 | ∓2.655 | ∓4.425 |
| **박리 (이 논문, 선형 맞춤)** [µm/h] | **−0.854** | **−1.731** | **−2.620** | **−4.431** |
| **도금 (이 논문)** [µm/h] | **+0.865** | **+1.732** | **+2.583** | **+4.273** |
| 우리 계산: 박리 vs 날카로운 | −3.5 % | −2.2 % | −1.3 % | +0.1 % |
| 우리 계산: 도금 vs 날카로운 | −2.3 % | −2.1 % | −2.7 % | −3.4 % |
| 우리 계산: 박리 vs 도금 | 1.3 % | 0.06 % | 1.4 % | **3.6 %** |

- 본문 *"the difference in the simulated deposition and depletion rates is negligible (≲2%)"* 는 **0.5 mA cm⁻² 에서 3.6 %** 라 성립하지 않는다 (§10-③).
- 두께 라벨 (`Fig. 2`, 0.5 mA cm⁻²): 박리 **27.1 → 22.6 → 15.9 µm** (0.5 · 1.5 · 3 h) · 도금 **7.7 → 12.0 → 18.4 µm**. 첫 0.5 h 는 느리다 (28.6 → 27.1 = 3 µm h⁻¹ — 날카로운 초기 aux 계면이 확산 계면으로 퍼지는 과도 구간, 본문 *"small nonlinear regions at the start"*) · 0.5–3 h 기울기 (우리 계산) 4.44 µm h⁻¹ = 맞춤값 4.431 과 일치.
- SE 안 전류 i_mag/i_app 은 0.95–1.05 색막대 안에서 균일 (`Fig. 2`) · `Fig. S3` 에서 i_y/i_app ≈ 0 (±10⁻⁴).

### 3c. 완벽 계면 · 다결정 SE — 순환 3 h 박리 + 3 h 도금 @ 0.5 mA cm⁻² (`Fig. 5` · `Fig. 6` · `Fig. S5` · `Fig. S8`)

| 지표 | κ_gb/κ_g = 0.067 | 1 (균질) | 10 |
|---|---|---|---|
| 두께 라벨 0.5 / 3.0 / 4.7 / 6 h (`Fig. 5`) | 27.1 / **15.5** / 22.4 / **27.9 µm** | — | 27.1 / **15.7** / 22.4 / **27.8 µm** |
| SE 전류 i_mag/i_app 범위 (`Fig. 5` 색막대) | 0.08–2.15 (GB 에서 낮다) | 0.95–1.05 | 0.41–6.79 (GB 에서 높다) |
| 균질 대비 두께 % 차 최대 (`Fig. 6b`) | `figure-read ≈` **−2.5 %** (3 h) · 본문 *"about ~2.5%"* | 0 | `figure-read ≈` −1.2 % (≈3.2 h) |
| 6 h 뒤 원 두께 대비 | — | **< 1 %** 차 (본문) | — |
| \|∇μ_Na\| 최대 (`Fig. S8` 색막대) | 8.27×10⁷ J/(mol m) | — | 2.34×10⁸ J/(mol m) |

- 평균 계면 플럭스 = i_app/F (±5.18×10⁻⁵ mol m⁻² s⁻¹ @ 0.5 mA cm⁻²) — GB 전도도와 무관 (`Fig. S5a`). Na 총량은 0.9 → ≈0.49 → 0.9 로 되돌아와 **질량 보존** (`Fig. S5b`).
- 3 h 박리 뒤 aux/금속 계면이 **살짝 휜다** (다결정 두 경우 모두 · 균질은 평평 · `Fig. 5`) — SE 계면을 따라 플럭스가 고르지 않아서.
- 전류는 **삼중점 (triple junction) 근처에 몰린다** — 두 GB 로 들어온 전류가 나머지 하나로 나가야 하므로 (전하 보존, ref 81).

### 3d. 단일 공극 · 균질 SE — 박리 (`Fig. 7`–`Fig. 9`) ★

초기 = 계면 가운데 **반원 r 4.8 µm** · Na 28.6 µm · 1 h 또는 접촉 상실까지. 공극 크기 = 중심 → 가장자리 (ξ_v = 0.5) 거리의 **2 배**.

| 지표 | 0.3 mA cm⁻² | 0.4 | 0.5 | 0.6 |
|---|---|---|---|---|
| 반공극 @ 0.6 h (`Fig. 7b` 라벨) | **9.5 µm** | **11.7** | **14.3** | — |
| 반공극 @ 0.25 / 0.75 / 1 h (`Fig. 7a` 라벨, 0.5 만) | — | — | **8.0 / 17.9 / 25.1 µm** | — |
| 공극 크기 @ 1 h (`Fig. 9a`, 추적) | `figure-read ≈` 26 µm | ≈36 | ≈50 | ≈68 |
| 정규화 Na 플럭스 봉우리 F·j/i_app @ 0.6 h (`Fig. 9b`) | **3.1** (점선 라벨) · ≈10 µm 지점 | `figure-read ≈` 3.75 · ≈12 µm | `figure-read ≈` 4.25 · ≈15 µm | — |
| 먼 곳 (40 µm) 플럭스 | `figure-read ≈` 1.05 | ≈1.07 | ≈1.1 | — |
| 가장자리 속도 이동평균 (`Fig. 9c`) | `figure-read ≈` 5–10 µm/h (거의 평탄) | ≈10 → 20 | ≈12 → 28 | ≈12 → 40 · 끝에 ≈70 |
| SE 전류 최대 (`Fig. 7` 색막대) | — | — | **12.47 × i_app** (1 h · `Fig. 7a`) · 7.68 (0.6 h · `Fig. 7b`) | — |

- **모양**: 반원 → 계면을 따라 납작한 **팬케이크** (`Fig. 7a` · Li/LLZO 실험 ref 19 · 28 · 시뮬레이션 ref 35 · 36 과 정성 일치). 계면에 수직인 방향 성장은 작다 — **"void tip" (계면에서 가장 먼 점) 둘레 플럭스는 거의 0** (`Fig. 8`).
- **기전**: SE 안 전류가 공극 가장자리에 몰리고 (가운데는 접촉 상실로 0) → 금속 안 Na 플럭스도 가장자리에 몰려 **공극 면에서 SE 쪽으로 빠져나간다** (`Fig. 8`) → 공공이 반대 방향으로 가장자리에 들어와 공극이 계면을 따라 자란다.
- **가속**: 공극 크기는 처음엔 거의 선형, 그 뒤 가속 (0.5 · 0.6 mA cm⁻² 에서 뚜렷) → Lu 2022 (ref 30) 의 **선형 성장 가정은 틀릴 수 있다** (저자).
- **Eq. 19 적분**: 가장자리 플럭스로 낸 속도를 적분한 크기가 추적값과 맞는다 — 단 고전류 · ≥ 0.8 h 에서 벌어진다 (0.6 mA cm⁻² 1 h: `figure-read ≈` 68 대 66 µm). 저자 설명 = Eq. 19 가 접촉각을 안 본다.
- 금속도 위 · 아래가 가운데보다 많이 준다 (공극이 가운데 Na⁺ 플럭스를 막아서) → aux/금속 계면이 휜다.

### 3e. 단일 공극 · 균질 SE — 도금 (`Fig. 10` ⚠ · `Fig. 11`)

| 지표 | −0.3 mA cm⁻² | −0.4 | −0.5 | −0.6 |
|---|---|---|---|---|
| 공극이 사라지는 시각 (`Fig. 11a`) | `figure-read ≈` **0.525 h** (본문 *"≲0.52 h"*) | ≈0.42 h | ≈0.355 h | ≈0.31 h |
| 공극 크기 @ 0.2 h (`Fig. 11a` 표지 iv–vi) | `figure-read ≈` 6.85 µm | ≈5.95 | ≈5.2 | — |
| 플럭스 봉우리 @ 0.2 h (`Fig. 11b`) | `figure-read ≈` 2.8 · ≈3.5–4 µm | ≈2.75 | ≈2.7 | — |
| 가장자리 속도 (`Fig. 11c`) | `figure-read ≈` −5 … −10 µm/h | ≈ −8 … −12 | ≈ −10 … −14 | ≈ −11 … −15 · 소멸 직전 < −60 |

- 공극은 계면을 따라 줄어들고 **도금 끝에 사라진다** — Zhao 2022 (가둬진 공극이 남는다) 와 다르다. 저자 설명 = 계 · 초기 공극이 작다 (Zhao 는 80 × 250 µm² · r 10 µm).
- 도금에선 플럭스 봉우리가 전류와 거의 무관 (2.7–2.8) — 박리 (3.1 → 4.25) 와 다르다 (`figure-read`).
- ⚠ **출판된 `Fig. 10` 은 이 실험의 그림이 아니다** — 이미지가 `Fig. 12` (다결정 순환) 와 **같은 객체**다 (§10-①). 그래서 도금 공극 모양 (`Fig. 10a` −0.5 mA cm⁻² 시간 변화 · `Fig. 10b` 0.2 h 전류 비교) 은 **그림으로 확인할 수 없다**. `Fig. 11a` 의 표지 (i)–(iii) 는 −0.5 mA cm⁻² 의 0.1 · ≈0.255 · ≈0.353 h, (iv)–(vi) 는 0.2 h 의 세 전류라서, 원래 `Fig. 10` 이 무엇을 보여야 했는지는 알 수 있다.

### 3f. 단일 공극 · 다결정 SE — 순환 1 h 박리 + 1 h 도금 @ 0.5 mA cm⁻² (`Fig. 12`–`Fig. 14` · `Fig. S6`–`Fig. S9`)

| 지표 | κ_gb/κ_g = 0.067 | 1 | 10 |
|---|---|---|---|
| 반공극 0.25 / 1.0 / 1.25 / 2.0 h (`Fig. 12` 라벨) | 8.0 / **25.5** / 19.1 / 5.3 µm | — | 8.4 / **25.4** / 19.3 / 5.2 µm |
| SE 전류 최대 (`Fig. 12` 색막대) | 14.99 | — | 18.25 |
| +y 반공극 % 차 (균질 대비, `Fig. 13b`) | `figure-read ≈` 대부분 **양 (+)** · 최대 ≈+2.4 % (0.75 h) · 국소 골 ≈ −0.1 % (0.23 h) | 0 | 봉우리 `figure-read ≈` +5.4 (0.21 h) · **+6.4** (0.61 h) · +4.6 % (0.83 h) — 본문 *"just over 6%"* |
| 위 가장자리가 GB 에 닿는 시각 (`Fig. 13c,d`) | 6.2 µm GB: 0.123 h · 16.5 µm GB: 0.687 h | — | 0.117 h · **0.663 h** |
| 0.6 h 플럭스 봉우리 (GB 16.5 µm 근처, `Fig. 13e`) | `figure-read ≈` 3.9 | ≈5.3 | **≈12** (다른 GB 교차점 ≈22 · 28.5 · 35.5 µm 에도 봉우리) |
| −y (GB 7.5 µm 아래, `Fig. S6b`) | `figure-read ≈` 최대 +4.5 % (≈0.92 h) | 0 | ≈+10.5 % (≈0.92 h) |
| 2 h 전체 +y % 차 (`Fig. S7`) | `figure-read ≈` ≤ 2.4 % | 0 | 박리 5.4 · 6.4 · 4.6 % · 도금 ≈4.3 % (≈1.4 h) |

- **쌍결정 · 삼결정** (`Fig. 14` · 0.5 mA cm⁻² 박리 1 h): 수평 GB 를 공극 중심 **10 µm 위** (쌍결정) · **+ 15 µm 아래** (삼결정). +y 반공극 % 차 최대 **≈10 %** (쌍결정, 고전도) · **≈9 %** (삼결정, 고전도) [본문 · `figure-read ≈` 11 · 10 %] · −y 최대 **≈8 %** (삼결정 고전도 · 15 µm 아래 GB) · 저전도 GB 는 +y 에서 *"drops to 2%"* (본문 — 그림은 ≈ −2 % 의 **음수**). 닿는 시각 0.386 h (저전도) / 0.316 h (고전도) @ 10 µm · 0.669 / 0.609 h @ 15 µm 아래.
- 결론 (저자): **GB 전도도의 공극 이동 속도 영향은 ≤ 10 % — 작다.** 고전도 GB 쪽으로 다가갈 때 빨라지고 (봉우리), 저전도 GB 쪽으로 다가갈 때 느려진다 (골). ⚠ 저전도 곡선은 대부분 양 (+) 이라 "느려진다" 는 **기울기** 얘기지 **크기** 얘기가 아니다 (§10-⑨).
- **비대칭** (`Fig. S9`): 균질 SE 에서도 위 · 아래 가장자리 거리비가 1 에서 벗어난다 (`figure-read ≈` 균질 최대 ≈1.075 · 고전도 GB ≈1.09 · 0.6 mA cm⁻² ≈1.08 · 본문 *"≤ 8%"*) — 저자 원인 = **선형 QUAD4 요소의 이산화 오차** (가장자리 전류 봉우리가 위 · 아래 다르다: 0.25 h `figure-read ≈` 4.2 대 3.75). 전류가 클수록 비대칭이 크다 (`Fig. S9b`).

### 3g. 다공극 (`Fig. 15`–`Fig. 17`) ★

초기 = 반지름이 다른 공극 **7 개** · Na 28.6 µm · 접촉 상실 (공극 1 개만 남음) 까지.

| 지표 (균질 SE) | 0.3 mA cm⁻² | 0.4 | 0.5 | 0.6 |
|---|---|---|---|---|
| 접촉 상실 시각 t_f (`Fig. 15c`) | `figure-read ≈` **2.5 h** | ≈1.86 h | ≈1.22 h | ≈0.97 h |
| 0.55 mAh cm⁻² 시점 남은 공극 수 (`Fig. 15b` · `Fig. 15c` 표지) | 4 | 3 | 3 | — |
| 마지막 평균 공극 면적 (`Fig. 15d`) | `figure-read ≈` 215 µm² | ≈207 | ≈195 | ≈192 |
| **C_crit = i_app · t_f** (`Fig. 15e`) | `figure-read ≈` **0.755** | ≈0.742 | ≈**0.605** | ≈**0.58 mAh cm⁻²** |

- 0.1 mA cm⁻² **외삽** (0.3 · 0.4 두 점 직선 · `Fig. 15e` 점선) `figure-read ≈` **0.78 mAh cm⁻²** → *"about 22% lower"* than **Li/LLZO 실측 ≈1 mAh cm⁻² (0.7 MPa · 0.1 mA cm⁻², ref 29 · 37)**. 저자가 든 차이 원인: ① 공극을 미리 심어 핵생성 주기를 건너뛰었다 ② 적층압 (공극 억제) 이 없다 ③ 표면 확산이 없다.
- 0.4 → 0.5 mA cm⁻² 사이 C_crit 가 **급락** (0.742 → 0.605) — 합쳐짐 사건이 계단식이라 마지막 사건 순서가 바뀐 것일 수 있다 (§10-⑧).
- 초기 평균 공극 면적 `figure-read ≈` 17 µm² (`Fig. 15d` 시작점) = 코드 기하로 낸 **17.8 µm²** (우리 계산) — 전부 반원이면 14.4 µm² 라 맞지 않는다 (§5c-⑤). 초기 계면 접촉 상실 비율 ≈48 % (우리 계산).
- **다결정 다공극** (`Fig. 16` · 0.5 mA cm⁻²): 첫 합쳐짐 (7 → 6) `figure-read ≈` 0.67 h (저전도) · 0.71 h (균질) · **0.83 h (고전도 — 가장 느림)** · 3 → 2 는 고전도가 가장 빠름 (≈1.16 h). **접촉 상실 t_f**: 균질 `figure-read ≈` **1.22 h** · 고전도 ≈**1.33 h** · 저전도 ≈**1.37 h** → **두 다결정 모두 9–12 % 늦다** (§10-⑨). 마지막 평균 면적 ≈195–198 µm² (셋 비슷).
  - 공극 6 + 7 (합쳐지는 점이 GB 에서 멂): 0.67 h (저전도) vs 0.84 h (고전도) → 저전도가 빠름 · 공극 2 + 3 (합쳐지는 점이 GB 근처): 1.23 h (저전도) vs **1.16 h (고전도)** → 고전도가 빠름 (`Fig. 16e,f`).
- **공극 2 개 + 쌍결정** (`Fig. 17` · r 4.8 µm · 0.5 mA cm⁻²): ① GB 가 합쳐지는 점 근처 · 중심 간격 **20 µm** → 고전도만 **0.94 h** 에 합쳐짐 (평균 면적 ≈95 → ≈190 µm² 점프) · 저전도 · 균질은 1.2 h 까지 안 합쳐짐 ② GB 가 멂 · 간격 **15.8 µm** → 셋 다 1.2 h 까지 안 합쳐짐 · 공극이 **합쳐지는 쪽 반대로** 자란다 · 평균 면적 % 차 최대 +1.2 % (≈0.2 h, 고전도) · −0.2 % (저전도).

### 3h. 계면 폭 민감도 (Fig. A·1 · 부록 A.4) ★

| l_w [µm] | 0.5 | 0.6 | 0.7 |
|---|---|---|---|
| 반공극 @ 1 h, 0.5 mA cm⁻² (라벨) | **26.73 µm** | 26.51 | **23.16** (−13.4 %, 우리 계산) |
| SE 전류 최대 i_mag/i_app (색막대) | 12.47 | 10.23 | 9.13 |

- 계면이 넓을수록 가장자리 전류 집중이 약해지고 → 공극이 덜 자란다 (저자). ⚠ **수치 매개변수 하나가 결과를 13 % 움직인다** — GB 효과 (≤ 10 %) 보다 크다 (§10-②).
- ⚠ l_w = 0.5 µm 패널은 `Fig. 7a(iii)` (같은 조건 · 색막대 최대도 **같은 12.47**) 와 같은 결과로 보이는데 라벨이 **26.73 대 25.1 µm** 로 다르다 (§10-②).

### 3i. 검증 (`Fig. S1`–`Fig. S3` · `Table S1`)

| 검증 | 결과 |
|---|---|
| 전하 보존 (`Fig. S1` · S.4 해석해) | 금속 · aux 안 전위 ≈0, SE 안 선형 강하 · 해석해와 겹침 · x = 50 µm 전위 `figure-read ≈` −1.5 / −3 / −4.5 / −7.4 ×10⁻⁵ V (0.1 / 0.2 / 0.3 / 0.5 mA cm⁻²) · 전류 = i_app 상수 |
| 질량 보존 (`Fig. S2` · `Table S1`) | 부피평균 c_Na 감소 · 증가율 해석 ∓0.028 / 0.056 / 0.084 / 0.141 h⁻¹ 대 박리 −0.027 / −0.055 / −0.082 / −0.136 · 도금 +0.028 / +0.055 / +0.083 / +0.139 h⁻¹ |
| 계면 평균 플럭스 (`Fig. S2c,d`) | i_app/F (`figure-read ≈` 1.04 / 2.07 / 3.11 / 5.18 ×10⁻⁵ mol m⁻² s⁻¹) 로 시간 불변 |

- 본문 *"the difference between the Na loss and gain rates is negligible (≤1%)"* — 0.5 mA cm⁻² 에서 0.136 대 0.139 = **2.2 % (상대)** 라 **절대차 (h⁻¹) 로 읽어야** 맞다 (우리 계산). 해석 대비 박리 0.136/0.141 = −3.5 %.
- aux 상 Na 몰분율은 평형 10⁻⁸ 에서 ≈10⁻⁶ 으로 뜬다 (확산 퍼텐셜이 0 이 아니라서) — 총량엔 무시 가능 (저자).

---

## 4. 계산 방법 ★ — 모델 전체 (따라 하려면 필요한 것 전부)

> 이 논문엔 DFT · MD 가 없다. 템플릿의 "DFT/계산 방법" 칸 (functional · pseudo · k · ecut · AIMD · MLIP · 무질서) 은 **전부 해당 없음 (n/a)** 이다. 대신 상장 모델의 식 · 매개변수 · 경계조건 · 수치를 빠짐없이 적는다.
> 기호: ξ_a · ξ_m · ξ_v = aux · 금속 · 공극 상장 변수 (그 상에서 1, 밖에서 0) · μ_M^ed = 금속 M 의 확산 퍼텐셜 (J/mol) · φ^ed · φ^el = 전극 · SE 전위 · ξ_gi^el = SE 결정립 i 의 질서 변수 (정적).

### 4a. 영역과 상

- **Ω_ed** (집전체 ~ 금속 | SE 경계): aux 상 + 금속 + 공극(들). 상장 3 변수 + μ + φ^ed 를 푼다.
- **Ω_el** (분리막): 전하 보존만 (φ^el). SE 는 **단일 이온 전도체**로 보고 (NBA 전달수 ≈1, ref 63 · 64) 농도 구배를 무시한다 → SE 안 확산 방정식이 없다.
- **Γ_ed/el**: 두 영역 사이 **날카롭고 움직이지 않는** 경계. 금속이 줄어드는 것은 **aux/금속 확산 계면이 움직이는 것**으로 나타낸다 (`Fig. 1b`) — 날카로운 움직이는 계면을 추적하는 어려움 (ref 44 질량 보존 문제) 을 피하려는 설계다.
- 공극은 **이미 핵생성됐다고 가정**하고 Γ_ed/el 에 붙여 심는다 (실험이 계면 공극을 보여서 · ref 19 · 28). 공극은 Γ_ed/el 을 가로지르는 금속 이온 이동을 막는 장벽 역할.
- 집전체는 따로 나타내지 않는다 (aux 의 왼쪽 경계 Γ_L 이 집전체 자리).
- **온도 300 K · 정적 GB** (∂ξ_gi^el/∂t = 0).

### 4b. 자유 에너지 — grand-potential 범함수 (Eq. 1–4)

Eq. 1 (Ω_ed):
`Ψ^ed = ∫ [ Σ_p (α/2)|∇ξ_p|² + m { Σ_p (ξ_p⁴/4 − ξ_p²/2) + 1.5(ξ_a²ξ_m² + ξ_a²ξ_v² + ξ_m²ξ_v²) + 1/4 } + ω_bulk^ed ] dV`  (p = a, m, v)

- **α = (3/4) γ l_w** (기울기 에너지 계수) · **m = 6.0 γ / l_w** (장벽 높이) — Moelans 2011 (ref 53) 관계식. 교차항 계수 **1.5** 는 모든 상 쌍에 같다 → **모든 확산 계면의 에너지 = γ** · 폭 = l_w (우리 확인: Moelans 의 γ_ij = 1.5 에서 g(γ) = √2/3 이라 σ = g√(αm) = γ, 폭 √(8α/m) = l_w).
- Eq. 2: `ω_bulk^ed = Σ_p h_p ω_p` (상별 bulk grand potential 의 보간).
- Eq. 3: `ω_p(μ) = f_p(μ) − μ c_M^p(μ)/v_m` — **독립 변수는 c 가 아니라 μ** (grand-potential 의 핵심 · Kim–Kim–Suzuki 처럼 계면에서 상들이 같은 확산 퍼텐셜을 갖는다 → 계면과 bulk 구동력이 분리돼 µm 규모 계면 폭을 쓸 수 있다).
- Eq. 4 (보간 함수): `h_p = ξ_p² / (ξ_a² + ξ_m² + ξ_v²)`.
- **포물선 자유에너지** (S.1–S.3): `f_p = (A^p/2)(c_Na^p − c_Na^eq,p)²` → `c_Na^p(μ) = μ/(A^p v_m) + c_Na^eq,p` → `ω_p = −[μ²/(v_m² A^p) + μ c_Na^eq,p / v_m]`. 로그 (이상 · 희박 용액) 형은 희박 상에서 수렴이 나빠 안 썼다 (ref 72). A^p 는 *"high enough"* (농도가 평형에서 크게 안 벗어나게) 로 골랐고 실험 근거는 없다 — **10³ 배로 키우면 공극 상장이 불안정해진다** (`Fig. S10` · 구동력 ω_m − ω_v 가 μ 에 비례해 커져서).

### 4c. 상장 진화 — Allen–Cahn (Eq. 5)

`∂ξ_p/∂t = −L_φ [ m(ξ_p³ − ξ_p + 3ξ_p Σ_{q≠p} ξ_q²) − α∇²ξ_p + Σ_q (∂h_q/∂ξ_p) ω_q ]`
- L_φ 는 상 쌍에 상관없이 한 값 (**10⁻⁴ m³/(J s)**) · 확산 지배가 되도록 크게 잡았다 (저자 · ref 36 이 L_φ 가 공극 속도를 바꾼다고 보고). 실험 (고장 시간 · 공극 깊이) 으로 나중에 맞출 수 있다 (ref 37 처럼).

### 4d. Na 확산 — 플럭스 · 질량 보존 · μ 진화 (Eq. 6–8 · 부록 A.1–A.2)

- Eq. 6: `j_M^ed = −[(h_a M_a + h_m M_m + h_v M_v)/v_m] ∇μ_M^ed` · `M_p = D_M^p dc_M^p/dμ_M^ed` (dc/dμ = 열역학 인자의 역수 = 1/(v_m A^p)).
- 금속 bulk (ξ_m = 1) 에서는 **Fick 법칙** `j = −(D_M^m/v_m)∇c_M^ed` 로 줄어든다 (A.4) — 다른 금속 확산 모델 (ref 56–58) 과 같은 꼴.
- Eq. 7 (질량 보존): `(1/v_m)∂c_M^ed/∂t + ∇·j_M^ed = 0` — 이걸 직접 풀지 않고 μ 의 진화식으로 바꾼다:
- Eq. 8: `[Σ_p (dc_M^p/dμ)(h_p/v_m)] ∂μ/∂t + ∇·j_M^ed + Σ_p (Σ_q ∂h_p/∂ξ_q ∂ξ_q/∂t) c_M^p/v_m = 0`.
- 전극 안 전하 밀도 = 0 (금속 원자가 유일한 확산종) 이라 **정전 에너지 항은 범함수에 없다** (ref 51 · 59 · 62 와 다른 점).
- 질량 보존 · 플럭스 구성식 · 전하 보존은 범함수 최소화에서 나온 식이 **아니다** — 그래도 상장 · μ 에 대한 변분은 있어 저자는 "변분 모델" 이라 부른다.

### 4e. 전하 보존 (Eq. 9–12)

- Ω_ed (전자만 전하 운반): `i^ed = −(σ_a h_a + σ_m h_m + σ_v h_v)∇φ^ed` (Eq. 9) · `∇·i^ed = 0` (Eq. 10).
- Ω_el (Na⁺ 만): `∇·i^el = 0` (Eq. 11) · `i^el = −[κ_g^el (h_g^el − h_gb^el) + κ_gb^el h_gb^el]∇φ^el` (Eq. 12) — **옴 법칙만** (농도 구배 없음).
- NBA 전도도: `κ_p^el = (K_p/T) e^(−E_p/k_BT)` (p = g · gb · ref 74 Heinz 2021).

### 4f. 다결정 SE (Eq. 13 · `Fig. S4`)

- `h_g^el = Σ_i (ξ_gi^el)² / Σ_i (ξ_gi^el)²` · `h_gb^el = 16 Σ_i Σ_{j>i} (ξ_gi^el)²(ξ_gj^el)²` (ref 65).
  ⚠ 적힌 h_g 는 **분자 · 분모가 같아 항상 1** 이다 — 코드 (`ABSwitchingFunctionMaterial` = MOOSE `SwitchingFunctionMultiPhaseMaterial` 에 모든 결정립을 넣음) 도 그렇다. 그래서 실제 식은 `κ = κ_g + (κ_gb − κ_g) h_gb` 다. GB 한가운데 (두 ξ = 0.5) 에서 h_gb = 1 · 삼중점 (세 ξ ≈ 1/3) 에선 ≈0.59 (우리 계산).
- 미세구조 = MOOSE 안 **Voronoi 테셀레이션** (결정립 24 개 · 중심 좌표 파일 · §5b). GB 폭 = l_w = 0.5 µm — 평균 결정립보다 훨씬 작지만 실제 GB 의 **≈10³ 배** 라 GB 수송이 실제보다 훨씬 빠르다. 보정 (ref 65 의 Eq. 26 으로 GB 전도도를 낮춤) 은 *"can be reduced"* 라고만 하고 **적용하지 않았다** (코드에도 없다).
- 경우 셋: κ_gb/κ_g = **1 (균질) · 10 (고전도 GB · 표면 개질 ref 41 · 75 근거) · 0.067 (저전도 GB · ref 74 근거)**. κ_g 는 늘 Table 1 값. ⚠ 코드의 저전도 경우는 0.067 이 아니라 Table 1 Arrhenius 그대로 (1.7×10⁻³ · §5c-①).
- 금속 쪽은 **단결정**으로 본다 (다결정 금속의 GB 확산은 미래 과제, ref 76).

### 4g. 계면 · 경계 조건 (Eq. 14–18) ★ — 계면 에너지 · 점착이 들어가는 (들어가지 않는) 자리

| 경계 | 식 | 뜻 | 코드 (`single_void/…homogeneous_CC.i`) |
|---|---|---|---|
| Γ_ed/el 전류 연속 | `i^ed·n = i^el·n` (Eq. 14) | | `[InterfaceKernels] equality_of_current_density` (`InterfaceDiffusion`, 484–495) |
| Γ_ed/el 전위 연속 | `φ^ed = φ^el` (Eq. 15) | **전하이동 · 활성화 과전압 없음** → 1 차 전류분포 | `MatchedValueBC equality_of_electric_potential` (504–509) |
| Γ_ed/el Na 플럭스 | `j_M^ed·n = j_M⁺^el·n = i_x^el/(zF)` (Eq. 16) → 실제로는 **`i_x^el (1 − ξ_v)/(zF)`** | 공극 아래는 반응이 없어 플럭스 0 이어야 하는데 σ_v ≠ 0 이라 새어 나간다 → (1 − ξ_v) 를 곱해 0 으로 만든다 (안 그러면 수렴이 나쁘고 공극 안 c 가 0 아래로) | `MatNeumannBC flux_at_interface` (530–536) + `applied_flux_mat` = `ix_sep*(1-etaa0)*…` (818–825) |
| Γ_L (집전체 자리) | `φ^ed = 0` (Eq. 17) | 0 V 는 원래 aux/금속 계면에 걸어야 하지만 (움직여서 어렵다) 왼쪽 끝에 걸고 σ_a = σ_m 으로 둠 | `DirichletBC v_left` (515–521) |
| Γ_R (SE 오른쪽 끝) | `i^el·n_R = i_app` (Eq. 18) | 정전류 (박리 +, 도금 −) | `NeumannBC constantcurrent_right` (523–528) |
| 그 밖 모든 바깥 경계 | 플럭스 0 (자연 경계) | 위 · 아래 (y = ±40 µm) 는 **거울 대칭** → 공극은 사실상 80 µm 주기로 늘어선 배열 (우리 추론) | 조건 없음 |
| **Γ_ed/el 위의 상장 변수 ξ_v · ξ_m · ξ_a** | **조건 없음 = 자연 경계 (n·∇ξ = 0)** | **계면 에너지 · 점착 · 접촉각 항이 없다** → 평형 접촉각 90° (우리 추론) | `[BCs]` 블록에 해당 변수 **없음** (498–539) |

- ⭐ **우리 W 가 들어갈 자리는 마지막 행이다.** 지금은 비어 있어서 θ = 90° 가 고정된다 — Young–Dupré `W = γ_m/v + γ_SE/v − γ_SE/m = γ_m/v (1 + cos θ)` 에 넣으면 **W = γ = 0.22 J m⁻²** (우리 추론). W 를 바꾸려면 Γ_ed/el 에 **젖음 경계조건** (Cahn 형 표면 에너지 f_s(ξ) 의 변분 → `α n·∇ξ_v = −∂f_s/∂ξ_v` · 목표 cos θ = W/γ − 1) 을 넣어야 한다. W ≥ 2γ (= 0.44 J m⁻²) 면 θ = 0 (금속이 SE 를 완전히 적심 · 공극이 SE 위로 퍼지기 싫어함), W → 0 이면 θ → 180° (공극이 SE 를 따라 쉽게 퍼짐) (우리 추론 · W_ad 보고서 §7 과 같은 식).
- ⚠ **γ 와 W 는 같은 방법으로 내야 θ 가 뜻을 갖는다** — 이 모델의 γ 는 MP (PBE) 값이다. 우리 W (PBE+D3 · 고정기하 W_sep) 를 넣는다면 γ 도 같은 틀로 다시 내야 한다 (보고서 §7 의 *"γLi 도 같은 방법 · 같은 Li 면으로"* 와 같은 규칙).
- 이 모델에는 **계면 저항 (R_int) 도 없다** — 접촉 품질 (점착) 이 저항으로 들어가는 길도 없다.

### 4h. 무차원화 (부록 A.3 · Eq. A.10–A.17)

- `∇̃ = l_c ∇` · `t̃ = t/τ` · `ω̃ = ω/f_c` · `μ̃ = μ/RT` · `φ̃ = Fφ/RT` · **l_c = 1 nm · τ = l_c²/D_Na^m · f_c = RT/v_m**.
- `L̃_φ = L_φ τ m` · `κ̃ = α/(m l_c²)` · `Ã^p = A^p/f_c` (= 310 · 11 · 310) · `M̃_p = M_p τ RT/l_c²` · `σ̃_p = σ_p RT τ v_m/(F² l_c²)` · `κ̃_p = κ_p RT τ v_m/(F² l_c²)`.
- 수렴 때문에 무차원화했다 (저자).

### 4i. 수치 (MOOSE)

| 항목 | 논문 | 코드 (`single_void/…homogeneous_CC.i`) |
|---|---|---|
| 틀 | MOOSE (ref 69 · 70 · 71) phase-field module · 사용자 정의 Material · Function | `[Kernels]` 309–482 · `src/` · `include/` |
| 차원 · 격자 | 2D · 균일 4 절점 사각형 · Δx = l_w/3 | `GeneratedMeshGenerator` nx = 300 · ny = 480 (QUAD4 144,000 개) · 61–91 · 자유도 ≈0.5 M (우리 어림: Ω_ed 5 변수 + Ω_el 1 변수) |
| 영역 | 50 × 80 µm · SE 18.5 µm | `longitudnal_length 50e-6` · `lateral_length 80e-6` · SE 블록 `x ≥ 6500 nm` (8–9 · 58–59 · 75–81) |
| 시간 적분 | 암시적 · 적응 시간 간격 | `Transient` · **BDF2** · `IterationAdaptiveDT` dt₀ = 100 τ (≈1.6×10⁻⁴ s) · ×1.5 / ×0.8 · optimal 25 · window 2 · dtmin 10⁻⁴ (957–993) |
| 비선형 · 선형 | Newton + LU 전조건 · 상대 · 절대 허용 10⁻⁸ · 10⁻⁹ | `NEWTON` · PETSc `lu` + **MUMPS** · nl_rel 10⁻⁸ · nl_abs 10⁻⁹ · l_tol 10⁻⁶ · l_max 30 · nl_max 25 · SMP full |
| 미세구조 | MOOSE Voronoi | `PolycrystalVoronoi` (`file_name = center_pos.txt` · op_num 24 · rand_seed 10 · int_width = l_w) · `PolycrystalColoringIC` |
| 출력 | (본문 그림) | Exodus · checkpoint · CSV (후처리량) |

### 4j. 모델에 **없는 것** (저자 인정 + 우리 확인)

- **역학 전부** — 적층압 · 크리프 · 탄성 응력 (저자: 다음 과제 · 적층압이 공극을 억제한다고 서론에서 스스로 강조). README 는 solid mechanics module 을 켜라고 하지만 **입력 9 개 어디에도 역학 블록이 없다** (우리 확인).
- **전하이동 동역학** (Eq. 15 · 저자: 다음 과제) → 계면 저항 · 과전압 없음.
- **표면 확산** (공극 면을 따른 Na 확산 · 저자가 C_crit 차이 원인으로 언급).
- **공극 핵생성** (공극을 처음부터 심는다).
- **다결정 금속** · 다중 사이클 · **3D** (저자: MOOSE 는 차원 무관이라 확장 가능).
- SE 안 농도 구배 · 공간전하 · GB 폭 보정.

---

## 5. 코드 저장소 대조 ★ — 예제 입력의 매개변수 · 논문과 다른 점 · 점착을 넣을 자리

> 저장소 `souravmat-git/MOOSE-BatModelling` @ `3e44674` · 경로는 저장소 루트 기준 (로컬 사본 `/home/user/souravmat-git/moose-batmodelling/`).
> 입력은 전부 **0.5 mA cm⁻² (5 A m⁻²) 박리** 뿐이다 — 도금 · 순환 · 전류 스윕 · 쌍결정/삼결정 · 공극 2 개 · 계면 폭 스윕 입력은 **없다** (§5c-③).

### 5a. 저장소 구성 (파일 25 개)

| 파일 | 내용 |
|---|---|
| `README.md` | 개요 · MOOSE 앱 빌드 시 phase field + solid mechanics module 을 켜라 · `mpiexec -n <N> your-app-opt -i <입력>.i` · 사용자 정의 객체는 `registerMooseObject(<YourAppName>, <ClassName>)` 로 등록 (소스엔 자리표시 `"yourApp"`) |
| `perfect/Na_stripping_perfect_{homogeneous,lowGB,highGB}_CC.i` (868–873 줄) | 완벽 계면 (공극 변수 없음 · 상장 2 변수 aux + 금속) |
| `single_void/Na_stripping_void_{homogeneous,lowGB,highGB}_CC.i` (1018–1023 줄) | 단일 공극 (상장 3 변수) |
| `multiple_voids/Na_stripping_mv_{homogeneous,lowGB,highGB}_CC.i` (989–1008 줄) | 다공극 7 개 · `FeatureFloodCount` · `AverageGrainVolume` 후처리 |
| `*/center_pos.txt` (24 줄 · 세 폴더 md5 동일) | Voronoi 결정립 중심 24 개 (nm · x 6.9–24.2 µm · y −39.0 … +39.6 µm = 전부 SE 블록 안) |
| `single_void/pore_pos.txt` | `x y r` = `6500 0 4800` (nm) → 계면 (x = 6.5 µm) 위 반원 r 4.8 µm |
| `multiple_voids/multiple_pores_pos.txt` | 7 행 (§5c-⑤) |
| `single_void/bicrystal_pos.txt` · `tricrystal_pos.txt` | 결정립 중심 (15.5, 30) · (15.5, −10) µm [+ (15.5, −20)] → GB 가 y = **+10 µm** [+ **−15 µm**] (`Fig. 14` 설정과 일치) — ⚠ **어느 입력도 이 파일을 안 읽는다** (`file_name = 'center_pos.txt'` 고정) |
| `src/functions/CircleFunctionIC.C` + `.h` | 표 (x y r) 에서 원 안 1 · 밖 0 의 **날카로운** 초기 공극 |
| `src/materials/ABSwitchingFunctionMaterial.C` + `.h` | MOOSE `SwitchingFunctionMultiPhaseMaterial` 를 그대로 부름 → 모든 결정립을 넣으니 **h_g ≡ 1** |
| `src/materials/CTBarrierFunctionMaterial.C` · `CrossTermBarrierFunctionBaseWij.C` + `.h` | h_gb = **16 Σ_i Σ_{j>i} ξ_i² ξ_j²** (`SIMPLE`) 또는 4 Σ ξ_i ξ_j (`LOW`) — 입력은 `SIMPLE` |

### 5b. 매개변수 표 — 코드 값 · 파일:줄 · 논문 `Table 1` 대조

> 파일 약칭: **SV-H** = `single_void/Na_stripping_void_homogeneous_CC.i` · **SV-L** = `…_lowGB_CC.i` · **SV-HG** = `…_highGB_CC.i` · **PF-H** = `perfect/Na_stripping_perfect_homogeneous_CC.i` · **MV-H** = `multiple_voids/Na_stripping_mv_homogeneous_CC.i`.

| 양 | 코드 값 (원문 그대로) | 파일:줄 | 논문 Table 1 | 판정 |
|---|---|---|---|---|
| **계면 에너지 γ** | `sigma = 0.22  #J/m2` | SV-H:40 (PF-H:44 · MV-H:37) | 0.22 J/m² (ref 77) | ✅ 같다 · **유일한 계면 에너지 입력** |
| α · m | `kappa_dim = (3/4)*sigma*interface_width` · `mu_dim = 6*sigma/interface_width` | SV-H:619–620 | (3/4)γ l_w · 6γ/l_w | ✅ |
| 교차항 계수 | `gab = 1.5` (`gamma_names = 'gab gab'`) | SV-H:633 · 131 | 1.5 (Eq. 1) | ✅ 세 상 쌍 공통 |
| 계면 폭 l_w | `interface_width = 0.5e-6` · GB 폭 `int_width = interface_width/characteristic_length` | SV-H:6 · 137 | 0.5 µm | ✅ |
| L_φ | `L_dim = ${fparse 1e-4}` (위 두 줄에 thin-interface 식이 **주석 처리**됨) | SV-H:621–623 | 10⁻⁴ m³/(J s) | ✅ 값은 같다 · 식 대안은 §5c-⑥ |
| 포물선 계수 | `kvoid = 3.1e2` · `kspace = ${kvoid}` · `kmetal = 1.1e1` | SV-H:548–550 | 310 · 310 · 11 | ✅ |
| c_v^eq | `vibrational_entropy = -2.0` · `formation_energy_of_vacancy = 1.57e-1 #Sullivan (1974)` → `exp(S)·exp(-E/(kb_eV*T))` | SV-H:544–545 · 553 | e^(−2.0) e^(−0.157/k_BT) (ref 78 = Sullivan & Weymouth **1964**) | ✅ 값 · ⚠ 주석 연도 1974 ≠ 1964 |
| c_Na^eq | `exLi_void = 1e-8` · `exLi_space = ${exLi_void}` · `exLi_metal = 1 - c_v^eq` | SV-H:555–557 | 10⁻⁸ · 1 − c_v^eq · 10⁻⁸ | ✅ (변수 이름이 `Li` 로 남아 있다 — Li 코드에서 옮겨 온 흔적) |
| D_Na^m | `D_Na1 = 8.0 cm²/s · Q_Na1 = 14000` · `D_Na2 = 0.144 · 10840` · `D_Na3 = 0.009 · 8720` (cal/mol) 의 3 항 Arrhenius 합 | SV-H:24–35 | 6.33×10⁻¹³ m²/s (ref 79 Mundy 1971) | ✅ **6.330×10⁻¹³ 재현** (우리 계산) · 주석 단위 `cal/(mol K)` 는 cal/mol 의 오기 |
| D_Na^a · D_Na^v | `DC_space = ${fparse DC_metal}` · `DC_void = 0` | SV-H:565–566 | 6.33×10⁻¹³ · 0 | ✅ |
| σ_m · σ_v · σ_a | `cond_metal = 2.1e7` · `cond_void = 2.1e-7` · `cond_space = ${cond_metal}` (S/m) | SV-H:610–613 | 2.1×10⁵ · 2.1×10⁻⁹ · 2.1×10⁵ S/cm | ✅ |
| κ_g (NBA 결정립) | `prefactor = 8.537e3*1e2` (S K/m) · `activation_energy_grain = 0.20` → `(prefactor/T)*exp(-E/(kb_eV*T))` | SV-H:571–573 | 8.537×10³ (S K)/cm · 0.20 eV | ✅ → 1.25 S/m = 12.5 mS/cm |
| **κ_gb — 균질** | `cond_gb = 1 * cond_sep` | SV-H:614 · PF-H:530 · MV-H:611 | 비 1 | ✅ |
| **κ_gb — 고전도** | `cond_gb = 10 * cond_sep` | SV-HG:614 · PF-HG:530 · MV-HG:614 | 비 10 | ✅ |
| **κ_gb — 저전도** | `prefactor_GB = 4.786e3*1e2` · `activation_energy_GB = 0.35` · `cond_gb_measured = 1 * (prefactor_GB/T)*exp(...)` · `cond_gb = cond_gb_measured/cond_characteristic` | SV-L:576–578 · 619 (PF-L:501–503 · 535 · MV-L:573–575 · 616) | 본문 · 그림 = **비 0.067** | ⚠⚠ 코드 = Table 1 Arrhenius 그대로 → **비 1.7×10⁻³** (우리 계산) · §5c-① |
| SE 전도도 보간 | `cond_sep*(hd_sep - hgb_sep) + cond_gb*hgb_sep` | SV-H:805–811 | Eq. 12 | ✅ (hd_sep ≡ 1) |
| 결정립 | `op_num = 24` · `file_name = 'center_pos.txt'` · `PolycrystalVoronoi rand_seed = 10` · `coloring_algorithm = jp` | SV-H:132–133 · 940–946 | Voronoi (`Fig. S4`) · 개수 미기재 | 코드에서만: **24 개** · SE 18.5 × 80 µm² 에 평균 면적 61.7 µm² · 등가 지름 ≈8.9 µm (우리 계산) |
| 영역 · 초기 위치 | `longitudnal_length = 50e-6` · `lateral_length = 80e-6` · aux/금속 = `−L/2 + 3000 nm` · 금속/SE = `L/2 − 18500 nm` | SV-H:8–9 · 58–59 | 50 × 80 µm · SE 18.5 µm · Na 28.6 µm | ✅ (코드 경계값으로는 Na 28.5 µm + aux 3 µm — 확산 계면 반폭 안의 차) |
| 격자 | `grid_spacing = interface_width/3.0` · nx = 300 · ny = 480 · `QUAD4` | SV-H:11 · 63–73 | Δx = l_w/3 · 4 절점 사각형 | ✅ |
| 무차원 | `characteristic_length = 1e-9` · `characteristic_time = l_c²/DC_metal` · `Ec = R*T` | SV-H:7 · 37 · 20 | l_c 1 nm · τ = l_c²/D · f_c = RT/v_m | ✅ (τ = 1.58×10⁻⁶ s) |
| 전류 | `applied_current_density = 5 #A/m2` → `NeumannBC value = -applied_current_density/ic_calc` | SV-H:50 · 523–528 | 0.5 mA cm⁻² (그림마다 0.1–0.6) | 입력엔 **0.5 하나뿐** |
| 계면 플럭스 | `applied_flux_mat = ix_sep*(1-etaa0)*ic_calc/F/flux_calc` (완벽 계면은 `(1-etaa0)` 없음) | SV-H:818–825 · PF-H:696–703 | Eq. 16 + (1 − ξ_v) 보정 | ✅ |
| 시간 | `real_time = 2 h` (SV-H · MV) · `1 h` (SV-L · SV-HG) · `6 h` (PF 셋) | SV-H:44 · SV-L:44 · PF-H:48 · MV-H:41 | 단일 공극 1 h · 완벽 계면 3 h · 순환 6 h | ⚠ §5c-② |
| 공극 크기 측정 | `FindValueOnLine target = 0.5 v = etaa0` 수직선 x = **계면 − 200 nm** (SV-H) / **계면 − 000** (SV-L · SV-HG) | SV-H:857–875 · SV-L:862–880 | *"along the electrode/electrolyte interface"* | ⚠ §5c-④ |
| 공극 수 · 면적 | `FeatureFloodCount` (etaa0 · `connecting_threshold = 0.5` · `use_less_than_threshold_comparison = true`) + `AverageGrainVolume` | MV-H:845–861 | `Fig. 15c,d` · `Fig. 16c,d` | 후처리 정의 확인용 |
| 풀이 | `Transient` · `bdf2` · `NEWTON` · `lu` + `mumps` · `nl_rel_tol 1e-8` · `nl_abs_tol 1e-9` · `IterationAdaptiveDT dt = 100, growth 1.5, cutback 0.8, optimal_iterations 25` | SV-H:957–993 | Newton + LU · 10⁻⁸ · 10⁻⁹ · 적응 dt | ✅ (BDF2 · MUMPS 는 코드에서만) |

### 5c. 논문과 다른 점 · 코드에서만 보이는 것 ★

1. **⚠⚠ 저전도 GB 의 κ_gb/κ_g — 코드 1.7×10⁻³ 대 논문 0.067 (≈40 배).** 저전도 입력 셋 (SV-L · PF-L · MV-L) 은 Table 1 의 K_gb · E_gb 로 300 K Arrhenius 를 그대로 계산한다: `(4.786/8.537)·exp(−0.15 eV/k_BT) = 1.70×10⁻³` (우리 계산). 본문 · 그림 범례는 전부 **0.067** 이다. 0.067 을 300 K 에서 내려면 E_gb ≈ 0.255 eV 여야 한다 (우리 계산) — 논문에 그런 값은 없다. `Fig. S4c` 색막대 바닥 (0.001 S/cm) 으로는 가를 수 없다: `Fig. S4d` 최대 0.118 S/cm 가 10 κ_g (0.125) 의 ≈94 % 라 격자 표본이 GB 중심 (h_gb = 1) 에 못 닿는다는 뜻이고, 같은 표본률이면 0.067 은 바닥 ≈1.5×10⁻³, 1.7×10⁻³ 은 ≈8×10⁻⁴ S/cm 가 된다 — 둘 다 "0.001" 근처다 (우리 추론). 마지막 커밋 (2025-05-14) 이 바로 `Na_stripping_void_lowGB_CC.i` 를 고친 것이라, **그림을 만든 값이 어느 쪽인지는 알 수 없다** (얕은 클론 · 이전 판 없음).
2. **실행 시간이 논문 조건과 다르다.** 단일 공극 균질 2 h (논문 1 h) · 완벽 계면 6 h **정전류 박리** (논문은 3 h 박리 · 순환은 3 h + 3 h — 그대로 돌리면 0.5 mA cm⁻² × 6 h = 26.6 µm 를 벗겨 28.6 µm 중 ≈2 µm 만 남는다, 우리 계산). ⇒ 저장소 입력은 **그림 재현 입력이 아니라 틀**이다.
3. **없는 입력**: 도금 (전류 부호만 바꾸면 됨) · 순환 (시간에 따라 부호 바꾸는 경계 함수 필요) · 0.1–0.6 mA cm⁻² 스윕 · 쌍결정 / 삼결정 (위치 파일은 있지만 `file_name` · `op_num` 을 바꿔야 함) · 공극 2 개 (`Fig. 17`) · l_w 스윕 (`Fig. A·1`, Δx 도 같이 바뀐다).
4. **공극 크기를 재는 선이 경우마다 다르다.** 균질 단일 공극은 계면에서 **0.2 µm 금속 안쪽** 선 (x = 6.3 µm) 에서, GB 두 경우는 **계면 위** (x = 6.5 µm) 에서 ξ_v = 0.5 를 찾는다. `Fig. 13b` · `Fig. 14e,f` · `Fig. S6` · `Fig. S7` 의 "% change vs homogeneous" 는 균질 값을 분모로 쓴다. 그림이 이 후처리로 만들어졌다면 분모와 분자의 측정선이 다르다 — t = 0 (반원) 에선 차가 0.09 % (√(4.8² − 0.2²) · 우리 계산) 지만, 가장자리가 얇은 팬케이크가 되면 커질 수 있다 (크기는 모름 · 우리 추론). 논문 정의 (*"along the electrode/electrolyte interface"*) 와 맞는 쪽은 GB 입력이다.
5. **다공극이 전부 반원은 아니다.** `multiple_pores_pos.txt` 의 7 개 중 4 개 (y = 23 · 33 · −23 · −33 µm) 는 중심이 계면 (x = 6.5 µm) 보다 **0.7–1.4 µm 금속 안쪽** (x = 5.1–5.8 µm) 이라 반원보다 큰 원 조각이다. 반지름 4.8 · 2.8 · 2.0 · 3.0 · 2.0 · 3.2 · 2.5 µm (y = 0 · 23 · 33 · 12 · −8 · −23 · −33 µm). 코드 기하의 평균 면적 **17.8 µm²** (우리 계산) 가 `Fig. 15d` 시작점 `figure-read ≈` 17 µm² 와 맞는다 (전부 반원이면 14.4). 초기 접촉 상실 = 80 µm 중 38.4 µm (**≈48 %**, 우리 계산).
6. **L_φ 의 대안 식이 주석으로 남아 있다.** `zeta = (c_m − c_v)²·A^m v_m … /(Vm·D)` · `L = 4m/(3αζ)` (SV-H:621–622) — thin-interface 해석에서 나오는 확산 지배 L 이다. 값을 넣으면 **L ≈ 2.3×10⁻⁸ m³/(J s)** (우리 계산) 로 채택값 10⁻⁴ 의 **1/4300** 이다. 즉 채택 L_φ 는 물리값이 아니라 "계면 반응은 무한히 빠르다" 를 보장하려고 크게 잡은 수치 매개변수다 (저자 본문 서술과도 일치).
7. **초기 계면은 날카롭다.** aux/금속 (ParsedFunction `if(x < …, 1, 0)`) 과 공극 (`CircleFunctionIC`, 0/1) 모두 계단 초기값이라, 시작 직후 확산 계면으로 퍼지는 과도 구간이 생긴다 — `Fig. 2`/`Fig. 3` 의 첫 0.5 h 가 느린 이유와 같은 것으로 보인다 (저자도 *"start with a sharp aux/electrode interface"* 라고 적는다).
8. **역학 블록이 없다** (README 는 solid mechanics module 을 켜라고 함) · 사용자 정의 소스의 등록 이름은 자리표시 `"yourApp"` — 그대로는 컴파일 안 된다 (앱 이름으로 바꿔야 함).

### 5d. ★ 우리 점착 W 를 넣을 수 있는 자리 (코드 수준 · 우리 추론)

- **어디에**: `[BCs]` 블록 (SV-H:498–539) 의 경계 `metal_sep_int` (`SideSetsBetweenSubdomainsGenerator`, SV-H:83–89) 위에서 **상장 변수 `etaa0` (ξ_v) · `etab0` (ξ_m) · `eta_space` (ξ_a)** — 지금은 조건이 없어 자연 경계 (n·∇ξ = 0) 다.
- **무엇을**: 벽 에너지 `f_s(ξ) = Σ_p γ_SE/p h_p(ξ)` 의 경계 적분 (Allen–Cahn 약형식에 `∫_Γ L_φ (∂f_s/∂ξ_p) ψ dS` 항). 이 계에서 실제로 필요한 것은 **차 하나** — `Δγ_w = γ_SE/v − γ_SE/m = W − γ` (Young: γ_SE/v = γ_SE/m + γ cos θ · W = γ(1 + cos θ)). **지금 모델은 Δγ_w = 0 (W = γ) 인 특수한 경우**다.
- **넣을 값**: W(금속 | SE) 와 γ(금속 표면) — **같은 방법 · 같은 금속 면**에서 낸 쌍. 우리 W 원장 위치 (값은 여기 싣지 않는다): `db/properties/adhesion.json` (`surface_energies` · `adhesion_v*`) · `db/properties/wad_*.json` · 보고서 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` (§2 쌍별 값 · §7 Li 친화성 = 같은 Young–Dupré 식). ⚠ 우리 쌍은 Li / Ag / C / LPSCl / NCM 계라 **Na | NBA 인 이 모델에 그대로 넣을 값은 없다** — 넣으려면 모델을 Li | LPSCl (또는 Li | Ag–C) 로 다시 매개변수화해야 한다 (D · c_v^eq · κ · γ 전부).
- **영향이 어디로 가나**: ① 공극 가장자리의 **국소 각도** (얇은 쐐기 ↔ 뭉툭한 가장자리) ② 그 결과 Γ 위 ξ_v 분포가 바뀌어 **플럭스 차단 폭** (`(1 − ξ_v)` 곱) 이 바뀐다 ③ 모세관 구동력 자체는 이 전류 범위에서 작다 (§10-⑥). ⇒ W 의 효과는 **가장자리 기하 → 플럭스 집중 → 성장 속도** 로 간접적으로 들어간다. 크기는 돌려 봐야 안다 (논문 · 우리 모두 시험 없음).
- **같이 바꿔야 할 것**: l_w 민감도 (`Fig. A·1`, −13 %) 가 이미 GB 효과보다 크다 — W 민감도를 재려면 **l_w · Δx 수렴을 먼저** 보여야 한다 (가장자리 전류가 1 차 분포의 특이점이라 정규화 길이에 묶여 있다 · §10-④).

---

## 6. 결과 — 절별 상세 (그림 실독 포함)

### 6.1 모델 그림 (`Fig. 1`) — 크롭 실독

- **(a)** 왼쪽부터 Γ_L (집전체 자리) · aux 상 (ξ_a = 1) · 회색 점선 = aux/금속 확산 계면 · 금속 (ξ_m = 1 · 전자 e⁻ 는 왼쪽으로) · 파란 반원 = 공극 (ξ_v = 1 · 경계는 파란 점선) · **보라 실선 = 날카로운 Γ_ed/el** (법선 n_ed/el) · 오른쪽 SE (빨간 점선 = GB · M^z+ 는 오른쪽으로) · Γ_R (법선 n_R · 양극 쪽). 공극이 SE 에 닿은 구간에 **j_M^z+^el = 0** 이라는 표지가 있다 — 그림 단계부터 "공극은 플럭스를 막는다" 만 있고 **접촉각 · 벽 에너지 표기는 없다**.
- **(b)** 위 = t = 0, 아래 = 박리 t > 0: aux 상이 오른쪽으로 넓어지며 금속이 얇아지고 SE (GB 포함) 는 그대로다.

### 6.2 완벽 계면 · 균질 SE (`Fig. 2`–`Fig. 4` · `Table 2` · `Fig. S1`–`Fig. S3`) — 쪽 렌더

- `Fig. 2`: Ω_ed 는 c_Na 색 (금속 1 · aux 0), Ω_el 은 i_mag/i_app (0.95–1.05 에서 녹색 일색 = 균일). 금속 두께 라벨은 §3b. 50 µm 가로 화살표 · 80 µm 세로.
- `Fig. 3`: 두께 대 시간 직선 4 개씩 (박리 0.1–0.5 · 도금 −0.1 – −0.5 mA cm⁻²) · 기울기 라벨 = `Table 2` · 검은 표지 (i)–(iii) = `Fig. 2` 의 세 시각.
- `Fig. 4`: 3 h 뒤 ξ_a = 0.5 등고선을 전류별로 겹친 그림 — 전류가 클수록 박리 땐 더 오른쪽 (얇음), 도금 땐 더 왼쪽 (두꺼움). SE 18.5 µm 표기 · 점선 = 초기 위치.
- 검증 (`Fig. S1`–`Fig. S3` · `Table S1`): 해석해와 전위 · 전류 · 질량 변화율이 겹친다 (§3i). 저자는 *"our approach naturally conserves mass and does not require interfacial conditions at the moving interface"* 를 장점으로 든다 (움직이는 날카로운 계면 모델의 질량 보존 문제 · ref 44 · 47).

### 6.3 완벽 계면 · 다결정 SE 순환 (`Fig. 5` · `Fig. 6` · `Fig. S4` · `Fig. S5` · `Fig. S8`) — 쪽 렌더 (`Fig. S4` 만 크롭)

- `Fig. S4` (크롭 실독): (a) Ω_ed 전자 전도도 지도 — 로그 색막대 2.1×10⁻⁹ … 2.1×10⁵ S/cm · 공극 자리만 바닥색 · σ_a = σ_m · σ_v = 10⁻¹⁴ σ_m. (b) 균질 = 0.012 S/cm 일색 (색막대 라벨이 0.01 / 0.012 로만 찍힘). (c) 저전도 = 결정립 0.012 · GB 바닥 **0.001** S/cm. (d) 고전도 = 결정립 0.012 · GB 최대 **0.118** S/cm. 결정립은 세로로 긴 Voronoi 다각형 (코드 24 개).
- `Fig. 5`: 4 시각 (0.5 · 3.0 · 4.7 · 6 h). 저전도는 GB 를 따라 전류가 **낮고** (파랑) 고전도는 **높다** (주황–빨강) · 3 h 패널에 *"Curved aux/electrode interface"* 표기.
- `Fig. 6a`: 세 곡선이 V 자로 거의 겹침 (28.6 → ≈15.6 → ≈28 µm · `figure-read`). `Fig. 6b`: 균질 대비 % 차 — 저전도가 3 h 에 `figure-read ≈` −2.5 % 로 가장 크고, 고전도 ≈ −1.2 %, 도금 동안 0 쪽으로 돌아온다. ⇒ *"thickness … marginally impacted by the SE GB conductivity"*.
- `Fig. S8`: 같은 순환을 \|∇μ_Na\| 로 칠한 그림 — GB 가 계면과 만나는 점마다 μ 기울기 점이 찍힌다 · 그래도 c_Na 는 평형 근처 (A^p 를 크게 잡았기 때문 · 저자).

### 6.4 단일 공극 · 균질 SE 박리 (`Fig. 7`–`Fig. 9` · `Fig. S9` · `Fig. S10`) — 크롭 실독 ★

- `Fig. 7a` (크롭): 0.25 · 0.75 · 1 h. 흰 양방향 화살표 = **공극 중심 → 위 가장자리** (= 반공극) 라벨 8.0 · 17.9 · 25.1 µm. SE 쪽 색막대는 **로그** (0.01 … 12.47) — 공극 바로 앞 SE 는 0.01–0.2 (파랑–청록, 전류 거의 없음), **공극 위 · 아래 끝에 빨간 점** (전류 집중), 먼 곳은 1–2 (주황). 왼쪽 aux 띠가 위 · 아래로 갈수록 넓다 = 금속이 위 · 아래에서 더 줄었다. 가장자리는 SE 면을 따라 **가늘게 늘어진 쐐기** 꼴로 보인다 — 접촉각은 이 해상도로 못 읽는다.
- `Fig. 7b` (크롭): 0.6 h 에서 0.3 · 0.4 · 0.5 mA cm⁻² — 전류가 클수록 공극이 길고 (9.5 → 11.7 → 14.3 µm) 가장자리 빨간 점이 진하다 (색막대 최대 7.68).
- `Fig. 8` (크롭): 공극 상 (빨강 · ξ_v) 위에 Na 플럭스 화살표 (6500 개 상한 · 길이 ∝ 정규화 크기 · 색막대 0 … 5.7). 0.25 → 1.0 h 동안 **가장자리 화살표가 굵고 검붉어지며** (≈4–5.7) 방향은 **공극 면에서 SE 쪽 (오른쪽 위 · 아래)**. 공극의 가장 왼쪽 점 (*"Void tip"* 표기) 근처엔 화살표가 거의 없다. 먼 곳은 x 방향 · 크기 ≈1 (주황). 본문 서술과 일치한다.
- `Fig. 9a` (크롭): 실선 = 추적 · 점선 = Eq. 19 적분, 4 전류. 모두 9.6 µm (= 2 × 4.8) 에서 출발해 **아래로 볼록 (가속)**. 0.6 mA cm⁻² 만 0.6 h 뒤 실선 · 점선이 벌어진다 (1 h 에 ≈68 대 ≈66). ⚠ 표지 (i) 는 `figure-read ≈` **0.29–0.30 h** 에 찍혀 있다 — `Fig. 7a(i)` 은 0.25 h 다 (§10-⑪). (ii) ≈0.76 h ≈36 µm (= 2 × 17.9 ✓) · (iii) 1.0 h ≈50 µm (= 2 × 25.1 ✓) · (iv)–(vi) 0.6 h ≈19 · ≈23.5 · ≈29 µm (= 2 × 9.5 · 11.7 · 14.3 ✓).
- `Fig. 9b` (크롭): x = 공극 중심에서의 거리 (0–40 µm) · y = F·\|j_Na^ed\|/i_app. 공극 구간은 0 이다가 가장자리에서 수직으로 솟아 봉우리 (3.1 · ≈3.75 · ≈4.25) → 멀어질수록 ≈1.05–1.1 로 감쇠. ≈29 µm 부근에 세 곡선 모두 **작은 계단**이 있다 (원인 언급 없음 · 격자 표본 흔적으로 보임). 점선 = 0.3 mA cm⁻² 봉우리 3.1 을 *"j_Na^ed at ξ_v = 0.5"* 로 표기.
- `Fig. 9c` (크롭): 점 = 원자료 (흩어짐 ±10 µm/h 수준) · 실선 = 15 스텝 이동평균. 0.3 은 거의 평탄 (≈8 µm/h), 0.6 은 0.2 h 의 ≈18 → 0.9 h 의 ≈40 → 1 h 에 ≈70 으로 치솟는다.
- **Eq. 19**: `dy_tr/dt |_Γ = ±2 v_m j_tr(t)` · j_tr = 가장자리 (ξ_v = 0.5) 의 Na 플럭스 크기 · + 박리 / − 도금. 계수 2 의 유도는 없다 (휴리스틱) · 저자: *"suggests an improved approach … than that used by Lu et al. but a more quantitative analytical model is still needed"*.
- `Fig. S9` (쪽 렌더): 비대칭비 (위/아래 가장자리 거리) — 균질 SE 도 ≈1.07 까지 · 저자 원인 = 선형 요소 이산화 오차 (고차 요소 · 조밀 격자로 줄일 수 있음). `Fig. S10`: A^p × 10³ 이면 0.1 s 만에 ξ_v 가 계면을 따라 진동 (`figure-read ≈` 진폭 0.03 → 1 s 에 0.12) — 큰 구동력의 상장 불안정 (ref 5 · 6 of SI).

### 6.5 단일 공극 · 균질 SE 도금 (`Fig. 10` ⚠ · `Fig. 11`) — 크롭 실독

- `Fig. 10` (크롭): **보이는 그림은 다결정 SE (GB 선이 보임) · 0.25 · 1.0 · 1.25 · 2.0 h · 반공극 8.0 / 25.5 / 19.1 / 5.3 µm (a) · 8.4 / 25.4 / 19.3 / 5.2 µm (b) · 색막대 14.99 / 18.25** — 캡션 (균질 SE · −0.5 mA cm⁻² 도금 · (b) 0.2 h 전류 비교) 과 **전혀 안 맞고** `Fig. 12` 와 같다. PDF 에서 두 쪽 (14 · 16) 이 **같은 이미지 객체 (xref 108 · 1820 × 1453 px · 같은 해시)** 를 쓴다 — 출판 과정의 그림 중복이다 (§10-①).
- `Fig. 11a` (크롭): 9.6 µm 에서 내려가는 곡선 4 개 · 끝에 수직으로 떨어진다 (공극 소멸). 실선 · 점선이 끝까지 붙어 있다 (도금은 Eq. 19 적분이 잘 맞음 · 고전류에서 약간 벌어짐).
- `Fig. 11b` (크롭): 봉우리 ≈2.7–2.8 이 ≈3.5–4 µm 에 모여 있고 곡선 셋이 거의 겹친다 · ⚠ 범례가 **+0.30 / +0.40 / +0.50 mA cm⁻²** 로 찍혀 있다 (도금이라 음수여야 함 · 표기 실수).
- `Fig. 11c` (크롭): 속도는 음수 (공극 축소) · 전류가 클수록 더 음수 · 소멸 직전 −60 µm/h 아래로 떨어진다.

### 6.6 단일 공극 · 다결정 SE 순환 + 쌍결정 · 삼결정 (`Fig. 12`–`Fig. 14` · `Fig. S6` · `Fig. S7`) — `Fig. 13` 크롭 실독

- `Fig. 12` (= `Fig. 10` 이미지): 1 h 박리 후 1 h 도금. 공극은 1 h 에 최대 (반공극 ≈25.5 µm) → 2 h 에 거의 원래 (5.2–5.3 µm). 저전도 GB 는 GB 선이 **청록 (전류 낮음)** · 고전도는 **빨강 (전류 높음)**. 공극 앞 SE 의 전류 결핍 (파랑) 영역 · 가장자리 빨간 점은 균질과 같은 꼴.
- `Fig. 13a` (크롭): +y 반공극 대 순환 시간 — 세 곡선이 **Λ 자로 거의 겹침** (0 h 4.8 → 1 h ≈25.3 → 2 h ≈5 µm) · 점선 = GB 위치 6.2 · 16.5 µm. 표지 (i)–(iv) = `Fig. 12` 의 네 시각.
- `Fig. 13b` (크롭): 균질 대비 % 차 (박리 1 h 만). 고전도 (파랑) 는 0.2 h · 0.6 h 에 뾰족한 봉우리 (각 GB 를 지날 때), 저전도 (초록) 는 0.25 h 이후 **대부분 +1 … +2.4 %** 로 위에 있고 "Troughs" 화살표는 그 안의 **국소 골** 두 곳을 가리킨다.
- `Fig. 13c,d` (크롭): GB 에 닿는 순간의 확대 — 고전도 GB 는 빨간 선, 저전도는 청록 점선. 6.2 µm GB 에서 0.123 (저) / 0.117 h (고) · 16.5 µm GB 에서 0.687 / 0.663 h — 고전도 쪽이 **먼저 닿는다**.
- `Fig. 13e` (크롭): 0.6 h 계면 플럭스 — 고전도는 16.5 µm 근처 봉우리 ≈12 에 이어 ≈22 (≈6.8) · ≈28.5 (≈3.8) · ≈35.5 µm (≈8) 에 2 차 봉우리 (GB 와 계면이 만나는 곳) · 저전도는 같은 자리들에 **움푹한 골** (≈35.5 µm 에서 ≈0.6). 점선 세로줄 (GB) 은 `figure-read ≈` 16 µm 에 그어져 있다.
- `Fig. 13f` (크롭): 가장자리 속도 원자료가 크게 흩어지고 (5–55 µm/h) 이동평균은 10 → 30 µm/h · 고전도는 (vi) 0.15 h · (viii) 0.6 h 에 이동평균이 **튄다** (≈23 · ≈41).
- `Fig. 14` (쪽 렌더): 쌍결정 · 삼결정에서 GB 를 지날 때 % 차가 고전도 +10 / +9 % (+y) · +8 % (−y) 로 가장 크고, 저전도는 −2 % 남짓 — **결론: GB 영향 ≤ 10 %**.
- `Fig. S6` · `Fig. S7` (쪽 렌더): 아래 가장자리 (−y) 와 2 h 전체 그림 — 도금 중에도 고전도 쪽이 커지는 경향 (≈4.3 %).

### 6.7 다공극 · 균질 SE (`Fig. 15`) — 크롭 실독 ★

- `Fig. 15a` (크롭): 0.15 · 0.91 · 1.22 h · 공극 7 → 합쳐져 하나의 긴 막 · 접촉 상실이 커질수록 **SE 안 전류 집중 점 (빨강) 이 여러 개** 생기고 1.22 h 에 색막대 최대 **39.44**.
- `Fig. 15b` (크롭): 같은 용량 0.55 mAh cm⁻² 에서 세 전류 비교 — 겉모양은 비슷하지만 0.3 mA cm⁻² 쪽이 덜 합쳐졌다 (색막대 최대 31.86).
- `Fig. 15c` (크롭): 공극 수 계단 함수 7 → 1 · 전류가 클수록 왼쪽 (빠름). ⚠ 표지 (i) 는 `figure-read ≈` 0.19 h (`Fig. 15a(i)` 은 0.15 h).
- `Fig. 15d` (크롭): 평균 공극 면적 — 합쳐질 때마다 계단 상승 · 마지막 공극 하나가 남을 때 190–215 µm² 로 수직 상승.
- `Fig. 15e` (크롭): C_crit 대 전류 — 0.3 → 0.4 완만 (0.755 → 0.742) · **0.4 → 0.5 급락** (→ 0.605) · 0.6 에서 0.58 · 0.1 은 **점선 외삽** (0.78).
- Agier 2022 (ref 35) 를 따라 **C_crit = i_app · t_f** (t_f = 공극 하나만 남는 시각). 전류가 클수록 C_crit 가 줄어드는 것은 실험 (ref 29) · Li/LLZO 시뮬레이션 (ref 35 · 37) 과 정성 일치.

### 6.8 다공극 · 다결정 SE + 공극 2 개 (`Fig. 16` · `Fig. 17`) — `Fig. 16` 크롭 실독

- `Fig. 16a,b` (크롭): 공극 번호 1–7 (위 → 아래) · 저전도 (a) · 고전도 (b) · 0.15 · 0.91 · 1.22 h — 모양은 거의 같다 · 색막대 최대 40.91 / 39.45.
- `Fig. 16c` (크롭): 동그라미 두 개 — 첫 합쳐짐에선 *"High-conductivity GB case is slowest"* · ≈1.2 h 의 3 → 2 에선 *"fastest"*. ⚠ 그림에서 **마지막 2 → 1 (접촉 상실)** 은 균질 ≈1.22 h · 고전도 ≈1.33 h · 저전도 ≈1.37 h 로, **두 다결정이 모두 늦다** — 본문은 이 차이를 따로 말하지 않는다 (§10-⑨).
- `Fig. 16d` (크롭): 평균 면적의 같은 계단 · 동그라미 = 같은 두 사건.
- `Fig. 16e,f` (크롭): 공극 6 + 7 — 합쳐지는 점이 GB 에서 멀다 · 0.67 h (저전도) vs 0.84 h (고전도) · 공극 2 + 3 — 합쳐지는 점 근처에 GB · 1.23 h (저전도) vs 1.16 h (고전도). 저자 해석: **합쳐지는 점이 GB 근처면 고전도 GB 가 가장자리 속도를 높여 빨리 합쳐지고, 멀면 저전도 쪽이 빠르다.**
- `Fig. 17` (쪽 렌더): 공극 2 개 + 쌍결정 — GB 가 합쳐지는 점 근처 (간격 20 µm) 면 고전도만 0.94 h 에 합쳐지고, GB 가 멀면 (간격 15.8 µm) 1.2 h 까지 아무도 안 합쳐지며 공극이 합쳐지는 쪽 **반대로** 자란다 (inset % 차 +1.2 / −0.2 %). ⇒ *"void coalescence behavior depends on the position of the SE GB relative to the point of coalescence"*.

### 6.9 결론 (저자 글머리 그대로 요약) · 다음 과제

- Na 음극은 박리 · 도금에서 줄고 커지며 속도는 전류에 비례 · 날카로운 계면 모델과 일치.
- 완벽 계면에서도 다결정 SE 면 플럭스가 고르지 않아 aux/금속 계면이 살짝 휜다.
- 계면 공극은 박리 · 도금 중 **계면을 따라** 자라고 줄며, 이동 속도는 공극 가장자리의 Na/Na⁺ 플럭스에 비례한다 (전류에 의존) · 공극은 Na 음극의 줄고 커짐을 막는다.
- SE GB 성질은 국소 공극 이동 속도와 합쳐짐 속도에 영향을 주지만 **작다**.
- 다음 과제 (저자): ① 계면 전하이동 동역학 ② **적층압** ③ 다중 사이클 (셀 고장 예측) ④ **3D** (Na/NBA 공극 실험 ref 28 과 정량 비교하려면 필요 — 공극 수 · 총 부피를 사이클별로 보고한 실험).
