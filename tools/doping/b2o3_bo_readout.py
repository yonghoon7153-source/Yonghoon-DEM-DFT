#!/usr/bin/env python3
"""b2o3_bo_readout.py — B·O 배치 카드 개정 1 (셀구축 v1.1) 판독기 — 결과 **전에** 만든 판독 계약의 기계판.

카드 db/properties/b2o3_bo_placement_estimand_2026_11_09.json `개정_1_셀구축_v1_2026_11_09.판독_계약` 을 그대로 옮긴다
(Codex DV Q5 · Q6 · P2 — 끝 꼴 · G3 분모 · 결측 처리 · 연속 파일럿 세 끝점 · 승자–차저 · EOS 가족별 B ·
 Codex DW P1-1 · P1-2 · P1-3 · P2 — 단계 결속 · 파일럿 시간축 · EOS 기준 순서 · 비유한 기하).

단계 사슬 (DW P1-1 · P1-2) — 각 단계는 앞 단계 파일을 sha256 으로 묶고, 묶인 입력에서 앞 판정을 **다시 내서** 같은지 본다
(손으로 바꾼 판정 · 영수증 · 다른 묶음의 결과는 거부한다)
  screen   6 단계 — 생성 manifest (구조 이름 · 시작 파일 sha256) + 이완만 결과 → 거름 판정
           · 누락 (기록 없음) 이 있으면 '거름 미완료' — 합집합 · 파일럿을 내지 않는다 (누락 ≠ 실패)
           · 실패 (미수렴 · 결과 검사 실패) 는 세어 적고 순위에서 뺀다 · 가족 하나라도 성공이 k_f 미만이면 '거름 보류'
           · 기록마다 정체성 필수 · 시작 파일 = manifest 의 그 구조 파일 (sha256) · 단계 · 설정 = 카드 값 · 계획 밖 기록 = 거부
           · 완결이면 합집합 · 파일럿 구조 · 8 단계 계획 (합집합 × 세 가족 · 시작 파일 = 6 단계 post_relax · sha256 ·
             6 단계에서 실패한 항목은 시작 없음 → 8 단계 실패로 센다) · --plan_dir 이면 실행기용 시작 파일 manifest 둘
  extract  7 단계 — 거름 판정 + 파일럿 100 ps 런 기록 → 20 · 50 · 100 ps 프레임 스냅숏 + 출처 + 실행기용 manifest
           · 저장 간격 · dt · 프레임 수는 **런 기록 (outputs.md_traj)** 에서만 — 명령줄로 받지 않는다 (DW P1-2)
           · 런 = 파일럿 구조 하나 · 시작 파일 = 판정의 파일럿 시작 sha256 · 100 ps · 500 K · 카드 설정
  pilot    7 단계 — 출처 (궤적 sha256 → 프레임 번호 → 스냅숏 좌표 다시 대조) + 세 스냅숏 이완 결과 → 파일럿 영수증
           (t_a 20 또는 100 ps · 아니면 '파일럿 미완료')
  anneal   8 단계 — 거름 판정 + 파일럿 영수증 (같은 판정에서 나온 것) + 어닐 결과
           · 계획 전체가 있어야 판독 (누락이면 거부) · 계획 밖 기록 = 거부 · 시간 = t_a · 500 K · 설정 · 시작 파일 대조
           · G1 분모 = 계획 수 (시작 없는 항목 · 실패 포함) → G1 · G2 · G3 · 가족 최저 · 공통 성공 짝 · 승자–차저 (또는 보류)
  eos      9 단계 ③ — 기준 (보정 전) 의 **전체 순서와 0.10 판정**이 가족별 B 독립 2³ 조합 모두에서 그대로인가 (DW P1-3)

성공 (판독에 쓰는 구조) = run_anneal 상태 converged **이고** verify_outputs (결과 파일 존재 · sha256 · 판독 · 조성 ·
기하 유효 — 유한 좌표 · 셀 · 특이 셀 아님 · md_traj 기록이 있으면 궤적까지) 통과 · 유한 에너지.
가족 표지 = 시작 가족 (생성기 manifest) · 끝 꼴은 따로 센다 (G3).

⛔ 이 도구가 못 하는 것
  · 판정 문장을 쓰지 않는다 — 허용 · 금지 서술은 카드에서만.
  · UMA 가 맞는지 모른다 (UMA 내부 비교) · 최저가 진짜 바닥인지 모른다 ('선언한 표본에서 찾은 최저') ·
    6 단계에서 실패한 구조의 에너지는 모른다 (순위에서 빠진다 — 실패 목록으로 적는다).
  · 끝 꼴 분류는 거리 문턱 (O–B · O–P < 1.8 Å 결합 · 1.8–2.3 Å 미분류) 의 기하 분류다 — 결합 차수 · 전하를 보지 않는다.
  · 어닐이 Li 초기점 의존성을 없앴다고 말하지 않는다.
  · 실행기를 돌리지 않는다 — 실행기가 받을 시작 파일 manifest 를 쓰고, 결과가 그 파일 · 설정에서 나왔는지만 본다.
  · seed 는 대조하지 않는다 (실행기 기본 seed 에서 이름으로 유도 — 재현의 필요조건일 뿐).
  · eos 의 가족별 (E, P, V) 입력은 아직 결과 파일에 묶지 않는다 — DFT 단계 앞에 붙인다 (DW P1-3 '9 단계 전 조건').

  python3 tools/doping/b2o3_bo_readout.py --selftest
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, os, sys
from pathlib import Path
import numpy as np
from ase import Atoms
from ase.io import read, write

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_RA = _load("run_anneal_mod", HERE / "run_anneal.py")        # verify_outputs · identity_sha · _file_sha256 (결속 규칙 하나)
_EN = _load("b2o3_enumerate_mod", HERE / "b2o3_enumerate.py")  # verify_manifest · mic_dists

# ── 판독 계약 (카드 개정 1 · 판독_계약 과 같아야 한다 — selftest 가 카드 값과 대조) ─────────────────
CONTRACT = {
    "families": {"bo4": "F_B", "distributed": "F_P", "free_s": "F_free"},
    "unit_B2O3": 1,                      # 에너지 차 / 1
    "k_f": 6,                            # 6 단계 가족마다 상위 바탕 수
    "k_f_shortfall": "hold",             # 성공이 k_f 미만인 가족이 있으면 거름 보류 (DW 제안 · 있는 것만 넣지 않는다)
    "r_bond_A": 1.8,                     # O–B · O–P 결합 (기존: Nd O 꼴 카드 P–O < 1.8 Å)
    "r_grey_A": 2.3,                     # 1.8 ≤ d < 2.3 이면 그 O 는 미분류
    "g1_frac": "ceil(5M/6)",             # 가족마다 성공 ≥ ceil(5M/6) (M = 그 가족 어닐 계획 수)
    "g3_rule": "changed / n_success > 1/3",  # 분모 = 그 가족 성공 수 · 바뀜 = 끝 꼴 ≠ 시작 가족 (섞임 · 미분류 포함)
    "margin_uma_eV": 0.20,               # 승자–차저 (이상이면 승자)
    "pair_min": 3,                       # 공통 성공 짝이 이보다 적으면 짝 서술 보류
    "pair_frac": 5 / 6,                  # 같은 부호 비율 ≥ 5/6 이면 '짝으로도 같은 방향'
    "pilot_times_ps": [20, 50, 100],     # 파일럿 런 길이 = 마지막 값 (100 ps)
    "pilot_spread_eV": 0.05,             # max − min ≤ 0.05 (/B₂O₃) · 끝 꼴 같음 → 20 ps
    "margin_dft_eV": 0.10,
    "B_range_GPa": [21.7, 32.5],
    "eos_P_max_GPa": 2.0,
    # ── DW P1-1 · P1-2: 단계 설정 — 결과 기록 정체성 (run_anneal identity) 과 대조 (카드 6_거름 · 7_어닐 · 실행기 기본값)
    "model": "uma-s-1p1/omat",
    "relax_fmax": 0.05,
    "cell_relax": True,
    "relax_steps": 1500,
    "dt_fs": 2.0,
    "friction": 0.01,
    "anneal_T_K": 500.0,
}
FAM_ORDER = ["F_B", "F_P", "F_free"]
SNAP_TOL_A = 1e-6                        # 스냅숏 파일 ↔ 궤적 프레임 좌표 · 셀 허용 차 (xyz 는 1e-8 Å 자리까지 쓴다)
_SETTINGS = ("model", "relax_fmax", "cell_relax", "relax_steps")


# ───────────────────────── 끝 꼴 ─────────────────────────
def classify_o(atoms, r_bond=None, r_grey=None):
    """O 마다 'B' · 'P' · 'free' · 'bridge' (둘 이상 결합) · 'unclassified' (가장 가까운 B/P 가 회색 띠)."""
    r_bond = CONTRACT["r_bond_A"] if r_bond is None else r_bond
    r_grey = CONTRACT["r_grey_A"] if r_grey is None else r_grey
    sy = np.array(atoms.get_chemical_symbols())
    iO = np.nonzero(sy == "O")[0]
    out = []
    cen = {e: atoms.positions[sy == e] for e in ("B", "P")}
    for i in iO:
        nb = {}
        dmin = np.inf
        for e, X in cen.items():
            if len(X):
                d = _EN.mic_dists(atoms.positions[i][None], X, atoms.cell.array)[0]
                nb[e] = int((d < r_bond).sum())
                dmin = min(dmin, float(d.min()))
            else:
                nb[e] = 0
        nbond = nb["B"] + nb["P"]
        if nbond >= 2:
            out.append("bridge")
        elif nbond == 1:
            out.append("B" if nb["B"] else "P")
        elif dmin < r_grey:
            out.append("unclassified")
        else:
            out.append("free")
    return out


def end_motif(atoms):
    """구조의 끝 꼴: 모든 O 가 B → F_B · P → F_P · free → F_free · 미분류 O 하나라도 → unclassified · 그 밖 → mixed.

    기하가 유효하지 않으면 (NaN · inf · 특이 셀) 분류하지 않고 'invalid' (DW P2 — 옛 판은 NaN 거리를 '자유' 로 셌다).
    """
    if _RA.geometry_problems(atoms):
        return "invalid"
    c = classify_o(atoms)
    if not c:
        return "unclassified"
    if "unclassified" in c:
        return "unclassified"
    s = set(c)
    if s == {"B"}:
        return "F_B"
    if s == {"P"}:
        return "F_P"
    if s == {"free"}:
        return "F_free"
    return "mixed"


# ───────────────────────── 공통: 해시 · 묶인 입력 · 다시 내기 ─────────────────────────
def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _norm(x):
    return json.loads(json.dumps(x, sort_keys=True, ensure_ascii=False, default=str))


def _feq(a, b, tol=1e-9):
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def _dump(obj, path):
    """JSON 으로 쓴다 — inputs 의 경로는 출력 파일 폴더 기준 상대경로로 (나무째 옮겨도 다시 대조된다)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    o = json.loads(json.dumps(obj, ensure_ascii=False, default=str))
    for v in (o.get("inputs") or {}).values():
        if isinstance(v, dict) and v.get("path"):
            v["path"] = os.path.relpath(Path(v["path"]).resolve(), path.resolve().parent)
    path.write_text(json.dumps(o, ensure_ascii=False, indent=1) + "\n")
    return path


def _input(obj, key, base):
    """묶인 입력 하나 → 절대 경로 (파일이 있고 sha256 이 기록과 같아야 한다)."""
    e = (obj.get("inputs") or {}).get(key)
    if not e or not e.get("path") or not e.get("sha256"):
        raise SystemExit(f"⛔ 묶인 입력 '{key}' 기록이 없다 — 판독하지 않는다")
    p = (Path(base) / e["path"]).resolve()
    if not p.is_file():
        raise SystemExit(f"⛔ 묶인 입력 '{key}' 파일이 없다 ({p})")
    if _sha(p) != e["sha256"]:
        raise SystemExit(f"⛔ 묶인 입력 '{key}' 가 기록 뒤 바뀌었다 (sha256 불일치 · {p.name})")
    return p


def _core(obj):
    """다시 낸 판정과 견줄 몸통 — 입력은 sha256 만 (경로는 기록 위치에 따라 다르다)."""
    o = _norm(obj)
    ins = o.pop("inputs", {}) or {}
    o["inputs_sha256"] = {k: (v or {}).get("sha256") for k, v in ins.items()}
    return o


# ───────────────────────── 입력 ─────────────────────────
def manifest_plan(gen_dir):
    """생성기 출력 → {manifest · manifest_sha256 · structures {이름: {rank · family · file · sha256}}} (manifest 검증이 깨끗해야)."""
    gen_dir = Path(gen_dir)
    prob = _EN.verify_manifest(gen_dir)
    if prob:
        raise SystemExit(f"⛔ 생성기 manifest 검증 실패 ({len(prob)} 건 · 예 {prob[0]}) — 판독하지 않는다")
    mp = gen_dir / "manifest.json"
    m = json.loads(mp.read_text())
    st = {}
    for b in m["bases"]:
        for motif, e in b["motifs"].items():
            n = Path(e["file"]).stem
            if n in st:
                raise SystemExit(f"⛔ manifest 에 같은 구조 이름 {n} 이 둘 — 결과 기록을 이름으로 묶을 수 없다")
            st[n] = {"rank": int(b["rank"]), "family": CONTRACT["families"][motif],
                     "file": e["file"], "sha256": e["sha256"]}
    return {"manifest": str(mp.resolve()), "manifest_sha256": _sha(mp), "structures": st}


def load_records(results_json):
    """anneal_results.json → {path · sha256 · records {이름: dict(ok · status · E · atoms · why · vo · identity · identity_sha · outputs)}}.

    성공 (ok) = converged · verify_outputs 통과 · 유한 에너지. identity 는 없으면 None 그대로 둔다
    (빈 dict 로 바꾸지 않는다 — DW P1-1: 옛 판은 identity 없는 기록을 단계 검사 없이 통과시켰다).
    """
    p = Path(results_json)
    raw = p.read_bytes()
    res = json.loads(raw).get("results", [])
    out = {}
    for r in res:
        n = r.get("name")
        if n in out:
            raise SystemExit(f"⛔ 결과에 같은 이름 {n} 이 둘 — 섞인 기록 · 판독하지 않는다")
        st = r.get("status")
        vo = _RA.verify_outputs(r, p.parent) if st in ("converged", "unconverged") else []
        why = ([] if st == "converged" else [f"상태 {st}"]) + vo
        try:
            E = float(r.get("E_post_relax"))
        except (TypeError, ValueError):
            E = None
        if E is None or not math.isfinite(E):
            why.append("에너지 없음 · 유한 아님")
            E = None
        atoms = None
        if not vo and st in ("converged", "unconverged"):
            atoms = read(str(p.parent / r["outputs"]["post_relax"]["rel"]))
        out[n] = {"ok": not why, "status": st, "E": E, "atoms": atoms, "why": why, "vo": vo,
                  "identity": r.get("identity"), "identity_sha": r.get("identity_sha"),
                  "outputs": r.get("outputs") or {}}
    return {"path": str(p.resolve()), "sha256": hashlib.sha256(raw).hexdigest(), "records": out}


def identity_problems(n, r, *, stage, input_sha, time_ps=None, T=None):
    """기록 하나가 계획한 시작 파일 · 단계 · 설정의 결과인가 → 문제 목록 (DW P1-1)."""
    idn = r.get("identity")
    if not idn:
        return [f"{n}: 정체성 (identity) 없음 — 어느 입력 · 설정의 결과인지 묶을 수 없다"]
    p = []
    if r.get("identity_sha") != _RA.identity_sha(idn):
        p.append(f"{n}: identity_sha 가 identity 와 안 맞는다 (기록이 바뀌었다)")
    if idn.get("stage") != stage:
        p.append(f"{n}: 단계 {idn.get('stage')} ≠ {stage}")
    if idn.get("input_file_sha256") != input_sha:
        p.append(f"{n}: 시작 파일이 계획과 다르다 (입력 sha256 {str(idn.get('input_file_sha256'))[:12]}… ≠ "
                 f"계획 {str(input_sha)[:12]}…)")
    for k in _SETTINGS:
        want, got = CONTRACT[k], idn.get(k)
        if not (_feq(got, want) if isinstance(want, float) else got == want):
            p.append(f"{n}: {k} {got} ≠ 카드 {want}")
    if stage == "anneal_relax":
        for k, want in (("time_ps", time_ps), ("temperature_K", T), ("dt_fs", CONTRACT["dt_fs"]),
                        ("friction", CONTRACT["friction"])):
            if not _feq(idn.get(k), want):
                p.append(f"{n}: {k} {idn.get(k)} ≠ {want}")
    elif not _feq(idn.get("time_ps"), 0.0):
        p.append(f"{n}: 이완만인데 time_ps {idn.get('time_ps')}")
    return p


# ───────────────────────── 6 단계 거름 ─────────────────────────
def screen_verdict(gen_dir, results_json, k_f=None):
    """6 단계 판정 (완결 · 미완료 · 보류) — 완결일 때만 합집합 · 파일럿 · 8 단계 계획을 낸다."""
    k_f = CONTRACT["k_f"] if k_f is None else int(k_f)
    plan = manifest_plan(gen_dir)
    S = plan["structures"]
    R = load_records(results_json)
    recs = R["records"]
    extra = sorted(set(recs) - set(S))
    if extra:
        raise SystemExit(f"⛔ 거름 결과에 manifest 에 없는 기록 {len(extra)} 건 (예 {extra[:2]}) — 섞인 폴더 · 판독하지 않는다")
    bad = [q for n in sorted(recs)
           for q in identity_problems(n, recs[n], stage="relax_only", input_sha=S[n]["sha256"])]
    if bad:
        raise SystemExit(f"⛔ 거름 기록 결속 실패 {len(bad)} 건 (예 {bad[0]}) — 판독하지 않는다")
    missing = sorted(set(S) - set(recs))
    fam, failed = {F: [] for F in FAM_ORDER}, []
    for n in sorted(recs):
        s, r = S[n], recs[n]
        if r["ok"]:
            fam[s["family"]].append((r["E"], s["rank"], n))
        else:
            failed.append({"name": n, "family": s["family"], "rank": s["rank"], "why": r["why"][:3]})
    for F in FAM_ORDER:
        fam[F].sort()
    v = {"kind": "b2o3_bo_screen_verdict/v1", "k_f": k_f,
         "inputs": {"gen_manifest": {"path": plan["manifest"], "sha256": plan["manifest_sha256"]},
                    "screen_results": {"path": R["path"], "sha256": R["sha256"]}},
         "expected": len(S), "n_records": len(recs), "missing": missing, "failed": failed,
         "n_success_by_family": {F: len(fam[F]) for F in FAM_ORDER},
         "top_bases_by_family": None, "union_bases": None, "M": None, "pilot": None, "plan_anneal": None}
    if missing:
        v.update(status="incomplete",
                 decision=f"거름 미완료 — 누락 {len(missing)} 건 (실패 {len(failed)} 건과 다르다) · 합집합 · 파일럿을 내지 않는다")
        return v
    short = [F for F in FAM_ORDER if len(fam[F]) < k_f]
    if short:
        v.update(status="hold",
                 decision=f"거름 보류 — 성공 구조가 k_f {k_f} 보다 적은 가족 {short} (있는 것만 넣지 않는다 · DW 제안)")
        return v
    top = {F: [x[1] for x in fam[F][:k_f]] for F in FAM_ORDER}
    union = sorted({b for F in FAM_ORDER for b in top[F]})
    by = {(s["rank"], s["family"]): n for n, s in S.items()}

    def start(n):
        r = recs[n]
        if not r["ok"]:
            return None
        e = r["outputs"]["post_relax"]
        return {"rel": e["rel"], "sha256": e["sha256"]}

    plan_anneal = []
    for b in union:
        for F in FAM_ORDER:
            n = by[(b, F)]
            e = {"name": n, "rank": b, "family": F, "start": start(n)}
            if e["start"] is None:
                e["⚠"] = "6 단계 실패 — 시작 구조 없음 · 8 단계에서 돌리지 않고 실패로 센다 (G1 분모에 남는다)"
            plan_anneal.append(e)
    E0, r0, n0 = min(x for F in FAM_ORDER for x in fam[F])
    n_ns = sum(e["start"] is None for e in plan_anneal)
    v.update(status="complete", top_bases_by_family=top, union_bases=union, M=len(union),
             pilot={"name": n0, "rank": r0, "family": S[n0]["family"], "E_screen": E0, "start": start(n0)},
             plan_anneal=plan_anneal,
             decision=f"거름 완결 — 합집합 M = {len(union)} · 8 단계 계획 {len(plan_anneal)} (시작 없음 {n_ns}) · 파일럿 {n0}")
    return v


def verify_screen_verdict(vpath, k_f=None):
    """거름 판정 파일 → 묶인 입력 (manifest · 결과) 이 그대로이고, 거기서 다시 낸 판정이 파일과 같아야 한다 → 다시 낸 판정."""
    vpath = Path(vpath)
    v = json.loads(vpath.read_text())
    if v.get("kind") != "b2o3_bo_screen_verdict/v1":
        raise SystemExit(f"⛔ {vpath.name} 는 거름 판정 파일이 아니다")
    want_k = CONTRACT["k_f"] if k_f is None else int(k_f)
    if v.get("k_f") != want_k:
        raise SystemExit(f"⛔ 거름 판정 k_f {v.get('k_f')} ≠ 카드 {want_k}")
    base = vpath.resolve().parent
    gm = _input(v, "gen_manifest", base)
    sr = _input(v, "screen_results", base)
    again = screen_verdict(gm.parent, sr, k_f=want_k)
    if _core(again) != _core(v):
        raise SystemExit(f"⛔ 거름 판정 {vpath.name} 이 묶인 입력에서 다시 낸 판정과 다르다 — 바뀐 판정은 쓰지 않는다")
    return again


def write_plan_manifests(v, plan_dir):
    """실행기 (run_uma_kgy.sh CAND) 용 시작 파일 manifest 둘 — plan_dir/pilot · plan_dir/anneal (files {상대경로: {sha256 …}})."""
    if v.get("status") != "complete":
        raise SystemExit("⛔ 완결 판정에서만 시작 파일 manifest 를 쓴다")
    res_dir = Path(v["inputs"]["screen_results"]["path"]).resolve().parent
    out = {}
    for stage, label, entries, note in (
            ("pilot", "7_pilot_continuous", [v["pilot"]],
             "TIME_PS = 파일럿 길이 (100) · TEMP 500 · N_EXPECT 1 — 결과는 extract 로"),
            ("anneal", "8_anneal_t_a", [e for e in v["plan_anneal"] if e["start"]],
             "TIME_PS = 파일럿 영수증의 t_a · TEMP 500 · N_EXPECT = n — 새 출력 폴더 (파일럿 런과 섞지 않는다)")):
        d = Path(plan_dir) / stage
        d.mkdir(parents=True, exist_ok=True)
        files = {}
        for e in entries:
            f = (res_dir / e["start"]["rel"]).resolve()
            files[os.path.relpath(f, d.resolve())] = {"sha256": e["start"]["sha256"], "name": e["name"],
                                                      "family": e["family"], "rank": e["rank"]}
        (d / "manifest.json").write_text(json.dumps(
            {"schema": "b2o3_bo_plan/v1", "stage": label, "n": len(files), "실행기": note,
             "screen_results_sha256": v["inputs"]["screen_results"]["sha256"], "files": files},
            ensure_ascii=False, indent=1) + "\n")
        out[stage] = len(files)
    return out


# ───────────────────────── 7 단계 파일럿 ─────────────────────────
def _pilot_run_record(pv, R, t_len):
    """파일럿 런 기록 (구조 하나) 결속 → (기록, md_traj 기록). 저장 간격 · dt · 프레임 수는 여기서만 온다 (DW P1-2)."""
    recs = R["records"]
    if set(recs) != {pv["name"]}:
        raise SystemExit(f"⛔ 파일럿 런 결과는 파일럿 구조 {pv['name']} 하나여야 한다 — {sorted(recs)[:3]}")
    r = recs[pv["name"]]
    prob = identity_problems(pv["name"], r, stage="anneal_relax", input_sha=pv["start"]["sha256"],
                             time_ps=float(t_len), T=CONTRACT["anneal_T_K"])
    if r["status"] not in ("converged", "unconverged"):
        prob.append(f"파일럿 런 상태 {r['status']}")
    prob += r["vo"]
    mt = r["outputs"].get("md_traj")
    if not mt:
        prob.append("파일럿 런 기록에 md_traj 가 없다 (궤적 · 저장 간격을 묶을 수 없다 — DW 이전 판 run_anneal)")
    if prob:
        raise SystemExit(f"⛔ 파일럿 런 결속 실패 ({prob[0]}) — 스냅숏을 믿지 않는다")
    return r, mt


def _frame_index(t, mt):
    step_ps = float(mt["dt_fs"]) * int(mt["log_every_steps"]) / 1000.0
    k = float(t) / step_ps
    if abs(k - round(k)) > 1e-9:
        raise SystemExit(f"⛔ {t} ps 가 저장 간격 {step_ps} ps 의 배수가 아니다 (런 기록의 dt · 저장 간격)")
    k = int(round(k))
    if k >= int(mt["n_frames"]):
        raise SystemExit(f"⛔ {t} ps 프레임 {k} 가 궤적에 없다 (프레임 {mt['n_frames']} 개) — 연속 궤적이 짧다")
    return k


def _same_geometry(a, b, tol=SNAP_TOL_A):
    if a.get_chemical_symbols() != b.get_chemical_symbols() or list(a.pbc) != list(b.pbc):
        return False
    return (float(np.abs(a.get_positions() - b.get_positions()).max()) <= tol
            and float(np.abs(a.cell.array - b.cell.array).max()) <= tol)


def extract_pilot(vpath, pilot_results, out_dir, k_f=None):
    """거름 판정 + 파일럿 런 기록 → 20 · 50 · 100 ps 스냅숏 xyz + 출처 JSON + 실행기용 manifest → (출처 경로, 출처)."""
    from ase.io.trajectory import Trajectory
    times = list(CONTRACT["pilot_times_ps"])
    v = verify_screen_verdict(vpath, k_f)
    if v["status"] != "complete":
        raise SystemExit(f"⛔ 거름 판정이 완결이 아니다 ({v['status']}) — 파일럿을 시작하지 않는다")
    pv = v["pilot"]
    R = load_records(pilot_results)
    r, mt = _pilot_run_record(pv, R, max(times))
    traj = Path(R["path"]).parent / mt["rel"]
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    snaps = {}
    with Trajectory(str(traj)) as T:
        for t in times:
            k = _frame_index(t, mt)
            fr = T[k]
            a = Atoms(fr.get_chemical_symbols(), positions=fr.get_positions(), cell=fr.cell.array, pbc=fr.pbc)
            f = out_dir / f"{pv['name']}_t{int(t):03d}.xyz"
            write(str(f), a)
            snaps[str(int(t))] = {"frame": k, "time_ps": k * float(mt["dt_fs"]) * int(mt["log_every_steps"]) / 1000.0,
                                  "file": f.name, "sha256": _sha(f)}
    x = {"kind": "b2o3_bo_pilot_snapshots/v1",
         "inputs": {"screen_verdict": {"path": str(Path(vpath).resolve()), "sha256": _sha(vpath)},
                    "pilot_results": {"path": R["path"], "sha256": R["sha256"]}},
         "pilot_name": pv["name"], "pilot_identity_sha": r["identity_sha"],
         "traj": {k: mt[k] for k in ("rel", "sha256", "dt_fs", "log_every_steps", "n_frames")},
         "snapshots": snaps}
    xp = _dump(x, out_dir / f"{pv['name']}_snapshots.json")
    (out_dir / "manifest.json").write_text(json.dumps(
        {"schema": "b2o3_bo_plan/v1", "stage": "7_pilot_snapshot_relax", "n": len(snaps),
         "실행기": "TIME_PS 0 (이완만) · N_EXPECT 3 · 새 출력 폴더",
         "files": {s["file"]: {"sha256": s["sha256"], "name": Path(s["file"]).stem, "time_ps": int(t)}
                   for t, s in snaps.items()}}, ensure_ascii=False, indent=1) + "\n")
    return xp, x


def pilot_receipt(xpath, relax_results, k_f=None):
    """출처 (다시 대조) + 세 스냅숏 이완 결과 → 파일럿 영수증 (t_a 또는 '파일럿 미완료')."""
    from ase.io.trajectory import Trajectory
    times = list(CONTRACT["pilot_times_ps"])
    xpath = Path(xpath)
    x = json.loads(xpath.read_text())
    if x.get("kind") != "b2o3_bo_pilot_snapshots/v1":
        raise SystemExit(f"⛔ {xpath.name} 는 파일럿 스냅숏 출처가 아니다")
    base = xpath.resolve().parent
    vp = _input(x, "screen_verdict", base)
    pr = _input(x, "pilot_results", base)
    v = verify_screen_verdict(vp, k_f)
    if v["status"] != "complete":
        raise SystemExit("⛔ 거름 판정이 완결이 아니다 — 파일럿 판독을 하지 않는다")
    if x.get("pilot_name") != v["pilot"]["name"]:
        raise SystemExit(f"⛔ 출처의 파일럿 구조 {x.get('pilot_name')} ≠ 거름 판정의 {v['pilot']['name']}")
    R = load_records(pr)
    r, mt = _pilot_run_record(v["pilot"], R, max(times))
    if r["identity_sha"] != x.get("pilot_identity_sha"):
        raise SystemExit("⛔ 출처가 가리키는 파일럿 런이 지금 기록과 다르다 (identity_sha)")
    xt = x.get("traj") or {}
    for k in ("rel", "sha256", "dt_fs", "log_every_steps", "n_frames"):
        if xt.get(k) != mt.get(k):
            raise SystemExit(f"⛔ 출처의 궤적 {k} ({xt.get(k)}) 가 파일럿 런 기록 ({mt.get(k)}) 과 다르다 — 스냅숏을 믿지 않는다")
    snaps = x.get("snapshots") or {}
    if sorted(int(t) for t in snaps) != sorted(times):
        raise SystemExit(f"⛔ 스냅숏 시각 {sorted(snaps)} ≠ {times}")
    traj = Path(R["path"]).parent / mt["rel"]
    with Trajectory(str(traj)) as T:
        for t in times:
            s = snaps[str(t)]
            k = _frame_index(t, mt)
            if s.get("frame") != k:
                raise SystemExit(f"⛔ {t} ps 스냅숏 프레임 {s.get('frame')} ≠ 런 기록 시간축의 {k}")
            f = base / s["file"]
            if not f.is_file() or _sha(f) != s.get("sha256"):
                raise SystemExit(f"⛔ {t} ps 스냅숏 파일이 없거나 출처 기록 뒤 바뀌었다 ({s.get('file')})")
            if not _same_geometry(T[k], read(str(f))):
                raise SystemExit(f"⛔ {t} ps 스냅숏이 궤적 프레임 {k} 와 다르다 (좌표 · 셀 · 원소)")
    RR = load_records(relax_results)
    recs = RR["records"]
    want = {Path(snaps[str(t)]["file"]).stem: t for t in times}
    extra = sorted(set(recs) - set(want))
    if extra:
        raise SystemExit(f"⛔ 스냅숏 이완 결과에 스냅숏이 아닌 기록 {extra[:2]} — 섞인 폴더 · 판독하지 않는다")
    why, E, mot = [], {}, {}
    for n, t in want.items():
        r_ = recs.get(n)
        if r_ is None:
            why.append(f"{t} ps 끝점 없음 (누락)")
            continue
        ip = identity_problems(n, r_, stage="relax_only", input_sha=snaps[str(t)]["sha256"])
        if ip:
            why += [f"{t} ps: {q}" for q in ip]
            continue
        if not r_["ok"]:
            why.append(f"{t} ps: {r_['why'][:1]}")
            continue
        E[str(t)] = r_["E"] / CONTRACT["unit_B2O3"]
        mot[str(t)] = end_motif(r_["atoms"])
        if mot[str(t)] in ("unclassified", "invalid"):
            why.append(f"{t} ps: 끝 꼴 {mot[str(t)]}")
    rc = {"kind": "b2o3_bo_pilot_receipt/v1",
          "inputs": {"snapshots": {"path": str(xpath.resolve()), "sha256": _sha(xpath)},
                     "relax_results": {"path": RR["path"], "sha256": RR["sha256"]},
                     "screen_verdict": {"path": str(vp), "sha256": _sha(vp)}},
          "pilot_name": x["pilot_name"], "traj_sha256": mt["sha256"],
          "frames": {str(t): snaps[str(t)]["frame"] for t in times}, "E": E, "end_motif": mot}
    if why:
        rc.update(decision="파일럿 미완료", t_a_ps=None, why=why)
        return rc
    spread = max(E.values()) - min(E.values())
    same = len(set(mot.values())) == 1
    ta = 20 if (spread <= CONTRACT["pilot_spread_eV"] + 1e-12 and same) else 100
    rc.update(decision=f"t_a = {ta} ps", t_a_ps=ta, spread_eV=spread, same_end_motif=same,
              **{"⚠": "운영 규칙 (길이 고르기) — 수렴 증거가 아니다 · 파일럿의 선택된 t_a 보다 긴 결과는 다른 배치와 견주지 않는다"})
    return rc


def verify_pilot_receipt(rpath, k_f=None):
    """파일럿 영수증 → 묶인 입력이 그대로이고 거기서 다시 낸 영수증이 파일과 같아야 한다 → 다시 낸 영수증."""
    rpath = Path(rpath)
    rc = json.loads(rpath.read_text())
    if rc.get("kind") != "b2o3_bo_pilot_receipt/v1":
        raise SystemExit(f"⛔ {rpath.name} 는 파일럿 영수증이 아니다")
    base = rpath.resolve().parent
    xp = _input(rc, "snapshots", base)
    rr = _input(rc, "relax_results", base)
    _input(rc, "screen_verdict", base)
    again = pilot_receipt(xp, rr, k_f)
    if _core(again) != _core(rc):
        raise SystemExit(f"⛔ 파일럿 영수증 {rpath.name} 이 묶인 입력에서 다시 낸 영수증과 다르다 — 바뀐 영수증은 쓰지 않는다")
    return again


# ───────────────────────── 8 단계 어닐 판독 ─────────────────────────
def anneal_judge(plan, recs, margin=None):
    """8 단계 계획 [{name · rank · family · start}] + (결속을 통과한) 기록 → 가족 판독.

    시작 없는 항목 (6 단계 실패) 은 실패로 센다 · 시작 있는 항목의 기록이 없으면 판독하지 않는다 (누락 ≠ 실패).
    """
    margin = CONTRACT["margin_uma_eV"] if margin is None else margin
    unit = CONTRACT["unit_B2O3"]
    miss = [e["name"] for e in plan if e["start"] and e["name"] not in recs]
    if miss:
        raise SystemExit(f"⛔ 어닐 기록 누락 {len(miss)} 건 (예 {miss[:2]}) — 누락은 실패가 아니다 · 다 돌린 뒤 판독한다")
    fams, holds = {}, []
    for F in FAM_ORDER:
        P = sorted((e for e in plan if e["family"] == F), key=lambda e: e["rank"])
        M = len(P)
        succ, changed, failed = [], [], []
        for e in P:
            r = recs.get(e["name"]) if e["start"] else None
            if r is None or not r["ok"]:
                failed.append({"name": e["name"],
                               "why": (["시작 구조 없음 (6 단계 실패)"] if not e["start"] else r["why"][:2])})
                continue
            em = end_motif(r["atoms"])
            succ.append({"rank": e["rank"], "name": e["name"], "E": r["E"] / unit, "end_motif": em})
            if em != F:
                changed.append(e["name"])
        need = math.ceil(5 * M / 6) if M else 0
        g1 = M > 0 and len(succ) >= need
        g3_mixed = bool(succ) and (len(changed) / len(succ) > 1 / 3)
        best = min(succ, key=lambda x: (x["E"], x["rank"])) if succ else None
        fams[F] = {"M": M, "n_success": len(succ), "need_G1": need, "G1": g1, "failed": failed,
                   "n_end_changed": len(changed), "G3_mixed": g3_mixed,
                   "G3": f"{len(changed)}/{len(succ)}" if succ else "—",
                   "min": best, "success": succ}
        if not g1:
            holds.append(f"{F}: G1 실패 (성공 {len(succ)} < {need} · 탈락)")
        if best is None:
            holds.append(f"{F}: 성공 구조 없음 (가족 결측)")
        elif best["end_motif"] in ("unclassified", "invalid"):
            holds.append(f"{F}: 가족 최저 구조의 끝 꼴 {best['end_motif']}")
    # G2 — 조성 전부 같음
    comps = {json.dumps(_RA._composition(recs[s["name"]]["atoms"]), sort_keys=True)
             for F in FAM_ORDER for s in fams[F]["success"]}
    g2 = len(comps) <= 1
    if not g2:
        holds.append(f"G2 실패: 조성 {len(comps)} 가지")
    # 공통 성공 짝
    by = {F: {s["rank"]: s["E"] for s in fams[F]["success"]} for F in FAM_ORDER}
    common = sorted(set.intersection(*[set(by[F]) for F in FAM_ORDER])) if all(by.values()) else []
    out = {"contract": CONTRACT, "families": {F: {k: v for k, v in d.items() if k != "success"}
                                              for F, d in fams.items()},
           "G2_same_composition": g2, "common_success_pairs": common, "n_pairs": len(common)}
    if holds:
        out.update({"winner": None, "decision": "승자 보류", "hold_reasons": holds})
        return out
    order = sorted(FAM_ORDER, key=lambda F: fams[F]["min"]["E"])
    gap = fams[order[1]]["min"]["E"] - fams[order[0]]["min"]["E"]
    out["order"] = order
    out["winner_runner_up_gap_eV"] = gap
    if gap >= margin - 1e-12:
        out.update({"winner": order[0], "decision": f"승자 {order[0]} (차저 {order[1]} 와 {gap:.3f} ≥ {margin})"})
    else:
        out.update({"winner": None, "decision": f"UMA 로는 못 가른다 (승자–차저 {gap:.3f} < {margin})"})
    # 짝 — 승자 (또는 최저) 와 차저 사이 같은 부호
    a, b = order[0], order[1]
    if len(common) < CONTRACT["pair_min"]:
        out["pairs"] = f"짝 서술 보류 (공통 성공 짝 {len(common)} < {CONTRACT['pair_min']})"
    else:
        sgn = [np.sign(by[a][k] - by[b][k]) for k in common]
        same = sum(1 for s in sgn if s < 0)
        out["pairs"] = {"n": len(common), "same_sign_as_order": same,
                        "같은_방향": same >= math.ceil(CONTRACT["pair_frac"] * len(common) - 1e-12)}
    out["G3_mixed_families"] = [F for F in FAM_ORDER if fams[F]["G3_mixed"]]
    return out


def anneal_readout(vpath, rpath, results_json, margin=None, k_f=None):
    """8 단계 — 거름 판정 · 파일럿 영수증 (같은 판정) · 어닐 결과를 묶어 판독한다 (DW P1-1)."""
    v = verify_screen_verdict(vpath, k_f)
    if v["status"] != "complete":
        raise SystemExit(f"⛔ 거름 판정이 완결이 아니다 ({v['status']}) — 어닐 판독을 하지 않는다")
    rc = verify_pilot_receipt(rpath, k_f)
    if rc["inputs"]["screen_verdict"]["sha256"] != _sha(vpath):
        raise SystemExit("⛔ 파일럿 영수증이 다른 거름 판정에서 나왔다 — 판독하지 않는다")
    if rc.get("t_a_ps") is None:
        raise SystemExit("⛔ 파일럿 미완료 — t_a 가 없어 어닐 판독을 하지 않는다")
    t_a = float(rc["t_a_ps"])
    R = load_records(results_json)
    recs = R["records"]
    plan = v["plan_anneal"]
    runnable = {e["name"]: e for e in plan if e["start"]}
    extra = sorted(set(recs) - set(runnable))
    if extra:
        raise SystemExit(f"⛔ 어닐 결과에 계획 (시작 파일이 있는 항목) 밖 기록 {len(extra)} 건 (예 {extra[:2]}) — 판독하지 않는다")
    missing = sorted(set(runnable) - set(recs))
    if missing:
        raise SystemExit(f"⛔ 어닐 결과 누락 {len(missing)} 건 (예 {missing[:2]}) — 누락은 실패가 아니다 · 다 돌린 뒤 판독한다")
    bad = [q for n in sorted(recs)
           for q in identity_problems(n, recs[n], stage="anneal_relax", input_sha=runnable[n]["start"]["sha256"],
                                      time_ps=t_a, T=CONTRACT["anneal_T_K"])]
    if bad:
        raise SystemExit(f"⛔ 어닐 기록 결속 실패 {len(bad)} 건 (예 {bad[0]}) — 판독하지 않는다")
    out = anneal_judge(plan, recs, margin)
    return {"kind": "b2o3_bo_anneal_readout/v1",
            "inputs": {"screen_verdict": {"path": str(Path(vpath).resolve()), "sha256": _sha(vpath)},
                       "pilot_receipt": {"path": str(Path(rpath).resolve()), "sha256": _sha(rpath)},
                       "anneal_results": {"path": R["path"], "sha256": R["sha256"]}},
            "t_a_ps": rc["t_a_ps"], "M": v["M"], "plan_n": len(plan),
            "plan_no_start": [e["name"] for e in plan if not e["start"]], **out}


# ───────────────────────── 9 단계 EOS 생략 조건 ─────────────────────────
GPA_A3_EV = 1e9 * 1e-30 / 1.602176634e-19        # GPa·Å³ → eV


def eos_correction(P_GPa, V_A3, B_GPa):
    return -(P_GPa ** 2) * V_A3 * GPA_A3_EV / (2.0 * B_GPa)


def eos_robust(fam, margin=None, B_range=None, P_max=None):
    """fam = {가족: (E_eV, P_GPa, V_A3)} → 기준 (보정 전) 의 **전체 순서**와 **승자–차저 0.10 판정**이 가족마다 B 를
    **독립으로** 범위 끝에 둔 모든 조합에서 그대로인가 (DW P1-3 — 옛 판은 조합끼리만 견줘서 모든 조합이 같은 쪽으로
    뒤집히면 '그대로' 로 셌고, 아래 순위가 바뀌는 것은 보지 않았다).

    보정은 B 에 단조라 끝점 조합 (2^n) 이면 충분하다. |P| > P_max 인 가족이 있으면 생략 불가.
    """
    import itertools
    margin = CONTRACT["margin_dft_eV"] if margin is None else margin
    B_range = CONTRACT["B_range_GPa"] if B_range is None else B_range
    P_max = CONTRACT["eos_P_max_GPa"] if P_max is None else P_max
    names = sorted(fam)

    def verdict(Ec):
        order = sorted(names, key=lambda F: (Ec[F], F))
        gap = Ec[order[1]] - Ec[order[0]]
        return order, gap, (order[0], gap >= margin - 1e-12)

    b_order, b_gap, b_dec = verdict({F: fam[F][0] for F in names})
    corners = []
    for Bs in itertools.product(B_range, repeat=len(names)):
        Ec = {F: fam[F][0] + eos_correction(fam[F][1], fam[F][2], B) for F, B in zip(names, Bs)}
        order, gap, dec = verdict(Ec)
        corners.append({"B": dict(zip(names, Bs)), "order": order, "gap": gap,
                        "same_as_baseline": order == b_order and dec == b_dec})
    common = []
    for B in B_range:
        order, gap, dec = verdict({F: fam[F][0] + eos_correction(fam[F][1], fam[F][2], B) for F in names})
        common.append(order == b_order and dec == b_dec)
    p_ok = all(abs(fam[F][1]) <= P_max for F in names)
    rob = all(c["same_as_baseline"] for c in corners)
    return {"baseline_order": b_order, "baseline_gap": b_gap,
            "baseline_decision": {"lowest": b_dec[0], "gap_ge_margin": b_dec[1], "margin": margin},
            "robust_independent_B": rob, "robust_common_B": all(common),
            "pressure_ok": p_ok, "skip_eos": p_ok and rob, "corners": corners}


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    import tempfile
    from ase.io.trajectory import Trajectory
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    def raises(f, *a, **k):
        try:
            f(*a, **k)
        except SystemExit as ex:
            return str(ex) or True
        except Exception:                    # 거부가 아니라 터진 것 — 거부로 세지 않는다 (빨간불)
            return False
        return False

    def refuses(kw, f, *a, **k):
        """거부하되 **그 이유로** 거부해야 통과 (다른 데서 멈춘 것을 잡았다고 세지 않는다)."""
        m = raises(f, *a, **k)
        return isinstance(m, str) and kw in m

    def toy(kind, shift=0.0):
        """B (2,2,2) · P (8,8,8) · O 셋 · S 하나 · 12 Å 상자. kind = F_B · F_P · F_free · mixed · grey."""
        B, P = np.array([2.0, 2, 2]), np.array([8.0, 8, 8])
        dirs = np.eye(3)
        if kind == "F_B":
            O = [B + 1.45 * d for d in dirs]
        elif kind == "F_P":
            O = [P - 1.55 * d for d in dirs]
        elif kind == "F_free":
            O = [np.array([5.0, 5, 5]) + 0.8 * d for d in dirs]
        elif kind == "mixed":
            O = [B + 1.45 * dirs[0], B + 1.45 * dirs[1], P - 1.55 * dirs[2]]
        else:                                                   # grey: 한 O 가 P 에서 2.0 Å
            O = [P - 1.55 * dirs[0], P - 1.55 * dirs[1], P - 2.0 * dirs[2]]
        pos = [B, P] + O + [np.array([10.0, 2, 10]) + shift]
        return Atoms("BPO3S", positions=pos, cell=[12, 12, 12], pbc=True)

    # (1) 끝 꼴 분류
    chk([end_motif(toy(k)) for k in ("F_B", "F_P", "F_free", "mixed", "grey")] ==
        ["F_B", "F_P", "F_free", "mixed", "unclassified"],
        "끝 꼴: B · P · 자유 · 섞임 · 회색 띠 (1.8–2.3 Å) 는 미분류")
    br = toy("F_B")
    br.positions[2] = np.array([2.0, 2, 2]) + np.array([1.45, 0, 0])
    br.positions[1] = br.positions[2] + np.array([1.6, 0, 0])   # 그 O 가 B · P 둘 다에 붙음
    chk("bridge" in classify_o(br) and end_motif(br) == "mixed", "⛔음성: B · P 둘 다에 붙은 O 는 가교 → 섞임")
    nanb = toy("F_B"); nanb.positions[2, 0] = np.nan
    chk(end_motif(nanb) == "invalid", "⛔음성: NaN 좌표 구조는 분류하지 않는다 ('invalid' — DW P2 · 옛 판은 F_free)")

    def idn(input_sha, stage, time_ps=0.0, T=500.0, **over):
        d = {"input_file_sha256": input_sha, "input_struct": "x", "n_atoms": 6, "stage": stage,
             "temperature_K": float(T), "time_ps": float(time_ps), "dt_fs": 2.0, "friction": 0.01,
             "relax_steps": 1500, "relax_fmax": 0.05, "cell_relax": True, "seed": 1, "model": "uma-s-1p1/omat"}
        d.update(over)
        return d

    def put(d, n, kind, E, status, ident, traj=None, shift=0.0, sha_ok=True):
        """d 폴더에 run_anneal 꼴 기록 하나 — traj = (프레임 수, dt, 저장 간격, 걸음 수) 면 md_traj 도."""
        w = d / n
        w.mkdir(parents=True, exist_ok=True)
        a = toy(kind, shift)
        for k in ("post_md", "post_relax"):
            write(str(w / f"{k}.xyz"), a)
        if status == "failed":
            return {"name": n, "status": "failed", "error": "x", "identity": ident,
                    "identity_sha": _RA.identity_sha(ident) if ident else None}
        rec = {"name": n, "status": status, "converged": status == "converged", "E_post_relax": E,
               "identity": ident, "identity_sha": (_RA.identity_sha(ident) if (ident and sha_ok) else
                                                    ("bad" if ident else None)),
               "composition": _RA._composition(a),
               "outputs": {k: {"rel": f"{n}/{k}.xyz", "sha256": _RA._file_sha256(w / f"{k}.xyz")}
                           for k in ("post_md", "post_relax")}}
        if traj:
            nf, dt, le, ns = traj
            T_ = Trajectory(str(w / "md.traj"), "w")
            for k in range(nf):
                T_.write(toy(kind, shift=0.001 * k))
            T_.close()
            rec["outputs"]["md_traj"] = {"rel": f"{n}/md.traj", "sha256": _RA._file_sha256(w / "md.traj"),
                                         "n_frames": nf, "log_every_steps": le, "dt_fs": dt, "n_steps": ns}
        return rec

    def save(d, recs):
        d.mkdir(parents=True, exist_ok=True)
        (d / "anneal_results.json").write_text(json.dumps({"results": recs}))
        return d / "anneal_results.json"

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # ── (2) 판정 논리 (anneal_judge) — 계획 + 기록 (결속은 아래 사슬 시험에서)
        code = {"F_B": "bo4", "F_P": "distributed", "F_free": "free_s"}
        M_bases = list(range(6))
        plan6 = [{"name": f"cfg{b:04d}_O-{code[F]}", "rank": b, "family": F, "start": {"rel": "x", "sha256": "s"}}
                 for b in M_bases for F in FAM_ORDER]

        def judge_recs(sub, Eshift, status=None, motif=None):
            rr = []
            for e in plan6:
                st = (status or {}).get(e["name"], "converged")
                kd = (motif or {}).get(e["name"], e["family"])
                rr.append(put(td / sub, e["name"], kd, Eshift[e["family"]] + 0.01 * e["rank"], st,
                              idn("s", "anneal_relax", 20)))
            return load_records(save(td / sub, rr))["records"]

        r = anneal_judge(plan6, judge_recs("q6", {"F_P": 0.0, "F_B": -0.21, "F_free": -0.20}))
        chk(r["winner"] is None and "못 가른다" in r["decision"],
            f"⛔음성: 승자는 최저 대 차저 차로 — F_B −0.21 · F_free −0.20 은 0.01 차라 못 가른다 ({r['decision'][:30]})")
        r2 = anneal_judge(plan6, judge_recs("win", {"F_P": 0.0, "F_B": -0.50, "F_free": -0.20}))
        chk(r2["winner"] == "F_B" and r2["pairs"]["같은_방향"] and r2["n_pairs"] == 6,
            "[양성] 차 0.30 ≥ 0.20 → 승자 F_B · 공통 성공 짝 6 개 모두 같은 방향")
        st5 = {"cfg0005_O-bo4": "unconverged"}
        mo2 = {"cfg0001_O-bo4": "F_P", "cfg0002_O-bo4": "mixed"}
        E3 = {"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}
        r3 = anneal_judge(plan6, judge_recs("g3a", E3, st5, mo2))
        r4 = anneal_judge(plan6, judge_recs("g3b", E3, None, mo2))
        chk(r3["families"]["F_B"]["G3"] == "2/5" and r3["families"]["F_B"]["G3_mixed"]
            and r4["families"]["F_B"]["G3"] == "2/6" and not r4["families"]["F_B"]["G3_mixed"]
            and r3["families"]["F_B"]["G1"],
            "⛔음성: G3 분모 = 그 가족 성공 수 — 2/5 는 섞임 · 2/6 은 아님 (경계 '넘으면' = 엄격 >) · G1 은 5/6 통과")
        r5 = anneal_judge(plan6, judge_recs("g1", E3, {f"cfg{b:04d}_O-distributed": "failed" for b in (0, 1)}))
        chk(r5["winner"] is None and any("G1 실패" in h for h in r5["hold_reasons"]),
            "⛔음성: 가족 하나가 G1 실패 (성공 4 < 5) → 승자 보류 (탈락 가족을 빼고 고르지 않는다)")
        r6 = anneal_judge(plan6, judge_recs("miss", E3, {f"cfg{b:04d}_O-free_s": "failed" for b in M_bases}))
        chk(r6["winner"] is None and any("결측" in h for h in r6["hold_reasons"]),
            "⛔음성: 한 가족이 성공 0 (결측) → 보류")
        r7 = anneal_judge(plan6, judge_recs("grey", E3, None, {"cfg0000_O-bo4": "grey"}))
        chk(r7["winner"] is None and any("unclassified" in h for h in r7["hold_reasons"]),
            "⛔음성: 가족 최저 구조의 끝 꼴이 미분류 → 보류")
        recs_b = judge_recs("bind", E3)
        pth = td / "bind" / "anneal_results.json"
        write(str(td / "bind" / "cfg0000_O-bo4" / "post_relax.xyz"), toy("F_P"))
        rr_ = load_records(pth)["records"]
        chk(recs_b["cfg0000_O-bo4"]["ok"] and not rr_["cfg0000_O-bo4"]["ok"]
            and any("sha256" in w for w in rr_["cfg0000_O-bo4"]["why"]),
            "⛔음성: 결과 파일이 바뀐 구조는 판독에 안 쓴다 (run_anneal.verify_outputs — 결속 규칙 하나)")
        r8 = anneal_judge([e for e in plan6 if e["rank"] < 2], judge_recs("pairs", E3))
        chk(r8["winner"] == "F_B" and r8["n_pairs"] == 2 and isinstance(r8["pairs"], str) and "보류" in r8["pairs"],
            "⛔음성: 공통 성공 짝 2 < 3 → 승자는 내도 짝 서술은 보류")
        # NaN 기하 (sha 를 맞춰도) → 성공 아님 (실패로 셈 · F_free 로 세지 않는다)
        recs_n = judge_recs("nan", E3)
        pn = td / "nan" / "anneal_results.json"
        dn = json.loads(pn.read_text())
        an = toy("F_B"); an.positions[2] = [np.nan, np.nan, np.nan]
        write(str(td / "nan" / "cfg0000_O-bo4" / "post_relax.xyz"), an)
        for r_ in dn["results"]:
            if r_["name"] == "cfg0000_O-bo4":
                r_["outputs"]["post_relax"]["sha256"] = _RA._file_sha256(td / "nan" / "cfg0000_O-bo4" / "post_relax.xyz")
        pn.write_text(json.dumps(dn))
        rn = anneal_judge(plan6, load_records(pn)["records"])
        chk(recs_n["cfg0000_O-bo4"]["ok"] and rn["families"]["F_B"]["n_success"] == 5
            and rn["families"]["F_free"]["n_success"] == 6
            and any("NaN" in str(f["why"]) for f in rn["families"]["F_B"]["failed"]),
            "⛔음성: NaN 좌표 결과 (sha256 을 맞춰도) 는 실패로 센다 — F_free 로 세지 않는다 (Codex DW P2)")
        chk(refuses("누락", anneal_judge, plan6, {k: v for k, v in recs_b.items() if k != "cfg0003_O-free_s"}),
            "⛔음성: 시작 파일이 있는 계획 항목의 기록이 없으면 판독하지 않는다 (누락 ≠ 실패 · DW P1-1)")
        pl_ns = [dict(e, start=None) if e["name"] == "cfg0000_O-distributed" else e for e in plan6]
        rns = anneal_judge(pl_ns, {k: v for k, v in recs_b.items() if k != "cfg0000_O-distributed"})
        chk(rns["families"]["F_P"]["M"] == 6 and rns["families"]["F_P"]["n_success"] == 5
            and rns["families"]["F_P"]["G1"],
            "[양성] 6 단계 실패로 시작이 없는 항목은 G1 분모에 남고 실패로 센다 (6 중 5 성공 → G1 통과)")

        # ── (3) 단계 사슬 — 생성 manifest → 거름 판정 → 파일럿 런 → 스냅숏 → 영수증 → 어닐 판독 (DW P1-1 · P1-2)
        _vm = _EN.verify_manifest
        _EN.verify_manifest = lambda gd: []            # 생성기 검증은 생성기 selftest 몫 — 여기서는 판독기 결속만
        try:
            gen = td / "gen"
            (gen / "cif").mkdir(parents=True)
            NB = 8
            rank_val = {"F_B": {b: b for b in range(NB)},
                        "F_P": {b: (b - 2) % NB for b in range(NB)},
                        "F_free": {b: {1: 0, 4: 1}.get(b, 2 + b) for b in range(NB)}}
            base_E = {"F_B": -0.5, "F_P": 0.0, "F_free": -0.2}
            bases = []
            for b in range(NB):
                mot = {}
                for F in FAM_ORDER:
                    f = gen / "cif" / f"cfg{b:04d}_O-{code[F]}.xyz"
                    write(str(f), toy(F, shift=0.01 * b))
                    mot[code[F]] = {"file": str(f.relative_to(gen)), "sha256": _sha(f)}
                bases.append({"rank": b, "motifs": mot})
            (gen / "manifest.json").write_text(json.dumps({"bases": bases}))
            S = manifest_plan(gen)["structures"]

            def screen_res(sub, drop=(), fail=(), over=None, foreign=(), noid=(), badsha=(), extra=False):
                rr = []
                for n, s in sorted(S.items()):
                    if n in drop:
                        continue
                    F = s["family"]
                    E = base_E[F] + 0.01 * rank_val[F][s["rank"]]
                    ident = None if n in noid else idn("0" * 64 if n in foreign else s["sha256"], "relax_only",
                                                       **((over or {}).get(n, {})))
                    rr.append(put(td / sub, n, F, E, "failed" if n in fail else "converged", ident,
                                  sha_ok=n not in badsha))
                if extra:
                    rr.append(put(td / sub, "stranger", "F_B", -9.0, "converged", idn("1" * 64, "relax_only")))
                return save(td / sub, rr)

            K = 2
            V = screen_verdict(gen, screen_res("s_ok"), k_f=K)
            chk(V["status"] == "complete" and V["union_bases"] == [0, 1, 2, 3, 4] and V["M"] == 5
                and V["pilot"]["name"] == "cfg0000_O-bo4" and len(V["plan_anneal"]) == 15,
                "[양성] 거름 완결: 가족별 상위 2 (F_B 0,1 · F_P 2,3 · F_free 1,4) → 합집합 5 · 계획 15 · 파일럿 = 전체 최저")
            vp = _dump(V, td / "verdict.json")
            nplan = write_plan_manifests(V, td / "plan")
            pm = json.loads((td / "plan" / "anneal" / "manifest.json").read_text())
            chk(nplan == {"pilot": 1, "anneal": 15}
                and all(_sha((td / "plan" / "anneal" / k).resolve()) == e["sha256"] for k, e in pm["files"].items()),
                "[양성] 실행기용 시작 파일 manifest (파일럿 1 · 어닐 15) — 경로가 6 단계 post_relax 를 가리키고 sha256 이 맞다")
            chk(refuses("정체성", screen_verdict, gen, screen_res("s_noid", noid={"cfg0003_O-bo4"}), k_f=K),
                "⛔음성: 정체성 없는 기록이 있으면 거름 판독 거부 (Codex DW missing_identity — 옛 판: 승자 F_B)")
            chk(refuses("시작 파일이 계획과 다르다", screen_verdict, gen, screen_res("s_for", foreign={"cfg0002_O-free_s"}), k_f=K),
                "⛔음성: 같은 이름 · 다른 입력 (시작 sha256 ≠ manifest) 기록 → 거부 (Codex DW other_input_same_names)")
            chk(refuses("manifest 에 없는 기록", screen_verdict, gen, screen_res("s_ext", extra=True), k_f=K),
                "⛔음성: manifest 에 없는 기록이 섞이면 거부")
            chk(refuses("identity_sha", screen_verdict, gen, screen_res("s_bsh", badsha={"cfg0001_O-bo4"}), k_f=K),
                "⛔음성: identity_sha 가 identity 와 안 맞으면 (손으로 바뀐 기록) 거부")
            chk(refuses("relax_fmax", screen_verdict, gen,
                        screen_res("s_fmx", over={"cfg0001_O-bo4": {"relax_fmax": 0.02}}), k_f=K),
                "⛔음성: 설정 (이완 fmax 0.02 ≠ 카드 0.05) 이 다른 기록 → 거부")
            Vp = screen_verdict(gen, screen_res("s_part", drop={n for n in S if not n.startswith("cfg0000")}), k_f=K)
            chk(Vp["status"] == "incomplete" and Vp["union_bases"] is None and Vp["pilot"] is None
                and len(Vp["missing"]) == 21,
                "⛔음성: 누락 21 건 → '거름 미완료' · 합집합 · 파일럿 없음 (Codex DW screen_partial — 옛 판: 합집합 [0] · 파일럿)")
            Vh = screen_verdict(gen, screen_res("s_kf", fail={f"cfg{b:04d}_O-free_s" for b in range(1, NB)}), k_f=K)
            chk(Vh["status"] == "hold" and Vh["union_bases"] is None and len(Vh["failed"]) == 7,
                "⛔음성: 한 가족 성공 1 < k_f 2 → 거름 보류 (있는 것만 넣지 않는다 · 실패 7 건은 적는다)")
            Vf = screen_verdict(gen, screen_res("s_f0", fail={"cfg0000_O-distributed"}), k_f=K)
            chk(Vf["status"] == "complete" and any(e["start"] is None and e["name"] == "cfg0000_O-distributed"
                                                   for e in Vf["plan_anneal"]),
                "[양성] 합집합 바탕 (0) 의 F_P 가 6 단계 실패 → 그 계획 항목은 시작 없음 (8 단계 실패로 센다)")
            # 판정 파일 변조 · 입력 변조
            vt = json.loads(vp.read_text()); vt["union_bases"] = [0, 1]; vt["M"] = 2
            vtp = td / "verdict_tampered.json"; vtp.write_text(json.dumps(vt))
            chk(refuses("다시 낸 판정과 다르다", verify_screen_verdict, vtp, K),
                "⛔음성: 판정 파일의 합집합을 손으로 줄이면 다시 낸 판정과 달라 거부 (Codex DW short_union — 옛 판: 승자)")
            chk(not raises(verify_screen_verdict, vp, K), "[양성] 바뀌지 않은 판정 파일은 다시 내도 같다")

            # 파일럿 런 (100 ps · dt 2 · 500 걸음마다 → 프레임 101)
            pv = V["pilot"]
            pstart = pv["start"]["sha256"]

            def pilot_run(sub, time_ps=100.0, T=500.0, start=None, traj=(101, 2.0, 500, 50000), name=None):
                return save(td / sub, [put(td / sub, name or pv["name"], "F_B", -0.6, "converged",
                                           idn(start or pstart, "anneal_relax", time_ps, T), traj=traj)])

            pr = pilot_run("p_ok")
            xp, X = extract_pilot(vp, pr, td / "snap", k_f=K)
            chk([X["snapshots"][t]["frame"] for t in ("20", "50", "100")] == [20, 50, 100],
                "[양성] 저장 간격 · dt 는 런 기록에서 — 500 걸음 · 2 fs → 20 · 50 · 100 ps = 프레임 20 · 50 · 100")
            pr250 = pilot_run("p_250", traj=(201, 2.0, 250, 50000))
            _, X250 = extract_pilot(vp, pr250, td / "snap250", k_f=K)
            chk([X250["snapshots"][t]["frame"] for t in ("20", "50", "100")] == [40, 100, 200],
                "[양성] 같은 시각도 런 기록의 간격 (250 걸음) 이면 프레임 40 · 100 · 200 — 명령줄 간격 없음 (Codex DW wrong_cadence)")
            for label, kw, why in (("20 ps 런 (파일럿 길이 100 ≠)", {"time_ps": 20.0, "traj": (21, 2.0, 500, 10000)},
                                    "time_ps"),
                                   ("1000 K", {"T": 1000.0}, "temperature_K"),
                                   ("다른 시작 파일", {"start": "2" * 64}, "시작 파일"),
                                   ("md_traj 기록 없음", {"traj": None}, "md_traj 가 없다")):
                chk(refuses(why, extract_pilot, vp, pilot_run("p_" + str(abs(hash(label)) % 10**6), **kw),
                            td / "snap_x", k_f=K),
                    f"⛔음성: 파일럿 런이 {label} 이면 스냅숏을 꺼내지 않는다")
            pdl = json.loads(pr.read_text())
            pdl["results"][0]["outputs"]["md_traj"]["log_every_steps"] = 50
            prb = td / "p_le" / "anneal_results.json"
            (td / "p_le").mkdir()
            import shutil
            shutil.copytree(td / "p_ok" / pv["name"], td / "p_le" / pv["name"])
            prb.write_text(json.dumps(pdl))
            chk(refuses("프레임 수", extract_pilot, vp, prb, td / "snap_le", k_f=K),
                "⛔음성: 런 기록의 저장 간격을 바꾸면 (500 → 50) 프레임 수가 안 맞아 거부 (간격은 기록이 정한다)")

            def relax3(sub, Es, bad_in=None, drop=None, kinds=None):
                rr = []
                for t, E in zip((20, 50, 100), Es):
                    if t == drop:
                        continue
                    s = X["snapshots"][str(t)]
                    sha = "3" * 64 if t == bad_in else s["sha256"]
                    rr.append(put(td / sub, Path(s["file"]).stem, (kinds or {}).get(t, "F_B"), E, "converged",
                                  idn(sha, "relax_only")))
                return save(td / sub, rr)

            ra = pilot_receipt(xp, relax3("r_a", [0.0, -0.02, -0.04]), k_f=K)
            rb = pilot_receipt(xp, relax3("r_b", [0.0, -0.30, -0.02]), k_f=K)
            chk(ra["t_a_ps"] == 20 and rb["t_a_ps"] == 100,
                "⛔음성: 세 시점 0 · −0.02 · −0.04 → 20 ps · Codex 예 0 · −0.30 · −0.02 → 100 ps (옛 |E20−E100| 규칙은 20 을 골랐다)")
            rc_ = pilot_receipt(xp, relax3("r_c", [0.0, -0.01, -0.02], drop=50), k_f=K)
            rd = pilot_receipt(xp, relax3("r_d", [0.0, -0.01, -0.02], bad_in=100), k_f=K)
            re_ = pilot_receipt(xp, relax3("r_e", [0.0, -0.01, -0.02], kinds={100: "F_P"}), k_f=K)
            chk(rc_["t_a_ps"] is None and rd["t_a_ps"] is None and re_["t_a_ps"] == 100,
                "⛔음성: 끝점 누락 · 다른 입력 (스냅숏 sha 불일치) → 파일럿 미완료 · 끝 꼴이 갈리면 100 ps")
            # 출처 변조 — 궤적 sha · 프레임 번호 · 스냅숏 파일 (sha 를 맞춰도 좌표가 프레임과 다르면)
            for label, mut, why in (("궤적 sha256 을 0 으로", lambda o: o["traj"].__setitem__("sha256", "0" * 64),
                                     "궤적 sha256"),
                                    ("50 ps 프레임 번호 50 → 49", lambda o: o["snapshots"]["50"].__setitem__("frame", 49),
                                     "프레임 49"),
                                    ("저장 간격 500 → 250", lambda o: o["traj"].__setitem__("log_every_steps", 250),
                                     "궤적 log_every_steps")):
                xo = json.loads(xp.read_text()); mut(xo)
                xb = xp.with_name("bad_" + xp.name); xb.write_text(json.dumps(xo))
                chk(refuses(why, pilot_receipt, xb, relax3("r_a2", [0.0, -0.02, -0.04]), k_f=K),
                    f"⛔음성: 출처의 {label} 바꾸면 영수증을 안 낸다 (Codex DW pilot_bad_trajectory — 옛 판: t_a 100)")
            snapf = td / "snap" / X["snapshots"]["50"]["file"]
            keep = snapf.read_bytes()
            write(str(snapf), toy("F_B", shift=0.3))
            xo = json.loads(xp.read_text()); xo["snapshots"]["50"]["sha256"] = _sha(snapf)
            xb = xp.with_name("bad2_" + xp.name); xb.write_text(json.dumps(xo))
            chk(refuses("궤적 프레임", pilot_receipt, xb, relax3("r_a3", [0.0, -0.02, -0.04]), k_f=K),
                "⛔음성: 스냅숏 파일을 다른 좌표로 바꾸고 sha 를 맞춰도 궤적 프레임과 달라 거부")
            snapf.write_bytes(keep)
            R100 = pilot_receipt(xp, relax3("r_b2", [0.0, -0.30, -0.02]), k_f=K)
            rp = _dump(R100, td / "receipt.json")
            chk(not raises(verify_pilot_receipt, rp, K) and R100["t_a_ps"] == 100, "[양성] 영수증 다시 내기 = 같다 (t_a 100)")
            rt = json.loads(rp.read_text()); rt["t_a_ps"] = 20; rt["decision"] = "t_a = 20 ps"
            rtp = td / "receipt_tampered.json"; rtp.write_text(json.dumps(rt))
            chk(refuses("다시 낸 영수증과 다르다", verify_pilot_receipt, rtp, K), "⛔음성: 영수증의 t_a 를 손으로 100 → 20 바꾸면 거부")

            # 8 단계 어닐 (t_a = 100)
            def ann(sub, t=100.0, T=500.0, drop=(), extra=(), start_from=None, fail=(), eshift=None):
                rr = []
                for e in V["plan_anneal"]:
                    if e["name"] in drop:
                        continue
                    F = e["family"]
                    sha = e["start"]["sha256"] if start_from is None else S[e["name"]]["sha256"]
                    E = (eshift or base_E)[F] + 0.01 * e["rank"]
                    rr.append(put(td / sub, e["name"], F, E, "failed" if e["name"] in fail else "converged",
                                  idn(sha, "anneal_relax", t, T)))
                for n in extra:
                    rr.append(put(td / sub, n, "F_B", -9.0, "converged", idn(S[n]["sha256"], "anneal_relax", t, T)))
                return save(td / sub, rr)

            A = anneal_readout(vp, rp, ann("a_ok"), k_f=K)
            chk(A["winner"] == "F_B" and A["t_a_ps"] == 100 and A["families"]["F_P"]["M"] == 5
                and A["families"]["F_P"]["need_G1"] == 5,
                "[양성] 어닐 판독 — 계획 전체 · t_a 100 · 500 K · 시작 = 6 단계 post_relax → 승자 F_B (M 5 · G1 5)")
            for label, kw, why in (("20 ps (t_a 100 ≠)", {"t": 20.0}, "time_ps"),
                                   ("1000 K", {"T": 1000.0}, "temperature_K"),
                                   ("계획 하나 누락", {"drop": {"cfg0004_O-free_s"}}, "누락"),
                                   ("계획 밖 기록", {"extra": ["cfg0007_O-bo4"]}, "밖 기록"),
                                   ("시작 = 생성 CIF (6 단계 post_relax 아님)", {"start_from": "cif"}, "시작 파일이 계획과 다르다")):
                chk(refuses(why, anneal_readout, vp, rp, ann("a_" + str(abs(hash(label)) % 10**6), **kw), k_f=K),
                    f"⛔음성: 어닐 결과가 {label} 이면 판독하지 않는다 (Codex DW — 옛 판: 승자 F_B)")
            Af = anneal_readout(vp, rp, ann("a_fail", fail={"cfg0001_O-distributed"}), k_f=K)
            chk(Af["winner"] is None and any("G1" in h for h in Af["hold_reasons"])
                and Af["families"]["F_P"]["n_success"] == 4,
                "⛔음성: 실패 기록은 거부가 아니라 G1 분모에서 실패로 센다 (M 5 · 성공 4 < 5 → 보류 · 누락과 다르다)")
            V2 = screen_verdict(gen, screen_res("s_ok2", over={"cfg0007_O-bo4": {}}), k_f=K)
            vp2 = _dump(dict(V2, decision=V2["decision"]), td / "verdict2.json")
            s2 = json.loads(vp2.read_text())
            chk(_sha(vp2) != _sha(vp) and refuses("다른 거름 판정", anneal_readout, vp2, rp, ann("a_v2"), k_f=K) and s2["status"] == "complete",
                "⛔음성: 다른 거름 판정 (다른 결과 묶음) 에 이 파일럿 영수증을 붙이면 거부")
            chk(refuses("다시 낸 판정과 다르다", anneal_readout, vtp, rp, ann("a_vt"), k_f=K),
                "⛔음성: 손으로 바뀐 거름 판정으로는 어닐 판독을 하지 않는다")
        finally:
            _EN.verify_manifest = _vm

    # (4) EOS — 기준 (보정 전) 순서와 0.10 판정을 모든 조합이 지켜야 생략 (DW P1-3)
    c21, c32 = eos_correction(2.0, 2436.33, 21.7), eos_correction(2.0, 2436.33, 32.5)
    chk(abs(c21 + 1.402) < 2e-3 and abs(c32 + 0.936) < 2e-3, f"[외부 산술] P 2 GPa · V 2436.33 Å³ 보정 {c21:.3f} ~ {c32:.3f} eV (Codex)")
    e2 = eos_robust({"F_B": (-0.15, 2.0, 2436.33), "F_P": (0.0, 2.0, 2436.33), "F_free": (0.5, 2.0, 2436.33)}, margin=0.10)
    chk(e2["robust_common_B"] and not e2["robust_independent_B"] and not e2["skip_eos"],
        "⛔음성: 같은 압력의 두 가족 — 공통 B 면 0.15 차 유지 · 가족별 B 독립이면 뒤집힌다 → EOS 생략 불가")
    e3 = eos_robust({"F_B": (-0.6, 0.3, 2436.33), "F_P": (0.0, 0.3, 2436.33), "F_free": (0.4, 0.2, 2436.33)}, margin=0.10)
    chk(e3["skip_eos"], "[양성] 압력이 작고 (0.3 GPa) 차가 크면 모든 조합에서 기준과 같은 판정 → EOS 생략 가능")
    chk(not eos_robust({"F_B": (-0.6, 2.5, 2436.33), "F_P": (0.0, 0.3, 2436.33), "F_free": (0.4, 0.2, 2436.33)})["skip_eos"],
        "⛔음성: 한 가족이라도 |P| > 2 GPa 면 생략 불가")
    e4 = eos_robust({"F_B": (-0.15, 0.0, 2436.33), "F_P": (0.0, 2.0, 2436.33), "F_free": (0.5, 0.0, 2436.33)})
    chk(not e4["skip_eos"] and e4["baseline_order"] == ["F_B", "F_P", "F_free"]
        and all(c["order"][0] == "F_P" for c in e4["corners"]),
        "⛔음성: 모든 조합이 같은 쪽으로 뒤집히면 (기준 F_B → 전부 F_P) 생략 불가 (Codex DW all_corners_flip — 옛 판: 생략)")
    e5 = eos_robust({"F_B": (-5.0, 0.0, 2436.33), "F_P": (0.0, 2.0, 2436.33), "F_free": (0.15, 2.0, 2436.33)})
    chk(not e5["skip_eos"] and all(c["order"][0] == "F_B" for c in e5["corners"]),
        "⛔음성: 승자 · 0.10 판정은 그대로여도 아래 순위가 바뀌는 조합이 있으면 생략 불가 (Codex DW lower_ranks — 옛 판: 생략)")

    # (5) 계약 = 카드 값 (갈라지면 개정이 필요하다)
    card = HERE.parents[1] / "db/properties/b2o3_bo_placement_estimand_2026_11_09.json"
    if card.is_file():
        c = json.loads(card.read_text())["개정_1_셀구축_v1_2026_11_09"].get("판독_계약", {})
        mach = c.get("기계_판독_값", {})
        keys = ["k_f", "k_f_shortfall", "r_bond_A", "r_grey_A", "margin_uma_eV", "pair_min", "pilot_spread_eV",
                "margin_dft_eV", "B_range_GPa", "eos_P_max_GPa", "pilot_times_ps", "unit_B2O3",
                "model", "relax_fmax", "cell_relax", "relax_steps", "dt_fs", "friction", "anneal_T_K"]
        diff = [k for k in keys if mach.get(k) != CONTRACT[k]]
        chk(bool(mach) and not diff, f"카드 판독_계약 기계_판독_값 == 도구 CONTRACT (갈라지면 개정 · 다른 키 {diff})")
    print(f"selftest {'PASS' if ok[0] == ok[1] else 'FAIL'} — {ok[1]}/{ok[0]}")
    return 0 if ok[0] == ok[1] else 1


def main(argv=None):
    if argv is None and "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("screen"); s.add_argument("--gen", required=True); s.add_argument("--results", required=True)
    s.add_argument("--out", required=True); s.add_argument("--plan_dir", help="실행기용 시작 파일 manifest (pilot · anneal)")
    e = sub.add_parser("extract"); e.add_argument("--verdict", required=True)
    e.add_argument("--pilot_results", required=True); e.add_argument("--out_dir", required=True)
    p = sub.add_parser("pilot"); p.add_argument("--snapshots", required=True); p.add_argument("--results", required=True)
    p.add_argument("--out", required=True)
    a = sub.add_parser("anneal"); a.add_argument("--verdict", required=True); a.add_argument("--receipt", required=True)
    a.add_argument("--results", required=True); a.add_argument("--out", required=True)
    q = sub.add_parser("eos"); q.add_argument("--families", required=True, help="JSON {가족: [E_eV, P_GPa, V_A3]}")
    q.add_argument("--out", required=True)
    A = ap.parse_args(argv)

    if A.cmd == "screen":
        r = screen_verdict(A.gen, A.results)
        print(f"-> {_dump(r, A.out)}")
        print(r["decision"])
        if r["status"] == "complete" and A.plan_dir:
            print(f"   시작 파일 manifest {write_plan_manifests(r, A.plan_dir)} -> {A.plan_dir}")
        return 0 if r["status"] == "complete" else 3
    if A.cmd == "extract":
        xp, x = extract_pilot(A.verdict, A.pilot_results, A.out_dir)
        print(f"-> {xp} · 프레임 { {t: s['frame'] for t, s in x['snapshots'].items()} } · manifest {Path(A.out_dir) / 'manifest.json'}")
        return 0
    if A.cmd == "pilot":
        r = pilot_receipt(A.snapshots, A.results)
        print(f"-> {_dump(r, A.out)}")
        print(r["decision"], r.get("why", ""))
        return 0 if r["t_a_ps"] else 3
    if A.cmd == "anneal":
        r = anneal_readout(A.verdict, A.receipt, A.results)
        print(f"-> {_dump(r, A.out)}")
        print(r["decision"], r.get("hold_reasons", ""))
        return 0
    if A.cmd == "eos":
        fam = {k: tuple(v) for k, v in json.loads(Path(A.families).read_text()).items()}
        r = eos_robust(fam)
        print(f"-> {_dump(r, A.out)}")
        print("EOS 생략 가능" if r["skip_eos"] else "EOS 생략 불가")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
