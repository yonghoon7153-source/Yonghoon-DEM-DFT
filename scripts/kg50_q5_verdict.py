#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""50kg Q5 판독기 — 가지 폴더 (q5 덤프 · 로그 · manifest) → O1 · O2 · O3 (+ R1–R6 보고) → §7 판정 (읽기만).

등록 = `docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md` (1저자 10-27 밤 비준 · Q1–Q12 = 머리 비준 표).
  가지 폴더 = `scripts/kg50_q5_branches.py` 가 만든 폴더 (q5_manifest.json · 가지 덱 · 본 덱 사본) + 런이 남긴 것
  (log.liggghts · post_<case>/q5atom_<step>.liggghts · q5contact_<step>.liggghts) + 운영자 ckpt_sha256.txt.

관측량 (§6 · 허용 오차 = Q4 — 결과 전 고정)
  T0  기술 — 끝까지 돎 (`Loop time of` 줄 수 · step 수 = 덱 run) · ERROR 0 · thermo 비유한 없음 · 마지막 thermo step = 창 끝
      (원자 수는 기록만 · 1저자 10-27)
  O1  SE · AM 질량 중심 높이 z̄ = Σ ρ r³ z / Σ ρ r³ (창 끝 atom 덤프)                  상대 0.5 %   W1 판정
  O2  평균 접촉 수 — AM–AM (AM 당) · AM–SE (AM 당) · SE–SE (SE 당) · 전체 (입자당)  상대 5 %     W1 · W2 판정
      (창 끝 contact 덤프 id 두 열 c_cpl[7] · c_cpl[8] + 같은 step atom 덤프 type)
  O3  판 압력 — 창 마지막 0.05 s (양 끝 포함) 의 thermo pressMPa 평균                 상대 5 %     W2 판정
  R1 KE (창 끝 thermo) · R2 윗면 z + r 최대 · 99 % · R3 겹침 δ/R* 50 · 99 % (쌍 종류별) · R4 위치 차 RMS 비 (id 대응 ·
  x · y 주기 최소상) · R5 감쇠 저항 몫 (W2) · R6 PLATE HEIGHT = 보고 (판정 밖)
  "같은 시각" = manifest compare_step (A · C · F 400002 ↔ B 600003 = 체크포인트 뒤 0.200001 s)

판정 (§7 — 결정 관측량 o 마다 · X ↔ A · 바닥 F · 위에서부터 먼저 걸리는 것)
  ① X · A · F 중 하나라도 T0 실패            → 판정 불가 (기술)
  ② |F − A| / |A| > τ_o                      → 판정 불가 (그 창이 τ 를 가를 해상도가 없다)
  ③ |X − A| / |A| > τ_o                      → 불합격
  ④ 그 밖 (|X − A| = τ 는 합격)              → 합격
  (a) = X = B (D0.7) · (b) = X = C (D0.7) · C3 (D3 · 바닥 F3 · Q2 (가)) — 침대마다 따로 · 전체 = 나쁜 쪽
  (불합격 > 판정 불가 > 합격) · W1 · W2 를 둘 다 하면 창마다 따로 · 전체 = 나쁜 쪽 (`--combine`)
  W1 만으로 낸 (b) 합격 = "안정화 창에서 감쇠 민감도 τ 안" 까지만 (한정어를 결과에 붙인다)
  값이 없거나 비유한이거나 |A| = 0 이면 그 항목 = 판정 불가 (상대 차를 정할 수 없다)

입력 거부 (rc 2 · 판정 없음 · fail-closed): manifest 꼴 · 역할 ↔ 가지 · 덱 sha256 · 허용 목록 다시 대조 (리포 생성기) ·
  ckpt_sha256.txt (두 줄 · 같은 해시 · 침대 안 같음) · 로그 없음 · procs ≠ NP · dt 치환 줄 · 덱 명령 ↔ 로그 echo · 첫 step ·
  덤프 빠짐 · 남는 덤프 · TIMESTEP ≠ 이름 · 프레임 둘 · 줄 수 ≠ 머리 · 줄 꼴 · 비유한 · 중복 id · 모르는 type · 열 다름 ·
  접촉 중복 쌍 · 자기 쌍 · 원자 덤프에 없는 id · 시작 상태 (t0 덤프) 가 가지마다 다름 · 끝 상태가 두 가지에서 같음 ·
  F 의 NP = A 의 NP · 같은 폴더 두 역할 · 창 · 침대 섞임 · (W2) O3 표본 시각이 가지마다 다름.
  T0 실패 가지는 덤프를 요구하지 않는다 (그 비교 = 판정 불가 (기술)).

사용 (리포 안 · 결과를 받은 기계)
    python3 scripts/kg50_q5_verdict.py --branch A=<폴더> --branch B=<폴더> --branch C=<폴더> --branch F=<폴더> \\
        [--branch A3=<폴더> --branch C3=<폴더> --branch F3=<폴더>] [--json out.json] [--main-log <본 런 log>]
    python3 scripts/kg50_q5_verdict.py --combine W1.json W2.json [--json out.json]
    python3 scripts/kg50_q5_verdict.py --selftest
  리포 밖 (예: ibb 에서 이 파일 하나로) = --no-repo-verify (허용 목록 다시 대조를 건너뛴 사실을 결과에 적는다 ·
  리포에서 `python3 scripts/kg50_q5_branches.py --verify <폴더>` 로 따로).  판정 경로는 표준 라이브러리만 쓴다.
웹앱 화면 없음 (일회성 등록 판정 · 결과는 docs/data/ 기록으로 남긴다).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import struct
import sys
from array import array

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SCHEMA = 'kg50_q5_verdict/v1'
BRANCH_SCHEMA = 'kg50_q5_branch/v1'
REGISTRATION = 'docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md'
#: Q4 — 허용 오차 (상대) · O3 창 마지막 0.05 s · R3 = 보고
TAU = {'O1': 0.005, 'O2': 0.05, 'O3': 0.05}
O3_LAST_S = 0.05
#: §7 (a) — 결정 관측량
DECISION = {'W1': ('O1', 'O2'), 'W2': ('O2', 'O3')}
#: Q3 (나) — 창 길이 (덱 시간)
WINDOW_S = {'W1': 0.200001, 'W2': 0.3}
#: §3 — 침대마다 역할 (기준 · 바닥 · (a) X · (b) X)
BEDS = {'D0.7-50': dict(case='kg50_d07_b50', base='A', floor='F', a='B', b='C'),
        'D3-50 s1': dict(case='kg50_d3_b50_s1', base='A3', floor='F3', a=None, b='C3')}
ROLE_BED = {r: bed for bed, d in BEDS.items() for r in (d['base'], d['floor'], d['a'], d['b']) if r}
ROLE_KIND = {'A': 'base', 'B': 'dt_half', 'C': 'damp', 'F': 'floor', 'A3': 'base', 'C3': 'damp', 'F3': 'floor'}
ITEMS = {'O1': ('O1.z_SE', 'O1.z_AM'), 'O2': ('O2.cn_AM_AM', 'O2.cn_AM_SE', 'O2.cn_SE_SE', 'O2.cn_all'), 'O3': ('O3.P',)}
ATOM_COLS = ['id', 'type', 'x', 'y', 'z', 'radius', 'vx', 'vy', 'vz']
CONTACT_COLS = ['c_cpl[%d]' % i for i in range(1, 27)]
PASS, FAIL, UNDECIDED, UNDECIDED_TECH = '합격', '불합격', '판정 불가', '판정 불가 (기술)'
QUALIFIER_W1_B = ('"안정화 창에서 감쇠 민감도 τ 안" 까지만 — 압축 구간 감쇠 교란이 없다는 뜻이 아니다 '
                  '(§1-2 · W2 나 감시가 닫는다)')
#: §7 ① ② ③ 순서 (selftest ⓪ 가 등록 문장 · 행동을 대조한다)
ORDER = ('tech', 'floor', 'fail')

#: 거부 관문 — selftest 변이 (하나를 끄면 그것을 겨눈 시험이 실패해야 한다).  생산에서는 늘 True.
GUARDS = {k: True for k in (
    'manifest', 'role', 'deck_sha', 'repo_verify', 'ckpt', 'log_missing', 'np_procs', 'dt_echo', 'echo', 'start_step',
    't0_loop', 't0_error', 't0_finite', 't0_end', 'dump_set', 'dump_timestep', 'dump_frames', 'dump_rows', 'dump_format',
    'dump_finite', 'dump_dup_id', 'dump_cols', 'type_known', 'contact_dup', 'contact_self', 'contact_ids', 'contact_finite',
    'bed', 't0_identity', 'end_identity', 'floor_np', 'same_folder', 'window', 'thermo_times', 'bind_atoms', 'bind_zmax')}


class Refused(Exception):
    """입력이 판정을 낼 자격이 없다 (rc 2)."""


def _on(name):
    return GUARDS.get(name, True)


def _refuse(guard, msg):
    if _on(guard):
        raise Refused(msg)


def _sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _tok_finite(t):
    """덤프 · thermo 글자 하나 — ASCII 숫자 글자 (float() 은 유니코드 숫자도 받는다) 이고 유한."""
    if not t.isascii():
        return False
    try:
        return math.isfinite(float(t))
    except ValueError:
        return False


# ───────────────────────── LIGGGHTS 줄 규칙 (생성기 commands() 와 같음 · selftest ⓪e 가 대조) ─────────────────────────
def _uncomment(s):
    out, q = [], None
    for ch in s:
        if q:
            out.append(ch)
            if ch == q:
                q = None
        elif ch in '"\'':
            q = ch
            out.append(ch)
        elif ch == '#':
            break
        else:
            out.append(ch)
    return ''.join(out)


def norm(s):
    return ' '.join(_uncomment(s).split())


def commands(text):
    res, buf, b0 = [], '', None
    raw = text.split('\n')
    for i, line in enumerate(raw, 1):
        r = line.rstrip()
        if b0 is None:
            b0 = i
        if r.endswith('&'):
            buf += r[:-1] + ' '
            continue
        s = norm(buf + r)
        buf = ''
        if s:
            res.append((s, b0, i))
        b0 = None
    if buf.strip():
        s = norm(buf)
        if s:
            res.append((s, b0, len(raw)))
    return res


# ───────────────────────── manifest · 폴더 ─────────────────────────
def expected_steps(s0, end, every):
    return [s for s in range(((s0 + every - 1) // every) * every, end + 1, every)]


def load_manifest(folder):
    try:
        with open(os.path.join(folder, 'q5_manifest.json'), encoding='utf-8') as f:
            man = json.load(f)
    except (OSError, ValueError) as e:
        raise Refused(f'{folder}: q5_manifest.json 못 읽음 ({e})')
    if not _on('manifest'):
        return man
    try:
        W = man['window']
        tm = man['type_map']
        ok = (man['schema'] == BRANCH_SCHEMA and W in WINDOW_S and _is_int(man['np']) and man['np'] >= 1
              and _finite(man['dt']) and man['dt'] > 0 and isinstance(man['dt_echo'], str) and _is_int(man['s0'])
              and isinstance(man['runs'], list) and man['runs'] and all(_is_int(x) and x >= 1 for x in man['runs'])
              and _is_int(man['end_step']) and man['end_step'] == man['s0'] + sum(man['runs']) and man['compare_step'] == man['end_step']
              and man['checkpoint']['step'] == man['s0'] and isinstance(man['folder'], str)
              and abs(man['dt'] * sum(man['runs']) - WINDOW_S[W]) <= 1e-9 * WINDOW_S[W]
              and isinstance(tm, dict) and tm and all(isinstance(k, str) and re.fullmatch(r'[0-9]+', k) for k in tm)
              and set(tm.values()) <= {'AM', 'SE'} and set(man['density']) == set(tm)
              and all(_finite(man['density'][k]) and man['density'][k] > 0 for k in tm)
              and _finite(man['area_sim']) and man['area_sim'] > 0)
        for k in ('atom_dump', 'contact_dump'):
            d = man[k]
            ok = (ok and _is_int(d['every']) and d['every'] >= 1 and isinstance(d['dir'], str)
                  and d['steps'] == expected_steps(man['s0'], man['end_step'], d['every'])
                  and man['s0'] in d['steps'] and man['end_step'] in d['steps'])
        ok = (ok and man['atom_dump']['columns'] == ATOM_COLS and man['contact_dump']['columns'] == CONTACT_COLS
              and isinstance(man['deck']['file'], str) and isinstance(man['main_deck']['copy'], str)
              and bool(re.fullmatch(r'[0-9a-f]{64}', man['deck']['sha256']))
              and bool(re.fullmatch(r'[0-9a-f]{64}', man['main_deck']['sha256'])))
    except (KeyError, TypeError, AttributeError):
        ok = False
    if not ok:
        raise Refused(f'{folder}: q5_manifest.json 꼴 · 내부 일관성 (끝 step = s0 + run 합 · 덤프 step · 창 길이 Q3) 이 아니다')
    return man


def _read_bytes(path, what):
    try:
        with open(path, 'rb') as f:
            return f.read()
    except OSError as e:
        raise Refused(f'{what} 못 읽음 ({e})')


def check_ckpt(folder, man):
    """운영자 ckpt_sha256.txt — 두 줄 · 같은 sha256 · 둘째 = 이 가지 폴더의 사본 · 첫째 = 원본 (가지 폴더 밖)."""
    rel = man['checkpoint']['rel_path']
    try:
        with open(os.path.join(folder, 'ckpt_sha256.txt'), encoding='utf-8') as f:
            lines = [x for x in f.read().split('\n') if x.strip()]
    except OSError:
        _refuse('ckpt', f'{folder}: ckpt_sha256.txt 없음 (운영자 cp · sha256sum 줄 — 원본 · 사본 sha256 기록)')
        return None
    m = [re.fullmatch(r'([0-9a-f]{64})  (\S.*)', x) for x in lines]
    if len(lines) != 2 or not all(m):
        _refuse('ckpt', f'{folder}: ckpt_sha256.txt 가 sha256sum 두 줄이 아니다')
        return None
    (h1, p1), (h2, p2) = m[0].groups(), m[1].groups()
    if h1 != h2:
        _refuse('ckpt', f'{folder}: 체크포인트 원본 ↔ 사본 sha256 다름 ({h1[:12]}… ↔ {h2[:12]}…)')
    if not (p2.endswith('/' + man['folder'] + '/' + rel) and p1.endswith('/' + rel) and ('/' + man['folder'] + '/') not in p1):
        _refuse('ckpt', f'{folder}: ckpt_sha256.txt 경로가 원본 → 이 가지 폴더 사본 ({man["folder"]}/{rel}) 이 아니다')
    return h2


# ───────────────────────── 로그 ─────────────────────────
RE_LOOP = re.compile(r'^Loop time of (\S+) on ([0-9]+) procs.*? for ([0-9]+) steps with ([0-9]+) atoms')
RE_PLATE = re.compile(r'^====== PLATE HEIGHT: (\S+) ======\s*$')
RE_ERROR = re.compile(r'^\s*ERROR\b')
RE_HEADER = re.compile(r'^\s*Step\s+Atoms\b')


def parse_log(path):
    try:
        with open(path, encoding='utf-8', errors='replace') as f:
            lines = f.read().split('\n')
    except OSError:
        return None
    blocks, cur, errors, plate, loops = [], None, [], [], []
    for ln in lines:
        if RE_ERROR.match(ln):
            errors.append(ln)
        m = RE_PLATE.match(ln)
        if m:
            plate.append(m.group(1))
        m = RE_LOOP.match(ln)
        if m:
            loops.append(dict(procs=int(m.group(2)), steps=int(m.group(3)), atoms=int(m.group(4))))
            if cur is not None:
                cur['loop'] = loops[-1]
            cur = None
            continue
        if RE_HEADER.match(ln):
            cur = dict(header=ln.split(), rows=[], bad=[], loop=None)
            blocks.append(cur)
            continue
        if cur is not None:
            t = ln.split()
            if t and re.fullmatch(r'[0-9]+', t[0]):
                (cur['rows'] if len(t) == len(cur['header']) else cur['bad']).append(t)
    return dict(lines=lines, blocks=blocks, errors=errors, plate=plate, loops=loops)


def t0_eval(log, man):
    """T0 (§6) — 반환 (ok, 이유 목록, 원자 수 처음 · 끝)."""
    why, runs = [], man['runs']
    blocks = log['blocks']
    if _on('t0_loop'):
        done = [b['loop']['steps'] for b in blocks if b['loop'] is not None]
        if len(blocks) != len(runs) or done != runs or len(log['loops']) != len(runs):
            why.append(f'끝까지 안 돎 — thermo 묶음 {len(blocks)} · Loop time {len(log["loops"])} (step {done}) ≠ 덱 run {runs}')
    if _on('t0_error') and log['errors']:
        why.append(f'ERROR 줄 {len(log["errors"])} ({log["errors"][0][:80]})')
    if _on('t0_finite'):
        nf = sum(1 for b in blocks for r in b['rows'] for t in r[1:] if not _tok_finite(t))
        bad = sum(len(b['bad']) for b in blocks)
        if nf or bad:
            why.append(f'thermo 비유한 {nf} · 열 수 다른 줄 {bad}')
    last = blocks[-1]['rows'][-1][0] if blocks and blocks[-1]['rows'] else None
    if _on('t0_end') and (last is None or int(last) != man['end_step']):
        why.append(f'마지막 thermo step {last} ≠ 창 끝 {man["end_step"]}')
    atoms = []
    for b in blocks:
        if 'Atoms' in b['header']:
            k = b['header'].index('Atoms')
            atoms += [r[k] for r in b['rows']]
    return (not why), why, (atoms[0] if atoms else None), (atoms[-1] if atoms else None)


def check_log_provenance(log, man, deck_text, t0_ok):
    """이 로그가 이 가지 덱 · 이 NP · 이 체크포인트의 실행인가 — 거부 사유 (문자열) 또는 None."""
    if _on('np_procs') and any(x['procs'] != man['np'] for x in log['loops']):
        return f'Loop time procs {sorted({x["procs"] for x in log["loops"]})} ≠ manifest NP {man["np"]}'
    nl = [norm(x) for x in log['lines']]
    if _on('dt_echo'):
        # 덱 45 행 `timestep ${dt}` 의 치환 줄 (LIGGGHTS echo · %.15g) — 있으면 이 가지 dt 여야 (다른 dt = 다른 덱 · 늘 거부) ·
        # 없으면 T0 통과일 때만 거부 (빈 · 시작 전 잘린 로그 = T0 실패 = 판정 불가 (기술) 로 둔다)
        k = next((i for i, x in enumerate(nl) if x == 'timestep ${dt}'), None)
        if k is None:
            if t0_ok:
                return '로그에 dt 치환 줄 (timestep ${dt} → timestep …) 이 없다 (덱 dt 가 실제로 쓰였는지 · §4-2)'
        elif k + 1 >= len(nl) or nl[k + 1] != 'timestep ' + man['dt_echo']:
            return f'로그의 dt 치환 줄 [{nl[k + 1] if k + 1 < len(nl) else ""}] ≠ timestep {man["dt_echo"]} (다른 dt · 다른 덱 · §4-2)'
    if not t0_ok:
        return None
    if _on('echo'):
        j = 0
        for c, _a, _b in commands(deck_text):
            while j < len(nl) and nl[j] != c:
                j += 1
            if j >= len(nl):
                return f'로그 echo 에 가지 덱 명령이 (그 순서로) 없다: [{c[:80]}] — 이 덱으로 돈 로그가 아니다'
            j += 1
    if _on('start_step'):
        first = log['blocks'][0]['rows'][0][0] if log['blocks'] and log['blocks'][0]['rows'] else None
        if first is None or int(first) != man['s0']:
            return f'첫 thermo step {first} ≠ 체크포인트 step {man["s0"]}'
    return None


def thermo_series(log, col_names):
    """마지막 묶음의 (step, 값) — col_names 중 처음 있는 열."""
    if not log['blocks']:
        return []
    b = log['blocks'][-1]
    k = next((b['header'].index(c) for c in col_names if c in b['header']), None)
    if k is None:
        return []
    return [(int(r[0]), float(r[k])) for r in b['rows']]


# ───────────────────────── 덤프 (줄 단위로 읽는다 · D0.7 contact ≈ 백만 줄) ─────────────────────────
def _dump_files(folder, d):
    path = os.path.join(folder, d['dir'])
    try:
        names = os.listdir(path)
    except OSError:
        names = []
    got = {}
    for n in names:
        m = re.fullmatch(re.escape(d['prefix']) + r'([0-9]+)\.liggghts', n)
        if m:
            got.setdefault(int(m.group(1)), []).append(n)
    return path, got


def check_dump_set(folder, man, key):
    path, got = _dump_files(folder, man[key])
    want = set(man[key]['steps'])
    dup = sorted(s for s, v in got.items() if len(v) > 1)
    missing, extra = sorted(want - set(got)), sorted(set(got) - want)
    if dup or missing or extra:
        _refuse('dump_set', f'{folder}: {key} 덤프 — 빠짐 {missing[:5]} · 남음 {extra[:5]} · 같은 step 여러 파일 {dup[:5]}')
    return {s: os.path.join(path, got[s][0]) for s in want if s in got}


def _rows(path, kind, step, cols):
    """덤프 머리 검사 뒤 줄을 하나씩 낸다 — (n, box, 줄 iterator).  끝에서 줄 수 대조."""
    try:
        f = open(path, encoding='utf-8')
    except OSError as e:
        raise Refused(f'{path}: 못 읽음 ({e})')
    try:
        head = [f.readline().rstrip('\n') for _ in range(9)]
    except UnicodeDecodeError as e:
        f.close()
        raise Refused(f'{path}: 못 읽음 ({e})')
    if (head[0].strip() != 'ITEM: TIMESTEP' or head[2].strip() != f'ITEM: NUMBER OF {kind}'
            or not head[4].startswith('ITEM: BOX BOUNDS') or not re.fullmatch(r'[0-9]+', head[1].strip())
            or not re.fullmatch(r'[0-9]+', head[3].strip())):
        f.close()
        raise Refused(f'{path}: LIGGGHTS 덤프 머리가 아니다 (잘림 · 다른 꼴)')
    if _on('dump_timestep') and int(head[1]) != step:
        f.close()
        raise Refused(f'{path}: ITEM: TIMESTEP {head[1].strip()} ≠ 파일 이름 · 기대 step {step}')
    word = 'ATOMS' if kind == 'ATOMS' else 'ENTRIES'
    if _on('dump_cols') and (head[8].split()[:2] != ['ITEM:', word] or head[8].split()[2:] != cols):
        f.close()
        raise Refused(f'{path}: 열 {head[8].split()[2:][:9]} ≠ manifest 열')
    try:
        box = [tuple(float(v) for v in head[5 + i].split()[:2]) for i in range(3)]
    except ValueError:
        f.close()
        raise Refused(f'{path}: BOX BOUNDS 숫자가 아니다')
    n = int(head[3])

    def it():
        k = 0
        try:
            for raw in f:
                r = raw.rstrip('\n')
                if r.startswith('ITEM:'):
                    if _on('dump_frames'):
                        raise Refused(f'{path}: 프레임이 하나가 아니다 (ITEM: 줄이 본문에)')
                k += 1
                yield r
        finally:
            f.close()
        if _on('dump_rows') and k != n:
            raise Refused(f'{path}: 줄 {k} ≠ NUMBER OF {kind} {n} (잘림 · 남음)')
    return n, box, it()


def _bad_row(path, r):
    if _on('dump_format'):
        raise Refused(f'{path}: 덤프 줄 꼴이 아니다 [{r[:80]}]')


def read_atom_dump(path, step, man):
    n, box, rows = _rows(path, 'ATOMS', step, man['atom_dump']['columns'])
    tm = man['type_map']
    ids, typ = array('q'), array('q')
    val = [array('d') for _ in range(7)]
    for r in rows:
        t = r.split()
        if not r.isascii() or len(t) != 9 or not re.fullmatch(r'[0-9]+', t[0]) or not re.fullmatch(r'[0-9]+', t[1]):
            _bad_row(path, r)
            continue                   # (관문을 끈 변이에서만 닿는다 — 깨진 줄이 조용히 빠지는 꼴)
        if _on('type_known') and t[1] not in tm:
            raise Refused(f'{path}: 모르는 type {t[1]} (type_map {sorted(tm)})')
        ids.append(int(t[0]))
        typ.append(int(t[1]))
        for k in range(7):
            try:
                v = float(t[2 + k])
            except ValueError:
                v = float('nan')
            if _on('dump_finite') and not math.isfinite(v):
                raise Refused(f'{path}: 비유한 값 [{r[:80]}]')
            val[k].append(v)
    if _on('dump_dup_id') and len(set(ids)) != len(ids):
        raise Refused(f'{path}: 중복 atom id')
    h = hashlib.sha256()
    for i in sorted(range(len(ids)), key=ids.__getitem__):
        h.update(struct.pack('<qq7d', ids[i], typ[i], *(val[k][i] for k in range(7))))
    return dict(step=step, n=len(ids), box=box, id=ids, type=typ, x=val[0], y=val[1], z=val[2], r=val[3], vx=val[4], vy=val[5],
                vz=val[6], digest=h.hexdigest())


def read_contact_dump(path, step, man, atoms):
    _n, _box, rows = _rows(path, 'ENTRIES', step, man['contact_dump']['columns'])
    known = set(atoms['id'])
    seen = set()
    i1, i2, dl = array('q'), array('q'), array('d')
    for r in rows:
        t = r.split()
        if not r.isascii() or len(t) != 26 or not re.fullmatch(r'[0-9]+', t[6]) or not re.fullmatch(r'[0-9]+', t[7]):
            _bad_row(path, r)      # id = 정수 글자만 (지수 표기 = %g 6 자리에서 잘린 id 일 수 있다)
            continue
        if _on('contact_finite') and not all(_tok_finite(x) for x in t):
            raise Refused(f'{path}: 비유한 값 [{r[:80]}]')
        a, b = int(t[6]), int(t[7])
        if _on('contact_self') and a == b:
            raise Refused(f'{path}: 자기 쌍 {a}')
        key = (a, b) if a < b else (b, a)
        if _on('contact_dup') and key in seen:
            raise Refused(f'{path}: 중복 접촉 쌍 {key}')
        seen.add(key)
        if _on('contact_ids') and (a not in known or b not in known):
            raise Refused(f'{path}: 같은 step atom 덤프에 없는 id ({a}, {b})')
        i1.append(a)
        i2.append(b)
        dl.append(float(t[22]))
    return dict(step=step, n=len(i1), id1=i1, id2=i2, delta=dl)


def light_check(path, step, kind, man):
    """판정에 안 쓰는 덤프 — 머리 · 줄 수 · 프레임 (빠짐 · 잘림 · step)."""
    cols = man['atom_dump']['columns'] if kind == 'ATOMS' else man['contact_dump']['columns']
    _n, _box, rows = _rows(path, kind, step, cols)
    for _r in rows:
        pass


# ───────────────────────── 관측량 ─────────────────────────
def _pct(v, p):
    v = sorted(v)
    if not v:
        return None
    h = (len(v) - 1) * p / 100.0
    lo = int(math.floor(h))
    hi = min(lo + 1, len(v) - 1)
    return v[lo] + (h - lo) * (v[hi] - v[lo])


def observables(at, ct, man):
    tm, rho = man['type_map'], man['density']
    ph = [tm[str(t)] for t in at['type']]
    out = {}
    for P in ('SE', 'AM'):
        sel = [i for i in range(at['n']) if ph[i] == P]
        w = math.fsum(rho[str(at['type'][i])] * at['r'][i] ** 3 for i in sel)
        wz = math.fsum(rho[str(at['type'][i])] * at['r'][i] ** 3 * at['z'][i] for i in sel)
        out[f'O1.z_{P}'] = wz / w if sel and w > 0 else None
    pid = dict(zip(at['id'], ph))
    rad = dict(zip(at['id'], at['r']))
    nA, nS = ph.count('AM'), ph.count('SE')
    cnt = {'AM_AM': 0, 'AM_SE': 0, 'SE_SE': 0}
    ov = {'AM_AM': [], 'AM_SE': [], 'SE_SE': []}
    for a, b, d in zip(ct['id1'], ct['id2'], ct['delta']):
        k = '_'.join(sorted((pid[a], pid[b])))
        cnt[k] += 1
        ra, rb = rad[a], rad[b]
        ov[k].append(d / (ra * rb / (ra + rb)))
    out['O2.cn_AM_AM'] = 2.0 * cnt['AM_AM'] / nA if nA else None
    out['O2.cn_AM_SE'] = 1.0 * cnt['AM_SE'] / nA if nA else None
    out['O2.cn_SE_SE'] = 2.0 * cnt['SE_SE'] / nS if nS else None
    out['O2.cn_all'] = 2.0 * sum(cnt.values()) / at['n'] if at['n'] else None
    top = [at['z'][i] + at['r'][i] for i in range(at['n'])]
    rep = dict(counts=dict(n_AM=nA, n_SE=nS, **{'N_' + k: v for k, v in cnt.items()}),
               R2_top_max=max(top) if top else None, R2_top_p99=_pct(top, 99),
               R3={k: dict(p50=_pct(v, 50), p99=_pct(v, 99), n=len(v)) for k, v in ov.items()})
    return out, rep


def o3_mean(log, man):
    """O3 — 마지막 묶음 thermo pressMPa 의 창 마지막 0.05 s (끝 step − 0.05/dt … 끝 step · 양 끝 포함) 평균 · 표본 시각."""
    n50 = round(O3_LAST_S / man['dt'])
    lo = man['end_step'] - n50
    ser = [(s, v) for s, v in thermo_series(log, ('pressMPa', 'v_pressMPa')) if lo <= s <= man['end_step']]
    if not ser:
        return None, []
    times = [round((s - man['s0']) * man['dt'], 9) for s, _v in ser]
    return math.fsum(v for _s, v in ser) / len(ser), times


def r4_ratio(a_end, a_start, x_end):
    """R4 = RMS(x_X − x_A) / RMS(x_A(끝) − x_A(시작)) · 공통 id · x · y 주기 최소상 (A 끝 상자)."""
    (xl, xh), (yl, yh), _z = a_end['box']
    Lx, Ly = xh - xl, yh - yl

    def mi(d, L):
        return d - L * round(d / L) if L > 0 else d

    def pos(at):
        return {at['id'][i]: (at['x'][i], at['y'][i], at['z'][i]) for i in range(at['n'])}
    pe, ps, px = pos(a_end), pos(a_start), pos(x_end)
    com = sorted(set(pe) & set(ps) & set(px))
    if not com:
        return None
    num = math.fsum(mi(px[i][0] - pe[i][0], Lx) ** 2 + mi(px[i][1] - pe[i][1], Ly) ** 2 + (px[i][2] - pe[i][2]) ** 2 for i in com)
    den = math.fsum(mi(pe[i][0] - ps[i][0], Lx) ** 2 + mi(pe[i][1] - ps[i][1], Ly) ** 2 + (pe[i][2] - ps[i][2]) ** 2 for i in com)
    return math.sqrt(num / den) if den > 0 else None


def r5_share(at, log, man):
    """R5 (W2 · 보고) — Σ γ_type |v_z| / (P × 면적 × 10⁶) · 같은 step thermo P."""
    damp = man.get('damp') or {}
    g = {int(k): damp.get('gamma', 0.5) for k in man['type_map']}
    if damp.get('scale'):
        g[int(damp['scale']['type'])] = damp.get('gamma', 0.5) * float(damp['scale']['s'])
    P = dict(thermo_series(log, ('pressMPa', 'v_pressMPa'))).get(at['step'])
    if not P:
        return None
    return math.fsum(g[at['type'][i]] * abs(at['vz'][i]) for i in range(at['n'])) / (P * man['area_sim'] * 1e6)


# ───────────────────────── 덤프 ↔ 로그 결합 ─────────────────────────
def bind_dumps_to_log(folder, log, man, at0, atE, a0, a1):
    """덤프가 이 로그의 실행인가 — 원자 수 (첫 · 마지막 thermo Atoms = 시작 · 창 끝 덤프 줄 수) · W1 시작 zmax (첫 thermo
    c_zmax = 시작 덤프 z 최대 · 상대 1e-4 = 덤프 %g 6 자리 · thermo 글자 반올림 몫)."""
    def as_int(x):
        return int(x) if isinstance(x, str) and re.fullmatch(r'[0-9]+', x) else None
    if _on('bind_atoms') and (as_int(a0) != at0['n'] or as_int(a1) != atE['n']):
        raise Refused(f'{folder}: 로그 Atoms (처음 {a0} · 끝 {a1}) ≠ 덤프 원자 수 (시작 {at0["n"]} · 창 끝 {atE["n"]}) — 다른 실행의 덤프')
    if not _on('bind_zmax'):
        return
    b = log['blocks'][0] if log['blocks'] else None
    k = next((b['header'].index(c) for c in ('zmax', 'c_zmax') if b and c in b['header']), None)
    if k is None:
        if man['window'] == 'W1':
            raise Refused(f'{folder}: W1 첫 thermo (판 높이 run) 에 zmax 열이 없다')
        return
    zl, zd = float(b['rows'][0][k]), max(at0['z'])
    if abs(zl - zd) > 1e-4 * max(abs(zd), 1e-300):
        raise Refused(f'{folder}: 첫 thermo zmax {zl:.8g} ≠ 시작 덤프 z 최대 {zd:.8g} — 시작 덤프가 이 로그의 실행이 아니다')


# ───────────────────────── 가지 하나 ─────────────────────────
def read_branch(folder, role, repo_verify=True):
    man = load_manifest(folder)
    if _on('role') and (man.get('branch') != role or ROLE_BED.get(role) != man.get('bed')
                        or BEDS[ROLE_BED[role]]['case'] != man.get('case') or ROLE_KIND.get(role) != man.get('kind')):
        raise Refused(f'{folder}: manifest 가지 {man.get("branch")} ({man.get("case")}) ≠ 역할 {role}')
    db = _read_bytes(os.path.join(folder, man['deck']['file']), '가지 덱')
    mb = _read_bytes(os.path.join(folder, man['main_deck']['copy']), '본 덱 사본')
    if _on('deck_sha') and (_sha256_bytes(db) != man['deck']['sha256'] or _sha256_bytes(mb) != man['main_deck']['sha256']):
        raise Refused(f'{folder}: 가지 덱 · 본 덱 사본 sha256 ≠ manifest')
    rv = 'skipped (--no-repo-verify)'
    if repo_verify and _on('repo_verify'):
        try:
            sys.path.insert(0, HERE)
            import kg50_q5_branches as G      # 리포 생성기의 허용 목록 대조 (리포 안에서만)
        except ImportError as e:
            raise Refused(f'리포 생성기 (kg50_q5_branches) 를 못 불러옴 ({e}) — 리포 밖이면 --no-repo-verify')
        p = G.verify_folder(folder)
        if p:
            raise Refused(f'{folder}: 허용 목록 다시 대조 실패 — ' + ' | '.join(p[:3]))
        rv = 'ok'
    ck = check_ckpt(folder, man)
    log = parse_log(os.path.join(folder, 'log.liggghts'))
    if log is None:
        _refuse('log_missing', f'{folder}: log.liggghts 없음 (T0 를 볼 수 없다)')
        log = dict(lines=[], blocks=[], errors=[], plate=[], loops=[])
    ok, why, a0, a1 = t0_eval(log, man)
    bad = check_log_provenance(log, man, db.decode('utf-8'), ok)
    if bad:
        raise Refused(f'{folder}: {bad}')
    br = dict(role=role, folder=os.path.realpath(folder), man=man, repo_verify=rv, ckpt=ck,
              t0=dict(ok=ok, why=why, atoms_first=a0, atoms_last=a1), log=log, plate=log['plate'][:1], atoms={})
    s0, cs = man['s0'], man['compare_step']
    if not ok:
        _p, got = _dump_files(folder, man['atom_dump'])      # T0 실패 — 덤프 요구 없음 · 시작 상태 대조만 (있으면)
        if s0 in got and len(got[s0]) == 1:
            try:
                br['atoms'][s0] = read_atom_dump(os.path.join(_p, got[s0][0]), s0, man)
            except Refused:
                pass
        return br
    afiles = check_dump_set(folder, man, 'atom_dump')
    cfiles = check_dump_set(folder, man, 'contact_dump')
    for s, p in sorted(afiles.items()):
        if s in (s0, cs):
            br['atoms'][s] = read_atom_dump(p, s, man)
        else:
            light_check(p, s, 'ATOMS', man)
    if cs not in cfiles or cs not in br['atoms'] or s0 not in br['atoms']:
        raise Refused(f'{folder}: 시작 · 창 끝 덤프 없음')
    bind_dumps_to_log(folder, log, man, br['atoms'][s0], br['atoms'][cs], a0, a1)
    for s, p in sorted(cfiles.items()):
        if s != cs:
            light_check(p, s, 'ENTRIES', man)
    br['contact'] = read_contact_dump(cfiles[cs], cs, man, br['atoms'][cs])
    br['obs'], br['rep'] = observables(br['atoms'][cs], br['contact'], man)
    if man['window'] == 'W2':
        br['obs']['O3.P'], br['o3_times'] = o3_mean(log, man)
        br['rep']['R5_damp_share'] = r5_share(br['atoms'][cs], log, man)
    ke = thermo_series(log, ('KinEng',))
    br['rep']['R1_ke_end'] = ke[-1][1] if ke else None
    return br


# ───────────────────────── 판정 ─────────────────────────
def _rel(x, a):
    if x is None or a is None or not (_finite(x) and _finite(a)) or a == 0:
        return None
    return abs(x - a) / abs(a)


def judge_item(tech_ok, a, f, x, tau, order=None):
    """결정 관측량 하나 — (결과, 이유, |F−A|/|A|, |X−A|/|A|).  순서 = §7 ① ② ③ ④ (order = selftest 변이용)."""
    rf, rx = _rel(f, a), _rel(x, a)
    for step in (order or ORDER):
        if step == 'tech' and not tech_ok:
            return UNDECIDED_TECH, '① X · A · F 중 T0 실패', rf, rx
        if step in ('floor', 'fail') and (rf is None or rx is None):
            return UNDECIDED, ('상대 차를 정할 수 없다 (값 없음 · 비유한 · |A| = 0 — §7 에 없는 자리 · 합격으로 두지 않는다)'), rf, rx
        if step == 'floor' and rf > tau:
            return UNDECIDED, f'② |F − A|/|A| {rf:.4g} > τ {tau:g} (이 창이 τ 를 가를 해상도가 없다)', rf, rx
        if step == 'fail' and rx > tau:
            return FAIL, f'③ |X − A|/|A| {rx:.4g} > τ {tau:g}', rf, rx
    return PASS, f'④ |X − A|/|A| {rx:.4g} ≤ τ {tau:g} · 바닥 {rf:.4g} ≤ τ', rf, rx


def worst(results):
    rs = list(results)
    if FAIL in rs:
        return FAIL
    if UNDECIDED_TECH in rs:
        return UNDECIDED_TECH
    if UNDECIDED in rs or not rs:
        return UNDECIDED
    return PASS


def compare(here, bed, xrole, window):
    d = BEDS[bed]
    A, F, X = here.get(d['base']), here.get(d['floor']), here.get(xrole)
    tech = all(b is not None and b['t0']['ok'] for b in (A, F, X))
    tw = [f'{b["role"]}: ' + '; '.join(b['t0']['why']) for b in (A, F, X) if b is not None and not b['t0']['ok']]
    items = {}
    for o in DECISION[window]:
        for it in ITEMS[o]:
            vals = [b['obs'].get(it) if (b is not None and 'obs' in b) else None for b in (A, F, X)]
            res, why, rf, rx = judge_item(tech, vals[0], vals[1], vals[2], TAU[o])
            if res == UNDECIDED_TECH and tw:
                why += ' — ' + ' | '.join(tw)
            items[it] = dict(a=vals[0], f=vals[1], x=vals[2], rel_floor=rf, rel_x=rx, tau=TAU[o], result=res, why=why)
    return dict(x=xrole, base=d['base'], floor=d['floor'], tech_ok=tech, items=items,
                result=worst(v['result'] for v in items.values()))


def _bed_checks(bed, here, window):
    d = BEDS[bed]
    if d['base'] not in here or d['floor'] not in here:
        raise Refused(f'{bed}: 기준 {d["base"]} · 바닥 {d["floor"]} 둘 다 있어야 비교한다')
    ms = {(b['man']['case'], b['man']['main_deck']['sha256'], b['man']['s0'], b['man']['window']) for b in here.values()}
    if _on('bed') and len(ms) != 1:
        raise Refused(f'{bed}: 가지들의 케이스 · 본 덱 · 체크포인트 step · 창이 같지 않다')
    if _on('ckpt') and len({b['ckpt'] for b in here.values()}) != 1:
        raise Refused(f'{bed}: 가지마다 체크포인트 sha256 이 다르다 (같은 체크포인트에서 시작이 아니다)')
    if _on('floor_np') and here[d['floor']]['man']['np'] == here[d['base']]['man']['np']:
        raise Refused(f'{bed}: 바닥 {d["floor"]} NP = 기준 {d["base"]} NP — 합산 순서가 같아 바닥이 0 이 된다')
    s0 = here[d['base']]['man']['s0']
    t0d = {r: b['atoms'][s0]['digest'] for r, b in here.items() if s0 in b['atoms']}
    if _on('t0_identity') and len(set(t0d.values())) > 1:
        raise Refused(f'{bed}: 시작 상태 (step {s0} atom 덤프) 가 가지마다 다르다 — 같은 체크포인트가 아니다')
    ed = [(r, b['atoms'][b['man']['compare_step']]['digest']) for r, b in sorted(here.items())
          if b['t0']['ok'] and b['man']['compare_step'] in b['atoms']]
    dup = [(r1, r2) for i, (r1, h1) in enumerate(ed) for r2, h2 in ed[i + 1:] if h1 == h2]
    if _on('end_identity') and dup:
        raise Refused(f'{bed}: 끝 상태가 두 가지에서 바이트 같다 {dup} — 복사된 덤프 (다른 계산이 아니다)')
    if window == 'W2' and _on('thermo_times'):
        if len({tuple(b.get('o3_times') or ()) for b in here.values() if b['t0']['ok']}) > 1:
            raise Refused(f'{bed}: O3 표본 시각이 가지마다 다르다 — 같은 시각 비교가 아니다')


def _bed_report(bed, here):
    d = BEDS[bed]
    A = here[d['base']]
    s0 = A['man']['s0']
    rep = {}
    for r, b in sorted(here.items()):
        if not b['t0']['ok']:
            continue
        rr = dict(b['rep'])
        if A['t0']['ok'] and r != d['base']:
            rr['R4_rms_ratio'] = r4_ratio(A['atoms'][A['man']['compare_step']], A['atoms'][s0], b['atoms'][b['man']['compare_step']])
            rr['R1_rel_vs_base'] = _rel(rr.get('R1_ke_end'), A['rep'].get('R1_ke_end'))
        rr['R6_plate_height'] = b['plate'][0] if b['plate'] else None
        if A['plate'] and b['plate'] and _tok_finite(A['plate'][0]) and _tok_finite(b['plate'][0]):
            rr['R6_rel_vs_base'] = _rel(float(b['plate'][0]), float(A['plate'][0]))
        rep[r] = rr
    return rep


def run(roles, repo_verify=True, main_log=None):
    """roles = {역할: 폴더}.  반환 판정 dict.  거부 = Refused."""
    bad = sorted(set(roles) - set(ROLE_BED))
    if bad:
        raise Refused(f'모르는 역할 {bad} (등록 §3: A B C F · A3 C3 F3)')
    reals = [os.path.realpath(p) for p in roles.values()]
    if _on('same_folder') and len(set(reals)) != len(reals):
        raise Refused('같은 폴더가 두 역할에 쓰였다')
    brs = {r: read_branch(p, r, repo_verify) for r, p in sorted(roles.items())}
    wins = sorted({b['man']['window'] for b in brs.values()})
    if _on('window') and len(wins) != 1:
        raise Refused(f'창이 섞였다 ({wins})')
    window = brs[sorted(brs)[0]]['man']['window']
    beds = {}
    for bed, d in BEDS.items():
        here = {r: brs[r] for r in brs if ROLE_BED[r] == bed}
        if not here:
            continue
        _bed_checks(bed, here, window)
        cmp_ = {k: compare(here, bed, d[k], window) for k in ('a', 'b') if d[k] and d[k] in here}
        beds[bed] = dict(case=d['case'], comparisons=cmp_, report=_bed_report(bed, here))
    a = beds.get('D0.7-50', {}).get('comparisons', {}).get('a')
    bres = {bed: v['comparisons']['b'] for bed, v in beds.items() if 'b' in v['comparisons']}
    if len(bres) == 2:
        b_all, b_why = worst(v['result'] for v in bres.values()), '두 침대 중 나쁜 쪽 (불합격 > 판정 불가 > 합격)'
    else:
        b_all = UNDECIDED if bres else None
        b_why = ('침대 하나만 읽음 (Q2 (가) — D0.7 C · D3 C3 둘 다 있어야 전체 (b))' if bres else '(b) 가지 없음')
    out = dict(schema=SCHEMA, registration=REGISTRATION, registration_sha256=_reg_sha(), window=window,
               tau=TAU, decision=list(DECISION[window]),
               branches={r: dict(folder=b['folder'], case=b['man']['case'], kind=b['man']['kind'], np=b['man']['np'],
                                 deck_sha256=b['man']['deck']['sha256'], ckpt_sha256=b['ckpt'], repo_verify=b['repo_verify'],
                                 t0=b['t0'], obs=b.get('obs'), counts=(b.get('rep') or {}).get('counts'))
                         for r, b in brs.items()},
               beds=beds,
               a=(dict(result=a['result'], why='X = B · 결정 관측량 중 나쁜 쪽') if a else None),
               b=(dict(result=b_all, why=b_why, per_bed={k: v['result'] for k, v in bres.items()}) if b_all else None))
    if window == 'W1':
        for bed in bres:
            if bres[bed]['result'] == PASS:
                bres[bed]['qualifier'] = QUALIFIER_W1_B
        if out['b'] and out['b']['result'] == PASS:
            out['b']['qualifier'] = QUALIFIER_W1_B
    if main_log:
        out['R6_main_log'] = main_log_compare(main_log, brs.get('A'))
    return out


def main_log_compare(path, A):
    """§8-3 2 — 멈춘 본 런 로그의 체크포인트 뒤 첫 줄 (판 높이 run) · PLATE HEIGHT ↔ A (보고)."""
    m = parse_log(path)
    if m is None or A is None:
        return dict(status='없음')
    s0 = A['man']['s0']

    def first_rows(lg):
        for b in lg['blocks']:
            if b['rows'] and int(b['rows'][0][0]) == s0:
                return [' '.join(r) for r in b['rows'][:2]]
        return None
    a_rows, m_rows = first_rows(A['log']), first_rows(m)
    mp = m['plate'][-1] if m['plate'] else None
    return dict(status='읽음', thermo_same=(a_rows is not None and a_rows == m_rows), main_rows=m_rows, a_rows=a_rows,
                plate_main=mp, plate_a=(A['plate'][0] if A['plate'] else None),
                plate_same=bool(mp is not None and A['plate'] and mp == A['plate'][0]))


def _reg_sha():
    try:
        with open(os.path.join(ROOT, REGISTRATION), 'rb') as f:
            return _sha256_bytes(f.read())
    except OSError:
        return None


def combine(w1, w2):
    """W1 · W2 판정 둘 → 창마다 따로 · 전체 = 나쁜 쪽 (§7)."""
    if w1.get('schema') != SCHEMA or w2.get('schema') != SCHEMA or (w1.get('window'), w2.get('window')) != ('W1', 'W2'):
        raise Refused('combine = W1 판정 · W2 판정 (이 판독기 JSON) 순서로')
    out = dict(schema=SCHEMA + '+combine', registration=REGISTRATION, windows=['W1', 'W2'])
    for k in ('a', 'b'):
        rs = [x[k]['result'] for x in (w1, w2) if x.get(k)]
        out[k] = dict(result=(worst(rs) if len(rs) == 2 else UNDECIDED),
                      per_window={w: (x[k]['result'] if x.get(k) else None) for w, x in (('W1', w1), ('W2', w2))},
                      why=('창마다 따로 · 나쁜 쪽' if len(rs) == 2 else '한 창에 이 판정이 없다'))
    return out


# ───────────────────────── 보고 ─────────────────────────
def _f(x, nd=5):
    return '—' if x is None else (f'{x:.{nd}g}' if isinstance(x, float) else str(x))


def report(out):
    L = [f'# 50kg Q5 판정 — 창 {out["window"]} · 등록 {out["registration"]} §7 · τ = {out["tau"]}', '',
         '| 가지 | 케이스 | NP | T0 | 원자 수 (처음 → 끝) | 허용 목록 다시 대조 | 메모 |', '|---|---|---|---|---|---|---|']
    for r, b in out['branches'].items():
        L.append(f'| {r} | {b["case"]} | {b["np"]} | {"통과" if b["t0"]["ok"] else "실패"} | {b["t0"]["atoms_first"]} → '
                 f'{b["t0"]["atoms_last"]} | {b["repo_verify"]} | {"; ".join(b["t0"]["why"]) or "-"} |')
    for bed, v in out['beds'].items():
        for k, c in v['comparisons'].items():
            L += ['', f'## {bed} — ({k}) {c["x"]} ↔ {c["base"]} (바닥 {c["floor"]}) = **{c["result"]}**'
                  + (f' · 한정어: {c["qualifier"]}' if c.get('qualifier') else ''), '',
                  '| 관측량 | A | F | X | \\|F−A\\|/\\|A\\| | \\|X−A\\|/\\|A\\| | τ | 판정 | 근거 |', '|---|---|---|---|---|---|---|---|---|']
            for it, x in c['items'].items():
                L.append(f'| {it} | {_f(x["a"])} | {_f(x["f"])} | {_f(x["x"])} | {_f(x["rel_floor"], 3)} | {_f(x["rel_x"], 3)} | '
                         f'{x["tau"]:g} | {x["result"]} | {x["why"]} |')
        if v['report']:
            L += ['', f'보고 관측량 (판정 밖) — {bed}: ' + json.dumps({r: {k: x for k, x in rr.items() if k != 'counts'}
                                                                for r, rr in v['report'].items()}, ensure_ascii=False)]
    L.append('')
    if out.get('a'):
        L.append(f'**(a) dt: {out["a"]["result"]}** — {out["a"]["why"]}')
    if out.get('b'):
        L.append(f'**(b) 감쇠: {out["b"]["result"]}** — {out["b"]["why"]} · 침대별 {out["b"]["per_bed"]}'
                 + (f' · 한정어: {out["b"]["qualifier"]}' if out['b'].get('qualifier') else ''))
    return '\n'.join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description='50kg Q5 판독기 (읽기 전용 · 등록 §6 · §7)')
    ap.add_argument('--branch', action='append', default=[], help='역할=가지 폴더 (A B C F · A3 C3 F3)')
    ap.add_argument('--json', default='', help='판정 기록 JSON 을 쓸 곳')
    ap.add_argument('--main-log', default='', help='멈춘 본 런 log.liggghts (보고 R6 · 선택)')
    ap.add_argument('--no-repo-verify', action='store_true', help='리포 생성기 허용 목록 다시 대조를 건너뜀 (결과에 적힌다)')
    ap.add_argument('--combine', nargs=2, metavar=('W1_JSON', 'W2_JSON'), help='W1 · W2 판정 합치기 (나쁜 쪽)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.combine:
            with open(a.combine[0], encoding='utf-8') as f1, open(a.combine[1], encoding='utf-8') as f2:
                out = combine(json.load(f1), json.load(f2))
            print(json.dumps(out, ensure_ascii=False, indent=1))
        else:
            roles = {}
            for s in a.branch:
                r, sep, p = s.partition('=')
                if not sep or not p or r in roles:
                    print(f'⛔ --branch 형식 · 중복: {s!r}')
                    return 2
                roles[r] = p
            if not roles:
                print('⛔ --branch 가 없다')
                return 2
            out = run(roles, repo_verify=not a.no_repo_verify, main_log=a.main_log or None)
            print(report(out))
    except (Refused, OSError, ValueError) as e:
        print(f'⛔ 입력 거부 — 판정 없음: {e}')
        return 2
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(f'\n판정 기록: {a.json}')
    return 0


# ───────────────────────────── selftest ─────────────────────────────
def registration_check(path=None):
    """§7 판정 순서 · 묶는 규칙 · W1 한정어 · Q3 · Q4 · §6 관측량 줄이 이 파일과 같은가 — (ok, 문제)."""
    try:
        with open(path or os.path.join(ROOT, REGISTRATION), encoding='utf-8') as f:
            txt = f.read()
    except OSError as e:
        return False, [f'등록 문서 못 읽음 ({e})']
    need = (
        '1. ① **기술**: X · A · F 중 하나라도 T0 실패 → 그 비교 **판정 불가 (기술)** · 다시 돌릴지 = 1저자 (자동 재실행 없음).',
        '2. ② **바닥**: |F − A| / |A| > τ_o → o **판정 불가** (그 창이 τ 를 가를 해상도가 없다).',
        '3. ③ |X − A| / |A| > τ_o → o **불합격**.',
        '4. ④ 그 밖 → o **합격** (|X − A| = τ 는 합격).',
        '- **(a)** = X = B · 결정 관측량 (W1: O1 · O2 / W2: O2 · O3) 중 하나라도 불합격 → 불합격 · 아니고 하나라도 판정 불가 → 판정 불가 · '
        '다 합격 → 합격.',
        '- **(b)** = X = C (D0.7) · Q2 (가) 면 C3 (D3 · 바닥 F3) 도 — 침대마다 따로 판정하고 둘을 함께 적는다 · 전체 = 나쁜 쪽 '
        '(불합격 > 판정 불가 > 합격).',
        '- W1 · W2 를 둘 다 하면 창마다 따로 판정 · 전체 = 나쁜 쪽.',
        '- **W1 만으로 낸 (b) 합격 = "안정화 창에서 감쇠 민감도 τ 안" 까지만** — 압축 구간 감쇠 교란이 없다는 뜻이 아니다 '
        '(§1-2 · W2 나 감시가 닫는다).',
        '> | Q4 | O1 0.5 % · O2 5 % · O3 5 % (창 마지막 0.05 s 평균) · R3 겹침 = 보고 |',
        '> | Q3 | (나) W1 0.200001 s + W2 0.3 s |',
        '> | Q2 | (가) AM 기준 s (감쇠 가지 C · C3) |',
        '| T0 | 기술 — 끝까지 돎 (`Loop time of`) · ERROR 0 · thermo 비유한 없음 · 원자 수 | 로그 · thermo `atoms` | 둘 다 | 판정 ① |',
        '| O1 | SE · AM 질량 중심 높이 z̄_SE · z̄_AM | 창 끝 atom 덤프 (type · z) | W1 | (a) · (b) 판정 |',
        '| O2 | 평균 접촉 수 (AM–AM · AM–SE · SE–SE · 입자당) | 창 끝 contact 덤프 (id 두 열) + atom 덤프 (type) | 둘 다 | 판정 |',
        '| O3 | 판 압력 P — 창 마지막 0.05 s 의 thermo `v_pressMPa` 평균 | thermo | W2 | 판정 |',
        '| R3 | 겹침 δ/R* 50 · 99 % 분위 (쌍 종류별) | contact 덤프 (delta) | 둘 다 | 보고',
        '판정 순서를 selftest 첫 항목으로',
    )
    probs = [f'등록 줄 없음: {s[:80]}…' for s in need if s not in txt]
    m = re.search(r'\| Q4 \| O1 ([0-9.]+) % · O2 ([0-9.]+) % · O3 ([0-9.]+) % \(창 마지막 ([0-9.]+) s 평균\)', txt)
    if not m or tuple(float(x) / 100 for x in m.groups()[:3]) != (TAU['O1'], TAU['O2'], TAU['O3']) or float(m.group(4)) != O3_LAST_S:
        probs.append(f'Q4 문턱 ≠ 판독기 ({TAU} · 마지막 {O3_LAST_S} s)')
    m = re.search(r'\| Q3 \| \(나\) W1 ([0-9.]+) s \+ W2 ([0-9.]+) s \|', txt)
    if not m or (float(m.group(1)), float(m.group(2))) != (WINDOW_S['W1'], WINDOW_S['W2']):
        probs.append(f'Q3 창 길이 ≠ 판독기 {WINDOW_S}')
    if ORDER != ('tech', 'floor', 'fail'):
        probs.append(f'판정 순서 {ORDER} ≠ §7 ① ② ③')
    return (not probs), probs


def selftest():
    import io
    import shutil
    import tempfile
    from contextlib import redirect_stdout
    tally = [0, 0]

    def chk(label, cond, extra=''):
        tally[1] += 1
        tally[0] += bool(cond)
        print(f'  {"✓" if cond else "✗"} {label}{(" — " + str(extra)[:300]) if extra and not cond else ""}')

    def go(label, fn):
        try:
            fn()
        except Exception as e:          # noqa: BLE001 — 구현 전 · 예외 = 그 묶음 실패
            chk(f'{label} (예외)', False, f'{type(e).__name__}: {e}')

    print('kg50_q5_verdict selftest')
    # ⓪ 판정 순서 — 첫 항목 (등록 문장 + 행동)
    ok, why = registration_check()
    chk('⓪ 등록 §7 판정 순서 ① ② ③ ④ · (a) · (b) 묶기 · W1 한정어 · Q2 · Q3 · Q4 문턱 · §6 T0 · O1 · O2 · O3 · R3 줄 = 판독기', ok, why)

    def order_tests():
        t = TAU['O1']
        r = [judge_item(False, 200.0, 202.0, 202.0, t)[0], judge_item(True, 200.0, 202.0, 202.0, t)[0],
             judge_item(True, 200.0, 200.0, 202.0, t)[0], judge_item(True, 200.0, 200.0, 201.0, t)[0],
             judge_item(True, 200.0, 201.0, 200.0, t)[0], judge_item(True, 0.0, 0.0, 0.0, t)[0],
             judge_item(True, 200.0, None, 200.0, t)[0], judge_item(True, 200.0, 200.0, float('nan'), t)[0]]
        chk('⓪b 순서 — T0 실패 + 바닥 + X 다 넘음 → ① 판정 불가 (기술) · 바닥 + X 넘음 → ② 판정 불가 · X 만 → ③ 불합격 · '
            '|X−A| = τ (201/200) → ④ 합격 · 바닥 = τ → 합격 · 분모 0 · 값 없음 · nan → 판정 불가',
            r == [UNDECIDED_TECH, UNDECIDED, FAIL, PASS, PASS, UNDECIDED, UNDECIDED, UNDECIDED], r)
        chk('⓪c 묶기 — 불합격 > 판정 불가 (기술) > 판정 불가 > 합격 · 빈 목록 = 판정 불가',
            worst([PASS, UNDECIDED, FAIL]) == FAIL and worst([PASS, UNDECIDED]) == UNDECIDED and worst([PASS, PASS]) == PASS
            and worst([UNDECIDED, UNDECIDED_TECH]) == UNDECIDED_TECH and worst([]) == UNDECIDED)
        bad = [o for o in (('floor', 'tech', 'fail'), ('tech', 'fail', 'floor'), ('fail', 'floor', 'tech'))
               if [judge_item(False, 200.0, 202.0, 202.0, t, o)[0], judge_item(True, 200.0, 202.0, 202.0, t, o)[0]]
               == [UNDECIDED_TECH, UNDECIDED]]
        chk('⓪d 순서 변이 (① ② ③ 를 바꾼 세 꼴) → ⓪b 의 기대가 깨진다 (순서 시험이 순서를 본다)', bad == [], bad)
    go('⓪ 순서', order_tests)
    sys.path.insert(0, HERE)
    import kg50_q5_branches as G

    def parity():
        for case in G.CASES:
            with open(os.path.join(ROOT, G.CASES[case]['deck']), encoding='utf-8') as fh:
                t = fh.read()
            chk(f'⓪e LIGGGHTS 줄 규칙 사본 = 생성기 commands() ({case} 본 덱)', G.commands(t) == commands(t))
    go('⓪e 줄 규칙', parity)
    tmp = tempfile.mkdtemp(prefix='q5v_')
    try:
        base = os.path.join(tmp, 'gen')
        hold = {}

        def setup():
            mans = {}
            for case in G.CASES:
                for br in G.CASES[case]['branches']:
                    mans[br] = G.build_branch(case, br, G.NP[br], base)
            hold['S'] = Synth(base, mans)
        go('V0 합성 자료 (생성기 가지 일곱 + 작은 침대)', setup)

        class _Lazy:
            def __getattr__(self, k):
                return getattr(hold['S'], k)
        S = _Lazy()

        def v1():
            out = S.verdict('v1')
            chk('V1 거의 같은 일곱 → (a) 합격 · (b) 합격 (D0.7 · D3 둘 다) + W1 한정어 · 결정 관측량 6 (O1 둘 · O2 넷)',
                out['a']['result'] == PASS and out['b']['result'] == PASS and out['b'].get('qualifier') == QUALIFIER_W1_B
                and out['b']['per_bed'] == {'D0.7-50': PASS, 'D3-50 s1': PASS}
                and len(out['beds']['D0.7-50']['comparisons']['a']['items']) == 6, (out.get('a'), out.get('b')))
            it = out['beds']['D0.7-50']['comparisons']['a']['items']
            chk('V1b 값 — z̄ = Σρr³z/Σρr³ · cn_SE_SE = 2N/n_SE (40/8 = 5) · AM–SE = N/n_AM · AM–AM = 2N/n_AM (손 계산)',
                abs(it['O1.z_SE']['a'] - S.zbar('SE')) < 1e-15 and abs(it['O1.z_AM']['a'] - S.zbar('AM')) < 1e-15
                and it['O2.cn_SE_SE']['a'] == 5.0 and it['O2.cn_AM_SE']['a'] == 1.5 and it['O2.cn_AM_AM']['a'] == 1.0
                and it['O2.cn_all']['a'] == 2 * 28 / 12, it)
            rep = out['beds']['D0.7-50']['report']
            r4 = [rep[r].get('R4_rms_ratio') for r in ('B', 'C', 'F')]
            chk('V1c 보고 — R1 · R2 · R3 (쌍 종류별 n = 접촉 수) · R4 (x 이동 1 · 2 · 3 · 4 µm·10⁻³ → B · C · F = 1 · 2 · 3) · R6 판 높이',
                all(x is not None for x in r4) and max(abs(x - y) for x, y in zip(r4, (1.0, 2.0, 3.0))) < 1e-6
                and rep['A']['R3']['SE_SE']['n'] == 20 and rep['A']['R3']['AM_AM']['n'] == 2
                and rep['C'].get('R6_plate_height') == '0.0123' and rep['F'].get('R1_rel_vs_base') == 0.0
                and rep['A'].get('R2_top_max') is not None, rep.get('B'))
            txt = report(out)
            chk('V1d 보고 표 = 비교 셋 (D0.7 (a) · (b) · D3 (b)) · (a) · (b) 줄 · 한정어', '**(a) dt: 합격**' in txt
                and '**(b) 감쇠: 합격**' in txt and '한정어' in txt and txt.count('\n## ') == 3, txt[:300])
            chk('V1e 허용 목록 다시 대조 = 일곱 다 ok (리포 생성기 verify_folder)',
                all(b['repo_verify'] == 'ok' for b in out['branches'].values()))
        go('V1 기준', v1)

        def v2():
            out = S.verdict('v2', zse={'B': 1.006})
            it = out['beds']['D0.7-50']['comparisons']['a']['items']['O1.z_SE']
            chk('V2 B 의 z̄_SE +0.6 % → O1 불합격 (③) → (a) 불합격 · (b) 합격 그대로',
                out['a']['result'] == FAIL and it['result'] == FAIL and it['why'].startswith('③') and out['b']['result'] == PASS, it)
            out = S.verdict('v2b', zse={'F': 1.006, 'B': 1.007})
            it = out['beds']['D0.7-50']['comparisons']['a']['items']['O1.z_SE']
            chk('V2b 바닥 F +0.6 % · B +0.7 % → ② 판정 불가 (③ 보다 먼저) → (a) 판정 불가 · (b) D0.7 도 그 항목 판정 불가',
                it['result'] == UNDECIDED and it['why'].startswith('②') and out['a']['result'] == UNDECIDED
                and out['beds']['D0.7-50']['comparisons']['b']['result'] == UNDECIDED, it)
            out = S.verdict('v2c', drop_ss={'C': 1})
            c = out['beds']['D0.7-50']['comparisons']['b']['items']['O2.cn_SE_SE']
            chk('V2c C 의 SE–SE 접촉 하나 빠짐 (5 → 4.75 = −5 % = τ) → 합격 (경계 · |X − A| = τ 는 합격)',
                c['result'] == PASS and c['rel_x'] == 0.05 and out['b']['per_bed']['D0.7-50'] == PASS, c)
            out = S.verdict('v2d', drop_ss={'C': 2})
            chk('V2d C SE–SE −10 % → (b) D0.7 불합격 → 전체 (b) 불합격 (D3 합격이라도 · 나쁜 쪽) · 한정어 없음',
                out['b']['result'] == FAIL and out['b']['per_bed'] == {'D0.7-50': FAIL, 'D3-50 s1': PASS} and 'qualifier' not in out['b'],
                out['b'])
            out = S.verdict('v2e', zse={'C3': 1.006})
            chk('V2e D3 C3 z̄_SE +0.6 % → (b) D3 불합격 · 전체 (b) 불합격 · (a) 합격 그대로',
                out['b']['per_bed'] == {'D0.7-50': PASS, 'D3-50 s1': FAIL} and out['b']['result'] == FAIL and out['a']['result'] == PASS,
                out['b'])
        go('V2 판정', v2)

        def v3():
            out = S.verdict('v3', log={'B': dict(drop_last_loop=True)})
            chk('V3 B 로그 끝 Loop time 없음 → (a) 판정 불가 (기술) · (b) 그대로 판정',
                out['a']['result'] == UNDECIDED_TECH and out['b']['result'] == PASS and not out['branches']['B']['t0']['ok'], out['a'])
            out = S.verdict('v3b', log={'F': dict(error=True)})
            chk('V3b F 로그에 ERROR 줄 → (a) · (b) D0.7 둘 다 판정 불가 (기술) · 전체 (b) 판정 불가 (기술)',
                out['a']['result'] == UNDECIDED_TECH and out['b']['per_bed']['D0.7-50'] == UNDECIDED_TECH
                and out['b']['result'] == UNDECIDED_TECH, out['b'])
            out = S.verdict('v3c', log={'C': dict(nan=True)})
            chk('V3c C thermo nan → (b) D0.7 판정 불가 (기술)', out['b']['per_bed']['D0.7-50'] == UNDECIDED_TECH)
            out = S.verdict('v3d', log={'A3': dict(last_step=399000)})
            chk('V3d A3 마지막 thermo step ≠ 창 끝 → (b) D3 판정 불가 (기술)', out['b']['per_bed']['D3-50 s1'] == UNDECIDED_TECH)
            out = S.verdict('v3e', log={'B': dict(drop_last_loop=True)}, del_dumps=('B',))
            chk('V3e T0 실패 가지 (B) 의 덤프가 없어도 거부 아님 (판정 불가 (기술))', out['a']['result'] == UNDECIDED_TECH)
        go('V3 T0', v3)

        def v4():
            out = S.verdict('v4', only=('A', 'B', 'C', 'F'))
            chk('V4 D0.7 만 읽음 → (a) 판정 · (b) 전체 = 판정 불가 (D3 없음 · 이유 적음) · D0.7 (b) 합격 + 한정어',
                out['a']['result'] == PASS and out['b']['result'] == UNDECIDED and '침대 하나' in out['b']['why']
                and out['beds']['D0.7-50']['comparisons']['b'].get('qualifier') == QUALIFIER_W1_B, out['b'])
        go('V4 침대 하나', v4)

        def v5():
            w1 = S.verdict('v5')
            w2 = dict(w1, window='W2', a=dict(result=FAIL, why='x'), b=dict(result=PASS, why='x', per_bed={}))
            c = combine(w1, w2)
            chk('V5 combine W1 (합격) + W2 ((a) 불합격) → (a) 불합격 · (b) 합격 (창마다 · 나쁜 쪽)',
                c['a']['result'] == FAIL and c['b']['result'] == PASS and c['a']['per_window'] == {'W1': PASS, 'W2': FAIL})
            try:
                combine(w1, w1)
                chk('V5b combine W1 + W1 → 거부', False)
            except Refused:
                chk('V5b combine W1 + W1 → 거부', True)
        go('V5 combine', v5)

        def v6():
            out = S.verdict_w2('v6')
            it = out['beds']['D0.7-50']['comparisons']['a']['items']
            chk('V6 W2 (합성 manifest · 리포 대조 끔) — 결정 = O2 · O3 · O3 = 마지막 0.05 s pressMPa 평균 (손 계산) · O1 판정 안 함',
                set(it) == set(ITEMS['O2'] + ITEMS['O3']) and abs(it['O3.P']['a'] - S.o3_expect) < 1e-12
                and out['a']['result'] == PASS and 'qualifier' not in (out['b'] or {}), (it.get('O3.P'), S.o3_expect))
            chk('V6a 리포 대조를 끈 사실이 결과에 남는다 (가지마다 repo_verify = skipped …)',
                all(b['repo_verify'].startswith('skipped') for b in out['branches'].values()))
            out = S.verdict_w2('v6b', press={'B': 1.06})
            chk('V6b W2 B 압력 +6 % → O3 불합격 → (a) 불합격', out['a']['result'] == FAIL
                and out['beds']['D0.7-50']['comparisons']['a']['items']['O3.P']['result'] == FAIL)
            rep = out['beds']['D0.7-50']['report']
            chk('V6c W2 보고 R5 감쇠 몫 = Σγ|v_z| / (P·면적·10⁶) (손 계산 · B γ 0.5 · C SE γ 0.5·s)',
                abs(rep['B']['R5_damp_share'] - S.r5_expect('B', 1.06)) < 1e-15
                and abs(rep['C']['R5_damp_share'] - S.r5_expect('C', 1.0)) < 1e-15,
                (rep['B'].get('R5_damp_share'), S.r5_expect('B', 1.06)))
        go('V6 W2', v6)

        def v7():
            buf = io.StringIO()
            R = S.prepare('cli', only=('A', 'B', 'C', 'F'))
            js = os.path.join(tmp, 'cli.json')
            with redirect_stdout(buf):
                rc = main(sum([['--branch', f'{r}={R[r]}'] for r in ('A', 'B', 'C', 'F')], []) + ['--json', js])
            with open(js, encoding='utf-8') as fh:
                jout = json.load(fh)
            chk('V7 CLI 판정 = rc 0 · JSON 기록', rc == 0 and jout['a']['result'] == PASS, buf.getvalue()[-300:])
            with redirect_stdout(io.StringIO()):
                rc = main(['--branch', f'A={R["A"]}', '--branch', f'F={R["A"]}'])
            chk('V7b CLI 거부 (같은 폴더 두 역할) = rc 2', rc == 2)
            with redirect_stdout(io.StringIO()):
                rc = main(['--branch', f'B={R["B"]}'])
            chk('V7c CLI 거부 (A · F 없이 B 만) = rc 2', rc == 2)
        go('V7 CLI', v7)

        def v8():
            R = S.prepare('v8', only=('A', 'B', 'C', 'F'))
            ml = os.path.join(tmp, 'main_log.liggghts')
            with open(ml, 'w') as f:
                f.write('    Step    Atoms         zmax \n200001 12 0.0055\n200002 12 0.0055\nLoop time of 2 on 56 procs for 1 steps with 12 '
                        'atoms\n====== PLATE HEIGHT: 0.0123 ======\n')
            out = run(R, main_log=ml)
            m = out.get('R6_main_log') or {}
            chk('V8 --main-log (§8-3 2) — 멈춘 본 런의 체크포인트 뒤 판 높이 run 줄 · PLATE HEIGHT ↔ A = 같음 (보고)',
                m.get('thermo_same') is True and m.get('plate_same') is True and out['a']['result'] == PASS, m)
            with open(ml, 'w') as f:
                f.write('    Step    Atoms         zmax \n200001 12 0.0124\n200002 12 0.0124\n====== PLATE HEIGHT: 0.0124 ======\n')
            m = run(S.prepare('v8b', only=('A', 'B', 'C', 'F')), main_log=ml).get('R6_main_log') or {}
            chk('V8b 본 런 줄이 다르면 다름으로 보고 (판정은 안 바뀐다)', m.get('thermo_same') is False and m.get('plate_same') is False, m)
        go('V8 본 런 로그', v8)

        # ── 거부 (fail-closed) · 변이: 관문 하나를 끄면 그것을 겨눈 시험이 실패해야 한다 ──
        def m_all():
            cases = S.adversarial()
            for lab, fn in cases.pop('__extra__'):
                chk(f'X {lab}', fn() is True)
            for g in GUARDS:
                if g not in cases:
                    chk(f'M {g}: 겨눈 시험 있음', False)
                    continue
                lab, fn, also = cases[g]
                try:
                    for x in also:
                        GUARDS[x] = False
                    on = fn()
                    GUARDS[g] = False
                    off = fn()
                finally:
                    for x in GUARDS:
                        GUARDS[x] = True
                chk(f'M {g}: {lab}' + (f' (같이 끔: {", ".join(also)})' if also else '') + ' → 켜면 막음 · 끄면 통과',
                    on is True and off is False, (on, off))
        go('M 거부 · 변이', m_all)
    finally:
        for g in GUARDS:
            GUARDS[g] = True
        shutil.rmtree(tmp, ignore_errors=True)
    n, N = tally
    print(f'kg50_q5_verdict selftest: {"PASS" if n == N else "FAIL"} ({n}/{N})')
    return 0 if n == N else 1


class Synth:
    """selftest 합성 자료 — 생성기가 만든 진짜 가지 폴더 (덱 · manifest) 에 작은 침대 (AM 4 · SE 8 · 접촉 28) 의 로그 · 덤프 · ckpt.

    접촉: AM–AM 2 · AM–SE 6 · SE–SE 20 (SE 5–11 사이 21 쌍 중 20 · SE 12 는 접촉 없음).  cn_SE_SE = 40/8 = 5 (이진수 정확 ·
    하나 빼면 4.75 → 상대 차 0.25/5 = τ 0.05 정확 → 경계 시험)."""
    AM = [(1, 0.010, 0.010, 0.004), (2, 0.030, 0.012, 0.0045), (3, 0.012, 0.035, 0.005), (4, 0.040, 0.040, 0.0055)]
    SEZ = [0.0010 + 0.0005 * k for k in range(8)]

    def __init__(self, base, mans):
        import shutil
        self.base, self.mans, self.shutil = base, mans, shutil
        self.root = os.path.join(os.path.dirname(base), 'syn')
        os.makedirs(self.root)
        se = [(a, b) for a in range(5, 12) for b in range(a + 1, 12)][:20]
        self.contacts = [(1, 2), (3, 4), (1, 5), (1, 6), (2, 7), (3, 8), (4, 9), (4, 10)] + se
        self.n_tag = 0

    def rse(self, case):
        return 0.00035 if case == 'kg50_d07_b50' else 0.0015

    def atoms(self, man, step, zse=1.0, vx_tag=0.0, dx=0.0):
        rows = [(i, 1, x + dx, y, z, 0.003, vx_tag, 0.0, -1e-4) for i, x, y, z in self.AM]
        for k, z in enumerate(self.SEZ):
            rows.append((5 + k, 3, 0.002 + 0.0055 * k + dx, 0.025, z * zse, self.rse(man['case']), vx_tag, 0.0, -2e-4))
        return rows

    def zbar(self, P):
        man = self.mans['A']
        rows = self.atoms(man, man['compare_step'])
        rho = {1: 4850.0, 3: 1640.0}
        sel = [r for r in rows if (r[1] == 3) == (P == 'SE')]
        return math.fsum(rho[r[1]] * r[5] ** 3 * r[4] for r in sel) / math.fsum(rho[r[1]] * r[5] ** 3 for r in sel)

    @staticmethod
    def write_atom(path, step, rows):
        with open(path, 'w') as f:
            f.write(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n{len(rows)}\nITEM: BOX BOUNDS pp pp ff\n0 0.05\n0 0.05\n-0.01 1\n'
                    'ITEM: ATOMS id type x y z radius vx vy vz\n')
            for r in rows:
                f.write('%d %d %.10g %.10g %.10g %.10g %.10g %.10g %.10g\n' % r)

    @staticmethod
    def write_contact(path, step, pairs):
        with open(path, 'w') as f:
            f.write(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ENTRIES\n{len(pairs)}\nITEM: BOX BOUNDS pp pp ff\n0 0.05\n0 0.05\n-0.01 1\n'
                    'ITEM: ENTRIES ' + ' '.join(CONTACT_COLS) + '\n')
            for a, b in pairs:
                v = ['0'] * 26
                v[6], v[7], v[22] = str(a), str(b), '1e-06'
                f.write(' '.join(v) + '\n')

    @staticmethod
    def write_log(path, man, deck, ke_end=1e-9, plate='0.0123', drop_last_loop=False, error=False, nan=False, last_step=None,
                  procs=None, press=1.0, dt_echo=None, drop_cmd=None, zmax='0.0055', atoms_end=12):
        """LIGGGHTS 꼴 로그 — 덱 명령 echo (주석 · 이어 붙이기 정리) · timestep 치환 줄 · print 출력 · run 마다 thermo + Loop time."""
        out = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled 2025-08-25)']
        runs, step, k = list(man['runs']), man['s0'], 0
        for c, _a, _b in commands(deck):
            if c == drop_cmd:
                continue
            out.append(c)
            if c == 'timestep ${dt}':
                out.append('timestep ' + (dt_echo or man['dt_echo']))
            if c.startswith('print "====== PLATE HEIGHT'):
                out.append(f'====== PLATE HEIGHT: {plate} ======')
            if not c.startswith('run '):
                continue
            n = runs[k]
            every = man['thermo_every'][k]
            if k == 0 and man['window'] == 'W1':
                out.append('    Step    Atoms         zmax ')
                rows = [f'{step} 12 {zmax}', f'{step + n} 12 {zmax}']
            else:
                out.append('    Step    Atoms         KinEng            CPU       pressMPa ')
                ss = sorted({step, step + n} | set(range(((step + every - 1) // every) * every, step + n + 1, every)))
                rows = [f'{s} {atoms_end if s == step + n else 12} {ke_end if s == step + n else 2e-9} 1.5 '
                        f'{press * (1.0 + (s - man["s0"]) * man["dt"]):.12g}' for s in ss]
                if nan:
                    rows[len(rows) // 2] = rows[len(rows) // 2].split()[0] + ' 12 nan 1.5 0'
                if last_step is not None and k == len(runs) - 1:
                    rows[-1] = f'{last_step} 12 {ke_end} 1.5 0'
            out += rows
            if error and k == len(runs) - 1:
                out.append('ERROR: Lost atoms: original 12 current 11 (../thermo.cpp:389)')
            if not (drop_last_loop and k == len(runs) - 1):
                out.append(f'Loop time of 1.5 on {procs or man["np"]} procs for {n} steps with 12 atoms, '
                           'finish time Tue Oct 28 10:00:00 2026')
            step += n
            k += 1
        with open(path, 'w') as f:
            f.write('\n'.join(out) + '\n')

    def _w2(self, man):
        """W2 합성 manifest · 덱 (생성기가 W2 를 거부하므로 selftest 안에서만 · 리포 대조 끔)."""
        m = json.loads(json.dumps(man))
        m['window'], m['s0'] = 'W2', 1000000
        m['runs'] = [600000] if m['kind'] == 'dt_half' else [300000]
        m['end_step'] = m['compare_step'] = m['s0'] + m['runs'][0]
        m['checkpoint']['step'] = m['s0']
        m['thermo_every'] = [2000] if m['kind'] == 'dt_half' else [1000]
        for k in ('atom_dump', 'contact_dump'):
            m[k]['every'] = 100000
            m[k]['steps'] = expected_steps(m['s0'], m['end_step'], 100000)
        sc = m['damp']['scale']
        deck = ('# selftest W2 덱 (합성)\nunits si\nvariable dt equal %s\ntimestep ${dt}\nread_restart restart_%s/restart_compress_%d.bin\n'
                'fix damp all viscous 0.5%s\nthermo 1000\nrun %d\n') % (
            '5.0e-7' if m['kind'] == 'dt_half' else '1.0e-6', m['case'], m['s0'], (' scale 3 ' + sc['s']) if sc else '', m['runs'][0])
        m['deck']['sha256'] = _sha256_bytes(deck.encode('utf-8'))
        return m, deck

    def prepare(self, tag, only=None, zse=None, drop_ss=None, log=None, del_dumps=(), w2=False, press=None, thermo_every=None):
        roles = only or tuple(self.mans)
        self.n_tag += 1
        off = 1e-9 * self.n_tag
        out = {}
        for i, r in enumerate(roles):
            man = self.mans[r]
            dst = os.path.join(self.root, tag, man['folder'])
            self.shutil.copytree(os.path.join(self.base, man['folder']), dst)
            deck = None
            if w2:
                man, deck = self._w2(man)
                if thermo_every and r in thermo_every:
                    man['thermo_every'] = [thermo_every[r]]
                with open(os.path.join(dst, man['deck']['file']), 'w', encoding='utf-8') as f:
                    f.write(deck)
                with open(os.path.join(dst, 'q5_manifest.json'), 'w', encoding='utf-8') as f:
                    json.dump(man, f)
            post = os.path.join(dst, man['atom_dump']['dir'])
            os.makedirs(post)
            z = (zse or {}).get(r, 1.0)
            for s in man['atom_dump']['steps']:
                self.write_atom(os.path.join(post, f'q5atom_{s}.liggghts'), s,
                                self.atoms(man, s, zse=(z if s == man['compare_step'] else 1.0),
                                           vx_tag=(0.0 if s == man['s0'] else 1e-7 * (i + 1) + off),
                                           dx=(0.0 if s == man['s0'] else 1e-6 * (i % 4 + 1))))
            se = [p for p in self.contacts if p[0] >= 5]
            pairs = [p for p in self.contacts if p not in se[:(drop_ss or {}).get(r, 0)]]
            for s in man['contact_dump']['steps']:
                self.write_contact(os.path.join(post, f'q5contact_{s}.liggghts'), s, pairs if s == man['compare_step'] else self.contacts)
            with open(os.path.join(dst, man['deck']['file']), encoding='utf-8') as f:
                deck = f.read()
            self.write_log(os.path.join(dst, 'log.liggghts'), man, deck, press=(press or {}).get(r, 1.0), **(log or {}).get(r, {}))
            h = hashlib.sha256(('ckpt-' + man['case']).encode()).hexdigest()
            root = '/home/u/dem_test' if man['case'] == 'kg50_d07_b50' else '/home/u/simulation'
            rel = man['checkpoint']['rel_path']
            with open(os.path.join(dst, 'ckpt_sha256.txt'), 'w') as f:
                f.write(f'{h}  {root}/{man["case"]}/{rel}\n{h}  {root}/{man["folder"]}/{rel}\n')
            if r in del_dumps:
                self.shutil.rmtree(post)
            out[r] = dst
        return out

    def verdict(self, tag, only=None, **kw):
        return run(self.prepare(tag, only=only, **kw))

    def verdict_w2(self, tag, press=None):
        R = self.prepare(tag, only=('A', 'B', 'C', 'F'), w2=True, press=press)
        self.w2man = {r: json.load(open(os.path.join(R[r], 'q5_manifest.json'), encoding='utf-8')) for r in R}
        m = self.w2man['A']
        ss = [s for s in range(m['s0'], m['end_step'] + 1, 1000) if m['end_step'] - 50000 <= s]
        self.o3_expect = math.fsum(float('%.12g' % (1.0 + (s - m['s0']) * m['dt'])) for s in ss) / len(ss)
        return run(R, repo_verify=False)

    def r5_expect(self, r, press):
        m = self.w2man[r]
        P = float('%.12g' % (press * (1.0 + (m['end_step'] - m['s0']) * m['dt'])))
        g = {1: 0.5, 2: 0.5, 3: 0.5 * (float(m['damp']['scale']['s']) if m['damp']['scale'] else 1.0)}
        rows = self.atoms(m, m['compare_step'])
        return math.fsum(g[x[1]] * abs(x[8]) for x in rows) / (P * m['area_sim'] * 1e6)

    # ── 거부 시험 (관문마다 하나 · 그 관문만 걸리게) ──
    def adversarial(self):
        D7 = ('A', 'B', 'C', 'F')
        tn = [0]

        def fresh(**kw):
            tn[0] += 1
            return self.prepare('adv%d' % tn[0], **kw)

        def refused(roles, **kw):
            try:
                run(roles, **kw)
            except Refused:
                return True
            except Exception:           # noqa: BLE001 — 다른 예외 = 올바른 거부가 아니다
                return False
            return False

        def tech(roles):
            try:
                out = run(roles)
            except Exception:           # noqa: BLE001
                return False
            return out['a']['result'] == UNDECIDED_TECH

        def edit(path, old, new):
            with open(path, encoding='utf-8') as f:
                t = f.read()
            if old not in t:
                raise AssertionError(f'{path}: [{old}] 없음')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(t.replace(old, new, 1))

        def man_edit(folder, fn):
            p = os.path.join(folder, 'q5_manifest.json')
            with open(p, encoding='utf-8') as f:
                m = json.load(f)
            fn(m)
            with open(p, 'w', encoding='utf-8') as f:
                json.dump(m, f)

        def row_edit(path, k, col, val):
            with open(path) as f:
                t = f.read().split('\n')
            x = t[k].split()
            x[col] = val
            t[k] = ' '.join(x)
            with open(path, 'w') as f:
                f.write('\n'.join(t))

        def post(R, r, name):
            return os.path.join(R[r], self.mans[r]['atom_dump']['dir'], name)

        C = {}

        def c_manifest():
            R = fresh(only=D7)
            man_edit(R['B'], lambda m: m.__setitem__('end_step', m['end_step'] + 1))
            return refused(R)
        C['manifest'] = ('B manifest 끝 step +1 (s0 + run 합 아님)', c_manifest, ())

        def c_role():
            R = fresh(only=D7)
            R2 = fresh(only=('F',))
            return refused({'A': R['A'], 'B': R['B'], 'C': R2['F'], 'F': R['F']})
        C['role'] = ('다른 F 폴더를 C 역할로', c_role, ())

        def c_deck_sha():
            R = fresh(only=D7)
            edit(os.path.join(R['B'], self.mans['B']['deck']['file']), '# ===== 50kg Q5 가지 B', '# ===== 50kg Q5 가지  B')
            return refused(R)
        C['deck_sha'] = ('B 가지 덱 머리 주석 한 글자 (sha256 만 다름)', c_deck_sha, ('repo_verify',))

        def c_repo():
            R = fresh(only=D7)
            p = os.path.join(R['B'], self.mans['B']['deck']['file'])
            edit(p, 'fix gravi all gravity 9.81 vector', 'fix gravi all gravity 9.80 vector')
            sha = _sha256_bytes(open(p, 'rb').read())
            man_edit(R['B'], lambda m: m['deck'].__setitem__('sha256', sha))
            edit(os.path.join(R['B'], 'log.liggghts'), 'fix gravi all gravity 9.81 vector', 'fix gravi all gravity 9.80 vector')
            return refused(R)
        C['repo_verify'] = ('B 덱 물리 줄 바꾸고 manifest sha256 · 로그도 맞춤 (리포 허용 목록만 잡는다)', c_repo, ())

        def c_ckpt():
            R = fresh(only=D7)
            p = os.path.join(R['C'], 'ckpt_sha256.txt')
            with open(p) as f:
                a, b = f.read().split('\n')[:2]
            with open(p, 'w') as f:
                f.write(a + '\n' + '0' * 64 + b[64:] + '\n')
            return refused(R)
        C['ckpt'] = ('C 체크포인트 원본 ↔ 사본 sha256 다름', c_ckpt, ())

        def c_log():
            R = fresh(only=D7)
            os.remove(os.path.join(R['B'], 'log.liggghts'))
            return refused(R)
        C['log_missing'] = ('B log.liggghts 없음', c_log, ('dt_echo',))

        C['np_procs'] = ('F 로그 Loop time 56 procs (manifest 28)', lambda: refused(fresh(only=D7, log={'F': dict(procs=56)})), ())
        C['dt_echo'] = ('B 로그 dt 치환 줄 1e-06 (B 덱 5e-07)', lambda: refused(fresh(only=D7, log={'B': dict(dt_echo='1e-06')})), ())
        C['echo'] = ('C 로그에 scale 감쇠 명령 echo 없음 (다른 덱으로 돈 로그)',
                     lambda: refused(fresh(only=D7, log={'C': dict(drop_cmd='fix damp all viscous 0.5 scale 3 5.3696e-4')})), ())

        def c_start():
            R = fresh(only=D7)
            edit(os.path.join(R['A'], 'log.liggghts'), '\n200001 12 0.0055\n', '\n200000 12 0.0055\n')
            return refused(R)
        C['start_step'] = ('A 첫 thermo step 200000 (체크포인트 200001 아님)', c_start, ())
        C['t0_loop'] = ('B 끝 Loop time 없음 (덤프는 다 있음)', lambda: tech(fresh(only=D7, log={'B': dict(drop_last_loop=True)})), ())
        C['t0_error'] = ('B ERROR 줄', lambda: tech(fresh(only=D7, log={'B': dict(error=True)})), ())
        C['t0_finite'] = ('B thermo nan', lambda: tech(fresh(only=D7, log={'B': dict(nan=True)})), ())
        C['t0_end'] = ('B 마지막 thermo step 599000', lambda: tech(fresh(only=D7, log={'B': dict(last_step=599000)})), ())

        def c_set():
            R = fresh(only=D7)
            os.remove(post(R, 'B', 'q5atom_466669.liggghts'))
            return refused(R)
        C['dump_set'] = ('B 중간 atom 덤프 하나 없음 (T0 통과)', c_set, ())

        def c_ts():
            R = fresh(only=D7)
            edit(post(R, 'C', 'q5atom_266668.liggghts'), 'ITEM: TIMESTEP\n266668\n', 'ITEM: TIMESTEP\n266669\n')
            return refused(R)
        C['dump_timestep'] = ('C 덤프 TIMESTEP ≠ 이름', c_ts, ())

        def c_frames():
            R = fresh(only=D7)
            p = post(R, 'C', 'q5atom_400002.liggghts')
            with open(p) as f:
                t = f.read()
            with open(p, 'w') as f:
                f.write(t + t)
            return refused(R)
        C['dump_frames'] = ('C 창 끝 atom 덤프에 프레임 둘', c_frames, ('dump_rows', 'dump_format', 'dump_dup_id', 'bind_atoms'))

        def c_rows():
            R = fresh(only=D7)
            p = post(R, 'C', 'q5atom_333335.liggghts')
            with open(p) as f:
                t = f.read().split('\n')
            with open(p, 'w') as f:
                f.write('\n'.join(t[:-4]) + '\n')
            return refused(R)
        C['dump_rows'] = ('C 중간 atom 덤프 잘림 (줄 < NUMBER OF ATOMS)', c_rows, ())

        def c_format():
            R = fresh(only=D7)
            p = post(R, 'C', 'q5atom_400002.liggghts')
            with open(p) as f:
                t = f.read().split('\n')
            t[9 + 11] = ' '.join(t[9 + 11].split()[:8])
            with open(p, 'w') as f:
                f.write('\n'.join(t))
            return refused(R)
        C['dump_format'] = ('C 창 끝 atom 줄 하나 열 8 (id 12 · 접촉 없음)', c_format, ('bind_atoms',))

        def c_atoms():
            return refused(fresh(only=D7, log={'B': dict(atoms_end=11)}))
        C['bind_atoms'] = ('B 로그 마지막 Atoms 11 ↔ 창 끝 덤프 12 (다른 실행의 덤프)', c_atoms, ())

        def c_zmax():
            return refused(fresh(only=D7, log={'C': dict(zmax='0.0056')}))
        C['bind_zmax'] = ('C 로그 첫 zmax 0.0056 ↔ 시작 덤프 z 최대 0.0055', c_zmax, ())

        # ── 관문 변이 밖의 거부 (모든 관문 켬) ──
        def x_ascii(col_row):
            def f():
                R = fresh(only=D7)
                row_edit(post(R, 'C', 'q5atom_400002.liggghts'), 9, col_row, '0.0١')
                return refused(R)
            return f

        def x_ascii_contact():
            R = fresh(only=D7)
            p = os.path.join(R['C'], self.mans['C']['contact_dump']['dir'], 'q5contact_400002.liggghts')
            row_edit(p, 9, 6, '١')
            return refused(R)

        def x_thermo_unicode():
            R = fresh(only=D7)
            edit(os.path.join(R['B'], 'log.liggghts'), '\n200003 12 2e-09 1.5 ', '\n200003 12 2e-09 ١.5 ')
            try:
                out = run(R)
            except Exception:           # noqa: BLE001
                return False
            return out['a']['result'] == UNDECIDED_TECH

        def x_np_bool():
            R = fresh(only=D7)
            man_edit(R['A'], lambda m: m.__setitem__('s0', True))
            return refused(R)

        def x_json_nan():
            R = fresh(only=D7)
            p = os.path.join(R['F'], 'q5_manifest.json')
            with open(p, encoding='utf-8') as f:
                t = f.read()
            with open(p, 'w', encoding='utf-8') as f:
                f.write(re.sub(r'"area_sim": [0-9.e+-]+', '"area_sim": NaN', t))
            return refused(R)

        def x_empty_log():
            R = fresh(only=D7)
            open(os.path.join(R['F'], 'log.liggghts'), 'w').close()
            return tech(R)
        C['__extra__'] = [('C 창 끝 atom x 에 유니코드 숫자 (float() 은 받는다) → 거부', x_ascii(2)),
                          ('C 창 끝 contact id 에 유니코드 숫자 → 거부', x_ascii_contact),
                          ('B thermo CPU 열에 유니코드 숫자 → T0 실패 (판정 불가 (기술))', x_thermo_unicode),
                          ('A manifest s0 = true (JSON bool 은 정수가 아니다) → 거부', x_np_bool),
                          ('F manifest area_sim = NaN (JSON NaN) → 거부', x_json_nan),
                          ('F log.liggghts 비어 있음 → 거부 아님 · T0 실패 (판정 불가 (기술))', x_empty_log)]

        def c_finite():
            R = fresh(only=D7)
            row_edit(post(R, 'B', 'q5atom_600003.liggghts'), 12, 4, 'nan')
            return refused(R)
        C['dump_finite'] = ('B 창 끝 atom z = nan', c_finite, ())

        def c_dup():
            R = fresh(only=D7)
            row_edit(post(R, 'F', 'q5atom_400002.liggghts'), 9 + 11, 0, '11')
            return refused(R)
        C['dump_dup_id'] = ('F 창 끝 atom id 12 → 11 (중복 · 12 는 접촉 없음)', c_dup, ())

        def c_cols():
            R = fresh(only=D7)
            edit(post(R, 'F', 'q5atom_400002.liggghts'), 'radius vx vy vz', 'radius vx vz vy')
            return refused(R)
        C['dump_cols'] = ('F atom 열 순서 vy ↔ vz', c_cols, ())

        def c_type():
            R = fresh(only=D7)
            row_edit(post(R, 'F', 'q5atom_400002.liggghts'), 13, 1, '4')
            return refused(R)
        C['type_known'] = ('F type 4 (type_map 에 없음)', c_type, ())

        def contact(fn):
            R = fresh(only=D7)
            p = os.path.join(R['C'], self.mans['C']['contact_dump']['dir'], 'q5contact_400002.liggghts')
            with open(p) as f:
                t = f.read().split('\n')
            fn(t)
            with open(p, 'w') as f:
                f.write('\n'.join(t))
            return refused(R)

        def dup_pair(t):
            x = t[10].split()
            x[6], x[7] = t[9].split()[7], t[9].split()[6]
            t[10] = ' '.join(x)

        def self_pair(t):
            x = t[9].split()
            x[7] = x[6]
            t[9] = ' '.join(x)

        def unknown_id(t):
            x = t[9].split()
            x[7] = '999'
            t[9] = ' '.join(x)

        def nan_col(t):
            x = t[9].split()
            x[0] = 'nan'
            t[9] = ' '.join(x)
        C['contact_dup'] = ('C 접촉 a–b · b–a 두 줄', lambda: contact(dup_pair), ())
        C['contact_self'] = ('C 접촉 자기 쌍', lambda: contact(self_pair), ())
        C['contact_ids'] = ('C 접촉 id 999 (atom 덤프에 없음)', lambda: contact(unknown_id), ())
        C['contact_finite'] = ('C 접촉 첫 열 nan', lambda: contact(nan_col), ())

        def c_bed():
            R = fresh(only=D7)
            p = os.path.join(R['C'], self.mans['C']['main_deck']['copy'])
            with open(p, 'ab') as f:
                f.write(b'# extra\n')
            with open(p, 'rb') as f:
                sha = _sha256_bytes(f.read())
            man_edit(R['C'], lambda m: m['main_deck'].__setitem__('sha256', sha))
            return refused(R, repo_verify=False)
        C['bed'] = ('C 의 본 덱 sha256 이 다른 가지와 다름 (사본 · manifest 맞춤 · 리포 대조 끔)', c_bed, ())

        def c_t0():
            R = fresh(only=D7)
            edit(post(R, 'C', 'q5atom_200001.liggghts'), '\n1 1 0.01 0.01 0.004 ', '\n1 1 0.01 0.01 0.0040001 ')
            return refused(R)
        C['t0_identity'] = ('C 시작 상태 덤프 한 값 다름', c_t0, ())

        def c_end():
            R = fresh(only=D7)
            self.shutil.copyfile(post(R, 'A', 'q5atom_400002.liggghts'), post(R, 'F', 'q5atom_400002.liggghts'))
            return refused(R)
        C['end_identity'] = ('F 끝 atom 덤프 = A 사본', c_end, ())

        def c_fnp():
            R = fresh(only=D7, log={'F': dict(procs=56)})
            man_edit(R['F'], lambda m: m.__setitem__('np', 56))
            return refused(R, repo_verify=False)
        C['floor_np'] = ('F NP 56 = A (manifest · 로그 맞춤 · 리포 대조 끔)', c_fnp, ())

        def c_same():
            R = fresh(only=D7)
            return refused({'A': R['A'], 'B': R['B'], 'C': R['B'], 'F': R['F']})
        C['same_folder'] = ('B 폴더를 B · C 두 역할에', c_same, ('role', 'end_identity'))

        def c_window():
            R = fresh(only=D7)
            R3 = fresh(only=('A3', 'C3', 'F3'), w2=True)
            R.update(R3)
            return refused(R, repo_verify=False)
        C['window'] = ('D0.7 = W1 · D3 = W2 (창 섞임)', c_window, ())

        def c_times():
            R = fresh(only=D7, w2=True, thermo_every={'B': 1000})
            return refused(R, repo_verify=False)
        C['thermo_times'] = ('W2 B thermo 간격 1000 (A 시각과 다른 표본)', c_times, ())
        return C


if __name__ == '__main__':
    sys.exit(main())
