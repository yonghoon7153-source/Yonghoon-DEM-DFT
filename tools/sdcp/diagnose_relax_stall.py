#!/usr/bin/env python3
"""diagnose_relax_stall.py — QE relax 가 힘 문턱 위에서 **진동만 하는** 이유를 찾는다.

왜 만들었나 (gabia SDCP v2, 2026-08-06)
  LiNiO2(104) 슬랩 이완이 22스텝째에 max|F| ≈ 0.003 Ry/bohr 에서 멈춰 있다(목표 1e-3).
  그런데 **ΔE 는 −1.6 meV/스텝**(목표 1.4)로 거의 수렴했다.
  → 에너지는 평평한데 기울기가 안 죽는다 = **soft mode 이거나 힘 자체에 수치 잡음**이 있다.
  더 기다리는 것은 답이 아니고, **무엇이 흔드는지**를 봐야 한다.

이 도구가 보는 것 (전부 relax.out + relax.in 만으로)
  1) 스텝별 **max|F| 를 지고 있는 원자**가 누구인가 — 고정되어 있나, 바뀌나
     · 한 원자에 눌러앉아 있다 → 국소 문제(표면 종단·댕글링·잘못된 자리)
     · 스텝마다 돌아간다 → 전역 문제(믹싱·잡음·너무 얇은 슬랩)
  2) 그 원자들의 **좌표 궤적** — 두 위치를 왕복하면 이중우물/BFGS 요동
  3) **BFGS 건강성** — trust radius 축소·history reset 횟수
  4) **수치 잡음 용의자** — ecutrho/ecutwfc 비, degauss, k-mesh
     ⚠ USPP/PAW 에서 ecutrho 가 낮으면 힘이 1e-3 Ry/bohr 급에서 **바닥 잡음**을 친다.
       그러면 문턱을 못 넘는 게 물리가 아니라 격자 이산화 탓이다.
  5) **자성 요동** — Ni 하나가 스텝마다 스핀을 뒤집으면 힘이 그만큼 튄다
  6) 에너지-힘 **수렴 불일치** (지금 상태의 정의)

  python3 tools/sdcp/diagnose_relax_stall.py \\
      --out /data/work/runs/sdcp_v2/slab_relax/relax.out \\
      --in  /data/work/runs/sdcp_v2/slab_relax/relax.in
  python3 tools/sdcp/diagnose_relax_stall.py --out ... --in ... --top 5 --steps 12
"""
import argparse
import re
from collections import Counter

RY_EV = 13.605693


def read_free(in_path):
    """relax.in 의 ATOMIC_POSITIONS → {1-based idx: (종, 자유여부)}.

    ⚠ per-atom 힘 출력에는 **고정 원자(if_pos 0 0 0)** 의 raw 힘도 찍힌다.
      안 걸르면 움직일 수 없는 원자가 늘 1위로 잡혀 진단이 통째로 틀어진다.
    """
    free, on, n = {}, False, 0
    for line in open(in_path, errors="ignore"):
        if line.lstrip().startswith("ATOMIC_POSITIONS"):
            on, n = True, 0
            continue
        if on:
            f = line.split()
            if len(f) < 4:
                break
            n += 1
            fixed = len(f) >= 7 and f[4] == "0" and f[5] == "0" and f[6] == "0"
            free[n] = (f[0], not fixed)
    return free


def parse_steps(out_path, free):
    """[{maxf, who, per_atom{idx:max|F|}}] — 이온스텝 순서."""
    steps, cur, on = [], {}, False
    for line in open(out_path, errors="ignore"):
        if "Forces acting on atoms" in line:
            on, cur = True, {}
            continue
        if on and ("Total force" in line or line.lstrip().startswith("The ")):
            # ⚠ iverbosity 를 올리면 본 블록과 Total force 사이에 기여도 분해가 낀다.
            #   같은 `atom N type M force =` 형식이라 안 끊으면 물어 버린다.
            if cur:
                steps.append(cur)
            on, cur = False, {}
            continue
        f = line.split()
        if on and len(f) >= 9 and f[0] == "atom":
            i = int(f[1])
            if not free.get(i, (None, True))[1]:
                continue
            try:
                cur[i] = max(abs(float(v)) for v in f[6:9])
            except ValueError:
                pass
    return steps


def parse_positions(out_path):
    """ATOMIC_POSITIONS 블록들 → [[(sym,x,y,z), …], …] (스텝 순서)."""
    frames, cur, on = [], [], False
    for line in open(out_path, errors="ignore"):
        if line.lstrip().startswith("ATOMIC_POSITIONS"):
            if cur:
                frames.append(cur)
            on, cur = True, []
            continue
        if on:
            f = line.split()
            if len(f) >= 4 and re.match(r"^[A-Z][a-z]?\d*$", f[0]):
                try:
                    cur.append((f[0], float(f[1]), float(f[2]), float(f[3])))
                    continue
                except ValueError:
                    pass
            on = False
            if cur:
                frames.append(cur)
                cur = []
    if cur:
        frames.append(cur)
    return frames


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--top", type=int, default=4, help="추적할 상위 원자 수")
    ap.add_argument("--steps", type=int, default=10, help="보여줄 최근 스텝 수")
    ap.add_argument("--thr", type=float, default=1e-3, help="forc_conv_thr")
    a = ap.parse_args()

    txt = open(a.out, errors="ignore").read()
    free = read_free(a.inp)
    n_free = sum(1 for v in free.values() if v[1])
    steps = parse_steps(a.out, free)
    if not steps:
        print("⛔ per-atom 힘 블록을 못 찾았다. iverbosity/tprnfor 확인.")
        return
    print(f"원자 {len(free)}개 중 자유 {n_free}개 · 이온스텝 {len(steps)}개 파싱")
    print("=" * 78)

    # ── 1) 누가 max|F| 를 지고 있나 ─────────────────────────────────────────
    owners = [max(s, key=s.get) for s in steps]
    cnt = Counter(owners[-min(len(owners), 20):])
    print("① max|F| 를 지고 있는 원자 (최근 20스텝)")
    for i, c in cnt.most_common(6):
        sym = free.get(i, ("?", True))[0]
        vals = [s.get(i) for s in steps[-a.steps:] if i in s]
        rng = f"{min(vals):.5f}–{max(vals):.5f}" if vals else "-"
        print(f"   atom {i:4d} {sym:3s} — {c:2d}/{sum(cnt.values())} 스텝 1위 · 최근 {rng}")
    if len(cnt) == 1:
        print("   → **한 원자에 눌러앉아 있다** = 국소 문제. 그 원자의 자리·종단·이웃거리를 본다.")
    elif len(cnt) >= 4:
        print("   → **1위가 계속 바뀐다** = 전역 문제(믹싱·힘 잡음·슬랩 두께). "
              "개별 원자를 고쳐도 안 낫는다.")
    else:
        print("   → 소수 원자가 번갈아 1위 = 그 원자들끼리 결합한 국소 모드일 가능성.")

    # ── 2) 상위 원자의 힘·좌표 궤적 ────────────────────────────────────────
    top = [i for i, _ in cnt.most_common(a.top)]
    print(f"\n② 상위 {len(top)}개 원자의 힘 궤적 (최근 {a.steps}스텝)")
    for i in top:
        seq = [s.get(i) for s in steps[-a.steps:]]
        print(f"   atom {i:4d} {free.get(i, ('?',))[0]:3s} " +
              " ".join(f"{v:.4f}" if v else "  -  " for v in seq))

    frames = parse_positions(a.out)
    if len(frames) >= 3:
        print(f"\n③ 같은 원자의 z 좌표 궤적 (프레임 {len(frames)}개) — 왕복하면 이중우물/요동")
        for i in top:
            if i - 1 >= len(frames[-1]):
                continue
            zs = [fr[i - 1][3] for fr in frames[-a.steps:] if i - 1 < len(fr)]
            if len(zs) < 3:
                continue
            amp = max(zs) - min(zs)
            # 부호 반전 횟수 = 왕복의 지표
            d = [zs[k + 1] - zs[k] for k in range(len(zs) - 1)]
            flips = sum(1 for k in range(len(d) - 1) if d[k] * d[k + 1] < 0)
            tag = ("  ⚠ **왕복**" if flips >= len(d) * 0.5 and amp > 1e-3 else "")
            print(f"   atom {i:4d} Δz {amp:.4f} Å · 방향전환 {flips}/{len(d)-1}{tag}")
            print(f"        " + " ".join(f"{z:.4f}" for z in zs))
    else:
        print("\n③ ATOMIC_POSITIONS 프레임이 3개 미만 — 좌표 궤적 생략")

    # ── 4) BFGS 건강성 ─────────────────────────────────────────────────────
    print("\n④ BFGS 건강성")
    tr = re.findall(r"trust radius\s*=\s*([\d.]+)", txt)
    reset = len(re.findall(r"history already reset", txt))
    small = len(re.findall(r"trust radius.*too small|bfgs failed", txt, re.I))
    if tr:
        print(f"   trust radius 최근 {[f'{float(x):.4f}' for x in tr[-6:]]}")
        if float(tr[-1]) < 1e-3:
            print("   ⛔ **trust radius 붕괴** — BFGS 가 스스로 못 움직인다. "
                  "구조가 아니라 최적화기가 막혔다(재시작/알고리즘 교체).")
    print(f"   history reset {reset}회 · bfgs 실패 신호 {small}회"
          + ("   ⚠ reset 이 잦으면 힘 잡음을 의심한다" if reset >= 3 else ""))

    # ── 5) 수치 잡음 용의자 ────────────────────────────────────────────────
    print("\n⑤ 수치 잡음 용의자 (힘 바닥이 문턱보다 높으면 물리가 아니라 이산화 탓)")
    inp = open(a.inp, errors="ignore").read()

    def _num(key, src=inp):
        m = re.search(rf"{key}\s*=\s*([\d.eEdD+-]+)", src)
        return float(m.group(1).replace("d", "e").replace("D", "e")) if m else None

    ew, er = _num("ecutwfc"), _num("ecutrho")
    dg, thr = _num("degauss"), _num("forc_conv_thr")
    if ew:
        ratio = (er / ew) if er else 4.0
        print(f"   ecutwfc {ew:.0f} Ry · ecutrho {er if er else ew*4:.0f} Ry (비 {ratio:.1f}×)")
        if ratio < 8:
            print("   ⚠⚠ **USPP/PAW 에서 ecutrho/ecutwfc < 8 은 힘 잡음의 단골 원인이다.**")
            print("      밀도 컷이 낮으면 FFT 격자가 성글어 힘이 1e-3 Ry/bohr 급에서 바닥을 친다.")
            print("      → 검산: ecutrho 를 1.5배 올려 **single-point(scf) 한 판**만 돌려서")
            print("        같은 구조의 max|F| 가 유의하게 바뀌는지 본다. 바뀌면 잡음 확정.")
    if dg:
        print(f"   degauss {dg} Ry" + ("   ⚠ 큰 smearing 은 힘에 편향을 준다" if dg > 0.02 else ""))
    kg = re.search(r"K_POINTS[^\n]*\n\s*([\d\s]+)", inp)
    if kg:
        print(f"   k-mesh {' '.join(kg.group(1).split())}")
    if thr:
        print(f"   forc_conv_thr {thr:g} Ry/bohr")

    # ── 6) 자성 요동 ───────────────────────────────────────────────────────
    tm = [float(x) for x in re.findall(r"total magnetization\s+=\s+(-?[\d.]+)", txt)]
    am = [float(x) for x in re.findall(r"absolute magnetization\s+=\s+([\d.]+)", txt)]
    if len(am) >= 4:
        print("\n⑥ 자성 안정성 (스텝마다 스핀이 뒤집히면 힘이 그만큼 튄다)")
        print(f"   total 최근 {[f'{v:+.2f}' for v in tm[-6:]]}")
        print(f"   abs   최근 {[f'{v:.2f}' for v in am[-6:]]}"
              + ("   ⚠ **흔들린다**" if max(am[-6:]) - min(am[-6:]) > 0.3 else "   ✓ 안정"))

    # ── 7) 에너지 vs 힘 — 지금 상태의 정의 ─────────────────────────────────
    et = [float(x) for x in re.findall(r"^!\s+total energy\s+=\s+(-?[\d.]+)", txt, re.M)]
    mf = [max(s.values()) for s in steps if s]
    if len(et) >= 2 and mf:
        de = (et[-1] - et[-2]) * RY_EV * 1000
        print("\n⑦ 진단 요약")
        print(f"   ΔE {de:+.2f} meV/스텝 · max|F| {mf[-1]:.5f} (목표 {a.thr:g})"
              f" = 문턱의 {mf[-1]/a.thr:.1f}배")
        if abs(de) < 5 and mf[-1] > 2 * a.thr:
            print("   → **에너지는 평평한데 힘이 안 죽는다.** 둘 중 하나다:")
            print("      (a) soft mode — 움직여도 에너지가 거의 안 변하는 방향이 있다")
            print("      (b) 힘 잡음 — 격자/스미어링 탓에 힘 바닥이 문턱보다 높다")
            print("      ⑤의 ecutrho 검산이 (b)를 몇 시간 안에 가른다. 먼저 그것부터.")


if __name__ == "__main__":
    main()
