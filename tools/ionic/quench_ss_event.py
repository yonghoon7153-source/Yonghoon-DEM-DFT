#!/usr/bin/env python3
"""quench_ss_event.py — 담금질 궤적(traj.xyz + thermo.csv)에서 **S–S 근접 사건**을 프레임별로 추적한다.

왜 (회신 CC · 2026-09-26 · 외부 1저자 Q9): seed5 의 final 에서 PS₄ 하나가 깨지고 S–S 2.03 Å 가 남았다.
  *"먼저 그 S–S 가 무엇인지 확인하세요 — 담금질 궤적에서 언제 생겼는지(고온 구간인지 냉각 말미인지),
   끝까지 유지되는지, 4배위를 잃은 P 가 PS₃ 인지 다리를 공유하는 형태인지."* 궤적이 있으니 비용 ≈ 0.

무엇을 재나 (프레임마다)
  · 최단 S–S 거리(최소상) 와 그 쌍 · 쌍의 두 S 가 P 에 결합돼 있는지(R_PS 2.6 Å · melt_quench_uma.indicators 와 같은 컷)
    → 형태 (쌍의 두 S 가 각각 P 에 붙어 있는가로만 가른다): `P-S-S-P`(둘 다 = 과황화 다리) · `P-S-S`(한쪽만 = 말단 과황화,
      P–S–S) · `S-S_free`(둘 다 P 없음 = 떨어져 나온 S₂) · `none`(컷 위). PS₃ 가 생겼는지는 별도 열 `P_not_4coord` 로 본다 —
      seed5 의 질문("4배위를 잃은 P 가 PS₃ 인지 다리를 공유하는 형태인지")은 이 둘을 같이 읽어야 답이 된다.
  · PS₄ 보존율 · P–S 배위 분포 · 다리 S(P 2개 이상에 붙은 S) · 4배위 아닌 P 목록  (전부 indicators 재사용)
  · 온도: thermo.csv 의 T_K(순간) · T_set_K(설정) — 프레임 ↔ thermo 행 대응은 frame_index_map 규칙(개수 같아야 함)
사건 판정
  · onset = 최단 S–S 가 --ss_cut(기본 2.30 Å) 아래로 **처음** 들어간 프레임 · 그때의 쌍을 고정하고 이후 프레임에서
    **같은 쌍**의 거리를 추적 → 지속 분율 · 마지막 프레임 유지 여부 · 쌍이 바뀐 횟수
  · 구간 라벨: T_set 이 최고값이면 `melt_hold` · 최저값이면 `final_hold` · 그 사이면 `quench`

⛔ 이 도구가 **못 하는 것**
  · 결합인지 판정하지 않는다 — 거리 기준이다 (2.30 Å 는 S–S 공유결합 2.03–2.10 과 비결합 최근접 ≥ 3.3 사이의 창).
    전자구조(결합 차수)는 안 본다. 보고에는 "거리 2.03 Å" 로만 쓴다 (회신 CC).
  · 게이트를 판정하지 않는다 — 판정은 외부 1저자 몫. 개수·시각·형태를 옮길 뿐이다.
  · thermo 행 수와 프레임 수가 다르면 시간축을 **plan.json 의 save_ps 로 가정**하고 그 사실을 기록한다(조용히 넘어가지 않는다).
  · 저장 간격(save_ps) 사이의 사건은 못 본다.

--trace_S — **특정 S 원자의 내력** (회신 CH · 2026-09-28 · 외부 1저자)
  *"S54 의 내력을 세어 주세요. S54 가 처음부터 자유 S 였는지, 냉각 중 어딘가에서 떨어져 나온 것인지에 따라
   이 관측의 의미가 달라집니다. 후자라면 '끊김 두 건이 만나 P–S–S 가 됐다' 는 경로가 되고, 그건 기계화학
   종 생성과 훨씬 가까운 그림입니다."*
  프레임마다 그 S 의 P 이웃(R_PS 컷) · 최근접 P 거리 · 최근접 S 짝을 찍고, 붙었다/떨어졌다 전이를
  구간 라벨과 함께 센다. 판정은 세 갈래로만 나온다 —
    `처음부터_자유` (프레임 0 에서 P 없음 **그리고** 끝까지 한 번도 안 붙음) ·
    `이탈` (붙어 있다가 떨어져 마지막 프레임에 자유) · `붙어있음` (마지막 프레임에 P 에 붙어 있음).
  ⛔ 이 갈래는 **거리 컷 판정**이다 — 결합 차수를 안 본다. 그리고 첫 프레임이 이미 용융이면
  *"처음부터 자유"* 는 **담금질 시작 시점** 얘기지 조성 설계 얘기가 아니다 (그 구분을 `first_frame_segment` 로 같이 찍는다).

--s_census — **48 S 전수 소속-이동 조사** (회신 CH 후속 · 2026-09-28)
  `PS₄ 보존율` 은 P 의 **배위수**를 세고 그 넷이 **원래 그 P 의 S 인지는 안 본다** — seed5 실측에서
  P50·P55 가 끝까지 4배위인 채 남의 S 를 하나씩 물고 있었고(S3 ← P0 · S8 ← P5), P30 은 4배위였던
  구간에 원래 S 가 둘뿐이었다. 그래서 **정체**를 따로 센다: S 마다 프레임 0 의 주인 P 와 마지막
  프레임의 주인 P, 주인이 바뀐 횟수·시각, P 별 '남의 S' 수.
  ⛔ 못 하는 것: 거리 컷 판정이다 · 저장 간격 사이의 교환은 못 본다 · 다리 S(두 P 동시)는
  주인 집합이 둘인 상태로 세고 별도 갈래로 만들지 않는다.
  ⛔ (2026-09-28 seed3 실측) 기준이 **첫 저장 프레임**이다 — 그 프레임이 이미 용융(1200 K)이면 늘어난
  P–S 가 컷 밖으로 나가 '프레임 0 자유' 로 찍히고, 다음 프레임에 제 P 로 돌아오면 **'[] → P 이동'** 으로 센다
  (seed3 S49 → P45 · 실제로는 P45 자기 S). '남의 S' 목록에도 오른다. 정체 온전율은 영향 없다 (프레임 0
  자유 S 는 원래 집합·분모에서 빠진다). 설계 기준(초기 구조)으로 고치려면 --ref_xyz 가 필요하다 — **미구현**.
  ⛔ '이동' 은 주인 **집합** 비교라 원래 P 에 붙은 채 두 번째 P 를 얻는 **다리 형성**도 이동으로 센다
  (seed3 S54 {P50} → {P35, P50}). 정체 온전율은 소속(∈)으로 봐서 원래 P 가 그 S 를 지킨 것으로 센다.

사용
  python3 tools/ionic/quench_ss_event.py <run_dir> [--ss_cut 2.30] [--stride 1] [--table 50] [--out JSON] [--tools_dir DIR]
  python3 tools/ionic/quench_ss_event.py <run_dir> --s_census                # 48 S 전수 소속-이동
  python3 tools/ionic/quench_ss_event.py <run_dir> --trace_S 54 59      # 특정 S 내력 (전역 원자 index)
  python3 tools/ionic/quench_ss_event.py --selftest
"""
import argparse
import json
import math
import os
import pathlib
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SS_CUT = 2.30


def _load_mq(tools_dir=None):
    """melt_quench_uma 의 indicators · mic_dists · read_thermo · R_PS 를 빌린다 (컷오프를 여기 복사하지 않는다)."""
    d = tools_dir or HERE
    if d not in sys.path:
        sys.path.insert(0, d)
    import melt_quench_uma as mq  # noqa: E402
    return mq


def trace_frame(sym, pos, cell, mq, trace):
    """trace 의 각 전역 원자 index 에 대해 프레임 하나의 P 이웃·최근접 P·최근접 S 를 낸다.
    ⛔ index 가 S 가 아니면 죽는다 (조용히 다른 원소를 재지 않는다)."""
    sym = np.asarray(sym); pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    iP = np.where(sym == "P")[0]; iS = np.where(sym == "S")[0]
    out = {}
    for g in trace:
        if g < 0 or g >= len(sym):
            raise ValueError(f"⛔ --trace_S {g} 가 원자 수 {len(sym)} 밖이다")
        if sym[g] != "S":
            raise ValueError(f"⛔ --trace_S {g} 는 S 가 아니라 {sym[g]} 다 — 다른 원소를 S 로 세지 않는다")
        rec = {"P_neighbors": [], "d_nearest_P_A": None, "nearest_S": None, "d_nearest_S_A": None}
        if len(iP):
            dP = mq.mic_dists(pos[[g]], pos[iP], cell)[0]
            rec["P_neighbors"] = [int(iP[k]) for k in np.where(dP <= mq.R_PS)[0]]
            rec["d_nearest_P_A"] = round(float(dP.min()), 4)
        others = iS[iS != g]
        if len(others):
            dS = mq.mic_dists(pos[[g]], pos[others], cell)[0]
            k = int(np.argmin(dS))
            rec["nearest_S"] = int(others[k]); rec["d_nearest_S_A"] = round(float(dS[k]), 4)
        rec["bonded"] = len(rec["P_neighbors"]) > 0
        out[str(g)] = rec
    return out


def s_trace_stats(rows, trace):
    """trace 한 S 마다 붙음/떨어짐 내력. 판정은 세 갈래 (docstring --trace_S 참조).
    ⛔ 못 하는 것: 거리 컷 판정이다 · 저장 간격 사이의 이탈·재결합은 못 본다 ·
       '처음부터 자유' 는 **첫 저장 프레임** 기준이다 (그 구간 라벨을 같이 찍는다)."""
    out = {}
    for g in trace:
        key = str(g)
        seq = [(r, (r.get("S_trace") or {}).get(key)) for r in rows]
        seq = [(r, t) for r, t in seq if t is not None]
        if not seq:
            out[key] = {"verdict": "자료없음", "note": "이 원자에 대한 프레임 기록이 없다"}
            continue
        first_r, first_t = seq[0]
        last_r, last_t = seq[-1]
        by_seg, partners, ev = {}, {}, []
        n_bonded = 0
        prev = None
        for r, t in seq:
            s = r.get("segment") or "unknown"
            g_ = by_seg.setdefault(s, {"frames": 0, "frames_bonded": 0})
            g_["frames"] += 1
            if t["bonded"]:
                g_["frames_bonded"] += 1; n_bonded += 1
                for pp in t["P_neighbors"]:
                    partners[str(pp)] = partners.get(str(pp), 0) + 1
            if prev is not None and t["bonded"] != prev:
                ev.append({"kind": "재결합" if t["bonded"] else "이탈", "frame": r.get("frame"), "t_ps": r.get("t_ps"),
                           "T_K": r.get("T_K"), "T_set_K": r.get("T_set_K"), "segment": s,
                           "P_neighbors": list(t["P_neighbors"]), "d_nearest_P_A": t["d_nearest_P_A"]})
            prev = t["bonded"]
        for v in by_seg.values():
            v["fraction_bonded"] = round(v["frames_bonded"] / v["frames"], 4) if v["frames"] else None
        if last_t["bonded"]:
            verdict = "붙어있음"
        elif n_bonded == 0:
            verdict = "처음부터_자유"
        else:
            verdict = "이탈"
        out[key] = {"verdict": verdict,
                    "first_frame_bonded": bool(first_t["bonded"]), "first_frame": first_r.get("frame"),
                    "first_frame_segment": first_r.get("segment"), "first_frame_T_set_K": first_r.get("T_set_K"),
                    "first_frame_P_neighbors": list(first_t["P_neighbors"]), "first_frame_d_nearest_P_A": first_t["d_nearest_P_A"],
                    "last_frame_bonded": bool(last_t["bonded"]), "last_frame_d_nearest_P_A": last_t["d_nearest_P_A"],
                    "last_frame_nearest_S": last_t["nearest_S"], "last_frame_d_nearest_S_A": last_t["d_nearest_S_A"],
                    "frames_total": len(seq), "frames_bonded": n_bonded,
                    "by_segment": by_seg, "P_partner_frames": partners,
                    "transitions": ev, "n_detach": sum(1 for e in ev if e["kind"] == "이탈"),
                    "n_reattach": sum(1 for e in ev if e["kind"] == "재결합"),
                    "first_detach": next((e for e in ev if e["kind"] == "이탈"), None)}
    return {"trace": list(trace), "per_S": out,
            "note": "거리 컷 R_PS 기준 · 저장 간격 사이 사건은 못 봄 · '처음부터_자유' 는 첫 저장 프레임 기준(구간 라벨 병기)"}


def census_frame(sym, pos, cell, mq):
    """프레임 하나의 S → 주인 P 집합 (R_PS 컷). 다리 S 는 집합 크기가 2 이상으로 나온다."""
    sym = np.asarray(sym); pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    iP = np.where(sym == "P")[0]; iS = np.where(sym == "S")[0]
    if not len(iS):
        return {}
    if not len(iP):
        return {int(s): () for s in iS}
    D = mq.mic_dists(pos[iP], pos[iS], cell)            # (nP, nS)
    return {int(iS[c]): tuple(int(iP[r]) for r in np.where(D[:, c] <= mq.R_PS)[0]) for c in range(len(iS))}


def s_census_summary(hist, n_frames):
    """hist[s] = [(frame, t_ps, T_set_K, segment, owners), ...] — 바뀐 프레임만 (첫 프레임 포함).
    ⛔ '이동' 은 **첫 프레임 주인 집합 ≠ 마지막 프레임 주인 집합** 이다 (일시 이탈 후 복귀는 이동이 아니다).
       일시 변화는 `n_changes` 로 따로 센다 — 둘을 섞지 않는다."""
    if not hist:
        return {"n_S": 0, "note": "S 가 없다"}
    first = {s: v[0][4] for s, v in hist.items()}
    last = {s: v[-1][4] for s, v in hist.items()}
    movers, transient_only, free_end, foreign = [], [], [], {}
    for s in sorted(hist):
        f, l = first[s], last[s]
        n_ch = len(hist[s]) - 1
        if not l:
            free_end.append(s)
        if set(f) != set(l):
            movers.append({"S": s, "from_P": list(f), "to_P": list(l), "n_changes": n_ch,
                           "changes": [{"frame": c[0], "t_ps": c[1], "T_set_K": c[2], "segment": c[3], "owners": list(c[4])}
                                       for c in hist[s][1:]]})
        elif n_ch:
            transient_only.append({"S": s, "P": list(f), "n_changes": n_ch})
        for p in l:
            if p not in f:
                foreign.setdefault(str(p), []).append(s)
    # ── 정체 기준 온전율 (배위 기준 PS₄ 보존율과 **다른 양**이다) ──
    orig = {}                                  # P → 프레임 0 에 그 P 것이던 S 집합
    free0 = [s for s in sorted(hist) if not first[s]]
    for s in sorted(hist):
        for pp in first[s]:
            orig.setdefault(int(pp), []).append(s)
    intact, broken = [], []
    for pp, ss in sorted(orig.items()):
        lost = [s for s in ss if pp not in last[s]]
        (intact if not lost else broken).append({"P": pp, "original_S": ss, "lost_S": lost} if lost else {"P": pp, "original_S": ss})
    kept = [s for s in sorted(hist) if first[s] and set(first[s]) == set(last[s])]
    n_own0 = len(hist) - len(free0)
    identity = {
        "⛔_배위_보존율과_다른_양이다": "PS₄ 보존율은 P 의 **4배위**를 세고 그 넷이 원래 그 P 의 S 인지는 안 본다. 아래는 **정체**다.",
        "n_P": len(orig), "n_P_all_original_S_kept": len(intact),
        "fraction_P_all_original_S_kept": round(len(intact) / len(orig), 4) if orig else None,
        "P_broken": broken,
        "n_S_with_owner_at_frame0": n_own0, "n_S_free_at_frame0": len(free0), "S_free_at_frame0": free0,
        "n_S_kept_original_owner": len(kept),
        "fraction_S_kept_original_owner": round(len(kept) / n_own0, 4) if n_own0 else None,
        "note": "'온전' = 프레임 0 에 그 P 것이던 S **전부**가 마지막 프레임에도 그 P 에 있다. "
                "**남의 S 를 받은 것은 온전성을 깨지 않는다** (배위수만 늘 뿐이다).",
    }
    return {"n_S": len(hist), "n_frames_scanned": n_frames, "identity": identity,
            "n_moved": len(movers), "n_transient_only": len(transient_only),
            "n_free_at_last_frame": len(free_end), "free_at_last_frame": free_end,
            "moved": movers, "transient_only": transient_only,
            "foreign_S_per_P_at_last_frame": {k: sorted(v) for k, v in sorted(foreign.items())},
            "note": "'이동' = 첫 프레임 주인 ≠ 마지막 프레임 주인 · 일시 이탈 후 복귀는 transient_only · "
                    "거리 컷 R_PS 기준 · 저장 간격 사이 교환은 못 봄 · 다리 S 는 주인 집합 크기 ≥ 2 로 나온다"}


def frame_stats(sym, pos, cell, mq, ss_cut=SS_CUT):
    sym = np.asarray(sym); pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    ind = mq.indicators(sym, pos, cell)
    iS = np.where(sym == "S")[0]; iP = np.where(sym == "P")[0]
    out = {"PS4_fraction": ind.get("PS4_fraction"), "P_S_coord_hist": ind.get("P_S_coord_hist"),
           "bridging_S": ind.get("bridging_S_P2S7_like"), "P_P_bonds": ind.get("P_P_bonds_P2S6_like")}
    if len(iS) < 2:
        out.update({"ss_min_A": None, "ss_pair": None, "ss_kind": "n/a"})
        return out
    D = mq.mic_dists(pos[iS], pos[iS], cell); np.fill_diagonal(D, np.inf)
    a, b = np.unravel_index(int(np.argmin(D)), D.shape)
    dmin = float(D[a, b]); i, j = int(iS[a]), int(iS[b])
    pair = (min(i, j), max(i, j))
    kind = "none"
    p_of = {}
    if len(iP):
        DPS = mq.mic_dists(pos[iP], pos[iS], cell)          # (nP, nS)
        nS_per_P = (DPS <= mq.R_PS).sum(axis=1)
        out["P_not_4coord"] = [[int(iP[k]), int(n)] for k, n in enumerate(nS_per_P) if n != 4]
        for s_loc, s_glob in ((a, i), (b, j)):
            p_of[s_glob] = [int(iP[k]) for k in np.where(DPS[:, s_loc] <= mq.R_PS)[0]]
        if dmin < ss_cut:
            has = [len(p_of[i]) > 0, len(p_of[j]) > 0]
            kind = "P-S-S-P" if all(has) else ("P-S-S" if any(has) else "S-S_free")
    else:
        out["P_not_4coord"] = []
        if dmin < ss_cut:
            kind = "S-S_free"
    out.update({"ss_min_A": round(dmin, 4), "ss_pair": list(pair), "ss_kind": kind,
                "ss_pair_P_neighbors": {str(k): v for k, v in p_of.items()}})
    return out


def _segment(tset, tmax, tmin, tol=1.0):
    if tset is None:
        return "unknown"
    if abs(tset - tmax) <= tol:
        return "melt_hold"
    if abs(tset - tmin) <= tol:
        return "final_hold"
    return "quench"


def p_coord_stats(rows):
    """4 배위를 벗어난 P 의 통계 (회신 CD 새 항목 1 · 2026-09-27 — *"다른 네 시드의 궤적에서도 같은 통계를"*).
    구간별 '이탈 P 가 하나라도 있는 프레임' 분율 · P 별 이탈 프레임 수(구간별)·배위값·이탈 횟수·처음 이탈·끝까지 이탈했나·회복 시점.
    ⛔ 못 하는 것: 배위는 거리 컷(R_PS) 기준이다 — 결합 차수·전자구조가 아니다 · 저장 간격 사이의 끊김/회복은 못 본다 ·
       '회복' 은 마지막 이탈 다음 **저장 프레임**이다 (실제 회복 시각은 그 사이 어딘가)."""
    seg, perP, maxsim, prev = {}, {}, 0, set()
    for i, r in enumerate(rows):
        s = r.get("segment") or "unknown"
        g = seg.setdefault(s, {"frames": 0, "frames_any_not4": 0})
        g["frames"] += 1
        bad = [(int(p), int(n)) for p, n in (r.get("P_not_4coord") or [])]
        if bad:
            g["frames_any_not4"] += 1
        maxsim = max(maxsim, len(bad))
        cur = set()
        for p, n in bad:
            cur.add(p)
            q = perP.setdefault(p, {"frames_not4": 0, "by_segment": {}, "coord_values": {}, "episodes": 0, "first": None, "last": None, "_i": None})
            q["frames_not4"] += 1
            q["by_segment"][s] = q["by_segment"].get(s, 0) + 1
            q["coord_values"][str(n)] = q["coord_values"].get(str(n), 0) + 1
            if p not in prev:
                q["episodes"] += 1
            pt = {"frame": r.get("frame"), "t_ps": r.get("t_ps"), "T_set_K": r.get("T_set_K"), "segment": s}
            if q["first"] is None:
                q["first"] = pt
            q["last"] = pt; q["_i"] = i
        prev = cur
    last_bad = {int(p) for p, _ in (rows[-1].get("P_not_4coord") or [])} if rows else set()
    for p, q in perP.items():
        q["in_last_frame"] = p in last_bad
        i = q.pop("_i")
        nx = rows[i + 1] if (not q["in_last_frame"] and i is not None and i + 1 < len(rows)) else None
        q["recovered_at"] = {"frame": nx.get("frame"), "t_ps": nx.get("t_ps"), "T_set_K": nx.get("T_set_K"), "segment": nx.get("segment") or "unknown"} if nx else None
    for g in seg.values():
        g["fraction_any_not4"] = round(g["frames_any_not4"] / g["frames"], 4) if g["frames"] else None
    return {"by_segment": seg, "per_P": {str(k): v for k, v in sorted(perP.items())}, "n_P_ever_not4": len(perP),
            "n_P_not4_last_frame": len(last_bad), "max_simultaneous_not4": maxsim,
            "note": "거리 컷 R_PS 기준 배위 · 저장 간격 사이 사건은 못 봄 · '회복' = 마지막 이탈 다음 저장 프레임"}


def analyze(run_dir, mq, ss_cut=SS_CUT, stride=1, log=print, trace_S=None, census=False):
    from ase.io import iread
    run = pathlib.Path(run_dir)
    traj, thermo = run / "traj.xyz", run / "thermo.csv"
    if not traj.exists():
        raise FileNotFoundError(f"{traj} 가 없다 — 궤적 없이는 못 잰다")
    t_axis, T_K, T_set, axis_note = None, None, None, ""
    try:
        imap, n_traj = mq.frame_index_map(traj, thermo)
        th = mq.read_thermo(thermo)
        t_axis = [float(x) for x in th["t_ps"]]
        T_K = [float(x) for x in th["T_K"]] if "T_K" in th else None
        T_set = [float(x) for x in th["T_set_K"]] if "T_set_K" in th else None
        axis_note = f"thermo.csv 행 {n_traj} = 프레임 {n_traj} (frame_index_map)"
    except (ValueError, FileNotFoundError, KeyError) as e:
        n_traj = sum(1 for _ in iread(str(traj), index=":", format="extxyz"))
        save_ps = None
        pj = run / "plan.json"
        if pj.exists():
            try:
                plan = json.loads(pj.read_text(encoding="utf-8"))
                save_ps = plan.get("save_ps") or (plan.get("md") or {}).get("save_ps")
            except Exception:
                save_ps = None
        if not save_ps:
            raise ValueError(f"⛔ 시간축을 만들 수 없다 — {e} · plan.json 의 save_ps 도 없다")
        t_axis = [k * float(save_ps) for k in range(n_traj)]
        axis_note = f"⚠ thermo 대응 실패({e}) → t = 프레임 × save_ps {save_ps} ps **가정** · 온도 열 없음"
    tmax = max(T_set) if T_set else None; tmin = min(T_set) if T_set else None
    rows = []
    onset = None; pair0 = None; switches = 0; last_pair = None
    cen_hist, cen_prev, cen_n = {}, None, 0
    for k, at in enumerate(iread(str(traj), index=":", format="extxyz")):
        if k % stride:
            continue
        sym, pos, cell = at.get_chemical_symbols(), at.get_positions(), np.asarray(at.get_cell())
        st = frame_stats(sym, pos, cell, mq, ss_cut)
        if trace_S:
            st["S_trace"] = trace_frame(sym, pos, cell, mq, trace_S)
        if census:
            own = census_frame(sym, pos, cell, mq); cen_n += 1
            for s, o in own.items():
                if cen_prev is None or cen_prev.get(s) != o:
                    cen_hist.setdefault(s, []).append((k, t_axis[k] if k < len(t_axis) else None,
                                                       (T_set[k] if T_set and k < len(T_set) else None),
                                                       _segment(T_set[k] if T_set and k < len(T_set) else None, tmax, tmin), o))
            cen_prev = own
        d_pair0 = None
        if pair0 is not None:
            d_pair0 = float(mq.mic_dists(pos[[pair0[0]]], pos[[pair0[1]]], cell)[0, 0])
        row = {"frame": k, "t_ps": t_axis[k] if k < len(t_axis) else None,
               "T_K": (T_K[k] if T_K and k < len(T_K) else None), "T_set_K": (T_set[k] if T_set and k < len(T_set) else None),
               "segment": _segment(T_set[k] if T_set and k < len(T_set) else None, tmax, tmin),
               **st, "d_onset_pair_A": (round(d_pair0, 4) if d_pair0 is not None else None)}
        if st["ss_min_A"] is not None and st["ss_min_A"] < ss_cut:
            if onset is None:
                onset, pair0 = k, tuple(st["ss_pair"]); last_pair = pair0
                row["d_onset_pair_A"] = st["ss_min_A"]
            elif tuple(st["ss_pair"]) != last_pair:
                switches += 1; last_pair = tuple(st["ss_pair"])
        rows.append(row)
    res = {"run_dir": str(run), "n_frames": n_traj, "stride": stride, "ss_cut_A": ss_cut, "R_PS_A": mq.R_PS, "time_axis": axis_note,
           "rows": rows, "onset": None}
    ps4_first_drop = next((r for r in rows if r["PS4_fraction"] is not None and r["PS4_fraction"] < 1.0 - 1e-9), None)
    res["PS4_first_below_1"] = ({"frame": ps4_first_drop["frame"], "t_ps": ps4_first_drop["t_ps"], "T_set_K": ps4_first_drop["T_set_K"],
                                 "segment": ps4_first_drop["segment"], "PS4_fraction": ps4_first_drop["PS4_fraction"]} if ps4_first_drop else None)
    if onset is not None:
        after = [r for r in rows if r["frame"] >= onset]
        held = [r for r in after if r["d_onset_pair_A"] is not None and r["d_onset_pair_A"] < ss_cut]
        o = rows[[r["frame"] for r in rows].index(onset)]
        last = rows[-1]
        res["onset"] = {"frame": onset, "t_ps": o["t_ps"], "T_K": o["T_K"], "T_set_K": o["T_set_K"], "segment": o["segment"],
                        "pair": list(pair0), "d_A": o["ss_min_A"], "kind": o["ss_kind"], "P_neighbors_of_pair": o["ss_pair_P_neighbors"],
                        "P_not_4coord_at_onset": o.get("P_not_4coord")}
        res["persistence"] = {"frames_after_onset": len(after), "frames_pair_below_cut": len(held),
                              "fraction": round(len(held) / len(after), 4) if after else None,
                              "last_frame_pair_d_A": last["d_onset_pair_A"], "last_frame_below_cut": (last["d_onset_pair_A"] is not None and last["d_onset_pair_A"] < ss_cut),
                              "last_frame_kind": last["ss_kind"], "pair_switches_after_onset": switches,
                              "longest_gap_frames_above_cut": _longest_gap([r["d_onset_pair_A"] for r in after], ss_cut)}
        kinds = {}
        for r in after:
            kinds[r["ss_kind"]] = kinds.get(r["ss_kind"], 0) + 1
        res["kind_histogram_after_onset"] = kinds
    res["P_coord_stats"] = p_coord_stats(rows)
    if trace_S:
        res["S_trace_stats"] = s_trace_stats(rows, trace_S)
    if census:
        res["S_owner_census"] = s_census_summary(cen_hist, cen_n)
    res["summary"] = _summary(res)
    for ln in res["summary"]:
        log(ln)
    return res


#: 회신 CO (2026-10-04 · li2s v2 · 결과 전) 골격 게이트 숫자 — **외부 1저자 원문 그대로**
#:   ① 프레임의 95 % 이상에서 이탈 P 0 개 · ② production 중 주인이 바뀐 S 0 개 · ③ S–S < 2.30 Å 0 개
CO_GATE = {"P_frac_frames_changed_max": 0.05, "S_moved_max": 0, "SS_new_pairs_max": 0}


def production_framework(run_dir, mq, ss_cut=SS_CUT, stride=1):
    """생산 궤적(traj.xyz) 하나의 골격 세 지표 — 회신 CO Q-CO-4 게이트의 입력 (2026-10-04).

    정의 (**잠정 해석 · 생산 첫 프레임 대비** — 게이트의 뜻이 '생산 중 골격이 움직였나' 라서):
      ① 이탈 P = 그 프레임의 S 배위수(R_PS · 최소상)가 **첫 프레임의 자기 배위수와 다른** P.
         지표 = 이탈 P 가 하나라도 있는 프레임 비율 (게이트 ≤ 5 % = '95 % 이상에서 0 개').
      ② 소속 이동 = 첫 프레임 주인 P 집합 ≠ 마지막 프레임 주인 P 집합인 S — `s_census_summary` 의 '이동' 과 같은 정의
         (담금질 48 S 전수 조사가 눈금이다). 일시 이탈 후 복귀는 transient 로 따로 센다. 게이트 0.
      ③ 새 S–S = 첫 프레임에 없던 S–S < ss_cut 쌍이 어느 프레임에서든 생긴 것. 게이트 0.
    **글자 그대로 읽은 값도 같이 낸다** (`literal`): ① 4 배위 아닌 P 가 있는 프레임 비율 (담금질 'P 이탈 프레임' 셈법) ·
      ③ 첫 프레임 것까지 포함한 S–S < ss_cut 쌍 수. 담금질이 남긴 결함(seed5 의 PS₃ · S–S 2.03 Å)이 첫 프레임에 이미
      있으면 두 읽기가 갈린다 — 어느 쪽이 게이트인지는 외부 1저자 확인 대상이다.

    ⛔ 못 하는 것: 거리 컷 판정이다 (결합 차수 안 봄) · 저장 간격 사이 사건은 못 본다 · 판정을 확정하지 않는다
      (게이트로 쓰는지 기록만 하는지는 카드 개정이 정한다) · 눈금(담금질 통계)은 1200 K 용융을 거친 다른 구간의 것이다.
    """
    from ase.io import iread
    traj = pathlib.Path(run_dir) / "traj.xyz"
    if not traj.exists():
        raise FileNotFoundError(f"{traj} 가 없다 — 궤적 없이는 못 잰다")
    n = 0
    iP = iS = coord0 = own0 = pairs0 = own_prev = None
    n_changed_frames = n_not4_frames = n_new_frames = max_changed = 0
    P_changed_ever, changes, new_pairs, literal_pairs = set(), {}, {}, set()
    for k, at in enumerate(iread(str(traj), index=":", format="extxyz")):
        if k % stride:
            continue
        sym = np.asarray(at.get_chemical_symbols()); pos = at.get_positions(); cell = np.asarray(at.get_cell())
        if iP is None:
            iP = np.where(sym == "P")[0]; iS = np.where(sym == "S")[0]
        DPS = mq.mic_dists(pos[iP], pos[iS], cell) if (len(iP) and len(iS)) else np.zeros((len(iP), len(iS)))
        coord = (DPS <= mq.R_PS).sum(axis=1)
        own = {int(iS[c]): tuple(int(iP[r]) for r in np.where(DPS[:, c] <= mq.R_PS)[0]) for c in range(len(iS))}
        pairs = {}
        if len(iS) >= 2:
            DSS = mq.mic_dists(pos[iS], pos[iS], cell)
            for x, y in zip(*np.where(np.triu(DSS < ss_cut, 1))):
                pairs[(int(iS[x]), int(iS[y]))] = float(DSS[x, y])
        if coord0 is None:
            coord0, own0, pairs0 = coord.copy(), dict(own), dict(pairs)
        ch = np.where(coord != coord0)[0]
        if len(ch):
            n_changed_frames += 1
            P_changed_ever.update(int(iP[x]) for x in ch)
        max_changed = max(max_changed, int(len(ch)))
        if np.any(coord != 4):
            n_not4_frames += 1
        if own_prev is not None:
            for sx, o in own.items():
                if own_prev.get(sx) != o:
                    changes[sx] = changes.get(sx, 0) + 1
        own_prev = own
        fresh = [q for q in pairs if q not in pairs0]
        if fresh:
            n_new_frames += 1
            for q in fresh:
                e = new_pairs.setdefault(q, {"S_pair": list(q), "first_frame": k, "min_d_A": pairs[q], "n_frames": 0})
                e["min_d_A"] = min(e["min_d_A"], pairs[q]); e["n_frames"] += 1
        literal_pairs.update(pairs)
        n += 1
    if n == 0:
        raise ValueError(f"{traj} 에 프레임이 없다")
    last = own_prev
    moved = [{"S": sx, "from_P": list(own0[sx]), "to_P": list(last.get(sx, ())), "n_changes": changes.get(sx, 0)}
             for sx in sorted(own0) if set(own0[sx]) != set(last.get(sx, ()))]
    transient = [{"S": sx, "P": list(own0[sx]), "n_changes": c} for sx, c in sorted(changes.items())
                 if set(own0[sx]) == set(last.get(sx, ()))]
    frac_ch, frac_n4 = n_changed_frames / n, n_not4_frames / n
    g = CO_GATE
    crit = {"①_P": frac_ch <= g["P_frac_frames_changed_max"], "②_S": len(moved) <= g["S_moved_max"],
            "③_SS": len(new_pairs) <= g["SS_new_pairs_max"]}
    lit = {"①_P": frac_n4 <= g["P_frac_frames_changed_max"], "②_S": crit["②_S"],
           "③_SS": len(literal_pairs) <= g["SS_new_pairs_max"]}
    return {
        "run_dir": str(run_dir), "n_frames": n, "stride": stride, "R_PS_A": mq.R_PS, "ss_cut_A": ss_cut,
        "P": {"n_P": int(len(iP)), "n_not4_at_first_frame": int(np.sum(coord0 != 4)),
              "frac_frames_any_P_changed_vs_first": round(frac_ch, 5),
              "max_P_changed_in_a_frame": max_changed, "P_changed_ever": sorted(P_changed_ever)},
        "S": {"n_S": int(len(iS)), "n_moved_first_ne_last": len(moved), "n_transient_only": len(transient),
              "moved": moved[:20], "transient_only": transient[:20]},
        "SS": {"pairs_lt_cut_at_first_frame": [[i, j, round(d, 4)] for (i, j), d in sorted(pairs0.items())],
               "n_new_pairs": len(new_pairs), "frac_frames_with_new_pair": round(n_new_frames / n, 5),
               "new_pairs": [{**v, "min_d_A": round(v["min_d_A"], 4)} for _, v in sorted(new_pairs.items())][:20]},
        "literal": {"①_frac_frames_any_P_not4": round(frac_n4, 5),
                    "③_n_SS_pairs_lt_cut_any_frame_incl_first": len(literal_pairs)},
        "co_gate": {"thresholds": dict(g), "criteria_vs_first_frame": crit, "framework_moved": not all(crit.values()),
                    "literal_criteria": lit, "literal_framework_moved": not all(lit.values()),
                    "⚠": "첫 프레임 대비 = 잠정 해석 · literal = 글자 그대로 — 갈리면 둘 다 적는다 · 게이트로 쓰는지는 카드 개정이 정한다"},
    }


def production_summary(r):
    g, P, S, SS = r["co_gate"], r["P"], r["S"], r["SS"]
    yn = lambda b: "예" if b else "아니오"
    return [f"골격 (생산 궤적 · 회신 CO 게이트 입력) · 프레임 {r['n_frames']} · R_PS {r['R_PS_A']} Å · S–S 컷 {r['ss_cut_A']} Å",
            f" ① 이탈 P(첫 프레임 대비) 있는 프레임 {100 * P['frac_frames_any_P_changed_vs_first']:.2f} % (≤ 5 %) · 첫 프레임 4 배위 아닌 P "
            f"{P['n_not4_at_first_frame']} · [글자 그대로: 4 배위 아닌 P 있는 프레임 {100 * r['literal']['①_frac_frames_any_P_not4']:.2f} %]",
            f" ② S 소속 이동(첫 ≠ 끝) {S['n_moved_first_ne_last']} (= 0) · 일시 변화 {S['n_transient_only']}",
            f" ③ 새 S–S < {r['ss_cut_A']} Å 쌍 {SS['n_new_pairs']} (= 0) · 첫 프레임에 이미 있던 쌍 {len(SS['pairs_lt_cut_at_first_frame'])} "
            f"· [글자 그대로: 첫 프레임 포함 {r['literal']['③_n_SS_pairs_lt_cut_any_frame_incl_first']}]",
            f" → 골격 이동 표시: 첫 프레임 대비 {yn(g['framework_moved'])} · 글자 그대로 {yn(g['literal_framework_moved'])}"]


def _longest_gap(ds, cut):
    best = cur = 0
    for d in ds:
        if d is None or d >= cut:
            cur += 1; best = max(best, cur)
        else:
            cur = 0
    return best


def _summary(res):
    L = [f"프레임 {res['n_frames']} · 컷 S–S < {res['ss_cut_A']} Å · P–S 배위 컷 {res['R_PS_A']} Å · 시간축: {res['time_axis']}"]
    p = res.get("PS4_first_below_1")
    L.append("PS₄ 보존율 < 1 첫 프레임: " + (f"#{p['frame']} t={p['t_ps']} ps · T_set={p['T_set_K']} · {p['segment']} · 값 {p['PS4_fraction']:.4f}" if p else "없음 (전 구간 1.0)"))
    ps = res.get("P_coord_stats")
    if ps:
        L.append("P 4배위 이탈 (이탈 P 가 하나라도 있는 프레임): " + " · ".join(f"{k} {v['frames_any_not4']}/{v['frames']}" for k, v in ps["by_segment"].items())
                 + f" · 이탈한 P {ps['n_P_ever_not4']} 개 · 마지막 프레임에도 이탈 {ps['n_P_not4_last_frame']} 개 · 동시 최대 {ps['max_simultaneous_not4']}")
        for pk, q in ps["per_P"].items():
            rec = q["recovered_at"]
            L.append(f"   P{pk}: {q['frames_not4']} 프레임 {q['by_segment']} · 배위 {q['coord_values']} · 이탈 {q['episodes']} 회 · 처음 #{q['first']['frame']} "
                     f"({q['first']['segment']} · T_set {q['first']['T_set_K']}) · "
                     + ("**끝까지 이탈**" if q["in_last_frame"] else f"회복 #{rec['frame']} ({rec['segment']} · T_set {rec['T_set_K']})"))
    cs = res.get("S_owner_census")
    if cs and cs.get("n_S"):
        L.append(f"S 소속-이동 (전수 {cs['n_S']}): **이동 {cs['n_moved']}** · 일시변화만 {cs['n_transient_only']} · "
                 f"마지막 프레임 자유 {cs['n_free_at_last_frame']} {cs['free_at_last_frame']}")
        L.append(f"   P 별 '남의 S' (마지막 프레임): {cs['foreign_S_per_P_at_last_frame'] or '없음'}")
        idt = cs.get("identity") or {}
        if idt:
            L.append(f"   ★ **정체** 기준: 원래 S 를 전부 지킨 P **{idt['n_P_all_original_S_kept']}/{idt['n_P']}** "
                     f"({idt['fraction_P_all_original_S_kept']}) · 원래 주인을 지킨 S "
                     f"{idt['n_S_kept_original_owner']}/{idt['n_S_with_owner_at_frame0']} ({idt['fraction_S_kept_original_owner']})"
                     + (f" · 프레임 0 자유 S {idt['n_S_free_at_frame0']}" if idt['n_S_free_at_frame0'] else "")
                     + "  ⛔ 배위 기준 PS₄ 보존율과 다른 양이다")
        for m in cs["moved"]:
            c0 = m["changes"][0]
            L.append(f"   S{m['S']}: P{m['from_P']} → P{m['to_P']} · 변화 {m['n_changes']} 회 · "
                     f"첫 변화 #{c0['frame']} t={c0['t_ps']} ps (설정 {c0['T_set_K']} K · {c0['segment']})")
    ts = res.get("S_trace_stats")
    if ts:
        for sk, q in ts["per_S"].items():
            if q["verdict"] == "자료없음":
                L.append(f"   S{sk} 내력: **자료없음** — {q['note']}"); continue
            fd = q["first_detach"]
            L.append(f"   S{sk} 내력: **{q['verdict']}** · 첫 프레임 #{q['first_frame']} ({q['first_frame_segment']} · T_set {q['first_frame_T_set_K']}) "
                     f"{'P 에 붙어 있었다 ' + str(q['first_frame_P_neighbors']) if q['first_frame_bonded'] else 'P 없음 (최근접 P ' + str(q['first_frame_d_nearest_P_A']) + ' Å)'} · "
                     f"붙은 프레임 {q['frames_bonded']}/{q['frames_total']} · 이탈 {q['n_detach']} 회 · 재결합 {q['n_reattach']} 회 · "
                     + (f"첫 이탈 #{fd['frame']} t={fd['t_ps']} ps (설정 {fd['T_set_K']} K · {fd['segment']})" if fd else "이탈 없음")
                     + f" · 마지막 프레임 {'붙어있음' if q['last_frame_bonded'] else '자유'} (최근접 P {q['last_frame_d_nearest_P_A']} Å · 최근접 S S{q['last_frame_nearest_S']} {q['last_frame_d_nearest_S_A']} Å)")
            L.append(f"      구간별 붙음 분율: " + " · ".join(f"{k} {v['frames_bonded']}/{v['frames']}" for k, v in q["by_segment"].items())
                     + f" · P 짝 {q['P_partner_frames']}")
    o = res.get("onset")
    if not o:
        L.append("S–S 근접 사건: **없음** (전 프레임 최단 S–S ≥ 컷)")
        return L
    L.append(f"S–S onset: #{o['frame']} t={o['t_ps']} ps · T={o['T_K']} K (설정 {o['T_set_K']}) · 구간 **{o['segment']}** · 쌍 {o['pair']} · d {o['d_A']} Å · 형태 **{o['kind']}** · 쌍의 P 이웃 {o['P_neighbors_of_pair']}")
    pr = res["persistence"]
    L.append(f"지속: onset 뒤 {pr['frames_after_onset']} 프레임 중 {pr['frames_pair_below_cut']} 에서 같은 쌍 < 컷 (분율 {pr['fraction']}) · 마지막 프레임 d={pr['last_frame_pair_d_A']} Å ({'유지' if pr['last_frame_below_cut'] else '해소'}) · 쌍 교체 {pr['pair_switches_after_onset']} 회 · 컷 위 최장 연속 {pr['longest_gap_frames_above_cut']} 프레임")
    L.append(f"형태 분포(onset 뒤): {res.get('kind_histogram_after_onset')}")
    return L


# ───────────────────────── selftest ─────────────────────────
def _synthetic(tmpdir, event=True, thermo_rows=None):
    """PS₄ 1 개 + 자유 S 1 + Li 4 · 12 Å 셀 · 10 프레임.
    event="detach"(=True): 5 프레임부터 S0 가 P 를 떠나 자유 S 옆(2.05 Å)으로 → PS₃ + `S-S_free`
    event="attach": 5 프레임부터 자유 S 가 결합 S1 옆(2.05 Å)으로 → PS₄ 그대로 + `P-S-S`
    event=False: 사건 없음"""
    from ase import Atoms
    from ase.io import write
    L = 12.0
    P = np.array([6.0, 6.0, 6.0]); v = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3) * 2.05
    Sfree = np.array([1.5, 1.5, 1.5]); Li = np.array([[3, 9, 3], [9, 3, 9], [9, 9, 3], [3, 3, 9]], float)
    run = pathlib.Path(tmpdir); (run / "traj.xyz").unlink(missing_ok=True)
    rows = []
    for k in range(10):
        S = P + v; Sf = Sfree.copy()
        if event and k >= 5:
            if event == "attach":
                Sf = S[0] + (S[0] - P) / np.linalg.norm(S[0] - P) * 2.05   # 자유 S 가 결합 S0 바깥쪽 2.05 Å 로 (P–S0 2.05 · P–Sf 4.10 > R_PS)
            else:
                S[0] = Sfree + np.array([2.05, 0, 0])                        # S0 가 자유 S 옆으로 (P 에서 멀어짐)
        at = Atoms(["P"] + ["S"] * 4 + ["S"] + ["Li"] * 4, positions=np.vstack([P, S, Sf, Li]), cell=np.eye(3) * L, pbc=True)
        write(str(run / "traj.xyz"), at, format="extxyz", append=True)
        rows.append(k)
    n_th = len(rows) if thermo_rows is None else thermo_rows
    with open(run / "thermo.csv", "w") as f:
        f.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
        for k in range(n_th):
            tset = 1200.0 if k < 3 else (300.0 if k >= 8 else 1200.0 - (k - 2) * 180.0)
            f.write(f"{k*1.0:.3f},{tset+3:.1f},{tset:.1f},1.6,1728,0,0,0\n")
    json.dump({"save_ps": 1.0}, open(run / "plan.json", "w"))
    return run


def _synthetic_production(tmpdir, case):
    """PS₄ 두 개 + 자유 S 하나 + Li 2 · 14 Å 셀 · 40 프레임 · ±0.02 Å 떨림 (생산 궤적 흉내).
    case: quiet · moved(30 프레임부터 S0 가 P0 를 떠남) · transient(10–11 프레임만 떠났다 복귀) ·
          newSS(20 프레임부터 자유 S 가 S7 옆 2.05 Å) · seed5(처음부터 P1 이 PS₃ · 자유 S 가 S7 옆 = 담금질 결함)"""
    from ase import Atoms
    from ase.io import write
    L = 14.0
    v = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3) * 2.05
    P = np.array([[4.0, 4.0, 4.0], [10.0, 10.0, 10.0]])
    Li = np.array([[1.0, 12.0, 7.0], [12.0, 1.0, 7.0]])
    rng = np.random.default_rng(0)
    run = pathlib.Path(tmpdir); (run / "traj.xyz").unlink(missing_ok=True)
    s7_out = P[1] + v[3] + v[3]                       # S7 바깥쪽 2.05 Å (P1 에서 4.1 Å — P 에 안 붙는다)
    for k in range(40):
        S = np.vstack([P[0] + v, P[1] + v])
        free = np.array([7.0, 1.0, 12.0])
        if (case == "moved" and k >= 30) or (case == "transient" and k in (10, 11)):
            S[0] = np.array([4.0, 4.0, 0.5])         # P0 에서 3.5 Å · 어느 S 와도 2.30 Å 밖
        if case == "seed5":
            S[4] = np.array([13.0, 2.0, 6.0])        # P1 이 처음부터 PS₃
        if (case == "newSS" and k >= 20) or case == "seed5":
            free = s7_out
        pos = np.vstack([P, S, free, Li]) + rng.normal(0, 0.02, (2 + 8 + 1 + 2, 3))
        at = Atoms(["P"] * 2 + ["S"] * 8 + ["S"] + ["Li"] * 2, positions=pos, cell=np.eye(3) * L, pbc=True)
        write(str(run / "traj.xyz"), at, format="extxyz", append=True)
    return run


def _selftest():
    import tempfile
    mq = _load_mq(); ok = bad = 0
    def ck(c, m):
        nonlocal ok, bad
        if c:
            ok += 1
        else:
            bad += 1; print("  ✗", m)
    with tempfile.TemporaryDirectory() as td:
        r = analyze(_synthetic(td, event="detach"), mq, log=lambda *a: None)
        o = r["onset"]
        ck(o is not None and o["frame"] == 5 and o["kind"] == "S-S_free" and o["segment"] == "quench", f"떨어짐: 5 프레임 onset · S-S_free · 냉각 중 — {o}")
        ck(o and abs(o["d_A"] - 2.05) < 1e-3 and set(o["pair"]) == {1, 5}, f"쌍 = (S1, 자유 S5) · d 2.05 — {o and o['pair']}")
        ck(r["persistence"]["fraction"] == 1.0 and r["persistence"]["last_frame_below_cut"] and r["persistence"]["pair_switches_after_onset"] == 0, "지속 1.0 · 마지막 유지 · 교체 0")
        ck(r["PS4_first_below_1"] and r["PS4_first_below_1"]["frame"] == 5 and o["P_not_4coord_at_onset"] == [[0, 3]], "PS₄ < 1 첫 프레임 5 · P0 가 3 배위 (PS₃)")
        ck(r["rows"][0]["segment"] == "melt_hold" and r["rows"][-1]["segment"] == "final_hold", "구간 라벨: 처음 melt_hold · 끝 final_hold")
    with tempfile.TemporaryDirectory() as td:
        ra = analyze(_synthetic(td, event="attach"), mq, log=lambda *a: None)
        oa = ra["onset"]
        ck(oa is not None and oa["frame"] == 5 and oa["kind"] == "P-S-S" and ra["PS4_first_below_1"] is None and oa["P_not_4coord_at_onset"] == [],
           f"붙음: 자유 S 가 결합 S 옆으로 → P-S-S(말단 과황화) · PS₄ 는 1.0 유지 · PS₃ 없음 — {oa}")
    with tempfile.TemporaryDirectory() as td:
        r0 = analyze(_synthetic(td, event=False), mq, log=lambda *a: None)
        ck(r0["onset"] is None and r0["PS4_first_below_1"] is None, "⛔음성: 사건 없는 궤적 → onset None · PS₄ 1.0 유지")
    with tempfile.TemporaryDirectory() as td:
        r1 = analyze(_synthetic(td, event="detach", thermo_rows=7), mq, log=lambda *a: None)
        ck(r1["time_axis"].startswith("⚠") and r1["rows"][0]["T_K"] is None and r1["onset"]["frame"] == 5, "⛔음성: thermo 행 수 ≠ 프레임 → save_ps 가정 표기 · 온도 없음(0 아님)")
    with tempfile.TemporaryDirectory() as td:
        run = _synthetic(td, event="detach"); (run / "thermo.csv").unlink(); (run / "plan.json").unlink()
        try:
            analyze(run, mq, log=lambda *a: None); bad_ = False
        except ValueError:
            bad_ = True
        ck(bad_, "⛔음성: thermo 도 plan.json 도 없으면 시간축을 지어내지 않고 죽는다")
    rows_t = [{"frame": 0, "t_ps": 0.0, "T_set_K": 1200.0, "segment": "melt_hold", "P_not_4coord": []},
              {"frame": 1, "t_ps": 1.0, "T_set_K": 1200.0, "segment": "melt_hold", "P_not_4coord": [[7, 3]]},
              {"frame": 2, "t_ps": 2.0, "T_set_K": 1200.0, "segment": "melt_hold", "P_not_4coord": [[7, 3], [9, 5]]},
              {"frame": 3, "t_ps": 3.0, "T_set_K": 900.0, "segment": "quench", "P_not_4coord": []},
              {"frame": 4, "t_ps": 4.0, "T_set_K": 700.0, "segment": "quench", "P_not_4coord": [[7, 3]]},
              {"frame": 5, "t_ps": 5.0, "T_set_K": 300.0, "segment": "final_hold", "P_not_4coord": [[7, 3]]}]
    st = p_coord_stats(rows_t)
    q7, q9 = st["per_P"].get("7", {}), st["per_P"].get("9", {})
    ck(st["n_P_ever_not4"] == 2 and st["n_P_not4_last_frame"] == 1 and st["max_simultaneous_not4"] == 2 and q7.get("frames_not4") == 4
       and q7.get("episodes") == 2 and q7.get("in_last_frame") is True and q7.get("by_segment") == {"melt_hold": 2, "quench": 1, "final_hold": 1}
       and q9.get("in_last_frame") is False and (q9.get("recovered_at") or {}).get("frame") == 3 and (q9.get("recovered_at") or {}).get("T_set_K") == 900.0
       and q9.get("coord_values") == {"5": 1} and st["by_segment"]["melt_hold"]["frames_any_not4"] == 2 and st["by_segment"]["quench"]["fraction_any_not4"] == 0.5,
       f"P 4배위 이탈 통계: 구간별 분율 · P 별 프레임·이탈 횟수·끝까지 이탈·회복 시점 — {st}")
    s0 = p_coord_stats([{**x, "P_not_4coord": []} for x in rows_t])
    ck(s0["n_P_ever_not4"] == 0 and s0["per_P"] == {} and s0["max_simultaneous_not4"] == 0 and all(v["frames_any_not4"] == 0 for v in s0["by_segment"].values()),
       "⛔음성: 이탈 없는 행 → 이탈 P 0 · 분율 0")
    with tempfile.TemporaryDirectory() as td:
        rp = analyze(_synthetic(td, event="detach"), mq, log=lambda *a: None)["P_coord_stats"]
        p0 = rp["per_P"].get("0", {})
        ck(p0.get("first", {}).get("frame") == 5 and p0.get("in_last_frame") is True and p0.get("episodes") == 1 and rp["n_P_ever_not4"] == 1,
           f"합성 궤적(떨어짐): P0 이 5 프레임부터 끝까지 3 배위 — {rp}")
    # ── --trace_S (회신 CH · S54 내력) ──
    with tempfile.TemporaryDirectory() as td:
        rt = analyze(_synthetic(td, event="detach"), mq, log=lambda *a: None, trace_S=[1, 5])
        q1 = rt["S_trace_stats"]["per_S"]["1"]; q5 = rt["S_trace_stats"]["per_S"]["5"]
        ck(q1["verdict"] == "이탈" and q1["first_frame_bonded"] is True and q1["n_detach"] == 1
           and q1["first_detach"]["frame"] == 5 and q1["first_detach"]["segment"] == "quench" and q1["last_frame_bonded"] is False,
           f"trace: 붙어 있다 냉각 중 떨어진 S → '이탈' · 첫 이탈 프레임 5 · quench — {q1}")
        ck(q5["verdict"] == "처음부터_자유" and q5["frames_bonded"] == 0 and q5["n_detach"] == 0
           and q5["first_frame_bonded"] is False and q5["first_frame_segment"] == "melt_hold",
           f"trace: 한 번도 P 에 안 붙은 S → '처음부터_자유' · 첫 프레임 구간 melt_hold 병기 — {q5}")
        ck(q1["by_segment"]["melt_hold"]["frames_bonded"] == 3 and q1["by_segment"]["quench"]["frames_bonded"] == 2
           and q1["by_segment"]["final_hold"]["frames_bonded"] == 0 and q1["P_partner_frames"] == {"0": 5},
           f"trace: 구간별 붙음 분율 · P 짝 셈 — {q1['by_segment']} {q1['P_partner_frames']}")
    with tempfile.TemporaryDirectory() as td:
        ra2 = analyze(_synthetic(td, event="attach"), mq, log=lambda *a: None, trace_S=[1, 5])
        a1 = ra2["S_trace_stats"]["per_S"]["1"]; a5 = ra2["S_trace_stats"]["per_S"]["5"]
        ck(a1["verdict"] == "붙어있음" and a1["n_detach"] == 0 and a5["verdict"] == "처음부터_자유"
           and a5["last_frame_nearest_S"] == 1 and abs(a5["last_frame_d_nearest_S_A"] - 2.05) < 1e-3,
           f"trace: 자유 S 가 결합 S 옆에 붙어도 P 가 없으면 '처음부터_자유' · 최근접 S 짝이 그 S — {a5}")
        ck(a5["verdict"] != "이탈", "⛔음성: P 에 한 번도 안 붙은 S 를 '이탈' 로 읽지 않는다")
    with tempfile.TemporaryDirectory() as td:
        run_t = _synthetic(td, event="detach")
        for idx, why in ((0, "P 원자"), (7, "Li 원자"), (99, "범위 밖")):
            try:
                analyze(run_t, mq, log=lambda *a: None, trace_S=[idx]); died = False
            except ValueError:
                died = True
            ck(died, f"⛔음성: --trace_S {idx} ({why}) 면 죽는다 — 다른 원소를 S 로 세지 않는다")
        rt2 = analyze(run_t, mq, log=lambda *a: None)
        ck("S_trace_stats" not in rt2 and (rt2["rows"][0].get("S_trace") is None),
           "⛔음성: --trace_S 없으면 S_trace 를 만들지 않는다 (빈 dict 로 채우지 않는다)")
        st_none = s_trace_stats(rt2["rows"], [1])
        ck(st_none["per_S"]["1"]["verdict"] == "자료없음",
           "⛔음성: 프레임에 trace 기록이 없으면 '자료없음' — 갈래를 지어내지 않는다")
    # ── --s_census (48 S 전수 소속-이동) ──
    with tempfile.TemporaryDirectory() as td:
        rc = analyze(_synthetic(td, event="detach"), mq, log=lambda *a: None, census=True)
        c = rc["S_owner_census"]
        ck(c["n_S"] == 5 and c["n_moved"] == 1 and c["n_transient_only"] == 0
           and c["n_free_at_last_frame"] == 2 and c["free_at_last_frame"] == [1, 5],
           f"census: S 5 개 중 이동 1 · 일시변화 0 · 마지막 자유 2 (S1 이탈 + 원래 자유 S5) — {c}")
        m = c["moved"][0]
        ck(m["S"] == 1 and m["from_P"] == [0] and m["to_P"] == [] and m["n_changes"] == 1
           and m["changes"][0]["frame"] == 5 and m["changes"][0]["segment"] == "quench",
           f"census: 이동 항목이 원래 주인·최종 주인·시각을 싣는다 — {m}")
        ck(c["foreign_S_per_P_at_last_frame"] == {},
           f"census: 남의 S 를 받은 P 없음 — {c['foreign_S_per_P_at_last_frame']}")
    with tempfile.TemporaryDirectory() as td:
        rc0 = analyze(_synthetic(td, event=False), mq, log=lambda *a: None, census=True)
        c0 = rc0["S_owner_census"]
        ck(c0["n_moved"] == 0 and c0["n_transient_only"] == 0 and c0["free_at_last_frame"] == [5],
           f"⛔음성: 사건 없는 궤적 → 이동 0 · 일시변화 0 · 원래 자유 S 만 자유 — {c0}")
        rc1 = analyze(_synthetic(td, event=False), mq, log=lambda *a: None)
        ck("S_owner_census" not in rc1, "⛔음성: --s_census 없으면 census 를 만들지 않는다")
    h_back = {1: [(0, 0.0, 1200.0, "melt_hold", (0,)), (3, 3.0, 900.0, "quench", ()), (5, 5.0, 300.0, "final_hold", (0,))]}
    cb = s_census_summary(h_back, 6)
    ck(cb["n_moved"] == 0 and cb["n_transient_only"] == 1 and cb["transient_only"][0] == {"S": 1, "P": [0], "n_changes": 2}
       and cb["n_free_at_last_frame"] == 0,
       f"⛔음성: 일시 이탈 후 **같은 P 로 복귀**는 이동이 아니다 (transient_only 로 센다) — {cb}")
    h_move = {2: [(0, 0.0, 1200.0, "melt_hold", (0,)), (4, 4.0, 700.0, "quench", (7,))]}
    cm = s_census_summary(h_move, 6)
    ck(cm["n_moved"] == 1 and cm["moved"][0]["from_P"] == [0] and cm["moved"][0]["to_P"] == [7]
       and cm["foreign_S_per_P_at_last_frame"] == {"7": [2]},
       f"census: 주인이 바뀌면 이동 + 받은 P 의 '남의 S' 목록에 오른다 — {cm}")
    h_bridge = {3: [(0, 0.0, 1200.0, "melt_hold", (0,)), (2, 2.0, 1000.0, "quench", (0, 7))]}
    cbr = s_census_summary(h_bridge, 3)
    ck(cbr["n_moved"] == 1 and cbr["foreign_S_per_P_at_last_frame"] == {"7": [3]} and cbr["moved"][0]["to_P"] == [0, 7],
       f"census: 다리 S(주인 둘)는 주인 집합 크기 2 로 나오고 새 P 만 '남의 S' 로 센다 — {cbr}")
    ck(s_census_summary({}, 0)["n_S"] == 0, "⛔음성: S 가 없으면 n_S 0 (지어내지 않는다)")
    # ── 정체 기준 온전율 ──
    with tempfile.TemporaryDirectory() as td:
        ci = analyze(_synthetic(td, event="detach"), mq, log=lambda *a: None, census=True)["S_owner_census"]["identity"]
        ck(ci["n_P"] == 1 and ci["n_P_all_original_S_kept"] == 0 and ci["P_broken"][0]["lost_S"] == [1]
           and ci["n_S_with_owner_at_frame0"] == 4 and ci["n_S_free_at_frame0"] == 1 and ci["S_free_at_frame0"] == [5]
           and ci["n_S_kept_original_owner"] == 3 and ci["fraction_S_kept_original_owner"] == 0.75,
           f"정체: S 하나를 잃은 P 는 온전하지 않다 · 프레임 0 자유 S 는 분모에서 빠진다 — {ci}")
    i2 = s_census_summary({10: [(0, 0.0, 1200.0, "melt_hold", (0,))],
                           20: [(0, 0.0, 1200.0, "melt_hold", (7,)), (4, 4.0, 700.0, "quench", (0,))]}, 6)["identity"]
    ck(i2["n_P"] == 2 and i2["n_P_all_original_S_kept"] == 1 and [b["P"] for b in i2["P_broken"]] == [7],
       f"⛔음성: **남의 S 를 받은 것은 온전성을 깨지 않는다** — P0 은 온전, 잃은 P7 만 깨진다 — {i2}")
    i3 = s_census_summary({11: [(0, 0.0, 1200.0, "melt_hold", (0,)), (3, 3.0, 900.0, "quench", ()),
                                (5, 5.0, 300.0, "final_hold", (0,))]}, 6)["identity"]
    ck(i3["n_P_all_original_S_kept"] == 1 and i3["n_S_kept_original_owner"] == 1 and i3["P_broken"] == [],
       f"⛔음성: 일시 이탈 후 **같은 P 로 복귀**는 온전성을 깨지 않는다 — {i3}")
    i4 = s_census_summary({12: [(0, 0.0, 1200.0, "melt_hold", ())]}, 2)["identity"]
    ck(i4["n_P"] == 0 and i4["fraction_P_all_original_S_kept"] is None and i4["fraction_S_kept_original_owner"] is None,
       f"⛔음성: 프레임 0 에 주인이 아무도 없으면 분율을 **0 으로 그리지 않고 None** 이다 — {i4}")
    # ── 생산 궤적 골격 세 지표 (회신 CO · 2026-10-04) ──
    for case, want in (("quiet", (True, True, True, False, False)), ("moved", (False, False, True, True, True)),
                       ("transient", (True, True, True, False, False)), ("newSS", (True, True, False, True, True)),
                       ("seed5", (True, True, True, False, True))):
        with tempfile.TemporaryDirectory() as td:
            pr = production_framework(_synthetic_production(td, case), mq)
            c = pr["co_gate"]["criteria_vs_first_frame"]
            got = (c["①_P"], c["②_S"], c["③_SS"], pr["co_gate"]["framework_moved"], pr["co_gate"]["literal_framework_moved"])
            ck(got == want, f"생산 골격 [{case}] ①②③·이동·글자그대로 = {want} — 실제 {got} · {pr['P']} · {pr['S']['n_moved_first_ne_last']} · {pr['SS']['n_new_pairs']}")
            if case == "transient":
                ck(pr["S"]["n_transient_only"] == 1 and abs(pr["P"]["frac_frames_any_P_changed_vs_first"] - 0.05) < 1e-9,
                   "⛔음성: 2/40 프레임 일시 이탈 후 복귀 = 5 % (문턱 안) · 이동 아님 (transient 1)")
            if case == "seed5":
                ck(pr["P"]["n_not4_at_first_frame"] == 1 and len(pr["SS"]["pairs_lt_cut_at_first_frame"]) == 1
                   and pr["literal"]["①_frac_frames_any_P_not4"] == 1.0,
                   "⛔음성: 담금질이 남긴 PS₃ · S–S 는 첫 프레임 대비로는 이동 아님 · 글자 그대로는 걸린다 (두 읽기를 다 적는다)")
    print(f"{'✅' if not bad else '⛔'} quench_ss_event selftest {ok}/{ok + bad}")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run_dir", nargs="?")
    ap.add_argument("--ss_cut", type=float, default=SS_CUT)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--table", type=int, default=0, help="N 프레임마다 한 줄 표 (0 = 안 찍음)")
    ap.add_argument("--trace_S", type=int, nargs="+", metavar="IDX",
                    help="특정 S 원자(전역 index)의 내력 — 프레임별 P 이웃·이탈/재결합 (회신 CH · S54)")
    ap.add_argument("--s_census", action="store_true",
                    help="48 S 전수 소속-이동 조사 — PS₄ 보존율이 못 보는 '정체' 를 센다")
    ap.add_argument("--production", action="store_true",
                    help="생산 MD 궤적(traj.xyz 만 · thermo 없음)의 골격 세 지표 — 회신 CO 게이트 입력 "
                         "(첫 프레임 대비 + 글자 그대로 둘 다 · 판정 아님)")
    ap.add_argument("--out")
    ap.add_argument("--tools_dir", help="melt_quench_uma.py 가 있는 폴더 (기본 = 이 파일 폴더)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.run_dir:
        ap.error("run_dir 이 필요하다")
    mq = _load_mq(a.tools_dir)
    if a.production:
        pr = production_framework(a.run_dir, mq, a.ss_cut, a.stride)
        print("\n".join(production_summary(pr)))
        if a.out:
            pathlib.Path(a.out).write_text(json.dumps(pr, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            print(f"-> {a.out}")
        return 0
    res = analyze(a.run_dir, mq, a.ss_cut, a.stride, trace_S=a.trace_S, census=a.s_census)
    if a.table:
        print(f"{'frame':>6s} {'t_ps':>8s} {'T_set':>7s} {'seg':>10s} {'PS4':>6s} {'ssmin':>6s} {'pair':>10s} {'kind':>9s} {'d_onset':>7s}")
        for r in res["rows"]:
            if r["frame"] % a.table == 0 or (res["onset"] and abs(r["frame"] - res["onset"]["frame"]) <= 2):
                print(f"{r['frame']:6d} {r['t_ps'] if r['t_ps'] is not None else float('nan'):8.1f} {r['T_set_K'] if r['T_set_K'] is not None else float('nan'):7.0f} {r['segment']:>10s} "
                      f"{r['PS4_fraction']:6.3f} {r['ss_min_A']:6.3f} {str(r['ss_pair']):>10s} {r['ss_kind']:>9s} {r['d_onset_pair_A'] if r['d_onset_pair_A'] is not None else float('nan'):7.3f}")
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
