# STEP4 완전 AC-solve 설계 (미세구조-해상 EIS, 연구트랙 킥오프 2026-07-24)

목표: 지금의 reduced-order 등가회로 EIS(`eis_drt_ica.physics_eis`)를 넘어, **STEP4-v2 복셀계
(2.9M-dof e+i 이중망 + BV 계면 + 구형확산)에 소신호 섭동을 걸어 Z(ω)를 미세구조에서 직접** 산출.
등가회로가 가정하는 "단일 R_ct∥C_dl + 단일 Warburg"가 실제 침대에선 **분포**(coverage 불균일·초점
전류·two-class D_s)라는 것을 정량화 — DRT 로 보이던 다중 시상수의 미세구조 기원을 해상.

## 방법 (주파수영역 선형화 — 시간전개 불필요)
운전점(x̄, η_s)에서 STEP4 시스템을 선형화:
```
[ G_e + jω·C_dl,int     −(∂i/∂φ 커플)      ] [δφ_e]   [δI]
[ 커플†                G_i + jω·C_dl,int + Y_diff(ω) ] [δφ_i] = [0 ]
```
- **G_e/G_i** = 기존 STEP3/4 전도 라플라시안 (재사용 — 이미 조립돼 있음).
- **jω·C_dl** = BV face 마다 이중층 (c_dl 앵커 × face 면적) — physics_eis 와 같은 앵커, 이번엔
  **face-분해**(coverage 불균일이 그대로 반영).
- **Y_diff(ω)** = 구형확산 어드미턴스 (해석해: √(jω/D)·coth 형 — RadialDiffusion 을 주파수영역
  폐형으로 대체, per-particle D_s 지원 → SC/poly 가 **다른 Warburg** 를 냄 = bimodal 지문).
- BV 선형화 기울기 ∂i/∂η = i0·(α_a+α_c)F/RT·cosh(…) — step4_dyn Newton 야코비안과 동일 항.

풀이: 주파수 20~30점 × 복소 CG (near-null-B AMG 그대로 — 시스템은 G+jωC 라 ω>0 에서 오히려
더 잘 조건화됨).  시간전개가 없으므로 **CCCV 런보다 훨씬 쌈** (스텝당 CG 1회 × n_freq).

## 산출/검증
- Z(ω) 복셀-emergent → Nyquist/DRT — **균질 극한에서 physics_eis 와 수렴 = 내부 selftest**.
- frame[4]: 실험 EIS(이종기술) 위 겹침 — 등가회로보다 강한 대조 (arc 눌림 α<1 이 미세구조
  분포에서 **자연 발생**하는지가 핵심 질문 = depressed-arc 의 기원).
- 사이클-N: A10 ledger 접촉손실을 face-마스크로 → Z(ω,N) 미세구조-해상 열화 EIS (D5 상위호환).

## 실행 계획
1. `step4_ac.py` 스캐폴드: 소형 합성 grid(CPU) selftest — 균질 침대 → Randles 회귀 확인.
2. V100: 실제 2.9M-dof 케이스 1회 (SBE) → physics_eis·실험과 3-자 대조.
3. (후속) --swcnt/coverage 케이스 스윕 = "어느 미세구조가 arc 를 누르나".

⚠ §F1: c_dl·i0·D_s 앵커 상태는 등가회로와 동일 (자릿수/스윕) — AC-solve 가 새로 정하는 건
**분포와 모양**이지 절대 소자값이 아님.
