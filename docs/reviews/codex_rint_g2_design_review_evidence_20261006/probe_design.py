"""Independent review calculations; no production edits, no bed/GPU campaign.
Run with NumPy/SciPy on PYTHONPATH. All material values below are synthetic.
"""
from pathlib import Path
import contextlib, hashlib, io, itertools, json, math, sys
import numpy as np
import scipy

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "source" / "scripts"))
import step3_sigma as s3
from lens_geometry import intersection_disc_area

def calculate():
    out = {"environment": {"python": sys.version, "numpy": np.__version__, "scipy": scipy.__version__}}
    # Byte identity of files fetched at the fixed request commit.
    manifest = json.loads((ROOT / "source_manifest.json").read_text(encoding="utf8"))
    checks = []
    for row in manifest["files"]:
        b = (ROOT / "source" / row["path"]).read_bytes()
        actual = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        assert actual == row["git_blob"], (row["path"], actual, row["git_blob"])
        checks.append({"path": row["path"], "git_blob": actual, "sha256": hashlib.sha256(b).hexdigest()})
    out["source_verification"] = checks

    # The original hand calculation in §3-3.
    r1, r2, delta = 6., 2., .05
    d = r1 + r2 - delta
    plane = (d*d+r1*r1-r2*r2)/(2*d)
    bridge_center = r1 - delta/2
    out["radical_plane_um"] = {"plane": plane, "bridge": bridge_center, "offset": plane-bridge_center}

    # E4 uses r'=r_face*1e4, an area-reduced term, not edge resistance.
    h, sig, rface = .2, .01, .01024
    rho_half, rho_film = h/sig, rface*1e4
    gcode = h*h/(rho_half+rho_film)
    phi_jump = 1.
    icode = gcode*phi_jump
    ptotal_code = gcode*phi_jump**2
    wrong = icode**2*rho_film/ptotal_code
    correct = icode**2*(rho_film/h**2)/ptotal_code
    eps = 1e-5
    gp = h*h/(rho_half + rho_film*math.exp(eps))
    gm = h*h/(rho_half + rho_film*math.exp(-eps))
    fd = -(math.log(gp)-math.log(gm))/(2*eps)
    actual_g = s3.interface_face_g(
        np.full(1,sig*h),np.full(1,sig),np.full(1,sig),np.full(1,rface),h)
    assert np.allclose(actual_g,gcode,rtol=1e-14,atol=0)
    assert abs(fd-correct) < 1e-8
    out["E4_area_factor"] = {"h_um":h, "rface_ohm_cm2":rface, "R_half_reduced":rho_half,
        "rprime_reduced":rho_film, "g_code":gcode, "actual_function_g_code":actual_g.tolist(),
        "printed_Icode_squared_rprime_over_P":wrong,
        "correct_film_share":correct, "log_derivative_FD":fd,
        "correct_to_printed_ratio":correct/wrong}

    # Same total film conductance, different trace energy in the continuum:
    # phi jump = 1 + beta*x on a circular interface.
    a2 = 1.-(.99)**2
    b, beta = .24, 4.
    area = math.pi*a2
    actual_a = intersection_disc_area(1.,1.,.02)
    assert math.isclose(actual_a,area,rel_tol=1e-13)
    true_energy_factor = 1 + beta*beta*a2/4
    smeared_energy_factor = 1 + beta*beta*b*b/4
    out["support_smearing_continuum"] = {
        "a_um":math.sqrt(a2), "Atrue_um2":area, "lens_function_area_um2":actual_a,
        "b_um":b, "beta_per_um":beta, "sum_g_same":True,
        "P_true_div_G":true_energy_factor,
        "P_smeared_div_G":smeared_energy_factor,
        "P_relative_difference":smeared_energy_factor/true_energy_factor-1,
        "support_area_ratio":math.pi*b*b/area,
        "masked_two_parallel_patches": {"before_R":1., "remove_one_fixed_patch_R":2.,
                                         "renormalize_full_area_onto_remaining_R":1.}}

    # Exact concentric sphere l=1 solution in an outer sphere of radius L.
    # Dirichlet phi=-E*L*cos(theta), equivalent boundary response:
    # k_eff/k_m=(1+2*beta*(a/L)^3)/(1-beta*(a/L)^3).
    ki, km, film_over_a = 10.,1.,1.
    keq = ki/(1+film_over_a*ki)
    b_correct = (keq-km)/(keq+2*km)
    b_wrong = (ki-km)/(ki+2*km)  # mutant: film operator entirely missing.
    rows = []
    for L_a in (5.,10.,20.,40.,80.):
        f = L_a**-3
        kc = km*(1+2*b_correct*f)/(1-b_correct*f)
        kw = km*(1+2*b_wrong*f)/(1-b_wrong*f)
        rows.append({"outer_radius_over_a":L_a,"volume_fraction":f,"correct_k":kc,
                     "film_deleted_k":kw,"absolute_difference":abs(kw-kc),
                     "difference_div_volume_fraction":abs(kw-kc)/f})
    out["sphere_dilution_false_pass"] = {"sigma_eq":keq, "beta_correct":b_correct,
        "beta_film_deleted":b_wrong, "polarizability_error":b_wrong-b_correct, "rows":rows}

    # Actual current producer: changing input order changes sid, even when a
    # separately defined radical-plane owner would be unchanged.
    c = np.array([[1.,1.,1.],[1.,1.,2.9]])
    rad = np.ones(2)
    typ = np.array([2,1])  # first AM_S, second AM_P.
    lo, hi, vox = (0.,0.,0.), (2.,2.,3.9), .1
    sigtable = np.zeros(10); sigtable[1]=.01; sigtable[2]=.005
    rows, fields = [], []
    for perm in ([0,1],[1,0]):
        sid,pid = s3.rasterize(c[perm],rad[perm],typ[perm],None,None,lo,hi,vox,bridge_um=.24)
        with contextlib.redirect_stdout(io.StringIO()):
            res = s3.solve_sigma_z(sid,sigtable,vox,z_bot_um=0,z_top_um=3.9)
        assert res["cg_info"] == 0 and not res["unconverged"] and np.isfinite(res["resid"]), res
        fields.append(sid)
        rows.append({"permutation":perm,"sigma_eff_S_cm":res["sigma_eff"],
                     "unconverged":res["unconverged"],"cg_info":res["cg_info"],"resid":res["resid"],
                     "sid1_cells":int((sid==1).sum()),"sid2_cells":int((sid==2).sum())})
    out["actual_raster_order"]={"R_um":1.,"delta_um":.1,"vox_um":vox,"bridge_um":.24,
        "changed_sid_cells":int((fields[0]!=fields[1]).sum()),"rows":rows,
        "relative_sigma_change":rows[1]["sigma_eff_S_cm"]/rows[0]["sigma_eff_S_cm"]-1}
    assert out["actual_raster_order"]["changed_sid_cells"] == 16
    assert out["actual_raster_order"]["relative_sigma_change"] > .04

    # The T1-4 "direct-edge equality" must include the same finite half cells.
    Rj,h,sig = 100.,1.,1e8
    # Correct physical bulk resistance is length_cm/(sigma*area_cm2).
    out["units_direct_vs_face"]={"face_physical_G_S":1/(Rj+1e4/(sig*h)),
        "direct_physical_G_S":1/Rj,"halfcell_total_R_ohm":1e4/(sig*h)}

    # J2 ambiguity: fiber-fiber and fiber-sphere have distinct radius sums.
    rf,ram,dmin = .075,2.,2.12
    out["fiber_sphere_threshold"]={"r_f_um":rf,"r_AM_um":ram,"distance_um":dmin,
        "correct_contact_threshold_um":rf+ram,"literal_J2_threshold_um":2*rf+ram,
        "correct_contact":dmin<=rf+ram,"literal_J2_contact":dmin<=2*rf+ram}

    # Multi-class envelope identity: if both parameters vary, sum shares.
    rA,rB,bulk = 1.,2.,3.
    out["multiclass_envelope"]={"R_total_ohm":bulk+rA+rB,"share_A":rA/(bulk+rA+rB),
        "share_B":rB/(bulk+rA+rB),"joint_log_derivative":(rA+rB)/(bulk+rA+rB),
        "all_resistance_log_gain":math.log(bulk/(bulk+rA+rB)),
        "only_A_integral_while_both_scaled":rA/(rA+rB)*math.log(bulk/(bulk+rA+rB))}

    # Check manufactured solution and equivalent-sphere mapping algebraically.
    alpha,beta,sig1,sig2,r,v = 2.,3.,2.,5.,.1,.4
    grad1=alpha+beta*v;grad2=sig1/sig2*grad1
    phi1=0.;phi2=r*sig1*grad1
    Jn=-sig1*grad1
    out["mms_sign_check"]={"normal_from_1_to_2":True,"normal_flux_1":Jn,
        "normal_flux_2":-sig2*grad2,"phi1_minus_phi2":phi1-phi2,"r_times_Jn":r*Jn}
    return out

if __name__ == "__main__":
    result = calculate()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    (ROOT/"evidence.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
