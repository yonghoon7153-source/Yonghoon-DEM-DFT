# DF-01 independent check: is the hinted profile grid built so that method-(a) endpoints are exact grid points?
import json, numpy as np
j = json.load(open("out/degeneracy_300_0009_Li_v2.json"))
best_modes = j["best_modes_percent"]
for k in ("LAM_PE","LAM_NE","LLI"):
    d = j[k+"_percent"]; ext = d["from_constrained_extrema"]; pr = d["from_mode_profile"]
    h_lo, h_hi = ext["min"]/100, ext["max"]/100          # fractions, as in verify.py
    pad = max((h_hi-h_lo)*0.5, 1e-4)
    g_lo, g_hi = h_lo-pad, h_hi+pad                      # assume no clamp by box -> verify vs stored grid_range_pct
    stored = pr["grid_range_pct"]
    clamp_ok = np.allclose([g_lo*100, g_hi*100], stored, rtol=0, atol=1e-12)
    grid = np.unique(np.concatenate([np.linspace(g_lo, g_hi, 21), [best_modes[k]/100]]))*100
    # index of the profile min/max in the grid and of ext endpoints
    def idx(v): 
        i = int(np.argmin(abs(grid-v))); return i, grid[i]-v
    imin, dmin = idx(pr["min"]); imax, dmax = idx(pr["max"])
    e_lo, de_lo = idx(ext["min"]); e_hi, de_hi = idx(ext["max"])
    n_contig = imax-imin+1 + (1 if not any(abs(grid[imin:imax+1]-best_modes[k])<1e-12) and imin<=idx(best_modes[k])[0]<=imax else 0)
    # count grid points (incl. best) that lie inside [prof.min, prof.max]
    inside = int(np.sum((grid>=pr["min"]-1e-12)&(grid<=pr["max"]+1e-12)))
    print(f"{k}: stored grid range matches unclamped hint±pad: {clamp_ok}; n_grid={grid.size}(json {pr['n_grid']})")
    print(f"   ext.min -> grid idx {e_lo} (delta {de_lo:.1e}), ext.max -> grid idx {e_hi} (delta {de_hi:.1e})")
    print(f"   prof.min = grid[{imin}] (delta {dmin:.1e}), prof.max = grid[{imax}] (delta {dmax:.1e}); prof.min==ext.min {pr['min']==ext['min']}, prof.max==ext.max {pr['max']==ext['max']}")
    print(f"   grid points inside [prof.min,prof.max] incl. best = {inside} vs n_grid_attainable {pr['n_grid_attainable']} -> contiguous={inside==pr['n_grid_attainable']}; grid step = {grid[1]-grid[0]:.4f} %p")
print("is_lower_bound:", {k: j[k+'_percent']['is_lower_bound'] for k in ('LAM_PE','LAM_NE','LLI')}, "LLI span", j['LLI_percent']['span'])
