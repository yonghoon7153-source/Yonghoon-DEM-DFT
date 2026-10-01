---
source_url: https://github.com/ImperialCollegeLondon/PyProBE
ingested: 2026-10-01
sha256: 239064bd184961dcec7f05f02043870dfaed60adaa28b23ea6385244fba52986
---

수집 목적: 경쟁 도구 · 판정 대상 (일일 브리핑 ② 축) — 2026-10-01 첫 PyProBE 실측이 **용량을 참값으로 준** 조건이었으므로, 용량 정보를 뺀 **형상만** 조건에서 답이 어떻게 되는가를 잰다 (`np-lip-ocv-reparametrization` 2 자유도 정리의 직접 검증). 사용자 승인 2026-10-01 ("1번 3번 진행하자").

# PyProBE 2.6.0 — 용량 열을 바꿔 가며 같은 곡선을 피팅 (2026-10-01 실측)

## 조건 · 격리

- 첫 실측 (`2026-10-01-pyprobe-dma-on-synthetic-truth.md`) 과 **같은 곡선 · 같은 OCP 표 · 같은 피팅** (기본 시작점 `[0.9, 0.1, 0.1, 0.9]` · 전 범위 · OCV target · `minimize`). 바꾼 것은 `Capacity [Ah]` 열 하나다:
  - `truth` — 각 조건의 참값 용량 `q_mah` (첫 실측과 같음 · 대조군)
  - `pristine` — 모든 조건에 pristine 용량 5621.07 mAh (= "용량이 줄었는지 모른다", SOH 정보 제거)
  - `unit` — 모든 조건에 1 Ah (= 순수 형상)
- PyProBE 는 `Cell Capacity = ptp(Capacity)/ptp(SOC)` 로 쓰므로 `pristine` 과 `unit` 은 **비율이 같아 결과가 같아야** 한다 (실측도 같았다 — 아래).
- 조건 추가: LLI 0.20 단독 · LAM_NE 0.20 단독 (noise 0 · grid_curves_v4 에 있음).
- 버리는 venv (PyProBE 2.6.0 재설치) · 운영 환경 · 저장소 · 등록부 불변 (parquet 읽기만) · 전체 12 s.

## 결과 (shape_only_run.txt 원문)

```
START 2026-10-01T02:01:19Z
[truth   ] LLI_only_0.10          truth LLI=0.100 LAM_pe=0.000 LAM_ne=0.000 SOH=0.8769 | fit LLI=+0.1011 LAM_pe=+0.0032 LAM_ne=-0.0183 SOH=0.8769 rmse=12.7mV
[truth   ] LAMNE_only_0.10        truth LLI=0.000 LAM_pe=0.000 LAM_ne=0.100 SOH=0.9236 | fit LLI=+0.0045 LAM_pe=+0.0067 LAM_ne=+0.1016 SOH=0.9236 rmse=11.1mV
[truth   ] mixed_0.10_0.10_0.10   truth LLI=0.100 LAM_pe=0.100 LAM_ne=0.100 SOH=0.8991 | fit LLI=+0.1008 LAM_pe=+0.1014 LAM_ne=+0.0955 SOH=0.8991 rmse=10.7mV
[truth   ] LAMPE_only_max         truth LLI=0.000 LAM_pe=0.060 LAM_ne=0.000 SOH=1.0093 | fit LLI=-0.0055 LAM_pe=+0.0440 LAM_ne=-0.0006 SOH=1.0093 rmse=8.6mV
[truth   ] LLI_0.20               truth LLI=0.200 LAM_pe=0.000 LAM_ne=0.000 SOH=0.7377 | fit LLI=+0.2063 LAM_pe=+0.0068 LAM_ne=-0.0718 SOH=0.7377 rmse=15.1mV
[truth   ] LAMNE_0.20             truth LLI=0.000 LAM_pe=0.000 LAM_ne=0.200 SOH=0.8336 | fit LLI=+0.0094 LAM_pe=+0.0093 LAM_ne=+0.1859 SOH=0.8336 rmse=11.9mV
rc=0
[pristine] LLI_only_0.10          truth LLI=0.100 LAM_pe=0.000 LAM_ne=0.000 SOH=0.8769 | fit LLI=-0.0251 LAM_pe=-0.1367 LAM_ne=-0.1612 SOH=1.0000 rmse=12.7mV
[pristine] LAMNE_only_0.10        truth LLI=0.000 LAM_pe=0.000 LAM_ne=0.100 SOH=0.9236 | fit LLI=-0.0779 LAM_pe=-0.0755 LAM_ne=+0.0273 SOH=1.0000 rmse=11.1mV
[pristine] mixed_0.10_0.10_0.10   truth LLI=0.100 LAM_pe=0.100 LAM_ne=0.100 SOH=0.8991 | fit LLI=-0.0001 LAM_pe=+0.0006 LAM_ne=-0.0059 SOH=1.0000 rmse=10.7mV
[pristine] LAMPE_only_max         truth LLI=0.000 LAM_pe=0.060 LAM_ne=0.000 SOH=1.0093 | fit LLI=+0.0037 LAM_pe=+0.0528 LAM_ne=+0.0086 SOH=1.0000 rmse=8.6mV
[pristine] LLI_0.20               truth LLI=0.200 LAM_pe=0.000 LAM_ne=0.000 SOH=0.7377 | fit LLI=-0.0759 LAM_pe=-0.3463 LAM_ne=-0.4528 SOH=1.0000 rmse=15.1mV
[pristine] LAMNE_0.20             truth LLI=0.000 LAM_pe=0.000 LAM_ne=0.200 SOH=0.8336 | fit LLI=-0.1884 LAM_pe=-0.1885 LAM_ne=+0.0234 SOH=1.0000 rmse=11.9mV
rc=0
[unit    ] LLI_only_0.10          truth LLI=0.100 LAM_pe=0.000 LAM_ne=0.000 SOH=0.8769 | fit LLI=-0.0251 LAM_pe=-0.1367 LAM_ne=-0.1612 SOH=1.0000 rmse=12.7mV
[unit    ] LAMNE_only_0.10        truth LLI=0.000 LAM_pe=0.000 LAM_ne=0.100 SOH=0.9236 | fit LLI=-0.0779 LAM_pe=-0.0755 LAM_ne=+0.0273 SOH=1.0000 rmse=11.1mV
[unit    ] mixed_0.10_0.10_0.10   truth LLI=0.100 LAM_pe=0.100 LAM_ne=0.100 SOH=0.8991 | fit LLI=-0.0001 LAM_pe=+0.0006 LAM_ne=-0.0059 SOH=1.0000 rmse=10.7mV
[unit    ] LAMPE_only_max         truth LLI=0.000 LAM_pe=0.060 LAM_ne=0.000 SOH=1.0093 | fit LLI=+0.0037 LAM_pe=+0.0528 LAM_ne=+0.0086 SOH=1.0000 rmse=8.6mV
[unit    ] LLI_0.20               truth LLI=0.200 LAM_pe=0.000 LAM_ne=0.000 SOH=0.7377 | fit LLI=-0.0759 LAM_pe=-0.3463 LAM_ne=-0.4528 SOH=1.0000 rmse=15.1mV
[unit    ] LAMNE_0.20             truth LLI=0.000 LAM_pe=0.000 LAM_ne=0.200 SOH=0.8336 | fit LLI=-0.1884 LAM_pe=-0.1885 LAM_ne=+0.0234 SOH=1.0000 rmse=11.9mV
rc=0
END 2026-10-01T02:01:31Z
```

RMSE 가 세 모드에서 같다 = **적합된 화학량론 창 4 개는 용량 열과 무관하게 같다** (형상이 창을 정한다). 용량은 창을 전극 용량 · Li 재고로 환산할 때만 들어간다.

## 손계산 대조 (해석의 재료 — 정본은 위키 페이지)

용량을 모르면 (SOH 를 1 로 두면) PyProBE 의 각 모드는 `1 − (1 − mode_true) / SOH_true` 가 되어야 한다 (전극 용량 = 셀 용량 / 창 폭 · Li 재고도 셀 용량에 비례).

| 조건 | SOH_true | 기대 LLI | 실측 | 기대 LAM_pe | 실측 | 기대 LAM_ne | 실측 |
|---|---:|---:|---:|---:|---:|---:|---:|
| LLI 0.10 | 0.8769 | −0.0264 | −0.0251 | −0.1404 | −0.1367 | −0.1404 | −0.1612 |
| LAM_NE 0.10 | 0.9236 | −0.0827 | −0.0779 | −0.0827 | −0.0755 | +0.0256 | +0.0273 |
| 혼합 0.1/0.1/0.1 | 0.8991 | −0.0010 | −0.0001 | −0.0010 | +0.0006 | −0.0010 | −0.0059 |
| LLI 0.20 | 0.7377 | −0.0845 | −0.0759 | −0.3556 | −0.3463 | −0.3556 | −0.4528 |
| LAM_NE 0.20 | 0.8336 | −0.1996 | −0.1884 | −0.1996 | −0.1885 | +0.0403 | +0.0234 |

실측 − 기대 의 잔차는 `truth` 모드에서의 적합 오차 (LAM_ne 쪽이 크다 — NE 충전 끝 창 −0.085 의 체계 오차) 와 같은 크기다.

## 스크립트 (첫 실측 스크립트에 더한 함수 — 실행한 그대로 · 나머지는 `2026-10-01-pyprobe-dma-on-synthetic-truth.md` 와 동일)

```python
def main_shape_only():
    """CAP_MODE = truth | pristine | unit — 용량 열에 무엇을 주는가. 형상 (SOC-정규화 OCV) 은 셋 모두 같다."""
    import os
    mode = os.environ.get("CAP_MODE", "truth")
    t0 = time.time()
    cols = ["cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah", "x_norm", "v_pe", "v_ne", "v_full", "v_full_noisy"]
    df = pd.read_parquet(PARQ, columns=cols)
    conds = df.drop_duplicates("cond_id")[["cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah"]]
    z = conds[conds.noise == 0]
    def pick(lli, pe, ne):
        r = z[(z.lli == lli) & (z.lam_pe == pe) & (z.lam_ne == ne)]
        return None if r.empty else r.iloc[0]
    pe_only = z[(z.lli == 0) & (z.lam_ne == 0) & (z.lam_pe > 0)].sort_values("lam_pe")
    cases = {"pristine": pick(0, 0, 0), "LLI_only_0.10": pick(0.10, 0, 0), "LAMNE_only_0.10": pick(0, 0, 0.10),
             "mixed_0.10_0.10_0.10": pick(0.10, 0.10, 0.10), "LAMPE_only_max": pe_only.iloc[-1],
             "LLI_0.20": pick(0.20, 0, 0), "LAMNE_0.20": pick(0, 0, 0.20)}
    cases = {k: v for k, v in cases.items() if v is not None}
    def curve(cid):
        r = df[df.cond_id == cid].sort_values("x_norm")
        soc = 1.0 - r.x_norm.to_numpy(); return soc[::-1], r.v_full.to_numpy()[::-1], float(r.q_mah.iloc[0])
    xn, v, q0 = curve(cases["pristine"].cond_id)
    qcap = lambda q: {"truth": q, "pristine": q0, "unit": 1000.0}[mode]
    lim0, d0, rmse0 = fit(make_result(xn, v, qcap(q0)))
    out = {"pyprobe": pyprobe.__version__, "cap_mode": mode, "cases": {}}
    for name, c in cases.items():
        if name == "pristine": continue
        xn, v, q = curve(c.cond_id)
        lim, d, rmse = fit(make_result(xn, v, qcap(q)))
        out["cases"][name] = {"truth": {"LLI": float(c.lli), "LAM_pe": float(c.lam_pe), "LAM_ne": float(c.lam_ne), "SOH": q / q0},
                              "dma": dma_of(lim0, lim), "limits": d, "rmse_V": rmse}
    out["wall_s"] = time.time() - t0
    (OUT / f"shape_only_{mode}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    for name, r in out["cases"].items():
        t, m = r["truth"], r["dma"]
        print(f"[{mode:8s}] {name:22s} truth LLI={t['LLI']:.3f} LAM_pe={t['LAM_pe']:.3f} LAM_ne={t['LAM_ne']:.3f} SOH={t['SOH']:.4f} | fit LLI={m['LLI']:+.4f} LAM_pe={m['LAM_pe']:+.4f} LAM_ne={m['LAM_ne']:+.4f} SOH={m['SOH']:.4f} rmse={r['rmse_V']*1e3:.1f}mV")
```

(해석은 raw 가 아니라 위키 페이지 `entities/pyprobe.md` · `concepts/np-lip-ocv-reparametrization.md` · 질문 카드 `22p-physics-or-degeneracy` 에 둔다.)
