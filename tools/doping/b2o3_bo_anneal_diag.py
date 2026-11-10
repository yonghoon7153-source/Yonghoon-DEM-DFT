#!/usr/bin/env python3
"""b2o3 B·O 배치 카드 개정 3 — 어닐 시간 진단 (8 단계 판독 전에 박음 · 2026-11-10).

카드 db/properties/b2o3_bo_placement_estimand_2026_11_09.json '개정_3_어닐_시간_진단_2026_11_10'
(결정 D-2026-11-10-b2o3-bo-placement-anneal-time-diagnostic).

  extract — 8 단계 결과를 판독기와 **같은 결속** (판독기의 anneal_readout 을 그대로 부른다) 으로 확인한 뒤,
            성공한 런마다 md.traj 의 50 ps 프레임을 떼어 xyz 로 쓴다 + 출처 JSON (diag_frames.json) +
            실행기용 계획 manifest (b2o3_bo_plan/v1 · 실행 목적 b2o3_bo/anneal_diag_t050 · 이완만).
  judge   — 그 프레임들의 이완 결과 (실행기 TIME_PS=0) 를 이름 · 시작 파일 sha256 · 단계 · 실행 목적으로 결속하고,
            판독기의 anneal_judge 로 50 ps 시점 가족 판독을 한 번 더 낸다 → 본 판독 (100 ps · 같은 판독기로 다시 냄 ·
            --readout 파일과 몸통 대조) 과 견줘 잠정 규칙을 적용한다:
              본 판독이 '승자 F' 이고 50 ps 판독도 F 가 승자 → 승자 F (100 ps 어닐 · 50 ps 시점에도 같은 순서)
              본 판독이 '승자 F' 인데 50 ps 판독이 다른 가족 · 못 가름 · 보류 → UMA 100 ps 어닐로는 못 가른다
              본 판독이 승자 없음 → 그대로 (규칙은 낮추기만 · 올리지 않는다)
            + 기록: 런마다 Δ = E_100 − E_50 (가족별 중앙 · IQR · 최소 · 최대 · 부호 수) · 50 → 100 ps 끝 꼴이 바뀐 런 수.

판독기는 고치지 않는다 — --readout_tool 로 받은 파일 (기본 = 이 파일 옆의 b2o3_bo_readout.py · gabia 에서는 판 고정
$R/src 의 것 · sha256 872d91f7… = 12b8bdef) 을 불러 그 함수를 쓴다. 이 도구는 그 판독기 sha256 을 출력에 남긴다.

쓰는 법
  python3 b2o3_bo_anneal_diag.py --selftest
  python3 b2o3_bo_anneal_diag.py extract --readout_tool <판독기> --verdict s6_verdict.json --receipt s7_receipt.json \
          --results s8_anneal/anneal_results.json --out_dir s8b_frames
  (실행기: CAND=s8b_frames · N_EXPECT=<프레임 수> · TIME_PS=0 · 새 OUTNAME)
  python3 b2o3_bo_anneal_diag.py judge --readout_tool <판독기> --frames s8b_frames/diag_frames.json \
          --relax s8b_relax/anneal_results.json --readout s8_readout.json --out s8b_diag.json

⛔ 이 도구가 못 하는 것
  · 이완을 돌리지 않는다 (실행기 run_uma_kgy.sh 가 돌린다) · 판독 규칙 (G1–G3 · 여유 0.20 · 짝) 을 새로 만들지 않는다
    (판독기의 anneal_judge 를 그대로 부른다).
  · 50 ps 와 100 ps 는 같은 궤적의 앞뒤다 — 두 시점이 같다고 어닐이 수렴했다는 뜻이 아니다 (독립 표본 아님 · 카드).
  · 8 단계에서 실패한 런 (기록이 ok 아님) 은 진단에서도 실패로 센다 (프레임을 떼지 않는다) — 실패 런의 궤적은 믿지 않는다.
  · 잠정 규칙은 Codex 회신 (편지 EA) 으로 바뀔 수 있다 — 바뀌면 카드 개정 4 와 이 도구를 판독 전에 같이 고친다.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DEFAULT_RD = HERE / "b2o3_bo_readout.py"
T_DIAG_PS = 50.0
T_A_REQUIRED = 100
PURPOSE_DIAG = "b2o3_bo/anneal_diag_t050"
CARD_REF = "db/properties/b2o3_bo_placement_estimand_2026_11_09.json#개정_3_어닐_시간_진단_2026_11_10"
NEED = ("anneal_readout", "verify_screen_verdict", "load_records", "identity_problems", "anneal_judge", "end_motif",
        "_frame_index", "_same_geometry", "_sha", "_input", "_core", "_dump", "CONTRACT", "FAM_ORDER")
DISCLAIMER = ("500 K · 100 ps 어닐 뒤 UMA 이완 에너지 기준 — 어닐 길이는 운영 규칙이고 수렴을 뜻하지 않는다 · "
              "50 ps 시점은 같은 궤적의 앞 시점이다 (독립 표본 아님) — 카드 개정 3")
FAILED_WHY = "8 단계 런 실패 — 진단 프레임 없음 (8 단계 판독에서도 실패로 셌다)"


def _sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_rd(path=None):
    """판독기 파일을 불러온다 (그 파일 옆의 run_anneal · b2o3_enumerate 를 판독기가 스스로 불러온다)."""
    p = Path(path or DEFAULT_RD).resolve()
    if not p.is_file():
        raise SystemExit(f"⛔ 판독기 파일이 없다 ({p})")
    spec = importlib.util.spec_from_file_location("b2o3_bo_readout_for_diag", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    miss = [k for k in NEED if not hasattr(mod, k)]
    if miss:
        raise SystemExit(f"⛔ 판독기 {p.name} 에 {miss} 가 없다 — 이 진단이 기대하는 판이 아니다")
    mod.__diag_path__, mod.__diag_sha256__ = str(p), _sha_file(p)
    return mod


def _stage8(RD, verdict, receipt, results):
    """판독기와 같은 결속으로 8 단계 본 판독을 다시 낸다 → (본 판독, 계획, 8 단계 기록)."""
    A100 = RD.anneal_readout(verdict, receipt, results)          # 결속 실패면 판독기가 SystemExit
    if A100.get("t_a_ps") != T_A_REQUIRED:
        raise SystemExit(f"⛔ 파일럿 영수증의 t_a {A100.get('t_a_ps')} ≠ {T_A_REQUIRED} ps — 진단 (50 ps 프레임) 은 "
                         f"t_a 100 ps 에 대해서만 정의됐다 (카드 개정 3)")
    v = RD.verify_screen_verdict(verdict)
    R = RD.load_records(results)
    return A100, v["plan_anneal"], R


def _expected_frames(plan, recs):
    """진단 프레임을 떼어야 하는 이름 = 시작 파일이 있고 8 단계 기록이 ok 인 런."""
    return {e["name"] for e in plan if e["start"] and recs.get(e["name"]) and recs[e["name"]]["ok"]}


def extract(RD, verdict, receipt, results, out_dir, t_diag=T_DIAG_PS):
    from ase import Atoms
    from ase.io import read, write
    from ase.io.trajectory import Trajectory
    A100, plan, R = _stage8(RD, verdict, receipt, results)
    recs = R["records"]
    out_dir = Path(out_dir)
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"⛔ 출력 폴더 {out_dir} 가 비어 있지 않다 — 덮지 않는다 (새 폴더를 준다)")
    out_dir.mkdir(parents=True, exist_ok=True)
    base = Path(R["path"]).parent
    frames, no_start, failed = {}, [], {}
    for e in plan:
        n = e["name"]
        if not e["start"]:
            no_start.append(n)
            continue
        r = recs[n]
        if not r["ok"]:
            failed[n] = [str(w) for w in (r.get("why") or [])[:2]]
            continue
        mt = (r.get("outputs") or {}).get("md_traj")
        if not mt:
            raise SystemExit(f"⛔ {n}: 8 단계 기록에 md_traj 가 없다 — 프레임을 결속할 수 없다")
        k = RD._frame_index(t_diag, mt)                           # 저장 간격의 배수 · 궤적 길이 안 (아니면 SystemExit)
        tp = base / mt["rel"]
        if not tp.is_file() or _sha_file(tp) != mt["sha256"]:
            raise SystemExit(f"⛔ {n}: 궤적 {mt['rel']} 이 없거나 8 단계 기록 뒤 바뀌었다 (sha256)")
        with Trajectory(str(tp)) as T:
            if len(T) != int(mt["n_frames"]):
                raise SystemExit(f"⛔ {n}: 궤적 프레임 {len(T)} ≠ 기록 {mt['n_frames']}")
            fr = T[k]
            a = Atoms(fr.get_chemical_symbols(), positions=fr.get_positions(), cell=fr.cell.array, pbc=fr.pbc)
        f = out_dir / f"{n}_t{int(round(t_diag)):03d}.xyz"
        write(str(f), a)
        if not RD._same_geometry(a, read(str(f))):
            raise SystemExit(f"⛔ {n}: 쓴 프레임 파일이 궤적 프레임 {k} 와 다르다")
        frames[n] = {"rank": e["rank"], "family": e["family"], "frame": int(k),
                     "time_ps": k * float(mt["dt_fs"]) * int(mt["log_every_steps"]) / 1000.0,
                     "file": f.name, "sha256": _sha_file(f), "traj_rel": mt["rel"], "traj_sha256": mt["sha256"],
                     "stage8_identity_sha": r.get("identity_sha")}
    if set(frames) != _expected_frames(plan, recs):
        raise SystemExit("⛔ 뗀 프레임 집합 ≠ 성공한 8 단계 런 집합 (내부 오류)")
    if not frames:
        raise SystemExit("⛔ 떼어낼 프레임이 없다 (성공한 8 단계 런 0)")
    x = {"kind": "b2o3_bo_anneal_diag_frames/v1", "card": CARD_REF, "t_diag_ps": float(t_diag), "t_a_ps": A100["t_a_ps"],
         "purpose": PURPOSE_DIAG, "readout_tool": {"path": RD.__diag_path__, "sha256": RD.__diag_sha256__},
         "inputs": {"screen_verdict": {"path": str(Path(verdict).resolve()), "sha256": _sha_file(verdict)},
                    "pilot_receipt": {"path": str(Path(receipt).resolve()), "sha256": _sha_file(receipt)},
                    "anneal_results": {"path": R["path"], "sha256": R["sha256"]}},
         "plan_n": len(plan), "n_frames": len(frames), "frames": frames, "no_start": no_start, "stage8_failed": failed}
    xp = RD._dump(x, out_dir / "diag_frames.json")
    (out_dir / "manifest.json").write_text(json.dumps(
        {"schema": "b2o3_bo_plan/v1", "stage": "8b_anneal_time_diag_relax", "purpose": PURPOSE_DIAG, "n": len(frames),
         "실행기": f"TIME_PS 0 (이완만) · N_EXPECT {len(frames)} · 새 출력 폴더 (8 단계 폴더와 섞지 않는다)",
         "files": {fr["file"]: {"sha256": fr["sha256"], "name": Path(fr["file"]).stem, "time_ps": int(round(t_diag))}
                   for fr in frames.values()}}, ensure_ascii=False, indent=1) + "\n")
    return Path(xp), x


def apply_rule(A100, A50):
    """잠정 기본 규칙 (카드 개정 3) — 판정을 낮추기만 한다."""
    w100, w50 = A100.get("winner"), A50.get("winner")
    if w100 is None:
        return {"final_winner": None, "final_decision": A100.get("decision"),
                "rule": "본 판독 (100 ps) 이 승자 없음 → 그대로 (규칙은 낮추기만 · 50 ps 판독으로 올리지 않는다)"}
    if w50 == w100:
        return {"final_winner": w100, "final_decision": f"승자 {w100} (100 ps 어닐 · 50 ps 시점에도 같은 순서)",
                "rule": "두 시점에서 같은 가족이 승자 (차 ≥ 여유)"}
    return {"final_winner": None, "final_decision": "UMA 100 ps 어닐로는 못 가른다 (순서가 어닐 시간에 따라 바뀐다)",
            "rule": f"50 ps 판독 = '{A50.get('decision')}' ≠ 100 ps 승자 {w100} → 낮춤"}


def _summ(xs):
    if not xs:
        return {"n": 0}
    q = np.percentile(np.asarray(xs, float), [25, 50, 75])
    return {"n": len(xs), "median": float(q[1]), "q25": float(q[0]), "q75": float(q[2]),
            "min": float(min(xs)), "max": float(max(xs)),
            "n_lower_at_100": sum(1 for x in xs if x < 0), "n_higher_at_100": sum(1 for x in xs if x > 0)}


def delta_stats(RD, plan, recs100, recs50):
    """런마다 Δ = E_100 − E_50 (eV / B₂O₃ 단위) · 끝 꼴 변화 — 두 시점 모두 ok 인 런만."""
    unit = RD.CONTRACT["unit_B2O3"]
    rows, by = [], {F: [] for F in RD.FAM_ORDER}
    for e in plan:
        n = e["name"]
        a, b = recs100.get(n), recs50.get(n)
        if not (a and b and a["ok"] and b["ok"]):
            continue
        d = float(a["E"]) / unit - float(b["E"]) / unit
        m100, m50 = RD.end_motif(a["atoms"]), RD.end_motif(b["atoms"])
        rows.append({"name": n, "family": e["family"], "rank": e["rank"], "dE_100_minus_50_eV": d,
                     "end_motif_50": m50, "end_motif_100": m100})
        by.setdefault(e["family"], []).append(d)
    return {"by_family": {F: _summ(v) for F, v in by.items()}, "all": _summ([r["dE_100_minus_50_eV"] for r in rows]),
            "n_end_motif_changed_50_to_100": sum(1 for r in rows if r["end_motif_50"] != r["end_motif_100"]),
            "rows": rows}


def summary(A):
    fam = {F: {"M": d.get("M"), "n_success": d.get("n_success"), "G1": d.get("G1"), "G3": d.get("G3"),
               "G3_mixed": d.get("G3_mixed"), "min": d.get("min"), "n_failed": len(d.get("failed") or [])}
           for F, d in (A.get("families") or {}).items()}
    return {"decision": A.get("decision"), "winner": A.get("winner"), "order": A.get("order"),
            "winner_runner_up_gap_eV": A.get("winner_runner_up_gap_eV"), "hold_reasons": A.get("hold_reasons"),
            "pairs": A.get("pairs"), "G2_same_composition": A.get("G2_same_composition"), "families": fam}


def judge(RD, frames_json, relax_results, readout_json=None, margin=None):
    xp = Path(frames_json)
    x = json.loads(xp.read_text(encoding="utf-8"))
    if x.get("kind") != "b2o3_bo_anneal_diag_frames/v1":
        raise SystemExit(f"⛔ {xp.name} 는 진단 프레임 출처가 아니다")
    if x.get("purpose") != PURPOSE_DIAG or float(x.get("t_diag_ps", -1)) != T_DIAG_PS:
        raise SystemExit(f"⛔ 진단 프레임 출처의 목적 · 시각 ({x.get('purpose')} · {x.get('t_diag_ps')}) 이 이 도구와 다르다")
    base = xp.resolve().parent
    vp, rp, ap_ = (RD._input(x, k, base) for k in ("screen_verdict", "pilot_receipt", "anneal_results"))
    A100, plan, R100 = _stage8(RD, vp, rp, ap_)
    if readout_json is not None:
        got = json.loads(Path(readout_json).read_text(encoding="utf-8"))
        if RD._core(got) != RD._core(A100):
            raise SystemExit("⛔ 본 판독 파일이 같은 입력에서 다시 낸 본 판독과 다르다 — 바뀐 판독은 쓰지 않는다")
    frames = x.get("frames") or {}
    if set(frames) != _expected_frames(plan, R100["records"]):
        raise SystemExit("⛔ 진단 프레임 출처의 이름 집합 ≠ 성공한 8 단계 런 집합 — 출처가 바뀌었거나 다른 결과에서 나왔다")
    for n, fr in frames.items():
        f = base / fr["file"]
        if not f.is_file() or _sha_file(f) != fr["sha256"]:
            raise SystemExit(f"⛔ {n}: 진단 프레임 파일이 없거나 출처 기록 뒤 바뀌었다 ({fr['file']})")
    RR = RD.load_records(relax_results)
    raw = RR["records"]
    want = {Path(fr["file"]).stem: n for n, fr in frames.items()}
    extra = sorted(set(raw) - set(want))
    if extra:
        raise SystemExit(f"⛔ 진단 이완 결과에 진단 프레임이 아닌 기록 {extra[:2]} — 섞인 폴더 · 판독하지 않는다")
    missing = sorted(set(want) - set(raw))
    if missing:
        raise SystemExit(f"⛔ 진단 이완 결과 누락 {len(missing)} 건 (예 {missing[:2]}) — 누락은 실패가 아니다 · 다 돌린 뒤 판독한다")
    bad = [q for s, n in sorted(want.items())
           for q in RD.identity_problems(s, raw[s], stage="relax_only", input_sha=frames[n]["sha256"], purpose=PURPOSE_DIAG)]
    if bad:
        raise SystemExit(f"⛔ 진단 이완 기록 결속 실패 {len(bad)} 건 (예 {bad[0]}) — 판독하지 않는다")
    recs50 = {n: raw[s] for s, n in want.items()}
    plan50 = [{"name": e["name"], "rank": e["rank"], "family": e["family"], "start": frames.get(e["name"])} for e in plan]
    A50 = RD.anneal_judge(plan50, recs50, margin)
    for d in (A50.get("families") or {}).values():
        for fl in d.get("failed") or []:
            if fl.get("name") in (x.get("stage8_failed") or {}):
                fl["why"] = [FAILED_WHY] + list(x["stage8_failed"][fl["name"]])
    rule = apply_rule(A100, A50)
    out = {"kind": "b2o3_bo_anneal_diag/v1", "card": CARD_REF,
           "inputs": {"diag_frames": {"path": str(xp.resolve()), "sha256": _sha_file(xp)},
                      "diag_relax_results": {"path": RR["path"], "sha256": RR["sha256"]}},
           "readout_tool": {"path": RD.__diag_path__, "sha256": RD.__diag_sha256__},
           "t_diag_ps": T_DIAG_PS, "t_a_ps": A100["t_a_ps"], "at_100ps": summary(A100), "at_50ps": summary(A50),
           **rule, "delta_E": delta_stats(RD, plan, R100["records"], recs50),
           "stage8_failed": x.get("stage8_failed") or {}, "no_start": x.get("no_start") or [], "⚠": DISCLAIMER}
    if readout_json is not None:
        out["inputs"]["stage8_readout"] = {"path": str(Path(readout_json).resolve()), "sha256": _sha_file(readout_json)}
    return out


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    import copy
    import tempfile
    import types
    from ase import Atoms
    from ase.io import read
    from ase.io.trajectory import Trajectory
    n_ok, fails = 0, []

    def chk(c, msg):
        nonlocal n_ok
        if c:
            n_ok += 1
            print(f"  ✔ {msg}")
        else:
            fails.append(msg)
            print(f"  ✘ {msg}")

    def refuses(fn, *a, **k):
        try:
            fn(*a, **k)
        except SystemExit as e:
            return str(e)
        return None

    real = load_rd()
    chk(all(hasattr(real, k) for k in NEED) and real.__diag_sha256__ == _sha_file(DEFAULT_RD),
        "[양성] 이 저장소의 판독기를 불러온다 (필요한 함수 전부 · sha256 기록)")
    chk(refuses(load_rd, "/nonexistent/b2o3_bo_readout.py") is not None, "⛔음성: 판독기 파일이 없으면 멈춘다")

    # 규칙 (낮추기만)
    A = lambda w, d=None: {"winner": w, "decision": d or (f"승자 {w}" if w else "UMA 로는 못 가른다")}
    r = apply_rule(A("F_B"), A("F_B"))
    chk(r["final_winner"] == "F_B" and "50 ps 시점에도 같은 순서" in r["final_decision"], "[양성] 규칙: 두 시점 같은 승자 → 승자 유지")
    r = apply_rule(A("F_B"), A("F_P"))
    chk(r["final_winner"] is None and "못 가른다" in r["final_decision"], "⛔음성: 규칙: 50 ps 승자가 다르면 → 못 가른다로 낮춤")
    r = apply_rule(A("F_B"), A(None))
    chk(r["final_winner"] is None and "못 가른다" in r["final_decision"], "⛔음성: 규칙: 50 ps 가 못 가름 · 보류 → 낮춤")
    r = apply_rule(A(None, "승자 보류"), A("F_B"))
    chk(r["final_winner"] is None and r["final_decision"] == "승자 보류", "⛔음성: 규칙: 본 판독 승자 없음 → 50 ps 로 올리지 않는다 (그대로)")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        FAMS = ["F_B", "F_P", "F_free"]
        plan = []
        for F in FAMS:
            for rk in (1, 2):
                st = None if (F == "F_free" and rk == 2) else {"sha256": f"start-{F}-{rk}"}
                plan.append({"name": f"cfg{rk:02d}_{F}", "rank": rk, "family": F, "start": st})
        no_start_name, failed_name = "cfg02_F_free", "cfg02_F_P"
        E100 = {"cfg01_F_B": -10.0, "cfg02_F_B": -9.8, "cfg01_F_P": -9.5, "cfg02_F_P": None, "cfg01_F_free": -9.0}
        E50 = {"cfg01_F_B": -9.7, "cfg02_F_B": -9.6, "cfg01_F_P": -9.6, "cfg01_F_free": -8.9}

        def make_tree(root, n_frames=101, rec_frames=None):
            root.mkdir(parents=True)
            res = root / "anneal_results.json"
            res.write_text(json.dumps({"results": [], "tag": str(root)}))
            recs = {}
            for e in plan:
                n = e["name"]
                if not e["start"]:
                    continue
                if n == failed_name:
                    recs[n] = {"ok": False, "E": None, "atoms": None, "why": ["상태 unconverged", "x"], "outputs": {}}
                    continue
                (root / n).mkdir()
                tp = root / n / "md.traj"
                with Trajectory(str(tp), "w") as T:
                    for k in range(n_frames):
                        T.write(Atoms("BO2", positions=[[0.01 * k, 0, 0], [1.4, 0, 0], [0, 1.4, 0]], cell=[8, 8, 8], pbc=True))
                mt = {"rel": f"{n}/md.traj", "sha256": _sha_file(tp), "n_frames": rec_frames or n_frames,
                      "log_every_steps": 500, "dt_fs": 2.0, "n_steps": 50000}
                at = Atoms("BO2", positions=[[0, 0, 0], [1.4, 0, 0], [0, 1.4, 0]], cell=[8, 8, 8], pbc=True)
                at.info["motif"] = e["family"]
                recs[n] = {"ok": True, "E": E100[n], "atoms": at, "why": [], "identity_sha": f"id-{n}", "outputs": {"md_traj": mt}}
            return res, {"path": str(res.resolve()), "sha256": _sha_file(res), "records": recs}

        S = {}

        def fake_rd(R100, R50=None, t_a=100, A100=None, A50=None, readout_raise=None):
            def anneal_readout(v, rc, a):
                if readout_raise:
                    raise SystemExit(readout_raise)
                S["readout_calls"] = S.get("readout_calls", 0) + 1
                return copy.deepcopy(A100 or {"t_a_ps": t_a, "winner": "F_B", "decision": "승자 F_B (차저 F_P 와 0.300 ≥ 0.2)",
                                              "order": ["F_B", "F_P", "F_free"], "families": {}})

            def load_records(p):
                if R50 is not None and Path(p).resolve() == Path(R50["path"]).resolve():
                    return R50
                return R100

            def identity_problems(n, r, *, stage, input_sha, time_ps=None, T=None, purpose=None):
                idn = r.get("identity") or {}
                p = []
                if idn.get("stage") != stage:
                    p.append(f"{n}: 단계 {idn.get('stage')} ≠ {stage}")
                if idn.get("input_file_sha256") != input_sha:
                    p.append(f"{n}: 시작 파일이 계획과 다르다")
                if purpose is not None and idn.get("purpose") != purpose:
                    p.append(f"{n}: 실행 목적 {idn.get('purpose')} ≠ {purpose}")
                return p

            def anneal_judge(p50, r50, margin=None):
                S["judge_args"] = (copy.deepcopy([{k: e[k] for k in ("name", "rank", "family")} | {"has_start": bool(e["start"])} for e in p50]),
                                   sorted(r50))
                fams = {F: {"M": 2, "n_success": 0, "failed": [{"name": e["name"], "why": ["시작 구조 없음 (6 단계 실패)"]}
                                                                for e in p50 if e["family"] == F and not e["start"]]} for F in FAMS}
                return copy.deepcopy(A50 or {"winner": "F_B", "decision": "승자 F_B (차저 F_P 와 0.250 ≥ 0.2)", "families": fams}) | {"families": fams}

            ns = types.SimpleNamespace(
                anneal_readout=anneal_readout, verify_screen_verdict=lambda p: {"status": "complete", "plan_anneal": plan},
                load_records=load_records, identity_problems=identity_problems, anneal_judge=anneal_judge,
                end_motif=lambda at: at.info.get("motif", "F_B"), _frame_index=real._frame_index,
                _same_geometry=real._same_geometry, _sha=real._sha, _input=real._input, _core=real._core, _dump=real._dump,
                CONTRACT={"unit_B2O3": 1}, FAM_ORDER=list(FAMS))
            ns.__diag_path__, ns.__diag_sha256__ = "fake_readout.py", "0" * 64
            return ns

        vfile, rfile = td / "s6_verdict.json", td / "s7_receipt.json"
        vfile.write_text('{"v": 1}'); rfile.write_text('{"r": 1}')
        res, R100 = make_tree(td / "s8")
        RD = fake_rd(R100)
        xp, x = extract(RD, vfile, rfile, res, td / "fr")
        fx = {n: read(str(td / "fr" / f["file"])) for n, f in x["frames"].items()}
        man = json.loads((td / "fr" / "manifest.json").read_text())
        chk(sorted(x["frames"]) == ["cfg01_F_B", "cfg01_F_P", "cfg01_F_free", "cfg02_F_B"] and x["no_start"] == [no_start_name]
            and list(x["stage8_failed"]) == [failed_name], "[양성] extract: 성공한 8 단계 런만 프레임 · 시작 없음 · 8 단계 실패를 따로 적는다")
        chk(all(f["frame"] == 50 and abs(f["time_ps"] - 50.0) < 1e-12 for f in x["frames"].values())
            and all(abs(a.positions[0, 0] - 0.50) < 1e-9 for a in fx.values()),
            "[양성] extract: 저장 간격 500 걸음 × 2 fs → 프레임 50 = 50 ps (파일 좌표가 그 프레임)")
        chk(man["purpose"] == PURPOSE_DIAG and man["n"] == 4 and set(man["files"]) == {f["file"] for f in x["frames"].values()}
            and all(v["sha256"] == x["frames"][Path(k).stem.rsplit("_t", 1)[0]]["sha256"] for k, v in man["files"].items()),
            "[양성] extract: 실행기 계획 manifest (목적 · 개수 · 파일 sha256 = 출처)")
        chk(refuses(extract, RD, vfile, rfile, res, td / "fr") is not None, "⛔음성: 출력 폴더가 비어 있지 않으면 덮지 않는다")
        chk("t_a" in (refuses(extract, fake_rd(R100, t_a=20), vfile, rfile, res, td / "fr_ta") or ""),
            "⛔음성: 영수증 t_a 20 → 진단을 시작하지 않는다 (t_a 100 에만 정의)")
        chk("결속 실패" in (refuses(extract, fake_rd(R100, readout_raise="⛔ 어닐 기록 결속 실패 1 건"), vfile, rfile, res, td / "fr_b") or ""),
            "⛔음성: 판독기 결속이 실패하면 그대로 멈춘다 (판독기의 anneal_readout 을 거친다)")
        res2, R2 = make_tree(td / "s8_mod")
        (td / "s8_mod" / "cfg01_F_B" / "md.traj").write_bytes((td / "s8_mod" / "cfg01_F_B" / "md.traj").read_bytes() + b"\0")
        chk("sha256" in (refuses(extract, fake_rd(R2), vfile, rfile, res2, td / "fr_m") or ""),
            "⛔음성: 궤적이 8 단계 기록 뒤 바뀌면 멈춘다 (sha256)")
        res3, R3 = make_tree(td / "s8_short", n_frames=40)
        chk(refuses(extract, fake_rd(R3), vfile, rfile, res3, td / "fr_s") is not None, "⛔음성: 궤적이 50 ps 보다 짧으면 멈춘다 (프레임 40 개)")
        res4, R4 = make_tree(td / "s8_nomt")
        R4["records"]["cfg01_F_P"]["outputs"] = {}
        chk("md_traj" in (refuses(extract, fake_rd(R4), vfile, rfile, res4, td / "fr_n") or ""),
            "⛔음성: 성공 런 기록에 md_traj 가 없으면 멈춘다")
        res5, R5 = make_tree(td / "s8_len", rec_frames=200)
        chk(refuses(extract, fake_rd(R5), vfile, rfile, res5, td / "fr_l") is not None, "⛔음성: 기록 프레임 수 ≠ 실제 궤적 → 멈춘다")

        # judge
        def relax_tree(root, xx, mutate=None):
            root.mkdir(parents=True)
            rr = root / "anneal_results.json"
            rr.write_text(json.dumps({"results": [], "tag": str(root)}))
            recs = {}
            for n, f in xx["frames"].items():
                at = Atoms("BO2", positions=[[0, 0, 0], [1.4, 0, 0], [0, 1.4, 0]], cell=[8, 8, 8], pbc=True)
                at.info["motif"] = "F_P" if n == "cfg02_F_B" else f["family"]
                recs[Path(f["file"]).stem] = {"ok": True, "E": E50[n], "atoms": at, "why": [],
                                               "identity": {"stage": "relax_only", "input_file_sha256": f["sha256"], "purpose": PURPOSE_DIAG}}
            if mutate:
                mutate(recs)
            return rr, {"path": str(rr.resolve()), "sha256": _sha_file(rr), "records": recs}

        rr, R50 = relax_tree(td / "rx", x)
        RDj = fake_rd(R100, R50)
        out = judge(RDj, xp, rr)
        pa, rn = S["judge_args"]
        chk(out["final_winner"] == "F_B" and "50 ps 시점에도 같은 순서" in out["final_decision"], "[양성] judge: 두 시점 같은 승자 → 승자 문장")
        chk(rn == ["cfg01_F_B", "cfg01_F_P", "cfg01_F_free", "cfg02_F_B"]
            and [e["name"] for e in pa if not e["has_start"]] == [failed_name, no_start_name] and len(pa) == len(plan),
            "[양성] judge: anneal_judge 에 계획 이름 그대로 (기록은 계획 이름 키 · 시작 없음 = 6 단계 실패 · 8 단계 실패)")
        fl = [f for d in out["at_50ps"]["families"].values() for f in [d]]
        chk(out["stage8_failed"] == {failed_name: ["상태 unconverged", "x"]} and out["no_start"] == [no_start_name],
            "[양성] judge: 8 단계 실패 · 시작 없음 기록을 같이 낸다")
        dE = out["delta_E"]
        chk(abs(dE["by_family"]["F_B"]["median"] - (-0.25)) < 1e-12 and dE["by_family"]["F_P"]["n"] == 1
            and abs(dE["by_family"]["F_P"]["median"] - 0.1) < 1e-12 and dE["all"]["n"] == 4 and dE["n_end_motif_changed_50_to_100"] == 1,
            "[양성] judge: Δ = E_100 − E_50 가족별 중앙 · 끝 꼴 변화 수")
        chk(out["readout_tool"]["sha256"] == "0" * 64 and out["inputs"]["diag_frames"]["sha256"] == _sha_file(xp),
            "[양성] judge: 판독기 sha256 · 입력 sha256 을 남긴다")
        rd_file = td / "s8_readout.json"
        real._dump({"t_a_ps": 100, "winner": "F_B", "decision": "승자 F_B (차저 F_P 와 0.300 ≥ 0.2)",
                    "order": ["F_B", "F_P", "F_free"], "families": {}}, rd_file)
        chk(judge(RDj, xp, rr, readout_json=rd_file)["final_winner"] == "F_B", "[양성] judge: 본 판독 파일 = 다시 낸 본 판독 → 진행")
        rd_bad = td / "s8_readout_bad.json"
        real._dump({"t_a_ps": 100, "winner": "F_P", "decision": "승자 F_P", "order": ["F_P", "F_B", "F_free"], "families": {}}, rd_bad)
        chk("본 판독 파일" in (refuses(judge, RDj, xp, rr, readout_json=rd_bad) or ""), "⛔음성: 본 판독 파일이 다시 낸 것과 다르면 멈춘다")
        chk(judge(fake_rd(R100, R50, A50={"winner": "F_P", "decision": "승자 F_P"}), xp, rr)["final_winner"] is None,
            "⛔음성: judge: 50 ps 승자가 다르면 → 못 가른다 (낮춤)")
        rr_x, R50x = relax_tree(td / "rx_extra", x, lambda r: r.update({"stray_t050": dict(next(iter(r.values())))}))
        chk("진단 프레임이 아닌" in (refuses(judge, fake_rd(R100, R50x), xp, rr_x) or ""), "⛔음성: 진단 이완 결과에 다른 기록 → 멈춘다")
        rr_m, R50m = relax_tree(td / "rx_miss", x, lambda r: r.pop("cfg01_F_P_t050"))
        chk("누락" in (refuses(judge, fake_rd(R100, R50m), xp, rr_m) or ""), "⛔음성: 진단 이완 결과 누락 → 멈춘다 (누락 ≠ 실패)")
        rr_i, R50i = relax_tree(td / "rx_sha", x, lambda r: r["cfg01_F_B_t050"]["identity"].update(input_file_sha256="0" * 64))
        chk("결속 실패" in (refuses(judge, fake_rd(R100, R50i), xp, rr_i) or ""), "⛔음성: 이완 기록의 시작 파일 sha256 ≠ 프레임 → 멈춘다")
        rr_p, R50p = relax_tree(td / "rx_pur", x, lambda r: r["cfg02_F_B_t050"]["identity"].update(purpose="b2o3_bo/stage8_anneal"))
        chk("결속 실패" in (refuses(judge, fake_rd(R100, R50p), xp, rr_p) or ""), "⛔음성: 이완 기록의 실행 목적 ≠ 진단 → 멈춘다")
        rr_s, R50s = relax_tree(td / "rx_stage", x, lambda r: r["cfg01_F_free_t050"]["identity"].update(stage="anneal_relax"))
        chk("결속 실패" in (refuses(judge, fake_rd(R100, R50s), xp, rr_s) or ""), "⛔음성: 이완 기록이 이완만이 아니면 멈춘다")
        # 프레임 파일 · 묶인 입력 · 출처 변경
        f0 = td / "fr" / x["frames"]["cfg01_F_B"]["file"]
        keep = f0.read_bytes()
        f0.write_bytes(keep + b"\n")
        chk("프레임 파일" in (refuses(judge, RDj, xp, rr) or ""), "⛔음성: 진단 프레임 파일이 출처 기록 뒤 바뀌면 멈춘다")
        f0.write_bytes(keep)
        res_keep = res.read_bytes()
        res.write_bytes(res_keep + b" ")
        chk(refuses(judge, RDj, xp, rr) is not None, "⛔음성: 묶인 입력 (8 단계 결과) 이 바뀌면 멈춘다")
        res.write_bytes(res_keep)
        x2 = json.loads(xp.read_text())
        x2["frames"].pop("cfg01_F_free")
        xp2 = td / "fr" / "diag_frames_edit.json"
        xp2.write_text(json.dumps(x2, ensure_ascii=False))
        chk("이름 집합" in (refuses(judge, RDj, xp2, rr) or ""), "⛔음성: 출처의 프레임 집합 ≠ 성공한 8 단계 런 → 멈춘다")
        x3 = dict(x2, kind="b2o3_bo_pilot_snapshots/v1")
        xp3 = td / "fr" / "diag_frames_kind.json"
        xp3.write_text(json.dumps(x3, ensure_ascii=False))
        chk("출처가 아니다" in (refuses(judge, RDj, xp3, rr) or ""), "⛔음성: 진단 프레임 출처가 아닌 파일 → 멈춘다")
        chk(judge(RDj, xp, rr)["final_winner"] == "F_B", "[양성] 되돌린 뒤 다시 판독 = 같다")

    print(f"selftest {'PASS' if not fails else 'FAIL'} — {n_ok}/{n_ok + len(fails)}")
    return 0 if not fails else 1


def main(argv=None):
    if argv is None and "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("--readout_tool", default=str(DEFAULT_RD))
    e.add_argument("--verdict", required=True); e.add_argument("--receipt", required=True)
    e.add_argument("--results", required=True); e.add_argument("--out_dir", required=True)
    j = sub.add_parser("judge")
    j.add_argument("--readout_tool", default=str(DEFAULT_RD))
    j.add_argument("--frames", required=True); j.add_argument("--relax", required=True)
    j.add_argument("--readout", help="8 단계 본 판독 파일 (있으면 다시 낸 본 판독과 몸통 대조)")
    j.add_argument("--out", required=True)
    A = ap.parse_args(argv)
    RD = load_rd(A.readout_tool)
    print(f"판독기 {RD.__diag_path__} · sha256 {RD.__diag_sha256__}")
    if A.cmd == "extract":
        xp, x = extract(RD, A.verdict, A.receipt, A.results, A.out_dir)
        print(f"-> {xp} · 프레임 {x['n_frames']} 개 (50 ps) · 시작 없음 {len(x['no_start'])} · 8 단계 실패 {len(x['stage8_failed'])}")
        print(f"   실행기: CAND={Path(A.out_dir).resolve()} · N_EXPECT={x['n_frames']} · TIME_PS=0 · 새 OUTNAME")
        return 0
    if Path(A.out).exists():
        raise SystemExit(f"⛔ {A.out} 가 이미 있다 — 덮지 않는다")
    out = judge(RD, A.frames, A.relax, A.readout)
    p = RD._dump(out, A.out)
    print(f"-> {p}")
    print(f"100 ps: {out['at_100ps']['decision']}")
    print(f" 50 ps: {out['at_50ps']['decision']}")
    print(f"최종 (잠정 규칙): {out['final_decision']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
