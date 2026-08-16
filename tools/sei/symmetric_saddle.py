#!/usr/bin/env python3
"""symmetric_saddle.py — **대칭 홉**의 장벽을 relax 2회로 얻는다 (full NEB 대체).

왜 (2026-08-16)
  li3nd c→c 의 셀 수렴을 확인하려면 3×3×3(107원자) 장벽이 필요하다. 그런데 full NEB 은
  이미지 7 × 스텝 ~80 ≈ **560 SCF** 다. 이 홉은 대칭이라 그럴 필요가 없다:

    · 양 끝점이 **대칭 동등**하면 안장점은 경로 중앙에 대칭으로 놓인다.
    · 실측 증거: 2×2×2 ccpath 에서 CI 가 값을 **1 μeV** 만 바꿨다
      (`no-CI 0.228980 → CI 0.228981`). 안장점이 이미 중점 이미지 위에 있었다는 뜻이다.

  → 중점에 뛰는 원자를 **고정**하고 나머지를 이완하면 그게 안장점이다.
    끝점 1 + 안장 1 = **2 relax**. 수십~수백 배 싸다.

⛔ 대칭이 아니면 쓰면 안 된다
  비대칭 홉(li3nd c→b 처럼 자리 종류가 다름)은 안장점이 중점에 없다. 두 근거 중
  하나가 있어야 통과하고, **어느 쪽으로 통과했는지 기록한다**:
    (a) `meta.endpoints_symmetry_equivalent = true` — spglib orbit 판정
    (b) **측정된 끝점 에너지 축퇴** |ΔE| ≤ 20 meV — 이완된 두 끝점 에너지가 같다
  (b) 를 넣은 이유: cc333 은 build 가 "끝점 미이완" 으로 조기 반환해 meta.json 이
  없는데, 재생성하면 `.ep_hash` 가 달라져 **이미 돌린 끝점 relax 를 버린다**.
  그리고 (b) 는 메타데이터가 아니라 실측이라 근거로 더 낫다.
  ⚠ (b) 는 **필요조건이지 충분조건이 아니다** — 대칭 비동등한 두 자리가 우연히 같은
  에너지일 수 있다. (b) 로만 통과하면 경고를 남긴다.

프로토콜 일치
  안장 입력은 `ep_initial/relax.in` 의 헤더(cell·k·q·smearing·PP·cutoff)를 **그대로
  복사**해 만든다. 다시 계산하지 않는다 — 그래야 두 에너지가 같은 규약이 된다.

  python3 tools/sei/symmetric_saddle.py --work /data/work/runs/sei_neb_v2_cc333 --tag li3nd
  python3 tools/sei/symmetric_saddle.py --work ... --tag li3nd --collect
  python3 tools/sei/symmetric_saddle.py --selftest

이 도구가 못 하는 것
  · 안장점을 **찾지** 않는다. 대칭으로 결정된 중점을 쓴다 — 대칭이 깨지면 틀린다.
  · 비대칭 홉·다중 안장 경로에 못 쓴다 (거부한다).
  · 경로 형상(반응좌표)을 주지 않는다. 장벽 높이 하나만 준다.
  · 이완 후 **수직 힘**은 보고만 한다 — 자동으로 판정하지 않는다.
  · 셀 수렴을 대신 해주지 않는다. 다른 셀에서 이 도구를 두 번 돌려 비교하는 것이 목적이다.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#: 끝점 에너지 축퇴 문턱 [eV] — 이보다 크면 대칭 홉으로 안 본다.
#:  0.229 eV 장벽 대비 20 meV 는 9% — 그 이상 어긋나면 중점이 안장점이라는 전제가 흔들린다.
ENDPOINT_TOL_EV = 0.020
#: 고정 대상 원자가 끝점 사이에서 움직여도 되는 한계 [Å] — 넘으면 Ea 오염 (리뷰 F2)
FROZEN_SHIFT_TOL_A = 0.05


def _pos_block(txt, start):
    """start 부터의 첫 ATOMIC_POSITIONS 블록 → [(sym,[x,y,z])] (angstrom 만)."""
    m = re.search(r"ATOMIC_POSITIONS\s*\(?(\w+)", txt[start:])
    if not m or m.group(1).lower() != "angstrom":
        return None
    s = start + m.end()
    rows = []
    for l in txt[s:].splitlines()[1:]:
        q = l.split()
        if len(q) >= 4 and re.match(r"^[A-Z][a-z]?\d*$", q[0]):
            rows.append((q[0], [float(q[1]), float(q[2]), float(q[3])]))
        elif rows:
            break
    return rows or None


def last_force(txt):
    """마지막 `Total force = X` [Ry/au]. 없으면 None."""
    f = re.findall(r"Total force\s*=\s*([\d.eE+-]+)", txt)
    return float(f[-1]) if f else None


def read_relaxed(outp, allow_unconverged=False):
    """이완 좌표를 읽는다 → (rows, err, info).

    ⚠ 2026-08-16 — 옛 판은 `Begin final coordinates` 만 봤다. 그런데 QE 는 BFGS 가
    **수렴했을 때만** 그 블록을 찍는다. cc333 끝점은 nstep 한도에서 끝나(16h41m)
    그 블록이 없고, 힘이 0.018 Ry/au (문턱 1e-3 의 **18배**) 에서 진동만 했다.
    그런 산출물을 조용히 '이완됨' 으로 쓰면 안 되고, 그렇다고 좌표가 없는 것도 아니다.
    → 마지막 BFGS 스텝의 ATOMIC_POSITIONS 로 후퇴하되 **미수렴을 명시**한다.
    """
    if not os.path.isfile(outp):
        return None, f"없음: {outp}", {}
    t = open(outp, encoding="utf-8", errors="replace").read()
    if "JOB DONE" not in t:
        return None, f"아직 안 끝났다 (JOB DONE 없음): {outp}", {}
    info = {"last_total_force_Ry_au": last_force(t),
            "max_steps_reached": "The maximum number of steps has been reached" in t}
    i = t.rfind("Begin final coordinates")
    if i >= 0:
        rows = _pos_block(t, i)
        info["converged"] = True
        if rows:
            return rows, None, info
    # ── 미수렴 후퇴 ──
    info["converged"] = False
    j = t.rfind("ATOMIC_POSITIONS")
    rows = _pos_block(t, j) if j >= 0 else None
    if rows is None:
        return None, f"좌표를 못 읽었다: {outp}", info
    if not allow_unconverged:
        return None, (f"⛔ 이완이 수렴하지 않았다: {outp}\n"
                      f"      마지막 Total force = {info['last_total_force_Ry_au']} Ry/au "
                      f"(= {(info['last_total_force_Ry_au'] or 0)*25.711:.2f} eV/Å)"
                      + (", nstep 한도 도달" if info["max_steps_reached"] else "") + "\n"
                      f"      좌표는 있다 — 미수렴을 감수하고 쓰려면 --allow_unconverged"), info
    return rows, None, info


def final_energy(outp):
    """relax.out 의 마지막 총에너지 [eV]. Ry → eV."""
    t = open(outp, encoding="utf-8", errors="replace").read()
    e = re.findall(r"^!\s+total energy\s+=\s+([-\d.]+)\s+Ry", t, re.M)
    return float(e[-1]) * 13.605693122994 if e else None


def parse_input_positions(relax_in):
    """relax.in 의 ATOMIC_POSITIONS (angstrom) → [(sym,[x,y,z])].

    ★ 왜 relax.**in** 인가 (2026-08-16): cc333 의 relax.**out** 은 미수렴 BFGS 가
    50스텝 밀어낸 표류 구조라 홉이 3.667 → 4.203 Å 로 벌어지고 이웃 하나가 1.24 Å
    움직였다. 반면 relax.in 은 이상 좌표(홉 3.667, 나머지 변위 0.000)로 깨끗하다.
    고정셸 방식은 여기서 새로 시작한다 — 표류를 승계하지 않는다.
    """
    txt = open(relax_in, encoding="utf-8").read()
    i = txt.index("ATOMIC_POSITIONS")
    return _pos_block(txt, i)


def parse_cell(relax_in):
    """relax.in 의 CELL_PARAMETERS angstrom → 3×3 리스트."""
    t = open(relax_in, encoding="utf-8").read()
    m = re.search(r"CELL_PARAMETERS\s*\(?angstrom\)?\s*\n((?:\s*[-\d.eE+]+\s+[-\d.eE+]+\s+[-\d.eE+]+\s*\n){3})", t)
    if not m:
        return None
    return [[float(x) for x in l.split()] for l in m.group(1).strip().splitlines()]


def min_image(d, cell):
    """최소이미지로 변위를 편다. cell 이 없으면 그대로 돌려준다."""
    if not cell:
        return d
    import itertools
    best, bn = d, sum(x * x for x in d)
    for n in itertools.product((-1, 0, 1), repeat=3):
        c = [d[k] + sum(n[j] * cell[j][k] for j in range(3)) for k in range(3)]
        nn = sum(x * x for x in c)
        if nn < bn:
            best, bn = c, nn
    return best


def _symmetry_gate(meta, ini_out, fin_out):
    """대칭 근거를 판정한다 → (basis, warn, |ΔE|, meta의 sym).

    ⛔ build 와 build_frozen 이 **같은 게이트**를 타야 한다. 리뷰 F1: 고정셸 경로가
    이 검사를 통째로 건너뛰어, 모듈 docstring 이 "거부한다" 고 적은 비대칭 홉이
    그냥 통과했다. 중점법의 전제(안장 = 중점)는 두 경로에 똑같이 필요하다.
    """
    sym = meta.get("endpoints_symmetry_equivalent")
    e1 = final_energy(ini_out) if os.path.isfile(ini_out) else None
    e2 = final_energy(fin_out) if os.path.isfile(fin_out) else None
    de = abs(e2 - e1) if (e1 is not None and e2 is not None) else None
    if sym is True:
        return "meta.endpoints_symmetry_equivalent=true (spglib orbit)", None, de, sym
    if de is not None and de <= ENDPOINT_TOL_EV:
        return (f"measured endpoint degeneracy |ΔE| = {de*1000:.1f} meV "
                f"≤ {ENDPOINT_TOL_EV*1000:.0f} meV",
                ("⚠ spglib 판정(meta)이 없어 **끝점 에너지 축퇴**로만 통과했다. 이는 필요조건이지 "
                 "충분조건이 아니다 — 같은 홉이 더 작은 셀에서 대칭 동등으로 확인됐는지 함께 볼 것."),
                de, sym)
    return None, None, de, sym


def _symmetry_refusal(tag, sym, de):
    return (f"⛔ {tag}: 대칭 근거가 없다 — 중점법을 쓸 수 없다.\n"
            f"   meta.endpoints_symmetry_equivalent = {sym!r}\n"
            f"   끝점 에너지 차 |ΔE| = "
            + (f"{de*1000:.1f} meV (> {ENDPOINT_TOL_EV*1000:.0f} meV 문턱)" if de is not None
               else "측정 불가") + "\n"
            f"   비대칭 홉은 안장점이 중점에 없다. full NEB 을 쓸 것.\n"
            f"   (정말 강행하려면 --force — 근거를 db 에 남길 것)")


def build(work, tag, force=False, allow_unconverged=False):
    d = os.path.join(work, tag)
    meta_p = os.path.join(d, "meta.json")
    meta = json.load(open(meta_p, encoding="utf-8")) if os.path.isfile(meta_p) else {}

    ini_out = os.path.join(d, "ep_initial", "relax.out")
    fin_out = os.path.join(d, "ep_final", "relax.out")
    ini_in = os.path.join(d, "ep_initial", "relax.in")
    first, e1, i1 = read_relaxed(ini_out, allow_unconverged)
    last, e2, i2 = read_relaxed(fin_out, allow_unconverged)
    if first is None or last is None:
        return 1, (f"⛔ {tag}: 이완된 끝점이 필요하다.\n   {e1 or ''}\n   {e2 or ''}\n"
                   f"   먼저: bash tools/sei/run_sei_neb.sh endpoints {tag}")
    unconv = [n for n, i in (("ep_initial", i1), ("ep_final", i2)) if not i.get("converged")]
    if [s for s, _ in first] != [s for s, _ in last]:
        return 1, f"⛔ {tag}: 두 끝점의 원자 목록이 다르다 — 같은 계가 아니다"

    basis, warn, de, sym = _symmetry_gate(meta, ini_out, fin_out)
    if basis is None and not force:
        return 1, _symmetry_refusal(tag, sym, de)
    if basis is None:
        basis = "⛔ --force (대칭 근거 없음)"

    cell = parse_cell(ini_in)
    # 뛰는 원자 = 두 끝점 사이 변위가 가장 큰 원자
    disp = [min_image([b[k] - a[k] for k in range(3)], cell)
            for (_, a), (_, b) in zip(first, last)]
    dn = [sum(x * x for x in v) ** 0.5 for v in disp]
    j = max(range(len(dn)), key=lambda i: dn[i])
    dmax = dn[j]
    others = sorted(dn)[-2] if len(dn) > 1 else 0.0
    if dmax < 0.5:
        return 1, (f"⛔ {tag}: 두 끝점이 사실상 같은 구조다 (최대 변위 {dmax:.3f} Å) — "
                   f"뛰는 원자가 없다")

    # 중점 구성: 모든 원자를 두 끝점의 중간으로 (= NEB 7이미지의 4번째와 같은 선형보간)
    mid = [(s, [first[i][1][k] + disp[i][k] / 2.0 for k in range(3)])
           for i, (s, _) in enumerate(first)]

    # ── 안장 입력: 끝점 relax.in 헤더를 **그대로** 쓴다 (프로토콜 일치 보장) ──
    src = open(ini_in, encoding="utf-8").read()
    head = src[:src.index("ATOMIC_POSITIONS")]
    tail_i = src.index("K_POINTS")
    tail = src[tail_i:]
    head = head.replace(f"prefix          = '{tag}_ep_initial'", f"prefix          = '{tag}_saddle'")
    lines = [head.rstrip("\n"), "", "ATOMIC_POSITIONS angstrom"]
    for i, (s, p) in enumerate(mid):
        # 뛰는 원자만 고정한다 (if_pos 0 0 0). 나머지는 자유 이완.
        fix = "  0 0 0" if i == j else ""
        lines.append(f"  {s:3s} %16.10f %16.10f %16.10f{fix}" % tuple(p))
    lines += ["", tail.rstrip("\n")]

    sd = os.path.join(d, "saddle")
    os.makedirs(sd, exist_ok=True)
    open(os.path.join(sd, "relax.in"), "w").write("\n".join(lines) + "\n")
    json.dump({
        "tag": tag, "work": work,
        "method": ("대칭 홉 중점 구속 이완. 뛰는 원자를 두 끝점의 중점에 if_pos=0 0 0 으로 "
                   "고정하고 나머지를 이완한다. 프로토콜은 ep_initial/relax.in 헤더를 그대로 복사."),
        "moving_atom_index_0based": j, "moving_atom_symbol": mid[j][0],
        "hop_distance_A": round(dmax, 4),
        "second_largest_displacement_A": round(others, 4),
        "endpoints_symmetry_equivalent": sym,
        "symmetry_basis": basis,
        "endpoints_converged": not unconv,
        "unconverged_endpoints": unconv,
        "endpoint_last_force_Ry_au": {"ep_initial": i1.get("last_total_force_Ry_au"),
                                      "ep_final": i2.get("last_total_force_Ry_au")},
        "endpoint_energy_diff_eV": (round(de, 6) if de is not None else None),
        "symmetry_warning": warn,
        "supercell": meta.get("supercell"), "min_cell_A": meta.get("min_cell_A"),
        "protocol_hash_of_endpoint": meta.get("protocol_hash"),
        "limitations": [
            "안장점을 찾지 않는다 — 대칭으로 결정된 중점을 쓴다",
            "대칭이 깨지면 틀린다. 이완 후 수직 힘을 확인할 것",
            "장벽 높이만 준다 (경로 형상 없음)",
        ],
    }, open(os.path.join(sd, "saddle_meta.json"), "w"), ensure_ascii=False, indent=1)

    return 0, (f"✓ {tag}: 안장 입력 생성 → {sd}/relax.in\n"
               f"   뛰는 원자 #{j} {mid[j][0]} · 홉 {dmax:.3f} Å "
               f"(다음으로 큰 변위 {others:.3f} Å)\n"
               + ((f"   ⛔ 끝점 미수렴: {' · '.join(unconv)} — "
                   f"마지막 힘 {i1.get('last_total_force_Ry_au')}/{i2.get('last_total_force_Ry_au')} Ry/au "
                   f"(문턱 1e-3). 장벽이 그만큼 오염된다\n") if unconv else "")
               + f"   대칭 근거: {basis}\n"
               + (f"   {warn}\n" if warn else "")
               + f"   셀 {meta.get('supercell')} · 최소변 {meta.get('min_cell_A')} Å\n"
               f"   실행:  cd {sd} && mpirun -np <N> pw.x -in relax.in > relax.out")


def collect(work, tag, radius=None, allow_unconverged=False):
    d = os.path.join(work, tag)
    if radius:
        base = os.path.join(d, f"frozen_R{radius:g}")
        ep = os.path.join(base, "endpoint", "relax.out")
        sd = os.path.join(base, "saddle", "relax.out")
    else:
        ep = os.path.join(d, "ep_initial", "relax.out")
        sd = os.path.join(d, "saddle", "relax.out")
    for p in (ep, sd):
        if not os.path.isfile(p):
            return 1, f"⛔ 없음: {p}"
    # ⛔ 리뷰 F5 — 옛 판은 JOB DONE 도 수렴도 안 봤다. 아직 도는 중인 relax.out 에서
    #   깔끔한 Ea 가 나왔다(실측 재현). 에너지 줄이 있으면 무조건 읽었기 때문이다.
    bad = []
    for name, p in (("endpoint", ep), ("saddle", sd)):
        txt = open(p, encoding="utf-8", errors="replace").read()
        if "JOB DONE" not in txt:
            bad.append(f"{name}: 아직 안 끝났다 (JOB DONE 없음)")
            continue
        if "Begin final coordinates" not in txt:
            f = last_force(txt)
            bad.append(f"{name}: 이완 미수렴 (마지막 힘 {f} Ry/au"
                       + (f" = {f*25.711:.2f} eV/Å" if f else "") + ")")
    if bad and not allow_unconverged:
        return 1, ("⛔ 회수 거부 — 아래를 감수하려면 --allow_unconverged:\n   "
                   + "\n   ".join(bad))
    e_end, e_sad = final_energy(ep), final_energy(sd)
    if e_end is None or e_sad is None:
        return 1, "⛔ 총에너지를 못 읽었다"
    ea = e_sad - e_end
    # 구속 원자에 남은 힘 — 대칭이 지켜졌는지의 지표 (판정은 사람이)
    t = open(sd, encoding="utf-8", errors="replace").read()
    fm = re.findall(r"Total force =\s+([\d.eE+-]+)", t)
    meta = {}
    mp = (os.path.join(d, f"frozen_R{radius:g}", "frozen_meta.json") if radius
          else os.path.join(d, "saddle", "saddle_meta.json"))
    if os.path.isfile(mp):
        meta = json.load(open(mp, encoding="utf-8"))
    out = {
        "tag": tag, "root": os.path.basename(work.rstrip("/")),
        "Ea_eV": round(ea, 6), "E_endpoint_eV": round(e_end, 6), "E_saddle_eV": round(e_sad, 6),
        "total_force_last_Ry_au": float(fm[-1]) if fm else None,
        "method": ("frozen-shell symmetric-midpoint" if radius
                   else "symmetric-midpoint constrained relax (2 SCF relaxations, not NEB)"),
        "relax_radius_A": radius,
        "supercell": meta.get("supercell"), "min_cell_A": meta.get("min_cell_A"),
        "converged": not bad,
        "convergence_notes": bad,
        "caveat": ("대칭 홉 전제. 절대값 인용 전에 다른 셀에서 같은 방법으로 한 번 더 재고 "
                   "차이를 볼 것 — 이 도구의 용도가 그 비교다."),
    }
    return 0, ((f"⚠ {' · '.join(bad)}\n" if bad else "")
               + f"{tag} ({out['root']}, 셀 {out['supercell']}, 최소변 {out['min_cell_A']} Å)\n"
               f"  E_endpoint = {e_end:.6f} eV\n"
               f"  E_saddle   = {e_sad:.6f} eV\n"
               f"  ── Ea      = {ea:.4f} eV ──\n"
               f"  마지막 Total force = {out['total_force_last_Ry_au']} (Ry/au) "
               f"— 구속점이 대칭점이면 작아야 한다\n"
               f"  JSON: {json.dumps(out, ensure_ascii=False)}")


def build_frozen(work, tag, radius, force=False):
    """고정셸 방식: 원거리 원자를 묶고 공공 주변만 이완한다.

    왜 (2026-08-16)
      3×3×3 은 107원자 = **자유도 321** 이라 nstep 50 으로 못 끝났다(16h41m, 잔여 힘
      0.018 Ry/au = 문턱의 18배). 전이완을 끝내려면 GPU 8~12일이다.
      그런데 우리가 재려는 건 **이미지 상호작용의 셀 의존성**이고, 공공에서 먼 원자는
      두 셀 모두 이상 격자 위치에 있어 사실상 같다. 그 원자를 고정하면 자유도가
      크게 줄어 BFGS 가 빨리 끝난다.

    ⛔ 반드시 지킬 것
      · 끝점과 안장에 **같은 중심·같은 반경·같은 자유 원자 집합**을 쓴다.
        (다르면 E 차에 프로토콜 차이가 섞인다)
      · 2×2×2 대조군도 **같은 규약**으로 다시 잰다. 전이완 0.229 와 직접 비교하지 않는다.
      · 반경이 셀 수직 폭의 절반을 넘으면 자유영역이 자기 이미지와 닿아 의미가 없다 — 거부한다.

    산출: <tag>/frozen_R<r>/{endpoint,saddle}/relax.in  (+ frozen_meta.json)
    """
    d = os.path.join(work, tag)
    ini_in = os.path.join(d, "ep_initial", "relax.in")
    fin_in = os.path.join(d, "ep_final", "relax.in")
    for f in (ini_in, fin_in):
        if not os.path.isfile(f):
            return 1, f"⛔ 없음: {f} — build_neb_inputs.py 로 끝점 입력부터 만들 것"

    # ⛔ 리뷰 F1 — build 와 **같은** 대칭 게이트를 탄다 (중점=안장 전제가 동일하므로)
    meta_p = os.path.join(d, "meta.json")
    meta = json.load(open(meta_p, encoding="utf-8")) if os.path.isfile(meta_p) else {}
    basis, warn, de, sym = _symmetry_gate(
        meta, os.path.join(d, "ep_initial", "relax.out"),
        os.path.join(d, "ep_final", "relax.out"))
    if basis is None and not force:
        return 1, _symmetry_refusal(tag, sym, de)
    if basis is None:
        basis = "⛔ --force (대칭 근거 없음)"

    first = parse_input_positions(ini_in)
    last = parse_input_positions(fin_in)
    if not first or not last or len(first) != len(last):
        return 1, "⛔ relax.in 의 ATOMIC_POSITIONS 를 못 읽었다 (또는 원자 수가 다르다)"
    if [s for s, _ in first] != [s for s, _ in last]:
        return 1, "⛔ 두 끝점의 원자 목록이 다르다"

    cell = parse_cell(ini_in)
    if cell is None:
        return 1, "⛔ CELL_PARAMETERS 를 못 읽었다"
    import math
    V = abs(_det3(cell))
    widths = [V / _norm(_cross(cell[(i + 1) % 3], cell[(i + 2) % 3])) for i in range(3)]
    dmin = min(widths)
    if radius > dmin / 2.0 and not force:
        return 1, (f"⛔ 반경 {radius} Å 이 셀 최소 수직폭의 절반({dmin/2:.2f} Å)을 넘는다 — "
                   f"자유영역이 자기 이미지와 닿아 고정의 의미가 없다.\n"
                   f"   수직폭 {[round(x,2) for x in widths]} Å. --force 로 강행 가능")

    disp = [min_image([b[k] - a[k] for k in range(3)], cell)
            for (_, a), (_, b) in zip(first, last)]
    dn = [math.sqrt(sum(x * x for x in v)) for v in disp]
    j = max(range(len(dn)), key=lambda i: dn[i])
    dmax = dn[j]
    others = sorted(dn)[-2] if len(dn) > 1 else 0.0
    if dmax < 0.5:
        return 1, f"⛔ 두 끝점이 같은 구조다 (최대 변위 {dmax:.3f} Å)"
    if others > 0.3 * dmax and not force:
        return 1, (f"⛔ 뛰는 원자 외에도 크게 움직인다 (2위 변위 {others:.3f} Å > 홉 {dmax:.3f} 의 30%) "
                   f"— 단일 홉 입력이 아니다. --force 로 강행 가능")

    # 중심 = 홉 중점 (끝점·안장 **공통**)
    ctr = [first[j][1][k] + disp[j][k] / 2.0 for k in range(3)]
    freeze = []
    for i, (s, p) in enumerate(first):
        v = min_image([p[k] - ctr[k] for k in range(3)], cell)
        freeze.append(math.sqrt(sum(x * x for x in v)) > radius)
    freeze[j] = False                      # 뛰는 원자는 항상 자유(안장에선 좌표 고정)
    n_free = sum(1 for f in freeze if not f)
    if n_free < 8 and not force:
        return 1, (f"⛔ 자유 원자가 {n_free}개뿐이다 — 반경 {radius} Å 이 너무 작다. "
                   f"--relax_radius 를 키울 것")

    src = open(ini_in, encoding="utf-8").read()
    head = src[:src.index("ATOMIC_POSITIONS")]
    tail = src[src.index("K_POINTS"):]
    outd = os.path.join(d, f"frozen_R{radius:g}")

    mid = [(s, [first[i][1][k] + disp[i][k] / 2.0 for k in range(3)])
           for i, (s, _) in enumerate(first)]

    # ⛔⛔ 리뷰 F2 — 고정 원자는 **두 파일에서 같은 좌표**여야 한다.
    #   옛 판은 끝점에 first[i], 안장에 mid[i] 를 썼다. 변위가 0 이 아닌 원거리 원자는
    #   두 계산에서 서로 다른 위치에 못박히고, 이완으로 풀 수도 없으니 그 차이가
    #   **그대로 Ea 에 들어간다**. 실측 재현: 0.4 Å 강체 오프셋이 게이트를 통과했다.
    #   → 고정 원자는 양쪽 다 mid[i] 를 쓴다(= 두 끝점의 평균, 대칭점).
    frozen_shift = max((dn[i] for i in range(len(dn)) if freeze[i]), default=0.0)
    if frozen_shift > FROZEN_SHIFT_TOL_A and not force:
        return 1, (f"⛔ 고정 대상 원자가 끝점 사이에서 {frozen_shift:.3f} Å 움직인다 "
                   f"(문턱 {FROZEN_SHIFT_TOL_A} Å) — 국소 홉이 아니거나 반경이 너무 작다.\n"
                   f"   고정 원자를 한 좌표에 못박으면 그 차이가 Ea 에 직접 들어간다. "
                   f"--relax_radius 를 키울 것 (--force 로 강행 가능)")

    def emit(sub, rows, fix_moving):
        os.makedirs(os.path.join(outd, sub), exist_ok=True)
        h = head.replace(f"prefix          = '{tag}_ep_initial'",
                         f"prefix          = '{tag}_frozen_{sub}'")
        L = [h.rstrip("\n"), "", "ATOMIC_POSITIONS angstrom"]
        for i, (s, p) in enumerate(rows):
            frz = freeze[i]
            # 고정 원자는 **양쪽 동일 좌표**(mid) · 자유 원자는 각 상태의 좌표
            pos = mid[i][1] if frz else p
            fx = "  0 0 0" if (frz or (fix_moving and i == j)) else ""
            L.append(f"  {s:3s} %16.10f %16.10f %16.10f{fx}" % tuple(pos))
        L += ["", tail.rstrip("\n")]
        open(os.path.join(outd, sub, "relax.in"), "w").write("\n".join(L) + "\n")
    emit("endpoint", first, fix_moving=False)
    emit("saddle", mid, fix_moving=True)

    meta = {
        "tag": tag, "work": work, "method": "frozen-shell symmetric-midpoint",
        "relax_radius_A": radius, "freeze_center_xyz": [round(x, 6) for x in ctr],
        "n_atoms": len(first), "n_free": n_free, "n_frozen": len(first) - n_free,
        "dof_free": 3 * n_free, "dof_total": 3 * len(first),
        "moving_atom_index_0based": j, "moving_atom_symbol": first[j][0],
        "hop_distance_A": round(dmax, 4), "second_largest_displacement_A": round(others, 4),
        "cell_perp_widths_A": [round(x, 3) for x in widths],
        "min_perp_width_A": round(dmin, 3),
        "cell_vector_lengths_A": [round(_norm(v), 3) for v in cell],
        "supercell": meta.get("supercell"),
        "min_cell_A": meta.get("min_cell_A"),
        "symmetry_basis": basis,
        "symmetry_warning": warn,
        "endpoint_energy_diff_eV": (round(de, 6) if de is not None else None),
        "max_frozen_atom_shift_A": round(frozen_shift, 4),
        "started_from": "relax.in (ideal) — relax.out 의 표류 구조를 승계하지 않는다",
        "contract": ("끝점과 안장이 **같은 중심·반경·자유집합**을 쓴다. "
                     "다른 셀과 비교하려면 그 셀도 같은 radius 로 이 도구를 돌릴 것. "
                     "전이완 값(예: 2×2×2 의 0.229)과 직접 비교하지 말 것 — 프로토콜이 다르다."),
        "limitations": ["원거리 이완을 버린다 — 절대 장벽은 전이완보다 약간 높게 나온다",
                        "그 편향은 두 셀에서 같은 방향이라 **차이**에는 대부분 상쇄된다",
                        "대칭 홉 전제 (안장 = 중점)"],
    }
    json.dump(meta, open(os.path.join(outd, "frozen_meta.json"), "w"),
              ensure_ascii=False, indent=1)
    return 0, (f"✓ {tag}: 고정셸 입력 생성 → {outd}/\n"
               f"   반경 {radius} Å · 자유 {n_free}/{len(first)}원자 "
               f"(자유도 {3*n_free} / {3*len(first)}, {100*n_free/len(first):.0f}%)\n"
               f"   중심 = 홉 중점 · 홉 {dmax:.3f} Å (2위 변위 {others:.3f}) · "
               f"고정원자 최대 이동 {frozen_shift:.3f} Å\n"
               f"   셀 수직폭 {[round(x,1) for x in widths]} Å (최소 {dmin:.2f}) · "
               f"슈퍼셀 {meta.get('supercell')} · 대칭근거 {basis}\n"
               f"   ⚠ 끝점·안장이 같은 자유집합을 쓴다. **다른 셀도 같은 radius 로** 돌릴 것.\n"
               f"   실행 (순서대로, 같은 노드):\n"
               f"     cd {outd}/endpoint && mpirun -np <N> pw.x -in relax.in > relax.out\n"
               f"     cd {outd}/saddle   && mpirun -np <N> pw.x -in relax.in > relax.out\n"
               f"   회수:  python3 tools/sei/symmetric_saddle.py --work {work} --tag {tag} "
               f"--collect --relax_radius {radius:g}")


def _cross(a, b):
    return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]


def _norm(v):
    return sum(x*x for x in v) ** 0.5


def _det3(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            - m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            + m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def selftest():
    import shutil
    import tempfile
    td = tempfile.mkdtemp(prefix="symsaddle_st_")
    ok = True

    def chk(c, m):
        nonlocal ok
        ok &= bool(c)
        print(f"  {'✓' if c else '✗'} {m}")

    def mk(tag, sym, ini, fin, cell=None):
        d = os.path.join(td, tag)
        for n in ("ep_initial", "ep_final"):
            os.makedirs(os.path.join(d, n), exist_ok=True)
        json.dump({"endpoints_symmetry_equivalent": sym, "supercell": [3, 3, 3],
                   "min_cell_A": 15.56, "protocol_hash": "deadbeef"},
                  open(os.path.join(d, "meta.json"), "w"))
        c = cell or [[15.0, 0, 0], [0, 15.0, 0], [0, 0, 15.0]]
        hdr = ("&CONTROL\n    calculation     = 'relax'\n"
               f"    prefix          = '{tag}_ep_initial'\n/\n"
               "&SYSTEM\n    ibrav           = 0\n    tot_charge      = 0.0\n/\n\n"
               "ATOMIC_SPECIES\n  Li 6.94 li.UPF\n\n")
        for n, rows in (("ep_initial", ini), ("ep_final", fin)):
            p = os.path.join(d, n)
            body = "ATOMIC_POSITIONS angstrom\n" + "".join(
                f"  {s:3s} {x:16.10f} {y:16.10f} {z:16.10f}\n" for s, (x, y, z) in rows)
            k = "K_POINTS automatic\n  2 2 2 0 0 0\n\nCELL_PARAMETERS angstrom\n" + \
                "".join("  %16.10f %16.10f %16.10f\n" % tuple(v) for v in c)
            open(os.path.join(p, "relax.in"), "w").write(hdr + body + "\n" + k)
            open(os.path.join(p, "relax.out"), "w").write(
                "Begin final coordinates\n" + body + "End final coordinates\n"
                "!    total energy              =    -100.0000 Ry\nJOB DONE.\n")
        return d

    A = [("Li", (0.0, 0.0, 0.0)), ("Li", (5.0, 0.0, 0.0)), ("Li", (0.0, 5.0, 0.0))]
    B = [("Li", (3.667, 0.0, 0.0)), ("Li", (5.0, 0.0, 0.0)), ("Li", (0.0, 5.0, 0.0))]

    # 양성 — 대칭 홉
    mk("good", True, A, B)
    rc, msg = build(td, "good")
    chk(rc == 0, "대칭 홉이면 안장 입력을 만든다")
    sp = os.path.join(td, "good", "saddle", "relax.in")
    chk(os.path.isfile(sp), "saddle/relax.in 이 생긴다")
    txt = open(sp).read()
    chk(txt.count("  0 0 0") == 1, "[핵심] 구속(if_pos)이 **정확히 한 원자**에만 붙는다")
    chk("1.8335000000" in txt.replace(" ", " "), "뛰는 원자가 중점(3.667/2=1.8335)에 놓인다")
    chk("CELL_PARAMETERS" in txt and "K_POINTS" in txt, "셀·k 가 끝점 입력에서 승계된다")
    chk("'good_saddle'" in txt, "prefix 가 안장용으로 바뀐다")
    m = json.load(open(os.path.join(td, "good", "saddle", "saddle_meta.json")))
    chk(m["moving_atom_index_0based"] == 0 and abs(m["hop_distance_A"] - 3.667) < 1e-6,
        "뛰는 원자와 홉 거리를 맞게 기록한다")

    # ── 음성 ──
    mk("asym", False, A, B)
    # 두 끝점 에너지를 크게 벌린다 → (b) 경로도 막혀야 한다
    fp = os.path.join(td, "asym", "ep_final", "relax.out")
    # ⚠ open(fp,"w").write(open(fp).read()) 은 **쓰기가 먼저 평가돼 파일을 자른 뒤** 읽는다.
    _s = open(fp).read()
    open(fp, "w").write(_s.replace("-100.0000 Ry", "-99.0000 Ry"))
    rc, msg = build(td, "asym")
    chk(rc == 1 and "대칭 근거가 없다" in msg, "[음성] 비대칭 + 에너지 불일치를 거부한다")
    chk("meV" in msg, "[음성] 거부 사유에 실측 |ΔE| 를 적는다")
    rc, _ = build(td, "asym", force=True)
    chk(rc == 0, "[음성] --force 로만 강행된다")
    mm = json.load(open(os.path.join(td, "asym", "saddle", "saddle_meta.json")))
    chk("--force" in str(mm.get("symmetry_basis")), "[음성] --force 로 통과하면 그렇게 기록한다")

    # ★ meta 없이 **끝점 에너지 축퇴**로만 통과 (cc333 의 실제 상황)
    d0 = mk("nometa", None, A, B)
    os.remove(os.path.join(d0, "meta.json"))
    rc, msg = build(td, "nometa")
    chk(rc == 0 and "measured endpoint degeneracy" in msg,
        "[핵심] meta 없어도 끝점 에너지 축퇴로 통과한다 (cc333 상황)")
    chk("필요조건이지" in msg, "[핵심] 그때 충분조건이 아니라는 경고를 띄운다")
    mm = json.load(open(os.path.join(td, "nometa", "saddle", "saddle_meta.json")))
    chk(mm.get("endpoint_energy_diff_eV") == 0.0 and mm.get("symmetry_warning"),
        "[핵심] 근거·ΔE·경고를 meta 에 남긴다")

    mk("same", True, A, A)
    rc, msg = build(td, "same")
    chk(rc == 1 and "같은 구조" in msg, "[음성] 끝점이 같으면 거부한다 (뛰는 원자 없음)")

    d = mk("noout", True, A, B)
    os.remove(os.path.join(d, "ep_final", "relax.out"))
    rc, msg = build(td, "noout")
    chk(rc == 1 and "이완된 끝점이 필요하다" in msg, "[음성] 끝점 미이완이면 거부한다")

    # ★ cc333 실제 상황: JOB DONE 인데 final coordinates 없음 (nstep 한도)
    d0 = mk("unconv", True, A, B)
    for n in ("ep_initial", "ep_final"):
        fp = os.path.join(d0, n, "relax.out")
        s0 = open(fp).read()
        body = s0[s0.index("ATOMIC_POSITIONS"):s0.index("End final coordinates")]
        open(fp, "w").write(
            "     The maximum number of steps has been reached.\n"
            "     End of BFGS Geometry Optimization\n" + body +
            "     Total force =     0.018069     Total SCF correction =     0.000028\n"
            "!    total energy              =    -100.0000 Ry\nJOB DONE.\n")
    rc, msg = build(td, "unconv")
    chk(rc == 1 and "수렴하지 않았다" in msg, "[핵심] 미수렴 끝점을 기본값으로 거부한다")
    chk("0.46 eV/Å" in msg or "eV/Å" in msg, "[핵심] 잔여 힘을 eV/Å 로도 알려준다")
    rc, msg = build(td, "unconv", allow_unconverged=True)
    chk(rc == 0 and "끝점 미수렴" in msg, "[핵심] --allow_unconverged 면 진행하되 경고한다")
    mm = json.load(open(os.path.join(td, "unconv", "saddle", "saddle_meta.json")))
    chk(mm.get("endpoints_converged") is False and mm.get("unconverged_endpoints"),
        "[핵심] 미수렴 사실이 saddle_meta 에 박힌다")
    chk(abs(mm["endpoint_last_force_Ry_au"]["ep_initial"] - 0.018069) < 1e-9,
        "[핵심] 잔여 힘 값을 기록한다")

    d = mk("notdone", True, A, B)
    p = os.path.join(d, "ep_final", "relax.out")
    _s = open(p).read()                      # ⚠ 같은 truncate-before-read 함정
    open(p, "w").write(_s.replace("JOB DONE.", ""))
    rc, msg = build(td, "notdone")
    chk(rc == 1, "[음성] JOB DONE 없는 relax.out 을 안 받는다")

    # 최소이미지: 홉이 셀 경계를 넘어도 3.667 로 펴져야 한다
    small = [[7.0, 0, 0], [0, 7.0, 0], [0, 0, 7.0]]
    C = [("Li", (6.5, 0.0, 0.0)), ("Li", (2.0, 0.0, 0.0)), ("Li", (0.0, 2.0, 0.0))]
    D = [("Li", (0.5, 0.0, 0.0)), ("Li", (2.0, 0.0, 0.0)), ("Li", (0.0, 2.0, 0.0))]
    mk("pbc", True, C, D, cell=small)
    rc, _ = build(td, "pbc")
    mm = json.load(open(os.path.join(td, "pbc", "saddle", "saddle_meta.json")))
    chk(rc == 0 and abs(mm["hop_distance_A"] - 1.0) < 1e-6,
        f"[PBC] 경계를 넘는 홉을 최소이미지로 편다 (6.5→0.5 는 1.0 Å, got {mm['hop_distance_A']})")

    # collect
    sd = os.path.join(td, "good", "saddle")
    # ⚠ F5 가드가 생겨서 fixture 도 **끝난 relax** 여야 한다 (JOB DONE + final coordinates).
    #   옛 fixture 는 둘 다 없었는데 통과했다 — 그게 F5 가 잡은 결함이다.
    open(os.path.join(sd, "relax.out"), "w").write(
        "Begin final coordinates\nATOMIC_POSITIONS angstrom\n"
        "  Li  0.0 0.0 0.0\nEnd final coordinates\n"
        "     Total force =     0.000123\n"
        "!    total energy              =    -99.9832 Ry\nJOB DONE.\n")
    rc, msg = collect(td, "good")
    chk(rc == 0 and "Ea" in msg, "collect 가 Ea 를 낸다")
    ea = json.loads(msg.split("JSON: ")[1])["Ea_eV"]
    chk(abs(ea - (0.0168 * 13.605693122994)) < 1e-3, f"Ea 가 ΔE 와 맞는다 ({ea:.4f} eV)")

    # ══ 고정셸 경로 (리뷰 F3 — 이 170줄이 selftest 에 하나도 없었다) ══════════
    import math as _m
    CELL = [[14.0, 0, 0], [0, 14.0, 0], [0, 0, 14.0]]

    def mkf(tag, sym, ini, fin, cell=CELL, e_fin="-100.0000"):
        d = os.path.join(td, tag)
        for n in ("ep_initial", "ep_final"):
            os.makedirs(os.path.join(d, n), exist_ok=True)
        json.dump({"endpoints_symmetry_equivalent": sym, "supercell": [3, 3, 3],
                   "min_cell_A": 15.56}, open(os.path.join(d, "meta.json"), "w"))
        hdr = ("&CONTROL\n    calculation     = 'relax'\n"
               f"    prefix          = '{tag}_ep_initial'\n/\n"
               "&SYSTEM\n    ibrav           = 0\n/\n\nATOMIC_SPECIES\n  Li 6.94 li.UPF\n\n")
        k = ("K_POINTS automatic\n  2 2 2 0 0 0\n\nCELL_PARAMETERS angstrom\n"
             + "".join("  %16.10f %16.10f %16.10f\n" % tuple(v) for v in cell))
        for n, rows, en in (("ep_initial", ini, "-100.0000"), ("ep_final", fin, e_fin)):
            body = "ATOMIC_POSITIONS angstrom\n" + "".join(
                f"  {s:3s} {x:16.10f} {y:16.10f} {z:16.10f}\n" for s, (x, y, z) in rows)
            open(os.path.join(d, n, "relax.in"), "w").write(hdr + body + "\n" + k)
            open(os.path.join(d, n, "relax.out"), "w").write(
                "Begin final coordinates\n" + body + "End final coordinates\n"
                f"!    total energy              =    {en} Ry\nJOB DONE.\n")
        return d

    # 뛰는 Li 하나 + 근거리 이웃 + 원거리 원자들
    # 자유 원자 ≥ 8 가드를 만족하도록 근거리를 현실적으로 채운다
    NEAR = [("Li", (7.0, 0.0, 0.0)), ("Li", (0.0, 3.0, 0.0)), ("Li", (0.0, -3.0, 0.0)),
            ("Li", (1.8, 2.5, 0.0)), ("Li", (1.8, -2.5, 0.0)), ("Li", (1.8, 0.0, 2.5)),
            ("Li", (1.8, 0.0, -2.5)), ("Li", (3.0, 3.0, 0.0))]
    FAR = [("Li", (0.0, 0.0, 6.5)), ("Li", (6.5, 6.5, 6.5))]
    A2 = [("Li", (0.0, 0.0, 0.0))] + NEAR + FAR
    B2 = [("Li", (3.667, 0.0, 0.0))] + NEAR + FAR
    mkf("fz", True, A2, B2)
    rc, msg = build_frozen(td, "fz", 4.0)
    chk(rc == 0, "[고정셸] 대칭 홉이면 입력을 만든다")
    fd = os.path.join(td, "fz", "frozen_R4")
    chk(os.path.isfile(os.path.join(fd, "endpoint", "relax.in"))
        and os.path.isfile(os.path.join(fd, "saddle", "relax.in")),
        "[고정셸] endpoint·saddle 둘 다 생긴다")

    def rows_of(f):
        L = open(f).read().splitlines()
        i = [n for n, l in enumerate(L) if l.startswith("ATOMIC_POSITIONS")][0]
        out = []
        for l in L[i + 1:]:
            q = l.split()
            if len(q) >= 4 and re.match(r"^[A-Z][a-z]?$", q[0]):
                out.append((q[0], [float(x) for x in q[1:4]], "0 0 0" in l))
            elif out:
                break
        return out
    E = rows_of(os.path.join(fd, "endpoint", "relax.in"))
    S = rows_of(os.path.join(fd, "saddle", "relax.in"))
    chk(len(E) == len(S) == 1 + len(NEAR) + len(FAR), "[고정셸] 원자 수 보존")
    chk([r[2] for r in E][1:] == [r[2] for r in S][1:],
        "[고정셸] 고정/자유 집합이 endpoint·saddle 에서 동일하다")
    # ★ F2 회귀: 고정 원자는 두 파일에서 **같은 좌표**
    same = all(abs(a[1][k] - b[1][k]) < 1e-9 for a, b in zip(E, S) if a[2]
               for k in range(3))
    chk(same, "[핵심 F2] 고정 원자가 endpoint·saddle 에서 같은 좌표다")
    chk(sum(1 for r in E if r[2]) >= 1, "[고정셸] 원거리 원자가 실제로 고정된다")
    chk(not E[0][2] and S[0][2], "[고정셸] 뛰는 원자는 끝점에서 자유·안장에서 고정")
    fm = json.load(open(os.path.join(fd, "frozen_meta.json")))
    chk(fm.get("supercell") == [3, 3, 3] and fm.get("min_perp_width_A"),
        "[핵심 F4] frozen_meta 에 셀 식별정보가 있다")
    chk(fm.get("symmetry_basis") and fm.get("max_frozen_atom_shift_A") is not None,
        "[F4] 대칭근거·고정원자 이동량을 기록한다")

    # ── 음성 ──
    mkf("fz_asym", False, A2, B2, e_fin="-99.0000")
    rc, msg = build_frozen(td, "fz_asym", 4.0)
    chk(rc == 1 and "대칭 근거가 없다" in msg, "[핵심 F1] 고정셸도 비대칭 홉을 거부한다")

    rc, msg = build_frozen(td, "fz", 8.0)          # 14 Å 셀의 절반 = 7 Å
    chk(rc == 1 and "수직폭의 절반" in msg, "[음성] 반경이 셀 절반을 넘으면 거부")

    rc, msg = build_frozen(td, "fz", 0.5)          # 자유 원자 거의 없음
    chk(rc == 1, "[음성] 반경이 너무 작으면 거부")

    # ★ F2 회귀 (음성): 원거리 원자가 끝점 사이에서 움직이면 거부
    FARM = [("Li", (0.0, 0.0, 6.5)), ("Li", (6.9, 6.5, 6.5))]   # 원거리 하나가 0.4 Å 이동
    mkf("fz_shift", True, [("Li", (0.0, 0.0, 0.0))] + NEAR + FAR,
        [("Li", (3.667, 0.0, 0.0))] + NEAR + FARM)
    rc, msg = build_frozen(td, "fz_shift", 4.0)
    chk(rc == 1 and "고정 대상 원자가" in msg,
        "[핵심 F2] 고정 대상이 움직이면 거부한다 (Ea 오염 방지)")

    # ★ F5 회귀: 안 끝난 relax.out 에서 Ea 를 만들지 않는다
    for sub in ("endpoint", "saddle"):
        open(os.path.join(fd, sub, "relax.out"), "w").write(
            "!    total energy              =    -100.0000 Ry\n")   # JOB DONE 없음
    rc, msg = collect(td, "fz", 4.0)
    chk(rc == 1 and "JOB DONE" in msg, "[핵심 F5] 아직 도는 중이면 회수를 거부한다")
    rc, msg = collect(td, "fz", 4.0, allow_unconverged=True)
    chk(rc == 0 and "Ea" in msg, "[F5] --allow_unconverged 면 경고와 함께 회수")

    shutil.rmtree(td, ignore_errors=True)
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/data/work/runs/sei_neb_v2_cc333")
    ap.add_argument("--tag", default="li3nd")
    ap.add_argument("--collect", action="store_true", help="돌린 뒤 Ea 를 뽑는다")
    ap.add_argument("--force", action="store_true", help="비대칭인데도 강행 (권장 안 함)")
    ap.add_argument("--relax_radius", type=float, default=None,
                    help="고정셸 방식: 이 반경[Å] 밖 원자를 고정하고 공공 주변만 이완한다. "
                         "끝점·안장에 **같은** 중심·반경·자유집합을 쓴다")
    ap.add_argument("--allow_unconverged", action="store_true",
                    help="끝점 이완이 수렴 안 했어도 마지막 스텝 좌표로 진행 (결과에 명시된다)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.relax_radius is not None and a.relax_radius <= 0:
        # ⛔ 리뷰 F6 — 진리값으로 분기하면 0 이 전이완(수일짜리)으로 조용히 샌다
        print("⛔ --relax_radius 는 0 보다 커야 한다 (고정셸 반경 [Å]). "
              "전이완을 원하면 이 옵션을 아예 빼라")
        return 2
    if a.relax_radius and not a.collect:
        rc, msg = build_frozen(a.work, a.tag, a.relax_radius, a.force)
    elif a.collect:
        rc, msg = collect(a.work, a.tag, a.relax_radius, a.allow_unconverged)
    else:
        rc, msg = build(a.work, a.tag, a.force, a.allow_unconverged)
    print(msg)
    return rc


if __name__ == "__main__":
    sys.exit(main())
