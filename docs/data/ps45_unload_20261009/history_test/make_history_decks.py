#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 — 작은 침대 이력 시험 (H0–H5) 덱 생성기.  덱을 손으로 고치지 말 것.

    python3 make_history_decks.py             # 덱 · 판 STL · SHA256SUMS 다시 쓰기
    python3 make_history_decks.py --check     # 커밋본 = 생성 결과 · SHA256SUMS 일치 (다르면 rc 1)
    python3 make_history_decks.py --selftest  # 구조 · 설계 · run 사이 읽기 · 러너 짝 검사

무엇 (정본 = ../README.md §1 · 등록 docs/reviews/dem_unloading_ps45_prereg_20261009.md §12-1 · §13-6 ③ ·
      Codex 판정문 docs/reviews/codex_review_dem_unloading_prereg_rereview_20261012.md §5 · 노트 …/notes/history.md §3)
  작은 침대 (입자 20) 에서 **알려진 이력** (저장 deltaMax > 현재 겹침 · 0 아닌 접선 이력) 을 만들어 restart 로 저장하고,
  별도 프로세스가 다시 읽어 PRE_SETUP (write_dump = 배열 그대로) · POST_SETUP (run 0 setup 뒤 local 재평가) 로 관측한다.
  H0 문법 · H1 같은 NP round-trip · H2 NP 바꿈 · H3 바닥 (primitive) 만 소거 · H4 판 (mesh) 만 소거 · H5 결손 / 0 뿐 —
  읽는 쪽 = read_history.py.  덤으로 SYN (본 키트 덱 문법 미리 지나가기 · 판정 밖).

fixture 를 만드는 법 (적분 없음 · 운동학)
  입자를 적분하지 않는다 (fix nve/sphere 없음) — 위치 · 속도는 명령으로만 바뀐다.
  ① 적재: 설계 deltaMax 만큼 겹친 자리에 만들고 run 10 → setup 에서 history[0] = max(0, δ) = deltaMax
     (normal_model_hooke_hysteresis.h:156–158 · 갱신 막는 guard 앞).
  ② 부분 제하: set atom … z / x / y 로 현재 겹침 δ < deltaMax 자리로 옮긴다 (순간 · 이력 유지).
  ③ 접선: set atom … vx vy vz (접촉 법선에 수직) → run 1000 → shear += v_t·dt (tangential_model_history.h:147–159 · 위치는 그대로).
  ④ 정지: 속도 0 → run 990 → 마지막 step (2000) 의 in-run 덤프 = 봉인할 기대값 · write_dump 묶음 · write_restart.
  모델 머리 (재료 m1–m9 · pair · 벽 · 중력 · 감쇠 · 메시) 는 r8 원 덱 글자에서 뽑는다 (숫자를 다시 적지 않는다 — history_params.json head_source).

LIGGGHTS 근거 (3d5c00f · Codex 판정문 §5 · 노트 §1–§3):
  primitive 내부 fix = history_<벽 ID> property/atom (fix_wall_gran.cpp:497–519) · dump custom f_ID[N] 정수 첨자 (dump_custom.cpp:1367–1396) ·
  write_dump = 덤프 init → write 만 (write_dump.cpp:63–114 · setup 없음) · wall/gran/local 은 mesh 벽만 (compute_pair_gran_local.cpp:247–269) ·
  활성 wall local compute 를 둔 벽 unfix 거부 (fix_wall_gran.cpp:541–542) · 양의 timestep 에서 새 local compute 제한 (126–127) →
  소거 = 별도 진단 사본: run 0 (첫 초기화) → undump · uncompute → 벽 하나 unfix → write_restart → 새 프로세스.
  ⚠ 덤프 local 은 run 사이에 compute 가 현재가 아니면 ERROR (dump_local count — 'not current') → POST 관측은 write_dump 가 아니라
     dump … first yes + run 0 (가지 키트 스냅숏 덱이 ibb 에서 지나간 꼴) 으로 한다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))
PARAMS = os.path.join(HERE, 'history_params.json')
SUMS = 'SHA256SUMS'
PLATE_STL = 'plate_hist.stl'
SBATCH = 'run_history_ibb.sbatch'
RUNNER = 'run_history.sh'
READER = 'read_history.py'

DECKS = {
    'producer': 'in.hist_producer.liggghts',
    'producer_zero': 'in.hist_producer_zero.liggghts',
    'consumer': 'in.hist_consumer.liggghts',
    'erase_bot': 'in.hist_erase_bot.liggghts',
    'erase_top': 'in.hist_erase_top.liggghts',
    'erase_none': 'in.hist_erase_none.liggghts',
    'badid': 'in.hist_badid.liggghts',
    'syntax_probe': 'in.hist_syntax_probe.liggghts',
    'grammar': 'in.hist_grammar.liggghts',
}
SUMMED = list(DECKS.values()) + [PLATE_STL, 'history_params.json', 'make_history_decks.py', READER, RUNNER, SBATCH]


def load_params(path=PARAMS):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ── 구현 (아래 selftest 를 먼저 썼다 — 시험 먼저 기록 = ../README.md §9) ───────────────────────────────

#  덱 언어 도우미 — 가지 키트 (docs/data/ps73_damping_branch_20261007/make_branch_decks.py ⑭) 의 검사기를 옮겨 왔다 (그 키트 봉인과 섞지 않게 사본)

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
#: 일부러 살아 있게 두는 equal 변수 (⑭b 면제 · 이유)
LAZY_OK = {
    'pressMPa': 'thermo_style 의 v_pressMPa — run 동안 thermo 가 읽는다',
    'Ps': 'ave/time · thermo 의 v_Ps — run 동안 읽힌다 (부호 있는 판 압력)',
    'u_nc': 'count(group,region) 공식 — run 뒤 영역을 고친 다음 ${u_nc} 로 바로 읽는다 (compute 아님)',
    'hb_step_now': '다음 줄이 즉시 치환으로 얼린다 (step)',
    'hb_n_now': '다음 줄이 즉시 치환으로 얼린다 (atoms)',
    'gr_dnext': 'dump_modify … every v_gr_dnext 의 다음 덤프 시각 공식 — run setup 과 덤프 뒤에 LIGGGHTS 가 읽는다 (본 키트 ul_dnext 꼴)',
    'gr_nc': 'count(group,region) 공식 — 창 뒤 ${gr_nc} 로 바로 읽는다 (compute 아님 · 본 키트 판 접촉 개수 꼴)',
}


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


def scan_between_runs(text):
    """덱의 모든 경로에서 run 사이 위험한 읽기 → [(줄 번호, 변수, 종류, 설명, 명령)] (가지 키트 ⑭a 와 같은 규칙)."""
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


def unfrozen_lazy(text):
    """⑭b — 살아 있는 equal 정의 바로 다음 줄이 `variable X equal ${X}` 가 아닌 곳 (LAZY_OK 빼고)."""
    lines = logical_lines(text)
    bad = []
    for i, ln in enumerate(lines):
        w = words(ln)
        if len(w) == 4 and w[0] == 'variable' and w[2] == 'equal' and w[1] not in LAZY_OK and expr_deps(w[3]):
            nxt = lines[i + 1] if i + 1 < len(lines) else ''
            if nxt != f'variable {w[1]} equal ${{{w[1]}}}':
                bad.append(ln)
    return bad


# ── 모델 머리 (r8 원 덱 글자) ─────────────────────────────────────────────────

def _member_text(P):
    tgz = os.path.join(REPO, P['head_source']['tgz'])
    suf = P['head_source']['member_suffix']
    with tarfile.open(tgz, 'r:gz') as t:
        ms = [m for m in t.getmembers() if m.isfile() and m.name.endswith('/' + suf)]
        if len(ms) != 1:
            raise SystemExit(f'⛔ 원 덱 멤버 (…/{suf}) 가 {len(ms)} 개')
        raw = t.extractfile(ms[0]).read()
    return raw


def extract_head(P=None):
    """r8 원 덱 → {'sha256', 'cmd': {키: 정규화한 명령 줄}, 'radius': {type: m}, 'density': {type: kg/m³}, 'plate_file', 'm': 재료 표}.
    같은 키가 둘 이상이면 거부 (이완 감쇠는 마지막 run 앞 마지막 `fix damp` · 중력은 하나뿐이어야)."""
    P = P or load_params()
    raw = _member_text(P)
    sha = hashlib.sha256(raw).hexdigest()
    lines = logical_lines(raw.decode('utf-8'))
    cmd = {}

    def take(key, pred, pick='one'):
        hits = [ln for ln in lines if pred(ln)]
        if pick == 'one' and len(hits) != 1:
            raise SystemExit(f'⛔ r8 에서 {key} 가 {len(hits)} 번')
        if not hits:
            raise SystemExit(f'⛔ r8 에서 {key} 없음')
        cmd[key] = hits[-1] if pick == 'last' else hits[0]

    for k in ('atom_style', 'atom_modify', 'boundary', 'newton', 'soft_particles', 'communicate', 'units', 'processors',
              'neighbor', 'neigh_modify', 'pair_style', 'pair_coeff', 'timestep'):
        take(k, lambda ln, k=k: ln.split()[0] == k)
    for v in ('dt', 'r_AM_P', 'r_AM_S', 'r_SE'):
        take(v, lambda ln, v=v: ln.split()[:2] == ['variable', v])
    for m in range(1, 10):
        take(f'm{m}', lambda ln, m=m: ln.split()[:2] == ['fix', f'm{m}'])
    for c in ('strs', 'ke', 'cpl'):
        take(c, lambda ln, c=c: ln.split()[:2] == ['compute', c])
    for f in ('zwall_bot', 'integr', 'gravi', 'top_mesh', 'zwall_top'):
        take(f, lambda ln, f=f: ln.split()[:2] == ['fix', f])
    #  이완 감쇠 = 마지막 run 앞의 마지막 `fix damp` (r8 145 행 · 압축 0.5 는 114 행)
    last_run = max(i for i, ln in enumerate(lines) if ln.split()[0] == 'run')
    damps = [ln for ln in lines[:last_run] if ln.split()[:2] == ['fix', 'damp']]
    cmd['damp_relax'] = damps[-1]
    take('energy', lambda ln: ln == 'fix_modify zwall_top energy yes')
    take('pressMPa', lambda ln: ln.split()[:2] == ['variable', 'pressMPa'])
    tw = cmd['top_mesh'].split()
    plate_file = tw[tw.index('file') + 1]
    radius = {1: float(cmd['r_AM_P'].split()[3]), 2: float(cmd['r_AM_S'].split()[3]), 3: float(cmd['r_SE'].split()[3])}
    dpath = os.path.join(REPO, P['head_source']['density_deck'])
    dtext = open(dpath, encoding='utf-8').read()
    if hashlib.sha256(dtext.encode('utf-8')).hexdigest() != P['head_source']['density_deck_sha256']:
        raise SystemExit('⛔ 밀도 원 덱 sha256 이 표와 다르다')
    density = {}
    for ln in logical_lines(dtext):
        w = ln.split()
        if w[:1] == ['fix'] and len(w) > 3 and w[3] == 'particletemplate/sphere':
            density[int(w[w.index('atom_type') + 1])] = float(w[w.index('density') + 2])

    def matrix(key):
        w = cmd[key].split()
        vals = [float(x) for x in w[w.index('peratomtypepair') + 2:]]
        return [vals[0:3], vals[3:6], vals[6:9]]

    mat = {'k2max_over_kn': matrix('m6'), 'kc_over_kn': matrix('m7'), 'phiF': matrix('m8'), 'mu': matrix('m4')}
    skin = float(cmd['neighbor'].split()[1])
    return {'sha256': sha, 'cmd': cmd, 'radius': radius, 'density': density, 'plate_file': plate_file, 'm': mat, 'skin': skin}


# ── fixture 설계 (자리 · 산술 검사) ─────────────────────────────────────────────

def _dlim(a, phiF, reff):
    return a / (a - 1.0) * phiF * 2.0 * reff


def _fhys_over_kn(d, dmax, a, dl):
    """hooke/hysteresis 이력 가지 힘 ÷ kn (점착 가지 · 감쇠 제외) — normal_model_hooke_hysteresis.h:160–193."""
    if dmax >= dl:
        return a * (d - dl) + dl
    k2 = 1.0 + (a - 1.0) * dmax / dl
    ftmp = k2 * (d - dmax) + dmax
    return d if ftmp >= d else ftmp


def fixture_design(P=None, zero=False):
    """→ 자리 · 접촉 · 산술 검사.  zero = 모든 겹침을 −zero_gap 으로 (접촉 0 fixture · H5b)."""
    P = P or load_params()
    H = extract_head(P)
    R, M = H['radius'], H['m']
    zp, zm, gap = P['z_plate'], P['pair_mid_z'], P['zero_gap']
    lx, ly = P['box'][1] - P['box'][0], P['box'][3] - P['box'][2]
    dt = float(H['cmd']['dt'].split()[3])
    nsh = P['steps']['shear']
    parts = []
    anchors = {p['pair']: p for p in P['particles'] if p.get('role') == 'anchor'}
    for i, p in enumerate(P['particles'], start=1):
        t, r = p['type'], R[p['type']]
        dmax = -gap if zero and 'dmax' in p else p.get('dmax')
        d = -gap if zero and 'd' in p else p.get('d')
        if p['set'] == 'B':
            load, unl = (p['x'], p['y'], r - dmax), (p['x'], p['y'], r - d)
        elif p['set'] == 'T':
            load, unl = (p['x'], p['y'], zp - r + dmax), (p['x'], p['y'], zp - r + d)
        elif p['set'] == 'P' and p['role'] == 'anchor':
            load = unl = (p['x'], p['y'], zm)
        elif p['set'] == 'P':
            a = anchors[p['pair']]
            ra = R[a['type']]
            u = p['dir']
            load = tuple(c + uu * (ra + r - dmax) for c, uu in zip((a['x'], a['y'], zm), u))
            unl = tuple(c + uu * (ra + r - d) for c, uu in zip((a['x'], a['y'], zm), u))
        else:
            load = unl = (p['x'], p['y'], p['z'])
        parts.append(dict(p, id=i, r=r, load=load, unl=unl, v=p.get('v', [0.0, 0.0, 0.0])))

    def overlaps(key):
        bottom = [q['name'] for q in parts if q[key][2] - q['r'] < 0.0]
        top = [q['name'] for q in parts if q[key][2] + q['r'] > zp and q[key][2] < zp]
        pair, near = [], []
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                a, b = parts[i], parts[j]
                dx = (a[key][0] - b[key][0] + lx / 2) % lx - lx / 2
                dy = (a[key][1] - b[key][1] + ly / 2) % ly - ly / 2
                dz = a[key][2] - b[key][2]
                dist = math.sqrt(dx * dx + dy * dy + dz * dz)
                if dist < a['r'] + b['r']:
                    pair.append((a['name'], b['name']))
                elif dist < a['r'] + b['r'] + H['skin']:
                    near.append((a['name'], b['name']))
        return bottom, top, pair, near

    out = {'parts': parts, 'dt': dt}
    want_b = {q['name'] for q in parts if q['set'] == 'B'}
    want_t = {q['name'] for q in parts if q['set'] == 'T'}
    want_p = {tuple(sorted((anchors[q['pair']]['name'], q['name']))) for q in parts if q.get('role') == 'mover'}
    unintended, near_all = [], []
    for key in ('load', 'unl'):
        b, t, pr, near = overlaps(key)
        near_all += near
        if zero:
            unintended += [('bottom', x) for x in b] + [('top', x) for x in t] + [('pair', x) for x in pr]
        else:
            unintended += [('bottom', x) for x in set(b) ^ want_b] + [('top', x) for x in set(t) ^ want_t]
            unintended += [('pair', x) for x in {tuple(sorted(x)) for x in pr} ^ want_p]
        if key == 'unl':
            out['n_contacts'] = {'bottom': len(b), 'top': len(t), 'pair': len(pr)}
    out['unintended'] = unintended
    out['near'] = sorted(set(near_all)) if not zero else []
    seam, boundary, tension, regimes = [], [], [], set()
    cfrac, max_vn, straddle = 0.0, 0.0, 0
    for q in parts:
        x, y, z = q['unl']
        if not (q['r'] < x < lx - q['r'] and q['r'] < y < ly - q['r'] and P['box'][4] < z - q['r'] and z + q['r'] < P['box'][5]):
            boundary.append(q['name'])
        if zero or 'dmax' not in q:
            continue
        t = q['type']
        if q['set'] in ('B', 'T'):
            a, phi, mu, reff = M['k2max_over_kn'][t - 1][0], M['phiF'][t - 1][0], M['mu'][t - 1][0], q['r']
            normal = (0.0, 0.0, 1.0)
            if q['set'] == 'T':
                acont = math.sqrt(2.0 * q['r'] * q['dmax'])
                dseam = min(abs(x - y) / math.sqrt(2.0), x, y, lx - x, ly - y)
                if dseam <= 2.0 * acont:
                    seam.append(q['name'])
        else:
            an = anchors[q['pair']]
            ta = an['type']
            a, phi, mu = M['k2max_over_kn'][t - 1][ta - 1], M['phiF'][t - 1][ta - 1], M['mu'][t - 1][ta - 1]
            reff = q['r'] * R[ta] / (q['r'] + R[ta])
            normal = tuple(float(c) for c in q['dir'])
            ax, ay, _ = an['unl'] if False else (an['x'], an['y'], zm)
            if (min(ax, x) < 0.025 < max(ax, x)) or (min(ay, y) < 0.025 < max(ay, y)):
                straddle += 1
        dl = _dlim(a, phi, reff)
        regimes.add('sat' if q['dmax'] >= dl else 'unsat')
        if q.get('regime') and q['regime'] != ('sat' if q['dmax'] >= dl else 'unsat'):
            tension.append(q['name'] + ' (가지 표지 ≠ 산술)')
        f = _fhys_over_kn(q['d'], q['dmax'], a, dl)
        if not f > 0.0:
            tension.append(q['name'])
        s = math.sqrt(sum(c * c for c in q['v'])) * nsh * dt
        cfrac = max(cfrac, s / (mu * f) if f > 0 else float('inf'))
        max_vn = max(max_vn, abs(sum(c * nn for c, nn in zip(q['v'], normal))))
        q['design'] = {'dlim': dl, 'fhys_over_kn': f, 'shear_mag': s, 'regime': 'sat' if q['dmax'] >= dl else 'unsat'}
    out.update(seam=seam, boundary=boundary, tension=tension, coulomb_max_frac=cfrac, max_vn=max_vn, regimes=regimes,
               straddle_np4=straddle)
    return out


# ── 덱 ──────────────────────────────────────────────────────────────────────

def _fmt(cols):
    return ' '.join('%d' if c in ('id', 'type') else '%.17g' for c in cols)


def _r(x):
    return repr(float(x))


def _head_lines(H, plate=True, integr=True, read=True, P=None):
    c = H['cmd']
    out = [c['atom_style'], c['atom_modify'], c['boundary'], c['newton'], c['soft_particles'], c['communicate'], c['units'], '',
           c['r_AM_P'], c['r_AM_S'], c['r_SE'], c['dt'], c['timestep'], c['processors'], '']
    if read:
        out += ['read_restart ${ckpt}', '']
    else:
        b = P['box']
        out += [f'region hb_box block {_r(b[0])} {_r(b[1])} {_r(b[2])} {_r(b[3])} {_r(b[4])} {_r(b[5])} units box',
                'create_box 3 hb_box', '']
    out += [c['neighbor'], c['neigh_modify'], '']
    out += [c[f'm{m}'] for m in range(1, 10)] + ['']
    out += [c['pair_style'], c['pair_coeff'], '', c['strs'], c['ke'], c['cpl'], '', c['zwall_bot'], '']
    return out


def _dyn_lines(H, integr=True):
    c = H['cmd']
    out = [c['integr']] if integr else ['# (생산자 · SYN: 적분 fix 없음 — 운동학 fixture · 위치는 명령으로만 바뀐다)']
    out += [c['gravi'], c['top_mesh'].replace(H['plate_file'], '${plate_stl}'), c['zwall_top'], c['damp_relax'], c['energy'], '',
            c['pressMPa'], 'thermo_style custom step atoms ke cpu v_pressMPa']
    return out


#  r8 머리의 cpl (pair/gran/local) 은 머리 글자 그대로 두고 hb_ph 앞에서 내린다 — LIGGGHTS pair gran 은 pair/gran/local 을
#  하나만 받고 compute 를 만드는 순간 등록한다 (3d5c00f pair_gran.cpp:581 · compute_pair_gran_local.cpp post_create).
#  uncompute 는 pre_delete 로 등록을 푼다.  첫 ibb 실행 (job 281180) = 이 겹침으로 H0–H5 전부 TECH (README §1-5 · 원장 ULK-02).
DROP_CPL = ['# r8 머리 cpl 을 내린다 — pair gran 은 pair/gran/local 을 하나만 받는다 (만들 때 등록 · pair_gran.cpp:581) · 머리 글자는 그대로',
            'uncompute cpl']


def _obs_consumer(P, badid=False):
    O = P['observers']
    pre = list(O['atoms_pre'])
    if badid:
        pre = [x.replace('f_history_zwall_bot', 'f_history_zwallbot') for x in pre]
    return [
        'thermo 1',
        'variable hb_step_now equal step',
        'variable hb_step0 equal ${hb_step_now}',
        'variable hb_n_now equal atoms',
        'variable hb_n0 equal ${hb_n_now}',
        'print "HIST_CONSUMER_START step=${hb_step0} atoms=${hb_n0}"',
        '# PRE_SETUP — read_restart 뒤 벽 정의로 primitive 배열이 풀린 자리 · 첫 setup 전 (write_dump = 덤프 init → write · system setup 없음)',
        f'write_dump all custom ${{out}}/pre_atoms.dump {" ".join(pre)} modify format "{_fmt(pre)}"',
        '# POST_SETUP — run 0 의 setup · local 재평가 뒤 (deltaMax 상한 갱신 · 분리 소거 가능 · 시간 적분 없음)',
        'compute hb_wh all wall/gran/local id history',
        *DROP_CPL,
        'compute hb_ph all pair/gran/local id history',
        f'dump hb_dw all local 1000000 ${{out}}/post_mesh_*.dump {" ".join(O["mesh_local"])}',
        f'dump_modify hb_dw first yes format "{_fmt(O["mesh_local"])}"',
        f'dump hb_dp all local 1000000 ${{out}}/post_pair_*.dump {" ".join(O["pair_local"])}',
        f'dump_modify hb_dp first yes format "{_fmt(O["pair_local"])}"',
        f'dump hb_da all custom 1000000 ${{out}}/post_atoms_*.dump {" ".join(O["atoms_post"])}',
        f'dump_modify hb_da first yes format "{_fmt(O["atoms_post"])}"',
        'run 0',
        'undump hb_dw',
        'undump hb_dp',
        'undump hb_da',
    ]


HEADER = """\
# ============================================================
# DEM 언로딩 키트 — 작은 침대 이력 시험 (H0–H5) · @TITLE@
#   생성: history_test/make_history_decks.py (손으로 고치지 말 것 — 생성기를 고치고 다시 만든다 · SHA256SUMS)
#   정본: docs/data/ps45_unload_20261009/README.md §1 · 등록 §12-1 · §13-6 ③ · Codex 판정문 10-12 §5
#   변수: run_history.sh 가 -var 로 준다 — out (이 단계 폴더) · plate_stl (판 STL · 자료는 restart 에서) · ckpt (읽을 restart)
#   모델 머리 = r8 원 덱 글자 (재료 · pair · 벽 · 중력 9.81 · 감쇠 1.0e-5 · 메시) — 숫자를 다시 적지 않는다
@NOTE@
# ============================================================

"""

NOTES = {
    'producer': '#   생산자: 입자 20 (적분 없음) → 적재 (deltaMax) → 부분 제하 (set) → 접선 (속도 · run 1000) → 정지 (run 990) → 덤프 · restart',
    'producer_zero': '#   0 생산자 (H5b): 같은 덱 · 모든 겹침을 −zero_gap 으로 → 접촉 0 → 이력 0 뿐 (읽는 쪽 = INCONCLUSIVE 여야)',
    'consumer': '#   소비자: restart → 머리 → PRE_SETUP write_dump → run 0 (덤프 first yes) → POST_SETUP (H1 · H2 · H3 · H4 둘째 · H5b)',
    'erase_bot': '#   소거 (H3): 소비자와 같은 관측 → run 0 (첫 초기화 · restart 보관자료 해제) → undump · uncompute → unfix zwall_bot → 진단 restart',
    'erase_top': '#   소거 (H4): … → unfix zwall_top (top_mesh 기하는 그대로) → 진단 restart',
    'erase_none': '#   양성 대조: 같은 직렬화 횟수 · 벽 unfix 없음 → 진단 restart',
    'badid': '#   잘못된 내부 ID (H5a): history_zwallbot (없는 fix) → LIGGGHTS ERROR 가 나야 한다 (읽는 쪽 = TECH)',
    'syntax_probe': '#   SYN (판정 밖 · 정보): 본 키트 덱 문법 — read_restart 뒤 dt · erotate/sphere · ave/time · 부호 있는 Ps · 영역 개수 판 접촉 · '
                    'move/mesh +z · mesh 덤프 · 명시 write_restart',
    'grammar': '#   문법 fixture (Q8 · 등록 개정 3 §14-9 · Codex 판정문 10-14 §6 · 판정 = read_history.py --grammar): 본 키트 덱 상태 기계의 빠진 경로 —\n'
               '#     맨 바깥 include 상태 파일 + jump SELF 이어 돌림 · 변수 주기 덤프 (every v_) · 단마다 fix move/mesh 정의 · 해제 (판 z 누적) · 상태 파일 복귀.\n'
               '#     GA = -var gr_resume 0 (빈 상태 파일) · GB = -var gr_resume 1 (GA 마지막 단 끝 restart + 상태 파일 · 새 프로세스) · 짧은 문법 런 = 물리 검증 아님 (C19)',
}
TITLES = {'producer': '생산자', 'producer_zero': '0 생산자', 'consumer': '소비자', 'erase_bot': '바닥 소거', 'erase_top': '판 소거',
          'erase_none': '양성 대조', 'badid': '잘못된 ID', 'syntax_probe': '문법 미리 지나가기', 'grammar': '문법 fixture (상태 기계 · 이어 돌림)'}


def _producer(P, H, zero):
    D = fixture_design(P, zero=zero)
    O = P['observers']
    S = P['steps']
    final = S['load'] + S['shear'] + S['hold']
    L = _head_lines(H, read=False, P=P)
    L += ['# ── fixture 입자 (자리 = 생성기 계산 · 적재 자리 = 설계 deltaMax 겹침 · history_params.json)']
    for q in D['parts']:
        x, y, z = q['load']
        L.append(f'create_atoms {q["type"]} single {_r(x)} {_r(y)} {_r(z)} units box')
    for q in D['parts']:
        L.append(f'set atom {q["id"]} diameter {_r(2 * q["r"])} density {_r(H["density"][q["type"]])}')
    for g, s in (('hb_bot', 'B'), ('hb_top', 'T'), ('hb_pair', 'P'), ('hb_zero', 'Z')):
        L.append(f'group {g} id ' + ' '.join(str(q['id']) for q in D['parts'] if q['set'] == s))
    L += [''] + _dyn_lines(H, integr=False) + ['thermo 100', '',
          'compute hb_wh all wall/gran/local id history', *DROP_CPL, 'compute hb_ph all pair/gran/local id history',
          f'restart {S["auto_restart_every"]} ${{out}}/restart/auto_*.bin', '',
          '# ① 적재 — 첫 setup 에서 history[0] = max(0, δ) = 설계 deltaMax',
          'print "HIST_STAGE load"', f'run {S["load"]}', '',
          '# ② 부분 제하 — 순간 이동 (이력 유지 · 현재 겹침 δ < deltaMax)']
    for q in D['parts']:
        if q['set'] in ('B', 'T') or q.get('role') == 'mover':
            ax = [2] if q['set'] in ('B', 'T') else [k for k, u in enumerate(q['dir']) if u]
            L.append(f'set atom {q["id"]} ' + ' '.join(f'{"xyz"[k]} {_r(q["unl"][k])}' for k in ax))
    L += ['', '# ③ 접선 이력 — 적분이 없어 위치는 그대로 · shear += v_t·dt (법선에 수직)']
    for q in D['parts']:
        if any(q['v']):
            L.append(f'set atom {q["id"]} vx {_r(q["v"][0])} vy {_r(q["v"][1])} vz {_r(q["v"][2])}')
    L += ['print "HIST_STAGE shear"', f'run {S["shear"]}', 'velocity all set 0.0 0.0 0.0 units box', '',
          f'# ④ 정지 — 마지막 step ({final}) 의 in-run 덤프 = 봉인할 기대값 (생산자 끝)',
          f'dump hb_pa all custom {final} ${{out}}/producer/atoms_*.dump {" ".join(O["atoms_post"])}',
          f'dump_modify hb_pa format "{_fmt(O["atoms_post"])}"',
          f'dump hb_pw all local {final} ${{out}}/producer/mesh_*.dump {" ".join(O["mesh_local"])}',
          f'dump_modify hb_pw format "{_fmt(O["mesh_local"])}"',
          f'dump hb_pp all local {final} ${{out}}/producer/pair_*.dump {" ".join(O["pair_local"])}',
          f'dump_modify hb_pp format "{_fmt(O["pair_local"])}"',
          'print "HIST_STAGE hold"', f'run {S["hold"]}', 'undump hb_pa', 'undump hb_pw', 'undump hb_pp',
          'variable hb_step_now equal step', 'variable hb_step_end equal ${hb_step_now}',
          'variable hb_n_now equal atoms', 'variable hb_n_end equal ${hb_n_now}',
          f'write_dump all custom ${{out}}/producer/end_pack.dump {" ".join(O["atoms_pre"])} modify format "{_fmt(O["atoms_pre"])}"',
          'write_restart ${out}/fixture.bin',
          'print "HIST_PRODUCER_DONE step=${hb_step_end} atoms=${hb_n_end}"']
    return L


def _probe(P, H):
    Y = P['syntax_probe']
    zp = P['z_plate']
    ne, nr, nf = Y['ave']
    L = _head_lines(H, P=P) + _dyn_lines(H, integr=False)
    L += ['', '# dt 를 read_restart 뒤에 둔다 (restart 가 dt 를 되살린다 — UT 규약)', f'variable dt equal {Y["dt"]!r}', 'timestep ${dt}',
          'compute u_erot all erotate/sphere', 'compute u_ke all ke',
          'variable Ps equal f_top_mesh[3]/0.0025/1000000',
          f'fix u_av all ave/time {ne} {nr} {nf} v_Ps c_u_ke c_u_erot',
          'group u_t1 type 1', 'group u_t2 type 2', 'group u_t3 type 3',
          f'variable u_pz equal {_r(zp)}',
          'variable u_lo1 equal ${u_pz}-${r_AM_P}', 'variable u_lo2 equal ${u_pz}-${r_AM_S}', 'variable u_lo3 equal ${u_pz}-${r_SE}',
          'region u_c1 block INF INF INF INF ${u_lo1} ${u_pz} units box',
          'region u_c2 block INF INF INF INF ${u_lo2} ${u_pz} units box',
          'region u_c3 block INF INF INF INF ${u_lo3} ${u_pz} units box',
          'variable u_nc equal count(u_t1,u_c1)+count(u_t2,u_c2)+count(u_t3,u_c3)',
          '# 판 접촉 = (mesh index · 삼각형 · 입자 id · 입자가 받는 법선력 x y z) — 본 키트 TENSION 판별의 부호 약속 (압축 = fn_z 음수?) 을 먼저 잰다',
          'compute u_wh all wall/gran/local id force_normal',
          f'dump u_dw all local {nf} ${{out}}/probe/mesh_*.dump ' + ' '.join(f'c_u_wh[{i}]' for i in range(1, 7)),
          f'dump u_dm all mesh/stl {nf} ${{out}}/probe/plate_*.stl top_mesh',
          'thermo_style custom step atoms ke c_u_erot v_Ps v_pressMPa dt cpu', f'thermo {Y["thermo"]}',
          f'restart {Y["restart_every"]} ${{out}}/restart/probe_auto_*.bin', '',
          'print "SYN_START"', f'run {Y["window"]}']
    for tag in ('W0', 'W1'):
        if tag == 'W1':
            L += [f'fix u_lift all move/mesh mesh top_mesh linear 0.0 0.0 {Y["lift_v"]!r}', f'run {Y["lift_steps"]}', 'unfix u_lift',
                  f'variable u_pz equal ${{u_pz}}+{Y["lift_v"]!r}*${{dt}}*{Y["lift_steps"]}',
                  'variable u_lo1 equal ${u_pz}-${r_AM_P}', 'variable u_lo2 equal ${u_pz}-${r_AM_S}', 'variable u_lo3 equal ${u_pz}-${r_SE}',
                  'region u_c1 delete', 'region u_c1 block INF INF INF INF ${u_lo1} ${u_pz} units box',
                  'region u_c2 delete', 'region u_c2 block INF INF INF INF ${u_lo2} ${u_pz} units box',
                  'region u_c3 delete', 'region u_c3 block INF INF INF INF ${u_lo3} ${u_pz} units box',
                  f'run {Y["window"]}']
        L += ['variable u_step equal step', 'variable u_step equal ${u_step}',
              'variable u_P equal f_u_av[1]', 'variable u_P equal ${u_P}',
              'variable u_K equal f_u_av[2]', 'variable u_K equal ${u_K}',
              'variable u_R equal f_u_av[3]', 'variable u_R equal ${u_R}',
              'variable u_n equal ${u_nc}',
              'variable u_dtv equal dt', 'variable u_dtv equal ${u_dtv}',
              f'print "SYN_{tag} step=${{u_step}} Ps_avg=${{u_P}} ke_avg=${{u_K}} erot_avg=${{u_R}} n_contact_geo=${{u_n}} plate_z=${{u_pz}} dt=${{u_dtv}}"']
    L += ['undump u_dw', 'undump u_dm', 'write_restart ${out}/probe_end.bin', 'print "SYN_DONE"']
    return L


def _gr_regions(z):
    """판 접촉 영역 (본 키트 ul_c1–3 꼴 · 판 아래 반경 띠) — z = 판 높이 변수 글자."""
    out = []
    for i, r in ((1, 'r_AM_P'), (2, 'r_AM_S'), (3, 'r_SE')):
        out += [f'variable gr_lo{i} equal {z}-${{{r}}}', f'region gr_c{i} block INF INF INF INF ${{gr_lo{i}}} {z} units box']
    return out


def _grammar(P, H):
    """문법 fixture (Q8 · 등록 개정 3 §14-9) — 본 키트 U 덱 상태 기계의 꼴 그대로 (ul_ → gr_) · 빠진 경로만 한 번씩:
    맨 바깥 include ${gr_state} + if … jump SELF gr_resumed (이어 돌림) · 변수 주기 덤프 (dump_modify every v_gr_dnext — 창 전 = 다음 창 끝 ·
    이동 전 = step + big) · 단마다 fix move/mesh → run → unfix (판 z 누적) · 단 끝 write_restart + 상태 파일 (file · append) · 새 프로세스 복귀.
    적분 없음 (운동학 fixture — 입자는 그대로 · 판만 움직인다)."""
    Y = P['grammar_probe']
    ne, nr = Y['ave']
    afmt = ' '.join('%d' if c in ('id', 'type') else '%.17g' for c in Y['atom_cols'])
    L = _head_lines(H, P=P) + _dyn_lines(H, integr=False)
    L += ['', '# >>> block gr_params — 표 (history_params.json grammar_probe) 에서 온 숫자 (본 키트 ul_params 꼴)',
          f'variable gr_W equal {Y["window"]}', f'variable gr_n equal {Y["n_move"]}', f'variable gr_v equal {Y["v"]!r}',
          f'variable gr_kfresh equal {Y["k_fresh"]}', f'variable gr_big equal {Y["big"]}', f'variable gr_h0 equal {_r(P["z_plate"])}',
          'variable gr_resume index 0',
          '# 이어 돌림 대조 값 — 상태 파일이 다시 정의한다 (처음이면 빈 상태 파일 · −1 그대로)',
          'variable gr_rstep equal -1',
          'variable gr_dz equal ${gr_v}*${dt}*${gr_n}',
          '# <<< block gr_params', '',
          '# >>> block gr_obs — 관측 (본 키트 ul_obs 꼴 · 원자 · 판 local 덤프 = 변수 주기 · 판 mesh/stl = 고정 주기)',
          'compute gr_wh all wall/gran/local id force_normal',
          'variable Ps equal f_top_mesh[3]/0.0025/1000000',
          f'fix gr_av all ave/time {ne} {nr} ${{gr_W}} v_Ps',
          'group gr_t1 type 1', 'group gr_t2 type 2', 'group gr_t3 type 3']
    L += _gr_regions('${gr_h0}')
    L += ['variable gr_nc equal count(gr_t1,gr_c1)+count(gr_t2,gr_c2)+count(gr_t3,gr_c3)',
          'thermo_style custom step atoms ke v_Ps v_pressMPa cpu', 'thermo ${gr_W}',
          'variable gr_dnext equal step+${gr_big}',
          f'dump gr_da all custom ${{gr_W}} ${{out}}/probe/atom_*.dump {" ".join(Y["atom_cols"])}',
          f'dump_modify gr_da every v_gr_dnext format "{afmt}"',
          'dump gr_dw all local ${gr_W} ${out}/probe/wall_*.dump ' + ' '.join(f'c_gr_wh[{i}]' for i in range(1, 7)),
          'dump_modify gr_dw every v_gr_dnext format "' + ' '.join(['%.17g'] * 6) + '"',
          'dump gr_dm all mesh/stl ${gr_W} ${out}/probe/mesh_*.stl top_mesh',
          '# <<< block gr_obs', '',
          '# >>> block gr_start — 처음 또는 이어 돌림 (본 키트 start 꼴 · 상태 파일은 늘 맨 바깥 include — if 안 include = 3d5c00f input.cpp 845 ERROR)',
          'include ${gr_state}',
          'if "${gr_resume} == 1" then "jump SELF gr_resumed"',
          'variable gr_step equal step', 'variable gr_step equal ${gr_step}',
          'variable gr_k equal 0', 'variable gr_pz equal ${gr_h0}', 'variable gr_klast equal ${gr_kfresh}',
          'print "GRAM_START step=${gr_step} k=${gr_k} plate_z=${gr_pz}"',
          'jump SELF gr_window',
          'label gr_resumed',
          'variable gr_step equal step', 'variable gr_step equal ${gr_step}',
          'if "${gr_step} != ${gr_rstep}" then "print \'GRAM_ABORT reason=resume_step step=${gr_step} expect=${gr_rstep}\'" "quit"',
          'variable gr_klast equal ${gr_k}+1',
          'region gr_c1 delete', 'region gr_c2 delete', 'region gr_c3 delete']
    L += _gr_regions('${gr_pz}')
    L += ['print "GRAM_RESUMED step=${gr_step} k=${gr_k} plate_z=${gr_pz}"',
          'jump SELF gr_next',
          '# <<< block gr_start', '',
          '# >>> block gr_machine — 창 (덤프 = 창 끝) → 단 끝 restart + 상태 파일 → 이동 (덤프 없음) → 창 …',
          'label gr_window',
          'variable gr_dnext equal (floor(step/${gr_W})+1)*${gr_W}',
          'run ${gr_W}',
          'variable gr_step equal step', 'variable gr_step equal ${gr_step}',
          'variable gr_P equal f_gr_av[1]', 'variable gr_P equal ${gr_P}',
          'variable gr_ncnow equal ${gr_nc}',
          'print "GRAM_STEP k=${gr_k} step=${gr_step} plate_z=${gr_pz} Ps_avg=${gr_P} n_contact_geo=${gr_ncnow}"',
          'write_restart ${out}/restart/restart_g_${gr_step}.bin',
          'print "variable gr_rstep equal ${gr_step}" file ${out}/restart/state_g_${gr_step}.in screen no',
          'print "variable gr_k equal ${gr_k}" append ${out}/restart/state_g_${gr_step}.in screen no',
          'print "variable gr_pz equal ${gr_pz}" append ${out}/restart/state_g_${gr_step}.in screen no',
          'print "GRAM_STATE_WRITTEN step=${gr_step} k=${gr_k}"',
          'if "${gr_k} >= ${gr_klast}" then "jump SELF gr_done"',
          'label gr_next',
          'variable gr_k equal ${gr_k}+1',
          'variable gr_dnext equal step+${gr_big}',
          'fix gr_mv all move/mesh mesh top_mesh linear 0.0 0.0 ${gr_v}',
          'run ${gr_n}',
          'unfix gr_mv',
          'variable gr_pz equal ${gr_pz}+${gr_dz}',
          'region gr_c1 delete', 'region gr_c2 delete', 'region gr_c3 delete']
    L += _gr_regions('${gr_pz}')
    L += ['jump SELF gr_window',
          'label gr_done',
          'undump gr_da', 'undump gr_dw', 'undump gr_dm',
          'print "GRAM_DONE step=${gr_step} k=${gr_k} plate_z=${gr_pz}"',
          '# <<< block gr_machine']
    return L


def grammar_sim(text, start_step, z0, cli=None, includes=None, max_cmds=200000):
    """문법 fixture 덱의 제어문 · 덤프 시각 · 판 z 를 해석하는 작은 모의기 (입자 계산 없음 · 시험 전용 · Q8 — LIGGGHTS 대신이 아니다).
    variable (equal = 공식 · ${} 는 정의 때 치환 · 꺼낼 때 %.15g · index = 먼저 정의되면 그대로 · string) · if/then/else · jump SELF · label · quit ·
    include (includes[경로] 의 줄을 그 자리에서) · timestep · fix move/mesh linear (판 z += v · dt · n) · unfix · dump (custom · local · mesh/stl) ·
    dump_modify every v_ · first (run setup 에서 공식 = 다음 시각 · 그 시각 ≤ 지금 = 오류 · 쓴 뒤 다시) · undump · write_restart · print (화면 · file · append) ·
    run (고정 주기 덤프 = setup 에서 step % N = 0 이고 마지막이 그 step 아니면 · 그 뒤 N 배수).  f_* · count() = 0 (값은 보지 않는다).
    → {'runs': [(시작 step, n, 이동?)], 'dumps': {덤프 ID: [step]}, 'mesh_z': {step: z}, 'restarts': [step], 'files': {경로: 글자}, 'screen': [줄],
       'aborted', 'errors'}."""
    import math as _m
    L = logical_lines(text)
    Wd = [words(x) for x in L]
    labels = {w[1]: i for i, w in enumerate(Wd) if w[:1] == ['label']}
    var = {k: ('index', str(v)) for k, v in (cli or {}).items()}
    sim = {'step': start_step, 'z': z0, 'dt': None, 'vz': None, 'mover': None, 'runs': [], 'dumps': {}, 'mesh_z': {}, 'restarts': [], 'files': {},
           'screen': [], 'aborted': None, 'errors': []}
    dumps = {}

    def num(x):
        return '%.15g' % x

    def ev(expr, step=None):
        e = expr.replace('&&', ' and ').replace('||', ' or ')
        e = re.sub(r'\bf_\w+(?:\[\d+\])?', '0.0', e)
        e = re.sub(r'\bcount\([^)]*\)', '0', e)
        e = re.sub(r'\bstep\b', str(sim['step'] if step is None else step), e)
        return float(eval(e, {'__builtins__': {}}, {'abs': abs, 'floor': _m.floor}))   # noqa: S307 — 생성 덱의 숫자 식 (시험 전용)

    def get(name):
        st, v = var[name]
        return num(ev(v)) if st == 'equal' else v

    def sub(s):
        return re.sub(r'\$\{(\w+)\}', lambda mm: get(mm.group(1)), s)

    def write(did, t):
        sim['dumps'].setdefault(did, []).append(t)
        dumps[did]['last'] = t
        if dumps[did]['style'] == 'mesh/stl':
            sim['mesh_z'][t] = z_at(t)

    run_ctx = {'s': None, 'z': None, 'vz': 0.0}

    def z_at(t):
        return run_ctx['z'] + run_ctx['vz'] * sim['dt'] * (t - run_ctx['s'])

    def do(w):
        c = w[0]
        if c == 'variable' and len(w) >= 4:
            if w[2] == 'equal':
                var[w[1]] = ('equal', sub(' '.join(w[3:])))
            elif w[2] == 'string':
                var[w[1]] = ('string', sub(' '.join(w[3:])))
            elif w[2] == 'index' and w[1] not in var:
                var[w[1]] = ('index', sub(w[3]))
        elif c == 'timestep':
            sim['dt'] = float(sub(w[1]))
        elif c == 'include':
            path = sub(w[1])
            if path not in (includes or {}):
                raise RuntimeError(f'include 파일 없음: {path}')
            for ln in logical_lines(includes[path]):
                r = do(words(ln))
                if r is not None:
                    raise RuntimeError(f'include 안의 jump · quit: {ln}')
        elif c == 'if':
            branches, cur, conds, k = [], [], [w[1]], 3
            while k < len(w):
                if w[k] == 'elif':
                    branches.append(cur)
                    cur = []
                    conds.append(w[k + 1])
                    k += 2
                    continue
                if w[k] == 'else':
                    branches.append(cur)
                    cur = []
                    conds.append('1')
                else:
                    cur.append(w[k])
                k += 1
            branches.append(cur)
            for cond, br in zip(conds, branches):
                if ev(sub(cond)):
                    for cmd in br:
                        r = do(words(cmd))
                        if r is not None:
                            return r
                    break
        elif c == 'jump' and len(w) >= 3 and w[1] == 'SELF':
            return ('jump', labels[w[2]])
        elif c == 'quit':
            return ('quit',)
        elif c == 'fix' and len(w) >= 8 and w[3] == 'move/mesh':
            if sim['mover'] is not None:
                raise RuntimeError(f'move/mesh 가 이미 있다 ({sim["mover"]})')
            k = w.index('linear')
            sim['mover'], sim['vz'] = w[1], float(sub(w[k + 3]))
        elif c == 'unfix' and w[1] == sim['mover']:
            sim['mover'], sim['vz'] = None, None
        elif c == 'dump' and len(w) >= 5:
            dumps[w[1]] = {'style': w[3], 'every': int(float(sub(w[4]))), 'var': None, 'first': False, 'last': None}
        elif c == 'dump_modify':
            d = dumps[w[1]]
            k = 2
            while k < len(w):
                if w[k] == 'every':
                    d['var'] = w[k + 1][2:] if w[k + 1].startswith('v_') else None
                    if d['var'] is None:
                        d['every'] = int(float(sub(w[k + 1])))
                    k += 2
                elif w[k] == 'first':
                    d['first'] = w[k + 1] == 'yes'
                    k += 2
                elif w[k] == 'format':
                    k += 2
                else:
                    k += 1
        elif c == 'undump':
            dumps.pop(w[1], None)
        elif c == 'run':
            n = int(float(sub(w[1])))
            s, e = sim['step'], sim['step'] + n
            run_ctx.update(s=s, z=sim['z'], vz=sim['vz'] or 0.0)
            for did, d in dumps.items():
                if d['var']:
                    if d['first'] and d['last'] is None:
                        write(did, s)
                    nd = int(ev(var[d['var']][1], s))
                    if nd <= s:
                        raise RuntimeError(f'dump {did} every 변수가 지난 시각 ({nd} ≤ {s}) — Dump every variable returned a bad timestep')
                    while nd <= e:
                        write(did, nd)
                        nxt = int(ev(var[d['var']][1], nd))
                        if nxt <= nd:
                            raise RuntimeError(f'dump {did} every 변수가 지난 시각 ({nxt} ≤ {nd})')
                        nd = nxt
                else:
                    if (s % d['every'] == 0 and d['last'] != s) or (d['first'] and d['last'] is None):
                        write(did, s)
                    t = (s // d['every'] + 1) * d['every']
                    while t <= e:
                        write(did, t)
                        t += d['every']
            sim['runs'].append((s, n, sim['mover'] is not None))
            sim['z'] = z_at(e)
            sim['step'] = e
        elif c == 'write_restart':
            sim['restarts'].append(sim['step'])
        elif c == 'print':
            txt = sub(w[1])
            if len(w) >= 4 and w[2] in ('file', 'append'):
                path = sub(w[3])
                sim['files'][path] = (sim['files'].get(path, '') if w[2] == 'append' else '') + txt + '\n'
            else:
                sim['screen'].append(txt)
                if txt.startswith('GRAM_ABORT'):
                    sim['aborted'] = txt
        return None

    pc, n_cmds = 0, 0
    try:
        while pc < len(Wd) and n_cmds < max_cmds:
            n_cmds += 1
            r = do(Wd[pc])
            if r is None:
                pc += 1
            elif r[0] == 'jump':
                pc = r[1] + 1
            else:
                break
    except (RuntimeError, KeyError, ValueError, ZeroDivisionError) as ex:
        sim['errors'].append(f'{type(ex).__name__}: {ex}')
    if n_cmds >= max_cmds:
        sim['errors'].append('명령 수 상한 (고리?)')
    return sim


def render(name, P=None):
    P = P or load_params()
    H = extract_head(P)
    if name in ('producer', 'producer_zero'):
        L = _producer(P, H, zero=(name == 'producer_zero'))
    elif name in ('consumer', 'badid', 'erase_bot', 'erase_top', 'erase_none'):
        L = _head_lines(H, P=P) + _dyn_lines(H) + [''] + _obs_consumer(P, badid=(name == 'badid'))
        if name.startswith('erase'):
            mode = name.split('_')[1]
            L += ['# 소거 경로 (판정문 §5-3): 활성 wall local compute 를 둔 벽 unfix 는 거부 → 덤프 · compute 를 먼저 푼다',
                  'uncompute hb_wh', 'uncompute hb_ph']
            if mode == 'bot':
                L.append('unfix zwall_bot')
            elif mode == 'top':
                L.append('unfix zwall_top')
            L += ['write_restart ${out}/erased.bin', f'print "HIST_ERASE_DONE mode={mode} step=${{hb_step0}}"']
        else:
            L.append('print "HIST_CONSUMER_DONE step=${hb_step0} atoms=${hb_n0}"')
    elif name == 'syntax_probe':
        L = _probe(P, H)
    elif name == 'grammar':
        L = _grammar(P, H)
    else:
        raise KeyError(name)
    head = HEADER.replace('@TITLE@', TITLES[name]).replace('@NOTE@', NOTES[name])
    return head + '\n'.join(L) + '\n'


def plate_stl(P=None):
    P = P or load_params()
    z = _r(P['z_plate'])
    rows = ['solid plate', 'facet normal 0 0 -1', 'outer loop', f'vertex 0.0 0.0 {z}', f'vertex 0.05 0.05 {z}', f'vertex 0.05 0.0 {z}',
            'endloop', 'endfacet', 'facet normal 0 0 -1', 'outer loop', f'vertex 0.0 0.0 {z}', f'vertex 0.0 0.05 {z}',
            f'vertex 0.05 0.05 {z}', 'endloop', 'endfacet', 'endsolid plate']
    return '\n'.join(rows) + '\n'


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def generated_files(P=None):
    P = P or load_params()
    out = {fname: render(k, P) for k, fname in DECKS.items()}
    out[PLATE_STL] = plate_stl(P)
    return out


def sums_text():
    lines = []
    for name in SUMMED:
        p = os.path.join(HERE, name)
        if not os.path.exists(p):
            raise SystemExit(f'⛔ SHA256SUMS 대상이 없다: {name}')
        lines.append(f'{sha256_file(p)}  {name}')
    return '\n'.join(lines) + '\n'


def write_all():
    for name, text in generated_files().items():
        with open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    with open(os.path.join(HERE, SUMS), 'w', encoding='utf-8', newline='\n') as f:
        f.write(sums_text())
    print(f'✓ 덱 {len(DECKS)} · 판 STL · SHA256SUMS 를 다시 썼다')


def check():
    bad = []
    for name, text in generated_files().items():
        p = os.path.join(HERE, name)
        if not os.path.exists(p) or open(p, encoding='utf-8').read() != text:
            bad.append(f'{name}: 커밋본 ≠ 생성 결과 (make_history_decks.py 로 다시 만들 것)')
    sp = os.path.join(HERE, SUMS)
    if not os.path.exists(sp) or open(sp, encoding='utf-8').read() != sums_text():
        bad.append(f'{SUMS}: 현재 파일 해시와 다르다')
    for b in bad:
        print('✗', b)
    if not bad:
        print(f'✓ check: 덱 {len(DECKS)} · 판 STL = 생성 결과 · SHA256SUMS 일치 ({len(SUMMED)} 파일 · 러너 · 래퍼 · 읽는 쪽 포함)')
    return 1 if bad else 0


# ── selftest ─────────────────────────────────────────────────────────────────

def selftest() -> int:
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001 — 시험 대상의 예외도 실패로 센다 (빈 구현 · 고치기 전)
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)
        return ok

    P = load_params()
    # ① 표
    chk('① 표: 입자 이름 겹침 없음 · 집합 B · T · P · Z', lambda: len({p['name'] for p in P['particles']}) == len(P['particles'])
        and {p['set'] for p in P['particles']} == {'B', 'T', 'P', 'Z'})
    chk('① 표: 마지막 step = load + shear + hold = 2000', lambda: sum(P['steps'][k] for k in ('load', 'shear', 'hold')) == 2000)
    chk('① 표: 자동 restart 주기는 run 끝 step (10 · 1010 · 2000) 의 약수가 아니다 (끝 자동 쓰기를 가려낸다)',
        lambda: all(s % P['steps']['auto_restart_every'] for s in (10, 1010, 2000)))
    # ② 머리 = r8 원 덱 글자
    head = {}
    chk('② 머리: r8 원 덱 (리포 tgz) 에서 뽑는다 · 멤버 sha256 = 표', lambda: head.update(extract_head(P)) or head['sha256'] == P['head_source']['member_sha256'])
    for key in ('m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7', 'm8', 'm9', 'pair_style', 'pair_coeff', 'zwall_bot', 'gravi', 'integr',
                'top_mesh', 'zwall_top', 'damp_relax', 'energy', 'pressMPa', 'strs', 'ke', 'cpl', 'dt', 'r_AM_P', 'r_AM_S', 'r_SE'):
        chk(f'② 머리: {key} 가 r8 에서 정확히 하나', lambda key=key: key in head.get('cmd', {}))
    chk('② 머리: 이완 감쇠 = viscous 1.0e-5 (r8 145 행 · 압축 0.5 아님)', lambda: head['cmd']['damp_relax'].endswith('viscous 1.0e-5'))
    chk('② 머리: 중력 9.81 (정착 98.1 아님)', lambda: '9.81 vector' in head['cmd']['gravi'] and '98.1' not in head['cmd']['gravi'])
    chk('② 머리: 반경 r_AM_P 4.5e-3 · r_AM_S 2.0e-3 · r_SE 0.5e-3 · 밀도 4800 · 4800 · 2000 (원 덱 글자)',
        lambda: head['radius'] == {1: 4.5e-3, 2: 2.0e-3, 3: 0.5e-3} and head['density'] == {1: 4800.0, 2: 4800.0, 3: 2000.0})
    # ③ fixture 설계 (산술 · 덱 물성으로)
    D = {}
    chk('③ 설계: 계산된다', lambda: D.update(fixture_design(P)) or bool(D))
    chk('③ 설계: 의도한 접촉만 겹친다 (B–바닥 4 · T–판 4 · 쌍 5 · 주기 영상 포함 · 그 밖 0)',
        lambda: D['n_contacts'] == {'bottom': 4, 'top': 4, 'pair': 5} and not D['unintended'])
    chk('③ 설계: 의도 밖 이웃 (r_i + r_j + skin 안) 없음 — setup 의 분리 소거 경로 (surfacesClose) 를 피한다', lambda: not D['near'])
    chk('③ 설계: 판 접촉점이 대각 이음매 (x = y) 에서 접촉 반경 × 2 밖', lambda: not D['seam'])
    chk('③ 설계: 상자 안 · 주기 경계 x · y 에서 반경 밖', lambda: not D['boundary'])
    chk('③ 설계: 모든 sentinel 이 압축 가지 (f_hys > 0 · 점착 가지 아님) — 덱 m6 · m8 · 이력 식', lambda: not D['tension'])
    chk('③ 설계: 접선 이력 ≤ Coulomb 한도의 50 % (미끄럼 clip 경계 밖)', lambda: D['coulomb_max_frac'] <= 0.5)
    chk('③ 설계: 접선 속도 ⊥ 법선 (법선 감쇠 · 투영 없음)', lambda: D['max_vn'] == 0.0)
    chk('③ 설계: 포화 · 비포화 둘 다 있다 (벽 · 쌍)', lambda: D['regimes'] >= {'sat', 'unsat'})
    chk('③ 설계: 쌍 하나 이상이 NP 4 분할면 (x 또는 y = 0.025) 을 걸친다', lambda: D['straddle_np4'] >= 1)
    Z = {}
    chk('③ 설계: 0 fixture = 접촉 0 (모든 겹침 음수)', lambda: Z.update(fixture_design(P, zero=True)) or Z['n_contacts'] == {'bottom': 0, 'top': 0, 'pair': 0})
    # ④ 덱
    decks = {}
    chk(f'④ 덱: {len(DECKS)} 개가 만들어진다 (H0–H5 여덟 + 문법 fixture)', lambda: decks.update({k: render(k, P) for k in DECKS}) or set(decks) == set(DECKS))
    cli = {'out', 'plate_stl', 'ckpt'}
    for k in DECKS:
        text = decks.get(k, '')
        chk(f'④ {k}: 채우지 않은 @…@ · 탭 · `$` 꼴 · 주소 / 사용자 이름 없음',
            lambda text=text: text and not re.search(r'@[A-Z0-9_]+@', text) and '\t' not in text and not re.search(r'\$(?!\{)', text)
            and not re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|lustre|/home/|yonghoon|ibb-master', text))
        chk(f'④ {k}: 쓰인 ${{…}} 가 다 정의됨 (덱 안 · CLI out · plate_stl · ckpt' + (' · gr_state)' if k == 'grammar' else ')'),
            lambda text=text, k=k: text and _undefined(text, cli | ({'gr_state'} if k == 'grammar' else set())) == set())
        chk(f'④ {k}: run 사이 위험한 읽기 없음 (⑭a — write_restart 뒤 ke · run 0 뒤 메시 힘 · 없는 fix)', lambda text=text: text and scan_between_runs(text) == [])
        chk(f'④ {k}: 살아 있는 equal 정의 다음 줄 = 얼림 (⑭b)', lambda text=text: text and unfrozen_lazy(text) == [])
        chk(f'④ {k}: if 조건 = 숫자 · 비교 · 논리만', lambda text=text: text and _bad_if(text) == [])
        chk(f'④ {k}: 함께 사는 pair/gran/local ≤ 1 · wall/gran/local ≤ 1 · 내리는 compute 를 쓰는 덤프 없음 (⑮ — 첫 ibb 실행 TECH)',
            lambda text=text: text and _local_compute_problems(text) == [], '; '.join(_local_compute_problems(text)))
        chk(f'④ {k}: r8 머리 cpl 글자 그대로 (내리기만 하고 고치지 않는다)', lambda text=text: head['cmd']['cpl'] in _cmds(text))
    # ⑮ 규칙 자체 — 반례는 잡고 바른 꼴은 통과해야 (규칙이 비어 초록을 내지 않게)
    syn = {'둘 함께': 'compute a all pair/gran/local id\ncompute b all pair/gran/local id history\nrun 0\n',
           '덤프 살아 있는 uncompute': 'compute b all pair/gran/local id history\ndump d all local 1 x c_b[1]\nuncompute b\n',
           'wall 둘': 'compute w1 all wall/gran/local id\ncompute w2 all wall/gran/local id history\n',
           '내린 compute 를 쓰는 덤프': 'compute b all pair/gran/local id\nuncompute b\ndump d all local 1 x c_b[1]\n'}
    good = ('compute a all pair/gran/local id\nuncompute a\ncompute b all pair/gran/local id history\n'
            'compute w all wall/gran/local id history\ndump d all local 1 x c_b[1] c_w[1]\nrun 0\nundump d\nuncompute w\nuncompute b\n')
    chk('⑮ 규칙 자체: 반례 넷 (둘 함께 · 덤프 살아 있는 uncompute · wall 둘 · 내린 compute 덤프) 을 잡고 · 사이에 uncompute 한 꼴은 통과',
        lambda: all(_local_compute_problems(t) for t in syn.values()) and _local_compute_problems(good) == [])
    # ⑤ 소비자 (H1 · H2 · H3 · H4 둘째 단계 · H5b)
    c = decks.get('consumer', '')
    cl = _cmds(c)
    chk('⑤ 소비자: read_restart ${ckpt} 가 하나 · 첫 명령 묶음 뒤', lambda: [x for x in cl if x.startswith('read_restart')] == ['read_restart ${ckpt}'])
    chk('⑤ 소비자: PRE_SETUP write_dump (atoms_pre 열 그대로) 가 fix zwall_bot 뒤 · 첫 run 앞',
        lambda: _idx(cl, 'write_dump all custom ${out}/pre_atoms.dump ' + ' '.join(P['observers']['atoms_pre'])) > _idx(cl, 'fix zwall_bot ')
        and _idx(cl, 'write_dump all custom ${out}/pre_atoms.dump') < _idx(cl, 'run '))
    chk('⑤ 소비자: run 은 run 0 하나뿐', lambda: [x for x in cl if x.split()[0] == 'run'] == ['run 0'])
    chk('⑤ 소비자: wall · pair local compute 가 run 0 앞 · 덤프 셋 first yes · run 0 뒤 undump',
        lambda: _idx(cl, 'compute hb_wh all wall/gran/local id history') < _idx(cl, 'run 0')
        and _idx(cl, 'compute hb_ph all pair/gran/local id history') < _idx(cl, 'run 0')
        and all(_idx(cl, f'dump_modify {d} first yes') < _idx(cl, 'run 0') < _idx(cl, f'undump {d}') for d in ('hb_dw', 'hb_dp', 'hb_da')))
    chk('⑤ 소비자: 머리 fix 순서 = 원 PHASE 4 (zwall_bot → integr → gravi → top_mesh → zwall_top → damp 1e-5)',
        lambda: _order(cl, ['fix zwall_bot ', 'fix integr ', 'fix gravi ', 'fix top_mesh ', 'fix zwall_top ', 'fix damp all viscous 1.0e-5']))
    chk('⑤ 소비자: 머리 정의 글자 = r8 (재료 · pair · 벽 · 중력 · 감쇠 · 에너지)',
        lambda: all(head['cmd'][k] in cl for k in ('m1', 'm6', 'm7', 'm8', 'pair_style', 'pair_coeff', 'zwall_bot', 'gravi', 'integr', 'zwall_top', 'damp_relax', 'energy')))
    chk('⑤ 소비자: 판 STL = ${plate_stl} (메시 자료는 restart 에서)', lambda: head['cmd']['top_mesh'].replace(head['plate_file'], '${plate_stl}') in cl)
    # ⑥ 소거 (H3 · H4 · 양성 대조)
    for mode, want in (('erase_bot', ['unfix zwall_bot']), ('erase_top', ['unfix zwall_top']), ('erase_none', [])):
        e = _cmds(decks.get(mode, ''))
        chk(f'⑥ {mode}: run 0 → undump 셋 → uncompute 둘 → unfix {want or "없음"} → write_restart (순서)',
            lambda e=e, want=want: [x for x in e if x.startswith('unfix')] == want
            and _idx(e, 'run 0') < min(_idx(e, 'undump hb_dw'), _idx(e, 'undump hb_dp'), _idx(e, 'undump hb_da'))
            and max(_idx(e, 'undump hb_dw'), _idx(e, 'undump hb_dp'), _idx(e, 'undump hb_da')) < _idx(e, 'uncompute hb_wh')
            and _idx(e, 'uncompute hb_ph') < (_idx(e, want[0]) if want else _idx(e, 'write_restart ${out}/erased.bin'))
            and _idx(e, 'write_restart ${out}/erased.bin') > max([_idx(e, w) for w in want] + [_idx(e, 'uncompute hb_ph')]))
        chk(f'⑥ {mode}: top_mesh 는 지우지 않는다 · run 은 run 0 하나', lambda e=e: 'unfix top_mesh' not in e and [x for x in e if x.split()[0] == 'run'] == ['run 0'])
    # ⑦ 생산자
    p = _cmds(decks.get('producer', ''))
    chk('⑦ 생산자: create_box · 적분 fix 없음 (운동학 fixture)', lambda: any(x.startswith('create_box 3 ') for x in p) and not any(x.startswith('fix integr') for x in p))
    chk('⑦ 생산자: run 10 → run 1000 → run 990 (표)', lambda: [x for x in p if x.split()[0] == 'run'] == ['run 10', 'run 1000', 'run 990'])
    chk('⑦ 생산자: 입자 20 개 create_atoms single … units box', lambda: sum(1 for x in p if x.startswith('create_atoms ') and x.endswith('units box')) == 20)
    chk('⑦ 생산자: 속도 0 이 마지막 run 앞 · 덤프 셋 주기 2000 이 마지막 run 앞',
        lambda: _idx(p, 'velocity all set 0.0 0.0 0.0 units box') < _last(p, 'run ')
        and all(_idx(p, f'dump {d} all ') < _last(p, 'run ') for d in ('hb_pa', 'hb_pw', 'hb_pp'))
        and all(' 2000 ' in p[_idx(p, f'dump {d} all ')] for d in ('hb_pa', 'hb_pw', 'hb_pp')))
    chk('⑦ 생산자: 끝 write_dump 묶음 → write_restart fixture.bin (마지막 run 뒤)',
        lambda: _last(p, 'run ') < _idx(p, 'write_dump all custom ${out}/producer/end_pack.dump') < _idx(p, 'write_restart ${out}/fixture.bin'))
    chk('⑦ 생산자: 자동 restart 1500 이 첫 run 앞 (H0b)', lambda: _idx(p, 'restart 1500 ${out}/restart/auto_*.bin') < _idx(p, 'run '))
    pz = _cmds(decks.get('producer_zero', ''))
    chk('⑦ 0 생산자: 생산자와 create_atoms · set 위치 줄만 다르다', lambda: _diff_kinds(p, pz) <= {'create_atoms', 'set'})
    # ⑧ 잘못된 ID (H5a)
    b = _cmds(decks.get('badid', ''))
    chk('⑧ 잘못된 ID: 소비자와 history 열 이름만 다르다 (history_zwallbot — 없는 fix)',
        lambda: len(b) == len(cl) and [i for i, (x, y) in enumerate(zip(cl, b)) if x != y] == [_idx(cl, 'write_dump all custom ${out}/pre_atoms.dump')]
        and 'f_history_zwallbot[1]' in b[_idx(cl, 'write_dump all custom ${out}/pre_atoms.dump')])
    # ⑨ 문법 미리 지나가기 (SYN)
    s = _cmds(decks.get('syntax_probe', ''))
    chk('⑨ SYN: timestep 이 read_restart 뒤에도 있다 (dt 5e-7 · restart 가 dt 를 되살리는 규약)',
        lambda: _idx(s, 'read_restart ${ckpt}') < _last(s, 'timestep ${dt}') and _last(s, 'variable dt equal 5e-07') < _last(s, 'timestep ${dt}')
        and _idx(s, 'read_restart ${ckpt}') < _last(s, 'variable dt equal 5e-07'))
    chk('⑨ SYN: erotate/sphere · ave/time · 부호 있는 Ps · 판 이동 +z · unfix · 명시 write_restart',
        lambda: _idx(s, 'compute u_erot all erotate/sphere') >= 0 and any(x.startswith('fix u_av all ave/time 10 10 100 ') for x in s)
        and 'variable Ps equal f_top_mesh[3]/0.0025/1000000' in s and 'fix u_lift all move/mesh mesh top_mesh linear 0.0 0.0 0.01' in s
        and _idx(s, 'unfix u_lift') > _idx(s, 'fix u_lift all move/mesh mesh top_mesh linear 0.0 0.0 0.01')
        and _idx(s, 'write_restart ${out}/probe_end.bin') > _last(s, 'run '))
    chk('⑨ SYN: 적분 fix 없음 (운동학 · 판 이동 기하만)', lambda: not any(x.startswith('fix integr') for x in s))
    chk('⑨ SYN: 판 접촉 local = id force_normal (6 열 — 본 키트 TENSION 판별의 부호 약속을 먼저 잰다)',
        lambda: 'compute u_wh all wall/gran/local id force_normal' in s
        and any(x.startswith('dump u_dw all local ') and x.endswith(' '.join(f'c_u_wh[{i}]' for i in range(1, 7))) for x in s))
    # ⑩ 판 STL · 러너 짝 · 봉인
    chk('⑩ 판 STL: 삼각형 둘 · 높이 하나 = z_plate', lambda: plate_stl(P).count('vertex') == 6
        and set(re.findall(r'vertex \S+ \S+ (\S+)', plate_stl(P))) == {repr(P['z_plate'])})
    sb = _read(os.path.join(HERE, SBATCH))
    rb = _read(os.path.join(HERE, RUNNER))
    chk('⑩ 래퍼: #SBATCH -n = np_main (6) · 하나뿐', lambda: [x for x in sb.splitlines() if x.startswith('#SBATCH -n ')] == [f"#SBATCH -n {P['np_main']}"])
    chk('⑩ 래퍼: SLURM_NTASKS = NP 대조 · 밖이면 사전 점검만', lambda: '"${SLURM_NTASKS:-}" != "$NP"' in sb and 'run_history.sh" --preflight-only' in sb)
    chk('⑩ 러너: mpirun 줄 = "$MPIRUN" $MPIRUN_FLAGS -np "$np" · 기본 --oversubscribe --bind-to none',
        lambda: '"$MPIRUN" $MPIRUN_FLAGS -np "$np" "$LMP"' in rb and 'MPIRUN_FLAGS=${MPIRUN_FLAGS:---oversubscribe --bind-to none}' in rb)
    chk('⑩ 러너: 단계마다 Loop time … on N procs 의 N = 그 단계 NP 를 본다 (읽는 쪽 H0)', lambda: 'np.txt' in rb)
    chk('⑩ 러너: kit 사본 목록 = SHA256SUMS 대상 + SHA256SUMS', lambda: _kit_list(rb) == set(SUMMED) | {SUMS})
    chk('⑩ 래퍼 · 러너: 주소 · 포트 · 사용자 이름 없음', lambda: not re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|-P\s*\d{2,5}\b|yonghoon|ibb-master', sb + rb))
    for path in (os.path.join(HERE, SBATCH), os.path.join(HERE, RUNNER)):
        chk(f'⑩ bash -n {os.path.basename(path)}', lambda path=path: subprocess.run(['bash', '-n', path], capture_output=True).returncode == 0)
    # ⑪ 검사기 자신 (⑭a · ⑭b 반례 — 가지 키트 10-07 t0 1 회의 꼴)
    syn = 'read_restart ${ckpt}\nthermo_style custom step atoms ke\nfix top_mesh all mesh/surface/stress file x type 1\n'
    chk('⑪ 검사기: write_restart 뒤 살아 있는 ke 를 잡는다',
        lambda: {h[2] for h in scan_between_runs(syn + 'run 5\nvariable k equal ke\nwrite_restart a.bin\nprint "${k}"\n')} == {'stale'})
    chk('⑪ 검사기: run 0 뒤 메시 힘을 잡는다',
        lambda: {h[2] for h in scan_between_runs(syn + 'run 5\nrun 0\nvariable F equal f_top_mesh[3]\nprint "${F}"\n')} == {'setup'})
    chk('⑪ 검사기: 얼린 정의는 놓아 준다', lambda: unfrozen_lazy('variable k equal ke\nvariable k equal ${k}\n') == [])
    # ⑯ 문법 fixture (Q8 · 등록 개정 3 §14-9 · Codex 판정문 10-14 §6) — 본 키트 덱 상태 기계의 빠진 경로: 맨 바깥 include 상태 파일 + jump SELF 이어 돌림 ·
    #    변수 주기 덤프 (every v_) · 단마다 move/mesh 정의 · 해제 (판 z 누적) · 상태 파일 복귀 (새 프로세스).  모의기로 GA (처음) → GB (GA 마지막 상태 파일) 를
    #    끝까지 해석해 읽는 쪽 기대 (read_history.grammar_expect) 와 대조한다 — 실제 바이너리 확인은 ibb 한 번 (1저자 · README §1-6).
    g = decks.get('grammar', '')
    gl = _cmds(g)
    Y = P.get('grammar_probe', {})
    chk('⑯ 문법: 덱이 있다 · 상태 파일 include = 맨 바깥 하나 (if 안 아님 · 3d5c00f input.cpp 845) · 이어 돌림 분기 앞 · gr_resume = index (CLI 가 이긴다)',
        lambda: g and [x for x in gl if x.startswith('include')] == ['include ${gr_state}']
        and _idx(gl, 'include ${gr_state}') < _idx(gl, 'if "${gr_resume} == 1" then "jump SELF gr_resumed"') < 10 ** 9 and 'variable gr_resume index 0' in gl)
    chk('⑯ 문법: 변수 주기 덤프 둘 (원자 custom · 판 local) = dump_modify … every v_gr_dnext · first yes 없음 · 판 mesh/stl = 고정 주기 (창)',
        lambda: any(x.startswith('dump_modify gr_da every v_gr_dnext') for x in gl) and any(x.startswith('dump_modify gr_dw every v_gr_dnext') for x in gl)
        and not any('first yes' in x for x in gl) and 'dump gr_dm all mesh/stl ${gr_W} ${out}/probe/mesh_*.stl top_mesh' in gl)
    chk('⑯ 문법: 이동 = fix gr_mv move/mesh → run ${gr_n} → unfix gr_mv (붙어 있다 · 한 자리 — 단마다 다시 정의) · 이동 전 gr_dnext = step + big · 창 전 = 다음 창 끝',
        lambda: (lambda i: i < 10 ** 9 and gl[i + 1] == 'run ${gr_n}' and gl[i + 2] == 'unfix gr_mv' and gl[i - 1] == 'variable gr_dnext equal step+${gr_big}')(
            _idx(gl, 'fix gr_mv all move/mesh mesh top_mesh linear 0.0 0.0 ${gr_v}'))
        and sum(1 for x in gl if x.startswith('fix gr_mv ')) == 1
        and gl[_idx(gl, 'run ${gr_W}') - 1] == 'variable gr_dnext equal (floor(step/${gr_W})+1)*${gr_W}')
    chk('⑯ 문법: 단 끝 write_restart → 상태 파일 (file → append 둘) · 이어 돌림 = step 대조 (≠ → quit) · 적분 fix 없음 (운동학 fixture)',
        lambda: _idx(gl, 'write_restart ${out}/restart/restart_g_${gr_step}.bin') < _idx(gl, 'print "variable gr_rstep equal ${gr_step}" file ')
        < _idx(gl, 'print "variable gr_k equal ${gr_k}" append ') < _idx(gl, 'print "variable gr_pz equal ${gr_pz}" append ') < 10 ** 9
        and any(x.startswith('if "${gr_step} != ${gr_rstep}" then') and x.endswith('"quit"') for x in gl) and not any(x.startswith('fix integr') for x in gl))
    chk('⑯ 표: grammar_probe dt = 머리 dt · 이동 · 반 이동 = 창 배수 · k_fresh ≥ 2 (move/mesh 를 처음 프로세스에서 두 번)',
        lambda: Y['dt'] == float(head['cmd']['dt'].split()[3]) and Y['n_move'] % Y['window'] == 0 and (Y['n_move'] // 2) % Y['window'] == 0
        and Y['k_fresh'] >= 2)
    GS = {}

    def _gsim():
        sys.path.insert(0, HERE)
        import read_history as RH  # noqa: E402 — 같은 폴더 읽는 쪽 (기대값 = 표에서)
        E = RH.grammar_expect(P)
        a = grammar_sim(g, E['GA']['start'], z0=E['GA']['z0'], cli={'out': 'OUT', 'gr_state': 'FRESH', 'gr_resume': '0'},
                        includes={'FRESH': '# 처음 (빈 상태 파일)\n'})
        st = a['files'].get(f'OUT/restart/state_g_{E["GA"]["ends"][-1]}.in', '')
        b = grammar_sim(g, E['GB']['start'], z0=E['GB']['z0'], cli={'out': 'OUT', 'gr_state': 'STATE', 'gr_resume': '1'}, includes={'STATE': st})
        GS.update(E=E, A=a, B=b)
        return True
    chk('⑯ 모의기 GA (처음): run = 창 · 이동 · 창 · 이동 · 창 · 변수 주기 덤프 (원자 · 판) = 창 끝만 (setup · 이동 중 없음) · restart = 창 끝 · 오류 없음',
        lambda: _gsim() and not GS['A']['errors'] and GS['A']['aborted'] is None
        and [(s, n, mv) for s, n, mv in GS['A']['runs']] == GS['E']['GA']['runs']
        and GS['A']['dumps'].get('gr_da') == GS['E']['GA']['ends'] == GS['A']['dumps'].get('gr_dw') and GS['A']['restarts'] == GS['E']['GA']['ends'])
    chk('⑯ 모의기 GA: 판 z (mesh/stl 고정 주기) = 읽는 쪽 기대 (두 번째 이동이 앞 이동 위로 쌓인다 · 창 동안 그대로) · 상태 파일 셋 = (rstep · k · pz)',
        lambda: all(abs(GS['A']['mesh_z'].get(s, -1.0) - z) <= 1e-12 for s, z in GS['E']['GA']['mesh'].items())
        and all(GS['A']['files'].get(f'OUT/restart/state_g_{e}.in') == f'variable gr_rstep equal {e}\nvariable gr_k equal {k}\nvariable gr_pz equal {"%.15g" % z}\n'
                for k, (e, z) in enumerate(zip(GS['E']['GA']['ends'], GS['E']['GA']['z']))))
    chk('⑯ 모의기 GB (GA 마지막 상태 파일 그대로 include · 새 프로세스): 이어 돌림 분기 → 이동 하나 → 창 · 덤프 = 그 창 끝 · restart 하나 · 판 z 이어서',
        lambda: not GS['B']['errors'] and GS['B']['aborted'] is None and [(s, n, mv) for s, n, mv in GS['B']['runs']] == GS['E']['GB']['runs']
        and GS['B']['dumps'].get('gr_da') == GS['E']['GB']['ends'] == GS['B']['dumps'].get('gr_dw') and GS['B']['restarts'] == GS['E']['GB']['ends']
        and all(abs(GS['B']['mesh_z'].get(s, -1.0) - z) <= 1e-12 for s, z in GS['E']['GB']['mesh'].items()))
    chk('⑯ 모의기 화면 표지 = 읽는 쪽이 읽는 꼴 (GA: GRAM_START · GRAM_STEP k 0 … · GRAM_DONE / GB: GRAM_RESUMED · GRAM_STEP k k_fresh + 1 · GRAM_DONE)',
        lambda: (lambda RH: RH.gram_markers_ok(GS['A']['screen'], GS['E']['GA'], resumed=False) == []
                 and RH.gram_markers_ok(GS['B']['screen'], GS['E']['GB'], resumed=True) == [])(__import__('read_history')))

    def _mut(old, new):
        t = g.replace(old, new, 1)
        E = GS['E']
        return grammar_sim(t, E['GA']['start'], z0=E['GA']['z0'], cli={'out': 'OUT', 'gr_state': 'FRESH', 'gr_resume': '0'},
                           includes={'FRESH': '# 처음\n'})
    chk('⑯ 모의기 자신 (판별력): 이동 전 gr_dnext = step + big 을 빼면 이동 중 덤프 · dump_modify 에 first yes 를 더하면 setup 덤프 를 잡는다',
        lambda: GS['E']['GA']['ends'] != _mut('variable gr_dnext equal step+${gr_big}\nfix gr_mv', 'fix gr_mv')['dumps'].get('gr_da')
        and _mut('dump_modify gr_da every v_gr_dnext', 'dump_modify gr_da first yes every v_gr_dnext')['dumps'].get('gr_da', [None])[0] == GS['E']['GA']['start'])
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


# ── selftest 도우미 (구현과 독립 — 덱 글자를 그대로 읽는다) ─────────────────────────────

def _read(path):
    return open(path, encoding='utf-8').read() if os.path.exists(path) else ''


def _cmds(text):
    try:
        return logical_lines(text)
    except Exception:  # noqa: BLE001
        return []


def _idx(lines, prefix):
    for i, x in enumerate(lines):
        if x.startswith(prefix):
            return i
    return 10 ** 9


def _last(lines, prefix):
    j = -1
    for i, x in enumerate(lines):
        if x.startswith(prefix):
            j = i
    return j


def _order(lines, prefixes):
    pos = [_idx(lines, p) for p in prefixes]
    return all(p < 10 ** 9 for p in pos) and pos == sorted(pos)


def _diff_kinds(a, b):
    if len(a) != len(b):
        return {'length'}
    return {x.split()[0] for x, y in zip(a, b) if x != y}


def _undefined(text, cli):
    used = set(re.findall(r'\$\{([A-Za-z0-9_]+)\}', text))
    defined = set(cli)
    for ln in logical_lines(text):
        w = ln.split()
        if len(w) >= 3 and w[0] == 'variable':
            defined.add(w[1])
        if w and w[0] == 'if':
            for sub in re.findall(r'"variable (\w+) ', ln):
                defined.add(sub)
    return used - defined


def _bad_if(text):
    bad = []
    for ln in logical_lines(text):
        w = words(ln)
        if w[:1] == ['if']:
            cond = re.sub(r'\$\{\w+\}', '1', w[1])
            cond = re.sub(r'\d+\.?\d*(?:[eE][-+]?\d+)?', '1', cond)
            if re.search(r'[A-Za-z_]|[+*/]', cond) or re.search(r'\d\s*-\s*\d', cond):
                bad.append(ln)
    return bad


LOCAL_STYLES = ('pair/gran/local', 'wall/gran/local')


def _local_compute_problems(text):
    """⑮ LIGGGHTS 는 compute pair/gran/local · wall/gran/local 을 **만드는 순간** pair gran · 벽 fix 에 등록하고 (post_create →
    init_cpgl → register_*) 하나만 받는다 (공개 3d5c00f pair_gran.cpp:581 · fix_wall_gran.cpp:1236 — compute_pair_gran_local.cpp
    sha256 71c4d3b5… = docs/data/liggghts_add_pair_pin.json 의 ibb · WSL 소스).  uncompute 가 등록을 푼다 (pre_delete).
    덱 순서대로 살아 있는 개수와 덤프 참조를 센다 — 첫 ibb 실행 (job 281180) 의 TECH (r8 머리 cpl + hb_ph) 를 런 전에 잡는다."""
    live = {s: [] for s in LOCAL_STYLES}
    defined, dumps, bad = set(), {}, []
    for ln in _cmds(text):
        w = ln.split()
        if w[0] == 'compute' and len(w) > 3:
            if w[3] in live:
                if live[w[3]]:
                    bad.append(f'{w[3]} 둘이 함께 산다 ({live[w[3]][0]} · {w[1]})')
                live[w[3]].append(w[1])
            defined.add(w[1])
        elif w[0] == 'uncompute' and len(w) > 1:
            users = sorted(d for d, refs in dumps.items() if w[1] in refs)
            if users:
                bad.append(f'uncompute {w[1]} 때 그것을 쓰는 덤프가 살아 있다 ({", ".join(users)})')
            for ids in live.values():
                if w[1] in ids:
                    ids.remove(w[1])
            defined.discard(w[1])
        elif w[0] == 'dump' and len(w) > 1:
            refs = set(re.findall(r'\bc_([A-Za-z0-9_]+)', ln))
            if refs - defined:
                bad.append(f'dump {w[1]} 가 살아 있지 않은 compute 를 쓴다 ({", ".join(sorted(refs - defined))})')
            dumps[w[1]] = refs
        elif w[0] == 'undump' and len(w) > 1:
            dumps.pop(w[1], None)
    return bad


def _kit_list(rb):
    m = re.search(r'for f in (in\.hist_producer\.liggghts.*?); do', rb, re.S)
    return set(m.group(1).replace('\\\n', ' ').split()) if m else set()


def main(argv=None):
    ap = argparse.ArgumentParser(description='DEM 언로딩 키트 — 작은 침대 이력 시험 덱 생성기 (H0–H5)')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--check', action='store_true', help='커밋본 = 생성 결과 · SHA256SUMS 일치 (다르면 rc 1)')
    g.add_argument('--selftest', action='store_true', help='구조 · 설계 · run 사이 읽기 · 러너 짝 검사')
    a = ap.parse_args(argv)
    if a.check:
        return check()
    if a.selftest:
        return selftest()
    write_all()
    return 0


if __name__ == '__main__':
    sys.exit(main())
