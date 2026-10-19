#!/usr/bin/env python3
"""nd_anion_removal.py — Nd@Li (6 월 선별 구조의 9 월 새 PP 판 · 120 원자) **음이온 떼어내기 / 중성 S 빈자리** 카드 도구.

카드 (숫자 · 자리 규칙 · 모드는 카드의 `기계_판독_값` 에서만 · --card 로 고른다):
  v2 (기본) db/properties/nd_s_vacancy_neutral_estimand_2026_10_20.json — 중성 S 넷 (removal_mode neutral · 전자 586)
  v1 (대체됨) db/properties/nd_anion_removal_estimand_2026_10_19.json — 전하 떼어내기 S²⁻ +2 · Cl⁻ +1 (모드 키 없음 = charged)
    ⛔ v1 은 계보 셀 (바늘 꼴 · 면 안 7 Å) 에서 배경 전하 띠 휨이 띠틈보다 커서 정의되지 않는다 — --make_inputs 가 거부한다
       (runlog nd_anion_removal_runlog_2026_10_19.json ⛔_첫_점_미수렴_진단_2026_10_20). --sites · --predict 는 기록 재현용으로 남긴다.
계보: db/raw/nd_q3_bader_2026_10_19/scf_input_copy.in (= gabia kprobe.in · sha256 adbd6f70… · Bader 와 같은 기하)

  --sites                  자리 다시 재기 (이미지 전수 최소상) + Bader 표 (반올림 최소상) 와 대조 → 어긋남 목록
  --predict [--out J]      (v1 기록) 점전하 Ewald 예측 (형식 전하 · Bader 전하) — 전하 떼기의 '방향' 예측이었다
  --make_inputs --out DIR  계보 입력에서 원자 하나 빼고 nat · prefix · outdir 만 바꾼 입력 (카드 elements 의 옆 → 먼 순서) · MANIFEST.json
  --readout --runs DIR     출력 → ΔE (옆 − 먼) · 점유 셈 · gap · 갈래 · 문장
  --selftest

v2: ΔE_vac(S) = 평균 E[셀 − S⁰_옆] − 평균 E[셀 − S⁰_먼]  (같은 셀 · 중성 · 같은 전자 수라 S 원자 기준 · 원래 셀이 빠진다)
  > 0 ⇒ Nd 옆 S 를 빼는 데 더 든다 · 갈래는 값이 겹치지 않고 |ΔE| ≥ dE_floor_eV (셀 쌍극자 이미지 상한) 일 때만 방향
  · 넷 중 일부만 부분 점유 (frac_occ_tol < f < 1 − tol) 면 상태가 섞여 '구분 안 됨' · 넷 다면 갈래 + '부분 점유' 단서

⛔ 이 도구가 못 하는 것
  · 이완하지 않는다 — 얼린 격자 (빼고 나서 이웃이 움직이는 에너지는 안 본다).
  · 절대 빈자리 · 떼어내기 에너지를 내지 않는다 — S 기준 화학 퍼텐셜 / 떼어 낸 이온의 기준 상태가 없다 (차이만 뜻이 있다).
  · '결합 하나의 에너지' 가 아니다 — 그 자리 환경 전체 + (v2) 남은 전자 2 개가 가는 곳의 차이다.
  · 남은 전자가 어디 있는지 (빈자리 · Nd 5d) 재지 않는다 — 점유 셈 · gap 만 본다 (사영 · 밀도 적분 없음).
  · 셀 쌍극자를 계산하지 않는다 — 카드 문턱 (최악 어림) 으로만 막는다.
  · 점전하 예측은 가리개 (유전 차폐) 가 없어 크기를 과대평가한다 — v1 의 **방향 (부호) 만** 예측이었다.
  · 돌리지 않는다 (러너 몫) · 4f 를 다루지 않는다 (frozen-4f PP).
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import pathlib
import re
import sys

import numpy as np

REPO = pathlib.Path(__file__).resolve().parents[2]
CARD = REPO / "db" / "properties" / "nd_s_vacancy_neutral_estimand_2026_10_20.json"
CARD_V1 = REPO / "db" / "properties" / "nd_anion_removal_estimand_2026_10_19.json"     # 대체됨 (전하 · 이 셀에서 정의 안 됨)
LINEAGE = REPO / "db" / "raw" / "nd_q3_bader_2026_10_19" / "scf_input_copy.in"
BADER_SITES = REPO / "db" / "raw" / "nd_q3_bader_2026_10_19" / "nd_bader_sites.csv"
KE = 14.399645478425668                 # e²/(4πε₀) [eV·Å]
FORMAL = {"Li": 1, "Nd": 3, "P": 5, "S": -2, "Cl": -1, "O": -2}
RY_TO_EV = 13.605693122994


def load_card(path=CARD) -> dict:
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))["기계_판독_값"]


# ───────────────────────── 기하 (기울어진 셀 · 이미지 전수) ─────────────────────────
def image_bounds(cell, rmax):
    """|n·cell| ≤ rmax 를 놓치지 않는 정수 범위 — 면간 거리 h_i = V / |a_j × a_k| 로 센다 (벡터 길이 아님)."""
    c = np.asarray(cell, float)
    V = abs(np.linalg.det(c))
    h = np.array([V / np.linalg.norm(np.cross(c[(i + 1) % 3], c[(i + 2) % 3])) for i in range(3)])
    return np.ceil(rmax / h).astype(int)


def mic_all(r1, r2, cell):
    """최소상 거리 (이미지 전수) — 분율 반올림으로 출발한 뒤 ±이미지를 다 본다 (기울어진 셀에서도 맞다)."""
    c = np.asarray(cell, float)
    inv = np.linalg.inv(c)
    d = np.asarray(r2, float) - np.asarray(r1, float)
    f = d @ inv
    f -= np.round(f)
    d0 = f @ c
    n = image_bounds(c, np.linalg.norm(d0)) + 1
    best = np.linalg.norm(d0)
    for i, j, k in itertools.product(*(range(-m, m + 1) for m in n)):
        best = min(best, float(np.linalg.norm(d0 + i * c[0] + j * c[1] + k * c[2])))
    return best


def mic_round(r1, r2, cell):
    """반올림 최소상 (Bader 도구 bader_summary_zval.mic_dist 와 같은 셈) — 대조용."""
    c = np.asarray(cell, float)
    f = (np.asarray(r2, float) - np.asarray(r1, float)) @ np.linalg.inv(c)
    f -= np.round(f)
    return float(np.linalg.norm(f @ c))


def read_lineage(path=LINEAGE):
    from ase.io import read
    at = read(str(path), format="espresso-in")
    return at


def classify(at, card) -> list[dict]:
    """Bader 사전등록 거리 (R_PS · R_NdX · R_NdO) 로 자리를 다시 나눈다 — 이미지 전수 최소상."""
    r = card["site_rules"]
    sym = at.get_chemical_symbols()
    pos = at.get_positions()
    cell = at.cell.array
    nd = [i for i, s in enumerate(sym) if s == "Nd"]
    P = [i for i, s in enumerate(sym) if s == "P"]
    rows = []
    for i, s in enumerate(sym):
        if s not in ("S", "Cl", "O"):
            continue
        dnd = min(mic_all(pos[i], pos[j], cell) for j in nd)
        dnd_r = min(mic_round(pos[i], pos[j], cell) for j in nd)
        dP = min(mic_all(pos[i], pos[j], cell) for j in P)
        if s == "S":
            kind = "S_PS4" if dP <= r["R_PS"] else "S_free"
            near = dnd <= r["R_NdX"]
        elif s == "Cl":
            kind, near = "Cl", dnd <= r["R_NdX"]
        else:
            kind, near = "O_P", dnd <= r["R_NdO"]
        nli = sum(1 for j, t in enumerate(sym) if t == "Li" and mic_all(pos[i], pos[j], cell) <= r["R_LiX_coord"])
        rows.append({"index": i + 1, "element": s, "kind": kind, "near": bool(near),
                     "category": kind + ("_nearNd" if near else ""), "d_Nd_min_A": round(dnd, 4),
                     "d_Nd_round_A": round(dnd_r, 4), "d_P_min_A": round(dP, 4), "n_Li": nli})
    return rows


def select_sites(rows, card) -> dict:
    """카드 규칙: 자유 S 옆 전부 · 먼 전부 / Cl 옆 전부 · 먼 = Nd 최소거리가 가장 큰 둘 (같으면 번호 작은 쪽)."""
    k = int(card["far_cl_n"])
    fs_near = [r["index"] for r in rows if r["kind"] == "S_free" and r["near"]]
    fs_far = [r["index"] for r in rows if r["kind"] == "S_free" and not r["near"]]
    cl_near = [r["index"] for r in rows if r["kind"] == "Cl" and r["near"]]
    cl_far_all = sorted([r for r in rows if r["kind"] == "Cl" and not r["near"]],
                        key=lambda r: (-r["d_Nd_min_A"], r["index"]))
    return {"S": {"near": sorted(fs_near), "far": sorted(fs_far)},
            "Cl": {"near": sorted(cl_near), "far": sorted(r["index"] for r in cl_far_all[:k])}}


def bader_crosscheck(rows, path=BADER_SITES) -> list[dict]:
    """Bader 표 (반올림 최소상) 의 범주 · 거리와 이미지 전수 재계산을 대조 — 다른 원자 목록."""
    import csv
    bad = []
    by = {r["index"]: r for r in rows}
    with open(path, newline="") as f:
        for b in csv.DictReader(f):
            i = int(b["index"])
            if i not in by:
                continue
            r = by[i]
            cat_b = b["category"]
            if cat_b != r["category"] or abs(float(b["d_Nd_min_A"]) - r["d_Nd_min_A"]) > 1e-3:
                bad.append({"index": i, "element": r["element"], "bader_category": cat_b, "now_category": r["category"],
                            "bader_d_Nd": float(b["d_Nd_min_A"]), "now_d_Nd": r["d_Nd_min_A"]})
    return bad


# ───────────────────────── 점전하 Ewald (기울어진 셀) ─────────────────────────
def ewald_potentials(cell, pos, q, alpha=None, tol=1e-12):
    """φ_i [V] — 다른 모든 전하 (자기 이미지 포함 · 자기 자신 제외) 가 자리 i 에 만드는 퍼텐셜. 중성 셀만.

    실공간 이미지 범위 = 면간 거리로 센 (rcut + 셀 변 길이 합) — 보수적 여유라 위치가 셀 어디에 있어도 빠지지 않는다.
    역공간 범위 = |m_i| ≤ kcut·|a_i| / 2π (a_i·G = 2π m_i 에서). 검증 = NaCl 마델룽 (입방 · 60° 원시 · 길고 기울어진 7 배 셀) ·
    α 무관성 (selftest). ⚠ 여유가 커서 '면간 거리 대신 벡터 길이' 로 바꿔도 이 시험들은 통과한다 — 그 차이를 가르는 시험은 없다."""
    c = np.asarray(cell, float)
    pos = np.asarray(pos, float)
    q = np.asarray(q, float)
    if abs(q.sum()) > 1e-8:
        raise ValueError(f"⛔ 셀 전하 {q.sum():.3e} ≠ 0 — 중성으로 맞춘 뒤 부른다")
    N, V = len(q), abs(np.linalg.det(c))
    frac = pos @ np.linalg.inv(c)
    frac -= np.floor(frac)
    pos = frac @ c
    if alpha is None:
        alpha = math.sqrt(math.pi) * (N / V ** 2) ** (1.0 / 6.0)
    s = math.sqrt(-math.log(tol))
    rcut, kcut = s / alpha, 2.0 * alpha * s
    from scipy.special import erfc
    D = float(np.linalg.norm(c, axis=1).sum())
    n = image_bounds(c, rcut + D)
    L = np.array([i * c[0] + j * c[1] + k * c[2] for i, j, k in itertools.product(*(range(-m, m + 1) for m in n))])
    phi = np.zeros(N)
    dij = pos[None, :, :] - pos[:, None, :]                         # r_j − r_i
    for Lv in L:
        r = np.linalg.norm(dij + Lv, axis=2)
        m = (r > 1e-10) & (r < rcut)
        t = np.zeros_like(r)
        t[m] = erfc(alpha * r[m]) / r[m]
        phi += (t * q[None, :]).sum(axis=1)
    B = 2.0 * math.pi * np.linalg.inv(c).T
    nk = np.ceil(kcut * np.linalg.norm(c, axis=1) / (2.0 * math.pi)).astype(int)
    G = np.array([i * B[0] + j * B[1] + k * B[2] for i, j, k in itertools.product(*(range(-m, m + 1) for m in nk))
                  if (i, j, k) != (0, 0, 0)])
    G2 = (G ** 2).sum(axis=1)
    keep = G2 <= kcut ** 2
    G, G2 = G[keep], G2[keep]
    w = 4.0 * math.pi / V * np.exp(-G2 / (4.0 * alpha ** 2)) / G2
    ph = pos @ G.T                                                   # N × K
    Sc, Ss = (q[:, None] * np.cos(ph)).sum(axis=0), (q[:, None] * np.sin(ph)).sum(axis=0)
    phi += (np.cos(ph) * Sc[None, :] + np.sin(ph) * Ss[None, :]) @ w
    phi -= 2.0 * alpha / math.sqrt(math.pi) * q
    return KE * phi


def predict(at, sel, card, bader_csv=BADER_SITES) -> dict:
    """점전하 떼어내기 예측: E_rm^pc(i) = −q_i^형식 · φ_i (자기 이미지 항은 같은 q 끼리 같아 차에서 상쇄)."""
    import csv
    sym = at.get_chemical_symbols()
    pos, cell = at.get_positions(), at.cell.array
    out = {}
    qf = np.array([FORMAL[s] for s in sym], float)
    qb = np.zeros(len(sym))
    with open(bader_csv, newline="") as f:
        for b in csv.DictReader(f):
            qb[int(b["index"]) - 1] = float(b["net_e"])
    qb -= qb.mean()                                                  # 중성으로 (+0.025 e 를 고르게)
    for name, q in (("형식_전하", qf), ("Bader_전하", qb)):
        phi = ewald_potentials(cell, pos, q)
        rec = {}
        for el in ("S", "Cl"):
            e = lambda idx: [float(-FORMAL[el] * phi[i - 1]) for i in idx]
            near, far = e(sel[el]["near"]), e(sel[el]["far"])
            rec[el] = {"near_eV": near, "far_eV": far, "dE_near_minus_far_eV": float(np.mean(near) - np.mean(far)),
                       "sign": "옆이 더 든다" if np.mean(near) > np.mean(far) else "옆이 덜 든다"}
        out[name] = rec
    out["⛔"] = "점전하 · 차폐 없음 (ε = 1) — 크기 과대 · 방향만 예측 · 결과 전 기록"
    return out


# ───────────────────────── 입력 · 판독 ─────────────────────────
def removal_input(text, idx, el, card, pseudo_dir=None) -> str:
    """계보 입력에서 원자 idx (1 부터) 하나를 빼고 nat · prefix · outdir 만 바꾼다 (charged 카드면 tot_charge 줄을 더한다).
    pseudo_dir 를 주면 그 줄도 바꾼다 (실행 기계의 PAW 폴더 · 시험 폴더) — 차이 검사가 그 값일 때만 허용한다."""
    lines = text.splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.strip().upper().startswith("ATOMIC_POSITIONS"))
    atoms = [i for i in range(i0 + 1, len(lines)) if re.match(r"^\s*[A-Z][a-z]?\s+[-\d.]+\s+[-\d.]+\s+[-\d.]+\s*$", lines[i])]
    nat = int(re.search(r"nat\s*=\s*(\d+)", text).group(1))
    if len(atoms) != nat:
        raise ValueError(f"⛔ 원자 줄 {len(atoms)} ≠ nat {nat}")
    li = atoms[idx - 1]
    if lines[li].split()[0] != el:
        raise ValueError(f"⛔ 원자 {idx} 는 {lines[li].split()[0]} 이다 ({el} 아님)")
    charged = mode_of(card) == "charged"
    tag = f"rm_{el}{idx}"
    out = []
    for i, l in enumerate(lines):
        if i == li:
            continue
        if re.match(r"^\s*prefix\s*=", l):
            l = f"  prefix='{tag}'"
        elif re.match(r"^\s*outdir\s*=", l):
            l = f"  outdir='./tmp_{tag}/'"
        elif pseudo_dir is not None and re.match(r"^\s*pseudo_dir\s*=", l):
            l = f"  pseudo_dir='{pseudo_dir}'"
        elif re.match(r"^\s*nat\s*=", l):
            l = f"  nat={nat - 1}"
            if charged:
                out.append(l)
                l = f"  tot_charge={card['tot_charge'][el]:+.1f}"
        out.append(l)
    return "\n".join(out) + "\n"


def mode_of(card) -> str:
    """카드 모드 — v2 는 'neutral' 을 적는다 · 키가 없으면 v1 (charged)."""
    return card.get("removal_mode", "charged")


def input_diff_ok(orig, new, pseudo_dir=None, charged=False) -> list[str]:
    """줄 단위 차이가 prefix · outdir · nat · 원자 한 줄(삭제) 뿐인가 (charged 면 tot_charge 추가도 · 준 pseudo_dir 값 그대로일 때만 그 줄)."""
    import difflib
    allow = re.compile(r"^\s*(prefix|outdir|nat" + ("|tot_charge" if charged else "") + r")\s*=")
    pd_ok = re.compile(r"^\s*pseudo_dir\s*=")
    bad, removed_atoms = [], 0
    for d in difflib.ndiff(orig.splitlines(), new.splitlines()):
        if d.startswith("? ") or d.startswith("  "):
            continue
        body = d[2:]
        if allow.match(body):
            continue
        if pseudo_dir is not None and pd_ok.match(body) and (d.startswith("- ") or body.strip() == f"pseudo_dir='{pseudo_dir}'"):
            continue
        if d.startswith("- ") and re.match(r"^\s*[A-Z][a-z]?\s+[-\d.]+\s+[-\d.]+\s+[-\d.]+\s*$", body):
            removed_atoms += 1
            continue
        bad.append(d)
    if removed_atoms != 1:
        bad.append(f"지운 원자 줄 {removed_atoms} ≠ 1")
    return bad


def make_inputs(card, text, out, pseudo_dir=None, lineage="") -> dict:
    """카드 elements 의 옆 → 먼 자리마다 rm_<El><idx>/scf.in + MANIFEST.json (그 순서가 러너의 실행 순서 · 첫 줄이 탐침).
    ⛔ charged (v1) 카드는 거부한다 — 이 셀에서 정의되지 않는다 (바늘 셀 배경 전하 띠 휨 > 띠틈)."""
    if mode_of(card) != "neutral":
        raise SystemExit("⛔ 전하 떼어내기 카드 (v1) 는 대체됐다 — 바늘 셀 (면 안 7 Å) 에서 배경 전하 띠 휨이 띠틈보다 커 정의되지 않는다 "
                         "(runlog nd_anion_removal_runlog_2026_10_19.json ⛔_첫_점_미수렴_진단_2026_10_20) · 중성 카드 v2 로")
    if hashlib.sha256(text.encode()).hexdigest() != card["lineage_sha256"]:
        raise SystemExit(f"⛔ 계보 입력 sha256 ≠ 카드 ({lineage}) — 다른 기하다")
    man = {"lineage": str(lineage), "lineage_sha256": card["lineage_sha256"], "pseudo_dir": pseudo_dir,
           "removal_mode": mode_of(card), "n_electrons_after": card["n_electrons_after"], "inputs": []}
    for el in card["elements"]:
        for side in ("near", "far"):
            for idx in card["selected"][el][side]:
                t = removal_input(text, idx, el, card, pseudo_dir)
                b = input_diff_ok(text, t, pseudo_dir)
                if b:
                    raise SystemExit(f"⛔ rm_{el}{idx}: 허용 밖 차이 {b[:3]}")
                d = pathlib.Path(out) / f"rm_{el}{idx}"
                d.mkdir(parents=True, exist_ok=True)
                (d / "scf.in").write_text(t)
                man["inputs"].append({"dir": d.name, "element": el, "side": side, "index": idx,
                                      "sha256": hashlib.sha256(t.encode()).hexdigest()})
    (pathlib.Path(out) / "MANIFEST.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    return man


_NUM = re.compile(r"-?\d+\.\d+")          # QE f9.4 는 음수가 붙어 나온다 (-40.1000-12.2000) — 소수점으로 끊는다


def read_occupations(t) -> list[tuple[list[float], list[float]]]:
    """마지막 'End of self-consistent calculation' 뒤 k 점마다 (고유값 eV, 점유) — verbosity high 출력.
    못 찾으면 [] (부르는 쪽이 '없음' 으로 죽인다 — 0 으로 두지 않는다)."""
    i = t.rfind("End of self-consistent calculation")
    if i < 0:
        return []
    ks, mode, e, f = [], None, [], []
    for line in t[i:].splitlines():
        if "bands (ev)" in line:
            if e or f:
                ks.append((e, f))
            mode, e, f = "e", [], []
        elif "occupation numbers" in line:
            mode = "f"
        elif "Fermi energy" in line or "highest occupied" in line or line.lstrip().startswith("!"):
            break
        elif mode == "e":
            e += [float(x) for x in _NUM.findall(line)]
        elif mode == "f":
            f += [float(x) for x in _NUM.findall(line)]
    if e or f:
        ks.append((e, f))
    return ks


def read_out(path, tol=0.02) -> dict:
    t = pathlib.Path(path).read_text(errors="replace")
    if t.count("JOB DONE") != 1 or len(re.findall(r"Program PWSCF .*? starts on", t)) > 1:
        raise ValueError("JOB DONE 이 정확히 하나가 아니다 (실행이 붙었거나 안 끝났다)")
    if "convergence has been achieved" not in t:
        raise ValueError("SCF 미수렴")
    E = re.findall(r"^!\s+total energy\s+=\s+([-\d.]+)\s+Ry", t, re.M)
    ne = re.findall(r"number of electrons\s+=\s+([-\d.]+)", t)
    if not E or not ne:
        raise ValueError("총에너지 · 전자 수 줄이 없다")
    ks = read_occupations(t)
    if not ks:
        raise ValueError("점유 줄이 없다 (verbosity high 인데 'occupation numbers' 블록을 못 찾음)")
    if any(len(e) != len(f) or not e for e, f in ks):
        raise ValueError(f"고유값 · 점유 수가 k 점마다 안 맞는다 ({[(len(e), len(f)) for e, f in ks]})")
    frac = sum(1 for e, f in ks for x in f if tol < x < 1 - tol)
    occ = [x for e, f in ks for x, y in zip(e, f) if y > 0.5]
    emp = [x for e, f in ks for x, y in zip(e, f) if y <= 0.5]
    gap = (min(emp) - max(occ)) if occ and emp else None
    return {"E_eV": float(E[-1]) * RY_TO_EV, "n_electrons": float(ne[0]), "n_k": len(ks), "n_frac": frac,
            "homo_eV": max(occ) if occ else None, "lumo_eV": min(emp) if emp else None,
            "gap_eV": gap}


def readout(runs, card) -> dict:
    """runs/<rm_ElIdx>/scf.out → 원소마다 ΔE · 점유 셈 · gap · 갈래 (상태 규칙 → 겹침 → 문턱)."""
    sel, tol = card["selected"], float(card.get("frac_occ_tol", 0.02))
    floor = float(card.get("dE_floor_eV", 0.0))
    res = {}
    for el in card.get("elements", ("S", "Cl")):
        vals, cells = {}, {}
        for side in ("near", "far"):
            vals[side] = []
            for idx in sel[el][side]:
                o = read_out(pathlib.Path(runs) / f"rm_{el}{idx}" / "scf.out", tol)
                if abs(o["n_electrons"] - float(card["n_electrons_after"])) > 1e-6:
                    raise ValueError(f"⛔ rm_{el}{idx}: 전자 수 {o['n_electrons']} ≠ {card['n_electrons_after']}")
                vals[side].append(o["E_eV"])
                cells[f"rm_{el}{idx}"] = {k: o[k] for k in ("n_frac", "gap_eV", "homo_eV", "lumo_eV", "n_k")}
        n, f = vals["near"], vals["far"]
        d = float(np.mean(n) - np.mean(f))
        fr = [c["n_frac"] > 0 for c in cells.values()]
        caveat = ""
        if any(fr) and not all(fr):
            br = "구분 안 됨"
            caveat = "상태가 섞임 (일부만 부분 점유)"
        else:
            if min(n) > max(f) and d >= floor:
                br = "옆이 더 세게"
            elif max(n) < min(f) and d <= -floor:
                br = "옆이 덜"
            else:
                br = "구분 안 됨"
            if all(fr):
                caveat = "넷 다 부분 점유 (금속성)"
        res[el] = {"E_near_eV": n, "E_far_eV": f, "dE_eV": d, "spread_near_eV": float(np.ptp(n)),
                   "spread_far_eV": float(np.ptp(f)), "floor_eV": floor, "cells": cells, "branch": br,
                   "caveat": caveat, "sentence": sentence(el, d, br, len(n), len(f), mode_of(card), floor, caveat)}
    return res


def sentence(el, d, br, nn, nf, mode="charged", floor=0.0, caveat="") -> str:
    tail = f" ({caveat})" if caveat else ""
    if mode == "neutral":
        what, cond = "자유 S", "같은 셀 · 얼린 격자 · 중성 (닫힌 껍질) 에서"
        if br == "옆이 더 세게":
            return (f"{cond} Nd 옆 {what} 를 빼는 데 (빈자리 에너지) Li 만 이웃한 {what} 보다 {d:.2f} eV 더 든다 "
                    f"(n {nn} 대 {nf} · 값이 겹치지 않음 · 문턱 {floor:.1f} eV 넘음) — 이 모델 · 이 셀에서 Nd 옆 S 가 더 단단히 붙잡혀 있다.{tail}")
        if br == "옆이 덜":
            return (f"{cond} Nd 옆 {what} 를 빼는 데 {abs(d):.2f} eV 덜 든다 (n {nn} 대 {nf} · 값이 겹치지 않음 · 문턱 {floor:.1f} eV 넘음)"
                    f" — 이 모델 · 이 셀에서 Nd 옆 S 가 오히려 빠지기 쉽다.{tail}")
        return f"{cond} Nd 옆 · 먼 {what} 의 빈자리 에너지는 이 표본 (n {nn} 대 {nf}) 으로 구분되지 않는다 (차 {d:+.2f} eV).{tail}"
    ion = {"S": "자유 S²⁻", "Cl": "Cl⁻"}[el]
    if br == "옆이 더 세게":
        return (f"같은 셀 · 같은 전하 · 얼린 격자에서 Nd 옆 {ion} 를 떼어 내는 데 Li 만 이웃한 같은 이온보다 {d:.2f} eV 더 든다 "
                f"(n {nn} 대 {nf} · 값이 겹치지 않음) — 이 모델 · 이 셀에서 Nd 가 이웃 음이온을 더 세게 붙잡는다.")
    if br == "옆이 덜":
        return (f"같은 셀 · 같은 전하 · 얼린 격자에서 Nd 옆 {ion} 를 떼어 내는 데 {abs(d):.2f} eV 덜 든다 "
                f"(n {nn} 대 {nf} · 값이 겹치지 않음) — 이 모델 · 이 셀에서 Nd 옆 음이온이 오히려 덜 붙잡혀 있다.")
    return f"같은 셀 · 같은 전하 · 얼린 격자에서 Nd 옆 · 먼 {ion} 의 떼어내기 에너지는 이 표본 (n {nn} 대 {nf}) 으로 구분되지 않는다 (차 {d:+.2f} eV)."


# ───────────────────────── selftest ─────────────────────────
def _selftest() -> int:
    import tempfile
    ok = [0, 0]

    def chk(c, m):
        print(("  ✓ " if c else "  ✗ ") + m)
        ok[0 if c else 1] += 1

    M_NACL = 1.747564594633
    a = 2.0                                       # 이웃 거리 r0 = 1
    conv = a * np.eye(3)
    na = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0]]) * a
    pos = np.vstack([na, na + [a / 2, 0, 0]])
    q = np.array([1] * 4 + [-1] * 4, float)
    M1 = -ewald_potentials(conv, pos, q)[0] * 1.0 / KE
    chk(abs(M1 - M_NACL) < 1e-6, f"[양성] NaCl 입방 8 원자 → 마델룽 {M1:.9f}")
    prim = a * np.array([[0, .5, .5], [.5, 0, .5], [.5, .5, 0]])
    p2 = np.array([[0, 0, 0], 0.5 * prim.sum(axis=0)])
    M2 = -ewald_potentials(prim, p2, np.array([1., -1.]))[0] / KE
    chk(abs(M2 - M_NACL) < 1e-6, f"[양성] NaCl 원시 (60° 기울어진) 셀 → 마델룽 {M2:.9f}")
    sup = prim.copy(); sup[2] = 7 * prim[2] + 3 * prim[0]       # 길고 크게 기울어진 1×1×7 꼴 (Nd 셀처럼)
    fr = [(0, 0, 0)]
    pts, qs = [], []
    for m in range(7):
        for s_, qq in ((np.zeros(3), 1.0), (0.5 * prim.sum(axis=0), -1.0)):
            pts.append(s_ + m * prim[2] + (m * 3 // 7) * 0 * prim[0]); qs.append(qq)
    pts = np.array(pts)
    M3 = -ewald_potentials(sup, pts, np.array(qs))[0] / KE
    chk(abs(M3 - M_NACL) < 1e-6, f"[양성] NaCl 길고 기울어진 7 배 셀 → 마델룽 {M3:.9f}")
    Ma = -ewald_potentials(conv, pos, q, alpha=0.9)[0] / KE
    Mb = -ewald_potentials(conv, pos, q, alpha=1.6)[0] / KE
    chk(abs(Ma - Mb) < 1e-8, "[양성] α 를 바꿔도 같다 (0.9 · 1.6)")
    try:
        ewald_potentials(conv, pos, q + 0.1)
        chk(False, "[음성] 비중성 셀 → 죽어야 한다")
    except ValueError:
        chk(True, "[음성] 비중성 셀 → ValueError")
    # 최소상: 이 셀에서 반올림이 실제로 틀리는 쌍 (Nd2–S45 · ELF 표본 도구가 빠뜨린 그 결합) 을 이미지 전수는 잡는다
    #   ⚠ 처음엔 손으로 만든 기울어진 셀 예를 썼는데 반올림도 맞게 나와 시험이 아무것도 못 쟀다 → 실물 쌍으로 바꿈
    card = load_card()
    at = read_lineage()
    sk, pp_ = at.cell.array, at.get_positions()
    r1, r2 = pp_[1], pp_[44]                                       # 원자 2 (Nd) · 45 (S)
    dr, da = mic_round(r1, r2, sk), mic_all(r1, r2, sk)
    brute = min(np.linalg.norm(r2 - r1 + i * sk[0] + j * sk[1] + k * sk[2])
                for i in range(-15, 16) for j in range(-15, 16) for k in range(-2, 3))
    chk(at.get_chemical_symbols()[1] == "Nd" and at.get_chemical_symbols()[44] == "S"
        and abs(da - brute) < 1e-9 and dr > da + 1.0,
        f"[음성] 실물 Nd2–S45: 반올림 {dr:.3f} Å · 전수 {da:.3f} Å = 무차별 {brute:.3f}")
    # 계보 · 자리 · 입력 (v2 = 기본 카드 · 중성 S)
    chk(card.get("removal_mode") == "neutral" and card["elements"] == ["S"] and card["n_electrons_after"] == 586,
        "[양성] 기본 카드 = v2 (중성 · S 만 · 전자 586)")
    chk(hashlib.sha256(LINEAGE.read_bytes()).hexdigest() == card["lineage_sha256"], "[양성] 계보 입력 sha256 = 카드")
    rows = classify(at, card)
    sel = select_sites(rows, card)
    chk(sel == card["selected"], f"[양성] 카드 규칙으로 고른 자리 = 카드 기록 {sel}")
    text = LINEAGE.read_text()
    new = removal_input(text, sel["S"]["near"][0], "S", card)
    chk(input_diff_ok(text, new) == [] and "tot_charge" not in new and "nat=119" in new,
        "[양성] 중성 S 입력: 줄 차이가 prefix · outdir · nat · 원자 한 줄뿐 · tot_charge 없음 · nat 119")
    chk(any("tot_charge" in b for b in input_diff_ok(text, new.replace("  nat=119", "  nat=119\n  tot_charge=+2.0"))),
        "[음성] 중성 입력에 tot_charge 가 끼면 줄 차이 검사가 잡는다")
    v1 = load_card(CARD_V1)
    old = removal_input(text, sel["S"]["near"][0], "S", v1)
    chk("tot_charge=+2.0" in old and input_diff_ok(text, old, charged=True) == [],
        "[양성] v1 (기록) 생성기는 그대로 — S²⁻ → tot_charge +2 (charged 검사에서만 허용)")
    chk(any("ecutwfc" in b for b in input_diff_ok(text, new.replace("ecutwfc=70.0", "ecutwfc=60.0"))),
        "[음성] ecutwfc 를 바꾸면 줄 차이 검사가 잡는다")
    new_pd = removal_input(text, sel["S"]["near"][0], "S", card, "/tmp/paw")
    chk(input_diff_ok(text, new_pd, "/tmp/paw") == [] and "pseudo_dir='/tmp/paw'" in new_pd,
        "[양성] pseudo_dir 를 준 값으로 바꾸면 그 줄은 허용")
    chk(input_diff_ok(text, new_pd) != [], "[음성] pseudo_dir 를 안 준 검사에서는 pseudo_dir 줄 차이도 잡는다")
    try:
        removal_input(text, sel["S"]["near"][0], "Cl", card)
        chk(False, "[음성] 원소가 다른 번호 → 죽어야 한다")
    except ValueError:
        chk(True, "[음성] 원소가 다른 번호 → ValueError")
    td = pathlib.Path(tempfile.mkdtemp())
    man = make_inputs(card, text, td / "mk", "/tmp/paw", "x")
    chk([m["dir"] for m in man["inputs"]] == ["rm_S51", "rm_S112", "rm_S54", "rm_S115"]
        and len(list((td / "mk").glob("rm_*/scf.in"))) == 4,
        "[양성] make_inputs: 넷 · 옆 → 먼 순서 (첫 줄 = 탐침 rm_S51) · MANIFEST")
    try:                                           # elements 를 붙인 v1 — 거부 줄 말고 다른 데서 우연히 죽지 않게 (KeyError)
        make_inputs(dict(v1, elements=["S", "Cl"]), text, td / "mk1", None, "x")
        chk(False, "[음성] v1 (전하) 카드로 입력 만들기 → 거부해야 한다")
    except SystemExit as e:
        chk("대체" in str(e) and not (td / "mk1").exists(), "[음성] v1 (전하) 카드 → 거부 · 아무것도 안 만든다")
    try:
        make_inputs(card, text + "\n", td / "mk2", None, "x")
        chk(False, "[음성] 계보 sha 다름 → 거부해야 한다")
    except SystemExit:
        chk(True, "[음성] 계보 sha 다름 → 거부")
    # 점유 읽기 (QE f9.4 붙은 음수 · k 점 둘)
    occ_ok = ("     End of self-consistent calculation\n\n          k = 0.0000 0.0000 0.0000 ( 24512 PWs)   bands (ev):\n\n"
              "  -40.1000-12.2000   1.5000   2.0000   4.6000   5.1000\n\n     occupation numbers\n"
              "     1.0000   1.0000   1.0000   1.0000   0.0000   0.0000\n\n"
              "          k = 0.3333 0.0000 0.0000 ( 24498 PWs)   bands (ev):\n\n"
              "  -40.0500 -12.1000   1.6000   2.1000   4.7000   5.2000\n\n     occupation numbers\n"
              "     1.0000   1.0000   1.0000   1.0000   0.0000   0.0000\n\n     the Fermi energy is     3.1000 ev\n")
    try:
        ks = read_occupations(occ_ok)
    except ValueError as e:                        # 끊는 규칙이 틀리면 float 변환에서 죽는다 — 죽어도 ✗ 로 센다
        ks = []; print(f"    ({e})")
    chk(len(ks) == 2 and [len(e) for e, f in ks] == [6, 6] and ks[0][0][:2] == [-40.1, -12.2],
        "[양성] 점유 읽기: k 둘 · 고유값 여섯 · 붙은 음수 (-40.1000-12.2000) 를 둘로 끊는다")
    occ_frac = occ_ok.replace("1.0000   1.0000   1.0000   1.0000   0.0000   0.0000\n\n     the",
                              "1.0000   1.0000   1.0000   0.5000   0.5000   0.0000\n\n     the")

    def fake(name, E, ne=None, conv=True, occ=occ_ok):
        d = td / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "scf.out").write_text("     Program PWSCF v.7.4.1 starts on x\n"
                                   f"     number of electrons       =   {ne or card['n_electrons_after']:.2f}\n"
                                   + ("     convergence has been achieved in  10 iterations\n" if conv else "")
                                   + occ + f"!    total energy              =   {E / RY_TO_EV:.8f} Ry\n     JOB DONE.\n")
    near, far = card["selected"]["S"]["near"], card["selected"]["S"]["far"]
    for i in near:
        fake(f"rm_S{i}", -100.0 + 0.5)
    for i in far:
        fake(f"rm_S{i}", -100.0)
    r = readout(td, card)
    chk(set(r) == {"S"} and r["S"]["branch"] == "옆이 더 세게" and abs(r["S"]["dE_eV"] - 0.5) < 1e-6
        and r["S"]["cells"][f"rm_S{near[0]}"]["n_frac"] == 0 and abs(r["S"]["cells"][f"rm_S{near[0]}"]["gap_eV"] - 2.5) < 1e-9,
        "[양성] 옆 둘 다 0.5 eV 위 · 문턱 0.3 넘음 → '옆이 더 세게' · 점유 셈 0 · gap 2.5 (최고 점유 2.1 · 최저 빈 4.6)")
    chk("빈자리 에너지" in r["S"]["sentence"] and "더 단단히" in r["S"]["sentence"], "[양성] 중성 문장 (빈자리 에너지)")
    for i in near:
        fake(f"rm_S{i}", -100.0 + 0.2)
    chk(readout(td, card)["S"]["branch"] == "구분 안 됨", "[음성] 겹치지 않아도 |ΔE| 0.2 < 문턱 0.3 → '구분 안 됨'")
    for i in near:
        fake(f"rm_S{i}", -100.0 - 0.5)
    chk(readout(td, card)["S"]["branch"] == "옆이 덜", "[양성] 옆 둘 다 0.5 eV 아래 → '옆이 덜'")
    fake(f"rm_S{near[0]}", -100.0 - 0.5, occ=occ_frac)
    rr = readout(td, card)["S"]
    chk(rr["branch"] == "구분 안 됨" and "섞임" in rr["caveat"], "[음성] 넷 중 하나만 부분 점유 → '구분 안 됨 (상태가 섞임)'")
    for i in near + far:
        fake(f"rm_S{i}", -100.0 - (0.5 if i in near else 0.0), occ=occ_frac)
    rr = readout(td, card)["S"]
    chk(rr["branch"] == "옆이 덜" and "금속성" in rr["caveat"] and "금속성" in rr["sentence"],
        "[양성] 넷 다 부분 점유 → 갈래는 내고 '부분 점유 (금속성)' 단서")
    for i in near + far:
        fake(f"rm_S{i}", -100.0 + (0.5 if i in near else 0.0))
    fake(f"rm_S{near[1]}", -100.0 - 0.2)                              # 옆 하나가 먼 값 아래로 → 겹침
    chk(readout(td, card)["S"]["branch"] == "구분 안 됨", "[음성] 옆 하나가 먼 값과 겹치면 '구분 안 됨'")
    fake(f"rm_S{near[1]}", -100.0, conv=False)
    try:
        readout(td, card)
        chk(False, "[음성] 미수렴 출력 → 죽어야 한다")
    except ValueError:
        chk(True, "[음성] 미수렴 출력 → ValueError")
    fake(f"rm_S{near[1]}", -100.0, ne=584)
    try:
        readout(td, card)
        chk(False, "[음성] 전자 584 (전하 셀) → 죽어야 한다")
    except ValueError:
        chk(True, "[음성] 전자 584 (전하 셀 · v1 출력) → ValueError")
    fake(f"rm_S{near[1]}", -100.0, occ="")
    try:
        readout(td, card)
        chk(False, "[음성] 점유 블록 없음 → 죽어야 한다 (0 으로 두지 않는다)")
    except ValueError:
        chk(True, "[음성] 점유 블록 없음 → ValueError ('없음' 을 0 으로 안 읽는다)")
    print(f"selftest {'PASS' if ok[1] == 0 else 'FAIL'}  ({ok[0]}/{ok[0] + ok[1]})")
    return 0 if ok[1] == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sites", action="store_true")
    ap.add_argument("--predict", action="store_true")
    ap.add_argument("--make_inputs", action="store_true")
    ap.add_argument("--readout", action="store_true")
    ap.add_argument("--runs")
    ap.add_argument("--out")
    ap.add_argument("--pseudo_dir", help="--make_inputs: 실행 기계 PAW 폴더 (주면 그 줄을 바꾼다 · 안 주면 계보 값 그대로)")
    ap.add_argument("--lineage", help="--make_inputs: 계보 입력 경로 (기본 저장소 사본 · sha256 이 카드와 같아야 한다)")
    ap.add_argument("--card", default=str(CARD), help="카드 (기본 v2 중성 S · v1 은 --sites · --predict 기록 재현에만)")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    card = load_card(a.card)
    at = read_lineage()
    if a.sites:
        rows = classify(at, card)
        print(json.dumps({"selected": select_sites(rows, card), "bader_mismatch": bader_crosscheck(rows),
                          "rows": rows}, ensure_ascii=False, indent=1))
        return 0
    if a.predict:
        p = predict(at, card["selected"], card)
        s = json.dumps(p, ensure_ascii=False, indent=1)
        print(s)
        if a.out:
            pathlib.Path(a.out).write_text(s + "\n", encoding="utf-8")
        return 0
    if a.make_inputs:
        if not a.out:
            ap.error("--make_inputs 는 --out 이 필요하다")
        lp = pathlib.Path(a.lineage) if a.lineage else LINEAGE
        man = make_inputs(card, lp.read_bytes().decode(), a.out, a.pseudo_dir, lp)
        print(f"입력 {len(man['inputs'])} ({mode_of(card)} · 전자 {card['n_electrons_after']}) → {a.out} · "
              f"순서 {' '.join(m['dir'] for m in man['inputs'])}")
        return 0
    if a.readout:
        if not a.runs:
            ap.error("--readout 은 --runs 가 필요하다")
        r = readout(a.runs, card)
        s = json.dumps(r, ensure_ascii=False, indent=1)
        print(s)
        if a.out:
            pathlib.Path(a.out).write_text(s + "\n", encoding="utf-8")
        return 0
    ap.error("--sites · --predict · --make_inputs · --readout · --selftest 중 하나")
    return 2


if __name__ == "__main__":
    sys.exit(main())
