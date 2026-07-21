# A10 — 사이클 chemo-mechanics 설계 (부피변화 → 접촉손실 → σ(N)·R_int(N))

작성 2026-07-21 (4-에이전트 앵커 리서치 wf_18e8ae4f 기반; 로컬 PDF 정독 = pdf_local,
웹 스니펫 = web_abstract 라벨 — §F1: 아래 수치는 전부 출판값, 추정치 없음).
지위: **설계 초안 — 메커니즘 선택은 사용자 논의 후 확정** (frame 규약: solo-decide 금지).
R_int 풀셀 프로젝트 Phase 3 (docs/project_rint_fullcell_cycling.md §3).

## 0. 한 줄 프레임

우리가 이미 가진 것: 300 MPa 압밀 베드(DEM) + 접촉망 σ 솔버(Kirchhoff/Holm) + 측정
R_int(N) 앵커/궤적 인프라(A11-②) + 압밀-파괴(A9 Auerbach).  A10 = 여기에 **사이클당
AM 부피진동을 가해 접촉망이 열화되는 과정**을 넣어, coverage(N)·σ_e/σ_ion(N)·
R_contact(N)을 **모델 출력**으로 만들고, 측정 R_int(N)과의 갭을 **화학(interphase)
몫**으로 정직 분리하는 것 (R_geom 스플릿의 사이클판).

## 1. 앵커 (전부 출판값)

### 1.1 부피변화 driver — NMC811
| 값 | 조건 | 출처 | 신뢰 |
|---|---|---|---|
| 격자 ΔV **−5.1%** (c 14.467→14.030 Å) | 3.0–4.3 V, in-situ XRD; 악화는 x(Li)<0.5 | Kondrakov 2017 JPCC | web_abstract |
| ΔV 2.4%(NCM111) → **8.0%**(NCM851005) | 충전 시 수축, Ni↑→ΔV↑ | Koerver 2018 EES | web_abstract |
| H2-H3 c-축 ~4% 불연속 수축 | >~4.15 V (Ni≥80%) | Ryu 2018 Chem.Mater. | secondary |
| ★ 2차입자(poly) **+19% 평균/+28% 최대 팽창** — 격자와 부호 반대 (균열부피 9–16%가 열림) | 1회 충전 4.5 V, C/50, same-particle nano-CT | Parks 2023 JMCA (로컬 PDF) | pdf_local |
| NCA 5.9% (ε_d=(Ω/3)Δc_Li) · NMC 5.9% (Ω=1.338e-6 m³/mol) · SC-NMC83 5.5% | FEM 입력/실측 | Kang&Shin 2025 · Yun 2023 · Doerrer 2021 | pdf_local×2, secondary |

방향: 충전(탈리튬) = **수축** → 계면 박리 driver (Bucci 2018).  단 poly 2차입자는
입계균열이 열리며 **거시 팽창** (Parks) — SC와 poly의 사이클 응답이 정반대 부호로
갈릴 수 있음 = per-particle poly/SC 분리(오늘 구현한 D_s/i0 축)와 같은 분류축.

### 1.2 CZM/파괴 파라미터
| 값 | 의미 | 출처 |
|---|---|---|
| **G_c(황화물 SE) = 2.8±1.8 J/m²** (K_IC 0.23±0.04 MPa√m, E 18.5 GPa) | 유일한 실측 황화물 파괴에너지 | McGrogan (Bucci 2017 인용, pdf_local) |
| 균열 개시 **ΔV≈3%** (E_SE=15, G_c=1) · 무손상 조건 **ΔV≤7.5% AND G_c≥4** | 황화물 대표 물성에서 NMC811 ΔV 5.1%는 손상 영역 | Bucci 2017 (pdf_local) |
| **연질 SE가 더 잘 균열** (E_SE 15 ≪ 150 GPa 대비; 비선형 kinematics만 포착) | 황화물 = 취약측; E-의존 부호 주의 | Bucci 2017 |
| Γ = ½k_SE(3β_AM·A_AM)²/(H·G_c) **< 1000 = SE 건전** | 케이스별 스칼라 게이트 (우리 베드에서 즉시 계산 가능) | Bucci 2017 Fig5 |
| 박리 개시 **반경 ~2.5% (부피 ~7.5%)** ; contiguous 50% 박리 → Li 도달시간 **×2.75** | 박리→수송 페널티 정량 (FPT) | Bucci 2018 (pdf_local) |
| bilinear TSL σ_c=100 MPa, G_c=1 J/m²; 10µm 입자 damage→1, 3µm ~0.4 | 랩 FEM 파라미터 (크기의존 입계손상) | Kang&Shin 2025 (pdf_local) |
| ⚠ **AM-SE 계면 γ 실측 부재** (Bucci 1–10 J/m²는 스윕이지 측정 아님) | 정직 갭 — 스윕+밴드로 다룰 것.  ★충전 경로(2026-07-22): DFT 프로그램 Wad 방법론(argyrodite-ml `kb/methodology/adhesion_energy.md`, UMA 검증 R=0.989)으로 NCM/SE 계면 분리에너지 **계산 앵커** 산출 가능 — ML 지도 §7 | Phase 0 조사 재확인 |

### 1.3 접촉손실/R_int(N) 실측 (검증 타깃)
| 궤적 | 값 (Ω·cm²) | 출처 |
|---|---|---|
| ★ B-NCA(3+10µm)/LPSCl 0.5C 100cyc | R_int 113.5→275.6→332.2→335.7→**501.8 (4.4×)**, R_w 70.7→353.4 (5×); retention 47.7% | Kang&Shin 2025 Table S2 (pdf_local, verbatim) |
| U-NCA(3µm 단일) | R_int 56.0→84.5 (**1.5×**), retention 67.3% | 같은 논문 S3 |
| LZO코팅 B-NCA | R_int 36.8→102.5 | 같은 논문 S6 |
| NCM-LPSCl 0.33C 100cyc | R_ion +23%, **R_int +187%** (341.7→982.3) → 계면반응 지배 | Yun 2023 (랩, pdf_local) |
| interphase는 **첫 충전에 대부분 형성** 후 완만 성장 | 첫점프 j의 문헌 근거 | Koerver 2017 |
| SC 84.9% vs PC 65.6% @150cyc (랩, LPSCl) | SC/poly 사이클 격차 검증점 | Jung 2023 (pdf_local) |
| So 2021 DEM: 접촉면적 **첫 사이클 최대 영구손실**; κ 열화는 φ가 아니라 **τ 스파이크(균열)** 지배; P_fab↑→내구↑ | 접촉-원장 모델의 기대 거동 | So 2021 JES (pdf_local digest) |

### 1.4 모델링 접근 지형
- ★ **Alabdali 2024 (ESM 70:103527, Franco그룹)**: LIGGGHTS 강체구 베드(NMC532+LPSCl,
  11k 입자)에 **AM 반경 ±6% 팽창/수축 스크립트** → 응력 재분배 관찰.  **우리 스택과
  동일 도구** = v1 구현 경로의 문헌 선례.  (한계: 접촉손실→σ 전환 없음, 영구손상 없음.)
- So 2021/2025: DEM 2-step (제조+사이클), equilibrium-overlap 소성 ratchet + cohesive 결합.
- Bucci 2017/2018·Kang&Shin·Parks·Taghikhani·Schmidt 2024: FEM/phase-field CZM (연속체,
  frame[5] 상 MPM/FEM 소관 — 입자내부 균열 형상은 우리 DEM 범위 밖).
- Nat.Commun. 2024 (grain-level): 결정이방성까지 — 범위 밖 (참고만).

## 2. 설계 옵션 (논의용)

### 옵션 A — 접촉-원장(contact-ledger) 후처리 v1 ★추천
압밀 완료 베드(atoms.csv)에서 시작, MD 재실행 없이 사이클 N을 **접촉 원장 갱신**으로 전개:
1. 충전 반각: AM 반경 r→r(1−ΔV/3·x_swing) 수축 (SC=격자 −5.1% 앵커; poly는 §3 분기).
2. 각 AM-SE/AM-AM 접촉: 새 gap 계산 → gap>0 이면 **박리 후보**.  Griffith 판정
   (해방 탄성에너지 U_el(δ) vs G_c·A_contact; G_c 2.8±1.8 밴드) → 영구 파단 or 탄성 재접촉.
3. 방전 반각: 재팽창 — 파단 접촉은 **재접촉 금지**(Bucci flux=0 규약; Schmidt식 re-contact은
   v2 옵션), 생존 접촉은 복원.  첫 사이클에 interphase 첫점프(Koerver)를 R_chem 몫으로 병기.
4. 사이클 루프 → coverage(N)·A_contact(N) → **기존 Kirchhoff 솔버 재실행** → σ_e/σ_ion(N),
   Stage-E, R_contact(N).  체크포인트 N∈{1,25,50,75,100} (Kang&Shin 격자와 정렬).
- 장점: 전부 기존 코드 재사용(접촉 재구성·Kirchhoff·Stage-E·A11-② 체크포인트 명령),
  Alabdali 선례, So 기대거동(첫 사이클 최대손실)과 직접 대조 가능.  주말 스케일 구현.
- 한계(정직): 강체구 → 입자내부 균열/소성 재배열 없음(τ 스파이크 과소평가 위험),
  준정적, rate 무관.  SE 크리프/재습윤 없음.

### 옵션 B — LIGGGHTS 재실행 (Alabdali 완전 재현)
반경 진동을 실제 MD로 (per-cycle grow/shrink + 평형화).  응력장·재배열 포함, 그러나
사이클당 압밀 1회 비용×2N — 100 사이클이면 비현실적.  **대표 사이클(1, 2, 10)만 MD로
찍어 옵션 A의 원장 규칙을 보정**하는 하이브리드가 현실적.

### 옵션 C — 경험 R_int(N)만 (A11-② 그대로)
모델링 없이 측정 궤적(양끝고정 밴드)으로 STEP4 체크포인트 전개.  이미 구축됨 —
A10의 **대조군**으로 유지 (모델 성공 판정 = 밴드 안에 들어오는가).

**추천: A (+B 보정 포인트, C 대조군).**  frame[5] 분업 유지: 입자내부 입계균열
형상·연속체 CZM은 랩 FEM(Kang&Shin)/MPM 소관, 우리는 **접촉망 열화 = DEM 소관.**

## 3. poly/SC 분기 (오늘 D_s/i0 분리와 같은 축)
- SC(소립): 격자 ΔV −5.1% 그대로, 입계 없음 → 접촉손실만.  Jung 2023 SC 84.9%가 상한 검증.
- poly(대립): Parks +19%(균열 열림 팽창) — v1은 (a) 격자값 적용 + A9 파괴상태(F/P_c)로
  균열-보정, (b) Kang&Shin 크기의존(10µm damage→1) 반영해 **poly 접촉손실 가중**.
  U-NCA 1.5× vs B-NCA 4.4×(대입자 포함) 격차가 분기 검증 타깃.

## 4. 출력·검증 체인
- 출력: coverage(N), σ_e/σ_ion(N), R_contact(N) [모델], + 측정 R_int(N) − R_contact(N)
  = **화학 몫(정직 노출)**.  STEP4 체크포인트 방전곡선(N) = rint_cycle_traj 명령 재사용.
- 검증: ① Kang&Shin 4.4×/1.5× 모양(첫점프+포화, Bucci 3-stage와 일치) ② So 첫사이클
  최대손실 ③ Yun R_ion +23% (τ 완만↑ — SE-망 온존) ④ Jung SC/PC retention 부호.
- Γ-게이트(§1.2)를 케이스별 사전 스칼라로 출력 (손상 예상 유무 라벨).

## 5. 미결 (사용자 논의)
1. 옵션 A/B/C 조합 승인 여부 (추천: A+B보정+C대조).
2. ΔV 앵커 선택: SC −5.1%(Kondrakov) vs 5.9%(Yun/Kang 계열) — 스윕 축으로 둘 다?
3. G_c 2.8±1.8 밴드를 스윕으로 노출할지, 중앙값 고정할지.
4. 파단 접촉 재접촉 금지(Bucci) vs 확률적 재습윤(Schmidt 2024) — **v1 구현됨**:
   `--recontact forbid(하한)/partial --rewet-frac f/elastic(무열화 상한)`.  스택압↔f 매핑은 미결.
5. 구현 파일: `scripts/cycle_contact_ledger.py` (신규, 후처리) + 기존 솔버 훅.
6. **[리뷰 신규] ov0 층위 혼합**: DEM 겹침(18×-연화 E 규약 길이, real14 AM-SE 중앙 59nm)을
   문헌 절대값 δcr=100nm에서 빼는 것 → δcr을 **캘리브 노브**로 스윕할지, 겹침을 real-E로
   재스케일할지.  완전-탄성 회복(잔류 압평 δ_res 무시)은 개구 과소 방향(보수적).
7. **[리뷰 신규] AM-AM 채널**: 기본은 재폐합(비영구) — 입자내부 전자열화(Parks 균열)는
   frame[5] MPM/FEM 소관.  DEM 접촉-원장은 AM-SE 반응면 열화만 담당 (정정 확정).

## 6. ★ 실전 결과 (2026-07-22) + 3각 리뷰 반영

### 6.1 첫 실런 (WSL, 100사이클)
| 지표 | mono (r_AM 2.5µm) | bimodal (AM_P 6+AM_S 2µm) | Kang&Shin 실측 |
|---|---|---|---|
| N=1 AM_P 즉시파단 | 없음(수축 42nm<δcr) | **있음**(102nm>δcr) | 첫충전 점프 |
| f_broken(AM-SE)@100 | 8.8% | **52.1%** | — |
| **R_ct 접촉-몫**@100 | **1.05×** | **1.51×** | U-NCA **1.5×** / B-NCA **4.4×** |
| σ_ion_rel | 1.000 | 1.000 | R_ion +23%뿐 (Yun) |
| Γ* 게이트 | 393 (건전) | **1,100 (damage-expected)** | — |
→ **bimodal≫mono 방향·즉시파단·포화·Γ* 판별 = Kang&Shin/Yun/Bucci 3앵커 동시 정합.**
헤드라인 진술: "R_int(N) 성장의 접촉-기계 몫 = mono ~1.05×/bimodal ~1.51×, 나머지 = 화학."
⚠ 이 표의 σ_e_rel 열(구판 0.878→0.214)은 **폐기** — §6.2 범주오류.  R_ct·σ_ion은 유효.

### 6.2 3각 적대 리뷰 (wf_60455c5a, 20 검증) → 6건 수정 (커밋됨)
- **[CRITICAL] rnm_sigma 특이계**: 고립/부동 노드(σ_e 계의 SE 전원 등)로 Laplacian 특이 →
  spsolve NaN → 퍼콜 베드를 미퍼콜 오진.  **연결성분 제한**으로 근본수정 (src/snk 담은 성분만).
  대형베드(내 실런)는 CG 경로라 무사했으나 이젠 크기 무관 견고.  selftest 5·6 추가(위양성 차단).
- **[MAJOR] AM-AM 범주오류**: Bucci δcr=100nm는 **SE-상 cohesive TSL**인데 AM-AM 강체접촉에
  영구파단 적용 → 허위 σ_e 열화.  정정: 기본 CZM = AM-SE+SE-SE만, **AM-AM은 스택압 재폐합**
  (비영구, 충전개구는 보고만).  `--aa-czm`로 상한 시나리오 opt-in.  → **σ_e_rel=1.000**,
  열화는 AM-SE 반응면(R_ct)만 = Yun(R_int≫R_ion) 정합.  (입자내부 전자열화 = frame[5] 밖.)
- [MAJOR] 컨덕턴스/면적 프록시 R*(감쇄반경) 누락 → √(R*δ) 수정 (bimodal 가중 정확).
- [MAJOR] --recontact elastic no-op → forbid/partial/elastic 3-모드 + --rewet-frac(§5-4).
- [MINOR] Γ* 라벨 정직화 · checkpoints 가드 · ov0 층위혼합 caveat.
⚠ **재실런 필요**: 최신 코드로 mono/bimodal 재실행 시 σ_e_rel≈1.000 (재폐합).  R_ct·f_broken·
Γ*·σ_ion은 불변 예상 (AM-SE·SE-SE 채널은 수정 무관, R* 추가로 bimodal 가중만 소폭).
