# ★★★ 실험검증된 대변형 압밀 DEM — Zunker, Dunatunga, Thakur, Tang, Kamrin · Powder Technology 459 (2025) 120972 (Experimentally validated DEM for large deformation powder compaction: Mechanically-derived contact model and screening of non-physical contacts)

> slug `zunker2025_dem_large_deformation_compaction` · DOI `10.1016/j.powtec.2025.120972` · type `DEM (LAMMPS, MDR 접촉모델 다체 확장) + MPFEM(Abaqus) 검증 + 제약 tableting 실험` · PDF `1-s2.0-S0032591025003675-main.pdf` (+ 보충 영상 `1-s2.0-S0032591025003675-mmc1.mp4` · `…-mmc2.mp4`) · digested `2026-11-12` (**출판본 보강** — 크롭 187 + 영상 프레임 8 = 그림 폴더 195 · 프리프린트 대조 §0-P · 첨언 §16; 초판 = **프리프린트 판** `2026-08-25`) · status ✅
>
> **프리프린트 판 (초판 2026-08-25)** — PDF `5f242057-Experimentntacts.pdf` · *"Preprint submitted to Powder Technology January 3, 2025"* · 21 pp · 부록 A–E · 본문에 DOI 없음 · 텍스트로만 읽음 (그림 0 장 확인).  ⚠ 그 PDF 는 이번 보강의 작업 환경에 없어 **다시 열지 못했다** → 아래의 "프리프린트" 값은 전부 **08-25 카드 기록**이다 (카드가 잘못 읽었을 가능성은 남는다 — §0-P 끝).
>
> **2026-11-12 출판본으로 보강** (1저자 11-12 *"크롭핑해서 다시 litdb 에 보내고 추가로 첨언할 내용 있음 더 추가해서"*) — Powder Technology **459** (2025) **120972** · 받음 2024-12-12 · 수정본 받음 2025-03-14 · 수락 2025-03-25 · 온라인 2025-04-04 · 22 pp · 부록 A–H · © 2025 Elsevier B.V. · 보충 영상 2 편 (mmc1 · mmc2 · **캡션 없음**).
>
> ⚠⚠ **출판본은 프리프린트와 실험 · 표 1 · 입자 수 · 그림 번호 · 부록 구성이 다르다** (§0-P).  아래 §1–§15 의 옛 값은 지우지 않았고, 바뀐 자리 옆에 `▶ 출판본:` 으로 새 값과 쪽 · 식 · 그림 번호를 붙였다.  **인용은 출판본 값으로.**

> ## ★★★ 3부작의 결론편 — **여기에 "실행 가능성" 판정이 다 있다**
> ①(접촉 LAW) → ②(벌크탄성) 을 **실제 다체 DEM 으로 돌린 유일한 편**.  세 가지가 새로 나온다:
> **(a) 반경이 다른 입자쌍 처리(가상 강체평면 배치 스킴)**, **(b) 대변형 DEM 에만 생기는 *비물리 접촉*
> 을 걸러내는 위상 페널티 알고리즘**, **(c) LAMMPS 오픈소스 구현 + MPFEM 대조 + Avicel PH102 실험 검증**.
> 코드 (프리프린트 기록): **`https://github.com/willzunker/lammps`, `mdr` 브랜치, commit `c6159505` (2024-12-03), GPL v2**,
> `sims/` 폴더에 문서와 입력 스크립트 포함.
> `▶ 출판본 §2.3 (p.4):` *"formally implemented into the main repository of the open-source DEM software LAMMPS https://github.com/lammps/lammps. The most up-to-date version of the implementation is maintained on the develop branch … Information on the usage of the MDR model can be found in the LAMMPS documentation."* — 포크 · 커밋 · 라이선스 · `sims/` 언급은 출판본에 **없다** (`txt_p4_lammps_main_repository_and_large_deformation_overlap.png`).
>
> ⚠⚠ **우리에게 결정적인 한 줄** (출판본 §2.2 p.3 에도 그대로): *"we focus on developing and testing a many-interacting particle
> methodology that properly handles **varying radii**, leaving the additional task of considering
> **varying material properties as future work**."*  결론 (§8 p.13) 도 *"Reformulating the many-interacting-particles MDR contact model to accommodate varying material properties would enable the modeling of multi-component formulations."*
> ⇒ **우리 LPSCl + NMC811 2상 복합양극은 이 코드로 오늘 못 돌린다.**  **pure-SE(단일재료)는 돌릴 수 있다.**
> ⇒ **그래서 우리가 해야 할 실험이 딱 하나로 좁혀진다 — §12 를 볼 것.**
> ⇒ **출판본이 더한 것 (§0-P)**: 상대밀도를 x 축으로 한 **두 시험 (RD 0.85 · 0.99) 의 가압 · 제하 곡선**과 잔류 반경응력 (11.5 · 31 MPa) · Particle 1 의 접촉 단위 정량 대조 (변위 · 면적 · 힘 · 부피) · MDR 전체 식 (부록 A) · **민감도 분석 (부록 G)** · 보충 영상 2.

---

## 0. 출판본 (2026-11-12) 한눈에

### 0-1. 서지 (출판본 1 쪽 · 머리글에서 직접 확인)

| 항목 | 내용 |
|---|---|
| 제목 | *Experimentally validated DEM for large deformation powder compaction: Mechanically-derived contact model and screening of non-physical contacts* |
| 저자 · 소속 | William Zunker ᵃ · Sachith Dunatunga ᵃ · Subhash Thakur ᶜ · Pingjun Tang ᶜ · Ken Kamrin ᵃ ᵇ \* — ᵃ MIT 기계공학과 (77 Massachusetts Ave, Cambridge, 02319, MA, USA — 우편번호 인쇄 그대로) · ᵇ UC Berkeley 기계공학과 · ᶜ Vertex Pharmaceuticals (50 Northern Avenue, Boston, 02210) |
| 교신 | Ken Kamrin — *"Corresponding author at: Department of Mechanical Engineering, University of California Berkeley, University Ave, Berkeley, 94720, CA, USA"* · `kkamrin@berkeley.edu` (p.1) |
| 학술지 | **Powder Technology 459 (2025) 120972** · DOI **10.1016/j.powtec.2025.120972** |
| 날짜 | Received 12 December 2024 · Received in revised form 14 March 2025 · Accepted 25 March 2025 · Available online 4 April 2025 |
| 쪽 · 구성 | 22 pp · 본문 §1–§8 · 부록 A (MDR 정식) · B (겹침 상한) · C (반경비 검증) · D (페널티 예) · E (Particle 1 재구성) · F (입도) · G (민감도) · H (보충 자료) |
| 키워드 | discrete element method · large deformation powder compaction · tableting · adhesive elastic–plastic · multi-particle finite element method · normal contact model |
| 자금 · 감사 | NSF-GRFP · IFPRI (Grant ARR-109-01) · Sandia 의 Dan Bolintineanu · Joel Clemmer 가 LAMMPS 구현 도움 |
| 자료 공개 | *"Data will be made available on request."* (p.21) |
| 보충 자료 | 부록 H — 영상 2 편 (`mmc1.mp4` 19.17 s · `mmc2.mp4` 20.23 s · 1280×720 · 30 fps · 소리 없음 · PDF 에 영상 캡션 없음) |
| CRediT (p.13) | Zunker = 초고 · 검토 · 시각화 · 검증 · 소프트웨어 · 방법 · 조사 · 분석 · 자료 · 개념 / Dunatunga = 검토 · 검증 · 소프트웨어 · 방법 · 조사 / Thakur · Tang = 검토 · 자원 · 조사 · 자료 / Kamrin = 검토 · 감독 · 자원 · 방법 · 자금 · 개념 |

### 0-2. 하이라이트 (원문 그대로, p.1)

- *"Large deformation adhesive elastic–plastic powder compaction is studied."*
- *"A recently proposed adhesive elastic–plastic contact model is further developed."*
- *"A new algorithm screens non-physical contacts in large deformation DEM simulations."*
- *"The extended contact model is implemented in LAMMPS and validated with MPFEM."*
- *"Pharmaceutical tableting simulations show strong agreement with experimental data."*

### 0-3. 그래픽 초록 (`graphical_abstract.png`)

두 상자.  위 **"DEM & MPFEM"** = 단분산 14 입자 배치 (처음 · 끝, W · Δ 표시) + σyy/E vs Δ/W (fem · lammps).  아래 **"Pharmaceutical Tableting"** = LAMMPS 4 단계 (die fill · max compaction · upper punch release · ejection) + 축응력 · 반경응력 vs 상대밀도 (그림 14 와 같은 자료).

### 0-4. 이번 보강에서 한 일 (전부 출판본 PDF 와 영상에서)

- **그림 폴더 195 장 = 크롭 187 + 영상 프레임 8** (`litdb/figures/zunker2025_dem_large_deformation_compaction/`): 그림 22 (본문 14 + 부록 8) · 패널 94 · 그래픽 초록 1 · 표 3 · 식 48 (번호 붙은 식 전부) · 근거 문단 19 · 영상 프레임 8.  도구가 잡은 15 장은 전부 여백을 고르게 다시 자름 · 부록 그림 8 · 부록 표 2 는 도구가 라벨 꼴 (`Fig. C.15`) 을 못 읽어 손으로.  전부 열어 봤다.
- **벡터 판독**: 그림 14(a)(b) 의 표지 중심을 눈금으로 환산 (적힌 값 재현 확인 — §3-5) · 그림 6 · 8 · 9 · 10 · 11 의 끝값 · 그림 C.15 의 정점 (§4).
- **영상**: 프레임 8 장 (영상마다 처음 · 최대 압축 · 해제 뒤 · 끝) + 화면 측정 (입자 띠 높이) — §7-V.
- **프리프린트 ↔ 출판본 대조** §0-P · **첨언** §16.

### 0-5. ★ 바뀐 것 가운데 우리에게 가장 큰 셋

1. **실험 자체가 바뀌었다** — 프리프린트 = 한 시험 (축변형 0.4 · 최대 축응력 240 · 반경 147 · 잔류 반경 15 MPa).  출판본 = **두 시험, 상대밀도 0.85 · 0.99** (시료 203.8 · 247.2 mg) · 축 정점 **96.5 · 297.5 MPa** · 반경 정점 **42.5 · 176 MPa** · 잔류 반경 **11.5 · 31 MPa** · 제하 끝 상대밀도 **0.82 · 0.95** (p.10).  240 · 147 · 15 · 0.4 · 5.85 · 3.57 mm · 배출 1.2/1.5 MPa 는 출판본에 **없다**.
2. **표 1 이 통째로 바뀌었다** — E 5 → **8 GPa** · ν 0.4 → **0.3** · Y 19 → **77 MPa** · Δγ 450 → **900 J/m²** · ψb 0.5 → **0.125** · CoR 0.5 → **ηn (점성)** · µt 0.7 → **0.3** · µroll 0.6 → **1.0** · xγ,t 0 → **1.0** · R 96–144 → **139–160 µm** · 입자 20,000 → **10,000** · Δt 계수 0.35 → **0.08** (1.1×10⁻⁸ s) · 겹침 상한 0.75 → **0.95**.  ⇒ 카드의 E/Y 263 · KIc 1.64 · Δt 9×10⁻¹¹ s (LPSCl) 같은 **파생값도 다시** (§0-P).
3. **상대밀도가 보고된다** — 08-25 카드의 *"세 논문 전체에 porosity/relative-density 수치 0 개"* 는 **출판본에 대해 거짓**이다.  축 · 반경 응력이 상대밀도의 함수로 그려지고 (그림 14 · 그림 G.20–G.22), 시작 상대밀도 (실험 0.34 · LAMMPS ≈0.50 [판독]) 와 제하 끝 상대밀도가 적혀 있다.  단 실험 상대밀도는 정점 = 누른 채 · 끝 = 제하 곡선이 끝나는 자리 (축응력 ≈ 0 · 정제가 아직 다이 안인 상태로 읽힌다 [추정 — 원문은 '다이 안' 이라 쓰지 않는다]) 이고, Avicel 입자 안 기공을 포함한 진밀도 기준이다 (§3-4).

---

## 0-P. ★ 프리프린트 ↔ 출판본 대조 (1저자 11-12 지시 2 번)

> 왼쪽 = 08-25 카드가 프리프린트에서 적은 값 (그 PDF 를 이번에 다시 열지 못함).  오른쪽 = 출판본 (쪽 · 식 · 그림 · 표).  판정: **같음 / 바뀜 / 새로 / 없어짐**.  `[카드 산술]` = 이 카드가 계산 · `[판독]` = 그림에서 읽음.

### P-1. 숫자 — 실험

| 항목 | 프리프린트 (카드 08-25) | 출판본 (위치) | 판정 |
|---|---|---|---|
| 시험 수 · 목표 | 1 시험 · 축변형 0.4 | **2 시험 · 상대밀도 0.85 · 0.99** (p.8 §6) | 바뀜 |
| 시료 · 높이 | 충전 높이 5.85 → 압축 뒤 3.57 mm | **초기 시료 질량 203.8 · 247.2 mg** (p.8) · 높이 없음.  [카드 산술] h = 질량 ÷ (1560 kg/m³ × RD × π·(4 mm)²) (다이 지름 8 mm 단면 · 펀치는 *"slightly less than 8 mm"*): 정점 높이 ≈3.06 · 3.18 mm · 상대밀도 0.34 에서 ≈7.64 · 9.27 mm | 바뀜 |
| 가압 · 제하 속도 · 시간 | 압축+해제 1 초 | **변위 제어 · 가압 1 mm/s · 제하 0.25 mm/s** · 다이 벽 윤활 (p.8) · '1 초' 없음 | 바뀜 |
| 최대 축응력 | **240 MPa** @ 축변형 0.4 | **96.5 · 297.5 MPa** (0.85 · 0.99 시험, p.10 — 원문은 *"peak forces are 96.5 MPa and 297.5 MPa"* 로 '힘' 이라 적고 MPa 단위) | 바뀜 |
| 최대 반경응력 | **147 MPa** (측압비 0.61) | **42.5 · 176 MPa** (p.10) · [카드 산술] 측압비 0.44 · 0.59 | 바뀜 |
| 잔류 반경응력 | **15 MPa** | **11.5 · 31 MPa** (p.10) · [카드 산술] 축 정점 대비 0.119 · 0.104 | 바뀜 |
| 제하 끝 | 축변형 0.32 (회복 0.08 · 13.1 %) | **상대밀도 0.82 · 0.95** (p.10) · [카드 산술] 제하 끝 높이 회복 (질량 · 단면 일정) = 0.85/0.82 − 1 = 3.7 % · 0.99/0.95 − 1 = 4.2 % | 바뀜 |
| 시작 상대밀도 | — (카드 추정 ρ₀ 0.25–0.85 · 인용 금지) | **실험 0.34** (p.10) · LAMMPS ≈0.50 [판독 · 그림 14a] | 새로 |
| 배출 축응력 | 실험 1.2 · 시뮬 1.5 MPa | **없음** — µt,wall 을 *"approximately match the experimentally measured ejection force"* 로 맞췄다는 말만 (p.11) | 없어짐 |
| 다이 · 펀치 | Ø8 mm · 틈 위 40–50 · 아래 25–30 µm · 축력 2 + 반경 2 센서 | 같음 (p.8) · 그림 12 치수: 다이 윗면에서 반경 센서까지 10 · 12 mm · 다이 높이 12.75 mm [판독] | 같음 (+ 치수) |
| Avicel PH102 | D50 지름 116 µm · 재료밀도 1560 kg/m³ | 같음 · *"true material density"* · 제조사 자료 (p.8 · p.11) · SEM 그림 13 새로 | 같음 |
| 반경응력 처리 | — | 위 · 아래 센서 평균 · *"post-processing local extrapolation of the axial and radial compaction curves"* ([29] 방식, p.8) | 새로 |

### P-2. 숫자 — DEM (표 1 · 본문)

| 항목 | 프리프린트 | 출판본 (표 1 p.11 · §7) | 판정 |
|---|---|---|---|
| E · ν | 5 GPa · 0.4 (문헌 범위) | **8 GPa · 0.3** (문헌 범위 [29, 58, 59]) | 바뀜 |
| Y | 19 MPa (맞춤) | **77 MPa** (맞춤 · *"falls within the expected range for organic materials [60]"*) | 바뀜 |
| E/Y | 263 [카드 산술] — Part I 검증 범위 6.25–200 **위** | **103.9** [카드 산술] — 범위 **안** | 바뀜 |
| Δγ | 450 J/m² (KIc 경유) | **900 J/m²** (KIc 경유 · 점착은 **입자–입자만**, 입자–벽 점착 없음) | 바뀜 |
| KIc 환산 | 1.64 MPa·m^½ [카드 산술 · E*c = E/(2(1−ν²))] | [카드 산술] 식 (A.11) 의 E*c = E/(1−ν²) = 8.79 GPa 로 **3.98** · 옛 카드 꼴 (두 물체 합성 4.40 GPa) 로 2.81 | 바뀜 |
| ψb | **0.5** (튜닝 · Part II 권장 0.08 의 6.25 배) | **0.125** (튜닝 · 0.08 의 1.56 배 [카드 산술]) | 바뀜 |
| 법선 감쇠 | CoR 0.5 | **ηn = 1e4 ρ Rmean² vp kg/s** (vp = 위 펀치 평균 속도) · 각주 6: *"Damping in the normal direction for the range of compaction speeds tested was shown not to alter the final results."* | 바뀜 |
| 접선 | kt = (2/7) E Rmean · xγ,t 0 · µt 0.7 · µt,wall 0.1 | kt 같은 꼴 · **xγ,t 1.0** (법선 감쇠에 맞춤) · **µt 0.3** · µt,wall 0.1 | 바뀜 |
| 구름 | kroll = (9/4) µroll² E Rmean · γroll 0 · µroll 0.6 | kroll 같은 꼴 · **γroll = ηn** (각주 5 '유사 힘' 꼴) · **µroll 1.0** (*"to obtain a very loose fill"*) | 바뀜 |
| 입자 반경 · 수 | R 96–144 µm (Rmax/Rmin 1.5) · 20,000 | **R 139–160 µm (1.151 [카드 산술]) · 10,000** (§7.2 p.11) · 지름 278–320 µm = D50 116 µm 의 2.4–2.8 배 [카드 산술] | 바뀜 |
| 시간 간격 | Δt = 0.35√(m/k) = 3×10⁻⁸ s | **Δt = 0.08√(m/k) = 1.1×10⁻⁸ s** (m = ρ(4/3)πRmin³ · k = κRmin) · [카드 산술 검산] κ = E/(3(1−2ν)) = 6.67 GPa → 1.10×10⁻⁸ s ✓ · *"subject to change depending on the compact geometry and loading conditions"* | 바뀜 |
| 겹침 상한 (부록 B) | δ^max_geo/R > 0.75 → 0.75R | **0.95R** — *"The non-unique overlap limit of 0.95 is used for all simulations in this work."* (식 B.1 · p.16) | 바뀜 |
| tp | 50 · 유일한 값 없음 | 같음 (p.5 · p.17) | 같음 |
| MPFEM 대조의 LAMMPS ψb | 0.5 | **0.125** — *"set to 0.125 to match the simulation presented in Section 7"* (p.7) | 바뀜 |
| MPFEM 설정 · 비용 | 14 · 12 입자 · E/Y 20 · ν 0.3 · µ 0.5 · C3D10M · 5.5 h (10 proc) vs ≈1 s 직렬 | 같음 (p.6–7) | 같음 |
| 정제 시뮬 초기 충전 | 20,000 입자를 빈 다이에 고르게 → 중력 침강 | 10,000 입자를 **위 · 아래 펀치 사이 빈 공간 전체에 하나씩** · 속도 0 · 비겹침 확인 → 중력 침강 (p.11) · **두 시뮬은 같은 초기 충전에 위 펀치 행정만 다르다** (p.12) — 실험은 질량이 다르다 | 바뀜 |
| 입도 (부록) | 부록 E · shifted Weibull λ 6 · k 0.69 · s 4.5 · 3.2 배 | **부록 F** · 같은 값 (식 F.1 · F.2) | 번호만 바뀜 |

### P-3. 식

| 식 | 프리프린트 (카드) | 출판본 | 판정 |
|---|---|---|---|
| (1)–(4) 강체 평면 배치 | 카드 §4 | 같은 꼴 (p.4) | 같음 |
| (5)–(8) · (10) · (11) 페널티 | 카드 §5-2 | 같은 꼴 (p.5–6) | 같음 |
| (9) 시그모이드 | p̂ = 1/(1 + exp(−tp(α/π − 1/2))) | **인쇄본은 `exp(−tp α/π − 1/2)` — 안쪽 괄호 없음** (`eq_09_sigmoid_penalty.png`).  그대로면 α ≥ 0 에서 늘 p̂ ≥ 0.62 [카드 산술] 이라 그림 D.16a · 각주 9 (*"approximately 0.4 ≤ α/π ≤ 0.6"*) 와 맞지 않는다 → 뜻은 카드 꼴 (괄호 있음) | 인쇄 오류 (뜻 같음) |
| 부록 A 전체 (A.1–A.34) | 카드는 Part I · II 식 번호로 인용 | **이 논문 안에 전부 다시 실림** (p.13–16) · 표 A.2 기호 사전 | 새로 |
| (A.14) 경화 곡선 | pY = Y(1.75 e^{−4.4δ/R} + 1) (Part I 식 16) | 같음 | 같음 |
| (A.22) 항복 변위 | Part I 카드 식 (41): 지수 −4.4 δY/R | **인쇄본 지수 −1.1 δY/R** — (A.14) 와 4 배 차 · 설명 없음 [미확인] | 차이 (원인 미확인) |
| (B.1) 겹침 상한 | 0.75 | **0.95** | 바뀜 |
| (F.1) · (F.2) 입도 | 카드 §8 서술 | 식으로 실림 · 지수 안 변수가 x (앞은 size) — 인쇄 그대로 | 새로 |

### P-4. 그림 번호 · 절 구성

| 프리프린트 번호 (카드 §7-0) | 출판본 번호 | 무엇 |
|---|---|---|
| 1–7 | 1–7 | 같은 주제 (그림 7 = 형상 재구성) |
| — | **8 · 9 · 10 · 11** | **새로**: Particle 1 의 접촉별 변위 · 면적 · 힘 · 부피 (FEM ↔ LAMMPS) |
| 8 | **12** | 압축 시험기 |
| — | **13** | **새로**: Avicel PH102 SEM |
| 9 | **14** | 정제 실험 ↔ 시뮬 — x 축이 **축변형 → 상대밀도** |
| C.10 | **C.15** | 반경비 대조 |
| D.11 | **D.16** | 페널티 예 |
| — | **E.17 · E.18 · 표 E.3** | **새로**: Particle 1 접촉 다섯 방향 · 13 번 접촉 놓침 · 최소 부피 타원체 |
| E.12 | **F.19** | 입도 |
| — | **G.20 · G.21 · G.22** | **새로**: 민감도 (축 · 반경 · 비) |
| — | **표 A.2** | **새로**: 기호 사전 |

절: 출판본 §2.1 *"Review of the MDR contact model"* (특징 6 개) · §5.2 *"MPFEM"* (Particle 1 정량) · 부록 A · E · G · H 가 새로.  프리프린트 부록 A 의 내용은 카드에 기록이 없다 [미확인].

### P-5. 결론 · 주장 문장

| 주제 | 프리프린트 (카드) | 출판본 | 판정 |
|---|---|---|---|
| 실험 대조 | *"축·반경 응력–변형 곡선 재현"* | 초록: *"Good agreement is observed … for the axial and radial stress measurements **as a function of relative density**. Notably, the simulation is able to predict a similar residual radial stress after release of the axially confining pressure to that of the experiment."* · 본문은 **한정**: RD **0.6–0.8 위**에서 일치 · *"After a relative density of 0.8 the LAMMPS simulation underpredicts the axial stress"* (벌크 전이가 날카로움 — 각주 7) · 정점 근처 재합류 · 제하 두 경우 일치 · 잔류 반경응력은 0.99 가 0.85 보다 낫다 (p.12) | 바뀜 (더 정량 · 더 한정) |
| 형상 재구성 | MPFEM 입자의 *"all five of the contact patches"* 가 재구성에 나타남 | Particle 1 의 FEM 접촉 **9 개 가운데 13 번을 LAMMPS 가 못 잡음** — *"inability of the MDR contact model, and classical DEM more generally, to capture anisotropic deformations induced by shear"* (p.8 · 부록 E.2) · 각주 2: *"should be employed for predominately isotropic loading conditions"* | **바뀜 (약해짐)** |
| 단일 재료 | §2.2 *"varying material properties as future work"* | 같은 문장 + 결론의 향후 과제 (p.13) | 같음 |
| Y 맞춤 문장 | *"No reports … could be located, necessitating a fitting of Y"* | *"No reports in the literature on Avicel PH102 give a yield stress value, necessitating a fitting of Y, however, the selected value falls within the expected range for organic materials [60]."* | 문구 바뀜 |
| ψb 튜닝 문장 | *"tuned to trigger the high confinement bulk response stiffening in alignment with the experimental results"* | 같음 (p.11) | 같음 |
| 배터리 | 서론 refs 11, 12 (Meyer · Abdollahifar) · 결론 캘린더링 | 서론 **[9, 10]** · 결론 **[65–67]** (Giménez 2019 · Ge 2022 · Sonzogni 2024 — DEM 캘린더링) | 번호 바뀜 · 결론 인용 셋 |
| 민감도 | 압력 스윕 없음 · 프로토콜 하나 | **부록 G**: 1000 입자 · 8 변수 ±10 · ±20 % · 상대밀도 0.9 까지 · 잔류응력 경향 | 새로 |

### P-6. 08-25 카드의 판정 가운데 출판본으로 바뀌는 것

- ~~*"⚠ 상대밀도·porosity 한 번도 보고되지 않음"*~~ (§3-1 · §3-4 · §11 · §13-1 ⑥ · §15) → **출판본은 상대밀도를 보고한다** (정점 = 누른 채 · 끝 = 제하 곡선 끝 · 진밀도 기준 — §3-4).  *"porosity 는 비교 불가"* 는 **"단위계는 같아졌지만 재료 · 기준이 달라 절대값 전이는 여전히 불가"** 로 바꾼다.
- ~~*"압력 스윕이 없다 — 프로토콜 하나"*~~ → 정점이 다른 두 시험 (96.5 · 297.5 MPa) + 부록 G 민감도.  여전히 압력 '스윕' (여러 정점의 Heckel) 은 아니다.
- ~~*"E/Y = 263 — Part I 검증범위 위"*~~ → 103.9, 범위 안.
- ~~*"ψb 0.08 → 0.5 로 6.25× 튜닝"*~~ → 0.125 (1.56×).  튜닝이라는 사실은 그대로.
- ~~*"Δγ 450 → 우리 W_ad 의 400×"*~~ → 900 J/m² → **813×** [카드 산술].
- ~~*"MPFEM 입자의 접촉패치 5개 모두 재구성"*~~ → 9 개 중 1 개 놓침 (비등방 변형) — 층 (2.75) 의 **한계가 원문으로** 생겼다 (§6).
- ~~*"20,000 입자 · 우리 real_14 와 같은 등급"*~~ → 10,000.
- ~~*"Zunker 규칙으로 우리 SE Δt ≈ 9×10⁻¹¹ s"*~~ → 출판본 계수 0.08 로 **2.0×10⁻¹¹ s** [카드 산술] (4.4 배 짧다).
- ~~*"코드 = willzunker/lammps mdr 브랜치"*~~ → LAMMPS 본 저장소 develop 가지 (§9).
- ⚠ **이 카드가 프리프린트를 잘못 읽었을 가능성**: 위 변화가 너무 많아 *"카드 오독"* 인지 *"논문 수정"* 인지 PDF 없이는 가를 수 없다.  다만 (i) 08-25 카드의 Δt 검산 (3×10⁻⁸ s 재현) · KIc 환산이 프리프린트 값끼리 맞물리고 (ii) 수정본 접수일 (2025-03-14) 이 프리프린트 날짜 (2025-01-03) 뒤라, **논문이 수정된 것**으로 보는 것이 자연스럽다 [추정].

---

## 1. 한 줄 요약

Part I·II 의 MDR 접촉모델을 **다체(many-interacting)** 로 확장해 **LAMMPS 에 구현·공개**하고,
**MPFEM(다입자 유한요소)** 으로 접지검증한 뒤 **제약 정제(tableting)** 실험 — Avicel PH102(미결정
셀룰로오스), Ø8 mm die, 축변형 0.4, 최대 축응력 240 MPa — 의 **축·반경 응력–변형 곡선을 재현**한다.
`▶ 출판본:` 실험은 **상대밀도 0.85 · 0.99 두 시험** (축 정점 96.5 · 297.5 MPa) 이고 곡선은 **상대밀도의 함수**로 대조한다 (그림 14).  일치는 상대밀도 **0.6–0.8 위**에서 · 0.8 뒤 축응력 과소 · 제하 · 잔류 반경응력 (0 이 아님) 재현.
부수로 **대변형 DEM 고유 결함**(막고 있는 입자를 *관통해* 생기는 기하학적 가짜 접촉)을 진단하고
**삼중항(triplet) 위상 페널티** 로 걸러낸다.  또한 **변형된 입자 형상을 재구성**해 FEM 과 비교한다
(`▶ 출판본:` 접촉별 변위 · 면적 · 힘 · 부피까지 정량 대조 · 9 접촉 중 1 개 놓침 — §6).

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **William Zunker**ᵃ, **Sachith Dunatunga**ᵃ, **Subhash Thakur**ᶜ, **Pingjun Tang**ᶜ, **Ken Kamrin**\*ᵃᵇ |
| 소속 | ᵃMIT 기계공학 · ᵇ**UC Berkeley 기계공학** · ᶜ**Vertex Pharmaceuticals** (50 Northern Ave, Boston) |
| 교신 | `kkamrin@berkeley.edu` |
| 저널 | **Powder Technology** — 이 PDF 는 **프리프린트 판**("Preprint submitted to Powder Technology January 3, 2025"), 21 pp incl. Appendix A–E · `▶ 출판본:` **459 (2025) 120972** · 22 pp · 부록 A–H (§0-1) |
| DOI | **n/a** (프리프린트 판에 미기재).  ⚠ 인용 시 출판판 확인 필요 · `▶ 출판본:` **10.1016/j.powtec.2025.120972** (확인함) |
| 코드 | **github.com/willzunker/lammps**, `mdr` 브랜치, **commit c6159505 (2024-12-03)**, **GPL v2**, `sims/` 에 문서+예제 · `▶ 출판본:` **github.com/lammps/lammps 본 저장소 · develop 가지 · LAMMPS 문서** (§2.3 p.4) — 라이선스 표기 없음 |
| 소재 | **Avicel PH102 (미결정 셀룰로오스, MCC)** — 연성 제약 부형제.  ⚠ **황화물 SE·NMC 아님** · `▶ 출판본:` SEM (그림 13) — 입자가 **불규칙한 판 · 섬유 조각** [관찰] · 입도는 Vertex 제공 실측 (부록 F) |
| 자금 | NSF GRFP + IFPRI ARR-109-01.  Sandia 의 **Dan Bolintineanu · Joel Clemmer** 가 LAMMPS 구현 지원 (출판본 같음) |
| 배터리 언급 | 서론에 **"전극 캘린더링"** 을 응용 예로 명시(refs 11,12 Meyer/Abdollahifar), 결론에서 **"배터리 제조 캘린더링에 적용 가능"** 이라 씀 — **실제 배터리 런은 0건** · `▶ 출판본:` 서론 [9, 10] · 결론 [65–67] (Giménez 2019 · Ge 2022 · Sonzogni 2024) — 여전히 배터리 런 0 |

---

## 3. 핵심 수치

> ⚠ (프리프린트 판) 그림 이미지 미확인(텍스트 추출만) → **digitized 값 0개**.  아래 3-1–3-4 는 전부 **stated** (프리프린트).
> ⚠ ③의 graphical abstract 페이지에 LaTeX base64 잡음이 섞여 있어 본문 페이지만 읽었다.
> `▶ 출판본:` 3-1′ · 3-2′ · 3-5 를 새로 넣었다 (적힌 값 + [판독]).

### 3-1. 실험 (Avicel PH102 compaction simulator) — 프리프린트 기록

| 항목 | 값 | 비고 |
|---|---|---|
| die 직경 | **8 mm** | 상·하 펀치 평면, 클리어런스 상 40–50 µm / 하 25–30 µm (출판본 같음) |
| 계측 | 상·하 펀치 **축력 센서** + die 내면 **반경압력 센서 2개**(상/하) | 출판본 같음 · 반경응력 = 두 센서 평균 |
| 분말 | **Avicel PH102 (MCC)**, **D50 지름 116 µm**, 재료밀도 **1560 kg/m³** | 연성(ductile) 거동 (출판본 같음) |
| 초기 충전높이 | **5.85 mm** | `▶ 출판본: 없음` (시료 질량 203.8 · 247.2 mg 로 바뀜) |
| 압축 후 높이 | **3.57 mm** | ⇒ **부피비 0.6103**, 공칭 축변형 **0.390 ≈ 0.4** (**DERIVED** from stated heights) · `▶ 출판본: 없음` |
| 압축+해제 시간 | **1 초** | `▶ 출판본: 없음` — 가압 1 mm/s · 제하 0.25 mm/s (p.8) |
| **최대 축응력** | **240 MPa** @ 축변형 0.4 | ★ 우리 300 MPa 와 **같은 차수** · `▶ 출판본: 96.5 · 297.5 MPa` (p.10) |
| **최대 반경응력** | **147 MPa** | ⇒ 측압비 147/240 = **0.61** (**DERIVED**) · `▶ 출판본: 42.5 · 176 MPa` (측압비 0.44 · 0.59 [카드 산술]) |
| 축 곡선 형태 | 0–0.2 구간 **bi-linear**([0,0.05],[0.05,0.2]) → 0.2 초과 **점진적 stiffening** | ★ = Part II 의 3구간 구조가 거시적으로 보이는 것 · `▶ 출판본:` *"gradually increase in stiffness as the relative density rises"* (p.10) |
| 제하 종료 변형 | **0.32** ⇒ **탄성회복 0.08** | 압축체 높이 대비 springback **13.1 %** (**DERIVED**) · `▶ 출판본:` 제하 끝 **상대밀도 0.82 · 0.95** |
| **잔류 반경응력** | **15 MPa** | ★ 해제 후에도 남음 — 캡핑/래미네이션 결함의 원인 · `▶ 출판본: 11.5 · 31 MPa` |
| 배출(ejection) 축응력 | 실험 **1.2 MPa** / 시뮬 **1.5 MPa** | `▶ 출판본: 없음` |
| ⚠ **상대밀도·porosity** | **한 번도 보고되지 않음** | ★★ **세 논문 전체에 porosity/relative-density 수치 0개** · `▶ 출판본: 거짓이 됨` — §3-1′ · §3-4 |

### 3-1′. 실험 — 출판본 (§6 p.8 · p.10 · 그림 14 · `txt_p8_experiment_die_rates_rd_two_tests.png` · `txt_p10_measured_peaks_residual_radial_stress.png`)

| 항목 | RD 0.85 시험 | RD 0.99 시험 | 출처 |
|---|---|---|---|
| 초기 시료 질량 | 203.8 mg | 247.2 mg | p.8 (stated) |
| 시작 상대밀도 | 0.34 | 0.34 | p.10 (stated) · [판독] 0.340 |
| 정점 상대밀도 (목표) | 0.85 | 0.99 | p.8 (stated) · [판독] 표지 끝 0.849 · 0.996 |
| 정점 축응력 | **96.5 MPa** | **297.5 MPa** | p.10 (stated) |
| 정점 반경응력 | **42.5 MPa** | **176 MPa** | p.10 (stated) |
| 제하 끝 상대밀도 | **0.82** | **0.95** | p.10 (stated) · [판독] 0.817 · 0.949 |
| 잔류 반경응력 | **11.5 MPa** | **31 MPa** | p.10 (stated) |
| 측압비 (정점 반경 ÷ 정점 축) | 0.44 | 0.59 | [카드 산술] |
| 잔류 반경 ÷ 정점 축 | 0.119 | 0.104 | [카드 산술] |
| 제하 끝 높이 회복 (RD 정점 ÷ RD 끝 − 1) | 3.7 % (적힌 값) · 3.9 % ([판독]) | 4.2 % (적힌 값) · 5.0 % ([판독]) | [카드 산술] · 질량 · 다이 면적 일정 가정 |
| 정점 정제 높이 | ≈3.06 mm | ≈3.18 mm | [카드 산술] 질량 ÷ (1560 × π·4²) ÷ RD |

- 측정 조건: 변위 제어 · 가압 1 mm/s · 제하 0.25 mm/s (*"chosen to be slow so as to minimizes any effects of air"*) · 다이 벽 윤활 · 축응력 = 위 펀치 축력 ÷ 펀치 면 면적 (각주 4) · 반경응력 = 위 · 아래 센서 평균 · 곡선은 [29] 방식의 국소 외삽 후처리.
- ⚠ **상대밀도 정의**: *"RD = ρt/ρ, where ρt is the bulk density of the tablet"* · ρ = **진밀도 1560 kg/m³**.  정점은 '누른 채', 제하 끝은 '제하 곡선이 끝나는 자리' 이다 — 원문은 *"nonlinear unloading curves that terminate at relative densities of 0.82 and 0.95"* (p.10) 라고만 쓰고, 정제가 그때 다이 안이라는 것은 읽기 [추정].  배출 뒤 정제 밀도는 없다.
- ⚠ 시작 상대밀도 0.34 ↔ LAMMPS ≈0.50 의 차이는 *"intraparticle porosity of Avicel PH102"* 때문이라고 저자가 쓴다 (p.12) — 실험 상대밀도에는 **입자 안 기공**이 들어 있고 시뮬 입자는 꽉 찬 구다.

### 3-2. DEM 파라미터 (프리프린트 판 표 1 전문 전재 — 출판본 Table 1 은 §3-2′)

| 법선 (MDR) | 접선 (LH) | 롤링 (SDS) | 입자 |
|---|---|---|---|
| **E = 5 GPa** (문헌범위) | k_t = **(2/7)·E·R_mean** [N/m] | k_roll = **(9/4)·µ_roll²·E·R_mean** | R_min = **96 µm** |
| **ν = 0.4** (문헌범위) | x_γ,t = **0.0** (접선 감쇠 off) | γ_roll = **0.0** | R_max = **144 µm** |
| **Y = 19 MPa** ⚠ **피팅** | µ_t = **0.7** ⚠ 튜닝 | µ_roll = **0.6** ⚠ 튜닝 | ρ = **1560 kg/m³** |
| **Δγ = 450 J/m²** (K_Ic 경유) | µ_t,wall = **0.1** ⚠ 튜닝 | | N = **20,000** |
| **ψ_b = 0.5** ⚠ **튜닝** | | | |
| **CoR = 0.5** (문헌범위) | | | |

- **E/Y = 263** (**DERIVED**) — Part I 검증범위 6.25–200 의 **위**(상한 없음이므로 사용 가능).  `▶ 출판본:` 103.9 (범위 안).
- **Δγ 조달법**: `K_Ic = √(2 Δγ E*_c)` 로 역산 (K_Ic 가 더 흔히 측정되므로).
  ⇒ E*_c = E/(2(1−ν²)) = 2.976 GPa → **K_Ic = 1.64 MPa·m^½** (**DERIVED**).  `▶ 출판본:` 식 (A.11) 이 E*c = E/(1−ν²) 로 정의 → Δγ 900 · E 8 GPa · ν 0.3 이면 **3.98 MPa·m^½** [카드 산술] (옛 꼴 두 물체 합성이면 2.81).
  ★★ **Δγ = 450 J/m² 는 열역학 표면에너지가 아니라 소성소산까지 럼핑한 *유효 파괴에너지*** 다.
  우리 DFT `W_ad = 1.107 J/m²` 를 **이 자리에 그대로 넣으면 안 된다** (400× 차이).  `▶ 출판본:` 900 J/m² → **813×** [카드 산술].
- **Y 는 문헌값이 없어 피팅**했다고 저자가 명시 (*"No reports in the literature on Avicel PH102 yield
  stress could be located, necessitating a fitting of Y"*), 다만 유기물 기대범위 안이라고 방어.  `▶ 출판본 문구:` *"No reports in the literature on Avicel PH102 give a yield stress value, necessitating a fitting of Y, however, the selected value falls within the expected range for organic materials [60]."*
- **시간스텝**: `Δt = 0.35·√(m/k)`, `m = ρ(4/3)πR_min³`, `k = κ·R_min` → **Δt = 3×10⁻⁸ s**.
  ✅ **우리가 검산했다**: κ = E/(3(1−2ν)) = 8.333 GPa, m = 5.78×10⁻⁹ kg, k = 8.0×10⁵ N/m
  → 0.35√(m/k) = **2.98×10⁻⁸ s** = 논문값 (**DERIVED 검증 일치**).  `▶ 출판본:` `Δt = 0.08·√(m/k)` → **1.1×10⁻⁸ s** · 검산: κ = 6.667 GPa · m = 1.755×10⁻⁸ kg · k = 9.27×10⁵ N/m → 1.10×10⁻⁸ s ✓ [카드 산술].
- **속도 무관 주장**: *"Specific compaction speeds and loading sequence timings are omitted because of the
  rate-independent nature of the defined contact models"* + 입자 관성이 평균 접촉력보다 충분히 작아
  **준정적**임을 확인.  ⚠ **총 스텝수·벽시계 시간은 미보고 → n/a**.  (출판본 같음 · 각주 6 추가.)

### 3-2′. DEM 파라미터 — 출판본 Table 1 (p.11 · `tab_1.png`)

| 법선 (MDR) | 접선 (LH) | 구름 (SDS) | 입자 |
|---|---|---|---|
| **E = 8 GPa** (문헌 범위) | kt = **(2/7) E Rmean** N/m | kroll = **(9/4) µroll² E Rmean** N/m | Rmin = **139 µm** |
| **ν = 0.3** (문헌 범위) | xγ,t = **1.0** | γroll = **ηn** | Rmax = **160 µm** |
| **Y = 77 MPa** ⚠ 맞춤 | µt = **0.3** ⚠ 튜닝 | µroll = **1.0** ⚠ 튜닝 | ρ = **1560 kg/m³** |
| **Δγ = 900 J/m²** (KIc 경유) | µt,wall = **0.1** ⚠ 튜닝 | | N = **10,000** (§7.2) |
| **ψb = 0.125** ⚠ 튜닝 | | | |
| **ηn = 1e4 ρ Rmean² vp kg/s** | | | |

- 각 값의 근거 문장 = `txt_p11_parameter_selection_fitted_tuned_timestep.png` (§7.1): E · ν · Δγ = 문헌 범위 [29, 58, 59] · Y = 맞춤 · ψb = *"tuned to trigger the high confinement bulk response stiffening in alignment with the experimental results"* · µt = *"best match the experimental macroscopic stress evolutions in forward loading with particular focus on the dense high confinement regime"* · µt,wall = 배출력 · µroll = *"mostly influences the relative density just after die-filling … 1.0 to obtain a very loose fill"*.
- 시간 간격 1.1×10⁻⁸ s = *"general guide … subject to change depending on the compact geometry and loading conditions, which can change the effective stiffness due to the nonlinear nature of the contact model"*.

### 3-3. MPFEM 대조 (§4) — 출판본과 같음 (ψb 만 다름)

| 항목 | 값 |
|---|---|
| 케이스 | **단분산 14 입자** / **삼분산 12 입자**(소 6 / 중 2 / 대 4; 중 대비 ±20 % 반경) |
| 재료 | E/Y = **20**, ν = **0.3** (Part II 와 동일) |
| 구속 | **6 강체벽**, 상자 중심으로 등속 Δ 만큼 접근 (kinematic) |
| 접촉 | 법선 hard, 접선 마찰 **µ = 0.5** |
| 요소 | **C3D10M** (10절점 modified quadratic tetra), Abaqus **dynamic explicit**, 감쇠 없음 |
| LAMMPS 재현 | 입자 좌표·반경을 **정확히 복제**, µ_t = 0.5, x_γ,t = 0, **ψ_b = 0.5** · `▶ 출판본: ψb = 0.125` (*"to match the simulation presented in Section 7"*) · 점착 끔 · kt ∝ E Rmean |
| 결과 | σ_xx, σ_yy, σ_zz 세 방향 모두 **양호 일치**; 단분산 최대변위에서 **σ_zz 만 약간 과대예측** · `▶ 출판본 [판독 · 그림 6 끝값]`: 단분산 σxx/E 0.337 ↔ 0.358 · σyy 0.399 ↔ 0.397 · σzz 0.464 ↔ 0.542 (+17 %) / 삼분산 σxx 0.411 ↔ 0.481 · σyy 0.527 ↔ 0.627 · σzz 0.595 ↔ 0.625 (FEM ↔ LAMMPS) — 삼분산도 끝에서 LAMMPS 가 높다 (본문은 *"Good agreement"*) |
| 변위 범위 | `▶ 출판본 [판독]`: Δ/W 단분산 0–0.30 · 삼분산 0–0.33 |
| **비용** | **MPFEM 5.5 시간** (10 프로세서, 24-core 3.2 GHz) **vs DEM ≈ 1 초** (같은 기계, **직렬**) |
| ⇒ 속도비 | **≈ 2×10⁴ 배**(벽시계), **≈ 2×10⁵ 배**(코어-시간) (**DERIVED**) |
| 응력 정의 | 벽 법선 힘 합 ÷ *"available wall contact area, taking into consideration their movement"* (p.7) |

### 3-4. ★ 상대밀도 — 프리프린트: **보고되지 않음** / `▶ 출판본: 보고됨`

- (프리프린트 기록) 세 논문 어디에도 porosity·상대밀도가 **없다**.  검증 타깃이 **σ_axial(ε)·σ_radial(ε)** 이지 porosity(P) 가 아니다.
- (프리프린트 기록) 유일한 hard 제약 = **부피비 0.6103** (die 가 강체이므로 높이비 = 부피비).
- (프리프린트 기록) **DERIVED 범위**: N=20,000, R∈[96,144] µm, die 부피 π(4 mm)²×5.85 = **294.05 mm³**
  → 초기 상대밀도 ρ₀ = 20000·(4/3)π⟨R³⟩/294.05 mm³ ∈ **[0.25 (R̄=96), 0.85 (R̄=144)]** — 너무 헐겁다.
  마찰(µ_t 0.7, µ_roll 0.6) 침전이 물리적 RLP(ρ₀ ≈ 0.55–0.60)라면 **최종 ρ = ρ₀/0.6103 ≈ 0.90–0.98**
  (= porosity **2–10 %**).  ⚠ **가정 기반 추정 — 논문 수치 아님, 인용 금지.**
- (프리프린트 기록) ⇒ **압력은 우리 영역에 닿는다(240 vs 300 MPa).  porosity 는 비교 불가.**
- `▶ 출판본`: **상대밀도가 x 축**이다 (그림 14 · G.20–G.22).  실험 시작 0.34 → 정점 0.85 · 0.99 → 제하 끝 0.82 · 0.95 (§3-1′).  LAMMPS 시작 ≈0.50 [판독].  부록 G 의 민감도는 상대밀도 0.9 까지.  ⇒ 08-25 의 추정 범위는 **출판본 값으로 대체** (옛 추정은 프리프린트 형상으로 한 것이라 그대로 둔다).
- ⇒ **압력은 우리 영역에 닿는다** (출판본 0.99 시험 축 정점 **297.5 MPa** ≈ 우리 300 MPa).  **기공은 '같은 단위' 로 적혔지만 비교 기준이 다르다** — Avicel 진밀도 기준 (입자 안 기공 포함) · 정점 (누른 채) 과 제하 끝 값 · 재료가 연성 유기물 → 우리 LPSCl 기공 (진밀도 1.64 g/cm³ 기준 · 랩 표준 순수 SE 10–13 %) 과 **절대값을 나란히 놓지 않는다**.

### 3-5. `▶ 출판본` Fig 14 판독 (벡터 표지 중심 → 눈금 환산 · `fig_14a.png` · `fig_14b.png`)

> 방법: 그림 14(a)(b) 의 표지는 벡터 (실험 = 파란 원 2,130 · 1,689 개 · LAMMPS = 노란 네모 665 개씩).  각 축 틀의 주 눈금 (x 0.3–1.0 · y 0–300 MPa) 으로 1 차 환산 (잔차 < 2×10⁻⁵).  **검증**: 적힌 값을 재현 — 시작 0.340 (0.34) · 축 정점 297.1 (297.5) · 제하 끝 0.817 · 0.949 (0.82 · 0.95) · 반경 정점 175.8 (176) · 잔류 11.7 · 31.1 (11.5 · 31) MPa.  표지 지름 만큼 (정점에서 ≈0.4 MPa) 낮게 읽힌다.

| 양 | 실험 (적힌 값) | LAMMPS [판독] | LAMMPS − 실험 |
|---|---|---|---|
| 시작 상대밀도 | 0.34 | **0.497** | +0.16 |
| 축 정점 · 0.99 시험 | 297.5 MPa (RD 0.996 [판독]) | **278.0 MPa** (RD 0.996) | −6.6 % |
| 축 정점 · 0.85 시험 | 96.5 MPa (RD 0.849 [판독]) | **79.9 MPa** (RD 0.847) | −17 % |
| 반경 정점 · 0.99 | 176 MPa | **193.2 MPa** | ≈ +10 % |
| 반경 정점 · 0.85 | 42.5 MPa | **52.3 MPa** | +23 % |
| 잔류 반경 · 0.99 | 31 MPa | **36.0 MPa** | +16 % |
| 잔류 반경 · 0.85 | 11.5 MPa | **20.8 MPa** | +81 % |
| 제하 끝 상대밀도 · 0.99 | 0.95 | **0.939** | −0.011 |
| 제하 끝 상대밀도 · 0.85 | 0.82 | **0.826** | +0.006 |
| 측압비 정점 · 0.99 / 0.85 | 0.59 / 0.44 | **0.69 / 0.65** | LAMMPS 가 옆으로 더 민다 |
| 제하 끝 높이 회복 · 0.99 / 0.85 | 4.2 / 3.7 % (적힌 값) | **6.0 / 2.5 %** | [카드 산술] |

- 저자 문장과 맞는다: 축응력 0.8 위 과소 → 정점 근처 재합류 · 반경은 0.6 위 일치 · 잔류 반경응력은 0.99 가 0.85 보다 낫다 (+16 % ↔ +81 %).
- [판독 · 상대밀도 0.02 구간마다 가압 가지의 위 포락선 비 LAMMPS/실험] 축: 0.90 (RD 0.72–0.76) → **0.74 (RD 0.92–0.94 · 최저)** → 0.94 (RD 0.98–0.996) · 반경: 1.00 (RD 0.68–0.70) → **1.23 (RD 0.82–0.84 · 최고)** → 1.04–1.10 (RD 0.94–0.996).  ⇒ LAMMPS 는 가압 중 **옆으로 더 밀고 (반경 ↑) 위로는 덜 민다 (축 ↓)**.
- ⚠ 두 LAMMPS 시뮬은 **같은 초기 충전** (10,000 입자) 에 위 펀치 행정만 다르다 — 실험은 시료 질량이 다르다.  LAMMPS 상대밀도를 어떻게 셌는지 (입자 부피 합 ÷ 펀치 사이 부피?) 는 원문에 없다 [미확인].

---

## 4. 방법 ★ (1) — 다체 확장: 가상 강체평면 배치 스킴 (§2.2)

Part I·II 는 **"입자 1개 + 강체 평면들"** 만 다뤘다.  다체로 가는 방법이 **놀랍도록 단순**하다 (출판본 p.3 같음 · `fig_1.png` · `txt_p3_varying_material_properties_future_work_tradeoffs.png`):

1. 접촉쌍 {i, j} 사이에 **가상의 강체평면**을 하나 놓는다.
2. **양쪽에서 각각** "강체평면과의 접촉"으로 힘을 계산한다 — `F^i_ij` (j 를 무시), `F^j_ij` (i 를 무시).
3. **평균**한다: `F_ij = (F^i_ij + F^j_ij)/2`.

**평면 위치 = 겹침 δ 를 δ_i + δ_j 로 어떻게 쪼개나** (eq 1–4 · `eq_01…png` – `eq_04…png` · 그림 2 = `fig_2a.png` · `fig_2b.png`):
```
전방재하 (δ = δ_max) — 기하 교차점에 놓는다:
   δ^max_i,geo = (δ_max² − 2 R_j δ_max) / (2(δ_max − R_i − R_j))            … (3)
   δ^max_j,geo = (δ_max² − 2 R_i δ_max) / (2(δ_max − R_i − R_j))            … (4)
제하 — 두 쪽이 동시에 0 힘에 닿도록 소성변위로 선형보간:
   δ_i = δ^max_i,geo − [(δ^p_i − δ^max_i,geo)/(δ^p − δ_max)]·(δ − δ_max)     … (1)
   δ_j = (i↔j 대칭)                                                          … (2)
극단 겹침 캡 (App B):  δ^max_geo/R > 0.75 이면 0.75R 로 자르고 나머지를 반대쪽에 배분
   ▶ 출판본 (B.1) p.16: 상한 0.95 — "The non-unique overlap limit of 0.95 is used for all simulations in this work."
```
**정당화**: 완전소성에서 접촉면적 ≈ 기하 교차면적이므로, 평면을 기하 교차면에 놓으면 **양쪽 면적이
근사적으로 같아진다**.  출판본: 제하 보간 = *"placing the rigid flat at the location where the deformed profiles touch"* (그림 2b).

★★ **우리에게 결정적인 성질 (DERIVED)**:
- 동일 반경이면 `δ_i,geo = δ_j,geo = δ/2` → ★ **Part I 의 "구-구 δ = 2× 구-평면 δ" 환산이 코드로 확인된다.**
- **크기가 다르면 작은 입자가 겹침을 거의 다 먹는다**: `δ_i,geo/δ ≈ R_j/(R_i+R_j)`.
  우리 12:1(AM_P 6 µm : SE 0.5 µm)이면 **SE 가 겹침의 92 %, AM 이 8 %** 를 가진다.
  ⇒ **AM 은 사실상 강체처럼 행동하고 SE 만 소성한다** — 우리 `AM-freeze scaffold` 가정이 이 스킴 안에서
  **자동으로 나온다** (Mesarović–Fleck 2000 의 dissimilar 결과와도 정합).
  ⚠ (2026-11-12 첨언) 이 92 % 는 **같은 재료**일 때의 기하 배분이다 — 재료가 다르면 (AM 이 훨씬 단단하면) 배분은 경도도 따라야 하는데, 출판본은 그 일을 *"future work"* 로 남겼다 (§16 (나)).
- **트레이드오프 (저자 명시)**: (i) 쌍마다 **힘을 2번** 계산 → 비용↑ (ii) 평면 양쪽의 접촉량(예: 면적)이
  **불일치**할 수 있음.  (출판본 같음.)
- **검증 (App C)**: 반경비 `R_i/R_j = [1, 0.75, 0.5, 0.25]` 4케이스 FEM 대조.  **0.25 가 가장 나쁘다** —
  이유 2가지: (i) 반경비가 커질수록 기하 교차가 접촉면적을 잘 못 나타냄, (ii) **작은 입자는 완전항복인데
  큰 입자는 거의 미항복**이라 소성누적 격차가 큼.  ⚠ **제하 곡선은 4케이스 모두 잘 맞는다.**
  `▶ 출판본:` 부록 C · **그림 C.15** (옛 C.10) · FEM = **2D 축대칭 반구 두 개 · CAX8R · tie 구속 · 법선 강체 · 접선 마찰 없음** · Rc* = (1/Ri + 1/Rj)⁻¹ 로 정규화 (`fig_C15.png` · `txt_p16_overlap_limit_095_and_radii_ratio_validation.png`).  [판독 · 벡터 표지 · 눈금 x 0/0.5/1 · y 0–0.5 틀 · 가장 큰 δ/Rc* 의 점] 정점 F/(E Rc*²) LAMMPS ↔ FEM: 반경비 1 → 0.445 ↔ 0.434 (δ/Rc* 1.20) · 0.75 → 0.407 ↔ 0.362 (1.05) · 0.5 → 0.340 ↔ 0.296 (0.90) · 0.25 → 0.199 ↔ 0.238 (0.75) — 0.25 에서만 LAMMPS 가 낮다 (방향 반대).  본문: *"Relatively good agreement is seen across the four cases in forward loading with the Ri/Rj = 0.25 case having the largest difference"* · *"all of the LAMMPS unloading curves show good agreement with FEM, unloading to zero force at approximately the same δ/Ri"* (p.16).
  ⚠ **우리 12:4:1 = R 비 0.083** 로 검증범위 밖(0.25 의 3배 더 극단) → **외삽**.

---

## 5. 방법 ★ (2) — ★★★ 비물리 접촉 선별: 위상 페널티 (§3, 사용자 질문 ④)

### 5-1. 무엇이 비물리적인가

일반 DEM 은 **"두 구가 기하학적으로 겹치면 접촉"** 으로 판정한다.  소변형에서는 겹침이 반경보다
훨씬 작아 서로 다른 접촉이 간섭하지 않으므로 문제없다.  **대변형에서는 다르다** (Fig 3 · `fig_3a.png`–`fig_3d.png`):

> **핵심 질문 (저자 원문)**: *"Should particle i be able to contact j given the presence of k?"*
> 출판본 원문 (p.4 · `txt_p4_lammps_main_repository_and_large_deformation_overlap.png`): *"In DEM simulations involving small deformations this geometric overlap contact detection works well given that distinct contacts don't typically infringe on one another due to the overlap being small compared to the particle radii. In large deformation DEM the situation changes dramatically …"*

입자 i, j 가 **사이에 낀 k 를 관통하여** 겹칠 수 있다.  실제로는 k 의 재료가 그 사이를 채우고 있으니
i–j 접촉은 **존재하지 않는다**.  그런데 표준 DEM 은 0 이 아닌 힘을 계산한다.
⇒ **대변형 DEM 에만 생기는 결함**이고, 겹침 규약(우리 ε_sphere)의 **기하학적 사촌**이다.

### 5-2. 알고리즘 (3단계) — 출판본 식 (5)–(11) 같음 (`eq_05…png` – `eq_11…png` · 그림 4 = `fig_4a.png` · `fig_4b.png`)

```
① 페널티가 필요한가:  δ_ij ≤ 0 또는 δ_ik ≤ 0 또는 δ_jk ≤ 0  →  모든 페널티 0        … (5),(6)
                        (셋이 다 겹칠 때만 진행.  삼중항 후보는 기존 neighbor list 로 제한)
② 비중심 접촉에 페널티:
     중심 판정: max(d_ij, d_ik, d_jk) = d_ij  →  k 가 중심                            … (7)
     각도:      α_kij = arccos(e_ki · e_kj)                                          … (8)
     시그모이드: p̂(α) = 1 / (1 + exp(−t_p (α/π − 1/2)))                              … (9)
       ▶ 출판본 인쇄는 exp(−t_p α/π − 1/2) (안쪽 괄호 빠짐) — §0-P P-3 · 뜻은 위 꼴
     배정:      p_ij = p̂(α_kij),  p_ik = 0,  p_jk = 0                                … (10)
     ⇒ 한 접촉이 여러 삼중항에서 비중심이면 **페널티를 중첩(합산)** 한다
③ 가중치: w = max(1 − p, 0),  최종 힘 = w · F                                        … (11)
```
- **t_p = 50** (모든 시뮬 공통) — 저자 표현 *"a fitted penalty transition intensity"*, *"no unique value
  of t_p exists"*.  전이구간 = **0.4 ≤ α/π ≤ 0.6** (p̂ ∈ [0.01, 0.99]).  출판본 각주 9 (p.17): *"Effectively in this case is defined as the range p̂(α) ∈ [0.01, 0.99]."* · [카드 산술] 정확한 경계 α/π = 0.408 · 0.592.
- **물리적 읽기**: α → π (i–k–j 가 일직선) = k 가 **완전히 막음** → p → 1 → 힘 0.
  α 작음 (i, j 가 k 의 같은 쪽) = 막지 않음 → p → 0 → 힘 그대로.
  **α = π/2 에서 정확히 반**(w = 0.5).
- **성질**: 시그모이드라 **가중치가 매끄럽게** 변한다 → 힘 점프 없음.  중심 입자가 바뀌어도 연속.
- 출판본 §3.1 (p.5 · `txt_p5_penalty_only_alters_force_at_large_overlaps.png`): *"This scheme can be appended to any typical DEM code without introducing significant modification given that it only alters the final resulting force in the case of large overlaps."*
- **예시 (App D, Fig D.11 → ▶ 출판본 그림 D.16)**: (b)(c) 완전차폐 p=1,w=0 / (d) 부분차폐 p=0.5,w=0.5 / (e) 무차폐 p=0,w=1 /
  (f)(g) 4입자 6접촉 4삼중항 — **대각접촉이 2번 페널티받아 0.5+0.5=1 → w=0** (`fig_D16a.png`–`fig_D16g.png`).  ▶ 출판본 정확히: 0.5 + 0.5 는 **(g)** 의 대각 접촉 {i,j} · {k,l} (p.17 *"penalized twice"*) · **(f)** 는 일직선 완전 차폐 둘 (p_ij = 1 · p_kl = 1 → w = 0) · {i,l} = 비접촉 (n.c.).
  [벡터 판독 · 그림 D.16 의 원은 모두 지름 79.46 pt] (d) 반 가중 배치: k–i · k–j 겹침 δ/R **0.83 · 0.87** · i–j 0.37 · α = 90° — 아래 5-3 의 최소값 '0.586' 보다 깊게 그려져 있다 (같은 쪽).

### 5-3. ★★ 우리 겹침 규약과의 관계 + **우리 침대에서의 정량 판정 (DERIVED)**

**(a) 동일 크기 삼중항 — 우리는 안전하다.**
반경 R, 양쪽 겹침 δ 인 대칭 삼중항에서 `d_ij = 2(2R−δ)·sin(α/2)` 이고 i–j 가 겹치려면 `d_ij < 2R`:

| 조건 | 필요 겹침 δ/R (08-25 · 반올림 경계 0.4 · 0.6) | `▶ 출판본 식 (9) · 각주 9 의 정확한 경계` [카드 산술] |
|---|---|---|
| 페널티가 **조금이라도** 걸림 (p̂ = 0.01) | **> 0.299** (α/π = 0.4) | **> 0.328** (α/π = 0.408 · α = 73.5°) |
| **절반** 가중 (α = 90°, p = 0.5) | **> 0.586** | **> 0.586** |
| 사실상 **소거** (p̂ = 0.99) | **> 0.764** (α/π = 0.6) | **> 0.752** (α/π = 0.592) |

우리 실측: composite SE-SE **δ/R = 0.148**, pure-SE **0.22** ⇒ **둘 다 발동 문턱(0.30) 아래** (출판본 경계 0.328 로는 더 아래).
★ **결론: 우리 현재 규약에서 이 알고리즘은 *아무 것도 하지 않는다*.**  Zunker 의 δ/R ≲ 0.75 영역에서만
1차 효과다.  ⇒ **"우리 18× 연화가 겹침을 키워 가짜 접촉을 만든다"는 걱정은 정량적으로 기각된다**
(연화가 겹침을 2배 더 키워도 0.30 에 못 닿는다).
⚠ (2026-11-12) 우리 실측 δ/R 0.148 · 0.22 는 08-25 카드의 기록이고 이번에 다시 재지 않았다.

**(b) ⚠⚠ 그러나 강한 다분산에서는 이야기가 다르다 — 우리 12:4:1 에 대한 경고 (DERIVED).**
큰 AM 두 개(R=6 µm)가 서로 접촉하고, 그 홈(groove)에 작은 SE(r=0.5 µm)가 끼어 **두 AM 을 동시에 겹치는**
배치를 생각하자.  예: d_AM-AM = 11.9 µm(겹침 0.1), d_AM-SE = 6.4 µm(겹침 0.1) ×2.
- ① 조건: 세 겹침 모두 > 0 ✅ 통과
- ② 중심 판정: max(11.9, 6.4, 6.4) = d_AM-AM ⇒ **SE 가 "중심"** 으로 지정된다
- 각도: cos α = (6.4²+6.4²−11.9²)/(2·6.4²) = −0.7286 → **α = 136.8°**, α/π = 0.76
- ③ p̂ = 1/(1+e^{−50(0.76−0.5)}) ≈ **1.0** → **w_AM-AM = 0 → AM–AM 접촉력이 0 이 된다**

**그런데 물리적으로는 두 AM 이 진짜로 닿아 있고, SE 는 *사이*가 아니라 *옆*(홈)에 있다.**
⇒ ★★ **거리 기반 중심 판정이 크기를 모르기 때문에, 작은 입자가 홈에 끼면 큰 입자끼리의 정당한 접촉을
소거한다.**  우리 침대에서 이것이 일어나면 **AM 골격의 force chain 과 σ_e 전자망이 통째로 무너진다**.
- ⚠ 이건 **논문의 오류 주장이 아니다** — 그들 검증은 **단분산 + 삼분산(±20 %, 최대/최소 반경비 1.5)** 뿐이고,
  **위상 페널티를 강한 다분산에서 시험한 적이 없다** (App C 의 0.25 시험은 *강체평면 배치 스킴*이지
  페널티가 아니다).  ⇒ **우리 12:4:1(반경비 0.083)에 쓰려면 크기-인지 중심판정으로 고쳐야 한다**
  (예: 중심 후보를 `d`가 아니라 `d − (R_i+R_j)` 또는 `d/(R_i+R_j)` 로 고르기).  **논문 밖 제안 = 우리 몫.**
  `▶ 출판본:` 식 (5)–(11) 이 바뀌지 않아 이 위험도 그대로.  정제 시뮬의 Rmax/Rmin 은 **1.15** (139–160 µm) · 부록 G 도 1.15 — 오히려 더 좁아졌다.

---

## 6. 방법 ★ (3) — 변형 입자 형상 재구성 (§5, 사용자 질문 ①의 최종 판정)

- **무엇을 들고 있나**: 접촉당 `δ_max`(접촉 상태변수) + 입자당 `R`(입자 상태변수).
- **재구성**: `겉보기반경 R 의 구` 에서 `각 접촉 방향으로 δ 만큼 잘라낸 구관`을 제거 → 변형형상.
- **검증 2건** (그림 7 = `fig_7_a-b.png` · `fig_7_c-d.png`):
  1. **삼축압밀 단일 입자** (E/Y = 20, ν = 0.3, δ_o/R_o = 0.15) — 하중 제거 후 Abaqus 형상 vs 모델 형상
     (Fig 7a vs 7b) → *"good agreement"* (정성).
  2. **MPFEM 단분산 침대 안의 한 입자**, 최대압축 시점 (Fig 7c vs 7d) → *"nice qualitative agreement with
     **all five of the contact patches** of the FEM particle present on the MDR reconstruction"* (프리프린트).
     `▶ 출판본 (§5.2 p.8 · 그림 8–11 · 부록 E)`: 이 문장은 **없다**.  대신 **정량** — Particle 1 의 FEM 접촉 **9 개** (상대 3 · 4 · 5 · 6 · 8 · 9 · 12 · 13 · 14) 의 변위 · 면적 · 힘 · 부피를 Δ/W 에 따라 비교하고, **13 번 접촉을 LAMMPS 가 못 잡는다** (§6-B).
- 저자 주장: *"aids in resolving a common deficit of elastic-plastic DEM whereby the deformation of a
  particle is not accessible."* (출판본 p.8 같음 · `txt_p8_reconstruction_deficit_of_elastic_plastic_dem.png`)

### ★★★ 최종 판정 — "진짜 형상 자유도인가, 사후 역산인가"

**둘 다 아니다.  정확히는 "구속된 형상 족 위의 진짜 상태변수"다.**

| 질문 | 답 | 근거 |
|---|---|---|
| 형상이 상태변수로 존재하나? | ✅ **그렇다** — `R` + 접촉당 `δ_max` | §5, Part I §5.2 |
| 그 형상이 **다음 스텝 물리**에 되먹임되나? | ✅ **그렇다** — 힘(δ 증가), **신규 2차 접촉**, `A_free/A_tot` 벌크발동, `V_geo` | Part I §8.2 / Part II §5.1 · 출판본 식 (A.4) · (A.23) · (A.32) |
| **사후 후처리(post-hoc)** 인가? | ❌ **아니다** — 재구성은 시각화지만 그 상태변수는 이미 물리를 굴린다 | |
| **자유형상(free-form)** 인가? | ❌ **아니다** — 입자당 **스칼라 1개(R)** + 접촉평면들 | App C eq (C.1) (08-25 카드 표기 · ▶ 출판본에는 번호 붙은 (C.1) 이 없다 — 대응 = §5.1 · 식 (A.23) · (A.33)) |
| 무엇을 못 하나 | **이방 배럴링 · 비축대칭 유동 · 재료 국소이동 · 오목 프로파일 · 파쇄 · 내부 변형장/응력장** | Part I §8.3.2, 본 논문 결론 · `▶ 출판본 부록 E.2`: *"the MDR contact model, and classical DEM more generally, being unable to capture anisotropic internal deformations"* |
| 언제 무너지나 | 고구속에서 **구관들이 서로 교차** → ΔR 비물리 → Part II 가 **R 성장 동결**로 회피 | Part I App C, Part II §4.3.3 |

⇒ **litdb 정본 층위지도 갱신 필요** — 새 칸 **층(2.75) "매개변수 형상 상태"**.  자세히는 ①카드 §7-1.
⇒ **frame[5] 는 유지되지만 경계가 이동한다**: MPM 의 고유영역이 *"형상 소성 전부"* 에서
*"**자유형상**·**내부 변형장**·**비축대칭 유동**·**void-fill 의 재료이동**"* 으로 **좁아졌다**.
⇒ `▶ 출판본`이 이 경계를 **원문으로 확인**했다: 전단이 만드는 비등방 변형 → 접촉 놓침 (부록 E.2) · *"In practice, the MDR contact model should be employed for predominately isotropic loading conditions, as studied here, given that plastic shear strains are only modeled adjacent to contacts and not deep within a particle's interior."* (각주 2, p.8).

### 6-B. `▶ 출판본` §5.2 — Particle 1 정량 대조 (Fig 8 – Fig 11 · 부록 E · 표 E.3)

> [판독] = 그림 8–11 의 벡터 표지를 틀 · 눈금으로 환산한 **마지막 점** (Δ/W ≈ 0.30).  FEM ↔ LAMMPS.

| 상대 입자 | 변위 δo/Ro (그림 8) | 면적 AC/(πRo²) (그림 9) | 힘 F/(E Ro²) (그림 10) |
|---|---|---|---|
| 3 | +0.024 ↔ −0.034 | 0.115 ↔ 0.019 | 0.0231 ↔ 0.0090 |
| 4 | +0.311 ↔ +0.248 | 0.281 ↔ 0.243 | 0.0671 ↔ 0.0655 |
| 5 | +0.144 ↔ +0.140 | 0.192 ↔ 0.105 | 0.0359 ↔ 0.0398 |
| 6 | +0.301 ↔ +0.269 | 0.249 ↔ 0.255 | 0.0644 ↔ 0.0727 |
| 8 | +0.047 ↔ +0.030 | 0.093 ↔ 0.032 | 0.0155 ↔ 0.0048 |
| 9 | +0.378 ↔ +0.331 | 0.349 ↔ 0.322 | 0.0818 ↔ 0.0958 |
| 12 | +0.416 ↔ +0.270 | 0.350 ↔ 0.306 | 0.0770 ↔ 0.0902 |
| **13** | **+0.036 ↔ −0.114** | **0.109 ↔ 0 (놓침)** | **0.0234 ↔ 0 (놓침)** |
| 14 | +0.211 ↔ +0.159 | 0.205 ↔ 0.156 | 0.0452 ↔ 0.0533 |
| **합** | — | **1.94 ↔ 1.44 (74 %)** [카드 산술] | **0.433 ↔ 0.431 (99.5 %)** [카드 산술] |

- 변위 축: Fig 8 은 y 틀 끝 = −1 · 0.5 로 환산 (위 큰 눈금이 틀선과 겹쳐 틀 끝으로) · 검산 = 가운데 큰 눈금 (−0.5) 자리가 이 환산으로 −0.5000.  각 패널의 처음 값 (Δ/W = 0) [판독]: 3 −0.57 · 4 −0.26 · 5 −0.004 · 6 −0.31 · 8 −0.60 · 9 −0.07 · 12 −0.15 · 13 −0.86 · 14 −0.59.
- 접촉 3 의 LAMMPS 끝 δo/Ro 는 −0.034 (음수) 인데 면적 (그림 9) 은 0.019 > 0 — 본문은 그림 8 의 0 선을 *"the transition from non-contact to contact"* (p.8) 로 쓰지만, MDR 의 겹침은 겉보기 반경 기준 (식 A.3 δ = δo + R − Ro) 이라 R 이 자란 만큼 δo < 0 이어도 접촉일 수 있다 [추정 — 원문 설명 없음].
- ★ **읽기**: 입자 하나에 걸린 **힘의 합은 거의 같고** (경계가 같은 하중을 준다), **배분이 다르다** — 끝 겹침이 작은 접촉 (3 · 8 · 13 — FEM 끝 δo/Ro < 0.05 [판독]) 은 LAMMPS 쪽 힘이 작거나 없고, 큰 접촉 (6 · 9 · 12 · 14) 은 LAMMPS 힘이 13–18 % 크다 [카드 산술: 0.0727/0.0644 · 0.0958/0.0818 · 0.0902/0.0770 · 0.0533/0.0452].  **면적은 대체로 작다** (합 74 %) → MDR 접촉 압력 (F/A) 이 FEM 보다 높은 쪽 [카드 산술 · 해석].  본문은 *"evolutions are modeled to a reasonable degree of accuracy"* · *"All remaining contacts … show a matching force evolution"* 이라 적는다.
- 부피 (그림 11): 끝 V/Vo FEM 0.9636 ↔ LAMMPS 0.9645 [판독] — *"good agreement"*.  탄성 부피 감소 ≈3.6 % (E/Y 20 재료).
- 부록 E (그림 E.17 · E.18 · 표 E.3): 다섯 방향 그림에서 접촉 크기 · 자리는 맞고 13 번만 없다.  최소 부피 타원체 반축 — FEM Particle 1: 0.4751 · 0.5184 · 0.5577 · Particle 13: 0.5083 · 0.5504 · 0.5889 (비등방) · MDR 은 *"essentially a sphere"*.  ⇒ 두 입자의 비등방 변형이 겹쳐 생긴 접촉을 MDR 이 못 만든다.

### 6-A. `▶ 출판본` 부록 A — MDR 정식 요약 (식 A.1–A.34 · 표 A.2 · 크롭 = §7-E)

| 블록 | 식 | 내용 |
|---|---|---|
| 분해 | (A.1)–(A.3) | F = F_MDR + F_Bulk · δo = δo,MDR + δo,Bulk · 겉보기 겹침 δ = δo + R − Ro |
| 벌크 발동 | (A.4)–(A.9) | Afree/Atot ≥ ψb → 증분 전부 MDR · 아니면 평균 표면 변위 dδ̄o 만큼 벌크로 · Acon = ΣAC · AC = π(2δR − δ²) + cA · Atot · Afree |
| MDR 힘 | (A.10)–(A.13) | 1D 타원 압자 (높이 A · 폭 B) · E*c = E/(1−ν²) (상대가 늘 강체 평면) · 탄성 A = 4R, B = 2R · 완전 소성 A = 4pY amax/E*c, B = 2amax |
| 경화 · 전이 | (A.14)–(A.22) | pY = Y(1.75 e^{−4.4 δMDR,max/R} + 1) · Hertz p̄H = (4E*c/3π√R)√δ 와 만나면 탄성 → 완전 소성 (*"A sharp transition"*) · 큰 변형 보정 δR · amax · cA · 항복 변위 δY (A.22 지수 인쇄 −1.1 · §0-P P-3) |
| 반경 성장 | (A.23) | ΔR = max[(ΔVᵉ − Σπ Δδo,MDR(…))/(2πR Σ(…) − 4πR²), 0] (Afree/Atot ≥ ψb 일 때) · 아니면 0 = **소성 비압축을 R 성장으로** |
| 부피 | (A.24) | V = Vo(1 + tr(Σ f⊗b)/(3κV)) — 탄성 부피 (κ = 체적 탄성률) |
| 점착 (JKR 형) | (A.25)–(A.31) | Δl(a) = √(2πaΔγ/E*c) · 임계 반경 ac (힘 제어 ξ = 3 · 변위 제어 ξ = 1) · 세 상태 (인장 없음 / 인장 · 임계 이하 / 초과 → 분리 판정) · *"material may only adhere once compressed"* (본문 p.15 · 붙은 각주 8 = JKR 의 '하중 없이 저절로 생기는 접촉 면적' 을 무시한다는 말) |
| 벌크 힘 | (A.32)–(A.34) | dF_Bulk,i = (Acon/Vgeo) κ dδ̄o AC,i · Vgeo = (4/3)πR³ − Σ(π/3)δi²(3R − δi) |

- 입력: E · ν · Y · Δγ · ψb (+ κ 는 E · ν 로) — §2.1: *"The inputs to the model are primarily physical material properties … The exception is the critical confinement ratio"* (`txt_p3_mdr_features_inputs_physical_psi_b_exception.png`).

### 6-G. `▶ 출판본` 부록 G — 민감도 분석 (그림 G.20–G.22 · `txt_p19_sensitivity_analysis_residual_stress_trends.png`)

- 설정: **1000 입자 · Rmax/Rmin = 1.15** · 같은 충전 · 변수 E · ν · Y · Δγ · ψb · µt · µt,wall · µroll 을 기준의 0.8 · 0.9 · 1.1 · 1.2 배 · **상대밀도 0.9 까지** 압축 후 제하 · 그림은 기준 최대값으로 정규화 (절대 MPa 없음).
- 원문 경향 (잔류 응력): *"as E increases, ν decreases, or Y decreases, the residual stress tends to increase. Although Δγ does not influence the overall compaction curve, decreasing its value lowers the residual stress. If reduced sufficiently, the tablet will fracture … ψb has a significant impact on residual stress … As ψb increases, radial growth is halted earlier, leading to less buildup of radial stress and, consequently, a lower residual radial stress after unloading … residual stress generally decreases as µt increases. Lastly, µt,wall and µwall have minimal influence"* (`µwall` 은 인쇄 그대로 — 그림 G.21h 는 µroll).
- [판독 · G.20–G.22 는 래스터 그림이라 눈으로 · ±0.05] 그림 G.22: σzz/σrr 가 상대밀도 0.5 근처 ≈2.8 → 0.84 근처 최소 ≈1.7 → 0.9 에서 ≈1.8 · ψb 1.2 배면 0.9 에서 ≈2.0.  ⇒ 측압비 σrr/σzz ≈ 0.56 (기준, RD 0.9).
- [판독 · 눈으로 · ±0.01] 기준 곡선의 제하 끝 상대밀도 ≈0.81–0.82 (정점 0.90 → 높이 ≈10 % 되돌아옴 [카드 산술]) · 그림 G.21 의 잔류 반경응력 ≈ 기준 최대의 0.2 · ψb 1.2 배 → 제하 끝 ≈0.79 · 0.8 배 → ≈0.83 (ψb ↑ = 더 되돌아오고 잔류 반경 ↓ — 본문 문장과 같은 방향).  같은 모델의 정제 시뮬 (10,000 입자 · 0.996 → 0.939 · 6.0 % · §3-5) 보다 크게 되돌아온다 — 원문은 이 차이를 다루지 않는다 [미확인].
- ⚠ 기준 변수 목록 문장 {E, ν, Y, Δγ, µt, µt,wall, µroll} 에 ψb 가 빠져 있지만 ψb 도 그림 (e) 에서 바꾼다 — 인쇄 그대로.

---

## 7. Figure set ★ — 출판본 번호 · 크롭 (2026-11-12)

> 전부 `litdb/figures/zunker2025_dem_large_deformation_compaction/` · 패널은 `fig_<N><패널>.png` (짝은 `fig_5_a-b.png` 꼴) · 부록 그림은 점을 뺀 이름 (`fig_C15.png`).  [판독] 값은 §3-5 · §6-B.

| Fig | 무엇 | 크롭 | 우리가 쓸 것 |
|---|---|---|---|
| 1 | 다체 접촉 {i,j,k,l} + 각 접촉에 **가상 강체평면** | `fig_1.png` | 다체 확장의 개념도 |
| 2 | 평면 배치: (a) 전방재하 = 기하교차 (b) 제하 = 소성변위 선형보간 | `fig_2.png` · `fig_2a` · `fig_2b` | ★ 작은 입자가 겹침을 거의 다 먹는다 (§4) |
| 3 | **비물리 접촉 2예**: (a)(b) 3입자 단축 (c)(d) 4입자 등방 | `fig_3.png` · `fig_3a`–`fig_3d` | ★★ 대변형 DEM 의 숨은 결함 — 발표용 |
| 4 | 삼중항 페널티 기하 (a) 불필요 (b) 필요 · α_kij | `fig_4.png` · `fig_4a` · `fig_4b` | 알고리즘 정의 |
| 5 | MPFEM 배치: 단분산 14 (a 처음 · b 끝) · 삼분산 12 (c · d) | `fig_5.png` · `fig_5_a-b` · `fig_5_c-d` | ★ 접지검증 셋업 (12–14 입자) |
| 6 | σ_xx · σ_yy · σ_zz / E vs Δ/W — 단분산 (a–c) · 삼분산 (d–f) | `fig_6.png` · `fig_6a`–`fig_6f` | ★★ 정량 검증 본체 · 끝값 [판독] §3-3 |
| 7 | 형상 재구성: (a)(b) 삼축 단일 입자 FEM ↔ MDR (c)(d) MPFEM Particle 1 | `fig_7.png` · `fig_7_a-b` · `fig_7_c-d` | ★★★ 층 (2.75) 의 증거 그림 |
| 8 | Particle 1 의 접촉별 변위 δo/Ro (9 접촉) | `fig_8.png` · `fig_8a`–`fig_8i` | (h) 13 번: FEM 접촉 ↔ MDR 비접촉 |
| 9 | Particle 1 의 접촉 면적 AC/(πRo²) | `fig_9.png` · `fig_9a`–`fig_9i` | ★ MDR 면적이 대체로 작다 (합 74 %) — 우리 coverage · 협착 면적에 직결 |
| 10 | Particle 1 의 접촉력 F/(E Ro²) | `fig_10.png` · `fig_10a`–`fig_10i` | 힘 합은 같고 배분이 다르다 |
| 11 | Particle 1 부피 V/Vo vs Δ/W | `fig_11.png` | 탄성 부피 식 (A.24) 검증 |
| 12 | 압축 시험기 (a) 압축 전 (b) 압축 뒤 · 센서 자리 · 치수 | `fig_12.png` · `fig_12a` · `fig_12b` | 실험 셋업 (범례는 `fig_12a` 에) |
| 13 | Avicel PH102 SEM | `fig_13.png` | 입자가 구가 아님 — 시뮬 구의 한계 |
| 14 | ★ (a) 축응력 · (b) 반경응력 vs 상대밀도 — 실험 ↔ LAMMPS · (c) LAMMPS 4 단계 | `fig_14.png` · `fig_14a` · `fig_14b` · `fig_14c` | ★★★ 핵심 결과 · 판독 §3-5 |
| C.15 | 반경비 1 · 0.75 · 0.5 · 0.25 의 F–δ (FEM ↔ LAMMPS) | `fig_C15.png` · `fig_C15a`–`fig_C15d` | 다분산 검증 범위 원장 — 우리 0.083 은 밖 |
| D.16 | 페널티 예 (a) 시그모이드 (b)–(e) 세 입자 (f)(g) 네 입자 | `fig_D16.png` · `fig_D16a`–`fig_D16g` | 페널티 직관 |
| E.17 | Particle 1 접촉 다섯 방향 (위 FEM · 아래 MDR) · (d) 13 번 놓침 | `fig_E17.png` · `fig_E17a`–`fig_E17e` | 층 (2.75) 의 한계 그림 |
| E.18 | Particle 1 · 13 겹쳐 보기 + 최소 부피 타원체 | `fig_E18.png` · `fig_E18a` · `fig_E18b` | 비등방 = MPM 몫 |
| F.19 | 입도 (a) 부피 분포 (b) 확률 밀도 + Weibull 맞춤 | `fig_F19.png` · `fig_F19a` · `fig_F19b` | PSD 이상화 정도 |
| G.20 | 축응력 민감도 (8 변수) | `fig_G20.png` · `fig_G20a`–`fig_G20h` | 보정 손잡이 지도 |
| G.21 | 반경응력 민감도 | `fig_G21.png` · `fig_G21a`–`fig_G21h` | ★ 잔류 반경응력의 손잡이 (E · ν · Y · ψb · µt) |
| G.22 | 축/반경 응력비 민감도 | `fig_G22.png` · `fig_G22a`–`fig_G22h` | 측압비 ≈0.56 at RD 0.9 [판독] |
| Table 1 | 출판본 LAMMPS 값 | `tab_1.png` | §3-2′ |
| Table A.2 | MDR 기호 사전 | `tab_A2.png` | 식 읽기 |
| Table E.3 | 최소 부피 타원체 반축 · 주축 | `tab_E3.png` | 비등방 정량 |

### 7-0. 프리프린트 판 그림 표 (2026-08-25 · 텍스트로만 · 보존 — 번호가 출판본과 다르다)

> ⚠ (프리프린트) 이미지 미확인 — 캡션·본문 기반, digitized 값 0개.  첫 칸은 **프리프린트 번호** · 둘째 칸이 출판본 번호.

| 프리프린트 번호 | 출판본 번호 | 무엇 (08-25 원문 그대로) | 우리가 쓸 것 (08-25) |
|---|---|---|---|
| **1** | 1 | 다체 접촉 {i,j,k,l} + 각 접촉에 **가상 강체평면** 배치 | 다체 확장의 개념도 |
| **2** | 2 | 평면 배치 스킴 (a) 전방재하=기하교차 (b) 제하=소성변위 기반 선형보간 | ★ **작은 입자가 겹침을 거의 다 먹는다**는 §4 결론의 그림 |
| **3** | 3 | **비물리 접촉 2예**: (a)(b) 3입자 단축압축 — i,j 가 k 를 관통해 겹침 (c)(d) 4입자 등방압축 | ★★ **대변형 DEM 의 숨은 결함**을 한 장으로 — 우리 발표에 그대로 쓸 만함 |
| **4** | 4 | 삼중항 페널티 기하: (a) 불필요 (b) {i,j} 페널티 필요, α_kij·e_ki·e_kj 표시 | 알고리즘 정의 |
| **5** | 5 | **MPFEM**: (a)(b) 단분산 14 입자 초기/최종 (c)(d) 삼분산 12 입자 초기/최종 | ★ **접지검증 셋업** — 우리가 같은 대조를 짜려면 이 규모(12–14 입자)면 된다 |
| **6** | 6 | **σ_xx·σ_yy·σ_zz vs Δ/W**: 상 = 단분산 (a)(b)(c), 하 = 삼분산 (d)(e)(f), FEM vs DEM | ★★ **정량 검증의 본체**.  ⚠ Δ/W 범위는 **그림에만** → n/a (출판본 판독: Δ/W 0–0.30 · 0–0.33) |
| **7** | 7 | **형상 재구성**: (a)(b) 삼축압밀 FEM vs 모델 (c)(d) MPFEM 입자 FEM vs 모델(**접촉패치 5개**) | ★★★ **층(2.75) 의 증거 그림** (출판본: 9 접촉 중 1 개 놓침) |
| **8** | 12 | compaction simulator 실물 모식 (a) 압축 전 (b) 후, 치수(8 mm, 5.85 → 3.57 mm) + 센서 위치 | 실험 셋업 (출판본: 높이 표기 없음 · 센서 깊이 10 · 12 mm · 다이 12.75 mm [판독]) |
| **9** | 14 | (a) **축응력–축변형** exp vs sim (b) **반경응력–축변형** exp vs sim (c) LAMMPS 4단계 스냅샷(die fill / max compaction / upper punch release / ejection) | ★★★ **핵심 결과**.  (b) 의 **잔류 반경응력** 재현이 하이라이트 (출판본: x 축 = 상대밀도) |
| **C.10** | C.15 | 반경비 [1, 0.75, 0.5, 0.25] 4케이스 F–δ, FEM vs LAMMPS | ★ **다분산 검증범위의 원장** — 우리 0.083 은 여기 밖 |
| **D.11** | D.16 | (a) 시그모이드 페널티 함수 (b)–(e) 3입자 4배치 + 가중치 (f)(g) 4입자 배치 + 가중치 | 페널티 직관 |
| **E.12** | F.19 | Avicel PH102 **PSD**: (a) 부피분포 (b) 확률밀도 + **shifted Weibull 피팅** | ★ PSD 이상화 정도(§10 주의) |

### 7-E. 식 크롭 (번호 붙은 식 전부 · 400 dpi · `eq_*.png`)

| 묶음 | 파일 | 뜻 |
|---|---|---|
| (1)–(4) 강체 평면 배치 | `eq_01_rigid_flat_overlap_partition_i` · `eq_02_…_j` · `eq_03_geometric_intersection_i` · `eq_04_…_j` | §4 |
| (5)–(11) 위상 페널티 | `eq_05_penalty_check_overlaps` · `eq_06_zero_penalties` · `eq_07_central_particle_max_distance` · `eq_08_angle_alpha_kij` · **`eq_09_sigmoid_penalty`** (인쇄 괄호 빠짐) · `eq_10_penalty_assignment` · **`eq_11_contact_weights`** | §5 |
| (A.1)–(A.9) 분해 · 벌크 발동 | `eq_A01_force_mdr_plus_bulk` … **`eq_A04_partition_psi_b`** … `eq_A09_mean_surface_displacement` | §6-A |
| (A.10)–(A.22) MDR 힘 · 경화 · 전이 | **`eq_A10_mdr_force`** · `eq_A11_plane_strain_modulus` · `eq_A12_…` · `eq_A13_ellipse_A_B` · **`eq_A14_hardening_pY`** · `eq_A15_hertz_mean_pressure` … `eq_A22_yield_displacement` (지수 인쇄 −1.1) | §6-A |
| (A.23)–(A.24) 반경 성장 · 부피 | **`eq_A23_apparent_radius_growth`** · `eq_A24_particle_volume` | §6-A |
| (A.25)–(A.31) 점착 | `eq_A25_critical_extension_length` … `eq_A31_separation_condition` | §6-A |
| (A.32)–(A.34) 벌크 힘 | **`eq_A32_bulk_force_increment`** · `eq_A33_geometric_volume` · `eq_A34_bulk_force_integral` | §6-A |
| (B.1) 겹침 상한 0.95 | `eq_B01_overlap_cap_0p95` | §4 |
| (F.1) · (F.2) 입도 | `eq_F01_avicel_psd_shifted_weibull` · `eq_F02_lammps_psd_scaled_3p2` | §8 |

### 7-T. 근거 문단 크롭 (카드가 인용한 문장 · 19 장 · 400 dpi)

`txt_p2_abstract_relative_density_residual_radial_stress` (초록 끝) · `txt_p3_mdr_features_inputs_physical_psi_b_exception` (§2.1) · `txt_p3_varying_material_properties_future_work_tradeoffs` (§2.2) · `txt_p4_lammps_main_repository_and_large_deformation_overlap` (§2.3 · §3) · `txt_p5_penalty_only_alters_force_at_large_overlaps` (§3.1) · `txt_p7_mpfem_lammps_setup_psi_b_cost_wall_stress` (§4) · `txt_p8_reconstruction_deficit_of_elastic_plastic_dem` (§5.1) · `txt_p8_contact13_missed_and_isotropic_loading_footnote` (§5.2 + 각주 2) · `txt_p8_experiment_die_rates_rd_two_tests` (§6) · `txt_p10_measured_peaks_residual_radial_stress` (실측 + 각주 4) · `txt_p11_parameter_selection_fitted_tuned_timestep` (§7.1) · `txt_p11_tableting_setup_10000_particles_quasistatic` (§7.2 + 각주 6) · `txt_p12_axial_results_initial_rd_bulk_underprediction` (§7.2 + 각주 7) · `txt_p12_radial_stress_method_residual_prediction` · `txt_p13_future_work_multicomponent_calendaring` (§8) · `txt_p16_overlap_limit_095_and_radii_ratio_validation` (부록 B · C) · `txt_p17_sigmoid_range_tp50_no_unique_value` (부록 D + 각주 9) · `txt_p18_anisotropic_deformation_classical_dem_limit` (부록 E.2) · `txt_p19_sensitivity_analysis_residual_stress_trends` (부록 G).

### 7-V. 보충 영상 — 프레임 8 장 (보충 영상 프레임 · 캡션 없음 · 화면 관찰)

> 본문 p.12: *"Videos showcasing all phases of the tableting simulations for the two relative densities are shown in Supplementary Videos 1 and 2."* — PDF 에 영상 캡션은 없다 (어느 영상이 어느 상대밀도인지 적혀 있지 않다).  mp4 는 커밋하지 않았다 (sha256 · 길이는 `figures.json` 의 `movies`).

| 프레임 | 화면에서 보이는 것 [관찰] |
|---|---|
| `vid1_t0.0s.png` · `vid2_t0.0s.png` | 다이 절단면 (뒤쪽 반만) · 위 · 아래 펀치 사이를 구 입자가 채움 (die fill).  두 영상의 첫 프레임이 거의 같다 = *"The same initial packing is used in both simulations"* (p.12) 와 맞는다 |
| `vid1_t6.2s.png` · `vid2_t6.5s.png` | 최대 압축 근처 — 위 펀치가 다이 안으로 들어가 입자 띠가 얇다 · 입자는 구로 그려진다 |
| `vid1_t10.0s.png` · `vid2_t10.0s.png` | 위 펀치 해제 뒤 — 정제가 다이 안에 남음 |
| `vid1_t19.0s.png` · `vid2_t20.0s.png` | 배출 끝 — 아래 펀치가 정제를 다이 위로 밀어 올림 · 위 펀치는 위에 |

- 화면 측정 (갈색 입자 화소의 세로 범위 · 0.1 s 간격): 처음 232 px · 최소 **85 px (영상 1, 6.2 s)** · **75 px (영상 2, 6.5 s)**.  비 85/75 = 1.13 ↔ 0.99/0.85 = 1.165 (같은 충전이면 두께 ∝ 1/상대밀도) ⇒ **영상 1 = 0.85 시험 · 영상 2 = 0.99 시험** [추정 — 캡션 없음 · 원근 · 펀치 가림 때문에 근사].
- 단계 시각 [관찰]: 0–≈2.5 s 충전 상태 · ≈2.5–6.2/6.5 s 하강 · ≈7–9 s 위 펀치 복귀 · ≈10.5–17.5 s 배출 · 그 뒤 정지.  글자 · 축척 · 시각 표시 없음.  ⚠ 해제 뒤 화소 높이가 커지는 것은 정제 윗면이 보이기 때문이라 **되돌아옴을 이 영상에서 잴 수 없다**.

---

## 8. Post-processing ★

- **거시 응력 산출 2가지 (★ 방법이 다르다 — 주의)**:
  - **축응력**: 상·하 펀치에 입자가 가하는 **총 힘 / 펀치면적** (= 실험 센서와 같은 양).  출판본: 시뮬은 *"the total force exerted on the upper punch by the particles is tracked"* (p.12) · 실험 축응력 = 축력 ÷ 펀치 면 면적 (각주 4).
  - **반경응력**: **입자당 응력텐서**(per-particle stress)를 전 입자 평균 → **부피분율 곱** → 축에 직교하는
    두 법선성분 평균.  ⚠ **die 벽 반력이 아니라 입자 응력 평균**이다 — 실험(벽 압력센서)과 **같은 양이
    아니다**.  MPFEM 대조(§4)에서는 반대로 **벽 반력 / 벽 면적**을 썼다.  ⇒ **두 절에서 응력 정의가
    다르다** (인용 시 명시할 것).  (출판본 p.12 같음 · `txt_p12_radial_stress_method_residual_prediction.png`.)
- **입자당 응력** = Part I eq (38) 의 `Σ_c f_c ⊗ b_c` (Christoffersen/Love–Weber) — ★ 우리 `f_AM` 하중분담
  측정의 **phase-virial 규약**과 **같은 대상**이다 (CLAUDE.md 2026-08-11 Q2/Q6 참조).  출판본 식 (A.24) 가 같은 tr(Σ f⊗b) 를 부피에 쓴다.
- **도구**: LAMMPS (DEM, `mdr` 브랜치) + Abaqus (MPFEM) + compaction simulator (실험).  `▶ 출판본:` LAMMPS 본 저장소 (develop) · 최소 부피 타원체 = MATLAB File Exchange [68] (부록 E.2).
- **재구성 시각화**: 상태변수(R, δ_max)로부터 잘린 구를 그린다 (별도 도구 미명시 · 출판본: *"the lines on the MDR contact model reconstructions are for visualization purposes and do not represent a mesh"* — 그림 7 캡션).
- **PSD 처리 (App E → ▶ 출판본 부록 F · 식 F.1 · F.2)**: 실측 PSD 를 **shifted Weibull**(λ=6, k=0.69, shift s=4.5)로 피팅한 뒤
  **3.2배 스케일업**한 분포에서 `R ∈ [96, 144] µm` 만 채택.  `▶ 출판본:` R ∈ [**139, 160**] µm.
  ⚠ **이상화 정도 (DERIVED)**: 실제 D50 **지름 116 µm** 인데 시뮬 입자는 **지름 192–288 µm** = **약 2배 큼**,
  그리고 최대/최소 반경비 **1.5** 로 꼬리가 잘렸다.  저자가 *"computational tractability"* 로 명시.
  `▶ 출판본:` 지름 **278–320 µm = 2.4–2.8 배** · 반경비 **1.15** [카드 산술] — 더 좁고 더 크다.  ⚠ 그림 F.19 의 'size' 가 지름인지 반경인지 축 이름만으로는 모른다 [미확인].
- `▶ 출판본` **상대밀도 판독**: 실험 = 펀치 위치로 낸 정제 부피밀도 ÷ 진밀도 (*"RD = ρt/ρ"*) · 시뮬의 정의는 적혀 있지 않다 [미확인].

---

## 9. 실행 가능성 ★ (사용자 질문 ⑧) — LIGGGHTS 로 옮길 수 있나

> `▶ 출판본`: MDR 과 페널티는 **LAMMPS 본 저장소 (develop)** 에 들어갔다 (§2.3) — 포크 · 커밋 고정 없이 LAMMPS 그대로 받아 쓸 수 있다는 뜻이다.  아래 9-1 의 구조 (3-패스 · 상태 변수 이름) 는 08-25 카드가 그 당시 포크 코드에서 읽은 것이고 **출판본에는 구현 구조 서술이 없다** [추정 — 본 저장소 판에서 다시 확인 필요].

### 9-1. 옮길 수 있나 — **원리적으로 가능, 실무적으로는 "포팅"이 아니라 "재구현"**

| 축 | 상태 | 난이도 |
|---|---|---|
| 라이선스 | **GPL v2** = LIGGGHTS 와 동일 계열 (08-25 기록 · 출판본 표기 없음) | ✅ 문제없음 |
| 코드 계보 | LIGGGHTS 는 LAMMPS 포크(2011–12).  이 구현은 **현대 LAMMPS `GRANULAR` 서브모델 아키텍처**(Bolintineanu·Clemmer, 감사절에 명시) 위에 있음 | ⚠ **아키텍처가 다르다** — LIGGGHTS `pair gran` + `fix wall/gran` + cohesion/rolling model 트리와 1:1 대응 안 됨 |
| 입자별 영속 상태 | `R`, `V`, `Y_flag`, `c_A` | ✅ LIGGGHTS `fix property/atom` |
| 접촉별 영속 상태 | `δ_max,MDR`, `δ_MDR`, `δ_o,Bulk`, `a`(점착 시) | ✅ `fix contacthistory` (필드 수만 늘림) |
| **3-패스 구조** | `calcBulkItems`(입자집계) → 접촉루프 → `findUpdatedRadiusAndVol`(입자집계) | ⚠⚠ **최대 난점**.  LAMMPS/LIGGGHTS 의 단일 pairwise 패스 규약을 깬다.  병렬에서 **입자 집계량(A_con, δ̄_o, V_geo)의 ghost 통신**이 추가로 필요.  출판본 식 (A.5)–(A.9) · (A.23) · (A.32) 가 바로 그 입자 집계량이다 |
| **삼중항 루프** | 이웃의 이웃 순회 | ⚠ 표준 아님.  neighbor list 로 후보를 줄인다지만 **O(N·⟨Z⟩²)** 추가 (출판본 p.5: *"Triplet eligibility is determined strictly by the current neighbor lists"*) |
| 쌍당 힘 2회 평가 | 가상평면 양쪽 | ⚠ 비용 ×2 |
| 무마찰 가정 | 법선만 MDR; 접선·롤링은 **기존 모델과 중첩** | ✅ LIGGGHTS 도 같은 구조 |

★ **판정**: **"LIGGGHTS 로 포팅"은 1–2주가 아니라 수개월급 소프트웨어 작업**이다.
**대신 그들 LAMMPS 브랜치를 직접 쓰는 것이 압도적으로 싸다** — 우리가 필요한 것은 *우리 침대에서
돌려보는 것*이지 *우리 코드베이스에 넣는 것*이 아니다.  `▶ 출판본:` "브랜치" → **LAMMPS 본 저장소 develop** (§16 (라)).

### 9-2. 계산비용 (DERIVED)

- 그들 시간스텝 규칙 `Δt = 0.35√(m/k)`, `k = κ R_min` 를 **우리 LPSCl 에 적용**:
  ρ_SE = 1640 kg/m³, R_SE = 0.5 µm, κ = **B₀ = 26.23 GPa** (우리 DFT)
  → m = 8.59×10⁻¹⁶ kg, k = 1.31×10⁴ N/m → **Δt ≈ 9×10⁻¹¹ s** (= 0.09 ns).
  `▶ 출판본 계수 0.08`: **Δt ≈ 2.0×10⁻¹¹ s** [카드 산술] — 4.4 배 짧다.  저자 스스로 *"subject to change depending on the compact geometry and loading conditions"*.
- 우리 현재(E_eff 1.35 GPa) Rayleigh 기준 대비: **실제 E(22.1 GPa)로 가면 Δt 는 √(22.1/1.35) ≈ 4.0배 작아진다.**
  ⇒ ★ **"실제 물성으로 가는 값" = 스텝 수 4배** (+ 위 3-패스/삼중항 오버헤드).  **감당 가능한 규모다.**  (출판본 계수로는 Zunker 규칙 자체가 더 보수적 — 우리 Rayleigh 규칙과 직접 비교는 하지 않는다.)
- 입자수 비교: 그들 tableting **20,000 개** ↔ 우리 real_14 SE **32,832 개** — **같은 등급**.  `▶ 출판본:` **10,000 개**.
  ⚠ 그들의 tableting 총 벽시계 시간은 **미보고**(n/a); 보고된 것은 14-입자 MPFEM 대조의 ~1 초뿐이다 (출판본 같음).

### 9-3. **"경로 A(항복캡)" 를 이걸로 대체하는 게 나은가** — 판정

| 축 | **경로 A** (So 2021 H-cap / Thornton–Ning 을 LIGGGHTS 에) | **경로 A′ = Zunker 브랜치 직접 사용** (▶ 출판본: LAMMPS 본 저장소) |
|---|---|---|
| 구현 노력 | 중 (LIGGGHTS pair style 교체) | **낮음** (기존 코드 실행) — 단 **우리 파이프라인 밖** |
| 항복캡 | ✅ 상수 H 또는 p_y | ✅ **δ-의존 경화곡선** (더 정확) |
| 접촉면적 | 별도 Stage-E 필요 | ✅ **내장** (▶ 출판본 그림 9: FEM 대비 대체로 작다) |
| 다중이웃·2차접촉 | ✗ | ✅ |
| 벌크탄성 | ✗ | ✅ (ψ_b 필요) |
| **2상(SE+CAM)** | ✅ **가능** (재료별 파라미터) | ❌ **불가** — "varying material properties = future work" (출판본 같음) |
| 다분산 12:4:1 | ✅ | ⚠ 검증범위 밖(0.25까지) + **위상페널티 위험**(§5-3b) |
| 우리 σ 솔버 연결 | ✅ 기존 덤프 규약 그대로 | ⚠ 덤프 포맷·상태변수 매핑 필요 |
| 파괴(Auerbach) | ✅ 유지 | ❌ 없음 (▶ 출판본 부록 G: Δγ 를 충분히 낮추면 *"the tablet will fracture"* — 접촉 분리로서의 파괴는 있다 · 입자 파쇄는 없다) |
| 제하 · 잔류 응력 | ⚠ 우리 hooke/hysteresis 의 이력 | ✅ **실험 대조됨** (▶ 출판본 그림 14 · 잔류 반경 +16 / +81 %) |

★★ **판정: 대체가 아니라 *역할 분담*이다.**
- **경로 A′(Zunker 브랜치) = *pure-SE 단일재료 진위판정*용.**  우리가 정말 답해야 할 질문
  ("연화 없이 Minnmann 10 % @300 MPa 가 나오나")은 **pure-SE 문제**이고, 거기엔 이 코드가 **가장
  좋은 도구**다 (구현 0, 항복캡·면적·다중이웃·벌크 전부 내장).
  ⛔ (2026-11-12 표지) "Minnmann 10 % @300 MPa" 는 정본 `CL-94` 로 **출처 철회** — 외부 앵커가 아니다.  기준은 **랩 표준 순수 SE 기공률 10–13 % · 진밀도 1.64 g/cm³** (CLAUDE.md 11-10 · 고정) 로 읽는다.
- **경로 A(LIGGGHTS 항복캡) = *생산 파이프라인*용.**  2상·다분산·파괴·σ 삼중항이 필요한 곳은
  여전히 우리 코드여야 한다.
- ⇒ **순서**: 먼저 A′ 로 **진위를 싸게 판정**하고, 그 결과에 따라 A 의 사양(상수 H 냐 δ-의존 경화곡선이냐)
  을 정한다.  **A′ 를 건너뛰고 A 를 짜면 "무엇을 맞춰야 하는지" 모른 채 짜게 된다.**

---

## 10. 초기 패킹 ★ (사용자 질문 ⑨)

- **tableting = 완전한 bottom-up.**  4단계: **die filling → compaction → release → ejection** (프리프린트 그림 9c → ▶ 출판본 **Fig 14c** · `fig_14c.png`).
  - die fill (프리프린트): *"20,000 non-overlapping particles sampled from the defined particle distribution are inserted
    homogeneously into the empty die space"* → *"At zero-time the particles are allowed to settle under the
    action of gravity creating a loose packing."*
  - `▶ 출판본 (p.11)`: *"During die filling, 10,000 particles are randomly sampled from the defined particle radius distribution of Appendix F. The sampled particles are then inserted in a spatially homogeneous, but random manner, one-by-one into the entire length of the empty die space between the upper and lower punch … Upon insertion, each particle is assigned zero velocity and its position is checked to ensure it is initially non-overlapping with all other particles … At zero-time the particles are allowed to settle under the action of gravity, towards the lower punch, creating a loose packing."* · µroll 1.0 = *"very loose fill"* · 시작 상대밀도 ≈0.50 [판독].
  - 이후 **입자 추가 없음**.  상 펀치가 **사인파 변위**로 축변형 0.4 까지 압축 (▶ 출판본: 상대밀도 0.85 · 0.99 까지), 같은 사인파로 원위치 복귀,
    하 펀치 상승으로 배출(상 펀치도 같이 올라가 여유 확보).
  - `▶ 출판본`: **두 시뮬이 같은 초기 충전**을 쓰고 위 펀치 행정만 다르다 (p.12) · 영상 1 · 2 가 이 4 단계를 보여 준다 (§7-V).
- **MPFEM 대조 = 좌표 수입.**  Abaqus MPFEM 셋업의 **입자 좌표·반경을 정확히 복제**해서 LAMMPS 에 넣었다.
  ⚠ 그 MPFEM 셋업 자체는 **구성한 것**(14/12 입자)이지 XCT 가 아니다.
- ★ **XCT 수입은 세 논문 어디에도 없다.**  전부 **생성(generated)** 이다.  (출판본 같음.)
- ⇒ **우리와 같은 계보**: 우리도 LIGGGHTS 삽입 + 침전 + 압축이다.  `positioning_vs_geodict.md` 의
  "bottom-up 생성 vs reconstruct-then-compress" 축에서 **Zunker 는 우리 쪽**이다 (GeoDict/ElastoDict 반대편).

---

## 11. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

| 항목 | Zunker 2025 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 코드 | LAMMPS (`mdr` 브랜치, 공개) → ▶ 출판본: LAMMPS 본 저장소 develop | LIGGGHTS | 계보는 같으나 아키텍처가 갈림 |
| 법선 접촉 | **MDR** (항복캡 + 면적 + R 성장 + 벌크) | `hooke/hysteresis` (캡 없음) | ★ 근본 차이 |
| E_SE | **실제값** (MCC 5 GPa, 문헌범위) → ▶ 출판본 **8 GPa** | **1.35 GPa (18× 연화)** | ★ 판정은 §13 |
| 접선 | LH + Coulomb, µ_t **0.7**(튜닝) → ▶ **0.3**, µ_wall **0.1**(튜닝) | µ 0.4 (Bazzoun 계열) | 둘 다 튜닝 축 |
| 롤링 | SDS, µ_roll **0.6**(튜닝) → ▶ **1.0** | 없음 | ⚠ 그들은 **초기 패킹을 롤링저항으로 맞춘다** (출판본: *"very loose fill"*) |
| 감쇠 | CoR = 0.5 (법선만) → ▶ **ηn 점성 + xγ,t 1.0** | COR 0.4 | 유사 (프리프린트) · ▶ 출판본: 속도 범위에서 결과 무관 (각주 6) |
| PSD | 단일재료, R 비 1.5 (Weibull 잘라 씀) → ▶ **1.15** | **12:4:1 삼모드, R 비 0.083** | ★ 우리가 훨씬 극단 |
| **재료 상(phase)** | **1개** (동일 재료).  "varying material properties = future work" | **2개** (LPSCl + NMC811) | ★★ **결정적 제약** (출판본 같음) |
| 초기 패킹 | bottom-up (삽입+중력침전) | bottom-up | **같음** ✓ |
| 검증 타깃 | **σ_axial(ε), σ_radial(ε), 배출력, 잔류응력** → ▶ **σ_axial(RD) · σ_radial(RD) · 잔류 반경응력 · 제하 끝 RD** (배출력 수치는 없음) | **porosity(P), σ_ion/e/th, coverage, CN** | ★ **타깃 자체가 다르다** — 단 ▶ 출판본은 RD 도 보인다 |
| porosity 보고 | ❌ **0개** → ▶ **상대밀도 보고** (정점 · 제하 끝 · 진밀도 기준) | ✅ 핵심 산출 | ⇒ 직접 비교 불가 (프리프린트) · ▶ 단위는 같아졌으나 재료 · 기준이 달라 절대값 비교 불가 |
| 파괴 | ❌ | ✅ Auerbach + fracture-Holm | 우리 우위 |
| 전달 σ | ❌ | ✅ 삼중항 (LOOCV 0.975/0.953/0.903) | 우리 우위 (frame[5]) |
| 형상 | **층(2.75)** — R + 잘린 구관, 재구성 검증 (▶ 출판본: 9 접촉 중 1 놓침 · 등방 하중에 쓰라) | DEM ✗ / **MPM 층(3)** | ★ 우리 MPM 영역이 **좁아졌다** (§6) — 비등방은 여전히 MPM 몫 |
| 벌크·공극소멸 감지 | ✅ `A_free/A_tot` | ❌ | 우리가 못 하는 것 |
| 2차 접촉 생성 | ✅ | ❌ | 우리가 못 하는 것 |
| 다중압력 | 단일 프로토콜(0→0.4→0) → ▶ **두 정점 (96.5 · 297.5 MPa) + 부록 G 민감도** | 4압력 Heckel (100/200/300/600) | ⚠ **우리가 앞선다** — 그들은 압력 스윕이 없다 (▶ 출판본: 정점 둘 · 여전히 '스윕' 은 아님) |
| 자유변수 수 (전체 DEM) | **Y, ψ_b, µ_t, µ_t,wall, µ_roll, t_p, 겹침캡 0.75, (CoR)** ≈ **6–8개** → ▶ 출판본: Y · ψb · µt · µt,wall · µroll · tp · 겹침 상한 0.95 · (ηn) — 개수 같음 | E_eff(1개, 그러나 물성 왜곡) + µ + COR + adhesion | ★ **§13-2 참조** |

---

## 12. ★★★ 적용 인사이트 — 우리가 실제로 할 일 (우선순위순)

### ① ★★★ **결정 실험: pure-LPSCl 을 Zunker 브랜치로 돌린다** (가장 값진 1건)
- **왜 이것 하나인가**: 우리 18× 연화의 정당성은 결국 **"실제 물성으로는 실험 porosity 가 안 나온다"**
  라는 주장인데, 그 주장을 **가장 강한 반례 도구**로 직접 시험하는 것이다.  단일재료라 그들 코드의
  **미해결 제약(2상 불가)에 걸리지 않는다.**
- **셋업**: `E = 22.1 GPa`, `ν = 0.37`, `Y = {0.05, 0.15, 0.30} GPa`, `κ = B₀ = 26.23 GPa`(우리 DFT),
  `Δγ = ?` (⚠ §13-3), `ψ_b = {0.08, 0.28, 0.5}`, PSD = 우리 SE 단일모드(D50 1.0–1.5 µm),
  die 압밀 **100 / 200 / 300 / 600 MPa** (= 우리 Heckel 4압력 그대로).
  `▶ 출판본 반영 (2026-11-12 · 제안)`: ψb 범위에 출판본의 **0.125** 를 넣는다 · 겹침 상한은 0.95 가 기본값 · Δt 는 출판본 계수 0.08 기준 2.0×10⁻¹¹ s 부터.  ⚠ 'Y = {0.05, 0.15, 0.30}' 의 범위 출처는 [미확인] (CLAUDE.md `SELF-160` 표지) — 등록 전에 원문 카드 (나노압입 경도 등) 로 환산 규칙을 먼저 정한다.
- **판정선(런 전에 등록할 것)**:
  - **h0** = "연화 없이도 300 MPa 에서 porosity ≤ 12 %" → **우리 18× 연화의 *설명*이 무너진다**
    (연화 = 빠진 항복캡의 대역이었다).  원고 §연화 절 전면 재작성.
  - **h1** = "porosity ≥ 18 %" (Doux LPSCl 실측 floor 근처) → **연화가 항복캡만으로는 안 되는 무언가를
    담고 있다** = 우리 주장 강화 + 정량화.
  - 사이면 σ_y 감도로 보고.
  - ⚠ (2026-11-12) 판정선의 기준은 **랩 표준 순수 SE 10–13 % (진밀도 1.64)** 로 다시 적어야 한다 — 위 12 % 는 08-25 문장 그대로 둔다.
- ⚠ **비용**: Δt ≈ 9×10⁻¹¹ s (DERIVED; ▶ 출판본 계수로 2.0×10⁻¹¹ s), 입자 3만개 급 → **GPU 없음(LAMMPS CPU)**.  먼저 **1,000 입자
  소형 RVE** 로 스모크 (▶ 출판본 부록 G 도 1000 입자 · Rmax/Rmin 1.15 로 민감도를 돌렸다 — 같은 규모의 선례).
- ⚠ **porosity 규약을 반드시 맞출 것**: 그들은 porosity 를 안 낸다 → 우리가 `ΣV_o/V_box`(= ε_sphere)로
  직접 계산해야 한다.  ★ 다행히 §4-5(①카드)대로 **그들 부피부기와 ε_sphere 는 같은 양**이다.
  `▶ 출판본`: 그들은 상대밀도를 낸다 — 다만 시뮬 쪽 정의가 적혀 있지 않아 [미확인], 우리 규약으로 직접 세는 것이 여전히 안전하다.

### ② ★★★ **Stage-E 상수 H → δ-의존 경화곡선** (비용 ≈ 0, DEM 재실행 불필요)
`H_eff(δ) = Y(1.75 e^{−4.4(δ/2)/R} + 1)`.  우리 overlap 에서 **2.08–2.26 Y** vs 현행 **2.8–3.0 Y**
→ `A_tabor = F/H` 가 **24–44 % 증가**, σ_ionic ∝ √cov 이므로 **σ +12–20 %** (**DERIVED**).
Jackson–Green 2005 가 **같은 방향**을 이미 지시 = **2 독립 출처**.
`▶ 출판본 식 (A.14)` 같은 꼴 확인.  ⚠ 단 출판본 그림 9 는 **MDR 접촉 면적이 FEM 보다 대체로 작다** (끝 합 74 % [판독 · 카드 산술]) — "경화 곡선으로 면적을 키우면 더 맞는다" 는 방향 주장을 할 때 같이 적는다.

### ③ ★★ **`A_free/A_tot` 를 우리 후처리에 추가** (DEM 재실행 불필요)
우리 침대가 벌크탄성 구간에 있는지 정량 판정 + coverage 의 새 분모 + MPM `d_h/dx` 트랙과의 상관.  (출판본 식 A.4–A.8.)

### ④ ★★ **위상 페널티를 우리 규약으로 재검** — §5-3.
(a) 우리 δ/R 에서는 **비활성**임을 확인했으니 *"우리 겹침은 가짜 접촉을 만들지 않는다"* 를 **정량 방어
문장**으로 쓸 수 있다 (▶ 출판본 정확 경계 δ/R > 0.328).  (b) 반대로 **크기-인지 중심판정**은 우리가 제안할 몫 = 작은 방법론 기여 후보.

### ⑤ ★ **무차원 보고 규약 + 3구간 프레이밍** 채택 (①카드 §8-②⑤).  (▶ 출판본 그림 8–10 이 같은 무차원 축: δo/Ro · AC/(πRo²) · F/(E Ro²) · V/Vo.)

### ⑥ ★ **잔류 반경응력을 우리 산출목록에 추가**.
그들 실험 **15 MPa 잔류 반경응력**은 캡핑/래미네이션 결함의 직접 원인이고, 우리 pellet 도 같은 물리를
가진다.  ⇒ 우리 DEM 에서 **die 벽 반력의 해제 후 잔류**를 뽑으면 **새 실험 대조축**이 생긴다
(우리는 지금 porosity·σ 만 본다).  ⚠ 우리 RVE 는 측방 주기경계라 **벽이 없다** → 벽 있는 케이스 추가 필요.
`▶ 출판본`: 잔류 반경응력 **11.5 · 31 MPa** · 그리고 **그들 시뮬의 반경응력은 벽 반력이 아니라 입자 응력 평균 × 부피분율** (§8) — 그러니 주기 경계 RVE 에서도 **같은 방식의 '측방 평균 응력'** 은 잴 수 있다 (벽 없이).  자세히 §16 (다).

---

## 13. ★★★ 3편 관통 종합 판정 (사용자 요청 절)

### 13-1. 사용자 질문 9개에 대한 정면 답

| # | 질문 | 판정 |
|---|---|---|
| **①** | 입자 SHAPE 이 실제로 변하는가 | **부분적으로 그렇다 — 새 층(2.75).**  `겉보기반경 R`(스칼라 1개) + 접촉당 `δ_max` 로 정의되는 **잘린 구** 족.  **사후 역산이 아니다**(힘·신규접촉·벌크발동에 되먹임).  그러나 **자유형상이 아니다**(이방성·오목·내부유동·파쇄 불가).  ⇒ **우리 정본 "층(3) 23년째 아무도 못 함"은 유지되나 "층(2.75)이 열렸다"로 정정 필요.**  ▶ 출판본: 비등방 변형 → 접촉 놓침 (9 중 1) 이 원문으로 확인됐다 |
| **②** | 입력이 R·E·ν·σ_y·γ 뿐인가 / 보정 자유변수는 | **접촉 LAW 자체는 재료별 보정 0.**  피팅은 **정규화 경화곡선 상수 2개(1.75, 4.4)** 뿐이고 **전 재료 공통**이다.  **그러나 3편 전체를 돌리려면 자유변수가 6–8개**: `Y`(문헌 없어 피팅), **`ψ_b`(0.08→0.5 로 6.25× 튜닝)** (▶ 출판본 0.125), `µ_t`(0.7 → ▶ 0.3), `µ_t,wall`(0.1, 배출력에 맞춤), `µ_roll`(0.6 → ▶ 1.0, 초기패킹에 맞춤), `t_p`(50), 겹침캡 0.75 (▶ 0.95), CoR (▶ ηn).  ⇒ **"무보정"은 과장.  정확히는 "*법선 접촉 물성*을 왜곡하지 않는다".** |
| **③** | 입자 부피를 어떻게 다루나 | **구 부피 합을 아예 안 쓴다.**  `V_geo = (4/3)πR³ − Σ(π/3)δᵢ²(3R−δᵢ)` (잘린 구) 이고, **`ΔV = −ΔV_e`**(소성 등적) 를 강제해 **R 이 자라 잘린 부피를 되돌린다**.  탄성분은 `V = V_o(1 + tr(Σf⊗b)/(3κV))`.  (출판본 식 A.23 · A.24 · A.33.)  ★ **우리 ε_sphere(=ΣV_o)는 이 모델이 보존하는 바로 그 양과 tr(ε̄)≈1 % 이내로 같다** ⇒ **ε_sphere 규약이 외부 역학으로 지지된다.**  ⚠ 우리에게 없는 것은 **표면**(자유면적)이 같이 움직이는 것. |
| **④** | 비물리 접촉 선별이 무엇을 고치나 | 대변형에서 **막고 있는 입자를 관통해** 생기는 기하학적 가짜 접촉.  삼중항 각도 α 의 시그모이드 페널티(t_p=50)로 힘에 가중치 w∈[0,1].  ★ **우리 겹침(δ/R 0.15–0.22)에서는 발동 문턱(0.30 · ▶ 출판본 정확 경계 0.328) 아래 = 비활성** → *우리 연화가 가짜 접촉을 만든다*는 걱정은 **기각**.  ⚠ 반대로 **강한 다분산(우리 12:4:1)에서는 홈에 낀 작은 SE 가 정당한 AM–AM 접촉을 소거할 수 있다** (§5-3b, 미검증 영역). |
| **⑤** | 벌크탄성 발동 기준 / Varkey F_mc 대비 | `A_free/A_tot < ψ_b` (남은 자유표면적 비).  힘은 `dF_Bulk = (A_con/V)κ dδ̄_o A_C` (▶ 출판본 식 A.32: 분모 = **V_geo**).  ★ **Varkey 는 평균장 1항(β)으로 럼핑, Zunker 는 2기구로 분해**(R 성장 = 기하 다중이웃 / 벌크 = 공극소멸).  발동도 다르다 — Varkey 는 상시-연속, Zunker 는 문턱-스위치.  필요물성: Varkey ν, **Zunker κ (= 우리 DFT B₀ 26.23 을 바로 씀)**.  자세히 = ②카드 §7-2.  ▶ 출판본: 문턱 전이가 **날카로워** RD 0.8 위에서 축응력을 과소예측한다 (각주 7 · 최저 비 0.74 @ RD ≈0.93 [판독 §3-5]) |
| **⑥** | 도달 상대밀도 / 압력 | **압력은 닿는다**: 최대 축응력 **240 MPa**(우리 300, Doux 370, Minnmann 380 과 같은 계열) — ▶ 출판본 **297.5 MPa** (0.99 시험).  **상대밀도/porosity 는 세 논문에 0개** — ▶ **출판본에서 거짓**: 상대밀도 0.34 → 0.85 · 0.99 → 0.82 · 0.95 (정점 · 제하 끝 · 진밀도 기준).  DERIVED 로 부피비 0.610 만 확실하고, RLP 가정 시 최종 0.90–0.98 (인용 금지 · 프리프린트 형상). |
| **⑦** | MPFEM 이 주고 이들 DEM 이 못 주는 것 | **내부 응력·변형장, 진짜 자유형상, 임의 형상(중공구 등), 다재료 접촉·접착, 파쇄.**  대가는 **비용 2×10⁴–10⁵ 배**(5.5 h/10-proc vs 1 s 직렬, 14 입자).  ⇒ **층(3) 경계 = "내부 필드 + 자유형상"** 이고 그건 MPFEM·**우리 MPM** 영역으로 남는다.  ▶ 출판본 서론도 MPFEM 의 강점으로 *"hollow spheres [32], multi-material compaction [33], and adhesive bonding … large plastic deformations [34,35]"* 를 든다 |
| **⑧** | LIGGGHTS 이식 가능성 / 비용 | **포팅은 수개월급 재구현**(3-패스 구조 + 삼중항 루프 + 병렬 집계통신이 LAMMPS/LIGGGHTS 단일-패스 규약을 깬다).  **대신 그들 브랜치를 직접 쓰는 것이 압도적으로 싸다** (▶ 출판본: LAMMPS 본 저장소).  런 비용: 실제 E 로 가면 Δt 가 **4배** 작아짐(Rayleigh √) + 위 오버헤드.  Zunker 규칙으로 우리 SE 는 **Δt ≈ 9×10⁻¹¹ s** (▶ 출판본 계수 0.08 → 2.0×10⁻¹¹ s).  ⇒ **경로 A 를 *대체*하지 말고 *선행 진위판정*으로 쓸 것** (§9-3). |
| **⑨** | 초기 패킹 = bottom-up 인가 XCT 인가 | **완전 bottom-up.**  die fill(20,000 → ▶ **10,000** 입자 삽입 + 중력 침전) → 압축 → 해제 → 배출.  MPFEM 대조는 FEM 셋업 **좌표 수입**(XCT 아님).  ★ **XCT 는 세 논문 어디에도 없다** = 우리와 같은 생성 계보. |

### 13-2. ★★★ **우리 18× 연화에 대한 최종 판정** (정직 계약 §F1 — 불리해도 그대로)

**판정: *설명*은 반쯤 무너진다.  *결론*은 아직 안 무너진다.  *증명 실험*은 값싸고 우리가 안 했다.**

**(a) 무너지는 것 — 우리 서사의 인과 부분**
CLAUDE.md frame[2] 는 18× 연화를 *"granular 재배열·GB 슬라이딩·미세파괴를 럼핑한 것"* 이라고 설명한다.
Zunker 는 이 설명에 **더 단순한 경쟁 가설**을 세운다:
> 완전소성 구간의 접촉력은 `F ≈ p_Y(δ)·A_geo(δ)` 로 **E 가 아예 들어가지 않는다.**
> 항복캡이 없는 선형 접촉은 `F ∝ E·δ` 라 **E 를 낮추는 것 외에 δ 를 키울 방법이 없다.**

그리고 **우리 접촉은 이미 항복점을 한참 지났다** — LPSCl 에 Zunker eq (41) 을 넣으면 항복겹침은
`δ_Y/R = 0.13 / 1.12 / 4.12 %` (σ_y = 0.05/0.15/0.30 GPa, 구-구 환산)인데 우리 실측은 **14.8 %(복합) ·
22 %(pure-SE)** 다 ⇒ **3.6×–169×, 중앙값 σ_y=0.15 에서 13× 초과** (**DERIVED**).
⚠ (2026-11-12) 출판본 식 (A.22) 은 같은 식의 지수를 **−1.1 δY/R** 로 인쇄했다 (Part I 카드 기록은 −4.4 · 원인 [미확인]).  [카드 산술 — 같은 식을 다시 풂 · E 22.1 GPa · ν 0.37] 위 08-25 값 (두 물체 합성 E/(2(1−ν²)) · −4.4) 0.128 · 1.117 · 4.117 % 는 지수 −1.1 이면 0.128 · 1.143 · 4.469 % (많아야 +9 %) · 출판본 식 (A.11) 처럼 상대를 강체 평면으로 두고 (E*c = E/(1−ν²)) 쪼갠 겹침의 합으로 보면 4 배 작은 0.032 · 0.286 · 1.117 % (−4.4) / 0.032 · 0.288 · 1.143 % (−1.1).  ⇒ 우리 겹침 14.8 % · 22 % 가 항복 겹침을 크게 넘는다는 결론은 어느 꼴이든 그대로 (A.11 꼴이면 넘는 배수가 더 크다).
⇒ ★ **"18× 연화 = 빠진 항복캡의 대역(surrogate)" 이 가장 절약적인 설명이 된다.**

**(b) 안 무너지는 것 — 세 개의 반례**
1. **우리 MPM 은 항복캡(J2, σ_y 0.15–0.30)을 갖고도 연화가 필요했다** (E=24 → 33–38 % porosity).
   ⇒ 캡만으로 전부 설명 안 된다.  (단 2026-06-10 이후 그 연화는 **전단 μ** 로 국한됐고, Zunker 도
   **bulk κ 는 실제값**을 쓴다 — 두 모델이 같은 곳에 연화를 두고 있을 가능성이 있다.)
2. **Zunker 3편 어디에도 porosity 검증이 없다.**  "연화 없이 실험 porosity 도달"을 **아무도 보이지 않았다**
   (So 2021 이 rel.density 0.98 을 보였으나 LPS+Si, 600 MPa, 다른 캡, 2D).
   `▶ 출판본`: **상대밀도 곡선을 실험과 대조했다** — 다만 연화 없이 **실제 E (8 GPa) + 맞춘 Y (77 MPa) + 튜닝 ψb** 로, 연성 유기물 (MCC) 에서, 시작 상대밀도가 0.16 어긋난 채 (입자 안 기공).  ⇒ *"실제 물성 접촉 DEM 이 가압 · 제하 곡선을 상대밀도 축에서 따라간다"* 는 **MCC 에서 처음 보였다**.  황화물 (취성 · 파쇄) 에서는 여전히 아무도 안 보였다.
3. **소재가 다르다**: MCC(연성 유기물, 파쇄 없음) ≠ LPSCl(취성 세라믹, >3 µm 파쇄 — Fan 2026 §3.5).
   Zunker 모델에는 **파쇄가 없다.**  LPSCl 압밀의 일부는 **진짜로 부서지는 것**이고 그건 이 모델이 못 준다.

**(c) 자유변수 회계 — 공정한 대조**
| | 우리 | Zunker 3편 |
|---|---|---|
| 물성 왜곡 | **E 를 18× (24→1.35 GPa)** — 물성 자체를 바꿈 | **없음** (E, ν, κ 전부 문헌값) |
| 피팅 상수 | Stage-E 상수 H, µ, COR, adhesionStiffness | **Y**(문헌 부재), **ψ_b**(0.08→0.5 · ▶ 출판본 0.125), µ_t, µ_t,wall, µ_roll, t_p, 겹침캡 (▶ 0.95) |
| 개수 | 적음 | **더 많다 (6–8)** |
| 성질 | **하나가 매우 나쁘다** (물성 왜곡) | **여럿이 온건하다** (무차원 문턱·마찰) |
⇒ ★ **"그들은 무보정, 우리는 보정"은 틀린 요약이다.**  정확히는 **"그들은 자유변수가 더 많지만 그 중
어느 것도 물성을 왜곡하지 않는다"**.  이것이 진짜 차이고, **우리에게 불리하다**.
`▶ 출판본` 부록 G 가 그 자유변수들의 **손잡이 지도** (잔류 응력에 크게 듣는 것: E · ν · Y · ψb · µt) 를 준다.

**(d) 그래서 뭘 해야 하나** — §12-① 의 pure-SE 결정 실험 하나면 (a)/(b) 사이가 갈린다.
**이 실험을 안 한 채로 원고에 "연화는 irreducible" 을 쓰면, 이 3부작이 리뷰어의 손에 들어가는 순간
정확히 그 문장이 표적이 된다.**

### 13-3. ⚠ 파라미터 전이 시 반드시 확인할 3가지

1. **`Δγ` 단위 함정**: 그들 Avicel `Δγ = 450 J/m²` (▶ 출판본 **900**) 는 **소성소산 포함 유효 파괴에너지**(K_Ic 역산).
   우리 DFT `W_ad = 1.107 J/m²` 는 **열역학** 값이다 (**400× 차이** → ▶ 813×).  그대로 넣으면 점착이 사실상 0 이 된다.
   ⇒ 우리 LPSCl 은 **K_Ic 0.2–0.4 MPa·m^½** (Fan 2026 §3.5) 로부터 `G_c = K_Ic²(1−ν²)/E` 를 써서
   **G_c ≈ 3.24 J/m² (K_Ic 0.3, E 24)** 를 넣는 것이 맞다 (CLAUDE.md 2026-08-06 절과 동일 환산).
   ⚠ (2026-11-12) MDR 의 관계는 `K_Ic = √(2ΔγE*c)` (Δγ = 유효 **표면** 에너지 · 2Δγ = G_c) — 위 G_c 3.24 를 넣으려면 **Δγ = G_c/2 ≈ 1.6 J/m²** 이다 [카드 산술 · 정의 확인 필요].  출판본 부록 G: Δγ 는 압밀 곡선을 거의 안 바꾸고 **잔류 응력 · 파괴**만 바꾼다.
2. **점착 유효조건이 LPSCl 에서 경계다**: `2a/r_Ip ≈ 1.9` (DERIVED, Δγ=1.107, σ_y=0.15) — "소규모 항복"
   조건 `≫1` 을 만족한다고 보기 어렵다.  ⇒ **점착 분기는 켜기 전에 eq (49) 를 실제로 평가할 것.**
3. **δ 환산 규약**: 그들 δ_o 는 **구-평면**, 우리 LIGGGHTS δ 는 **구-구**.  동일 반경이면 `δ_sf = δ_ss/2`
   (본 논문 eq 3/4 가 그것을 코드 수준에서 확인).  **부등 반경이면 eq (3)(4) 로 쪼개야 한다** —
   우리 12:1 이면 SE 가 92 %.

### 13-4. 층위지도 · frame[5] 갱신 요약 (정본 문서에 반영할 문장)

- `contact_models_layer_map.md` §0/§1 — **층(2.75) 행 신설**:
  *"매개변수 형상 상태 — 입자 형상이 상태변수(겉보기반경 R + 접촉당 δ_max)로 살아 힘·**신규 접촉 생성**·
  공극소멸 판정에 되먹임된다.  Zunker & Kamrin 2024 I·II / 2025 가 유일.  자유형상은 아니다."*
  `▶ 출판본 덧붙임`: *"전단이 만드는 비등방 변형은 못 담는다 (2025 부록 E.2 — 9 접촉 중 1 놓침) · 등방 하중에 쓰라 (각주 2)."*
- `elasto_plastic_feasibility.md` §0 표 — Zunker 열 추가, **"(3) 입자 SHAPE 소성 = 23년째 아무도 못 함"**
  을 **"자유형상은 여전히 못 함; 매개변수 형상은 2024 에 열림"** 으로 정정.
- `our_dem_baseline.md` §3 (MPM 고유) — *"진짜 소성 입자 형상변화"* 를
  **"*자유형상* 소성 · 내부 변형장 · 비축대칭 유동 · 재료 이동 기반 void-fill"** 으로 **좁혀 다시 쓸 것**.
  (DEM 도 이제 *배럴링 유사* 형상과 2차 접촉을 낸다.)

---

## 14. 인용 가능 문장 (deck/paper용)

- (프리프린트 판 문장 — ⛔ 240 MPa · 'strain' 표현은 출판본과 다르다 · 인용 금지) "Zunker et al. (Powder Technology 2025) implement the MDR contact model for many interacting particles in
  LAMMPS, validate it against multi-particle FEM for mono- and tri-disperse packings, and reproduce the
  measured axial and radial stress–strain response of Avicel PH102 tableting up to 240 MPa, including the
  finite residual radial stress after decompression — at a cost roughly four orders of magnitude below MPFEM."
- `▶ 출판본 판 (2026-11-12)`: "Zunker et al. (Powder Technol. 459 (2025) 120972) implement the MDR contact model for many interacting particles in the main LAMMPS repository, validate it against multi-particle FEM for mono- and tri-disperse packings (14 and 12 particles; ≈1 s serial DEM vs 5.5 h MPFEM on 10 processors), and compare die-compaction tests of Avicel PH102 to relative densities of 0.85 and 0.99 (peak axial stress 96.5 and 297.5 MPa): axial and radial stress agree beyond a relative density of about 0.6–0.8, the axial stress is under-predicted after 0.8 where the bulk-elastic transition is sharp, and the non-zero residual radial stress after release is predicted (31 MPa measured for the 0.99 test)."
- "They identify a failure mode unique to large-deformation DEM: geometric overlap detection creates contacts
  between particles that are physically separated by an intervening grain, and screen them with a triplet
  angular penalty."  (출판본 같음.)
- "The model carries a per-particle apparent radius and per-contact maximum overlap, from which the
  plastically deformed particle shape can be reconstructed and compared to FEM — a capability absent from
  conventional elastic-plastic DEM."  `▶ 출판본 덧붙임`: "… but it cannot represent shear-induced anisotropic deformation: one of the nine FEM contacts of the examined particle is missed, and the authors restrict the model to predominately isotropic loading."
- (우리 방어용) "The screening applies only at overlaps δ/R ≳ 0.3; at the overlap magnitudes of our beds
  (δ/R = 0.15–0.22) the topological penalty is inactive, so our contact set is free of the through-particle
  artefact." *(DERIVED — 근거는 §5-3a 의 기하 계산 · 출판본 정확 경계 0.328)*

---

## 15. 주의 / 한계 (over-claim 방지)

- ⚠⚠ **단일 재료만.**  *"varying material properties as future work"* (§2.2 · 출판본 §8 결론도).  ⇒ **LPSCl+NMC811 복합양극
  불가.**  pure-SE 만 가능.
- ⚠⚠ **ψ_b = 0.5** 는 *"tuned to trigger the high confinement bulk response stiffening in alignment with the
  experimental results"* 다.  Part II 권장 0.08 의 **6.25배**.  ⇒ **"무보정" 인용 금지.**  `▶ 출판본`: ψb **0.125** (1.56 배) · 같은 튜닝 문장.
- ⚠ **Y 는 피팅값**(Avicel PH102 항복응력 문헌 부재).  ⇒ 축·반경 응력 일치는 **Y 를 맞춘 뒤의 일치**다.  `▶ 출판본`: Y **77 MPa**.
- ⚠ **µ_t, µ_t,wall, µ_roll 도 튜닝**이고, 각각 **고밀도 응력 / 배출력 / 초기 패킹**에 맞췄다 —
  즉 **관측량마다 대응 노브가 있다**.  자유도-관측 매칭이 1:1 이면 예측력 주장은 약해진다.  (출판본 같음.)
- ⚠ **압력 스윕이 없다** — 프로토콜 하나(0→0.4→0)뿐이다.  **우리 4압력 Heckel 이 이 축에서는 앞선다.**  `▶ 출판본`: 정점 둘 (0.85 · 0.99) + 부록 G — 여전히 Heckel 형 스윕은 아니다.
- ⚠ **porosity·상대밀도 보고 0.**  우리 핵심 관측량과 **비교 불가**.  `▶ 출판본에서 거짓` — 상대밀도를 보고한다 · 단 정점 · 제하 끝 값 · 진밀도 기준 (입자 안 기공 포함) · 시뮬 정의 미기재 · 시작값 0.16 어긋남 → **절대값 비교 불가는 그대로**.
- ⚠ **PSD 이상화**: 실제 D50 지름 116 µm ↔ 시뮬 지름 192–288 µm(**약 2배**), 반경비 1.5 로 꼬리 절단
  (**DERIVED**).  "실험 검증"의 입력 분포는 실물이 아니다.  `▶ 출판본`: 278–320 µm (2.4–2.8 배) · 반경비 1.15 · SEM 은 판 · 섬유 조각 모양 (그림 13).
- ⚠ **응력 정의가 절마다 다르다**: MPFEM 대조는 **벽 반력/면적**, tableting 반경응력은 **입자 응력텐서
  평균×부피분율**.  같은 표에 넣지 말 것.  (출판본 같음.)
- ⚠ **위상 페널티는 강한 다분산에서 미검증**이고, §5-3(b) 의 기하 계산상 **우리 12:4:1 에서 정당한
  AM–AM 접촉을 소거할 위험**이 있다.  ⛔ 크기-인지 중심판정으로 고치기 전 우리 침대 적용 금지.
- ⚠ **반경비 검증범위 0.25 까지** (App C → 출판본 부록 C).  우리 0.083 은 **외삽**이고, 0.25 에서 이미 전방재하 일치가
  가장 나빴다.
- ⚠ **파쇄 없음 · 온도 없음 · 소결 없음 · 사이클 없음 · 전달(σ) 없음.**  (출판본: Δγ 를 낮추면 *"the tablet will fracture"* — 접촉 분리로서의 정제 파괴 · 입자 파쇄는 여전히 없음.)
- ⚠ **총 계산시간 미보고**(tableting).  "1초"는 **14 입자 MPFEM 대조**의 값이다 — 20,000 입자 tableting 에
  전용 금지.  (출판본: 10,000 입자 · 여전히 미보고.)
- ⚠ **DOI 미확인** (프리프린트 판).  인용 전 출판판 확인.  `▶ 출판본 확인 완료`: 10.1016/j.powtec.2025.120972.
- ⚠ **소재 전이 금지**: MCC ≠ LPSCl.  **방법·무차원군·알고리즘·판정만** 가져온다.
- ⚠ `▶ 출판본 추가`: **비등방 (전단) 변형은 못 담는다** (부록 E.2 · 각주 2) · **벌크 전이가 날카로워** 고구속 직전 (RD 0.8 위 · 최저 비 0.74 @ ≈0.93 [판독]) 축응력 과소 (각주 7) · **시작 상대밀도 불일치** (실험 0.34 ↔ 시뮬 ≈0.50) · 식 (9) · (A.22) 인쇄 문제 (§0-P P-3).

---

## 16. 본 세션 첨언 (2026-11-12 · 출판본 보강)

> 1저자 11-12: *"추가로 첨언할 내용있음 더 추가해서 보내"*.  원문 근거 줄을 같이 단다.  `[추정]` = 이 카드의 판단 (원문 아님).

### (가) [DEM 우선 (수영)] — "AM + SE 를 가압부터 탈압까지 한 모델로" 와 이 논문이 한 범위

**이 논문이 한 것 (원문 근거)**
- **같은 모델 · 같은 실행 안에서 가압 → 해제 → 배출** 까지 돌렸다 (§7.2 *"four stages: die filling, compaction, release, and ejection"* · 그림 14c · 영상 1 · 2).  우리 사슬 (DEM 가압 → MPM 은 후처리) 과 달리 **끊김이 없다**.
- **제하 곡선을 실험과 대조**했다: 축응력 *"shows good agreement in both unloading cases"* · *"capturing the elastic spring-back of the tablet"* (p.12) · 잔류 반경응력 *"correctly predict the non-zero residual radial stress"* (0.99 시험 +16 % · 0.85 시험 +81 % [판독 §3-5]).
- 접촉 단위의 제하도 FEM 대조 (부록 C · 그림 C.15: *"all of the LAMMPS unloading curves show good agreement with FEM"* — 반경비 0.25 까지).

**못 한 것 (원문 근거)**
- **두 재료 (AM + SE) — 못 한다**: *"varying material properties as future work"* (§2.2 · §8).  ⇒ 수영 트랙의 "AM + SE 한 모델" 의 **절반 (재료 둘)** 은 이 논문 밖이다.
- **상대밀도 시작값을 못 맞춘다** (입자 안 기공 · 0.34 ↔ ≈0.50) · **고구속 직전 축응력 과소** (날카로운 벌크 전이 · 각주 7).
- **비등방 (전단) 형상**을 못 담는다 (부록 E.2) — 저자는 이 논문의 하중을 *"predominately isotropic loading conditions, as studied here"* 로 묶는다 (각주 2 · 단축 다이 압축을 '대체로 등방' 에 넣은 것은 저자 판단).
- 입자 파쇄 · 전달 물성 없음.

**우리 MPM 문헌과 견줌 (정본 카드에서)**
- `nezamabadi2022_mpm_cd_plastic_particle_compaction` — *"제하 (unloading) · 실험 검증은 이 논문에 없다"* (그 카드 L39 · L333) · *"제하는 이 논문에서 얻을 것이 없다"* (L453).
- `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` — *"이 논문은 하중 쪽만 다룬다 (탈압 · 스프링백 없음)"* (L41) · 무른 입자가 초탄성이라 소성 잔류 자체가 없다 (L171).
- `pycompact2025_dem_mpfem_workflow` — **MPFEM (OpenRadioss) 으로 가압 → 제하를 한 계산에서 푼다** (그 카드 L43) · 제하 뒤 상대밀도 (5 MPa 문턱) 를 실험과 대조 — 단 금속 분말 · 2000 MPa · 잔류 반경응력 · 제하 곡선 모양의 실험 대조는 그 카드에 없다 [그 카드 기준].
- (MPM 밖이지만 같은 질문) `demirtas2021_mpfem_hollow_sphere_die_compaction` — MPFEM 으로 압축 + 제하를 풀고 형상 · 스프링백을 그림으로 보이며 실험 (XRCT · eSEM) 과 **경향**을 대조 — 시뮬 응력은 무차원 (E/σy 100) 이라 *"물리 MPa 는 실험 곡선에만"* (그 카드 L21 · L226 · L234).
- (DEM · 오늘 카드) `yano2024_eepa_binary_mixture_plasticity_compression_dem` — EEPA DEM 300 MPa → 0.02 s 유지 → 제하를 NCM–Na₂SO₄ 정제 실험과 대조 — 되돌아옴 Δε 시뮬 0.081–0.088 ↔ 실험 0.028–0.038 · 실험의 잔류 응력 평탄부 8–34 MPa · **경향만** 비교 (그 카드 L36 · L41).
- ⇒ ★ **이번에 본 정본 카드 다섯 (위) 가운데 "제하 곡선과 잔류 반경응력을 실험과 같은 축 (상대밀도) 에 겹쳐 맞춘" 입자 모델은 이 논문뿐이다** [검색 범위 = 위 다섯 카드 · 정본 전체를 훑지는 않았다].
- **수영 트랙에 주는 뜻** [추정]: '한 모델로 탈압까지' 의 **검증 꼴** (같은 실행에서 가압 · 해제 · 배출 → 축 · 반경 응력을 상대밀도 축에서 실험과 겹치기 · 잔류 반경응력 · 제하 끝 상대밀도) 을 그대로 빌릴 수 있다.  재료 둘 · 비등방 · 파쇄는 이 꼴 밖이라 MPM (후보 A · A′) 쪽 숙제로 남는다.

**자세한 분석 — 우리 계획에 무엇을 주나 (정독 지시서 3 절의 이름)**

| 계획의 자리 | 이 논문이 주는 것 | 못 주는 것 · 차이 |
|---|---|---|
| 단계 0 (기공 연산자 · 판정 기준) | 상대밀도 = 진밀도 기준 부피 밀도 (*"RD = ρt/ρ"*) · 정점 (누른 채) / 제하 끝 구분 · 시작 상대밀도 불일치를 원인과 함께 적는 꼴 | 시뮬 상대밀도 정의 미기재 · 랩 표준 (순수 SE 10–13 % · 진밀도 1.64) 과 다른 재료 |
| 단계 4 (3D 순수 SE 로 항복 세기 하나 맞추기) | **같은 일을 MCC 로 했다**: Y 하나를 맞추고 (77 MPa) 나머지는 문헌 · 튜닝 · 1000 입자 민감도 (부록 G) | Y 외에 ψb · µt · µroll 도 튜닝 → '맞추는 값 하나' (R5) 가 아니다 |
| 단계 6 (탈압 · 되돌아옴) | 제하 끝까지의 되돌아옴 (RD 0.99 → 0.95 · 0.85 → 0.82) · 잔류 반경응력 · 그 손잡이 (부록 G: E · ν · Y · ψb · µt) | 배출 뒤 되돌아옴 · 정제 밀도 없음 · MCC |
| 단계 7 (형상 · 피복 · 수송) | 접촉 면적 AC 를 상태 변수에서 직접 (그림 9 — FEM 대비 합 74 % [판독]) | 수송 없음 |
| 후보 D0 (지금의 DEM) | §13-2 의 반례 · 대조 (연화 없는 접촉 DEM 이 MCC 곡선을 따라간다) | 2 상 불가 · 우리 침대에 바로 못 씀 |
| **후보 C (MDR 류)** | **본 논문 = 후보 C 의 현행 최선** — LAMMPS 본 저장소 · 실험 대조 · 제하 · 잔류 | 2 상 · 강한 다분산 (0.083) · 비등방 · 파쇄 |
| 후보 C′ (항복 캡 탄소성 DEM) | 경화 곡선 (A.14) · 날카로운 전이의 부작용 (각주 7) 을 경고로 | — |
| 후보 B (MPFEM) | 14 · 12 입자 대조 설정 · 비용 (5.5 h ↔ 1 s) | — |
| 후보 A · A′ (MPM) | 비등방 · 다재료 · 자유 형상이 MPM 몫이라는 원문 근거 (부록 E.2 · 서론의 MPFEM 강점) | MPM 계산 없음 |
| U3 (단단한 구를 소성 블록에 눌렀다 떼기) | 부록 C 의 반경비 0.25 대조 (작은 입자 완전 항복 · 큰 입자 거의 미항복 · 제하 일치) = 같은 재료 판 | 다른 재료 (AM 단단 · SE 무름) 판은 없다 |
| U6 (작은 조밀 충전 해상도) | 14 입자 MPFEM 배치 = 작은 조밀 충전 대조의 선례 | 해상도 수렴 자체는 없음 |
| R1 (AM 하중 분담) · R4 (탈압) | R4 = 채움 (MCC) · R1 = 없음 (단일 재료) | — |
| R6 (SE 형상 변형) | 매개변수 형상 (층 2.75) · 재구성 | 자유 형상 · 비등방 아님 |
| 결과 전 대조 항목 | **제안**: 우리 탈압 계산의 결과 전 대조 칸에 '측압비 (정점 · 잔류)' 와 '제하 끝 높이 회복' 을 두고, MCC 값 (0.59 / 0.10 / 4.2 % · 0.99 시험) 은 **참고 범위로만** (재료가 달라 판정 기준으로 쓰지 않는다) [추정] | — |

### (나) 우리 LIGGGHTS hooke/hysteresis + 18 배 연화 ↔ MDR 실제 물성 입력 — 우리 침대에 쓰려면

**원문이 말한 것**
- MDR 입력 = E · ν · Y · Δγ (+ ψb) — *"primarily physical material properties"* (§2.1).  체적 탄성률 κ (표 A.2) 가 시간 간격 (§7.1 k = κRmin) · 탄성 부피 (식 A.24) · 벌크 힘 (식 A.32) 에 쓰인다 (κ = E/(3(1−2ν)) 는 카드 산술에 쓴 등방 관계).
- 저자도 다재료가 필요함을 적는다 (§2.2 p.3): *"Industrially relevant powder compaction processes such as pharmaceutical tableting often involves multi-component formulations that span a large range of particle size and material behavior [20]"* · *"a more generic loading capability for the case of many-interacting particles with varying radii and material properties is desirable"*.
- 다체 확장은 **반경만 다른 같은 재료**를 위해 설계됐다 — *"properly handles varying radii, leaving … varying material properties as future work"* (§2.2).  평면 배치 (식 3–4) 는 **기하만** 본다.
- 반경비 검증은 0.25 까지 — 작은 쪽 완전 항복 · 큰 쪽 거의 미항복일 때 전방 재하 오차가 가장 크다 (부록 C).
- 페널티의 중심 판정은 **거리만** 본다 (식 7).
- Part I 검증 범위 E/Y 6.25–200 (Part I 카드) · 출판본 E/Y 103.9.

**바꿔야 할 것 [추정 — 원문 밖 · 우리 제안]**
1. **두 재료 결합 규칙** — 평면 배치를 기하가 아니라 **양쪽의 소성 저항 (pY_i 대 pY_j) 이 같아지는 자리**로 (경도 가중).  AM (NCM, 탄성 140 GPa 급 · 항복 [미확인]) 이 SE (LPSCl) 보다 훨씬 단단하면 평면은 AM 의 원래 표면에 붙고 겹침은 거의 다 SE 몫이 된다 → 같은 재료 기하 배분 (12:1 에서 SE 92 %) 보다 **더 SE 쪽**으로.
2. **AM 을 '강체에 가까운 MDR 입자' 로** — AM–AM 은 Hertz 탄성 영역에 머물 것 (MDR 의 탄성 분기) · AM 의 R 성장 · 벌크 발동은 사실상 꺼짐.  우리 AM-freeze 가정과 같은 쪽.
3. **12:4:1 크기비** — 반경비 0.083 은 검증 밖 (0.25 의 3 배 극단).  **U3 형 대조 (단단한 큰 구 ↔ 무른 작은 구 하나) 를 먼저** — FEM 이든 MPM 이든 — 해야 쓸 수 있다.
4. **삼중항 페널티의 중심 판정을 크기 인지로** (§5-3b) — 그대로면 홈에 낀 SE 가 AM–AM 접촉을 지운다.
5. **물성 입력** — LPSCl: E 22.06 GPa (우리 DFT E_VRH) · ν 0.36 · κ = B₀ 26.23 GPa (우리 DFT) · Y = [미확인 — 환산 규칙 먼저 · `SELF-160`] · Δγ = KIc 기반 유효값 (§13-3, 우리 DFT W_ad 1.107 J/m² 를 그대로 쓰지 않는다).  LPSCl E/Y 는 Y 0.15 · 0.30 GPa 이면 147 · 74 [카드 산술] — Part I 범위 안.
6. 시간 간격 — 출판본 계수 0.08 이면 SE (R 0.5 µm) Δt ≈ 2.0×10⁻¹¹ s [카드 산술].

### (다) 우리 300 MPa ↔ 이 논문의 압력 · 측압비 · 잔류 응력 — 우리 언로딩 (G2c′ · ULK 키트) 과 견줄 값이 되나

- **압력 수준은 같다**: 출판본 0.99 시험 축 정점 **297.5 MPa** ≈ 우리 300 MPa (프리프린트의 240 MPa 보다 더 가깝다).
- **견줄 수 있는 양** (값이 아니라 **꼴**) [추정]:
  1. **측압비** 정점 반경 ÷ 축 = 0.59 (0.99) · 0.44 (0.85) [카드 산술] · 시뮬 0.69 · 0.65 [판독] · 부록 G 기준 ≈0.56 (RD 0.9, [판독]).
  2. **잔류 반경 ÷ 정점 축** = 0.104 · 0.119.
  3. **제하 끝 높이 회복** = 4.2 % · 3.7 % (적힌 상대밀도로) [카드 산술].
- **왜 값을 그대로 견주지 못하나**:
  1. **재료** — MCC (연성 유기물 · 입자 안 기공) ↔ LPSCl + NCM (2 상 · 취성 SE · 단단한 AM).  측압비 · 잔류 응력은 E · ν · Y · ψb · µt 에 민감하다 (부록 G) — 재료가 다르면 값이 다르다.
  2. **경계** — 그들 = 윤활한 강체 다이 벽 (벽 마찰 µt,wall 0.1) · 우리 RVE = 측방 주기 경계 (08-25 카드 §12-⑥ 기록 · ⚠ 우리 키트의 지금 경계 · 산출 항목은 이번에 다시 확인하지 않았다 [미확인]).  주기 경계에서는 벽 마찰이 잔류 측방 응력을 붙잡는 몫이 없다.
  3. **'반경응력' 의 정의** — 그들 시뮬 반경응력은 **벽 반력이 아니라 입자 응력 평균 × 부피분율** (§7.2 p.12) — 그러니 **우리 주기 RVE 에서도 같은 정의 (Σ f⊗b 의 측방 성분 평균) 로 '측방 응력' 을 낼 수 있다**.  08-25 카드 §12-⑥ 의 *"벽이 없어 그대로는 못 잰다"* 는 **이 정의로는 지나친 말**이다 [추정 — 우리 덤프로 실제로 내 본 적 없음].
  4. **G2c′ 와는 견줄 자리가 아니다** — G2c′ 는 재시작 경로에서 접촉 기록이 같은지 보는 **장부 검사**다 (CLAUDE.md 11-04 줄).  이 논문 값과 견줄 자리는 ULK 본 실행 (언로딩 곡선 산출물) 쪽이다 [추정].
  5. **속도** — 그들 실험 가압 1 · 제하 0.25 mm/s · 시뮬은 속도 무관 모델 · 우리 판 속도 0.01 mm/s (CLAUDE.md 10-12) — 비교에 걸리는 축은 아니다 (모델이 속도 무관이라) [추정].

### (라) LAMMPS 구현 (출판본 §2.3) — 우리는 LIGGGHTS: 옮길 때 필요한 것 [추정]

- **원문**: MDR 과 위상 페널티가 *"formally implemented into the main repository of the open-source DEM software LAMMPS"* · develop 가지 · LAMMPS 문서에 사용법 (p.4).  구현 구조 · 명령 이름 · 입력 예는 **출판본에 없다**.
- **가장 싼 길** = 옮기지 않고 **LAMMPS 를 따로 돌린다** (§9-3 경로 A′) — 순수 SE 진위 판정.  필요한 것: ① LAMMPS (develop 또는 MDR 이 들어간 정식판 [미확인 — 판 번호 확인 필요]) 빌드 ② 우리 SE 입도 · 침강 · 압축 덱을 LAMMPS 문법으로 다시 쓰기 (LIGGGHTS `fix insert/pack` · `fix mesh/surface` 같은 메시 벽 → LAMMPS 쪽 대응 [미확인]) ③ 덤프 → 우리 기공 연산자 (ε_sphere) · 접촉망 솔버로 넘기는 변환기.
- **LIGGGHTS 로 옮기는 길** (§9-1 · 08-25 판정 '수개월') — 입자 집계량 (Acon · dδ̄o · Vgeo · R) 을 한 스텝 안에서 접촉 루프 **전후**로 모으고 ghost 통신 · 삼중항 순회 · 쌍당 힘 두 번.  출판본 부록 A 가 식을 다 주므로 **식은 충분**하고, 막히는 것은 코드 구조다.
- **검증 꼴을 같이 옮긴다**: 우리 구현 (어느 쪽이든) 은 출판본 그림 6 · 8–11 (14 입자 MPFEM 대조) 과 그림 C.15 (반경비) 를 **재현 시험**으로 둘 수 있다 — 값이 무차원이라 재료 무관하게 비교된다.

### (마) lit-reader 가지 읽기 카드 (프리프린트 바탕) 에서 출판본 기준으로 고칠 문장 (그 가지는 고치지 않는다 · 매일 밤 다시 만들어진다)

`origin/lit-reader:cards/zunker2025_dem_large_deformation_compaction.md` (2026-11-12 15:17 판) 과 `values/zunker2025_dem_large_deformation_compaction.csv`:
1. 머리 *"doi:n/a (프리프린트 판 …)"* → 10.1016/j.powtec.2025.120972 · Powder Technol. 459, 120972.
2. 요점 2 *"최대 축응력 240 MPa까지의 … 축·반경 응력 곡선과 잔류 반경응력을 재현했다"* → 상대밀도 0.85 · 0.99 두 시험 (축 정점 96.5 · 297.5 MPa · 잔류 반경 11.5 · 31 MPa) · 일치는 RD 0.6–0.8 위 · 0.8 뒤 축 과소.
3. 요점 3 · "어디까지 믿나" *"porosity는 보고되지 않아 · 상대밀도와 porosity는 보고되지 않았고, 압력 스윕 없이 프로토콜 하나뿐"* → 상대밀도 보고 (정점 · 제하 끝) · 시험 둘 + 부록 G 민감도.
4. "정제 실험 재현" 절 *"축변형 0.4 · 최대 축응력 240 MPa · 최대 반경응력 147 MPa · 반경응력 15 MPa · 입자 20,000개 · 배출 축응력 1.2 / 1.5 MPa"* → 출판본 값으로 (배출 수치는 출판본에 없다).
5. "어디까지 믿나" *"Y는 … 19 MPa로 피팅 · ψ_b는 … 0.5로 튜닝"* → 77 MPa · 0.125.
6. "우리 연구에 주는 뜻" *"δ/R 0.299를 넘어야 걸리기 시작"* → 출판본 각주 9 정의 그대로면 0.328 (0.299 는 반올림 경계 0.4).
7. 핵심 수치 표 (240 · 147 · 15 · 1.2 · 19 MPa) → 출판본 값 · "MPFEM 5.5 시간" 은 그대로.
8. "읽을 때 조심할 것" *"ψ_b 0.5는 Part II 권장 0.08의 6.25배"* → 0.125 (1.56 배) · *"지름 192–288 µm"* → 278–320 µm · *"20,000 입자"* → 10,000.
9. "원문에서 먼저 볼 곳" 이 프리프린트 번호 (그림 9 · 그림 C.10) 를 가리킨다 → 출판본 Fig 14 · 그림 C.15.
10. values CSV: 5.85 · 3.57 · 0.6103 · 0.390 · 1 초 · 240 · 147 · 0.61 · 0.32 · 0.08 · 13.1 % · 15 · 1.2 · 1.5 · E 5 · ν 0.4 · xγ,t 0 · γroll 0 · R 96 · 144 · Y 19 · µt 0.7 · µroll 0.6 · Δγ 450 · N 20,000 · ψb 0.5 (두 줄) · CoR 0.5 · E/Y 263 · E*c 2.976 · KIc 1.64 · 400× · 0.35 · 3×10⁻⁸ · κ 8.333 · m 5.78×10⁻⁹ · k 8.0×10⁵ · 2.98×10⁻⁸ · die 부피 294.05 · ρ₀ 범위 · porosity 2–10 % — **전부 프리프린트 값** → 출판본 값 (§0-P) 으로 다시 뽑히면 된다 (이 카드가 바뀌었으니 다음 밤 생성에서 반영될 것으로 본다 [추정]).

---

## 17. [미확인] 목록

- 프리프린트 PDF (`5f242057-Experimentntacts.pdf`) 를 이번에 다시 열지 못했다 → §0-P 의 왼쪽 열은 08-25 카드 기록 · 프리프린트 부록 A 의 내용.
- 식 (A.22) 의 지수 −1.1 (↔ (A.14) · Part I 카드 식 41 의 −4.4) 의 이유 — 오식인지 변수 규약 차이인지.
- 시뮬 상대밀도를 어떻게 셌는지 (입자 부피 합 ÷ 펀치 사이 부피? 겉보기 반경 · 탄성 부피 반영?).
- 영상 1 · 2 ↔ 상대밀도 0.85 · 0.99 대응 (캡션 없음 — 화면 높이 비로 추정).
- 그림 F.19 의 'size' = 지름인지 반경인지.
- MDR 이 들어간 LAMMPS 정식판 번호 · 명령 이름 · 라이선스 표기 (출판본에 없음).
- 우리 ULK 키트의 지금 측방 경계 · 산출 항목 (이 카드에서 확인 안 함).
- 우리 침대 δ/R 0.148 · 0.22 (08-25 기록 · 다시 재지 않음).
- 부록 G 의 제하 끝 상대밀도 ≈0.81–0.82 (0.9 에서 ≈10 % 되돌아옴 · 래스터 그림을 눈으로) 가 정제 시뮬 (6.0 %) 보다 큰 이유 — 원문에 설명 없음.
- 그림 G.20–G.22 값은 래스터 그림을 눈으로 읽은 것 (±0.05 · 벡터 판독 불가).

## 18. 원문 대조 기록 (이 보강 중 직접 확인한 것 · 2026-11-12)

- 서지 · 날짜 · 소속 · 하이라이트 · 키워드 · 자료 공개 · 보충 자료 문장 — 출판본 1 · 2 · 13 · 21 쪽.
- 표 1 · 본문 §2–§8 · 부록 A–H 전부 텍스트로 읽고 크롭으로 대조.  그림 22 · 표 3 · 식 48 전부 열어 봤다.
- 그림 14 판독 방법은 적힌 값 6 개를 재현 (§3-5).  그림 6 · 8–11 · C.15 판독은 눈금 · 틀 환산 (그림 8 은 틀 끝 = −1 · 0.5 · 가운데 큰 눈금 −0.5 로 검산) · 그림 D.16 은 원 경로의 테두리 상자로 중심 · 반경 (지름 79.46 pt).
- Δt = 0.08√(m/k) = 1.1×10⁻⁸ s 재현 [카드 산술].
- 식 (9) 인쇄 (괄호 빠짐) · 식 (A.22) 지수 · 식 (F.1) 의 x 변수 · 본문 `µwall` · 우편번호 02319 — 인쇄 그대로 적었다.
- 영상: ffprobe (길이 · 크기 · 프레임 수) · sha256 · 0.1 s 간격 프레임에서 입자 화소 높이를 잼.

---

## 🔗 관련 카드

- `zunker2024_mdr_contact_model_partI` — 접촉 LAW (경화 곡선 식 16 · 항복 변위 식 41 · 점착) · 3 부작 ①.
- `zunker2024_bulk_elastic_partII` — 벌크 탄성 · ψb 권장 0.08 · 3 부작 ②.
- `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` · `thakur2014_eepa_adhesive_elastoplastic_dem` — EEPA (작은 겹침 · 강성비 이력 · 점착 접촉 · 항복 캡 없음 — 후보 D0 의 같은 층 · morrissey2013 카드 L390 *"C′ 가 아니다"*) — 이 논문의 MDR (후보 C · 큰 겹침) 과 대비.
- `yano2024_eepa_binary_mixture_plasticity_compression_dem` — EEPA 로 **소성비 λp 만 다른 두 종** (크기 · 밀도 · E 같음) 혼합 압축 + 300 MPa 유지 → 제하 + 이종 접촉 λp 규칙 (식 6–7) — 이 논문이 *future work* 로 남긴 '다른 재료 성질' 을 EEPA 쪽에서 한 예 (크기 · 강성 차는 넣지 않았다 · 그 카드 L54).
- `demirtas2021_mpfem_hollow_sphere_die_compaction` — 이 논문의 MPFEM 강점 인용 [32] (중공 구) · MPFEM 압축 + 제하 (§16 (가)).
- `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` — 입자를 푼 MPM · NSCD 압축 (제하 없음 — §16 (가)).
- `pycompact2025_dem_mpfem_workflow` — DEM → MPFEM 가압 · 제하 (금속 분말) — §16 (가).
- `giannis2021_stress_based_multicontact_dem` — 다접촉 평균장 (Varkey F_mc 계보) — §13-1 ⑤.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
