#!/usr/bin/env python3
"""b2o3_site_dft.py — B 자리 (P 4b 대 Li) DFT 형성 에너지 카드의 준비 도구.

카드: db/properties/b2o3_site_dft_estimand_2026_11_23.json · 결정 D-2026-11-23-b2o3-site-dft

하위 명령
  ob_pairs  10월 UMA 후보 12 개 (O 세 개가 전부 P 에 붙은 꼴 · B-P 6 · B-Li 6) 에서, B · Li · 공공 배치는 그대로 두고
            O 세 개를 'B 결합 S' (B–S ≤ 2.3 Å) 자리로 옮긴 조합을 **전부** 만든다 (O↔S 교환 · 원자 수 · 조성 그대로).
            옮긴 원자는 결합 길이만 맞춘다: 새 O 는 B 에서 1.45 Å · 새 S 는 P 에서 2.05 Å (같은 방향) — 나머지 원자는 안 움직인다.
            출력 = 후보 폴더 (manifest.json · run_uma_kgy.sh 가 그대로 읽는 꼴: files{상대경로: {sha256 …}} · purpose)
  pick_ob   조합의 UMA 이완 결과 (run_anneal.py --time_ps 0 · anneal_results.json) 에서 바탕마다 최저 하나를 골라
            어닐용 후보 폴더를 만든다 (post_relax.xyz 를 바이트 그대로 복사 · sha256 · 둘째와의 차 · 끝 꼴)
  probe     DFT 메모리 프로브 입력 — 9 단계 판 고정 b2o3_bo_dft.py (sha256 0c3b7f51…) 의 pw_input_text 를 그대로 쓰고
            disk_io 한 줄만 바꾼다 (disk_io 는 숫자에 영향 없음 — QE 설명서: nowf · low 는 파동함수를 메모리에 ·
            medium · high 는 k 점이 둘 이상이면 디스크에)
  --selftest  음성 경로 포함

이 도구가 못 하는 것 (한계 — 숨기지 않는다)
  · UMA · DFT 를 돌리지 않는다 (입력 · 고르기만) · 형성 에너지 · D 를 내지 않는다 (판독 도구는 따로 · DFT 결과 전에 만든다).
  · 'B 결합 S' 는 10월 UMA 이완 구조의 2.3 Å 안 S 다 — B 가 이완 중 S 하나를 놓은 경우 (B-P 의 BS₃) 그 S 는 후보가 아니다.
  · 조합 고르기는 UMA 에너지다 (DFT 아님) · 어닐 전 이완 하나로 고른다 — 다른 조합이 어닐 뒤 더 낮을 가능성은 남는다.
  · O 꼴 이름 (O–B · O–P) 은 끝 구조로 다시 매겨야 한다 — 여기서는 시작 꼴만 적는다 (pick_ob 는 고른 이완 구조의 끝 꼴을 적는다).
  · 10월 O–P 후보는 10월 run_anneal.py (08-30 판) 로, O–B 짝은 지금 판으로 돈다 — MD · 이완 경로는 같고 수렴 판정 · 기록만 다르다
    (git diff 34a400e93 HEAD -- tools/doping/run_anneal.py · 11-23 확인).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import shutil
import sys
import tempfile
from pathlib import Path

import numpy as np

CARD = "db/properties/b2o3_site_dft_estimand_2026_11_23.json"
DECISION = "D-2026-11-23-b2o3-site-dft"
PINNED_DFT_REL = "tools/doping/b2o3_bo_dft.py"
PINNED_DFT_SHA = "0c3b7f51dbebff7ab9b818e165f0a4cf36a627a93efc878d2db04ff69b08cd0b"
MODELS = {"B-P": {"B": 2, "Cl": 16, "Li": 58, "O": 3, "P": 8, "S": 41},
          "B-Li": {"B": 2, "Cl": 16, "Li": 48, "O": 3, "P": 10, "S": 41}}
BASES = {"B-P": [f"BMP_{i:02d}" for i in range(6)], "B-Li": [f"BMLi_{i:02d}" for i in range(6)]}
R_BS = 2.3      # B 결합 S (끝 꼴 판정 문턱과 같다)
R_XO = 1.8      # O–B · O–P 결합 (9 단계 · 10월 판독과 같다)
D_BO = 1.45     # 옮긴 O 의 B–O 시작 거리 (Å)
D_PS = 2.05     # 옮긴 S 의 P–S 시작 거리 (Å)
MIN_PAIR = 1.0  # 옮긴 뒤 원자 쌍 최소 거리 (Å) — 이보다 가까우면 멈춘다
PURPOSE_COMBO = "b2o3_site_dft/ob_combo_relax"
PURPOSE_ANNEAL = "b2o3_site_dft/ob_anneal"
DISK_IO = ("nowf", "low", "medium", "high")


def sha256_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tool_sha() -> str:
    return sha256_file(__file__)


def composition(atoms) -> dict:
    out = {}
    for s in atoms.get_chemical_symbols():
        out[s] = out.get(s, 0) + 1
    return dict(sorted(out.items()))


def site_of(base: str) -> str:
    for s, names in BASES.items():
        if base in names:
            return s
    raise SystemExit(f"⛔ 모르는 바탕 이름 {base}")


# ----------------------------------------------------------------------------- 이웃
def _neighbors(atoms, i, species, rmax):
    """원자 i 에서 rmax 안의 species 원자 (최소상 · 벡터 포함) — [(j, d, vec_i_to_j)]."""
    syms = atoms.get_chemical_symbols()
    out = []
    for j, s in enumerate(syms):
        if j == i or s != species:
            continue
        v = atoms.get_distance(i, j, mic=True, vector=True)
        d = float(np.linalg.norm(v))
        if d <= rmax:
            out.append((j, d, np.asarray(v, float)))
    return sorted(out, key=lambda t: t[1])


def o_partners(atoms) -> list:
    """O 마다 결합 상대 (B · P · ≤ R_XO) — 끝 꼴 기록용."""
    syms = atoms.get_chemical_symbols()
    res = []
    for o, s in enumerate(syms):
        if s != "O":
            continue
        part = sorted({syms[j] for j, _, _ in _neighbors(atoms, o, "B", R_XO) + _neighbors(atoms, o, "P", R_XO)})
        res.append("".join(part) or "free")
    return res


def b_shells(atoms) -> list:
    syms = atoms.get_chemical_symbols()
    out = []
    for b, s in enumerate(syms):
        if s != "B":
            continue
        nO = len(_neighbors(atoms, b, "O", R_XO))
        nS = len(_neighbors(atoms, b, "S", R_BS))
        out.append(f"O{nO}S{nS}")
    return out


# ----------------------------------------------------------------------------- 짝 만들기
def op_motif_problems(atoms) -> list:
    """O–P 꼴 (O 마다 P 에 붙고 B 에는 안 붙음) 이 아니면 문제 목록."""
    syms = atoms.get_chemical_symbols()
    probs = []
    for o, s in enumerate(syms):
        if s != "O":
            continue
        if _neighbors(atoms, o, "B", R_XO):
            probs.append(f"O {o} 가 이미 B 에 붙어 있다")
        elif not _neighbors(atoms, o, "P", R_XO):
            probs.append(f"O {o} 가 P 에 안 붙어 있다 (≤ {R_XO} Å)")
    return probs


def ob_combos(atoms, *, expect_comp=None):
    """O–P 꼴 구조 하나 → O–B 조합 목록 [(atoms_new, info)] · 입력이 O–P 꼴이 아니면 멈춘다."""
    syms = atoms.get_chemical_symbols()
    if expect_comp is not None and composition(atoms) != dict(sorted(expect_comp.items())):
        raise SystemExit(f"⛔ 조성 {composition(atoms)} ≠ 모델 {dict(sorted(expect_comp.items()))}")
    Bs = [i for i, s in enumerate(syms) if s == "B"]
    Os = [i for i, s in enumerate(syms) if s == "O"]
    if len(Os) != 3:
        raise SystemExit(f"⛔ O 가 {len(Os)} 개 — 3 개여야 한다")
    if not Bs:
        raise SystemExit("⛔ B 가 없다")
    probs = op_motif_problems(atoms)
    if probs:
        raise SystemExit("⛔ 입력이 O–P 꼴이 아니다: " + " · ".join(probs))
    o_parent = {o: _neighbors(atoms, o, "P", R_XO)[0] for o in Os}
    shell = {}                       # S index → (nearest B, d, vec B→S)
    for b in Bs:
        for j, d, v in _neighbors(atoms, b, "S", R_BS):
            if j not in shell or d < shell[j][1]:
                shell[j] = (b, d, v)
    cand = sorted(shell)
    if len(cand) < 3:
        raise SystemExit(f"⛔ B 결합 S 가 {len(cand)} 개 (≤ {R_BS} Å) — 셋을 못 고른다")
    out = []
    for k, combo in enumerate(itertools.combinations(cand, 3)):
        a = atoms.copy()
        pos = a.get_positions()
        new_syms = list(syms)
        for o in Os:                          # O → S · P 에서 D_PS (같은 방향)
            p, d, v = o_parent[o]             # v = o → p 벡터
            u = -v / np.linalg.norm(v)        # p → o 방향
            pos[o] = pos[p] + u * D_PS        # P 의 실제 좌표 기준 · 최소상 방향 (셀 밖이면 아래 wrap)
            new_syms[o] = "S"
        for s in combo:                       # S → O · B 에서 D_BO (같은 방향)
            b, d, v = shell[s]                # v = b → s
            pos[s] = pos[b] + v / np.linalg.norm(v) * D_BO
            new_syms[s] = "O"
        a.set_chemical_symbols(new_syms)
        a.set_positions(pos)
        a.wrap()
        dmin = _min_pair(a)
        if dmin < MIN_PAIR:
            raise SystemExit(f"⛔ 조합 {combo}: 옮긴 뒤 원자 쌍 최소 거리 {dmin:.2f} Å < {MIN_PAIR}")
        by_b = {}
        for s in combo:
            by_b[shell[s][0]] = by_b.get(shell[s][0], 0) + 1
        split = "+".join(str(x) for x in sorted(by_b.values(), reverse=True))
        out.append((a, {"k": k, "o_from": sorted(Os), "o_to": list(combo), "split": split,
                        "n_bshell_S": len(cand), "min_pair_A": round(dmin, 3)}))
    return out


def _min_pair(atoms) -> float:
    from ase.neighborlist import neighbor_list
    d = neighbor_list("d", atoms, 2.0)
    return float(d.min()) if len(d) else 9.9


def read_sums(raw: Path) -> dict:
    p = raw / "SHA256SUMS"
    if not p.is_file():
        raise SystemExit(f"⛔ {p} 가 없다")
    out = {}
    for ln in p.read_text().splitlines():
        if not ln.strip():
            continue
        h, rel = ln.split(None, 1)
        rel = rel.strip()
        out[rel[2:] if rel.startswith("./") else rel] = h
    return out


def cmd_ob_pairs(raw: Path, out: Path, *, bases=None, expect_comp=True) -> dict:
    from ase.io import read, write
    raw, out = Path(raw), Path(out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"⛔ {out} 가 비어 있지 않다 — 덮지 않는다")
    sums = read_sums(raw)
    names = bases or [n for s in BASES for n in BASES[s]]
    (out / "combos").mkdir(parents=True, exist_ok=True)
    files, parents = {}, {}
    for base in names:
        rel = f"structures/{base}.xyz"
        src = raw / rel
        if rel not in sums:
            raise SystemExit(f"⛔ SHA256SUMS 에 {rel} 가 없다")
        h = sha256_file(src)
        if h != sums[rel]:
            raise SystemExit(f"⛔ {rel} sha256 {h[:12]} ≠ SHA256SUMS {sums[rel][:12]}")
        site = site_of(base)
        a = read(str(src))
        combos = ob_combos(a, expect_comp=MODELS[site] if expect_comp else None)
        splits = {}
        for a2, info in combos:
            fn = f"combos/{base}__c{info['k']:02d}.xyz"
            write(str(out / fn), a2, format="extxyz")
            files[fn] = {"sha256": sha256_file(out / fn), "parent": base, "parent_sha256": h, "site": site,
                         "o_from": info["o_from"], "o_to": info["o_to"], "split": info["split"],
                         "min_pair_A": info["min_pair_A"]}
            splits[info["split"]] = splits.get(info["split"], 0) + 1
        parents[base] = {"site": site, "sha256": h, "n_combos": len(combos), "n_bshell_S": combos[0][1]["n_bshell_S"],
                         "splits": splits, "start_o_partners": o_partners(a), "start_b_shells": b_shells(a)}
    man = {"schema": "b2o3_site_dft_combos/v1", "purpose": PURPOSE_COMBO, "card": CARD, "decision": DECISION,
           "tool": {"path": "tools/doping/b2o3_site_dft.py", "sha256": tool_sha()},
           "source": {"raw": str(raw), "SHA256SUMS_sha256": sha256_file(raw / "SHA256SUMS")},
           "rule": {"R_BS_A": R_BS, "R_XO_A": R_XO, "D_BO_A": D_BO, "D_PS_A": D_PS, "min_pair_A": MIN_PAIR},
           "n_files": len(files), "parents": parents, "files": files}
    assert "bases" not in man, "run_uma_kgy.sh 는 'bases' 키를 b2o3_enumerate manifest 로 읽는다"
    (out / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    return man


# ----------------------------------------------------------------------------- 고르기
def cmd_pick_ob(combos: Path, results: Path, out: Path) -> dict:
    from ase.io import read
    combos, results, out = Path(combos), Path(results), Path(out)
    man = json.loads((combos / "manifest.json").read_text())
    if man.get("schema") != "b2o3_site_dft_combos/v1" or man.get("purpose") != PURPOSE_COMBO:
        raise SystemExit("⛔ 조합 manifest 가 아니다 (schema · purpose)")
    for rel, e in man["files"].items():
        if sha256_file(combos / rel) != e["sha256"]:
            raise SystemExit(f"⛔ 조합 파일이 manifest 뒤 바뀌었다: {rel}")
    R = json.loads(results.read_text())
    if float(R.get("time_ps", -1)) != 0.0:
        raise SystemExit(f"⛔ 결과의 time_ps {R.get('time_ps')} — 조합 고르기는 이완만 (0) 이어야 한다")
    rec = {}
    for r in R.get("results", []):
        nm = r.get("name")
        if nm in rec:
            raise SystemExit(f"⛔ 결과에 같은 이름이 둘: {nm}")
        rec[nm] = r
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"⛔ {out} 가 비어 있지 않다 — 덮지 않는다")
    by_parent = {}
    for rel, e in man["files"].items():
        nm = Path(rel).stem
        r = rec.get(nm)
        if r is None:
            raise SystemExit(f"⛔ 조합 {nm} 의 결과가 없다 (누락은 실패가 아니다 — 다 돌린 뒤 고른다)")
        by_parent.setdefault(e["parent"], []).append((nm, rel, e, r))
    extra = set(rec) - {Path(rel).stem for rel in man["files"]}
    if extra:
        raise SystemExit(f"⛔ 결과에 조합 밖 이름 {sorted(extra)[:5]}")
    (out / "ob_selected").mkdir(parents=True, exist_ok=True)
    files, summary = {}, {}
    for base in sorted(by_parent):
        rows = []
        for nm, rel, e, r in by_parent[base]:
            st = r.get("status")
            if st is None:
                raise SystemExit(f"⛔ {nm}: status 가 없다 (2026-11-09 이전 판 기록 — 지금 판 run_anneal.py 로 돌려야 한다)")
            if st != "converged":
                rows.append((nm, rel, e, r, None, st)); continue
            o = r.get("outputs", {}).get("post_relax")
            if not o:
                raise SystemExit(f"⛔ {nm}: outputs.post_relax 기록이 없다")
            p = results.parent / o["rel"]
            if not p.is_file() or sha256_file(p) != o["sha256"]:
                raise SystemExit(f"⛔ {nm}: post_relax.xyz 가 없거나 기록 뒤 바뀌었다")
            a = read(str(p))
            if composition(a) != dict(sorted(MODELS[e["site"]].items())):
                raise SystemExit(f"⛔ {nm}: 이완 구조 조성 {composition(a)} ≠ 모델")
            E = float(r["E_post_relax"])
            if not np.isfinite(E):
                raise SystemExit(f"⛔ {nm}: 에너지가 유한하지 않다")
            rows.append((nm, rel, e, r, E, st))
        ok = sorted([x for x in rows if x[4] is not None], key=lambda x: (x[4], x[0]))
        if not ok:
            raise SystemExit(f"⛔ {base}: 수렴한 조합이 없다 ({len(rows)} 개 중)")
        nm, rel, e, r, E, _ = ok[0]
        src = results.parent / r["outputs"]["post_relax"]["rel"]
        dst = out / "ob_selected" / f"{base}_OB.xyz"
        shutil.copyfile(src, dst)
        a = read(str(dst))
        files[f"ob_selected/{base}_OB.xyz"] = {
            "sha256": sha256_file(dst), "parent": base, "site": e["site"], "from_combo": nm,
            "from_combo_input_sha256": e["sha256"], "E_uma_relax_eV": E,
            "gap_to_second_eV": (ok[1][4] - E) if len(ok) > 1 else None,
            "end_o_partners": o_partners(a), "end_b_shells": b_shells(a), "split": e["split"]}
        summary[base] = {"n_combos": len(rows), "n_converged": len(ok),
                         "n_not_converged": {st: sum(1 for x in rows if x[5] == st) for st in {x[5] for x in rows if x[4] is None}},
                         "chosen": nm}
    want = sorted(man["parents"])
    if sorted(summary) != want:
        raise SystemExit(f"⛔ 고른 바탕 {sorted(summary)} ≠ 조합 바탕 {want}")
    sel = {"schema": "b2o3_site_dft_ob_selected/v1", "purpose": PURPOSE_ANNEAL, "card": CARD, "decision": DECISION,
           "tool": {"path": "tools/doping/b2o3_site_dft.py", "sha256": tool_sha()},
           "combos_manifest_sha256": sha256_file(combos / "manifest.json"),
           "results_sha256": sha256_file(results), "summary": summary, "files": files}
    (out / "manifest.json").write_text(json.dumps(sel, ensure_ascii=False, indent=1) + "\n")
    return sel


# ----------------------------------------------------------------------------- DFT 입력 (프로브)
def load_pinned(repo_root: Path):
    p = Path(repo_root) / PINNED_DFT_REL
    h = sha256_file(p)
    if h != PINNED_DFT_SHA:
        raise SystemExit(f"⛔ {PINNED_DFT_REL} sha256 {h[:12]} ≠ 판 고정 {PINNED_DFT_SHA[:12]} — 9 단계와 같은 설정이 아니다")
    spec = importlib.util.spec_from_file_location("b2o3_bo_dft_pinned", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def pw_text(mod, atoms, *, prefix, calc, k, pseudo_dir, disk_io, tstress=False) -> str:
    if disk_io not in DISK_IO:
        raise SystemExit(f"⛔ disk_io {disk_io} — {DISK_IO} 중 하나")
    t = mod.pw_input_text(atoms, prefix=prefix, calc=calc, k=k, pseudo_dir=pseudo_dir, tstress=tstress)
    old = f"    disk_io = '{mod.DFT['disk_io']}'"
    if t.count(old) != 1:
        raise SystemExit(f"⛔ 판 고정 입력에서 disk_io 줄을 정확히 하나 못 찾았다 ({t.count(old)})")
    return t.replace(old, f"    disk_io = '{disk_io}'")


def cmd_probe(xyz: Path, out: Path, *, pseudo_dir: str, k, disk_io: str, repo_root: Path) -> str:
    from ase.io import read
    mod = load_pinned(repo_root)
    a = read(str(xyz))
    t = pw_text(mod, a, prefix=f"probe_{Path(xyz).stem}_{disk_io}", calc="scf", k=k, pseudo_dir=pseudo_dir, disk_io=disk_io)
    Path(out).write_text(t)
    return t


# ----------------------------------------------------------------------------- selftest
def selftest() -> int:
    from ase import Atoms
    from ase.io import write
    n = bad = 0

    def chk(cond, msg):
        nonlocal n, bad
        n += 1
        if cond:
            print(f"  ✓ {msg}")
        else:
            bad += 1
            print(f"  ✗ {msg}")

    def refuses(f, *a, **kw):
        try:
            f(*a, **kw)
        except SystemExit:
            return True
        return False

    def toy(o_on_b=False, free_o=False, n_shell=4, edge=True):
        # 10 Å 입방 셀 · B 하나 (경계 근처 — 최소상 시험) · P 하나 · S 들 · O 셋
        L = 10.0
        sy, ps = [], []
        bx = 0.5 if edge else 5.0
        sy.append("B"); ps.append([bx, 5.0, 5.0])
        shell_dirs = [[-1.85, 0, 0], [0, 1.85, 0], [0, -1.85, 0], [0, 0, 1.85]][:n_shell]
        for v in shell_dirs:                         # -x 쪽은 경계 건너편 (x = 8.65)
            sy.append("S"); ps.append([(bx + v[0]) % L, 5.0 + v[1], 5.0 + v[2]])
        sy.append("P"); ps.append([5.0, 2.0, 2.0])
        for v in ([1.55, 0, 0], [0, 1.55, 0], [0, 0, 1.55]):
            sy.append("O"); ps.append([5.0 + v[0], 2.0 + v[1], 2.0 + v[2]])
        if o_on_b:
            ps[-1] = [bx, 5.0, 6.45]
        if free_o:
            ps[-1] = [8.0, 8.0, 8.0]
        sy += ["S", "Li", "Li"]; ps += [[2.0, 8.0, 2.0], [7.5, 7.5, 2.0], [2.0, 2.0, 7.5]]
        return Atoms(sy, positions=ps, cell=[L, L, L], pbc=True)

    print("— ob_combos")
    a = toy()
    cs = ob_combos(a)
    chk(len(cs) == 4, f"[양성] B 결합 S 4 개 → C(4,3) = 4 조합 (최소상 건너편 S 포함) — {len(cs)}")
    a2, info = cs[0]
    chk(composition(a2) == composition(a), "[양성] 조성 그대로 (O↔S 교환)")
    moved = set(info["o_from"]) | set(info["o_to"])
    same = all(np.allclose(a.get_positions()[i], a2.get_positions()[i]) for i in range(len(a)) if i not in moved)
    chk(same, "[양성] 옮긴 원자 6 개 밖은 좌표 그대로")
    b = 0
    dBO = sorted(a2.get_distance(b, j, mic=True) for j in info["o_to"])
    chk(all(abs(x - D_BO) < 1e-6 for x in dBO), f"[양성] 새 O 는 B 에서 {D_BO} Å — {np.round(dBO, 3).tolist()}")
    p = [i for i, s in enumerate(a.get_chemical_symbols()) if s == "P"][0]
    dPS = sorted(a2.get_distance(p, j, mic=True) for j in info["o_from"])
    chk(all(abs(x - D_PS) < 1e-6 for x in dPS), f"[양성] 새 S 는 P 에서 {D_PS} Å — {np.round(dPS, 3).tolist()}")
    chk(o_partners(a2) == ["B", "B", "B"] and o_partners(a) == ["P", "P", "P"], "[양성] 끝 꼴 판독: 시작 P·P·P → 짝 B·B·B")
    chk(refuses(ob_combos, toy(o_on_b=True)), "[음성] O 가 이미 B 에 붙음 → 멈춘다")
    bridge = Atoms("BOP", positions=[[0, 0, 0], [1.45, 0, 0], [3.0, 0, 0]], cell=[12, 12, 12], pbc=True)
    chk(any("B 에 붙어" in x for x in op_motif_problems(bridge)),
        "[음성] 다리 O (B–O–P · P 에도 붙음) 도 'B 에 붙음' 으로 잡는다")
    chk(refuses(ob_combos, toy(free_o=True)), "[음성] O 가 P 에 안 붙음 (자유 O) → 멈춘다")
    chk(refuses(ob_combos, toy(n_shell=2)), "[음성] B 결합 S 2 개 → 멈춘다")
    chk(refuses(ob_combos, toy(), expect_comp={"B": 2}), "[음성] 조성이 모델과 다름 → 멈춘다")
    chk(len(ob_combos(toy(edge=False))) == 4, "[양성] 경계에서 먼 B 도 같은 수")
    a_edge_nomic = toy()
    nb = _neighbors(a_edge_nomic, 0, "S", R_BS)
    chk(len(nb) == 4 and any(abs(x[2][0] + 1.85) < 1e-6 for x in nb), "[양성] 최소상: 경계 건너편 S 를 −x 벡터로 찾는다")
    crowd = toy(); crowd += Atoms("Li", positions=[[1.45, 5.0, 6.3]])    # 새 O (0.5, 5, 6.45) 에서 0.96 Å · 처음엔 모든 원자와 ≥ 1.0 Å
    chk(_min_pair(crowd) >= MIN_PAIR, "[전제] crowd 시작 구조는 최소 거리 ≥ 1.0 Å (음성 시험이 옮긴 원자를 잰다)")
    chk(refuses(ob_combos, crowd), "[음성] 옮긴 원자가 다른 원자와 1.0 Å 안 → 멈춘다")

    with tempfile.TemporaryDirectory() as td:
        T = Path(td)
        print("— ob_pairs (파일 · SHA256SUMS · manifest)")
        raw = T / "raw"; (raw / "structures").mkdir(parents=True)
        write(str(raw / "structures" / "BMP_00.xyz"), toy(), format="extxyz")
        write(str(raw / "structures" / "BMLi_00.xyz"), toy(edge=False), format="extxyz")
        (raw / "SHA256SUMS").write_text("".join(f"{sha256_file(raw / 'structures' / f)}  ./structures/{f}\n"
                                                for f in ("BMP_00.xyz", "BMLi_00.xyz")))
        man = cmd_ob_pairs(raw, T / "o1", bases=["BMP_00", "BMLi_00"], expect_comp=False)
        chk(man["n_files"] == 8 and "bases" not in man and man["purpose"] == PURPOSE_COMBO,
            "[양성] 조합 8 개 · manifest 에 'bases' 없음 (실행기 호환) · 목적 기록")
        okh = all(sha256_file(T / "o1" / r) == e["sha256"] for r, e in man["files"].items())
        chk(okh, "[양성] manifest sha256 = 실제 파일")
        chk(refuses(cmd_ob_pairs, raw, T / "o1", bases=["BMP_00"], expect_comp=False), "[음성] 비어 있지 않은 출력 폴더 → 덮지 않는다")
        (raw / "structures" / "BMP_00.xyz").write_text((raw / "structures" / "BMP_00.xyz").read_text() + " ")
        chk(refuses(cmd_ob_pairs, raw, T / "o2", bases=["BMP_00"], expect_comp=False), "[음성] 원본이 SHA256SUMS 와 다름 → 멈춘다")
        chk(refuses(cmd_ob_pairs, raw, T / "o3", bases=["BMP_09"], expect_comp=False), "[음성] SHA256SUMS 에 없는 바탕 → 멈춘다")

        print("— pick_ob")
        # 가짜 run_anneal 결과 — 조성 검사는 모델 조성이라 toy 는 못 통과 → 조성 함수 우회용 모델을 잠깐 바꾼다
        saved = dict(MODELS)
        MODELS["B-P"] = composition(toy()); MODELS["B-Li"] = composition(toy())
        try:
            res = T / "res"; res.mkdir()
            recs = []
            for rel, e in man["files"].items():
                nm = Path(rel).stem
                (res / nm).mkdir()
                shutil.copyfile(T / "o1" / rel, res / nm / "post_relax.xyz")
                k = int(nm.split("__c")[1])
                recs.append({"name": nm, "status": "converged", "E_post_relax": -100.0 + k * 0.1,
                             "outputs": {"post_relax": {"rel": f"{nm}/post_relax.xyz",
                                                        "sha256": sha256_file(res / nm / "post_relax.xyz")}}})
            def dump(rs):
                (res / "anneal_results.json").write_text(json.dumps({"time_ps": 0.0, "results": rs}))
            dump(recs)
            sel = cmd_pick_ob(T / "o1", res / "anneal_results.json", T / "p1")
            chk(sel["summary"]["BMP_00"]["chosen"] == "BMP_00__c00" and sel["summary"]["BMLi_00"]["chosen"] == "BMLi_00__c00",
                "[양성] 바탕마다 최저 (c00) 를 고른다")
            f0 = sel["files"]["ob_selected/BMP_00_OB.xyz"]
            chk(abs(f0["gap_to_second_eV"] - 0.1) < 1e-9 and f0["sha256"] == sha256_file(T / "p1" / "ob_selected" / "BMP_00_OB.xyz"),
                "[양성] 둘째와의 차 · 복사본 sha256 기록")
            chk(sel["purpose"] == PURPOSE_ANNEAL and "bases" not in sel, "[양성] 어닐 목적 · 'bases' 없음")
            r2 = [dict(r) for r in recs]; r2[0]["status"] = "unconverged"
            dump(r2)
            s2 = cmd_pick_ob(T / "o1", res / "anneal_results.json", T / "p2")
            b0 = r2[0]["name"].split("__")[0]
            chk(s2["summary"][b0]["chosen"] != r2[0]["name"] and s2["summary"][b0]["n_converged"] == 3
                and s2["summary"][b0]["n_not_converged"] == {"unconverged": 1},
                f"[양성] 미수렴 조합 ({r2[0]['name']}) 은 빼고 고른다 · 기록")
            dump(recs[1:])
            chk(refuses(cmd_pick_ob, T / "o1", res / "anneal_results.json", T / "p3"), "[음성] 조합 결과 누락 → 멈춘다 (누락 ≠ 실패)")
            r3 = [dict(r, status="failed") if r["name"].startswith("BMP_") else r for r in recs]
            dump(r3)
            chk(refuses(cmd_pick_ob, T / "o1", res / "anneal_results.json", T / "p4"), "[음성] 한 바탕의 조합이 전부 실패 → 멈춘다")
            r4 = [dict(r) for r in recs]; r4[0].pop("status")
            dump(r4)
            chk(refuses(cmd_pick_ob, T / "o1", res / "anneal_results.json", T / "p5"), "[음성] status 없는 옛 판 기록 → 멈춘다")
            dump(recs)
            (res / recs[0]["name"] / "post_relax.xyz").write_text("x")
            chk(refuses(cmd_pick_ob, T / "o1", res / "anneal_results.json", T / "p6"), "[음성] post_relax.xyz 가 기록 뒤 바뀜 → 멈춘다")
            r0 = man["files"][next(r for r in man["files"] if Path(r).stem == recs[0]["name"])]
            shutil.copyfile(T / "o1" / next(r for r in man["files"] if Path(r).stem == recs[0]["name"]),
                            res / recs[0]["name"] / "post_relax.xyz")
            chk(sha256_file(res / recs[0]["name"] / "post_relax.xyz") == r0["sha256"], "[전제] 바꾼 파일을 되돌렸다 (다음 음성 시험이 자기 조건만 잰다)")
            (res / "anneal_results.json").write_text(json.dumps({"time_ps": 20.0, "results": recs}))
            chk(refuses(cmd_pick_ob, T / "o1", res / "anneal_results.json", T / "p7"), "[음성] 이완만 (time_ps 0) 이 아닌 결과 → 멈춘다")
            dump(recs + [dict(recs[1])])
            chk(refuses(cmd_pick_ob, T / "o1", res / "anneal_results.json", T / "p8"), "[음성] 같은 이름 결과 둘 → 멈춘다")
            dump(recs + [dict(recs[1], name="ZZZ")])
            chk(refuses(cmd_pick_ob, T / "o1", res / "anneal_results.json", T / "p9"), "[음성] 조합 밖 이름 → 멈춘다")
        finally:
            MODELS.clear(); MODELS.update(saved)

        print("— probe (판 고정 입력 + disk_io 한 줄)")
        root = Path(__file__).resolve().parents[2]
        try:
            mod = load_pinned(root)
        except SystemExit as ex:
            mod = None
            chk(False, f"[양성] 판 고정 b2o3_bo_dft.py 불러오기 — {ex}")
        if mod is not None:
            from ase import Atoms as _A
            t_atoms = _A("LiPS4", positions=[[0, 0, 0], [2, 2, 2], [3, 2, 2], [2, 3, 2], [2, 2, 3], [1, 1, 1]][:6], cell=[6, 6, 6], pbc=True)
            t0 = mod.pw_input_text(t_atoms, prefix="x", calc="scf", k=[3, 3, 1], pseudo_dir="/pp")
            t1 = pw_text(mod, t_atoms, prefix="x", calc="scf", k=[3, 3, 1], pseudo_dir="/pp", disk_io="medium")
            d = [(x, y) for x, y in zip(t0.splitlines(), t1.splitlines()) if x != y]
            chk(len(d) == 1 and "disk_io = 'medium'" in d[0][1] and len(t0.splitlines()) == len(t1.splitlines()),
                "[양성] 판 고정 입력과 disk_io 한 줄만 다르다")
            chk("3 3 1 0 0 0" in t1, "[양성] k 격자 3 3 1")
            chk(refuses(pw_text, mod, t_atoms, prefix="x", calc="scf", k=[3, 3, 1], pseudo_dir="/pp", disk_io="fast"),
                "[음성] 모르는 disk_io → 멈춘다")
        fake = T / "fake_root"; (fake / "tools" / "doping").mkdir(parents=True)
        (fake / PINNED_DFT_REL).write_text("# 다른 판\n")
        chk(refuses(load_pinned, fake), "[음성] 판 고정 sha256 이 다르면 → 멈춘다")

    print(f"selftest {'PASS' if bad == 0 else 'FAIL'} ({n - bad}/{n})")
    return 0 if bad == 0 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sp = ap.add_subparsers(dest="cmd")
    a1 = sp.add_parser("ob_pairs"); a1.add_argument("--raw", required=True); a1.add_argument("--out", required=True)
    a2 = sp.add_parser("pick_ob"); a2.add_argument("--combos", required=True); a2.add_argument("--results", required=True)
    a2.add_argument("--out", required=True)
    a3 = sp.add_parser("probe"); a3.add_argument("--xyz", required=True); a3.add_argument("--out", required=True)
    a3.add_argument("--pseudo_dir", required=True); a3.add_argument("--k", type=int, nargs=3, default=[3, 3, 1])
    a3.add_argument("--disk_io", default="medium", choices=DISK_IO)
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.cmd == "ob_pairs":
        m = cmd_ob_pairs(Path(a.raw), Path(a.out))
        for base, p in m["parents"].items():
            print(f"  {base:8s} {p['site']:5s} B 결합 S {p['n_bshell_S']} · 조합 {p['n_combos']} · 나눔 {p['splits']} · 시작 O {p['start_o_partners']}")
        print(f"조합 {m['n_files']} 개 → {a.out}/manifest.json (N_EXPECT={m['n_files']})")
        return 0
    if a.cmd == "pick_ob":
        s = cmd_pick_ob(Path(a.combos), Path(a.results), Path(a.out))
        for rel, e in s["files"].items():
            g = e["gap_to_second_eV"]
            print(f"  {e['parent']:8s} ← {e['from_combo']} · 둘째와 {g if g is None else round(g, 3)} eV · 끝 O {e['end_o_partners']} · B {e['end_b_shells']}")
        print(f"고름 {len(s['files'])} 개 → {a.out}/manifest.json")
        return 0
    if a.cmd == "probe":
        root = Path(__file__).resolve().parents[2]
        cmd_probe(Path(a.xyz), Path(a.out), pseudo_dir=a.pseudo_dir, k=a.k, disk_io=a.disk_io, repo_root=root)
        print(f"프로브 입력 → {a.out} (disk_io {a.disk_io} · k {a.k})")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
