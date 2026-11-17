"""Offline RT30 and REG 15-5b numeric guards; no engine or certificate.

PASS is a numeric result only. Run/file bindings, technical/reset gates,
grammar qualification and certificate publication remain separate.
"""
import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
from pathlib import Path
import re
import struct

ID_MAX = 2**53
REL = 1e-5
MIN_CELL_PAIRS = 100
GLOBAL_LIMIT, CELL_LIMIT = .05, .5
NUMBER = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z')
LAYOUTS = {'rt30': (30, 'c_ul_ph'), 'legacy26': (26, 'c_cpl')}


def _finite(token):
    if not NUMBER.fullmatch(token):
        raise ValueError('non-numeric token')
    value = float(token)
    if not math.isfinite(value):
        raise ValueError('non-finite value')
    return value


def _id(token):
    value = Decimal(token)
    if not value.is_finite() or not 0 < value <= ID_MAX or value != value.to_integral_value():
        raise ValueError('ID outside exact positive integer range')
    return int(value)


def project_legacy(values):
    return values[:21] + values[25:]


def _indices(layout):
    return list(range(6)) + list(range(9,18)) + list(range(21,LAYOUTS[layout][0]))


def _periodic(layout):
    cp = 27 if layout == 'rt30' else 23
    return {0:0, 1:1, 3:0, 4:1, cp:0, cp+1:1}


def _canonical(values, layout):
    values = values.copy()
    if values[6] > values[7]:
        values[:6] = values[3:6] + values[:3]
        values[6], values[7] = values[7], values[6]
        for i in list(range(9,18)) + ([22,23,24] if layout == 'rt30' else []):
            values[i] = -values[i]
    return values


def _values(values, layout, box):
    periodic = _periodic(layout)
    return [values[i] % box[periodic[i]] if i in periodic else values[i] for i in _indices(layout)]


def read_contacts(path, layout='rt30', box=(.05,.05)):
    if layout not in LAYOUTS:
        raise ValueError('unknown layout')
    if len(box) != 2 or any(not math.isfinite(x) or x <= 0 for x in box):
        raise ValueError('invalid periodic lengths')
    report = {'status':'NOT_COMPUTED', 'rows':{}, 'n_dup_consistent':0}
    try:
        path = Path(path)
        before = path.stat()
        raw = path.read_bytes()
        after = path.stat()
        if (before.st_size,before.st_mtime_ns,before.st_ino) != (after.st_size,after.st_mtime_ns,after.st_ino):
            report['reason'] = 'input changed during read'
            return report
        lines = raw.decode('ascii').splitlines()
    except FileNotFoundError:
        report['reason'] = 'input absent'
        return report
    except (OSError,UnicodeError,TypeError):
        report.update(status='FAIL',reason='input unreadable or undecodable')
        return report
    report['sha256'] = hashlib.sha256(raw).hexdigest()
    n, prefix = LAYOUTS[layout]
    expected = [f'{prefix}[{i}]' for i in range(1,n+1)]
    headers = [line.split()[2:] for line in lines if line.startswith('ITEM: ENTRIES ')]
    if not headers:
        report.update(status='FAIL',reason='entry header absent or malformed')
        return report
    if not set(expected).issubset(headers[0]):
        report['reason'] = 'required columns absent'
        return report
    try:
        if len(headers) != 1 or len(lines) < 9 or lines[0] != 'ITEM: TIMESTEP' or lines[2] != 'ITEM: NUMBER OF ENTRIES':
            raise ValueError('single-frame header required')
        if not re.fullmatch(r'[0-9]+',lines[1]) or not re.fullmatch(r'[0-9]+',lines[3]):
            raise ValueError('invalid timestep or count')
        if lines[8] != 'ITEM: ENTRIES ' + ' '.join(expected):
            raise ValueError('column order, duplicate or extra column')
        flags = lines[4].split()
        if flags[:3] != ['ITEM:','BOX','BOUNDS'] or len(flags) != 6 or any(not re.fullmatch('[pfsm]{2}',x) for x in flags[3:]):
            raise ValueError('orthogonal box header required')
        bounds = [tuple(_finite(x) for x in line.split()) for line in lines[5:8]]
        if any(len(b) != 2 or b[1] <= b[0] or not math.isfinite(b[1]-b[0]) for b in bounds):
            raise ValueError('invalid bounds')
        data = [line for line in lines[9:] if line.strip()]
        if len(data) != int(lines[3]):
            raise ValueError('entry count mismatch')
        rows, duplicates = {}, 0
        for line in data:
            tokens = line.split()
            if len(tokens) != n:
                raise ValueError('row width mismatch')
            values = [_finite(x) for x in tokens]
            values[6],values[7] = _id(tokens[6]),_id(tokens[7])
            if values[6] == values[7]:
                raise ValueError('self pair')
            values = _canonical(values,layout)
            key = (values[6],values[7])
            if key in rows:
                a,b = _values(rows[key],layout,box),_values(values,layout,box)
                if any(abs(x-y) > 1e-12*max(1.,abs(x)) for x,y in zip(a,b)):
                    raise ValueError('conflicting duplicate')
                duplicates += 1
            else:
                rows[key] = values
        report.update(status='PASS',rows=rows,step=int(lines[1]),bounds=bounds,n_dup_consistent=duplicates)
    except (ValueError,InvalidOperation,OverflowError):
        report.update(status='FAIL',reason='malformed dump or conflicting duplicate')
    return report


def _inputs(test,original,test_layout,original_layout,step,box):
    result = {'status':'FAIL','physical_qualification':False,'scope':'offline numeric only'}
    if type(step) is not int or step < 0:
        result['reason'] = 'explicit nonnegative expected step required'
        return result,None,None
    o,t = read_contacts(original,original_layout,box),read_contacts(test,test_layout,box)
    result.update(input_status=[o['status'],t['status']],input_sha256=[o.get('sha256'),t.get('sha256')])
    if 'FAIL' in result['input_status']:
        result['reason'] = 'invalid input'
        return result,None,None
    if 'NOT_COMPUTED' in result['input_status']:
        result.update(status='NOT_COMPUTED',reason='required input unavailable')
        return result,None,None
    if o['step'] != step or t['step'] != step:
        result['reason'] = 'step mismatch'
        return result,None,None
    ok,tk = o['rows'].keys(),t['rows'].keys()
    result.update(n_orig=len(ok),n_test=len(tk),n_common=len(ok & tk),
                  missing_pairs=[list(k) for k in sorted(ok-tk)],extra_pairs=[list(k) for k in sorted(tk-ok)],
                  n_dup_consistent=o['n_dup_consistent']+t['n_dup_consistent'])
    if not ok and not tk:
        result.update(status='NOT_COMPUTED',reason='both pair sets empty')
        return result,None,None
    return result,o,t


def _median(values):
    values = sorted(values)
    n = len(values)
    return values[n//2] if n%2 else values[n//2-1]/2 + values[n//2]/2


def g2cp_compare(test,original,*,expected_step,box=(.05,.05)):
    result,original,test = _inputs(test,original,'rt30','rt30',expected_step,box)
    if original is None:
        return result
    o,t = original['rows'],test['rows']
    indices = _indices('rt30')
    ov,tv = ({k:_values(v,'rt30',box) for k,v in rows.items()} for rows in (o,t))
    medians = [_median([abs(v[j]) for v in ov.values()]) for j in range(len(indices))] if o else []
    mismatches,exact = [0]*len(indices),0
    max_relative = [0.]*len(indices)
    bitwise,full30 = 0,0
    for key in sorted(o.keys() & t.keys()):
        a,b = ov[key],tv[key]
        exact += a == b
        bitwise += struct.pack('!24d',*a)==struct.pack('!24d',*b)
        full30 += struct.pack('!30d',*o[key])==struct.pack('!30d',*t[key])
        for j,col in enumerate(indices):
            delta = abs(b[j]-a[j])
            if col in _periodic('rt30'):
                delta = min(delta,box[_periodic('rt30')[col]]-delta)
            floor = max(abs(a[j]),medians[j])
            relative = delta/floor if floor else (0. if delta==0 else math.inf)
            max_relative[j] = max(max_relative[j],relative)
            if delta > REL*floor:
                mismatches[j] += 1
    result.update(status='FAIL' if o.keys()!=t.keys() or any(mismatches) else 'PASS',
                  compared_columns=[i+1 for i in indices],mismatch_counts=mismatches,n_exact_compared_pairs=exact,
                  n_bitwise_compared_pairs=bitwise,n_bitwise_full30_pairs=full30,
                  max_relative_difference=[x if math.isfinite(x) else None for x in max_relative],
                  unbounded_relative_columns=[indices[j]+1 for j,x in enumerate(max_relative) if not math.isfinite(x)],
                  input_bytes_equal=result['input_sha256'][0]==result['input_sha256'][1],
                  exact_metric='canonical selected float values; not whole-file bit identity',
                  discriminating_frac=sum(any(v[i]!=0 for i in range(15,18)) for v in o.values())/len(o) if o else None,
                  shear_nonzero_frac=sum(any(v[i]!=0 for i in (22,23,24)) for v in o.values())/len(o) if o else None,
                  periodic_flag_pairs=[sum(v[8]!=0 for v in rows.values()) for rows in (o,t)])
    return result


def grid_evidence(text,expected_grid,expected_np):
    active = [line.split('#',1)[0].strip() for line in text.splitlines()]
    grids = re.findall(r'^\s*(\d+) by (\d+) by (\d+) MPI processor grid\s*$','\n'.join(active),re.M)
    procs = re.findall(r'\bon (\d+) procs\b','\n'.join(active))
    valid = (isinstance(expected_grid,(tuple,list)) and len(expected_grid)==3
             and all(type(v) is int and v>0 for v in expected_grid)
             and type(expected_np) is int and expected_np>0
             and expected_grid[2]==1 and math.prod(expected_grid)==expected_np)
    balance = False
    for line in active:
        words = line.split()
        if words and (words[0]=='balance' or (len(words)>3 and words[0]=='fix' and words[3]=='balance')):
            balance = True
    if not valid or len(grids)!=1 or tuple(map(int,grids[0]))!=tuple(expected_grid) or not procs or any(int(n)!=expected_np for n in procs) or balance:
        return {'status':'NOT_COMPUTED','reason':'written grid/procs ambiguous, unsupported or balancing active'}
    return {'status':'PASS','grid':list(expected_grid)}


def _metrics(keys,original,test):
    loaded = [k for k in keys if any(original[k][i]!=0 for i in (15,16,17))]
    result = {'n_loaded':len(loaded),'n_reset_like':0,'W':None,'reset_frac':None,
              'r_median':None,'r_q95':None,'collapse_frac':None}
    if not loaded:
        return result
    scale = max(abs(original[k][i]) for k in loaded for i in (15,16,17))
    weights,losses,ratios,collapses = [],[],[],0
    for k in loaded:
        o,t = original[k][15:18],test[k][15:18]
        weight = math.hypot(*(x/scale for x in o))
        common_scale = max(abs(x) for x in o+t)
        on = math.hypot(*(x/common_scale for x in o))
        delta = math.hypot(*(b/common_scale-a/common_scale for a,b in zip(o,t)))
        ratio = delta/on if on else math.inf
        weights.append(weight)
        if delta > .5*on:
            losses.append(weight)
        ratios.append(ratio)
        collapses += math.hypot(*(x/common_scale for x in t)) < .5*on
    if any(w==0 for w in weights):
        result['reason'] = 'positive reference weight underflow; needs extended arithmetic'
        return result
    ratios.sort()
    median,q95 = _median(ratios),ratios[math.ceil(.95*len(ratios))-1]
    result.update(n_reset_like=len(losses),W=math.fsum(losses)/math.fsum(weights),
                  reset_frac=len(losses)/len(loaded),r_median=median if math.isfinite(median) else None,
                  r_q95=q95 if math.isfinite(q95) else None,r_nonfinite=sum(not math.isfinite(x) for x in ratios),
                  collapse_frac=collapses/len(loaded))
    return result


def _cell(position,bounds,p,q):
    cell = []
    for x,(lo,hi),n in zip(position,bounds,(p,q)):
        length,offset = hi-lo,x-lo
        if not math.isfinite(offset):
            return None
        wrapped = offset%length
        width = length/n
        if abs(wrapped-round(wrapped/width)*width) <= 1e-12*length:
            return None
        cell.append(min(n-1,int(wrapped/width)))
    return tuple(cell)


def cont_guard(test,original,*,expected_step,grid_text,expected_grid,expected_np,test_layout='legacy26',box=(.05,.05)):
    result,original,test = _inputs(test,original,test_layout,'legacy26',expected_step,box)
    if original is None:
        return result
    o,t = original['rows'],test['rows']
    keys = sorted(o.keys() & t.keys())
    result.update(_metrics(keys,o,t))
    failure = o.keys()!=t.keys() or (result['W'] is not None and result['W']>GLOBAL_LIMIT)
    unknown = result['W'] is None
    grid = grid_evidence(grid_text,expected_grid,expected_np)
    result.update(grid_evidence=grid,cells=[],n_ambiguous_atoms=0,n_cross_cell_pairs=0,
                  limits={'global_W':GLOBAL_LIMIT,'cell_W':CELL_LIMIT,'cell_minimum':MIN_CELL_PAIRS})
    if grid['status']!='PASS':
        unknown = True
    else:
        p,q,_ = grid['grid']
        cells = {(ix,iy):[] for ix in range(p) for iy in range(q)}
        ambiguous = set()
        for k in keys:
            v = o[k]
            a,b = _cell(v[0:2],original['bounds'],p,q),_cell(v[3:5],original['bounds'],p,q)
            if a is None: ambiguous.add(k[0])
            if b is None: ambiguous.add(k[1])
            if a is not None and b is not None:
                if a==b: cells[a].append(k)
                else: result['n_cross_cell_pairs'] += 1
        result['n_ambiguous_atoms'] = len(ambiguous)
        for index,members in cells.items():
            metrics = _metrics(members,o,t)
            metrics['index'] = list(index)
            result['cells'].append(metrics)
            if metrics['n_loaded']<MIN_CELL_PAIRS or metrics['W'] is None:
                unknown = True
            elif metrics['W']>CELL_LIMIT:
                failure = True
    result['status'] = 'FAIL' if failure else 'NOT_COMPUTED' if unknown else 'PASS'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['roundtrip','continuity'])
    parser.add_argument('test',type=Path)
    parser.add_argument('original',type=Path)
    parser.add_argument('--step',type=int,required=True)
    parser.add_argument('--grid-log',type=Path)
    parser.add_argument('--grid',type=int,nargs=3)
    parser.add_argument('--np',type=int)
    parser.add_argument('--rt30',action='store_true')
    args = parser.parse_args()
    if args.mode=='roundtrip':
        result = g2cp_compare(args.test,args.original,expected_step=args.step)
    else:
        try: text = args.grid_log.read_text(encoding='utf8') if args.grid_log else ''
        except (OSError,UnicodeError): text = ''
        result = cont_guard(args.test,args.original,expected_step=args.step,grid_text=text,
                            expected_grid=args.grid,expected_np=args.np,test_layout='rt30' if args.rt30 else 'legacy26')
    print(json.dumps(result,indent=2,allow_nan=False))
    return 0 if result['status']=='PASS' else 2


if __name__=='__main__':
    raise SystemExit(main())
