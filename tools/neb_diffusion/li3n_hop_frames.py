#!/usr/bin/env python3
"""li3n_hop_frames.py — Li3N(001) hop 의 VESTA 표시용 프레임 생성.

계산한 두 구조(흡착 최소점 min, 안장점 TS)의 .vesta 를 받아, adatom 만 직선 hop 위로
옮긴 프레임 여러 장을 쓴다. 기판은 min 구조 것을 그대로 쓰고 adatom 좌표만 바꾼다
(min/TS 기판 차이는 육안으로 구분 안 되는 수준). 나머지 VESTA 설정(색·결합·경계)은
템플릿에서 통째로 승계하므로 렌더가 기존 두 장과 정확히 같은 양식으로 나온다.

hop 끝점은 min 을 표면 격자 병진으로 옮긴 **대칭 등가 자리**다. 기본값 (-1,+1) 은
supercell 분수좌표 (-1/3,+1/3) = 원시격자 -a1+a2, 길이 sqrt(3)*a. 끝점이 등가이므로
E(xi=0) = E(xi=1) 이 대칭에 의해 정확히 성립한다 — 그래프의 양끝 0.0 이 참이 되는 이유.

  python3 tools/neb_diffusion/li3n_hop_frames.py \\
      --min  li3n_onN_min_adNa_display.vesta \\
      --ts   li3n_TS_saddle_adNa_display.vesta \\
      --outdir docs/figures/li3n/hop_frames --xi 0,0.2,0.4,0.5,0.6,0.8,1.0

*** 이 도구가 못 하는 것 (중요) ***
  - **에너지를 만들지 않는다.** 중간 프레임은 계산된 배치가 아니라 직선 보간이다.
    xi=0 과 실제 TS(xi≈0.40) 두 장만 수렴한 DFT 구조이고 나머지는 그림용 궤적이다.
    캡션에 이 사실을 쓰지 않으면 계산하지 않은 이미지를 계산한 것처럼 보이게 된다.
  - 기판 이완을 xi 에 따라 바꾸지 않는다 (min 기판 고정).
  - 직선이 최소에너지 경로라고 주장하지 않는다. 구속 스캔은 MEP 의 상한이다.
  - 자리 이름(on-N / bridge)을 판정하지 않는다. 배위수는 --report 로 찍어보고
    직접 판단할 것 — 파일명 라벨과 실측이 어긋난 전례가 있다.

*** 2026-08-12 실측 경고 ***
Li3N(001) 에서는 **어느 격자 병진 방향으로도 직선 hop 이 N 원자를 관통한다**
(경로상 최소 Li-N 1.10-1.59 A; N 육각망 위 1.2 A 높이를 직선으로 가로지르기 때문).
min 을 TS 기준으로 반사한 점도 N 바로 위(1.495 A)라 자리가 아니다. 따라서 이 도구로
min/TS 를 잇는 7점 궤적을 만들면 Li 공이 N 을 뚫고 지나간다. 실제 MEP 는 hollow ->
bridge -> hollow 의 **지그재그**이지 직선이 아니다. 가드가 기본으로 막고,
--allow_collision 으로만 뚫린다 (진단용).
"""
import argparse
import math
import os
import re
import sys

HOP_DEFAULT = (-1, 1)
CLEARANCE_A = 1.90      # 이보다 가까우면 Li 가 N 을 관통 — 그림으로 쓸 수 없다
TS_XI_MAX = 1.35        # 계산된 안장점이 hop 위 어디까지 있어도 되는가.
                        # xi_ts > 1 = 안장점이 도착지보다 더 멀다 = 이 hop 의 안장점이 아니다.
                        # 경고만 하고 통과시킨다 (그림은 hop 자체가 물리적이면 그릴 수 있다).


def parse_vesta(path):
    """(cell6, [(idx, elem, label, fx, fy, fz, struc_line_no)], lines) 반환."""
    lines = open(path, encoding="ascii", errors="strict").read().splitlines()
    cell = None
    atoms = []
    for i, l in enumerate(lines):
        if l.strip() == "CELLP":
            cell = [float(x) for x in lines[i + 1].split()[:6]]
        if l.strip() == "STRUC":
            j = i + 1
            while j < len(lines):
                s = lines[j].split()
                if not s or s[0] == "0":
                    break
                if re.match(r"^\d+$", s[0]) and len(s) >= 8:
                    atoms.append((int(s[0]), s[1], s[2],
                                  float(s[4]), float(s[5]), float(s[6]), j))
                    j += 2
                else:
                    j += 1
    if cell is None or not atoms:
        raise SystemExit(f"VESTA 파싱 실패 (CELLP/STRUC 없음): {path}")
    return cell, atoms, lines


def lat2d(cell):
    a, b = cell[0], cell[1]
    g = math.radians(cell[5])
    return (a, 0.0), (b * math.cos(g), b * math.sin(g))


def adatom_of(atoms):
    """adatom = 라벨이 Na 인 원자 (표시용 재라벨 관례). 정확히 1개여야 한다."""
    cand = [a for a in atoms if a[1] == "Na"]
    if len(cand) != 1:
        raise SystemExit(f"adatom(Na) 이 {len(cand)}개 — 표시용 재라벨 관례를 확인할 것")
    return cand[0]


def hop_frac(hop):
    """격자 병진 (m,n) -> 3x3 supercell 분수좌표 증분. ('free',dfx,dfy) 면 그대로."""
    if len(hop) == 3 and hop[0] == "free":
        if abs(hop[1]) < 1e-9 and abs(hop[2]) < 1e-9:
            raise ValueError("--to_frac 가 시작점과 같다")
        return (hop[1], hop[2])
    m, n = hop
    if not (isinstance(m, int) and isinstance(n, int)):
        raise ValueError("hop 은 정수쌍이어야 한다 (원시격자 병진)")
    if m == 0 and n == 0:
        raise ValueError("hop (0,0) — 이동이 없다")
    return (m / 3.0, n / 3.0)


def min_clearance(atoms, cell, f_min, hop, n=60, z=None):
    """경로 위에서 가장 가까운 Li-N 거리 (Å). 직선이 물리적으로 통과 가능한지 판정."""
    dfx, dfy = hop_frac(hop)
    zf = f_min[2] if z is None else z
    worst = float("inf")
    for k in range(1, n):
        xi = k / n
        r = neighbours(atoms, cell, f_min[0] + xi * dfx, f_min[1] + xi * dfy, zf, "N", 3.2)
        if r:
            worst = min(worst, r[0])
    return worst


def frame_positions(f_min, f_ts, hop, xis):
    """[(xi, fx, fy, fz)] — xy 는 직선 보간, z 는 TS 높이를 정점으로 하는 대칭 보간.

    순수 함수 (파일 IO 없음) — selftest 가 직접 때린다.
    """
    dfx, dfy = hop_frac(hop)
    # TS 가 hop 위 어디인지 (xy 를 hop 벡터에 사영)
    vx, vy = f_ts[0] - f_min[0], f_ts[1] - f_min[1]
    denom = dfx * dfx + dfy * dfy
    xi_ts = (vx * dfx + vy * dfy) / denom
    if not (0.05 < xi_ts < TS_XI_MAX):
        raise ValueError(f"TS 가 hop 위 xi={xi_ts:.3f} — 이 hop 의 안장점이 아닌 듯하다")
    out = []
    for xi in xis:
        if not (0.0 <= xi <= 1.0):
            raise ValueError(f"xi={xi} 가 [0,1] 밖이다")
        # z: (0, z_min) - (xi_ts, z_ts) - (1-xi_ts, z_ts) - (1, z_min) 를 잇는 대칭 꺾은선
        t = min(xi, 1.0 - xi) if xi_ts < 0.95 else xi
        zf = f_min[2] + (f_ts[2] - f_min[2]) * (min(t / xi_ts, 1.0) if xi_ts > 0 else 0.0)
        out.append((xi, f_min[0] + xi * dfx, f_min[1] + xi * dfy, zf))
    return out, xi_ts


def neighbours(atoms, cell, fx, fy, fz, elem="N", cut=3.0):
    (a1x, a1y), (a2x, a2y) = lat2d(cell)
    c = cell[2]
    out = []
    for _i, el, _lb, gx, gy, gz, _j in atoms:
        if el != elem:
            continue
        for sx in (-1, 0, 1):
            for sy in (-1, 0, 1):
                dx, dy, dz = gx + sx - fx, gy + sy - fy, (gz - fz) * c
                cx, cy = dx * a1x + dy * a2x, dx * a1y + dy * a2y
                r = math.sqrt(cx * cx + cy * cy + dz * dz)
                if r <= cut:
                    out.append(r)
    return sorted(out)


def fix_bound(lines, zmax_needed, margin=0.03):
    """BOUND 의 z 범위를 adatom 이 들어오도록 넓힌다. (넓힌 새 zmax, 원래 zmax) 반환.

    VESTA 의 BOUND 는 표시 범위를 자른다. 원본 파일은 zmax=0.4 인데 adatom 은 z~0.45 라
    **경계 밖**이다. 그래도 보였던 이유는 SBOND 가 '경계 밖이라도 결합된 원자는 끌어온다'
    이기 때문 — 즉 결합을 끄거나 결합 규칙 없는 원소로 넣으면 원자가 조용히 사라진다.
    (2026-08-12 두 번 같은 방식으로 당함.)
    """
    i = next((k for k, l in enumerate(lines) if l.split() and l.split()[0] == "BOUND"), None)
    if i is None:
        raise SystemExit("BOUND 섹션이 없다")
    t = lines[i + 1].split()
    if len(t) < 6:
        raise SystemExit(f"BOUND 값줄을 못 읽음: {lines[i + 1]!r}")
    old = float(t[5])
    if zmax_needed + margin <= old:
        return old, old
    new = round(zmax_needed + margin, 4)
    t[5] = f"{new:g}"
    lines[i + 1] = "".join(f"{v:>9s}" for v in t[:6])
    return new, old


def _section_end(lines, header, nzero):
    """header 섹션의 종료줄(0 이 nzero 개) 인덱스."""
    # 헤더에 인자가 붙는 섹션이 있다 (예: "THERI 1") -> 첫 토큰으로 찾는다
    i = next((k for k, l in enumerate(lines)
              if l.split() and l.split()[0] == header), None)
    if i is None:
        raise SystemExit(f"{header} 섹션이 없다")
    for k in range(i + 1, len(lines)):
        t = lines[k].split()
        if t and all(x == "0" for x in t) and len(t) == nzero:
            return k
    raise SystemExit(f"{header} 종료줄(0 x{nzero}) 을 못 찾음")


def write_merged(lines, ad_line, pts, dst, ghost_rgb=(252, 238, 170), ghost_r=1.25,
                 no_bonds=False):
    """7 프레임의 adatom 을 **한 구조**에 다 넣는다.

    전부 **같은 원소(Na)** 로 넣고 크기·색은 SITET(= 라벨 단위)으로 구분한다.
    끝점 2개는 원래 크기·색, 중간점은 작고 옅게.

    2026-08-12: 처음엔 중간점을 다른 원소(K)로 넣어 SBOND 를 피하려 했는데
    **VESTA 가 그 원자들을 아예 안 그렸다.** 템플릿에 없던 원소를 ATOMT 에 추가하는
    경로는 신뢰할 수 없다 -> 원소는 그대로 두고 SITET 으로만 구분한다.
    no_bonds=True 면 Na-N SBOND 최대거리를 0 으로 만들어 결합선을 전부 끈다.
    STRUC / THERI / SITET 세 목록에 모두 넣어야 VESTA 가 인식한다.
    """
    out = list(lines)
    base = out[ad_line].split()
    nat = int(base[0])
    real_rgb, real_r = (249, 220, 60), 1.91
    new_struc, new_theri, new_sitet = [], [], []
    idx = nat
    for k, (xi, fx, fy, fz) in enumerate(pts):
        if k == 0:
            out[ad_line] = (f"{nat:>3d} {'Na':>2s} {'Na1':>10s}  1.0000 "
                            f"{fx:10.6f} {fy:10.6f} {fz:10.6f}    1a       1")
            continue
        idx += 1
        endpoint = (k == len(pts) - 1)
        el = base[1]                      # 템플릿 adatom 과 같은 원소 (새 원소 도입 금지)
        lb = f"{el}{idx}"
        rgb, rad = ((real_rgb, real_r) if endpoint else (ghost_rgb, ghost_r))
        new_struc += [f"{idx:>3d} {el:>2s} {lb:>10s}  1.0000 "
                      f"{fx:10.6f} {fy:10.6f} {fz:10.6f}    1a       1",
                      "                            0.000000   0.000000   0.000000  0.00"]
        new_theri.append(f"{idx:>3d} {lb:>10s} -0.000000")
        new_sitet.append(f"{idx:>3d} {lb:>10s}  {rad:.4f} {rgb[0]:3d} {rgb[1]:3d} {rgb[2]:3d} "
                         f"{rgb[0]:3d} {rgb[1]:3d} {rgb[2]:3d}  50  0")
    # adatom 이 BOUND 밖이면 결합 없이는 안 보인다 -> 경계부터 넓힌다
    zb_new, zb_old = fix_bound(out, max(p[3] for p in pts))
    if zb_new != zb_old:
        print(f"   BOUND zmax {zb_old:g} -> {zb_new:g} (adatom 이 경계 밖이었다)")
    if no_bonds:                      # Na-N 결합선 끄기 (최대거리 -> 0)
        for k, l in enumerate(out):
            t = l.split()
            if len(t) > 4 and t[1] == base[1] and t[2] == "N":
                out[k] = l.replace(t[4], "0.00000", 1)
    for header, nzero, block in (("SITET", 6, new_sitet),
                                 ("THERI", 3, new_theri), ("STRUC", 7, new_struc)):
        e = _section_end(out, header, nzero)
        out[e:e] = block
    txt = "\n".join(out) + "\n"
    txt.encode("ascii")
    with open(dst, "w", newline="\r\n") as f:
        f.write(txt)
    return idx


def write_frame(lines, line_no, elem, label, fx, fy, fz, dst):
    out = list(lines)
    fix_bound(out, fz)
    old = out[line_no].split()
    out[line_no] = (f"{old[0]:>3s} {elem:>2s} {label:>10s}  {float(old[3]):.4f} "
                    f"{fx:10.6f} {fy:10.6f} {fz:10.6f}    {old[7]}       {old[8]}")
    txt = "\n".join(out) + "\n"
    txt.encode("ascii")                      # CLAUDE.md: .vesta 는 ASCII 전용
    with open(dst, "w", newline="\r\n") as f:   # + CRLF
        f.write(txt)


def selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        print(("  ok   " if cond else "  FAIL ") + name)
        ok = ok and bool(cond)

    fmin, fts = (0.887775, 0.120635, 0.446500), (0.750001, 0.250006, 0.455211)
    pts, xi_ts = frame_positions(fmin, fts, (-1, 1), [0.0, 0.4, 0.5, 0.6, 1.0])
    chk("TS 가 hop 위 0.40 근처", abs(xi_ts - 0.401) < 0.01)
    chk("xi=0 은 min 좌표 그대로", abs(pts[0][1] - fmin[0]) < 1e-12 and abs(pts[0][3] - fmin[2]) < 1e-12)
    chk("끝점 = min + (-1/3,+1/3)", abs(pts[4][1] - (fmin[0] - 1 / 3)) < 1e-12
        and abs(pts[4][2] - (fmin[1] + 1 / 3)) < 1e-12)
    chk("z 가 xi 0.4/0.6 에서 대칭", abs(pts[1][3] - pts[3][3]) < 1e-12)
    chk("z 정점 = TS 높이", abs(pts[2][3] - fts[2]) < 1e-12)
    chk("xy 가 xi 0.4/0.6 에서 대칭", abs((pts[1][1] + pts[3][1]) / 2 - (fmin[0] - 1 / 6)) < 1e-12)

    # --- 음성 경로: 틀린 입력을 잡아내는가 ---
    for bad, why in (((0, 0), "hop (0,0)"), ((0.5, 1), "비정수 hop")):
        try:
            frame_positions(fmin, fts, bad, [0.5]); chk(f"{why} 거부", False)
        except (ValueError, TypeError):
            chk(f"{why} 거부", True)
    try:
        frame_positions(fmin, fts, (-1, 1), [1.5]); chk("범위 밖 xi 거부", False)
    except ValueError:
        chk("범위 밖 xi 거부", True)
    try:   # TS 가 이 hop 위에 없으면 (엉뚱한 방향) 거부해야 한다
        frame_positions(fmin, (0.9, 0.13, 0.45), (-1, 1), [0.5]); chk("hop 밖 TS 거부", False)
    except ValueError:
        chk("hop 밖 TS 거부", True)
    chk("관통 임계가 Li-N 결합보다 낮게 잡혀 있지 않다", CLEARANCE_A >= 1.85)
    chk("TS_XI_MAX 가 1 을 넘는 경우를 허용", 1.0 < TS_XI_MAX < 2.0)
    try:   # 완전히 반대 방향이면 여전히 거부해야 한다
        frame_positions(fmin, fts, (1, -1), [0.5]); chk("역방향 hop 거부", False)
    except ValueError:
        chk("역방향 hop 거부", True)
    # 병합 블록이 세 목록 전부에 들어가는가 (하나라도 빠지면 VESTA 가 원자를 무시한다)
    import inspect as _ins
    src = _ins.getsource(write_merged)
    chk("STRUC/THERI/SITET 셋 다 갱신", all(h in src for h in ("STRUC", "THERI", "SITET")))
    # VESTA 가 안 그리는 사고 재발 방지: 템플릿에 없던 원소를 새로 만들면 안 된다
    chk("새 원소를 도입하지 않는다 (el = base[1])", 'el = base[1]' in src)
    chk("ATOMT 를 건드리지 않는다", "new_atomt" not in src)
    # BOUND 가 adatom 을 자르면 결합 없이는 안 보인다 — 넓히는지 확인
    demo = ["BOUND", "       0        1         0        1         0      0.4", "  0   0   0   0  0"]
    new, old = fix_bound(demo, 0.4537)
    chk("BOUND zmax 를 adatom 위로 넓힘", new > 0.4537 and old == 0.4)
    chk("BOUND 값줄이 6필드 유지", len(demo[1].split()) == 6)
    # fix_bound 는 리스트를 제자리 수정한다 -> 새 사본으로 검사해야 한다
    demo2 = ["BOUND", "       0        1         0        1         0      0.4", "  0   0   0   0  0"]
    before = demo2[1]
    n2, o2 = fix_bound(demo2, 0.20)
    chk("이미 충분하면 안 건드림", n2 == o2 == 0.4 and demo2[1] == before)
    try:
        fix_bound(["STRUC"], 0.5); chk("BOUND 없으면 거부", False)
    except SystemExit:
        chk("BOUND 없으면 거부", True)
    # 헤더에 인자가 붙는 섹션(THERI 1)도 찾아야 한다 — 못 찾으면 원자가 조용히 누락된다
    demo = ["STRUC", "  1 Li Li1 1.0 0 0 0 1a 1", "  0 0 0 0 0 0 0",
            "THERI 1", "  1 Li1 -0.0", "  0 0 0"]
    chk("'THERI 1' 처럼 인자 붙은 헤더 인식", _section_end(demo, "THERI", 3) == 5)
    try:
        _section_end(demo, "SITET", 6); chk("없는 섹션 거부", False)
    except SystemExit:
        chk("없는 섹션 거부", True)
    try:
        adatom_of([(1, "Li", "Li1", 0, 0, 0, 0)]); chk("adatom 없음 거부", False)
    except SystemExit:
        chk("adatom 없음 거부", True)

    print("RESULT:", "0 실패" if ok else "실패 있음")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min", dest="fmin", help="흡착 최소점 .vesta (기판 템플릿)")
    ap.add_argument("--ts", help="안장점 .vesta (adatom 높이·hop 방향 참조)")
    ap.add_argument("--outdir")
    ap.add_argument("--xi", default="0,0.2,0.4,0.5,0.6,0.8,1.0")
    ap.add_argument("--hop", default="-1,1", help="원시격자 병진 (m,n); 기본 -1,1 = sqrt(3)a")
    ap.add_argument("--to_frac", help="끝점 supercell 분수좌표 'fx,fy' (--hop 대신; 격자 병진이 아니어도 됨)")
    ap.add_argument("--report", action="store_true", help="각 프레임 N 배위 거리 출력")
    ap.add_argument("--allow_collision", action="store_true",
                    help="N 관통 경로도 강행 (진단 전용 — 그림으로 쓰지 말 것)")
    ap.add_argument("--no_bonds", action="store_true",
                    help="adatom-N 결합선 전부 끄기 (궤적이 지저분하면)")
    ap.add_argument("--merge", action="store_true",
                    help="7 프레임을 낱장 대신 **한 .vesta** 에 (끝점 2개는 실색, 중간은 ghost)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    for r in ("fmin", "ts", "outdir"):
        if not getattr(a, r):
            sys.exit(f"--{'min' if r == 'fmin' else r} 필요")

    cell, atoms, lines = parse_vesta(a.fmin)
    cell_t, atoms_t, _ = parse_vesta(a.ts)
    if [round(x, 4) for x in cell] != [round(x, 4) for x in cell_t]:
        sys.exit("min/TS 셀이 다르다 — 같은 슬랩이 아니다")
    ad, ad_t = adatom_of(atoms), adatom_of(atoms_t)
    if a.to_frac:
        tfx, tfy = [float(t) for t in a.to_frac.replace(" ", "").split(",")]
        hop = ("free", tfx - ad[3], tfy - ad[4])
    else:
        hop = tuple(int(t) for t in a.hop.split(","))
    xis = [float(t) for t in a.xi.replace(" ", "").split(",")]

    clear = min_clearance(atoms, cell, ad[3:6], hop)
    if clear < CLEARANCE_A and not a.allow_collision:
        sys.exit(f"거부: 경로상 최소 Li-N = {clear:.3f} A < {CLEARANCE_A} A -- 직선이 N 을 관통한다.\n"
                 "  Li3N(001) 에서는 모든 격자 병진 방향이 그렇다 (docstring 경고 참조).\n"
                 "  실제 MEP 는 hollow->bridge->hollow 지그재그다. 계산 없이 그릴 수 없다.\n"
                 "  진단 목적이면 --allow_collision.")
    if clear < CLEARANCE_A:
        print(f"*** 경고: 경로상 최소 Li-N = {clear:.3f} A -- 물리적으로 불가능한 궤적이다. 그림 금지. ***")
    pts, xi_ts = frame_positions(ad[3:6], ad_t[3:6], hop, xis)
    if xi_ts > 1.0:
        print(f"*** 주의: 계산된 안장점이 hop 위 xi={xi_ts:.2f} — 도착지보다 멀다.\n"
              f"    이 hop 의 안장점은 계산된 적이 없다. 프레임의 중간 높이는 표시용 보간이다. ***")
    (a1x, a1y), (a2x, a2y) = lat2d(cell)
    dfx, dfy = hop_frac(hop)
    hx, hy = dfx * a1x + dfy * a2x, dfx * a1y + dfy * a2y
    print(f"hop {hop} = {math.hypot(hx, hy):.3f} A ; 계산된 TS 는 xi = {xi_ts:.3f}")
    os.makedirs(a.outdir, exist_ok=True)
    if a.merge:
        dst = os.path.join(a.outdir, "li3n_hop_alladatoms%s_display.vesta"
                           % ("_nobond" if a.no_bonds else ""))
        n = write_merged(lines, ad[6], pts, dst, no_bonds=a.no_bonds)
        print(f"-> {dst}  ({len(pts)} 위치, 총 원자 {n})")
        for xi, fx, fy, fz in pts:
            tagr = "끝점(큰 공)" if (xi in (pts[0][0], pts[-1][0])) else "중간(작은 공)"
            print(f"     xi={xi:.2f}  frac=({fx:.4f},{fy:.4f},{fz:.4f})  {tagr}")
        print("\n[캡션 필수] ghost 위치는 계산된 배치가 아니라 직선 보간 궤적이다.")
        return
    for xi, fx, fy, fz in pts:
        name = f"li3n_hop_xi{int(round(xi * 100)):03d}_adNa_display.vesta"
        dst = os.path.join(a.outdir, name)
        write_frame(lines, ad[6], "Na", "Na1", fx, fy, fz, dst)
        note = "  <- 계산된 구조" if abs(xi) < 1e-9 or abs(xi - round(xi_ts, 1)) < 1e-9 else ""
        print(f"-> {dst}  xi={xi:.2f}  frac=({fx:.4f},{fy:.4f},{fz:.4f}){note}")
        if a.report:
            r = neighbours(atoms, cell, fx, fy, fz, "N", 3.0)
            print("     N 3.0 A 안: " + " ".join(f"{v:.3f}" for v in r[:5]))
    print("\n[캡션 필수] 중간 프레임은 직선 보간 궤적이다. 수렴한 DFT 구조는 "
          f"xi=0 과 xi={xi_ts:.2f} 두 장뿐.")


if __name__ == "__main__":
    main()
