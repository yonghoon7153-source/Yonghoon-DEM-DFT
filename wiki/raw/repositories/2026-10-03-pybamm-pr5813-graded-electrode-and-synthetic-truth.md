---
source_url: https://github.com/pybamm-team/PyBaMM/pull/5813
ingested: 2026-10-03
sha256: 3d66560acf445daa5e06679d865342f0e1334d1c97412468ef89700c73a0b81c
---

수집 목적: 의존성 위험 감시 (일일 브리핑 ① 축) — PyBaMM PR #5813 (2026-09-30 병합 · 26.9.0.0 미포함) 이 (가) 브리핑이 제안한 구배 전극 조건에서 실제로 무엇을 고치는가, (나) **우리 합성 truth 경로** 에 닿는가를 실측한다. 사용자 지시 2026-10-03 "관련해서도 확인을 해보고 사용가능한지 판단을 해보고".

---

# PyBaMM #5813 — 구배 전극 LLI · 총 리튬 시험 + 우리 합성 truth 두 조건 (2026-10-03 실측)

## 조건 · 격리

- 수정 전 = 운영 설치본 `pybamm 26.8.0.0` (`/usr/local/lib/python3.11/dist-packages/pybamm` · solver 지문 pybammsolvers 0.9.1 · casadi 3.7.2).
- 수정 후 = 그 설치본을 스크래치패드로 복사한 사본 (`…/scratchpad/pr5813/site/pybamm`) 에 #5813 (`bd572504`) 의 `expression_tree/averages.py` 고침 세 덩이를 덧댄 것. 둘째 · 셋째 덩이 (나눗셈 분할 규칙) 는 `patch` 로 그대로 들어갔고, 첫째 덩이는 26.8 의 문맥 한 줄이 develop 과 달라 (`node.domain` ↔ `node._domains["primary"]`) 같은 내용 (`not node.children` · 모든 도메인 검사) 으로 손으로 바꿨다. 다른 파일 · 테스트는 덧대지 않았다. `PYTHONPATH` 로 사본을 먼저 읽는다 — 시험 A 출력의 `pybamm path` 줄이 두 경로를 보인다.
- 운영 환경 · 작업 트리 · 등록부 · 산출물에 쓰지 않았다. 시험 B 코드 사본 = `git archive 3c30f570f` 의 `degradation-degeneracy/` (RUN_SCOPE 가 87차 판정 대상 `b8d4b6933` 과 같다 — 두 커밋 사이 RUN_SCOPE `git diff` 0).
- 설치하지 않았다 (pip 0). 실행 시간: 시험 B 한 번 ≈10 s.

### 설치본 ↔ 사본의 `averages.py` 차이 (`diff` 출력 원문)

```
21,22c21,22
<         if isinstance(node, pybamm.Variable | pybamm.SpatialVariable) and any(
<             domain_matches(dom) for dom in node.domain
---
>         if not node.children and any(
>             domain_matches(dom) for doms in node._domains.values() for dom in doms
68,69c68,70
<         * ``Multiplication`` / ``Division`` split when at least one operand is
<           constant under this average.
---
>         * ``Multiplication`` splits when at least one operand is constant under
>           this average.
>         * ``Division`` splits only when the denominator is constant.
79c80,83
<             if cls.symbol_is_constant(left) or cls.symbol_is_constant(right):
---
>             if cls.symbol_is_constant(right) or (
>                 isinstance(symbol, pybamm.Multiplication)
>                 and cls.symbol_is_constant(left)
>             ):
```

## 시험 A — 부반응 없는 DFN · 구배 음극 (브리핑의 '작은 검증')

Chen2020 · 1 h 방전 · 부반응 서브모델 0. 구배 = 음극 활물질 분율 0.675 → 0.825 (x 평균 0.75 = 원값) · 다공도 = 1 − 그 값. 대조 = 같은 조건의 균일 음극. 참값: `LLI [%]` = 0 · 총 리튬 표류 = 0 · PyBaMM 음극 리튬 = 손 적분.

### `graded_lli.py` (실행한 그대로)

```python
"""PyBaMM #5813 확인 — 부반응 없는 DFN 에서 활물질 분율이 x 로 변할 때 `LLI [%]` 와 총 입자 리튬.

브리핑(2026-10-02) 의 '작은 검증' 제안: 부반응을 끈 같은 구배 전극에서 수정 전후 총 리튬 보존과 LLI≈0.
수정 전 = 설치본 26.8.0.0 · 수정 후 = 그 사본에 #5813 (bd572504) averages.py 고침을 덧댄 것 (PYTHONPATH).
쓰는 것은 stdout 과 argv[1] 의 JSON 하나뿐.

검사 셋:
  (1) PyBaMM `LLI [%]` (부반응 0 이므로 참값 0)
  (2) PyBaMM `Total lithium [mol]` 의 시작 ↔ 끝 표류
  (3) PyBaMM `Total lithium in negative electrode [mol]` ↔ 손 적분 Σ ε_s(x_i) · c̄_s(x_i) · Δx_i · A (같은 해 · 같은 격자)
"""
import json
import sys

import numpy as np
import pybamm

L_N = 85.2e-6  # Chen2020 negative electrode thickness [m]


def eps_s_graded(x, *_yz):  # PyBaMM 은 전극 공간 함수를 (x, y, z) 로 부른다
    return 0.75 + 0.15 * (x / L_N - 0.5)  # 0.675 → 0.825 (x 평균 0.75 = Chen2020 원값)


def run(graded: bool):
    model = pybamm.lithium_ion.DFN()
    param = pybamm.ParameterValues("Chen2020")
    if graded:
        param.update({
            "Negative electrode active material volume fraction": eps_s_graded,
            "Negative electrode porosity": lambda x, *_yz: 1.0 - eps_s_graded(x),  # 부피 분율 합 1 유지
        })
    sim = pybamm.Simulation(model, parameter_values=param)
    sol = sim.solve([0, 3600])
    area = param["Electrode width [m]"] * param["Electrode height [m]"]

    lli = np.asarray(sol["LLI [%]"].entries)
    tot = np.asarray(sol["Total lithium [mol]"].entries)
    tot_n = np.asarray(sol["Total lithium in negative electrode [mol]"].entries)
    cbar = np.asarray(sol["R-averaged negative particle concentration [mol.m-3]"].entries)  # (n_x, n_t)
    x_n = np.asarray(sol["x_n [m]"].entries)[:, 0]
    dx = np.diff(np.asarray(sim.mesh["negative electrode"].edges))
    eps = eps_s_graded(x_n) if graded else np.full_like(x_n, 0.75)
    hand = (eps[:, None] * cbar * dx[:, None]).sum(axis=0) * area
    rel = (tot_n - hand) / hand
    return {
        "graded": graded,
        "pybamm": pybamm.__version__,
        "pybamm_path": pybamm.__file__,
        "n_t": int(len(sol.t)),
        "LLI_end_pct": float(lli[-1]),
        "LLI_maxabs_pct": float(np.max(np.abs(lli))),
        "total_li_drift_rel": float((tot[-1] - tot[0]) / tot[0]),
        "neg_li_pybamm_vs_hand_rel_start": float(rel[0]),
        "neg_li_pybamm_vs_hand_rel_maxabs": float(np.max(np.abs(rel))),
        "dx_sum_m": float(dx.sum()),
    }


def main(path):
    out = [run(False), run(True)]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    for r in out:
        print(json.dumps({k: v for k, v in r.items() if k != "pybamm_path"}, ensure_ascii=False))
    print("pybamm path:", out[0]["pybamm_path"])


if __name__ == "__main__":
    main(sys.argv[1])
```

### 출력 원문 — 수정 전 (`python3 graded_lli.py graded_unpatched.json`)

```
{"graded": false, "pybamm": "26.8.0.0", "n_t": 170, "LLI_end_pct": 8.810729923425242e-13, "LLI_maxabs_pct": 9.379164112033322e-13, "total_li_drift_rel": -8.441773919150525e-15, "neg_li_pybamm_vs_hand_rel_start": 2.832251866191152e-16, "neg_li_pybamm_vs_hand_rel_maxabs": 1.5629800888410663e-15, "dx_sum_m": 8.52e-05}
{"graded": true, "pybamm": "26.8.0.0", "n_t": 155, "LLI_end_pct": -0.00822347342521823, "LLI_maxabs_pct": 0.27346537810899463, "total_li_drift_rel": 8.070911624045874e-05, "neg_li_pybamm_vs_hand_rel_start": 1.4161259330955758e-16, "neg_li_pybamm_vs_hand_rel_maxabs": 0.009221989892433138, "dx_sum_m": 8.52e-05}
pybamm path: /usr/local/lib/python3.11/dist-packages/pybamm/__init__.py
```

### 출력 원문 — 수정 후 (`PYTHONPATH=…/pr5813/site python3 graded_lli.py graded_patched.json`)

```
{"graded": false, "pybamm": "26.8.0.0", "n_t": 170, "LLI_end_pct": 8.810729923425242e-13, "LLI_maxabs_pct": 9.379164112033322e-13, "total_li_drift_rel": -8.441773919150525e-15, "neg_li_pybamm_vs_hand_rel_start": 2.832251866191152e-16, "neg_li_pybamm_vs_hand_rel_maxabs": 1.5629800888410663e-15, "dx_sum_m": 8.52e-05}
{"graded": true, "pybamm": "26.8.0.0", "n_t": 155, "LLI_end_pct": 9.094947017729282e-13, "LLI_maxabs_pct": 9.094947017729282e-13, "total_li_drift_rel": -8.633632417313038e-15, "neg_li_pybamm_vs_hand_rel_start": -1.4161259330955758e-16, "neg_li_pybamm_vs_hand_rel_maxabs": 1.5710188150413967e-15, "dx_sum_m": 8.52e-05}
pybamm path: /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/a45978e3-3a6e-5e3d-af55-7c9b61e0d809/scratchpad/pr5813/site/pybamm/__init__.py
```

## 시험 B — 우리 합성 truth 두 조건 (2026-10-01 과 같은 드라이버)

드라이버 `cmp_pybamm.py` 와 비교 스크립트 `compare.py` 는 `raw/repositories/2026-10-01-pybamm-26.8-vs-26.9-synthetic-truth.md` 에 실린 두 블록과 **바이트 동일** (sha256 앞 16자 `b3904928181464e2` · `7ddbbe1703879cae`) — 다시 싣지 않는다. 조건 둘: (lli 0 · lam_pe 0 · lam_ne 0) · (lli 0.10 · lam_pe 0.13 · lam_ne 0.13), 둘 다 `de`. 실행: 코드 사본의 `degradation-degeneracy/` 에서 수정 전 `PYTHONPATH=. python3 cmp_pybamm.py out_268.json` · 수정 후 `PYTHONPATH=…/pr5813/site:. python3 cmp_pybamm.py out_269.json` (`compare.py` 가 읽는 파일 이름을 그대로 쓰려고 `out_269` — 내용은 26.8 + #5813 이다).

### 비교 출력 원문 — 수정 전 ↔ 수정 후 (`python3 compare.py …/pr5813`)

```
versions 26.8.0.0 ↔ 26.8.0.0
discharged_state identical: True

[lli=0.0 lam_pe=0.0 lam_ne=0.0] errors: None / None · solver {'requested': {'type': 'idaklu', 'fallback': 'casadi', 'rtol': 1e-06, 'atol': 1e-06, 'casadi_mode': 'safe'}, 'effective_class': 'IDAKLUSolver', 'pybamm': '26.8.0.0', 'pybammsolvers': '0.9.1', 'casadi': '3.7.2'} / {'requested': {'type': 'idaklu', 'fallback': 'casadi', 'rtol': 1e-06, 'atol': 1e-06, 'casadi_mode': 'safe'}, 'effective_class': 'IDAKLUSolver', 'pybamm': '26.8.0.0', 'pybammsolvers': '0.9.1', 'casadi': '3.7.2'}
  q_mah: 5621.0728471098655 vs 5621.0728471098655  Δ=0.000e+00 mAh (0.00e+00 %)
  x_norm: max|Δ|=0.000e+00 at idx 0/300 (x_norm=0.000) · median|Δ|=0.000e+00 · identical=True
  v_full: max|Δ|=2.713e-08 at idx 299/300 (x_norm=1.000) · median|Δ|=1.791e-10 · identical=False
  v_pe: max|Δ|=2.713e-08 at idx 299/300 (x_norm=1.000) · median|Δ|=1.791e-10 · identical=False
  v_ne: max|Δ|=0.000e+00 at idx 0/300 (x_norm=0.000) · median|Δ|=0.000e+00 · identical=True

[lli=0.1 lam_pe=0.13 lam_ne=0.13] errors: None / None · solver {'requested': {'type': 'idaklu', 'fallback': 'casadi', 'rtol': 1e-06, 'atol': 1e-06, 'casadi_mode': 'safe'}, 'effective_class': 'IDAKLUSolver', 'pybamm': '26.8.0.0', 'pybammsolvers': '0.9.1', 'casadi': '3.7.2'} / {'requested': {'type': 'idaklu', 'fallback': 'casadi', 'rtol': 1e-06, 'atol': 1e-06, 'casadi_mode': 'safe'}, 'effective_class': 'IDAKLUSolver', 'pybamm': '26.8.0.0', 'pybammsolvers': '0.9.1', 'casadi': '3.7.2'}
  q_mah: 4973.114263289146 vs 4973.114263289146  Δ=0.000e+00 mAh (0.00e+00 %)
  x_norm: max|Δ|=0.000e+00 at idx 0/300 (x_norm=0.000) · median|Δ|=0.000e+00 · identical=True
  v_full: max|Δ|=4.908e-08 at idx 299/300 (x_norm=1.000) · median|Δ|=8.518e-11 · identical=False
  v_pe: max|Δ|=4.908e-08 at idx 299/300 (x_norm=1.000) · median|Δ|=8.518e-11 · identical=False
  v_ne: max|Δ|=0.000e+00 at idx 0/300 (x_norm=0.000) · median|Δ|=0.000e+00 · identical=True
```

### 결정성 대조 — 수정 전 ↔ 수정 전 다시 실행 (`compare.py …/pr5813/rerun` · 같은 줄만 grep)

```
versions 26.8.0.0 ↔ 26.8.0.0
  q_mah: 5621.0728471098655 vs 5621.0728471098655  Δ=0.000e+00 mAh (0.00e+00 %)
  v_full: max|Δ|=0.000e+00 at idx 0/300 (x_norm=0.000) · median|Δ|=0.000e+00 · identical=True
  v_pe: max|Δ|=0.000e+00 at idx 0/300 (x_norm=0.000) · median|Δ|=0.000e+00 · identical=True
  q_mah: 4973.114263289146 vs 4973.114263289146  Δ=0.000e+00 mAh (0.00e+00 %)
  v_full: max|Δ|=0.000e+00 at idx 0/300 (x_norm=0.000) · median|Δ|=0.000e+00 · identical=True
  v_pe: max|Δ|=0.000e+00 at idx 0/300 (x_norm=0.000) · median|Δ|=0.000e+00 · identical=True
```

(해석은 raw 가 아니라 위키 페이지 `entities/pybamm.md` 에 둔다.)
