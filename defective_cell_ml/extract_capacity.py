"""Validated cycler/EIS readers and a CSV preparation CLI. No import side effects."""
from pathlib import Path
import argparse
import io
import re
import numpy as np
import pandas as pd
from config import VERSION,Config,DataError,config_dict,digest,load_config,write_json

CYCLE_COLUMNS=['Test Time(s)','Step Time(s)','Cycle No.','Step No.','|Q|(Ah)','Voltage(V)','Current(A)']
CYCLE_NAMES={'Test Time(s)':'time','Step Time(s)':'step_time','Cycle No.':'cycle','Step No.':'step',
             '|Q|(Ah)':'capacity','Voltage(V)':'voltage','Current(A)':'current'}
RAW_NAMES={short:raw for raw,short in CYCLE_NAMES.items()}
EIS_COLUMNS=['freq/Hz','Re(Z)/Ohm','-Im(Z)/Ohm']
FEATURE_RE=re.compile(r'^(mag|re|im|phase)@([0-9.eE+\-]+)Hz$')
FEATURE_ANY_RE=re.compile(r'^(mag|re|im|phase)@([0-9.eE+\-]+)Hz$',re.I)
HANGUL_RE=re.compile(r'[가-힣]')
SPREADSHEETS=['.xlsx','.xlsm','.xls','.ods']
CAP_EXCESS_FACTOR=1.5
SAME_VOLTAGE_V=.01
IMPLAUSIBLE_CC_FRACTION=.2

def read_text(path,cfg):
    raw=Path(path).read_bytes()
    for encoding in cfg.encodings:
        try:
            return raw.decode(encoding),encoding
        except (UnicodeDecodeError,LookupError):
            continue
    raise DataError(f'{Path(path).name}: cannot decode with encodings {cfg.encodings}; '
                    'add the instrument code page (for example "cp1252") to config encodings')

def read_csv_any(path,cfg,**options):
    """Decode a CSV with the configured encodings before parsing; name the remedy on failure."""
    name=Path(path).name
    if Path(path).suffix.lower() in SPREADSHEETS:
        raise DataError(f'{name}: spreadsheets are not read; export a CSV (in Excel choose "CSV UTF-8")')
    try:
        text,encoding=read_text(path,cfg)
    except DataError as exc:
        raise DataError(f'{exc}; in Excel save the CSV as "CSV UTF-8"') from exc
    try:
        return pd.read_csv(io.StringIO(text),**options),encoding
    except (pd.errors.ParserError,pd.errors.EmptyDataError) as exc:
        raise DataError(f'{name}: unreadable CSV: {exc}') from exc

def cell_id(filename):
    m=re.search(r'cell(\d+)',Path(filename).name,re.I)
    if not m:
        raise DataError(f'{filename}: missing cell<number> in filename')
    return int(m.group(1))

def read_table(path,required,cfg):
    name=Path(path).name
    text,encoding=read_text(path,cfg)
    lines=text.splitlines()
    header=None
    for i,line in enumerate(lines[:300]):
        cols=[v.strip() for v in line.split('\t')]
        if set(required).issubset(cols):
            if len(cols)!=len(set(cols)):
                raise DataError(f'{name}: duplicate column headers')
            header=i
            break
    if header is None:
        raise DataError(f'{name}: required header not found: {required}')
    try:
        # index_col=False keeps a trailing tab on data rows from promoting the first column to an index.
        frame=pd.read_csv(io.StringIO('\n'.join(lines[header:])),sep='\t',dtype=str,index_col=False)
    except pd.errors.ParserError as exc:
        raise DataError(f'{name}: inconsistent tab-separated rows: {exc}') from exc
    frame.columns=[c.strip() for c in frame.columns]
    if frame.empty:
        raise DataError(f'{name}: no data rows')
    info={'encoding':encoding,'header_line_1based':header+1,'warnings':[]}
    if encoding!='utf-8-sig' and lines[0].startswith('EC-Lab') and HANGUL_RE.search('\n'.join(lines[:header+1])):
        info['warnings'].append(f'{name}: EC-Lab header decoded as {encoding} contains Hangul characters; '
                                'the instrument code page may differ (try adding "cp1252" to config encodings)')
    return frame,info

def numeric_hint(value):
    if ',' in value and '.' not in value:
        return '; decimal comma found, export with a dot decimal separator'
    if ':' in value:
        return '; export times in seconds, not h:mm:ss'
    return ''

def require_finite(name,frame,numeric,columns,info,names=None):
    """Name the first nonnumeric/nonfinite value with its column, row and original text."""
    bad=~np.isfinite(numeric[columns].to_numpy(dtype=float))
    if not bad.any():
        return
    row,column=(int(v) for v in np.argwhere(bad)[0])
    label=int(numeric.index[row])
    raw=(names or {}).get(columns[column],columns[column])
    value=str(frame.at[label,raw])
    raise DataError(f'{name}: nonnumeric or nonfinite {raw}={value!r} at data row {label+1} '
                    f'(file line {info["header_line_1based"]+label+1}){numeric_hint(value)}')

def cc_reference_current(current,rows):
    """Plateau current from the first rows of the segment; one overshoot row cannot define it."""
    return float(np.median(current[:max(1,min(int(rows),len(current)))]))

def find_cv_start(frame,tol=.01,reference_rows=5,sustained_rows=3):
    current=np.abs(frame['current'].to_numpy(dtype=float))
    if not len(current) or not np.isfinite(current).all() or current[0]<=0:
        raise DataError('CC/CV detection requires a finite, nonzero first current')
    reference=cc_reference_current(current,reference_rows)
    if reference<=0:
        raise DataError('CC/CV detection requires a positive plateau current')
    below=current<reference*(1-tol)
    for i in np.flatnonzero(below):
        # One noisy row is not a transition: the drop must hold for k rows or to the end of the segment.
        if below[int(i):int(i)+max(1,int(sustained_rows))].all():
            return int(i)
    return None

def trim_boundary_zero_current(segment):
    """Drop only leading/trailing zero-current logging rows that add no capacity."""
    current=segment['current'].to_numpy(); capacity=segment['capacity'].to_numpy()
    head=0
    while head<len(segment)-1 and current[head]==0:
        head+=1
    tail=len(segment)
    while tail-1>head and current[tail-1]==0 and capacity[tail-1]<=capacity[tail-2]+1e-12:
        tail-=1
    removed=[int(v)+1 for v in list(segment.index[:head])+list(segment.index[tail:])]
    return segment.iloc[head:tail],removed

def read_cycle(path,cfg=None):
    cfg=(cfg or Config()).validate()
    name=Path(path).name
    frame,info=read_table(path,CYCLE_COLUMNS,cfg)
    tokens={c:str(frame.iloc[0][c]).strip(' []()').lower() for c in ['|Q|(Ah)','Current(A)']}
    # Remove only a recognized units row, never an arbitrary first observation.
    is_units=tokens['|Q|(Ah)']=='ah' and tokens['Current(A)']=='a'
    if not is_units and all(token.isalpha() for token in tokens.values()):
        raise DataError(f'{name}: units row {list(tokens.values())} not recognized; '
                        'export |Q| in Ah and current in A')
    if is_units:
        frame=frame.iloc[1:].copy()
    if frame.empty:
        raise DataError(f'{name}: no observations after units row')
    numeric=frame[CYCLE_COLUMNS].apply(pd.to_numeric,errors='coerce')
    numeric.columns=[CYCLE_NAMES[c] for c in CYCLE_COLUMNS]
    require_finite(name,frame,numeric,['cycle','step'],info,RAW_NAMES)
    if not np.equal(numeric[['cycle','step']],np.floor(numeric[['cycle','step']])).all().all():
        raise DataError('Cycle/Step numbers must be integers')
    cycle=numeric[numeric['cycle']==cfg.target_cycle].copy()
    if cycle.empty:
        raise DataError(f'{name}: target cycle {cfg.target_cycle} missing')
    # Unused columns and untargeted cycles must not reject a complete target cycle.
    require_finite(name,frame,cycle,['time','capacity','current'],info,RAW_NAMES)
    if (np.diff(cycle['time'].to_numpy())<0).any():
        raise DataError(f'{name}: time is not monotonic in cycle {cfg.target_cycle}; inspect acquisition order')
    cycle['step_i']=(cycle['step'].ne(cycle['step'].shift())).cumsum()-1
    segment=cycle[cycle['step_i']==cfg.target_step_i] if cfg.target_raw_step is None else cycle[cycle['step']==cfg.target_raw_step]
    if segment.empty:
        raise DataError(f'{name}: target segment missing')
    if cfg.target_raw_step is not None and segment['step_i'].nunique()!=1:
        raise DataError('Raw Step No. occurs in multiple segments; use target_step_i')
    trimmed=[]
    if cfg.trim_zero_current_boundary_rows:
        segment,trimmed=trim_boundary_zero_current(segment)
    currents=segment['current'].to_numpy()
    sign=1 if cfg.expected_current_sign=='positive' else -1
    if (sign*currents<=0).any():
        raise DataError('Selected segment current sign/zero does not match configured charging direction')
    capacities=segment['capacity'].to_numpy()
    if (capacities<0).any() or (np.diff(capacities)<-1e-12).any() or capacities[-1]<=0:
        raise DataError('Selected capacity must be nonnegative, monotonic, and end positive')
    magnitude=np.abs(currents)
    reference=cc_reference_current(magnitude,cfg.cc_reference_rows)
    cv=find_cv_start(segment,cfg.cv_relative_drop,cfg.cc_reference_rows,cfg.cc_sustained_rows)
    cap=float(capacities[-1])
    cc=cap if cv is None else float(capacities[cv])
    if not 0<=cc<=cap:
        raise DataError('Invalid CC/total capacity relationship')
    if cc/cap<IMPLAUSIBLE_CC_FRACTION:
        info['warnings'].append(f'{name}: cc_frac={cc/cap:.3f} is implausibly low for a CC-CV charge; '
                                'verify the selected segment, current noise and cv_relative_drop')
    following=cycle[cycle['step_i']==int(segment['step_i'].iloc[0])+1]
    gap=abs(float(following['voltage'].iloc[0])-float(segment['voltage'].iloc[-1])) if len(following) else np.inf
    if len(following) and sign*following['current'].iloc[0]>0 and np.isfinite(gap) and gap<=SAME_VOLTAGE_V:
        info['next_segment_continues_charge']=True
        info['warnings'].append(f'{name}: the next segment continues charging at the same voltage; '
                                'CC and CV may be separate Step No. and cap would then exclude the CV charge')
    pressure=re.search(r'_(\d+(?:\.\d+)?)MPa',name,re.I)
    info.update(units_row_removed=bool(is_units),raw_step=float(segment['step'].iloc[0]),
                step_i=int(segment['step_i'].iloc[0]),segment_rows=len(segment),
                cv_first_below_index=cv,cc_definition='capacity through the first sustained below-threshold current row',
                cc_reference_current_a=reference,cc_sustained_rows=cfg.cc_sustained_rows,
                cc_plateau_max_relative_deviation=float(np.max(np.abs(magnitude-reference))/reference),
                boundary_zero_current_rows_removed=trimmed,initial_capacity_ah=float(capacities[0]))
    return {'cell_number':cell_id(path),'pressure_mpa':float(pressure.group(1)) if pressure else None,
            'cap':cap,'cap_cc':cc,'cap_cv':cap-cc,'cc_frac':cc/cap},info

def sweep_labels(frame,spec):
    """Separate stacked sweeps by the EC-Lab cycle number, else by a repeated frequency."""
    if 'cycle number' in frame:
        numbers=pd.to_numeric(frame['cycle number'],errors='coerce').to_numpy()
        if len(numbers)==len(spec) and np.isfinite(numbers).all():
            order={value:index for index,value in enumerate(dict.fromkeys(numbers.tolist()))}
            return np.asarray([order[value] for value in numbers.tolist()],dtype=int)
    labels=[]; seen=set(); index=0
    for frequency in spec['f'].tolist():
        if frequency in seen:
            index+=1; seen={frequency}
        else:
            seen.add(frequency)
        labels.append(index)
    return np.asarray(labels,dtype=int)

def convert_mpt(path,cfg=None):
    cfg=(cfg or Config()).validate()
    name=Path(path).name
    frame,info=read_table(path,EIS_COLUMNS,cfg)
    numeric=frame[EIS_COLUMNS].apply(pd.to_numeric,errors='coerce')
    require_finite(name,frame,numeric,EIS_COLUMNS,info)
    if (numeric['freq/Hz']<=0).any():
        raise DataError(f'{name}: EIS frequency must be greater than zero')
    spec=pd.DataFrame({'f':numeric.iloc[:,0],'re':numeric.iloc[:,1],'im':-numeric.iloc[:,2]})
    if '<Ewe>/V' in frame:
        ocv=pd.to_numeric(frame['<Ewe>/V'],errors='coerce')
        if cfg.use_ocv and not np.isfinite(ocv).all():
            raise DataError(f'{name}: missing/nonfinite EIS potential')
        spec['ocv']=ocv
    elif cfg.use_ocv:
        raise DataError(f'{name}: <Ewe>/V missing; set use_ocv=false for an EIS-only analysis')
    if '|Z|/Ohm' in frame:
        mag=pd.to_numeric(frame['|Z|/Ohm'],errors='coerce').to_numpy()
        expected=np.hypot(spec['re'],spec['im']).to_numpy()
        info['raw_magnitude_max_abs_difference_ohm']=float(np.max(np.abs(mag-expected))) if np.isfinite(mag).all() else None
    labels=sweep_labels(frame,spec)
    info['eis_sweeps']=count=int(labels.max())+1
    if count>1:
        if 'ocv' in spec and np.isfinite(spec['ocv']).all():
            info['sweep_ocv_median_v']=[float(np.median(spec['ocv'].to_numpy()[labels==k])) for k in range(count)]
        if cfg.eis_sweep=='all':
            info['warnings'].append(f'{name}: {count} EIS sweeps are stacked in one file; set eis_sweep to '
                                    '"first", "last" or an index so that one measured state is analysed')
        else:
            index=0 if cfg.eis_sweep=='first' else count-1 if cfg.eis_sweep=='last' else int(cfg.eis_sweep)
            if not 0<=index<count:
                raise DataError(f'{name}: eis_sweep={cfg.eis_sweep} is outside the {count} sweeps in this file')
            spec=spec[labels==index].reset_index(drop=True)
            info['selected_sweep']=index
    info['raw_rows']=len(spec)
    return spec,info

def build_features(spectrum,cfg):
    df=spectrum.copy()
    if not len(df) or not np.isfinite(df[['f','re','im']]).all().all() or (df['f']<=0).any():
        raise DataError('Invalid EIS spectrum')
    duplicates=int(df['f'].duplicated().sum())
    if duplicates:
        if cfg.duplicate_frequency_policy=='error':
            raise DataError(f'Duplicate EIS frequencies ({duplicates} rows); select one sweep with eis_sweep, '
                            'split the file, or set duplicate_frequency_policy="mean" for repeats of one state')
        if cfg.mean_max_ewe_spread_v is not None and 'ocv' in df and np.isfinite(df['ocv']).all():
            spread=float(df.groupby('f')['ocv'].agg(lambda s:s.max()-s.min()).max())
            if spread>cfg.mean_max_ewe_spread_v:
                raise DataError(f'Duplicate frequencies span {spread:.4g} V of EIS potential, above '
                                f'mean_max_ewe_spread_v={cfg.mean_max_ewe_spread_v:g}; averaging different '
                                'states is not physical, select one sweep with eis_sweep')
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
            raise DataError(f'Configured frequencies {grid[outside].tolist()} exceed measured support '
                            f'[{low}, {high}] by up to {np.max(fraction):.3e} relative; move the grid endpoint '
                            'inside the measured range, or set boundary_policy="clamp" with '
                            'max_boundary_fraction just above that value')
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
        reason=f'outside configured cell range {cfg.cell_min}..{cfg.cell_max}'
    elif str(cell) in cfg.exclude_cells:
        reason=cfg.exclude_cells[str(cell)]
    # One exclusion event per cell, even when the cell appears in several input directories.
    if reason and not any(e.get('cell_number')==cell and e.get('status')=='excluded' for e in events):
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

def has_eis_header(path,cfg):
    try:
        read_table(path,EIS_COLUMNS,cfg)
    except DataError:
        return False
    return True

def manifest_integer(value,column):
    text=str(value).strip()
    number=pd.to_numeric(text,errors='coerce')
    if not np.isfinite(number) or number!=int(number):
        raise DataError(f'Manifest {column} must be an integer: {text!r}')
    return int(number)

def single_file(cell,paths,suffix,cfg,events):
    if len(paths)>1 and suffix=='.mpt':
        # EC-Lab writes one file per technique; a file without EIS columns is not a spectrum.
        keep=[p for p in paths if has_eis_header(p,cfg)]
        if keep and len(keep)<len(paths):
            events.extend({'cell_number':cell,'status':'skipped_non_eis_file','file':p.name}
                          for p in paths if p not in keep)
            paths=keep
    if len(paths)>1:
        raise DataError(f'Duplicate cell {cell}: {", ".join(p.name for p in paths)}; provide a selection manifest')
    return paths[0]

def load_raw(cycle_dir,eis_dir,cfg,events,manifest=None):
    pairs=[]
    if manifest:
        m,encoding=read_csv_any(manifest,cfg,dtype=str,keep_default_na=False)
        events.append({'status':'selection_manifest','file':Path(manifest).name,'encoding':encoding,'rows':len(m)})
        required={'cell_number','eis_file'}|({'cycle_file'} if cycle_dir else set())
        if not required.issubset(m):
            raise DataError(f'Manifest requires {sorted(required)}')
        records=[(manifest_integer(row['cell_number'],'cell_number'),row) for row in m.to_dict('records')]
        if len({cell for cell,_ in records})!=len(records):
            raise DataError('Manifest must select exactly one measurement per cell')
        for cell,row in records:
            if not included(cell,cfg,events):
                continue
            paths={}
            for key,directory in [('eis_file',eis_dir),('cycle_file',cycle_dir)]:
                if directory:
                    value=str(row[key]).strip()
                    if not value:
                        raise DataError(f'Manifest cell {cell}: {key} is empty')
                    base=Path(directory).resolve()
                    p=(base/value).resolve()
                    if not p.is_relative_to(base) or not p.is_file():
                        raise DataError(f'Manifest path missing or outside input directory: {value}')
                    if cell_id(p)!=cell:
                        raise DataError(f'Manifest and filename cell IDs disagree: {p.name}')
                    paths[key]=p
            group=str(row.get(cfg.group_column,'')).strip() or None
            pairs.append((cell,paths.get('cycle_file'),paths['eis_file'],group))
    else:
        maps=[]
        for directory,suffix in [(cycle_dir,'.txt'),(eis_dir,'.mpt')]:
            candidates={}
            if directory:
                for p in inventory(directory,suffix):
                    cell=cell_id(p)
                    if not included(cell,cfg,events):
                        continue
                    candidates.setdefault(cell,[]).append(p)
            maps.append({cell:single_file(cell,paths,suffix,cfg,events) for cell,paths in candidates.items()})
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
                target,cycle_detail=read_cycle(cycle_path,cfg)
                row.update(target)
                event['cycle_reader']=cycle_detail
            spec,detail=convert_mpt(eis_path,cfg)
            features,feature_detail=build_features(spec,cfg)
        except Exception as exc:
            event.update(status='failed',error=str(exc),error_type=type(exc).__name__)
            raise DataError(f'Cell {cell}: {exc}') from exc
        row.update(features)
        if group is not None and pd.notna(group):
            row[cfg.group_column]=group
        event.update(status='included',eis_reader=detail,feature_processing=feature_detail)
        for reader in [event.get('cycle_reader'),detail]:
            events.extend({'cell_number':cell,'status':'warning','reason':message}
                          for message in (reader or {}).get('warnings',[]))
        rows.append(row)
    return pd.DataFrame(rows).sort_values('cell_number').reset_index(drop=True)

def feature_frequency(name,text):
    try:
        frequency=float(text)
    except ValueError:
        raise DataError(f'Invalid feature frequency: {name}') from None
    if not np.isfinite(frequency) or frequency<=0:
        raise DataError(f'Invalid feature frequency: {name}')
    return frequency

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
        raise DataError(f'No rows remain after exclusions (cell_min={cfg.cell_min}, cell_max={cfg.cell_max}, '
                        f'{len(cfg.exclude_cells)} exclude_cells; input cell_number '
                        f'{int(ids.min())}..{int(ids.max())})')
    features=[]; other=[]
    for name in df.columns:
        match=FEATURE_RE.fullmatch(name)
        if not match:
            loose=FEATURE_ANY_RE.fullmatch(name)
            if loose:
                canonical=f'{loose.group(1).lower()}@{feature_frequency(name,loose.group(2)):g}Hz'
                raise DataError(f'Use canonical feature name {canonical}, not {name}')
            if name.lower().startswith(('mag@','re@','im@','phase@')):
                raise DataError(f'Invalid EIS feature name: {name}; example mag@1000Hz')
            other.append(name)
            continue
        canonical=f'{match.group(1)}@{feature_frequency(name,match.group(2)):g}Hz'
        if canonical!=name:
            raise DataError(f'Use canonical feature name {canonical}, not {name}')
        features.append(name)
    if not features:
        raise DataError('No EIS feature columns (example mag@1000Hz)')
    if cfg.use_ocv:
        if 'ocv' not in df:
            raise DataError('ocv required; set use_ocv=false for EIS-only analysis')
        features.append('ocv')
    ignored=[c for c in other if c not in {'cell_number','cap','cap_cc','cap_cv','cc_frac','ocv',
                                           'pressure_mpa',cfg.group_column}]
    if ignored:
        events.append({'status':'ignored_columns','columns':ignored,
                       'reason':'not EIS features or recognized targets; kept as metadata only'})
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
        median=float(df['cap'].median())
        if not cfg.design_capacity_ah/cfg.cap_plausibility_factor<=median<=cfg.design_capacity_ah*cfg.cap_plausibility_factor:
            raise DataError(f'cap must be in Ah: median {median:.6g} Ah differs from design_capacity_ah '
                            f'{cfg.design_capacity_ah:.6g} Ah by more than the allowed factor '
                            f'{cfg.cap_plausibility_factor:g}; check for mAh values or another unit error')
        excess=df.loc[df['cap']>CAP_EXCESS_FACTOR*cfg.design_capacity_ah]
        events.extend({'cell_number':int(c),'status':'warning',
                       'reason':f'cap {v:.6g} Ah exceeds {CAP_EXCESS_FACTOR:g} x design_capacity_ah '
                                f'{cfg.design_capacity_ah:.6g} Ah; verify units, irreversible first-charge '
                                'capacity or a soft short'}
                      for c,v in zip(excess['cell_number'],excess['cap']))
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

def write_audit(path,record,events):
    try:
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        write_json(path,{**record,'events':events})
    except OSError:
        pass

def main(argv=None):
    parser=argparse.ArgumentParser(description='Prepare validated EIS/capacity features without model fitting')
    parser.add_argument('--config')
    parser.add_argument('--cycle-dir')
    parser.add_argument('--eis-dir',required=True)
    parser.add_argument('--selection-manifest')
    parser.add_argument('--output',required=True,help='New CSV file')
    args=parser.parse_args(argv)
    output=Path(args.output)
    audit=output.with_suffix('.audit.json')
    if output.exists() or audit.exists():
        parser.error('Output already exists; choose a new path')
    events=[]
    record={'version':VERSION,'status':'failed','cycle_dir':args.cycle_dir,'eis_dir':args.eis_dir}
    try:
        cfg=load_config(args.config)
        record['config']=config_dict(cfg)
        if args.selection_manifest:
            record['selection_manifest']={'file':Path(args.selection_manifest).name,
                                          'sha256':digest(args.selection_manifest)}
        df=load_raw(args.cycle_dir,args.eis_dir,cfg,events,args.selection_manifest)
        df,_=validate_frame(df,cfg,events,training=bool(args.cycle_dir))
        output.parent.mkdir(parents=True,exist_ok=True)
        df.to_csv(output,index=False,encoding='utf-8-sig')
        record.update(status='completed',cells=len(df))
    except (DataError,ValueError,TypeError,KeyError,OSError) as exc:
        # Configuration, manifest and encoding failures share one contract: exit 2 and keep the audit.
        record.update(error_type=type(exc).__name__,error=str(exc))
        write_audit(audit,record,events)
        parser.exit(2,f'Input error: {exc}\n')
    write_audit(audit,record,events)
    print(f'Prepared {len(df)} cells: {output}')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
