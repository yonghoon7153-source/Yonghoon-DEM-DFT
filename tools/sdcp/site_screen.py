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
from math import comb
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
        # 2026-08-11 gabia 회수본으로 고정. 원본:
        #   /data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c/sdcp_v7c_neutral.xyz (ORCA r2SCAN-3c)
        # ⚠ 파일이 아직 repo 에 커밋되지 않았다 — 등재 전까지 inputs 가 MISSING 을 보고한다.
        "sha256": "fc5ed6da243b33923aecd7c3c5781f98366da6dba48c222ca76b9f4ba67039e0",
        "electrons": "closed-shell singlet (charge 0)",
        "cap": (),
        "anchor_tag": {"sulfonate_down": "SO3", "thiophene_down": "thiophene_S"},
        "note": "−SO₃H 보호형. Phase-A/B 의 mol_neutral.",
    },
    "sdcp_doped": {
        "path": STRUCT / "sdcp_v7c_doped.xyz",
        "counts": {"C": 11, "H": 15, "O": 6, "S": 2},
        # 원본: .../inputs/sdcp_v7c/sdcp_v7c_doped.xyz (ORCA r2SCAN-3c, doublet)
        "sha256": "4d0ca2ac299fb14d231bb900f1228efe43ed7fbe28d5044607d172771a847620",
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
    # (구 "extract_disp_A": 0.50 은 폐기 — 아래 원소별 임계로 대체됐다. 죽은 키를 남겨 두면
    #  JSON·문서에서 여전히 유효한 규약처럼 읽힌다.)
    # ⚠ 2026-08-11 2차 재교정 (Codex 교차검증 지적, 채택) — 예전에는 "슬랩 양이온이 분자
    #   O/F/S 에 < 2.20 Å" **하나만으로** 추출로 판정했다. 그건 거리 컷 오판의 재발이다:
    #   변위가 0.00 Å 인 정상 Li–O 배위(2.0–2.2 Å)도 추출로 죽는다(Codex 가 실제 코드로 재현).
    #   추출은 **움직였고(변위) + 기판 배위를 잃었을 때**만 성립한다. 분자 접촉은 보조 증거다.
    "extract_disp_Li_A": 0.80,    # Li 는 원래 잘 움직인다 — 더 관대하게
    "extract_disp_NiO_A": 0.50,   # Ni/O 가 이만큼 움직이면 재구성 의심(경고)
    "extract_coord_cut_A": 2.50,  # 기판 Li–O 이웃 판정 반경
    "extract_coord_loss_n": 2,    # 잃은 기판 O 이웃 수 (이만큼 잃어야 '뽑혔다')
    "extract_contact_A": 2.20,    # 분자 O/F/S 접촉 — **보조 증거만**, 단독 탈락 금지
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


def _mic_full(vec: np.ndarray, cell: np.ndarray) -> np.ndarray:
    """3차원 최소이미지 벡터 (기울어진 셀 대응)."""
    frac = np.linalg.solve(cell.T, vec)
    frac -= np.round(frac)
    return frac @ cell


def _unwrap_by_bonds(pos: np.ndarray, bonds: Sequence[Tuple[int, int, str]],
                     cell: np.ndarray) -> np.ndarray:
    """감긴(wrapped) 분자를 **결합 그래프를 따라** MIC 로 편다.

    원자 0 기준의 통짜 MIC 는 쓰면 안 된다 — C10 장축(13.9 Å)이 b/2(5.8 Å)보다 길어
    멀쩡한 구조를 접어 버린다. 결합 길이(≤1.9 Å)는 반쪽 셀보다 훨씬 짧으므로
    이웃→이웃 MIC 는 항상 안전하고, 정상 구조에서는 무연산이다.
    """
    n = len(pos)
    adj: Dict[int, List[int]] = {i: [] for i in range(n)}
    for i, j, _lab in bonds:
        if i < n and j < n:
            adj[i].append(j); adj[j].append(i)
    out = pos.copy()
    seen = set()
    for root in range(n):
        if root in seen:
            continue
        seen.add(root)
        stack = [root]
        while stack:
            i = stack.pop()
            for j in adj[i]:
                if j in seen:
                    continue
                seen.add(j)
                out[j] = out[i] + _mic_full(pos[j] - pos[i], cell)
                stack.append(j)
    return out


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
    # basin 서술자 — 자세가 '같은 골짜기'인지 판정하는 데 쓴다 (Codex 방식 이식·일반화).
    # Codex 는 사슬축(azimuth/tilt)을 썼는데 SDCP 는 사슬이 없으므로 **관성 주축**으로 일반화한다.
    mp = cx.positions[nslab:]
    q = mp - mp.mean(axis=0)
    axis = np.linalg.eigh(q.T @ q)[1][:, -1]
    azim = math.degrees(math.atan2(float(axis[1]), float(axis[0]))) % 180.0
    tilt = math.degrees(math.asin(min(1.0, abs(float(axis[2])))))
    com_h = float(mp.mean(axis=0)[2] - zs.max())

    return {
        "min_contact_A": round(dmin, 3), "min_contact_pair": pair,
        "axis_azimuth_deg_mod180": round(azim, 2),
        "axis_tilt_from_plane_deg": round(tilt, 2),
        "com_height_above_slab_A": round(com_h, 3),
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
    # ★ 자체 리뷰 #5 — clean 과 복합체 앞 nslab 의 대응을 검증 없이 인덱스로 비교하면,
    #   다르게 정렬된 슬랩이 들어왔을 때 **엉뚱한 원자끼리의 변위**로 대량 오판이 난다.
    if (len(clean) < nslab
            or clean.get_chemical_symbols()[:nslab] != cx.get_chemical_symbols()[:nslab]):
        return {"verdict": "CLEAN_MISMATCH", "flag": False,
                "note": "clean 슬랩이 복합체 앞 nslab 원자와 원소/순서가 다르다 — "
                        "추출검사 불가 (판정 아님). 같은 정렬의 슬랩을 --clean 으로 줄 것."}
    """Li 추출 / 표면 재구성 격리 — 'freeze 0.6 의 −1.465 eV' 를 결합으로 오독한 사건의 재발 방지.

    VASP dE_extract = +0.336 eV(2026-08-08) 로 추출이 열역학적으로 불리함이 확인됐으므로,
    추출형 끝점은 **결합 순위에서 빼고 따로 센다**.
    """
    sym = cx.get_chemical_symbols()
    cell = cx.cell.array
    zc = clean.positions[:, 2]
    surf = [i for i in range(nslab) if zc[i] > zc.max() - 1.2]

    # 변위는 **최소이미지**로 — 셀 경계를 넘어 감긴 원자를 '크게 이동'으로 오독하지 않게.
    dv = np.array([_mic_xy(cx.positions[i] - clean.positions[i], cell) for i in range(nslab)])
    disp = np.linalg.norm(dv, axis=1)

    def lim(el: str) -> float:
        return GATE["extract_disp_Li_A"] if el == "Li" else GATE["extract_disp_NiO_A"]

    moved = [(i, sym[i], round(float(disp[i]), 3)) for i in surf if disp[i] > lim(sym[i])]

    # 기판 배위 손실 — 깨끗한 슬랩에서 가졌던 O 이웃을 몇 개나 잃었나
    rc = GATE["extract_coord_cut_A"]
    Dc = mic_matrix(clean.positions[:nslab], clean.positions[:nslab], cell)
    Dx = mic_matrix(cx.positions[:nslab], cx.positions[:nslab], cell)
    oidx = [j for j in range(nslab) if sym[j] == "O"]
    lost, hop = [], []
    for i in surf:
        if sym[i] not in CATIONS:
            continue
        # ⚠ Round-2 지적 (채택): 이전 이웃의 **identity** 상실로 세면, 면내로 hop 하면서
        #   새 O 를 같은 수만큼 얻은 Li 도 '뽑혔다'가 된다. **배위수(count)** 차로 센다.
        cn_before = sum(1 for j in oidx if Dc[i, j] < rc)
        cn_after = sum(1 for j in oidx if Dx[i, j] < rc)
        same_id = len({j for j in oidx if Dc[i, j] < rc} & {j for j in oidx if Dx[i, j] < rc})
        if cn_before - cn_after >= GATE["extract_coord_loss_n"]:
            lost.append((i, sym[i], cn_before, cn_after))
        elif cn_before - same_id >= GATE["extract_coord_loss_n"]:
            # 이웃이 바뀌었지만 배위수는 유지 — 면내 hop / 재배열이지 추출이 아니다
            hop.append((i, sym[i], cn_before, cn_after, same_id))

    # 분자 접촉 — **보조 증거만**. 단독으로는 절대 탈락시키지 않는다.
    Dm = mic_matrix(cx.positions[:nslab], cx.positions[nslab:], cell)
    contact = []
    for i in surf:
        if sym[i] not in CATIONS:
            continue
        j = int(np.argmin(Dm[i]))
        if Dm[i, j] < GATE["extract_contact_A"] and sym[nslab + j] in ("O", "F", "S"):
            contact.append((i, sym[i], sym[nslab + j], round(float(Dm[i, j]), 3)))

    moved_ids = {i for i, _, _ in moved}
    lost_ids = {i for i, _, _, _ in lost}
    # 추출은 **바깥으로** 나가는 것이다 — 면내 이동은 hop 이지 추출이 아니다.
    outward = {i for i in surf if dv[i][2] > 0.0}
    extracted = sorted(moved_ids & lost_ids & outward)
    if extracted:
        verdict = "EXTRACTION_CANDIDATE"
    elif hop or (moved_ids & lost_ids):
        verdict = "LATERAL_HOP_OR_RECONSTRUCTION"      # 배위수 유지 · 또는 안쪽으로 이동
    elif moved or lost:
        verdict = "RECONSTRUCTION_REVIEW"
    else:
        verdict = "NORMAL_COORDINATION"
    return {
        "verdict": verdict,
        "max_surface_disp_A": round(float(max([disp[i] for i in surf], default=0.0)), 3),
        "z_top_shift_A": round(float(cx.positions[:nslab, 2].max() - zc.max()), 3),
        "moved_surface_atoms": moved,
        "lost_substrate_O_coordination": lost,   # (idx, el, CN_before, CN_after)
        "neighbor_swap_no_CN_loss": hop,         # 면내 hop — 추출로 세지 않는다
        "cation_near_molecule": contact,         # 증거일 뿐 — 판정에 단독으로 못 쓴다
        "extracted_indices": extracted,
        "flag": bool(extracted),                 # 탈락은 EXTRACTION_CANDIDATE 뿐
    }


def apply_gates(cx: Atoms, nslab: int, mol_ref: Atoms, frag: str,
                clean: Optional[Atoms] = None, relaxed: bool = False,
                bonds: Optional[Sequence[Tuple[int, int, str]]] = None) -> Dict[str, Any]:
    """모든 게이트를 한 번에. **판정 불가와 실패를 구분한다.**

    ⚠ 전제 — 원자 순서는 **슬랩 원본 순서가 먼저, 분자가 뒤**다. 종별로 재정렬된
      POSCAR/CONTCAR(우리 _write_poscar 산출물 포함)를 직접 넣으면 안 된다.
      cmd_gate 가 이 전제를 파일마다 검사한다 (자체 리뷰 #4).
    """
    cell = cx.cell.array
    mp = cx.positions[nslab:]
    sp = cx.positions[:nslab]
    mol = cx[nslab:]
    mol.set_pbc(False)
    bl = bond_table(mol_ref) if bonds is None else bonds
    # VASP 류 출력은 좌표를 셀 안으로 감는다 — 감긴 분자는 결합 검사에서 전부 절단,
    # 이미지 검사에서 자기 이미지와 거리 0 으로 오판된다. 결합 그래프를 따라 MIC 로 편
    # 좌표(mpu)로 결합·이미지를 검사한다(정상 구조에는 무연산). 접촉은 MIC 라 무관.
    mpu = _unwrap_by_bonds(mp, bl, cell)
    mol.positions[:] = mpu
    stats = contact_stats(cx, nslab)
    lat = lateral_image_min(mpu, cell)
    ver = vertical_image_min(mpu, sp, cell)
    bm = bond_metrics(mol, bl)
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
        if ex["verdict"] == "CLEAN_MISMATCH":
            warns.append("extraction_not_checked(clean_mismatch)")   # 판정 아님 — 크게 표시
        elif ex["flag"]:
            reasons.append(f"EXTRACTION_CANDIDATE(idx {ex['extracted_indices'][:4]})")
        elif ex["verdict"] == "RECONSTRUCTION_REVIEW":
            # 죽이지 않는다 — 다만 기준선이 달라졌을 수 있으니 표시하고 verdict 가 따로 센다
            warns.append(f"reconstruction_review(disp {ex['max_surface_disp_A']}Å)")
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
        if info["status"] != "OK":
            # ⚠ 경고로 흘려보내면 **다른 분자로 스캔한 결과가 이름만 맞게** 남는다
            #   (2026-08-11 Codex 지적, 채택). 입력이 선언과 다르면 여기서 멈춘다.
            sys.exit(f"⛔ {frag}: 입력이 선언과 다르다 ({info['status']}) — 중단.\n"
                     f"   {info}\n   등록부의 sha256/조성을 고치든지, 파일을 정본으로 되돌릴 것.")
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


# ── basin 클러스터링 (Codex ptfe_linio2_uma 에서 이식·일반화) ─────────────────────
#   왜 필요한가 — 자세 20개를 20개의 독립 후보로 세면 안 된다. 같은 골짜기에 굴러 들어간
#   자세들은 하나다. 그걸 세지 않으면 "다양한 후보를 넘겼다"가 착각이 된다.
#   1×4 초격자라 **b축 frac 0.25 병진은 같은 물리 자세**다 — 실측 확인(2026-08-11):
#   등가 표면 원자들이 정확히 frac b +0.25 간격으로 반복한다. Codex 구현이 우리 셀에 그대로 맞다.
BASIN_TOL = {
    "count": 1,          # 접촉 개수 차
    "dist_A": 0.60,      # 원소별 최단거리 차
    "azimuth_deg": 35.0, # 주축 방위 차 (mod 180)
    "tilt_deg": 20.0,    # 면 대비 기울기 차
    "height_A": 0.75,    # COM 높이 차
    "rmsd_A": 0.75,      # 분자 원자별 주기 RMSD
}


def molecule_rmsd_A(left: Atoms, right: Atoms, nslab: int) -> float:
    """분자 부분의 원자별 RMSD. **1×4 b축 병진(0/¼/½/¾)을 다 시도해 최소를 취한다.**"""
    if left.get_chemical_symbols() != right.get_chemical_symbols():
        return float("inf")
    cell = np.asarray(left.cell.array, float)
    delta = np.asarray(right.positions[nslab:] - left.positions[nslab:], float)
    frac = np.linalg.solve(cell.T, delta.T).T
    best = np.inf
    for shift in (0.0, 0.25, 0.5, 0.75):
        f = frac.copy()
        f[:, 1] -= shift
        f[:, :2] -= np.round(f[:, :2])
        cart = f @ cell
        best = min(best, float(np.sqrt(np.mean(np.sum(cart * cart, axis=1)))))
    return best


def _pair_key(reg: Dict[str, Any], el: str) -> int:
    return sum(v for k, v in (reg or {}).items() if k.endswith(f"-{el}"))


def same_basin(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """서술자만으로 같은 골짜기인지 (구조 파일 없이 판정 — 진단용 proxy)."""
    if a.get("nearest_cation") != b.get("nearest_cation"):
        return False
    for el in CATIONS:
        if abs(_pair_key(a.get("registry"), el) - _pair_key(b.get("registry"), el)) > BASIN_TOL["count"]:
            return False
        da, db = a.get(f"d_{el}_A"), b.get(f"d_{el}_A")
        if (da is None) != (db is None):
            return False
        if da is not None and abs(da - db) > BASIN_TOL["dist_A"]:
            return False
    az = abs(a.get("axis_azimuth_deg_mod180", 0.0) - b.get("axis_azimuth_deg_mod180", 0.0))
    if min(az, 180.0 - az) > BASIN_TOL["azimuth_deg"]:
        return False
    if abs(a.get("axis_tilt_from_plane_deg", 0.0) - b.get("axis_tilt_from_plane_deg", 0.0)) > BASIN_TOL["tilt_deg"]:
        return False
    if abs(a.get("com_height_above_slab_A", 0.0) - b.get("com_height_above_slab_A", 0.0)) > BASIN_TOL["height_A"]:
        return False
    return True


def cluster_basins(rows: Sequence[Dict[str, Any]], struct_dir: Optional[Path] = None,
                   nslab: int = 192) -> List[List[Dict[str, Any]]]:
    """서술자로 1차 묶고, 구조가 있으면 주기 RMSD 로 **더 묶는다**(합치기만, 쪼개지 않음).

    ⚠ 자동 basin 라벨은 진단용 proxy 다 — 대칭 등가를 다르게 세거나 다른 것을 합칠 수 있다.
    물리적으로 독립인 basin 수는 구조를 눈으로 보고 확정할 것 (Codex 와 같은 단서).
    """
    clusters: List[List[Dict[str, Any]]] = []
    cache: Dict[str, Atoms] = {}

    def load(r) -> Optional[Atoms]:
        if struct_dir is None:
            return None
        lab = r.get("label")
        if lab in cache:
            return cache[lab]
        p = struct_dir / f"{lab}.xyz"
        if not p.is_file():
            return None
        cache[lab] = read(p)
        return cache[lab]

    for r in sorted(rows, key=lambda x: x.get("E_pose_eV") if x.get("E_pose_eV") is not None else 0.0):
        placed = False
        for cl in clusters:
            head = cl[0]
            # ⚠ Round-2 지적 (채택): 초판은 `서술자 OR RMSD` 였다 — RMSD 경로가 registry 검사를
            #   통째로 우회해서 Li 접촉과 Ni 접촉이 합쳐질 수 있었다. **AND** 로 조인다.
            if head.get("nearest_cation") != r.get("nearest_cation"):
                continue                                  # 최종 registry 가 다르면 같은 basin 이 아니다
            if not same_basin(head, r):
                continue
            A, B = load(head), load(r)
            if A is not None and B is not None:
                if molecule_rmsd_A(A, B, nslab) > BASIN_TOL["rmsd_A"]:
                    continue                              # 서술자는 같아도 구조가 멀면 다른 basin
            cl.append(r); placed = True; break
        if not placed:
            clusters.append([r])
    return clusters


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
        # ★ 자체 리뷰 #4 — 순서 규약(슬랩 원본 순서 + 분자 뒤)을 파일마다 검사한다.
        #   종별 재정렬된 POSCAR/CONTCAR(우리 _write_poscar 산출물 포함)가 들어오면
        #   슬랩/분자 절단이 어긋나 게이트 전부가 조용히 쓰레기를 낸다.
        sym_c = cx.get_chemical_symbols()
        if sym_c[:nslab] != slab.get_chemical_symbols():
            print(f"⛔ {f.name}: 앞 {nslab}개가 정본 슬랩 순서와 다르다 — 종별 정렬본은 직접 못 넣는다. "
                  "건너뜀 (판정 아님)")
            continue
        if Counter(sym_c[nslab:]) != Counter(mol_ref.get_chemical_symbols()):
            print(f"⛔ {f.name}: 분자부 조성 {dict(Counter(sym_c[nslab:]))} 이 기준 조각과 다르다 — "
                  "건너뜀 (판정 아님)")
            continue
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
        e = g.get("extraction") or {}
        if e.get("verdict") in ("EXTRACTION_CANDIDATE", "RECONSTRUCTION_REVIEW"):
            print(f"    {'⛔' if e.get('flag') else '⚠'} {e['verdict']}: 표면 최대변위 "
                  f"{e.get('max_surface_disp_A')} Å · z_top {e.get('z_top_shift_A', 0):+.3f} Å")
            print(f"       움직인 표면원자 {e.get('moved_surface_atoms')}")
            # (자체 리뷰 #6 — 옛 키 이름을 참조해 근거가 항상 None 으로 찍혔다)
            print(f"       기판 O 배위수 감소 {e.get('lost_substrate_O_coordination')}")
            if e.get("neighbor_swap_no_CN_loss"):
                print(f"       면내 hop(배위 유지) {e.get('neighbor_swap_no_CN_loss')}")
            print(f"       분자 접촉(증거만) {e.get('cation_near_molecule')}")
        for r in g["gate_reasons"]:
            print(f"    ⛔ {r}")
        for w in g["warnings"]:
            print(f"    ⚠ {w}")
    if a.json:
        Path(a.json).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
        print(f"\n→ {a.json}")
    return 0


def gate_version() -> str:
    """게이트 규약의 지문. **계산 지문과 분리한다.**

    이전에는 fingerprint 안에 GATE 를 넣었는데, 그러면 임계를 한 글자만 고쳐도 GPU 이완을
    전부 다시 돌아야 했다(2026-08-11 실제로 두 번 그랬다). 게이트는 저장된 이완 구조에
    **사후 적용**할 수 있는 후처리다 — 재계산 대상이 아니다.
    계산을 바꾸는 것(model·task·gap·fmax·steps·freeze·슬랩)만 fingerprint 에 넣는다.
    """
    return hashlib.sha256(json.dumps({"gates": GATE, "bonds": BOND_LIMITS,
                                      "basin": BASIN_TOL}, sort_keys=True).encode()).hexdigest()[:12]


def make_protocol(*, stage: str, model: str, task: str, atlas_gap: Any, atlas_ndir: Any,
                  fmax: float, steps: int, freeze_frac: Any) -> Dict[str, Any]:
    """계산 프로토콜 + 지문.

    ★ 2026-08-11 자체 리뷰 수정 — 이전 구현은 relax 단계에서 `dict(proto)` 를 통째로
      재해시했는데, proto 에는 이미 `gate_version`(과 옛 fingerprint)이 들어 있었다.
      게이트 임계를 한 글자만 고쳐도 relax 지문이 바뀌어 **GPU 이완이 전부 재실행**됐다 —
      게이트/계산 분리를 만들어 놓고 스스로 깨뜨린 셈이다.
      지금은 지문 입력을 **계산을 바꾸는 항목만** 담은 별도 dict 로 고정한다.
      (gap/ndir 는 atlas manifest 값을 쓴다 — 구조의 출처는 atlas 이지 score 플래그가 아니다.)
    ⚠ 지문 조리법이 바뀌었으므로 이 커밋 이전에 저장된 레코드는 재개 시 재계산된다(1회성)."""
    base = {"tool": "site_screen.py", "stage": stage, "model": model, "task": task,
            "atlas_gap_A": atlas_gap, "atlas_ndir": atlas_ndir,
            "fmax": fmax, "steps": steps, "freeze_frac": freeze_frac,
            "slab_sha256": SLAB["sha256"]}
    fp = hashlib.sha256(json.dumps(base, sort_keys=True).encode()).hexdigest()[:16]
    return {**base, "fingerprint": fp, "gate_version": gate_version()}


def _load_record(path: Path) -> Optional[Dict[str, Any]]:
    """죽은 런이 남긴 반쪽 JSON 은 '기록 없음'으로 취급한다 — 재개가 여기서 죽으면 안 된다."""
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def _atomic_json(path: Path, payload: Any) -> None:
    """임시 파일에 쓰고 rename — 도중에 죽어도 반쪽 파일이 본 이름을 차지하지 않는다."""
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    os.replace(tmp, path)


def _guard_gpu(allow_concurrent: bool = False, need_gib: float = 8.0) -> None:
    """gabia 규약 — **GPU 빌드** pw.x 와 UMA 동시 실행 금지 (VRAM 47/48 GB 점유 사례).

    ⛔⛔ 2026-08-29 — 종전 가드는 `pgrep -fa pw.x` 로 **아무 pw.x** 나 잡았다. 그래서
      VRAM 과 무관한 **CPU 빌드**(`qe-*-cpu/bin/pw.x`, 예: nscf_gap) 가 돌기만 해도
      UMA 가 막혔다. 실제 위험은 GPU 빌드뿐이다 — 경로로 가른다.

    `allow_concurrent=True` 는 **명시적 옵트인**이다 (1저자 승인 필요). 그때도
    남은 VRAM 이 `need_gib` 미만이면 막는다 — "OOM 나면 끄지" 는 계획이지 보장이 아니다.

    ⛔ 못 하는 것: 다른 사용자의 GPU 프로세스나 곧 늘어날 점유를 예측하지 못한다.
      여유는 **지금 이 순간**의 값이다.
    """
    try:
        import subprocess
        out = subprocess.run(["pgrep", "-fa", "pw.x"], capture_output=True, text=True).stdout.strip()
        gpu = [ln for ln in out.splitlines() if "-gpu/bin/pw.x" in ln]
        cpu = [ln for ln in out.splitlines() if "-cpu/bin/pw.x" in ln]
        if cpu and not gpu:
            print(f"  ⓘ CPU 빌드 pw.x {len(cpu)}개는 VRAM 을 쓰지 않는다 — 통과")
        if gpu:
            free = None
            try:
                q = subprocess.run(
                    ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                    capture_output=True, text=True).stdout.strip().splitlines()
                free = float(q[0]) / 1024.0
            except Exception:
                pass
            if not allow_concurrent:
                sys.exit("⛔ **GPU 빌드** pw.x 가 돌고 있다 — UMA 와 동시 실행 금지 (CLAUDE.md).\n"
                         + "\n".join(gpu)
                         + (f"\n   현재 VRAM 여유 {free:.1f} GiB." if free else "")
                         + "\n   승인이 있으면 --allow_concurrent_pwx 로 명시적으로 켜라.")
            if free is not None and free < need_gib:
                sys.exit(f"⛔ --allow_concurrent_pwx 를 줬으나 VRAM 여유가 {free:.1f} GiB "
                         f"< {need_gib} GiB 다. 지금 띄우면 OOM 이 거의 확실하다.")
            print(f"  ⚠ GPU pw.x 와 **동시 실행** (명시 승인). VRAM 여유 "
                  f"{free:.1f} GiB" if free is not None else "  ⚠ GPU pw.x 와 동시 실행 (명시 승인)")
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
    _guard_gpu(allow_concurrent=getattr(a, "allow_concurrent_pwx", False))
    from ase.optimize import FIRE
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator

    slab = load_slab()
    nslab = len(slab)
    out = Path(a.out)
    atlas = out / "atlas_manifest.json"
    if not atlas.is_file():
        sys.exit(f"⛔ {atlas} 가 없다 — atlas 를 먼저 돌릴 것")
    mft = json.loads(atlas.read_text())
    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit(a.model, device=a.device),
                              task_name=a.task)

    def proto_for(stage: str, ff: Any = None) -> Dict[str, Any]:
        return make_protocol(stage=stage, model=a.model, task=a.task,
                             atlas_gap=mft.get("gap_A"), atlas_ndir=mft.get("ndir"),
                             fmax=a.fmax, steps=a.steps, freeze_frac=ff)

    proto = proto_for(a.stage)
    print(f"프로토콜 {proto['fingerprint']} · {a.model}/{a.task} · stage={a.stage} "
          f"· freeze={getattr(a, 'freeze', None)} · gate {proto['gate_version']}")
    clean_cache: Dict[float, Any] = {}      # freeze → (e_slab, clean, cons, nfix, zcut) — 조각과 무관

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
        if info["status"] != "OK":
            sys.exit(f"⛔ {frag}: 입력이 선언과 다르다 ({info['status']}) — 중단. {info}")
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
            _atomic_json(sdir / "_references.json",
                         {"E_slab_eV": e_slab, "E_mol_eV": e_mol, "protocol": proto,
                          "note": "E_mol 은 ORCA 기하 그대로의 UMA SP — 조각 안에서 상수라 순위에서 상쇄된다."})
            done = 0
            for i, r in enumerate(rows, 1):
                jf = sdir / f"{r['label']}.json"
                rec = _load_record(jf)
                if rec and rec.get("fingerprint") == proto["fingerprint"]:
                    done += 1; continue
                # ★ 자체 리뷰 수정 — 예전엔 score 시점의 --gap/--ndir 로 자세를 **다시 생성**했다.
                #   atlas 와 플래그가 어긋나면 게이트를 통과한 적 없는 기하를 조용히 채점하고,
                #   relax 는 저장본을 읽어 rigid 와 다른 구조에서 출발했다. 이제 저장된
                #   atlas 구조만 읽는다 — 구조의 정본은 atlas 산출물이다.
                xyz = fdir / f"{r['label']}.xyz"
                if not xyz.is_file():
                    sys.exit(f"⛔ {xyz} 가 없다 — atlas 를 --dry-run 으로 돌렸다면 구조 없이 "
                             "rigid 를 돌 수 없다. atlas 를 --dry-run 없이 다시 돌릴 것.")
                cx = read(xyz)
                cx.set_cell(slab.cell.array); cx.set_pbc(True)
                e = sp(cx)
                _atomic_json(jf, {**r, "E_complex_eV": e, "E_slab_eV": e_slab,
                                  "E_mol_eV": e_mol, "E_pose_eV": e - e_slab - e_mol,
                                  "fingerprint": proto["fingerprint"], "protocol": proto})
                if i % 25 == 0:
                    print(f"  [{frag} rigid {i}/{len(rows)}]", flush=True)
            print(f"■ {frag} rigid 완료 (건너뜀 {done}/{len(rows)}) → {sdir}")
            continue

        # ── relax ──────────────────────────────────────────────────────────────
        # ★★ P0 (2026-08-11 Codex 교차검증) — 에너지 캐시와 **게이트 판정**이 같은 rigid JSON 에
        #   묶여 있는데 계산 지문에서 gate 를 뺐다. 그래서 게이트를 고쳐도 rigid JSON 은
        #   skip 되고, 그 안의 **옛 ranking_eligible** 이 shortlist 로 재진입했다.
        #   → 판정은 **현재 atlas row** 에서 다시 가져오고, rigid 에서는 **에너지만** 재사용한다.
        cur = {r["label"]: r for r in rows}      # rows = 지금 게이트로 eligible 한 것만
        rigid, stale, orphan = [], 0, 0
        for p in sorted((fdir / "rigid").glob("*.json")):
            if p.name.startswith("_"):
                continue
            rec = _load_record(p)
            if not isinstance(rec, dict) or rec.get("E_pose_eV") is None:
                orphan += 1; continue
            lab = rec.get("label")
            if lab not in cur:                   # 현재 게이트에서 탈락했거나 아틀라스에 없다
                stale += 1; continue
            rigid.append({**cur[lab],            # 판정은 현재 것
                          "E_pose_eV": rec["E_pose_eV"],
                          "E_complex_eV": rec.get("E_complex_eV"),
                          "energy_fingerprint": rec.get("fingerprint")})
        if not rigid:
            print(f"⛔ {frag}: 현재 게이트에서 살아남은 rigid 레코드가 없다 — rigid 먼저"); continue
        if stale or orphan:
            print(f"  ※ {frag}: rigid 캐시 중 현재 게이트 탈락 {stale}개 · 에너지 없음 {orphan}개 제외 "
                  f"(에너지만 재사용하고 판정은 현재 atlas 기준)")
        short = shortlist_with_matched_pairs(rigid, a.top_per_site, a.pairs)
        for ff in a.freeze:
            pr = proto_for(a.stage, ff)          # 계산 항목만 해시 — 게이트는 안 들어간다
            sdir = fdir / f"relax_f{ff:.2f}"; sdir.mkdir(parents=True, exist_ok=True)
            # 깨끗한 슬랩은 (슬랩, freeze) 에만 의존한다 — 조각마다 다시 이완하면 GPU 낭비 (자체 리뷰 #8)
            if ff not in clean_cache:
                cons, nfix, zcut = _freeze_mask(nslab, slab, ff)
                cs = slab.copy(); cs.set_constraint(cons); cs.calc = calc
                if ff < 1.0:
                    FIRE(cs, logfile=str(out / f"_clean_f{ff:.2f}.log")).run(fmax=a.fmax, steps=a.steps)
                e_cs = float(cs.get_potential_energy())
                cl = cs.copy(); cl.set_constraint()
                clean_cache[ff] = (e_cs, cl, cons, nfix, zcut)
            e_slab, clean, cons, nfix, zcut = clean_cache[ff]
            write(sdir / "_clean_slab.vasp", clean, format="vasp", direct=True)
            _atomic_json(sdir / "_references.json",
                         {"E_slab_eV": e_slab, "E_mol_eV": e_mol, "freeze_frac": ff,
                          "n_fixed": nfix, "z_cut_A": round(zcut, 3), "protocol": pr})
            # watch 가 목표치를 추측하지 않도록 이완 대상 명단을 그대로 남긴다 (자체 리뷰 #9)
            _atomic_json(sdir / "_shortlist.json", [r["label"] for r in short])
            print(f"■ {frag} relax freeze={ff} (고정 {nfix}/{nslab}, z≤{zcut:.2f} Å) · 대상 {len(short)}")
            for i, r in enumerate(short, 1):
                jf = sdir / f"{r['label']}.json"
                rec = _load_record(jf)               # 반쪽 JSON 은 '없음'으로 — 재개가 죽으면 안 된다
                if rec and rec.get("fingerprint") == pr["fingerprint"]:
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
                # ⚠ 고정 인덱스는 z 기준이라 **연속이 아니다** (1×4 초격자는 층이 뒤섞여 있다).
                #   positions[:nfix] 로 재면 '자유롭게 움직여야 하는 원자'를 재게 되고,
                #   freeze 0.85 자세가 전부 FROZEN_DRIFT 로 오탈락한다 (2026-08-11 Codex 지적, 실측 확인).
                fixed_idx = np.asarray(cons.index, dtype=int)
                drift = (float(np.abs(fin.positions[fixed_idx] - slab.positions[fixed_idx]).max())
                         if fixed_idx.size else 0.0)
                g = apply_gates(fin, nslab, mol, frag, clean=clean, relaxed=True, bonds=bonds)
                if drift > GATE["frozen_drift_A"]:
                    g["gate_reasons"].append(f"FROZEN_DRIFT({drift:.4f}Å)"); g["ranking_eligible"] = False
                if not converged:
                    g["gate_reasons"].append(f"NOT_CONVERGED(steps>{a.steps})"); g["ranking_eligible"] = False
                write(sdir / f"{r['label']}.xyz", fin)
                _atomic_json(jf, {**r, "freeze_frac": ff, "converged": converged,
                                  "frozen_drift_A": drift, "E_complex_eV": e,
                                  "E_slab_eV": e_slab, "E_mol_eV": e_mol,
                                  "E_pose_eV": e - e_slab - e_mol,
                                  **{k: v for k, v in g.items() if k != "bond"},
                                  "bond_changes": g["bond"]["n_changes"],
                                  "fingerprint": pr["fingerprint"], "protocol": pr})
                print(f"  [{i}/{len(short)}] {r['label']} E_pose {e - e_slab - e_mol:+.3f} eV "
                      f"{'✔' if g['ranking_eligible'] else '⛔ ' + ','.join(x.split('(')[0] for x in g['gate_reasons'])}",
                      flush=True)
    return 0


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
            # ★ 2026-08-11 (Codex Round-3, 채택) — `min(E_Li, E_Ni)` 로 정렬하면 **한쪽 끝점만
            #   매우 깊은 쌍**이 먼저 뽑힌다. DFT handoff 에서만 고쳤는데, relax 에 보낼
            #   방향부터 이미 편향돼 있었다. 여기서는 **쌍 균형 순위**로 고른다:
            #   두 끝점의 (자리 안 순위) 중 나쁜 쪽 = max — 양쪽 다 괜찮은 쌍이 먼저 온다.
            pairs.append((d, ro, r, q))
    # 자리별 순위(0 = 그 자리에서 가장 깊음)를 만든 뒤 쌍의 대표 순위를 max 로 잡는다
    rank: Dict[str, int] = {}
    for s in ("Li_top", "Ni_top"):
        v = sorted([r for r in ok if r["site"] == s], key=lambda x: x["E_pose_eV"])
        for k, r in enumerate(v):
            rank[r["label"]] = k
    # ★ 방향 quota — roll 변형은 독립 표본이 아니다. 같은 down_dir 에서 최대 1쌍만 먼저 채우고,
    #   방향을 다 쓰면 그때 두 번째 roll 을 채운다 (Codex: direction-level 집계 요구).
    pairs.sort(key=lambda t: max(rank.get(t[2]["label"], 1 << 20), rank.get(t[3]["label"], 1 << 20)))
    chosen, used_dir = [], set()
    for d, ro, r, q in pairs:
        if d in used_dir:
            continue
        chosen.append((d, ro, r, q)); used_dir.add(d)
        if len(chosen) >= n_pairs:
            break
    for d, ro, r, q in pairs:                     # 방향을 다 썼으면 남은 자리를 채운다
        if len(chosen) >= n_pairs:
            break
        if (d, ro) not in {(x[0], x[1]) for x in chosen}:
            chosen.append((d, ro, r, q))
    for d, ro, r, q in chosen:
        picked[r["label"]] = r
        picked[q["label"]] = q
    by_site = defaultdict(list)
    for r in ok:
        by_site[r["site"]].append(r)
    for s, v in by_site.items():
        for r in sorted(v, key=lambda x: x["E_pose_eV"])[:top_per_site]:
            picked[r["label"]] = r
    return sorted(picked.values(), key=lambda r: (r["site"], r["E_pose_eV"]))



# ══ basin 중복제거 + calibration/audit 선정 (회신 W 절차 2~4) ═══════════════
#: 접촉으로 셀 원자쌍의 상한 거리 [Å]. `min_contact_pair` **하나**가 아니라
#:   이 안의 **전체 접촉 graph** 를 지문으로 쓴다 (회신 W 2단계).
BASIN_CONTACT_CUT = 3.2
#: 같은 basin 으로 묶는 무거운원자 RMSD 상한 [Å] (PBC 최소이미지, 슬랩 프레임 고정)
BASIN_RMSD_TOL = 0.75
#: 분자 높이 차 상한 [Å]
BASIN_HEIGHT_TOL = 0.40
#: 초기 scheduling shell [eV] — **coverage 규칙이 아니다** (회신 W Q3).
#:   최종 창은 W = max(W0, B + TAU) 로 calibration 뒤에 정한다.
BASIN_W0_EV = 0.15
BASIN_TAU_EV = 0.04


def _mol_slab_split(at, nslab):
    return list(range(nslab)), list(range(nslab, len(at)))


def basin_descriptor(at, nslab, cut=BASIN_CONTACT_CUT):
    """이완 최종 구조 → basin 서술자.

    → dict(fingerprint, anchor, height_A, tilt_deg, heavy_xyz)

    ⛔ 못 하는 것: 슬랩 공간군 대칭으로 **등가 자세를 접지 않는다** (병진만 PBC 로
      처리한다). 대칭으로 같은 자세가 서로 다른 basin 으로 남을 수 있다 — 그건
      과다분할이라 **보수적** 이지만, 예산을 낭비한다.
    """
    import numpy as np
    sym = at.get_chemical_symbols()
    sl, mo = _mol_slab_split(at, nslab)
    D = at.get_all_distances(mic=True)
    sub = D[np.ix_(mo, sl)]
    # 접촉 graph — cut 안의 (분자원소, 슬랩원소) 쌍을 전부 센다
    from collections import Counter
    c = Counter()
    for i in range(len(mo)):
        for j in range(len(sl)):
            if sub[i, j] <= cut:
                c[(sym[mo[i]], sym[sl[j]])] += 1
    # ⛔⛔ 2026-08-29 — 초판은 `(원소쌍, **개수 정확값**)` 이라 3.2 Å 안 원자수가 ±1 만
    #   달라도 다른 지문이 됐다. 실측에서 자세 109 → basin 103 (6개만 병합) 으로
    #   **중복제거가 사실상 작동하지 않았다.** 개수는 거친 구간(1 / 2-3 / 4-6 / 7+)으로
    #   접고, 물리적으로 뜻이 있는 **어느 원소쌍이 닿았나** 를 지문의 중심에 둔다.
    def _bin(n):
        return 1 if n <= 1 else (2 if n <= 3 else (3 if n <= 6 else 4))
    fp = tuple(sorted((k[0], k[1], _bin(v)) for k, v in c.items()))
    i, j = divmod(int(sub.argmin()), sub.shape[1])
    anchor = (sym[mo[i]], sym[sl[j]], round(float(sub[i, j]), 3))
    z = at.positions[:, 2]
    height = float(np.mean(z[mo]) - np.max(z[sl]))
    heavy = [k for k in mo if sym[k] != "H"]
    hx = at.positions[heavy]
    # tilt — 분자 주축과 표면법선 사이 각
    q = hx - hx.mean(0)
    try:
        ax = np.linalg.svd(q, full_matrices=False)[2][0]
        tilt = float(np.degrees(np.arccos(abs(ax[2]))))
    except Exception:
        tilt = float("nan")
    return {"fingerprint": fp, "anchor": anchor, "height_A": round(height, 3),
            "tilt_deg": round(tilt, 1), "heavy_xyz": hx, "n_heavy": len(heavy)}


def _pbc_rmsd(a, b, cell):
    """무거운원자 RMSD (최소이미지). 슬랩 프레임이 같으므로 회전맞춤은 안 한다."""
    import numpy as np
    if a.shape != b.shape:
        return float("inf")
    d = a - b
    f = np.linalg.solve(np.array(cell).T, d.T).T
    f -= np.round(f)
    d = f @ np.array(cell)
    return float(np.sqrt((d ** 2).sum(1).mean()))


def dedup_basins(poses, rmsd_tol=BASIN_RMSD_TOL, height_tol=BASIN_HEIGHT_TOL):
    """(라벨, E, 서술자, cell) 목록 → basin 묶음. 에너지 낮은 자세가 대표.

    같은 basin 조건: **접촉지문 동일 AND 높이차 < tol AND RMSD < tol**.
    ⛔ 못 하는 것: 대칭 등가를 안 접는다 (위 docstring 참조).
    """
    order = sorted(poses, key=lambda x: x[1])
    basins = []
    for lab, e, desc, cell in order:
        hit = None
        for b in basins:
            if b["fingerprint"] != desc["fingerprint"]:
                continue
            if abs(b["height_A"] - desc["height_A"]) > height_tol:
                continue
            if _pbc_rmsd(b["_xyz"], desc["heavy_xyz"], cell) > rmsd_tol:
                continue
            hit = b
            break
        if hit is None:
            basins.append({"basin_id": "b%02d" % len(basins), "rep_label": lab,
                           "E_pose_eV": round(e, 6), "fingerprint": desc["fingerprint"],
                           "anchor": desc["anchor"], "height_A": desc["height_A"],
                           "tilt_deg": desc["tilt_deg"], "members": [lab],
                           "_xyz": desc["heavy_xyz"]})
        else:
            hit["members"].append(lab)
    for b in basins:
        b.pop("_xyz", None)
        b["n_members"] = len(b["members"])
    return basins


def cmd_basins(a):
    """basin 중복제거 → calibration 4 + sealed audit 2 를 **DFT 전에** 고른다."""
    import glob
    import hashlib
    import json
    import os
    import random
    from ase.io import read

    out = {"schema": "prospective_basins/v1", "date": a.date,
           "params": {"contact_cut_A": BASIN_CONTACT_CUT, "rmsd_tol_A": BASIN_RMSD_TOL,
                      "height_tol_A": BASIN_HEIGHT_TOL, "W0_eV": BASIN_W0_EV,
                      "tau_eV": BASIN_TAU_EV, "audit_seed": a.seed},
           "⚠": ("이 문서는 **DFT 를 보기 전에** 만든다. calibration 은 값을 보고 고르고, "
                 "sealed audit 은 그 밖에서 고른다 — audit 를 보고 모델/창을 고치면 "
                 "그것은 더 이상 holdout 이 아니다 (회신 W 4단계)."),
           "fragments": {}}
    for frag in a.frag:
        D = os.path.join(a.out, frag, "relax_f%.2f" % a.freeze)
        ref = json.load(open(os.path.join(D, "_references.json")))
        poses = []
        gated = []
        for f in sorted(glob.glob(os.path.join(D, "*.json"))):
            lab = os.path.basename(f)[:-5]
            if lab.startswith("_"):
                continue
            d = json.load(open(f))
            g = d.get("gate_reasons") or d.get("gates") or []
            e = d.get("E_pose_eV")
            if e is None and "E_complex_eV" in d:
                e = d["E_complex_eV"] - ref["E_slab_eV"] - ref["E_mol_eV"]
            if e is None:
                continue
            if g:
                gated.append({"label": lab, "E_pose_eV": round(e, 6), "gates": g})
                continue
            xp = os.path.join(D, lab + ".xyz")
            if not os.path.isfile(xp):
                sys.exit("⛔ %s 의 최종 구조가 없다 — basin 을 만들 수 없다" % lab)
            at = read(xp)
            poses.append((lab, e, basin_descriptor(at, a.nslab), at.get_cell()[:]))
        if not poses:
            sys.exit("⛔ %s: 게이트 통과 자세가 없다" % frag)
        basins = dedup_basins(poses)
        emin = basins[0]["E_pose_eV"]
        inside = [b for b in basins if b["E_pose_eV"] - emin <= BASIN_W0_EV]
        outside = [b for b in basins if b["E_pose_eV"] - emin > BASIN_W0_EV]

        # calibration 4 (회신 W 3단계)
        cal, seen = [], set()

        def take(b, why):
            if b and b["basin_id"] not in seen:
                seen.add(b["basin_id"])
                cal.append({**{k: v for k, v in b.items() if k != "members"},
                            "role": "calibration", "why": why})
        take(basins[0], "UMA global-min basin")
        take(next((b for b in basins[1:]
                   if b["fingerprint"] != basins[0]["fingerprint"]), None),
             "다른 접촉지문 중 최저")
        take(inside[-1] if inside else None, "provisional 창 W0 안쪽 경계")
        take(outside[0] if outside else None, "W0 바깥 최근접")

        # sealed audit 2 (회신 W 4단계) — 선택집합 **밖**에서, seed 를 먼저 기록
        # ⛔⛔ 2026-08-29 — 초판은 `pool[0]`(선택 안 된 것 중 **최저**)을 집어
        #   "창 바깥 최근접" 이라 라벨했다. 실측에서 그것이 W0 **안쪽**이었다
        #   (sdcp +0.0765 vs 창 ~+0.17). 회신 W 4단계가 못박은 금지사항이다 —
        #   **창 안에서 하나를 빼 holdout 이라 부르면 안 된다.**
        pool_out = [b for b in outside if b["basin_id"] not in seen]
        pool_in = [b for b in inside if b["basin_id"] not in seen]
        aud = []
        if pool_out:
            aud.append({**{k: v for k, v in pool_out[0].items() if k != "members"},
                        "role": "sealed_audit",
                        "why": "W0 **바깥** 최근접 excluded (calibration 다음)"})
        else:
            out.setdefault("warnings", []).append(
                "%s: W0 바깥에 남은 basin 이 없다 — audit#1 을 만들 수 없다" % frag)
        rest = [b for b in (pool_out + pool_in)
                if b["basin_id"] != (aud[0]["basin_id"] if aud else None)]
        if rest:
            # 접촉지문 층화 난수 — seed 를 params 에 박아 뒀다
            rng = random.Random(a.seed)
            strata = {}
            for b in rest:
                strata.setdefault(b["fingerprint"], []).append(b)
            key = rng.choice(sorted(strata, key=str))
            pick = rng.choice(strata[key])
            # 층화 난수는 제외 풀 전체에서 뽑는다 (창 안팎 모두) — 회신 W 는
            # "나머지 제외 풀에서 접촉지문 층화 난수" 라고만 했다.
            aud.append({**{k: v for k, v in pick.items() if k != "members"},
                        "role": "sealed_audit", "why": "접촉지문 층화 난수 (seed %d)" % a.seed})
        out["fragments"][frag] = {
            "n_poses_passed": len(poses), "n_gated": len(gated),
            "n_basins": len(basins), "E_min_eV": emin,
            "gated": gated,
            "basins": [{k: v for k, v in b.items() if k != "members"} for b in basins],
            "basin_members": {b["basin_id"]: b["members"] for b in basins},
            "calibration": cal, "sealed_audit": aud}
        print("■ %s: 자세 %d(게이트 %d) → **basin %d** · 최저 %+.4f eV"
              % (frag, len(poses), len(gated), len(basins), emin))
        for b in cal:
            print("   cal   %s %+.4f  %-46s %s"
                  % (b["basin_id"], b["E_pose_eV"], b["rep_label"][:46], b["why"]))
        for b in aud:
            print("   AUDIT %s %+.4f  %-46s %s"
                  % (b["basin_id"], b["E_pose_eV"], b["rep_label"][:46], b["why"]))

    body = json.dumps(out, ensure_ascii=False, sort_keys=True, default=str)
    out["freeze_sha256"] = hashlib.sha256(body.encode()).hexdigest()
    json.dump(out, open(a.save, "w"), ensure_ascii=False, indent=1, default=str)
    print("\n→ %s  (freeze %s)" % (a.save, out["freeze_sha256"][:16]))
    print("⛔ 이 파일을 DFT 전에 커밋해 동결하라 — audit 를 보고 고치면 holdout 이 아니다")
    return 0


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
    # ⚠ Round-2 지적 (채택): 경고만 하고 계속 계산하면 서로 다른 프로토콜이 한 표에 섞인다.
    #   pair key 에도 freeze·지문이 없어서 같은 (site, dir, roll) 행이 덮어써졌다. 이제 막는다.
    fz = sorted({r.get("freeze_frac") for r in rows if r.get("freeze_frac") is not None})
    fp = sorted({r.get("fingerprint") for r in rows if r.get("fingerprint")})
    if len(fz) > 1 or len(fp) > 1:
        sys.exit(f"⛔ 프로토콜이 섞였다 — freeze {fz} · 지문 {fp}\n"
                 "   서로 다른 구속·게이트로 낸 값을 한 표에 놓을 수 없다. 하나씩 따로 돌릴 것.")
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
        # basin 클러스터링 — 자세 n개가 실제로 몇 개의 골짜기인가
        sdir = Path(a.rows[0]) if Path(a.rows[0]).is_dir() else None
        cls = cluster_basins(fs, struct_dir=sdir)
        print(f"   basin: 자세 {len(fs)} → **구별되는 골짜기 {len(cls)}개** "
              f"(크기 {sorted((len(c) for c in cls), reverse=True)[:8]}…)"
              + ("  [주기 RMSD 포함]" if sdir else "  [서술자만 — 구조 없음]"))
        if len(cls) < max(3, len(fs) // 20):
            print("     ⚠ 골짜기가 매우 적다 — 자세를 많이 만들어도 **같은 곳으로 굴러가고 있다.**")
        print("     ※ 자동 basin 라벨은 진단용 proxy — 대칭 등가를 다르게 세거나 다른 것을 합칠 수 있다.")

        by_site = defaultdict(list)
        for r in fs:
            by_site[r.get("site_from_geometry") or r["site"]].append(r)
        # E_pose = E_complex − E_slab − E_mol(ORCA 기하). 분자가 표면에서 이완하면 **변형 몫**이
        # 같이 들어간다 — 유연한 분자(SDCP)는 그게 커서 부호가 양수로 뒤집힐 수 있다.
        # 같은 조각 안 순위에는 무해하지만(E_mol 이 상수), **부호를 '결합 안 됨'으로 읽으면 안 된다.**
        lo = min(r["E_pose_eV"] for r in fs)
        if lo > 0:
            # ★ 2026-08-11 정정 (Round-2 지적) — 앞서 "변형 몫은 상쇄돼 무해하다"고 적었는데 틀렸다.
            #   상쇄되는 건 상수인 E_mol·E_slab 기준뿐이고, **변형 에너지는 자세마다 달라
            #   E_complex 안에 남는다.** 그리고 그건 오염이 아니라 흡착 안정성의 일부다.
            print(f"   ⚠ E_pose 최저가 양수({lo:+.3f}) — 기준상태(고정 슬랩 + 기체상 ORCA 기하 분자)")
            print(f"     대비 불리하다는 뜻이지 **국소 상호작용이 없다는 뜻이 아니다.**")
            print(f"     E_ads = E_interaction + E_deform(분자) + E_deform(표면) 이고, 변형 몫은"
                  f" **자세마다 달라 상쇄되지 않는다** — 순위의 일부다.")
            print(f"     분해하려면 이완된 조각·슬랩을 각각 따로 재야 한다(현재 안 함).")
        print(f"   {'자리':16s} {'n':>4s} {'최저':>9s} {'중앙값':>9s} {'폭':>8s}")
        for s in sorted(by_site, key=lambda s: min(x["E_pose_eV"] for x in by_site[s])):
            E = sorted(x["E_pose_eV"] for x in by_site[s])
            print(f"   {s:16s} {len(E):4d} {E[0]:+9.3f} {E[len(E)//2]:+9.3f} {E[-1]-E[0]:8.3f}")
        # 검열 회계 — 사유별 · **양이온별** · 그리고 '검열이 순위를 왜곡했나'
        killed = [r for r in fr if not r.get("ranking_eligible")]
        confounded = False
        if killed:
            by_reason = Counter((r.get("gate_reasons") or ["?"])[0].split("(")[0] for r in killed)
            print("   검열(게이트로 죽은 자세) — '졌다'가 아니라 '못 쟀다':")
            for why, n in by_reason.most_common():
                sub = [r for r in killed if (r.get("gate_reasons") or ["?"])[0].startswith(why)]
                cat = Counter(r.get("nearest_cation") for r in sub)
                es = sorted(r["E_pose_eV"] for r in sub if r.get("E_pose_eV") is not None)
                emin = f"{es[0]:+.3f}" if es else "—"
                print(f"     {why:28s} {n:3d}  최근접양이온 {dict(cat)}  최저 {emin}")

            # ★ 결정적 검사 — 검열된 자세가 살아남은 최저보다 낮으면 비교가 통째로 오염된다.
            surv_min = {c: min((r["E_pose_eV"] for r in fs if r.get("nearest_cation") == c),
                               default=None) for c in CATIONS}
            print("   ▸ 검열이 순위를 왜곡했나 (검열된 자세 중 '살아남은 최저'보다 낮은 것):")
            for c in CATIONS:
                lo = surv_min[c]
                sub = [r for r in killed if r.get("nearest_cation") == c
                       and r.get("E_pose_eV") is not None]
                if lo is None:
                    print(f"     {c}: 살아남은 자세가 없다 — 이 양이온은 **비교 불가**")
                    confounded = True
                    continue
                below = sorted(r["E_pose_eV"] for r in sub if r["E_pose_eV"] < lo)
                mark = "⛔" if below else "·"
                print(f"     {mark} {c}: 검열 {len(sub):3d}개 중 살아남은 최저({lo:+.3f})보다 낮은 것 "
                      f"**{len(below)}개**" + (f" (최저 {below[0]:+.3f})" if below else ""))
                confounded |= bool(below)
            if confounded:
                print("     ⛔ **검열이 한쪽 양이온의 강한 자세를 잘라냈다** — 아래 분포 비교는")
                print("        자리 선호가 아니라 '어느 쪽이 더 많이 검열됐나'를 재고 있을 수 있다.")
                print("        검열 사유가 물리적으로 정당해도(예: Li 추출) **비교의 근거는 되지 못한다** —")
                print("        같은 자세로 짝지은 대조쌍으로만 판정할 것.")
        # 대조쌍 — 시작 자리로 짝짓되, **최종 registry 로 자격을 검사**한다.
        #   Li 시작이 Ni 접촉으로 끝나거나(이주), 두 끝점이 같은 자리로 합쳐지면(붕괴)
        #   그 쌍의 ΔE 는 '자리 차'가 아니다. 내지 않는다. (Round-2 지적, 채택)
        pairs, bad_pairs = [], []
        idx = {(r["site"], r["down_dir"], r["roll_deg"], r.get("freeze_frac"),
                r.get("fingerprint")): r for r in fs}
        for key, r in idx.items():
            s, d, ro, ff, fp = key
            if s != "Li_top":
                continue
            q = idx.get(("Ni_top", d, ro, ff, fp))
            if not q:
                continue
            lc, nc = r.get("nearest_cation"), q.get("nearest_cation")
            if lc is None or nc is None:
                bad_pairs.append((d, ro, "NO_CATION_CONTACT", lc, nc)); continue
            if lc == nc:
                bad_pairs.append((d, ro, "PAIR_SITE_COLLAPSED", lc, nc)); continue
            if lc != "Li" or nc != "Ni":
                bad_pairs.append((d, ro, "PAIR_MIGRATED", lc, nc)); continue
            pairs.append((d, ro, r["E_pose_eV"], q["E_pose_eV"], q["E_pose_eV"] - r["E_pose_eV"]))
        if bad_pairs:
            print(f"   ⛔ 자격 미달 대조쌍 {len(bad_pairs)}개 — ΔE 를 내지 않는다:")
            for d, ro, why, lc, nc in bad_pairs[:8]:
                print(f"      {why:22s} {d}/r{int(ro):03d} · Li시작→{lc} · Ni시작→{nc}")
        if pairs:
            # ★ Codex Round-3 (채택) — roll 변형은 독립 표본이 아니다. **방향 단위로 먼저
            #   접고**, 그 방향 중앙값들로 판정한다. 쌍 개수로 통계를 내면 같은 방향을
            #   n 번 센 셈이 된다 (sdcp_doped f0.85 가 정확히 그 경우였다: 3쌍 = 1방향).
            by_dir: Dict[str, List[float]] = defaultdict(list)
            for d, ro, _el, _en, de in pairs:
                by_dir[d].append(de)
            dir_med = {d: float(np.median(v)) for d, v in by_dir.items()}
            dl = sorted(dir_med.values())          # ← 판정 입력을 방향 중앙값으로 바꾼다
            print(f"   자격 있는 대조쌍 {len(pairs)}개 · **독립 방향 {len(by_dir)}개** "
                  f"(roll 변형은 한 표본으로 접음)")
            for d in sorted(by_dir, key=lambda k: dir_med[k]):
                n = len(by_dir[d])
                print(f"     {d:8s} ΔE {dir_med[d]:+.3f}" + (f"  (roll {n}개 중앙값)" if n > 1 else ""))
            if len(by_dir) == 1:
                print("     ⛔ **독립 방향이 1개다** — 이 조각의 자리 비교는 분자 방향 하나에 "
                      "얹혀 있다. 표본 1개짜리로 읽을 것(중앙값·편차 모두 의미 없음).")
            elif len(by_dir) < 3:
                print(f"     ⚠ 독립 방향 {len(by_dir)}개 — 방향 의존성을 가릴 표본이 부족하다.")
            # ΔE 산포가 **어느 쪽에서** 오는지 — 중앙값 비교는 이 비대칭을 지운다
            li_e = [p[2] for p in pairs]; ni_e = [p[3] for p in pairs]
            sl, sn = max(li_e) - min(li_e), max(ni_e) - min(ni_e)
            print(f"     Li 끝점 폭 {sl:.3f} eV · Ni 끝점 폭 {sn:.3f} eV")
            if max(sl, sn) > 3 * max(min(sl, sn), 1e-3):
                side = "Ni" if sn > sl else "Li"
                print(f"     ⚠ ΔE 산포가 거의 전부 **{side} 쪽**에서 온다 — "
                      f"{'Li' if side == 'Ni' else 'Ni'} 접촉은 방향에 둔감하고 "
                      f"{side} 접촉만 방향 민감하다는 뜻이다. 한쪽만 대표로 재는 셈이 아닌지 볼 것")
            # 방향 다양성 — 같은 down_dir 의 roll 변형만 남으면 '쌍 n개' 가 과대평가다
            dirs = {p[0] for p in pairs}
            if len(dirs) == 1 and len(pairs) > 1:
                print(f"     ⚠ 자격쌍 {len(pairs)}개가 **전부 같은 방향({next(iter(dirs))})의 roll 변형**이다 "
                      f"— 독립 표본 {len(dirs)}개짜리로 읽을 것")
            print(f"   Li_top↔Ni_top 짝지은 대조쌍 {len(pairs)}개 · "
                  f"ΔE(Ni−Li) 중앙값 {np.median(dl):+.3f} eV · 범위 {min(dl):+.3f}…{max(dl):+.3f}")
            # ⛔⛔ 2026-08-11 자체검토 P0 — **σ=0 이면 MARGINAL 가드가 통째로 무력화된다.**
            #   se_med 가 0 이 되어 `margin < se_med` 가 항상 거짓 → 곧바로 판정으로 간다.
            #   재현: dl=[0.031,0.031,0.031] → 마진 +1 meV 인데 "Li 우세" — **이 커밋이
            #   막으려던 바로 그 1 meV 판정**이다. 방향이 1개인 경우도 실제 데이터에 있다
            #   (sdcp_doped f0.85 는 자격쌍 3개가 전부 fib07 = 방향 1개).
            #   → 표본 하드게이트를 **판정보다 먼저** 둔다. 크기든 부호든 n<3 이면 검정 불가다.
            if len(dl) < 3:
                print(f"   ⛔ **판정 불가 — 독립 방향 {len(dl)}개** (3 미만). 크기도 부호도 "
                      f"검정할 수 없다. 중앙값 {float(np.median(dl)):+.3f} eV 는 참고값일 뿐이다.")
                print(f"     해소: atlas --ndir 를 늘려 독립 방향을 확보할 것.")
                continue
            # ⚠ ddof=1 (표본 표준편차). ddof=0 은 n=3~6 에서 se_med 를 최대 22% 과소평가해
            #   **가드가 필요한 작은 표본에서 정확히 약해진다** (자체검토 실측).
            sd = float(np.std(dl, ddof=1))
            floor = max(GATE["decision_floor_eV"], sd)
            med = float(np.median(dl))
            # ★★ 2026-08-11 — 바닥을 **얼마나** 넘었는지를 안 보던 게 구멍이었다.
            #   ptfe_c10 f0.85 가 중앙값 +0.031 vs 바닥 0.030 = **마진 1 meV** 로
            #   "Li 우세" 판정을 받았다. 1 meV 는 UMA 로도 우리 표본으로도 잰 적 없는 양이다.
            #   기준: 중앙값 자체의 불확실도(중앙값 표준오차 ≈ 1.25·σ/√n)보다 마진이
            #   작으면 **넘은 게 아니다**. 임계값 근처에서 반올림으로 갈리는 판정을 막는다.
            n_dir = len(dl)
            # ⚠ 1.2533·σ/√n 은 **정규분포 중앙값의 점근** 표준오차다. n=3~6 에서는:
            #   · 정규면 5~15% 보수적(무해)
            #   · **이봉이면 참값의 0.54배** — 방향에 따라 부호가 갈리는 바로 그 경우에
            #     가드가 가장 약해진다. 그래서 하한을 깐다.
            #   부트스트랩은 대안이 아니다 (n=5 면 재표본 중앙값이 4~5개 값밖에 안 나온다).
            se_med = max(0.005, 1.2533 * sd / max(1.0, n_dir ** 0.5))
            margin = abs(med) - floor
            # 순서통계 CI — 분포무관·소표본 정확. n=3 은 90% CI 가 **원리적으로 불가능**하다
            #   (극단 2개를 써도 커버리지 75%). 그 사실 자체가 se_med 숫자보다 방어력이 크다.
            ci_lo, ci_hi = float(min(dl)), float(max(dl))
            ci_cov = 1.0 - 2.0 * 0.5 ** n_dir      # [x(1), x(n)] 의 정확 커버리지
            # 부호 일관성 — 크기와 별개의 증거다. 크기는 작아도 방향이 다 같으면 실재를 시사하고,
            # 크기가 커도 부호가 갈리면 방향 하나에 얹힌 것이다. 둘을 같이 보고한다.
            # ⚠ 동점(정확히 0)은 부호검정에서 **버리고 n 을 줄이는** 게 표준이다.
            #   dl 은 방향 중앙값이라 짝수 roll 의 대칭 조합에서 0.000 이 나올 수 있는데,
            #   옛 코드는 `x > 0` 이라 그걸 음수로 셌다.
            npos = sum(1 for x in dl if x > 0)
            nneg = sum(1 for x in dl if x < 0)
            n_eff = npos + nneg
            try:
                k = max(npos, nneg)
                # ⚠ npos = n/2 (짝수 n)에서 raw 가 1 을 넘는 건 정상이다 — '작은 꼬리를 2배'
                #   관례에서 중앙값이 양쪽 꼬리에 중복 계산된다. 정확 p 는 그때 1.0 이다.
                p_sign = (min(1.0, 2.0 * sum(comb(n_eff, j) for j in range(k, n_eff + 1))
                              / 2 ** n_eff) if n_eff else None)
                # 단측 — 만장일치를 판정 요소로 쓰려면 이쪽이다 (n=5 만장일치 p1=0.031)
                p1_sign = (sum(comb(n_eff, j) for j in range(k, n_eff + 1)) / 2 ** n_eff
                           if n_eff else None)
            except Exception:
                p_sign = p1_sign = None
            unanimous = n_eff >= 3 and (npos == n_eff or nneg == n_eff)
            sign_txt = (f"부호 {npos}/{n_eff} 양(Li 쪽)"
                        + (f" · 동점 {n_dir - n_eff}개 제외" if n_eff < n_dir else "")
                        + (f" · 양측 p={p_sign:.3f}" if p_sign is not None else "")
                        + ("  **만장일치**" if unanimous else ""))
            ci_txt = (f"방향 순서통계 CI [{ci_lo:+.3f}, {ci_hi:+.3f}] eV "
                      f"(정확 커버리지 {ci_cov * 100:.1f}%)"
                      + ("  ⚠ n=3 은 90% CI 가 원리적으로 불가능하다" if n_dir == 3 else ""))
            ci_excludes_zero = (ci_lo > 0) or (ci_hi < 0)
            # ── 결합 규칙 (2026-08-11 자체검토) — 크기와 부호를 **같은 층**에 둔다 ────
            #   크기 증거 = 순서통계 CI 가 0 을 배제 AND |중앙값| ≥ 판정바닥
            #   부호 증거 = 만장일치 (n≥3). 둘은 서로 다른 종류의 증거라 따로 센다.
            #   ⚠ 옛 규칙은 크기가 관문이고 부호는 주석이었는데, 부호가 더 강한 경우가
            #     실제로 있다 (dimer 3/3 만장일치인데 크기는 바닥 아래).
            ev_mag = ci_excludes_zero and abs(med) >= floor
            ev_sign = unanimous
            # ★★ 2026-08-11 (Codex 재리뷰 채택) — **유한 설계 분류**.
            #   방향은 사전 선언된 atlas 설계지 무작위 표본이 아니다. 그러면 SE·p 를
            #   population inference 처럼 쓰면 안 되고, 대신 **고정 실무 임계 δ=30 meV** 에
            #   대한 ① 부호 일관성 ② 임계 초과 커버리지 를 따로 보고하는 게 정직하다.
            #   (n=3~5 에서 정규 근사 SE 도 부트스트랩도 못 믿는다는 게 양쪽 검토의 결론.)
            delta = GATE["decision_floor_eV"]
            side = 1 if med > 0 else -1
            frac_sign = (npos if side > 0 else nneg) / n_dir
            frac_exceed = sum(1 for x in dl if side * x > delta) / n_dir
            if frac_sign >= 0.8 and frac_exceed >= 0.8:
                cls = "ROBUST_SCREENING"
            elif frac_sign >= 0.8 and abs(med) > delta:
                cls = "MARGINAL_TENDENCY"
            elif frac_sign >= 0.8:
                cls = "SIGN_CONSISTENT_SMALL"
            else:
                cls = "UNRESOLVED_MIXED"
            print(f"     유한설계 분류 **{cls}** — 같은 부호 {frac_sign * 100:.0f}% · "
                  f"|Δ|>{delta * 1000:.0f} meV 인 방향 {frac_exceed * 100:.0f}% "
                  f"(δ 는 UMA 실무 해상도로 **고정**, n 과 무관)")
            print(f"     {ci_txt}")
            print(f"     {sign_txt}")
            if abs(med) < floor:
                print(f"   → **가려지지 않았다** (|Δ| {abs(med):.3f} < 판정바닥 {floor:.3f} eV "
                      f"= max(30 meV, 방향 표준편차 ddof=1))")
                if ev_sign:
                    print(f"     ⚠ 크기는 바닥 아래인데 **부호는 만장일치**다 — 작지만 실재하는 "
                          f"차이일 수 있다. 방향을 늘리면 갈릴 자리다. 지금은 판정 안 한다.")
            elif margin < se_med:
                win = "Li" if med > 0 else "Ni"
                print(f"   → ⚠ **판정 보류 (MARGINAL)** — 바닥 {floor:.3f} eV 를 "
                      f"{margin * 1000:+.1f} meV 로 넘었는데 중앙값 자체의 표준오차가 "
                      f"±{se_med * 1000:.1f} meV 다. 넘은 폭이 불확실도보다 작다.")
                print(f"     방향 {n_dir}개 → 중앙값은 {(n_dir + 1) // 2}번째 방향 하나가 정한다. "
                      f"⛔ '{win} 우세'로 인용하지 말 것.")
                print(f"     증거: 크기 {'✔' if ev_mag else '✗'} · 부호 {'✔' if ev_sign else '✗'}")
                print(f"     해소: 독립 방향을 늘리거나(atlas --ndir↑) DFT+U 대조로 간다.")
            else:
                win = "Li" if med > 0 else "Ni"
                if ev_mag and ev_sign:
                    print(f"   → 이 프로토콜에서 **{win} 우세** — 크기·부호 **두 증거 모두** "
                          f"(바닥 {floor:.3f} eV 를 {margin * 1000:+.1f} meV 초과 · "
                          f"CI 가 0 배제 · 부호 만장일치). 열역학 판정 아님 — DFT+U 대조 필요.")
                else:
                    have = "크기" if ev_mag else "부호"
                    lack = "부호(만장일치 아님)" if ev_mag else "크기(CI 가 0 을 포함)"
                    print(f"   → ⚠ **판정 보류 (한쪽 증거만)** — {have} 증거는 있는데 "
                          f"{lack} 증거가 없다. {win} 쪽이지만 인용하지 말 것.")
                    print(f"     두 증거가 갈리는 건 방향 의존성이 남아 있다는 뜻이다 — "
                          f"독립 방향을 늘리거나 DFT+U 대조로 간다.")
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
                if confounded:
                    print(f"     → ⛔ **무효**. 위 검열 검사가 걸렸으므로 이 Δ 는 자리 선호가 아니다.")
                    print(f"        방향({'Ni' if d < 0 else 'Li'} 낮음)을 인용하지 말 것 — 검열된 자세를")
                    print(f"        되살리면 부호가 뒤집힐 수 있다.")
                elif abs(d) < floor:
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
    clean = read(a.clean) if getattr(a, "clean", None) else None
    if clean is None:
        print("⚠ --clean 없음 → 추출 검사를 못 한다. 이 대조는 **기하 게이트 한정**이다.")
    recs = sorted(d.glob("**/*.json"))
    if not recs:
        sys.exit(f"⛔ {d} 에 json 레코드가 없다")
    n_ok = n_dis = seen = no_model = no_struct = 0
    disagreements = []
    for p in recs:
        try:
            r = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        if not isinstance(r, dict):
            continue
        seen += 1
        # Codex 레코드는 model=uma-s-1p1 / model_name=dimer|c10 · stage="relaxed" 를 쓴다
        # (2026-08-11 교차검증에서 확인 — 예전 우리 매핑은 0건을 조용히 넘겼다).
        frag = {"dimer": "ptfe_dimer", "c10": "ptfe_c10"}.get(
            r.get("model_name") or r.get("model"))
        if not frag:
            no_model += 1
            continue
        sfile = (r.get("structure_xyz") or (r.get("structures") or {}).get("xyz")
                 or (r.get("structure") or {}).get("xyz"))
        if not sfile:
            for k in ("relaxed_structures", "rigid_structures"):
                cand = d / k / f"{r.get('pose_id', '')}.xyz"
                if cand.is_file():
                    sfile = str(cand); break
        if not sfile or not Path(sfile).is_file():
            no_struct += 1
            continue
        relaxed_flag = (r.get("stage") == "relaxed") or bool(r.get("relaxed"))
        mol_ref, _ = load_fragment(frag)
        cx = read(sfile)
        cx.set_cell(slab.cell.array); cx.set_pbc(True)
        g = apply_gates(cx, len(slab), mol_ref, frag, clean=clean, relaxed=relaxed_flag)
        theirs = bool(r.get("ranking_eligible"))
        if theirs == g["ranking_eligible"]:
            n_ok += 1
        else:
            n_dis += 1
            disagreements.append((p.name, theirs, g["ranking_eligible"], g["gate_reasons"],
                                  r.get("classification")))
    print(f"레코드 {seen}건 · 조각 인식 실패 {no_model} · 구조 파일 없음 {no_struct}")
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

    # 8) 추출 판정 — **움직였고 + 배위를 잃었을 때만** 탈락해야 한다 (Codex 지적 반영)
    cx = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 3.2)
    cx.positions[li, 2] += 1.5
    check("Li 추출 (표면 Li +1.5 Å, 배위 상실)", cx, "EXTRACTION_CANDIDATE", clean=slab)

    #   ★ Codex 가 지적한 회귀 — 슬랩이 **전혀 안 움직인** 정상 배위를 추출로 죽이면 안 된다.
    def contact_at(el_target: str, d: float) -> Atoms:
        c = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 2.4)
        low = n + int(np.argmin(c.positions[n:, 2]))
        c.positions[n:] += (c.positions[li] + np.array([0, 0, d])) - c.positions[low]
        return c
    for d in (2.00, 2.15):
        g = check(f"정상 배위 F···Li {d:.2f} Å (슬랩 변위 0)", contact_at("F", d), "", clean=slab)
        v = g.get("extraction", {}).get("verdict")
        good = v == "NORMAL_COORDINATION"
        ok &= good
        print(f"   {'✔' if good else '⛔'} {'  └ 추출 판정 = NORMAL':34s} 실제={v} "
              f"· 접촉증거={len(g.get('extraction',{}).get('cation_near_molecule',[]))}건")

    #   변위 경계 — Li 0.80 Å 아래는 정상, 위이면서 배위를 잃어야 추출
    #   변위 경계는 **정확한 판정**으로 본다 (Round-2: 'NORMAL 아님'은 검사가 아니다)
    for d, want in ((0.79, "NORMAL_COORDINATION"), (0.81, None), (1.20, "EXTRACTION_CANDIDATE")):
        c = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 3.2)
        c.positions[li, 2] += d
        v = apply_gates(c, n, mol, "ptfe_c10", clean=slab, relaxed=True,
                        bonds=bonds)["extraction"]["verdict"]
        good = (v == want) if want else (v != "NORMAL_COORDINATION")
        ok &= good
        print(f"   {'✔' if good else '⛔'} 표면 Li +{d:.2f} Å → {v} (기대 {want or 'NORMAL 아님'})")

    #   면내 hop 은 추출이 아니다 — 배위수를 유지하며 옆으로 움직인 Li
    c = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 3.2)
    c.positions[li] += slab.cell.array[1] / 4.0        # b/4 = 등가 자리로 병진
    v = apply_gates(c, n, mol, "ptfe_c10", clean=slab, relaxed=True,
                    bonds=bonds)["extraction"]["verdict"]
    good = v != "EXTRACTION_CANDIDATE"
    ok &= good
    print(f"   {'✔' if good else '⛔'} 면내 hop (Li 를 b/4 병진) → {v} (추출이면 안 된다)")

    # 9) 고정 원자 drift 검사가 **실제 구속 인덱스**를 보는가 — 진짜 assert 로
    cons, nfix, _z = _freeze_mask(n, slab, 0.85)
    fixed = np.asarray(cons.index, dtype=int)
    free_in_prefix = sorted(set(range(nfix)) - set(fixed.tolist()))
    ok &= bool(free_in_prefix)          # 이 슬랩에서 비연속이 아니면 회귀시험 전제가 깨진 것
    print(f"   {'✔' if free_in_prefix else '⛔'} freeze 0.85 고정 인덱스 비연속 — "
          f"앞 {nfix}개 중 자유 원자 {len(free_in_prefix)}개")
    #   자유 원자만 흔들었을 때: cons.index 로 재면 0, positions[:nfix] 로 재면 0 이 아니어야 한다
    probe = slab.copy()
    probe.positions[free_in_prefix[0], 2] += 0.5
    d_right = float(np.abs(probe.positions[fixed] - slab.positions[fixed]).max())
    d_wrong = float(np.abs(probe.positions[:nfix] - slab.positions[:nfix]).max())
    good = d_right < GATE["frozen_drift_A"] <= d_wrong
    ok &= good
    print(f"   {'✔' if good else '⛔'}   └ 자유 원자 하나를 0.5 Å 흔들면 "
          f"cons.index 기준 drift {d_right:.4f} · positions[:nfix] 기준 {d_wrong:.4f}")

    # 9) 거울상 방지 — 반평행 정렬이 카이랄성을 뒤집지 않는지
    try:
        make_pose(slab, mol, anc["Li_top"]["xyz"], np.array([0.0, 0.0, -1.0]), 0, 2.4)
        make_pose(slab, mol, anc["Li_top"]["xyz"], np.array([0.0, 0.0, 1.0]), 0, 2.4)
        print("   ✔ 반평행 정렬에서 거울상/변형 없음")
    except RuntimeError as e:
        ok = False
        print(f"   ⛔ 반평행 정렬: {e}")

    # 10) ★ 게이트/계산 지문 분리 — 게이트 임계를 바꿔도 계산 지문은 그대로여야 한다
    #     (자체 리뷰 #1: 예전엔 relax 가 gate_version 을 지문에 섞어 이완 전부가 재실행됐다)
    def _fp():
        return make_protocol(stage="relax", model="uma-s-1p1", task="omat",
                             atlas_gap=2.4, atlas_ndir=12, fmax=0.05, steps=300,
                             freeze_frac=0.85)
    p1 = _fp()
    _old = GATE["decision_floor_eV"]
    GATE["decision_floor_eV"] = 0.999
    p2 = _fp()
    GATE["decision_floor_eV"] = _old
    good = p1["fingerprint"] == p2["fingerprint"] and p1["gate_version"] != p2["gate_version"]
    ok &= good
    print(f"   {'✔' if good else '⛔'} 게이트 임계 변경 → 계산 지문 불변({p1['fingerprint'][:8]}) · "
          f"gate_version 만 변경")

    # 11) 감긴 분자 — 원자 하나를 +b 로 감아도 결합 검사가 절단으로 오판하면 안 된다
    cxw = make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 2.4)
    wi = n + int(np.argmax(cxw.positions[n:, 2]))       # 분자 꼭대기 원자 하나를 감는다
    cxw.positions[wi] += slab.cell.array[1]
    g = check("주기 감김 (원자 하나 +b 병진)", cxw, "")
    good = g["bond"]["n_changes"] == 0
    ok &= good
    print(f"   {'✔' if good else '⛔'}   └ 결합변화 {g['bond']['n_changes']} (감김을 펴서 검사)")

    # 12) clean 불일치 — 다르게 정렬된 clean 은 오판 대신 '검사 불가'를 내야 한다
    bad_clean = slab[list(range(1, n)) + [0]]           # 순서를 한 칸 민 슬랩
    g = check("clean 순서 불일치 (오판 대신 미실시)", make_pose(slab, mol, anc["Li_top"]["xyz"], down, 0, 2.4),
              "", relaxed=True, clean=bad_clean)
    v = g.get("extraction", {}).get("verdict")
    good = v == "CLEAN_MISMATCH" and any("clean_mismatch" in w for w in g["warnings"])
    ok &= good
    print(f"   {'✔' if good else '⛔'}   └ 판정={v} · 경고 표시됨")

    # ══ basin 중복제거 (회신 W 2단계) ═══════════════════════════════════════
    def _chk(good, name):
        nonlocal ok
        ok &= bool(good)
        print(f"   {'✔' if good else '⛔'} {name}")

    import numpy as _np
    from ase import Atoms as _A
    _cell = _np.diag([18.0, 11.0, 30.0])

    def _mk(dz, dx=0.0, el="C"):
        # 슬랩 4 (Li,Ni,O,O) + 분자 3 (heavy 2 + H)
        pos = [[0, 0, 0], [3, 0, 0], [6, 0, 0], [9, 0, 0],
               [0 + dx, 0, 2.5 + dz], [1.4 + dx, 0, 2.5 + dz], [0.7 + dx, 0, 3.5 + dz]]
        return _A(symbols=["Li", "Ni", "O", "O", el, "C", "H"],
                  positions=pos, cell=_cell, pbc=True)

    d0 = basin_descriptor(_mk(0.0), 4)
    d1 = basin_descriptor(_mk(0.05), 4)          # 거의 같은 자세
    d2 = basin_descriptor(_mk(3.0), 4)           # 훨씬 위 — 접촉이 끊긴다
    d3 = basin_descriptor(_mk(0.0, el="S"), 4)   # 접촉 원소가 다르다
    _chk(d0["fingerprint"] == d1["fingerprint"], "basin: 미세 이동은 같은 접촉지문")
    _chk(d0["fingerprint"] != d3["fingerprint"],
         "[음성] 접촉 **원소**가 다르면 다른 지문 (min_contact 하나가 아니라 graph)")
    _chk(d0["fingerprint"] != d2["fingerprint"],
         "[음성] 높이가 3 Å 다르면 접촉이 끊겨 다른 지문")
    b = dedup_basins([("a", -1.0, d0, _cell), ("b", -0.9, d1, _cell),
                      ("c", -0.8, d3, _cell)])
    _chk(len(b) == 2, f"basin 묶기: 같은 지문 2개 → 1 basin, 다른 지문은 별도 (실제 {len(b)})")
    _chk(b[0]["rep_label"] == "a" and "b" in b[0]["members"],
         "대표는 **에너지 낮은 쪽**, 나머지는 members 로 보존")
    # ⛔ 회신 W 4단계 — **sealed audit 은 창 안에서 뽑으면 안 된다.**
    #   초판이 그랬고(실측 +0.0765 vs 창 ~+0.17) 시험이 없어서 놓쳤다.
    _fake = [{"basin_id": "b%02d" % i, "E_pose_eV": e, "rep_label": "L%d" % i,
              "fingerprint": (("C", "O", 1),) if i % 2 else (("C", "Ni", 1),),
              "anchor": ("C", "O", 2.4), "height_A": 2.5, "tilt_deg": 30.0,
              "members": ["L%d" % i], "n_members": 1}
             for i, e in enumerate([0.00, 0.02, 0.08, 0.14, 0.19, 0.31, 0.45])]
    _emin = _fake[0]["E_pose_eV"]
    _inside = [b for b in _fake if b["E_pose_eV"] - _emin <= BASIN_W0_EV]
    _outside = [b for b in _fake if b["E_pose_eV"] - _emin > BASIN_W0_EV]
    _chk(len(_inside) == 4 and len(_outside) == 3,
         f"창 W0=0.15 분할: 안 {len(_inside)} / 밖 {len(_outside)}")
    _seen = {"b00", "b01", "b03", "b04"}          # calibration 4 가 잡았다고 가정
    _pool_out = [b for b in _outside if b["basin_id"] not in _seen]
    _chk(bool(_pool_out) and _pool_out[0]["basin_id"] == "b05",
         "[음성 W-4] audit#1 은 **창 바깥**에서 (b05) — 창 안 b02 를 집으면 안 된다")
    _chk(_pool_out[0]["E_pose_eV"] - _emin > BASIN_W0_EV,
         f"[음성 W-4] 그 basin 이 실제로 창 밖이다 (+{_pool_out[0]['E_pose_eV'] - _emin:.3f} "
         f"> {BASIN_W0_EV})")

    far = basin_descriptor(_mk(0.0, dx=6.0), 4)
    if far["fingerprint"] == d0["fingerprint"]:
        b2 = dedup_basins([("a", -1.0, d0, _cell), ("x", -0.9, far, _cell)])
        _chk(len(b2) == 2, "[음성] 지문이 같아도 RMSD 가 크면 **다른 basin**")

    print(f"\n{'✔ 전부 통과' if ok else '⛔ 실패 있음'}")
    return 0 if ok else 1


# ── DFT+U 인계 ────────────────────────────────────────────────────────────────────
#   UMA 는 후보를 제안하고 **판정은 DFT+U 가** 한다. 이 단계가 그 경계다.
#   두 자기 초기값은 필수다 — Ni 자기상태가 다르게 수렴하면 ΔE 가 통째로 오염된다
#   (2026-08-03 실측: U=6.2 를 바로 넣으면 FM 붕괴, 총자화 0 → +2.58).
INCAR_TEMPLATE = """SYSTEM = {system}
# 자리 선호 판정용 — Li_top / Ni_top 대조쌍은 **모든 설정이 같아야** 한다.
ISTART = 0 ; ICHARG = 2
PREC   = Accurate
ENCUT  = 520
EDIFF  = 1E-5
EDIFFG = -0.02
IBRION = 2 ; NSW = 200 ; ISIF = 2
ISMEAR = 0 ; SIGMA = 0.05      # 자성 반도체 슬랩 — 가우시안. (분자도 ISMEAR=0)
ALGO   = Normal
LREAL  = Auto
NELM   = 200

# 스핀 · DFT+U (Dudarev)
ISPIN  = 2
LASPH  = .TRUE.                # DFT+U 에는 필수
LDAU   = .TRUE. ; LDAUTYPE = 2
LDAUL  = {ldaul}
LDAUU  = {ldauu}
LDAUJ  = {ldauj}
LDAUPRINT = 2
LMAXMIX = 4
MAGMOM = {magmom}

# 분산 — ⚠ IVDW=11 은 **D3 zero damping** 이다. D3(BJ) 는 12 다.
#   (우리 2026-08-08 외주 수령분 JSON 이 11 을 'D3(BJ)' 로 잘못 적어 뒀다 — 그 표기가 틀렸다.
#    값은 그 실행과 맞추려고 11 을 유지한다. BJ 로 갈 거면 12 로 바꾸고 양쪽 다 바꿀 것.)
IVDW   = 11

# 한쪽만 흡착한 슬랩 — 쌍극자 보정
LDIPOL = .TRUE. ; IDIPOL = 3

# 출력 — ⚠ CHGCAR 를 남긴다. U-ramp 가 필요하면 ICHARG=1 로 승계해야 하는데
#   LCHARG=.FALSE. 면 그 경로가 막힌다 (요청서가 U-ramp 를 허용하므로 켜 둔다).
LORBIT = 11
LWAVE  = .FALSE. ; LCHARG = .TRUE.
NCORE  = 4
"""


def _magmom_configs(atoms: Atoms, nslab: int, frag: str) -> Dict[str, List[float]]:
    """자기 초기값 2종을 **원자 원본 순서**의 리스트로 돌려준다.

    ⚠⚠ 문자열로 바로 만들면 안 된다 — POSCAR 는 종별로 재정렬되므로 **재매핑이 필요**하다.
      2026-08-11 Codex 교차검증에서 실측: 48개 모멘트 중 36개가 Li·O 에 걸려 있었다
      (원본은 층별로 뒤섞인 순서, POSCAR 는 Li48 Ni48 O96… 블록). 외주 입력이 통째로
      틀어질 뻔했다. 그래서 반환형을 리스트로 바꾸고 호출부에서 POSCAR 순서로 옮긴다.

    ⚠ 이름은 실제 알짜값이다. Ni 48개를 전부 ±2 로 두면 총합이 4k−96 이라 **4 의 배수만**
      가능하다 — 'net2' 는 이 구성에서 만들 수 없다(그렇게 부르면 거짓말).
    ⚠ 열린 껍질 조각(sdcp_doped 라디칼)은 분자 쪽에도 씨앗을 준다. 전부 0 으로 두면
      doublet 이 닫힌 껍질로 붕괴할 수 있다 (Codex 지적, 채택).
    """
    sym = atoms.get_chemical_symbols()
    ni = [i for i in range(nslab) if sym[i] == "Ni"]
    order = sorted(ni, key=lambda i: (round(atoms.positions[i, 2], 2), atoms.positions[i, 0]))
    open_shell = "DOUBLET" in FRAGMENTS[frag]["electrons"].upper()
    # 라디칼 씨앗 자리 — 분자부에서 술포네이트 O (없으면 분자 전체에 옅게)
    seed: List[int] = []
    if open_shell:
        molpart = atoms[nslab:]
        gi = group_indices(molpart, "SO3")
        seed = [nslab + i for i in gi if molpart.get_chemical_symbols()[i] == "O"] \
            or list(range(nslab, len(atoms)))
    out: Dict[str, List[float]] = {}
    for name, flip in (("afm_balanced", 0), ("afm_net4", 1)):
        mag = [0.0] * len(atoms)
        for k, i in enumerate(order):
            mag[i] = 2.0 if k % 2 == 0 else -2.0
        if flip and len(order) >= 2:
            mag[order[1]] = 2.0          # 한 자리를 뒤집으면 알짜가 0 → +4
        for i in seed:                   # 라디칼 1개분(총 1 μB)을 씨앗 자리에 나눠 준다
            mag[i] = round(1.0 / len(seed), 3)
        out[name] = mag
    return out


def _write_poscar(path: Path, atoms: Atoms, nslab: int, freeze_frac: float,
                  zcut=None) -> Dict[str, Any]:
    """종별로 묶고 Selective Dynamics 로 **아래 절반 고정 / 위 절반+분자 자유**.

    ⚠ UMA 단계의 구속을 그대로 승계하지 않는다 — DFT 는 표면 이완을 허용해야 한다.
    ⚠⚠ 2026-08-11 자체검토 — order 밖 원소(leftover)가 좌표로는 적히는데 counts 루프가
      order 만 돌아 종/개수 헤더에서 **사라졌다**. VASP 는 헤더 개수만 믿으므로 남는
      좌표를 조용히 버리고 **다른 계를 계산**한다. 현 조각(Li/Ni/O/S/C/F/H)에선 미발현,
      P·Na·B 가 들어오는 순간 터지는 잠복이라 원소별로 묶어 전부 센다.
    ★ zcut 을 밖에서 주면 쌍·기준계 전 잡이 **같은 고정 평면**을 공유한다 — 자세마다
      z-범위로 다시 재면 UMA 이완 후 표면이 뜬 자세에서 고정 원자 집합이 어긋난다.
    """
    order = ["Li", "Ni", "O", "S", "C", "F", "H"]
    sym = atoms.get_chemical_symbols()
    order = order + sorted({x for x in sym if x not in order})
    idx: List[int] = []
    for el in order:
        idx += [i for i in range(len(atoms)) if sym[i] == el]
    z = atoms.positions[:nslab, 2]
    if zcut is None:
        zcut = z.min() + (z.max() - z.min()) * freeze_frac
    cell = atoms.cell.array
    frac = np.linalg.solve(cell.T, atoms.positions.T).T
    counts, seen = [], []
    for el in order:
        n = sum(1 for i in idx if sym[i] == el)
        if n:
            counts.append(n); seen.append(el)
    lines = [f"site_screen DFT handoff (freeze<= {zcut:.3f} A)", "1.0"]
    lines += [f"  {v[0]:.10f} {v[1]:.10f} {v[2]:.10f}" for v in cell]
    lines += ["  " + "  ".join(seen), "  " + "  ".join(str(c) for c in counts),
              "Selective dynamics", "Direct"]
    nfix = 0
    for i in idx:
        fixed = i < nslab and atoms.positions[i, 2] <= zcut + 1e-9
        nfix += fixed
        f = "F  F  F" if fixed else "T  T  T"
        lines.append(f"  {frac[i,0]:.10f} {frac[i,1]:.10f} {frac[i,2]:.10f}   {f}")
    path.write_text("\n".join(lines) + "\n")
    return {"species_order": seen, "counts": counts, "n_fixed": int(nfix),
            "z_cut_A": round(float(zcut), 3),
            "order": [int(i) for i in idx],          # POSCAR 위치 k → 원본 인덱스
            "vasp_index_map_1based": {str(k + 1): int(i) for k, i in enumerate(idx)}}


def cmd_dft_handoff(a) -> int:
    """자격 있는 대조쌍을 **같은 프로토콜의 VASP 잡**으로 내보낸다."""
    slab = load_slab()
    nslab = a.nslab
    d = Path(a.dir)
    rows = [json.loads(p.read_text()) for p in sorted(d.glob("*.json"))
            if not p.name.startswith("_")]
    fs = [r for r in rows if r.get("ranking_eligible") and r.get("E_pose_eV") is not None]
    if not fs:
        sys.exit(f"⛔ {d} 에 순위 가능한 자세가 없다")

    idx = {(r["site"], r["down_dir"], r["roll_deg"]): r for r in fs}
    pairs = []
    for (s, dd, ro), r in idx.items():
        if s != "Li_top":
            continue
        q = idx.get(("Ni_top", dd, ro))
        if not q:
            continue
        if r.get("nearest_cation") != "Li" or q.get("nearest_cation") != "Ni":
            continue                                    # 자격 미달 — verdict 와 같은 규칙
        pairs.append((min(r["E_pose_eV"], q["E_pose_eV"]), dd, ro, r, q))
    if not pairs:
        sys.exit("⛔ 자격 있는 대조쌍이 없다 — DFT 로 넘길 반사실 대조가 성립하지 않는다")

    # ★ 2026-08-11 — 쌍 선택을 `min(E_Li, E_Ni)` 로만 하면 **한쪽 끝점만 매우 깊은 쌍**이
    #   먼저 뽑힌다(Codex Round-2 지적). 실제로 그렇게 골랐더니 ptfe_c10 f0.85 에서
    #   ΔE 중앙값 +0.041 인데 **부호가 반대인 −0.037 쌍**이 1순위로 나왔다.
    #   DFT 는 비싸다 — 무엇을 대표로 보내는지 명시적으로 고른다.
    dl = sorted(q["E_pose_eV"] - r["E_pose_eV"] for _e, _d, _r, r, q in pairs)
    med = float(np.median(dl))
    print(f"자격 있는 대조쌍 {len(pairs)}개 · ΔE(Ni−Li) 중앙값 {med:+.3f} eV")
    for _e, dd, ro, r, q in sorted(pairs, key=lambda t: t[4]["E_pose_eV"] - t[3]["E_pose_eV"]):
        de = q["E_pose_eV"] - r["E_pose_eV"]
        mark = "  ← 중앙값과 부호 반대" if de * med < 0 else ""
        print(f"   {dd}/r{int(ro):03d}  ΔE {de:+.3f}  (Li {r['E_pose_eV']:+.3f} · "
              f"Ni {q['E_pose_eV']:+.3f}){mark}")

    def key(t):
        de = t[4]["E_pose_eV"] - t[3]["E_pose_eV"]
        return {"median": abs(de - med),          # 대표 — 중앙값에 가장 가까운 쌍
                "deepest": t[0],                  # 옛 방식 — 한쪽 끝점이 가장 깊은 쌍
                "extreme": -abs(de - med)}[a.select]   # 양 끝 — 불일치를 DFT 로 검사
    pairs.sort(key=key)
    pairs = pairs[:a.pairs]
    print(f"→ 선택 기준 '{a.select}' 로 {len(pairs)}쌍 인계")

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    manifest: Dict[str, Any] = {
        "source_run": str(d), "gate_version": gate_version(), "nslab": nslab,
        "freeze_frac_dft": a.freeze, "kmesh": a.kmesh,
        "protocol": "PBE+U(Ni 6.2, Dudarev) + D3(BJ) · LASPH · LDIPOL/IDIPOL=3 · ISMEAR=0 "
                    "· 아래 절반 고정 · 자기 초기값 2종",
        "why_two_magnetic_starts": "Ni 자기상태가 두 끝점에서 다르게 수렴하면 ΔE 가 통째로 "
                                   "오염된다. 2026-08-03 에 U=6.2 즉시 투입으로 FM 붕괴를 겪었다.",
        "jobs": {}, "pairs": [],
    }
    for _e, dd, ro, r, q in pairs:
        pid = f"{dd}_r{int(ro):03d}"
        manifest["pairs"].append({
            "pair_id": pid, "down_dir": dd, "roll_deg": ro,
            "uma_E_pose_Li": r["E_pose_eV"], "uma_E_pose_Ni": q["E_pose_eV"],
            "uma_dE_Ni_minus_Li_eV": round(q["E_pose_eV"] - r["E_pose_eV"], 4),
            "note": "UMA 값은 순위용이다 — DFT 결과와 같은 표에 놓지 말 것",
        })
        for role, rec in (("Li", r), ("Ni", q)):
            xyz = d / f"{rec['label']}.xyz"
            if not xyz.is_file():
                print(f"  ⚠ {rec['label']}.xyz 없음 — 건너뜀"); continue
            cx = read(xyz); cx.set_cell(slab.cell.array); cx.set_pbc(True)
            frag_of = rec.get("fragment") or Path(a.dir).parent.name
            for mag_name, mag_orig in _magmom_configs(cx, nslab, frag_of).items():
                jd = out / f"{pid}__{role}top__{mag_name}"
                jd.mkdir(parents=True, exist_ok=True)
                pos = _write_poscar(jd / "POSCAR", cx, nslab, a.freeze)
                el = pos["species_order"]
                # ★★ POSCAR 는 종별로 재정렬된다 — MAGMOM 을 **그 순서로 옮긴다**.
                #    안 옮기면 모멘트가 Ni 가 아닌 원자에 걸린다 (2026-08-11 실측: 48개 중 36개).
                mag_poscar = [mag_orig[i] for i in pos["order"]]
                nz_ok = all(cx.get_chemical_symbols()[pos["order"][k]] in ("Ni",)
                            or abs(v) < 1e-9 or k >= sum(pos["counts"][:2])
                            for k, v in enumerate(mag_poscar))
                (jd / "INCAR").write_text(INCAR_TEMPLATE.format(
                    system=f"{pid} {role}-top {mag_name}",
                    ldaul=" ".join("2" if e == "Ni" else "-1" for e in el),
                    ldauu=" ".join("6.2" if e == "Ni" else "0.0" for e in el),
                    ldauj=" ".join("0.0" for _ in el),
                    magmom=" ".join(f"{m:.3f}" for m in mag_poscar)))
                (jd / "KPOINTS").write_text(
                    f"auto\n0\nGamma\n{a.kmesh}\n0 0 0\n")
                manifest["jobs"][jd.name] = {
                    "pair_id": pid, "role": role, "magnetic": mag_name,
                    "source_pose": rec["label"], "uma_E_pose_eV": rec["E_pose_eV"],
                    **pos}
    (out / "HANDOFF_MANIFEST.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    print(f"→ {out}  · 대조쌍 {len(manifest['pairs'])}개 · 잡 {len(manifest['jobs'])}개")
    for p in manifest["pairs"]:
        print(f"   {p['pair_id']:22s} UMA ΔE(Ni−Li) {p['uma_dE_Ni_minus_Li_eV']:+.3f} eV")
    print("   ⚠ POTCAR 은 넣지 않았다(라이선스) — 실행 측에서 Li Ni O S C F H 순서로 붙일 것")
    print("   ⚠ 판정은 두 자기 초기값 중 **각각 더 낮은 쪽**끼리 비교한다. 국소 모멘트와")
    print("      LDAU 점유행렬을 눈으로 확인하기 전에는 수치가 통과해도 조건부다.")
    return 0


def cmd_regate(a) -> int:
    """저장된 이완 구조에 **게이트만 다시 적용**한다 — GPU 재계산 없이.

    게이트는 후처리다. 임계를 고쳤다고 몇 시간짜리 이완을 다시 돌 이유가 없다.
    에너지(E_pose)는 그대로 두고 판정 필드만 갈아끼운다.
    """
    slab = load_slab()
    nslab = a.nslab
    d = Path(a.dir)
    jsons = [p for p in sorted(d.glob("*.json")) if not p.name.startswith("_")]
    if not jsons:
        sys.exit(f"⛔ {d} 에 자세 JSON 이 없다")
    clean_path = a.clean or (d / "_clean_slab.vasp")
    clean = read(clean_path) if Path(clean_path).is_file() else None
    if clean is None:
        print(f"⚠ 깨끗한 슬랩이 없다 ({clean_path}) — 추출 검사는 '미실시'로 기록된다")
    gv = gate_version()
    n_chg, n_same, n_nostruct = 0, 0, 0
    for p in jsons:
        r = json.loads(p.read_text())
        frag = r.get("fragment")
        xyz = d / f"{r.get('label')}.xyz"
        if not frag or not xyz.is_file():
            n_nostruct += 1
            continue
        mol, info = load_fragment(frag)
        if mol is None:
            n_nostruct += 1
            continue
        cx = read(xyz)
        cx.set_cell(slab.cell.array); cx.set_pbc(True)
        g = apply_gates(cx, nslab, mol, frag, clean=clean, relaxed=True)
        was = bool(r.get("ranking_eligible"))
        r.update({k: v for k, v in g.items() if k != "bond"})
        r["bond_changes"] = g["bond"]["n_changes"]
        r["gate_version"] = gv
        # 계산 단계에서 붙은 판정(수렴·고정드리프트)은 게이트가 지우면 안 된다
        for extra, cond in (("NOT_CONVERGED", r.get("converged") is False),
                            ("FROZEN_DRIFT", (r.get("frozen_drift_A") or 0) > GATE["frozen_drift_A"])):
            if cond and not any(x.startswith(extra) for x in r["gate_reasons"]):
                r["gate_reasons"].append(extra); r["ranking_eligible"] = False
        p.write_text(json.dumps(r, indent=1, ensure_ascii=False))
        n_chg += (was != bool(r["ranking_eligible"]))
        n_same += (was == bool(r["ranking_eligible"]))
    print(f"{d.name}: {len(jsons)}개 · 판정 바뀜 {n_chg} · 그대로 {n_same} · 구조 없음 {n_nostruct}")
    print(f"   게이트 버전 {gv}")
    return 0


def cmd_bundle(a) -> int:
    """실행 결과를 **독립 재감사 가능한 묶음**으로 내보낸다.

    Round-2 지적: 회답에 적은 수치를 남이 검증할 machine-readable 근거가 repo 에 없었다.
    manifest 에 commit·모델/task·프로토콜 지문·파일별 sha256 을 전부 박는다.
    """
    import subprocess
    import tarfile
    run = Path(a.run)
    out = Path(a.out)
    if not run.is_dir():
        sys.exit(f"⛔ {run} 이 없다")
    try:
        commit = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "-C", str(REPO), "status", "--porcelain"],
                                    capture_output=True, text=True).stdout.strip())
    except FileNotFoundError:
        commit, dirty = "unknown", True

    files, manifest = [], {
        "tool": "site_screen.py", "repo_commit": commit, "repo_dirty": dirty,
        "run_dir": str(run), "slab": {k: str(v) for k, v in SLAB.items()},
        "fragments": {}, "files": {},
    }
    for name, spec in FRAGMENTS.items():
        p: Path = spec["path"]
        manifest["fragments"][name] = {
            "path": str(p), "declared_sha256": spec["sha256"],
            "actual_sha256": sha256(p) if p.is_file() else None,
            "present": p.is_file(), "electrons": spec["electrons"],
        }
    for pat in ("**/*.json", "**/*.xyz", "**/*.vasp", "**/*.txt", "**/*.log", "**/*.csv"):
        for f in run.glob(pat):
            if f.is_file() and f.stat().st_size < a.max_mb * (1 << 20):
                files.append(f)
                manifest["files"][str(f.relative_to(run))] = {
                    "sha256": sha256(f), "bytes": f.stat().st_size}
    mpath = run / "BUNDLE_MANIFEST.json"
    mpath.write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    with tarfile.open(out, "w:gz") as tf:
        tf.add(mpath, arcname="BUNDLE_MANIFEST.json")
        for f in files:
            tf.add(f, arcname=str(f.relative_to(run)))
    mb = out.stat().st_size / (1 << 20)
    print(f"→ {out}  ({len(files)}개 파일 · {mb:.1f} MB)")
    print(f"   commit {commit[:12]}{' ⚠ dirty' if dirty else ''}")
    miss = [k for k, v in manifest["fragments"].items() if not v["present"]]
    bad = [k for k, v in manifest["fragments"].items()
           if v["present"] and v["declared_sha256"] and v["declared_sha256"] != v["actual_sha256"]]
    if miss:
        print(f"   ⛔ 조각 파일 없음: {miss} — 이 묶음만으로는 재현이 안 된다")
    if bad:
        print(f"   ⛔ sha 불일치: {bad}")
    return 0 if not (miss or bad) else 2


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
    # (--gap/--ndir 제거 — 구조의 정본은 atlas 산출물이고 score 는 저장본만 읽는다. 자체 리뷰 #3)
    p.add_argument("--fmax", type=float, default=0.05)
    p.add_argument("--steps", type=int, default=300)
    p.add_argument("--freeze", nargs="*", type=float, default=[1.0, 0.85],
                   help="1.0=Phase-A/Codex 프로토콜, 0.85=표면 이완 허용. 둘 다 돌려 편향을 드러낸다.")
    p.add_argument("--allow_concurrent_pwx", action="store_true",
                   help="⚠ GPU 빌드 pw.x 와 **동시 실행**을 명시적으로 허용 (1저자 승인 필요). "
                        "VRAM 여유가 8 GiB 미만이면 그래도 막는다. CPU 빌드 pw.x 는 원래 안 막는다")
    p.add_argument("--top-per-site", type=int, default=2)
    p.add_argument("--pairs", type=int, default=5, help="강제로 살릴 Li/Ni 대조쌍 수")

    p = sub.add_parser("basins", help="basin 중복제거 + calibration/audit 선정 (회신 W 2~4)")
    p.add_argument("--out", required=True, help="스크린 디렉터리")
    p.add_argument("--frag", nargs="+", required=True)
    p.add_argument("--freeze", type=float, default=0.85)
    p.add_argument("--nslab", type=int, default=192)
    p.add_argument("--seed", type=int, required=True,
                   help="sealed audit 층화 난수 seed — **DFT 전에** 정하고 기록한다")
    p.add_argument("--date", default="2026-08-29")
    p.add_argument("--save", required=True, help="동결할 manifest 경로")

    p = sub.add_parser("verdict", help="자리 선호 판정표")
    p.add_argument("rows", nargs="+", help="atlas_rows.json 또는 점수가 붙은 rows json")

    p = sub.add_parser("crosscheck", help="Codex 레코드와 **기하 게이트만** 대조 (전체 프로토콜 대조 아님)")
    p.add_argument("--codex", required=True)
    p.add_argument("--clean", default=None,
                   help="깨끗한 슬랩 — 없으면 추출 검사를 못 하므로 대조 범위가 좁아진다")

    p = sub.add_parser("regate", help="저장된 이완 구조에 게이트만 재적용 (GPU 재계산 없음)")
    p.add_argument("dir", help="relax_f*.* 디렉터리")
    p.add_argument("--nslab", type=int, default=192)
    p.add_argument("--clean", default=None, help="기본: <dir>/_clean_slab.vasp")

    p = sub.add_parser("dft-handoff", help="자격 대조쌍을 VASP 잡으로 (자기 초기값 2종)")
    p.add_argument("--dir", required=True, help="relax_f*.* 디렉터리")
    p.add_argument("--out", required=True)
    p.add_argument("--pairs", type=int, default=1, help="몇 쌍을 넘길지")
    p.add_argument("--select", choices=("median", "deepest", "extreme"), default="median",
                   help="median=중앙값 대표(기본) · deepest=한쪽 끝점이 가장 깊은 쌍 · "
                        "extreme=중앙값에서 가장 먼 쌍(불일치 검사용)")
    p.add_argument("--nslab", type=int, default=192)
    p.add_argument("--freeze", type=float, default=0.5, help="DFT 에서 고정할 아래 비율")
    p.add_argument("--kmesh", default="2 2 1")

    p = sub.add_parser("bundle", help="독립 재감사용 실행 묶음 내보내기")
    p.add_argument("--run", required=True)
    p.add_argument("--out", required=True, help="예: /tmp/site_screen_bundle.tar.gz")
    p.add_argument("--max-mb", type=float, default=20.0)
    return ap


def main() -> int:
    a = build_parser().parse_args()
    return {
        "inputs": cmd_inputs, "sites": cmd_sites, "atlas": cmd_atlas,
        "gate": cmd_gate, "verdict": cmd_verdict, "crosscheck": cmd_crosscheck,
        "bond-limits": cmd_bond_limits, "selftest": cmd_selftest, "score": cmd_score,
        "bundle": cmd_bundle, "regate": cmd_regate, "dft-handoff": cmd_dft_handoff,
        "basins": cmd_basins,
    }[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
