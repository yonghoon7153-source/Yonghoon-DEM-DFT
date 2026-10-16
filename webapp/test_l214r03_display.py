#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L214R-03 — 최종 화면이 미채택 값을 옛 CSV 에서 복원하지 않는다 (Codex LHS214 재검증 판정문 §4 · §7 · 수정 계획
`docs/reviews/lhs214r_fix_plan_20261016.md` Q3 = 1저자 비준 "화면만" — 분석기 CSV · 계산 무변경 · CLAUDE.md "코드 → 웹앱 순차 반영").

계기: network 게시 목록 (`pipeline_service`) 은 contact 단계의 `network_summary.csv` 를 갱신하지 않는다.  그 CSV 에 옛 σ 가 남아 있으면 최종 병합
(transform Step 1 → normalize Pass A split 병합 · 늘 내는 행) 이 FULL 모형 한계 · σ 미채택 모드의 숫자를 다시 채웠다 (Codex 탐침 l214_display.py):
  · split CSV (Hertz · Physics 두 절)      → 이온 σ 0.6 / 0.9 / +50.0% · Plastic amplification 1.50× / 1.50× / 0%
  · 두 열 CSV + H0 도 모형 한계              → Hertz σ 0.6 · R_brug 2.0× 가 남음
  · 네 열 CSV                               → 0.6 / 0.6 / 0% 그대로
  같은 화면의 상태 행 = FULL 모형 한계 · τ 행 = NOT_COMPUTED (full_over_conduction) — 숫자와 상태가 모순.

계약 (고친 뒤): 최종 병합 뒤에도 **현재 모드별 망 상태가 이긴다** — 모형 한계 · σ 미채택 (값 없음 · 비유한 · not_computed · valid_zero 등) 모드의
이온 σ · FULL 유도비 (R_brug · Contact-free/Full · σ_brug/σ_ionic · Plastic amplification) 칸 = '—' (+ 사유) · Δ = '—' — CSV 꼴 (split · 두 열 · 네 열 · 새 표) 과
무관.  채택된 모드 (computed · 옛 세대 = 상태 키 없음 + 유한 σ) 의 칸은 그대로 둔다.  비가 미제공인 '— / — / 0%' 행의 Δ 도 '—'.
의도된 변화 기록: 정상 새 표의 R_brug Physics 2.0× → 1.4× · Δ 0% → −30.0% (loader → normalize → 템플릿) = 앞선 L214-03 의 의도된 표시 교정 (되돌리지 않는다).

경로: 실제 `app` import · 실 생산자 CLI (`test_network_handover_chain._run_ml` — 침대 ml_physics · ml_hertz) 로 게시한 폴더 · `_load_case_tables`
(케이스 · 보고서 · 보관함 라우트 공용) · Flask GET /single/<id> (전체 single.html 템플릿).  합성 metrics 사례는 Codex 탐침과 같은 값.

  python3 webapp/test_l214r03_display.py
"""
import contextlib
import copy
import csv
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for _p in (HERE, os.path.join(ROOT, 'scripts')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

#  케이스 · 보관함 폴더 = 임시 폴더 (리포 안 webapp/results 를 건드리지 않는다) — app import 전에
WORK = tempfile.mkdtemp(prefix='l214r03_')
for _k, _n in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
               ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
    os.environ[_k] = os.path.join(WORK, _n)
os.environ['MPLCONFIGDIR'] = os.path.join(WORK, 'mplconfig')
os.environ['SUPABASE_URL'] = ''
os.environ['SUPABASE_KEY'] = ''

PASS = FAIL = 0


def chk(label, ok, detail=''):
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f'  PASS {label}')
    else:
        FAIL += 1
        print(f'  FAIL {label}' + (f' — {str(detail)[:600]}' if detail else ''))


class _Rows(HTMLParser):
    """렌더된 HTML 의 표 행 (<tr> 안 <td> 글) — Codex 탐침과 같은 판독."""

    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.row = []
        if tag == 'td' and self.row is not None:
            self.cell = []

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.row.append(''.join(self.cell).strip())
            self.cell = None
        if tag == 'tr' and self.row is not None:
            if self.row:
                self.rows.append(self.row)
            self.row = None


#  contact 단계 옛 CSV (Codex 탐침 LEGACY 그대로 — 게시 전 폴더에 이미 있는 옛 표시값 · 합성 변이)
LEGACY = [['── Network Solver (Hertzian DEM-native) ──', ''],
          ['σ_ionic (mS/cm)', 0.6], ['R_brug (과대추정 배수)', '2.0×'],
          ['Constriction 비율(%)', 40.0], ['σ_electronic (mS/cm)', 2.0],
          ['σ_thermal (mS/cm equiv)', 0.3], ['SE Volume Fraction', 0.5]]
LAYOUTS = ('new', 'csv', 'split', 'fourcol')


def csv_layout(layout):
    """→ (머리, 행) — new = 망 절 없는 새 표 · csv = 분석기 두 열 (Hertz 절) · split = Hertz + Physics 두 절 · fourcol = 이미 네 열."""
    if layout == 'new':
        return ['지표', '값'], [['SE Volume Fraction', 0.5]]
    rows = copy.deepcopy(LEGACY)
    if layout == 'split':
        rows += [['── Physics (Plastic film, Tabor+volume) ──', ''], ['σ_ionic [physics] (mS/cm)', 0.9],
                 ['σ_ionic ratio (physics/Hertzian)', '1.50×']]
    if layout == 'fourcol':
        return ['지표', 'H', 'P', 'Δ'], [[r[0], r[1], r[1], '0%'] for r in rows]
    return ['지표', '값'], rows


def write_csv(rd, layout):
    head, rows = csv_layout(layout)
    p = os.path.join(rd, 'network_summary.csv')
    with open(p, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(rows)
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


#  합성 metrics (Codex 탐침 NORMAL 과 같은 값)
NORMAL = dict(sigma_full_mScm=.6, sigma_full_mScm_physics=.9, sigma_full_status='computed', sigma_full_status_physics='computed',
              network_solver_status='success', sigma_ratio=.4, phi_se=.5, sigma_bulk_net_mScm=1., sigma_bulk_net_mScm_physics=1.,
              R_brug_over_full=2., R_brug_over_full_physics=1.4, bulk_resistance_fraction=.6, bulk_resistance_fraction_physics=.8,
              electronic_sigma_full_mScm=2., electronic_sigma_full_mScm_physics=3., thermal_sigma_full_mScm=.3,
              thermal_sigma_full_mScm_physics=.45, tortuosity_mean=1.2)
ML = 'full_over_conduction'


def synth(kind):
    """합성 사례 — Codex 탐침 변이와 같은 값 (이온 · 전자 · 열 σ + R_brug 를 같이 바꾼다):
    null = None · missing = 키 없음 · zero = 0 (R_brug 포함) — 상태 not_computed + full_over_conduction /
    valid_zero_null · valid_zero_numeric = σ None · 0 (R_brug None) — 상태 valid_zero + no_through_path (증명된 비관통)."""
    mx = copy.deepcopy(NORMAL)
    if kind == 'normal':
        return mx
    if kind == 'legacy_single':                     # 옛 세대 — 상태 키 · physics 키 없음 (단일 모드 시절) · Hertz σ 유한
        return {k: v for k, v in mx.items() if not k.endswith('_physics') and 'status' not in k}
    side, var = kind.split(':')                       # 'hertz:null' · 'physics:missing' · 'both:valid_zero_numeric' …
    sides = ('', '_physics') if side == 'both' else (('_physics',) if side == 'physics' else ('',))
    for sx in sides:
        for base in ('sigma_full_mScm', 'electronic_sigma_full_mScm', 'thermal_sigma_full_mScm', 'R_brug_over_full'):
            if var == 'missing':
                mx.pop(base + sx, None)
            elif var == 'zero':
                mx[base + sx] = 0.
            elif var == 'valid_zero_numeric':
                mx[base + sx] = 0. if base != 'R_brug_over_full' else None
            else:
                mx[base + sx] = None
        for pre in ('', 'electronic_', 'thermal_'):
            if var.startswith('valid_zero'):
                mx[pre + 'sigma_full_status' + sx], mx[pre + 'sigma_full_reason' + sx] = 'valid_zero', 'no_through_path'
            else:
                mx[pre + 'sigma_full_status' + sx], mx[pre + 'sigma_full_reason' + sx] = 'not_computed', ML
    return mx


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        import app
    import test_network_handover_chain as chain     # _run_ml — 실 생산자 CLI 사슬 (같은 도구)
    app.app.config['TESTING'] = True
    client = app.app.test_client()
    RES, UPL = app.app.config['RESULTS_FOLDER'], app.app.config['UPLOAD_FOLDER']
    PL = app._PAPER_LABEL_MAP
    ION, RB, PAMP = (PL[k] for k in ('σ_ionic (mS/cm)', 'R_brug (과대추정 배수)', 'σ_ionic ratio (physics/Hertzian)'))
    CF, SBI = PL['Contact-free / Full'], PL['σ_brug / σ_ionic']
    MODE_ROWS = (ION, RB, CF, SBI)                     # 모드별 칸 (Hertz · Physics) — 이온 σ 와 FULL 유도비
    STATUS_ROW = 'σ_ionic network state'
    HANDOVER_ROW = 'tau2 handover status'

    def masked(c):
        return str(c).strip() == '—' or str(c).strip().startswith('— (')

    def number(c):
        return not masked(c) and any(ch.isdigit() for ch in str(c))

    def by_label(rows):
        """행 → {라벨: [글 칸 …]} (loader 칸은 수 · 글이 섞여 있다 — 화면 글과 같은 꼴로 str)."""
        return {str(r[0]).strip(): [str(x) for x in r] for r in rows if isinstance(r, list) and r}

    def case(cid, metrics=None, layout='new', bed=None):
        """케이스 하나 — results/<cid> (+ uploads/<cid>/meta.json) · 옛 CSV 먼저 · bed 면 실 생산자 게시 (그 뒤 CSV sha 대조) ·
        → dict(loader · route 행 · 상태 · CSV 보존)."""
        rd = os.path.join(RES, cid)
        os.makedirs(rd, exist_ok=True)
        os.makedirs(os.path.join(UPL, cid), exist_ok=True)
        with open(os.path.join(UPL, cid, 'meta.json'), 'w', encoding='utf-8') as f:
            json.dump({'name': cid, 'status': 'done', 'scale': 1}, f)       # scale = 업로드 meta 의 배율 (템플릿 RVE 배지가 쓴다)
        sha0 = write_csv(rd, layout)
        st = None
        if bed:
            with contextlib.redirect_stdout(io.StringIO()):
                _d, st, _failed, _rid = chain._run_ml(app, bed, tm='1:SE', d=rd)
        else:
            with open(os.path.join(rd, 'full_metrics.json'), 'w', encoding='utf-8') as f:
                json.dump(metrics, f)
        sha1 = hashlib.sha256(open(os.path.join(rd, 'network_summary.csv'), 'rb').read()).hexdigest()
        with contextlib.redirect_stdout(io.StringIO()):
            tables, met, _ip = app._load_case_tables(rd, {})
            resp = client.get('/single/' + cid)
        parsed = _Rows()
        parsed.feed(resp.get_data(as_text=True))
        return dict(loader=by_label(tables['network_summary']['data']), route=by_label(parsed.rows), http=resp.status_code,
                    state=st, csv_kept=(sha0 == sha1), metrics=met, layout=layout)

    def mode_problems(c, hertz_ok, physics_ok, where=('loader', 'route')):
        """모드별 행 (이온 σ · R_brug · CF/FULL · σ_brug/σ_ionic) + Plastic amplification 의 계약 위반 목록.
        hertz_ok · physics_ok = 그 모드가 채택 (숫자를 보여도 된다 · 칸을 가리지 않는다) 인가.
        옛 CSV 꼴 (두 열 · split · 네 열) 은 이온 σ · R_brug · Plastic amplification 행이 있어야 한다 (행이 사라져 헛통과하지 않게)."""
        bad = []
        need = (ION, RB, PAMP) if c.get('layout') != 'new' else ()
        for w in where:
            rows = c[w]
            bad += [(w, lab[:24], '행 없음') for lab in need if lab not in rows]
            for lab in MODE_ROWS:
                r = rows.get(lab)
                if r is None or len(r) < 4:
                    continue                                   # 행 없음 = 숫자 없음 (새 표 · Hertz 미채택이면 망 절 행이 안 선다)
                for i, ok_ in ((1, hertz_ok), (2, physics_ok)):
                    if not ok_ and not masked(r[i]):
                        bad.append((w, lab[:24], 'H' if i == 1 else 'P', r[i]))
                    if ok_ and lab == ION and not number(r[i]):
                        bad.append((w, lab[:24], ('H' if i == 1 else 'P') + ' 채택 모드가 가려짐', r[i]))
                if not (hertz_ok and physics_ok) and str(r[3]).strip() != '—':
                    bad.append((w, lab[:24], 'Δ', r[3]))
            r = rows.get(PAMP)
            if r is not None and len(r) >= 4:
                if not (hertz_ok and physics_ok) and not (masked(r[1]) and masked(r[2])):
                    bad.append((w, 'Plastic amp', 'H/P', r[1], r[2]))
                if (masked(r[1]) or masked(r[2])) and str(r[3]).strip() != '—':
                    bad.append((w, 'Plastic amp', 'Δ', r[3]))
        return bad

    try:
        print('① 실 생산자 (ml_physics = Hertz 채택 · Physics FULL 모형 한계 / ml_hertz = 세 모드 모형 한계) × 옛 CSV 꼴')
        prod = {}
        for bed in ('ml_physics', 'ml_hertz'):
            for lay in LAYOUTS:
                prod[(bed, lay)] = case(f'l214r03_{bed}_{lay}', layout=lay, bed=bed)
        st = {k: (v['state'], v['http'], v['csv_kept']) for k, v in prod.items()}
        chk(f'①a 게시 = done 여덟 · GET /single = 200 · network 게시 뒤 옛 CSV 바이트 그대로 (게시 목록이 contact CSV 를 갱신하지 않는다 — 화면이 막아야 하는 이유) {st}',
            all(v == ('done', 200, True) for v in st.values()))
        p_split = prod[('ml_physics', 'split')]
        r_st, r_ho = (next((r for k, r in p_split['loader'].items() if k.startswith(w)), None) for w in (STATUS_ROW, HANDOVER_ROW))
        chk('①b 같은 화면의 상태 행 Physics = FULL 모형 한계 · τ 인계 상태 Physics = NOT_COMPUTED (full_over_conduction) (숫자와 맞춰야 할 상태)',
            r_st is not None and '모형 한계' in str(r_st[2]) and r_ho is not None and f'NOT_COMPUTED ({ML})' in str(r_ho[2]), (r_st, r_ho))
        b = mode_problems(p_split, True, False)
        chk(f'①c ★ Codex 반례 1 — split CSV + Physics 모형 한계 → Physics 이온 σ · R_brug · CF/FULL · σ_brug/σ_ionic = — · Δ — · Plastic amplification '
            f'— / — / — (옛: 0.6 / 0.9 / +50.0% · 1.50× / 1.50× / 0%) · Hertz (채택) 숫자 유지 {b}', not b)
        b = mode_problems(prod[('ml_hertz', 'csv')], False, False)
        chk(f'①d ★ Codex 반례 2 — H0 도 모형 한계 + 두 열 CSV → Hertz · Physics 어느 칸에도 이온 σ · R_brug 숫자 없음 · Δ — (옛: Hertz σ 0.6 · R_brug 2.0×) {b}', not b)
        b = mode_problems(prod[('ml_physics', 'fourcol')], True, False)
        chk(f'①e ★ Codex 반례 3 — 이미 네 열인 CSV + Physics 모형 한계 → Physics 칸 — · Δ — (옛: 0.6 / 0.6 / 0% 그대로) {b}', not b)
        rest = {lay: mode_problems(prod[('ml_hertz', lay)], False, False) for lay in ('new', 'split', 'fourcol')}
        rest.update({f'ml_physics {lay}': mode_problems(prod[('ml_physics', lay)], True, False) for lay in ('new', 'csv')})
        chk(f'①f 나머지 조합 — ml_hertz × (새 표 · split · 네 열) · ml_physics × (새 표 · 두 열) 도 같은 규약 (Plastic amplification 미제공 Δ 포함) {rest}',
            not any(rest.values()))
        r_ion = p_split['route'].get(ION)
        chk('①g 렌더된 single.html (GET) 의 이온 σ 행 = Hertz 숫자 · Physics 모형 한계 문구 (사유 full_over_conduction) · Δ —',
            r_ion is not None and number(r_ion[1]) and masked(r_ion[2]) and ML in str(r_ion[2]) and str(r_ion[3]).strip() == '—', r_ion)

        print('② H0 결측 · 미채택 조합 (합성 metrics · Codex 탐침 변이) × CSV 꼴')
        h0 = {}
        for kind in ('hertz:null', 'hertz:missing', 'hertz:zero'):
            for lay in ('csv', 'split', 'fourcol'):
                c = case(f'l214r03_{kind.replace(":", "_")}_{lay}', synth(kind), lay)
                h0[(kind, lay)] = mode_problems(c, False, True)
        chk(f'②a ★ H0 결측 (모형 한계 σ None · 키 없음 · 0 + not_computed) × (두 열 · split · 네 열) → Hertz 이온 σ · R_brug = — · Δ — · Physics (채택) 숫자 유지 '
            f'(옛: Hertz 0.6 · 2.0× · Δ 0% / +50%) {h0}', not any(h0.values()))
        c_hz = case('l214r03_hertz_zero_csv_reason', synth('hertz:zero'), 'csv')
        r_hz = c_hz['loader'].get(ION)
        chk('②b H0 σ = 0 + not_computed (full_over_conduction) — Hertz 칸 = 모형 한계 문구 (0.6 · 0 아님) · Physics 0.9 · Δ — (옛: Δ 0% = h 0 이라 가짜)',
            r_hz is not None and ML in str(r_hz[1]) and str(r_hz[2]) == '0.9' and str(r_hz[3]).strip() == '—', r_hz)
        vz = {}
        for kind in ('both:valid_zero_null', 'both:valid_zero_numeric', 'physics:null', 'physics:missing'):
            for lay in ('csv', 'split', 'fourcol'):
                c = case(f'l214r03_{kind.replace(":", "_")}_{lay}', synth(kind), lay)
                vz[(kind, lay)] = mode_problems(c, kind.startswith('physics'), False)
        chk(f'②c 미채택 σ (valid_zero = 증명된 비관통 · 값 None 또는 0 / Physics 모형 한계 None · 키 없음) × CSV 꼴 → 그 모드 칸 — · Δ — (옛 CSV 숫자 없음) {vz}',
            not any(vz.values()))

        print('③ 정상 (두 모드 채택) — 의도된 값 · 바뀌지 않는 꼴')
        n_new = case('l214r03_normal_new', synth('normal'), 'new')
        want = {ION: ['0.6', '0.9', '+50.0%'], RB: ['2.0×', '1.4×', '-30.0%'], PAMP: ['1.50×', '1.50×', '0%'], CF: ['2.0×', '1.4×', '-30.0%']}
        got = {lab[:20]: [n_new[w].get(lab, [None] * 4)[1:4] for w in ('loader', 'route')] for lab in want}
        ok_ = all(n_new[w].get(lab, [None] * 4)[1:4] == v for lab, v in want.items() for w in ('loader', 'route'))
        chk(f'③a ★ 의도된 변화 기록 — 정상 새 표 (loader → normalize → 템플릿): R_brug = 2.0× / 1.4× / -30.0% (옛 전체 표시: Physics 2.0× · Δ 0% = Hertz 복사 — 앞선 '
            f'L214-03 의 의도된 교정 · 되돌리지 않는다) · 이온 σ 0.6 / 0.9 / +50.0% · Plastic amplification 1.50× / 1.50× / 0% · CF/FULL 2.0× / 1.4× / -30.0% {got}', ok_)
        nb = {lay: mode_problems(case(f'l214r03_normal_{lay}', synth('normal'), lay), True, True) for lay in ('csv', 'split', 'fourcol')}
        chk(f'③b 정상 × (두 열 · split · 네 열) — 두 모드 채택이면 가리지 않는다 (이온 σ 두 칸 숫자) {nb}', not any(nb.values()))
        c_l = case('l214r03_legacy_single_csv', synth('legacy_single'), 'csv')
        r_l = c_l['loader'].get(ION)
        chk('③c 옛 세대 (상태 키 · physics 키 없음 · Hertz σ 유한) + 두 열 CSV → Hertz 칸 = CSV 값 그대로 (채택) · Physics — · Δ —',
            r_l is not None and str(r_l[1]) == '0.6' and masked(r_l[2]) and str(r_l[3]).strip() == '—', r_l)

        print('④ 비 미제공 행의 Δ (— / — / 0% → —)')
        pa = {}
        for nm, mx, lay in (('physics_null_new', synth('physics:null'), 'new'), ('legacy_single_csv2', synth('legacy_single'), 'csv'),
                            ('hertz_null_csv', synth('hertz:null'), 'csv')):
            c = case(f'l214r03_pamp_{nm}', mx, lay)
            pa[nm] = [c[w].get(PAMP, [None] * 4)[1:4] for w in ('loader', 'route')]
        chk(f'④a ★ Plastic amplification 비 미제공 (Physics 모형 한계 · 옛 단일 모드 · H0 모형 한계) → — / — / — (옛: — / — / 0%) {pa}',
            all(v == ['—', '—', '—'] for vs in pa.values() for v in vs))
    finally:
        shutil.rmtree(WORK, ignore_errors=True)
    print(f'\ntest_l214r03_display: {PASS}/{PASS + FAIL} PASS' + ('' if not FAIL else f'   ({FAIL} FAIL)'))
    return 0 if not FAIL else 1


if __name__ == '__main__':
    sys.exit(main())
