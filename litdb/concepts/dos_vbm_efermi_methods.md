# DOS · VBM 정렬 · E_F artifact — 수식 기반 입문 노트

> 목적: "DOS가 뭔지, 왜 두 계산의 VBM 절대값을 못 비교하는지, 왜 절연체 E_F를 쓰면 안 되는지"를 **처음 보는 사람도** 수식으로 이해. 슬라이드 21(DOS/E_F)·24(CDD)·25(전자전도) 방어 자료.
> 한 줄: **DOS = 고유값 히스토그램(PDOS는 파동함수를 궤도에 투영) / VBM 0점은 셀마다 달라 정렬 필요 / 절연체 E_F는 smearing이 만든 가짜값.**

---

## 0. 출발점 — DFT가 내놓는 것
Kohn–Sham 방정식을 풀면 각 밴드 $n$, 각 k-점 $\mathbf{k}$ 마다:
$$\hat{H}_{\text{KS}}\,\psi_{n\mathbf{k}} = \varepsilon_{n\mathbf{k}}\,\psi_{n\mathbf{k}}$$
- $\varepsilon_{n\mathbf{k}}$ = **고유값**(에너지 준위)
- $\psi_{n\mathbf{k}}$ = **파동함수**(그 준위의 전자 상태)

DOS·VBM·E_F는 전부 이 둘에서 *후처리*로 나온다.

---

## 1. DOS / PDOS — 파동함수에 무엇을 하나

### 1-1. Total DOS = 고유값 히스토그램
"에너지 $E$ 근처에 상태가 몇 개냐"를 세는 것:
$$g(E) = \sum_{n,\mathbf{k}} w_{\mathbf{k}}\;\delta(E-\varepsilon_{n\mathbf{k}})$$
- $w_{\mathbf{k}}$ = k-점 가중치 ($\sum_\mathbf{k} w_\mathbf{k}=1$)
- $\delta$ = Dirac 델타 → 실제로는 그림용으로 **Gaussian**으로 퍼뜨림(broadening):
$$\delta(x)\approx G(x,\sigma)=\frac{1}{\sigma\sqrt{2\pi}}\exp\!\Big(-\frac{x^2}{2\sigma^2}\Big)$$
- 규격: 점유 상태를 다 더하면 전자 수 → $\displaystyle\int_{-\infty}^{E_F} g(E)\,dE = N_{\text{electrons}}$

→ **Total DOS는 파동함수를 직접 안 쓴다.** 파동함수가 만든 *에너지* $\varepsilon$만 에너지축에 늘어놓는 것.

### 1-2. PDOS = 파동함수를 원자궤도에 "투영"
"이 상태가 S의 p가 몇 %냐"를 알려면 파동함수 $\psi$를 원자궤도 $\phi_{a,\ell m}$(원자 $a$, 궤도 $\ell$=s/p/d)에 **투영**:
$$P^{a,\ell}_{n\mathbf{k}} = \sum_{m}\big|\langle \phi_{a,\ell m}\,|\,\psi_{n\mathbf{k}}\rangle\big|^2 \quad(\text{overlap의 제곱 = 그 상태의 } a,\ell \text{ 비중})$$
$$g_{a,\ell}(E) = \sum_{n,\mathbf{k}} w_{\mathbf{k}}\;P^{a,\ell}_{n\mathbf{k}}\;\delta(E-\varepsilon_{n\mathbf{k}})$$
- $\langle\phi|\psi\rangle$ = 내적(overlap). **여기가 "파동함수에 하는 짓".**
- 완전성: 모든 궤도 합 = 전체 DOS, $\;\sum_{a,\ell} g_{a,\ell}(E)\approx g(E)$.
- 투영 구현: PAW projector $\langle\tilde p|\tilde\psi\rangle$, 원자구 안 구면조화 전개, 또는 LCAO overlap.

### 1-3. 코드 검증 (모의 argyrodite)
```
∫ Total DOS dE = 1.000          (= Σ w_k, 전체 상태수 규격) ✓
Σ_orbital PDOS  = Total DOS      (최대 오차 1e-16) ✓
VBM 근처 궤도 기여: S_p 86% / P_p 7% / Li_s 3% / Cl_p 4%
   → "VBM = S 3p" 가 PDOS로 이렇게 나온다.
```
> ⚠ 주의: DOS 그림의 $\sigma$(broadening, **시각화**)와 §3 E_F의 $\sigma$(occupation smearing, **점유수 계산**)는 **다른 용도**.

---

## 2. 왜 두 계산의 VBM "절대값"을 비교 못 하나 + 맞추는 법

### 2-1. artifact 출처 = G=0 (셀 평균전위) 관례
주기적 plane-wave DFT에서 Hartree 전위를 푸리에 전개하면 **$G=0$ 성분(=셀 전체 평균 전위 $\bar V$)** 은 무한계에서 발산/미정 → **관례로 0**으로 둔다. 그 결과 모든 고유값의 **0점이 "그 셀의 평균전위"** 가 된다:
$$\varepsilon_{n\mathbf{k}}^{\text{(cell)}} = \varepsilon_{n\mathbf{k}}^{\text{(intrinsic)}} + C_{\text{cell}},\qquad C_{\text{cell}}=\text{(셀 평균전위, 미지·셀마다 다름)}$$
따라서 두 셀(조성/부피 다름)의 VBM 차이:
$$\text{VBM}_A-\text{VBM}_B = \underbrace{(\text{VBM}^{\text{int}}_A-\text{VBM}^{\text{int}}_B)}_{\text{진짜}} + \underbrace{(C_A-C_B)}_{\text{미지 artifact}}$$
→ $C_A-C_B$ 를 모르므로 **절대 VBM 비교는 의미 없음.**

### 2-2. 맞추는 법 = 공통 기준으로 정렬
두 셀이 *모두* 가진 **공통 내부 기준** $R$(깊은 core-level, 또는 slab의 진공준위)로 빼면 $C_{\text{cell}}$ 이 상쇄:
$$\Delta_{\text{aligned}} = (\text{VBM}_A-R_A)-(\text{VBM}_B-R_B) \;=\; \text{VBM}^{\text{int}}_A-\text{VBM}^{\text{int}}_B$$
- **rigorous**: **slab** 만들어 진공준위 $V_{\text{vac}}$ → 이온화퍼텐셜 $\text{IP}=V_{\text{vac}}-\text{VBM}$ (절대 기준).
- 또는 **core-level alignment**(깊은 준위), **평균 정전기 전위 정렬**.

### 2-3. 코드 검증
```
물리적으로 동일한 밴드, 평균전위만 V0_A=+1.3 / V0_B=-0.7:
  [raw]    VBM_A=+1.10  VBM_B=-0.90 → 차이 +2.00 eV  (= V0_A-V0_B, 순수 artifact)
  [align]  공통 기준으로 빼면         → 차이  0.00 eV  (진짜)
```

---

## 3. 왜 절연체 E_F를 쓰면 안 되나 (smearing artifact)

### 3-1. E_F의 정의 = N(μ)=N_e 의 해
Fermi 준위(화학퍼텐셜 $\mu$)는 **점유 전자수 = 전체 전자수** 가 되는 $\mu$:
$$N(\mu) = \int g(E)\,f\!\Big(\frac{E-\mu}{\sigma}\Big)\,dE = N_{\text{electrons}},\qquad f(x)=\frac{1}{1+e^{x}}$$
코드는 이걸 **bisection**으로 푼다.

### 3-2. 금속 vs 절연체
- **금속**: $g(E_F)>0$ → $N(\mu)$가 $\mu$에서 **가파르게 상승** → 해가 **한 점**으로 확정.
- **절연체**: 갭 안 $g=0$ → $N(\mu)$가 갭에서 **평평(plateau)** → $T=0$에서 **갭 안 어느 $\mu$든 해** = 미정.
  - 수렴시키려 **smearing $\sigma$** 를 넣으면 밴드가장자리 꼬리가 갭에 스며 $\mu$가 한 점 찍히지만, **그 값이 $\sigma$와 밴드가장자리 DOS 비대칭에 의존** = **artifact**.

### 3-3. 코드 검증
```
절연체 (VBM=-0.20, CBM=2.00, 가전자대 가장자리 dense):
  σ=0.02 → E_F +0.50 | σ=0.10 → +0.93 | σ=0.30 → +1.07 | σ=0.50 → +1.24   (σ 따라 이동)
금속 (E_F 부근 조밀):
  σ=0.02~0.50 → E_F 0.00 (불변)
```
→ **절연체 DFT E_F = 물리값이 아니라 $\sigma$·DOS-edge가 정하는 수치.**

### 3-4. 그래서
- $|E_F - \text{VBM}|$ 로 **조성 간 산화안정성 비교 금지** (슬라이드 21–22에서 고친 오류의 근원).
- 해법: `occupations='fixed'` 로 **VBM/CBM을 직접** 쓰거나, **진공기준 IP/EA**(slab) 또는 **UPS**(실험 절대 기준).

---

## 4. 한 줄 요약
| 양 | 무엇 | 비교 가능? |
|---|---|---|
| **DOS** | 고유값 히스토그램 $\sum w_k\,\delta(E-\varepsilon)$ | 형태(상대) O |
| **PDOS** | $\psi$를 궤도에 투영 $|\langle\phi|\psi\rangle|^2$ → 원자·궤도 character | 상대 O (VBM=S 3p 등) |
| **VBM 절대값** | 0점=셀 평균전위($C_{\text{cell}}$) | **X — 공통 기준 정렬/slab IP 필요** |
| **절연체 E_F** | 갭 plateau + smearing → $\sigma$-의존 | **X — VBM/CBM 직접 or IP/UPS** |

## 5. 재현용 코드 (numpy만)
```python
import numpy as np
trap=getattr(np,"trapezoid",np.trapz)
def G(x,s): return np.exp(-x*x/(2*s*s))/(s*np.sqrt(2*np.pi))
# --- DOS/PDOS ---
eps=np.array([-6.5,-6,-2,-1.6,-1.2,-.8,-.4,-.1, 2.2,2.6,3.2,4]); wk=np.ones_like(eps)/len(eps)
E=np.linspace(-9,6,1501); DOS=sum(w*G(E-e,0.15) for e,w in zip(eps,wk))
# PDOS: char[orbital] = 각 상태의 |<phi|psi>|^2 (합=1) → g_orb = Σ w*char*δ
# --- E_F bisection ---
def fermi(E,mu,s): return 1/(1+np.exp(np.clip((E-mu)/s,-50,50)))
def Ef(levels,Ne,s,lo=-20,hi=20):
    for _ in range(300):
        m=.5*(lo+hi); lo,hi=(m,hi) if sum(fermi(levels,m,s))<Ne else (lo,m)
    return .5*(lo+hi)
ins=np.array([-3,-1.5,-.8,-.5,-.35,-.25,-.2, 2,3.5,5])   # 절연체, Ne=7
for s in (0.02,0.1,0.3,0.5): print(s, round(Ef(ins,7,s),3))  # σ 따라 E_F 이동
# --- VBM 정렬 ---
true=np.array([-3,-2.5,-1,-.2, 2,2.5,3,3.5])
A=true+1.3; B=true-0.7
print("raw ΔVBM", A[3]-B[3], " aligned", (A[3]-A[0])-(B[3]-B[0]))
```
