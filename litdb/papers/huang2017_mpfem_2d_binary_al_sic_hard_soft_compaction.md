<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 같은 부류 선례 = demirtas2021_mpfem_hollow_sphere_die_compaction.md · 같은 묶음 = zhou2019_mpfem_2d_copper_powder_die_compaction_release.md -->
# 무른 Al + 단단한 SiC 원판 이원 혼합을 입자마다 FE 메시로 (2D MPFEM · MSC.Marc) 단동 다이 압축 — 정렬 (SC · HCP) ↔ 무작위 충전 · SiC 10–50 % · 크기비 1.5 · 2 · 3 · 입자 간 µ 0 ↔ 0.2 ★★ 힘 사슬은 **맞닿은 단단한 입자 (SiC)** 가 정하고 큰 응력이 SiC 에 모인다 · 정렬 충전에서는 미끄럼이 없어 마찰이 거의 무관하다 — [DEM 우선 (수영)] 단단한 + 무른 짝 (AM + SE) 과 2D 49 원판 정렬 배열의 해석에 쓴다 — Huang, An, Zhang, Yu (Powder Technol. 2017)

> slug `huang2017_mpfem_2d_binary_al_sic_hard_soft_compaction` · DOI `10.1016/j.powtec.2017.03.017` · type `MPFEM 2D (MSC.Marc · 입자마다 요소 1200 · 절점 1241 · 갱신 라그랑주 · 완전 Newton–Raphson · segment-to-segment 접촉 · 국부 메시 적응 + 전체 다시 메시 · Al 탄소성 멱경화 + SiC 탄성 · 강체 다이 · 펀치) + DEM (무작위 초기 충전 전용) · 실험 없음` · PDF `huang2017.pdf` · digested `2026-11-25` · status ✅

> 표지: **[인쇄]** = 본문 · 표 · 캡션 · 그림 패널에 찍힌 값 · **[판독]** = 그림에서 읽은 값 (이 논문 그림은 전부 200 dpi 래스터 — 곡선은 눈 판독 ±0.005 · Heckel 맞춤선 끝은 화소 열 단면으로 읽음 · `litdb/figures/huang2017_mpfem_2d_binary_al_sic_hard_soft_compaction/digitized.csv`) · **[카드 산술]** · **[추정]** · **[미확인]** = 원문에 없음.

---

## 0. 이 논문이 우리에게 *왜* 필요한가 (한눈 positioning)

1저자 11-25 Q1 — [DEM 우선 (수영)] 2D 49 원판 S/F 벤치마크에 MPFEM 바깥 기준을 연다.  이 논문은 그 축에서 **두 가지**를 준다.

1. **(나) 단단한 + 무른 짝** — 우리 계 (단단한 AM + 무른 SE) 와 같은 *짝 꼴* 을 입자마다 FE 로 푼 2D 선례.  결론 *"the force chain structure is mainly determined by the contacted SiC particles"* (초록) · *"large stresses are mostly focused on the enhanced phase of SiC particles"* (§3.3) 은 우리 MPM DO-NOT ② (AM 을 얼려 하중 0 → SE 가 100 % 를 지고 과압축 · `fam_platen_prereg_20260812.md` §11) 의 반대 극을 FE 로 보여 준다 — **단단한 상이 맞닿으면 그 상이 하중을 진다.**
2. **(가) 정렬 배열의 함정** — 정렬 충전 (SC · HCP) 에서는 *"no sliding between particles is obviously observed"* 이라 입자 간 µ 0 ↔ 0.2 의 압축 곡선이 거의 같다 (그림 3).  무작위 충전에서는 µ 가 초 · 중반 곡선을 옮긴다 (그림 4).  ⇒ 우리 7 × 7 **정사각 배열**에서 Q13 이 S/F 를 못 가른 것은 배열 대칭이 미끄럼을 막은 몫일 수 있다 [추정 · §7-A].

| 우리가 필요한 것 | 이 논문이 주는 것 | 주지 않는 것 |
|---|---|---|
| 단단한 + 무른 혼합의 FE 거동 | Al (E 62.59 GPa · K 225.9 MPa · n 0.05) + SiC (E 470 GPa · 탄성) · 힘 사슬 · 응력 집중 · 닫힌 공극 [인쇄] | 하중 분담 몫의 숫자 (상별 평균 응력 · 힘 몫) [미확인] |
| 조성 · 크기비 효과 | SiC 10–50 % · 크기비 1.5–3 · Heckel 기울기 0.0055 → 0.0035 MPa⁻¹ (SiC 10 → 50 %) [판독 + 카드 산술] | 실험 대조 (문헌 경향과 정성 비교만) |
| 정렬 ↔ 무작위 · 마찰 | 정렬: 미끄럼 없음 · 배위수 일정 (HCP CN_Al 12 · CN_SiC 3 / SC 8 · 4) · µ 무관 / 무작위: µ 가 초 · 중반에 영향 | µ 0.2 에서 무작위 충전의 정량 차를 표로 주지 않음 |
| FE 해상도 · 설정 | 입자당 요소 1200 (면적 등가 지름당 ≈39 요소 [카드 산술]) · 국부 적응 + 전체 다시 메시 · 완전 Newton–Raphson (암시 · 정적으로 읽음) | 메시 수렴 시험 · 펀치 속도 값 · 입자 절대 크기 · 다이 크기 [미확인] |
| 탈압 (R4) | — | **탈압을 풀지 않았다** |

⚠ **크기 역할이 우리와 반대다** — 이 논문의 단단한 상 (SiC) 은 **작고 소수** (10–50 %) · 무른 상 (Al) 이 **크다**.  우리 계는 단단한 AM 이 **크고 다수** (AM_P : AM_S : SE 지름 ≈ 12 : 4 : 1 · CLAUDE.md) · 무른 SE 가 작다.  옮기는 것은 *기전의 방향* (단단한 상끼리의 접촉 사슬 · 무른 상의 공극 채움 · 닫힌 공극) 이지 값 · 조성 법칙이 아니다.

---

## 1. 한 줄 요약

DEM 으로 만든 무작위 이원 충전 (판독 ≈96–98 원판 · R_Al/R_SiC = 2 · SiC 10–50 %) 과 MSC.Marc 로 만든 정렬 이원 충전 (SC · HCP · SiC 가 큰 Al 사이 빈자리를 꼭 채우는 크기) 의 원판마다 같은 FE 메시 (요소 1200 · 절점 1241) 를 주고 2D 단동 다이 압축을 풀었다.  **SiC 가 많을수록 같은 밀도에 더 큰 압력이 들고** (Heckel 기울기가 준다), **크기비와 초기 충전 상태가 과정과 결과를 바꾸며**, 무작위 충전에서 하중은 **맞닿은 SiC 의 힘 사슬**로 전달돼 큰 응력이 SiC 에 모이고 마지막에는 SiC 가 둘러싼 **닫힌 공극**이 남는다.  정렬 충전에서는 입자가 미끄러지지 않아 배위수가 일정하고 Al 이 규칙적인 다각형 (SC = 사각 · HCP = 육각) 이 되며 마찰 효과가 거의 없다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Fen Huang · Xizhong An** (교신, anxz@mail.neu.edu.cn) · **Yuxi Zhang · A.B. Yu** |
| 소속 | School of Metallurgy, Northeastern University, Shenyang 110004, China (Huang · An · Zhang) · Department of Chemical Engineering, Monash University, Clayton, Victoria 3800, Australia (Yu) |
| 저널 | **Powder Technology 314 (2017) 39–48** |
| DOI | **10.1016/j.powtec.2017.03.017** |
| 이력 | Received 2016-05-31 · Revised 2017-03-03 · Accepted 2017-03-04 · Online 2017-03-06 |
| 키워드 | Multi-particle finite element method · Al/SiC composite powders · Compaction · Densification dynamics and mechanism · Multi-scale modeling |
| 연구비 | National Natural Science Foundation of China (No. 51374070) · Fundamental Research Funds for the Central Universities of China (N162505001) |
| 연구유형 | **2D MPFEM** (MSC.Marc) + DEM (무작위 초기 충전 · 상세는 앞선 논문 [42–45] 로 넘김) · 실험 없음 |
| 같은 그룹 | [39] Zhang, An, Zhang 2015 (Appl. Phys. A · 2D MPFEM 미시 거동) · [41] Han, An, Zhang, Huang 외 2016/2017 (Fe + Al MPFEM — 이 논문의 von Mises 식 출처) · 같은 묶음 `zhou2019_mpfem_2d_copper_powder_die_compaction_release` 는 이 논문을 [17] 로 인용 |

---

## 3. 핵심 수치

### 3-1. 모델 구성 (Table 1 · Table 2 전사 + 유도)

**Table 1** — *Materials parameters used in the simulation* [인쇄 · `tab_1.png`]

| Materials | Young's modulus E/GPa | Poisson's ratio ν | Hardening index n | Strength coefficient K/MPa |
|---|---|---|---|---|
| Al | 62.59 | 0.33 | 0.05 | 225.9 |
| SiC | 470 | 0.142 | Elastic | – |

**Table 2** — *Modeling conditions* [인쇄 · `tab_2.png`]

| Contact definition | Load setting | Jobs |
|---|---|---|
| Particles: deformable | Iteration method: full Newton-Raphson algorithm | Updated Lagrange for large strain |
| Die and punch: rigid | Convergence criterion: displacement | Large deformation |
| Friction between particles: 0 | | |
| Upper punch: velocity control | | Segment to segment method |

| 항목 | 값 | 표지 |
|---|---|---|
| 입자 | 2D 원판 · 큰 원판 = Al (무름) · 작은 원판 = SiC (단단) | [인쇄] |
| 메시 | **모든 원판이 같은 메시 — 절점 1241 · 요소 1200** (그림 2: O-격자 꼴 사각형 · 가운데 조밀) — 작은 SiC 도 같은 요소 수라 요소 크기가 작다 | [인쇄] |
| 면적 등가 해상도 | √(1200 / (π/4)) ≈ **39 요소 / 지름** (큰 · 작은 원판 모두) | [카드 산술] |
| 메시 적응 | **국부 메시 적응 (local mesh adaptability) + 전체 다시 메시 (global remeshing)** — *"to improve the accuracy of computation and get much denser green compacts"* | [인쇄] · 적응 기준 · 다시 메시 횟수 [미확인] |
| 무작위 충전 입자 수 | **원문에 없다.**  그림 1b 영상 계수: Al 90 % = 67 + 29 · 80 % = 48 + 49 · 70 % = 37 + 60 · 60 % = 27 + 71 · 50 % = 21 + 75 (큰 + 작은 · 합 96–98) — 면적비 4 로 되짚은 Al 부피 몫 0.902 · 0.797 · 0.712 · 0.603 · 0.528 이 명목값과 맞는다 | [판독 + 카드 산술] |
| 전체 메시 크기 | ≈97 × 1200 ≈ **11.6 만 요소** · ≈97 × 1241 ≈ 12.0 만 절점 | [카드 산술] |
| 정렬 충전 크기비 | SC: R_Al : R_SiC = **1 : (√2 − 1)** (= 0.414 · 정사각 빈자리에 꼭 맞음) · HCP: **3 : (2√3 − 3)** (= 0.155 · 삼각 빈자리에 꼭 맞음) | [인쇄] |
| 정렬 초기 밀도 | SC ≈ **0.914** · HCP ≈ **0.945–0.950** (그림 3 첫 표식) — 단위 칸 이론값 SC 0.920 · HCP 0.950 | [판독] · 이론값 [카드 산술] |
| 무작위 조건 ① | R_Al/R_SiC = **2** 고정 · SiC 부피 분율 **10 · 20 · 30 · 40 · 50 %** | [인쇄] |
| 무작위 조건 ② | **Al 90 %** 고정 · R_Al/R_SiC = **1.5 · 2 · 3** | [인쇄] |
| 같은 조성 · 다른 충전 (그림 7) | Al 80 % · R 2 · 초기 상대밀도 **case I 0.7541** (캡션) / **0.7451** (본문) · **case II 0.7756** | [인쇄] — ⚠ case I 값이 캡션 ↔ 본문에서 다르다 |
| 재료식 | Eq. (1) von Mises (`eq_01_von_mises_stress.png` · [41] 인용) · Eq. (2) σ_y = C(ε₀ + ε̄)ʰ + D(ε̃)ᵏ · Eq. (3) ε̃ = [2/3 (ε_ij ε_ij)]^(1/2) ("equivalent strain rate" 라 적고 변형률 텐서로 씀) · Eq. (4) 갱신 라그랑주 가상일 | [인쇄] |
| 기호 대응 | Eq. (2) 의 h · C ↔ 표 1 의 n · K.  본문: K 는 *"just the same as the commonly used yield stress"* — n 0.05 라 거의 완전 소성으로 읽음 | [인쇄] · 해석은 [카드 추론] |
| 마찰 | 본문: *"the friction between the particles and die is set to be μ = 0"* · 입자 간 µ 는 그림 3 · 4 에서 0 · 0.2 비교 · **표 2 는 "Friction between particles: 0"** | [인쇄] — ⚠ 표 2 와 본문이 어긋난다 · 그림 5–11 의 µ [미확인] |
| 구동 · 풀이 | 위 펀치 **속도 제어** (값 없음) · 완전 Newton–Raphson · 변위 수렴 판정 → 암시 · 정적 풀이로 읽음 (관성 없음) | [인쇄] · 정적 여부는 [카드 추론] |

### 3-2. 압축 곡선 (그림 3–7 · 래스터 눈 판독)

| 그림 · 경우 | 초기 ρ | 주요 판독 | 표지 |
|---|---|---|---|
| **3** 정렬 SC (순수 Al µ 0.2 · Al/SiC µ 0.2 · µ 0) | ≈0.914 | 180–220 MPa 에서 계단 (0.93 → 0.96) · 0.98 ≈ 400 MPa · ≈0.998–1.0 at 700–1000 MPa · 세 곡선이 겹친다 | [판독] |
| **3** 정렬 HCP (순수 Al · Al/SiC µ 0.2 · µ 0) | ≈0.945–0.950 | 순수 Al 이 가장 조밀 (0.995 ≈ 470 MPa) · **Al/SiC (µ 0.2) 는 ≈0.990–0.993 에서 580–970 MPa 동안 멈춘다** · µ 0 ↔ 0.2 차이는 초기만 | [판독] |
| **4** 무작위 Al 90 % · R 2 · µ 0 ↔ 0.2 | ≈0.75–0.78 | ρ 0.90: ≈175 MPa (µ 0) ↔ ≈195 MPa (µ 0.2) · ρ 0.95: ≈300 ↔ ≈345 MPa · 끝 ≈0.981 (740 MPa · µ 0) · ≈0.977 (650 MPa · µ 0.2) — **마찰은 초 · 중반에 압력을 10–15 % 올리고 끝에서 모인다** | [판독] · 10–15 % [카드 산술] |
| **5a** 무작위 R 2 · SiC 10–50 % | ≈0.76–0.80 | 300 MPa 에서 ≈0.945 (10 %) · ≈0.952 (20 %) · ≈0.94 (30 %) · ≈0.92 (40 %) · ≈0.91 (50 %) · **40 · 50 % 곡선은 ≈345 MPa 에서 끝난다** (이유 미기재) · 20 % 가 10 % 보다 조밀한 구간이 있다 (단조 아님) | [판독] |
| **6a** 무작위 Al 90 % · R 1.5 · 2 · 3 | ≈0.78–0.80 (R 3 이 가장 높음) | R 3 은 ≈40 MPa 에서 계단 (0.82 → 0.84) · 0.95 ≈ 270 MPa 근처에서 셋이 가깝다 · R 2 가 끝까지 조금 덜 조밀 | [판독] |
| **7** Al 80 % · R 2 · case I ↔ II | 0.754 · 0.776 | ρ 0.86: case I ≈112 MPa ↔ case II ≈128 MPa · **ρ ≈ 0.95 (≈300 MPa) 위에서 두 곡선이 겹친다** [인쇄 서술 + 판독] | [판독] |
| **11** Al 90 % · R 2 · ρ + 총 변형 에너지 | ≈0.78 | 영역 A (P ≲ 8 MPa · 재배열 · 변형 에너지 ≈0) · B (≈8–170 MPa · ρ 가 P 에 거의 선형 · *"elastic deformation is dominant"*) · C (≈170–415 MPa · Al 큰 변형 · 변형 에너지 급증) · D (> 415 MPa · ρ 증가 둔화 · SiC 탄성 변형 증가) · 변형 에너지 축 0–3000 "KJ" | [인쇄 서술 + 판독 경계] |

### 3-3. Heckel 맞춤 (그림 5b · 6b)

식 [인쇄]: **ln[1/(1 − ρ)] = M·P + A** — M = *"densification coefficient which is related to the plastic deformation of particles"* · *"the larger the value M, the better the compressibility"*.  맞춤 구간은 그림에서 50–250 MPa.  M 값은 **원문에 없다** — 맞춤선 끝 (248 MPa) 의 화소 열 단면 + 50 MPa 시작 (≈1.60–1.66 · 겹침) 으로 되짚었다 [판독 + 카드 산술 · ±0.0003 MPa⁻¹].

| 경우 | −ln(1−ρ) at 248 MPa | M (MPa⁻¹) | 1/M (MPa · 참고) |
|---|---|---|---|
| SiC 10 % (R 2) | 2.710 | ≈0.0055 | ≈180 |
| SiC 20 % | 2.686 | ≈0.0054 | ≈185 |
| SiC 30 % | 2.534 | ≈0.0046 | ≈215 |
| SiC 40 % | 2.428 | ≈0.0041 | ≈245 |
| SiC 50 % | 2.318 | ≈0.0035 | ≈285 |
| R 1.5 (SiC 10 %) | 2.942 | ≈0.0064 | ≈155 |
| R 2 (SiC 10 %) | 2.776 | ≈0.0057 | ≈175 |
| R 3 (SiC 10 %) | 2.840 | ≈0.0055 | ≈180 |

- SiC 가 늘수록 M 이 준다 — *"the higher the content of reinforced SiC particles, the lower the value of M"* (실험 문헌 [11,14] 와 같은 방향이라고 적음) [인쇄].
- ⚠ 그림 5b 의 표식 범례는 5a 와 다르다 (5a: 20 % = 사각형 · 40 % = 별 · 50 % = 십자 ↔ 5b: 20 % = 별 · 40 % = 삼각형 · 50 % = 사각형).  위 표는 5b 범례를 따른다.
- 같은 경우 (R 2 · SiC 10 %) 의 두 판독 0.0055 (그림 5b) · 0.0057 (그림 6b) 이 판독 오차 안에서 같다.

### 3-4. 미시 판독 (그림 8–10 · 11 의 국부 그림)

| 관측 | 내용 | 표지 |
|---|---|---|
| 정렬 SC 압력 단계 (그림 8a) | P = 0 · 33.68 · 177.90 · 301.64 · 487.28 · **1341.50 MPa** · 색 띠 0–1000 MPa · 1341.5 MPa 에서 SiC 가 노란색 (≈900 MPa 대) | [인쇄 · 패널] · 색 [판독] |
| 정렬 HCP 압력 단계 (그림 8b) | P = 0 · 73.44 · 290.21 · 360.14 · 571.58 · **888.62 MPa** | [인쇄 · 패널] |
| 정렬 배위수 | **HCP CN_Al 12 · CN_SiC 3 · SC CN_Al 8 · CN_SiC 4** — 압축 내내 일정 | [인쇄] |
| 정렬 Al 모양 | 최종 Al = **정다각형** (SC 사각 · HCP 육각) · 공극은 Al 변형이 채운다 · 같은 종류 입자는 각 단계에서 모양 · 응력 분포가 같다 | [인쇄] |
| 무작위 Al 70 % · R 2 (그림 9) | P = 0 · 32.01 · 102.73 · 251.52 · **987.69 MPa** · 초기 미끄럼 · 구름 → Al 큰 소성 → 끝에 **SiC 가 둘러싼 닫힌 공극** · 987.69 MPa 에서 SiC 사슬이 회색 (> 1000 MPa) | [인쇄] + 색 [판독] |
| case I ↔ II (그림 10) | 같은 단계에 드는 압력: case I 38.98 · 87.57 · 156.97 · 248.14 · 509.43 MPa ↔ case II 78.65 · 133.71 · 232.40 · 375.40 · 636.19 MPa · case I 은 SiC 가 더 고르게 퍼져 벽 효과가 작고 응력이 고르며 압력이 덜 든다 | [인쇄 · 패널 + 본문] |
| 접촉 변화 | 점 → 선 접촉 · 응력이 접점에서 입자 안쪽으로 번진다 · Al 의 큰 응력은 SiC 와의 접촉 경계에 | [인쇄] |

### 3-5. 이 논문에 **없는** 값

입자 절대 크기 · 다이 폭 · 초기 충전 높이 · 펀치 속도 · 증분 수와 크기 · 다시 메시 기준과 횟수 · 메시 수렴 시험 · 압력 산정식 · 상별 하중 몫 · 배위수의 무작위 충전 값 · 그림 5–11 의 µ · 시드 반복 · D · k · h(=n) 외 재료 상수 · 탈압 · 실험 대조 · 2D 평면변형/평면응력 · 변형 에너지 단위 (그림 11 "KJ") 의 두께 가정.

---

## 4. 시뮬레이션 방법 ★

### 4-1. 흐름

1. **충전 만들기** — 무작위: DEM 동역학 모의 (*"which can realistically reflect the packing structures dominated by interparticle forces"* · 상세는 [42–45]) · 정렬: MSC.Marc 안의 기하 함수.
2. **FE 이식** — 충전을 MPFEM 모형으로 옮겨 원판마다 메시를 나눈다 (모든 원판 같은 메시).
3. **조건 설정** — 재료 · 접촉 · 메시 적응 · 하중 사례 · 작업 (*"material properties, definition of contact, mesh adaptability, loading cases and jobs"*) → 서버에서 계산.
4. **압축** — 위 펀치 속도 제어 · 단동.  **탈압 없음.**

### 4-2. 입자 처리 (DEM 판 "무질서 처리")

- **두 상 모두 변형체** — Al = 탄소성 (멱경화 n 0.05) · **SiC = 탄성 변형체 (강체 아님)** · 다이 · 펀치 = 강체.  ⇒ 우리 MPM 의 '얼린 강체 AM' 과 다르게 **단단한 상도 응력을 받아 하중을 진다.**
- 이원 (bimodal) 크기 — 무작위 R 1.5 · 2 · 3 · 정렬 0.414 · 0.155 (작은 쪽 = SiC).
- 진짜 형상 소성 — Al 이 다각형으로 눌려 공극을 채운다 (그림 8 · 9 · 10).  겹침 대리가 아니다.
- 국부 메시 적응 + 전체 다시 메시로 큰 뒤틀림을 넘긴다 — Zhou 2019 · Demirtas 2021 은 다시 메시를 적지 않았다 (`zhou2019_…` §4-2 · `demirtas2021_…` 카드).

### 4-3. 접촉 · 마찰 · 풀이

- **segment-to-segment** 접촉 (표 2) — 같은 그룹 Zhou 2019 는 node-to-segment.  허용 거리 · 벌점 · 승수 [미확인].
- 마찰: 그림 3 (정렬) 에서 µ 0 ↔ 0.2 가 거의 같다 — *"in the compaction of initial ordered packings, the structure is relatively stable and no sliding between particles is obviously observed"* [인쇄].  그림 4 (무작위) 에서는 초 · 중반에 차이 — *"the difference of the compaction curves for composite powders with different friction coefficient is mainly indicated at the early and middle stages of compaction"* [인쇄] (Zhang [33] 과 같은 결론).
- 완전 Newton–Raphson · 변위 수렴 — 암시 정적 FE 로 읽힌다.  우리 명시 MPM 의 재하율 함정 (판 속도 ÷ 파속) 은 이 풀이에 원리상 없다 [카드 추론].

---

## 5. Figure set ★ (11 개 전부 + 표 2 개 · 식 3 개 — 모두 렌더해서 열어 봤다)

| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| **1** ★ | (a) 정렬 SC · HCP 이원 단위 (b) 무작위 이원 충전 다섯 (R 2 · Al 90 · 80 · 70 · 60 · 50 %) — 붉은 틀 = 다이 | ★ 입자 수 영상 계수 (96–98 개 · §3-1) · 조성이 낮을수록 충전이 짧아진다 (같은 바닥 폭) |
| **2** | 원판 하나의 메시 (O-격자 사각형 1200 요소) | 지름당 ≈39 요소 — 우리 MPM 36 칸과 같은 자릿수 |
| **3** ★★ | 정렬 SC · HCP — 순수 Al (µ 0.2) · Al/SiC (µ 0.2 · µ 0) | ★★ **µ 무관 (정렬)** — 우리 7 × 7 정사각 배열 해석 (§7-A) · HCP Al/SiC 의 0.99 멈춤 |
| **4** ★★ | 무작위 Al 90 % · R 2 · µ 0 ↔ 0.2 | ★★ 무작위에서는 µ 가 초 · 중반 압력을 10–15 % 옮긴다 [판독] |
| **5** ★★ | (a) SiC 10–50 % ρ(P) (b) Heckel 맞춤 50–250 MPa | ★★ SiC ↑ → M ↓ (0.0055 → 0.0035 MPa⁻¹ [판독 + 카드 산술]) · 40 · 50 % 곡선 조기 종료 · 범례 불일치 |
| **6** ★ | (a) 크기비 1.5 · 2 · 3 ρ(P) (b) Heckel | 크기비가 곡선과 끝 밀도를 바꾼다 · R 3 의 저압 계단 |
| **7** ★ | Al 80 % · R 2 · 초기 밀도만 다른 두 충전 (inset 형태) | 초기 충전이 ρ < 0.95 구간을 바꾸고 그 위에서 모인다 |
| **8** ★★★ | 정렬 SC · HCP 압축 단계별 von Mises (0–1000 MPa 색 띠) | ★★★ 응력이 **SiC (단단)** 에 모인다 · Al 은 정다각형 · 배위수 일정 |
| **9** ★★★ | 무작위 Al 70 % · R 2 압축 단계별 von Mises | ★★★ **SiC 힘 사슬** · 끝의 닫힌 공극 · SiC > 1000 MPa |
| **10** ★★ | 그림 7 의 case I · II 단계별 형태 · 응력 | 고른 SiC 분포 = 벽 효과 ↓ · 응력 고름 · 압력 ↓ |
| **11** ★ | Al 90 % · R 2 · ρ 와 총 변형 에너지 vs P + 국부 변형 에너지 그림 | 네 영역 A–D · ⚠ 영역 B 를 "탄성 지배" 라 한 해석 (§10-B) |
| 표 1 · 2 | 재료 상수 · 모형 조건 | §3-1 에 전사 |
| 식 (1)–(3) | von Mises · 멱경화 · 등가 변형률 | `eq_*.png` |

---

## 6. Post-processing ★

| 무엇 | 어떻게 | 우리 대응물 |
|---|---|---|
| 압축 곡선 ρ(P) | 상대밀도 vs 압력 (산정법 미기재) | 2D MPM 아래판 압력 vs Φ_m · 3D MPM wallP vs ε |
| Heckel 맞춤 | ln[1/(1−ρ)] = M·P + A · 50–250 MPa | 우리 DEM 순수 SE Heckel (P_y 138 MPa · R² 0.965 · CLAUDE.md frame [3]) |
| 응력장 | 등가 von Mises 등고선 · 고정 색 띠 0–1000 MPa · 압력 단계 스냅숏 | `viz_mpm_morphology.py` · 2D S/F 판독 |
| 배위수 | 정렬 충전의 최종 CN (상별) | DEM CN (AM–AM · AM–SE · SE–SE) |
| 변형 에너지 | 총 변형 에너지 vs P + 국부 변형 에너지 지도 | 없음 (우리 MPM 은 에너지 장부를 적지 않는다 · 비교 문서 F 절) |
| 도구 | MSC.Marc (FE) · DEM 코드 [미확인] | — |

---

## 7. 우리 DEM+MPM 대비  →  `comparison_vs_ours_DEM.md` · `our_dem_baseline.md` (⛔ 자리표시 — 우리 값은 CLAUDE.md · 리포 기록에서 직접)

### 7-0. 요약표

| 항목 | 이 논문 (2D MPFEM · Al + SiC) | 우리 | 판정 |
|---|---|---|---|
| 단단한 상의 처리 | **탄성 변형체 · 하중을 진다** (SiC 응력 > 1000 MPa) | 3D MPM: AM = 얼린 장애물 (하중 0) · DEM: AM 강구 (E 140 GPa 입력 · 출처 재확인 중 `SELF-51`) · 2D 벤치마크: 한 재료 | **그들이 맞다** — 우리 MPM ② 의 근거 쪽 |
| 무른 상 | Al 탄소성 · 공극을 채운다 | SE J2 (MPM) · 연화 탄성 (DEM) | 같은 편 (MPM) |
| 크기 역할 | 단단 = 작고 소수 | 단단 = 크고 다수 (12 : 4 : 1) | **반대** — 방향만 |
| E 비 (단단 / 무름) | 470 / 62.59 = **7.5** | 실물 꼴: Bazzoun 2026 입력 E_CAM 161.5 / E_SE 22.1 = **7.3** · 우리 DEM 연화 입력 140 / 1.35 ≈ 104 | 실물 비와는 가깝다 · 우리 DEM 은 한 자릿수 크다 (`mcgrogan2017` 줄과 같은 결론) |
| 입자 간 미끄럼 · 분리 | ✅ (segment-to-segment · µ 0 / 0.2) | 2D F ✅ · S ❌ · 3D MPM ❌ | F 와 같은 꼴 |
| 해상도 | 지름당 ≈39 요소 + 국부 적응 · 다시 메시 · 수렴 시험 없음 | 2D 12 · 16 · 24 · 36 칸 사다리 | 그들 쪽이 우리 36 칸 자리 |
| 탈압 | ❌ | ❌ (R4 미구현) | 둘 다 없다 |
| 실험 | ❌ (문헌 경향과 정성 비교) | 2D 벤치마크 = 검산 | — |

### ★ 7-A. 2D 49 원판 벤치마크에 주는 것 — **정렬 배열의 함정**

- 우리 2D 벤치마크 = **7 × 7 정사각 배열 · 같은 지름 49 원판 · 시작 Φ_m 0.78** (`docs/reviews/suyoung_u6_first_development_20261118/README.md` — π/4 = 0.785 와 같다 [카드 산술]).  이 논문의 '정렬 SC' 는 같은 정사각 꼴 (+ 빈자리 채움 원판) 이다.
- 이 논문 그림 3: 정렬 충전에서 µ 0 ↔ 0.2 곡선이 거의 겹치고, 본문은 그 이유를 *"no sliding between particles is obviously observed"* · 배위수 일정으로 든다 [인쇄].  무작위 충전 (그림 4) 에서만 µ 가 초 · 중반에 압력을 10–15 % 옮긴다 [판독].
- ⇒ ★ **[추정 · 검증 전]** Q13 의 *"이 2D 배치에서 S/F 를 구별하지 못함"* (`docs/reviews/suyoung_q13_return_20261125/README.md`) 은 S (한 속도장 · 미끄럼 · 분리 없음) 와 F (원판별 장 · µ 0.5) 가 갈리는 기전 = **접촉 미끄럼** 이 정사각 배열 대칭에서 거의 일어나지 않은 몫일 수 있다.  S/F 를 가르려면 **무작위 (DEM 충전) 배열 팔**이 더 정보가 크다 — 메모 §4-5 의 "작은 흔들림 시드" 보다 한 걸음 더.  (단: 우리 S 는 셀 거리 안에서 일찍 붙는 효과도 있어 미끄럼만으로 다 설명되지 않는다.)
- 해상도: 이 논문 지름당 ≈39 요소 (+ 적응 · 다시 메시) ≈ 우리 36 칸 자리 — FE 팔 사다리의 위쪽 칸 (메모 §4-3 의 지름당 16 · 32 · 64 요소) 과 같은 자릿수 [카드 산술].

### ★ 7-B. 단단한 + 무른 짝 (나) — AM + SE 에 옮길 수 있는 것 / 없는 것

| 기전 (이 논문) | 우리 계에서의 읽기 | 옮김 |
|---|---|---|
| 힘 사슬 = 맞닿은 SiC 사슬 (그림 9) · 큰 응력이 SiC 에 모인다 | 단단한 AM 이 맞닿으면 AM 골격이 하중을 진다 = DEM 의 AM 차폐 (순수 SE overlap 11–12 % ↔ 복합 1.75 % · CLAUDE.md E_SE 절) 와 같은 방향 · MPM 의 '얼린 AM 하중 0' 과 반대 | **방향 ✅** — MPM ② (AM 하중 분담) 가 필요하다는 FE 쪽 근거 하나 (값 ✗) |
| 무른 Al 이 공극을 채우고, 끝에 **SiC 가 둘러싼 닫힌 공극**이 남는다 | 단단한 골격이 만든 틈은 무른 상이 다 못 채운다 = 복합 기공 바닥 | 방향 ✅ · `cardenasbarrantes2020_…` 의 φmax(κ) 와 같은 결론 |
| SiC ↑ → 같은 밀도에 더 큰 압력 · M ↓ | 우리 DEM 은 기공 vs AM% 에 **Furnas dip** (AM ≈75–85 wt%) 이 있다 (CLAUDE.md frame [3]) — dip 너머 (AM-rich) 에서만 AM ↑ → 기공 ↑ · 그 아래는 반대 | 방향은 **dip 너머 쪽에서만** ✅ · 이 논문은 단단상 10–50 % (소수) 라 dip 을 보지 않는다 · 값 ✗ |
| 초기 충전 (고른 SiC 분포) 이 ρ < 0.95 구간 · 응력 고름 · 압력을 바꾼다 | 믹싱 (분산 상태) 이 압밀에 남긴다 — 믹서 트랙 (Ⓒ) 의 압밀 쪽 효과 | 방향 ✅ |
| 크기비 1.5 · 2 · 3 의 효과 | 우리 크기비 4 · 12 (단단이 큼) | ✗ — 크기 역할이 반대 |

### 7-C. 판정 (frame [4] · [5])

- frame [5]: 역학 쪽 (형상 소성 · 접촉 · 힘 사슬 · 변형 에너지) 만 있고 전달 · 탈압은 없다.
- frame [4]: 실험 대조가 없다 — 문헌 경향 *"agreeable with … physical experiment [11], DEM [26], and MPFEM [33,35]"* 은 정성적이다.  우리 쪽에서 이 논문은 앵커가 아니라 **기전 · 설정의 선례**다.

---

## 8. 적용 인사이트 (실행 가능한 순서)

1. **S/F 벤치마크에 무작위 배열 팔을 둔다** (Q13 다음 등록 때) — 근거: 이 논문 그림 3 (정렬 = µ 무관) ↔ 그림 4 (무작위 = µ 영향).  등록 문서에 "정렬 배열에서 S ≈ F 는 기대값" 을 결과 전에 적는다 [추정].
2. **FE 팔의 해상도 기준** — 지름당 ≈39 요소 + 국부 적응 · 다시 메시 (이 논문) 를 위쪽 칸으로 둔다.  다시 메시를 쓰면 수렴 사다리의 '같은 메시 계열' 이 깨진다 — 다시 메시 팔과 고정 메시 팔을 나눠 적는다 [추정].
3. **MPM ② 설계 메모에 인용** — 단단한 상을 변형체 (탄성) 로 두면 단단–단단 접촉이 하중을 진다 (FE 근거).  우리 후보 A (움직이는 강체 AM) 는 강체라 응력장이 없다 → 하중 몫은 접촉 충격량으로 읽어야 한다 [추정].
4. **Heckel 맞춤 구간을 결과 전에 정한다** — 이 논문은 50–250 MPa 를 그림으로만 보였다.  우리 Heckel (P_y 138 MPa) 과 견줄 때는 구간 · 판독 (압력 정의) 을 맞춘다.
5. **크기 역할 반대를 표지로** — 이 논문 결론의 크기비 · 조성 법칙을 우리 AM : SE 에 옮기지 않는다.

---

## 9. 인용 가능 문장 (deck/paper 용)

- *"DEM can effectively model the compaction of composite powder from micro particulate scale; however, as indicated in previous studies its wide applications can only be limited to small deformation or low relative packing densities (e.g. the packing density is usually lower than 0.85) [25–27]."* (p.40) — DEM 의 밀도 한계 (2 차 인용 · 원전 [25–27] = Martin & Bouvard 2003 · 2004 · Skrinjar & Larsson 2004).
- *"One of the advantages of this method is that it can describe non-uniform contact area and arbitrary particle shape without any simplifications."* (p.41) — MPFEM 의 장점.
- *"in this case, the force chain structure is mainly determined by the contacted SiC particles."* (초록) — 단단한 상의 힘 사슬.
- 우리 문장 (한정어 포함): "2D Al/SiC MPFEM (Huang 외 2017) 에서 단단한 SiC 는 탄성 변형체로서 맞닿은 사슬로 하중을 지고, 정렬 충전에서는 입자 미끄럼이 없어 입자 간 마찰의 효과가 거의 없었다 (그림 3)."

---

## 10. 주의 / 한계 (over-claim 방지 + **이 논문에 대한 비판**)

### 10-A. 우리가 전이할 때의 한계

- **소재 · 차원**: Al/SiC 금속 · 세라믹 2D ≠ NCM811 + LPSCl 3D.  절대값 · 조성 법칙 전이 0 건.
- **크기 역할 반대**: 단단한 상이 작고 소수 (이 논문) ↔ 크고 다수 (우리).
- **SiC = 탄성 · 깨지지 않음**: NCM 은 깨진다 (우리 Auerbach · R7).  SiC 의 > 1000 MPa 응력은 파괴 없이 쌓인 값이다.
- **탈압 없음**: R4 에는 쓸 수 없다 (그 몫은 `zhou2019_…` · `pycompact2025_…`).

### 10-B. ★ 이 논문 자체의 약점 (비판적으로)

1. **마찰 설정이 서로 어긋난다** — 표 2 *"Friction between particles: 0"* ↔ 본문 *"the friction between the particles and die is set to be μ = 0"* ↔ 그림 3 · 4 의 입자 간 µ 0.2 / 0.  그림 5–11 의 µ 를 알 수 없다.
2. **초기 밀도 숫자가 어긋난다** — 그림 7 캡션 case I **0.7541** ↔ 본문 **0.7451**.
3. **그림 5 의 범례가 패널마다 다르고 곡선이 단조가 아니다** — 5a 에서 SiC 20 % 가 10 % 보다 조밀한 구간이 있는데 본문은 *"usually needs larger compaction pressure"* 로 넘긴다.  40 · 50 % 곡선이 ≈345 MPa 에서 끝나는 이유가 없다 (계산 중단으로 읽힘 [추정]).
4. **영역 B 의 "elastic deformation is dominant" 해석이 의심스럽다** — 그 구간에서 ρ 가 ≈0.79 → 0.90 으로 오른다 (그림 11 판독).  탄성만으로 그만큼 치밀해질 수 없다 — 재배열 + 소성 시작으로 읽는 게 맞다 [카드 추론].  변형 에너지 "KJ" 는 2D 두께 가정이 없어 물리 단위로 읽을 수 없다.
5. **메시 수렴 시험이 없다** — 적응 · 다시 메시를 썼다고만 적었다.  적응 기준 · 다시 메시 빈도도 없다.
6. **실험 대조가 없다** — 문헌 경향과 *"agreeable"* 정성 비교뿐 · *"this also illustrates the robustness of our model and the accuracy of simulation results"* 는 과장.
7. **재현 값이 빠졌다** — 입자 크기 · 수 · 다이 폭 · 펀치 속도 (§3-5).  입자 수는 영상 계수로만 알 수 있었다.
8. **충전 1 개씩** — 조성 · 크기비마다 시드 반복이 없어 그림 5a 의 비단조가 잡음인지 알 수 없다 (그림 7 이 같은 조성에서 충전만 바꿔도 곡선이 갈린다는 것을 스스로 보였다).

### 10-C. frame 규율 재확인

- 이 논문 값으로 우리 MPM · DEM 을 보정하지 않는다 (frame [4]).  인용은 기전 방향 · 설정 선례로만.

---

## 11. 관련 카드 (중복 서술 금지 — 겹치면 넘김)

- `zhou2019_mpfem_2d_copper_powder_die_compaction_release` — 같은 그룹 계열 · 2D Cu 단일 재료 · **탈압 포함** · node-to-segment · 지름당 ≈13 요소.  이 논문을 [17] 로 인용.
- `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` · `cardenasbarrantes2021_soft_rigid_mix_compaction_proceedings` · `cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic` — 2D 강체 + 초탄성 혼합 (NSCD) · φmax(κ) · 같은 크기.  단단한 상 = 강체.
- `martinbouvard2003_dem_composite_cold_compaction` — 무른 + 단단 혼합 DEM (이 논문 [25]) · 단단–단단 하중 분담.
- `demirtas2021_mpfem_hollow_sphere_die_compaction` · `pycompact2025_dem_mpfem_workflow` — 3D MPFEM (단일 재료).
- `bardenhagen2000_mpm_granular_multibody_frictional_contact` — MPM 다물체 마찰 접촉 (우리 F 의 원형).

---

## 12. 용어 (technique mini-glossary)

- **MPFEM** — 입자마다 FE 메시 + 입자 사이 FE 접촉 (`zhou2019_…` §12).
- **segment-to-segment 접촉** — 양쪽 표면 선분끼리 겹침을 막는 접촉 판정 (node-to-segment 보다 대칭).
- **국부 메시 적응 (local adaptivity)** — 오차 기준으로 요소를 국부적으로 쪼개는 것.
- **전체 다시 메시 (global remeshing)** — 뒤틀린 메시를 새 메시로 바꾸고 상태량을 옮기는 것.
- **정렬 SC · HCP 이원 충전** — 큰 원판을 정사각 · 육각으로 놓고 빈자리에 꼭 맞는 작은 원판을 넣은 배열.
- **Heckel 식** — ln[1/(1−ρ)] = M·P + A.  M (이 논문 이름 "densification coefficient") 이 클수록 잘 눌린다.
- **닫힌 공극 (isolated enclosed pores)** — 단단한 입자들이 둘러싸 무른 입자가 들어가지 못한 공극.

---

## 🗨️ Q&A 로그

- (2026-11-25 · litdb-curator) 입자 수 · M 값은 원문에 없어 그림 1b 영상 계수와 그림 5b · 6b 화소 열 단면으로 되짚었다.  둘 다 원고에 인쇄값처럼 옮기지 않는다.
