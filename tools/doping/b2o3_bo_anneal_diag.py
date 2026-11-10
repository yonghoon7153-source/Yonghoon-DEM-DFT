#!/usr/bin/env python3
"""b2o3 B·O 배치 카드 — 어닐 시간 진단 (개정 3 → 개정 4 · 회신 EA · 8 단계 · 50 ps 결과를 열기 전에 고정 · 2026-11-10).

카드 db/properties/b2o3_bo_placement_estimand_2026_11_09.json '개정_4_EA_회신_2026_11_10'
(결정 D-2026-11-10-b2o3-bo-placement-amend4-ea · 개정 3 의 잠정 규칙 · 기록 · 문장을 대체).

  extract — 8 단계 결과를 판 고정 판독기의 anneal_readout 으로 결속 (목적 · 입력 · 설정 · 정체성 · 궤적 sha) 한 뒤
            계획 항목마다 부모 상태를 가른다:
              no_start (6 단계 실패) · parent_failed (상태가 converged · unconverged 아님) · parent_unverified (출력 검증 실패) ·
              parent_no_traj (md_traj 없음) · relax100_failed (100 ps 끝 이완 실패 · 출력 · 궤적은 검증됨) · ok100
            ok100 · relax100_failed 런의 md.traj 에서 50 ps 프레임 (기록의 dt_fs × log_every_steps 로 번호) 을 떼어 xyz 로 쓴다
            + 출처 JSON (diag_frames.json) + 실행기 계획 manifest (실행 목적 b2o3_bo/anneal_diag_t050 · 이완만).
  judge   — 출처를 다시 결속 (부모 상태 · 프레임 파일 sha · **부모 궤적에서 그 프레임을 다시 읽어 원소 순서 · 좌표 · 셀 · PBC 대조**) ·
            진단 이완 결과 (새 폴더 · 이완만 · 진단 목적 · 같은 설정 · 유한 E_post_relax) 를 이름으로 결속 →
            판독기 anneal_judge 로 50 ps 시점 가족 판독 → 본 판독 (100 ps · 그대로 보존) 과 견준 사유 다섯 갈래:
              ⑤ 본 판독 승자 없음 → 그대로 (진단은 올리지 않는다)
              ④ 판독 보류 — 가족별 성공 런 집합이 두 시점에서 다름 · 또는 50 ps 판독 보류 (게이트)
              ③ 50 ps 여유 부족 (게이트 통과 · 승자–차점 < 0.20)
              ② 다른 승자
              ① 같은 선택 — 두 시점 모두 같은 초기 가족이 여유 ≥ 0.20 으로 선택 (같은 성공 집합)
            + 기록: 런별 E · Δ = E_100 − E_50 · 시점별 상태 (결측은 결측) · 가족별 Δ 중앙 · IQR · 최솟값 · 최댓값 · max|Δ| ·
              두 시점 최저 런 ID · 끝 꼴 · 그 Δ · 최저 간 차 m_G(t) − m_F(t) 와 변화 · 같은 바탕 짝 변화 δ_FG,i · 가족별 E 중앙 ·
              판독기 짝 판정 · md.log Epot · T 구간 평균 ([40,50] · [90,100] ps · 기록만).

판독기는 고치지 않는다 — --readout_tool (기본 = 이 파일 옆 · gabia 는 판 고정 $R/src · sha256 872d91f7… = 12b8bdef) 의 함수를 부른다.

쓰는 법
  python3 b2o3_bo_anneal_diag.py --selftest
  python3 b2o3_bo_anneal_diag.py extract --readout_tool <판독기> --verdict s6_verdict.json --receipt s7_receipt.json \
          --results s8_anneal/anneal_results.json --out_dir s8b_frames
  (실행기: CAND=s8b_frames · N_EXPECT=<프레임 수> · TIME_PS=0 · 새 OUTNAME)
  python3 b2o3_bo_anneal_diag.py judge --readout_tool <판독기> --frames s8b_frames/diag_frames.json \
          --relax s8b_relax/anneal_results.json --readout s8_readout.json --out s8b_diag.json

⛔ 이 도구가 못 하는 것
  · 이완을 돌리지 않는다 (실행기 run_uma_kgy.sh) · 판정 규칙 (G1–G3 · 여유 0.20 · 짝) 을 새로 만들지 않는다 (anneal_judge 그대로).
  · 두 시점 일치는 같은 궤적의 앞뒤라 시간 수렴 · 독립 재현 · 전역 최저의 증거가 아니다 · 전체 가족 순서 · 같은 구조 골짜기를 뜻하지 않는다.
  · 공통 성공 집합으로 다시 판독하지 않는다 (분모를 바꾸지 않는다 · 집합이 다르면 ④).
  · md.log 는 실행기 기록에 sha 가 없어 결속이 약하다 — 구간 평균은 기록만 (판정에 안 쓴다 · 열적 배치 에너지 ≠ 이완 끝점 에너지).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
DEFAULT_RD = HERE / "b2o3_bo_readout.py"
T_DIAG_PS = 50.0
T_A_REQUIRED = 100
PURPOSE_DIAG = "b2o3_bo/anneal_diag_t050"
CARD_REF = "db/properties/b2o3_bo_placement_estimand_2026_11_09.json#개정_4_EA_회신_2026_11_10"
MDLOG_WINDOWS_PS = ((40.0, 50.0), (90.0, 100.0))
NEED = ("anneal_readout", "verify_screen_verdict", "load_records", "identity_problems", "anneal_judge", "end_motif",
        "_frame_index", "_same_geometry", "_sha", "_input", "_core", "_dump", "CONTRACT", "FAM_ORDER")
FRAMED = ("ok100", "relax100_failed")
PARENT_WHY = {"no_start": "시작 구조 없음 (6 단계 실패)", "parent_failed": "부모 런 실패 (상태가 converged · unconverged 아님) — 궤적 없음",
              "parent_unverified": "부모 기록 출력 검증 실패 — 궤적을 믿지 않는다", "parent_no_traj": "부모 기록에 md_traj 없음 — 50 ps 프레임 없음"}
SENT = {
 "①": ("선언한 초기점 생성·탐색 절차에서, 초기 가족 {F}의 최저 이완 에너지가 500 K·100 ps 어닐 뒤 가장 낮았다. 동일한 유효 런 집합의 "
       "50 ps 판독에서도 같은 가족이 선택됐으며, 두 시점 모두 차점과의 차가 0.20 eV/B₂O₃ 이상이었다. 이는 두 시점의 선택 일치이며, "
       "어닐 시간 수렴·독립 재현·전역 최저 상태를 뜻하지 않는다."),
 "②": "50 ps와 100 ps에서 선택된 초기 가족이 달라, 이번 탐색에서는 시간에 일관된 승자를 보고하지 않는다.",
 "③": "100 ps에서는 승자 문턱을 만족했으나, 50 ps에서는 여유가 부족해 두 시점 일치 조건을 충족하지 못했다.",
 "④": "시간 비교의 유효성 조건이 충족되지 않아 최종 승자 서술을 보류한다.",
}
DISCLAIMER = ("초기 가족 라벨 (F_B · F_P · F_free) 은 출발 꼴이다 — 최저 구조의 끝 꼴을 같이 본다 · 어닐 길이는 운영 규칙 · "
              "두 시점 일치는 시간 수렴 · 독립 재현 · 전역 최저의 증거가 아니다 (카드 개정 4)")


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


def _stage8(RD, verdict, receipt, results, k_f=None):
    """판 고정 판독기와 같은 결속으로 8 단계 본 판독을 다시 낸다 → (본 판독, 계획, 8 단계 기록)."""
    A100 = RD.anneal_readout(verdict, receipt, results, k_f=k_f)   # 결속 실패면 판독기가 SystemExit
    if A100.get("t_a_ps") != T_A_REQUIRED:
        raise SystemExit(f"⛔ 파일럿 영수증의 t_a {A100.get('t_a_ps')} ≠ {T_A_REQUIRED} ps — 진단 (50 ps 프레임) 은 "
                         f"t_a 100 ps 에 대해서만 정의됐다 (카드 개정 3 · 4)")
    plan = RD.verify_screen_verdict(verdict, k_f)["plan_anneal"]
    names = [e["name"] for e in plan]
    if len(set(names)) != len(names):
        raise SystemExit("⛔ 계획에 같은 이름이 둘 — 이름으로 결속할 수 없다")
    return A100, plan, RD.load_records(results)


def parent_status(e, r):
    """계획 항목 하나의 부모 상태 (8 단계 기록 기준)."""
    if not e["start"]:
        return "no_start"
    if r is None:
        raise SystemExit(f"⛔ {e['name']}: 시작 파일이 있는 계획 항목의 8 단계 기록이 없다")
    if r.get("status") not in ("converged", "unconverged"):
        return "parent_failed"
    if r.get("vo"):
        return "parent_unverified"
    if not (r.get("outputs") or {}).get("md_traj"):
        return "parent_no_traj"
    return "ok100" if r["ok"] else "relax100_failed"


def _read_frame(RD, base, mt, t):
    """검증된 부모 기록의 md_traj → (프레임 번호, 원자) — 번호는 기록의 dt_fs × log_every_steps (판독기 _frame_index)."""
    from ase import Atoms
    from ase.io.trajectory import Trajectory
    k = RD._frame_index(t, mt)
    tp = Path(base) / mt["rel"]
    if not tp.is_file() or _sha_file(tp) != mt["sha256"]:
        raise SystemExit(f"⛔ 궤적 {mt['rel']} 이 없거나 8 단계 기록 뒤 바뀌었다 (sha256)")
    with Trajectory(str(tp)) as T:
        if len(T) != int(mt["n_frames"]):
            raise SystemExit(f"⛔ 궤적 {mt['rel']} 프레임 {len(T)} ≠ 기록 {mt['n_frames']}")
        fr = T[k]
        a = Atoms(fr.get_chemical_symbols(), positions=fr.get_positions(), cell=fr.cell.array, pbc=fr.pbc)
    return int(k), a


def extract(RD, verdict, receipt, results, out_dir, t_diag=T_DIAG_PS, k_f=None):
    from ase.io import read, write
    A100, plan, R = _stage8(RD, verdict, receipt, results, k_f)
    recs = R["records"]
    out_dir = Path(out_dir)
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"⛔ 출력 폴더 {out_dir} 가 비어 있지 않다 — 덮지 않는다 (새 폴더를 준다)")
    out_dir.mkdir(parents=True, exist_ok=True)
    base = Path(R["path"]).parent
    status = {e["name"]: parent_status(e, recs.get(e["name"])) for e in plan}
    frames = {}
    for e in plan:
        n = e["name"]
        if status[n] not in FRAMED:
            continue
        mt = recs[n]["outputs"]["md_traj"]
        k, a = _read_frame(RD, base, mt, t_diag)
        f = out_dir / f"{n}_t{int(round(t_diag)):03d}.xyz"
        write(str(f), a)
        if not RD._same_geometry(a, read(str(f))):
            raise SystemExit(f"⛔ {n}: 쓴 프레임 파일이 궤적 프레임 {k} 와 다르다")
        frames[n] = {"base": e["rank"], "family": e["family"], "frame": k,
                     "time_ps": k * float(mt["dt_fs"]) * int(mt["log_every_steps"]) / 1000.0,
                     "file": f.name, "sha256": _sha_file(f), "traj_rel": mt["rel"], "traj_sha256": mt["sha256"],
                     "stage8_identity_sha": recs[n].get("identity_sha")}
    if not frames:
        raise SystemExit("⛔ 떼어낼 프레임이 없다 (궤적이 검증된 8 단계 런 0)")
    x = {"kind": "b2o3_bo_anneal_diag_frames/v2", "card": CARD_REF, "t_diag_ps": float(t_diag), "t_a_ps": A100["t_a_ps"],
         "purpose": PURPOSE_DIAG, "readout_tool": {"path": RD.__diag_path__, "sha256": RD.__diag_sha256__},
         "inputs": {"screen_verdict": {"path": str(Path(verdict).resolve()), "sha256": _sha_file(verdict)},
                    "pilot_receipt": {"path": str(Path(receipt).resolve()), "sha256": _sha_file(receipt)},
                    "anneal_results": {"path": R["path"], "sha256": R["sha256"]}},
         "plan_n": len(plan), "n_frames": len(frames), "parent_status": status, "frames": frames}
    xp = RD._dump(x, out_dir / "diag_frames.json")
    (out_dir / "manifest.json").write_text(json.dumps(
        {"schema": "b2o3_bo_plan/v1", "stage": "8b_anneal_time_diag_relax", "purpose": PURPOSE_DIAG, "n": len(frames),
         "실행기": f"TIME_PS 0 (이완만) · N_EXPECT {len(frames)} · 새 출력 폴더 (8 단계 폴더와 섞지 않는다)",
         "files": {fr["file"]: {"sha256": fr["sha256"], "name": Path(fr["file"]).stem, "time_ps": int(round(t_diag))}
                   for fr in frames.values()}}, ensure_ascii=False, indent=1) + "\n")
    return Path(xp), x


def verdict_reason(A100, A50, sets_equal):
    """사유 다섯 갈래 (카드 개정 4 · 평가 순서 ⑤ → ④ → ③ → ② → ①) — 본 판독을 올리지 않는다."""
    w100, w50 = A100.get("winner"), A50.get("winner")
    if w100 is None:
        return {"code": "⑤", "reason": "본 판독 (100 ps) 승자 없음 — 그대로 (진단은 올리지 않는다)", "final_winner": None,
                "final_decision": A100.get("decision"), "sentence": None}
    if not sets_equal:
        return {"code": "④", "reason": "판독 보류 — 가족별 성공 런 집합이 두 시점에서 다르다 (시간 효과와 비교 대상 변경이 섞인다)",
                "final_winner": None, "final_decision": "최종 승자 서술 보류 (100 ps 본 판정은 보존)", "sentence": SENT["④"]}
    if A50.get("hold_reasons"):
        return {"code": "④", "reason": f"판독 보류 — 50 ps 판독 보류 ({'; '.join(A50['hold_reasons'])[:200]})",
                "final_winner": None, "final_decision": "최종 승자 서술 보류 (100 ps 본 판정은 보존)", "sentence": SENT["④"]}
    if w50 is None:
        return {"code": "③", "reason": f"50 ps 여유 부족 ({A50.get('decision')})", "final_winner": None,
                "final_decision": "두 시점 일치 미충족 — 50 ps 여유 부족 (100 ps 본 판정은 보존)", "sentence": SENT["③"]}
    if w50 != w100:
        return {"code": "②", "reason": f"다른 승자 (100 ps {w100} · 50 ps {w50})", "final_winner": None,
                "final_decision": "시간에 일관된 승자 없음 (100 ps 본 판정은 보존)", "sentence": SENT["②"]}
    return {"code": "①", "reason": f"같은 선택 ({w100} · 두 시점 모두 여유 ≥ 문턱)", "final_winner": w100,
            "final_decision": f"두 시점에서 같은 가족 ({w100}) 이 선택됐다", "sentence": SENT["①"].format(F=w100)}


def _summ(xs):
    if not xs:
        return {"n": 0}
    q = np.percentile(np.asarray(xs, float), [25, 50, 75])
    return {"n": len(xs), "median": float(q[1]), "q25": float(q[0]), "q75": float(q[2]), "IQR": float(q[2] - q[0]),
            "min": float(min(xs)), "max": float(max(xs)), "max_abs": float(max(abs(x) for x in xs)),
            "n_lower_at_100": sum(1 for x in xs if x < 0), "n_higher_at_100": sum(1 for x in xs if x > 0)}


def _why(r):
    return "; ".join(str(w) for w in (r or {}).get("why", [])[:2]) or "기록 없음"


def build_records(RD, plan, recs100, recs50, status, A100, A50):
    unit = RD.CONTRACT["unit_B2O3"]
    FAM = list(RD.FAM_ORDER)
    rows = []
    for e in plan:
        n, F, b = e["name"], e["family"], e["rank"]
        a, c = recs100.get(n), recs50.get(n)
        E100 = float(a["E"]) / unit if (a and a["ok"]) else None
        E50 = float(c["E"]) / unit if (c and c["ok"]) else None
        st = status[n]
        rows.append({"name": n, "base": b, "family": F, "parent_status": st,
                     "status_100": "ok" if E100 is not None else (PARENT_WHY.get(st) or f"실패 — {_why(a)}"),
                     "status_50": "ok" if E50 is not None else (PARENT_WHY.get(st) or f"실패 — {_why(c)}"),
                     "E_100": E100, "E_50": E50, "dE_100_minus_50": (E100 - E50) if (E100 is not None and E50 is not None) else None,
                     "end_motif_100": RD.end_motif(a["atoms"]) if E100 is not None else None,
                     "end_motif_50": RD.end_motif(c["atoms"]) if E50 is not None else None})
    by = {F: [r["dE_100_minus_50"] for r in rows if r["family"] == F and r["dE_100_minus_50"] is not None] for F in FAM}
    dE = {r["name"]: r["dE_100_minus_50"] for r in rows}
    minima = {}
    for t, A in (("50", A50), ("100", A100)):
        minima[t] = {}
        for F in FAM:
            m = ((A.get("families") or {}).get(F) or {}).get("min")
            minima[t][F] = (None if not m else {"name": m["name"], "base": m["rank"], "E": m["E"], "end_motif": m["end_motif"],
                                                "dE_100_minus_50_of_this_run": dE.get(m["name"])})
    gaps = {}
    for F, G in itertools.combinations(FAM, 2):
        g = {t: (minima[t][G]["E"] - minima[t][F]["E"]) if (minima[t][F] and minima[t][G]) else None for t in ("50", "100")}
        gaps[f"m_{G} − m_{F}"] = {"50": g["50"], "100": g["100"],
                                  "change_100_minus_50": (g["100"] - g["50"]) if None not in g.values() else None}
    cell = {(r["base"], r["family"]): r["dE_100_minus_50"] for r in rows}
    paired = {}
    for F, G in itertools.combinations(FAM, 2):
        vals = []
        for b in sorted({r["base"] for r in rows}):
            u, w = cell.get((b, F)), cell.get((b, G))
            if u is not None and w is not None:
                vals.append({"base": b, "delta": u - w})
        xs = [v["delta"] for v in vals]
        paired[f"δ_{F}{G} = Δ_{F} − Δ_{G}"] = {"n": len(xs), "median": float(np.median(xs)) if xs else None,
                                               "min": min(xs) if xs else None, "max": max(xs) if xs else None, "per_base": vals}
    med = {t: {F: (float(np.median(v)) if (v := [r[f"E_{t}"] for r in rows if r["family"] == F and r[f"E_{t}"] is not None]) else None)
               for F in FAM} for t in ("50", "100")}
    return {"rows": rows, "delta_by_family": {F: _summ(v) for F, v in by.items()},
            "delta_all": _summ([x for v in by.values() for x in v]),
            "n_end_motif_changed_50_to_100": sum(1 for r in rows if r["end_motif_50"] and r["end_motif_100"]
                                                 and r["end_motif_50"] != r["end_motif_100"]),
            "family_minimum": minima, "family_minimum_gaps": gaps, "paired_change": paired, "family_median_E": med,
            "pairs_verdict": {"50": A50.get("pairs"), "100": A100.get("pairs")}}


def mdlog_windows(base, plan, status, windows=MDLOG_WINDOWS_PS):
    """8 단계 md.log (ASE MDLogger) 의 Epot · T 구간 평균 — 기록만. 없거나 못 읽으면 결측 (지어내지 않는다)."""
    out = {}
    for e in plan:
        n = e["name"]
        if status[n] in ("no_start", "parent_failed"):
            out[n] = {"status": PARENT_WHY[status[n]]}
            continue
        p = Path(base) / n / "md.log"
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            hdr = lines[0].split()
            it, ie, iT = hdr.index("Time[ps]"), hdr.index("Epot[eV]"), hdr.index("T[K]")
        except (OSError, IndexError, ValueError):
            out[n] = {"status": "md.log 없음 · 못 읽음"}
            continue
        vals = []
        for ln in lines[1:]:
            q = ln.split()
            try:
                vals.append((float(q[it]), float(q[ie]), float(q[iT])))
            except (IndexError, ValueError):
                continue
        rec = {}
        for lo, hi in windows:
            w = [(E, T) for t, E, T in vals if lo - 1e-9 <= t <= hi + 1e-9 and math.isfinite(E) and math.isfinite(T)]
            rec[f"{lo:g}-{hi:g}ps"] = ({"n": len(w), "Epot_mean_eV": float(np.mean([x[0] for x in w])),
                                        "T_mean_K": float(np.mean([x[1] for x in w]))} if w else {"n": 0})
        k1, k2 = (f"{lo:g}-{hi:g}ps" for lo, hi in windows)
        if rec[k1].get("n") and rec[k2].get("n"):
            rec["Epot_change_eV"] = rec[k2]["Epot_mean_eV"] - rec[k1]["Epot_mean_eV"]
            rec["T_change_K"] = rec[k2]["T_mean_K"] - rec[k1]["T_mean_K"]
        out[n] = rec
    return {"windows_ps": [list(w) for w in windows], "per_run": out,
            "⚠": "기록만 — 열적 배치 에너지 (MD 중) 는 이완 끝점 에너지와 다른 양 · md.log 는 기록에 sha 가 없다 · D1 을 대신하지 않는다"}


def summary(A):
    fam = {F: {"M": d.get("M"), "n_success": d.get("n_success"), "need_G1": d.get("need_G1"), "G1": d.get("G1"),
               "G3": d.get("G3"), "G3_mixed": d.get("G3_mixed"), "min": d.get("min"),
               "failed": [{"name": f.get("name"), "why": f.get("why")} for f in (d.get("failed") or [])]}
           for F, d in (A.get("families") or {}).items()}
    return {"decision": A.get("decision"), "winner": A.get("winner"), "order": A.get("order"),
            "winner_runner_up_gap_eV": A.get("winner_runner_up_gap_eV"), "hold_reasons": A.get("hold_reasons"),
            "pairs": A.get("pairs"), "G2_same_composition": A.get("G2_same_composition"), "families": fam}


def judge(RD, frames_json, relax_results, readout_json=None, margin=None, k_f=None):
    from ase.io import read
    xp = Path(frames_json)
    x = json.loads(xp.read_text(encoding="utf-8"))
    if x.get("kind") != "b2o3_bo_anneal_diag_frames/v2":
        raise SystemExit(f"⛔ {xp.name} 는 진단 프레임 출처 (v2) 가 아니다")
    if x.get("purpose") != PURPOSE_DIAG or float(x.get("t_diag_ps", -1)) != T_DIAG_PS:
        raise SystemExit(f"⛔ 진단 프레임 출처의 목적 · 시각 ({x.get('purpose')} · {x.get('t_diag_ps')}) 이 이 도구와 다르다")
    base = xp.resolve().parent
    vp, rp, ap_ = (RD._input(x, k, base) for k in ("screen_verdict", "pilot_receipt", "anneal_results"))
    A100, plan, R100 = _stage8(RD, vp, rp, ap_, k_f)
    if readout_json is not None:
        got = json.loads(Path(readout_json).read_text(encoding="utf-8"))
        if RD._core(got) != RD._core(A100):
            raise SystemExit("⛔ 본 판독 파일이 같은 입력에서 다시 낸 본 판독과 다르다 — 바뀐 판독은 쓰지 않는다")
    recs100 = R100["records"]
    status = {e["name"]: parent_status(e, recs100.get(e["name"])) for e in plan}
    if status != x.get("parent_status"):
        raise SystemExit("⛔ 출처의 부모 상태가 8 단계 기록에서 다시 낸 것과 다르다 — 출처가 바뀌었거나 다른 결과에서 나왔다")
    frames = x.get("frames") or {}
    if set(frames) != {n for n, s in status.items() if s in FRAMED}:
        raise SystemExit("⛔ 진단 프레임 이름 집합 ≠ 궤적이 검증된 8 단계 런 집합")
    base100 = Path(R100["path"]).parent
    fam_of = {e["name"]: (e["rank"], e["family"]) for e in plan}
    for n, fr in frames.items():
        if (fr.get("base"), fr.get("family")) != fam_of[n]:
            raise SystemExit(f"⛔ {n}: 출처의 바탕 · 초기 가족이 계획과 다르다")
        f = base / fr["file"]
        if not f.is_file() or _sha_file(f) != fr["sha256"]:
            raise SystemExit(f"⛔ {n}: 진단 프레임 파일이 없거나 출처 기록 뒤 바뀌었다 ({fr['file']})")
        mt = recs100[n]["outputs"]["md_traj"]
        k, a = _read_frame(RD, base100, mt, T_DIAG_PS)
        if fr.get("frame") != k or fr.get("traj_sha256") != mt["sha256"]:
            raise SystemExit(f"⛔ {n}: 출처의 프레임 {fr.get('frame')} · 궤적 sha 가 기록 시간축의 50 ps 프레임 {k} 과 다르다")
        if not RD._same_geometry(a, read(str(f))):
            raise SystemExit(f"⛔ {n}: 진단 입력이 부모 궤적의 50 ps 프레임과 다르다 (원소 순서 · 좌표 · 셀 · PBC)")
    RR = RD.load_records(relax_results)
    if Path(RR["path"]).resolve().parent == base100.resolve():
        raise SystemExit("⛔ 진단 이완 결과가 8 단계 폴더에 있다 — 새 출력 폴더여야 한다")
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
            if status.get(fl.get("name")) not in FRAMED:
                fl["why"] = [PARENT_WHY[status[fl["name"]]] + " — 50 ps 프레임 없음"]
    FAM = list(RD.FAM_ORDER)
    S = {t: {F: sorted(e["name"] for e in plan if e["family"] == F and (rr.get(e["name"]) or {}).get("ok"))
             for F in FAM} for t, rr in (("100", recs100), ("50", recs50))}
    sets_equal = all(S["100"][F] == S["50"][F] for F in FAM)
    v = verdict_reason(A100, A50, sets_equal)
    out = {"kind": "b2o3_bo_anneal_diag/v2", "card": CARD_REF,
           "inputs": {"diag_frames": {"path": str(xp.resolve()), "sha256": _sha_file(xp)},
                      "diag_relax_results": {"path": RR["path"], "sha256": RR["sha256"]}},
           "readout_tool": {"path": RD.__diag_path__, "sha256": RD.__diag_sha256__},
           "t_diag_ps": T_DIAG_PS, "t_a_ps": A100["t_a_ps"],
           "at_100ps_main_readout_preserved": summary(A100), "at_50ps": summary(A50),
           "success_sets": {F: {"100": S["100"][F], "50": S["50"][F], "same": S["100"][F] == S["50"][F]} for F in FAM},
           "verdict": v, "records": build_records(RD, plan, recs100, recs50, status, A100, A50),
           "md_log": mdlog_windows(base100, plan, status), "parent_status": status, "⚠": DISCLAIMER}
    if readout_json is not None:
        out["inputs"]["stage8_readout"] = {"path": str(Path(readout_json).resolve()), "sha256": _sha_file(readout_json)}
    return out


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    import copy
    import shutil
    import tempfile
    from ase import Atoms
    from ase.io import read, write
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

    def refuses(kw, fn, *a, **k):
        """그 이유로 거부해야 통과 — 다른 데서 멈추거나 터진 것은 빨간불."""
        try:
            fn(*a, **k)
        except SystemExit as e:
            return kw in str(e)
        except Exception as e:                      # 거부가 아니라 터짐
            print(f"     (터짐 {type(e).__name__}: {e})")
            return False
        return False

    RD = load_rd()
    chk(all(hasattr(RD, k) for k in NEED) and RD.__diag_sha256__ == _sha_file(DEFAULT_RD),
        "[양성] 이 저장소의 판독기를 불러온다 (필요한 함수 전부 · sha256 기록)")
    chk(refuses("판독기 파일이 없다", load_rd, "/nonexistent/b2o3_bo_readout.py"), "⛔음성: 판독기 파일이 없으면 멈춘다")

    # ── (1) 사유 다섯 갈래 (회신 EA 반례 꼴) ──────────────────────────────
    A = lambda w, d=None, hold=None: {"winner": w, "decision": d or (f"승자 {w}" if w else "UMA 로는 못 가른다 (승자–차저 0.100 < 0.2)"),
                                      "hold_reasons": hold}
    v = verdict_reason(A("F_B"), A("F_B"), True)
    chk(v["code"] == "①" and v["final_winner"] == "F_B" and "같은 가족이 선택" in v["sentence"] and "순서" not in v["final_decision"],
        "[양성] ① 같은 선택 → '두 시점에서 같은 가족이 선택됐다' (차점이 바뀌어도 '같은 순서' 라 쓰지 않는다 · EA runner_up_changed)")
    v = verdict_reason(A("F_B"), A(None), True)
    chk(v["code"] == "③" and v["final_winner"] is None and "바뀌" not in v["sentence"] + v["final_decision"],
        "⛔음성: ③ 50 ps 여유 부족 → 순서 역전이라 쓰지 않는다 (EA margin_only)")
    v = verdict_reason(A("F_B"), A(None, "승자 보류", ["F_P: G1 실패 (성공 14 < 15 · 탈락)"]), True)
    chk(v["code"] == "④" and v["final_winner"] is None and "바뀌" not in v["sentence"], "⛔음성: ④ 50 ps 판독 보류 → 판독 보류 (EA unavailable_50)")
    v = verdict_reason(A("F_B"), A("F_P"), True)
    chk(v["code"] == "②" and v["final_winner"] is None, "⛔음성: ② 다른 승자 → 시간에 일관된 승자 없음")
    v = verdict_reason(A("F_B"), A("F_B"), False)
    chk(v["code"] == "④" and v["final_winner"] is None, "⛔음성: ④ 성공 집합이 두 시점에서 다르면 같은 승자여도 보류 (EA false_same_winner)")
    v = verdict_reason(A(None, "UMA 로는 못 가른다"), A("F_B"), True)
    chk(v["code"] == "⑤" and v["final_winner"] is None and v["final_decision"] == "UMA 로는 못 가른다",
        "⛔음성: ⑤ 본 판독 승자 없음 → 50 ps 로 올리지 않는다 (그대로)")

    # ── (2) 실제 판독기 사슬 — 생성 manifest → 거름 → 파일럿 → 영수증 → 8 단계 (md_traj) → 진단 (정상 · 음성 경로) ──
    RA, EN, C = RD._RA, RD._EN, RD.CONTRACT
    FAM = list(RD.FAM_ORDER)
    code = {"F_B": "bo4", "F_P": "distributed", "F_free": "free_s"}
    BASE = 20261109

    def toy(kind, shift=0.0):
        B, P = np.array([2.0, 2, 2]), np.array([8.0, 8, 8])
        dirs = np.eye(3)
        O = {"F_B": [B + 1.45 * d for d in dirs], "F_P": [P - 1.55 * d for d in dirs],
             "F_free": [np.array([5.0, 5, 5]) + 0.8 * d for d in dirs]}[kind]
        return Atoms("BPO3S", positions=[B, P] + O + [np.array([10.0, 2, 10]) + shift], cell=[12, 12, 12], pbc=True)

    def idn(sha, stage, time_ps=0.0, T=500.0, purpose=None, seed=1, **over):
        d = {"input_file_sha256": sha, "input_struct": "x", "n_atoms": 6, "stage": stage, "temperature_K": float(T),
             "time_ps": float(time_ps), "dt_fs": 2.0, "friction": 0.01, "relax_steps": 1500, "relax_fmax": 0.05,
             "cell_relax": True, "seed": seed, "model": "uma-s-1p1/omat"}
        if purpose is not None:
            d["purpose"] = purpose
        d.update(over)
        return d

    def put(d, n, kind, E, status, ident, traj=None, mdlog_E=None):
        w = d / n
        w.mkdir(parents=True, exist_ok=True)
        a = toy(kind)
        for k in ("post_md", "post_relax"):
            write(str(w / f"{k}.xyz"), a)
        if status == "failed":
            return {"name": n, "status": "failed", "error": "x", "identity": ident, "identity_sha": RA.identity_sha(ident)}
        rec = {"name": n, "status": status, "converged": status == "converged", "E_post_relax": E, "identity": ident,
               "identity_sha": RA.identity_sha(ident), "composition": RA._composition(a),
               "outputs": {k: {"rel": f"{n}/{k}.xyz", "sha256": RA._file_sha256(w / f"{k}.xyz")} for k in ("post_md", "post_relax")}}
        if traj:
            nf, dt, le, ns = traj
            T_ = Trajectory(str(w / "md.traj"), "w")
            for k in range(nf):
                T_.write(toy(kind, shift=0.001 * k))
            T_.close()
            rec["outputs"]["md_traj"] = {"rel": f"{n}/md.traj", "sha256": RA._file_sha256(w / "md.traj"),
                                         "n_frames": nf, "log_every_steps": le, "dt_fs": dt, "n_steps": ns}
        if mdlog_E is not None:
            rows = ["Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]"]
            rows += [f"{t:<10.4f} {mdlog_E:.4f} {mdlog_E + 0.001 * t:.6f} 0.0 {500.0 + (t % 5):.1f}" for t in range(101)]
            (w / "md.log").write_text("\n".join(rows) + "\n")
        return rec

    def save(d, recs, fname="anneal_results.json"):
        d.mkdir(parents=True, exist_ok=True)
        (d / fname).write_text(json.dumps({"results": recs}))
        return d / fname

    _vm = EN.verify_manifest
    EN.verify_manifest = lambda gd: []          # 생성기 검증은 생성기 selftest 몫 (판독기 selftest 와 같은 처리)
    try:
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            gen = td / "gen"
            (gen / "cif").mkdir(parents=True)
            NB, K = 8, 2
            rank_val = {"F_B": {b: b for b in range(NB)}, "F_P": {b: (b - 2) % NB for b in range(NB)},
                        "F_free": {b: (b - 4) % NB for b in range(NB)}}
            base_E = {"F_B": -0.5, "F_P": 0.0, "F_free": -0.2}
            bases = []
            for b in range(NB):
                mot = {}
                for F in FAM:
                    f = gen / "cif" / f"cfg{b:04d}_O-{code[F]}.xyz"
                    write(str(f), toy(F, shift=0.01 * b))
                    mot[code[F]] = {"file": str(f.relative_to(gen)), "sha256": RD._sha(f)}
                bases.append({"rank": b, "motifs": mot})
            (gen / "manifest.json").write_text(json.dumps({"bases": bases}))
            Sg = RD.manifest_plan(gen)["structures"]
            s6 = save(td / "s6", [put(td / "s6", n, s["family"], base_E[s["family"]] + 0.01 * rank_val[s["family"]][s["rank"]],
                                      "converged", idn(s["sha256"], "relax_only")) for n, s in sorted(Sg.items())])
            V = RD.screen_verdict(gen, s6, k_f=K)
            vp = RD._dump(V, td / "verdict.json")
            plan = V["plan_anneal"]
            chk(V["status"] == "complete" and V["M"] == 6 and len(plan) == 18,
                "[양성] 사슬 준비: 거름 완결 · 합집합 6 · 계획 18 (G1 = 6 중 5 — 한 가족 하나 실패까지 통과)")
            pv = V["pilot"]
            pr = save(td / "p", [put(td / "p", pv["name"], "F_B", -0.6, "converged",
                                     idn(pv["start"]["sha256"], "anneal_relax", 100, 500, purpose=C["purpose_pilot"],
                                         seed=RA.derive_seed(BASE, pv["name"])), traj=(101, 2.0, 500, 50000))])
            xps, X = RD.extract_pilot(vp, pr, td / "snap", k_f=K)

            def receipt(sub, Es):
                rr = [put(td / sub, Path(X["snapshots"][str(t)]["file"]).stem, "F_B", E, "converged",
                          idn(X["snapshots"][str(t)]["sha256"], "relax_only")) for t, E in zip((20, 50, 100), Es)]
                return RD._dump(RD.pilot_receipt(xps, save(td / sub, rr), k_f=K), td / f"{sub}_receipt.json")

            rp = receipt("r100", [0.0, -0.30, -0.02])
            rp20 = receipt("r20", [0.0, -0.02, -0.04])
            plan_by = {e["name"]: e for e in plan}
            nm = lambda F, b: f"cfg{b:04d}_O-{code[F]}"

            def s8(sub, st=None, eshift=None, traj=None, tamper=(), t=100.0):
                rr = []
                for e in plan:
                    n, F = e["name"], e["family"]
                    E = (eshift or base_E)[F] + 0.01 * e["rank"]
                    rr.append(put(td / sub, n, F, E, (st or {}).get(n, "converged"),
                                  idn(e["start"]["sha256"], "anneal_relax", t, 500, purpose=C["purpose_stage8"],
                                      seed=RA.derive_seed(BASE, n)),
                                  traj=(traj or {}).get(n, (int(t) + 1, 2.0, 500, int(t * 500))), mdlog_E=E))
                res = save(td / sub, rr)
                for n in tamper:
                    (td / sub / n / "md.traj").write_bytes((td / sub / n / "md.traj").read_bytes() + b"\0")
                return res

            def relax(sub, xx, dE=None, st=None, over=None, extra=False, drop=(), E_over=None, folder=None, fname="anneal_results.json"):
                rr = []
                d0 = folder or (td / sub)
                for n, fr in xx["frames"].items():
                    e = plan_by[n]
                    F = e["family"]
                    E100 = base_E[F] + 0.01 * e["rank"]
                    E = (E_over or {}).get(n, E100 + (dE or {}).get(F, 0.1))
                    s = Path(fr["file"]).stem
                    if s in drop:
                        continue
                    kw = {"stage": "relax_only", "purpose": PURPOSE_DIAG, **((over or {}).get(n, {}))}
                    sha = kw.pop("input_file_sha256", fr["sha256"])
                    rr.append(put(d0, s, F, E, (st or {}).get(n, "converged"), idn(sha, kw.pop("stage"), **kw)))
                if extra:
                    rr.append(put(d0, "stray_t050", "F_B", -9.0, "converged", idn("1" * 64, "relax_only", purpose=PURPOSE_DIAG)))
                return save(d0, rr, fname)

            # 정상 경로 ① — 같은 선택
            res = s8("s8")
            A100 = RD.anneal_readout(vp, rp, res, k_f=K)
            chk(A100["winner"] == "F_B", "[양성] 사슬: 8 단계 본 판독 (실제 판독기) → 승자 F_B")
            xp, x = extract(RD, vp, rp, res, td / "fr", k_f=K)
            chk(x["n_frames"] == 18 and all(f["frame"] == 50 for f in x["frames"].values())
                and all(abs(read(str(td / "fr" / f["file"])).positions[5, 0] - (10.0 + 0.05)) < 1e-6 for f in x["frames"].values()),
                "[양성] extract: 18 런 모두 프레임 50 (500 걸음 × 2 fs) — 파일 = 부모 궤적의 그 프레임")
            rr0 = relax("rx", x)
            out = judge(RD, xp, rr0, k_f=K)
            chk(out["verdict"]["code"] == "①" and out["verdict"]["final_winner"] == "F_B"
                and out["at_100ps_main_readout_preserved"]["winner"] == "F_B" and out["at_50ps"]["winner"] == "F_B",
                "[양성] judge (실제 판독기 · 검증된 100 ps 기록 ↔ 50 ps 기록) → ① 같은 선택 F_B")
            rec = out["records"]
            chk(abs(rec["delta_by_family"]["F_B"]["median"] + 0.1) < 1e-9 and rec["delta_by_family"]["F_B"]["max_abs"] > 0
                and rec["family_minimum"]["100"]["F_B"]["name"] == nm("F_B", 0) and rec["family_minimum"]["50"]["F_B"]["name"] == nm("F_B", 0)
                and abs(rec["family_minimum"]["100"]["F_B"]["dE_100_minus_50_of_this_run"] + 0.1) < 1e-9,
                "[양성] 기록: 가족별 Δ 중앙 · max|Δ| · 두 시점 최저 런 ID · 그 Δ")
            g = rec["family_minimum_gaps"]["m_F_free − m_F_B"]
            pc = rec["paired_change"]["δ_F_BF_P = Δ_F_B − Δ_F_P"]
            chk(abs(g["100"] - 0.3) < 1e-9 and abs(g["50"] - 0.3) < 1e-9 and abs(g["change_100_minus_50"]) < 1e-9
                and pc["n"] == 6 and abs(pc["median"]) < 1e-9 and rec["pairs_verdict"]["100"] is not None,
                "[양성] 기록: 최저 간 차 m_G − m_F (두 시점 · 변화) · 같은 바탕 짝 변화 δ_FG,i · 판독기 짝 판정")
            ml = out["md_log"]["per_run"][nm("F_B", 0)]
            chk(abs(ml["Epot_change_eV"] - 0.05) < 1e-9 and ml["40-50ps"]["n"] == 11 and ml["90-100ps"]["n"] == 11,
                "[양성] md.log 구간 [40,50] · [90,100] ps 평균 (기록만)")
            rdf = RD._dump(A100, td / "s8_readout.json")
            chk(judge(RD, xp, rr0, readout_json=rdf, k_f=K)["verdict"]["code"] == "①", "[양성] 본 판독 파일 = 다시 낸 본 판독 → 진행")
            Ab = copy.deepcopy(A100); Ab["winner"] = "F_P"
            rdb = RD._dump(Ab, td / "s8_readout_bad.json")
            chk(refuses("본 판독 파일", judge, RD, xp, rr0, readout_json=rdb, k_f=K), "⛔음성: 본 판독 파일이 다시 낸 것과 다르면 멈춘다")
            # ③ · ② · ⑤
            o3 = judge(RD, xp, relax("rx3", x, dE={"F_B": 0.25, "F_P": 0.1, "F_free": 0.1}), k_f=K)
            chk(o3["verdict"]["code"] == "③" and o3["at_50ps"]["winner"] is None, "⛔음성: 50 ps 여유 0.15 < 0.20 → ③ (실제 판독기)")
            o2 = judge(RD, xp, relax("rx2", x, dE={"F_B": 0.1, "F_P": 0.1, "F_free": -0.5}), k_f=K)
            chk(o2["verdict"]["code"] == "②" and o2["at_50ps"]["winner"] == "F_free", "⛔음성: 50 ps 승자 F_free ≠ 100 ps F_B → ②")
            res5 = s8("s8_5", eshift={"F_B": -0.3, "F_P": 0.0, "F_free": -0.2})
            xp5, x5 = extract(RD, vp, rp, res5, td / "fr5", k_f=K)
            o5 = judge(RD, xp5, relax("rx5", x5, dE={"F_B": -0.3, "F_P": 0.1, "F_free": 0.1}), k_f=K)
            chk(o5["verdict"]["code"] == "⑤" and o5["at_50ps"]["winner"] == "F_B" and o5["verdict"]["final_winner"] is None,
                "⛔음성: 100 ps 못 가름 → ⑤ (50 ps 가 F_B 승자여도 올리지 않는다)")
            # ④ 성공 집합 — 시점마다 다른 F_B 런이 실패 (EA false_same_winner) · 100 ps 끝 이완 실패 런도 프레임은 뗀다
            res4 = s8("s8_4", st={nm("F_B", 1): "unconverged"})
            xp4, x4 = extract(RD, vp, rp, res4, td / "fr4", k_f=K)
            chk(x4["parent_status"][nm("F_B", 1)] == "relax100_failed" and nm("F_B", 1) in x4["frames"],
                "[양성] 100 ps 끝 이완 실패 (궤적 검증됨) 런도 50 ps 프레임을 뗀다 (가능한 50 ps 결과를 버리지 않는다)")
            o4 = judge(RD, xp4, relax("rx4", x4, st={nm("F_B", 2): "unconverged"}), k_f=K)
            chk(o4["verdict"]["code"] == "④" and o4["at_100ps_main_readout_preserved"]["winner"] == "F_B"
                and o4["at_50ps"]["winner"] == "F_B" and not o4["success_sets"]["F_B"]["same"],
                "⛔음성: 두 시점 모두 F_B 승자 (5/6) 지만 실패한 런이 다르면 → ④ 판독 보류 (본 판정 보존)")
            row = next(r for r in o4["records"]["rows"] if r["name"] == nm("F_B", 1))
            chk(row["status_100"].startswith("실패") and row["status_50"] == "ok" and row["dE_100_minus_50"] is None,
                "[양성] 시점별 상태 기록 (100 ps 실패 · 50 ps 성공 · Δ 는 결측)")
            o4s = judge(RD, xp4, relax("rx4s", x4, st={nm("F_B", 1): "unconverged"}), k_f=K)
            chk(o4s["verdict"]["code"] == "①" and o4s["success_sets"]["F_B"]["same"],
                "[양성] 같은 런이 두 시점 모두 실패 → 성공 집합 같음 → 비교한다 (① · 실패 수만이 아니라 이름이 같아야)")
            o4n = judge(RD, xp, relax("rx4n", x, E_over={nm("F_P", 3): float("nan")}), k_f=K)
            chk(o4n["verdict"]["code"] == "④" and next(r for r in o4n["records"]["rows"] if r["name"] == nm("F_P", 3))["status_50"].startswith("실패"),
                "⛔음성: 비유한 E_50 → 그 런은 50 ps 실패로 센다 (터지지 않는다) → 집합 다름 → ④")
            o4u = judge(RD, xp, relax("rx4u", x, st={nm("F_P", 3): "unconverged"}), k_f=K)
            chk(o4u["verdict"]["code"] == "④", "⛔음성: 50 ps 에서만 미수렴 (한 시점만 실패) → 집합 다름 → ④")
            # 부모 상태 — 실패 · 검증 실패 · 궤적 없음 (프레임 없음) · 저장 간격 250
            res7 = s8("s8_7", st={nm("F_P", 5): "failed"}, tamper=(nm("F_free", 2),),
                      traj={nm("F_free", 3): (201, 2.0, 250, 50000)})
            xp7, x7 = extract(RD, vp, rp, res7, td / "fr7", k_f=K)
            chk(x7["parent_status"][nm("F_P", 5)] == "parent_failed" and x7["parent_status"][nm("F_free", 2)] == "parent_unverified"
                and nm("F_P", 5) not in x7["frames"] and nm("F_free", 2) not in x7["frames"],
                "[양성] 부모 런 실패 · 궤적 변조 (검증 실패) → 프레임 없음 · 사유를 가른다")
            chk(x7["frames"][nm("F_free", 3)]["frame"] == 100
                and abs(read(str(td / "fr7" / x7["frames"][nm("F_free", 3)]["file"])).positions[5, 0] - (10.0 + 0.1)) < 1e-6,
                "[양성] 저장 간격 250 걸음 런은 50 ps = 프레임 100 (기록의 간격으로)")
            o7 = judge(RD, xp7, relax("rx7", x7), k_f=K)
            chk(o7["verdict"]["code"] in ("①", "④") and any("50 ps 프레임 없음" in str(f["why"])
                                                              for f in o7["at_50ps"]["families"]["F_P"]["failed"]),
                "[양성] 프레임 없는 런은 50 ps 에서도 실패 · 사유 = 부모 상태")
            # 음성 — 결속
            res20 = s8("s8_20", t=20.0)
            chk(RD.anneal_readout(vp, rp20, res20, k_f=K)["t_a_ps"] == 20 and refuses("t_a", extract, RD, vp, rp20, res20, td / "fr_ta", k_f=K),
                "⛔음성: 영수증 t_a 20 (8 단계 20 ps · 판독기는 받는다) → 진단 안 함 (100 ps 에만 정의)")
            chk(refuses("비어 있지 않다", extract, RD, vp, rp, res, td / "fr", k_f=K), "⛔음성: 출력 폴더가 비어 있지 않으면 덮지 않는다")

            def tamper_frames(sub, fn):
                d = td / sub
                shutil.copytree(td / "fr", d)
                xx = json.loads((d / "diag_frames.json").read_text())
                fn(d, xx)
                (d / "diag_frames.json").write_text(json.dumps(xx, ensure_ascii=False))
                return d / "diag_frames.json", xx

            n0, n1 = nm("F_B", 0), nm("F_P", 0)

            def other_frame(d, xx):                 # 다른 런의 프레임으로 바꿔치기 (sha 는 맞춘다)
                f0 = d / xx["frames"][n0]["file"]
                shutil.copy(d / xx["frames"][n1]["file"], f0)
                xx["frames"][n0]["sha256"] = _sha_file(f0)
            xpo, xo = tamper_frames("fr_other", other_frame)
            chk(refuses("부모 궤적의 50 ps 프레임과 다르다", judge, RD, xpo, relax("rx_o", xo), k_f=K),
                "⛔음성: 다른 런의 프레임 (sha 를 맞춰도) → 부모 궤적에서 다시 읽어 거부")

            def frame49(d, xx):                     # 49 ps 프레임 (출처 번호 · 파일 · sha 를 다 맞춰도)
                mt = json.loads(res.read_text())["results"]
                rec0 = next(r for r in mt if r["name"] == n0)
                with Trajectory(str(td / "s8" / rec0["outputs"]["md_traj"]["rel"])) as T:
                    fr = T[49]
                    a = Atoms(fr.get_chemical_symbols(), positions=fr.get_positions(), cell=fr.cell.array, pbc=fr.pbc)
                f0 = d / xx["frames"][n0]["file"]
                write(str(f0), a)
                xx["frames"][n0].update(frame=49, sha256=_sha_file(f0))
            xp49, x49 = tamper_frames("fr_49", frame49)
            chk(refuses("50 ps 프레임 50", judge, RD, xp49, relax("rx_49", x49), k_f=K), "⛔음성: 49 ps 프레임 → 거부")

            def swap(d, xx):                        # 스냅숏 교체 (좌표를 조금 옮긴 파일 · sha 는 맞춘다)
                f0 = d / xx["frames"][n0]["file"]
                a = read(str(f0)); a.positions[3] += 0.01
                write(str(f0), a)
                xx["frames"][n0]["sha256"] = _sha_file(f0)
            xps_, xs_ = tamper_frames("fr_swap", swap)
            chk(refuses("부모 궤적의 50 ps 프레임과 다르다", judge, RD, xps_, relax("rx_s", xs_), k_f=K), "⛔음성: 스냅숏 교체 → 거부")
            xpst, _ = tamper_frames("fr_st", lambda d, xx: xx["parent_status"].update({n0: "parent_no_traj"}))
            chk(refuses("부모 상태", judge, RD, xpst, rr0, k_f=K), "⛔음성: 출처의 부모 상태를 바꾸면 거부")
            xpdr, xdr = tamper_frames("fr_drop", lambda d, xx: xx["frames"].pop(n1))
            chk(refuses("진단 프레임 이름 집합", judge, RD, xpdr, relax("rx_dr", xdr), k_f=K),
                "⛔음성: 출처에서 프레임 하나를 빼면 거부 (빼면 50 ps 실패로 조용히 세어 ④ 가 된다)")
            xpfb, _ = tamper_frames("fr_fb", lambda d, xx: xx["frames"][n0].update(family="F_P"))
            chk(refuses("초기 가족", judge, RD, xpfb, rr0, k_f=K), "⛔음성: 출처의 초기 가족 · 바탕을 바꾸면 거부 (이름으로 결속)")
            f0 = td / "fr" / x["frames"][n0]["file"]
            keep = f0.read_bytes(); f0.write_bytes(keep + b"\n")
            chk(refuses("프레임 파일", judge, RD, xp, rr0, k_f=K), "⛔음성: 진단 프레임 파일이 출처 기록 뒤 바뀌면 거부")
            f0.write_bytes(keep)
            chk(refuses("진단 프레임이 아닌", judge, RD, xp, relax("rx_x", x, extra=True), k_f=K), "⛔음성: 섞인 기록 → 거부")
            chk(refuses("진단 이완 결과 누락", judge, RD, xp, relax("rx_m", x, drop={f"{n1}_t050"}), k_f=K), "⛔음성: 진단 이완 누락 → 거부 (누락 ≠ 실패)")
            for label, ov, kw in (("목적 8 단계", {"purpose": C["purpose_stage8"]}, "실행 목적"), ("단계 어닐", {"stage": "anneal_relax"}, "단계"),
                                  ("time_ps 0.5", {"time_ps": 0.5}, "time_ps"), ("fmax 0.02", {"relax_fmax": 0.02}, "relax_fmax"),
                                  ("셀 고정", {"cell_relax": False}, "cell_relax"), ("시작 sha", {"input_file_sha256": "0" * 64}, "시작 파일")):
                chk(refuses(kw, judge, RD, xp, relax("rx_i" + str(abs(hash(label)) % 10**6), x, over={n0: ov}), k_f=K),
                    f"⛔음성: 진단 이완 기록의 {label} → 거부")
            k8 = res.read_bytes()
            chk(refuses("8 단계 폴더", judge, RD, xp, relax("rx_in8", x, folder=td / "s8", fname="diag_relax.json"), k_f=K)
                and res.read_bytes() == k8, "⛔음성: 진단 이완 결과가 8 단계 폴더 (다른 파일 이름이어도) → 거부")
            rk = res.read_bytes(); res.write_bytes(rk + b" ")
            chk(refuses("묶인 입력", judge, RD, xp, rr0, k_f=K), "⛔음성: 묶인 입력 (8 단계 결과) 이 바뀌면 거부")
            res.write_bytes(rk)
            chk(judge(RD, xp, rr0, k_f=K)["verdict"]["code"] == "①", "[양성] 되돌린 뒤 다시 판독 = 같다")
    finally:
        EN.verify_manifest = _vm
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
        cnt = {}
        for s in x["parent_status"].values():
            cnt[s] = cnt.get(s, 0) + 1
        print(f"-> {xp} · 프레임 {x['n_frames']} 개 (50 ps) · 부모 상태 {cnt}")
        print(f"   실행기: CAND={Path(A.out_dir).resolve()} · N_EXPECT={x['n_frames']} · TIME_PS=0 · 새 OUTNAME")
        return 0
    if Path(A.out).exists():
        raise SystemExit(f"⛔ {A.out} 가 이미 있다 — 덮지 않는다")
    out = judge(RD, A.frames, A.relax, A.readout)
    p = RD._dump(out, A.out)
    print(f"-> {p}")
    print(f"100 ps (본 판독 · 보존): {out['at_100ps_main_readout_preserved']['decision']}")
    print(f" 50 ps: {out['at_50ps']['decision']}")
    print(f"사유 {out['verdict']['code']}: {out['verdict']['reason']}")
    print(f"최종: {out['verdict']['final_decision']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
