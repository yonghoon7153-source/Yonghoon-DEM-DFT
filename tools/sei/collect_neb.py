#!/usr/bin/env python3
"""collect_neb.py — NEB 결과를 읽어 **장벽과 그 신뢰 근거**를 같이 낸다.

왜 "장벽만" 안 내나
  NEB 의 barrier 는 세 가지가 맞아야 의미가 있다.
    ① 경로가 **수렴**했나 (`neb: convergence achieved`)
    ② **CI(climbing image)** 가 켜져 최고점을 실제로 올라탔나 — 안 그러면 이미지 격자
       때문에 장벽이 과소평가된다
    ③ 정·역 장벽이 **거의 같은가** — 공공 매개 홉은 시작·끝이 대칭 자리라 크게 다르면
       끝점 하나가 다른 국소최소로 흘렀다는 뜻이다
  셋 다 안 보고 숫자만 옮기면 조용히 틀린 값이 논문에 들어간다.

  python3 tools/sei/collect_neb.py
  python3 tools/sei/collect_neb.py --work /data/work/runs/sei_neb
"""
import argparse
import glob
import json
import os
import re
import sys

OUT = "db/properties/sei_neb.json"
# QE neb.x 가 찍는 줄:
#   activation energy (->) =   0.286745 eV
#   activation energy (<-) =   0.286712 eV
_ACT = re.compile(r"activation energy\s*\((->|<-)\)\s*=\s*(-?[\d.]+)\s*eV")
_IMG = re.compile(r"num_of_images\s*=\s*(\d+)")
_CI = re.compile(r"CI_scheme\s*=\s*'([^']+)'")


def read_one(d):
    tag = os.path.basename(d)
    out = os.path.join(d, "neb.out")
    r = {"tag": tag, "status": "not_started"}
    if not os.path.isfile(out):
        return r
    t = open(out, errors="ignore").read()
    inp = ""
    if os.path.isfile(os.path.join(d, "neb.in")):
        inp = open(os.path.join(d, "neb.in"), errors="ignore").read()
    acts = _ACT.findall(t)
    fwd = [float(v) for k, v in acts if k == "->"]
    bwd = [float(v) for k, v in acts if k == "<-"]
    conv = "neb: convergence achieved" in t
    r.update({
        "status": "converged" if conv else ("running" if acts else "no_energy_yet"),
        "n_path_steps": len(fwd),
        "Ea_forward_eV": fwd[-1] if fwd else None,
        "Ea_backward_eV": bwd[-1] if bwd else None,
        "num_of_images": int(_IMG.search(inp).group(1)) if _IMG.search(inp) else None,
        "CI_scheme": _CI.search(inp).group(1) if _CI.search(inp) else None,
        "tot_charge": ("+1 (Li+ vacancy)" if "tot_charge      = 1.0" in inp
                       or "tot_charge = 1.0" in inp else "0 (⚠ 중성 공공 — 정공 오염 주의)"),
    })
    # ③ 정·역 대칭성 — 공공 매개 홉은 대칭 자리라 거의 같아야 한다
    if r["Ea_forward_eV"] is not None and r["Ea_backward_eV"] is not None:
        asym = abs(r["Ea_forward_eV"] - r["Ea_backward_eV"])
        r["asymmetry_eV"] = asym
        r["symmetric"] = asym < 0.02
    checks = []
    if not conv:
        checks.append("경로 미수렴 — nstep_path 를 늘려 이어서 돌릴 것")
    if r.get("CI_scheme") in (None, "no-CI"):
        checks.append("CI 가 꺼져 있다 — 장벽이 이미지 격자만큼 과소평가된다")
    if r.get("symmetric") is False:
        checks.append(f"정·역 장벽이 {r['asymmetry_eV']:.3f} eV 어긋난다 — "
                      f"끝점 하나가 다른 국소최소로 흘렀을 수 있다")
    if "tot_charge" in r and r["tot_charge"].startswith("0"):
        checks.append("중성 공공이라 원자가띠에 정공이 생긴다 — tot_charge=+1 로 다시 걸 것")
    r["blocking_checks"] = checks
    r["citable"] = conv and not checks
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=os.environ.get("WORK", "/data/work/runs/sei_neb"))
    a = ap.parse_args()
    dirs = sorted(d for d in glob.glob(os.path.join(a.work, "*")) if os.path.isdir(d))
    if not dirs:
        print(f"⛔ {a.work} 에 작업 폴더가 없다 — build_neb_inputs.py 부터")
        return 1
    res = {}
    print(f"{'상':12s} {'상태':12s} {'Ea→(eV)':>9s} {'Ea←(eV)':>9s} {'비대칭':>8s} {'스텝':>5s}  판정")
    for d in dirs:
        r = read_one(d)
        res[r["tag"]] = r
        f = r.get("Ea_forward_eV"); b = r.get("Ea_backward_eV"); s = r.get("asymmetry_eV")
        print(f"{r['tag']:12s} {r['status']:12s} "
              f"{(f'{f:.4f}' if f is not None else '—'):>9s} "
              f"{(f'{b:.4f}' if b is not None else '—'):>9s} "
              f"{(f'{s:.4f}' if s is not None else '—'):>8s} "
              f"{r.get('n_path_steps', 0):5d}  "
              + ("✅ 인용 가능" if r.get("citable") else
                 ("⚠ " + " · ".join(r.get("blocking_checks") or ["진행 중"]))[:70]))
    ok = [r for r in res.values() if r.get("citable")]
    if ok:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump({
            "property": "sei_li_migration_barrier_neb",
            "method": ("QE CI-NEB (neb.x). 공공 매개 Li 홉, tot_charge=+1 (Li⁺ 공공, jellium). "
                       "ecutwfc 60 / ecutrho 480 Ry — 갭 계산과 같은 사양."),
            "warning": ("⚠ jellium 보정은 유한 셀 근사다 — 절대값은 셀 수렴 확인 뒤 인용할 것. "
                        "**상 사이 비교**가 이 값의 용도다. "
                        "⛔ BVSE 프록시 값과 같은 표에 놓지 말 것(단위는 같아도 다른 양이다)."),
            "results": res,
        }, open(OUT, "w"), ensure_ascii=False, indent=2)
        print(f"\n→ {OUT}  (인용 가능 {len(ok)}/{len(res)})")
    else:
        print("\n(아직 인용 가능한 결과가 없다 — JSON 을 쓰지 않았다)")
    print("⚠ 장벽은 **상 사이 비교**용이다. jellium 유한 셀 보정이 남아 있으니")
    print("  절대값을 실험과 나란히 놓기 전에 셀 크기 수렴을 확인할 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
