"""Minimal reproductions on the HEAD snapshot (dfe26fcd4) — numbers for the design table."""
import math
from g2lib import PC, NC, ESTAR, area_variant, rc_from_area, geom_disk

print('HEAD constants: E*_AMSE=%.6g  H=%.3g  H_FILM_MIN=%.3g  DR_YIELD_ONSET=%.6g  DR_FULLY_PLASTIC=%.6g'
      % (PC.E_STAR_AM_SE, PC.H_REAL_SE, PC.H_FILM_MIN, PC.DR_YIELD_ONSET, PC.DR_FULLY_PLASTIC))
print('E* by pair (GPa):', {k: round(v / 1e9, 4) for k, v in ESTAR.items()})

# ── DESC-03 : sim(mm) units vs SI, r = 0.5 µm both, δ/R* = 0.05 ──
r = 0.5e-6; Rs = r / 2; d = 0.05 * Rs
for lab, s in (('SI (m)', 1.0), ('sim (mm = SI×1e3, what build_network passes)', 1e3)):
    A, reg, c = PC.film_area_from_overlap(d * s, Rs * s, R_min=r * s, ligg_area=0.0, mode='physics',
                                          return_components=True)
    print(f'DESC-03 {lab:45s} binding={c["binding"]:7s} A/A_hertz={A / c["A_hertzian"]:.6f} '
          f'A_volume/A_tabor={c["A_volume"] / c["A_tabor"]:.6g}')

# ── L1-02 : legacy V vs exact lens ──
r = 0.5
for d in (0.0125, 0.95):
    print(f'L1-02 r=0.5 δ={d}: legacy={PC.legacy_v_overlap(d, r / 2):+.12f}  exact={PC.lens_volume(r, r, d):+.12f}'
          f'  ratio={PC.legacy_v_overlap(d, r / 2) / PC.lens_volume(r, r, d):.6f}')

# ── L1-01 : SI, r = 0.5 µm, δ/R* = 0.01, ligg = intersection disc ──
r = 0.5e-6; Rs = r / 2; d = 0.01 * Rs
ligg = geom_disk(r, r, d)
A, reg, c = PC.film_area_from_overlap(d, Rs, R_min=r, ligg_area=ligg, mode='physics', return_components=True)
print(f'L1-01 binding={c["binding"]} cap_conflict={c["cap_conflict"]} A/A_tabor={A / c["A_tabor"]:.6f} '
      f'A/A_volume={A / c["A_volume"]:.6f}')

# ── L1-03 : same geometry, three pairs → same area (no pair argument) ──
r = 0.5e-6; Rs = r / 2; d = 0.05 * Rs
for pair in ('AM_AM', 'AM_SE', 'SE_SE'):
    A, reg = PC.film_area_from_overlap(d, Rs, R_min=r, ligg_area=0.0, mode='physics')
    print(f'L1-03 {pair}: A={A * 1e12:.10f} µm² (helper has no pair/E*/H argument) ; '
          f'A_tabor would scale ×{ESTAR[pair] / ESTAR["AM_SE"]:.4f} with own E*')

# ── SELF-28 ladder r_SE 0.5 ↔ r_AM 6.0 µm, ligg = 0 : legacy divide vs multiply (σ=1, k=1) ──
r1, r2 = 0.5, 6.0
print('SELF-28 ladder (µm): δ, A_phys, binding, s, ψ, R_c(divide), R_c(multiply), R_Holm(a)')
for d in (0.02, 0.05, 0.10, 0.1023, 0.1025, 0.12, 0.20):
    A, b, cc = area_variant(d, r1, r2, 0.0, 'AM_SE', var='G1')
    Rd, s, psi = rc_from_area(A, r1, r2, 1.0, 'divide')
    Rm, _, _ = rc_from_area(A, r1, r2, 1.0, 'multiply')
    a = math.sqrt(A / math.pi)
    print(f'   {d:.4f}  {A:.6f}  {b:8s} s={s:.6f} ψ={psi:.6g}  Rd={Rd:.6g}  Rm={Rm:.6g}  Holm={1/(2*min(a, 0.5)):.6g}')
# floor band under multiply: worst-case jump
s_star = 1 - PSI_FLOOR ** (2 / 3) if (PSI_FLOOR := 1e-4) else None
print(f'floor: ψ≤1e-4 ⟺ s≥{s_star:.11f} ; multiply jump at floor = 1e-4/(2σ·{s_star:.5f}·r_min) '
      f'= {1e-4 / (2 * s_star):.4g}/(σ r_min) ; vs R_bulk(equal r, δ→0) = 2/(π σ r) = {2 / math.pi:.4g}/(σ r) '
      f'→ ratio {1e-4 / (2 * s_star) / (2 / math.pi):.3g}')
