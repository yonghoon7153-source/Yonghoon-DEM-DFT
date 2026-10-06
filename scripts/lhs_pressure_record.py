#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LHS 침대마다 **압밀 목표압 (300 MPa) 에 실제로 닿았는가** — LIGGGHTS 로그의 압밀 루프 기록 (DESC-06 잔여 · 읽기 전용).

왜 (원장 DESC-06 · Codex 배포 v1.1 최종 리뷰 §6 · 판정문 2026-09-13 §7):
  배포 README 는 "300 MPa 압밀 뒤 한 프레임" 이라 적지만 그것을 기계로 확인한 곳이 없었다 (수확 · 배치 · 봉인 grep 0 — CANNOT TELL).
  같은 step 메시의 플래튼 − 고체 윗면 (J12 · J16) 은 판이 침대를 누르고 있다는 것까지이지 목표 도달의 증거가 아니다.
  마지막 프레임의 응력도 증거가 못 된다 — 덱은 목표에 닿으면 판을 고정하고 **이완** (PHASE 4) 하므로 마지막 프레임 응력은 목표보다 낮은 것이 정상이다
  (CLAUDE.md MPM DO-NOT 의 "final_stress < target 을 목표 미달로 읽지 말 것" 과 같은 이유).
  ⇒ 원천 = 덱의 압밀 루프 자신이 남기는 판정 줄:
        label loop_press · run N · variable current_press equal "abs(f_top_mesh[3]) / 면적 / 1e6"
        print "Current Pressure: ${current_press} MPa (Target: ${target_press})"
        if "${current_press} < ${target_press}" then "jump SELF loop_press"
     루프는 current ≥ target 일 때만 빠져나온다 ⇒ **로그의 마지막 판정 줄의 current ≥ target** 이 도달의 기록이다.
     (두 값은 덱 단위 — print 의 "MPa" 글자와 달리 ×1000 이 MPa (press_units) · 둘을 같은 단위로 비교한다.)

판정 (침대마다 · fail-closed — 모르면 통과가 아니다):
  OK            덱에 위 루프 꼴이 있고 · 로그 하나에만 판정 줄이 있고 · 마지막 줄의 Target = 덱 target_press · current 유한 · current ≥ target
  NOT_REACHED   마지막 판정 줄의 current < target (루프 안에서 끝난 로그 — 중단 · 시간 초과)
  REFUSED       덱 없음 · 루프 꼴 모름 · 판정 줄 없음 · 판정 줄 있는 로그가 둘 이상 (어느 것이 끝인지 모른다) · Target ≠ 덱 · current 비유한 ·
                덱 sha ≠ 수확 raw.deck.sha256 (--harvest-dir 를 주면)
  ⚠ 기록은 "루프가 목표에서 빠져나왔다" 까지다 — 그 뒤 이완 단계가 끝까지 돌았는지 · 수확 프레임이 그 뒤인지는 이 기록이 보증하지 않는다
     (lines_after_last 는 정보 · 같은 프레임 관문은 수확 · 배치의 timestep · sha 관문).

산출 TSV (한 행 = 한 침대) → 인계 생성기 `scripts/lhs_design_dataset.py --export-handover … --pressure-record <TSV>` 가 관문으로 읽는다
(OK · reached True · 목표 300 MPa · 덱 sha = 수확 raw.deck 이 아니면 그 인계표를 만들지 않는다).

사용 (원자료가 있는 저자 기계 — WSL):
  python3 scripts/lhs_pressure_record.py --cohort docs/data/area_s2_cohort.tsv --harvest-dir docs/data/lhs_descriptors_cov_1e09f661d \\
      [--root-from <코호트 경로 접두사> --root-to <실제 접두사>] [--log-glob '{case_dir}/log*'] --out <폴더>/lhs_pressure_record.tsv
시험: scripts/test_lhs_pressure_record.py (합성 덱 · 로그 · 생성기 관문 끝-끝).
"""
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import parse_liggghts as PL          # noqa: E402  — 덱 변수 해석 (target_press_sim) · 사본 금지
import press_units as PU             # noqa: E402  — 덱 단위 → MPa (필드 이름이 단위를 정한다 · F-11)

SCHEMA = 'lhs_pressure_record/v1'
COLS = ('case', 'schema', 'status', 'why', 'deck', 'deck_sha256', 'target_press_deck', 'target_mpa', 'log_file', 'log_sha256',
        'n_press_lines', 'last_press_deck', 'last_press_mpa', 'max_press_mpa', 'reached', 'lines_after_last')
STATUSES = ('OK', 'NOT_REACHED', 'REFUSED')
#: 로그의 판정 줄 — print 의 출력 (명령 되풀이 echo 는 'print "…${…}' 로 시작해 이 꼴에 안 걸린다)
PRESS_LINE = re.compile(r'^\s*Current Pressure:\s*(\S+)\s*MPa\s*\(Target:\s*(\S+)\s*\)\s*$')
#: 덱의 루프 꼴 — 판정 줄 print · 탈출 조건 (current < target 이면 다시) · 루프 라벨
DECK_PRINT = re.compile(r'^\s*print\s+"Current Pressure:\s*\$\{current_press\}\s*MPa\s*\(Target:\s*\$\{target_press\}\)"', re.M)
DECK_IF = re.compile(r'^\s*if\s+"\$\{current_press\}\s*<\s*\$\{target_press\}"\s+then\s+"jump\s+SELF\s+loop_press"', re.M)
DECK_LABEL = re.compile(r'^\s*label\s+loop_press\s*$', re.M)
TARGET_REL_TOL = 1e-9


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _num(s):
    try:
        v = float(s)
    except (TypeError, ValueError):
        return None
    return v


def parse_log(text):
    """로그 글 → {'n': 판정 줄 수, 'last': (current, target) 덱 단위 · 'max': 최대 current · 'after': 마지막 판정 줄 뒤 비지 않은 줄 수}."""
    lines = text.splitlines()
    hits = [(i, m) for i, ln in enumerate(lines) for m in [PRESS_LINE.match(ln)] if m]
    if not hits:
        return {'n': 0, 'last': None, 'max': None, 'after': 0}
    cur = [_num(m.group(1)) for _, m in hits]
    i_last, m_last = hits[-1]
    finite = [c for c in cur if c is not None and math.isfinite(c)]
    return {'n': len(hits), 'last': (_num(m_last.group(1)), _num(m_last.group(2))),
            'max': (max(finite) if finite else None), 'after': sum(1 for ln in lines[i_last + 1:] if ln.strip())}


def deck_form(deck_path):
    """덱 → (target_press_sim · 문제 문자열 '' = 루프 꼴 정상)."""
    try:
        text = open(deck_path, encoding='utf-8', errors='replace').read()
    except OSError as e:
        return None, f'덱을 못 읽었다 ({type(e).__name__})'
    miss = [n for n, rx in (('print 판정 줄', DECK_PRINT), ('탈출 조건 if … jump SELF loop_press', DECK_IF), ('label loop_press', DECK_LABEL))
            if not rx.search(text)]
    if miss:
        return None, f'덱에 압밀 루프 꼴이 없다 ({" · ".join(miss)}) — 모르는 덱이라 도달을 판정하지 않는다'
    ip = PL.parse_input_script(deck_path) or {}
    tp = ip.get('target_press_sim')
    if tp is None or not math.isfinite(float(tp)) or float(tp) <= 0:
        return None, f'덱 target_press 를 못 읽었다 ({tp!r})'
    return float(tp), ''


def record(case, deck_path, log_paths, want_deck_sha=None):
    """한 침대의 기록 dict (COLS).  log_paths = 후보 로그 (판정 줄이 있는 것만 쓴다)."""
    r = {k: '' for k in COLS}
    r.update(case=case, schema=SCHEMA, deck=os.path.basename(deck_path or ''))

    def done(status, why=''):
        r.update(status=status, why=why)
        return r
    if not deck_path or not os.path.isfile(deck_path):
        return done('REFUSED', f'덱 없음 ({deck_path})')
    r['deck_sha256'] = sha256_of(deck_path)
    if want_deck_sha is not None and r['deck_sha256'] != want_deck_sha:
        return done('REFUSED', f'덱 sha {r["deck_sha256"][:12]}… ≠ 수확 raw.deck {str(want_deck_sha)[:12]}… — 다른 덱')
    tp, prob = deck_form(deck_path)
    if prob:
        return done('REFUSED', prob)
    r['target_press_deck'] = repr(tp)
    r['target_mpa'] = repr(PU.target_pressure_mpa({'target_press_sim': tp}))
    parsed = []
    for lp in sorted(set(log_paths)):
        try:
            text = open(lp, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        pl = parse_log(text)
        if pl['n']:
            parsed.append((lp, pl))
    if not parsed:
        return done('REFUSED', f'판정 줄 (Current Pressure: …) 이 있는 로그가 없다 (후보 {len(set(log_paths))})')
    if len(parsed) > 1:
        return done('REFUSED', f'판정 줄이 있는 로그가 둘 이상 ({len(parsed)} 개) — 어느 것이 끝인지 모른다 ({[os.path.basename(p) for p, _ in parsed][:4]})')
    lp, pl = parsed[0]
    cur, tgt = pl['last']
    r.update(log_file=os.path.basename(lp), log_sha256=sha256_of(lp), n_press_lines=str(pl['n']), lines_after_last=str(pl['after']),
             last_press_deck=('' if cur is None else repr(cur)))
    if tgt is None or not math.isfinite(tgt) or abs(tgt - tp) > TARGET_REL_TOL * max(abs(tp), 1.0):
        return done('REFUSED', f'로그의 Target {tgt!r} ≠ 덱 target_press {tp!r} — 다른 덱의 로그')
    if cur is None or not math.isfinite(cur):
        return done('REFUSED', f'마지막 판정 줄의 current {cur!r} 가 유한하지 않다 (NaN 이면 덱의 if 가 루프를 빠져나간다 — 도달로 치지 않는다)')
    r['last_press_mpa'] = repr(PU.target_pressure_mpa({'target_press_sim': cur}))
    if pl['max'] is not None:
        r['max_press_mpa'] = repr(PU.target_pressure_mpa({'target_press_sim': pl['max']}))
    reached = cur >= tgt
    r['reached'] = str(bool(reached))
    return done('OK' if reached else 'NOT_REACHED', '' if reached else f'마지막 판정 줄 current {cur!r} < target {tgt!r} — 루프 안에서 끝난 로그')


def _remap(p, a, b):
    return (b + p[len(a):]) if (a and p.startswith(a)) else p


def read_cohort(path):
    with open(path, encoding='utf-8', newline='') as fh:
        rows = [ln for ln in fh if not ln.startswith('#')]
    out = {}
    for r in csv.DictReader(rows, delimiter='\t'):
        c = r.get('case')
        if not c:
            continue
        if c in out:
            raise SystemExit(f'⛔ 코호트에 같은 case 가 둘: {c}')
        out[c] = r
    return out


def harvest_deck_sha(hdir):
    out = {}
    for p in sorted(glob.glob(os.path.join(hdir, '*.json'))):
        if os.path.basename(p).startswith('_'):
            continue
        h = json.load(open(p, encoding='utf-8'))
        out[h.get('case')] = ((h.get('raw') or {}).get('deck') or {}).get('sha256')
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description='LHS 침대마다 압밀 목표압 도달 기록 (LIGGGHTS 로그 압밀 루프 · DESC-06 · 읽기 전용)')
    ap.add_argument('--cohort', required=True, help='봉인 코호트 TSV (case · deck 열 — docs/data/area_s2_cohort.tsv 형식)')
    ap.add_argument('--harvest-dir', default='', help='수확 JSON 폴더 — 덱 sha 를 raw.deck.sha256 과 맞댄다 (주면 그 케이스만 · 없는 케이스는 REFUSED)')
    ap.add_argument('--root-from', default='', help='코호트 경로 접두사 (치환 전)')
    ap.add_argument('--root-to', default='', help='실제 경로 접두사 (치환 뒤)')
    ap.add_argument('--log-glob', default='{case_dir}/log*', help='후보 로그 glob — {case_dir} = 덱이 있는 폴더 · {case} = 케이스 이름')
    ap.add_argument('--case', action='append', default=[], help='이 케이스만 (여러 번)')
    ap.add_argument('--out', required=True, help='산출 TSV')
    a = ap.parse_args(argv)
    coh = read_cohort(a.cohort)
    want = harvest_deck_sha(a.harvest_dir) if a.harvest_dir else None
    cases = sorted(want) if want is not None else sorted(coh)
    if a.case:
        cases = [c for c in cases if c in set(a.case)]
    rows = []
    for c in cases:
        cr = coh.get(c) or {}
        deck = _remap((cr.get('deck') or '').strip(), a.root_from, a.root_to)
        if not cr:
            r = {k: '' for k in COLS}
            r.update(case=c, schema=SCHEMA, status='REFUSED', why='봉인 코호트에 없는 케이스')
        else:
            cdir = os.path.dirname(deck)
            logs = glob.glob(a.log_glob.format(case_dir=cdir, case=c))
            r = record(c, deck, logs, None if want is None else (want.get(c) or 'MISSING'))
        rows.append(r)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, COLS, delimiter='\t', lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)
    cnt = {}
    for r in rows:
        cnt[r['status']] = cnt.get(r['status'], 0) + 1
    print(f'→ {a.out}   {len(rows)} 행 · {cnt}')
    for r in rows:
        if r['status'] != 'OK':
            print(f'  {r["case"]}: {r["status"]} — {r["why"]}')
    return 0 if rows and all(r['status'] == 'OK' for r in rows) else 1


if __name__ == '__main__':
    sys.exit(main())
