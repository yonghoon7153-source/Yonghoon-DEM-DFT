# 문헌-앵커 generalizable reference R_int(N) 설계 (Phase 1)

정의일 2026-07-20.  프로젝트 `docs/project_rint_fullcell_cycling.md` Phase 1의 핵심 설계.
앵커 데이터 조사는 `docs/rint_anchor_db_research.md`(Phase 0) — 이 문서는 그 위에 **성장-법칙 + 전이성 설계**를 얹는다.

## 0. 발단 (사용자 질문 2개, 2026-07-20)
1. **"R_int을 초반·후반만 앵커하고 사이클 따라 유동적으로 바뀌게 안 되나?"** → 유동적 R_int(N) 궤적.
2. **"이건 SDCP 들어간 특이 케이스고, reference는 문헌값으로 하면 안 되나? 앞으로 bimodal 등 여러 개 할 건데."**
   → reference = 문헌 앵커, 특이 재료(SDCP)만 자기 실측, 그리고 **여러 config(bimodal/mono/크기별)로 확장.**

이 둘을 합치면 §F1(정직: 예측 가능=OUTPUT, 예측 불가=측정앵커, 날조·보간 금지)에 정확히 부합하는
아키텍처가 나온다.

## 1. 왜 2점 앵커만으로는 부족했나 (Q1의 문제)
pristine(신선)·cycled(사이클후) **두 점**만 있으면 그 사이 곡선은 **무한히 많다** — √N이냐 선형이냐
포화냐에 따라 중간 사이클 값이 크게 갈린다.  2점 보간 = **"가정한 형태"** 이지 측정이 아님 → §F1 원칙 #2
위반(보간·눈대중 금지).  **해결: 문헌이 "모양(성장 법칙)"을 준다.**

## 2. ★ 핵심 아키텍처 — SHAPE(문헌) × MAGNITUDE(우리 모델) + delta(실측)

```
R_int(config, N)  =  R_ref(N)  ×  S(config)  [+ Δ_special(config)]
                     └─ 문헌 ─┘   └ 우리 OUTPUT ┘   └ 자기 실측 ┘
                     성장법칙 모양    구조 스케일        특이재료 편차
```

- **R_ref(N) = 문헌-앵커 reference 성장-법칙** (§3).  표준 NMC811/LPSCl 복합양극의 R_int(N) *모양* +
  기준 크기.  = **측정앵커(literature)**, 여러 config에 공통.
- **S(config) = 구조 스케일 인자** = 우리 DEM/MPM이 config마다 계산하는 **coverage/접촉면적**에서 유도.
  물리: Holm 수축저항 R ∝ 1/(σ·a_contact), Stage-E 소성 접촉면적 → **R_int ∝ 1/coverage** 근사.
  ```
  S(config) = coverage_ref / coverage(config)      (1차 근사; §4 성립조건)
  ```
  = **모델 OUTPUT**.  → **bimodal이든 mono든 자기 구조로 스케일** = 하나의 문헌 reference가 전이.
- **Δ_special(config) = 특이재료 실측 편차** (§5).  SDCP처럼 문헌 reference로 안 잡히는 재료는
  사용자 자기 실측으로 override/보정.  = **user-lab 측정.**

**이 구조가 "앞으로 bimodal 등 여러 개"를 정직하게 커버하는 이유**: config마다 논문을 못 구하니까,
문헌은 *모양*만 주고(공통), *크기*는 우리가 이미 config마다 뽑는 coverage로 스케일 → 날조 없이
새 config(bimodal)로 확장.  SDCP만 예외적으로 실측 delta.

## 3. Reference 성장-법칙 R_ref(N) — 형태 (문헌 앵커)

### 3.1 형태 (정성적으로 확정, §F1: SHAPE는 measured, 계수는 확인중)
문헌 합의 = **첫-사이클 점프 + 완만한 성장**:
```
R_ref(N) = R_0 · [ 1 + j·H(N≥1) + g(N) ]
  R_0  : pristine(신선) 계면 ASR 바닥
  j    : 첫-사이클 점프 비율 (interphase가 1st charge에 대부분 형성 — Koerver 2017)
  g(N) : 완만 성장 — 후보:  (a) √N  (확산-제한 interphase 두께 성장)
                            (b) k·N (접촉손실·크랙 누적, 선형)
                            (c) 포화 A(1−e^(−N/τ))
```
- **첫-사이클 점프(j)** — Koerver 2017 (10.1021/acs.chemmater.7b00931): "interphase는 주로 first
  charge에 형성, 이후 완만" = 이 SHAPE의 문헌 근거.  `precision=confirmed_snippet`.
- **완만 성장 g(N)** — 어느 형태(√N/선형/포화)가 맞는지 = **Conforto 2021 per-cycle R_ct 테이블**
  (10.1149/1945-7111/ac13d2)로 fit해야 확정.  ⏳ **WSL PDF 디지타이즈 대기.**

### 3.2 알려진 절대 앵커 (Phase 0 §2에서, precision=confirmed_snippet)
| 양 | 값 | 조건 | 출처 | 역할 |
|---|---|---|---|---|
| R_0 (pristine 바닥) | **≈ 40 Ω·cm²** | NMC(SC)/LPSCl, 비대칭압 2.5/0.2 MPa, 30°C | acsami.1c07952 | R_ref pristine 앵커 |
| (벤치 하한) | 7.6 Ω·cm² | LiPON 모델계면 | 리뷰 | 하한 참조 |
| 성장(집계) | R_ct **593.8 → 350.9 Ω / 300cyc** | 개질 NCM811-sulfide | Feng 2025 cssc.202501033 | 성장 크기 감(주의: 감소=개질효과) |
| 접촉손실 성장 | ~100 → ~300 Ω (×3) | LPSCl/LLZO 이중층 | acsaem.5c02435 | 접촉손실 크기 감(2차) |

⏳ **에이전트 3종(2026-07-20 실행중)** 이 (i) g(N) 형태·계수, (ii) 집전체 접촉 R 성장,
(iii) 모델링 파라미터화(ASR-vs-BV) + 전이성 근거를 보강 → 확정 후 이 표 갱신.

## 4. 전이성 S(config) — 성립 조건과 한계 (정직)

**성립 근거 (R_int ∝ 1/coverage 방향)**: Holm 수축저항(접촉면적↑→R↓) + 우리 Stage-E가 이미 쓰는
소성 접촉면적 논리 + 문헌 경향(fine LPSCl R_ct < coarse — Zhou 2025 acsenergylett.4c03256;
SC vs poly NMC R_int 차 — Conforto 2021).  ⏳ 에이전트가 "ASR ∝ 1/접촉면적" 명시 근거 확인중.

**깨질 수 있는 곳 (over-generalization 위험 — 절대 무비판 전이 금지)**:
- **화학 interphase 항**은 접촉면적이 아니라 *반응성·전위*가 지배 → coverage 스케일 대상 아님
  (R_ref의 화학 성장분은 config-공통으로 두고, 기하분만 S로 스케일하는 2-항 분리가 더 정확).
- **압력·온도** 절대 R_int을 크게 움직임 → S는 *같은 압력/온도* 비교에서만.
- **chemistry(SE/양극) 전환** 시 R_ref 절대값 자체가 달라짐 → LPSCl/NMC811 계열 내에서만 reference 재사용.

→ 그래서 S(config)는 **"같은 chemistry·압력·온도에서 config 간 상대 스케일"** 로만 쓰고,
절대 이식은 R_ref 앵커 조건을 라벨.  (에이전트 verify가 이 위험도 등급화중.)

## 5. SDCP / 특이 케이스 = 실측 delta
- SDCP는 혼성전도 배달부라 문헌 reference(표준 VGCF/PTFE)로 안 잡힘 → **사용자 실측(배영진 펠릿/필름/
  cell EIS)** 로 Δ_special 또는 R_int override.
- 우리 자기 endpoint(SBE 18→110, DBE 12→46, C-SUS 10→30 Ω·cm² @1000cyc 2C)는 **user-lab 측정앵커** —
  R_ref의 *절대 스케일*을 우리 셀에 맞추는 데 사용(문헌은 모양, 우리 endpoint는 크기 고정).

## 6. 두 시간-일관 시나리오 (σ_apparent MIX 해소)
절대 섞지 않는 두 세트:
- **pristine (fresh+fresh)**: BOL 구조 + **pristine R_int(~18/12/10, panel e — 디지타이즈 필요)** = R_ref(N=0).
- **cycled (aged)**: 별도 "노화 시나리오" 라벨, **post-cycling R_int(110/46/30)** = R_ref(N=large).
현재 σ_apparent가 **fresh 벌크 + aged 계면**을 섞은 것(§project 6.1)을 이 분리로 교정.  R_ref(N)이 이
두 끝점을 잇는 궤적을 문헌 모양으로 채움.

## 7. step4_dyn 배선 (인프라 이미 있음)
`scripts/step4_dyn.py`:
- `--r-int-ohm-cm2` (기본 0.0) → 직렬 옴성 필름: `V_term = V_cell − I·R_int` (집전체/필름 ASR).
- `--asr-film` → SEI/CEI 필름 항.
- **반응 계면(AM|SE, AM|SDCP)** 은 Butler-Volmer i0(η_kin)로 이미 분리 — R_int(집전체)과 **다른 계면**.
→ 배선 = **DB 값을 이 플래그로 주입 + 출처 태그** (플래그 생성 아님).  전극-내부(R_int=0) 기본 유지,
풀셀 축은 명시 옵션.

## 8. §F1 정직 원장
| 입력 | 종류 | 근거 |
|---|---|---|
| R_geom (기하 집전체 저항) | **OUTPUT(모델)** | L·(1/σ_bare−1/σ_wetted), SBE 1.37e-5/DBE 9.05e-6 Ω·cm² |
| coverage(config) → S(config) | **OUTPUT(모델)** | DEM/MPM Stage-E 접촉면적 |
| R_ref(N) 모양 (첫점프+g(N)) | **측정앵커(문헌)** | Koerver/Conforto/Feng, precision 태그 |
| R_0 40 Ω·cm², 성장 크기 | **측정앵커(문헌)** | §3.2, confirmed_snippet |
| SBE/DBE/C-SUS endpoint 18→110 등 | **user-lab 측정** | Fig6e (사이클#·pristine EIS 디지타이즈 대기) |
| g(N) 형태 미확정분 | **assumed-form (라벨 필수)** | Conforto per-cycle fit 전까지 √N 가정 = 모델, 측정 아님 |

## 9. GAP (닫으려면 필요)
- ⏳ **Conforto 2021 / Koerver 2017 per-cycle R_ct 테이블 (WSL PDF 디지타이즈)** → g(N) 형태·계수 확정.
- ⏳ **pristine 집전체 EIS(사이클 전) + 중간-사이클 EIS** → 2점이 아니라 궤적 앵커(있으면 갈래1, 없으면 √N 라벨).
- ⏳ **"ASR ∝ 1/접촉면적" 명시 문헌** → S(config) 스케일 정당화(에이전트 확인중).
- ⏳ SDCP E_bind DFT (gabia) → Δ_special 물리 근거.

## 10. 상태
- 2026-07-20: 설계 정의.  reference=문헌·SHAPE / magnitude=우리 coverage / SDCP=실측 delta 아키텍처 확정.
  성장-법칙 계수·전이성 근거 = 에이전트 3종 조사중 → 반영 예정.
