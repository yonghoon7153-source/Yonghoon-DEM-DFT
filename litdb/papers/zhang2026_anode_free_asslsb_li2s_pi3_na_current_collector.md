<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = zuo2022_chlorination_cathode_interface.md.
     2026-09-23 신규 — 1저자 연구실 논문세미나 0923-1.
     1저자 요청: "li2s 관련한 dft 계산들이 많았어 — 중점적으로 논문에이전트 진행하고 우리 계산이 참고할 게 있는지 봐봐".
     크롭 22장(그림 21 + 표 1) 중 17장을 실제로 봤다 (아래 목록). 커밋·푸시는 메인이 PDF 재대조 뒤에 한다. -->

# Stable and Low-Pressure Anode-Free All-Solid-State Li–S Batteries Enabled by Reaction-Derived Nanocrystalline-Amorphous Li₂S Cathodes and Deformable Sodium Current Collectors — Zhang et al. (*Adv. Energy Mater.* **2026**, e71471)

> slug `zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector` · DOI `10.1002/aenm.71471` · type `exp 주도 + AIMD 1건 (CP2K PBE-D3(BJ) · 231 원자 · 800 K 단일 온도 · 단일 궤적)` · PDF `litdb/inbox/0923-1. AdvEnergyMater_Zhang_AnodeFree_ASSLSB_Li2S-PI3_Na_CC_MAIN.pdf` (본문 11 pp) + `0923-1. Sup) AdvEnergyMater_Zhang_AnodeFree_ASSLSB_SI.pdf` (SI 19 pp — 원본은 `.docx`, Methods + Fig S1–S15 + Table S1–S2) · digested `2026-09-23` · status ✅ · 태그 **[외부]** · 세미나 `0923-1`

> elements: Li, S, P, I, Na, Cl, Br, Cu
> methods: DFT, AIMD, XPS, Raman

> **저자**: Qi Zhang⁺, Rui Yang⁺ (공동 1저자), Zhiwei Ni, Zhengran Wang, Baojuan Xi, Shenglin Xiong, **Aimin Zhang\***, **Jinkui Feng\*** (Shandong Univ. — 재료과학공학원 액고상 구조진화·가공 교육부 중점실험실 + 첨단장비코팅 국가중점실험실 · 화학화공학원) · 접수 2026-06-25 / 수정 2026-08-01 / 수락 2026-08-10 · Early View (권·호 `0`, 기사번호 **e71471**) · NSFC 52472219 · 62133007 + 산둥성 자연과학기금 ZR2024ME073 · 데이터 *"upon reasonable request"* (공개 데이터 없음) · ⚠ **계산 자원(계산센터·노드) 사사 없음**
>
> **문맥**: 같은 세미나의 0923-2(Liu, *Adv. Funct. Mater.* 2026 — Li₄SnS₄ mediator 로 Li₂S 활성화) · 0923-3(Wang, *Nat. Mater.* 24, 243 (2025) — MIEC 삼상계면, **이 논문의 ref 9**). Na 집전체 아이디어의 원전은 ref 20 (Yoon et al., *Matter* 8, 102463 (2025) — NCM622 + Na 집전체 저압 전지) — litdb 미보유.
>
> 🎤 **관련 발표**: 없음 — 2026-09-23 `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` 결과 대기열을 가진 파일은 `lee2026_skku_mlip_materials_design.md` 하나이고, 이 논문은 그 표에 없다.

> **본 digest 에서 실제로 본 그림 (2026-09-23)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` (본문 6장 전부) + `Fig. S5` `Fig. S6` `Fig. S7` `Fig. S8` `Fig. S9` `Fig. S11` `Fig. S12` `Fig. S13` `Fig. S14` `Fig. S15` (SI 10장) = **그림 16장** + `Table S1` 크롭 1장(크롭 검수용).
> **안 본 것**: `Fig. S1`(LiI 의 I 3d XPS) · `Fig. S2`(원료 Li₂S 의 S 2p XPS) · `Fig. S3` · `Fig. S4`(SEM/EDS) · `Fig. S10`(대칭셀 Nyquist) — 이 다섯 장은 본문 서술만 옮겼다.
> 표는 PDF 텍스트로 읽었다. ⚠ **크롭 결함 1건**: `tab_S1.png` 안에 **Table S2 본문 대부분이 같이 들어갔다**. Table S2 는 캡션이 다음 쪽(p18)으로 넘어가서 별도 크롭이 "거의 백지" 로 제외됐다 → webapp 에서 `Table S2` 를 누르면 그림이 안 뜬다. 값은 §3f 에 텍스트로 옮겼다.
> 그림에서만 읽은 값은 **`figure-read ≈`**, **우리 산수**는 **✎** 로 표시했다.

---

## 0. 이 digest 를 읽는 법 — 1저자 요청 읽기축

1저자 요청: *"li2s 관련한 dft 계산들이 많았어 — 중점적으로 … 우리 계산이 참고할 게 있는지"*.

**먼저 사실 하나 — 이 논문의 계산은 AIMD 한 건뿐이다.** 정적 DFT(구조이완·형성에너지·DOS·밴드갭)·NEB·Bader·COHP·계면·핵생성 계산은 **0건**이다. 본문·SI 텍스트 전체에서 "DFT" 는 SI 의 *"DFT-D3 method"* **1회**뿐이다. 그 한 건은:

- CP2K Quickstep (GPW) · PBE + D3(BJ) · GTH + MOLOPT · CUTOFF 520 / REL_CUTOFF 60 Ry
- **231 원자 Li₁₃₈S₆₉P₆I₁₈** (= 69 Li₂S + 6 PI₃ = PI₃ 8 mol%)
- 2000 K NVT 2 ps → 1500 K NPT 2.5 ps → **800 K NVT 40 ps** (dt 2 fs)
- 산출: **D_Li(800 K) = 2.36×10⁻⁵ cm² s⁻¹** 하나 + 부분 RDF 3개 + 스냅샷 2장 (`Fig. 1b–e`)

그래서 §7(중점)은 "이 한 건이 우리에게 무엇을 주나" 를 트랙별로 나눠 답한다:

| 갈래 | 트랙 · 1저자 | 이 digest 가 하는 것 |
|---|---|---|
| ① li2s 소셀 유리 | **li2s — 외부 1저자** (사용자 아님) | 프로토콜 대조와 **참고·주의 관찰만**. 판단은 그쪽 몫 (§7b) |
| ② MLIP-MD 결정계 규약 | 우리 DFT/MD 기준선 — 사용자 | 같은 표 금지 사유 (§7c) |
| ③ W_ad 리뷰 BW (B) 안 (CP2K GPW PBE-D3) | 우리 DFT (W_ad) — 사용자 | 이 논문이 규모·설정 근거가 되나 (§7d) |
| ④ ESW | ESW — 사용자 | Li₂S 활성화 창 · Na 전위 (§7e) |
| ⑤ DEM | DEM | 저적층압(0/1/4 MPa) 운전 · in-situ 압력 곡선 (§7g → `comparison_vs_ours_DEM.md` §I-7) |

실험부(구조·수송·전기화학·Na 집전체·압력)는 논문 수준으로 전부 옮겼다(§3·§5). 그림을 직접 보니 **본문 서술과 그림이 어긋나거나 본문이 말하지 않는 것이 열 건 넘게** 나왔다(§10).

---

## 1. 한 줄 요약

PI₃ 를 Li₂S 에 8 mol% 섞어 2 h 고에너지 밀링하면 LiI + 비정질 티오인산염(PS₄³⁻/P₂S₇⁴⁻/P₂S₆⁴⁻ + 환원 P) 이 나노결정 Li₂S 를 감싸 σ_ion 이 **1×10⁻⁸ → 3.28×10⁻⁵ S cm⁻¹** 로 오른다. 이 양극을 **변형 가능한 Na 집전체** 와 짝지은 무음극 LPSCBr 전고체 Li–S 셀이 **4 MPa 에서 0.5 C 200 사이클 ≈100 %**, **1 MPa 에서 300 사이클 70.54 %** 를 낸다. 계산은 **231 원자 AIMD 1건**(800 K D_Li = 2.36×10⁻⁵ cm² s⁻¹)으로 "재구성된 틀이 Li 를 잘 통한다" 를 **정성적으로** 받친다.

⚠ 세 가지를 같이 적어야 한다.
(i) AIMD 셀은 실험의 "나노결정 Li₂S + 비정질 매트릭스" 가 아니라 **반응물 조성 그대로의 균질한 용융 유래 유리**이고, **대조 계산(PI₃ 없는 Li₂S)이 없다**.
(ii) 8 % 셀의 첫 충전이 그림 속 **이론용량선(1166 mAh g⁻¹)을 넘는다**(`figure-read ≈`1330). SE·LiI·티오인산염의 용량 기여가 분리되지 않았다.
(iii) 명목 "1 MPa" 셀은 실측 **≈1.2–1.4 MPa** 에서 돌았다(`Fig. S13`) — 정간극 지그라 압력이 출력이다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 문제 | 무음극 ASSLSB 의 두 병목 — ① Li₂S 첫 충전 활성화 과전압(>3.5 V, ref 24)과 낮은 전도도(서론 문헌값: 이온 ∼10⁻⁸, 전자 ∼10⁻¹¹ S cm⁻¹) ② 저적층압에서 고체–고체 계면 불안정 |
| 양극 처방 | PI₃ 를 "반응성 전구체" 로 쓴다: 밀링 중 `Li₂S + PI₃ → LiI + 티오인산염` 이 **in situ** 로 일어나 나노 Li₂S 를 이온전도 비정질 틀에 박는다 |
| 음극 처방 | Cu 대신 **Na 금속 집전체** — 상온 Li 고용도 <1 %(합금 안 함, `Fig. S8`) · 항복강도 **0.19–0.28 MPa**(ref 50 인용값) → 저압에서 소성 변형으로 계면 공극을 채운다 |
| SE | **LPSCBr = Li₅.₅PS₄.₅Cl₀.₇₅Br₀.₇₅** (~20 µm, 냉간압착 ∼13 mS cm⁻¹ — ref 51 인용값, 이 논문은 미측정) |
| 선행 | Na 집전체 + NCM622 저압 전지(ref 20) — 이 논문은 그것을 **Li₂S 양극 · LPSCBr** 로 옮겼다 |
| 논문 스스로 단 단서 | *"Although the simulated pathway does not fully replicate the experimental ball-milling process, the resulting structural evolution still provides useful mechanistic insight"* (p.2) |

---

## 3. 핵심 수치 총정리 ★

### 3a. 합성·구조 (`Fig. 2`, `Table S1`)

| 항목 | 값 | 출처 |
|---|---|---|
| PI₃ 함량 | X = 4, 6, 8, 10 mol% | SI §1.2 |
| ✎ PI₃ 질량분율 (Li₂S–PI₃ 안) | **27.2 / 36.4 / 43.8 / 49.9 wt%** (4/6/8/10 mol%) | 우리 산수 (M_PI₃ 411.69, M_Li₂S 45.95 g mol⁻¹) |
| ✎ PI₃ 가 전부 LiI 로 갈 때 남는 원료 Li₂S | 93.7 / 90.4 / **87.0** / 83.3 % (몰 기준) | 우리 산수 (`PI₃ + 1.5 Li₂S → 3 LiI + …`) |
| XRD | LiI(PDF#74-1974) 선 출현 · Li₂S 선이 **넓어지고 약해짐 · 이동 없음** → 고용체 아님 | `Fig. 2a` |
| Rietveld (8 %) | 결정상 상대분율 **Li₂S 93.86 % · LiI 6.14 %** · **Rwp 2.08 %** · 비정질 기여 **~62.31 %**(내부표준 없음 → 논문 스스로 "정성") · Li₂S a = **5.7189 Å** | `Fig. 2b`, `Table S1` |
| ⁷Li MAS NMR | Li₂S **2.39 ppm**(본문) / **2.42 ppm**(그림 라벨 "mLi₂S") · LiI **−4.51 ppm**(본문) / **−4.56 ppm**(그림) · 비정질 티오인산염 속 Li(그림에 ≈0 ppm 봉우리, 라벨 없음) | `Fig. 2c` |
| ³¹P MAS NMR | PS₄³⁻ · P₂S₇⁴⁻ · P₂S₆⁴⁻ 세 성분 (`figure-read ≈`84 / ≈91 / ≈107 ppm) · 넓은 선폭 = 단거리 질서 | `Fig. 2c` |
| XPS P 2p | PS₄³⁻ · P₂Sₓ(P₂S₇⁴⁻/P₂S₆⁴⁻) · **환원 P (P′)** (`figure-read ≈`130 eV 부근) | `Fig. 2d` |
| XPS S 2p | Li₂S · 다리 S(P₂Sₓ) · 비다리 S(PS₄³⁻) — **Li₂S 성분이 바닥 수준으로 작다**(`figure-read`) | `Fig. 2e` |
| Raman | PS₄³⁻ **≈420**(최강) · P₂S₆⁴⁻ **380**(어깨) · 환원 P **360** · LiI **≈180** cm⁻¹ (본문) + 그림 라벨 PS₄³⁻ ≈265 · P₂S₆⁴⁻ ≈560 · 원료 Li₂S 단일선 `figure-read ≈`372 | `Fig. 2f` |
| TEM/SAED/HRTEM | 비정질 바탕 속 나노결정(점선원, `figure-read` 수 nm) · SAED 링 Li₂S(022)(004) + LiI(024)(004) · Li₂S(200) 격자무늬 **0.28 nm** (✎ a/2 = 0.286 nm 정합) | `Fig. 2g–i` |

### 3b. 수송 — Hebb–Wagner (`Fig. 3a`, `Fig. S5`, `Fig. S6`)

| 시료 | σ_ion (인쇄값) | ✎ 재계산 (`Fig. S5` 전류 + SI 식) | σ_e (인쇄값) |
|---|---|---|---|
| Li₂S | **1×10⁻⁸** — ⚠ `Fig. S5` 에 측정이 없다 | — | **2.29×10⁻¹¹** (`Fig. S6b,d`) |
| 4 % | 2.55×10⁻⁶ | 2.0×10⁻⁶ (인쇄값보다 26 % 낮음 — 원인 불명, 두께 차이 가능) | — |
| 6 % | **9.36×10⁻⁶** (`Fig. 3a`) / **2.59×10⁻⁵** (`Fig. S5b` 라벨) ⚠ 불일치 | **8.5×10⁻⁶** → `Fig. 3a` 가 맞고 `Fig. S5b` 라벨이 오기 | — |
| 8 % | **3.28×10⁻⁵** | 3.30–3.32×10⁻⁵ ✓ | **8.7×10⁻⁸** (`Fig. S6c,d`) |
| 10 % | **7.3×10⁻⁵** | 7.2–7.4×10⁻⁵ ✓ | — |

- 재계산 조건: R_LPSCBr = 20 mV / 0.32 mA = **62.5 Ω** · 40 mV / 0.62 mA = **64.5 Ω** (`Fig. S5a`) · `R_ion = U/I_total − U/I_LPSCBr` · `σ = L/(R_ion·S)` · L = **0.063 ± 0.002 cm**, S = **0.785 cm²** (`Fig. S5b` 인쇄) · 20 mV 와 40 mV 두 계단에서 각각 풀었다.
- ✎ 배율: σ_e **×3800** (2.29×10⁻¹¹ → 8.7×10⁻⁸) · σ_ion **×3280** (1×10⁻⁸ → 3.28×10⁻⁵) — **두 전도도가 같은 자릿수 폭으로 올랐다.** 본문은 전자 쪽을 *"increases slightly"* 라고 쓴다.
- ⚠ `Fig. S6b`: 0.2 / 0.3 / 0.4 V 에서 정상전류 `figure-read ≈`0.57 / 0.57 / 0.60 nA — **바이어스에 거의 무관** → 옴 거동이 아니고 측정 바닥 근처다. `Fig. S6c`: `figure-read ≈`0.4 / 0.8 / 2.4 ×10⁻⁷ A — **초선형**이고, 0.2·0.3 V 전류는 1 h 끝에도 아직 감소 중이다. ⇒ σ_e 두 값은 **자릿수 표지**로만 읽는다.

### 3c. AIMD (`Fig. 1b–e`, SI §1.6)

| 항목 | 값 |
|---|---|
| D_Li (800 K) | **2.36×10⁻⁵ cm² s⁻¹** (본문 p.2) — ✎ MSD 기울기 1.416 Å² ps⁻¹ ⇔ 40 ps 에 56.6 Å² |
| MSD 판독 (40 ps 끝) | Li `figure-read ≈`60 · I ≈13 · S ≈10 · P ≈5 Å² |
| MSD 모양 | Li 는 0–40 ps 거의 직선(≈15 ps 에 ≈24 → ≈31 Å² 계단) · **I·S 는 처음 ≈15 ps 동안 오르고 이후 거의 평탄** |
| ✎ 늦은 창 기울기 | 16–40 ps (`figure-read` 31 → 61 Å²) → 1.25 Å² ps⁻¹ → D ≈2.1×10⁻⁵ (보고값의 ≈88 %) |
| RDF | P–S 날카로운 봉우리 ≈2.0–2.1 Å (그림 g_max ≈14) · **P–P ≈2.3 Å** (g_max `figure-read ≈`19 → P₂S₆⁴⁻) · P–S 넓은 둔덕 3.7–4.5 Å (→ PS₄³⁻/P₂S₇⁴⁻) · Li–I 넓은 봉우리 ≈2.8 Å (→ LiI 유사 배위) |
| 스냅샷 | `Fig. 1d,e`: P(보라 "framework P") · S(노랑) · I(주황)만, **Li 미표시** · 패널마다 P 중심 다면체 ≈6개 |

### 3d. 양극 반응속도 (`Fig. 3b–f`, `Fig. S7`)

| 측정 | 값 (전부 `figure-read`, 인쇄값은 명시) |
|---|---|
| LSV (0.1 mV s⁻¹, 첫 충전 2.05–3.65 V) | 8 %: 봉우리 ≈0.85 mA @ ≈2.84 V · Li₂S: ≈0.47 mA @ ≈3.06 V (≈2.7 V 어깨). **개시는 둘 다 ≈2.45 V** |
| CV (1.7–3.0 V, 0.1 mV s⁻¹) | 8 %: 산화 ≈2.45 V(≈0.35 mA) · ≈2.82 V(≈0.38 mA), 환원 ≈1.97 V(≈−0.49 mA) · Li₂S: 산화 ≈2.55 V(≈0.15 mA), 환원 ≈2.1 V(≈−0.22 mA) |
| EIS + DRT (SOC/DOD 각 4점 + pristine) | 8 % 가 전 구간에서 임피던스·DRT 세기가 작다. SOC 100 % Nyquist 끝 ≈650 (8 %) vs ≈1400 Ω cm² (Li₂S). DRT 봉우리 τ ≈0.15 · ≈2 · **≈20–50 s** (8 %) / ≈0.12 · ≈1.1 · **≈12–40 s** (Li₂S) — ⚠ §10-⑪ |
| GITT (0.05 mA · 20 min 펄스 · 6 h 휴지) | Li₂S: 충전 ≈105 h + 방전 ≈110 h / 8 %: 충전 ≈325 h + 방전 ≈360 h — **본문에서 한 번도 언급되지 않고 D 도 안 뽑았다** |

### 3e. Na 집전체 반쪽셀 (`Fig. 4`, `Fig. S8`, `Fig. S9`)

| 항목 | 값 | 출처 |
|---|---|---|
| Li 석출 과전압 | Na **≈10 mV** vs Cu **≈22 mV** (인쇄) · Cu 는 핵생성 딥 `figure-read ≈`−55 mV (그림 주석 "≈30 mV" = 딥 − 평탄) · Na 는 딥 없음 | `Fig. 4a` |
| 첫 사이클 CE | Na **85.57 %** · Cu **76.49 %** (Cu 값은 그림에만) | `Fig. 4b` |
| 장기 CE | Na **평균 99.857 %**, 1000 사이클 · 0.5 mA cm⁻² · 0.5 mAh cm⁻² · ≈4 MPa (≈2000 h) · Cu 는 `figure-read` ≈60 사이클 안에 CE 40–60 % 로 붕괴 + 연단락/단락 | `Fig. 4e,f` |
| EIS | Li–Cu 초기 매우 큼(`figure-read` ≳700 Ω cm²) · Li–Na HF 절편 `figure-read ≈`26–29 Ω cm², 3 사이클 동안 변동 작음 · Cu 특성주파수 56.25 / 38.28 / 31.64 kHz (1–3 사이클) | `Fig. 4c,d` |
| CV (−0.05–0.5 V) | Li–Na 에 **≈0.4 V 산화 봉우리**(본문) — `figure-read` **≈0.37 V · ≈2.45 mA** (석출 전류보다 크다) | `Fig. S9` |
| 단면 SEM/EDS | 1 mAh cm⁻² 석출 후 조밀 연속층(`figure-read` ≈5 µm; ✎ 이론 4.85 µm) · 15 mV 까지 탈리 후 공극·박리 없음 · **EDS 맵은 Na · S · Br 뿐** | `Fig. 4g,h` |
| Li–Na 상도 (Landolt-Börnstein 전재) | 상온 상호고용 <1 % · ✎`figure-read` **공정 ≈360 K (≈87 °C)** · 단조(monotectic) ≈445 K · 액상 혼화갭 임계 ≈580 K @ x_Na ≈0.33 — 판독 교정: Na 녹는점 370.1 K(실제 370.9) · Li 453.6 K(실제 453.7) | `Fig. S8` |

### 3f. 완전셀 (`Fig. 5`, `Fig. S11`, `Fig. S12`, `Table S2`)

| 조건 | 값 |
|---|---|
| 공통 | LPSCBr SE · Na 집전체 · 25 °C(대부분 ±3 °C, 항온 챔버 아님) · ≈4 MPa(별도 표기 외) · 방전 컷오프 **1.7 V**(Na 기생산화 회피, `Fig. S11`) · 충전 3.0 V |
| 첫 사이클 0.05 C (≈1.3 mg cm⁻²) — `Fig. 5a` | 8 %: 방전 **971 mAh g⁻¹**(본문) · 충전 `figure-read ≈`**1330** (그림 속 이론용량 점선 1166 을 넘는다) · ✎ 첫 CE ≈73 %. 방전: 10 % ≈930 · 6 % ≈820 · 4 % ≈720 · 0 % ≈270 (`figure-read`) · 충전: 10 % ≈1290 · 6 % ≈1200 · 4 % ≈960 · 0 % ≈360 |
| 율속 (≈1.3 mg cm⁻²) — `Fig. 5b,c` | 8 %: 0.05 C ≈920–970 · 0.1 C ≈820–860 · 0.2 C ≈720–740 · 0.5 C ≈510 · 1 C ≈310–330 → 0.05 C 복귀 ≈1060 → 1140 (**계속 오름**) (`figure-read`) |
| 0.5 C 200 사이클 (≈1.3 mg cm⁻²) — `Fig. 5d,e` | 8 %: *"approximately 100 % capacity retention"* — `figure-read` 첫 0.5 C ≈505 → ≈590 (≈70 사이클) → ≈565 (200) · CE ≈100 % · 10 % ≈470 → ≈420 · 6 % ≈410 → ≈340 · 4 % ≈330 → ≈270 |
| 0.2 C 400 사이클 (**2.52 mg cm⁻²**) — `Fig. 5f` | **89.71 %**(초록·본문) / **89.72 %**(그림 라벨·`Table S2`) · `figure-read` ≈560–600 → ≈510 · ≈300 사이클에 "temperature fluctuation" 표기 |
| 90 °C · 1 C (**2.81 mg cm⁻²**, 3.26 mA cm⁻²) — `Fig. S12` | 1·2 사이클 `figure-read ≈`**1530 · 1280** (둘 다 1166 초과) → 3 사이클 ≈1160 → **828.87 mAh g⁻¹, 71.31 %** (≈62 사이클) · ✎ 1 C = 1166 mAh g⁻¹ 기준이면 3.28 mA cm⁻² — 인쇄 3.26 과 정합 |
| Li₂S 양극을 1.4 V 까지 방전 — `Fig. S11` | `figure-read` ≈265 mAh g⁻¹ 에서 **≈0.2 V 계단**(≈1.85 → ≈1.65 V) + dQ/dV ≈1.6 V 봉우리 = "oxidative side reaction" |
| 벤치마크 `Table S2` (PDF 텍스트) | In-doped Ag@SUS ~30 MPa · 50 °C · 80.2 %@250 / MXene/Mg 2 · 25 · 62 %@30 / Ag-ZnO@SUS 20 · RT · 80.8 %@100 / Cu₂Te@Cu ~13 · RT · 80 %@50 / AgF@SUS 20 · RT · 85.4 %@50 / Carbon Felt 7.5 · RT · 55.4 %@100 / Li₃N N/A · 55 · 75.8 %@200 / **this work Na: 4 · 25 · 100 %@200 · 4 · 25 · 89.72 %@400 · 1 · 25 · 70.54 %@300** |

### 3g. 압력 (`Fig. 6`, `Fig. S13`–`Fig. S15`)

| 항목 | 값 | 출처 |
|---|---|---|
| 첫 방전 (0.5 C, 활성화 3 사이클 후, ≈1.3 mg cm⁻²) | 4 MPa ≈ 1 MPa `figure-read ≈`450 mAh g⁻¹ · 0 MPa ≈360 | `Fig. 6b` |
| 300 사이클 (0.5 C) | 4 MPa **92.2 %** · 1 MPa **70.54 %** (`figure-read` ≈150 사이클부터 하락) · 0 MPa `figure-read` ≈330 → ≈160, ≈60 사이클에서 끝 | `Fig. 6c` |
| in-situ 압력 4 MPa (1.45 mg cm⁻²) | 시작 `figure-read ≈`4.3 → 휴지 ≈20 h 동안 ≈3.55 MPa 로 이완(✎ −17 %) · 활성화 3 사이클은 진폭이 크다 · 이후 가역 진동 — **본문 "3.4–3.8 MPa" = ≈100 h 부근의 띠** · ≈380–420 h 에는 ≈3.2–3.7 MPa (띠 전체가 ≈0.15–0.2 MPa 하강) · 충전 시 상승 / 방전 시 하강, 전압과 동기 | `Fig. 6d` |
| in-situ 압력 "1 MPa" | 시작 `figure-read ≈`1.31 → ≈1.19 · 활성화 봉우리 ≈1.55 / 1.49 / 1.46 · 67–315 h 정상 진동 **≈1.22–1.40 MPa** (진폭 ≈0.15–0.18) · 센서 분해능 계단 ≈0.0125 MPa 가 보인다 | `Fig. S13` |
| 초기 EIS HF 절편 | 0 MPa `figure-read ≈`50 · 1 MPa ≈20 · 4 MPa ≈18 Ω cm² (셋 다 거의 직선 = 차단형 응답) | `Fig. S14` |
| 10 사이클 뒤 EIS | 0 MPa ≈38–40 (+ ≈53 까지 반원) · 1 MPa ≈14 · 4 MPa ≈8–9 Ω cm² · 등가회로 `R_bulk + (CPE1‖R_gb) + (CPE2‖R_int) + (CPE3‖R_ct) + CPE4` — **적합값은 본문·SI 어디에도 없다** | `Fig. 6e` |
| 압력 전환 4 → 1 MPa | 4 MPa 10 사이클 `figure-read` ≈490 → ≈455 (CE ≈99 %) → 1 MPa 10 사이클 ≈440 → ≈368 (CE ≈98 %) — ✎ 감쇠 기울기 −3.9 → −7.7 mAh g⁻¹ cycle⁻¹ (≈2배) | `Fig. S15` |

---

## 4. 재료 & 방법 — 재현 조건 전부 ★

### 4a. 합성 (SI §1.1–1.2)
- 원료: Li₂S · PI₃ (Macklin) · MWCNT (Suiheng) · LPSCBr (~20 µm; 공급처 미기재) · Na (Changgao).
- Li₂S–PI₃ X %: Ar 글러브박스(O₂ <1 ppm · H₂O <0.01 ppm) 마노유발 10 min → ZrO₂ 용기 **3D 스윙 볼밀(QM-3B) 1400 rpm** · 15 min 가동 / 5 min 정지 · 1 h 마다 벽 긁기 · **유효 2 h** · BPR ≈30:1.
- 양극 복합체: Li₂S–PI₃ : LPSCBr : MWCNT = **5 : 4 : 1 (질량)**, 같은 밀링 조건.
- ✎ 8 % 양극 복합체에서 **원료 Li₂S 는 복합체 질량의 ≈28 %** (0.5 × 56.2 %, 반응 소모 전) — **LPSCBr 이 40 wt%** 로 원료 Li₂S 보다 많다.

### 4b. 셀 (SI §1.3)
- 반쪽셀: LPSCBr 100 mg · Ø10 mm 세라믹 몰드 **250 MPa 3 min** → Li 박(50 µm) **75 MPa 30 s** → Na(압연 50 µm) 또는 Cu 박 **25 MPa 30 s** → **4 MPa** 일정 외압에서 시험.
- 완전셀: LPSCBr 100 mg 250 MPa 3 min → 양극 복합체를 한쪽에 **400 MPa 3 min** → Na 박 **25 MPa 30 s** → 설정 외압에서 시험, **활성화도 같은 적층압에서**.
- 외압 지그(`Fig. 6a`): 볼트로 조이는 판 + 하부 하중센서. ⚠ **정간극(screw-tightened) 지그** — 압력은 제어값이 아니라 **출력**이다(§7g).

### 4c. 측정 (SI §1.4–1.5)
- XRD MiniFlex 600 (Cu Kα) · SEM JSM-7610F + EDS · TEM JEM-F200 (200 kV) · XPS ESCALAB 250Xi · Raman 532 nm (Renishaw inVia) · MAS NMR 600 MHz AVANCE NEO.
- 25 °C · NEWARE CT-4008 · CHI660E · **EIS 0.2 Hz–1 MHz, 진폭 10 mV** (전 측정 공통으로 적혀 있다).
- Hebb–Wagner: 전자 = 시료 100 mg 250 MPa + 양면 MWCNT 5 mg 250 MPa (이온 차단), 전류는 1 h 후 값 · 이온 = 시료 100 mg 250 MPa + 양면 LPSCBr 30 mg 250 MPa + Li 박 75 MPa (전자 차단), `R_ion = R_total − R_LPSCBr`, S = 0.785 cm². ⚠ SI 식의 σ 단위가 "S cm⁻²" 로 오기(→ S cm⁻¹).
- ⚠ LSV/CV(`Fig. 3b,c`)의 대극·기준이 명시되지 않았다 (창 1.7–3.0 V 로 보아 무음극 완전셀로 추정).

### 4d. 계산 (SI §1.6) — 전부

| 항목 | 값 | 비고 |
|---|---|---|
| 코드 | **CP2K / Quickstep** | 버전 미기재 |
| 방법 | **GPW** (Gaussian and plane waves) | |
| 범함수 | **PBE** | |
| 분산 | **DFT-D3, Becke–Johnson damping** | |
| 의사퍼텐셜 | **GTH** | 원소별 원자가(q) 미기재 |
| 기저 | **MOLOPT** (전 원소) | ⚠ **수준 미기재** — DZVP / TZVP / TZV2P, SR 여부 모름 |
| CUTOFF / REL_CUTOFF | **520 Ry / 60 Ry** | |
| SCF 수렴 | **1.0×10⁻⁴ ~ 5.0×10⁻⁵** ("depending on the simulation stage") | 고온 AIMD 용 느슨한 값 |
| 스미어링 | **Fermi–Dirac** ("to facilitate SCF convergence under high-temperature conditions") | 전자온도 미기재 |
| k 점 | **미기재** | CP2K MD 관례상 Γ 로 추정되나 논문은 말하지 않는다 |
| 스핀 | 미기재 | |
| 셀 | **231 원자 Li₁₃₈S₆₉P₆I₁₈** (= Li₂S–PI₃ 8 %) · *"constructed as a representative reconstructed framework"* | ⚠ **격자상수·밀도·초기구조 생성법 미기재** |
| ① 용융 | **NVT 2000 K, 2 ps** | dt·thermostat 미기재 |
| ② 치밀화 | **NPT 1500 K, 2.5 ps, 목표 1 bar** | dt·barostat 미기재 |
| ③ 평형/생산 | **NVT 800 K, 40 ps, dt 2 fs (20,000 steps)** | thermostat 미기재 · **③ 의 부피 = ② 끝 부피** |
| 담금질 램프 | **없음** — 1500 K → 800 K 즉시 전환 | 본문은 *"melt-quench protocol"* 이라 부른다 |
| 확산 | Einstein `D = (1/6)·d⟨|r(t)−r(0)|²⟩/dt`, *"slope was obtained from the linear region of the MSD curve"* | **적합 창 · 시간원점 평균 여부 미기재** |
| 온도 | **800 K 하나** | 아레니우스·Ea 없음 |
| 시드 / 궤적 | **미기재** (하나로 보인다) | 오차막대 없음 |
| 계산 자원 | **미기재** (사사에도 없음) | 벽시간·노드·GPU 여부 모름 |
| `Fig. 1d,e` 캡션 *"different thermal protocols"* | Methods 에는 **한 가지 프로토콜만** 있다 | 어느 패널이 어느 단계인지 미기재 |

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 AIMD — "재구성된 틀이 Li 를 통한다" (`Fig. 1b–e`) ★★

**논문 논리**: melt 로 만든 Li₂S–PI₃ 8 % 구조에서 (i) Li MSD 가 크고(D = 2.36×10⁻⁵ @800 K) (ii) RDF 에 P₂S₆⁴⁻(P–P 2.3 Å) · PS₄³⁻/P₂S₇⁴⁻(P–S 2 Å + 3.7–4.5 Å) · LiI(Li–I 2.8 Å) 특징이 보인다 → *"PI₃ incorporation promotes the formation of a thiophosphate-rich framework that likely contributes to enhanced Li⁺ transport"*.

**그림을 보고 확인한 것**
- **`Fig. 1b`** — y 0–60 Å², x 0–40 ps, 곡선 4개(Li 실선, I·S·P 점선).
  · Li 는 `figure-read ≈`60 Å² @40 ps 까지 거의 직선이다(≈15 ps 에 ≈24 → ≈31 계단). ✎ 보고 D 는 기울기 1.416 Å² ps⁻¹ ⇔ 40 ps 에 56.6 Å² 로 그림과 맞는다.
  · **I(≈13)·S(≈10)·P(≈5 Å²) 는 0–15 ps 에 오르고 그 뒤 거의 평탄**하다. 1500 → 800 K 급전환 뒤 **음이온 골격이 ≈15 ps 동안 이완**했고, 그 뒤로는 거의 정지했다고 읽힌다. Li 의 15 ps 계단이 I·S 의 계단과 **같은 시각**이다 = 집단 재배열 1회.
  · ⇒ 보고 D 가 0–40 ps 전체 적합이면 **이완 과도구간이 섞여 있다**. ✎ 16–40 ps 만 쓰면 D ≈2.1×10⁻⁵ (보고값의 ≈88 %) — 창 선택에 크게 민감하지는 않지만, 단일 궤적이라 이 차이의 유의성은 말할 수 없다.
  · ⚠ 800 K 에서 S 가 ≈10 Å² 움직인 것은 결정 Li₂S 의 열진동 수준이 아니다 — 시뮬레이션 계는 **결정 Li₂S 를 포함하지 않는 비정질 상태**다(`Fig. 1d,e` 에도 반형석 격자가 안 보인다).
- **`Fig. 1c`** — x 1–6 Å, 곡선 3개. P–S(보라 실선) g_max `figure-read ≈`14 @≈2.1 Å · P–P(빨강 점선) g_max ≈19 @≈2.25–2.3 Å · Li–I(주황 점선) 넓은 봉우리 g ≈2.3 @≈2.8 Å · P–S 3.7–4.5 Å 는 g ≈0.8–1.5 의 완만한 둔덕.
  · ✎ **P 가 6 개뿐**이라 P–P 쌍은 15 개다. g_max 19 · 폭 ≈0.2 Å 로 적분하면 P 당 P–P 이웃 ≈0.2–0.35 개 = **셀 전체에 P–P 결합 ≈1 개** 수준이다 (⚠ 밀도가 미기재라 ideal-mixing 부피 ≈4300 Å³ 를 가정한 우리 추정). "P₂S₆⁴⁻ 가 생긴다" 는 **P₂S₆ 단위 1개의 일화**다.
  · ⚠ 본문은 3.7–4.5 Å 를 *"wavelength range"* 로 적었다(→ distance). 그 대역의 P–S 는 **어느 티오인산염이든** 갖는 2차 이웃이라 PS₄³⁻ 와 P₂S₇⁴⁻ 를 가르지 못한다.
- **`Fig. 1d,e`** — 상자 테두리 + P(보라)·S(노랑)·I(주황), **Li 미표시**. 패널마다 P 다면체 ≈6개(일부 P 는 둘씩 가깝다). 캡션은 *"with different thermal protocols"* 인데 Methods 는 한 프로토콜만 적는다 — **두 패널이 무엇의 차이인지 알 수 없다**.
- **`Fig. 1a`** — 개념 모식도(양극 / LPSCBr / Na 집전체, 비정질 티오인산염 속 나노 Li₂S, 석출·탈리 때 Na 변형). "Key features" 세 개(저압 계면 접촉 · 빠른 Li⁺ 경로 · 계면 완충 껍질)는 **주장 목록**이지 데이터가 아니다.

### 5.2 구조 (`Fig. 2`, `Table S1`)
- `Fig. 2a` XRD: PI₃ 4–10 % 에서 LiI 선(주황 점선 ≈25.5° · ≈29.6° · ≈42.5°)이 약하게 나타나고, Li₂S 선이 넓어지고 약해진다. 봉우리 이동이 없어 고용체가 아니다. 밀링 시료는 전부 저각 쪽으로 **배경이 크게 솟는다**.
- `Fig. 2b` Rietveld: 배경이 강도의 대부분을 차지하는 패턴에서 **Rwp 2.08 %**. 배경 지배 패턴은 배경만 잘 맞춰도 Rwp 가 낮게 나와 적합 품질의 증거로는 약하다(§10-⑱). 비정질 ~62.31 % 는 논문 스스로 정성값이라 한다.
- `Fig. 2c` NMR: ⁷Li 에 mLi₂S 2.42 ppm(큰 봉우리) + ≈0 ppm(두 번째, 라벨 없음 = 본문의 "비정질 티오인산염 속 Li") + LiI −4.56 ppm(작다). ³¹P 는 세 성분인데 **P₂S₆⁴⁻(≈107 ppm) 봉우리 높이가 PS₄³⁻(≈84 ppm)와 비슷하다**(`figure-read`) — P(IV)–P(IV) 결합 단위가 주성분 중 하나다.
- `Fig. 2d,e` XPS: P 2p 에 환원 P(P′, 녹색)가 분명하다. **S 2p 의 Li₂S 성분(주황)은 바닥 수준**이다 — 시료는 몰비로 92 % 가 Li₂S 인데 표면(수 nm)은 티오인산염이 덮는다 = "Li₂S 핵 + 비정질 껍질" 그림과 맞는다. 논문은 이 대비를 말하지 않는다.
- `Fig. 2f` Raman: 8 % 스펙트럼에 LiI ≈180–190 · PS₄³⁻ ≈265 · P′ ≈360 · P₂S₆⁴⁻ ≈380 · PS₄³⁻ ≈420(최강) · P₂S₆⁴⁻ ≈560. 원료 Li₂S 는 ≈372 단일선이다. ⚠ **8 % 에서 Li₂S 372 선이 어디로 갔는지** 논문이 말하지 않는다 — P′(360)과 P₂S₆⁴⁻(380) 배정 사이에 끼어 있다.
- `Fig. 2g–i` TEM: 비정질 바탕에 나노결정(점선원) · FFT 확산 헤일로 + 약한 점 · SAED 링(Li₂S + LiI) · HRTEM Li₂S(200) 0.28 nm.

### 5.3 수송 (`Fig. 3a`, `Fig. S5`, `Fig. S6`)
- `Fig. 3a`: 로그축 막대 5개(1×10⁻⁸ · 2.55×10⁻⁶ · 9.36×10⁻⁶ · 3.28×10⁻⁵ · 7.3×10⁻⁵ S cm⁻¹), 단조 증가.
- `Fig. S5a`: 바이어스 10 → 50 mV 계단(각 2000 s), Li|LPSCBr|Li 전류 0.15 / 0.32 / 0.47 / 0.62 / 0.78 mA. `Fig. S5b`: 네 조성의 계단 전류 + 인쇄 σ + 두께 0.063 ± 0.002 cm.
  · ✎ **재계산이 인쇄값을 받친다** (8 %·10 % 는 ±2 % 안). **6 % 만 `Fig. S5b` 라벨(2.59×10⁻⁵)이 자기 전류와 안 맞는다** → 오기다. 4 % 는 재계산 2.0×10⁻⁶ vs 인쇄 2.55×10⁻⁶ (+26 %, 원인 불명).
  · ⚠ 원료 Li₂S 의 1×10⁻⁸ 은 **`Fig. S5` 에 측정이 없다**(4–10 % 만 있다) — 서론의 문헌값 "∼10⁻⁸" 과 같은 수다.
  · ⚠ 이 "σ_ion" 은 **SE|시료 계면 두 개를 포함한 유효값**이다(참조셀로 빼는 것은 Li|SE 계면과 SE 벌크뿐).
- `Fig. S6`: §3b 참조. 본문의 *"increases slightly"* 는 그림(×3800)과 맞지 않는다. 두 측정 모두 옴 거동이 아니라서 σ_e 두 값은 **자릿수 표지**다.

### 5.4 반응속도 (`Fig. 3b–f`, `Fig. S7`)
- `Fig. 3b` LSV: 봉우리 ≈3.06 → ≈2.84 V 로 **≈0.2 V 음이동**, 전류 ≈1.8배. 개시는 둘 다 ≈2.45 V — 본문의 *"negatively shifted oxidation onset"* 은 **봉우리 이동**으로 읽어야 한다.
- `Fig. 3c` CV: 8 % 는 산화 2봉(≈2.45 / ≈2.82 V) · 환원 1봉(≈1.97 V), Li₂S 는 각 1봉에 작은 전류.
- `Fig. 3d–f` EIS/DRT: SOC 쪽으로 가며 Nyquist 가 부풀고 방전 쪽으로 가며 오그라든다. 8 % 가 전 구간 작다. ⚠ Nyquist 는 **세로로 어긋나게 쌓은(offset) 그림**이라 −Im 절대값을 읽으면 안 된다. ⚠ DRT 최대 봉우리 τ ≈10–50 s 는 ✎ f = 1/(2πτ) ≈3–16 mHz 로, **SI 가 적은 EIS 하한 0.2 Hz(τ ≈0.8 s) 밖**이다(§10-⑪).
- `Fig. S7` GITT: 8 % 가 Li₂S 보다 **약 3배 긴 충전 시간**(≈325 vs ≈105 h)을 받아내고, 충전 펄스의 과전압 스파이크가 작다(`figure-read` Li₂S ≈0.3–0.5 V vs 8 % ≈0.1–0.25 V). 본문 미언급 · D 미산출.

### 5.5 Na 집전체 (`Fig. 4`, `Fig. S8`, `Fig. S9`, `Fig. S11`)
- **논리**: 낮은 Li 고용도(`Fig. S8`) + 낮은 항복강도(ref 50) → 저압 접촉 유지. Na 의 환원전위(−2.71 V vs SHE)가 Li 보다 덜 음이라 *"may reduce the thermodynamic driving force for electrolyte decomposition"*. 한편 본문은 *"LPSCBr exhibits a narrow stability window that precludes direct Li pairing"* 이라고도 쓴다(§10-⑭).
- `Fig. S9`: Li–Na 는 Li–Li 와 같은 크기의 석출/탈리 전류를 내고, 탈리가 끝난 뒤 **≈0.37 V 에 큰 산화 봉우리(≈2.45 mA — 석출 전류보다 크다)** 가 나온다. 논문 귀속: *"parasitic oxidation of Na or Na-derived interphase species, indicating potential interfacial instability under high overpotential"*.
  · ✎ **우리 읽기**: E°(Na⁺/Na) −2.71 V(논문) − E°(Li⁺/Li) −3.04 V(교과서값 — 논문에 없음) = **+0.33 V vs Li⁺/Li**. 봉우리 위치가 이 값과 맞는다 ⇒ **Na 금속 자체의 산화**(Na → Na⁺, SE 로 들어감)로 설명된다. 부수적 계면종이 아니라 **집전체가 소모되는 반응**이다.
- `Fig. S11`: Li₂S 양극 완전셀을 1.4 V 까지 방전하면 ≈265 mAh g⁻¹ 에서 **≈0.2 V 계단**(≈1.85 → ≈1.65 V) + dQ/dV ≈1.6 V 봉우리가 나온다. ✎ 이 계단은 "석출된 Li 가 바닥나 음극 전위가 Li → Na⁺/Na(+0.33 V)로 뛰는 순간" 과 정량적으로 맞는다 ⇒ **1.7 V 컷오프는 선택이 아니라 필수**이고, 무음극 셀에서는 **매 방전 끝이 이 경계에 닿는다**.
- `Fig. 4a,b`: 과전압 10 vs 22 mV, Cu 의 핵생성 딥 ≈30 mV — Na 위에는 딥이 없다(= 핵생성 장벽이 작다; 해석은 ref 54 인용). CE 85.57 vs 76.49 %. Na 는 탈리 중 전압이 서서히 오르고 Cu 는 가파르게 오른다.
- `Fig. 4c,d`: Li–Cu 초기 임피던스 ≳700 Ω cm²(강체 Cu 접촉 불량), 1 사이클 뒤 두 반원. Li–Na 는 Re 26–38 Ω cm² 범위에서 조금 움직인다.
- `Fig. 4e,f`: Na 1000 사이클 · 2000 h 안정 vs Cu 연단락 → 단락.
- `Fig. 4g,h`: ⚠ 본문 *"elemental maps confirming uniform Li distribution adjacent to the Na current collector"* — **실린 맵은 Na · S · Br 뿐**이고 Li 는 EDS 로 검출되지 않는다. "Li" 층은 SEM 대비로 그은 점선이다.

### 5.6 완전셀 (`Fig. 5`, `Fig. S12`, `Table S2`)
- `Fig. 5a`: PI₃ 가 늘수록 충전 과전압↓·용량↑, 8 % 가 최적(방전 971 mAh g⁻¹). ⚠ **8 %·10 %·6 % 의 첫 충전이 전부 그림 속 "Theoretical capacity" 점선(1166)을 넘는다**(`figure-read` ≈1330 / ≈1290 / ≈1200). 본문은 이것을 말하지 않는다.
  · ✎ 초과분의 후보: ① 양극 복합체의 LPSCBr(40 wt%) 산화 — 3.0 V 충전은 argyrodite 의 열역학 산화 onset 위다(§7e) ② LiI(I⁻/I₃⁻)·티오인산염·환원 P 의 산화환원 ③ 정규화 기준 — "Li₂S loading" 이 원료 Li₂S 인지 Li₂S–PI₃ 인지 미기재. ✎ PI₃ 8 mol% 는 복합체의 **43.8 wt%** 이고, PI₃ 가 전부 LiI 로 가면 원료 Li₂S 의 13 % 가 소모된다 — 기준에 따라 비용량이 최대 ≈1.8배 달라진다.
- `Fig. 5b,c`: 율속 — 복귀 0.05 C 가 처음보다 **높고 계속 오른다**(≈1060 → 1140) = 사이클 중 추가 활성화 또는 부반응 용량.
- `Fig. 5d,e`: 0.5 C 200 사이클 — 첫 0.5 C 대비 오르다가(≈505 → ≈590) 서서히 내려온다(≈565). "≈100 % retention" 은 **상승 후 하강**을 한 숫자로 접은 것이다.
- `Fig. 5f`: 2.52 mg cm⁻² · 0.2 C · 400 사이클 89.72 %. 셀이 **항온 챔버가 아니라 25 ± 3 °C** 에 있어 ≈300 사이클의 용량 점프가 "temperature fluctuation" 으로 표기돼 있다.
- `Fig. 5g` / `Table S2`: 기포 차트(색 = 적층압 0–30 MPa, 크기 = 온도 25/40/55 °C). 비교 문헌의 압력(2–30 MPa)·온도(RT–55 °C)·사이클 수(30–250)가 제각각이라 **같은 조건 비교가 아니다**.
- `Fig. S12`: 90 °C · 2.81 mg cm⁻² · 1 C — 1·2 사이클이 **1530 · 1280 mAh g⁻¹(> 1166)**, 이후 62 사이클에 71.31 %. 본문은 *"highly reversible areal capacity"* 라고만 쓴다. ⚠ 90 °C = 363 K 는 **자기 `Fig. S8` 의 Li–Na 공정점(✎`figure-read` ≈360 K) 바로 위**이고, Na 의 상동온도 T/T_m ≈0.98 이다 — Li 가 쌓이는 Na 계면에 액상이 생길 수 있는 조건인데 논의가 없다.

### 5.7 압력 (`Fig. 6`, `Fig. S13`–`Fig. S15`)
- `Fig. 6a`: 볼트 4개로 조이는 판 + 하부 하중센서. 셀 = Li₂S–PI₃ 8 % 양극 / LPSCBr / Na.
- `Fig. 6b`: 활성화 3 사이클 뒤 0.5 C 첫 방전 — 1 MPa 와 4 MPa 가 겹친다(≈450), 0 MPa 만 ≈360.
- `Fig. 6c`: 4 MPa 92.2 % · 1 MPa 70.54 % · 0 MPa 는 ≈60 사이클에서 끝난다.
- `Fig. 6d`: §3g 참조. 논문의 귀속 *"slight stress relaxation of the screw-tightened fixture"* — 4.3 → 3.55 MPa(✎ −17 %)는 "slight" 보다 크고, **50 µm Na 박의 크리프**(상온 T/T_m ≈0.80)도 같은 모양을 만든다. 논문은 둘을 가르지 않았다. 충전 시 압력 상승은 *"Li deposition on the Na current collector and the associated local volume expansion"* 으로 귀속한다(✎ 부호는 두께 수지와 맞는다 — §7g).
- `Fig. S13`: 명목 "1 MPa" 셀이 **≈1.2–1.4 MPa** 에서 돌았다 — 명목보다 평균 ≈30 % 높다. 1 MPa 결과(70.54 %)는 **≈1.3 MPa 평균**으로 읽어야 한다.
- `Fig. S14` / `Fig. 6e`: 초기 HF 절편이 0 → 1 MPa 에서 ≈50 → ≈20 Ω cm² 로 크게 줄고, 1 → 4 MPa 는 ≈20 → ≈18 로 거의 포화다. 10 사이클 뒤에는 셋 다 더 낮다(≈39 / ≈14 / ≈8.5). 등가회로 적합값은 미공개.
- `Fig. S15`: 4 → 1 MPa 전환 뒤 감쇠 기울기 ≈2배, CE ≈1 %p 하락. 본문 표현은 *"slight deterioration"*.

---

## 6. 메커니즘 종합 (논문의 논리 흐름 + 약한 고리)

```
[양극]  Li₂S + PI₃ ──(3D 스윙밀 1400 rpm, 유효 2 h)──▶ LiI(결정) + 티오인산염(PS₄³⁻/P₂S₇⁴⁻/P₂S₆⁴⁻, 비정질) + 환원 P
        ├─ 나노결정 Li₂S 가 비정질 껍질에 박힌다 (TEM · XPS S 2p)
        ├─ σ_ion ×3280 · σ_e ×3800 (Hebb–Wagner) ─▶ 활성화 과전압↓ · 이용률↑ (LSV / CV / GITT / EIS)
        └─ [AIMD] 231 원자 용융 유래 유리 @800 K: D_Li 2.36e-5 · P–P / P–S / Li–I 특징   ← "정성 보강"
[음극]  Na 집전체: Li 비고용(상도) + 연성(항복 0.19–0.28 MPa, 인용) ─▶ 저압에서 계면 접촉 유지
        ├─ 석출 과전압 10 vs 22 mV · 핵생성 딥 없음 · CE 99.857 % / 1000 cyc
        └─ ⚠ +0.33 V vs Li 에서 Na 자체가 산화 ─▶ 방전 컷오프 1.7 V 필수
[셀]    Li₂S 는 충전 때 수축 · Li 는 Na 위로 석출 ─▶ 압력 가역 진동(충전 때 상승) = "접촉 유지" 의 증거로 제시
        └─ 4 MPa 92.2 % / 300 · 1 MPa 70.54 % / 300 · 0 MPa 실패
```

**약한 고리 셋**: ① AIMD 에 대조군이 없어 "PI₃ 가 수송을 높인다" 를 시험하지 않는다 ② 용량의 출처(Li₂S vs SE vs LiI/티오인산염)가 갈리지 않았다 ③ 압력은 정간극 지그의 출력이라 "4 MPa / 1 MPa" 는 명목값이다.

---

## 7. 우리 계산과의 대조 ★★ (1저자 지정 중점)

### 7a. 판정 — "이 논문의 li2s 계산" 의 실체 + "nucleation DFT" 문장의 출처

- **계산은 Li₂S–PI₃ 벌크 AIMD 1건이다.** 정적 DFT 없음 · Na·Li 계면 계산 없음 · 핵생성 계산 없음.
- **"DFT and mesoscale calculations provide complementary insight regarding nucleation-growth" — 이 논문의 문장이 아니다.** 본문·SI 텍스트층 전체에 *mesoscale* · *complementary* · *nucleation-growth* 가 **0건**이다(2026-09-23 pymupdf 전문 검색, 줄바꿈 하이픈을 지운 뒤에도 0). 같은 세미나 0923-2·0923-3 의 본문·SI 에도 없다. 이 논문에서 Na 위 Li 핵생성에 관한 서술은 **전부 실험**(과전압 ≈10 vs ≈22 mV, 핵생성 딥 유무)이고, 해석은 ref 54(Wang et al., *Nat. Commun.* 11, 5201 (2020) — in situ plating)를 **인용**한 것이다. Cu 위 두 번째 반원(*"Li nucleation and growth processes on Cu"*)도 ref 14 인용이다.
  · 출처 후보(✎ 추정 — 원문을 litdb 에 갖고 있지 않아 문장 대조는 못 했다): 이 논문 참고문헌 중 **B. S. Vishnugopi 공저 4편**(P. P. Mukherjee 그룹 — "mesoscale" 을 쓰는 쪽) — ref 10 Sandoval 2025 *Nat. Mater.* 24, 673 · ref 14 Sandoval 2023 *Joule* 7, 2054 · ref 16 Park 2025 *Adv. Energy Mater.* 15, 2405129 · ref 55 Yoon 2025 *Science* 388, 1062. 저자 목록은 이 논문 참고문헌에서 확인했다.

### 7b. li2s 소셀 유리 트랙과의 대조 — ⚠ 외부 1저자 트랙: 참고·주의로만

> 트랙 = **li2s (소셀 유리)** · 1저자 = **외부** (사용자 아님). 아래는 **리뷰 입력용 관찰**이지 결정이 아니다. 우리 쪽 항목은 전부 `citable: false` 카드에서 왔고, 소셀 수치에는 영구 단서 *"120 원자 · L ≈ 14 Å · 감김 홉 2.33 · 담금질 10¹² K/s · 단일 시드"* 가 붙는다 (`db/properties/lpscl_smallcell_production_scope_2026_09_18.json` §4). 우리 쪽 칸은 **설계 사양**이지 결과값이 아니다.

| 항목 | Zhang 2026 (CP2K AIMD) | 우리 li2s 소셀 유리 (UMA) | 무엇이 다른가 |
|---|---|---|---|
| 계 | Li₁₃₈S₆₉P₆I₁₈ (231) — 반응물 조성 그대로(Li₂S : PI₃ = 92 : 8) | a-Li₄PS₄Cl × 12 = Li₄₈P₁₂S₄₈Cl₁₂ (120) | 조성·할로겐(I vs Cl)·크기가 다르다 |
| 셀 길이 | **미기재** (✎ ideal-mixing 가정 시 ≈16 Å — 우리 추정) | L = 13.98 Å 정육면체 | |
| 힘 | PBE-D3(BJ) DFT (GPW) | UMA uma-s-1p1 (omat, 분산 없음) — 120 원자에서 QE/PBE 대비 G1 통과 (`li2s_track_ladder_2026_09_18.json` L-3) | 힘 축이 다르다 |
| 용융 | 2000 K NVT **2 ps** | 1200 K **100 ps** | 그쪽이 50배 짧다 |
| 담금질 | **램프 없음** — 1500 K NPT 2.5 ps 뒤 800 K 로 즉시 | **10¹² K/s 선형 900 ps** → 300 K 50 ps (NPT, 원 선언 `lpscl_li2s_interphase_prereg_2026_09_11.json`) | 그쪽은 담금질 속도가 정의되지 않는다 |
| 부피 | 1500 K NPT 2.5 ps 끝 부피를 800 K NVT 가 물려받는다 | 담금질 전 구간 NPT | 그쪽 800 K 밀도는 1500 K 액체 밀도 — ✎ 낮을 가능성(→ D 과대 방향, 추론) |
| 측정 온도 | **800 K 하나** | **400 / 465 / 550 K** (1/T 등간격, Δ(1/T) 0.682×10⁻³ K⁻¹) | 그쪽은 아레니우스가 불가능하다 |
| 상한 온도의 근거 | 없음 | 120 원자 상자 감김 — 5 ps lag p90 이 **600 K 에서 무상관 한계 (d/2)² = 48.88 Å² 에 닿음 → 상한 550 K** (`lpscl_smallcell_quench_scan_2026_09_21.json`) | 우리 상한은 **우리 셀·우리 분석**의 성질이다 (아래 ⛔) |
| Tg | 논의 없음 | 10¹² K/s 담금질의 동역학적 정지 ≈400–450 K (진단, 비인용) | |
| 생산 길이 | 40 ps (dt 2 fs) | 400 ps (dt 2 fs · Langevin friction 0.02 · equilib 5 ps) | 10배 |
| D 적합 | "선형 영역" — 창 미기재 | **MSD 창 2–50 ps 고정 · 자유절편** | 그쪽 궤적(40 ps)은 우리 창 끝(50 ps)보다 짧다 |
| 시드 | 미기재 (하나로 보인다) | **구조(담금질) 시드 5** · 보고 = 중앙값 + IQR · **풀링 금지** | |
| 게이트 | 없음 | C1 MSD ≥3 Å² · C2 β 0.8–1.2 · 400 K 노화 검사 · 550 K 감김 검사 — 결과 전에 고정 | |
| 보고량 | D_Li(800 K) **절대값** | **N_pass/15 + Ea 시드 산포** — Ea·D 절대값은 보고량이 아니다 (`lpscl_smallcell_glass_md_estimand_2026_09_21.json`) | |
| 대조 계 | **없음** (PI₃ 없는 Li₂S 계산 없음) | 이 카드에는 없다 — Phase B 로 분리 | 둘 다 대조가 비어 있다. 차이는 **그쪽은 주장을 하고, 우리는 주장을 안 한다**는 것 |

**참고할 것 — 그 트랙 1저자에게 올릴 수 있는 관찰 넷**
1. **"우리 규율이 과한가?" 에 대한 외부 눈금** — 동료심사를 통과한 *Adv. Energy Mater.* 논문이 단일 온도·단일 궤적·40 ps·창 미기재 D 를 *"intrinsic Li⁺ migration capability"* 의 근거로 쓴다. 우리 카드가 금지한 형태(절대 D · 단일 시드 · 대조 없음) 그대로다. 우리 설계의 **상대적 위치**를 보여 주는 사례로 쓸 만하다 — 우리가 옳다는 증거는 아니다.
2. **"점프 담금질" 의 흔적이 음이온 MSD 에 보인다** — I·S MSD 가 800 K 첫 ≈15 ps 에 오르고 멈춘다(`Fig. 1b`). 과도구간이 **음이온 MSD 에서 어떻게 보이는지**의 진단 모양 한 점이다. ⚠ 우리 계는 램프로 담금질하므로 이 15 ps 라는 **길이**를 우리 equilib 5 ps 판단에 옮기면 안 된다 — 가져오는 것은 "음이온 MSD 의 초기 상승-평탄" 이라는 **점검 항목**뿐이다.
3. **P 개수 바닥** — 우리 생산 셀 선언이 *"상분리·조성 요동: 120 원자로는 표본이 안 된다 (Cl 12 · P 12)"* 라고 적었다. 그쪽은 **P 6 개**로 P₂S₆/P₂S₇/PS₄ 종분화를 말한다(✎ P–P 결합 ≈1 개). ⇒ 우리가 "국소 화학(PS₄ 보존율·배위수)" 은 말하고 "종분화 분율" 은 안 말하는 선이 **문헌 관행보다 보수적**이라는 확인이다.
4. **할로겐–Li 봉우리의 셀 크기 민감도** — 그쪽은 Li–I ≈2.8 Å 봉우리를 LiI 유사 배위로 읽는다. 우리는 G-B2 에서 **Li–Cl 첫 봉우리가 120 ↔ 400 원자 사이에 0.150 Å 벌어지는 것**을 실측했다(`lpscl_smallcell_gb2_result_2026_09_18.json`). ⇒ 할로겐–Li 봉우리 위치로 상을 동정할 때 **셀 크기 시험 없이 0.1 Å 급 해석을 하지 않는다**는 우리 쪽 근거에 사례 하나가 더해진다(그쪽 크기 시험 0).

**비교하면 안 되는 것**
- ⛔ 그쪽 D(800 K) 와 우리 어떤 D·Ea 도 한 표·한 문장에 두지 않는다 — 조성·할로겐·힘 계산·온도·통계가 전부 다르고, 1저자 인용정책(2026-09-18)이 우리 쪽도 **계 간 상대차**로만 쓰게 한다.
- ⛔ **우리 550 K 상한을 이 논문에 대한 비판으로 쓰지 않는다.** 상한은 *우리* 셀(L 13.98 Å)과 *우리* 분석(최소영상 변위, (d/2)² 한계)에서 나왔다. 그쪽 셀 길이는 미기재이고, MSD 가 60 Å² 까지 포화 없이 직선이라 **감싸지 않은(unwrapped) 좌표**로 계산했을 가능성이 크다. 옮길 수 있는 것은 **질문**뿐이다: *"40 ps 동안 Li RMS 변위(✎ ≈7.7 Å)가 상자 반폭(✎ ≈8 Å, 추정)에 닿는데 유한크기 점검을 했는가"*.
- ⛔ 그쪽 800 K 가 "Tg 위냐 아래냐" 를 우리 Tg(≈400–450 K, a-Li₄PS₄Cl · 10¹² K/s)로 판정하지 않는다 — 조성(Li₂S 92 %)이 전혀 달라 Tg 도 다르다. 그쪽 음이온 MSD 평탄화(15 ps 이후)는 **800 K 에서 골격이 거의 정지**했음을 시사할 뿐이다.

### 7c. MLIP-MD 결정계 규약과의 관계 — 같은 표 금지
- 우리 결정계(modelc · lpsocl) D 는 **UMA MLIP-MD · Langevin NVT · 2 fs · equilib 5 ps / prod 200 ps(일부 400 ps) · MSD 창 2–50 ps · 멀티시드 판정 · 절대값 인용 금지**(`our_dft_baseline.md`, CLAUDE.md §MLIP-MD). 레지스트리의 Ea 항목은 전부 `absolute_sigma` · `single_trajectory_CI` 같은 금지 표지를 달고 있다.
- 이 논문 D 는 **AIMD · 단일 T · 40 ps · 창 미기재 · 단일 궤적 · 비정질 Li₂S–PI₃** 로, 규약을 하나도 공유하지 않는다. ⇒ `comparison_vs_ours.md` §A 의 수치 표에 **넣지 않는다** — §J-44 방법 블록으로만 둔다.
- 방법 라벨 주의(`our_dft_baseline.md` 2026-07-27): *"둘 다 AIMD 라 직접 비교"* 식 문장 금지 — 우리 것은 AIMD 가 아니다.

### 7d. W_ad 리뷰 BW (B) 안 — CP2K 근거가 되나? (트랙 = 우리 DFT · 1저자 = 사용자)

> (B) = *"가우스 기저 DFT (CP2K GPW · PBE-D3 · DZVP/TZV2P-MOLOPT) — 진공에 비용을 안 내서 전체 계면 DFT 를 지키는 길"* (`kb/reviews/codex_BW_prompt_wad_validation_without_cluster_2026_09_23.md` §2(B)).
> **BW 회신은 이미 왔다**: *"CP2K 전환이 필수는 아닙니다"* · *"'진공에 비용을 안 낸다'는 수정해야 합니다 … GPW의 전하밀도 격자·FFT에는 셀 크기가 들어갑니다. GPU 지원도 연산별이므로 host RAM 부담이 사라지는 것은 아닙니다"* (`kb/reviews/codex_BW_reply_wad_validation_without_cluster_2026_09_23.md` Q1).

**판정: 이 논문은 (B) 의 규모·설정 근거가 되지 못한다.** 이유 넷:
1. **계산 자원이 한 줄도 없다** — 노드·코어·GPU·메모리·벽시간 미기재, 사사에도 계산센터가 없다. "231 원자 PBE-D3 AIMD 가 돌았다" 는 존재 증명일 뿐이고, **우리 제약(KISTI 종료 · 단일 노드 · 큰 계산은 GPU 한 장 48 GB)** 에서 되는지는 아무것도 말하지 않는다.
2. **벌크다 — 진공이 없다.** BW 회신이 고친 논점(GPW 밀도 격자·FFT 가 진공 포함 셀 부피를 따라간다)은 슬랩 + 진공에서 생기는데, 이 논문은 그 상황을 겪지 않는다. 우리 P1 ≈436 · P2 ≈820 원자 **슬랩 + 진공**과 규모를 견줄 수 없다.
3. **기저 수준이 미기재다** — "MOLOPT" 만 있고 DZVP/TZV2P · SR 여부가 없다. (B) 가 묻는 바로 그 선택에 답을 주지 않는다. **BSSE(counterpoise)** 는 벌크 AIMD 라 애초에 다루지 않았다 — W_ad 에서는 필수다.
4. **SCF 문턱 10⁻⁴–5×10⁻⁵ 는 고온 AIMD 용**이지 J m⁻² 급 **에너지 차**용 설정이 아니다. ✎ 0.10 J m⁻²(BV 합격선)는 200 Å² 계면에서 ≈1.25 eV 라 SCF 잡음보다는 크지만, 기저 불완전성·BSSE 는 그 크기에 들어올 수 있다 — 자체 수렴 시험 없이 설정을 옮기지 않는다.

**그래도 한 줄은 가져온다 — litdb 의 CP2K 선례 세 점이 컷오프·기저에서 서로 갈린다:**

| 출처 | 계 | 기저 · PP | CUTOFF / REL_CUTOFF | D3 | 비고 |
|---|---|---|---|---|---|
| **[Zhang26PI3]** (이 논문) | Li₂S–PI₃ 벌크 231 원자 AIMD | MOLOPT (수준 미기재) · GTH | **520 / 60 Ry** | **BJ** | k 미기재 |
| [Wang26uMLP] `wang2026_domain_oriented_universal_machine_learning_potential` | 액체 전해질 라벨 400–4000 원자 | **DZVP-MOLOPT-SR-GTH** · GTH | **900 Ry** (Li⁺ 계) · REL 미기재 | damping 미기재 | k 미기재 (Γ 추정) |
| [Liu24SbO] `liu2024_pband_center_sbo_dual_interface` | argyrodite AIMD 10 ps @300 K | **DZVP-MOLOPT-SR-GTH** · GTH · Γ | digest 에 기록 없음 | 없음 | dt 1 fs |

⇒ (B) 를 연다면 문헌 설정을 옮기는 게 아니라 CUTOFF(520 vs 900 Ry) · 기저(DZVP vs TZV2P) · BSSE 를 **우리 SE|SE 대조(V1)로 자체 수렴**시켜야 한다 — BW 회신의 *"CP2K도 자동 해법은 아닙니다"* 와 같은 방향이다. **BW 판정(A′ 경로)을 바꿀 새 정보는 이 논문에 없다.**

### 7e. ESW 축 — Li₂S 활성화 창과 Na 전위 (트랙 = ESW · 1저자 = 사용자)
- **축 ① (S²⁻-limited 분해 onset)**: 우리 comp1/modelc grand-potential 산화 onset **2.256 V vs Li⁺/Li** (LiS₄ 제외 GG set; 문헌 [Zhu15]·[Schw21] 은 2.01 V — 0.246 V 차는 원인 미확정, `our_dft_baseline.md`). 이 논문의 첫 충전은 **3.0 V 까지**, LSV 는 **≈3.65 V 까지** 가고, 양극 복합체의 **40 wt% 가 LPSCBr** 이다 ⇒ 활성화 전압 전 구간이 argyrodite 열역학 분해 onset **위**다(층① 기준). ⚠ LPSCBr(Br 포함)은 우리가 계산하지 않은 조성이다 — **"같은 계열 onset 의 위"** 까지만 말한다.
  · ⇒ `Fig. 5a` 의 **이론 초과 첫 충전(`figure-read` ≈1330 vs 1166)** 과 `Fig. S12` 의 **1530 · 1280** 에 SE 산화 몫이 섞였을 가능성을 논문이 배제하지 않았다. [Cronk26] 의 CE 129 %(LPSCl 이 용량에 기여, dQ/dV 로 분리)와 같은 현상 계열인데, 이 논문은 **분리를 시도하지 않았다**.
- **환원 쪽 — "Na 가 분해 구동력을 줄인다" 주장**: Na⁺/Na 는 ✎ +0.33 V vs Li⁺/Li. argyrodite 환원 한계는 ~1.7 V 급(문헌 [Zhu15] 1.71 · 우리 grand-potential **교환-0 가장자리 1.717 V** — 인용 시 규약 명시, `HZ-esw-reduction-limit-facet-convention`). ⇒ Na 전위(0.33 V)도 환원 한계보다 **≈1.4 V 아래**라 LPSCBr 은 Na 에 대해서도 **열역학적으로 환원된다**. 게다가 Li 가 석출된 뒤 SE 가 닿는 것은 **Li(0 V)** 다. "구동력 감소" 는 **크기 서술(0.33 V 만큼)** 이지 **창 안에 든다는 서술이 아니다** — 논문이 같은 쪽에서 *"narrow stability window that precludes direct Li pairing"* 이라고 쓴 것과도 모순이다.
- 평판 CV 경고(§B①, [Jang23ZnO] 등)와 같은 맥락: 이 논문의 CV(`Fig. S9`, −0.05–0.5 V)는 **집전체 산화**를 보는 창이지 SE 창을 재지 않는다.

### 7f. 전자구조 축 D — σ_e ×3800 과 환원 P
- 이 논문은 DOS·밴드갭을 계산하지 않았다 → **수치 대조 0**.
- 정성 연결 하나: 밀링 산물에 **환원 P(P′, XPS·Raman)** 와 **P–P 결합 단위(P₂S₆⁴⁻, NMR 주성분)** 가 있고 σ_e 가 ×3800 오른다. 우리 SEI gap 사다리(fixed-occ nscf, `comparison_vs_ours.md` §E)에서도 P 가 환원된 쪽(Li₃P)의 gap 이 가장 작다 — **"환원 P 종 = 전자 누설 후보"** 라는 방향은 같다. ⚠ 이 논문의 P′ 가 무엇인지(원소 P? P–P 사슬? Li₃P?) 동정되지 않았으므로 **방향 일치까지만** 말한다.

### 7g. DEM 트랙 — 적층압·in-situ 압력 (→ `comparison_vs_ours_DEM.md` §I-7)
- **압력 층위**: 제조압 250(SE)·400(양극)·75(Li)·25(Na) MPa ≠ **운전 적층압 0/1/4 MPa**. 우리 DEM "3종 압력 구분"(제조 ~300–490 · 운전 ~5–70 MPa)의 운전 쪽보다도 **한 자릿수 아래**다.
- **정간극 지그 = 압력이 출력**: 설정 ≈4.3 MPa → 휴지 중 ≈3.55 MPa(−17 %) · 운전 띠 ≈3.2–3.8 MPa · "1 MPa" 는 ≈1.2–1.4 MPa. 우리 DEM 박리·압밀은 **하중 제어**(P 고정)라 **경계조건 종류가 반대**다. 이 논문 수치를 "P 에서의 거동" 으로 쓸 때는 **명목값이 아니라 판독 띠**를 쓴다.
- **호흡 진폭**: 충전 때 +, 방전 때 −. ΔP ≈0.35–0.5 MPa(4 MPa 셀) · ≈0.15–0.18 MPa(≈1.3 MPa 셀) — 두 점 모두 ΔP/P ≈11–13 % (✎, `figure-read`). 부호는 ✎ 두께 수지와 맞는다: 충전당 Li 석출 ≈+3.5 µm(0.73 mAh cm⁻² = 1.45 mg cm⁻² × ≈500 mAh g⁻¹) vs 양극 Li₂S → S 수축 ≈−1.65 µm(몰부피 27.7 → 15.5 cm³ mol⁻¹) ⇒ 순 ≈+1.9 µm 팽창(우리 추정, 기공 흡수 무시). ⚠ ΔP 크기는 **지그 + 적층 컴플라이언스**가 정한다 — 재료 물성이 아니다. ⚠ 1 MPa 셀의 로딩은 미기재라 두 점의 ΔP/P 비교는 가설 수준이다.
- **접촉 포화**: 초기 HF 절편 ≈50(0 MPa) → ≈20(1 MPa) → ≈18 Ω cm²(4 MPa) — **1 MPa 이하에서 대부분 포화**한다. Na 항복강도(인용 0.19–0.28 MPa)의 수 배에서 포화한다는 그림과 맞는다. ⚠ HF 절편 = SE 벌크 + 복합양극 + 두 계면의 합이라 Na 계면 몫을 분리하지 못한다.
- **이완 귀속**: 논문은 휴지 중 압력 강하를 지그 이완으로 돌린다 — Na 박(50 µm) 크리프(상온 T/T_m ≈0.80)와 **분리되지 않았다**. MPM(소성·크리프 금속층) 쪽 질문으로 넘길 수 있다.
- DEM 이 **가져갈 것**: 압력 띠 · 호흡 진폭 · 포화 압력의 **실측 사양**(대조 표적이지 보정 표적이 아니다). **가져가지 말 것**: 명목 "1/4 MPa" 를 제어값처럼 쓰는 것, ΔP 를 재료 강성으로 읽는 것.

### 7h. 항목별 대조 요약

| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| 비정질 Li₂S 근방 상의 MD | CP2K AIMD 231 원자 · 800 K 1점 · 40 ps · 단일 | UMA 120 원자 유리 · 400/465/550 K · 400 ps · 구조 시드 5 (li2s, 외부 1저자) | **비교 불가** — 프로토콜 대조만 (§7b) |
| D 절대값 | 2.36×10⁻⁵ cm² s⁻¹ @800 K | 절대값 인용 금지 | ⛔ 같은 표 금지 |
| 종분화 (P₂S₆/P₂S₇/PS₄) | RDF 로 주장 (P 6 개) | 소셀은 "종분화 분율" 을 말하지 않음 (P 12 개도 부족하다고 선언) | 우리가 더 보수적 |
| CP2K 설정 | 520/60 Ry · MOLOPT(수준 미기재) · D3(BJ) | W_ad (B) 안 → BW 회신 A′ | 근거 안 됨 (§7d) |
| 산화 창 | 활성화 3.0–3.65 V (SE 40 wt% 포함) | onset 2.256 V (LPSCl, 축 ①) | 활성화 전압이 onset 위 — SE 기여 미분리 |
| 환원 / Na | "Na 가 분해 구동력을 줄인다" | 환원 한계 ~1.7 V 급 (교환-0 가장자리 1.717 V) | Na(+0.33 V)도 한계 한참 아래 — 크기 서술일 뿐 |
| 전자 누설 | σ_e ×3800, 환원 P | SEI gap 사다리 — 환원 P 쪽이 최소 | 방향만 같음 |
| 적층압 | 0/1/4 MPa (정간극, 실측 띠) | DEM 하중 제어 | 경계조건 반대 — 판독 띠로 대조 |

---

## 8. DFT/계산 방법 ★ (템플릿 §4 형식 요약)
- **code / version**: CP2K Quickstep (GPW) / 버전 n/a
- **functional + vdW**: PBE + D3(BJ)
- **pseudo / basis**: GTH / MOLOPT (수준 n/a)
- **k-points / ecut / supercell / nat**: k n/a · CUTOFF 520 Ry · REL_CUTOFF 60 Ry · 셀 치수·밀도 n/a · **nat 231** (Li₁₃₈S₆₉P₆I₁₈)
- **DFT+U**: 없음
- **AIMD**: NVT 2000 K 2 ps → NPT 1500 K 2.5 ps (1 bar) → NVT 800 K 40 ps · dt 2 fs(③) · thermostat/barostat n/a · 시드 n/a
- **MLIP**: 없음
- **무질서 처리**: 용융 유래 배치 1개(*"representative reconstructed framework"*) — 초기구조 생성법 n/a
- **특이사항**: SCF 10⁻⁴–5×10⁻⁵ · Fermi–Dirac 스미어링 · 800 K 부피 = 1500 K NPT 끝 부피 · 본문은 "melt-quench" 라 부르지만 담금질 램프가 없다 · `Fig. 1d,e` 의 "different thermal protocols" 미설명
- **Post-processing**: MSD(Einstein, "선형 영역") → D · 부분 RDF(P–S, P–P, Li–I) · 스냅샷(P/S/I 만). 도구 · 시간원점 평균 · 적합 창 n/a. Bader/COHP/DOS/NEB/ELF 없음.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 셀 구성 모식도 — Li₂S–PI₃ + LiI + LPSCBr/CNT 양극 / LPSCBr / Na 집전체 · 확대원(비정질 티오인산염 속 나노 Li₂S) · 석출·탈리 때 Na 변형 | 발표용 개념도. "Key features" 3개는 **주장 목록**이지 데이터가 아님 |
| 1b | AIMD MSD @800 K (Li·I·S·P), 0–40 ps · Li `figure-read ≈`60 Å² · I ≈13 · S ≈10 · P ≈5 · I/S 는 15 ps 이후 평탄 | ★ **점프 담금질 과도구간이 음이온 MSD 에 보이는 모양** (li2s 트랙 점검 항목, §7b-2). D 값 자체는 ⛔ 비교 금지 |
| 1c | 부분 RDF P–S(≈2.1 Å, g ≈14) · P–P(≈2.3 Å, g ≈19) · Li–I(≈2.8 Å, 넓음) | ✎ P 6 개 → P–P ≈1 쌍. **작은 셀 종분화의 반면교사** (§7b-3) |
| 1d,e | 800 K "평형" 스냅샷 두 장 (P·S·I, Li 미표시), "different thermal protocols" | 프로토콜 미기재 — 인용 금지 |
| 2a | XRD 0–10 % — LiI 출현, Li₂S 선 넓어짐·이동 없음 | 고용체 아님 → "Li₂S 격자 도핑" 서사와 구별 |
| 2b | Rietveld 8 %: Li₂S 93.86 / LiI 6.14 %, Rwp 2.08 % | 배경 지배 Rwp — 적합 품질 근거로 약함 |
| 2c | ⁷Li (2.42 / ≈0 / −4.56 ppm) · ³¹P (PS₄³⁻ ≈84 · P₂S₇⁴⁻ ≈91 · P₂S₆⁴⁻ ≈107 ppm) | P₂S₆⁴⁻ 가 PS₄³⁻ 만큼 크다 = 환원성 밀링 산물의 지문. 본문 수치와 0.03–0.05 ppm 어긋남 |
| 2d,e | XPS P 2p(PS₄³⁻ · P₂Sₓ · P′) · S 2p(PS₄³⁻ · P₂Sₓ · **Li₂S 거의 없음**) | **표면 = 티오인산염 껍질**의 증거로 쓸 수 있음(논문은 말하지 않음). 우리 XPS anchor(`db/properties/xps_reference_sei.csv`)와 BE 대조 후보 |
| 2f | Raman 8 % vs Li₂S | 380 cm⁻¹ P₂S₆⁴⁻ 배정이 Li₂S ≈372 와 겹침 — 배정 주의 |
| 2g–i | TEM(나노결정 + 비정질) · SAED(Li₂S + LiI 링) · HRTEM Li₂S(200) 0.28 nm | 나노결정은 수 nm (`figure-read`) — **AIMD 셀에 없는 성분** |
| 3a | σ_ion 막대 1×10⁻⁸ → 7.3×10⁻⁵ S cm⁻¹ | ✎ 재계산 정합(8·10 %) · 6 % 는 `Fig. S5b` 라벨 오기 · 1×10⁻⁸ 은 측정 미제시 |
| 3b | LSV: 봉우리 ≈3.06 → ≈2.84 V, 개시는 둘 다 ≈2.45 V | **활성화 전압이 argyrodite onset(우리 2.256 V, 축 ①) 위** — SE 기여 미분리 (§7e) |
| 3c | CV 1.7–3.0 V: 8 % 산화 ≈2.45 / ≈2.82 V, 환원 ≈1.97 V | — |
| 3d–f | SOC/DOD 별 EIS + DRT, 8 % 가 전 구간 낮음 | ⚠ DRT 최대 봉우리 τ ≈10–50 s 가 측정 하한(0.2 Hz ⇔ τ 0.8 s) 밖 |
| 4a,b | Li 석출·탈리: Na 10 mV vs Cu 22 mV · Cu 핵생성 딥 ≈30 mV · CE 85.57 vs 76.49 % | "핵생성 장벽이 작다" 의 **실험** 근거 — 계산 아님 (§7a) |
| 4c,d | Li–Cu / Li–Na Nyquist, 3 사이클 | 강체 Cu 접촉 불량의 크기(≳700 Ω cm²) |
| 4e,f | Na CE 99.857 % / 1000 사이클 · Cu 연단락·단락 | — |
| 4g,h | 단면 SEM + EDS(Na·S·Br) — Li 층 ≈5 µm (`figure-read`) | ⚠ Li 는 EDS 로 안 보인다 — "균일 Li 분포" 주장의 근거가 아님 |
| 5a | 첫 사이클 0.05 C, X = 0–10 % — 8 % 충전 ≈1330 > 이론 1166 | ★ **이론 초과 충전** — SE·LiI·티오인산염 기여 미분리 (§7e, §10-⑧) |
| 5b,c | 율속 — 복귀 0.05 C 가 계속 오름 | 추가 활성화 / 부반응 용량 신호 |
| 5d,e | 0.5 C 200 사이클 "≈100 %" — 실제 ≈505 → ≈590 → ≈565 | retention 한 숫자가 상승-하강을 접음 |
| 5f | 2.52 mg cm⁻² · 0.2 C · 400 사이클 89.72 % | 25 ± 3 °C 비항온 |
| 5g | 문헌 기포 차트 (색 = 압력 · 크기 = 온도) | 조건 제각각 — 순위 인용 금지 |
| 6a | 정간극 볼트 지그 + 하중센서 | ★ DEM: 압력 = 출력 (§7g) |
| 6b | 활성화 후 첫 방전: 1 ≈ 4 MPa > 0 MPa | 1 MPa 이상에서 포화 |
| 6c | 300 사이클: 4 MPa 92.2 % · 1 MPa 70.54 % · 0 MPa ≈60 사이클 중단 | "1 MPa" 는 실측 ≈1.3 MPa (`Fig. S13`) |
| 6d | in-situ 압력 4 MPa: 4.3 → 3.55 (휴지) → 띠 3.4–3.8(초기) / 3.2–3.7(≈400 h), 충전 때 상승 | ★ DEM 대조 사양: 호흡 ΔP ≈0.35–0.5 MPa · 휴지 이완 −17 % |
| 6e | 10 사이클 뒤 Nyquist 0/1/4 MPa + 등가회로 | 적합값 미공개 — HF 절편만 `figure-read` |
| S5 | Hebb–Wagner 이온: 계단 바이어스 · 전류 · σ, L 0.063 cm | ✎ 재계산 레시피. 6 % 라벨 오기 |
| S6 | Hebb–Wagner 전자: Li₂S 2.29×10⁻¹¹ · 8 % 8.7×10⁻⁸ S cm⁻¹ | 두 측정 다 비옴 — 자릿수 표지로만 |
| S7 | GITT Li₂S vs 8 % | 본문 미언급 · D 미산출 |
| S8 | Li–Na 이원 상도 (Landolt-Börnstein) | ✎ 공정 ≈360 K — 90 °C 시험(`Fig. S12`) 해석의 열쇠 |
| S9 | CV Li–Li / Li–Na / Li–Cu, Li–Na ≈0.37 V 산화 봉우리 | ✎ = Na⁺/Na (+0.33 V vs Li) — Na 자체 산화 |
| S11 | Li₂S 양극 1.4 V 방전: ≈265 mAh g⁻¹ 계단 + dQ/dV ≈1.6 V | 1.7 V 컷오프 = Li 재고 소진 지점 |
| S12 | 90 °C · 1 C · 2.81 mg cm⁻²: 1530 · 1280 → 828.87 mAh g⁻¹ (71.31 %) | 이론 초과 + 공정점 위 — 기전이 다를 수 있음 |
| S13 | in-situ 압력 "1 MPa": 실측 ≈1.22–1.40 MPa | 명목 ≠ 실측 |
| S14 | 초기 Nyquist 0/1/4 MPa: HF ≈50 / ≈20 / ≈18 Ω cm² | 1 MPa 이하 포화 (§7g) |
| S15 | 4 → 1 MPa 전환: 감쇠 기울기 ≈2배 | 셀-대-셀 산포(§10-⑰)와 같이 읽기 |
| Table S1 | Rietveld: Li₂S 93.86 · LiI 6.14 · 비정질 ~62.31 % | 정성값 (논문 자인) |
| Table S2 | 무음극 ASSLSB 문헌 7건 + 이 연구 3조건 | ⚠ 별도 크롭 없음(`tab_S1.png` 에 본문 대부분 포함) · 조건 제각각 |

---

## 10. 비판 — 이 논문의 약한 곳 ★

**계산부**

① **대조 계산이 없다.** PI₃ 없는 Li₂S(결정이든 같은 프로토콜의 유리든)를 같은 방법으로 돌리지 않았다. 그래서 *"PI₃ incorporation promotes … enhanced Li⁺ transport"* 를 AIMD 가 시험하지 않는다 — 2.36×10⁻⁵ 는 비교 대상이 없는 숫자다.

② **모델이 실험 대상을 표현하지 않는다.** 실험은 결정상의 94 % 가 Li₂S 인 "나노결정 Li₂S + 비정질 매트릭스" 복합체인데, AIMD 셀은 반응물 조성(92 : 8)의 **균질한 용융 유래 유리**다. 나노결정 Li₂S 도 없고, 실제 비정질 매트릭스의 조성(P·I 가 훨씬 많아야 한다)도 아니다. 논문의 단서(*"does not fully replicate"*)보다 간극이 크다.

③ **프로토콜 서술이 서로 다르다.** 본문은 "melt-quench", SI 는 "melt–densify–equilibrate", 실제로는 **담금질 램프가 없다**(1500 → 800 K 즉시). `Fig. 1d,e` 의 *"different thermal protocols"* 는 Methods 에 없다.

④ **800 K 밀도가 1500 K 에서 왔다.** 2.5 ps NPT(부피 수렴에는 짧다) 끝 부피로 800 K NVT 를 돌렸고, 밀도를 보고하지 않았다. ✎ 방향상 저밀도 → D 과대 가능(추론).

⑤ **통계와 창.** 단일 온도, 단일 궤적(시드 미기재), 40 ps, 적합 창 미기재, 처음 ≈15 ps 의 음이온 과도구간이 적합에 섞였을 수 있다(`Fig. 1b`). 오차막대 없음.

⑥ **작은 셀 종분화.** P 6 개로 P₂S₆⁴⁻/P₂S₇⁴⁻/PS₄³⁻ 를 말한다(✎ P–P ≈1 쌍). 셀 크기 시험이 없고, 3.7–4.5 Å P–S 둔덕은 종 특이적이지 않다.

⑦ **재현 정보 결손.** 기저 수준 · k 점 · 셀 치수·밀도 · 초기구조 · thermostat/barostat · ①②단계 스텝 · 계산 자원이 전부 미기재다. 데이터는 "upon request".

**실험부**

⑧ **이론 초과 첫 충전을 논하지 않는다** (`Fig. 5a` ≈1330, `Fig. S12` 1530 · 1280 vs 1166). 초과분은 Li₂S 가 아닌 곳(SE 40 wt% · LiI · 티오인산염 · 환원 P · 부반응)에서 왔다. "8 % 가 Li₂S 활성화에 가장 효과적" 이라는 결론의 **용량 분모가 섞여 있다**. 정규화 기준(원료 Li₂S? Li₂S–PI₃?)도 미기재다 — ✎ PI₃ 8 mol% = 43.8 wt%.

⑨ **"electronic conductivity … increases slightly" 는 그림과 반대다.** `Fig. S6d` 는 ×3800 이다. 두 측정 모두 옴 거동도 아니다(`Fig. S6b` 는 전류가 바이어스에 무관, `Fig. S6c` 는 초선형).

⑩ **σ_ion 표기 불일치 + 기준 미측정.** 6 % 가 `Fig. 3a` 9.36×10⁻⁶ vs `Fig. S5b` 2.59×10⁻⁵ (✎ 재계산 8.5×10⁻⁶ → S5b 오기). 원료 Li₂S 1×10⁻⁸ 은 `Fig. S5` 에 측정이 없다(서론 문헌값과 같다) — "단조 증가" 의 출발점이 측정인지 인용인지 알 수 없다.

⑪ **DRT 봉우리가 측정창 밖에 있다.** 최대 봉우리 τ ≈10–50 s ⇔ ✎ 3–16 mHz 로, SI 가 적은 EIS 하한 0.2 Hz(τ ≈0.8 s) 밖이다. 그 봉우리는 저주파 꼬리의 외삽이거나, SI 의 주파수 범위 서술이 이 측정에는 틀렸다.

⑫ **EDS 로 Li 를 봤다고 쓴다.** `Fig. 4g` 맵은 Na · S · Br 뿐이다.

⑬ **Na 산화 봉우리의 정체를 흐린다.** ≈0.37 V(✎ Na⁺/Na +0.33 V)는 Na 금속 산화로 설명되는데 *"Na or Na-derived interphase species … potential instability"* 로 적었다. 무음극 셀은 매 방전 끝에 이 경계에 닿는다(`Fig. S11`) — 1.7 V 컷오프가 **유일한 방어선**이고, 과방전·셀 불균일 때 집전체가 소모될 위험이 논의되지 않았다.

⑭ **"Na 가 SE 분해 구동력을 줄인다" 는 크기 서술이지 창 서술이 아니다.** Na(+0.33 V)도 argyrodite 환원 한계(~1.7 V 급)보다 한참 아래이고, 운전 중 SE 는 석출된 Li(0 V)와 닿는다. 논문 스스로 *"narrow stability window that precludes direct Li pairing"* 이라고 쓴 것과 같은 문단에서 모순된다.

⑮ **90 °C 시험이 공정점 위다.** 자기 `Fig. S8` 기준 Li–Na 공정 ✎ ≈360 K(≈87 °C) · Na T/T_m ≈0.98. "변형 가능한 고체 Na" 기전의 증거로 쓸 수 없다. *"highly reversible"* 은 62 사이클 71.31 % 와 맞지 않는다.

⑯ **압력은 명목값이다.** 정간극 지그라 4 MPa 셀은 ≈3.2–3.8, "1 MPa" 셀은 ≈1.2–1.4 MPa 에서 돌았다. 본문 "3.4–3.8 MPa" 는 초기 띠다(≈400 h 에는 ≈3.2–3.7). 휴지 중 −17 % 강하를 지그 탓으로 돌리지만 Na 크리프와 분리하지 않았다.

⑰ **n = 1 과 셀-대-셀 산포.** 같은 4 MPa · 0.5 C 조건에서 `Fig. 5e` 셀은 첫 70 사이클에 ≈+17 % 오르고 `Fig. S15` 셀은 10 사이클에 ≈−7 % 내려간다(`figure-read`). 반복 셀·오차막대가 없어 조건 간 차이(예: 4 vs 1 MPa)의 유의성을 말할 수 없다.

⑱ **자잘한 불일치.** NMR 2.39 / −4.51 ppm(본문) vs 2.42 / −4.56 ppm(그림) · 89.71 %(초록·본문) vs 89.72 %(`Fig. 5f` · `Table S2`) · LSV "onset 이동" 은 실제로 봉우리 이동 · Raman 380 cm⁻¹ 배정이 Li₂S ≈372 와 겹침 · Rwp 2.08 % 는 배경 지배 패턴 · GITT(`Fig. S7`) 본문 미언급 · 축 오타("Capcaity", "nmber", "Cvcle") · SI 식 σ 단위 "S cm⁻²".

⑲ **벤치마크가 같은 조건 비교가 아니다.** `Table S2` 의 문헌은 2–30 MPa · RT–55 °C · 30–250 사이클이다. *"rare combination"* 주장은 조건을 맞추지 않고 나온다.

---

## 11. 우리 원장 매핑 (요약표)

| 항목 | Zhang 2026 (소환값) | 우리 원장 | 판정 |
|---|---|---|---|
| AIMD D_Li | 2.36×10⁻⁵ cm² s⁻¹ @800 K (단일) | li2s 소셀: 보고량 = N_pass/15 + Ea 산포 (절대값 비보고) — `db/properties/lpscl_smallcell_glass_md_estimand_2026_09_21.json` | ⛔ 비교 불가 |
| 담금질 | 램프 없음 (1500 → 800 K) | 10¹² K/s · NPT — `db/properties/lpscl_li2s_interphase_prereg_2026_09_11.json` | 프로토콜 대조만 |
| 온도 창 | 800 K | 400/465/550 K (550 K = 120 원자 감김 상한) — `db/properties/lpscl_smallcell_quench_scan_2026_09_21.json` | 상한은 우리 셀의 성질 |
| 종분화 표본 | P 6 개 | "P 12 개도 부족" 선언 — `db/properties/lpscl_smallcell_production_scope_2026_09_18.json` §3 | 우리가 더 보수적 |
| CP2K 설정 | 520/60 Ry · MOLOPT · D3(BJ) | W_ad BW 회신: CP2K 필수 아님(A′) — `kb/reviews/codex_BW_reply_wad_validation_without_cluster_2026_09_23.md` | 새 정보 없음 |
| 산화 창 | 활성화 3.0–3.65 V | onset 2.256 V (LPSCl, 축 ①) — `litdb/our_dft_baseline.md` | onset 위에서 활성화 |
| 환원 | Na +0.33 V vs Li | 환원 한계 교환-0 가장자리 1.717 V — `db/properties/citation_hazards.json` `HZ-esw-reduction-limit-facet-convention` | Na 도 한계 아래 |
| σ_e | ×3800 | SEI gap 사다리 (`comparison_vs_ours.md` §E) | 방향만 |

---

## 12. 적용 인사이트 ★

1. **"li2s 관련 DFT 가 많았다" 의 실체는 AIMD 1건이다.** 정적 DFT·계면·핵생성 계산은 이 논문에 없다. 가져올 것은 수치가 아니라 **방법 대조**다.
2. **li2s 소셀 트랙에 주는 외부 관찰 넷**(외부 1저자 판단용): ① 동료심사 논문의 D 보고 관행 대비 우리 설계의 위치 ② 점프 담금질 뒤 음이온 MSD 의 상승-평탄 모양(점검 항목) ③ "P 6 개로 종분화" — 우리 선언(P 12 개도 부족)이 더 보수적 ④ 할로겐–Li 봉우리의 크기 민감도(우리 G-B2 의 0.150 Å) 앞에서 그쪽은 크기 시험 0.
3. **W_ad (B) 는 이 논문으로 살아나지 않는다.** 자원 · 기저 수준 · 진공이 전부 비어 있다. litdb 의 CP2K 설정은 520 vs 900 Ry 로 갈리므로, (B) 를 열면 **자체 수렴**이 먼저다. BW 회신(A′) 유지.
4. **ESW 축의 새 사례** — Li₂S 활성화 전압(3.0–3.65 V)이 argyrodite onset 위이고, 이론 초과 충전이 두 그림(`Fig. 5a`, `Fig. S12`)에 있다. [Cronk26] 처럼 **SE 용량 기여를 dQ/dV 로 분리하지 않은 Li–S 논문은 "Li₂S 이용률" 을 과대 보고할 수 있다**는 경고 문장으로 쓸 수 있다.
5. **Na 집전체의 전기화학적 한계를 우리 산수로 정리했다** — +0.33 V vs Li 에서 Na 자체가 산화되고, 무음극 셀은 매 방전 끝이 그 경계다. "저압 안정" 은 기계 축이고, 전기화학 창은 1.7 V 컷오프에 매달려 있다.
6. **DEM** — 저압 운전의 실측 사양(띠 · 호흡 · 포화)을 대조 표적으로 등록한다. 단 **정간극 지그의 출력**이라는 경계조건 차이를 같이 적는다(`comparison_vs_ours_DEM.md` §I-7).

---

## 13. 인용 가능 문장 (영문 초안)

- "Zhang et al. report a single 800 K AIMD trajectory (CP2K, PBE-D3(BJ), 231 atoms, 40 ps) for a melt-derived Li₂S–PI₃ (8 mol%) glass, giving D_Li = 2.36 × 10⁻⁵ cm² s⁻¹; no PI₃-free control, temperature series or replicate trajectory is reported, so the value indicates Li mobility in that model glass but does not isolate the effect of PI₃."
- "In anode-free cells with a sodium current collector, the anode potential rises from Li plating to Na⁺/Na (≈ +0.33 V vs Li⁺/Li) once the plated Li is exhausted; the 1.7 V discharge cutoff used by Zhang et al. coincides with this step (their Fig. S11) and therefore protects the collector rather than being an optional setting."
- "Because the first-charge capacities of Li₂S–PI₃ cathodes exceed the theoretical capacity of Li₂S (≈1330 vs 1166 mAh g⁻¹, read from Fig. 5a of Zhang et al.) and 40 wt% of the composite is argyrodite charged above its thermodynamic oxidation onset, part of the reported capacity cannot be attributed to Li₂S without an explicit deconvolution."
- ⚠ (DEM, 조건부) "Stack pressures in screw-tightened (constant-gap) fixtures are outputs rather than controls: a nominal 4 MPa cell relaxed to ≈3.55 MPa at rest and cycled within ≈3.2–3.8 MPa, and a nominal 1 MPa cell within ≈1.2–1.4 MPa (read from Fig. 6d and Fig. S13 of Zhang et al.)."

---

## 14. 주의 / 한계 (인용 규율)

- ⛔ D_Li(800 K) 2.36×10⁻⁵ 를 우리 D·Ea 옆에 두지 않는다 (계 · 힘 · 온도 · 통계가 다 다르고, 1저자 인용정책도 막는다).
- ⛔ "AIMD 가 PI₃ 의 수송 향상을 보였다" 로 인용하지 않는다 — 대조 계산이 없다.
- ⛔ RDF 종분화(P₂S₆⁴⁻ 등)를 AIMD 근거로 인용하지 않는다 — P 6 개. 실험(³¹P NMR · Raman · XPS)으로만 인용한다.
- ⛔ 비용량(971 mAh g⁻¹ 등)을 "Li₂S 이용률" 로 인용하지 않는다 — 정규화 기준 미기재 + 이론 초과 충전.
- ⛔ σ_e 의 "slight increase" 를 옮기지 않는다 — ×3800.
- ⛔ 6 % σ_ion 은 `Fig. 3a` 의 9.36×10⁻⁶ 을 쓴다 (`Fig. S5b` 2.59×10⁻⁵ 는 오기).
- ⛔ "1 MPa" 결과는 ≈1.3 MPa(실측 띠 1.2–1.4)로, "4 MPa" 결과는 3.2–3.8 MPa 띠로 쓴다.
- ⛔ 90 °C 결과를 고체 Na 변형 기전의 증거로 쓰지 않는다 — Li–Na 공정점 위다.
- ⚠ 이 논문의 CP2K 설정(520/60 Ry · MOLOPT)을 W_ad 설정 근거로 쓰지 않는다 — 벌크 · 자원 미기재 · 기저 수준 미기재.
- ⚠ li2s 트랙 관련 서술은 **외부 1저자의 판단 대상**이다 — 여기 적은 것은 관찰이다.
- ⚠ `figure-read ≈` 값은 판독값(오차 수 %)이다 — 본문 인쇄값과 섞지 않는다.

---

## 15. 기법 용어 미니사전

- **CP2K / Quickstep / GPW**: 파동함수는 원자 중심 가우스 기저로, 전자밀도는 평면파 격자로 표현하는 혼합 방식. 파동함수 기저 수는 원자 수를 따라가고 진공과 무관하지만, **밀도 격자(FFT)는 셀 부피를 따라간다** — 그래서 슬랩 + 진공이 "공짜" 가 아니다(BW 회신 요지).
- **CUTOFF / REL_CUTOFF**: GPW 밀도 격자의 해상도. CUTOFF 는 가장 촘촘한 격자의 평면파 컷오프(Ry), REL_CUTOFF 는 가우스 함수를 어느 격자 단계에 올릴지 정하는 기준. 둘 다 수렴 시험 대상이다.
- **MOLOPT (DZVP / TZV2P, -SR)**: CP2K 표준 가우스 기저 계열. DZVP = 이중 제타 + 분극, TZV2P = 삼중 제타 + 분극 2개, SR = short-range(응축상 수치 안정용). 수준을 안 쓰면 재현할 수 없다.
- **GTH 의사퍼텐셜**: Goedecker–Teter–Hutter 노름보존 의사퍼텐셜. q 숫자가 원자가 전자 수다(Li q3 = 1s 포함).
- **D3(BJ)**: Grimme 분산 보정 + Becke–Johnson 감쇠. 짧은 거리에서 0 이 아니라 유한값으로 수렴한다.
- **melt–quench vs melt–densify–equilibrate**: 전자는 녹인 뒤 정해진 속도(K/s)로 식힌다 — 속도가 유리 구조를 정한다. 이 논문은 식히는 램프 없이 1500 K → 800 K 로 **바로 옮겼다**(속도가 정의되지 않는다).
- **Einstein 관계 / MSD**: D = (1/6)·d⟨Δr²⟩/dt. 탄도(ballistic) 초반과 통계가 나쁜 후반을 빼고 "확산 영역"(log MSD–log t 기울기 β ≈1)에서 기울기를 잡는다. 우리 규약은 창 2–50 ps 고정 + β 게이트.
- **무상관 한계 (d/2)²**: 주기 상자에서 최소영상 변위로 MSD 를 재면 상자 반폭의 제곱 근처에서 포화한다. 우리 120 원자 셀은 48.88 Å².
- **부분 RDF g_αβ(r)**: α 원자 주위 거리 r 에서 β 원자를 찾을 상대 확률. 원자 수가 적으면(P 6 개) 봉우리 높이가 한두 쌍으로 정해진다.
- **Hebb–Wagner 분극**: 한 종류 전하만 통과시키는 전극으로 막고 DC 전류를 잰다. 전자 차단(LPSCBr + Li) → 이온 전도도, 이온 차단(MWCNT) → 전자 전도도. 정상상태 · 옴 거동이 전제다.
- **DRT (distribution of relaxation times)**: 임피던스를 이완시간 τ 의 분포로 푼다. 측정 주파수 범위 밖의 τ 에 나오는 봉우리는 외삽 산물이다.
- **GITT**: 짧은 전류 펄스 + 긴 휴지를 반복. 휴지 뒤 전압 = 준평형 전위, 펄스 스파이크 = 과전압.
- **Rietveld Rwp**: 가중 잔차. 배경이 큰 패턴은 배경만 잘 맞춰도 Rwp 가 작아진다 — 상 정량 품질의 지표로는 약하다.
- **무음극(anode-free)**: 음극 활물질 없이 집전체만 두고, 첫 충전 때 양극의 Li 가 집전체 위에 석출돼 음극이 된다. Li 여분이 없어 손실이 곧 용량 손실이다.
- **정간극(constant-gap) 지그**: 볼트로 간격을 고정한다 — 셀 두께가 변하면 압력이 변한다(압력 = 출력). 하중 제어(스프링·공압)와 경계조건이 반대다.
- **항복강도 / 크리프 / 상동온도 T/T_m**: 금속이 소성 변형을 시작하는 응력 / 일정 응력에서 시간에 따라 쌓이는 변형 / 절대온도 ÷ 녹는점. Na 는 상온에서 T/T_m ≈0.80 이라 크리프가 크다.
- **공정(eutectic)**: 두 성분 합금이 가장 낮은 온도에서 녹는 조성·온도. Li–Na 는 Na 쪽 ≈360 K (`Fig. S8` 판독).
