# SE-코팅(core-shell) vs 입자-혼합 ASSB 양극의 DEM 냉간압밀 — tortuosity·AM damage·percolation + 코팅의 σ_e 차폐 — So (J. Power Sources 2022)

> slug `so2022_dem_compaction_coated_particles_assb` · DOI `10.1016/j.jpowsour.2022.231279` · type `DEM` (결과/적용 논문) · PDF `So_2022_JPowerSources_DEM_Compaction_CoatedParticles_ASSBCathode.pdf` · digested `2026-06-26` · status ✅ · OPEN ACCESS (© 2022 Elsevier)

---

## 1. 한 줄 요약

**SE를 두 방식 — 자유입자(particle MIXTURE) vs SE-코팅-AM(core-shell SE COATING) — 으로 모델한 3D DEM 냉간압밀(cold-press) 시뮬레이션으로, 코어-쉘 SE 코팅이 *우월한 percolating network* 덕에 *더 효과적인 이온수송*을 만든다는 것을 보인 ASSB 양극 결과 논문.**
핵심 발견 3개: ① **SE 코팅은 낮은 몰드압(25 MPa)에서 이미 SE percolation >90 %** (혼합은 같은 90 %에 **360 MPa** 필요) → 코팅이 이온망에 압도적으로 유리; ② **★ 낮은 몰드압에서 SE-코팅 쉘이 AM-AM 전자접촉을 *차폐(shielding)* 해 전자수송이 끊긴다 — 이 차폐는 200 MPa 초과 고압에서 사라진다**(쉘이 박리/관통돼 AM-AM 접촉 형성); ③ **두 방식 모두 AM 손상(damage)이 ~12 %@500 MPa로 비슷하고, 둘 다 손상이 집전체 근처(상·하 벽 경계)에 집중**된다.
이 논문은 우리가 이미 digest한 **So 2022 MethodsX(접촉모델 정의서, `so2022_dem_contact_model_assb_compaction_sintering`)의 *결과(results) 짝*** 이며 — MethodsX가 "엔진(접촉법칙 방정식)"이라면 이 JPS가 "결과(코팅 vs 혼합·tortuosity·damage·percolation)" — 동시에 **So 2021 JPS(LPS+Si)의 *양극·코팅* 확장판**이다.
⚠ **전달은 *명시적 σ 솔버가 아니라 TauFactor tortuosity(τ_SE / τ_AM)로 추정*** 하며, **소재는 LPS(Li₂S–P₂S₅) + NCM/LiCoO₂ 양극**(우리 LPSCl+NMC811 아님) → 절대값 전이 금지, *방법·추세*만. ⇒ **이 논문이 우리에게 주는 직접적 가치 = (a) SE-코팅을 *명시적 core-shell* 로 모델하는 방법(우리 backlog A4 se_coating·Kang2025 LZO 코팅의 직접 선례), (b) "코팅이 저압서 σ_e 를 차폐한다"는 메커니즘(우리 σ_e 폼·coverage 차폐와 비교).**

---

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Magnus So, Gen Inoue (교신), Kayoung Park, Keita Nunoshita, Shota Ishikawa, Yoshifumi Tsuge** (Kyushu University, Dept. Chemical Engineering) | **J. Power Sources 530 (2022) 231279** | 10.1016/j.jpowsour.2022.231279 | **LPS = Li₂S–P₂S₅** SE + **NCM/LiCoO₂** AM (양극; Table 1 E_AM=199·H_AM=11.2 = Cheng LiNi₀.₃₃Mn₀.₃₃Co₀.₃₃O₂ / LiCoO₂) | **3D DEM** 냉간압밀(코팅 vs 혼합), Nakamura et al. [17] FIB-SEM 실험과 대조 |

> **이 논문의 위치 (So 그룹 계보):**
> - **So 2020 (2D)** [27, 29] — ASSB 제조·셀-인터칼레이션 2D DEM, 평형 overlap 소성 정의 시초.
> - **So 2021 JPS 508, 230344** [30] (= 우리 digest `so2021_dem_mold_pressure_assb_coldpress`) — 그 2D 의 **3D 확장**, LPS+Si, σ_SE^rel·percolation(φ_SE^crit=0.13).
> - **★ So 2022 JPS 530, 231279 = *이 논문*** — So 2021 을 **양극(NCM)·코팅(core-shell)** 으로 확장, AM breakage 추가.
> - **So 2022 MethodsX 9, 101857** [31] (= 우리 digest `so2022_dem_contact_model_assb_compaction_sintering`) — **이 JPS 의 접촉모델 부록**(rate-h_eq + F_th=H·A_con + c_area/c_spring + 소결).
> ⇒ **이 JPS(결과) + MethodsX(방법) 은 *한 쌍* 이다.** 접촉법칙 방정식은 MethodsX digest 가 완전 유도; 여기선 *결과*(코팅 vs 혼합, tortuosity, damage, percolation) 에 집중하고 방법은 요약만.
> ⚠ **소재 주의:** SE = **LPS(Li₂S–P₂S₅, argyrodite 아님)**; AM = **NCM/LiCoO₂ 양극**(So 2021 의 Si *음극* 과 다름 — 이번엔 *양극*). E_AM=199·H_AM=11.2 GPa (Cheng [37]). 절대값 전이 금지.

---

## 3. 핵심 물성·수치

> 데이터 CSV: `docs/data/so2022_coated_particles.csv` (코팅 vs 혼합 × 몰드압 sweep: damage / tortuosity / percolation / fusion-bond / volume-fraction).

### 3.1 소재·기하 파라미터 (Table 1–2, stated)
| 물성/파라미터 | 값 | 출처/조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **E_SE (LPS)** | **24 GPa** | Sakuda et al. [8] | stated (Table 1) | 우리 real-bulk 24 와 수치 동일(우연; LPS 도 sulfide). 우리 E_eff 1.35 는 이 24 의 18× 연화 프록시 |
| **E_AM (NCM/LiCoO₂)** | **199 GPa** | Cheng et al. [37] | stated (Table 1) | ⚠ "Young modulus of AM (NCM)" — So 2021 의 Si(70) 과 다른, *양극* AM. 우리 NMC811 140 보다 뻣뻣 |
| **H_AM (NCM hardness)** | **11.2 GPa** | Cheng et al. [37] | stated (Table 1) | AM 단단 → 소성 거의 안 함; **AM-AM 융착은 냉간서 *새로 안 생김*** (NCM 은 고온소결 필요) |
| **H_SE (LPS hardness)** | **1.9 GPa** | McGrogan et al. [7] | stated (Table 1) | LPS 무름 → SE 만 소성·융착. F_th=min(H_i,H_j)·A_con 항복 임계 |
| ν_SE / ν_AM | **0.32 / 0.25** | Sakuda [13] / Cheng [37] | stated (Table 1) | (So 2021 은 0.3/0.3; 여기선 상별로 다름) |
| μ (마찰) | 0.5 | This study | stated | Coulomb |
| e (COR) | 0.5 | This study | stated | damping η = f(e) |
| **d_AM aggregate / primary** | **5 / 1 µm** | Nakamura [17] / fit | stated (Table 1) | AM = 1 µm primary NCM 의 5 µm 응집체 |
| **d_SE aggregate / primary** | **1.5 / 0.5 µm** | fit (§2.2) | stated (Table 1) | SE primary 0.5 µm peak(부피로는 ≤0.7 µm tail 지배) → aggregate 1.5 µm |
| f_SE (응집 안 한 자유 SE 부피분율) | **30 %** | mixture 설정 (§2.2) | stated | mixture 에서 non-aggregated SE = 30 vol% |
| f_AM (solid 내 AM 부피분율) | **0.734** | Nakamura [17] | stated (Table 1) | |
| **입자수 (coated 적용)** | mixture: AM+SE 혼합 / coated: SE-코팅-AM | Table 2 (MethodsX) | stated | 20×20 µm box |
| 압력 프로파일 | PID 제어 상단벽 → 목표 몰드압 | §2.4 | stated | bottom wall 고정, 측방 주기경계 |

### 3.2 결과 수치 (코팅 vs 혼합, 몰드압 함수 — Fig 3–7)
| 물성 | 값 (mixture / coating) | 조건 (P) | stated/digitized | 비고 |
|---|---|---|---|---|
| **porosity (= 1 − AM − SE)** | mixture ~17 % / coating ~16 % | 360 MPa | digitized (Fig 3a) | FIB-SEM 과 부피분율 잘 일치; ⚠ **AM-pore 면적은 과대평가**(§4.3, AM 내부 소공극 과다) |
| vol% AM / SE | mix 0.61 / 0.22 · coat 0.59 / 0.25 | 360 MPa, sim | digitized (Fig 3a) | |
| **★ Rel. SE percolation volume** | mix 0.15→0.9 / **coat >0.9** | 25 MPa | **stated** (§3.3) | ★ **코팅 SE 가 25 MPa 서 이미 >90 % percolate; 혼합은 360 MPa 필요** = 코팅의 핵심 이점 |
| **★ Rel. AM percolation volume** | mix ~1.0 / **coat ~0.3** | 25 MPa | **stated** (§3.3) | ★ **코팅 AM 은 25 MPa 서 0.3 (쉘이 AM-AM 차폐); 100 MPa 서 ~1.0** = 차폐가 고압서 사라짐 |
| τ_SE (SE tortuosity factor) | mix 36→6 / coat 10→4 | 50→500 MPa | digitized (Fig 7a) | ★ **코팅이 모든 P 서 τ_SE 낮음**(red < blue) = 이온수송 우월; 고압서 둘 다 수렴 |
| τ_AM (AM tortuosity factor) | mix 7→2.5 / **coat 26→2.5** | 50→360 MPa | digitized (Fig 7c) | ★ **코팅 τ_AM 이 저압서 *훨씬 높음*(26)** = 전자경로 차폐; 고압서 거의 같아짐(merge) |
| **AM damage f^AM (eq 9)** | mix ~12 % / coat ~12 % | 500 MPa | **stated** (§3.5) | ★ **둘이 비슷**(통계적 유의차 없음); AM-AM 융착결합 *감소율*로 정의 |
| AM damage 공간분포 | 상·하 벽 ~25 %, 중앙 ~5 % | 360 MPa | digitized (Fig 6d) | ★ **집전체·SE층 경계 근처 집중**(두 방식 동일) |
| AM-SE fusion bonds | mix 0→2.3e4 / **coat 5.0e4→5.5e4** | 0→500 MPa | digitized (Fig 5a) | 코팅은 *시작부터* AM-SE 결합 보유(혼합은 0서 빌드업); 저압서 차 최대 |
| AM-SE delaminated / attached | delam 1.3e4 / attach 1.8e4 (net↑) | 500 MPa, coat | digitized (Fig 5b) | ★ **박리(detachment)된 SE > 재부착(reattach) 인데도 *순증*** — 코팅 핵심 메커니즘 |
| AM-AM fusion bonds | 4.2e4 → 3.7e4 (둘 다) | 0→500 MPa | digitized (Fig 6a) | **압력↑ → AM-AM 결합 *감소* = damage** (이게 f^AM 의 분자) |
| **전달 σ (절대 mS/cm)** | **n/a — 명시 안 함** | — | — | ★ **τ-기반 추정만** (TauFactor). σ_ionic/e 절대값·Kirchhoff·Holm·coverage 없음 |
| **Heckel P_y / knee** | n/a (Heckel 안 함) | — | n/a | relative-density 곡선은 MethodsX/So2021; 이 논문 본문엔 porosity-vs-P 풀곡선 없음 |
| PSD (D10/D50/D90) | n/a (명시 표 없음) | — | n/a | primary 0.5/1 µm + aggregate 1.5/5 µm peak·lognormal σ_g 0.3 만 |

---

## 4. 시뮬레이션 방법 ★

> 접촉법칙 *완전 유도*는 동반 MethodsX digest(`so2022_dem_contact_model_assb_compaction_sintering` §4) 에 있음 — 여기선 *이 결과 논문이 쓴 방법*을 요약하고, **코팅 생성·percolation·tortuosity·damage 후처리**(이 논문 고유) 에 집중.

### 4.0 code / version
- **code**: **in-house DEM** (So 그룹 자체 MATLAB; "slight modification of code in [30]" = So 2021). LIGGGHTS/LAMMPS 아님. 적분 = **Verlet 2차** [35]. 워크스테이션 Intel Xeon W-2145(8코어), **1 data point ≈ 4 h**, 전체 sweep **~10 일**.
- 접촉모델 상세는 [31] MethodsX (eq 1–9 in this paper = MethodsX 의 축약 재서술).

### 4.1 DEM 접촉법칙 (eq 1–7, 요약 — MethodsX 와 동일)
- **탄성 Hertz 스프링** (eq 1–4): `F_spring = k_n·h_ov`, `k_n = 4/3·E_eff·h_ov^{1/2}·R_eff^{1/2}`, R_eff·E_eff 표준 조합.
- **소성 — 평형 overlap h_eq** (eq 5): `F_spring = k_n(h_ov − h_eq)` — 소성변형으로 접촉점이 비구형이 된 *영구 잔류* overlap.
- **h_eq rate** (eq 6) — 부호별 3분기 (소결/융착 포함):
  ```
  ∂h_eq/∂t =  (F_spring − F_th)/(t_rel·k_n)   if  F_spring > F_th     (consolidation, 압축 융착)
              0                                if  −F_th < F < F_th    (dead band)
              (F_spring + F_th)/(t_rel·k_n)    if  F_spring < −F_th    (detachment, 융착/코팅 박리)
  ```
- **임계력 F_th** (eq 7): `F_th = min(H_i, H_j)·A_con` — 재료 경도 H 로 항복 결정(σ_yield ≈ H 근사). **detachment 시 F_th=0** (단, 같은 aggregate 가 아니거나 *기존 pre-sintered* 접촉이 끊긴 경우). c_area·k_n 보정인자(porosity→0)는 [31] 참조.
- **★ 물리 핵심:** **LPS SE 는 상온 압력소결로 융착(fusion bond) 가능** [8] → SE-SE·AM-SE 에 융착 허용. **AM-AM 은 냉간서 *새 융착 금지*** (NCM 은 고온소결 필요) — 단 응집체 *내부* 엔 이미 융착이 있고, 그게 *끊기면* = **AM 균열(cracking) damage**. ⇒ **"AM-SE 박리 = 코팅 박리(delamination)", "AM-AM 융착 끊김 = AM 입자 손상"** 이 이 논문의 두 핵심 사건.

### 4.2 ★ SE 코팅 생성 방법 (§2.3, Fig 1d) — core-shell 표현 (이 논문 고유, backlog A4 직접 선례)
**혼합(mixture)**: AM 응집체 + 자유 SE 입자(30 vol%) 를 도메인에 *섞어* 배치 (Fig 1b). SE 와 AM 이 독립 입자.
**코팅(coating)**: SE 를 AM 표면에 *붙여서* core-shell 생성 (Fig 1d) — 4단계:
1. AM 응집체를 §2.2 방식으로 먼저 구성(1 µm primary NCM → 5 µm 응집체, annealing 융착).
2. **AM 표면을 수치적으로 추정**: AM subparticle 위치들의 **3D Delaunay triangulation** → tetrahedra → **긴 모서리(long-edge) tetrahedra 제거**(표면 거칠게, no long edge 남을 때까지) → 표면 삼각망.
3. **SE 입자(0.5 µm primary)를 그 표면에 랜덤 배치** → SE 쉘.
4. **shoving 알고리즘**으로 겹침 제거 → 코팅된 입자 위치 재계산.
⇒ **SE 가 AM 을 둘러싼 *film/shell* 로 집중** (graphical abstract: coating 은 SE 가 AM 주위 막). **이게 우리 backlog A4(`se_coating_interface` carbon) + Kang2025 LZO 코팅의 직접 DEM 선례** — 단 그들 SE 코팅은 *이온전도* 쉘(σ↑), A4 carbon·LZO 는 *전자전도/패시베이션* 쉘(종류 다름; §B 참조).

### 4.3 percolation·tortuosity 후처리 ★ (이 논문 고유 — 전달 *추정*)
- **percolation cluster 분석** (Fig 4): 압밀 후 **접촉력으로 연결된 입자를 cluster 로 묶음**. (a) **AM aggregate 수**(fragmentation), (b) **AM percolation cluster 수**(연결도; 적을수록 연결↑), (c) **Rel. AM percolation volume**(전자수송 backbone = AM 중 percolate 한 부피비), (d) **Rel. SE percolation volume**(이온수송 backbone).
- **tortuosity factor τ** (Fig 7, **TauFactor** [36], Cooper et al. 외부 MATLAB): 입자→3D grid 매핑 [30] 후 **SE 상·AM 상 각각의 τ 를 라플라스 확산으로 계산**. PBC(주기경계)·non-PBC 두 버전. **non-PBC 가 FIB-SEM 실험(Nakamura)과 더 잘 일치**.
- **★ "이온수송 = τ_SE / SE percolation", "전자수송 = τ_AM / AM percolation" 으로 *논의*** — **명시적 σ 값을 안 푼다.** σ_eff ∝ φ/τ (So 2021 eq 1) 형태가 암묵 전제지만, 이 논문은 **τ 와 percolation volume 만 보고**하고 코팅 vs 혼합의 *상대 우열*을 거기서 읽는다. ⇒ **우리 Kirchhoff/Holm 명시 σ 솔버가 정확히 그들이 비운 칸**(§C novelty 1).

### 4.4 AM damage 후처리 ★ (Fig 6)
- **damage 정의 (eq 9):** `f^AM = (n_initial^{AM-AM} − n_current^{AM-AM}) / n_initial^{AM-AM}` = **AM-AM 융착결합의 상대 감소율**. 압밀 중 AM 응집체 내부 융착이 인장으로 끊기면(F_spring < −F_th) = 균열 = damage↑.
- **공간분포 (Fig 6c/d):** 입자별 damage 를 3D 로 색칠(c) + **수직위치(z) 별 수평단면 평균**(d). → **상·하 벽(집전체·SE층 경계) 근처에 집중** (~25 % vs 중앙 ~5 %), 두 방식 동일.

### 4.5 입자 처리 ★★ (DEM판 "무질서 처리")
- **구(sphere)만** — AM·SE 모두 구 (1 µm AM primary, 0.5 µm SE primary 의 *응집체*). **입자 외형은 절대 변하지 않는다.** 소성은 **CONTACT 소성**(h_eq = 접촉점 함몰/융착 proxy)이며 **진짜 입자 SHAPE 흐름(void-fill flow) 아님.**
- **AM = 깨질 수 있는 응집체(breakable aggregate)** ★ — primary NCM 구들이 융착으로 묶인 클러스터; **융착이 끊기면 fragment(균열)**. = So 2021 의 "AM 은 구, intraparticle cracking 은 future work" 를 **한 발 넘어선** 부분: **응집체-수준 균열(aggregate breakage)은 모델**하지만 **primary 구 *자체*의 균열·형상변화는 안 함**.
- **SE 코팅 = AM 표면 SE 쉘** — core-shell 이지만 **여전히 구의 집합**(0.5 µm SE 구가 AM 표면에 배치). 쉘의 *박리(delamination)·재부착(reattachment)* 은 모델하나, SE 가 *흘러서* AM 을 감싸는 연속 film 형성은 안 함.
- ★ **명시 한계(저자 스스로, §4.3):** "rough spherical AM 으로 제한 — 비구형·구조화 배열은 안 함 → 구형/타원에서 크게 벗어난 입자엔 결론 적용 불가"; "**AM-pore 면적 과대평가** (시뮬이 AM 내부 소공극을 너무 많이 만듦)"; "SE 코팅이 실험보다 *덜 매끈* → AM 표면이 부분 노출".

### 4.6 도메인/RVE / servo / seeds / 압력범위
- **도메인 20×20 µm** (측방 주기경계 + ghost; bottom wall 고정). ⚠ "**20 µm 는 AM 응집체(5 µm) 대비 크지 않다 → aggregate-수 의존성 배제 못 함**"(§4.3 명시 한계). primary 0.5–1 µm 라 도메인 더 키우기 어려움(전체 sweep 10일).
- **압력 sweep ~25–500 MPa**(Fig 4–7; percolation·tortuosity·damage 곡선). 일부 비교는 360 MPa(Nakamura 실험 매칭).
- **servo**: 상단벽 PID 제어로 목표 몰드압 유지(So 2021 과 동일).
- **seeds**: 다중실현·통계 명시 없음(단일 실현으로 보임; damage "통계적 유의차" 언급은 곡선 차 기준).

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **실험(Nakamura SEM) vs 시뮬 — 혼합·코팅 모식**: (a) mixture SEM(Mn/S EDS), (b) mixture sim(검은 AM 응집체 + 노란 SE), (c) **SE-coated AM SEM**, (d) **SE-coated AM sim** (AM core + SE shell + 파란 delaminated) | ★ **core-shell 코팅 생성(§4.2)의 그림**; Delaunay-triangulation 표면추정 → SE 쉘. 우리 backlog A4 se_coating 의 시각 레퍼런스 |
| **2** | **압밀 후 입자분포 360 MPa**: (a–c) mixture 3D/2D-slice/FIB-SEM, (d–f) coating 3D/2D-slice/FIB-SEM (box 22.9/23.9 µm) | morphology 정성 — 우리 vis_zoom·MPM morphology 대비(단 구라 형상변화 없음). FIB-SEM 직접 대조 = frame[4] 실험 앵커 |
| **3** | **부피분율·계면면적**: (a) AM/SE/pore 부피분율 sim-vs-exp(혼합·코팅), (b) **비표면적 AM-pore/AM-SE** sim-vs-exp | ★ **(a) porosity ~16–17 %@360 MPa**(우리 15.6 % 와 *방향* 비교); **(b) AM-SE 면적 과대평가**(§4.3) = 우리 coverage/A_AM-SE 와 대조 시 주의(그들은 *추정*, 우리는 Stage-E 물리) |
| **4** | **★ percolation 비교(코팅 vs 혼합)**: (a) AM aggregate 수, (b) AM perc cluster 수, **(c) Rel. AM perc volume(전자), (d) Rel. SE perc volume(이온)** | ★★ **핵심 결과**. (c)(d) 가 *코팅의 이온 우월 + 저압 전자 차폐* 를 동시에 보여줌: **(d) coat SE >90 %@25 MPa(이온↑), (c) coat AM 0.3@25→1.0@100 MPa(전자 차폐→해제)** = 우리 σ_e 차폐·σ_ionic 비교의 핵심 데이터 |
| **5** | **AM-SE 융착(코팅 박리)**: (a) AM-SE fusion bonds 코팅 vs 혼합, (b) **코팅의 balance(accumulated=initial+attached−delaminated)**, (c) 3D delaminated, (d) slice, (e) FIB-SEM delaminated SE | ★ **delamination 메커니즘**: 박리된 SE > 재부착인데 *순증* → AM-AM 접촉 위한 *공간* 생김(쉘 얇아짐). 우리 `--coh` 정적점착과 달리 *rate 박리/재부착* |
| **6** | **★ AM damage**: (a) AM-AM fusion bonds(감소=damage), (b) **AM damage vs 몰드압(~12 %@500, 코팅≈혼합)**, (c) 3D damage map, **(d) damage vs 수직위치(상·하 벽 ~25 %)** | ★ **damage-near-current-collector** = 우리 Auerbach 균열·force-chain 과 비교. (b) 코팅이 AM 보호 *거의 안 함*; (d) 벽 근처 집중 = 우리 fracture 공간분포와 대조 |
| **7** | **★ tortuosity factor**: (a) τ_SE vs P, (b) τ_SE vs SE분율, (c) τ_AM vs P, (d) τ_AM vs AM분율 (sim·exp·PBC) | ★ **(a) coat τ_SE < mix(이온↑); (c) coat τ_AM 26@저압→merge@고압(전자 차폐→해제)** = 우리 τ_Laplace/τ_Dijkstra 와 비교; 코팅이 τ_AM 을 *올린다*(전자 불리)는 trade-off |

---

## 6. Post-processing ★

- **무엇**: ① **percolation cluster 분석**(접촉-연결 입자 grouping → AM aggregate 수·AM/SE percolation volume·cluster 수); ② **tortuosity factor τ_SE·τ_AM**(TauFactor 라플라스 확산, PBC/non-PBC); ③ **AM damage f^AM**(AM-AM 융착 상대감소율 eq 9 + 공간분포 z-profile); ④ **AM-SE delamination/reattachment balance**(accumulated = initial + attached − delaminated, eq 8); ⑤ **부피분율·비표면적**(AM/SE/pore + AM-pore/AM-SE 계면, sim-vs-FIB-SEM); ⑥ **입자분포 시각화**(3D + 2D slice, FIB-SEM 대조).
- **도구**: 자체 MATLAB DEM 후처리 + **TauFactor** [36](Cooper, Imperial College). 외부 COMSOL/Kirchhoff 망 *없음*.
- **수치화·플롯·기록 방식**: 모든 지표(damage·τ·percolation volume·fusion bonds)를 **몰드압(25–500 MPa) 함수**로 **혼합 vs 코팅 두 곡선** 비교. **Nakamura et al. [17] FIB-SEM 실험**(부피분율·계면면적·τ·percolation)에 직접 중첩 검증(frame[4]). **σ 절대값은 안 뽑음** — 코팅 vs 혼합의 *상대 우열*을 τ·percolation 으로 논의.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

| 항목 | 이 논문 (So 2022 JPS) | 우리 | 차이 / 이유 (rigid·plastic / 소재 / 2D·3D / τ-추정·명시σ) |
|---|---|---|---|
| **DEM 접촉 소성** | rate-기반 CONTACT 소성(h_eq + H 항복캡, MethodsX) | hooke/hysteresis(plasticity 無) + Stage-E(Tabor) 사후보정 | **같은 부류**(CONTACT 소성·δ/h_eq 잔류, 진짜 SHAPE 흐름 아님). So 의 H-cap 이 우리 18× 연화의 물리적 대안(MethodsX §7 참조) |
| **★ SE 코팅 표현** | **✅ core-shell 명시**(Delaunay 표면추정 → SE 쉘 + 박리/재부착 rate) | **✗ 없음** — SE 를 *자유입자*로 시드(우리 = particle MIXTURE 쪽) + Stage-E coverage 로 AM 피복 *사후 측정* | ★ **핵심 차이**: 그들은 코팅을 *구조로* 만들고(쉘 박리까지), 우리는 *자유 SE + coverage 메트릭*. **우리는 그들의 "혼합" 측만 모델 — "코팅" 측은 우리 backlog A4 의 정확한 선례**(§B) |
| **★ σ_e 코팅 차폐** | **✅ 메커니즘 발견**: 저압서 SE 쉘이 AM-AM 전자접촉 차폐(Rel.AM perc 0.3@25 MPa, τ_AM 26) → 고압서 사라짐(박리/관통) | **부분적** — 우리 σ_e 폼은 *coverage·SE 부피*가 AM-AM 접촉을 줄이는 걸 √A_AM-AM·φ_AM⁴ 로 반영하나, **"코팅 쉘 차폐 → 압력으로 해제" 라는 *압력-의존 차폐 동역학*은 없음** | ★ **그들이 *메커니즘*을 명시; 우리는 *정적 결과*만**. 우리 σ_e 의 coverage-shielding 은 *정적*(한 압력) — 그들 "저압 차폐→고압 해제" 는 우리 미보유 *압력축*(§B 흡수후보) |
| **★ AM damage** | **✅ AM-AM 융착 감소율 f^AM**(~12 %@500, 벽 근처 집중) — *응집체 균열* | **Auerbach 임계 + Lawn → fracture-aware Holm**(f_intact, partial-conduction; AM_P 92:8 8mAh서 37–40 % cracked) — *접촉응력 균열* | **다른 정의·같은 현상**: 그들 = 융착결합 끊김(aggregate breakage), 우리 = 접촉응력 Auerbach. **그들은 damage→전달 연결 안 함**(τ 만); **우리는 fracture→σ_e 직접 reduce**(우리 우위) |
| **transport 솔버** | **τ-기반 추정**(TauFactor 라플라스, φ/τ) — **명시 σ·접촉저항 없음** | **Kirchhoff + Holm 접촉저항 R=1/(2σr_c) + Stage-E 면적 + 삼중항** | ★ **우리 압도적 우위**: 그들은 *상대 τ* 만, 우리는 σ_ionic/e/thermal 절대값·구속저항·coverage. So 2021 도 τ-기반(같은 그룹 한계) |
| **percolation** | **cluster-부피 명시**(AM/SE percolation volume vs P) | √(φ−φc)·CN²·f_p³ percolation backbone | **둘 다 percolation 채택**. 그들 = *기하 cluster*; 우리 = *scaling-law 지수*. 그들 "코팅 SE >90 %@25 MPa" = 우리 dead-SE/φc 의 코팅-버전 |
| **MPM/morphology** | **✗ 없음** (구·CONTACT 소성·응집체 균열) | **MPM J2 ν=0.49 진짜 소성 SHAPE 흐름 + void-fill + scaffold 커플링** | ★ **우리 우위**: 입자 SHAPE 흐름·void-fill·Σdg = 우리 MPM 고유. 그들 SE 쉘 *박리*는 모델하나 SE *흐름*은 안 함 |
| **소재 SE** | **LPS (Li₂S–P₂S₅)**, E=24, H_SE=1.9 GPa | **LPSCl (argyrodite)**, E_eff 1.35 / real 24 | **다른 SE**. E=24 우연 일치; H_SE=1.9 우리 미사용 |
| **소재 AM** | **NCM/LiCoO₂ 양극**, E=199, H=11.2 GPa | **NMC811 양극**, E=140 GPa | **같은 부류(양극)** 이나 So 2021 의 Si 음극과 달리 *양극*. E 199 vs 우리 140(더 뻣뻣) |
| **차원** | **3D** (20 µm box) | DEM 3D / MPM 2D·3D | **둘 다 3D** |
| **압력** | **다중**(25–500 MPa percolation·τ·damage 곡선) | DEM 단일 300 + Heckel 4압력 | So 다중압력 → 우리 압력-의존(차폐 해제·percolation onset) 검증 유용 |
| **검증 앵커** | **Nakamura FIB-SEM**(LPS+NCM, 부피분율·τ·percolation) | Minnmann/Doux/Bazzoun(LPSCl) + MPM 독립 | 둘 다 실험 앵커; 단 *다른 소재* |

---

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **★ SE 코팅 core-shell 표현(§4.2) = 우리 backlog A4(`se_coating_interface`) + Kang2025 LZO 코팅의 *직접 DEM 선례*.** 우리 `additives.py` 는 carbon 을 *bulk 간극*에 시드하거나(seed_carbon_black) *surface_frac* 으로 일부 AM 표면에 코팅하지만 — **연속 *쉘(film)* 로 AM 을 감싸는 구조 + 쉘 *박리(delamination)*는 모델 못 함.** So 의 **Delaunay-triangulation 표면추정 → 표면에 입자 배치 → shoving 겹침제거** 가 정확히 그 방법. → A4 구현 시 **이 §4.2 를 레시피로** (단 So 는 *SE 이온쉘*, A4 carbon·LZO 는 *전자/패시베이션 쉘* — 시드 위치 동일, σ 효과 반대; §B 참조).
- ② **★ "코팅이 저압서 σ_e 를 차폐한다 → 고압서 사라진다" = 우리 σ_e 폼에 추가할 *압력-의존 차폐* 메커니즘 후보.** 우리 σ_e 는 coverage·SE 부피가 AM-AM 접촉을 *정적*으로 줄이는 걸 반영하나, **"쉘이 AM-AM 전자접촉을 막다가 압력으로 박리/관통돼 해제" 라는 *압력 동역학*은 없다**(Fig 4c: coat AM perc 0.3@25→1.0@100 MPa; Fig 7c: τ_AM 26→merge). → **se_coating 옵션에 "코팅 두께·압력 → AM-AM 접촉 게이팅" 항**을 넣으면, 저압 셀(작동 5–70 MPa)에서 코팅 전자저항이 *과소평가되지 않게* 됨. ⚠ 단 *우리 production 은 자유-SE 혼합*이라 이 차폐는 *코팅 regime 전용*; mixture 엔 무관.
- ③ **혼합 vs 코팅 대조 = 우리 SE-seeding 전략의 *프레이밍*.** So 결과: **이온은 코팅 우월(저압 percolation·낮은 τ_SE), 전자는 코팅이 저압서 불리(차폐), 고압서 무차별.** 우리는 *혼합*(자유 SE)만 → **우리 SE 분포가 So 의 "particle mixture" 에 해당**. ⇒ "코팅하면 이온↑·(저압)전자↓" 의 trade-off 를 우리가 *재현*하려면 A4 se_coating 이 필요; 안 하면 우리는 "혼합 측" 결과만 (정직히 명시). Kang2025 LZO 가 *이온쉘 아닌 패시베이션쉘* 이라 σ_e 차폐는 더 강할 수 있음(전자절연체).
- ④ **AM damage-near-current-collector(Fig 6d) ↔ 우리 Auerbach fracture 공간분포 비교.** So: AM-AM 융착 끊김이 **상·하 벽(집전체·SE층) 근처 집중**(~25 % vs 중앙 ~5 %) — 벽이 단단해 응력 집중. 우리 fracture-aware Holm(AM_P 92:8 8mAh 37–40 % cracked)은 *전체 평균*만 — **공간(z) 분포는 안 봄.** → 우리 fracture 출력에 **z-profile(벽 근처 균열↑)** 추가하면 So 와 직접 대조 가능 + backlog A9(크기-의존 파괴)의 *공간* 짝. ⚠ driver 다름: 그들 = 응집체 융착 인장끊김, 우리 = Auerbach 접촉응력.
- ⑤ **그들 τ_SE/τ_AM = 우리 τ_Laplace/τ_Dijkstra 의 *코팅-효과* 대조점.** So: **코팅이 τ_SE 낮춤(이온↑)·τ_AM 올림(저압 전자↓)**. 우리 τ 는 *한 구조*의 SE·AM 우회도지 *코팅 vs 혼합* 비교가 아님. → A4 se_coating RVE 를 우리 τ 솔버에 돌리면 "코팅 → τ_SE↓·τ_AM↑" 가 우리 솔버로도 나오는지(frame[4] 교차검증) 확인 가능.

---

## 9. ★ 우리 novelty — 왜 우리가 이 도메인 DEM 에서 state-of-the-art 인가 (our novelty vs So 2022 JPS)

> **확고히 — 우리는 DEM novelty 를 가지며 SOTA 다.** 근거 기반(그들 stated 범위·한계 인용), 과장 없이. So 2022 JPS 는 **ASSB 코팅-압밀 DEM 의 정교한 결과 논문**이고 **SE 코팅을 core-shell 로 모델한 점은 우리가 *없는* 강점**이지만, *역학·기하-추정 transport* 에 국한된다. 우리 7대 차별점을 그들이 *하는 것/없는 것*에 매핑.

1. **★ 전달 TRIAD(σ_ionic + σ_electronic + σ_thermal)를 *하나의 명시적 접촉망*에서 (Kirchhoff + Holm 1967 구속저항) — 그들은 σ 를 *안 푼다*.**
   So 2022 JPS 는 **명시적 σ 솔버가 없다** — 이온·전자 수송을 **TauFactor tortuosity(τ_SE / τ_AM) + percolation volume 로 *추정/논의*** 할 뿐, **σ_ionic/e/thermal 절대값을 한 번도 계산하지 않는다**(논문 전체가 τ·percolation·damage). 코팅의 "더 효과적 이온수송" 도 *τ_SE 낮음 + SE percolation 높음* 에서 *읽은* 정성 결론이다. ⇒ **우리는 같은 rigid-sphere 압밀 위에 σ 삼중항을 Kirchhoff+Holm 명시 저항망(R=1/(2σr_c))으로 얹는다** — 이게 So 계보(2020 τ → 2021 τ → 2022 τ)가 *구조적으로 비운 칸*이고 우리 transport novelty 의 정확한 위치다. (같은 그룹 *밖* Bazzoun 2026 이 RNM/Holm 을 추가한 것과 같은 방향 = 우리가 옳은 칸을 채운 증거.)

2. **★ Stage-E 소성 접촉-AREA 재유도(Tabor F/H + volume + geom min-cap) → *전달에 연결된* 면적; 그들 면적은 *과대평가된 기하-추정*.**
   So 는 AM-SE 비표면적을 보고하나 **스스로 "AM-SE 면적을 *과대평가*"(§4.3, AM 내부 소공극 과다·코팅 덜 매끈) 한다고 인정**하고, 그 면적이 *전달로 가지 않는다*(σ 없음, τ 만). 우리 Stage-E 는 *소성 접촉면적*을 **물리식 5-regime**(Tabor 소성 A=F/H, volume A=V/h_min, geom 하한)으로 풀고 **그 면적을 Holm 구속저항·coverage(Hertz 16 %/Tabor 52 %)에 직접 투입**한다. ⇒ 우리 면적은 *전달-연결·물리식·검증된 값*, 그들 면적은 *추정·과대·전달 미연결*.

3. **★ DEM↔MPM 커플링(scaffold) — 진짜 소성 SHAPE morphology 필드; 그들은 SE *박리*는 모델하나 SE *흐름*은 못 함.**
   So 2022 는 **rigid 구 + CONTACT 소성**(h_eq 함몰 proxy)이라 **SE 가 *흘러서* AM 을 감싸는 연속 film 형성을 못 한다** — 코팅을 *0.5 µm SE 구의 표면 배치 + 박리/재부착*으로만 표현하고, 스스로 "코팅이 실험보다 *덜 매끈*, AM 표면 부분 노출" 이라 인정한다. 우리는 **MPM(von Mises J2, ν=0.49)로 *진짜* 소성 SE SHAPE 흐름·void-fill·누적소성변형장 Σdg**를 풀고 **DEM AM scaffold + MPM SE 커플링**으로 porosity(15.93 %)·두께(29.95 µm)·코어보존+경계평탄화 morphology(SEM 일치)가 *EMERGE* 하게 한다. ⇒ So 가 "코팅이 덜 매끈하다(SE 흐름 부재)" 고 인정한 *바로 그 형상-morphology 절반*을 우리 MPM 이 채운다(frame[5]).

4. **★ Fracture-aware *전달*(Auerbach + Lawn → partial-Holm) — 그들 damage 는 전달과 *분리*.**
   So 2022 는 **AM damage(f^AM, ~12 %@500 MPa)를 *정량화*하지만 *전달에 연결하지 않는다*** — damage 는 부피분율·τ 와 별도로 보고되고, "코팅이 damage 를 거의 안 줄인다(유의차 없음)" 로 끝난다. 우리는 **Auerbach 임계 + Lawn 미세균열 → fracture-aware Holm(f_intact, partial conduction)**으로 *깨진 접촉이 σ_e 에 주는 영향*까지 폼에 넣는다(AM_P 92:8 8mAh 37–40 % cracked → σ_e fracture-reduced). ⇒ **균열→전달 결합 = 그들에 *완전히* 없는 축** (그들 damage 는 *역학 통계*, 우리 fracture 는 *전달 입력*).

5. **★ 문헌-grounded σ_grain(Cronau/Trevisanello/Wang) — 재료물성 1차 앵커; 그들은 *전달이 없으니* σ_grain 도 없다.**
   So 2022 는 역학 H/E 만 쓰고 *전달 σ 가 없으니* σ_grain·intrinsic σ 가 등장하지 않는다(τ 는 무차원 상대값). 우리 σ_ionic 은 **Cronau 2022 단결정 3.0 mS/cm × Cronau(r_SE) sub-µm GB 인자**, σ_e 는 **Trevisanello endpoint(10/5) + NCM(r)**, σ_thermal 은 Wang — 각 채널을 literature 물성에 고정. ⇒ 우리 전달 *absolute* 가 문헌-anchored (그들 τ 는 절대 σ 로 환산하려면 σ_bulk 곱이 추가로 필요).

6. **★ 실험-앵커 *독립* 이중모델 보정 (frame[4]/[5]) — 그들은 역학 단일모델 + FIB-SEM 한 종류.**
   So 2022 는 **Nakamura FIB-SEM(부피분율·τ·percolation) 한 종류에 비교**(역학·기하 단일모델). 우리는 **DEM(E=1.35 hooke/hysteresis+Stage-E)과 MPM(E=1.53 J2)을 *서로가 아니라 각각 실험(Minnmann)에* 독립 보정**하고 — 수렴(real_14 porosity 15.6↔16.7↔exp, coverage Tabor 48–52 %)은 *교차검증*, 발산은 *정량화된 모델한계*로 읽는다(frame[4]). ⇒ *두 독립 물리엔진의 합의*가 우리 신뢰 척도(단일 비교모델보다 강건).

7. **★ 솔버→스케일링법칙 압축(노이즈-천장 LOOCV) → ML 설계 예측기; 그들은 forward 결과에서 종료.**
   So 2022 는 *DEM → τ·percolation·damage 곡선*에서 멈춘다(설계 역문제·ML 없음). 우리는 **네트워크 솔버 출력을 노이즈-천장 LOOCV 스케일링법칙으로 압축**(σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.90)하고 → **설계 knobs → 전 메트릭 예측 → 2D 미세구조 합성 → 층상 복합양극**의 5단계 파이프라인으로 간다. ⇒ *예측·역설계*가 우리 work 정체성, So 는 *forward 역학·기하-추정*에서 종료.

**⚠ 정직히 — 그들이 우리보다 앞서는 것:**
- **★ SE 코팅 core-shell *구조* 표현(§4.2)** — **우리가 *없는* 것.** Delaunay 표면추정 → SE 쉘 배치 + 쉘 *박리/재부착 rate(eq 6 detachment)* 로 코어-쉘 입자를 *진짜 구조로* 만든다. 우리는 SE 를 *자유입자(mixture)*로만 시드하고 코팅은 *coverage 메트릭으로 사후 측정* — **코팅 *입자 자체*는 안 만든다.** ⇒ 코팅 표현은 So 가 명백히 앞선 칸(우리 backlog A4 의 정확한 흡수 타깃; §B).
- **★ 코팅의 σ_e *차폐 메커니즘*(Fig 4c/7c)** — "저압서 SE 쉘이 AM-AM 전자접촉을 차폐 → 고압서 박리/관통으로 해제" 라는 *압력-의존 전자 차폐 동역학*을 *발견·정량*했다. 우리 σ_e 의 coverage-shielding 은 *정적*(한 압력)이라 이 *압력축 차폐 해제*는 우리 미보유.
- **소결(sintering)·융착결합 rate(eq 6)** — 우리가 *전혀* 안 가진 물리(MethodsX digest 와 동일). consolidation+detachment dead-band 의 ductile fusion-bond. 우리 `--coh`/adhesion 은 *정적* 점착이지 *rate 융착·박리*가 아니다.
- **AM 응집체-수준 균열(breakable aggregate)** — primary 구의 융착이 끊겨 *fragment* 하는 aggregate breakage 를 모델(우리 Auerbach 는 *접촉응력* 기준이지 *융착-인장-끊김* 기준이 아님 — 정의가 다름; 둘 다 "AM 깨짐" 이나 메커니즘 상이).
→ 즉 **코팅 구조 표현·코팅 σ_e 차폐 메커니즘·소결·응집체 균열의 *깊이*는 So 가, 명시 σ 삼중항·Stage-E 전달면적·MPM morphology·fracture-전달·예측의 *폭*은 우리가** 앞선다. 우리 SOTA 주장은 "*ASSB 복합양극의 구조→전달 σ 삼중항 + 소성 morphology + 설계예측 통합 파이프라인*" 에 한정해 *정확*하다.

---

## 10. 주의/한계 (over-claim 방지)

- **소재가 다르다**: SE = **LPS(Li₂S–P₂S₅, argyrodite 아님)**; AM = **NCM/LiCoO₂ 양극**(E=199·H=11.2 = Cheng [37], So 2021 의 Si 음극과 다름). σ_grain·E_CAM·H 모두 우리와 다름 → **절대 porosity·σ·τ·damage 직접 전이 금지, 방법·추세만**. E_SE=24 가 우리 real-bulk 와 같은 건 우연(LPS 도 sulfide).
- **★ transport 가 명시 σ 가 아니라 τ-추정**: 이온·전자 수송을 **TauFactor τ_SE/τ_AM + percolation volume 으로 *논의*** 하지 **σ_ionic/e/thermal 절대값을 안 푼다.** "코팅이 더 효과적 이온수송", "코팅이 저압서 전자 차폐" 는 *τ·percolation 에서 읽은 정성 결론*이지 σ 수치 비교가 아님 → **우리 Kirchhoff/Holm σ 와 직접 수치 비교 불가**(추세·메커니즘만). σ_e "차폐" 도 *AM-AM 접촉/τ_AM* 증거지 σ_e 값이 아님.
- **rigid sphere + CONTACT 소성 + 응집체 균열**: 입자 *외형* 불변(h_eq 함몰 proxy; SE 쉘 박리는 모델하나 SE *흐름* 없음). **진짜 void-fill SHAPE 흐름 없음** → 우리 MPM morphology 영역 못 다룸(frame[5] 역학 절반). 저자 스스로 "rough spherical AM 제한, 비구형 결론 적용 불가", "코팅 덜 매끈·AM 부분 노출", "AM-SE 면적 과대평가" 인정.
- **★ 코팅은 *SE(이온) 쉘* — A4 carbon·Kang2025 LZO 와 종류 다름**: So 의 코팅은 *이온전도 SE* 쉘이라 **σ_ionic↑·(저압)σ_e↓**. 우리 backlog A4 `se_coating` carbon 은 *전자전도* 쉘(σ_e↑), Kang2025 LZO 는 *절연 패시베이션* 쉘(σ_e↓·계면안정화). **시드 *위치*(AM 표면 쉘)는 직접 차용 가능하나, σ 효과는 코팅 재료별로 정반대** — So 의 "이온 우월" 을 carbon/LZO 코팅에 그대로 전이 금지.
- **도메인 작음(20 µm)**: AM 응집체(5 µm) 대비 작아 **aggregate-수 의존성 배제 못 함**(§4.3 명시). 우리 RVE 크기 논의와 비교 시 주의.
- **damage 정의 = AM-AM 융착 *상대감소율*(eq 9)**: 우리 Auerbach 접촉응력 균열과 *다른 정의*. ~12 %@500 MPa 는 *융착끊김 비율*이지 *깨진 입자 수* 가 아님. 우리 frac_severe(37–40 %)와 직접 동일시 금지(분모·기준 다름).
- **그림 읽은 값(digitized)은 추세만(±)**: percolation volume·τ·damage·fusion-bond 곡선 수치는 Fig 4–7 에서 읽은 근삿값. stated(porosity ~16 %, SE perc >90 %@25 MPa, AM perc 0.3@25→1.0@100 MPa, damage ~12 %@500)와 구분.
- **단일 실현으로 보임**: seed 다중실현·통계 명시 없음("통계적 유의차" 는 곡선 차 기준). 우리 multi-seed 분산과 다름.
- **결과/방법 분리**: 이 논문(JPS)은 *결과(코팅 vs 혼합·tortuosity·damage·percolation)*; **접촉모델 방정식 상세는 동반 MethodsX [31]**(우리 digest `so2022_dem_contact_model_assb_compaction_sintering`). 접촉법칙(rate-h_eq·c_area·c_spring·소결) 수치 인용 시 *그 MethodsX* 우선.

---

## 11. 인용 가능 문장 (deck/paper 용)

- "So et al. (2022, JPS 530)는 SE 를 자유입자(혼합) 또는 SE-코팅-AM(core-shell)으로 모델한 3D DEM 냉간압밀로, **코어-쉘 SE 코팅이 25 MPa 에서 이미 SE percolation >90 % 에 도달(혼합은 360 MPa 필요)** 하여 우월한 이온수송망을 만든다는 것을 보였다 — 단 transport 는 명시 σ 가 아니라 TauFactor tortuosity 로 추정된다."
- "코팅 SE 쉘은 *저압(25 MPa)*에서 AM-AM 전자접촉을 *차폐*하여(Rel. AM percolation 0.3, τ_AM 26) 전자수송을 끊지만, 이 차폐는 200 MPa 초과 고압에서 쉘이 박리·관통되며 사라진다(AM percolation →1.0) — 이는 우리 σ_e 의 *정적* coverage-shielding 이 갖지 못한 *압력-의존* 차폐 동역학이다."
- "두 제조방식(혼합·코팅) 모두 AM 손상이 ~12 %@500 MPa 로 비슷하고 손상이 집전체·SE층 경계 근처에 집중되며(상·하 벽 ~25 %, 중앙 ~5 %), So et al.은 damage 를 AM-AM 융착결합의 상대감소율로 정량화하되 *전달과 연결하지 않는다* — 우리 fracture-aware Holm 은 이 균열을 σ_e 입력으로 직접 사용한다."
- "So 의 SE-코팅 core-shell 표현(Delaunay 표면추정 → SE 쉘 배치 + 박리/재부착 rate)은 우리 backlog A4(`se_coating_interface`)·Kang2025 LZO 코팅의 직접 DEM 선례이나, 그들 코팅은 *이온* 쉘(σ_ionic↑·저압 σ_e↓)이고 carbon/LZO 는 *전자/패시베이션* 쉘 — 시드 위치는 차용하되 σ 효과는 재료별로 정반대다."

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
