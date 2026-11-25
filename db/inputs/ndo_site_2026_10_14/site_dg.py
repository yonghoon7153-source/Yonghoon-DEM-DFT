#!/usr/bin/env python3
"""site_dg.py — 자리 비교 2 단계: UMA 어닐 결과 → 모델별 최저 · ΔG_site(UMA) (조성 균형 · Li₂S/Li₃PS₄ 교환)

  ΔG_site = { [E(M@P) − E(M@Li)] − [a·e(Li₂S) + b·e(Li₃PS₄)] } / n_M        (eV / 도펀트 · > 0 ⇒ P 자리 불리)
  M@P − M@Li 의 조성차를 a·Li₂S + b·Li₃PS₄ 로 **정확히** 닫는다 (P 로 b · S 로 a · Li 검산 · 다른 원소 차 0).
  이번 캠페인의 두 모델은 n·(+5 Li −1 P) = n·(4 Li₂S − Li₃PS₄) 다 (a = 4n · b = −n).
  카드: db/properties/b2o3_site_screen_estimand_2026_10_14.json · db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json

입력
  --anneal  run_anneal.py 의 anneal_results.json (여러 개) — 이름 [M]MP_ii · [M]MLi_ii · [M]host_ii
  --refs    기준상 이완 (run_uma_kgy.sh --refs) 의 anneal_results.json
  종류는 이름으로, 도펀트는 조성 (Li P S O Cl 밖의 원소) 으로 가른다. 조성은 각 레코드의 post_relax.xyz 에서 센다
  (그래서 결과 폴더가 있는 기계 — kgy — 에서 돌린다).

게이트 (카드가 결과 전에 정한 것 중 기계로 볼 수 있는 것만)
  · 오류 레코드 · 미수렴 이완이 하나라도 있으면 ΔG 를 내지 않는다 (B 카드 G1 '다 있어야 계산한다').
    --allow_incomplete 면 그것들을 빼고 내되 뺀 이름을 찍는다.
  · --expect N: 모델마다 N 개 (오류 · 미수렴 포함 셈) 가 있어야 한다.
  · 같은 모델 안 조성이 다르면 · 조성차가 Li₂S/Li₃PS₄ 로 안 닫히면 · 도펀트 수가 다르면 멈춘다.
  · 모델별 최저와 둘째의 차를 찍는다 (B G3).
  · --thresholds: |ΔG| 가 판정 문턱에서 0.11 eV 안이면 '다형 재확인 발동' (B G4 · Nd G7 · 0.11 = MP 다형 차 0.0138 eV/atom × 8).
    'B=0.20 Nd=0' 처럼 도펀트별로, 또는 '0.20' 처럼 전부에.

⛔ 이 도구가 못 하는 것
  · 판정 문장을 쓰지 않는다 — 허용 · 금지 서술은 카드에서만 가져온다.
  · UMA 가 맞는지 모른다 (UMA 내부 비교다) · DFT 를 하지 않는다.
  · 최저가 진짜 바닥인지 모른다 — 모델마다 같은 탐색 예산 (N 개) 안의 최저다.
  · 저장소는 Li₂S/Li₃PS₄ 교환 하나다 (회신 BG — 다른 μ 꼭짓점은 안 본다).
  · Li₃PS₄ 다형을 스스로 바꾸지 않는다 — --refs 에 준 다형 하나를 쓴다.

  종료 코드: 0 모든 도펀트 ΔG 냄 · 3 하나라도 거절 (위 게이트 · 화면에 이유) · 1 멈춤 (⛔ 조성 · 기준상 · 이름 이상)
  --out · --bundle 파일은 화면 출력 **전에** 쓴다 (출력이 끊겨도 남는다).

  python3 site_dg.py --selftest
  python3 site_dg.py --anneal $R/uma_anneal/anneal_results.json --refs $R/uma_ref_relax/anneal_results.json \
      --expect 10 --top 3 --out $R/site_dg_rietveld.json --bundle <폴더>

DFT 모드 (2026-10-15 · Nd 카드 Q1 · 계산부는 위와 같은 analyze())
  --qe <폴더>   run_force_check_scf.sh 꼴 (<이름>/scf.in · scf.out) — 기준상은 조성 (Li · P · S 만) 으로 가른다
    · 완료 = 러너 _fc_ok 와 **같은 판정** (selftest 가 러너 파일에서 함수를 떼어 9 fixture 로 대조)
    · 에너지 = 마지막 '!' 줄 (vc-relax 면 최종 scf) × RYTOEV · 조성 = scf.in 의 ATOMIC_POSITIONS
    · 후보가 하나라도 미완료 · 안 돌았으면 ΔG 를 내지 않는다 (종료 3) · 기준상이 미완료면 멈춘다 (종료 1)
  --compare_uma <site_dg_rietveld.json>  G2 UMA 부호 대조 · --g3 0.30  G3 여유 (고정셀 + EOS 발동 여부)
  --kprobe <폴더>  G4 — k 한 단계 올린 두 모델 최저 셀 (<폴더>/<이름>/scf.*) · ΔG 움직임 > 0.05 eV 면 발동
  --thresholds Nd=0.30  G7 다형 재확인 (단일점 판정 문턱 0.30 에서 0.11 안) — EOS 뒤 판정이면 Nd=0.10
  ⛔ DFT 모드가 못 하는 것: EOS (G3) · 다형 (G7) 을 돌리거나 맞추지 않는다 — 발동 여부만 표시한다 ·
     판정 문장을 쓰지 않는다 (카드 §5 에서만) · k 탐침 입력을 만들지 않는다
  python3 site_dg.py --qe $R --expect 3 --top 3 --thresholds Nd=0.30 --compare_uma <UMA 요약 json> \
      --out $R/site_dg_dft.json --bundle $R/bundle_dft
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import Counter
from pathlib import Path

HOST_EL = {"Li", "P", "S", "O", "Cl"}
NAME = re.compile(r"^(?P<pre>[A-Za-z]*?)(?P<kind>MP|MLi|host)_(?P<i>\d+)$")
POLY_MARGIN = 0.11          # eV/도펀트 — 카드 B G4 · Nd G7
KIND_LABEL = {"MP": "M@P", "MLi": "M@Li"}


def _read_comp(path):
    from ase.io import read
    return Counter(read(path).get_chemical_symbols())


def formula(c):
    return "".join(f"{e}{c[e]}" for e in sorted(c))


# ═══ DFT 모드 (2026-10-15 · Nd 카드 Q1 · QE 출력에서 같은 계산) ══════════════════════════════
#   QE 출력을 어닐 레코드와 **같은 꼴**로 바꿔 analyze() 를 그대로 쓴다 — 계산부는 한 곳이다.
#   'post_relax_xyz' 자리에 scf.in 경로를 넣고 조성은 qe_comp 로 센다 (계산부를 안 건드리려고 이름은 그대로 둔다).
RY_EV = 13.605693122994      # QE constants.f90 RYTOEV (= AUTOEV / 2)
G3_MARGIN = 0.30             # 카드 G3 — |ΔG_site(DFT 단일점)| < 0.30 eV/Nd 면 고정셀 + EOS 이완 뒤에만 부호 (10-15 개정)
G4_MOVE = 0.05               # 카드 G4 — k 한 단계 올린 탐침에서 ΔG 가 이만큼 넘게 움직이면 전 점을 그 k 로 다시
ENERGY = re.compile(r"^!+\s+total energy\s+=\s+(-?\d+\.\d+)\s+Ry", re.M)
KPTS = re.compile(r"K_POINTS\s+automatic\s*\n\s*(\d+\s+\d+\s+\d+)")


def qe_done(out, inp):
    """완료 판정 — 러너 tools/doping/run_force_check_scf.sh::_fc_ok 와 **같은 판정**이어야 한다
    (재개 · 성공 · 판독이 한 기준 · selftest 가 두 구현을 같은 fixture 로 대조한다). → (완료?, 이유)."""
    out, inp = Path(out), Path(inp)
    if not out.exists():
        return False, "scf.out 없음"
    t = out.read_text(errors="replace")
    for need in ("JOB DONE", "convergence has been achieved", "Forces acting on atoms"):
        if need not in t:
            return False, f"'{need}' 없음"
    s = inp.read_text(errors="replace") if inp.exists() else ""
    if re.search(r"tstress *= *\.true\.", s, re.I) and not re.search(r"total +stress", t):
        return False, "tstress 인데 응력 블록 없음"
    if re.search(r"calculation *= *'(vc-)?relax'", s, re.I):
        if "bfgs converged in" not in t:
            return False, "relax 인데 'bfgs converged in' 없음"
        if re.search(r"calculation *= *'vc-relax'", s, re.I):
            lines = t.splitlines()
            e = [i for i, ln in enumerate(lines) if "End final coordinates" in ln]
            f = [i for i, ln in enumerate(lines) if ln.startswith("!")]
            if not e or not f or f[-1] <= e[-1]:
                return False, "vc-relax 인데 최종 scf 에너지가 'End final coordinates' 뒤에 없음"
    return True, ""


def qe_energy_eV(out):
    """마지막 '!' 총에너지 (vc-relax 면 최종 scf) → eV. 없으면 None."""
    out = Path(out)
    m = ENERGY.findall(out.read_text(errors="replace")) if out.exists() else []
    return float(m[-1]) * RY_EV if m else None


def qe_comp(scf_in):
    """scf.in 의 ATOMIC_POSITIONS 블록 (nat 줄) 에서 원소를 센다."""
    t = Path(scf_in).read_text(errors="replace")
    nat = int(re.search(r"^\s*nat\s*=\s*(\d+)", t, re.M).group(1))
    rows = t.split("ATOMIC_POSITIONS", 1)[1].splitlines()[1:1 + nat]
    c = Counter(ln.split()[0] for ln in rows if ln.strip())
    if sum(c.values()) != nat:
        raise SystemExit(f"⛔ {scf_in}: ATOMIC_POSITIONS 줄 {sum(c.values())} ≠ nat {nat}")
    return c


def qe_kpts(scf_in):
    m = KPTS.search(Path(scf_in).read_text(errors="replace"))
    return " ".join(m.group(1).split()) if m else None


def qe_records(root):
    """<root>/<이름>/scf.in · scf.out → (후보 레코드, 기준상 레코드, 건너뛴 폴더).
    기준상은 조성 (Li · P · S 만) 으로 가른다. 출력이 없거나 에너지 줄이 없으면 오류 레코드 · 미완료면 converged False —
    둘 다 analyze() 가 ΔG 를 거절한다 (기준상이면 멈춘다). 이름 꼴이 아닌 폴더는 **목록에 남겨** 화면에 낸다."""
    cands, refs, skipped = [], [], []
    for d in sorted(Path(root).iterdir()):
        inp = d / "scf.in"
        if not d.is_dir() or not inp.exists():
            continue
        c = qe_comp(inp)
        is_ref = set(c) <= {"Li", "P", "S"}
        if not is_ref and not NAME.match(d.name):
            skipped.append(d.name)
            continue
        ok, why = qe_done(d / "scf.out", inp)
        e = qe_energy_eV(d / "scf.out")
        r = ({"name": d.name, "error": why or "에너지 줄 없음"} if e is None else
             {"name": d.name, "E_post_relax": e, "converged": ok, "why_not": why, "post_relax_xyz": str(inp),
              "K_POINTS": qe_kpts(inp)})
        (refs if is_ref else cands).append(r)
    return cands, refs, skipped


def dft_gates(s, uma=None, g3=G3_MARGIN, kprobe=None):
    """카드 G2 (UMA 부호) · G3 (여유 0.30) · G4 (k 탐침) 표지를 s 에 붙인다 — 판정 문장은 없다 (카드 §5 에서만)."""
    for dop, b in s["dopants"].items():
        if "dG_site_eV_per_dopant" not in b:
            continue
        dg = b["dG_site_eV_per_dopant"]
        mins = {k: m["ranked"][0] for k, m in b["models"].items()}
        g = {"G3_margin": g3, "G3_triggered": abs(dg) < g3, "min_cells": {k: v["name"] for k, v in mins.items()}}
        if uma is not None:
            u = uma.get("dopants", {}).get(dop, {}).get("dG_site_eV_per_dopant")
            g["G2_uma_dG"] = u
            g["G2_same_sign"] = None if u is None or u == 0 or dg == 0 else (u > 0) == (dg > 0)
        if kprobe is not None:
            n = b["closure"]["n_dopant"]
            ep, why = {}, []
            for kind, r in mins.items():
                d = Path(kprobe) / r["name"]
                base_in = Path(r["post_relax_xyz"])
                if not (d / "scf.in").exists():
                    why.append(f"{r['name']} 탐침 입력 없음")
                    continue
                if qe_comp(d / "scf.in") != qe_comp(base_in):
                    raise SystemExit(f"⛔ G4 탐침 {r['name']}: 단일점과 조성이 다르다")
                if qe_kpts(d / "scf.in") == qe_kpts(base_in):
                    raise SystemExit(f"⛔ G4 탐침 {r['name']}: k 가 단일점과 같다 ({qe_kpts(base_in)}) — 탐침이 아니다")
                ok, w = qe_done(d / "scf.out", d / "scf.in")
                e = qe_energy_eV(d / "scf.out")
                if not ok or e is None:
                    why.append(f"{r['name']} 탐침 미완료 ({w or '에너지 없음'})")
                    continue
                ep[kind] = (e, qe_kpts(d / "scf.in"))
            if why or set(ep) != {"MP", "MLi"}:
                g["G4"] = {"done": False, "why": why}
            else:
                dgk = dg + ((ep["MP"][0] - mins["MP"]["E_eV"]) - (ep["MLi"][0] - mins["MLi"]["E_eV"])) / n
                g["G4"] = {"done": True, "k_probe": ep["MP"][1], "dG_probe": dgk, "moved": abs(dgk - dg),
                           "limit": G4_MOVE, "triggered": abs(dgk - dg) > G4_MOVE}
        b["gates"] = g
    return s


def bundle_qe(s, root, dest):
    """DFT 모드 묶음 — 폴더마다 scf.in · scf.out + SHA256SUMS + 요약 (repo 에 올리기용 · 원자료 봉인)."""
    dest = Path(dest)
    sums = []
    for d in sorted(Path(root).iterdir()):
        if not (d / "scf.in").exists():
            continue
        (dest / d.name).mkdir(parents=True, exist_ok=True)
        for f in ("scf.in", "scf.out"):
            if (d / f).exists():
                shutil.copy2(d / f, dest / d.name / f)
                sums.append(f"{hashlib.sha256((d / f).read_bytes()).hexdigest()}  {d.name}/{f}")
    (dest / "site_dg_summary.json").write_text(json.dumps(s, indent=1, ensure_ascii=False, default=str))
    (dest / "SHA256SUMS").write_text("\n".join(sums) + "\n")
    return dest


def ref_energies(records, comp=_read_comp):
    """기준상 레코드 → {'Li2S': e/f.u., 'Li3PS4': e/f.u.} — 오류 · 미수렴 · 조성 이상 · 빠짐은 멈춘다."""
    e = {}
    for r in records:
        if "error" in r:
            raise SystemExit(f"⛔ 기준상 {r['name']} 오류: {r['error']}")
        if not r.get("converged"):
            raise SystemExit(f"⛔ 기준상 {r['name']} 이완 미수렴")
        c = comp(r["post_relax_xyz"])
        if set(c) == {"Li", "S"} and c["Li"] == 2 * c["S"]:
            f, n = "Li2S", c["S"]
        elif set(c) == {"Li", "P", "S"} and c["Li"] == 3 * c["P"] and c["S"] == 4 * c["P"]:
            f, n = "Li3PS4", c["P"]
        else:
            raise SystemExit(f"⛔ 기준상 {r['name']}: 조성 {formula(c)} 이 Li2S · Li3PS4 가 아니다")
        if f in e:
            raise SystemExit(f"⛔ 기준상 {f} 가 둘이다")
        e[f] = r["E_post_relax"] / n
    if set(e) != {"Li2S", "Li3PS4"}:
        raise SystemExit(f"⛔ 기준상 Li2S · Li3PS4 가 다 있어야 한다 (있는 것 {sorted(e)})")
    return e


def close_with_refs(cP, cLi):
    """cP − cLi = a·Li2S + b·Li3PS4 를 정확히 푼다. 안 닫히면 ValueError."""
    d = Counter(cP)
    d.subtract(cLi)
    other = {k: v for k, v in d.items() if k not in ("Li", "P", "S") and v}
    if other:
        raise ValueError(f"Li P S 밖의 원소 차 {other}")
    b = d["P"]
    a = d["S"] - 4 * b
    if 2 * a + 3 * b != d["Li"]:
        raise ValueError(f"Li 가 안 맞는다 (차 Li {d['Li']} · P {d['P']} · S {d['S']})")
    return a, b


def classify(records, comp=_read_comp):
    """레코드 → ({(도펀트, 종류): [레코드]}, 오류 이름들). 이름 · 조성이 안 맞으면 멈춘다."""
    groups, errors = {}, []
    for r in records:
        if "error" in r:
            errors.append(r["name"])
            continue
        m = NAME.match(r["name"])
        if not m:
            raise SystemExit(f"⛔ 이름 {r['name']} 이 [M]MP_ii · [M]MLi_ii · [M]host_ii 꼴이 아니다")
        c = comp(r["post_relax_xyz"])
        dop = sorted(set(c) - HOST_EL)
        if m["kind"] == "host":
            if dop:
                raise SystemExit(f"⛔ {r['name']}: host 이름인데 도펀트 {dop}")
            key = ("host", "host")
        else:
            if len(dop) != 1:
                raise SystemExit(f"⛔ {r['name']}: 도펀트 원소가 하나가 아니다 {dop}")
            if m["pre"] and m["pre"] != dop[0]:
                raise SystemExit(f"⛔ {r['name']}: 이름 앞머리 {m['pre']} 와 조성의 도펀트 {dop[0]} 가 다르다")
            key = (dop[0], m["kind"])
        groups.setdefault(key, []).append(dict(r, _comp=c))
    return groups, errors


def parse_thresholds(items):
    out = {}
    for it in items or []:
        k, _, v = it.rpartition("=")
        out[k or "*"] = float(v)
    return out


def analyze(anneal_records, ref_records, expect=None, allow_incomplete=False, top=3,
            thresholds=None, comp=_read_comp):
    """→ 요약 dict. 판정 문장은 없다 — 숫자 · 게이트 표지만."""
    eref = ref_energies(ref_records, comp)
    groups, errors = classify(anneal_records, comp)
    thr = thresholds or {}
    out = {"refs_eV_per_fu": eref,
           "reservoir_4Li2S_minus_Li3PS4_eV": 4 * eref["Li2S"] - eref["Li3PS4"],
           "error_records": errors, "dopants": {}, "hosts": []}
    for r in sorted(groups.get(("host", "host"), []), key=lambda r: r["E_post_relax"]):
        out["hosts"].append({"name": r["name"], "E_eV": r["E_post_relax"], "converged": r["converged"],
                             "formula": formula(r["_comp"]), "post_relax_xyz": r["post_relax_xyz"]})
    for dop in sorted({k[0] for k in groups if k[0] != "host"}):
        blk = {"models": {}, "refusals": []}
        if errors and not allow_incomplete:
            blk["refusals"].append(f"오류 레코드 {len(errors)} 개 ({' '.join(errors)}) — 다 있어야 계산한다")
        mins = {}
        for kind in ("MP", "MLi"):
            recs = groups.get((dop, kind), [])
            if not recs:
                blk["refusals"].append(f"{KIND_LABEL[kind]} 후보 0 개")
                continue
            forms = {formula(r["_comp"]) for r in recs}
            if len(forms) != 1:
                raise SystemExit(f"⛔ {dop} {KIND_LABEL[kind]}: 같은 모델 안 조성이 다르다 {sorted(forms)}")
            bad = [r["name"] for r in recs if not r.get("converged")]
            if bad and not allow_incomplete:
                blk["refusals"].append(f"{KIND_LABEL[kind]} 미수렴 {len(bad)} 개 ({' '.join(bad)})")
            n_err = sum(1 for nm in errors if (m := NAME.match(nm)) and m["kind"] == kind and m["pre"] in ("", dop))
            if expect is not None and len(recs) + n_err != expect:
                blk["refusals"].append(f"{KIND_LABEL[kind]} {len(recs) + n_err} 개 (--expect {expect})")
            # 미수렴은 --allow_incomplete 일 때만 뺀다 — 아니면 표에 남기고 (위에서) ΔG 를 거절한다
            use = sorted((r for r in recs if r.get("converged") or not allow_incomplete),
                         key=lambda r: r["E_post_relax"])
            if not use:
                blk["refusals"].append(f"{KIND_LABEL[kind]} 쓸 후보 0 개")
                continue
            e0 = use[0]["E_post_relax"]
            blk["models"][kind] = {
                "formula": forms.pop(), "n": len(recs), "n_converged": len(recs) - len(bad),
                "excluded_unconverged": bad if allow_incomplete else [],
                "gap_min_second_eV": (use[1]["E_post_relax"] - e0) if len(use) > 1 else None,
                "top": [r["name"] for r in use[:top]],
                "ranked": [{"name": r["name"], "E_eV": r["E_post_relax"], "dE_from_min_eV": r["E_post_relax"] - e0,
                            "converged": r["converged"], "n_relax_steps": r.get("n_relax_steps"),
                            "post_relax_xyz": r["post_relax_xyz"]} for r in use]}
            mins[kind] = use[0]
        if set(mins) == {"MP", "MLi"}:
            cP, cL = mins["MP"]["_comp"], mins["MLi"]["_comp"]
            if cP[dop] != cL[dop]:
                raise SystemExit(f"⛔ {dop}: 두 모델의 도펀트 수가 다르다 ({cP[dop]} · {cL[dop]})")
            try:
                a, b = close_with_refs(cP, cL)
            except ValueError as ex:
                raise SystemExit(f"⛔ {dop}: 조성차가 Li₂S/Li₃PS₄ 로 안 닫힌다 — {ex}")
            n = cP[dop]
            blk["closure"] = {"a_Li2S": a, "b_Li3PS4": b, "n_dopant": n}
            if not blk["refusals"]:
                dg = (mins["MP"]["E_post_relax"] - mins["MLi"]["E_post_relax"]
                      - (a * eref["Li2S"] + b * eref["Li3PS4"])) / n
                blk["dG_site_eV_per_dopant"] = dg
                ts = [thr[k] for k in (dop, "*") if k in thr]
                blk["polymorph_recheck"] = [{"threshold": t, "distance": abs(abs(dg) - t),
                                             "triggered": abs(abs(dg) - t) <= POLY_MARGIN} for t in ts]
        out["dopants"][dop] = blk
    return out


def report(s):
    print(f"== 기준상 e(Li₂S) {s['refs_eV_per_fu']['Li2S']:.5f} · e(Li₃PS₄) {s['refs_eV_per_fu']['Li3PS4']:.5f} eV/f.u. "
          f"· 저장소 항 4·e(Li₂S) − e(Li₃PS₄) = {s['reservoir_4Li2S_minus_Li3PS4_eV']:.5f} eV")
    if s["error_records"]:
        print(f"   ⛔ 오류 레코드: {' '.join(s['error_records'])}")
    for dop, b in s["dopants"].items():
        cl = b.get("closure")
        print(f"== {dop}" + (f" (n {cl['n_dopant']} · 조성차 = {cl['a_Li2S']} Li₂S {cl['b_Li3PS4']:+d} Li₃PS₄ ✓)" if cl else ""))
        for kind, m in b["models"].items():
            gap = "—" if m["gap_min_second_eV"] is None else f"{m['gap_min_second_eV']:+.4f}"
            print(f"   {KIND_LABEL[kind]:<5} {m['formula']} · {m['n']} 개 (수렴 {m['n_converged']}) · "
                  f"최저 {m['ranked'][0]['name']} · 둘째와 차 {gap} eV · 상위 {' '.join(m['top'])}")
            if m["excluded_unconverged"]:
                print(f"         ⚠ 미수렴 빼고 계산: {' '.join(m['excluded_unconverged'])}")
            print("         " + " · ".join(f"{x['name']} {x['dE_from_min_eV']:+.3f}" for x in m["ranked"]))
        for why in b["refusals"]:
            print(f"   ⛔ ΔG 안 냄 — {why}")
        if "dG_site_eV_per_dopant" in b:
            meth = s.get("method", "UMA")
            print(f"   ΔG_site({meth}) = {b['dG_site_eV_per_dopant']:+.3f} eV/{dop}  (> 0 ⇒ P 자리 불리 · "
                  + ("UMA 내부 · " if meth == "UMA" else "DFT 단일점 · ") + "Li₃PS₄/Li₂S 교환 기준)")
            for p in b["polymorph_recheck"]:
                print(f"   문턱 {p['threshold']:.2f} 과의 거리 {p['distance']:.3f} eV → 다형 재확인 "
                      + ("**발동** (Li₃PS₄ 다른 다형 둘도 이완)" if p["triggered"] else "안 함"))
            g = b.get("gates")
            if g:
                mc = g["min_cells"]
                if "G2_uma_dG" in g:
                    u = g["G2_uma_dG"]
                    print(f"   G2 UMA 부호 {'—' if u is None else f'{u:+.3f}'} → "
                          + {True: "같은 부호", False: "⚠ **갈림** — 두 방법이 갈림 · UMA x-추세를 쓰지 않는다",
                             None: "비교 못 함 (값 없음 · 0)"}[g["G2_same_sign"]])
                print(f"   G3 |ΔG| {abs(b['dG_site_eV_per_dopant']):.3f} "
                      + (f"< {g['G3_margin']:.2f} → **발동**: 두 최저 셀 ({mc.get('MP')} · {mc.get('MLi')}) 을 고정셀 + EOS 로 이완한 뒤에만 부호"
                         if g["G3_triggered"] else f"≥ {g['G3_margin']:.2f} → 단일점 부호를 쓸 수 있다 (G4 · G7 은 따로)"))
                g4 = g.get("G4")
                if g4 is None:
                    print(f"   G4 k 탐침 대상 {mc.get('MP')} · {mc.get('MLi')} (k 한 단계 올림) — 출력이 오면 --kprobe 로 다시 판독")
                elif not g4["done"]:
                    print(f"   G4 k 탐침 미완료 — {' · '.join(g4['why'])}")
                else:
                    print(f"   G4 k {g4['k_probe']} 에서 ΔG {g4['dG_probe']:+.3f} · 움직임 {g4['moved']:.3f} eV → "
                          + (f"> {g4['limit']:.2f} **발동** (전 점을 그 k 로 다시 · 안 할 거면 사용자 명시 결정)"
                             if g4["triggered"] else f"≤ {g4['limit']:.2f} 통과"))
    for h in s["hosts"]:
        print(f"   host {h['name']} {h['formula']} · 수렴 {h['converged']}")


def bundle(s, inputs, dest):
    """결과 json · 요약 · 모든 post_relax.xyz 를 한 폴더로 (repo 에 올리기용)."""
    dest = Path(dest)
    (dest / "structures").mkdir(parents=True, exist_ok=True)
    for p in inputs:
        p = Path(p)
        shutil.copy2(p, dest / f"{p.parent.name}.anneal_results.json")
        for r in json.loads(p.read_text())["results"]:
            if "post_relax_xyz" in r and Path(r["post_relax_xyz"]).exists():
                shutil.copy2(r["post_relax_xyz"], dest / "structures" / f"{r['name']}.xyz")
    (dest / "site_dg_summary.json").write_text(json.dumps(s, indent=1, ensure_ascii=False, default=str))
    return dest


def _selftest():
    import tempfile
    import numpy as np
    from ase import Atoms
    from ase.io import write
    ok = []

    def chk(c, m):
        ok.append(bool(c))
        print(("  ✓ " if c else "  ✗ ") + m)

    def expect_exit(fn, m):
        try:
            fn()
        except SystemExit as ex:
            chk(str(ex).startswith("⛔"), m + f" → {str(ex)[:70]}")
        else:
            chk(False, m + " → 멈추지 않았다")

    tmp = Path(tempfile.mkdtemp())
    rng = np.random.default_rng(0)

    def xyz(name, form):
        sym = [e for e, k in re.findall(r"([A-Z][a-z]?)(\d+)", form) for _ in range(int(k))]
        p = tmp / f"{name}.xyz"
        write(p, Atoms(sym, positions=rng.random((len(sym), 3)) * 20, cell=[20] * 3, pbc=True))
        return str(p)

    def rec(name, form, E, conv=True):
        return {"name": name, "E_post_relax": E, "converged": conv, "n_relax_steps": 10,
                "post_relax_xyz": xyz(name, form)}

    P, L = "Cl8Li31Nd2O3P3S19", "Cl8Li21Nd2O3P5S19"
    refs = [rec("li2s", "Li2S1", -12.0), rec("li3ps4", "Li12P4S16", -140.0)]       # e = −12 · −35 → 저장소 −13
    base = [rec("MP_00", P, -400.0), rec("MP_01", P, -399.9), rec("MLi_00", L, -374.5), rec("MLi_01", L, -374.0),
            rec("host_00", "Cl8Li27P5S20", -300.0)]
    s = analyze(base, refs, expect=2, thresholds={"*": 0.20})
    b = s["dopants"]["Nd"]
    chk(abs(s["reservoir_4Li2S_minus_Li3PS4_eV"] + 13.0) < 1e-12, "저장소 항 4(−12) − (−35) = −13")
    chk(abs(b.get("dG_site_eV_per_dopant", 9) - 0.25) < 1e-12, "ΔG = [(−400 + 374.5) − 2·(−13)] / 2 = +0.25")
    chk(b["closure"] == {"a_Li2S": 8, "b_Li3PS4": -2, "n_dopant": 2}, "조성차 = 8 Li₂S − 2 Li₃PS₄ · n 2")
    chk(abs(b["models"]["MP"]["gap_min_second_eV"] - 0.1) < 1e-9 and b["models"]["MP"]["top"][0] == "MP_00", "최저 · 둘째 차")
    chk(b["polymorph_recheck"][0]["triggered"], "|0.25 − 0.20| ≤ 0.11 → 다형 재확인 발동")
    s2 = analyze(base, refs, thresholds={"Nd": 0.50, "B": 0.0})
    chk(not s2["dopants"]["Nd"]["polymorph_recheck"][0]["triggered"], "도펀트별 문턱 0.50 → 거리 0.25 · 안 함")
    chk(len(s["hosts"]) == 1, "host 는 ΔG 밖 목록")
    # 음성 — 막아야 하는 것
    s3 = analyze(base[:1] + [rec("MP_02", P, -401.0, conv=False)] + base[1:], refs)
    chk("dG_site_eV_per_dopant" not in s3["dopants"]["Nd"] and s3["dopants"]["Nd"]["refusals"], "미수렴 있으면 ΔG 안 냄")
    s4 = analyze(base[:1] + [rec("MP_02", P, -401.0, conv=False)] + base[1:], refs, allow_incomplete=True)
    chk(abs(s4["dopants"]["Nd"]["dG_site_eV_per_dopant"] - 0.25) < 1e-12
        and s4["dopants"]["Nd"]["models"]["MP"]["excluded_unconverged"] == ["MP_02"],
        "--allow_incomplete: 미수렴 (더 낮아도) 빼고 계산 · 뺀 이름 기록")
    s5 = analyze(base + [{"name": "MLi_02", "error": "CUDA OOM"}], refs)
    chk("dG_site_eV_per_dopant" not in s5["dopants"]["Nd"], "오류 레코드 있으면 ΔG 안 냄")
    s6 = analyze(base, refs, expect=3)
    chk("dG_site_eV_per_dopant" not in s6["dopants"]["Nd"], "--expect 3 인데 2 개 → ΔG 안 냄")
    expect_exit(lambda: analyze(base + [rec("MP_03", L, -1.0)], refs), "같은 모델 안 조성 다름")
    expect_exit(lambda: analyze([rec("MP_00", "Cl8Li31Nd2O4P3S18", -1.0)] + base[2:], refs), "조성차가 안 닫힘 (O 차)")
    expect_exit(lambda: analyze(base, refs[:1]), "기준상 Li₃PS₄ 빠짐")
    expect_exit(lambda: analyze(base, [refs[0], rec("li3ps4", "Li12P4S16", -140.0, conv=False)]), "기준상 미수렴")
    expect_exit(lambda: analyze([rec("BMP_00", P, -1.0)] + base[1:], refs), "이름 앞머리 B 인데 조성은 Nd")
    expect_exit(lambda: analyze([rec("MP_00", "Cl8Li31Nd2O3P3S19Y1", -1.0)] + base[1:], refs), "도펀트 원소 둘")

    # ══ DFT 모드 (2026-10-15) ══
    import subprocess
    # ① 완료 판정 = 러너 _fc_ok — 러너 파일에서 함수를 그대로 떼어 bash 로 부르고 같은 fixture 로 대조한다
    runner = Path(__file__).resolve().parents[3] / "tools/doping/run_force_check_scf.sh"
    src = runner.read_text()
    body = src[src.index("_fc_ok() {"):]
    (tmp / "fc_ok.sh").write_text(body[:body.index("\n}\n") + 3])

    def bash_ok(d):
        r = subprocess.run(["bash", "-c", f'. "{tmp / "fc_ok.sh"}"; _fc_ok "{d}/scf.out"'], capture_output=True)
        return r.returncode == 0

    B1 = ("!    total energy              =    -100.00000000 Ry\n     convergence has been achieved in  10 iterations\n"
          "     Forces acting on atoms (cartesian axes, Ry/au):\n     total   stress  (Ry/bohr**3)   (kbar)     P=  -0.10\n")
    FIN = "bfgs converged in 12 scf cycles and 5 bfgs steps\nBegin final coordinates\nEnd final coordinates\n"
    VC, RX, SC = "calculation = 'vc-relax'\ntstress = .true.\n", "calculation = 'relax'\ntstress = .true.\n", "calculation = 'scf'\ntstress = .true.\n"
    cases = {"scf 완료": (SC, B1 + "JOB DONE.\n", True),
             "scf 응력 없음": (SC, B1.replace("total   stress", "x") + "JOB DONE.\n", False),
             "scf JOB DONE 없음": (SC, B1, False),
             "vc-relax 수렴 + 최종 scf": (VC, B1 + FIN + B1 + "JOB DONE.\n", True),
             "vc-relax 최종 scf 없음": (VC, B1 + FIN + "JOB DONE.\n", False),
             "vc-relax nstep 소진": (VC, B1 + "The maximum number of steps has been reached.\nEnd final coordinates\n" + B1 + "JOB DONE.\n", False),
             "relax 수렴": (RX, B1 + FIN + "JOB DONE.\n", True),
             "relax 수렴 선언 없음": (RX, B1 + "JOB DONE.\n", False),
             "대문자 VC-RELAX 키 · 수렴 없음": ("CALCULATION = 'VC-RELAX'\nTSTRESS = .TRUE.\n", B1 + "JOB DONE.\n", False)}
    agree = []
    for i, (nm, (inp, out, want)) in enumerate(cases.items()):
        d = tmp / "fc" / f"c{i}"
        d.mkdir(parents=True)
        (d / "scf.in").write_text(inp)
        (d / "scf.out").write_text(out)
        py = qe_done(d / "scf.out", d / "scf.in")[0]
        sh = bash_ok(d)
        agree.append(py == sh == want)
        if not py == sh == want:
            print(f"     ✗ {nm}: 이 도구 {py} · 러너 {sh} · 기대 {want}")
    chk(all(agree), f"완료 판정 — 이 도구 = 러너 _fc_ok = 기대 ({sum(agree)}/{len(agree)} fixture · 양성 3 · 음성 6)")

    # ② 끝에서 끝까지 — 가짜 QE 나무 (후보 6 + 기준상 2) · 손계산 ΔG = +0.25
    def qdir(root, name, form, calc, e_eV, done=True, final=True, forces=True, kp="2 2 1"):
        d = Path(root) / name
        d.mkdir(parents=True, exist_ok=True)
        sym = [e for e, k in re.findall(r"([A-Z][a-z]?)(\d+)", form) for _ in range(int(k))]
        pos = "".join(f"  {e}  0.1 0.2 0.3\n" for e in sym)
        (d / "scf.in").write_text(f"&CONTROL\n    calculation = '{calc}'\n    tstress     = .true.\n/\n&SYSTEM\n"
                                  f"    nat         = {len(sym)}\n/\nATOMIC_POSITIONS crystal\n{pos}K_POINTS automatic\n  {kp} 0 0 0\n")
        one = (f"!    total energy              = {e_eV / RY_EV:17.8f} Ry\n     convergence has been achieved in  9 iterations\n"
               + ("     Forces acting on atoms (cartesian axes, Ry/au):\n" if forces else "")
               + "     total   stress  (Ry/bohr**3)   (kbar)     P=  0.1\n")
        txt = one + (FIN + (one if final else "") if calc == "vc-relax" else "")
        (d / "scf.out").write_text(txt + ("JOB DONE.\n" if done else ""))

    def tree(tag, **kw):
        root = tmp / f"qe_{tag}"
        E = {"MP_07": -400.0, "MP_09": -399.7, "MP_00": -399.5, "MLi_03": -374.5, "MLi_04": -374.4, "MLi_05": -374.2}
        for nm, e in E.items():
            qdir(root, nm, P if nm.startswith("MP") else L, "scf", e, **kw.get(nm, {}))
        qdir(root, "Li2S", "Li2S1", "vc-relax", -12.0, **kw.get("Li2S", {}))
        qdir(root, "Li3PS4", "Li12P4S16", "vc-relax", -140.0, **kw.get("Li3PS4", {}))
        return root

    def run_qe(root, uma=0.319, kprobe=None):
        c, r, sk = qe_records(root)
        s = analyze(c, r, expect=3, thresholds={"Nd": 0.30}, comp=qe_comp)
        s["method"] = "DFT"
        return dft_gates(s, {"dopants": {"Nd": {"dG_site_eV_per_dopant": uma}}}, kprobe=kprobe), sk

    s7, sk7 = run_qe(tree("ok"))
    b7 = s7["dopants"]["Nd"]
    chk(abs(b7.get("dG_site_eV_per_dopant", 9) - 0.25) < 1e-5, f"DFT ΔG = [(−400 + 374.5) − 2·(−13)] / 2 = +0.25 (얻음 {b7.get('dG_site_eV_per_dopant', float('nan')):+.6f})")
    chk(b7["gates"]["min_cells"] == {"MP": "MP_07", "MLi": "MLi_03"} and not sk7, "모델별 DFT 최저 = MP_07 · MLi_03 · 건너뛴 폴더 없음")
    chk(b7["gates"]["G2_same_sign"] is True, "G2: UMA +0.319 와 같은 부호")
    chk(b7["gates"]["G3_triggered"] is True, "G3: |0.25| < 0.30 → 발동 (고정셀 + EOS 뒤에만 부호)")
    chk(b7["polymorph_recheck"][0]["triggered"], "G7: |0.25 − 0.30| ≤ 0.11 → 다형 재확인 발동")
    s8, _ = run_qe(tree("ok8"), uma=-0.2)
    chk(s8["dopants"]["Nd"]["gates"]["G2_same_sign"] is False, "[음성] G2: UMA −0.2 → 갈림")
    s9, _ = run_qe(tree("noforce", MLi_05={"forces": False}))
    chk("dG_site_eV_per_dopant" not in s9["dopants"]["Nd"], "[음성] 후보 하나 미완료 (힘 없음) → ΔG 안 냄")
    tr = tree("notrun")
    (tr / "MP_00" / "scf.out").unlink()
    s10, _ = run_qe(tr)
    chk("dG_site_eV_per_dopant" not in s10["dopants"]["Nd"], "[음성] 아직 안 돈 후보 (scf.out 없음) → ΔG 안 냄")
    expect_exit(lambda: run_qe(tree("nofinal", Li3PS4={"final": False})), "[음성] 기준상 vc-relax 최종 scf 없음 → 멈춤")
    tr = tree("extra")
    qdir(tr, "MP_07_k331", P, "scf", -400.0)
    _, sk11 = run_qe(tr)
    chk(sk11 == ["MP_07_k331"], "이름 꼴 아닌 폴더는 계산에서 빼되 목록으로 낸다")
    # ③ G4 k 탐침
    kp = tmp / "kp_ok"
    qdir(kp, "MP_07", P, "scf", -400.06, kp="3 3 1")
    qdir(kp, "MLi_03", L, "scf", -374.5, kp="3 3 1")
    g4 = run_qe(tree("k1"), kprobe=kp)[0]["dopants"]["Nd"]["gates"]["G4"]
    chk(g4["done"] and abs(g4["dG_probe"] - 0.22) < 1e-5 and not g4["triggered"], f"G4: ΔG 0.25 → 0.22 · 움직임 0.03 ≤ 0.05 통과")
    kp2 = tmp / "kp_move"
    qdir(kp2, "MP_07", P, "scf", -400.2, kp="3 3 1")
    qdir(kp2, "MLi_03", L, "scf", -374.5, kp="3 3 1")
    chk(run_qe(tree("k2"), kprobe=kp2)[0]["dopants"]["Nd"]["gates"]["G4"]["triggered"], "[음성] G4: 움직임 0.10 > 0.05 → 발동")
    kp3 = tmp / "kp_same"
    qdir(kp3, "MP_07", P, "scf", -400.0)
    qdir(kp3, "MLi_03", L, "scf", -374.5)
    expect_exit(lambda: run_qe(tree("k3"), kprobe=kp3), "[음성] G4: 탐침 k 가 단일점과 같으면 멈춤")
    kp4 = tmp / "kp_half"
    qdir(kp4, "MP_07", P, "scf", -400.06, kp="3 3 1")
    chk(not run_qe(tree("k4"), kprobe=kp4)[0]["dopants"]["Nd"]["gates"]["G4"]["done"], "[음성] G4: 탐침 하나 빠짐 → 미완료로 표시 (판정 안 함)")
    print(f"selftest: {sum(ok)}/{len(ok)}")
    return 0 if all(ok) else 1


def main():
    if "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--anneal", nargs="+")
    ap.add_argument("--refs")
    ap.add_argument("--qe", help="DFT 모드 — <폴더>/<이름>/scf.in · scf.out (run_force_check_scf.sh 꼴) · 기준상은 조성으로 가른다")
    ap.add_argument("--compare_uma", help="DFT 모드 G2 — UMA 판독 요약 (site_dg_rietveld.json)")
    ap.add_argument("--g3", type=float, default=G3_MARGIN, help="DFT 모드 G3 여유 (카드 0.30 eV/도펀트)")
    ap.add_argument("--kprobe", help="DFT 모드 G4 — k 한 단계 올린 탐침 폴더 (<폴더>/<최저 셀 이름>/scf.in · scf.out)")
    ap.add_argument("--expect", type=int)
    ap.add_argument("--allow_incomplete", action="store_true")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--thresholds", nargs="*", default=[])
    ap.add_argument("--out")
    ap.add_argument("--bundle")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.qe:
        cands, refs, skipped = qe_records(a.qe)
        s = analyze(cands, refs, a.expect, a.allow_incomplete, a.top, parse_thresholds(a.thresholds), comp=qe_comp)
        s["method"] = "DFT"
        s["skipped_dirs"] = skipped
        dft_gates(s, json.loads(Path(a.compare_uma).read_text()) if a.compare_uma else None, a.g3, a.kprobe)
        s["inputs"] = {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted(Path(a.qe).glob("*/scf.*")) if p.suffix in (".in", ".out")}
        if a.compare_uma:
            s["inputs"][a.compare_uma] = hashlib.sha256(Path(a.compare_uma).read_bytes()).hexdigest()
        s["args"] = {"qe": a.qe, "expect": a.expect, "allow_incomplete": a.allow_incomplete, "top": a.top,
                     "thresholds": a.thresholds, "g3": a.g3, "kprobe": a.kprobe, "compare_uma": a.compare_uma}
        if a.out:
            Path(a.out).write_text(json.dumps(s, indent=1, ensure_ascii=False, default=str))
        dest = bundle_qe(s, a.qe, a.bundle) if a.bundle else None
        if skipped:
            print(f"   ⚠ 이름 꼴이 아니라 건너뛴 폴더: {' '.join(skipped)}")
    else:
        if not (a.anneal and a.refs):
            ap.error("--anneal 과 --refs 가 필요하다 (DFT 모드면 --qe)")
        recs = [r for p in a.anneal for r in json.loads(Path(p).read_text())["results"]]
        refs = json.loads(Path(a.refs).read_text())["results"]
        s = analyze(recs, refs, a.expect, a.allow_incomplete, a.top, parse_thresholds(a.thresholds))
        s["inputs"] = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in a.anneal + [a.refs]}
        s["args"] = {"expect": a.expect, "allow_incomplete": a.allow_incomplete, "top": a.top, "thresholds": a.thresholds}
        # 파일을 **먼저** 쓴다 — 화면 출력이 `| head` 등으로 끊겨도 (BrokenPipe) 요약 · 묶음은 남게 (로컬 시험에서 묶음이 통째로 빠졌다)
        if a.out:
            Path(a.out).write_text(json.dumps(s, indent=1, ensure_ascii=False, default=str))
        dest = bundle(s, a.anneal + [a.refs], a.bundle) if a.bundle else None
    report(s)
    if a.out:
        print(f"   요약 → {a.out}")
    if dest:
        print(f"   묶음 → {dest}")
    refused = [d for d, b in s["dopants"].items() if "dG_site_eV_per_dopant" not in b]
    if refused or not s["dopants"]:
        print(f"   ⛔ ΔG 를 못 낸 도펀트: {' '.join(refused) or '(후보 없음)'} — 종료 3")
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
