# A3 PTFE binder sweep — GPU result + honest reframe (2026-06-30)

Ran `scripts/a3_binder_sweep.py --arch cuda --n-grid 384` on the **real14 production
scaffold** (457 AM + 32,832 real SE, 45.6 M pts, kserver CUDA). PTFE wt% = 0…8,
champion SE (E=1.53, ν=0.49, σ_y=0.3), `--coh-ptfe 0.10 --binder-opt-wt 1.5`.

## Result
| PTFE wt% | binder_cap | coh (GPa) | porosity@target % | thickness µm | cov AM_P |
|---|---|---|---|---|---|
| 0   | 0.000 | 0.000 | **15.91** | 29.95 | 29.3% |
| 0.5 | 0.649 | 0.065 | 15.15 | 29.95 | 29.6% |
| 1   | 0.930 | 0.093 | 14.37 | 29.95 | 29.9% |
| 2   | 0.955 | 0.095 | 13.59 | 30.22 | 28.7% |
| 4   | 0.504 | 0.050 | 10.38 | 30.22 | 30.2% |
| 8   | 0.070 | 0.007 | **4.40** | 30.49 | 32.7% |

**Porosity is MONOTONE-decreasing** (15.9 → 4.4 %), NOT the ∪ the binder-cap
peak (at 1.5–2 wt%) would imply. The cohesion non-monotonicity (binder_cap
0.93→0.96→0.50→0.07) is completely masked.

## Why — and why this is CORRECT physics, not a failure
The PTFE points carry their **recipe volume** into the MPM (0.91 → 15.76 vol% of
solid across the sweep). That volume-fill lowers porosity **monotonically**, and it
dwarfs the cohesion term: at 8 wt% the binder adds ~16 vol% of solid, so porosity
craters to 4.4 % even though the binding strength has collapsed (cap 0.07).

⇒ **The ∪-in-porosity was a mis-framing.** The literature non-monotonicity (Hong
2026 optimal ~1 wt%; Cho 2024 over-binder harmful) lives in **performance** —
mechanical integrity + transport — NOT in raw porosity:
- **Raw porosity vs binder wt% is monotone-decreasing (volume-fill), and that is
  physically right** — more solid binder = less void. (Hong's 1 wt% −6.4 %p is
  reproduced direction-wise.)
- The binder's **non-monotonic harm at over-application** is:
  (i) **mechanical**: binding STRENGTH peaks then declines → captured by
      `binder_cap` cohesion (active here — the early-servo wallP rises 0.32→0.56 GPa
      as coh rises 0→0.093 over 0→1 wt%, i.e. the cohesion IS doing work), and
  (ii) **transport σ-block**: over-binder = resistive film → handled by
      `whatif_additives` (W2, PTFE σ_ion ×0.74; Bielefeld 2020).
- A porosity **rebound** would require the over-applied binder to act as a rigid
  *spacer* (propping AM/SE apart so void cannot close). **★ This is unphysical at the
  300 MPa production pressure — and the reason is quantitative, not just "no data":**
  PTFE is soft (E = 0.30 GPa, **σ_y = 0.05 GPa = 50 MPa**). The press is **300 MPa ≫
  50 MPa**, so the binder *yields and plastically flows into the void* — it cannot
  hold rigid particles apart. To act as a spacer the binder would have to **resist
  300 MPa with a 50 MPa yield stress (6× too soft)** → impossible. So porosity is
  monotone *because the soft binder fills void at production pressure*, which is the
  real mechanism. (Literature agrees in direction: Hong's only point, 1 wt%, *lowers*
  porosity; the reported over-binder harm is σ / retention, not a porosity rebound.)
  Forcing a ∪ with an "agglomeration-void / spacer" term would be **wrong physics**,
  not just unvalidated curve-fitting → **not done**.
  ⚠ Regime note: at **low operating pressure** (≲ a few MPa, e.g. tailored-low-P cells)
  the binder may *not* fully yield and a spacer/propping effect could appear — a
  DIFFERENT regime from our 300 MPa press. If that regime is ever targeted, model it
  there with a yield-gated propping term (active only when P < σ_y-scale), not here.

## Verdict on A3
- ✅ **`binder_cap` non-monotonic COHESION is correct and ACTIVE** — it models the
  binder's binding-strength optimum (peak ~1.5 wt%, decline after), which manifests
  in cohesion / integrity / early-servo wallP, exactly where binding strength should.
- ✅ **Monotone porosity is the right answer** — volume-fill dominates; the binder's
  non-monotonic role is mechanical-integrity + transport, not a porosity ∪.
- ⇒ A3 stays as-is. The deliverable was "make the binder's mechanical effect
  distribution-aware (non-monotonic)"; that is done and validated active. The
  **porosity** channel correctly shows volume-fill; the **transport** channel (W2)
  carries the over-binder σ harm. Frame[5]: MPM = mechanics (cohesion/integrity),
  network/W2 = transport (σ-block).
## ✅ A3 CLOSED (2026-06-30) — real physics, no fudge
The binder dual-role is modelled by its REAL mechanisms, split across the right
channels — **not** by bending the porosity number:
1. **mechanical binding strength** → `binder_cap` non-monotonic cohesion
   (mpm3d_compaction `--coh-ptfe`/`--binder-opt-wt`), GPU-confirmed active.
2. **transport σ-block** → `whatif_additives` (W2, PTFE σ_ion ×0.74).
3. **porosity** → monotone volume-fill = correct physics at 300 MPa (soft binder
   yields at 50 MPa ≪ 300 MPa → fills void, cannot prop).
No spacer/agglomeration-void term (wrong physics at production pressure). The
porosity-∪ was a mis-framing; the real over-binder penalty is σ + integrity.
A3 complete; the only adjacent open item is the SEPARATE, literature-gated **CBD
nano-porosity** (deferred) — it redistributes binder solid but does not change total
porosity in a solid-counting model at 300 MPa.

Data: `a3_sweep_out/m_ptfe_{0,0.5,1,2,4,8}.json` (on kserver).
