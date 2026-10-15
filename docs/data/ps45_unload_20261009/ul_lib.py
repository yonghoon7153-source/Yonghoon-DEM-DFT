#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 — 공용 도우미 (표 · 원 덱 · 덱 언어 검사 · 덤프 · thermo · CSV).  표준 라이브러리만 · 읽기 전용.

    python3 ul_lib.py --selftest

- 표 = unload_params.json (하나뿐 — 덱 생성기 · 러너 · 읽는 쪽이 여기서만 읽는다).
- 원 덱 = 리포 tgz 멤버 (이름 끝으로 찾는다 · sha256 = 표) — 덱 글자 데이터로만 읽는다.
- 덱 언어 검사 (⑭a run 사이 위험한 읽기 · ⑭b 얼림) = 가지 키트 make_branch_decks.py 의 검사기를 옮겨 왔다 (그 키트 봉인과 섞지 않게 사본).
- thermo: run 마다 첫 줄 = setup 줄 (기준 아님) · 같은 step 이 두 번 나오면 앞 줄 (정규 줄) 만 쓴다 (가지 키트 README §5 · 재개 체크리스트 ⑤).
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
PARAMS = os.path.join(HERE, 'unload_params.json')


def load_params(path=PARAMS):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def tgz_member(suffix, sha=None, P=None):
    """리포 tgz 안에서 이름이 '/' + suffix 로 끝나는 멤버 하나 → 바이트 (sha 가 있으면 대조 · 다르면 거부)."""
    P = P or load_params()
    tgz = os.path.join(REPO, P['head_source']['tgz'])
    with tarfile.open(tgz, 'r:gz') as t:
        ms = [m for m in t.getmembers() if m.isfile() and m.name.endswith('/' + suffix)]
        if len(ms) != 1:
            raise SystemExit(f'⛔ tgz 멤버 …/{suffix} 가 {len(ms)} 개')
        raw = t.extractfile(ms[0]).read()
    if sha and sha256_bytes(raw) != sha:
        raise SystemExit(f'⛔ tgz 멤버 …/{suffix} sha256 이 표와 다르다')
    return raw


def r8_text(P=None):
    P = P or load_params()
    return tgz_member(P['head_source']['r8_suffix'], P['head_source']['r8_sha256'], P).decode('utf-8')


def r2_text(P=None):
    P = P or load_params()
    return tgz_member(P['head_source']['r2_suffix'], P['head_source']['r2_sha256'], P).decode('utf-8')


# ── 덱 언어 ─────────────────────────────────────────────────────────────────

def strip_comment(s):
    q = ''
    for i, ch in enumerate(s):
        if ch == '#' and not q:
            return s[:i]
        if q and ch == q:
            q = ''
        elif not q and ch in '"\'':
            q = ch
    return s


def logical_lines(text):
    """주석 · 빈 줄 빼고 `&` 이음을 붙인 명령 줄 (공백은 하나로)."""
    out, cur = [], ''
    for raw in text.splitlines():
        s = raw.rstrip()
        cont = s.endswith('&')
        if cont:
            s = s[:-1]
        cur += ' ' + s
        if cont:
            continue
        line = strip_comment(cur).strip()
        cur = ''
        if line:
            out.append(' '.join(line.split()))
    return out


def words(line):
    """LIGGGHTS nextword 와 같게 — 따옴표 묶음은 한 낱말 (따옴표 뒤는 공백이어야 한다)."""
    out, i, n = [], 0, len(line)
    while i < n:
        while i < n and line[i].isspace():
            i += 1
        if i >= n:
            break
        if line[i] in '"\'':
            j = line.find(line[i], i + 1)
            if j < 0:
                raise ValueError(f'따옴표가 닫히지 않는다: {line}')
            if j + 1 < n and not line[j + 1].isspace():
                raise ValueError(f'따옴표 뒤가 공백이 아니다: {line}')
            out.append(line[i + 1:j])
            i = j + 1
        else:
            j = i
            while j < n and not line[j].isspace():
                j += 1
            out.append(line[i:j])
            i = j
    return out


THERMO_COMPUTE = frozenset({'ke', 'pe', 'etotal', 'enthalpy', 'temp', 'press', 'evdwl', 'ecoul', 'epair', 'ebond', 'eangle',
                            'edihed', 'eimp', 'emol', 'elong', 'etail', 'erotate', 'pxx', 'pyy', 'pzz', 'pxy', 'pxz', 'pyz'})
THERMO_NOT_BETWEEN = frozenset({'elapsed', 'elaplong', 'cpu', 'cu', 'tpcpu', 'spcpu', 'cpuremain'})
THERMO_PLAIN = frozenset({'step', 'atoms', 'dt', 'time', 'part', 'vol', 'lx', 'ly', 'lz', 'xlo', 'xhi', 'ylo', 'yhi', 'zlo', 'zhi',
                          'xy', 'xz', 'yz', 'xlat', 'ylat', 'zlat', 'nbuild', 'ndanger'})
GROUP_FUNCS = frozenset({'count', 'mass', 'charge', 'xcm', 'vcm', 'fcm', 'bound', 'gyration', 'ke', 'angmom', 'torque',
                         'inertia', 'omega'})


def expr_deps(expr):
    e = re.sub(r'\$\{\w+\}', '0', expr)
    deps = set()
    for kind in 'cfv':
        for m in re.finditer(r'\b' + kind + r'_(\w+)(?:\[(\d+)\])?', e):
            deps.add((kind, m.group(1), int(m.group(2) or 0)))
    e = re.sub(r'\b[cfv]_\w+(?:\[\d+\])?', '0', e)
    for m in re.finditer(r'(?<![\w.])([A-Za-z_]\w*)(\s*\()?', e):
        name, call = m.group(1), m.group(2)
        if call:
            if name in GROUP_FUNCS:
                deps.add(('g', name, 0))
        elif name in THERMO_COMPUTE:
            deps.add(('k', name, 0))
        elif name in THERMO_NOT_BETWEEN:
            deps.add(('x', name, 0))
        elif name in THERMO_PLAIN:
            deps.add(('t', name, 0))
    return frozenset(deps)


def _st_new():
    return {'ke': True, 'fix': {}, 'env': {}, 'thermo': frozenset()}


def _st_copy(s):
    return {'ke': s['ke'], 'fix': dict(s['fix']), 'env': dict(s['env']), 'thermo': s['thermo']}


def _st_key(s):
    return (s['ke'], tuple(sorted(s['fix'].items())), tuple(sorted(s['env'].items(), key=lambda kv: kv[0])), s['thermo'])


def _resolve(name, env, seen=frozenset()):
    leaves = set()
    for d in env.get(name, frozenset()):
        if d[0] == 'v':
            if d[1] not in seen:
                leaves |= _resolve(d[1], env, seen | {name})
        else:
            leaves.add(d)
    return leaves


def _read_hazards(name, s, mesh_ids):
    out = []
    for kind, ident, idx in sorted(_resolve(name, s['env'])):
        if kind in ('k', 'c') and s['ke']:
            out.append(('stale', f'{ident} 가 현재가 아니다 (write_restart · read_restart 뒤 · run 전)'))
        elif kind == 'x':
            out.append(('between', f'{ident} 는 run 사이에 못 읽는다'))
        elif kind == 'f':
            st = s['fix'].get(ident, 'absent')
            if st in ('gone', 'absent'):
                out.append(('nofix', f'f_{ident} 가 없다'))
            elif st == 'polluted' and ident in mesh_ids and (idx == 0 or 1 <= idx <= 6):
                out.append(('setup', f'f_{ident}[{idx}] 가 run 0 · 새 fix 뒤라 직전 합 + rank 몫'))
    return out


def _apply_cmd(w, s, mesh_ids):
    if not w:
        return
    c = w[0]
    if c == 'variable' and len(w) >= 3:
        s['env'][w[1]] = expr_deps(w[3]) if (w[2] == 'equal' and len(w) == 4) else frozenset()
    elif c == 'run' and len(w) >= 2:
        s['ke'] = False
        for fid, st in list(s['fix'].items()):
            if fid in mesh_ids and st != 'gone':
                s['fix'][fid] = 'polluted' if w[1] == '0' else 'ok'
    elif c in ('write_restart', 'read_restart'):
        s['ke'] = True
    elif c == 'fix' and len(w) >= 4:
        s['fix'][w[1]] = 'polluted' if w[1] in mesh_ids else 'ok'
    elif c == 'unfix' and len(w) >= 2:
        s['fix'][w[1]] = 'gone'
    elif c == 'thermo_style':
        s['thermo'] = frozenset(re.findall(r'\bv_(\w+)', ' '.join(w)))


def _if_branches(w):
    branches, cur, has_else, k = [], [], False, 3
    while k < len(w):
        t = w[k]
        if t == 'elif':
            branches.append(cur)
            cur, k = [], k + 2
            continue
        if t == 'else':
            branches.append(cur)
            cur, has_else = [], True
        else:
            cur.append(' '.join(t.split()))
        k += 1
    branches.append(cur)
    return branches, has_else


def scan_between_runs(text, include_files=None):
    """덱의 모든 경로에서 run 사이 위험한 읽기 → [(줄 번호, 변수, 종류, 설명, 명령)] (가지 키트 ⑭a 와 같은 규칙).
    include ${…} 는 상태 파일 (변수 정의만) 로 보고 그 안의 변수를 상수로 둔다."""
    lines = logical_lines(text)
    n = len(lines)
    W = [words(ln) for ln in lines]
    labels = {w[1]: i for i, w in enumerate(W) if len(w) >= 2 and w[0] == 'label'}
    mesh_ids = {w[1] for w in W if len(w) >= 4 and w[0] == 'fix' and 'mesh/surface/stress' in w[3]}
    found = {}
    seen = [set() for _ in range(n)]
    work = [(0, _st_new())]
    while work:
        i, s = work.pop()
        k = _st_key(s)
        if k in seen[i]:
            continue
        seen[i].add(k)
        w = W[i]
        for name in re.findall(r'\$\{(\w+)\}', lines[i]):
            for kind, why in _read_hazards(name, s, mesh_ids):
                found[(i, name, kind)] = (i, name, kind, why, lines[i])
        succ = []
        if w[0] == 'run':
            for name in sorted(s['thermo']):
                for kind, why in _read_hazards(name, s, mesh_ids):
                    if kind == 'nofix':
                        found[(i, 'v_' + name, kind)] = (i, 'v_' + name, kind, 'thermo_style 의 ' + why, lines[i])
        if w[0] == 'jump' and len(w) >= 3 and w[1] == 'SELF':
            succ.append((labels[w[2]], s))
        elif w[0] == 'quit':
            pass
        elif w[0] == 'if':
            branches, has_else = _if_branches(w)
            if not has_else:
                succ.append((i + 1, s))
            for br in branches:
                b = _st_copy(s)
                ended = False
                for cmd in br:
                    cw = words(cmd)
                    if cw[:2] == ['jump', 'SELF']:
                        succ.append((labels[cw[2]], b))
                        ended = True
                        break
                    if cw[:1] == ['quit']:
                        ended = True
                        break
                    _apply_cmd(cw, b, mesh_ids)
                if not ended:
                    succ.append((i + 1, b))
        else:
            t = _st_copy(s)
            _apply_cmd(w, t, mesh_ids)
            succ.append((i + 1, t))
        for j, s2 in succ:
            if j < n:
                work.append((j, s2))
    return sorted(found.values())


def unfrozen_lazy(text, lazy_ok):
    """⑭b — 살아 있는 equal 정의 바로 다음 줄이 `variable X equal ${X}` 가 아닌 곳 (lazy_ok 빼고)."""
    lines = logical_lines(text)
    bad = []
    for i, ln in enumerate(lines):
        w = words(ln)
        if len(w) == 4 and w[0] == 'variable' and w[2] == 'equal' and w[1] not in lazy_ok and expr_deps(w[3]):
            nxt = lines[i + 1] if i + 1 < len(lines) else ''
            if nxt != f'variable {w[1]} equal ${{{w[1]}}}':
                bad.append(ln)
    return bad


def bad_if_conditions(text):
    """if 조건 = 숫자 · 비교 · 논리 · 괄호뿐 (variable.cpp evaluate_boolean) — 산술 · 이름이 있으면 그 줄."""
    bad = []
    for ln in logical_lines(text):
        w = words(ln)
        if w[:1] == ['if']:
            cond = re.sub(r'\$\{\w+\}', '1', w[1])
            cond = re.sub(r'\d+\.?\d*(?:[eE][-+]?\d+)?', '1', cond)
            if re.search(r'[A-Za-z_]|[+*/]', cond) or re.search(r'\d\s*-\s*\d', cond):
                bad.append(ln)
    return bad


# ── 덤프 · thermo · CSV ────────────────────────────────────────────────────────

def read_dump(path, kind, cols_expected=None):
    """LIGGGHTS 덤프 한 장 → {'ok','step','cols','rows','box','problems'} (kind = custom | local)."""
    out = {'ok': False, 'path': path, 'step': None, 'cols': None, 'rows': [], 'box': None, 'problems': []}
    if not path or not os.path.exists(path):
        out['problems'].append(f'파일 없음: {path}')
        return out
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    pr = out['problems']
    try:
        out['step'] = int(lines[lines.index('ITEM: TIMESTEP') + 1].strip())
    except (ValueError, IndexError):
        pr.append('TIMESTEP 머리 없음')
    head = 'ITEM: ATOMS' if kind == 'custom' else 'ITEM: ENTRIES'
    nhead = 'ITEM: NUMBER OF ATOMS' if kind == 'custom' else 'ITEM: NUMBER OF ENTRIES'
    try:
        n_decl = int(lines[lines.index(nhead) + 1].strip())
    except (ValueError, IndexError):
        n_decl = None
        pr.append(f'{nhead} 머리 없음')
    try:
        kb = next(i for i, x in enumerate(lines) if x.startswith('ITEM: BOX BOUNDS'))
        out['box'] = [tuple(float(v) for v in lines[kb + j].split()[:2]) for j in (1, 2, 3)]
    except (StopIteration, ValueError, IndexError):
        pr.append('BOX BOUNDS 머리 없음')
    k = next((i for i, x in enumerate(lines) if x.startswith(head)), None)
    if k is None:
        pr.append(f'{head} 머리 없음')
        return out
    cols = lines[k].split()[2:]
    out['cols'] = cols
    if cols_expected is not None and cols != list(cols_expected):
        pr.append(f'열 이름 {cols} ≠ 기대 {list(cols_expected)}')
    for ln in lines[k + 1:]:
        if not ln.strip():
            continue
        if ln.startswith('ITEM:'):
            pr.append('한 파일에 프레임이 둘 이상')
            break
        vals = ln.split()
        if len(vals) != len(cols):
            pr.append(f'열 수 {len(vals)} ≠ {len(cols)}')
            continue
        try:
            row = {c: float(v) for c, v in zip(cols, vals)}
        except ValueError:
            pr.append(f'숫자가 아닌 값: {ln[:60]}')
            continue
        if not all(math.isfinite(v) for v in row.values()):
            pr.append(f'비유한 값: {ln[:60]}')
            continue
        out['rows'].append(row)
    if n_decl is not None and n_decl != len(out['rows']) and not any(p.startswith(('비유한', '숫자가', '열 수')) for p in pr):
        pr.append(f'행 수 {len(out["rows"])} ≠ 머리 {n_decl}')
    out['ok'] = not pr
    return out


def write_custom(path, step, cols, rows, box=((0.0, 0.05), (0.0, 0.05), (-0.01, 1.0)), fmt=repr):
    """합성 시험용 — LIGGGHTS custom 덤프 꼴로 쓴다 (rows = dict 목록 · id · type 은 정수)."""
    L = ['ITEM: TIMESTEP', str(step), 'ITEM: NUMBER OF ATOMS', str(len(rows)), 'ITEM: BOX BOUNDS pp pp ff']
    L += [f'{a!r} {b!r}' for a, b in box] + ['ITEM: ATOMS ' + ' '.join(cols)]
    for r in rows:
        L.append(' '.join(str(int(r[c])) if c in ('id', 'type') else fmt(float(r[c])) for c in cols))
    with open(path, 'w') as f:
        f.write('\n'.join(L) + '\n')


def write_local(path, step, cols, rows, box=((0.0, 0.05), (0.0, 0.05), (-0.01, 1.0))):
    L = ['ITEM: TIMESTEP', str(step), 'ITEM: NUMBER OF ENTRIES', str(len(rows)), 'ITEM: BOX BOUNDS pp pp ff']
    L += [f'{a!r} {b!r}' for a, b in box] + ['ITEM: ENTRIES ' + ' '.join(cols)]
    L += [' '.join(repr(float(r[c])) for c in cols) for r in rows]
    with open(path, 'w') as f:
        f.write('\n'.join(L) + '\n')


def parse_thermo(text):
    """화면 · 로그 → {'blocks': [{'cols', 'rows': [(step, dict, is_setup)]}], 'regular': {step: dict}, 'setup': [(step, dict)],
    'loops': [N procs …]} — run 마다 머리 줄 (Step …) 다음 첫 줄 = setup · 같은 step 이 여러 번이면 정규 줄 (먼저 나온 것) 하나."""
    blocks, cur = [], None
    loops = []
    for ln in text.splitlines():
        t = ln.split()
        if t and t[0] == 'Step' and len(t) >= 2:
            cur = {'cols': t, 'rows': []}
            blocks.append(cur)
            continue
        m = re.search(r'Loop time of [0-9.eE+-]+ on (\d+) procs', ln)
        if m:
            loops.append(int(m.group(1)))
            cur = None
            continue
        if cur is not None and t and re.fullmatch(r'\d+', t[0]) and len(t) == len(cur['cols']):
            try:
                vals = [float(x) for x in t]
            except ValueError:
                continue
            row = dict(zip(cur['cols'], vals))
            cur['rows'].append((int(t[0]), row, not cur['rows']))
    regular, setup = {}, []
    for b in blocks:
        for step, row, is_setup in b['rows']:
            if is_setup:
                setup.append((step, row))
            elif step not in regular:
                regular[step] = row
    return {'blocks': blocks, 'regular': regular, 'setup': setup, 'loops': loops}


def read_csv(path):
    if not os.path.exists(path):
        return None
    lines = [ln for ln in open(path, encoding='utf-8').read().splitlines() if ln.strip()]
    if not lines:
        return []
    head = lines[0].split(',')
    out = []
    for ln in lines[1:]:
        v = ln.split(',')
        if len(v) != len(head):
            continue
        out.append(dict(zip(head, v)))
    return out


def read_kv(path):
    out = {}
    if not os.path.exists(path):
        return out
    for ln in open(path, encoding='utf-8').read().splitlines():
        if '=' in ln:
            k, v = ln.split('=', 1)
            out[k.strip()] = v.strip()
    return out


def fnum(x):
    """문자열 → float (빈 · 비유한 · 숫자 아님 = None · NaN 을 비교로 흘려보내지 않는다)."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


ID_MAX = 2 ** 53   # float 로 읽은 정수가 정확한 범위


def exact_id(x):
    """원자 ID (덤프를 float 로 읽은 값) → int — 유한 · 양 · 정확한 정수 (2^53 이하) 일 때만 · 아니면 None.
    ULKRR-04: 소수 ID 를 정수로 자르지 않는다 (int(2.5) = 2 가 다른 원자로 둔갑) · bool · 글자는 받지 않는다."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return None
    if isinstance(x, float) and not (math.isfinite(x) and x.is_integer()):
        return None
    return int(x) if 0 < x <= ID_MAX else None


def ids_of(rows, key='id'):
    """행 목록의 ID → (정수 목록 | None, 문제 목록) — 필수 열 결손 · 소수 · 비유한 · 0 이하 = None + 사유 (예외 없이 · ULKRR-04)."""
    if any(key not in r for r in rows):
        return None, [f'{key} 열 없음 (필수 열 결손)']
    ids = [exact_id(r[key]) for r in rows]
    bad = [r[key] for r, i in zip(rows, ids) if i is None]
    if bad:
        return None, [f'{key} 가 유한 · 양의 정확한 정수가 아니다 ({bad[:3]}) — 정수로 자르지 않는다']
    return ids, []


# ── selftest ─────────────────────────────────────────────────────────────────

def selftest():
    import tempfile
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    P = load_params()
    chk('L1 표: 침대 다섯 · 팔 여섯 · 튜플 넷', lambda: len(P['beds']) == 5 and set(P['arms']) == {'UB', 'UT', 'UVa', 'UVb', 'UT3', 'UC'}
        and set(P['tuples']) == {'t1', 't2', 't3', 't4'})
    chk('L2 원 덱 r8 · r2 = 리포 tgz 멤버 · sha256 = 표', lambda: 'run 100000' in r8_text(P) and 'run 100000' in r2_text(P))
    chk('L3 logical_lines: & 이음 · 주석 · 공백', lambda: logical_lines('fix a all x &\n  1 2 # c\n\n# z\nrun 0\n') == ['fix a all x 1 2', 'run 0'])
    chk('L4 words: 따옴표 묶음', lambda: words('if "${a} > 1" then "print \'x y\'"') == ['if', '${a} > 1', 'then', "print 'x y'"])
    syn = 'read_restart ${ckpt}\nthermo_style custom step atoms ke\nfix top_mesh all mesh/surface/stress file x type 1\n'
    cases = [
        ('write_restart 뒤 살아 있는 ke', syn + 'run 5\nvariable k equal ke\nwrite_restart a.bin\nprint "${k}"\n', {'stale'}),
        ('얼리면 통과', syn + 'run 5\nvariable k equal ke\nvariable k equal ${k}\nwrite_restart a.bin\nprint "${k}"\n', set()),
        ('jump 경로', syn + 'run 5\nvariable k equal ke\nwrite_restart a.bin\njump SELF g\nprint "x"\nlabel g\nprint "${k}"\n', {'stale'}),
        ('run 0 뒤 메시 힘', syn + 'run 5\nrun 0\nvariable F equal f_top_mesh[3]\nprint "${F}"\n', {'setup'}),
        ('run N>0 뒤 메시 힘 통과', syn + 'run 0\nrun 5\nvariable F equal f_top_mesh[3]\nprint "${F}"\n', set()),
        ('unfix 뒤 읽기', syn + 'run 5\nvariable F equal f_top_mesh[3]\nunfix top_mesh\nprint "${F}"\n', {'nofix'}),
        ('run 사이 금지 cpu', syn + 'run 5\nvariable c equal cpu\nprint "${c}"\n', {'between'}),
        ('count 는 run 사이 통과', syn + 'write_restart a.bin\nvariable n equal count(all)\nprint "${n}"\n', set()),
    ]
    for name, deck, want in cases:
        chk(f'L5 ⑭a 검사기: {name}', lambda deck=deck, want=want: {h[2] for h in scan_between_runs(deck)} == want)
    chk('L6 ⑭b 얼림 검사', lambda: unfrozen_lazy('run 5\nvariable k equal ke\nprint "${k}"\n', {}) == ['variable k equal ke']
        and unfrozen_lazy('variable k equal ke\nvariable k equal ${k}\n', {}) == [])
    chk('L7 if 조건 검사 (산술 거부)', lambda: bad_if_conditions('if "${a}+1 > 2" then "quit"\nif "${a} > 2" then "quit"\n') == ['if "${a}+1 > 2" then "quit"'])
    scr = ('    Step    Atoms         KinEng            CPU       pressMPa \n 100   10  1e-6  0  0.31 \n 600 10 2e-6 1 0.20 \n 1100 10 3e-6 2 0.19 \n'
           'Loop time of 1.0 on 6 procs for 1000 steps with 10 atoms\n'
           '    Step    Atoms         KinEng            CPU       pressMPa \n 1100   10  3e-6  0  0.38 \n 1600 10 4e-6 1 0.18 \n'
           'Loop time of 1.0 on 6 procs for 500 steps with 10 atoms\n')
    T = parse_thermo(scr)
    chk('L8 thermo: setup 줄 둘 · 정규 줄 = 600 · 1100 · 1600 · 겹친 1100 은 정규 (앞 줄) 값', lambda: [s for s, _ in T['setup']] == [100, 1100]
        and sorted(T['regular']) == [600, 1100, 1600] and T['regular'][1100]['pressMPa'] == 0.19 and T['loops'] == [6, 6])
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'a.dump')
        write_custom(p, 5, ['id', 'type', 'z'], [{'id': 1, 'type': 3, 'z': 0.1}, {'id': 2, 'type': 1, 'z': 0.2}])
        d = read_dump(p, 'custom', ['id', 'type', 'z'])
        chk('L9 덤프 custom 왕복', lambda: d['ok'] and d['step'] == 5 and d['rows'][1]['z'] == 0.2)
        open(p, 'a').write('3 1 nan\n')
        chk('L10 덤프: 비유한 · 행 수 어긋남 = 문제', lambda: not read_dump(p, 'custom', ['id', 'type', 'z'])['ok'])
        q = os.path.join(td, 'b.dump')
        write_local(q, 7, ['c_x[1]', 'c_x[2]'], [{'c_x[1]': 1.0, 'c_x[2]': -2.5}])
        chk('L11 덤프 local 왕복 · 열 이름 대조', lambda: read_dump(q, 'local', ['c_x[1]', 'c_x[2]'])['ok'] and not read_dump(q, 'local', ['c_y[1]', 'c_x[2]'])['ok'])
    chk('L12 fnum: NaN · inf · 빈 = None', lambda: fnum('nan') is None and fnum('inf') is None and fnum('') is None and fnum('1e-3') == 1e-3)
    chk('L13 ULKRR-04 exact_id: 유한 · 양 · 정확한 정수만 (1.0 → 1 · 7 → 7) · 2.5 · 0 · −1 · nan · inf · True · "1" · 2^53 + 2 = None (자르지 않는다)',
        lambda: exact_id(1.0) == 1 and exact_id(7) == 7 and all(exact_id(x) is None for x in (2.5, 0.0, -1.0, float('nan'), float('inf'), True, '1',
                                                                                               2.0 ** 53 + 2)))
    chk('L13 ULKRR-04 ids_of: 정상 = (정수 목록 · 문제 없음) · 소수 ID · 열 결손 = (None · 사유) — 예외 없음',
        lambda: ids_of([{'id': 1.0}, {'id': 2.0}]) == ([1, 2], []) and ids_of([{'id': 1.0}, {'id': 1.5}])[0] is None and ids_of([{'id': 1.0}, {'id': 1.5}])[1]
        and ids_of([{'not_id': 1.0}])[0] is None and ids_of([{'not_id': 1.0}])[1])
    # ── Q4 (Codex 수정 재확인 10-15 Q3 비차단 · 1저자 10-15 권고대로) — 덤프의 ID 열 정수 토큰은 float 를 거치지 않고 검사한다 ──
    #    (옛 판: read_dump 가 '9007199254740993' 을 float 9007199254740992.0 (= 2^53) 으로 읽어 exact_id 가 받았다 · '1.0000000000000001' 도 1.0 으로 받았다)
    with tempfile.TemporaryDirectory() as td:
        def dump_with(tok, kind='custom'):
            p = os.path.join(td, f'{kind}_{len(os.listdir(td))}.dump')
            if kind == 'custom':
                write_custom(p, 5, ['id', 'type', 'z'], [{'id': 1, 'type': 3, 'z': 0.1}, {'id': 2, 'type': 1, 'z': 0.2}])
                txt = open(p).read().replace('\n2 1 ', f'\n{tok} 1 ', 1)
            else:
                write_local(p, 5, ['c_cpl[7]', 'c_cpl[8]', 'c_x[1]'], [{'c_cpl[7]': 1.0, 'c_cpl[8]': 2.0, 'c_x[1]': 0.5}])
                txt = open(p).read().replace('\n1.0 2.0 ', f'\n1.0 {tok} ', 1)
            with open(p, 'w', newline='\n') as f:
                f.write(txt)
            return read_dump(p, kind, ['id', 'type', 'z'] if kind == 'custom' else ['c_cpl[7]', 'c_cpl[8]', 'c_x[1]'])
        big = dump_with('9007199254740993')
        norm = dump_with('2')
        chk('L14 Q4 원자 덤프 ID 정수 토큰 9007199254740993 (2^53 + 1) — float 를 거치지 않는다 → exact_id · ids_of 거부 (2^53 으로 둔갑해 받지 않는다) · '
            '정상 토큰 1 · 2 = 그대로 (1 · 2)',
            lambda: big['ok'] and big['rows'][1]['id'] == 9007199254740993 and exact_id(big['rows'][1]['id']) is None and ids_of(big['rows'])[0] is None
            and bool(ids_of(big['rows'])[1]) and norm['ok'] and [exact_id(r['id']) for r in norm['rows']] == [1, 2] and ids_of(norm['rows']) == ([1, 2], []),
            f'{big["rows"][1:]} {norm["rows"]}')
        lbig, l1, lmask = dump_with('9007199254740993', 'local'), dump_with('2.0', 'local'), dump_with('2.0000000000000001', 'local')
        chk('L14 Q4 쌍 덤프 참조 열 (c_cpl[7] · c_cpl[8]) 같은 규칙 — 정수 토큰 2^53 + 1 거부 · 소수 꼴 정확한 정수 2.0 그대로 (2) · '
            '2.0000000000000001 (float 가 정수 2.0 으로 가린다) = 파서 문제 (ok 거짓 · 사유)',
            lambda: lbig['ok'] and exact_id(lbig['rows'][0]['c_cpl[8]']) is None and l1['ok'] and exact_id(l1['rows'][0]['c_cpl[8]']) == 2
            and not lmask['ok'] and any('정수' in x for x in lmask['problems']),
            f'{lbig["rows"]} {l1["rows"]} {lmask["ok"]} {lmask["problems"]}')
        huge = dump_with('1' + '0' * 400)
        chk('L14 Q4 아주 긴 정수 토큰 (401 자리) — 예외 없이 ID 로 받지 않는다 (파서 문제 또는 exact_id 거부)',
            lambda: (not huge['ok']) or exact_id(huge['rows'][1]['id']) is None, f'{huge["ok"]} {huge["problems"]}')
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


if __name__ == '__main__':
    if '--selftest' in sys.argv[1:]:
        sys.exit(selftest())
    print(__doc__)
