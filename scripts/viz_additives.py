#!/usr/bin/env python3
"""Visualise the Stage-1 additive morphology: a top-down (x–y) slab of the MPM
output coloured by phase — AM skeleton + SE + VGCF fibres + Super P + PTFE — to
eyeball "where the carbon sits" vs the SEM.

Real run:  --se se_dump.npy --phase phase.npy [--am am_scaffold.csv] [--lateral-box B]
Preview :  --demo   (synthesise a few AM + VGCF fibres + Super P, render the look)

  python3 scripts/viz_additives.py --demo --out docs/figures/additives_preview.png
"""
import argparse
import math

import numpy as np

#: phase → (colour, label, marker size).
#  ⚠⚠ **상 코드의 정본은 `additives.PHASE` 다** — 여기 숫자를 직접 적지 않는다.
#  2026-08-29 실사고: 이 표가 1~4 만 갖고 있어 **SDCP(5)·SWCNT(6) 이 그림에서 조용히
#  사라졌다.**  Figure 4a 의 요지가 *"DBE 에 SDCP 가 있다"* 인데 렌더러가 그 상을 안 그리면
#  두 침대가 바인더 양만 다른 것처럼 보인다 = **그림판 false-green**.  경고도 안 났다 —
#  `for code in COL` 이라 목록에 없는 코드는 애초에 순회되지 않기 때문이다.
#  ⇒ ① 정본에서 만들고 ② 자료에 있는데 **안 그려진 코드가 있으면 거부**한다.
_STYLE = {                       # ★ 이름이 키다 (숫자가 아니다) — 코드가 바뀌어도 안 어긋난다
    'AM':     ('#5a6b7a', 3),
    'SE':     ('#bdbdbd', 1),
    'VGCF':   ('#111111', 6),
    'SuperP': ('#777777', 8),
    'PTFE':   ('#e08214', 4),
    'SDCP':   ('#2166ac', 5),
    'SWCNT':  ('#762a83', 5),
}
_LABEL = {'SuperP': 'Super P', 'AM': 'AM (points)'}


def _build_col():
    """`additives.PHASE` 로부터 만든다 — 상 목록을 두 곳에 적지 않기 위해서다."""
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import additives as _ad
    out = {}
    for name, code in _ad.PHASE.items():
        if name not in _STYLE:
            raise SystemExit(f'⛔ 상 `{name}`(코드 {code}) 의 표시 규약이 없다 — '
                             '`_STYLE` 에 추가할 것.  안 그리고 넘어가지 않는다')
        c, ms = _STYLE[name]
        out[int(code)] = (c, _LABEL.get(name, name), ms)
    return out


COL = _build_col()


def undrawn_codes(phase):
    """자료에 있는데 `COL` 이 모르는 상 코드 → 정렬 목록.  비어 있어야 정상이다."""
    return sorted(int(c) for c in np.unique(np.asarray(phase)) if int(c) not in COL)


def _demo(rng, box=50.0):
    """AM_P(6µm)+AM_S(2µm) skeleton + VGCF fibres threading the gaps + Super P dots."""
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import additives as ad
    am = []                                                  # (x,y,z,r)
    for r, k in ((6.0, 9), (2.0, 40)):
        for _ in range(k):
            am.append((rng.uniform(r, box - r), rng.uniform(r, box - r),
                       rng.uniform(r, box - r), r))
    am = np.array(am)

    def in_am(p):                                            # reject points inside an AM sphere
        d = am[:, :3] - p
        return bool((np.einsum('ij,ij->i', d, d) <= am[:, 3] ** 2).any())
    fib = ad.seed_fibres(70, (box, box, box), 0.3, rng, L=10.0, in_am=in_am)
    sp = ad.seed_blobs(300, (box, box, box), rng, in_am=in_am)
    return am, fib, sp


def selftest():
    """상 목록이 정본을 따라가는가 + 모르는 상을 **정말** 거부하는가."""
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import additives as _ad
    ok, bad = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(f'{name} {extra}')

    # ① 정본의 모든 상이 그려진다 — 이 사고의 재현 시험이다.
    #    옛 판(1~4)이었다면 SDCP·SWCNT 에서 실패한다.
    for nm, code in _ad.PHASE.items():
        chk(f'① {nm}({code}) 표시 규약 있음', int(code) in COL)
    chk('① SDCP 가 실제로 들어 있다', int(_ad.PHASE['SDCP']) in COL)
    chk('① SWCNT 가 실제로 들어 있다', int(_ad.PHASE['SWCNT']) in COL)

    # ② 라벨·색이 상마다 구분된다 (한 색으로 뭉치면 그림이 못 읽힌다)
    cols = [v[0] for v in COL.values()]
    chk('② 색이 전부 다르다', len(set(cols)) == len(cols), str(cols))
    labs = [v[1] for v in COL.values()]
    chk('② 라벨이 전부 다르다', len(set(labs)) == len(labs), str(labs))

    # ③ 모르는 코드는 **잡힌다** (음성 경로)
    ph = np.array([1, 2, 5, 99], dtype=np.int8)
    chk('③ 미등록 코드 검출', undrawn_codes(ph) == [99], str(undrawn_codes(ph)))
    chk('③ 등록 코드만이면 빈 목록', undrawn_codes(np.array([1, 2, 4, 5])) == [])

    # ④ 실제 CLI 가 그 자료를 **거부**한다 (검사기가 있어도 배선이 없으면 소용없다)
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        se = np.column_stack([np.linspace(0, 1, 4)] * 3).astype(np.float32)
        np.save(os.path.join(tmp, 'se.npy'), se)
        np.save(os.path.join(tmp, 'ph.npy'), ph)
        cmd = [sys.executable, os.path.abspath(__file__),
               '--se', os.path.join(tmp, 'se.npy'), '--phase', os.path.join(tmp, 'ph.npy'),
               '--out', os.path.join(tmp, 'o.png')]
        r = subprocess.run(cmd, capture_output=True, text=True)
        chk('④ CLI 가 거부한다', r.returncode != 0 and not os.path.exists(os.path.join(tmp, 'o.png')),
            f'rc={r.returncode}')
        r2 = subprocess.run(cmd + ['--allow-undrawn'], capture_output=True, text=True)
        chk('④ --allow-undrawn 이면 그린다', r2.returncode == 0
            and os.path.exists(os.path.join(tmp, 'o.png')), f'rc={r2.returncode} {r2.stderr[-200:]}')

    # ⑤ AM scaffold 단위 — 크기 휴리스틱이 냈던 1000배 오차의 재현 시험
    #    우리 scaffold 는 **mm** 다 (헤더: "lateral 0..0.05 = 50um").
    mm = np.array([[0.000157, 0.010], [0.025033, 0.030], [0.049955, 0.049]])
    chk('⑤ mm 을 mm 으로 읽는다', am_scale_to_um(mm, 50.0) == 1e3, str(am_scale_to_um(mm, 50.0)))
    chk('⑤ 옛 휴리스틱이면 상자 밖', 0.025033 * 1e6 > 50.0)     # = 25,033 µm
    um = mm * 1e3
    chk('⑤ µm 을 µm 으로 읽는다', am_scale_to_um(um, 50.0) == 1.0, str(am_scale_to_um(um, 50.0)))
    chk('⑤ 명시 단위가 이긴다', am_scale_to_um(mm, 50.0, 'mm') == 1e3)
    try:                                                       # 잘못 지정하면 거부 (음성 경로)
        am_scale_to_um(mm, 50.0, 'm')
        chk('⑤ 틀린 단위 거부', False, '거부하지 않았다')
    except SystemExit:
        chk('⑤ 틀린 단위 거부', True)

    # ⑥ 리포의 **실제** scaffold 로 확인한다 (합성 픽스처만으로는 규약을 못 맞춘다)
    real = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', 'docs', 'data', 'real14_am_scaffold.csv')
    if os.path.exists(real):
        arr = np.loadtxt(real, delimiter=',', comments='#', ndmin=2)
        s_real = am_scale_to_um(arr[:, 1:3], 50.0)
        chk('⑥ 실제 scaffold = mm', s_real == 1e3, str(s_real))
        chk('⑥ 반지름이 2·6 µm 로 나온다',
            sorted(set(np.round(arr[:, 4] * s_real, 6).tolist())) == [2.0, 6.0],
            str(sorted(set(np.round(arr[:, 4] * s_real, 6).tolist()))))
    else:                                                      # pragma: no cover
        bad.append('⑥ real14_am_scaffold.csv 가 없다 — 규약 대조를 건너뛸 수 없다')

    print(f'viz_additives selftest: {ok}/{ok + len(bad)} PASS')
    for b in bad:
        print('  ✗', b)
    return 0 if not bad else 1


#: AM scaffold CSV 의 길이 단위 후보 → µm 환산 배수.
#  우리 scaffold 헤더가 *"LIGGGHTS box units (lateral 0..0.05 = 50um)"* 라고 적는다
#  ⇒ 1 단위 = 1 mm.  µm 로 저장된 것도 있을 수 있어 둘 다 둔다.
_AM_UNIT_UM = {'mm': 1e3, 'um': 1.0, 'm': 1e6}


def am_scale_to_um(xy, box_um, unit='auto'):
    """AM scaffold 좌표 → µm 배수.  `auto` 는 **상자 폭에 맞춰** 고르고 검증한다.

    ⚠⚠ 2026-08-29 실사고: 옛 코드가 `v*1e6 if v < 1 else v` 라는 **크기 휴리스틱**을 썼다.
    우리 scaffold 는 mm 라 0.025 → **25,033 µm** 가 되고, 축은 0–50 이라 **AM 원이 전부
    화면 밖으로 나갔다.**  경고는 없다 — 그림은 그냥 AM 이 없는 것처럼 보인다.
    상 누락(위 `_STYLE` 주석)과 **같은 부류**이고, Figure 4a 는 AM 골격이 요지의 절반이다.
    ⇒ 배수를 고른 뒤 **정말 상자 안에 들어오는지 확인**하고, 아니면 거부한다.
    """
    xy = np.asarray(xy, dtype=float)
    if unit != 'auto':
        if unit not in _AM_UNIT_UM:
            raise SystemExit(f'⛔ --am-units {unit} 은 모른다 (auto/mm/um/m)')
        s = _AM_UNIT_UM[unit]
    else:
        span = float(np.nanmax(xy) - np.nanmin(xy))
        if not np.isfinite(span) or span <= 0:
            raise SystemExit('⛔ AM scaffold 의 좌표 폭이 0 이다 — 단위를 정할 수 없다')
        #  상자 폭에 **가장 가깝게** 만드는 배수 (로그 거리로 고른다)
        s = min(_AM_UNIT_UM.values(), key=lambda m: abs(math.log((span * m) / box_um)))
    out = xy * s
    lo, hi = float(np.nanmin(out)), float(np.nanmax(out))
    if lo < -0.05 * box_um or hi > 1.05 * box_um:
        name = next((k for k, v in _AM_UNIT_UM.items() if v == s), s)
        raise SystemExit(
            f'⛔ AM scaffold 를 {name} 로 읽으면 좌표가 {lo:.3g}~{hi:.3g} µm 라 '
            f'상자 0~{box_um:g} µm 밖이다 — 그대로 그리면 **AM 이 화면 밖으로 사라진다**.  '
            '`--am-units` 로 단위를 지정할 것.')
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--se', default=''); ap.add_argument('--phase', default='')
    ap.add_argument('--am', default=''); ap.add_argument('--lateral-box', type=float, default=50.0)
    ap.add_argument('--demo', action='store_true')
    ap.add_argument('--slab', default='0.45,0.55', help='z-slab fraction to show (clarity)')
    ap.add_argument('--out', default='docs/figures/additives_preview.png')
    ap.add_argument('--allow-undrawn', action='store_true',
                    help='표시 규약이 없는 상을 빼고 그린다 — 진단 전용, 그림 산출 금지')
    ap.add_argument('--am-units', default='auto', choices=('auto', 'mm', 'um', 'm'),
                    help='AM scaffold CSV 의 길이 단위.  auto 는 상자 폭에 맞춰 고르고 검증한다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(selftest())
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle
    rng = np.random.default_rng(1)
    fig, ax = plt.subplots(figsize=(8, 8))

    if a.demo:
        am, fib, sp = _demo(rng)
        box = 50.0
        for x, y, z, r in am:
            ax.add_patch(Circle((x, y), r, fc='#5a6b7a', ec='#33414d', alpha=0.85, zorder=1))
        ax.scatter(sp[:, 0], sp[:, 1], s=8, c='#777777', alpha=0.6, zorder=2, label='Super P')
        ax.scatter(fib[:, 0], fib[:, 1], s=5, c='#111111', zorder=3, label='VGCF')
        ax.set_title('Stage-1 additive morphology — PREVIEW (synthetic)\n'
                     'AM skeleton + VGCF fibres threading interstices + Super P', fontsize=11)
    else:
        se = np.load(a.se); ph = np.load(a.phase)
        #  ★ fail-closed — 모르는 상이 있으면 **그리지 않고 멈춘다** (위 주석의 사고).
        _un = undrawn_codes(ph)
        if _un and not a.allow_undrawn:
            raise SystemExit(
                f'⛔ 자료에 표시 규약이 없는 상 코드 {_un} 이 있다 — 그대로 그리면 '
                '그 상이 **그림에서 사라진 채 아무 표시도 남지 않는다**.  '
                '`_STYLE`(=`additives.PHASE`) 를 맞추거나, 진단 목적이면 --allow-undrawn.')
        if _un:
            print(f'⚠ --allow-undrawn: 상 코드 {_un} 을 그리지 않는다 (진단 전용)')
        box = a.lateral_box
        # the MPM se.npy is in box units [0,1] lateral; map to µm if a lateral-box given
        sx, sy, sz = se[:, 0], se[:, 1], se[:, 2]
        zlo, zhi = (float(v) for v in a.slab.split(','))
        m = (sz >= sz.min() + zlo * (sz.max() - sz.min())) & (sz <= sz.min() + zhi * (sz.max() - sz.min()))
        um = box / (sx.max() - sx.min() + 1e-9)
        if a.am:
            amr = np.loadtxt(a.am, delimiter=',', comments='#', ndmin=2)
            #  ★ 크기 휴리스틱이 아니라 **상자 폭에 맞춰 고르고 검증한 배수** (am_scale_to_um)
            s_am = am_scale_to_um(amr[:, 1:3], box, a.am_units)
            print(f'AM scaffold {len(amr)}개 · 배수 x{s_am:g} → '
                  f'{amr[:, 1].min() * s_am:.2f}~{amr[:, 1].max() * s_am:.2f} µm')
            for row in amr:
                ax.add_patch(Circle((row[1] * s_am, row[2] * s_am), row[4] * s_am,
                                    fc='#5a6b7a', ec='none', alpha=0.5, zorder=1))
        for code, (c, lab, ms) in COL.items():
            sel = m & (ph == code)
            if sel.any():
                ax.scatter((sx[sel] - sx.min()) * um, (sy[sel] - sy.min()) * um, s=ms, c=c,
                           alpha=0.7, label=f'{lab} ({int(sel.sum())})', zorder=COL[code][2])
        ax.set_title(f'Stage-1 additive morphology — {a.se}\nz-slab {a.slab} (top-down x–y)', fontsize=10)

    ax.set_xlim(0, box); ax.set_ylim(0, box); ax.set_aspect('equal')
    ax.set_xlabel('x (µm)'); ax.set_ylabel('y (µm)'); ax.legend(loc='upper right', fontsize=9)
    import os
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    fig.tight_layout(); fig.savefig(a.out, dpi=130)
    print(f'saved {a.out}')


if __name__ == '__main__':
    main()
