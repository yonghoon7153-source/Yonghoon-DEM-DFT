# 기계학습 포텐셜 기반 소재 물성 해석 및 설계 (MLIP-Based Materials Analysis and Design) — 이상욱 (성균관대)

> slug `lee2026_skku_mlip_materials_design` · type `talk` · 발표 2026-08-21 (2026년도 전지기술 심포지엄, 한국전기화학회, 기술세션 3-3) ·
> 발표자 **Sang Uck Lee**, School of Chemical Engineering, Sungkyunkwan University (**CMS Lab** — Computational Materials Science) ·
> PDF 18 pp (자료집 pp. 279–296), 슬라이드 31장 · digested 2026-07-28 · status ✅ (덱), ⏳ 구술 txt 대기
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
| **Cathode interface RXN** | SevenNet | **17,233 Li·P·S·O 결정구조 @ MP** → electro-/mechanical-/electronic-stability → Li-ion conductivity → best candidates. **코팅 소재 스크리닝** | **Nano Converg. 2026, 13, 27** |
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
(1) 6 characteristic configurations, DFT-최적화 @ PBE
(2) Lattice strain = ±0.05%, 0                      ← 덱 표기 그대로 (아마 ±5%의 오기, §12 참조)
(3) Short-time AIMD @ 300–1200 K, 0.1 ps 간격 스냅샷  → 7,200 structures
(4) Single point DFT, functional 3종: ① PBE ② optB88 ③ PBE+D3damp
(5) MTP 훈련 (R_cut = 5 Å, lev = 100:1 표기)
(6) MTP로 MD: 100 ps NVT 승온 → 10 ns NPT → σ_ionic 획득
```
정확도 회귀 3패널: **MAE 2.09 meV/atom (에너지) · 0.073 meV/Å (힘)** — 힘 단위가 meV/Å로 적혀
있는데 이는 `papers/kim2024_...` 감사에서 **이미 확인된 단위 오기**(실제 eV/Å)의 덱 재발이다.

> 🔑 (4)의 **functional 3종 병렬 학습**이 그 그룹의 서명 기법이다. Kim 2024 논문에서
> **optB88-vdW만 site-disorder 의존성을 재현**하고 PBE·PBE-D3는 100%-ordered를 3.7 mS/cm로
> 오판한다는 결론이 여기서 나온다. → **"MLIP σ 절대값은 훈련 functional의 각인"**.
> 우리 "UMA 절대 σ 인용 금지" 규율의 외부 정면 증거로 이미 등록돼 있다.

### 5b. 계면용 훈련셋 (슬 16) — passive + active learning

**훈련 구조 3계층**
- **Bulk**: Li₆PS₅Cl / Li₆PS₅Cl **50% disordered** / Li bcc (3×3×3)
- **Slab**: LPSCl(100) / LPSCl 50%-disordered(100) / Li bcc(100)
- **Interface**: LPSCl(100) ‖ LPSCl 50%-disordered(100) ‖ Li(100)

**Passive learning**: DFT(PBE) 구조최적화 → Bulk AIMD 5 ps (300–1200 K, 200 K 간격, 0.1 ps 스냅샷)
+ strain −5…+5 % (2.5 % 간격, 5 ps 간격 스냅샷) + Slab AIMD 10 ps → **DFT(optB88) 재계산**
→ MTP 훈련·선별 (R_cut = 5, lev_max = 12)

**Active learning**: MTP-MD @ 300/500/700/900 K → **γ_select / γ_break 로 구조 선별**
→ DFT(optB88) → 재훈련 → 수렴 MTP (η = 0.91, **MAE_E ≈ 10 meV/atom**, MAE_F ≈ 0.5 eV/Å)

**ΔE_MTP vs ΔE_DFT 산점도에 `γ_select`–`γ_break` 사이를 "Accurate region"으로 명시** ★★
→ **외삽 등급(extrapolation grade) 관리**. 이것이 이 덱에서 우리가 가져올 1순위 항목이다.

**스케일 전환**: 훈련은 **atoms < 200**, 생산 MD는 **atoms > 6,000**.

### 5c. 훈련셋 규모 (슬 17)

| 물질 | 유형 | 개수 |
|---|---|---|
| Li | Bulk (0.2 ps 간격) | 5 T × 150 = 750 |
| | Bulk (2 ps 간격, ±10 % strain) | 5 T × 10 × 11 = 550 |
| | Slab (100) (0.5 ps 간격) | 5 T × 100 = 500 |
| LPSCl **0 % X@4a4c** | 위와 동일 3종 | 1,800 |
| LPSCl **50 % X@4a4c** | 위와 동일 3종 | 1,800 |
| **합계** | | **5,400** |

온도 5점 = 300 / 600 / 900 / 1200 / 2000 K.
**정확도**: Li — 11 meV/atom · 0.063 eV/Å · LPSCl — **5 meV/atom · 0.111 eV/Å**.
1 ns DFT-vs-MTP 에너지 궤적이 겹침(초기 0.2 ns 완화 구간 제외).

무질서 배열 도해 6종 표기: `0 % X in 4a (P-43m)` / `25 % (R3m)` / `50 %` / `100 % (F-43m)` / `50 % (R3m)` …
→ Kim 2024 논문의 6배열과 동일 세트.

---

## 6. 음극 계면 반응 MD ★★ (p.11–12 슬 18–19)

**"Long-time & Large-scale Simulation + Interface Reaction Dynamics"**

- 셀: LPSCl 층 + Li 층, 3 nm × (10 nm 방향), **0 → 10 ns → 20 ns** 진화, SEI 영역 형성
- **계면 결정영역이 Li₂S로 동정**: g(r)가 Li₂S 기준 곡선과 일치, (100)/(010)/(001) 면 도해
- **영역분해 MSD** (11 ns 시점):
  - **Li (결정영역) D ≈ 0.4 × 10⁻⁶ cm²/s**
  - **Li (잔여 벌크) D ≈ 1.1 × 10⁻⁶ cm²/s**
  → 생성된 interphase가 **모체보다 느리다**(약 1/3)
- **50 ns까지 확장** (슬 19): interphase 두께 **≈ 11 nm**
- **실험 대조**: *ACS Energy Lett.* **2022, 7, 3064–3071** 의 TEM interphase layer (25 °C vs 80 °C)와
  "well agreement" 주장

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
하위 셋: `General purpose` / `LPSC(100)` / `LPSC(100)+H₂O` / **`Guided MD`** (D_S–H, D_O–H 좌표로 유도)
/ `LPSC "S ↔ O"` (S–O 교환 경로)

**엔진 정확도** (SevenNet, 슬 22): **8.8 meV/atom · 0.57 eV/Å · 0.35 kbar**. MD 500 스텝 에너지 궤적이 DFT와 일치.

### 7b. LPSCl vs H₃O⁺ + OH⁻ + H₂O (슬 23)

- 계: **LPSC(100) 4 nm + 용액 2.5 nm**, 3 nm × 3 nm, **32 H₃O⁺ + 32 OH⁻ + 200 H₂O**, **500 ps**
- 결과: **PS₄ 분해 → H₂S 발생 → 표면 붕괴**. `polyhedron-sulfur → single-sulfur` 전환
- **H 침투 지도**(z 0–40 Å × t 0–500 ps): hydration layer 형성 후 H가 벌크로 침투
- **COHP 정량** ★:
  - **ICOHP(P–S) = −6.43 eV**, 결합 2.04 Å
  - **ICOHP(P–S(H)) = −4.69 eV**, 결합 **2.18 Å** ← 양성자화가 P–S를 **27 % 약화**
  - 반결합 상태(antibonding)가 E_F 근처에 생김
- **S 궤적 비교**: 순수 H₂O에서는 S가 거의 안 움직이고, H₃O⁺/OH⁻ 조건에서 광범위 확산

### 7c. Sn 치환의 억제 기구 (슬 24) ★

- 조성: **Li₆.₂₅P₀.₇₅Sn₀.₂₅S₅Cl**
- **SnS₄–H 결합이 PS₄–H 보다 강해 H를 SnS₄ 쪽으로 유인** → PS₄ 보호
- 정량: `SnS₄–H` 정규화 신호 **0.6–0.8** 이 500 ps 내내 유지 vs `PS₄–H` **≈ 0**(억제)
- 상대 활성화에너지: **SnS₄–H 0.0 → PS₄–H 0.28 eV** (선형)

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

| 물질 | 구조 | σ (또는 D) |
|---|---|---|
| **Li₂SiS₃** | corner-sharing (안정, 실험상) | **10⁻⁴ mS/cm** |
| **Li₂SiS₃** | **edge-sharing (준안정)** | **2.4 mS/cm** |

→ **같은 조성에서 다면체 연결방식만 바꿔 4자릿수 전도도 상승**.
`D_600K × 10⁵ cm²/s` vs `Relative Stability rank 1–10` 플롯에서 **E_rel 0–0.05 eV/atom 안에
고전도 준안정상이 다수 존재**함을 보임 (Li₂SiS₃, Li₄SiGeS₆). 실험 보고 구조는 낮은 rank에 위치.

**준안정 고전도의 3 기술자** (슬 29, JACS 2025, 147, 47381):
1. **Dead volume** — 양이온 중심 S₄ 사면체가 Li 경로를 막는 부피
2. **Distance of cation** — corner-sharing의 양이온-양이온 거리 d_c > edge-sharing d_e
3. **Li–S₄ distortion** — Li–S₄ 부격자 왜곡 시 인력↓·거리↑·부피↑

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
| **음극 계면 반응** | Li₂S interphase, 11 nm @ 50 ns, D 0.4 vs 1.1 ×10⁻⁶ | **없음** | **완패 — 우리 공백**. 최우선 채택 후보 |
| **표면 가수분해** | SevenNet 반응 MD + ICOHP + Sn 억제 E_a 0.28 eV | `air_hsab` **정성 tier** | **완패**. 단 우리는 47종 횡단, 그들은 2조성 |
| **양극 코팅 스크리닝** | **17,233 Li-P-S-O @ MP** 4축 깔때기 (Nano Converg. 2026) | cascade 47종 × 6축 + 오늘 M6 계면반응성 추가 | **풀은 그들이 10²배, 축 밀도는 우리가 우위** — S6 감사의 직접 대조군 |
| **CSP / 신조성** | USPEX+MTP, Li₂SiS₃ 준안정 4자릿수 σ 상승 | 없음 (host 고정 문제설정) | **문제설정이 다름** — 열위가 아니라 무관. 단 "준안정이 더 좋을 수 있다"는 명제는 우리 metastable 고찰과 공명 |
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
7. **Nano Converg. 2026, 13, 27 (17,233 스크리닝)** — **S6 후보 나열 감사의 직접 대조군**.
   PDF 확보 최우선 (§13 위시리스트).

---

## 12. 주의 / 한계 (over-claim 방지)

1. **덱은 부재의 증거가 아니다.** "그들은 config-variance 오차막대가 없다"는 서술은 **덱이 아니라
   `papers/kim2024_...` 논문 실물 감사**에서 나온 것이며, 그 범위(Nano Energy 2024) 안에서만 유효하다.
   *Revision in Adv. Energy Mater.* 로 표기된 후속에서 보완됐을 수 있다.
2. **슬 14 단계 (2) "Lattice strain = ±0.05%"** — 슬 16의 계면 훈련셋은 `−5 ~ +5 %`,
   슬 17 표는 `±10 % strain`. **세 값이 서로 다르다**. 덱 오기 가능성이 높고, 논문(kim2024)은
   `±5 %`. **덱 수치를 그대로 인용하지 말 것**.
3. **힘 MAE 단위** — 슬 14 "0.073 meV/Å"는 eV/Å의 오기. 논문 감사에서 이미 확인된 동일 오기의 재발.
4. **슬 13 "Li₆xPO₄(?)"** — 코팅 스크리닝 최종 후보 조성이 저해상도로 판독 불가. **추정 금지**,
   논문(Nano Converg. 2026)으로 확인할 것.
5. **σ_RT 절대값 인용 금지** — 그들 파이프라인이 10 ns NPT MTP-MD에서 σ_RT를 직접 뽑지만,
   `papers/kim2024_...` 가 **같은 물질에서 functional에 따라 8배 갈린다**는 것을 보였다.
   Li₂SiS₃ `10⁻⁴ → 2.4 mS/cm` 도 **비율(4자릿수 상승)로만** 인용하고 절대값은 쓰지 말 것.
6. **"well agreement with experiment"(슬 19)** 는 TEM 이미지의 정성 대조다. 두께 11 nm가
   실험과 몇 % 일치인지는 덱에 없다.
7. **LFP SOC(슬 30)** 는 학생 프로젝트 수준이고 우리 축과 무관. 인용 가치 없음.

---

## 13. 미해결 질문 (구술 txt / 논문 확보로 닫을 것)

| # | 질문 | 닫는 방법 |
|---|---|---|
| Q1 | 코팅 스크리닝 17,233 풀의 **입구 필터와 최종 후보 조성**은? | Nano Converg. 2026, 13, 27 PDF |
| Q2 | Li\|LPSCl 계면 MD에서 **어느 무질서 배열**을 썼나 (50 %만? 전수?) | Chem. Eng. J. under review / 구술 |
| Q3 | γ_select / γ_break **수치 기준**은? | 논문 SI / 구술 |
| Q4 | 가수분해 MD의 **H₂S 발생량 정량**(우리 db의 Taklu 1.07→0.49 cm³/g와 대조 가능한가) | Adv. Funct. Mater. revision |
| Q5 | Adv. Energy Mater. revision(=Dynamic properties 후속)이 **BH₄ 계**인지 argyrodite인지 | 구술 |
| Q6 | CSP의 준안정 구조가 **합성 가능성** 검증을 받았나 | JACS 2025, 147, 47381 |

---

## 14. 인용 가능 문장 (원고/발표용)

- "범용 uMLIP는 평형 근처 훈련점에 치우쳐 고에너지 영역에서 PES가 물러진다(softening) — 그래서
  반응 영역을 보려면 fine-tuning 또는 반응좌표 기반 훈련이 필요하다" (덱 슬 8·21의 명제)
- "MLIP로 계산한 이온전도도의 절대값은 훈련에 쓴 exchange-correlation functional의 각인을 받는다"
  (kim2024 정본; 덱 슬 14가 그 병렬학습 절차를 보여줌)
- "같은 조성에서도 다면체 연결방식(corner→edge)만 바뀌면 확산이 4자릿수 달라질 수 있다"
  (덱 슬 28, Li₂SiS₃ — **비율만** 인용)

---

## 99. ⏳ 발표 구술 내용 (txt 대기 중)

사용자가 발표 구술 txt를 제공하기로 함 (2026-07-28). 받으면 여기에 정리하고 §13의 Q1–Q6를 닫는다.

_(비어 있음)_
