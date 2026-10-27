#!/usr/bin/env python3
"""50kg D3 칸 판정 판독기 — 웹앱 결과 여섯 (SE D50 3 µm · 40×40 / 50×50 · 시드 3) → 등록 지표 넷 → 평균 차 · SE_Δ → 판정.

등록 = `docs/data/kg50_decks_20261026_v2/README.md` §3 (1저자 10-26 밤 Q6 · 판정 모드 Hertz = 1저자 10-27 결과 전).
읽기만 한다 — 웹앱 결과 폴더 (`full_metrics.json` · `network_conductivity_dual.json` · `network_provenance.json`) 와 업로드
폴더의 `meta.json` 을 읽고, 값을 새로 계산하지 않는다 (규율 ①):
  • 수송 tortuosity = `tau_flux.case_row` 그대로 (인계 열 `tau2_ion_hertz` · 세대 · 상태 검사 포함)
  • σ_ion = 솔버의 Hertz σ FULL (`dual['hertzian']['sigma_full_mScm']` · 상태 computed 만)
  • porosity = 웹앱 `porosity` (ε_sphere — `porosity_spheresum` 과 같은 값이어야 한다)
  • AM coverage = 둘 다 판정 (1저자 10-27 *"am coverage는 physics로 봤잖아 / 같이 봐"*) — <AM> = meta type_map 의 유일한 AM 상
      Physics = 웹앱 `coverage_<AM>_mean_physics_union` (합집합 cap · 웹앱 표 Physics 열 · `coverage_status_physics_union` = ok 만)
      Hertz   = 웹앱 `coverage_<AM>_mean` (Hertz 계열 = LIGGGHTS 접촉 면적)

지표 다섯 (문턱 = 등록 §3 · σ_ion · 수송 tortuosity = Hertz · coverage = Physics · Hertz 둘 다)
  porosity          절대 차 %p   문턱 0.5
  coverage_physics  절대 차 %p   문턱 1
  coverage_hertz    절대 차 %p   문턱 1
  tau2              상대 차 %    문턱 5   (분모 = 50×50 평균)
  sigma_ion         상대 차 %    문턱 5   (분모 = 50×50 평균)
  Δ = 평균(40) − 평균(50) · SE_Δ = √(s40²/3 + s50²/3) (s = 시드 3 의 표본 표준편차) · 상대 지표는 둘 다 평균(50) 으로 나눈다.

지표마다 판정 — 위에서부터 먼저 걸리는 것 (결과 전 명확화 · 1저자 10-27)
  ① 여섯 값 중 하나라도 비유한 · 상태 미달 (비관통 · 풀이 실패 포함)  → 판정 불가
  ② SE_Δ > 문턱                                                      → 판정 불가 (시드 산포가 문턱보다 크다)
  ③ |Δ| > 문턱                                                       → 불합격
  ④ 그 밖                                                            → 통과
전체 — 하나라도 불합격 → 불합격 (50×50 · `--fallback50`) · 아니고 하나라도 판정 불가 → 판정 불가 (1저자 결정) ·
       넷 다 통과 → "D3 등록 지표 평균 차 기준 통과" (D0.7 · D1 · D2 를 40×40 으로 — 그 영역을 채택한 탐색 비교 · 영역 수렴 주장 아님)

입력 거부 (rc 2 · 판정 없음): 케이스 이름이 0 개 · 여러 개 · 필수 파일 없음 · 여섯의 망 코드 판 (`network_provenance.code_sha`) 이 다름 ·
  meta type_map 의 AM 상이 하나가 아님.

사용 (저자 WSL — 웹앱 결과가 있는 기계)
    python3 scripts/kg50_d3_cell_verdict.py                                  # 기본 = 웹앱 uploads · results (WEBAPP_*_FOLDER 또는 리포 webapp/)
    python3 scripts/kg50_d3_cell_verdict.py --uploads-root U --results-root R --json out.json
    python3 scripts/kg50_d3_cell_verdict.py --case kg50_d3_b40_s1=<케이스 id> …   # 같은 이름이 여러 개일 때 id 로 지정
    python3 scripts/kg50_d3_cell_verdict.py --selftest
웹앱 화면 없음 (일회성 등록 판정 · 결과는 `docs/data/` 기록으로 남긴다).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import statistics
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

SCHEMA = 'kg50_d3_cell_verdict/v1'
REGISTRATION = 'docs/data/kg50_decks_20261026_v2/README.md §3'
B40 = ('kg50_d3_b40_s1', 'kg50_d3_b40_s2', 'kg50_d3_b40_s3')
B50 = ('kg50_d3_b50_s1', 'kg50_d3_b50_s2', 'kg50_d3_b50_s3')
NAMES = B40 + B50
#: (키, 표시 이름, 종류, 문턱) — 종류 abs = 절대 차 (단위 그대로) · rel = 상대 차 % (분모 = 50×50 평균)
INDICATORS = (
    ('porosity', 'porosity ε_sphere (%)', 'abs', 0.5),
    ('coverage_physics', 'AM coverage Physics (%)', 'abs', 1.0),
    ('coverage_hertz', 'AM coverage Hertz (%)', 'abs', 1.0),
    ('tau2', '수송 tortuosity Hertz', 'rel', 5.0),
    ('sigma_ion', 'σ_ion Hertz (mS/cm)', 'rel', 5.0),
)
PASS, FAIL, UNDECIDED = '통과', '불합격', '판정 불가'
OVERALL_PASS = 'D3 등록 지표 평균 차 기준 통과'


class Refused(Exception):
    """입력이 판정을 낼 자격이 없다 (rc 2)."""


def _load_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def _default_roots():
    up = os.environ.get('WEBAPP_UPLOAD_FOLDER') or os.path.join(ROOT, 'webapp', 'uploads')
    rs = os.environ.get('WEBAPP_RESULTS_FOLDER') or os.path.join(ROOT, 'webapp', 'results')
    return up, rs


def find_cases(uploads_root, explicit):
    """이름 → (케이스 id, meta).  explicit = {이름: id} (지정분은 이름 대조 없이 그 id 의 meta 를 읽는다)."""
    by_name = {}
    if os.path.isdir(uploads_root):
        for cid in sorted(os.listdir(uploads_root)):
            meta = None
            try:
                meta = _load_json(os.path.join(uploads_root, cid, 'meta.json'))
            except (OSError, ValueError):
                meta = None                       # 깨진 meta 는 후보에서 빠진다 (이름을 알 수 없다)
            if isinstance(meta, dict) and meta.get('name') in NAMES:
                by_name.setdefault(meta['name'], []).append((cid, meta))
    out, probs = {}, []
    for n in NAMES:
        if n in explicit:
            cid = explicit[n]
            meta = _load_json(os.path.join(uploads_root, cid, 'meta.json'))
            if not isinstance(meta, dict):
                probs.append(f'{n}: 지정한 id {cid} 의 meta.json 이 없다')
                continue
            out[n] = (cid, meta)
            continue
        hits = by_name.get(n, [])
        if len(hits) == 1:
            out[n] = hits[0]
        elif not hits:
            probs.append(f'{n}: 이 이름의 웹앱 케이스가 없다 (업로드 이름 확인)')
        else:
            probs.append(f'{n}: 같은 이름 케이스 {len(hits)} 개 ({", ".join(c for c, _ in hits)}) — --case {n}=<id> 로 지정')
    if probs:
        raise Refused('; '.join(probs))
    return out


def am_phase(meta):
    import type_map_resolve as TMR
    names = [v for v in TMR.parse_map(meta.get('type_map') or '').values() if v.startswith('AM')]
    if len(names) != 1:
        raise Refused(f'meta type_map {meta.get("type_map")!r} 의 AM 상이 하나가 아니다 ({names})')
    return names[0]


def extract(results_dir, meta, case_row_fn=None):
    """한 케이스 → {'values': {지표: 값 | None}, 'notes': {지표: 사유}, 'code_sha': …, …}.  값 · 상태 문제는 None + 사유 (판정 불가 재료)."""
    if case_row_fn is None:
        import tau_flux as TF
        case_row_fn = TF.case_row
    fm = _load_json(os.path.join(results_dir, 'full_metrics.json'))
    dual = _load_json(os.path.join(results_dir, 'network_conductivity_dual.json'))
    prov = _load_json(os.path.join(results_dir, 'network_provenance.json'))
    missing = [n for n, d in (('full_metrics.json', fm), ('network_conductivity_dual.json', dual),
                              ('network_provenance.json', prov)) if not isinstance(d, dict)]
    if missing:
        raise Refused(f'{results_dir}: 필수 파일 없음 · 깨짐 ({", ".join(missing)})')
    vals, notes = {}, {}
    # porosity — ε_sphere (웹앱 porosity = porosity_spheresum · 다르면 정의가 바뀐 것)
    p, ps = fm.get('porosity'), fm.get('porosity_spheresum')
    if not _finite(p):
        vals['porosity'], notes['porosity'] = None, f'porosity 비유한 ({p!r})'
    elif ps is not None and not (_finite(ps) and float(ps) == float(p)):
        vals['porosity'], notes['porosity'] = None, f'porosity {p!r} ≠ porosity_spheresum {ps!r} (ε_sphere 아님)'
    else:
        vals['porosity'] = float(p)
    # AM coverage — Physics (합집합 cap · 상태 ok 만) · Hertz 계열 둘 다 (meta type_map 의 유일한 AM 상)
    am = am_phase(meta)
    ck = f'coverage_{am}_mean'
    pk = f'coverage_{am}_mean_physics_union'
    pst = fm.get('coverage_status_physics_union')
    for key, src, extra in (('coverage_hertz', ck, None), ('coverage_physics', pk, pst)):
        c = fm.get(src)
        if key == 'coverage_physics' and extra != 'ok':
            vals[key], notes[key] = None, f'coverage_status_physics_union {extra!r} (ok 아님)'
        elif not _finite(c) or not 0.0 <= float(c) <= 100.0:
            vals[key], notes[key] = None, f'{src} 비유한 · 범위 밖 ({c!r})'
        else:
            vals[key] = float(c)
    # σ_ion — 솔버 Hertz σ FULL · computed 만
    h = dual.get('hertzian') if isinstance(dual.get('hertzian'), dict) else {}
    s, st = h.get('sigma_full_mScm'), h.get('sigma_full_status')
    if st != 'computed' or not _finite(s) or float(s) <= 0.0:
        vals['sigma_ion'], notes['sigma_ion'] = None, f'Hertz σ_ion 상태 {st!r} · 값 {s!r} (비관통 · 풀이 실패 = 판정 불가)'
    else:
        vals['sigma_ion'] = float(s)
    # 수송 tortuosity — tau_flux.case_row 그대로 (상태 OK 만)
    row = case_row_fn(results_dir) or {}
    t, ts = row.get('tau2_ion_hertz'), row.get('ion_net_status_hertz')
    if ts != 'OK' or not _finite(t) or float(t) <= 0.0:
        vals['tau2'], notes['tau2'] = None, (f'tau2_ion_hertz 상태 {ts!r} ({row.get("ion_net_status_reason_hertz") or "-"}) · '
                                             f'값 {t!r}')
    else:
        vals['tau2'] = float(t)
    return {'values': vals, 'notes': notes, 'am_phase': am, 'coverage_key': ck, 'coverage_physics_key': pk,
            'code_sha': prov.get('code_sha'), 'network_run_id': prov.get('network_run_id') or fm.get('network_run_id'),
            'ion_net_electrode_hertz': row.get('ion_net_electrode_hertz'),
            'ion_net_area_rule_hertz': row.get('ion_net_area_rule_hertz'),
            'f_ion_hertz': row.get('f_ion_hertz')}


def judge(v40, v50, kind, thr):
    """지표 하나 → dict (m40 · s40 · m50 · s50 · delta · se · result · why).  판정 순서 = 모듈 docstring ①–④."""
    rec = {'kind': kind, 'threshold': thr, 'v40': list(v40), 'v50': list(v50),
           'm40': None, 's40': None, 'm50': None, 's50': None, 'delta': None, 'se': None}
    if len(v40) != 3 or len(v50) != 3 or not all(_finite(x) for x in list(v40) + list(v50)):
        rec.update(result=UNDECIDED, why='① 여섯 값 중 비유한 · 상태 미달이 있다')
        return rec
    m40, m50 = statistics.fmean(v40), statistics.fmean(v50)
    s40, s50 = statistics.stdev(v40), statistics.stdev(v50)
    d, se = m40 - m50, math.sqrt(s40 ** 2 / 3.0 + s50 ** 2 / 3.0)
    if kind == 'rel':
        if not m50 > 0.0:
            rec.update(m40=m40, s40=s40, m50=m50, s50=s50, result=UNDECIDED, why='① 50×50 평균이 0 이하 (상대 차 분모 없음)')
            return rec
        d, se = 100.0 * d / m50, 100.0 * se / m50
    rec.update(m40=m40, s40=s40, m50=m50, s50=s50, delta=d, se=se)
    if se > thr:
        rec.update(result=UNDECIDED, why=f'② SE_Δ {se:.4g} > 문턱 {thr:g} (시드 산포가 문턱보다 크다)')
    elif abs(d) > thr:
        rec.update(result=FAIL, why=f'③ |Δ| {abs(d):.4g} > 문턱 {thr:g}')
    else:
        rec.update(result=PASS, why=f'④ |Δ| {abs(d):.4g} ≤ 문턱 {thr:g} · SE_Δ {se:.4g} ≤ 문턱')
    return rec


def overall(results):
    rs = [r['result'] for r in results.values()]
    if FAIL in rs:
        return FAIL, '하나 이상 불합격 → 50×50 (--fallback50)'
    if UNDECIDED in rs:
        return UNDECIDED, '불합격은 없고 판정 불가가 있다 → 1저자 결정'
    return PASS, OVERALL_PASS + ' → D0.7 · D1 · D2 를 40×40 으로 (그 영역을 채택한 탐색 비교 · 영역 수렴 주장 아님)'


def run(uploads_root, results_root, explicit, case_row_fn=None):
    cases = find_cases(uploads_root, explicit)
    per = {}
    for n in NAMES:
        cid, meta = cases[n]
        rdir = os.path.join(results_root, cid)
        if not os.path.isdir(rdir):
            raise Refused(f'{n}: 결과 폴더 없음 ({rdir}) — 웹앱 분석이 끝났는지 확인')
        e = extract(rdir, meta, case_row_fn)
        e.update(case_id=cid, name=n)
        per[n] = e
    shas = sorted({str(per[n]['code_sha']) for n in NAMES})
    if len(shas) != 1 or shas[0] in ('', 'None'):
        raise Refused(f'여섯 케이스의 망 코드 판이 같지 않다 · 없다 ({shas}) — 같은 판으로 다시 분석')
    res = {}
    for key, _lab, kind, thr in INDICATORS:
        res[key] = judge([per[n]['values'][key] for n in B40], [per[n]['values'][key] for n in B50], kind, thr)
    ov, why = overall(res)
    return {'schema': SCHEMA, 'registration': REGISTRATION, 'mode': 'hertz', 'code_sha': shas[0],
            'cases': per, 'indicators': res, 'overall': ov, 'overall_why': why}


def _fmt(x, nd=4):
    return '—' if x is None else (f'{x:.{nd}g}' if isinstance(x, float) else str(x))


def report(out):
    lines = [f'# 50kg D3 칸 판정 — {out["registration"]} · 판정 모드 Hertz · 망 코드 판 {out["code_sha"]}', '',
             '| 케이스 | 웹앱 id | porosity % | coverage Physics % | coverage Hertz % | 수송 tortuosity | σ_ion mS/cm | 메모 |',
             '|---|---|---|---|---|---|---|---|']
    for n in NAMES:
        c = out['cases'][n]
        v = c['values']
        memo = ' · '.join(f'{k}: {w}' for k, w in c['notes'].items()) or '-'
        lines.append(f'| {n} | {c["case_id"]} | {_fmt(v["porosity"])} | {_fmt(v["coverage_physics"])} | '
                     f'{_fmt(v["coverage_hertz"])} | {_fmt(v["tau2"])} | {_fmt(v["sigma_ion"])} | {memo} |')
    lines += ['', '| 지표 | 평균 40 (s) | 평균 50 (s) | Δ | SE_Δ | 문턱 | 판정 | 근거 |', '|---|---|---|---|---|---|---|---|']
    for key, lab, kind, thr in INDICATORS:
        r = out['indicators'][key]
        unit = '%p' if kind == 'abs' else '%'
        lines.append(f'| {lab} | {_fmt(r["m40"])} ({_fmt(r["s40"], 2)}) | {_fmt(r["m50"])} ({_fmt(r["s50"], 2)}) | '
                     f'{_fmt(r["delta"], 3)} {unit} | {_fmt(r["se"], 3)} {unit} | {thr:g} {unit} | {r["result"]} | {r["why"]} |')
    lines += ['', f'**전체: {out["overall"]}** — {out["overall_why"]}']
    return '\n'.join(lines)


# ───────────────────────────── selftest ─────────────────────────────
def _tree_digest(root):
    h = hashlib.sha256()
    for d, _ds, fs in sorted(os.walk(root)):
        for f in sorted(fs):
            p = os.path.join(d, f)
            h.update(p.encode())
            with open(p, 'rb') as fh:
                h.update(fh.read())
    return h.hexdigest()


def _mk(root, cid, name, *, por=10.0, cov=50.0, covp=60.0, covp_status='ok', sig=0.1, sig_status='computed', sha='abc',
        tm='1:AM_P,3:SE', spheresum='same'):
    up, rs = os.path.join(root, 'uploads', cid), os.path.join(root, 'results', cid)
    os.makedirs(up, exist_ok=True)
    os.makedirs(rs, exist_ok=True)
    with open(os.path.join(up, 'meta.json'), 'w') as f:
        json.dump({'name': name, 'type_map': tm}, f)
    fm = {'porosity': por, 'coverage_AM_P_mean': cov, 'coverage_AM_P_mean_physics_union': covp,
          'coverage_status_physics_union': covp_status, 'network_run_id': 'run-' + cid}
    if spheresum == 'same':
        fm['porosity_spheresum'] = por
    elif spheresum is not None:
        fm['porosity_spheresum'] = spheresum
    with open(os.path.join(rs, 'full_metrics.json'), 'w') as f:
        json.dump(fm, f)
    with open(os.path.join(rs, 'network_conductivity_dual.json'), 'w') as f:
        json.dump({'hertzian': {'sigma_full_mScm': sig, 'sigma_full_status': sig_status}}, f)
    with open(os.path.join(rs, 'network_provenance.json'), 'w') as f:
        json.dump({'code_sha': sha, 'network_run_id': 'run-' + cid}, f)


def _stub_rows(tau):
    """케이스 폴더 이름 → tau2 (stub case_row — 실제 사슬은 시험 ⑪ 이 따로 본다)."""
    def fn(rdir):
        t = tau.get(os.path.basename(rdir))
        if t is None:
            return {'tau2_ion_hertz': None, 'ion_net_status_hertz': 'NOT_COMPUTED', 'ion_net_status_reason_hertz': 'no_path'}
        if isinstance(t, tuple):                     # (값, 상태) — 상태 미달인데 값이 남은 꼴
            return {'tau2_ion_hertz': t[0], 'ion_net_status_hertz': t[1], 'ion_net_status_reason_hertz': 'stub'}
        return {'tau2_ion_hertz': t, 'ion_net_status_hertz': 'OK', 'ion_net_electrode_hertz': 'x', 'f_ion_hertz': 0.1}
    return fn


def _bed(root, spec, tau=None):
    """spec = {이름: kwargs} — 없는 이름은 기본값 (모두 같다 → 통과)."""
    tau = dict(tau or {})
    for i, n in enumerate(NAMES):
        cid = f'c{i}'
        _mk(root, cid, n, **spec.get(n, {}))
        tau.setdefault(cid, 4.0)
    return _stub_rows(tau)


def registration_check():
    """등록 README §3 의 문턱 · 분모 · 모드 문장이 이 파일의 상수와 같은가 — 결과를 보고 문턱을 옮기면 게이트가 터진다.
    반환 (ok, 사유)."""
    import re
    path = os.path.join(ROOT, *REGISTRATION.split(' ')[0].split('/'))
    try:
        txt = open(path, encoding='utf-8').read()
    except OSError as e:
        return False, f'등록 문서 못 읽음 ({e})'
    m = re.search(r'porosity \(ε_sphere\) ([0-9.]+) %p · AM coverage ([0-9.]+) %p · 수송 tortuosity ([0-9.]+) % · '
                  r'σ_ion ([0-9.]+) % \(상대 차 분모 = 50×50 평균\)', txt)
    if not m:
        return False, '§3 문턱 문장을 못 찾음'
    reg = tuple(float(x) for x in m.groups())
    thr = {k: t for k, _l, _k, t in INDICATORS}
    ours = (thr['porosity'], thr['coverage_physics'], thr['tau2'], thr['sigma_ion'])
    if reg != ours or thr['coverage_hertz'] != thr['coverage_physics']:
        return False, f'문턱 다름 — 등록 {reg} ↔ 판독기 {ours} · coverage 두 문턱 {thr["coverage_physics"]} / {thr["coverage_hertz"]}'
    if '판정 모드 = Hertz' not in txt:
        return False, '§3 에 "판정 모드 = Hertz" 줄 없음'
    if 'AM coverage = Physics · Hertz 둘 다 판정' not in txt:
        return False, '§3 에 "AM coverage = Physics · Hertz 둘 다 판정" 줄 없음'
    if 'SE_Δ = √(s40²/3 + s50²/3)' not in txt:
        return False, '§3 의 SE_Δ 식이 판독기와 다름'
    return True, f'등록 문턱 {reg} = 판독기 · 모드 Hertz · SE_Δ 식 같음'


def selftest():
    ok_all = True

    def chk(label, cond, extra=''):
        nonlocal ok_all
        ok_all &= bool(cond)
        print(f'  {"✓" if cond else "✗"} {label}{(" — " + extra) if extra and not cond else ""}')

    rok, rwhy = registration_check()
    chk('⓪ 등록 README §3 문턱 · 모드 · SE_Δ 식 = 판독기 상수 (결과 뒤 문턱 이동 차단)', rok, rwhy)

    def go(root, fn, explicit=None):
        return run(os.path.join(root, 'uploads'), os.path.join(root, 'results'), explicit or {}, fn)

    jit = {  # 시드 산포 (작다) — 같은 상자끼리 조금씩 다르게
        'kg50_d3_b40_s1': 0.00, 'kg50_d3_b40_s2': 0.02, 'kg50_d3_b40_s3': -0.02,
        'kg50_d3_b50_s1': 0.01, 'kg50_d3_b50_s2': -0.01, 'kg50_d3_b50_s3': 0.00}
    print('kg50_d3_cell_verdict selftest')
    # ① 통과 — 여섯 거의 같다
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {n: dict(por=10 + j, cov=50 + j, covp=60 + j, sig=0.1 * (1 + j / 100)) for n, j in jit.items()})
        before = _tree_digest(r)
        out = go(r, fn)
        chk('① 거의 같은 여섯 → 전체 통과 · 지표 다섯 통과', out['overall'] == PASS
            and all(out['indicators'][k]['result'] == PASS for k, *_ in INDICATORS), str(out['overall']))
        chk('①b 읽기만 — 입력 트리 바이트 그대로', _tree_digest(r) == before)
        chk('①c 보고 표에 여섯 줄 + 지표 넷 + 전체', report(out).count('| kg50_d3_') == 6 and '**전체: 통과**' in report(out))
    # ② porosity 불합격 — 40 쪽이 0.8 %p 높고 산포 작다
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {n: dict(por=(10.8 if n in B40 else 10.0) + j) for n, j in jit.items()})
        out = go(r, fn)
        pr = out['indicators']['porosity']
        chk('② |Δ| 0.8 %p > 0.5 · SE 작음 → porosity 불합격 · 전체 불합격', pr['result'] == FAIL and out['overall'] == FAIL
            and abs(pr['delta'] - 0.8) < 1e-9, f'{pr}')
    # ③ 우선순위 — |Δ| > 문턱 이어도 SE_Δ > 문턱 이면 판정 불가
    with tempfile.TemporaryDirectory() as r:
        big = {'kg50_d3_b40_s1': 0.0, 'kg50_d3_b40_s2': 1.5, 'kg50_d3_b40_s3': -1.5,
               'kg50_d3_b50_s1': 0.0, 'kg50_d3_b50_s2': 1.2, 'kg50_d3_b50_s3': -1.2}
        fn = _bed(r, {n: dict(por=(11.0 if n in B40 else 10.0) + j) for n, j in big.items()})
        out = go(r, fn)
        pr = out['indicators']['porosity']
        chk('③ |Δ| 1.0 > 0.5 이고 SE_Δ > 0.5 → 판정 불가 (② 가 ③ 보다 먼저) · 전체 판정 불가',
            pr['result'] == UNDECIDED and pr['why'].startswith('②') and out['overall'] == UNDECIDED, f'{pr}')
    # ④ 상대 차 분모 = 50×50 평균 · 경계 (≤ 문턱 = 통과)
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {n: dict(sig=(0.105 if n in B40 else 0.1)) for n in NAMES})
        out = go(r, fn)
        sr = out['indicators']['sigma_ion']
        chk('④ σ 0.105 vs 0.100 → Δ = +5.000 % (분모 50) · 산포 0 → 경계 통과', sr['result'] == PASS
            and abs(sr['delta'] - 5.0) < 1e-9 and sr['se'] == 0.0, f'{sr}')
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {n: dict(sig=(0.106 if n in B40 else 0.1)) for n in NAMES})
        out = go(r, fn)
        chk('④b σ 0.106 vs 0.100 → Δ 6 % > 5 → 불합격', out['indicators']['sigma_ion']['result'] == FAIL)
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {n: dict(sig=(0.1 if n in B40 else 0.105)) for n in NAMES})
        out = go(r, fn)
        chk('④c 분모 = 50×50 평균 (0.1 vs 0.105 → −4.76 % · 40 분모였다면 −5 %)',
            abs(out['indicators']['sigma_ion']['delta'] - (-100 * 0.005 / 0.105)) < 1e-9)
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {n: dict(por=(10.5 if n in B40 else 10.0)) for n in NAMES})   # 10.5 − 10.0 = 0.5 (이진수로 정확)
        out = go(r, fn)
        pr = out['indicators']['porosity']
        chk('④d 경계 정확히 |Δ| = 문턱 0.5 → 통과 (≤ 문턱 = 통과 · 등록 §3)', pr['delta'] == 0.5 and pr['result'] == PASS, f'{pr}')
    # ⑤ 비관통 · 풀이 실패 → 판정 불가 (값 없음)
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {'kg50_d3_b50_s2': dict(sig=0.0, sig_status='valid_zero')}, tau={'c4': None})
        out = go(r, fn)
        chk('⑤ σ valid_zero (비관통) 한 침대 → σ_ion 판정 불가 · 사유 남김',
            out['indicators']['sigma_ion']['result'] == UNDECIDED
            and 'valid_zero' in out['cases']['kg50_d3_b50_s2']['notes']['sigma_ion'])
        chk('⑤b τ 상태 NOT_COMPUTED → 수송 tortuosity 판정 불가', out['indicators']['tau2']['result'] == UNDECIDED)
        chk('⑤c 다른 지표는 그대로 판정 (porosity 통과)', out['indicators']['porosity']['result'] == PASS)
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {'kg50_d3_b40_s2': dict(sig=0.1, sig_status='not_computed')})   # 상태 미달인데 옛 양수 값이 남은 꼴
        out = go(r, fn)
        chk('⑤d σ 상태 not_computed 인데 값 양수 → σ_ion 판정 불가 (값보다 상태가 먼저)',
            out['indicators']['sigma_ion']['result'] == UNDECIDED)
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {}, tau={'c1': (4.0, 'HOLD')})
        out = go(r, fn)
        chk('⑤e τ 상태 HOLD 인데 값 양수 → 수송 tortuosity 판정 불가', out['indicators']['tau2']['result'] == UNDECIDED)
    # ⑥ NaN · porosity ≠ spheresum → 그 지표 판정 불가
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {'kg50_d3_b40_s1': dict(cov=float('nan')), 'kg50_d3_b40_s2': dict(spheresum=11.0)})
        out = go(r, fn)
        chk('⑥ coverage (Hertz) NaN → 판정 불가', out['indicators']['coverage_hertz']['result'] == UNDECIDED)
        chk('⑥b porosity ≠ porosity_spheresum → porosity 판정 불가 (ε_sphere 아님)',
            out['indicators']['porosity']['result'] == UNDECIDED)
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {'kg50_d3_b50_s1': dict(cov=150.0)})
        out = go(r, fn)
        cc = out['cases']['kg50_d3_b50_s1']
        chk('⑥c coverage 150 % (범위 밖) → 그 값 빈칸 · 사유 · 판정 불가 (① — 산포 탓 ② 가 아니다)',
            cc['values']['coverage_hertz'] is None and '범위' in cc['notes'].get('coverage_hertz', '')
            and out['indicators']['coverage_hertz']['why'].startswith('①'))
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {'kg50_d3_b40_s2': dict(covp_status='blank: 시험')})
        out = go(r, fn)
        chk('⑥d Physics coverage 상태 blank → coverage Physics 판정 불가 · Hertz 는 그대로 통과',
            out['indicators']['coverage_physics']['result'] == UNDECIDED
            and out['indicators']['coverage_hertz']['result'] == PASS)
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {'kg50_d3_b50_s3': dict(covp=150.0)})
        out = go(r, fn)
        cc = out['cases']['kg50_d3_b50_s3']
        chk('⑥e Physics coverage 150 % → 그 값 빈칸 · 사유 (①)', cc['values']['coverage_physics'] is None
            and '범위' in cc['notes'].get('coverage_physics', ''))
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {n: dict(covp=(61.5 if n in B40 else 60.0)) for n in NAMES})
        out = go(r, fn)
        chk('⑥f Physics 만 1.5 %p 차 → coverage Physics 불합격 · 전체 불합격 (둘 다 판정)',
            out['indicators']['coverage_physics']['result'] == FAIL and out['overall'] == FAIL
            and out['indicators']['coverage_hertz']['result'] == PASS)
    # ⑦ 입력 거부 — 이름 없음 · 중복 · 판 다름 · AM 상 둘
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {})
        os.remove(os.path.join(r, 'uploads', 'c3', 'meta.json'))
        try:
            go(r, fn)
            chk('⑦ 이름 하나 없음 → 거부', False)
        except Refused as e:
            chk('⑦ 이름 하나 없음 → 거부', 'kg50_d3_b50_s1' in str(e), str(e))
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {})
        _mk(r, 'c9', 'kg50_d3_b40_s1')
        try:
            go(r, fn)
            chk('⑦b 같은 이름 둘 → 거부', False)
        except Refused as e:
            chk('⑦b 같은 이름 둘 → 거부 (id 지정 안내)', '--case' in str(e), str(e))
        out = go(r, fn, explicit={'kg50_d3_b40_s1': 'c0'})
        chk('⑦c --case 이름=id 로 지정하면 판정', out['cases']['kg50_d3_b40_s1']['case_id'] == 'c0')
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {'kg50_d3_b50_s3': dict(sha='other')})
        try:
            go(r, fn)
            chk('⑦d 망 코드 판 다름 → 거부', False)
        except Refused as e:
            chk('⑦d 망 코드 판 다름 → 거부', '판' in str(e), str(e))
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {'kg50_d3_b40_s3': dict(tm='1:AM_P,2:AM_S,3:SE')})
        try:
            go(r, fn)
            chk('⑦e AM 상 둘 → 거부', False)
        except Refused as e:
            chk('⑦e AM 상 둘 → 거부', 'AM 상' in str(e), str(e))
    with tempfile.TemporaryDirectory() as r:
        fn = _bed(r, {})
        os.remove(os.path.join(r, 'results', 'c5', 'network_provenance.json'))
        try:
            go(r, fn)
            chk('⑦f 필수 파일 없음 → 거부', False)
        except Refused as e:
            chk('⑦f 필수 파일 없음 → 거부', 'network_provenance.json' in str(e), str(e))
    # ⑧ 전체 조합 — 하나 불합격 + 하나 판정 불가 → 불합격
    rs = {'a': {'result': FAIL}, 'b': {'result': UNDECIDED}, 'c': {'result': PASS}}
    chk('⑧ 불합격 + 판정 불가 → 전체 불합격', overall(rs)[0] == FAIL)
    chk('⑧b 판정 불가 + 통과 → 전체 판정 불가', overall({'a': {'result': UNDECIDED}, 'b': {'result': PASS}})[0] == UNDECIDED)
    # ⑨ SE_Δ 식 = √(s40²/3 + s50²/3) · 표본 표준편차
    j = judge([1.0, 2.0, 3.0], [1.0, 1.0, 1.0], 'abs', 10.0)
    chk('⑨ SE_Δ = √(1/3) (s40 = 1 · s50 = 0)', abs(j['se'] - math.sqrt(1 / 3)) < 1e-12 and abs(j['delta'] - 1.0) < 1e-12)
    # ⑩ 값 두 개 · 네 개 → 판정 불가 (시드 3 고정)
    chk('⑩ 시드 수 ≠ 3 → 판정 불가', judge([1.0, 2.0], [1.0, 1.0, 1.0], 'abs', 1.0)['result'] == UNDECIDED)
    # ⑪ 실제 사슬 — 리포의 실제 웹앱 결과 폴더에서 tau_flux.case_row 가 tau2 를 낸다 (기본 함수 경로)
    fx = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'smoke_postfix', 'controls',
                      'c1_general_positive_1eol4bw_')
    if os.path.isdir(fx):
        e = extract(fx, {'type_map': '1:SE,2:AM_P'})
        chk('⑪ 실제 결과 폴더 → τ 상태 OK · tau2 양수 (기본 tau_flux.case_row)',
            _finite(e['values']['tau2']) and e['values']['tau2'] > 0, str(e['notes']))
        chk('⑪b 실제 결과 폴더 → σ_ion computed 양수 · 판 sha 읽힘',
            _finite(e['values']['sigma_ion']) and bool(e['code_sha']), str(e))
    else:
        chk('⑪ 실제 결과 폴더 고정물 있음', False, fx)
    print(f'kg50_d3_cell_verdict selftest: {"PASS" if ok_all else "FAIL"}')
    return 0 if ok_all else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='50kg D3 칸 판정 판독기 (읽기 전용 · 등록 README §3 · Hertz)')
    up, rs = _default_roots()
    ap.add_argument('--uploads-root', default=up, help='웹앱 uploads (meta.json 이름으로 케이스를 찾는다)')
    ap.add_argument('--results-root', default=rs, help='웹앱 results (케이스 id 폴더)')
    ap.add_argument('--case', action='append', default=[], help='이름=케이스 id (같은 이름이 여러 개일 때)')
    ap.add_argument('--json', default='', help='판정 기록 JSON 을 쓸 곳 (선택)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    explicit = {}
    for c in a.case:
        n, sep, cid = c.partition('=')
        if not sep or n not in NAMES or not cid:
            print(f'⛔ --case 형식 · 이름이 틀렸다: {c!r} (이름 = {", ".join(NAMES)})')
            return 2
        explicit[n] = cid
    try:
        out = run(a.uploads_root, a.results_root, explicit)
    except Refused as e:
        print(f'⛔ 입력 거부 — 판정 없음: {e}')
        return 2
    print(report(out))
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(f'\n판정 기록: {a.json}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
