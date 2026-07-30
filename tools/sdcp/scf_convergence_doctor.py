#!/usr/bin/env python3
"""scf_convergence_doctor.py — QE scf.out 의 accuracy 궤적을 읽고 처방을 낸다.

왜 필요한가
  "iteration #300 에서 accuracy 0.0143 Ry" 라는 **마지막 한 줄만** 보면
  (a) 아직 잘 내려가는 중인데 maxstep 이 모자란 건지
  (b) 진짜 정체·진동인지
  를 구별할 수 없다. 실제로 두 번(2026-07-28 ELF, 07-29 Bader) 마지막 줄만 보고
  "반복당 비용이 커서 사실상 안 끝난다"로 오경보했는데 각각 15·17회 만에 끝났다.
  **남은 반복 수는 비용이 아니라 accuracy 궤적이 정한다.**

무엇을 보나
  · 최근 구간의 로그-선형 감소율 → 목표(conv_thr)까지 남은 반복 수 추정
  · 진동(오르내림) 비율 — mixing 문제의 지문
  · 정체(감소율 ~0) — 시드/스미어링 문제의 지문
  · 자화 궤적 — AFM 이 FM 으로 무너지거나 진동하면 그게 근본 원인이다

  python3 tools/sdcp/scf_convergence_doctor.py --scf_out .../slab/scf.out
"""
import argparse
import math
import re
from pathlib import Path

ACC = re.compile(r"estimated scf accuracy\s*<\s*([0-9.]+(?:[eE][-+]?\d+)?)\s*Ry")
ITER = re.compile(r"iteration #\s*(\d+)")
TOTMAG = re.compile(r"total magnetization\s*=\s*(-?[\d.]+)")
ABSMAG = re.compile(r"absolute magnetization\s*=\s*([\d.]+)")
CONV = re.compile(r"convergence has been achieved")
CONVTHR = re.compile(r"conv_thr\s*=\s*([0-9.]+(?:[eE][-+]?\d+)?)")


def rate(vals):
    """마지막 n 구간의 반복당 로그10 감소율 (양수 = 내려가는 중)."""
    if len(vals) < 3:
        return None
    a, b = vals[0], vals[-1]
    if a <= 0 or b <= 0:
        return None
    return (math.log10(a) - math.log10(b)) / (len(vals) - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scf_out", required=True)
    ap.add_argument("--scf_in", default=None, help="conv_thr 를 읽는다 (없으면 1e-6 가정)")
    ap.add_argument("--window", type=int, default=50, help="감소율을 잴 최근 구간")
    a = ap.parse_args()

    txt = Path(a.scf_out).read_text(errors="ignore")
    acc = [float(m.group(1)) for m in ACC.finditer(txt)]
    its = [int(m.group(1)) for m in ITER.finditer(txt)]
    tot = [float(m.group(1)) for m in TOTMAG.finditer(txt)]
    ab = [float(m.group(1)) for m in ABSMAG.finditer(txt)]
    thr = 1e-6
    if a.scf_in and Path(a.scf_in).exists():
        m = CONVTHR.search(Path(a.scf_in).read_text(errors="ignore"))
        if m:
            thr = float(m.group(1))

    if not acc:
        raise SystemExit("accuracy 줄이 없다 — 아직 첫 반복 전이거나 경로가 틀렸다")
    # ⚠ QE 는 accuracy 가 표시 자릿수 아래로 내려가면 **0.00000000 을 찍는다.**
    #   그대로 log10 하면 죽는다(실측). 0 은 '표시 한계 이하' 로 다룬다.
    acc = [v for v in acc if v > 0] or [thr]
    zero_tail = acc and float(ACC.findall(txt)[-1]) == 0.0
    print(f"반복 {len(its)}회 · accuracy {len(acc)}개 · 목표 conv_thr = {thr:g} Ry")
    if zero_tail:
        print("수렴 ❔  마지막 accuracy 가 0.00000000 (표시 자릿수 이하) — "
              "'convergence has been achieved' 유무로 판단하라")
    print(f"수렴 {'✅' if CONV.search(txt) else '❌'}   마지막 accuracy = {acc[-1]:.6g} Ry "
          f"(목표까지 {math.log10(acc[-1] / thr):.1f} 자릿수)")

    # ── 구간별 감소율 ────────────────────────────────────────────────────
    print("\n구간별 반복당 감소율 (자릿수/iter, 양수 = 내려가는 중):")
    n = len(acc)
    for lo, hi, lab in ((0, n // 3, "초반"), (n // 3, 2 * n // 3, "중반"),
                        (max(0, n - a.window), n, f"최근 {min(a.window, n)}회")):
        seg = acc[lo:hi]
        r = rate(seg)
        print(f"  {lab:10s} n={len(seg):3d}  {seg[0]:.3g} → {seg[-1]:.3g}   "
              + (f"{r:+.4f}" if r is not None else "  —"))

    recent = acc[-min(a.window, n):]
    r = rate(recent)
    # 진동: 직전보다 커진 횟수 비율
    ups = sum(1 for i in range(1, len(recent)) if recent[i] > recent[i - 1])
    osc = ups / max(1, len(recent) - 1)
    print(f"\n최근 구간 진동률 {osc:.0%} (오른 횟수/전체) — 40% 넘으면 mixing 문제 신호")

    if tot:
        print(f"total magnetization  마지막 {tot[-1]:+.3f}  "
              f"[최근 10: {', '.join(f'{v:+.2f}' for v in tot[-10:])}]")
    if ab:
        print(f"absolute magnetization 마지막 {ab[-1]:.3f}  "
              f"[최근 10: {', '.join(f'{v:.2f}' for v in ab[-10:])}]")

    # ── 처방 ────────────────────────────────────────────────────────────
    print("\n" + "=" * 66)
    if CONV.search(txt):
        print("✅ 수렴했다 — 처방 불필요.")
        return
    need = math.log10(acc[-1] / thr)
    if r is not None and r > 0.002:
        est = int(math.ceil(need / r))
        print(f"▶ **아직 내려가는 중이다.** 최근 감소율 {r:.4f} 자릿수/iter →"
              f" 목표까지 대략 **{est} iter** 더 필요.")
        print(f"   처방: electron_maxstep 을 {len(its) + est + 100} 이상으로 올리고 재시작.")
        print("   ⚠ 이때 mixing 을 건드리지 마라 — 잘 가고 있는 궤적을 흔든다.")
    elif osc > 0.40:
        print("▶ **진동한다** — accuracy 가 오르내린다. mixing 이 원인이다.")
        print("   처방(순서대로 하나씩):")
        print("     1) mixing_beta 를 절반으로 (0.03 → 0.015)")
        print("     2) mixing_ndim 을 늘린다 (20 → 12 로 **줄이는** 것도 시도 — 이력이 길면")
        print("        오히려 옛 정보가 발목을 잡는다)")
        print("     3) degauss 를 넓힌다 (0.02 → 0.03) — 금속 표면 점유수 요동 완화")
    else:
        print("▶ **정체다** — 감소율이 사실상 0. 반복만 늘려도 안 붙는다.")
        print("   처방(원인 순):")
        print("     1) **스핀 초기조건**을 의심하라. 위 자화 궤적이 흔들리거나 AFM(≈0)이")
        print("        아니면 그게 근본 원인이다. starting_magnetization 을 키우거나")
        print("        (±0.3 → ±0.6) 반대로 tot_magnetization 으로 잠깐 묶어 밑그림을 잡고")
        print("        푸는 2단 전략을 쓴다.")
        print("     2) degauss 를 넓힌다 (0.02 → 0.03~0.05). 좁은 스미어링은 금속 표면에서")
        print("        점유수를 매 반복 바꾸게 만든다.")
        print("     3) Hubbard U 를 켠 채로는 어렵다면 U=0 으로 먼저 수렴시키고 그 밀도를")
        print("        받아 U 를 켜는 단계 전략.")
    print("=" * 66)
    print(f"\n재시작 가능 여부: outdir 에 charge-density 가 남아 있으면 restart_mode='restart' 로")
    print(f"  {len(its)} 반복을 버리지 않고 이어받는다. 확인:")
    d = Path(a.scf_out).parent
    print(f"    ls -la {d}/tmp/*.save/charge-density* 2>/dev/null")


if __name__ == "__main__":
    main()
