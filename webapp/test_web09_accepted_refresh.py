#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WEB-09 — 최종 화면의 **채택된** 모드 칸 = 현재 metrics 값 (옛 CSV 숫자 아님) (Codex LHS214 재검증 판정문 §4 최소 해제
"최종 병합 뒤에도 현재 모드별 수치 · 상태를 우선" · 1저자 10-16 Q1 "권고대로" = 화면만 — 분석기 CSV · 계산 무변경 · CLAUDE.md "코드 → 웹앱 순차 반영").

계기: contact 단계 (`scripts/analyze_contacts.py`) 가 그때 있던 full_metrics.json 으로 network_summary.csv 를 쓰고, network 게시는 그 CSV 를 갱신하지
않는다.  망을 다시 분석하면 **채택된** 모드 (생산자 상태 computed · 유한 σ > 0) 의 칸에 옛 CSV 숫자가 남고 Δ 는 현재 값으로 계산된다 — L214R-03 (Pass G) 은
미채택 모드만 가렸다 (Codex 증거 `docs/reviews/codex_lhs214_fix_reverify_evidence_20261015/` display_source.json):
  · ml_physics (Hertz 채택 2.386067 · Physics FULL 모형 한계) + 옛 CSV → Hertz σ 칸 0.6
  · ml_el (두 모드 채택 1.201613 · 2.078264) + 두 열 CSV → 0.6 / 2.0783 / +73.0% (Hertz 칸만 옛 값 · Δ 는 현재 값)
  · split · 네 열 CSV → 이온 σ 0.6 / 0.9 (또는 0.6) · R_brug 2.0× · Plastic amplification 1.50× 가 그대로.

계약 (고친 뒤): 최종 병합 (Pass G 포함) 뒤 채택된 모드의 이온 행 칸 (σ_ionic · R_brug · Contact-free / Full · σ_brug / σ_ionic) = 새 표 경로 (CSV 망 절이
없을 때 metrics 로 만드는 표) 가 **현재** metrics 로 내는 값 (같은 정의 · 같은 꼴) · Plastic amplification = 두 모드 다 채택이면 현재 값 · Δ = 새 표와 같은
방식 (두 칸이 다 현재 값일 때만 — 한 칸이 옛 칸 그대로면 '—').  미채택 모드 = Pass G 그대로 ('—' 또는 모형 한계 사유) · valid_zero = '—' (1저자 Q2).
옛 세대 (상태 키 없음): metrics 에 값이 있으면 새 표와 똑같이 · 필요한 metric 이 없으면 기존 칸 그대로 (지어내지 않는다).  Constriction · 전자 · 열 행 무변경.
정상 새 표 (CSV 망 절 없음) 는 수정 전과 똑같이 렌더된다.

경로: 실제 `app` import · 실 생산자 CLI (`test_network_handover_chain._run_ml` — 침대 ml_el · ml_physics · ml_hertz) 로 게시한 폴더 · `_load_case_tables`
(케이스 · 보고서 · 보관함 라우트 공용) · Flask GET /single/<id> (전체 single.html).  옛 CSV 꼴 · 합성 metrics · HTML 판독 = `test_l214r03_display` 의 것을 그대로 쓴다.

  python3 webapp/test_web09_accepted_refresh.py
"""
import contextlib
import csv
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for _p in (HERE, os.path.join(ROOT, 'scripts')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

#  케이스 · 보관함 폴더 = 임시 폴더 (리포 안 webapp/results 를 건드리지 않는다) — app import 전에
WORK = tempfile.mkdtemp(prefix='web09_')
import test_l214r03_display as L     # noqa: E402  옛 CSV 꼴 (LEGACY · csv_layout · write_csv) · 합성 metrics (NORMAL · synth) · HTML 판독 (_Rows)
shutil.rmtree(L.WORK, ignore_errors=True)   # 그 모듈이 import 때 만든 임시 폴더 (여기서는 안 쓴다)
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
        print(f'  FAIL {label}' + (f' — {str(detail)[:900]}' if detail else ''))


#  현재 값 — 옛 CSV (LEGACY: σ 0.6 · Physics 0.9 · R_brug 2.0× · 비 1.50×) 와 다른 수 (Codex ml_el 의 σ 두 값) → 채택 모드 칸이 어느 쪽인지 구분된다
CUR_ION = {'sigma_full_mScm': 1.2016, 'sigma_full_mScm_physics': 2.0783, 'R_brug_over_full': 3.3, 'R_brug_over_full_physics': 1.9}


def current(kind='normal'):
    """L.synth(kind) (Codex 탐침 변이 — 바뀐 쪽 = 모형 한계 · 결측) 위에 **바뀌지 않은** 쪽의 이온 값 = CUR_ION."""
    mx = L.synth(kind)
    side = kind.split(':')[0] if ':' in kind else None
    for k, v in CUR_ION.items():
        if side not in ('physics' if k.endswith('_physics') else 'hertz', 'both'):
            mx[k] = v
    return mx


OLD_DUAL = {k: v for k, v in L.NORMAL.items() if 'status' not in k}   # 옛 세대 두 모드 — 생산자 상태 키 없음 (σ 두 값 유한 = 채택)

#  네 열 + 옛 CF/Full · σ_brug/σ_ionic · 비 행 (옛 전체 표 사본 꼴) — 이온 다섯 행이 모두 옛 값
STALE_X = [['σ_ionic ratio (physics/Hertzian)', '1.50×', '1.50×', '0%'], ['Contact-free / Full', '2.0×', '2.0×', '0%'],
           ['σ_brug / σ_ionic', '2.0×', '2.0×', '0%']]
#  옛 세대 두 모드의 네 열 CSV = metrics (OLD_DUAL 을 새 표 꼴로 쓴 것 — Physics 값까지 같다)
FOURCOL_EQ = [['── Network Solver (Hertzian DEM-native) ──', '', '', ''],
              ['σ_ionic (mS/cm)', 0.6, 0.9, '+50.0%'], ['R_brug (과대추정 배수)', '2.0×', '1.4×', '-30.0%'],
              ['σ_ionic ratio (physics/Hertzian)', '1.50×', '1.50×', '0%'], ['Constriction 비율(%)', 40.0, 20.0, '-50.0%'],
              ['σ_electronic (mS/cm)', 2.0, 3.0, '+50.0%'], ['σ_thermal (mS/cm equiv)', 0.3, 0.45, '+50.0%'],
              ['Contact-free / Full', '2.0×', '1.4×', '-30.0%'], ['σ_brug / σ_ionic', '2.0×', '1.3×', '-33.3%'],
              ['SE Volume Fraction', 0.5, 0.5, '0%']]


def write_layout(rd, layout):
    """L.LAYOUTS (new · csv · split · fourcol) = L.write_csv 그대로 · fourcol_x = 네 열 + STALE_X · fourcol_eq = FOURCOL_EQ."""
    if layout in L.LAYOUTS:
        return L.write_csv(rd, layout)
    head, rows = L.csv_layout('fourcol')
    rows = rows[:3] + STALE_X + rows[3:] if layout == 'fourcol_x' else FOURCOL_EQ
    p = os.path.join(rd, 'network_summary.csv')
    with open(p, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(head)
        w.writerows(rows)
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


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
    LABS = (ION, RB, CF, SBI, PAMP)                    # 이온 다섯 행 (Pass G 가 다루는 넷 + Plastic amplification)
    MLT = app.MODEL_LIMIT_CELL
    D = '—'

    def by_label(rows):
        """행 → {라벨: [글 칸 …]} (loader 칸은 수 · 글이 섞여 있다 — 화면 글과 같은 꼴로 str)."""
        return {str(r[0]).strip(): [str(x) for x in r] for r in rows if isinstance(r, list) and r}

    def render(cid):
        rd = os.path.join(RES, cid)
        with contextlib.redirect_stdout(io.StringIO()):
            tables, met, _ip = app._load_case_tables(rd, {})
            resp = client.get('/single/' + cid)
        parsed = L._Rows()
        parsed.feed(resp.get_data(as_text=True))
        data = tables['network_summary']['data']
        lo = by_label(data)
        return dict(loader=lo, route=by_label(parsed.rows), full=[[str(x) for x in r] for r in data],
                    route_net={k: v for k, v in by_label(parsed.rows).items() if k in lo}, http=resp.status_code, metrics=met)

    def case(cid, metrics=None, layout='new', bed=None, tm='1:SE'):
        """케이스 하나 — results/<cid> (+ uploads/<cid>/meta.json) · 옛 CSV 먼저 · bed 면 실 생산자 게시 (그 뒤 CSV sha 대조) → 화면 (loader · route)."""
        rd = os.path.join(RES, cid)
        os.makedirs(rd, exist_ok=True)
        os.makedirs(os.path.join(UPL, cid), exist_ok=True)
        with open(os.path.join(UPL, cid, 'meta.json'), 'w', encoding='utf-8') as f:
            json.dump({'name': cid, 'status': 'done', 'scale': 1}, f)
        sha0 = write_layout(rd, layout)
        st = None
        if bed:
            with contextlib.redirect_stdout(io.StringIO()):
                _d, st, _failed, _rid = chain._run_ml(app, bed, tm=tm, d=rd)
        else:
            with open(os.path.join(rd, 'full_metrics.json'), 'w', encoding='utf-8') as f:
                json.dump(metrics, f)
        sha1 = hashlib.sha256(open(os.path.join(rd, 'network_summary.csv'), 'rb').read()).hexdigest()
        v = render(cid)
        v.update(cid=cid, state=st, csv_kept=(sha0 == sha1), layout=layout)
        return v

    def cells(v, w, lab):
        r = v[w].get(lab)
        return None if r is None or len(r) < 4 else r[1:4]

    def miss(v, mode):
        return app._mode_missing_text(v['metrics'], 'ionic', mode)

    def problems(v, ref, use=(True, True), need=(ION, RB, PAMP)):
        """v (옛 CSV 꼴) 의 이온 다섯 행 ↔ 기대 — 어긋난 목록.  ref = 같은 정의의 새 표 (CSV 망 절 없음) 렌더 · use = (Hertz 채택, Physics 채택).
        채택 칸 = ref 의 그 칸 · 미채택 칸 = 모형 한계 문구 또는 '—' (Pass G) · Δ = 두 모드 다 채택이면 ref 의 Δ · 아니면 '—'.
        Plastic amplification = 두 모드 다 채택이면 ref 그대로 · 아니면 — / — / —.  need = 옛 CSV 꼴에 있어야 할 행 (행이 사라져 헛통과하지 않게)."""
        bad = []
        for w in ('loader', 'route'):
            bad += [(w, lab[:20], '행 없음') for lab in need if cells(v, w, lab) is None]
            for lab in LABS:
                got, r = cells(v, w, lab), cells(ref, w, lab)
                if got is None:
                    continue
                if lab == PAMP:
                    want = r if all(use) else [D, D, D]
                elif all(use):
                    want = r
                else:
                    want = [(r[0] if r else None) if use[0] else miss(v, 'hertz'),
                            (r[1] if r else None) if use[1] else miss(v, 'physics'), D]
                if want != got:
                    bad.append((w, lab[:20], 'got', got, 'want', want))
        return bad

    try:
        print('① 실 생산자 ml_el (이온 두 모드 채택 · 전자 Physics 모형 한계) × 옛 CSV — 채택 칸 = 새 표 (현재 값)')
        el = {lay: case(f'web09_ml_el_{lay}', layout=lay, bed='ml_el', tm='1:SE,2:AM_P') for lay in ('new', 'csv', 'split', 'fourcol')}
        st = {k: (v['state'], v['http'], v['csv_kept']) for k, v in el.items()}
        chk(f'①a 게시 = done 넷 · GET /single = 200 · network 게시 뒤 옛 CSV 바이트 그대로 (게시가 contact CSV 를 갱신하지 않는다 — 화면이 맞춰야 하는 이유) {st}',
            all(x == ('done', 200, True) for x in st.values()))
        sh, sp = (el['csv']['metrics'].get(k) for k in ('sigma_full_mScm', 'sigma_full_mScm_physics'))
        want_codex = [str(round(sh, 4)) if isinstance(sh, float) else None, '2.0783', '+73.0%']
        got_codex = [cells(el['csv'], w, ION) for w in ('loader', 'route')]
        chk(f'①b ★ Codex 수치 — 두 열 CSV 이온 σ = 현재 Hertz {sh} / 2.0783 / +73.0% (옛: 0.6 / 2.0783 / +73.0% — Hertz 칸만 옛 CSV · Δ 는 현재 값) {got_codex}',
            isinstance(sh, float) and abs(sh - 1.201613) < 5e-4 and isinstance(sp, float) and abs(sp - 2.078264) < 5e-4
            and all(g == want_codex for g in got_codex), (sh, sp))
        b = {lay: problems(el[lay], el['new']) for lay in ('csv', 'split', 'fourcol')}
        chk(f'①c ★ × (두 열 · split · 네 열) — 이온 다섯 행 (σ · R_brug · CF/Full · σ_brug/σ_ionic · Plastic amplification) 칸 · Δ = 같은 침대의 새 표 (loader · route) {b}',
            not any(b.values()))

        print('② 합성 현재 값 (두 모드 채택 · 옛 CSV 와 다른 수) × 옛 CSV 꼴')
        cur = {lay: case(f'web09_cur_{lay}', current(), lay) for lay in ('new', 'csv', 'split', 'fourcol', 'fourcol_x')}
        b = {lay: problems(cur[lay], cur['new']) for lay in ('csv', 'split', 'fourcol', 'fourcol_x')}
        chk(f'②a ★ × (두 열 · split · 네 열 · 네 열+ (CF/Full · σ_brug/σ_ionic · 비 행까지 옛 값)) — 이온 다섯 행 = 새 표 (σ 1.2016 / 2.0783 / +73.0% · '
            f'R_brug 3.3× / 1.9× · 비 1.73×) · split 의 옛 Δ 식 · 네 열 옛 Δ 0% 도 새 표 Δ {b}', not any(b.values()))

        print('③ Hertz 채택 + Physics FULL 모형 한계')
        ph = {lay: case(f'web09_ml_physics_{lay}', layout=lay, bed='ml_physics') for lay in ('new', 'csv', 'split', 'fourcol')}
        shp = ph['csv']['metrics'].get('sigma_full_mScm')
        got_p = [cells(ph['csv'], w, ION) for w in ('loader', 'route')]
        chk(f'③a ★ Codex 수치 — ml_physics 두 열 CSV 이온 σ Hertz = 현재 {shp} → {str(round(shp, 4)) if isinstance(shp, float) else None} (옛: 0.6) · Physics = 모형 한계 '
            f'문구 · Δ — {got_p}',
            isinstance(shp, float) and abs(shp - 2.386067) < 5e-4 and all(g == [str(round(shp, 4)), MLT, D] for g in got_p),
            [v['state'] for v in ph.values()])
        b = {lay: problems(ph[lay], ph['new'], (True, False)) for lay in ('csv', 'split', 'fourcol')}
        chk(f'③b ★ ml_physics × (두 열 · split · 네 열) — Hertz 칸 = 새 표 Hertz 칸 (현재 값) · Physics = 모형 한계 문구 · Δ — · Plastic amplification — / — / — {b}',
            not any(b.values()))
        pn = {lay: case(f'web09_cur_physics_null_{lay}', current('physics:null'), lay) for lay in ('new', 'csv', 'split', 'fourcol', 'fourcol_x')}
        b = {lay: problems(pn[lay], pn['new'], (True, False)) for lay in ('csv', 'split', 'fourcol', 'fourcol_x')}
        chk(f'③c ★ 합성 Hertz 채택 (1.2016 · 3.3×) + Physics 모형 한계 × (두 열 · split · 네 열 · 네 열+) — 같은 규약 {b}', not any(b.values()))

        print('④ Physics 채택 + Hertz FULL 모형 한계 — Physics 칸 = 새 표 식 (두 모드 채택 짝의 Physics 칸)')
        hn = {lay: case(f'web09_cur_hertz_null_{lay}', current('hertz:null'), lay) for lay in ('csv', 'split', 'fourcol', 'fourcol_x')}
        b = {lay: problems(hn[lay], cur['new'], (False, True)) for lay in hn}
        chk(f'④a ★ × (두 열 · split · 네 열 · 네 열+) — Physics 칸 = 현재 값 (2.0783 · 1.9× · CF/Full 1.9× · σ_brug/σ_ionic 0.6×) · Hertz = 모형 한계 문구 · '
            f'Δ — (옛: split 0.9 · 네 열 0.6 · 2.0×) {b}', not any(b.values()))

        print('⑤ 옛 세대 (생산자 상태 키 없음)')
        lg = {lay: case(f'web09_legacy_single_{lay}', L.synth('legacy_single'), lay) for lay in ('csv', 'split', 'fourcol')}
        want_lg = {ION: ['0.6', D, D], RB: ['2.0×', D, D], CF: ['2.0×', D, D], SBI: ['2.0×', D, D], PAMP: [D, D, D]}
        got = {lay: {lab[:12]: [cells(v, w, lab) for w in ('loader', 'route')] for lab in LABS} for lay, v in lg.items()}
        chk(f'⑤a 옛 세대 단일 모드 + CSV = metrics (σ 0.6 · R_brug 2.0×) × (두 열 · split · 네 열) → 수정 전 화면 그대로 (σ 0.6 / — / — · R_brug · CF/Full · '
            f'σ_brug/σ_ionic 2.0× / — / — · Plastic amplification — / — / —) {got}',
            all(cells(v, w, lab) == want for v in lg.values() for w in ('loader', 'route') for lab, want in want_lg.items()))
        od = {lay: case(f'web09_old_dual_{lay}', OLD_DUAL, lay) for lay in ('split', 'fourcol_eq')}
        want_od = {ION: ['0.6', '0.9', '+50.0%'], RB: ['2.0×', '1.4×', '-30.0%'], CF: ['2.0×', '1.4×', '-30.0%'], SBI: ['2.0×', '1.3×', '-33.3%'],
                   PAMP: ['1.50×', '1.50×', '0%']}
        got = {lay: {lab[:12]: [cells(v, w, lab) for w in ('loader', 'route')] for lab in LABS} for lay, v in od.items()}
        chk(f'⑤b 옛 세대 두 모드 + CSV = metrics (split · Physics 값까지 같은 네 열) → 수정 전 화면 그대로 {got}',
            all(cells(v, w, lab) == want for v in od.values() for w in ('loader', 'route') for lab, want in want_od.items()))
        lgc_mx = dict(L.synth('legacy_single'), sigma_full_mScm=1.2016, R_brug_over_full=3.3)
        lgc = case('web09_legacy_cur_csv', lgc_mx, 'csv')
        lgc_new = case('web09_legacy_cur_new', lgc_mx, 'new')
        b = problems(lgc, lgc_new, (True, False))
        chk(f'⑤c ★ 옛 세대 + 현재 값 ≠ CSV (σ 1.2016 · R_brug 3.3× ↔ CSV 0.6 · 2.0×) + 두 열 → Hertz 칸 = 새 표 (현재 값) · Physics — · Δ — {b}', not b)
        lgm = case('web09_legacy_no_rbrug_csv', {k: v for k, v in L.synth('legacy_single').items() if k != 'R_brug_over_full'}, 'csv')
        got = [cells(lgm, w, RB) for w in ('loader', 'route')]
        chk(f'⑤d 옛 세대 + 필요한 metric 없음 (R_brug_over_full 키 없음) + 두 열 CSV R_brug 2.0× → 그 칸 그대로 (지어내지도 지우지도 않는다) · Physics — · Δ — {got}',
            all(g == ['2.0×', D, D] for g in got))
        odm = case('web09_old_dual_no_rbp_fourcol',
                   dict({k: v for k, v in OLD_DUAL.items() if k != 'R_brug_over_full_physics'}, R_brug_over_full=3.3), 'fourcol')
        got = {lab[:12]: [cells(odm, w, lab) for w in ('loader', 'route')] for lab in (ION, RB)}
        chk(f'⑤e ★ 옛 세대 두 모드 + Physics R_brug metric 없음 + 네 열 옛 CSV (σ 0.6 / 0.6 / 0% · R_brug 2.0× / 2.0× / 0%) → σ = 0.6 / 0.9 / +50.0% (현재) · '
            f'R_brug = 3.3× (현재) / 2.0× (옛 칸 그대로 — 지어내지 않는다) / — (Δ 는 두 칸이 다 현재 값일 때만) {got}',
            all(cells(odm, w, ION) == ['0.6', '0.9', '+50.0%'] and cells(odm, w, RB) == ['3.3×', '2.0×', D] for w in ('loader', 'route')))

        print('⑥ valid_zero (증명된 비관통) — 이온 칸 그대로 \'—\' (1저자 Q2)')
        vz = {}
        for kind in ('both:valid_zero_null', 'both:valid_zero_numeric'):
            for lay in ('csv', 'split', 'fourcol', 'fourcol_x'):
                v = case(f'web09_{kind.replace(":", "_")}_{lay}', L.synth(kind), lay)
                vz[(kind, lay)] = [(w, lab[:12], cells(v, w, lab)) for w in ('loader', 'route') for lab in LABS
                                   if cells(v, w, lab) not in (None, [D, D, D])]
        chk(f'⑥a valid_zero (σ None · 0) × (두 열 · split · 네 열 · 네 열+) → 이온 다섯 행 칸 · Δ 전부 — (옛 CSV 숫자 · 0 없음) {vz}', not any(vz.values()))

        print('⑦ 정상 새 표 (CSV 망 절 없음) — 수정 전과 똑같이')
        news = {'normal': case('web09_normal_new', L.synth('normal'), 'new'), 'cur': cur['new'], 'physics_null': case('web09_physics_null_new', L.synth('physics:null'), 'new'),
                'legacy_single': case('web09_legacy_single_new', L.synth('legacy_single'), 'new'), 'cur_physics_null': pn['new'],
                'hertz_null': case('web09_hertz_null_new', L.synth('hertz:null'), 'new'),
                'valid_zero': case('web09_valid_zero_new', L.synth('both:valid_zero_null'), 'new'),
                'ml_el': el['new'], 'ml_physics': ph['new'], 'ml_hertz': case('web09_ml_hertz_new', layout='new', bed='ml_hertz')}
        #  수정 전 (2fc138274) 화면의 이온 다섯 행 (loader = route) — None = 행 없음
        G = {
            'normal': {ION: ['0.6', '0.9', '+50.0%'], RB: ['2.0×', '1.4×', '-30.0%'], CF: ['2.0×', '1.4×', '-30.0%'], SBI: ['2.0×', '1.3×', '-33.3%'],
                       PAMP: ['1.50×', '1.50×', '0%']},
            'cur': {ION: ['1.2016', '2.0783', '+73.0%'], RB: ['3.3×', '1.9×', '-42.4%'], CF: ['3.3×', '1.9×', '-42.4%'], SBI: ['1.0×', '0.6×', '-42.2%'],
                    PAMP: ['1.73×', '1.73×', '0%']},
            'physics_null': {ION: ['0.6', MLT, D], RB: ['2.0×', MLT, D], CF: ['2.0×', MLT, D], SBI: ['2.0×', MLT, D], PAMP: [D, D, D]},
            'legacy_single': {ION: ['0.6', D, D], RB: ['2.0×', D, D], CF: ['2.0×', D, D], SBI: ['2.0×', D, D], PAMP: [D, D, D]},
            'cur_physics_null': {ION: ['1.2016', MLT, D], RB: ['3.3×', MLT, D], CF: ['3.3×', MLT, D], SBI: ['1.0×', MLT, D], PAMP: [D, D, D]},
            'hertz_null': {}, 'valid_zero': {}, 'ml_hertz': {},
            'ml_el': {ION: ['1.2016', '2.0783', '+73.0%'], RB: ['9.8×', '5.7×', '-42.2%'], CF: ['9.8×', '5.7×', '-42.2%'], SBI: None,
                      PAMP: ['1.73×', '1.73×', '0%']},
            'ml_physics': {ION: ['2.3861', MLT, D], RB: ['4.9×', MLT, D], CF: ['4.9×', MLT, D], SBI: None, PAMP: [D, D, D]},
        }
        bad = [(nm, w, lab[:12], cells(news[nm], w, lab), G[nm].get(lab)) for nm in G for w in ('loader', 'route') for lab in LABS
               if cells(news[nm], w, lab) != G[nm].get(lab)]
        chk(f'⑦a 새 표 이온 다섯 행 = 수정 전 화면 (합성 정상 · 현재 값 · Physics 모형 한계 · 옛 세대 · 실 생산자 ml_el · ml_physics / 행 없음 = H0 모형 한계 · '
            f'valid_zero · ml_hertz) (loader · route) {bad}', not bad)
        fn = getattr(app, '_refresh_accepted_ion_modes', None)
        if fn is not None:
            app._refresh_accepted_ion_modes = lambda data, metrics: None
        try:
            off = {nm: render(v['cid']) for nm, v in news.items()}
        finally:
            if fn is not None:
                app._refresh_accepted_ion_modes = fn
        bad = [nm for nm, v in news.items() if v['full'] != off[nm]['full'] or v['route_net'] != off[nm]['route_net']]
        chk(f'⑦b 새 표 전체 (모든 행 · 칸 · loader · route) = 채택 갱신 단계를 끈 렌더 — 그 단계는 새 표에서 아무것도 바꾸지 않는다 '
            f'(수정 전 = 그 단계 없음 · 같은 렌더 두 번) {bad}', not bad and all(v['http'] == 200 for v in news.values()))
    finally:
        shutil.rmtree(WORK, ignore_errors=True)
    print(f'\ntest_web09_accepted_refresh: {PASS}/{PASS + FAIL} PASS' + ('' if not FAIL else f'   ({FAIL} FAIL)'))
    return 0 if not FAIL else 1


if __name__ == '__main__':
    sys.exit(main())
