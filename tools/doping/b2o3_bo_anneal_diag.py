#!/usr/bin/env python3
"""b2o3 B·O 배치 카드 — 어닐 시간 진단 (개정 3 → 개정 4 · 회신 EA · 리뷰 EC · 8 단계 · 50 ps 결과를 열기 전에 고정 · 2026-11-10).

카드 db/properties/b2o3_bo_placement_estimand_2026_11_09.json '개정_4_EA_회신_2026_11_10'
(결정 D-2026-11-10-b2o3-bo-placement-amend4-ea · 개정 3 의 잠정 규칙 · 기록 · 문장을 대체).
v3 = 내부 반박 리뷰 EC (kb/reviews/internal_EC_reply_b2o3_amend4_diag_v2_2026_11_10.md) 고침 — 결과 0 건 열람 상태에서.

  extract — 8 단계 결과를 판 고정 판독기의 anneal_readout 으로 결속 (목적 · 입력 · 설정 · 정체성 · 궤적 sha) 한 뒤
            계획 항목마다 부모 상태를 **궤적 검사로** 가른다 (EC P1-2 · 판 고정 run_anneal._verify_md_traj):
              no_start (6 단계 실패) · parent_failed (상태 failed — 기록에 궤적 결속 없음) · parent_no_traj (md_traj 없음) ·
              parent_unverified (궤적 검사 실패 — 파일 · sha256 · 프레임 수 · dt · 걸음 · 프레임마다 원자 수 · 조성 · 기하) ·
              relax100_failed (궤적은 통과 · 100 ps 끝 이완 미수렴 · 끝 구조 파일 (post_md · post_relax) 검사 실패 · 에너지 비유한) · ok100
            ok100 · relax100_failed 런의 md.traj 에서 50 ps 프레임 (기록의 dt_fs × log_every_steps 로 번호) 을 떼어 xyz 로 쓴다
            + 출처 JSON (diag_frames.json — 진단 도구 · 판독기 sha256 · EC P1-1) + 실행기 계획 manifest (목적 b2o3_bo/anneal_diag_t050 · 이완만)
            + 구간 평균에 쓸 궤적 프레임에 에너지 · 운동량이 실렸는지 GPU 를 쓰기 전에 본다 (없으면 멈춘다 · EC P2-2).
  judge   — 진단 도구 · 판독기 sha256 이 extract 때와 같아야 진행 (EC P1-1) · 본 판독 파일 (--readout · 필수) 과 다시 낸 본 판독을 대조 ·
            출처를 다시 결속 (부모 상태 · 프레임 파일 sha · **부모 궤적에서 그 프레임을 다시 읽어 원소 · 좌표 · 셀 · PBC · 제약 없음 ·
            추가 배열 없음 · 같은 방식으로 다시 쓴 바이트 sha** 대조 · EC P2-5) · 진단 이완 결과 (새 폴더 · 이완만 · 진단 목적 · 같은 설정)
            를 이름으로 결속 — failed (예외) 와 '수렴 표시인데 결과 검사 · 에너지가 안 맞는 기록' 은 누락처럼 거부 (다시 돌린 뒤 판독 ·
            EC P2-3) · 미수렴 (unconverged) 만 50 ps 실패 → 판독기 anneal_judge 로 50 ps 가족 판독 → 본 판독 (100 ps · 보존) 과 견준 사유:
              ⑤ 본 판독 승자 없음 → 그대로 (진단은 올리지 않는다)
              ④ 판독 보류 — 가족별 성공 런 집합이 두 시점에서 다름 · 또는 50 ps 판독 보류 (게이트)
              ③ 50 ps 여유 부족 (게이트 통과 · 승자–차점 < 0.20) — 50 ps 순서 · 최저 가족을 같이 적는다 (EC P2-4)
              ② 다른 승자
              ① 같은 선택 — 두 시점 모두 같은 초기 가족이 여유 ≥ 0.20 으로 선택 (같은 성공 집합)
            + 판정 옆 (게이트 아님 · 회신 EA Q2): 두 시점의 짝 판정 · 가족별 E 중앙
            + 기록: 런별 E · Δ = E_100 − E_50 · 시점별 상태 (결측은 결측) · 가족별 Δ 중앙 · IQR · 최솟값 · 최댓값 · max|Δ| ·
              두 시점 최저 런 ID · 끝 꼴 · 그 Δ · 최저 간 차 m_G(t) − m_F(t) 와 변화 · 같은 바탕 짝 변화 δ_FG,i · 가족별 E 중앙 ·
              판독기 짝 판정 · 구간 평균 ([40,50] · [90,100] ps) = sha 로 묶인 8 단계 md.traj 프레임의 Epot · 온도 (운동량) —
              md.log 는 대조로만 (한 시도보다 줄이 많으면 표지 · EC P2-2).

판독기는 고치지 않는다 — --readout_tool (기본 = 이 파일 옆 · gabia 는 판 고정 $R/src · sha256 872d91f7… = 12b8bdef) 의 함수를 부른다.
명령줄 (extract · judge) 은 판독기 sha256 이 판 고정 값이 아니면 멈춘다.

쓰는 법
  python3 b2o3_bo_anneal_diag.py --selftest
  python3 b2o3_bo_anneal_diag.py extract --readout_tool <판독기> --verdict s6_verdict.json --receipt s7_receipt.json \
          --results s8_anneal/anneal_results.json --out_dir s8b_frames
  (실행기: CAND=s8b_frames · N_EXPECT=<프레임 수> · TIME_PS=0 · 새 OUTNAME · run_rc 0 · check_rc 0 일 때만 judge)
  python3 b2o3_bo_anneal_diag.py judge --readout_tool <판독기> --frames s8b_frames/diag_frames.json \
          --relax s8b_relax/anneal_results.json --readout s8_readout.json --out s8b_diag.json

⛔ 이 도구가 못 하는 것
  · 이완을 돌리지 않는다 (실행기 run_uma_kgy.sh) · 판정 규칙 (G1–G3 · 여유 0.20 · 짝) 을 새로 만들지 않는다 (anneal_judge 그대로).
  · 두 시점 일치는 같은 궤적의 앞뒤라 시간 수렴 · 독립 재현 · 전역 최저의 증거가 아니다 · 전체 가족 순서 · 같은 최저 런 ·
    같은 구조 골짜기를 뜻하지 않는다.
  · 공통 성공 집합으로 다시 판독하지 않는다 (분모를 바꾸지 않는다 · 집합이 다르면 ④) — 100 ps 끝 이완 실패 런 하나로도
    (50 ps 이완이 성공하면) ④ 가 된다 (시간 효과가 아니다).
  · 바이트 대조는 extract 와 judge 가 같은 ASE 판이어야 맞는다 — 판이 바뀌면 같은 기하여도 멈춘다 (큰 소리 · 틀린 통과는 없다).
  · 한 런의 저장 간격이 50 ps 의 약수가 아니면 extract 전체가 멈춘다 (실제 8 단계는 다 500 걸음 · EC P2-5 마 · 메모).
  · 궤적 프레임에 에너지 · 운동량이 없으면 구간 평균을 못 내고 멈춘다 (md.log 로 대신하지 않는다 — md.log 는 ASE 가 덧붙여 써서
    다시 돈 런은 시도가 섞이고 기록에 sha 가 없다).
  · 구간 평균은 기록만 (판정에 안 쓴다 · 열적 배치 에너지 ≠ 이완 끝점 에너지).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import tempfile
from pathlib import Path

import numpy as np

SELF = Path(__file__).resolve()
HERE = SELF.parent
DEFAULT_RD = HERE / "b2o3_bo_readout.py"
PINNED_RD_SHA256 = "872d91f7508ad21c3d67f373bee228bd894994b731a77f69525818db3a8967cf"   # 판 고정 판독기 (커밋 12b8bdef)
T_DIAG_PS = 50.0
T_A_REQUIRED = 100
PURPOSE_DIAG = "b2o3_bo/anneal_diag_t050"
CARD_REF = "db/properties/b2o3_bo_placement_estimand_2026_11_09.json#개정_4_EA_회신_2026_11_10"
REVIEW_REF = "kb/reviews/internal_EC_reply_b2o3_amend4_diag_v2_2026_11_10.md"
KIND_FRAMES = "b2o3_bo_anneal_diag_frames/v3"
KIND_OUT = "b2o3_bo_anneal_diag/v3"
# aux-window-ok: MSD 창이 아니다 — 8 단계 md.traj Epot · 온도 구간 평균 (ps · 기록만 · 카드 개정 4 md_log_진단_Q3 가 결과 전에 고정)
MDLOG_WINDOWS_PS = ((40.0, 50.0), (90.0, 100.0))
NEED = ("anneal_readout", "verify_screen_verdict", "load_records", "identity_problems", "anneal_judge", "end_motif",
        "_frame_index", "_same_geometry", "_sha", "_input", "_core", "_dump", "CONTRACT", "FAM_ORDER", "_RA")
FRAMED = ("ok100", "relax100_failed")
PARENT_WHY = {"no_start": "시작 구조 없음 (6 단계 실패)",
              "parent_failed": "부모 런 실패 (상태 failed — 기록에 궤적 결속 없음)",
              "parent_unverified": "부모 궤적 검사 실패 (run_anneal 궤적 검사) — 50 ps 프레임을 믿지 않는다",
              "parent_no_traj": "부모 기록에 md_traj 없음 — 50 ps 프레임 없음"}
LIMIT_D = "① 은 같은 초기 가족의 선택까지다 — 전체 가족 순서 · 같은 최저 런 · 같은 구조 골짜기의 유지를 뜻하지 않는다."   # 카드 문장 D 그대로
SENT = {
 "①": ("선언한 초기점 생성·탐색 절차에서, 초기 가족 {F}의 최저 이완 에너지가 500 K·100 ps 어닐 뒤 가장 낮았다. 동일한 유효 런 집합의 "
       "50 ps 판독에서도 같은 가족이 선택됐으며, 두 시점 모두 차점과의 차가 0.20 eV/B₂O₃ 이상이었다. 이는 두 시점의 선택 일치이며, "
       "어닐 시간 수렴·독립 재현·전역 최저 상태를 뜻하지 않는다. " + LIMIT_D),
 "②": "50 ps와 100 ps에서 선택된 초기 가족이 달라, 이번 탐색에서는 시간에 일관된 승자를 보고하지 않는다.",
 "③": "100 ps에서는 승자 문턱을 만족했으나, 50 ps에서는 여유가 부족해 두 시점 일치 조건을 충족하지 못했다.",
 "④": "시간 비교의 유효성 조건이 충족되지 않아 최종 승자 서술을 보류한다.",
}
DISCLAIMER = ("초기 가족 라벨 (F_B · F_P · F_free) 은 출발 꼴이다 — 최저 구조의 끝 꼴을 같이 본다 · 어닐 길이는 운영 규칙 · "
              "두 시점 일치는 시간 수렴 · 독립 재현 · 전역 최저의 증거가 아니다 · ① 은 같은 초기 가족의 선택까지다 — "
              "전체 가족 순서 · 같은 최저 런 · 같은 구조 골짜기의 유지를 뜻하지 않는다 (카드 개정 4 · 리뷰 EC)")


def _sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _tool_fp() -> dict:
    """이 진단 도구 자신의 지문 (EC P1-1) — extract 가 출처에 쓰고 judge 가 대조한다."""
    return {"path": str(SELF), "sha256": _sha_file(SELF)}


def load_rd(path=None):
    """판독기 파일을 불러온다 (그 파일 옆의 run_anneal · b2o3_enumerate 를 판독기가 스스로 불러온다)."""
    p = Path(path or DEFAULT_RD).resolve()
    if not p.is_file():
        raise SystemExit(f"⛔ 판독기 파일이 없다 ({p})")
    spec = importlib.util.spec_from_file_location("b2o3_bo_readout_for_diag", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    miss = [k for k in NEED if not hasattr(mod, k)] + ([] if hasattr(getattr(mod, "_RA", None), "_verify_md_traj")
                                                        else ["_RA._verify_md_traj"])
    if miss:
        raise SystemExit(f"⛔ 판독기 {p.name} 에 {miss} 가 없다 — 이 진단이 기대하는 판이 아니다")
    mod.__diag_path__, mod.__diag_sha256__ = str(p), _sha_file(p)
    return mod


def _raw_records(R) -> dict:
    """판독기가 결속한 결과 파일의 원 기록 (이름 → dict) — 같은 바이트인지 sha 로 다시 본다 (궤적 검사에 composition 이 필요하다)."""
    b = Path(R["path"]).read_bytes()
    if hashlib.sha256(b).hexdigest() != R["sha256"]:
        raise SystemExit("⛔ 8 단계 결과 파일이 판독기 결속 뒤 바뀌었다 (sha256) — 판독하지 않는다")
    return {r.get("name"): r for r in json.loads(b).get("results", [])}


def _stage8(RD, verdict, receipt, results, k_f=None):
    """판 고정 판독기와 같은 결속으로 8 단계 본 판독을 다시 낸다 → (본 판독, 계획, 8 단계 기록, 원 기록)."""
    A100 = RD.anneal_readout(verdict, receipt, results, k_f=k_f)   # 결속 실패면 판독기가 SystemExit
    if A100.get("t_a_ps") != T_A_REQUIRED:
        raise SystemExit(f"⛔ 파일럿 영수증의 t_a {A100.get('t_a_ps')} ≠ {T_A_REQUIRED} ps — 진단 (50 ps 프레임) 은 "
                         f"t_a 100 ps 에 대해서만 정의됐다 (카드 개정 3 · 4)")
    plan = RD.verify_screen_verdict(verdict, k_f)["plan_anneal"]
    names = [e["name"] for e in plan]
    if len(set(names)) != len(names):
        raise SystemExit("⛔ 계획에 같은 이름이 둘 — 이름으로 결속할 수 없다")
    R = RD.load_records(results)
    return A100, plan, R, _raw_records(R)


def parent_status(RD, e, r, raw, base):
    """계획 항목 하나의 부모 상태 → (상태, 사유) — **궤적 검사로** 가른다 (EC P1-2).

    궤적이 판 고정 run_anneal._verify_md_traj 를 통과하면 끝 구조 · 에너지 문제가 있어도 relax100_failed (50 ps 프레임을 뗀다) ·
    궤적 자체가 검사에 걸릴 때만 parent_unverified (옛 판은 결과 검사 목록 전체로 갈라 NaN 끝 구조 런의 프레임을 버렸다).
    """
    if not e["start"]:
        return "no_start", []
    if r is None:
        raise SystemExit(f"⛔ {e['name']}: 시작 파일이 있는 계획 항목의 8 단계 기록이 없다")
    if r.get("status") not in ("converged", "unconverged"):
        return "parent_failed", [f"상태 {r.get('status')}"]
    mt = (r.get("outputs") or {}).get("md_traj")
    if not mt:
        return "parent_no_traj", [str(q) for q in (r.get("vo") or [])[:2]]
    if raw is None:                                 # 같은 바이트 (sha 대조) 에서 읽었으니 없을 수 없다 — 방어
        raise SystemExit(f"⛔ {e['name']}: 원 기록이 없다")
    n_id = (raw.get("identity") or {}).get("n_atoms")
    tp = RD._RA._verify_md_traj(raw, mt, base, n_id)
    if tp:
        return "parent_unverified", [str(q) for q in tp]
    return ("ok100", []) if r["ok"] else ("relax100_failed", [str(q) for q in (r.get("why") or [])])


def statuses(RD, plan, recs, raw, base):
    status, detail = {}, {}
    for e in plan:
        status[e["name"]], detail[e["name"]] = parent_status(RD, e, recs.get(e["name"]), raw.get(e["name"]), base)
    return status, detail


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


# ───────────────────────── 구간 평균 (EC P2-2) — sha 로 묶인 궤적에서 · md.log 는 대조로만 ─────────────────────────
def _frame_E_T(fr, n, k):
    try:
        E = float(fr.get_potential_energy())
    except Exception as ex:                       # 계산기 없음 · 에너지 없음
        raise SystemExit(f"⛔ {n}: 8 단계 md.traj 프레임 {k} 에 퍼텐셜 에너지가 없다 ({type(ex).__name__}) — 구간 평균은 sha 로 묶인 "
                         f"궤적에서만 낸다 (md.log 로 대신하지 않는다 · EC P2-2) · gabia 궤적에 에너지가 실렸는지 먼저 본다")
    if not fr.has("momenta"):
        raise SystemExit(f"⛔ {n}: 8 단계 md.traj 프레임 {k} 에 운동량이 없다 — 온도를 궤적에서 낼 수 없다 (EC P2-2)")
    T = float(fr.get_temperature())
    if not (math.isfinite(E) and math.isfinite(T)):
        raise SystemExit(f"⛔ {n}: 8 단계 md.traj 프레임 {k} 의 에너지 · 온도가 유한하지 않다 ({E}, {T})")
    return E, T


def _mdlog_crosscheck(p, n_frames, step_ps, series):
    """md.log 대조 (기록만) — 머리줄 · 줄 수 (한 시도 = 궤적 프레임 수) · 마지막 시도의 Epot · T 와 궤적 값의 차."""
    try:
        lines = Path(p).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return {"status": "md.log 없음 · 못 읽음"}
    heads = [i for i, ln in enumerate(lines) if ln.split()[:1] == ["Time[ps]"]]
    if not heads:
        return {"status": "md.log 머리줄 없음"}
    blocks = []
    for j, h in enumerate(heads):
        hdr = lines[h].split()
        try:
            it, ie, iT = hdr.index("Time[ps]"), hdr.index("Epot[eV]"), hdr.index("T[K]")
        except ValueError:
            return {"status": "md.log 머리줄에 Time[ps] · Epot[eV] · T[K] 가 없다", "headers": len(heads)}
        rows = []
        for ln in lines[h + 1:(heads[j + 1] if j + 1 < len(heads) else len(lines))]:
            q = ln.split()
            try:
                rows.append((float(q[it]), float(q[ie]), float(q[iT])))
            except (IndexError, ValueError):
                continue
        blocks.append(rows)
    n_rows = sum(len(b) for b in blocks)
    last = blocks[-1]
    res = {"headers": len(heads), "rows": n_rows, "rows_one_attempt": int(n_frames), "rows_last_attempt": len(last),
           "multi_attempt": len(heads) > 1 or n_rows > int(n_frames)}
    if res["multi_attempt"]:
        res["⚠"] = (f"md.log 에 한 시도보다 많은 줄 (머리줄 {len(heads)} · 줄 {n_rows} · 한 시도 {int(n_frames)}) — ASE MDLogger 는 "
                    f"덧붙여 쓴다 · 구간 평균은 궤적에서만 낸다")
    if len(last) == int(n_frames):
        dE, dT, bad_t = [], [], 0
        for ser in series.values():
            for k, (E, T) in ser.items():
                t, El, Tl = last[k]
                bad_t += abs(t - k * step_ps) > 1e-6
                dE.append(abs(El - E))
                dT.append(abs(Tl - T))
        res.update(last_attempt_max_abs_dEpot_vs_traj_eV=max(dE) if dE else None,
                   last_attempt_max_abs_dT_vs_traj_K=max(dT) if dT else None, last_attempt_time_mismatch=int(bad_t))
    else:
        res["last_attempt_vs_traj"] = "마지막 시도의 줄 수가 궤적 프레임 수와 달라 대조하지 않는다"
    return res


def traj_windows(plan, status, recs, base, windows=MDLOG_WINDOWS_PS, crosscheck=True):
    """8 단계 md.traj (sha 로 묶임) 프레임의 Epot · 온도 구간 평균 — 기록만 (게이트 아님 · EC P2-2).

    궤적 검사를 통과한 런 (ok100 · relax100_failed) 만 · 프레임에 에너지 · 운동량이 없으면 멈춘다 (지어내지 않는다).
    """
    from ase.io.trajectory import Trajectory
    out = {}
    for e in plan:
        n = e["name"]
        st = status[n]
        if st not in FRAMED:
            out[n] = {"status": PARENT_WHY[st] + " — 궤적 구간 평균 없음"}
            continue
        mt = recs[n]["outputs"]["md_traj"]
        tp = Path(base) / mt["rel"]
        if not tp.is_file() or _sha_file(tp) != mt["sha256"]:
            raise SystemExit(f"⛔ 궤적 {mt['rel']} 이 없거나 8 단계 기록 뒤 바뀌었다 (sha256)")
        step = float(mt["dt_fs"]) * int(mt["log_every_steps"]) / 1000.0
        rec, series = {}, {}
        with Trajectory(str(tp)) as T:
            nf = len(T)
            if nf != int(mt["n_frames"]):
                raise SystemExit(f"⛔ 궤적 {mt['rel']} 프레임 {nf} ≠ 기록 {mt['n_frames']}")
            for lo, hi in windows:
                key = f"{lo:g}-{hi:g}ps"
                ks = [k for k in range(nf) if lo - 1e-9 <= k * step <= hi + 1e-9]
                vals = [_frame_E_T(T[k], n, k) for k in ks]
                series[key] = dict(zip(ks, vals))
                rec[key] = ({"n": len(vals), "frames": [ks[0], ks[-1]], "Epot_mean_eV": float(np.mean([v[0] for v in vals])),
                             "T_mean_K": float(np.mean([v[1] for v in vals]))} if vals else {"n": 0})
        k1, k2 = (f"{lo:g}-{hi:g}ps" for lo, hi in windows)
        if rec[k1].get("n") and rec[k2].get("n"):
            rec["Epot_change_eV"] = rec[k2]["Epot_mean_eV"] - rec[k1]["Epot_mean_eV"]
            rec["T_change_K"] = rec[k2]["T_mean_K"] - rec[k1]["T_mean_K"]
        if crosscheck:
            rec["md_log_crosscheck"] = _mdlog_crosscheck(Path(base) / n / "md.log", nf, step, series)
        out[n] = rec
    return {"windows_ps": [list(w) for w in windows],
            "source": "8 단계 md.traj 프레임 (sha256 결속 · 저장 간격마다) — Epot = 프레임 에너지 · T = 프레임 운동량",
            "per_run": out,
            "⚠": "기록만 — 열적 배치 에너지 (MD 중) 는 이완 끝점 에너지와 다른 양 · D1 을 대신하지 않는다 · md.log 는 대조로만 "
                 "(ASE 가 덧붙여 써서 다시 돈 런은 시도가 섞인다 · 기록에 sha 가 없다)"}


def extract(RD, verdict, receipt, results, out_dir, t_diag=T_DIAG_PS, k_f=None):
    from ase.io import read, write
    A100, plan, R, raw = _stage8(RD, verdict, receipt, results, k_f)
    recs = R["records"]
    out_dir = Path(out_dir)
    if out_dir.exists() and any(out_dir.iterdir()):
        raise SystemExit(f"⛔ 출력 폴더 {out_dir} 가 비어 있지 않다 — 덮지 않는다 (새 폴더를 준다)")
    base = Path(R["path"]).parent
    status, detail = statuses(RD, plan, recs, raw, base)
    traj_windows(plan, status, recs, base, crosscheck=False)        # 에너지 · 운동량이 없으면 GPU 를 쓰기 전에 멈춘다 (EC P2-2)
    out_dir.mkdir(parents=True, exist_ok=True)
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
    x = {"kind": KIND_FRAMES, "card": CARD_REF, "review": REVIEW_REF, "t_diag_ps": float(t_diag), "t_a_ps": A100["t_a_ps"],
         "purpose": PURPOSE_DIAG, "diag_tool": _tool_fp(),
         "readout_tool": {"path": RD.__diag_path__, "sha256": RD.__diag_sha256__},
         "inputs": {"screen_verdict": {"path": str(Path(verdict).resolve()), "sha256": _sha_file(verdict)},
                    "pilot_receipt": {"path": str(Path(receipt).resolve()), "sha256": _sha_file(receipt)},
                    "anneal_results": {"path": R["path"], "sha256": R["sha256"]}},
         "plan_n": len(plan), "n_frames": len(frames), "parent_status": status, "parent_detail": detail, "frames": frames}
    xp = RD._dump(x, out_dir / "diag_frames.json")
    (out_dir / "manifest.json").write_text(json.dumps(
        {"schema": "b2o3_bo_plan/v1", "stage": "8b_anneal_time_diag_relax", "purpose": PURPOSE_DIAG, "n": len(frames),
         "실행기": f"TIME_PS 0 (이완만) · N_EXPECT {len(frames)} · 새 출력 폴더 (8 단계 폴더와 섞지 않는다) · run_rc 0 · check_rc 0 일 때만 judge",
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
        o = list(A50.get("order") or [])
        lo = o[0] if o else None
        gap = A50.get("winner_runner_up_gap_eV")
        tail = (f"50 ps 순서 {o} · 최저 {lo}" + ("" if lo == w100 else f" (100 ps 승자 {w100} 와 다른 가족)")
                + (f" · 차 {gap:.3f}" if isinstance(gap, (int, float)) else ""))
        return {"code": "③", "reason": f"50 ps 여유 부족 ({A50.get('decision')}) · {tail}", "final_winner": None,
                "final_decision": f"두 시점 일치 미충족 — 50 ps 여유 부족 ({tail}) (100 ps 본 판정은 보존)",
                "sentence": SENT["③"], "at_50ps_order": o, "at_50ps_lowest": lo, "lowest_50_is_winner_100": lo == w100,
                "note": "50 ps 최저가 100 ps 승자와 다른 가족이어도 ③ 이다 — '여유 부족' 을 '같은 쪽 · 작은 차' 로 읽지 않는다"}
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


def _tail(d):
    return (" — " + "; ".join(str(x) for x in d[:2])) if d else ""


def build_records(RD, plan, recs100, recs50, status, detail, A100, A50):
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
                     "status_100": "ok" if E100 is not None else ((PARENT_WHY[st] + _tail(detail.get(n))) if st in PARENT_WHY
                                                                  else f"실패 — {_why(a)}"),
                     "status_50": "ok" if E50 is not None else ((PARENT_WHY[st] + " — 50 ps 프레임 없음") if st in PARENT_WHY
                                                                else f"실패 — {_why(c)}"),
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


def summary(A):
    fam = {F: {"M": d.get("M"), "n_success": d.get("n_success"), "need_G1": d.get("need_G1"), "G1": d.get("G1"),
               "G3": d.get("G3"), "G3_mixed": d.get("G3_mixed"), "min": d.get("min"),
               "failed": [{"name": f.get("name"), "why": f.get("why")} for f in (d.get("failed") or [])]}
           for F, d in (A.get("families") or {}).items()}
    return {"decision": A.get("decision"), "winner": A.get("winner"), "order": A.get("order"),
            "winner_runner_up_gap_eV": A.get("winner_runner_up_gap_eV"), "hold_reasons": A.get("hold_reasons"),
            "pairs": A.get("pairs"), "G2_same_composition": A.get("G2_same_composition"), "families": fam}


def judge(RD, frames_json, relax_results, readout_json, margin=None, k_f=None):
    from ase.io import read, write
    xp = Path(frames_json)
    x = json.loads(xp.read_text(encoding="utf-8"))
    if x.get("kind") != KIND_FRAMES:
        raise SystemExit(f"⛔ {xp.name} 는 진단 프레임 출처 ({KIND_FRAMES}) 가 아니다")
    if x.get("purpose") != PURPOSE_DIAG or float(x.get("t_diag_ps", -1)) != T_DIAG_PS:
        raise SystemExit(f"⛔ 진단 프레임 출처의 목적 · 시각 ({x.get('purpose')} · {x.get('t_diag_ps')}) 이 이 도구와 다르다")
    me = _tool_fp()
    xd, xr = x.get("diag_tool") or {}, x.get("readout_tool") or {}
    if xd.get("sha256") != me["sha256"]:
        raise SystemExit(f"⛔ 진단 도구 sha256 {me['sha256'][:12]}… 이 extract 때 ({str(xd.get('sha256'))[:12]}…) 와 다르다 — "
                         f"extract 와 같은 판으로만 판독한다 (EC P1-1)")
    if xr.get("sha256") != RD.__diag_sha256__:
        raise SystemExit(f"⛔ 판독기 sha256 {RD.__diag_sha256__[:12]}… 이 extract 때 ({str(xr.get('sha256'))[:12]}…) 와 다르다 — "
                         f"extract 와 같은 판독기로만 판독한다 (EC P1-1)")
    if readout_json is None:
        raise SystemExit("⛔ 본 판독 파일 (--readout) 이 없다 — ① 에서 연 본 판독과 묶어야 판독한다 (EC P2-5)")
    base = xp.resolve().parent
    vp, rp, ap_ = (RD._input(x, k, base) for k in ("screen_verdict", "pilot_receipt", "anneal_results"))
    A100, plan, R100, raw100 = _stage8(RD, vp, rp, ap_, k_f)
    got = json.loads(Path(readout_json).read_text(encoding="utf-8"))
    if RD._core(got) != RD._core(A100):
        raise SystemExit("⛔ 본 판독 파일이 같은 입력에서 다시 낸 본 판독과 다르다 — 바뀐 판독은 쓰지 않는다")
    recs100 = R100["records"]
    base100 = Path(R100["path"]).parent
    status, detail = statuses(RD, plan, recs100, raw100, base100)
    if status != x.get("parent_status"):
        raise SystemExit("⛔ 출처의 부모 상태가 8 단계 기록에서 다시 낸 것과 다르다 — 출처가 바뀌었거나 다른 결과에서 나왔다")
    frames = x.get("frames") or {}
    if set(frames) != {n for n, s in status.items() if s in FRAMED}:
        raise SystemExit("⛔ 진단 프레임 이름 집합 ≠ 궤적이 검증된 8 단계 런 집합")
    fam_of = {e["name"]: (e["rank"], e["family"]) for e in plan}
    with tempfile.TemporaryDirectory() as tmpd:
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
            got_a = read(str(f))
            if not RD._same_geometry(a, got_a):
                raise SystemExit(f"⛔ {n}: 진단 입력이 부모 궤적의 50 ps 프레임과 다르다 (원소 순서 · 좌표 · 셀 · PBC)")
            if got_a.constraints:
                raise SystemExit(f"⛔ {n}: 진단 입력에 제약 {got_a.constraints} 이 있다 — 부모 프레임에 없는 것 (EC P2-5)")
            if set(got_a.arrays) != {"numbers", "positions"}:
                raise SystemExit(f"⛔ {n}: 진단 입력에 추가 배열 {sorted(set(got_a.arrays) - {'numbers', 'positions'})} 이 있다 — "
                                 f"부모 프레임에 없는 것 (EC P2-5)")
            p = Path(tmpd) / Path(fr["file"]).name
            write(str(p), a)
            if _sha_file(p) != fr["sha256"]:
                raise SystemExit(f"⛔ {n}: 부모 프레임을 같은 방식으로 다시 쓴 바이트가 진단 입력과 다르다 (sha256 · EC P2-5) — "
                                 f"손댄 입력이거나 extract 와 ASE 판이 다르다")
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
    notdone = [s for s in sorted(want) if not raw[s]["ok"] and raw[s]["status"] != "unconverged"]
    if notdone:
        s0 = notdone[0]
        raise SystemExit(f"⛔ 진단 이완 기록 {len(notdone)} 건이 끝나지 않았다 (예 {s0}: 상태 {raw[s0]['status']} · {raw[s0]['why'][:1]}) — "
                         f"failed (예외) 는 끝난 것이 아니다 · 같은 폴더 · 같은 설정으로 다시 돌린 뒤 (check_rc 0) 판독한다 (누락과 같이 · "
                         f"EC P2-3) · 수렴 표시인데 결과 검사 · 에너지가 안 맞는 기록도 판독하지 않는다 · 미수렴만 50 ps 실패로 센다")
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
    records = build_records(RD, plan, recs100, recs50, status, detail, A100, A50)
    v["beside_minimum_not_gates"] = {"pairs": {"50": A50.get("pairs"), "100": A100.get("pairs")},
                                     "family_median_E": records["family_median_E"],
                                     "⚠": "게이트 아님 — 최저 판정 옆에 둔다 (회신 EA Q2 · EC P2-4)"}
    out = {"kind": KIND_OUT, "card": CARD_REF, "review": REVIEW_REF,
           "inputs": {"diag_frames": {"path": str(xp.resolve()), "sha256": _sha_file(xp)},
                      "diag_relax_results": {"path": RR["path"], "sha256": RR["sha256"]},
                      "stage8_readout": {"path": str(Path(readout_json).resolve()), "sha256": _sha_file(readout_json)}},
           "diag_tool": me, "readout_tool": {"path": RD.__diag_path__, "sha256": RD.__diag_sha256__},
           "extract_tools": {"diag_tool": xd, "readout_tool": xr},
           "t_diag_ps": T_DIAG_PS, "t_a_ps": A100["t_a_ps"],
           "at_100ps_main_readout_preserved": summary(A100), "at_50ps": summary(A50),
           "success_sets": {F: {"100": S["100"][F], "50": S["50"][F], "same": S["100"][F] == S["50"][F]} for F in FAM},
           "verdict": v, "records": records, "md_window": traj_windows(plan, status, recs100, base100),
           "parent_status": status, "parent_detail": detail, "⚠": DISCLAIMER}
    return out


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    import copy
    import shutil
    import tempfile as _tf
    from ase import Atoms, units
    from ase.calculators.singlepoint import SinglePointCalculator
    from ase.constraints import FixAtoms
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
            if kw in str(e):
                return True
            print(f"     (다른 거부: {str(e)[:160]})")
            return False
        except Exception as e:                      # 거부가 아니라 터짐
            print(f"     (터짐 {type(e).__name__}: {e})")
            return False
        return False

    near = lambda a, b, tol=1e-9: (a is not None and b is not None and abs(float(a) - float(b)) <= tol)

    RD = load_rd()
    chk(all(hasattr(RD, k) for k in NEED) and RD.__diag_sha256__ == _sha_file(DEFAULT_RD),
        "[양성] 이 저장소의 판독기를 불러온다 (필요한 함수 전부 · run_anneal._verify_md_traj · sha256 기록)")
    chk(refuses("판독기 파일이 없다", load_rd, "/nonexistent/b2o3_bo_readout.py"), "⛔음성: 판독기 파일이 없으면 멈춘다")

    # ── (1) 사유 다섯 갈래 (회신 EA 반례 꼴) ──────────────────────────────
    A = lambda w, d=None, hold=None, order=None, gap=None: {
        "winner": w, "decision": d or (f"승자 {w}" if w else f"UMA 로는 못 가른다 (승자–차저 {gap or 0.1:.3f} < 0.2)"),
        "hold_reasons": hold, "order": order, "winner_runner_up_gap_eV": gap}
    v = verdict_reason(A("F_B"), A("F_B"), True)
    chk(v["code"] == "①" and v["final_winner"] == "F_B" and "같은 가족이 선택" in v["sentence"] and "순서" not in v["final_decision"]
        and LIMIT_D in v["sentence"] and "같은 구조 골짜기" in DISCLAIMER and "같은 최저 런" in DISCLAIMER,
        "[양성] ① 같은 선택 → '두 시점에서 같은 가족이 선택됐다' · 문장 · ⚠ 에 '전체 순서 · 같은 최저 런 · 같은 골짜기 아님' (EC P2-4)")
    v = verdict_reason(A("F_B"), A(None, order=["F_B", "F_P", "F_free"], gap=0.10), True)
    chk(v["code"] == "③" and v["final_winner"] is None and "바뀌" not in v["sentence"] + v["final_decision"]
        and v["at_50ps_lowest"] == "F_B" and v["lowest_50_is_winner_100"] and "['F_B', 'F_P', 'F_free']" in v["final_decision"],
        "⛔음성: ③ 50 ps 여유 부족 → 순서 역전이라 쓰지 않는다 · 50 ps 순서 · 최저를 적는다 (EA margin_only · EC P2-4)")
    v = verdict_reason(A("F_B"), A(None, order=["F_P", "F_B", "F_free"], gap=0.15), True)
    chk(v["code"] == "③" and v["at_50ps_lowest"] == "F_P" and v["lowest_50_is_winner_100"] is False
        and "다른 가족" in v["final_decision"] and "다른 가족" in v["reason"],
        "⛔음성: ③ 인데 50 ps 최저가 100 ps 승자와 다른 가족 → 그 사실을 사유 · 최종 판정에 적는다 (EC P2-4)")
    v = verdict_reason(A("F_B"), A(None, "승자 보류", ["F_P: G1 실패 (성공 14 < 15 · 탈락)"]), True)
    chk(v["code"] == "④" and v["final_winner"] is None and "바뀌" not in v["sentence"], "⛔음성: ④ 50 ps 판독 보류 → 판독 보류 (EA unavailable_50)")
    v = verdict_reason(A("F_B"), A("F_P"), True)
    chk(v["code"] == "②" and v["final_winner"] is None, "⛔음성: ② 다른 승자 → 시간에 일관된 승자 없음")
    v = verdict_reason(A("F_B"), A("F_B"), False)
    chk(v["code"] == "④" and v["final_winner"] is None, "⛔음성: ④ 성공 집합이 두 시점에서 다르면 같은 승자여도 보류 (EA false_same_winner)")
    v = verdict_reason(A(None, "UMA 로는 못 가른다"), A("F_B"), True)
    chk(v["code"] == "⑤" and v["final_winner"] is None and v["final_decision"] == "UMA 로는 못 가른다",
        "⛔음성: ⑤ 본 판독 승자 없음 → 50 ps 로 올리지 않는다 (그대로)")
    v = verdict_reason(A(None, "UMA 로는 못 가른다"), A("F_B"), False)
    chk(v["code"] == "⑤" and v["final_decision"] == "UMA 로는 못 가른다",
        "⛔음성: ⑤ 와 집합 다름이 겹치면 ⑤ 가 먼저 (평가 순서 ⑤ → ④ · EC P2-1)")

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

    def T_of(t):                                    # 궤적 · md.log 의 순간 온도 (시각마다 다르게)
        return 500.0 + (t % 5)

    def with_ET(a, E, T):                           # 프레임에 에너지 (계산기) · 운동량 (그 온도) 을 싣는다
        m = a.get_masses()
        a.set_momenta(np.stack([np.sqrt(2 * m * 1.5 * units.kB * T), np.zeros(len(a)), np.zeros(len(a))], 1))
        a.calc = SinglePointCalculator(a, energy=E)
        return a

    def idn(sha, stage, time_ps=0.0, T=500.0, purpose=None, seed=1, **over):
        d = {"input_file_sha256": sha, "input_struct": "x", "n_atoms": 6, "stage": stage, "temperature_K": float(T),
             "time_ps": float(time_ps), "dt_fs": 2.0, "friction": 0.01, "relax_steps": 1500, "relax_fmax": 0.05,
             "cell_relax": True, "seed": seed, "model": "uma-s-1p1/omat"}
        if purpose is not None:
            d["purpose"] = purpose
        d.update(over)
        return d

    def put(d, n, kind, E, status, ident, traj=None, mdlog_E=None, end_kind=None, relax_atoms=None, traj_energy=True,
            mdlog_attempts=None, traj_momenta=True):
        w = d / n
        w.mkdir(parents=True, exist_ok=True)
        a = toy(kind)
        write(str(w / "post_md.xyz"), a)
        write(str(w / "post_relax.xyz"), relax_atoms if relax_atoms is not None else toy(end_kind or kind))
        if status == "failed":
            return {"name": n, "status": "failed", "error": "x", "identity": ident, "identity_sha": RA.identity_sha(ident)}
        rec = {"name": n, "status": status, "converged": status == "converged", "E_post_relax": E, "identity": ident,
               "identity_sha": RA.identity_sha(ident), "composition": RA._composition(a),
               "outputs": {k: {"rel": f"{n}/{k}.xyz", "sha256": RA._file_sha256(w / f"{k}.xyz")} for k in ("post_md", "post_relax")}}
        E0 = mdlog_E if mdlog_E is not None else 0.0
        if traj:
            nf, dt, le, ns = traj
            T_ = Trajectory(str(w / "md.traj"), "w")
            for k in range(nf):
                t = k * dt * le / 1000.0
                fr = toy(kind, shift=0.001 * k)
                if traj_energy and traj_momenta:
                    fr = with_ET(fr, E0 + 0.001 * t, T_of(t))
                elif traj_energy:                   # 에너지만 (운동량 없음)
                    fr.calc = SinglePointCalculator(fr, energy=E0 + 0.001 * t)
                T_.write(fr)
            T_.close()
            rec["outputs"]["md_traj"] = {"rel": f"{n}/md.traj", "sha256": RA._file_sha256(w / "md.traj"),
                                         "n_frames": nf, "log_every_steps": le, "dt_fs": dt, "n_steps": ns}
        if mdlog_E is not None:
            rows = []
            for lo, hi, off in (mdlog_attempts or ((0, 100, 0.0),)):
                rows.append("Time[ps]      Etot[eV]     Epot[eV]     Ekin[eV]    T[K]")
                rows += [f"{t:<10.4f} {E0 + off:.4f} {E0 + off + 0.001 * t:.6f} 0.0 {T_of(t):.1f}" for t in range(lo, hi + 1)]
            (w / "md.log").write_text("\n".join(rows) + "\n")
        return rec

    def save(d, recs, fname="anneal_results.json"):
        d.mkdir(parents=True, exist_ok=True)
        (d / fname).write_text(json.dumps({"results": recs}))
        return d / fname

    _vm = EN.verify_manifest
    EN.verify_manifest = lambda gd: []          # 생성기 검증은 생성기 selftest 몫 (판독기 selftest 와 같은 처리)
    try:
        with _tf.TemporaryDirectory() as td:
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
            nan = float("nan")

            def s8(sub, st=None, eshift=None, traj=None, tamper=(), t=100.0, E_map=None, end_kind=None, relax_atoms=None,
                   noenergy=(), mdlog_attempts=None, tamper_post_md=(), nomomenta=()):
                rr = []
                for e in plan:
                    n, F = e["name"], e["family"]
                    E = (E_map or {}).get(n, (eshift or base_E)[F] + 0.01 * e["rank"])
                    rr.append(put(td / sub, n, F, E, (st or {}).get(n, "converged"),
                                  idn(e["start"]["sha256"], "anneal_relax", t, 500, purpose=C["purpose_stage8"],
                                      seed=RA.derive_seed(BASE, n)),
                                  traj=(traj or {}).get(n, (int(t) + 1, 2.0, 500, int(t * 500))),
                                  mdlog_E=(E if math.isfinite(E) else 0.0), end_kind=(end_kind or {}).get(n),
                                  relax_atoms=(relax_atoms or {}).get(n), traj_energy=n not in noenergy,
                                  mdlog_attempts=(mdlog_attempts or {}).get(n), traj_momenta=n not in nomomenta))
                res = save(td / sub, rr)
                for n in tamper:
                    (td / sub / n / "md.traj").write_bytes((td / sub / n / "md.traj").read_bytes() + b"\0")
                for n in tamper_post_md:
                    (td / sub / n / "post_md.xyz").write_bytes((td / sub / n / "post_md.xyz").read_bytes() + b"\n")
                return res

            def RO(res):                            # ① 본 판독 파일 (판 고정 판독기 그대로)
                return RD._dump(RD.anneal_readout(vp, rp, res, k_f=K), td / f"ro_{res.parent.name}.json")

            def relax(sub, xx, dE=None, st=None, over=None, extra=False, drop=(), E_over=None, folder=None, fname="anneal_results.json",
                      tamper_post_relax=()):
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
                res_ = save(d0, rr, fname)
                for n in tamper_post_relax:
                    p_ = d0 / f"{n}_t050" / "post_relax.xyz"
                    p_.write_bytes(p_.read_bytes() + b"\n")
                return res_

            def run(sub, E100=None, E50=None, st100=None, st50=None, end_kind=None, **kw):
                """8 단계 (E100) → 본 판독 파일 → extract → 진단 이완 (E50) → judge."""
                res_ = s8(f"s8_{sub}", st=st100, E_map=E100, end_kind=end_kind, **kw)
                xp_, x_ = extract(RD, vp, rp, res_, td / f"fr_{sub}", k_f=K)
                rel_ = relax(f"rx_{sub}", x_, st=st50, E_over=E50)
                return judge(RD, xp_, rel_, RO(res_), k_f=K), x_

            # 정상 경로 ① — 같은 선택
            res = s8("s8")
            A100 = RD.anneal_readout(vp, rp, res, k_f=K)
            ro = RO(res)
            chk(A100["winner"] == "F_B", "[양성] 사슬: 8 단계 본 판독 (실제 판독기) → 승자 F_B")
            xp, x = extract(RD, vp, rp, res, td / "fr", k_f=K)
            chk(x["n_frames"] == 18 and all(f["frame"] == 50 for f in x["frames"].values())
                and all(abs(read(str(td / "fr" / f["file"])).positions[5, 0] - (10.0 + 0.05)) < 1e-6 for f in x["frames"].values()),
                "[양성] extract: 18 런 모두 프레임 50 (500 걸음 × 2 fs) — 파일 = 부모 궤적의 그 프레임")
            chk(x["diag_tool"]["sha256"] == _sha_file(SELF) and x["readout_tool"]["sha256"] == RD.__diag_sha256__,
                "[양성] 출처에 진단 도구 · 판독기 sha256 (EC P1-1)")
            rr0 = relax("rx", x)
            out = judge(RD, xp, rr0, ro, k_f=K)
            chk(out["verdict"]["code"] == "①" and out["verdict"]["final_winner"] == "F_B"
                and out["at_100ps_main_readout_preserved"]["winner"] == "F_B" and out["at_50ps"]["winner"] == "F_B",
                "[양성] judge (실제 판독기 · 검증된 100 ps 기록 ↔ 50 ps 기록) → ① 같은 선택 F_B")
            chk(out["diag_tool"]["sha256"] == _sha_file(SELF) and out["readout_tool"]["sha256"] == RD.__diag_sha256__
                and out["extract_tools"]["diag_tool"]["sha256"] == _sha_file(SELF),
                "[양성] 판독 출력에 진단 도구 · 판독기 sha256 (EC P1-1)")
            vb = out["verdict"]["beside_minimum_not_gates"]
            chk(vb["pairs"]["100"] == out["at_100ps_main_readout_preserved"]["pairs"] and vb["pairs"]["50"] == out["at_50ps"]["pairs"]
                and vb["family_median_E"] == out["records"]["family_median_E"],
                "[양성] 판정 옆에 두 시점 짝 판정 · 가족 E 중앙 (게이트 아님 · EC P2-4)")
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
            mw = out["md_window"]["per_run"][nm("F_B", 0)]
            chk(near(mw["Epot_change_eV"], 0.05) and mw["40-50ps"]["n"] == 11 and mw["90-100ps"]["n"] == 11
                and mw["40-50ps"]["frames"] == [40, 50] and near(mw["40-50ps"]["T_mean_K"], 500 + 20 / 11, 1e-6)
                and near(mw["40-50ps"]["Epot_mean_eV"], -0.5 + 0.045) and "md.traj" in out["md_window"]["source"]
                and mw["md_log_crosscheck"]["multi_attempt"] is False
                and mw["md_log_crosscheck"]["last_attempt_max_abs_dEpot_vs_traj_eV"] < 1e-5
                and mw["md_log_crosscheck"]["last_attempt_max_abs_dT_vs_traj_K"] < 0.06,
                "[양성] 구간 [40,50] · [90,100] ps 평균 = sha 로 묶인 md.traj 프레임의 Epot · 온도 (프레임 40–50) · md.log 는 대조 (EC P2-2)")
            chk(judge(RD, xp, rr0, ro, k_f=K)["verdict"]["code"] == "①", "[양성] 본 판독 파일 = 다시 낸 본 판독 → 진행")
            Ab = copy.deepcopy(A100); Ab["winner"] = "F_P"
            rdb = RD._dump(Ab, td / "s8_readout_bad.json")
            chk(refuses("본 판독 파일", judge, RD, xp, rr0, rdb, k_f=K), "⛔음성: 본 판독 파일이 다시 낸 것과 다르면 멈춘다")
            chk(refuses("본 판독 파일 (--readout) 이 없다", judge, RD, xp, rr0, None, k_f=K),
                "⛔음성: 본 판독 파일 없이 판독하지 않는다 (--readout 필수 · EC P2-5)")
            # ③ · ② · ⑤
            o3 = judge(RD, xp, relax("rx3", x, dE={"F_B": 0.25, "F_P": 0.1, "F_free": 0.1}), ro, k_f=K)
            chk(o3["verdict"]["code"] == "③" and o3["at_50ps"]["winner"] is None and o3["verdict"]["at_50ps_lowest"] == "F_B"
                and o3["verdict"]["lowest_50_is_winner_100"], "⛔음성: 50 ps 여유 0.15 < 0.20 → ③ (실제 판독기 · 50 ps 최저 F_B = 100 ps 승자)")
            o3b = judge(RD, xp, relax("rx3b", x, dE={"F_B": 0.35, "F_P": 0.1, "F_free": 0.0}), ro, k_f=K)
            chk(o3b["verdict"]["code"] == "③" and o3b["verdict"]["at_50ps_lowest"] == "F_free"
                and o3b["verdict"]["at_50ps_order"] == ["F_free", "F_B", "F_P"] and not o3b["verdict"]["lowest_50_is_winner_100"]
                and "F_free" in o3b["verdict"]["final_decision"],
                "⛔음성: 50 ps 최저가 F_free (F_B 와 0.05 차) → ③ 이되 '다른 가족' 을 적는다 (EC P2-4 · margin_other_lowest)")
            o2 = judge(RD, xp, relax("rx2", x, dE={"F_B": 0.1, "F_P": 0.1, "F_free": -0.5}), ro, k_f=K)
            chk(o2["verdict"]["code"] == "②" and o2["at_50ps"]["winner"] == "F_free", "⛔음성: 50 ps 승자 F_free ≠ 100 ps F_B → ②")
            res5 = s8("s8_5", eshift={"F_B": -0.3, "F_P": 0.0, "F_free": -0.2})
            xp5, x5 = extract(RD, vp, rp, res5, td / "fr5", k_f=K)
            o5 = judge(RD, xp5, relax("rx5", x5, dE={"F_B": -0.3, "F_P": 0.1, "F_free": 0.1}), RO(res5), k_f=K)
            chk(o5["verdict"]["code"] == "⑤" and o5["at_50ps"]["winner"] == "F_B" and o5["verdict"]["final_winner"] is None,
                "⛔음성: 100 ps 못 가름 → ⑤ (50 ps 가 F_B 승자여도 올리지 않는다)")
            o5s = judge(RD, xp5, relax("rx5s", x5, dE={"F_B": -0.3, "F_P": 0.1, "F_free": 0.1}, st={nm("F_P", 2): "unconverged"}),
                        RO(res5), k_f=K)
            chk(o5s["verdict"]["code"] == "⑤" and not o5s["success_sets"]["F_P"]["same"],
                "⛔음성: 100 ps 못 가름 + 성공 집합 다름 → ⑤ (실제 사슬 · ⑤ 가 ④ 보다 먼저)")
            # ④ 성공 집합 — 시점마다 다른 F_B 런이 실패 (EA false_same_winner) · 100 ps 끝 이완 실패 런도 프레임은 뗀다
            res4 = s8("s8_4", st={nm("F_B", 1): "unconverged"})
            xp4, x4 = extract(RD, vp, rp, res4, td / "fr4", k_f=K)
            chk(x4["parent_status"][nm("F_B", 1)] == "relax100_failed" and nm("F_B", 1) in x4["frames"],
                "[양성] 100 ps 끝 이완 실패 (궤적 검증됨) 런도 50 ps 프레임을 뗀다 (가능한 50 ps 결과를 버리지 않는다)")
            ro4 = RO(res4)
            o4 = judge(RD, xp4, relax("rx4", x4, st={nm("F_B", 2): "unconverged"}), ro4, k_f=K)
            chk(o4["verdict"]["code"] == "④" and o4["at_100ps_main_readout_preserved"]["winner"] == "F_B"
                and o4["at_50ps"]["winner"] == "F_B" and not o4["success_sets"]["F_B"]["same"],
                "⛔음성: 두 시점 모두 F_B 승자 (5/6) 지만 실패한 런이 다르면 → ④ 판독 보류 (본 판정 보존)")
            row = next(r for r in o4["records"]["rows"] if r["name"] == nm("F_B", 1))
            chk(row["status_100"].startswith("실패") and row["status_50"] == "ok" and row["dE_100_minus_50"] is None,
                "[양성] 시점별 상태 기록 (100 ps 실패 · 50 ps 성공 · Δ 는 결측)")
            o4s = judge(RD, xp4, relax("rx4s", x4, st={nm("F_B", 1): "unconverged"}), ro4, k_f=K)
            chk(o4s["verdict"]["code"] == "①" and o4s["success_sets"]["F_B"]["same"],
                "[양성] 같은 런이 두 시점 모두 실패 → 성공 집합 같음 → 비교한다 (① · 실패 수만이 아니라 이름이 같아야)")
            o4n = judge(RD, xp, relax("rx4n", x, E_over={nm("F_P", 3): nan}, st={nm("F_P", 3): "unconverged"}), ro, k_f=K)
            chk(o4n["verdict"]["code"] == "④" and next(r for r in o4n["records"]["rows"] if r["name"] == nm("F_P", 3))["status_50"].startswith("실패"),
                "⛔음성: 미수렴 · 비유한 E_50 → 그 런은 50 ps 실패로 센다 (터지지 않는다) → 집합 다름 → ④")
            o4u = judge(RD, xp, relax("rx4u", x, st={nm("F_P", 3): "unconverged"}), ro, k_f=K)
            chk(o4u["verdict"]["code"] == "④", "⛔음성: 50 ps 에서만 미수렴 (한 시점만 실패) → 집합 다름 → ④")
            # EC P2-3 — 진단 이완의 failed (예외) · 수렴 표시인데 결과 검사 · 에너지 실패 → 누락처럼 거부
            chk(refuses("끝나지 않았다", judge, RD, xp, relax("rx_f", x, st={nm("F_free", 2): "failed"}), ro, k_f=K),
                "⛔음성: 진단 이완 하나가 failed (예외) → 판정에 세지 않고 거부 (다시 돌린 뒤 · EC P2-3)")
            chk(refuses("끝나지 않았다", judge, RD, xp, relax("rx_cn", x, E_over={nm("F_P", 3): nan}), ro, k_f=K),
                "⛔음성: 수렴 표시인데 E_50 비유한 → 거부 (손상 기록 · EC P2-3)")
            chk(refuses("끝나지 않았다", judge, RD, xp, relax("rx_ct", x, tamper_post_relax=(nm("F_B", 4),)), ro, k_f=K),
                "⛔음성: 수렴 표시인데 결과 파일이 기록 뒤 바뀜 → 거부 (EC P2-3)")
            # 부모 상태 — 실패 · 궤적 검증 실패 · 저장 간격 250 · 수렴 표시인데 E_100 비유한
            res7 = s8("s8_7", st={nm("F_P", 5): "failed"}, tamper=(nm("F_free", 2),),
                      traj={nm("F_free", 3): (201, 2.0, 250, 50000)}, E_map={nm("F_B", 4): nan})
            xp7, x7 = extract(RD, vp, rp, res7, td / "fr7", k_f=K)
            chk(x7["parent_status"][nm("F_P", 5)] == "parent_failed" and x7["parent_status"][nm("F_free", 2)] == "parent_unverified"
                and nm("F_P", 5) not in x7["frames"] and nm("F_free", 2) not in x7["frames"]
                and any("md_traj" in q for q in x7["parent_detail"][nm("F_free", 2)]),
                "[양성] 부모 런 실패 · 궤적 변조 (궤적 검사 실패) → 프레임 없음 · 사유를 가른다")
            chk(x7["frames"][nm("F_free", 3)]["frame"] == 100
                and abs(read(str(td / "fr7" / x7["frames"][nm("F_free", 3)]["file"])).positions[5, 0] - (10.0 + 0.1)) < 1e-6,
                "[양성] 저장 간격 250 걸음 런은 50 ps = 프레임 100 (기록의 간격으로)")
            chk(x7["parent_status"][nm("F_B", 4)] == "relax100_failed" and nm("F_B", 4) in x7["frames"],
                "[양성] 수렴 표시인데 E_100 비유한 (궤적 멀쩡) → 100 ps 끝 이완 실패 · 프레임을 뗀다")
            o7 = judge(RD, xp7, relax("rx7", x7), RO(res7), k_f=K)
            chk(o7["verdict"]["code"] == "④" and any("50 ps 프레임 없음" in str(f["why"]) for f in o7["at_50ps"]["families"]["F_P"]["failed"]),
                "[양성] 프레임 없는 런은 50 ps 에서도 실패 · 사유 = 부모 상태 (F_B 4 는 50 ps 성공 → 집합 다름 → ④)")
            w250 = o7["md_window"]["per_run"][nm("F_free", 3)]
            chk(w250["40-50ps"]["frames"] == [80, 100] and w250["40-50ps"]["n"] == 21
                and o7["md_window"]["per_run"][nm("F_free", 2)].get("status", "").startswith("부모 궤적 검사 실패"),
                "[양성] 구간 평균도 기록의 저장 간격으로 (250 걸음 → 프레임 80–100) · 궤적 검사 실패 런은 구간 평균 없음")
            # EC P1-2 — 끝 구조만 검사에 걸린 100 ps 실패 (궤적 멀쩡) 는 프레임을 뗀다 · 궤적 변조만 parent_unverified
            bad_relax = toy("F_free"); bad_relax.positions[3, 0] = nan
            res12 = s8("s8_12", st={nm("F_free", 5): "unconverged"}, relax_atoms={nm("F_free", 5): bad_relax},
                       tamper_post_md=(nm("F_P", 4),), tamper=(nm("F_B", 3),))
            xp12, x12 = extract(RD, vp, rp, res12, td / "fr12", k_f=K)
            ps12 = x12["parent_status"]
            chk(ps12[nm("F_free", 5)] == "relax100_failed" and nm("F_free", 5) in x12["frames"]
                and any("NaN" in q for q in x12["parent_detail"][nm("F_free", 5)]),
                "[양성] 100 ps 끝 구조 NaN (발산한 이완 · 궤적 멀쩡) → relax100_failed · 프레임을 뗀다 (EC P1-2 · relax100_nan)")
            chk(ps12[nm("F_P", 4)] == "relax100_failed" and nm("F_P", 4) in x12["frames"]
                and any("post_md" in q for q in x12["parent_detail"][nm("F_P", 4)]),
                "[양성] post_md 파일 sha 불일치 (궤적 멀쩡) → relax100_failed · 프레임을 뗀다 (EC P1-2)")
            chk(ps12[nm("F_B", 3)] == "parent_unverified" and nm("F_B", 3) not in x12["frames"],
                "⛔음성: md.traj 변조 → parent_unverified · 프레임 없음 (EC P1-2)")
            o12 = judge(RD, xp12, relax("rx12", x12), RO(res12), k_f=K)
            chk(o12["verdict"]["code"] == "④" and not o12["success_sets"]["F_free"]["same"] and not o12["success_sets"]["F_P"]["same"]
                and o12["success_sets"]["F_B"]["same"],
                "⛔음성: 그 런들의 50 ps 이완이 성공 → 집합 다름 → ④ (유한 미수렴과 같은 결과 · 실패 모양이 판정을 안 가른다)")
            # EC P2-2 — 궤적에 에너지 · 운동량이 없으면 멈춘다 · md.log 두 시도는 표지 (평균은 궤적에서)
            res_ne = s8("s8_ne", noenergy=(nm("F_P", 1),))
            chk(refuses("퍼텐셜 에너지가 없다", extract, RD, vp, rp, res_ne, td / "fr_ne", k_f=K)
                and not (td / "fr_ne").exists(),
                "⛔음성: 8 단계 궤적 프레임에 에너지가 없으면 extract 가 (GPU 를 쓰기 전에) 멈춘다 · 출력 폴더도 안 만든다 (EC P2-2)")
            res_nm = s8("s8_nm", nomomenta=(nm("F_free", 1),))
            chk(refuses("운동량이 없다", extract, RD, vp, rp, res_nm, td / "fr_nm", k_f=K),
                "⛔음성: 궤적 프레임에 에너지는 있고 운동량이 없으면 멈춘다 (온도를 0 K 로 지어내지 않는다 · EC P2-2)")
            o_ml, _ = run("ml", mdlog_attempts={nm("F_B", 0): ((0, 60, 5.0), (0, 100, 0.0)), nm("F_P", 0): ((0, 100, 0.01),)})
            mw2 = o_ml["md_window"]["per_run"][nm("F_B", 0)]
            cc = mw2["md_log_crosscheck"]
            chk(near(mw2["Epot_change_eV"], 0.05) and mw2["40-50ps"]["n"] == 11 and cc["multi_attempt"] is True and cc["headers"] == 2
                and cc["rows"] == 162 and "⚠" in cc and cc["last_attempt_max_abs_dEpot_vs_traj_eV"] < 1e-5,
                "⛔음성: md.log 에 시도가 둘 (덧붙여 씀) → 표지 · 구간 평균은 궤적에서 그대로 (변화 0.05 · 섞임 없음 · EC P2-2)")
            cp = o_ml["md_window"]["per_run"][nm("F_P", 0)]["md_log_crosscheck"]
            chk(cp["multi_attempt"] is False and near(cp["last_attempt_max_abs_dEpot_vs_traj_eV"], 0.01, 1e-5)
                and cp["last_attempt_max_abs_dT_vs_traj_K"] < 0.06 and cp["last_attempt_time_mismatch"] == 0,
                "⛔음성: md.log 가 궤적과 0.01 eV 어긋나면 대조 값이 그 차를 그대로 보인다 (한 시도 · 표지 없음 · 대조는 기록만)")
            # EC P2-1 — 회신 EA 반례를 실제 사슬로 (합성 · 손계산 값과 대조)
            # (가) same_drift_summaries — Δ 모두 −0.4 · F_B 바탕 5 만 −3.0 (최저 런이 바뀐다) · F_free 2 의 100 ps 끝 꼴이 F_P (꼴 바뀜 1)
            E50 = {nm(F, b): {"F_B": -0.30 + 0.05 * b, "F_P": 0.0, "F_free": 0.5}[F] for F in FAM for b in range(6)}
            E100 = {n: E - 0.4 for n, E in E50.items()}
            E100[nm("F_B", 5)] = E50[nm("F_B", 5)] - 3.0
            o_sd, _ = run("sd", E100=E100, E50=E50, end_kind={nm("F_free", 2): "F_P"})
            r = o_sd["records"]
            dB = r["delta_by_family"]["F_B"]
            chk(o_sd["verdict"]["code"] == "①" and near(dB["median"], -0.4) and near(dB["min"], -3.0) and near(dB["max"], -0.4)
                and near(dB["max_abs"], 3.0) and dB["n_lower_at_100"] == 6 and dB["n_higher_at_100"] == 0 and near(dB["IQR"], 0.0),
                "[양성] EA same_drift: ① · Δ F_B 중앙 −0.4 · 최솟값 −3.0 · 최댓값 −0.4 · max|Δ| 3.0 · 내려간 6 · 올라간 0 (손계산)")
            fm = r["family_minimum"]
            chk(fm["50"]["F_B"]["name"] == nm("F_B", 0) and fm["100"]["F_B"]["name"] == nm("F_B", 5)
                and near(fm["50"]["F_B"]["dE_100_minus_50_of_this_run"], -0.4) and near(fm["100"]["F_B"]["dE_100_minus_50_of_this_run"], -3.0),
                "[양성] EA same_drift: F_B 최저 런 50 ps 바탕 0 (Δ −0.4) → 100 ps 바탕 5 (Δ −3.0) (손계산)")
            gg = r["family_minimum_gaps"]
            chk(near(gg["m_F_P − m_F_B"]["50"], 0.30) and near(gg["m_F_P − m_F_B"]["100"], 2.65)
                and near(gg["m_F_P − m_F_B"]["change_100_minus_50"], 2.35) and near(gg["m_F_free − m_F_P"]["change_100_minus_50"], 0.0),
                "[양성] EA same_drift: m_F_P − m_F_B 0.30 → 2.65 (변화 +2.35) · m_F_free − m_F_P 변화 0 (손계산)")
            p5 = next(q for q in r["paired_change"]["δ_F_BF_P = Δ_F_B − Δ_F_P"]["per_base"] if q["base"] == 5)
            chk(near(p5["delta"], -2.6) and near(r["family_median_E"]["50"]["F_B"], -0.175) and near(r["family_median_E"]["100"]["F_B"], -0.625),
                "[양성] EA same_drift: δ_F_BF_P (바탕 5) = Δ_F_B − Δ_F_P = −2.6 · 가족 E 중앙 F_B −0.175 → −0.625 (손계산)")
            rf2 = next(q for q in r["rows"] if q["name"] == nm("F_free", 2))
            chk(r["n_end_motif_changed_50_to_100"] == 1 and rf2["end_motif_50"] == "F_free" and rf2["end_motif_100"] == "F_P",
                "[양성] 끝 꼴이 50 → 100 ps 에 바뀐 런 1 (F_free 바탕 2 · F_free → F_P)")
            # (나) common_per_base_drift — 바탕마다 세 가족에 같은 Δ_b (짝 차 보존) · 최저가 다른 바탕에서 → 승자 F_B → F_P (②)
            Db = [0.0, -0.1, -0.2, -0.8, -0.4, -0.5]
            E50 = {nm(F, b): {"F_B": -0.3 if b == 0 else 0.6, "F_P": 0.0 if b == 3 else 0.5, "F_free": 1.0}[F] for F in FAM for b in range(6)}
            E100 = {nm(F, b): E50[nm(F, b)] + Db[b] for F in FAM for b in range(6)}
            o_cd, _ = run("cd", E100=E100, E50=E50)
            r = o_cd["records"]
            pcd = r["paired_change"]
            chk(o_cd["verdict"]["code"] == "②" and all(abs(q["delta"]) < 1e-9 for v_ in pcd.values() for q in v_["per_base"])
                and all(v_["n"] == 6 for v_ in pcd.values()),
                "[양성] EA common_per_base_drift: δ 전부 0 (짝 차 보존) 인데 ② 승자 F_B → F_P (손계산)")
            dC = r["delta_by_family"]["F_P"]
            chk(near(dC["median"], -0.3) and near(dC["q25"], -0.475) and near(dC["q75"], -0.125) and near(dC["IQR"], 0.35)
                and near(dC["min"], -0.8) and near(dC["max"], 0.0) and near(dC["max_abs"], 0.8) and dC["n_lower_at_100"] == 5
                and dC["n_higher_at_100"] == 0,
                "[양성] EA common_per_base_drift: Δ F_P 중앙 −0.3 · IQR 0.35 (q25 −0.475 · q75 −0.125) · 최솟값 −0.8 · 최댓값 0 · 내려간 5 (손계산)")
            gg = r["family_minimum_gaps"]
            chk(near(gg["m_F_P − m_F_B"]["50"], 0.3) and near(gg["m_F_P − m_F_B"]["100"], -0.5)
                and near(gg["m_F_P − m_F_B"]["change_100_minus_50"], -0.8) and near(gg["m_F_free − m_F_B"]["change_100_minus_50"], -0.8)
                and near(gg["m_F_free − m_F_P"]["change_100_minus_50"], 0.0),
                "[양성] EA common_per_base_drift: m_F_P − m_F_B 0.3 → −0.5 (변화 −0.8) · m_F_free − m_F_P 변화 0 (손계산)")
            fm = r["family_minimum"]
            chk(fm["50"]["F_free"]["name"] == nm("F_free", 0) and fm["100"]["F_free"]["name"] == nm("F_free", 3)
                and fm["50"]["F_P"]["name"] == fm["100"]["F_P"]["name"] == nm("F_P", 3),
                "[양성] EA common_per_base_drift: 최저 런 F_free 바탕 0 → 3 · F_P 바탕 3 그대로 (시점 표지 · 손계산)")
            pv50, pv100 = r["pairs_verdict"]["50"], r["pairs_verdict"]["100"]
            chk(pv50 == {"n": 6, "same_sign_as_order": 1, "같은_방향": False} and pv100 == {"n": 6, "same_sign_as_order": 5, "같은_방향": True}
                and o_cd["verdict"]["beside_minimum_not_gates"]["pairs"] == {"50": pv50, "100": pv100},
                "[양성] EA common_per_base_drift: 짝 판정 50 ps 1/6 · 100 ps 5/6 (시점 표지 · 판정 옆 · 손계산)")
            md_ = r["family_median_E"]
            chk(near(md_["50"]["F_B"], 0.6) and near(md_["50"]["F_P"], 0.5) and near(md_["100"]["F_B"], 0.15)
                and near(md_["100"]["F_P"], 0.2) and near(md_["100"]["F_free"], 0.7),
                "[양성] EA common_per_base_drift: 가족 E 중앙 50 ps F_B 0.6 · F_P 0.5 → 100 ps 0.15 · 0.2 · F_free 0.7 (손계산)")
            # (다) outlier_minimum — F_P 하나만 −1.0 · 나머지 +0.2 · F_B 0 · F_free 1.0 (두 시점 같음) → ① F_P · 짝 1/6 · 중앙 F_P > F_B
            Eo = {nm(F, b): {"F_B": 0.0, "F_P": -1.0 if b == 0 else 0.2, "F_free": 1.0}[F] for F in FAM for b in range(6)}
            o_om, _ = run("om", E100=Eo, E50=dict(Eo))
            vo_ = o_om["verdict"]
            bz = vo_["beside_minimum_not_gates"]
            chk(vo_["code"] == "①" and vo_["final_winner"] == "F_P" and "초기 가족 F_P의" in vo_["sentence"]
                and bz["pairs"]["100"] == {"n": 6, "same_sign_as_order": 1, "같은_방향": False}
                and near(bz["family_median_E"]["100"]["F_P"], 0.2) and near(bz["family_median_E"]["100"]["F_B"], 0.0),
                "[양성] EA outlier_minimum: ① F_P (문장에 그 가족) · 판정 옆 짝 1/6 · 중앙 F_P 0.2 > F_B 0 (확장 금지를 보여 줌)")
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
            chk(refuses("부모 궤적의 50 ps 프레임과 다르다", judge, RD, xpo, relax("rx_o", xo), ro, k_f=K),
                "⛔음성: 다른 런의 프레임 (sha 를 맞춰도) → 부모 궤적에서 다시 읽어 거부")

            def frame49(d, xx):                     # 49 ps 프레임 (출처 번호 · 파일 · sha 를 다 맞춰도)
                mt = json.loads(res.read_text())["results"]
                rec0 = next(r_ for r_ in mt if r_["name"] == n0)
                with Trajectory(str(td / "s8" / rec0["outputs"]["md_traj"]["rel"])) as T:
                    fr = T[49]
                    a = Atoms(fr.get_chemical_symbols(), positions=fr.get_positions(), cell=fr.cell.array, pbc=fr.pbc)
                f0 = d / xx["frames"][n0]["file"]
                write(str(f0), a)
                xx["frames"][n0].update(frame=49, sha256=_sha_file(f0))
            xp49, x49 = tamper_frames("fr_49", frame49)
            chk(refuses("50 ps 프레임 50", judge, RD, xp49, relax("rx_49", x49), ro, k_f=K), "⛔음성: 49 ps 프레임 → 거부")

            def swap(d, xx):                        # 스냅숏 교체 (좌표를 조금 옮긴 파일 · sha 는 맞춘다)
                f0 = d / xx["frames"][n0]["file"]
                a = read(str(f0)); a.positions[3] += 0.01
                write(str(f0), a)
                xx["frames"][n0]["sha256"] = _sha_file(f0)
            xps_, xs_ = tamper_frames("fr_swap", swap)
            chk(refuses("부모 궤적의 50 ps 프레임과 다르다", judge, RD, xps_, relax("rx_s", xs_), ro, k_f=K), "⛔음성: 스냅숏 교체 → 거부")

            def fixatoms(d, xx):                    # 좌표 · 셀 · 원소 · PBC 그대로 · 전 원자 FixAtoms (sha 는 맞춘다) — EC P2-5 가
                f0 = d / xx["frames"][n0]["file"]
                a = read(str(f0)); a.set_constraint(FixAtoms(indices=list(range(len(a)))))
                write(str(f0), a)
                xx["frames"][n0]["sha256"] = _sha_file(f0)
            xpfx, xfx = tamper_frames("fr_fix", fixatoms)
            chk(refuses("제약", judge, RD, xpfx, relax("rx_fx", xfx), ro, k_f=K),
                "⛔음성: 이완 입력에 FixAtoms (기하는 그대로 · sha 맞춤) → 거부 (EC P2-5 · 옛 판은 통과)")

            def tags(d, xx):                        # 추가 배열 (tags) — 기하 그대로
                f0 = d / xx["frames"][n0]["file"]
                a = read(str(f0)); a.set_tags([1] * len(a))
                write(str(f0), a)
                xx["frames"][n0]["sha256"] = _sha_file(f0)
            xptg, xtg = tamper_frames("fr_tags", tags)
            chk(refuses("추가 배열", judge, RD, xptg, relax("rx_tg", xtg), ro, k_f=K), "⛔음성: 이완 입력에 추가 배열 (tags) → 거부 (EC P2-5)")

            def info(d, xx):                        # 바이트만 다름 (설명 줄의 info 키 · 기하 · 배열 · 제약 그대로)
                f0 = d / xx["frames"][n0]["file"]
                a = read(str(f0)); a.info["note"] = "x"
                write(str(f0), a)
                xx["frames"][n0]["sha256"] = _sha_file(f0)
            xpin, xin = tamper_frames("fr_info", info)
            chk(refuses("다시 쓴 바이트", judge, RD, xpin, relax("rx_in", xin), ro, k_f=K),
                "⛔음성: 기하 · 배열 · 제약은 같고 바이트만 다른 입력 → 다시 쓴 바이트 sha 로 거부 (EC P2-5)")
            xpst, _ = tamper_frames("fr_st", lambda d, xx: xx["parent_status"].update({n0: "parent_no_traj"}))
            chk(refuses("부모 상태", judge, RD, xpst, rr0, ro, k_f=K), "⛔음성: 출처의 부모 상태를 바꾸면 거부")
            xpdr, xdr = tamper_frames("fr_drop", lambda d, xx: xx["frames"].pop(n1))
            chk(refuses("진단 프레임 이름 집합", judge, RD, xpdr, relax("rx_dr", xdr), ro, k_f=K),
                "⛔음성: 출처에서 프레임 하나를 빼면 거부 (빼면 50 ps 실패로 조용히 세어 ④ 가 된다)")
            xpfb, _ = tamper_frames("fr_fb", lambda d, xx: xx["frames"][n0].update(family="F_P"))
            chk(refuses("초기 가족", judge, RD, xpfb, rr0, ro, k_f=K), "⛔음성: 출처의 초기 가족 · 바탕을 바꾸면 거부 (이름으로 결속)")
            xpdt, _ = tamper_frames("fr_dt", lambda d, xx: xx["diag_tool"].update(sha256="0" * 64))
            chk(refuses("진단 도구 sha256", judge, RD, xpdt, rr0, ro, k_f=K),
                "⛔음성: extract 때 진단 도구와 다른 판 (sha) → 거부 (EC P1-1)")
            xprt, _ = tamper_frames("fr_rt", lambda d, xx: xx["readout_tool"].update(sha256="0" * 64))
            chk(refuses("판독기 sha256", judge, RD, xprt, rr0, ro, k_f=K),
                "⛔음성: extract 때 판독기와 다른 판 (sha) → 거부 (EC P1-1)")
            f0 = td / "fr" / x["frames"][n0]["file"]
            keep = f0.read_bytes(); f0.write_bytes(keep + b"\n")
            chk(refuses("프레임 파일", judge, RD, xp, rr0, ro, k_f=K), "⛔음성: 진단 프레임 파일이 출처 기록 뒤 바뀌면 거부")
            f0.write_bytes(keep)
            chk(refuses("진단 프레임이 아닌", judge, RD, xp, relax("rx_x", x, extra=True), ro, k_f=K), "⛔음성: 섞인 기록 → 거부")
            chk(refuses("진단 이완 결과 누락", judge, RD, xp, relax("rx_m", x, drop={f"{n1}_t050"}), ro, k_f=K),
                "⛔음성: 진단 이완 누락 → 거부 (누락 ≠ 실패)")
            for label, ov, kw in (("목적 8 단계", {"purpose": C["purpose_stage8"]}, "실행 목적"), ("단계 어닐", {"stage": "anneal_relax"}, "단계"),
                                  ("time_ps 0.5", {"time_ps": 0.5}, "time_ps"), ("fmax 0.02", {"relax_fmax": 0.02}, "relax_fmax"),
                                  ("셀 고정", {"cell_relax": False}, "cell_relax"), ("시작 sha", {"input_file_sha256": "0" * 64}, "시작 파일")):
                chk(refuses(kw, judge, RD, xp, relax("rx_i" + str(abs(hash(label)) % 10**6), x, over={n0: ov}), ro, k_f=K),
                    f"⛔음성: 진단 이완 기록의 {label} → 거부")
            k8 = res.read_bytes()
            chk(refuses("8 단계 폴더", judge, RD, xp, relax("rx_in8", x, folder=td / "s8", fname="diag_relax.json"), ro, k_f=K)
                and res.read_bytes() == k8, "⛔음성: 진단 이완 결과가 8 단계 폴더 (다른 파일 이름이어도) → 거부")
            rk = res.read_bytes(); res.write_bytes(rk + b" ")
            chk(refuses("묶인 입력", judge, RD, xp, rr0, ro, k_f=K), "⛔음성: 묶인 입력 (8 단계 결과) 이 바뀌면 거부")
            res.write_bytes(rk)
            chk(judge(RD, xp, rr0, ro, k_f=K)["verdict"]["code"] == "①", "[양성] 되돌린 뒤 다시 판독 = 같다")
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
    j.add_argument("--readout", required=True, help="8 단계 본 판독 파일 (① 의 출력 · 다시 낸 본 판독과 몸통 대조 · 필수)")
    j.add_argument("--out", required=True)
    A = ap.parse_args(argv)
    RD = load_rd(A.readout_tool)
    me = _tool_fp()
    print(f"진단 도구 {me['path']} · sha256 {me['sha256']}")
    print(f"판독기 {RD.__diag_path__} · sha256 {RD.__diag_sha256__}")
    if RD.__diag_sha256__ != PINNED_RD_SHA256:
        raise SystemExit(f"⛔ 판독기 sha256 이 판 고정 값 ({PINNED_RD_SHA256[:12]}… = 12b8bdef) 이 아니다 — 판 고정 판독기로만 판독한다")
    if A.cmd == "extract":
        xp, x = extract(RD, A.verdict, A.receipt, A.results, A.out_dir)
        cnt = {}
        for s in x["parent_status"].values():
            cnt[s] = cnt.get(s, 0) + 1
        print(f"-> {xp} · 프레임 {x['n_frames']} 개 (50 ps) · 부모 상태 {cnt}")
        print(f"   실행기: CAND={Path(A.out_dir).resolve()} · N_EXPECT={x['n_frames']} · TIME_PS=0 · 새 OUTNAME · run_rc 0 · check_rc 0 일 때만 judge")
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
