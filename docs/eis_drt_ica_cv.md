# v3-1 — EIS / DRT / ICA / CV (물리-기반, `scripts/eis_drt_ica.py`)

STEP4 확장: 우리 STEP3/STEP4 물리에서 **등가회로 각 소자를 유도**해 임피던스·특성화 곡선을 산출.
frame[4]: 실험 EIS(`eis_fit.py` CNLS 피팅)와 **같은 회로**(R0-p(R1,CPE1)-Wo1)라 **직접 대조 = 교차검증**.

## 회로 (eis_fit 정합)
```
Z(ω) = R0 + R_ct/(1 + jω·R_ct·C_dl) + Z_Wo(ω)
```
| 소자 | 물리 유도 | provenance |
|---|---|---|
| **R0** 직렬/옴 | L/σ_ion + L/σ_e + R_int | STEP3 σ-삼중 + 집전체 앵커 |
| **R_ct** 전하전달 | RT/(F·i0·(α_a+α_c)·a_spec) | STEP4 BV 선형화 (i0·반응면) |
| **C_dl** 이중층 | c_dl_int · a_spec | ★**앵커**(실험 EIS CPE 또는 sulfide\|NMC 문헌 1-10 µF/cm²) — §F1 |
| **Z_Wo** 확산 | R_w·coth(√(jωτ))/√(jωτ), τ=r²/D_s | STEP4 구형 고체확산 (**Warburg 공짜**) |

**핵심 정직(§F1)**: C_dl 은 STEP4 방전솔브가 명시적 범위 밖(τ~ms≪dt)이라 EIS 전용으로 추가 —
**크기는 앵커 필요**. R_w 은 구형-Warburg DC저항 물리추정(O(1) 인자 미정 = ASSUMED-FORM), 실험 Wo1_R 로
교체 가능.  **모양(주파수 위치 ω_ct=1/R_ct C_dl, τ=r²/D)은 우리 물리가 결정 = 예측력.**

## 4 기능
- **EIS** `physics_eis()` / `randles_eis()` → Z(ω) Nyquist. 소자 dict + provenance.
- **DRT** `drt()` (Tikhonov 2차평활 + NNLS 비음수) → γ(τ) 분포 = **R_ct/C_dl/Warburg/GB 시상수 분리**(모델-자유).
  검증: R_ct arc(τ≈R_ct·C_dl) + Warburg 확산(τ≈r²/D) 두 프로세스 자동 분리 (selftest).
- **ICA** `ica_dqdv()` — 방전 V(t)/Q(t) → dQ/dV = **OCP 상전이 피크** (기존 STEP4 방전곡선 후처리, 공짜).
- **CV** `cv_curve()` — OCP + 준평형 dQ/dV × scan-rate + 방향부호 → I(V) (간이; 전 CV solve 는 step4_dyn `--cv-hold`).

## 사용
```bash
python3 scripts/eis_drt_ica.py --selftest                 # 5-검증 (Randles·physics·DRT·ICA·CV)
python3 scripts/eis_drt_ica.py --eis --metrics mpm_metrics.json --c-dl-uf 10   # 케이스 σ→EIS+DRT CSV
python3 scripts/eis_drt_ica.py --eis --sigma-e 1.98 --sigma-ion 2.03e-4 --thickness-um 72.48 --r-int 50
python3 scripts/eis_drt_ica.py --ica discharge.csv        # V,Q 곡선 → dQ/dV
```
실행 예(리뷰-반영): R0=62(=HF절편 R_e+R_int + 전극이온수송 TL DC극한 R_ion/3) · R_ct≈5(φ_AM·coverage
반영) · C_dl · **f_ct=124Hz** · **τ_w=300s(=r²/D)**.  DRT 2피크: **전하전달(130Hz) + 확산(mHz)** 분리 —
실험 Nyquist 위에 겹치면 frame[4] 그림.

## ★ 물리·전기화학 리뷰 반영 (§F1 날조0·방정식0 확인)
- **R0 분리**(리뷰#1): 전극 L/σ_ion 을 전량 HF 직렬에 넣으면 실험 HF절편(eis_fit R0=직렬/접촉)과 3× 어긋남
  → **R0_hf(=R_e+R_int, frame[4] 정합) + R_ion_tl_dc(=R_ion/3, 다공전극 TL DC극한, 중간주파 45° feature)**
  로 분리 보고.  per-element R0 분할은 model-의존 → 총 DC(R0+R_ct+R_w)가 더 신뢰.
- **a_spec = φ_AM·coverage·3/r·L**(리뷰#3): 옛 (1−ε)전고체는 반응면 2-4× 과대→R_ct 과소.  φ_AM(≈75%고체)·
  coverage(SE덮인 AM면만) 반영.  ★a_spec 은 R_ct∝1/a·C_dl∝a 라 **f_ct 서 상쇄**(주파수 불변, 크기만).
- **DRT 프로세스 저항 = basin 적분**(리뷰#2): 옛 단일-빈 height×Δlnτ 는 R_ct ~8× 과소 → 피크 basin(인접
  극소 사이) ∫γ dlnτ.
- **framing 정직화**(리뷰#4): "주파수 위치=예측력" 은 **σ-triad(R0_hf) 한정**; arc f_ct 는 i0·c_dl(둘 다
  미앵커), Warburg τ_w 는 D_s(미측정)가 결정 → 동역학 위치는 앵커 대기(§F1, provenance dict 명시).

## frame[4] 대조 (실험 EIS)
`eis_fit.py` 가 랩 BioLogic .mpr(→ `eis_archive.py`)를 R0-p(R1,CPE1)-Wo1 로 피팅 → R0/R1(R_ct)/CPE(C_dl)/
Wo1(R_w,τ) 추출.  우리 `physics_eis` 가 **같은 소자를 우리 물리로 예측** → 실측과 대조:
- 일치 → 우리 σ-삼중·i0·D_s·구형확산이 EIS를 재현(교차검증).
- 편차 → 정량적 모델-한계(정직).  **C_dl 은 실측서 앵커, 나머지는 예측** = 진짜 예측력 시험.

## ★ webapp 패널 (`/eis`) — BUILT (2026-07-24)
한 페이지에 **Nyquist + DRT γ(τ) + ICA dQ/dV** 3 도구.  `/api/eis`(GET)·`/api/ica`(POST) = eis_drt_ica
단일소스.  SBE/DBE/SC **프리셋** + **`&case=` 자동로드**(DEM `results/<case>` + mpm_lab `<pid>` 둘 다 —
STEP3 σ-triad·두께·porosity만; R_int앵커·i0/D_s스윕·C_dl앵커는 UI 유지).  **mpm_lab 저장목록 각 행에 🔌 EIS
링크**(클릭→그 케이스 σ로 EIS).  소자 카드(R0=hf+ionTL·R_ct·C_dl·f_ct·R_w·τ_w) + §F1 앵커 경고 + **σ_e-필드축
주석**(EIS=이온/R_ct 지배, σ_e는 필드맵 → SBE≈DBE EIS 정상).  코드리뷰 HIGH/MED 0 + LOW 하드닝.

## ★ C_dl/R_w 실험 EIS 앵커 (frame[4]) — BUILT (2026-07-24)
실험 EIS(`이종기술/eis`, eis_fit CNLS)를 physics_eis 앵커로 = 문헌/ASSUMED-FORM 을 실측으로 교체.
- **eis_fit.py**: full-cell CPE(Q,α) ‖ R1 아크 → **Brug/Hsu-Mansfeld 유효 이중층** C_eff=Q^(1/α)·R1^((1−α)/α)
  → `C_dl_uF_cm2`(µF/cm²geo) + `CPE_Q` export + summary_means `full_C_dl_uF_cm2`.  ★발견: **셀간 40-80×
  분산**(No1 ~1440 vs No2 ~18-37) — α 0.33-0.48 **depressed arc** 라 Brug C 가 α-초민감 → **자릿수 앵커**(정밀X).
- **eis_drt_ica.py** `load_experimental_anchors()`: full-cell 로부터 C_dl **기하평균**(로그-분산 대표 ≈192
  µF/cm²geo, 범위 18-1460) · R_w **median**(Wo1_R, 0=미포착 제외 → 73.5 Ω·cm²) · R_int/R0_hf 평균.  파일
  부재 시 None(클라우드 graceful).  `physics_eis(c_dl_areal_uF_cm2=…)` 오버라이드 = 총 이중층 직접(a_spec 곱
  안 함) + intrinsic 역산 표시.  `--use-exp-anchors` CLI.
- **★ frame[4] 교차검증**: 모델 자체 a_spec(25)×c_dl_int(10)=**250 µF/cm²geo** vs 실험 Brug **192**(기하평균)
  = ~30% 내 일치 · 역산 intrinsic **7.67 µF/cm²** = 문헌 1-10 범위 안.  R_w ASSUMED(3.3)→실측(73.5)=20× 보정.
- **webapp**: `/api/eis&expanchor=1` + eis.html **🔬 실험앵커 토글**(C_dl≈192·R_w=73.5·범위·provenance 표시,
  데이터 없으면 문헌 유지) · 소자카드 C_dl int+총(µF/cm²geo) 병기.  검증: py_compile·selftest·node --check PASS.

## ★ D5 — 사이클-N EIS/DRT 궤적 (열화 기전 진단) — BUILT (2026-07-24)
R_int(N) 성장을 EIS 로 투영 → **어느 저항(R_ct arc·확산·접촉)이 자라는지 = 기전 지문**.
- **eis_drt_ica.py** `cycle_eis_trajectory(freqs, base_elems, cycles, growth_mult, rct/r0/rw_share)`:
  base(N=0) 소자 + 사이클별 성장곱수 → 각 N Z(ω)+DRT.  총 성장 ΔR_dc(N)=(mult−1)·R_dc0 를 arc/직렬/
  Warburg 분배(★ASSUMED 0.7/0.2/0.1 = 황화물 접촉손실 지배, §F1) · **집전체 R_int 비열화 고정**(fold
  기준서 제외) · C_dl·τ_w 고정(성장=크기만).  `rint_growth_mult()` = rint_cycle_traj r_of_n 형(끝점측정·
  사이 assumed-form) 재사용 → 기존 사이클 작업과 일관.  `--cycle-traj r0,rc,ntot[,shape,jump]` CLI +
  `_cycle.csv`.  selftest +1(6/6): R_ct 단조증가·성장총량보존.
- **검증 데모**(DBE, R_int 50→125@1000, sqrt): R_ct **5.1→25.8 Ω·cm²(×5)** · f_ct **124→25 Hz**(저주파
  이동=arc 성장) · DRT 피크 134→28 Hz + 확산 mHz 분리 = 접촉손실 지문.
- **webapp** `/api/eis_cycle` + eis.html **🔄 사이클-N 궤적 패널**: Nyquist 오버레이(N=0 파랑→N_max 빨강)
  + DRT γ(τ) 오버레이(자라는 피크) + 프리셋(Kang&Shin B-NCA 50→125·완만 50→80) + 기전요약.  케이스 σ
  로드 시 자동 갱신.  검증: py_compile·selftest·node --check PASS.

## 잔여 (v3-1 후속)
- **완전 AC-solve**(step4_dyn 2.9M-dof 에 소신호 섭동 + FFT) = 미세구조-해상 EIS (지금은 reduced-order 등가회로).
- C_dl 정밀앵커 = **α 높은(덜 depressed) 셀** 재측정 필요(현재 자릿수만) · D5 분배(R_ct/R0/R_w)·C_dl(N)·
  D_s(N) 실측 앵커(현재 ASSUMED) · SOC-의존 EIS.
- ICA **케이스 방전곡선 자동로드 ✅ BUILT (2026-07-24)**: `/api/ica_case?case=<pid>` — 저장된 STEP4
  `st4_viz.json`(mpm_lab `<pid>` + DEM `results/<case>` 둘 다, `step4_viz*.json` glob 포함)의 `curve`
  에서 **V_terminal(측정 전압) + x_mean→용량%**(|Δx|/|x100−x0|×100, §F1: 면적/질량 앵커 부재 → 정규화
  진행률만) 뽑아 `ica_dqdv` 자동 산출.  `/eis?case=` 로드 시 EIS 와 함께 자동 채움(텍스트에어리어 = 소스
  V,Q 로 채워 열람·편집·재계산 가능) · 부재 시 조용히 붙여넣기 폴백(hint).  **EIS 케이스 방전곡선 자동로드**
  (완전 AC-solve)와 **SOC/사이클-N EIS 궤적(D5)** 은 잔여.
- **DRT 사이클 전개**: R_int(N) 성장을 DRT 피크별(R_ct vs 확산 vs 접촉)로 분해 = 열화 기전 진단.
