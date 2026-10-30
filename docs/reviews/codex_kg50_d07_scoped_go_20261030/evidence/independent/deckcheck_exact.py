import difflib, os, re, sys
TMPL = re.compile(r'^(particletemplate/|particledistribution/)')
INS = re.compile(r'^insert/')
MESH = {'mesh/surface/stress', 'mesh/surface'}


class DeckRead(Exception):
    # 10-30 (KG50R-F01 2 판 · 사전 공격 R3): 덱 바이트를 LIGGGHTS 와 같게 읽을 수 없음 — 부르는 쪽이 닫힌 실패로
    pass


CWS = b' \t\n\v\f\r'                 # C isspace (LIGGGHTS Input::file 의 줄 끝 공백)


def uncomment(b):
    # LIGGGHTS 고정판 Input::parse() (input.cpp 354–364 행): 따옴표 밖 첫 # 부터 지움 — 따옴표 안에서 다른 따옴표를 만나면 그 따옴표로
    #   바뀐다 (예전 = 같은 따옴표만 닫음 · 10-30 사전 공격 R3) · 바이트
    q = None
    for i, c in enumerate(b):
        if c == 35 and q is None:
            return b[:i]
        if c == q:
            q = None
        elif c in (34, 39):
            q = c
    return b


def deck_lines(path):
    # 10-30 (KG50R-F01 2 판 · 사전 공격 R3): LIGGGHTS 고정판 Input::file() + parse() 와 같게 읽는다 (예전 = 텍스트 모드 · \r 도 줄 끝 ·
    #   유니코드 공백 · & 이음에 공백 하나 더함 → "#\r…" · "& + NBSP" · "variab&↵le" 가 LIGGGHTS 와 다른 명령이 됐다)
    #   원 줄 = \n 에서만 (fgets) · 줄 끝 C 공백 (" \t\n\v\f\r") 을 빼고 마지막 글자가 & 면 다음 원 줄을 그 & 자리부터 붙인다 (사이 공백 안 넣음) ·
    #   파일 끝 원 줄에 \n 이 없거나 & 이음 중 파일이 끝나면 그 줄을 그대로 (& 도 글자 · LIGGGHTS 와 같음) · 주석 = uncomment()
    #   거부 (DeckRead): 제어 글자 (탭 · 원 줄 끝 \r 말고 · 주석 안이어도) · 주석 밖 비 ASCII (주석 안 한글 = 받음 · 실제 덱 꼴)
    #   → ([(명령 · 처음 원 줄 번호 · 끝 원 줄 번호)], 원 줄 글 목록 (마지막 \n 뒤 빈 줄 포함 = data.split(b'\n')))
    with open(path, 'rb') as f:
        data = f.read()
    phys = data.split(b'\n')
    for k, p in enumerate(phys):
        for j, c in enumerate(p):
            if (c < 32 and c != 9 and not (c == 13 and j == len(p) - 1)) or c == 127:
                raise DeckRead('%d 번째 원 줄에 제어 글자 %r (탭 · 원 줄 끝 \\r 말고 · LIGGGHTS 와 줄 · 낱말 읽기가 갈린다)' % (k + 1, bytes([c])))
    body = phys[:-1] if data.endswith(b'\n') else phys    # 원 줄 (\n 이 있는 것 + 끝에 \n 없는 하나)
    nl = len(phys) - 1                                     # \n 으로 끝난 원 줄 수
    res, line, full, b0 = [], b'', b'', None
    for k, p in enumerate(body):
        if b0 is None:
            b0 = k
        full = line + p
        if k < nl:
            m = len(full)
            while m > 0 and full[m - 1] in CWS:
                m -= 1
            if m > 0 and full[m - 1] == 38:
                line = full[:m - 1]
                continue
            cmd = full[:m]
        else:
            cmd = full                                     # 끝에 \n 없는 원 줄 = 이음 · 끝 공백 빼기 없음 (LIGGGHTS 와 같음)
        line = b''
        res.append((cmd, b0, k))
        b0 = None
    if line:
        res.append((full, b0, len(body) - 1))             # & 이음 중 파일 끝 = 그 줄 그대로 (& 를 글자로)
    out = []
    for cmd, a, z in res:
        c = uncomment(cmd)
        bad = [x for x in c if x > 127]
        if bad:
            raise DeckRead('%d 번째 원 줄%s 주석 밖 비 ASCII 글자 (LIGGGHTS 는 공백 · 낱말로 안 읽음 · 주석 안 한글만 받는다): [%s]' % (
                a + 1, '' if a == z else ' (–%d)' % (z + 1), cmd.decode('utf-8', 'replace')[:120]))
        s = ' '.join(c.decode('ascii').split())
        if s:
            out.append((s, a, z))
    return out, [p.decode('utf-8', 'replace') for p in phys]


def deck(path):
    # 명령 목록 — deck_lines() (LIGGGHTS 줄 읽기 · 못 읽으면 DeckRead)
    return [s for s, _, _ in deck_lines(path)[0]]


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
    w = wpos(s)
    return None if w is None else [t for _, _, t in w]


def wpos(s):
    # words() 의 낱말과 원 줄 자리 — [(시작, 끝, 낱말)] · 따옴표 낱말의 자리 = 따옴표까지 (10-30 KG50R-F01 · 치환 자리 ↔ 인자 대조)
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
            out.append((i, j + 1, s[i + 1:j]))
            i = j + 1
        else:
            j = i
            while j < n and s[j] not in ' \t':
                j += 1
            out.append((i, j, s[i:j]))
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
#     10-30 (KG50R-F01 · Codex KG50RF-01 · 1저자 Q1): 글자 · 순서만으로는 모자라다 — 준비 구간 명령의 그 자리 치환 값 = 두 덱에서 펼쳐
#     글자 같고 상수 · 끝 상태 = 정의 자리 치환을 펼친 줄로 대조 (setup_values · xstate 머리 주석)
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
# 10-30 (KG50R-F01 2 판 · 사전 공격 R1): 상태 표 키 · 분류 자리 (낱말 번호) — 여기에 $ 가 있으면 닫힌 실패 (run_state)
KEYPOS = {'fix': (1, 3), 'unfix': (1,), 'fix_modify': (1,), 'compute': (1,), 'uncompute': (1,), 'compute_modify': (1,), 'dump': (1,),
          'undump': (1,), 'dump_modify': (1,), 'region': (1, 2), 'pair_coeff': (1, 2), 'variable': (1,)}
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
        if c == 'partition' and len(cw) > 3:
            todo.append(cw[3:])                    # 10-30 (사전 공격 R2): partition yes|no N <명령> 의 명령도 (include · next · jump)
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


def run_state(L, where, probs, src=None):
    # 명령 목록이 끝에서 남기는 상태 (10-28 KG50R-03) — 키 → 줄 (… _modify · 쌓이는 꼴은 줄 묶음)
    #   src (10-30 KG50R-F01) = 키 → 그 줄의 L 번호 (쌓이는 꼴은 번호 묶음) — 끝 상태 줄을 정의 자리 치환으로 펼치려고
    st, sx = {}, ({} if src is None else src)

    def put(k, l, i):
        st[k], sx[k] = l, i

    def add(k, l, i):
        st[k], sx[k] = st.get(k, ()) + (l,), sx.get(k, ()) + (i,)

    def drop(k):
        st.pop(k, None)
        sx.pop(k, None)
    for i, l in enumerate(L):
        w = words(l)
        if not w:
            continue
        c, n = w[0], len(w)
        # 10-30 (KG50R-F01 2 판 · 사전 공격 R1): 키 · 분류 자리 (ID · 형 · fix 스타일 · region 꼴 · 변수 이름) 에 $ = 닫힌 실패 — 이 표의 키는
        #   치환 전 글자인데 LIGGGHTS 는 펼친 뒤 읽는다 (fix gx${n} 둘이 한 키 · unfix ${u} 가 아무것도 안 지움 · fix … ${s} 의 삽입 판별)
        kp = [w[x] for x in KEYPOS.get(c, ()) if x < n and '$' in w[x]]
        if kp:
            probs.append('%s 상태 표 키 자리에 그 자리 치환 %s — 끝 상태 키를 줄 순서로 정할 수 없음 (%s R1 · 닫힌 실패 · LIGGGHTS 는 ${x} · $x 를 '
                         '펼친 뒤 ID · 형 · 스타일을 읽는다): [%s]' % (where, ' · '.join(kp), F01P, l))
        if c == 'fix' and n >= 4:
            put(('fix', w[1]), l, i)
            drop(('fix_modify', w[1]))
        elif c == 'unfix' and n >= 2:
            drop(('fix', w[1]))
            drop(('fix_modify', w[1]))
        elif c in ('fix_modify', 'compute_modify', 'dump_modify') and n >= 2:
            add((c, w[1]), l, i)
        elif c == 'compute' and n >= 4:
            put(('compute', w[1]), l, i)
            drop(('compute_modify', w[1]))
        elif c == 'uncompute' and n >= 2:
            drop(('compute', w[1]))
            drop(('compute_modify', w[1]))
        elif c == 'dump' and n >= 2:
            put(('dump', w[1]), l, i)
            drop(('dump_modify', w[1]))
        elif c == 'undump' and n >= 2:
            drop(('dump', w[1]))
            drop(('dump_modify', w[1]))
        elif c == 'variable' and n >= 3:
            if w[2] == 'delete':
                drop(('variable', w[1]))
            elif w[2] in VAR_OK:
                put(('variable', w[1]), l, i)
            else:
                probs.append('%s 에 다룰 수 없는 변수 꼴 %s (equal · atom · string · delete 만 · 10-28 KG50R-03): [%s]' % (where, w[2], l))
        elif c == 'region' and n >= 3:
            if w[2] == 'delete':
                drop(('region', w[1]))
            else:
                put(('region', w[1]), l, i)
        elif c == 'thermo_style':
            put(('thermo_style',), l, i)
            drop(('thermo_modify',))
        elif c == 'thermo':
            put(('thermo',), l, i)
        elif c == 'thermo_modify':
            add(('thermo_modify',), l, i)
        elif c in GLOB1:
            put(('glob', c), l, i)
        elif c in MODS:
            add(('mods', c), l, i)
        elif c == 'pair_coeff' and n >= 3:
            put(('pair_coeff', w[1], w[2]), l, i)
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
                if '$' in nf or '$' in (mesh_file(b, a) or ''):
                    # 10-30 (KG50R-F01 2 판 · 사전 공격 R6): 뒤 구간 판 메시 file 이름에 그 자리 치환 — 펼친 이름으로 있는지 볼 수 없음
                    probs.append('판 메시 file 이름에 그 자리 치환 (%s · %s R6 · 뒤 구간은 펼친 이름을 안 셈 = 닫힌 실패): 본 덱 [%s] ↔ 재개 덱 [%s]'
                                 % (what, F01P, a, b))
                    continue
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


def setup_order(Rs, Mp, probs, ri=None):
    # 10-28 밤 2 (독립 사전 공격 A · KG50R-03 부류): 준비 구간 (read_restart 빼고) = 본 덱 체크포인트 앞 명령의 순서 보존 부분열.
    #   상태 명령 줄은 본 덱 체크포인트 앞에 글자 그대로 있어야 하고 명령 순서 (상태 + 동작) 도 본 덱과 같아야 한다 — LIGGGHTS 는
    #   ${x} 를 그 자리에서 치환하므로 끝 상태 표만 같아서는 안 된다 (변수를 바꿨다 되돌리면 끝 표는 같은데 timestep 은 2 배).
    #   허용 차이 줄: 템플릿 fix (④ · 도구가 read_restart 바로 뒤에 넣는다) = 빼고 본다 · shell mkdir ↔ mkdir -p (③) · 판 메시 fix 의
    #   file 이름 (② · 파일이 있는지는 상태 대조가 본다) = 같은 명령으로 본다
    #   10-30 (KG50R-F01): 돌려주는 값 = 맞춘 짝 [(재개 덱 번호 (ri[n] · 없으면 Rs 번호), 본 덱 번호 (Mp 번호))] — 순서가 깨진 곳 뒤는 없음 ·
    #   그 자리 치환 값 대조 (setup_values) 가 이 짝의 본 덱 자리에서 펼친다 (순서 보존 부분열만으로는 중간 정의를 뺀 덱을 못 막는다)
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

    Mq = [(x, l) for x, l in enumerate(Mp) if not tmpl(l)]
    j, prev, pairs = 0, None, []
    for n, l in enumerate(Rs):
        w = words(l)
        if not w or tmpl(l):
            continue                      # 따옴표 = 다룰 수 없는 구문 · 템플릿 = 상태 대조 (선언하면 같아야)
        if not any(eq(l, m) for _, m in Mq):
            if w[0] in STATE_CMD:
                probs.append('재개 덱 준비 구간 상태 명령이 본 덱 체크포인트 앞에 글자 그대로 없음 (10-28 사전 공격 A · LIGGGHTS 는 '
                             '${x} 를 그 자리에서 치환한다 — 끝 상태만 같아서는 안 된다): [%s]' % l)
            continue                      # 동작 줄은 setup_check 가 이미 거부
        k = j
        while k < len(Mq) and not eq(l, Mq[k][1]):
            k += 1
        if k == len(Mq):
            probs.append('재개 덱 준비 구간 명령 순서가 본 덱 체크포인트 앞 순서와 다름 (10-28 사전 공격 A · 순서 보존 부분열이어야 — '
                         '같은 변수 다시 정의 · fix 순서): [%s] 는 본 덱에서 [%s] 보다 앞에만 있다' % (l, prev or '(처음)'))
            return pairs
        pairs.append((ri[n] if ri is not None else n, Mq[k][0]))
        j, prev = k + 1, l
    return pairs


def part_cmd(l):
    # partition yes|no N <명령> 의 명령 (원 글 · LIGGGHTS Input::partition 은 셋째 낱말 뒤 원 줄을 one() 으로 돈다) — 못 읽으면 ''
    wp = wpos(l)
    return l[wp[2][1]:].strip() if wp is not None and len(wp) > 3 else ''


def mprefix_check(Mp, probs):
    # 본 덱 체크포인트 앞 if = print · quit · jump 만 (그 밖 = 그 시점 상태를 정할 수 없다 · 10-28 KG50R-03)
    #   10-30 (KG50R-F01 2 판 · 사전 공격 R2): run … every · partition 안 명령도 같은 규칙 (예전 = if 만 봐서 run every 안 fix · unfix ·
    #   timestep 이 통과) — 둘 안 jump 도 거부 (restart 체크포인트의 남은 step 셈 · write_restart 의 흐름 줄 검사가 못 보는 자리)
    for l in Mp:
        w = words(l) or ['']
        if w[0] == 'run' and 'every' in w[2:]:
            cs = [x for x in w[w.index('every', 2) + 2:] if x != 'NULL']
            if any((words(c) or [''])[0] not in IFOK for c in cs):
                probs.append('본 덱 체크포인트 앞 run every 에 print · quit 말고 다른 명령 — 그 시점 상태를 정할 수 없음 (%s R2 · if 와 같은 '
                             '규칙 · jump 도 거부): [%s]' % (F01P, l))
            continue
        if w[0] == 'partition':
            if (words(part_cmd(l)) or [''])[0] not in IFOK:
                probs.append('본 덱 체크포인트 앞 partition 에 print · quit 말고 다른 명령 — 그 시점 상태를 정할 수 없음 (%s R2 · if 와 같은 '
                             '규칙 · jump 도 거부): [%s]' % (F01P, l))
            continue
        if w[0] != 'if':
            continue
        cs = if_cmds(w)
        if cs is None or any((words(c) or [''])[0] not in IFOK | {'jump'} for c in cs):
            probs.append('본 덱 체크포인트 앞 if 에 print · quit · jump 말고 다른 명령 — 그 시점 상태를 정할 수 없음 (10-28 KG50R-03): [%s]' % l)


def state_cmp(stM, stR, W, notes, probs, xM=None, xR=None):
    # 재개 지점 상태 (10-28 KG50R-03 · 예전 C 를 넓힘) — 본 덱 체크포인트 시점 ↔ 재개 덱 준비 구간 끝
    #   xM · xR (10-30 KG50R-F01 · 1저자 Q1 (3)) = 같은 키의 줄을 정의 자리의 그 자리 치환으로 펼친 글 (xstate) — 글자가 같아도 펼친 글이
    #   다르면 거부 (변수 · fix · timestep … 상태 표 전부 · 같은 글자 줄이 본 덱에 둘이면 끝 상태 = 뒤 것)
    skip = []
    for k in sorted(set(stM) | set(stR), key=lambda x: tuple(str(y) for y in x)):
        a, b = stM.get(k), stR.get(k)
        what = '재개 지점 ' + kname(k)
        if a == b:
            if xM is not None and xR is not None and xM.get(k) != xR.get(k):
                probs.append('%s 다름 — 그 자리 치환을 펼치면 (%s · 정의 때 값 · LIGGGHTS 는 ${x} · $x 를 그 줄을 읽을 때 치환): 본 덱 %s ↔ '
                             '재개 덱 %s' % (what, F01, xfmt(xM.get(k)), xfmt(xR.get(k))))
            continue
        if b is None and not need(k, a):
            skip.append(kname(k))
            continue
        if isinstance(a, tuple) or isinstance(b, tuple):
            probs.append('%s 다름 (10-28 KG50R-03): 본 덱 %s ↔ 재개 덱 %s' % (what, fmt(list(a or ())), fmt(list(b or ()))))
        elif xM is not None and xR is not None and a and b and mesh_file(a, b) is not None and (isubs(a) or isubs(b)):
            nfx = mesh_file(xM.get(k) or '', xR.get(k) or '')
            if nfx is None:
                # 10-30 (KG50R-F01): 판 메시 file 이름만 다름 허용 = 그 자리 치환을 펼친 줄도 file 이름만 다를 때만
                probs.append('%s 다름 — 판 메시 fix 에 그 자리 치환 (%s · file 이름만 다름 허용은 펼친 줄도 file 이름만 다를 때): 본 덱 %s ↔ '
                             '재개 덱 %s (원 줄 [%s] ↔ [%s])' % (what, F01, xfmt(xM.get(k)), xfmt(xR.get(k)), a, b))
            elif any(c in nfx for c in (VAL0, VAL1, RT0, RT1)):
                probs.append('%s — 판 메시 file 이름을 펼칠 수 없음 (%s R6 · equal 값 · 실행 상태 값 · 못 펼침 = 닫힌 실패): 재개 덱 %s'
                             % (what, F01P, xfmt(xR.get(k))))
            else:
                same_or_mesh(a, b, W, notes, probs, what, nfx)   # 10-30 사전 공격 R6: 작업 폴더에 있는지 = 펼친 이름 (예전 = 치환 전 글자)
        else:
            same_or_mesh(a, b, W, notes, probs, what)
    notes.append('재개 지점 상태 대조 (10-28 KG50R-03): 본 덱 %d 항목 · 재개 덱 %d 항목%s' % (
        len(stM), len(stR), (' · 재개 덱이 다시 선언하지 않음 (선언하면 같아야 하는 것 · 쓰는 곳은 참조 검사): ' + ' · '.join(skip)) if skip else ''))


# ── 10-30 (KG50R-F01 · Codex KG50RF-01 · P1 · 1저자 Q1 "권고대로") 준비 구간이 그 자리에서 쓰는 변수 값 ──
#   LIGGGHTS 는 따옴표 밖 ${x} · $x 를 그 줄을 읽는 순간 x 의 그때 값으로 바꾸고 (equal = 그때 계산한 수 · string = 글) equal 수식 안
#   v_y 는 그 수식을 계산할 때 y 의 그때 정의로 계산한다 (고정판 doc/variable.txt · src/input.cpp Input::substitute ·
#   src/variable.cpp Variable::retrieve).  순서 보존 부분열 · 끝 상태 글자만으로는 중간 정의를 뺀 덱 (본 덱 g 98.1 → 196.2 → fix ${g}
#   → 98.1 · 재개 덱은 196.2 만 뺌 = fix 196.2 ↔ 98.1) · 실행 상태에 따라 바뀌는 수식 (두 덱 같은 98.1*(step+1) = step 1 ↔ 20001) 을
#   못 막는다.
#   ① setup_values — 준비 구간 명령마다 (템플릿 fix · variable 포함 · print · if · shell mkdir 빼고 = 효과가 출력 · 닫힌 실패 quit) 그
#     자리 치환 변수를 두 덱에서 펼친다: 본 덱 = 순서 대조가 맞춘 체크포인트 앞 명령 자리 (템플릿 fix = 본 덱 끝 상태의 그 fix 자리) ·
#     재개 덱 = 그 명령 자리.  펼침 = 그 자리 정의 (정의 안 ${} · $c = 정의 줄 자리 값 · equal 수식의 v_y = 쓰는 자리 정의).  두 펼침의
#     글자가 같고 상수일 때만 통과.  상수 = 수 · + - * / % ^ · == != < <= > >= · 괄호 · 쉼표 · 공백 · sqrt exp ln log abs sin cos tan
#     asin acos atan atan2 ceil floor round · 상수 변수 · string 글.  그 밖 (step · time · dt · atoms 같은 thermo 낱말 · count() ·
#     bound() 같은 group · region 함수 · 원자 값 · c_ · f_ · random · normal · ramp · stagger · logfreq · stride · vdisplace · swiggle ·
#     cwiggle · PI · && || !) = 실행 상태에 따라 바뀌거나 등록 목록 밖 → 거부
#   ② xstate → state_cmp — 끝 상태 대조를 정의 자리 치환으로 펼친 줄로 (변수 · fix · timestep … 상태 표 전부) · 끝 자리 앞에 ③ 의
#     흐름 · 변수 바꾸는 줄이 있으면 끝 상태 변수 표 = 못 정함 (재개 덱이 다시 선언한 변수 = 거부)
#   ③ 펼칠 수 없음 = 거부 (닫힌 실패): $(...) · } 없는 ${ · $ 뒤 이름 글자 아님 · equal · string 밖 변수 꼴 · 정의 없음 · 순환 ·
#     string 값에 공백 · 따옴표 · v_ 로 쓰는 string 이 수 글 아님 · 그 자리 앞의 흐름 · 변수 바꾸는 줄 (label · jump · next · python ·
#     partition · if · run every 안 (겹친 것까지) 그런 줄 · variable · 못 읽는 variable 줄 · variable 이름 · 꼴 자리 치환 — 그 자리
#     값을 줄 순서로 못 정한다)
#   예외 (체크포인트 step 에서 돈 본 덱 명령의 실행 상태 값) 는 두지 않는다 — after_settling 판 높이 블록 (variable plate_z equal
#     ${z_max}+…) 은 write_restart 뒤 = 뒤 구간 (명령 하나하나 대조 · 두 덱 같은 step) 이라 준비 구간이 아니다
#   표기: ⟦…⟧ = equal 값 (그 수식) · ⟨…⟩ = 정의 때 실행 상태 값 · 못 펼침 (두 덱에서 늘 다름)
F01 = '10-30 KG50R-F01'
F01P = '10-30 KG50R-F01 · 사전 공격'                      # 2 판 (독립 사전 공격 R1–R8) 문제 줄 표지
XCAP = 4096                                               # 10-30 사전 공격 R7: 펼친 글 크기 상한 (자) — 넘으면 못 펼침 = 닫힌 실패


def xcap_why(x):
    return ('%s 펼친 글이 %d 자를 넘음 (%s R7 · 닫힌 실패 · LIGGGHTS 는 계산한 수를 넣지만 이 대조는 수식 글을 펼쳐 견준다 — 사슬이 깊으면 '
            '지수로 커진다)' % (x, XCAP, F01P))


VAL0, VAL1, RT0, RT1 = '\x1c', '\x1d', '\x1e', '\x1f'   # 펼친 글의 표지 — deck() 명령에는 없는 글자 (str.split() 이 공백으로 지움)
MATHF = {'sqrt', 'exp', 'ln', 'log', 'abs', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'ceil', 'floor', 'round'}
NUMS = re.compile(r'[0-9.]+([eE][+-]?[0-9]*)?')    # LIGGGHTS Variable::evaluate 의 수 읽기 (숫자 · 점 → e · E [+-] 숫자)
NUMLIT = re.compile(r'[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][+-]?[0-9]+)?')   # v_ 로 쓰는 string 값 = 이 꼴의 수 글만 (LIGGGHTS atof)
FLOWV = {'label', 'jump', 'next', 'python', 'partition'}   # partition yes|no N <명령> = 그 명령을 실행 (파티션 하나면 늘)


def isubs(l):
    # 그 줄을 읽을 때 치환되는 자리 — LIGGGHTS Input::substitute 와 같게 (" · ' 를 따로 뒤집어 둘 다 밖일 때의 $ 만 · 치환한 글은 다시
    #   읽지 않음) → [(시작, 끝, 꼴, 이름)] · 꼴 'v' = ${이름} · $c · '(' = $(...) · 'x' = 못 읽음 (} 없음 · ) 없음 · $ 뒤 이름 글자 아님)
    out, i, n, dq, sq = [], 0, len(l), False, False
    while i < n:
        ch = l[i]
        if ch == '$' and not dq and not sq:
            nx = l[i + 1] if i + 1 < n else ''
            if nx == '{':
                j = l.find('}', i + 2)
                if j < 0:
                    out.append((i, n, 'x', l[i:]))
                    return out
                out.append((i, j + 1, 'v', l[i + 2:j]))
                i = j + 1
            elif nx == '(':
                j, d = i + 2, 0
                while j < n and not (l[j] == ')' and d == 0):
                    d += (l[j] == '(') - (l[j] == ')')
                    j += 1
                if j >= n:
                    out.append((i, n, 'x', l[i:]))
                    return out
                out.append((i, j + 1, '(', l[i:j + 1]))
                i = j + 1
            elif re.fullmatch(r'[A-Za-z0-9_]', nx):
                out.append((i, i + 2, 'v', nx))
                i += 2
            else:
                out.append((i, min(i + 2, n), 'x', l[i:i + 2]))
                i += 2
            continue
        if ch == '"':
            dq = not dq
        elif ch == "'":
            sq = not sq
        i += 1
    return out


def show(t):
    return t.replace(VAL0, '⟦').replace(VAL1, '⟧').replace(RT0, '⟨').replace(RT1, '⟩')


def xfmt(v):
    return '(없음)' if v is None else ' '.join('[%s]' % show(x) for x in (v if isinstance(v, tuple) else (v,)))


def mark_end(t, i):
    # t[i] = VAL0 · RT0 → 짝 표지 다음 자리 (VAL 은 겹칠 수 있음 · RT 안에는 표지 없음)
    if t[i] == RT0:
        return t.index(RT1, i) + 1
    j, d = i + 1, 1
    while d:
        d += (t[j] == VAL0) - (t[j] == VAL1)
        j += 1
    return j


def word_end(t, i):
    j = i
    while j < len(t) and t[j].isascii() and (t[j].isalnum() or t[j] == '_'):
        j += 1
    return j


def bare(t):
    # 표지 (⟦…⟧ · ⟨…⟩) 밖 글자만 — 표지 안 = LIGGGHTS 가 넣는 수 · 실행 상태 값 (공백 · 따옴표 없음)
    out, i = [], 0
    while i < len(t):
        if t[i] in (VAL0, RT0):
            i = mark_end(t, i)
        else:
            out.append(t[i])
            i += 1
    return ''.join(out)


def fwhy(t):
    # 펼친 equal 값이 상수인가 — '' = 상수 · 아니면 첫 까닭 (LIGGGHTS Variable::evaluate 의 읽기: 공백 · 괄호 · 수 · 이름 · 연산자)
    i, n = 0, len(t)
    while i < n:
        ch = t[i]
        if ch == RT0:
            return t[i + 1:mark_end(t, i) - 1]
        if ch == VAL0:
            j = mark_end(t, i)
            w = fwhy(t[i + 1:j - 1])
            if w:
                return w
            i = j
        elif ch in ' ()+-*/%^,':
            i += 1
        elif t[i:i + 2] in ('==', '!=', '<=', '>='):
            i += 2
        elif ch in '<>':
            i += 1
        elif ch in '&|!':
            return '논리 연산자 %s (등록 상수 목록 밖)' % ch
        elif ch.isascii() and (ch.isdigit() or ch == '.'):
            i = NUMS.match(t, i).end()
        elif ch.isascii() and ch.isalpha():
            j = word_end(t, i)
            if t[i:j] in MATHF and t[j:j + 1] == '(':
                i = j
                continue
            return '%s%s (실행 상태 낱말 · 함수 · 등록 상수 목록 밖)' % (t[i:j], '()' if t[j:j + 1] == '(' else '')
        else:
            return '모르는 글자 %r' % ch
    return ''


def expand(x, env, seen=()):
    # 변수 x 의 그 자리 값 (env = 그 자리 변수 표) — (글, 상수가 아니면 그 까닭) · 못 펼치면 (None, 까닭)
    #   string = 정의 글 그대로 (LIGGGHTS 는 그 글을 넣는다) · equal = ⟦수식⟧ (v_y = 이 자리 y 정의로 펼침 · string y 는 수 글만 ·
    #   LIGGGHTS 는 계산한 수를 %.15g 로 넣는다 — 같은 상수 수식이면 같은 수)
    d = env.get(x)
    if d is None:
        return None, '%s 정의 없음' % x
    st, body = d
    if st == 'bad':
        return None, body
    if st == 'string':
        return body, (body[body.index(RT0) + 1:mark_end(body, body.index(RT0)) - 1] if RT0 in body else '')
    if st != 'equal':
        return None, '%s 변수 %s 는 ${} · v_ 로 값 하나가 안 나온다' % (st, x)
    if x in seen or len(seen) > 64:
        return None, '%s 순환 참조' % x
    out, i, n, size = [], 0, len(body), 0
    while i < n:
        if size > XCAP:
            return None, xcap_why(x)              # 10-30 사전 공격 R7: v_ 사슬 (매 단 두 갈래) 이 지수로 커지기 전에 끊는다
        ch = body[i]
        if ch in (VAL0, RT0):
            j = mark_end(body, i)               # 정의 때 넣은 값 — 다시 읽지 않는다
        elif ch.isascii() and (ch.isdigit() or ch == '.'):
            j = NUMS.match(body, i).end()
        elif ch.isascii() and ch.isalpha():
            j = word_end(body, i)
            if body.startswith('v_', i):
                y = body[i + 2:j]
                if body[j:j + 1] == '[':
                    return None, 'v_%s[…] (atom 변수 원자 하나 값 · 지원 안 함)' % y
                dy = env.get(y)
                if dy is not None and dy[0] == 'string':
                    if dy[1][:1] == VAL0 and mark_end(dy[1], 0) == len(dy[1]):
                        out.append(dy[1])           # 정의 때 넣은 equal 값 하나 (수)
                    elif NUMLIT.fullmatch(dy[1]):
                        out.append(VAL0 + dy[1] + VAL1)
                    else:
                        return None, 'v_%s — string 값 [%s] 이 수 글이 아님 (LIGGGHTS 는 atof)' % (y, show(dy[1]))
                else:
                    t, w = expand(y, env, seen + (x,))
                    if t is None:
                        return None, w
                    out.append(t)
                size += len(out[-1])
                i = j
                continue
        else:
            j = i + 1
        out.append(body[i:j])
        size += j - i
        i = j
    if size > XCAP:
        return None, xcap_why(x)
    t = VAL0 + ''.join(out) + VAL1
    return t, fwhy(t)


def sub_text(k, x, raw, env, why0, nm, i):
    # 그 자리 치환 하나 (꼴 k · 이름 x · 원 글 raw) 를 이 자리 (env · 못 정하는 까닭 why0) 에서 펼친 글 — (글, '') · 상수가 아니면 실행
    #   상태 값 표지 (그 덱 · 자리를 담아 두 덱에서 늘 다르다) · 못 펼치면 (None, 까닭)
    if why0:
        return None, why0
    if k == '(':
        return None, '%s 그 자리 식 = 지원 안 함' % raw
    if k == 'x':
        return None, '%s — 치환 이름을 못 읽음 (} · ) 없음 · $ 뒤 이름 글자 아님)' % raw
    t, why = expand(x, env)
    if t is None:
        return None, why
    if why:
        return RT0 + '실행 상태 값 · %s %d 번째 명령의 %s = %s · %s' % (nm, i + 1, raw, show(t), why) + RT1, ''
    if env[x][0] == 'string' and re.search('[ \t"\']', bare(t)):
        return None, '%s — string 값에 공백 · 따옴표 (치환 뒤 낱말이 갈린다 · 지원 안 함)' % raw
    return t, ''


def nested(w):
    # if · run every 안 명령 (겹친 것까지 · unsupported() 와 같은 길) — [낱말 목록] (맨 위 명령은 빼고)
    out, todo, n = [], [w], 0
    while todo and n < 64:
        cw = todo.pop()
        n += 1
        if not cw:
            continue
        cs = []
        if cw[0] == 'if':
            cs = if_cmds(cw) or []
        elif cw[0] == 'run' and 'every' in cw[2:]:
            cs = [x for x in cw[cw.index('every', 2) + 2:] if x != 'NULL']
        for x in cs:
            xw = words(x) or ['']
            out.append(xw)
            todo.append(xw)
    return out


def var_env(L, nm):
    # 명령 목록 L 을 앞에서부터 — [(명령 i 바로 앞 변수 표, 그 자리 펼침을 못 정하는 까닭)] (길이 len(L) + 1 · 끝 = 목록 끝 자리)
    #   표 = 이름 → (꼴, 정의 때 그 자리 치환을 펼친 본문) · 꼴 = equal · string · atom · 'bad' (본문 = 까닭)
    #   까닭 = 그 앞의 흐름 · 변수 바꾸는 줄 (label · jump · next · python · partition · if · run every 안 (겹친 것까지) 그런 줄 ·
    #   variable) · 못 읽는 variable 줄 · 이름 · 꼴 자리 치환 — 그 자리 뒤 전부 (자리 값을 바꾸는 반복은 그 자리 앞 label · 앞으로
    #   건너뛰기는 그 앞 jump 가 있다 · 끝 자리의 까닭 = 끝 상태 변수 표를 못 정함)
    out, env, why = [], {}, ''
    for i, l in enumerate(L):
        out.append((dict(env), why))
        w = words(l)
        if w is None:
            if l.split()[0] == 'variable':
                why = why or '%s %d 번째 명령 variable 줄을 못 읽음 [%s]' % (nm, i + 1, l)
            continue
        if not w:
            continue
        if w[0] in FLOWV or any(x[0] in FLOWV | {'variable'} for x in nested(w)):
            why = why or ('%s 체크포인트 앞 %d 번째 명령이 흐름 줄 · 변수를 바꾸는 줄 [%s] — 그 자리 변수 값을 줄 순서로 정할 수 없음'
                          % (nm, i + 1, l))
        if w[0] != 'variable':
            continue
        wp, subs = wpos(l), isubs(l)
        if len(wp) < 3 or any(s < wp[2][1] for s, _, _, _ in subs):
            why = why or '%s %d 번째 명령 variable 이름 · 꼴 자리를 못 정함 [%s]' % (nm, i + 1, l)
            continue
        x, st = w[1], w[2]
        old = env.get(x)
        if st == 'delete':
            env.pop(x, None)
        elif old is not None and old[0] == 'bad':
            pass                                  # 못 펼치는 변수는 delete 전까지 그대로
        elif st not in ('equal', 'string', 'atom'):
            env[x] = ('bad', '%s 변수 꼴 %s (equal · string 만 펼친다)' % (x, st))
        elif old is not None and old[0] != st:
            env[x] = ('bad', '%s 를 다른 꼴 %s 로 다시 정의 (LIGGGHTS 오류)' % (x, st))
        elif len(wp) != 4:
            env[x] = ('bad', '%s 정의 인자가 %d 개 (하나여야)' % (x, len(wp) - 3))
        elif l[wp[3][0]] in '"\'':
            env[x] = (st, wp[3][2]) if not subs else ('bad', '%s 정의의 따옴표 낱말 안 치환 자리 (낱말 규칙이 LIGGGHTS 와 다름)' % x)
        else:
            body, p, bad = [], wp[3][0], ''
            for s, e, k, y in subs:
                t, bad = sub_text(k, y, l[s:e], env, '', nm, i)
                if t is None:
                    break
                body += [l[p:s], t]
                p = e
            b = ''.join(body) + l[p:wp[3][1]]
            if not bad and len(b) > XCAP:
                bad = xcap_why(x)                  # 10-30 사전 공격 R7: ${} 사슬 (정의 때 치환 · 매 단 두 배) 을 끊는다
            env[x] = ('bad', '%s 정의의 %s' % (x, bad)) if bad else (st, b)
    out.append((dict(env), why))
    return out


def xline(l, ew, nm, i):
    # 줄 l 을 그 자리 (ew = (변수 표, 까닭)) 의 치환으로 펼친 글 — 치환 자리가 없으면 l 그대로 · 못 펼치면 그 자리에 늘 다른 표지
    subs = isubs(l)
    if not subs:
        return l
    out, p = [], 0
    for s, e, k, x in subs:
        t, why = sub_text(k, x, l[s:e], ew[0], ew[1], nm, i)
        out += [l[p:s], t if t is not None else RT0 + '못 펼침 · %s %d 번째 명령의 %s — %s' % (nm, i + 1, l[s:e], show(why)) + RT1]
        p = e
    return ''.join(out) + l[p:]


def xstate(L, src, envs, nm):
    # 끝 상태 표 (run_state 의 src = 키 → 줄 번호) 의 줄을 정의 자리 치환으로 펼친 글 — 키 → 글 (쌓이는 꼴 = 글 묶음)
    #   변수는 끝 자리 (envs[-1]) 에 까닭이 있으면 (그 앞 run every · if · partition 안 variable · 흐름 줄 …) 끝 상태 표를 줄 순서로 못 정한다
    #   → 늘 다른 표지 (재개 덱이 다시 선언하면 거부 · 뒤 구간이 쓰는 값이 달라질 수 있다)
    def one(i):
        return xline(L[i], envs[i], nm, i)
    endwhy = envs[-1][1]
    return dict((k, (RT0 + '못 정함 · %s 끝 상태 변수 표를 줄 순서로 정할 수 없음 — %s' % (nm, show(endwhy)) + RT1)
                 if (k[0] == 'variable' and endwhy) else (tuple(one(i) for i in v) if isinstance(v, tuple) else one(v)))
                for k, v in src.items())


def setup_values(R, ri, pairs, tpl, eM, eR, notes, probs):
    # ① 준비 구간 명령의 그 자리 치환 값 (규칙 = 위 머리 주석) — ri = 재개 덱 준비 구간 명령 번호 · pairs = 순서 대조가 맞춘
    #   (재개 번호, 본 번호) · tpl = 템플릿 fix 재개 번호 → 본 덱 끝 상태의 그 fix 번호 · eM · eR = var_env
    mp, n0 = dict(pairs), len(probs)
    mp.update(tpl)
    nc = ns = 0
    for i in ri:
        l = R[i]
        w = words(l)
        if not w or w[0] in ('print', 'if') or mkdir_key(w) is not None:
            continue                      # print · if (print · quit 만) · shell mkdir = 값 대조 밖 (효과 = 출력 · 닫힌 실패 quit)
        subs = isubs(l)
        if not subs or mp.get(i) is None:
            continue                      # 본 덱에 맞춘 명령이 없으면 = 순서 · 상태 대조가 이미 거부
        mi = mp[i]
        nc += 1
        for s, e, k, x in subs:
            ns += 1
            raw = l[s:e]
            em, wm = sub_text(k, x, raw, eM[mi][0], eM[mi][1], '본 덱', mi)
            er, wr = sub_text(k, x, raw, eR[i][0], eR[i][1], '재개 덱', i)
            if em is None or er is None:
                probs.append('준비 구간 그 자리 치환을 펼칠 수 없음 (%s · 닫힌 실패): [%s] 의 %s — %s' % (
                    F01, l, raw, ('본 덱: ' + show(wm)) if em is None else ('재개 덱: ' + show(wr))))
            elif RT0 in er or RT0 in em:
                probs.append('준비 구간 그 자리 치환 값이 상수가 아님 — 실행 상태에 따라 바뀜 · 등록 상수 목록 밖 (%s · 상수 = 수 · 연산자 · 괄호 · '
                             '정해진 수학 함수 · 상수 변수 · string 글): [%s] 의 %s — 본 덱 %s ↔ 재개 덱 %s' % (F01, l, raw, show(em), show(er)))
            elif em != er:
                probs.append('준비 구간 그 자리 치환 값이 본 덱과 다름 (%s · LIGGGHTS 는 ${x} · $x 를 그 줄을 읽을 때 치환): [%s] 의 %s — '
                             '본 덱 (%d 번째 명령 자리) %s ↔ 재개 덱 (%d 번째 명령 자리) %s' % (F01, l, raw, mi + 1, show(em), i + 1, show(er)))
    if nc and len(probs) == n0:
        notes.append('그 자리 치환 대조 (%s): 명령 %d 개 · 치환 %d 곳 = 두 덱 같은 상수 값' % (F01, nc, ns))


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
    # 판 메시 fix 둘이 file 이름만 다르면 b 의 file 이름 · 아니면 None — 낱말 = 공백 · 탭에서만 (10-30 사전 공격 R6: 펼친 글의 표지
    #   \x1c–\x1f 를 str.split() 은 공백으로 봐 낱말을 가른다)
    ta, tb = re.split('[ \t]+', a.strip(' \t')), re.split('[ \t]+', b.strip(' \t'))
    if (len(ta) != len(tb) or len(ta) < 6 or ta[0] != 'fix' or ta[3] not in MESH
            or 'file' not in ta or 'file' not in tb or ta.index('file') != tb.index('file')):
        return None
    i = ta.index('file')
    if i + 1 >= len(ta) or ta[:i + 1] != tb[:i + 1] or ta[i + 2:] != tb[i + 2:]:
        return None
    return tb[i + 1]


def same_or_mesh(a, b, W, notes, probs, what, nfx=None):
    # nfx (10-30 사전 공격 R6) = 펼친 file 이름 (그 자리 치환이 있을 때 · 작업 폴더에 있는지는 이 이름으로)
    if a == b:
        return
    nf = nfx if nfx is not None else (mesh_file(a, b) if (a and b) else None)
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


FLOW5 = {'label', 'jump', 'clear', 'python'}


def flow_before_write(Mp, probs):
    # 10-30 (KG50R-F01 2 판 · 사전 공격 R5): write_restart 체크포인트 앞 label · jump · clear · python (맨 위 · if · run every 안 · partition 안은
    #   mprefix_check 가 print · quit 만 받는다) =
    #   체크포인트 시점 상태 표를 줄 순서로 정할 수 없음 (닫힌 실패) — restart 체크포인트는 남은 step 셈이 이미 거부한다 (예전 = write_restart 꼴은
    #   변수 표만 못 정함 · 변수 없는 상태 (fix …) 는 줄 순서대로 읽어 jump 가 건너뛴 · clear 가 지운 fix 가 남은 것으로 보였다)
    for l in Mp:
        w = words(l) or ['']
        hit = [x[0] for x in [w] + nested(w) if x and x[0] in FLOW5]
        if hit:
            probs.append('본 덱 write_restart 체크포인트 앞 흐름 줄 %s — 체크포인트 시점 상태 표를 줄 순서로 정할 수 없음 (%s R5 · 닫힌 실패): [%s]'
                         % (' · '.join(sorted(set(hit))), F01P, l))


def print_file_reads(L, n, nm, probs):
    # 10-30 (KG50R-F01 2 판 · 사전 공격 R4 · 1저자 결정 대기 — 그때까지 닫힌 실패): 재개 덱 준비 구간 (L[:n]) 의 print … file|append <이름> 으로
    #   쓴 파일을 그 뒤 명령 (print 말고 · 준비 · 뒤 구간) 이 읽음 — print 의 그 자리 치환 값은 대조 밖 (규칙 (5)) 이라 재개 덱이 쓴 파일 글이
    #   본 덱과 다를 수 있다 (판 STL 을 준비 구간에서 쓰고 mesh fix 가 읽는 꼴).  이름에 $ · 읽는 쪽 file 이름에 $ = 정할 수 없음 = 같은 거부.
    #   본 덱은 보지 않는다 — 본 덱이 제 준비 구간에서 쓰고 읽는 파일 (압축 루프 체크포인트 앞 판 STL 같은) 은 본 덱 자신의 이력이다
    seen = set()
    for i in range(min(n, len(L))):
        w = words(L[i]) or ['']
        if w[0] != 'print':
            continue
        for t in [w[k + 1] for k in range(2, len(w) - 1) if w[k] in ('file', 'append')]:
            if t in seen:
                continue
            for j in range(i + 1, len(L)):
                wj = words(L[j]) or ['']
                if wj[0] == 'print':
                    continue
                dyn = '$' in t or any(wj[k] == 'file' and '$' in wj[k + 1] for k in range(1, len(wj) - 1))
                if t in wj[1:] or dyn:
                    seen.add(t)
                    probs.append('%s 준비 구간 print file/append 로 쓴 파일 %s 를 뒤 명령이 읽음 — print 의 그 자리 치환 값은 대조 밖 (%s R4 · 1저자 결정 '
                                 '대기 · 닫힌 실패): [%s] → [%s]' % (nm, t, F01P, L[i], L[j]))
                    break


def check(main, res, ckpt, s0, W):
    # 10-28 밤 (KG50R-01 · 02 · 03 · 05 · 1저자 Q2 (가) · Q3 (가)) — 전체 프로그램 대조 (규칙 = 위 STATE_CMD 머리 주석)
    #   예전 B (물리 줄이 본 덱 어딘가에) · C (fix · 쌍 · 이웃 · timestep 만) · E (fix · run · if … 만 순서) = 아래 상태 · 구간 대조가 대신한다
    #   10-30 (KG50R-F01 2 판 · 사전 공격 R3): 덱을 LIGGGHTS 와 같게 읽을 수 없으면 (제어 글자 · 주석 밖 비 ASCII) 대조 전에 닫힌 실패
    rd = []
    for nm, p in (('본 덱', main), ('재개 덱', res)):
        try:
            deck(p)
        except DeckRead as e:
            rd.append('덱 바이트를 LIGGGHTS 와 같게 읽을 수 없음 (%s R3 · 닫힌 실패): %s %s' % (F01P, nm, e))
    if rd:
        return rd, []
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
        flow_before_write(M[:pM], probs)          # 10-30 사전 공격 R5
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
        print_file_reads(R, q, '재개 덱', probs)  # 10-30 사전 공격 R4
        ri = [i for i in range(q) if i != rs[0]]
        setup_check([R[i] for i in ri], M[:pM], probs)
        pairs = setup_order([R[i] for i in ri], M[:pM], probs, ri)
        sM, sR = {}, {}
        stM, stR = run_state(M[:pM], '본 덱 체크포인트 앞', probs, sM), run_state(R[:q], '재개 덱 준비 구간', probs, sR)
        # 10-30 (KG50R-F01 · 1저자 Q1): 그 자리 치환 값 — 템플릿 fix (순서 대조 밖) 의 본 덱 자리 = 본 덱 끝 상태의 그 fix 줄 (글자 같을 때만)
        tpl = {}
        for i in ri:
            w = words(R[i]) or []
            mi = sM.get(('fix', w[1])) if len(w) >= 4 and w[0] == 'fix' and TMPL.match(w[3]) else None
            if isinstance(mi, int) and M[mi] == R[i]:
                tpl[i] = mi
        eM, eR = var_env(M[:pM], '본 덱'), var_env(R[:q], '재개 덱')
        setup_values(R, ri, pairs, tpl, eM, eR, notes, probs)
        state_cmp(stM, stR, W, notes, probs, xstate(M, sM, eM, '본 덱'), xstate(R, sR, eR, '재개 덱'))
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
    # deck() 와 같은 규칙으로 명령을 만들고, 명령마다 그 명령을 이룬 원 줄 번호 (처음 · 끝) 를 함께 낸다 (10-30 사전 공격 R3: 같은 deck_lines())
    return deck_lines(path)


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
