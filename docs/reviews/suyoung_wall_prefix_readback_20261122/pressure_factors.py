"""Split the verified first-crossing wall pressure difference at matched native displacements."""
import math

def breakdown(coarse, fine, dt8, dt16, width):
    if coarse["u"] != fine["u"]:
        raise ValueError("Two native displacements must coincide")
    if not all(math.isfinite(x) and x > 0 for x in (dt8, dt16, width)):
        raise ValueError("Invalid time or width")
    def checked(part, dt):
        m, v, j = part["M"], part["mean_down"], part["J"]
        if m == 0 and v is None and j == 0 and part["count"] == 0:
            return 0.0, None, 0.0
        if not all(isinstance(x, (int,float)) and math.isfinite(x) and x>0 for x in (m,v,j)) or part["count"] <= 0:
            raise ValueError("Invalid supported wall record")
        rate = m / dt
        p = 10 * (j / dt) / width
        if not math.isclose(10 * rate * v / width, p, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("Native impulse differs from mass-speed product")
        return rate, v, p
    rows = {}
    for phase in ("pre","post"):
        a8,v8,p8 = checked(coarse[phase],dt8)
        a16,v16,p16 = checked(fine[phase],dt16)
        dm = dv = one_side = 0.
        if v8 is None or v16 is None:
            one_side = p8 - p16
            state = "BOTH_EMPTY" if v8 is None and v16 is None else "ONE_SIDED_WALL_SUPPORT"
        else:
            dm = (10 / width) * (a8 - a16) * (v8 + v16) / 2
            dv = (10 / width) * (a8 + a16) * (v8 - v16) / 2
            state = "BOTH_SUPPORTED"
        if not math.isclose(math.fsum((dm,dv,one_side)), p8-p16, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("Per-contact-phase closure")
        rows[phase] = dict(support=state, mass_rate_MPa=dm, speed_MPa=dv, one_sided_MPa=one_side,
                           F8_M=coarse[phase]["M"], F16_M=fine[phase]["M"], F8_M_over_dt=a8, F16_M_over_dt=a16,
                           F8_mean_down=v8,F16_mean_down=v16,F8_pressure_MPa=p8,F16_pressure_MPa=p16)
    total={key:math.fsum(row[key] for row in rows.values()) for key in ("mass_rate_MPa","speed_MPa","one_sided_MPa")}
    d = coarse["p_MPa"] - fine["p_MPa"]
    if not math.isclose(math.fsum(total.values()), d, rel_tol=1e-12, abs_tol=1e-12):
        raise ValueError("Total pressure closure")
    shares={k:100*x/d for k,x in total.items()} if abs(d)>1e-12 else None
    return dict(F8_step=coarse["step"],F16_step=fine["step"],u=coarse["u"],phases=rows,
                F8_minus_F16_MPa=d,contributions=total,signed_percent=shares)

def report(coarse, fine, dt8, dt16, width, summary):
    before=breakdown(coarse[-2],fine[-3],dt8,dt16,width)
    after=breakdown(coarse[-1],fine[-1],dt8,dt16,width)
    if (before["F8_step"],before["F16_step"],after["F8_step"],after["F16_step"])!=(269,538,270,540):
        raise ValueError("Wrong observation window")
    if not math.isclose(after["F8_minus_F16_MPa"],summary["matched"]["coarse_minus_fine_MPa"],rel_tol=1e-12,abs_tol=1e-12):
        raise ValueError("Native summary mismatch")
    return dict(method="symmetric_product_split_per_wall_call",before=before,after=after,
                at_539_total_only=summary["first_exceedance"])
