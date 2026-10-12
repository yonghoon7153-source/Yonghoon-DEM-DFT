"""Codex 탐침 출력 ↔ 우리 트리 재실행 출력 대조 (ps45 σ_e 보고 기준 검토 · 10-13).

    python3 -I compare_probe_outputs.py <out.json> <Codex JSON>=<우리 JSON> [<Codex JSON>=<우리 JSON> …]
    python3 -I compare_probe_outputs.py --selftest

JSON 을 평탄화해 키별로 비교한다.  같지 않은 값은 다섯으로 나눈다:
  env    — 키의 마지막 이름이 실행 환경 (python · numpy · scipy · networkx) — 이름으로만 고른다 (값 모양으로 고르지 않는다)
  path   — 둘 다 문자열이고 ① 둘 다 작업 경로 (윈도 드라이브 · /tmp/ · /home/) 가 들어 있거나 ② 경로 구분자 (\\ ↔ /) 만 다름 = 환경 차이
  resid  — 키의 마지막 이름이 반올림 오차 측정 (conservation_rel · residual_rel · linear_relative_error) 이고 양쪽 |값| ≤ 1e-12
           (기계 정밀도 잔차 — 판정은 1e-6 문턱 · 이 범위의 끝자리는 BLAS · SciPy 판에 따라 다르다)
  float  — 둘 다 실수 (bool 제외) · 상대 차 ≤ 1e-12 (0 근처는 절대 ≤ 1e-15)
  other  — 나머지 (+ 한쪽에만 있는 키) = **판정값 차이** — 0 이어야 같은 판정 (rc 0)
NaN 은 둘 다 NaN 일 때만 같다.  True ↔ 1 · False ↔ 0 은 다르다 (파이썬 == 가 같다고 하는 것을 막는다).
"""
import json
import math
import re
import sys

ENV_KEYS = ('python', 'numpy', 'scipy', 'networkx')
RESID_KEYS = ('conservation_rel', 'residual_rel', 'linear_relative_error')
RESID_MAX = 1e-12
PATHY = re.compile(r'([A-Za-z]:\\|\\\\|/tmp/|/home/|/root/|/Users/)')
REL_TOL = 1e-12
ABS_TOL = 1e-15


def flat(x, p=''):
    o = {}
    if isinstance(x, dict):
        if not x:
            o[p] = {}
        for k, v in x.items():
            o.update(flat(v, f'{p}.{k}' if p else str(k)))
    elif isinstance(x, list):
        if not x:
            o[p] = []
        for i, v in enumerate(x):
            o.update(flat(v, f'{p}[{i}]'))
    else:
        o[p] = x
    return o


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _same(va, vb):
    """정확히 같은가 — 타입까지 (bool ↔ int 구분 · NaN 은 NaN 끼리만)."""
    if isinstance(va, bool) or isinstance(vb, bool):
        return isinstance(va, bool) and isinstance(vb, bool) and va == vb
    if _is_num(va) and _is_num(vb):
        fa, fb = float(va), float(vb)
        if math.isnan(fa) or math.isnan(fb):
            return math.isnan(fa) and math.isnan(fb)
        return fa == fb
    return type(va) is type(vb) and va == vb


def classify(key, va, vb):
    if _same(va, vb):
        return 'equal'
    last = re.split(r'[.\[]', key)[-1]
    if last in ENV_KEYS:
        return 'env'
    if isinstance(va, str) and isinstance(vb, str):
        if PATHY.search(va) and PATHY.search(vb):
            return 'path'
        if '\\' in (va + vb) and va.replace('\\', '/') == vb.replace('\\', '/'):
            return 'path'
    if last in RESID_KEYS and _is_num(va) and _is_num(vb):
        fa, fb = float(va), float(vb)
        if all(math.isfinite(x) and abs(x) <= RESID_MAX for x in (fa, fb)):
            return 'resid'
    if _is_num(va) and _is_num(vb):
        fa, fb = float(va), float(vb)
        if not (math.isnan(fa) or math.isnan(fb) or math.isinf(fa) or math.isinf(fb)):
            if abs(fa - fb) <= max(REL_TOL * max(abs(fa), abs(fb)), ABS_TOL):
                return 'float'
    return 'other'


def compare(a, b):
    fa, fb = flat(a), flat(b)
    cat = {'equal': 0, 'env': [], 'path': [], 'resid': [], 'float': [], 'other': []}
    for k in sorted(set(fa) | set(fb)):
        if k not in fa or k not in fb:
            cat['other'].append({'key': k, 'codex': fa.get(k, '<없음>'), 'ours': fb.get(k, '<없음>')})
            continue
        c = classify(k, fa[k], fb[k])
        if c == 'equal':
            cat['equal'] += 1
        else:
            item = {'key': k, 'codex': fa[k], 'ours': fb[k]}
            if c == 'float':
                item['rel'] = abs(float(fa[k]) - float(fb[k])) / max(abs(float(fa[k])), abs(float(fb[k])), ABS_TOL)
            cat[c].append(item)
    cat['n_keys_codex'], cat['n_keys_ours'] = len(fa), len(fb)
    return cat


def _selftest():
    ok, bad = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(name)

    base = {'python': '3.12.1', 'numpy': '2.3.5', 'checks': [{'edges_equal': True, 'q': 0.25, 'n': 3,
            'status': 'computed', 'path': 'C:\\work\\x.json'}], 'ratio': 4.375, 'nan': float('nan')}

    def mut(f):
        import copy
        d = copy.deepcopy(base)
        f(d)
        return compare(base, d)

    r = compare(base, base)
    chk('① 같은 입력 = other 0 · equal = 키 수', not r['other'] and r['equal'] == r['n_keys_codex'] == 9)
    r = mut(lambda d: d['checks'][0].__setitem__('edges_equal', False))
    chk('② 판정 bool 뒤집힘 = other 1', len(r['other']) == 1)
    r = mut(lambda d: d.__setitem__('ratio', 4.375 * (1 + 1e-9)))
    chk('③ 상대 1e-9 수치 차 = other (허용 아님)', len(r['other']) == 1 and not r['float'])
    r = mut(lambda d: d.__setitem__('ratio', 4.375 * (1 + 1e-15)))
    chk('④ 상대 1e-15 = float · other 0', len(r['float']) == 1 and not r['other'])
    r = mut(lambda d: d['checks'][0].pop('q'))
    chk('⑤ 우리 쪽 키 결손 = other', len(r['other']) == 1 and r['other'][0]['ours'] == '<없음>')
    r = mut(lambda d: d.__setitem__('python', '3.11.15'))
    chk('⑥ 실행 환경 키 (python) = env · other 0', len(r['env']) == 1 and not r['other'])
    r = mut(lambda d: d['checks'][0].__setitem__('path', '/tmp/r/x.json'))
    chk('⑦ 작업 경로 문자열 = path · other 0', len(r['path']) == 1 and not r['other'])
    r = mut(lambda d: d['checks'][0].__setitem__('edges_equal', 1))
    chk('⑧ True ↔ 1 = other (bool ≠ int)', len(r['other']) == 1)
    r = mut(lambda d: d['checks'][0].__setitem__('status', 'failed'))
    chk('⑨ 상태 문자열 차 = other', len(r['other']) == 1)
    r = mut(lambda d: d['checks'].append({'edges_equal': True}))
    chk('⑩ 목록 길이 차 = other', len(r['other']) >= 1)
    r = mut(lambda d: d.__setitem__('nan', 1.0))
    chk('⑪ NaN ↔ 수 = other · NaN ↔ NaN = 같음', len(r['other']) == 1 and not compare(base, base)['other'])
    r = mut(lambda d: d['checks'][0].__setitem__('status', '/home/x'))
    chk('⑫ 한쪽만 경로 꼴 = other (둘 다 경로일 때만 path)', len(r['other']) == 1)
    r = mut(lambda d: d['checks'][0].__setitem__('n', '3'))
    chk('⑬ 수 ↔ 같은 글자 문자열 = other', len(r['other']) == 1)
    r = mut(lambda d: d.__setitem__('numpy_version_like', '2.4.6'))
    chk('⑭ env 는 키 이름으로만 — 새 키 (값이 버전 꼴) = other', len(r['other']) == 1)
    rel_a, rel_b = {'deck': 'dem_scripts\\x\\in.a.liggghts'}, {'deck': 'dem_scripts/x/in.a.liggghts'}
    r = compare(rel_a, rel_b)
    chk('⑮ 상대 경로 구분자만 다름 (\\ ↔ /) = path · other 0', len(r['path']) == 1 and not r['other'])
    r = compare(rel_a, {'deck': 'dem_scripts/x/in.b.liggghts'})
    chk('⑯ 구분자를 맞춰도 다른 경로 = other', len(r['other']) == 1)
    ra, rb = {'c': {'conservation_rel': 0}}, {'c': {'conservation_rel': 2.0157532542446545e-15}}
    r = compare(ra, rb)
    chk('⑰ 잔차 측정 키 0 ↔ 2e-15 = resid · other 0', len(r['resid']) == 1 and not r['other'])
    r = compare(ra, {'c': {'conservation_rel': 1e-9}})
    chk('⑱ 잔차 측정 키라도 1e-9 (기계 정밀도 밖) = other', len(r['other']) == 1)
    r = compare({'c': {'q_raw': 0}}, {'c': {'q_raw': 2e-15}})
    chk('⑲ 잔차 키가 아니면 (q_raw) 0 ↔ 2e-15 = other', len(r['other']) == 1)
    n = ok + len(bad)
    print(f'compare_probe_outputs selftest {ok}/{n}' + ('' if not bad else '  FAIL: ' + ' · '.join(bad)))
    return 0 if not bad else 1


def main(argv):
    if argv[:1] == ['--selftest']:
        return _selftest()
    out, pairs = argv[0], argv[1:]
    res, total_other = {}, 0
    for pair in pairs:
        ca, ob = pair.split('=', 1)
        a = json.load(open(ca, encoding='utf-8'))
        b = json.load(open(ob, encoding='utf-8'))
        r = compare(a, b)
        name = ca.replace('\\', '/').rsplit('/', 1)[-1]
        res[name] = {'codex': ca.replace('\\', '/').rsplit('/', 2)[-2:], 'ours': ob.replace('\\', '/').rsplit('/', 2)[-2:],
                     'n_keys_codex': r['n_keys_codex'], 'n_keys_ours': r['n_keys_ours'], 'equal': r['equal'],
                     'env': r['env'], 'path': r['path'],
                     'resid_n': len(r['resid']), 'resid_max_abs': max((max(abs(float(x['codex'])), abs(float(x['ours'])))
                                                                       for x in r['resid']), default=0.0),
                     'resid': r['resid'][:40], 'float_n': len(r['float']),
                     'float_max_rel': max((x['rel'] for x in r['float']), default=0.0),
                     'float_max_abs': max((abs(float(x['codex']) - float(x['ours'])) for x in r['float']), default=0.0),
                     'float': r['float'][:40], 'other': r['other']}
        total_other += len(r['other'])
    res['verdict_value_differences'] = total_other
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    for k, v in res.items():
        if isinstance(v, dict):
            print(f"{k}: 키 {v['n_keys_codex']} / {v['n_keys_ours']} · 같음 {v['equal']} · env {len(v['env'])} · path {len(v['path'])} · "
                  f"resid {v['resid_n']} (|값| ≤ {v['resid_max_abs']:.3g}) · float {v['float_n']} (최대 상대 {v['float_max_rel']:.3g} · "
                  f"최대 절대 {v['float_max_abs']:.3g}) · other {len(v['other'])}")
    print('판정값 차이 (other 합) =', total_other)
    return 0 if total_other == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
