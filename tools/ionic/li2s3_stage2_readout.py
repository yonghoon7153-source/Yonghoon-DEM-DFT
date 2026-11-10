#!/usr/bin/env python3
"""li2s-3 2 단계 판독 — v1 런 사후 검증 · 궤적 유효성 · 골격 기록 ⓐ–ⓒ · 측정 가능 온도 창 W (카드 개정 DZ · 결과 전 커밋 · 2026-11-10).

카드 db/properties/lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json ('개정_DZ_회신_2026_11_10')
결정 D-2026-11-10-li2s3-dense-protocol-ensemble (+ -amend1).

  verify  — 런마다 사후 검증 ①–⑦ 만 (수송 · 골격 · 기록은 안 읽는다 — 판독 허가 전에도 돌려도 된다):
            ① 계 러너 로그의 '✅ T<T> seed<S> 끝 (rc N)' 의 N = 0 · ensemble_results.json 있음
            ② run_meta = 카드 기계 값 (T · prod · equilib · seed = offset + 구조 시드 · 원자 수 · 창 · turbo · 모델 · 라벨 · v0 = init 사본)
            ③ init 사본 sha256 = 카드 입력 기록 · 드라이버가 쓴 시작 구조 (d0.00_cfg0/config.xyz) 와 init 이 원소 순서 · 셀 · 좌표 (최소상 1e-6 Å) 로 같다
            ④ aimd_results (T · save_fs 100 · prod · dt 2 · 프레임 수) · traj.xyz (프레임 수 = 계획 · 모든 프레임 원자 수 · 원소 순서 = 시작 구조 ·
              좌표 · 셀 유한 · 셀 불변 · PBC) · md.log (dt 0.002 ps · 끝 시각 = equilib + prod)
            ⑤ msd.json 파싱 · T · 배열 유한
            ⑥ 비용 = 장부 행의 벽시계 (없거나 깨졌으면 '비용 미확정' — 0 아님)
            ⑦ 판독 시점 worktree 의 드라이버 · 러너 sha16 = 카드 (실행 중 바뀌었다가 되돌아간 경우는 못 본다)
  readout — 카드의 '판독_허가_2단계' 가 있을 때만 (회신 EB 뒤): verify + 유효한 런만 glass_v2_readout.read_run (C1 · C2 · 골격 — 고치지 않은 판)
            + skeleton_gate (생산 첫 프레임 대비 ①–④) → (계, T) 측정 가능 = 두 시드 모두 유효 ∧ C1 ∧ 최종 C2 '통과' ∧ 골격 통과 ·
            W = 두 계 공통 · 갈래 (|W| ≥ 3 · 1–2 · 0) · cond550 자격 · 시드별 기술표 (결함 표지 = 담금질 입력 기준) · 세 층 수 ·
            기록 ⓐ 첫 프레임 S–S 쌍 유지 · 소멸 · 재형성 ⓑ P 배위 전이 (3→4 · 4→3) ⓒ 담금질 입력 대 생산 첫 프레임 (기록만 · 판정에 안 씀).
            D 값은 출력하지 않는다.
  control — 대조 잡: 같은 읽기 경로 (궤적 유효성 → read_run → skeleton_gate) 로 10-14 대조 계 판독 기록 (A v2 600 K · B 600 K) 의
            kgy 시드 행을 재현하는가 (C1 · C1 값 · β_MTO 1e-9 · 최종 C2 · σ 거리 · 끝 두 b · N · R 집합 · 골격 네 값).

⛔ 이 도구가 못 하는 것
  · 압력을 내지 않는다 (별도 도구) · R(T) · ΔEa 를 내지 않는다 (3 단계) · 판정 규칙을 새로 만들지 않는다 (glass_v2_readout 그대로).
  · 사후 검증은 '실행 직전 결속' 의 대체 증거다 — 충분한지는 회신 EB 가 정한다 (카드 개정 DZ).
  · 골격 판정은 생산 첫 프레임 대비다 — 담금질 결함이 준비 구간 · 생산 구간 전체에서 보존됐다고 말하지 않는다 (ⓐ–ⓒ 는 기록만).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import pathlib
import re
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[1]
CARD = REPO / "db" / "properties" / "lpscl_glass_dense_protocol_ensemble_estimand_2026_11_10.json"
DECISIONS = REPO / "db" / "governance" / "decisions.json"
NEED_ACTIVE = ("D-2026-11-10-li2s3-dense-protocol-ensemble", "D-2026-11-10-li2s3-dense-protocol-ensemble-amend1")
READ_PERMIT_KEY = "판독_허가_2단계"
N_BOOT = 400                      # 10-14 대조 계 판독과 같은 값 (σ 가 n_boot 에 달려 있다)
SAVE_FS, DT_FS = 100.0, 2.0       # 드라이버 기본 save_fs (러너가 안 넘긴다) · dt
BIND_TOL_A = 1e-6
DEFECT_LABEL_SOURCE = "카드 '입력_2026_11_10.시드' (담금질 final.xyz 기준 · 11-10 kgy 읽기 블록) — 생산 뒤 모습으로 다시 붙이지 않는다"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _sha(p) -> str:
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def card_values(card_path=CARD) -> dict:
    c = json.loads(pathlib.Path(card_path).read_text(encoding="utf-8"))
    mv, inp = c["기계_판독_값"], c["입력_2026_11_10"]["시드"]
    s2 = mv["stage2"]
    return {"systems": list(s2["systems"]), "seeds": list(s2["seeds"]), "temperatures": list(s2["temperatures_K"]),
            "prod_ps": float(s2["prod_ps"]), "equilib_ps": float(s2["equilib_ps"]), "vseed_offset": int(s2["vseed_offset"]),
            "n_atoms": 120, "md_driver_sha16": mv["md_driver_sha16"], "md_runner_sha16": mv["md_runner_sha16"],
            "inputs_sha256": dict(mv["inputs_sha256"]), "defects": {k: {q: v.get(q) for q in ("P_S_배위", "다리_S", "P_P", "li2s2_판정")}
                                                                      for k, v in inp.items()},
            "read_permit": c.get(READ_PERMIT_KEY), "card_sha256": _sha(card_path)}


def decision_states(path=DECISIONS, ids=NEED_ACTIVE) -> dict:
    D = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    L = D["decisions"] if isinstance(D, dict) else D
    return {i: next((e.get("decision_state") for e in L if e.get("id") == i), None) for i in ids}


def _mic_disp(a, b, cell):
    d = np.asarray(b, float) - np.asarray(a, float)
    inv = np.linalg.inv(cell)
    f = d @ inv
    f -= np.round(f)
    return np.linalg.norm(f @ cell, axis=1)


def _runner_rc(log_path, T, seed):
    """계 러너 로그 (tee) 의 마지막 '✅ T<T> seed<S> 끝 (rc N)' → N · 없으면 None."""
    try:
        txt = pathlib.Path(log_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    m = re.findall(rf"✅ T{int(T)} seed{int(seed)} 끝 \(rc (-?\d+)\)", txt)
    return int(m[-1]) if m else None


def _ledger_hours(ledger, sys_, T, seed):
    try:
        rows = list(csv.DictReader(pathlib.Path(ledger).read_text(encoding="utf-8").splitlines(), delimiter="\t"))
    except OSError:
        return None, "장부 없음 — 비용 미확정"
    hit = [r for r in rows if r.get("system") == sys_ and r.get("T_K") == str(int(T)) and r.get("seed") == str(int(seed))]
    if len(hit) != 1:
        return None, f"장부 행 {len(hit)} 개 — 비용 미확정"
    try:
        h = float(hit[0]["hours"])
    except (TypeError, ValueError, KeyError):
        return None, "장부 시간 못 읽음 — 비용 미확정"
    if not (math.isfinite(h) and h >= 0):
        return None, f"장부 시간 {h} — 비용 미확정"
    return h, "장부"


def check_trajectory(tdir, n_atoms, symbols0, prod_ps, T, equilib_ps, keep_PS=False):
    """④ — 궤적 · 기록 유효성. → (문제 목록, 미완 여부, 프레임 자료 {P,S 좌표 · 셀} 또는 None)."""
    from ase.io import iread
    tdir = pathlib.Path(tdir)
    probs, incomplete = [], False
    try:
        ar = json.loads((tdir / "aimd_results.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return ["aimd_results.json 없음 · 못 읽음"], True, None
    n_exp = int(round(prod_ps * 1000.0 / SAVE_FS)) + 1
    for k, want in (("T_K", float(T)), ("save_fs", SAVE_FS), ("prod_ps", float(prod_ps)), ("dt_fs", DT_FS)):
        try:
            ok = abs(float(ar.get(k)) - want) <= 1e-9
        except (TypeError, ValueError):
            ok = False
        if not ok:
            probs.append(f"aimd_results {k} {ar.get(k)!r} ≠ {want}")
    if ar.get("n_frames") != n_exp:
        probs.append(f"aimd_results n_frames {ar.get('n_frames')!r} ≠ 계획 {n_exp}")
    tp = tdir / "traj.xyz"
    if not tp.is_file():
        return probs + ["traj.xyz 없음"], True, None
    n, cell0, P, S = 0, None, [], []
    try:
        for a in iread(str(tp), index=":", format="extxyz"):
            sym = a.get_chemical_symbols()
            pos, cell = a.get_positions(), np.asarray(a.get_cell())
            if len(a) != n_atoms:
                probs.append(f"프레임 {n}: 원자 {len(a)} ≠ {n_atoms}")
                break
            if sym != symbols0:
                probs.append(f"프레임 {n}: 원소 순서가 시작 구조와 다르다")
                break
            if not (np.all(np.isfinite(pos)) and np.all(np.isfinite(cell))):
                probs.append(f"프레임 {n}: 좌표 · 셀이 유한하지 않다")
                break
            if not all(a.pbc):
                probs.append(f"프레임 {n}: PBC 가 꺼져 있다")
                break
            if cell0 is None:
                cell0 = cell
            elif float(np.abs(cell - cell0).max()) > 1e-9:
                probs.append(f"프레임 {n}: 셀이 바뀌었다 (NVT 인데)")
                break
            if keep_PS:
                s = np.asarray(sym)
                P.append(pos[s == "P"]); S.append(pos[s == "S"])
            n += 1
    except Exception as e:                                            # 못 읽은 것은 '변화 없음' 이 아니다
        probs.append(f"traj.xyz 를 못 읽었다 ({type(e).__name__}: {e})")
    if n != n_exp and not probs:
        probs.append(f"traj.xyz 프레임 {n} ≠ 계획 {n_exp}")
        incomplete = n < n_exp
    if n < 2:
        probs.append(f"traj.xyz 프레임 {n} 개 (2 개 미만)")
        incomplete = True
    try:
        lines = (tdir / "md.log").read_text(encoding="utf-8", errors="replace").splitlines()
        it = lines[0].split().index("Time[ps]")
        ts = [float(q.split()[it]) for q in lines[1:] if q.strip()]
        if len(ts) < 3 or abs((ts[1] - ts[0]) - DT_FS / 1000.0) > 1e-9:
            probs.append("md.log dt ≠ 0.002 ps")
        if abs(ts[-1] - (equilib_ps + prod_ps)) > 1e-6:
            probs.append(f"md.log 끝 시각 {ts[-1]} ≠ {equilib_ps + prod_ps} ps")
            incomplete = incomplete or ts[-1] < equilib_ps + prod_ps
    except (OSError, IndexError, ValueError) as e:
        probs.append(f"md.log 를 못 읽었다 ({type(e).__name__})")
    data = {"P": P, "S": S, "cell": cell0} if (keep_PS and not probs) else None
    return probs, incomplete, data


def verify_run(base, sys_, seed, T, cv, worktree, keep_PS=False):
    """런 하나의 사후 검증 ①–⑦ → {status: valid | invalid | incomplete, reasons, cost_h, ...}."""
    from ase.io import read
    base = pathlib.Path(base)
    rd = base / sys_ / f"seed{seed}" / f"T{int(T)}"
    tdir = rd / "d0.00_cfg0" / f"T{int(T)}"
    inv, inc = [], []
    out = {"system": sys_, "seed": int(seed), "T_K": int(T), "run_dir": str(rd)}
    if not (tdir / "msd.json").is_file():
        inc.append("msd.json 없음 (끝나지 않았다)")
    rc = _runner_rc(base / sys_ / "queue_kgy.log", T, seed)
    out["runner_rc"] = rc
    if rc is None:
        (inc if inc else inv).append("러너 로그에 이 런의 끝 줄이 없다")
    elif rc != 0:
        inv.append(f"드라이버 종료 코드 {rc} ≠ 0 (러너 로그)")
    if not (rd / "ensemble_results.json").is_file():
        (inc if inc else inv).append("ensemble_results.json 없음")
    try:
        m = json.loads((rd / "run_meta.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        m = None
        inv.append("run_meta.json 없음 · 못 읽음")
    init = base / sys_ / "init" / f"seed{seed}_final.xyz"
    if m is not None:
        want = {"n_atoms": cv["n_atoms"], "supercell": [1, 1, 1], "temperatures": [float(T)], "prod_ps": cv["prod_ps"],
                "equilib_ps": cv["equilib_ps"], "seed": cv["vseed_offset"] + int(seed), "fit_window_ps": [2.0, 50.0],
                "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo",
                "label": f"li2s3_{sys_}_s{seed}_T{int(T)}"}
        for k, w in want.items():
            g = m.get(k)
            same = (abs(float(g) - float(w)) <= 1e-9) if isinstance(w, float) and isinstance(g, (int, float)) else (
                [float(x) for x in g] == [float(x) for x in w] if (isinstance(w, list) and isinstance(g, list) and k != "supercell") else g == w)
            if not same:
                inv.append(f"run_meta {k} {g!r} ≠ 카드 {w!r}")
        try:
            v0_ok = pathlib.Path(m.get("v0_xyz", "")).resolve() == init.resolve()
        except (OSError, TypeError):
            v0_ok = False
        if not v0_ok:
            inv.append(f"run_meta v0_xyz {m.get('v0_xyz')!r} ≠ init 사본 {init}")
    want_sha = cv["inputs_sha256"].get(f"{sys_}{seed}")
    symbols0 = None
    if not init.is_file() or _sha(init) != want_sha:
        inv.append(f"init 사본 {init.name} 이 없거나 sha256 ≠ 카드 입력 기록")
    else:
        try:
            a_in, a_cf = read(str(init)), read(str(rd / "d0.00_cfg0" / "config.xyz"))
            symbols0 = a_cf.get_chemical_symbols()
            if (a_in.get_chemical_symbols() != symbols0 or float(np.abs(np.asarray(a_in.get_cell()) - np.asarray(a_cf.get_cell())).max()) > BIND_TOL_A
                    or float(_mic_disp(a_in.get_positions(), a_cf.get_positions(), np.asarray(a_in.get_cell())).max()) > BIND_TOL_A):
                inv.append("드라이버가 쓴 시작 구조 (config.xyz) ≠ init 사본 (원소 순서 · 셀 · 좌표)")
            out["_input_atoms"] = a_in
        except Exception as e:
            inv.append(f"시작 구조 대조 실패 ({type(e).__name__}: {e})")
    if symbols0 is not None:
        tp, ti, data = check_trajectory(tdir, cv["n_atoms"], symbols0, cv["prod_ps"], T, cv["equilib_ps"], keep_PS=keep_PS)
        (inc if (ti and inc) else inv).extend(tp)
        out["_frames"] = data
    if not inc:
        try:
            d = json.loads((tdir / "msd.json").read_text(encoding="utf-8"))
            arr = [float(x) for x in d["times_ps"]] + [float(x) for x in d["msd_Li_A2"]]
            if abs(float(d.get("T_K")) - float(T)) > 1e-9 or not arr or not all(math.isfinite(x) for x in arr):
                inv.append("msd.json T · 배열이 맞지 않거나 유한하지 않다")
        except (OSError, ValueError, KeyError, TypeError) as e:
            inv.append(f"msd.json 을 못 읽었다 ({type(e).__name__})")
    h, src = _ledger_hours(base / "cost_ledger.tsv", sys_, T, seed)
    out["cost_h"], out["cost_source"] = h, src
    wt = pathlib.Path(worktree)
    for key, rel in (("md_driver_sha16", "tools/modelc_v3/disorder_ensemble_diffusion.py"),
                     ("md_runner_sha16", "db/raw/lpscl_glass_md_v2_2026_09_30/glass_kgy_q_v2.sh")):
        f = wt / rel
        got = _sha(f)[:16] if f.is_file() else None
        if got != cv[key]:
            inv.append(f"{rel} sha16 {got} ≠ 카드 {cv[key]} (판독 시점 worktree)")
    out["status"] = "incomplete" if inc else ("invalid" if inv else "valid")
    out["reasons"] = inc + inv
    return out


def records_abc(data, a_input, mq, ss_cut=2.30):
    """기록 ⓐ–ⓒ (판정에 안 씀) — data = {P: [프레임별 P 좌표], S: [...], cell}."""
    P, S, cell = data["P"], data["S"], np.asarray(data["cell"])
    rps = mq.R_PS

    def coord(Pp, Sp):
        return (mq.mic_dists(Pp, Sp, cell) <= rps).sum(axis=1)

    def owners(Pp, Sp):
        D = mq.mic_dists(Pp, Sp, cell)
        return [tuple(np.where(D[:, j] <= rps)[0]) for j in range(D.shape[1])]

    def ss_pairs(Sp):
        D = mq.mic_dists(Sp, Sp, cell)
        iu = np.triu_indices(len(Sp), 1)
        return {(int(i), int(j)) for i, j in zip(*iu) if D[i, j] < ss_cut}

    pairs0 = sorted(ss_pairs(S[0]))
    pa = []
    for i, j in pairs0:
        d = np.array([float(_mic_disp(S[k][i:i + 1], S[k][j:j + 1], cell)[0]) for k in range(len(S))])
        on = d < ss_cut
        pa.append({"S_pair": [i, j], "d0_A": float(d[0]), "frac_frames_kept": float(on.mean()), "kept_last": bool(on[-1]),
                   "n_break": int(np.sum(on[:-1] & ~on[1:])), "n_reform": int(np.sum(~on[:-1] & on[1:]))})
    cs = np.array([coord(P[k], S[k]) for k in range(len(P))])
    trans = {}
    for k in range(1, len(cs)):
        for a0, a1 in zip(cs[k - 1], cs[k]):
            if a0 != a1:
                key = f"{int(a0)}→{int(a1)}"
                trans[key] = trans.get(key, 0) + 1
    sym = np.asarray(a_input.get_chemical_symbols())
    Pin, Sin = a_input.get_positions()[sym == "P"], a_input.get_positions()[sym == "S"]
    hist = lambda c: {int(k): int(v) for k, v in zip(*np.unique(c, return_counts=True))}
    o_in, o_f0 = owners(Pin, Sin), owners(P[0], S[0])
    ss_in, ss_f0 = ss_pairs(Sin), set(pairs0)
    return {"ⓐ_first_frame_SS_pairs": pa,
            "ⓑ_P_coordination_transitions": trans,
            "ⓑ_P_coord_hist_first_last": {"first": hist(cs[0]), "last": hist(cs[-1])},
            "ⓒ_input_vs_first_frame": {"P_coord_hist_input": hist(coord(Pin, Sin)), "P_coord_hist_first": hist(cs[0]),
                                       "n_S_owner_changed": sum(1 for a, b in zip(o_in, o_f0) if set(a) != set(b)),
                                       "SS_pairs_input": len(ss_in), "SS_pairs_first": len(ss_f0),
                                       "SS_kept": len(ss_in & ss_f0), "SS_lost": len(ss_in - ss_f0), "SS_new": len(ss_f0 - ss_in)},
            "⚠": "기록만 — 판정에 안 씀 (카드 개정 DZ ⓐ–ⓒ) · 거리 컷 판독 (결합 차수 안 봄)"}


def _row(G, rec):
    sk = G.skeleton_gate(rec)
    c2 = rec.get("C2") or {}
    ok = G.run_pass(rec)
    return {"C1_pass": rec.get("C1_pass"), "C1_msd_at_50_mto_A2": rec.get("C1_msd_at_50_mto_A2"), "beta_MTO": rec.get("beta_MTO"),
            "C2_final": c2.get("final_verdict"), "n_sigma_end": c2.get("n_sigma_end_signed"), "n_sigma_prev": c2.get("n_sigma_prev_signed"),
            "b_end": c2.get("b_end"), "b_prev": c2.get("b_prev"), "counts_in_N": ok, "skeleton": sk,
            "in_R_set": bool(ok and sk["pass"]), "error": rec.get("error")}


def readout(base, worktree, card=CARD, decisions=DECISIONS, n_boot=N_BOOT, read_run=None, require_permit=True):
    import glass_v2_readout as G
    import quench_ss_event as Q
    st = decision_states(decisions)
    if any(v != "active" for v in st.values()):
        raise SystemExit(f"⛔ 결정이 active 가 아니다 {st} — 판독하지 않는다")
    cv = card_values(card)
    if require_permit and not (isinstance(cv["read_permit"], dict) and cv["read_permit"].get("근거") and cv["read_permit"].get("by")):
        raise SystemExit(f"⛔ 카드에 '{READ_PERMIT_KEY}' (근거 · by) 가 없다 — 2 단계 판독 보류 중 (카드 개정 DZ · 회신 EB 뒤)")
    rr = read_run or G.read_run
    mq = Q._load_mq(str(HERE))
    runs, rows = {}, []
    for sys_ in cv["systems"]:
        for sd in cv["seeds"]:
            for T in cv["temperatures"]:
                v = verify_run(base, sys_, sd, T, cv, worktree, keep_PS=True)
                runs[(sys_, sd, T)] = v
    inc = [f"{k[0]}{k[1]} T{k[2]}: {'; '.join(v['reasons'][:2])}" for k, v in runs.items() if v["status"] == "incomplete"]
    if inc:
        raise SystemExit(f"⛔ 끝나지 않은 런 {len(inc)} 개 (예 {inc[0]}) — 계획 런이 다 끝난 뒤 한 번 읽는다")
    for (sys_, sd, T), v in runs.items():
        row = {"system": sys_, "seed": sd, "T_K": T, "verify": {k: v[k] for k in ("status", "reasons", "runner_rc", "cost_h", "cost_source")}}
        if v["status"] == "valid":
            msd = pathlib.Path(v["run_dir"]) / "d0.00_cfg0" / f"T{int(T)}" / "msd.json"
            rec = rr(msd, n_boot=n_boot, framework=True, mq=mq)
            rec.pop("_D_slope", None)
            row.update(_row(G, rec))
            row["measurable"] = bool(row["in_R_set"])
            row["records"] = records_abc(v["_frames"], v["_input_atoms"], mq) if v.get("_frames") else {"status": "자료 없음"}
            row["exclusion"] = None if row["measurable"] else (
                "판독 오류" if rec.get("error") else "C1 미통과" if not row["C1_pass"] else
                f"C2 {row['C2_final']}" if row["C2_final"] != "통과" else "골격 이동 · 보류")
        else:
            row["measurable"], row["exclusion"] = False, f"사후 검증 {v['status']}"
        rows.append(row)
    meas = {(s, T): all(r["measurable"] for r in rows if r["system"] == s and r["T_K"] == T)
            for s in cv["systems"] for T in cv["temperatures"]}
    W = [T for T in cv["temperatures"] if all(meas[(s, T)] for s in cv["systems"])]
    branch = ("3 단계 후보 = W 의 가장 낮은 셋 → 사용자 결정 (상한 포함)" if len(W) >= 3 else
              "Ea 차 없음 · R 만 그 온도에서 (축소 3 단계 · 사용자 결정)" if W else "닫는다 (S2 허용 문구 + 구조군 문구)")
    table = []
    for s in cv["systems"]:
        for sd in cv["seeds"]:
            table.append({"system": s, "seed": sd, "defect_label": cv["defects"].get(f"{s}{sd}"), "label_source": DEFECT_LABEL_SOURCE,
                          "per_T": {str(r["T_K"]): {k: r.get(k) for k in ("C1_pass", "C2_final", "measurable", "exclusion")}
                                    | {"skeleton_values": (r.get("skeleton") or {}).get("values")}
                                    for r in rows if r["system"] == s and r["seed"] == sd}})
    cost = [r["verify"]["cost_h"] for r in rows]
    return {"kind": "li2s3_stage2_readout/v1", "card_sha256": cv["card_sha256"], "decisions": st, "n_boot": n_boot,
            "rows": rows, "measurable": {f"{s}_T{T}": meas[(s, T)] for (s, T) in meas}, "W": W, "branch": branch,
            "cond550_eligible": all(meas.get((s, 600), False) for s in cv["systems"]),
            "seed_table": table,
            "layers": {"생성_후보군": len(cv["defects"]), "포함_가능군": len(cv["defects"]),
                       "2단계_시드": [f"{s}{sd}" for s in cv["systems"] for sd in cv["seeds"]],
                       "온도별_측정가능_시드수": {f"{s}_T{T}": sum(1 for r in rows if r["system"] == s and r["T_K"] == T and r["measurable"])
                                         for s in cv["systems"] for T in cv["temperatures"]}},
            "cost_h_total": (sum(cost) if all(c is not None for c in cost) else None),
            "cost_note": "None = 비용 미확정 (런 하나라도 장부에 없거나 깨짐 — 0 으로 세지 않는다)",
            "⚠": "D · σ 값 없음 · 기록 ⓐ–ⓒ 는 판정에 안 씀 · 골격은 생산 첫 프레임 대비 (카드 개정 DZ)"}


def control(root_a, root_b, seeds=(1, 3), record=None, n_boot=N_BOOT, read_run=None):
    """대조 잡 — 10-14 대조 계 판독 기록 행을 같은 읽기 경로로 재현하는가 (kgy 시드)."""
    import glass_v2_readout as G
    import quench_ss_event as Q
    from ase.io import read
    rec = G.readout600(record or G.READOUT_600)
    if rec.get("status"):
        return {"same": None, "status": rec["status"]}
    if rec.get("n_boot") != n_boot:
        return {"same": None, "status": f"n_boot {n_boot} ≠ 기록 {rec.get('n_boot')}"}
    rr = read_run or G.read_run
    mq = Q._load_mq(str(HERE))
    diffs, rows = [], []
    for sys_, root in (("A", root_a), ("B", root_b)):
        old = {x.get("seed"): x for x in rec[sys_]}
        for sd in seeds:
            tdir = pathlib.Path(root) / f"seed{sd}" / "T600" / "d0.00_cfg0" / "T600"
            first = None
            try:
                first = read(str(tdir / "traj.xyz"), index=0)
                ar = json.loads((tdir / "aimd_results.json").read_text(encoding="utf-8"))
                eq = json.loads((tdir.parents[1] / "run_meta.json").read_text(encoding="utf-8")).get("equilib_ps", 5.0)
                probs, incp, _ = check_trajectory(tdir, len(first), first.get_chemical_symbols(), float(ar["prod_ps"]), 600, float(eq))
            except Exception as e:
                probs = [f"못 읽었다 ({type(e).__name__}: {e})"]
            if probs:
                diffs.append(f"{sys_} seed{sd}: 궤적 유효성 실패 — {probs[:2]} (옛 런을 이 검사가 거부 = 검사 결함 의심)")
                continue
            x = _row(G, {k: v for k, v in rr(tdir / "msd.json", n_boot=n_boot, framework=True, mq=mq).items() if k != "_D_slope"})
            y = old.get(sd)
            rows.append({"system": sys_, "seed": sd, **{k: x[k] for k in G.ROW_SAME_EXACT + G.ROW_SAME_FLOAT}})
            if y is None:
                diffs.append(f"{sys_} seed{sd}: 기록에 행이 없다")
                continue
            for k in G.ROW_SAME_EXACT:
                if x.get(k) != y.get(k):
                    diffs.append(f"{sys_} seed{sd} {k}: 기록 {y.get(k)} · 지금 {x.get(k)}")
            for k in G.ROW_SAME_FLOAT:
                u, w = x.get(k), y.get(k)
                if u is None or w is None or abs(u - w) > 1e-9:
                    diffs.append(f"{sys_} seed{sd} {k}: 기록 {w} · 지금 {u}")
            if (x.get("skeleton") or {}).get("values") != (y.get("skeleton") or {}).get("values"):
                diffs.append(f"{sys_} seed{sd} 골격 네 값: 기록 {(y.get('skeleton') or {}).get('values')} · 지금 {(x.get('skeleton') or {}).get('values')}")
    return {"same": not diffs, "diffs": diffs, "rows": rows, "n_boot": n_boot, "record_tool_sha16": rec.get("tool_sha16"),
            "⚠": "대조 잡 — 판정 규칙이 아니다 · 같은 읽기 경로 (궤적 유효성 → read_run → skeleton_gate) 의 무결성 확인"}


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    import tempfile
    from ase import Atoms
    from ase.io import write
    import glass_v2_readout as G
    import quench_ss_event as Q
    n_ok, fails = 0, []

    def chk(c, msg):
        nonlocal n_ok
        if c:
            n_ok += 1
            print(f"  ✔ {msg}")
        else:
            fails.append(msg)
            print(f"  ✘ {msg}")

    def refuses(kw, fn, *a, **k):
        try:
            fn(*a, **k)
        except SystemExit as e:
            return kw in str(e)
        except Exception as e:
            print(f"     (터짐 {type(e).__name__}: {e})")
            return False
        return False

    mq = Q._load_mq(str(HERE))
    L = 12.0
    tet = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3) * 2.05

    def structure(seed_shift=0.0, ss_pair=False, three_coord=False):
        """P 두 개 (PS₄ · three_coord 면 하나는 PS₃) + 자유 S 둘 (ss_pair 면 2.1 Å) + Li 12 — 원자 26 · 12 Å 상자."""
        P1, P2 = np.array([3.0, 3, 3]), np.array([9.0, 9, 9]) + seed_shift
        pos = [P1] + list(P1 + tet) + [P2] + list(P2 + tet[: (3 if three_coord else 4)])
        sy = ["P"] + ["S"] * 4 + ["P"] + ["S"] * (3 if three_coord else 4)
        fs = [np.array([6.0, 2.0, 9.0]), np.array([6.0, 2.0, 9.0 + (2.1 if ss_pair else 3.5)])]
        pos += fs; sy += ["S", "S"]
        if three_coord:
            pos.append(np.array([2.0, 9.0, 6.0])); sy.append("S")
        rng = np.random.default_rng(7)
        li = rng.uniform(0.5, L - 0.5, (26 - len(sy), 3))
        return Atoms(sy + ["Li"] * len(li), positions=np.vstack(pos + [li]), cell=np.eye(3) * L, pbc=True)

    def make_run(base, sys_, sd, T, cv, a0, frames_fn=None, n_frames=None, rc=0, meta_over=None, write_msd=True,
                 cfg_shift=0.0, mdlog_end=None):
        rd = base / sys_ / f"seed{sd}" / f"T{T}"
        td_ = rd / "d0.00_cfg0" / f"T{T}"
        td_.mkdir(parents=True, exist_ok=True)
        init = base / sys_ / "init" / f"seed{sd}_final.xyz"
        if not init.exists():
            init.parent.mkdir(parents=True, exist_ok=True)
            write(str(init), a0, format="extxyz")
        cf = a0.copy(); cf.positions[0, 0] += cfg_shift
        write(str(rd / "d0.00_cfg0" / "config.xyz"), cf, format="extxyz")
        meta = {"label": f"li2s3_{sys_}_s{sd}_T{T}", "n_atoms": len(a0), "supercell": [1, 1, 1], "v0_xyz": str(init),
                "temperatures": [float(T)], "prod_ps": cv["prod_ps"], "equilib_ps": cv["equilib_ps"], "seed": cv["vseed_offset"] + sd,
                "fit_window_ps": [2.0, 50.0], "save_traj": True, "uma_model": "uma-s-1p1", "uma_inference_mode_requested": "turbo"}
        meta.update(meta_over or {})
        (rd / "run_meta.json").write_text(json.dumps(meta))
        (rd / "ensemble_results.json").write_text("{}")
        nf = n_frames if n_frames is not None else int(round(cv["prod_ps"] * 1000 / SAVE_FS)) + 1
        rng = np.random.default_rng(sd + int(T))
        sym = np.asarray(a0.get_chemical_symbols())
        li = a0.positions[sym == "Li"].copy()
        for k in range(nf):
            a = a0.copy()
            li = li + rng.normal(0, 0.25, li.shape)
            a.positions[sym == "Li"] = li
            if frames_fn:
                a = frames_fn(k, a)
            write(str(td_ / "traj.xyz"), a, format="extxyz", append=True)
        (td_ / "aimd_results.json").write_text(json.dumps({"T_K": float(T), "save_fs": SAVE_FS, "n_frames": int(round(cv["prod_ps"] * 1000 / SAVE_FS)) + 1,
                                                          "prod_ps": cv["prod_ps"], "dt_fs": DT_FS}))
        end = mdlog_end if mdlog_end is not None else cv["equilib_ps"] + cv["prod_ps"]
        (td_ / "md.log").write_text("Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]\n"
                                    + "".join(f"{t:.4f} -1.0 -1.0 0.0 {T}\n" for t in (0.0, 0.002, 0.004)) + f"{end:.4f} -1.0 -1.0 0.0 {T}\n")
        if write_msd:
            (td_ / "msd.json").write_text(json.dumps({"T_K": float(T), "times_ps": [0.1 * i for i in range(1, 50)],
                                                      "msd_Li_A2": [0.375 * 0.1 * i for i in range(1, 50)], "save_fs": SAVE_FS}))
        log = base / sys_ / "queue_kgy.log"
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(f"[x] ▶ T{T} seed{sd} PID 1 · prod {cv['prod_ps']:g} ps\n")
            if rc is not None:
                fh.write(f"[x] ✅ T{T} seed{sd} 끝 (rc {rc})\n")
        return rd

    def wt_dir(root, drv=b"driver", run=b"runner"):
        (root / "tools/modelc_v3").mkdir(parents=True, exist_ok=True)
        (root / "db/raw/lpscl_glass_md_v2_2026_09_30").mkdir(parents=True, exist_ok=True)
        (root / "tools/modelc_v3/disorder_ensemble_diffusion.py").write_bytes(drv)
        (root / "db/raw/lpscl_glass_md_v2_2026_09_30/glass_kgy_q_v2.sh").write_bytes(run)
        return root

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        wt = wt_dir(td / "wt")
        a_ok, a_def = structure(), structure(ss_pair=True, three_coord=True)
        cv = {"systems": ["A", "B"], "seeds": [11, 12], "temperatures": [600, 650], "prod_ps": 20.0, "equilib_ps": 5.0,
              "vseed_offset": 3000, "n_atoms": len(a_ok), "md_driver_sha16": hashlib.sha256(b"driver").hexdigest()[:16],
              "md_runner_sha16": hashlib.sha256(b"runner").hexdigest()[:16], "inputs_sha256": {}, "defects": {}, "read_permit": None,
              "card_sha256": "x"}
        base = td / "b1"
        for s in ("A", "B"):
            for sd in (11, 12):
                a0 = a_def if (s, sd) in (("A", 11), ("B", 12)) else a_ok
                for T in (600, 650):
                    make_run(base, s, sd, T, cv, a0)
                cv["inputs_sha256"][f"{s}{sd}"] = _sha(base / s / "init" / f"seed{sd}_final.xyz")
        (base / "cost_ledger.tsv").write_text("system\tT_K\tseed\tprod_ps\tstart\tend\thours\trc\n"
                                              + "".join(f"{s}\t{T}\t{sd}\t20\tx\ty\t1.5\t0\n" for s in "AB" for sd in (11, 12) for T in (600, 650)))
        v = verify_run(base, "A", 11, 600, cv, wt, keep_PS=True)
        chk(v["status"] == "valid" and v["runner_rc"] == 0 and v["cost_h"] == 1.5 and v["_frames"] is not None,
            "[양성] 사후 검증 ①–⑦ 통과 (러너 rc 0 · run_meta = 카드 · 시작 구조 = init · 궤적 유효 · msd · 장부 · 코드 지문)")
        r = records_abc(v["_frames"], v["_input_atoms"], mq)
        chk(len(r["ⓐ_first_frame_SS_pairs"]) == 1 and r["ⓐ_first_frame_SS_pairs"][0]["kept_last"]
            and r["ⓒ_input_vs_first_frame"]["P_coord_hist_input"] == {3: 1, 4: 1},
            "[양성] 기록: 첫 프레임 S–S 쌍 (2.1 Å) 유지 · 입력 P 배위 {3: 1, 4: 1}")

        def build(label, mutate, sys_="B", sd=11, T=600):
            b = td / ("n_" + str(abs(hash(label)) % 10**7))
            for s in ("A", "B"):
                for s_ in (11, 12):
                    a0 = a_def if (s, s_) in (("A", 11), ("B", 12)) else a_ok
                    for T_ in (600, 650):
                        kw_ = mutate if (s, s_, T_) == (sys_, sd, T) else {}
                        make_run(b, s, s_, T_, cv, a0, **kw_)
            (b / "cost_ledger.tsv").write_text((base / "cost_ledger.tsv").read_text())
            return b

        def neg(label, kw, mutate, sys_="B", sd=11, T=600, want="invalid"):
            b = build(label, mutate, sys_, sd, T)
            vv = verify_run(b, sys_, sd, T, cv, wt)
            chk(vv["status"] == want and any(kw in q for q in vv["reasons"]), f"⛔음성: {label} → {want} ({'; '.join(vv['reasons'])[:80]})")
            return b

        nanf = lambda k, a: (a.positions.__setitem__((3, 0), np.nan) or a) if k == 50 else a

        def swapf(k, a):
            if k == 60:
                s = a.get_chemical_symbols(); s[1], s[-1] = s[-1], s[1]; a.set_chemical_symbols(s)
            return a

        def cellf(k, a):
            if k == 70:
                a.set_cell(np.eye(3) * 12.1, scale_atoms=False)
            return a
        neg("드라이버 종료 코드 7 (msd.json 은 있음)", "종료 코드 7", {"rc": 7})
        neg("러너 끝 줄 없음", "끝 줄", {"rc": None})
        neg("궤적 NaN 프레임", "유한", {"frames_fn": nanf})
        neg("궤적 원소 바뀜", "원소 순서", {"frames_fn": swapf})
        neg("궤적 셀 바뀜", "셀이 바뀌었다", {"frames_fn": cellf})
        neg("궤적 프레임 수 ≠ 계획 (msd 있음)", "프레임", {"n_frames": 150})
        neg("run_meta seed 9011", "run_meta seed", {"meta_over": {"seed": 9011}})
        neg("run_meta prod 7", "run_meta prod_ps", {"meta_over": {"prod_ps": 7.0}})
        neg("run_meta 다른 v0", "v0_xyz", {"meta_over": {"v0_xyz": "/tmp/other.xyz"}})
        neg("시작 구조 ≠ init (0.5 Å)", "config.xyz", {"cfg_shift": 0.5})
        neg("md.log 끝 시각 짧음 (msd 있음)", "md.log 끝 시각", {"mdlog_end": 10.0})
        neg("끝나지 않은 런 (msd.json 없음 · 끝 줄 없음)", "msd.json 없음", {"write_msd": False, "rc": None}, want="incomplete")
        bb = build("깨진 msd.json", {})
        (bb / "B" / "seed11" / "T600" / "d0.00_cfg0" / "T600" / "msd.json").write_text("{broken")
        vv = verify_run(bb, "B", 11, 600, cv, wt)
        chk(vv["status"] == "invalid" and any("msd.json" in q for q in vv["reasons"]), "⛔음성: 깨진 msd.json → invalid (완료로 안 친다)")
        cv3 = json.loads(json.dumps(cv)); cv3["inputs_sha256"]["A11"] = "0" * 64
        chk(verify_run(base, "A", 11, 600, cv3, wt)["status"] == "invalid", "⛔음성: init sha256 ≠ 카드 → invalid")
        chk(any("sha16" in q for q in verify_run(base, "A", 11, 600, cv, wt_dir(td / "wt2", drv=b"other"))["reasons"]),
            "⛔음성: 판독 시점 드라이버 sha16 ≠ 카드 → invalid")
        (base / "cost_ledger.tsv").rename(base / "cost_ledger.bak")
        v0 = verify_run(base, "A", 11, 600, cv, wt)
        chk(v0["cost_h"] is None and "미확정" in v0["cost_source"] and v0["status"] == "valid", "⛔음성: 장부 없음 → 비용 미확정 (0 아님 · 판정과 별개)")
        (base / "cost_ledger.bak").rename(base / "cost_ledger.tsv")
        # 골격 반례 (회신 DZ P1-6) — NaN · 원소 바뀜 · 프레임 1 개는 유효성에서 먼저 걸린다
        neg("궤적 프레임 1 개 (msd · 끝 줄 있음)", "2 개 미만", {"n_frames": 1})
        # 기록 ⓐ — 기존 S–S 쌍 소멸 (회신 DZ P2-1 반례: 쌍을 2.1 → 4.0 Å 로 · 나머지 그대로)
        bS = td / "b_ss"
        free_idx = [i for i, s in enumerate(a_def.get_chemical_symbols()) if s == "S"][-3:-1]

        def breakf(k, a):
            if k >= 100:
                a.positions[free_idx[1], 2] = a.positions[free_idx[0], 2] + 4.0
            return a
        make_run(bS, "A", 11, 600, cv, a_def, frames_fn=breakf)
        vS = verify_run(bS, "A", 11, 600, dict(cv, inputs_sha256={**cv["inputs_sha256"], "A11": _sha(bS / "A/init/seed11_final.xyz")}),
                        wt, keep_PS=True)
        rS = records_abc(vS["_frames"], vS["_input_atoms"], mq)
        pa = rS["ⓐ_first_frame_SS_pairs"][0]
        chk(vS["status"] == "valid" and not pa["kept_last"] and pa["n_break"] == 1 and abs(pa["frac_frames_kept"] - 100 / 201) < 1e-9,
            "[양성] 기록 ⓐ: 기존 S–S 쌍 소멸을 잡는다 (유지 분율 · 마지막 · 끊김 수 — 골격 ①–④ 는 못 잡는 반례)")
        bP = td / "b_p"

        def p3to4(k, a):
            if k >= 120:
                s_extra = [i for i, s in enumerate(a.get_chemical_symbols()) if s == "S"][-1]
                a.positions[s_extra] = a.positions[5] + tet[3]
            return a
        make_run(bP, "A", 11, 600, cv, a_def, frames_fn=p3to4)
        vP = verify_run(bP, "A", 11, 600, dict(cv, inputs_sha256={**cv["inputs_sha256"], "A11": _sha(bP / "A/init/seed11_final.xyz")}),
                        wt, keep_PS=True)
        rP = records_abc(vP["_frames"], vP["_input_atoms"], mq)
        chk(rP["ⓑ_P_coordination_transitions"].get("3→4") == 1 and rP["ⓑ_P_coord_hist_first_last"]["last"] == {4: 2},
            "[양성] 기록 ⓑ: P 배위 전이 3→4 를 센다")
        # 판독 — 결정 · 허가 · 미완 · W 규칙 (read_run 은 가짜: 판정 함수는 glass_v2_readout selftest 몫)
        dec = td / "dec.json"
        dec.write_text(json.dumps({"decisions": [{"id": i, "decision_state": "active"} for i in NEED_ACTIVE]}))
        card = td / "card.json"

        def write_card(permit):
            c = {"기계_판독_값": {"stage2": {"systems": ["A", "B"], "seeds": [11, 12], "temperatures_K": [600, 650], "prod_ps": 20.0,
                                             "equilib_ps": 5.0, "vseed_offset": 3000},
                                  "md_driver_sha16": cv["md_driver_sha16"], "md_runner_sha16": cv["md_runner_sha16"],
                                  "inputs_sha256": cv["inputs_sha256"]},
                 "입력_2026_11_10": {"시드": {f"{s}{sd}": {"P_S_배위": {"4": 2}, "다리_S": 0, "P_P": 0, "li2s2_판정": "x"} for s in "AB" for sd in (11, 12)}}}
            if permit:
                c[READ_PERMIT_KEY] = {"근거": "시험", "by": "selftest"}
            card.write_text(json.dumps(c, ensure_ascii=False))
        SELF = sys.modules[__name__]                           # 이 모듈 자신 (깨기 사본도 자기 함수를 시험한다) — n_atoms 120 고정을 시험용으로 바꾼다
        SELF_cv = SELF.card_values
        SELF.card_values = lambda p=CARD: dict(SELF_cv(p), n_atoms=len(a_ok))

        def fake_rr(outcome):
            def rr_(msd, n_boot=400, framework=True, mq=None):
                p = pathlib.Path(msd)
                T = int(p.parent.name[1:]); sd = int(p.parents[3].name[4:]); s = p.parents[4].name
                ok = outcome(s, sd, T)
                return {"C1_pass": True, "C1_msd_at_50_mto_A2": 5.0, "beta_MTO": 1.0, "_D_slope": 1e-6,
                        "C2": {"final_verdict": "통과" if ok else "경계 · 구분 불가", "b_end": 64, "b_prev": 48,
                               "n_sigma_end_signed": 0.5, "n_sigma_prev_signed": 0.4},
                        "framework": {"P": {"frac_frames_any_P_changed_vs_first": 0.0}, "S_moved": 0, "SS_new": 0, "S_transient": 0}}
            return rr_
        try:
            write_card(False)
            chk(refuses("판독 보류", SELF.readout, base, wt, card=card, decisions=dec, read_run=fake_rr(lambda *a: True)),
                "⛔음성: 카드에 판독 허가가 없으면 판독하지 않는다 (회신 EB 전)")
            write_card(True)
            dec2 = td / "dec2.json"
            dec2.write_text(json.dumps({"decisions": [{"id": NEED_ACTIVE[0], "decision_state": "active"}]}))
            chk(refuses("active", SELF.readout, base, wt, card=card, decisions=dec2, read_run=fake_rr(lambda *a: True)),
                "⛔음성: 개정 결정이 active 가 아니면 판독하지 않는다")
            o = SELF.readout(base, wt, card=card, decisions=dec, read_run=fake_rr(lambda *a: True))
            chk(o["W"] == [600, 650] and o["cond550_eligible"] and "Ea 차 없음" in o["branch"]
                and "_D_slope" not in json.dumps(o) and all(r.get("records", {}).get("ⓐ_first_frame_SS_pairs") is not None for r in o["rows"]),
                "[양성] 판독: 전부 측정 가능 → W [600, 650] · cond550 자격 · D 값 없음 · 기록 ⓐ–ⓒ")
            o2 = SELF.readout(base, wt, card=card, decisions=dec, read_run=fake_rr(lambda s, sd, T: not (s == "B" and sd == 12 and T == 650)))
            chk(o2["W"] == [600] and o2["measurable"]["B_T650"] is False and o2["measurable"]["A_T650"],
                "⛔음성: B 시드 하나가 650 K 에서 경계 → 650 K 는 W 에 못 든다 (두 시드 모두 · 두 계 모두)")
            o3 = SELF.readout(base, wt, card=card, decisions=dec, read_run=fake_rr(lambda s, sd, T: T != 600))
            chk(o3["W"] == [650] and not o3["cond550_eligible"], "⛔음성: 600 K 측정 불가 → cond550 자격 없음")
            bI = neg("판독용: B12 650 K 끝나지 않음", "msd.json 없음", {"write_msd": False, "rc": None}, sys_="B", sd=12, T=650, want="incomplete")
            (bI / "cost_ledger.tsv").write_text((base / "cost_ledger.tsv").read_text())
            write_card(True)
            card_j = json.loads(card.read_text()); card_j["기계_판독_값"]["inputs_sha256"] = {f"{s}{sd}": _sha(bI / s / "init" / f"seed{sd}_final.xyz") for s in "AB" for sd in (11, 12)}
            card.write_text(json.dumps(card_j, ensure_ascii=False))
            chk(refuses("끝나지 않은 런", SELF.readout, bI, wt, card=card, decisions=dec, read_run=fake_rr(lambda *a: True)),
                "⛔음성: 끝나지 않은 런이 있으면 판독하지 않는다 (다 끝난 뒤 한 번)")
            bV = neg("판독용: A11 600 K rc 7", "종료 코드 7", {"rc": 7}, sys_="A", sd=11, T=600)
            (bV / "cost_ledger.tsv").write_text((base / "cost_ledger.tsv").read_text())
            card_j["기계_판독_값"]["inputs_sha256"] = {f"{s}{sd}": _sha(bV / s / "init" / f"seed{sd}_final.xyz") for s in "AB" for sd in (11, 12)}
            card.write_text(json.dumps(card_j, ensure_ascii=False))
            oV = SELF.readout(bV, wt, card=card, decisions=dec, read_run=fake_rr(lambda *a: True))
            chk(oV["W"] == [650] and oV["measurable"]["A_T600"] is False
                and next(r for r in oV["rows"] if (r["system"], r["seed"], r["T_K"]) == ("A", 11, 600))["exclusion"] == "사후 검증 invalid",
                "⛔음성: 사후 검증 invalid 런은 측정 가능이 아니다 (그 온도는 W 밖 · 사유 기록)")
        finally:
            SELF.card_values = SELF_cv
        # 실제 read_run 한 번 (합성 브라운 · 판정 함수 무변경 경로가 터지지 않는다)
        import msd_diffusive_check as M
        bR = td / "b_rr"
        make_run(bR, "A", 12, 600, dict(cv, prod_ps=110.0), a_ok)
        jp = bR / "A/seed12/T600/d0.00_cfg0/T600/msd.json"
        dd = json.loads(jp.read_text()); dd.update(M.mto_from_traj(jp, SAVE_FS) or {}); jp.write_text(json.dumps(dd))
        rec = G.read_run(jp, n_boot=40, framework=True, mq=mq)
        rw = _row(G, rec)
        chk(not rec.get("error") and rw["C2_final"] is not None and (rw["skeleton"] or {}).get("pass") is not None,
            f"[양성] 실제 read_run (C1 · C2 · 골격) 이 이 꼴의 런 폴더를 읽는다 (110 ps 합성 · {rw['C2_final']})")
    print(f"selftest {'PASS' if not fails else 'FAIL'} — {n_ok}/{n_ok + len(fails)}")
    return 0 if not fails else 1


def main(argv=None):
    if argv is None and "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("verify", "readout"):
        p = sub.add_parser(name)
        p.add_argument("--base", required=True); p.add_argument("--worktree", required=True); p.add_argument("--out", required=True)
    c = sub.add_parser("control")
    c.add_argument("--root_a", required=True); c.add_argument("--root_b", required=True)
    c.add_argument("--seeds", type=int, nargs="+", default=[1, 3]); c.add_argument("--out", required=True)
    A = ap.parse_args(argv)
    if pathlib.Path(A.out).exists():
        raise SystemExit(f"⛔ {A.out} 가 이미 있다 — 덮지 않는다")
    if A.cmd == "verify":
        cv = card_values()
        res = []
        for s in cv["systems"]:
            for sd in cv["seeds"]:
                for T in cv["temperatures"]:
                    v = verify_run(A.base, s, sd, T, cv, A.worktree)
                    res.append({k: v[k] for k in ("system", "seed", "T_K", "status", "reasons", "runner_rc", "cost_h", "cost_source")})
                    print(f"{s}{sd} T{T}: {v['status']}" + (f" — {'; '.join(v['reasons'])[:160]}" if v["reasons"] else ""))
        out = {"kind": "li2s3_stage2_verify/v1", "card_sha256": cv["card_sha256"], "runs": res,
               "⚠": "사후 검증만 — 수송 · 골격 · 기록은 안 읽었다"}
    elif A.cmd == "readout":
        out = readout(A.base, A.worktree)
        print(f"W = {out['W']} · {out['branch']} · cond550 자격 {out['cond550_eligible']}")
    else:
        out = control(A.root_a, A.root_b, tuple(A.seeds))
        print(f"대조 잡: same = {out.get('same')} · {out.get('status') or ''} · 차이 {len(out.get('diffs') or [])} 건")
        for d in (out.get("diffs") or [])[:10]:
            print("  ", d)
    pathlib.Path(A.out).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print(f"-> {A.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
