#!/usr/bin/env python3
"""b2o3_bo_readout.py — B·O 배치 카드 개정 1 (셀구축 v1.1) 판독기 — 결과 **전에** 만든 판독 계약의 기계판.

카드 db/properties/b2o3_bo_placement_estimand_2026_11_09.json `개정_1_셀구축_v1_2026_11_09.판독_계약` 을 그대로 옮긴다
(Codex DV Q5 · Q6 · P2 — 끝 꼴 · G3 분모 · 결측 처리 · 연속 파일럿 세 끝점 · 승자–차저 · EOS 가족별 B).

하위 명령
  screen   6 단계 — 이완만 결과 → 가족마다 성공 구조 에너지 순위 → 상위 k_f 바탕의 합집합 (어닐 대상 목록)
  extract  7 단계 파일럿 — 연속 100 ps 어닐의 md.traj 에서 20 · 50 · 100 ps 프레임을 꺼내 xyz + 출처 (궤적 sha256 · 프레임)
  pilot    7 단계 — 세 스냅숏 이완 결과 → t_a (20 또는 100 ps) 또는 '파일럿 미완료'
  anneal   8 단계 — 어닐 결과 → G1 · G2 · G3 · 가족 최저 · 공통 성공 짝 · 승자–차저 (또는 보류 이유)
  eos      9 단계 ③ — 가족마다 B 를 독립으로 범위 끝에 둬도 순서 · 승자–차저 판정이 그대로인가 (EOS 생략 조건)

성공 (판독에 쓰는 구조) = run_anneal 상태 converged **이고** verify_outputs (결과 파일 존재 · sha256 · 판독 · 조성) 통과.
가족 표지 = 시작 가족 (생성기 manifest) · 끝 꼴은 따로 센다 (G3).

⛔ 이 도구가 못 하는 것
  · 판정 문장을 쓰지 않는다 — 허용 · 금지 서술은 카드에서만.
  · UMA 가 맞는지 모른다 (UMA 내부 비교) · 최저가 진짜 바닥인지 모른다 ('선언한 표본에서 찾은 최저').
  · 끝 꼴 분류는 거리 문턱 (O–B · O–P < 1.8 Å 결합 · 1.8–2.3 Å 미분류) 의 기하 분류다 — 결합 차수 · 전하를 보지 않는다.
  · 어닐이 Li 초기점 의존성을 없앴다고 말하지 않는다.

  python3 tools/doping/b2o3_bo_readout.py --selftest
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, sys
from pathlib import Path
import numpy as np
from ase.io import read, write

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_RA = _load("run_anneal_mod", HERE / "run_anneal.py")        # verify_outputs · _file_sha256 (결속 규칙 하나)
_EN = _load("b2o3_enumerate_mod", HERE / "b2o3_enumerate.py")  # verify_manifest · mic_dists

# ── 판독 계약 (카드 개정 1 · 판독_계약 과 같아야 한다 — selftest 가 카드 값과 대조) ─────────────────
CONTRACT = {
    "families": {"bo4": "F_B", "distributed": "F_P", "free_s": "F_free"},
    "unit_B2O3": 1,                      # 에너지 차 / 1
    "k_f": 6,                            # 6 단계 가족마다 상위 바탕 수
    "r_bond_A": 1.8,                     # O–B · O–P 결합 (기존: Nd O 꼴 카드 P–O < 1.8 Å)
    "r_grey_A": 2.3,                     # 1.8 ≤ d < 2.3 이면 그 O 는 미분류
    "g1_frac": "ceil(5M/6)",             # 가족마다 성공 ≥ ceil(5M/6) (M = 그 가족 어닐 수)
    "g3_rule": "changed / n_success > 1/3",  # 분모 = 그 가족 성공 수 · 바뀜 = 끝 꼴 ≠ 시작 가족 (섞임 · 미분류 포함)
    "margin_uma_eV": 0.20,               # 승자–차저 (이상이면 승자)
    "pair_min": 3,                       # 공통 성공 짝이 이보다 적으면 짝 서술 보류
    "pair_frac": 5 / 6,                  # 같은 부호 비율 ≥ 5/6 이면 '짝으로도 같은 방향'
    "pilot_times_ps": [20, 50, 100],
    "pilot_spread_eV": 0.05,             # max − min ≤ 0.05 (/B₂O₃) · 끝 꼴 같음 → 20 ps
    "margin_dft_eV": 0.10,
    "B_range_GPa": [21.7, 32.5],
    "eos_P_max_GPa": 2.0,
}
FAM_ORDER = ["F_B", "F_P", "F_free"]


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
    """구조의 끝 꼴: 모든 O 가 B → F_B · P → F_P · free → F_free · 미분류 O 하나라도 → unclassified · 그 밖 → mixed."""
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


# ───────────────────────── 입력 ─────────────────────────
def manifest_map(gen_dir):
    """생성기 출력 → {구조 이름 (파일 stem): (바탕 순위, 시작 가족)} · manifest 검증이 깨끗해야 한다."""
    prob = _EN.verify_manifest(gen_dir)
    if prob:
        raise SystemExit(f"⛔ 생성기 manifest 검증 실패 ({len(prob)} 건 · 예 {prob[0]}) — 판독하지 않는다")
    m = json.loads((Path(gen_dir) / "manifest.json").read_text())
    out = {}
    for b in m["bases"]:
        for motif, e in b["motifs"].items():
            out[Path(e["file"]).stem] = (int(b["rank"]), CONTRACT["families"][motif])
    return out


def load_records(results_json):
    """anneal_results.json → {이름: dict(ok, status, E, atoms, why)} — 성공 = converged + verify_outputs 통과."""
    p = Path(results_json)
    res = json.loads(p.read_text()).get("results", [])
    out = {}
    for r in res:
        n = r.get("name")
        st = r.get("status")
        why = []
        if st != "converged":
            why.append(f"상태 {st}")
        vo = _RA.verify_outputs(r, p.parent) if st in ("converged", "unconverged") else []
        why += vo
        E = r.get("E_post_relax")
        if E is None or not math.isfinite(float(E)):
            why.append("에너지 없음 · 유한 아님")
        atoms = None
        if not vo and r.get("outputs"):
            atoms = read(str(p.parent / r["outputs"]["post_relax"]["rel"]))
        out[n] = {"ok": not why, "status": st, "E": (float(E) if E is not None else None),
                  "atoms": atoms, "why": why, "identity": r.get("identity") or {}}
    return out


# ───────────────────────── 6 단계 거름 ─────────────────────────
def screen(mmap, recs, k_f=None):
    k_f = CONTRACT["k_f"] if k_f is None else k_f
    fam = {F: [] for F in FAM_ORDER}
    missing, failed = [], []
    for n, (rank, F) in mmap.items():
        r = recs.get(n)
        if r is None:
            missing.append(n)
            continue
        stg = r["identity"].get("stage")
        if stg is not None and stg != "relax_only":
            raise SystemExit(f"⛔ {n}: 거름 입력은 이완만 (stage relax_only) 이어야 한다 — {stg}")
        if not r["ok"]:
            failed.append({"name": n, "why": r["why"]})
            continue
        fam[F].append((r["E"], rank, n))
    for F in FAM_ORDER:
        fam[F].sort()
    top = {F: [x[1] for x in fam[F][:k_f]] for F in FAM_ORDER}
    union = sorted({b for F in FAM_ORDER for b in top[F]})
    short = [F for F in FAM_ORDER if len(fam[F]) < k_f]
    lowest = min((x for F in FAM_ORDER for x in fam[F]), default=None)
    return {"k_f": k_f, "top_bases_by_family": top, "union_bases": union, "M": len(union),
            "n_success_by_family": {F: len(fam[F]) for F in FAM_ORDER},
            "missing": missing, "failed": failed,
            "pilot_structure": (lowest[2] if lowest else None),
            "⚠": ([f"성공 구조가 k_f 보다 적은 가족 {short} — 있는 것만 넣었다"] if short else [])
            + (["입력에 없는 구조가 있다 — 거름이 완전하지 않다"] if missing else [])}


# ───────────────────────── 7 단계 파일럿 ─────────────────────────
def extract_snapshots(traj, times_ps, dt_fs, log_every, out_dir, stem):
    """연속 궤적 md.traj 에서 times_ps 프레임 → xyz + 출처 JSON. 프레임 k 의 시각 = k · log_every · dt_fs / 1000 ps."""
    from ase.io.trajectory import Trajectory
    traj = Path(traj)
    tsha = hashlib.sha256(traj.read_bytes()).hexdigest()
    T = Trajectory(str(traj))
    n = len(T)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    prov = {"traj": str(traj), "traj_sha256": tsha, "n_frames": n, "dt_fs": dt_fs, "log_every": log_every,
            "snapshots": {}}
    for t in times_ps:
        k = t * 1000.0 / (dt_fs * log_every)
        if abs(k - round(k)) > 1e-9:
            raise SystemExit(f"⛔ {t} ps 가 프레임 간격 ({dt_fs * log_every / 1000} ps) 의 배수가 아니다")
        k = int(round(k))
        if k >= n:
            raise SystemExit(f"⛔ {t} ps 프레임 {k} 가 궤적에 없다 (프레임 {n} 개) — 연속 궤적이 짧다")
        f = out_dir / f"{stem}_t{int(t):03d}.xyz"
        write(str(f), T[k])
        prov["snapshots"][str(int(t))] = {"frame": k, "file": f.name,
                                          "sha256": hashlib.sha256(f.read_bytes()).hexdigest()}
    T.close()
    (out_dir / f"{stem}_snapshots.json").write_text(json.dumps(prov, ensure_ascii=False, indent=1) + "\n")
    return prov


def pilot(prov, recs, stem):
    """세 스냅숏 이완 → t_a. 셋 다 같은 궤적 · 정확한 시각 · 성공 · 유한 · 끝 꼴 분류여야 판정 (아니면 미완료)."""
    times = CONTRACT["pilot_times_ps"]
    why, E, mot = [], {}, {}
    if sorted(int(t) for t in prov.get("snapshots", {})) != times:
        why.append(f"스냅숏 시각 {sorted(prov.get('snapshots', {}))} ≠ {times}")
    for t in times:
        s = prov.get("snapshots", {}).get(str(t))
        n = f"{stem}_t{t:03d}"
        r = recs.get(n)
        if s is None or r is None:
            why.append(f"{t} ps 끝점 없음")
            continue
        idn = r["identity"]
        if idn.get("input_file_sha256") != s["sha256"]:
            why.append(f"{t} ps: 이완 입력이 추출한 스냅숏이 아니다 (sha256)")
        if idn.get("stage") != "relax_only":
            why.append(f"{t} ps: 이완만이 아니다")
        if not r["ok"]:
            why.append(f"{t} ps: {r['why'][:1]}")
            continue
        E[t] = r["E"] / CONTRACT["unit_B2O3"]
        mot[t] = end_motif(r["atoms"])
        if mot[t] == "unclassified":
            why.append(f"{t} ps: 끝 꼴 미분류")
    if why:
        return {"decision": "파일럿 미완료", "t_a_ps": None, "why": why, "E": E, "end_motif": mot,
                "traj_sha256": prov.get("traj_sha256")}
    spread = max(E.values()) - min(E.values())
    same = len(set(mot.values())) == 1
    ta = 20 if (spread <= CONTRACT["pilot_spread_eV"] + 1e-12 and same) else 100
    return {"decision": f"t_a = {ta} ps", "t_a_ps": ta, "spread_eV": spread, "same_end_motif": same,
            "E": E, "end_motif": mot, "traj_sha256": prov.get("traj_sha256"),
            "⚠": "운영 규칙 (길이 고르기) — 수렴 증거가 아니다 · 파일럿의 선택된 t_a 보다 긴 결과는 다른 배치와 견주지 않는다"}


# ───────────────────────── 8 단계 어닐 판독 ─────────────────────────
def anneal_readout(mmap, recs, union_bases, margin=None):
    margin = CONTRACT["margin_uma_eV"] if margin is None else margin
    unit = CONTRACT["unit_B2O3"]
    ub = set(int(b) for b in union_bases)
    planned = {F: [] for F in FAM_ORDER}
    for n, (rank, F) in mmap.items():
        if rank in ub:
            planned[F].append((rank, n))
    fams = {}
    holds = []
    for F in FAM_ORDER:
        M = len(planned[F])
        succ, changed, notrun = [], [], []
        for rank, n in sorted(planned[F]):
            r = recs.get(n)
            if r is None:
                notrun.append(n)
                continue
            stg = r["identity"].get("stage")
            if stg is not None and stg != "anneal_relax":      # 정체성 없는 실패 기록은 어차피 성공이 아니다
                raise SystemExit(f"⛔ {n}: 어닐 판독 입력은 stage anneal_relax 여야 한다 ({stg})")
            if not r["ok"]:
                continue
            em = end_motif(r["atoms"])
            succ.append({"rank": rank, "name": n, "E": r["E"] / unit, "end_motif": em})
            if em != F:
                changed.append(n)
        need = math.ceil(5 * M / 6) if M else 0
        g1 = M > 0 and len(succ) >= need
        g3_mixed = bool(succ) and (len(changed) / len(succ) > 1 / 3)
        best = min(succ, key=lambda x: (x["E"], x["rank"])) if succ else None
        fams[F] = {"M": M, "n_success": len(succ), "need_G1": need, "G1": g1, "not_run": notrun,
                   "n_end_changed": len(changed), "G3_mixed": g3_mixed,
                   "G3": f"{len(changed)}/{len(succ)}" if succ else "—",
                   "min": best, "success": succ}
        if not g1:
            holds.append(f"{F}: G1 실패 (성공 {len(succ)} < {need} · 탈락)")
        if best is None:
            holds.append(f"{F}: 성공 구조 없음 (가족 결측)")
        elif best["end_motif"] == "unclassified":
            holds.append(f"{F}: 가족 최저 구조의 끝 꼴 미분류")
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


# ───────────────────────── 9 단계 EOS 생략 조건 ─────────────────────────
GPA_A3_EV = 1e9 * 1e-30 / 1.602176634e-19        # GPa·Å³ → eV


def eos_correction(P_GPa, V_A3, B_GPa):
    return -(P_GPa ** 2) * V_A3 * GPA_A3_EV / (2.0 * B_GPa)


def eos_robust(fam, margin=None, B_range=None, P_max=None):
    """fam = {가족: (E_eV, P_GPa, V_A3)} → 가족마다 B 를 **독립으로** 범위 끝에 둔 모든 조합에서 순서 · 승자–차저 판정이 같은가.

    보정은 B 에 단조라 끝점 조합 (2^n) 이면 충분하다. |P| > P_max 인 가족이 있으면 생략 불가.
    """
    import itertools
    margin = CONTRACT["margin_dft_eV"] if margin is None else margin
    B_range = CONTRACT["B_range_GPa"] if B_range is None else B_range
    P_max = CONTRACT["eos_P_max_GPa"] if P_max is None else P_max
    names = sorted(fam)
    verdicts, corners = set(), []
    for Bs in itertools.product(B_range, repeat=len(names)):
        Ec = {F: fam[F][0] + eos_correction(fam[F][1], fam[F][2], B) for F, B in zip(names, Bs)}
        order = sorted(names, key=Ec.get)
        gap = Ec[order[1]] - Ec[order[0]]
        v = (order[0], gap >= margin - 1e-12)
        verdicts.add(v)
        corners.append({"B": dict(zip(names, Bs)), "order": order, "gap": gap})
    common = set()
    for B in B_range:
        Ec = {F: fam[F][0] + eos_correction(fam[F][1], fam[F][2], B) for F in names}
        order = sorted(names, key=Ec.get)
        common.add((order[0], Ec[order[1]] - Ec[order[0]] >= margin - 1e-12))
    p_ok = all(abs(fam[F][1]) <= P_max for F in names)
    return {"robust_independent_B": len(verdicts) == 1, "robust_common_B": len(common) == 1,
            "pressure_ok": p_ok, "skip_eos": p_ok and len(verdicts) == 1,
            "corners": corners}


# ───────────────────────── selftest ─────────────────────────
def _selftest():
    import tempfile
    from ase import Atoms
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

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
    br.positions[2] = (br.positions[0] + br.positions[1]) / 2 * 0 + np.array([2.0, 2, 2]) + np.array([1.45, 0, 0])
    br.positions[1] = br.positions[2] + np.array([1.6, 0, 0])   # 그 O 가 B · P 둘 다에 붙음
    chk("bridge" in classify_o(br) and end_motif(br) == "mixed", "⛔음성: B · P 둘 다에 붙은 O 는 가교 → 섞임")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)

        def results(rows, stage, sub):
            """rows = [(이름, 꼴, E, 상태)] → run_anneal 꼴 결과 (outputs 해시 · 조성 · 정체성)."""
            d = td / sub
            d.mkdir(parents=True, exist_ok=True)
            res = []
            for n, kind, E, st in rows:
                (d / n).mkdir(exist_ok=True)
                a = toy(kind)
                for k in ("post_md", "post_relax"):
                    write(str(d / n / f"{k}.xyz"), a)
                rec = {"name": n, "status": st, "converged": st == "converged", "E_post_relax": E,
                       "identity": {"stage": stage, "n_atoms": len(a), "input_file_sha256": f"sha-{n}"},
                       "composition": _RA._composition(a),
                       "outputs": {k: {"rel": f"{n}/{k}.xyz", "sha256": _RA._file_sha256(d / n / f"{k}.xyz")}
                                   for k in ("post_md", "post_relax")}}
                if st == "failed":
                    rec = {"name": n, "status": "failed", "error": "x"}
                res.append(rec)
            (d / "anneal_results.json").write_text(json.dumps({"results": res}))
            return d / "anneal_results.json"

        fam_kind = {"F_B": "F_B", "F_P": "F_P", "F_free": "F_free"}
        code = {"F_B": "bo4", "F_P": "distributed", "F_free": "free_s"}
        M_bases = list(range(6))
        mmap = {f"cfg{b:04d}_O-{code[F]}": (b, F) for b in M_bases for F in FAM_ORDER}

        def rows_for(Eshift, status=None, motif=None):
            rr = []
            for b in M_bases:
                for F in FAM_ORDER:
                    n = f"cfg{b:04d}_O-{code[F]}"
                    st = (status or {}).get(n, "converged")
                    kd = (motif or {}).get(n, fam_kind[F])
                    rr.append((n, kd, Eshift[F] + 0.01 * b, st))
            return rr

        # (2) 승자–차저 (Codex Q6 예): F_P 0 · F_B −0.21 · F_free −0.20 → 둘 다 F_P 보다 낮지만 승자 차 0.01 → 못 가른다
        r = anneal_readout(mmap, load_records(results(rows_for({"F_P": 0.0, "F_B": -0.21, "F_free": -0.20}),
                                                      "anneal_relax", "q6")), M_bases)
        chk(r["winner"] is None and "못 가른다" in r["decision"],
            f"⛔음성: 승자는 최저 대 차저 차로 — F_B −0.21 · F_free −0.20 은 0.01 차라 못 가른다 ({r['decision'][:30]})")
        r2 = anneal_readout(mmap, load_records(results(rows_for({"F_P": 0.0, "F_B": -0.50, "F_free": -0.20}),
                                                       "anneal_relax", "win")), M_bases)
        chk(r2["winner"] == "F_B" and r2["pairs"]["같은_방향"] and r2["n_pairs"] == 6,
            "[양성] 차 0.30 ≥ 0.20 → 승자 F_B · 공통 성공 짝 6 개 모두 같은 방향")
        # (3) G3 분모 (Codex 예): M 6 · 성공 5 · 끝 꼴 바뀜 2 → 2/5 > 1/3 섞임 · 성공 6 · 바뀜 2 → 2/6 섞임 아님
        st5 = {"cfg0005_O-bo4": "unconverged"}
        mo2 = {"cfg0001_O-bo4": "F_P", "cfg0002_O-bo4": "mixed"}
        r3 = anneal_readout(mmap, load_records(results(rows_for({"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}, st5, mo2),
                                                       "anneal_relax", "g3a")), M_bases)
        r4 = anneal_readout(mmap, load_records(results(rows_for({"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}, None, mo2),
                                                       "anneal_relax", "g3b")), M_bases)
        chk(r3["families"]["F_B"]["G3"] == "2/5" and r3["families"]["F_B"]["G3_mixed"]
            and r4["families"]["F_B"]["G3"] == "2/6" and not r4["families"]["F_B"]["G3_mixed"]
            and r3["families"]["F_B"]["G1"],
            "⛔음성: G3 분모 = 그 가족 성공 수 — 2/5 는 섞임 · 2/6 은 아님 (경계 '넘으면' = 엄격 >) · G1 은 5/6 통과")
        # (4) G1 탈락 → 승자 보류 · 가족 결측 → 보류 · 최저 구조 미분류 → 보류
        st_bad = {f"cfg{b:04d}_O-distributed": "failed" for b in (0, 1)}
        r5 = anneal_readout(mmap, load_records(results(rows_for({"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}, st_bad),
                                                       "anneal_relax", "g1")), M_bases)
        chk(r5["winner"] is None and any("G1 실패" in h for h in r5["hold_reasons"]),
            "⛔음성: 가족 하나가 G1 실패 (성공 4 < 5) → 승자 보류 (탈락 가족을 빼고 고르지 않는다)")
        st_none = {f"cfg{b:04d}_O-free_s": "failed" for b in M_bases}
        r6 = anneal_readout(mmap, load_records(results(rows_for({"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}, st_none),
                                                       "anneal_relax", "miss")), M_bases)
        chk(r6["winner"] is None and any("결측" in h for h in r6["hold_reasons"]),
            "⛔음성: 한 가족이 성공 0 (결측) → 보류")
        mo_g = {"cfg0000_O-bo4": "grey"}
        r7 = anneal_readout(mmap, load_records(results(rows_for({"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}, None, mo_g),
                                                       "anneal_relax", "grey")), M_bases)
        chk(r7["winner"] is None and any("미분류" in h for h in r7["hold_reasons"]),
            "⛔음성: 가족 최저 구조의 끝 꼴이 미분류 → 보류")
        # (5) 결과 파일 결속 — 최저 구조 파일을 바꾸면 그 구조는 성공이 아니다
        pth = results(rows_for({"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}), "anneal_relax", "bind")
        write(str(pth.parent / "cfg0000_O-bo4" / "post_relax.xyz"), toy("F_P"))
        rr = load_records(pth)
        chk(not rr["cfg0000_O-bo4"]["ok"] and any("sha256" in w for w in rr["cfg0000_O-bo4"]["why"]),
            "⛔음성: 결과 파일이 바뀐 구조는 판독에 안 쓴다 (run_anneal.verify_outputs — 결속 규칙 하나)")
        # (6) 짝 보류 — 공통 성공 짝 < 3 (합집합 바탕 2 개 · 모두 성공 → G1 통과 · 승자는 내되 짝 서술은 보류)
        r8 = anneal_readout(mmap, load_records(results(rows_for({"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}),
                                                       "anneal_relax", "pairs")), [0, 1])
        chk(r8["winner"] == "F_B" and r8["n_pairs"] == 2 and isinstance(r8["pairs"], str) and "보류" in r8["pairs"],
            "⛔음성: 공통 성공 짝 2 < 3 → 승자는 내도 짝 서술은 보류")
        # (7) 거름 — 이완만 결과에서 가족별 상위 k_f 합집합 · 실패 제외 · 단계 확인
        rows_s = rows_for({"F_P": 0.0, "F_B": -0.5, "F_free": -0.2}, {"cfg0000_O-bo4": "failed"})
        sc = screen(mmap, load_records(results(rows_s, "relax_only", "scr")), k_f=2)
        chk(sc["top_bases_by_family"]["F_B"] == [1, 2] and sc["union_bases"] == [0, 1, 2]
            and sc["pilot_structure"] == "cfg0001_O-bo4" and len(sc["failed"]) == 1,
            "[양성] 거름: 실패 구조는 빼고 가족별 상위 2 · 합집합 · 파일럿 = 성공 구조 전체 최저")
        try:
            screen(mmap, load_records(results(rows_s, "anneal_relax", "scr2")), k_f=2); okx = False
        except SystemExit:
            okx = True
        chk(okx, "⛔음성: 거름에 어닐 결과 (stage anneal_relax) 를 넣으면 멈춘다")

        # (8) 파일럿 — 한 연속 궤적 · 세 끝점
        from ase.io.trajectory import Trajectory
        tr = td / "pilot" / "md.traj"
        tr.parent.mkdir()
        T = Trajectory(str(tr), "w")
        for k in range(101):
            T.write(toy("F_B", shift=0.001 * k))
        T.close()
        prov = extract_snapshots(tr, [20, 50, 100], 2.0, 500, td / "snap", "pil")
        chk(prov["snapshots"]["50"]["frame"] == 50, "[양성] 2 fs · 500 걸음마다 → 50 ps = 프레임 50")
        try:
            extract_snapshots(tr, [20, 50, 150], 2.0, 500, td / "snap2", "pil"); okx = False
        except SystemExit:
            okx = True
        chk(okx, "⛔음성: 궤적이 150 ps 를 안 담으면 멈춘다 (지어내지 않는다)")

        def prec(Es, st=None, kinds=None, bad_sha=None):
            rows = []
            for t, E in zip((20, 50, 100), Es):
                rows.append((f"pil_t{t:03d}", (kinds or {}).get(t, "F_B"), E, (st or {}).get(t, "converged")))
            p = results(rows, "relax_only", f"pilot_{abs(hash((tuple(Es), str(st), str(kinds), str(bad_sha)))) % 10**8}")
            d = json.loads(p.read_text())
            for r_ in d["results"]:
                t = int(r_["name"][-3:])
                if "identity" in r_:
                    r_["identity"]["input_file_sha256"] = prov["snapshots"][str(t)]["sha256"] if t != bad_sha else "x"
            p.write_text(json.dumps(d))
            return load_records(p)

        pa = pilot(prov, prec([0.0, -0.02, -0.04]), "pil")
        pb = pilot(prov, prec([0.0, -0.30, -0.02]), "pil")
        chk(pa["t_a_ps"] == 20 and pb["t_a_ps"] == 100,
            "⛔음성: 세 시점 0 · −0.02 · −0.04 → 20 ps · Codex 예 0 · −0.30 · −0.02 → 100 ps (옛 |E20−E100| 규칙은 20 을 골랐다)")
        pc = pilot(prov, prec([0.0, -0.01, -0.02], st={50: "unconverged"}), "pil")
        pd = pilot(prov, prec([0.0, -0.01, -0.02], bad_sha=100), "pil")
        pe = pilot(prov, prec([0.0, -0.01, -0.02], kinds={100: "F_P"}), "pil")
        chk(pc["t_a_ps"] is None and pd["t_a_ps"] is None and pe["t_a_ps"] == 100,
            "⛔음성: 끝점 미수렴 · 다른 입력 (스냅숏 sha 불일치) → 파일럿 미완료 · 끝 꼴이 갈리면 100 ps")

    # (9) EOS — 공통 B 에서는 유지되는 0.15 eV 차가 가족별 B 를 독립으로 두면 뒤집힐 수 있다 (Codex Q5)
    fam = {"F_B": (-0.15, 2.0, 2436.33), "F_P": (0.0, 0.0, 2436.33), "F_free": (0.5, 0.0, 2436.33)}
    c21, c32 = eos_correction(2.0, 2436.33, 21.7), eos_correction(2.0, 2436.33, 32.5)
    chk(abs(c21 + 1.402) < 2e-3 and abs(c32 + 0.936) < 2e-3, f"[외부 산술] P 2 GPa · V 2436.33 Å³ 보정 {c21:.3f} ~ {c32:.3f} eV (Codex)")
    fam2 = {"F_B": (-0.15 + 0.0, 2.0, 2436.33), "F_P": (0.0 + 0.0, 2.0, 2436.33), "F_free": (0.5, 2.0, 2436.33)}
    e2 = eos_robust(fam2, margin=0.10)
    chk(e2["robust_common_B"] and not e2["robust_independent_B"] and not e2["skip_eos"],
        "⛔음성: 같은 압력의 두 가족 — 공통 B 면 0.15 차 유지 · 가족별 B 독립이면 뒤집힌다 → EOS 생략 불가")
    e3 = eos_robust({"F_B": (-0.6, 0.3, 2436.33), "F_P": (0.0, 0.3, 2436.33), "F_free": (0.4, 0.2, 2436.33)}, margin=0.10)
    chk(e3["skip_eos"], "[양성] 압력이 작고 (0.3 GPa) 차가 크면 모든 조합에서 같은 판정 → EOS 생략 가능")
    chk(not eos_robust({"F_B": (-0.6, 2.5, 2436.33), "F_P": (0.0, 0.3, 2436.33), "F_free": (0.4, 0.2, 2436.33)})["skip_eos"],
        "⛔음성: 한 가족이라도 |P| > 2 GPa 면 생략 불가")
    del fam

    # (10) 계약 = 카드 값 (갈라지면 개정이 필요하다)
    card = HERE.parents[1] / "db/properties/b2o3_bo_placement_estimand_2026_11_09.json"
    if card.is_file():
        c = json.loads(card.read_text())["개정_1_셀구축_v1_2026_11_09"].get("판독_계약", {})
        mach = c.get("기계_판독_값", {})
        keys = ["k_f", "r_bond_A", "r_grey_A", "margin_uma_eV", "pair_min", "pilot_spread_eV", "margin_dft_eV",
                "B_range_GPa", "eos_P_max_GPa", "pilot_times_ps", "unit_B2O3"]
        chk(bool(mach) and all(mach.get(k) == CONTRACT[k] for k in keys),
            "카드 판독_계약 기계_판독_값 == 도구 CONTRACT (갈라지면 개정)")
    print(f"selftest {'PASS' if ok[0] == ok[1] else 'FAIL'} — {ok[1]}/{ok[0]}")
    return 0 if ok[0] == ok[1] else 1


def main(argv=None):
    if argv is None and "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("screen"); s.add_argument("--gen", required=True); s.add_argument("--results", required=True)
    s.add_argument("--out", required=True)
    e = sub.add_parser("extract"); e.add_argument("--traj", required=True); e.add_argument("--stem", required=True)
    e.add_argument("--dt_fs", type=float, default=2.0); e.add_argument("--log_every", type=int, default=500)
    e.add_argument("--out_dir", required=True)
    p = sub.add_parser("pilot"); p.add_argument("--snapshots", required=True); p.add_argument("--results", required=True)
    p.add_argument("--stem", required=True); p.add_argument("--out", required=True)
    a = sub.add_parser("anneal"); a.add_argument("--gen", required=True); a.add_argument("--results", required=True)
    a.add_argument("--screen", required=True); a.add_argument("--out", required=True)
    q = sub.add_parser("eos"); q.add_argument("--families", required=True, help="JSON {가족: [E_eV, P_GPa, V_A3]}")
    q.add_argument("--out", required=True)
    A = ap.parse_args(argv)

    def dump(obj, path):
        Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str) + "\n")
        print(f"-> {path}")

    if A.cmd == "screen":
        r = screen(manifest_map(A.gen), load_records(A.results))
        dump(r, A.out)
        print(f"합집합 M = {r['M']} · 파일럿 = {r['pilot_structure']} · ⚠ {r['⚠']}")
    elif A.cmd == "extract":
        extract_snapshots(A.traj, CONTRACT["pilot_times_ps"], A.dt_fs, A.log_every, A.out_dir, A.stem)
    elif A.cmd == "pilot":
        r = pilot(json.loads(Path(A.snapshots).read_text()), load_records(A.results), A.stem)
        dump(r, A.out)
        print(r["decision"], r.get("why", ""))
        return 0 if r["t_a_ps"] else 3
    elif A.cmd == "anneal":
        sc = json.loads(Path(A.screen).read_text())
        r = anneal_readout(manifest_map(A.gen), load_records(A.results), sc["union_bases"])
        dump(r, A.out)
        print(r["decision"], r.get("hold_reasons", ""))
    elif A.cmd == "eos":
        fam = {k: tuple(v) for k, v in json.loads(Path(A.families).read_text()).items()}
        r = eos_robust(fam)
        dump(r, A.out)
        print("EOS 생략 가능" if r["skip_eos"] else "EOS 생략 불가")
    return 0


if __name__ == "__main__":
    sys.exit(main())
