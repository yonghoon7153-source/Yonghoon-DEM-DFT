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

SID_SDCP, SID_VGCF = 5, 3
VGCF_D_UM = 0.15                 # 공칭 Ø (dia_rel 실측 min=med=max=1.0, cv=0)
SIGMA_VGCF_BULK = 100.0          # S/cm — 재척도 **전** 벌크값
SIGMA_SDCP = 250.0               # S/cm — 입자라 재척도 **없음** (섬유만 직경-보존 재척도)


def sigma_vgcf_at(vox_um, d_um=VGCF_D_UM, sigma_bulk=SIGMA_VGCF_BULK):
    """직경-보존 재척도 (step3_sigma.diameter_preserving_sigma 와 같은 식, dia_rel≡1)."""
    return sigma_bulk * math.pi * d_um * d_um / (4.0 * float(vox_um) ** 2)


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


# ─────────────────────────────────────────────────────────────────────────────
# ★ SBE ↔ DBE 상 치환 (2026-08-18) — "SDCP 셀은 **어느 상**을 밀어냈나"
#
# 왜 이것이 필요한가: 심층 리뷰 ③ 이 지적한 대로 **dof 원장은 σ-치환 채널을 원리적으로
# 못 본다** — SDCP 가 VGCF 셀 위에 찍히면 도체 셀 수(dof)는 그대로인데 그 셀의 σ 만
# 올라간다.  상별 셀 수를 SBE 와 나란히 빼면 그 채널이 **보인다**.
#
# ⚠ 세 겹으로 조심할 것:
#  ① Σ(밀려난 셀) = SDCP 셀 수 는 **항등식**이다 (두 침대의 격자 총 셀 수가 같으므로).
#     전사 오류 검사로만 쓸 것 — 물리 증거가 **아니다**.
#  ② SBE 와 DBE 는 **다른 침대**다 (따로 압밀).  차이에는 SDCP 의 래스터 overwrite 뿐
#     아니라 "SDCP 가 자리를 차지한 채로 압밀돼 VGCF/SE 가 다르게 놓인" 몫도 섞인다.
#     ⇒ "SDCP 가 이 상을 덮었다" 가 아니라 "**SDCP 가 있는 침대에서 이 상이 이만큼
#     줄었다**" 가 정확한 서술이다.
#  ③ 그래서 우연 기대치(그 상의 부피분율)로 나눈 **enrichment** 를 같이 본다 — 절대
#     몫은 격자에 따라 크게 움직이지만 enrichment 는 그렇지 않다면, 움직인 것은
#     "SDCP 의 선호" 가 아니라 "그 상 자신의 표현 부피" 다.
# ─────────────────────────────────────────────────────────────────────────────
def _split_tag(tag):
    """'DBE_v04_pt' → ('DBE', 'v04_pt').  침대 접두어가 없으면 (None, tag)."""
    for bed in ('SBE', 'DBE'):
        if tag.startswith(bed + '_'):
            return bed, tag[len(bed) + 1:]
    return None, tag


def displacement(led):
    """같은 (vox, 스탬프) 의 SBE↔DBE 쌍마다 상 치환 표를 만든다.  리스트[dict] 반환."""
    pairs = {}
    for tag in led:
        bed, key = _split_tag(tag)
        if bed:
            pairs.setdefault(key, {})[bed] = led[tag]
    out = []
    for key in sorted(pairs, key=lambda k: -float(pairs[k][next(iter(pairs[k]))]['vox_um'])):
        p = pairs[key]
        if 'SBE' not in p or 'DBE' not in p:
            continue
        s = {int(k): v for k, v in p['SBE']['cells_by_sid'].items()}
        d = {int(k): v for k, v in p['DBE']['cells_by_sid'].items()}
        vox = float(p['DBE']['vox_um'])
        n_sdcp = d.get(SID_SDCP, 0)
        tot_s, tot_d = sum(s.values()), sum(d.values())
        disp = {k: s[k] - d.get(k, 0) for k in sorted(s)}
        rows = []
        for k, n in disp.items():
            share = n / n_sdcp if n_sdcp else float('nan')
            ref = s[k] / tot_s if tot_s else float('nan')
            rows.append({'sid': k, 'phase': SID.get(k, str(k)), 'cells_displaced': n,
                         'share_of_sdcp': share, 'chance_frac_in_SBE': ref,
                         'enrichment': (share / ref) if ref else float('nan')})
        sub = next((r for r in rows if r['sid'] == SID_VGCF), None)
        sv = sigma_vgcf_at(vox)
        out.append({
            'key': key, 'vox_um': vox, 'sdcp_cells': n_sdcp,
            'grid_cells_SBE': tot_s, 'grid_cells_DBE': tot_d,
            'sum_identity_ok': (tot_s == tot_d) and (sum(disp.values()) == n_sdcp),
            'rows': rows,
            'sigma_vgcf_rescaled_S_cm': sv,
            'sigma_sdcp_over_vgcf': SIGMA_SDCP / sv if sv else float('nan'),
            'sigma_substitution_intensity': (sub['share_of_sdcp'] * SIGMA_SDCP / sv)
            if (sub and sv) else float('nan'),
        })
    return out


def displacement_report(led):
    dp = displacement(led)
    if not dp:
        return ['(SBE↔DBE 쌍 없음 — 치환 표를 못 만든다)']
    L = ['══ SDCP 셀은 어느 상을 밀어냈나 (SBE − DBE) ══════════════════', '']
    for e in dp:
        flag = '' if e['sum_identity_ok'] else '   ⚠ 합계 항등식 실패 (전사 오류?)'
        L.append(f"── {e['key']}  (vox {e['vox_um']} · SDCP {e['sdcp_cells']:,} 셀){flag}")
        L.append(f"     {'상':<8}{'밀려난 셀':>12}{'SDCP 몫':>10}{'우연 기대':>10}{'enrich':>9}")
        for r in e['rows']:
            L.append(f"     {r['phase']:<8}{r['cells_displaced']:>12,}"
                     f"{100 * r['share_of_sdcp']:>9.1f} %{100 * r['chance_frac_in_SBE']:>9.1f} %"
                     f"{r['enrichment']:>9.2f}")
        L.append(f"     σ_VGCF(재척도) = {e['sigma_vgcf_rescaled_S_cm']:.2f} S/cm  →  "
                 f"σ_SDCP/σ_VGCF = **{e['sigma_sdcp_over_vgcf']:.1f}×**  ·  "
                 f"σ-치환 강도(몫×배수) = **{e['sigma_substitution_intensity']:.2f}**")
        L.append('')
    L += [
        '★ 읽는 법:',
        '  · **합계는 항등식**이다 (격자 총 셀 수가 같다) — 전사 검사일 뿐 증거가 아니다.',
        '  · SBE↔DBE 는 **다른 침대**다 → "SDCP 가 덮었다" 가 아니라 "SDCP 가 있는 침대에서',
        '    이 상이 이만큼 적다" 가 정확한 서술.  래스터 overwrite 와 압밀 재배치가 섞여 있다.',
        '  · **enrichment** = SDCP 몫 / 그 상의 부피분율.  1 보다 크면 SDCP 가 그 상 자리에',
        '    우연보다 자주 앉는다는 뜻.  격자를 바꿔도 안 변하면 그것이 구조적 사실이고,',
        '    절대 몫만 변했다면 변한 것은 **그 상 자신의 표현 부피**다 (DR3-06).',
        '  · **σ-치환 강도** = VGCF 몫 × (σ_SDCP/σ_VGCF).  섬유 σ 는 직경-보존으로 격자마다',
        '    재척도되는데 입자 σ 는 **안 된다** → 대비 자체가 vox 의 함수다 (DR3-05).',
        '    ⚠ 이것은 셀 수와 σ 규약으로 만든 **산술 지표**이지 σ_e 기여 측정이 아니다.',
        '    판별 팔: σ_SDCP := σ_VGCF(vox) 로 맞춘 "σ-매칭 SDCP" 음성 대조 (§ 아래).',
        '  · **왜 VGCF 에만 이 지표를 붙이나**: 재척도를 받는 상이 VGCF 하나뿐이라서다.',
        '    AM_S 를 밀어내는 것도 큰 σ 상승이지만(σ_AM ≪ σ_SDCP) 그 **대비는 격자 불변**이고',
        '    몫도 11.8 → 7.1 % 로 1.7배밖에 안 움직인다 ⇒ 관측된 이득의 26배 스윙을 못 만든다.',
        '    VGCF 채널만 몫(5.5×)과 대비(7.1×)가 **같은 방향으로** 곱해져 39배 움직인다.',
    ]
    return L


def _selftest():
    """합성 원장으로 표의 산술을 검증 — 실측 파일 없이 돈다."""
    ok = 0

    def mk(vox, cells):
        return {'vox_um': vox, 'grid_shape': [1, 1, 1], 'cells_by_sid': {str(k): v for k, v in cells.items()}}

    # ① 합계 항등식 + 몫/enrichment 산술
    led = {'SBE_vX': mk(0.4, {0: 100, 3: 200, 6: 700}),
           'DBE_vX': mk(0.4, {0: 90, 3: 150, 5: 100, 6: 660})}
    e = displacement(led)[0]
    assert e['sum_identity_ok'] and e['sdcp_cells'] == 100, e
    r = {x['sid']: x for x in e['rows']}
    assert r[3]['cells_displaced'] == 50 and abs(r[3]['share_of_sdcp'] - 0.5) < 1e-12
    assert abs(r[3]['chance_frac_in_SBE'] - 0.2) < 1e-12
    assert abs(r[3]['enrichment'] - 2.5) < 1e-12
    ok += 1

    # ② 항등식이 깨지면 (총 셀 수 불일치) 플래그가 선다 — 조용히 넘어가면 안 된다
    led2 = {'SBE_vY': mk(0.4, {0: 100, 6: 700}),
            'DBE_vY': mk(0.4, {0: 90, 5: 100, 6: 660})}
    assert displacement(led2)[0]['sum_identity_ok'] is False
    ok += 1

    # ③ 직경-보존 재척도 — CLAUDE.md 정본값 11.0447 @ vox 0.4
    assert abs(sigma_vgcf_at(0.4) - 11.0447) < 1e-3, sigma_vgcf_at(0.4)
    assert abs(sigma_vgcf_at(0.15) - 78.5398) < 1e-3, sigma_vgcf_at(0.15)
    ok += 1

    # ④ σ 대비는 vox 의 함수 — 거친 격자일수록 크다 (DR3-05)
    assert sigma_vgcf_at(0.4) < sigma_vgcf_at(0.15)
    assert (SIGMA_SDCP / sigma_vgcf_at(0.4)) > (SIGMA_SDCP / sigma_vgcf_at(0.15))
    ok += 1

    # ⑤ 짝 없는 침대는 조용히 버린다 (SBE 만 있는 격자)
    led3 = dict(led); led3['SBE_vZ'] = mk(0.3, {0: 10, 6: 90})
    assert len(displacement(led3)) == 1
    ok += 1

    # ⑥ 상이 **늘어난** 경우(음수 치환)도 그대로 보고한다 — 클립하지 않는다
    led4 = {'SBE_vW': mk(0.4, {0: 100, 3: 200, 6: 700}),
            'DBE_vW': mk(0.4, {0: 120, 3: 150, 5: 100, 6: 630})}
    r4 = {x['sid']: x for x in displacement(led4)[0]['rows']}
    assert r4[0]['cells_displaced'] == -20, r4[0]
    ok += 1

    # ⑦ 태그 분해
    assert _split_tag('DBE_v015_sph') == ('DBE', 'v015_sph')
    assert _split_tag('nobed_v04') == (None, 'nobed_v04')
    ok += 1
    print(f'selftest {ok}/7 PASS')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--dir', default='phase_ledger')
    ap.add_argument('--n-sdcp-pts', type=int, default=138988,
                    help='DBE SDCP 점 수 (원격 로그 실측 138,988)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        _selftest()
        raise SystemExit(0)
    led = load(a.dir)
    if not led:
        raise SystemExit(f'원장 없음: {a.dir}/ledger_*.json')
    print('\n'.join(report(led, a.n_sdcp_pts)))
    print('\n'.join(displacement_report(led)))
    print('⚠ 이 원장은 **래스터만** 이다 — σ 영향은 대조 팔(솔브)이 준다.  '
          '다만 결함이 건드린 셀이 몇 개인지는 여기서 **정확히** 나온다 (상계 아님).')
