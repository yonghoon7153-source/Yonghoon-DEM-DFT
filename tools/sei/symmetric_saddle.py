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


def read_relaxed(outp):
    """relax.out 의 마지막 `Begin final coordinates` 블록 → [(sym, [x,y,z]), ...] (angstrom)."""
    if not os.path.isfile(outp):
        return None, f"없음: {outp}"
    t = open(outp, encoding="utf-8", errors="replace").read()
    if "JOB DONE" not in t:
        return None, f"아직 안 끝났다 (JOB DONE 없음): {outp}"
    i = t.rfind("Begin final coordinates")
    if i < 0:
        return None, f"final coordinates 블록 없음: {outp}"
    blk = t[i:t.find("End final coordinates", i)]
    m = re.search(r"ATOMIC_POSITIONS\s*\(?(\w+)", blk)
    if not m or m.group(1).lower() != "angstrom":
        return None, f"ATOMIC_POSITIONS 단위가 angstrom 이 아니다: {outp}"
    rows = []
    for l in blk[blk.index(m.group(0)) + len(m.group(0)):].splitlines()[1:]:
        p = l.split()
        if len(p) >= 4 and re.match(r"^[A-Z][a-z]?\d*$", p[0]):
            rows.append((p[0], [float(p[1]), float(p[2]), float(p[3])]))
        elif rows:
            break
    return (rows, None) if rows else (None, f"좌표를 못 읽었다: {outp}")


def final_energy(outp):
    """relax.out 의 마지막 총에너지 [eV]. Ry → eV."""
    t = open(outp, encoding="utf-8", errors="replace").read()
    e = re.findall(r"^!\s+total energy\s+=\s+([-\d.]+)\s+Ry", t, re.M)
    return float(e[-1]) * 13.605693122994 if e else None


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


def build(work, tag, force=False):
    d = os.path.join(work, tag)
    meta_p = os.path.join(d, "meta.json")
    meta = json.load(open(meta_p, encoding="utf-8")) if os.path.isfile(meta_p) else {}

    ini_out = os.path.join(d, "ep_initial", "relax.out")
    fin_out = os.path.join(d, "ep_final", "relax.out")
    ini_in = os.path.join(d, "ep_initial", "relax.in")
    first, e1 = read_relaxed(ini_out)
    last, e2 = read_relaxed(fin_out)
    if first is None or last is None:
        return 1, (f"⛔ {tag}: 이완된 끝점이 필요하다.\n   {e1 or ''}\n   {e2 or ''}\n"
                   f"   먼저: bash tools/sei/run_sei_neb.sh endpoints {tag}")
    if [s for s, _ in first] != [s for s, _ in last]:
        return 1, f"⛔ {tag}: 두 끝점의 원자 목록이 다르다 — 같은 계가 아니다"

    # ── 대칭 게이트 ────────────────────────────────────────────────────────
    #  ⛔ 비대칭 홉이면 안장점이 중점에 없다. 두 근거 중 하나면 통과시키되 **어느 쪽인지 적는다**:
    #    (a) meta 의 spglib orbit 판정 (`endpoints_symmetry_equivalent: true`)
    #    (b) **측정된 끝점 에너지 축퇴** — 이완된 두 끝점 에너지가 같다
    #  (b) 를 넣은 이유 (2026-08-16): cc333 은 build 가 "끝점 미이완" 으로 조기 반환해
    #  meta.json 이 아예 없다. 그렇다고 재생성하면 .ep_hash 가 달라져 이미 돌린 끝점
    #  relax 를 버린다. 그리고 (b) 는 메타데이터가 아니라 **실측**이라 더 낫다.
    #  ⚠ 다만 (b) 는 필요조건이지 충분조건이 아니다 — 대칭 비동등한 두 자리가 우연히
    #    같은 에너지일 수 있다. (b) 만으로 통과하면 경고를 남긴다.
    sym = meta.get("endpoints_symmetry_equivalent")
    e_ini, e_fin = final_energy(ini_out), final_energy(fin_out)
    de = (abs(e_fin - e_ini) if (e_ini is not None and e_fin is not None) else None)
    basis, warn = None, None
    if sym is True:
        basis = "meta.endpoints_symmetry_equivalent=true (spglib orbit)"
    elif de is not None and de <= ENDPOINT_TOL_EV:
        basis = f"measured endpoint degeneracy |ΔE| = {de*1000:.1f} meV ≤ {ENDPOINT_TOL_EV*1000:.0f} meV"
        warn = ("⚠ spglib 판정(meta)이 없어 **끝점 에너지 축퇴**로만 통과했다. 이는 필요조건이지 "
                "충분조건이 아니다 — 같은 홉이 더 작은 셀에서 대칭 동등으로 확인됐는지 함께 볼 것.")
    if basis is None and not force:
        return 1, (f"⛔ {tag}: 대칭 근거가 없다 — 중점법을 쓸 수 없다.\n"
                   f"   meta.endpoints_symmetry_equivalent = {sym!r}\n"
                   f"   끝점 에너지 차 |ΔE| = "
                   + (f"{de*1000:.1f} meV (> {ENDPOINT_TOL_EV*1000:.0f} meV 문턱)" if de is not None
                      else "측정 불가") + "\n"
                   f"   비대칭 홉은 안장점이 중점에 없다. full NEB 을 쓸 것.\n"
                   f"   (정말 강행하려면 --force — 근거를 db 에 남길 것)")
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
               f"   대칭 근거: {basis}\n"
               + (f"   {warn}\n" if warn else "")
               + f"   셀 {meta.get('supercell')} · 최소변 {meta.get('min_cell_A')} Å\n"
               f"   실행:  cd {sd} && mpirun -np <N> pw.x -in relax.in > relax.out")


def collect(work, tag):
    d = os.path.join(work, tag)
    ep = os.path.join(d, "ep_initial", "relax.out")
    sd = os.path.join(d, "saddle", "relax.out")
    for p in (ep, sd):
        if not os.path.isfile(p):
            return 1, f"⛔ 없음: {p}"
    e_end, e_sad = final_energy(ep), final_energy(sd)
    if e_end is None or e_sad is None:
        return 1, "⛔ 총에너지를 못 읽었다"
    ea = e_sad - e_end
    # 구속 원자에 남은 힘 — 대칭이 지켜졌는지의 지표 (판정은 사람이)
    t = open(sd, encoding="utf-8", errors="replace").read()
    fm = re.findall(r"Total force =\s+([\d.eE+-]+)", t)
    meta = {}
    mp = os.path.join(d, "saddle", "saddle_meta.json")
    if os.path.isfile(mp):
        meta = json.load(open(mp, encoding="utf-8"))
    out = {
        "tag": tag, "root": os.path.basename(work.rstrip("/")),
        "Ea_eV": round(ea, 6), "E_endpoint_eV": round(e_end, 6), "E_saddle_eV": round(e_sad, 6),
        "total_force_last_Ry_au": float(fm[-1]) if fm else None,
        "method": "symmetric-midpoint constrained relax (2 SCF relaxations, not NEB)",
        "supercell": meta.get("supercell"), "min_cell_A": meta.get("min_cell_A"),
        "caveat": ("대칭 홉 전제. 절대값 인용 전에 다른 셀에서 같은 방법으로 한 번 더 재고 "
                   "차이를 볼 것 — 이 도구의 용도가 그 비교다."),
    }
    return 0, (f"{tag} ({out['root']}, 셀 {out['supercell']}, 최소변 {out['min_cell_A']} Å)\n"
               f"  E_endpoint = {e_end:.6f} eV\n"
               f"  E_saddle   = {e_sad:.6f} eV\n"
               f"  ── Ea      = {ea:.4f} eV ──\n"
               f"  마지막 Total force = {out['total_force_last_Ry_au']} (Ry/au) "
               f"— 구속점이 대칭점이면 작아야 한다\n"
               f"  JSON: {json.dumps(out, ensure_ascii=False)}")


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
    open(os.path.join(sd, "relax.out"), "w").write(
        "     Total force =     0.000123\n"
        "!    total energy              =    -99.9832 Ry\nJOB DONE.\n")
    rc, msg = collect(td, "good")
    chk(rc == 0 and "Ea" in msg, "collect 가 Ea 를 낸다")
    ea = json.loads(msg.split("JSON: ")[1])["Ea_eV"]
    chk(abs(ea - (0.0168 * 13.605693122994)) < 1e-3, f"Ea 가 ΔE 와 맞는다 ({ea:.4f} eV)")

    shutil.rmtree(td, ignore_errors=True)
    print("selftest", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/data/work/runs/sei_neb_v2_cc333")
    ap.add_argument("--tag", default="li3nd")
    ap.add_argument("--collect", action="store_true", help="돌린 뒤 Ea 를 뽑는다")
    ap.add_argument("--force", action="store_true", help="비대칭인데도 강행 (권장 안 함)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    rc, msg = (collect(a.work, a.tag) if a.collect else build(a.work, a.tag, a.force))
    print(msg)
    return rc


if __name__ == "__main__":
    sys.exit(main())
