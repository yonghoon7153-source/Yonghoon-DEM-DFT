import json, numpy as np, sys
sys.path.insert(0, ".")
from src.config import load_config
from src.halfcell import compute_halfcell_from_ocp, RECIPE_DEFAULTS
cfg = load_config("configs/base.yaml")
d = RECIPE_DEFAULTS["ocpbias"]; yt, yb = d["pe_tilt_y_top"], d["pe_tilt_y_bot"]
base = compute_halfcell_from_ocp(cfg)
out = {"y_T": yt, "y_B": yb}
for name, kw in {"U5": dict(pe_offset_mv=5), "U10": dict(pe_offset_mv=10), "T5": dict(pe_offset_mv=5, pe_tilt_mv=10),
                 "T10": dict(pe_offset_mv=10, pe_tilt_mv=20), "L6": dict(pe_tilt_mv=10)}.items():
    r = compute_halfcell_from_ocp(cfg, **kw)
    assert np.array_equal(r.y_pe, base.y_pe)
    dmv = (r.u_pe - base.u_pe) * 1000
    y = r.y_pe
    top, bot, mid = dmv[y <= yt], dmv[y >= yb], (y >= yt) & (y <= yb)
    yy = np.linspace(yt, yb, 200001); win_mean = float(np.mean(np.interp(yy, y, dmv)))
    out[name] = {"top_mv": [round(float(top.min()), 9), round(float(top.max()), 9)],
                 "bottom_mv": [round(float(bot.min()), 9), round(float(bot.max()), 9)],
                 "window_mean_mv": round(win_mean, 6), "ne_unchanged": bool(np.array_equal(r.u_ne, base.u_ne))}
# U5 와 옛 균일 식 (u_pe + 5/1000) 의 비트 일치
r5 = compute_halfcell_from_ocp(cfg, pe_offset_mv=5)
out["U5_bit_equal_old_uniform"] = bool(np.array_equal(r5.u_pe, base.u_pe + 5 / 1000.0))
print(json.dumps(out, indent=1))
