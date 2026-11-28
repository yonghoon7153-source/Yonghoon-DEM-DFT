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
  --mixing  (sp_inputs · probe) 개정 1 (D-2026-11-25-b2o3-site-dft-amend1) — SCF 믹싱 두 줄 (mixing_mode · mixing_beta) 만
            바꾼다 · 예 local-TF:0.2. 계획 (sp_plan.json) 에 적고, read_sp 는 그 값으로 입력을 다시 만들어 G2 로 대조한다.
            믹싱은 수렴 경로만 바꾸고 수렴한 바닥상태는 같다 (57 Å 막대 셀의 전하 출렁임 처방 · 우리 슬랩 규칙)
  relax_inputs 카드 4 단계_2 — read_sp 결과의 relax_pick 을 믿지 않고 rows 에서 같은 규칙 (최저 + 0.30 eV 안의 둘째) 으로
            다시 골라 대조 → 고정 기준 셀 (host × (1,1,2) 를 V₀ 로 등방 스케일 · 9 단계와 같은 host · V₀) 로 분수 좌표째 옮긴
            이온 이완 입력 (bfgs · tstress · k 3 3 1 · 판독 결과 = 계획의 믹싱) + relax_plan.json (판독 · 계획 · 구조 · host sha256)
  ref_inputs  카드 2 기준상 — Li₂S (mp-1153) · Li₃PS₄ 다형 셋 vc-relax 입력 (판 고정 설정 + &CELL bfgs · k = ceil(13.9 Å / 축)) ·
            저장소에 있는 둘은 저장소 파일 sha256 으로 묶고, MP 에서 받은 둘은 mp_fetch.json 기록 (sha256 · 물은 id) 과 대조 + ref_plan.json
  mp_fetch  카드 2 기준상 넷 모으기 — 저장소 둘 (Li₂S mp-1153 · Li₃PS₄ mp-985583) 은 바이트 그대로 복사 · 없는 둘 (Li₃PS₄ mp-2646995 ·
            mp-1097036) 은 MP 에서 받는다 (fetch_mp_structure.py fetch_mp_doc · 키는 환경변수 MP_API_KEY · 출력 안 함) + mp_fetch.json
            (물은 id · 돌려받은 id — MP 가 id 를 옮기는 중 · 화학식 · DB 판 · sha256) · 다 받고 조성까지 맞아야 쓴다
  --selftest  음성 경로 포함

이 도구가 못 하는 것 (한계 — 숨기지 않는다)
  · UMA · DFT 를 돌리지 않는다 (입력 · 고르기 · 단일점 판독만) · 형성 에너지 · D 를 내지 않는다 — read_sp 도 자리 사이
    단일점 에너지를 빼지 않는다 (조성이 다르다 · D 는 기준상 · 이온 이완 · 압력 어림 · k 탐침 뒤 · 카드 4).
  · 'B 결합 S' 는 10월 UMA 이완 구조의 2.3 Å 안 S 다 — B 가 이완 중 S 하나를 놓은 경우 (B-P 의 BS₃) 그 S 는 후보가 아니다.
  · 조합 고르기는 UMA 에너지다 (DFT 아님) · 어닐 전 이완 하나로 고른다 — 다른 조합이 어닐 뒤 더 낮을 가능성은 남는다.
  · O 꼴 이름 (O–B · O–P) 은 끝 구조로 다시 매겨야 한다 — 여기서는 시작 꼴만 적는다 (pick_ob 는 고른 이완 구조의 끝 꼴을 적는다).
  · 10월 O–P 후보는 10월 run_anneal.py (08-30 판) 로, O–B 짝은 지금 판으로 돈다 — MD · 이완 경로는 같고 수렴 판정 · 기록만 다르다
    (git diff 34a400e93 HEAD -- tools/doping/run_anneal.py · 11-23 확인).
  · relax_inputs · ref_inputs 도 pw.x 를 돌리지 않는다 · 이완 · 기준상 출력 판독 (read_relax · D · 압력 어림 · k 탐침) 은 따로
    (결과 전에 커밋한다) · 기준상 믹싱은 판 고정 그대로다 (개정 1 믹싱은 57 Å 막대 셀 후보 SCF 에만 — 기준상은 작은 벌크 셀) ·
    MP 에서 받는 것은 mp_fetch 하나다 (키 · 네트워크가 있는 기계 · 받은 그대로 · 다형을 고르지 않는다 — 고르기는 판독기 몫) ·
    UMA 셀 모양이 기준 셀과 크게 다르면 옮기지 않고 멈춘다 (문턱 = 9 단계 UMA 셀 6 개의 최대 차 2.1 % · 0.95° 의 두 배 넘게 여유).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import os
import re
import shutil
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
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
MIXING_MODES = ("plain", "TF", "local-TF")      # QE &ELECTRONS mixing_mode 값
AMEND1 = "D-2026-11-25-b2o3-site-dft-amend1"     # 개정 1 — 단일점 · 이완 SCF 믹싱 local-TF β 0.2 (12 점 전부 · 새 폴더)
FAMILIES = ("O-P", "O-B")
KIND_SP_READ = "b2o3_site_dft_sp_read/v1"
SP_RELAX_WINDOW_EV = 0.30   # 카드 4 단계_2 — 자리마다 단일점 최저 + 둘째가 첫째와 셀 에너지 0.30 eV 안이면 둘째도
# ── 단계_2 이완 · 기준상 (카드 4 · 2 · 개정 4) ─────────────────────────────────────────────
AMEND4 = "D-2026-11-28-b2o3-site-dft-amend4-gabia"   # 개정 4 — 단계_2 · 기준상 · 탐침 기계 kgy → gabia (11b 끝난 뒤 · GPU 독점)
SITE_SUPERCELL = (1, 1, 2)          # 카드 4 기준_셀 — host × (1,1,2) (판 고정 reference_cell 은 9 단계 셀 모양 (1,2,1) 이라 따로)
CARD_CELLPAR_UNSCALED = (7.007, 7.007, 70.07, 60.0, 60.0, 60.0)   # 카드 문구 (스케일 전) — host × (1,1,2) 대조 (0.01 Å · 0.01°)
RELAX_K = (3, 3, 1)                 # 카드 4 k_main
RELAX_SHAPE_TOL = {"len_rel": 0.05, "angle_deg": 3.0}   # UMA 셀 ↔ 기준 셀 모양 차 상한 — 다른 초격자 · 축 순서를 잡는 문턱
KIND_RELAX_PLAN = "b2o3_site_dft_relax_plan/v1"
PURPOSE_RELAX = "b2o3_site_dft/dft_relax_stage2"
KIND_REF_PLAN = "b2o3_site_dft_ref_plan/v1"
PURPOSE_REF = "b2o3_site_dft/dft_reference_vc_relax"
KIND_MP_FETCH = "b2o3_site_dft_mp_fetch/v1"
REF_K_LEN_A = 13.9                  # 기준상 k = ceil(13.9 Å / 축 길이) (카드 4 · 10-15 선례)
REF_SPECS = {                       # 카드 2 기준상 — 저장소 파일은 sha256 결속 · 나머지는 MP 받은 기록 (mp_fetch.json) 결속
    "Li2S_mp-1153": {"file": "sei_li2s_mp-1153.cif", "formula": {"Li": 2, "S": 1}, "mp": "mp-1153",
                     "repo": "db/structures/sei_li2s_mp-1153.cif"},
    "Li3PS4_mp-985583": {"file": "li3ps4_mp-985583.cif", "formula": {"Li": 3, "P": 1, "S": 4}, "mp": "mp-985583",
                         "repo": "db/structures/li3ps4_mp-985583.cif"},
    "Li3PS4_mp-2646995": {"file": "li3ps4_mp-2646995.cif", "formula": {"Li": 3, "P": 1, "S": 4}, "mp": "mp-2646995",
                          "repo": None},
    "Li3PS4_mp-1097036": {"file": "li3ps4_mp-1097036.cif", "formula": {"Li": 3, "P": 1, "S": 4}, "mp": "mp-1097036",
                          "repo": None},
}


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


def parse_mixing(m):
    """'local-TF:0.2' 또는 ('local-TF', 0.2) → ('local-TF', 0.2) · None → None (판 고정 믹싱 그대로).

    모르는 모드 · β 가 숫자가 아님 · 0 < β ≤ 1 밖 · NaN · 꼴이 다름 → 멈춘다 (조용히 판 고정 값으로 떨어지지 않는다).
    """
    if m is None:
        return None
    if isinstance(m, (tuple, list)):
        if len(m) != 2:
            raise SystemExit(f"⛔ 믹싱 {m} — (모드, β) 둘이어야 한다")
        mode, beta = m
    elif isinstance(m, str) and m.count(":") == 1:
        mode, b = m.split(":")
        try:
            beta = float(b)
        except ValueError:
            raise SystemExit(f"⛔ --mixing β '{b}' 가 숫자가 아니다")
    else:
        raise SystemExit(f"⛔ --mixing '{m}' — '모드:β' 꼴 (예 local-TF:0.2)")
    if mode not in MIXING_MODES:
        raise SystemExit(f"⛔ mixing_mode '{mode}' — {MIXING_MODES} 중 하나")
    if isinstance(beta, bool) or not isinstance(beta, (int, float)) or not math.isfinite(beta) or not 0.0 < beta <= 1.0:
        raise SystemExit(f"⛔ mixing_beta {beta} — 0 < β ≤ 1")
    return (mode, float(beta))


def pw_text(mod, atoms, *, prefix, calc, k, pseudo_dir, disk_io, tstress=False, mixing=None) -> str:
    if disk_io not in DISK_IO:
        raise SystemExit(f"⛔ disk_io {disk_io} — {DISK_IO} 중 하나")
    t = mod.pw_input_text(atoms, prefix=prefix, calc=calc, k=k, pseudo_dir=pseudo_dir, tstress=tstress)
    old = f"    disk_io = '{mod.DFT['disk_io']}'"
    if t.count(old) != 1:
        raise SystemExit(f"⛔ 판 고정 입력에서 disk_io 줄을 정확히 하나 못 찾았다 ({t.count(old)})")
    t = t.replace(old, f"    disk_io = '{disk_io}'")
    mx = parse_mixing(mixing)
    if mx is not None:                     # 개정 1 — 믹싱 두 줄만 바꾼다 (나머지는 판 고정 그대로)
        for key, cur, new in (("mixing_mode", f"'{mod.DFT['mixing_mode']}'", f"'{mx[0]}'"),
                              ("mixing_beta", f"{mod.DFT['mixing_beta']}", f"{mx[1]}")):
            o = f"    {key} = {cur}"
            if t.count(o) != 1:
                raise SystemExit(f"⛔ 판 고정 입력에서 {key} 줄을 정확히 하나 못 찾았다 ({t.count(o)})")
            t = t.replace(o, f"    {key} = {new}")
    return t


def cmd_sp_inputs(sp_pick: Path, out: Path, *, pseudo_dir: str, disk_io: str, repo_root: Path, k=(3, 3, 1),
                  mixing=None) -> dict:
    """카드 4 단계_1 — pick_dft 가 고른 12 구조의 DFT 단일점 입력 (UMA 구조 · UMA 셀 그대로 · 9 단계 판 고정 설정).

    출력 = <out>/<이름>/scf.in (run_force_check_scf.sh 가 그대로 도는 꼴) + <out>/sp_plan.json
    (입력 sha256 · 구조 sha256 · 판 고정 도구 sha256 · 유사포텐셜 sha256 · md5 · z_valence · k · disk_io).
    입력은 결정론이다 — 판독기가 같은 인자로 다시 만들어 sha256 으로 대조한다.
    mixing (개정 1): 주면 믹싱 두 줄만 바꾸고 계획 settings.mixing 에 적는다 (read_sp 가 그 값으로 다시 만든다) ·
       안 주면 판 고정 믹싱 그대로 · settings.mixing = null.
    ⛔ 못 하는 것: pw.x 를 돌리지 않는다 · disk_io 는 메모리 프로브 결과로 사람이 고른다 (숫자에는 영향 없음 ·
       9 단계 단일점은 gabia nowf) · 셀을 기준 셀로 옮기지 않는다 (단일점은 UMA 셀 그대로 — 기준 셀은 단계_2 이완).
    """
    from ase.io import read
    mx = parse_mixing(mixing)              # 잘못된 값이면 파일을 만들기 전에 멈춘다
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
        t = pw_text(mod, a, prefix=f"sp_{nm}", calc="scf", k=list(k), pseudo_dir=pseudo_dir, disk_io=disk_io, mixing=mx)
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
                                                            "mixing_mode", "mixing_beta", "electron_maxstep", "diagonalization")},
                         "DFT_note": "DFT = 판 고정 값 · mixing 이 null 이 아니면 입력의 믹싱 두 줄은 그 값이다",
                         "mixing": (None if mx is None else {"mode": mx[0], "beta": mx[1], "decision": AMEND1})},
            "pseudo": pp, "sp_pick_manifest_sha256": sha256_file(sp_pick / "manifest.json"), "jobs": jobs}
    (out / "sp_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1) + "\n")
    return plan


def cmd_probe(xyz: Path, out: Path, *, pseudo_dir: str, k, disk_io: str, repo_root: Path, mixing=None) -> str:
    from ase.io import read
    mx = parse_mixing(mixing)
    mod = load_pinned(repo_root)
    a = read(str(xyz))
    t = pw_text(mod, a, prefix=f"probe_{Path(xyz).stem}_{disk_io}", calc="scf", k=k, pseudo_dir=pseudo_dir, disk_io=disk_io,
                mixing=mx)
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
    mset = (plan.get("settings") or {}).get("mixing")    # 개정 1 — 계획에 적힌 믹싱으로 다시 만든다 (없음 = 판 고정)
    if mset is not None and not (isinstance(mset, dict) and {"mode", "beta"} <= set(mset)):
        raise SystemExit(f"⛔ 계획의 settings.mixing 꼴이 다르다: {mset}")
    mix = None if mset is None else parse_mixing((mset["mode"], mset["beta"]))
    with tempfile.TemporaryDirectory() as td:
        re_plan = cmd_sp_inputs(sp_pick, Path(td) / "re", pseudo_dir=pseudo_dir, disk_io=plan["settings"]["disk_io"],
                                repo_root=repo_root, k=tuple(plan["settings"]["k"]), mixing=mix)
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
         "settings_from_plan": {"mixing": mset, "disk_io": plan["settings"]["disk_io"], "k": plan["settings"]["k"]},
         "relax_window_eV": SP_RELAX_WINDOW_EV, "rows": sorted(rows, key=lambda x: (x["site"], x["E_eV"])), "sites": sites,
         "판정_아님": "자리 사이 D 는 기준상 · 이온 이완 · 압력 어림 · k 탐침 뒤에만 낸다 (카드 4) — 단일점 에너지를 자리 사이에서 빼지 않는다 (조성이 다르다)",
         "next": "단계_2 — 자리마다 relax_pick 을 고정 기준 셀 (V₀ 2436.33 Å³ · 등방 스케일) 로 옮겨 이온 이완 (카드 4 · 입력 도구는 따로) · "
                 "이완 SCF 도 같은 믹싱 (settings_from_plan.mixing · 개정 1)"}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n")
    return v


# ----------------------------------------------------------------------------- 단계_2 이완 · 기준상 입력
def site_reference_cell(mod, host: Path):
    """카드 4 기준_셀 — host (modelc_V0_k663.xyz · 9 단계와 같은 파일 · sha256) × (1,1,2) 의 cellpar 를 V₀ 로 등방 스케일.

    판 고정 reference_cell 은 9 단계 셀 모양 (1,2,1) 이라 쓰지 않는다 — host sha256 · V₀ 는 판 고정 값을 그대로 쓴다.
    스케일 전 cellpar 가 카드 문구 (7.007 · 7.007 · 70.07 Å · 60°) 와 다르면 멈춘다 (초격자 방향을 잘못 잡은 경우).
    """
    from ase.geometry import cellpar_to_cell
    from ase.io import read
    hp = Path(host)
    if not hp.is_file() or sha256_file(hp) != mod.DFT["ref_cell"]["host_sha256"]:
        raise SystemExit(f"⛔ host {hp} 가 없거나 sha256 이 카드의 modelc_V0_k663.xyz 가 아니다")
    h = read(str(hp)).repeat(SITE_SUPERCELL)
    par = np.array(h.cell.cellpar(), float)
    if any(abs(par[i] - CARD_CELLPAR_UNSCALED[i]) > 0.01 for i in range(6)):
        raise SystemExit(f"⛔ host × {SITE_SUPERCELL} cellpar {np.round(par, 4).tolist()} ≠ 카드 문구 {CARD_CELLPAR_UNSCALED}")
    V0 = float(mod.DFT["ref_cell"]["V0_A3"])
    s = (V0 / h.get_volume()) ** (1.0 / 3.0)
    par[:3] *= s
    cell = np.asarray(cellpar_to_cell(par), float)
    return cell, {"host_sha256": sha256_file(hp), "supercell": list(SITE_SUPERCELL), "host_volume_A3": float(h.get_volume()),
                  "scale": float(s), "cellpar": par.tolist(), "V0_A3": V0, "volume_A3": float(abs(np.linalg.det(cell)))}


def cell_shape_diff(cell_a, cell_b) -> dict:
    """두 셀의 cellpar 차 — 길이는 상대 차 최대 · 각은 절대 차 최대 (°)."""
    from ase.geometry import cell_to_cellpar
    pa = cell_to_cellpar(np.asarray(cell_a, float))
    pb = cell_to_cellpar(np.asarray(cell_b, float))
    return {"len_rel_max": float(max(abs(pa[i] - pb[i]) / pb[i] for i in range(3))),
            "angle_deg_max": float(max(abs(pa[i] - pb[i]) for i in range(3, 6)))}


def min_pair_distance(atoms) -> float:
    d = np.asarray(atoms.get_all_distances(mic=True), float)
    np.fill_diagonal(d, np.inf)
    return float(d.min())


def relax_atoms(mod, a, cell):
    """후보 (UMA 셀) → 기준 셀 (분수 좌표 그대로 · 판 고정 map_to_cell). 반환 (옮긴 원자, 기록).

    멈추는 경우: 기하가 유한 · 정칙이 아님 (판 고정 _geom_bad) · UMA 셀 모양이 기준 셀과 크게 다름 (RELAX_SHAPE_TOL —
    다른 초격자 · 축 순서) · 옮긴 뒤 원자 쌍이 MIN_PAIR (1.0 Å) 보다 가까움 (가장 짧은 실제 결합 B–O ≈ 1.37 Å).
    """
    if mod._geom_bad(a):
        raise SystemExit("⛔ 후보 기하가 유한 · 정칙이 아니다")
    d = cell_shape_diff(a.cell.array, cell)
    if d["len_rel_max"] > RELAX_SHAPE_TOL["len_rel"] or d["angle_deg_max"] > RELAX_SHAPE_TOL["angle_deg"]:
        raise SystemExit(f"⛔ UMA 셀 모양이 기준 셀과 크게 다르다 ({d}) — 분수 좌표째 옮기면 결합이 일그러진다")
    m = mod.map_to_cell(a, cell)
    if mod._geom_bad(m):
        raise SystemExit("⛔ 옮긴 기하가 유한 · 정칙이 아니다")
    d0, d1 = min_pair_distance(a), min_pair_distance(m)
    if d1 < MIN_PAIR:
        raise SystemExit(f"⛔ 옮긴 뒤 원자 쌍 최소 거리 {d1:.3f} Å < {MIN_PAIR} Å")
    from ase.geometry import cell_to_cellpar
    return m, {"uma_cellpar": [float(x) for x in cell_to_cellpar(a.cell.array)], "uma_volume_A3": float(abs(np.linalg.det(a.cell.array))),
               "shape_diff": d, "min_pair_before_A": d0, "min_pair_after_A": d1}


def cmd_relax_inputs(sp_read: Path, sp_dft: Path, sp_pick: Path, host: Path, out: Path, *, pseudo_dir: str, disk_io: str,
                     repo_root: Path) -> dict:
    """카드 4 단계_2 — read_sp 가 고른 이완 후보를 고정 기준 셀로 옮긴 이온 이완 입력 (bfgs · tstress · k 3 3 1 · 같은 믹싱).

    결속: 판독 결과 (kind · 카드 · 결정) ↔ 단일점 계획 (판독 결과의 plan sha256) ↔ sp_pick manifest (계획의 sha256) ↔ 구조 파일
    (manifest · 계획의 sha256) · 유사포텐셜 (파일 · sha256 · md5 · z — 폴더 경로는 기계마다 달라 안 본다) · host (판 고정 sha256).
    판독 결과의 relax_pick 을 믿지 않고 rows 에서 같은 규칙 (최저 + 0.30 eV 안의 둘째) 으로 다시 골라 다르면 멈춘다.
    믹싱은 판독 결과의 settings_from_plan.mixing (= 계획 settings.mixing · 개정 1) 그대로. 검사를 다 통과한 뒤에만 쓴다.
    출력 = <out>/r<순서>_<이름>/scf.in (run_force_check_scf.sh 가 그대로 도는 꼴 · relax 완료 = bfgs converged) + <out>/relax_plan.json.
    순서 = 자리마다 최저 먼저 (B-P · B-Li) · 그 다음 둘째 — 실행기는 폴더 이름 순으로 돈다 (GPU 상한에 걸려도 자리 최저 둘이 먼저 끝난다).
    ⛔ 못 하는 것: pw.x 를 돌리지 않는다 · 자리 사이 D · 압력 어림 · k 탐침을 하지 않는다 (판독기는 따로 · 결과 전 커밋) ·
       이완 시작 구조는 UMA 구조 그대로다 (DFT 단일점의 전자 밀도를 이어 쓰지 않는다 · 셀이 다르다).
    """
    from ase.io import read
    mod = load_pinned(repo_root)
    sp_read, sp_dft, sp_pick, host, out = Path(sp_read), Path(sp_dft), Path(sp_pick), Path(host), Path(out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"⛔ {out} 가 비어 있지 않다 — 덮지 않는다")
    v = json.loads(sp_read.read_text())
    if v.get("kind") != KIND_SP_READ or v.get("card") != CARD or v.get("decision") != DECISION:
        raise SystemExit("⛔ read_sp 판독 결과가 아니다 (kind · card · decision)")
    pf = sp_dft / "sp_plan.json"
    if not pf.is_file():
        raise SystemExit(f"⛔ {pf} 가 없다")
    plan = json.loads(pf.read_text())
    if plan.get("schema") != "b2o3_site_dft_sp_plan/v1" or plan.get("purpose") != PURPOSE_SP or plan.get("card") != CARD:
        raise SystemExit("⛔ sp_inputs 의 단일점 계획이 아니다 (schema · purpose · card)")
    if (v.get("plan") or {}).get("sha256") != sha256_file(pf):
        raise SystemExit("⛔ 판독 결과가 이 단일점 계획에서 나온 것이 아니다 (plan sha256)")
    if not (sp_pick / "manifest.json").is_file() or sha256_file(sp_pick / "manifest.json") != plan.get("sp_pick_manifest_sha256"):
        raise SystemExit("⛔ sp_pick manifest 가 없거나 계획과 다르다 (sha256)")
    man = json.loads((sp_pick / "manifest.json").read_text())
    jp = plan.get("jobs") or {}
    rows = v.get("rows") or []
    if len(rows) != len(jp) or {r.get("name") for r in rows} != set(jp):
        raise SystemExit("⛔ 판독 결과의 rows 가 계획의 잡과 다르다")
    if v.get("relax_window_eV") != SP_RELAX_WINDOW_EV:
        raise SystemExit(f"⛔ 판독 결과의 창 {v.get('relax_window_eV')} ≠ 카드 {SP_RELAX_WINDOW_EV} eV")
    picks = {}
    for s in BASES:
        r = sorted((x for x in rows if x.get("site") == s), key=lambda x: (x["E_eV"], x["name"]))
        if len(r) < 2 or any(jp[x["name"]].get("site") != s for x in r):
            raise SystemExit(f"⛔ {s}: rows 의 자리가 계획과 다르거나 둘보다 적다")
        if any(not math.isfinite(float(x["E_eV"])) for x in r):
            raise SystemExit(f"⛔ {s}: rows 에 유한하지 않은 에너지")
        gap = r[1]["E_eV"] - r[0]["E_eV"]
        want = [r[0]["name"]] + ([r[1]["name"]] if gap <= SP_RELAX_WINDOW_EV else [])
        if ((v.get("sites") or {}).get(s) or {}).get("relax_pick") != want:
            raise SystemExit(f"⛔ {s}: 판독 결과의 relax_pick 이 rows 에서 다시 고른 {want} 와 다르다")
        picks[s] = want
    mset = (plan.get("settings") or {}).get("mixing")
    if (v.get("settings_from_plan") or {}).get("mixing") != mset:
        raise SystemExit("⛔ 판독 결과의 믹싱이 계획의 믹싱과 다르다")
    if mset is not None and not (isinstance(mset, dict) and {"mode", "beta"} <= set(mset)):
        raise SystemExit(f"⛔ 계획의 settings.mixing 꼴이 다르다: {mset}")
    mx = None if mset is None else parse_mixing((mset["mode"], mset["beta"]))
    pp = mod.pseudo_record(pseudo_dir)
    if pp.get("files") != (plan.get("pseudo") or {}).get("files"):
        raise SystemExit("⛔ 유사포텐셜 파일 기록 (sha256 · md5 · z_valence) 이 단일점 계획과 다르다")
    cell, crec = site_reference_cell(mod, host)
    order = [picks[s][0] for s in BASES] + [picks[s][1] for s in BASES if len(picks[s]) > 1]
    texts, jobs = {}, {}
    for rank, nm in enumerate(order, 1):
        s = jp[nm]["site"]
        j = jp[nm]
        rel = j.get("xyz")
        e = (man.get("files") or {}).get(rel)
        if e is None or e.get("sha256") != j.get("xyz_sha256") or sha256_file(sp_pick / rel) != e["sha256"]:
            raise SystemExit(f"⛔ {nm}: 구조 파일이 manifest · 계획과 다르다 (sha256)")
        a = read(str(sp_pick / rel))
        if composition(a) != dict(sorted(MODELS[s].items())) or len(a) != j.get("nat"):
            raise SystemExit(f"⛔ {nm}: 조성 · 원자 수가 모델 · 계획과 다르다")
        m, grec = relax_atoms(mod, a, cell)
        texts[nm] = pw_text(mod, m, prefix=f"rx_{nm}", calc="relax", k=list(RELAX_K), pseudo_dir=pseudo_dir,
                            disk_io=disk_io, tstress=True, mixing=mx)
        jobs[nm] = {"priority": rank, "dir": f"r{rank}_{nm}", "site": s, "family": j.get("family"), "base": j.get("base"),
                    "nat": len(m), "xyz": rel,
                    "xyz_sha256": e["sha256"], "sp_E_eV": next(x["E_eV"] for x in rows if x["name"] == nm),
                    "geometry": grec, "scf_in_sha256": hashlib.sha256(texts[nm].encode("utf-8")).hexdigest()}
    for nm, t in texts.items():                     # 검사를 다 통과한 뒤에만 쓴다
        (out / jobs[nm]["dir"]).mkdir(parents=True)
        (out / jobs[nm]["dir"] / "scf.in").write_text(t)
        if sha256_file(out / jobs[nm]["dir"] / "scf.in") != jobs[nm]["scf_in_sha256"]:
            raise SystemExit(f"⛔ {nm}: 쓴 입력의 sha256 이 만든 텍스트와 다르다")
    rp = {"schema": KIND_RELAX_PLAN, "purpose": PURPOSE_RELAX, "card": CARD, "decision": DECISION, "amendments": [AMEND1, AMEND4],
          "tool": {"path": "tools/doping/b2o3_site_dft.py", "sha256": tool_sha()},
          "pinned_dft": {"path": PINNED_DFT_REL, "sha256": PINNED_DFT_SHA},
          "sp_read": {"sha256": sha256_file(sp_read)}, "sp_plan": {"sha256": sha256_file(pf)},
          "sp_pick_manifest_sha256": sha256_file(sp_pick / "manifest.json"), "picks": picks, "order": order, "ref_cell": crec,
          "settings": {"calc": "relax", "k": list(RELAX_K), "disk_io": disk_io, "tstress": True,
                       "relax": dict(mod.DFT["relax"]), "mixing": mset, "cell": "고정 기준 셀 (host × (1,1,2) · V₀ 등방 스케일)"},
          "pseudo": pp, "jobs": jobs,
          "next": "run_force_check_scf.sh (GPU 독점) → 판독기 (따로 · 결과 전 커밋): bfgs 수렴 · 자리 값 = 이완한 것 중 최저 · 압력 어림 · 기준상 · k 탐침 → D"}
    (out / "relax_plan.json").write_text(json.dumps(rp, ensure_ascii=False, indent=1) + "\n")
    return rp


def ref_vc_text(mod, atoms, *, prefix, k, pseudo_dir, disk_io) -> str:
    """기준상 vc-relax 입력 — 판 고정 relax 입력 (tstress) 에서 calculation 한 줄만 vc-relax 로 · &IONS 뒤에 &CELL (bfgs · 0.5 kbar)."""
    t = pw_text(mod, atoms, prefix=prefix, calc="relax", k=k, pseudo_dir=pseudo_dir, disk_io=disk_io, tstress=True)
    a = "    calculation = 'relax'"
    if t.count(a) != 1:
        raise SystemExit(f"⛔ 판 고정 relax 입력에서 calculation 줄을 정확히 하나 못 찾았다 ({t.count(a)})")
    t = t.replace(a, "    calculation = 'vc-relax'")
    ions = "&IONS\n    ion_dynamics = 'bfgs'\n/\n"
    if t.count(ions) != 1:
        raise SystemExit(f"⛔ 판 고정 relax 입력에서 &IONS 블록을 정확히 하나 못 찾았다 ({t.count(ions)})")
    return t.replace(ions, ions + "&CELL\n    cell_dynamics = 'bfgs'\n    press_conv_thr = 0.5\n/\n")


def cmd_ref_inputs(refs_dir: Path, out: Path, *, pseudo_dir: str, disk_io: str, repo_root: Path) -> dict:
    """카드 2 기준상 — Li₂S · Li₃PS₄ 다형 셋 vc-relax 입력 (사용자 허락 11-23 · argyrodite 아님 · 판 고정 설정 + &CELL bfgs).

    결속: 저장소에 있는 파일 (REF_SPECS repo) 은 refs_dir 사본이 저장소 파일과 같은 sha256 이어야 한다 · 나머지는
    refs_dir/mp_fetch.json (kind · 파일마다 sha256 · 물은 id) 과 같아야 한다 · 조성은 화학식의 정수배 · k = ceil(13.9 Å / 축 길이).
    믹싱은 판 고정 그대로 (개정 1 은 후보 SCF 에만). 검사를 다 통과한 뒤에만 쓴다.
    ⛔ 못 하는 것: MP 에서 받지 않는다 · 다형 중 최저를 고르지 않는다 (판독기 몫) · vc-relax 의 Pulay 응력을 보정하지 않는다
       (완료 = bfgs converged + 최종 scf — 판독은 최종 scf 에너지로).
    """
    from ase.io import read
    mod = load_pinned(repo_root)
    refs_dir, out = Path(refs_dir), Path(out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"⛔ {out} 가 비어 있지 않다 — 덮지 않는다")
    fetch = None
    if (refs_dir / "mp_fetch.json").is_file():
        fetch = json.loads((refs_dir / "mp_fetch.json").read_text())
        if fetch.get("schema") != KIND_MP_FETCH:
            raise SystemExit("⛔ mp_fetch.json 의 schema 가 다르다")
    pp = mod.pseudo_record(pseudo_dir)
    texts, jobs = {}, {}
    for name, spec in REF_SPECS.items():
        f = refs_dir / spec["file"]
        if not f.is_file():
            raise SystemExit(f"⛔ 기준상 구조 {f} 가 없다")
        h = sha256_file(f)
        if spec["repo"]:
            rp = Path(repo_root) / spec["repo"]
            if not rp.is_file() or sha256_file(rp) != h:
                raise SystemExit(f"⛔ {spec['file']}: 저장소 파일 {spec['repo']} 과 sha256 이 다르다")
            src = {"kind": "repo", "path": spec["repo"], "sha256": h}
        else:
            e = ((fetch or {}).get("files") or {}).get(spec["file"])
            if not e or e.get("sha256") != h or e.get("material_id_asked") != spec["mp"]:
                raise SystemExit(f"⛔ {spec['file']}: MP 받은 기록 (mp_fetch.json · sha256 · 물은 id) 과 다르다")
            src = {"kind": "mp_fetch", "sha256": h, "material_id_asked": spec["mp"],
                   "material_id_returned": e.get("material_id_returned"), "db_version": e.get("db_version")}
        a = read(str(f))
        c = composition(a)
        fo = spec["formula"]
        nfu = c.get(next(iter(fo)), 0) // next(iter(fo.values()))
        if set(c) != set(fo) or nfu < 1 or any(c[el] != nfu * n for el, n in fo.items()):
            raise SystemExit(f"⛔ {name}: 조성 {c} 이 {fo} 의 정수배가 아니다")
        if mod._geom_bad(a):
            raise SystemExit(f"⛔ {name}: 기하가 유한 · 정칙이 아니다")
        lens = [float(x) for x in a.cell.cellpar()[:3]]
        k = [max(1, math.ceil(REF_K_LEN_A / L)) for L in lens]
        texts[name] = ref_vc_text(mod, a, prefix=f"ref_{name}", k=k, pseudo_dir=pseudo_dir, disk_io=disk_io)
        jobs[name] = {"file": spec["file"], "source": src, "composition": c, "n_fu": int(nfu), "nat": len(a),
                      "cell_lengths_A": lens, "k": k, "mp": spec["mp"],
                      "scf_in_sha256": hashlib.sha256(texts[name].encode("utf-8")).hexdigest()}
    for name, t in texts.items():                   # 검사를 다 통과한 뒤에만 쓴다
        (out / name).mkdir(parents=True)
        (out / name / "scf.in").write_text(t)
    plan = {"schema": KIND_REF_PLAN, "purpose": PURPOSE_REF, "card": CARD, "decision": DECISION, "amendments": [AMEND4],
            "tool": {"path": "tools/doping/b2o3_site_dft.py", "sha256": tool_sha()},
            "pinned_dft": {"path": PINNED_DFT_REL, "sha256": PINNED_DFT_SHA},
            "settings": {"calc": "vc-relax", "cell_dynamics": "bfgs", "press_conv_thr_kbar": 0.5, "tstress": True,
                         "relax": dict(mod.DFT["relax"]), "k_rule": f"ceil({REF_K_LEN_A} Å / 축 길이)", "disk_io": disk_io,
                         "mixing": None, "mixing_note": "판 고정 (개정 1 믹싱은 57 Å 막대 셀 후보 SCF 에만)"},
            "pseudo": pp, "mp_fetch_sha256": (sha256_file(refs_dir / "mp_fetch.json") if fetch else None), "jobs": jobs,
            "next": "run_force_check_scf.sh (vc-relax 완료 = bfgs converged + 최종 scf) → 판독기 (따로): Li₃PS₄ = 셋 중 f.u. 당 최저"}
    (out / "ref_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1) + "\n")
    return plan


def _parse_formula(t: str) -> dict:
    """'Li3PS4' → {'Li': 3, 'P': 1, 'S': 4} (MP formula_pretty 꼴 · 꼴이 다르면 빈 dict)."""
    if not isinstance(t, str) or not re.fullmatch(r"(?:[A-Z][a-z]?\d*)+", t):
        return {}
    out = {}
    for el, n in re.findall(r"([A-Z][a-z]?)(\d*)", t):
        if el in out:
            return {}
        out[el] = int(n) if n else 1
    return out


def _mp_fetcher_default(repo_root: Path):
    """기본 받기 — tools/doping/fetch_mp_structure.py 의 fetch_mp_doc (mp_api). 키는 환경변수 MP_API_KEY 에서만 읽고 출력하지 않는다."""
    key = os.environ.get("MP_API_KEY")
    if not key:
        raise SystemExit("⛔ MP_API_KEY 환경변수가 없다 — 키를 대화에 붙이지 말고 그 기계 셸에서 read -rs 로 넣는다 · 받지 않는다")
    spec = importlib.util.spec_from_file_location("fetch_mp_structure", Path(repo_root) / "tools" / "doping" / "fetch_mp_structure.py")
    fm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fm)

    def f(mp_id):
        d = fm.fetch_mp_doc(mp_id, key)
        return {"cif_text": d["structure"].to(fmt="cif"), "material_id_returned": d["material_id_returned"],
                "formula_pretty": d["formula_pretty"], "db_version": d["db_version"]}
    return f


def cmd_mp_fetch(refs_dir: Path, *, repo_root: Path, fetcher=None) -> dict:
    """카드 2 기준상 넷을 한 폴더에 모은다 — ref_inputs 가 그대로 받는 꼴 (저장소 사본 sha256 · mp_fetch.json).

    저장소에 있는 둘 (REF_SPECS repo) 은 바이트 그대로 복사 · 없는 둘은 MP 에서 받는다 (fetcher(mp_id) →
    {cif_text · material_id_returned · formula_pretty · db_version} · 기본 = fetch_mp_doc · selftest 는 가짜 받기).
    멈추는 경우 (아무것도 안 쓴다): 폴더가 비어 있지 않음 · 키 없음 · 받기 실패 · MP 가 다른 화학식을 돌려줌 ·
    받은 CIF 를 다시 읽은 조성이 화학식의 정수배가 아님 — 다 받고 다 읽은 뒤에만 폴더에 쓴다.
    ⛔ 못 하는 것: 다형을 고르거나 구조를 고치지 않는다 (받은 그대로 · P1 CIF) · 에너지를 보지 않는다 · 키를 출력하지 않는다 ·
       돌려받은 id 가 물은 id 와 달라도 멈추지 않는다 (MP 의 id 옮김 · 둘 다 기록하고 화학식 · 조성으로 확인한다).
    """
    from ase.io import read
    refs_dir = Path(refs_dir)
    if refs_dir.exists() and any(refs_dir.iterdir()):
        raise SystemExit(f"⛔ {refs_dir} 가 비어 있지 않다 — 덮지 않는다")
    f = fetcher or _mp_fetcher_default(repo_root)
    got, files, copies = {}, {}, {}
    for name, spec in REF_SPECS.items():
        if spec["repo"]:
            src = Path(repo_root) / spec["repo"]
            if not src.is_file():
                raise SystemExit(f"⛔ 저장소 파일 {spec['repo']} 가 없다")
            got[spec["file"]] = src.read_bytes()
            copies[spec["file"]] = {"path": spec["repo"], "sha256": hashlib.sha256(got[spec["file"]]).hexdigest()}
            continue
        try:
            d = f(spec["mp"])
        except SystemExit:
            raise
        except Exception as ex:
            raise SystemExit(f"⛔ {spec['mp']} 받기 실패 — {type(ex).__name__}: {str(ex)[:200]} · 아무것도 안 썼다")
        if _parse_formula(d.get("formula_pretty")) != spec["formula"]:
            raise SystemExit(f"⛔ {spec['mp']}: MP 가 돌려준 화학식 {d.get('formula_pretty')!r} ≠ {spec['formula']} · 아무것도 안 썼다")
        b = str(d.get("cif_text") or "").encode("utf-8")
        got[spec["file"]] = b
        files[spec["file"]] = {"material_id_asked": spec["mp"], "material_id_returned": d.get("material_id_returned"),
                               "formula_pretty": d.get("formula_pretty"), "db_version": d.get("db_version"),
                               "sha256": hashlib.sha256(b).hexdigest()}
    tmp = Path(tempfile.mkdtemp(prefix="b2o3_mp_fetch_"))
    try:                                            # 다 받은 뒤 — 임시 폴더에서 다시 읽어 조성을 본 다음에만 옮긴다
        for fn, b in got.items():
            (tmp / fn).write_bytes(b)
        for name, spec in REF_SPECS.items():
            try:
                a = read(str(tmp / spec["file"]))
            except Exception as ex:
                raise SystemExit(f"⛔ {spec['file']}: CIF 를 다시 못 읽었다 — {type(ex).__name__}: {str(ex)[:160]} · 아무것도 안 썼다")
            c, fo = composition(a), spec["formula"]
            nfu = c.get(next(iter(fo)), 0) // next(iter(fo.values()))
            if set(c) != set(fo) or nfu < 1 or any(c[el] != nfu * n for el, n in fo.items()):
                raise SystemExit(f"⛔ {spec['file']}: 다시 읽은 조성 {c} 이 {fo} 의 정수배가 아니다 · 아무것도 안 썼다")
            (files.get(spec["file"]) or copies[spec["file"]]).update({"nat": len(a), "composition": c})
        refs_dir.mkdir(parents=True, exist_ok=True)
        for fn in got:
            shutil.copyfile(tmp / fn, refs_dir / fn)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for fn, e in list(files.items()) + list(copies.items()):
        if sha256_file(refs_dir / fn) != e["sha256"]:
            raise SystemExit(f"⛔ {fn}: 쓴 파일의 sha256 이 받은 바이트와 다르다")
    rec = {"schema": KIND_MP_FETCH, "card": CARD, "decision": DECISION, "amendments": [AMEND4],
           "tool": {"path": "tools/doping/b2o3_site_dft.py", "sha256": tool_sha()},
           "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "files": files, "repo_copies": copies,
           "note": "받은 그대로 (pymatgen Structure.to cif · P1) — 고르거나 고치지 않았다 · 물은 id ≠ 돌려받은 id 면 MP 의 id 옮김 (둘 다 기록)"}
    (refs_dir / "mp_fetch.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
    return rec


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
            print("— 믹싱 (개정 1 · local-TF β 0.2 · 두 줄만)")
            t2 = pw_text(mod, t_atoms, prefix="x", calc="scf", k=[3, 3, 1], pseudo_dir="/pp", disk_io="medium", mixing="local-TF:0.2")
            d2 = [(x, y) for x, y in zip(t1.splitlines(), t2.splitlines()) if x != y]
            chk(len(d2) == 2 and d2[0][1] == "    mixing_mode = 'local-TF'" and d2[1][1] == "    mixing_beta = 0.2"
                and len(t1.splitlines()) == len(t2.splitlines()),
                "[양성] 믹싱을 주면 mixing_mode · mixing_beta 두 줄만 다르다 (local-TF · 0.2)")
            chk(pw_text(mod, t_atoms, prefix="x", calc="scf", k=[3, 3, 1], pseudo_dir="/pp", disk_io="medium", mixing=None) == t1,
                "[양성] 믹싱을 안 주면 판 고정 입력 그대로")
            chk(parse_mixing("TF:1") == ("TF", 1.0) and parse_mixing(("local-TF", 0.2)) == ("local-TF", 0.2)
                and parse_mixing(None) is None, "[양성] 꼴 둘 (문자열 · 짝) 같은 값 · None 은 판 고정")
            for bad_m in ("local-TF", "foo:0.2", "local-TF:0", "local-TF:1.5", "local-TF:nan", "local-TF:-0.1",
                          "local-TF:x", "local-TF:0.2:1", ("local-TF",), ("local-TF", True), ("local-TF", "0.2"), 0.2):
                chk(refuses(parse_mixing, bad_m), f"[음성] 잘못된 믹싱 {bad_m!r} → 멈춘다")
            import types as _ty
            fake2 = _ty.SimpleNamespace(DFT=mod.DFT, pw_input_text=lambda *a_, **k_: t0 + "    mixing_mode = 'plain'\n")
            chk(refuses(pw_text, fake2, t_atoms, prefix="x", calc="scf", k=[3, 3, 1], pseudo_dir="/pp", disk_io="medium",
                        mixing="local-TF:0.2"), "[음성] 판 고정 입력에 mixing_mode 줄이 둘 → 멈춘다 (어느 줄인지 모른다)")
            chk(not refuses(pw_text, fake2, t_atoms, prefix="x", calc="scf", k=[3, 3, 1], pseudo_dir="/pp", disk_io="medium"),
                "[양성] 믹싱을 안 바꾸면 그 줄은 안 본다 (disk_io 만)")

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
                D = fresh("oldplan")
                pj = json.loads((D / "sp_plan.json").read_text()); pj["settings"].pop("mixing", None)
                (D / "sp_plan.json").write_text(json.dumps(pj))
                chk(bool(try_rs(D, "rs_old.json").get("rows")), "[양성] 옛 계획 (settings.mixing 키 없음) → 판 고정 믹싱으로 다시 만들어 통과")
                print("— 개정 1 믹싱 — sp_inputs 계획 기록 · read_sp 가 같은 믹싱으로 다시 만들어 G2 대조")
                plm = cmd_sp_inputs(pk, T / "sp_m", pseudo_dir=str(pdir), disk_io="medium", repo_root=root, mixing="local-TF:0.2")
                tm = (T / "sp_m" / "X00" / "scf.in").read_text()
                chk(plm["settings"]["mixing"] == {"mode": "local-TF", "beta": 0.2, "decision": AMEND1}
                    and "    mixing_mode = 'local-TF'" in tm and "    mixing_beta = 0.2" in tm and "mixing_mode = 'plain'" not in tm
                    and all("mixing_mode = 'local-TF'" in (T / "sp_m" / j / "scf.in").read_text() for j in plm["jobs"]),
                    "[양성] 계획에 믹싱 (모드 · β · 개정 1) 을 적고 입력 12 개 모두에 두 줄을 넣는다")
                chk(plm["jobs"]["X00"]["scf_in_sha256"] != pl["jobs"]["X00"]["scf_in_sha256"],
                    "[양성] 믹싱이 다르면 입력 sha256 도 다르다 (옛 sp_dft 와 섞이지 않는다)")
                chk(refuses(cmd_sp_inputs, pk, T / "sp_m2", pseudo_dir=str(pdir), disk_io="medium", repo_root=root, mixing="local-TF:2")
                    and not (T / "sp_m2").exists(), "[음성] 잘못된 β → 입력 폴더를 만들기 전에 멈춘다")

                def fresh_m(tag, plan_edit=None):
                    Dm = T / f"rsm_{tag}"
                    shutil.copytree(T / "sp_m", Dm)
                    for nm in plm["jobs"]:
                        (Dm / nm / "scf.out").write_text(mod._fake_out(Dm / nm / "scf.in", E_list=[E0[nm]], stage="sp",
                                                                       pp=plm["pseudo"]["files"]))
                    if plan_edit:
                        pj_ = json.loads((Dm / "sp_plan.json").read_text()); plan_edit(pj_)
                        (Dm / "sp_plan.json").write_text(json.dumps(pj_))
                    return Dm
                vm = try_rs(fresh_m("ok"), "rsm_ok.json")
                chk(((vm.get("settings_from_plan") or {}).get("mixing") or {}).get("mode") == "local-TF"
                    and vm["sites"]["B-P"].get("relax_pick") == ["X01", "X04"] and "같은 믹싱" in vm.get("next", ""),
                    "[양성] 믹싱 계획 → 같은 믹싱으로 다시 만들어 G2 통과 · 판독 결과가 믹싱을 단계_2 로 넘긴다")
                chk(refuses(rs, fresh_m("drop", lambda q: q["settings"].__setitem__("mixing", None)), "rsm_d.json"),
                    "[음성] 계획에서 믹싱을 지우면 → 다시 만든 입력 (판 고정) 과 달라 G2 멈춤")
                chk(refuses(rs, fresh_m("beta", lambda q: q["settings"]["mixing"].__setitem__("beta", 0.3)), "rsm_b.json"),
                    "[음성] 계획의 β 를 바꾸면 → G2 멈춤")
                chk(refuses(rs, fresh_m("shape", lambda q: q["settings"].__setitem__("mixing", {"mode": "local-TF"})), "rsm_s.json"),
                    "[음성] 계획의 믹싱 꼴이 다르면 (β 없음) → 멈춘다")
                D = fresh("addmix")
                pj = json.loads((D / "sp_plan.json").read_text())
                pj["settings"]["mixing"] = {"mode": "local-TF", "beta": 0.2, "decision": AMEND1}
                (D / "sp_plan.json").write_text(json.dumps(pj))
                chk(refuses(rs, D, "rs_addmix.json"), "[음성] 판 고정 입력인데 계획에 믹싱을 덧붙이면 → G2 멈춤")

                print("— relax_inputs (단계_2 이온 이완 입력 · 고정 기준 셀 · 판독 결과 결속 · 결과 전)")
                host = root / "db" / "structures" / "modelc_V0_k663.xyz"
                cell_r, crec = site_reference_cell(mod, host)
                from ase.geometry import cell_to_cellpar as _c2p
                from ase.io import read as _rd2
                p0_, p1_ = _rd2(str(host)).repeat((1, 1, 2)).cell.cellpar(), _c2p(cell_r)
                chk(abs(crec["volume_A3"] - mod.DFT["ref_cell"]["V0_A3"]) < 1e-6 and np.allclose(p1_[3:], p0_[3:], atol=1e-8)
                    and np.allclose(p1_[:3] / p0_[:3], crec["scale"], atol=1e-10) and all(abs(x - 60.0) < 1e-3 for x in p1_[3:])
                    and crec["supercell"] == [1, 1, 2],
                    "[양성] 기준 셀 = host × (1,1,2) 를 V₀ 로 등방 스케일 (세 축 같은 배율 · 각 그대로 60°)")
                host_bad = T / "host_bad.xyz"              # 읽히는 구조 · 좌표 하나만 다름 (sha256 만 다르다)
                hb = _rd2(str(host)); hb.positions[0] += np.array([1e-3, 0.0, 0.0]); write(str(host_bad), hb, format="extxyz")
                chk(refuses(site_reference_cell, mod, host_bad), "[음성] host 가 카드 파일 (sha256) 이 아님 (좌표 하나 다름) → 멈춘다")

                def toy_ref(scale=1.0):            # 기준 셀 (× scale) 안의 장난감 — UMA 셀은 기준 셀과 조금 다르다 (실제 문턱으로 시험)
                    t_ = toy(edge=False)
                    sy_ = t_.get_chemical_symbols()
                    return Atoms(sy_, scaled_positions=[[0.0, 0.0, (i + 0.5) / len(sy_)] for i in range(len(sy_))],
                                 cell=cell_r * scale, pbc=True)

                def mk_pick_ref(D):
                    (D / "sp_selected").mkdir(parents=True)
                    files = {}
                    for i in range(12):
                        rel = f"sp_selected/X{i:02d}.xyz"
                        write(str(D / rel), toy_ref(1.02), format="extxyz")
                        files[rel] = {"sha256": sha256_file(D / rel), "site": "B-P" if i < 6 else "B-Li",
                                      "family": "O-P" if i % 2 else "O-B", "base": f"X{i:02d}", "E_uma_eV": -100.0 - i,
                                      "end_motif": "O-P"}
                    (D / "manifest.json").write_text(json.dumps({"schema": "b2o3_site_dft_sp_selected/v1",
                                                                 "purpose": PURPOSE_SP, "files": files}))
                    return D
                pk_r = mk_pick_ref(T / "pk_r")
                pl_r = cmd_sp_inputs(pk_r, T / "sp_r", pseudo_dir=str(pdir), disk_io="medium", repo_root=root,
                                     mixing="local-TF:0.2")
                for nm in pl_r["jobs"]:
                    (T / "sp_r" / nm / "scf.out").write_text(mod._fake_out(T / "sp_r" / nm / "scf.in", E_list=[E0[nm]],
                                                                           stage="sp", pp=pl_r["pseudo"]["files"]))
                try_rs(T / "sp_r", "rr.json", sp_pick=pk_r)

                def rx(out_name, sp_read=None, sp_dft=None, sp_pick=None, host_=None, pseudo=None):
                    return cmd_relax_inputs(sp_read or T / "rr.json", sp_dft or T / "sp_r", sp_pick or pk_r, host_ or host,
                                            T / out_name, pseudo_dir=str(pseudo or pdir), disk_io="medium", repo_root=root)
                rp1 = None
                try:
                    rp1 = rx("rx1")
                except SystemExit as ex:
                    print(f"    (양성 호출이 멈춤: {ex})")
                f1 = T / "rx1" / "r1_X01" / "scf.in"     # 자리 최저 (B-P X01) 의 입력 — 폴더 이름까지 본다
                ok_rx = rp1 is not None and f1.is_file()
                t1 = f1.read_text() if ok_rx else ""
                chk(ok_rx and sorted(rp1["jobs"]) == ["X01", "X04", "X06"]
                    and rp1["picks"] == {"B-P": ["X01", "X04"], "B-Li": ["X06"]}
                    and all((T / "rx1" / rp1["jobs"][j]["dir"] / "scf.in").is_file() for j in rp1["jobs"]),
                    "[양성] 자리마다 다시 고른 relax_pick 만 입력 (B-P X01 · X04 둘째 0.20 eV · B-Li X06 둘째 0.35 eV 는 창 밖)")
                chk(ok_rx and rp1["order"] == ["X01", "X06", "X04"]
                    and sorted(x.name for x in (T / "rx1").iterdir() if x.is_dir()) == ["r1_X01", "r2_X06", "r3_X04"],
                    "[양성] 폴더 순서 = 자리 최저 둘 먼저 (r1 B-P · r2 B-Li) · 둘째 (r3) 뒤 — 실행기가 이름 순으로 돈다")
                chk(ok_rx and "calculation = 'relax'" in t1 and "tstress = .true." in t1 and "ion_dynamics = 'bfgs'" in t1
                    and "mixing_mode = 'local-TF'" in t1 and "mixing_beta = 0.2" in t1 and "\n3 3 1 0 0 0\n" in t1
                    and "disk_io = 'medium'" in t1 and "forc_conv_thr" in t1,
                    "[양성] 이완 (bfgs · tstress · 판 고정 문턱) · 판독 결과의 믹싱 · k 3 3 1 · disk_io")
                if ok_rx:
                    pin = mod.parse_pw_in(T / "rx1" / "r1_X01" / "scf.in")
                    chk(np.allclose(np.asarray(pin["cell"], float), cell_r, atol=1e-8)
                        and abs(rp1["jobs"]["X01"]["geometry"]["shape_diff"]["len_rel_max"] - 0.02) < 1e-9
                        and np.abs((lambda d_: d_ - np.round(d_))(np.asarray(pin["frac"], float)
                                   - _rd2(str(pk_r / "sp_selected" / "X01.xyz")).get_scaled_positions(wrap=False))).max() < 1e-6
                        and rp1["jobs"]["X01"]["scf_in_sha256"] == sha256_file(T / "rx1" / "r1_X01" / "scf.in")
                        and rp1["sp_read"]["sha256"] == sha256_file(T / "rr.json") and rp1["ref_cell"]["supercell"] == [1, 1, 2],
                        "[양성] UMA 셀 (기준 × 1.02) → 입력 셀 = 기준 셀 · 분수 좌표 그대로 · 계획에 입력 · 판독 결과 sha256 · 기준 셀 기록")
                    chk(rx("rx2")["jobs"]["X04"]["scf_in_sha256"] == rp1["jobs"]["X04"]["scf_in_sha256"],
                        "[양성] 결정론 — 같은 인자로 다시 만든 입력이 같은 바이트")
                else:
                    chk(False, "[양성] UMA 셀 → 입력 셀 = 기준 셀 — 입력 rx1/r1_X01/scf.in 이 없다 (폴더 이름 · 순서)")
                chk(refuses(rx, "rx1"), "[음성] 비어 있지 않은 출력 폴더 → 덮지 않는다")
                vj = json.loads((T / "rr.json").read_text()); vj["sites"]["B-Li"]["relax_pick"] = ["X06", "X10"]
                (T / "rr_pick.json").write_text(json.dumps(vj))
                chk(refuses(rx, "rx3", sp_read=T / "rr_pick.json") and not (T / "rx3").exists(),
                    "[음성] 판독 결과의 relax_pick 을 고쳐도 → rows 에서 다시 고른 것과 달라 멈춘다 (아무것도 안 쓴다)")
                vj = json.loads((T / "rr.json").read_text())
                for x in vj["rows"]:
                    if x["name"] == "X10":
                        x["E_eV"] = -1.0e9
                (T / "rr_rows.json").write_text(json.dumps(vj))
                chk(refuses(rx, "rx4", sp_read=T / "rr_rows.json"), "[음성] rows 에너지만 고쳐도 → relax_pick 과 안 맞아 멈춘다")
                vj = json.loads((T / "rr.json").read_text()); vj["kind"] = "x"
                (T / "rr_kind.json").write_text(json.dumps(vj))
                chk(refuses(rx, "rx5", sp_read=T / "rr_kind.json"), "[음성] read_sp 판독 결과가 아님 (kind) → 멈춘다")
                vj = json.loads((T / "rr.json").read_text()); vj["settings_from_plan"]["mixing"] = None
                (T / "rr_mix.json").write_text(json.dumps(vj))
                chk(refuses(rx, "rx6", sp_read=T / "rr_mix.json"), "[음성] 판독 결과의 믹싱이 계획과 다름 → 멈춘다")
                vj = json.loads((T / "rr.json").read_text()); vj["relax_window_eV"] = 0.5
                (T / "rr_win.json").write_text(json.dumps(vj))
                chk(refuses(rx, "rx7", sp_read=T / "rr_win.json"), "[음성] 판독 결과의 창이 카드 (0.30 eV) 와 다름 → 멈춘다")
                Dp = T / "sp_r2"
                shutil.copytree(T / "sp_r", Dp)
                (Dp / "sp_plan.json").write_text((Dp / "sp_plan.json").read_text() + " ")
                chk(refuses(rx, "rx8", sp_dft=Dp), "[음성] 단일점 계획이 판독 뒤 바뀜 (plan sha256) → 멈춘다")
                chk(refuses(rx, "rx9", pseudo=pdir2), "[음성] 유사포텐셜 파일이 단일점 계획과 다름 → 멈춘다")
                chk(refuses(rx, "rx10", host_=host_bad), "[음성] host 가 카드 파일이 아님 → 멈춘다")
                pk_r2 = T / "pk_r2"
                shutil.copytree(pk_r, pk_r2)
                (pk_r2 / "sp_selected" / "X04.xyz").write_text((pk_r2 / "sp_selected" / "X04.xyz").read_text() + " ")
                chk(refuses(rx, "rx11", sp_pick=pk_r2) and not (T / "rx11").exists(),
                    "[음성] 둘째 이완 후보 (X04) 구조 파일이 manifest 뒤 바뀜 → 멈춘다 (앞 후보 X01 도 안 쓴다)")
                chk(refuses(relax_atoms, mod, toy(edge=False), cell_r),
                    "[음성] UMA 셀 모양이 기준 셀과 크게 다름 (10 Å 입방 ↔ 7·7·70 Å 60°) → 옮기지 않고 멈춘다")
                cl = toy_ref()
                cl.positions[1] = cl.positions[0] + np.array([0.5, 0.0, 0.0])
                chk(refuses(relax_atoms, mod, cl, cell_r), "[음성] 옮긴 뒤 원자 쌍이 1.0 Å 보다 가까움 → 멈춘다")
                sq = toy_ref()
                sq.set_cell(cell_r * np.array([[1.03], [1.03], [1.03]]), scale_atoms=True)
                chk(not refuses(relax_atoms, mod, sq, cell_r), "[양성] 셀 길이 3 % 차 (등방) 는 옮긴다 (문턱 5 %)")
                saved_bp = dict(MODELS["B-P"]); MODELS["B-P"] = {"B": 2}
                try:
                    chk(refuses(rx, "rx12"), "[음성] 조성이 모델과 다름 → 멈춘다")
                finally:
                    MODELS["B-P"] = saved_bp

                print("— ref_inputs (기준상 넷 vc-relax · 저장소 · MP 받은 기록 결속 · k = ceil(13.9/축))")
                RD = T / "refs"
                RD.mkdir()
                for sp_ in REF_SPECS.values():
                    src_ = root / (sp_["repo"] or REF_SPECS["Li3PS4_mp-985583"]["repo"])   # MP 몫은 시험용 가짜 (조성 Li₃PS₄)
                    shutil.copy(src_, RD / sp_["file"])

                def mp_meta(Dir):
                    (Dir / "mp_fetch.json").write_text(json.dumps({"schema": KIND_MP_FETCH, "files": {
                        sp_["file"]: {"sha256": sha256_file(Dir / sp_["file"]), "material_id_asked": sp_["mp"],
                                      "material_id_returned": sp_["mp"], "db_version": "selftest"}
                        for sp_ in REF_SPECS.values() if not sp_["repo"]}}))
                mp_meta(RD)
                rf = None
                try:
                    rf = cmd_ref_inputs(RD, T / "ref1", pseudo_dir=str(pdir), disk_io="low", repo_root=root)
                except SystemExit as ex:
                    print(f"    (양성 호출이 멈춤: {ex})")
                tl = (T / "ref1" / "Li2S_mp-1153" / "scf.in").read_text() if rf else ""
                chk(rf is not None and sorted(rf["jobs"]) == sorted(REF_SPECS) and tl.count("calculation = 'vc-relax'") == 1
                    and tl.count("&CELL") == 1 and "cell_dynamics = 'bfgs'" in tl and "press_conv_thr = 0.5" in tl
                    and "tstress = .true." in tl and "mixing_mode = 'plain'" in tl and "calculation = 'relax'" not in tl,
                    "[양성] 넷 다 vc-relax · &CELL bfgs 0.5 kbar · tstress · 판 고정 믹싱 (plain)")
                chk(rf is not None and rf["jobs"]["Li2S_mp-1153"]["k"] == [4, 4, 4]
                    and rf["jobs"]["Li3PS4_mp-985583"]["k"] == [3, 2, 2]
                    and rf["jobs"]["Li2S_mp-1153"]["source"]["kind"] == "repo"
                    and rf["jobs"]["Li3PS4_mp-2646995"]["source"]["kind"] == "mp_fetch",
                    "[양성] k = ceil(13.9 Å / 축) (Li₂S 원시 셀 4.01 Å → 4 4 4 · Li₃PS₄ 6.17/8.02/13.03 Å → 3 2 2) · 출처 결속")
                chk(refuses(cmd_ref_inputs, RD, T / "ref1", pseudo_dir=str(pdir), disk_io="low", repo_root=root),
                    "[음성] 비어 있지 않은 출력 폴더 → 덮지 않는다")
                R2 = T / "refs2"; shutil.copytree(RD, R2)
                (R2 / "sei_li2s_mp-1153.cif").write_text((R2 / "sei_li2s_mp-1153.cif").read_text() + "\n")
                chk(refuses(cmd_ref_inputs, R2, T / "ref2", pseudo_dir=str(pdir), disk_io="low", repo_root=root)
                    and not (T / "ref2").exists(), "[음성] 저장소에 있는 기준상 사본이 저장소 파일과 다름 → 멈춘다 (아무것도 안 쓴다)")
                R3 = T / "refs3"; shutil.copytree(RD, R3)
                (R3 / "li3ps4_mp-1097036.cif").write_text((R3 / "li3ps4_mp-1097036.cif").read_text() + "\n")
                chk(refuses(cmd_ref_inputs, R3, T / "ref3", pseudo_dir=str(pdir), disk_io="low", repo_root=root)
                    and not (T / "ref3").exists(),
                    "[음성] 마지막 기준상 (MP 받은 파일) 이 mp_fetch.json 기록 (sha256) 과 다름 → 멈춘다 (앞 셋도 안 쓴다)")
                R4 = T / "refs4"; shutil.copytree(RD, R4)
                (R4 / "mp_fetch.json").unlink()
                chk(refuses(cmd_ref_inputs, R4, T / "ref4", pseudo_dir=str(pdir), disk_io="low", repo_root=root),
                    "[음성] mp_fetch.json 이 없음 → MP 몫을 결속 못 해 멈춘다")
                R5 = T / "refs5"; shutil.copytree(RD, R5)
                shutil.copy(root / REF_SPECS["Li2S_mp-1153"]["repo"], R5 / "li3ps4_mp-2646995.cif")
                mp_meta(R5)
                chk(refuses(cmd_ref_inputs, R5, T / "ref5", pseudo_dir=str(pdir), disk_io="low", repo_root=root),
                    "[음성] Li₃PS₄ 이름에 Li₂S 구조 (조성이 화학식의 정수배가 아님) → 멈춘다")
                R6 = T / "refs6"; shutil.copytree(RD, R6)
                (R6 / "li3ps4_mp-985583.cif").unlink()
                chk(refuses(cmd_ref_inputs, R6, T / "ref6", pseudo_dir=str(pdir), disk_io="low", repo_root=root),
                    "[음성] 기준상 파일 하나 없음 → 멈춘다")

                print("— mp_fetch (저장소 둘 복사 · MP 둘 받기 (가짜 받기) · 받은 기록 · ref_inputs 로 이어짐)")
                cif_l3 = (root / REF_SPECS["Li3PS4_mp-985583"]["repo"]).read_text()
                cif_l2 = (root / REF_SPECS["Li2S_mp-1153"]["repo"]).read_text()

                def fake_mp(ret=None, formula="Li3PS4", text=None, boom_on=None):
                    def f_(mp_id):
                        if boom_on == mp_id:
                            raise RuntimeError("selftest 가짜 네트워크 오류")
                        return {"cif_text": cif_l3 if text is None else text, "material_id_returned": (ret or {}).get(mp_id, mp_id),
                                "formula_pretty": formula, "db_version": "selftest"}
                    return f_
                F1 = T / "mpf1"
                rec = None
                try:
                    rec = cmd_mp_fetch(F1, repo_root=root, fetcher=fake_mp(ret={"mp-1097036": "mp-aaaselftest"}))
                except SystemExit as ex:
                    print(f"    (양성 호출이 멈춤: {ex})")
                want_files = sorted([sp_["file"] for sp_ in REF_SPECS.values()] + ["mp_fetch.json"])
                chk(rec is not None and sorted(x.name for x in F1.iterdir()) == want_files
                    and rec["files"]["li3ps4_mp-1097036.cif"]["material_id_returned"] == "mp-aaaselftest"
                    and rec["files"]["li3ps4_mp-1097036.cif"]["material_id_asked"] == "mp-1097036"
                    and all(rec["files"][fn]["sha256"] == sha256_file(F1 / fn) for fn in rec["files"])
                    and sorted(rec["files"]) == ["li3ps4_mp-1097036.cif", "li3ps4_mp-2646995.cif"]
                    and all(sha256_file(F1 / sp_["file"]) == sha256_file(root / sp_["repo"]) for sp_ in REF_SPECS.values() if sp_["repo"]),
                    "[양성] 저장소 둘은 바이트 그대로 복사 · MP 둘은 받은 기록 (물은 id · 돌려받은 id 따로 · sha256)")
                rfp = None
                try:
                    rfp = cmd_ref_inputs(F1, T / "ref_mpf1", pseudo_dir=str(pdir), disk_io="low", repo_root=root)
                except SystemExit as ex:
                    print(f"    (양성 호출이 멈춤: {ex})")
                chk(rfp is not None and rfp["jobs"]["Li3PS4_mp-1097036"]["source"]["material_id_returned"] == "mp-aaaselftest"
                    and rfp["mp_fetch_sha256"] == sha256_file(F1 / "mp_fetch.json"),
                    "[양성] mp_fetch 가 쓴 폴더를 ref_inputs 가 그대로 받는다 (돌려받은 id · 기록 sha256 이 계획까지 간다)")
                chk(refuses(cmd_mp_fetch, F1, repo_root=root, fetcher=fake_mp()), "[음성] 비어 있지 않은 폴더 → 덮지 않는다")
                chk(refuses(cmd_mp_fetch, T / "mpf2", repo_root=root, fetcher=fake_mp(formula="Li2S")) and not (T / "mpf2").exists(),
                    "[음성] MP 가 다른 화학식을 돌려줌 → 멈춘다 (아무것도 안 쓴다)")
                chk(refuses(cmd_mp_fetch, T / "mpf3", repo_root=root, fetcher=fake_mp(text=cif_l2)) and not (T / "mpf3").exists(),
                    "[음성] 화학식은 Li₃PS₄ 라는데 받은 구조가 Li₂S → 다시 읽은 조성으로 멈춘다 (아무것도 안 쓴다)")
                chk(refuses(cmd_mp_fetch, T / "mpf4", repo_root=root, fetcher=fake_mp(boom_on="mp-1097036")) and not (T / "mpf4").exists(),
                    "[음성] 마지막 받기가 네트워크 오류 → 멈춘다 (먼저 받은 것 · 저장소 복사도 안 쓴다)")
                chk(_parse_formula("Li3PS4") == {"Li": 3, "P": 1, "S": 4} and _parse_formula("PS4Li3") == {"P": 1, "S": 4, "Li": 3}
                    and _parse_formula("Li3PS4 ") == {} and _parse_formula("li3ps4") == {} and _parse_formula(None) == {},
                    "[양성 · 음성] 화학식 읽기 — 순서는 상관없다 · 꼴이 다르면 빈 값 (멈춤으로 이어진다)")
                def refuse_msg(f_, *a_, **kw_):    # 멈춘 이유까지 본다 (다른 이유로 멈춘 것을 통과로 읽지 않게)
                    try:
                        f_(*a_, **kw_)
                    except SystemExit as ex:
                        return str(ex)
                    return ""
                saved_key = os.environ.pop("MP_API_KEY", None)
                try:
                    chk("MP_API_KEY 환경변수가 없다" in refuse_msg(cmd_mp_fetch, T / "mpf5", repo_root=root) and not (T / "mpf5").exists(),
                        "[음성] 키 (MP_API_KEY) 없음 → 그 이유로 받지 않고 멈춘다")
                finally:
                    if saved_key is not None:
                        os.environ["MP_API_KEY"] = saved_key
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
    a5.add_argument("--mixing", default=None, help="개정 1 — 예 local-TF:0.2 (안 주면 판 고정 믹싱)")
    a6 = sp.add_parser("read_sp"); a6.add_argument("--sp_dft", required=True); a6.add_argument("--sp_pick", required=True)
    a6.add_argument("--pseudo_dir", required=True); a6.add_argument("--out", required=True)
    a3 = sp.add_parser("probe"); a3.add_argument("--xyz", required=True); a3.add_argument("--out", required=True)
    a3.add_argument("--pseudo_dir", required=True); a3.add_argument("--k", type=int, nargs=3, default=[3, 3, 1])
    a3.add_argument("--disk_io", default="medium", choices=DISK_IO)
    a3.add_argument("--mixing", default=None, help="개정 1 — 예 local-TF:0.2 (안 주면 판 고정 믹싱)")
    a7 = sp.add_parser("relax_inputs", help="개정 4 — 단계_2 이온 이완 입력 (고정 기준 셀 · 판독 결과 결속)")
    a7.add_argument("--sp_read", required=True); a7.add_argument("--sp_dft", required=True)
    a7.add_argument("--sp_pick", required=True); a7.add_argument("--host", required=True)
    a7.add_argument("--pseudo_dir", required=True); a7.add_argument("--disk_io", required=True, choices=DISK_IO)
    a7.add_argument("--out", required=True)
    a8 = sp.add_parser("ref_inputs", help="개정 4 — 기준상 Li₂S · Li₃PS₄ 셋 vc-relax 입력 (저장소 · mp_fetch.json 결속)")
    a8.add_argument("--refs_dir", required=True); a8.add_argument("--pseudo_dir", required=True)
    a8.add_argument("--disk_io", required=True, choices=DISK_IO); a8.add_argument("--out", required=True)
    a9 = sp.add_parser("mp_fetch", help="개정 4 — 기준상 넷 모으기 (저장소 둘 복사 · MP 둘 받기 · mp_fetch.json · 키는 MP_API_KEY)")
    a9.add_argument("--refs_dir", required=True)
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
        pl = cmd_sp_inputs(Path(a.sp_pick), Path(a.out), pseudo_dir=a.pseudo_dir, disk_io=a.disk_io, repo_root=root,
                           mixing=a.mixing)
        for nm, j in pl["jobs"].items():
            print(f"  {nm:12s} {j['site']:5s} {j['family']} · nat {j['nat']} · scf.in {j['scf_in_sha256'][:12]}")
        print(f"단일점 입력 {len(pl['jobs'])} 개 → {a.out}/<이름>/scf.in · 계획 {a.out}/sp_plan.json (disk_io {a.disk_io} · "
              f"k {pl['settings']['k']} · 믹싱 {pl['settings']['mixing'] or '판 고정'})")
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
    if a.cmd == "relax_inputs":
        root = Path(__file__).resolve().parents[2]
        rp = cmd_relax_inputs(Path(a.sp_read), Path(a.sp_dft), Path(a.sp_pick), Path(a.host), Path(a.out),
                              pseudo_dir=a.pseudo_dir, disk_io=a.disk_io, repo_root=root)
        c = rp["ref_cell"]
        print(f"  기준 셀 host × {tuple(c['supercell'])} · 스케일 {c['scale']:.5f} · V {c['volume_A3']:.2f} Å³ (V₀ {c['V0_A3']})")
        for nm, j in rp["jobs"].items():
            g = j["geometry"]
            print(f"  {nm:12s} {j['site']:5s} {j['family']} · nat {j['nat']} · 단일점 {j['sp_E_eV']:.4f} eV · 셀 차 길이 "
                  f"{g['shape_diff']['len_rel_max'] * 100:.2f} % · 각 {g['shape_diff']['angle_deg_max']:.2f}° · 최소 쌍 "
                  f"{g['min_pair_before_A']:.3f} → {g['min_pair_after_A']:.3f} Å · scf.in {j['scf_in_sha256'][:12]}")
        mx = rp["settings"]["mixing"]
        print(f"이완 입력 {len(rp['jobs'])} 개 → {a.out}/<이름>/scf.in · 계획 {a.out}/relax_plan.json (disk_io {a.disk_io} · "
              f"k {rp['settings']['k']} · 믹싱 {mx['mode'] + ':' + str(mx['beta']) if mx else '판 고정'})")
        return 0
    if a.cmd == "mp_fetch":
        root = Path(__file__).resolve().parents[2]
        rec = cmd_mp_fetch(Path(a.refs_dir), repo_root=root)
        for fn, e in rec["files"].items():
            print(f"  {fn:24s} 물은 {e['material_id_asked']} → 돌려받은 {e['material_id_returned']} · {e['formula_pretty']} · "
                  f"nat {e['nat']} · DB {e['db_version']} · sha256 {e['sha256'][:12]}")
        for fn, e in rec["repo_copies"].items():
            print(f"  {fn:24s} 저장소 {e['path']} · nat {e['nat']} · sha256 {e['sha256'][:12]}")
        print(f"→ {a.refs_dir}/mp_fetch.json (받은 그대로 · 다형 고르기는 판독기)")
        return 0
    if a.cmd == "ref_inputs":
        root = Path(__file__).resolve().parents[2]
        pl = cmd_ref_inputs(Path(a.refs_dir), Path(a.out), pseudo_dir=a.pseudo_dir, disk_io=a.disk_io, repo_root=root)
        for nm, j in pl["jobs"].items():
            src = j["source"]
            where = src["path"] if src["kind"] == "repo" else f"MP {src['material_id_asked']} → {src['material_id_returned']}"
            print(f"  {nm:18s} nat {j['nat']:3d} · f.u. {j['n_fu']} · 축 " + " · ".join(f"{x:.3f}" for x in j["cell_lengths_A"])
                  + f" Å · k {j['k']} · {where} · scf.in {j['scf_in_sha256'][:12]}")
        print(f"기준상 vc-relax 입력 {len(pl['jobs'])} 개 → {a.out}/<이름>/scf.in · 계획 {a.out}/ref_plan.json (disk_io {a.disk_io} · 믹싱 판 고정)")
        return 0
    if a.cmd == "probe":
        root = Path(__file__).resolve().parents[2]
        cmd_probe(Path(a.xyz), Path(a.out), pseudo_dir=a.pseudo_dir, k=a.k, disk_io=a.disk_io, repo_root=root, mixing=a.mixing)
        print(f"프로브 입력 → {a.out} (disk_io {a.disk_io} · k {a.k} · 믹싱 {a.mixing or '판 고정'})")
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
