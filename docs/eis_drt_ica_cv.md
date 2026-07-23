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

## 잔여 (v3-1 후속)
- **완전 AC-solve**(step4_dyn 2.9M-dof 에 소신호 섭동 + FFT) = 미세구조-해상 EIS (지금은 reduced-order 등가회로).
- C_dl **실험 앵커**(eis_fit CPE1_Q → µF/cm²) 배선 · R_w 실험 Wo1_R 채택.
- webapp /step4 패널에 Nyquist·DRT 표시 · SOC/사이클-N EIS 궤적(D5 R_ct/C_dl/Warburg 시그니처).
- **DRT 사이클 전개**: R_int(N) 성장을 DRT 피크별(R_ct vs 확산 vs 접촉)로 분해 = 열화 기전 진단.
