# -*- coding: utf-8 -*-
"""믹서 침대 보기 — `/mixer` 의 "침대 보기" 탭이 부르는 **읽기 전용** 도우미 (1저자 비준 2026-09-30).

★ 보기 전용 — 판정은 3D 칸 M (`scripts/measure_mixing_index.py`) 으로만.  여기서는 혼합 지표 · 겹침을
  **계산하지 않는다**.  단면 · 투영은 눈으로 보는 필터일 뿐 판정 근거가 아니다.
★ 경로 — 런 루트 = 환경변수 `WEBAPP_MIXER_RUNS` (`os.pathsep` 로 여럿) · 없으면 `<리포>/dem_scripts/mixer_20260921/runs`.
  루트 번호 · 런 이름 · step 은 정규식 fullmatch 로만 받고, 프레임 파일은 **목록에서 고른 이름**만 연다
  (요청 문자열로 경로를 만들지 않는다).  열기 전에 realpath 가 루트 안인지 다시 본다 (심볼릭 링크 탈출).
★ 맹검 — 정책 파일 `webapp/mixer_view_policy.json` 의 패턴 (fullmatch) 에 든 런만 연다.  나머지는 잠근다 —
  고-Bo · 강성 축 확인 런처럼 M-맹검으로 등록된 런을 이 화면이 깨지 않게 (fail-closed · 파일이 깨져도 전부 잠금).
★ 덤프 스키마 = `measure_bed_aspect.validate_frame` (판독기 · 검사기와 같은 관문) — 문제가 있으면 그리지 않는다.
★ 쓰기 없음 — 런 폴더에 캐시 · 부산물을 남기지 않는다 (메모리 LRU 만).
★ 색 · 상 이름은 새로 정하지 않는다 — 색은 `viz_mixer_bed` (PNG 와 같은 팔레트), 상 이름은 덱의 템플릿 시드
  (`make_mixer_deck.TPL_SEED`) 에서 읽는다.  못 읽으면 "type N" 으로 두고 짐작하지 않는다.
"""
from __future__ import annotations

import base64
import functools
import json
import math
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DEFAULT_ROOT = os.path.join(REPO, 'dem_scripts', 'mixer_20260921', 'runs')
POLICY_PATH = os.path.join(HERE, 'mixer_view_policy.json')
POLICY_SCHEMA = 'mixer_view_policy/1'
VIEW_ONLY = '보기 전용 — 판정은 3D 칸 M 으로만'

RUN_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_]{0,95}')
FRAME_RE = re.compile(r'mix_(0|[1-9][0-9]{0,11})\.liggghts')        # 앞자리 0 없음 → 같은 step 두 파일 불가
STEP_Q_RE = re.compile(r'[0-9]{1,12}')
ROOT_Q_RE = re.compile(r'[0-9]{1,2}')
MAX_FRAME_BYTES = 256 * 1024 * 1024
MAX_STL_BYTES = 16 * 1024 * 1024
VIEWS = ('3d', 'slab', 'proj')
SLAB_RULE = 'x₀ − t/2 ≤ x ≤ x₀ + t/2 (입자 중심 · 닫힌 구간) · 원 크기 = 실제 반경'
_FALLBACK_COL = ('#9467bd', '#17becf', '#bcbd22', '#e377c2', '#8c564b')
_LOCK_MSG = ('맹검 잠금 — 정책 파일 webapp/mixer_view_policy.json 에 없는 런이다 (고-Bo · 강성 축 확인 런처럼 '
             'M-맹검으로 등록된 런일 수 있다).  열려면 판정 · 열람 기록의 근거와 함께 정책에 올린다.')


class Refuse(Exception):
    """요청 거부 — 상태 코드 + 사람이 읽는 사유 (+ 덤프 관문의 문제 목록)."""

    def __init__(self, status, msg, problems=None):
        super().__init__(msg)
        self.status, self.msg, self.problems = status, msg, list(problems or [])

    def payload(self):
        out = {'ok': False, 'error': self.msg, 'view_only': VIEW_ONLY}
        if self.problems:
            out['problems'] = self.problems
        return out


# ── 루트 · 정책 ─────────────────────────────────────────────────────────────────
def roots():
    """[{i, path, exists}] — 환경변수를 **부를 때마다** 읽는다 (시험이 루트를 바꿀 수 있게)."""
    raw = os.environ.get('WEBAPP_MIXER_RUNS')
    parts = [p for p in (raw.split(os.pathsep) if raw else [DEFAULT_ROOT]) if p.strip()]
    out = []
    for i, p in enumerate(parts[:100]):
        ap = os.path.abspath(os.path.expanduser(p.strip()))
        out.append({'i': i, 'path': ap, 'exists': os.path.isdir(ap)})
    return out


def load_policy(path=None):
    """정책 파일 → {ok, allow:[{pattern, basis, since, _rx}], reason}.  하나라도 이상하면 ok False = 전부 잠금."""
    path = path or POLICY_PATH

    def fail(why):
        return {'ok': False, 'allow': [], 'reason': why + ' — 전부 잠금 (fail-closed)'}
    try:
        with open(path, encoding='utf-8') as fh:
            raw = json.load(fh)
    except (OSError, ValueError) as e:
        return fail(f'정책 파일을 못 읽음 ({type(e).__name__})')
    if not isinstance(raw, dict) or raw.get('schema') != POLICY_SCHEMA or not isinstance(raw.get('allow'), list):
        return fail(f'정책 schema 가 {POLICY_SCHEMA} 가 아니다')
    allow = []
    for k, a in enumerate(raw['allow']):
        if not isinstance(a, dict):
            return fail(f'정책 항목 {k} 가 객체가 아니다')
        pat, basis, since = a.get('pattern'), a.get('basis'), a.get('since')
        if not all(isinstance(v, str) and v.strip() for v in (pat, basis, since)):
            return fail(f'정책 항목 {k}: pattern · basis · since 중 빈 것이 있다')
        try:
            rx = re.compile(pat)
        except re.error as e:
            return fail(f'정책 항목 {k}: 정규식 오류 ({e})')
        allow.append({'pattern': pat, 'basis': basis, 'since': since, '_rx': rx})
    return {'ok': True, 'allow': allow, 'reason': ''}


def classify(name, pol):
    """(열림?, 근거 또는 잠금 사유).  패턴은 **fullmatch** — 앞뒤에 무엇이 붙은 이름은 다른 런이다."""
    if not pol.get('ok'):
        return False, '맹검 잠금 — ' + (pol.get('reason') or '정책 없음')
    for a in pol['allow']:
        if a['_rx'].fullmatch(name):
            return True, a['basis']
    return False, _LOCK_MSG


def _policy_public(pol):
    return {'ok': pol['ok'], 'reason': pol['reason'], 'file': 'webapp/mixer_view_policy.json',
            'allow': [{k: a[k] for k in ('pattern', 'basis', 'since')} for a in pol['allow']]}


def _inside(real, root_real):
    return real.startswith(root_real + os.sep)


# ── 덱 (표시용 — 상 이름 · 시간 · 드럼) ────────────────────────────────────────
def _deck_lines(txt):
    """주석 (`#` 뒤) 을 떼고 `&` 이음 줄을 붙인 명령 줄 목록."""
    out, buf = [], ''
    for raw in txt.splitlines():
        s = raw.split('#', 1)[0].rstrip()
        if s.endswith('&'):
            buf += s[:-1] + ' '
            continue
        s = (buf + s).strip()
        buf = ''
        if s:
            out.append(s)
    if buf.strip():
        out.append(buf.strip())
    return out


def _stl_vertices(path):
    """ASCII STL 꼭짓점 (n×3) · 못 읽으면 None (이진 STL 도 None — 짐작하지 않는다)."""
    try:
        if os.path.getsize(path) > MAX_STL_BYTES:
            return None
        with open(path, encoding='ascii', errors='replace') as fh:
            txt = fh.read()
    except OSError:
        return None
    V = re.findall(r'^\s*vertex\s+(\S+)\s+(\S+)\s+(\S+)\s*$', txt, re.M)
    if not V:
        return None
    try:
        A = np.array(V, dtype=float)
    except ValueError:
        return None
    return A if np.all(np.isfinite(A)) else None


def _palette():
    import viz_mixer_bed                                   # PNG 와 같은 팔레트 — 두 벌을 만들지 않는다
    return {viz_mixer_bed.TYPE_LAB[k]: viz_mixer_bed.TYPE_COL[k] for k in viz_mixer_bed.TYPE_COL}


def deck_info(run_dir):
    """런 폴더의 `in.mixer` · `Drum.stl` → 표시용 정보.  못 읽은 것은 None 으로 두고 notes 에 사유를 적는다."""
    notes = []
    info = {'dt': None, 'period': None, 'rot_start_step': None, 'drum': None,
            'type_names': {}, 'types_named': False, 'notes': notes}
    try:
        with open(os.path.join(run_dir, 'in.mixer'), encoding='utf-8', errors='replace') as fh:
            L = _deck_lines(fh.read())
    except OSError:
        notes.append('in.mixer 없음 — 상 이름 · 시간 · 드럼을 덱에서 못 읽는다 (짐작하지 않는다)')
        return info
    # 시간 간격
    dts = {w[1] for w in (l.split() for l in L) if len(w) == 2 and w[0] == 'timestep'}
    try:
        vals = {float(v) for v in dts}
    except ValueError:
        vals = set()
    if len(vals) == 1 and all(math.isfinite(v) and v > 0 for v in vals):
        info['dt'] = vals.pop()
    else:
        notes.append(f'timestep 을 하나로 못 읽음 ({sorted(dts)})')
    # 상 이름 (템플릿 시드 → 상)
    try:
        import make_mixer_deck
        seed_to_phase = {v: k for k, v in make_mixer_deck.TPL_SEED.items()}
    except Exception as e:                                  # noqa: BLE001 — 표시용: 못 읽으면 번호로
        seed_to_phase = {}
        notes.append(f'make_mixer_deck.TPL_SEED 를 못 읽음 ({type(e).__name__})')
    names = {}
    for l in L:
        m = re.search(r'particletemplate/(?:sphere|multisphere)\s+(\d+)\s+atom_type\s+(\d+)\b', l)
        if m:
            names[int(m.group(2))] = seed_to_phase.get(int(m.group(1)))
    if names and all(names.values()) and len(set(names.values())) == len(names):
        info['type_names'] = {str(t): n for t, n in sorted(names.items())}
        info['types_named'] = True
    else:
        notes.append('템플릿 시드로 상 이름을 다 못 읽음 — 번호로만 표시')
    # 드럼 (Drum.stl 꼭짓점 × scale)
    scale = None
    for l in L:
        m = re.match(r'fix\s+\S+\s+all\s+mesh/surface\s+file\s+Drum\.stl\b(.*)$', l)
        if m:
            s = re.search(r'\bscale\s+(\S+)', m.group(1))
            try:
                scale = float(s.group(1)) if s else 1.0
            except ValueError:
                scale = None
            break
    stl = os.path.join(run_dir, 'Drum.stl')
    V = _stl_vertices(stl) if os.path.realpath(stl).startswith(os.path.realpath(run_dir) + os.sep) else None
    if scale is None or not (math.isfinite(scale) and scale > 0):
        notes.append('덱에 Drum.stl 메시 줄 (scale) 이 없다 — 드럼 윤곽 없음')
    elif V is None:
        notes.append('Drum.stl 을 못 읽음 (없음 · 이진 · 비유한) — 드럼 윤곽 없음 (짐작하지 않는다)')
    else:
        rad = np.sqrt(V[:, 1] ** 2 + V[:, 2] ** 2)
        info['drum'] = {'R': float(scale * rad.max()), 'x_min': float(scale * V[:, 0].min()),
                        'x_max': float(scale * V[:, 0].max()), 'scale': scale,
                        'source': 'Drum.stl 꼭짓점 반경 × scale (다각형 외접원 · 회전 위상 무시)'}
        #  gen_all.sh 가 런 옆에 적는 드럼 반경 (판독기 --r-container 입력) — 대조만 하고 그림은 STL 기준 그대로
        try:
            with open(os.path.join(run_dir, 'r_container'), encoding='utf-8') as fh:
                rc = float(fh.read().strip())
        except (OSError, ValueError):
            rc = None
        if rc is not None and math.isfinite(rc) and rc > 0:
            info['drum']['r_container'] = rc
            if abs(info['drum']['R'] - rc) / rc > 1e-3:
                notes.append(f'r_container (생성기 기록 {rc * 1e3:.4f} mm) 가 Drum.stl 반경 '
                             f'{info["drum"]["R"] * 1e3:.4f} mm 와 0.1 % 넘게 다르다 — 그림은 STL 기준')
    # 회전 시작 · 주기 — 드럼 회전 fix 앞의 run 합
    rot_i, period = None, None
    for k, l in enumerate(L):
        m = re.match(r'fix\s+\S+\s+all\s+move/mesh\s+mesh\s+Drum\s+rotate\b.*\bperiod\s+(\S+)', l)
        if m:
            rot_i = k
            try:
                period = float(m.group(1))
            except ValueError:
                period = None
            break
    if rot_i is None or period is None or not (math.isfinite(period) and period > 0):
        notes.append('드럼 회전 줄 (move/mesh … period) 을 못 읽음 — 바퀴 수 없음')
    else:
        tot, odd = 0, []
        for l in L[:rot_i]:
            w = l.split()
            if w[0] == 'run':
                if len(w) < 2 or not w[1].isdigit() or any(x in ('upto', 'start', 'stop', 'every') for x in w[2:]):
                    odd.append(l)
                else:
                    tot += int(w[1])
        if odd:
            notes.append(f'run 줄을 합으로 못 읽음 ({odd[:2]}) — 바퀴 수 없음')
        else:
            info['period'], info['rot_start_step'] = period, tot
    return info


def _type_table(type_names, types_named):
    """{타입 번호: {name, color}} — 덱에서 상 이름을 다 읽었을 때만 (아니면 빈 표 → "type N")."""
    if not types_named:
        return {}
    pal = _palette()
    out = {}
    for k, t in enumerate(sorted(int(x) for x in type_names)):
        n = type_names[str(t)]
        out[str(t)] = {'name': n, 'color': pal.get(n, _FALLBACK_COL[k % len(_FALLBACK_COL)])}
    return out


# ── 프레임 ──────────────────────────────────────────────────────────────────────
def list_frames(run_dir, root_real):
    """[(step, 파일명)] **숫자순** — 이름 규약 밖 · 루트 밖을 가리키는 링크 · 보통 파일 아닌 것은 뺀다."""
    post = os.path.join(run_dir, 'post')
    try:
        names = os.listdir(post)
    except OSError:
        return []
    out = []
    for fn in names:
        m = FRAME_RE.fullmatch(fn)
        if not m:
            continue
        real = os.path.realpath(os.path.join(post, fn))
        if _inside(real, root_real) and os.path.isfile(real):
            out.append((int(m.group(1)), fn))
    return sorted(out)


def list_runs(pol=None):
    """목록 API — 열린 런은 프레임 step · 덱 정보까지, 잠긴 런은 이름 · 사유만."""
    pol = pol or load_policy()
    rs = roots()
    runs = []
    for r in rs:
        if not r['exists']:
            continue
        root_real = os.path.realpath(r['path'])
        try:
            ents = sorted(os.listdir(r['path']))
        except OSError:
            continue
        for name in ents:
            if not RUN_RE.fullmatch(name):
                continue
            d = os.path.join(r['path'], name)
            real = os.path.realpath(d)
            if not (_inside(real, root_real) and os.path.isdir(os.path.join(real, 'post'))):
                continue
            ok, why = classify(name, pol)
            item = {'root': r['i'], 'run': name, 'allowed': ok}
            if ok:
                fr = list_frames(d, root_real)
                item.update(basis=why, steps=[s for s, _ in fr], n_frames=len(fr), deck=deck_info(d))
            else:
                item['reason'] = why
            runs.append(item)
    return {'ok': True, 'view_only': VIEW_ONLY, 'roots': rs, 'runs': runs, 'policy': _policy_public(pol)}


def resolve(root_q, run_q, step_q, pol=None):
    """(런 폴더, 프레임 realpath, step) — 형식 · 맹검 · 루트 안 · 목록 안 을 차례로 본다."""
    for q, rx, what in ((root_q, ROOT_Q_RE, 'root'), (run_q, RUN_RE, 'run'), (step_q, STEP_Q_RE, 'step')):
        if not (isinstance(q, str) and rx.fullmatch(q)):
            raise Refuse(400, f'{what} 형식 밖 — 거부')
    rs = roots()
    ri = int(root_q)
    if ri >= len(rs) or not rs[ri]['exists']:
        raise Refuse(404, '그 번호의 런 루트가 없다')
    ok, why = classify(run_q, pol or load_policy())
    if not ok:
        raise Refuse(403, why)
    root_real = os.path.realpath(rs[ri]['path'])
    d = os.path.join(rs[ri]['path'], run_q)
    real = os.path.realpath(d)
    if not (_inside(real, root_real) and os.path.isdir(real)):
        raise Refuse(404, '런 폴더가 없다 (또는 루트 밖을 가리키는 링크)')
    step = int(step_q)
    fr = dict(list_frames(d, root_real))
    if step not in fr:
        raise Refuse(404, f'step {step} 의 프레임이 목록에 없다')
    p = os.path.realpath(os.path.join(d, 'post', fr[step]))
    if not _inside(p, root_real):
        raise Refuse(404, '프레임이 루트 밖을 가리킨다')
    return d, p, step


def _parse_frame(path):
    """덤프 한 장 → 읽기 전용 배열.  먼저 판독기 · 검사기와 같은 스키마 관문을 지난다."""
    import measure_bed_aspect
    probs = measure_bed_aspect.validate_frame(path)
    if probs:
        raise Refuse(422, '덤프 스키마 관문 실패 — 그리지 않는다', problems=probs)
    with open(path, encoding='utf-8', errors='replace') as fh:
        L = fh.read().split('\n')
    i = next(k for k, l in enumerate(L) if l.startswith('ITEM: ATOMS'))
    cols = L[i].split()[2:]
    A = np.array(' '.join(l for l in L[i + 1:] if l.strip()).split(), dtype=float).reshape(-1, len(cols))
    out = {c: np.ascontiguousarray(A[:, cols.index(c)]) for c in ('id', 'type', 'x', 'y', 'z', 'radius')}
    for a in out.values():
        a.setflags(write=False)
    return out


@functools.lru_cache(maxsize=4)
def _cached(real, mtime_ns, size):
    return _parse_frame(real)


def clear_cache():
    _cached.cache_clear()


def _finite(q, what):
    if not isinstance(q, str) or not q.strip():
        raise Refuse(400, f'{what} 가 없다')
    try:
        v = float(q)
    except ValueError:
        raise Refuse(400, f'{what} 가 수가 아니다') from None
    if not math.isfinite(v):
        raise Refuse(400, f'{what} 가 유한하지 않다')
    return v


def _b64(a, dtype):
    return base64.b64encode(np.ascontiguousarray(a, dtype=dtype).tobytes()).decode('ascii')


def frame_payload(args):
    """프레임 API — args = {root, run, step, view, [x0, t]}.  view: 3d (x0·t 를 주면 그 조각만) · slab · proj."""
    view = args.get('view') or '3d'
    if view not in VIEWS:
        raise Refuse(400, f'view 는 {VIEWS} 중 하나')
    has = [args.get(k) not in (None, '') for k in ('x0', 't')]
    sel = None
    if view == 'slab' or (view == '3d' and any(has)):
        x0, t = _finite(args.get('x0'), 'x0'), _finite(args.get('t'), 't')
        if t <= 0:
            raise Refuse(400, 't (조각 두께) 는 0 보다 커야 한다')
        sel = (x0, t)
    d, path, step = resolve(args.get('root'), args.get('run'), args.get('step'))
    st = os.stat(path)
    if st.st_size > MAX_FRAME_BYTES:
        raise Refuse(413, f'프레임이 {st.st_size:,} B — 상한 {MAX_FRAME_BYTES:,} B 를 넘어 읽지 않는다')
    D = _cached(path, st.st_mtime_ns, st.st_size)
    x = D['x']
    typ = D['type'].astype(np.int64)
    if typ.size and (typ.min() < 1 or typ.max() > 255):
        raise Refuse(422, 'type 이 1–255 밖 — 그리지 않는다')
    m = np.ones(x.shape, dtype=bool) if sel is None else (x >= sel[0] - sel[1] / 2.0) & (x <= sel[0] + sel[1] / 2.0)
    dk = deck_info(d)
    table = _type_table(dk['type_names'], dk['types_named'])
    present = {}
    for k, t in enumerate(sorted(set(typ.tolist()))):
        ent = table.get(str(t)) or {'name': f'type {t}', 'color': _FALLBACK_COL[k % len(_FALLBACK_COL)]}
        present[str(t)] = dict(ent, n_total=int(np.sum(typ == t)), n_shown=int(np.sum(typ[m] == t)))
    rev = phase = None
    if dk['rot_start_step'] is not None and dk['dt'] and dk['period']:
        if step >= dk['rot_start_step']:
            rev, phase = (step - dk['rot_start_step']) * dk['dt'] / dk['period'], 'rotation'
        else:
            phase = 'fill'
    bnd = {c: ([float(D[c].min()), float(D[c].max())] if D[c].size else None) for c in ('x', 'y', 'z')}
    return {
        'ok': True, 'view_only': VIEW_ONLY, 'root': int(args.get('root')), 'run': args.get('run'), 'step': step,
        'time_s': (step * dk['dt'] if dk['dt'] else None), 'rev': rev, 'phase': phase, 'view': view,
        'selection': ({'rule': SLAB_RULE, 'x0': sel[0], 't': sel[1]} if sel else None),
        'n_total': int(x.size), 'n_shown': int(m.sum()), 'types_present': present,
        'types_named': dk['types_named'], 'drum': dk['drum'], 'deck_notes': dk['notes'], 'bounds': bnd,
        'r_max': (float(D['radius'].max()) if D['radius'].size else None),
        'data': {'x': _b64(x[m], '<f4'), 'y': _b64(D['y'][m], '<f4'), 'z': _b64(D['z'][m], '<f4'),
                 'r': _b64(D['radius'][m], '<f4'), 'type': _b64(typ[m], np.uint8)},
    }
