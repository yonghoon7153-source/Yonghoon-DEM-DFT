#!/usr/bin/env python3
"""EIS measurement archiver — BioLogic .mpr → tidy CSV + catalog.

INTENT
------
Ingest the lab's BioLogic EC-Lab EIS raw files (`.mpr` binary + `.mps` settings)
into a version-controlled, self-describing archive under
`docs/data/eis_measurements/`:

  raw/        <-- the original .mpr/.mps (renamed, uuid prefix stripped)
  extracted/  <-- one tidy CSV per .mpr  (freq, Re(Z), -Im(Z), |Z|, phase, ...)
  eis_catalog.csv  <-- one row per measurement, metadata parsed from the filename
                       + quick descriptors (R_s, low-freq Re, arc width)

WHY the CSVs are committed (not just the .mpr): the .mpr parser (`galvani`,
GPL-3.0) is an EXTERNAL dependency we deliberately do NOT vendor into this repo.
The tidy CSVs are the user's own data and make the archive fully usable
(plotting, fitting, model anchoring) without galvani installed.  Re-running this
script only NEEDS galvani when INGESTING NEW .mpr files.

PARSER RESOLUTION (lazy, no hard dependency):
  1. `from galvani import BioLogic`         (pip install galvani)
  2. env GALVANI_SRC=/path/to/galvani/src   (dir containing BioLogic.py)
  3. otherwise: skip extraction, catalog from existing extracted/*.csv

FILENAME TAXONOMY (lab convention, date_sample_blend_cell_...):
  260715_No1_only_sym_01_C01      -> 2026-07-15, No1, pure-small,   symmetric, run01, C01
  260719_No1_only_full_1cyc_02_1_C01 -> full cell, 1 cycle, run02_1
  260719_No1_55_70um_sym_01_C01   -> 5:5 poly:small blend, 70 um,   symmetric
  ..._C06_1.3V                    -> EIS taken at 1.3 V cell state

⚠ AREA: the .mps 'Electrode surface area' is a placeholder (0.001 cm2), so the
raw impedances are in Ω, NOT Ω·cm².  To compare against manuscript R_int
(Ω·cm²) multiply by the true electrode area (see README).  Catalog keeps Ω.
"""
import csv
import os
import re
import sys

ARCHIVE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       '이종기술', 'eis')     # hetero-tech project (separate from SDCP)
RAW = os.path.join(ARCHIVE, 'raw')
EXTRACTED = os.path.join(ARCHIVE, 'extracted')
CATALOG = os.path.join(ARCHIVE, 'eis_catalog.csv')

# tidy-CSV columns, mapped from the BioLogic dtype field names
_FIELD_MAP = [
    ('freq_Hz', 'freq/Hz'), ('ReZ_ohm', 'Re(Z)/Ohm'), ('negImZ_ohm', '-Im(Z)/Ohm'),
    ('absZ_ohm', '|Z|/Ohm'), ('phase_deg', 'Phase(Z)/deg'), ('Ewe_V', '<Ewe>/V'),
    ('I_mA', '<I>/mA'), ('cycle', 'cycle number'),
]

# Electrode disk diameter by cell type (lab notes 2026-06: 대칭셀=10pi, 율특/수명=13pi).
# Ω → Ω·cm² = Ω × area.  Inferred from cell geometry, NOT per-file measured.
_PI_DIAM_MM = {'symmetric': 10.0, 'full': 13.0}


def _area_cm2(cell_type):
    import math
    d = _PI_DIAM_MM.get(cell_type)
    return round(math.pi * (d / 2.0 / 10.0) ** 2, 4) if d else None


def _load_biologic():
    """Return the galvani BioLogic module, or None (with a message)."""
    try:
        from galvani import BioLogic          # pip install galvani
        return BioLogic
    except Exception:
        pass
    src = os.environ.get('GALVANI_SRC')
    if src and os.path.isdir(src):
        sys.path.insert(0, src)
        try:
            import BioLogic                    # noqa: E402  (galvani/BioLogic.py on GALVANI_SRC)
            return BioLogic
        except Exception as e:
            print(f'  [warn] GALVANI_SRC set but import failed: {e}')
    return None


def parse_name(stem):
    """Filename stem (no extension) -> metadata dict.  Best-effort; the full
    filename is always kept in the catalog for provenance."""
    toks = stem.split('_')
    d = {'filename': stem, 'date': '', 'sample': '', 'blend': '', 'thickness_um': '',
         'cell_type': '', 'cycle': '', 'state': '', 'technique': '', 'run': ''}
    if toks and re.fullmatch(r'\d{6}', toks[0]):
        yy, mm, dd = toks[0][:2], toks[0][2:4], toks[0][4:]
        d['date'] = f'20{yy}-{mm}-{dd}'
    for t in toks:
        if re.fullmatch(r'No\d+', t):
            d['sample'] = t
        elif t == 'full':
            d['cell_type'] = 'full'
        elif t == 'sym':
            d['cell_type'] = 'symmetric'
        elif re.fullmatch(r'\d+um', t):
            d['thickness_um'] = t[:-2]
        elif re.fullmatch(r'\d+cyc', t):
            d['cycle'] = t[:-3]
        elif re.fullmatch(r'C\d+', t):
            d['technique'] = t
        elif re.fullmatch(r'\d+\.\d+V', t):
            d['state'] = t
    # blend: 'only' = pure small-particle; a 2-digit token preceding a '<N>um' = ratio
    if 'only' in toks:
        d['blend'] = 'pure_small'
    else:
        for i, t in enumerate(toks):
            if re.fullmatch(r'\d{2}', t) and i + 1 < len(toks) and re.fullmatch(r'\d+um', toks[i + 1]):
                d['blend'] = f'{t[0]}:{t[1]}_poly:small'    # '55' -> '5:5_poly:small'
                break
    if not d['state']:
        d['state'] = 'OCV'
    # run: the maximal stretch of pure-digit tokens ending just before the C-technique token
    ti = next((i for i, t in enumerate(toks) if re.fullmatch(r'C\d+', t)), len(toks))
    run = []
    j = ti - 1
    while j >= 0 and toks[j].isdigit():
        run.insert(0, toks[j])
        j -= 1
    d['run'] = '_'.join(run)
    return d


def _rs_intercept(re_z, im_z):
    """High-freq real-axis intercept R_s: first -Im crossing 0 (inductive->capacitive)."""
    import numpy as np
    for i in range(len(im_z) - 1):
        if im_z[i] <= 0 and im_z[i + 1] > 0:
            t = -im_z[i] / (im_z[i + 1] - im_z[i])
            return float(re_z[i] + t * (re_z[i + 1] - re_z[i]))
    return float(re_z[int(np.argmin(np.abs(im_z)))])


def extract_mpr(BioLogic, mpr_path, out_csv):
    """Parse one .mpr -> tidy CSV; return a descriptor dict (Ω, not Ω·cm²)."""
    import numpy as np
    m = BioLogic.MPRfile(mpr_path)
    d = m.data
    names = set(d.dtype.names)
    cols = [(k, src) for k, src in _FIELD_MAP if src in names]
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow([k for k, _ in cols])
        for row in d:
            w.writerow([row[src] for _, src in cols])
    f_hz = d['freq/Hz']
    re_z = d['Re(Z)/Ohm']
    im_z = d['-Im(Z)/Ohm']
    rs = _rs_intercept(re_z, im_z)
    lf = float(re_z[int(np.argmin(f_hz))])
    return {'n_points': len(d), 'f_max_Hz': float(f_hz.max()), 'f_min_Hz': float(f_hz.min()),
            'R_s_ohm': round(rs, 3), 'Re_LF_ohm': round(lf, 3), 'arc_ohm': round(lf - rs, 3)}


def main():
    os.makedirs(EXTRACTED, exist_ok=True)
    BioLogic = _load_biologic()
    if BioLogic is None:
        print('  [info] galvani not available -> cataloging from existing extracted/*.csv only.')
        print('         (pip install galvani  OR  export GALVANI_SRC=/path/to/galvani)')
    mprs = sorted(f for f in os.listdir(RAW) if f.lower().endswith('.mpr'))
    rows = []
    cat_cols = ['filename', 'date', 'sample', 'blend', 'thickness_um', 'cell_type',
                'cycle', 'state', 'technique', 'run', 'n_points', 'f_max_Hz', 'f_min_Hz',
                'area_cm2', 'R_s_ohm', 'Re_LF_ohm', 'arc_ohm',
                'R_s_ohmcm2', 'Re_LF_ohmcm2', 'arc_ohmcm2', 'extracted_csv', 'note']
    for fn in mprs:
        stem = fn[:-4]
        meta = parse_name(stem)
        out_csv = os.path.join(EXTRACTED, stem + '.csv')
        note = ''
        desc = {k: '' for k in ('n_points', 'f_max_Hz', 'f_min_Hz', 'R_s_ohm', 'Re_LF_ohm', 'arc_ohm')}
        if BioLogic is not None:
            try:
                desc = extract_mpr(BioLogic, os.path.join(RAW, fn), out_csv)
            except Exception as e:
                note = f'extract_fail: {e}'
        elif os.path.exists(out_csv):
            note = 'cached_csv (galvani absent)'
        meta.update(desc)
        area = _area_cm2(meta['cell_type'])          # Ω → Ω·cm² via disk area (10pi sym / 13pi full)
        meta['area_cm2'] = area if area else ''
        for k_ohm, k_asr in (('R_s_ohm', 'R_s_ohmcm2'), ('Re_LF_ohm', 'Re_LF_ohmcm2'),
                             ('arc_ohm', 'arc_ohmcm2')):
            v = meta.get(k_ohm, '')
            meta[k_asr] = round(float(v) * area, 2) if (area and v != '') else ''
        meta['extracted_csv'] = os.path.relpath(out_csv, ARCHIVE) if os.path.exists(out_csv) else ''
        meta['note'] = note
        rows.append(meta)
    # stable order: date, cell_type, blend, sample, filename
    rows.sort(key=lambda r: (r['date'], r['cell_type'], r['blend'], r['sample'], r['filename']))
    with open(CATALOG, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cat_cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in cat_cols})
    print(f'  cataloged {len(rows)} measurements -> {os.path.relpath(CATALOG)}')
    ok = sum(1 for r in rows if r['n_points'] != '')
    print(f'  extracted {ok}/{len(rows)} tidy CSVs -> {os.path.relpath(EXTRACTED)}/')
    return rows


if __name__ == '__main__':
    main()
