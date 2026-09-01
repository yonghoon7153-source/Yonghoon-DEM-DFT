#!/usr/bin/env python3
"""neb_path_structures.py — QE neb.x `.crd` 의 이미지들을 VESTA 배포용 구조로 뽑는다.

`.crd` 는 FIRST_IMAGE / INTERMEDIATE_IMAGE… / LAST_IMAGE 블록에 **Cartesian
angstrom** 좌표만 들고 있고 **셀이 없다.** 셀은 원 구조 × 슈퍼셀 배수로 복원하고,
복원한 셀에 좌표가 실제로 들어가는지 **검증한 뒤에만** 쓴다 (안 맞으면 거절).

산출 (구조당 xyz + POSCAR 쌍 — 하우스 규약):
  db/structures/neb_paths/<case>_img<N>.{vasp,xyz}   (--all 일 때 7장 전부)
  db/structures/neb_paths/<case>_{initial,saddle,final}.{vasp,xyz}   (기본)

⛔ 이 도구가 **못 하는 것**
  · 좌표를 이완하지 않는다. `.crd` 에 있는 그대로 옮긴다.
  · 어느 이미지가 안장점인지 **스스로 판정하지 않는다** — `.dat` 의 에너지 최댓값
    이미지를 쓴다. `.dat` 가 없으면 saddle 을 만들지 않는다 (추측 금지).
  · 셀이 원 구조 × 정수배가 **아닌** 경우(vc-relax 로 격자가 바뀐 판)는 복원할 수
    없다. 그때는 검증에서 걸려 중단된다 — pw 입력의 CELL_PARAMETERS 가 필요하다.
"""
import argparse
import os
import sys

import numpy as np
from ase import Atoms
from ase.io import read, write

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = os.path.join(ROOT, "runs", "sei_neb_paths_2026_09_01")
OUT = os.path.join(ROOT, "db", "structures", "neb_paths")

#: case → (crd 파일, dat 파일, 원 구조, 슈퍼셀 배수, 표시명)
CASES = {
    "li2s": ("li2s/li2s.crd", "li2s/li2s.dat",
             "db/structures/sei_li2s_mp-1153.vasp", 3, "Li2S c->c (3x3x3)"),
    "li3nd_ccc": ("li3nd_ccc/li3nd.crd", "li3nd_ccc/li3nd.dat",
                  "db/structures/sei_li3nd_mp-976264.vasp", 2, "Li3Nd c->c (2x2x2)"),
    "li3nd_ccb": ("li3nd_ccb/li3nd.crd", "li3nd_ccb/li3nd.dat",
                  "db/structures/sei_li3nd_mp-976264.vasp", 2, "Li3Nd c->b diagnostic (2x2x2)"),
}
_MARK = ("FIRST_IMAGE", "INTERMEDIATE_IMAGE", "LAST_IMAGE")


def read_crd(path):
    """→ [(symbols, positions), ...] 이미지 순서대로."""
    imgs, sym, pos = [], [], []
    for ln in open(path, encoding="utf-8", errors="ignore"):
        t = ln.strip()
        if t in _MARK:
            if sym:
                imgs.append((sym, np.array(pos)))
            sym, pos = [], []
            continue
        if t.startswith("ATOMIC_POSITIONS") or not t:
            continue
        p = t.split()
        if len(p) >= 4:
            try:
                xyz = [float(x) for x in p[1:4]]
            except ValueError:
                continue
            sym.append(p[0])
            pos.append(xyz)
    if sym:
        imgs.append((sym, np.array(pos)))
    return imgs


def saddle_index(dat):
    """`.dat` 의 에너지 최댓값 이미지 번호(0-based). 없으면 None."""
    if not os.path.exists(dat):
        return None
    e = []
    for ln in open(dat, encoding="utf-8", errors="ignore"):
        p = ln.split()
        if len(p) >= 2:
            try:
                e.append(float(p[1]))
            except ValueError:
                pass
    return int(np.argmax(e)) if e else None


def build(case, dump_all=False, verbose=True):
    crd, dat, base, rep, label = CASES[case]
    imgs = read_crd(os.path.join(RAW, crd))
    _b = read(os.path.join(ROOT, base))
    cell, n_base = _b.cell.array * rep, len(_b)

    # ── 셀 복원 검증 ──────────────────────────────────────────────────────
    # ⚠ 분수좌표가 [0,1] 을 넘는 것은 **정상**이다. NEB 경로 좌표는 일부러 감싸지
    #   않는다 — 감싸면 이동 원자가 셀을 넘는 순간 경로가 튀기 때문이다 (li3nd c→b
    #   에서 1.125 까지 나갔다, 2026-09-01 실측). 그래서 범위로 판정하지 않는다.
    #   셀이 틀렸는지는 **감싼 뒤 원자가 겹치는가**로 본다 — 틀린 셀로 감싸면
    #   말도 안 되는 거리에 원자가 포개진다.
    for k, (sym, pos) in enumerate(imgs):
        f = np.linalg.solve(cell.T, pos.T).T
        if f.min() < -0.6 or f.max() > 1.6:                 # 총체적으로 틀린 셀만
            raise SystemExit(
                f"⛔ {case} 이미지 {k}: 좌표가 셀 밖으로 크게 벗어난다 "
                f"(분수 {f.min():.2f}~{f.max():.2f}) — 원 구조 × {rep} 가 아니다.")
        w = Atoms(symbols=sym, positions=pos, cell=cell, pbc=True)
        w.wrap()
        # (a) 셀이 **작으면** — 감쌌을 때 원자가 포개진다
        dmin = float(np.min(w.get_all_distances(mic=True)
                            + np.eye(len(w)) * 1e3))
        if dmin < 1.2:
            raise SystemExit(
                f"⛔ {case} 이미지 {k}: 감싼 뒤 최단 원자간 거리가 {dmin:.2f} Å 다 — "
                f"복원한 셀이 **작다** (pw 입력의 CELL_PARAMETERS 필요).")
        # (b) 셀이 **크면** — 겹치지도 않고 좌표도 다 들어가서 (a) 를 통과한다.
        #     ⚠ "채움 폭" 으로는 못 잡는다 — 감싸면 어느 셀이든 [0,1) 을 채운다
        #        (2026-09-01 실측: rep 2·3·4 전부 채움 0.999). 원자 **수**로 본다.
        #        NEB 셀은 완전 슈퍼셀에서 공공 몇 개가 빠진 것이어야 한다.
        n_exp = n_base * rep ** 3
        if not 0 <= n_exp - len(sym) <= 3:
            raise SystemExit(
                f"⛔ {case} 이미지 {k}: 원자 수가 안 맞는다 — 완전 {rep}×{rep}×{rep} 는 "
                f"{n_exp}개인데 경로에는 {len(sym)}개다 (차 {n_exp - len(sym)}). "
                f"공공 몇 개 차이여야 한다 — 슈퍼셀 배수가 틀렸다.")

    os.makedirs(OUT, exist_ok=True)
    sad = saddle_index(os.path.join(RAW, dat))
    pick = {0: "initial", len(imgs) - 1: "final"}
    if sad is not None and sad not in pick:
        pick[sad] = "saddle"
    made = []
    for k, (sym, pos) in enumerate(imgs):
        names = []
        if dump_all:
            names.append(f"{case}_img{k+1}")
        if k in pick:
            names.append(f"{case}_{pick[k]}")
        for nm in names:
            at = Atoms(symbols=sym, positions=pos, cell=cell, pbc=True)
            write(os.path.join(OUT, nm + ".vasp"), at, format="vasp",
                  direct=True, sort=True)
            write(os.path.join(OUT, nm + ".xyz"), at, format="extxyz")
            made.append(nm)
    if verbose:
        print(f"  {label}: 이미지 {len(imgs)} · 원자 {len(imgs[0][0])} · "
              f"안장점 이미지 {'미판정(.dat 없음)' if sad is None else sad + 1}")
        for nm in made:
            print(f"    → db/structures/neb_paths/{nm}.{{vasp,xyz}}")
    return made, imgs, cell, sad



#: 경로 겹침 파일에서 **중간 이미지**의 이동 원자를 무엇으로 찍을까.
#:   ⚠ 실제 원소가 아니다 — VESTA 에서 색이 갈리라고 쓰는 **표지**다.
#:   그래서 파일명에 `_marked` 를 달고, 겹침 파일은 계산 입력으로 쓰지 않는다.
PATH_MARK = "He"
#: 이동 원자로 볼 최소 변위 [Å] (초기→최종). 협동 이동이면 여럿이 잡힌다.
MOVE_MIN_A = 1.0


def path_overlay(case, mark=True, verbose=True):
    """골격(고정 원자) + 이동 원자의 **7 위치**를 한 파일에.

    경로를 한 장으로 보는 표준 그림이다 — 격자는 한 번만 그리고 뛰는 이온을
    구슬 사슬로 얹는다.

    ⛔ 못 하는 것
      · 이동 원자를 **자동으로 하나라고 가정하지 않는다.** 초기→최종 변위가
        MOVE_MIN_A 를 넘는 원자를 전부 넣는다 (협동 이동이면 여럿이다).
      · 표지 원소(He)는 **가짜다.** 계산 입력으로 쓰면 안 된다.
    """
    crd, dat, base, rep, label = CASES[case]
    imgs = read_crd(os.path.join(RAW, crd))
    _b = read(os.path.join(ROOT, base))
    cell = _b.cell.array * rep

    d = np.linalg.norm(imgs[-1][1] - imgs[0][1], axis=1)
    mov = np.where(d > MOVE_MIN_A)[0]
    if len(mov) == 0:
        raise SystemExit(f"⛔ {case}: 변위 {MOVE_MIN_A} Å 를 넘는 원자가 없다 — "
                         f"경로가 비었거나 이미지 순서가 어긋났다 (최대 {d.max():.2f} Å)")

    sym0, pos0 = imgs[0]
    keep = [i for i in range(len(sym0)) if i not in set(mov)]
    S = [sym0[i] for i in keep]
    P = [pos0[i] for i in keep]
    for k, (sym, pos) in enumerate(imgs):          # 이동 원자의 7 위치
        for i in mov:
            first_last = k in (0, len(imgs) - 1)
            S.append(sym[i] if (first_last or not mark) else PATH_MARK)
            P.append(pos[i])

    at = Atoms(symbols=S, positions=np.array(P), cell=cell, pbc=True)
    os.makedirs(OUT, exist_ok=True)
    nm = f"{case}_path_all{len(imgs)}" + ("_marked" if mark else "")
    write(os.path.join(OUT, nm + ".vasp"), at, format="vasp", direct=True, sort=True)
    write(os.path.join(OUT, nm + ".xyz"), at, format="extxyz")
    if verbose:
        print(f"  {label}: 골격 {len(keep)} + 이동원자 {len(mov)}개 × {len(imgs)} 위치 "
              f"= {len(S)} · 변위 {d[mov].min():.2f}–{d[mov].max():.2f} Å")
        print(f"    → db/structures/neb_paths/{nm}.{{vasp,xyz}}")
    return nm, len(mov), at


def selftest():
    """⛔음성 포함."""
    ok = [0, 0]

    def chk(c, m):
        print(("  ✔ " if c else "  ⛔ ") + m)
        ok[0 if c else 1] += 1

    made, imgs, cell, sad = build("li2s", verbose=False)
    chk(len(imgs) == 7, "li2s 가 7 이미지로 갈린다")
    chk(len(imgs[0][0]) == 80,
        "원자 80개 = 3×3×3(81) − 공공 1 (%d)" % len(imgs[0][0]))
    chk(sad == 3, "안장점이 4번째 이미지 (.dat 최댓값 기준, 0-based %s)" % sad)
    chk(all(len(s) == len(imgs[0][0]) for s, _ in imgs),
        "모든 이미지가 같은 원자 수다")
    d0 = np.abs(imgs[0][1] - imgs[-1][1]).max()
    chk(d0 > 1.0, "⛔음성 시작·끝 이미지가 실제로 다르다 (최대 변위 %.2f Å)" % d0)

    # ⛔음성: 셀 배수를 틀리게 주면 **거절해야** 한다
    import copy
    bad = copy.deepcopy(CASES["li2s"])
    CASES["li2s"] = (bad[0], bad[1], bad[2], 4, bad[4])      # 3 → 4 로 위조
    try:
        build("li2s", verbose=False)
        chk(False, "[음성] 셀을 **크게** 틀려도 그냥 통과시킨다 (채움 검사 없음)")
    except SystemExit:
        chk(True, "⛔음성 셀을 크게 틀리면(3→4) 채움 검사가 거절한다")
    finally:
        CASES["li2s"] = bad
    CASES["li2s"] = (bad[0], bad[1], bad[2], 2, bad[4])      # 3 → 2 (작게)
    try:
        build("li2s", verbose=False)
        chk(False, "[음성] 셀을 **작게** 틀려도 그냥 통과시킨다 (겹침 검사 없음)")
    except SystemExit:
        chk(True, "⛔음성 셀을 작게 틀리면(3→2) 겹침/이탈 검사가 거절한다")
    finally:
        CASES["li2s"] = bad

    m2, i2, _, s2 = build("li3nd_ccb", verbose=False)
    chk(s2 == 6, "⛔음성 li3nd c→b 의 최댓값은 **마지막 이미지**다 (안장점이 아니라 "
                 "끝점이 높은 진단 홉 — 0-based %s)" % s2)
    chk(not any("saddle" in x for x in m2),
        "⛔음성 그래서 saddle 파일을 만들지 않는다 (final 과 같은 이미지다)")
    nm, nmov, at = path_overlay("li2s", verbose=False)
    chk(nmov == 1, "li2s 는 이동 원자가 1개다 (공공 매개 단일 홉, %d)" % nmov)
    chk(len(at) == 80 + 6,
        "겹침 파일 = 골격 79 + 이동원자 7위치 = 86 (%d)" % len(at))
    chk(sum(1 for x in at.get_chemical_symbols() if x == PATH_MARK) == 5,
        "⛔음성 중간 5장만 표지로 찍고 처음·끝은 **실제 원소**로 남긴다")
    _, nm2, at2 = path_overlay("li3nd_ccc", verbose=False)
    chk(nm2 >= 1, "li3nd c→c 도 이동 원자를 찾는다 (%d개)" % nm2)

    print("selftest: %d 통과 / %d 실패" % (ok[0], ok[1]))
    return 0 if ok[1] == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", nargs="*", default=list(CASES))
    ap.add_argument("--all", action="store_true", help="7 이미지 전부 뽑는다")
    ap.add_argument("--overlay", action="store_true",
                    help="골격 + 이동원자 7위치를 **한 파일**로 (경로 한 장 보기)")
    ap.add_argument("--no_mark", action="store_true",
                    help="겹침에서 중간 위치도 실제 원소로 (표지 He 안 씀)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    for c in a.cases:
        build(c, dump_all=a.all)
        if a.overlay:
            path_overlay(c, mark=not a.no_mark)
    print("\n⚠ VESTA: .vasp 로 열어야 Boundary 타일링이 된다 (xyz 는 격자가 없다).")
    print("⚠ 이 구조들의 장벽은 citable=false 다 — db/properties/sei_neb.json 참조.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
