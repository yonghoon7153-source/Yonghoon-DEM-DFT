#!/usr/bin/env python3
"""dissolution_energy.py — 녹아 들어가는 에너지 (cascade 1단계 구성 · UMA): 입력 받기 · 모으기 · 합치기.

왜 (2026-10-14 · 트랙 cascade · 1저자 = 사용자 · 사용자 *"한번 해보지 뭐"* · *"mp 받고 바로 돌릴 수 있도록 코드 짜자"*)
  1단계 de (원자당 에너지 − 호스트 원자당 에너지) 는 더해진 원소의 기준이 없어 조성에 오염된다 (8장 · element_effects 데모:
  구성 순위가 뺀 Li 수와 ρ 0.48). 같은 UMA 로 전구체 · 교환상 · 호스트를 재서 조성을 정확히 닫은 반응 에너지로 바꾼다:

      host + n·전구체 → 구성 + Σν·교환상 (Li₂S · LiCl · Li₃PS₄)
      ΔE = [E(구성) + Σν E(교환상) − E(host) − n E(전구체)] / (n · 전구체 한 단위의 기준 원소 수)      (eV / 기준 원자)

  기준 원소 = element_effects.key_element — 교환상에 없는 첫 원소 (양이온 먼저 · Li₂O 는 O · Li₂S·LiCl 은 Li).
  카드: db/properties/cascade_dissolution_energy_estimand_2026_10_14.json

하위 명령
  fetch    (gabia · mp_api) 화학식마다 MP 다형 후보를 고르고 (창 안 E_hull · 실험 관측 최저는 늘 포함) 구조 파일 · manifest ·
           tools/doping/run_uma_screening.py 입력 목록 (+ 호스트 comp1_V0_k444) 을 쓴다
  collect  (gabia) 1단계 원본 <런>/02_screen/uma_results.json 에서 구성별 총에너지와 그 런의 기준값 (baseline) 을 모은다
  combine  (어디서나 · numpy) 위 둘 + UMA 이완 결과 → 관문 · 구성별 · 전구체별 ΔE · Origin CSV · 그림 · element_effects 라벨

이완은 이 도구가 하지 않는다 — 1단계와 같은 코드 tools/doping/run_uma_screening.py (UMA-s-1p1 omat · FIRE · FrechetCellFilter ·
fmax 0.05 · steps 1500) 가 한다. 그 도구가 --base 로 canonical 호스트를 다시 이완해 1단계 기준값을 재현하는지가 대조 잡이다.

⛔ 이 도구가 못 하는 것
  · 형식전하가 0 이 아닌 구성 (1단계 생성기가 음이온 자리 · 받개 양이온 전하를 안 맞춘 것 · 감사 ②) 은 값이 없다 —
    교환상 셋으로 닫히지 않고, 닫으려면 Li 금속 같은 저장소의 화학 퍼텐셜을 골라야 해서 스칼라가 정해지지 않는다.
  · 1단계 구조의 결함 (canonical 기하 상속 · 감사 ①) 을 고치지 않는다 — 1단계 구성 에너지를 그대로 쓴다 → 값은 데모다.
  · 다형 선택은 '창 안 MP 후보 중 UMA 최저' 다 — 실험 상과 다를 수 있다 (표에 표지 · 예측 구조면 표지).
  · 농도 · 배치 엔트로피 · 온도 항이 없다 (0 K UMA 에너지).
  · UMA 의 화학 정확도를 검증하지 않는다 — DFT 가 아니다.

  python3 tools/cascade/dissolution_energy.py --selftest
  python3 tools/cascade/dissolution_energy.py fetch --out <dir>                      # gabia (MP_API_KEY · uma env)
  python3 tools/cascade/dissolution_energy.py collect --out <dir>/stage1_energies.json
  python3 tools/cascade/dissolution_energy.py combine --mp_dir <dir>/mp --uma <dir>/uma/uma_results.json \\
          --stage1 <dir>/stage1_energies.json --out <dir>/result
"""
import argparse
import csv
import glob
import json
import math
import os
import re
import sys
from datetime import datetime

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import element_effects as ee  # noqa: E402

RESERVOIR_FORMULAS = tuple(ee.RESERVOIRS)                      # Li2S · LiCl · Li3PS4
HOST_H2 = ('HOST__comp1_V0_k444', 'db/structures/comp1_V0_k444.cif')   # DFT k444 평형 Li24P4S20Cl4 (UMA 부피 +0.06 %)
HOST_H1_CIF = 'db/structures/lpscl_F43m_24G_canonical.cif'    # 1단계 baseline 의 출처 (md5 57e24e164d1b…)
STAGE1_ROOTS = ('/data/work/runs/multi_category_2026_05_26_v23', '/data/work/runs/as2s3_recover')
VALENCE = {'Li': 1, 'P': 5, 'S': -2, 'Cl': -1}
FIELDS = ['material_id', 'formula_pretty', 'energy_above_hull', 'theoretical', 'nsites', 'symmetry', 'deprecated', 'structure']


def formula_counts(f):
    out = {}
    for e, n in re.findall(r'([A-Z][a-z]?)(\d*)', f):
        out[e] = out.get(e, 0) + (int(n) if n else 1)
    return out


def prec_counts(f):
    return formula_counts(f)


# ---------------------------------------------------------------- fetch
def select_candidates(docs, window=0.03, max_n=4, max_sites=200):
    """MP 후보 고르기. docs = dict (material_id · energy_above_hull · theoretical · nsites · deprecated).
    ① deprecated 버림 ② E_hull ≤ window 를 E_hull 순으로 max_n 개 (nsites > max_sites 는 건너뜀) ③ 창 안이 없으면 최저 하나
    ④ 실험 관측 (theoretical False) 최저는 창 · 개수 · 크기와 상관없이 늘 넣는다. E_hull None 은 정렬 맨 뒤 (0.0 을 거짓으로 읽지 않는다)."""
    live = [d for d in docs if not d.get('deprecated')]
    key = lambda d: (math.inf if d.get('energy_above_hull') is None else d['energy_above_hull'], d['material_id'])
    live.sort(key=key)
    picked = []
    for d in live:
        eh = d.get('energy_above_hull')
        if eh is not None and eh <= window and len(picked) < max_n and (d.get('nsites') or 0) <= max_sites:
            picked.append((d, 'within_window'))
    if not picked and live:
        picked.append((live[0], 'lowest_overall'))
    obs = [d for d in live if d.get('theoretical') is False]
    if obs and all(p[0]['material_id'] != obs[0]['material_id'] for p in picked):
        picked.append((obs[0], 'lowest_observed'))
    return [dict(d, reason=r) for d, r in picked]


def _doc_dict(d):
    sym = getattr(d, 'symmetry', None)
    return {'material_id': str(d.material_id), 'formula_pretty': getattr(d, 'formula_pretty', None),
            'energy_above_hull': getattr(d, 'energy_above_hull', None), 'theoretical': getattr(d, 'theoretical', None),
            'nsites': getattr(d, 'nsites', None), 'deprecated': getattr(d, 'deprecated', False),
            'spacegroup': getattr(sym, 'symbol', None) if sym is not None else None}


def write_structure(structure, path_stub):
    """MP 구조 → <stub>.extxyz (이완 입력 · 셀 그대로) + <stub>.cif (사람 · VESTA)."""
    from pymatgen.io.ase import AseAtomsAdaptor
    from ase.io import write
    at = AseAtomsAdaptor.get_atoms(structure)
    write(path_stub + '.extxyz', at, format='extxyz')
    structure.to(filename=path_stub + '.cif')
    return path_stub + '.extxyz'


def precursors_from_master(path=ee.MASTER):
    return sorted({ee.base(r['dopant']) for r in ee.load_stage1(path)})


def eligible_precursors(path=ee.MASTER):
    """Precursors with ≥ 1 configuration that can get a value: formally neutral · not host composition · closes with the
    three reservoirs. The others (2026-10-14: AlN · Ca₃N₂ · GaN · Li₃N · Mg₃N₂ · NbCl₅ · TaCl₅ · Li₂S · LiCl) are not fetched."""
    configs, _ = config_rows(path)
    ok = set()
    for c in configs:
        try:
            if formal_charge(c['comp'], c['precursor']) != 0:
                continue
        except ValueError:
            continue
        if all(c['comp'].get(e, 0) == ee.HOST_CELL.get(e, 0) for e in set(c['comp']) | set(ee.HOST_CELL)):
            continue
        try:
            ee.balance(c['comp'], ee.HOST_CELL, prec_counts(c['precursor']))
            ok.add(c['precursor'])
        except ValueError:
            pass
    return sorted(ok)


def fetch(out, formulas, rester, window, max_n, max_sites, writer=write_structure, db_version=None):
    os.makedirs(os.path.join(out, 'structures'), exist_ok=True)
    man = {'what': 'MP 다형 후보 (dissolution_energy.py fetch)', 'date': datetime.now().strftime('%F %T'),
           'mp_database_version': db_version, 'window_eV_per_atom': window, 'max_per_formula': max_n, 'max_sites': max_sites,
           'formulas': {}, 'missing': [], 'errors': {}}
    summary = []
    for f in formulas:
        try:
            docs = [_doc_dict(d) | {'_obj': d} for d in rester.materials.summary.search(formula=f, fields=FIELDS)]
        except Exception as e:                               # 하나 실패해도 나머지는 받는다 — 빠진 것은 manifest 에 남는다
            man['errors'][f] = f'{type(e).__name__}: {e}'[:300]
            man['missing'].append(f)
            continue
        docs = [d for d in docs if d['formula_pretty'] in (None, f)]
        sel = select_candidates([{k: v for k, v in d.items() if k != '_obj'} for d in docs], window, max_n, max_sites)
        role = 'reservoir' if f in RESERVOIR_FORMULAS else 'precursor'
        man['formulas'][f] = {'role': role, 'n_docs': len(docs),
                              'docs': [{k: v for k, v in d.items() if k != '_obj'} for d in docs][:12], 'selected': []}
        if not sel:
            man['missing'].append(f)
            continue
        objs = {d['material_id']: d['_obj'] for d in docs}
        for s in sel:
            name = f"{f}__{s['material_id']}"
            path = writer(objs[s['material_id']].structure, os.path.join(out, 'structures', name))
            man['formulas'][f]['selected'].append({k: s[k] for k in ('material_id', 'energy_above_hull', 'theoretical',
                                                                         'nsites', 'spacegroup', 'reason')})
            summary.append({'name': name, 'xyz_file': os.path.relpath(path, ROOT) if path.startswith(ROOT) else path,
                            'formula': f, 'role': role, 'material_id': s['material_id'],
                            'e_above_hull_mp': s['energy_above_hull'], 'theoretical': s['theoretical'], 'reason': s['reason']})
    summary.append({'name': HOST_H2[0], 'xyz_file': HOST_H2[1], 'formula': 'Li24P4S20Cl4', 'role': 'host',
                    'material_id': None, 'reason': 'DFT k444 equilibrium host (comp1)'})
    with open(os.path.join(out, 'manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump(man, fh, indent=1, ensure_ascii=False, default=str)
    with open(os.path.join(out, 'structures_summary.json'), 'w', encoding='utf-8') as fh:
        json.dump({'structures': summary, 'baseline': {'note': 'H1 = run_uma_screening --base ' + HOST_H1_CIF}}, fh, indent=1)
    return man, summary


# ---------------------------------------------------------------- collect
def collect(roots, out):
    runs, recs = {}, []
    for root in roots:
        pats = [os.path.join(root, '*', '02_screen', n) for n in ('uma_results.json', 'uma_screening_results.json')]
        for f in sorted(set(sum((glob.glob(p) for p in pats), []))):
            run = f'{os.path.basename(root.rstrip("/"))}/{os.path.basename(os.path.dirname(os.path.dirname(f)))}'
            d = json.load(open(f, encoding='utf-8'))
            bl = d.get('baseline') or {}
            runs[run] = {**{k: bl.get(k) for k in ('e_per_atom', 'volume_per_atom', 'n_atoms', 'converged', 'source_base_md5',
                                                  'n_steps')}, 'file': f, 'n_results': len(d.get('results', [])),
                         'n_failed': d.get('n_failed'), 'cli_steps': (d.get('cli_args') or {}).get('steps'),
                         'cli_device': (d.get('cli_args') or {}).get('device')}
            for r in d.get('results', []):
                u = r.get('uma_relaxed') or {}
                recs.append({'run': run, 'name': r.get('name'), 'e_total': u.get('e_total'), 'n_atoms': u.get('n_atoms'),
                             'converged': r.get('converged'), 'baseline_e_per_atom': r.get('baseline_e_per_atom')})
    base = sorted({round(v['e_per_atom'], 9) for v in runs.values() if v.get('e_per_atom') is not None})
    res = {'what': '1단계 원본 구성 에너지 (dissolution_energy.py collect)', 'date': datetime.now().strftime('%F %T'),
           'roots': list(roots), 'n_runs': len(runs), 'n_records': len(recs), 'distinct_baseline_e_per_atom': base,
           'distinct_baseline_md5': sorted({str(v.get('source_base_md5')) for v in runs.values()}), 'runs': runs, 'records': recs}
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as fh:
        json.dump(res, fh, indent=0, ensure_ascii=False)
    return res


# ---------------------------------------------------------------- combine
def formal_charge(comp, prec):
    pi = ee.parse_precursor(prec)
    z = dict(VALENCE)
    if pi['cation'] != 'Li':
        z[pi['cation']] = pi['z_cat']
    z[pi['anion']] = -pi['z_an']
    miss = [e for e in comp if e not in z]
    if miss:
        raise ValueError(f'no formal valence for {miss}')
    return sum(z[e] * n for e, n in comp.items())


def phase_energies(uma, man):
    """Per formula: UMA energy per formula unit = min over converged candidates; polymorph flags against the MP ground candidate."""
    by = {}
    for r in uma.get('results', []):
        if r.get('role') not in ('precursor', 'reservoir'):
            continue
        u = r.get('uma_relaxed') or {}
        apf = sum(formula_counts(r['formula']).values())
        n = u.get('n_atoms')
        if not n or n % apf:
            raise ValueError(f"{r['name']}: {n} atoms is not a multiple of {apf}")
        by.setdefault(r['formula'], []).append({'material_id': r.get('material_id'), 'converged': bool(r.get('converged')),
                                                'E_fu': u['e_total'] * apf / n, 'e_above_hull_mp': r.get('e_above_hull_mp'),
                                                'theoretical': r.get('theoretical'), 'reason': r.get('reason')})
    out = {}
    for f, cands in by.items():
        ok = [c for c in cands if c['converged']]
        if not ok:
            out[f] = {'E_fu': None, 'candidates': cands, 'flag': 'no_converged_candidate'}
            continue
        best = min(ok, key=lambda c: c['E_fu'])
        eh = [c['e_above_hull_mp'] for c in cands if c['e_above_hull_mp'] is not None]
        ground = [c for c in ok if eh and c['e_above_hull_mp'] == min(eh)]
        flag = 'mp_ground' if best in ground else 'uma_prefers_other'
        out[f] = {'E_fu': best['E_fu'], 'material_id': best['material_id'], 'theoretical': best['theoretical'], 'flag': flag,
                  'uma_gain_vs_mp_ground_eV_per_fu': (min(c['E_fu'] for c in ground) - best['E_fu']) if ground else None,
                  'candidates': cands}
    for f in (man or {}).get('missing', []):
        out.setdefault(f, {'E_fu': None, 'candidates': [], 'flag': 'not_fetched'})
    return out


def config_rows(master):
    rep = {}
    rows = ee.load_stage1(master, rep)
    out = []
    for r in rows:
        comp = {k[12:]: int(round(float(r[k]))) for k in r if k.startswith('composition_') and r[k] not in ('', None)}
        comp = {e: n for e, n in comp.items() if n}
        out.append({'name': r['name'], 'family': r['family'], 'precursor': ee.base(r['dopant']), 'dopant': r['dopant'],
                    'comp': comp, 'de': float(r['screen_de_per_atom'])})
    return out, rep


def combine(configs, phases, uma, stage1, tol_baseline=5e-4, allow_mismatch=False):
    rep = {'gates': {}, 'counts': {}}
    bl = uma.get('baseline') or {}
    e_h1 = bl.get('e_per_atom')
    e_b = stage1.get('distinct_baseline_e_per_atom') or []
    md5_now = bl.get('source_base_md5')
    md5_s1 = [m for m in stage1.get('distinct_baseline_md5', []) if m not in (None, 'None')]
    worst = max((abs(e_h1 - v) for v in e_b), default=None) if e_h1 is not None else None
    ok_h1 = (e_h1 is not None and bool(e_b) and bl.get('converged', True) and worst <= tol_baseline
             and (not md5_s1 or all(m == md5_now for m in md5_s1)))
    rep['gates']['G1_baseline_reproduced'] = {'pass': bool(ok_h1), 'e_H1_now': e_h1, 'stage1_e_b': e_b, 'max_abs_diff': worst,
                                              'tol_eV_per_atom': tol_baseline, 'md5_now': md5_now, 'md5_stage1': md5_s1}
    if not ok_h1 and not allow_mismatch:
        raise RuntimeError(f'G1: canonical host does not reproduce the Stage-1 baseline (now {e_h1} · Stage-1 {e_b} · '
                           f'md5 {md5_now} vs {md5_s1}) — the Stage-1 configuration energies would not be on the same footing')
    h2 = [r for r in uma.get('results', []) if r.get('role') == 'host' and r.get('converged')]
    e_h2 = h2[0]['uma_relaxed']['e_total'] / h2[0]['uma_relaxed']['n_atoms'] if h2 else None
    hosts = {k: v for k, v in (('H1_canonical', e_h1), ('H2_comp1_k444', e_h2)) if v is not None}
    host_used = min(hosts, key=hosts.get)
    rep['hosts_eV_per_atom'] = hosts
    rep['host_used'] = host_used
    miss_res = [f for f in RESERVOIR_FORMULAS if (phases.get(f) or {}).get('E_fu') is None]
    rep['gates']['G2_reservoirs'] = {'pass': not miss_res, 'missing': miss_res}
    if miss_res:
        raise RuntimeError(f'G2: reservoir energies missing for {miss_res}')
    # Stage-1 configuration energies: raw e_total of the record in the row's own family; CSV de cross-check
    recs = {}
    for r in stage1.get('records', []):
        recs.setdefault((r['run'].split('/')[0], r['name']), r)
    nh = sum(ee.HOST_CELL.values())
    out, mism = [], []
    for c in configs:
        row = {'name': c['name'], 'slot': ee.slot(c['name']), 'precursor': c['precursor'], 'family': c['family'],
               'stage1_de_eV_per_atom': c['de']}
        try:
            q = formal_charge(c['comp'], c['precursor'])
        except ValueError as e:
            out.append(row | {'status': 'no_valence', 'note': str(e)})
            continue
        row['formal_charge'] = q
        if q != 0:
            out.append(row | {'status': 'non_neutral'})
            continue
        r = recs.get((c['family'], c['name']))
        N = sum(c['comp'].values())
        if all(c['comp'].get(e, 0) == ee.HOST_CELL.get(e, 0) for e in set(c['comp']) | set(ee.HOST_CELL)):
            # Li₂S · LiCl 'null 대조' — 호스트와 같은 조성 (배치만 다름): 녹는 에너지는 없고 재배치 에너지만 있다
            if r and r.get('e_total') is not None:
                out.append(row | {'status': 'null_control', 'energy_source': 'stage1_raw', 'E_config_eV': r['e_total'],
                                  **{f'rearrangement_eV_per_atom_{h}': r['e_total'] / N - e for h, e in hosts.items()}})
            else:
                out.append(row | {'status': 'null_control'})
            continue
        try:
            n, nu = ee.balance(c['comp'], ee.HOST_CELL, prec_counts(c['precursor']))
        except ValueError as e:
            out.append(row | {'status': 'unbalanced', 'note': str(e)[:120]})
            continue
        if r and r.get('e_total') is not None:
            e_conf, src = r['e_total'], 'stage1_raw'
            if r.get('baseline_e_per_atom') is not None:
                mism.append(abs(N * (c['de'] + r['baseline_e_per_atom']) - e_conf) / N)
            if r.get('n_atoms') not in (None, N):
                out.append(row | {'status': 'atom_count_mismatch'})
                continue
        elif len(e_b) == 1:
            e_conf, src = N * (c['de'] + e_b[0]), 'csv_de_plus_unique_baseline'
        else:
            out.append(row | {'status': 'no_energy'})
            continue
        ph = phases.get(c['precursor']) or {}
        if ph.get('E_fu') is None:
            out.append(row | {'status': 'missing_phase', 'note': ph.get('flag', 'not_fetched')})
            continue
        k = ee.key_element(prec_counts(c['precursor']))
        nk = n * prec_counts(c['precursor'])[k]
        res_sum = sum(v * phases[f]['E_fu'] for f, v in nu.items())
        de_by = {h: (e_conf + res_sum - nh * e - n * ph['E_fu']) for h, e in hosts.items()}
        out.append(row | {'status': 'ok', 'energy_source': src, 'n_units': n, 'key_element': k, 'n_key_atoms': nk,
                          **{f'nu_{f}': nu[f] for f in RESERVOIR_FORMULAS}, 'E_config_eV': e_conf,
                          'dE_per_key_atom_eV': de_by[host_used] / nk,
                          **{f'dE_per_key_atom_eV_{h}': v / nk for h, v in de_by.items()}})
    rep['gates']['G3_csv_vs_raw_eV_per_atom_max'] = max(mism) if mism else None
    nulls = [r for r in out if r['status'] == 'null_control' and 'E_config_eV' in r]
    rep['null_controls'] = {h: {'n': len(nulls), 'min': min(r[f'rearrangement_eV_per_atom_{h}'] for r in nulls),
                                'median': float(np.median([r[f'rearrangement_eV_per_atom_{h}'] for r in nulls]))}
                            for h in hosts} if nulls else None
    from collections import Counter
    rep['counts'] = dict(Counter(r['status'] for r in out))
    return out, rep


U_TM = ('Co', 'Cr', 'Fe', 'Mn', 'Mo', 'Ni', 'V', 'W')   # MP/OMat24 put +U on oxides · fluorides of these


def u_risk(prec):
    """True when the precursor is an oxide or fluoride of a +U metal: its training labels are PBE+U, the S/Cl host and the
    reservoirs are plain PBE — the reaction can mix the two (MP2020 needs a correction for exactly this)."""
    pi = ee.parse_precursor(prec)
    return pi['cation'] in U_TM and pi['anion'] in ('O', 'F')


def by_precursor(rows, phases):
    """Per precursor: each slot (x020 · x050 · x100 copies of one composition · element_effects.slot) gets the MEDIAN of its
    eligible copies — one copy that relaxed somewhere odd cannot become the minimum (2026-10-14: copies differ by up to
    0.46 eV/atom ≈ 24 eV per key atom) — then min over slots (1st) · median over slots · gap · copy spread of the argmin slot."""
    groups = {}
    for r in rows:
        groups.setdefault(r['precursor'], []).append(r)
    out = []
    for p in sorted(groups):
        g = groups[p]
        ok = [r for r in g if r['status'] == 'ok']
        slots = {}
        for r in ok:
            slots.setdefault(ee.slot(r['name']), []).append(r['dE_per_key_atom_eV'])
        sv = sorted((float(np.median(v)), k, v) for k, v in slots.items())
        ph = phases.get(p) or {}
        rec = {'precursor': p, 'anion_family': ee.parse_precursor(p)['anion'], 'n_total': len(g), 'n_eligible': len(ok),
               'n_eligible_slots': len(sv), 'key_element': ok[0]['key_element'] if ok else ee.key_element(prec_counts(p)),
               'precursor_mp_id_used': ph.get('material_id'), 'precursor_polymorph_flag': ph.get('flag'),
               'precursor_theoretical': ph.get('theoretical'), 'tm_u_risk': u_risk(p),
               'stage1_de_min_eligible_eV_per_atom': min((r['stage1_de_eV_per_atom'] for r in ok), default=None),
               'stage1_de_min_all_eV_per_atom': min(r['stage1_de_eV_per_atom'] for r in g)}
        if sv:
            v = [x[0] for x in sv]
            rec.update(dE_min_per_key_atom_eV=v[0], dE_median_per_key_atom_eV=float(np.median(v)),
                       gap_second_minus_min_eV=(v[1] - v[0]) if len(v) > 1 else None, argmin_slot=sv[0][1],
                       argmin_copy_spread_eV=(max(sv[0][2]) - min(sv[0][2])) if len(sv[0][2]) > 1 else None)
        else:
            rec.update(dE_min_per_key_atom_eV=None, dE_median_per_key_atom_eV=None, gap_second_minus_min_eV=None,
                       argmin_slot=None, argmin_copy_spread_eV=None, why_no_value=sorted({r['status'] for r in g}))
        out.append(rec)
    return out


def _cell(v):
    if v is None:
        return ''
    if isinstance(v, float):
        return f'{v:.6g}'
    if isinstance(v, (list, tuple)):
        return ' '.join(map(str, v))
    return str(v)


def write_rows(path, header, rows, cols):
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        for h in header:
            fh.write('# ' + h + '\n')
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow([_cell(r.get(c)) for c in cols])


def figure(prec_rows, out, note):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    sys.path.insert(0, ROOT)
    from tools.figures.house_style import INK, MUT, ELEM, apply_axes
    col = {'O': ELEM.get('O', '#be123c'), 'S': ELEM.get('S', '#c05621'), 'Cl': ELEM.get('Cl', '#65a30d'),
           'F': '#0891b2', 'Br': '#92400e', 'I': '#6d28d9', 'N': '#1d4ed8'}
    pts = [r for r in prec_rows if r['dE_min_per_key_atom_eV'] is not None and r['stage1_de_min_eligible_eV_per_atom'] is not None]
    fig, ax = plt.subplots(figsize=(3.6, 3.3))
    for fam in ('O', 'F', 'N', 'Cl', 'S', 'Br', 'I'):
        s = [r for r in pts if r['anion_family'] == fam]
        if s:
            ax.scatter([r['stage1_de_min_eligible_eV_per_atom'] for r in s], [r['dE_min_per_key_atom_eV'] for r in s],
                       s=16, color=col[fam], edgecolor=INK, linewidth=0.3, label=fam)
    rho = ee.spearman([r['stage1_de_min_eligible_eV_per_atom'] for r in pts], [r['dE_min_per_key_atom_eV'] for r in pts]) \
        if len(pts) > 2 else float('nan')
    apply_axes(ax, xlabel='Stage-1 energy per atom vs host (eV/atom)', ylabel='dissolution energy (eV per key atom)',
               fontsize=8.5)
    ax.tick_params(labelsize=8)
    ax.axhline(0, color=MUT, lw=0.7)
    ax.text(0.03, 0.97, f'n = {len(pts)} · Spearman {rho:.2f}', transform=ax.transAxes, va='top', fontsize=7.5, color=MUT)
    ax.legend(fontsize=6.5, frameon=False, ncol=2, loc='lower right')
    ax.set_title(note, fontsize=7.5, color=MUT)
    fig.tight_layout()
    p = os.path.join(out, 'dissolution_vs_stage1_de.png')
    fig.savefig(p, dpi=300)
    plt.close(fig)
    return p, rho


DEMO_NOTE = ('DEMO (2026-10-14): Stage-1 configuration energies are used as they are — they inherit the Stage-1 structure '
             'flaws (canonical-geometry start · audit 1). UMA, not DFT. Not citable.')
CFG_COLS = ['name', 'slot', 'precursor', 'family', 'status', 'formal_charge', 'n_units', 'key_element', 'n_key_atoms', 'nu_Li2S',
            'nu_LiCl', 'nu_Li3PS4', 'energy_source', 'E_config_eV', 'dE_per_key_atom_eV', 'dE_per_key_atom_eV_H1_canonical',
            'dE_per_key_atom_eV_H2_comp1_k444', 'rearrangement_eV_per_atom_H1_canonical', 'rearrangement_eV_per_atom_H2_comp1_k444',
            'stage1_de_eV_per_atom', 'note']
PREC_COLS = ['precursor', 'anion_family', 'key_element', 'n_total', 'n_eligible', 'n_eligible_slots', 'dE_min_per_key_atom_eV',
             'dE_median_per_key_atom_eV', 'gap_second_minus_min_eV', 'argmin_slot', 'argmin_copy_spread_eV', 'precursor_mp_id_used',
             'precursor_polymorph_flag', 'precursor_theoretical', 'tm_u_risk', 'stage1_de_min_eligible_eV_per_atom',
             'stage1_de_min_all_eV_per_atom', 'why_no_value']


def run_combine(a):
    man = json.load(open(os.path.join(a.mp_dir, 'manifest.json'), encoding='utf-8'))
    uma = json.load(open(a.uma, encoding='utf-8'))
    stage1 = json.load(open(a.stage1, encoding='utf-8'))
    configs, dedupe = config_rows(a.csv)
    phases = phase_energies(uma, man)
    rows, rep = combine(configs, phases, uma, stage1, a.tol_baseline, a.allow_baseline_mismatch)
    prec = by_precursor(rows, phases)
    os.makedirs(a.out, exist_ok=True)
    hdr = [DEMO_NOTE, 'dE = [E(config) + sum nu E(reservoir) - E(host) - n E(precursor)] / (n * key atoms per unit) · '
           'lower = more favourable · host = ' + rep['host_used']]
    write_rows(os.path.join(a.out, 'dissolution_configs.csv'), hdr, rows, CFG_COLS)
    write_rows(os.path.join(a.out, 'dissolution_by_precursor.csv'), hdr + ['min over eligible (formally neutral, '
               'balanced) configurations · Origin-ready'], prec, PREC_COLS)
    with open(os.path.join(a.out, 'label_dissolution_min_per_key_atom.csv'), 'w', encoding='utf-8', newline='') as fh:
        fh.write('# ' + DEMO_NOTE + '\n')
        w = csv.writer(fh)
        w.writerow(['precursor', 'value'])
        w.writerows([[r['precursor'], f"{r['dE_min_per_key_atom_eV']:.6g}"] for r in prec if r['dE_min_per_key_atom_eV'] is not None])
    fig, rho = figure(prec, a.out, 'DEMO · UMA · not citable')
    mm = [(r['dE_min_per_key_atom_eV'], r['dE_median_per_key_atom_eV']) for r in prec if r['dE_min_per_key_atom_eV'] is not None]
    rep['gates']['G6_spearman_min_vs_median'] = ee.spearman(*zip(*mm)) if len(mm) > 2 else None
    cs = [r['argmin_copy_spread_eV'] for r in prec if r.get('argmin_copy_spread_eV') is not None]
    rep['gates']['G8_argmin_copy_spread'] = {'n_over_0p05_eV': sum(1 for c in cs if c > 0.05), 'max': max(cs) if cs else None}
    rep.update(note=DEMO_NOTE, dropped_duplicates=dedupe.get('dropped_duplicates'), spearman_vs_stage1_de=rho,
               n_precursors_with_value=sum(1 for r in prec if r['dE_min_per_key_atom_eV'] is not None),
               phases={f: {k: v for k, v in p.items() if k != 'candidates'} | {'n_candidates': len(p.get('candidates', []))}
                       for f, p in phases.items()}, figure=os.path.basename(fig))
    with open(os.path.join(a.out, 'combine_report.json'), 'w', encoding='utf-8') as fh:
        json.dump(rep, fh, indent=1, ensure_ascii=False, default=str)
    g = rep['gates']
    print(f"G1 baseline reproduced: {g['G1_baseline_reproduced']['pass']} (max |Δ| {g['G1_baseline_reproduced']['max_abs_diff']})"
          f" · G2 reservoirs: {g['G2_reservoirs']['pass']} · CSV vs raw max {g['G3_csv_vs_raw_eV_per_atom_max']}")
    print(f"host used {rep['host_used']} {rep['hosts_eV_per_atom']} · configs {rep['counts']}")
    print(f"precursors with a value {rep['n_precursors_with_value']}/{len(prec)} · Spearman vs Stage-1 de {rho:.2f} · "
          f"min vs median {g['G6_spearman_min_vs_median']} · argmin copy spread > 0.05 eV: {g['G8_argmin_copy_spread']}")
    return 0


# ---------------------------------------------------------------- selftest
def _selftest():
    import tempfile
    from types import SimpleNamespace as NS
    ok = []

    def chk(c, m):
        ok.append(bool(c))
        print(('  ✓ ' if c else '  ✗ ') + m)
    D = lambda mid, eh, th, ns=10, dep=False: {'material_id': mid, 'energy_above_hull': eh, 'theoretical': th, 'nsites': ns,
                                               'deprecated': dep}
    sel = select_candidates([D('mp-2', 0.0, True, 12), D('mp-1', 0.0, False), D('mp-3', 0.02, True, 8), D('mp-4', 0.05, False, 6),
                             D('mp-5', None, False, 5), D('mp-6', 0.01, False, 400), D('mp-7', 0.0, False, 4, True)])
    chk([s['material_id'] for s in sel] == ['mp-1', 'mp-2', 'mp-3'], 'window 0.03 · E_hull 0.0 kept (not read as false) · '
        'too-big and deprecated skipped')
    sel = select_candidates([D('mp-1', 0.0, True), D('mp-4', 0.05, False)])
    chk([(s['material_id'], s['reason']) for s in sel] == [('mp-1', 'within_window'), ('mp-4', 'lowest_observed')],
        'the lowest observed polymorph is always added (LiCl rock salt lesson)')
    sel = select_candidates([D('mp-9', 0.2, True), D('mp-8', None, True)])
    chk([(s['material_id'], s['reason']) for s in sel] == [('mp-9', 'lowest_overall')], 'nothing in the window → lowest one only')
    # fetch with a fake MP client and writer
    with tempfile.TemporaryDirectory() as td:
        class Fake:
            class materials:
                class summary:
                    @staticmethod
                    def search(formula, fields):
                        if formula == 'XxO':
                            raise RuntimeError('MP down')
                        return [NS(material_id='mp-1', formula_pretty=formula, energy_above_hull=0.0, theoretical=False,
                                   nsites=5, symmetry=NS(symbol='Pm-3m'), deprecated=False, structure='S'),
                                NS(material_id='mp-2', formula_pretty=formula + 'x', energy_above_hull=0.0, theoretical=False,
                                   nsites=5, symmetry=NS(symbol='P1'), deprecated=False, structure='S')]
        written = []
        man, summ = fetch(td, ['Al2O3', 'XxO', 'LiCl'], Fake, 0.03, 4, 200,
                          writer=lambda st, stub: written.append(stub) or stub + '.extxyz', db_version='test')
        chk(man['missing'] == ['XxO'] and 'MP down' in man['errors']['XxO'] and len(written) == 2
            and [s['role'] for s in summ] == ['precursor', 'reservoir', 'host'] and summ[-1]['name'] == HOST_H2[0],
            'fetch: one failure is recorded, others written, other-formula docs dropped, host appended')
    # collect from fake run folders
    with tempfile.TemporaryDirectory() as td:
        for root, cmp, md5, eb in (('v23', 'Al2O3_x020', 'aaa', -4.0), ('v23', 'MgO_x020', 'aaa', -4.0), ('rec', 'AlI3_x020', 'aaa', -4.0)):
            p = os.path.join(td, root, cmp, '02_screen')
            os.makedirs(p)
            json.dump({'baseline': {'e_per_atom': eb, 'source_base_md5': md5, 'converged': True}, 'cli_args': {'steps': 1500},
                       'results': [{'name': f'{cmp}_s00', 'converged': True, 'baseline_e_per_atom': eb,
                                    'uma_relaxed': {'e_total': -200.0, 'n_atoms': 50}}]},
                      open(os.path.join(p, 'uma_results.json'), 'w'))
        res = collect([os.path.join(td, 'v23'), os.path.join(td, 'rec')], os.path.join(td, 's1.json'))
        chk(res['n_runs'] == 3 and res['n_records'] == 3 and res['distinct_baseline_e_per_atom'] == [-4.0]
            and {r['run'] for r in res['records']} == {'v23/Al2O3_x020', 'v23/MgO_x020', 'rec/AlI3_x020'},
            'collect: runs, records and the one baseline found')
    # combine: planted energies are recovered; gates refuse what they should
    e_h, e_h2 = -4.0, -4.01
    E = {'Li2S': -12.0, 'LiCl': -7.0, 'Li3PS4': -35.0}
    cfg_al = {'Li': 18, 'Al': 2, 'O': 3, 'Cl': 4, 'P': 4, 'S': 17}            # host + Al2O3 → config + 3 Li2S
    cfg_li2o = {'Li': 24, 'O': 1, 'Cl': 4, 'P': 4, 'S': 19}                    # host + Li2O → config + Li2S
    cfg_bad = {'Li': 21, 'Al': 1, 'Cl': 7, 'P': 4, 'S': 17}                    # AlCl3 Cl on S sites, uncompensated (+3)
    plant_al, plant_li = -0.40, 0.15                                            # eV per key atom (Al · O), host H2
    E_al2o3, E_li2o = -30.5, -14.0
    e_conf_al = 52 * e_h2 + E_al2o3 - 3 * E['Li2S'] + 2 * plant_al
    e_conf_li = 52 * e_h2 + E_li2o - E['Li2S'] + plant_li
    e_conf_al2 = e_conf_al + 2 * 0.50                                          # second Al2O3 slot, 0.50 eV/Al higher
    e_conf_al0c = e_conf_al + 2 * 0.20                                         # x-label copy of s0 that relaxed 0.20 eV/Al higher
    configs = [{'name': 'Al2O3_x020_s0', 'family': 'v23', 'precursor': 'Al2O3', 'comp': cfg_al, 'de': e_conf_al / 48 - e_h},
               {'name': 'Al2O3_x020_s1', 'family': 'v23', 'precursor': 'Al2O3', 'comp': cfg_al, 'de': e_conf_al2 / 48 - e_h},
               {'name': 'Al2O3_x050_s0', 'family': 'v23', 'precursor': 'Al2O3', 'comp': cfg_al, 'de': e_conf_al0c / 48 - e_h},
               {'name': 'Li2O_s0', 'family': 'v23', 'precursor': 'Li2O', 'comp': cfg_li2o, 'de': e_conf_li / 52 - e_h},
               {'name': 'AlCl3_s0', 'family': 'v23', 'precursor': 'AlCl3', 'comp': cfg_bad, 'de': -0.3},
               {'name': 'MgO_s0', 'family': 'v23', 'precursor': 'MgO', 'comp': {'Li': 22, 'Mg': 1, 'O': 1, 'Cl': 4, 'P': 4, 'S': 19},
                'de': -0.2},
               {'name': 'Li2S_s0', 'family': 'v23', 'precursor': 'Li2S', 'comp': dict(ee.HOST_CELL), 'de': 0.002}]
    res_ = lambda f, mid, e, conv=True, eh=0.0, th=False: {'name': f'{f}__{mid}', 'formula': f, 'role': 'reservoir'
                                                          if f in E else 'precursor', 'material_id': mid, 'converged': conv,
                                                          'e_above_hull_mp': eh, 'theoretical': th,
                                                          'uma_relaxed': {'e_total': e * 2, 'n_atoms': 2 * sum(formula_counts(f).values())}}
    uma = {'baseline': {'e_per_atom': e_h + 1e-5, 'converged': True, 'source_base_md5': 'aaa'},
           'results': [res_('Li2S', 'mp-1153', E['Li2S']), res_('LiCl', 'mp-22905', E['LiCl']), res_('Li3PS4', 'mp-985583', E['Li3PS4']),
                       res_('Al2O3', 'mp-1143', -30.0), res_('Al2O3', 'mp-x', E_al2o3, th=True, eh=0.02),
                       res_('Al2O3', 'mp-y', -31.0, conv=False), res_('Li2O', 'mp-1960', E_li2o),
                       {'name': HOST_H2[0], 'role': 'host', 'converged': True, 'uma_relaxed': {'e_total': 52 * e_h2, 'n_atoms': 52}}]}
    stage1 = {'distinct_baseline_e_per_atom': [e_h], 'distinct_baseline_md5': ['aaa'],
              'records': [{'run': 'v23/Al2O3_x', 'name': 'Al2O3_x020_s0', 'e_total': e_conf_al, 'n_atoms': 48, 'baseline_e_per_atom': e_h},
                          {'run': 'v23/Al2O3_x', 'name': 'Al2O3_x020_s1', 'e_total': e_conf_al2, 'n_atoms': 48, 'baseline_e_per_atom': e_h},
                          {'run': 'v23/Al2O3_x', 'name': 'Al2O3_x050_s0', 'e_total': e_conf_al0c, 'n_atoms': 48, 'baseline_e_per_atom': e_h},
                          {'run': 'v23/Li2O_x', 'name': 'Li2O_s0', 'e_total': e_conf_li, 'n_atoms': 52, 'baseline_e_per_atom': e_h},
                          {'run': 'v23/Li2S_x', 'name': 'Li2S_s0', 'e_total': 52 * (e_h + 0.002), 'n_atoms': 52, 'baseline_e_per_atom': e_h}]}
    ph = phase_energies(uma, {'missing': ['MgO']})
    chk(ph['Al2O3']['material_id'] == 'mp-x' and ph['Al2O3']['flag'] == 'uma_prefers_other'
        and abs(ph['Al2O3']['uma_gain_vs_mp_ground_eV_per_fu'] - 0.5) < 1e-9 and ph['MgO']['flag'] == 'not_fetched',
        'phase: UMA minimum over converged candidates (unconverged lower one ignored) · polymorph flag · missing kept as missing')
    rows, rep = combine(configs, ph, uma, stage1)
    got = {r['name']: r for r in rows}
    chk(abs(got['Al2O3_x020_s0']['dE_per_key_atom_eV'] - plant_al) < 1e-9 and abs(got['Li2O_s0']['dE_per_key_atom_eV'] - plant_li) < 1e-9
        and got['Li2O_s0']['key_element'] == 'O' and rep['host_used'] == 'H2_comp1_k444',
        'planted dissolution energies recovered per key atom (Al · O) with the lower host')
    chk(abs(got['Al2O3_x020_s0']['dE_per_key_atom_eV_H1_canonical'] - (plant_al + 52 * (e_h2 - e_h - 1e-5) / 2)) < 1e-9,
        'the H1 column differs by exactly the host energy difference')
    chk(got['AlCl3_s0']['status'] == 'non_neutral' and got['AlCl3_s0']['formal_charge'] == 3 and 'dE_per_key_atom_eV' not in got['AlCl3_s0']
        and got['MgO_s0']['status'] == 'missing_phase', 'non-neutral and missing-phase configurations get no value (never 0)')
    chk(rep['gates']['G3_csv_vs_raw_eV_per_atom_max'] < 1e-9, 'CSV de and raw energies agree')
    chk(got['Li2S_s0']['status'] == 'null_control' and abs(got['Li2S_s0']['rearrangement_eV_per_atom_H2_comp1_k444']
                                                          - (e_h + 0.002 - e_h2)) < 1e-9 and 'dE_per_key_atom_eV' not in got['Li2S_s0'],
        'host-composition (null control) configuration: no dissolution value, rearrangement energy vs each host')
    bad = dict(uma, baseline={'e_per_atom': e_h + 0.01, 'converged': True, 'source_base_md5': 'aaa'})
    try:
        combine(configs, ph, bad, stage1)
        chk(False, 'G1 refuses a host that does not reproduce the Stage-1 baseline')
    except RuntimeError:
        chk(True, 'G1 refuses a host that does not reproduce the Stage-1 baseline')
    bad = dict(uma, baseline={'e_per_atom': e_h, 'converged': True, 'source_base_md5': 'bbb'})
    try:
        combine(configs, ph, bad, stage1)
        chk(False, 'G1 refuses a different base file (md5)')
    except RuntimeError:
        chk(True, 'G1 refuses a different base file (md5)')
    ph2 = phase_energies(dict(uma, results=[r for r in uma['results'] if r.get('formula') != 'LiCl']), {})
    try:
        combine(configs, ph2, uma, stage1)
        chk(False, 'G2 refuses a missing reservoir')
    except RuntimeError:
        chk(True, 'G2 refuses a missing reservoir')
    prec = by_precursor(rows, ph)
    pp = {r['precursor']: r for r in prec}
    chk(u_risk('Fe2O3') and u_risk('NiO') and u_risk('MoO3') and not u_risk('FeCl3') and not u_risk('Al2O3') and not pp['Al2O3']['tm_u_risk'],
        '+U mixing flag: oxides/fluorides of Co Cr Fe Mn Mo Ni V W only')
    chk(pp['AlCl3']['dE_min_per_key_atom_eV'] is None and pp['AlCl3']['why_no_value'] == ['non_neutral']
        and abs(pp['Al2O3']['dE_min_per_key_atom_eV'] - (plant_al + 0.10)) < 1e-9 and pp['Al2O3']['argmin_slot'] == 'Al2O3_s0'
        and abs(pp['Al2O3']['gap_second_minus_min_eV'] - 0.40) < 1e-9 and abs(pp['Al2O3']['dE_median_per_key_atom_eV'] - (plant_al + 0.30)) < 1e-9
        and abs(pp['Al2O3']['argmin_copy_spread_eV'] - 0.20) < 1e-9 and pp['Al2O3']['n_eligible_slots'] == 2,
        'by precursor: slot median of copies → min over slots (gap · median · copy spread of the argmin slot) · reason when none')
    # end to end through the files (the path the runner takes)
    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, 'mp'))
        json.dump({'missing': ['MgO']}, open(os.path.join(td, 'mp', 'manifest.json'), 'w'))
        json.dump(uma, open(os.path.join(td, 'uma.json'), 'w'))
        json.dump(stage1, open(os.path.join(td, 's1.json'), 'w'))
        master = os.path.join(td, 'master.csv')
        els = ['Li', 'Al', 'O', 'Cl', 'P', 'S', 'Mg']
        with open(master, 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(['name', 'family', 'dopant', 'screen_de_per_atom'] + [f'composition_{e}' for e in els])
            for c in configs:
                w.writerow([c['name'], ee.MAIN_FAMILIES[0], c['precursor'], repr(c['de'])] + [c['comp'].get(e, '') for e in els])
        for r in stage1['records']:
            r['run'] = ee.MAIN_FAMILIES[0] + '/' + r['run'].split('/')[1]
        json.dump(stage1, open(os.path.join(td, 's1.json'), 'w'))
        a = NS(mp_dir=os.path.join(td, 'mp'), uma=os.path.join(td, 'uma.json'), stage1=os.path.join(td, 's1.json'), csv=master,
               out=os.path.join(td, 'res'), tol_baseline=5e-4, allow_baseline_mismatch=False)
        chk(eligible_precursors(master) == ['Al2O3', 'Li2O', 'MgO'],
            'eligible precursors: non-neutral (AlCl3) and host-composition (Li2S) ones are not fetched')
        rc = run_combine(a)
        lab = [l for l in open(os.path.join(td, 'res', 'label_dissolution_min_per_key_atom.csv'), encoding='utf-8') if not l.startswith('#')]
        bp = list(csv.DictReader(l for l in open(os.path.join(td, 'res', 'dissolution_by_precursor.csv'), encoding='utf-8')
                                 if not l.startswith('#')))
        chk(rc == 0 and lab[0].strip() == 'precursor,value' and len(lab) == 3
            and {r['precursor']: r['dE_min_per_key_atom_eV'] for r in bp}['AlCl3'] == ''
            and abs(float({r['precursor']: r['dE_min_per_key_atom_eV'] for r in bp}['Al2O3']) - (plant_al + 0.10)) < 1e-5,
            'files: label CSV has the two eligible precursors · blank (not 0) for the non-neutral one')
    print(f'selftest: {sum(ok)}/{len(ok)}')
    return 0 if all(ok) else 1


def main():
    if '--selftest' in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    f = sub.add_parser('fetch')
    f.add_argument('--out', required=True)
    f.add_argument('--csv', default=ee.MASTER)
    f.add_argument('--window', type=float, default=0.03)
    f.add_argument('--max_per_formula', type=int, default=4)
    f.add_argument('--max_sites', type=int, default=200)
    f.add_argument('--only', nargs='*', help='화학식 일부만 (시험용)')
    c = sub.add_parser('collect')
    c.add_argument('--roots', nargs='*', default=list(STAGE1_ROOTS))
    c.add_argument('--out', required=True)
    m = sub.add_parser('combine')
    m.add_argument('--mp_dir', required=True)
    m.add_argument('--uma', required=True)
    m.add_argument('--stage1', required=True)
    m.add_argument('--csv', default=ee.MASTER)
    m.add_argument('--out', required=True)
    m.add_argument('--tol_baseline', type=float, default=5e-4)
    m.add_argument('--allow_baseline_mismatch', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'fetch':
        key = os.environ.get('MP_API_KEY') or os.environ.get('PMG_MAPI_KEY')
        if not key:
            sys.exit('⛔ MP_API_KEY 가 없다 (⚠ 파일에 넣지 말 것)')
        from mp_api.client import MPRester
        elig = eligible_precursors(a.csv)
        skipped = sorted(set(precursors_from_master(a.csv)) - set(elig))
        forms = a.only or sorted(set(elig) | set(RESERVOIR_FORMULAS))
        print(f'precursors with an eligible configuration {len(elig)} · not fetched (no value possible) {skipped}')
        with MPRester(key) as r:
            try:
                dbv = r.get_database_version()
            except Exception:
                dbv = None
            man, summ = fetch(a.out, forms, r, a.window, a.max_per_formula, a.max_sites, db_version=dbv)
        n_sel = sum(len(v['selected']) for v in man['formulas'].values())
        print(f"MP {dbv} · formulas {len(forms)} · structures {n_sel} · missing {man['missing']}")
        return 0 if all(f not in man['missing'] for f in RESERVOIR_FORMULAS) else 6
    if a.cmd == 'collect':
        res = collect(a.roots, a.out)
        bl = res['distinct_baseline_e_per_atom']
        print(f"runs {res['n_runs']} · records {res['n_records']} · baselines {len(bl)} distinct "
              f"({min(bl, default=None)} … {max(bl, default=None)}) · md5 {res['distinct_baseline_md5']}")
        return 0 if res['n_records'] else 7
    if a.cmd == 'combine':
        try:
            return run_combine(a)
        except RuntimeError as e:
            print(f'⛔ {e}')
            return 3
    return 1


if __name__ == '__main__':
    sys.exit(main())
