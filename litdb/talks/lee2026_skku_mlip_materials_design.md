# 기계학습 포텐셜 기반 소재 물성 해석 및 설계 (MLIP-Based Materials Analysis and Design) — 이상욱 (성균관대)

> slug `lee2026_skku_mlip_materials_design` · type `talk` · 발표 2026-08-21 (2026년도 전지기술 심포지엄, 한국전기화학회, 기술세션 3-3) ·
> 발표자 **Sang Uck Lee**, School of Chemical Engineering, Sungkyunkwan University (**CMS Lab** — Computational Materials Science) ·
> PDF 18 pp (자료집 pp. 279–296), 슬라이드 31장 · digested 2026-07-28 · status ✅ (덱) · ✅ **구술 STT 판독 2026-08-26 → §99**
>
> 🔁 **덱 실물 독립 재판독 완료 2026-08-03** — 같은 PDF가 inbox에 재투입(`litdb/inbox/이상욱 교수님.pdf`,
> **사용자 분류 `(미분류)`**)되어 **전 18 pp를 이미지로 다시 판독**(PDF는 텍스트 레이어 0 = 전 페이지 스캔;
> 수치 영역은 embedded raster 원해상도까지 확대). 결과 **교정 14건(+캐비앳 2건) · 신규 8건 ·
> 미해결질문 2건(Q1·Q3) 종결 · 우리 db 전역에 퍼진 오기 1건("덱이 17,233 Li-P-S-O라고 적었다") 철회**.
> 전체 목록과 근거는 **§15**. 아래 본문은 재판독 값으로 이미 갱신돼 있다.
>
> ⚠ **덱 인용 규율**: `litdb/talks/README.md` 참조. 이 그룹의 **정본은 `papers/kim2024_mtp_argyrodite_disorder_gb.md`**
> (Nano Energy 2024, 124, 109436 — 덱 슬라이드 13 "Dynamic properties" 가 바로 그 논문). 덱과 논문이 충돌하면 논문이 이긴다.
> ⚠ 슬라이드 번호 표기가 `/31`, `/50`, `/24` 로 섞여 있다(마스터 덱 잔재). 아래는 **PDF 페이지 + 덱 표기** 병기.

---

## 1. 한 줄 요약

**"DFT는 작고 MD는 부정확하다 — MLIP가 그 사이를 메워 ASSB의 계면·표면 반응을 실제 크기(6,000+ 원자)와
실제 시간(50 ns)에서 본다"**가 전체 서사이고, argyrodite에 대해 **음극계면 반응(Li|LPSCl, MTP)·표면
가수분해(SevenNet)·벌크 무질서 전도(MTP)·양극 코팅 스크리닝(SevenNet)·신물질 CSP(MTP)** 다섯 갈래로
전개한다. 우리 캠페인과 **같은 물질·같은 도구(MLIP)·다른 축**이라 경쟁이자 벤치마크다.

---

## 2. 덱 구조 (PDF 페이지 → 슬라이드)

| PDF p. | 슬라이드 | 내용 |
|---|---|---|
| 1 | 표지 | 자료집 p.279 |
| 3 | 1–2 | 타이틀 / **과학방법 5세대** |
| 4 | 3–4 | Scale & Scientific Method / DFT 기반 LIB 연구 |
| 5 | 5–6 | **DB 기반 스크리닝 깔때기** / **GNoME** |
| 6 | 7–8 | ML vs MLIP / **MLIP PES softening–fine-tuning** |
| 7 | 9–10 | Why MLIP (DFT vs MD) / **시뮬–실험 4대 괴리** |
| 8 | 11–12 | Bridging the gap / **ASSB 과제 지도** |
| 9 | 13–14 | **ASSB MLIP 연구 5갈래** / **MLIP 훈련셋 6단계** |
| 10 | 15–16 | [섹션] Anode Interface RXN / **MTP 훈련(passive+active)** |
| 11 | 17–18 | **MTP 정확도(5,400 데이터셋)** / **계면반응 MD** |
| 12 | 19–20 | **시뮬 vs 실험 검증** / [섹션] Surface RXN |
| 13 | 21–22 | **반응좌표 기반 훈련셋** / uMLIP 정확도 |
| 14 | 23–24 | **LPSCl vs H₃O⁺/OH⁻** / **Sn 치환 억제** |
| 15 | 25–26 | [섹션] CSP / Metastable Materials |
| 16 | 27–28 | **uMLIP-CSP 플랫폼** / **Li–[Si–Ge]–S CSP** |
| 17 | 29–30 | **metastable 3 기술자** / LFP SOC(PyBaMM+ML) |
| 18 | 31 | 총괄 |

---

## 3. 서사 축 — "왜 MLIP인가" (p.7 슬 9–10)

**DFT(AIMD)**: 고정확도 · 소규모 · 비용↑ / **고전 MD**: 대규모 · 비용↓ · **force field 의존** · 저정확도
→ MLIP가 양쪽을 흡수.

**시뮬레이션–실험 괴리 4가지** (p.7 슬 10) — 이 목록이 덱 전체의 문제 정의다:
1. **Size-scale (DFT)** — 다결정 grain의 다양한 크기·형상이 이상화된 작은 모델에 안 담긴다
2. **Time-scale (MD)** — 이온 동역학·계면 반응이 **ns~μs**에서 일어남 → DFT 시간창 밖 + 적절한 force field 부재
3. **Reactive dynamics (DFT & MD)** — 입계·이종 계면의 고유 반응성이 단순 주기 모델로 표현 불가
4. **External environment (DFT & MD)** — 비평형 / 전기장 / 이온 농도구배

→ MLIP로 **수천 원자 / 장시간 확산·반응 / 계면 반응 동역학**을 열겠다는 것.

**MLIP PES 개념도** (p.6 슬 8)가 이 덱의 방법론적 핵심 한 장:
DFT PES → uMLIP PES 로 갈 때 **softening**(평활화)이 일어나고, **fine-tuning**으로 되돌린다.
훈련점이 **near-equilibrium(노란 점)**에 몰려 있고 **high-energy states(붉은 점)를 augment 해야
한다**고 그림으로 명시. → **범용 uMLIP를 그대로 쓰면 고에너지·반응 영역에서 PES가 물러진다**는 자인.

---

## 4. ASSB × MLIP 연구 5갈래 (p.9 슬 13) ★ 핵심 지도

| 갈래 | 엔진 | 내용 | 출판 상태 (덱 표기) |
|---|---|---|---|
| **Anode interface RXN** | MTP | Li \| SSE 계면 반응 | *Under review* at **Chem. Eng. J.** |
| **Cathode interface RXN** | SevenNet | **"17,230 Li, O crystal structure @ MP"**(덱 원문 그대로 = Li·O 함유 산화물) → **Electro-, interfacial, electronic stability** → **Li–Li networks (≤ 3.5 Å)** → **Best candidate: Li₃Sc₂(PO₄)₃** (+ 계면 MD `NCM523(104) ‖ Li₃Sc₂(PO₄)₃(101)`, Arrhenius σ 패널). **코팅 소재 스크리닝** | **Nano Converg. 2026, 13, 27** (= `papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md` 정본) |
| **Dynamic properties** | MTP | Li-ion conductivity @ bulk & interface. **ordered anions → slow / disordered anions → superionic**; Li⁺–BH₄ 거리, B–H 각변위 | *Revision* in **Adv. Energy Mater.** / **Nano Energy 2024, 124, 109436** |
| **Surface RXN** | SevenNet | 전기화학 물성 평가, fine-tuned universal MLIP, 반응물→전이상태→생성물, 대규모 MD, **RHS 가수분해 기구**, **Sn 도핑 억제** | *Revision* in **Adv. Funct. Mater.** |
| **Designing novel materials** | MTP | **CSP** (USPEX + GA + active learning) | **JACS 2025, 147, 47381**; **Rare Metals 2025, 44, 2366** |

> 🔑 이 표가 이 덱에서 우리에게 가장 값진 정보다. **다섯 축 중 셋(음극계면·표면가수분해·양극코팅
> 스크리닝)이 우리 미보유 축**이고, 하나(무질서 전도)는 우리가 `papers/kim2024_...` 로 이미
> 정독한 축이며, 하나(CSP)는 우리 문제설정(host 고정 개질)과 다른 축이다.

---

## 5. MLIP 훈련셋 프로토콜 ★★ (p.9 슬 14 · p.11 슬 17)

### 5a. 일반 6단계 (슬 14) — "configuration space를 거의 전부 덮는다"

```
(1) 6 characteristic configurations, DFT-optimization @ PBE
(2) Lattice strain = ±0.05%, 0                      ← 박스 표기. 같은 슬라이드 도해 밴드는 "±5% Strain"
                                                       = ±0.05%는 오기 확정 (§12-2 · §15)
(3) Short-time AIMD @ 300K–1200K, 0.1 ps 간격 스냅샷  → (7,200 structures)
(4) Single point DFT with different functional: 1) PBE  2) optB88  3) PBE + D3damp
(5) MTP potential training (R_cut = 5 Å, **w_e : w_f = 100 : 1**)   ← 에너지:힘 가중치비 (lev 아님)
(6) MD simulation with MTP: 100 ps NVT heating → 10 ns NPT → ionic conductivity(σ_RT)
```
도해 밴드 3계층(훈련셋이 configuration space를 덮어가는 그림): **6 configurations("Untrained region"
= 점 6개만) → ±5 % Strain(점이 원으로 확대) → AIMD snapshots(원들이 겹쳐 공간을 덮음)**.

정확도 회귀는 **3조성 6패널**(덱 (a)/(b)/(c)):

| 조성 | 에너지 MAE | 힘 MAE (덱 표기) |
|---|---|---|
| **Li₆PS₅Cl** | **2.88 meV/atom** | 0.073 meV/Å |
| Li₆PS₅Br | 2.92 meV/atom | 0.075 meV/Å |
| Li₆PS₅I | 2.51 meV/atom | 0.066 meV/Å |

힘 단위가 meV/Å로 적혀 있는데 이는 `papers/kim2024_...` 감사에서 **이미 확인된 단위 오기**(실제 eV/Å)의
덱 재발이다 — 3패널 전부 같은 오기.

> 🔑 (4)의 **functional 3종 병렬 학습**이 그 그룹의 서명 기법이다. Kim 2024 논문에서
> **optB88-vdW만 site-disorder 의존성을 재현**하고 PBE·PBE-D3는 100%-ordered를 3.7 mS/cm로
> 오판한다는 결론이 여기서 나온다. → **"MLIP σ 절대값은 훈련 functional의 각인"**.
> 우리 "UMA 절대 σ 인용 금지" 규율의 외부 정면 증거로 이미 등록돼 있다.

### 5b. 계면용 훈련셋 (슬 16) — passive + active learning

**훈련 구조 3계층**
- **Bulk**: Li₆PS₅Cl / Li₆PS₅Cl **50% disordered** / Li bcc (3×3×3)
- **Slab**: LPSCl(100) / LPSCl 50%-disordered(100) / Li bcc(100)
- **Interface**: LPSCl(100) ‖ LPSCl 50%-disordered(100) ‖ Li(100)

**Passive learning**: DFT(PBE) 구조최적화 → **Bulk AIMD 30 ps** (T = **300–1200 K + 2000 K, 300 K 간격**,
**0.2 ps 간격 스냅샷**) + **3 ps 간격 스냅샷 → −10 ~ +10 % (2 % 간격) strain** + **Slab AIMD 10 ps**
(Li(100) / Argyrodite(100)) → **DFT(optB88) 재계산** → MTP 훈련·선별 (**R_cut = 6, Lev_max = 12**)

**Active learning**: MTP-MD @ **300/500/700/900 K, strain −5 ~ +5 % (5 % 간격)** →
**γ_select = 2, γ_break = 10 ↔ 5 ↔ 2** 로 구조 선별 → DFT(optB88) → MTP 재훈련
(**w_e = 1, w_f = 0.01, w_s = 0.001**) → **수렴 판정 4조건: MD reliability = 100 % · No. structures
selected < 50 · MAE_energies < 10 meV/atom · MAE_forces < 0.3 eV/Å** → Trained MTP →
생산 **MD NVT, large interface models (>1,000 atoms), 20 ns, 350 K**

> ✅ **§13 Q3("γ 수치 기준은?") 종결** — 덱 슬 16 좌하단 흐름도에 숫자가 그대로 있다. 그리고 이 값들은
> `papers/kim2026_li_argyrodite_sei_reactive_md.md`(SSRN 정본)의 **γ_select = 2 / γ_break 10→5→2 ·
> R_cut 6 Å · lev_max 16 · 5,400 스냅샷 · NVT 350 K · 20 ns** 와 정합한다(lev_max만 덱 12 ≠ 정본 16 —
> 정본 우선). 이전 digest의 `η = 0.91` · `MAE_F ≈ 0.5 eV/Å` 는 **덱 어디에도 없다**(§15-8).

**ΔE_MTP vs ΔE_DFT 산점도에 `γ_select`–`γ_break` 사이를 "Accurate region"으로 명시** ★★
→ **외삽 등급(extrapolation grade) 관리**. 이것이 이 덱에서 우리가 가져올 1순위 항목이다.

**스케일 전환**: 훈련은 **atoms < 200**, 생산 MD는 **atoms > 6,000**.

### 5c. 훈련셋 규모 (슬 17)

| 물질 | 유형 | 개수 |
|---|---|---|
| Li | Bulk (0.2 ps interval) | 5 temps × 150 = 750 |
| | Bulk (**3 ps interval → ±10 % strain**) | 5 temps × 10 × 11 = 550 |
| | Slab 100 (**0.1 ps interval**) | 5 temps × 100 = 500 |
| LPSCl **0 % X⁻@4c** | 위와 동일 3종 | 1,800 |
| LPSCl **50 % X⁻@4c** | 위와 동일 3종 | 1,800 |
| **합계** | | 1800 + 1800 + 1800 = **5,400** |

온도 5점 = 300 / 600 / 900 / 1200 / 2000 K.
**정확도**: Li — **11 meV/atom · 0.083 eV/Å** · LPSCl — **5 meV/atom · 0.111 eV/Å**
(이 두 패널만 단위가 제대로 eV/Å로 적혀 있다 — 슬 14의 meV/Å 오기와 대조).
1 ns DFT-vs-MTP 에너지 궤적이 겹침(초기 0.2 ns 완화 구간 제외).

무질서 배열 도해 6종 (덱 표기 그대로, 전부 **X⁻ in 4c**):
`0 % X⁻ in 4c (F4̄3m)` / `25 % (R3m)` / `50 % (P2₁22)` / `100 % (F4̄3m)` / `75 % (R3m)` / `50 % (P2mm)`
범례 = `4c sites (S²⁻)` / `4c sites (X⁻)` / `4a sites (S²⁻)` / `4a sites (X⁻)`.
→ Kim 2024 논문의 6배열과 동일 세트. ⚠ 표기 주의: **이 랩의 `4c` = Kraft/우리 `4d`(cage center)**.

---

## 6. 음극 계면 반응 MD ★★ (p.11–12 슬 18–19)

**"Long-time & Large-scale Simulation + Interface Reaction Dynamics"**

- 셀: **Li metal 6 nm + LPSCl 10 nm = 총 16 nm** (슬 18 좌측 화살표 라벨, 9× 확대 확정 2026-08-26 — 종전 기재 `3 nm × (10 nm 방향)` 은 **오독이라 정정**; STT `6나노 16나노` 가 독립 확인 → §99-5 B2), **0 → 10 ns → 20 ns** 진화, SEI 영역 형성
- **계면 결정영역이 Li₂S로 동정**: g(r)가 Li₂S 기준 곡선과 일치, (100)/(010)/(001) 면 도해
- **영역분해 MSD** (MSD(t) 0–20 ns, **11 ns 기점 표시**):
  - **Li (crystalline region) D = 0.4 × 10⁻⁷ cm²/s**
  - **Li (remaining bulk) D = 1.1 × 10⁻⁷ cm²/s**   ← **덱도 10⁻⁷ 로 적혀 있다**(2026-08-03 원해상도 확인)
  → 생성된 interphase가 **모체보다 느리다**(비 **0.36**). 정본 `papers/kim2026_li_argyrodite_sei_reactive_md.md`
  의 0.4e-7 / 1.1e-7 / pristine 1.6e-7 과 일치. ⛔ **D 절대값 인용 금지**(정본 규율) — 비율만.
- **시계열**: 우측 소패널이 **1 ns / 7 ns / 10.5 ns / 11.5 ns / 20 ns** 로 끊어져 있다(정본의
  "S가 먼저 골격 7 ns → Li 침투가 결정화 11 ns" 2단계 기구와 같은 시점들).
- **상 동정**: g(r) 가 Li₂S 기준곡선과 겹침 + Li₂S **(100)/(010)/(001)** 면 도해.
- **50 ns까지 확장** (슬 19): initial/10/20/30/40/50 ns 6단, 50 ns 프레임에 **≈ 11 nm** 화살표.
- **실험 대조**: *ACS Energy Lett.* **2022, 7, 3064–3071**(Luo 2022) 의 cryo-TEM 두 장을 나란히 놓고
  "well agreement" 주장. 두 패널 라벨은 **25 °C** (interphase layer **~12 nm**, Li₂S(111) ~0.33 nm
  격자무늬, 20 nm 스케일바) 와 **60 °C** (Amorphous + Li₂S 회절점) — **80 °C 가 아니다**.
  ⇒ 즉 **"계산 11 nm @50 ns vs 실험 ~12 nm"** 라는 정량 대조가 **덱 안에 실제로 있다**(§12-6 갱신).
  단 이 두 온도 라벨은 **인용된 실험 그림의 것**이지 그들 MD 조건이 아니다(MD는 350 K 단일).

> 🔑 **우리에게 직접적인 벤치마크 수치**가 여기 있다 — 우리가 Li|LPSCl 반응성 MD(M-계열 후보)를
> 돌리면 **① interphase 두께 ~11 nm @ 50 ns ② Li₂S 결정화 ③ D(interphase)/D(bulk) ≈ 0.36**
> 이 세 개를 재현 대상으로 삼을 수 있다. 단 **UMA(사전학습) vs MTP(자체학습)** 차이가 있어
> 정량 일치는 요구하지 않는다(§10 참조).

---

## 7. 표면 가수분해 (H₂S 발생) ★★ (p.13–14 슬 21–24)

### 7a. 반응좌표 기반 훈련셋 (슬 21) — 발상이 좋다

훈련셋을 **반응 진행 단계로 나눠** 설계:
```
Pre-mixing (Li₂S + LiCl + P₂S₅) → Material prepared (Li₆PS₅Cl) → Reactants (LPSCl + H₂O)
   → Transition state (H₂O → H₂S, E_a)  → Products
```
하위 셋: `General purpose`(Li·P·S·Cl·H·O 무작위 상자) / `LPSC (100)` / `LPSC (100) + H₂O` /
**`Guided MD`** — 유도 좌표 **2개: D_S–H** (H가 골격 S로 접근) 와 **D_O–P** (H₂O의 O가 P로 접근) /
`LPSC "S ↔ O"` (S–O 교환 경로)

**엔진 정확도** (SevenNet, 슬 22): **8.8 meV/atom · 0.57 eV/Å · 0.35 kbar**. MD 500 스텝 에너지 궤적이 DFT와 일치.

### 7b. LPSCl vs H₃O⁺ + OH⁻ + H₂O (슬 23)

- 계: **LPSC(100) 4 nm + 용액 2.5 nm**, 3 nm × 3 nm, **32 H₃O⁺ + 32 OH⁻ + 299 H₂O**, **500 ps**
- 결과: **PS₄ 분해 → H₂S 발생 → 표면 붕괴**. `polyhedron-sulfur → single-sulfur` 전환
- **H 침투 지도**(**z 0–65 Å** × t 0–500 ps, colorbar `Number of H` 0–15): 표면(z ≈ 40–46 Å)과
  용액 상단(z ≈ 58–65 Å)에 **hydration layer** 점선박스, 그 아래로 **H penetration** 화살표.
  ⚠ z ≈ 0–4 Å 의 띠는 주기경계 반대편 표면(슬래브 바닥)이다 — 벌크 침투로 읽지 말 것.
- **COHP 정량** ★:
  - **ICOHP(P–S) = −6.43 eV**, 결합 2.04 Å
  - **ICOHP(P–S(H)) = −4.69 eV**, 결합 **2.18 Å** ← 양성자화가 P–S를 **27 % 약화**
  - 반결합 상태(antibonding)가 E_F 근처에 생김
- **S 궤적 비교**: 순수 H₂O에서는 S가 거의 안 움직이고, H₃O⁺/OH⁻ 조건에서 광범위 확산

### 7c. Sn 치환의 억제 기구 (슬 24) ★

- 조성: **Li₆.₂₅P₀.₇₅Sn₀.₂₅S₅Cl**
- **SnS₄–H 결합이 PS₄–H 보다 강해 H를 SnS₄ 쪽으로 유인** → PS₄ 보호
- 정량: `Normalized SnS₄–H (≤ 2 Å)` 신호 **0.6–0.8** 이 500 ps 내내 유지 vs `PS₄–H` **≈ 0**(억제)
- **Relative E_H**: **SnS₄–H = 0.0 → PS₄–H ≈ 0.3 eV** (직선; y축 0.0/0.1/0.2/0.3 눈금의 최상단)
  ⚠ figure-read — 이전 digest의 `0.28 eV` 는 과잉정밀이다. **"≈0.3 eV" 또는 "0.28–0.30 eV"** 로 쓸 것

> 🔑 이것이 **HSAB 소프트-산 도핑이 대기안정성을 올린다**는 우리 cascade `air_hsab` 축의
> **반응 동역학 수준 기구 설명**이다. 우리는 정성 tier만 갖고 있고, 그들은 궤적·COHP·E_a를 갖고 있다.
> 우리 db의 `taklu2021_cucl...`(Cu₃PS₄ → H₂S 절반)이 실험 쪽 같은 이야기다 — **실험(Taklu) +
> 기구(Lee) + 우리 스크리닝(cascade)** 삼각이 성립한다.

---

## 8. CSP — 준안정 구조 설계 (p.15–17 슬 26–29)

**문제 제기**: "Composition = Structure?" 아니다 — C(다이아/그래파이트), C₈H₁₀(p-/m-크실렌).
**Metastable = New Functional Materials**.

**uMLIP-CSP 플랫폼** (슬 27): 조성 입력 → 초기구조(amorphous + random) → uMLIP →
**CSP 루프(USPEX GA ↔ MTP ↔ active learning ↔ DFT query)** → finetuned MTP로 최종 CSP → 평가.
응용 표적: 고엔트로피 합금 / **다성분 고체전해질** / 고활성·선택성 / **초이온전도**.

**Li–[Si–Ge]–S 적용** (슬 28) ★ — 덱에서 가장 강한 단일 결과:

> ⛔ **아래 표는 철회됐다 (2026-07-29).** 논문 실물 대조 결과는
> `papers/kim2025_csp_metastable_edge_sharing_sse.md` §9-A · `papers/huang2022_li2sis3_anomalous_conductivity_bvse.md` §2.
> `talks/README.md` 규율 #2 — **덱과 논문이 충돌하면 논문이 정본**이다.

| 덱 표기 | 논문 실물 | 판정 |
|---|---|---|
| corner-sharing σ = **10⁻⁴ mS/cm** | 논문은 corner 상의 σ 를 **수치로 주지 않는다**. "3 orders lower" 역산 ≈ 2.4×10⁻³ mS/cm | ❌ 약 24배 틀림 |
| edge-sharing σ = **2.4 mS/cm** | **Huang 2022 실험값**(n-Li₂SiS₃, 2.4×10⁻³ S/cm @298 K) — CSP 논문 자체는 σ 를 한 번도 계산하지 않는다 | ⚠ 출처를 Huang 2022 로 붙이면 사용 가능 |
| 상승폭 **4자릿수** | CSP 논문 자체 주장 = **2자릿수**(계산 D). Huang 2022 소환 = **3자릿수**. **4자릿수는 어디에도 없다** | ❌ 존재하지 않는 수치 |

→ 안전한 서술: **"준안정 edge-sharing 상이 계산 D 기준 2자릿수 앞선다(CSP 논문)"**,
   실험 대비가 필요하면 **"Huang 2022 실험에서 3자릿수"** 로 출처를 갈라 쓴다.
`D_600K × 10⁵ cm²/s` vs `Relative Stability rank 1–10` 플롯에서 **E_rel 0–0.05 eV/atom 안에
고전도 준안정상이 다수 존재**함을 보임 (Li₂SiS₃, Li₄SiGeS₆). 실험 보고 구조는 낮은 rank에 위치.

**준안정 고전도의 3 기술자** (슬 29, JACS 2025, 147, 47381):
1. **Dead volume** — 양이온 중심 S₄ 사면체가 Li 경로를 막는 부피
2. **Distance of cation** — corner-sharing의 양이온-양이온 거리 d_c > edge-sharing d_e
3. **Li–S₄ distortion** — Li–S₄ 부격자 왜곡 시 인력↓·거리↑·부피↑

> ⚠ **논문 결론부의 기술자 3종은 이것과 다르다** (`papers/kim2025_csp…` §9 / 원문 eq 9–11):
> **① packing ratio α ② Li–S₄ 부격자 부피 ③ CSM(연속대칭척도)**.
> 덱의 "dead volume" 은 독립 기술자가 아니라 **α 의 구성요소**이고,
> "distance of cation" 은 기술자가 아니라 **기구(mechanism)** 다. 이식할 땐 논문 쪽을 쓴다.

---

## 9. 기타 (p.5 슬 5–6, p.17 슬 30)

- **DB 스크리닝 깔때기** (슬 5): ICSD/MP/USPEX/AIRSS/EnumLib/OQMD/**K-MDS** → >10,000 DFT+U 최적화
  → **E_hull < 30 meV/atom → Q ≥ 400 mAh/g → E_g < 2.0 eV** → 유망 양극.
  **슬라이드가 직접 던지는 질문 두 개**: *"Suitable database for R&D topic — General DB? Specific DB of SSE?"*,
  *"Screening Descriptor!! — General? Specific?"* → 우리 깔때기 문제의식과 정확히 같은 질문.
- **GNoME** (슬 6, *Nature* 624, 80–85, 2023): 기존 DB → 후보 생성 → GNN 안정성 예측 → DFT 검증 →
  DB 확장 → GNN 재학습 → 반복. 2.2 M stable / 381 k new stable crystals.
- **LFP SOC 예측** (슬 30): **PyBaMM**(SPM, Prada2013 파라미터셋) → 합성 데이터 → 특징공학(ΔT, ΔV, 이동평균)
  → **Random Forest**. 학생 프로젝트 성격.

---

## 10. 우리 대비 — 축별 판정 ★★

| 축 | 그들 (덱 + kim2024 논문) | 우리 | 판정 |
|---|---|---|---|
| **무질서 → σ** | 6배열 전수 MTP-MD, ordered Ea 339–529 meV vs disordered 151–256 meV | disorder_ensemble (disordered 0.177 ± 0.027 eV, ordered frozen) | **방향 완전 일치**. 우리 강점은 **배열 간 분산을 오차막대로 보고**하는 것 (`papers/kim2024_...` §감사: 그들 6배열엔 config-variance 오차막대 없음) |
| **MLIP σ 절대값** | 훈련 functional에 따라 σ80% 가 8배 갈림 → optB88만 맞음 | **절대 σ 인용 금지** 규율 | **우리 규율이 그들 데이터로 정당화됨**. 그들은 σ_RT를 직접 인용 |
| **음극 계면 반응** | Li₂S interphase, 11 nm @ 50 ns(실험 ~12 nm), D 0.4 vs 1.1 ×10⁻⁷ (비 0.36) | **없음** | **완패 — 우리 공백**. 최우선 채택 후보 |
| **표면 가수분해** | SevenNet 반응 MD + ICOHP + Sn 억제 ΔE_H ≈ 0.3 eV | `air_hsab` **정성 tier** | **완패**. 단 우리는 47종 횡단, 그들은 2조성 |
| **양극 코팅 스크리닝** | **17,230 Li·O 산화물 @ MP** 4축 깔때기 → **Li₃Sc₂(PO₄)₃** (Nano Converg. 2026) | cascade 47종 × 6축 + 오늘 M6 계면반응성 추가 | **풀은 그들이 10²배, 축 밀도는 우리가 우위** — S6 감사의 직접 대조군. 원소 수렴: 그들 최종 **Sc** ↔ 우리 cascade `Sc₂O₃` 1위(⚠ 이유 다름) |
| **CSP / 신조성** | USPEX+MTP, Li₂SiS₃ 준안정 상 σ 상승(⛔ 덱의 '4자릿수' 철회 — 계산 2자릿수) | 없음 (host 고정 문제설정) | **문제설정이 다름** — 열위가 아니라 무관. 단 "준안정이 더 좋을 수 있다"는 명제는 우리 metastable 고찰과 공명 |
| **MLIP 외삽 관리** | γ_select / γ_break "Accurate region" | **없음** | **완패 — 방법론 공백**. 우리 UMA는 외삽 등급 무관리 |
| **엔진 전략** | 자체 학습 (MTP 5,400셋 / SevenNet fine-tune) | 사전학습 UMA 그대로 | 트레이드오프. 그들은 정확도·우리는 횡단 속도 |
| **입계(GB)** | Σ5 GB >13,860원자, D_GB = 0.3× bulk | 없음 | **공백** (이미 등록됨) |
| **데이터 정직성 장치** | 덱에서 확인 안 됨 | vacuous gate·순서민감도·탈락명단·인용금지 규율 | **우리 우위** (단 §12 주의 — 부재 주장 금지) |

---

## 11. 우리가 가져올 것 (실행 항목화)

각 항목은 `kb/projects/symposium_2026_competitive_analysis.md` 에서 **T1–T8** 로 관리한다.
여기서는 근거만 남긴다.

1. **γ_select / γ_break 외삽 등급** (슬 16) — 비용 0에 가까운 방법론 이득. 우리 UMA MD에
   **"이 스냅샷은 훈련영역 밖"** 판정이 아예 없다. 가장 먼저 가져올 것.
2. **반응좌표 기반 검증셋** (슬 21) — 우리는 학습을 안 하므로 훈련셋이 아니라 **검증셋**으로:
   pre-mixing → reactants → TS → products 각 단계에서 UMA vs DFT 단일점 비교.
3. **Li|LPSCl 반응 MD** (슬 18–19) — 벤치마크 3종(11 nm / Li₂S / D비 0.36) 확보 완료.
4. **ICOHP(P–S) 양성자화 약화 기술자** (슬 23) — −6.43 → −4.69 eV. 이건 **우리 47 도펀트에
   그대로 계산 가능한 정량 기술자**다. `air_hsab` 정성 tier를 대체할 후보.
5. **functional 병렬 학습의 우리 판** — 우리는 학습을 안 하지만, **UMA vs DFT 단일점 벤치마크를
   무질서 배열별로** 돌리면 같은 종류의 "각인" 진단이 된다.
6. **영역분해 MSD** (슬 18) — 계면/벌크 구획별 D 산출. 우리 MSD 파이프라인에 구획 마스크만 추가.
7. **Nano Converg. 2026, 13, 27 (17,230 스크리닝)** — **S6 후보 나열 감사의 직접 대조군**.
   PDF 확보 최우선 (§13 위시리스트).

---

## 12. 주의 / 한계 (over-claim 방지)

1. **덱은 부재의 증거가 아니다.** "그들은 config-variance 오차막대가 없다"는 서술은 **덱이 아니라
   `papers/kim2024_...` 논문 실물 감사**에서 나온 것이며, 그 범위(Nano Energy 2024) 안에서만 유효하다.
   *Revision in Adv. Energy Mater.* 로 표기된 후속에서 보완됐을 수 있다.
2. **strain 값 4개가 덱 안에서 갈린다 — 2026-08-03 재판독으로 정리됨**:
   - **벌크 σ 프로토콜(슬 14)**: 박스 `±0.05 %` **vs** 같은 슬라이드 도해 밴드 `±5 % Strain`
     → **`±0.05 %` 가 오기**(논문 kim2024 도 `±5 %`). 이건 모순이 아니라 **오타 1건**으로 확정.
   - **계면 훈련셋(슬 16·17)**: passive `−10 ~ +10 % (2 % 간격)` / active `−5 ~ +5 % (5 % 간격)`
     → **서로 다른 단계의 서로 다른 설정**이라 모순 아님. 정본(`kim2026_li_argyrodite_sei…`)의
     "±10 % 부피 strain 포함"과도 정합.
   ⇒ 인용 시 **"벌크 ±5 % / 계면 passive ±10 %·active ±5 %"** 로 쓰고, `±0.05 %` 는 쓰지 말 것.
3. **힘 MAE 단위** — 슬 14 "0.073 / 0.075 / 0.066 meV/Å"(Cl/Br/I 3패널 전부)는 eV/Å의 오기.
   논문 감사에서 이미 확인된 동일 오기의 재발. 반면 **슬 17은 eV/Å 로 제대로** 적혀 있다(같은 덱 안 불일치).
4. ✅ **해소(2026-08-03)** — 코팅 스크리닝 최종 후보는 **`Best candidate: Li₃Sc₂(PO₄)₃`** 로
   덱에 명시돼 있다(원해상도 확대로 판독). 이전 "Li₆xPO₄(?) 판독 불가"는 저해상도 탓이었다.
   정본 `papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md`(17,230 → 88 → 8 → Li₃Sc₂(PO₄)₃ γ-phase)와 일치.
5. **σ_RT 절대값 인용 금지** — 그들 파이프라인이 10 ns NPT MTP-MD에서 σ_RT를 직접 뽑지만,
   `papers/kim2024_...` 가 **같은 물질에서 functional에 따라 8배 갈린다**는 것을 보였다.
   ⛔ **그런데 그 비율 자체가 틀렸다** — `10⁻⁴ → 2.4 mS/cm` 의 "4자릿수" 는 논문에 없다
   (계산 2자릿수 / Huang 2022 실험 3자릿수). 절대값도 비율도 덱에서 가져오지 말고
   **논문 digest 에서 가져올 것**: `papers/kim2025_csp_metastable_edge_sharing_sse.md` §9-A.
6. **"well agreement with experiment"(슬 19)** — 재판독 결과 **정성 대조만은 아니다**: 인용된
   cryo-TEM(ACS EL 2022, 25 °C) 패널에 **`~12 nm` 라벨**이 찍혀 있어 **계산 11 nm vs 실험 ~12 nm**
   비교가 성립한다(정본 digest의 서술과 동일). 다만 **덱 본문에 "몇 % 일치" 문장은 없고**, 그림은
   **단일 시야·단일 시료**이며 우리 쪽 인용은 **"자릿수·두께 스케일이 맞다"** 수준까지만.
7. **LFP SOC(슬 30)** 는 학생 프로젝트 수준이고 우리 축과 무관. 인용 가치 없음.

---

## 13. 미해결 질문 (2026-08-26 구술 판독 반영)

| # | 질문 | 닫는 방법 |
|---|---|---|
| ~~Q1~~ ✅ | 코팅 스크리닝 17,230 풀의 **입구 필터와 최종 후보 조성**은? | **종결** — 정본 `papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md` 확보(MP의 **Li·O 함유 산화물 17,230종** → ECW → 계면반응성 → gap → **Li–Li ≤ 3.5 Å** → 88 → 8 → **Li₃Sc₂(PO₄)₃** γ-phase). 덱 슬 13에도 같은 4단 깔때기 + 후보명이 그대로 적혀 있다(2026-08-03 재판독) |
| Q2 | Li\|LPSCl 계면 MD에서 **어느 무질서 배열**을 썼나 (50 %만? 전수?) | Chem. Eng. J. under review / 구술. ⚠ 정본(SSRN `kim2026_li_argyrodite_sei_reactive_md`)도 **프로덕션 무질서배열 미명시** — 덱 훈련셋은 0 %와 50 % 두 배열뿐(슬 17) |
| ~~Q3~~ ✅ | γ_select / γ_break **수치 기준**은? | **종결(2026-08-03)** — 덱 슬 16 흐름도에 **γ_select = 2, γ_break = 10 ↔ 5 ↔ 2**, 수렴 4조건(reliability 100 % · selected < 50 · MAE_E < 10 meV/atom · MAE_F < 0.3 eV/Å), 손실 가중치 w_e = 1 / w_f = 0.01 / w_s = 0.001. 정본과 일치 |
| Q4 | 가수분해 MD의 **H₂S 발생량 정량**(우리 db의 Taklu 1.07→0.49 cm³/g와 대조 가능한가) | Adv. Funct. Mater. revision. ⏳ **구술로 못 닫힘**(2026-08-26) — 구술은 기구만 말하고 수량이 없다 → §99-6 |
| Q5 | Adv. Energy Mater. revision(=Dynamic properties 후속)이 **BH₄ 계**인지 argyrodite인지 | ~~구술~~ ⏳ **구술로 못 닫힘**(2026-08-26) — 31분 전체에 후속 논문 언급 자체가 없다. **논문 확보만이 답** → §99-9 #7 |
| ~~Q6~~ ✅ | CSP의 준안정 구조가 **합성 가능성** 검증을 받았나 | **종결** — 정본 `papers/kim2025_csp_metastable_edge_sharing_sse.md` 확보(E_hull 40구조 전부 0–42 meV/atom · phonopy G(T) 교차온도 보고). 구술도 *"실험하시는 분들이 이 준안정 구조를 만드시면"* 로 **미합성 상태임을 전제**한다 `[STT 24:27]` |
| **Q-T1** 🆕 | 자료집 다음 발표자가 **문장혁**인가 STT 의 `김장현`인가 | 자료집 **목차 페이지** 필요 → §99-9 #2 |
| **Q-T2** 🆕 | A1 "파라미터가 많아서"가 **속도**인가 **PES softening**인가 | 음성 재청취 / 본인 확인. **T1b 해석에 직결** → §99-3 |
| **Q-T3** 🆕 | STT `파라테스`·`인시이션` 의 실제 단어 | 음성 필요 → §99-5 D1·D2 |

---

## 14. 인용 가능 문장 (원고/발표용)

- "범용 uMLIP는 평형 근처 훈련점에 치우쳐 고에너지 영역에서 PES가 물러진다(softening) — 그래서
  반응 영역을 보려면 fine-tuning 또는 반응좌표 기반 훈련이 필요하다" (덱 슬 8·21의 명제)
- "MLIP로 계산한 이온전도도의 절대값은 훈련에 쓴 exchange-correlation functional의 각인을 받는다"
  (kim2024 정본; 덱 슬 14가 그 병렬학습 절차를 보여줌)
- ⛔ **인용 금지 (2026-07-29 철회)**: "corner→edge 로 확산 4자릿수" — 논문에 없는 수치다.
  대체 문장: "준안정 edge-sharing 상이 계산 D 기준 **2자릿수** 앞선다"
  (`papers/kim2025_csp_metastable_edge_sharing_sse.md`; 실험 대비는 Huang 2022 **3자릿수**)

---

## 15. 🔁 덱 실물 독립 재판독 로그 (2026-08-03)

**계기**: 같은 PDF(`litdb/inbox/이상욱 교수님.pdf`, 13.9 MB, 18 pp, Microsoft Print-To-PDF,
2026-07-28 14:40 생성)가 inbox에 **재투입**됨. 사용자 분류 **`(미분류)`**.
**방법**: PDF에 **텍스트 레이어가 전혀 없다**(전 18 pp 스캔/이미지, 페이지당 raster 2–28장) →
전 페이지를 이미지로 렌더링해 눈으로 판독하고, 숫자가 걸린 곳은 **embedded raster 원해상도**
(≈267 dpi, strip 1737 px)까지 확대해 확인. 자료집 쪽번호 279–296, p.2(=자료집 280)는 백지.

### 15a. 교정 14건

| # | 항목 | 이전 digest | **덱 실물(재판독)** | 근거 |
|---|---|---|---|---|
| 1 | 코팅 풀 원소집합 | "17,230 **Li·P·S·O**" | **"17,230 Li, O crystal structure @ MP"** | p.9 슬 13 깔때기 최상단 밴드 (1100 dpi) |
| 2 | 깔때기 2단 | "electro-/**mechanical**-/electronic-stability" | **"Electro-, interfacial, electronic stability"** | 동상 |
| 3 | 코팅 최종 후보 | "판독 불가(Li₆xPO₄?)" | **"Best candidate: Li₃Sc₂(PO₄)₃"** + 계면 MD `NCM523(104)‖Li₃Sc₂(PO₄)₃(101)` | p.9 슬 13 (900 dpi) |
| 4 | 슬 14 에너지 MAE | 2.09 meV/atom | **2.88 meV/atom** | p.9 embedded raster 원해상도 |
| 5 | 슬 14 회귀 패널 수 | 1개(LPSCl) | **3개 — Cl 2.88/0.073 · Br 2.92/0.075 · I 2.51/0.066** | p.9 (a)(b)(c) |
| 6 | 훈련 단계 (5) | "lev = 100:1" | **w_e : w_f = 100 : 1** (R_cut 5 Å) | p.9 슬 14 박스 |
| 7 | passive learning | "Bulk AIMD 5 ps / 200 K 간격 / 0.1 ps / strain −5~+5 %(2.5 %) / R_cut 5" | **Bulk AIMD 30 ps · 300–1200 K + 2000 K(300 K 간격) · 0.2 ps 스냅샷 · 3 ps 간격 → −10~+10 %(2 % 간격) strain · R_cut = 6, Lev_max = 12** | p.10 슬 16 흐름도 |
| 8 | active learning | "η = 0.91 · MAE_F ≈ 0.5 eV/Å" | **덱에 η 없음.** γ_select = 2 · γ_break = 10↔5↔2 · **MAE_F < 0.3 eV/Å** · MAE_E < 10 meV/atom · selected < 50 · reliability 100 % · w_e/w_f/w_s = 1/0.01/0.001 · 생산 MD >1,000 atoms·20 ns·**350 K** | p.10 슬 16 |
| 9 | 무질서 6배열 표기 | "0 % X in **4a** (P-43m)" 등 | **전부 `X⁻ in 4c`**: 0 %(F4̄3m)·25 %(R3m)·**50 %(P2₁22)**·100 %(F4̄3m)·75 %(R3m)·**50 %(P2mm)** | p.11 슬 17 도해 |
| 10 | 슬 17 표 간격 | "bulk 2 ps · slab 0.5 ps" | **bulk 3 ps interval → ±10 % strain · slab 100 = 0.1 ps interval** | p.11 슬 17 표 |
| 11 | Li 힘 MAE | 0.063 eV/Å | **0.083 eV/Å** | p.11 슬 17 회귀 |
| 12 | 영역분해 D | "잔여 벌크 1.1 × 10⁻**6**, 덱 자릿수 오기" | **덱도 `1.1 × 10⁻⁷`** (결정영역 0.4 × 10⁻⁷) → **"덱 자릿수 오기" 주석 철회**, 비 0.36 유지 | p.11 슬 18 MSD 패널 |
| 13 | 가수분해 용액/지도 | "200 H₂O · z 0–40 Å" | **299 H₂O** (32 H₃O⁺ + 32 OH⁻) · **z 0–65 Å**, colorbar 0–15 H | p.14 슬 23 (900 dpi) |
| 14 | Guided MD 좌표 | "D_S–H, D_O–**H**" | **D_S–H, D_O–P** | p.13 슬 21 (650 dpi) |

**부가 교정 2건(캐비앳 성격)**: ① Sn 억제 `Relative E_H` 는 **≈0.3 eV**(y축 상단) — `0.28 eV` 는
과잉정밀(§7c). ② 슬 19 실험 TEM 라벨은 **25 °C / 60 °C**(이전 기록의 "80 °C"는 오독)이고 왼쪽 패널에
**~12 nm · Li₂S(111) 0.33 nm** 가 찍혀 있다 → **"계산 11 nm vs 실험 ~12 nm"** 대조가 덱 안에 존재(§12-6).

### 15b. ⛔ 우리 기록의 오류 정정 — "덱이 `17,233 Li-P-S-O` 라고 적었다"는 **사실이 아니다**

우리 db 여러 곳(`papers/kim2026_hts_li3sc2po43…` §2 · `papers/kim2025_csp_metastable…` §9-A ·
`papers/kim2025_li3ycl6…` · `papers/kim2026_li_argyrodite_sei…` · `INDEX.md` ·
`db/properties/external_benchmarks_symposium_2026.json`)에 **"덱: 17,233 Li-P-S-O → 논문 실물:
17,230 Li·O = 덱 오류"** 라는 서술이 퍼져 있었다. **덱 슬 13 원문은 `17,230 Li, O crystal structure @ MP`**
(위 교정 #1, 1100 dpi 판독)로 **논문과 완전히 일치**한다.

⇒ **틀린 쪽은 덱이 아니라 2026-07-28 저해상도 판독으로 만든 우리 전사(轉寫)였다.**
"덱-vs-실물 불일치" 사례는 **2건 → 1건**으로 줄어든다. 남는 진짜 1건은
**Rare Metals 2025(Li₃YCl₆)의 CSP 엔진** — 덱 슬 13은 CSP 갈래를 `MTP + USPEX + GA + active learning`
으로 묶었지만 그 논문 실물은 **CALYPSO/PSO + 직접 DFT**다(`papers/kim2025_li3ycl6_new_crystal_structure.md` §1).

> 🔑 **교훈은 방향이 바뀐다**: "덱은 정본이 아니다"는 규율은 그대로 유효하되,
> **"덱이 틀렸다"고 단정하기 전에 덱 실물을 원해상도로 다시 볼 것**. 스캔 PDF의 저해상도 판독은
> 논문 digest와 같은 등급의 증거가 아니다. (이 로그가 그 절차의 첫 적용 사례다.)

### 15c. 신규 8건 (이전 digest에 없던 내용)

1. **슬 4 "DFT-based LIB Material Researches"** — 이 랩의 DFT 이력 4종이 한 장에: 전해액
   **OP/RP(산화·환원 전위)** 꺾은선(용매 5–6종, OP 최대 ~7.3 V 급), **LiₓMn₂O₄ 2상/1상 영역** ΔE_f,
   **전압곡선 시뮬 vs 실험**, **layered→spinel 반응경로**(TM_hm → 2O₂ gen → dumbbell → spinel, −3O₂)
   + HRTEM. → **MLIP 이전에 이미 양극 상전이·전해액 산화 축을 갖고 있던 랩**.
2. **슬 8 도구 지도** — DFT 코드 `VASP/GAUSSIAN/ORCA/SIESTA`, MLIP `MTP·SevenNET·MACE·CHGNET`,
   그리고 **descriptor 기반 MTP vs GNN 기반 uMLIP(M3GNet/CHGNet/SevenNet/MACE)** 2계층 도해.
3. **슬 12 ASSB 과제 지도의 인용 4축** — 저 σ(bulk, *Energy Sci. Eng.* 2022, 10, 1643) ·
   GB(*JMCA* 2015, 3, 21343) · 대기안정(*JPS* 448 (2020) 227338 — LPSCl 대비 Sn 치환계 2종의
   15 min 노출 H₂S 곡선. ⚠ 두 치환 조성 라벨은 저해상도로 **판독 불가, 추정 금지**) ·
   ESW(*ACS AMI* 2015, 7, 23685).
4. **슬 15(음극 섹션 표지)** — 음극 3계열 **Li metal / LiₓC₆ / LiₓSi** + 과제 4종
   (Li dendrite · interfacial side reaction · interface contact stripping · **highly tortuous
   ion/electronic transport path**).
5. **슬 14 도해 3계층** — `6 configurations`("Untrained region" 명시) → `±5 % Strain` →
   `AIMD snapshots`(공간 피복). **훈련셋 설계 철학을 한 장으로 보여주는 그림**.
6. **슬 18 시계열 해상도** — interphase 진화 소패널이 **1 ns / 7 ns / 10.5 ns / 11.5 ns / 20 ns**
   (700 dpi 판독). 정본의 "S가 먼저 골격(~7 ns) → Li 침투가 결정화(~11 ns)" 2단계와 같은 시점 배치.
7. **슬 23 H 침투 지도 구조** — hydration layer가 **표면(z≈40–46 Å)과 용액 상단(z≈58–65 Å)** 두 곳,
   슬래브 바닥(z≈0–4 Å)은 주기 반대면. **S 궤적 비교**(순수 H₂O = 거의 정지 vs RHS = 광범위 확산).
8. **슬 31 총괄 4블록** — `Surface RXN` / `Interface RXN` / `Long-Time & Large-Scale` /
   `High-throughput Screening` + "Bridge the gap between small-scale models and realistic device-scale"
   (배경 그림 출처 *J. Mater. Inf.* 1, 10, 2021).

### 15d. 재확인(변경 없음)

슬 22 uMLIP 정확도 **8.8 meV/atom · 0.57 eV/Å · 0.35 kbar** · 슬 23 **ICOHP(P–S) −6.43 eV @2.04 Å →
P–S(H) −4.69 eV @2.18 Å** · 슬 24 조성 **Li₆.₂₅P₀.₇₅Sn₀.₂₅S₅Cl** · 슬 17 총 **5,400** 구조 ·
슬 17 정확도 **Li 11 meV/atom · LPSCl 5 meV/atom, 0.111 eV/Å** · 슬 16 **atoms < 200 → atoms > 6,000** ·
슬 28 덱 표기 **10⁻⁴ → 2.4 mS/cm**(⛔ 인용 금지, §14 그대로) · 슬 13 출판정보 5건 ·
슬라이드 번호 `/31`·`/50`·`/24` 혼재.

---

## 99. 🎙 발표 구술(STT) 판독 — 2026-08-26 입수분

> 입수 2026-08-26 · STT 원본 `음성 341` 31분 54초 · 39 블록 ·
> 도구 산출 `_transcripts/lee2026_skku_mlip_materials_design{.json,_scaffold.md,_source_manifest.json}`
>
> ⚠ **증거층 배지**는 `talks/README.md` §3 을 따른다. **음성 미보유**이므로 `[말]` 은 한 번도 쓰지 않는다.
> `[덱]` 인쇄됨 · `[STT mm:ss]` STT 문자열에만 있음 · `[덱+STT]` 일치 · `⛔[불일치]`.
>
> ⛔ **citable = no.** 아래 STT-유래 문장은 **전부 가설 생성용**이다. 원고·발표·db 승격 금지.
> 특히 **Q&A 는 동의 상태 미상**이라 외부 사용이 추가로 막혀 있다(§99-0).

### 99-0. coverage · 증거 상태

| 축 | 값 | 근거 |
|---|---|---|
| 슬롯 | **36 슬롯 추출**(18 pp × 2-up) / 덱 실슬라이드 **31** | `litdb/figures/lee2026_skku_mlip_materials_design/` |
| 덱 판독 | **31/31** (2026-08-03 원해상도 전수) + 오늘 **7 슬라이드 재확인**(6a·6b·9b·11a·11b·12a·13a·13b·16b) | §15 · 오늘 로그 |
| 음성 | **absent** — 파일 미보유 | manifest |
| STT 엔진 | **CLOVA Note** — 원문 말미에 `clovanote.naver.com` 이 **적혀 있다** (추정 아님) | STT 원문 261행 |
| 권리 | **unknown** | — |
| Q&A 동의 | **unknown** ⚠ 질문자 3인 실명 등장 | — |
| 정렬 | 39/39 블록에 슬라이드 배정(§99-1) · `?` 0 · `–` 4 · `skip` 0 | — |
| 미해결 | **6건**(§99-6) | — |
| **citable** | **no** (승격차단 4: audio·rights·qa_consent·stt_engine 중 engine 은 오늘 해소) | manifest |

**등급**: `Exploratory` (README §5-3). 우리와 접점이 크므로 index-only 로 두지 않았다.

---

### 99-1. 슬라이드 ↔ 녹취 정렬 (39 블록 전수)

`–` = 봤으나 어느 슬라이드인지 특정 못 함. PDF p → 슬 번호 환산은 §2 표.

| 시각 | 슬 | 무엇을 말하는 중인가 | 덱에 없는 말? |
|---|---|---|---|
| 00:32 | 1 | 인사 · "앞 강의들과 전혀 다른 세계" | ✅ 있음 |
| 01:31 | 2 | (앞 블록 이어짐 — 화자 겹침) | – |
| 01:32 | 2 | 계산과학의 **기대**: 개발기간 단축 + 실험 가이드라인 → **"눈에 띄는 성과는 없다"** | ✅✅ |
| 02:38 | 3 | Scale & Scientific Method — "이용민 교수님은 오른쪽 끝(셀·전극), 나는 왼쪽 끝(전자)" | ✅ |
| 03:42 | 4 | DFT → 빅데이터 → AI 3단 · 유기전해질 ESW·분해 메커니즘 · 상전이·전압프로파일 | 부분 |
| 04:50 | 4–5 | 양극 붕괴 해석 → **데이터가 쌓인다** → DB 스크리닝 깔때기 | 부분 |
| 05:54 | 5 | **AI 만능 아님 ①** DB 편재성 + 생성방법 불일치 → normalizing **②** descriptor 설정·기준 | ✅✅ |
| 06:55 | 5 | **③** 자체 생성하면 일관되지만 **양이 부족** | ✅ |
| 08:01 | 6 | (좌중 반응 — 화자 3) | – |
| 08:02 | 6 | **GNoME** 2.2 M 안정구조 · 38만 신규 · "DFT 만으로는 절대 불가능" | [덱+STT] |
| 09:05 | 7 | ML = 회귀(W·b) → 변수 늘면 딥러닝/ANN → 학습데이터 필요 | [덱+STT] |
| 10:15 | 7→8 | 데이터 부족 → **active learning** · 둘을 합친 것이 MLIP · PES 정의 | [덱+STT] |
| 11:12 | 9 | **왜 MLIP 인가**: DFT = 슈뢰딩거 → 전자 관련 물성 강함, 계산량 → 작은 계만 / MD = 뉴턴 방정식 → **force field 없으면 아예 못 씀**("argyrodite force field 가 없으면 MD 를 사용할 수가 없다") | ✅ 기구설명 |
| 12:15 | 10 | 크기·시간 한계 → 반응 못 봄 → 실험–시뮬 갭 → **MLIP = scale-bridging technology** | [덱+STT] |
| 13:12 | 11–12 | ASSB 과제 지도 · **"DFT/MD 로 절대 볼 수 없었던 것 = 계면 반응"** | 부분 |
| 14:13 | 13 | 5갈래 예고 + **동기**: "argyrodite 원천기술은 해외 → 완전히 다른 새 결정구조를 찾아야 한다" | ✅✅ |
| 15:11 | 14 | **configuration space 를 덮어야 한다** — 안 덮으면 "MLIP 만들어봐야 아무 소용 없다" | ✅ 강조 |
| 16:12 | 15–16 | passive → **active learning** 재학습 루프 · **200 atom 학습 → 6,000 atom 시뮬** | [덱+STT] |
| 17:06 | 17–18 | 검증(스냅샷 DFT 재계산) · 셀 **6 nm + 10 nm** · Li 확산 → 비정질 붕괴 | [덱+STT] |
| 18:09 | 18 | **기구**: S 가 Li 보다 커서 **음이온이 먼저 close-packing** → 뉴클리에이션 → 빈 격자간 자리에 Li 진입 → Li₂S interphase | ✅✅ 기구 |
| 19:01 | 19 | 50 ns · **11 nm 수렴** · 실험 12 nm · "bridging 근거" | [덱+STT] |
| 20:11 | 20–21 | 가수분해 훈련셋: 실제 **합성 공정 단계**를 본떠 설계 · **TS 구조가 없으면 반응을 못 그린다** → **guided MD** | ✅✅ 방법 |
| 21:22 | 23 | H⁺ 가 골격 S 와 결합 → **P–S 결합 세기 약화** → PS₄ 분해 · H 의 **깊이 방향 침투** | [덱+STT] |
| 22:30 | 24→25 | **Sn 치환**: Sn 이 P 보다 H 를 **더 강하게 붙잡고**, Sn–S 결합이 더 강해 → **H scavenging** → 억제 | [덱+STT] |
| 22:30 | 26 | 준안정 동기: C(다이아몬드/흑연) · **C₈H₁₀ para-/meta-xylene** | ✅ 비유 |
| 23:27 | 27–28 | CSP 로 **1–10위 신규 구조** · **corner-sharing 이 안정 / edge-sharing 이 준안정인데 전도 높다** | [덱+STT] |
| 24:27 | 28→29 | **실험자에게 제안**: "이 준안정 구조를 만드시면 전도도가 엄청나게 높다" | ✅ 태도 |
| 25:12 | 30 | **PyBaMM + ML 로 SOC 추정** — 학부연구생 2명 · 동기 "셀·전극 단위로 넘어가고 싶어서" | ✅ 동기 |
| 25:12 | 31 | 총괄 — MLIP = scale-bridging | [덱+STT] |
| 25:43 | – | 좌장 정리 | – |
| **26:02** | – | **Q1 — 질문자 = 안용훈(한양대)** ★ | Q&A |
| **26:50** | – | **A1 — MTP vs universal potential 분업** ★★★ | Q&A |
| 27:53 | – | A1 마무리(문장 끊김) | Q&A |
| **28:01** | – | **Q2 — 좌장: 멀티스케일 통합 가능한가** | Q&A |
| **28:47** | – | **A2 — "10여 년 전부터의 꿈, 아직 요원"** ★★ | Q&A |
| 29:46 | – | Q3 질문자 자기소개(UNIST) | Q&A |
| **29:54** | – | **Q3 — 도메인 지식 중심 학생이 쌓을 기초는?** | Q&A |
| 30:30 | – | (좌중 발화 · 판독 불가) | – |
| **30:34** | – | **A3 — "수학·코딩보다 도메인 지식 + LLM 활용력"** ★★ | Q&A |
| 31:33 | – | 좌장 마무리 | – |
| 31:44 | – | 다음 발표 안내 ⛔ 이름 불일치(§99-5 B1) | – |

---

### 99-2. 구술이 **덱에 없는 것을 준** 대목 — 이게 이 자료의 값어치다

아래는 전부 `[STT]` 다. **발표자 주장으로 인용 금지**, 우리 내부 가설 생성 전용.

#### (a) 계산과학의 성적표에 대한 자기평가 ★★
> `[STT 01:32]` 계산이 실험에 붙으면서 기대한 것은 **개발기간 단축**과 **실험 가이드라인 제시**였는데,
> **지금까지 눈에 띄는 성과는 없다** — 그 대신 **데이터가 쌓였고**, 그래서 빅데이터 → AI 로 넘어왔다.

우리 관점: **"계산이 실험을 앞서 이끈 사례가 드물다"** 는 자기평가를, 그 분야에서 20년 한 사람이
공개 강의에서 말했다. 우리 cascade 의 **정직성 장치**(vacuous 게이트·컷 지배 경고·"발굴력은 랜덤과
구별 불가" 자백)가 **분위기에 반하는 별종이 아니라 이 자기평가와 같은 계열**이라는 정황이다.
⛔ 다만 **인용 금지** — 우리가 "그분도 그렇게 말했다"를 논거로 쓰는 순간 §12-1 위반이다.

#### (b) AI 를 소재에 쓸 때의 3가지 병목 (덱은 그림만, 말이 항목화) ★
`[STT 05:54–06:55]`
1. **DB 편재성 + 생성방법 불일치** — 여러 DB 를 한꺼번에 쓰면 편향·불일치가 섞인다 → *normalizing* 이 관건
2. **descriptor 선택과 그 문턱** — 무엇을 기준으로 잡느냐에 따라 최종 결과가 달라진다
3. **자체 생성**하면 일관성은 얻지만 **양이 부족**하다

→ 이 셋은 우리가 이미 **실측으로 겪은 것**과 1:1 이다:
(1) MP e_hull 내부보정 vs 우리 QE 값 혼용 금지 · (2) **G5 percentile 0.25→1.00 에서 최종 0→11 = 컷 지배** ·
(3) 우리 자체 생성분 47종 → 302 cascade 로 넓혔지만 여전히 축별 결측이 많다(→ `D-2026-08-25-missing-axis-is-unknown-not-worst`).
**즉 우리 정직성 장치는 이 3병목에 대한 우리 쪽 대응물이다.** 이 대응 관계는 세미나에서 쓸 만하다.

#### (c) MD 를 못 쓰는 진짜 이유는 "느려서"가 아니라 **force field 가 없어서** ★
> `[STT 11:12]` DFT 는 슈뢰딩거 방정식을 풀어 전자 관련 물성까지 보지만 계산량 때문에 작은 계에만 쓴다.
> 고전 MD 는 뉴턴 방정식을 푸는데 **파라미터(force field)가 없으면 사용할 수가 없다** —
> "내가 관심 있는 것이 argyrodite 인데 argyrodite 의 force field 가 없으면 MD 를 못 쓴다."

교육적으로 정확한 프레이밍이다. 우리가 사람들에게 "왜 MLIP 냐"를 설명할 때 쓰던
"DFT 는 느리고 MD 는 부정확" 보다 **"MD 는 우리 물질에 대해 아예 존재하지 않는다"** 가 더 정직하다.

#### (d) 계면 결정화의 **기구** — 음이온이 먼저다 ★★
> `[STT 18:09]` S 가 Li 보다 크기 때문에 **큰 음이온이 먼저 close-packing** 을 한다.
> 비정질로 움직이다가 close-packing 핵생성이 일어나고, **빈 격자간(interstitial) 자리에 Li 가 들어가면서**
> 안정화되기 시작한다 → 그 결과가 Li₂S interphase.

덱 슬 18 은 **시점(1/7/10.5/11.5/20 ns)과 g(r)** 만 보여주고 "왜 S 가 먼저인가"는 안 적혀 있다.
이 한 문장이 그림을 기구로 바꾼다.
🔑 **우리 접점**: 우리 BVSE 채널 해석도 **음이온 부격자가 골격을 정하고 Li 가 그 사이를 흐른다**는
같은 그림 위에 서 있다. 그리고 오늘 우리가 세운 **골격 β 게이트**(골격이 rigid 여야 Li 확산 판정이
의미를 갖는다)가 바로 이 순서의 정량판이다.

#### (e) 반응 훈련셋을 **공정 순서**로 설계한다 ★★ 방법
> `[STT 20:11]` 합성(precursor → SE) → 수분 환경에 놓임 → 반응 → 최종 산물, **각 단계에 해당하는 구조**를
> 설계해 학습데이터에 넣는다. 가장 큰 문제는 **transition state 구조**인데, 반응이 매우 빠르고 한 번에
> 일어나서 시뮬레이션으로 얻기 어렵다 → **guided MD** 로 반응 경로를 인위적으로 유도해 구조를 얻는다.

덱 슬 21 의 5단 화살표(Pre-mixing → … → Products)와 `Guided MD` 박스(유도좌표 **D_S–H · D_O–P**)가
바로 이 절차의 그림이다. **T4(반응좌표 검증셋)의 방법 원본이 여기 있다.**

#### (f) 왜 새 결정구조를 찾아야 하는가 — 동기가 기술이 아니다 ★
> `[STT 14:13]` argyrodite 를 국내 배터리 3사가 많이 쓰지만 **원천기술은 해외**다.
> 우리 소재를 개발하려면 **기존과 완전히 다른 새 결정구조**를 찾아야 한다.

CSP 라인의 동기가 물리가 아니라 **IP 지형**이라는 것. 우리가 "CSP 는 안 한다"(host 고정 개질)로
결정한 근거(`symposium_2026_competitive_analysis.md` §4 하지 않기로)와 **문제설정이 다른 이유**가
여기서 명시적으로 확인된다 — 그들은 IP 공백을, 우리는 기존 host 의 개질 축을 푼다.

---

### 99-3. ★★★ Q&A — 우리 질문과 답 (이 세션의 최대 수확)

⚠ **Q&A 동의 상태 미상**(manifest `qa_consent_status: unknown`) → **외부 사용 금지**. 내부 기록 전용.
⚠ 아래는 STT 문자열을 **우리가 의역**한 것이다. 강조·태도는 살리지 않았다(README §4).

#### Q1 (26:02) — 질문자: **안용훈** (한양대, DFT 전공)
> FairChem 의 **UMA** 를 MLIP 로 쓰고 있다. 오늘 말씀에 나온 **SevenNet·MACE** 같은 오픈소스 모델들이
> 여럿 있는데, 교수님 연구실에서는 **어떤 계산에 어떤 모델**을 쓰시는지, 각 모델이 **어떤 계산에
> 특화**되어 있는지 알 수 있는지.

> ⚠ STT 는 소속을 `한양대학교 인동중학교 연구실`, 이름을 `안용희` 로 적었다 — 둘 다 오전사(§99-5 A14).

#### A1 (26:50–27:53) — **두 갈래로 분류한다** ★★★

| | **MTP** (Moment Tensor Potential) | **universal potential** (M3GNet · SevenNet · MACE …) |
|---|---|---|
| 이 랩의 사용 | **주력** | 최근 도입 |
| 덱 대응 | 슬 8 *Descriptor based MTP* | 슬 8 *GNN based uMLIP* |
| `[STT]` 용도 | **동력학적(kinetic) 물성** | **static 물성** |
| `[STT]` 이유 | **훨씬 빠르다** | **"파라미터 개수가 워낙 많다"** |

그리고 **학생 지도 원칙**을 하나 덧붙였다:

> `[STT 26:50]` MLIP 를 학습시키려면 **어차피 DFT 계산을 해야 한다**. 그래서
> **"DFT 로 끝날 수 있는 연구에 MLIP 를 만드는 것은 아무 의미가 없다"** 고 학생들에게 말한다.
> 내가 MLIP 를 적용하는 기준은 **동력학을 볼 때**다.

##### ⚠ 이 답의 **정확한 뜻은 STT 만으로 결정되지 않는다** — 두 읽기
| 읽기 | 문장 | 함의 |
|---|---|---|
| **(i) 속도** | 파라미터가 많아 **스텝당 비용이 크다** → ns 급 MD 를 못 돌린다 | uMLIP 의 문제는 **도달 못 하는 시간창** |
| **(ii) PES 품질** | 파라미터가 많아/평형 근처에 치우쳐 **PES 가 무르다(softening)** → 동역학이 틀린다 | uMLIP 의 문제는 **틀린 궤적** |

`stt_status = ambiguous`. **덱은 (ii) 를 독립적으로 지지한다** — 슬 8 의
`DFT PES ──softening──▶ uMLIP PES` 화살표와 범례(*노란 점 = 평형 근처 훈련점 · 빨간 점 = 보강이 필요한
고에너지 상태*)가 그것이다. 그러나 **A1 의 문장이 (ii) 를 말한 것인지는 음성 없이 확정 불가**.
→ §99-6 Q-T2 로 열어둔다.

🔑 **우리에게는 두 읽기가 같은 곳에 떨어진다** — 우리 b2o3 **골격 β ≥ 0.60 @ 700 K** 는
**universal potential 로 얻은 동력학 결과**이고, A1 은 그 조합을 권하지 않는다.
⛔ 그러나 이것은 **정황이지 증거가 아니다**. 우리 판정의 근거는 여전히 우리 데이터
(modelc 12/12 rigid · lpsocl 12/12 rigid · b2o3 만 700 K 부터 무너짐)이며, 물리적 근거는
**T1b(vdW DFT 대조)** 로 세워야 한다. "이상욱 교수님이 그렇게 말했다"는 논거가 아니다(§12-1).

##### 덱이 주는 **숫자로 된 대조** (참고 — 계가 다르므로 직접 비교 아님)
| | 엔진 | MAE(E) | MAE(F) | 대상 |
|---|---|---|---|---|
| 슬 17 | **MTP** (자체학습, 5,400 구조) | Li 11 · **LPSCl 5** meV/atom | 0.083 · **0.111** eV/Å | Li \| LPSCl 계면 |
| 슬 14 | **MTP** (벌크) | **2.88** meV/atom | **0.073** eV/Å | Li₆PS₅Cl 벌크 |
| 슬 22 | **SevenNet** (fine-tuned) | **8.8** meV/atom | **0.57** eV/Å | LPSCl + H₂O 가수분해 |

⚠ **이 표로 "uMLIP 이 8배 부정확하다"를 말하면 안 된다** — 슬 22 는 **H₂O 가 붙은 반응계**로
난이도가 다르고, 훈련셋도 다르다. 말할 수 있는 것은 **"같은 랩이 같은 물질군에서 보고한 값의
자릿수"** 까지다. 그래도 힘 MAE 가 **0.073 → 0.57 eV/Å (7.8×)** 라는 것은,
**힘이 곧 동역학**이라는 점에서 A1 의 분업을 이해할 수 있게 해 준다.

#### Q2 (28:01) — 좌장
> 초반에 스케일마다 다른 기술이 필요하고 그 사이 **bridging** 이 중요하다고 하셨는데, 앞으로
> AI 가 발전하면 DFT 에서 시작해 **셀 단위까지 확장되는 하나의 통합된** 체계가 가능하겠는가.

#### A2 (28:47) ★★
> `[STT]` **10여 년 전부터 시뮬레이션 하는 사람들의 꿈**이었고, 아직 요원하다.
> **내 스케일과 이용민 교수님 스케일은 거리가 너무 멀다.** 그게 메꿔지지 않으면 셀 단위까지는
> 절대 갈 수 없다. **AI 가 발전해도 금방 해결되리라고 보지 않는다.**
> 적어도 DFT 로 못 하던 **grain boundary 나 particle 정도까지 확장**하는 것도 큰 의미가 있다.

🔑 **우리 M5/T8(P2D 파라미터 export) 의 온도를 낮춰 주는 답이다.** 우리는 σ·Ea·C_ij·ESW 를
셀 모델 입력으로 넘기는 것을 접점으로 잡았는데, **원자 스케일 쪽 당사자는 그 다리를 "요원하다"고
본다.** 우리 목표를 "통합"이 아니라 **"한 칸 위(입계·입자)까지"** 로 잡는 편이 방어 가능하다.
동시에 이건 **문장혁 랩과의 상보 구도가 여전히 유효한 이유**이기도 하다 — 다리를 한 랩이 혼자
놓으려 하지 않는다는 뜻이니까.

#### Q3 (29:54) — UNIST, `[STT]` 정승빈 ⚠ 이름 미확인(§99-5 D)
> 도메인 지식 중심으로 공부하는 학생이 AI/ML 적용 논문을 읽고 참고하려면 어떤 **수학적 배경이나
> 공부**를 해 두는 게 도움이 되겠는가.

#### A3 (30:34) ★★
> `[STT]` **ChatGPT 나 Claude 같은 모델이 나오기 전이라면** 수학 공부, 파이썬 코딩 정도는 해야 한다고
> 말했을 텐데 **지금은 필요 없다.** 중요한 것은 **그 도구를 얼마나 잘 활용할 수 있느냐**이고,
> **그보다 더 중요한 것이 도메인 지식**이다. 도메인 지식을 가지고 "어떤 기능의 코드로 무엇을 하고 싶다"를
> **맥락에 맞게 질문만 잘 하면** 아주 좋은 코드를 만들어 준다. **만들어준 코드를 이해하고 잘 활용하는 것**이
> 더 중요하지 않을까 생각한다.

우리 repo 의 운영 방식(도메인 규율은 `CLAUDE.md`·`kb/` 에 사람이 박고, 코드는 LLM 이 쓰고,
`--selftest`·`convention_check.py` 로 사람이 검증)이 이 답과 같은 모양이다.
⛔ 인용 금지지만, **세미나에서 우리 워크플로를 정당화할 때 참고 배경**은 된다.

---

### 99-4. 전문가 관찰 — 덱 지지(4A) / STT 전용(4B)

#### 4A. 덱이 **독립적으로** 지지 — 내용 인용 가능(문구는 우리 의역)
| # | 명제 | 덱 근거 |
|---|---|---|
| A1 | uMLIP 의 PES 는 평형 근처 훈련점에 치우쳐 고에너지 영역에서 **물러진다**; 이를 fine-tuning 으로 되돌린다 | 슬 8 화살표 + 범례 |
| A2 | MLIP 은 **descriptor 기반(MTP)** 과 **GNN 기반(uMLIP: M3GNet/CHGNet/SevenNet/MACE)** 두 계열이다 | 슬 8 하단 2행 |
| A3 | 반응을 보려면 **TS 를 포함한 반응좌표 훈련셋**이 필요하다 | 슬 21 |
| A4 | 계면 SEI 는 **≈11 nm 에서 수렴**하고 실험 cryo-TEM **~12 nm** 와 두께 스케일이 맞는다 | 슬 19 + ACS EL 2022, 7, 3064 |
| A5 | 계면 결정영역의 Li 는 모체보다 **느리다**(0.4 vs 1.1 ×10⁻⁷ cm²/s, 비 0.36) | 슬 18 |
| A6 | 학습–시뮬 규모비: **200 atom 급 학습 → 6,000 atom 급 시뮬** | 슬 16–18 + `[STT 16:12]` |

#### 4B. STT 에만 있음 — `allowed_use: hypothesis_generation_only`
| # | 가설 | 시각 |
|---|---|---|
| B1 | 계산과학이 실험을 앞서 이끈 **눈에 띄는 성과는 아직 없다**(자기평가) | 01:32 |
| B2 | AI×소재의 3병목 = DB 편재성/불일치 · descriptor 문턱 · 자체생성 데이터 부족 | 05:54 |
| B3 | MD 를 못 쓰는 1차 이유는 **해당 물질의 force field 부재** | 11:12 |
| B4 | 계면 결정화는 **큰 음이온 close-packing 이 먼저**, Li 는 격자간에 나중 | 18:09 |
| B5 | **MTP = 동력학 / uMLIP = static** 분업 (⚠ 이유는 ambiguous, §99-3 A1) | 26:50 |
| B6 | **DFT 로 끝나는 연구에 MLIP 를 만드는 것은 무의미** (학생 지도 원칙) | 26:50 |
| B7 | 멀티스케일 통합은 **10년째 꿈이고 아직 요원** — AI 로도 곧 해결 안 된다 | 28:47 |
| B8 | 지금 필요한 기초는 수학·코딩이 아니라 **도메인 지식 + LLM 활용력** | 30:34 |
| B9 | CSP 의 동기는 물리가 아니라 **원천기술(IP) 공백** | 14:13 |

#### 4C. 판독 메타 — 구술이 얇은 구간
- **슬 3–4 (DFT 기반 LIB 연구)** — 40초에 5개 주제를 스쳐서 어느 그림인지 특정 불가(`–`).
- **슬 25–26 (섹션 표지·metastable 정의)** — 비유(다이아몬드·xylene)만 있고 슬 29 의 **3기술자는 언급 없음**.
  → 덱 슬 29 의 `packing ratio α · Li–S₄ 부피 · CSM` 은 **구술로 보강되지 않았다**.
- **슬 30 (PyBaMM+ML SOC)** — 20초. §12-7 판정(인용 가치 없음) 유지.

---

### 99-5. STT 교정표 (README §4b 여섯 갈래)

#### A. 확정 교정 — 덱/문맥으로 확인, 본문에서 정정형 사용
| # | STT | 정정 | 근거 |
|---|---|---|---|
| A1 | `DT` `DMT` `dot` `TMT` `d 레벨` `itp` | **DFT** | 전 구간 문맥 |
| A2 | `아지로다이트` `아지노다이트` `아지바디` | **argyrodite** | 덱 |
| A3 | `그놈` | **GNoME** | 슬 6 |
| A4 | `페어 캠` | **FairChem** | 질문 문맥 |
| A5 | `7 net` `세븐 넷` | **SevenNet** | 슬 8 |
| A6 | `mac` `MC 지넷` | **MACE** / **M3GNet** | 슬 8 |
| A7 | `모멘트 텐서/댄서 포텐셜` | **MTP** (Moment Tensor Potential) | 슬 8 |
| A8 | `파이 왕` `온리 모델` | **PyBaMM** (오픈소스 셀 모델) | 슬 30 |
| A9 | `슈레더 이케이션` | **Schrödinger equation** | 슬 9 |
| A10 | `올리키라 나이네믹스` `유터니얼 리케이션` | **(classical) molecular dynamics** / **Newtonian equation** | 슬 9 |
| A11 | `포스필드` | **force field** | 슬 9 |
| A12 | `인터페이지` | **interphase** | 슬 18 |
| A13 | `컴퓨레이션 스페이스` | **configuration space** | 슬 14 |
| A14 | `안용희` · `한양대학교 인동중학교 연구실` | **안용훈** · 한양대 (연구실명 오전사) | 본인 |
| A15 | `크리스탈 스트럭터 프레덱션` | **CSP** | 슬 27 |
| A16 | `일본이 가장 안전합니다` | **1번이 가장 안정**하다 | 슬 28 `Relative Stability` 1–10 |
| A17 | `PI s4` | **PS₄** | 슬 28 |
| A18 | `이혼 전도` | **이온 전도** | 문맥 |
| A19 | `CHP` (자일렌) | **C₈H₁₀** | 문맥 |
| A20 | `펜시브 러닝` | **passive learning** | 슬 16 |
| A21 | `11층 나노 세컨디즘` | **11.5 ns** | 슬 18 우측 소패널 라벨 |

#### B. ⛔ 불일치 — 판정하고 근거를 남긴다
| # | 건 | 판정 |
|---|---|---|
| **B1** | STT 31:44 은 다음 발표자를 `중앙대학교 **김장현** 교수님 · AI 기반 배터리 자동화` 라고 함. 우리 정본은 **문장혁**(중앙대, BEARS) — `litdb/talks/moon2026_cau_llm_agent_battery_automation.md` | `stt_status = ambiguous` · **미해결**. 이 PDF 는 **이상욱 섹션 18 pp 만** 이라 자료집 목차로 확인 불가 → §99-6 Q-T1 |
| **B2** | 🔴 **우리 기록 정정** — 본 digest §6 이 계면 셀을 `3 nm × (10 nm 방향)` 이라 적었는데, 슬 18 좌측 화살표를 **9× 확대 재판독**하니 **`6nm`(Li metal) · `10nm`(LPSCl)** 이다. STT 도 독립적으로 `6나노 16나노`(=6+10) 라고 말한다 | ✅ **정정 확정**: **Li 6 nm + LPSCl 10 nm = 총 16 nm**. §6 을 고쳤다 |

#### C. 구두 근사·실언 — **덱 값을 쓴다** (해결된 건)
| # | STT | 덱 정본 |
|---|---|---|
| C1 | `6나노 16나노` | 6 nm + 10 nm = **16 nm** (B2) |
| C2 | `이온 전도도 **만 배**` (CSP edge vs corner) | 덱 슬 28 `10⁻⁴ → 2.4 mS/cm` = 2.4×10⁴ 배. **⛔ 그런데 덱 값 자체가 논문에 없다** — 정본은 **계산 2자릿수**(§14) |
| C3 | `한 11나노 정도의 컨버즈` | 슬 19 **≈11 nm @ 50 ns** |
| C4 | `실험적으로 12나노 정도로 관측` | 슬 19 인용그림 **~12 nm** (ACS EL 2022, 7, 3064, 25 °C) |
| C5 | `한 200개 어텀` / `6천 개` | 슬 16–18 학습 **200 atom 급** → 시뮬 **6,000 atom 급** |
| C6 | `1번부터 10번까지` | 슬 28 **rank 1–10** |

#### D. 추정 — ⛔ **인용 금지**, 미해결로 남긴다
| # | STT | 후보 | 왜 못 닫나 |
|---|---|---|---|
| D1 | `파라테스` `파나케스` (21:22 · 22:30) | **hydrolysis**? / **P–S dissociation**? | 문맥은 "P–S 약화 → ○○ 발생 / Sn 넣으면 ○○ 안 생김". 덱 슬 23–24 에 대응 단어가 인쇄돼 있지 않다 |
| D2 | `인시이션` (21:22) | **initiation**? **nucleation**? | 위와 같은 문장 |
| D3 | `그게 흔히 **포도 정도**로` (23:27) | `4 order 정도`? | 판독 불가. **C2 와 같은 수치를 말하는 중일 수 있어 더 위험** |
| D4 | `정승빈` (UNIST, 29:46) | — | 이름 확인 수단 없음 |
| D5 | `6나노 16나노 정도는 되지만` 앞의 `이용민 교수님 시스템에 비해서는 상당히 작았습니다` | — | 비교 대상 규모 불명 |
| D6 | `**11층** 나노 세컨디즘` → A21 로 정정했으나 **"이상이 되면"** 의 경계값인지 그 프레임 라벨인지 | — | 슬 18 은 11.5 ns 프레임 라벨. 문장의 "이상" 은 구술 표현 |

#### E. 덱 자체 오류 (우리 전사 오류 아님) — §12 에 이미 등재
`±0.05 %` strain 오타(슬 14) · 힘 MAE 단위 `meV/Å`(슬 14, 실제 eV/Å) · `10⁻⁴→2.4 mS/cm` 비율(논문 미지지)

#### F. 덱 내부 표기 흔들림
슬라이드 번호가 `7/50` `8/24` `14/31` `17/31` `22/31` `28/50` 로 **세 마스터가 섞여** 있다.
→ 인용할 때는 **PDF 페이지 + 덱 표기**를 병기한다(본 digest §2 표가 그 환산표다).

---

### 99-6. 이 구술이 **닫은 것 / 못 닫은 것**

| # | 질문 | 상태 |
|---|---|---|
| ~~Q5~~ | Adv. Energy Mater. revision 이 argyrodite 인가 BH₄ 인가 | ⏳ **못 닫음** — 구술에 후속 논문 언급 자체가 없다 |
| Q2 | Li\|LPSCl 계면 MD 가 어느 무질서 배열을 썼나 | ⏳ **못 닫음** — 구술도 배열을 말하지 않는다 |
| Q4 | 가수분해 H₂S **발생량** 정량 | ⏳ **못 닫음** — 구술은 기구만(H 침투·Sn scavenging), 수량 없음 |
| **Q-T1** 🆕 | 다음 발표자가 **문장혁**인가 **김장현**인가 (§99-5 B1) | ⏳ 자료집 **목차 페이지**가 필요 |
| **Q-T2** 🆕 | A1 의 "파라미터가 많아서"가 **속도**인가 **PES 품질**인가 | ⏳ **음성 재청취 또는 본인 확인**이 필요. 우리 T1b 해석에 직결 |
| **Q-T3** 🆕 | D1/D2 의 `파라테스`/`인시이션` 실제 단어 | ⏳ 음성 필요 |

---

### 99-7. ⛔ 인용 금지 (이 절에서 추가되는 것)

1. **§99-3 Q&A 전체** — 동의 미상. 내부 기록 전용.
2. **B1–B9 (STT 전용 가설)** — "이상욱 교수님이 …라고 했다" 형태 **전면 금지**.
3. **"uMLIP 은 동역학에 못 쓴다"** — A1 을 이렇게 요약하면 **우리가 만든 문장**이 된다.
   허용되는 최대치: *"덱 슬 8 은 uMLIP PES 의 softening 을 명시하고, fine-tuning 을 그 대응으로 제시한다"* (덱 인용).
4. **MTP 2.88 vs SevenNet 8.8 meV/atom 을 나란히 놓고 우열**로 쓰는 것 — 계·훈련셋이 다르다(§99-3).
5. **`만 배` / `4자릿수`** — C2·D3. 정본은 **계산 2자릿수**.

---

### 99-8. 안 본 것 / 못 하는 것

**본 것**: STT 전문 261행 전수 · 덱 슬라이드 재확인 9장(6a·6b·9b·11a·11b·12a·13a·13b·16b) + 9× 확대 1건(슬 18 치수).
**안 본 것**: 슬 1–5·10–12·15–16·19하·20·23–27·29–31 의 **오늘자 재확인**(2026-08-03 전수 판독 기록에 의존).
음성 파일. 자료집의 이상욱 섹션 **바깥** 페이지(목차·다른 연사).
**못 하는 것**: 화자 분리 정확성 보증 · `[말]` 승격 · Q&A 외부 사용 · D1–D6 확정.

---

### 99-9. 📌 **사용자에게 요청 — litdb 에 없어서 내가 필요한 것**

이 강의를 세미나로 만들 때 **우리가 근거를 댈 수 없는 지점**만 골랐다. 순위는 효용순.

| 순위 | 무엇 | 왜 필요한가 | 지금 상태 |
|---|---|---|---|
| **1** | **Adv. Funct. Mater.** (revision) — argyrodite **가수분해 SevenNet** 논문 | 슬 21–24 의 정본. **guided MD 유도좌표 정의 · SevenNet fine-tune 조건 · H₂S 정량 · Sn 의 ΔE_a 0.28 eV** 가 전부 여기 있다. 우리 **T2(ICOHP 기술자)** 와 **Q4** 가 이것 하나로 닫힌다 | ⛔ **없음** (위시리스트 #2, 유일하게 남은 3부작 공백) |
| **2** | **자료집 목차 페이지** (이상욱 섹션 앞뒤 1–2 pp) | §99-5 B1 (다음 발표자 이름) + 세션 번호·발표 시각 확정. **1분이면 되는 건** | ⛔ 이 PDF 는 내지 18 pp 만 |
| **3** | **Shapeev 2016** *Moment Tensor Potentials* (Multiscale Model. Simul. 14, 1153) + **Novikov 2021** *MLIP package* (Mach. Learn.: Sci. Technol. 2, 025002) | MTP 의 **기저·γ(maxvol/D-optimality) 원정의**. 지금 우리는 γ 를 **덱 슬 16 숫자로만** 안다(γ_select 2 / γ_break 10↔5↔2). **T1(외삽 대리지표)** 을 설계하려면 원정의가 있어야 "UMA 에는 왜 이식 불가한가"를 정확히 쓸 수 있다 | ⛔ 없음 (인용만 6곳) |
| **4** | **Merchant 2023 GNoME** (Nature 624, 80) | 슬 6 = 강의 서사의 출발점(`[STT 08:02]` 2.2 M / 38만). 지금은 **다른 digest 안의 참조로만** 존재 | ⛔ 자체 digest 없음 |
| **5** | **Park 2024 SevenNet** (J. Chem. Theory Comput. 20, 4857) | 슬 8·22 의 엔진. **우리 UMA 와 같은 GNN 계열**이라 "softening 이 GNN 공통인가 모델별인가"를 가르는 데 필요 → **T1b 의 대조군** | ⛔ 없음 (언급 8곳) |
| 6 | **Luo 2022** *ACS Energy Lett.* **7, 3064–3071** | 슬 19 의 **실험 앵커(~12 nm cryo-TEM)**. 우리가 Li\|LPSCl MD(T3)를 하면 **그대로 우리 대조군**이 된다 | ⛔ 없음 (수치만 전재) |
| 7 | **Adv. Energy Mater.** (revision) — Dynamic properties 후속 | **Q5**(config-variance 오차막대 보강 여부) — 우리 §3-2 최강 카드의 **유효범위**가 여기 걸려 있다 | ⛔ 없음 |

> ✅ **이미 있어서 요청하지 않는 것**: Nano Energy 2024(무질서·GB MTP) · SSRN 6020397(Li 계면 MTP) ·
> JACS 2025 147, 47381(CSP 준안정) · Nano Convergence 2026 13, 27(코팅 스크리닝) ·
> lee2024(다성분 argyrodite MTP) · UMA 원논문 · PET-MAD.
> **1·2번만 받아도 이 강의의 미해결이 절반으로 준다.**
>
> 📥 **파일명·slug·앵커·양방향 링크 규약은 §99-10 · §99-11** (논문 에이전트가 읽는 표).

---

### 99-10. 📥 논문 에이전트 인입 대기열 — **이 talk 과 관계를 맺어야 하는 6건**

> 2026-08-26 확정. 사용자가 아래 6건을 `litdb/inbox/` 로 넣기로 했다.
> **litdb-curator 는 이 표를 읽고 digest 를 만든 뒤 §99-11 의 양방향 링크를 반드시 건다.**
>
> ⚠ **서지 신뢰도를 열로 표시했다** — `✅확인` = 우리 digest/덱에 적혀 있어 재확인 가능,
> `⚠재구성` = 내가 기억에서 복원한 것이라 **표지로 대조하기 전에는 인용하지 말 것**.
> 파일을 받으면 curator 가 **표지에서 서지를 다시 읽어 이 표를 정정**한다.

| # | inbox 파일명 (이대로 주면 좋다) | 예상 slug | 서지 | 신뢰 |
|---|---|---|---|---|
| **1** | `66. Kim2026_Argyrodite_Hydrolysis_SevenNet_Sn.pdf`<br>`66. Sup) …` | `kim2026_argyrodite_hydrolysis_sevennet_sn` ⚠저자·연도는 표지 보고 확정 | **Adv. Funct. Mater.**, 이상욱 랩. 덱 표기 *"revision"*(2026-07 시점) → **이미 출판됐을 수 있다**. 검색어: `argyrodite hydrolysis machine learning potential H2S Sn doping Sungkyunkwan` / `Li6PS5Cl H2O reactive MD SevenNet` | ⚠서지 미상 |
| **2** | `lee2026_skku_program_toc.pdf` → `litdb/talks/_transcripts/` (논문 아님) | — | 심포지엄 **자료집 목차 페이지**. 이상욱 섹션(pp.279–296) 앞뒤 1–2 pp | ✅ |
| **3a** | `67. Shapeev2016_Moment_Tensor_Potentials.pdf` | `shapeev2016_moment_tensor_potentials` | A. V. Shapeev, *Multiscale Model. Simul.* **2016**, 14(3), 1153–1173 · DOI `10.1137/15M1054183` · arXiv 1512.06054 | ⚠재구성 (연도·저널은 ✅) |
| **3b** | `68. Gubaev2019_Active_Learning_Alloy_MTP.pdf` | `gubaev2019_active_learning_alloy_mtp` | Gubaev·Podryabinkin·Hart·Shapeev, *Comput. Mater. Sci.* **156** (2019) **148–156** — **γ(maxvol/D-optimality) 원전** | ✅ 권·쪽은 `kim2026_li_argyrodite_sei_reactive_md` ref [39] 에 기록됨 |
| **3c** | `69. Novikov2021_MLIP_Package.pdf` | `novikov2021_mlip_package_mpi_active_learning` | Novikov·Gubaev·Podryabinkin·Shapeev, *Mach. Learn.: Sci. Technol.* **2021**, 2, 025002 · DOI `10.1088/2632-2153/abc9fe` | ⚠재구성 |
| **4** | `70. Merchant2023_GNoME_Scaling_Deep_Learning.pdf` | `merchant2023_gnome_scaling_deep_learning_discovery` | Merchant·Batzner·Schoenholz·Aykol·Cheon·Cubuk, *Nature* **2023**, 624, 80–85 · DOI `10.1038/s41586-023-06735-9` | ⚠재구성 (Nature 2023·GNoME 은 ✅ — `kim2025_csp…` ref 35) |
| **5** | `71. Park2024_SevenNet_Parallel_GNN_MD.pdf` | `park2024_sevennet_parallel_gnn_md` | Park·Kim·Hwang·Han (SNU), *J. Chem. Theory Comput.* **2024**, 20, 4857–4868 · DOI `10.1021/acs.jctc.4c00190` | ⚠재구성 |
| **6** | `72. Luo2022_CryoTEM_Li_Dendrite_Sulfide_Interphase.pdf` | `luo2022_cryotem_li_dendrite_sulfide_interphase` | *ACS Energy Lett.* **2022**, 7, **3064–3071** — "single Li dendrite ‖ sulfide electrolyte" **cryo-TEM interphase** | ✅ 권·쪽 (덱 슬 19 + SSRN ref [49] 이중 확인) · ⚠제목·저자 재구성 |

#### 각 편이 **이 talk 의 어디에 매달리나** (curator 가 걸 앵커)

| # | talk 앵커 | 닫는 질문 / 여는 작업 |
|---|---|---|
| **1** | §7(슬 21–24) · §99-2(e) guided MD · §99-4 A3 | **Q4**(H₂S 정량) 종결 · **T2**(ICOHP 양성자화 기술자) 방법 원본 확보 · `air_hsab` 정성 tier 를 정량으로 교체할 수 있는지 판정 |
| **2** | §99-5 **B1** · §99-6 **Q-T1** | 다음 발표자 이름(문장혁 ↔ STT `김장현`) 확정 · 세션 번호·발표 시각 확정 |
| **3a·3b** | §5b(슬 16 γ_select 2 / γ_break 10↔5↔2) · §99-3 **A1** | **T1** 설계 — "γ 를 UMA 에 왜 못 옮기나"를 **원정의로** 쓸 수 있게 된다(지금은 덱 숫자만) |
| **3c** | §5b · §5c(5,400 구조) | MTP **훈련 실무**(w_e:w_f:w_s · R_cut · lev_max · 비용) 원본 |
| **4** | §9(슬 6) · §99-1 08:02 | 강의 서사의 출발점. **"MLIP 없이는 불가능했다"** 주장의 실물 근거 |
| **5** | §7a(슬 22) · §99-3 A1 · §99-4 **A1** | ★ **T1b 대조군** — SevenNet 은 **우리 UMA 와 같은 GNN 계열**이다. PES softening 이 **GNN 공통 성질**인지 **모델별**인지를 가르는 유일한 대조 |
| **6** | §6(슬 19) · §99-4 **A4** · §12-6 | **T3** 실험 앵커(~12 nm cryo-TEM) 확보 — 우리가 Li\|LPSCl MD 를 돌리면 그대로 대조군 |

#### ⛔ curator 가 **하지 말아야 할 것**

1. **덱/구술 수치를 논문 digest 에 정본으로 옮기지 않는다.** 이 talk 은 `citable = no` 다.
   방향은 **논문 → talk** 이지 talk → 논문이 아니다(논문이 이기고, talk 의 오기를 정정한다).
2. **#3a–#5 는 방법론 원전이라 `comparison_vs_ours.md` 의 물성 4축 표에 넣지 않는다.**
   물성값이 없다 — 넣으면 표가 무의미해진다. `🔧 방법 원전` 블록으로 따로 둔다.
3. **#6 은 실험 논문이다.** 우리 계산값과 같은 줄에 놓지 말고 **앵커(대조 대상)** 로만 쓴다.
4. **#1 의 σ·H₂S 절대값을 우리 db 로 이식하지 않는다** — 방법(functional·셀·시간창)이 다르다.

---

### 99-11. 🔗 양방향 링크 규약 (talk ↔ paper)

논문이 들어올 때마다 **양쪽을 다 고친다.** 한쪽만 고치면 6개월 뒤에 "이 덱에 그 얘기 있었는데
논문이 어디 갔지" 가 반복된다.

**① 논문 digest 쪽** — 머리 블록에 한 줄:
```
> 🎤 **관련 발표**: `talks/lee2026_skku_mlip_materials_design.md` §<절> (슬 <n>) ·
>   ⛔ 그 talk 은 citable=no — **이 논문이 정본이고, 덱/구술과 어긋나면 이 논문이 이긴다**
```

**② 이 talk 쪽** — §99-10 표의 해당 행을 `~~#n~~ ✅` 로 긋고 slug 를 적는다. 그리고
**덱/구술과 어긋난 것이 나오면 §12(주의/한계) 또는 §99-5 E 에 정정으로 남긴다.**
(선례: `kim2025_csp…` 가 덱의 `10⁻⁴→2.4 mS/cm` 를 부인해 §14 에 인용금지가 생겼다.)

**③ `INDEX.md`** — 논문 행 설명 끝에 `🎤 talks/lee2026_skku… 슬 <n> 의 정본` 을 붙인다
(기존 `kim2026_hts_li3sc2po43…` 행이 그 형식이다).

**④ `comparison_vs_ours.md`** — 물성값이 있는 편(#1·#6)만. #3a–#5 는 `🔧 방법 원전` 으로.
