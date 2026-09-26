#!/usr/bin/env python3
"""믹서 런 재개 — 죽은 런의 `in.mixer` 를 체크포인트에서 잇는 `in.resume` 으로 바꾼다.

사용:
  python3 scripts/make_mixer_resume.py <run_dir>                 # in.resume · 영수증 · 보존 (띄우지는 않는다)
  python3 scripts/make_mixer_resume.py <run_dir> --smoke-steps 5000   # 시험용 — 체크포인트 + 5000 스텝에서 멈춘다
  python3 scripts/make_mixer_resume.py --selftest

★ 왜 (2026-09-26): WSL 이 죽었다 다시 뜨면서 층상 캠페인 L 10 런이 53–61 % 에서 한꺼번에 끊겼다.
  `run_all.sh` 의 `FORCE=1` 은 **처음부터** 다시 돌려 로그·덤프를 덮는다 (런당 ~3 일 손실).  덱이
  `restart N restart/a.bin restart/b.bin` 로 체크포인트를 번갈아 남기므로 거기서 잇는다.

규칙
  ① 체크포인트 — 로그의 마지막 thermo step L, 간격 N, thermo 간격 T:  ckpt = ⌊L/N⌋·N.
     L < ckpt + T 이면 (체크포인트를 쓰다 죽었을 수 있다) 하나 앞 (ckpt − N) 을 쓴다.
     파일 = a/b 중 mtime 이 최신인 것이 ckpt, 다른 것이 ckpt − N.
     ⚠ 파일 안의 step 은 여기서 읽지 않는다 → 덱이 `read_restart` 직후 `RESUME_STEP` 을 찍고, 스모크가 그것을 대조한다.
  ② 덱 — 원 덱의 줄을 **그대로** 쓰고 다음만 바꾼다:
       `create_box` (+ 그 region) → `read_restart restart/<file>` + `RESUME_STEP` print
       삭제: particletemplate · particledistribution · insert/* 와 그 region · 그 unfix · write_restart · shell mkdir ·
             마지막이 아닌 run
       마지막 run → `run <원 덱 run 합> upto`  (스모크: `run <ckpt + smoke> upto`)
  ③ 보존 — 쓰는 체크포인트를 `restart/resume_from_<ckpt>.bin` 으로 복사하고, ckpt 보다 뒤의 덤프는 지우지 않고
     `post_pre_resume_<ckpt>/` 로 옮긴다 (재개 뒤 같은 step 덤프와 `cmp` 하면 재개가 비트 단위로 같은지 공짜로 안다).
     같은 ckpt 로 두 번 잇게 되면 (재개한 런이 다음 체크포인트 전에 또 죽음) `…_2/` 처럼 새 폴더 — 먼저 옮긴 것을 덮지 않는다.
  ④ 거부 — ckpt 가 회전 시작보다 앞이면 (정착 중 죽음) 이 도구로 잇지 않는다.
"""
import argparse
import json
import math
import os
import re
import shutil
import sys

THERMO_RE = re.compile(r'^ +(\d+) +\d+ ')


def logical_commands(text):
    """덱을 논리 명령 단위로 묶는다 — `&` 로 끝나는 줄은 다음 줄과 한 명령.  반환: [(first_line_idx, [lines])]"""
    lines = text.split('\n')
    out, i = [], 0
    while i < len(lines):
        start, block = i, [lines[i]]
        while block[-1].rstrip().endswith('&') and i + 1 < len(lines):
            i += 1
            block.append(lines[i])
        out.append((start, block))
        i += 1
    return out


def _tokens(block):
    s = ' '.join(l.rstrip().rstrip('&') for l in block)
    s = s.split('#', 1)[0]
    return s.split()


def transform(deck_text, ckpt_file, ckpt_step, smoke_steps=None):
    """원 덱 → 재개 덱.  반환 (text, info)."""
    cmds = logical_commands(deck_text)
    toks = [_tokens(b) for _, b in cmds]
    runs = [k for k, t in enumerate(toks) if t[:1] == ['run']]
    if not runs:
        raise SystemExit('⛔ 덱에 run 이 없다')
    run_total = sum(int(toks[k][1]) for k in runs)
    rot_start = run_total - int(toks[runs[-1]][1])
    cb = [k for k, t in enumerate(toks) if t[:1] == ['create_box']]
    if len(cb) != 1:
        raise SystemExit(f'⛔ create_box 가 {len(cb)} 개 — 덱 형식이 예상과 다르다')
    box_region = toks[cb[0]][2]
    drop_fix_ids, drop_regions = set(), {box_region}
    for t in toks:
        if t[:1] == ['fix'] and len(t) >= 4 and (t[3].startswith('particletemplate/')
                                                 or t[3].startswith('particledistribution/')
                                                 or t[3].startswith('insert/')):
            drop_fix_ids.add(t[1])
            if t[3].startswith('insert/') and 'region' in t:
                drop_regions.add(t[t.index('region') + 1])
    target = (ckpt_step + smoke_steps) if smoke_steps else run_total
    out, dropped = [], []
    header = [f'# ⚠ 재개 덱 — scripts/make_mixer_resume.py 가 in.mixer 에서 만들었다 (손으로 고치지 말 것)',
              f'#   체크포인트 {ckpt_file} · 기대 step {ckpt_step:,} · 목표 step {target:,}'
              + (f' (스모크 {smoke_steps:,} 스텝)' if smoke_steps else f' (원 덱 run 합)'),
              '#   원 덱과 다른 곳: create_box → read_restart · 삽입·정착·write_restart·shell mkdir·앞쪽 run 삭제 · 마지막 run → upto']
    for k, (_, block) in enumerate(cmds):
        t = toks[k]
        kw = t[0] if t else ''
        drop = False
        if kw == 'region' and len(t) > 1 and t[1] in drop_regions:
            drop = True
        elif kw == 'fix' and len(t) > 1 and t[1] in drop_fix_ids:
            drop = True
        elif kw == 'unfix' and len(t) > 1 and t[1] in drop_fix_ids:
            drop = True
        elif kw == 'write_restart':
            drop = True
        elif kw == 'shell' and t[1:2] == ['mkdir']:
            drop = True
        elif kw == 'run' and k != runs[-1]:
            drop = True
        if kw == 'create_box':
            out += [f'read_restart    {ckpt_file}',
                    'variable        resume_step equal step',
                    'print           "RESUME_STEP ${resume_step}"']
            dropped.append(' '.join(t))
            continue
        if kw == 'run' and k == runs[-1]:
            out.append(f'run {target} upto')
            dropped.append(' '.join(t))
            continue
        if drop:
            dropped.append(' '.join(t))
            continue
        out.extend(block)
    text = '\n'.join(header + out)
    if not text.endswith('\n'):
        text += '\n'
    return text, {'run_total': run_total, 'rotation_start': rot_start, 'target': target,
                  'dropped': dropped, 'dropped_fix_ids': sorted(drop_fix_ids),
                  'dropped_regions': sorted(drop_regions)}


def deck_params(deck_text):
    toks = [_tokens(b) for _, b in logical_commands(deck_text)]
    rs = [t for t in toks if t[:1] == ['restart'] and len(t) >= 4]
    th = [t for t in toks if t[:1] == ['thermo'] and len(t) == 2]
    if len(rs) != 1 or len(th) != 1:
        raise SystemExit('⛔ restart N a b / thermo N 줄이 하나씩이 아니다')
    return int(rs[0][1]), rs[0][2], rs[0][3], int(th[0][1])


def choose_checkpoint(last_step, every, thermo_every, rot_start):
    """반환 (ckpt_step, which) — which = 'newest' | 'older'."""
    ckpt = (last_step // every) * every
    which = 'newest'
    if last_step < ckpt + thermo_every:
        ckpt -= every
        which = 'older'
    if ckpt < rot_start:
        raise SystemExit(f'⛔ 체크포인트 step {ckpt:,} 가 회전 시작 {rot_start:,} 보다 앞이다 — 정착 중 죽은 런은 이 도구로 잇지 않는다')
    return ckpt, which


def last_thermo_step(log_text):
    last = None
    for ln in log_text.split('\n'):
        m = THERMO_RE.match(ln)
        if m:
            last = int(m.group(1))
    return last


def prepare(run_dir, smoke_steps=None, move_dumps=True):
    deck_text = open(os.path.join(run_dir, 'in.mixer'), encoding='utf-8').read()
    every, fa, fb, thermo_every = deck_params(deck_text)
    last = last_thermo_step(open(os.path.join(run_dir, 'log.lmp'), encoding='utf-8', errors='replace').read())
    if last is None:
        raise SystemExit(f'⛔ {run_dir}: log.lmp 에 thermo 줄이 없다')
    _, info0 = transform(deck_text, 'X', 0)
    ckpt, which = choose_checkpoint(last, every, thermo_every, info0['rotation_start'])
    pa, pb = (os.path.join(run_dir, f) for f in (fa, fb))
    for p in (pa, pb):
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            raise SystemExit(f'⛔ 체크포인트가 없거나 비었다: {p}')
    newest, older = (fa, fb) if os.path.getmtime(pa) >= os.path.getmtime(pb) else (fb, fa)
    chosen = newest if which == 'newest' else older
    sa, sb = os.path.getsize(pa), os.path.getsize(pb)
    if abs(sa - sb) > 0.2 * max(sa, sb):
        raise SystemExit(f'⛔ a/b 크기가 20 % 넘게 다르다 ({sa:,} vs {sb:,}) — 쓰다 잘린 파일일 수 있다.  손으로 확인할 것')
    text, info = transform(deck_text, chosen, ckpt, smoke_steps)
    receipt = {'run_dir': os.path.abspath(run_dir), 'last_logged_step': last, 'checkpoint_step': ckpt,
               'checkpoint_file': chosen, 'checkpoint_choice': which, 'restart_every': every,
               'thermo_every': thermo_every, **{k: info[k] for k in ('run_total', 'rotation_start', 'target')},
               'smoke_steps': smoke_steps, 'dropped_commands': info['dropped']}
    if not smoke_steps:
        backup = os.path.join(run_dir, os.path.dirname(chosen), f'resume_from_{ckpt}.bin')
        if not os.path.exists(backup):
            shutil.copy2(os.path.join(run_dir, chosen), backup)
        receipt['checkpoint_backup'] = os.path.relpath(backup, run_dir)
        moved = []
        post = os.path.join(run_dir, 'post')
        dst = None
        if move_dumps and os.path.isdir(post):
            dst = os.path.join(run_dir, f'post_pre_resume_{ckpt}')
            n = 2
            while os.path.exists(dst):
                dst = os.path.join(run_dir, f'post_pre_resume_{ckpt}_{n}')
                n += 1
            for f in sorted(os.listdir(post)):
                m = re.match(r'mix_(\d+)\.liggghts$', f)
                if m and int(m.group(1)) > ckpt:
                    os.makedirs(dst, exist_ok=True)
                    shutil.move(os.path.join(post, f), os.path.join(dst, f))
                    moved.append(f)
        receipt['dumps_moved'] = moved
        receipt['dumps_moved_to'] = os.path.relpath(dst, run_dir) if moved else None
    name = 'in.resume' if not smoke_steps else 'in.smoke'
    open(os.path.join(run_dir, name), 'w', encoding='utf-8').write(text)
    rname = 'resume_receipt.json' if not smoke_steps else 'smoke_receipt.json'
    with open(os.path.join(run_dir, rname), 'w', encoding='utf-8') as fh:
        json.dump(receipt, fh, ensure_ascii=False, indent=1)
    return receipt


# ───────────────────────── selftest ─────────────────────────
def selftest():
    import importlib.util
    import tempfile
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location('mmd', os.path.join(here, 'make_mixer_deck.py'))
    mmd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mmd)
    fails = []

    def chk(name, ok):
        print(('  ✓ ' if ok else '  ✗ ') + name)
        if not ok:
            fails.append(name)

    p = mmd.plan(8000)
    decks = {'LA (층상 삽입 둘)': mmd.deck(p, rpm=75, revolutions=8, arm='LA'),
             'E1 (삽입 하나)': mmd.deck(p, rpm=60, revolutions=5, arm='E1')}
    for label, dk in decks.items():
        toks = [_tokens(b) for _, b in logical_commands(dk)]
        runs = [int(t[1]) for t in toks if t[:1] == ['run']]
        rot = sum(runs) - runs[-1]
        out, info = transform(dk, 'restart/a.bin', rot + 400000)
        ot = [_tokens(b) for _, b in logical_commands(out)]
        kws = [t[0] for t in ot if t]
        print(f'── {label} ──')
        chk('read_restart 이 정확히 1 개 · create_box 0 개', kws.count('read_restart') == 1 and 'create_box' not in kws)
        chk('run 이 정확히 1 개이고 `run <원 run 합> upto`',
            [t for t in ot if t[:1] == ['run']] == [['run', str(sum(runs)), 'upto']])
        chk('삽입 · 템플릿 · 분포 fix 가 하나도 없다',
            not any(t[:1] == ['fix'] and len(t) > 3 and re.match(r'(insert|particletemplate|particledistribution)/', t[3])
                    for t in ot))
        chk('unfix · write_restart · shell mkdir 이 없다',
            not any(t[:1] in (['unfix'], ['write_restart']) or t[:2] == ['shell', 'mkdir'] for t in ot))
        chk('삽입 region 과 상자 region 이 없다', not any(t[:1] == ['region'] for t in ot))
        chk('read_restart 이 units 뒤 · 첫 fix 앞',
            kws.index('units') < kws.index('read_restart') < kws.index('fix'))
        chk('RESUME_STEP 을 찍는다 (read_restart 바로 뒤)',
            re.search(r'^read_restart .*\n^variable +resume_step equal step\n^print +"RESUME_STEP \$\{resume_step\}"$',
                      out, re.M) is not None)
        # 보존: 삭제 대상이 아닌 원 명령은 순서 그대로 한 글자도 안 바뀐다
        keep = []
        for (_, b), t in zip(logical_commands(dk), toks):
            kw = t[0] if t else ''
            if kw in ('create_box', 'run', 'unfix', 'write_restart') or t[:2] == ['shell', 'mkdir']:
                continue
            if kw == 'region':
                continue
            if kw == 'fix' and len(t) > 3 and re.match(r'(insert|particletemplate|particledistribution)/', t[3]):
                continue
            keep.append('\n'.join(b))
        body = [('\n'.join(b)) for _, b in logical_commands(out)][3:]
        body = [x for x in body if not x.startswith(('read_restart', 'variable        resume_step', 'print           "RESUME'))
                and not x.startswith('run ')]
        chk('나머지 명령은 순서 · 글자 그대로 (재료 · 접촉 · 메시 · 벽 · 적분 · 덤프 · restart · 회전)', body == keep)
        chk('회전 move/mesh 가 run 앞에 있다',
            max(i for i, t in enumerate(ot) if len(t) > 3 and t[3] == 'move/mesh')
            < max(i for i, t in enumerate(ot) if t[:1] == ['run']))
        chk('`restart N a b` 와 dump 가 남아 있다',
            any(t[:1] == ['restart'] for t in ot) and any(t[:1] == ['dump'] for t in ot))
        o2, i2 = transform(dk, 'restart/b.bin', rot + 400000, smoke_steps=5000)
        chk('스모크: `run <ckpt + 5000> upto`', f'run {rot + 400000 + 5000} upto' in o2)
        chk('& 이어진 줄이 반쯤 남지 않았다 (삭제 명령의 연속줄까지 같이 빠짐)',
            not any(ln.rstrip().endswith('&') and (j + 1 >= len(out.split('\n')) or not out.split('\n')[j + 1].strip())
                    for j, ln in enumerate(out.split('\n'))))

    print('── 체크포인트 선택 ──')
    chk('L 5,805,000 · N 200,000 · T 5,000 → 5,800,000 (최신)', choose_checkpoint(5_805_000, 200_000, 5_000, 385_337) == (5_800_000, 'newest'))
    chk('L 5,800,000 (체크포인트 step 에서 죽음) → 5,600,000 (하나 앞)', choose_checkpoint(5_800_000, 200_000, 5_000, 385_337) == (5_600_000, 'older'))
    try:
        choose_checkpoint(390_000, 200_000, 5_000, 385_337)
        chk('회전 시작 전 체크포인트는 거부', False)
    except SystemExit:
        chk('회전 시작 전 체크포인트는 거부', True)

    print('── 폴더 (보존 · 영수증) ──')
    with tempfile.TemporaryDirectory() as td:
        rd = os.path.join(td, 'LA_s1')
        os.makedirs(os.path.join(rd, 'restart'))
        os.makedirs(os.path.join(rd, 'post'))
        dk = decks['LA (층상 삽입 둘)']
        open(os.path.join(rd, 'in.mixer'), 'w', encoding='utf-8').write(dk)
        every, fa, fb, th = deck_params(dk)
        toks = [_tokens(b) for _, b in logical_commands(dk)]
        runs = [int(t[1]) for t in toks if t[:1] == ['run']]
        rot = sum(runs) - runs[-1]
        c = ((rot // every) + 3) * every
        with open(os.path.join(rd, 'log.lmp'), 'w') as fh:
            for s in range(c - 2 * th, c + 2 * th, th):
                fh.write(f'{s:>9d}   100000  1.0e-06  1.0e-07  2.7e-05\n')
        for f, age in ((fa, 100), (fb, 200)):
            pth = os.path.join(rd, f)
            open(pth, 'wb').write(b'x' * 1000)
            os.utime(pth, (1e9 + (1000 - age), 1e9 + (1000 - age)))
        for s in (c - 45333, c, c + 1000, c + 2000):
            open(os.path.join(rd, 'post', f'mix_{s}.liggghts'), 'w').write('x')
        r = prepare(rd)
        chk('최신 파일 (a) 을 고른다', r['checkpoint_file'] == fa and r['checkpoint_step'] == c)
        chk('사용 체크포인트를 복사 보존', os.path.exists(os.path.join(rd, 'restart', f'resume_from_{c}.bin')))
        chk('ckpt 보다 뒤 덤프만 post_pre_resume_<ckpt>/ 로 옮긴다 (지우지 않는다)',
            sorted(os.listdir(os.path.join(rd, f'post_pre_resume_{c}'))) == sorted([f'mix_{c + 1000}.liggghts', f'mix_{c + 2000}.liggghts'])
            and sorted(os.listdir(os.path.join(rd, 'post'))) == sorted([f'mix_{c - 45333}.liggghts', f'mix_{c}.liggghts']))
        chk('in.resume · resume_receipt.json 이 생긴다',
            os.path.exists(os.path.join(rd, 'in.resume')) and os.path.exists(os.path.join(rd, 'resume_receipt.json')))
        # 같은 ckpt 로 두 번째 재개 (다음 체크포인트 전에 또 죽음) — 먼저 옮긴 덤프를 덮지 않는다
        open(os.path.join(rd, 'post', f'mix_{c + 1000}.liggghts'), 'w').write('second')
        r2 = prepare(rd)
        chk('두 번째 재개는 새 폴더 (…_2) — 먼저 옮긴 덤프를 안 덮는다',
            r2['dumps_moved_to'] == f'post_pre_resume_{c}_2'
            and open(os.path.join(rd, f'post_pre_resume_{c}', f'mix_{c + 1000}.liggghts')).read() == 'x')
        # 변이: a 가 b 보다 훨씬 작다 (쓰다 잘림) → 거부
        open(os.path.join(rd, fa), 'wb').write(b'x' * 10)
        try:
            prepare(rd)
            chk('변이: 크기가 크게 다른 a/b 는 거부', False)
        except SystemExit:
            chk('변이: 크기가 크게 다른 a/b 는 거부', True)

    print(f'\n{"✓ 전부 통과" if not fails else "✗ 실패 " + str(len(fails))}')
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description='믹서 런 재개 덱 (in.resume) 생성 — 띄우지는 않는다')
    ap.add_argument('run_dir', nargs='?')
    ap.add_argument('--smoke-steps', type=int, default=None, help='시험: 체크포인트 + N 스텝에서 멈추는 in.smoke')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.run_dir:
        ap.error('run_dir 이 필요하다')
    r = prepare(a.run_dir, smoke_steps=a.smoke_steps)
    print(f"✓ {os.path.basename(os.path.abspath(a.run_dir))}  로그 마지막 {r['last_logged_step']:,} → 체크포인트 "
          f"{r['checkpoint_file']} (step {r['checkpoint_step']:,}, {r['checkpoint_choice']}) → 목표 {r['target']:,}"
          + (f"  · 덤프 {len(r.get('dumps_moved', []))} 개 → {r.get('dumps_moved_to')}" if not a.smoke_steps else ''))


if __name__ == '__main__':
    main()
