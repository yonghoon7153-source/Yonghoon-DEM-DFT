"""Export the two registered metrics in the mixer story's existing fractional units."""
import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from statistics import stdev


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compact(u_path, c_path, pair_path):
    raw = [p.read_bytes() for p in (u_path,c_path)]
    u,c = (json.loads(b) for b in raw)
    pair = json.loads(pair_path.read_bytes())
    hashes = [hashlib.sha256(b).hexdigest() for b in raw]
    require(hashes == [pair["sha256"]["u"],pair["sha256"]["c"]], "observer sources differ")
    steps = [32976*i for i in range(134,234)]
    result = dict(label="DEVELOPMENT_DATA_ONLY", arms=["PRECAL_R1_B2_U","PRECAL_R1_B2_C"],
                  jobs=["368758","369734"], generator_seed=32452843, nominal_SE_Bo=[21.244,21.244],
                  gamma_AM_over_gamma_SE=[0.1,1.0], bins="index 134..233 inclusive (100 native frames)",
                  n_independent_seeds=1, sources_sha256=hashes, E0=u["e0_frame"], metrics={})
    require(c["provenance"]["binding"]["seed"] == result["generator_seed"], "C seed mismatch")
    require(u["counts"]["observed_by_type"] == c["counts"]["observed_by_type"], "different species counts")
    den = u["counts"]["observed_by_type"]["3"]
    for section,key,expected in (("s1_se_clusters","se_frac_in_clusters",-1),("s2_am_se_attach","se_attached_any_frac",1)):
        entry = {}
        counts = []
        for arm,doc in (("B2_U",u),("B2_C",c)):
            block = doc["contact"]["bin"]
            require(block["steps"] == [r["step"] for r in block["frames"]] == steps, "nonmatching frames")
            vals = [r[section][key] for r in block["frames"]]
            count = [round(x*den) for x in vals]
            require(all(x == n/den for x,n in zip(vals,count)), "not native SE counts")
            counts.append(count)
            bounds = [block["mean"][prefix+key] for prefix in ("lo.","hi.")]
            mean = float(Fraction(sum(count),den*len(steps)))
            sd = stdev(vals)
            require(bounds[0] <= mean <= bounds[1] and math.isclose(block["mean"][key],mean,rel_tol=1e-14)
                    and math.isclose(block["sd"][key],sd,rel_tol=1e-14), "observer summary disagrees")
            entry[arm] = dict(mean=mean,frame_sd=sd,coordinate_precision_lo_mean=bounds[0],
                              coordinate_precision_hi_mean=bounds[1])
        differences = [b-a for a,b in zip(*counts,strict=True)]
        delta = Fraction(sum(differences),den*len(steps))
        native = pair["metrics"][key]
        matched = delta*expected > 0
        require(delta == Fraction(native["exact_fraction_delta"]) and native["predicted_direction_observed"] == matched,
                "registered exact arithmetic disagrees")
        a,b = (entry[k] for k in ("B2_U","B2_C"))
        entry.update(B2_C_minus_U_mean=float(delta),exact_fraction_delta=str(delta),
                     B2_C_minus_U_frame_sd=stdev([v/den for v in differences]),
                     B2_C_minus_U_coordinate_precision_lo=b["coordinate_precision_lo_mean"]-a["coordinate_precision_hi_mean"],
                     B2_C_minus_U_coordinate_precision_hi=b["coordinate_precision_hi_mean"]-a["coordinate_precision_lo_mean"],
                     predicted_direction_observed=matched)
        result["metrics"][key] = entry
    result["both_directions_observed"] = all(m["predicted_direction_observed"] for m in result["metrics"].values())
    require(result["both_directions_observed"] == pair["both_directions_observed"], "joint verdict")
    return result


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ("u_observer","c_observer","exact_pair","new_output"):
        parser.add_argument(arg,type=Path)
    args=parser.parse_args()
    result=compact(args.u_observer,args.c_observer,args.exact_pair)
    with args.new_output.open("x",encoding="utf8",newline="\n") as f:
        json.dump(result,f,indent=2,allow_nan=False)
        f.write("\n")
