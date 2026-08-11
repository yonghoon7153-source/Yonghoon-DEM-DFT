#!/usr/bin/env python3
"""site_screen.py — LiNiO₂(104) 위 4개 조각의 **자리(site) 선호 · 자세(pose) 스크리닝** 엔진.

조각 4종
  sdcp_neutral  · sdcp_doped   (SDCP 모노머, Phase-A/B 가 쓴 그 분자)
  ptfe_dimer    · ptfe_c10     (ORCA r2SCAN-3c 이완본, Codex 패키지와 **바이트 동일**)

왜 다시 만드나 — 이미 치른 하자 5개를 구조적으로 막기 위해서다
  ① "Ni 가 졌다" vs "Ni 를 안 재봤다"  → 7자리 전수 + **같은 자세로 짝지은 Li/Ni 대조쌍**.
     Ni 자세가 게이트에 걸려 죽으면 그건 '패배'가 아니라 **검열(censored)** 로 따로 센다.
  ② 고정 슬랩이 Ni 에 불리   → freeze 프로토콜을 라벨에 박고, 고정판 수치를 열역학이라 부르지 않는다.
  ③ 주기이미지 아티팩트   → 2026-07 티오펜 S···이미지 슬랩 O 1.506 Å 샌드위치로 Δ +0.689 를
     철회한 적이 있다. 가로 4.5 Å / 세로 5.0 Å 이격 게이트를 **자세를 만들기 전에** 건다.
  ④ Li 추출을 결합으로 오독   → freeze 0.6 의 -1.465 eV 가 그거였다(VASP dE_extract = +0.336 eV
     로 반증됨). 깨끗한 슬랩 대비 표면 Li 변위·배위 이전을 재서 **격리**한다.
  ⑤ 조각 사이 점수 빼기   → 금지. UMA 점수는 **같은 조각·같은 프로토콜 안에서 순위**만.
     특히 sdcp_doped 는 **알짜중성 라디칼(doublet)** 이고 UMA 에는 다중도 입력이 없다.

자세 표본화 — Phase-A 의 "sulfonate 만 아래로" 구멍을 메운다
  분자 프레임에서 피보나치 구면 N 방향을 −z 로 정렬(=down_dir) × z축 roll 4개.
  화학적으로 의미 있는 방향(sulfonate-down 등)은 **태그를 달아** 따로 보존해 Phase-A 와 비교 가능.

서브커맨드
  inputs     입력 4종 + 슬랩 검증(원자수·sha256·스핀 선언). 없으면 '없다'고 말한다(판정 아님).
  sites      표면 자리 7종 열거 + **대표 1개로 충분한지** 동치성 검사.
  atlas      자세 아틀라스 생성(게이트 통과분만) → 구조 + manifest.json
  gate       임의 구조 묶음에 게이트 적용(우리 것·Codex 것·QE/VASP CONTCAR 무관).
  score      UMA rigid SP / relax (gabia 전용, 재개 가능).
  verdict    자리 선호 판정표 — 검열 회계 + 대조쌍 + 판정 바닥.
  crosscheck Codex ptfe_linio2_uma 레코드와 자세별 대조.

  python3 tools/sdcp/site_screen.py inputs
  python3 tools/sdcp/site_screen.py sites
  python3 tools/sdcp/site_screen.py atlas --frag ptfe_c10 --out /data/work/runs/sdcp_v4
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
from ase import Atoms
from ase.io import read, write

REPO = Path(__file__).resolve().parents[2]
STRUCT = REPO / "db" / "structures"

# ── 슬랩 (Codex 패키지 inputs/linio2_104_1x4_relaxed.vasp 와 sha256 동일) ────────────
SLAB = {
    "path": STRUCT / "linio2_104_sym_1x4L4_relaxed.vasp",
    "counts": {"Li": 48, "Ni": 48, "O": 96},
    "sha256": "26a48473060243fef55e86d151050b6a27d6e65801b4d3ccd818678913aee25e",
}

# ── 조각 등록부 ────────────────────────────────────────────────────────────────────
#   electrons : UMA 에 넣을 수 없는 정보. 기록만 하고 **UMA 판정의 유효범위를 깎는 근거**로 쓴다.
#   cap       : 실제 고분자에 없는 인공 말단. 이 원소가 최근접 접촉이면 CAP_ARTIFACT.
#   anchor_tag: Phase-A 비교용으로 반드시 보존할 화학적 방향 (down_dir 에 태그로 추가).
FRAGMENTS: Dict[str, Dict[str, Any]] = {
    "sdcp_neutral": {
        "path": STRUCT / "sdcp_v7c_neutral.xyz",
        "counts": {"C": 11, "H": 16, "O": 6, "S": 2},
        "sha256": None,  # gabia 회수 후 고정
        "electrons": "closed-shell singlet (charge 0)",
        "cap": (),
        "anchor_tag": {"sulfonate_down": "SO3", "thiophene_down": "thiophene_S"},
        "note": "−SO₃H 보호형. Phase-A/B 의 mol_neutral.",
    },
    "sdcp_doped": {
        "path": STRUCT / "sdcp_v7c_doped.xyz",
        "counts": {"C": 11, "H": 15, "O": 6, "S": 2},
        "sha256": None,
        "electrons": "OPEN-SHELL DOUBLET, net charge 0 (acidic H removed homolytically)",
        "cap": (),
        "anchor_tag": {"sulfonate_down": "SO3", "thiophene_down": "thiophene_S"},
        "note": "라디칼. UMA 에 다중도 입력이 없다 — doped 의 UMA 점수는 neutral 과 비교 불가.",
    },
    "ptfe_dimer": {
        "path": STRUCT / "ptfe_dimer_c4h2f8_r2scan3c.xyz",
        "counts": {"C": 4, "H": 2, "F": 8},
        "sha256": "dcc0f678202ced02c222cded61a0892a78f177ad12dbb107839bc462ea3bdb7b",
        "electrons": "closed-shell singlet (charge 0)",
        "cap": ("H",),
        "anchor_tag": {"CF2_face_down": "internal_F"},
        "note": "말단 H 는 실제 PTFE 에 없는 인공 cap.",
    },
    "ptfe_c10": {
        "path": STRUCT / "ptfe_c10f22_r2scan3c.xyz",
        "counts": {"C": 10, "F": 22},
        "sha256": "66dd0bcc4badd26d6db42cc3ed429fbd9ec50a0d467f76a07d2532329efc2d57",
        "electrons": "closed-shell singlet (charge 0)",
        "cap": (),
        "anchor_tag": {"CF2_face_down": "internal_F"},
        "note": "유한 CF₃-말단 perfluoroalkane. dimer 와 사슬길이 수렴열을 이루지 **않는다**.",
    },
    # 참고용(이번 라운드 범위 밖): v7c 다이머는 셀 b(11.51 Å)보다 길어 이미지 게이트를 통과 못 한다.
    "sdcp_dimer_neutral": {
        "path": STRUCT / "sdcp_v7c_dimer_neutral.xyz",
        "counts": {"C": 22, "H": 30, "O": 12, "S": 4},
        "sha256": "eb9f1022c91a8eab1b77b04b582b4d8317dfeb4329667032a013e99561d32704",
        "electrons": "closed-shell singlet (charge 0)",
        "cap": (),
        "anchor_tag": {"sulfonate_down": "SO3"},
        "note": "장축 16.6 Å > 최단 면내 격자 11.51 Å — 방향의 2/3 이 이미지 게이트에 걸린다. "
                "불가능은 아니지만 **방향 표본이 심하게 검열**되므로 셀 확장 전에는 자리 판정에 쓰지 않는다.",
        "out_of_scope": True,
    },
    "sdcp_dimer_doped": {
        "path": STRUCT / "sdcp_v7c_dimer_doped.xyz",
        "counts": {"C": 22, "H": 29, "O": 12, "S": 4},
        "sha256": "755a8daf907d7a283bdefd8f8681f2d5a5ccd671565752c2df1d658f0220f8d4",
        "electrons": "OPEN-SHELL DOUBLET, net charge 0",
        "cap": (),
        "anchor_tag": {"sulfonate_down": "SO3"},
        "note": "장축 16.7 Å — 위와 같은 이유로 이번 라운드 범위 밖.",
        "out_of_scope": True,
    },
}
PRIMARY = ("sdcp_neutral", "sdcp_doped", "ptfe_dimer", "ptfe_c10")

SITE_ORDER = ("Li_top", "Ni_top", "O_top", "LiO_bridge", "NiO_bridge", "LiNi_bridge", "hollow")
CATIONS = ("Li", "Ni")

# ── 게이트 임계 (전부 명시. 근거는 주석에.) ──────────────────────────────────────────
GATE = {
    "collision_A": 1.50,          # 분자–슬랩 원자 충돌
    "image_lateral_min_A": 4.50,  # 분자 ↔ 자기 가로 이미지 (Codex 와 동일)
    "image_lateral_warn_A": 5.00,
    "image_vertical_min_A": 5.00, # 분자 ↔ 세로(진공 너머) 슬랩 이미지 — 2026-07 샌드위치 재발 방지
    "detach_A": 4.00,             # 이보다 멀면 흡착이 아니다
    "frozen_drift_A": 1e-3,       # 고정 원자가 움직이면 그 런은 무효
    "extract_disp_A": 0.50,       # 깨끗한 슬랩 대비 표면 양이온 변위
    "extract_coord_A": 2.20,      # 슬랩 Li 가 분자 O 에 배위하면 추출 의심
    # ⚠ 2026-08-11 재교정 — 예전에는 분자 비금속↔슬랩 양이온에 **2.00 Å 일괄** 컷을 썼는데,
    #   그러면 O···Li 1.75–1.94 Å 가 전부 '반응'으로 죽는다. 그건 틀렸다: Li–O 배위는
    #   1.90–2.20 Å 가 정상이고 기체상 LiOH 의 Li–O 는 1.58 Å 다. 즉 짧다고 반응이 아니다.
    #   원소쌍별 공유반지름 합의 비율로 바꾼다 — 융합급만 죽이고, 짧은 배위는 태그만 단다.
    #   진짜 판별자는 거리 컷이 아니라 **추출/재구성 게이트**(깨끗한 슬랩 대조)다.
    "reactive_frac": 0.80,        # d < 0.80 Σr_cov → 융합급, 탈락
    "short_frac": 0.92,           # 0.80–0.92 Σr_cov → 짧은 접촉, 경고 태그 (DFT 확인 대상)
    "decision_floor_eV": 0.030,   # 이보다 작은 차이는 '가려지지 않았다'
}
# 결합 유지 임계: (형성, 절단, 과단축) — PTFE 3종은 Codex 값을 그대로 쓴다(교차검증 가능하게).
BOND_LIMITS = {
    "C-C": (1.75, 1.90, 1.20),
    "C-F": (1.55, 1.70, 1.10),
    "C-H": (1.25, 1.35, 0.85),
    # SDCP 계열 — ORCA 실측 최대(C-O 1.45 / C-S 1.84 / O-S 1.66 / H-O 0.97)에
    # 형성 ×1.10, 절단 ×1.20, 과단축 ×0.80 을 적용해 유도. 아래 --show-bond-limits 로 확인.
    "C-O": (1.60, 1.75, 1.14),
    "C-S": (2.02, 2.21, 1.38),
    "O-S": (1.83, 2.00, 1.17),
    "H-O": (1.07, 1.17, 0.78),
}
COV = {"C": 0.76, "F": 0.57, "H": 0.31, "O": 0.66, "S": 1.05, "Li": 1.28, "Ni": 1.24}


# ── 유틸 ──────────────────────────────────────────────────────────────────────────
def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def counts_of(atoms: Atoms) -> Dict[str, int]:
    return dict(Counter(atoms.get_chemical_symbols()))


def load_slab() -> Atoms:
    if not SLAB["path"].is_file():
        sys.exit(f"⛔ 슬랩이 없다: {SLAB['path']}")
    got = sha256(SLAB["path"])
    if got != SLAB["sha256"]:
        sys.exit(f"⛔ 슬랩 sha256 불일치\n   기대 {SLAB['sha256']}\n   실제 {got}")
    return read(SLAB["path"])


def load_fragment(name: str) -> Tuple[Optional[Atoms], Dict[str, Any]]:
    """조각을 읽는다. **없으면 None 을 돌려주고 '없다'고 말한다** — 대체 구조를 슬쩍 쓰지 않는다."""
    spec = FRAGMENTS[name]
    p: Path = spec["path"]
    if not p.is_file():
        return None, {"status": "MISSING", "path": str(p)}
    mol = read(p)
    got = sha256(p)
    info = {"status": "OK", "path": str(p), "sha256": got, "counts": counts_of(mol)}
    if spec["sha256"] and got != spec["sha256"]:
        info["status"] = "SHA_MISMATCH"
        info["expected_sha256"] = spec["sha256"]
    if counts_of(mol) != spec["counts"]:
        info["status"] = "COUNT_MISMATCH"
        info["expected_counts"] = spec["counts"]
    return mol, info


# ── 표면 자리 ─────────────────────────────────────────────────────────────────────
def surface_indices(slab: Atoms, depth: float = 1.2) -> List[int]:
    z = slab.positions[:, 2]
    return [i for i in range(len(slab)) if z[i] > z.max() - depth]


def site_equivalence(slab: Atoms, depth: float = 1.2) -> Dict[str, Any]:
    """대표 1개로 충분한가 — 표면 동종 원자들이 실제로 같은 환경인지 잰다.

    허용오차를 바꿔가며 군집 수가 요동치면 그건 **수치잡음에 의한 과분할**이고,
    '자리가 여러 종류다'가 아니다. 그 판정을 숫자로 남긴다.
    """
    sym = slab.get_chemical_symbols()
    z = slab.positions[:, 2]
    surf = surface_indices(slab, depth)
    D = slab.get_all_distances(mic=True)
    out: Dict[str, Any] = {}
    for el in CATIONS + ("O",):
        idx = [i for i in surf if sym[i] == el]
        if not idx:
            continue
        rec: Dict[str, Any] = {"n_surface": len(idx),
                               "z_spread_A": round(float(max(z[i] for i in idx) - min(z[i] for i in idx)), 4)}
        for tol in (0.02, 0.05, 0.10, 0.20):
            cl: Dict[Any, List[int]] = {}
            for i in idx:
                fp = tuple(sorted((round(D[i, j] / tol) * tol, sym[j])
                                  for j in range(len(slab)) if j != i and D[i, j] < 3.2))
                cl.setdefault(fp, []).append(i)
            rec[f"classes@{tol:.2f}A"] = len(cl)
        # 결합거리 분산 = 진짜 비등가성의 척도
        bl = []
        for i in idx:
            near = sorted(D[i, j] for j in range(len(slab)) if j != i and D[i, j] < 2.4)
            bl.append(near[0] if near else np.nan)
        rec["nearest_bond_spread_A"] = round(float(np.nanmax(bl) - np.nanmin(bl)), 4)
        out[el] = rec
    return out


def _mic_xy(vec: np.ndarray, cell: np.ndarray) -> np.ndarray:
    """면내 최소이미지 벡터 (기울어진 셀 대응, 3×3 탐색)."""
    A = cell[:2, :2].T
    frac = np.linalg.solve(A, vec[:2])
    best, bd = None, np.inf
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            c = A @ (frac - np.round(frac) + np.array([di, dj]))
            d = float(np.linalg.norm(c))
            if d < bd:
                bd, best = d, c
    return np.array([best[0], best[1], vec[2]])


def site_anchors(slab: Atoms, depth: float = 1.2) -> Dict[str, Dict[str, Any]]:
    """7자리 대표 앵커. 셀 중앙에 가장 가까운 원자를 대표로 골라 이미지 여유를 최대화한다."""
    sym = slab.get_chemical_symbols()
    pos = slab.positions
    cell = slab.cell.array
    surf = surface_indices(slab, depth)
    center = (cell[0] + cell[1])[:2] / 2.0

    def most_central(idx: Sequence[int]) -> int:
        return min(idx, key=lambda i: np.linalg.norm(_mic_xy(pos[i] - np.array([center[0], center[1], pos[i, 2]]), cell)[:2]))

    by_el = {el: [i for i in surf if sym[i] == el] for el in ("Li", "Ni", "O")}
    for el, v in by_el.items():
        if not v:
            sys.exit(f"⛔ 표면에 {el} 이 없다 — 종단이 예상과 다르다")
    li, ni, ox = most_central(by_el["Li"]), most_central(by_el["Ni"]), most_central(by_el["O"])

    def midpoint(i: int, js: Sequence[int]) -> Tuple[np.ndarray, int]:
        j = min(js, key=lambda k: np.linalg.norm(_mic_xy(pos[k] - pos[i], cell)))
        d = _mic_xy(pos[j] - pos[i], cell)
        return pos[i] + 0.5 * d, j

    anchors: Dict[str, Dict[str, Any]] = {}
    anchors["Li_top"] = {"xyz": pos[li].copy(), "atoms": [li]}
    anchors["Ni_top"] = {"xyz": pos[ni].copy(), "atoms": [ni]}
    anchors["O_top"] = {"xyz": pos[ox].copy(), "atoms": [ox]}
    m, j = midpoint(li, by_el["O"]);  anchors["LiO_bridge"] = {"xyz": m, "atoms": [li, j]}
    m, j = midpoint(ni, by_el["O"]);  anchors["NiO_bridge"] = {"xyz": m, "atoms": [ni, j]}
    m, j = midpoint(li, by_el["Ni"]); anchors["LiNi_bridge"] = {"xyz": m, "atoms": [li, j]}
    # hollow = Li·Ni·O 삼각형 무게중심
    jn = min(by_el["Ni"], key=lambda k: np.linalg.norm(_mic_xy(pos[k] - pos[li], cell)))
    jo = min(by_el["O"], key=lambda k: np.linalg.norm(_mic_xy(pos[k] - pos[li], cell)))
    tri = pos[li] + (_mic_xy(pos[jn] - pos[li], cell) + _mic_xy(pos[jo] - pos[li], cell)) / 3.0
    tri[2] = max(pos[li, 2], pos[jn, 2], pos[jo, 2])
    anchors["hollow"] = {"xyz": tri, "atoms": [li, jn, jo]}
    return {k: anchors[k] for k in SITE_ORDER}


# ── 자세 생성 ─────────────────────────────────────────────────────────────────────
def fibonacci_directions(n: int) -> np.ndarray:
    """결정론적 준균일 구면 방향 (난수 없음 — 재현성)."""
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    theta = np.pi * (1 + 5 ** 0.5) * i
    return np.stack([np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)], axis=1)


def rot_align(src: np.ndarray, dst: np.ndarray) -> np.ndarray:
    """src → dst 로 보내는 **고유회전**(det=+1). 반평행일 때 −I 를 쓰면 거울상이 되므로
    수직축 180° 회전으로 처리한다 (분자 카이랄성이 조용히 뒤집히는 사고 방지)."""
    a = src / np.linalg.norm(src)
    b = dst / np.linalg.norm(dst)
    v = np.cross(a, b)
    c = float(np.dot(a, b))
    if np.linalg.norm(v) < 1e-12:
        if c > 0:
            return np.eye(3)
        perp = np.array([1.0, 0.0, 0.0])
        if abs(float(np.dot(perp, a))) > 0.9:
            perp = np.array([0.0, 1.0, 0.0])
        w = np.cross(a, perp)
        w /= np.linalg.norm(w)
        return 2 * np.outer(w, w) - np.eye(3)      # w 축 180° 회전, det=+1
    K = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + K + K @ K * (1 / (1 + c))


def rot_z(deg: float) -> np.ndarray:
    t = math.radians(deg)
    return np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])


def group_indices(mol: Atoms, tag: str) -> List[int]:
    """화학적 접촉 그룹 — 태그된 방향을 만들 때만 쓴다(무편향 표본은 피보나치가 담당)."""
    sym = mol.get_chemical_symbols()
    D = mol.get_all_distances()
    if tag == "SO3":
        S = [i for i in range(len(mol)) if sym[i] == "S"]
        best, bn = None, -1
        for s in S:
            o = [j for j in range(len(mol)) if sym[j] == "O" and D[s, j] < 1.80]
            if len(o) > bn:
                bn, best = len(o), [s] + o
        return best or []
    if tag == "thiophene_S":
        S = [i for i in range(len(mol)) if sym[i] == "S"]
        # 술폰 S 가 아닌 S (O 배위가 적은 쪽)
        return [min(S, key=lambda s: sum(1 for j in range(len(mol)) if sym[j] == "O" and D[s, j] < 1.80))] if S else []
    if tag == "internal_F":
        C = [i for i in range(len(mol)) if sym[i] == "C"]
        F = [i for i in range(len(mol)) if sym[i] == "F"]
        if len(C) < 3:
            return F
        # 사슬 끝 = C 중 다른 C 이웃이 1개뿐인 것
        endc = {c for c in C if sum(1 for c2 in C if c2 != c and D[c, c2] < 1.75) <= 1}
        inner = [f for f in F if min(C, key=lambda c: D[f, c]) not in endc]
        return inner or F
    return []


def make_pose(slab: Atoms, mol: Atoms, anchor: np.ndarray,
              down: np.ndarray, roll_deg: float, gap: float) -> Atoms:
    """분자 프레임의 down 방향을 −z 로 돌리고, z-roll 을 준 뒤, 앵커 위 gap 만큼 띄운다."""
    m = mol.copy()
    m.positions -= m.get_center_of_mass()
    R = rot_align(down, np.array([0.0, 0.0, -1.0]))
    m.positions = m.positions @ R.T
    m.positions = m.positions @ rot_z(roll_deg).T
    low = int(np.argmin(m.positions[:, 2]))
    shift = np.array([anchor[0] - m.positions[low, 0],
                      anchor[1] - m.positions[low, 1],
                      anchor[2] + gap - m.positions[low, 2]])
    m.positions += shift
    # 강체 불변 자체검사 — 회전행렬이 고유회전이 아니면(거울상) 내부 거리행렬은 같아도
    # 카이랄성이 뒤집힌다. 부호 있는 부피로 잡는다.
    if len(mol) >= 4:
        def chirality(p: np.ndarray) -> float:
            q = p[:4] - p[:4].mean(axis=0)
            return float(np.linalg.det(np.stack([q[1] - q[0], q[2] - q[0], q[3] - q[0]])))
        c0, c1 = chirality(mol.positions), chirality(m.positions)
        if abs(c0) > 1e-6 and c0 * c1 < 0:
            raise RuntimeError("자세 생성이 분자를 거울상으로 뒤집었다 — 회전행렬 버그")
    d0 = np.linalg.norm(mol.positions[0] - mol.positions[-1])
    d1 = np.linalg.norm(m.positions[0] - m.positions[-1])
    if abs(d0 - d1) > 1e-6:
        raise RuntimeError("자세 생성이 분자를 변형시켰다 — 강체 조건 위반")
    cx = slab.copy()
    cx += m
    cx.set_pbc(True)
    return cx


# ── 기하 계측 · 게이트 ─────────────────────────────────────────────────────────────
def lateral_image_min(mp: np.ndarray, cell: np.ndarray) -> float:
    """분자 ↔ 자기 자신의 가로 주기이미지 최소거리."""
    best = np.inf
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            T = di * cell[0] + dj * cell[1]
            d = np.linalg.norm(mp[:, None, :] - (mp[None, :, :] + T), axis=2)
            best = min(best, float(d.min()))
    return best


def vertical_image_min(mp: np.ndarray, sp: np.ndarray, cell: np.ndarray) -> float:
    """분자 ↔ 진공 너머 슬랩 이미지 최소거리 (2026-07 샌드위치 아티팩트 감지용)."""
    best = np.inf
    for dk in (-1, 1):
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                T = di * cell[0] + dj * cell[1] + dk * cell[2]
                d = np.linalg.norm(mp[:, None, :] - (sp[None, :, :] + T), axis=2)
                best = min(best, float(d.min()))
    return best


def bond_table(mol: Atoms) -> List[Tuple[int, int, str]]:
    sym = mol.get_chemical_symbols()
    D = mol.get_all_distances()
    out = []
    for i in range(len(mol)):
        for j in range(i + 1, len(mol)):
            lab = "-".join(sorted((sym[i], sym[j])))
            lim = BOND_LIMITS.get(lab)
            if lim and D[i, j] <= lim[0]:
                out.append((i, j, lab))
    return out


def bond_metrics(mol: Atoms, bonds: Sequence[Tuple[int, int, str]]) -> Dict[str, Any]:
    res = {"broken": [], "formed": [], "too_short": []}
    have = {(i, j, lab) for i, j, lab in bonds}
    P = mol.positions
    for i, j, lab in bonds:
        d = float(np.linalg.norm(P[i] - P[j]))
        form, brk, short = BOND_LIMITS[lab]
        if d > brk:
            res["broken"].append(f"{lab}:{i}-{j}:{d:.3f}")
        if d < short:
            res["too_short"].append(f"{lab}:{i}-{j}:{d:.3f}")
    sym = mol.get_chemical_symbols()
    for i in range(len(mol)):
        for j in range(i + 1, len(mol)):
            lab = "-".join(sorted((sym[i], sym[j])))
            if lab not in BOND_LIMITS or (i, j, lab) in have:
                continue
            d = float(np.linalg.norm(P[i] - P[j]))
            if d < BOND_LIMITS[lab][0]:
                res["formed"].append(f"{lab}:{i}-{j}:{d:.3f}")
    res["n_changes"] = len(res["broken"]) + len(res["formed"]) + len(res["too_short"])
    return res


def mic_matrix(A: np.ndarray, B: np.ndarray, cell: np.ndarray) -> np.ndarray:
    """A(n,3) × B(m,3) 면내 최소이미지 거리행렬 (3×3 탐색, 기울어진 셀 대응)."""
    diff = A[:, None, :] - B[None, :, :]
    best = None
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            d = np.linalg.norm(diff - (di * cell[0] + dj * cell[1]), axis=2)
            best = d if best is None else np.minimum(best, d)
    return best


def contact_stats(cx: Atoms, nslab: int) -> Dict[str, Any]:
    """분자–슬랩 접촉 통계 + **최종 기하 기준** 자리 재분류."""
    sym = cx.get_chemical_symbols()
    cell = cx.cell.array
    D = mic_matrix(cx.positions[nslab:], cx.positions[:nslab], cell)   # (nmol, nslab)
    zs = cx.positions[:nslab, 2]
    surf = np.array([i for i in range(nslab) if zs[i] > zs.max() - 1.2])
    k = int(np.argmin(D))
    mi_local, si = divmod(k, D.shape[1])
    mi = nslab + mi_local
    dmin, pair = float(D[mi_local, si]), f"{sym[mi]}···{sym[si]}"
    # 양이온 접촉 등록부 (3.2 Å 안의 분자원자–표면양이온 쌍)
    reg: Dict[str, int] = Counter()
    per_cation: Dict[str, float] = {}
    for c in surf:
        if sym[c] not in CATIONS:
            continue
        col = D[:, c]
        hit = np.nonzero(col < 3.2)[0]
        for h in hit:
            reg[f"{sym[nslab + int(h)]}-{sym[c]}"] += 1
        if hit.size:
            per_cation[sym[c]] = min(per_cation.get(sym[c], np.inf), float(col[hit].min()))
    nearest_cation = min(per_cation, key=per_cation.get) if per_cation else None
    # 원소쌍별 최단거리 → 공유반지름 합 대비 비율. 거리 게이트는 이걸로 판정한다.
    msym = sym[nslab:]; ssym = sym[:nslab]
    pair_min: Dict[str, float] = {}
    for a_i, a_el in enumerate(msym):
        col = D[a_i]
        for b_j in np.nonzero(col < 3.6)[0]:
            key = f"{a_el}-{ssym[b_j]}"
            v = float(col[b_j])
            if v < pair_min.get(key, np.inf):
                pair_min[key] = v
    ratios = {}
    for key, v in pair_min.items():
        e1, e2 = key.split("-")
        s = COV.get(e1, 0.8) + COV.get(e2, 1.2)
        ratios[key] = (round(v, 3), round(v / s, 3))
    return {
        "min_contact_A": round(dmin, 3), "min_contact_pair": pair,
        "min_contact_mol_index": mi, "min_contact_slab_index": si,
        "min_contact_slab_element": sym[si] if si >= 0 else None,
        "registry": dict(reg),
        "d_Li_A": round(per_cation["Li"], 3) if "Li" in per_cation else None,
        "d_Ni_A": round(per_cation["Ni"], 3) if "Ni" in per_cation else None,
        "nearest_cation": nearest_cation,
        "site_from_geometry": (f"{nearest_cation}_contact" if nearest_cation else "no_cation_contact"),
        "pair_min_A_and_ratio": ratios,
    }


def extraction_check(cx: Atoms, clean: Atoms, nslab: int) -> Dict[str, Any]:
    """Li 추출 / 표면 재구성 격리 — 'freeze 0.6 의 −1.465 eV' 를 결합으로 오독한 사건의 재발 방지.

    VASP dE_extract = +0.336 eV(2026-08-08) 로 추출이 열역학적으로 불리함이 확인됐으므로,
    추출형 끝점은 **결합 순위에서 빼고 따로 센다**.
    """
    sym = cx.get_chemical_symbols()
    zc = clean.positions[:, 2]
    surf = [i for i in range(nslab) if zc[i] > zc.max() - 1.2]
    disp = np.linalg.norm(cx.positions[:nslab] - clean.positions[:nslab], axis=1)
    moved = [(i, sym[i], round(float(disp[i]), 3)) for i in surf if disp[i] > GATE["extract_disp_A"]]
    transferred = []
    D = mic_matrix(cx.positions[:nslab], cx.positions[nslab:], cx.cell.array)  # (nslab, nmol)
    for i in surf:
        if sym[i] not in CATIONS:
            continue
        j = int(np.argmin(D[i]))
        if D[i, j] < GATE["extract_coord_A"] and sym[nslab + j] in ("O", "F", "S"):
            transferred.append((i, sym[i], f"{sym[nslab + j]}", round(float(D[i, j]), 3)))
    return {
        "max_surface_disp_A": round(float(max([disp[i] for i in surf], default=0.0)), 3),
        "z_top_shift_A": round(float(cx.positions[:nslab, 2].max() - zc.max()), 3),
        "moved_surface_atoms": moved,
        "cation_transferred_to_molecule": transferred,
        "flag": bool(moved) or bool(transferred),
    }


def apply_gates(cx: Atoms, nslab: int, mol_ref: Atoms, frag: str,
                clean: Optional[Atoms] = None, relaxed: bool = False,
                bonds: Optional[Sequence[Tuple[int, int, str]]] = None) -> Dict[str, Any]:
    """모든 게이트를 한 번에. **판정 불가와 실패를 구분한다.**"""
    cell = cx.cell.array
    mp = cx.positions[nslab:]
    sp = cx.positions[:nslab]
    mol = cx[nslab:]
    mol.set_pbc(False)
    stats = contact_stats(cx, nslab)
    lat = lateral_image_min(mp, cell)
    ver = vertical_image_min(mp, sp, cell)
    bm = bond_metrics(mol, bond_table(mol_ref) if bonds is None else bonds)
    spec = FRAGMENTS[frag]

    reasons: List[str] = []
    warns: List[str] = []
    if stats["min_contact_A"] < GATE["collision_A"]:
        reasons.append(f"COLLISION({stats['min_contact_A']:.2f}Å<{GATE['collision_A']})")
    if lat < GATE["image_lateral_min_A"]:
        reasons.append(f"IMAGE_LATERAL({lat:.2f}Å<{GATE['image_lateral_min_A']})")
    elif lat < GATE["image_lateral_warn_A"]:
        warns.append(f"image_lateral_tight({lat:.2f}Å)")
    if ver < GATE["image_vertical_min_A"]:
        reasons.append(f"IMAGE_VERTICAL({ver:.2f}Å<{GATE['image_vertical_min_A']})")
    if bm["n_changes"]:
        reasons.append("BOND_TOPOLOGY(" + ",".join(bm["broken"] + bm["formed"] + bm["too_short"])[:120] + ")")
    if spec["cap"] and stats["min_contact_pair"].split("···")[0] in spec["cap"]:
        # 시작 자세에서는 **경고**다 — H 아래로 출발해도 이완하면서 F 쪽으로 돌아설 수 있다.
        # 이완 결과에서 여전히 cap 이 최근접이면 그때 죽인다.
        (reasons if relaxed else warns).append(
            ("CAP_ARTIFACT(%s)" if relaxed else "cap_down_start(%s)") % stats["min_contact_pair"])
    if relaxed and stats["min_contact_A"] > GATE["detach_A"]:
        reasons.append(f"DETACHED({stats['min_contact_A']:.2f}Å>{GATE['detach_A']})")
    # 거리 게이트는 원소쌍별 공유반지름 합 대비 비율로 본다 (일괄 2.00 Å 컷은 폐기 — Li–O 배위를
    # 반응으로 오판했다). 융합급만 죽이고, 짧은 접촉은 태그를 달아 DFT 확인 대상으로 넘긴다.
    for key, (d, ratio) in stats["pair_min_A_and_ratio"].items():
        if ratio < GATE["reactive_frac"]:
            reasons.append(f"REACTIVE_CONTACT({key} {d:.2f}Å = {ratio:.2f}Σr_cov)")
        elif ratio < GATE["short_frac"]:
            warns.append(f"short_contact({key} {d:.2f}Å = {ratio:.2f}Σr_cov)")

    out: Dict[str, Any] = {
        "image_lateral_A": round(lat, 3), "image_vertical_A": round(ver, 3),
        "bond": bm, **stats, "warnings": warns,
    }
    if clean is not None:
        ex = extraction_check(cx, clean, nslab)
        out["extraction"] = ex
        if ex["flag"]:
            reasons.append("EXTRACTION_OR_RECONSTRUCTION")
    elif relaxed:
        out["extraction"] = {"status": "NOT_CHECKED — clean slab reference 없음"}
        warns.append("extraction_not_checked")

    out["gate_reasons"] = reasons
    out["ranking_eligible"] = not reasons
    return out


# ── 서브커맨드 ────────────────────────────────────────────────────────────────────
def cmd_inputs(a) -> int:
    print("① 슬랩")
    if SLAB["path"].is_file():
        got = sha256(SLAB["path"])
        ok = got == SLAB["sha256"]
        slab = read(SLAB["path"])
        print(f"   {SLAB['path'].relative_to(REPO)}  N={len(slab)}  {counts_of(slab)}")
        print(f"   sha256 {'✔ 일치' if ok else '⛔ 불일치'}  ({got[:16]}…)")
        print(f"   cell a={np.linalg.norm(slab.cell[0]):.3f} b={np.linalg.norm(slab.cell[1]):.3f} "
              f"c={np.linalg.norm(slab.cell[2]):.3f} Å · 최단 면내 격자 "
              f"{min(np.linalg.norm(slab.cell[0]), np.linalg.norm(slab.cell[1])):.2f} Å")
    else:
        print(f"   ⛔ 없다: {SLAB['path']}")

    print("\n② 조각")
    missing = []
    for name in PRIMARY + tuple(k for k in FRAGMENTS if k not in PRIMARY):
        spec = FRAGMENTS[name]
        mol, info = load_fragment(name)
        mark = {"OK": "✔", "MISSING": "⛔", "SHA_MISMATCH": "⚠", "COUNT_MISMATCH": "⚠"}[info["status"]]
        scope = " (범위 밖)" if spec.get("out_of_scope") else ""
        print(f"   {mark} {name:20s}{scope}")
        if info["status"] == "MISSING":
            missing.append(name)
            print(f"       **파일이 없다** — 판정 아님. 기대 경로 {Path(info['path']).relative_to(REPO)}")
            print(f"       기대 조성 {spec['counts']}")
            continue
        ext = np.ptp(mol.positions, axis=0)
        print(f"       N={len(mol)} {info['counts']} · 최장축 {ext.max():.2f} Å · sha {info['sha256'][:16]}…")
        print(f"       전자상태: {spec['electrons']}")
        if spec["cap"]:
            print(f"       인공 cap: {spec['cap']} — 이게 최근접이면 CAP_ARTIFACT")
        print(f"       {spec['note']}")

    print("\n③ UMA 유효범위 (이 표가 '무엇을 인용하면 안 되는지'의 근거다)")
    print("   · 조각 사이 점수 차 금지 — dimer vs C10, doped vs neutral 모두.")
    print("   · sdcp_doped 는 doublet 라디칼인데 UMA 에 다중도 입력이 없다 → doped 의 UMA 순위는")
    print("     'doped 구조들 사이 순위'까지만. neutral 과의 비교는 DFT 몫.")
    print("   · UMA 는 Ni 자기상태를 고르지 못한다 → Li vs Ni 자리 판정은 UMA 가 가장 약한 질문.")
    if missing:
        print(f"\n⛔ 회수 필요: {', '.join(missing)} — gabia $MOLDIR 에서 db/structures/ 로 등재할 것.")
        return 2
    return 0


def cmd_sites(a) -> int:
    slab = load_slab()
    eq = site_equivalence(slab)
    print("① 표면 동종 원자가 정말 여러 종류인가 (대표 1개로 충분한지)")
    for el, r in eq.items():
        cls = " ".join(f"{k.split('@')[1]}:{v}" for k, v in r.items() if k.startswith("classes@"))
        print(f"   {el}: 표면 {r['n_surface']}개 · z 편차 {r['z_spread_A']:.3f} Å · "
              f"최근접결합 편차 {r['nearest_bond_spread_A']:.3f} Å · 군집수 {cls}")
    print("   판정: 허용오차를 바꾸면 군집수가 요동친다 = 수치잡음에 의한 과분할.")
    print("         z·결합거리 편차가 0.02 Å 수준이면 **표면 Li 끼리(그리고 Ni 끼리)는 등가**이고,")
    print("         자리마다 대표 1개를 쓰는 설계가 정당하다. (Codex 패키지와 같은 결론)")

    anc = site_anchors(slab)
    sym = slab.get_chemical_symbols()
    pos = slab.positions
    print("\n② 자리 앵커 7종")
    for k, v in anc.items():
        who = " ".join(f"{sym[i]}#{i}" for i in v["atoms"])
        print(f"   {k:12s} xyz=({v['xyz'][0]:7.3f},{v['xyz'][1]:7.3f},{v['xyz'][2]:7.3f})  ← {who}")
    print("\n③ Li·Ni 대조쌍 성립 조건")
    dz = abs(anc["Li_top"]["xyz"][2] - anc["Ni_top"]["xyz"][2])
    print(f"   Li_top 과 Ni_top 의 z 차 = {dz:.3f} Å — 같은 gap 을 주면 시작 높이가 이만큼 다르다.")
    print("   → 대조쌍은 **같은 down_dir·같은 roll·같은 gap** 으로만 짝짓고, 그 밖의 비교는 짝이 아니다.")
    return 0


def cmd_atlas(a) -> int:
    slab = load_slab()
    nslab = len(slab)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    anchors = site_anchors(slab)
    dirs = fibonacci_directions(a.ndir)
    rolls = [float(x) for x in a.rolls]
    frags = a.frag or list(PRIMARY)

    manifest: Dict[str, Any] = {
        "tool": "site_screen.py", "stage": "atlas",
        "slab": {"path": str(SLAB["path"]), "sha256": SLAB["sha256"], "n": nslab},
        "gap_A": a.gap, "ndir": a.ndir, "rolls": rolls, "gates": GATE,
        "sites": {k: {"xyz": [round(float(x), 4) for x in v["xyz"]],
                      "atoms": v["atoms"]} for k, v in anchors.items()},
        "fragments": {},
    }
    grand = Counter()
    for frag in frags:
        if frag not in FRAGMENTS:
            sys.exit(f"⛔ 모르는 조각: {frag}")
        mol, info = load_fragment(frag)
        if mol is None:
            print(f"⛔ {frag}: 파일이 없다 ({info['path']}) — 건너뛴다. 판정 아님.")
            manifest["fragments"][frag] = {"status": "MISSING"}
            continue
        spec = FRAGMENTS[frag]
        # 화학 태그 방향 (Phase-A 비교용) — 그룹 중심 → COM 방향의 반대가 'down'
        tagged: List[Tuple[str, np.ndarray]] = []
        com = mol.get_center_of_mass()
        for tname, gtag in spec["anchor_tag"].items():
            gi = group_indices(mol, gtag)
            if gi:
                v = mol.positions[gi].mean(axis=0) - com
                if np.linalg.norm(v) > 1e-6:
                    tagged.append((tname, v / np.linalg.norm(v)))
        specs = [(f"fib{i:02d}", d) for i, d in enumerate(dirs)] + tagged

        rows, kept, killed = [], 0, Counter()
        bonds = bond_table(mol)
        fdir = out / frag
        fdir.mkdir(exist_ok=True)
        for site, av in anchors.items():
            for dname, dvec in specs:
                for roll in rolls:
                    cx = make_pose(slab, mol, av["xyz"], np.asarray(dvec, float), roll, a.gap)
                    g = apply_gates(cx, nslab, mol, frag, clean=None, relaxed=False, bonds=bonds)
                    label = f"{frag}__{site}__{dname}__r{int(roll):03d}"
                    row = {"label": label, "fragment": frag, "site": site,
                           "down_dir": dname, "roll_deg": roll, "gap_A": a.gap,
                           "tagged": dname in dict(tagged), **{k: v for k, v in g.items() if k != "bond"},
                           "bond_changes": g["bond"]["n_changes"]}
                    rows.append(row)
                    if g["ranking_eligible"]:
                        kept += 1
                        if not a.dry_run:
                            write(fdir / f"{label}.xyz", cx)
                    else:
                        killed[g["gate_reasons"][0].split("(")[0]] += 1
        grand[frag] = kept
        manifest["fragments"][frag] = {
            "status": "OK", "sha256": info["sha256"], "counts": info["counts"],
            "electrons": spec["electrons"], "n_generated": len(rows), "n_eligible": kept,
            "killed_by": dict(killed),
            "tagged_dirs": [t for t, _ in tagged],
        }
        print(f"\n■ {frag}  생성 {len(rows)} → 통과 {kept}  ({100*kept/max(len(rows),1):.0f}%)")
        for r, n in killed.most_common():
            print(f"    − {r:22s} {n}")
        # 자리별 생존 — '검열' 회계의 원장
        per = Counter(r["site"] for r in rows if r["ranking_eligible"])
        print("    자리별 생존: " + " · ".join(f"{s}:{per.get(s,0)}" for s in SITE_ORDER))
        dead = [s for s in SITE_ORDER if per.get(s, 0) == 0]
        if dead:
            print(f"    ⚠ 생존 0인 자리: {', '.join(dead)} — 이 자리는 **재본 적이 없다**로 기록한다"
                  f" (졌다가 아니다).")
        (fdir / "atlas_rows.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))

    (out / "atlas_manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    print(f"\n→ {out}/atlas_manifest.json  (조각별 atlas_rows.json + 통과 구조 xyz)")
    if not grand:
        return 2
    return 0


def parse_legacy_label(stem: str) -> Dict[str, Any]:
    """`complex_doped_sulfonate_down_r90_g22` → 방향·roll·격자점.

    레거시 스캔은 자리를 라벨로 갖고 있지 않다(g## 는 격자점이지 Li/Ni 가 아니다).
    그래서 `site` 는 **기하로 재분류한 것만** 쓰고, 시작 라벨은 g## 그대로 남긴다.
    """
    t = stem[len("complex_"):] if stem.startswith("complex_") else stem
    parts = t.split("_")
    out: Dict[str, Any] = {}
    if parts and parts[0] in ("doped", "neutral"):
        out["tag"] = parts.pop(0)
    roll = grid = None
    body = []
    for p in parts:
        if p.startswith("r") and p[1:].isdigit():
            roll = float(p[1:])
        elif p.startswith("g") and p[1:].isdigit():
            grid = p
        else:
            body.append(p)
    if body:
        out["down_dir"] = "_".join(body)
    if roll is not None:
        out["roll_deg"] = roll
    if grid:
        out["site"] = grid          # 시작 격자점 — 자리 라벨이 아니다
        out["site_label_kind"] = "legacy_grid_point (자리 아님)"
    return out


def cmd_gate(a) -> int:
    slab = load_slab()
    nslab = a.nslab
    if a.mol_ref:
        mol_ref = read(a.mol_ref)
        print(f"※ 결합 위상 기준을 --mol-ref 로 대체: {a.mol_ref}")
        print("   (기체상 ORCA 기하가 아니면 '결합이 이미 깨진 채로 기준이 되는' 위험이 있다 —")
        print("    아래 절대 기준 검사가 0 이어야 쓸 수 있다)")
        bm0 = bond_metrics(mol_ref, bond_table(mol_ref))
        print(f"   기준분자 자체 결합변화 {bm0['n_changes']} "
              f"{'✔ 사용 가능' if bm0['n_changes'] == 0 else '⛔ 사용 불가'}")
        if bm0["n_changes"]:
            return 2
    else:
        mol_ref, info = load_fragment(a.frag)
        if mol_ref is None:
            sys.exit(f"⛔ 기준 분자가 없다: {info['path']} — 결합 위상 기준을 만들 수 없다")
    clean = read(a.clean) if a.clean else None
    files = sorted(Path(a.path).glob(a.glob)) if Path(a.path).is_dir() else [Path(a.path)]
    if not files:
        sys.exit(f"⛔ {a.path} 에 {a.glob} 가 없다")
    # 레거시 스캔 에너지 붙이기 (새 계산 없이 판정까지 가려고)
    ecsv: Dict[str, float] = {}
    if a.csv:
        with open(a.csv) as fh:
            rd = csv.DictReader(l for l in fh if not l.startswith("#"))
            for r in rd:
                if "label" not in r:
                    print("⚠ CSV 에 label 열이 없다 — 에너지 결합 생략 "
                          f"(열: {list(r.keys())})"); ecsv = {}; break
                try:
                    if int(r.get("converged", 1)):
                        ecsv[r["label"]] = float(r["E_bind_eV"])
                except (ValueError, KeyError, TypeError):
                    pass
        print(f"※ 레거시 에너지 {len(ecsv)}개 결합: {a.csv}")

    rows = []
    ref = slab.cell.array
    for f in files:
        cx = read(f)
        if len(cx) <= nslab:
            print(f"⚠ {f.name}: 원자수 {len(cx)} ≤ nslab {nslab} — 건너뜀")
            continue
        own = cx.cell.array
        if np.abs(own).sum() < 1e-6:           # xyz 처럼 격자가 없는 파일에만 셀을 씌운다
            cx.set_cell(ref)
            print(f"   ※ {f.name}: 격자가 없어 repo 슬랩 셀을 씌웠다")
        else:
            # 면내는 같아야 하고, c 는 그 계산이 쓴 진공을 그대로 존중한다
            if not np.allclose(own[:2, :2], ref[:2, :2], atol=1e-3):
                print(f"   ⚠ {f.name}: 면내 격자가 repo 슬랩과 다르다 — 이미지 게이트는 이 파일 셀 기준")
            if abs(own[2, 2] - ref[2, 2]) > 1e-3:
                print(f"   ※ {f.name}: c={own[2,2]:.3f} Å (repo 슬랩 {ref[2,2]:.3f}) — **파일 셀을 쓴다**"
                      f" (셀을 갈아끼우면 없던 세로 이미지 위반이 생긴다)")
        cx.set_pbc(True)
        g = apply_gates(cx, nslab, mol_ref, a.frag, clean=clean, relaxed=a.relaxed)
        row = {"file": str(f), "label": f.stem, "fragment": a.frag, **g}
        row.update(parse_legacy_label(f.stem))
        lab = f.stem[len("complex_"):] if f.stem.startswith("complex_") else f.stem
        if lab in ecsv:
            row["E_pose_eV"] = ecsv[lab]
            row["E_pose_source"] = f"legacy UMA E_bind ({os.path.basename(a.csv)}) — 순위용, 절대값 인용 금지"
        rows.append(row)
        mark = "✔" if g["ranking_eligible"] else "⛔"
        print(f"{mark} {f.name}")
        print(f"    접촉 {g['min_contact_A']:.2f} Å ({g['min_contact_pair']}) · "
              f"Li {g['d_Li_A']} · Ni {g['d_Ni_A']} · 최근접양이온 {g['nearest_cation']}")
        print(f"    이미지 가로 {g['image_lateral_A']:.2f} / 세로 {g['image_vertical_A']:.2f} Å · "
              f"결합변화 {g['bond']['n_changes']}")
        if g.get("extraction", {}).get("flag"):
            e = g["extraction"]
            print(f"    ⛔ 추출/재구성: 표면 최대변위 {e['max_surface_disp_A']} Å · "
                  f"z_top {e['z_top_shift_A']:+.3f} Å · 이전 {e['cation_transferred_to_molecule']}")
        for r in g["gate_reasons"]:
            print(f"    ⛔ {r}")
        for w in g["warnings"]:
            print(f"    ⚠ {w}")
    if a.json:
        Path(a.json).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
        print(f"\n→ {a.json}")
    return 0


def _protocol(a, stage: str) -> Dict[str, Any]:
    p = {"tool": "site_screen.py", "stage": stage, "model": a.model, "task": a.task,
         "gap_A": a.gap, "fmax": a.fmax, "steps": a.steps,
         "freeze_frac": getattr(a, "freeze", None), "gates": GATE,
         "slab_sha256": SLAB["sha256"]}
    p["fingerprint"] = hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest()[:16]
    return p


def _guard_gpu() -> None:
    """gabia 규약 — pw.x 와 UMA 동시 실행 금지 (VRAM 47/48 GB 점유 사례)."""
    try:
        import subprocess
        out = subprocess.run(["pgrep", "-fa", "pw.x"], capture_output=True, text=True).stdout.strip()
        if out:
            sys.exit("⛔ pw.x 가 돌고 있다 — UMA 와 동시 실행 금지 (CLAUDE.md).\n" + out)
        me = subprocess.run(["pgrep", "-fc", "site_screen.py score"], capture_output=True, text=True).stdout.strip()
        if me.isdigit() and int(me) > 1:
            sys.exit("⛔ site_screen score 가 이미 돌고 있다 — 중복 실행 방지")
    except FileNotFoundError:
        pass


def _freeze_mask(slab_n: int, slab: Atoms, freeze_frac: float):
    """아래에서 freeze_frac 만큼 고정. 1.0 = 슬랩 전체 고정 (Phase-A·Codex 프로토콜)."""
    from ase.constraints import FixAtoms
    z = slab.positions[:, 2]
    zcut = z.min() + (z.max() - z.min()) * freeze_frac
    idx = [i for i in range(slab_n) if z[i] <= zcut + 1e-9]
    return FixAtoms(indices=idx), len(idx), float(zcut)


def cmd_score(a) -> int:
    """UMA rigid SP / relax. **재개 가능** — 완료된 JSON 은 건너뛴다."""
    _guard_gpu()
    from ase.optimize import FIRE
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

    slab = load_slab()
    nslab = len(slab)
    out = Path(a.out)
    atlas = out / "atlas_manifest.json"
    if not atlas.is_file():
        sys.exit(f"⛔ {atlas} 가 없다 — atlas 를 먼저 돌릴 것")
    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit(a.model, device=a.device),
                              task_name=a.task)
    proto = _protocol(a, a.stage)
    print(f"프로토콜 {proto['fingerprint']} · {a.model}/{a.task} · stage={a.stage} "
          f"· freeze={getattr(a, 'freeze', None)}")

    def sp(atoms: Atoms) -> float:
        atoms = atoms.copy(); atoms.calc = calc
        e = float(atoms.get_potential_energy())
        if not np.isfinite(e):
            raise RuntimeError("UMA 가 비유한 에너지를 반환")
        return e

    frags = a.frag or list(PRIMARY)
    for frag in frags:
        mol, info = load_fragment(frag)
        if mol is None:
            print(f"⛔ {frag}: 조각 파일이 없다 — 건너뜀 (판정 아님)")
            continue
        fdir = out / frag
        rowf = fdir / "atlas_rows.json"
        if not rowf.is_file():
            print(f"⛔ {frag}: {rowf} 가 없다 — atlas 먼저")
            continue
        rows = [r for r in json.loads(rowf.read_text()) if r["ranking_eligible"]]
        bonds = bond_table(mol)

        # 기준 에너지 — 같은 셀·같은 head. 조각 안에서는 상수라 순위에 영향 없다(기록용).
        molcell = mol.copy(); molcell.set_cell(slab.cell.array); molcell.set_pbc(True)
        molcell.positions += np.array([slab.cell[0][0], slab.cell[1][1], slab.cell[2][2]]) / 2 - molcell.get_center_of_mass()
        e_mol = sp(molcell)

        if a.stage == "rigid":
            sdir = fdir / "rigid"; sdir.mkdir(parents=True, exist_ok=True)
            e_slab = sp(slab)
            (sdir / "_references.json").write_text(json.dumps(
                {"E_slab_eV": e_slab, "E_mol_eV": e_mol, "protocol": proto,
                 "note": "E_mol 은 ORCA 기하 그대로의 UMA SP — 조각 안에서 상수라 순위에서 상쇄된다."},
                indent=1, ensure_ascii=False))
            anchors = site_anchors(slab)
            dirs = fibonacci_directions(a.ndir)
            done = 0
            for i, r in enumerate(rows, 1):
                jf = sdir / f"{r['label']}.json"
                if jf.is_file() and json.loads(jf.read_text()).get("fingerprint") == proto["fingerprint"]:
                    done += 1; continue
                dvec = _dir_from_name(mol, FRAGMENTS[frag], dirs, r["down_dir"])
                cx = make_pose(slab, mol, np.array(atlas_site_xyz(anchors, r["site"])),
                               dvec, r["roll_deg"], a.gap)
                e = sp(cx)
                jf.write_text(json.dumps({**r, "E_complex_eV": e, "E_slab_eV": e_slab,
                                          "E_mol_eV": e_mol, "E_pose_eV": e - e_slab - e_mol,
                                          "fingerprint": proto["fingerprint"], "protocol": proto},
                                         indent=1, ensure_ascii=False))
                if i % 25 == 0:
                    print(f"  [{frag} rigid {i}/{len(rows)}]", flush=True)
            print(f"■ {frag} rigid 완료 (건너뜀 {done}/{len(rows)}) → {sdir}")
            continue

        # ── relax ──────────────────────────────────────────────────────────────
        rigid = [json.loads(p.read_text()) for p in sorted((fdir / "rigid").glob("*.json"))
                 if not p.name.startswith("_")]
        if not rigid:
            print(f"⛔ {frag}: rigid 레코드가 없다 — rigid 먼저"); continue
        short = shortlist_with_matched_pairs(rigid, a.top_per_site, a.pairs)
        for ff in a.freeze:
            a.freeze_current = ff
            pr = dict(proto); pr["freeze_frac"] = ff
            pr["fingerprint"] = hashlib.sha256(json.dumps(pr, sort_keys=True).encode()).hexdigest()[:16]
            sdir = fdir / f"relax_f{ff:.2f}"; sdir.mkdir(parents=True, exist_ok=True)
            cons, nfix, zcut = _freeze_mask(nslab, slab, ff)
            # 같은 구속으로 이완한 **깨끗한 슬랩** — 기준에너지이자 추출검사의 대조군
            cs = slab.copy(); cs.set_constraint(cons); cs.calc = calc
            if ff < 1.0:
                FIRE(cs, logfile=str(sdir / "_clean_slab.log")).run(fmax=a.fmax, steps=a.steps)
            e_slab = float(cs.get_potential_energy())
            clean = cs.copy(); clean.set_constraint()
            write(sdir / "_clean_slab.vasp", clean, format="vasp", direct=True)
            (sdir / "_references.json").write_text(json.dumps(
                {"E_slab_eV": e_slab, "E_mol_eV": e_mol, "freeze_frac": ff,
                 "n_fixed": nfix, "z_cut_A": round(zcut, 3), "protocol": pr}, indent=1, ensure_ascii=False))
            print(f"■ {frag} relax freeze={ff} (고정 {nfix}/{nslab}, z≤{zcut:.2f} Å) · 대상 {len(short)}")
            for i, r in enumerate(short, 1):
                jf = sdir / f"{r['label']}.json"
                if jf.is_file() and json.loads(jf.read_text()).get("fingerprint") == pr["fingerprint"]:
                    continue
                cx = read(fdir / f"{r['label']}.xyz") if (fdir / f"{r['label']}.xyz").is_file() else None
                if cx is None:
                    print(f"  ⚠ {r['label']}: atlas 구조 파일이 없다 — 건너뜀"); continue
                cx.set_cell(slab.cell.array); cx.set_pbc(True)
                cx.set_constraint(cons); cx.calc = calc
                opt = FIRE(cx, logfile=str(sdir / f"{r['label']}.log"),
                           trajectory=str(sdir / f"{r['label']}.traj"))
                converged = bool(opt.run(fmax=a.fmax, steps=a.steps))
                e = float(cx.get_potential_energy())
                fin = cx.copy(); fin.set_constraint()
                drift = float(np.abs(fin.positions[:nfix] - slab.positions[:nfix]).max()) if nfix else 0.0
                g = apply_gates(fin, nslab, mol, frag, clean=clean, relaxed=True, bonds=bonds)
                if drift > GATE["frozen_drift_A"]:
                    g["gate_reasons"].append(f"FROZEN_DRIFT({drift:.4f}Å)"); g["ranking_eligible"] = False
                if not converged:
                    g["gate_reasons"].append(f"NOT_CONVERGED(steps>{a.steps})"); g["ranking_eligible"] = False
                write(sdir / f"{r['label']}.xyz", fin)
                jf.write_text(json.dumps({**r, "freeze_frac": ff, "converged": converged,
                                          "frozen_drift_A": drift, "E_complex_eV": e,
                                          "E_slab_eV": e_slab, "E_mol_eV": e_mol,
                                          "E_pose_eV": e - e_slab - e_mol,
                                          **{k: v for k, v in g.items() if k != "bond"},
                                          "bond_changes": g["bond"]["n_changes"],
                                          "fingerprint": pr["fingerprint"], "protocol": pr},
                                         indent=1, ensure_ascii=False))
                print(f"  [{i}/{len(short)}] {r['label']} E_pose {e - e_slab - e_mol:+.3f} eV "
                      f"{'✔' if g['ranking_eligible'] else '⛔ ' + ','.join(x.split('(')[0] for x in g['gate_reasons'])}",
                      flush=True)
    return 0


def atlas_site_xyz(anchors: Dict[str, Dict[str, Any]], site: str) -> List[float]:
    return list(anchors[site]["xyz"])


def _dir_from_name(mol: Atoms, spec: Dict[str, Any], dirs: np.ndarray, name: str) -> np.ndarray:
    if name.startswith("fib"):
        return dirs[int(name[3:])]
    gtag = spec["anchor_tag"][name]
    gi = group_indices(mol, gtag)
    v = mol.positions[gi].mean(axis=0) - mol.get_center_of_mass()
    return v / np.linalg.norm(v)


def shortlist_with_matched_pairs(rigid: List[Dict[str, Any]], top_per_site: int,
                                 n_pairs: int) -> List[Dict[str, Any]]:
    """이완 대상 고르기 — **Li/Ni 짝을 강제로 살린다**.

    점수만으로 고르면 Ni 자세가 하나도 안 남아 자리 비교가 조용히 사라진다.
    그게 '두 챔피언이 다 Li 였다'의 정체였을 수 있다. 그래서 짝을 먼저 예약한다.
    """
    ok = [r for r in rigid if r.get("ranking_eligible") and r.get("E_pose_eV") is not None]
    picked: Dict[str, Dict[str, Any]] = {}
    idx = {(r["site"], r["down_dir"], r["roll_deg"]): r for r in ok}
    pairs = []
    for (s, d, ro), r in idx.items():
        if s != "Li_top":
            continue
        q = idx.get(("Ni_top", d, ro))
        if q:
            pairs.append((min(r["E_pose_eV"], q["E_pose_eV"]), r, q))
    for _, r, q in sorted(pairs, key=lambda t: t[0])[:n_pairs]:
        picked[r["label"]] = r
        picked[q["label"]] = q
    by_site = defaultdict(list)
    for r in ok:
        by_site[r["site"]].append(r)
    for s, v in by_site.items():
        for r in sorted(v, key=lambda x: x["E_pose_eV"])[:top_per_site]:
            picked[r["label"]] = r
    return sorted(picked.values(), key=lambda r: (r["site"], r["E_pose_eV"]))


def cmd_verdict(a) -> int:
    """자리 선호 판정 — 검열 회계 · 대조쌍 · 판정 바닥을 한 표에."""
    rows: List[Dict[str, Any]] = []
    for p in a.rows:
        q = Path(p)
        if q.is_dir():                       # score 단계의 자세별 JSON 디렉터리
            for f in sorted(q.glob("*.json")):
                if f.name.startswith("_"):
                    continue
                rows.append(json.loads(f.read_text()))
        else:                                # atlas_rows.json 같은 리스트 파일
            payload = json.loads(q.read_text())
            rows += payload if isinstance(payload, list) else [payload]
    if not rows:
        sys.exit("⛔ 입력 행이 없다")
    fz = sorted({r.get("freeze_frac") for r in rows if r.get("freeze_frac") is not None})
    if len(fz) > 1:
        print(f"⚠ freeze_frac 이 섞여 있다 {fz} — 프로토콜이 다르면 같은 표에 놓지 않는다.\n")
    scored = [r for r in rows if r.get("ranking_eligible") and r.get("E_pose_eV") is not None]
    frags = sorted({r["fragment"] for r in rows})
    print("자리 선호 판정 (같은 조각 안에서만 유효)\n")
    for frag in frags:
        fr = [r for r in rows if r["fragment"] == frag]
        fs = [r for r in scored if r["fragment"] == frag]
        print(f"■ {frag}   생성 {len(fr)} · 순위가능 {len([r for r in fr if r.get('ranking_eligible')])} "
              f"· 점수있음 {len(fs)}")
        print(f"   {FRAGMENTS[frag]['electrons']}")
        if not fs:
            print("   ⛔ 점수가 없다 — score 단계를 돌리지 않았다. **판정 아님**\n")
            continue
        by_site = defaultdict(list)
        for r in fs:
            by_site[r.get("site_from_geometry") or r["site"]].append(r)
        print(f"   {'자리':16s} {'n':>4s} {'최저':>9s} {'중앙값':>9s} {'폭':>8s}")
        for s in sorted(by_site, key=lambda s: min(x["E_pose_eV"] for x in by_site[s])):
            E = sorted(x["E_pose_eV"] for x in by_site[s])
            print(f"   {s:16s} {len(E):4d} {E[0]:+9.3f} {E[len(E)//2]:+9.3f} {E[-1]-E[0]:8.3f}")
        # 검열 회계
        cens = Counter()
        for r in fr:
            if not r.get("ranking_eligible"):
                cens[(r["site"], (r.get("gate_reasons") or ["?"])[0].split("(")[0])] += 1
        if cens:
            print("   검열(게이트로 죽은 시작자리) — '졌다'가 아니라 '못 쟀다':")
            for (s, why), n in sorted(cens.items()):
                print(f"     {s:12s} {why:24s} {n}")
        # 대조쌍
        pairs = []
        idx = {(r["site"], r["down_dir"], r["roll_deg"]): r for r in fs}
        for (s, d, ro), r in idx.items():
            if s != "Li_top":
                continue
            q = idx.get(("Ni_top", d, ro))
            if q:
                pairs.append((d, ro, r["E_pose_eV"], q["E_pose_eV"], q["E_pose_eV"] - r["E_pose_eV"]))
        if pairs:
            dl = [p[4] for p in pairs]
            print(f"   Li_top↔Ni_top 짝지은 대조쌍 {len(pairs)}개 · "
                  f"ΔE(Ni−Li) 중앙값 {np.median(dl):+.3f} eV · 범위 {min(dl):+.3f}…{max(dl):+.3f}")
            floor = max(GATE["decision_floor_eV"], float(np.std(dl)))
            if abs(float(np.median(dl))) < floor:
                print(f"   → **가려지지 않았다** (|Δ| < 판정바닥 {floor:.3f} eV = max(30 meV, 쌍 편차))")
            else:
                win = "Li" if np.median(dl) > 0 else "Ni"
                print(f"   → 이 프로토콜에서 {win} 우세 (판정바닥 {floor:.3f} eV 초과). "
                      f"열역학 판정 아님 — DFT+U 대조 필요.")
        else:
            print("   ⛔ 짝지은 Li/Ni 대조쌍이 없다 (레거시 스캔에는 자리 라벨이 없다).")
            # 짝이 없으면 **분포 비교**만 가능하다 — 교란되어 있음을 반드시 같이 적는다.
            li = [r["E_pose_eV"] for r in fs if r.get("nearest_cation") == "Li"]
            ni = [r["E_pose_eV"] for r in fs if r.get("nearest_cation") == "Ni"]
            if li and ni:
                d = min(ni) - min(li)
                sp = max(np.std(li), np.std(ni))
                floor = max(GATE["decision_floor_eV"], float(sp))
                print(f"   [짝 아님·분포 비교] Li 접촉 n={len(li)} 최저 {min(li):+.3f} · "
                      f"Ni 접촉 n={len(ni)} 최저 {min(ni):+.3f} · Δ(Ni−Li) {d:+.3f} eV")
                print(f"     자세 폭 σ={sp:.3f} eV → 판정바닥 {floor:.3f} eV")
                if abs(d) < floor:
                    print("     → **가려지지 않았다**")
                else:
                    print(f"     → 분포상 {'Li' if d > 0 else 'Ni'} 쪽이 낮다. 다만 두 집합은 "
                          "**방향·roll·격자점이 서로 달라** 자리 이외의 요인이 섞여 있다 —")
                    print("       이것만으로 자리 선호를 주장할 수 없다(짝지은 대조쌍이 필요).")
            elif li or ni:
                only = "Li" if li else "Ni"
                print(f"   ⛔ {only} 접촉 자세만 점수가 있다 — 비교 자체가 성립하지 않는다.")
        print()
    return 0


def cmd_crosscheck(a) -> int:
    """Codex ptfe_linio2_uma 레코드와 자세별 기하 대조 (GPU 불필요, 순수 기하)."""
    slab = load_slab()
    d = Path(a.codex)
    recs = sorted(d.glob("**/*.json"))
    if not recs:
        sys.exit(f"⛔ {d} 에 json 레코드가 없다")
    n_ok = n_dis = 0
    disagreements = []
    for p in recs:
        try:
            r = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        if not isinstance(r, dict) or "model" not in r:
            continue
        frag = {"dimer": "ptfe_dimer", "c10": "ptfe_c10"}.get(r.get("model"))
        if not frag:
            continue
        sfile = r.get("structure_xyz") or r.get("structure", {}).get("xyz")
        if not sfile or not Path(sfile).is_file():
            continue
        mol_ref, _ = load_fragment(frag)
        cx = read(sfile)
        cx.set_cell(slab.cell.array); cx.set_pbc(True)
        g = apply_gates(cx, len(slab), mol_ref, frag, relaxed=bool(r.get("relaxed")))
        theirs = bool(r.get("ranking_eligible"))
        if theirs == g["ranking_eligible"]:
            n_ok += 1
        else:
            n_dis += 1
            disagreements.append((p.name, theirs, g["ranking_eligible"], g["gate_reasons"],
                                  r.get("classification")))
    print(f"자세 게이트 대조: 일치 {n_ok} · 불일치 {n_dis}")
    for name, t, o, why, cls in disagreements[:30]:
        print(f"  ⚠ {name}: Codex={t} / 우리={o} · 우리사유={why} · Codex분류={cls}")
    if n_ok + n_dis == 0:
        print("⛔ 대조할 레코드를 못 찾았다 — --codex 경로가 Codex 실행 산출물 디렉터리인지 확인")
        return 2
    return 0 if n_dis == 0 else 1


def cmd_selftest(a) -> int:
    """게이트가 **실제로 발동하는지** 아는 사고를 재현해 검증한다.

    통과 케이스만 보고 '잘 된다'고 말하면 그건 검증이 아니다. 각 게이트마다
    걸려야 하는 구조를 일부러 만들어 넣고, 그 게이트가(그리고 그것만) 걸리는지 본다.
    """
    slab = load_slab()
    n = len(slab)
    cell = slab.cell.array
    mol, _ = load_fragment("ptfe_c10")
    if mol is None:
        sys.exit("⛔ ptfe_c10 이 없다 — 자체검사 불가")
    bonds = bond_table(mol)
    anc = site_anchors(slab)
    down = np.array([0.0, 0.0, 1.0])
    ok = True

    def check(name: str, cx: Atoms, want: str, relaxed=False, clean=None, frag="ptfe_c10", mref=None):
        nonlocal ok
        g = apply_gates(cx, n, mref if mref is not None else mol, frag,
                        clean=clean, relaxed=relaxed, bonds=None if mref is not None else bonds)
        hit = [r.split("(")[0] for r in g["gate_reasons"]]
        good = (want in hit) if want else (not hit)
        ok &= good
        print(f"   {'✔' if good else '⛔'} {name:34s} 기대={want or '통과':22s} 실제={hit or ['통과']}")
        return g

    print("게이트 자체검사 (일부러 나쁜 구조를 만들어 넣는다)\n")

    # 0) 정상 자세는 통과해야 한다
    check("정상 자세 (Li_top, gap 2.4)", make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 2.4), "")

    # 1) 충돌
    check("충돌 (gap 0.6 Å)", make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 0.6), "COLLISION")

    # 2) 가로 이미지 — 장축을 최단 격자(b, 11.51 Å)에 눕힌다
    b_hat = cell[1] / np.linalg.norm(cell[1])
    long_axis = mol.positions[int(np.argmax(mol.positions[:, 2]))] - mol.positions[int(np.argmin(mol.positions[:, 2]))]
    lay = mol.copy()
    lay.positions = lay.positions @ rot_align(long_axis, b_hat).T
    check("가로 이미지 (장축을 b 축에 눕힘)",
          make_pose(slab, lay, anc["Li_top"]["xyz"], np.array([1.0, 0, 0]), 0, 2.4), "IMAGE_LATERAL")

    # 3) 세로 이미지 — 2026-07 '샌드위치' 재현: 분자를 진공 위쪽 슬랩 이미지에 붙인다
    cx = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 2.4)
    cx.positions[n:, 2] += (cell[2][2] - (cx.positions[:n, 2].max() - cx.positions[:n, 2].min())) - 8.0
    check("세로 이미지 (진공 너머 슬랩에 접근)", cx, "IMAGE_VERTICAL")

    # 4) 결합 위상 — C–F 를 끊어 놓는다
    cx = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 2.4)
    sym = cx.get_chemical_symbols()
    fi = next(i for i in range(n, len(cx)) if sym[i] == "F")
    cx.positions[fi] += np.array([0.0, 0.0, 1.2])
    check("결합 절단 (C–F 를 1.2 Å 끌어냄)", cx, "BOND_TOPOLOGY")

    # 5) cap 아티팩트 — dimer 의 H 를 아래로, 이완본으로 취급
    dm, _ = load_fragment("ptfe_dimer")
    dsym = dm.get_chemical_symbols()
    com = dm.get_center_of_mass()
    # 두 H 는 사슬 양 끝이라 평균이 COM 과 겹친다 — **한 개**를 골라야 방향이 생긴다
    hi = max((i for i in range(len(dm)) if dsym[i] == "H"),
             key=lambda i: np.linalg.norm(dm.positions[i] - com))
    cxd = make_pose(slab, dm, anc["Li_top"]["xyz"], dm.positions[hi] - com, 0, 2.4)
    check("cap 아티팩트 (H 아래, 이완본)", cxd, "CAP_ARTIFACT",
          relaxed=True, frag="ptfe_dimer", mref=dm)
    check("cap 아래 시작 (시작자세면 경고만)", cxd, "", relaxed=False, frag="ptfe_dimer", mref=dm)

    # 6) 분리 — 짧은 dimer 로 해야 세로 이미지와 섞이지 않는다
    check("분리 (dimer, gap 6.0 Å, 이완본)",
          make_pose(slab, dm, anc["Li_top"]["xyz"], down, 0, 6.0), "DETACHED",
          relaxed=True, frag="ptfe_dimer", mref=dm)

    # 7) 거리 게이트 재교정 검증 — 융합급만 죽고, 짧은 배위는 살아야 한다
    li = anc["Li_top"]["atoms"][0]

    def at_height(h: float) -> Atoms:
        c = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 2.4)
        low = n + int(np.argmin(c.positions[n:, 2]))
        c.positions[n:] += (c.positions[li] + np.array([0, 0, h])) - c.positions[low]
        return c

    # F–Li: Σr_cov = 1.85 Å → 탈락 < 1.48 · 경고 < 1.70
    check("융합급 접촉 (F···Li 1.35 Å < 0.80Σ)", at_height(1.35), "REACTIVE_CONTACT")
    g = check("짧은 배위 (F···Li 1.60 Å) 는 죽이지 않는다", at_height(1.60), "")
    ok_short = any(w.startswith("short_contact") for w in g["warnings"])
    ok &= ok_short
    print(f"   {'✔' if ok_short else '⛔'} {'  └ short_contact 태그가 붙는다':34s} "
          f"실제 경고={g['warnings']}")
    g = check("정상 배위 (F···Li 2.00 Å) 는 경고도 없다", at_height(2.00), "")
    no_short = not any(w.startswith("short_contact") for w in g["warnings"])
    ok &= no_short
    print(f"   {'✔' if no_short else '⛔'} {'  └ 태그 없음':34s} 실제 경고={g['warnings']}")

    # 8) Li 추출 — 표면 Li 를 분자 쪽으로 1.5 Å 끌어올린다 (freeze 0.6 사고의 재현)
    cx = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 3.2)
    cx.positions[li, 2] += 1.5
    check("Li 추출/재구성 (표면 Li +1.5 Å)", cx, "EXTRACTION_OR_RECONSTRUCTION", clean=slab)

    # 9) 거울상 방지 — 반평행 정렬이 카이랄성을 뒤집지 않는지
    try:
        make_pose(slab, mol, anc["Li_top"]["xyz"], np.array([0.0, 0.0, -1.0]), 0, 2.4)
        make_pose(slab, mol, anc["Li_top"]["xyz"], np.array([0.0, 0.0, 1.0]), 0, 2.4)
        print("   ✔ 반평행 정렬에서 거울상/변형 없음")
    except RuntimeError as e:
        ok = False
        print(f"   ⛔ 반평행 정렬: {e}")

    print(f"\n{'✔ 전부 통과' if ok else '⛔ 실패 있음'}")
    return 0 if ok else 1


def cmd_bond_limits(a) -> int:
    print("결합 유지 임계 (형성 / 절단 / 과단축) [Å]")
    for k, v in BOND_LIMITS.items():
        src = "Codex 동일" if k in ("C-C", "C-F", "C-H") else "ORCA 실측 최대 × (1.10/1.20/0.80)"
        print(f"   {k:5s}  {v[0]:.2f} / {v[1]:.2f} / {v[2]:.2f}   ({src})")
    print("\n조각별 실측 결합길이:")
    for name in FRAGMENTS:
        mol, info = load_fragment(name)
        if mol is None:
            print(f"   {name:20s} (파일 없음)")
            continue
        sym = mol.get_chemical_symbols(); D = mol.get_all_distances()
        tab = defaultdict(list)
        for i in range(len(mol)):
            for j in range(i + 1, len(mol)):
                lab = "-".join(sorted((sym[i], sym[j])))
                if lab in BOND_LIMITS and D[i, j] <= BOND_LIMITS[lab][0]:
                    tab[lab].append(D[i, j])
        print(f"   {name:20s} " + " ".join(f"{k}:{min(v):.2f}-{max(v):.2f}({len(v)})"
                                           for k, v in sorted(tab.items())))
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("inputs", help="입력 검증 (원자수·sha·전자상태)")
    sub.add_parser("sites", help="표면 자리 열거 + 대표 동치성 검사")
    sub.add_parser("bond-limits", help="결합 임계표와 실측치")
    sub.add_parser("selftest", help="게이트 회귀시험 — 일부러 나쁜 구조를 넣어 발동 확인")

    p = sub.add_parser("atlas", help="자세 아틀라스 생성")
    p.add_argument("--frag", nargs="*", default=None, help=f"기본: {' '.join(PRIMARY)}")
    p.add_argument("--out", required=True)
    p.add_argument("--gap", type=float, default=2.4)
    p.add_argument("--ndir", type=int, default=12, help="피보나치 구면 방향 수")
    p.add_argument("--rolls", nargs="*", type=float, default=[0, 90, 180, 270])
    p.add_argument("--dry-run", action="store_true", help="구조 파일은 안 쓰고 통계만")

    p = sub.add_parser("gate", help="구조 묶음에 게이트 적용")
    p.add_argument("path")
    p.add_argument("--frag", required=True, choices=sorted(FRAGMENTS))
    p.add_argument("--glob", default="*.xyz")
    p.add_argument("--nslab", type=int, default=192)
    p.add_argument("--clean", default=None, help="깨끗한 슬랩 (추출 검사에 필요)")
    p.add_argument("--mol-ref", default=None,
                   help="결합 위상 기준 분자를 파일로 대체 (등록부 조각이 아직 없을 때)")
    p.add_argument("--csv", default=None,
                   help="레거시 스캔 결과 CSV (label,E_bind_eV,converged) — 자세에 에너지를 붙인다")
    p.add_argument("--relaxed", action="store_true", help="이완 후 구조로 취급(분리·추출 게이트 켜짐)")
    p.add_argument("--json", default=None)

    p = sub.add_parser("score", help="UMA rigid SP / relax (gabia)")
    p.add_argument("--out", required=True, help="atlas 를 만든 디렉터리")
    p.add_argument("--stage", choices=("rigid", "relax"), required=True)
    p.add_argument("--frag", nargs="*", default=None)
    p.add_argument("--model", default="uma-s-1p1")
    p.add_argument("--task", default="omat", help="omat | oc20 — head 를 바꾸면 결과는 별도 계열")
    p.add_argument("--device", default="cuda")
    p.add_argument("--gap", type=float, default=2.4)
    p.add_argument("--ndir", type=int, default=12)
    p.add_argument("--fmax", type=float, default=0.05)
    p.add_argument("--steps", type=int, default=300)
    p.add_argument("--freeze", nargs="*", type=float, default=[1.0, 0.85],
                   help="1.0=Phase-A/Codex 프로토콜, 0.85=표면 이완 허용. 둘 다 돌려 편향을 드러낸다.")
    p.add_argument("--top-per-site", type=int, default=2)
    p.add_argument("--pairs", type=int, default=5, help="강제로 살릴 Li/Ni 대조쌍 수")

    p = sub.add_parser("verdict", help="자리 선호 판정표")
    p.add_argument("rows", nargs="+", help="atlas_rows.json 또는 점수가 붙은 rows json")

    p = sub.add_parser("crosscheck", help="Codex 레코드와 게이트 대조")
    p.add_argument("--codex", required=True)
    return ap


def main() -> int:
    a = build_parser().parse_args()
    return {
        "inputs": cmd_inputs, "sites": cmd_sites, "atlas": cmd_atlas,
        "gate": cmd_gate, "verdict": cmd_verdict, "crosscheck": cmd_crosscheck,
        "bond-limits": cmd_bond_limits, "selftest": cmd_selftest, "score": cmd_score,
    }[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
