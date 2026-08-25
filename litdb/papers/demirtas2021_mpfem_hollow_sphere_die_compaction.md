<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md / alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md -->
# 중공(hollow) 구의 다이 압밀을 **3D MPFEM**(입자마다 FE 메시 = 진짜 **형상** 소성)으로 — ★★★ 저자들이 본문에서 **"DEM 은 압밀 중 변형된 입자 표면을 보정할 수 없다"** 고 명시 = 우리 3층 지도 **층③(입자 형상 소성 = 연속체 소관)** 의 **제3자 근거** — Demirtas & Klinzing (Merck, Powder Technology 2021)

> slug `demirtas2021_mpfem_hollow_sphere_die_compaction` · DOI `10.1016/j.powtec.2021.06.004` · type `MPFEM (Abaqus/Explicit 3D 다입자 유한요소; 입자당 C3D8R ~1650 요소, elastic-perfectly-plastic E/σ_y=100·ν 0.3, general contact + Coulomb μ 0.1, mass scaling) + DEM(다이필 초기배치 전용) + 실험(HPMCAS 분무건조 중공입자 정제압밀·XRCT·eSEM)` · PDF `a997a14a-Understanding_die_compaction_of_hollow_spheres_using_the_multiparticle_finite_element_method_MPFEM.pdf` · digested `2026-08-25` · status ✅

---

## 0. 이 논문이 우리에게 *왜* 특별한가 (한눈 positioning)

우리 litdb 의 **접촉모델 3층 지도**(`contact_models_layer_map.md`)가 내리는 판정은 이것이다:

> **① 접촉 힘–변위 LAW 의 소성** (Thornton–Ning 항복캡, EEPA, Luding no-cap, So 2021/2022 H-cap …) → DEM 문헌에 **여럿** 있다.
> **② 접촉 *면적* 의 소성 보정** (Storåkers c², Mesarović–Fleck pile-up, 우리 Stage-E Tabor+volume) → 있다.
> **③ 입자 *자신의 형상*이 변하는 소성** (평탄화·좌굴·void-fill 흐름) → **어떤 DEM 도 못 한다. 연속체(MPFEM / MPM) 소관.**

우리 원고는 "그래서 MPM 을 도입했다" 를 이 판정 위에 세운다.  문제는 지금까지 ③이 **우리 자신의 판정**뿐이라
리뷰어가 *"그건 너희 주장 아니냐"* 로 칠 수 있다는 것이었다.

**이 논문이 그 구멍을 정확히 메운다.**  제약회사(Merck) 소속 저자 2인이, ASSB 와 무관한 맥락에서,
서론에서 DEM 과 MPFEM 을 나란히 놓고 **DEM 이 못 하는 것을 명시**한 뒤 **입자마다 FE 메시를 주는 방법**으로
넘어간다.  그리고 그 형상 변화(평탄화·좌굴·**접촉 개구**·스프링백)를 **그림으로 실증**하고 **실험(XRCT/eSEM)으로
대조**한다.  즉 우리에게 이 논문은:

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| ③ "DEM 은 형상 소성을 못 한다" 의 **제3자 진술** | §1(p.35) 원문 3문장 — **§7-A 에 verbatim 전사** |
| ③ 의 **실증** (형상이 진짜 변한다) | Fig 4b(구→드럼) · Fig 9(평탄화→좌굴) · Fig 12c-d(주름진 리본, 실험과 동형) · Fig 13a(recoil) |
| ①② 로 때우는 DEM 이 **왜 부족한가** 의 제3자 진술 | "DEM requires a plastic-contact law …" + "[27–31] 접근들은 **특별한 보정**이 필요해 DEM 계산비용을 올린다" |
| MPFEM 대신 **MPM 을 택한 것이 정당한가** 의 판정 근거 | **입자 2000개 미만 / wall clock <60 h** (저자 명시) + **Fig 3 런타임 표**(메시 5.6× → 비용 4.7×) |
| 우리 MPM(연속체)의 **약점**에 대한 제3자 진술 | 같은 서론이 연속체(DPC/Cam-Clay)를 "개별 입자 특성을 못 담는다" 로 비판 — **우리에게도 그대로 적용** |
| **면적형 관측량이 늦게 수렴**한다는 선례 | Fig 5 — **응력은 메시 무관, 접촉면적은 3363 요소까지 단조 감소·미수렴** |

⚠ **소재는 완전히 다르다** — HPMCAS(제약용 고분자)를 **분무건조한 중공(속 빈) 입자** vs 우리 LPSCl(중실 황화물 SE) +
NMC811.  **절대값·조성 전이 금지.**  이 카드에서 우리가 가져가는 것은 **방법론·기전·판정**뿐이다.

---

## 1. 한 줄 요약

각 입자를 **완전한 유한요소 메시로 채운 변형 가능한 물체**로 놓는 3D MPFEM 으로 **중공 구**의 다이 압밀을
**RD 0.90** 까지 계산하고, **입경/껍질두께 비 `d/w` 가 지배 변수**(입경 `d` 자체는 거의 무관)임을 보인 뒤,
분무건조 HPMCAS 정제 압밀 실험(XRCT·eSEM)과 **추세 수준에서 대조**한다.  얇은 껍질일수록 **더 낮은 거시응력에서
전면 항복**(d/w 10 은 RD 0.46 에서 100 % 항복)하고 **평탄화·좌굴**이 일어나며, 좌굴은 **이미 형성된 접촉을 다시
열어버린다**.  우리에게 값진 것은 중공 구 자체가 아니라 — 저자들이 서론에서 **DEM 이 "변형된 입자 표면을 보정할 수
없다"** 고 명시하고, 그 대안으로 **입자마다 FE 메시**를 준다는 **방법론적 진술과 실증**이다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Ahmet Demirtas** (교신, ahmet.demirtas@merck.com), **Gerard R. Klinzing** |
| 소속 | **Merck & Co. Inc., Kenilworth, NJ 07033, United States** (제약 — 정제(tablet) 압밀 공정) |
| 저널 | **Powder Technology 391 (2021) 34–45** |
| DOI | **10.1016/j.powtec.2021.06.004** |
| 이력 | Received 2021-03-20 · Revised 2021-06-03 · Accepted 2021-06-05 · Online 2021-06-08 |
| 키워드 | Multi-particle finite element analysis · Hollow particle compaction · Particle size · Particle shell thickness · Powder compaction behavior |
| 소재 | **HPMCAS** (hydroxypropyl methylcellulose acetate succinate, M-grade, Ashland) **분무건조 중공 입자** — 시뮬레이션은 **무차원**(E/σ_y=100) |
| 연구유형 | **3D MPFEM (Abaqus/Explicit)** + DEM(초기배치 전용) + **실험**(정제 압밀 + XRCT + eSEM) |
| 이해상충 | 없음 선언 |
| 감사 | Rachel King, Richard Huang (분무건조 입자 제작) |

**자기 위치 선언 (저자 원문, 결론부 p.44)**
> "To the authors' knowledge, this is the first study investigating the compaction behavior of the hollow
> particles in 3D MPFEM with the number of particles ranging from 411 to 1979."

---

## 3. 핵심 수치

> **라벨 규약 (§F1)**
> · **stated** = 본문/표/그림-내-표에 적힌 값
> · **derived** = stated 값에서 *산술로만* 유도 (디지타이즈 아님, 재현 가능)
> · **figure-read ≈** = **그림 픽셀에서 눈으로 읽은 값 — TREND 전용, 오차 ±5–10 %, 정량 인용 금지**
> · **inferred** = 서술에서 방향만 읽은 것 (값 아님)
> ★ 이 카드는 **13개 본문 그림 중 9장(Fig 2,3,4,5,6,7,8,9,10,11,12,13)을 실제로 렌더해서 봤다.**
>   Fig 1(DEM 모식)은 안 봤다.  그림에서 읽은 값은 전부 `figure-read ≈` 로 표시했다.

### 3-1. 모델 구성 (Table 1 전사 + 유도)

| 모델 | 입자 수 (stated) | 외반경 r (stated) | d/w (stated) | **벽두께 w (derived)** | **껍질 부피/외피 부피 (derived)** |
|---|---|---|---|---|---|
| r1–2.5 | **411** | 1 | 2.5 | 0.800 | 0.992 (거의 중실) |
| r1–5 | **520** | 1 | 5 | 0.400 | 0.784 |
| r1–6.25 | **594** | 1 | 6.25 | 0.320 | 0.686 |
| r1–8 | **705** | 1 | 8 | 0.250 | 0.578 |
| r1–10 | **835** | 1 | 10 | 0.200 | 0.488 |
| r1–12.5 | **1003** | 1 | 12.5 | 0.160 | 0.407 |
| r0.75–2.5 | **973** | 0.75 | 2.5 | 0.600 | 0.992 |
| r0.75–5 | **1232** | 0.75 | 5 | 0.300 | 0.784 |
| r0.75–10 | **1979** | 0.75 | 10 | 0.150 | 0.488 |

- 소입자는 대입자의 **75 % 반경**(= 25 % 작다).  **단일모드**(monomodal) — 한 모델에 한 크기만.
- **총 질량 일정** (stated).  ★ **검증 (derived)**: 껍질 부피 × 입자 수 = 1705.7 – 1711.1 (임의단위, 9 모델 평균
  1707.3, **산포 0.3 %**) → 질량 일정 조건이 **산술로 확인된다** ✓
- ★ **Table 1 오타 발견 (derived)**: `r1–12.5` 행 설명문이 "a d/w ratio of **12**" 라고 적혀 있으나, d/w=12 로 계산하면
  총질량이 다른 8개 대비 **+3.6 %** 어긋나고 d/w=**12.5** 면 **+0.2 %** 로 맞는다.  ⇒ **모델명(12.5)이 옳고 설명문이 오타.**
  (본문·Fig 7·Fig 8 범례도 전부 12.5 로 쓴다.)
- **다이 반경 = 10 r_L** (대입자 외반경의 10배).  DEM 다이 높이는 "임의로 크게".

### 3-2. 압밀 (거시) 결과

| 항목 | 값 | 라벨 |
|---|---|---|
| **목표 상대밀도 RD** | **0.90** (5 초 만에 도달하도록 상부 펀치 속도 BC) | stated |
| **초기(다이필 후) RD 범위** | **23.5 % – 45.3 %** | stated (모델별 배정 **미기재**) |
| 초기 RD 추세 | d/w ↓(껍질 두꺼울수록) → 초기 RD ↑ · 입경 ↓ → 다이필 효율 **약간** ↑ | stated |
| d/w 5 ↔ d/w 2.5 곡선 **교차점** | **Σ_y = 0.48, RD = 0.78** | stated (본문 유일한 좌표값) |
| d/w 10 최종 응력 | RD 0.90 에서 d/w 5·2.5 **보다 낮음**; 궤적상 **RD > 0.9 에서야** 동등 응력 도달 예상 | stated |
| d/w → 최종응력 전이 | **선형이 아니라 sigmoidal**; **전이대 = d/w 5 ↔ 8** | stated (Fig 7d) |
| 입경 효과 | **d/w 고정 시 25 % 입경 감소 → 거시 압밀거동 유의미한 변화 없음** | stated (초록·결론) |

**★ Fig 7d — RD 0.90 에서의 최종 압밀응력 vs d/w (r = 1)**

| d/w | 2.5 | 5 | 6.25 | 8 | 10 | 12.5 |
|---|---|---|---|---|---|---|
| Σ_y (σ_y 단위) | ≈ **0.83** | ≈ 0.79 | ≈ 0.70 | ≈ 0.61 | ≈ 0.58 | ≈ **0.56** |

`figure-read ≈` — **TREND 전용**.  읽히는 것: 상부 plateau(2.5–5) → **급강하(5→8)** → 하부 plateau(10–12.5),
전 구간 낙차 **≈ −33 %**.  본문의 "sigmoidal, 전이대 5–8" 서술과 정합.

**★ Fig 7e — 부피변형 축 `LN(RD/RD₀)`**: 두꺼운 껍질(d/w 2.5)은 **LN ≈ 0.5** 에서 최종응력에 닿고
가장 얇은 껍질(d/w 12.5)은 **LN ≈ 1.3** 이 필요하다 ⇒ **≈ 2.6배 더 큰 부피변형** (`figure-read ≈`).

**★ 초기 packing 을 뒤에서 복원 (derived + figure-read)** — 논문이 안 적은 값
Fig 6·7c 의 **응력 개시 RD**(= 펀치가 분말에 닿는 지점)를 §3-1 의 껍질부피분율로 나누면 **외피 기준 패킹분율**이 나온다:

| 모델 | 응력개시 RD (`figure-read ≈`) | ÷ 껍질분율 | **φ_env (derived)** |
|---|---|---|---|
| r1–10 | ≈ 0.275 | 0.488 | **0.56** |
| r1–5 | ≈ 0.425 | 0.784 | **0.54** |
| r1–2.5 | ≈ 0.545 | 0.992 | **0.55** |
| r0.75–10 | ≈ 0.295 | 0.488 | **0.60** |
| r0.75–5 | ≈ 0.475 | 0.784 | **0.61** |
| r0.75–2.5 | ≈ 0.60 | 0.992 | **0.60** |

⇒ **φ_env ≈ 0.55 (r1) vs ≈ 0.60 (r0.75)** — 여섯 모델이 크기별로 **한 값으로 모인다**.
이것은 저자들의 정성 서술("as the particle size decreased, the die filling efficiency increased slightly")에
**≈ +10 %** 라는 크기를 붙여 준다.  ⚠ 어디까지나 `figure-read` 기반 **derived** 값 — 정량 인용 금지.

⚠ **"초기 RD 23.5–45.3 %" 와 위 개시 RD(0.275–0.60)는 서로 다른 양이다.**  Fig 2 를 실제로 보면
**상부 펀치가 분말 위에 떠 있는 head-space 가 있다** — 즉 stated 초기 RD 는 *펀치 간격 기준*(공간 포함)이고,
개시 RD 는 *펀치가 분말에 닿은 시점*이다.  ⚠ 논문은 **RD 정의식도 초기 펀치 위치도 적지 않는다** → §10-B-8.

★ **RD 정의 (inferred)**: "가장 얇은 껍질이 **intraparticle porosity 때문에** 초기 RD 가 가장 낮다" 는 서술에서,
RD = **껍질 재료 부피 / 펀치 사이 부피** 이고 **입자 내부 공극도 porosity 로 센다**는 읽기가 유일하게 정합적이다.
⇒ **RD 0.90 도달 = 내부 공극이 대부분 닫혔다 = 껍질이 실제로 무너졌다** (§7-A 형상소성 실증 논거).

### 3-3. 항복 (YV/TV = 항복 요소 부피 / 전체 요소 부피)

정의(stated): "the yielded volume was calculated by summing the total volume of the **elements** within all particles
that exhibited **non-zero equivalent plastic strain**" → YV/TV = 1 이면 전 입자 전 요소가 항복.

| 모델 | 전면 항복(YV/TV = 1) 도달 RD | 라벨 |
|---|---|---|
| **r1–10** (얇음) | **0.46** | stated |
| **r0.75–10** (얇음) | **0.47** | stated |
| **r1–5** (중간) | **0.73** | stated |
| **r0.75–5** (중간) | **0.72** | stated |
| **r1–2.5** (두꺼움) | 도달 **못 함** — 종료 시 **97 %** | stated |
| **r0.75–2.5** (두꺼움) | 도달 **못 함** — 종료 시 **98 %** | stated |
| r1–6.25 / r1–8 / r1–12.5 | 최종 RD 전에 전면 항복 (**RD 값 미기재**) | stated |

**★ Fig 8b — YV/TV = 0.9 에 필요한 거시응력 Σ_y** (`figure-read ≈`, TREND 전용)

| d/w | 12.5 | 10 | 8 | 6.25 | 5 | 2.5 |
|---|---|---|---|---|---|---|
| Σ_y @ YV/TV = 0.9 | ≈ 0.09 | ≈ 0.10 | ≈ 0.13 | ≈ 0.17 | ≈ 0.23 | ≈ **0.50** |

⇒ **≈ 5–6배 스프레드**.  Fig 8a 를 보면 아홉 곡선이 **d/w 순서대로 완벽히 정렬**하며(색 순서 그대로),
같은 d/w 안에서 **소입자(파선)가 대입자(실선)보다 오른쪽**에 있다 — 본문의 "small particles require slightly
higher forces … larger contributions of inter-particle friction per unit volume" 와 정합.
★ 또한 **항복 개시는 각 모델의 응력 개시 직후 곧바로** 일어난다 (Fig 8a 의 상승 시작 RD ≈ Fig 6 의 응력 개시 RD).

- ⚠ **전면 항복이 재료 응력을 더 못 올린다**: elastic-perfectly-plastic 이라 "plastic strains on deformed elements
  do not contribute to further increase in local particle stresses" → 얇은 껍질은 **거시응력이 낮게 유지**된다.

### 3-4. 실험 수치

| 항목 | 45 °C SDI | 80 °C SDI | 라벨 |
|---|---|---|---|
| 입경 d (근사) | **~90 µm** | **~120 µm** | stated (⚠ 저자가 **정성적**이라 명시) |
| 벽두께 w (근사) | **~12 µm** | **~6 µm** | stated (동일 경고) |
| **d/w** | **7.5** | **20** | stated |
| 형상 | 덜 구형, **깨진 껍질 조각 다수**(Fig 10a–c) | **더 구형**, 매끈, 조각 적음(Fig 10d–f) | stated + figure-read |
| 정제 직경 | 2.023 ± 0.010 mm | 2.016 ± 0.005 mm | stated (Table 2) |
| 정제 두께 | 1.398 ± 0.024 mm | **1.552 ± 0.077 mm** | stated (Table 2) |
| 정제 무게 | 3.82 ± 0.26 mg | 3.76 ± 0.11 mg | stated (Table 2) |
| **in-die → out-of-die 팽창** | **61 %** | **78 %** | stated |
| **RD 0.90 에서의 압밀응력** | ≈ **47 MPa** | ≈ **35 MPa** | `figure-read ≈` (Fig 11a) |
| 최대 도달 응력 / RD | ≈ 52 MPa @ RD ≈ 0.93 | ≈ 50 MPa @ RD ≈ 0.98 | `figure-read ≈` |

★★ **Fig 11a 가 이 논문의 유일한 물리단위 응력 축이다** (Σ_y 를 **MPa** 로, 0–60 MPa 범위).
시뮬레이션은 무차원이므로 **물리 응력은 여기서만 나온다.**
- **정량 대조 (`figure-read ≈`)**: RD 0.90 에서 두꺼운-껍질/작은 입자가 얇은-껍질/큰 입자보다 **≈ +34 %** 높은 응력을
  요구한다(47 vs 35 MPa).  같은 지점에서 **MPFEM(Fig 11b)** 은 r0.75–2.5 ≈ 0.75 vs r1–10 ≈ 0.575 = **≈ +30 %**.
  ⇒ **상대 격차가 34 % vs 30 % 로 맞는다** — 이 논문의 정량적 실험-모델 일치 중 가장 강한 지점.
  ⚠ 둘 다 `figure-read` 라 **±5–10 %** 오차.  "34 vs 30" 을 유효숫자 두 자리로 인용하면 안 된다.
- **inlay (RD 0.05–0.2)**: 매우 낮은 RD 에서는 **80 °C(얇은·큰)가 위**에 있다 → 본문의 "initially build stress …
  greater" 를 그림으로 확인.  그 뒤 교차한다.
- ⚠ 두 실험 정제가 **같은 RD 에서 끝나지 않는다** (압축을 *고정 펀치간격 1 mm* 까지 했기 때문): 45 °C 는 RD ≈ 0.93,
  80 °C 는 ≈ 0.98 까지 간다.  시뮬(고정 RD 0.90)과 **종료 조건이 다르다.**

★ **팽창값의 자기정합 검증 (derived)**: 두 팽창률을 각자의 out-of-die 두께에 역산하면
in-die 두께 = 1.398/1.61 = **0.868 mm** (45 °C), 1.552/1.78 = **0.872 mm** (80 °C) — **0.5 % 안에서 일치**한다.
⇒ 61 %/78 % 는 **서로 정합적**이다.  다만 §2.6 의 "**punch separation 1 mm** 까지 압축" 과는 **≈13 % 어긋난다**
(1 mm 기준이면 팽창률이 40 %/55 %).  ⇒ **기준 상태 정의가 본문에 없다** — §10-B-7.

### 3-5. 실험 조건 (재현용)

- **분무건조**: Mobile Minor™ (GEA Niro A/S), HPMCAS M-grade 8 wt% 를 **MEK:물 = 90:10 (질량)** 에 용해,
  출구온도 **45 °C / 80 °C**.  회수 후 트레이 건조.  **추가 가공·첨가제 없음**.
- **압밀**: Huxley-Bertram 유압 compaction simulator, **평면 원형 펀치 Ø2 mm**, 정제당 분말 **4–4.5 mg**,
  다이 충전높이 **16 mm**, **단동(single-action)**, V-profile, **총 punch separation 1 mm 까지**.
  타임라인 = **압축 5 s + 제하 5 s + 배출 2 s (t = 8 s 부터)**, 총 10 s.  ★ 시뮬 5 s 압축은 **이 실험에 맞춘 것**.
- **XRCT**: XRadia Versa 500, 80 kV / 7 µA.  자유분말 = 20× 대물, **0.7 µm/pixel**, 360° **7200 장**;
  정제 = 4× 대물, **3.3 µm/pixel**, **3600 장**.
- **eSEM**: FEI Quanta FEG 250, 저진공 **0.825 Torr**, 가속 **20 kV**, WD ≈ 10 mm, 2차전자 검출기.

### 3-6. ★ 이 논문에 **없는** 값 (정직 목록 — 찾으러 갔다가 없다고 확인한 것)

| 우리가 원한 것 | 상태 |
|---|---|
| 전달물성 (σ_ionic / σ_e / κ) | **n/a** — 순수 역학 논문.  전달 계산·측정 **0건** |
| 물리단위 응력 (시뮬) | **n/a** — **무차원**(E/σ_y = 100).  물리 MPa 는 **실험 곡선(Fig 11a)에만** |
| E, σ_y, 진밀도의 실제 물성값 | **n/a** — 비(ratio)만 지정.  HPMCAS 의 E·σ_y·ρ_true 어느 것도 없음 |
| "DEM 이 무너지는 RD" 의 **수치 문턱** | **n/a** — 정성 서술만 ("low relative density … loose powders", "significant approximations") |
| **전체 모델**의 wall clock / 하드웨어 / 코어 수 | **부분** — "**<60 h**" 상한(stated) + **8입자 모델 런타임 표**(Fig 3, §4-3).  **전체 모델별 시간·머신·병렬도는 없음** |
| 모델 전체 요소 수 | **n/a** — 입자당 값만.  총합 미기재 (§4-3 에 우리 산술 있음, derived) |
| 시드/반복 (통계) | **n/a** — 모델당 1 실현.  산포·오차막대 없음 |
| PSD | **n/a (시뮬)** — 단일모드.  실험은 **정성 측정**만 ("by no means does this represent a statistical analysis") |
| 마찰계수 민감도 | **n/a** — μ = 0.1 **한 값**을 입자–입자/펀치/다이벽 **모두** 동일 적용 |
| 점착(cohesion) / 배출(ejection) / 인장강도 | **n/a** — "**due to the lack of cohesive elements**" 로 압축+제하까지만 |
| 요소 왜곡 / 리메싱 진단 | **n/a** — RD 0.9 + 좌굴에서의 C3D8R 왜곡 서술 없음 |
| 좌굴의 **정량화** | **n/a** — 저자 명시: "a quantified extent of buckling … is beyond the scope of this study" |
| 모델별 펀치 속도 | **n/a** — "5 초에 RD 0.9" 만.  ⇒ **모델마다 속도가 다르다** (§4-5 confound) |

---

## 4. 시뮬레이션 방법 ★

### 4-1. 3단계 워크플로 (★ 우리 scaffold 커플링과 같은 계열)

> 원문(p.36): "The model was generated in a three-step process by **coupling DEM and traditional FEM**.
> In the first step, a gravity forced random die filling simulation was carried out using the **DEM** approach.
> In the second step, the **coordinate of each particle center was extracted from the DEM simulations and used as
> the initial particle configuration for the MPFEM**.  Finally, the powder compaction simulation was run by using MPFEM."

1. **DEM**: 중력 랜덤 다이필 → 정착 좌표
2. **Python 스크립트**로 입자 중심 좌표를 MPFEM 모델에 이식
3. **MPFEM**: 압밀 (+ 제하)

★★ **우리와의 결정적 차이 = 인계 시점.**  그들은 **느슨한 다이필 상태**(RD 0.235–0.453)를 넘기고 **압밀 전 과정을
연속체가 한다**.  우리 scaffold 는 **300 MPa 압밀이 *끝난*** DEM 좌표(`atom_2060000`)를 넘긴다.
→ 이 차이가 §7-B 판정의 핵심이다 (CLAUDE.md 2026-08-12 "씨앗이 정답을 인코딩한다" 문제와 직결).

- 둘 다 **Abaqus 2019 (Simulia)** 로 생성·계산.  **Abaqus/Explicit, double precision**.

### 4-2. DEM 부분 (초기배치 전용)

- 목적은 **초기 배치 생성뿐** — 압밀은 DEM 이 **전혀** 하지 않는다.
- 구성: **particle generator + lower punch + die** (Fig 1a).  다이 반경 **10 r_L**, 다이 높이는 "임의로 크게".
- **다이 높이를 크게 잡은 이유 (stated)**: 같은 외경·다른 껍질두께 모델들에 **같은 DEM 배치**를 재활용하기 위해 —
  "this helped to **maintain identical initial particle orientation** for those models".
  ⇒ **d/w 스윕은 같은 패킹 위의 통제된 비교**다 ✓ (반대로 말하면 **패킹 실현은 크기당 1개뿐**).
- **정지 판정**: "run until the **first 2000 particles were settled** in the die, i.e., the average displacement in all
  particles reached a **plateau**".
- BC: **중력 + 전역 접촉**, 마찰계수 **0.1** (ref [36] Procopio & Zavaliangos 2005).
- 단일모드 — 한 번에 대입자 **또는** 소입자만 생성.

### 4-3. MPFEM 이산화 (★★★ 층③ 의 실체) + **비용 표**

| 항목 | 값 |
|---|---|
| 구성 (Fig 2) | 상부 펀치 · 하부 펀치 · 다이 · **개별 메시된 입자들**(그림에서 입자마다 다른 색) |
| 입자 요소 | **C3D8R** (8절점 선형 육면체, **reduced integration**) |
| 입자 모델링 | "Hollow particles were modeled as **solid parts**" (= 껍질을 **3D 연속체**로; shell 요소가 아니다) |
| 전역 seeding | **≈ 0.125** (r = 1 기준, 즉 반경의 1/8) |
| 입자당 요소 수 | **1650** (메시 연구로 선정) |
| 두께방향 구획 | **3 section** — 바깥 두 층 각각 **두께 0.05**, 나머지는 전역 seeding 0.125 |
| 펀치·다이 | **3D discrete rigid body** (변형 없음) |
| 접촉 | **general explicit contact detection** + **Coulomb 마찰** + **penalty formulation** |
| 마찰계수 | **0.1**, 입자–입자 / 입자–펀치 / 입자–다이벽 **전부 동일** |

**★★ Fig 3 안의 표 (stated — ⚠ PDF 텍스트층에는 없고 그림 안에만 있다.  렌더해서 읽었다)**

| 입자당 요소 | 600 | 1059 | **1650 (생산)** | 1800 | 3363 |
|---|---|---|---|---|---|
| 입자당 절점 | 808 | 1420 | **2208** | 2408 | 4492 |
| 입자당 **표면 절점** | 202 | 355 | **552** | 602 | 1123 |
| **8입자 모델 총 런타임 (min)** | **46.3** | **53.0** | **72.1** | **98.3** | **218.2** |

★ **비용 법칙 (derived)**: 요소 **5.61배**(600 → 3363) → 시간 **4.71배** = 지수 **≈ 0.90**.
명시적 동역학의 순수 비용은 요소수 × 스텝수 ∝ N_el^(4/3) 이어야 하는데 관측이 ≈1.0 에 가깝다 ⇒
**mass scaling 이 Δt 를 사실상 고정시키고 있다**는 뜻으로 읽힌다 (§4-5 와 정합).  ⚠ 우리 해석.
★ **표면 절점 수**(202 → 1123)는 **접촉 탐색 비용**의 직접 구동자다 — MPFEM 이 비싼 두 번째 이유.

★ **총 요소 수 (derived, 대략)**: 1650 × 1979 ≈ **3.3 M** (가장 큰 모델), 1650 × 411 ≈ 0.68 M (가장 작은 모델).
⚠ 입자당 1650 은 **r1–5 기준**으로 선정된 값이고 껍질두께가 다르면 요소 수도 달라진다 — **자릿수 감각용**.
⚠ 8입자 72.1 min 을 1979 입자에 선형 외삽하면 ≈ 297 h 로 **stated <60 h 를 5배 초과**한다
⇒ **병렬화/설정이 다르다**는 뜻이므로 **단일 per-element 비용으로 외삽하지 않는다** (§7-B-2).

★ **두께방향 요소 수 (derived)**: 바깥 두 층(0.05 + 0.05 = 0.10) + 나머지를 0.125 로 seeding →
d/w 12.5 (w = 0.16) → **3 요소**; d/w 10 (w = 0.20) → **3 요소**; d/w 5 (w = 0.40) → **≈5**; d/w 2.5 (w = 0.80) → **≈8**.
⇒ **가장 얇은 껍질은 두께방향 3 요소** — 좌굴(굽힘 지배)을 1차 감차적분 육면체 3층으로 푸는 것은 **얇은 쪽 한계**
(§10-B-2).  Fig 3 의 절단 구 그림에서 껍질 두께방향 요소층이 눈으로 확인된다.

### 4-4. 재료 모델 — **무차원** (★ 우리와 직접 비교되는 지점)

- **elastic-perfectly plastic**, **E/σ_y = 100**, **ν = 0.3**.
- 원문: "The MPFEM material property definition in this study is **based on previous studies**, and it allows to
  present the results in a **dimensionless domain** [36,53,54]." ([36] Procopio–Zavaliangos 2005, [53] Hertzberg,
  [54] **Mesarović–Fleck 2000** = 우리 카드 `mesarovicfleck2000_dissimilar_elastoplastic_indentation`)
- ★ **정규화 확인 (figure-read, 확정적)**: Fig 9 의 컬러바가 "S, Mises (Avg: 75 %)" 에 **0.000 → 1.000** 이고
  Fig 13a 컬러바가 "Mises stress **0 → 1**" 이다.  **완전소성 재료의 Mises 최대값 = σ_y** 이므로
  **모든 응력은 σ_y 로 정규화돼 있다**.  ⇒ Fig 7 의 `Σ_y ≈ 0.83` = **0.83 σ_y**.
  ⚠ 논문은 정규화 식을 **명시하지 않는다**(eq 3 은 날 것) — 위는 컬러바로부터의 **확인**이다.
- ⚠ **재료 선택이 물리가 아니라 부분적으로 수치 사정** — 원문: "Since material property selection **directly
  influences the stable time increment**, i.e., the total run time of the simulation and the accuracy of the results,
  an **optimized selection must be made** on material properties."
  ★ **우리 18× 연화와 같은 종류의 고백**이다 — 다만 그들은 비(E/σ_y)를 **물리 밴드 안**에 두었고 우리는 밖으로
  끌고 나갔다 (§7-B-4 비교표).

### 4-5. 시간적분 · mass scaling · **준정적 판정** ★ + ⚠ **재하율 confound**

- 안정 시간증분 (eq 1): `Δt ≤ min( δ · √(ρ / (λ̂ + 2μ̂)) )` — δ = 요소 특성길이, λ̂·μ̂ = Lamé, ρ = 밀도.
- **mass scaling** 채택: 입자 **밀도를 인위로 올려** Δt 를 키운다 (refs [36,56,57] = Procopio–Zavaliangos,
  Martin–Bouvard 2003, Thornton–Antony 2000).
- ★★ **준정적 판정 기준 (stated)**: "the influence of the mass scaling can be controlled by maintaining an
  **energy balance on the ratio of kinetic energy and potential energy**.  In this study, the energy balance ratio
  was kept **below 1 % at RD ≥ 0.6** [36]."
  ⇒ **KE/PE < 1 %** = 제3자·표준 준정적 게이트.  **우리 `--platen-mach` 규율의 문헌 앵커로 쓸 수 있다** (§8-③).
- ⚠⚠ **적용 구간이 헤드라인을 안 덮는다.**  헤드라인 중 하나인 **"얇은 껍질은 RD 0.46–0.47 에서 전면 항복"** 은
  게이트가 걸리지 않는 **RD < 0.6** 구간이다.  Fig 8a 를 보면 d/w 12.5·10·8·6.25 **네 모델이 전부** 그 구간에서
  전면 항복한다 (§10-B-1).
- ⚠⚠ **모델마다 펀치 속도가 다르다 (derived — 논문이 안 짚은 confound)**.  구동은 "**5 초에 RD 0.9 도달**" 이고
  질량은 고정이므로 침대 높이 ∝ 1/RD ⇒ 스트로크 = C(1/RD_i − 1/0.9).
  stated 범위 양 끝(RD_i = 0.235 / 0.453)을 넣으면 스트로크 비 = 3.144/1.097 = **2.87** ⇒
  **가장 얇은 껍질 팔의 펀치가 가장 두꺼운 팔보다 ≈ 2.9배 빠르다** (공칭 변형률로 보면 ≈1.5배, 진변형률로 ≈1.9배).
  ★ **이것은 우리 자신의 "재하율 함정"과 같은 구조**다 (CLAUDE.md 2026-08-06: `vmax = 0.008·(WALL0−FLOOR)` 이
  플래튼 속도를 침대 높이에 비례시켜 두께가 다른 침대의 재하율을 갈라놓았던 것).
  ⇒ **d/w 비교는 재하율이 일치된 비교가 아니다** — 그리고 하필 **가장 빠른 팔이 헤드라인 팔**이다.

### 4-6. 메시 수렴 연구 ★★★ (**응력은 수렴, 접촉면적은 *미수렴*** — 우리에게 가장 값진 방법론)

- 2단계: (i) **8입자 simple-cubic** 축소모델을 RD 0.90 까지 압축(Fig 4) → 최적 메시 선정,
  (ii) coarse / fine / optimal 을 **520입자 full-size**(r1–5)에서 재확인 (Fig 5c,d).
- 검사 지표 **두 개**: **응력 응답 Σ_y** + **정규화 접촉면적 N.C.Area** = (총 접촉면적)/(모델 전체 입자 표면적).
- 저자들이 **왜 두 번째 지표를 넣었는지 명시**한다: "this study requires **another confirmation point** to be
  defined for hollow particles **due to the buckling phenomenon** [58]."

**★★ Fig 5 를 실제로 읽은 결과 (`figure-read ≈`, TREND 전용)** — 곡선은 1/2/3/4/5 s 시각별

| | 8입자 (a,b) | full-size 520입자 (c,d) |
|---|---|---|
| **Σ_y** (600 → 3363 요소) | 5개 시각 **전부 평평** (변화 ≲ 2 %) | 5 s: 0.87 → 0.92 (**+5 %**), 나머지 시각도 ≲ +5 % |
| **N.C.Area** 4 s | **0.64 → 0.57 → 0.53 → 0.535 → 0.49** = **−23 %**, **plateau 없음** | **0.72 → 0.605 → 0.56** = **−22 %**, plateau 없음 |
| **N.C.Area** 1 s | 0.155 → 0.115 = −26 % | 0.115 → 0.065 = **−43 %** |
| **N.C.Area** 5 s (최종 치밀) | 0.90 → 0.885 (거의 평평) | 0.965 → 0.91 (−6 %) |

★★★ **판정**: **응력은 메시 무관, 접촉면적은 단조 감소하며 3363 요소에서도 수렴하지 않는다.**
저자 본문도 같은 취지지만("mesh dependency was observed … prominent in the fourth second"), 그림은 그보다 강하다 —
**중간 시각일수록, 그리고 압밀이 덜 됐을수록 미수렴이 심하다.**

⚠⚠ **그런데 저자들이 고른 "최적" 1650 은 수렴점이 아니다.**  Fig 5b 에서 1650(□)과 1800(△)이
거의 겹치는(0.53 vs 0.535) **비단조 wiggle** 이 있고 그 다음 3363(◇)에서 다시 0.49 로 내려간다.
⇒ **"1650 이 최적" 은 곡선이 평평해져서가 아니라 *꿈틀거려서* 고른 것**으로 읽힌다.  Fig 3 표를 보면
3363 요소는 8입자 모델에서 **218.2 min = 1650 대비 3.03배** 비싸다 ⇒ **면적을 수렴시키는 비용이 감당 안 된다**는
것이 실제 사정으로 보인다 (§10-B-2).

★★★ **우리에게 왜 중요한가**: 이것은 **"힘형 관측량이 수렴했다고 면적형 관측량이 수렴한 것이 아니다"** 의
정량적 제3자 선례다.  우리 SR-01 의 σ_e 격자 미수렴(CL-41: vox 0.15/0.125/0.115 에서 이득이
**+12.3 → +14.4 → +15.5 %** 로 단조 증가하며 **멱법칙 수렴이 성립하지 않음**)은 구조가 같다 —
역학은 진작 안정한데 **면적/표현 부피에 붙은 양**이 계속 움직인다.
⚠ **우리 수치를 이 논문으로 정당화하는 것이 아니다** — 우리 값은 여전히 **하한 표기 필수**.

### 4-7. 경계조건 · 구동 (★ 제어변수 = 밀도, 출력 = 응력)

- 다이·하부 펀치 = **전 자유도 고정**.  **상부 펀치에만 속도 BC** — "so that the model could reach **90 % relative
  density in five seconds**".  ⇒ **단동(single-action)**, 실험과 동일.  Fig 2 에서 **상부 펀치가 분말 위에 떠 있다**.
- **총 입자질량 고정** → 모델마다 초기 RD 가 다르다 (23.5–45.3 %) → 그리고 **펀치 속도도 다르다** (§4-5).
- **응력 판독 (eq 3)**: `Σ_y = (RF_U,2 + RF_L,2)/2 / A` — **상·하부 펀치 반력의 평균**을 펀치 단면적으로 나눈 값.
  ★ 우리 MPM **wallP**(플래튼 반력/면적)와 **같은 계열**이고, 상·하 평균은 **다이벽 마찰로 생기는 상하 비대칭을
  부분 상쇄**하는 표준 규약(ref [60] Cunningham–Sinka–Zavaliangos 2004)이다.
- **Mises 응력 (eq 2)**: 표준 `σ_V = √(½[(σ1−σ2)² + (σ1−σ3)² + (σ2−σ3)²])`.

★★ **제어/판독 방향이 우리와 반대**: 그들은 **RD 를 목표로 몰고 응력을 읽는다**.
우리 MPM scaffold 는 (servo 규약에서) **응력을 목표로 몰고 porosity 를 읽는다**.
그런데 우리 플래튼 정본(`docs/mpm_platen_kinematic_stop_defect.md` rev6 §31)이 이미 판정하기를,
scaffold 런에서 **porosity 는 독립 정보를 담지 않는다**(solid_vol 은 씨앗 시점 상수, 출력은 wall_z 하나) —
**반증 가능한 출력은 응력-정지 두께 하나**다.  ⇒ **이 논문의 규약(밀도 제어 → 응력 판독)이 우리가 자체 리뷰로
도달한 결론의 제3자 선례**다 (§8-④).

### 4-8. ★★★ 입자 처리 — **진짜 형상 소성인가?** (DEM판 "무질서 처리")

| 축 | 이 논문 (MPFEM) | 우리 DEM (LIGGGHTS) | 우리 MPM |
|---|---|---|---|
| 입자 표현 | **입자마다 완전한 FE 메시** (C3D8R ~1650, 표면 절점 552) | **영원한 강체 구** | 배경격자 위의 **material point** 집합 |
| 형상 변화 | **✅ 있다** — 평탄화·좌굴·접촉 개구 | **❌ 없음** — δ overlap 이 프록시 | **✅ 있다** — J2 등적 흐름 |
| 소성 종류 | **층③ (SHAPE)**; 층①②는 접촉 알고리즘이 자동 처리 | **층① (CONTACT LAW)** + 층②(Stage-E 면적 사후보정) | **층③ (SHAPE)** |
| 입자 개별성 | **✅ 유지** (별개 물체, 마찰 미끄럼·분리 가능) | ✅ 유지 | **❌ 상실** (SE 는 단일 연속체장; AM 은 동결 마스크로만 구분) |
| 형상 자유도 | 구 외에 **불규칙 형상·내부 미세구조** 가능 (저자 명시; 이 논문은 구만) | 구 고정 | 임의 형상 (씨앗 기하로 결정) |
| 크기 분포 | **단일모드** | **다분산 12:4:1** | 씨앗 따라감 |

**실증 근거 — 그림을 실제로 보고 적는다**

1. **Fig 4b (8입자 축소모델, RD 0.9)** ★ — 원래 simple-cubic 으로 놓인 **구 8개가 위아래가 납작한 "드럼/팬케이크"
   형태**로 변했다.  이웃과 닿은 자리에 **평평한 접촉 facet** 이 생기고 적도부는 **불룩(pile-up)** 하다.
   FE 메시선이 그대로 보여서 **요소가 실제로 늘어나고 눌린 것**이 확인된다.
   ⇒ *"구가 겹친 것"이 아니라 "구가 다른 형상이 된 것"* 을 한 장으로 보여주는 그림.
2. **Fig 9 (Mises 단면, 1 s / 2.5 s / 5 s × d/w 2.5·5·10 × r1·r0.75)** ★★★ — 원문:
   "upon final compression, the particles in the **d/w 2.5 model have relatively maintained their spherical shape**.
    However, as the shell-thickness decreases, there is a **significant amount of particle flattening**.
    In addition, the **d/w 10 particles start to show a buckling behavior where it appears that contact that was
    initially made has now opened**."
   **우리가 그림에서 실제로 본 것**:
   - **1 s**: d/w 2.5 는 거의 전부 **파랑(σ_V ≈ 0, 미항복)** — r0.75–2.5 는 **완전히 파랑**.
     d/w 5 는 청록/초록이 섞이고, **d/w 10 은 이미 초록–빨강이 넓게 퍼져 있다** ⇒ **얇은 껍질이 먼저 항복** ✓
   - **2.5 s**: **d/w 10 은 거의 전면 빨강(= σ_V = σ_y, 전면 항복)**; 2.5 와 5 는 아직 섞여 있다 ✓
   - **5 s**: d/w 2.5 → **다각형(허니콤) 셀** — 구가 눌려 다면체가 됐지만 윤곽은 여전히 둥글다.
     d/w 5 → 다각형 + 내부 공극 링이 남아 있다.
     **d/w 10 → 물결치는 주름·겹층 리본** = 껍질이 접히고 좌굴한 형상.  **입자 경계가 원형이 아니다.**
3. **Fig 12 (실험 ↔ 시뮬)** ★★★ — (a) 정제 상면 eSEM(400 µm bar): 입자들이 **가운데가 함몰된 크레이터/도넛**
   모양.  (b) 단면 eSEM(40 µm bar): **구겨진 호일 같은 주름진 리본**.
   (c) MPFEM r1–10 상면: **같은 크레이터 패턴**.  (d) MPFEM 단면: **같은 주름 리본**.
   ⇒ 시뮬의 좌굴 형상이 실물과 **눈으로 봐서 같은 종류**다.  이 논문의 가장 설득력 있는 검증 그림.
4. **Fig 13a (제하 후 중앙 단면)** ★ — d/w 10 패널은 주름 리본, d/w 2.5·5 는 내부 공극(파란 코어)이 남은 다각형 셀.
   각 패널 오른쪽의 **빨간 양끝 화살표 = recoil 거리**가 **d/w 10 에서 눈에 띄게 길다**.
   Fig 13b XRCT 실물 단면도 **같은 주름 리본**이고, **파란 원**으로 표시된 무너진 중공 입자가
   시뮬 d/w 10 패널의 같은 형상과 화살표로 연결돼 있다.  정제 상·하면의 **볼록/오목 곡선**은 빨간 파선으로 표시.

**요소 수준 근거**: YV/TV 정의 자체가 "**non-zero equivalent plastic strain 을 가진 요소들의 부피 합**" —
즉 **입자 내부의 소성변형장**이 존재한다.  강체 구 DEM 에는 그런 장이 없다.

★★ **왜 "접촉 개구" 가 결정적인가**: 강체 구에서 접촉이 열리려면 **중심 간 거리가 멀어져야** 한다.
여기서는 **중심은 계속 가까워지는데도** 껍질이 안으로 꺼지면서 접촉면이 사라진다.
= **역학이 접촉망의 *위상*을 바꾸는 사건**.  DEM 은 원리적으로, 우리 MPM(단일 속도장 → 접촉면 용접)도 실질적으로
못 낸다.  **전달 관점에서 우리 사각지대**다.

### 4-9. 실험 방법 요약 + 대응의 한계

§3-5 참조.  ⚠ **모델–실험 대응의 한계 3가지**:
- 실험 d/w = **7.5 / 20**, 시뮬 d/w = **2.5–12.5** → **80 °C(d/w 20)는 시뮬 범위 밖**(외삽).
- 시뮬은 **단일모드·무차원·온전한 구**; 실험은 **다분산**이고 Fig 10a–c 에서 보이듯 45 °C 분말은
  **깨진 껍질 조각이 다수** 섞여 있다.
- 종료 조건이 다르다: 시뮬 = **고정 RD 0.90**, 실험 = **고정 펀치간격 1 mm**(→ RD 0.93 / 0.98 로 갈림).
⇒ 대조는 **정성/추세 수준**으로만 성립한다.  단 **RD 0.9 에서의 상대 격차(exp +34 % vs sim +30 %)** 는
`figure-read` 수준에서 잘 맞는다 (§3-4).

---

## 5. Figure set ★ (13개 전부 — ★표는 실제로 렌더해서 본 것)

| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | (a) DEM 모델 모식(particle generator·하부 펀치·다이), (b) DEM 다이필 단계별 스냅샷 | DEM→연속체 인계의 표준 그림 (⚠ **이 그림만 안 봤다**) |
| **2** ★ | MPFEM 모델 3D + 단면.  **입자마다 다른 색으로 개별 메시**돼 있고 **상부 펀치가 분말 위에 떠 있다** | ★ "입자마다 메시" 를 한 장으로 보여주는 그림 · **head-space 확인**(§3-2 RD 정의) |
| **3** ★★ | 메시 연구용 절단 구 5개 + **표(요소/절점/표면절점/8입자 런타임)** | ★★ **PDF 텍스트층에 없는 비용 데이터** — §4-3 |
| **4** ★★★ | (a) 8입자 simple-cubic 초기, (b) **RD 0.9 최종 변형 형상 = 드럼/팬케이크** | ★★★ **형상 소성 실증 ①** (가장 명확) |
| **5** ★★★ | 메시 수렴: (a,c) Σ_y, (b,d) N.C.Area — 8입자 / 520입자, 시각 1–5 s | ★★★ **응력 수렴 ≠ 면적 수렴** — §4-6 |
| **6** ★ | 압밀 초기 Σ_y vs RD, "Thin/Medium/Thick shell" 3군 라벨 + 무응력 구간 inlay | 응력 개시 RD 추출(§3-2 φ_env 복원).  같은 d/w 안에서 **소입자가 더 오른쪽** = 다이필 효율↑ ✓ |
| **7** ★★ | (a) d/w 10/5/2.5 두 크기, (b) r0.75, (c) r1 전 6조건, (d) **최종응력 vs d/w = sigmoid**, (e) Σ_y vs **LN(RD/RD₀)** | ★ (d) 전이대 5–8, 낙차 −33 % · ★★ (e) 초기 패킹 제거 표시법 (우리 `d_h` 접힘과 목적 동일) |
| **8** ★★ | **YV/TV** vs (a) RD, (b) Σ_y — 9곡선이 d/w 순서로 완전 정렬 | ★★ **항복 지표 — 우리 MPM 에 즉시 이식 가능**(§8-⑤) |
| **9** ★★★ | Mises 단면 (1/2.5/5 s) × (d/w 2.5,5,10) × (r1, r0.75), 컬러바 0→1 | ★★★ **형상 소성 실증 ②** + **정규화 확인**(max = 1 = σ_y) |
| **10** ★ | 자유분말 XRCT (a,d) + eSEM (b,c/e,f), 45 vs 80 °C, bar 100 µm | 중공 구조 실물 확인.  ⚠ **45 °C 는 깨진 조각이 많다** = 모델의 온전한 구 가정과 어긋남 |
| **11** ★★ | Σ_y vs RD: (a) **실험 (MPa 축!)**, (b) MPFEM, 빨간 화살표 = 0.9 RD | ★★ **유일한 물리단위 응력** (RD 0.9 에서 ≈47 / ≈35 MPa) + **곡선 대 곡선 검증** |
| **12** ★★★ | 80 °C 정제 eSEM (a) 상면 (b) 단면 + MPFEM r1–10 (c) 상면 (d) 단면 | ★★★ **좌굴의 실험 대조** — 크레이터·주름 리본이 동형 |
| **13** ★★ | 제하 단면: (a) 시뮬 6조건 + **recoil 거리(빨간 화살표)**, (b) XRCT 실물 + 오목/볼록(빨간 파선) | ★★ **스프링백** — 얇은 껍질일수록 큼.  우리 DEM 은 hooke/hysteresis 제하 분기로만 다룸 |

---

## 6. Post-processing ★

| 무엇 | 어떻게 | 우리 대응물 |
|---|---|---|
| **압밀곡선** Σ_y vs RD | 상·하 펀치 반력 평균 / 펀치면적 (eq 3) vs 상대밀도 | MPM **wallP** vs ε (porosity) |
| **부피변형 표시** Σ_y vs LN(RD/RD₀) | 초기 패킹 효율 차이를 제거 (ref [60]) | **Heckel** `ln(1/(1−D)) = K·P + A` (우리 P_y = 138 MPa).  ⚠ 같은 계열이나 **같은 식은 아니다** |
| **항복 밀도** YV/TV | 비영 등가소성변형 요소의 **부피 합 / 전체 요소 부피** | MPM 누적소성변형장 Σdg → **소성 material point 부피분율** (미구현 → §8-⑤) |
| **정규화 접촉면적** N.C.Area | 총 접촉면적 / 전체 입자 표면적 | Stage-E `A_physics` / coverage(Hertz·Tabor) — ⚠ **정규화 기준이 다르다**(우리는 AM 표면 기준) |
| **Mises 응력 단면** | 동일 단면·동일 시각(1/2.5/5 s) 스냅샷, 컬러바 0–1 | `viz_mpm_morphology.py` x–z 단면 |
| **recoil 거리** | 제하 후 중앙단면에서 입자별 튐 거리 측정 (Fig 13a) | 우리 미보유 (DEM 제하 분기만) |
| **실험 미세구조** | XRCT 단면 → d·w **정성** 측정 · eSEM → 구형도/좌굴 | SEM morphology 대조 (우리 vis_zoom ④) |

- 도구: **Abaqus 2019** (DEM + MPFEM 둘 다), **Python 스크립트**(DEM 좌표 → MPFEM 이식),
  **XRadia 전용 소프트웨어**(재구성·가시화).  오픈소스 파이프라인은 없다.

---

## 7. 우리 DEM+MPM 대비  →  `comparison_vs_ours_DEM.md` · `our_dem_baseline.md`

### 7-0. 요약표

| 항목 | 이 논문 (MPFEM) | 우리 | 판정 |
|---|---|---|---|
| **입자 형상 소성 (층③)** | **✅ 있다** (평탄화·좌굴·접촉개구) | **MPM ✅ / DEM ❌** | **같은 편** — 우리 MPM 도입 근거의 제3자 확인 |
| 입자 개별성 | ✅ 별개 FE 물체 | DEM ✅ / **MPM ❌**(SE 단일장) | **그들 우세** |
| 느슨한 상태에서 시작 | **✅ RD 0.235 → 0.90 을 연속체가 전부** | ❌ scaffold 는 **압밀 끝난** 좌표에서 시작 | **그들 우세** (우리 순환성 문제) |
| 입자 수 | **411 – 1979** (<2000, <60 h) | DEM **~33 k** (real_14: AM 457 + SE 32,832) / MPM 10⁷–10⁸ points | **우리 우세 (17×)** |
| 전달물성 σ | **없음** | **σ_ion·σ_e·κ 삼중항 × 2 이산화**(접촉망 + 복셀 FV) | **우리 우세 (압도적)** |
| PSD | 단일모드 | **12:4:1 다분산** (Furnas dip) | **우리 우세** |
| 압력/밀도 스윕 | RD 0.9 단일 목표, d/w 6점 | 다압력 Heckel(100–600 MPa), 조성 스윕 132 케이스 | 축이 다름 |
| 실험 검증 | **압밀곡선 전체 + XRCT/eSEM 형상** (정성 + `figure-read` 상대격차 일치) | Minnmann 단일점(10 % @300 MPa) + Cronau overlap + SEM | **그들이 곡선 대조로 우세**, 우리가 채널 수로 우세 |
| 다이벽 마찰·밀도구배 | **✅ 실물 다이**(μ = 0.1) | ❌ **주기 RVE**(벽 없음) | **그들 우세** (단 우리는 RVE 를 의도) |
| 점착 | **❌ 없음** (배출 계산 불가) | **✅** DEM adhesionStiffness(DMT) / MPM `--coh` | **우리 우세** |
| 재료 비 E/σ_y | **100** (물리 밴드 안) | MPM 1.53/0.30 = **5.1**(3D) · 1.53/0.15 = 10.2(2D) · real LPSCl 24/(0.05–0.30) = **80–480** | ⚠ **우리가 밴드 밖** |
| ν | 0.3 (**중공**이라 부피변화는 공극이 담당) | **0.49** (**중실**이라 부피를 재료가 담당하면 안 됨) | **각자 옳다** — §7-C-3 |
| 재하율 통제 | ⚠ **없음** (팔마다 펀치 속도 ≈2.9배 차, §4-5) | ⚠ 우리도 같은 함정을 겪었고 `--platen-mach` 로 고쳤다 | **우리가 이 축에서는 앞선다** |

---

### ★ 7-A. 층③ 의 제3자 근거 — **원문 그대로**

> ⚠ 아래는 PDF 텍스트층에서 그대로 옮긴 것이다.  ligature(ﬁ→fi)와 줄바꿈 하이픈만 정규화했고
> **단어는 하나도 바꾸지 않았다.**  각색·의역 금지 — 리뷰에서 그대로 대조당하는 문장이다.

#### (A-1) ★★★ DEM 의 한계 — **Powder Technology 391 (2021) 34–45, p. 35** (§1 Introduction)

> "The other commonly used approach is the aforementioned Discrete Element Method (DEM). This method's
> significant benefits are its ability to model a statistically relevant number of particles using Newton's second
> law of motion [20–22]. **Traditionally DEM has been applied to low relative density and low-stress state analyses
> of loose powders, e.g., powder flow. More recently, it has been adapted to account for higher relative densities
> observed during die compaction but not without significant approximations to achieve valid higher relative
> density results.** Since the particles are modeled with simple line elements, the ability to model high strain
> conditions where particle overlap can exist is limited. **DEM requires a plastic-contact law [23,24] to accurately
> represent the plastic deformation, which is vital during powder compaction.** This is especially important for
> pharmaceutical powder compactions, where high relative densities are required to form mechanically stable
> tablets [25,26]. **Another limitation of this method is the technique cannot compensate for the deformed particle
> surfaces during compaction, which plays an essential role in determining the contact pressure between contact
> pairs (particle-particle and particle-tooling).** New approaches were developed in recent studies to address
> these issues in DEM [27–31]. **However, these approaches require particular calibration methods, which increase
> the computational cost of DEM.**"

**한국어 해설 (우리 3층 지도로 번역)**
- "DEM requires a **plastic-contact law** … to accurately represent the plastic deformation" → **층①** 의 존재를 인정.
  참조 [23] = **Storåkers 1997**, [24] = Vu-Quoc 2001 — **우리 지도의 층①/층② 원전들**을 정확히 가리킨다.
- ★★★ "the technique **cannot compensate for the deformed particle surfaces** during compaction, which plays an
  essential role in **determining the contact pressure**" → **층③ 이 DEM 에 없다**는 제3자 진술.
  그리고 그 결손이 **접촉압력(= 접촉면적, = 우리 Holm 협착저항의 입력)** 을 망친다고까지 적는다.
- "[27–31] … **require particular calibration methods, which increase the computational cost of DEM**"
  → **DEM 쪽 고급 처방들이 있지만 보정 의존적이고 비싸다**.  그 [27–31] 이 누구인지가 중요하다:
  | ref | 논문 | 우리 지도에서의 자리 |
  |---|---|---|
  | [27] | Agarwal & Gonzalez, *Int. J. Eng. Sci.* **133** (2018) 26 | **nonlocal(다중접촉) 접촉반경·곡률 보정** |
  | [28] | Garner, Strong & Zavaliangos, *Powder Technol.* **330** (2018) 357 | **고밀도 다이압밀 DEM** |
  | [29] | Gonzalez & Cuitiño, *J. Mech. Phys. Solids* **60** (2012) 333 | **nonlocal contact formulation** |
  | [30] | Harthong et al., *Int. J. Solids Struct.* **46** (2009) 3357 | **고밀도 압밀 DEM** |
  | [31] | Tsigginos, Strong & Zavaliangos, *Int. J. Solids Struct.* **60-61** (2015) 17 | **고 RD 에서의 힘–변위 법칙** |
  ⇒ 이 목록은 우리 카드 `varkey2026_multicontact_elastoplastic_dem`(Giannis 응력기반 multi-contact)이 서 있는
  계보 그 자체다.  **"DEM 쪽 최선의 처방 = 층① + ②의 정교화이고, 그래도 층③은 아니다"** 가 제3자 서술로 성립한다.

⚠ **정직 경고 (반드시 같이 옮길 것)**: 같은 문단의 "**Since the particles are modeled with simple line elements**"
는 **느슨한 표현**이다.  DEM 입자는 "선 요소"가 아니라 강체 구이고, 접촉을 스프링/댐퍼(선 요소)로 잇는다는 뜻으로
읽는 것이 자연스럽다.  **이 구절을 우리 원고에 인용하지 말 것** — 리뷰어가 부정확하다고 반격할 여지가 있다.
인용은 **볼드 처리한 세 문장**(고밀도 근사 / plastic-contact law 필요 / **변형된 표면 보정 불가**)으로 한정한다.

#### (A-2) MPFEM 이 무엇인가 — **p. 35** (같은 절, 다음 문단)

> "One alternative approach to addressing the challenges associated with FEM and DEM techniques is applying the
> multi particle finite element method (MPFEM), which incorporates the characteristics of both FEM and DEM
> approaches [32–38]. **Like DEM, the powder material is modeled as discrete bodies; however, unlike DEM,
> particles are enriched with a full mesh of finite elements. This flexibility makes it possible to model more complex
> irregular particle shapes and internal microstructures.** The particles in MPFEM can be modeled to obey realistic
> material behavior with proper interaction properties. Furthermore, friction, cohesion, and other variables can be
> implemented at the particle scale. Thus, the method does not require extensive simplification; **however, the
> computational cost is the main limitation for this method, limiting the number of particles used in a model.** Even
> though the computational cost is massive compared to other methods, the model's accuracy increases
> proportionally and provides a broader perspective on the problem by presenting the particle scale powder
> movement, stress distribution, and **large particle contact deformation**."

**해설**: "**unlike DEM, particles are enriched with a full mesh of finite elements**" 가 층③ 의 **정의문**이다.
마지막 문장의 "large particle contact deformation" = MPFEM 고유 산출물로 **저자 스스로 꼽은 것**.
동시에 **"computational cost is the main limitation … limiting the number of particles"** 가 §7-B 판정의 근거다.

#### (A-3) ⚠ **연속체(우리 MPM)에 대한 비판도 같은 서론에 있다** — **p. 34–35**

> "The former approach considers the powder as a continuous medium, **which does not incorporate the individual
> particle characteristics, i.e., neglecting the problem's discrete nature** and prediction accuracy **relies on the
> experimental calibration of the constitutive model**. … **This approach does not allow for discrete prediction of
> particle-particle interactions or the influence of particle physical properties (e.g., size and size distribution).**"

★ 그들이 말하는 연속체는 **Drucker-Prager/Cap · modified Cam-Clay** 같은 **균질화 REV** 다
(refs [14] Drucker–Prager 1952, [15] Roscoe–Burland 1968) — 우리 `cap_compaction_heckel.py`(경로 나)가 그것이다.
그러나 **비판의 두 번째 절반("입자–입자 상호작용·입도분포 효과를 못 낸다")은 우리 resolved-grain MPM 에도
그대로 적용된다** — 우리가 이미 자체 실측으로 확인한 바:
- **CORRECTION 2 (2026-06-10)**: 소성 MPM 은 **Furnas dip 을 어떤 보정에서도 재현 못 한다** (재료 스윕으로 증명).
- **SE-rich 과압축**: 연속체 SE 는 DEM 의 강체 SE 가 **잼되는** 자리로 **흘러 들어간다**.
⇒ **이 논문의 서론은 DEM 과 우리 MPM 을 *양쪽 다* 비판한다.**  카드에 유리한 절반만 옮기면 그것이 §F1 위반이다.
정직한 인용 형태: *"they name a DEM limit (deformed surfaces) **and** a continuum limit (no discrete particle
characteristics) — our DEM+MPM division of labour is a response to **both**."*

#### (A-4) ⚠ **없는 것** — "DEM 이 무너지는 RD" 의 **숫자**

찾았으나 **없다.**  이 논문은 DEM 의 고밀도 한계를 **정성적으로만** 말한다
("low relative density and low-stress state … loose powders", "significant approximations").
**RD 몇 % 부터 DEM 이 실패한다** 는 수치는 **본문·표·그림 어디에도 없다.**
⇒ 우리 원고에서 숫자가 필요하면 **다른 출처**로 대야 한다 (예: 카드 `varkey2026_multicontact_elastoplastic_dem`
의 "<20 % porosity 는 비용 때문에 추구하지 않았다" 진술, 우리 값 "강체 구 porosity floor ≈ 20 %").
**이 논문으로 그 숫자를 주장하면 날조다.**

---

### ★ 7-B. MPFEM vs 우리 MPM — 정면 비교 + 판정

#### (B-1) 정면 비교표

| 축 | **MPFEM** (Demirtas 2021) | **우리 MPM** (`mpm3d_compaction.py`, MLS-MPM/Taichi) |
|---|---|---|
| **이산화** | 입자마다 **Lagrangian FE 메시** (C3D8R ~1650/입자, 표면절점 552) | **material point + 배경 Eulerian 격자** (n_grid 256–512) |
| **입자 접촉 표현** | **명시적 surface-to-surface general contact** + Coulomb 마찰(μ = 0.1) + penalty | **격자를 통한 암묵적 접촉** — 단일 속도장 = 접촉면이 **붙어버린다**(no-slip).  AM 은 `am_mask` 로 v = 0 고정 |
| **입자 개별성** | **유지** — 미끄럼·분리·재접촉 가능 | **상실** — SE 는 하나의 연속체장.  두 SE 입자가 닿으면 **용접**된다 |
| **형상 소성 (층③)** | **✅** 평탄화·좌굴·**접촉 개구** | **✅** J2 등적 흐름, void-fill, 코어보존 + 경계평탄화 (SEM 일치) |
| **void-fill 흐름** | ✅ (내부 공극으로 껍질이 무너짐) | ✅ (부피보존 흐름으로 공극 채움; porosity 가 RCP 아래로) |
| **느슨한 상태 재배열** | **✅** (마찰 미끄럼이 물리적으로 존재) | **❌** — 느슨한 침대를 주면 재배열이 아니라 **붕괴/용접**.  그래서 **AM 동결 + 압밀된 좌표**에서 시작 |
| **요소 왜곡 한계** | **있다** — RD 0.9 + 좌굴에서 C3D8R 왜곡.  리메싱 서술 **없음** | **없다** — 격자가 매 스텝 리셋 → 임의 대변형 가능 |
| **계산비용** | **입자 <2000, wall clock <60 h** (stated) · 8입자 모델 **72.1 min** @1650 el (Fig 3) | 10⁷–10⁸ points, **GPU 수십분–수시간** (n_grid 288 kit 런 6685 s; 512 = 115 M points) |
| **입자 수 상한** | **~2000** (2021 기준, 저자 명시) | 씨앗 개수 제한 없음 — real_14 = **33 k 입자** |
| **전달물성 σ** | **불가/미수행** (역학 전용) | **가능** — STEP3 복셀 FV `∇·(σ∇φ) = 0` → σ_ion·σ_e·κ |
| **다분산·Furnas** | 단일모드만 수행 | 씨앗이 다분산이면 따라감 (단 **dip 재현은 못 함** — CORRECTION 2) |
| **점착** | 없음 | `--coh` (SE cold-weld + vdW) |
| **실험 앵커** | HPMCAS 정제 압밀곡선(MPa) + XRCT/eSEM | Minnmann pure-SE 10 % @300 MPa + SEM morphology |

#### (B-2) ★ 판정 — **우리가 MPM 을 택한 것이 맞는가? → 우리 문제에서는 맞다.  단 이유를 정확히 적어야 한다.**

**맞는 이유 3개**

1. **규모.**  저자들이 **자기 입으로** 상한을 적었다 — "the number of particles was kept **under 2000** to maintain
   the wall clock time to **<60 h**".  우리 생산 침대 `real_14` 는 **AM 457 + SE 32,832 ≈ 33.3 k 입자**로
   그들 최대(1979)의 **16.8배**다.
   ★ **우리 산술 (derived, ⚠ 낙관적 하한)**: 요소 수가 입자 수에 선형이라고만 가정해도
   `60 h × 16.8 ≈ 1,008 h ≈ 42 일` **한 케이스**.  우리 코퍼스는 132 케이스다.
   ⚠ 이 추정은 **하한**이다 — 우리 침대는 **12:4:1 다분산**이라 안정시간증분 `Δt ∝ δ`(최소 요소 크기)가
   **가장 작은 SE 입자**에 물린다.  SE(Ø1 µm)를 입자당 1650 요소로 메시하면 δ ≈ 0.125 µm 이고 AM(Ø12 µm)도
   같은 Δt 를 쓴다 ⇒ **단일모드 가정 대비 추가 배수**가 붙는다.
   ⚠ **8입자 72.1 min 을 그대로 외삽하지 말 것** — 선형 외삽은 1979 입자에 297 h 를 주어 저자의 <60 h 와
   5배 어긋난다(병렬화·설정 차이).  그래서 위 산술은 **저자 자신의 상한(<60 h, <2000 입자)** 을 기준으로 했다.
   ⚠ 2021→2026 하드웨어 향상도 미반영이다 (저자들도 "the number of particles … increases with computational
   power advancements" 라고 적는다).  그래도 **자릿수 판정**으로는 충분하다.
2. **전달물성.**  우리 프로젝트 존재 이유(frame[5])의 절반이 **σ 삼중항**이다.  MPFEM 은 여기서 **아무것도 주지
   않는다** — 이 논문에 전달 계산은 0건.  MPM 은 **복셀 격자를 그대로 유한체적 솔버에 넘긴다**(STEP3)
   ⇒ "역학 → 전달" 인계가 **공짜**인데 MPFEM 은 별도 메시 변환이 필요하다.
3. **대변형 안정성.**  우리는 SE 를 300 MPa 에서 porosity 10 % 까지 몰아붙인다.  Lagrangian FE 는 그 변형에서
   요소가 뒤집히고, 이 논문은 **리메싱/왜곡 진단을 전혀 보고하지 않는다**.  MPM 은 격자 리셋으로 그 문제가 없다
   (de Vaucorbeil 2020 리뷰가 MPM 의 첫 장점으로 꼽는 성질 — 카드 `devaucorbeil2020_mpm_after_25_years_review`).

★ **보강 근거 (Fig 3 표)**: MPFEM 은 **면적형 관측량을 수렴시키는 것 자체가 비싸다** — 요소 5.6배 = 비용 4.7배인데
그러고도 N.C.Area 는 수렴하지 않았다(§4-6).  ⇒ "MPFEM 으로 접촉면적까지 수렴시키자" 는 우리 규모에서
**두 겹으로 불가능**하다 (입자 수 × 메시 수렴).

#### (B-3) ★★ **MPFEM 이 우리 MPM 보다 나은 축 — 정직하게**

| # | MPFEM 우세 | 왜 중요한가 (우리에게) |
|---|---|---|
| **①** | **느슨한 상태에서 시작할 수 있다** | RD 0.235 → 0.90 **전 구간**을 연속체가 한다.  우리 scaffold 는 **압밀이 끝난** DEM 좌표를 씨앗으로 쓰므로 **씨앗이 정답을 인코딩**한다 (CLAUDE.md 2026-08-12: `solid_vol` 은 씨앗 시점 상수, MPM 의 유일 출력은 `wall_z` → "일치 = validity 증명서" 는 **순환**).  MPFEM 구조에는 그 순환이 **원리적으로 없다**. |
| **②** | **입자 개별성 → 마찰 재배열이 *물리적으로* 존재** | 우리 18× 연화(frame[2])는 재배열·GB 미끄럼·미세파괴를 유효탄성률에 럼핑한 **프록시**인데, MPFEM 에는 **마찰 재배열이 실제로 들어 있다**.  ⚠ **이 논문은 그것을 검정하지 않았다**(E/σ_y=100 한 값, 연화 연속체와 비교 없음) ⇒ **우리 가설(검정 가능)** 로만 적을 것.  ⚠ 게다가 그들 입자는 **중공**이라 부피 순응을 공극이 담당한다 = **중실 SE 에 미증명**. |
| **③** | **접촉 개구 같은 *위상* 사건** | 좌굴로 **이미 닫힌 접촉이 열린다**.  우리 DEM(강체 구)도 우리 MPM(용접 연속체)도 못 낸다.  전달 관점에서 "역학이 접촉망 위상을 바꾸는 채널" 은 **우리 완전 사각**. |
| **④** | **진짜 접촉면적을 직접 준다** | N.C.Area = **변형된 표면끼리의 실제 접촉면적**.  우리는 DEM Stage-E(Tabor+volume **cap 추정기**), MPM **밴드 coverage**(0.13/0.26 µm)로 **간접 추정**한다.  ⇒ MPFEM(또는 축소 FE)은 **Stage-E 를 검증할 수 있는 유일한 다중접촉 기준선**이다 (§8-⑥).  ⚠ 단 §4-6 대로 **그 면적 자체가 메시 미수렴**이라 기준선도 밴드로만 쓸 수 있다. |
| **⑤** | **실물 다이 + 벽 마찰 → 밀도구배·볼록/오목 면·배출** | 우리는 **주기 RVE** 라 벽이 없다.  정제/펠릿 스케일 엣지 결함은 우리 축 밖. |
| **⑥** | **곡선 대 곡선 실험 검증** | Fig 11 은 압밀곡선 **전체**를 실험과 겹친다.  우리 MPM 주력은 아직 **단일점 앵커**(Minnmann 10 % @300 MPa). |

⇒ **종합 판정**: **규모·전달·대변형 안정성 때문에 우리 문제에서는 MPM 이 옳은 선택**이다.
그러나 **"MPM 이 MPFEM 보다 나은 방법이다" 라고 쓰면 틀린다** — 축이 다르다.
원고에 쓸 정확한 문장: *"MPFEM 은 층③을 가장 직접적으로 푸는 방법이지만 **입자 수 상한(<2000)** 때문에
우리 침대(~33 k)에 못 쓴다.  MPM 은 같은 층③을 **격자 기반으로** 풀어 규모를 얻는 대신 **입자 개별성**을 잃고,
그 손실을 우리는 **DEM scaffold 동결**로 보상한다."*

#### (B-4) ⚠ 재료 파라미터 비교 — **우리가 밴드 밖이라는 사실을 적어 둔다**

| | E/σ_y | ν | 의미 |
|---|---|---|---|
| 이 논문 | **100** | 0.30 | 고분자로서 물리적 밴드 안.  항복 시 탄성변형 ≈ 1 % |
| real LPSCl | **80 – 480** (E 24, σ_y 0.05–0.30) | 0.360 (우리 DFT 쌍 B₀ 26.23) | 물리 |
| **우리 MPM 3D champion** | **5.1** (1.53 / 0.30) | **0.49** | ⚠ 밴드 **밖** — 항복 시 탄성변형 ≈ 20 % |
| 우리 MPM 2D champion | 10.2 (1.53 / 0.15) | 0.49 | ⚠ 밴드 밖 |
| 우리 DEM | E_eff 1.35 (항복캡 **없음**) | 0.30 (접촉모델 입력) | 층① 자체가 부재 |

★ **해석 (우리 것, frame[2] 재확인)**: 우리 연화는 **탄성률만** 낮춘 것이 아니라 **E/σ_y 비를 ~20배 낮춘 것**이고,
그것은 "**항복 전에 훨씬 더 많이 탄성 변형하는 재료**" 를 만든 것이다.  이 논문은 **E/σ_y 를 물리 밴드에 두고도**
RD 0.90 까지 간다 — 단 **중공**이라 부피변화를 **공극이 담당**한다는 결정적 차이가 있다(§7-C-3).
⇒ 이 논문은 우리 연화가 불필요함을 **증명하지 않는다**.  다만 "**층③ 을 제대로 넣으면 물리적 E/σ_y 로도
고밀도까지 간다**" 는 존재증명의 **일부**는 된다 — **중실 입자에 대해서는 미증명**이라고 반드시 붙일 것.

---

### ★ 7-C. 중공(hollow) 이라는 주제 — 전이되는 것과 안 되는 것

#### (C-1) ❌ **직접 전이 금지**
우리 SE(LPSCl)와 CAM(NMC811 1차입자)은 **중실(solid)** 이다.  이 논문의 **헤드라인(d/w 지배, d 무관)** 은
**중공 입자의 명제**이고 우리 계에 그대로 적용되지 않는다.  또 소재가 고분자 vs 황화물/산화물이라
절대응력·절대밀도는 옮길 수 없다(시뮬 응력은 애초에 무차원, 실험 응력은 ~50 MPa 급 = 우리 300 MPa 의 1/6).

#### (C-2) ✅ **전이되는 것 — 크기 무관성(size-independence)**
> 초록: "with a constant ratio of d/w, **changes to particle size (d) did not significantly influence** the global
> compaction behavior."  결론: "a reduction of **25 %** in particle diameter did not significantly influence."

★ **고전 연속체 소성에 길이 스케일이 없다**는 사실의 직접 실증.  크기는 오직
(a) **마찰**(단위부피당 입자간 마찰 기여 — 저자 명시, Fig 8 에서 파선이 실선 오른쪽) 과
(b) **다이필 효율**(우리 derived φ_env 0.55 → 0.60, ≈ +10 %) 을 통해서만 들어온다.
⇒ 우리 CLAUDE.md 2026-06-09 판정 **"SIZE EFFECT is PACKING, not overlap"** 의 **독립적 제3자 확인**이다.
우리 계에서 크기가 크게 작동하는 것(Furnas dip, `d_h` 접힘, Cronau(r_SE) σ_grain)은 전부
**패킹·기하·재료 특유의 크기의존 물성** 때문이지 **역학 구성방정식** 때문이 아니다.

#### (C-3) ✅ **전이되는 것 — 왜 우리는 ν = 0.49 를 써야 했는가의 대조군**
그들은 **ν = 0.30**(압축성)으로도 과압축을 겪지 않는다.  이유는 명확하다 — **중공 입자는 부피변화를 *내부 공극*이
기하학적으로 담당**하므로 구성방정식이 비압축일 필요가 없다.
우리는 **중실 SE** 라 부피변화를 **재료가 담당**하게 두면 (ν = 0.30 → K = 1.27 GPa) **~20 % 부피 압괴**가 나서
porosity 0 % 로 무너졌고, ν = 0.49 (K = 25.5 GPa ≈ 우리 DFT B₀ 26.23)로 고쳤다 (CLAUDE.md 3D 보정 (2)).
⇒ **"그들 파라미터를 그대로 가져오면 안 되는 이유"의 깔끔한 설명.**

#### (C-4) ⚠⚠ **추측 — 다결정 NCM 2차입자의 내부 공극과 연결될 여지** (추측임을 명시)

> **아래는 이 논문이 주장한 바가 아니다.  우리 쪽 유추이고, 검증되지 않았다.**

이 논문의 기전 한 줄은 **"내부 공극을 가진 입자는 더 낮은 거시응력에서 전면 항복하고, 껍질이 평탄화·좌굴하며,
그 과정에서 접촉이 열리기도 한다"** 이다.  우리 계에서 **내부 공극을 가진 입자**는 **다결정(poly) NCM811
2차입자**(1차 grain 사이 공극 + 입계)다.  형식적 유사성은 있다:
- 우리 A10 사이클 화학-역학 트랙이 이미 **`--poly-mode expand-void`** 를 둔다 — SC(2 µm)는 **계면 debond**,
  poly(6 µm)는 **입계 내부 void** 로 갈라 다룬다 (`poly_internal_void_frac` 는 **ASSUMED-FORM**, 앵커 대기).
- 그 축의 미해결 질문이 "**bimodal 증폭 4.4× 중 poly 내부 열화의 몫**" 인데, 이 논문은 "**내부 공극이 있는 입자가
  먼저 항복한다**" 를 **역학적으로 실증한 가장 가까운 제3자 선례**다 (정량: 전면 항복 RD **0.46 vs 0.73**,
  YV/TV 0.9 에 필요한 응력 **≈5–6배 차**).

⚠ **그런데 세 지점에서 유추가 끊긴다 — 원고에 쓸 수 없다**:
1. **위상이 다르다.**  중공 구 = **연속된 껍질 + 하나의 큰 중앙 공극**.  다결정 2차입자 = **다수 1차입자 + 분산된
   입계 공극 + 미끄럼/디본딩 가능한 입계**.  좌굴(굽힘 지배 불안정)은 **연속 껍질**의 현상이라 응집체에 그대로
   성립하지 않는다.
2. **재료 거동이 다르다.**  HPMCAS 는 **연성 고분자**(elastic-perfectly-plastic).  NCM 은 **취성 세라믹** —
   항복이 아니라 **입계 균열**로 간다 (우리 Auerbach/Bucci CZM 축).
3. **우리 모델에서 AM 은 강체다.**  E_CAM 140–161 GPa 로 SE 보다 두 자릿수 가까이 뻣뻣해 scaffold 로 **동결**한다.
   AM 내부 역학을 풀려면 **모델 자체를 바꿔야** 한다.

⇒ **쓸 수 있는 최대치**: *"내부 공극을 가진 입자가 중실 입자보다 낮은 거시응력에서 항복/붕괴한다는 것은
제약 분말의 MPFEM 연구에서 실증된 바 있다 (Demirtas & Klinzing 2021).  다결정 CAM 2차입자로의 전이는
위상·재료 거동이 달라 **미검증**이며, 우리 코드에서는 `--poly-mode expand-void` 의 **가설 형태**로만 존재한다."*
그 이상은 **추측**이다.

---

## 8. 적용 인사이트 (우리 연구에 어떻게 — 실행 가능한 순서)

**① ★★★ 원고 Introduction 의 층③ 논거에 제3자 인용을 붙인다 (즉시)**
현재 우리 논리는 "DEM 은 형상 소성을 못 한다 → 그래서 MPM" 인데 근거가 자체 판정뿐이다.
§7-A-1 의 볼드 세 문장을 인용하면 **제약 산업 연구자 2인의 독립 진술**이 붙는다.
⚠ 인용 시 **§7-A-3(연속체 비판)도 같이 소개**해야 정직하다 — 그들은 DEM 과 연속체를 **둘 다** 비판했고,
우리 DEM+MPM 분업은 **그 두 비판에 대한 응답**이라고 쓰는 것이 가장 강한 형태다.
⚠ `varkey2026` 과 **짝으로** 인용하면 층③ 논거가 **DEM 쪽·연속체 쪽 양쪽에서** 잠긴다.

**② ★★ "응력 수렴 ≠ 접촉면적 수렴" 을 우리 수렴 논의의 문헌 앵커로 (즉시)**
Fig 5 는 같은 메시 스윕에서 **응력 ≲2 % 변화 / 접촉면적 −22~−43 % 단조 감소, plateau 없음**을 보인다.
우리 SR-01 의 σ_e 격자 미수렴(CL-41)과 **같은 구조**다.
⇒ SI 문장: *"contact-area-type observables converge far more slowly than force-type observables; the same
behaviour is reported for MPFEM mesh refinement (Demirtas & Klinzing 2021, Fig 5)."*
⚠ **우리 수치를 정당화하는 것이 아니다** — 우리 값은 여전히 **하한 표기 필수**.
★ 보너스: Fig 3 표가 **그 수렴의 비용**(요소 5.6× → 시간 4.7×)까지 준다 ⇒ "면적 수렴은 비싸다" 를 수치로.

**③ ★★ 준정적 게이트로 KE/PE < 1 % 를 도입 (구현 소)**
현재 우리 준정적 규율은 **마하수**(`--platen-mach`, V/c_P·V/c_S)다.  이 논문의 게이트는
**운동에너지/포텐셜에너지 비 < 1 %** 이고 표준 MPFEM 관행(ref [36])이다.
우리 MPM 은 KE 를 이미 갖고 변형에너지도 계산 가능 → **런마다 자동 기록**하면
(a) 재하율 함정을 **에너지 기준으로도** 잡을 수 있고 (b) 문헌 기준을 인용할 수 있다.
★ **그들은 RD ≥ 0.6 에서만** 걸었다 — 우리가 **전 구간**으로 걸면 그 축에서 우위다.

**④ ★★ scaffold 판독 규약을 "밀도 제어 → 응력 판독" 으로 뒤집는 것을 검토**
그들은 **RD 0.90 을 목표로 몰고 Σ_y 를 읽는다**.  우리 플래튼 정본이 이미 도달한 결론
("scaffold 런에서 porosity 는 독립 정보를 담지 않는다; 반증 가능한 출력은 **응력-정지 두께** 하나")과 **같은 방향**.
⇒ `fam_platen_prereg_20260812` 후속에 **목표 porosity 로 몰고 wallP 를 보고하는 팔**을 추가하면
우리 판정이 **제3자 관행과 같은 규약** 위에 선다.  ⚠ servo(정압) 규약 폐기가 아니라 **두 규약 병기**가 목표.

**⑤ ★ YV/TV (항복 부피분율) 를 MPM 진단으로 즉시 이식 (비용 ~0)**
정의가 그대로 옮겨진다: **비영 누적소성변형을 가진 material point 의 부피분율**.  우리는 이미 Σdg 를 갖고 있으므로
**후처리 한 줄**이다.  얻는 것:
(a) "언제 전 재료가 항복했는가" 라는 **압력·밀도와 독립한 새 관측량**,
(b) Fig 8 처럼 **YV/TV vs RD** 와 **YV/TV vs 응력** 두 장 → 조성·P:S 스윕의 **소성 개시 지도**,
(c) frame[5] 에서 **MPM 고유 산출물**을 하나 더 확보 (DEM 은 원리적으로 못 냄).
★ 이 논문이 그 지표의 **판별력**까지 보여준다 — Fig 8a 에서 아홉 곡선이 d/w 순으로 **완전 정렬**한다.

**⑥ ★ Stage-E 접촉면적의 *다중접촉* 기준선으로 축소 MPFEM 을 검토 (중기)**
우리 Stage-E 는 5-regime cap 조합(`A_physics = max(lower[A_hertz, A_ligg], min(caps[A_tabor, A_volume, A_geom]))`)
= **추정기**다.  단일접촉 기준선은 이미 보유(Kogut–Etsion · Jackson–Green · Mesarović–Fleck 카드).
**빠진 것은 다중접촉·고밀도 기준선**이고 그 자리가 MPFEM 이다.
⇒ SE 수백 개 규모의 축소 MPFEM 한 판이면 **Stage-E 를 문헌이 아니라 계산으로** 검증할 수 있다.
⚠ **단 §4-6 대로 그 면적 자체가 메시 미수렴**이므로 기준선은 **점이 아니라 밴드**로만 쓸 수 있다.
⚠ 비용: 8입자 72 min(Fig 3) → 수백 입자면 수 시간~수십 시간.  **생산 침대는 불가**, 검증용 축소모델은 가능.

**⑦ ★ 압밀곡선 *전체* 대조를 검증 관행으로 승격**
Fig 11 처럼 **곡선 대 곡선**으로 맞추는 것이 단일점 앵커보다 훨씬 강하다.  우리는 이미 다압력 Heckel(DEM 4압력)과
σ-vs-P 를 갖고 있으므로 **MPM 도 같은 4압력에서 wallP–porosity 곡선**을 내면 frame[4] 교차검증이 점 → 곡선으로
승격된다 (CLAUDE.md 미결 "MPM Heckel sweep pending" 과 동일 항목).

**⑧ ★ LN(RD/RD₀) 표시법 = 초기 패킹 효율 제거**
Fig 7e 는 **초기 패킹이 다른 침대들을 같은 축에 놓기 위한** 표시법이다 (ref [60]).
우리 `d_h` 접힘 작업(다섯 침대를 하나로 접기)과 **목적이 같다**.
⇒ P:S 스윕처럼 초기 φ 가 다른 침대를 비교할 때 **ln(φ/φ₀) 축을 병기**하면 조성 효과와 초기패킹 효과가 갈린다.

**⑨ ⚠ 반면교사 — 재하율을 팔마다 다르게 두지 말 것**
§4-5 대로 이 논문의 d/w 비교는 **펀치 속도가 ≈2.9배 다른 팔들** 사이의 비교다.
우리도 같은 함정을 겪었고(`vmax ∝ 침대 높이`) `--platen-mach` 로 고쳤다.
⇒ **우리 규율이 이 축에서는 문헌보다 앞선다**는 것을 원고 Methods 에 쓸 수 있다 (겸손하게, 이 논문을 때리지 말고
"we additionally match the platen Mach number across arms" 형태로).

---

## 9. 인용 가능 문장 (deck/paper 용)

> ⚠ 아래는 **이 논문이 실제로 말한 것**만 담았다.  `figure-read` 값은 인용문에 넣지 않았다.

- **(층③ 논거 — 핵심)** "The limitation is stated explicitly in the MPFEM literature: a discrete-element treatment
  *'cannot compensate for the deformed particle surfaces during compaction, which plays an essential role in
  determining the contact pressure between contact pairs'* (Demirtas & Klinzing, *Powder Technol.* **391** (2021) 34–45, p. 35).
  Multi-particle FEM removes this limitation by construction — *'unlike DEM, particles are enriched with a full mesh
  of finite elements'* (ibid.) — at the price of a particle-count ceiling."
- **(우리 MPM 선택의 정당화)** "Multi-particle FEM resolves particle-shape plasticity most directly, but its authors
  cap their own study at *'under 2000'* particles for a *'<60 h'* wall-clock budget (Demirtas & Klinzing 2021).
  Our beds contain ~3×10⁴ particles, i.e. more than an order of magnitude beyond that ceiling, which is why the
  shape-plastic half of our workflow uses a grid-based material-point method rather than per-particle finite-element meshes."
- **(형상 소성 실증)** "With per-particle finite-element meshes the compaction of hollow spheres produces particle
  flattening and shell buckling in which *'contact that was initially made has now opened'* (Demirtas & Klinzing 2021) —
  a change of contact-network topology that a rigid-sphere discrete-element model cannot represent."
- **(크기 무관성 — 우리 packing 논지 지지)** "At a fixed geometric ratio and a fixed constitutive law, a 25 % change in
  particle diameter did not significantly change the compaction response (Demirtas & Klinzing 2021); size entered only
  through inter-particle friction per unit volume and die-filling efficiency.  This supports attributing our size
  effects to packing and to size-dependent material properties rather than to the mechanical constitutive response."
- **(수렴 관행)** "Mesh refinement converged the stress response but not the contact-area evolution in the same MPFEM
  study (Demirtas & Klinzing 2021, Fig. 5) — area-type observables converge more slowly than force-type ones."
- **(⚠ 균형 문장 — 우리 연속체의 한계도 같은 서론에 있다)** "The same introduction that names the DEM limitation also
  notes that continuum (Drucker-Prager/Cap, Cam-Clay) treatments *'do not allow for discrete prediction of
  particle-particle interactions or the influence of particle physical properties'*; our DEM+MPM division of labour is a
  response to **both** limitations, not only the first."

**⛔ 인용하면 안 되는 것**
- "Since the particles are modeled with **simple line elements**" — DEM 서술로 부정확 (§7-A-1 경고).
- "DEM 은 RD ○○ % 이상에서 실패한다" — **이 논문에 그런 수치가 없다** (§7-A-4).
- 시뮬레이션의 물리단위 응력 — **무차원**이다 (물리 MPa 는 실험 곡선에만, 그리고 그것도 `figure-read`).
- 이 카드의 **`figure-read ≈` 값 전부** (0.83 / 0.56 / 47 MPa / 35 MPa / −23 % …) — **TREND 전용**.
- 중공 입자의 d/w 결론을 우리 **중실** SE/CAM 에 적용하는 문장.

---

## 10. 주의 / 한계 (over-claim 방지 + **이 논문에 대한 비판**)

### 10-A. 우리가 전이할 때의 한계
1. **소재 전이 불가** — HPMCAS 고분자 **중공** 입자 vs LPSCl 황화물 **중실** SE + NMC811.  절대값 0건 전이.
2. **시뮬은 무차원** — 물리단위 응력은 실험 곡선(Fig 11a)에만 있고 그것도 우리가 `figure-read` 한 값이다.
   그 크기(≈35–50 MPa)는 우리 압밀압(300 MPa)의 **1/6–1/9** 이다.
3. **중공 ≠ 우리 계** — 헤드라인(d/w 지배)은 우리 계에 대한 주장이 아니다 (§7-C-1).
4. **전달물성 0건** — σ_ion/σ_e/κ 어느 것도 없다.  이 카드를 **전달 축(B) 근거로 쓰면 안 된다.**
5. **이 논문은 우리 MPM 도 비판한다** — 연속체는 "개별 입자 특성을 못 담는다"(§7-A-3).
   우리 자체 실측(Furnas dip 미재현, SE-rich 과압축)과 **같은 방향**이라 반박 불가.

### 10-B. ★ 이 논문 자체의 약점 (비판적으로)
1. ⚠⚠ **준정적 게이트가 헤드라인 구간을 안 덮는다.**  KE/PE < 1 % 는 **RD ≥ 0.6 에서만** 강제됐는데,
   "얇은 껍질은 **RD 0.46–0.47** 에서 전면 항복" 과 Fig 8a 의 **네 모델(d/w 12.5·10·8·6.25) 전면 항복**이
   전부 그 밖이다.  ⇒ 초기 구간(재배열 지배)의 결과는 **mass scaling 관성 오염이 통제되지 않았다**.
   (우리 자신의 재하율 함정과 **같은 종류의 결함**이라 남 얘기가 아니다.)
2. ⚠⚠ **재하율이 팔마다 다르다 (우리 발견)**: "5 초에 RD 0.9" 구동 + 질량 고정 ⇒ stated 초기 RD 양 끝
   (0.235 / 0.453)에서 **펀치 속도 ≈ 2.87배 차** (§4-5).  **하필 가장 빠른 팔이 헤드라인(얇은 껍질) 팔**이다.
   ⇒ d/w 효과와 재하율 효과가 **분리돼 있지 않다**.
3. ⚠⚠ **"최적 메시 1650" 은 수렴점이 아니다.**  Fig 5b/d 에서 N.C.Area 는 3363 요소까지 **단조 감소**하고
   plateau 가 없다 (4 s 에서 −22~−23 %).  1650 선택의 근거로 보이는 것은 **1650↔1800 의 비단조 wiggle** 이다.
   Fig 3 표를 보면 3363 은 1650 대비 **3.03배** 비싸다 ⇒ 실질적으로 **비용 제약**으로 읽힌다.
   ⇒ **접촉면적에 의존하는 결론(N.C.Area 절대값, 좌굴 개시 시점)은 메시 의존적**이다.
4. ⚠ **얇은 껍질 좌굴을 두께방향 3 요소 C3D8R 로 푼다** (derived, §4-3).  **1차 감차적분 육면체**로
   굽힘 지배 좌굴을 3층으로 해상하는 것은 얇은 쪽 한계다.  **좌굴 하중/형태의 메시 의존성은 별도로 보고되지 않는다.**
   저자들도 "a quantified extent of buckling … is beyond the scope of this study" 라고 인정한다.
5. ⚠ **실험 검증이 정성적이다.**  입경·벽두께는 XRCT 단면에서 눈으로 읽었고
   ("by no means does this represent a statistical analysis"), 실험 d/w = 7.5 / **20** 인데 시뮬 범위는 2.5–12.5 라
   **80 °C 는 외삽**이다.  Fig 10a–c 를 보면 **45 °C 분말에는 깨진 껍질 조각이 다수** 섞여 있어 "온전한 단일모드
   중공 구" 라는 모델 가정과도 어긋난다.  종료 조건도 다르다(고정 RD vs 고정 펀치간격).
   ⇒ Fig 11 의 일치는 **추세 일치**로만 읽어야 한다 (단 RD 0.9 의 **상대 격차 +34 % vs +30 %** 는 잘 맞는다).
6. ⚠ **통계가 없다.**  모델당 1 실현, 패킹 실현도 크기당 1개.  산포·오차막대 없음.
   (다만 **같은 패킹을 d/w 전체에 재사용**한 것은 통제로서 **좋은 설계**다 — 이건 칭찬.)
7. ⚠ **마찰 한 값(μ = 0.1)을 세 접촉쌍 모두에** 적용.  자기들이 인용한 [34,35] Zavaliangos 가
   "inter-particle friction plays a crucial role" 라고 했는데도 **민감도 스윕이 없다**.
8. ⚠ **점착 없음 → 배출·정제 강도 미계산.**  Xi/Hanmi [61] 의 "얇은 벽 → 인장강도 ↑" 는 **인용만** 하고
   자기 모델로 계산하지 않았다 ("This is a topic of future work").
9. ⚠ **RD 정의도 초기 펀치 위치도 없다.**  중공 입자에서 이건 사소하지 않다.  Fig 2 를 보면 **head-space 가 있고**,
   그래서 stated 초기 RD(23.5–45.3 %)와 Fig 6/7 의 응력 개시 RD(≈0.275–0.60)가 **다른 양**인데
   본문은 그 구분을 하지 않는다 (§3-2).
10. ⚠ **내부 불일치 4건** (모두 우리가 확인):
    - Table 1 `r1–12.5` 설명문 "d/w ratio of **12**" — **질량보존 산술로 12.5 가 옳다** (§3-1).
    - 메시 범위 본문 "**3288**" vs Fig 3/Fig 5 "**3363**".
    - Fig 7 캡션이 부피변형 그림을 "**(f)**" 라 부르는데 본문은 "**Fig. 7e**" 로 참조 — Fig 7 에 (f) 패널은 **없다**.
    - in-die → out-of-die 팽창 **61 %/78 %** 가 §2.6 의 "punch separation **1 mm**" 와 **≈13 % 어긋난다**;
      두 팽창률끼리는 **서로 정합**(in-die ≈ 0.87 mm)이므로 **기준 상태 정의 누락**으로 읽힌다 (§3-4).
11. ⚠ **요소 왜곡/리메싱 진단 없음** — RD 0.9 + 좌굴이면 Lagrangian 메시가 심하게 왜곡될 텐데 언급이 없다.

### 10-C. frame 규율 재확인
- **frame [4]**: 이 논문은 **DEM(다이필)과 MPFEM(압밀)을 직렬로 연결**한 것이지 두 모델을 **교차보정**하지 않았다.
  우리도 DEM↔MPM 을 각각 실험에 보정한다 — **이 논문을 우리 MPM 보정의 타깃으로 삼으면 안 된다**(소재가 다르다).
- **frame [5]**: 이 논문은 **역학 절반만** 소유한다.  전달 절반(σ 삼중항·퍼콜레이션·배위수·coverage)은 **없다**.
  ⇒ 이 카드는 **C(역학/morphology) 축 카드**이고 B(전달) 축에 인용하면 안 된다.

---

## 11. 관련 카드 (중복 서술 금지 — 겹치면 넘김)

| 카드 | 관계 |
|---|---|
| **`pycompact2025_dem_mpfem_workflow`** | ★★★ **직계 형제 — 같은 방법(MPFEM), 같은 층③ 주장.**  겹치는 서술은 **그 카드에 넘긴다**.  이 카드가 *추가로* 갖는 것 = ⓐ 서론이 **층①·②의 원전(Storåkers/Vu-Quoc)과 고밀도 DEM 처방 5편**을 이름으로 지목하고 "보정 의존·비쌈" 까지 적음 · ⓑ **접촉 개구**(위상 사건) · ⓒ **응력 수렴 ≠ 접촉면적 수렴** 을 한 그림에서 정량으로 · ⓓ **재하율 미통제** 반면교사 · ⓔ **중공 입자** 주제.  ⚠ 소재·압력이 달라(금속 @1400–2000 MPa vs 고분자 @≈50 MPa) **비용·RD 숫자를 섞지 말 것** |
| `gonzalez2012_nonlocal_contact_confined_granular` · `giannis2021_stress_based_multicontact_dem` | 이 논문 ref **[29]** 와 그 계보 — 서론이 "특별한 보정이 필요해 비싸진다" 고 지목한 **바로 그 DEM 쪽 처방**.  나란히 읽으면 **층①② 의 최선 ↔ 층③** 경계가 선명해진다 |
| `zunker2024_mdr_contact_model_partI` · `zunker2024_bulk_elastic_partII` · `zunker2025_dem_large_deformation_compaction` | DEM 쪽에서 **고 RD 까지 밀어붙인 접촉모델** — 이 논문이 "significant approximations" 라 부른 축의 최신판 |
| `varkey2026_multicontact_elastoplastic_dem` | ★ **정반대 편의 같은 문제** — 층①②를 끝까지 밀어붙인 DEM(Thornton–Ning + multi-contact).  거기서 "구는 타협, 실제 형상은 future work / <20 % porosity 는 비용 때문에 미추구" 를 **DEM 쪽에서** 인정한다.  **Demirtas = 연속체 쪽에서 같은 결론.**  둘을 나란히 인용하면 층③ 논거가 **양쪽에서** 잠긴다 |
| `contact_models_layer_map.md` | 이 카드가 **층③ 칸의 제3자 근거**로 들어갈 자리 |
| `mesarovicfleck2000_dissimilar_elastoplastic_indentation` | 이 논문 ref **[54]** — 무차원 재료 규약의 출처 중 하나.  우리 AM-freeze scaffold 정당화 근거이기도 함 |
| `storakers1997_similarity_inelastic_contact` | 이 논문 ref **[23]** — "DEM requires a plastic-contact law" 의 그 법칙 |
| `kogutetsion2002_ep_sphere_rigid_flat` · `jacksongreen2005_fem_elastoplastic_hemispherical_contact` | **단일접촉 FE 기준선**.  Demirtas 는 그 **다중접촉 확장**에 해당 |
| `devaucorbeil2020_mpm_after_25_years_review` | MPM 쪽 대응 리뷰 — MPFEM↔MPM 비교(§7-B)의 MPM 측 근거 |
| `stomakhin2013_mpm_snow_elastoplastic` · `klar2016_dp_sand_animation` | 우리 J2 계보 (항복면 box → cone → cylinder) |
| `bazzoun2026_dem_fem_rnm_ionic` | **전달 축**의 대응 카드 — 이 카드(역학)와 **축이 다르다**.  Bazzoun 은 σ_ion 실험 앵커, Demirtas 는 σ 0건 |
| `so2022_dem_contact_model_assb_compaction_sintering` | DEM 쪽 H-cap LAW 정의편 — "층① 로 얼마나 갈 수 있나" 의 상한 |
| `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` | 같은 "소성을 어떻게 다뤘나" 질문에 **안 다뤘다**로 답한 카드.  Demirtas 는 **다뤘다**로 답한 카드 |

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
