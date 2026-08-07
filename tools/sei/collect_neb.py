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
    # ⚠ 실행 자체가 실패한 경우를 **미수렴과 구분**한다 (2026-08-07 실측).
    #   neb.x 가 없어 mpirun 이 못 띄웠는데 회수기가 "경로 미수렴 — nstep_path 를 늘려"
    #   라고 안내해, 2시간 동안 안 돌고 있는 걸 눈치채지 못했다.
    if re.search(r"unable to launch|could not access or execute|command not found", t):
        r.update({"status": "launch_failed",
                  "blocking_checks": ["⛔ neb.x 실행 자체가 실패했다 — 계산이 안 돌았다. "
                                      "바이너리 경로·실행권한을 볼 것 (NEB=... 로 지정 가능)"],
                  "citable": False,
                  "launch_error": "\n".join(t.splitlines()[:8])})
        return r
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
    # ③ 정·역 대칭성 — ★ **끝점이 대칭적으로 같을 때만** 이 검사가 유효하다.
    #   실측(2026-08-07 spglib): Li₂S 는 Li 궤도 1개(Fm-3m, Wyckoff c)라 정=역이어야 하지만,
    #   Li₃P(P6₃/mmc, b+f)·Li₃PO₄γ(Pnma, d+c)는 **Li 자리가 두 종류**라 정≠역이 정상이다.
    #   그 차이는 버그가 아니라 **두 Li 자리의 에너지 차**다. 이걸 모르고 일괄로 걸면
    #   멀쩡한 결과를 의심스럽다고 잘못 판정한다 — 입력 단계에서 기록한 meta.json 을 읽는다.
    meta = {}
    mp = os.path.join(d, "meta.json")
    if os.path.isfile(mp):
        try:
            meta = json.load(open(mp, encoding="utf-8"))
        except (OSError, ValueError):
            meta = {}
    eqv = meta.get("endpoints_symmetry_equivalent")
    r["endpoints_symmetry_equivalent"] = eqv
    r["li_orbits"] = meta.get("li_orbits")
    r["supercell"] = meta.get("supercell")
    r["min_cell_A"] = meta.get("min_cell_A")
    if r["Ea_forward_eV"] is not None and r["Ea_backward_eV"] is not None:
        f_, b_ = r["Ea_forward_eV"], r["Ea_backward_eV"]
        asym = abs(f_ - b_)
        r["asymmetry_eV"] = asym
        # ★ 장거리 수송에 걸리는 유효 장벽 = 안장점 − **가장 낮은 자리** = max(정, 역).
        #   대칭 홉이면 둘이 같으니 자동으로 맞고, 비대칭 홉이면 이게 물리적으로 맞는 값이다.
        r["Ea_effective_eV"] = max(f_, b_)
        r["site_energy_diff_eV"] = asym if eqv is False else None
        # 대칭이어야 하는 경우에만 게이트를 건다
        r["symmetric"] = (asym < 0.02) if eqv else None
    checks = []
    if not conv:
        checks.append("경로 미수렴 — nstep_path 를 늘려 이어서 돌릴 것" if acts
                      else "아직 에너지가 안 나왔다 — 시작 직후이거나 첫 SCF 중")
    if r.get("CI_scheme") in (None, "no-CI"):
        checks.append("CI 가 꺼져 있다 — 장벽이 이미지 격자만큼 과소평가된다")
    if r.get("symmetric") is False:
        checks.append(f"정·역 장벽이 {r['asymmetry_eV']:.3f} eV 어긋난다 — "
                      f"이 상은 Li 자리가 한 종류라 같아야 한다 "
                      f"(끝점 하나가 다른 국소최소로 흘렀을 수 있다)")
    if eqv is None and os.path.isfile(mp) is False:
        checks.append("meta.json 이 없어 대칭 판정을 못 한다 — 생성기를 다시 돌릴 것")
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
    print(f"{'상':12s} {'상태':12s} {'Ea→':>8s} {'Ea←':>8s} {'유효Ea':>8s} {'끝점':>6s} {'스텝':>5s}  판정")
    for d in dirs:
        r = read_one(d)
        res[r["tag"]] = r
        f = r.get("Ea_forward_eV"); b = r.get("Ea_backward_eV")
        ef = r.get("Ea_effective_eV"); eq = r.get("endpoints_symmetry_equivalent")
        print(f"{r['tag']:12s} {r['status']:12s} "
              f"{(f'{f:.4f}' if f is not None else '—'):>8s} "
              f"{(f'{b:.4f}' if b is not None else '—'):>8s} "
              f"{(f'{ef:.4f}' if ef is not None else '—'):>8s} "
              f"{('대칭' if eq else ('비대칭' if eq is False else '?')):>6s} "
              f"{r.get('n_path_steps', 0):5d}  "
              + ("✅ 인용 가능" if r.get("citable") else
                 ("⚠ " + " · ".join(r.get("blocking_checks") or ["진행 중"]))[:64]))
        if r.get("site_energy_diff_eV"):
            print(f"{'':12s} └ Li 자리 두 종류 {r.get('li_orbits', {}).get('wyckoffs')} — "
                  f"정·역 차 {r['site_energy_diff_eV']:.3f} eV 는 **자리 에너지 차**다(정상). "
                  f"수송 장벽은 유효Ea 를 쓴다")
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
