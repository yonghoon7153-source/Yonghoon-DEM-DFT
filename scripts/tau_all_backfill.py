#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""기존 웹앱 케이스에 기하 τ 전체판 (τ_Dij,all) 을 채운다 — 파이프라인을 다시 돌리지 않고 (1저자 10-02).

  python3 scripts/tau_all_backfill.py --webapp-root ~/Yonghoon-DEM-DFT/webapp --name input_6mAh_real_1_D9 [...] [--write] [--tsv 표.tsv]
  python3 scripts/tau_all_backfill.py --results RESULTS_DIR [...] --type-map 1:AM_P,2:AM_S,3:SE --scale 1000 [--write]

같은 입력 · 같은 함수: results/<케이스>/atoms.csv · contacts.csv (웹앱 분석기가 읽은 그 파일 — run_pipeline 이 results 폴더에 둔다)
→ analyze_contacts.load_atoms_raw · load_contacts_raw → dem_analysis_core 의 _get_box_xy · get_plate_z · calc_percolation →
  calc_tortuosity (표본판 재계산) · calc_tortuosity_all.

· 표본판 재계산이 저장된 tortuosity_mean 과 같으면 (상대 1e-12) 분석 때와 입력이 같다는 증거 = 'match'.
· --write 는 match 일 때만 full_metrics.json 에 tortuosity_all_* + tortuosity_all_provenance 를 더한다 — 다른 키는 그대로 ·
  원본은 처음 한 번 full_metrics.json.pre_tau_all 로 남긴다.  mismatch 면 거부 (rc 2) — 그 케이스는 파이프라인을 다시 돌린다.
· 표 (TSV): 케이스 · SE 수 · τ_Dij (저장 · 재계산 · 일치) · τ_Dij,all (평균 · 중앙 · std · n · n_sources) · τ_Lap,bulk · τ_Lap,eff (Hertz ·
  physics) — 웹앱 τ 비교 블록과 같은 식 √(φ_SE · σ_grain / σ) · σ_grain = 웹앱 `_sigma_grain_mS_cm` — 그 제곱 (tortuosity factor) · CF/FULL.
⚠ τ_Dij,all 은 길이만 보는 기하 τ 다 (수송 τ 아님 · 정의 = `dem_analysis_core.calc_tortuosity_all`).
"""
import argparse
import datetime
import glob
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

TAU_KEYS = ('mean', 'median', 'std', 'n', 'n_sources', 'recommended')
COLS = ('case', 'results_dir', 'n_se', 'tau_dij_stored', 'tau_dij_recomputed', 'recheck',
        'tau_all_mean', 'tau_all_median', 'tau_all_std', 'tau_all_n', 'tau_all_n_sources',
        'tau_lap_bulk', 'tau_lap_eff_hertz', 'tau_lap_eff_physics', 'tau_lap_eff_hertz_sq', 'cf_full', 'phi_se', 'sigma_grain_mScm',
        'written')


def parse_type_map(s):
    tm = {}
    for item in str(s).split(','):
        k, v = item.split(':')
        tm[int(k)] = v.strip()
    return tm


def resolve_cases(webapp_root, names):
    """uploads/<id>/meta.json 의 name 으로 찾는다 → (name, results_dir, type_map_str, scale).  같은 이름이 둘이면 거부."""
    import type_map_resolve as tmr
    found = {}
    for mp in sorted(glob.glob(os.path.join(webapp_root, 'uploads', '*', 'meta.json'))):
        try:
            meta = json.load(open(mp, encoding='utf-8'))
        except Exception:
            continue
        nm = meta.get('name')
        if nm in names:
            cid = os.path.basename(os.path.dirname(mp))
            found.setdefault(nm, []).append((cid, meta))
    out = []
    for nm in names:
        hits = found.get(nm) or []
        if len(hits) != 1:
            raise SystemExit(f'⛔ 케이스 이름 {nm!r}: uploads 에서 {len(hits)} 개 — 정확히 하나여야 한다 '
                             f'({", ".join(c for c, _ in hits) or "없음"})')
        cid, meta = hits[0]
        tm_str, _fb = tmr.map_str_from_meta(meta, 'tau_all_backfill')
        out.append((nm, os.path.join(webapp_root, 'results', cid), tm_str, float(meta.get('scale', 1000))))
    return out


def _sigma_grain(metrics):
    """웹앱과 같은 σ_grain (온도 provenance 포함).  웹앱을 못 불러오면 None — τ_Lap 칸을 비운다 (다른 값으로 대신하지 않는다)."""
    try:
        wp = os.path.join(ROOT, 'webapp')
        if wp not in sys.path:
            sys.path.insert(0, wp)
        import app as _app                                   # noqa: E402
        return float(_app._sigma_grain_mS_cm(metrics))
    except Exception as e:                                   # pragma: no cover — 환경 의존
        print(f'  ⚠ 웹앱 _sigma_grain_mS_cm 을 못 불렀다 ({e}) — τ_Lap 칸은 비운다', file=sys.stderr)
        return None


def _code_sha():
    try:
        return subprocess.run(['git', '-C', ROOT, 'rev-parse', 'HEAD'], capture_output=True, text=True,
                              timeout=10).stdout.strip() or None
    except Exception:
        return None


def process(name, results_dir, type_map_str, scale, write):
    import analyze_contacts as ac
    import dem_analysis_core as dac
    fm_path = os.path.join(results_dir, 'full_metrics.json')
    atoms_csv, contacts_csv = (os.path.join(results_dir, f) for f in ('atoms.csv', 'contacts.csv'))
    for p in (fm_path, atoms_csv, contacts_csv):
        if not os.path.exists(p):
            raise SystemExit(f'⛔ {name}: {p} 없음 — 이 케이스는 채울 수 없다 (파이프라인을 다시 돌린다)')
    metrics = json.load(open(fm_path, encoding='utf-8'))
    type_map = parse_type_map(type_map_str)
    se_types = [k for k, v in type_map.items() if v == 'SE']
    atoms_raw, _ = ac.load_atoms_raw(atoms_csv)
    contacts_raw, _ = ac.load_contacts_raw(contacts_csv)
    box_x, box_y = dac._get_box_xy(results_dir)
    plate_z, _src = dac.get_plate_z(results_dir, atoms_raw, scale)
    perc = dac.calc_percolation(atoms_raw, contacts_raw, se_types, plate_z, box_x=box_x, box_y=box_y)
    tau = dac.calc_tortuosity(atoms_raw, perc, box_x=box_x, box_y=box_y)
    tau_all = dac.calc_tortuosity_all(atoms_raw, perc, box_x=box_x, box_y=box_y)

    stored, recomputed = metrics.get('tortuosity_mean'), tau.get('mean')
    if stored is None and recomputed is None:
        recheck = 'match'
    elif stored is None or recomputed is None:
        recheck = 'mismatch'
    else:
        recheck = 'match' if abs(float(stored) - float(recomputed)) <= 1e-12 * max(1.0, abs(float(stored))) else 'mismatch'

    row = {'case': name, 'results_dir': results_dir, 'n_se': perc.get('se_count'),
           'tau_dij_stored': stored, 'tau_dij_recomputed': recomputed, 'recheck': recheck,
           **{f'tau_all_{k}': tau_all.get(k) for k in TAU_KEYS if k != 'recommended'},
           'phi_se': metrics.get('phi_se'), 'written': 'no'}
    sg = _sigma_grain(metrics) if (metrics.get('phi_se') and metrics.get('sigma_full_mScm')) else None
    row['sigma_grain_mScm'] = sg
    phi = metrics.get('phi_se')

    def _lap(sig):
        return math.sqrt(phi * sg / sig) if (phi and sg and sig and sig > 0) else None
    row['tau_lap_bulk'] = _lap(metrics.get('sigma_bulk_net_mScm'))
    row['tau_lap_eff_hertz'] = _lap(metrics.get('sigma_full_mScm'))
    row['tau_lap_eff_physics'] = _lap(metrics.get('sigma_full_mScm_physics'))
    row['tau_lap_eff_hertz_sq'] = row['tau_lap_eff_hertz'] ** 2 if row['tau_lap_eff_hertz'] else None
    sb, sf = metrics.get('sigma_bulk_net_mScm'), metrics.get('sigma_full_mScm')
    row['cf_full'] = (sb / sf) if (sb and sf and sf > 0) else None

    if write:
        if recheck != 'match':
            print(f'⛔ {name}: 표본판 재계산 {recomputed} ≠ 저장 {stored} — 분석 때와 입력이 다르다 · 쓰지 않는다 '
                  f'(파이프라인을 다시 돌려 채울 것)', file=sys.stderr)
            return row, 2
        bak = fm_path + '.pre_tau_all'
        if not os.path.exists(bak):
            with open(bak, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, ensure_ascii=False)
        new = dict(metrics)
        for k in TAU_KEYS:
            new[f'tortuosity_all_{k}'] = tau_all.get(k)
        new['tortuosity_all_provenance'] = {
            'method': 'backfill scripts/tau_all_backfill.py (파이프라인 재실행 없음 · 같은 atoms.csv · contacts.csv)',
            'code_sha': _code_sha(), 'computed_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
            'sampled_recheck': recheck, 'n_se': perc.get('se_count')}
        tmp = fm_path + '.tmp_tau_all'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(new, f, ensure_ascii=False, default=str)
        os.replace(tmp, fm_path)
        row['written'] = 'yes'
    return row, 0


def _fmt(v):
    if v is None:
        return ''
    if isinstance(v, float):
        return f'{v:.6f}'
    return str(v)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--webapp-root', help='웹앱 데이터 폴더 (uploads/ · results/ 가 있는 곳)')
    ap.add_argument('--name', nargs='+', default=[], help='케이스 이름 (uploads/<id>/meta.json 의 name)')
    ap.add_argument('--results', nargs='+', default=[], help='results/<id> 폴더를 직접 (--type-map · --scale 필요)')
    ap.add_argument('--type-map', help="--results 용 (예: 1:AM_P,2:AM_S,3:SE)")
    ap.add_argument('--scale', type=float, default=1000.0)
    ap.add_argument('--write', action='store_true', help='표본판 재계산이 저장값과 같을 때만 full_metrics.json 에 새 키를 더한다')
    ap.add_argument('--tsv', help='표를 TSV 로 저장')
    a = ap.parse_args(argv)

    jobs = []
    if a.name:
        if not a.webapp_root:
            ap.error('--name 은 --webapp-root 와 함께')
        jobs += resolve_cases(a.webapp_root, a.name)
    if a.results:
        if not a.type_map:
            ap.error('--results 는 --type-map 과 함께')
        jobs += [(os.path.basename(os.path.dirname(r.rstrip('/'))) if os.path.basename(r.rstrip('/')) == 'out'
                  else os.path.basename(r.rstrip('/')), r, a.type_map, a.scale) for r in a.results]
    if not jobs:
        ap.error('케이스가 없다 (--name 또는 --results)')

    rows, rc = [], 0
    for nm, rd, tm, sc in jobs:
        print(f'── {nm}  ({rd})', flush=True)
        row, r = process(nm, rd, tm, sc, a.write)
        rows.append(row)
        rc = max(rc, r)
        print('   ' + ' · '.join(f'{k} {_fmt(row.get(k))}' for k in
                                 ('n_se', 'tau_dij_stored', 'recheck', 'tau_all_mean', 'tau_all_n', 'tau_lap_bulk',
                                  'tau_lap_eff_hertz', 'tau_lap_eff_hertz_sq', 'written')), flush=True)
    if a.tsv:
        with open(a.tsv, 'w', encoding='utf-8') as f:
            f.write('\t'.join(COLS) + '\n')
            for row in rows:
                f.write('\t'.join(_fmt(row.get(c)) for c in COLS) + '\n')
        print(f'표 → {a.tsv}')
    return rc


if __name__ == '__main__':
    sys.exit(main())
