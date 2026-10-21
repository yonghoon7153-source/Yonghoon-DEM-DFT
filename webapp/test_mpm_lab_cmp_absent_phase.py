#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⚖ MPM lab 비교표 — **없는 AM 상** 의 칸을 측정된 0 처럼 보이지 않는다 (2026-10-21 · 시험 먼저).

관찰 (1저자 10-20 19:2x · 웹앱 :5002 · SDCP 최종 팔 a0 SBE ↔ DBE · 진행 기록 "10-20 20" · 수정표 F11):
비교표 (`showLabCompareModal` 정량 표) 의 AM_P 행 = 0 (0.0000).  두 침대의 NCM811 은 단일 크기 = **AM_S 한 상**
(docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md L34 "침대의 활물질 = AM_S 한 상" · Table S3 원장
§10-2 "AM_P 계열은 전부 0 … 결측이 아니라 **모집단 부재**").  생산자는 없는 상에도 coverage 0.0 을 싣는다 (P 절 —
분모 0 의 자리채움 · 강체 짝은 같은 경우 None) 그런데 비교표의 07-18 규칙 (929c26543 · "0.0000 혼란 방지") 은
**AM_S 가 없을 때만** 행을 숨겼다 (그때 SDCP 침대는 AM_P 한 상).  같은 부류 = DESC-05 ("0 · N/A 가 한 값으로 접힌다" ·
범위 = LHS 수확 · 생성 — MPM lab 비교표는 그 범위 밖).

  P  생산자 사실 (실행 · 읽기만) — 없는 AM_P: deformed_coverage = [0.0, 0.0] · mpm3d coverage_fraction = (0.0, 0, 0)
     (분모 0) · 강체 geometric_coverage = None ⇒ 비교표가 받는 0.0 은 측정값이 아니다
  R  자료 경로 — 등록 (mpm_lab_register.register_local · 봉인 · 부르기만) → GET /mpm-lab/data/<pid> (Flask test client)
     = particles[].type 과 0.0 자리채움이 그대로 온다
  T  비교표 — `showLabCompareModal` 의 정량 표 블록 ("// ── 정량 표 ──" ~ "// ── 축 설명 카드:") 을 잘라 node 로 돌린다
     (실제 innerHTML · 그 블록이 부르는 최상위 함수도 뷰어에서 그대로 자른다)
     T0 1저자 화면 값 재현 (focus 91.59 / 204 · 이온 11.61 / 11.40 · 두께 72.53 · 기공 7.86 / 7.37 · SE 덮임 86.60 ·
        CA 덮임 13.10 / 13.50 · 연결률 100)
     T1 SDCP 꼴 (두 침대 AM_S 만) = AM_P 행 없음 · 생략 알림 (조용히 숨기지 않는다)
     T2 07-18 꼴 (두 침대 AM_P 만) = AM_S 행 숨김 그대로 (회귀) · 생략 알림
     T3 bimodal 둘 = 상 행 6 개 값 그대로 · 알림 없음 (회귀)
     T4 A bimodal ↔ B AM_S 만 = AM_P 행의 B 칸 '—' · Δ '—' (옛 = 0.0000 · Δ −100.0 %) · 알림
     T5 A AM_S 만 ↔ B bimodal = AM_P 행의 A 칸 '—' · 알림
     T6 있는 상의 참 0 (무접촉) = 0.0000 그대로 (0 ≠ N/A — 지우지 않는다)
     T7 상 아닌 행 = 모든 경우에 같은 수

  python3 webapp/test_mpm_lab_cmp_absent_phase.py      # 종료코드 0 = PASS
"""
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)
from test_closed_param_labels import js_fn, run_node   # noqa: E402  (같은 도구 — 뷰어 JS 를 잘라 node 로)

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


with open(VIEWER_JS, encoding='utf-8') as f:
    JS = f.read()

PH_ROWS = ('SE덮임 AM_P Hertz (%)', 'SE덮임 AM_S Hertz (%)', 'SE덮임 AM_P Tabor (%)', 'SE덮임 AM_S Tabor (%)',
           '도전재덮임 AM_P (%)', '도전재덮임 AM_S (%)')


# ── 합성 payload (생산자 `mpm_webapp_payload.py` 의 키 · 없는 상 = 0.0 자리채움 · 강체 = None) ──────────────
def _cov(ph, present, h, t, add, rh=None, rt=None):
    """한 상의 coverage 키 — 없는 상이면 생산자가 싣는 그대로 (plastic · 도전재 0.0 · 강체 None)."""
    s = 'coverage_AM_' + ph
    if not present:
        return {s + '_hertz_pct': 0.0, s + '_tabor_pct': 0.0, s + '_add_mpm_pct': 0.0, s + '_mpm_pct': 0.0,
                s + '_rigid_hertz_pct': None, s + '_rigid_tabor_pct': None}
    return {s + '_hertz_pct': h, s + '_tabor_pct': t, s + '_add_mpm_pct': add, s + '_mpm_pct': 40.4,
            s + '_rigid_hertz_pct': rh, s + '_rigid_tabor_pct': rt}


def payload(types, *, por, thick, fe, fi, cov_p=(32.4, 62.0, 14.1), cov_s=(65.7, 86.6, 13.1), clusters=3069):
    """types = 입자 상 목록 (예: ['AM_S'] * 4).  cov_* = (Hertz, Tabor, 도전재) — 그 상이 있을 때만 쓰인다."""
    parts = [{'id': i, 'type': ty, 'x': 2.0 + 4 * i, 'y': 3.0, 'z': 4.0, 'r': 1.5, 'coverage': 50.0}
             for i, ty in enumerate(types)]
    mm = {'porosity_mpm_pct': por, 'thickness_mpm_um': thick, 'se_fraction_pct': 46.7, 'SE_of_solid_pct': 46.7,
          'n_am': len(parts),
          'step3': {'sigma_e_eff_S_cm': 1.6e-3, 'sigma_ion_eff_S_cm': 1.37e-4,
                    'field_scale_e': {'focus_top': fe}, 'field_scale_ion': {'focus_top': fi}}}
    mm.update(_cov('P', 'AM_P' in types, *cov_p, rh=55.4, rt=80.1))
    mm.update(_cov('S', 'AM_S' in types, *cov_s, rh=57.0, rt=81.2))
    return {'kind': 'mpm', 'case': 'synthetic', 'particles': parts, 'additive_points': [],
            'box': {'x_max': 20.0, 'y_max': 20.0}, 'mpm_metrics': mm,
            'econn_summary': {'connected_pct': 100.0, 'n_carbon_clusters': clusters}}


#: 1저자 화면 (10-20 19:2x) 의 값 — SBE a0 · DBE a0 (두 침대 AM_S 만)
SBE = payload(['AM_S'] * 4, por=7.86, thick=72.53, fe=91.59, fi=11.61, cov_s=(65.7, 86.6, 13.1), clusters=3069)
DBE = payload(['AM_S'] * 4, por=7.37, thick=72.53, fe=204.0, fi=11.40, cov_s=(65.7, 86.6, 13.5), clusters=2747)
MONO_P = payload(['AM_P'] * 3, por=13.47, thick=31.3, fe=40.0, fi=8.0, cov_p=(65.9, 80.0, 12.0))
BIMOD = payload(['AM_P', 'AM_P', 'AM_S', 'AM_S', 'AM_S'], por=14.9, thick=121.87, fe=60.0, fi=9.0)
BIMOD0 = payload(['AM_P', 'AM_S', 'AM_S'], por=14.9, thick=121.87, fe=60.0, fi=9.0,
                 cov_p=(32.4, 62.0, 0.0))                        # AM_P 가 **있고** 도전재 무접촉 = 참 0


# ── P  생산자 사실 ──────────────────────────────────────────────────────────────────────────
def section_p():
    print('[P] 생산자 — 없는 AM_P 상의 coverage (실행 · 읽기만)')
    try:
        import mpm_webapp_payload as PL
        import mpm3d_compaction as M3
    except Exception as e:                                  # noqa: BLE001
        chk('P0 생산자 모듈 import', False, f'{type(e).__name__}: {e}')
        return
    rng = np.random.default_rng(0)
    t = np.array([2, 2])                                    # type 2 = AM_S 만 (name = {1: AM_P, 2: AM_S})
    c = np.array([[0.3, 0.3, 0.3], [0.7, 0.7, 0.7]]); r = np.array([0.05, 0.05])
    glob, _per, _pat = PL.deformed_coverage(rng.uniform(0, 1, (4000, 3)), t, c, r, [0.13, 0.26], sub=4000, n_samp=200)
    chk('P1 deformed_coverage — 없는 AM_P = [0.0, 0.0] (분모 max(len(idx), 1) 의 자리채움) · AM_S = 값',
        glob.get('AM_P') == [0.0, 0.0] and all(v > 0 for v in glob.get('AM_S', [0])), repr(glob))
    tmp = tempfile.mkdtemp(prefix='cmp_absent_p_')
    try:
        am = os.path.join(tmp, 'am.csv'); se = os.path.join(tmp, 'se.csv')
        np.savetxt(am, np.array([[2, 0.01, 0.01, 0.01, 0.002], [2, 0.02, 0.02, 0.02, 0.002]]), delimiter=',')
        np.savetxt(se, np.column_stack([np.full(50, 3), rng.uniform(0, 0.03, (50, 3)), np.full(50, 0.0005)]),
                   delimiter=',')
        g = PL.geometric_coverage(am, se, n_samp=200)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    chk('P2 강체 geometric_coverage — 없는 AM_P = None (같은 상황의 짝은 N/A 로 싣는다)',
        g.get('AM_P') is None and isinstance(g.get('AM_S'), dict), repr(g))
    pin = np.zeros((6, 6, 6), np.int8); pin[2:4, 2:4, 2:4] = 2
    occ = np.zeros((6, 6, 6), bool); occ[1, :, :] = True
    cf = M3.coverage_fraction(pin, occ, pin == 1)
    chk('P3 mpm3d coverage_fraction — 없는 AM_P = (0.0, 0, 0) (표면 복셀 0 개 = 분모 0 의 자리채움)',
        cf == (0.0, 0, 0), repr(cf))


# ── R  자료 경로 ────────────────────────────────────────────────────────────────────────────
def section_r(tmp):
    print('[R] 자료 경로 — 등록 → GET /mpm-lab/data/<pid>')
    os.environ['WEBAPP_MPM_LAB_FOLDER'] = os.path.join(tmp, 'mpm_lab')
    for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                 ('WEBAPP_ARCHIVE_FOLDER', 'archive')):
        os.environ[k] = os.path.join(tmp, v)
    import app as A
    import mpm_lab_register as REG
    lab = A.app.config['MPM_LAB_FOLDER']
    os.makedirs(lab, exist_ok=True)
    cl = A.app.test_client()
    got = {}
    for nm, d in (('SBE_a0', SBE), ('DBE_a0', DBE), ('MONO_P', MONO_P), ('BIMOD', BIMOD), ('BIMOD0', BIMOD0)):
        pid, _d, _meta = REG.register_local(json.loads(json.dumps(d)), nm, lab)
        r = cl.get('/mpm-lab/data/' + pid)
        got[nm] = r.get_json() if r.status_code == 200 else None
    s = got.get('SBE_a0') or {}
    chk('R1 경로가 payload 를 그대로 준다 (5/5 · 200)', all(v is not None for v in got.values()), repr(list(got)))
    chk('R2 SBE a0 꼴 — particles[].type = AM_S 만 (AM_P 입자 0 개)',
        sorted({p.get('type') for p in s.get('particles', [])}) == ['AM_S'], repr(s.get('particles', [])[:2]))
    mm = s.get('mpm_metrics', {})
    chk('R3 그 payload 의 AM_P 칸 = 0.0 자리채움 (plastic · 도전재) · 강체 = None — 비교표가 받는 그대로',
        mm.get('coverage_AM_P_tabor_pct') == 0.0 and mm.get('coverage_AM_P_add_mpm_pct') == 0.0
        and mm.get('coverage_AM_P_rigid_tabor_pct') is None, repr({k: v for k, v in mm.items() if 'AM_P' in k}))
    return got


# ── T  비교표 (node) ────────────────────────────────────────────────────────────────────────
_TOP_FN = re.compile(r'^(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(', re.M)


def _block(src, start, end):
    i = src.find(start)
    j = src.find(end, i + len(start)) if i >= 0 else -1
    return src[i:j] if (i >= 0 and j > i) else ''


def _helpers_for(code):
    """code 가 부르는 뷰어 최상위 함수 (전이 폐포) — 사본을 두지 않고 뷰어에서 그대로 자른다."""
    names = set(_TOP_FN.findall(JS)) - {'showLabCompareModal'}
    need, todo, out = set(), [code], []
    while todo:
        src = todo.pop()
        for nm in sorted(names - need):
            if re.search(r'(?<![\w$.])' + re.escape(nm) + r'\s*\(', src):
                need.add(nm)
                fn = js_fn(JS, nm)
                out.append(fn)
                todo.append(fn)
    return out


def render(pairs):
    blk = _block(JS, '// ── 정량 표 ──', '// ── 축 설명 카드:')
    if not blk:
        return None
    script = ('\n'.join(_helpers_for(blk)) + '\n'
              + 'const render = (A, B) => { const store = {};\n'
              + '  const $ = (id) => (store[id] = store[id] || {});\n'
              + blk + '\n  return (store["cmp-table"] || {}).innerHTML || ""; };\n'
              + 'const P = ' + json.dumps(pairs, ensure_ascii=False) + ';\n'
              + 'const out = {}; for (const k of Object.keys(P)) out[k] = render(P[k][0], P[k][1]);\n'
              + 'console.log(JSON.stringify(out));\n')
    return run_node(script)


def rows_of(html):
    h = re.sub(r'\sdata-tip="[^"]*"', '', html or '')
    return [tuple(x.strip() for x in r) for r in re.findall(
        r'<tr><td[^>]*>(.*?)</td><td[^>]*>(.*?)</td><td[^>]*>(.*?)</td><td[^>]*>(.*?)</td></tr>', h, re.S)]


def outside_tables(html):
    """표 (<table>…</table>) 밖의 글 — 생략 · N/A 알림이 놓이는 자리."""
    return re.sub(r'<[^>]+>', ' ', re.sub(r'<table.*?</table>', ' ', html or '', flags=re.S))


def section_t(got):
    print('[T] 비교표 — 정량 표 블록을 node 로 (실제 innerHTML)')
    if not shutil.which('node'):
        chk('T node 필요 (비교표 블록을 실제로 돌린다)', False, 'node 미설치')
        return
    g = {k: v for k, v in got.items() if v is not None}
    pairs = {
        'sdcp': [g['SBE_a0'], g['DBE_a0']],
        'monoP': [g['MONO_P'], g['MONO_P']],
        'bimod': [g['BIMOD'], g['BIMOD']],
        'mixAB': [g['BIMOD'], g['DBE_a0']],
        'mixBA': [g['SBE_a0'], g['BIMOD']],
        'zero': [g['BIMOD0'], g['BIMOD']],
    }
    out = render(pairs)
    if not chk('T00 node 실행 · 블록 추출', out is not None):
        return
    R = {k: rows_of(v) for k, v in out.items()}
    D = {k: {r[0]: r[1:] for r in v} for k, v in R.items()}
    lab = lambda k, pre: next((r for r in R[k] if r[0].startswith(pre)), None)   # noqa: E731

    sd = R['sdcp']
    want = [('e-집중 p99.8', '91.59', '204'), ('ion-집중 p99.8', '11.61', '11.40'), ('thickness', '72.53', '72.53'),
            ('porosity', '7.86', '7.37'), ('SE덮임 AM_S Tabor', '86.60', '86.60'),
            ('도전재덮임 AM_S', '13.10', '13.50'), ('econn 연결률', '100', '100')]
    bad = [(p, lab('sdcp', p)) for p, a, b in want
           if not (lab('sdcp', p) and lab('sdcp', p)[1] == a and lab('sdcp', p)[2] == b)]
    chk('T0 1저자 화면 값 재현 (focus · 이온 · 두께 · 기공 · SE 덮임 · CA 덮임 · 연결률)', not bad, repr(bad))
    amp = [r for r in sd if 'AM_P' in r[0]]
    chk('T1a SDCP 꼴 (두 침대 AM_S 만) — AM_P 행이 없다 (옛 = 0.0000 · 0.0000 세 행)', not amp, repr(amp))
    chk('T1b 그 경우 AM_S 행 셋은 값 그대로 (Hertz 65.70 · Tabor 86.60 · 도전재 13.10 / 13.50)',
        D['sdcp'].get('SE덮임 AM_S Hertz (%)', ('',))[0] == '65.70'
        and D['sdcp'].get('도전재덮임 AM_S (%)', ('', ''))[:2] == ('13.10', '13.50'), repr(D['sdcp'].get('도전재덮임 AM_S (%)')))
    note = outside_tables(out['sdcp'])
    chk('T1c 행을 조용히 숨기지 않는다 — 표 밖 알림에 "AM_P" · "입자 0" · "N/A"',
        'AM_P' in note and '입자 0' in note and 'N/A' in note, note.strip()[:200])

    ams = [r for r in R['monoP'] if 'AM_S' in r[0]]
    chk('T2a 07-18 꼴 (두 침대 AM_P 만) — AM_S 행 숨김 그대로 (회귀)', not ams, repr(ams))
    chk('T2b 그 경우 AM_P 행 셋은 값 그대로 (Tabor 80.00)',
        D['monoP'].get('SE덮임 AM_P Tabor (%)', ('',))[0] == '80.00', repr(D['monoP'].get('SE덮임 AM_P Tabor (%)')))
    n2 = outside_tables(out['monoP'])
    chk('T2c 그 경우도 알림 — "AM_S" · "입자 0"', 'AM_S' in n2 and '입자 0' in n2, n2.strip()[:200])

    bi = [r for r in R['bimod'] if r[0] in PH_ROWS]
    chk('T3a bimodal 둘 — 상 행 6 개 · 칸에 "—" 없음 (회귀)',
        len(bi) == 6 and all(r[1] != '—' and r[2] != '—' for r in bi), repr(bi))
    chk('T3b bimodal 둘 — 없는 상 알림 없음', '입자 0' not in outside_tables(out['bimod']),
        outside_tables(out['bimod']).strip()[:200])

    m = D['mixAB'].get('SE덮임 AM_P Tabor (%)')
    chk('T4a A bimodal ↔ B AM_S 만 — AM_P Tabor 행: A 62.00 · B "—" · Δ "—" (옛 = B 0.0000 · Δ −100.0%)',
        m is not None and m[0] == '62.00' and m[1] == '—' and m[2] == '—', repr(m))
    ma = D['mixAB'].get('도전재덮임 AM_P (%)')
    chk('T4b 같은 경우 도전재덮임 AM_P: B "—" · Δ "—"', ma is not None and ma[1] == '—' and ma[2] == '—', repr(ma))
    s4 = D['mixAB'].get('SE덮임 AM_S Tabor (%)')
    chk('T4c 같은 경우 AM_S 행은 두 칸 값 (둘 다 AM_S 있음)', s4 is not None and '—' not in s4[:2], repr(s4))
    n4 = outside_tables(out['mixAB'])
    chk('T4d 알림 — "—" 칸의 뜻 (AM_P · B · 입자 0)', 'AM_P' in n4 and 'B' in n4 and '입자 0' in n4, n4.strip()[:200])

    m5 = D['mixBA'].get('SE덮임 AM_P Hertz (%)')
    chk('T5 A AM_S 만 ↔ B bimodal — AM_P Hertz 행: A "—" · B 32.40 (옛 = A 0.0000)',
        m5 is not None and m5[0] == '—' and m5[1] == '32.40', repr(m5))

    z = D['zero'].get('도전재덮임 AM_P (%)')
    chk('T6 있는 상의 참 0 (AM_P 있음 · 도전재 무접촉) = 0.0000 그대로 (0 ≠ N/A)',
        z is not None and z[0] == '0.0000', repr(z))

    nph = {k: len([r for r in v if r[0] not in PH_ROWS]) for k, v in R.items()}
    chk('T7 상 아닌 행 = 모든 경우에 같은 수', len(set(nph.values())) == 1 and min(nph.values()) > 10, repr(nph))


def main():
    tmp = tempfile.mkdtemp(prefix='cmp_absent_')
    try:
        section_p()
        got = section_r(tmp)
        section_t(got)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    n = _ok + len(_fail)
    print(f'\n{_ok}/{n}  ' + ('✓ 전부 통과' if not _fail else f'✗ {len(_fail)} 건 실패'))
    for nm in _fail:
        print('  -', nm)
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
