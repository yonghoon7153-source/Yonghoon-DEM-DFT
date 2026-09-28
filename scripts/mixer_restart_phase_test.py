#!/usr/bin/env python3
"""mixer_restart_phase_test.py — 재개-위상 영수증 v2 (2026-09-28, Codex 3차 HBR3-01 · 02 · 03 · Q1 · Q2 · Q5 · 4 차 HBR4-01 · 02 · 03).

★ v2 (Codex 4 차) — ① B 에도 좌표 유한성 · 형상 검사 (B 가 전부 NaN 이면 `max(0.0, NaN)` = 0.0 으로 통과했다) · 봉인 목록과 덤프 해시
  목록을 기대 집합과 **정확히** 대조 (빈 목록이 통과했다) · 내보내는 수 전부 유한  ② 운동 시계 (mover 생성·해제 · run 끝 step) 와
  회전 시작 step 을 영수증에 남긴다 (소비자가 판정할 덱 · 발사 봉인과 대조)  ③ 형상 잔차 + 출력 반올림을 **거리** (`pos_bound_m`,
  좌표 최대 → √3) 로 남기고 각 경계는 max 가 아니라 합.

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
  run.sh   실행 **직전** 봉인 (바이너리 · 두 덱 · STL sha256 → seal.json) → A → B → 실행 결과 (exit · 배너 · 마지막 thermo step ·
           로그 sha · 덤프 sha256 → run_status.json — 판정하지 않고 사실만).  덤프 폴더는 매번 지우고 새로 만든다 (옛 시험 파일 혼입 방지 · HBR3-01).
  analyze  기대 step 집합 (A: 첫 덤프 ~ 끝 · B: N1 ~ 끝, dump 격자) 과 **정확히** 같아야 하고 (누락 · 추가 = 실패), 봉인 뒤 덱 · STL ·
           덤프가 안 바뀌었고, A/B 가 정상 완료했고 (exit 0 ∧ (배너 ∨ 로그의 마지막 thermo step = 끝) — 이 빌드는 배너를 안 찍는다 ·
           SELF-56), 배너가 같고, 매 step 의 전체 메시 (드럼 + 두 끝판) 가 원 STL 을 예정각으로 돌린
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
from check_contact_validity import (PHASE_EPS_DEG, RECEIPT_SCHEMA, motion_signature, motion_clock, read_stl,   # noqa: E402
                                    deck_walls, _rot, _planes, mesh_angle)

RESET_GAP_DEG = 1.0          # 재개-리셋 대안과의 최소 간격 (면 대칭을 뺀 뒤) — 등록값
N1_FRAC = 0.6                # 체크포인트 자리 = 회전 run 의 이 비율 근처 (L 런 재개 53–61 %)
DROP_FIX = ('insert/',)      # 삽입만 뺀다.  템플릿 · 분포는 남긴다 (0 입자 덱의 write_restart — 09-27 WSL 실측)
CKPT = 'restart_pt/ckpt.bin'


def _sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


THERMO_RE = re.compile(r'^\s*(\d+)\s+(\d+)(?:\s|$)')     # thermo 줄 (덱 `thermo_style custom step atoms …`) — run.sh 기록 코드와 같은 식


def log_completion(path, run_total):
    """완주 = 로그의 **마지막 thermo step = 봉인 덱의 끝 step** (숫자로만).  배너 `Total wall time` 은 **기록만** 한다.
    ⚠ 배너만 보면 안 된다 (1): 이 빌드 (LIGGGHTS-PUBLIC 3.8.0) 는 09-21 덱에서 마지막 run 을 끝내고 **배너 없이** 끝난다 (09-22 E0 3/3 ·
      09-28 WSL 영수증 A/B 실측 — 둘 다 exit 0) — 배너-전용 판정이 그 영수증을 '미완' 으로 떨어뜨렸다 (원장 SELF-56).
    ⚠ 배너가 숫자를 덮으면 안 된다 (2): 옛 판은 배너가 있으면 끝 step 과 무관하게 완주로 봤다 — 마지막 thermo step 14,000 (봉인 끝
      14,001) + 배너가 통과했다 (Codex 6 차 HBR6-03 · 재현 키 banner_short_tail).  숫자로 확인되는 끝 step 이 봉인 값과 다르면 미완이다.
      배너만 있고 thermo 줄이 없는 다른 로그 형식은 **받지 않는다** — 지원하려면 별도 증거 계약을 먼저 정한다.
    ⚠ `run_all.sh` `done_run` (캠페인 런 완주 표지) 은 아직 배너 ∨ 끝 step 이다 — 영수증 판정과 따로다.
    → dict(complete, basis ∈ {last_step, None}, last_thermo_step, banner, log_sha256)."""
    if not os.path.isfile(path):
        return dict(complete=False, basis=None, last_thermo_step=None, banner=False, log_sha256=None)
    last, banner = None, False
    with open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            banner = banner or 'Total wall time' in line
            m = THERMO_RE.match(line)
            if m:
                last = int(m.group(1))
    basis = 'last_step' if (last is not None and run_total is not None and last == run_total) else None   # HBR6-03 — 배너는 기록만
    return dict(complete=basis is not None, basis=basis, last_thermo_step=last, banner=banner, log_sha256=_sha(path))


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


RESUME_RE = re.compile(r'^RESUME_STEP\s+(\d+)\s*$')   # B 덱 (make_mixer_resume.transform) 의 `print "RESUME_STEP ${resume_step}"` 줄


def deck_steps(a_text, b_text):
    """**봉인된** A/B 덱의 logical commands → 영수증 완주 기준 (2026-09-28, Codex 5 차 HBR5-05).

    옛 analyze 는 끝 step · 덤프 간격 · N1 을 **봉인 밖 gen.json** 에서 읽었다 ⇒ 덱은 그대로 (끝 14,001) 두고 gen.json 끝만 9,500 으로
    줄인 뒤 그 범위의 짧은 로그 · 덤프를 두면 passed=true 였다 (재현 키 gen_end_truncated).  이제 기준은 덱이다:
      end        = A 의 run 합 (= 운동 시계의 end)
      n1         = A 의 `write_restart` 앞 run 합 (B 가 read_restart 하는 체크포인트의 step)
      dump_every = A 의 `dump dmesh … mesh/stl <간격>`
      end_b      = B 의 유일한 `run <끝> upto`
    gen.json 은 이것과 **대조**만 한다.  → dict(end, n1, dump_every, end_b, dump_every_b, read_restart_b)."""
    ta = [_tokens(b) for _, b in logical_commands(a_text)]
    tb = [_tokens(b) for _, b in logical_commands(b_text)]
    cum, n1, n_wr, de_a = 0, None, 0, None
    for t in ta:
        if t[:1] == ['run'] and len(t) > 1:
            cum += int(t[1])
        elif t[:1] == ['write_restart']:
            n_wr += 1
            n1 = cum
        elif t[:2] == ['dump', 'dmesh'] and len(t) > 4:
            de_a = int(t[4])
    runs_b = [t for t in tb if t[:1] == ['run']]
    end_b = int(runs_b[0][1]) if len(runs_b) == 1 and len(runs_b[0]) > 2 and runs_b[0][2] == 'upto' else None
    de_b = next((int(t[4]) for t in tb if t[:2] == ['dump', 'dmesh'] and len(t) > 4), None)
    return dict(end=cum, n1=n1 if n_wr == 1 else None, dump_every=de_a, end_b=end_b, dump_every_b=de_b,
                read_restart_b=sum(t[:1] == ['read_restart'] for t in tb) == 1)


def resume_steps(log_path):
    """B 로그의 `RESUME_STEP <n>` 줄들 (B 덱이 read_restart 직후 찍는다) → 정수 목록."""
    if not os.path.isfile(log_path):
        return []
    with open(log_path, encoding='utf-8', errors='replace') as fh:
        return [int(m.group(1)) for m in (RESUME_RE.match(line) for line in fh) if m]


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
# ibb (MPI 빌드 · 2026-09-28): LMP=lmp_mpi LMP_LAUNCH="mpirun --oversubscribe --bind-to none -np 1" bash run.sh  (sbatch -n 1 안에서 — 짝)
set -u
cd "$(dirname "$0")"
LMP=${LMP:-lmp_serial}
BIN=$(command -v "$LMP") || { echo "⛔ $LMP 없음 — LMP=<실행파일> 로"; exit 1; }
read -r -a PRE <<< "${LMP_LAUNCH:-}"      # (선택) 실행 접두사 — 비우면 옛 동작 (직접 실행) 그대로 · 봉인에 launch_prefix 로 남는다
rm -rf A/post_mesh A/restart_pt B/post_mesh B/restart_pt A/log.lmp B/log.lmp seal.json run_status.json
mkdir -p A/post_mesh A/restart_pt B/post_mesh
python3 - "$BIN" "${LMP_LAUNCH:-}" <<'PY' || { echo "⛔ 봉인 실패"; exit 1; }
import datetime, hashlib, json, os, platform, sys
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
b = sys.argv[1]
files = {p: h(p) for p in ['A/in.phase_a', 'B/in.phase_b'] + [f'{d}/{n}' for d in ('A', 'B') for n in sorted(os.listdir(d)) if n.lower().endswith('.stl')]}
json.dump(dict(binary_path=os.path.realpath(b), binary_sha256=h(b), launch_prefix=sys.argv[2], files=files, host=platform.node(),
               sealed_at=datetime.datetime.now().astimezone().isoformat()), open('seal.json', 'w'), indent=1)
PY
( cd A && ${PRE[@]+"${PRE[@]}"} "$BIN" -in in.phase_a > log.lmp 2>&1 ); ra=$?
rb=-1
if [ "$ra" -eq 0 ]; then cp -r A/restart_pt B/; ( cd B && ${PRE[@]+"${PRE[@]}"} "$BIN" -in in.phase_b > log.lmp 2>&1 ); rb=$?; fi
python3 - "$ra" "$rb" <<'PY'
import hashlib, json, os, re, sys
h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
TH = re.compile(r'^\s*(\d+)\s+(\d+)(?:\s|$)')          # thermo 줄 — analyze 의 THERMO_RE 와 같은 식 (완주 판정은 analyze 가 한다)
def st(d, rc):
    lg = os.path.join(d, 'log.lmp'); last, banner = None, False
    if os.path.isfile(lg):
        for line in open(lg, errors='replace'):
            banner = banner or 'Total wall time' in line
            m = TH.match(line)
            if m:
                last = int(m.group(1))
    pm = os.path.join(d, 'post_mesh')
    return dict(exit=rc, banner=banner, last_thermo_step=last, log_sha256=h(lg) if os.path.isfile(lg) else None,
                dumps={f: h(os.path.join(pm, f)) for f in sorted(os.listdir(pm))} if os.path.isdir(pm) else {})
json.dump(dict(A=st('A', int(sys.argv[1])), B=st('B', int(sys.argv[2]))), open('run_status.json', 'w'), indent=1)
PY
echo "끝 — A exit $ra · B exit $rb (완주 판정은 analyze 가 로그로 한다).  분석: python3 scripts/mixer_restart_phase_test.py analyze $(pwd) --out <영수증.json>"
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
    bp = os.path.join(d, 'B', 'in.phase_b')
    b_deck = open(bp, encoding='utf-8').read() if os.path.isfile(bp) else ''
    dk = deck_steps(a_deck, b_deck)                # ★ HBR5-05 — 완주 기준은 봉인된 덱에서 (gen.json 은 대조만)
    sp = deck_walls(a_deck)
    mv = sp['moves']['Drum']
    dt, period, axis, origin = sp['dt'], mv['period'], mv['axis'], mv['origin']
    rows, A_st, B_st, comp = [], [], [], {}
    mclock = motion_clock(a_deck)                  # ★ HBR4-02 — A 는 캠페인 step 구조 그대로 (회전 run 을 N1 에서 쪼갤 뿐) → 같은 시계
    rot_start = mv['start_step']                   # 소비자 (deck_walls) 와 **같은 정의**
    err_max, resid_max, ab_max, ang_res = 0.0, 0.0, 0.0, None
    out_round_m, pos_bound_m, scale = None, None, None
    if g is not None and seal is not None and rs is not None:
        #  ★ HBR4-01 (Codex 4 차) — "있는 항목만" 검사하면 **빈 목록**이 통과한다.  봉인 목록은 기대 집합과 **정확히** 같아야 한다.
        want_seal = ({'A/in.phase_a', 'B/in.phase_b'}
                     | {f'{s_}/{sp["meshes"][m_][0]}' for s_ in ('A', 'B') for m_ in sp['used']})
        got_seal = set(seal.get('files') or {})
        need(got_seal == want_seal,
             f'봉인 파일 목록이 기대와 다르다 — 빠짐 {sorted(want_seal - got_seal)[:4]} · 기대 밖 {sorted(got_seal - want_seal)[:4]} '
             f'(빈 · 부분 목록 거부 · HBR4-01)')
        bsha = seal.get('binary_sha256')
        need(isinstance(bsha, str) and re.fullmatch(r'[0-9a-f]{64}', bsha or ''), '봉인 바이너리 sha256 이 없거나 형식이 아니다')
        for p, h in (seal.get('files') or {}).items():
            need(os.path.isfile(os.path.join(d, p)) and _sha(os.path.join(d, p)) == h, f'봉인 뒤 바뀐 파일: {p}')
        if binary:
            need(os.path.isfile(binary) and _sha(binary) == seal.get('binary_sha256'), '지목한 바이너리 sha256 ≠ 봉인 값')
        #  ★ HBR5-05 (Codex 5 차) — 끝 · N1 · 간격을 **봉인된 덱**으로 재구성하고 세 출처 (A 덱 · B 덱 · 운동 시계) 가 한 값인지,
        #    봉인 밖 gen.json 이 그것과 같은지 본다.  아래 완주 · 기대 덤프 · 재개 step 은 전부 덱 값으로 판정한다.
        mc_end = mclock[-1][1] if mclock and mclock[-1][:1] == ['end'] else None
        dk_ok = need(dk['n1'] is not None and dk['dump_every'] and dk['end_b'] is not None and dk['read_restart_b']
                     and dk['end'] == dk['end_b'] == mc_end and dk['dump_every_b'] == dk['dump_every'],
                     f'봉인 덱에서 완주 기준을 한 값으로 재구성할 수 없다 — A 끝 {dk["end"]} · B `run … upto` {dk["end_b"]} · 운동 시계 끝 {mc_end} · '
                     f'A write_restart step {dk["n1"]} · 간격 A {dk["dump_every"]} / B {dk["dump_every_b"]} · B read_restart 하나 {dk["read_restart_b"]} (HBR5-05)')
        need((g.get('run_total'), g.get('n1'), g.get('dump_every')) == (dk['end'], dk['n1'], dk['dump_every']),
             f'gen.json (봉인 밖) 의 끝 · N1 · 간격 {(g.get("run_total"), g.get("n1"), g.get("dump_every"))} ≠ 봉인 덱 '
             f'{(dk["end"], dk["n1"], dk["dump_every"])} — 짧게 바꾼 기준으로 완주를 판정하지 않는다 (HBR5-05 · gen_end_truncated)')
        #  ★ HBR6-01 (Codex 6 차) — 운동 서명 · 면 수는 **봉인된 A (와 B) 의 덱 · STL** 에서 다시 만든다.  옛 판은 봉인 밖 gen.json 의
        #    서명을 영수증에 복사해, 측정하지 않은 메시 (드럼 149 µm 이동) 의 증서가 나왔다 (재현 키 changed_gen_motion_signature).
        #    gen.json 은 **대조만** 한다.  (위에서 봉인 파일 sha 를 이미 확인했다 — 여기서 읽는 STL 이 실행 직전 그 파일이다.)
        try:
            sig_a = motion_signature(a_deck, os.path.join(d, 'A'))
            sig_b = motion_signature(b_deck, os.path.join(d, 'B'))
        except (OSError, ValueError, IndexError, KeyError) as e:
            sig_a = sig_b = None
            need(False, f'봉인 A/B 덱 · STL 에서 운동 서명을 다시 만들 수 없다 ({type(e).__name__}: {e}) — HBR6-01')
        if sig_a is not None:
            need(sig_a == sig_b, 'B 덱의 메시 운동 계약 (서명: STL · scale · 축 · 주기 · 순서) ≠ A — B 는 A 와 같은 벽을 같은 규칙으로 '
                                 '돌려야 한다 (HBR6-01)')
            need(g.get('motion_signature') == sig_a,
                 f'gen.json (봉인 밖) 의 운동 서명 {str(g.get("motion_signature"))[:12]}… ≠ 봉인 A 에서 다시 만든 서명 {sig_a[:12]}… — '
                 '측정하지 않은 메시의 증서를 내지 않는다 (HBR6-01 · changed_gen_motion_signature)')
        try:
            nf_a = drum_facets(os.path.join(d, 'A'), a_deck)
        except (OSError, ValueError, IndexError, KeyError) as e:
            nf_a = None
            need(False, f'봉인 A 의 드럼 STL 에서 면 수를 다시 셀 수 없다 ({type(e).__name__}: {e}) — HBR6-01')
        need(nf_a is not None and g.get('nfacet') == nf_a,
             f'gen.json 면 수 {g.get("nfacet")} ≠ 봉인 A 드럼 STL 에서 다시 센 {nf_a} (재계산 가능한 기하 메타데이터 · HBR6-01)')
        #  B 의 운동 **시계**: read_restart 뒤에 A 와 같은 운동 fix (id · 메시) 가 서고 끝 step 이 같다 (위치 연속성 자체는 아래 A↔B 꼭짓점 대조)
        clk_b = motion_clock(b_deck)
        mov_a = sorted((e_[1], e_[2]) for e_ in mclock if e_[0] == 'move')
        mov_b = sorted((e_[1], e_[2]) for e_ in clk_b if e_[0] == 'move')
        i_rr = next((i_ for i_, e_ in enumerate(clk_b) if e_[0] == 'read_restart'), None)
        i_mv = next((i_ for i_, e_ in enumerate(clk_b) if e_[0] == 'move'), None)
        need(bool(mov_a) and mov_a == mov_b and clk_b[-1] == mclock[-1] and i_rr is not None and (i_mv is None or i_rr < i_mv),
             f'B 덱의 운동 시계가 A 와 이어지지 않는다 — 운동 fix A {mov_a} / B {mov_b} · 끝 A {mclock[-1]} / B {clk_b[-1]} · '
             f'read_restart 위치 {i_rr} (HBR6-01)')
        rt_d = dk['end'] if dk_ok else None
        for part in ('A', 'B'):
            s_ = rs.get(part, {})
            lc = comp[part] = log_completion(os.path.join(d, part, 'log.lmp'), rt_d)
            need(s_.get('exit') == 0 and lc['complete'],
                 f'{part} 실행이 정상 완료가 아니다 (exit {s_.get("exit")} · 배너 {lc["banner"]} · 마지막 thermo step '
                 f'{lc["last_thermo_step"]} / 봉인 덱 끝 {rt_d})')
            if s_.get('log_sha256') is not None or 'last_thermo_step' in s_:      # 옛 run.sh 기록 (09-28 WSL) 에는 없다 → 로그 판정만
                need(s_.get('log_sha256') == lc['log_sha256'] and s_.get('last_thermo_step') == lc['last_thermo_step'],
                     f'{part} 로그가 실행 결과 기록 뒤 바뀌었다 (sha · 마지막 thermo step 이 기록과 다르다)')
            for f, h in s_.get('dumps', {}).items():
                pth = os.path.join(d, part, 'post_mesh', f)
                need(os.path.isfile(pth) and _sha(pth) == h, f'{part} 덤프 {f} 가 실행 뒤 바뀌었거나 없다')
        #  ★ HBR5-05 — B 가 **이 영수증의 체크포인트** (A 덱의 write_restart step) 에서 재개됐다는 실행 증거 = B 로그의 RESUME_STEP
        #    (B 덱이 read_restart 직후 찍는다 — L 런 재개 로그 실측).  덤프 격자만 보면 다른 체크포인트에서의 재개를 못 가린다.
        rsb = resume_steps(os.path.join(d, 'B', 'log.lmp'))
        need(bool(rsb) and dk['n1'] is not None and all(x == dk['n1'] for x in rsb),
             f'B 로그의 RESUME_STEP {rsb[:3]} ≠ 봉인 A 덱의 write_restart step {dk["n1"]} — B 가 이 영수증의 체크포인트에서 재개됐다는 '
             f'실행 증거가 없다 (HBR5-05)')
        ver = _banner(os.path.join(d, 'A', 'log.lmp'))
        need(ver.startswith('LIGGGHTS') and ver == _banner(os.path.join(d, 'B', 'log.lmp')), 'A/B 로그 배너가 없거나 다르다')
        #  ★ HBR5-05 — 기대 덤프 격자도 **덱 값**으로 (gen.json 이 덱과 다르면 위에서 이미 실패 — 그래도 판정 기준은 덱이다)
        de, n1, rt, r0 = dk['dump_every'] or g['dump_every'], dk['n1'] or g['n1'], dk['end'], g['rot_start']
        need(r0 == rot_start, f'gen.json 회전 시작 {r0} ≠ A 덱의 운동 fix 시작 {rot_start} (두 정의가 갈렸다 · HBR4-02)')
        r0 = rot_start                                 # HBR6-01 — 이 아래 판정 · 내보내는 값은 덱 값 (gen 은 위에서 대조만)
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
            #  ★ HBR4-01 — 실행 결과 기록의 덤프 해시 목록도 **집합으로** 대조 (빈 · 부분 목록 거부)
            want_d = {os.path.basename(v) for v in have.values()}
            got_d = set(((rs.get(nm) or {}).get('dumps')) or {})
            need(bool(want_d) and got_d == want_d,
                 f'{nm} 실행 결과 기록의 덤프 해시 목록이 실제 덤프 집합과 다르다 — 기록 {len(got_d)} 개 · 실제 {len(want_d)} 개 '
                 f'(빠짐 {sorted(want_d - got_d)[:3]} · 기대 밖 {sorted(got_d - want_d)[:3]} · HBR4-01)')
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
            _sig = _sig_digits(hA[first])
            ang_res = float(np.degrees(2 * 10.0 ** (1 - _sig)))
            #  ★ HBR4-03 — 같은 반올림을 **길이**로도 남긴다 (소비자가 부호거리 불확실성에 전파한다)
            out_round_m = float(10.0 ** (1 - _sig) * scale)
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
                    #  ★ HBR4-01 — A 에만 있던 유한성 검사를 B 에도.  없으면 B 가 전부 NaN 이어도 `max(0.0, NaN)` 이 0.0 을
                    #    유지해 `ab_max ≤ 허용치` 를 통과한다 (Codex 4 차 재현 키 nan_B_receipt).
                    okB = need(TB.shape == T.shape and bool(np.all(np.isfinite(TB))),
                               f'B step {s}: 삼각형 {len(TB)} ≠ {n_tri} 또는 비유한 좌표')
                    ab = float(np.abs(TB - T).max()) if okB else float('inf')
                    if not np.isfinite(ab):
                        ab = float('inf')
                    row['ab_m'] = ab
                    ab_max = max(ab_max, ab) if np.isfinite(ab) else float('inf')
                    B_st.append(s)
                rows.append(row)
                if s > r0:
                    err_max = max(err_max, err)
                resid_max = max(resid_max, resid)
            need(resid_max <= tol, f'메시가 원 STL 의 강체 회전이 아니다 (남는 어긋남 최대 {resid_max:.3g} m > {tol:.3g})')
            need(ab_max <= 1e-12 * scale, f'B (재개) 메시 ≠ A — 꼭짓점 최대 차 {ab_max:.3g} m')
            #  ★ HBR4-03 — 생산자가 **허용한** 형상 잔차와 출력 반올림을 소비자가 쓸 수 있게 길이로 남긴다.
            #    resid_max · out_round_m 은 **좌표별** 최대라 유클리드 변위는 최악 √3 배다 (좌표 최대와 거리 노름을 혼동하지 않는다).
            pos_bound_m = float(np.sqrt(3.0) * (resid_max + (out_round_m or 0.0)))
        need(err_max <= PHASE_EPS_DEG, f'예정각 오차 최대 {err_max:.4g}° > 등록 ε {PHASE_EPS_DEG}°')
        sym, raw = (symmetric_gap_deg(n1, r0, dt, period, nf_a) if nf_a else (0.0, 0.0))
        need(sym >= RESET_GAP_DEG, f'리셋 대안과의 간격 (면 대칭 제외) {sym:.3f}° < {RESET_GAP_DEG}° — 이 N1 으로는 재개 리셋을 못 가린다')
    else:
        ver, sym, raw, n1, rsb = '', None, None, None, []
        sig_a, nf_a = None, None
    #  ★ HBR4-03 — 옛 판은 max() 였는데 그것은 오차 **합성**의 상한이 아니다 (두 성분은 같은 방향으로 겹칠 수 있다) → 최악 방향 합.
    bound = err_max + (ang_res or 0.0)
    need(bound <= PHASE_EPS_DEG, f'각 경계 {bound:.4g}° (실측 {err_max:.4g} + 출력 해상도 {ang_res}) > 등록 ε {PHASE_EPS_DEG}°')
    #  ★ HBR4-01 — 영수증이 내보내는 수는 전부 유한해야 한다 (비유한이 지표를 조용히 0 으로 만들던 자리)
    need(all(np.isfinite(x) for x in (err_max, resid_max, ab_max, bound) ) and (pos_bound_m is None or np.isfinite(pos_bound_m)),
         f'영수증 지표에 비유한 값 (오차 {err_max} · 잔차 {resid_max} · A↔B {ab_max} · 경계 {bound} · 위치 {pos_bound_m})')
    rc = dict(schema=RECEIPT_SCHEMA, test='restart_phase', passed=not reasons, reasons=reasons,
              period=float(period), dt=float(dt), axis=[float(x) for x in axis], origin=[float(x) for x in origin],
              rotation_start_step=rot_start, motion_clock=mclock, run_total=dk['end'],
              n1=n1, dump_every=dk['dump_every'],
              span_rotation_steps=(dk['end'] - rot_start) if (dk['end'] is not None and rot_start is not None) else None,
              deck_steps=dk, resume_steps_B=rsb,             # ★ HBR5-05 — 완주 기준의 출처 (봉인 덱) 와 B 로그의 재개 step
              steps_checked_A=sorted(A_st), steps_checked_B=sorted(B_st),
              angle_error_deg=float(err_max), angle_resolution_deg=ang_res, angle_bound_deg=float(bound),
              reset_alternative_gap_deg=raw, symmetric_gap_deg=sym, nfacet=nf_a,
              ab_max_vertex_diff_m=float(ab_max), residual_max_m=float(resid_max),
              pos_bound_m=None if pos_bound_m is None else float(pos_bound_m),
              output_rounding_m=None if out_round_m is None else float(out_round_m),
              rows=rows, liggghts_version=ver,
              binary_sha256=(seal or {}).get('binary_sha256'), seal=seal,
              run_status={p: dict(exit=(rs or {}).get(p, {}).get('exit'), complete=comp[p]['complete'], completion_basis=comp[p]['basis'],
                                  last_thermo_step=comp[p]['last_thermo_step'], banner=comp[p]['banner'], log_sha256=comp[p]['log_sha256'],
                                  dumps_n=len(((rs or {}).get(p) or {}).get('dumps') or {}),
                                  dumps_sha256=hashlib.sha256(json.dumps(((rs or {}).get(p) or {}).get('dumps') or {},
                                                                         sort_keys=True).encode()).hexdigest())
                          for p in ('A', 'B')} if comp else None,
              motion_signature=sig_a, motion_signature_basis='sealed_A_recomputed',      # HBR6-01 — gen.json 복사가 아니다
              motion_signature_gen_json=(g or {}).get('motion_signature'), deck_source=(g or {}).get('deck'),
              deck_source_sha256=(g or {}).get('deck_sha256'), tool_sha256=_sha(os.path.abspath(__file__)),
              date=datetime.date.today().isoformat(),
              note='바이너리 + 메시 운동 계약의 성질 (처방 회전은 입자와 무관 → 같은 step 구조면 캠페인 메시와 같은 궤적).  '
                   '개별 런의 체크포인트 상태 확인이 아니다.  바이너리 · STL · 주기 · dt 가 바뀌면 다시 만든다.')
    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        json.dump(rc, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'→ {out}')
    print(f'재개-위상 영수증 v2: {"통과" if rc["passed"] else "실패"} — A {len(A_st)} step · B {len(B_st)} step · 예정각 오차 최대 {err_max:.3g}° · '
          f'각 경계 {bound:.3g}° (등록 ε {PHASE_EPS_DEG}°) · 위치 경계 {pos_bound_m if pos_bound_m is None else f"{pos_bound_m:.3g} m"} · '
          f'A↔B {ab_max:.3g} m · 리셋 간격 (면 대칭 제외) '
          f'{"—" if sym is None else f"{sym:.3f}"}°'
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
    chk('④b ★ HBR4-02 — A 덱의 운동 **시계** (mover 생성 step · run 끝) = 캠페인 덱 (회전 run 을 N1 에서 쪼개도 시계는 같다)',
        motion_clock(a) == motion_clock(lc) and motion_clock(lc)[-1] == ['end', st['run_total']]
        and all(e_[3] == st['rot_start'] for e_ in motion_clock(lc) if e_[0] == 'move'))
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

    def _status_code():
        """run.sh 의 실행 결과 기록 코드 (두 번째 python heredoc) 그대로 — 셀프테스트가 **실제 run.sh 코드**를 돌린다.
        (09-28 SELF-56: 손으로 만든 가짜 run_status 가 run.sh 의 배너-전용 완주 판정을 한 번도 거치지 않아 결함을 통과시켰다.)"""
        return re.findall(r"<<'PY'[^\n]*\n(.*?)\nPY\n", RUN_SH, re.S)[1]

    def _run_status(o, ra=0, rb=0):
        import subprocess
        subprocess.run([sys.executable, '-c', _status_code(), str(ra), str(rb)], cwd=o, check=True)

    def _write_log(path, lo, end, banner=False, resume=None):
        """이 빌드 (LIGGGHTS-PUBLIC 3.8.0 · 09-21 덱) 의 로그 꼴: 배너 첫 줄 · thermo (step atoms …) · Loop time — `Total wall time` 은
        **없다** (09-22 E0 3/3 · 09-28 WSL 영수증 A/B 실측, 둘 다 exit 0).  banner=True = 배너를 찍는 빌드.
        재개 (B, lo > 0) 로그는 B 덱의 `print "RESUME_STEP ${resume_step}"` 줄을 갖는다 (L 런 재개 로그 실측 — 본 캠페인 prereg §3 2b).
        resume = 찍힌 값 (기본 = lo)."""
        steps = sorted(set(range(lo, end, 500)) | {end})
        with open(path, 'w') as fh:
            fh.write('LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0, compiled test)\n…\n'
                     + (f'RESUME_STEP {lo if resume is None else resume}\n' if lo > 0 else '')
                     + 'Step Atoms KinEng c_rke Volume\n')
            fh.write(''.join(f'{s:10d}        0            0            0 6.4e-05\n' for s in steps))
            fh.write('Loop time of 1.0 on 1 procs for 1000 steps with 0 atoms\n' + ('Total wall time: 0:00:01\n' if banner else ''))

    def _fake_run(td, mode='cont', fix=None, log='real'):
        """run.sh 흉내 — 봉인 · A/B 덤프 (예정각) · 로그 · 실행 결과 (run.sh 의 기록 코드 그대로).
        mode: cont (재개가 위상을 잇는다) · reset (재개 때 0 으로).  log: real (배너 없음 = 이 빌드) · banner (배너 있음)."""
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
        for sub, lo in (('A', 0), ('B', n1_)):
            _write_log(os.path.join(out_, sub, 'log.lmp'), lo, rt, banner=(log == 'banner'))
        binp = os.path.join(td, 'lmp_fake')
        open(binp, 'wb').write(b'fake-binary')
        files = {p: _sha(os.path.join(out_, p)) for p in ['A/in.phase_a', 'B/in.phase_b']
                 + [f'{s_}/{n}' for s_ in ('A', 'B') for n in ('Drum.stl', 'Front.stl', 'Back.stl')]}
        json.dump(dict(binary_path=binp, binary_sha256=_sha(binp), files=files), open(os.path.join(out_, 'seal.json'), 'w'))
        _run_status(out_)
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
        #  판정할 런의 발사 봉인 (launch_highbo.sh 꼴) — 영수증을 만든 바이너리로 띄운 런 (HBR4-02)
        json.dump(dict(schema='mixer_highbo_launch_record/1', run='camp', stage='first', lmp_sha256=_sha(binp),
                       sha256={f_: _sha(os.path.join(run_, f_)) for f_ in ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl')}),
                  open(os.path.join(run_, 'launch_record.json'), 'w'))
        need = list(range(2000, 14001, 500))
        try:
            r_ok = load_phase_receipt(os.path.join(td, 'r.json'), spc, run_dir=run_, deck_text=small, need_steps=need)
        except ValueError as e:
            r_ok = dict(passed=None, err=str(e))
        bad = small.replace('period 0.012', 'period 0.024')
        try:
            load_phase_receipt(os.path.join(td, 'r.json'), deck_walls(bad), run_dir=run_, deck_text=bad, need_steps=need)
            rej = False
        except ValueError:
            rej = True
        chk('⑥ 검사기가 이 영수증을 받는다 (주기 · dt · 축 · 운동 서명 · 운동 시계 · 발사 봉인 · 배너 · 판정 step ⊂ 실측 step · 목록) · '
            '주기가 다른 덱에는 거부', r_ok['passed'] is True and rej)
        chk('⑥c ★ HBR6-01 — 영수증의 운동 서명 = **봉인 A 덱 · STL 에서 다시 만든** 값 (= 캠페인 덱) · 면 수도 A 에서 (39)',
            rc.get('motion_signature') == motion_signature(open(os.path.join(out_, 'A', 'in.phase_a')).read(), os.path.join(out_, 'A'))
            == motion_signature(small, run_) and rc.get('motion_signature_basis') == 'sealed_A_recomputed' and rc.get('nfacet') == 39)
        chk(f'⑥b v2 필드 — 덤프 수 = 실측 step 수 · 위치 경계 유한 ({rc.get("pos_bound_m")} m) · 운동 시계 · 회전 시작 = 덱',
            rc['run_status']['A']['dumps_n'] == len(rc['steps_checked_A']) and rc['run_status']['B']['dumps_n'] == len(rc['steps_checked_B'])
            and rc['pos_bound_m'] is not None and np.isfinite(rc['pos_bound_m']) and rc['pos_bound_m'] > 0
            and rc['motion_clock'] == motion_clock(small) and rc['rotation_start_step'] == spc['moves']['Drum']['start_step'])
    #  ⑦ HBR3-01 반례 — 필수 대조 · 재개 뒤 표본이 없거나 · 봉인 · 실행 기록이 어긋나면 **실패**
    def _restatus(o):
        """변이를 '실행이 실제로 그렇게 끝난' 경우로 — run.sh 의 기록 코드를 지금 파일로 다시 돌린다 (exit 는 그대로 · 위조 검사가
        아니라 누락 · 형상 · 완주 검사가 걸리게)."""
        rs = json.load(open(os.path.join(o, 'run_status.json')))
        _run_status(o, rs['A']['exit'], rs['B']['exit'])

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

    def _short_A(o, r):
        """A 가 끝 step 전에 끊긴 실행 (배너 없음 · 마지막 thermo step < 끝) — exit 0 이어도 미완."""
        g_ = json.load(open(os.path.join(o, 'gen.json')))
        _write_log(os.path.join(o, 'A', 'log.lmp'), 0, g_['run_total'] - 2500)
        _restatus(o)

    def _log_edit(o, r):
        """실행 결과 기록 뒤 로그만 바뀜 (완주 판정은 그대로 서는 편집) — 기록의 로그 sha 가 잡아야 한다."""
        open(os.path.join(o, 'B', 'log.lmp'), 'a').write('# 실행 뒤 수정\n')

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
    #  ── Codex 4 차 HBR4-01 반례 (2026-09-28) ─────────────────────────────────────────────────
    def _nan_B(o, r):
        """B 좌표만 전부 NaN (A 는 정상 · 기대 step · 로그 · 해시 전부 갖춤).  옛 판은 B 에 유한성 검사가 없어
        `max(0.0, NaN)` 이 0.0 을 유지해 `ab_max_vertex_diff_m = 0.0` 으로 **통과**했다 (재현 키 nan_B_receipt)."""
        pm = os.path.join(o, 'B', 'post_mesh')
        for f in sorted(os.listdir(pm)):
            T = read_stl(os.path.join(pm, f))
            _write_stl(os.path.join(pm, f), np.full(T.shape, np.nan))
        _restatus(o)

    def _empty_seal_files(o, r):
        """봉인 목록이 비었다 — 옛 판은 '있는 항목만' 검사해 통과했다 (재현 키 empty_seal_lists_receipt)."""
        s_ = json.load(open(os.path.join(o, 'seal.json')))
        s_['files'] = {}
        json.dump(s_, open(os.path.join(o, 'seal.json'), 'w'))

    def _translate(o, r):
        """회전 뒤 A/B 메시 전부를 축 방향 +80 nm 평행이동 (A · B 는 서로 같다) — 생산자 허용 (1e-7 m) 안이라 통과는 맞지만
        그 잔차를 **거리로** 남겨야 소비자가 쓴다 (Codex 4 차 재현 키 translation_receipt)."""
        for sub in ('A', 'B'):
            pm = os.path.join(o, sub, 'post_mesh')
            for f in sorted(os.listdir(pm)):
                T = read_stl(os.path.join(pm, f))
                _write_stl(os.path.join(pm, f), T + np.array([8e-8, 0.0, 0.0]))
        _restatus(o)

    def _empty_dumps(o, r):
        """실행 결과 기록의 덤프 해시 목록이 비었다 — 같은 부류 (재현 키 empty_seal_lists_receipt)."""
        rs = json.load(open(os.path.join(o, 'run_status.json')))
        for p_ in ('A', 'B'):
            rs[p_]['dumps'] = {}
        json.dump(rs, open(os.path.join(o, 'run_status.json'), 'w'))

    #  ── Codex 5 차 HBR5-05 반례 (2026-09-28) ─────────────────────────────────────────────────
    def _gen_short(o, r):
        """봉인된 A/B 덱은 그대로 (끝 14,001) 인데 **봉인 밖 gen.json** 의 끝만 9,500 · N1 9,000 으로 줄이고, 그 짧은 범위에 맞춘
        덤프 · 로그 (마지막 thermo step 9,500) 를 둔다.  옛 판은 gen.json 의 끝으로 완주 · 기대 덤프를 정해 passed=true (A 19 / B 2 —
        재현 키 gen_end_truncated)."""
        gp = os.path.join(o, 'gen.json')
        g_ = json.load(open(gp))
        rt_s, n1_s, de_ = 9500, 9000, g_['dump_every']
        g_['run_total'], g_['n1'] = rt_s, n1_s
        json.dump(g_, open(gp, 'w'), indent=1)
        pa, pb = os.path.join(o, 'A', 'post_mesh'), os.path.join(o, 'B', 'post_mesh')
        for f in os.listdir(pa):
            if int(re.sub(r'\D', '', f)) > rt_s:
                os.remove(os.path.join(pa, f))
        for f in os.listdir(pb):
            os.remove(os.path.join(pb, f))
        for s in range(n1_s, rt_s + 1, de_):
            shutil.copyfile(os.path.join(pa, f'mesh_{s}.stl'), os.path.join(pb, f'mesh_{s}.stl'))
        _write_log(os.path.join(o, 'A', 'log.lmp'), 0, rt_s)
        _write_log(os.path.join(o, 'B', 'log.lmp'), n1_s, rt_s)
        _restatus(o)

    def _resume_other(o, r):
        """B 가 N1 이 아닌 체크포인트에서 재개됐다 (로그의 RESUME_STEP = N1 + 500) — 덤프 · 끝은 정상.  덤프 격자만 보면 못 가린다."""
        g_ = json.load(open(os.path.join(o, 'gen.json')))
        _write_log(os.path.join(o, 'B', 'log.lmp'), g_['n1'], g_['run_total'], resume=g_['n1'] + 500)
        _restatus(o)

    #  ── Codex 6 차 HBR6-01 · HBR6-03 반례 (2026-09-28 밤 · 비준) ─────────────────────────────────
    def _gen_sig(o, r):
        """측정 A/B · 봉인 · 덤프는 그대로, **봉인 밖 gen.json 의 운동 서명만** 다른 캠페인 (드럼 STL 을 y 로 0.01 옮긴 것) 의 값으로.
        옛 판은 그 서명을 영수증에 **복사**해 passed=true · 소비자 accepted (재현 키 changed_gen_motion_signature)."""
        od = os.path.join(o, '_other_campaign')
        os.makedirs(od, exist_ok=True)
        for nm in ('Front.stl', 'Back.stl'):
            shutil.copyfile(os.path.join(stl_src, nm), os.path.join(od, nm))
        T = read_stl(os.path.join(stl_src, 'Drum.stl'))
        _write_stl(os.path.join(od, 'Drum.stl'), T + np.array([0.0, 0.01, 0.0]))
        gp = os.path.join(o, 'gen.json')
        g_ = json.load(open(gp))
        g_['motion_signature'] = motion_signature(small, od)
        json.dump(g_, open(gp, 'w'), indent=1)

    def _gen_nfacet(o, r):
        """gen.json 의 면 수만 바꿈 (재계산 가능한 기하 메타데이터도 봉인 A 에서 다시 만든다 — HBR6-01 해제 조건)."""
        gp = os.path.join(o, 'gen.json')
        g_ = json.load(open(gp))
        g_['nfacet'] = int(g_['nfacet']) + 1
        json.dump(g_, open(gp, 'w'), indent=1)

    def _b_contract(o, r):
        """B 덱의 회전 주기만 다르게 **봉인까지 다시** (실행 전에 그렇게 만든 B) — A 와 B 의 운동 계약이 같아야 한다 (HBR6-01)."""
        bp_ = os.path.join(o, 'B', 'in.phase_b')
        txt_ = open(bp_).read()                      # 읽고 나서 쓴다 (open(…, 'w') 가 먼저 비운다)
        assert 'period 0.012' in txt_
        open(bp_, 'w').write(txt_.replace('period 0.012', 'period 0.024'))
        s_ = json.load(open(os.path.join(o, 'seal.json')))
        s_['files']['B/in.phase_b'] = _sha(bp_)
        json.dump(s_, open(os.path.join(o, 'seal.json'), 'w'))

    def _banner_tail(o, r):
        """봉인 끝 14,001 · 덤프 격자 그대로 · A/B 로그의 마지막 thermo step 만 14,000 + 완료 배너.  옛 판은 배너가 있으면 끝 step 과
        무관하게 완주로 봐 passed=true · completion_basis=banner (재현 키 banner_short_tail)."""
        g_ = json.load(open(os.path.join(o, 'gen.json')))
        _write_log(os.path.join(o, 'A', 'log.lmp'), 0, g_['run_total'] - 1, banner=True)
        _write_log(os.path.join(o, 'B', 'log.lmp'), g_['n1'], g_['run_total'] - 1, banner=True)
        _restatus(o)

    cases = [('A 대조 덤프 0 개 (Codex receipt_missing_all_A)', 'cont', _rm_all_A), ('B 한 장 · A 0 개', 'cont', _one_B),
             ('A · B 모두 회전 전 첫 덤프 한 장 (재개 전 정적 형상뿐 · Codex receipt_only_step0)', 'cont', _only0), ('기대 밖 덤프 (step 7301)', 'cont', _extra),
             ('재개 때 위상이 0 으로 (리셋)', 'reset', None), ('봉인 없음', 'cont', _no_seal), ('B exit 1', 'cont', _exit1),
             ('A 가 끝 step 전에 끊김 (exit 0 · 배너 없음)', 'cont', _short_A), ('실행 결과 기록 뒤 로그 수정', 'cont', _log_edit),
             ('봉인 뒤 덱 수정', 'cont', _deck_edit), ('실행 뒤 덤프 수정', 'cont', _dump_edit),
             ('끝판 빠진 메시 (드럼 78 삼각형만)', 'cont', _drop_cap),
             ('⑩ HBR4-01 B 좌표 전부 NaN (max(0.0, NaN) = 0.0 으로 통과하던 것)', 'cont', _nan_B),
             ('⑪ HBR4-01 봉인 목록이 빈 객체', 'cont', _empty_seal_files),
             ('⑫ HBR4-01 실행 결과 기록의 덤프 해시 목록이 빈 객체', 'cont', _empty_dumps),
             ('⑮ HBR5-05 gen.json 끝만 짧게 (봉인 덱 끝 14,001 · gen 9,500 · N1 9,000 · 그에 맞춘 짧은 덤프 · 로그)', 'cont', _gen_short),
             ('⑮b HBR5-05 B 로그의 RESUME_STEP ≠ 봉인 A 덱의 write_restart step (다른 체크포인트에서 재개)', 'cont', _resume_other),
             ('⑯ ★ HBR6-01 gen.json 운동 서명만 다른 캠페인 값 (측정 A/B · 봉인 그대로 — changed_gen_motion_signature)', 'cont', _gen_sig),
             ('⑯b HBR6-01 gen.json 면 수만 다름 (재계산 가능한 기하 메타데이터)', 'cont', _gen_nfacet),
             ('⑯c HBR6-01 B 덱의 운동 계약 (주기) ≠ A — 봉인까지 다시 한 B', 'cont', _b_contract),
             ('⑰ ★ HBR6-03 로그 마지막 thermo step 14,000 (봉인 끝 14,001) + 완료 배너 (banner_short_tail)', 'cont', _banner_tail)]
    for name, mode, f in cases:
        with tempfile.TemporaryDirectory() as td:
            out_, run_, binp = _fake_run(td, mode=mode, fix=f)
            rc = analyze(out_)
            chk(f'⑦ 변이 — {name} → 실패 ({rc["reasons"][:1]})', rc['passed'] is False and rc['reasons'])
    #  ⑧ ⑨ SELF-56 — 완주 = exit 0 ∧ (배너 ∨ 마지막 thermo step = 끝).  배너를 찍는 빌드도 통과 · 옛 run.sh 기록 (완료 표지 False,
    #  로그 sha 없음) 으로 끝난 09-28 WSL 실행은 LIGGGHTS 재실행 없이 analyze 만 다시 돌려 판정할 수 있어야 한다.
    with tempfile.TemporaryDirectory() as td:
        out_, run_, binp = _fake_run(td, fix=_translate)
        rc = analyze(out_)
        chk(f'⑬ ★ HBR4-03 — +80 nm 평행이동은 허용 안이라 통과하되 (잔차 {rc["residual_max_m"]:.2e} m) 위치 경계 '
            f'{rc["pos_bound_m"]:.2e} m ≥ √3·잔차 로 남긴다 (소비자가 부호거리에 더한다)',
            rc['passed'] is True and rc['residual_max_m'] >= 7.9e-8 and rc['pos_bound_m'] >= np.sqrt(3.0) * rc['residual_max_m'])
    with tempfile.TemporaryDirectory() as td:
        out_, run_, binp = _fake_run(td, log='banner')
        rc = analyze(out_)
        chk(f'⑧ 배너를 찍는 빌드의 로그도 통과 — 완주 근거는 숫자 끝 step (배너는 기록만 · HBR6-03) '
            f'({rc["run_status"] and rc["run_status"]["A"].get("completion_basis")})',
            rc['passed'] is True and rc['run_status']['A'].get('completion_basis') == 'last_step' and rc['run_status']['A'].get('banner') is True)

    def _old_status(o, r):
        rs = {}
        for sub in ('A', 'B'):
            pm = os.path.join(o, sub, 'post_mesh')
            rs[sub] = dict(exit=0, complete=False, dumps={f: _sha(os.path.join(pm, f)) for f in sorted(os.listdir(pm))})
        json.dump(rs, open(os.path.join(o, 'run_status.json'), 'w'))
    with tempfile.TemporaryDirectory() as td:
        out_, run_, binp = _fake_run(td, fix=_old_status)
        rc = analyze(out_)
        chk(f'⑨ 옛 run.sh 기록 (완료 표지 False · 로그 sha 없음) + 배너 없는 완주 로그 → 통과 (09-28 WSL 실행을 재실행 없이 판정 · '
            f'{rc["reasons"][:1]})', rc['passed'] is True and (rc['run_status'] or {}).get('B', {}).get('last_thermo_step') == rc['run_total'])
    #  ⑭ 2026-09-28 (1저자 결정: LH 를 ibb SLURM 으로) — MPI 빌드 실행 접두사 LMP_LAUNCH.  **생성된 run.sh 를 실제로** 돌린다
    #    (가짜 바이너리 · 가짜 mpirun).  접두사가 A · B 둘 다에 붙고 봉인에 남아야 한다 · 비우면 옛 동작 (WSL) 그대로.
    import subprocess
    with tempfile.TemporaryDirectory() as td:
        run_ = os.path.join(td, 'camp')
        os.makedirs(run_)
        for nm in ('Drum.stl', 'Front.stl', 'Back.stl'):
            shutil.copyfile(os.path.join(stl_src, nm), os.path.join(run_, nm))
        open(os.path.join(run_, 'in.mixer'), 'w').write(small)
        fb = os.path.join(td, 'lmp_mpi_fake')
        open(fb, 'w').write('#!/usr/bin/env bash\necho "LIGGGHTS (fake) $*"\n')
        fm = os.path.join(td, 'mpirun_fake')
        open(fm, 'w').write('#!/usr/bin/env bash\necho "mpirun $*" >> "$MPI_LOG"\n'
                            'while [ $# -gt 0 ]; do case "$1" in -np) shift 2; break;; *) shift;; esac; done\nexec "$@"\n')
        os.chmod(fb, 0o755)
        os.chmod(fm, 0o755)
        res = {}
        for tag, pre in (('mpi', f'{fm} --oversubscribe --bind-to none -np 1'), ('plain', '')):
            o_ = os.path.join(td, f'phase_{tag}')
            gen(os.path.join(run_, 'in.mixer'), o_)
            env_ = dict(os.environ, LMP=fb, MPI_LOG=os.path.join(td, f'mpi_{tag}.log'))
            env_.pop('LMP_LAUNCH', None)
            if pre:
                env_['LMP_LAUNCH'] = pre
            p_ = subprocess.run(['bash', os.path.join(o_, 'run.sh')], env=env_, capture_output=True, text=True)
            sl_ = json.load(open(os.path.join(o_, 'seal.json')))
            lg_ = open(env_['MPI_LOG']).read() if os.path.isfile(env_['MPI_LOG']) else ''
            res[tag] = (p_.returncode, sl_, lg_, open(os.path.join(o_, 'A', 'log.lmp')).read(), open(os.path.join(o_, 'B', 'log.lmp')).read())
        rc_m, sl_m, lg_m, la_m, lb_m = res['mpi']
        chk('⑭ ★ LMP_LAUNCH (ibb: mpirun … -np 1) — A · B 둘 다 접두사로 실행 · 봉인에 launch_prefix · 바이너리는 봉인한 그 파일',
            rc_m == 0 and sl_m.get('launch_prefix') == f'{fm} --oversubscribe --bind-to none -np 1'
            and lg_m.count(f'-np 1 {fb} -in in.phase_') == 2 and 'in.phase_a' in la_m and 'in.phase_b' in lb_m
            and sl_m.get('binary_sha256') == _sha(fb))
        rc_p, sl_p, lg_p, la_p, lb_p = res['plain']
        chk('⑭b (대조) LMP_LAUNCH 없으면 옛 동작 그대로 — 접두사 없이 직접 실행 · 봉인 launch_prefix = ""',
            rc_p == 0 and sl_p.get('launch_prefix') == '' and lg_p == '' and 'in.phase_a' in la_p and 'in.phase_b' in lb_p)
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
