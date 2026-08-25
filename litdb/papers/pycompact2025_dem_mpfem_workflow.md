# PyCompact — LIGGGHTS DEM → MPFEM(OpenRadioss) 분말압축 오픈소스 워크플로 ★★ 우리 DEM→MPM scaffold 인계의 **독립 선례** (인계 시점은 정반대) — Mohammadhosseinzadeh (SoftwareX 2026)

> slug `pycompact2025_dem_mpfem_workflow` · DOI `10.1016/j.softx.2025.102495` · type `DEM+MPFEM (workflow/software)` · PDF `1e08fdc4-PyCompact_lation.pdf` · digested `2026-08-25` · status ✅
>
> ⚠⚠ **소재 경고 — 먼저 읽을 것**: 분말이 **Fe–Si–Al–P 금속합금**(연자성 분말코어 계열)이고 압력이
> **1400–2000 MPa** 다.  우리 **Li₆PS₅Cl + NMC811 @ 300 MPa** 와는 재료·압력·강성이 전부 다르다.
> ⇒ **절대값 전이 0건. 방법론(인계 구조·검증 프로토콜·비용)만 가져온다.**
>
> ⚠ `> elements:` / `> methods:` 태그를 **의도적으로 생략**했다 — 주기율표 뷰는 아르지로다이트 축이라
> 이 금속분말의 Fe/Si/Al/P 를 걸면 오탐이 된다.  (백필 도구가 나중에 붙이지 않도록 여기 명시.)
>
> ⚠ slug 의 `2025` 는 **접수연도**(Received 2025-09-01)다.  정식 인용은 **SoftwareX 33 (2026) 102495**
> (Available online 2026-01-06).

---

## 1. 한 줄 요약 (bilingual)

**KR:** LIGGGHTS DEM 으로 **중력 침강 패킹만** 만들고, 그 **(x, y, z, r) CSV 하나**를 넘겨
**입자 하나하나를 사면체 FE 메시로 바꿔**(MPFEM) OpenRadioss 로 **압축 전체를 다시 푸는**
전(全)오픈소스 워크플로.  Fe–Si–Al–P 분말 2종(Fine/Coarse)·1400–2000 MPa 에서 상대밀도
**편차 ≤ 2.5 %**(=2.1 %p) 로 실험·ABAQUS 와 맞췄다.  자동화의 실체는 **파이썬 노트북 2개**
(`InputGen.ipynb` = LIGGGHTS 입력 생성, `MeshMatGen.ipynb` = 입자별 메시·재료 카드 생성)다.

**EN:** DEM is used **only as a packing generator** (raindrop insertion + gravity settling); the settled
configuration — *"Initial powder configuration (size, center)"*, `Fig. 1` — is exported as a
**(x, y, z, r) CSV**, each sphere is re-created and **meshed as a deformable elastic–plastic FE body**, and
the **entire loading–unloading compaction is solved in MPFEM (OpenRadioss)**.  All five tools are free
(LS-PrePost is free-but-proprietary and declared optional).

**우리에게 왜 중요한가 (3줄):**
① **구조적 형제** — "DEM 이 패킹, 연속체가 소성" 이라는 우리 frame[5] 분업을 **제3자가 독립적으로
같은 도구(LIGGGHTS)에서** 구현했다.  ② **그러나 인계 시점이 정반대다** — 그들은 **압축 전(P≈0)**
에 넘기고 압축을 전부 연속체가 하고, 우리는 **압축 후(300 MPa 평형)** 에 넘겨 AM 골격을 얼린다.
이 한 칸이 두 파이프라인의 인식론을 갈라놓는다(§15).  ③ **"DEM 은 입자 내부 변형을 무시한다"**
는 우리 원고의 핵심 논거를 **저자들이 자기 문장으로 적어 놨다**(§5) — 인용 가능한 제3자 진술.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Majid Mohammadhosseinzadeh**, **Hossein Ghorbani-Menghari**, **Ji Hoon Kim\*** (School of Mechanical Engineering, **부산대학교 Pusan National University**, Korea) |
| 저널 | **SoftwareX 33 (2026) 102495** (Elsevier, **open access CC BY-NC**) |
| DOI | 10.1016/j.softx.2025.102495 |
| 날짜 | Received 2025-09-01 · Revised 2025-12-02 · Accepted 2025-12-18 · Online 2026-01-06 |
| 분량 | 본문 9 pp · Fig 1–4 · Table 1–3 · refs 32 · **SI 없음** |
| 소재 | **Fe–Si–Al–P 합금분말** 2종 (Fine / Coarse) — ⛔ SE·CAM 아님 |
| 연구유형 | **소프트웨어/워크플로 논문** (DEM+MPFEM 커플링) + 문헌 실험데이터 재검증 |
| 코드 | https://github.com/plaslab-kimjh/PyCompact · v1.0 · **MIT** · git |
| 환경(C7) | **Windows** · OpenRadioss r2024 · **LIGGGHTS-PUBLIC 3.8** · ParaView 5.13.2 · FreeCAD 1.0.2 · Python 3.10+ · LS-PrePost 4.9 |
| 재현 캡슐(C3) | **N/A** | 
| 개발자 문서(C8) | **N/A** |
| 연락 | kimjh@pusan.ac.kr |
| 자금 | NRF Korea (NRF-2021M3H4A6A01045764 / RS-2021-NR057528), Nano&Material (RS-2024-00450561), NST (CRC23011-203), KBSI (2021R1A6C101A449), Busan RISE (2025-RISE-02-004-12260001) |

★ **검증 루프가 그룹 내부**다 — 실험 데이터와 ABAQUS 참조모델은 **같은 그룹의 선행 논문
[15][16]**(Ghorbani-Menghari 1저자, 2024 Mater. Res. Proc. / IOP Conf. Ser.), 재료상수는 **[17]**
(Kahhal 2023, Mater. Trans., 같은 그룹)에서 왔다.  **독립 외부 앵커가 아니다** (frame[4] 등급 낮춤).

---

## 3. 핵심 수치 — stated / digitized 구분

> ⚠ `digitized` 는 **그림에서 픽셀로 읽은 값 = 추세 전용**.  거짓 정밀도로 인용 금지.
> `derived(ours)` 는 논문 값으로 **내가** 계산한 것 — 논문에 없는 수다.

### 3.1 재료 (전부 stated, ref [17])
| 물성 | 값 | 비고 |
|---|---|---|
| **E (Young)** | **170 GPa** | ⚠ **MPFEM 용으로 명시**.  DEM 쪽 E 는 **미기재**(§7.1) |
| ν | 0.3 | |
| ρ | **7130 kg/m³** | |
| 경화식 | **Swift** `σ = K(ε+ε₀)ⁿ` (eq 3) | σ [MPa], ε = 소성변형 |
| K / n / ε₀ | **1380 MPa / 0.254 / 0.0354** | 실험 보정 |
| ⇒ 초기항복 σ_y(ε=0) | **590.6 MPa** | `derived(ours)` = 1380·0.0354^0.254 |
| ⇒ σ(ε=1.0) / σ(ε=1.3) | **1392 / 1485 MPa** | `derived(ours)`.  Fig 4c/d von Mises 컬러바 상한 **1500 MPa** 와 정합 ✓ |
| ⇒ **P/σ_y** | **3.39**(초기항복) ~ **1.44**(포화유동응력) | `derived(ours)`, P=2000 MPa.  ★ **우리 1.0–2.0 과 같은 밴드** (§15) |
| ⇒ **E/σ_y** | **288** | `derived(ours)`.  우리 real 80–160 · **MPM champion 5.1** ⇐ 연화의 무차원 척도 |

### 3.2 분말·RVE·압력 (stated)
| 항목 | Fine | Coarse |
|---|---|---|
| 평균 입경 (본문) | **16 µm**, sd **9.4 µm** | **118 µm**, sd **17 µm** |
| 모델 반지름 범위 | **6–33 µm** (⌀12–66) | **48–96 µm** (⌀96–192) |
| RVE (정육면체 한 변) | **210 µm** | **1000 µm** |
| 입자 수 | **569** | **403** |
| 최대압력 | **2000 MPa** | 2000 MPa (곡선은 1400–2000 MPa 5점) |
| ⇒ RVE/입경 | **≈8 입자** | **≈7 입자** `derived(ours)` |
| ⇒ 초기 패킹(=1−φ₀) | **≈0.57–0.59** | **≈0.585** `digitized` (Fig 4b 시작점 φ₀ ≈ 43 / 41.5 %) |

⚠ **본문 평균입경 ↔ 모델 반지름 범위가 안 맞는다** — Fine 은 "평균 ⌀16 µm" 인데 모델 최소가
**⌀12 µm** 라 평균이 범위 바닥에 붙는다.  Fig 3(a) 는 **weight fraction** 이고 그 최빈값은
`digitized` **⌀35–40 µm** 다.  ⇒ "평균 16 µm" 은 **개수평균**, 모델 샘플은 **부피가중**으로 보인다
(논문 미명시).  `derived(ours)`: 패킹 0.59 를 가정해 역산한 유효 평균 직경은 **Fine ⌀26.4 µm ·
Coarse ⌀141 µm** (둘 다 stated 평균보다 크다 — 위 해석과 부호 일치).

### 3.3 결과 (헤드라인)
| 항목 | 값 | 종류 |
|---|---|---|
| **상대밀도 (Fine)** | exp ≈ **87 %** · sim ≈ **87 %** ("negligible difference") | stated |
| **상대밀도 (Coarse)** | exp **83.3 %** · sim **85.4 %** | stated |
| **최대 편차** | **2.5 %** = **2.1 %p** (85.4/83.3 = 1.0252) | stated + `derived(ours)` |
| 문헌 편차 밴드 | **0.5–4 %** [8,13,14,20,32] | stated |
| 압력 스윕 | **1400 · 1500 · 1600 · 1800 · 2000 MPa** (5점) | `digitized` (Fig 4g/h) |
| 하중 중 porosity @2000 MPa | **≈4.5 %(Coarse) / ≈3.5 %(Fine)** | `digitized` (Fig 4b) |
| 제하 후 porosity (P→0) | **≈17 % / ≈16 %** | `digitized` (Fig 4b 종단 수직구간) |
| 상대밀도 판독 규약 | **제하 중 5 MPa 도달 시점**의 RVE 부피 | stated ★ (§10 참조) |
| 고체부피 규약 | **압축 전 초기 구 부피 합** ("volumetric changes … negligible") | stated ★ = **우리 ε_sphere 와 같은 규약** |

### 3.4 민감도 3종 (Fig 3e/f/g)
| 스윕 | 값 | 종류 |
|---|---|---|
| 요소/입자 → 95 %밀도 축응력 | 500 → **1650 MPa**, 2500 → **1310 MPa** | stated |
| 〃 중간점 | 1000 ≈1510 · 1500 ≈1440 · **2000 ≈1375** | `digitized` |
| 〃 런타임 | **2000 el → 9 h**, **2500 el → 36 h** | stated |
| ⇒ 선택 메시(2000)의 **잔여 격자의존** | **≈ −5 %** (2000→2500) | `derived(ours)` — **수렴 아님** |
| 마찰 µ(MPFEM) → RD (Coarse, 2000 MPa) | 0.1 ≈**84.2** · 0.2 ≈**85.4** · 0.3 ≈**86.0 %** | `digitized` (0.2 값이 stated 85.4 와 일치 ✓ = 눈금 검증됨) |
| RVE → RD (Fine, 2000 MPa) | 210 ≈**86.9** · 250 ≈**87.1** · 300 ≈**87.4 %** (EXP 선 ≈87.8) | `digitized` |
| RVE 비용 (Table 1) | 210 µm/569입자/**9 h** · 250/874/**16 h** · 300/1033/**24 h** | stated |
| 솔버 비용 (Table 3, Coarse 2000 MPa, **24 CPU**) | **ABAQUS 5 h vs PyCompact 7 h** | stated |

---

## 4. ★★★ DEM → MPFEM 인계 해부 (질문 1 — 이 카드의 핵심)

### 4.1 전체 파이프라인 (Fig 1 · Fig 2a)
```
[DEM 단계]
FreeCAD (경계·inlet 모델링) ──STL──┐
Template(.txt) + PSD(.xlsx) ─ InputGen.ipynb ─ LIGGGHTS 입력파일 ─┴─> LIGGGHTS (raindrop 삽입 + 중력 침강)
                                                                    └─ VTK ─ ParaView ─> **CSV (x, y, z, r)**
                                                                                              │
   ═══════════════ 여기가 인계면 ("This file forms the interface between DEM and MPFEM") ═══════
                                                                                              ▼
[MPFEM 단계]
CSV ─ MeshMatGen.ipynb ─ cfile(.cfile) + material.k ─> LS-PrePost[선택] (die/punch/contact/BC **수작업**)
   ─> .k / .rad ─> OpenRadioss (explicit 하중–제하) ─ VTK ─> ParaView (von Mises, PEEQ, 반력, porosity)
```
`Fig. 1` 의 두 단계를 잇는 화살표 라벨이 그대로 인계물의 정의다 — **"Initial powder configuration
(size, center)"**.

### 4.2 ★ 인계 **시점** = 중력 침강 직후, 압축 **전** (P ≈ 0)
> *"The particles are generated with a raindrop insertion method, then settled under gravity [28].
> The settled configuration is exported in VTK format… **Since DEM effectively manages the kinematics,
> the resulting configuration serves as a realistic initial configuration for MPFEM.**"*

⇒ DEM 은 **패킹 생성기**일 뿐이고, **압축(1400–2000 MPa)은 100 % MPFEM 이 한다.**
Fig 4(b) 의 하중곡선이 porosity **41 % 에서 4 %** 까지 내려가는 그 전 구간이 MPFEM 소관이다.
⚠ 우리와 **정반대**다 — 우리는 LIGGGHTS 가 **300 MPa 압축을 끝낸** `atom_2060000` 좌표를 넘긴다.

### 4.3 ★ 인계 **정보** = 좌표 + 반지름, 그게 전부
| 넘기는 것 | 안 넘기는 것 |
|---|---|
| 입자 중심 (x, y, z) | 접촉 리스트 · 접촉당 겹침 δ |
| 반지름 r | 접촉력 / 힘사슬 |
| (VTK 단계까진 particle ID 도 있으나 CSV 로 가며 **소실**) | 응력·변형 이력 · 속도 |
| — | DEM 강성(E)·마찰 이력 |
⇒ **상태변수(state) 전달 0.  순수 기하 인계.**  MPFEM 은 완전 무응력·무이력 상태에서 새로 시작한다.

⚠ **논문이 다루지 않은 구멍**: 중력 침강 상태에도 Hertz 겹침 δ>0 인 접촉이 있는데, 그 자리에
**완전한 구를 다시 만들면 FE 모델은 초기 상호침투 상태로 시작**한다 (penalty contact → 스퓨리어스
초기력).  침강 하중이 작아 δ 가 작으니 실질 영향은 작겠지만, **논문은 이 문제를 한 줄도 언급하지
않는다.**  ⇒ 우리가 압축된 상태를 넘길 때 이 문제가 **훨씬 심각**해진다는 사실이 오히려 강조된다
(우리 real_14 는 300 MPa 압축 상태라 겹침이 크다 — 그래서 우리는 구를 다시 만들지 않고
**복셀 union 으로 상(phase)** 을 굽는다).

### 4.4 `InputGen.ipynb` — LIGGGHTS 입력 생성 (Fig 2b)
1. template `.txt` 읽기 (재료물성·단위·경계·접촉모델·도메인·timestep 의 뼈대 — 사용자가 커스터마이즈)
2. PSD `.xlsx` 읽기 (반지름 + 부피분율 또는 확률밀도)
3. atom_type · density 지정
4. **pdd 의 최대 시드번호를 찾아** 크기 클래스마다 새 랜덤 시드 생성 —
   **10,000 초과 소수(prime)로 제한** ("to ensure reproducibility and proper randomization")
5. 크기마다 `fix particletemplate/sphere` (**pts**) 줄 생성
6. `fix particledistribution/discrete` (**pdd**) 블록을 PSD 로부터 통째로 구성
7. 삽입은 `fix insert/rate/region` — 목표 입자수까지 **속도제어 스트리밍**

★ **우리와 같은 문제를 푼 방식**: PSD → 템플릿 자동생성은 우리 `webapp` 의 입력 생성기가 하는 일과
동형이다.  **소수 시드 규약**은 우리 seed 관리(멀티시드 규율)에 얹을 만한 작은 아이디어.

### 4.5 `MeshMatGen.ipynb` — 인계 변환기 (Fig 2c) ★ 이 논문의 실제 novelty
**(A) 기하·메시 가지**
- 입력 = `position.csv`
- 사용자 지정 파라미터: `unit_scale`, `mesh_dens`, 요소·절점 수, **min/max edge size**(tet)
- **단위 스케일**: DEM 은 **cm** 단위로 돌렸고 **×10 → mm** 로 변환 (stated)
- CSV 각 행마다 명령 생성: `(xᵢ,yᵢ,zᵢ)` 에 **solid sphere 생성 → 사면체 메시 → surface 생성 →
  part set 생성**
- 산출 = LS-PrePost 용 **cfile**.  실행하면 입자마다 목표 요소수의 메시가 자동 생성.

**(B) 재료 카드 가지** (LS-PrePost 의 결함 우회)
> *"the key limitation of LS-PrePost is that it does not allow assigning material properties to all
> particles simultaneously."*
- 사용자 입력은 **총 입자수 하나**뿐
- 입자마다 `pid = i`, `secid = i`, `mid = 1` 을 찍은 **`material.k`** 생성
- 재료 카드 = **`*MAT_PIECEWISE_LINEAR_PLASTICITY`** (LS-DYNA 키워드) — 다른 재료모델로 가려면
  "minor modifications" 필요
- ⚠ **삽입 절차가 GUI 의존 해킹**이다: proj 로 저장 → 재로드 → k 로 재저장해야 placeholder 가
  파일 **맨 위 정렬 블록**으로 나오고, 그것을 `material.k` 로 치환.  저자 스스로
  *"After several trial-and-error iterations"* 라고 적었다.  ⇒ **"reproducible" 를 내세운
  워크플로에서 가장 재현성이 낮은 지점.**

**(C) 자동화 안 되는 나머지 (stated)**
> *"the subsequent steps, such as modelling the die and punch geometries, defining contacts, defining
> material, and setting boundary conditions, are completed **manually** within the LS-PrePost environment."*
⇒ 자동화 범위 = **입력파일 생성 + 입자 메시 + 재료 배정**.  다이/펀치/접촉/BC 는 손이다.

### 4.6 ★ 우리 scaffold 인계와 1:1 대조
| 축 | **PyCompact (DEM→MPFEM)** | **우리 (DEM→MPM scaffold)** | 판정 |
|---|---|---|---|
| 인계 파일 | `position.csv` (x,y,z,r) | `real14_am_scaffold.csv` / `real14_se_scaffold.csv` (x,y,z,r) | **같음** ✓ |
| 인계 **시점** | **중력 침강 직후, P≈0** | **300 MPa 압축 완료 후** (`atom_2060000`) | ⚠ **정반대** |
| 인계 정보 | 좌표+반지름 (상태변수 0) | 좌표+반지름 (상태변수 0) | **같음** ✓ |
| 연속체가 받는 상 | **모든 입자** (전상) | **SE 만** (AM 은 고정 장애물로 동결) | 다름 |
| 연속체 이산화 | **입자당 Lagrangian tet 메시** (~2000 el) | **Eulerian 배경격자 + material point** (MLS-MPM) | 다름 |
| 구를 다시 만드나 | **예** (perfect sphere 재생성 → 겹침 미처리) | **아니오** (복셀 union 으로 상 굽기, `--se-dump`) | 우리가 안전 |
| 압축을 누가 하나 | **MPFEM 100 %** | **DEM 이 하고**, MPM 은 SE 형상만 정련 | ⚠ **인식론이 갈리는 칸** |
| DEM 강성의 역할 | 침강 패킹에만 영향 (**최종답에 거의 무관**) | **E_eff 1.35 가 최종 porosity 를 정한다** (보정 대상) | ⚠ 우리 쪽이 DEM 에 훨씬 의존 |
| 접촉 | MPFEM 안에서 **명시적 penalty + Coulomb µ=0.2** | MPM 격자 접촉 = **암묵적**(같은 셀 = 사실상 no-slip 융합) | **그들이 우위** |

★★ 이 표의 마지막 세 줄이 이 카드의 값이다.  §15 에서 판정한다.

---

## 5. ★★★ "DEM 만으로는 왜 안 되는가" — 저자 원문 (질문 2)

우리 원고가 필요로 하는 **제3자 진술**이 §1 Motivation 에 세 덩어리로 들어 있다.  원문 그대로:

**(a) DEM 의 한계 = 입자 형상·내부변형**
> *"Limitations, however, include high computational costs for large particle counts (due to explicit
> time-stepping), **assumptions of rigid or simplified particle shapes that neglect internal
> deformation**, and challenges in scaling to industrial volumes without approximations [12]."*

**(b) MPFEM 이 그것을 메운다 — 그리고 그것이 고압에서 필수라고 명시**
> *"In MPFEM, **each particle is modeled as a deformable finite element body**, enabling detailed
> analysis of elastic–plastic responses, **localized plasticity at contact points**, and densification
> driven by **both particle rearrangement and deformation**.  **This capability is essential for
> accurately predicting high-pressure compaction behaviour** [15,16]."*

**(c) 거꾸로 — 균질화 연속체(FEM)는 저밀도 재배열 구간을 못 한다 (= 우리 frame[5] 의 반쪽)**
> *"However, FEM has limitations such as **assuming a homogenized continuum, which overlooks the
> discrete nature of particles, leading to inaccuracies in modeling low-density stages where particle
> rearrangement dominates**, and it requires empirical calibration of material models that may not
> capture micro-scale heterogeneities [10]."*

**(d) 커플링 자체의 난점도 자인**
> *"However, **achieving accurate data transfer between DEM and MPFEM stages can be challenging**, and
> large-scale simulations remain computationally demanding."*

**(e) 구(球) 가정의 대가 — 결과 논의에서 자기 한계로 적음**
> *"Additionally, **assuming perfectly spherical particles slightly reduces densification** compared to
> real irregular powders."*

★ **우리 원고에서의 쓸모**
- (a)+(b) = *"DEM 은 입자 형상 소성을 못 해서 연속체가 필요하다"* 의 **외부 인용**.  우리 CLAUDE.md
  frame[2]("particles are eternal rigid spheres")·frame[5] 와 **문장 수준에서 같은 말**이고,
  **우리와 무관한 소재·무관한 그룹**이 적었다는 점이 가치다.
- (c) = 대칭 진술.  *"연속체는 재배열을 못 하고 DEM 은 형상을 못 한다"* → **분업이 우리 편의가 아니라
  방법론의 구조**라는 논거.  우리 CORRECTION 2(소성 MPM 이 Furnas dip 재현 실패)의 **문헌 짝**이다.
- (e) = **구 가정이 치밀화를 과소평가**한다는 자인 → 우리 "강체 구 floor ~20 %" 서술의 방향 지지.
- ⚠ 단, **(b) 의 "essential" 은 그들의 1400–2000 MPa 금속압축 맥락**이다.  300 MPa 황화물에
  그대로 옮기면 과확대 — "고압 압밀에서" 라는 한정어를 반드시 함께 인용할 것.

---

## 6. ★★ MPFEM 이 주는 것 / DEM 이 못 주는 것 (질문 3, 이 논문 기준)

**MPFEM 만 주는 것 (논문이 실제로 보여준 것)**
1. **입자 형상 변화** — Fig 4(e)(f) 단면에서 구가 **다면체로 눌리고** 접촉면이 평평해진다.
2. **입자 내부 응력장** — Fig 4(c)(d) von Mises (0–1500 MPa), 접촉점 국소집중.
3. **누적 소성변형장(PEEQ)** — Fig 4(e)(f), 0–1.3.  ★ 분포가 **접촉/네크에 붉고 코어는 파랗다**
   = **core-preserved + boundary-flattening** — 우리 MPM champion 의 SEM 정합 morphology 와 **같은 무늬**.
4. **대변형 고밀도 영역의 상대밀도** — 하중 중 RD 95–96 % 까지 (강체 구로는 불가).
5. **하중–제하 이력(springback)** — Fig 4(a) 응력–변형 루프, Fig 4(b) porosity 루프.
6. **잔류 공극의 위치** — Fig 4(e) "residual voids between larger particles due to limited plastic flow".

**DEM 이 (이 논문에서) 준 것**
- 현실적 초기 패킹 하나.  그게 전부다.

**둘 다 못 주는 것 (우리 기준)**
- σ_ionic / σ_e / σ_thermal **전달물성 0건** — 이 논문은 전기·이온·열 전도를 **한 번도 계산하지
  않는다**.  접촉망 저항(Holm), percolation, coverage, tortuosity 전부 없음.
- 파괴/균열, 결합상(binder/bond), 다상(AM+SE) 복합, 다분산 bimodal, Furnas dip.
- ⇒ **우리 σ 삼중항과 접촉망은 여전히 우리 칸이다** (frame[5] 재확인).

---

## 7. 시뮬레이션 방법 상세 ★

### 7.1 DEM 단계 (LIGGGHTS-PUBLIC 3.8)
| 항목 | 값 | 출처 |
|---|---|---|
| 접촉법칙 | **Hertz–Mindlin (tangential)** — 법선+접선, 마찰 포함 | stated |
| 미끄럼 마찰 µ_s | **0.5** | stated |
| 구름 마찰 µ_r | **0.05** | stated |
| 반발계수 COR | **0.7** | stated |
| 삽입 | **raindrop** + `fix insert/rate/region` (속도제어 스트리밍) | stated |
| 안정화 | **중력 침강** | stated |
| PSD | `fix particletemplate/sphere` + `fix particledistribution/discrete` (개수 or 부피분율 가중) | stated |
| 시드 | 크기 클래스마다 **10,000 초과 소수** 자동생성 | stated |
| 단위 | **cm** (→ MPFEM 에서 ×10 = mm) | stated |
| 출력 | VTK (ID, center, radius) → ParaView → CSV(x,y,z,r) | stated |
| **영률 E** | ⛔ **n/a — 논문에 없다** | — |
| ν, 밀도(DEM), timestep, Rayleigh 비율, 중력값, 도메인 높이, 벽 마찰, 점착 | ⛔ **전부 n/a** | — |

★★ **질문 5 에 대한 정직한 답: "실제 E 를 썼는가, 낮췄는가" 는 이 논문으로 알 수 없다.**
템플릿 파일이 "재료물성"을 담고 "사용자가 커스터마이즈"한다고만 적혀 있고, 유일하게 명시된
E=170 GPa 는 **MPFEM 재료절(§3)** 의 값이다.  ⇒ `n/a`.
그런데 **이 논문에서는 그게 거의 중요하지 않다** — DEM 이 최종 밀도에 기여하는 것은 초기 패킹 하나뿐이고,
압축은 전부 MPFEM 이 다시 푼다.  ⇒ **PyCompact 는 DEM 강성에 둔감하고, 우리는 민감하다**
(우리 E_eff 1.35 는 최종 porosity 를 직접 정한다).  이 비대칭 자체가 §15 판정의 재료다.

### 7.2 MPFEM 단계 (OpenRadioss r2024)
| 항목 | PyCompact | ABAQUS 참조 [15,16] |
|---|---|---|
| 솔버 | **Explicit** | Explicit |
| 입자 요소 | **/TETRA4** (4절점 사면체, LS-PrePost 생성) | **C3D4** (선형 tet) |
| 다이·펀치 | **/SHELL** (강체 tooling) | **R3D4** (강체) |
| 접촉 | **General contact /TYPE26** (penalty, surface-to-surface) | General contact |
| 마찰 | **Coulomb µ = 0.2** (입자-입자) | 0.2 |
| 재료 | `*MAT_PIECEWISE_LINEAR_PLASTICITY` + Swift 데이터 | 동일 물성 |
| 요소/입자 | **평균 2000** (수렴시험 500–2500) | 명시 없음 |
| BC | 다이 **완전구속**, 펀치 **prescribed motion rigid** → 목표압 → 제하 | 동일 |
| 주기경계 | ⛔ **없음** (강체 다이 벽 = walled RVE).  저자도 "effects at the boundaries of the RVE" 를 오차원으로 든다 | — |
| **펀치 속도 / 질량스케일링 / 총 시간** | ⛔ **n/a — 미기재** | — |

⚠⚠ **명시적 동역학인데 재하율이 없다.**  저자 스스로 §1 에서 *"applied pressure, **punch velocity**,
and PSD"* 를 최적화 대상 3종으로 꼽아 놓고 자기 펀치 속도를 안 적었다.  우리 `--platen-mach` 규율
(재하율 = 크로스-베드 비교의 함정, CLAUDE.md 2026-08-06)의 관점에서 **가장 큰 미기재 항목**이다.
⇒ 이 논문의 절대 밀도값을 다른 재하율의 계산과 나란히 놓지 말 것.

### 7.3 ★ 입자 처리 (우리 "무질서 처리"의 DEM 대응)
| 축 | 이 논문 |
|---|---|
| 형상 | **완전 구** (DEM·MPFEM 둘 다).  저자 자인: 구 가정이 치밀화를 과소평가 |
| PSD | **단봉(unimodal) 2종** — Fine / Coarse.  ⛔ bimodal·다분산 혼합 없음 (저자: "focused on two unimodal powders") |
| 소성 표현 | **★ 진짜 SHAPE 소성** — 입자마다 FE 메시 + J2형 piecewise-linear plasticity(Swift).  δ-겹침 프록시 **아님** |
| 강체/변형체 | 입자 = **변형체**, 다이/펀치 = 강체 |
| 파괴 | ⛔ 없음 (요소 삭제·균열·파편화 없음) |
| 결합상 | ⛔ 없음 (binder/bond 모델 없음) |
| 상(phase) 수 | **1상** (단일 금속분말).  ⛔ AM+SE 복합 없음 |
| 무작위성 | DEM 시드(소수)로만.  **시드 앙상블·오차막대 0** — 조성·격자당 런 1개 |

⇒ **층 지도(`contact_models_layer_map.md`) 기준 위치**: 이 논문은 **층 A/B(접촉 LAW)를 통째로 건너뛰고
층 3(입자 형상 소성)을 직접 이산화**한다.  Thornton–Ning·EEPA·Luding 같은 접촉 LAW 가 **불필요**해지는
대신, 그 자리를 **penalty contact + FE 메시**가 차지한다.

---

## 8. 소재·검증 프로토콜 (질문 7)

- 분말 = **Fe–Si–Al–P 합금** 2종.  Fine(⌀16±9.4 µm) / Coarse(⌀118±17 µm) — 같은 재료, **PSD 만 다름**.
  (성분비·제조법·조성 wt% 는 **미기재**.)
- 실험 = 문헌 [15,16] 의 다이 압축시험 (Fig 3b 모식: 펀치–다이–압분체), 압축 후 상대밀도 측정.
- 압력 = **1400–2000 MPa** 5점 (Fig 4g/h).  본문은 2000 MPa 를 "고압 치밀화 평가에 적절"하다고 명시.
- **PSD 가 결과에 미치는 영향** (이 논문의 물리 결론):
  - **Fine 이 더 치밀해진다** (RD 87 vs 83–85 %; 최종 porosity 더 낮음).
  - 기전: Fig 4(d) — 미세분말은 **응력분포가 더 균질**하고 *"efficient force transmission through
    networks of smaller particles, which minimizes localized plastic deformation"*.
    Fig 4(f) 단면에 **큰 공극이 없다**.
  - 반대로 Coarse 는 Fig 4(c) 에서 **접촉점 국소집중** → Fig 4(e) 에 **큰 잔류공극**
    ("limited plastic flow").
  - ⚠ **본문의 근거 한 줄은 자기 그림과 어긋난다** — *"The fine powder shows reaching a lower final
    porosity **due to its denser packing**"* 인데, Fig 4(b) 의 **초기** porosity 는 Fine 이 **더 높다**
    (`digitized` 43 % + 스파이크 61 % vs Coarse 41.5 %) = Fine 이 **더 성기게** 쌓였다.
    올바른 기전은 그들이 다른 문단에서 쓴 **접촉 네트워크 균질성**이지 초기 패킹이 아니다.

---

## 9. 결과 — 섹션별 상세

### 9.1 Fig 3(e) 메시 수렴 — **수렴하지 않았고, 선택은 비용이 했다**
- 95 % 상대밀도에서의 축응력: 500 el → **1650**, 2500 el → **1310 MPa** (stated) = **−20.6 %**.
- 중간점 `digitized`: 1000 ≈1510 · 1500 ≈1440 · **2000 ≈1375**.  **단조 감소, 평탄화 없음.**
- 본문: *"indicating convergence, beyond which further refinement produced no significant change"* —
  그러나 2000→2500 이 `derived(ours)` **−5 %** 이고 기울기가 죽지 않는다.
- 실제 선택 이유는 바로 다음 문장에 있다: *"the runtime for the case with 2500 elements per particle
  was **36 h**, whereas it was **9 h** for the case with 2000 elements.  Therefore, an average of 2000
  elements per particle was selected"*.  ⇒ **비용이 정한 메시**.
- ⚠ 그리고 **요소 25 % 증가에 런타임 4배**는 설명되지 않는다 (explicit dt ∝ 최소 변길이로 따지면
  `derived(ours)` ≈1.35배가 상한).  논문에 원인 서술 없음.
- ★ **우리 자기비판의 거울**: 우리 CL-41(vox 0.15→0.115 에서 이득이 계속 오르고 멱법칙 외삽이
  성립하지 않음)과 **같은 병**이다.  우리는 그것을 "미수렴 확정"으로 라벨했고, 이 논문은
  "convergence" 라고 적었다.  ⇒ **같은 상황에서 라벨이 다르다** — 인용할 때 이 차이를 살릴 것.

### 9.2 Fig 3(f) 마찰 — RD 를 올리는 노브가 **제하(springback) 쪽**에 있다
- µ 0.1→0.3 에서 RD **84.2 → 86.0 %** (`digitized`), µ≥0.2 에서 완만.
- 저자 기전: *"raised relative density …, plateauing beyond µ = 0.2 **due to reduced sliding and
  elastic recovery**"* — 즉 **마찰이 제하 시 되돌아감을 잠근다**.
- ⚠ *"µ = 0.2 was selected for best experimental agreement."* 그런데 Coarse 실험은 **83.3 %** 이고
  `digitized` 로 µ=0.1 이 **84.2**, µ=0.2 가 **85.4** 다 ⇒ **Coarse 만 보면 µ=0.1 이 더 가깝다.**
  선택 기준(두 분말 동시? 다른 지표?)이 정량적으로 서술되지 않았다.
  ⇒ **마찰은 사실상 1개의 보정 노브**이고 헤드라인 2.5 % 는 그 노브를 지난 값이다.
- ⚠ **DEM µ_s = 0.5 ≠ MPFEM µ = 0.2** — 같은 분말인데 두 단계의 마찰이 다르다 (논문 설명 없음).

### 9.3 Fig 3(g) RVE — 역시 단조 상승, 가장 작은 것을 채택
- 210 → 250 → 300 µm 에서 RD **86.9 → 87.1 → 87.4 %** (`digitized`), 실험선 ≈87.8.
- 즉 **RVE 를 키울수록 실험에 가까워진다** = 보고된 편차에 **부호 아는 RVE 편향**이 남아 있다.
- 선택 근거(stated): "representativeness, experimental match, consistency with prior studies [15,16],
  and **computational efficiency**" — Table 1 이 그 비용이다 (9 / 16 / 24 h).

### 9.4 Fig 4(a) 응력–변형 (Coarse/Fine, 2000 MPa)
- 3단계 서사(stated): **① 입자 재배열**(응력 거의 0) → **② 변형에 의한 치밀화**(급상승) →
  **③ 부분 탄성회복**(제하 급강하) + **잔류변형 = 영구 치밀화**.
- `digitized`: 응력 개시 ε ≈ **0.365(Coarse) / 0.285(Fine)**; 정점 ε ≈ **0.622 / 0.577** @2000 MPa;
  제하 후 잔류 ε ≈ **0.598 / 0.556**.  ⇒ **Δε ≈ 0.024 / 0.020**
  (압축 높이 대비 회복률 `derived(ours)` **6.3 % / 4.7 %**).
- ⚠ **개시 변형이 다르다**(0.365 vs 0.285) = 두 케이스의 초기 베드 높이/공극이 다르다는 뜻인데,
  변형의 정규화 길이(초기 캐비티인지 베드 높이인지)가 **미기재**다 → 절대 변형값 해석 불가.

### 9.5 Fig 4(b) porosity–pressure 루프 ★ 형식을 훔칠 그림
- `digitized` 하중분지: φ₀ ≈ **41.5 %(C) / 43 %(F)** (F 는 시작에 **61 %** 스파이크) →
  500 MPa ≈33/31 → 1000 ≈22/20 → 1500 ≈12/10.5 → **2000 ≈4.5/3.5 %**.
- `digitized` 제하분지: 2000 에서 시작해 **거의 평평**(1000 MPa 에서도 ≈5/4 %) 하다가
  **P→0 에서 수직으로 ≈17/16 %** 로 튄다.
- ★ **하나의 축에 하중+제하를 같이 그리는 형식** = 우리가 안 하는 것.  우리는 porosity@P 를 점으로만
  보고한다.  이 형식이면 **springback 이 눈에 보인다**.

### 9.6 Fig 4(c)(d) von Mises · (e)(f) PEEQ 단면
- (c) Coarse: 하중 중 **접촉점 국소 고응력** → 그 자리에서 소성 → 재배열 촉진.  제하 시 응력완화가
  **입자 주변부**에서 일어남.
- (d) Fine: **더 균질한 응력분포**, 국소 소성 최소화.
- (e) Coarse 단면 높이 **445 µm**, (f) Fine **120 µm** (그림 내 화살표 라벨).
  `derived(ours)` 입자 개수 세기로 (e)=Coarse(⌀≈100 µm 급), (f)=Fine 이 맞다 ✓ (캡션과 일치).
- ★★ **PEEQ 분포 무늬 = 접촉/네크 붉음(0.8–1.3) + 코어 파랑(0.1–0.3)** ⇒
  **core-preserved + boundary-flattening**.  우리 MPM champion(E 1.53 / σ_y 0.15, `vis_zoom ④`)이
  SEM 과 맞춘 바로 그 무늬를 **다른 재료·다른 이산화(FE)** 가 재현한다 = frame[4] 성격의 교차확인.
- ★ **제하 프레임에서 입자 사이 어두운 틈이 눈에 띄게 넓어진다** (양 분말 모두) = **접촉이 열린다**.
  Fig 4(b) 의 porosity 반등과 시각적으로 정합.

### 9.7 Fig 4(g)(h) 실험·ABAQUS 대조 — ⚠ **패널 라벨이 뒤집혀 있다**
- **그림 범례**: (g) = **Fine**-EXP/OpenRadioss/ABAQUS, (h) = **Coarse**-….
- **캡션·본문**: "(g) Coarse powders and (h) Fine powders", *"As shown in Fig. 4(h), for the fine
  particles…"*.  ⇒ **정반대**.
- 값으로 판정하면 **범례가 맞다**: 본문이 말한 Coarse 83.3(exp)/85.4(sim) 짝은 **범례가 Coarse 인
  (h)** 에서 읽힌다.  ⇒ **캡션·본문 쪽 패널 문자가 오기**.  인용 시 (g)/(h) 를 바꿔 쓸 것.
- `digitized` (h)=Coarse: 1400 exp 83.3 / OR 82.5 / **ABQ 80.8** → 2000 exp 83.3 / **OR 85.3** / ABQ 83.6.
- `digitized` (g)=Fine: 1400 ≈83.7/82.9/83.1 → 2000 **≈87.4 / 87.0 / 86.9** (셋이 수렴).
- ★ **정직한 읽기**: 2000 MPa Coarse 에서는 **ABAQUS(83.6)가 실험(83.3)에 더 가깝고 OpenRadioss(85.3)가
  더 멀다**.  반대로 1400 MPa 에서는 ABAQUS 가 −2.5 %p 로 더 멀다.  ⇒ *"matching ABAQUS predictions"*
  는 **점대점 일치가 아니라 오차 크기가 비슷하다**는 뜻으로만 방어된다 (두 솔버 격차 `digitized`
  **0.8–2.5 %p**).

---

## 10. ★★ 상대밀도 도달 범위와 정확도 — 우리 관심(porosity 10 %)에 닿는가? (질문 4)

**어느 구간에서 2.5 % 인가**
- 편차의 **최댓값은 Coarse @2000 MPa 의 85.4 vs 83.3 = 2.1 %p = 상대 2.5 %**.
- Fine 은 두 값 모두 ≈87 % (편차 무시 가능).
- 즉 **2.5 % 는 "가장 나쁜 한 점"** 이고, 그 점은 **가장 높은 압력·거친 분말**이다.

**우리 관심 구간에 닿는가 — ⛔ 안 닿는다**
| | PyCompact | 우리 |
|---|---|---|
| 압력 | **1400–2000 MPa** | **300 MPa** (스윕 100–600) |
| 도달 RD (제하 후) | **83–87 %** = porosity **13–17 %** | pure-SE **90 %**(φ 10 %), real_14 **84.4 %**(15.6 %) |
| 도달 RD (하중 중) | **95–96 %** = porosity **4–5 %** `digitized` | — (우리는 제하를 안 푼다) |
⇒ **제하 후 기준으로 그들은 RD 0.90 에 도달하지 못한다** — 우리 press 의 **6.7배 압력**에서도.
저자의 설명은 **완전 구 가정**(불규칙 실분말보다 덜 치밀해짐)이다.
★ 우리 쪽 함의: **"강체 구 floor ~20 %"** 대비 **형상 소성이 있으면 하중 중 4–5 %까지 내려간다** —
소성이 강체 구 floor 를 깬다는 우리 주장의 **독립 방향지지**.  단 **제하하면 13–17 %로 되돌아온다**
= 형상 소성이 사는 자리는 "하중 중"이고, 보고값은 **제하 규약에 강하게 의존**한다.

**⚠⚠ 판독 규약이 near-vertical 구간 위에 있다 (내가 잡은 가장 큰 기술적 취약점)**
- stated: *"a designated pressure level of **5 MPa** was established as the threshold for determining the
  volume of the compacted powders in the unloading phase."*
- 그런데 Fig 4(b) 제하분지는 **P→0 에서 수직**이다 (≈9 % → ≈17 % 가 마지막 수십 MPa 안에서).
  5 MPa 는 x축(0–2500) 상에서 **1–2 픽셀** — 그림에서 읽는 것이 원리적으로 불가능하고,
  **판독값이 문턱 선택에 매우 민감**하다.
- **닫히지 않는 삼각형** (셋 다 같은 런이어야 하는데 안 맞는다):
  | 경로 | 제하 후 RD |
  |---|---|
  | Fig 4(a) Δε 로 유도 (`derived(ours)`, 하중 중 RD 96 % 가정) | **≈90.3 %** |
  | Fig 4(b) 종단 `digitized` | **≈83–84 %** |
  | 본문 stated (5 MPa 규약) | **85.4 %** |
  ⇒ **≈5–7 %p 벌어진다. 헤드라인 편차(2.1 %p)보다 크다.**
  가장 그럴듯한 양성 해석: **두 그림의 부피 규약이 다르다**(Fig 4a = 펀치 변위 기반 공칭변형,
  Fig 4b = 입자 집합 부피).  내 digitize 오차 가능성도 남긴다.  **논문 정보만으로는 판정 불가.**
- ⇒ **인용 규율**: PyCompact 의 RD 절대값을 우리 표에 넣을 때는 반드시
  *"제하 후·5 MPa 규약·구 가정"* 을 함께 적는다.  하중 중 값(4–5 % porosity)과 섞지 않는다.

---

## 11. 계산비용·확장성 (질문 8) + 저자 명시 한계

**실측 비용 (stated)**
| 케이스 | 입자수 | 시간 | 비고 |
|---|---|---|---|
| RVE 210 µm (Fine) | **569** | **9 h** | 2000 el/입자 ⇒ `derived(ours)` **≈1.14 M 요소** |
| RVE 250 µm | 874 | 16 h | |
| RVE 300 µm | 1033 | 24 h | |
| Coarse 2000 MPa, **24 CPU** | 403 | **ABAQUS 5 h / PyCompact 7 h** | Table 3 |
| 2500 el/입자 | 569 | **36 h** | 메시 수렴시험 |

**스케일링** `derived(ours)`: 569→874 는 지수 **1.34**, 874→1033 은 지수 **2.43** (입자수 대비 초선형).
⇒ 접촉쌍 증가로 초선형이 되는 전형.

**★ 우리 침대에 적용하면 (판정 (b)의 결정적 근거)** `derived(ours)`, 자릿수 전용:
- 우리 real_14 = **SE 32,832 개** (+AM 457).  569 대비 **57.7배**.
- 입자수만으로: 지수 1.0 → **519 h(22일)** · 1.33 → **1,980 h(82일)** · 1.5 → **3,945 h(164일)** (24 CPU).
- **여기에 explicit dt 벌금이 곱해진다** — 그들 Fine 은 ⌀16 µm, 우리 SE 는 **⌀1 µm** ⇒ 같은
  요소/입자면 요소 변길이 **16배 작음** ⇒ dt **16배 작음**.
- 곱하면 **≈8,300 h ≈ 1년 (24 CPU)**.  요소수는 **65.7 M**.
⇒ **결론: 우리 침대에 MPFEM 은 현재 하드웨어에서 불가.**  (GPU MPM 은 같은 침대를 시간 단위로 푼다.)

**저자 명시 한계 (stated)**
- *"Although this study focused on **two unimodal powders and small RVEs**…"* — 확장은 **future work**.
- *"Despite the computational cost of DEM–MPFEM simulations due to explicit time-stepping and contact
  resolution [13,14,31]…"*
- 편차 원인으로 스스로 든 5가지: **메시 해상도 · PSD 패킹 변동 · 마찰 알고리즘 차이 ·
  RVE 경계효과 · 두 explicit 솔버(OpenRadioss vs ABAQUS)의 미세한 차이** + **완전 구 가정**.

---

## 12. 도구 사슬 · 오픈소스 비율 · 재현성 (질문 6)

| 도구 | 역할 | 라이선스 | 우리 재현 가능? |
|---|---|---|---|
| **FreeCAD** 1.0.2 | 경계·inlet CAD → STL | 오픈소스 (LGPL) | ✓ (우리는 CAD 불필요 — 박스 도메인) |
| **LIGGGHTS-PUBLIC** 3.8 | DEM 패킹 | 오픈소스 (GPL) | ✓✓ **우리가 이미 쓰는 코드** |
| `InputGen.ipynb` | LIGGGHTS 입력 생성 | MIT | ✓ |
| **ParaView** 5.13.2 | VTK→CSV, 시각화, 반력 추출 | 오픈소스 (BSD) | ✓ |
| `MeshMatGen.ipynb` | **cfile + material.k** 생성 | MIT | ✓ 단 **LS-PrePost 포맷 종속** |
| **LS-PrePost** 4.9 | 메시 실행·접촉/BC/키워드 조립 | **무료지만 독점** (Ansys) | △ Windows·GUI·수작업 |
| **OpenRadioss** r2024 | explicit MPFEM 솔버 | **오픈소스 (AGPL)** ★ | ✓ (무료·소스공개) |

⚠ **라이선스 열의 출처 주의**: 논문이 명시한 라이선스는 **PyCompact 자신의 MIT (C4)** 와
*"LS-PrePost (free but proprietary)"* **둘뿐**이다.  나머지 칸(LGPL/GPL/BSD/AGPL)은 각 도구의
**통상 라이선스로 내가 채운 것** — 논문 근거가 아니다.  논문이 실제로 하는 주장은
*"integrates five **freely available** tools"* 이다.

- **오픈소스 비율**: 6/7 이 무료, 그중 **5/7 이 진짜 오픈소스**.  ⛔ 유일한 독점 = LS-PrePost,
  그런데 저자 스스로 결론에서 *"it can be replaced in future implementations without affecting
  reproducibility"* 라고 적고 `Fig. 2a` 에도 **"Ls-PrePost [optional]"** 로 표기.
- ★★ **OpenRadioss 가 무료라는 점의 값**: ABAQUS/LS-DYNA 라이선스 없이 **explicit 대변형 접촉
  FE** 를 돌릴 수 있다.  비용 대가는 Table 3 의 **7 h vs 5 h = 1.4배 느림**뿐.
- ⚠ **재현성 주장의 약한 곳**: (i) **C3 재현 캡슐 N/A**, (ii) **C8 개발자 문서 N/A**,
  (iii) OS **Windows 명시**, (iv) 재료 카드 삽입이 **GUI proj→k 라운드트립 해킹**,
  (v) die/punch/contact/BC 가 **수작업**, (vi) 본문 C7(FreeCAD 1.0.2 · LS-PrePost 4.9) ↔
  참고문헌 [24](1.0.1) · [26](4.8) **버전 불일치**.
- **우리가 실제로 재현 가능한가**: LIGGGHTS·ParaView·OpenRadioss·Python 은 전부 리눅스에서 되고,
  LS-PrePost 단계는 **우리 자체 메시 생성기로 대체**해야 한다 (gmsh/tetgen + Radioss starter deck 직접 생성).
  ⇒ **가능하지만 이 워크플로의 절반은 다시 짜야 한다.**  (그리고 §11 대로 우리 침대엔 비용이 안 맞는다.)

---

## 13. Figure set ★

| Fig | 내용 | 우리가 쓸 것 |
|---|---|---|
| **1** | DEM/MPFEM 두 상자와 각 단계 도구 로고 (Pre/Processing/Post) | ★ 화살표 라벨 **"Initial powder configuration (size, center)"** = 인계물 정의 인용구 |
| **2a** | 전체 데이터흐름 (STL·VTK·**CSV(x,y,z,r)**·cfile/.k·.rad) | ★★ 우리 scaffold 파이프라인 그림과 **1:1 대응** — 발표 슬라이드 비교도 재료 |
| **2b** | `InputGen.ipynb` 플로차트 (template→PSD→pts/pdd→시드) | PSD→DEM 입력 자동화 패턴 |
| **2c** | `MeshMatGen.ipynb` 플로차트 (CSV→구 생성→tet 메시→surface/part set ‖ pid/secid/mid) | ★ 인계 변환기의 실제 알고리즘 |
| **3a** | 두 분말 PSD (weight fraction vs 로그 직경) | `digitized` Fine 최빈 ⌀35–40 · Coarse ⌀≈120 (본문 평균과의 불일치 근거) |
| **3b** | 다이 압축 모식 (펀치/다이/압분체) | 우리 플래튼 그림의 표준형 |
| **3c** | DEM 침강 후 3D (Coarse 1000 µm / Fine 210 µm) | 인계 시점의 상태 = **압축 전** |
| **3d** | MPFEM 모델 (펀치 shell·다이·tet 메시 입자 + 단일 구 확대) | ★ "입자당 FE 메시" 가 무엇인지 보여주는 한 장 |
| **3e** | 요소/입자 → 95 % 밀도 축응력 (500–2500) | ★ **미수렴 격자의존** 사례 (우리 CL-41 의 거울) |
| **3f** | µ → RD (0.1/0.2/0.3) | 마찰이 **springback 잠금**으로 RD 를 올린다 |
| **3g** | RVE → RD (210/250/300 µm) + EXP 선 | RVE 편향의 부호 |
| **4a** | 하중–제하 응력–변형 (Coarse/Fine) | 3단계 서사 + Δε `digitized` |
| **4b** | **porosity–pressure 하중+제하 루프** | ★★ **그림 형식을 훔칠 것** (우리는 점만 본다) |
| **4c/4d** | von Mises 4프레임 (초기→하중→최대→제하), Coarse/Fine | 접촉 국소집중 vs 균질 전달 |
| **4e/4f** | **PEEQ 단면** (하중/제하), 445 µm / 120 µm | ★★ **core-preserved + boundary-flattening** = 우리 MPM morphology 와 같은 무늬 · 제하 시 **접촉 틈 벌어짐** |
| **4g/4h** | RD vs P (exp/OpenRadioss/ABAQUS), 1400–2000 MPa | ⚠ **패널 문자 뒤집힘**(§9.7) · 두 솔버 격차 0.8–2.5 %p |

---

## 14. Post-processing ★

- **반력 추출 (OpenRadioss 특유)**: 강체 시간이력에 **순간 반력이 저장되지 않고 임펄스**가 저장된다.
  `J_Fi(t) = ∫₀ᵗ F_i(τ)dτ` (eq 1) → **미분**해서 `F_i(t) = dJ_Fi/dt` (eq 2).
  ⚠ 수치미분은 잡음을 증폭하는데 **필터링/스무딩 언급이 없다**.  Fig 4(a) 제하부의 계단 모양이
  그 흔적일 수 있다.  ⇒ 우리 MPM `wallP`(경계 반력 직합)와 **판독 규약이 다르다** — 비교 시 주의.
- **상대밀도**: `RD = Σ(초기 구 부피) / V_RVE(제하 중 5 MPa 시점)`.  RVE 부피는 **시뮬레이션 출력에서
  직접 측정**.  고체부피는 **압축 전 초기 구 부피 합**으로 근사 (탄소성 부피변화 무시 — J2 등적 + 탄성
  체적변형 `derived(ours)` 1.2 % 이므로 정당).
  ★★ **이것은 우리 `ε_sphere` 규약과 정확히 같다** (CLAUDE.md: "solid = Σ original sphere vol").
  ⇒ **porosity 규약 오프셋 없이 비교 가능** (우리가 DEM ε_sphere ↔ MPM union 사이에서 겪은 1.251 %p
  문제가 여기선 안 생긴다).
- **필드**: ParaView 로 von Mises, equivalent plastic strain, 변위, 단면(clip) — 정량 지표(배위수·
  접촉면적·tortuosity·percolation)는 **뽑지 않는다**.
- ⛔ **없는 후처리**: Heckel 적합, 접촉수/배위수, 접촉면적 분포, coverage, tortuosity, percolation,
  전달물성 σ, 힘사슬 통계, 시드 앙상블/오차막대.

---

## 15. ★★★ 우리 DEM+MPM 대비 (→ `our_dem_baseline.md`)

### 15.1 나란히 표
| 축 | **PyCompact (이 논문)** | **우리 (DEM + MPM)** | 판정 |
|---|---|---|---|
| DEM 코드 | **LIGGGHTS-PUBLIC 3.8** | **LIGGGHTS** | **같음** ✓ |
| DEM 접촉 | Hertz–Mindlin, µ_s 0.5 / µ_r 0.05 / COR 0.7 | **hooke/hysteresis** + adhesion (Luding 계열, 캡 없음) | 다름 (우리가 이력형) |
| DEM 영률 | ⛔ **n/a (미기재)** | **E_eff 1.35 GPa (real 24 에서 18× 연화)** | 비교 불가 — §7.1 |
| DEM 의 역할 | **패킹 생성기** (압축 미참여) | **압축 솔버**(300 MPa) + 전달망 | ⚠⚠ **구조적 차이 1** |
| 연속체 | **MPFEM** — 입자당 tet 메시, Lagrangian | **MPM** — MLS-MPM, Eulerian 격자 + material point, GPU/Taichi | 다름 |
| 연속체 재료 | **real E 170 GPa** + Swift 경화 (σ_y 0.59→1.39 GPa) | **E 1.53 GPa · ν 0.49 · σ_y 0.30 GPa** (softened-J2) | ⚠⚠ **구조적 차이 2** |
| 무차원 압력 P/σ_y | **1.44–3.39** | **1.0–2.0** | ★ **같은 밴드** — 방법론 비교 정당화 |
| 무차원 강성 E/σ_y | **288** | real 80–160 / **champion 5.1** | ★ 연화의 무차원 크기 = **16–56배** |
| 인계 시점 | **압축 전 (P≈0)** | **압축 후 (300 MPa 평형)** | ⚠⚠ **구조적 차이 3** |
| 인계 정보 | (x,y,z,r) | (x,y,z,r) | **같음** ✓ |
| 연속체가 받는 상 | **전 입자** | **SE 만** (AM freeze) | 다름 |
| 소성 표현 | **진짜 입자 형상 소성 (FE)** | **진짜 입자 형상 소성 (MPM)** | **같은 층** ✓ (층 3) |
| 접촉 표현 | **명시적 penalty + Coulomb µ=0.2** | **암묵적 격자 접촉** (같은 셀 = 사실상 융합·no-slip) | ⚠ **그들이 우위** |
| 대변형 견고성 | tet 메시 왜곡 위험 (PEEQ 1.3 에서 이미 심함, 논문 미논의) | **격자 재사용 → 왜곡 없음** | ★ **우리가 우위** |
| porosity 규약 | **Σ 초기 구 부피 / V_RVE** | **ε_sphere (동일)** | **같음** ✓ |
| 제하/springback | **푼다** (Fig 4a/4b 루프) | ⛔ **안 푼다** (hold/servo 정지 후 종료) | ⚠ **우리 공백** |
| 다분산/bimodal | ⛔ 단봉 2종 | ✓ bimodal(12:4:1), Furnas dip | ★ 우리 우위 |
| 다상(AM+SE) | ⛔ 1상 | ✓ 2상 + 첨가제(VGCF/PTFE/SDCP) | ★ 우리 우위 |
| 전달물성 σ | ⛔ **0건** | **σ_ionic/σ_e/σ_thermal 삼중항** (Kirchhoff/Holm + STEP3 복셀 FV) | ★★ **우리 고유** |
| 파괴 | ⛔ 없음 | Auerbach, fracture-aware Holm, CZM 원장 | ★ 우리 우위 |
| 실험 검증 | RD vs P (5점 × 2분말), **자기 그룹 데이터** | Minnmann porosity, Cronau overlap, Bazzoun EIS 등 **외부** | 무승부(성격 다름) |
| 비용 | 569입자 **9 h / 24 CPU** (CPU explicit) | 침대 32k 입자 **시간 단위** (GPU MPM) | ★★ 우리가 **자릿수** 우위 |
| 코드 공개 | **MIT, GitHub 공개** | 내부 | ⚠ 그들 우위 |

### 15.2 ★ 판정 (a) — 우리 3층 지도에서 MPFEM 은 **층 3(입자 형상 소성)** 을 하는가?
**한다. 명백히.**  근거 셋:
1. **정의로부터**: *"each particle is modeled as a deformable finite element body"* — δ-겹침 프록시가
   아니라 입자 내부를 이산화한다.
2. **결과로부터**: Fig 4(e)(f) 에서 구가 **다면체로 눌리고**, PEEQ 가 **1.3(=130 %)** 까지 간다.
   접촉 LAW(층 A/B)에는 이런 장(場)이 원리적으로 없다.
3. **저자 진술로부터**: DEM 은 *"neglect internal deformation"*, MPFEM 은 그것을 *"essential"* 하게 메운다.

⇒ **우리 판정 "층 3 은 DEM 이 아니라 연속체 소관" 의 직접 근거가 된다.**
그리고 이 논문은 **접촉 LAW 층을 아예 우회**한다 — Thornton–Ning 항복캡(우리 "경로 A")조차 필요 없다.
★ 층 지도에 붙일 한 줄: **"층 3 을 하는 방법은 두 가지 — 연속체를 입자마다 메시하거나(MPFEM),
입자 없는 연속체로 상 전체를 흘리거나(MPM).  DEM 접촉 LAW 를 아무리 정교화해도 층 3 에 도달하지 못한다."**

### 15.3 ★ 판정 (b) — 우리 MPM 대신 **MPFEM 을 썼어야 했나?**  (정직하게)

**MPFEM 이 우리보다 나은 점 (인정할 것)**
1. ★★ **접촉과 형상소성을 *한 이산화 안에서 동시에* 갖는다.**  이것이 우리 **두 반쪽 어느 쪽에도
   없는** 조합이다:
   | | 명시적 접촉(면적·힘·미끄럼) | 진짜 입자 형상소성 | 그래서 필요한 우회로 |
   |---|---|---|---|
   | **우리 DEM** | ✓ (강체 구 접촉망) | ✗ | **Stage-E** — 탄성 겹침 δ → 소성 접촉면적(Tabor/volume 캡) 재유도 |
   | **우리 MPM** | ✗ (격자 암묵, 같은 셀 = 사실상 no-slip 융합) | ✓ | **기하/변형 coverage** — 접촉면적 대신 표면 근접도(Hertz 0.13 / Tabor 0.26 µm 밴드) |
   | **MPFEM** | ✓ (penalty + Coulomb µ) | ✓ | **없음** |
   ⇒ MPFEM 이면 **변형된 실제 접촉면적 a(δ)** 를 직접 읽어 **Holm 협착저항 1/(2σr_c) 를 소성-변형된
   면적 위에서** 계산할 수 있다.  **우리 Stage-E 근사의 상위 대체재가 원리적으로 존재한다 —
   이건 우리에게 불리한 사실이고 그대로 적는다.**
   ⚠ 단 **이 논문은 그것을 하지 않았다** (전달물성 계산 0건).  가능성이 있다는 것이지 실증이 아니다.
2. **입자 정체성이 보존된다.**  MPM 에서 두 SE 입자가 같은 셀에 들어가면 사실상 **융합**(no-slip)되어
   입계 미끄럼이 사라진다.  MPFEM 은 µ=0.2 로 **미끄러진다**.  Fig 3(f) 가 그 µ 가 RD 를 1.8 %p
   움직인다고 보여준다 ⇒ **우리 MPM 은 그 자유도를 통째로 못 가진다.**
3. **제하/springback 을 자연스럽게 푼다** (§15.4).

**우리 MPM 이 나은 점**
1. ★★ **비용이 자릿수로 다르다** (§11): 569 입자 9 h / 24 CPU vs 우리 32,832 SE 입자 GPU 시간 단위.
   우리 침대를 MPFEM 으로 하려면 `derived(ours)` **≈1년**.  ⇒ **선택지가 아니었다.**
2. **대변형에서 메시가 안 터진다.**  PEEQ 1.3 이면 tet 이 심하게 왜곡되는데 논문은 remeshing/ALE 를
   언급하지 않는다.  MPM 은 격자를 매 스텝 새로 쓰므로 이 문제가 **없다**.
3. **void-fill 흐름과 상(phase) 융합**이 자연스럽다 — SE 가 공극으로 흘러들어 채우는 우리 핵심 그림은
   Lagrangian 메시로는 **자기접촉·위상변화** 처리가 필요하다.
4. **scaffold 커플링과 궁합**: AM 을 격자 마스크(v=0)로 얼리는 것은 MPM 에서 한 줄이다.
   MPFEM 이면 AM 도 메시(또는 강체 표면)로 만들어 접촉쌍을 다 정의해야 한다.

**⇒ 종합 판정**: **우리 규모에서는 MPM 이 옳은 선택이었다** (비용·대변형·void-fill).
**그러나 "MPM 이 더 좋은 물리" 라고 쓰면 과장이다** — MPFEM 은 **접촉을 명시적으로 갖는다는 점에서
우리보다 물리적으로 풍부하고**, 그 부재가 정확히 우리가 Stage-E 로 메우는 자리다.
★ 방어 가능한 문장: *"MPM 을 고른 이유는 침대 규모(3만 SE)와 대변형 견고성이지, 접촉 표현의
우수성이 아니다.  접촉 표현은 MPFEM 이 낫고, 우리는 그 결손을 Stage-E 접촉면적 보정으로 다룬다."*
★ **실현 가능한 절충**: **소형 SE-only REV(100–500 입자)** 를 OpenRadioss MPFEM 으로 한 번 돌려
**변형 접촉면적 a(δ) 분포**를 뽑고, 그것을 **우리 Stage-E(Tabor/volume 캡)의 외부 검증**으로 쓰는 것.
비용 `derived(ours)` = 그들 실측 스케일로 **수 시간~하루 급** ⇒ **실행 가능한 백로그 항목**.

### 15.4 ★ 판정 (c) — 훔쳐올 것
1. ★★ **porosity–pressure 하중+제하 루프 그림 형식** (Fig 4b).  우리 압밀 결과를 점이 아니라
   **루프**로 그리면 springback 이 드러난다.
2. ★★ **검증 프로토콜 3종 세트 + 비용표**: (요소/입자) × (마찰) × (RVE 크기) 민감도 + **Table 1
   (크기·입자수·벽시계)**.  우리 SI 에 그대로 옮길 수 있는 정직한 형식이다.
   ⚠ 단 **그들의 라벨링("convergence")은 훔치지 않는다** — 우리는 미수렴을 미수렴이라 쓴다.
3. ★ **5 MPa 판독 문턱 규약**의 아이디어(제하 곡선 위 고정 기준점)는 좋은데, **near-vertical 구간에
   두면 안 된다**.  우리가 쓴다면 **평탄 구간에 문턱을 두고 민감도를 함께 보고**할 것.
4. ★ **소수(prime) 시드 규약** — 시드 충돌 방지의 값싼 규율.
5. ★ **OpenRadioss = 무료 explicit 대변형 FE** 라는 도구 정보 자체.  위 15.3 의 소형 REV 실험 경로.
6. ★ **임펄스→미분 반력 판독**(eq 1–2)은 **반면교사**: 판독 규약이 다르면 곡선 모양이 달라진다
   (우리 wallP vs σzz 논쟁과 같은 종류).

### 15.5 ★★ 이 논문이 건드린 **우리 공백** — 제하(springback)
- 그들은 제하를 풀고 **RD 를 제하 후에 잰다**.  우리는 **하중 중/정지 시점**의 porosity 를 보고한다.
- `derived(ours)` 탄성 회복변형 = P/E:
  | 모델 | 값 |
  |---|---|
  | 그들 (2000 MPa / 170 GPa) | **1.2 %** |
  | 우리 **DEM** (300 MPa / E_eff 1.35, ν 0.3 ⇒ K 1.125 GPa) | **체적 26.7 %** ⚠ |
  | 우리 **MPM** (300 MPa / K 25.5 GPa, ν 0.49) | **체적 1.2 %** ✓ |
- ⇒ ★★ **우리 MPM 의 stiff-bulk(ν=0.49) 선택이 제하 축에서 정확히 실재 금속분말과 같은 자리**에
  있고, **우리 DEM 의 18× 연화는 제하 축에서 비물리적**이다 (체적 회복이 26 %).
  우리는 제하를 안 풀기 때문에 **지금은 노출되지 않은 잠재 한계**다.
  ⚠ **열린 질문**: 우리 실험 앵커(Minnmann pure-SE 10 %, Cronau overlap)가 **가압 중** 측정인지
  **해압 후** 측정인지 — 후자라면 우리 DEM porosity 를 해압 후 값과 맞춘 것이 되어 규약이 어긋난다.
  ⇒ **문헌 재확인 필요(미해결).**  이 카드가 그 질문을 만들었다.

---

## 16. 적용 인사이트 (우리 연구에 어떻게)

- ① ★★ **원고 논거 보강 (§5)**: "DEM 은 입자 형상 소성을 못 한다 ⇒ 연속체가 필요하다" 에
  **무관한 소재·무관한 그룹의 2026 SoftwareX 진술**을 붙인다.  대칭 진술(c)까지 함께 쓰면
  **frame[5] 분업이 우리 편의가 아니라 방법론의 구조**라는 논증이 완성된다.
- ② ★★ **인계 시점의 차이를 우리 novelty 로 명시**: PyCompact 은 *DEM=패킹 / 연속체=압축*,
  우리는 *DEM=압축·전달 / 연속체(MPM)=SE 형상*.  후자는 **DEM 이 이미 실험에 보정된 골격**을
  넘기므로 **연속체가 패킹을 다시 만들 필요가 없다** = 우리 scaffold 의 논거.
  ⚠ 동시에 정직하게: 그 대가로 우리 결과는 **DEM 강성 보정에 종속**되고, 그들 결과는 아니다.
- ③ ★ **Stage-E 외부 검증 실험**: 소형 SE-only REV(100–500 입자) MPFEM(OpenRadioss) →
  **변형 접촉면적 a(δ)** 분포 → 우리 Tabor/volume 캡과 대조.  자릿수로 실행 가능(수 시간~하루).
  성공하면 **Stage-E 가 근사인지 정당한지**를 처음으로 외부에서 잰다.
- ④ ★ **springback 축 개시**: Fig 4(b) 형식으로 우리 압밀을 루프로 그리고, MPM(ν=0.49)과
  DEM(E_eff 1.35)의 **제하 거동 차이**를 보고한다.  현재 아무도 안 본 축이고, §15.5 대로
  **DEM 쪽이 비물리적일 것으로 예상**되므로 미리 라벨해 둔다.
- ⑤ **비용 논거 확보**: "왜 MPM 인가" 에 대해 **문헌 실측 기반 수치**(569입자 9 h/24 CPU,
  입자수 지수 1.3–2.4)로 답할 수 있게 됐다.

---

## 17. 인용 가능 문장 (deck/paper용)

- *"An independent open-source DEM–MPFEM workflow (Mohammadhosseinzadeh et al., SoftwareX 33 (2026)
  102495) adopts the same division of labour we use: DEM supplies the packing kinematics and a
  continuum discretisation supplies the particle-level plasticity.  The authors state the reason
  explicitly — DEM rests on **'assumptions of rigid or simplified particle shapes that neglect internal
  deformation'**, whereas in MPFEM **'each particle is modeled as a deformable finite element body'**,
  a capability they call **'essential for accurately predicting high-pressure compaction behaviour'**."*
- *"The same paper states the mirror limitation of a homogenised continuum — it **'overlooks the
  discrete nature of particles, leading to inaccuracies in modeling low-density stages where particle
  rearrangement dominates'** — so the two-model split is a structural property of the methods, not a
  convenience of our study."*
- *"Their handoff is a single (x, y, z, r) table taken at the gravity-settled state; ours is the same
  table taken after the 300 MPa DEM equilibrium.  Both transfer geometry only — no contact list, no
  stress history."*
- ⚠ **쓰면 안 되는 문장**: "MPFEM 은 상대밀도를 2.5 % 이내로 맞춘다 ⇒ 우리도 그 정도" —
  재료(강철계 금속)·압력(2000 MPa)·규약(제하 후 5 MPa)이 전부 다르다.

---

## 18. 주의 / 한계 (over-claim 방지)

**저자가 인정한 것**
- 단봉 2종 · 작은 RVE · **완전 구 가정이 치밀화를 과소평가** · DEM–MPFEM 데이터 전달의 어려움 ·
  대규모 계산비용 · 편차 원인 5종(메시·PSD 패킹·마찰 알고리즘·RVE 경계·솔버 차이).

**우리 쪽 전이 금지 목록**
- ⛔ **재료**: Fe–Si–Al–P (E 170 GPa, σ_y 0.59–1.39 GPa) ≠ LPSCl (E 22–24, σ_y 0.05–0.30).  절대 porosity·
  RD·응력 **전이 금지**.  (무차원 P/σ_y 밴드 겹침만 방법론 비교의 근거로 쓴다.)
- ⛔ **압력**: 1400–2000 MPa = 우리 300 MPa 의 **4.7–6.7배**.
- ⛔ **전달물성 0건** — σ 축에 이 논문을 인용할 여지 없음.
- ⚠ **검증 루프가 그룹 내부** ([15][16][17] 전부 같은 그룹) → frame[4] 의 "외부 실험 앵커" 아님.
- ⚠ **시드 앙상블·오차막대 0** — 케이스당 런 1개.  2.1 %p 편차에 **통계적 불확실도가 없다**.
- ⚠ **재하율(펀치 속도) 미기재** — explicit 동역학의 핵심 파라미터.  우리 platen-mach 교훈 적용 대상.
- ⚠ **DEM 영률 미기재** → "실제 E 를 썼나 낮췄나" 판정 불가 = `n/a`.
- ⚠ **µ 는 사실상 보정 노브** (Fig 3f, "selected for best experimental agreement").

**내가 잡은 내부 불일치 (인용 시 정정 필요)**
1. ★ **Fig 4(g)/(h) 패널 문자 뒤집힘** — 그림 범례(g=Fine, h=Coarse) ↔ 캡션·본문(g=Coarse, h=Fine).
   값으로 보면 **범례가 맞다**.
2. ★ **"convergence" 라벨** — Fig 3(e) 는 2000→2500 에서 `derived(ours)` −5 % 로 **단조 감소 중**이고
   평탄부가 없다.  선택 근거는 본문이 밝힌 대로 **런타임(9 h vs 36 h)** 이다.
3. ★ **제하 후 RD 삼각형이 닫히지 않는다** (§10): Fig 4(a) 유도 ≈90.3 % / Fig 4(b) 종단 ≈83–84 % /
   stated 85.4 %.  **≈5–7 %p, 헤드라인 편차보다 크다.**  (부피 규약 차이일 가능성 + 내 digitize 오차 가능성.)
4. **"fine … due to its denser packing"** ↔ Fig 4(b) 초기 porosity 는 Fine 이 **더 높다**(`digitized`).
5. **µ 선택 근거** — Coarse 단독으로는 `digitized` µ=0.1 이 실험에 더 가깝다.
6. **DEM µ_s=0.5 vs MPFEM µ=0.2** 불일치, 설명 없음.
7. **버전 불일치**: C7(FreeCAD 1.0.2 / LS-PrePost 4.9) ↔ refs [24](1.0.1) / [26](4.8).
8. **요소 +25 %에 런타임 4배**(9→36 h) 미설명.
9. **초록 "maximum relative density deviation of only 2.5 %"** 는 **상대**값이다 (절대 2.1 %p).
   퍼센트포인트로 오독하면 정확도를 과대평가하게 된다.

---

## 19. 기법 미니 용어집 (이 카드 안에서만 통용)

| 용어 | 뜻 | 우리 대응 |
|---|---|---|
| **MPFEM** (multi-particle FEM) | 입자 **하나하나**를 변형 가능한 FE 바디로 메시해 접촉과 함께 푸는 방법.  균질화 FEM 과 다르고, 강체구 DEM 과도 다르다 | MPM 과 **같은 층(3)**, 다른 이산화 |
| **cfile** | LS-PrePost 의 명령 스크립트 (GUI 조작을 텍스트로) | 우리 seeding 스크립트 |
| **material.k** | 입자마다 `pid/secid/mid` 를 찍는 LS-DYNA 키워드 조각 | 우리 상(phase) 배정 |
| **pts / pdd** | LIGGGHTS `fix particletemplate/sphere` / `fix particledistribution/discrete` — 반지름 템플릿과 그 가중 | 우리 PSD 입력 |
| **raindrop insertion** | 위에서 비처럼 뿌려 중력 침강시키는 초기 패킹법 | 우리 pour/settle |
| **Swift 경화식** | `σ=K(ε+ε₀)ⁿ` 멱함수 경화 | 우리 J2 + 선형경화(HARD_SE) |
| **/TYPE26 general contact** | OpenRadioss 의 penalty 기반 surface-to-surface 자동접촉 | MPM 격자 접촉(암묵) |
| **impulse readout** | 강체 시간이력에 ∫F dt 만 저장 → 미분해 F 복원 | 우리 `wallP` 직합 |
| **PEEQ** | equivalent plastic strain (누적 소성변형) | 우리 MPM 누적소성 Σdg |
| **relative density (RD)** | 고체부피/전체부피 = 1 − porosity | 우리 1 − ε_sphere |

---

## 20. 우리 백로그로 나가는 항목 (요약)

| # | 항목 | 상태 |
|---|---|---|
| P-1 | §5 인용문 3종을 원고 서론/방법 논거에 배선 | **즉시 가능** (텍스트) |
| P-2 | 소형 SE-only REV MPFEM(OpenRadioss) → 변형 접촉면적 a(δ) → **Stage-E 외부 검증** | 신규 제안, 자릿수 실행가능 |
| P-3 | porosity–pressure **하중+제하 루프** 그림 형식 도입 | 신규 |
| P-4 | **springback 축**: MPM(ν0.49) vs DEM(E_eff 1.35) 제하 거동 대조 | 신규 · §15.5 |
| P-5 | Minnmann/Cronau 앵커가 **가압 중인가 해압 후인가** 문헌 재확인 | **미해결 질문** |
| P-6 | 검증 프로토콜 3종 + 비용표(Table 1 형식)를 우리 SI 양식으로 | 형식 도입 |

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
