import difflib, os, re, sys
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


# ── 10-28 밤 전체 프로그램 대조 (Codex 재검토 KG50R-02 · 03 · 05 · 원장 KG50-10 · 18 · 1저자 Q2 (가) "50kg도 권고대로해") ──
#   재개 덱 = [준비 구간: 체크포인트 시점 상태를 다시 선언] + [뒤 구간: 본 덱의 체크포인트 뒤를 명령 하나하나 그대로]
#   뒤 구간 — restart 체크포인트 = 본 덱 그 run (남은 step 만 다름 · 그 run 에 꼬리 (every · pre · post · start · stop · upto …) 가 있으면
#     거부 · 10-28 밤 2 사전 공격 B) 부터 끝까지 · write_restart 체크포인트 = 그 줄 다음 명령부터 끝까지 (판 높이 run 1 같은 짧은 run ·
#     첫 긴 run 까지 글자 그대로)
#   준비 구간 — 상태 명령 (STATE_CMD) 과, 본 덱 체크포인트 앞에 글자 그대로 있는 print · if (print · quit 만) · group (type 꼴) ·
#     shell mkdir 만.  그 밖 (velocity · set · delete_atoms · run · label · jump · create_box · 모르는 명령 …) = 거부.
#     10-28 밤 2 (사전 공격 A): 상태 명령 줄도 본 덱 체크포인트 앞에 글자 그대로 있어야 하고, 준비 구간 명령 순서 = 본 덱 체크포인트 앞
#     명령의 순서 보존 부분열 (같은 변수를 두 번 정의하면 본 덱과 같은 순서 · 같은 정의만 — LIGGGHTS 는 ${x} 를 그 자리에서 치환한다)
#   상태 — 준비 구간 끝의 상태 표 (마지막 정의) = 본 덱 체크포인트 시점 상태 표 (즉시 치환의 그 자리 값은 위 글자 · 순서 대조가 본다).
#     꼭 있어야 (빠짐 = 거부): fix · fix_modify · 전역 설정 · pair · restart · atom/neigh/comm_modify.  재개 덱이 선언하면 같아야 (빠짐 =
#     허용 · 쓰는 곳은 아래 참조 검사 · c_/f_ 검사가 본다): compute · 변수 · dump · region · thermo · 템플릿 fix.  재개 덱에만 있는 것 = 거부
#   허용 차이 (목록 고정 · 시험): 첫 긴 run 남은 수 (restart 체크포인트) · 판 메시 fix 의 file 이름 (그 파일이 작업 폴더에 있을 때) ·
#     shell mkdir ↔ mkdir -p · 위 '선언하면 같아야' 항목의 빠짐 · 템플릿 fix 재선언 (본 덱 줄 그대로 · 순서 대조에서 뺀다)
#   그 밖 — 변수 참조 (${x} · $x · v_x) 는 그 앞에 정의 · label 은 본 덱 · 재개 덱 각각 유일 · jump 목적지 = 재개 덱에 있고 본 덱 뒤 구간의 그
#     label · 명령 자리 (최상위 · if 안 · run every 안) 의 include · next · jump SELF <label> 말고 다른 jump · 이름에 변수인 명령 = 거부 ·
#     첫 긴 run = 꼬리 없는 run N 한 줄 (every · pre · post · start · stop · upto · & 이음 = 거부) · read_restart 1 개 = 체크포인트
#   압축 체크포인트 (restart_compress_* · 반복 안 restart 체크포인트) = 거부 (KG50R-01 · 1저자 10-28 Q3 (가))
STATE_CMD = {'fix', 'unfix', 'fix_modify', 'compute', 'uncompute', 'compute_modify', 'variable', 'dump', 'undump',
             'dump_modify', 'region', 'thermo', 'thermo_style', 'thermo_modify', 'timestep', 'neighbor', 'neigh_modify',
             'atom_style', 'atom_modify', 'units', 'boundary', 'newton', 'dimension', 'processors', 'soft_particles',
             'communicate', 'comm_style', 'comm_modify', 'restart', 'pair_style', 'pair_coeff'}
GLOB1 = {'timestep', 'neighbor', 'atom_style', 'units', 'boundary', 'newton', 'dimension', 'processors', 'soft_particles',
         'communicate', 'comm_style', 'restart', 'pair_style'}
MODS = {'atom_modify', 'neigh_modify', 'comm_modify'}
REQ_CAT = {'fix', 'fix_modify', 'glob', 'mods', 'pair_coeff'}
VAR_OK = {'equal', 'atom', 'string', 'delete'}
Q3MSG = '압축 체크포인트 재개 = 지원 안 함 (KG50R-01 · 1저자 10-28 Q3 (가))'
VREF = re.compile(r'\$\{([^}]*)\}|\$([A-Za-z0-9_])|(?<![A-Za-z0-9_])v_([A-Za-z0-9_]+)')


def unsupported(l):
    # 다룰 수 없는 구문 (10-28 KG50R-03 (ⅵ)) — if 안 명령까지 · '' = 없음
    w = words(l)
    if w is None:
        return '따옴표를 못 읽음'
    todo, n = [w], 0
    while todo and n < 64:
        cw = todo.pop()
        n += 1
        if not cw:
            continue
        c = cw[0]
        if '$' in c:
            return '명령 이름에 변수'
        if c in ('include', 'next'):
            return c
        if c == 'jump' and not (len(cw) == 3 and cw[1] == 'SELF'):
            return 'jump 꼴 (jump SELF <label> 만)'
        if c == 'run' and 'every' in cw[2:]:
            # 10-28 밤 2 (사전 공격 B): run … every M "명령" … 의 명령도 본다 (그 안 include · next · jump 를 예전에는 못 봤다)
            k = cw.index('every', 2)
            for x in cw[k + 2:]:
                if x == 'NULL':
                    continue
                xw = words(x)
                if xw is None:
                    return 'run every 명령 따옴표를 못 읽음'
                todo.append(xw)
        if c == 'if':
            cs = if_cmds(cw)
            if cs is None:
                return 'if 꼴을 못 읽음'
            for x in cs:
                xw = words(x)
                if xw is None:
                    return 'if 안 따옴표를 못 읽음'
                todo.append(xw)
    return ''


def first_run_form(res, R, ir):
    # 재개 덱 첫 긴 run = 꼬리 없는 [run N] 원 줄 한 줄 (10-28 KG50R-02 · 05) — '' = 됨 · 아니면 이유
    w = words(R[ir])
    if not w or len(w) != 2 or w[0] != 'run' or not re.fullmatch(r'[0-9]+', w[1]):
        return ('재개 덱 첫 긴 run 꼴이 지원 밖 (10-28 KG50R-02 · 꼬리 없는 run N 만 · every · pre · post · start · stop · upto · '
                '변수 = 거부): [%s]' % R[ir])
    spans, _ = deck_spans(res)
    if [s for s, _, _ in spans] != R:
        return '재개 덱 원 줄 ↔ 명령 대응을 못 정함 (10-28 KG50R-05 · 시험 덱을 자를 줄을 모른다)'
    if spans[ir][1] != spans[ir][2]:
        return ('재개 덱 첫 긴 run 이 & 로 이어진 여러 줄 (원 줄 %d–%d · 10-28 KG50R-05 · 시험 덱을 한 줄로 못 자른다): [%s]'
                % (spans[ir][1] + 1, spans[ir][2] + 1, R[ir]))
    return ''


def run_state(L, where, probs):
    # 명령 목록이 끝에서 남기는 상태 (10-28 KG50R-03) — 키 → 줄 (… _modify · 쌓이는 꼴은 줄 묶음)
    st = {}
    for l in L:
        w = words(l)
        if not w:
            continue
        c, n = w[0], len(w)
        if c == 'fix' and n >= 4:
            st[('fix', w[1])] = l
            st.pop(('fix_modify', w[1]), None)
        elif c == 'unfix' and n >= 2:
            st.pop(('fix', w[1]), None)
            st.pop(('fix_modify', w[1]), None)
        elif c in ('fix_modify', 'compute_modify', 'dump_modify') and n >= 2:
            st[(c, w[1])] = st.get((c, w[1]), ()) + (l,)
        elif c == 'compute' and n >= 4:
            st[('compute', w[1])] = l
            st.pop(('compute_modify', w[1]), None)
        elif c == 'uncompute' and n >= 2:
            st.pop(('compute', w[1]), None)
            st.pop(('compute_modify', w[1]), None)
        elif c == 'dump' and n >= 2:
            st[('dump', w[1])] = l
            st.pop(('dump_modify', w[1]), None)
        elif c == 'undump' and n >= 2:
            st.pop(('dump', w[1]), None)
            st.pop(('dump_modify', w[1]), None)
        elif c == 'variable' and n >= 3:
            if w[2] == 'delete':
                st.pop(('variable', w[1]), None)
            elif w[2] in VAR_OK:
                st[('variable', w[1])] = l
            else:
                probs.append('%s 에 다룰 수 없는 변수 꼴 %s (equal · atom · string · delete 만 · 10-28 KG50R-03): [%s]' % (where, w[2], l))
        elif c == 'region' and n >= 3:
            if w[2] == 'delete':
                st.pop(('region', w[1]), None)
            else:
                st[('region', w[1])] = l
        elif c == 'thermo_style':
            st[('thermo_style',)] = l
            st.pop(('thermo_modify',), None)
        elif c == 'thermo':
            st[('thermo',)] = l
        elif c == 'thermo_modify':
            st[('thermo_modify',)] = st.get(('thermo_modify',), ()) + (l,)
        elif c in GLOB1:
            st[('glob', c)] = l
        elif c in MODS:
            st[('mods', c)] = st.get(('mods', c), ()) + (l,)
        elif c == 'pair_coeff' and n >= 3:
            st[('pair_coeff', w[1], w[2])] = l
    return st


def kname(k):
    if k[0] in ('glob', 'mods'):
        return k[1]
    if k[0] == 'pair_coeff':
        return 'pair_coeff %s %s' % (k[1], k[2])
    return ' '.join(k)


def need(k, v):
    # 본 덱 상태에 있으면 재개 덱에도 꼭 있어야 하는 것 (템플릿 fix 는 선언하면 같아야만)
    if k[0] not in REQ_CAT:
        return False
    if k[0] == 'fix':
        w = words(v) or []
        return not (len(w) >= 4 and TMPL.match(w[3]))
    return True


def mkdir_key(w):
    # shell mkdir [-p] 디렉터리… → 디렉터리 묶음 (mkdir ↔ mkdir -p 같게) · 아니면 None
    return tuple(x for x in w[2:] if x != '-p') if w[:2] == ['shell', 'mkdir'] else None


def cmd_eq(a, b):
    # 허용 차이까지 같은 명령인가 — 'same' · 'mesh:<새 파일>' (판 메시 fix 의 file 이름만 다름 · 파일 있는지는 부르는 쪽) · '' (다름)
    if a == b:
        return 'same'
    ka, kb = mkdir_key(words(a) or []), mkdir_key(words(b) or [])
    if ka is not None and ka == kb:
        return 'same'                     # shell mkdir ↔ mkdir -p (같은 디렉터리)
    nf = mesh_file(a, b)
    return ('mesh:' + nf) if nf is not None else ''


def seq_cmp(ml, rl, W, notes, probs, what):
    # 명령 하나하나 같아야 (10-28 KG50R-03) — 허용 차이 = 판 메시 fix 의 file 이름 (그 파일이 작업 폴더에 있을 때) · shell mkdir ↔ mkdir -p
    # 같으면 True · 다르면 문제 한 줄 (같은 수면 첫 차이 · 수가 다르면 더함 · 빠짐 · 바뀜을 앞에서 셋까지)
    if len(ml) == len(rl):
        bad = []
        for i, (a, b) in enumerate(zip(ml, rl)):
            e = cmd_eq(a, b)
            if e == 'same':
                continue
            if e:
                nf = e[5:]
                if os.path.isfile(os.path.join(W, nf)):
                    notes.append('판 메시 파일만 다름 (%s): %s' % (what, nf))
                else:
                    probs.append('판 메시 파일 %s 가 작업 폴더에 없음 (%s)' % (nf, what))
                continue
            bad.append((i, a, b))
        if not bad:
            if ml:
                notes.append('%s 같음 (10-28 KG50R-03 · 명령 하나하나 %d 개)' % (what, len(ml)))
            return True
        i, a, b = bad[0]
        probs.append('%s 다름 (10-28 KG50R-03 · 명령 하나하나): %d 곳 · 첫 차이 %d 번째 — 본 덱 [%s] ↔ 재개 덱 [%s]'
                     % (what, len(bad), i + 1, a, b))
        return False
    sm = difflib.SequenceMatcher(None, ml, rl, autojunk=False)
    kind = {'insert': '재개 덱에만', 'delete': '재개 덱에 없음', 'replace': '바뀜'}
    desc = ' · '.join('%s %s%s' % (kind[op], fmt((rl[j1:j2] if op == 'insert' else ml[i1:i2])[:2]),
                                   (' → ' + fmt(rl[j1:j2][:2])) if op == 'replace' else '')
                      for op, i1, i2, j1, j2 in [o for o in sm.get_opcodes() if o[0] != 'equal'][:3])
    probs.append('%s 다름 (10-28 KG50R-03 · 명령 하나하나): 본 덱 %d 개 ↔ 재개 덱 %d 개 — %s' % (what, len(ml), len(rl), desc))
    return False


def setup_check(Rs, Mp, probs):
    # 재개 덱 준비 구간 (read_restart 빼고) 의 명령 종류 (10-28 KG50R-03) — Mp = 본 덱 체크포인트 앞 명령
    mset = set(Mp)
    mk = set(k for k in (mkdir_key(words(l) or []) for l in Mp) if k is not None)
    for l in Rs:
        w = words(l)
        if not w:
            continue                      # 따옴표 = 다룰 수 없는 구문이 본다
        c = w[0]
        if c in STATE_CMD:
            continue
        if c == 'shell' and mkdir_key(w) is not None and mkdir_key(w) in mk:
            continue
        if c in ('print', 'if', 'group') and l in mset:
            if c == 'if' and not if_ok(w):
                probs.append('재개 덱 준비 구간의 if 에 print · quit 말고 다른 명령 (10-28 KG50R-03): [%s]' % l)
            elif c == 'group' and (len(w) < 3 or w[2] != 'type'):
                probs.append('재개 덱 준비 구간의 group 은 type 꼴만 (다시 고르면 원자가 바뀔 수 있다 · 10-28 KG50R-03): [%s]' % l)
            continue
        probs.append('재개 덱 준비 구간 명령 허용 안 됨 (10-28 KG50R-03 · 상태 명령 · 본 덱 체크포인트 앞에 글자 그대로 있는 print · '
                     'if (print · quit 만) · group type · shell mkdir 만): [%s]' % l)


def setup_order(Rs, Mp, probs):
    # 10-28 밤 2 (독립 사전 공격 A · KG50R-03 부류): 준비 구간 (read_restart 빼고) = 본 덱 체크포인트 앞 명령의 순서 보존 부분열.
    #   상태 명령 줄은 본 덱 체크포인트 앞에 글자 그대로 있어야 하고 명령 순서 (상태 + 동작) 도 본 덱과 같아야 한다 — LIGGGHTS 는
    #   ${x} 를 그 자리에서 치환하므로 끝 상태 표만 같아서는 안 된다 (변수를 바꿨다 되돌리면 끝 표는 같은데 timestep 은 2 배).
    #   허용 차이 줄: 템플릿 fix (④ · 도구가 read_restart 바로 뒤에 넣는다) = 빼고 본다 · shell mkdir ↔ mkdir -p (③) · 판 메시 fix 의
    #   file 이름 (② · 파일이 있는지는 상태 대조가 본다) = 같은 명령으로 본다
    def tmpl(l):
        w = words(l) or []
        return len(w) >= 4 and w[0] == 'fix' and bool(TMPL.match(w[3]))

    def eq(r, m):
        if r == m:
            return True
        kr, km = mkdir_key(words(r) or []), mkdir_key(words(m) or [])
        if kr is not None and kr == km:
            return True
        return mesh_file(m, r) is not None

    Mq = [l for l in Mp if not tmpl(l)]
    j, prev = 0, None
    for l in Rs:
        w = words(l)
        if not w or tmpl(l):
            continue                      # 따옴표 = 다룰 수 없는 구문 · 템플릿 = 상태 대조 (선언하면 같아야)
        if not any(eq(l, m) for m in Mq):
            if w[0] in STATE_CMD:
                probs.append('재개 덱 준비 구간 상태 명령이 본 덱 체크포인트 앞에 글자 그대로 없음 (10-28 사전 공격 A · LIGGGHTS 는 '
                             '${x} 를 그 자리에서 치환한다 — 끝 상태만 같아서는 안 된다): [%s]' % l)
            continue                      # 동작 줄은 setup_check 가 이미 거부
        k = j
        while k < len(Mq) and not eq(l, Mq[k]):
            k += 1
        if k == len(Mq):
            probs.append('재개 덱 준비 구간 명령 순서가 본 덱 체크포인트 앞 순서와 다름 (10-28 사전 공격 A · 순서 보존 부분열이어야 — '
                         '같은 변수 다시 정의 · fix 순서): [%s] 는 본 덱에서 [%s] 보다 앞에만 있다' % (l, prev or '(처음)'))
            return
        j, prev = k + 1, l


def mprefix_check(Mp, probs):
    # 본 덱 체크포인트 앞 if = print · quit · jump 만 (그 밖 = 그 시점 상태를 정할 수 없다 · 10-28 KG50R-03)
    for l in Mp:
        w = words(l) or ['']
        if w[0] != 'if':
            continue
        cs = if_cmds(w)
        if cs is None or any((words(c) or [''])[0] not in IFOK | {'jump'} for c in cs):
            probs.append('본 덱 체크포인트 앞 if 에 print · quit · jump 말고 다른 명령 — 그 시점 상태를 정할 수 없음 (10-28 KG50R-03): [%s]' % l)


def state_cmp(stM, stR, W, notes, probs):
    # 재개 지점 상태 (10-28 KG50R-03 · 예전 C 를 넓힘) — 본 덱 체크포인트 시점 ↔ 재개 덱 준비 구간 끝
    skip = []
    for k in sorted(set(stM) | set(stR), key=lambda x: tuple(str(y) for y in x)):
        a, b = stM.get(k), stR.get(k)
        if a == b:
            continue
        what = '재개 지점 ' + kname(k)
        if b is None and not need(k, a):
            skip.append(kname(k))
            continue
        if isinstance(a, tuple) or isinstance(b, tuple):
            probs.append('%s 다름 (10-28 KG50R-03): 본 덱 %s ↔ 재개 덱 %s' % (what, fmt(list(a or ())), fmt(list(b or ()))))
        else:
            same_or_mesh(a, b, W, notes, probs, what)
    notes.append('재개 지점 상태 대조 (10-28 KG50R-03): 본 덱 %d 항목 · 재개 덱 %d 항목%s' % (
        len(stM), len(stR), (' · 재개 덱이 다시 선언하지 않음 (선언하면 같아야 하는 것 · 쓰는 곳은 참조 검사): ' + ' · '.join(skip)) if skip else ''))


def var_refs(R, probs):
    # 재개 덱의 변수 참조 (${x} · $x · v_x) = 그 앞에 variable 정의 (10-28 KG50R-03 (ⅲ) · 변수는 restart 에 안 남는다)
    d = set()
    for i, l in enumerate(R):
        miss = []
        for m in VREF.finditer(l):
            nm = next(g for g in m.groups() if g is not None)
            if nm not in d and nm not in miss:
                miss.append(nm)
        if miss:
            probs.append('재개 덱이 정의 전 변수를 씀 (10-28 KG50R-03 · ${x} · $x · v_x): %s — %d 번째 명령 [%s]' % (' '.join(miss), i + 1, l))
        w = words(l) or ['']
        if w[0] == 'variable' and len(w) >= 3:
            if w[2] == 'delete':
                d.discard(w[1])
            else:
                d.add(w[1])


def labels_of(L):
    out = []
    for i, l in enumerate(L):
        w = words(l) or ['']
        if w[0] == 'label':
            out.append((i, w[1] if len(w) > 1 else ''))
    return out


def label_check(M, R, pM, probs):
    # label = 본 덱 · 재개 덱 각각 유일 · jump 목적지 = 재개 덱에 있고 본 덱 뒤 구간 (pM 부터) 의 그 label (10-28 KG50R-03 (ⅳ))
    for nm, L in (('본 덱', M), ('재개 덱', R)):
        names = [x for _, x in labels_of(L)]
        dup = sorted(set(x for x in names if names.count(x) > 1))
        if dup:
            probs.append('%s label 이 겹침 (10-28 KG50R-03 · jump SELF 는 처음 만나는 같은 이름 label 로 간다): %s' % (nm, ' '.join(dup)))
    rl = dict((x, i) for i, x in labels_of(R))
    ml = dict((x, i) for i, x in labels_of(M))
    for l in R:
        w = words(l) or ['']
        cs = [w] if w[0] != 'if' else [words(c) or [''] for c in (if_cmds(w) or [])]
        for cw in cs:
            if cw[0] != 'jump' or len(cw) != 3 or cw[1] != 'SELF':
                continue                  # 다른 jump 꼴 = 다룰 수 없는 구문이 본다
            if cw[2] not in rl:
                probs.append('jump 목적지 label %s 가 재개 덱에 없음 (10-28 KG50R-03): [%s]' % (cw[2], l))
            elif ml.get(cw[2], -1) < pM:
                probs.append('jump 목적지 label %s 가 본 덱 체크포인트 뒤 구간에 없음 (자리가 다르다 · 10-28 KG50R-03): [%s]' % (cw[2], l))


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
    # 10-28 밤 (KG50R-01 · 02 · 03 · 05 · 1저자 Q2 (가) · Q3 (가)) — 전체 프로그램 대조 (규칙 = 위 STATE_CMD 머리 주석)
    #   예전 B (물리 줄이 본 덱 어딘가에) · C (fix · 쌍 · 이웃 · timestep 만) · E (fix · run · if … 만 순서) = 아래 상태 · 구간 대조가 대신한다
    M, R = deck(main), deck(res)
    probs, notes = [], []
    # 0. 다룰 수 없는 구문 (10-28 KG50R-03 (ⅵ)) — 본 덱 · 재개 덱 어디든 (if 안 명령 포함)
    for nm, L in (('본 덱', M), ('재개 덱', R)):
        for l in L:
            bad = unsupported(l)
            if bad:
                probs.append('다룰 수 없는 구문 (%s · %s · 10-28 KG50R-03): [%s]' % (nm, bad, l))
    # A. 재삽입 금지
    for l in R:
        t = l.split()
        if t[0] == 'fix' and len(t) >= 4 and INS.match(t[3]):
            probs.append('재개 덱에 삽입 fix (재삽입): [%s]' % l)
    # F. 재개 덱에서 쓰는 c_ · f_ 이름이 재개 덱에 정의돼 있다 (compute · fix 는 restart 에 안 남는다)
    dc = set(l.split()[1] for l in R if l.split()[0] == 'compute' and len(l.split()) > 1)
    df = set(l.split()[1] for l in R if l.split()[0] == 'fix' and len(l.split()) > 1)
    for l in R:
        for kind, name in re.findall(r'\b([cf])_([A-Za-z0-9_]+)', l):
            if name not in (dc if kind == 'c' else df):
                probs.append('재개 덱이 %s_%s 를 쓰는데 정의가 없음: [%s]' % (kind, name, l))
    # read_restart — 재개 덱에 1 개 · 그 파일 = 체크포인트 (10-28 KG50R-03)
    rs = [i for i, l in enumerate(R) if l.split()[0] == 'read_restart']
    if len(rs) != 1:
        probs.append('재개 덱에 read_restart 가 %d 개 (1 개여야 · 10-28 KG50R-03)' % len(rs))
        return probs, notes
    rw = words(R[rs[0]]) or []
    if len(rw) != 2 or os.path.normpath(rw[1]) != os.path.normpath(ckpt):
        probs.append('재개 덱 read_restart 가 체크포인트 %s 가 아님 (10-28 KG50R-03): [%s]' % (ckpt, R[rs[0]]))
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
    if ir < rs[0]:
        probs.append('재개 덱 첫 긴 run 이 read_restart 앞 (10-28 KG50R-03): [%s]' % R[ir])
        return probs, notes
    # 첫 긴 run 꼴 (10-28 KG50R-02 · 05) — 꼬리 없는 run N · 원 줄 한 줄
    form = first_run_form(res, R, ir)
    if form:
        probs.append(form)
    pM, q = im, ir                        # 뒤 구간 시작 — 본 덱 pM · 재개 덱 q (준비 구간 = 재개 덱 q 앞 · 본 덱 상태 = pM 앞)
    if kind == 'restart' and len(words(M[im]) or []) > 2:
        # 10-28 밤 2 (사전 공격 B): 체크포인트가 든 본 덱 run 에 꼬리 (every · pre · post · start · stop · upto …) — 재개 덱 첫 긴 run 은
        #   꼬리 없는 run N 한 줄이라 같은 동작을 낼 수 없다 (예전 = 남은 step 만 보고 꼬리를 안 봤다)
        probs.append('본 덱 체크포인트 run 에 꼬리가 있음 (every · pre · post · start · stop · upto · 10-28 사전 공격 B — 재개 덱 첫 긴 run '
                     '(꼬리 없는 run N 한 줄) 으로는 같은 동작을 낼 수 없다): [%s]' % M[im])
    if kind == 'restart':
        # D. 남은 step — restart 명령이 만든 체크포인트 · 그 run 앞에 반복 · 변수 run 이 없을 때
        step, step0, known = 0, 0, True
        for i, l in enumerate(M[:im + 1]):
            t = l.split()
            if i == im:
                step0 = step
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
        labs = [i for i in range(ia + 1, im) if M[i].split()[0] == 'label']
        # Q3 (가) · KG50R-01: 압축 체크포인트 (이름 restart_compress_* · 반복 안 restart 체크포인트) = 거부 — 체크포인트가 루프 run 의 어디서
        #   저장됐는지 (다음 판정까지 남은 step) 를 맞추지 않는다 · 이완 중 restart_compress_* (KG50-11) 도 같은 길
        if base.startswith('restart_compress_') or (not known and labs):
            probs.append('%s — 체크포인트 %s (%s)' % (Q3MSG, base, '이름 restart_compress_*' if base.startswith('restart_compress_')
                                                     else '본 덱 반복 (label · jump) 안 restart 체크포인트'))
        if known:
            # 10-28 (KG50-18): 체크포인트 = 본 덱 그 run 도중 → 재개 덱 첫 긴 run 앞에 run (run 0 말고) 이 없어야
            #   (G0 이 시험 덱 run 합을 보면 그 run 으로 생긴 어긋남을 예전 G0 (마지막 run 만) 처럼 우연히 막지 못한다)
            pre = [l for l in R[:ir] if l.split()[0] == 'run' and run_n(words(l) or [''])[0] != 0]
            if pre:
                probs.append('재개 덱 첫 긴 run 앞에 run 이 있음 (restart 체크포인트 = 본 덱 그 run 도중 · 10-28 KG50-18): %s' % fmt(pre))
            if not step0 < s0 < step:
                probs.append('체크포인트 step %d 가 본 덱 그 run 의 범위 (%d, %d) 밖 (10-28 KG50R-03): [%s]' % (s0, step0, step, M[im]))
            elif not form:
                end = s0 + int(R[ir].split()[1])
                if end != step:
                    probs.append('남은 step 다름: 재개 끝 %d ↔ 본 덱 그 run 끝 %d ([%s])' % (end, step, R[ir]))
                else:
                    notes.append('남은 step 같음: 끝 %d' % end)
        elif labs:
            # 압축 루프 (위에서 거부) — 뒤 구간 = 루프 머리 label 부터 · 첫 긴 run 글자 그대로 (나머지 대조는 기록용)
            pM = labs[-1]
            if R[ir] != M[im]:
                probs.append('첫 긴 run 다름 (반복 안 restart 체크포인트 · 10-28 KG50R-01): 본 덱 [%s] ↔ 재개 덱 [%s]' % (M[im], R[ir]))
        else:
            probs.append('남은 step 을 정할 수 없음 (그 run 앞에 반복 · 흐름 · 변수 run · 체크포인트 뒤 루프 머리 label 없음 · 10-28 KG50-19) — 손으로 확인')
    else:
        # 10-28 (KG50-19): write_restart 체크포인트 = 그 뒤 run 을 처음부터 다시 — 본 덱 그 줄 뒤 첫 긴 run 까지의 실행 순서 줄 (run · label)
        # = 재개 덱 read_restart 뒤 첫 긴 run 까지 (글자 같아야) · run 수가 변수 · 흐름 줄이면 정할 수 없음 = 거부 (예전 = 해당 없음 · 통과)
        ml = [l for l in M[ia + 1:im + 1] if ctl(l)]
        bad = plain(ml)
        if bad:
            probs.append('첫 긴 run 길이를 정할 수 없음 (write_restart 체크포인트 · 10-28 KG50-19): 본 덱 그 뒤 %s — 손으로 확인' % bad)
        else:
            sched_cmp(ml, R, ir, '첫 긴 run', 'write_restart 체크포인트', '본 덱 그 뒤', probs, notes)
        # 10-28 밤 (KG50R-03): 그 줄 다음 ~ 첫 긴 run 앞 명령 전체 (판 높이 run 1 · 판 STL · 판 fix …) = 재개 덱 첫 긴 run 앞에 그대로
        pM = ia + 1
    # 뒤 구간 (10-28 KG50R-03 · 예전 E 를 넓힘) — 본 덱 pM ~ 끝 = 재개 덱 q ~ 끝 (첫 긴 run 은 위 D · write 대조가 본다)
    if im > pM:
        # 준비 구간 경계 q = 재개 덱 첫 긴 run 바로 앞 같은 수 명령 (그 꼴이면) · 아니면 재개 덱 read_restart 뒤에서 본 덱 구간을 맞춰 본
        #   첫 명령 자리 (difflib) — 끼워 넣은 · 뺀 명령이 아래 구간 대조에 그대로 보이고 준비 구간 · 상태 대조는 맞는 경계로 돈다
        seg, region = M[pM:im], R[rs[0] + 1:ir]
        tail = region[len(region) - len(seg):] if len(region) >= len(seg) else None
        if tail is not None and all(cmd_eq(a, b) for a, b in zip(seg, tail)):
            q = ir - len(seg)
        else:
            st = next((b for b in difflib.SequenceMatcher(None, seg, region, autojunk=False).get_matching_blocks()
                       if b.a == 0 and b.size > 0), None)
            q = (rs[0] + 1 + st.b) if st is not None else None
        if q is None:
            probs.append('재개 덱에 본 덱 체크포인트 뒤 첫 명령 [%s] 이 없음 — 준비 구간 경계를 못 정함 (10-28 KG50R-03 · 준비 구간 · 상태 대조 건너뜀)'
                         % seg[0])
        else:
            seq_cmp(seg, R[q:ir], W, notes, probs, '체크포인트 뒤 ~ 첫 긴 run 앞 명령')
    seq_cmp(M[im + 1:], R[ir + 1:], W, notes, probs, '첫 긴 run 뒤 명령')
    # 준비 구간 · 상태 (10-28 KG50R-03 · 예전 C 를 넓힘) — 재개 덱 q 앞 (read_restart 빼고) ↔ 본 덱 pM 앞
    if q is not None:
        mprefix_check(M[:pM], probs)
        setup_check([l for i, l in enumerate(R[:q]) if i != rs[0]], M[:pM], probs)
        setup_order([l for i, l in enumerate(R[:q]) if i != rs[0]], M[:pM], probs)
        state_cmp(run_state(M[:pM], '본 덱 체크포인트 앞', probs), run_state(R[:q], '재개 덱 준비 구간', probs), W, notes, probs)
    var_refs(R, probs)
    label_check(M, R, pM, probs)
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


def cut_trial(res, ts, out):
    # 10-28 밤 (KG50R-02 · 05 · 1저자 Q2 (가)): 시험 덱 = 재개 덱 첫 긴 run 앞 원 줄 그대로 + [run min(N, -t)] — 정적 대조와 같은 논리 명령
    # 파서로 자른다 (예전 = 원 줄 단위 awk · & 이음 · run 꼬리를 못 봤다).  첫 긴 run = 꼬리 없는 run N 원 줄 한 줄이 아니면 자르지 않는다.
    # 자른 덱을 다시 읽어 명령 = 재개 덱 첫 긴 run 앞 명령 + [run min(N, -t)] 일 때만 쓴다 (임시 파일 → os.replace).
    # stdout (통과) = 'N 시험run 첫긴run앞run합 원줄' 한 줄 (run 합을 못 세면 '-') · 종료 코드 0 / 거부 = 이유 한 줄 · 1 (시험 덱 안 씀)
    if not re.fullmatch(r'[1-9][0-9]*', ts):
        print('시험 step (-t) 이 1 이상 정수가 아님: %s' % ts)
        return 1
    R = deck(res)
    rr = long_runs(R)
    if not rr:
        print('재개 덱에 긴 run 이 없음')
        return 1
    ir = rr[0]
    why = first_run_form(res, R, ir)
    if why:
        print(why)
        return 1
    n = int(words(R[ir])[1])
    tn = min(n, int(ts))
    spans, raw = deck_spans(res)
    k = spans[ir][1]
    with open(res, 'rb') as f:
        rawb = f.read().split(b'\n')
    if len(rawb) != len(raw):
        print('재개 덱 원 줄 수를 못 맞춤 (줄 끝 꼴 · 10-28 KG50R-05)')
        return 1
    t = out + '.cut'
    try:
        with open(t, 'wb') as f:
            f.write(b''.join(x + b'\n' for x in rawb[:k]) + ('run %d\n' % tn).encode())
        if deck(t) != R[:ir] + ['run %d' % tn]:
            print('잘라 낸 시험 덱 명령 ≠ 재개 덱 첫 긴 run 앞 명령 + [run %d] (10-28 KG50R-05)' % tn)
            return 1
        os.replace(t, out)
    finally:
        if os.path.exists(t):
            os.remove(t)
    rs = [i for i in range(ir) if R[i].split()[0] == 'read_restart']
    ps, ok = 0, True
    for l in R[(rs[-1] + 1) if rs else 0:ir]:
        w = words(l) or ['']
        if w[0] == 'run':
            m, _ = run_n(w)
            if m is None:
                ok = False
            else:
                ps += m
    print('%d %d %s %d' % (n, tn, ps if ok else '-', k + 1))
    return 0


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
if len(sys.argv) == 5 and sys.argv[1] == '--cut-trial':
    try:
        sys.exit(cut_trial(*sys.argv[2:5]))
    except Exception as e:
        print('시험 덱 도구 오류: %s: %s' % (type(e).__name__, e))
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