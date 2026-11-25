#!/usr/bin/env python3
"""analyze_interface_decomp.py — decomposition metrics from an SE|Li interface traj.

Tracks, per production frame, the fingerprints of Li reducing the SE:
  - P-S coordination   (intact PS4 ~ 4 ; drop = P-S bond breaking -> PS_n)
  - S-Li coordination  (rise = Li2S_n formation on S)
  - P-Li coordination  (rise = Li3P formation on P)
  - B-S / B-Li         (b2o3 only: BS3 ~3 ; B-Li>0 = metallic LiB reduction  <-- THE flag)
  - Li penetration     (# Li that crossed below the initial SE surface)
Writes a per-frame CSV + an initial-vs-final summary. Run per system, then compare
b2o3 vs modelc (more P-S loss / Li penetration / B-Li = worse dynamic decomposition).

  python3 tools/oxidation/analyze_interface_decomp.py b2o3_traj.xyz --label b2o3 \
    --dt_ps 0.2 --out db/properties/interface_decomp_b2o3.csv

2026-11-20 — [혁주] MD-1 판독 (카드 db/properties/hyeokju_lzo_md_card_2026_11_16.json ⏩_개정_2_2026_11_20_MD1_결과_전)
  python3 tools/oxidation/analyze_interface_decomp.py --md1 <seed>_traj.xyz --freeze <init>_freeze.json --label s1 \
          --out_json s1_md1.json --out_csv s1_md1.csv          # 시드 하나
  python3 tools/oxidation/analyze_interface_decomp.py --md1_ensemble s1_md1.json s2_md1.json s3_md1.json --out_json md1_verdict.json
  python3 tools/oxidation/analyze_interface_decomp.py --selftest
  · 판정 결합 (카드 기계_판독_값 pairs_judged) 을 프레임마다 최소상 거리로 세고, 같은 원자 쌍이 연속 L 프레임 (persist_ps) 이상
    문턱 안에 있으면 '지속 결합 사건' 으로 센다 (한 프레임이라도 끊기면 새 구간 — 끊김 허용 없음) · 첫 사건 시작 시각 · 최장 구간 ·
    프레임마다 순간 · 지속 결합 수 (Origin CSV) · 기록 쌍 (pairs_record) 은 같은 방식으로 세되 판정에 안 쓴다 ·
    Li 가 계면을 넘은 수는 기록만 (슬랩 무거운 원자 중심에서 z 거리 · 처음 슬랩 반두께 + 1 Å)
  · 무결성 문 (하나라도 걸리면 그 시드 판정 안 함): 프레임 수 = prod/save + 1 · 프레임 k 의 t_prod_ps = k·save_fs · 원소열 · 셀 고정 ·
    좌표 유한 · 생산 평균 T 가 T_K ± T_band_K · 판정 쌍의 두 원소가 각각 슬랩 · 블록 한쪽에만 있다 (원소로 기원을 가른다)
  · 앙상블: 시드 수 = n_seeds · 전부 무결성 통과 · 궤적 sha 가 서로 다름 → 결합마다 사건 있는 시드 ≥ onset_seeds_min 이면 '개시 관측' ·
    1 이면 '시드 하나에서만' · 0 이면 '관측창 안 개시 없음' + 관측창 한 줄 (tools/sei/collect_neb.py observation_window ·
    t = 시드 수 × prod · 반응 기회 n = 두 원소 원자 수 중 작은 쪽 — 가정)
2026-11-22 — 개정 3 (결과 전 · 카드 ⏩_개정_3_2026_11_22_MD1_결과_전_t0쌍 · 사용자 선택 '새로 생긴 쌍만 판정')
  · 생산 첫 프레임 (t = 0) 에 이미 문턱 안이던 원자 쌍은 그 쌍의 사건을 전부 판정에서 뺀다 (기록만 — t0_pairs · n_t0_pairs) —
    그 쌍을 모든 프레임에서 지운 존재 배열로 같은 지속 규칙을 다시 센다 (n_events_new · first_onset_new_ps · {AB}_persist_new 열 ·
    끊겼다 다시 붙어도 그 쌍은 안 센다)
  · 앙상블은 개정 3 이 active 면 n_events_new 로 센다 (t = 0 쌍까지 센 개정 2 셈은 record_amend2_* 로 같이 남긴다) ·
    시드 판독이 지금 카드와 같은 개정 3 규칙으로 만들어지지 않았으면 판정 보류 · 개정 3 이 카드에 있는데 active 가 아니면
    판독 · 앙상블 둘 다 거부 · 카드에 개정 3 이 없으면 옛 판정 · 옛 출력 그대로
  ⛔ 개정 3 이 못 하는 것: t = 0 에 문턱 바로 밖에 있다가 들어온 쌍 (담금질 때 가까워진 쌍) 은 '새로 생긴 쌍' 으로 센다 —
    '새로 생겼다' 는 '생산 중 처음 문턱 안에 들어왔다' 는 뜻이지 '600 K 에서 새로 다가왔다' 는 증명이 아니다
  ⛔ MD-1 판독이 못 하는 것: 반응 속도 · 생성량 · 보호 효과를 내지 않는다 · 거리 문턱 결합이 화학 결합이라는 증명이 아니다
    (지속 시간으로 열진동 접촉을 거를 뿐) · 문턱은 카드에서만 읽는다 (스스로 정하지 않는다) · UMA 힘이 긴 동역학에서 맞는지 모른다
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np
from ase.io import read

CUT = {("P", "S"): 2.6, ("B", "S"): 2.5, ("B", "O"): 1.9, ("P", "O"): 1.9,
       ("Li", "S"): 2.95, ("Li", "P"): 2.9, ("Li", "B"): 2.85, ("Li", "Cl"): 3.0,
       ("Li", "O"): 2.4}


def coord(atoms, D, sym, a, b, cut):
    ia = np.where(sym == a)[0]
    ib = np.where(sym == b)[0]
    if len(ia) == 0 or len(ib) == 0:
        return np.nan
    sub = D[np.ix_(ia, ib)]
    return float((sub < cut).sum(axis=1).mean())     # avg # of b-neighbors per a


def legacy_main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("traj")
    ap.add_argument("--label", required=True)
    ap.add_argument("--dt_ps", type=float, default=0.2, help="save interval (ps) between frames")
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)

    frames = read(a.traj, index=":")
    sym0 = np.array(frames[0].get_chemical_symbols())
    has_B = "B" in sym0
    # O dopant present AND not part of B2O3 (b2o3 O is tracked via B); for LPSOCl the O
    # is a POS3 unit -> track P-O (unit intact) and O-Li (O reduced to Li2O). 2026-07-18.
    has_O = ("O" in sym0) and not has_B

    se_top0 = frames[0].positions[sym0 != "Li", 2].max()   # initial SE surface z

    rows = []
    hdr = ["frame", "t_ps", "P_S", "S_Li", "P_Li", "Li_penetrated"]
    if has_B:
        hdr += ["B_S", "B_Li"]
    if has_O:
        hdr += ["P_O", "O_Li"]
    for k, at in enumerate(frames):
        sym = np.array(at.get_chemical_symbols())
        D = at.get_all_distances(mic=True)
        r = [k, k * a.dt_ps,
             coord(at, D, sym, "P", "S", CUT[("P", "S")]),
             coord(at, D, sym, "S", "Li", CUT[("Li", "S")]),
             coord(at, D, sym, "P", "Li", CUT[("Li", "P")])]
        # Li that crossed below the initial SE surface (penetration into SE)
        zli = at.positions[sym == "Li", 2]
        r.append(int((zli < se_top0).sum()))
        if has_B:
            r.append(coord(at, D, sym, "B", "S", CUT[("B", "S")]))
            r.append(coord(at, D, sym, "B", "Li", CUT[("Li", "B")]))
        if has_O:
            # from O's view: O-P ~1 = POS3 intact (drop = P-O broke); O-Li rise = Li2O
            r.append(coord(at, D, sym, "O", "P", CUT[("P", "O")]))
            r.append(coord(at, D, sym, "O", "Li", CUT[("Li", "O")]))
        rows.append(r)

    rows = np.array(rows, float)
    out = a.out or f"interface_decomp_{a.label}.csv"
    with open(out, "w") as f:
        f.write(",".join(hdr) + "\n")
        for row in rows:
            f.write(",".join(f"{v:.3f}" for v in row) + "\n")

    i0, iN = rows[0], rows[-1]
    ps4_loss = (i0[2] - iN[2]) / i0[2] * 100 if i0[2] else 0
    print(f"\n===== [{a.label}] interface decomposition ({len(frames)} frames, {rows[-1,1]:.0f} ps) =====")
    print(f"  P-S coord : {i0[2]:.2f} -> {iN[2]:.2f}   ({ps4_loss:+.0f}% PS4 bonds; drop = P-S breaking)")
    print(f"  S-Li coord: {i0[3]:.2f} -> {iN[3]:.2f}   (rise = Li2S_n on S)")
    print(f"  P-Li coord: {i0[4]:.2f} -> {iN[4]:.2f}   (rise = Li3P on P)")
    print(f"  Li penetr.: {int(i0[5])} -> {int(iN[5])} atoms below initial SE surface")
    if has_B:
        print(f"  B-S coord : {i0[6]:.2f} -> {iN[6]:.2f}   (BS3 ~3; drop = B-S breaking)")
        print(f"  B-Li coord: {i0[7]:.2f} -> {iN[7]:.2f}   <-- >0 = metallic-LiB reduction (THE worst-case flag)")
    if has_O:
        print(f"  P-O coord : {i0[6]:.2f} -> {iN[6]:.2f}   (O-P ~1 = POS3 intact; drop = P-O breaking)")
        print(f"  O-Li coord: {i0[7]:.2f} -> {iN[7]:.2f}   <-- rise = O reduced to Li2O (the O-dopant flag)")
    print(f"  -> {out}")


# ───────────────────────── [혁주] MD-1 판독 (2026-11-20) ─────────────────────────
MD1_CARD = "db/properties/hyeokju_lzo_md_card_2026_11_16.json"
MD1_AMEND = "⏩_개정_2_2026_11_20_MD1_결과_전"
MD1_KEYS = ("pairs_judged", "pairs_record", "persist_ps", "save_fs", "prod_ps", "T_K", "T_band_K", "n_seeds",
            "onset_seeds_min", "slab_elements", "block_elements")
MD1_EVENTS_KEEP = 200          # 판독 JSON 에 싣는 사건 수 상한 (개수 · 첫 시각 · 최장은 전부에서 낸다)
MD1_AMEND3 = "⏩_개정_3_2026_11_22_MD1_결과_전_t0쌍"


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def md1_load_card(path=MD1_CARD, amend=MD1_AMEND):
    """카드 개정의 기계_판독_값 → dict. 개정이 없거나 active 가 아니거나 열쇠가 빠지면 SystemExit (숫자를 지어내지 않는다)."""
    c = json.loads(Path(path).read_text(encoding="utf-8"))
    if amend not in c:
        sys.exit(f"⛔ 카드에 {amend} 가 없다 — 판독하지 않는다")
    a = c[amend]
    if not str(a.get("상태", "")).startswith("active"):
        sys.exit(f"⛔ MD-1 개정이 active 가 아니다 ({str(a.get('상태'))[:40]!r}) — 판독하지 않는다")
    th = a.get("기계_판독_값") or {}
    miss = [k for k in MD1_KEYS if k not in th]
    if miss:
        sys.exit(f"⛔ 기계_판독_값에 {miss} 가 없다 — 숫자를 지어내지 않는다")
    return th


def md1_load_amend3(path=MD1_CARD):
    """카드 개정 3 (t = 0 쌍 빼기) → 규칙 dict · 카드에 없으면 None (개정 2 판정 그대로).
    있는데 active 가 아니거나 규칙 열쇠가 어긋나면 SystemExit — 반쯤 걸친 규칙으로 판독하지 않는다."""
    c = json.loads(Path(path).read_text(encoding="utf-8"))
    if MD1_AMEND3 not in c:
        return None
    a = c[MD1_AMEND3]
    if not str(a.get("상태", "")).startswith("active"):
        sys.exit(f"⛔ MD-1 개정 3 이 카드에 있는데 active 가 아니다 ({str(a.get('상태'))[:40]!r}) — 판독하지 않는다")
    rule = a.get("기계_판독_값") or {}
    if rule.get("judge_excludes_t0_pairs") is not True or rule.get("t0_frame") != 0:
        sys.exit(f"⛔ 개정 3 기계_판독_값이 'judge_excludes_t0_pairs: true · t0_frame: 0' 이 아니다 ({rule}) — 숫자를 지어내지 않는다")
    return rule


def md1_verdict_word(k, th):
    """사건 있는 시드 수 → 판정 낱말 (카드 onset_seeds_min)."""
    return "개시 관측" if k >= th["onset_seeds_min"] else ("시드 하나에서만" if k == 1 else "관측창 안 개시 없음")


def md1_persist_frames(th):
    L = th["persist_ps"] * 1000.0 / th["save_fs"]
    if abs(L - round(L)) > 1e-9 or round(L) < 1:
        sys.exit(f"⛔ persist_ps {th['persist_ps']} 가 save_fs {th['save_fs']} 의 양의 정수배가 아니다")
    return int(round(L))


def md1_integrity(frames, th, slab_idx):
    """무결성 문 → (문제 목록, 생산 평균 T). 문제가 하나라도 있으면 그 시드는 판정하지 않는다."""
    prob = []
    n_exp = int(round(th["prod_ps"] * 1000.0 / th["save_fs"])) + 1
    if len(frames) != n_exp:
        prob.append(f"프레임 {len(frames)} ≠ 기대 {n_exp} (prod {th['prod_ps']} ps · save {th['save_fs']} fs)")
    sym0 = frames[0].get_chemical_symbols()
    cell0 = np.array(frames[0].cell.array)
    for k, at in enumerate(frames):
        if at.get_chemical_symbols() != sym0:
            prob.append(f"프레임 {k} 원소열이 다르다"); break
        if not np.allclose(np.array(at.cell.array), cell0, atol=1e-8):
            prob.append(f"프레임 {k} 셀이 바뀌었다 (NVT 여야 한다)"); break
        if not np.isfinite(at.positions).all():
            prob.append(f"프레임 {k} 좌표가 유한하지 않다"); break
        tk = at.info.get("t_prod_ps")
        if tk is None or not np.isfinite(float(tk)) or abs(float(tk) - k * th["save_fs"] / 1000.0) > 1e-6:
            prob.append(f"프레임 {k} t_prod_ps {tk} ≠ {k * th['save_fs'] / 1000.0}"); break
    Tm = None
    Ts = [at.info.get("T_inst_K") for at in frames]
    if any(x is None for x in Ts):
        prob.append("프레임에 T_inst_K 기록이 없다")
    else:
        Tm = float(np.mean([float(x) for x in Ts]))
        if not np.isfinite(Tm) or abs(Tm - th["T_K"]) > th["T_band_K"]:
            prob.append(f"생산 평균 T {Tm:.1f} K — {th['T_K']} ± {th['T_band_K']} K 밖")
    sym = np.array(sym0)
    slab = np.zeros(len(sym), bool)
    idx = sorted(set(int(i) for i in slab_idx))
    if not idx or idx[0] < 0 or idx[-1] >= len(sym):
        prob.append("슬랩 인덱스가 원자 범위 밖이거나 비었다")
        return prob, Tm
    slab[idx] = True
    if set(sym[slab]) - set(th["slab_elements"]):
        prob.append(f"슬랩에 뜻밖의 원소 {sorted(set(sym[slab]) - set(th['slab_elements']))}")
    if set(sym[~slab]) - set(th["block_elements"]):
        prob.append(f"블록에 뜻밖의 원소 {sorted(set(sym[~slab]) - set(th['block_elements']))}")
    for A, B, _cut in list(th["pairs_judged"]) + list(th["pairs_record"]):
        for el in (A, B):
            m = sym == el
            if not m.any():
                prob.append(f"원소 {el} 가 없다 ({A}-{B})")
            elif slab[m].any() and (~slab[m]).any():
                prob.append(f"원소 {el} 가 슬랩 · 블록 양쪽에 있다 — 원소로 기원을 가를 수 없다 ({A}-{B})")
        mA, mB = sym == A, sym == B
        if mA.any() and mB.any() and (slab[mA].all() == slab[mB].all()):
            prob.append(f"{A}-{B} 두 원소가 같은 쪽에 있다 — 계면을 건너는 결합이 아니다")
    return prob, Tm


def md1_presence(frames, A, B, cut):
    """프레임마다 (A 원자 × B 원자) 최소상 거리 < cut → bool 배열 (프레임, nA, nB) · A · B 인덱스."""
    from ase.geometry import get_distances
    sym = np.array(frames[0].get_chemical_symbols())
    ia, ib = np.where(sym == A)[0], np.where(sym == B)[0]
    P = np.zeros((len(frames), len(ia), len(ib)), bool)
    for k, at in enumerate(frames):
        _, D = get_distances(at.positions[ia], at.positions[ib], cell=at.cell, pbc=at.pbc)
        P[k] = D < cut
    return P, ia, ib


def md1_runs(P, L):
    """쌍마다 연속 True 구간 중 길이 ≥ L 인 것만 사건 → (사건 [(a, b, 시작 프레임, 프레임 수)], 프레임마다 지속 결합 수)."""
    nF, nA, nB = P.shape
    persist = np.zeros(nF, int)
    events = []
    for a in range(nA):
        for b in range(nB):
            col = P[:, a, b].astype(np.int8)
            if not col.any():
                continue
            d = np.diff(np.concatenate(([0], col, [0])))
            for s, e in zip(np.where(d == 1)[0], np.where(d == -1)[0]):
                if e - s >= L:
                    events.append((a, b, int(s), int(e - s)))
                    persist[s:e] += 1
    events.sort(key=lambda x: (x[2], x[0], x[1]))
    return events, persist


def md1_li_crossing(frames, slab_idx):
    """기록만 — 블록 출신 Li 가 슬랩 영역 안 · 슬랩 출신 Li 가 슬랩 영역 밖에 있는 수 (프레임마다).
    슬랩 영역 = 슬랩 무거운 원자 (Li 아닌 원자) 의 z 원형 평균에서 |Δz| ≤ 처음 슬랩 반두께 + 1 Å (주기 z)."""
    sym = np.array(frames[0].get_chemical_symbols())
    slab = np.zeros(len(sym), bool); slab[sorted(set(int(i) for i in slab_idx))] = True
    heavy = slab & (sym != "Li")
    li = sym == "Li"

    def center_and_dz(at):
        c = at.cell.lengths()[2]
        fz = at.get_scaled_positions(wrap=True)[:, 2]
        ang = 2 * np.pi * fz[heavy]
        cz = (np.arctan2(np.sin(ang).mean(), np.cos(ang).mean()) / (2 * np.pi)) % 1.0
        dz = ((fz - cz + 0.5) % 1.0 - 0.5) * c
        return dz

    dz0 = center_and_dz(frames[0])
    half = float(np.abs(dz0[heavy]).max()) + 1.0
    out_in, out_out = [], []
    for at in frames:
        dz = np.abs(center_and_dz(at))
        out_in.append(int(((~slab) & li & (dz <= half)).sum()))
        out_out.append(int((slab & li & (dz > half)).sum()))
    return np.array(out_in), np.array(out_out), half


def md1_readout(traj, freeze, label, out_json, out_csv, card=MD1_CARD):
    """시드 하나의 MD-1 판독 → JSON · Origin CSV. 출력 파일이 이미 있으면 거부."""
    for o in (out_json, out_csv):
        if os.path.exists(o):
            sys.exit(f"⛔ {o} 가 이미 있다 — 덮지 않는다")
    th = md1_load_card(card)
    a3 = md1_load_amend3(card)          # None = 카드에 개정 3 없음 (옛 판정) · 있는데 active 아니면 여기서 거부
    L = md1_persist_frames(th)
    j = json.loads(Path(freeze).read_text(encoding="utf-8"))
    slab_idx = j["freeze_idx"] if isinstance(j, dict) else j
    frames = read(traj, index=":", format="extxyz")
    prob, Tm = md1_integrity(frames, th, slab_idx)
    rec = {"schema": "hyeokju_md1_seed_readout/v1", "label": label, "card": card, "amend": MD1_AMEND,
           "thresholds": th, "persist_frames": L,
           "tool": {"path": os.path.relpath(os.path.abspath(__file__)), "sha256": _sha(__file__)},
           "traj": {"path": traj, "sha256": _sha(traj), "n_frames": len(frames)},
           "freeze": {"path": freeze, "sha256": _sha(freeze), "n_slab": len(set(int(i) for i in slab_idx))},
           "integrity": {"ok": not prob, "problems": prob, "T_prod_mean_K": Tm}, "pairs": {}}
    if a3 is not None:
        rec["amend3"] = {"key": MD1_AMEND3, "rule": a3}
    cols = {"t_ps": np.array([float(f.info.get("t_prod_ps", np.nan)) for f in frames])}
    if not prob:
        dt = th["save_fs"] / 1000.0
        for judged, plist in ((True, th["pairs_judged"]), (False, th["pairs_record"])):
            for A, B, cut in plist:
                key = f"{A}-{B}"
                P, ia, ib = md1_presence(frames, A, B, float(cut))
                ev, per = md1_runs(P, L)
                inst = P.reshape(len(frames), -1).sum(axis=1)
                rec["pairs"][key] = {
                    "judged": judged, "cut_A": float(cut), "n_A": int(len(ia)), "n_B": int(len(ib)),
                    "n_events": len(ev), "n_distinct_pairs": len({(a, b) for a, b, _, _ in ev}),
                    "first_onset_ps": (round(min(s for _, _, s, _ in ev) * dt, 6) if ev else None),
                    "max_run_ps": (round(max(n for *_, n in ev) * dt, 6) if ev else None),
                    "frac_frames_with_persistent": float((per > 0).mean()),
                    "inst_max": int(inst.max()), "frames_with_inst_contact": int((inst > 0).sum()),
                    "events": [{"A_idx": int(ia[a]), "B_idx": int(ib[b]), "start_ps": round(s * dt, 6),
                                "dur_ps": round(n * dt, 6)} for a, b, s, n in ev[:MD1_EVENTS_KEEP]],
                    "events_truncated": len(ev) > MD1_EVENTS_KEEP}
                cols[f"{A}{B}_inst"] = inst
                cols[f"{A}{B}_persist"] = per
                if a3 is not None:
                    t0a, t0b = np.where(P[a3["t0_frame"]])
                    Pn = P.copy()
                    Pn[:, t0a, t0b] = False      # t = 0 쌍은 모든 프레임에서 지운다 (끊겼다 다시 붙어도 그 쌍은 안 센다)
                    evn, pern = md1_runs(Pn, L)
                    rec["pairs"][key].update({
                        "t0_pairs": [[int(ia[x]), int(ib[y])] for x, y in zip(t0a, t0b)],
                        "n_t0_pairs": int(len(t0a)),
                        "n_events_new": len(evn), "n_distinct_new_pairs": len({(x, y) for x, y, _, _ in evn}),
                        "first_onset_new_ps": (round(min(s for _, _, s, _ in evn) * dt, 6) if evn else None),
                        "max_run_new_ps": (round(max(n for *_, n in evn) * dt, 6) if evn else None),
                        "events_new": [{"A_idx": int(ia[x]), "B_idx": int(ib[y]), "start_ps": round(s * dt, 6),
                                        "dur_ps": round(n * dt, 6)} for x, y, s, n in evn[:MD1_EVENTS_KEEP]],
                        "events_new_truncated": len(evn) > MD1_EVENTS_KEEP})
                    cols[f"{A}{B}_persist_new"] = pern
        lin, lout, half = md1_li_crossing(frames, slab_idx)
        rec["li_crossing_record"] = {"block_Li_in_slab_max": int(lin.max()), "slab_Li_out_max": int(lout.max()),
                                     "block_Li_in_slab_last": int(lin[-1]), "slab_Li_out_last": int(lout[-1]),
                                     "slab_half_A": round(half, 3), "⚠": "기록만 — 판정 아님"}
        cols["Li_block_in_slab"] = lin
        cols["Li_slab_out"] = lout
    with open(out_csv, "w") as f:
        f.write(",".join(cols) + "\n")
        for i in range(len(frames)):
            f.write(",".join(f"{cols[c][i]:.3f}" if c == "t_ps" else str(int(cols[c][i])) for c in cols) + "\n")
    rec["csv"] = {"path": out_csv, "columns": list(cols)}
    Path(out_json).write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return rec


def md1_ensemble(seed_jsons, out_json, card=MD1_CARD):
    """시드 판독 셋 → 결합마다 앙상블 판정 (카드 문턱) · 관측창 한 줄. 출력이 이미 있으면 거부."""
    if os.path.exists(out_json):
        sys.exit(f"⛔ {out_json} 가 이미 있다 — 덮지 않는다")
    th = md1_load_card(card)
    a3 = md1_load_amend3(card)
    want_a3 = ({"key": MD1_AMEND3, "rule": a3} if a3 is not None else None)
    rs = [json.loads(Path(p).read_text(encoding="utf-8")) for p in seed_jsons]
    prob = []
    if len(rs) != th["n_seeds"]:
        prob.append(f"시드 판독 {len(rs)} 개 ≠ 카드 n_seeds {th['n_seeds']}")
    for p, r in zip(seed_jsons, rs):
        if r.get("schema") != "hyeokju_md1_seed_readout/v1":
            prob.append(f"{p}: 시드 판독 꼴이 아니다")
        elif not r["integrity"]["ok"]:
            prob.append(f"{p}: 무결성 {r['integrity']['problems']}")
        elif r.get("thresholds") != th:
            prob.append(f"{p}: 판독 때 문턱이 지금 카드와 다르다")
        elif r.get("amend3") != want_a3:
            prob.append(f"{p}: 시드 판독의 개정 3 규칙 ({r.get('amend3')}) 이 지금 카드 ({want_a3}) 와 다르다")
    shas = [r.get("traj", {}).get("sha256") for r in rs]
    if len(set(shas)) != len(shas):
        prob.append("같은 궤적이 두 번 들어왔다")
    out = {"schema": "hyeokju_md1_verdict/v1", "card": card, "amend": MD1_AMEND, "thresholds": th, "amend3": want_a3,
           "seeds": [{"json": p, "label": r.get("label"), "traj_sha256": r.get("traj", {}).get("sha256")} for p, r in zip(seed_jsons, rs)],
           "tool": {"path": os.path.relpath(os.path.abspath(__file__)), "sha256": _sha(__file__)}}
    if prob:
        out.update({"status": "판정 보류", "problems": prob})
    else:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
        from tools.sei.collect_neb import observation_window
        out["status"] = "판정"
        out["verdict"] = {}
        for A, B, _cut in th["pairs_judged"]:
            key = f"{A}-{B}"
            nk = "n_events_new" if a3 is not None else "n_events"       # 개정 3 active 면 생산 중 새로 든 쌍만 센다
            k = sum(1 for r in rs if r["pairs"][key][nk] > 0)
            v = md1_verdict_word(k, th)
            n_sites = min(rs[0]["pairs"][key]["n_A"], rs[0]["pairs"][key]["n_B"])
            ow = observation_window(th["T_K"], th["n_seeds"] * th["prod_ps"] * 1e-12, n_sites=n_sites)
            ent = {"seeds_with_event": k, "of": len(rs), "verdict": v, "counted": nk,
                   "first_onset_ps_per_seed": [r["pairs"][key]["first_onset_ps"] for r in rs],
                   "n_events_per_seed": [r["pairs"][key]["n_events"] for r in rs],
                   "obs_window": (ow["line"] if (ow and v != "개시 관측") else None),
                   "obs_window_n_sites_rule": "min(#A, #B) 원자 수 — 가정"}
            if a3 is not None:
                k2 = sum(1 for r in rs if r["pairs"][key]["n_events"] > 0)
                ent.update({"first_onset_new_ps_per_seed": [r["pairs"][key]["first_onset_new_ps"] for r in rs],
                            "n_events_new_per_seed": [r["pairs"][key]["n_events_new"] for r in rs],
                            "n_t0_pairs_per_seed": [r["pairs"][key]["n_t0_pairs"] for r in rs],
                            "record_amend2_seeds_with_event": k2, "record_amend2_verdict": md1_verdict_word(k2, th),
                            "⚠": "개정 3 — 판정은 생산 중 새로 문턱 안에 든 쌍만 센다 · record_amend2_* 는 t = 0 쌍까지 센 개정 2 셈 (기록만 · 판정 아님)"})
            out["verdict"][key] = ent
    Path(out_json).write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out


def md1_selftest():
    import tempfile
    from ase import Atoms
    res = []

    def chk(name, cond):
        res.append(bool(cond)); print(("  ✓ " if cond else "  ✗ ") + name)

    def refused(fn):
        try:
            fn()
        except SystemExit:
            return True
        return False

    T = tempfile.mkdtemp(prefix="md1_")
    th = {"pairs_judged": [["P", "O", 1.8], ["Zr", "S", 2.9]], "pairs_record": [["S", "O", 1.8]], "persist_ps": 1.0,
          "save_fs": 100, "prod_ps": 5.0, "T_K": 600, "T_band_K": 15, "n_seeds": 3, "onset_seeds_min": 2,
          "slab_elements": ["Li", "P", "S", "Cl"], "block_elements": ["Li", "Zr", "O"]}
    card = os.path.join(T, "card.json")
    Path(card).write_text(json.dumps({MD1_AMEND: {"상태": "active — 시험", "기계_판독_값": th}}, ensure_ascii=False))
    bad_card = os.path.join(T, "card_bad.json")
    Path(bad_card).write_text(json.dumps({MD1_AMEND: {"상태": "proposed", "기계_판독_값": th}}, ensure_ascii=False))
    # 원자: 슬랩 0 P · 1 S1 · 2 S2 · 3 Cl · 4 Li · 5 Li | 블록 6 Zr · 7 O1 · 8 O2 · 9 Li · 10 Li
    base = np.array([[5, 5, 5], [5, 5, 7.1], [5, 1.0, 5], [2, 2, 5], [1, 1, 4], [8, 8, 4],
                     [5, 5, 15], [5, 5, 17], [7, 7, 15], [1, 1, 15], [8, 8, 16]], float)
    syms = ["P", "S", "S", "Cl", "Li", "Li", "Zr", "O", "O", "Li", "Li"]
    freeze = os.path.join(T, "freeze.json"); Path(freeze).write_text(json.dumps([0, 1, 2, 3, 4, 5]))

    def make(name, n=51, mutate=None, Tval=600.0, events=True):
        fr = []
        for k in range(n):
            x = base.copy()
            if events:
                if 5 <= k <= 16:
                    x[7] = [3.6, 5, 5]               # P–O1 1.4 Å · 12 프레임 → 지속
                if 20 <= k <= 28:
                    x[8] = [5, 3.6, 5]               # P–O2 9 프레임 → 지속 아님
                if 32 <= k <= 41:
                    x[8] = [5, 6.4, 5]               # P–O2 딱 10 프레임 → 지속 (경계)
                if k in (0, 1, 2, 3, 4, 6, 7, 8, 9, 10):
                    x[6] = [5, 5, 9.6]               # Zr–S1 2.5 Å · 5 + 끊김 1 + 5 → 지속 아님 (끊김 허용 없음)
                if 12 <= k <= 25:
                    x[6] = [5, 8.5, 5]               # Zr–S2 주기 경계 너머 2.5 Å (그냥 거리 7.5) · 14 프레임 → 지속 (최소상)
                if 44 <= k <= 50:
                    x[7] = [5, 5, 8.5]               # S1–O1 1.4 Å · 7 프레임 · 기록 쌍
                if 30 <= k <= 40:
                    x[9] = [1, 1, 5.5]               # 블록 Li 가 슬랩 영역 안 (기록)
            a = Atoms(syms, positions=x, cell=[10, 10, 20], pbc=True)
            a.info["t_prod_ps"] = round(k * 0.1, 6)
            a.info["T_inst_K"] = Tval + (3.0 if k % 2 else -3.0)
            if mutate:
                mutate(k, a)
            fr.append(a)
        path = os.path.join(T, name + ".xyz")
        from ase.io import write as _w
        _w(path, fr, format="extxyz")
        return path

    good = make("good")
    r = md1_readout(good, freeze, "g", os.path.join(T, "g.json"), os.path.join(T, "g.csv"), card=card)
    po, zs, so = r["pairs"].get("P-O", {}), r["pairs"].get("Zr-S", {}), r["pairs"].get("S-O", {})
    chk("양성: 무결성 통과 (51 프레임 · 시각 · T 평균 600)", r["integrity"]["ok"])
    chk("양성: P–O 지속 사건 2 (12 프레임 · 딱 10 프레임) — 9 프레임 구간은 안 센다", po.get("n_events") == 2)
    chk("양성: P–O 첫 사건 0.5 ps · 최장 1.2 ps", po.get("first_onset_ps") == 0.5 and po.get("max_run_ps") == 1.2)
    chk("양성: Zr–S 지속 사건 1 — 주기 경계 너머 쌍 (최소상) 만 · 끊긴 5+5 구간은 안 센다",
        zs.get("n_events") == 1 and zs["events"][0]["start_ps"] == 1.2 and zs["events"][0]["dur_ps"] == 1.4)
    chk("양성: S–O 는 기록 쌍 (judged False) · 7 프레임이라 사건 0", so.get("judged") is False and so.get("n_events") == 0)
    chk("양성: Li 넘음 기록 — 블록 Li 1 개가 슬랩 영역 안 (최대 1)", r.get("li_crossing_record", {}).get("block_Li_in_slab_max") == 1)
    hdr = open(os.path.join(T, "g.csv")).readline().strip().split(",")
    chk("양성: CSV 열 (t_ps · PO · ZrS · SO 순간/지속 · Li 둘)",
        hdr == ["t_ps", "PO_inst", "PO_persist", "ZrS_inst", "ZrS_persist", "SO_inst", "SO_persist", "Li_block_in_slab", "Li_slab_out"])
    chk("⛔음성: 출력 파일이 있으면 덮지 않는다",
        refused(lambda: md1_readout(good, freeze, "g", os.path.join(T, "g.json"), os.path.join(T, "g2.csv"), card=card)))
    chk("⛔음성: 개정이 active 가 아니면 판독 안 함",
        refused(lambda: md1_readout(good, freeze, "x", os.path.join(T, "x.json"), os.path.join(T, "x.csv"), card=bad_card)))
    short = make("short", n=50)
    rs_ = md1_readout(short, freeze, "s", os.path.join(T, "s.json"), os.path.join(T, "s.csv"), card=card)
    chk("⛔음성: 프레임 수가 모자라면 무결성 실패 · 결합을 안 센다", (not rs_["integrity"]["ok"]) and rs_["pairs"] == {})

    def bad_t(k, a):
        if k == 10:
            a.info["t_prod_ps"] = 1.05
    rt = md1_readout(make("badt", mutate=bad_t), freeze, "t", os.path.join(T, "t.json"), os.path.join(T, "t.csv"), card=card)
    chk("⛔음성: 프레임 시각이 어긋나면 무결성 실패", not rt["integrity"]["ok"])
    rT = md1_readout(make("hot", Tval=640.0), freeze, "h", os.path.join(T, "h.json"), os.path.join(T, "h.csv"), card=card)
    chk("⛔음성: 생산 평균 T 가 600 ± 15 밖이면 무결성 실패", not rT["integrity"]["ok"])

    def nanpos(k, a):
        if k == 20:
            p = a.positions; p[0, 0] = np.nan; a.positions = p
    rn = md1_readout(make("nan", mutate=nanpos), freeze, "n", os.path.join(T, "n.json"), os.path.join(T, "n.csv"), card=card)
    chk("⛔음성: 좌표가 비유한이면 무결성 실패", not rn["integrity"]["ok"])

    def grow(k, a):
        if k == 30:
            a.set_cell([10, 10, 20.5], scale_atoms=False)
    rc = md1_readout(make("cell", mutate=grow), freeze, "c", os.path.join(T, "c.json"), os.path.join(T, "c.csv"), card=card)
    chk("⛔음성: 셀이 바뀌면 무결성 실패 (NVT)", not rc["integrity"]["ok"])
    fz2 = os.path.join(T, "freeze2.json"); Path(fz2).write_text(json.dumps([0, 1, 2, 3, 4, 5, 8]))
    ro = md1_readout(good, fz2, "o", os.path.join(T, "o.json"), os.path.join(T, "o.csv"), card=card)
    chk("⛔음성: O 가 슬랩 · 블록 양쪽에 있으면 (원소로 기원을 못 가르면) 무결성 실패", not ro["integrity"]["ok"])
    th_o = dict(th, slab_elements=th["slab_elements"] + ["O"])           # 원소 목록 문은 통과시키고 '양쪽' 문만 남긴다
    card_o = os.path.join(T, "card_o.json")
    Path(card_o).write_text(json.dumps({MD1_AMEND: {"상태": "active — 시험", "기계_판독_값": th_o}}, ensure_ascii=False))
    ro2 = md1_readout(good, fz2, "o2", os.path.join(T, "o2.json"), os.path.join(T, "o2.csv"), card=card_o)
    chk("⛔음성: (원소 목록은 허용해도) 판정 쌍 원소가 슬랩 · 블록 양쪽에 있으면 무결성 실패",
        (not ro2["integrity"]["ok"]) and any("양쪽" in x for x in ro2["integrity"]["problems"]))
    # 앙상블
    q1 = md1_readout(make("q1", Tval=602.0), freeze, "q1", os.path.join(T, "q1.json"), os.path.join(T, "q1.csv"), card=card)
    q0a = md1_readout(make("q0a", events=False), freeze, "q0a", os.path.join(T, "q0a.json"), os.path.join(T, "q0a.csv"), card=card)
    q0b = md1_readout(make("q0b", events=False, Tval=601.0), freeze, "q0b", os.path.join(T, "q0b.json"), os.path.join(T, "q0b.csv"), card=card)
    q0c = md1_readout(make("q0c", events=False, Tval=599.0), freeze, "q0c", os.path.join(T, "q0c.json"), os.path.join(T, "q0c.csv"), card=card)
    J = lambda n: os.path.join(T, n + ".json")
    e2 = md1_ensemble([J("g"), J("q1"), J("q0a")], os.path.join(T, "e2.json"), card=card)
    chk("양성: 사건 시드 2/3 → '개시 관측' (P–O · Zr–S 둘 다) · 관측창 줄 없음",
        e2.get("status") == "판정" and all(e2["verdict"][k]["verdict"] == "개시 관측" and e2["verdict"][k]["obs_window"] is None for k in ("P-O", "Zr-S")))
    e1 = md1_ensemble([J("g"), J("q0a"), J("q0b")], os.path.join(T, "e1.json"), card=card)
    chk("양성: 사건 시드 1/3 → '시드 하나에서만' (개시 관측이 아니다)", e1["verdict"]["P-O"]["verdict"] == "시드 하나에서만")
    e0 = md1_ensemble([J("q0a"), J("q0b"), J("q0c")], os.path.join(T, "e0.json"), card=card)
    chk("양성: 사건 시드 0/3 → '관측창 안 개시 없음' + 관측창 한 줄 (반응 기회 = min(#A, #B))",
        e0["verdict"]["P-O"]["verdict"] == "관측창 안 개시 없음" and "반응 기회" not in (e0["verdict"]["P-O"]["obs_window"] or "x")
        and e0["verdict"]["Zr-S"]["obs_window"] and "eV" in e0["verdict"]["Zr-S"]["obs_window"])
    eb = md1_ensemble([J("g"), J("q1")], os.path.join(T, "eb.json"), card=card)
    chk("⛔음성: 시드 수가 카드와 다르면 판정 보류", eb.get("status") == "판정 보류")
    ed = md1_ensemble([J("g"), J("g"), J("q0a")], os.path.join(T, "ed.json"), card=card)
    chk("⛔음성: 같은 궤적이 두 번 들어오면 판정 보류", ed.get("status") == "판정 보류")
    ei = md1_ensemble([J("g"), J("q1"), J("s")], os.path.join(T, "ei.json"), card=card)
    chk("⛔음성: 무결성 실패 시드가 섞이면 판정 보류", ei.get("status") == "판정 보류")
    chk("⛔음성: 앙상블 출력이 있으면 덮지 않는다",
        refused(lambda: md1_ensemble([J("g"), J("q1"), J("q0a")], os.path.join(T, "e2.json"), card=card)))
    # ── 개정 3 (t = 0 쌍 빼기 · 2026-11-22) ──
    a3rule = {"judge_excludes_t0_pairs": True, "t0_frame": 0}

    def card_with(state, rule):
        pth = os.path.join(T, f"card3_{len(os.listdir(T))}.json")
        Path(pth).write_text(json.dumps({MD1_AMEND: {"상태": "active — 시험", "기계_판독_값": th},
                                         MD1_AMEND3: {"상태": state, "기계_판독_값": rule}}, ensure_ascii=False))
        return pth
    card3 = card_with("active — 시험", a3rule)
    card3p = card_with("proposed", a3rule)
    card3x = card_with("active — 시험", {"judge_excludes_t0_pairs": False, "t0_frame": 0})

    def t0mut(k, a):
        p = a.positions
        if k <= 14 or 30 <= k <= 41:
            p[7] = [3.6, 5, 5]               # P–O1 1.4 Å — t = 0 부터 15 프레임 (지속) · 끊겼다 30–41 다시 12 프레임 (지속)
        if 12 <= k <= 25:
            p[6] = [5, 8.5, 5]               # Zr–S2 주기 경계 너머 2.5 Å · 12–25 (생산 중 새로 · 지속)
        a.positions = p

    def t0only(k, a):
        p = a.positions
        if k <= 14:
            p[7] = [3.6, 5, 5]               # P–O1 — t = 0 부터만 (새 쌍 없음)
        a.positions = p
    t0p = make("t0", events=False, mutate=t0mut)
    r3 = md1_readout(t0p, freeze, "t3", J("t3"), os.path.join(T, "t3.csv"), card=card3)
    po3, zs3 = r3["pairs"].get("P-O", {}), r3["pairs"].get("Zr-S", {})
    chk("양성 (개정 3): t = 0 부터 붙은 P–O1 — 개정 2 셈 사건 2 · 새 쌍 셈 0 (끊겼다 다시 붙어도 그 쌍은 안 센다) · t0 쌍 [P 0 · O 7]",
        po3.get("n_events") == 2 and po3.get("n_events_new") == 0 and po3.get("n_t0_pairs") == 1 and po3.get("t0_pairs") == [[0, 7]])
    chk("양성 (개정 3): 생산 중 새로 붙은 Zr–S2 — 새 쌍 사건 1 · 첫 1.2 ps · t0 쌍 0",
        zs3.get("n_events_new") == 1 and zs3.get("first_onset_new_ps") == 1.2 and zs3.get("n_t0_pairs") == 0)
    hdr3 = open(os.path.join(T, "t3.csv")).readline().strip().split(",")
    chk("양성 (개정 3): CSV 에 _persist_new 열 (판정 · 기록 쌍마다) · 시드 판독에 개정 3 규칙",
        all(f"{x}_persist_new" in hdr3 for x in ("PO", "ZrS", "SO")) and r3.get("amend3") == {"key": MD1_AMEND3, "rule": a3rule})
    chk("양성: 카드에 개정 3 이 없으면 출력에 개정 3 열쇠가 없다 (옛 판정 · 옛 CSV 그대로)",
        "amend3" not in r and "n_events_new" not in po and not any(h.endswith("_persist_new") for h in hdr))
    chk("⛔음성: 개정 3 이 카드에 있는데 active 가 아니면 판독 안 함",
        refused(lambda: md1_readout(t0p, freeze, "t3p", J("t3p"), os.path.join(T, "t3p.csv"), card=card3p)))
    chk("⛔음성: 개정 3 규칙 열쇠가 어긋나면 (judge_excludes_t0_pairs ≠ true) 판독 안 함",
        refused(lambda: md1_readout(t0p, freeze, "t3x", J("t3x"), os.path.join(T, "t3x.csv"), card=card3x)))
    md1_readout(make("t0b", events=False, Tval=601.0, mutate=t0only), freeze, "t0b3", J("t0b3"), os.path.join(T, "t0b3.csv"), card=card3)
    md1_readout(os.path.join(T, "q0a.xyz"), freeze, "q0a3", J("q0a3"), os.path.join(T, "q0a3.csv"), card=card3)
    e3 = md1_ensemble([J("t3"), J("t0b3"), J("q0a3")], os.path.join(T, "e3.json"), card=card3)
    chk("양성 (개정 3): t = 0 쌍 사건만 있는 시드 2 → P–O '관측창 안 개시 없음' + 관측창 줄 · 기록 (개정 2 셈) 은 '개시 관측' · Zr–S 새 쌍 1 시드 → '시드 하나에서만'",
        e3.get("status") == "판정" and e3["verdict"]["P-O"]["verdict"] == "관측창 안 개시 없음" and e3["verdict"]["P-O"]["obs_window"]
        and e3["verdict"]["P-O"]["record_amend2_verdict"] == "개시 관측" and e3["verdict"]["P-O"]["counted"] == "n_events_new"
        and e3["verdict"]["Zr-S"]["verdict"] == "시드 하나에서만")
    md1_readout(good, freeze, "g3", J("g3"), os.path.join(T, "g3.csv"), card=card3)
    md1_readout(os.path.join(T, "q1.xyz"), freeze, "q13", J("q13"), os.path.join(T, "q13.csv"), card=card3)
    e3p = md1_ensemble([J("g3"), J("q13"), J("q0a3")], os.path.join(T, "e3p.json"), card=card3)
    chk("양성 (개정 3): 생산 중 새로 든 쌍이 시드 2 에 있으면 '개시 관측' (P–O · Zr–S — good 의 t = 0 Zr–S1 쌍은 빼고도)",
        e3p.get("status") == "판정" and all(e3p["verdict"][x]["verdict"] == "개시 관측" for x in ("P-O", "Zr-S")))
    def no_crash(fn):                        # 예외로 죽으면 '보류' 가 아니라 시험 실패로 센다 (KeyError 로 우연히 막히는 것과 가른다)
        try:
            return fn()
        except SystemExit:
            raise
        except Exception as e:
            return {"status": f"예외 {type(e).__name__}"}
    em = no_crash(lambda: md1_ensemble([J("g"), J("q1"), J("q0a")], os.path.join(T, "em.json"), card=card3))
    chk("⛔음성: 카드는 개정 3 active 인데 시드 판독이 개정 3 없이 만들어졌으면 판정 보류 (예외 아님)",
        em.get("status") == "판정 보류" and any("개정 3" in x for x in em.get("problems", [])))
    er = no_crash(lambda: md1_ensemble([J("t3"), J("t0b3"), J("q0a3")], os.path.join(T, "er.json"), card=card))
    chk("⛔음성: 시드 판독은 개정 3 인데 카드에 개정 3 이 없으면 판정 보류", er.get("status") == "판정 보류")
    chk("⛔음성: 카드의 개정 3 이 active 가 아니면 앙상블도 거부",
        refused(lambda: md1_ensemble([J("t3"), J("t0b3"), J("q0a3")], os.path.join(T, "e3pp.json"), card=card3p)))
    n_bad = len(res) - sum(res)
    print(f"md1 selftest: {sum(res)} 통과 / {n_bad} 실패")
    return 0 if n_bad == 0 else 1


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        return md1_selftest()
    if "--md1" in argv or "--md1_ensemble" in argv:
        ap = argparse.ArgumentParser(description="[혁주] MD-1 판독")
        ap.add_argument("--md1", help="시드 하나의 생산 궤적 (extxyz)")
        ap.add_argument("--freeze", help="담금질 때 고정한 슬랩 인덱스 JSON (슬랩 = 고정 원자)")
        ap.add_argument("--label")
        ap.add_argument("--md1_ensemble", nargs="+")
        ap.add_argument("--card", default=MD1_CARD)
        ap.add_argument("--out_json", required=True)
        ap.add_argument("--out_csv")
        a = ap.parse_args(argv)
        if a.md1_ensemble:
            out = md1_ensemble(a.md1_ensemble, a.out_json, card=a.card)
            print(f"  앙상블 {out['status']}" + ("" if out["status"] == "판정" else f" — {out['problems']}"))
            for k, v in (out.get("verdict") or {}).items():
                if "record_amend2_verdict" in v:          # 개정 3 — 판정은 새 쌍 · t = 0 쌍까지 센 셈은 기록
                    print(f"  {k}: 새 쌍 사건 시드 {v['seeds_with_event']}/{v['of']} → {v['verdict']} · 새 쌍 첫 사건 (ps) {v['first_onset_new_ps_per_seed']}"
                          f" · t=0 쌍 {v['n_t0_pairs_per_seed']} · (기록) t=0 쌍 포함 셈 {v['record_amend2_seeds_with_event']}/{v['of']}"
                          + (f" · {v['obs_window']}" if v["obs_window"] else ""))
                else:
                    print(f"  {k}: 사건 시드 {v['seeds_with_event']}/{v['of']} → {v['verdict']} · 첫 사건 (ps) {v['first_onset_ps_per_seed']}"
                          + (f" · {v['obs_window']}" if v["obs_window"] else ""))
            print(f"→ {a.out_json}")
            return 0 if out["status"] == "판정" else 3
        if not (a.freeze and a.label and a.out_csv):
            ap.error("--md1 에는 --freeze · --label · --out_csv 가 필요하다")
        r = md1_readout(a.md1, a.freeze, a.label, a.out_json, a.out_csv, card=a.card)
        print(f"  [{a.label}] 무결성 {'통과' if r['integrity']['ok'] else '실패 ' + str(r['integrity']['problems'])} · 생산 평균 T {r['integrity']['T_prod_mean_K']}")
        for k, v in r["pairs"].items():
            print(f"  {k} ({'판정' if v['judged'] else '기록'} · < {v['cut_A']} Å): 지속 사건 {v['n_events']} · 첫 {v['first_onset_ps']} ps · 최장 {v['max_run_ps']} ps · 순간 최대 {v['inst_max']}"
                  + (f" · t=0 쌍 {v['n_t0_pairs']} · 새 쌍 지속 사건 {v['n_events_new']} · 새 쌍 첫 {v['first_onset_new_ps']} ps" if "n_events_new" in v else ""))
        print(f"→ {a.out_json} · {a.out_csv}")
        return 0 if r["integrity"]["ok"] else 3
    return legacy_main(argv)


if __name__ == "__main__":
    sys.exit(main())
