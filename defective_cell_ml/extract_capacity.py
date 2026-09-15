"""Validated cycler/EIS readers and a CSV preparation CLI. No import side effects."""
from pathlib import Path
import argparse
import io
import re
import numpy as np
import pandas as pd
from config import Config, DataError, digest, load_config, write_json

CYCLE_COLUMNS=['Test Time(s)','Step Time(s)','Cycle No.','Step No.','|Q|(Ah)','Voltage(V)','Current(A)']
FEATURE_RE=re.compile(r'^(mag|re|im|phase)@([0-9.eE+\-]+)Hz$')

def read_text(path,cfg):
    raw=Path(path).read_bytes()
    for encoding in cfg.encodings:
        try:
            return raw.decode(encoding),encoding
        except UnicodeDecodeError:
            continue
    raise DataError(f'{Path(path).name}: unsupported encoding {cfg.encodings}')

def cell_id(filename):
    m=re.search(r'cell(\d+)',Path(filename).name,re.I)
    if not m:
        raise DataError(f'{filename}: missing cell<number> in filename')
    return int(m.group(1))

def read_table(path,required,cfg):
    text,encoding=read_text(path,cfg)
    lines=text.splitlines()
    header=None
    for i,line in enumerate(lines[:300]):
        cols=[v.strip() for v in line.split('\t')]
        if set(required).issubset(cols):
            if len(cols)!=len(set(cols)):
                raise DataError(f'{Path(path).name}: duplicate column headers')
            header=i
            break
    if header is None:
        raise DataError(f'{Path(path).name}: required header not found: {required}')
    frame=pd.read_csv(io.StringIO('\n'.join(lines[header:])),sep='\t',dtype=str)
    frame.columns=[c.strip() for c in frame.columns]
    if frame.empty:
        raise DataError(f'{Path(path).name}: no data rows')
    return frame,{'encoding':encoding,'header_line_1based':header+1}

def find_cv_start(frame,tol=.01):
    current=np.abs(frame['current'].to_numpy(dtype=float))
    if not len(current) or not np.isfinite(current).all() or current[0]<=0:
        raise DataError('CC/CV detection requires a finite, nonzero first current')
    indices=np.flatnonzero(current<current[0]*(1-tol))
    return int(indices[0]) if len(indices) else None

def read_cycle(path,cfg=None):
    cfg=(cfg or Config()).validate()
    frame,info=read_table(path,CYCLE_COLUMNS,cfg)
    first=frame.iloc[0]
    # Remove only a recognized units row, never an arbitrary first observation.
    is_units=(str(first['|Q|(Ah)']).strip(' []()').lower()=='ah'
              and str(first['Current(A)']).strip(' []()').lower()=='a')
    if is_units:
        frame=frame.iloc[1:].copy()
    if frame.empty:
        raise DataError(f'{Path(path).name}: no observations after units row')
    numeric=frame[CYCLE_COLUMNS].apply(pd.to_numeric,errors='coerce')
    if not np.isfinite(numeric.to_numpy()).all():
        raise DataError(f'{Path(path).name}: nonnumeric or nonfinite required cycle values')
    numeric.columns=['time','step_time','cycle','step','capacity','voltage','current']
    if not np.equal(numeric[['cycle','step']],np.floor(numeric[['cycle','step']])).all().all():
        raise DataError('Cycle/Step numbers must be integers')
    if (np.diff(numeric['time'])<0).any():
        raise DataError(f'{Path(path).name}: time is not monotonic; inspect acquisition order')
    cycle=numeric[numeric['cycle']==cfg.target_cycle].copy()
    if cycle.empty:
        raise DataError(f'{Path(path).name}: target cycle {cfg.target_cycle} missing')
    cycle['step_i']=(cycle['step'].ne(cycle['step'].shift())).cumsum()-1
    segment=cycle[cycle['step_i']==cfg.target_step_i] if cfg.target_raw_step is None else cycle[cycle['step']==cfg.target_raw_step]
    if segment.empty:
        raise DataError(f'{Path(path).name}: target segment missing')
    if cfg.target_raw_step is not None and segment['step_i'].nunique()!=1:
        raise DataError('Raw Step No. occurs in multiple segments; use target_step_i')
    currents=segment['current'].to_numpy()
    sign=1 if cfg.expected_current_sign=='positive' else -1
    if (sign*currents<=0).any():
        raise DataError('Selected segment current sign/zero does not match configured charging direction')
    capacities=segment['capacity'].to_numpy()
    if (capacities<0).any() or (np.diff(capacities)<-1e-12).any() or capacities[-1]<=0:
        raise DataError('Selected capacity must be nonnegative, monotonic, and end positive')
    cv=find_cv_start(segment,cfg.cv_relative_drop)
    cap=float(capacities[-1])
    cc=cap if cv is None else float(capacities[cv])
    if not 0<=cc<=cap:
        raise DataError('Invalid CC/total capacity relationship')
    pressure=re.search(r'_(\d+(?:\.\d+)?)MPa',Path(path).name,re.I)
    info.update(units_row_removed=bool(is_units),raw_step=float(segment['step'].iloc[0]),
                step_i=int(segment['step_i'].iloc[0]),segment_rows=len(segment),
                cv_first_below_index=cv,cc_definition='capacity through first below-threshold current row',
                initial_capacity_ah=float(capacities[0]))
    return {'cell_number':cell_id(path),'pressure_mpa':float(pressure.group(1)) if pressure else None,
            'cap':cap,'cap_cc':cc,'cap_cv':cap-cc,'cc_frac':cc/cap},info

def convert_mpt(path,cfg=None):
    cfg=(cfg or Config()).validate()
    frame,info=read_table(path,['freq/Hz','Re(Z)/Ohm','-Im(Z)/Ohm'],cfg)
    required=['freq/Hz','Re(Z)/Ohm','-Im(Z)/Ohm']
    numeric=frame[required].apply(pd.to_numeric,errors='coerce')
    if not np.isfinite(numeric.to_numpy()).all() or (numeric['freq/Hz']<=0).any():
        raise DataError(f'{Path(path).name}: EIS frequency/complex values must be finite; frequency > 0')
    spec=pd.DataFrame({'f':numeric.iloc[:,0],'re':numeric.iloc[:,1],'im':-numeric.iloc[:,2]})
    if '<Ewe>/V' in frame:
        ocv=pd.to_numeric(frame['<Ewe>/V'],errors='coerce')
        if cfg.use_ocv and not np.isfinite(ocv).all():
            raise DataError(f'{Path(path).name}: missing/nonfinite EIS potential')
        spec['ocv']=ocv
    elif cfg.use_ocv:
        raise DataError(f'{Path(path).name}: <Ewe>/V missing; set use_ocv=false for an EIS-only analysis')
    if '|Z|/Ohm' in frame:
        mag=pd.to_numeric(frame['|Z|/Ohm'],errors='coerce').to_numpy()
        expected=np.hypot(spec['re'],spec['im']).to_numpy()
        info['raw_magnitude_max_abs_difference_ohm']=float(np.max(np.abs(mag-expected))) if np.isfinite(mag).all() else None
    info['raw_rows']=len(spec)
    return spec,info

def build_features(spectrum,cfg):
    df=spectrum.copy()
    if not len(df) or not np.isfinite(df[['f','re','im']]).all().all() or (df['f']<=0).any():
        raise DataError('Invalid EIS spectrum')
    duplicates=int(df['f'].duplicated().sum())
    if duplicates:
        if cfg.duplicate_frequency_policy=='error':
            raise DataError('Duplicate EIS frequencies; select a sweep or explicitly allow mean')
        df=df.groupby('f',as_index=False).mean(numeric_only=True)
    df=df.sort_values('f')
    if len(df)<2:
        raise DataError('At least two distinct EIS frequencies required')
    grid=np.asarray(cfg.frequency_grid_hz,dtype=float)
    low,high=float(df['f'].iloc[0]),float(df['f'].iloc[-1])
    outside=(grid<low)|(grid>high)
    if outside.any():
        fraction=np.maximum((low-grid)/low,(grid-high)/high)
        if cfg.boundary_policy=='error' or np.max(fraction)>cfg.max_boundary_fraction+1e-12:
            raise DataError(f'Configured frequencies {grid[outside].tolist()} exceed measured support [{low}, {high}]')
    real=np.interp(np.log10(grid),np.log10(df['f']),df['re'])
    imaginary=np.interp(np.log10(grid),np.log10(df['f']),df['im'])
    values={'re':real,'im':imaginary,'mag':np.hypot(real,imaginary),
            'phase':np.degrees(np.arctan2(imaginary,real))}
    result={f'{comp}@{f:g}Hz':float(v) for comp,array in values.items() for f,v in zip(grid,array)}
    if cfg.use_ocv:
        if 'ocv' not in df or not np.isfinite(df['ocv']).all():
            raise DataError('Finite EIS potential required when use_ocv=true')
        result['ocv']=float(np.median(df['ocv']))
    return result,{'duplicate_frequency_rows':duplicates,'clamped_frequencies_hz':grid[outside].tolist(),
                   'representation':'interpolate Re/Im on log10 frequency; derive magnitude/phase',
                   'eis_units':'Ohm; phase degrees','support_hz':[low,high]}

def included(cell,cfg,events):
    reason=None
    if not cfg.cell_min<=cell<=cfg.cell_max:
        reason='outside configured cell range'
    elif str(cell) in cfg.exclude_cells:
        reason=cfg.exclude_cells[str(cell)]
    if reason:
        events.append({'cell_number':cell,'status':'excluded','reason':reason})
    return reason is None

def inventory(directory,suffix):
    directory=Path(directory)
    if not directory.is_dir():
        raise DataError(f'Input directory missing: {directory}')
    files=sorted(p for p in directory.iterdir() if p.is_file() and p.suffix.lower()==suffix)
    if not files:
        raise DataError(f'No {suffix} input files in {directory}')
    return files

def load_raw(cycle_dir,eis_dir,cfg,events,manifest=None):
    pairs=[]
    if manifest:
        m=pd.read_csv(manifest,dtype=str)
        required={'cell_number','eis_file'}|({'cycle_file'} if cycle_dir else set())
        if not required.issubset(m):
            raise DataError(f'Manifest requires {sorted(required)}')
        if m['cell_number'].duplicated().any():
            raise DataError('Manifest must select exactly one measurement per cell')
        for row in m.to_dict('records'):
            cell=int(row['cell_number'])
            if not included(cell,cfg,events):
                continue
            paths={}
            for key,directory in [('eis_file',eis_dir),('cycle_file',cycle_dir)]:
                if directory:
                    base=Path(directory).resolve()
                    p=(base/row[key]).resolve()
                    if not p.is_relative_to(base) or not p.is_file():
                        raise DataError(f'Manifest path missing or outside input directory: {row[key]}')
                    if cell_id(p)!=cell:
                        raise DataError(f'Manifest and filename cell IDs disagree: {p.name}')
                    paths[key]=p
            pairs.append((cell,paths.get('cycle_file'),paths['eis_file'],row.get(cfg.group_column)))
    else:
        maps=[]
        for directory,suffix in [(cycle_dir,'.txt'),(eis_dir,'.mpt')]:
            found={}
            if directory:
                for p in inventory(directory,suffix):
                    cell=cell_id(p)
                    if not included(cell,cfg,events):
                        continue
                    if cell in found:
                        raise DataError(f'Duplicate cell {cell}: {found[cell].name}, {p.name}; provide a selection manifest')
                    found[cell]=p
            maps.append(found)
        cycles,spectra=maps
        if cycle_dir and set(cycles)!=set(spectra):
            raise DataError(f'Unmatched cells: missing EIS {sorted(set(cycles)-set(spectra))}; missing cycle {sorted(set(spectra)-set(cycles))}')
        pairs=[(cell,cycles.get(cell),spectra[cell],None) for cell in sorted(spectra)]
    if not pairs:
        raise DataError('No retained measurements')
    rows=[]
    for cell,cycle_path,eis_path,group in pairs:
        row={'cell_number':cell}
        event={'cell_number':cell,'status':'processing','eis_file':str(eis_path),'eis_sha256':digest(eis_path)}
        if cycle_path:
            event.update(cycle_file=str(cycle_path),cycle_sha256=digest(cycle_path))
        events.append(event)
        try:
            if cycle_path:
                target,detail=read_cycle(cycle_path,cfg)
                row.update(target)
                event['cycle_reader']=detail
            spec,detail=convert_mpt(eis_path,cfg)
            features,feature_detail=build_features(spec,cfg)
        except Exception as exc:
            event.update(status='failed',error=str(exc),error_type=type(exc).__name__)
            raise DataError(f'Cell {cell}: {exc}') from exc
        row.update(features)
        if group is not None and pd.notna(group):
            row[cfg.group_column]=group
        event.update(status='included',eis_reader=detail,feature_processing=feature_detail)
        rows.append(row)
    return pd.DataFrame(rows).sort_values('cell_number').reset_index(drop=True)

def validate_frame(frame,cfg,events,training=True):
    df=frame.copy()
    if 'cell_number' not in df or df.empty:
        raise DataError('Nonempty input with cell_number required')
    ids=pd.to_numeric(df['cell_number'],errors='coerce')
    if not np.isfinite(ids).all() or not np.equal(ids,np.floor(ids)).all():
        raise DataError('cell_number must contain finite integers')
    df['cell_number']=ids.astype(int)
    if df['cell_number'].duplicated().any():
        raise DataError('Duplicate cell_number: select one measurement per cell before analysis')
    if training:
        df=df[[included(int(c),cfg,events) for c in df['cell_number']]].copy()
    if df.empty:
        raise DataError('No rows remain after exclusions')
    features=[]
    for name in df.columns:
        match=FEATURE_RE.fullmatch(name)
        if not match and name.startswith(('mag@','re@','im@','phase@')):
            raise DataError(f'Invalid EIS feature name: {name}; example mag@1000Hz')
        if match:
            frequency=float(match.group(2))
            if not np.isfinite(frequency) or frequency<=0:
                raise DataError(f'Invalid feature frequency: {name}')
            canonical=f'{match.group(1)}@{frequency:g}Hz'
            if canonical!=name:
                raise DataError(f'Use canonical feature name {canonical}, not {name}')
            features.append(name)
    if not features:
        raise DataError('No EIS feature columns (example mag@1000Hz)')
    if cfg.use_ocv:
        if 'ocv' not in df:
            raise DataError('ocv required; set use_ocv=false for EIS-only analysis')
        features.append('ocv')
    df[features]=df[features].apply(pd.to_numeric,errors='coerce')
    if not np.isfinite(df[features]).all().all():
        raise DataError('Features contain NaN/Inf/nonnumeric values; correct measurements rather than implicitly imputing')
    if training:
        if 'cap' not in df:
            raise DataError('Training input needs cap in Ah')
        df['cap']=pd.to_numeric(df['cap'],errors='coerce')
        valid=np.isfinite(df['cap'])&(df['cap']>0)
        if not valid.all():
            bad=df.loc[~valid,'cell_number'].tolist()
            events.extend({'cell_number':int(c),'status':'unlabeled_invalid','reason':'cap must be finite and positive; no binary label assigned'} for c in bad)
            raise DataError(f'Invalid/missing capacity for cells {bad}; separate unlabeled rows for prediction')
        if 'cc_frac' in df:
            original=df['cc_frac']
            df['cc_frac']=pd.to_numeric(original,errors='coerce')
            if (original.notna() & df['cc_frac'].isna()).any():
                raise DataError('cc_frac has nonnumeric values; only explicit missing values may be omitted')
            present=df['cc_frac'].notna()
            if ((df.loc[present,'cc_frac']<0)|(df.loc[present,'cc_frac']>1)|~np.isfinite(df.loc[present,'cc_frac'])).any():
                raise DataError('cc_frac must be between 0 and 1 or missing')
        if cfg.outer_cv=='leave_one_group_out':
            if cfg.group_column not in df or df[cfg.group_column].isna().any() or df[cfg.group_column].astype(str).str.strip().eq('').any():
                raise DataError(f'Group evaluation requires nonmissing {cfg.group_column}')
            df[cfg.group_column]=df[cfg.group_column].astype(str)
    return df.sort_values('cell_number').reset_index(drop=True),features

def main(argv=None):
    parser=argparse.ArgumentParser(description='Prepare validated EIS/capacity features without model fitting')
    parser.add_argument('--config')
    parser.add_argument('--cycle-dir')
    parser.add_argument('--eis-dir',required=True)
    parser.add_argument('--selection-manifest')
    parser.add_argument('--output',required=True,help='New CSV file')
    args=parser.parse_args(argv)
    cfg=load_config(args.config)
    output=Path(args.output)
    if output.exists() or output.with_suffix('.audit.json').exists():
        parser.error('Output already exists; choose a new path')
    events=[]
    try:
        df=load_raw(args.cycle_dir,args.eis_dir,cfg,events,args.selection_manifest)
        df,_=validate_frame(df,cfg,events,training=bool(args.cycle_dir))
        output.parent.mkdir(parents=True,exist_ok=True)
        df.to_csv(output,index=False,encoding='utf-8-sig')
        write_json(output.with_suffix('.audit.json'),events)
    except DataError as e:
        parser.exit(2,f'Input error: {e}\n')
    print(f'Prepared {len(df)} cells: {output}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
