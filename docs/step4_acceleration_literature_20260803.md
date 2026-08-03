# STEP4 가속 — 문헌 조사 (2026-08-03)

계기: 0.2C 충전 1회에 **6일** (1843 스텝 × 281 s/스텝, `ev 5`).  사용자 판단
*"이렇게 느리면 그냥 실험을 하지"* — 타당하다.  이 문서는 **우리 병목의 정확한 형태**를 먼저
고정하고, 각 형태에 대응하는 문헌을 찾은 결과다.

⚠ **provenance 규약**: 아래에서
- **[문헌]** = 검색으로 확인한 논문의 주장 (초록/검색 스니펫 수준 — 아래 §6 한계 참조)
- **[우리]** = 우리 코드·실측에서 나온 사실
- **[추론]** = 위 둘을 잇는 내 판단 (검증 안 됨 — 실측 전엔 근거로 쓰지 말 것)

---

## 1. 병목의 형태 (문헌을 찾기 위한 좌표) — [우리]

라이브 로그 + `docs/step4_bottleneck_analysis_20260727.md` 실측:

| 축 | 측정값 | 무엇이 정하나 |
|---|---|---|
| 스텝 수 | **1843** (창 0.6444 traverse) | `dx_max=0.02` 를 **입자별 최대** 표면 SOC 변화에 건다 (`step4_dyn.py:1530`) |
| 이상적 스텝 수 | ~32 | 창/dx_max — 실제는 **57× 초과** |
| 스텝당 V-평가 | **5** (`ev 5`) | 정전류 Illinois 괄호법 (`solve_galv`) |
| 평가당 Newton | 2–4 | 로그: `it0 1.75e-01 → it1 3.56e-05 → it2 2.33e-06 → it3 1.41e-06` |
| Newton 목표 | 1e-08 | **도달한 적 없음** — stall/deep 게이트로 탈출 |
| CG 목표 | `max(rtol·‖b‖, atol_cg)`, `atol_cg = 0.05·agg_floor_abs` | **절대** 바닥 (rtol 아님) |

★ **rate 무관성**: `dt ∝ dx_max/rate` 이고 `t_total ∝ 1/rate` 이므로 **스텝 수는 rate 에
거의 무관**하다.  1C/2C 로 바꿔도 스텝 수는 안 줄고, 줄어드는 것은 **솔브 단가**다
(저율일수록 ‖b‖ 가 작아 rtol 항이 먼저 붕괴 → 거의 모든 솔브가 절대바닥을 쫓는 심층 솔브).

⇒ 가속 지렛대는 **네 개의 직교 축**: ①선형해 조건수 ②블록 구조 ③스텝 수 ④솔브 깊이.

---

## 2. ★ 최대 지렛대 — near-null 공간이 **연결성분 지시벡터**로 정확히 span 된다

### 사실 (수학) — [문헌]
그래프 Laplacian 의 **rank = 노드수 − 연결성분수**이고, 고립 클러스터는 크기와 무관하게
**하나씩** 센다.  즉 성분마다 null 벡터가 **정확히 하나** (그 성분의 지시벡터).

### 우리 상황과의 대응 — [우리]
`step4_bottleneck_analysis_20260727.md` §3-2 실측: **near-null 차원 = O(10⁴) ≫ 12**, 정체의
정체는 "6-conn VGCF 조각의 약결속/부유 모드".  `prune_float` 가 **완전** 부유 성분은 이미
제거하지만(해-불변), 남은 것은 **약결속**(작지만 0 아닌 고유값) 성분들이다.

### 문헌이 말하는 처방 — [문헌]
고대비 계수(high-contrast) 문제에서
- *"극단 고유값의 개수 = 고투과 층의 개수"*
- *"큰 점프로 분리된 대략-상수 투과도 **영역을 그대로 deflation 벡터로** 쓰면, 그 점프가
  만든 극단 고유값의 고유벡터를 잘 근사한다"*
- *"deflated CG 의 수렴이 **계수 점프 크기와 무관**해진다"*
- *"강한 확산 변동 문제에서는 **Jacobi 전처리 + subdomain deflation** 이 가장 좋다"*

(Tang & Vuik 계열: bubbly flow / 저수지 시뮬 — 물리는 다르지만 **행렬 구조가 같다**:
고전도 영역이 저전도 배경에 흩어져 있고 각 영역이 극단 고유값 하나씩을 만든다.)

### 왜 이게 우리에게 특별히 좋은가 — [우리] + [추론]
1. ★ **deflation 벡터를 만들 필요가 없다 — 이미 메모리에 있다.**  `step4_dyn.py:846` 이
   `lab_e, n_lab = ndimage.label(cond_e)` 로 e-망 연결성분을 **매 런 라벨링**한다.  코드 주석이
   직접 말한다: *"6-conn = FV 행렬 결합 그래프와 동일"* — 즉 `lab_e` 는 **우리 행렬의 결합
   그래프 연결성분 그 자체**다.  §2 첫 문단의 수학(성분마다 null 벡터 하나)에 의해
   **`lab_e` 의 각 라벨 지시벡터 = near-null 기저** 다.  [우리, 코드 확인]
   현재는 이 라벨을 **부유 성분 드롭**(AM·집전체 무접촉 = 정확특이)에만 쓰고 버린다.
   남는 것은 AM/집전체에 **약하게** 붙은 성분들 = 작지만 0 아닌 고유값 = 우리 near-null. [추론]
2. ⇒ LOBPCG 12벡터(12–15 s)로 near-null 을 **추정**하던 것을, 공짜로 이미 있는 **정확한**
   기저로 대체할 수 있다. [추론]
3. 문헌의 "점프 크기 무관" 주장이 옳다면, `MPM_S4_CONTRAST_CAP`(σ 대비 상한 — σ_eff −7.8%
   물리 비용을 지불하던 완화책)이 **불필요해진다**. [추론]
4. 현재 nnAMG 의 B-주입(9열)이 coarse 블록을 키워 OOM 위험 + plain 대비 4–5× 느림 (§2-4).
   deflation 은 그 대신 **투영**만 한다. [우리 §2-4 + 추론]

⚠ 미검증: 성분 수가 O(10⁴)면 deflation 공간이 크다.  Tang & Vuik 은 그 규모에서
**subdomain-levelset deflation** 같은 계층화를 쓴다.  우리 규모에서 곧바로 되는지는 **실측
필요**.

---

## 3. 블록/분리(segregated) 전처리 — 우리 J 구조와 정확히 일치

### [문헌] Allen, Chang, Usseglio-Viretta, Graf, Smith (NREL), *J. Sci. Comput.* (2021)
"A Segregated Approach for Modeling the Electrochemistry in the 3-D Microstructure of
Li-Ion Batteries and Its Acceleration Using Block Preconditioners"
- 미세구조-해상 FEM, 수백만 dof.
- **시스템을 두 블록(농도 / 전위)으로 분리** → block-GMRES + **AMG** 전처리.
- **직접해법(MUMPS) 대비 시간 6× · 메모리 1/2.**
- 핵심 근거: *"전극 내 방정식들은 **비선형 Butler-Volmer 를 통해서만** 결합돼 있어서"*
  block Gauss-Seidel 이 성립한다.

### 우리 J — [우리]
`step4_dyn.py:1100-1107` 이 매 Newton 마다 조립하는 것:
```
J = [ A_ee + diag(g)   −diag(g) ]     g = BV 면 컨덕턴스 (면당 스칼라)
    [ −diag(g)   A_ii + diag(g) ]
```
= **전자망 블록과 이온망 블록이 오직 `g` (BV) 를 통해서만 결합.**  NREL 이 말한 구조와 같다.

### [추론] 우리에게 무엇이 이식 가능한가
- **6× 는 그대로 이식 안 된다** — 그들의 baseline 은 **직접해법**이고 우리는 이미 반복법이다.
  이식되는 것은 **속도 배수가 아니라 구조**다.
- 이식 가능한 것: `g` 가 **대각**이므로 Schur 여인수 `S = A_ii + diag(g) − diag(g)(A_ee+diag(g))⁻¹diag(g)`
  가 잘 정의되고, PETSc `PCFIELDSPLIT`(Schur) 가 이 형태를 표준 지원한다 [문헌].
- **이득 가설**: 전자망(near-null 의 근원)과 이온망(잘 조건화)을 **분리**하면, 병든 블록에만
  deflation 을 걸고 건강한 블록은 싸게 푼다.  현재는 **한 덩어리로** 풀어 이온망까지 절대바닥을
  쫓는다.  → §2 와 곱해지는 지렛대.

---

## 4. 스텝 수 — 적응 시간간격 (우리 57× 초과분)

### [문헌] DandeLiion v1 (Korotkin 외), *Newman 모델 초고속 솔버*
- 비균일 staggered 격자 + **적응 시간간격** 유한차분, Newton + JAX 자동미분 Jacobian.
- *"적응 시간간격은 초반에 큰 스텝을 잡고 사이클 후반으로 갈수록 줄여 **고정 스텝 대비 약 2×**
  효율"*, 상용 대비 전체 ~100×.
- 관련: *"High-order adaptive multi-domain time integration scheme for microscale lithium-ion
  batteries simulations"* (arXiv 2310.06573) — **미세스케일** 배터리 전용 적응 시간적분.

### [우리] 우리 것은 적응이 아니라 **클램프**다
`step4_dyn.py:1530` 은 국소오차 추정이 아니라 **`dx_max` 하드 캡 + 초과 시 반감 재시도**다.
게다가 `dxs_meas = max|Δx_surf|` — **입자 하나**가 전체 dt 를 목 조른다.  창/dx_max = 32 스텝이
이상적인데 1843 스텝 = **57× 초과**.

### [추론] 기대치
DandeLiion 의 2× 는 **이미 적응인** 코드 기준이다.  우리는 클램프 → 적응으로 가는 것이므로
**더 클 수 있다**.  다만 `dx_max` 는 정확도 노브라 반드시 **수렴 검사**를 동반해야 한다
(같은 케이스를 dx_max 0.02/0.01 로 돌려 곡선이 안 변하는지).

---

## 5. 솔브 깊이 — oversolving

### [문헌]
- 내부 선형해에 **너무 조인 허용오차**를 주면 "oversolving" — *"고정 허용오차 1e-6 은 훨씬 많은
  GMRES 반복을 쓴다 = oversolving 의 정도"*.
- 처방: **고정 절대 허용오차가 아니라 적응 정지조건**, 즉 외부 Newton 허용오차와 **연동**.

### [우리] 우리는 정확히 그 반대를 하고 있다
`atol_cg = 0.05 · agg_floor_abs` = **절대** 바닥.  Newton 이 수렴할수록 `‖b‖↓` → rtol 항 붕괴 →
목표가 절대값에 고정 (§2-2).  그 절대 목표(≈2.7e-13)는 **Jacobi 자기바닥(1.4e-12)보다 1–2자릿수
아래** — 즉 **도달 불가능한 목표를 매 솔브 쫓는다**.  로그가 그 낭비를 보여준다: 목표 1e-08 인데
`3.94e-05`, `1.41e-06` 에서 탈출.

⚠ EW(Eisenstat-Walker) 는 이미 시도했고 **일량이 늘어 기본 OFF** 로 강등됐다(2026-07-27).
문헌의 처방과 어긋나 보이지만 우리 문서가 이유를 적어놨다: **atol 이 이겨서 EW 가 느슨하게 만들
여지가 없다.**  ⇒ **EW 를 다시 켜는 게 아니라 atol 을 먼저 고쳐야 한다** (순서가 중요).

### 이미 있는 노브
`MPM_S4_ATOL_FLOOR_FRAC` (기본 0.05, **0.5 = opt-in**).  코드 주석: *"0.5로 올리면 심층 목표가
Jacobi 자기바닥 위 = nnAMG 없이 종료"*.  V100 감사 전 기본 변경 금지로 남겨둔 것 — **그 감사가
지금 해야 할 일**.  `solver_env.atol_floor_frac` 가 npz 에 박히니 사후 구분 가능.

---

## 6. 저비용 부수 축 — 혼합정밀

### [문헌]
- FP16 다중격자 전처리 + iterative refinement: *"반복수는 저정밀에 거의 영향 없고, 메모리 전송이
  줄어 **전체 솔버 2.5× 까지**"*.
- Volta 텐서코어 혼합정밀 iterative refinement: **FP64 대비 4–5×**, FP64 안정성 유지.
- *"실무적으로 FP32 는 안전하고 효율적 — mix-FP32/FP64 반복수가 full-FP64 에 근접"*.

### [우리]
`MPM_S4_GPU_AMG_F32` 가 이미 있다 (env 목록 `step4_dyn.py:1990`).  **우리 V100 은 텐서코어가
있다** → 문헌의 4–5× 대역이 원리적으로 열려 있다.  다만 SpMV(33.5M nnz) 지배 구간이라 실이득은
메모리 대역 절감분에 가깝다 [추론].

---

## 7. 문헌에 **없는** 것 (정직한 공백)

- **우리 병리를 배터리 문헌은 이름 붙이지 않았다.** 탄소-바인더(CBD) 서브-퍼콜 → 고립 클러스터는
  *물리* 리뷰로 잘 다뤄져 있으나(Rev. Sust. Energy Rev. 2022 critical review), 그것이 만드는
  **솔버 near-null 병리**를 다룬 배터리 논문은 못 찾았다.  ⇒ 처방은 **수치선형대수 쪽
  (저수지/bubbly-flow deflation)** 에서 빌려와야 한다.  이건 frame[5] 스타일의 정직한 공백이지
  검색 실패가 아니다.
- **정전류 제약을 증강계로 한 번에 푸는 것**(`ev 5` 제거)에 대한 배터리 문헌 인용을 못 찾았다.
  ⚠ 모듈 docstring 은 "supernode-정전류 구조" 를 말하지만 **코드는 반대로 적혀 있다** —
  `step4_dyn.py:868` `self.N = self.n_e + self.n_i   # Dirichlet 구조 (supernode 없음)`.
  즉 지금 정전류는 **전적으로 외부 Illinois 괄호법**(`ev 5`)이 담당한다. [우리, 코드 확인]
  구현 여지는 있으나 문헌-무근거(=[추론] 전용)라 아래 우선순위에서 최하위로 둔다.

### ⚠ 검색의 한계 (반드시 감안)
Springer(`10.1007/s10915-021-01410-5`) · OSTI · arXiv PDF 가 **전부 403** 이었다.  위 인용은
**초록/검색 스니펫 수준**이고 **본문 방법 세부는 확인 못 했다.**  숫자를 논문에 인용하려면
WSL 에서 PDF 를 직접 받아 확인할 것 (§9 목록).

---

## 8. 우선순위 (기대이득 × 비용 × 위험)

| # | 지렛대 | 근거 | 기대 | 비용 | 위험 |
|---|---|---|---|---|---|
| **1** | `MPM_S4_ATOL_FLOOR_FRAC=0.5` A/B | §5, 이미 구현 | 심층 솔브 제거 — **최대 단일 지렛대** | **0** (env var) | 해 품질 → E-bal/KCL/`galv_miss` 로 판정 |
| **2** | 연결성분 deflation | §2, 벡터를 **이미 계산함** | 조건수 근본 해결 + `CONTRAST_CAP` 물리비용 제거 | 중 | 성분 O(10⁴) 규모 미검증 |
| **3** | 적응 dt (국소오차) + `dxs` max→분위수 | §4 | 스텝 수 (현재 57× 초과) | 중 | **정확도 노브** — 수렴검사 필수 |
| **4** | 블록/Schur 분리 | §3 | 병든 블록에만 비싼 처리 | 중~대 | 재구조화 |
| **5** | FP32/혼합정밀 확대 | §6, 부분 존재 | 1.5–2.5× | 소 | 정밀도 |
| 6 | 정전류 증강계 (`ev 5`→1) | [추론]만 | ~2–3× | 중 | 문헌 무근거 |

**순서가 중요하다**: ①을 먼저 해야 ②·⑤의 효과가 보인다 (지금은 절대바닥이 모든 것을 가려서,
전처리를 개선해도 도달 불가 목표를 쫓느라 이득이 안 나타난다).  EW 재시도는 ① **이후**.

---

## 9. 참고문헌 list-up (WSL 에서 PDF 확보할 것)

1. Allen, Chang, Usseglio-Viretta, Graf, Smith — *A Segregated Approach for Modeling the
   Electrochemistry in the 3-D Microstructure of Li-Ion Batteries and Its Acceleration Using
   Block Preconditioners*, **J. Sci. Comput.** (2021).  DOI `10.1007/s10915-021-01410-5`
   (OSTI 1765036 / NREL research-hub).  ★우리 J 구조와 동일, 블록+AMG.
2. Tang & Vuik — *Two-level preconditioned conjugate gradient methods with applications to
   bubbly flow problems* (TU Delft) · *Efficient deflation methods applied to 3-D bubbly flow
   problems*.  ★고대비 deflation 정본.
3. Vuik 외 — 극단 대비 계수에 대한 deflated ICCG 의 **투영벡터 구성**.  ★"영역 = deflation 벡터".
4. Gupta 외 — *Evaluation of the deflated preconditioned CG method to solve bubbly and porous
   media flow problems on GPU and CPU*, **Int. J. Numer. Meth. Fluids** (2016).  ★GPU 실적.
5. *The Parallel Subdomain-Levelset Deflation Method in Reservoir Simulation*, arXiv 1510.02148.
   ★성분 수가 클 때의 계층화.
6. Korotkin 외 — *DandeLiion v1: an extremely fast solver for the Newman model of lithium-ion
   battery (dis)charge*, arXiv 2102.06534.  ★적응 dt 2×.
7. *High-order adaptive multi-domain time integration scheme for microscale lithium-ion
   batteries simulations*, arXiv 2310.06573.  ★미세스케일 전용 적응 시간적분.
8. Wu, Srinivasan, Xu, Wang — *Newton-Krylov-Multigrid Algorithms for Battery Simulation*,
   **J. Electrochem. Soc.** (2002).  ★block-GS + MG 선례.
9. *Parallel, physics-oriented, monolithic solvers for 3-D coupled FE models of Li-ion cells*,
   **Comput. Methods Appl. Mech. Eng.** (2019).  ★monolithic 반대 견해 (분리 vs 일체 비교용).
10. *Accelerating Geometric Multigrid Preconditioning with Half-Precision Arithmetic on GPUs*,
    arXiv 2007.07539.  ★혼합정밀 2.5×.
11. *Advances in Mixed Precision Algorithms: 2021 Edition* (OSTI 1814447).  ★서베이.
12. Entwistle 외 — *Carbon binder domain networks and electrical conductivity in lithium-ion
    battery electrodes: A critical review*, **Renew. Sustain. Energy Rev.** 166 (2022) 112624.
    ★우리 near-null 의 **물리적** 근원 (서브-퍼콜 CBD) — 솔버 처방은 없음.

---

## 10. 다음 행동

0.2C 가 끝나는 대로 **같은 침대 · 1C** 에서:
1. `MPM_S4_ATOL_FLOOR_FRAC` 0.05 vs 0.5 **A/B** — E-bal · KCL · `galv_miss` · delivered% ·
   벽시계.  일치하면 캠페인 기본으로 승격 (`solver_env.atol_floor_frac` 가 런을 구분해 준다).
2. 그 다음에야 ② deflation 프로토타입 (성분 지시벡터는 이미 있으니 투영만 얹으면 됨).
3. ③ 적응 dt 는 **수렴검사와 한 쌍**으로만.
