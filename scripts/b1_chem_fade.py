#!/usr/bin/env python3
"""B-1 화학(CEI) N-전개 → 총 R_int(N) = ledger 접촉 + B-1 화학 (STEP5, 2026-07-23).

접촉-기계 fade(ledger, ~2%)는 작으니 진짜 열화는 화학 계면상(CEI) 성장이 지배(~98%).  이 도구는:
  총 R_int(N) = R_int_0 + ΔR_contact(N)[ledger 실측 shape] + ΔR_chem(N)[CEI 성장법칙]
을 실험 총 R_int 끝점(예: 너 랩 SBE 6.1×/DBE 3.8× @1000cyc)에 **앵커**해 궤적을 낸다.

★ 정직 (적대리뷰 교훈):
  - **끝점(magnitude)은 실험 앵커** (defensible).
  - **모양(shape)은 ASSUMED-FORM**: √N(확산제한 CEI 두께, 기본) or 선형(--shape linear).  검증 =
    실험 R_int(N) **곡선**(≥4 N점) 필요 — 끝점 하나론 √N/선형 구별 불가(--shape 스윕으로 노출).
  - **접촉 몫은 ledger 실측**(fade JSON), 화학 = 나머지(=총−접촉) → 접촉/화학 분해가 정직.
  - 흑연-SEI 계수 이식 금지(N1); √N은 CEI 두께 일반형만.

사용:
  python3 scripts/b1_chem_fade.py --fade fade_real14.json --rint0 18 --rint-exp-x 6.1 \
      --n-exp 1000 --r-contact0 2.0 --shape sqrt --label SBE --out rint_N_SBE
"""
import argparse
import json
import sys


def _shape(N, n_exp, kind, p=1.5):
    """정규화 성장 모양 (N=0→0, N=n_exp→1; 어떤 shape든 끝점=1 → magnitude 앵커 불변).
      • sqrt   = 확산제한 CEI/Wagner (지수 0.5) — Park2023 '코팅' 셀의 R∝√t 형태.
      • linear = 일정속도 (지수 1.0).
      • power  = 가속(super-√N, 지수 p>1 기본 1.5) — Park2023 '비코팅'(bare) 파라볼릭:
                 접촉손실이 화학 위에 얹혀 후기 가속.  ★√N 두 채널 합으론 못 만드는 모양."""
    frac = max(0.0, float(N) / n_exp if n_exp else 0.0)
    if kind == 'sqrt':
        return frac ** 0.5
    if kind == 'linear':
        return frac
    if kind == 'power':
        return frac ** max(0.05, float(p))
    raise ValueError(kind)


# shape provenance 라벨 — ★리뷰 반영: √N은 '문헌앵커'(=실험검증 magnitude 급) 아님.  Park2023 지지는
# [B] text-stated(snippet, PDF 미검증)이고 '코팅' 셀 한정(bare=파라볼릭) → '문헌지지 [B]'로 하향.
_SHAPE_KO = {'sqrt': '√N (확산제한 Wagner form — Park2023 코팅셀 R∝√t 문헌지지 [B]; bare엔 power 권장)',
             'linear': 'linear (ASSUMED)',
             'power': '가속 super-√N (Park2023 bare 파라볼릭 — 접촉손실 후기 가속)'}
_SHAPE_EN = {'sqrt': 'sqrt-N (Wagner form, Park2023 coated [B]; bare->use power)',
             'linear': 'linear (ASSUMED)',
             'power': 'accelerating power (Park2023 bare parabolic)'}


def _shape_label(out, en=False):
    base = (_SHAPE_EN if en else _SHAPE_KO).get(out['shape'], out['shape'])
    if out['shape'] == 'power':
        base += ' (p=%.2f)' % out.get('chem_p', 1.5)
    return base


def _assemble(rct_rel_at, extra_Ns, rint0, rint_exp_x, n_exp, r_contact0, shape, chem_x, chem_p=1.5,
              carbon_se_area=0.0, k_cat_carbon=0.0, vgcf_wt=0.0):
    """공통 조립 코어: 접촉 rel 콜백(rct_rel_at) + 화학/OTHER 분해 → 궤적 rows.
    trajectory()(ledger JSON 접촉궤적)와 trajectory_scalar()(스칼라 끝점)가 **둘 다 이 코어**를
    호출 = 단일 소스(분해 로직 중복 금지, 웹패널↔CLI 발산 방지).

    ★분해 정직 (리뷰 반영): magnitude(끝점)만 앵커, 채널 SPLIT은 가정(r_contact0·chem_x 미측정).
      bare(chem_x=None)에서 '화학'은 실은 '총−접촉' 잔차(=CEI 지배 가정, 상한).  입력 비정합
      (접촉/화학 > 총)이면 inconsistent=True 로 노출(shares 조작 안 함).

    ★#30 VGCF carbon-촉매 SE분해 (k_cat_carbon>0 일 때만): 화학 채널을 carbon-촉매몫 + baseline-CEI
      몫으로 **분해**(kim2024 3상계면 촉매·cho2024 R_int 2.1×@100cyc).  ★이중계산 가드: 실험 끝점
      (rint_exp_x)은 with-carbon 셀 측정 = carbon 효과 이미 포함 → carbon몫을 화학 위에 **더하지 않고
      SPLIT**(carbon = min(화학, k·area·wt), baseline = 화학−carbon).  k_cat_carbon=0 = 기본 = 무영향."""
    dR_total_exp = rint0 * (rint_exp_x - 1.0)                 # 실험 총 성장 Δ (Ω·cm²) @ n_exp
    dR_contact_exp = r_contact0 * (rct_rel_at(n_exp) - 1.0)   # 접촉 몫 @ n_exp (ledger, ★하한 = frozen-AM)
    if chem_x is None:
        dR_chem_exp = max(0.0, dR_total_exp - dR_contact_exp)  # bare: 화학=잔차(=총−접촉, 상한 가정)
        dR_other_exp = 0.0
    else:                                                     # 코팅 인식: 화학=명시(억제), OTHER=나머지
        dR_chem_exp = rint0 * (chem_x - 1.0)
        dR_other_exp = max(0.0, dR_total_exp - dR_contact_exp - dR_chem_exp)   # 접촉초과이탈·SE분해·Li (모델 밖)
    # 화학 채널 내부 분해 (carbon-촉매 vs baseline) — 앵커 초과 방지 min() = 더하기 아닌 쪼개기
    dR_chem_carbon_exp = min(dR_chem_exp, max(0.0, k_cat_carbon) * max(0.0, carbon_se_area) * max(0.0, vgcf_wt))
    dR_chem_base_exp = max(0.0, dR_chem_exp - dR_chem_carbon_exp)
    # 입력 비정합 판정: 총 성장이 비양수(exp_x≤1)이거나, 접촉/명시화학이 총을 초과 → shares 무의미
    inconsistent = (dR_total_exp <= 1e-9
                    or dR_contact_exp > dR_total_exp + 1e-9
                    or (chem_x is not None and dR_chem_exp > dR_total_exp + 1e-9))

    Ns = sorted(set([0] + list(extra_Ns) + [n_exp, n_exp // 10, n_exp // 4, n_exp // 2]))
    rows = []
    for N in Ns:
        dR_contact = r_contact0 * (rct_rel_at(N) - 1.0)
        dR_chem = dR_chem_exp * _shape(N, n_exp, shape, chem_p)      # ★shape ASSUMED, endpoint 앵커
        dR_other = dR_other_exp * _shape(N, n_exp, shape, chem_p)    # OTHER도 같은 모양(미상)
        R = rint0 + dR_contact + dR_chem + dR_other
        rows.append({'N': N, 'R_int': R, 'dR_contact': dR_contact, 'dR_chem': dR_chem,
                     'dR_other': dR_other, 'R_int_x': R / rint0, 'ledger_rct_rel': rct_rel_at(N)})
    denom = max(dR_total_exp, 1e-9)
    return {'rows': rows, 'rint0': rint0, 'rint_exp_x': rint_exp_x, 'n_exp': n_exp,
            'r_contact0': r_contact0, 'shape': shape, 'chem_x': chem_x, 'chem_p': chem_p,
            'inconsistent': bool(inconsistent),
            'chem_share_pct': 100.0 * dR_chem_exp / denom,
            'contact_share_pct': 100.0 * dR_contact_exp / denom,
            'other_share_pct': 100.0 * dR_other_exp / denom,
            # #30: 화학 채널 내부 분해 (carbon-촉매 vs baseline-CEI).  carbon_frac = 화학 중 carbon 몫.
            'chem_carbon_share_pct': 100.0 * dR_chem_carbon_exp / denom,
            'chem_base_share_pct': 100.0 * dR_chem_base_exp / denom,
            'chem_carbon_frac': (dR_chem_carbon_exp / dR_chem_exp) if dR_chem_exp > 1e-12 else 0.0,
            'carbon_se_area': carbon_se_area, 'k_cat_carbon': k_cat_carbon, 'vgcf_wt': vgcf_wt}


def trajectory(fade_json, rint0, rint_exp_x, n_exp, r_contact0, shape, chem_x=None, chem_p=1.5,
               carbon_se_area=0.0, k_cat_carbon=0.0, vgcf_wt=0.0):
    """chem_x=None → 화학=나머지(bare NCM 가정, 옛 방식).  chem_x 지정 → 화학 성장 ×를 명시
    (코팅 NCM = CEI 억제 → 작게) → 나머지 = OTHER(골격재배열·SE분해·Li쪽 = 우리 모델 밖).
    접촉 채널 = ledger fade JSON 의 rct_holm_rel 궤적(앵커 N점 사이 선형보간)."""
    d = json.load(open(fade_json))
    tr = d['trajectory']
    ledger_rct = {r['cycle']: r['rct_holm_rel'] for r in tr}
    ks = sorted(ledger_rct)

    def rct_rel_at(N):
        # ledger R_ct rel 보간 (앵커 N점 사이 = ledger 자체 궤적, 최근접-계단은 피하고 선형)
        if N <= ks[0]:
            return ledger_rct[ks[0]]
        if N >= ks[-1]:
            return ledger_rct[ks[-1]]
        for i in range(len(ks) - 1):
            if ks[i] <= N <= ks[i + 1]:
                t = (N - ks[i]) / (ks[i + 1] - ks[i])
                return ledger_rct[ks[i]] * (1 - t) + ledger_rct[ks[i + 1]] * t
        return ledger_rct[ks[-1]]

    return _assemble(rct_rel_at, ks, rint0, rint_exp_x, n_exp, r_contact0, shape, chem_x, chem_p,
                     carbon_se_area=carbon_se_area, k_cat_carbon=k_cat_carbon, vgcf_wt=vgcf_wt)


def trajectory_scalar(rint0, rint_exp_x, n_exp, r_contact0, shape, chem_x=None,
                      ledger_end_x=1.1, ledger_shape='sqrt', chem_p=1.5,
                      carbon_se_area=0.0, k_cat_carbon=0.0, vgcf_wt=0.0):
    """웹패널/스크립트용: ledger fade JSON 없이 접촉 채널을 **스칼라 끝점**(ledger_end_x, 예 1.1×)
    + ledger_shape 로 해석 → contact rct_rel(N) = 1 + (ledger_end_x−1)·shape_ledger(N).  나머지
    화학/OTHER 분해는 trajectory()와 동일 코어(_assemble).  ★ledger_end_x 는 A-3 ledger 실측(하한)에서
    가져와 넣는 값 — 여기선 파라미터(웹 슬라이더).  MPM 스캐폴드가 ledger 입력과 호환 안 되므로
    (mm·type-2 SE) 이 스칼라 경로가 웹 인터랙티브의 올바른 표면.
    ledger_shape 는 접촉 채널 모양(문서상 R_ct 는 포화 경향 — 접촉몫이 작아 영향 미미, 기본 sqrt)."""
    end = max(1.0, float(ledger_end_x))

    def rct_rel_at(N):
        return 1.0 + (end - 1.0) * _shape(N, n_exp, ledger_shape, chem_p)

    return _assemble(rct_rel_at, [n_exp // 20, n_exp // 5], rint0, rint_exp_x, n_exp,
                     r_contact0, shape, chem_x, chem_p,
                     carbon_se_area=carbon_se_area, k_cat_carbon=k_cat_carbon, vgcf_wt=vgcf_wt)


def _report(out, label):
    print('=' * 88)
    _shp = _shape_label(out)
    if out.get('inconsistent'):
        print('  ⚠ 입력 비정합: 접촉/명시화학 몫이 실험 총 성장을 초과(또는 exp_x≤1) → shares 무의미.')
    print(f'B-1 화학 N-전개 → 총 R_int(N)  [{label}]  ★shape={_shp} · endpoint 실험앵커')
    print('-' * 88)
    print(f"  {'N':>6} {'R_int(Ω·cm²)':>13} {'×pristine':>10} {'ΔR_chem':>9} {'ΔR_contact':>11}")
    for r in out['rows']:
        print(f"  {r['N']:>6} {r['R_int']:>13.1f} {r['R_int_x']:>10.2f} {r['dR_chem']:>9.1f} {r['dR_contact']:>11.2f}")
    print('-' * 88)
    if out['chem_x'] is None:
        print(f"  분해 @N{out['n_exp']}: 화학+기타(잔차) {out['chem_share_pct']:.1f}% / 접촉-기계 {out['contact_share_pct']:.1f}% "
              f"(★bare = 화학이 잔차[총−접촉] = CEI 지배 가정·상한; OTHER 0 가정)  ·  R_int0={out['rint0']} → ×{out['rint_exp_x']}")
    else:
        print(f"  분해 @N{out['n_exp']}: 화학 {out['chem_share_pct']:.1f}%(코팅 억제, ×{out['chem_x']}) / "
              f"접촉-기계 {out['contact_share_pct']:.1f}%(ledger 하한) / ★OTHER {out['other_share_pct']:.1f}% "
              f"(골격재배열·SE분해·Li — 우리 모델 밖)  ·  R_int0={out['rint0']} → ×{out['rint_exp_x']}")
        print(f"  ⚠ 코팅 NCM = CEI 억제 → 화학 작음 → 나머지 OTHER가 지배 = 현 모델(화학·frozen-AM 접촉) 미포착 gap.")
    print(f"  ⚠ shape(√N vs 선형)는 끝점 하나론 구별 불가 — 실험 R_int(N) 곡선(≥4점)으로 검증.  --shape 스윕 권장.")
    print('=' * 88)


def _plot(out, label, prefix):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        return
    rows = out['rows']
    N = [r['N'] for r in rows]
    Rc = [out['rint0'] for _ in rows]                        # baseline
    Rcon = [out['rint0'] + r['dR_contact'] for r in rows]
    Rchem = [out['rint0'] + r['dR_contact'] + r['dR_chem'] for r in rows]
    Rtot = [r['R_int'] for r in rows]
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.fill_between(N, 0, Rc, color='#bdc3c7', label='R_int_0 (pristine)')
    ax.fill_between(N, Rc, Rcon, color='#2980b9', label='+ contact-mech (ledger, ~%.0f%%)' % out['contact_share_pct'])
    ax.fill_between(N, Rcon, Rchem, color='#e67e22', label='+ chemical CEI (~%.0f%%)' % out['chem_share_pct'])
    if out['chem_x'] is not None and out.get('other_share_pct', 0) > 0.5:
        ax.fill_between(N, Rchem, Rtot, color='#c0392b', alpha=0.55,
                        label='+ OTHER unmodeled (~%.0f%%: skeleton/SE/Li)' % out['other_share_pct'])
    ax.plot(N, Rtot, 'k-o', lw=1.5, ms=3, label='total R_int(N)')
    ax.axhline(out['rint0'] * out['rint_exp_x'], color='#c0392b', ls='--', lw=1,
               label='exp anchor x%.1f @N%d' % (out['rint_exp_x'], out['n_exp']))
    ax.set_xlabel('cycle N')
    ax.set_ylabel('R_int (Ohm.cm2)')
    ax.set_title('STEP5 total R_int(N) = contact(ledger) + chemical(B-1, %s) [%s]' % (out['shape'], label),
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, loc='upper left')
    _sl = _shape_label(out, en=True)
    ax.text(0.5, -0.16, 'chem shape: %s . magnitude endpoint-anchored . SPLIT assumed . exact N-scale: curve pending'
            % _sl, transform=ax.transAxes, ha='center', fontsize=7.3, color='#888')
    fig.tight_layout()
    fn = f'{prefix}.png'
    fig.savefig(fn, dpi=130, bbox_inches='tight')
    print(f'  saved -> {fn}')


def _selftest():
    """내부 검증 — trajectory_scalar(웹패널 경로) + trajectory(JSON) 둘 다 단일 코어 통해 정합."""
    ok = tot = 0

    def chk(name, cond):
        nonlocal ok, tot
        tot += 1
        ok += 1 if cond else 0
        print(f"  {'✓' if cond else '✗ FAIL'} {name}")

    o = trajectory_scalar(18, 6.1, 1000, 2.0, 'sqrt', ledger_end_x=1.1)
    r0 = [r for r in o['rows'] if r['N'] == 0][0]
    rE = [r for r in o['rows'] if r['N'] == 1000][0]
    chk('N=0 → R=rint0', abs(r0['R_int'] - 18) < 1e-9)
    chk('endpoint bare = exp_x (magnitude 앵커)', abs(rE['R_int_x'] - 6.1) < 1e-6)
    chk('bare other=0', o['other_share_pct'] == 0.0)
    chk('bare 화학+접촉 = 100%', abs(o['chem_share_pct'] + o['contact_share_pct'] - 100.0) < 1e-6)
    xs = [r['R_int'] for r in o['rows']]
    chk('monotone R_int(N) 증가', all(xs[i] <= xs[i + 1] + 1e-9 for i in range(len(xs) - 1)))
    chk('contact rel 끝점 = ledger_end_x (하한)', abs(rE['ledger_rct_rel'] - 1.1) < 1e-9)
    oc = trajectory_scalar(18, 6.1, 1000, 2.0, 'sqrt', chem_x=1.3, ledger_end_x=1.1)
    chk('coated other>0 (모델밖 노출)', oc['other_share_pct'] > 0.5)
    chk('coated 화학 몫 < bare 화학 몫', oc['chem_share_pct'] < o['chem_share_pct'])
    oln = trajectory_scalar(18, 6.1, 1000, 2.0, 'linear', ledger_end_x=1.1)
    eLn = [r for r in oln['rows'] if r['N'] == 1000][0]['R_int']
    chk('shape 끝점 동일 (√N vs linear)', abs(rE['R_int'] - eLn) < 1e-6)
    mSq = [r for r in o['rows'] if r['N'] == 250][0]['R_int']
    mLn = [r for r in oln['rows'] if r['N'] == 250][0]['R_int']
    chk('shape 중간 다름 (√N > linear)', mSq > mLn + 1e-3)
    # #30 VGCF carbon-촉매 화학 분해 (SPLIT not ADD; k=0 무영향; carbon+base=chem; R_int 불변)
    cOff = trajectory_scalar(18, 6.1, 1000, 2.8, 'sqrt', chem_x=1.3, ledger_end_x=1.1)
    cOn = trajectory_scalar(18, 6.1, 1000, 2.8, 'sqrt', chem_x=1.3, ledger_end_x=1.1,
                            carbon_se_area=5000.0, k_cat_carbon=1e-5, vgcf_wt=2.0)
    chk('carbon OFF(k=0) → carbon몫 0', abs(cOff['chem_carbon_share_pct']) < 1e-12)
    chk('carbon ON → chem 불변 (SPLIT not ADD)', abs(cOff['chem_share_pct'] - cOn['chem_share_pct']) < 1e-9)
    chk('carbon+base = chem (분해)', abs(cOn['chem_carbon_share_pct'] + cOn['chem_base_share_pct']
                                        - cOn['chem_share_pct']) < 1e-9)
    chk('carbon split R_int 궤적 불변 (이중계산 가드)',
        all(abs(a['R_int'] - b['R_int']) < 1e-9 for a, b in zip(cOff['rows'], cOn['rows'])))
    chk('carbon_frac ∈ [0,1]', 0.0 <= cOn['chem_carbon_frac'] <= 1.0)
    import tempfile
    import os as _os
    fd = {'trajectory': [{'cycle': 0, 'rct_holm_rel': 1.0}, {'cycle': 100, 'rct_holm_rel': 1.1}]}
    tf = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False)
    json.dump(fd, tf)
    tf.close()
    oj = trajectory(tf.name, 18, 3.0, 100, 2.0, 'sqrt')
    _os.unlink(tf.name)
    chk('JSON trajectory 끝점 앵커 (동일 코어)',
        abs([r for r in oj['rows'] if r['N'] == 100][0]['R_int_x'] - 3.0) < 1e-6)
    op = trajectory_scalar(18, 6.1, 1000, 2.0, 'power', ledger_end_x=1.1, chem_p=1.5)
    chk('power 끝점 = exp_x (앵커 불변)',
        abs([r for r in op['rows'] if r['N'] == 1000][0]['R_int_x'] - 6.1) < 1e-6)
    mP = [r for r in op['rows'] if r['N'] == 250][0]['R_int']
    mS = [r for r in o['rows'] if r['N'] == 250][0]['R_int']
    chk('power(가속) 중간 < sqrt 중간 (후기 몰림)', mP < mS - 1e-3)
    oi = trajectory_scalar(18, 1.0, 1000, 2.0, 'sqrt', ledger_end_x=1.1)
    chk('exp_x≤1 → inconsistent 플래그', oi['inconsistent'] is True)
    chk('정상 입력 → inconsistent False', o['inconsistent'] is False)
    print(f'  b1_chem_fade selftest: {ok}/{tot} PASS')
    return ok == tot


def main(argv):
    ap = argparse.ArgumentParser(description='B-1 화학 N-전개 → 총 R_int(N)')
    ap.add_argument('--selftest', action='store_true', help='내부 검증만 실행')
    ap.add_argument('--fade', help='ledger fade JSON (접촉 R_ct 궤적)')
    ap.add_argument('--rint0', type=float, help='pristine R_int (Ω·cm²)')
    ap.add_argument('--rint-exp-x', type=float, help='실험 총 R_int 성장 × @ n-exp')
    ap.add_argument('--n-exp', type=int, default=1000, help='실험 끝점 사이클')
    ap.add_argument('--r-contact0', type=float, default=2.0, help='pristine 접촉 R 성분 (Ω·cm², ledger rel 곱함)')
    ap.add_argument('--shape', default='sqrt', choices=['sqrt', 'linear', 'power'],
                    help='CEI 성장 모양 — sqrt=확산제한 Wagner(Park2023 코팅셀 R∝√t 문헌지지 [B]) / '
                         'linear / power=가속 super-√N(Park2023 bare 파라볼릭, --chem-p 지수).  ★모두 ASSUMED-shape')
    ap.add_argument('--chem-p', type=float, default=1.5, help='--shape power 지수 (>1=가속, 기본 1.5)')
    ap.add_argument('--chem-x', type=float, default=None,
                    help='화학 R 성장 × @n_exp (코팅 NCM = CEI 억제 → 작게, 예 1.3).  미지정 = 화학이 나머지'
                         '(bare 가정).  지정 시 나머지 = OTHER(골격재배열·SE분해·Li = 모델 밖) 노출.')
    ap.add_argument('--label', default='case', help='라벨 (SBE/DBE 등)')
    ap.add_argument('--coating', default='none',
                    help='이종기술 코팅 프리셋 (none/LNO/LZO/Li3PO4/carbon/SDCP/SWCNT) — --chem-x(bare)에 '
                         'CEI 억제 적용 (coating_presets.py; 크기=앵커·shape=ASSUMED).  none=무코팅.')
    ap.add_argument('--out', default='rint_N', help='PNG prefix')
    a = ap.parse_args(argv)
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.coating and a.coating.lower() != 'none' and a.chem_x is not None:
        import os as _os2, sys as _sys2
        _sys2.path.insert(0, _os2.path.dirname(_os2.path.abspath(__file__)))
        import coating_presets as _cp
        _p = _cp.get_preset(a.coating); _eff = _cp.coated_chem_x(a.coating, a.chem_x)
        print(f"[coating {a.coating}] chem_x {a.chem_x} (bare) → {_eff:.4g}  "
              f"(CEI ×{_p.get('cei_suppress')} 억제; {_p['anchor']}; shape={_p['shape']})")
        a.chem_x = _eff
    missing = [n for n, v in (('--fade', a.fade), ('--rint0', a.rint0),
                              ('--rint-exp-x', a.rint_exp_x)) if v is None]
    if missing:
        ap.error('required (또는 --selftest): ' + ', '.join(missing))
    out = trajectory(a.fade, a.rint0, a.rint_exp_x, a.n_exp, a.r_contact0, a.shape, a.chem_x, a.chem_p)
    _report(out, a.label)
    _plot(out, a.label, a.out)


if __name__ == '__main__':
    main(sys.argv[1:])
