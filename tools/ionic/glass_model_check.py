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


# ───────────────────────── selftest ─────────────────────────
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
    n_ok, n_bad = ok
    print(f"selftest {'PASS' if n_bad == 0 else 'FAIL'}  ({n_ok}/{n_ok + n_bad})")
    return 0 if n_bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--bvse_control", action="store_true", help="대조 잡만: modelc 정본 재현")
    ap.add_argument("--bvse", action="store_true", help="열 구조 BVSE 판독 (대조 잡을 먼저 돈다)")
    ap.add_argument("--out", help="--bvse 결과 json")
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
    ap.error("--bvse · --bvse_control · --selftest 중 하나")
    return 2


if __name__ == "__main__":
    sys.exit(main())
