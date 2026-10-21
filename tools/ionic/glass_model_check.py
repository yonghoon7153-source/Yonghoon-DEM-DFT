#!/usr/bin/env python3
"""glass_model_check.py — li2s 소셀 유리 **모델 검증 카드** 판독 (BVSE 정적 지도 · A 5 대 B 5).

카드: db/properties/lpscl_smallcell_glass_model_check_estimand_2026_10_19.json
      (숫자는 카드의 `기계_판독_값` 에서만 읽는다 — 이 파일은 숫자를 자체 보관하지 않는다)

  python3 tools/ionic/glass_model_check.py --bvse_control              # 대조 잡: 저장된 modelc 지도로 BVSE 정본 재현
  python3 tools/ionic/glass_model_check.py --bvse --out <json>         # 열 구조 BVSE → β1/β2 · onset 판정 · 문장
  python3 tools/ionic/glass_model_check.py --selftest

순서 (카드 §2): `--bvse` 는 **대조 잡을 먼저 돌리고** 어긋나면 열 구조를 읽지 않는다 (회신 CX 상시 절차).

⛔ 이 도구가 못 하는 것
  · BVSE 는 정적 기하 지표다 — 확산계수 · Ea · σ · 수송 순위를 내지 않는다 (카드 §1a ⛔).
    BV 지도의 단위는 val² 이고 eV 가 아니다.
  · 구조를 고르지 않는다 — 카드가 정한 열 구조뿐이고, A 는 값 지문 (최단 P–S · PS₄ 개수 · ρ) ·
    B 는 sha16 이 안 맞으면 **멈춘다** (다른 파일을 조용히 읽지 않는다).
  · 비직교 · 비입방 셀은 읽지 않는다 — bvse_map 의 최소상은 분율 반올림이라 기울어진 셀에서 틀린다
    (2026-10-19 Nd ELF 표본 도구 선례).
  · 통계는 '완전 분리' 하나뿐이다 (n ≤ 5 · 정확 양측 순위합 p = 2 / C(n_A + n_B, n_A)).
    분리가 아니면 '구분되지 않았다' 까지고, '같다' 라고 쓰지 않는다 (채널 부피).
  · B 의 담금질 기계별 두 무리 (kgy 1·2 · gabia 3·4·5) 와 밀도 효과는 **기록만** 한다 — 판정에 안 쓴다.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import pathlib
import re
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
CARD = REPO / "db" / "properties" / "lpscl_smallcell_glass_model_check_estimand_2026_10_19.json"
A_ROOT = REPO / "db" / "raw" / "lpscl_glass_model_check_2026_10_19" / "structures"
B_ROOT = REPO / "db" / "raw" / "lpscl_glass_control_li3ps4_2026_10_05"
A_MACHINE = {1: "kgy", 2: "kgy", 3: "gabia", 4: "gabia", 5: "gabia"}   # 회수 경로 (담금질 기계) — 카드 §1b 구조
AMU_G = 1.66053906660                                                  # g/mol·Å³ → g/cm³ 환산 (질량 amu · 부피 Å³)


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BVS = _load_module("bvse_standalone", REPO / "tools" / "comp1_v3" / "bvse_standalone.py")
BVO = _load_module("bvse_onset_canonical", REPO / "tools" / "comp1_v3" / "bvse_onset_canonical.py")


# ───────────────────────── 카드 ─────────────────────────
def load_card(path=CARD) -> dict:
    """카드의 `기계_판독_값` — 없으면 KeyError 로 죽는다 (숫자를 지어내지 않는다)."""
    d = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    return d["기계_판독_값"]


# ───────────────────────── 구조 · 지문 ─────────────────────────
def mic_dist(A, B, cell):
    """직교 셀 최소상 거리 (n,m) — 호출부가 직교를 먼저 확인한다."""
    ci = np.linalg.inv(cell)
    d = A[:, None, :] - B[None, :, :]
    f = d @ ci
    f -= np.round(f)
    return np.linalg.norm(f @ cell, axis=2)


def check_cubic(cell, tol=1e-6):
    c = np.asarray(cell, float)
    off = float(np.abs(c - np.diag(np.diag(c))).max())
    L = np.diag(c)
    if off > tol or float(np.ptp(L)) > tol:
        raise ValueError(f"⛔ 직교 입방 셀이 아니다 (비대각 {off:.2e} · 변 {L}) — BVSE 최소상 가정이 깨진다")
    return float(L[0])


def fingerprint(path) -> dict:
    """값 지문 (v2 카드 §1b 규칙): 최단 P–S · PS₄ 개수 (P–S ≤ 2.6 Å 넷) · ρ · sha16 · 조성."""
    from ase.io import read
    at = read(str(path))
    L = check_cubic(at.cell.array)
    sym = np.array(at.get_chemical_symbols())
    pos = at.get_positions()
    D = mic_dist(pos[sym == "P"], pos[sym == "S"], at.cell.array)
    return {"n": len(at), "L_A": L,
            "comp": {k: int((sym == k).sum()) for k in ("Li", "P", "S", "Cl")},
            "min_PS_A": float(D.min()),
            "n_PS4": int(((D <= 2.6).sum(axis=1) == 4).sum()),
            "rho": float(at.get_masses().sum() * AMU_G / at.get_volume()),
            "sha16": hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()[:16]}


def structure_table(card) -> list[dict]:
    """카드의 열 구조 — A 는 값 지문 · B 는 sha16 으로 가린다. 하나라도 어긋나면 ValueError."""
    rows = []
    fp, tol = card["a_fingerprint"], card["a_fingerprint_tol"]
    for s in sorted(int(k) for k in fp):
        p = A_ROOT / A_MACHINE[s] / "A" / f"seed{s}" / "final.xyz"
        f = fingerprint(p)
        want = fp[str(s)]
        if not (abs(f["min_PS_A"] - want[0]) <= tol["min_PS_A"] and f["n_PS4"] == int(want[1])
                and abs(f["rho"] - want[2]) <= tol["rho"]):
            raise ValueError(f"⛔ A seed{s} 값 지문 불일치 — 얻음 {f['min_PS_A']:.4f}/{f['n_PS4']}/{f['rho']:.4f} · 카드 {want}")
        rows.append({"system": "A", "seed": s, "machine": A_MACHINE[s], "path": str(p.relative_to(REPO)), **f})
    for k, (mach, sha16) in sorted(card["b_structures"].items(), key=lambda kv: int(kv[0])):
        s = int(k)
        p = B_ROOT / mach / "B" / f"seed{s}" / "final.xyz"
        f = fingerprint(p)
        if f["sha16"] != sha16:
            raise ValueError(f"⛔ B seed{s} sha16 불일치 — 얻음 {f['sha16']} · 카드 {sha16}")
        rows.append({"system": "B", "seed": s, "machine": mach, "path": str(p.relative_to(REPO)), **f})
    return rows


# ───────────────────────── BVSE ─────────────────────────
def bvse_one(path, grid) -> dict:
    """한 구조의 BVSE 지도 → 정본 판독 (고정 격자 onset · 채널 %) · Li 자리 BVS."""
    A, frac, sym = BVS.parse_structure(str(path))
    check_cubic(A)
    bv, ns, L = BVS.bvse_map(A, frac, sym, grid)
    on = BVO.onsets(bv)
    iso = BVO.iso_fractions(bv)
    vals = [v for v in on.values() if v is not None]
    lis = BVS.li_site_bvs(A, frac, sym)
    return {"grid": [int(x) for x in ns], "voxel_A": round(float(L.min() / grid), 4),
            "onset": on, "onset_min": (min(vals) if vals else None), "iso_pct": iso,
            "li_bvs_mean": round(float(np.mean(lis)), 4), "li_bvs_std": round(float(np.std(lis)), 4)}


def bvse_control(card) -> dict:
    """대조 잡 — 저장된 modelc 지도로 정본 onset · 채널 % 를 **글자 그대로** 재현해야 한다."""
    c = card["bvse_control"]
    bv = np.load(REPO / c["map"])
    on, iso = BVO.onsets(bv), BVO.iso_fractions(bv)
    ok_on = all(on.get(k) == v for k, v in c["onset"].items())
    ok_iso = all(iso.get(k) == v for k, v in c["iso_pct"].items())
    return {"ok": bool(ok_on and ok_iso), "onset": on, "iso_pct": iso,
            "want_onset": c["onset"], "want_iso_pct": c["iso_pct"]}


def exact_p_separation(n_a, n_b) -> float:
    """완전 분리의 정확 양측 순위합 p = 2 / C(n_a + n_b, n_a)."""
    return 2.0 / math.comb(n_a + n_b, n_a)


def separation(a, b):
    """'A>B' · 'A<B' (모든 A 가 모든 B 보다 크다/작다) · 아니면 None. 같은 값이 섞이면 분리가 아니다."""
    a, b = list(a), list(b)
    if min(a) > max(b):
        return "A>B"
    if max(a) < min(b):
        return "A<B"
    return None


def median(v):
    return float(np.median(np.asarray(v, float)))


def bvse_compare(rows, card) -> dict:
    """카드 §4 BVSE_비교 — 채널 % (iso 주) 는 완전 분리 + 계마다 ≥ 최소 구조 · onset 은 + 칸 수."""
    iso_key = str(card["bvse_iso_main"])
    nmin = int(card["bvse_min_per_system"])
    step = float(card["bvse_onset_step"])
    k_diff, k_same = int(card["bvse_onset_differ_steps"]), int(card["bvse_onset_same_steps"])
    a = [r for r in rows if r["system"] == "A"]
    b = [r for r in rows if r["system"] == "B"]
    ca = [r["bvse"]["iso_pct"][iso_key] for r in a]
    cb = [r["bvse"]["iso_pct"][iso_key] for r in b]
    out = {"iso_main": iso_key, "n_A": len(a), "n_B": len(b),
           "channel_A": ca, "channel_B": cb,
           "channel_median_A": median(ca) if ca else None, "channel_median_B": median(cb) if cb else None}
    if len(a) < nmin or len(b) < nmin:
        out["channel_branch"] = "β2"
        out["channel_why"] = f"구조 부족 (A {len(a)} · B {len(b)} < {nmin}) — 분리 판정을 하지 않는다"
        sep = None
    else:
        sep = separation(ca, cb)
        out["channel_branch"] = "β1" if sep else "β2"
        out["channel_separation"] = sep
        out["exact_p_two_sided"] = exact_p_separation(len(a), len(b)) if sep else None
    oa = [r["bvse"]["onset_min"] for r in a]
    ob = [r["bvse"]["onset_min"] for r in b]
    out["onset_min_A"], out["onset_min_B"] = oa, ob
    if any(v is None for v in oa + ob):
        out["onset_verdict"] = "보류"
        out["onset_why"] = "침투 없음 (3.0 val² 까지) 인 구조가 있다 — 칸 수를 못 센다"
    else:
        dm = median(oa) - median(ob)
        k = abs(dm) / step
        out["onset_median_diff_val2"] = round(dm, 4)
        out["onset_median_diff_steps"] = round(k, 2)
        osep = separation(oa, ob) if (len(a) >= nmin and len(b) >= nmin) else None
        if k <= k_same + 1e-9:
            out["onset_verdict"] = "같다"
        elif k >= k_diff - 1e-9 and osep:
            out["onset_verdict"] = "낮다" if dm < 0 else "높다"     # A 가 B 보다
            out["onset_separation"] = osep
        else:
            out["onset_verdict"] = "보류"
    # 기록 (판정 아님): B 의 담금질 기계별 두 무리 · 밀도
    out["B_machine_groups"] = {m: [r["bvse"]["iso_pct"][iso_key] for r in b if r["machine"] == m]
                               for m in sorted({r["machine"] for r in b})}
    out["rho_vs_channel"] = [[r["system"], r["seed"], round(r["rho"], 4), r["bvse"]["iso_pct"][iso_key]] for r in rows]
    out["sentence"] = bvse_sentence(out, card)
    return out


def bvse_sentence(o, card) -> str:
    """카드 §1a β1 · β2 · onset 문장 — 갈래에서 고른다 (사람이 고르지 않는다)."""
    iso = o["iso_main"]
    ma, mb = o["channel_median_A"], o["channel_median_B"]
    if o["channel_branch"] == "β1":
        word = "크다" if o["channel_separation"] == "A>B" else "작다"
        s = (f"정적 BV 지도 (S · Cl · softBV 매개변수 · 0 K UMA 구조) 에서 iso {iso} 채널 부피는 A 유리가 B 유리보다 {word} "
             f"(중앙 {ma:.2f} % 대 {mb:.2f} % · 구조 {o['n_A']} · {o['n_B']} 완전 분리 · 정확 양측 p = {o['exact_p_two_sided']:.3f}) "
             f"— 정적 기하 지표이고 확산계수 · 활성화 에너지가 아니다.")
    else:
        s = (f"정적 BV 지도에서 구조 {o['n_A']} · {o['n_B']} 로는 A · B 의 iso {iso} 채널 부피가 구분되지 않았다 "
             f"(중앙 {ma:.2f} % 대 {mb:.2f} % · 범위 겹침) — 정적 기하 지표다.")
    v = o["onset_verdict"]
    if v in ("낮다", "높다"):
        s += (f" 침투 문턱 (고정 격자 {card['bvse_onset_step']} val²) 은 A 가 B 보다 "
              f"{abs(o['onset_median_diff_steps']):.0f} 칸 {v}.")
    elif v == "같다":
        s += f" 침투 문턱은 격자 해상도 안에서 같다 (중앙 차 {o['onset_median_diff_steps']:.0f} 칸)."
    else:
        s += " 침투 문턱은 판정 보류 (칸 수 · 분리 조건 미충족)."
    return s


def run_bvse(card, out_path=None, log=print) -> dict:
    ctl = bvse_control(card)
    log(f"대조 잡 (modelc 정본 재현): {'✓' if ctl['ok'] else '⛔'} onset {ctl['onset']} · 채널 {ctl['iso_pct']}")
    if not ctl["ok"]:
        log("⛔ 정본을 재현하지 못했다 — 열 구조를 읽지 않는다")
        return {"control": ctl, "rows": None}
    rows = structure_table(card)
    log(f"구조 {len(rows)} — 값 지문 · sha16 ✓")
    for r in rows:
        r["bvse"] = bvse_one(REPO / r["path"], int(card["bvse_grid"]))
        b = r["bvse"]
        log(f"  {r['system']} s{r['seed']} ({r['machine']:5s}) ρ {r['rho']:.4f} · voxel {b['voxel_A']} · "
            f"onset {b['onset']} → min {b['onset_min']} · 채널 {b['iso_pct']} · Li BVS {b['li_bvs_mean']}±{b['li_bvs_std']}")
    cmp_ = bvse_compare(rows, card)
    log(f"\n채널 (iso {cmp_['iso_main']}) 갈래 {cmp_['channel_branch']} · onset {cmp_['onset_verdict']}")
    log("문장: " + cmp_["sentence"])
    res = {"card": str(CARD.relative_to(REPO)), "control": ctl, "rows": rows, "compare": cmp_,
           "⛔": "BVSE 는 정적 기하 지표 — D · Ea · σ 아님 · val² 단위 · 결정 BVSE 숫자와 한 표에 놓지 않는다"}
    if out_path:
        pathlib.Path(out_path).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        log(f"→ {out_path}")
    return res


# ───────────────────────── 압력–부피 (UMA 경로 + QE 단일점) ─────────────────────────
GDI = _load_module("generate_dft_inputs", REPO / "tools" / "doping" / "generate_dft_inputs.py")
UMA_PATH_ROOT = REPO / "db" / "raw" / "lpscl_glass_model_check_2026_10_19" / "uma_path"
QE_ROOT = REPO / "db" / "raw" / "lpscl_glass_model_check_2026_10_19" / "qe_path"
GPA = 160.21766208                      # eV/Å³ → GPa
CONTROL_KINDS = ("relax", "k222", "ecut_hi")


def xtag(x) -> str:
    return f"x{float(x):.2f}"


def _num(s):
    try:
        return float(str(s).replace("d", "e").replace("D", "e"))
    except ValueError:
        return None


def qe_text(atoms, prefix, card, pseudo_dir, kind="path"):
    """카드 설정의 pw.x 입력 — kind: path (경로 단일점) · relax · k222 · ecut_hi (대조 셋)."""
    q = card["qe"]
    ew, er = (card["qe_pulay_control_ecut"] if kind == "ecut_hi" else (q["ecutwfc"], q["ecutrho"]))
    kp = " ".join(card["qe_k_control"].split()[:3]) if kind == "k222" else q["kpoints"]
    calc = "relax" if kind == "relax" else "scf"
    t = GDI.generate_pwin(atoms, prefix, ecutwfc=ew, ecutrho=er, kpoints=kp, pseudo_dir=pseudo_dir,
                          pp_names=q["pp"], calculation=calc, nosym=q["nosym"], occupations=q["occupations"],
                          conv_thr=q["conv_thr"], nspin=q["nspin"], mixing_mode=q["mixing_mode"],
                          mixing_beta=q["mixing_beta"], electron_maxstep=q["electron_maxstep"],
                          mixing_ndim=q["mixing_ndim"], smearing=q["smearing"], degauss=q["degauss"])
    if kind == "relax":                 # Nd EOS 생성기 선례 — 이온만 relax: &CELL 하나 지우고 forc 문턱을 카드 값으로
        n_cell = len(re.findall(r"^&CELL\n(?:.*\n)*?/\n", t, re.M))
        t = re.sub(r"^&CELL\n(?:.*\n)*?/\n", "", t, flags=re.M)
        t = t.replace("    forc_conv_thr = 1.0d-4\n", f"    forc_conv_thr = {card['qe_relax_forc_conv_thr']}\n", 1)
        if n_cell != 1 or "&CELL" in t or f"forc_conv_thr = {card['qe_relax_forc_conv_thr']}\n" not in t:
            raise ValueError("⛔ relax 입력 손질 실패 (&CELL 하나 지우기 · forc_conv_thr)")
    return t


def check_qe_input(t, card, kind="path") -> list[str]:
    """대조 잡 c_입력_설정 — 생성한 입력이 카드 표와 한 줄씩 같은가. 어긋난 줄 목록 (빈 목록 = 통과)."""
    q = card["qe"]
    ew, er = (card["qe_pulay_control_ecut"] if kind == "ecut_hi" else (q["ecutwfc"], q["ecutrho"]))
    want = {"calculation": "relax" if kind == "relax" else "scf", "occupations": q["occupations"],
            "smearing": q["smearing"], "mixing_mode": q["mixing_mode"],
            "nosym": ".true." if q["nosym"] else ".false.", "tstress": ".true.", "tprnfor": ".true."}
    wnum = {"ecutwfc": ew, "ecutrho": er, "degauss": q["degauss"], "conv_thr": _num(q["conv_thr"]),
            "mixing_beta": q["mixing_beta"], "mixing_ndim": q["mixing_ndim"], "electron_maxstep": q["electron_maxstep"]}
    if kind == "relax":
        wnum["forc_conv_thr"] = _num(card["qe_relax_forc_conv_thr"])
    bad = []
    for k, v in want.items():
        m = re.search(rf"^\s*{k}\s*=\s*'?([^'\s]+)'?", t, re.M)
        if not m or m.group(1) != str(v):
            bad.append(f"{k}: 얻음 {m.group(1) if m else None} · 카드 {v}")
    for k, v in wnum.items():
        m = re.search(rf"^\s*{k}\s*=\s*(\S+)", t, re.M)
        if not m or _num(m.group(1)) is None or abs(_num(m.group(1)) - float(v)) > 1e-12 * max(1.0, abs(float(v))):
            bad.append(f"{k}: 얻음 {m.group(1) if m else None} · 카드 {v}")
    if re.search(r"^\s*nspin\s*=\s*2", t, re.M) and int(q["nspin"]) == 1:
        bad.append("nspin: 2 · 카드 1")
    if kind == "k222":
        if not re.search(r"^K_POINTS automatic\n\s*" + r"\s+".join(card["qe_k_control"].split()) + r"\s*$", t, re.M):
            bad.append(f"K_POINTS: 카드 {card['qe_k_control']}")
    elif str(q["kpoints"]).lower() == "gamma" and not re.search(r"^K_POINTS gamma\s*$", t, re.M):
        bad.append("K_POINTS: 카드 gamma")
    if kind == "relax" and "&CELL" in t:
        bad.append("&CELL: relax 에 남아 있다")
    for el, f in q["pp"].items():
        if el in t and not re.search(rf"^\s*{el}\s+\S+\s+{re.escape(f)}\s*$", t, re.M):
            bad.append(f"PP {el}: 카드 {f}")
    return bad


def make_qe_inputs(card, uma_root, out_root, pseudo_dir, log=print) -> dict:
    """UMA 경로 점마다 <out>/<라벨>/x<..>/scf.in (+ struct.xyz) · 대조 셋 <out>/controls/<종류>_<라벨>/scf.in · MANIFEST.json.

    ⛔ 못 하는 것: 돌리지 않는다 (러너 몫) · 경로 밖 점 · 다른 설정을 만들지 않는다 · 유사포텐셜이 없으면 거부한다."""
    import hashlib
    from ase.io import read
    uma_root, out_root = pathlib.Path(uma_root), pathlib.Path(out_root)
    pp = GDI.preflight_pseudos(["Li", "P", "S", "Cl"], pseudo_dir, card["qe"]["pp"])
    man = {"card": str(CARD.relative_to(REPO)), "pseudo_dir": str(pseudo_dir), "pseudos": pp, "cells": [], "controls": []}
    bad_all = []

    def emit(d, at, prefix, kind, geom, src):
        t = qe_text(at, prefix, card, pseudo_dir, kind)
        b = check_qe_input(t, card, kind)
        d.mkdir(parents=True, exist_ok=True)
        (d / "scf.in").write_text(t)
        (d / "struct.xyz").write_bytes(geom.read_bytes())
        return {"dir": str(d.relative_to(out_root)), "kind": kind, "source": src,
                "geom_sha256": hashlib.sha256(geom.read_bytes()).hexdigest(),
                "scf_in_sha256": hashlib.sha256(t.encode()).hexdigest(), "check": b or "✓"}, b

    labels = sorted(p.name for p in uma_root.iterdir() if (p / "uma_path.json").is_file())
    for lab in labels:
        J = json.loads((uma_root / lab / "uma_path.json").read_text(encoding="utf-8"))
        for p in sorted(J["points"], key=lambda q: q["x"]):
            g = uma_root / lab / p["geom"]
            if hashlib.sha256(g.read_bytes()).hexdigest() != p["geom_sha256"]:
                raise ValueError(f"⛔ {g}: 기하 sha 가 uma_path.json 과 다르다")
            rec, b = emit(out_root / lab / xtag(p["x"]), read(str(g)), f"{lab}_{xtag(p['x'])}", "path", g, f"{lab}/{p['geom']}")
            man["cells"].append(rec); bad_all += [f"{rec['dir']}: {x}" for x in b]
    for sysn, seed in sorted(card["control_seeds"].items()):
        lab = f"{sysn}_s{seed}"
        J = json.loads((uma_root / lab / "uma_path.json").read_text(encoding="utf-8"))
        p1 = [p for p in J["points"] if abs(p["x"] - 1.0) < 1e-9]
        if not p1:
            raise ValueError(f"⛔ {lab}: x = 1.00 점이 없다 — 대조를 만들 수 없다")
        g = uma_root / lab / p1[0]["geom"]
        for kind in CONTROL_KINDS:
            rec, b = emit(out_root / "controls" / f"{kind}_{lab}", read(str(g)), f"{kind}_{lab}", kind, g, f"{lab}/{p1[0]['geom']}")
            man["controls"].append(rec); bad_all += [f"{rec['dir']}: {x}" for x in b]
    man["c_입력_설정"] = "✓" if not bad_all else bad_all
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    log(f"입력 {len(man['cells'])} 경로 + {len(man['controls'])} 대조 → {out_root} · c_입력_설정 {'✓' if not bad_all else '⛔'}")
    if bad_all:
        raise ValueError("⛔ 카드와 다른 입력 — " + " · ".join(bad_all[:5]))
    return man


def last_stress(text) -> dict:
    """relax 출력의 **마지막** 응력 블록 — 'bfgs converged' 와 끝 SCF 가 있어야 한다 (없으면 예외)."""
    if "bfgs converged" not in text or "End of BFGS Geometry Optimization" not in text:
        raise ValueError("relax 가 수렴하지 않았다 (bfgs converged · End of BFGS 없음)")
    blocks = list(re.finditer(r"total\s+stress\s+\(Ry/bohr\*\*3\)\s+\(kbar\)\s+P=\s*([-\d.Ee+]+)", text))
    if not blocks:
        raise ValueError("응력 블록이 없다")
    E = re.findall(r"^!\s+total energy\s+=\s+([-\d.]+)\s+Ry", text, re.M)
    return {"P_GPa": float(blocks[-1].group(1)) / 10.0, "E_eV": float(E[-1]) * GDI.RY_TO_EV, "n_stress_blocks": len(blocks)}


def read_qe_point(d) -> dict:
    """경로 점 scf.out → E · P · σ · 힘 · 플래그 (GDI 파서 그대로 — 두 실행이 붙은 출력은 거부)."""
    t = (pathlib.Path(d) / "scf.out").read_text(errors="replace")
    E, F, fl = GDI.parse_pw_out(t)
    S = GDI.parse_pw_stress(t)
    return {"E_eV": E, "F": np.asarray(F), "P_GPa": S["P_GPa"], "sigma_GPa": np.asarray(S["sigma_GPa"]),
            "ok": bool(fl["converged"] and fl["job_done"])}


def d3_energies(geom, card) -> dict:
    """simple-dftd3 · PBE BJ (카드 상수) · 3D 주기 — 2체 (s9 주) 와 ATM (s9 atm) 의 에너지 (eV)."""
    from ase.io import read
    from dftd3.interface import DispersionModel, RationalDampingParam
    at = read(str(geom))
    p = dict(card["d3"])
    s9m, s9a = p.pop("s9_main"), p.pop("s9_atm")
    bohr, hartree = 0.529177210903, 27.211386245988
    mdl = DispersionModel(at.get_atomic_numbers(), at.get_positions() / bohr, at.cell.array / bohr,
                          periodic=np.array([True, True, True]))
    e = {s9: mdl.get_dispersion(RationalDampingParam(s9=s9, **p), grad=False)["energy"] * hartree for s9 in (s9m, s9a)}
    return {"E_d3_eV": float(e[s9m]), "E_d3_atm_eV": float(e[s9a])}


def bm3_fit(V, E) -> dict:
    """ASE EquationOfState birchmurnaghan (Nd EOS 맞춤 도구와 같은 구현) — V₀ · E₀ · B₀ · B₀′ · 잔차."""
    from ase.eos import EquationOfState
    V, E = np.asarray(V, float), np.asarray(E, float)
    eos = EquationOfState(V, E, eos="birchmurnaghan")
    v0, e0, B = eos.fit(warn=False)
    res = E - eos.func(V, *eos.eos_parameters)
    return {"V0_A3": float(v0), "E0_eV": float(e0), "B0_GPa": float(B) * GPA, "Bp": float(eos.eos_parameters[2]),
            "rms_meV_atom": None, "rms_meV_cell": float(np.sqrt(np.mean(res ** 2)) * 1000), "n": int(len(V))}


def p_root(V, P):
    """P(V) 영점 (정렬 · 이웃 두 점 선형 보간) — 부호가 안 바뀌면 None."""
    o = np.argsort(V)
    V, P = np.asarray(V, float)[o], np.asarray(P, float)[o]
    for i in range(len(V) - 1):
        if P[i] == 0:
            return float(V[i])
        if P[i] * P[i + 1] < 0:
            return float(V[i] + (V[i + 1] - V[i]) * P[i] / (P[i] - P[i + 1]))
    return None


def read_structure(lab, card, uma_root, qe_root, d3_fn=None) -> dict:
    """한 구조의 경로 → 점 유효성 (토폴로지 · 수렴) · 세 BM3 · UMA 자기일관 · 연장 · ε · 분해 · x = 1.00 단일점."""
    import hashlib
    from ase.io import read
    d3_fn = d3_fn or (lambda g: d3_energies(g, card))
    J = json.loads((pathlib.Path(uma_root) / lab / "uma_path.json").read_text(encoding="utf-8"))
    pts = sorted(J["points"], key=lambda p: p["x"])
    ref = [p for p in pts if abs(p["x"] - 1.0) < 1e-9]
    if not ref:
        return {"label": lab, "status": "경로 불량", "why": "x = 1.00 점이 없다"}
    topo0 = (ref[0]["n_PS"], ref[0]["n_SS"])
    rows, excl = [], []
    for p in pts:
        d = pathlib.Path(qe_root) / lab / xtag(p["x"])
        why = None
        if not p["converged"]:
            why = "UMA 이완 미수렴"
        elif (p["n_PS"], p["n_SS"]) != topo0:
            why = f"토폴로지 변화 (P–S {p['n_PS']} · S–S {p['n_SS']} 대 x=1.00 {topo0})"
        q = None
        if why is None:
            if not (d / "scf.out").is_file():
                why = "QE 출력 없음"
            else:
                try:
                    q = read_qe_point(d)
                    if not q["ok"]:
                        why = "QE 미수렴"
                except ValueError as e:
                    why = f"QE 출력 거부 ({e})"
            if why is None and (d / "struct.xyz").is_file() and \
                    hashlib.sha256((d / "struct.xyz").read_bytes()).hexdigest() != p["geom_sha256"]:
                why = "QE 입력 기하가 UMA 경로 기하와 다르다"
        if why:
            excl.append({"x": p["x"], "why": why}); continue
        g = pathlib.Path(uma_root) / lab / p["geom"]
        d3 = d3_fn(g)
        rows.append({"x": p["x"], "V": p["V_A3"], "E_uma": p["E_eV"], "P_uma": p["P_virial_GPa"],
                     "sigma_uma_ase": np.asarray(p["sigma_GPa"]), "E_pbe": q["E_eV"], "P_pbe": q["P_GPa"],
                     "sigma_pbe": q["sigma_GPa"], "F_pbe": q["F"], "geom": g, **d3})
    out = {"label": lab, "system": lab.split("_")[0], "seed": int(lab.split("_s")[1]),
           "V_final_A3": J["meta"]["V_final_A3"], "n_points": len(rows), "excluded": excl}
    if len(rows) < int(card["min_points_fit"]):
        return {**out, "status": "경로 불량", "why": f"유효 점 {len(rows)} < {card['min_points_fit']}"}
    V = [r["V"] for r in rows]
    curves = {"UMA": [r["E_uma"] for r in rows], "PBE": [r["E_pbe"] for r in rows],
              "PBE+D3": [r["E_pbe"] + r["E_d3_eV"] for r in rows],
              "PBE+D3_ATM": [r["E_pbe"] + r["E_d3_atm_eV"] for r in rows]}
    fits = {k: bm3_fit(V, e) for k, e in curves.items()}
    nat = len(read(str(rows[0]["geom"])))
    for f in fits.values():
        f["rms_meV_atom"] = f["rms_meV_cell"] / nat
        f["x0"] = f["V0_A3"] / out["V_final_A3"]
    out["fits"] = fits
    # 5 점 창 (기록 · V₀ 가까운 다섯)
    win = {}
    for k, e in curves.items():
        o = np.argsort(np.abs(np.asarray(V) - fits[k]["V0_A3"]))[:5]
        if len(o) == 5:
            win[k] = bm3_fit(np.asarray(V)[o], np.asarray(e)[o])["V0_A3"] / fits[k]["V0_A3"] - 1
    out["window5_dV0_rel"] = win
    # UMA 자기일관 (대조 잡 c_UMA_자기일관)
    vr = p_root(V, [r["P_uma"] for r in rows])
    out["uma_P_root_A3"] = vr
    sc = None if vr is None else fits["UMA"]["V0_A3"] / vr - 1
    out["uma_selfconsistency_rel"] = sc
    out["pbe_P_root_A3"] = p_root(V, [r["P_pbe"] for r in rows])             # 기록 (UMA 기하 · Pulay)
    # 연장 규칙
    lo, hi = card["ext_trigger_x"]
    have_lo = any(abs(r["x"] - min(card["path_ext_low"])) < 1e-9 for r in rows) or \
        any(abs(e["x"] - min(card["path_ext_low"])) < 1e-9 for e in excl)
    have_hi = any(abs(r["x"] - max(card["path_ext_high"])) < 1e-9 for r in rows) or \
        any(abs(e["x"] - max(card["path_ext_high"])) < 1e-9 for e in excl)
    out_of = {}
    for k in ("UMA", "PBE", "PBE+D3"):
        x0 = fits[k]["x0"]
        if x0 < lo:
            out_of[k] = "격자 밖 (아래)" if have_lo else "ext_low"
        elif x0 > hi:
            out_of[k] = "격자 밖 (위)" if have_hi else "ext_high"
    out["extension"] = out_of
    if sc is None or abs(sc) > float(card["uma_selfconsistency_tol"]):
        return {**out, "status": "경로 불량", "why": f"UMA 자기일관 {sc} (문턱 {card['uma_selfconsistency_tol']})"}
    need = sorted({v for v in out_of.values() if v.startswith("ext_")})
    if need:
        return {**out, "status": "연장 필요", "why": f"V₀ 가 [{lo}, {hi}] 밖 → {need} 를 한 번 돌린다"}
    if "UMA" in out_of or "PBE" in out_of:
        return {**out, "status": "격자 밖", "why": f"{out_of} — 이 구조의 ε 는 경계값만"}
    out["eps_pbe_uma"] = fits["PBE"]["V0_A3"] / fits["UMA"]["V0_A3"] - 1
    out["eps_d3"] = (None if "PBE+D3" in out_of else fits["PBE+D3"]["V0_A3"] / fits["PBE"]["V0_A3"] - 1)
    out["eps_d3_atm_record"] = fits["PBE+D3_ATM"]["V0_A3"] / fits["PBE"]["V0_A3"] - 1
    # 분해 표 (ln-부피 %)
    mass = float(read(str(rows[0]["geom"])).get_masses().sum())
    v_ref = mass * AMU_G / float(card["rho_ref_g_cm3"][out["system"]])
    Vf, Vu, Vp = out["V_final_A3"], fits["UMA"]["V0_A3"], fits["PBE"]["V0_A3"]
    Vd = fits["PBE+D3"]["V0_A3"]
    out["decomp_pct"] = {"d_열": 100 * math.log(Vf / Vu), "d_모델": 100 * math.log(Vu / Vp),
                         "d_분산": 100 * math.log(Vp / Vd), "d_나머지": 100 * math.log(Vd / v_ref),
                         "합": 100 * math.log(Vf / v_ref), "V_ref_A3": v_ref}
    # x = 1.00 단일점 (P3) — UMA 응력은 ASE 부호 (인장 +) 라 QE 부호 (압축 +) 로 뒤집는다
    r1 = [r for r in rows if abs(r["x"] - 1.0) < 1e-9]
    if r1:
        r1 = r1[0]
        syms = read(str(r1["geom"])).get_chemical_symbols()
        Fm = np.linalg.norm(r1["F_pbe"], axis=1)
        out["P3"] = {"P_uma_GPa": r1["P_uma"], "P_pbe_GPa": r1["P_pbe"], "dP_GPa": r1["P_uma"] - r1["P_pbe"],
                     "max_dsigma_GPa": float(np.abs(-r1["sigma_uma_ase"] - r1["sigma_pbe"]).max()),
                     "F_pbe_rms_eV_A": float(np.sqrt((Fm ** 2).mean())),
                     "F_pbe_rms_by_el": {el: float(np.sqrt((Fm[[i for i, s in enumerate(syms) if s == el]] ** 2).mean()))
                                         for el in sorted(set(syms))}}
    return {**out, "status": "유효"}


def control_band(card, qe_root, fits_by_label) -> dict:
    """대조 셋 → 계마다 띠 b (ΔV/V) · Pulay 보정 · 하나라도 없으면 그 계는 띠 없음 (갈래 보류)."""
    out = {}
    for sysn, seed in sorted(card["control_seeds"].items()):
        lab = f"{sysn}_s{seed}"
        c = pathlib.Path(qe_root) / "controls"
        rec = {"label": lab}
        try:
            base = read_qe_point(pathlib.Path(qe_root) / lab / "x1.00")
            rel = last_stress((c / f"relax_{lab}" / "scf.out").read_text(errors="replace"))
            k = read_qe_point(c / f"k222_{lab}")
            hi = read_qe_point(c / f"ecut_hi_{lab}")
            f = fits_by_label.get(lab)
            if not (base["ok"] and k["ok"] and hi["ok"]) or not f or "PBE" not in f.get("fits", {}):
                raise ValueError("대조 SCF 미수렴 또는 대조 시드 맞춤 없음")
            B0 = f["fits"]["PBE"]["B0_GPa"]
            dP_relax = rel["P_GPa"] - base["P_GPa"]
            dP_k = k["P_GPa"] - base["P_GPa"]
            dP_cut = hi["P_GPa"] - base["P_GPa"]
            band = (abs(dP_relax) + (abs(dP_k) if abs(dP_k) > float(card["k_band_trigger_GPa"]) else 0.0)) / B0
            rec.update({"dP_relax_GPa": dP_relax, "dE_relax_meV_atom": (rel["E_eV"] - base["E_eV"]) * 1000 / 120,
                        "dP_k_GPa": dP_k, "dP_cut_GPa": dP_cut, "B0_PBE_GPa": B0, "band": band,
                        "pulay_correct_P3": abs(dP_cut) > float(card["pulay_trigger_GPa"])})
        except (OSError, ValueError) as e:
            rec.update({"band": None, "why": f"대조 없음/불량 — 갈래 보류 ({e})"})
        out[sysn] = rec
    return out


def system_branch(rows, card, band) -> dict:
    """카드 §4 갈래 — p1 |중앙 ε| + b ≤ 문턱 · p2 중앙 ε + b < −문턱 · p3 중앙 ε − b > +문턱 · p0 그 밖."""
    v = [r for r in rows if r.get("status") == "유효"]
    o = {"n_valid": len(v), "n_total": len(rows)}
    if len(v) < int(card["min_valid_structures"]):
        return {**o, "branch": "구조 부족", "why": f"유효 구조 {len(v)} < {card['min_valid_structures']}"}
    e = [r["eps_pbe_uma"] for r in v]
    o.update({"eps_median": median(e), "eps_range": [min(e), max(e)]})
    d3 = [r["eps_d3"] for r in v if r.get("eps_d3") is not None]
    o["eps_d3_median"] = median(d3) if d3 else None
    o["eps_d3_range"] = [min(d3), max(d3)] if d3 else None
    o["decomp_median_pct"] = {k: median([r["decomp_pct"][k] for r in v]) for k in ("d_열", "d_모델", "d_분산", "d_나머지", "합")}
    if band is None:
        return {**o, "branch": "보류", "why": "대조 띠 없음"}
    thr, m = float(card["eps_threshold"]), o["eps_median"]
    o["band"] = band
    if abs(m) + band <= thr:
        o["branch"] = "p1"
    elif m + band < -thr:
        o["branch"] = "p2"
    elif m - band > thr:
        o["branch"] = "p3"
    else:
        o["branch"] = "p0"
    o["range_straddles"] = (min(e) < -thr < max(e)) or (min(e) < thr < max(e))
    return o


def eos_sentences(sysres) -> list[str]:
    """카드 §1a 문장 — 갈래에서 고른다 (계마다 · 분산 · 나머지 · A–B)."""
    s = []
    pct = lambda x: f"{100 * x:+.1f} %"
    for sysn, o in sorted(sysres.items()):
        nm = {"A": "a-Li₄PS₄Cl", "B": "a-Li₃PS₄"}[sysn]
        if o["branch"] in ("구조 부족", "보류"):
            s.append(f"[{sysn}] {o['branch']} — {o.get('why', '')}"); continue
        rng = f"[{pct(o['eps_range'][0])}, {pct(o['eps_range'][1])}]"
        head = f"[{sysn} · {nm}] 중앙 ε {pct(o['eps_median'])} {rng} · 띠 ±{100 * o['band']:.1f} % · 구조 {o['n_valid']}"
        body = {"p1": "같은 유리 구조에서 UMA 의 0 K 평형 부피는 우리 PBE 설정의 평형 부피와 3 % 안에서 맞았다 — 실험 유리 대비 저밀도에서 UMA–PBE 차의 몫은 크지 않다 (분해 표 d_모델).",
                "p2": "PBE 평형 부피가 UMA 보다 작다 — 저밀도의 일부 (분해 표 d_모델) 는 UMA 가 자기 참조 (PBE) 보다 성기게 만든 몫이다.",
                "p3": "PBE 평형 부피가 UMA 보다 크다 — 저밀도는 UMA–PBE 차로 설명되지 않는다 (PBE 로 가면 더 성기다).",
                "p0": "UMA–PBE 부피 차는 3 % 문턱 근처라 일치 · 불일치를 가르지 않는다."}[o["branch"]]
        s.append(f"{head} — {body}" + (" (구조 범위가 문턱을 걸친다)" if o.get("range_straddles") else ""))
        if o.get("eps_d3_median") is not None:
            s.append(f"[{sysn}] PBE 에 D3(BJ) 2체 분산을 더하면 같은 구조의 평형 부피가 중앙 {pct(o['eps_d3_median'])} "
                     f"[{pct(o['eps_d3_range'][0])}, {pct(o['eps_d3_range'][1])}] 바뀌었다 (UMA 경로 위 단일점 — D3 자체 이완은 안 봤다).")
        dm = o["decomp_median_pct"]
        s.append(f"[{sysn}] 분해 (ln-부피 % · 중앙): 열 {dm['d_열']:+.1f} · 모델 {dm['d_모델']:+.1f} · 분산 {dm['d_분산']:+.1f} · "
                 f"나머지 {dm['d_나머지']:+.1f} = 합 {dm['합']:+.1f} — 나머지는 준비 경로 · 0 K 대 실온 · 실험 기준 (1.88 · 열간프레스 유리 펠릿) · "
                 f"토폴로지 중 어디서 오는지 가르지 않는다 (단서).")
    br = {k: v.get("branch") for k, v in sysres.items()}
    if br.get("A") == "p1" and br.get("B") == "p1":
        s.append("A–B MD 비교 (600 K c2 · 650 K b2) 가 3 % 를 넘는 조성 의존 모델 밀도 오차로 기울지 않았다.")
    elif br.get("A") in ("p1", "p2", "p3", "p0") and br.get("B") in ("p1", "p2", "p3", "p0") and br["A"] != br["B"]:
        s.append(f"두 계의 갈래가 다르다 (A {br['A']} · B {br['B']}) — c2 · b2 문장 옆에 단서로 단다 (판정은 안 바꾼다).")
    s.append("⛔ D · R · Ea · σ 아님 · 'UMA 는 정확하다' 를 이 구조 · 0 K 부피 · 우리 QE PBE 밖으로 넓히지 않는다 · 'PBE+D3 가 정답' 아님.")
    return s


def run_eos(card, uma_root=UMA_PATH_ROOT, qe_root=QE_ROOT, out_path=None, d3_fn=None, log=print) -> dict:
    labels = sorted(p.name for p in pathlib.Path(uma_root).iterdir() if (p / "uma_path.json").is_file())
    per = {lab: read_structure(lab, card, uma_root, qe_root, d3_fn) for lab in labels}
    bands = control_band(card, qe_root, per)
    sysres = {}
    for sysn in ("A", "B"):
        rows = [r for r in per.values() if r["label"].startswith(sysn + "_")]
        sysres[sysn] = system_branch(rows, card, bands[sysn]["band"])
    sent = eos_sentences(sysres)
    for lab, r in per.items():
        ex = f" · 뺀 점 {len(r['excluded'])}" if r.get("excluded") else ""
        log(f"  {lab}: {r['status']}{ex}" + (f" · ε {100 * r['eps_pbe_uma']:+.2f} %" if "eps_pbe_uma" in r else f" · {r.get('why', '')}"))
    for x in sent:
        log(x)

    def clean(o):
        if isinstance(o, dict):
            return {k: clean(v) for k, v in o.items() if k not in ("F_pbe", "sigma_uma_ase", "sigma_pbe", "geom")}
        if isinstance(o, list):
            return [clean(v) for v in o]
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, pathlib.Path):
            return str(o)
        return o
    res = {"card": str(CARD.relative_to(REPO)), "structures": clean(per), "controls": clean(bands),
           "systems": clean(sysres), "sentences": sent}
    if out_path:
        pathlib.Path(out_path).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        log(f"→ {out_path}")
    return res


# ───────────────────────── selftest ─────────────────────────
def _selftest_eos(chk, card, td) -> None:
    """합성 BM3 자료로 압력–부피 판독 배선을 본다 (QE · UMA 아님) — 음성 경로 포함."""
    from ase.io import write
    from ase import Atoms

    def bm3E(V, V0, E0, B, Bp):
        b = B / GPA
        eta = (V0 / V) ** (2 / 3)
        return E0 + 9 * V0 * b / 16 * ((eta - 1) ** 3 * Bp + (eta - 1) ** 2 * (6 - 4 * eta))

    def bm3P(V, V0, B, Bp):
        r = (V0 / V)
        return 1.5 * B * (r ** (7 / 3) - r ** (5 / 3)) * (1 + 0.75 * (Bp - 4) * (r ** (2 / 3) - 1))

    def qe_out(E_eV, P, nat=4, conv=True):
        Ry = E_eV / GDI.RY_TO_EV
        f = "".join(f"     atom {i + 1:4d} type  1   force =     0.00100000    0.00000000   -0.00100000\n" for i in range(nat))
        kb = P * 10
        return ("     Program PWSCF v.7.4.1 starts on 19Oct2026\n"
                + ("     convergence has been achieved in  12 iterations\n" if conv else "")
                + f"!    total energy              =   {Ry:.8f} Ry\n"
                + "     Forces acting on atoms (cartesian axes, Ry/au):\n\n" + f + "\n"
                + f"     total   stress  (Ry/bohr**3)                   (kbar)     P=  {kb:12.2f}\n"
                + f"   0.00000000   0.00000000   0.00000000        {kb:10.2f}  0.00  0.00\n"
                + f"   0.00000000   0.00000000   0.00000000          0.00 {kb:10.2f}  0.00\n"
                + f"   0.00000000   0.00000000   0.00000000          0.00  0.00 {kb:10.2f}\n\n"
                + "     JOB DONE.\n")

    Vf = 1000.0
    scales = [float(x) for x in card["path_scales"]]

    def build(root, lab, Vu0, Vp0, shiftP=0.0, topo_bad=(), qe_fail=()):
        d = root / "uma" / lab
        d.mkdir(parents=True, exist_ok=True)
        pts = []
        for x in scales:
            V = Vf * x
            L = V ** (1 / 3)
            at = Atoms("PS3", positions=[[0, 0, 0], [2.0, 0, 0], [0, 2.0, 0], [0, 0, 2.0]], cell=[L] * 3, pbc=True)
            g = d / f"{xtag(x)}.xyz"
            write(str(g), at, format="extxyz")
            import hashlib
            pts.append({"x": x, "V_A3": V, "E_eV": bm3E(V, Vu0, -10.0, 20.0, 4.5),
                        "P_virial_GPa": bm3P(V, Vu0, 20.0, 4.5) + shiftP,
                        "sigma_GPa": (-np.eye(3) * (bm3P(V, Vu0, 20.0, 4.5) + shiftP)).tolist(),
                        "Fmax_eV_A": 0.01, "steps": 10, "converged": True,
                        "n_PS": 3, "n_SS": 1 if x in topo_bad else 0, "geom": g.name,
                        "geom_sha256": hashlib.sha256(g.read_bytes()).hexdigest()})
            q = root / "qe" / lab / xtag(x)
            q.mkdir(parents=True, exist_ok=True)
            (q / "scf.out").write_text(qe_out(bm3E(V, Vp0, -20.0, 22.0, 4.5), bm3P(V, Vp0, 22.0, 4.5), conv=x not in qe_fail))
            (q / "struct.xyz").write_bytes(g.read_bytes())
        (d / "uma_path.json").write_text(json.dumps({"meta": {"V_final_A3": Vf}, "points": pts}))

    d3z = lambda g: {"E_d3_eV": 0.0, "E_d3_atm_eV": 0.0}
    root = td / "eos"
    build(root, "A_s1", 0.98 * Vf, 0.97 * Vf)
    r = read_structure("A_s1", card, root / "uma", root / "qe", d3z)
    chk(r["status"] == "유효" and abs(r["fits"]["UMA"]["V0_A3"] / (0.98 * Vf) - 1) < 1e-6,
        f"[양성] 합성 BM3 → V₀^UMA 복원 ({r['fits']['UMA']['V0_A3']:.3f})")
    chk(abs(r["eps_pbe_uma"] - (0.97 / 0.98 - 1)) < 1e-6, f"[양성] ε_V(PBE|UMA) = {100 * r['eps_pbe_uma']:.3f} %")
    chk(abs(r["uma_selfconsistency_rel"]) < 1e-3, "[양성] UMA 자기일관 (P 영점 ≈ E 적합 V₀)")
    dm = r["decomp_pct"]
    chk(abs(dm["d_열"] + dm["d_모델"] + dm["d_분산"] + dm["d_나머지"] - dm["합"]) < 1e-9, "[양성] 분해 네 항의 합 = 총")
    chk(abs(r["P3"]["dP_GPa"] - (bm3P(Vf, 0.98 * Vf, 20, 4.5) - bm3P(Vf, 0.97 * Vf, 22, 4.5))) < 0.01, "[양성] P3 ΔP = P_UMA − P_PBE")
    build(root, "A_s2", 0.98 * Vf, 0.97 * Vf, shiftP=0.6)
    r2 = read_structure("A_s2", card, root / "uma", root / "qe", d3z)
    chk(r2["status"] == "경로 불량" and "자기일관" in r2["why"], "[음성] UMA P 를 0.6 GPa 밀면 자기일관 탈락 → 경로 불량")
    build(root, "A_s3", 0.98 * Vf, 0.97 * Vf, topo_bad=(0.85,))
    r3 = read_structure("A_s3", card, root / "uma", root / "qe", d3z)
    chk(r3["status"] == "유효" and r3["n_points"] == len(scales) - 1 and "토폴로지" in r3["excluded"][0]["why"],
        "[음성] 토폴로지 바뀐 점 하나는 빼고 맞춘다 (6 점)")
    build(root, "A_s4", 0.98 * Vf, 0.97 * Vf, topo_bad=(0.85, 0.88), qe_fail=(1.03,))
    r4 = read_structure("A_s4", card, root / "uma", root / "qe", d3z)
    chk(r4["status"] == "경로 불량" and "유효 점" in r4["why"], "[음성] 뺀 점이 셋이면 유효 점 4 < 5 → 경로 불량")
    build(root, "A_s5", 0.98 * Vf, 0.80 * Vf)
    r5 = read_structure("A_s5", card, root / "uma", root / "qe", d3z)
    chk(r5["status"] == "연장 필요" and "ext_low" in r5["why"], "[음성] PBE V₀ 0.80 → 연장 필요 (ext_low)")
    def d3m(g):
        from ase.io import read as _r
        return {"E_d3_eV": -0.05 * 1000.0 / float(_r(str(g)).get_volume()), "E_d3_atm_eV": 0.0}
    r6 = read_structure("A_s1", card, root / "uma", root / "qe", d3m)
    chk(r6["eps_d3"] is not None and r6["eps_d3"] < 0, f"[양성] 끌어당기는 D3 → V₀ 가 줄어든다 ({100 * r6['eps_d3']:.2f} %)")
    # 갈래
    mk = lambda e: {"status": "유효", "eps_pbe_uma": e, "eps_d3": -0.05,
                    "decomp_pct": {"d_열": 1, "d_모델": 1, "d_분산": 5, "d_나머지": 10, "합": 17}}
    chk(system_branch([mk(-0.01), mk(0.0), mk(0.01)], card, 0.01)["branch"] == "p1", "[양성] 중앙 0 · 띠 1 % → p1")
    chk(system_branch([mk(-0.06), mk(-0.05), mk(-0.07)], card, 0.01)["branch"] == "p2", "[양성] 중앙 −6 % · 띠 1 % → p2")
    chk(system_branch([mk(0.06), mk(0.05), mk(0.07)], card, 0.01)["branch"] == "p3", "[양성] 중앙 +6 % → p3")
    chk(system_branch([mk(-0.025), mk(-0.025), mk(-0.02)], card, 0.01)["branch"] == "p0", "[음성] 중앙 −2.5 % · 띠 1 % → 문턱 걸침 p0")
    chk(system_branch([mk(0.0), mk(0.0)], card, 0.01)["branch"] == "구조 부족", "[음성] 유효 구조 2 < 3 → 구조 부족")
    chk(system_branch([mk(0.0), mk(0.0), mk(0.0)], card, None)["branch"] == "보류", "[음성] 대조 띠 없음 → 보류")
    # 입력 생성 · c_입력_설정 (대조 잡) — 가짜 유사포텐셜 폴더
    ppd = td / "pp"
    ppd.mkdir()
    for f in card["qe"]["pp"].values():
        (ppd / f).write_text("fake")
    at = Atoms("LiPS4Cl", positions=[[1, 1, 1], [5, 5, 5], [6.2, 5, 5], [5, 6.2, 5], [5, 5, 6.2], [3.8, 5, 5], [8, 8, 8]],
               cell=[10, 10, 10], pbc=True)
    for kind in ("path", "relax", "k222", "ecut_hi"):
        t = qe_text(at, "t", card, str(ppd), kind)
        chk(check_qe_input(t, card, kind) == [], f"[양성] {kind} 입력이 카드 표와 한 줄씩 같다")
    t = qe_text(at, "t", card, str(ppd), "path").replace("electron_maxstep = 200", "electron_maxstep = 100")
    chk(any("electron_maxstep" in b for b in check_qe_input(t, card, "path")), "[음성] electron_maxstep 100 (생성기 기본) → 잡는다")
    t = qe_text(at, "t", card, str(ppd), "path").replace("K_POINTS gamma", "K_POINTS automatic\n  1 1 1 0 0 0")
    chk(any("K_POINTS" in b for b in check_qe_input(t, card, "path")), "[음성] Γ 대신 automatic 1 1 1 → 잡는다")
    t = qe_text(at, "t", card, str(ppd), "relax")
    chk("&CELL" not in t and "forc_conv_thr = 1.0d-3" in t, "[양성] relax 대조: &CELL 없음 · forc 1.0d-3")
    # relax 마지막 응력
    rtxt = ("     total   stress  (Ry/bohr**3)                   (kbar)     P=  -5.00\n"
            "!    total energy              =   -100.00000000 Ry\n"
            "     bfgs converged in   3 scf cycles and   2 bfgs steps\n     End of BFGS Geometry Optimization\n"
            "!    total energy              =   -100.10000000 Ry\n"
            "     total   stress  (Ry/bohr**3)                   (kbar)     P=  -2.00\n")
    ls = last_stress(rtxt)
    chk(abs(ls["P_GPa"] + 0.2) < 1e-12 and ls["n_stress_blocks"] == 2, "[양성] relax 마지막 응력 블록 (−0.2 GPa)")
    try:
        last_stress(rtxt.replace("bfgs converged", "bfgs failed"))
        chk(False, "[음성] bfgs 미수렴 relax → 죽어야 한다")
    except ValueError:
        chk(True, "[음성] bfgs 미수렴 relax → ValueError")


def _selftest() -> int:
    import copy
    import tempfile
    ok = [0, 0]

    def chk(c, m):
        print(("  ✓ " if c else "  ✗ ") + m)
        ok[0 if c else 1] += 1

    card = load_card()
    # 카드 읽기 — 키가 없으면 죽는다 (음성)
    td = pathlib.Path(tempfile.mkdtemp())
    (td / "c.json").write_text(json.dumps({"x": 1}), encoding="utf-8")
    try:
        load_card(td / "c.json")
        chk(False, "[음성] 기계_판독_값 없는 카드 → 죽어야 한다")
    except KeyError:
        chk(True, "[음성] 기계_판독_값 없는 카드 → KeyError")

    # 완전 분리 · 정확 p
    chk(separation([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]) == "A<B", "[양성] 완전 분리 A<B")
    chk(separation([6, 7, 8, 9, 10], [1, 2, 3, 4, 5]) == "A>B", "[양성] 완전 분리 A>B")
    chk(separation([1, 2, 6, 4, 5], [5.5, 7, 8, 9, 10]) is None, "[음성] 한 값이 겹치면 분리가 아니다")
    chk(separation([1, 2, 3], [3, 4, 5]) is None, "[음성] 같은 값 (동률) 은 분리가 아니다")
    chk(abs(exact_p_separation(5, 5) - 2 / 252) < 1e-12 and abs(exact_p_separation(4, 5) - 2 / 126) < 1e-12,
        "[양성] 정확 p 5·5 = 2/252 · 4·5 = 2/126")

    # bvse_compare 갈래 · onset 칸 수 (가짜 행)
    def fake(sysn, s, ch, on, mach="kgy", rho=1.6):
        return {"system": sysn, "seed": s, "machine": mach, "rho": rho,
                "bvse": {"iso_pct": {str(card["bvse_iso_main"]): ch}, "onset_min": on}}
    rows = [fake("A", i, 5 + i, 0.30) for i in range(1, 6)] + [fake("B", i, 1 + 0.1 * i, 0.50) for i in range(1, 6)]
    o = bvse_compare(rows, card)
    chk(o["channel_branch"] == "β1" and o["channel_separation"] == "A>B", "[양성] 채널 분리 → β1 · A>B")
    chk(o["onset_verdict"] == "낮다", f"[양성] onset 중앙 차 4 칸 + 분리 → '낮다' (얻음 {o['onset_verdict']})")
    rows2 = copy.deepcopy(rows)
    rows2[0]["bvse"]["iso_pct"][str(card["bvse_iso_main"])] = 1.2      # A 하나가 B 범위 안
    chk(bvse_compare(rows2, card)["channel_branch"] == "β2", "[음성] A 하나가 B 범위 안 → β2")
    rows3 = [r for r in rows if not (r["system"] == "B" and r["seed"] >= 3)]   # B 2 개만
    o3 = bvse_compare(rows3, card)
    chk(o3["channel_branch"] == "β2" and "구조 부족" in o3["channel_why"], "[음성] B 구조 2 < 4 → β2 (구조 부족)")
    rows4 = copy.deepcopy(rows)
    for r in rows4:
        r["bvse"]["onset_min"] = 0.40 if r["system"] == "A" else 0.45   # 1 칸
    chk(bvse_compare(rows4, card)["onset_verdict"] == "같다", "[양성] onset 중앙 차 1 칸 → '같다'")
    for r in rows4:
        r["bvse"]["onset_min"] = 0.40 if r["system"] == "A" else 0.50   # 2 칸
    chk(bvse_compare(rows4, card)["onset_verdict"] == "보류", "[양성] onset 중앙 차 2 칸 → '보류'")
    rows5 = copy.deepcopy(rows4)
    for r in rows5:
        r["bvse"]["onset_min"] = 0.40 if r["system"] == "A" else 0.60   # 4 칸 · 그런데 겹침
    rows5[0]["bvse"]["onset_min"] = 0.70
    chk(bvse_compare(rows5, card)["onset_verdict"] == "보류", "[음성] onset 4 칸이어도 분리가 아니면 '보류'")
    rows6 = copy.deepcopy(rows)
    rows6[0]["bvse"]["onset_min"] = None
    chk(bvse_compare(rows6, card)["onset_verdict"] == "보류", "[음성] 침투 없음 구조가 있으면 '보류'")
    chk("확산계수" in o["sentence"] and "eV" not in o["sentence"], "[양성] 문장에 '확산계수 아님' 단서 · eV 없음")

    # 정본 재현 대조 잡 — 실제 지도 (양성) · 흔든 카드 값 (음성)
    ctl = bvse_control(card)
    chk(ctl["ok"], f"[양성] modelc 정본 재현 onset {ctl['onset']} · 채널 {ctl['iso_pct']}")
    bad = copy.deepcopy(card)
    bad["bvse_control"]["onset"]["c"] = 1.45
    chk(not bvse_control(bad)["ok"], "[음성] 카드 정본을 한 칸 흔들면 대조 잡이 떨어진다")

    # 비입방 셀 거부 (음성) · 입방 통과 (양성)
    try:
        check_cubic(np.array([[10, 0, 0], [0.5, 10, 0], [0, 0, 10]], float))
        chk(False, "[음성] 기울어진 셀 → 죽어야 한다")
    except ValueError:
        chk(True, "[음성] 기울어진 셀 → ValueError")
    try:
        check_cubic(np.diag([10.0, 10.0, 10.5]))
        chk(False, "[음성] 직교 비입방 → 죽어야 한다")
    except ValueError:
        chk(True, "[음성] 직교 비입방 → ValueError")

    # 작은 가짜 구조로 bvse_one 경로 (양성) — 입방 10 Å · Li 1 · S 2
    xyz = td / "t.xyz"
    xyz.write_text('3\nLattice="10 0 0 0 10 0 0 0 10" Properties=species:S:1:pos:R:3\n'
                   "Li 5.0 5.0 5.0\nS 2.5 5.0 5.0\nS 7.5 5.0 5.0\n")
    b1 = bvse_one(xyz, 20)
    chk(b1["grid"] == [20, 20, 20] and abs(b1["voxel_A"] - 0.5) < 1e-9 and set(b1["iso_pct"]) == {"0.25", "0.5", "1.0", "1.5", "2.0"},
        f"[양성] bvse_one 경로 (격자 {b1['grid']} · 복셀 {b1['voxel_A']})")

    # 지문 — 실제 A seed1 을 0.1 Å 흔들면 불일치 (음성) — 회수본이 있을 때만
    p1 = A_ROOT / "kgy" / "A" / "seed1" / "final.xyz"
    if p1.is_file():
        from ase.io import read, write
        at = read(str(p1))
        i = [j for j, s in enumerate(at.get_chemical_symbols()) if s == "P"][0]
        pos = at.get_positions()
        dmin = mic_dist(pos[[i]], pos[np.array(at.get_chemical_symbols()) == "S"], at.cell.array)
        jn = int(np.argmin(dmin[0]))
        js = [j for j, s in enumerate(at.get_chemical_symbols()) if s == "S"][jn]
        v = pos[js] - pos[i]
        pos[js] = pos[js] - 0.1 * v / np.linalg.norm(v)                 # 가장 가까운 S 를 P 쪽으로 0.1 Å
        at.set_positions(pos)
        q = td / "bad.xyz"
        write(str(q), at, format="extxyz")
        f = fingerprint(q)
        want = card["a_fingerprint"]["1"]
        chk(abs(f["min_PS_A"] - want[0]) > card["a_fingerprint_tol"]["min_PS_A"],
            f"[음성] P–S 0.1 Å 흔든 구조 → 지문 불일치 (최단 {f['min_PS_A']:.4f} 대 {want[0]})")
        rows_real = structure_table(card)
        chk(len(rows_real) == 10 and sorted({r['system'] for r in rows_real}) == ["A", "B"],
            "[양성] 카드 열 구조 지문 · sha16 전부 일치")
    else:
        print("  · (회수본 없음 — 지문 시험 건너뜀)")

    # 압력–부피 판독 (합성 자료) + 실제 D3 한 번
    _selftest_eos(chk, card, td)
    e3 = d3_energies(xyz, card)
    chk(e3["E_d3_eV"] < 0 and e3["E_d3_atm_eV"] != e3["E_d3_eV"], f"[양성] simple-dftd3 실행 (2체 {e3['E_d3_eV']:.4f} · ATM {e3['E_d3_atm_eV']:.4f} eV)")
    n_ok, n_bad = ok
    print(f"selftest {'PASS' if n_bad == 0 else 'FAIL'}  ({n_ok}/{n_ok + n_bad})")
    return 0 if n_bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--bvse_control", action="store_true", help="대조 잡만: modelc 정본 재현")
    ap.add_argument("--bvse", action="store_true", help="열 구조 BVSE 판독 (대조 잡을 먼저 돈다)")
    ap.add_argument("--out", help="--bvse · --eos 결과 json · --qe_inputs 출력 폴더")
    ap.add_argument("--qe_inputs", action="store_true", help="UMA 경로 → QE 입력 (경로 + 대조 셋) · c_입력_설정 대조")
    ap.add_argument("--eos", action="store_true", help="압력–부피 판독 (UMA 경로 + QE 출력 + D3) → 갈래 · 분해 · 문장")
    ap.add_argument("--uma_path", default=str(UMA_PATH_ROOT), help="UMA 경로 루트 (<라벨>/uma_path.json)")
    ap.add_argument("--qe_root", default=str(QE_ROOT), help="--eos: QE 출력 루트 (<라벨>/x<..>/scf.out · controls/)")
    ap.add_argument("--pseudo_dir", help="--qe_inputs: 실행 기계의 유사포텐셜 폴더 (해시를 MANIFEST 에)")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    card = load_card()
    if a.bvse_control:
        c = bvse_control(card)
        print(json.dumps(c, ensure_ascii=False, indent=1))
        return 0 if c["ok"] else 3
    if a.bvse:
        r = run_bvse(card, a.out)
        return 0 if r["rows"] is not None else 3
    if a.qe_inputs:
        if not (a.out and a.pseudo_dir):
            ap.error("--qe_inputs 는 --out 과 --pseudo_dir 이 필요하다")
        make_qe_inputs(card, a.uma_path, a.out, a.pseudo_dir)
        return 0
    if a.eos:
        r = run_eos(card, a.uma_path, a.qe_root, a.out)
        return 0 if all(v.get("branch") not in (None,) for v in r["systems"].values()) else 3
    ap.error("--bvse · --bvse_control · --qe_inputs · --eos · --selftest 중 하나")
    return 2


if __name__ == "__main__":
    sys.exit(main())
