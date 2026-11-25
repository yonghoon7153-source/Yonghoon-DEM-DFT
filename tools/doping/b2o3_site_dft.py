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
  pick_dft  카드 4 단계_1 — 자리 × O 꼴 (출발 가족: 10월 O–P 후보 · 11월 O–B 짝) 마다 UMA 최저 셋 = DFT 단일점 12 를 고른다
            (10월 기록은 SHA256SUMS · 셀 · 조성으로 · 11월 어닐은 run_anneal.check_results 로 묶는다 · 끝 꼴은 기록만)
  sp_inputs pick_dft 가 고른 12 구조의 단일점 scf.in (UMA 구조 · 셀 그대로 · 판 고정 설정 · k 3 3 1 · disk_io 는 프로브로 고름)
            + sp_plan.json (입력 · 구조 · 판 고정 도구 · 유사포텐셜 sha256) — 실행은 tools/doping/run_force_check_scf.sh
  read_sp   카드 4 단계_1 판독 — 단일점 12 의 입력 결속 (G2 · 다시 만든 입력 sha256) · 수렴 (G1 · 판 고정 out_problems)
            → 자리마다 (두 O 꼴 합쳐) DFT 순위 · 단계_2 이완 후보 (최저 + 0.30 eV 안의 둘째) · G3 기록 (O–B − O–P) · 판정 아님
  probe     DFT 메모리 프로브 입력 — 9 단계 판 고정 b2o3_bo_dft.py (sha256 0c3b7f51…) 의 pw_input_text 를 그대로 쓰고
            disk_io 한 줄만 바꾼다 (disk_io 는 숫자에 영향 없음 — QE 설명서: nowf · low 는 파동함수를 메모리에 ·
            medium · high 는 k 점이 둘 이상이면 디스크에)
  --selftest  음성 경로 포함

이 도구가 못 하는 것 (한계 — 숨기지 않는다)
  · UMA · DFT 를 돌리지 않는다 (입력 · 고르기 · 단일점 판독만) · 형성 에너지 · D 를 내지 않는다 — read_sp 도 자리 사이
    단일점 에너지를 빼지 않는다 (조성이 다르다 · D 는 기준상 · 이온 이완 · 압력 어림 · k 탐침 뒤 · 카드 4).
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
from collections import Counter
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
PURPOSE_SP = "b2o3_site_dft/dft_single_point"
OP_RESULTS_REL = "uma_anneal_modelc10.anneal_results.json"   # 10월 O–P 후보 어닐 기록 (op_raw 안 · SHA256SUMS 에 있다)
ANNEAL_T_K, ANNEAL_TIME_PS, ANNEAL_DT_FS = 500.0, 20.0, 2.0   # 10월과 같은 어닐 (카드 1b)
RELAX_FMAX = 0.05
N_PER_FAMILY = 3                                               # 자리 × O 꼴마다 UMA 최저 셋 (카드 4 단계_1)
DISK_IO = ("nowf", "low", "medium", "high")
FAMILIES = ("O-P", "O-B")
KIND_SP_READ = "b2o3_site_dft_sp_read/v1"
SP_RELAX_WINDOW_EV = 0.30   # 카드 4 단계_2 — 자리마다 단일점 최저 + 둘째가 첫째와 셀 에너지 0.30 eV 안이면 둘째도


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


# ----------------------------------------------------------------------------- DFT 단일점 고르기
def _load_run_anneal(repo_root: Path):
    p = Path(repo_root) / "tools/doping/run_anneal.py"
    spec = importlib.util.spec_from_file_location("run_anneal_for_pick_dft", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def b_disp(a0, a1) -> list:
    """B 마다 시작 → 끝 변위 (Å · 분수좌표 최소상 · 끝 셀).

    B 원자 번호가 두 구조에서 같아야 한다 — O–B 짝은 O↔S 를 **원소 자리 바꿈**으로 만들어 O · S 열은 바뀌지만
    B 번호는 그대로다 (11-24 selftest 가 잡았다: 원소 열 전체를 같다고 요구하면 O–B 가족 전부가 멈춘다).
    """
    i0 = [i for i, s in enumerate(a0.get_chemical_symbols()) if s == "B"]
    i1 = [i for i, s in enumerate(a1.get_chemical_symbols()) if s == "B"]
    if len(a0) != len(a1) or i0 != i1 or not i0:
        raise SystemExit(f"⛔ 시작 · 끝 구조의 B 번호가 다르다 ({i0} · {i1}) — B 변위를 못 잰다")
    df = a1.get_scaled_positions(wrap=False)[i1] - a0.get_scaled_positions(wrap=False)[i0]
    df -= np.round(df)
    v = df @ np.asarray(a1.cell.array)
    return [round(float(np.linalg.norm(x)), 3) for x in v]


def end_motif(o_parts: list) -> str:
    """O 끝 꼴 이름: 셋 다 P 만 → 'O-P' · 셋 다 B 만 → 'O-B' · 그 밖 → 'mixed' (B·P 둘 다 · 섞임 · 자유 O)."""
    if all(x == "P" for x in o_parts):
        return "O-P"
    if all(x == "B" for x in o_parts):
        return "O-B"
    return "mixed"


def cmd_pick_dft(op_raw: Path, op_inputs: Path, ob_sel: Path, ob_results: Path, out: Path, *, repo_root: Path) -> dict:
    """카드 4_DFT_사다리 단계_1 — 자리 × O 꼴마다 UMA 최저 셋 = DFT 단일점 12 를 고른다 (결과 보기 전에 쓴 도구).

    O 꼴 = **출발 가족**이다 (카드 1b '예산: 자리마다 바탕 6 × O 꼴 2' · G3 'O–P 꼴만으로 낸 D' 가 가족별 고르기를 전제한다):
      O–P 가족 = 10월 후보 12 (op_raw · 500 K × 20 ps 어닐 + 셀 포함 이완) · O–B 가족 = 11월 짝 12 (ob_sel → 같은 어닐 · ob_results).
    끝 꼴 (O 결합 상대 · B 배위 · B 가 처음 자리에서 얼마나 움직였나) 은 끝 구조로 매겨 **기록만** 한다 —
    가족이 바뀐 듯 보여도 후보에서 빼거나 다른 가족으로 옮기지 않는다 (카드 1b 끝_꼴_기록).
    B 변위의 '처음 자리' = 10월 후보 입력 (치환 자리 · op_inputs) — 두 가족 다 B 배치를 거기서 물려받았다.

    묶는 법 (파일 ↔ 기록):
      O–P · SHA256SUMS 파일 해시 + 기록 cell_post 와 셀 일치 (1e-6 Å) + 원자 수 · 조성 · 10월 입력은 구조 해시 = 기록 input.
        (10월 기록의 post_relax 구조 해시는 쓰지 않는다 — 파일로 쓰고 다시 읽은 좌표의 자릿수가 달라 1e-6 반올림에서
         갈린다 · 11-24 실측 3/3 불일치 · 셀은 일치)
      O–B · run_anneal.check_results (상태 · 정체성 · time_ps 20 · 500 K · 수렴 · 목적 ob_anneal · 결과 파일 sha256) +
        어닐 입력 파일 sha256 = pick_ob 가 고른 파일.
    같은 UMA 처리: 두 실행의 uma_model_name · uma_task_name 이 같아야 한다 (다르면 멈춘다) · 판 (ase · torch) 은 기록.

    ⛔ 못 하는 것: UMA 에너지를 다시 계산하지 않는다 · 끝 꼴 이름은 1.8 Å 문턱 하나로 붙인다 (문턱 근처 결합은 갈릴 수 있다) ·
       10월 실행의 마찰 · fmax · 셀 필터는 10월 기록에 없어 대조하지 않는다 (11월 쪽만 정체성으로 본다).
    """
    from ase.io import read
    RA = _load_run_anneal(repo_root)
    op_raw, op_inputs, ob_sel, ob_results, out = map(Path, (op_raw, op_inputs, ob_sel, ob_results, out))
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"⛔ {out} 가 비어 있지 않다 — 덮지 않는다")
    rows = []
    # ── O–P 가족 (10월)
    sums = read_sums(op_raw)
    rrel = OP_RESULTS_REL
    if rrel not in sums or sha256_file(op_raw / rrel) != sums[rrel]:
        raise SystemExit(f"⛔ 10월 결과 {rrel} 가 SHA256SUMS 에 없거나 다르다")
    R0 = json.loads((op_raw / rrel).read_text())
    rec0 = {}
    for r in R0.get("results", []):
        if r.get("name") in rec0:
            raise SystemExit(f"⛔ 10월 결과에 같은 이름이 둘: {r.get('name')}")
        rec0[r.get("name")] = r
    for site, names in BASES.items():
        for nm in names:
            r = rec0.get(nm)
            if r is None:
                raise SystemExit(f"⛔ 10월 결과에 {nm} 가 없다")
            if (float(r.get("temperature_K", -1)), float(r.get("time_ps", -1)), float(r.get("dt_fs", -1))) != (ANNEAL_T_K, ANNEAL_TIME_PS, ANNEAL_DT_FS):
                raise SystemExit(f"⛔ {nm}: 10월 어닐 조건 {r.get('temperature_K')} K · {r.get('time_ps')} ps · {r.get('dt_fs')} fs ≠ 카드")
            if r.get("converged") is not True:
                raise SystemExit(f"⛔ {nm}: 10월 이완 미수렴 기록 — 게이트 G1 (후보 24 개 UMA 수렴) 을 못 넘는다")
            E = float(r.get("E_post_relax", float("nan")))
            if not np.isfinite(E):
                raise SystemExit(f"⛔ {nm}: 10월 에너지가 유한하지 않다")
            srel = f"structures/{nm}.xyz"
            if srel not in sums or sha256_file(op_raw / srel) != sums[srel]:
                raise SystemExit(f"⛔ {srel} 가 SHA256SUMS 에 없거나 다르다")
            a = read(str(op_raw / srel))
            if not np.allclose(np.asarray(a.cell.array), np.asarray(r["cell_post"], float), atol=1e-6):
                raise SystemExit(f"⛔ {nm}: 구조 파일의 셀 ≠ 기록 cell_post — 이완 끝 구조가 아니다")
            if composition(a) != dict(sorted(MODELS[site].items())) or len(a) != int(r.get("n_atoms", -1)):
                raise SystemExit(f"⛔ {nm}: 조성 · 원자 수가 모델 · 기록과 다르다")
            sub = "MP" if site == "B-P" else "MLi"
            s0 = op_inputs / sub / f"{nm}.xyz"
            if not s0.is_file():
                raise SystemExit(f"⛔ 10월 후보 입력 {s0} 가 없다")
            a0 = read(str(s0))
            if RA._struct_hash(a0)[:16] != r["struct_sha256"]["input"]:
                raise SystemExit(f"⛔ {nm}: 10월 후보 입력의 구조 해시 ≠ 기록 input")
            rows.append({"family": "O-P", "site": site, "base": nm, "name": nm, "E_uma_eV": E, "atoms": a, "start": a0,
                         "src": op_raw / srel, "src_sha256": sums[srel]})
    # ── O–B 가족 (11월 어닐)
    sel = json.loads((ob_sel / "manifest.json").read_text())
    if sel.get("schema") != "b2o3_site_dft_ob_selected/v1" or sel.get("purpose") != PURPOSE_ANNEAL:
        raise SystemExit("⛔ pick_ob 의 어닐 후보 manifest 가 아니다 (schema · purpose)")
    for rel, e in sel["files"].items():
        if sha256_file(ob_sel / rel) != e["sha256"]:
            raise SystemExit(f"⛔ 어닐 후보 파일이 manifest 뒤 바뀌었다: {rel}")
    n_ob = sum(len(v) for v in BASES.values())
    prob = RA.check_results(ob_results, expect_n=n_ob, expect_time_ps=ANNEAL_TIME_PS, expect_temperature=ANNEAL_T_K,
                            require_converged=True, expect_purpose=PURPOSE_ANNEAL)
    if prob:
        raise SystemExit("⛔ 어닐 결과 검사 (run_anneal.check_results): " + " · ".join(prob[:6]))
    R1 = json.loads(Path(ob_results).read_text())
    rec1 = {}
    for r in R1.get("results", []):
        if r.get("name") in rec1:
            raise SystemExit(f"⛔ 어닐 결과에 같은 이름이 둘: {r.get('name')}")
        rec1[r.get("name")] = r
    want = {f"{b}_OB" for v in BASES.values() for b in v}
    if set(rec1) != want:
        raise SystemExit(f"⛔ 어닐 결과 이름 {sorted(set(rec1) ^ want)[:6]} — 기대 {len(want)} 개와 다르다")
    for site, names in BASES.items():
        for base in names:
            nm = f"{base}_OB"
            r = rec1[nm]
            idn = r["identity"]
            fe = sel["files"].get(f"ob_selected/{nm}.xyz")
            if fe is None or idn.get("input_file_sha256") != fe["sha256"]:
                raise SystemExit(f"⛔ {nm}: 어닐 입력이 pick_ob 가 고른 파일이 아니다 (sha256)")
            if float(idn.get("dt_fs", -1)) != ANNEAL_DT_FS or float(idn.get("relax_fmax", -1)) != RELAX_FMAX or idn.get("cell_relax") is not True:
                raise SystemExit(f"⛔ {nm}: 어닐 정체성 dt {idn.get('dt_fs')} · fmax {idn.get('relax_fmax')} · 셀 {idn.get('cell_relax')} ≠ 카드")
            E = float(r.get("E_post_relax", float("nan")))
            if not np.isfinite(E):
                raise SystemExit(f"⛔ {nm}: 에너지가 유한하지 않다")
            p = Path(ob_results).parent / r["outputs"]["post_relax"]["rel"]
            a = read(str(p))
            if composition(a) != dict(sorted(MODELS[site].items())):
                raise SystemExit(f"⛔ {nm}: 조성이 모델과 다르다")
            a0 = read(str(op_inputs / ("MP" if site == "B-P" else "MLi") / f"{base}.xyz"))
            rows.append({"family": "O-B", "site": site, "base": base, "name": nm, "E_uma_eV": E, "atoms": a, "start": a0,
                         "src": p, "src_sha256": r["outputs"]["post_relax"]["sha256"]})
    # ── 같은 UMA 처리
    p0, p1 = R0.get("provenance") or {}, R1.get("provenance") or {}
    for k in ("uma_model_name", "uma_task_name"):
        if p0.get(k) is None or p0.get(k) != p1.get(k):
            raise SystemExit(f"⛔ 두 실행의 {k} 가 다르거나 없다: 10월 {p0.get(k)} · 11월 {p1.get(k)}")
    prov = {k: {"10월": p0.get(k), "11월": p1.get(k)} for k in ("uma_model_name", "uma_task_name", "ase_version", "torch_version", "hostname")}
    # ── 끝 꼴 · 고르기
    for x in rows:
        x["end_o_partners"] = o_partners(x["atoms"])
        x["end_b_shells"] = b_shells(x["atoms"])
        x["end_motif"] = end_motif(x["end_o_partners"])
        x["motif_changed"] = x["end_motif"] != x["family"]
        x["b_disp_from_site_A"] = b_disp(x["start"], x["atoms"])
    (out / "sp_selected").mkdir(parents=True, exist_ok=True)
    files, groups = {}, {}
    for site in BASES:
        for fam in ("O-P", "O-B"):
            g = sorted([x for x in rows if x["site"] == site and x["family"] == fam], key=lambda x: (x["E_uma_eV"], x["name"]))
            if len(g) < N_PER_FAMILY:
                raise SystemExit(f"⛔ {site} · {fam}: 후보 {len(g)} 개 < {N_PER_FAMILY}")
            e0 = g[0]["E_uma_eV"]
            groups[f"{site}|{fam}"] = [{"rank": i + 1, "name": x["name"], "dE_from_family_min_eV": round(x["E_uma_eV"] - e0, 4),
                                        "chosen": i < N_PER_FAMILY, "end_motif": x["end_motif"]} for i, x in enumerate(g)]
            for x in g[:N_PER_FAMILY]:
                rel = f"sp_selected/{x['name']}.xyz"
                shutil.copyfile(x["src"], out / rel)
                h = sha256_file(out / rel)
                if h != x["src_sha256"]:
                    raise SystemExit(f"⛔ {x['name']}: 복사본 sha256 ≠ 원본 기록")
                files[rel] = {"sha256": h, "site": site, "family": fam, "base": x["base"], "E_uma_eV": x["E_uma_eV"],
                              "end_o_partners": x["end_o_partners"], "end_b_shells": x["end_b_shells"],
                              "end_motif": x["end_motif"], "motif_changed": x["motif_changed"],
                              "b_disp_from_site_A": x["b_disp_from_site_A"]}
    cross = {}
    for site in BASES:
        mins = {fam: min(x["E_uma_eV"] for x in rows if x["site"] == site and x["family"] == fam) for fam in ("O-P", "O-B")}
        cross[site] = {"E_min_O-P_eV": mins["O-P"], "E_min_O-B_eV": mins["O-B"], "O-B_minus_O-P_eV": round(mins["O-B"] - mins["O-P"], 4)}
    allrows = [{k: v for k, v in x.items() if k not in ("atoms", "start", "src")} | {"src": str(x["src"])} for x in rows]
    man = {"schema": "b2o3_site_dft_sp_selected/v1", "purpose": PURPOSE_SP, "card": CARD, "decision": DECISION,
           "tool": {"path": "tools/doping/b2o3_site_dft.py", "sha256": tool_sha()},
           "rule": {"N_PER_FAMILY": N_PER_FAMILY, "grouping": "출발 가족 (O–P = 10월 후보 · O–B = 11월 짝) · 끝 꼴은 기록만",
                    "R_XO_A": R_XO, "R_BS_A": R_BS},
           "inputs": {"op_results_sha256": sums[rrel], "op_SHA256SUMS_sha256": sha256_file(op_raw / "SHA256SUMS"),
                      "ob_selected_manifest_sha256": sha256_file(ob_sel / "manifest.json"),
                      "ob_results_sha256": sha256_file(ob_results)},
           "provenance": prov, "groups": groups, "cross_family_uma": cross,
           "⚠_읽는_법": "UMA 에너지 차는 고르기용이지 판정이 아니다 (판정은 DFT 이완 뒤 · 카드 4) · 자리 사이 (B-P 대 B-Li) 에너지는 조성이 달라 여기서 비교하지 않는다",
           "rows": allrows, "files": files}
    (out / "manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    return man


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


def cmd_sp_inputs(sp_pick: Path, out: Path, *, pseudo_dir: str, disk_io: str, repo_root: Path, k=(3, 3, 1)) -> dict:
    """카드 4 단계_1 — pick_dft 가 고른 12 구조의 DFT 단일점 입력 (UMA 구조 · UMA 셀 그대로 · 9 단계 판 고정 설정).

    출력 = <out>/<이름>/scf.in (run_force_check_scf.sh 가 그대로 도는 꼴) + <out>/sp_plan.json
    (입력 sha256 · 구조 sha256 · 판 고정 도구 sha256 · 유사포텐셜 sha256 · md5 · z_valence · k · disk_io).
    입력은 결정론이다 — 판독기가 같은 인자로 다시 만들어 sha256 으로 대조한다.
    ⛔ 못 하는 것: pw.x 를 돌리지 않는다 · disk_io 는 메모리 프로브 결과로 사람이 고른다 (숫자에는 영향 없음 ·
       9 단계 단일점은 gabia nowf) · 셀을 기준 셀로 옮기지 않는다 (단일점은 UMA 셀 그대로 — 기준 셀은 단계_2 이완).
    """
    from ase.io import read
    mod = load_pinned(repo_root)
    sp_pick, out = Path(sp_pick), Path(out)
    man = json.loads((sp_pick / "manifest.json").read_text())
    if man.get("schema") != "b2o3_site_dft_sp_selected/v1" or man.get("purpose") != PURPOSE_SP:
        raise SystemExit("⛔ pick_dft 의 단일점 manifest 가 아니다 (schema · purpose)")
    want = len(BASES) * 2 * N_PER_FAMILY
    if len(man.get("files", {})) != want:
        raise SystemExit(f"⛔ 고른 구조 {len(man.get('files', {}))} 개 ≠ {want}")
    for rel, e in man["files"].items():
        if sha256_file(sp_pick / rel) != e["sha256"]:
            raise SystemExit(f"⛔ 고른 구조 파일이 manifest 뒤 바뀌었다: {rel}")
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"⛔ {out} 가 비어 있지 않다 — 덮지 않는다")
    pp = mod.pseudo_record(pseudo_dir)
    jobs = {}
    for rel, e in sorted(man["files"].items()):
        nm = Path(rel).stem
        a = read(str(sp_pick / rel))
        if composition(a) != dict(sorted(MODELS[e["site"]].items())):
            raise SystemExit(f"⛔ {nm}: 조성이 모델과 다르다")
        t = pw_text(mod, a, prefix=f"sp_{nm}", calc="scf", k=list(k), pseudo_dir=pseudo_dir, disk_io=disk_io)
        (out / nm).mkdir(parents=True)
        (out / nm / "scf.in").write_text(t)
        jobs[nm] = {"scf_in_sha256": sha256_file(out / nm / "scf.in"), "xyz": rel, "xyz_sha256": e["sha256"],
                    "site": e["site"], "family": e["family"], "base": e["base"], "E_uma_eV": e["E_uma_eV"],
                    "end_motif": e["end_motif"], "nat": len(a)}
    plan = {"schema": "b2o3_site_dft_sp_plan/v1", "purpose": PURPOSE_SP, "card": CARD, "decision": DECISION,
            "tool": {"path": "tools/doping/b2o3_site_dft.py", "sha256": tool_sha()},
            "pinned_dft": {"path": PINNED_DFT_REL, "sha256": PINNED_DFT_SHA},
            "settings": {"calc": "scf", "k": list(k), "disk_io": disk_io, "tstress": False, "cell": "UMA 셀 그대로",
                         "DFT": {kk: mod.DFT[kk] for kk in ("ecutwfc", "ecutrho", "smearing", "degauss", "nspin", "conv_thr",
                                                            "mixing_mode", "mixing_beta", "electron_maxstep", "diagonalization")}},
            "pseudo": pp, "sp_pick_manifest_sha256": sha256_file(sp_pick / "manifest.json"), "jobs": jobs}
    (out / "sp_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1) + "\n")
    return plan


def cmd_probe(xyz: Path, out: Path, *, pseudo_dir: str, k, disk_io: str, repo_root: Path) -> str:
    from ase.io import read
    mod = load_pinned(repo_root)
    a = read(str(xyz))
    t = pw_text(mod, a, prefix=f"probe_{Path(xyz).stem}_{disk_io}", calc="scf", k=k, pseudo_dir=pseudo_dir, disk_io=disk_io)
    Path(out).write_text(t)
    return t


def cmd_read_sp(sp_dft: Path, sp_pick: Path, out: Path, *, pseudo_dir: str, repo_root: Path) -> dict:
    """카드 4 단계_1 판독 — 단일점 12 의 결속 (G2) · 수렴 (G1) → 자리마다 DFT 순위 · 단계_2 이완 후보. **판정 아님**.

    G2: sp_plan.json 의 입력 sha256 = 폴더의 scf.in = 같은 인자로 다시 만든 입력 (cmd_sp_inputs · 임시 폴더) ·
        sp_pick manifest sha256 · 유사포텐셜 기록이 계획과 같아야 한다 · 계획에 없는 잡 폴더가 없어야 한다 — 하나라도 어긋나면 멈춘다.
    G1: 잡마다 scf.out 을 판 고정 b2o3_bo_dft.py 의 parse_pw_out · out_problems (stage 'sp') 로 본다 — 한 실행 · JOB DONE 한 번 ·
        SCF 수렴 · QE 판 · 설정 · 유사포텐셜 md5 · Zval · 전자 수 · 셀 · 처음 좌표 · k 격자. 원자 수만 잡의 계획값 (B-P 128 · B-Li 120) 으로 본다.
        누락이 하나라도 있으면 판독하지 않는다 (누락 ≠ 실패 · 다 돈 뒤) · 검사 실패가 하나라도 있으면 판독하지 않는다 (카드 게이트 G1).
    출력: 자리마다 (두 O 꼴 합쳐) DFT 에너지 순위 · 최저와의 차 (eV/셀) · 단계_2 이완 후보 (최저 + 0.30 eV 안의 둘째) ·
        G3 기록 (자리마다 O–B 최저 − O–P 최저 · eV/셀) · UMA 순서와 DFT 순서 (기록만).
    ⛔ 못 하는 것: D (자리 사이 형성 에너지 차) 를 내지 않는다 — 기준상 (Li₂S · Li₃PS₄) · 이온 이완 · 압력 어림 · k 탐침 뒤 (카드 4) ·
       자리 사이 단일점 에너지를 빼지 않는다 (조성이 다르다) · 출력을 고치거나 다시 돌리지 않는다 · 결과 파일을 덮어쓰지 않는다 ·
       다시 만든 입력은 지금 도구 코드로 만든다 (판 고정 b2o3_bo_dft.py 는 sha256 으로 묶였다 · 이 파일이 바뀌면 그 차이가 G2 로 드러난다).
    """
    mod = load_pinned(repo_root)
    sp_dft, sp_pick, out = Path(sp_dft), Path(sp_pick), Path(out)
    if out.exists():
        raise SystemExit(f"⛔ {out} 가 이미 있다 — 덮지 않는다")
    pf = sp_dft / "sp_plan.json"
    if not pf.is_file():
        raise SystemExit(f"⛔ {pf} 가 없다")
    plan = json.loads(pf.read_text())
    if plan.get("schema") != "b2o3_site_dft_sp_plan/v1" or plan.get("purpose") != PURPOSE_SP or plan.get("card") != CARD:
        raise SystemExit("⛔ sp_inputs 의 단일점 계획이 아니다 (schema · purpose · card)")
    jobs = plan.get("jobs") or {}
    want = len(BASES) * len(FAMILIES) * N_PER_FAMILY
    if len(jobs) != want:
        raise SystemExit(f"⛔ 계획의 잡 {len(jobs)} 개 ≠ {want}")
    cnt = Counter((j.get("site"), j.get("family")) for j in jobs.values())
    if set(cnt) != {(s, f) for s in BASES for f in FAMILIES} or any(c != N_PER_FAMILY for c in cnt.values()):
        raise SystemExit(f"⛔ 자리 × O 꼴마다 {N_PER_FAMILY} 개가 아니다: {dict(cnt)}")
    if not (sp_pick / "manifest.json").is_file() or sha256_file(sp_pick / "manifest.json") != plan.get("sp_pick_manifest_sha256"):
        raise SystemExit("⛔ sp_pick manifest 가 없거나 계획을 만든 뒤 바뀌었다 (sha256)")
    pp = mod.pseudo_record(pseudo_dir)
    if pp != plan.get("pseudo"):
        raise SystemExit("⛔ 유사포텐셜 기록이 계획과 다르다 (파일 · sha256 · md5 · z_valence)")
    extra = sorted(d.name for d in sp_dft.iterdir() if d.is_dir() and (d / "scf.in").exists() and d.name not in jobs)
    if extra:
        raise SystemExit(f"⛔ 계획에 없는 잡 폴더 {extra}")
    with tempfile.TemporaryDirectory() as td:
        re_plan = cmd_sp_inputs(sp_pick, Path(td) / "re", pseudo_dir=pseudo_dir, disk_io=plan["settings"]["disk_io"],
                                repo_root=repo_root, k=tuple(plan["settings"]["k"]))
    if set(re_plan["jobs"]) != set(jobs):
        raise SystemExit("⛔ 다시 만든 입력의 잡 이름이 계획과 다르다")
    g2 = []
    for nm, j in sorted(jobs.items()):
        fin = sp_dft / nm / "scf.in"
        if not fin.is_file() or sha256_file(fin) != j["scf_in_sha256"]:
            g2.append(f"{nm}: 폴더의 scf.in 이 계획과 다르다 · 없다")
        elif re_plan["jobs"][nm]["scf_in_sha256"] != j["scf_in_sha256"]:
            g2.append(f"{nm}: 같은 인자로 다시 만든 입력이 계획과 다르다")
    if g2:
        raise SystemExit("⛔ G2 입력 결속 실패 — 판독하지 않는다:\n  " + "\n  ".join(g2))
    missing, bad, rows = [], [], []
    nat0 = mod.DFT["nat"]
    try:
        for nm, j in sorted(jobs.items()):
            fout = sp_dft / nm / "scf.out"
            if not fout.is_file():
                missing.append(nm)
                continue
            o = mod.parse_pw_out(fout)
            mod.DFT["nat"] = j["nat"]          # 자리마다 원자 수가 다르다 — 원자 수 줄만 잡의 계획값으로 본다
            q = mod.out_problems(o, mod.parse_pw_in(sp_dft / nm / "scf.in"), stage="sp", pp=pp["files"])
            if q:
                bad.append(f"{nm}: " + " · ".join(q[:3]))
                continue
            rows.append({"name": nm, "site": j["site"], "family": j["family"], "base": j["base"],
                         "E_Ry": o["E_Ry"], "E_eV": o["E_Ry"] * mod.RY_EV, "E_uma_eV": j["E_uma_eV"],
                         "end_motif": j["end_motif"], "nat": j["nat"], "nk": o["nk"], "scf_out_sha256": sha256_file(fout)})
    finally:
        mod.DFT["nat"] = nat0
    if missing:
        raise SystemExit(f"⛔ 단일점 출력 누락 {len(missing)} 건 ({missing}) — 누락은 실패가 아니다 · 다 돈 뒤 판독한다")
    if bad:
        raise SystemExit(f"⛔ G1 단일점 출력 검사 실패 {len(bad)} 건 — 판독하지 않는다 (카드 게이트 G1):\n  " + "\n  ".join(bad))
    sites = {}
    for s in BASES:
        r = sorted((x for x in rows if x["site"] == s), key=lambda x: (x["E_eV"], x["name"]))
        e0 = r[0]["E_eV"]
        for x in r:
            x["dE_site_min_eV"] = x["E_eV"] - e0
        gap = r[1]["E_eV"] - e0
        fam_min = {f: min(x["E_eV"] for x in r if x["family"] == f) for f in FAMILIES}
        sites[s] = {"dft_order": [x["name"] for x in r],
                    "uma_order": [x["name"] for x in sorted(r, key=lambda x: (x["E_uma_eV"], x["name"]))],
                    "relax_pick": [r[0]["name"]] + ([r[1]["name"]] if gap <= SP_RELAX_WINDOW_EV else []),
                    "second_gap_eV": gap, "lowest_family": r[0]["family"],
                    "family_min_eV": fam_min, "O-B_minus_O-P_eV": fam_min["O-B"] - fam_min["O-P"]}
    v = {"kind": KIND_SP_READ, "card": CARD, "decision": DECISION,
         "tool": {"path": "tools/doping/b2o3_site_dft.py", "sha256": tool_sha()},
         "pinned_dft": {"path": PINNED_DFT_REL, "sha256": PINNED_DFT_SHA},
         "plan": {"path": str(pf), "sha256": sha256_file(pf), "tool_sha256_at_inputs": (plan.get("tool") or {}).get("sha256")},
         "gates": {"G1": f"단일점 {len(rows)}/{want} — 출력 검사 (판 고정 out_problems · stage sp) 통과",
                   "G2": f"입력 {want} = 계획 = 같은 인자로 다시 만든 입력 (sha256) · sp_pick manifest · 유사포텐셜 같음"},
         "relax_window_eV": SP_RELAX_WINDOW_EV, "rows": sorted(rows, key=lambda x: (x["site"], x["E_eV"])), "sites": sites,
         "판정_아님": "자리 사이 D 는 기준상 · 이온 이완 · 압력 어림 · k 탐침 뒤에만 낸다 (카드 4) — 단일점 에너지를 자리 사이에서 빼지 않는다 (조성이 다르다)",
         "next": "단계_2 — 자리마다 relax_pick 을 고정 기준 셀 (V₀ 2436.33 Å³ · 등방 스케일) 로 옮겨 이온 이완 (카드 4 · 입력 도구는 따로)"}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n")
    return v


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

        print("— pick_dft (가족별 최저 셋 · 묶음 검사 · 끝 꼴은 기록만)")
        root = Path(__file__).resolve().parents[2]
        RA = _load_run_anneal(root)
        saved_m, saved_b = dict(MODELS), {k: list(v) for k, v in BASES.items()}
        MODELS["B-P"] = composition(toy()); MODELS["B-Li"] = composition(toy())
        BASES.clear(); BASES.update({"B-P": [f"BMP_{i:02d}" for i in range(4)], "B-Li": [f"BMLi_{i:02d}" for i in range(4)]})
        E_OP = {0: -100.0, 1: -100.3, 2: -100.1, 3: -100.2}       # 최저 셋 = 1 · 3 · 2 (0 은 빠진다)
        E_OB = {0: -100.25, 1: -100.05, 2: -100.15, 3: -100.35}   # 최저 셋 = 3 · 0 · 2 (1 은 빠진다)

        def build(D, mut=lambda k, o: o):
            """가짜 10월 (op_raw · op_inputs) + 11월 (ob_sel · ob_results) 묶음. mut(key, obj) 로 한 곳만 망가뜨린다."""
            opr, opi, obs, obr = D / "op_raw", D / "op_inputs", D / "ob_sel", D / "ob_res"
            for p in (opr / "structures", opi / "MP", opi / "MLi", obs / "ob_selected", obr):
                p.mkdir(parents=True)
            recs0, recs1, sums = [], [], {}
            for site, names in BASES.items():
                for i, nm in enumerate(names):
                    k = int(nm.split("_")[1])
                    start = toy(edge=False)
                    write(str(opi / ("MP" if site == "B-P" else "MLi") / f"{nm}.xyz"), start, format="extxyz")
                    fin = start.copy(); fin.positions[0] += [0.3, 0, 0]       # B 0.3 Å 이동
                    if nm == "BMP_01":
                        fin = ob_combos(start)[0][0]                          # O–P 가족인데 끝 꼴이 O–B (기록만 · 안 뺀다)
                    fin = mut(("op_fin", nm), fin)
                    write(str(opr / "structures" / f"{nm}.xyz"), fin, format="extxyz")
                    sums[f"structures/{nm}.xyz"] = sha256_file(opr / "structures" / f"{nm}.xyz")
                    recs0.append(mut(("op_rec", nm), {"name": nm, "temperature_K": 500.0, "time_ps": 20.0, "dt_fs": 2.0,
                                                      "converged": True, "E_post_relax": E_OP[k], "n_atoms": len(fin),
                                                      "cell_post": fin.cell.array.tolist(),
                                                      "struct_sha256": {"input": RA._struct_hash(start)[:16]}}))
                    ob = ob_combos(start)[0][0]
                    write(str(obs / "ob_selected" / f"{nm}_OB.xyz"), ob, format="extxyz")
                    (obr / f"{nm}_OB").mkdir()
                    for kk in ("post_md", "post_relax"):
                        write(str(obr / f"{nm}_OB" / f"{kk}.xyz"), ob, format="extxyz")
                    idn = {"n_atoms": len(ob), "time_ps": 20.0, "temperature_K": 500.0, "dt_fs": 2.0, "relax_fmax": 0.05,
                           "cell_relax": True, "purpose": PURPOSE_ANNEAL,
                           "input_file_sha256": sha256_file(obs / "ob_selected" / f"{nm}_OB.xyz")}
                    recs1.append(mut(("ob_rec", nm), {
                        "name": f"{nm}_OB", "status": "converged", "identity": idn, "E_post_relax": E_OB[k],
                        "outputs": {kk: {"rel": f"{nm}_OB/{kk}.xyz", "sha256": sha256_file(obr / f"{nm}_OB" / f"{kk}.xyz")}
                                    for kk in ("post_md", "post_relax")}}))
            prov = {"uma_model_name": "uma-s-1p1", "uma_task_name": "omat", "ase_version": "3.29.0"}
            (opr / OP_RESULTS_REL).write_text(json.dumps({"provenance": prov, "results": recs0}))
            sums[OP_RESULTS_REL] = sha256_file(opr / OP_RESULTS_REL)
            mut(("op_after", None), opr)
            (opr / "SHA256SUMS").write_text("".join(f"{h}  ./{r}\n" for r, h in sums.items()))
            mut(("op_tamper", None), opr)
            files = {f"ob_selected/{p.name}": {"sha256": sha256_file(p)} for p in sorted((obs / "ob_selected").iterdir())}
            (obs / "manifest.json").write_text(json.dumps({"schema": "b2o3_site_dft_ob_selected/v1", "purpose": PURPOSE_ANNEAL,
                                                            "files": files}))
            (obr / "anneal_results.json").write_text(json.dumps({"provenance": mut(("ob_prov", None), dict(prov)),
                                                                 "results": recs1}))
            mut(("ob_after", None), obr)
            return opr, opi, obs, obr / "anneal_results.json"

        def run(D, mut=lambda k, o: o, out=None):
            a_ = build(D, mut)
            return cmd_pick_dft(*a_, out or D / "out", repo_root=root)

        try:
            m = run(T / "d1")
            ch = {f["family"] + ":" + f["base"] for f in m["files"].values()}
            chk(len(m["files"]) == 12, f"[양성] 자리 2 × 가족 2 × 셋 = 12 — {len(m['files'])}")
            chk({"O-P:BMP_01", "O-P:BMP_03", "O-P:BMP_02"} <= ch and "O-P:BMP_00" not in ch,
                "[양성] O–P 가족 최저 셋 (1 · 3 · 2) · 넷째 (0) 는 뺀다")
            chk({"O-B:BMP_03", "O-B:BMP_00", "O-B:BMP_02"} <= ch and "O-B:BMP_01" not in ch,
                "[양성] O–B 가족은 따로 고른다 (3 · 0 · 2)")
            f01 = m["files"]["sp_selected/BMP_01.xyz"]
            chk(f01["family"] == "O-P" and f01["end_motif"] == "O-B" and f01["motif_changed"] is True,
                "[양성] 끝 꼴이 바뀐 후보는 기록만 하고 출발 가족에 남긴다 (안 뺀다)")
            f03 = m["files"]["sp_selected/BMP_03.xyz"]
            chk(f03["b_disp_from_site_A"] == [0.3] and f03["sha256"] == sha256_file(T / "d1" / "out" / "sp_selected" / "BMP_03.xyz"),
                "[양성] B 변위 (치환 자리 → 끝) 0.3 Å · 복사본 sha256")
            chk(abs(m["cross_family_uma"]["B-P"]["O-B_minus_O-P_eV"] - (-100.35 + 100.3)) < 1e-9 and m["purpose"] == PURPOSE_SP,
                "[양성] 가족 사이 UMA 최저 차 기록 · 목적 dft_single_point")
            a_edge = toy(); b_edge = a_edge.copy(); b_edge.positions[0] = [9.8, 5.0, 5.0]
            chk(b_disp(a_edge, b_edge) == [0.7], "[양성] B 변위는 최소상 (0.5 → 9.8 Å = 0.7 Å)")

            def neg(tag, mut, msg):
                chk(refuses(run, T / tag, mut), f"[음성] {msg} → 멈춘다")

            neg("n1", lambda k, o: (o / OP_RESULTS_REL).write_text((o / OP_RESULTS_REL).read_text() + " ") or o
                if k[0] == "op_tamper" else o, "10월 결과 JSON 이 SHA256SUMS 뒤 바뀜")
            neg("n2", lambda k, o: dict(o, cell_post=(np.asarray(o["cell_post"]) * 1.01).tolist())
                if k == ("op_rec", "BMP_02") else o, "10월 구조 셀 ≠ 기록 cell_post")
            neg("n3", lambda k, o: dict(o, converged=False) if k == ("op_rec", "BMLi_01") else o, "10월 미수렴 기록 (G1)")
            neg("n4", lambda k, o: dict(o, name="ZZ_99") if k == ("op_rec", "BMLi_03") else o, "10월 결과에 바탕 누락")
            neg("n5", lambda k, o: dict(o, struct_sha256={"input": "0" * 16}) if k == ("op_rec", "BMP_00") else o,
                "10월 후보 입력 구조 해시 ≠ 기록")
            neg("n6", lambda k, o: dict(o, status="unconverged") if k == ("ob_rec", "BMP_02") else o, "어닐 미수렴")
            neg("n7", lambda k, o: dict(o, identity=dict(o["identity"], purpose="other")) if k == ("ob_rec", "BMLi_00") else o,
                "어닐 실행 목적이 다름")
            neg("n8", lambda k, o: dict(o, identity=dict(o["identity"], input_file_sha256="0" * 64)) if k == ("ob_rec", "BMP_03") else o,
                "어닐 입력이 고른 파일이 아님")
            neg("n9", lambda k, o: dict(o, name="BMP_09_OB") if k == ("ob_rec", "BMP_01") else o, "어닐 결과 이름이 기대 밖")
            neg("n10", lambda k, o: dict(o, uma_model_name="uma-m-1p1") if k[0] == "ob_prov" else o, "두 실행의 UMA 모델이 다름")
            neg("n11", lambda k, o: dict(o, E_post_relax=float("nan")) if k == ("op_rec", "BMLi_02") else o, "에너지가 NaN")
            neg("n12", lambda k, o: dict(o, identity=dict(o["identity"], relax_fmax=0.1)) if k == ("ob_rec", "BMLi_03") else o,
                "어닐 이완 fmax 가 카드와 다름")
            neg("n13", lambda k, o: (o + Atoms("Li", positions=[[9.0, 9.0, 9.0]])) if k == ("op_fin", "BMLi_00") else o,
                "10월 구조 조성이 모델과 다름")
            (T / "n14" / "out").mkdir(parents=True); (T / "n14" / "out" / "x").write_text("x")
            chk(refuses(run, T / "n14"), "[음성] 비어 있지 않은 출력 폴더 → 덮지 않는다")
        finally:
            MODELS.clear(); MODELS.update(saved_m)
            BASES.clear(); BASES.update(saved_b)

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

            print("— sp_inputs (단일점 12 입력 · 판 고정 설정 · 결정론)")
            pdir = T / "pp"; pdir.mkdir()
            for el in mod.SPECIES:
                mod._write_fake_pp(pdir, el)
            saved_m2 = dict(MODELS)
            MODELS["B-P"] = composition(toy()); MODELS["B-Li"] = composition(toy())
            try:
                def mk_pick(D, n=12, tamper=False, schema="b2o3_site_dft_sp_selected/v1"):
                    (D / "sp_selected").mkdir(parents=True)
                    files = {}
                    for i in range(n):
                        site = "B-P" if i < n // 2 else "B-Li"
                        rel = f"sp_selected/X{i:02d}.xyz"
                        write(str(D / rel), toy(edge=False), format="extxyz")
                        files[rel] = {"sha256": sha256_file(D / rel), "site": site, "family": "O-P" if i % 2 else "O-B",
                                      "base": f"X{i:02d}", "E_uma_eV": -100.0 - i, "end_motif": "O-P"}
                    if tamper:
                        (D / "sp_selected" / "X00.xyz").write_text((D / "sp_selected" / "X00.xyz").read_text() + " ")
                    (D / "manifest.json").write_text(json.dumps({"schema": schema, "purpose": PURPOSE_SP, "files": files}))
                    return D
                pk = mk_pick(T / "pk1")
                pl = cmd_sp_inputs(pk, T / "sp1", pseudo_dir=str(pdir), disk_io="medium", repo_root=root)
                t00 = (T / "sp1" / "X00" / "scf.in").read_text()
                chk(len(pl["jobs"]) == 12 and all((T / "sp1" / j / "scf.in").is_file() for j in pl["jobs"]),
                    "[양성] 잡 12 개 · 잡마다 scf.in (run_force_check_scf.sh 꼴)")
                chk("calculation = 'scf'" in t00 and "disk_io = 'medium'" in t00 and "3 3 1 0 0 0" in t00 and "tstress" not in t00,
                    "[양성] scf · disk_io medium · k 3 3 1 · tstress 없음 (9 단계 단일점과 같다)")
                from ase.io import read as _rd
                again = pw_text(mod, _rd(str(pk / "sp_selected" / "X00.xyz")), prefix="sp_X00", calc="scf", k=[3, 3, 1],
                                pseudo_dir=str(pdir), disk_io="medium")
                chk(again == t00 and pl["jobs"]["X00"]["scf_in_sha256"] == sha256_file(T / "sp1" / "X00" / "scf.in"),
                    "[양성] 결정론 — 같은 인자로 다시 만들면 같은 바이트 · sha256 기록")
                chk(pl["pinned_dft"]["sha256"] == PINNED_DFT_SHA and set(pl["pseudo"]["files"]) == set(mod.SPECIES),
                    "[양성] 판 고정 도구 sha256 · 유사포텐셜 6 개 기록")
                chk(refuses(cmd_sp_inputs, mk_pick(T / "pk2", n=11), T / "sp2", pseudo_dir=str(pdir), disk_io="medium", repo_root=root),
                    "[음성] 고른 구조가 12 개가 아님 → 멈춘다")
                chk(refuses(cmd_sp_inputs, mk_pick(T / "pk3", tamper=True), T / "sp3", pseudo_dir=str(pdir), disk_io="medium", repo_root=root),
                    "[음성] 고른 구조 파일이 manifest 뒤 바뀜 → 멈춘다")
                chk(refuses(cmd_sp_inputs, mk_pick(T / "pk4", schema="x"), T / "sp4", pseudo_dir=str(pdir), disk_io="medium", repo_root=root),
                    "[음성] pick_dft manifest 가 아님 → 멈춘다")
                chk(refuses(cmd_sp_inputs, pk, T / "sp1", pseudo_dir=str(pdir), disk_io="medium", repo_root=root),
                    "[음성] 비어 있지 않은 출력 폴더 → 덮지 않는다")
                chk(refuses(cmd_sp_inputs, pk, T / "sp5", pseudo_dir=str(T / "no_pp"), disk_io="medium", repo_root=root),
                    "[음성] 유사포텐셜 폴더가 없음 → 멈춘다")
                chk(refuses(cmd_sp_inputs, pk, T / "sp6", pseudo_dir=str(pdir), disk_io="fast", repo_root=root),
                    "[음성] 모르는 disk_io → 멈춘다")
                print("— read_sp (단일점 판독 · G2 결속 · G1 수렴 · 자리 안 순위 · 이완 후보 · 판정 아님)")
                E0 = {"X00": -1000.00, "X01": -1000.40, "X02": -1000.15, "X03": -999.90, "X04": -1000.20, "X05": -999.80,
                      "X06": -900.00, "X07": -899.50, "X08": -899.60, "X09": -899.55, "X10": -899.65, "X11": -899.40}

                def fresh(tag, Emap=None, skip=(), kw_by=None):
                    D = T / f"rs_{tag}"
                    shutil.copytree(T / "sp1", D)
                    for nm in pl["jobs"]:
                        if nm in skip:
                            continue
                        txt = mod._fake_out(D / nm / "scf.in", E_list=[(Emap or E0)[nm]], stage="sp",   # _fake_out 은 eV 를 받아 Ry 로 찍는다
                                            pp=pl["pseudo"]["files"], **(kw_by or {}).get(nm, {}))
                        (D / nm / "scf.out").write_text(txt)
                    return D

                def rs(D, out_name, sp_pick=None, pseudo=None):
                    return cmd_read_sp(D, sp_pick or pk, T / out_name, pseudo_dir=str(pseudo or pdir), repo_root=root)

                def try_rs(D, out_name, **kw):     # 양성 호출 — 멈추면 실패 하나로 센다 (selftest 가 중간에 끊기지 않게)
                    try:
                        return rs(D, out_name, **kw)
                    except SystemExit as ex:
                        chk(False, f"[양성] 정상 출력인데 판독이 멈췄다 — {str(ex)[:120]}")
                        return {"sites": {s: {} for s in BASES}, "rows": []}

                D0 = fresh("ok")
                v = try_rs(D0, "rs_ok.json")
                chk(v["sites"]["B-P"].get("relax_pick") == ["X01", "X04"] and v["sites"]["B-Li"].get("relax_pick") == ["X06"],
                    "[양성] 이완 후보 = 자리마다 최저 + 0.30 eV 안의 둘째 (B-P 둘 · B-Li 하나)")
                chk(abs(v["sites"]["B-P"].get("O-B_minus_O-P_eV", 9) - 0.20) < 1e-6 and abs(v["sites"]["B-Li"].get("O-B_minus_O-P_eV", 9) + 0.45) < 1e-6,
                    "[양성] G3 기록 — 자리마다 O–B 최저 − O–P 최저")
                chk((v["sites"]["B-P"].get("dft_order") or [None])[0] == "X01" and v["sites"]["B-Li"].get("lowest_family") == "O-B"
                    and all(abs(x["dE_site_min_eV"]) < 1e-9 for x in v["rows"] if x["name"] in ("X01", "X06")),
                    "[양성] 자리 안 순위 · 최저와의 차 (두 O 꼴 합쳐)")
                chk("판정_아님" in v and not any(k.startswith("D") for k in v) and (T / "rs_ok.json").is_file(),
                    "[양성] D 를 내지 않는다 · 결과 파일을 쓴다")
                chk(refuses(rs, D0, "rs_ok.json"), "[음성] 결과 파일이 이미 있으면 → 덮지 않는다")
                Ein = dict(E0, X02=-999.95, X04=-1000.40 + 0.299)
                Eout = dict(E0, X02=-999.95, X04=-1000.40 + 0.301)
                chk(try_rs(fresh("w_in", Emap=Ein), "rs_win.json")["sites"]["B-P"].get("relax_pick") == ["X01", "X04"]
                    and try_rs(fresh("w_out", Emap=Eout), "rs_wout.json")["sites"]["B-P"].get("relax_pick") == ["X01"],
                    "[양성] 창 경계 — 둘째 차 0.299 eV 는 넣고 0.301 eV 는 뺀다")
                chk(refuses(rs, fresh("miss", skip=("X03",)), "rs_m.json"), "[음성] 출력 하나 누락 → 판독하지 않는다")
                chk(refuses(rs, fresh("nc", kw_by={"X05": {"not_conv": True}}), "rs_nc.json"), "[음성] SCF 미수렴 하나 → G1 멈춤")
                chk(refuses(rs, fresh("jd", kw_by={"X07": {"job_done": False}}), "rs_jd.json"), "[음성] JOB DONE 없음 → G1 멈춤")
                chk(refuses(rs, fresh("ver", kw_by={"X08": {"version": "7.3"}}), "rs_ver.json"), "[음성] QE 판이 다름 → G1 멈춤")
                D = fresh("tamper")
                (D / "X02" / "scf.in").write_text((D / "X02" / "scf.in").read_text() + "\n")
                chk(refuses(rs, D, "rs_t.json"), "[음성] scf.in 이 계획 뒤 바뀜 → G2 멈춤")
                D = fresh("regen")
                (D / "X02" / "scf.in").write_text((D / "X02" / "scf.in").read_text().replace("conv_thr", "conv_thr ", 1))
                pj = json.loads((D / "sp_plan.json").read_text()); pj["jobs"]["X02"]["scf_in_sha256"] = sha256_file(D / "X02" / "scf.in")
                (D / "sp_plan.json").write_text(json.dumps(pj))
                chk(refuses(rs, D, "rs_r.json"), "[음성] scf.in 과 계획 sha256 을 같이 바꿔 맞춰도 → 다시 만든 입력과 달라 G2 멈춤")
                D = fresh("extra")
                shutil.copytree(D / "X00", D / "Y99")
                chk(refuses(rs, D, "rs_x.json"), "[음성] 계획에 없는 잡 폴더 → 멈춘다")
                D = fresh("plan11")
                pj = json.loads((D / "sp_plan.json").read_text()); pj["jobs"].pop("X11")
                (D / "sp_plan.json").write_text(json.dumps(pj))
                chk(refuses(rs, D, "rs_p.json"), "[음성] 계획의 잡이 12 개가 아님 → 멈춘다")
                D = fresh("nat")
                pj = json.loads((D / "sp_plan.json").read_text()); pj["jobs"]["X09"]["nat"] += 1
                (D / "sp_plan.json").write_text(json.dumps(pj))
                chk(refuses(rs, D, "rs_n.json"), "[음성] 잡의 원자 수가 계획과 다름 → G1 멈춤")
                pdir2 = T / "pp2"
                shutil.copytree(pdir, pdir2)
                f0 = sorted(pdir2.iterdir())[0]
                f0.write_text(f0.read_text() + "\n")
                chk(refuses(rs, fresh("pp"), "rs_pp.json", pseudo=pdir2), "[음성] 유사포텐셜 파일이 계획과 다름 → 멈춘다")
                pk_t = T / "pk_t"
                shutil.copytree(pk, pk_t)
                (pk_t / "manifest.json").write_text((pk_t / "manifest.json").read_text() + " ")
                chk(refuses(rs, fresh("man"), "rs_man.json", sp_pick=pk_t), "[음성] sp_pick manifest 가 계획 뒤 바뀜 → 멈춘다")
                MODELS["B-Li"] = {"B": 2}
                chk(refuses(cmd_sp_inputs, pk, T / "sp7", pseudo_dir=str(pdir), disk_io="medium", repo_root=root),
                    "[음성] 조성이 모델과 다름 → 멈춘다")
            finally:
                MODELS.clear(); MODELS.update(saved_m2)
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
    a4 = sp.add_parser("pick_dft"); a4.add_argument("--op_raw", required=True); a4.add_argument("--op_inputs", required=True)
    a4.add_argument("--ob_sel", required=True); a4.add_argument("--ob_results", required=True); a4.add_argument("--out", required=True)
    a5 = sp.add_parser("sp_inputs"); a5.add_argument("--sp_pick", required=True); a5.add_argument("--out", required=True)
    a5.add_argument("--pseudo_dir", required=True); a5.add_argument("--disk_io", required=True, choices=DISK_IO)
    a6 = sp.add_parser("read_sp"); a6.add_argument("--sp_dft", required=True); a6.add_argument("--sp_pick", required=True)
    a6.add_argument("--pseudo_dir", required=True); a6.add_argument("--out", required=True)
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
    if a.cmd == "pick_dft":
        root = Path(__file__).resolve().parents[2]
        m = cmd_pick_dft(Path(a.op_raw), Path(a.op_inputs), Path(a.ob_sel), Path(a.ob_results), Path(a.out), repo_root=root)
        for key, g in m["groups"].items():
            print(f"  {key:10s} " + " · ".join(f"{x['name']}{'*' if x['chosen'] else ''} +{x['dE_from_family_min_eV']:.3f} [{x['end_motif']}]" for x in g))
        for site, c in m["cross_family_uma"].items():
            print(f"  {site:5s} UMA 최저 O–B − O–P = {c['O-B_minus_O-P_eV']:+.3f} eV (고르기용 · 판정 아님)")
        ch = sum(1 for f in m["files"].values() if f["motif_changed"])
        print(f"단일점 {len(m['files'])} 개 → {a.out}/manifest.json (* = 고름 · 끝 꼴이 출발 가족과 다른 고른 후보 {ch} 개 · 기록만)")
        return 0
    if a.cmd == "sp_inputs":
        root = Path(__file__).resolve().parents[2]
        pl = cmd_sp_inputs(Path(a.sp_pick), Path(a.out), pseudo_dir=a.pseudo_dir, disk_io=a.disk_io, repo_root=root)
        for nm, j in pl["jobs"].items():
            print(f"  {nm:12s} {j['site']:5s} {j['family']} · nat {j['nat']} · scf.in {j['scf_in_sha256'][:12]}")
        print(f"단일점 입력 {len(pl['jobs'])} 개 → {a.out}/<이름>/scf.in · 계획 {a.out}/sp_plan.json (disk_io {a.disk_io} · k {pl['settings']['k']})")
        return 0
    if a.cmd == "read_sp":
        root = Path(__file__).resolve().parents[2]
        v = cmd_read_sp(Path(a.sp_dft), Path(a.sp_pick), Path(a.out), pseudo_dir=a.pseudo_dir, repo_root=root)
        print(f"  게이트 G1 {v['gates']['G1']} · G2 {v['gates']['G2']}")
        for s, g in v["sites"].items():
            rs = [x for x in v["rows"] if x["site"] == s]
            print(f"  {s:5s} DFT 순위 (두 O 꼴 합쳐 · 최저와의 차 eV/셀 · 판정 아님):")
            for x in sorted(rs, key=lambda x: x["E_eV"]):
                print(f"        {x['name']:12s} {x['family']} +{x['dE_site_min_eV']:.3f} · UMA {x['E_uma_eV']:.3f} eV · 끝 꼴 {x['end_motif']}")
            print(f"        → 단계_2 이완 후보 {g['relax_pick']} (둘째와 {g['second_gap_eV']:.3f} eV · 창 {v['relax_window_eV']}) · "
                  f"G3 기록 O–B − O–P = {g['O-B_minus_O-P_eV']:+.3f} eV/셀")
        print(f"→ {a.out} · {v['판정_아님']}")
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
