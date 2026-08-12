#!/usr/bin/env python3
"""afm_ledger.py — 슬랩 Ni ↔ QE Ni1/Ni2 **부격자 원장** (stdlib 전용).

왜 필요한가 (2026-08-11 Codex 재검토 P0 §2②)
  VASP 는 Ni1/Ni2 를 구분하지 못한다 — AFM 은 종 분리가 아니라 MAGMOM 의 원자별 부호로
  준다. 그래서 "어느 Ni 가 어느 부격자냐" 는 **좌표로만** 알 수 있다. 그런데 번들
  생성기는 슬랩 파일에 나온 Ni 를 세어 앞 절반 −1 / 뒤 절반 +1 로 잘랐다. 개수가
  24/24 로 같다고 같은 자기 topology 인 것은 아니다. 실측:

    QE 원본(db/inputs/sdcp_v2/slab_relax/relax.in) 의 Ni 순서
      Ni2 Ni1 Ni1 Ni1 Ni2 Ni2 Ni2 Ni1 Ni1 Ni2 Ni2 Ni1   ← 블록이 아니라 뒤섞여 있다

  이 도구는 슬랩의 Ni 하나하나를 QE 셀로 접어 **좌표로 매칭**해 부격자를 확정하고,
  그 결과를 기계가 읽는 원장(JSON)으로 남긴다. 원장 없이는 `afm2424_pm1` 같은 이름을
  쓸 수 없다 — 이름은 검증된 매핑에만 붙인다.

부호 규약 (2026-08-08 실납품 계보)
  QE ATOMIC_SPECIES: Li(1) Ni1(2) Ni2(3) O(4),
  starting_magnetization(2)=+0.300 → Ni1,  (3)=−0.300 → Ni2.
  납품 INCAR 의 MAGMOM 은 Ni 블록이 −1 24개 → +1 24개인데, qe_to_vasp.py 가 라벨을
  **처음 나온 순서**(Ni2 가 먼저)로 묶었으므로 그 −1 블록은 Ni2 다.
  ⇒ **Ni2 = −1 · Ni1 = +1**.

    python3 tools/sdcp/afm_ledger.py                       # 기본 경로로 원장 생성
    python3 tools/sdcp/afm_ledger.py --out db/properties/afm_ledger.json
    python3 tools/sdcp/afm_ledger.py --selftest            # 데이터 불필요

이 도구가 **못 하는 것**
  · 자기바닥상태를 고르지 못한다. QE 입력의 배정을 옮길 뿐이고, 그 배정이 실제
    바닥상태인지는 계산이 답한다 (그래서 번들이 seed 를 2종 돌린다).
  · 슬랩이 QE 셀의 **정수 슈퍼셀**이 아니면 매핑하지 않는다 — 추정하지 않고 멈춘다.
  · 이완으로 원자가 크게 움직인 구조에는 못 쓴다 (tol 밖이면 실패로 처리).
  · Ni 외 원소의 자기 시드는 다루지 않는다 (라디칼 조각은 번들 쪽 소관).
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
QE_DEFAULT = REPO / "db" / "inputs" / "sdcp_v2" / "slab_relax" / "relax.in"
SLAB_DEFAULT = REPO / "db" / "structures" / "linio2_104_sym_1x4L4_relaxed.vasp"
OUT_DEFAULT = REPO / "db" / "properties" / "afm_ledger.json"
#: 부격자 배정 = 부호. 납품 계보 그대로 (위 docstring 참조).
SIGN = {"Ni1": +1.0, "Ni2": -1.0}
MATCH_TOL_A = 0.35          # 이완 잔차 허용. 이보다 멀면 "모르는 자리"로 실패시킨다.
#: 최근접과 **차순위** 자리의 간격. 좁으면 잔차가 작아도 배정이 흔들린다
#: (2026-08-12 Codex). 실측 이 슬랩은 2.728 Å 라 여유가 크다.
MARGIN_MIN_A = 0.5


# ── 3×3 선형대수 (numpy 없이) ────────────────────────────────────────────────
def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def inv3(m):
    d = det3(m)
    if abs(d) < 1e-12:
        raise ValueError("특이 행렬 — 셀이 퇴화했다")
    c = [[(m[(i + 1) % 3][(j + 1) % 3] * m[(i + 2) % 3][(j + 2) % 3]
           - m[(i + 1) % 3][(j + 2) % 3] * m[(i + 2) % 3][(j + 1) % 3]) / d
          for j in range(3)] for i in range(3)]
    return [[c[j][i] for j in range(3)] for i in range(3)]      # 전치 = 역행렬


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)]
            for i in range(3)]


def vecmat(v, m):
    return [sum(v[k] * m[k][j] for k in range(3)) for j in range(3)]


# ── 파서 ────────────────────────────────────────────────────────────────────
def parse_qe(path) -> dict:
    """QE 입력 → {cell, labels, frac}. Ni1/Ni2 라벨을 **그대로** 보존한다."""
    t = Path(path).read_text(errors="ignore")
    if "CELL_PARAMETERS" not in t or "ATOMIC_POSITIONS" not in t:
        raise ValueError(f"{path}: CELL_PARAMETERS/ATOMIC_POSITIONS 가 없다")
    chead = t.split("CELL_PARAMETERS")[1].splitlines()[0].lower()
    if "angstrom" not in chead:
        raise ValueError(f"{path}: CELL_PARAMETERS 단위가 angstrom 이 아니다 ({chead.strip()})"
                         " — bohr/alat 는 지원하지 않는다")
    cell = [[float(x) for x in l.split()[:3]]
            for l in t.split("CELL_PARAMETERS")[1].splitlines()[1:4]]
    phead = t.split("ATOMIC_POSITIONS")[1].splitlines()[0].lower()
    if "angstrom" not in phead and "crystal" not in phead:
        raise ValueError(f"{path}: ATOMIC_POSITIONS 단위 {phead.strip()} 는 지원하지 않는다")
    inv = inv3(cell)
    labels, frac = [], []
    for line in t.split("ATOMIC_POSITIONS")[1].splitlines()[1:]:
        v = line.split()
        if len(v) < 4 or not re.fullmatch(r"[A-Z][a-zA-Z]*\d*", v[0]):
            break
        try:
            xyz = [float(x) for x in v[1:4]]
        except ValueError:
            break
        labels.append(v[0])
        frac.append(xyz if "crystal" in phead else vecmat(xyz, inv))
    if not labels:
        raise ValueError(f"{path}: ATOMIC_POSITIONS 를 한 줄도 못 읽었다")
    # ★ 부호를 추론하지 않는다 — QE 입력이 직접 정의한다 (2026-08-12 Codex Q1).
    #   ATOMIC_SPECIES 의 **순서**가 starting_magnetization(i) 의 i 다.
    spec_order = []
    if "ATOMIC_SPECIES" in t:
        for line in t.split("ATOMIC_SPECIES")[1].splitlines()[1:]:
            v = line.split()
            if len(v) < 3 or not re.fullmatch(r"[A-Z][a-zA-Z]*\d*", v[0]):
                break
            spec_order.append(v[0])
    smag = {}
    for m in re.finditer(r"starting_magnetization\s*\(\s*(\d+)\s*\)\s*=\s*(-?[\d.eE+]+)", t):
        i = int(m.group(1))
        if 1 <= i <= len(spec_order):
            smag[spec_order[i - 1]] = float(m.group(2))
    return {"cell": cell, "labels": labels, "frac": frac,
            "species_order": spec_order, "starting_magnetization": smag}


def parse_poscar(path) -> dict:
    """POSCAR/CONTCAR → {cell, syms, frac}. Selective/Direct/Cartesian 지원.

    ⚠ 이 슬랩 파일은 종 헤더가 `Li Ni O` × 48 로 **반복**된다 (원자가 원소별로 안
      묶여 있다). counts 와 zip 해서 그대로 펼쳐야 원자 순서가 보존된다.
    """
    L = Path(path).read_text(errors="ignore").splitlines()
    scale = float(L[1].split()[0])
    cell = [[float(x) * scale for x in L[i].split()[:3]] for i in (2, 3, 4)]
    i = 5
    species = None
    if not re.fullmatch(r"-?\d+", L[i].split()[0]):
        species = L[i].split()
        i += 1
    counts = [int(x) for x in L[i].split()]
    i += 1
    if species is None:
        raise ValueError(f"{path}: 종 이름 줄이 없다 (VASP4 형식은 지원하지 않는다)")
    if len(species) != len(counts):
        raise ValueError(f"{path}: 종 {len(species)}개 vs 개수 {len(counts)}개 — 헤더 불일치")
    syms = [s for s, c in zip(species, counts) for _ in range(c)]
    if L[i].strip() and L[i].strip()[0] in "Ss":
        i += 1
    direct = bool(L[i].strip()) and L[i].strip()[0] in "Dd"
    i += 1
    inv = inv3(cell)
    frac = []
    for k in range(len(syms)):
        xyz = [float(x) for x in L[i + k].split()[:3]]
        frac.append(xyz if direct else vecmat(xyz, inv))
    return {"cell": cell, "syms": syms, "frac": frac}


# ── 원장 ────────────────────────────────────────────────────────────────────
def supercell_matrix(small, big, tol=1e-4):
    """big = M · small 의 M. 정수가 아니면 예외 — 추정하지 않는다."""
    M = matmul(big, inv3(small))
    for row in M:
        for x in row:
            if abs(x - round(x)) > tol:
                raise ValueError(f"슈퍼셀 행렬이 정수가 아니다 — 같은 격자가 아니다:\n"
                                 f"  M = {[[round(y, 4) for y in r] for r in M]}")
    return [[int(round(x)) for x in row] for row in M]


def _mic_A(fa, fb, cell):
    """분수좌표 차 → 최소이미지 거리 [Å]. 27개 이웃 이미지를 실제로 훑는다."""
    d = [fa[k] - fb[k] for k in range(3)]
    d = [x - math.floor(x + 0.5) for x in d]
    best = None
    for u in (-1, 0, 1):
        for v in (-1, 0, 1):
            for w in (-1, 0, 1):
                dd = [d[0] + u, d[1] + v, d[2] + w]
                c = vecmat(dd, cell)
                r = math.sqrt(sum(x * x for x in c))
                best = r if best is None or r < best else best
    return best


def build_ledger(qe: dict, slab: dict, element="Ni", tol=MATCH_TOL_A,
                 margin_min=MARGIN_MIN_A) -> dict:
    """슬랩 원자 인덱스 → 부격자 라벨. 게이트를 통과하지 못하면 ValueError."""
    M = supercell_matrix(qe["cell"], slab["cell"])
    nrep = abs(round(det3([[float(x) for x in r] for r in M])))
    ref = [(f, l) for f, l in zip(qe["frac"], qe["labels"])
           if l.startswith(element)]
    if not ref:
        raise ValueError(f"QE 입력에 {element}* 라벨이 없다")
    sub_names = sorted({l for _f, l in ref})
    # 부호 = QE starting_magnetization 의 부호. 없으면 하드코딩 계보로 후퇴하되 기록한다.
    smag = qe.get("starting_magnetization") or {}
    have = {n: smag[n] for n in sub_names if n in smag and abs(smag[n]) > 1e-12}
    if len(have) == len(sub_names):
        sign_map = {n: (1.0 if v > 0 else -1.0) for n, v in have.items()}
        sign_src = {n: f"starting_magnetization={v:+g}" for n, v in have.items()}
    else:
        missing = [n for n in sub_names if n not in have]
        sign_map = {n: SIGN[n] for n in sub_names if n in SIGN}
        if len(sign_map) != len(sub_names):
            raise ValueError(f"{missing} 의 starting_magnetization 이 없고 SIGN 계보에도 "
                             f"없다 — 부호를 추측하지 않는다")
        sign_src = {n: "하드코딩 계보(SIGN) — QE 에 starting_magnetization 없음"
                    for n in sign_map}
    if len(set(sign_map.values())) < 2 and len(sub_names) > 1:
        raise ValueError(f"부격자 부호가 전부 같다 {sign_map} — AFM 이 아니다")

    # 슬랩 원자를 QE 셀 분수좌표로 접는다: frac_qe = frac_slab · M
    rows, worst, thin = [], 0.0, None
    use = [0] * len(ref)                       # QE 자리별 사용 횟수
    for i, s in enumerate(slab["syms"]):
        if s != element:
            continue
        fq = vecmat(slab["frac"][i], [[float(x) for x in r] for r in M])
        ds = sorted((_mic_A(fq, f, qe["cell"]), k) for k, (f, _l) in enumerate(ref))
        r0, k0 = ds[0]
        margin = (ds[1][0] - r0) if len(ds) > 1 else float("inf")
        thin = margin if thin is None else min(thin, margin)
        worst = max(worst, r0)
        if r0 <= tol:
            use[k0] += 1
        rows.append({"slab_index": i, "sublattice": ref[k0][1] if r0 <= tol else None,
                     "residual_A": round(r0, 4), "margin_A": round(margin, 4)})

    bad = [r for r in rows if r["sublattice"] is None]
    if bad:
        raise ValueError(
            f"{len(bad)}개 {element} 가 QE 자리와 {tol} Å 안에서 안 맞는다 "
            f"(최대 잔차 {worst:.3f} Å) — 슈퍼셀 관계나 구조가 다르다. 추정하지 않는다.\n"
            f"  예: 슬랩 인덱스 {[r['slab_index'] for r in bad[:6]]}")
    counts = {n: sum(1 for r in rows if r["sublattice"] == n) for n in sub_names}
    if len(sub_names) == 2 and len(set(counts.values())) != 1:
        raise ValueError(f"부격자 개수가 안 맞는다 {counts} — AFM 이 성립하지 않는다")
    if len(rows) != nrep * len(ref):
        raise ValueError(f"{element} 개수 {len(rows)} ≠ QE {len(ref)} × 슈퍼셀 {nrep}")
    # ★ 총개수만 맞으면 통과하던 구멍 (2026-08-12 Codex) — 같은 QE 자리를 두 번 쓰고
    #   다른 자리를 놓쳐도 Ni1/Ni2 합계는 맞을 수 있다. 자리별 사용 횟수를 못 박는다.
    off = {ref[k][1] + f"#{k}": u for k, u in enumerate(use) if u != nrep}
    if off:
        raise ValueError(f"QE 자리별 사용 횟수가 슈퍼셀 배수({nrep})와 다르다 {off} — "
                         f"어떤 자리는 중복 배정되고 어떤 자리는 비었다")
    # ★ 최근접과 차순위의 간격이 좁으면 배정이 흔들린다 — 잔차만으로는 못 잡는다.
    if thin is not None and thin < margin_min:
        raise ValueError(f"최근접-차순위 간격 최소 {thin:.3f} Å < {margin_min} — "
                         f"자리 배정이 애매하다. tol 을 줄이거나 구조를 확인할 것")

    sign = [0.0] * len(slab["syms"])
    for r in rows:
        sign[r["slab_index"]] = sign_map.get(r["sublattice"], 0.0)
    net = sum(sign)
    return {"element": element, "supercell_matrix": M, "n_replicas": nrep,
            "counts": counts, "max_residual_A": round(worst, 4),
            "min_second_nearest_margin_A": None if thin is None else round(thin, 4),
            "qe_site_usage": {ref[k][1] + f"#{k}": u for k, u in enumerate(use)},
            "sign_convention": sign_map, "sign_source": sign_src,
            "net_moment_muB": round(net, 6),
            "sign_by_slab_index": {str(r["slab_index"]): SIGN[r["sublattice"]]
                                   for r in rows},
            "rows": rows}


def block_halves_agreement(ledger: dict) -> dict:
    """'Ni 를 파일 순서로 앞 절반 −1 / 뒤 절반 +1' 이 실제 부격자와 얼마나 맞나.

    이 함수가 이 도구를 만든 이유다 — 옛 seed 가 맞았는지 **수치로** 남긴다.
    """
    rows = ledger["rows"]
    half = len(rows) // 2
    naive = [-1.0] * half + [1.0] * (len(rows) - half)
    real = [SIGN[r["sublattice"]] for r in rows]
    agree = sum(1 for a, b in zip(naive, real) if a == b)
    return {"n": len(rows), "agree": agree,
            "agree_flipped": len(rows) - agree,
            "verdict": ("동일" if agree == len(rows) or agree == 0
                        else "다른 자기 topology")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qe", default=str(QE_DEFAULT))
    ap.add_argument("--slab", default=str(SLAB_DEFAULT))
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--element", default="Ni")
    ap.add_argument("--tol", type=float, default=MATCH_TOL_A)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    qe = parse_qe(a.qe)
    slab = parse_poscar(a.slab)
    led = build_ledger(qe, slab, a.element, a.tol)
    led["source_qe"] = str(a.qe)
    led["source_slab"] = str(a.slab)
    led["qe_sublattice_order"] = [l for l in qe["labels"] if l.startswith(a.element)]
    cmp_ = block_halves_agreement(led)
    led["naive_block_halves"] = cmp_

    print(f"QE {a.qe}")
    print(f"  {a.element} 라벨 순서: {' '.join(led['qe_sublattice_order'])}")
    print(f"슬랩 {a.slab}")
    print(f"  슈퍼셀 M = {led['supercell_matrix']} (×{led['n_replicas']})")
    print(f"  매칭 {len(led['rows'])}개 · 최대 잔차 {led['max_residual_A']} Å · "
          f"{led['counts']}")
    print(f"  net moment {led['net_moment_muB']:+.1f} μB  "
          f"(부호 규약 {led['sign_convention']})")
    print(f"\n옛 seed(파일 순서 앞 절반 −1 / 뒤 절반 +1) 대조: "
          f"{cmp_['agree']}/{cmp_['n']} 일치 · 뒤집으면 {cmp_['agree_flipped']}/{cmp_['n']}"
          f"  → **{cmp_['verdict']}**")
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(led, indent=1, ensure_ascii=False))
    print(f"\n→ {a.out}")
    return 0


# ── selftest ────────────────────────────────────────────────────────────────
def _fake(tmp, cell, atoms, kind):
    """atoms = [(label, fx, fy, fz)]. kind 'qe' | 'poscar' → 파일 경로."""
    p = Path(tmp) / (kind + ".in" if kind == "qe" else "POSCAR")
    if kind == "qe":
        L = ["CELL_PARAMETERS angstrom"]
        L += ["  " + "  ".join(f"{x:.10f}" for x in r) for r in cell]
        L += ["", "ATOMIC_POSITIONS crystal"]
        L += [f"  {a[0]}  {a[1]:.10f}  {a[2]:.10f}  {a[3]:.10f}" for a in atoms]
        L += ["K_POINTS automatic", " 1 1 1 0 0 0"]
    else:
        L = ["fake", "1.0"]
        L += ["  " + "  ".join(f"{x:.10f}" for x in r) for r in cell]
        L += ["  " + "  ".join(a[0] for a in atoms),
              "  " + "  ".join("1" for _ in atoms), "Direct"]
        L += [f"  {a[1]:.10f}  {a[2]:.10f}  {a[3]:.10f}" for a in atoms]
    p.write_text("\n".join(L) + "\n")
    return str(p)


def selftest() -> int:
    import tempfile
    td = tempfile.mkdtemp(prefix="afm_ledger_st_")
    ok = True

    def chk(cond, msg):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + msg)
        ok &= bool(cond)

    def fails(fn, needle, msg):
        try:
            fn()
        except (ValueError, ZeroDivisionError) as e:
            chk(needle in str(e), f"{msg} → 거부 ({str(e).splitlines()[0][:58]})")
            return
        chk(False, f"{msg} → **통과시켰다** (fail-open)")

    cq = [[4.0, 0, 0], [0, 4.0, 0], [0, 0, 12.0]]
    # 뒤섞인 부격자 — 블록이 아니다. 실제 QE 파일의 성격을 그대로 흉내낸다.
    qat = [("Ni2", 0.0, 0.0, 0.5), ("Ni1", 0.5, 0.0, 0.5),
           ("Ni1", 0.0, 0.5, 0.5), ("Ni2", 0.5, 0.5, 0.5), ("O", 0.25, 0.25, 0.3)]
    qp = _fake(td, cq, qat, "qe")
    qe = parse_qe(qp)
    chk([l for l in qe["labels"] if l.startswith("Ni")] == ["Ni2", "Ni1", "Ni1", "Ni2"],
        "QE 파서: Ni1/Ni2 라벨과 순서 보존")

    # 1×2×1 슈퍼셀을 만든다 (b 를 2배). 원자 순서는 일부러 뒤섞는다.
    cs = [[4.0, 0, 0], [0, 8.0, 0], [0, 0, 12.0]]
    sat = []
    for j in (0, 1):
        for lab, fx, fy, fz in qat:
            el = "Ni" if lab.startswith("Ni") else lab
            sat.append((el, fx, (fy + j) / 2.0, fz, lab))
    sat = [sat[i] for i in (7, 0, 3, 5, 1, 8, 2, 6, 4, 9)]      # 순서 섞기
    sp = _fake(td, cs, [(a[0], a[1], a[2], a[3]) for a in sat], "poscar")
    slab = parse_poscar(sp)
    led = build_ledger(qe, slab)
    got = {r["slab_index"]: r["sublattice"] for r in led["rows"]}
    want = {i: a[4] for i, a in enumerate(sat) if a[0] == "Ni"}
    chk(got == want, f"뒤섞인 순서에서도 부격자 정확 ({len(want)}개)")
    chk(led["net_moment_muB"] == 0.0 and led["counts"] == {"Ni1": 4, "Ni2": 4},
        f"AFM net 0 · 개수 균형 {led['counts']}")
    chk(led["max_residual_A"] < 1e-9, f"잔차 {led['max_residual_A']} Å")

    # 원장이 '앞 절반/뒤 절반' 과 실제로 다른지 — 이 도구의 존재 이유
    cmp_ = block_halves_agreement(led)
    chk(cmp_["verdict"] == "다른 자기 topology",
        f"뒤섞인 부격자 vs 앞절반/뒤절반 = {cmp_['agree']}/{cmp_['n']} → {cmp_['verdict']}")

    # ── 음성 경로 ──
    # N1: 정수 슈퍼셀이 아닌 셀
    bad_cell = [[4.0, 0, 0], [0, 7.3, 0], [0, 0, 12.0]]
    Path(td + "/n1").mkdir(parents=True, exist_ok=True)
    bp = _fake(td + "/n1", bad_cell, [(a[0], a[1], a[2], a[3]) for a in sat], "poscar")
    fails(lambda: build_ledger(qe, parse_poscar(bp)), "정수가 아니다",
          "N1 비정수 슈퍼셀")
    # N2: Ni 하나를 1.5 Å 옮긴다 → 모르는 자리는 추정하지 않고 실패
    Path(td + "/n2").mkdir(parents=True, exist_ok=True)
    moved = [list(a) for a in sat]
    k = next(i for i, a in enumerate(moved) if a[0] == "Ni")
    moved[k][1] += 1.5 / 4.0
    mp = _fake(td + "/n2", cs, [(a[0], a[1], a[2], a[3]) for a in moved], "poscar")
    fails(lambda: build_ledger(qe, parse_poscar(mp)), "안 맞는다", "N2 Ni 1.5 Å 이탈")
    # N3: 부격자 개수 불균형 (Ni2 하나를 Ni1 로 바꾼 QE)
    Path(td + "/n3").mkdir(parents=True, exist_ok=True)
    q3 = [("Ni1" if a[0] == "Ni2" and a[1] == 0.0 else a[0], a[1], a[2], a[3])
          for a in qat]
    qp3 = _fake(td + "/n3", cq, q3, "qe")
    fails(lambda: build_ledger(parse_qe(qp3), slab), "개수가 안 맞는다", "N3 부격자 3:1")
    # N4: 라벨이 아예 없는 QE
    Path(td + "/n4").mkdir(parents=True, exist_ok=True)
    qp4 = _fake(td + "/n4", cq, [("O", 0.25, 0.25, 0.3)], "qe")
    fails(lambda: build_ledger(parse_qe(qp4), slab), "라벨이 없다", "N4 Ni 라벨 없음")
    # 부호를 QE 에서 읽는 경로 (하드코딩 fallback 이 아니라)
    Path(td + "/sm").mkdir(parents=True, exist_ok=True)
    sm = Path(td + "/sm/qe.in")
    sm.write_text(Path(qp).read_text().replace(
        "CELL_PARAMETERS angstrom",
        "ATOMIC_SPECIES\n  Li 6.9 li.upf\n  Ni1 58.7 ni.upf\n  Ni2 58.7 ni.upf\n"
        "  O 16.0 o.upf\n  starting_magnetization(2) = +0.300\n"
        "  starting_magnetization(3) = -0.300\n\nCELL_PARAMETERS angstrom"))
    qsm = parse_qe(str(sm))
    chk(qsm["starting_magnetization"] == {"Ni1": 0.3, "Ni2": -0.3},
        f"QE starting_magnetization 파싱 {qsm['starting_magnetization']}")
    lsm = build_ledger(qsm, slab)
    chk(lsm["sign_convention"] == {"Ni1": 1.0, "Ni2": -1.0}
        and "starting_magnetization" in str(lsm["sign_source"]),
        f"부호를 QE 에서 회수 (하드코딩 아님) {lsm['sign_convention']}")
    # 음성: 두 부격자가 같은 부호면 AFM 이 아니다
    Path(td + "/sm2").mkdir(parents=True, exist_ok=True)
    sm2 = Path(td + "/sm2/qe.in")
    sm2.write_text(sm.read_text().replace("starting_magnetization(3) = -0.300",
                                          "starting_magnetization(3) = +0.300"))
    fails(lambda: build_ledger(parse_qe(str(sm2)), slab), "전부 같다",
          "N4d 두 부격자 같은 부호")
    # N4b: 같은 QE 자리를 두 번 쓰고 다른 자리를 비워도 **총개수는 맞는다** (Codex 2026-08-12)
    Path(td + "/n4b").mkdir(parents=True, exist_ok=True)
    dup = [list(a) for a in sat]
    k2 = next(i for i, a in enumerate(dup) if a[0] == "Ni" and a[4] == "Ni1"
              and abs(a[2] - 0.25) < 1e-9)          # ref#2 의 j=0 복제본
    dup[k2][1], dup[k2][2] = 0.5, 0.0               # ref#1 자리로 옮긴다 (Ni1 → Ni1)
    dp = _fake(td + "/n4b", cs, [(a[0], a[1], a[2], a[3]) for a in dup], "poscar")
    led_dup = None
    try:
        led_dup = build_ledger(qe, parse_poscar(dp))
    except ValueError as e:
        chk("사용 횟수" in str(e), f"N4b 자리 중복 배정 → 거부 ({str(e)[:52]})")
    if led_dup is not None:
        chk(False, f"N4b 자리 중복인데 통과 (counts={led_dup['counts']}) — 총개수만 본다")
    # N4c: 최근접과 차순위가 0.3 Å 밖에 안 떨어진 QE (잔차는 0 이라 tol 로는 못 잡는다)
    Path(td + "/n4c").mkdir(parents=True, exist_ok=True)
    cq2 = [[4.0, 0, 0], [0, 4.0, 0], [0, 0, 12.0]]
    q2 = [("Ni1", 0.0, 0.0, 0.5), ("Ni2", 0.075, 0.0, 0.5)]      # 0.3 Å 간격
    qp2 = _fake(td + "/n4c", cq2, q2, "qe")
    sp2 = _fake(td + "/n4c", cq2, [("Ni", 0.0, 0.0, 0.5), ("Ni", 0.075, 0.0, 0.5)], "poscar")
    fails(lambda: build_ledger(parse_qe(qp2), parse_poscar(sp2)), "간격",
          "N4c 최근접-차순위 0.3 Å")
    # N5: 지원하지 않는 단위를 조용히 넘기지 않는다
    Path(td + "/n5").mkdir(parents=True, exist_ok=True)
    p5 = Path(td + "/n5/bohr.in")
    p5.write_text(Path(qp).read_text().replace("CELL_PARAMETERS angstrom",
                                               "CELL_PARAMETERS bohr"))
    fails(lambda: parse_qe(str(p5)), "angstrom 이 아니다", "N5 bohr 단위")
    # N6: 종 헤더와 개수 줄 길이 불일치
    Path(td + "/n6").mkdir(parents=True, exist_ok=True)
    p6 = Path(td + "/n6/POSCAR")
    p6.write_text(Path(sp).read_text().replace("  1  1  1  1  1  1  1  1  1  1",
                                               "  1  1  1  1  1"))
    fails(lambda: parse_poscar(str(p6)), "헤더 불일치", "N6 종/개수 불일치")

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
