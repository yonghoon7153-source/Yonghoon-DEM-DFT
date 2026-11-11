# PyCompact — LIGGGHTS DEM → MPFEM(OpenRadioss) 분말압축 오픈소스 워크플로 ★★ 우리 DEM→MPM scaffold 인계의 **독립 선례** (인계 시점은 정반대) — Mohammadhosseinzadeh (SoftwareX 2026)

> slug `pycompact2025_dem_mpfem_workflow` · DOI `10.1016/j.softx.2025.102495` · type `DEM+MPFEM (workflow/software)` · PDF `02d3addf-1-s2.0-S2352711025004613-main.pdf` · digested `2026-08-25` · 보강 `2026-11-11` · status ✅
>
> ⓘ **보강 2026-11-11 (그림 크롭 + 원문 재대조)** — ① 그림 폴더 신설 `litdb/figures/pycompact2025_dem_mpfem_workflow/`
> = **37 장** (그림 4 + 패널 15 · 번호 표 3 + 코드 메타데이터 표 1 · 식 (1)(2)(3) 따로 + 식 문단 1 · 근거 문단 9) + 판독 원자료
> `digitized.csv` (§13).  ② **§4.7 넘겨받는 과정 (가)–(차)** · **§15.6 넘겨받는 과정 대조 표** 신설.  ③ 원문 · 그림 재대조로
> **고친 곳**: Fig 3(e) 판독 (2000 ≈1375 → **1398**, 2500 점 **≈1379** = 본문 1310 과 불일치 → "−5 % 미수렴" 판정 철회 §9.1) ·
> Fig 4(a) 제하 끝 (잔류 ε 0.598/0.556 은 20–50 MPa 근처 값 → 응력 0 꼬리 끝 **0.56 / 0.505** §9.4) · Fig 4(b) 가압 가지
> (500 MPa ≈33/31 % → **27.0 / 24.7 %** · 압력축 0 눈금은 틀 왼끝이 아니다 §9.5) · "제하 후 RD 삼각형이 5–7 %p
> 안 닫힌다" **철회** (닫힌다 §10) · "Fine 이 더 성기게 쌓였다" 철회 (§8) · σ_y(ε=0) 590.6 → 590.7 · '포화유동응력' 표기 ·
> P/E ↔ P/K 혼용 (§14 · §15.5) · 36 h 메시 시험의 분말 (Fine 569 → Coarse 문단 §11) · 569 입자 9 h 에 붙인 '24 CPU'
> (Table 1 에 CPU 수 없음 — 24 CPU 는 Table 3 의 Coarse 7 h) · RVE '정육면체' → 가로 두 변만 인쇄 · 'J2형' 은 원문 표현
> 아님 · Fig 4(a) '제하부 계단' 은 그림에 없음 · Minnmann 앵커 표기에 `CL-94` 철회 표지.  ⑤ 새로 더한 원문 사실: Table 2 의
> ABAQUS 칸 빈칸 · '모든 계산 2000 MPa' ↔ 그림 1400–2000 MPa · 9 h 가 두 곳 · 압분체 되돌아옴 ≈ 재료 P/K 의 8 배 (§15.5).
> ⑥ PDF 칸 = 이번 inbox 파일 (옛 칸 = 첫 digest 때의
> 업로드 이름 `1e08fdc4-PyCompact_lation.pdf` — 그 파일은 지금 inbox 에 없다 · 카드의 DOI 와 이번 PDF 의 DOI 가 같다).
> 보강 전 판독값은 고친 줄에 '옛 판독' 으로 남겼다.
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
configuration — *"Initial powder configuration (size, center)"*, Fig. 1 — is exported as a
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
| 제목 (원문 p.1) | *"PyCompact: An integrated workflow for discrete element method–multi-particle finite element method for powder compaction simulation"* |
| 저널 | **SoftwareX 33 (2026) 102495** (Elsevier, **open access CC BY-NC**) |
| DOI | 10.1016/j.softx.2025.102495 |
| 날짜 | Received 2025-09-01 · Revised 2025-12-02 · Accepted 2025-12-18 · Online 2026-01-06 |
| 분량 | 본문 9 pp · Fig 1–4 · Table 1–3 (+ 번호 없는 코드 메타데이터 표 C1–C9) · 번호 식 3 (식 1–3) · refs 32 · **SI 없음** |
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
| ⇒ 초기항복 σ_y(ε=0) | **590.7 MPa** | `derived(ours)` = 1380·0.0354^0.254 = 590.67 (2026-11-11 정정: 옛 590.6 은 끝자리 반올림) |
| ⇒ σ(ε=1.0) / σ(ε=1.3) | **1392 / 1485 MPa** | `derived(ours)`.  Fig 4c/d von Mises 컬러바 상한 **1500 MPa** (1.5e+03, 그림 인쇄) 와 정합 ✓ |
| ⇒ **P/σ_y** | **3.39**(초기항복) ~ **1.44**(ε = 1.0 의 유동응력) | `derived(ours)`, P=2000 MPa.  ⚠ Swift 식은 포화하지 않는다 (2026-11-11 정정: 옛 표기 '포화유동응력') — 1.44 는 PEEQ 컬러바 상한 1.3 근처의 값.  ★ **우리 1.0–2.0 과 같은 밴드** (§15) |
| ⇒ **E/σ_y** | **288** | `derived(ours)`.  우리 real 80–160 · **MPM champion 5.1** ⇐ 연화의 무차원 척도 |

### 3.2 분말·RVE·압력 (stated)
| 항목 | Fine | Coarse |
|---|---|---|
| 평균 입경 (본문) | **16 µm**, sd **9.4 µm** | **118 µm**, sd **17 µm** |
| 모델 반지름 범위 | **6–33 µm** (⌀12–66) | **48–96 µm** (⌀96–192) |
| RVE 크기 (Fig 3c 의 **가로 두 변** 화살표 · 캡션 'RVE size') | **210 µm** | **1000 µm** |
| RVE 높이 | **[미확인]** — 인쇄 없음 (2026-11-11 정정: 옛 표기 '정육면체 한 변' 은 원문에 없다) | [미확인] |
| 입자 수 | **569** | **403** |
| 최대압력 | **2000 MPa** | 2000 MPa (곡선은 1400–2000 MPa 5점) |
| ⇒ RVE/입경 | **≈8 입자** | **≈7 입자** `derived(ours)` |
| ⇒ 넘길 때 충전율 (압력이 뜨기 시작하는 점의 1−φ) | **≈0.572** (φ 42.8 %) | **≈0.576** (φ 42.4 %) `digitized` Fig 4b · 2026-11-11 재판독 (옛 판독 φ₀ ≈ 43 / 41.5 % — 둘의 차 0.4 %p 는 화소 두 칸 = 판독 오차 안) |

⚠ **본문 평균입경 ↔ 모델 반지름 범위가 안 맞는다** — Fine 은 "평균 ⌀16 µm" 인데 모델 최소가
**⌀12 µm** 라 평균이 범위 바닥에 붙는다.  Fig 3(a) 는 **weight fraction** 이고 그 최빈값은
`digitized` **⌀35–40 µm** 다.  ⇒ "평균 16 µm" 은 **개수평균**, 모델 샘플은 **부피가중**으로 보인다
(논문 미명시).  `derived(ours)`: 패킹 0.59 를 가정해 역산한 유효 평균 직경은 **Fine ⌀26.4 µm ·
Coarse ⌀141 µm** (둘 다 stated 평균보다 크다 — 위 해석과 부호 일치).  ⚠ 이 역산은 RVE 를 **정육면체** (높이 = 가로 변)
로 놓은 산술이다 — 높이는 원문에 없다 (위 표).  Fig 3(a) 재판독 (2026-11-11 · `digitized.csv`): Fine 봉우리 0.025 @ ≈38 µm
(반치 ≈11–56 µm) · Coarse 봉우리 0.017 @ ≈122 µm (반치 ≈100–163 µm) — x 축 = **지름** (축 제목 'Particle Diameter').

### 3.3 결과 (헤드라인)
| 항목 | 값 | 종류 |
|---|---|---|
| **상대밀도 (Fine)** | exp ≈ **87 %** · sim ≈ **87 %** ("negligible difference") | stated |
| **상대밀도 (Coarse)** | exp **83.3 %** · sim **85.4 %** | stated |
| **최대 편차** | **2.5 %** = **2.1 %p** (85.4/83.3 = 1.0252) | stated + `derived(ours)` |
| 문헌 편차 밴드 | **0.5–4 %** [8,13,14,20,32] | stated |
| 압력 스윕 | **1400 · 1500 · 1600 · 1800 · 2000 MPa** (5점) | `digitized` (Fig 4g/h) |
| 하중 중 porosity @2000 MPa | **≈4.4 %(Coarse) / ≈3.3 %(Fine)** | `digitized` (Fig 4b · 2026-11-11 재판독, 옛 판독 ≈4.5 / 3.5) |
| 제하 끝 porosity (P≈0 수직 구간의 위 끝) | **≈17.2 % / ≈16.9 %** | `digitized` (Fig 4b).  ⚠ 그 수직 구간 (Fine **12.1 → 16.9 %**) 은 압력 **0–5 MPa = 화소 한 칸** 안에서 생긴다 = Fig 4a 의 응력 0 꼬리와 같은 구간 — 펀치가 압분체에 닿아 있는지 인쇄 없음 (§10) |
| 5 MPa 규약 자리의 porosity | **Fine ≈12 %** (수직 구간 아래 끝) · Coarse ≈13–14 % (P 11–16 MPa 에 12.8–14.2 %) | `digitized` (Fig 4b) — 본문 RD ≈87 % (Fine) · 85.4 % (Coarse) 와 정합 [카드 판독 대조] |
| 상대밀도 판독 규약 | **제하 중 5 MPa 도달 시점**의 RVE 부피 | stated ★ (§10 참조) |
| 고체부피 규약 | **압축 전 초기 구 부피 합** ("volumetric changes … negligible") | stated ★ = **우리 ε_sphere 와 같은 규약** |

### 3.4 민감도 3종 (Fig 3e/f/g)
| 스윕 | 값 | 종류 |
|---|---|---|
| 요소/입자 → 95 %밀도 축응력 (Coarse) | 500 → **1650 MPa**, 2500 → **1310 MPa** | stated (p.6) |
| 〃 그림의 다섯 점 | 500 ≈**1641** · 1000 ≈**1529** · 1500 ≈**1469** · 2000 ≈**1398** · 2500 ≈**1379** | `digitized` Fig 3(e) (표지 무게중심 · 1 화소 = 4.8 MPa · 2026-11-11 두 판독 일치).  옛 판독 1510 · 1440 · 2000 ≈1375 |
| ⚠ 그림 ↔ 본문 | **2500 점: 그림 ≈1379 ↔ 본문 1310** (≈ 70 MPa · 화소 14 칸) | 원문 안 불일치 — 어느 쪽이 맞는지 [미확인] |
| 〃 런타임 | **2000 el → 9 h**, **2500 el → 36 h** | stated (p.6 · Coarse 메시 시험 문단) |
| ⇒ 선택 메시(2000)의 **잔여 격자의존** | 그림대로 **−1.4 %** (1398 → 1379) · 본문 숫자로 **−6.3 %** (1398 → 1310) | `derived(ours)` — 그림은 평탄화, 본문 숫자는 미평탄.  (옛 표기 '−5 % · 수렴 아님' 은 그림 2000 점과 본문 2500 값을 섞은 산술 → 철회) |
| 마찰 µ(MPFEM) → RD (Coarse, 2000 MPa) | 0.1 ≈**84.2** · 0.2 ≈**85.5** · 0.3 ≈**85.9 %** | `digitized` (0.2 값이 stated 85.4 와 0.1 %p 안 ✓ = 눈금 검증됨; 옛 판독 0.3 ≈86.0) |
| RVE → RD (Fine, 2000 MPa) | 210 ≈**86.9** · 250 ≈**87.0** · 300 ≈**87.5 %** (EXP 선 ≈87.8) | `digitized` (옛 판독 87.1 · 87.4) |
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
Fig. 1 의 두 단계를 잇는 화살표 라벨이 그대로 인계물의 정의다 — **"Initial powder configuration
(size, center)"**.  (그림 원본 = `fig_1.png` · 자료 흐름 = `fig_2a.png` · 원문 문단 = `txt_p2_p3_handover_interface_csv.png`)

### 4.2 ★ 인계 **시점** = 중력 침강 직후, 압축 **전** (P ≈ 0)
> *"The particles are generated with a raindrop insertion method, then settled under gravity [28].
> The settled configuration is exported in VTK format… **Since DEM effectively manages the kinematics,
> the resulting configuration serves as a realistic initial configuration for MPFEM.**"*

⇒ DEM 은 **패킹 생성기**일 뿐이고, **압축(1400–2000 MPa)은 100 % MPFEM 이 한다.**
Fig 4(b) 의 하중곡선이 porosity **≈42–43 % 에서 ≈3–4 %** 까지 내려가는 그 전 구간이 MPFEM 소관이다
(`digitized` 2026-11-11 · 옛 표기 41 → 4 %).
⚠ 우리와 **정반대**다 — 우리는 LIGGGHTS 가 **300 MPa 압축을 끝낸** `atom_2060000` 좌표를 넘긴다.

### 4.3 ★ 인계 **정보** = 좌표 + 반지름, 그게 전부
| 넘기는 것 | 안 넘기는 것 |
|---|---|
| 입자 중심 (x, y, z) | 접촉 리스트 · 접촉당 겹침 δ |
| 반지름 r | 접촉력 / 힘사슬 |
| (VTK 에는 particle ID 도 있다 (p.2) — CSV 칸은 **(x, y, z, r) 뿐** (p.2 · p.3 · Fig 2a 라벨 '.CSV File (x, y, z, r)'); FE 쪽 pid · secid 는 입자 번호 i 로 **다시 매긴다** (Fig 2c) — VTK ID ↔ pid 대응은 인쇄 없음) | 응력·변형 이력 · 속도 |
| — | DEM 강성(E)·마찰 이력 |
⇒ **상태변수(state) 전달 0.  순수 기하 인계.**  (오른쪽 칸 = CSV 칸 정의에서 나온 [카드 추론] — 원문은 '버린다' 고
적지 않고 CSV 칸만 적는다.)  MPFEM 의 'Initial stage' 프레임 (Fig 4c/d 왼쪽) 은 전 입자가 von Mises 눈금 맨 아래 색이다
[판독 — 0 인지 수십 MPa 인지는 색으로 못 가른다] → 무응력 출발과 모순 없음 (원문에 '초기 응력 0' 문장은 없다).

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

### 4.7 ★★★ 넘겨받는 과정 (가)–(차) — 원문 위치와 함께 (2026-11-11 보강)

> 1저자 11-11: *"우리랑 비슷한 과정인거 같으니까 dump 를 mpm 으로 가져오는"* — 이 논문은 DEM 결과를 다른 풀이 (입자별 FE)
> 로 넘겨 압축을 다시 푼다.  아래는 원문 9 쪽 · 그림 · 표 · 코드 메타데이터를 다시 읽고 항목마다 위치를 단 것이다.
> 표지: 인쇄 = 원문 문장 · [판독] = 그림에서 읽음 (`digitized.csv`) · [카드 산술] · [카드 추론] = 원문 문장에서 이끈 것 ·
> [미확인] = 원문에 없음.  근거 크롭 = §13 의 `txt_*` · `eq_*` · `fig_2*`.  우리 쪽과의 대조 표 = §15.6.

**(가) 무엇을 넘기나 — 중심 (x, y, z) 와 반지름 r, 넷뿐**
- 인쇄 (p.2 §2.1 · `txt_p2_p3_handover_interface_csv.png`): *"The settled configuration is exported in VTK format, including the
  particle IDs, centers, and radii of the particles. … Then, using ParaView, the VTK output is filtered and exported to CSV with
  (x, y, z, r).  **This file forms the interface between DEM and MPFEM.**"*
- 같은 말이 세 번 더: p.3 *"converted to CSV files containing particle coordinates and radii (x, y, z, r)"* · Fig 2(a) 라벨
  **'.CSV File (x, y, z, r)'** · Fig 1 화살표 **'Initial powder configuration (size, center)'**.
- 파일 · 단위: 입력 파일 이름 `position.csv` (Fig 2c) · DEM 은 **cm** 로 돌리고 *"multiplying by 10 converted the particle radii
  and positions into millimeters"* (p.3) — Fig 2(c) 의 매개변수 `unit_scale`.
- 넘어가지 않는 것: 접촉 목록 · 겹침 · 속도 · 접촉력 · 응력 — 원문에 '버린다' 는 문장은 없고, CSV 칸이 넷뿐이라 넘어갈 자리가
  없다 [카드 추론].  입자 ID 는 VTK 에 있지만 CSV 칸에 없고, FE 쪽은 `pid = i` · `secid = i` 로 다시 매긴다 (Fig 2c · p.3).
- 재료 값도 넘기지 않는다: DEM 재료 값은 사용자 템플릿 (`sample.txt`) 안에 있다 — *"The template file provides the general
  structure of a LIGGGHTS input script, including definitions of material properties, units, boundary conditions, contact models,
  simulation domain, and timestep settings, which the user customizes"* (p.3 · `txt_p3_inputgen_template_psd_seed_generation.png`).
  FE 재료는 §3 에서 따로 정한다 ((마)).

**(나) 언제 넘기나 — 가압 전 · 중력 침강 뒤 (압력 0)**
- 인쇄: *"The particles are generated with a raindrop insertion method, then settled under gravity [28]. The settled configuration
  is exported …"* (p.2) · 삽입 = `fix insert/rate/region` *"until the target particle count is achieved"* (p.3) · Fig 3(c) 캡션
  *"powder models after DEM settlement"* · 단계 정의 *"particle generation using DEM and compaction (loading-unloading) simulation
  using MPFEM"* (p.2).  ⇒ DEM 은 누르지 않는다.
- 넘긴 순간의 충전율 · 층 높이 · 접촉 겹침: **[미확인]** (인쇄 없음).  그림에서는 FE 판독으로 압력이 뜨기 시작하는 점의 기공
  Fine **42.8** · Coarse **42.4 %** → 충전율 ≈ 0.57–0.58 [판독 Fig 4b].  ⚠ 이것은 펀치가 층에 닿는 순간의 RVE 부피로 잰 값이라
  층 윗면의 요철 틈이 들어간다 — DEM 충전율 출력이 아니다 [카드 추론].
- 침강을 언제 멈췄나 (운동 에너지 문턱 · 시간): **[미확인]**.

**(다) 넘긴 뒤 입자를 어떻게 다시 만드나 — 구마다 사면체 메시**
- 인쇄 (p.3 · `txt_p3_dem_settings_and_dem_to_mpfem_conversion.png` · Fig 2c): MeshMatGen.ipynb 가 LS-PrePost 명령 파일 (cfile) 을
  만든다 — *"the script creates solid spheres at the specified positions with the provided radii, applies a tetrahedral mesh to
  each particle, and generates both surface and part sets"* · 실행하면 *"meshed spheres for each particle, with approximately the
  target number of elements per particle"*.
- 사용자 매개변수: *"mesh density, number of elements and nodes, and the minimum and maximum edge sizes for tetrahedral meshing"*
  (p.3; Fig 2c `unit_scale, mesh_dens, …, mesh_edge_size`) — 값 **[미확인]** (평균 요소 수만 인쇄).
- 요소: 4 절점 사면체 `/TETRA4` ↔ ABAQUS `C3D4` (p.6 · Table 2) · 입자당 **평균 2000** 요소 (p.6) → 총 요소 Coarse 403 × 2000
  ≈ **0.81 M** · Fine 569 × 2000 ≈ **1.14 M** [카드 산술].  지름당 요소 변 ≈ 7.7 개 (2000 요소 · 같은 크기 정사면체로 구 부피를
  나눈 가정 (N/(√2 π))^(1/3)) · 500 → 2500 요소면 4.8 → 8.3 개 [카드 산술].
- 겹친 구 · 틈의 처리: **원문에 문장 없음 [미확인]**.  FE 접촉은 *"a penalty-based contact formulation, enabling realistic sliding
  behavior while preventing physical overlap"* (p.3) — DEM 침강 상태의 겹침 (Hertz δ > 0) 을 그대로 구로 되살리면 초기 상호침투로
  출발한다 (§4.3 의 '논문이 다루지 않은 구멍', [카드 추론]).
- 나머지 조립: 다이 · 펀치 · 접촉 · 재료 · 경계는 LS-PrePost 에서 **손으로** (p.3).  재료 배정 = `material.k` (`pid = i` ·
  `secid = i` · `mid = 1` · *PIECEWISE_LINEAR_PLASTICITY*) → proj 로 저장 → 다시 열어 k 로 저장 → 맨 위 자리표시 블록을
  치환 (p.3 · `txt_p3_material_k_assignment_keyword_roundtrip.png`).

**(라) 넘긴 직후의 평형 — 문장 없음**
- 초기 응력 · 재평형 단계 (중력 재정착 · 감쇠 이완 등) · FE 단계의 중력: **[미확인]**.
- 그림 근거: Fig 4(c)(d) *'Initial stage'* 는 전 입자가 von Mises 눈금 맨 아래 색 [판독].  Fig 4(a) 는 응력이 Fine 0.287 ·
  Coarse 0.371 변형률까지 **0** 이고, Fig 4(b) 의 P ≈ 0 수직 구간 (Fine 60.9 → 42.8 %) 이 같은 구간이다 → 펀치가 층 위 빈
  공간에서 출발해 내려온다 [판독 · 카드 추론].  펀치 출발 높이 · 변형률의 기준 길이는 인쇄 없음.

**(마) 재료 · 접촉 · 마찰 — 두 풀이가 다르다**

| 항목 | DEM (LIGGGHTS-PUBLIC 3.8) | MPFEM (OpenRadioss r2024) | 원문 위치 |
|---|---|---|---|
| 접촉 법칙 | Hertz–Mindlin (tangential) | 일반 접촉 `/TYPE26` · 벌칙 (penalty) 면–면 + Coulomb | p.3 · p.6 · Table 2 |
| 입자–입자 마찰 | 미끄럼 **0.5** · 구름 **0.05** | Coulomb **0.2** (*"selected for best experimental agreement"*) | p.3 · p.6 |
| 반발계수 | **0.7** | — | p.3 |
| 입자–벽 마찰 | [미확인] | [미확인] (Table 2 의 'Friction coefficient 0.2' 한 줄뿐) | Table 2 |
| 영률 · ν · 밀도 | 템플릿 파일 안 (값 [미확인]) · density 는 InputGen 에서 사용자 지정 | E **170 GPa** · ν **0.3** · ρ **7130 kg/m³** (ref [17]) | p.3 · p.5 |
| 소성 | 없음 (구 · 점접촉) | Swift σ = K(ε + ε₀)ⁿ · K **1380 MPa** · n **0.254** · ε₀ **0.0354** (식 3) · `PIECEWISE_LINEAR_PLASTICITY` | p.5 · p.3 |
| 단위 | cm | mm (×10) | p.3 |

⇒ 같은 분말인데 마찰을 **다르게** 둔다 (0.5 ↔ 0.2) — 설명 없음 (§9.2).  DEM 값이 FE 답에 들어가는 길은 **초기 배치 하나**
[카드 추론].

**(바) 경계 · 하중 — 금형 고정 · 펀치 지정 운동 · 속도는 인쇄 없음**
- 인쇄: *"The packed assemblies were then converted to meshed deformable spherical particles with a rigid die and punch. The die
  was fully constrained, while the punch moves downward using a prescribed motion rigid boundary condition to a target peak pressure
  followed by unloading."* (p.5 · `txt_p5_material_constants_and_fe_boundary_conditions.png`) · 다이 · 펀치 = 강체 `/SHELL` ↔ `R3D4`
  (Table 2) · *"rigid tooling (die walls and punch)"* (p.2).
- RVE: 가로 1000 / 210 µm (Fig 3c) · 높이 [미확인] · 옆면 = 강체 다이 — 주기 경계 문장 없음.
- *"A peak pressure of 2000 MPa was applied in all simulations"* (p.6) — 그런데 Fig 4(g)(h) 는 **1400–2000 MPa 다섯 점**이다.
  낮은 압력 점을 따로 돌렸는지 · 2000 런에서 읽었는지 **[미확인]**.
- 펀치 속도 · 시간 간격 · 질량 스케일링 · 감쇠 · 준정적 판정 (운동 에너지 비 등): **전부 [미확인]** — 풀이 종류는 'Explicit'
  (Table 2) 만.
- 반력 판독: 강체 시간 이력에는 충격량만 남는다 → J_Fi(t) = ∫₀ᵗ F_i(τ)dτ (식 1) 를 F_i(t) = dJ_Fi/dt (식 2) 로 미분 (p.3 ·
  `eq_01_impulse_definition.png` · `eq_02_force_from_impulse.png`).  압력 = 반력 ÷ 면적의 면적 정의 · 미분 평활은 [미확인].

**(사) 하중을 뺄 때 — 같은 계산에서 푼다**
- 인쇄: *"Powder compaction simulations occur in two phases: loading to a peak nominal pressure and then unloading"* (p.3) ·
  *"During unloading, the stress drops rapidly, indicating elastic recovery. However, the remaining strain after unloading reveals
  that permanent densification has taken place."* · *"During unloading, stress relaxation showed elastic recovery primarily at particle
  peripheries"* (p.6 · `txt_p6_compaction_stages_loading_unloading_mechanics.png`).
- 값 [판독 2026-11-11 · Coarse / Fine]: Fig 4(a) 변형률 최고 **0.622 / 0.576** → 100 MPa 0.603 / 0.559 → 20 MPa 0.591 / 0.540 →
  응력 0 꼬리 끝 **≈0.56 / ≈0.505**.  Fig 4(b) 기공 2000 MPa **4.4 / 3.3 %** → 제하 1000 MPa 5.6 / 4.4 → 100 MPa 8.4 / 6.9 →
  20 MPa 10.4 / 9.2 → P ≈ 0 끝 **17.2 / 16.9 %**.
- 되돌아옴은 **낮은 압력 끝에 몰린다**: 2000 → 100 MPa 동안 기공 +4.0 / +3.6 %p, 100 → 0 MPa 동안 +8.8 / +10.0 %p [카드 산술].
  ⚠ 마지막 수직 구간 (Fine 12.1 → 16.9 %) 은 압력 0–5 MPa (화소 한 칸) 안 = Fig 4(a) 의 응력 0 꼬리 — 펀치가 압분체에서
  떨어진 뒤의 펀치 이동이 섞였을 수 있다 [카드 추론 — 원문 언급 없음].  저자 판독 규약 (5 MPa 문턱, p.6) 은 그 구간 아래
  끝에서 읽는다.
- 그림: Fig 4(e)(f) 제하 단면에서 입자 사이 틈이 벌어진다 [판독] · 단면 그림 높이 가압 → 제하 **×1.10 (Coarse) · ×1.09 (Fine)**
  [판독 — 같은 너비 화소로 잰 그림 높이; 두 장면이 어느 시점인지는 인쇄 없음].  제하 장면에도 응력 색이 남는다 (잔류 응력 —
  값 [미확인]).

**(아) 검증 — 같은 그룹의 실험 · ABAQUS 와**
- 인쇄 (p.6): Coarse 2000 MPa 실험 **83.3 %** · 계산 **85.4 %** (*"The roughly 2.5 % variance"*) · Fine *"both experimental and
  simulation results around 87 %"* · 초록 *"maximum relative density deviation of only 2.5 %"* (= 상대 2.5 % = 2.1 %p [카드 산술]) ·
  문헌 편차 0.5–4 % [8,13,14,20,32].
- 그림 [판독 ±0.3 %p]: Coarse (Fig 4h 범례) 계산 − 실험 = **−1.2 · +0.4 · +0.9 · +2.3 · +2.1 %p** (1400 · 1500 · 1600 · 1800 ·
  2000 MPa) · OpenRadioss − ABAQUS = +1.3 · +1.5 · +1.7 · +2.2 · +1.3 %p · Fine (Fig 4g 범례) |OpenRadioss − ABAQUS| ≤ 0.4 %p.
- 비교 규약: 제하 뒤 · 5 MPa 문턱의 RVE 부피 · 고체 부피 = 처음 구 부피 합 (p.6).  시드 · 반복 런 · 오차 막대 없음.
  실험 · ABAQUS 모두 같은 그룹 [15,16] (§2).

**(자) 계산 비용**
- Table 1 (MPFEM 단계 벽시계 · Fine): RVE 210 / 250 / 300 µm = 569 / 874 / 1033 입자 = **9 / 16 / 24 h** — CPU 수 미인쇄.
- Table 3 (Coarse · 2000 MPa · **24 CPU**): ABAQUS **5 h** · PyCompact **7 h**.
- 메시 시험 (p.5–6 의 Coarse 문단): 2500 요소/입자 **36 h** · 2000 요소/입자 **9 h** — CPU 수 미인쇄.  ⚠ 같은 'Coarse · 2000
  요소' 가 Table 3 에서는 7 h (24 CPU) — 조건 차이 [미확인].
- DEM 단계 비용 · 입자 수 외 DEM 설정 (시간 간격 · 단계 수): [미확인].

**(차) 저자가 적은 한계** (원문 그대로)
- *"achieving accurate data transfer between DEM and MPFEM stages can be challenging, and large-scale simulations remain computationally
  demanding"* (p.2).
- *"the key limitation of LS-PrePost is that it does not allow assigning material properties to all particles simultaneously"* ·
  *"After several trial-and-error iterations"* · 다이 · 펀치 · 접촉 · 재료 · 경계는 *"completed manually"* (p.3).
- 편차 원인 *"mesh resolution, variations in PSD packing, differences in friction algorithms, effects at the boundaries of the RVE, and
  minor discrepancies in explicit solvers between OpenRadioss and ABAQUS"* + *"assuming perfectly spherical particles slightly reduces
  densification compared to real irregular powders"* (p.6).
- *"Although this study focused on two unimodal powders and small RVEs …"* (p.6) · *"Despite the computational cost of DEM–MPFEM
  simulations due to explicit time-stepping and contact resolution [13,14,31] …"* (p.6).

**[미확인] — 넘겨받는 과정에서 원문에 없는 것**: ① 넘긴 순간의 DEM 충전율 · 층 높이 · 겹침 크기 · 침강 정지 판정
② 겹친 구 · 틈 처리와 초기 상호침투 검사 ③ 재평형 · 초기 응력 · FE 단계 중력 ④ 펀치 속도 · 시간 간격 · 질량 스케일링 ·
감쇠 · 준정적 판정 ⑤ DEM 영률 · ν · 밀도 · 시간 간격 (템플릿 파일) ⑥ 메시 매개변수 값 ⑦ 1400–1800 MPa 점을 얻은 방법
⑧ 압력의 면적 정의 · 충격량 미분 평활 ⑨ 코드 저장소 (`https://github.com/plaslab-kimjh/PyCompact` · v1.0 · MIT) 안의
구성 — 원문은 파일 이름 (`InputGen.ipynb` · `MeshMatGen.ipynb` · `sample.txt` · `PSD.xlsx` · `position.csv` · `material.k` ·
cfile) 만 적고, 재현 캡슐 (C3) · 개발자 문서 (C8) 는 N/A.

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

**(f) 역할 나눔 한 줄 + DEM 의 장점 (2026-11-11 보강 · p.2 · `txt_p2_dem_fem_limits_and_mpfem_role.png`)**
> *"**The DEM captures the initial particle interactions and packing behaviour, while the MPFEM extends traditional FEM to
> explicitly mesh and simulate the deformation of individual particles** [13,14]."*
> *"DEM models the powder as an assembly of discrete particles, capturing microscopic interactions like particle rearrangement,
> contact forces, and granular flow. Advantages of DEM include detailed insights into particle-level kinematics, the ability to
> simulate realistic PSDs and friction effects using contact laws, and applicability to processes involving flow and initial
> packing [11]."*

(a)–(f) 의 원문 단 전체 = 그림 폴더 `txt_p2_dem_fem_limits_and_mpfem_role.png` (p.2 왼쪽 단) · (e) = `txt_p6_relative_density_readout_deviation_limits.png`.

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
4. **대변형 고밀도 영역의 상대밀도** — 하중 중 RD ≈95.6 % (Coarse) · ≈96.7 % (Fine) @2000 MPa 까지 (`digitized` Fig 4b
   기공 4.4 / 3.3 %; 강체 구로는 불가).
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
| 재료 값이 있는 자리 | 사용자 템플릿 `sample.txt` — *"definitions of material properties, units, boundary conditions, contact models, simulation domain, and timestep settings, which the user customizes"* · atom type · density 는 InputGen.ipynb 에서 사용자 지정 (Fig 2b 'Determine atom_type & density') | stated (p.3 · 2026-11-11 보강) |
| 시드 규칙 | 템플릿의 pdd 시드를 찾아 (Fig 2b 'Compute the largest seed number from pdd') 크기 클래스마다 새 소수 시드 | stated (p.3 · Fig 2b) |

★★ **질문 5 에 대한 정직한 답: "실제 E 를 썼는가, 낮췄는가" 는 이 논문으로 알 수 없다.**
템플릿 파일이 "재료물성"을 담고 "사용자가 커스터마이즈"한다고만 적혀 있고, 유일하게 명시된
E=170 GPa 는 **MPFEM 재료절(§3)** 의 값이다.  ⇒ `n/a`.
그런데 **이 논문에서는 그게 거의 중요하지 않다** — DEM 이 최종 밀도에 기여하는 것은 초기 패킹 하나뿐이고,
압축은 전부 MPFEM 이 다시 푼다.  ⇒ **PyCompact 는 DEM 강성에 둔감하고, 우리는 민감하다**
(우리 E_eff 1.35 는 최종 porosity 를 직접 정한다).  이 비대칭 자체가 §15 판정의 재료다.

### 7.2 MPFEM 단계 (OpenRadioss r2024)
| 항목 | PyCompact | ABAQUS 참조 [15,16] |
|---|---|---|
| 솔버 | **Explicit** | Explicit (Table 2 의 이 칸은 **비어 있다** · p.6 *"explicit solvers between OpenRadioss and ABAQUS"* 로 읽음) |
| 입자 요소 | **/TETRA4** (4절점 사면체, LS-PrePost 생성) | **C3D4** (선형 tet) |
| 다이·펀치 | **/SHELL** (강체 tooling) | **R3D4** (강체) |
| 접촉 | **General contact /TYPE26** (penalty, surface-to-surface) | General contact |
| 마찰 | **Coulomb µ = 0.2** (입자-입자) | 0.2 (Table 2 의 이 칸도 **비어 있다** · *"follows the same geometric, material, and loading definitions"* (p.6) 로 같다고 읽음 [카드 추론]) |
| 재료 | `*MAT_PIECEWISE_LINEAR_PLASTICITY` + Swift 데이터 | 동일 물성 |
| 요소/입자 | **평균 2000** (수렴시험 500–2500) | 명시 없음 |
| BC | 다이 **완전구속**, 펀치 **prescribed motion rigid** → 목표압 → 제하 | 동일 |
| 주기경계 | ⛔ **없음** [카드 추론 — 주기 경계 문장이 없고 옆면 = 강체 다이 (p.5 · Fig 3d) = walled RVE].  저자도 "effects at the boundaries of the RVE" 를 오차원으로 든다 | — |
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
| 소성 표현 | **★ 진짜 SHAPE 소성** — 입자마다 FE 메시 + piecewise-linear plasticity (Swift 데이터).  δ-겹침 프록시 **아님**.  (원문은 모델 이름 *PIECEWISE_LINEAR_PLASTICITY* 만 적는다 — 'J2' · 'von Mises 항복' 이라는 말은 없다; 옛 표기 'J2형' 은 카드 해석 · 2026-11-11 정정) |
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
  - ⚠ 본문 근거 *"The fine powder shows reaching a lower final porosity **due to its denser packing**"* (p.6) —
    ~~Fig 4(b) 의 초기 porosity 는 Fine 이 더 높다 (43 % + 스파이크 61 % vs Coarse 41.5 %) = Fine 이 더 성기게 쌓였다~~
    **⛔ 2026-11-11 철회** (재판독 `digitized.csv`): 압력이 뜨기 시작하는 점의 기공은 Fine **42.8** · Coarse **42.4 %** —
    차 0.4 %p = 화소 두 칸 = 판독 오차 안이라 '더 성기게' 를 말할 수 없다.  61 % 는 **P ≈ 0 수직 구간의 위 끝** (Fine 의
    빨간 선만 보이고 Coarse 선은 그 밑에 가렸을 수 있다) 이고, Fig 4(a) 의 응력 0 구간 (펀치가 층에 닿기 전 · Fine 0.287 까지)
    과 같은 구간이라 충전 상태가 아니다 [카드 추론].  ⇒ 그림은 '초기 충전이 더 조밀' 을 지지하지도 반박하지도 않는다
    ('denser packing' 이 압축 뒤의 충전을 뜻하는지도 원문으로는 가를 수 없다).  기전 설명으로는 그들이 다른 문단에서 쓴
    **접촉 네트워크 균질성** (p.6) 이 그림 (Fig 4c–f) 과 맞는다.

---

## 9. 결과 — 섹션별 상세

### 9.1 Fig 3(e) 메시 수렴 — **그림과 본문 숫자가 다르다 · 선택은 비용이 했다** (2026-11-11 고쳐 씀)
- 95 % 상대밀도에서의 축응력 (Coarse): 500 el → **1650**, 2500 el → **1310 MPa** (stated, p.6) = −20.6 %.
- 그림의 다섯 점 `digitized` (표지 무게중심 · 1 화소 = 4.8 MPa · 두 판독 일치): 500 ≈**1641** · 1000 ≈**1529** ·
  1500 ≈**1469** · 2000 ≈**1398** · 2500 ≈**1379** → 단계 증분 −6.8 · −3.9 · −4.8 · **−1.4 %** = 마지막 단계가 평탄해진다.
- ⚠ **2500 점이 그림 ≈1379 ↔ 본문 1310** (≈70 MPa · 화소 14 칸) — 원문 안 불일치.  본문 숫자를 믿으면 2000 → 2500 이
  −6.3 % (평탄화 없음), 그림을 믿으면 −1.4 % (평탄화) — **어느 쪽인지 원문으로 못 가른다 [미확인]**.
- ~~2000→2500 이 −5 % 이고 기울기가 죽지 않는다 · 수렴하지 않았다~~ **⛔ 철회** — 옛 판독 (2000 ≈1375) 과 본문 2500 값 (1310)
  을 섞은 산술이었다.  그림만 보면 저자의 *"indicating convergence, beyond which further refinement produced no significant
  change"* 와 모순되지 않는다.
- 실제 선택 이유는 바로 다음 문장에 있다: *"the runtime for the case with 2500 elements per particle
  was **36 h**, whereas it was **9 h** for the case with 2000 elements.  Therefore, an average of 2000
  elements per particle was selected"*.  ⇒ **비용이 정한 메시** (이 문장은 그대로 선다).
- ⚠ 그리고 **요소 25 % 증가에 런타임 4배**는 설명되지 않는다 (explicit dt ∝ 최소 변길이로 따지면
  `derived(ours)` ≈1.35배가 상한).  논문에 원인 서술 없음.
- ~~우리 CL-41 과 같은 병 · 같은 상황에서 라벨이 다르다~~ **⛔ 철회** — 위 '미수렴' 판정이 무너졌으므로 거울 비유도 내린다.
  남는 교훈은 **보고 방식** 하나: 수렴 판정을 적을 때 그림 점과 본문 숫자가 같아야 하고, 마지막 증분을 숫자로 함께 적는다.

### 9.2 Fig 3(f) 마찰 — RD 를 올리는 노브가 **제하(springback) 쪽**에 있다
- µ 0.1 → 0.2 → 0.3 에서 RD **84.2 → 85.5 → 85.9 %** (`digitized` 2026-11-11; 옛 판독 0.3 ≈86.0), µ≥0.2 에서 완만.
- 저자 기전: *"raised relative density …, plateauing beyond µ = 0.2 **due to reduced sliding and
  elastic recovery**"* — 즉 **마찰이 제하 시 되돌아감을 잠근다**.
- ⚠ *"µ = 0.2 was selected for best experimental agreement."* 그런데 Coarse 실험은 **83.3 %** 이고
  `digitized` 로 µ=0.1 이 **84.2**, µ=0.2 가 **85.5** (본문 계산값 85.4) 다 ⇒ **Coarse 만 보면 µ=0.1 이 더 가깝다.**
  선택 기준(두 분말 동시? 다른 지표?)이 정량적으로 서술되지 않았다.
  ⇒ **마찰은 사실상 1개의 보정 노브**이고 헤드라인 2.5 % 는 그 노브를 지난 값이다.
- ⚠ **DEM µ_s = 0.5 ≠ MPFEM µ = 0.2** — 같은 분말인데 두 단계의 마찰이 다르다 (논문 설명 없음).

### 9.3 Fig 3(g) RVE — 역시 단조 상승, 가장 작은 것을 채택
- 210 → 250 → 300 µm 에서 RD **86.9 → 87.0 → 87.5 %** (`digitized` 2026-11-11; 옛 판독 87.1 · 87.4), 실험선 ≈87.8.
- 즉 **RVE 를 키울수록 실험에 가까워진다** = 보고된 편차에 **부호 아는 RVE 편향**이 남아 있다.
- 선택 근거(stated): "representativeness, experimental match, consistency with prior studies [15,16],
  and **computational efficiency**" — Table 1 이 그 비용이다 (9 / 16 / 24 h).

### 9.4 Fig 4(a) 응력–변형 (Coarse/Fine, 2000 MPa)
- 3단계 서사(stated): **① 입자 재배열**(응력 거의 0) → **② 변형에 의한 치밀화**(급상승) →
  **③ 부분 탄성회복**(제하 급강하) + **잔류변형 = 영구 치밀화**.
- `digitized` (2026-11-11 재판독 · 1 화소 = 0.0014 변형률 = 7.3 MPa · Coarse / Fine): 응력 개시 ε ≈ **0.371 / 0.287**;
  정점 ε ≈ **0.622 / 0.576** @2000 MPa; 제하 가지 100 MPa **0.603 / 0.559** → 20 MPa **0.591 / 0.540** → 응력 0 행 위의
  꼬리 끝 **≈0.56 / ≈0.505** (Fine 빨간 꼬리 0.505–0.532 · Coarse 검은 꼬리 0.561–0.572, 축선과 같은 색이라 ±0.01).
  ⇒ **Δε (정점 → 꼬리 끝) ≈ 0.062 / 0.071** · 그 절반이 20 MPa 아래에서 난다 (0.031 / 0.035) [카드 산술].
  압축 높이 (1 − ε_정점) 대비 회복률 `derived(ours)`: 20 MPa 까지 **8.2 % / 8.5 %** · 꼬리 끝까지 **16.4 % / 16.7 %**.
  ~~제하 후 잔류 ε ≈ 0.598 / 0.556 ⇒ Δε ≈ 0.024 / 0.020 (6.3 % / 4.7 %)~~ **⛔ 옛 판독 철회** — 제하 가지가 응력 0 에 닿기
  전 (≈20–50 MPa) 의 값이었고, 축선 위로 이어지는 꼬리를 놓쳤다.
- ⚠ 꼬리 (응력 0 인데 변형률이 줄어드는 구간) 는 펀치가 압분체에서 떨어진 뒤의 펀치 이동일 수 있다 — 원문은 이 구간을
  말하지 않는다 [카드 추론].  Fig 4(b) 의 P ≈ 0 수직 구간과 같은 구간이다 (§10).
- ⚠ **개시 변형이 다르다**(0.371 vs 0.287) = 펀치가 층에 닿기 전 빈 공간을 내려온 거리가 다르다는 뜻이다 (Fig 4b 의 P ≈ 0
  수직 구간과 같은 구간 [카드 추론]).  변형의 정규화 길이 (펀치 출발 높이인지 층 높이인지) 가 **미기재**다 → 절대 변형값 해석
  불가 (차이 · 비율만 쓴다).

### 9.5 Fig 4(b) porosity–pressure 루프 ★ 형식을 훔칠 그림
- ⚠ **압력 축 등록**: 눈금 0 · 1500 · 2000 · 2500 MPa 가 원본 화소 x 869 · 1145.5 · 1237.5 · 1329 에 있고 틀 왼끝은
  x 831.5 (= **−204 MPa**) 다 — **0 눈금은 틀 왼끝이 아니다** (2026-11-11 눈금 표시 화소로 확인).
- `digitized` 하중분지 (2026-11-11 · Coarse / Fine): 압력이 뜨는 점 **42.4 / 42.8 %** → 500 MPa **27.0 / 24.7** →
  1000 **15.6 / 13.7** → 1500 **8.5 / 7.0** → **2000 4.4 / 3.3 %**.  P ≈ 0 의 수직 구간 (Fine 60.9 → 42.8 %) 은 펀치가 층에
  닿기 전 구간 (§8 · §9.4).
- `digitized` 제하분지: 1000 MPa **5.6 / 4.4** → 500 **6.5 / 5.2** → 100 **8.4 / 6.9** → 20 **10.4 / 9.2** →
  P ≈ 0 수직 구간 끝 **17.2 / 16.9 %** (Fine 수직 구간 = 12.1 → 16.9 %, 압력 0–5 MPa 한 화소 안).
- ~~하중분지 500 MPa ≈33/31 → 1000 ≈22/20 → 1500 ≈12/10.5~~ **⛔ 옛 판독 철회** — 2026-11-11 의 두 판독 (눈금 화소로
  등록 · 서로 일치) 보다 4–7 %p 높다.  원인 [미확인] — 압력 0 을 틀 왼끝으로 잡으면 '500' 자리가 실제 ≈340 MPa 가 되어
  일부만 설명된다.
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
- 단면 그림 높이 (원본 화소 · 2026-11-11 판독): Coarse 가압 179 → 제하 197 px (**×1.10**) · Fine 196 → 214 px (**×1.09**) —
  너비는 471 / 469–470 px 로 같아 같은 배율로 읽힌다.  두 장면이 어느 하중 시점인지는 인쇄 없음.  ⚠ 너비를 RVE 가로 변으로
  놓고 잰 제하 단면 높이는 Coarse ≈418 µm (라벨 445) · Fine ≈96 µm (라벨 120) — Fine 이 25 % 어긋나 단면이 RVE 전폭인지
  [미확인] [카드 산술].

### 9.7 Fig 4(g)(h) 실험·ABAQUS 대조 — ⚠ **패널 라벨이 뒤집혀 있다**
- **그림 범례**: (g) = **Fine**-EXP/OpenRadioss/ABAQUS, (h) = **Coarse**-….
- **캡션·본문**: "(g) Coarse powders and (h) Fine powders", *"As shown in Fig. 4(h), for the fine
  particles…"*.  ⇒ **정반대**.
- 값으로 판정하면 **범례가 맞다**: 본문이 말한 Coarse 83.3(exp)/85.4(sim) 짝은 **범례가 Coarse 인
  (h)** 에서 읽힌다.  ⇒ **캡션·본문 쪽 패널 문자가 오기**.  인용 시 (g)/(h) 를 바꿔 쓸 것.
- `digitized` (h)=Coarse (2026-11-11 · ±0.3 %p · 1400 / 1500 / 1600 / 1800 / 2000 MPa): exp 83.3 / 82.7 / 83.1 / 82.7 / 83.3 ·
  OR 82.1 / 83.1 / 84.0 / 85.0 / **85.4** · ABQ **80.8** / 81.6 / 82.3 / 82.8 / 84.1.  (옛 판독: OR 1400 82.5 · 2000 85.3 · ABQ 2000 83.6)
- `digitized` (g)=Fine: exp 83.9 / 83.5 / 83.9 / 87.6 / 87.8 · OR 82.9 / 83.9 / 84.7 / 86.5 / 87.0 · ABQ 83.2 / 84.2 / 84.8 / 86.1 / 87.2
  (셋이 2000 MPa 에서 0.8 %p 안).  (옛 판독 2000 ≈87.4 / 87.0 / 86.9)
- ★ **정직한 읽기**: 2000 MPa Coarse 에서는 **ABAQUS(84.1)가 실험(83.3)에 더 가깝고 OpenRadioss(85.4)가
  더 멀다**.  반대로 1400 MPa 에서는 ABAQUS 가 −2.5 %p 로 더 멀다.  ⇒ *"matching ABAQUS predictions"*
  는 **점대점 일치가 아니라 오차 크기가 비슷하다**는 뜻으로만 방어된다 (두 솔버 격차 `digitized`
  Coarse **1.3–2.2 %p** · Fine **≤ 0.4 %p**; 옛 표기 0.8–2.5 %p).

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
| 도달 RD (제하 후 · 5 MPa 규약) | **85.4 %** (Coarse) · **≈87 %** (Fine) = porosity **≈13–15 %** (stated) · P ≈ 0 끝은 ≈17 % `digitized` | pure-SE **90 %**(φ 10 % — ⛔ 외부 앵커 아님: 출처 철회 stoic-knuth 원장 `CL-94` · 우리 MPM 보정 수렴값), real_14 **84.4 %**(15.6 %) |
| 도달 RD (하중 중) | **95.6 / 96.7 %** = porosity **4.4 / 3.3 %** `digitized` (Coarse / Fine) | — (우리는 제하를 안 푼다) |
⇒ **제하 후 기준으로 그들은 RD 0.90 에 도달하지 못한다** — 우리 press 의 **6.7배 압력**에서도.
저자의 설명은 **완전 구 가정**(불규칙 실분말보다 덜 치밀해짐)이다.
★ 우리 쪽 함의: **"강체 구 floor ~20 %"** 대비 **형상 소성이 있으면 하중 중 3–4 %까지 내려간다** —
소성이 강체 구 floor 를 깬다는 우리 주장의 **독립 방향지지**.  단 **제하하면 5 MPa 규약 13–15 % (P ≈ 0 끝 ≈17 %) 로
되돌아온다** = 형상 소성이 사는 자리는 "하중 중"이고, 보고값은 **제하 규약에 강하게 의존**한다.

**⚠⚠ 판독 규약이 near-vertical 구간 위에 있다 (내가 잡은 가장 큰 기술적 취약점)**
- stated: *"a designated pressure level of **5 MPa** was established as the threshold for determining the
  volume of the compacted powders in the unloading phase."*
- 그런데 Fig 4(b) 제하분지는 **P→0 에서 수직**이다 (20 MPa 10.4 / 9.2 % → P ≈ 0 끝 17.2 / 16.9 %, `digitized`).
  5 MPa 는 원본 화소 **한 칸** (1 px = 5.4 MPa) — 그림에서 읽는 것이 원리적으로 불가능하고,
  **판독값이 문턱 선택에 매우 민감**하다 (Fine 은 0–5 MPa 한 칸 안에서 12.1 → 16.9 %).
- ~~닫히지 않는 삼각형 (≈5–7 %p 벌어진다 · 헤드라인 편차보다 크다)~~ **⛔ 2026-11-11 철회 — 삼각형은 닫힌다.**
  옛 판정은 Fig 4(a) 제하 가지의 20–50 MPa 근처 값 (0.598) 을 '잔류' 로 읽고 축선 위 꼬리를 놓친 옛 판독에서 나왔다.
  같은 펀치 위치 부피로 두 그림을 맞대면 [카드 산술 — RD = RD_정점 × (1 − ε_정점)/(1 − ε) · 고체 부피 일정 (p.6)]:

| 경로 | Coarse | Fine |
|---|---|---|
| Fig 4(b) 2000 MPa 기공 → RD_정점 | 4.4 % → 95.6 % | 3.3 % → 96.7 % |
| Fig 4(a) 20 MPa ε → RD | 0.591 → **88.4 %** (기공 11.6) | 0.540 → **89.1 %** (10.9) |
| Fig 4(b) 20 MPa 기공 | 10.4 % (RD 89.6) | 9.2 % (RD 90.8) |
| Fig 4(a) 꼬리 끝 ε → RD | 0.56 → **82.1 %** (기공 17.9) | 0.505 → **82.8 %** (17.2) |
| Fig 4(b) P ≈ 0 끝 기공 | 17.2 % (RD 82.8) | 16.9 % (RD 83.1) |
| 본문 5 MPa 규약 (stated) | **85.4 %** | **≈87 %** |

  ⇒ 두 그림은 꼬리 끝에서 0.3–0.7 %p · 20 MPa 에서 1.2–1.7 %p 안에서 맞고 (20 MPa 행은 화소 한 칸 = 7 MPa 의 등록 오차가
  크다), 본문 5 MPa 값은 20 MPa 와 꼬리 끝 사이 가파른 발끝에 놓인다 = **세 경로가 서로 맞다**.
- ⚠ 남는 질문 하나: 꼬리 (응력 0 인데 부피가 커지는 구간 · Fine 기공 12.1 → 16.9 %) 에서 펀치가 압분체에 닿아 있는지 원문은
  말하지 않는다 → 그 구간은 압분체 되돌아옴이 아니라 **떨어진 펀치의 이동**일 수 있다 [카드 추론].  저자의 5 MPa 규약은 그
  구간을 피하는 정의로 읽힌다.  ⇒ 이 논문의 '제하 끝 ≈17 %' 를 압분체의 자유 상태 기공으로 인용하지 않는다.
- ⇒ **인용 규율**: PyCompact 의 RD 절대값을 우리 표에 넣을 때는 반드시
  *"제하 후·5 MPa 규약·구 가정"* 을 함께 적는다.  하중 중 값(3–4 % porosity)과 섞지 않는다.

---

## 11. 계산비용·확장성 (질문 8) + 저자 명시 한계

**실측 비용 (stated)**
| 케이스 | 입자수 | 시간 | 비고 |
|---|---|---|---|
| RVE 210 µm (Fine) | **569** | **9 h** | 2000 el/입자 ⇒ `derived(ours)` **≈1.14 M 요소** |
| RVE 250 µm | 874 | 16 h | |
| RVE 300 µm | 1033 | 24 h | |
| Coarse 2000 MPa, **24 CPU** | 403 | **ABAQUS 5 h / PyCompact 7 h** | Table 3 |
| 메시 시험 2500 el/입자 · 2000 el/입자 | 403 (Coarse 문단) | **36 h · 9 h** | p.6 · CPU 수 미인쇄.  2026-11-11 정정: 옛 칸 '569' — 메시 시험은 *"examined for a coarse powder"* (p.5) 문단이다.  ⚠ 같은 'Coarse · 2000 el' 이 Table 3 에서는 7 h (24 CPU) — 조건 차이 [미확인] |

**스케일링** `derived(ours)`: 569→874 는 지수 **1.34**, 874→1033 은 지수 **2.43** (입자수 대비 초선형).
⇒ 접촉쌍 증가로 초선형이 되는 전형.

**★ 우리 침대에 적용하면 (판정 (b)의 결정적 근거)** `derived(ours)`, 자릿수 전용:
- 우리 real_14 = **SE 32,832 개** (+AM 457).  569 대비 **57.7배**.
- 입자수만으로: 지수 1.0 → **519 h(22일)** · 1.33 → **1,980 h(82일)** · 1.5 → **3,945 h(164일)** (24 CPU — ⚠ Table 1 의
  9 h 에는 CPU 수가 인쇄되지 않았다; 24 CPU 는 Table 3 의 Coarse 런 값이라 같다고 놓은 산술 · 2026-11-11 표지).
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
  reproducibility"* 라고 적고 Fig. 2a 에도 **"Ls-PrePost [optional]"** 로 표기.
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

> 파일 = `litdb/figures/pycompact2025_dem_mpfem_workflow/` (2026-11-11 · 37 장 · `figures.json` indent 1).  그림 4 장은 PDF 에 박힌
> 300 dpi 래스터라 **원본 화소 그대로** 잘랐다 (재렌더 없음 · 사방 6 pt 흰 여백 · 캡션 글자는 그림 밖 = `figures.json` 의 caption ·
> 도구 관례).  Fig 4 는 그림이 p.7 · 캡션이 p.8 에 있어 도구가 건너뛰었다 → 손 크롭 (`manual_crop`).  표 · 식 · 근거 문단은 벡터
> 글자를 400 dpi 로 렌더 (6.4–7.5 pt 글자 때문에 도구 기본 300 dpi 보다 올림) · 줄 사이 흰 틈에 띠 경계.  판독 원자료 =
> `digitized.csv` (Fig 3a · 3e · 3f · 3g · 4a · 4b · 4e · 4f · 4g · 4h).  ⚠ 원문 안의 표기 어긋남: Fig 4(g)(h) 패널 문자 (§9.7) ·
> Fig 4(a) 캡션은 Coarse 만 적지만 그림은 Coarse · Fine 두 곡선 · Fig 3(e) 2500 점 ↔ 본문 1310 MPa (§9.1).

| Fig | 쪽 | 파일 | 원 캡션 요지 | 우리가 쓸 것 |
|---|---|---|---|---|
| **1** | p.2 | `fig_1.png` | DEM / MPFEM 두 상자와 단계별 도구 (FreeCAD · LIGGGHTS · ParaView ‖ python · LS-PrePost · OpenRadioss · ParaView) | ★ 화살표 라벨 **"Initial powder configuration (size, center)"** = 인계물 정의 인용구 |
| **2** | p.4 | `fig_2.png` | 자료 흐름 (a) + InputGen 순서도 (b) + MeshMatGen 순서도 (c) | 넘겨받는 과정의 그림 근거 한 장 (§4.7) |
| **2a** | p.4 | `fig_2a.png` | 전체 데이터흐름 (STL·VTK·**CSV(x,y,z,r)**·cfile/.k·.rad) | ★★ 우리 scaffold 파이프라인 그림과 **1:1 대응** — 발표 슬라이드 비교도 재료 |
| **2b** | p.4 | `fig_2b.png` | `InputGen.ipynb` 플로차트 (template→PSD→atom_type & density→pdd 최대 시드→소수 시드→pts/pdd) | PSD→DEM 입력 자동화 패턴 |
| **2c** | p.4 | `fig_2c.png` | `MeshMatGen.ipynb` 플로차트 (position.csv→unit_scale · mesh_dens · mesh_edge_size→구 생성→tet 메시→surface/part set ‖ pid = secid = i · mid = 1) | ★ 인계 변환기의 실제 알고리즘 |
| **3** | p.5 | `fig_3.png` | (a) PSD · (b) 금형 모식 · (c) DEM 침강 뒤 · (d) MPFEM 모형 · (e)(f)(g) 민감도 | 패널별 아래 |
| **3a** | p.5 | `fig_3a.png` | 두 분말 PSD (weight fraction vs 로그 **지름**) | `digitized` Fine 봉우리 ⌀≈38 · Coarse ⌀≈122 µm (본문 평균과의 불일치 근거) |
| **3b** | p.5 | `fig_3b.png` | 다이 압축 모식 (펀치/다이/압분체) — 실험 [15,16] | 우리 플래튼 그림의 표준형 |
| **3c** | p.5 | `fig_3c.png` | DEM 침강 후 3D (Coarse 1000 µm / Fine 210 µm · 가로 두 변 화살표) | 인계 시점의 상태 = **압축 전** |
| **3d** | p.5 | `fig_3d.png` | MPFEM 모델 (펀치 · 다이 셸 메시 · tet 메시 입자 + 단일 구 확대) | ★ "입자당 FE 메시" 가 무엇인지 보여주는 한 장 |
| **3e** | p.5 | `fig_3e.png` | 요소/입자 → 95 % 밀도 축응력 (500–2500 · Coarse) | ⚠ 그림 2500 점 ≈1379 ↔ 본문 1310 · 마지막 증분 −1.4 % (그림) — 보고 방식의 반면교사 (§9.1) |
| **3f** | p.5 | `fig_3f.png` | µ → RD (0.1/0.2/0.3 · Coarse · 2000 MPa) | 마찰이 **springback 잠금**으로 RD 를 올린다 |
| **3g** | p.5 | `fig_3g.png` | RVE → RD (210/250/300 µm · Fine) + EXP 선 | RVE 편향의 부호 |
| **4** | p.7 (캡션 p.8) | `fig_4.png` | (a) 응력–변형 · (b) 기공–압력 · (c)(d) von Mises · (e)(f) PEEQ 단면 · (g)(h) RD–압력 | 패널별 아래 |
| **4a** | p.7 | `fig_4a.png` | 하중–제하 응력–변형 (Coarse/Fine · 캡션은 Coarse 만 적음) | 3단계 서사 + 응력 0 꼬리 · Δε `digitized` (§9.4) |
| **4b** | p.7 | `fig_4b.png` | **porosity–pressure 하중+제하 루프** (압력축 0 은 틀 왼끝이 아님) | ★★ **그림 형식을 훔칠 것** (우리는 점만 본다) |
| **4c/4d** | p.7 | `fig_4_c-d.png` | von Mises 4프레임 (초기→하중→최대→제하), Coarse/Fine · 눈금 0–1.5e+03 MPa | 접촉 국소집중 vs 균질 전달 · 'Initial stage' = 넘긴 직후 무응력 색 |
| **4e/4f** | p.7 | `fig_4_e-f.png` | **PEEQ 단면** (하중/제하), 445 µm / 120 µm · 눈금 0–1.3 | ★★ **core-preserved + boundary-flattening** = 우리 MPM morphology 와 같은 무늬 · 제하 시 **접촉 틈 벌어짐** |
| **4g/4h** | p.7 | `fig_4g.png` · `fig_4h.png` | RD vs P (exp/OpenRadioss/ABAQUS), 1400–2000 MPa · 범례 (g) Fine · (h) Coarse | ⚠ **패널 문자 뒤집힘**(§9.7) · 두 솔버 격차 Coarse 1.3–2.2 · Fine ≤ 0.4 %p |

**표 그림**: `tab_1.png` (Table 1 · p.6 — RVE 210/250/300 µm · 569/874/1033 입자 · 9/16/24 h) · `tab_2.png` (Table 2 · p.6 —
PyCompact ↔ ABAQUS 설정; ABAQUS 칸의 Solver · Friction 빈칸 = 인쇄 그대로 · 도구가 '영역 없음' 으로 건너뛰어 손 크롭) ·
`tab_3.png` (Table 3 · p.8 — Coarse · 2000 MPa · 24 CPU · ABAQUS 5 h ↔ PyCompact 7 h) · `tab_code_metadata.png` (번호 없는 코드
메타데이터 표 C1–C9 · p.1).

**식 그림** (식 번호별): `eq_01_impulse_definition.png` (식 1 · p.3 — J_Fi(t) = ∫₀ᵗ F_i(τ)dτ) · `eq_02_force_from_impulse.png`
(식 2 · p.3 — F_i(t) = dJ_Fi/dt) · `eq_03_swift_hardening_law.png` (식 3 · p.5 — σ = K(ε + ε₀)ⁿ) · 식 1 · 2 와 앞뒤 문단 한 장
= `eq_01_02_in_text_reaction_force_readout.png` (p.3).  ⚠ 이 논문의 번호 붙은 식은 이 셋뿐이다 (지배 방정식 · 접촉 식 ·
요소 정식은 인쇄하지 않는다 — 풀이기 이름 · 키워드만).

**근거 문단 그림** (원문 단 그대로 · §4.7 의 인용 자리): `txt_p2_dem_fem_limits_and_mpfem_role.png` (p.2 왼 — FEM · DEM 한계 ·
MPFEM 역할) · `txt_p2_p3_handover_interface_csv.png` (p.2 오른 → p.3 — 두 단계 · 침강 · CSV 인계면) ·
`txt_p3_inputgen_template_psd_seed_generation.png` (p.3 왼 — 템플릿 · PSD · 소수 시드 · 2026-11-11 추가) ·
`txt_p3_dem_settings_and_dem_to_mpfem_conversion.png` (p.3 — DEM 접촉 값 · cm→mm · 구 재생성 · 벌칙 접촉 μ 0.2) ·
`txt_p3_material_k_assignment_keyword_roundtrip.png` (p.3 오른 — LS-PrePost 한계 · material.k · proj→k · 2026-11-11 추가) ·
`txt_p5_material_constants_and_fe_boundary_conditions.png` (p.5 — Swift 상수 · E · ν · ρ · 금형 · 펀치) ·
`txt_p6_mesh_friction_rve_choices_and_abaqus_reference.png` (p.6 왼 — 메시 · μ · RVE 선택 · ABAQUS 참조) ·
`txt_p6_compaction_stages_loading_unloading_mechanics.png` (p.6 — 세 단계 · 제하 탄성 회복 · 입자 주변 · 잔류 공극 · 2026-11-11 추가) ·
`txt_p6_relative_density_readout_deviation_limits.png` (p.6 오른 — 5 MPa 규약 · 편차 원인 · 한계).

---

## 14. Post-processing ★

- **반력 추출 (OpenRadioss 특유)**: 강체 시간이력에 **순간 반력이 저장되지 않고 임펄스**가 저장된다.
  `J_Fi(t) = ∫₀ᵗ F_i(τ)dτ` (eq 1) → **미분**해서 `F_i(t) = dJ_Fi/dt` (eq 2).
  ⚠ 수치미분은 잡음을 증폭하는데 **필터링/스무딩 언급이 없다**.  (2026-11-11 재판독: Fig 4(a) 의 제하 가지는 매끈하다 —
  옛 표기 '제하부의 계단 모양' 은 그림에서 보이지 않아 철회.)  ⇒ 우리 MPM `wallP`(경계 반력 직합)와 **판독 규약이 다르다** —
  비교 시 주의.
- **상대밀도**: `RD = Σ(초기 구 부피) / V_RVE(제하 중 5 MPa 시점)`.  RVE 부피는 **시뮬레이션 출력에서
  직접 측정**.  고체부피는 **압축 전 초기 구 부피 합**으로 근사 (탄소성 부피변화 무시 — 저자 근거 *"volumetric changes during
  elastic–plastic deformation is negligible [15,16]"* (p.6); 탄성 체적변형 `derived(ours)` P/K = 2000 MPa / 141.7 GPa ≈ **1.4 %**
  (K = E/(3(1−2ν)) · E 170 · ν 0.3) — 옛 표기 1.2 % 는 P/E (일축) 이었다 · 2026-11-11 정정).
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
| 실험 검증 | RD vs P (5점 × 2분말), **자기 그룹 데이터** | Minnmann porosity (⛔ 출처 철회 — stoic-knuth 원장 `CL-94` · 2026-11-11 표지), Cronau overlap, Bazzoun EIS 등 **외부** | 무승부(성격 다름) |
| 비용 | 569입자 **9 h** (Table 1 · CPU 수 미인쇄 — 24 CPU 는 Table 3 의 Coarse 7 h) (CPU explicit) | 침대 32k 입자 **시간 단위** (GPU MPM) | ★★ 우리가 **자릿수** 우위 |
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
1. ★★ **비용이 자릿수로 다르다** (§11): 569 입자 9 h (CPU 수 미인쇄 · 24 CPU 로 놓은 산술) vs 우리 32,832 SE 입자 GPU 시간 단위.
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
   ⚠ 단 **그림 점과 본문 숫자가 어긋난 채 "convergence" 라 적는 보고 방식은 훔치지 않는다** (Fig 3e 2500 점 ≈1379 ↔ 본문
   1310 · §9.1) — 우리는 마지막 증분을 숫자로 함께 적고, 미수렴이면 미수렴이라 쓴다.  (2026-11-11 고쳐 씀: 옛 줄은 그림이
   미수렴이라 보았는데 재판독으로는 그림이 평탄해진다.)
3. ★ **5 MPa 판독 문턱 규약**의 아이디어(제하 곡선 위 고정 기준점)는 좋은데, **near-vertical 구간에
   두면 안 된다**.  우리가 쓴다면 **평탄 구간에 문턱을 두고 민감도를 함께 보고**할 것.
4. ★ **소수(prime) 시드 규약** — 시드 충돌 방지의 값싼 규율.
5. ★ **OpenRadioss = 무료 explicit 대변형 FE** 라는 도구 정보 자체.  위 15.3 의 소형 REV 실험 경로.
6. ★ **임펄스→미분 반력 판독**(eq 1–2)은 **반면교사**: 판독 규약이 다르면 곡선 모양이 달라진다
   (우리 wallP vs σzz 논쟁과 같은 종류).

### 15.5 ★★ 이 논문이 건드린 **우리 공백** — 제하(springback)
- 그들은 제하를 풀고 **RD 를 제하 후에 잰다**.  우리는 **하중 중/정지 시점**의 porosity 를 보고한다.
- `derived(ours)` 재료의 탄성 체적 회복 = P/K (2026-11-11 정정: 옛 표는 그들 칸만 P/E 였다):

| 모델 | 값 |
|---|---|
| 그들 (2000 MPa · E 170 GPa · ν 0.3 ⇒ K 141.7 GPa) | **체적 1.4 %** (일축 P/E 는 1.2 %) |
| 우리 **DEM** (300 MPa / E_eff 1.35, ν 0.3 ⇒ K 1.125 GPa) | **체적 26.7 %** ⚠ |
| 우리 **MPM** (300 MPa / K 25.5 GPa, ν 0.49) | **체적 1.2 %** ✓ |

- ⇒ ★★ **우리 MPM 의 stiff-bulk(ν=0.49) 선택이 재료 탄성 회복 축에서 실재 금속분말과 같은 자릿수**에
  있고, **우리 DEM 의 18× 연화는 제하 축에서 비물리적**이다 (체적 회복이 26 %).
  우리는 제하를 안 풀기 때문에 **지금은 노출되지 않은 잠재 한계**다.
- ★ **그런데 압분체의 되돌아옴은 재료 P/K 보다 훨씬 크다** (2026-11-11 보강 · `derived(ours)`): 그들 Fig 4(b) 에서 2000 MPa →
  5 MPa 규약 자리까지 RVE 부피가 Coarse 0.956 / 0.854 − 1 ≈ **+12 %** · Fine 0.967 / 0.87 − 1 ≈ **+11 %** 커진다 (하중 중 RD
  `digitized` · 5 MPa RD stated) = 재료 탄성 체적 1.4 % 의 **≈8 배**.  저자 기전은 *"elastic recovery primarily at particle
  peripheries"* (p.6) 이고 Fig 4(e)(f) 제하 단면에 입자 사이 틈이 벌어진다 [판독] ⇒ 압분체 되돌아옴의 주역은 **접촉이 열리고
  입자 주변이 풀리는 것**이지 재료의 부피 탄성이 아니다 [카드 추론].  ⇒ 우리 MPM 의 K 가 맞아도 압분체 되돌아옴이 맞는다는
  보장은 없다 — 접촉이 열려야 한다 (비교 문서 C 절의 '단일 속도장 MPM 은 제하를 원리적으로 과소평가' 가설과 같은 방향).
  ⚠ **열린 질문**: 우리 실험 앵커(Minnmann pure-SE 10 %, Cronau overlap)가 **가압 중** 측정인지
  **해압 후** 측정인지 — 후자라면 우리 DEM porosity 를 해압 후 값과 맞춘 것이 되어 규약이 어긋난다.
  ⇒ **문헌 재확인 필요(미해결).**  이 카드가 그 질문을 만들었다.
  ⛔ 2026-11-11 표지: 'Minnmann pure-SE 10 %' 앵커는 출처가 철회됐다 (stoic-knuth 원장 `CL-94` — Minnmann 2021 에 그 값 없음).
  가압 중 ↔ 놓은 뒤 질문은 비교 문서 A 절의 `miss2026_insitu_conductivity_porosity_pressure_compaction` 항목이 이어받았다
  (순수 SE 300 MPa 가압 중 7.1–7.6 % · 다이 안 놓은 뒤 8.6 % · 재계산 · CL-94 의 후보 — 그 항목의 표지 그대로).

### 15.6 ★★★ 넘겨받는 과정 대조 표 — 이 논문 · 우리 지금 · 우리 계획 (2026-11-11 보강)

> 이 논문 칸 = §4.7 (원문 위치는 거기).  **우리 지금** = DEM 덤프 → MPM 골격 (가압이 끝난 DEM 덤프의 AM 자리를 고정 골격으로 ·
> SE 는 덤프 자리에 씨앗 → MPM 이 SE 만 다시 누름) — 이 카드 §4.6 · §11 · §15.1 과 정본 비교 문서 (`comparison_vs_ours_DEM.md`
> C · F 절) 에 적힌 것만.  **우리 계획** = 느슨한 충전부터 한 모델로 누르고 빼기 — 정독 지시서 3 절의 이름 (단계 4 = 3D 순수 SE
> 가루를 느슨하게 붓고 눌러 항복 세기 하나를 실험 기공에 맞춤 · 단계 5 = 3D 복합 (AM + SE) 누르기 · 단계 6 = 압력을 빼고 되돌아옴 ·
> 후보 A = MPM 에서 AM 을 움직이는 강체 + SE 한 속도장 · 후보 A′ = 입자마다 속도장 (다물체 마찰 접촉) · 후보 B = 입자마다 유한요소 +
> 접촉 = **이 논문의 꼴** · 조건 R1–R7).  어디에도 없으면 "카드 · 비교 문서에 없음".

| 항목 | 이 논문 (PyCompact) | 우리 지금 (DEM 덤프 → MPM 골격) | 우리 계획 (단계 4–6 · 후보 A · A′ · B) | 가져올 것 / 못 가져올 것 |
|---|---|---|---|---|
| (가) 무엇을 넘기나 | **(x, y, z, r) CSV 하나** (p.2 · Fig 2a) · ID 는 CSV 칸에 없고 FE 쪽 pid = i 로 다시 매김 · 접촉 · 겹침 · 속도 · 응력 · 재료 값은 넘어갈 칸이 없다 [카드 추론] · cm → mm ×10 | **(x, y, z, r)** — `real14_am_scaffold.csv` (AM 457) · `real14_se_scaffold.csv` (SE 32,832) · 상태변수 0 (§4.6 · §11) | 넘길 것 = 느슨한 출발 배치 · 무엇을 담을지 세부는 카드 · 비교 문서에 없음 | **가져올 것**: 넘김 = 중심 + 반지름 표 하나라는 최소 계약 · 단위 환산 칸 (`unit_scale`) · 입자 번호를 행 순서로 다시 매기는 방식.  **못 가져올 것**: 겹침 · 틈 처리가 없다 — 압밀이 끝난 덤프 (겹침 큼) 에는 그대로 못 쓴다 (§4.3) |
| (나) 언제 넘기나 | **중력 침강 뒤 · 가압 전 (P = 0)** (p.2 · Fig 3c) · 그 순간 충전율 [미확인] (FE 판독 ≈0.57–0.58) | **300 MPa 압밀이 끝난 뒤** (`atom_2060000`) → 씨앗이 정답을 담는다 (`solid_vol` 상수 · MPM 출력은 `wall_z` — 비교 문서 F 절) | **느슨한 충전 (가압 전)** = 이 논문과 **같은 시점** | **가져올 것**: ★ 계획의 넘김 시점이 이 논문과 같다 = '압밀 전에 넘기면 씨앗 순환이 없다' (비교 문서 F 절 MPFEM ①) 의 실례.  **못 가져올 것**: 넘긴 순간의 충전율 · 층 높이를 인쇄하지 않아 단계 4 의 출발 기준 숫자로는 못 쓴다 |
| (다) 넘긴 뒤 입자를 어떻게 다시 만드나 | 구마다 **사면체 메시** (평균 2000 요소/입자 · 총 0.81 M / 1.14 M · 지름당 ≈7.7 요소 변 [카드 산술]) · 겹침 · 틈 처리 문장 없음 · 벌칙 접촉 (p.3 · p.6) | 구를 다시 만들지 않는다 — AM = 격자 장애물로 고정 · SE = 덤프 중심의 구 씨앗을 복셀 union 으로 굽기 (`--se-dump`) · Eulerian 격자 + 물질점 (MLS-MPM) (§4.6) | 후보 A · A′ (MPM 속) / 후보 B (입자별 FE = 이 논문) | **가져올 것**: 후보 B 의 조립 순서 (구 → 사면체 → 면 · part 집합 → 재료 카드 `material.k`) · 입자당 요소 수 수렴 보고 꼴 (Fig 3e — 마지막 증분을 숫자로).  **못 가져올 것**: 생산 침대 규모 (SE 32,832 → 요소 ≈65.7 M · ≈1 년 — §11 카드 산술) — 작은 REV 만 |
| (라) 넘긴 직후의 평형 | 문장 없음 [미확인] · 'Initial stage' 무응력 색 [판독] · 펀치가 층 위에서 출발 (Fig 4a 응력 0 구간) | 카드 · 비교 문서에 없음 | 카드 · 비교 문서에 없음 | **가져올 것**: 그들도 안 적었다 → 출발 응력 · 겹침 검사 · 재평형 여부를 결과 전에 정해 적는다.  **못 가져올 것**: 절차 자체 (원문에 없음) |
| (마) 재료 · 접촉 · 마찰을 두 풀이에서 같게 두나 | **다르게** — DEM Hertz–Mindlin · μ 미끄럼 0.5 · 구름 0.05 · 반발 0.7 (E 미인쇄) ↔ FE 벌칙 + Coulomb **μ 0.2** (*"selected for best experimental agreement"*) · E 170 GPa · Swift (p.3 · p.5 · p.6) | DEM hooke/hysteresis + adhesion · E_eff 1.35 GPa ↔ MPM E 1.53 · ν 0.49 · σ_y 0.30 · 접촉 = 격자 암묵 (같은 셀 = 붙음 · 마찰 없음) (§4.6 · §15.1) | 조건 R2 (미끄럼 · 분리) · R5 (맞추는 값은 모델마다 하나) | **가져올 것**: 넘긴 뒤 풀이의 마찰을 따로 정하고 그 값 하나를 실험에 맞춘 선례 + 그 값의 민감도 (Fig 3f: μ 0.1–0.3 → RD 84.2–85.9 %).  **못 가져올 것**: 금속 값 (E 170 GPa · Swift) — 절대값 전이 0 |
| (바) 경계 · 하중 | 강체 금형 (완전 구속) + 펀치 지정 운동 → 최고 압력 → 제하 (p.5) · 펀치 속도 · 시간 간격 · 질량 스케일링 · 준정적 판정 **[미확인]** · 반력 = 충격량 미분 (식 1 · 2) | 판 (플래튼) servo / hold · 판 속도 마하 규율 (`--platen-mach`) · `wallP` = 경계 반력 직합 (§7.2 · §14) · 측방 주기 RVE (비교 문서 F 절) | 단계 4–6 (붓기 → 누르기 → 빼기) — 경계 세부는 카드 · 비교 문서에 없음 | **가져올 것**: 금형 + 지정 운동 펀치 + 같은 계산 안의 제하.  **못 가져올 것**: 재하율 · 준정적 판정 숫자가 없어 우리 규율로 대조할 값이 없다 · 반력 판독 규약이 다르다 (충격량 미분 ↔ `wallP`) |
| (사) 하중을 뺄 때 | **같은 계산에서 푼다** (p.3) · 2000 MPa → 5 MPa 규약 자리까지 부피 **+11–12 %** [카드 산술] · P ≈ 0 끝 기공 ≈17 % (마지막 수직 구간 = 펀치 이탈일 수 있음 [카드 추론]) | **안 푼다** — hold 는 정지 뒤 고정이라 되돌아옴 축을 원리상 못 낸다 (`--protocol release` 팔 필요 — 비교 문서 F 절) | **단계 6** · 조건 R4 | **가져올 것**: ★ 가압 + 제하 루프 그림 (Fig 4b) · 제하 판독 문턱 (5 MPa) 을 결과 전에 정하고 그 민감도를 같이 적기 · 응력 0 꼬리를 압분체 되돌아옴으로 세지 않기 · 압분체 되돌아옴 ≈ 재료 P/K 의 8 배 (§15.5) = 접촉 열림을 담아야 한다.  **못 가져올 것**: 금속 압분체의 되돌아옴 크기 |
| (아) 검증 | 같은 그룹 실험 [15,16] · 같은 그룹 ABAQUS 모형 · 최대 편차 2.1 %p (상대 2.5 %) · 제하 뒤 5 MPa 규약 · 시드 없음 | 외부 실험 대조 (porosity · overlap · EIS — §15.1; Minnmann 은 `CL-94` 로 출처 철회) | 단계 4 = 순수 SE 기공 기준에 항복 세기 하나 · 결과 전 대조 항목 | **가져올 것**: 같은 모형을 다른 풀이기로 돌려 풀이기 몫을 가르는 대조 (OpenRadioss − ABAQUS = Fine 0.4 %p 이하 · Coarse 1.3–2.2 %p).  **못 가져올 것**: 그룹 내부 실험 = 외부 앵커 아님 |
| (자) 계산 비용 | 403–1033 입자 · 0.81–2.07 M 요소 · 7–24 h (CPU 수는 Table 3 의 24 만) | 침대 3 만 입자급 · GPU MPM 시간 단위 (§15.1) | 카드 · 비교 문서에 없음 | **가져올 것**: 크기 · 입자 수 · 벽시계 표 (Table 1 꼴) 를 SI 에.  **못 가져올 것**: 생산 침대 규모의 입자별 FE (≈1 년, §11) |
| (차) 저자가 적은 한계 | 자료 넘김이 어렵다 (p.2) · LS-PrePost 수작업 (p.3) · 구 가정 · 단봉 2 종 · 작은 RVE (p.6) | 씨앗이 정답을 담는 순환 · 한 속도장 = 붙은 계면 · 제하 없음 (비교 문서 C · F 절) | 조건 R1–R7 (R1 AM 하중 분담 · R2 미끄럼 · 분리 · R3 SE 경계 기억 · R4 탈압 · R5 값 하나 · R6 SE 형상 변형 · R7 AM 파괴) | **가져올 것**: '넘김이 어렵다' 를 스스로 적은 원문 (§4.7 (차)) — 후보 B 를 고를 때의 비용 근거.  **못 가져올 것**: — |

⇒ **한 줄**: 이 논문은 우리 **계획** (느슨한 충전에서 넘겨 한 모델로 누르고 빼기) 과 넘김 시점 · 제하 포함이 같고, 우리 **지금**
(압밀이 끝난 덤프의 골격) 과는 시점이 정반대다.  넘기는 내용 (중심 + 반지름) 은 셋이 같고, 넘긴 직후의 겹침 · 평형 처리는
이 논문도 적지 않았다 — 우리가 결과 전에 정해 둘 빈칸이다.

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
- ⑤ **비용 논거 확보**: "왜 MPM 인가" 에 대해 **문헌 실측 기반 수치**(569입자 9 h — CPU 수 미인쇄 · Table 3 의 Coarse 는 24 CPU 7 h,
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
- ⛔ **재료**: Fe–Si–Al–P (E 170 GPa, σ_y 0.59–1.39 GPa) ≠ LPSCl (E 22–24, σ_y 0.05–0.30 — ⚠ 이 σ_y 범위는 출처
  [미확인] 표지 · stoic-knuth `SELF-160`).  절대 porosity·RD·응력 **전이 금지**.  (무차원 P/σ_y 밴드 겹침만 방법론 비교의
  근거로 쓴다.)
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
2. ★ **Fig 3(e) 의 2500 점 ↔ 본문** (2026-11-11 고쳐 씀) — 그림 ≈**1379** MPa · 본문 **1310** MPa (p.6).  그림대로면
   2000 → 2500 이 −1.4 % (평탄화 = 저자의 'convergence' 와 맞음), 본문대로면 −6.3 %.  선택 근거는 본문이 밝힌 대로
   **런타임(9 h vs 36 h)** 이다.  (옛 항목 '−5 % 로 단조 감소 · 평탄부 없음' 은 옛 판독과 본문 값을 섞은 것 → 철회.)
3. ~~★ 제하 후 RD 삼각형이 닫히지 않는다 (≈5–7 %p)~~ **⛔ 2026-11-11 철회 — 닫힌다** (§10 표: Fig 4a 꼬리 끝 ↔ Fig 4b
   P ≈ 0 끝 0.3–0.7 %p · 본문 5 MPa 값은 그 사이 발끝).  옛 판정은 Fig 4(a) 의 응력 0 꼬리를 놓친 옛 판독에서 나왔다.
   남는 것: 마지막 수직 구간 (Fine 12.1 → 16.9 %, 압력 0–5 MPa) 이 펀치 이탈일 수 있다 [카드 추론].
4. ~~"fine … due to its denser packing" ↔ Fig 4(b) 초기 porosity 는 Fine 이 더 높다~~ **⛔ 2026-11-11 철회** — 압력이 뜨는
   점의 기공 Fine 42.8 · Coarse 42.4 % (판독 오차 안) · 61 % 는 펀치 접촉 전 구간 (§8).
5. **µ 선택 근거** — Coarse 단독으로는 `digitized` µ=0.1 이 실험에 더 가깝다.
6. **DEM µ_s=0.5 vs MPFEM µ=0.2** 불일치, 설명 없음.
7. **버전 불일치**: C7(FreeCAD 1.0.2 / LS-PrePost 4.9) ↔ refs [24](1.0.1) / [26](4.8).
8. **요소 +25 %에 런타임 4배**(9→36 h) 미설명.
9. **초록 "maximum relative density deviation of only 2.5 %"** 는 **상대**값이다 (절대 2.1 %p).
   퍼센트포인트로 오독하면 정확도를 과대평가하게 된다.
10. (2026-11-11 추가) *"A peak pressure of 2000 MPa was applied in all simulations"* (p.6) ↔ Fig 4(g)(h) 는 **1400–2000 MPa
    다섯 점** — 낮은 압력 점을 얻은 방법 미기재.
11. (2026-11-11 추가) **9 h 가 두 곳** — Table 1 (Fine · RVE 210 µm) 과 p.6 메시 시험 문단 (Coarse · 2000 el/입자); 같은
    'Coarse · 2000 el' 이 Table 3 에서는 **7 h** (24 CPU).  CPU 수는 Table 3 에만 인쇄.
12. (2026-11-11 추가) Fig 4(a) 캡션 *"Engineering strain-stress curve of the Coarse powder"* ↔ 그림은 Coarse · Fine 두 곡선.
13. (2026-11-11 추가) Table 2 의 ABAQUS 칸은 Solver · Friction coefficient 행이 **비어 있다** — 본문의 *"follows the same
    geometric, material, and loading definitions"* (p.6) 로 같다고 읽을 뿐.

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
| P-5 | Minnmann/Cronau 앵커가 **가압 중인가 해압 후인가** 문헌 재확인 | **미해결 질문** · ⛔ Minnmann 앵커는 출처 철회 (`CL-94`) — 가압 중 ↔ 놓은 뒤 질문은 비교 문서 A 절 `miss2026_insitu_conductivity_porosity_pressure_compaction` 항목이 이어받음 (2026-11-11 표지) |
| P-7 | (2026-11-11 추가) 넘김 계약 정하기 — 넘기는 칸 (중심 · 반지름 · 상 · 번호) · 넘김 시점 · 겹침 · 틈 검사 · 출발 응력 · 재평형 여부 · 제하 판독 문턱을 **결과 전에** 적기 (§4.7 · §15.6 — 이 논문이 안 적은 빈칸) | 신규 · 계획 단계 4–6 의 사전 항목 |
| P-6 | 검증 프로토콜 3종 + 비용표(Table 1 형식)를 우리 SI 양식으로 | 형식 도입 |

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
