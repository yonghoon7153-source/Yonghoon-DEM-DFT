#!/usr/bin/env python3
"""상별 부피 원장 종합 — CL-25 의 단입자 산술을 **실침대 실측**으로 대체하고,
CL-34 의 우선순위 결함 크기를 **솔브 없이** 상계 아닌 실측으로 준다.

★ 왜 (심층 리뷰 ③): CL-34 의 "최대 39 %" 상계는 세 겹으로 무너졌다 —
  PTFE 는 선분 스탬프라 점≠셀 · dof 원장이 σ-치환 채널을 못 봄 · 증가분이 정당 구부피로도
  전액 설명 가능.  ⇒ 상계 대신 **직접 세는** 것이 답이고, 그것은 래스터만으로 된다.

★ 무엇을 읽나 (`--step3-rasterize-only` 가 쓴 JSON):
  · `cells_by_sid` — 상별 셀 수 (실침대, 충돌·overwrite **포함**)
  · `sphere_extra_from_sid` — 구 스탬프가 점 대비 **추가로** 차지한 셀의 **원래 상**
      그 중 sid 7(PTFE)·8(SWCNT) = 결함판에서 SDCP 가 **덮었을** 셀 = 결함의 크기

사용:  python3 scripts/sdcp_phase_ledger_report.py --dir phase_ledger
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os

SID = {0: 'pore', 1: 'AM_S', 2: 'AM_P', 3: 'VGCF', 4: 'SuperP', 5: 'SDCP',
       6: 'SE', 7: 'PTFE', 8: 'SWCNT'}
SDCP_D = 0.30
V_TRUE = math.pi / 6.0 * SDCP_D ** 3          # 0.014137 µm³


def load(d):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, 'ledger_*.json'))):
        out[os.path.basename(p)[len('ledger_'):-len('.json')]] = json.load(open(p, encoding='utf-8'))
    return out


def report(led, n_sdcp_pts=None):
    lines = []
    for tag in sorted(led):
        r = led[tag]
        vox = r['vox_um']
        c = {int(k): v for k, v in r['cells_by_sid'].items()}
        tot = sum(c.values())
        lines.append(f"── {tag}  (vox {vox} · 격자 {r['grid_shape']} · {tot:,} 셀)")
        for k in sorted(c):
            lines.append(f"     sid {k} {SID.get(k, '?'):7s} {c[k]:>12,} 셀  "
                         f"{c[k] * vox ** 3:>12,.1f} µm³  {100.0 * c[k] / tot:>6.3f} %")
        if 5 in c and n_sdcp_pts:
            v = c[5] * vox ** 3
            lines.append(f"     ★ SDCP 표현부피 / 참부피 = "
                         f"{v / (n_sdcp_pts * V_TRUE):.3f}  "
                         f"(단입자 산술 {vox ** 3 / V_TRUE:.2f} 와 비교 — 차이가 곧 "
                         f"셀 충돌·상 overwrite 몫)")
        if 'sphere_extra_from_sid' in r:
            ex = {int(k): v for k, v in r['sphere_extra_from_sid'].items()}
            steal = {k: v for k, v in ex.items() if k in (7, 8)}
            lines.append(f"     ★ 구 스탬프 추가 셀 {r['sphere_extra_cells']:,} — 원래 상: "
                         + ', '.join(f'{SID.get(k, k)} {v:,}' for k, v in sorted(ex.items())))
            n_st = sum(steal.values())
            lines.append(f"     ★★ **결함판이 뺏었을 PTFE/SWCNT = {n_st:,} 셀** "
                         f"({100.0 * n_st / max(r['sphere_extra_cells'], 1):.2f} % of 추가분)"
                         + ('  ⇒ 결함 크기 = 이만큼의 절연 셀이 σ 250 도체가 됐다는 것'
                            if n_st else '  ⇒ **결함 없음** (겹친 PTFE/SWCNT 셀이 0)'))
        lines.append('')
    return lines


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='phase_ledger')
    ap.add_argument('--n-sdcp-pts', type=int, default=138988,
                    help='DBE SDCP 점 수 (원격 로그 실측 138,988)')
    a = ap.parse_args()
    led = load(a.dir)
    if not led:
        raise SystemExit(f'원장 없음: {a.dir}/ledger_*.json')
    print('\n'.join(report(led, a.n_sdcp_pts)))
    print('⚠ 이 원장은 **래스터만** 이다 — σ 영향은 대조 팔(솔브)이 준다.  '
          '다만 결함이 건드린 셀이 몇 개인지는 여기서 **정확히** 나온다 (상계 아님).')
