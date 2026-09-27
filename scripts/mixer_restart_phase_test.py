#!/usr/bin/env python3
"""mixer_restart_phase_test.py — 재개-위상 영수증 v1 (2026-09-28, Codex 3차 HBR3-01 · 02 · 03 · Q1 · Q2 · Q5).

왜 — 믹서 드럼은 39 각형이라 벽 겹침은 회전각에 걸린다 (면 한가운데와 꼭짓점의 차 = SE 반경의 56 %).  캠페인 덱은 mesh 를 덤프하지
않으므로 벽 판정의 근거는 **예정각** 2π·(s − start)·dt/period 뿐이다.  그 식이 (i) 긴 회전 내내 (ii) 재개 (read_restart) 뒤에도
맞는지를 **같은 바이너리로 실측**한 기록이 이 영수증이다.

★ 핵심 논리 (v1) — 드럼 회전은 **처방 운동** (fix move/mesh rotate) 이라 입자와 무관하다.  그래서 캠페인 덱에서 **입자만 뺀** 덱을
  **같은 step 구조** (삽입 run 1 · 정착 두 run · 회전 run 을 그대로) 로 돌리면, 메시는 캠페인 런과 같은 궤적을 밟는다.  캠페인의
  원자 덤프 간격으로 `dump mesh/stl` 을 걸면 **캠페인 판정 프레임과 같은 step** 에서 벽을 직접 잰다 — 가정한 ε 가 아니라
  그 step 의 실측 오차 (+ 출력 반올림) 가 벽 각의 불확실성이 된다 (`check_contact_validity.load_phase_receipt` · `wall_interval`).
  재개는 B 가 잰다: A 가 N1 에서 `write_restart` 한 체크포인트를 **캠페인 재개 도구와 같은 변환** (`make_mixer_resume.transform`)
  으로 만든 덱이 읽어 끝까지 간다 — A 와 B 의 메시가 같은 step 에서 **꼭짓점까지 같아야** 한다.

무엇 (gen → run.sh → analyze)
  gen      캠페인 덱 → A 덱 (입자 삽입 · 원자 dump · 주기 restart 만 뺌 · 템플릿 · 분포는 남김 — 0 입자 덱의 write_restart 가
           `Atom types must start from 1` 로 죽기 때문 · 09-27 WSL 실측) · B 덱 (transform + 템플릿 재선언) · run.sh · gen.json
           N1 = 회전의 ~60 % (L 런이 재개된 자리) 근처 dump 격자 step 중, 재개 때 위상이 0 으로 돌아간다는 대안과의 차가 드럼 면
           대칭 (360°/면 수) 을 빼고도 ≥ 2 · RESET_GAP_DEG 인 것 (Codex Q2).
  run.sh   실행 **직전** 봉인 (바이너리 · 두 덱 · STL sha256 → seal.json) → A → B → 실행 결과 (exit · 완료 표지 · 덤프 sha256 →
           run_status.json).  덤프 폴더는 매번 지우고 새로 만든다 (옛 시험 파일 혼입 방지 · HBR3-01).
  analyze  기대 step 집합 (A: 첫 덤프 ~ 끝 · B: N1 ~ 끝, dump 격자) 과 **정확히** 같아야 하고 (누락 · 추가 = 실패), 봉인 뒤 덱 · STL ·
           덤프가 안 바뀌었고, A/B 가 정상 완료했고, 배너가 같고, 매 step 의 전체 메시 (드럼 + 두 끝판) 가 원 STL 을 예정각으로 돌린
           것과 **꼭짓점 순서대로** 맞고 (남는 어긋남 ≤ 허용), B = A (꼭짓점까지) 일 때만 통과.  → 영수증 JSON (schema restart_phase_v1).

⚠ 영수증은 **바이너리 + 메시 운동 계약**의 성질이다.  소비자가 런 로그 배너 · 운동 서명 · 판정 step 이 실측 step 안인지를 대조한다.
⚠ 개별 런의 체크포인트 상태 (그 런이 실제로 그 위상에서 이어졌는가) 는 이 시험이 아니다 — Codex Q1 의 런별 상태 확인은 따로 한다.

    python3 scripts/mixer_restart_phase_test.py gen --deck dem_scripts/mixer_20260921/runs/LC_s32452843/in.mixer --out ~/phase_v1
    bash ~/phase_v1/run.sh                      # WSL · lmp_serial (LMP=… 로 바꿈) · 0 입자라 분 단위
    python3 scripts/mixer_restart_phase_test.py analyze ~/phase_v1 --out docs/data/mixer_phase_receipt_<날짜>/receipt_v1.json
    python3 scripts/mixer_restart_phase_test.py --selftest
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import itertools
import json
import os
import re
import shutil
import sys

import numpy as np

_SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCR)
from make_mixer_resume import logical_commands, _tokens, transform      # noqa: E402  캠페인 재개와 **같은 변환**
from check_contact_validity import (PHASE_EPS_DEG, RECEIPT_SCHEMA, motion_signature, read_stl, deck_walls,   # noqa: E402
                                    _rot, _planes, mesh_angle)

RESET_GAP_DEG = 1.0          # 재개-리셋 대안과의 최소 간격 (면 대칭을 뺀 뒤) — 등록값
N1_FRAC = 0.6                # 체크포인트 자리 = 회전 run 의 이 비율 근처 (L 런 재개 53–61 %)
DROP_FIX = ('insert/',)      # 삽입만 뺀다.  템플릿 · 분포는 남긴다 (0 입자 덱의 write_restart — 09-27 WSL 실측)
CKPT = 'restart_pt/ckpt.bin'


def _sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def deck_structure(deck_text):
    """캠페인 덱 → dict(run_lens, run_total, rot_start, dump_every, dump_ids)."""
    toks = [_tokens(b) for _, b in logical_commands(deck_text)]
    runs = [int(t[1]) for t in toks if t[:1] == ['run']]
    if len(runs) < 2:
        raise ValueError(f'run 줄이 {len(runs)} 개')
    dumps = [t for t in toks if t[:1] == ['dump'] and len(t) > 4 and t[3] == 'custom']
    if len(dumps) != 1:
        raise ValueError(f'원자 dump (custom) 가 {len(dumps)} 개 — 하나여야 한다')
    return dict(run_lens=runs, run_total=sum(runs), rot_start=sum(runs) - runs[-1], dump_every=int(dumps[0][4]),
                dump_ids={t[1] for t in toks if t[:1] == ['dump']})


def drum_facets(stl_dir, deck_text):
    """드럼 면 수 (축에 수직이 아닌 평면 수)."""
    sp = deck_walls(deck_text)
    f, sc = sp['meshes']['Drum']
    T = read_stl(os.path.join(stl_dir, f)) * sc
    N, _ = _planes(T, T.reshape(-1, 3).mean(0))
    ax = sp['moves']['Drum']['axis']
    return int((np.abs(N @ ax) < 0.99).sum())


def symmetric_gap_deg(n1, rot_start, dt, period, nfacet):
    """연속 가설과 리셋 가설의 각 차 — 드럼 면 대칭 (360°/nfacet) 을 뺀 최소 거리 (Codex Q2)."""
    g = (360.0 * (n1 - rot_start) * dt / period) % 360.0
    fa = 360.0 / nfacet
    m = g % fa
    return float(min(m, fa - m)), float(min(g, 360.0 - g))


def choose_n1(st, dt, period, nfacet, frac=N1_FRAC, span=400):
    """dump 격자 위 · 회전 run 의 frac 근처 · 면 대칭을 뺀 리셋 간격 ≥ 2·RESET_GAP_DEG 인 가장 가까운 step."""
    de, r0, rt = st['dump_every'], st['rot_start'], st['run_total']
    target = r0 + frac * (rt - r0)
    k0 = int(round(target / de))
    for dk in sorted(range(-span, span + 1), key=abs):
        n1 = (k0 + dk) * de
        if not (r0 + de < n1 < rt - de):
            continue
        if symmetric_gap_deg(n1, r0, dt, period, nfacet)[0] >= 2 * RESET_GAP_DEG:
            return n1
    raise ValueError('리셋 대안과 구별되는 N1 을 dump 격자에서 못 찾았다')


def gen_decks(deck_text, n1):
    """캠페인 덱 → (A 덱, B 덱).  A = 입자 삽입 · 원자 dump (+ dump_modify · undump) · 주기 restart · write_restart · shell 을 빼고
    원자 dump 자리에 같은 간격의 `dump mesh/stl`, 마지막 (회전) run 을 N1 에서 쪼개 `write_restart` .  B = transform(A0) + 템플릿 재선언."""
    st = deck_structure(deck_text)
    if not (st['rot_start'] < n1 < st['run_total']):
        raise ValueError(f'N1 {n1} 이 회전 구간 ({st["rot_start"]}, {st["run_total"]}) 밖이다')
    cmds = logical_commands(deck_text)
    toks = [_tokens(b) for _, b in cmds]
    drop_fix, drop_reg = set(), set()
    for t in toks:
        if t[:1] == ['fix'] and len(t) > 3 and any(t[3].startswith(s) for s in DROP_FIX):
            drop_fix.add(t[1])
            if 'region' in t:
                drop_reg.add(t[t.index('region') + 1])
    atom_dumps = {t[1] for t in toks if t[:1] == ['dump'] and len(t) > 4 and t[3] == 'custom'}
    de = st['dump_every']
    a0, tmpl = [], []
    for (_, blk), t in zip(cmds, toks):
        if not t:
            continue
        k = t[0]
        if (k == 'fix' and t[1] in drop_fix) or (k == 'unfix' and t[1] in drop_fix) or (k == 'region' and t[1] in drop_reg):
            continue
        if k in ('dump_modify', 'undump') and len(t) > 1 and t[1] in atom_dumps:
            continue
        if k == 'dump' and t[1] in atom_dumps:
            a0.append(f'dump dmesh all mesh/stl {de} post_mesh/mesh_*.stl')
            continue
        if k in ('restart', 'write_restart', 'shell'):
            continue
        if k == 'fix' and len(t) > 3 and (t[3].startswith('particletemplate/') or t[3].startswith('particledistribution/')):
            tmpl.append(' '.join(t))
        a0.append(' '.join(t))
    runs_at = [i for i, c in enumerate(a0) if c.startswith('run ')]
    last = runs_at[-1]
    a = a0[:last] + [f'run {n1 - st["rot_start"]}', f'write_restart {CKPT}', f'run {st["run_total"] - n1}'] + a0[last + 1:]
    hdr = '# 재개-위상 영수증 v1 덱 {} — scripts/mixer_restart_phase_test.py (캠페인 덱에서 입자 삽입 · 원자 dump 만 뺌 · step 구조 그대로)\n'
    a_text = hdr.format('A (기준 · N1 체크포인트)') + '\n'.join(a) + '\n'
    b_text, info = transform('\n'.join(a0) + '\n', CKPT, n1)
    lines = b_text.split('\n')
    j = next(i for i, l in enumerate(lines) if l.startswith('print') and 'RESUME_STEP' in l)
    b_text = '\n'.join(lines[:j + 1] + ['# 템플릿 · 분포 재선언 — 0 입자 계의 원자 타입 (transform 은 입자 런용이라 뺀다)'] + tmpl + lines[j + 1:])
    return a_text, hdr.format('B (make_mixer_resume.transform 재개)') + b_text, st


RUN_SH = r"""#!/bin/bash
# 재개-위상 영수증 v1 — 실행 직전 봉인 → A (기준 · 체크포인트) → B (read_restart 재개) → 실행 결과.  WSL: bash run.sh  (LMP=경로)
set -u
cd "$(dirname "$0")"
LMP=${LMP:-lmp_serial}
BIN=$(command -v "$LMP") || { echo "⛔ $LMP 없음 — LMP=<실행파일> 로"; exit 1; }
rm -rf A/post_mesh A/restart_pt B/post_mesh B/restart_pt A/log.lmp B/log.lmp seal.json run_status.json
mkdir -p A/post_mesh A/restart_pt B/post_mesh
python3 - "$BIN" <<'PY' || { echo "⛔ 봉인 실패"; exit 1; }
import datetime, hashlib, json, os, platform, sys
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
b = sys.argv[1]
files = {p: h(p) for p in ['A/in.phase_a', 'B/in.phase_b'] + [f'{d}/{n}' for d in ('A', 'B') for n in sorted(os.listdir(d)) if n.lower().endswith('.stl')]}
json.dump(dict(binary_path=os.path.realpath(b), binary_sha256=h(b), files=files, host=platform.node(),
               sealed_at=datetime.datetime.now().astimezone().isoformat()), open('seal.json', 'w'), indent=1)
PY
( cd A && "$BIN" -in in.phase_a > log.lmp 2>&1 ); ra=$?
rb=-1
if [ "$ra" -eq 0 ]; then cp -r A/restart_pt B/; ( cd B && "$BIN" -in in.phase_b > log.lmp 2>&1 ); rb=$?; fi
python3 - "$ra" "$rb" <<'PY'
import hashlib, json, os, sys
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
def st(d, rc):
    lg = os.path.join(d, 'log.lmp'); txt = open(lg, errors='replace').read() if os.path.isfile(lg) else ''
    pm = os.path.join(d, 'post_mesh')
    return dict(exit=rc, complete=bool(rc == 0 and 'Total wall time' in txt),
                dumps={f: h(os.path.join(pm, f)) for f in sorted(os.listdir(pm))} if os.path.isdir(pm) else {})
json.dump(dict(A=st('A', int(sys.argv[1])), B=st('B', int(sys.argv[2]))), open('run_status.json', 'w'), indent=1)
PY
echo "끝 — A exit $ra · B exit $rb.  분석: python3 scripts/mixer_restart_phase_test.py analyze $(pwd) --out <영수증.json>"
"""


def gen(deck_path, out, n1=None):
    text = open(deck_path, encoding='utf-8', errors='replace').read()
    src = os.path.dirname(os.path.abspath(deck_path))
    sp = deck_walls(text)
    st = deck_structure(text)
    nf = drum_facets(src, text)
    mv = sp['moves']['Drum']
    if n1 is None:
        n1 = choose_n1(st, sp['dt'], mv['period'], nf)
    a, b, _ = gen_decks(text, n1)
    for sub, dk, nm in (('A', a, 'in.phase_a'), ('B', b, 'in.phase_b')):
        d = os.path.join(out, sub)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, nm), 'w', encoding='utf-8').write(dk)
        for m in sp['used']:
            shutil.copyfile(os.path.join(src, sp['meshes'][m][0]), os.path.join(d, sp['meshes'][m][0]))
    open(os.path.join(out, 'run.sh'), 'w', encoding='utf-8').write(RUN_SH)
    sym, raw = symmetric_gap_deg(n1, st['rot_start'], sp['dt'], mv['period'], nf)
    json.dump(dict(deck=os.path.abspath(deck_path), deck_sha256=hashlib.sha256(text.encode()).hexdigest(),
                   motion_signature=motion_signature(text, src), n1=n1, run_total=st['run_total'], rot_start=st['rot_start'],
                   dump_every=st['dump_every'], nfacet=nf, reset_gap_deg=raw, symmetric_gap_deg=sym,
                   tool_sha256=_sha(os.path.abspath(__file__))), open(os.path.join(out, 'gen.json'), 'w'), indent=1)
    print(f'→ {out}/A/in.phase_a · B/in.phase_b · run.sh · gen.json   (N1 {n1:,} · 회전 {st["run_total"] - st["rot_start"]:,} step · '
          f'리셋 대안과 {raw:.3f}° (면 대칭 제외 {sym:.3f}°) · 다음: bash {out}/run.sh)')


def _dump_steps(d):
    pm = os.path.join(d, 'post_mesh')
    out = {}
    for f in (os.listdir(pm) if os.path.isdir(pm) else []):
        m = re.fullmatch(r'mesh_(\d+)\.stl', f)
        if m:
            out[int(m.group(1))] = os.path.join(pm, f)
    return out


def _banner(path):
    if not os.path.isfile(path):
        return ''
    with open(path, encoding='utf-8', errors='replace') as fh:
        for k, line in enumerate(fh):
            if line.startswith('LIGGGHTS (Version'):
                return line.strip()
            if k > 200:
                break
    return ''


def _sig_digits(path):
    """덤프의 첫 꼭짓점 좌표 문자열의 유효숫자 수 (출력 반올림 → 각 해상도)."""
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            t = line.split()
            if t[:1] == ['vertex']:
                mant = re.sub(r'[eE].*$', '', t[1].lstrip('+-')).replace('.', '').lstrip('0')
                return max(len(mant), 1)
    return 1


def analyze(d, out=None, binary=None):
    """run.sh 뒤 → 영수증 dict (passed 는 모든 조건이 설 때만 True).  reasons = 실패 사유 목록."""
    reasons = []

    def need(cond, msg):
        if not cond:
            reasons.append(msg)
        return cond
    gp = os.path.join(d, 'gen.json')
    g = json.load(open(gp)) if os.path.isfile(gp) else None
    seal = json.load(open(os.path.join(d, 'seal.json'))) if os.path.isfile(os.path.join(d, 'seal.json')) else None
    rs = json.load(open(os.path.join(d, 'run_status.json'))) if os.path.isfile(os.path.join(d, 'run_status.json')) else None
    need(g is not None, 'gen.json 없음')
    need(seal is not None, 'seal.json 없음 — 실행 직전 봉인이 없다 (run.sh 로 돌리지 않았다)')
    need(rs is not None, 'run_status.json 없음 — 실행 결과 기록이 없다')
    a_deck = open(os.path.join(d, 'A', 'in.phase_a'), encoding='utf-8').read()
    sp = deck_walls(a_deck)
    mv = sp['moves']['Drum']
    dt, period, axis, origin = sp['dt'], mv['period'], mv['axis'], mv['origin']
    rows, A_st, B_st = [], [], []
    err_max, resid_max, ab_max, ang_res = 0.0, 0.0, 0.0, None
    if g is not None and seal is not None and rs is not None:
        for p, h in seal.get('files', {}).items():
            need(os.path.isfile(os.path.join(d, p)) and _sha(os.path.join(d, p)) == h, f'봉인 뒤 바뀐 파일: {p}')
        if binary:
            need(os.path.isfile(binary) and _sha(binary) == seal.get('binary_sha256'), '지목한 바이너리 sha256 ≠ 봉인 값')
        for part in ('A', 'B'):
            s_ = rs.get(part, {})
            need(s_.get('exit') == 0 and s_.get('complete') is True, f'{part} 실행이 정상 완료가 아니다 (exit {s_.get("exit")} · 완료 {s_.get("complete")})')
            for f, h in s_.get('dumps', {}).items():
                pth = os.path.join(d, part, 'post_mesh', f)
                need(os.path.isfile(pth) and _sha(pth) == h, f'{part} 덤프 {f} 가 실행 뒤 바뀌었거나 없다')
        ver = _banner(os.path.join(d, 'A', 'log.lmp'))
        need(ver.startswith('LIGGGHTS') and ver == _banner(os.path.join(d, 'B', 'log.lmp')), 'A/B 로그 배너가 없거나 다르다')
        de, n1, rt, r0 = g['dump_every'], g['n1'], g['run_total'], g['rot_start']
        #  기대 step — A: dump 명령이 선 step 이후의 dump 격자 · B: N1 ~ 끝
        pre = 0
        for c in a_deck.split('\n'):
            if c.startswith('dump dmesh'):
                break
            if c.startswith('run '):
                pre += int(c.split()[1])
        first = -(-pre // de) * de
        expA = list(range(first, rt + 1, de))
        expB = list(range(n1, rt + 1, de))
        hA, hB = _dump_steps(os.path.join(d, 'A')), _dump_steps(os.path.join(d, 'B'))
        for nm, exp, have in (('A', expA, hA), ('B', expB, hB)):
            miss, extra = sorted(set(exp) - set(have)), sorted(set(have) - set(exp))
            need(not miss, f'{nm} 덤프 누락 {len(miss)} 개 (step {miss[:4]}{"…" if len(miss) > 4 else ""})')
            need(not extra, f'{nm} 덤프 기대 밖 {len(extra)} 개 (step {extra[:4]})')
        comps = {m: read_stl(os.path.join(d, 'A', sp['meshes'][m][0])) * sp['meshes'][m][1] for m in sp['used']}
        n_tri = sum(len(v) for v in comps.values())
        scale = float(max(np.abs(v).max() for v in comps.values()))
        tol = max(1e-7, 1e-5 * scale)
        order = None
        if need(bool(hA) and first in hA and first <= r0, 'A 의 회전 전 첫 덤프가 없다 — 원 기하 대조 불가'):
            T0 = read_stl(hA[first])
            for perm in itertools.permutations(sp['used']):
                E0 = np.vstack([comps[m] for m in perm])
                if E0.shape == T0.shape and float(np.abs(E0 - T0).max()) <= tol:
                    order = perm
                    break
            need(order is not None, 'A 첫 덤프가 원 STL (드럼 · 끝판) 과 꼭짓점 순서대로 맞지 않는다 (구성요소 · 순서)')
            ang_res = float(np.degrees(2 * 10.0 ** (1 - _sig_digits(hA[first]))))
        if order is not None:
            k = axis
            Uall = np.vstack([comps[m] for m in order])
            nd = len(comps['Drum'])
            i0 = sum(len(comps[m]) for m in order[:order.index('Drum')])
            for s in expA:
                if s not in hA:
                    continue
                T = read_stl(hA[s])
                if not need(T.shape == Uall.shape and np.all(np.isfinite(T)), f'A step {s}: 삼각형 {len(T)} ≠ {n_tri} 또는 비유한'):
                    continue
                th = mesh_angle(sp, 'Drum', s)
                E = (Uall - origin) @ _rot(k, th).T + origin
                u = E[i0:i0 + nd].reshape(-1, 3) - origin
                v = T[i0:i0 + nd].reshape(-1, 3) - origin
                up, vp = u - np.outer(u @ k, k), v - np.outer(v @ k, k)
                w = np.linalg.norm(up, axis=1) > 0.5 * np.linalg.norm(up, axis=1).max()
                de_ang = float(np.arctan2((np.cross(up[w], vp[w]) @ k).sum(), (up[w] * vp[w]).sum()))
                Ef = (Uall - origin) @ _rot(k, th + de_ang).T + origin
                resid = float(np.abs(Ef - T).max())
                err = abs(np.degrees(de_ang))
                A_st.append(s)
                row = dict(step=s, error_deg=err, resid_m=resid)
                if s in hB:
                    TB = read_stl(hB[s])
                    ab = float(np.abs(TB - T).max()) if TB.shape == T.shape else float('inf')
                    row['ab_m'] = ab
                    ab_max = max(ab_max, ab)
                    B_st.append(s)
                rows.append(row)
                if s > r0:
                    err_max = max(err_max, err)
                resid_max = max(resid_max, resid)
            need(resid_max <= tol, f'메시가 원 STL 의 강체 회전이 아니다 (남는 어긋남 최대 {resid_max:.3g} m > {tol:.3g})')
            need(ab_max <= 1e-12 * scale, f'B (재개) 메시 ≠ A — 꼭짓점 최대 차 {ab_max:.3g} m')
        need(err_max <= PHASE_EPS_DEG, f'예정각 오차 최대 {err_max:.4g}° > 등록 ε {PHASE_EPS_DEG}°')
        sym, raw = symmetric_gap_deg(n1, r0, dt, period, g['nfacet'])
        need(sym >= RESET_GAP_DEG, f'리셋 대안과의 간격 (면 대칭 제외) {sym:.3f}° < {RESET_GAP_DEG}° — 이 N1 으로는 재개 리셋을 못 가린다')
    else:
        ver, sym, raw, n1 = '', None, None, None
    bound = max(err_max, ang_res or 0.0)
    need(bound <= PHASE_EPS_DEG, f'각 경계 {bound:.4g}° (실측 {err_max:.4g} · 출력 해상도 {ang_res}) > 등록 ε {PHASE_EPS_DEG}°')
    rc = dict(schema=RECEIPT_SCHEMA, test='restart_phase', passed=not reasons, reasons=reasons,
              period=float(period), dt=float(dt), axis=[float(x) for x in axis], origin=[float(x) for x in origin],
              rotation_start_step=g['rot_start'] if g else None, run_total=g['run_total'] if g else None,
              n1=n1, dump_every=g['dump_every'] if g else None,
              span_rotation_steps=(g['run_total'] - g['rot_start']) if g else None,
              steps_checked_A=sorted(A_st), steps_checked_B=sorted(B_st),
              angle_error_deg=float(err_max), angle_resolution_deg=ang_res, angle_bound_deg=float(bound),
              reset_alternative_gap_deg=raw, symmetric_gap_deg=sym, nfacet=g['nfacet'] if g else None,
              ab_max_vertex_diff_m=float(ab_max), residual_max_m=float(resid_max),
              rows=rows, liggghts_version=ver,
              binary_sha256=(seal or {}).get('binary_sha256'), seal=seal,
              run_status={p: {k_: v_ for k_, v_ in (rs or {}).get(p, {}).items() if k_ != 'dumps'} for p in ('A', 'B')} if rs else None,
              motion_signature=(g or {}).get('motion_signature'), deck_source=(g or {}).get('deck'),
              deck_source_sha256=(g or {}).get('deck_sha256'), tool_sha256=_sha(os.path.abspath(__file__)),
              date=datetime.date.today().isoformat(),
              note='바이너리 + 메시 운동 계약의 성질 (처방 회전은 입자와 무관 → 같은 step 구조면 캠페인 메시와 같은 궤적).  '
                   '개별 런의 체크포인트 상태 확인이 아니다.  바이너리 · STL · 주기 · dt 가 바뀌면 다시 만든다.')
    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        json.dump(rc, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'→ {out}')
    print(f'재개-위상 영수증 v1: {"통과" if rc["passed"] else "실패"} — A {len(A_st)} step · B {len(B_st)} step · 예정각 오차 최대 {err_max:.3g}° · '
          f'각 경계 {bound:.3g}° (등록 ε {PHASE_EPS_DEG}°) · A↔B {ab_max:.3g} m · 리셋 간격 (면 대칭 제외) {sym}°'
          + ('' if rc['passed'] else '\n   ✗ ' + '\n   ✗ '.join(reasons[:8])))
    return rc


def _selftest():                                                      # noqa: C901
    import tempfile
    import importlib.util
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)
    spec_ = importlib.util.spec_from_file_location('mmd', os.path.join(_SCR, 'make_mixer_deck.py'))
    m = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(m)
    stl_src = os.path.join(_SCR, '..', 'dem_scripts', 'mixer_20260919')
    # ── ①–④ 덱 변환 (생성기의 실제 LC 덱) ─────────────────────────────────────────────────────────
    lc = m.deck(m.plan(8000), rpm=60, revolutions=2, seed=32452843, arm='LC')
    st = deck_structure(lc)
    sp = deck_walls(lc)
    nf = drum_facets(stl_src, lc)
    n1 = choose_n1(st, sp['dt'], sp['moves']['Drum']['period'], nf)
    a, b, _ = gen_decks(lc, n1)
    ta = [_tokens(x) for _, x in logical_commands(a)]
    tb = [_tokens(x) for _, x in logical_commands(b)]
    runs_a = [int(t[1]) for t in ta if t[:1] == ['run']]
    chk(f'① A: step 구조 그대로 (run 합 {sum(runs_a):,} = 캠페인 {st["run_total"]:,}) · 회전 run 을 N1 {n1:,} 에서 쪼개 write_restart 하나 · '
        '삽입 · 원자 dump · 주기 restart 없음 · 템플릿 · 분포 남음 · mesh dump 간격 = 캠페인 원자 dump 간격',
        sum(runs_a) == st['run_total'] and sum(t[:1] == ['write_restart'] for t in ta) == 1
        and not any(t[:1] == ['fix'] and len(t) > 3 and t[3].startswith('insert/') for t in ta)
        and not any(t[:1] == ['dump'] and len(t) > 3 and t[3] == 'custom' for t in ta)
        and not any(t[:1] == ['restart'] for t in ta)
        and any(t[:1] == ['fix'] and len(t) > 3 and t[3].startswith('particletemplate/') for t in ta)
        and any(t[:1] == ['dump'] and t[3] == 'mesh/stl' and int(t[4]) == st['dump_every'] for t in ta))
    fa = [t[1] for t in ta if t[:1] == ['fix'] and not t[3].startswith(('particletemplate', 'particledistribution'))]
    fb = [t[1] for t in tb if t[:1] == ['fix'] and not t[3].startswith(('particletemplate', 'particledistribution'))]
    chk('② B = make_mixer_resume.transform (read_restart · RESUME_STEP · `run <끝> upto`) + 템플릿 재선언 · 운동 fix ID 가 A 와 같다',
        any(t[:1] == ['read_restart'] for t in tb) and any(t[:2] == ['run', str(st['run_total'])] and 'upto' in t for t in tb)
        and any(t[:1] == ['fix'] and len(t) > 3 and t[3].startswith('particletemplate/') for t in tb)
        and fa == fb and {'Drum', 'Front', 'Back', 'mvD', 'mvF', 'mvB'} <= set(fa))
    sym, raw = symmetric_gap_deg(n1, st['rot_start'], sp['dt'], sp['moves']['Drum']['period'], nf)
    chk(f'③ N1 은 dump 격자 위 · 회전의 ~{N1_FRAC:.0%} · 리셋 대안과 {raw:.2f}° (면 {nf} 개 대칭 제외 {sym:.2f}° ≥ {2 * RESET_GAP_DEG}°)',
        n1 % st['dump_every'] == 0 and sym >= 2 * RESET_GAP_DEG and nf == 39)
    with tempfile.TemporaryDirectory() as td:
        for nm in ('Drum.stl', 'Front.stl', 'Back.stl'):
            shutil.copyfile(os.path.join(stl_src, nm), os.path.join(td, nm))
        chk('④ A 덱 · B 덱의 메시 운동 서명 = 캠페인 덱 (STL 내용 · scale · 축 · 주기 · 순서)',
            motion_signature(a, td) == motion_signature(lc, td) == motion_signature(b, td))
    # ── ⑤–⑦ 분석기 (작은 캠페인꼴 덱 · 실제 STL · 합성 덤프) ─────────────────────────────────────────
    small = '\n'.join([
        'atom_style granular', 'region reg block -0.02 0.02 -0.02 0.02 -0.02 0.02 units box', 'create_box 4 reg', 'timestep 1e-6',
        'fix m1 all property/global youngsModulus peratomtype 1e7 1e7 1e7 1e7',
        'fix Drum all mesh/surface file Drum.stl type 4 scale 0.0149277',
        'fix Front all mesh/surface file Front.stl type 4 scale 0.0149277',
        'fix Back all mesh/surface file Back.stl type 4 scale 0.0149277',
        'fix walls all wall/gran model hertz tangential history mesh n_meshes 3 meshes Drum Front Back',
        'fix pt1 all particletemplate/sphere 10487 atom_type 1 density constant 4800 radius constant 0.0009',
        'fix pdd all particledistribution/discrete 32452867 1 pt1 1.0',
        'region ins cylinder x 0.0 0.0 0.005 -0.001 0.001 units box',
        'fix ins all insert/pack seed 32452843 distributiontemplate pdd maxattempt 200 insert_every once region ins particles_in_region 10',
        'shell mkdir post', 'shell mkdir restart',
        'run 1', 'unfix ins',
        'dump dmp all custom 500 post/mix_*.liggghts id type x y z radius',
        'restart 1000 restart/a.bin restart/b.bin',
        'run 1000', 'run 1000',
        'fix mvD all move/mesh mesh Drum rotate origin 0 0 0 axis 1. 0. 0. period 0.012',
        'fix mvF all move/mesh mesh Front rotate origin 0 0 0 axis 1. 0. 0. period 0.012',
        'fix mvB all move/mesh mesh Back rotate origin 0 0 0 axis 1. 0. 0. period 0.012',
        'run 12000', ''])

    def _write_stl(path, T):
        with open(path, 'w') as fh:
            fh.write('solid m\n')
            for tri in T:
                fh.write(' facet normal 0 0 0\n  outer loop\n' + ''.join(f'   vertex {v[0]:.12e} {v[1]:.12e} {v[2]:.12e}\n' for v in tri)
                         + '  endloop\n endfacet\n')
            fh.write('endsolid m\n')

    def _fake_run(td, mode='cont', fix=None):
        """run.sh 흉내 — 봉인 · A/B 덤프 (예정각) · 실행 결과.  mode: cont (재개가 위상을 잇는다) · reset (재개 때 0 으로)."""
        run_ = os.path.join(td, 'camp')
        os.makedirs(run_, exist_ok=True)
        for nm in ('Drum.stl', 'Front.stl', 'Back.stl'):
            shutil.copyfile(os.path.join(stl_src, nm), os.path.join(run_, nm))
        open(os.path.join(run_, 'in.mixer'), 'w').write(small)
        out_ = os.path.join(td, 'phase')
        gen(os.path.join(run_, 'in.mixer'), out_)
        g = json.load(open(os.path.join(out_, 'gen.json')))
        spA = deck_walls(open(os.path.join(out_, 'A', 'in.phase_a')).read())
        U = np.vstack([read_stl(os.path.join(out_, 'A', f'{nm}.stl')) * 0.0149277 for nm in ('Drum', 'Front', 'Back')])
        de, n1_, rt = g['dump_every'], g['n1'], g['run_total']
        first_ = de                                   # dump 명령이 `run 1` 뒤에 서므로 첫 덤프는 다음 격자 step (실제 LIGGGHTS 와 같게)
        for sub, steps in (('A', range(first_, rt + 1, de)), ('B', range(n1_, rt + 1, de))):
            pm = os.path.join(out_, sub, 'post_mesh')
            os.makedirs(pm, exist_ok=True)
            for s in steps:
                th = mesh_angle(spA, 'Drum', s)
                if sub == 'B' and mode == 'reset':
                    th = 2 * np.pi * (s - n1_) * spA['dt'] / spA['moves']['Drum']['period']
                _write_stl(os.path.join(pm, f'mesh_{s}.stl'), U @ _rot(np.array([1.0, 0, 0]), th).T)
        for sub in ('A', 'B'):
            open(os.path.join(out_, sub, 'log.lmp'), 'w').write('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled test)\n…\nTotal wall time: 0:00:01\n')
        binp = os.path.join(td, 'lmp_fake')
        open(binp, 'wb').write(b'fake-binary')
        files = {p: _sha(os.path.join(out_, p)) for p in ['A/in.phase_a', 'B/in.phase_b']
                 + [f'{s_}/{n}' for s_ in ('A', 'B') for n in ('Drum.stl', 'Front.stl', 'Back.stl')]}
        json.dump(dict(binary_path=binp, binary_sha256=_sha(binp), files=files), open(os.path.join(out_, 'seal.json'), 'w'))
        rsd = {sub: dict(exit=0, complete=True, dumps={f: _sha(os.path.join(out_, sub, 'post_mesh', f))
                                                        for f in sorted(os.listdir(os.path.join(out_, sub, 'post_mesh')))}) for sub in ('A', 'B')}
        json.dump(rsd, open(os.path.join(out_, 'run_status.json'), 'w'))
        if fix:
            fix(out_, run_)
        return out_, run_, binp
    with tempfile.TemporaryDirectory() as td:
        out_, run_, binp = _fake_run(td)
        rc = analyze(out_, out=os.path.join(td, 'r.json'), binary=binp)
        chk(f'⑤ 연속 · 완결 · 봉인 일치 → 통과 (A {len(rc["steps_checked_A"])} step · B {len(rc["steps_checked_B"])} step · 오차 {rc["angle_error_deg"]:.1e}° · '
            f'해상도 {rc["angle_resolution_deg"]:.1e}° · 리셋 간격 {rc["symmetric_gap_deg"]:.2f}°)',
            rc['passed'] and rc['schema'] == RECEIPT_SCHEMA and rc['angle_bound_deg'] <= 1e-6 and len(rc['steps_checked_B']) >= 5)
        from check_contact_validity import load_phase_receipt
        spc = deck_walls(small)
        open(os.path.join(run_, 'log.lmp'), 'w').write('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled test)\n')
        need = list(range(2000, 14001, 500))
        r_ok = load_phase_receipt(os.path.join(td, 'r.json'), spc, run_dir=run_, deck_text=small, need_steps=need)
        bad = small.replace('period 0.012', 'period 0.024')
        try:
            load_phase_receipt(os.path.join(td, 'r.json'), deck_walls(bad), run_dir=run_, deck_text=bad, need_steps=need)
            rej = False
        except ValueError:
            rej = True
        chk('⑥ 검사기가 이 영수증을 받는다 (주기 · dt · 축 · 운동 서명 · 배너 · 판정 step ⊂ 실측 step) · 주기가 다른 덱에는 거부',
            r_ok['passed'] is True and rej)
    #  ⑦ HBR3-01 반례 — 필수 대조 · 재개 뒤 표본이 없거나 · 봉인 · 실행 기록이 어긋나면 **실패**
    def _restatus(o):
        """변이를 '실행이 실제로 그렇게 끝난' 경우로 — run_status 의 덤프 목록 · sha 를 지금 파일로 다시 적는다 (위조 검사가 아니라
        누락 · 형상 검사가 걸리게)."""
        rs = json.load(open(os.path.join(o, 'run_status.json')))
        for sub in ('A', 'B'):
            pm = os.path.join(o, sub, 'post_mesh')
            rs[sub]['dumps'] = {f: _sha(os.path.join(pm, f)) for f in sorted(os.listdir(pm))}
        json.dump(rs, open(os.path.join(o, 'run_status.json'), 'w'))

    def _rm_all_A(o, r):
        for f in os.listdir(os.path.join(o, 'A', 'post_mesh')):
            os.remove(os.path.join(o, 'A', 'post_mesh', f))
        _restatus(o)

    def _one_B(o, r):
        fs = sorted(os.listdir(os.path.join(o, 'B', 'post_mesh')))
        for f in fs[1:]:
            os.remove(os.path.join(o, 'B', 'post_mesh', f))
        _rm_all_A(o, r)

    def _only0(o, r):
        f0 = min(os.listdir(os.path.join(o, 'A', 'post_mesh')), key=lambda f: int(re.sub(r'\D', '', f)))
        for sub in ('A', 'B'):
            for f in os.listdir(os.path.join(o, sub, 'post_mesh')):
                if f != f0:
                    os.remove(os.path.join(o, sub, 'post_mesh', f))
        shutil.copyfile(os.path.join(o, 'A', 'post_mesh', f0), os.path.join(o, 'B', 'post_mesh', f0))
        _restatus(o)

    def _extra(o, r):
        f0 = sorted(os.listdir(os.path.join(o, 'A', 'post_mesh')))[0]
        shutil.copyfile(os.path.join(o, 'A', 'post_mesh', f0), os.path.join(o, 'A', 'post_mesh', 'mesh_7301.stl'))

    def _no_seal(o, r):
        os.remove(os.path.join(o, 'seal.json'))

    def _exit1(o, r):
        rs = json.load(open(os.path.join(o, 'run_status.json')))
        rs['B']['exit'] = 1
        json.dump(rs, open(os.path.join(o, 'run_status.json'), 'w'))

    def _incomplete(o, r):
        rs = json.load(open(os.path.join(o, 'run_status.json')))
        rs['A']['complete'] = False
        json.dump(rs, open(os.path.join(o, 'run_status.json'), 'w'))

    def _deck_edit(o, r):
        open(os.path.join(o, 'B', 'in.phase_b'), 'a').write('# 봉인 뒤 수정\n')

    def _dump_edit(o, r):
        f = sorted(os.listdir(os.path.join(o, 'B', 'post_mesh')))[-1]
        open(os.path.join(o, 'B', 'post_mesh', f), 'a').write('\n')

    def _drop_cap(o, r):
        for sub in ('A', 'B'):
            pm = os.path.join(o, sub, 'post_mesh')
            for f in os.listdir(pm):
                T = read_stl(os.path.join(pm, f))[:78]
                _write_stl(os.path.join(pm, f), T)
        _restatus(o)
    cases = [('A 대조 덤프 0 개 (Codex receipt_missing_all_A)', 'cont', _rm_all_A), ('B 한 장 · A 0 개', 'cont', _one_B),
             ('A · B 모두 회전 전 첫 덤프 한 장 (재개 전 정적 형상뿐 · Codex receipt_only_step0)', 'cont', _only0), ('기대 밖 덤프 (step 7301)', 'cont', _extra),
             ('재개 때 위상이 0 으로 (리셋)', 'reset', None), ('봉인 없음', 'cont', _no_seal), ('B exit 1', 'cont', _exit1),
             ('A 완료 표지 없음', 'cont', _incomplete), ('봉인 뒤 덱 수정', 'cont', _deck_edit), ('실행 뒤 덤프 수정', 'cont', _dump_edit),
             ('끝판 빠진 메시 (드럼 78 삼각형만)', 'cont', _drop_cap)]
    for name, mode, f in cases:
        with tempfile.TemporaryDirectory() as td:
            out_, run_, binp = _fake_run(td, mode=mode, fix=f)
            rc = analyze(out_)
            chk(f'⑦ 변이 — {name} → 실패 ({rc["reasons"][:1]})', rc['passed'] is False and rc['reasons'])
    print(f'\nmixer_restart_phase_test selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='재개-위상 영수증 v1 (Codex 3차 HBR3-01 · 02) — 덱 생성 · 분석')
    sub = ap.add_subparsers(dest='cmd')
    g = sub.add_parser('gen', help='캠페인 덱 → 입자 없는 A/B 덱 (step 구조 그대로) + run.sh (봉인) + gen.json')
    g.add_argument('--deck', required=True, help='실행 덱 (dem_scripts/mixer_20260921/runs/<팔>_s<시드>/in.mixer) — STL 은 옆에서 복사')
    g.add_argument('--out', required=True)
    g.add_argument('--n1', type=int, default=None, help='체크포인트 step (기본: 회전 60 %% 근처 dump 격자 · 리셋 구별 가능)')
    an = sub.add_parser('analyze', help='run.sh 뒤: 봉인 · 실행 결과 · 전 step 메시 대조 → 영수증 JSON')
    an.add_argument('dir')
    an.add_argument('--binary', default=None, help='(선택) 지목한 바이너리의 sha256 이 봉인 값과 같은지도 본다')
    an.add_argument('--out', default=None)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.cmd == 'gen':
        gen(a.deck, a.out, a.n1)
    elif a.cmd == 'analyze':
        rc = analyze(a.dir, a.out, a.binary)
        raise SystemExit(0 if rc['passed'] else 1)
    else:
        ap.error('gen | analyze | --selftest')


if __name__ == '__main__':
    main()
