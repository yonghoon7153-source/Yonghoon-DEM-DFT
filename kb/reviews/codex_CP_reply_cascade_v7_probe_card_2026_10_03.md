---
title: "회신 CP — cascade D_rel v7 탐침 카드: 초안 그대로 실행 NO-GO · 온도 탐침 방향은 조건부 GO · P0 3 (온도 메타 결속 · 10 % 자격 기준의 통계적 역할 · H0 통과 → 40 런 자동 착수 끊기) · P1 (framework_alarm 은 보조 지표 · Q-CP-1 · Q-CP-4)"
date: 2026-10-03
updated: 2026-10-03
tags: [review, codex, cascade, d_rel, eprime, v7, probe, gate, msd, reply, no-go]
letter: CP
track: cascade
kind: review-reply
status: 수령 (2026-10-03 · 사용자 붙여넣기) — 회신 원문 · 고치지 않는다 · 이행은 별도 파일·커밋 · 트랙 cascade = 사용자 1저자
confidence: high
verificationStatus: verified
verifiedAt: 2026-10-03
verifiedBy: self
explored: false
authoredBy: external
effort: high
claimType: mixed
evidenceScope: single-source
prompt: kb/reviews/codex_CP_prompt_cascade_v7_probe_card_2026_10_01.md
verdict: NO-GO (초안 그대로 실행) · 방향 조건부 GO
---

# 회신 CP — 원문

> ⛔ **이 아래는 Codex 회신 원문이다. 고치지 않는다.** 정정·해석·이행은 별도 파일·커밋으로 남긴다.
> 붙여넣기 끝의 검증 자료 3 개(JSON 2 · 파이썬 스크립트 1)는 **내용을 한 글자도 바꾸지 않고** 코드 울타리(```) 안에만 넣었다 —
> 울타리가 없으면 마크다운이 스크립트의 `#` 주석을 제목으로 읽는다. 회신이 가리키는 `C:/Users/Administrator/Documents/Codex/…` 경로는
> 사용자 Windows 쪽 Codex 작업 폴더이고 레포에는 없다 (같은 내용이 아래 세 블록이다).
> 기준 커밋: 회신이 확인한 원격 `721f9538` = 대피 브랜치의 시작점 (friendly 끝).

---

현재 초안 그대로 실행은 NO-GO예요. 온도 탐침이라는 방향은 조건부 GO지만, 판독기 수정과 탐침의 역할 정리가 먼저예요. H0 통과만으로 40런을 여는 것은 승인하지 않겠습니다.
원격 `721f9538`의 카드·판독기를 확인했고, `judge_eprime.py --selftest` 59건 PASS를 재현했어요. 추가 시험은 합성 궤적만 사용했으며, 실제 MD·UMA·DFT는 실행하지 않았어요. v6의 봉인된 P1/P2 비교값도 열지 않았습니다.
Q-CP-2 — 10% 문턱에 원리적으로 닿는가: P0, 수정 필요
닿기는 해요. 하지만 정상 확산도 표집 잡음 때문에 상당수 탈락해요.
먼저 실제 구현은 다음이에요.

* D_inc: 구간 전체 회귀가 아니라 끝점 두 개의 MSD 차분 / 시간 차 / 6
* 상대산포: 네 D_inc의 (최댓값−최솟값)/|중앙값|
* 겹치는 시간원점은 사용하지만, 서로 독립인 표본은 아니에요.

실제 lag 목록과 판정 함수를 사용해, 독립 브라운 입자 90개 · 200 ps · 저장 간격 100 fs인 합성 궤적 512개를 검사했어요. 사건 수 조건은 충족시켜서 곡선 판정만 분리했어요.

* 처음부터 정상 확산인데 113/512, 22.1%가 탈락
* 상대산포 중앙값 5.33%, 95백분위 15.03%
* 부창 기울기비는 512개 모두 통과 — 탈락은 10% plateau 조건에서 발생
* 동일 궤적의 MSD 크기를 100배 해도 상대산포는 그대로

따라서 온도가 올라 D만 커진다면 이 잡음 문제는 사라지지 않아요. 온도 상승이 갇힘·상관·활성 이온 수까지 바꾸면 개선될 수 있지만, 그건 따로 확인해야 하는 효과예요. MSD의 시간적 상관과 추정법이 불확실성을 좌우한다는 점은 [McCluskey 등의 연구](https://doi.org/10.1021/acs.jctc.4c01249)와도 맞아요.
더 중요한 것은 부모별 네 런을 모두 요구한다는 점이에요. 위 합성 통과율을 네 독립 런에 적용하면 부모 생존율은 약 36.9%, 부모 10개 중 기대 생존 수는 3.7개예요. 실제 캠페인의 예측값은 아니지만, 부모 10개를 돌린다고 판정의 n이 10에 가까워지는 것은 아니라는 경고예요.
제안은 다음과 같아요.

1. 10%를 물리적 확산의 필요조건으로 설명하지 마세요. 유한 표본에 적용한 보수적인 운영 기준이에요.
2. 지금 임의로 20% 등으로 올리지 마세요. 허용할 정상 확산 탈락률과 비선형 곡선 검출력을 먼저 정하고, 그 목적에 맞춰 기준을 검증해야 해요.
3. 유지한다면 예상 탈락과 유효 부모 감소를 받아들인다는 결정을 카드에 적으세요. 실패는 우선 **“이 자료로 확산 영역을 확인하지 못함”**이지, 실제 확산계수가 존재하지 않는다는 뜻이 아니에요.

탐침 전 수정은 가능해요. 아직 초안이므로 v7 개정본으로 이력을 남기고 비준하면 됩니다. 다만 기준까지 바꾸면 “온도만 바꾼다”는 설명도 고쳐야 해요. v6의 마감과 기존 판정은 그대로 보존하세요.
Q-CP-1 — 온도라는 손잡이: P1, 조건부 찬성
“고온 조건부 수송 차이도 연구할 가치가 있다”면 온도를 먼저 시험하는 선택은 합리적이에요. 다만 600 K 질문을 가장 잘 해결하는 선택이라고 할 수는 없어요.

* 온도 상승: 짧은 시간 안에 다른 동역학 영역에 도달할 가능성이 있지만, 답하는 온도가 달라져요.
* 600 K의 긴 궤적·늦은 창: 원래 온도의 질문을 유지하지만, 비용이 늘고 늦은 창에서도 정상 확산이 보장되지는 않아요.
* 음이온 무질서: 확산 경로 자체를 바꿀 수 있어 이번 카드 밖에 두는 것이 맞아요. 실제 아지로다이트 연구에서도 음이온 질서에 따라 국소 이동과 장거리 확산망이 달라져요. [Morgan, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8029578/)

“같은 창이면 런을 늘려도 그대로”는 두 부분으로 나눠야 해요.

* 실제 평균 MSD의 휨: 궤적을 길게 모은다고 없어지지는 않아요.
* 추정된 MSD의 표집 잡음: 같은 lag 창에서도 긴 궤적으로 줄일 수 있어요.

추가 합성 시험에서는 800 ps 궤적에 기존 2–100 ps lag를 그대로 적용했을 때 128개 모두 통과했어요. 이것은 실제 600 K가 구제된다는 뜻이 아니라, 총길이가 잡음에 영향을 준다는 반례예요. 반대로 800 ps에서 lag도 100–400 ps로 옮기면 이 개선을 그대로 기대할 수는 없어요.
v6의 일관된 큰 휨을 단순 잡음으로 돌리지는 않겠습니다. 다만 원인을 “케이지 간 확산으로 넘어가는 중”으로 확정할 근거도 아직 없어요.
Q-CP-3 — H0 두 시드의 대표성: P0, 40런 착수 근거로는 부족
H0는 실행·분석 경로와 무도핑 호스트의 가능성을 보는 대조 계산이지, Al/O 처방 셀의 충분조건이 아니에요.
제안한 대표 부모 한 쌍을 넣되 D를 봉인하는 방식에 찬성해요. 최소한 다음 순서를 권해요.

1. H0 사다리로 후보 온도를 정해요.
2. 결과를 보지 않고 지정한 부모 하나에서 P1/P2 각각 두 속도 시드, 네 런의 자격을 확인해요.
3. 하나라도 실패하면 나머지 본 런은 열지 않아요. 다른 부모로 바꿔 재도전하지 않아요.

온도를 올려 재시험할지, 실패로 닫을지도 첫 탐침 전에 정해야 해요. 이 처방 탐침은 기존 최대 4런·30 GPU-h 밖이므로 예산도 별도로 적어야 합니다.
또한 그 네 런을 최종 40런에 포함할지 미리 결정하세요. 성공한 탐침을 포함하면 착수 조건에 의해 선택된 자료가 됩니다. 단순하게 가려면 탐침용 속도 시드를 따로 두고 최종 집계에서는 제외하는 편이 명확해요.
D를 가리는 것은 도움이 되지만, 자격도 같은 궤적에서 나오므로 선택 효과 자체가 없어지지는 않아요.
Q-CP-4 — 1000 K 보고량의 의미: P1, 조건부 찬성
`D_rel(T*)`는 해석 가능한 진단이에요. 다만 T*는 “확산이 시작되는 최저 온도”가 아니라, 지정 사다리와 시드에서 운영 기준을 통과한 온도예요.
고온의 ‘동등’은 특히 좁게 써야 해요. 단순 예시로 전지수 인자가 같고 장벽 차이가 30 meV라면 확산 비는:

* 1000 K에서 약 1.42
* 600 K에서 약 1.79

같은 두 계가 1000 K에서는 1.5배 영역 안에, 600 K에서는 밖에 놓일 수 있어요. 실제 캠페인의 장벽을 추정한 것은 아니고, 고온 동등성을 다른 온도로 옮길 수 없다는 예시입니다.
권장 문구는 다음과 같아요.
사전 지정된 탐침 규칙으로 선택한 T* K에서, UMA·공통 고정셀·준비 및 자격 조건 아래의 P1/P2 확산 비를 평가했다. 등가영역 내 판정은 이 조건에 한정하며, 600 K·작동 온도·실제 재료의 동등성을 뜻하지 않는다.
준비 구조는 초기 좌표로 재사용 가능해요. 하지만 그 구조가 온도와 무관하게 평형이라는 뜻은 아니며, 5 ps 평형화의 충분성까지 자동 승계되지는 않아요.
Q-CP-5 — 실행 전 결함과 최소 조건
P0-1. 온도를 고르는 판독기가 온도 기록의 불일치를 잡지 않아요
[judge_eprime.py (line 274)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_CP_20261003/snapshot/tools/doping/judge_eprime.py:274)
`aimd_results.json`에서는 저장 간격과 프레임 수만 읽고, `T_K`를 비교하지 않아요.
재현: 정상 자격의 합성 궤적에서 `msd.json`은 800 K, `aimd_results.json`은 600 K로 만들었는데 `probe_run()`이 **`eligible=True`**를 반환했어요. 두 온도를 일치시켜도 결과는 같았어요.
실행 전: 요청 온도·경로·두 메타데이터의 온도를 결속하고, 생산길이·시간간격도 카드 값과 대조하세요. 불일치를 실제로 차단하는 음성시험이 필요해요.
P0-2. 자격 기준의 통계적 역할을 비준해야 해요
위 Q2처럼 정상 확산의 상당한 탈락을 허용하는 운영 기준을 유지할지, 검증된 새 기준을 쓸지 탐침 전에 정해야 해요. “고온이면 통과하겠지”만으로 넘어갈 부분은 아니에요.
P0-3. H0 통과 → 40런 자동 착수를 끊어야 해요
대표 처방 쌍의 착수 검사와 실패 처리, 추가 예산을 먼저 선언하세요. 통과한 부모만 남았을 때의 결론도 전체 배열이 아니라 자격 통과 집합에 조건부라는 한계를 적어야 해요.
P1. `framework_alarm` 통과를 골격 보존 인증으로 쓰면 안 돼요
[msd_diffusive_check.py (line 858)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_CP_20261003/snapshot/tools/ionic/msd_diffusive_check.py:858)
실제 함수에 합성 궤적을 넣어 두 사각을 확인했어요.

* 골격이 중간에 4 Å 움직였다 돌아와도 `framework_static`
* Al/O가 서로 반대 방향으로 4 Å 이동해도, 소수 종 제외 때문에 `framework_static`

따라서 현재 경보는 보조 지표로 한정하세요. 동일한 고체 골격·기전을 유지했다는 주장에는 부족해요. 또 [본 런 자격 경로 (line 303)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_CP_20261003/snapshot/tools/doping/judge_eprime.py:303)는 이 경보를 호출하지 않으므로, v7 본 런에도 요구할 조건이라면 실제로 연결해야 해요.
정리하면, 온도 탐침을 포기하자는 판정은 아니에요. 온도 기록 검증을 고치고, 10% 기준의 역할과 대표 처방 쌍 검사를 사전에 확정한 뒤 제한된 탐침으로 진행하는 쪽을 권합니다. 지금 상태에서 40런을 바로 여는 것은 NO-GO예요.
검증 자료: [합성 통계 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_CP_20261003/synthetic_gate_results.json) · [판독기 반례 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_CP_20261003/probe_counterexamples.json) · [재현 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_CP_20261003/synthetic_gate_audit.py)

```json
{
  "source_commit": "721f95385cf95aba17f9b25a178dd780024fe748",
  "seed": 20261003,
  "kind": "synthetic Brownian null, not campaign data",
  "settings": {
    "N_independent_ions": 90,
    "dt_ps": 0.1,
    "frames": 2000,
    "D_A2_ps": 0.05
  },
  "note": "Event gate set satisfied to isolate curve-shape gates; no framework process. This is not a calibrated error rate for real correlated Li ions.",
  "checks": {
    "fft_vs_production_max_abs_error": 4.440892098500626e-14,
    "amplitude_x100_spread_difference": 9.71445146547012e-17,
    "exact_linear_with_intercept_pass": true,
    "bounded_OU_expectation_pass": false,
    "bounded_OU_spread": 2.3371115148700206
  },
  "brownian_200ps": {
    "n_replicates": 512,
    "plateau_pass_count": 399,
    "subwindows_pass_count": 512,
    "combined_shape_pass_count": 399,
    "combined_shape_pass_fraction": 0.779296875,
    "binomial_MC_se": 0.018328238523478046,
    "spread_quantiles_5_50_95": [
      0.00946775003144168,
      0.053251417048868294,
      0.15034550298094398
    ],
    "negative_trend_count": 261,
    "heuristic_parent_survival_if_four_independent": 0.3688176861178363
  },
  "brownian_800ps_same_lags": {
    "n_replicates": 128,
    "plateau_pass_count": 128,
    "subwindows_pass_count": 128,
    "combined_shape_pass_count": 128,
    "combined_shape_pass_fraction": 1.0,
    "binomial_MC_se": 0.0,
    "spread_quantiles_5_50_95": [
      0.003049510774584734,
      0.021281431729750964,
      0.05025894022534789
    ],
    "negative_trend_count": 60,
    "heuristic_parent_survival_if_four_independent": 1.0
  }
}
```

```json
{
  "temperature_metadata_mismatch": {
    "positive_control_attempt": 2,
    "msd_T_K": 800,
    "aimd_T_K": 600,
    "probe_result": {
      "tag": "H0_host__T800__s1",
      "run_dir": "C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_CP_20261003\\tmp4gy_ltj4\\md\\H0_host__T800__s1\\H0\\T800",
      "eligible": true,
      "aggregation_eligible": true,
      "framework_alarm": "framework_static",
      "run_verdict": "citable",
      "sub_window_ratios": [
        0.9882842334710586,
        0.9907832184461224,
        1.04350349654851
      ],
      "events": 808,
      "n_frames": 2000,
      "reasons": [
        "D_inc plateau (산포 1%) · 홉 3.4/이온"
      ]
    },
    "same_result_when_aimd_T_matches": true
  },
  "framework_endpoint_blindness": {
    "max_framework_displacement_A": 4.0,
    "result": {
      "state": "framework_static",
      "frame_total": 0.00010000000000000002,
      "frame_internal": 0.0,
      "kept_frac": 0.0,
      "li_total": 0.0,
      "li_internal": 0.00010000000000000002,
      "verdict": "framework_static",
      "excluded_species_note": "n < 8 인 종은 판정에서 빠진다 (예: Al₂·O₃)",
      "measure": "첫↔마지막 프레임 MSD (원자수 가중), 전역 COM 제거 — 시간원점 평균 아님"
    }
  },
  "minority_species_exclusion": {
    "Al_and_O_displacement_A": 4.0,
    "result": {
      "state": "framework_static",
      "frame_total": 0.00010000000000000002,
      "frame_internal": 8.091465479737989e-06,
      "kept_frac": 0.08091465479737987,
      "li_total": 0.0,
      "li_internal": 5.120046274736214e-05,
      "verdict": "framework_static",
      "excluded_species_note": "n < 8 인 종은 판정에서 빠진다 (예: Al₂·O₃)",
      "measure": "첫↔마지막 프레임 MSD (원자수 가중), 전역 COM 제거 — 시간원점 평균 아님"
    }
  }
}
```

```python
"""CP review: synthetic stochastic processes only; no MD or model inference.

Brownian null with the production lag grid and production eligibility functions.
FFT accelerates exactly the same time-origin average; checked against production.
No campaign trajectories or unblinded P1/P2 diffusivities are read.
"""
import argparse
import importlib.util
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "snapshot"
sys.path.insert(0, str(SRC / "tools/ionic"))
sys.path.insert(0, str(SRC / "tools/doping"))
import msd_diffusive_check as gate
import judge_eprime as judge


def fast_mto(x, dt):
    nt, ni, _ = x.shape
    # translation does not affect displacements; reduces subtraction roundoff
    x = x - x.mean(axis=0, keepdims=True)
    nfft = 1 << (2 * nt - 1).bit_length()
    f = np.fft.rfft(x, n=nfft, axis=0)
    ac = np.fft.irfft((f.conj() * f).sum(axis=(1, 2)), n=nfft)[:nt]
    ss = (x * x).sum(axis=(1, 2))
    cs = np.r_[0.0, np.cumsum(ss)]
    lm = max(2, nt // 2)
    lag = np.unique(np.linspace(1, lm, min(150, lm)).astype(int))
    y = (cs[nt] - cs[lag] + cs[nt-lag] - 2 * ac[lag]) / ((nt-lag) * ni)
    return (lag * dt).tolist(), y.tolist()


def summarize(rows):
    sp = np.array([r['spread'] for r in rows])
    p = np.mean([r['eligible_shape'] for r in rows])
    return {
        'n_replicates': len(rows),
        'plateau_pass_count': sum(r['plateau'] for r in rows),
        'subwindows_pass_count': sum(r['subwindows'] for r in rows),
        'combined_shape_pass_count': sum(r['eligible_shape'] for r in rows),
        'combined_shape_pass_fraction': float(p),
        'binomial_MC_se': float(np.sqrt(p*(1-p)/len(rows))),
        'spread_quantiles_5_50_95': np.quantile(sp, [.05, .5, .95]).tolist(),
        'negative_trend_count': sum(r['negative_trend'] for r in rows),
        'heuristic_parent_survival_if_four_independent': float(p**4),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=512)
    args = ap.parse_args()
    rng = np.random.default_rng(20261003)
    rows = []
    checks = {}
    # 2000 saved frames at 0.1 ps spacing, as a 200 ps production callback.
    nt, ni, dt, D = 2000, 90, .1, .05
    for i in range(args.reps):
        x = np.cumsum(rng.normal(0, np.sqrt(2*D*dt), (nt, ni, 3)), axis=0)
        t, y = fast_mto(x, dt)
        if i == 0:
            direct_t, direct_y, _ = judge._msd_multi_origin()(x, dt)
            checks['fft_vs_production_max_abs_error'] = float(np.max(np.abs(np.array(y)-direct_y)))
            assert t == direct_t and np.allclose(y, direct_y, rtol=1e-11, atol=1e-11)
            scaled = gate.dinc_plateau(t, (np.array(y)*100).tolist())
            checks['amplitude_x100_spread_difference'] = abs(scaled['spread']-gate.dinc_plateau(t,y)['spread'])
        pl = gate.dinc_plateau(t, y)
        ok, _, detail = gate.aggregation_eligible(t, y, 1000000)
        ratios = detail['sub_window_ratios']
        rows.append({'spread':pl['spread'], 'plateau':pl['status']=='plateau',
                     'subwindows':all(.8 <= v <= 1.2 for v in ratios),
                     'eligible_shape': bool(ok), 'negative_trend':pl['trend'] < 0})
        if (i+1) % 128 == 0:
            print(f'Brownian null {i+1}/{args.reps}', flush=True)
    linear = [2 + 6*D*v for v in t]
    confined = [12*(1-np.exp(-v/15)) for v in t]
    checks['exact_linear_with_intercept_pass'] = gate.aggregation_eligible(t,linear,100)[0]
    checks['bounded_OU_expectation_pass'] = gate.aggregation_eligible(t,confined,100)[0]
    checks['bounded_OU_spread'] = gate.dinc_plateau(t,confined)['spread']
    # Longer observation, same lag windows: test whether precision can improve
    # without changing the underlying Brownian physics or lag interval.
    more = []
    for i in range(128):
        x = np.cumsum(rng.normal(0,np.sqrt(2*D*dt),(8000,ni,3)),axis=0)
        # Preserve exactly the 200 ps production lag grid for comparability.
        # Reuse FFT function at full grid then interpolate is NOT equivalent:
        # directly evaluate all original lags here instead.
        xx = x-x.mean(axis=0,keepdims=True)
        nf=1 << (2*len(xx)-1).bit_length()
        f=np.fft.rfft(xx,n=nf,axis=0)
        ac=np.fft.irfft((f.conj()*f).sum(axis=(1,2)),n=nf)
        cs=np.r_[0.,np.cumsum((xx*xx).sum(axis=(1,2)))]
        lag=np.rint(np.array(t)/dt).astype(int)
        yy=((cs[len(xx)]-cs[lag]+cs[len(xx)-lag]-2*ac[lag])/((len(xx)-lag)*ni)).tolist()
        pl=gate.dinc_plateau(t,yy)
        ok,_,det=gate.aggregation_eligible(t,yy,1000000)
        more.append({'spread':pl['spread'],'plateau':pl['status']=='plateau',
                     'subwindows':all(.8 <= v <= 1.2 for v in det['sub_window_ratios']),
                     'eligible_shape':bool(ok),'negative_trend':pl['trend']<0})
    result = {'source_commit':'721f95385cf95aba17f9b25a178dd780024fe748',
              'seed':20261003,'kind':'synthetic Brownian null, not campaign data',
              'settings':{'N_independent_ions':ni,'dt_ps':dt,'frames':nt,'D_A2_ps':D},
              'note':'Event gate set satisfied to isolate curve-shape gates; no framework process. This is not a calibrated error rate for real correlated Li ions.',
              'checks':checks,'brownian_200ps':summarize(rows),'brownian_800ps_same_lags':summarize(more)}
    (ROOT/'synthetic_gate_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
```
