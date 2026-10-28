import os, re, sys
FWD = {'fix', 'pair_style', 'pair_coeff', 'compute', 'neighbor', 'neigh_modify', 'timestep', 'variable'}
GLOB = {'pair_style', 'neighbor', 'neigh_modify', 'timestep'}
SEQ = {'fix', 'unfix', 'run', 'restart', 'write_restart', 'pair_style', 'pair_coeff',
       'neighbor', 'neigh_modify', 'timestep', 'label', 'jump', 'if'}
TMPL = re.compile(r'^(particletemplate/|particledistribution/)')
INS = re.compile(r'^insert/')
MESH = {'mesh/surface/stress', 'mesh/surface'}


def uncomment(s):
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


def deck(path):
    # '&' 이어 붙이기 = 원 줄의 마지막 글자일 때 (주석을 지우기 전 · LIGGGHTS 입력 규칙) → 그 뒤 주석 · 공백 정리
    res, buf = [], ''
    with open(path, encoding='utf-8', errors='replace') as f:
        for raw in f:
            r = raw.rstrip('\n').rstrip()
            if r.endswith('&'):
                buf += r[:-1] + ' '
                continue
            s = ' '.join(uncomment(buf + r).split())
            buf = ''
            if s:
                res.append(s)
    s = ' '.join(uncomment(buf).split())
    if s:
        res.append(s)
    return res


def num(x):
    # awk 의 $2+0 과 같은 규칙: 앞의 ASCII 숫자 부분만 (없으면 0)
    m = re.match(r'[ \t]*[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?', x)
    return float(m.group(0)) if m else 0.0


def long_runs(L, start=0):
    # 시험 덱 자르기와 같은 규칙 (awk: $1=="run" && $2+0>1)
    return [i for i in range(start, len(L)) if L[i].split()[0] == 'run'
            and len(L[i].split()) > 1 and num(L[i].split()[1]) > 1]


# 10-28 (KG50-18 · 19): 실행 순서 · step 을 바꾸는 명령 — 시험 덱 run 합 (--trial-steps) 과 첫 긴 run 대조 (check D) 가 같이 쓴다
FLOWC = {'jump', 'next', 'include'}
STEPC = {'minimize', 'rerun', 'reset_timestep', 'read_restart', 'read_data', 'read_dump', 'clear',
         'partition', 'python', 'temper', 'prd', 'tad', 'neb'}
IFOK = {'print', 'quit'}


def words(s):
    # LIGGGHTS 입력 줄의 낱말 — " · ' 로 시작하면 같은 따옴표까지 한 낱말 (따옴표는 뺀다 · 닫는 따옴표 뒤는 공백이어야) · 못 읽으면 None
    out, i, n = [], 0, len(s)
    while True:
        while i < n and s[i] in ' \t':
            i += 1
        if i >= n:
            return out
        if s[i] in '"\'':
            j = s.find(s[i], i + 1)
            if j < 0 or (j + 1 < n and s[j + 1] not in ' \t'):
                return None
            out.append(s[i + 1:j])
            i = j + 1
        else:
            j = i
            while j < n and s[j] not in ' \t':
                j += 1
            out.append(s[i:j])
            i = j


def if_cmds(w):
    # if 의 then · elif · else 명령 (낱말 목록에서) — if 꼴이 아니면 None
    if len(w) < 4 or w[0] != 'if' or w[2] != 'then':
        return None
    out, i = [], 3
    while i < len(w):
        if w[i] == 'elif':
            i += 2
        elif w[i] == 'else':
            i += 1
        else:
            out.append(w[i])
            i += 1
    return out


def if_ok(w):
    # print · quit 만 든 if = 실행 순서 · step 을 안 바꾼다 (quit 이 돌면 시험이 일찍 끝나 G0 이 거부한다)
    cs = if_cmds(w)
    return cs is not None and all((words(c) or [''])[0] in IFOK for c in cs)


def run_n(w):
    # [run N] · [run N pre yes|no post yes|no] → (N, '') · 그 밖 (변수 · upto · every · start · stop · 모르는 꼬리) → (None, 이유)
    if len(w) < 2:
        return None, 'run 수 없음'
    if not re.match(r'^[0-9]+$', w[1]):
        return None, 'run 수가 숫자가 아님'
    rest = w[2:]
    for k in ('upto', 'every', 'start', 'stop'):
        if k in rest:
            return None, 'run 꼬리 %s' % k
    if len(rest) % 2 or any(a not in ('pre', 'post') or b not in ('yes', 'no') for a, b in zip(rest[0::2], rest[1::2])):
        return None, 'run 꼬리를 못 읽음 (pre · post yes|no 만)'
    return int(w[1]), ''


def ctl(l):
    # 실행 순서 줄 = run · label · jump · next · include · print/quit 말고 다른 명령이 든 if · 못 읽는 줄
    w = words(l)
    if not w:
        return w is None
    return w[0] in ('run', 'label') or w[0] in FLOWC or (w[0] == 'if' and not if_ok(w))


def plain(lst):
    # 실행 순서 줄 목록의 run 이 다 숫자 run (꼬리 pre · post 만) 이고 흐름 줄이 label 뿐이면 '' · 아니면 그 줄과 이유
    for l in lst:
        w = words(l) or ['']
        if w[0] == 'run':
            n, why = run_n(w)
            if n is None:
                return '%s [%s]' % (why, l)
        elif w[0] != 'label':
            return '흐름 명령 [%s]' % l
    return ''


def jump_to(l):
    # [jump SELF X] · 또는 print · quit 과 [jump SELF X] 하나만 든 if → X · 아니면 None
    w = words(l) or ['']
    if w[0] == 'jump':
        return w[2] if len(w) == 3 and w[1] == 'SELF' else None
    cs = if_cmds(w) if w[0] == 'if' else None
    if cs is None:
        return None
    js = []
    for c in cs:
        cw = words(c) or ['']
        if len(cw) == 3 and cw[:2] == ['jump', 'SELF']:
            js.append(cw[2])
        elif cw[0] not in IFOK:
            return None
    return js[0] if len(js) == 1 else None


def fmt(lst):
    return ' '.join('[%s]' % l for l in lst) if lst else '(없음)'


def sched_cmp(ml, R, ir, what, kind, mwhere, probs, notes):
    # 10-28 (KG50-19): 본 덱 실행 순서 줄 ml ↔ 재개 덱 read_restart 뒤 ~ 첫 긴 run 의 실행 순서 줄 — 글자 같아야 (deck() 정리 뒤)
    rs = [i for i, l in enumerate(R) if l.split()[0] == 'read_restart']
    if len(rs) != 1:
        probs.append('재개 덱에 read_restart 가 %d 개 (1 개여야 · %s 대조 못 함 · %s · 10-28 KG50-19)' % (len(rs), what, kind))
        return
    rl = [l for l in R[rs[0] + 1:ir + 1] if ctl(l)]
    if rl != ml:
        probs.append('%s 다름 (%s · 10-28 KG50-19): %s %s ↔ 재개 덱 read_restart 뒤 %s' % (what, kind, mwhere, fmt(ml), fmt(rl)))
    else:
        notes.append('%s 같음 (%s · 10-28 KG50-19): %s %s = 재개 덱 read_restart 뒤' % (what, kind, mwhere, fmt(ml)))


def mesh_file(a, b):
    ta, tb = a.split(), b.split()
    if (len(ta) != len(tb) or len(ta) < 6 or ta[0] != 'fix' or ta[3] not in MESH
            or 'file' not in ta or 'file' not in tb or ta.index('file') != tb.index('file')):
        return None
    i = ta.index('file')
    if i + 1 >= len(ta) or ta[:i + 1] != tb[:i + 1] or ta[i + 2:] != tb[i + 2:]:
        return None
    return tb[i + 1]


def state(L, end):
    fixes, glob = {}, {}
    for l in L[:end]:
        t = l.split()
        if t[0] == 'fix' and len(t) >= 4:
            if TMPL.match(t[3]) or INS.match(t[3]):
                continue
            fixes[t[1]] = l
        elif t[0] == 'unfix' and len(t) >= 2:
            fixes.pop(t[1], None)
        elif t[0] in GLOB:
            glob[t[0]] = l
        elif t[0] == 'pair_coeff':
            glob[' '.join(['pair_coeff'] + t[1:3])] = l
    return fixes, glob


def same_or_mesh(a, b, W, notes, probs, what):
    if a == b:
        return
    nf = mesh_file(a, b) if (a and b) else None
    if nf is not None:
        if os.path.isfile(os.path.join(W, nf)):
            notes.append('판 메시 파일만 다름 (%s): %s' % (what, nf))
        else:
            probs.append('판 메시 파일 %s 가 작업 폴더에 없음 (%s)' % (nf, what))
        return
    if a and b:
        probs.append('%s 다름: 본 덱 [%s] ↔ 재개 덱 [%s]' % (what, a, b))
    elif a:
        probs.append('%s 가 재개 덱에 없음: 본 덱 [%s]' % (what, a))
    else:
        probs.append('%s 는 재개 덱에만 있음: [%s]' % (what, b))


def check(main, res, ckpt, s0, W):
    M, R = deck(main), deck(res)
    probs, notes = [], []
    mset = set(M)
    # A. 재삽입 금지
    for l in R:
        t = l.split()
        if t[0] == 'fix' and len(t) >= 4 and INS.match(t[3]):
            probs.append('재개 덱에 삽입 fix (재삽입): [%s]' % l)
    # B. 재개 덱의 물리 · 변수 줄 = 본 덱 줄 그대로 (판 메시 파일 이름만 예외 · 그 파일이 작업 폴더에 있을 때)
    mfix = {}
    for l in M:
        t = l.split()
        if t[0] == 'fix' and len(t) >= 2:
            mfix.setdefault(t[1], []).append(l)
    for l in R:
        t = l.split()
        if t[0] not in FWD or l in mset:
            continue
        nf = None
        if t[0] == 'fix' and len(t) >= 2:
            for a in mfix.get(t[1], []):
                nf = mesh_file(a, l)
                if nf is not None:
                    break
        if nf is not None and os.path.isfile(os.path.join(W, nf)):
            notes.append('판 메시 파일만 다름: %s' % nf)
        elif nf is not None:
            probs.append('판 메시 파일 %s 가 작업 폴더에 없음' % nf)
        else:
            probs.append('본 덱에 없는 줄: [%s]' % l)
    # F. 재개 덱에서 쓰는 c_ · f_ 이름이 재개 덱에 정의돼 있다 (compute · fix 는 restart 에 안 남는다)
    dc = set(l.split()[1] for l in R if l.split()[0] == 'compute' and len(l.split()) > 1)
    df = set(l.split()[1] for l in R if l.split()[0] == 'fix' and len(l.split()) > 1)
    for l in R:
        for kind, name in re.findall(r'\b([cf])_([A-Za-z0-9_]+)', l):
            if name not in (dc if kind == 'c' else df):
                probs.append('재개 덱이 %s_%s 를 쓰는데 정의가 없음: [%s]' % (kind, name, l))
    # 체크포인트 → 본 덱의 자리 (그 파일을 만드는 restart · write_restart 줄 하나)
    base = os.path.basename(ckpt)
    hits = []
    for i, l in enumerate(M):
        t = l.split()
        if t[0] == 'write_restart' and len(t) >= 2 and os.path.basename(t[1]) == base:
            hits.append(('write', i))
        elif t[0] == 'restart' and len(t) >= 3 and num(t[1]) > 0:
            for p in t[2:4]:
                pat = '^' + re.escape(os.path.basename(p)).replace(r'\*', '[0-9]+') + '$'
                if re.match(pat, base):
                    hits.append(('restart', i))
                    break
    if len(hits) != 1:
        probs.append('체크포인트 %s 를 만든 restart · write_restart 줄이 본 덱에 %d 개 (1 개여야 · 손으로 확인)'
                     % (base, len(hits)))
        return probs, notes
    kind, ia = hits[0]
    mr, rr = long_runs(M, ia + 1), long_runs(R)
    if not mr or not rr:
        probs.append('긴 run 을 못 찾음 (본 덱 %d · 재개 덱 %d)' % (len(mr), len(rr)))
        return probs, notes
    im, ir = mr[0], rr[0]
    # C. 재개 지점의 상태 (살아 있는 fix · 쌍 · 이웃 · timestep) — 템플릿 · 분포 · 삽입 fix 는 뺀다
    fm, gm = state(M, im)
    fr, gr = state(R, ir)
    for k in sorted(set(fm) | set(fr)):
        same_or_mesh(fm.get(k), fr.get(k), W, notes, probs, '재개 지점 fix ' + k)
    for k in sorted(set(gm) | set(gr)):
        same_or_mesh(gm.get(k), gr.get(k), W, notes, probs, '재개 지점 ' + k)
    # D. 남은 step — restart 명령이 만든 체크포인트 · 그 run 앞에 반복 · 변수 run 이 없을 때
    if kind == 'restart':
        step, known = 0, True
        for l in M[:im + 1]:
            t = l.split()
            if t[0] in ('label', 'jump'):
                known = False
            elif t[0] == 'reset_timestep' and len(t) > 1:
                step = int(num(t[1]))
            elif t[0] == 'run' and len(t) > 1:
                if not re.match(r'^[0-9]+$', t[1]):
                    known = False
                elif 'upto' in t[2:]:
                    step = int(t[1])
                else:
                    step += int(t[1])
            elif ctl(l) or t[0] in STEPC:
                known = False  # 10-28 (KG50-19): include · next · print/quit 말고 다른 명령이 든 if · step 을 바꾸는 명령 = 남은 step 을 못 센다
        if known:
            # 10-28 (KG50-18): 체크포인트 = 본 덱 그 run 도중 → 재개 덱 첫 긴 run 앞에 run (run 0 말고) 이 없어야
            #   (G0 이 시험 덱 run 합을 보면 그 run 으로 생긴 어긋남을 예전 G0 (마지막 run 만) 처럼 우연히 막지 못한다)
            pre = [l for l in R[:ir] if l.split()[0] == 'run' and run_n(words(l) or [''])[0] != 0]
            if pre:
                probs.append('재개 덱 첫 긴 run 앞에 run 이 있음 (restart 체크포인트 = 본 덱 그 run 도중 · 10-28 KG50-18): %s' % fmt(pre))
            t = R[ir].split()
            if not re.match(r'^[0-9]+$', t[1]):
                probs.append('재개 덱 첫 긴 run 이 숫자가 아님: [%s]' % R[ir])
            else:
                end = int(t[1]) if 'upto' in t[2:] else s0 + int(t[1])
                if end != step:
                    probs.append('남은 step 다름: 재개 끝 %d ↔ 본 덱 그 run 끝 %d ([%s])' % (end, step, R[ir]))
                else:
                    notes.append('남은 step 같음: 끝 %d' % end)
        else:
            # 10-28 (KG50-19): 남은 step 을 못 센다 (그 run 앞에 반복 · 흐름 · 변수 run) — 체크포인트 뒤 루프 (label … 첫 긴 run … 그 label 로
            # 돌아가는 jump) 안이면 루프 머리 label 부터 첫 긴 run 까지를 재개 덱과 대조 · 아니면 정할 수 없음 = 거부 (예전 = 확인 생략 · 통과)
            labs = [i for i in range(ia + 1, im) if M[i].split()[0] == 'label']
            ml = [l for l in M[labs[-1]:im + 1] if ctl(l)] if labs else []
            lw = (words(M[labs[-1]]) or []) if labs else []
            back = [l for l in M[im + 1:] if ctl(l) and l.split()[0] != 'run']
            # 루프 머리 뒤 (label ~ 첫 긴 run) · 체크포인트 줄과 루프 머리 사이 = 숫자 run · label 만 (변수 run · 흐름 줄이면 체크포인트 자리를 못 정한다)
            why = ''
            if labs:
                b1, b2 = plain(ml), plain([l for l in M[ia + 1:labs[-1]] if ctl(l)])
                why = ('루프 머리 뒤 ' + b1) if b1 else ('체크포인트 줄과 루프 머리 사이 ' + b2) if b2 else ''
            if not labs:
                probs.append('남은 step 을 정할 수 없음 (그 run 앞에 반복 · 흐름 · 변수 run · 체크포인트 뒤 루프 머리 label 없음 · 10-28 KG50-19) — 손으로 확인')
            elif len(lw) != 2 or why or not back or jump_to(back[0]) != lw[1]:
                probs.append('루프 몸 run 을 정할 수 없음 (반복 안 restart 체크포인트 · 10-28 KG50-19): 본 덱 %s 뒤 첫 흐름 줄 %s '
                             '(그 label 로 돌아가는 jump 여야)%s — 손으로 확인'
                             % (fmt(ml), '[%s]' % back[0] if back else '없음', ' · ' + why if why else ''))
            else:
                sched_cmp(ml, R, ir, '루프 몸 run', '반복 안 restart 체크포인트', '본 덱', probs, notes)
    else:
        # 10-28 (KG50-19): write_restart 체크포인트 = 그 뒤 run 을 처음부터 다시 — 본 덱 그 줄 뒤 첫 긴 run 까지의 실행 순서 줄 (run · label)
        # = 재개 덱 read_restart 뒤 첫 긴 run 까지 (글자 같아야) · run 수가 변수 · 흐름 줄이면 정할 수 없음 = 거부 (예전 = 해당 없음 · 통과)
        ml = [l for l in M[ia + 1:im + 1] if ctl(l)]
        bad = plain(ml)
        if bad:
            probs.append('첫 긴 run 길이를 정할 수 없음 (write_restart 체크포인트 · 10-28 KG50-19): 본 덱 그 뒤 %s — 손으로 확인' % bad)
        else:
            sched_cmp(ml, R, ir, '첫 긴 run', 'write_restart 체크포인트', '본 덱 그 뒤', probs, notes)
    # E. 재개 지점 뒤 순서 (fix · unfix · run · restart · if …) = 본 덱 그대로
    tm = [l for l in M[im + 1:] if l.split()[0] in SEQ]
    tr = [l for l in R[ir + 1:] if l.split()[0] in SEQ]
    if len(tm) != len(tr):
        probs.append('재개 지점 뒤 순서 줄 수 다름: 본 덱 %d ↔ 재개 덱 %d' % (len(tm), len(tr)))
    for a, b in zip(tm, tr):
        if a != b:
            same_or_mesh(a, b, W, notes, probs, '재개 지점 뒤 줄')
    return probs, notes


def trial_steps(path):
    # 10-28 (KG50-18): 시험 덱 (재개 덱을 첫 긴 run 에서 자른 것) 의 read_restart 뒤 모든 run 합 = 시험이 갈 step 수 (G0 기대 끝 = S0 + 합).
    # 통과 = 'N 개수 [run …] [run …]' 한 줄 · 0.  못 정하면 이유 한 줄 · 1 — read_restart ≠ 1 개 · 따옴표 · 명령 이름에 변수 · jump · next ·
    # include · step 을 바꾸는 명령 · print/quit 말고 다른 명령이 든 if · read_restart 앞 run · run 수 · 꼬리 · 마지막 명령이 run 아님.
    # label 은 혼자서는 아무것도 안 한다 (jump · next 가 있으면 그쪽에서 거부).
    L = deck(path)
    rs = [i for i, l in enumerate(L) if l.split()[0] == 'read_restart']
    if len(rs) != 1:
        print('시험 덱에 read_restart 가 %d 개 (1 개여야)' % len(rs))
        return 1
    runs, tot = [], 0
    for i, l in enumerate(L):
        w = words(l)
        if not w:
            print('따옴표를 못 읽음: [%s]' % l)
            return 1
        if '$' in w[0]:
            print('명령 이름에 변수: [%s]' % l)
            return 1
        if w[0] in FLOWC:
            print('흐름 명령 (jump · next · include): [%s]' % l)
            return 1
        if w[0] in STEPC and i != rs[0]:
            print('step 을 바꾸는 명령: [%s]' % l)
            return 1
        if w[0] == 'if' and not if_ok(w):
            print('print · quit 말고 다른 명령이 든 if: [%s]' % l)
            return 1
        if w[0] == 'run':
            n, why = run_n(w)
            if i < rs[0] or n is None:
                print('%s: [%s]' % ('read_restart 앞에 run' if i < rs[0] else why, l))
                return 1
            runs.append(l)
            tot += n
    if not runs or (words(L[-1]) or [''])[0] != 'run':
        print('시험 덱 마지막 명령이 run 이 아님')
        return 1
    print('%d %d %s' % (tot, len(runs), fmt(runs)))
    return 0


def deck_spans(path):
    # deck() 와 같은 규칙으로 명령을 만들고, 명령마다 그 명령을 이룬 원 줄 번호 (처음 · 끝) 를 함께 낸다
    res, buf, b0 = [], '', None
    with open(path, encoding='utf-8', errors='replace') as f:
        raw = f.read().split('\n')
    for i, line in enumerate(raw):
        r = line.rstrip()
        if b0 is None:
            b0 = i
        if r.endswith('&'):
            buf += r[:-1] + ' '
            continue
        s = ' '.join(uncomment(buf + r).split())
        buf = ''
        if s:
            res.append((s, b0, i))
        b0 = None
    return res, raw


def fix_run(main, res, ckpt, s0, W):
    # 10-27 ibb kg50_d2_b50 r4 (1저자 Q1 (가) "권고대로 해줘"): dem_restart.py 의 settling 잔여 = 본 덱 그 run 길이 − 체크포인트 step
    # (200000 − 20001 = 179999) 인데 본 덱 정착 run 은 삽입 run 1 뒤 step 1 에서 시작해 끝이 200001 → 재개 끝 200000 = 1 step 짧다.
    # 고치는 꼴은 하나뿐: 정적 대조 문제가 그 '남은 step 다름' 하나 · 재개 덱 첫 긴 run 이 한 줄짜리 숫자 run (upto 없음) · 맞는 값 = 원래 + 1.
    # 그 줄의 숫자만 바꾸고 (앞 공백 · 뒤 주석 그대로) 다시 읽어 명령이 그 하나만 다르고 정적 대조 문제 0 일 때만 바꾼다 (임시 파일 → os.replace).
    # 그 밖 = 그대로 둔다 (뒤의 정적 대조가 거부).  종료 코드 0 = 고칠 것 없음 또는 고침 · 1 = 고치지 않음.
    import shutil
    s0 = int(s0)
    probs, _ = check(main, res, ckpt, s0, W)
    if not probs:
        print('  · 첫 긴 run 고칠 것 없음 (정적 대조 통과)')
        return 0
    rem = [p for p in probs if p.startswith('남은 step 다름')]
    if len(probs) != 1 or len(rem) != 1:
        print('  · 첫 긴 run 그대로 — 정적 대조 문제 %d 개 (남은 step 다름 하나뿐일 때만 고친다)' % len(probs))
        return 1
    m = re.match(r'^남은 step 다름: 재개 끝 ([0-9]+) ↔ 본 덱 그 run 끝 ([0-9]+) \(\[run ([0-9]+)\]\)$', rem[0])
    if not m:
        print('  · 첫 긴 run 그대로 — 숫자 한 개짜리 run 이 아님 (upto · 다른 꼴): %s' % rem[0])
        return 1
    end, want, n0 = (int(x) for x in m.groups())
    n1 = want - s0
    if n1 != n0 + 1:
        print('  · 첫 긴 run 그대로 — 차이 %+d step (dem_restart.py 의 1 step 짧음 꼴만 고친다)' % (n1 - n0))
        return 1
    R = deck(res)
    ir = long_runs(R)[0]
    spans, raw = deck_spans(res)
    if [s for s, _, _ in spans] != R or spans[ir][0] != 'run %d' % n0 or spans[ir][1] != spans[ir][2]:
        print('  · 첫 긴 run 그대로 — 그 run 이 원 줄 하나가 아님 (& 이어 붙이기 · 손으로 봐야 함)')
        return 1
    k = spans[ir][1]
    with open(res, 'rb') as f:
        rawb = f.read().split(b'\n')
    try:
        line = rawb[k].decode('utf-8')
    except (IndexError, UnicodeDecodeError):
        line = None
    mm = re.match(r'^(\s*run\s+)([0-9]+)(\s*(#.*)?)$', line) if line is not None else None
    if not mm or int(mm.group(2)) != n0 or len(rawb) != len(raw):
        print('  · 첫 긴 run 그대로 — 원 줄을 못 읽음: [%s]' % raw[k])
        return 1
    rawb[k] = (mm.group(1) + str(n1) + mm.group(3)).encode('utf-8')
    t = res + '.fixrun'
    try:
        with open(t, 'wb') as f:
            f.write(b'\n'.join(rawb))
        R2 = deck(t)
        p2, _ = check(main, t, ckpt, s0, W)
        if len(R2) != len(R) or [i for i in range(len(R)) if R[i] != R2[i]] != [ir] or R2[ir] != 'run %d' % n1 or p2:
            print('  · 첫 긴 run 그대로 — 고친 덱 다시 대조 실패 (문제 %d)' % len(p2))
            return 1
        shutil.copystat(res, t)
        os.replace(t, res)
    finally:
        if os.path.exists(t):
            os.remove(t)
    print('  · 재개 덱 첫 긴 run 고침 (1저자 10-27 Q1 (가)): [run %d] → [run %d] — 본 덱 그 run 끝 %d − 체크포인트 step %d '
          '(dem_restart.py 잔여는 끝 %d = 1 step 짧음 · 원 줄 %d · 다시 대조 통과)' % (n0, n1, want, s0, end, k + 1))
    return 0


def strip_comments(W):
    # -c (10-27 ibb · dem_restart.py 덱 검사가 머리 주석의 다른 케이스 이름도 거부): 작업 폴더 W 의 맨 위 input*.liggghts 에서
    # 줄 전체 주석 (첫 공백 아닌 글자 '#') 만 뺀다 — 인라인 주석 · 빈 줄 · 나머지 바이트 (줄 끝 포함) 그대로.
    # 덱마다 검사: 비주석 줄 sha256 = 원 파일 ↔ 다시 읽은 새 파일 · 새 파일에 줄 전체 주석 0 · LIGGGHTS 명령 (deck()) 같음
    # ('&' 로 이어진 명령 안의 주석 줄 · '&' 로 끝나는 주석 줄은 빼면 명령이 바뀐다).  하나라도 실패 = 어느 덱도 안 바꾼다.
    # 쓰기 = 임시 파일 → 검사 → 전부 통과 뒤 os.replace (새 inode — 멈춘 폴더 · 링크 대상 파일은 안 건드린다).
    import fnmatch, hashlib, shutil

    def lines(b):
        parts = b.split(b'\n')
        return [x + b'\n' for x in parts[:-1]] + ([parts[-1]] if parts[-1] else [])

    def body(b):
        return [x for x in lines(b) if not x.lstrip().startswith(b'#')]

    names, recs, probs, tmps, done, total = [], [], [], [], [], 0
    try:
        names = sorted(n for n in os.listdir(W)
                       if fnmatch.fnmatchcase(n, 'input*.liggghts') and os.path.isfile(os.path.join(W, n)))
        if not names:
            probs.append('작업 폴더에 input*.liggghts 없음')
        for name in names:
            p = os.path.join(W, name)
            with open(p, 'rb') as f:
                old = f.read()
            keep = body(old)
            n = len(lines(old)) - len(keep)
            h0 = hashlib.sha256(b''.join(keep)).hexdigest()
            if n == 0:
                recs.append('%s: 줄 전체 주석 0 줄 뺌 (파일 그대로) · 남은 줄 %d · 비주석 줄 sha256 전 %s = 후 %s'
                            % (name, len(keep), h0, h0))
                continue
            t = p + '.cstrip'
            tmps.append((t, p))
            with open(t, 'wb') as f:
                f.write(b''.join(keep))
            with open(t, 'rb') as f:
                new = f.read()
            h1 = hashlib.sha256(b''.join(body(new))).hexdigest()
            left = len(lines(new)) - len(body(new))
            dm, dn = deck(p), deck(t)
            if h1 != h0:
                probs.append('%s: 비주석 줄 sha256 다름 — 전 %s · 후 %s' % (name, h0, h1))
            if left:
                probs.append('%s: 새 파일에 줄 전체 주석 %d 줄 남음' % (name, left))
            if dm != dn:
                i = next(j for j in range(max(len(dm), len(dn)))
                         if j >= len(dm) or j >= len(dn) or dm[j] != dn[j])
                probs.append('%s: 주석 줄을 빼면 LIGGGHTS 명령이 바뀐다 (예: & 이어 붙이기 안의 주석 줄 · & 로 끝나는 주석 줄) — '
                             '%d 번째 명령 전 [%s] ↔ 후 [%s] · 손으로 봐야 함'
                             % (name, i + 1, dm[i][:120] if i < len(dm) else '없음', dn[i][:120] if i < len(dn) else '없음'))
            total += n
            recs.append('%s: 줄 전체 주석 %d 줄 뺌 · 남은 줄 %d · 비주석 줄 sha256 전 %s = 후 %s · LIGGGHTS 명령 %d 개 같음'
                        % (name, n, len(keep), h0, h1, len(dn)))
        if not probs:
            for t, p in tmps:
                shutil.copystat(p, t)
                os.replace(t, p)
                done.append(os.path.basename(p))
    except Exception as e:
        probs.append('도구 오류: %s: %s' % (type(e).__name__, e))
    finally:
        for t, _ in tmps:
            if os.path.exists(t):
                os.remove(t)
    if probs:
        for q in probs:
            print('  ✗ ' + q)
        print('  주석 줄 빼기 (-c): 실패 — %s' % ('이미 바꾼 덱 %s (작업 폴더만)' % ' '.join(done) if done else '어느 덱도 안 바꿈'))
        return 1
    for r in recs:
        print('  · ' + r)
    print('  주석 줄 빼기 (-c): 통과 (덱 %d · 뺀 줄 %d)' % (len(names), total))
    return 0


if len(sys.argv) == 3 and sys.argv[1] == '--strip-comments':
    sys.exit(strip_comments(sys.argv[2]))
if len(sys.argv) == 3 and sys.argv[1] == '--trial-steps':
    try:
        sys.exit(trial_steps(sys.argv[2]))
    except Exception as e:
        print('도구 오류: %s: %s' % (type(e).__name__, e))
        sys.exit(1)
if len(sys.argv) == 7 and sys.argv[1] == '--fix-run':
    try:
        sys.exit(fix_run(*sys.argv[2:7]))
    except Exception as e:
        print('  · 첫 긴 run 그대로 — 도구 오류: %s: %s' % (type(e).__name__, e))
        sys.exit(1)
try:
    main, res, ckpt, s0, W = sys.argv[1:6]
    probs, notes = check(main, res, ckpt, int(s0), W)
except Exception as e:
    probs, notes = ['대조 도구 오류: %s: %s' % (type(e).__name__, e)], []
for n in notes:
    print('  · ' + n)
for p in probs:
    print('  ✗ ' + p)
print('  재개 덱 정적 대조: %s (문제 %d)' % ('통과' if not probs else '실패', len(probs)))
sys.exit(1 if probs else 0)