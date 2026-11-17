#!/usr/bin/env python3
"""Rint ② 봉인본 만들기 — 핀 판 원본 등록 R + 붙일 글 (조각) + 계획 파일 → 봉인본 바이트 (기계로 · 사람이 블록 · 해시를 옮겨 적지 않는다).

    python3 -I make_sealed_copy.py --pin-reg <원본 등록 R> --pin-cmd <원본 kgy 명령 문서> \
        --reg-insert registration_R_insert.md --cmd-insert commands_doc_insert.md \
        --plan <봉인 계획 JSON> --s0-plan <S0 계획 JSON> --chain <핀 판 scripts/rint_r_chain.py> \
        --seal-date 20261120 [--seal-branch <가지>] [--final] --out <없거나 빈 폴더>
    python3 -I make_sealed_copy.py --selftest --chain <핀 판 scripts/rint_r_chain.py>

--final = 봉인 때 필수 (결과 전 등록 넷이 다 채워져야 · 핀 판 사슬 `require_plan_numbers` 와 같은 판정) · 없으면 후보 (넷 null 도 만든다 ·
_manifest.json `seal_status` = "후보 · 봉인 값 아님").

낸 것 (<out> 아래 · 리포 상대 자리 그대로):
  docs/reviews/rint2_seal_<날짜>/registration_R_sealed.md   = 원본 + R-00 · R-01 – R-15 (봉인본 · 새 파일)
  docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md = 원본 + R-MARK 한 줄 (봉인 전 판 · 해시 칸 ⬜ 그대로)
  docs/reviews/rint2_kgy_commands_20261020.md               = 원본 + K 조각
  docs/data/rint2_r_plan_<날짜>/ca1_plan.json               = 계획 파일 바이트 그대로
  _manifest.json (리포 밖 · 입력 · 출력 sha256 · 조각 · 남은 자리표 · 확인 · seal_status)
같은 입력 바이트 · 같은 인자 = 같은 바이트 (시각 · 경로 · 입력 파일 이름을 출력에 넣지 않는다 · v2.1).  리포 · 네트워크 · σ 없음 ·
쓰는 곳 = `--out` (만드는 동안 그 옆 `.msc_out_*` 임시 폴더 → 다 쓰면 이름 바꿈 · 실패면 지움) + 시스템 임시 폴더 (`msc_*` · `msc_chk_*` =
사슬 plan-doc 실행 · 대조 · 끝나면 지움 · 자기 시험 = `msc_selftest_*`).
조각 꼴 = 붙일 글 머리 (`@op <꼴> <원본 줄> <그 줄의 첫 글자들>` + `====` 사이 그대로).  확인 (하나라도 아니면 rc 2 · 아무것도 쓰지 않는다):
  입력 원본 · 사슬 = 핀 blob sha256 · 자리 줄 = 원본에 하나 · 그 줄 번호 · 조각 = @op 하나 · 꼴마다 블록 수 · 도구 자리표 다 채움 ·
  봉인본 = 원본 줄을 순서대로 다 갖고 (지움 없음) 바뀐 줄 = last · mid+last 자리뿐 · 블록 = 사슬 `--stage plan-doc` 출력 = `plan_doc_block` ·
  사슬 `registration_plan_hash` = 계획 sha256 · `registration_s0_hash` = S0 계획 sha256 · `plan_doc_problem` None · 자리 줄 글자 하나 ·
  원본 자리 = 원본 + 한 줄 (표지 = 해시 줄 머리 · 블록 표지 · 자리 줄 글자 없음 · 봉인본 자리 글자 있음) · 사슬 기본 경로 = PLAN_HASH_UNREGISTERED ·
  명령 문서의 ```bash 블록 = 주석 줄만 늘어남 (시험 K01 이 읽는 인자 그대로) · 블록 표지 없음.
v2.1 (11-17 · 내부 반박 리뷰 P2-2 · P3-4 · P3-12 · Codex 아님) 더 본다: 계획 바이트 = Q3 꼴 (`json.dumps(…, indent=1, sort_keys=True)` · ASCII ·
  끝 줄바꿈 없음) · 두 계획 대조 (핀 사슬 `plans_cross_problems(계획, S0 계획) == []` · S0 계획 = 엄격 JSON) · `--final` 이면 결과 전 넷 ·
  조각 이름 집합 = 고정 (R-MARK · R-00 – R-15 · K-01 – K-05) · 빈 블록 없음 · last · mid+last 블록 = 한 줄 · `|` 없음 ·
  남은 자리표 = 허용 목록 · 날짜 = 달력 날짜 (`datetime.strptime`) · 가지 = git 가지 이름 규칙 (`.lock` 끝 · `//` · `.` 시작 성분 · `@{` 등 거부).
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PIN = '64e4d213e8267bafaf3ae5af00a42996cefd3f33'
REG_REL = 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md'
CMD_REL = 'docs/reviews/rint2_kgy_commands_20261020.md'
#: 핀 blob sha256 (git show 64e4d213e:<경로> | sha256sum · 11-17 실측)
EXPECT = {'reg': '219b63514d8c594d1f96bf7ce610ff9e9bc59dd3482616883475e36fee112bf2',
          'cmd': '0fe96bb83bf0795a4f1f18e2e1968ba8dacbad3f8ace84f97828d407703fe983',
          'chain': '5fbc1c3417f17eba9bc9e569a9dad28f569ed1eedb64f8fcdd725492854de78b'}
ROW_PLAN, ROW_S0 = '| 계획 해시 |', '| S0 계획 해시 |'
ANCHOR = '계획 숫자 블록 = 이 줄 바로 아래'      # 시험 고정물 PLAN_DOC_ANCHOR (scripts/test_rint_r_chain.py @64e4d213e)
KINDS = {'last': 1, 'mid+last': 2, 'after': 1, 'before': 1}
OP_RE = re.compile(r'^@op (last|mid\+last|after|before) ([1-9][0-9]*) (.+)$')
HEAD_RE = re.compile(r'^## ((?:R|K)-(?:[0-9]{2}|MARK)) · ')
DATE_RE = re.compile(r'^20[0-9]{6}$')
BRANCH_RE = re.compile(r'^[A-Za-z0-9._][A-Za-z0-9._/-]*$')
PH_DATE, PH_SEALED, PH_PLAN, PH_BLOCK, PH_BRANCH = '<봉인 날짜>', '<봉인본>', '<봉인 계획 sha256>', '<계획 숫자 블록>', '<봉인 가지>'
TOOL_PH = (PH_DATE, PH_SEALED, PH_PLAN, PH_BLOCK)
PH_RE = re.compile(r'<[^<>\n]{1,60}>')
BASH_FENCE = '```bash'
#: 조각 이름 집합 (v2.1 고정 · 하나라도 빠지거나 더 있으면 거부 — 리뷰 P3-4 A15)
FRAG_SETS = (frozenset(['R-MARK'] + [f'R-{i:02d}' for i in range(16)]), frozenset(f'K-0{i}' for i in range(1, 6)))
#: 도구가 채우지 않고 남기는 자리표 허용 목록 (실행 때 화면 값 · 글 속 이름 꼴 — 그 밖 = 거부 · 리뷰 P3-4 A17)
ALLOWED_PH = frozenset(['<HOME>', '<P0 채택 번호>', '<P1 채택 번호>', '<R 역할>', '<T_DBE>', '<T_first>', '<T_hit>', '<UTC 시각>', '<c>',
                        '<ladder:P0 항목 번호>', '<n>', '<point:P0_c0_R_j0 항목 번호>', '<predict 항목 번호>', '<unit:P0_c0_R_j0 항목 번호>', '<…>',
                        '<가지>', '<그 시도 폴더>', '<기계>', '<기존 트리>', '<날짜>', '<넘김 기록 시각>', '<넘김 기록의 원장 끝 커밋>', '<묶음>', '<받는>',
                        '<법칙>', '<보낸>', '<봉인 가지>', '<봉인 커밋>', '<시도 번호>', '<시도 폴더>', '<열쇠>', '<원장 가지>', '<이름>', '<팔>',
                        '<확인한 것 · 한 줄>'])
SEAL_STATUS = {False: '후보 · 봉인 값 아님 (--final 없음 · 결과 전 등록 넷 null 이어도 만든다 · 봉인 때 --final 로 다시)',
               True: 'final (--final · 결과 전 등록 넷 채움 = 핀 사슬 require_plan_numbers 통과)'}


class Fail(Exception):
    pass


def sha(b):
    return hashlib.sha256(b).hexdigest()


def need(cond, msg):
    if not cond:
        raise Fail(msg)


# ── 붙일 글 읽기 ────────────────────────────────────────────────────────────────────────────────
def parse_insert(text, name):
    frags, order, cur, inseg, buf = {}, [], None, False, []
    for no, ln in enumerate(text.split('\n'), 1):
        if inseg:
            if ln == '====':
                frags[cur]['blocks'].append('\n'.join(buf))
                buf, inseg = [], False
            else:
                buf.append(ln)
            continue
        m = HEAD_RE.match(ln)
        if m:
            cur = m.group(1)
            need(cur not in frags, f'{name}:{no} 조각 {cur} 이 둘')
            frags[cur] = {'op': None, 'blocks': []}
            order.append(cur)
            continue
        need(not ln.startswith('## '), f'{name}:{no} 조각 머리 꼴이 아닌 ## 줄 ({ln[:40]!r})')
        if ln == '====':
            need(cur is not None, f'{name}:{no} 조각 밖 ====')
            inseg = True
            continue
        if ln.startswith('@op'):
            need(cur is not None, f'{name}:{no} 조각 밖 @op')
            mo = OP_RE.match(ln)
            need(mo is not None, f'{name}:{no} @op 꼴 ({ln[:60]!r})')
            need(frags[cur]['op'] is None, f'{name}:{no} {cur} 의 @op 가 둘')
            frags[cur]['op'] = (mo.group(1), int(mo.group(2)), mo.group(3))
    need(not inseg, f'{name}: 닫히지 않은 ====')
    for k in order:
        f = frags[k]
        need(f['op'] is not None, f'{name}: {k} 에 @op 가 없다')
        need(len(f['blocks']) == KINDS[f['op'][0]], f'{name}: {k} ({f["op"][0]}) 블록 {len(f["blocks"])} 개 ≠ {KINDS[f["op"][0]]}')
        need(all(b.strip() for b in f['blocks']), f'{name}: {k} 빈 블록 (빈칸 · 빈 줄만)')
        if f['op'][0] in ('last', 'mid+last'):
            need(all('\n' not in b and '|' not in b for b in f['blocks']), f'{name}: {k} ({f["op"][0]}) 표 칸 글 = 한 줄 · `|` 없음 (새 줄 · 새 칸이 생긴다)')
    return frags, order


def fill(t, subs):
    for k, v in subs.items():
        t = t.replace(k, v)
    return t


# ── 조각 넣기 ──────────────────────────────────────────────────────────────────────────────────
def last_cell_split(line):
    head, sep, tail = line.rstrip().rpartition(' | ')
    need(bool(sep) and tail.endswith('|'), f'표 줄 꼴이 아니다 ({line[-40:]!r})')
    return head, tail[:-1].strip()


def apply_ops(pin_text, ops, label):
    """ops = [(조각, 꼴, 원본 줄, 머리 글자, [채운 블록])] → (글, 기록).  원본 줄 = 1 부터 · 아래 줄부터 넣는다 (위 줄 번호 그대로)."""
    pin = pin_text.split('\n')
    lines, tags = list(pin), list(range(len(pin)))
    rec, seen_line = [], set()
    for fid, kind, n, prefix, blocks in sorted(ops, key=lambda o: -o[2]):
        hit = [i for i, l in enumerate(pin) if l.startswith(prefix)]
        need(len(hit) == 1, f'{label} {fid}: 머리 글자 {prefix[:40]!r} 로 시작하는 원본 줄 = {len(hit)} 개 (하나여야)')
        need(hit[0] + 1 == n, f'{label} {fid}: 자리 줄 = 원본 {hit[0] + 1} 줄 ≠ 적은 {n} 줄')
        need(n not in seen_line, f'{label} {fid}: 원본 {n} 줄에 조각이 둘')
        seen_line.add(n)
        i = tags.index(hit[0])
        old = lines[i]
        if kind in ('last', 'mid+last'):
            head, cell = last_cell_split(old)
            if kind == 'last':
                need('⬜' in cell and '~~⬜~~' in blocks[0], f'{label} {fid}: 끝 칸 = ⬜ 칸이어야 하고 새 글은 ~~⬜~~ 로 옛 값을 남긴다')
                lines[i] = head + ' | ' + blocks[0] + ' |'
            else:
                need(cell == '⬜', f'{label} {fid}: 끝 칸 {cell!r} ≠ ⬜')
                need(re.fullmatch(r'`[0-9a-f]{64}`', blocks[1]) is not None, f'{label} {fid}: 새 끝 칸 = 백틱 한 쌍 안 64 자 hex 하나')
                lines[i] = head + blocks[0] + ' | ' + blocks[1] + ' |'
            rec.append({'id': fid, 'kind': kind, 'line': n, 'inserted': 0, 'old_last_cell': cell})
        else:
            new = blocks[0].split('\n')
            at = i + 1 if kind == 'after' else i
            lines[at:at] = new
            tags[at:at] = [None] * len(new)
            rec.append({'id': fid, 'kind': kind, 'line': n, 'inserted': len(new)})
    # 되살림 대조 — 원본 줄이 순서대로 다 있고 (지움 없음) 바뀐 줄 = last · mid+last 자리뿐 (머리 글 그대로)
    kept = [(t, lines[k]) for k, t in enumerate(tags) if t is not None]
    need([t for t, _ in kept] == list(range(len(pin))), f'{label}: 원본 줄 순서 · 수가 다르다')
    cell_lines = {o[2] - 1 for o in ops if o[1] in ('last', 'mid+last')}
    for t, l in kept:
        if t in cell_lines:
            need(l.startswith(last_cell_split(pin[t])[0]), f'{label}: 원본 {t + 1} 줄의 머리 글이 바뀌었다')
        else:
            need(l == pin[t], f'{label}: 원본 {t + 1} 줄이 바뀌었다 (넣기 꼴이 아닌 바뀜)')
    return '\n'.join(lines), sorted(rec, key=lambda r: r['line'])


def bash_body(text):
    """```bash 블록의 주석 아닌 줄 (시험 K01 `doc_tool_commands` 와 같은 울타리 셈: 울타리 줄마다 inb = (not inb) and ```bash) ·
    bash 블록 끝마다 '```' 한 줄 — 주석 줄을 더하거나 sh 블록을 더해도 같아야 한다."""
    out, inb = [], False
    for ln in text.split('\n'):
        s = ln.strip()
        if s.startswith('```'):
            was, inb = inb, (not inb) and s.startswith(BASH_FENCE)
            if was and not inb:
                out.append('```')
            continue
        if inb and s and not s.startswith('#'):
            out.append(ln)
    return out


# ── 사슬 (핀 판) ──────────────────────────────────────────────────────────────────────────────
_CHAINS = {}


def load_chain(path):
    key = os.path.abspath(path)
    if key in _CHAINS:
        return _CHAINS[key]
    d = os.path.dirname(key)
    sys.path.insert(0, d)
    try:
        spec = importlib.util.spec_from_file_location('rint_r_chain', path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules['rint_r_chain'] = mod
        spec.loader.exec_module(mod)
    finally:
        if sys.path and sys.path[0] == d:
            sys.path.pop(0)
    _CHAINS[key] = mod
    return mod


def chain_block(chain, plan_path, R):
    """블록 = 핀 사슬 `--stage plan-doc --plan <계획>` 의 화면 그대로 (끝 줄바꿈 하나 뺌) · 같은 계획으로 `plan_doc_block` 도 불러 같은지."""
    with tempfile.TemporaryDirectory(prefix='msc_') as td:
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', os.path.abspath(chain), '--stage', 'plan-doc', '--plan',
                            os.path.abspath(plan_path)], cwd=td, capture_output=True)
    need(r.returncode == 0, f'사슬 plan-doc rc {r.returncode} · {r.stdout.decode("utf-8", "replace")[-200:]} {r.stderr.decode("utf-8", "replace")[-200:]}')
    out = r.stdout.decode('utf-8')
    need(out.endswith('\n') and not out.endswith('\n\n'), '사슬 plan-doc 출력 끝 줄바꿈이 하나가 아니다')
    blk = out[:-1]
    plan, _sha = R.load_plan(plan_path)
    need(blk == R.plan_doc_block(plan), '사슬 plan-doc 화면 ≠ plan_doc_block(load_plan(계획))')
    need(blk.startswith(R.PLAN_DOC_BEGIN) and blk.endswith(R.PLAN_DOC_END), '블록 표지 꼴')
    return blk, plan


def count_rows(text, prefix):
    return sum(1 for ln in text.splitlines() if ln.startswith(prefix))


def branch_ok(b):
    """git 가지 이름 규칙 (git check-ref-format 의 쓰는 부분) — 글자 = BRANCH_RE · `..` · `//` · `@{` 없음 · `/` · `.` 로 끝나지 않음 ·
    성분이 `.` 로 시작하거나 `.lock` 으로 끝나지 않음 · `@` 하나만이 아님."""
    if BRANCH_RE.fullmatch(b) is None or '..' in b or '//' in b or '@{' in b or b == '@' or b.endswith('/') or b.endswith('.'):
        return False
    return all(c and not c.startswith('.') and not c.endswith('.lock') for c in b.split('/'))


# ── 만들기 ──────────────────────────────────────────────────────────────────────────────────────
def build(a, expect=EXPECT):
    raw = {k: open(p, 'rb').read() for k, p in (('reg', a.pin_reg), ('cmd', a.pin_cmd), ('chain', a.chain), ('plan', a.plan),
                                                ('s0', a.s0_plan), ('reg_ins', a.reg_insert), ('cmd_ins', a.cmd_insert))}
    for k in ('reg', 'cmd', 'chain'):
        if expect and k in expect:
            need(sha(raw[k]) == expect[k], f'입력 {k} sha256 {sha(raw[k])[:16]}… ≠ 핀 blob {expect[k][:16]}…')
    need(DATE_RE.fullmatch(a.seal_date or '') is not None, f'--seal-date = 8 자리 (예 20261120) · {a.seal_date!r}')
    try:
        datetime.datetime.strptime(a.seal_date, '%Y%m%d')
    except ValueError:
        raise Fail(f'--seal-date = 달력 날짜 (YYYYMMDD) · {a.seal_date!r}') from None
    if a.seal_branch is not None:
        need(branch_ok(a.seal_branch), f'--seal-branch 글자 · git 가지 이름 규칙 · {a.seal_branch!r}')
    final = bool(getattr(a, 'final', False))
    pin_reg, pin_cmd = raw['reg'].decode('utf-8'), raw['cmd'].decode('utf-8')
    for k in TOOL_PH + (PH_BRANCH,):
        need(k not in pin_reg and k not in pin_cmd, f'원본에 도구 자리표 {k} 가 이미 있다')
    R = load_chain(a.chain)
    try:
        plan_obj = R._json_strict(raw['plan'], 'ascii')
        canon = json.dumps(plan_obj, indent=1, sort_keys=True).encode('ascii')
    except (UnicodeError, ValueError) as e:
        raise Fail(f'계획 파일 = Q3 꼴 (ASCII 엄격 JSON) 이 아니다 · {type(e).__name__}: {e}') from None
    need(raw['plan'] == canon, f'계획 파일 바이트 ≠ Q3 꼴 (json.dumps(indent=1, sort_keys=True) · ASCII · 끝 줄바꿈 없음) · {len(raw["plan"])} B ≠ {len(canon)} B')
    sealed_rel = f'docs/reviews/rint2_seal_{a.seal_date}/registration_R_sealed.md'
    plan_rel = f'docs/data/rint2_r_plan_{a.seal_date}/ca1_plan.json'
    plan_sha, s0_sha = sha(raw['plan']), sha(raw['s0'])
    blk, plan = chain_block(a.chain, a.plan, R)
    try:
        s0_obj = R._json_strict(raw['s0'], 'ascii')
    except (UnicodeError, ValueError) as e:
        raise Fail(f'S0 계획 = ASCII 엄격 JSON 이 아니다 · {type(e).__name__}: {e}') from None
    cdir = os.path.dirname(os.path.abspath(a.chain))
    sys.path.insert(0, cdir)
    try:
        cross = R.plans_cross_problems(plan, s0_obj)
    finally:
        if sys.path and sys.path[0] == cdir:
            sys.path.pop(0)
    need(cross == [], f'두 계획 대조 (핀 사슬 plans_cross_problems · 계획 ↔ S0 계획) 문제: {cross}')
    if final:
        try:
            R.require_plan_numbers(plan)
        except R.Stop as e:
            raise Fail(f'--final: {e.code} — {e.cause}') from None
    subs = {PH_SEALED: sealed_rel, PH_DATE: a.seal_date, PH_PLAN: plan_sha}
    if a.seal_branch is not None:
        subs[PH_BRANCH] = a.seal_branch
    rf, rorder = parse_insert(raw['reg_ins'].decode('utf-8'), 'registration_R_insert')
    cf, corder = parse_insert(raw['cmd_ins'].decode('utf-8'), 'commands_doc_insert')
    need('R-MARK' in rf and 'R-07' in rf, '등록 조각에 R-MARK · R-07 이 있어야')
    for nm, got, want in (('등록', set(rorder), FRAG_SETS[0]), ('명령', set(corder), FRAG_SETS[1])):
        need(got == set(want), f'{nm} 조각 이름 집합 ≠ 고정 집합 — 빠짐 {sorted(set(want) - got)} · 더 있음 {sorted(got - set(want))}')
    need(all(k.startswith('R-') for k in rorder) and all(k.startswith('K-') for k in corder), '조각 이름 접두 (R- · K-)')
    for nm, frs in (('reg', rf), ('cmd', cf)):
        for fid, f in frs.items():
            for b in f['blocks']:
                need(R.PLAN_DOC_BEGIN not in b and R.PLAN_DOC_END not in b, f'{fid}: 블록 표지 글자를 조각에 쓰지 않는다')
                need(ANCHOR not in b, f'{fid}: 자리 줄 글자를 조각에 쓰지 않는다')
                need(not any(ln.startswith(ROW_PLAN) or ln.startswith(ROW_S0) for ln in b.split('\n')), f'{fid}: 해시 줄 머리로 시작하는 줄')
                need(PH_BLOCK not in b or (nm == 'reg' and fid == 'R-07'), f'{fid}: {PH_BLOCK} 는 R-07 에만')
    r07 = rf['R-07']['blocks'][0].split('\n')
    need(r07.count(PH_BLOCK) == 1 and sum(PH_BLOCK in x for x in r07) == 1, f'R-07: {PH_BLOCK} = 한 줄 그 글자 하나')

    def filled(f):
        return [fill(b, subs) for b in f['blocks']]
    # 봉인본
    sops = []
    for fid in rorder:
        if fid == 'R-MARK':
            continue
        bl = filled(rf[fid])
        if fid == 'R-07':
            bl = ['\n'.join(blk if x == PH_BLOCK else x for x in bl[0].split('\n'))]
        sops.append((fid,) + rf[fid]['op'] + (bl,))
    sealed, srec = apply_ops(pin_reg, sops, '봉인본')
    # 원본 자리 (표지 한 줄)
    mark = filled(rf['R-MARK'])[0]
    need('\n' not in mark, 'R-MARK = 한 줄')
    need(not (mark.startswith(ROW_PLAN) or mark.startswith(ROW_S0)), 'R-MARK 가 해시 줄 머리로 시작')
    need(R.PLAN_DOC_BEGIN not in mark and R.PLAN_DOC_END not in mark and ANCHOR not in mark, 'R-MARK 에 블록 표지 · 자리 줄 글자')
    need(sealed_rel in mark and '봉인 커밋' in mark, 'R-MARK 가 봉인본 자리 · 봉인 커밋을 가리키지 않는다')
    marked, mrec = apply_ops(pin_reg, [('R-MARK',) + rf['R-MARK']['op'] + ([mark],)], '원본 자리')
    need(len(marked.split('\n')) == len(pin_reg.split('\n')) + 1, '원본 자리 = 원본 + 한 줄')
    # 명령 문서
    cops = [(fid,) + cf[fid]['op'] + (filled(cf[fid]),) for fid in corder]
    cmd, crec = apply_ops(pin_cmd, cops, '명령 문서')
    need(bash_body(cmd) == bash_body(pin_cmd), '명령 문서 ```bash 블록의 주석 아닌 줄이 바뀌었다 (시험 K01 이 읽는 인자)')
    need(R.PLAN_DOC_BEGIN not in cmd and R.PLAN_DOC_END not in cmd, '명령 문서에 블록 표지')
    for nm, t in (('봉인본', sealed), ('원본 자리', marked), ('명령 문서', cmd)):
        for k in TOOL_PH:
            need(k not in t, f'{nm}: 도구 자리표 {k} 가 남았다')
    # 사슬 함수 대조 (임시 파일)
    checks = {}
    with tempfile.TemporaryDirectory(prefix='msc_chk_') as td:
        sp, mp = os.path.join(td, 'sealed.md'), os.path.join(td, 'marked.md')
        open(sp, 'wb').write(sealed.encode('utf-8'))
        open(mp, 'wb').write(marked.encode('utf-8'))
        checks['sealed.registration_plan_hash = 계획 sha256'] = R.registration_plan_hash(sp)[0] == plan_sha
        checks['sealed.registration_s0_hash = S0 계획 sha256'] = R.registration_s0_hash(sp)[0] == s0_sha
        checks['sealed.plan_doc_problem None'] = R.plan_doc_problem(sp, plan) is None
        try:
            R.registration_plan_hash(mp)
            checks['marked.registration_plan_hash = PLAN_HASH_UNREGISTERED'] = False
        except R.Stop as e:
            checks['marked.registration_plan_hash = PLAN_HASH_UNREGISTERED'] = e.code == 'PLAN_HASH_UNREGISTERED'
        checks['marked.plan_doc_problem (블록 없음 = 문제)'] = R.plan_doc_problem(mp, plan) is not None
    for nm, t, nb in (('sealed', sealed, 1), ('marked', marked, 0)):
        checks[f'{nm}: 블록 표지 시작 · 끝 = {nb} · {nb}'] = t.count(R.PLAN_DOC_BEGIN) == nb and t.count(R.PLAN_DOC_END) == nb
        checks[f'{nm}: 해시 줄 둘 = 1 · 1'] = count_rows(t, ROW_PLAN) == 1 and count_rows(t, ROW_S0) == 1
        checks[f'{nm}: 자리 줄 글자 = 1 줄'] = sum(ANCHOR in ln for ln in t.splitlines()) == 1
    bad = [k for k, v in checks.items() if not v]
    need(not bad, f'사슬 함수 · 셈 대조 실패: {bad}')
    outs = {sealed_rel: sealed.encode('utf-8'), REG_REL: marked.encode('utf-8'), CMD_REL: cmd.encode('utf-8'), plan_rel: raw['plan']}
    left = sorted(set(PH_RE.findall('\n'.join(b for f in list(rf.values()) + list(cf.values()) for b in filled(f)))) - {PH_BLOCK})
    need(set(left) <= set(ALLOWED_PH), f'남은 자리표가 허용 목록 밖: {sorted(set(left) - set(ALLOWED_PH))}')
    me = open(os.path.abspath(__file__), 'rb').read()
    man = {'schema': 'rint2-seal-copy-v2', 'pin': PIN, 'tool_sha256': sha(me), 'seal_date': a.seal_date, 'seal_branch': a.seal_branch,
           'seal_status': SEAL_STATUS[final],
           'sealed_rel': sealed_rel, 'plan_rel': plan_rel, 'plan_sha256': plan_sha, 's0_plan_sha256': s0_sha, 'block_sha256': sha(blk.encode('utf-8')),
           'inputs': {k: {'sha256': sha(raw[k]), 'bytes': len(raw[k])} for k in ('reg', 'cmd', 'chain', 'plan', 's0', 'reg_ins', 'cmd_ins')},
           'outputs': {p: {'sha256': sha(b), 'bytes': len(b), 'lines': b.decode('utf-8').count('\n')} for p, b in sorted(outs.items())},
           'fragments': {'sealed': srec, 'marked': mrec, 'cmd': crec},
           'remaining_placeholders_in_fragments': left, 'checks': checks,
           'plan_checks': {'계획 바이트 = Q3 꼴 (indent 1 · sort_keys · ASCII · 끝 줄바꿈 없음)': True,
                           '두 계획 대조 plans_cross_problems(계획, S0 계획) = []': True,
                           '결과 전 등록 넷 (require_plan_numbers)': ('통과 (--final)' if final else '보지 않음 (후보 · --final 없음)')}}
    return outs, man


def write_out(out, outs, man):
    if os.path.exists(out):
        need(os.path.isdir(out) and not os.listdir(out), f'--out {out} 이 비어 있지 않다')
    tmp = tempfile.mkdtemp(prefix='.msc_out_', dir=os.path.dirname(os.path.abspath(out)))
    try:
        for rel, b in outs.items():
            p = os.path.join(tmp, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'wb') as f:
                f.write(b)
        with open(os.path.join(tmp, '_manifest.json'), 'w', encoding='utf-8') as f:
            json.dump(man, f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write('\n')
        if os.path.exists(out):
            os.rmdir(out)
        os.rename(tmp, out)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise


# ── 자기 시험 ──────────────────────────────────────────────────────────────────────────────────
def selftest(chain):
    """자기 시험 — ①–③ = v2 의 17 개 그대로 · ④ = v2.1 (11-17 · 내부 반박 리뷰 P2-2 · P3-4 · P3-12 반례 · 고치기 전 판에서 먼저 돌려 빠뜨림을 보았다).
    고정물 = 짧은 가짜 원본 · 조각 · 계획 (시험 값 · 등록 숫자 아님) · S0 고정물 = 두 계획 대조 칸만 (사슬 상수 L_par · r_port · r_f · tol = 계획 tol_ff)."""
    global FRAG_SETS, ALLOWED_PH
    td = tempfile.mkdtemp(prefix='msc_selftest_')
    ok, bad = 0, []
    saved_g = {k: globals().get(k) for k in ('FRAG_SETS', 'ALLOWED_PH')}

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(name)

    try:
        R = load_chain(chain)
        pin = '\n'.join(['# 등록 R 초안 — 시험', '', '| 문턱 | 식 | 숫자 |', '|---|---|---|', '| u (위치 불확도) | 식 | ⬜ |',
                         '| 계획 해시 | 계획 | ⬜ |', '| S0 계획 해시 | S0 | ⬜ |', '',
                         '- **(10-28 · 묶음 C1a) 계획 숫자 블록 = 이 줄 바로 아래 (봉인 커밋 때)** 자리', '', '## 10. 명령', '- 끝 줄', '']) + ''
        cmdpin = '\n'.join(['# 명령', '', '```bash', '# 머리', 'python3 x.py --a 1', '```', '', '## 4. 쟁점', '']) + ''
        plan = {'calib_rj_ratio_max': 'none', 'exec_policy': {'adoption': 'first_not_pre_result_v1', 'allowed_machines': ['kgy'],
                                                              'attempt_dir': 'attempt_<n>', 'env_unit': {'numpy': '1.24.4', 'python_minor': '3.8',
                                                                                                         'scipy': '1.10.1'},
                                                              'max_attempts': 8, 'max_hours': 168, 'retry_rule': 'pre_result_only_v1',
                                                              'same_config': 'plan_code_bed_env_v1'},
                'len_law': 'len_scaled_v0', 'max_ladder_points': 12, 'p2_extra': '--step3-maxiter 5000000', 's_min_um': 0.0,
                'schema': 'rint-r-plan-v3', 'step3_rtol': 1e-12, 'sv_cf_scope': 'R_j0', 'sv_cf_threshold': 2.0, 'tol_ff_um': 0.07, 'unreg_law': 'cut'}
        reg_ins = '\n'.join([
            '# 머리', '', '## R-MARK · 표지', '', '@op after 1 # 등록 R 초안 — 시험', '', '====',
            '> 표지 (<봉인 날짜>) 봉인본 `<봉인본>` · 봉인 커밋 = 그 파일을 넣은 커밋', '====', '',
            '## R-00 · 머리', '', '@op after 1 # 등록 R 초안 — 시험', '', '====', '', '> 봉인본 <봉인 날짜> · 원본 그대로 + 조각', '====', '',
            '## R-01 · u', '', '@op last 5 | u (위치 불확도) |', '', '====', '~~⬜~~ → **0.07 µm**', '====', '',
            '## R-05 · 계획 해시', '', '@op mid+last 6 | 계획 해시 |', '', '====', ' · 계획 = `docs/data/rint2_r_plan_<봉인 날짜>/ca1_plan.json`', '====',
            '', '====', '`<봉인 계획 sha256>`', '====', '',
            '## R-06 · S0', '', '@op mid+last 7 | S0 계획 해시 |', '', '====', ' · S0', '====', '', '====', '`<S0SHA>`', '====', '',
            '## R-07 · 블록', '', '@op after 9 - **(10-28 · 묶음 C1a)', '', '====', '', PH_BLOCK, '', '====', '',
            '## R-10 · 절', '', '@op after 11 ## 10. 명령', '', '====', '', '```sh', 'python3 ~/dem-ca1/scripts/rint_r_chain.py --registration ~/dem-ca1/<봉인본>',
            '```', '====', ''])
        cmd_ins = '\n'.join(['# 머리', '', '## K-01 · 주석', '', '@op after 4 # 머리', '', '====', '# ★ 봉인 <봉인 날짜> · <봉인 가지>', '====', '',
                             '## K-03 · 절', '', '@op before 8 ## 4. 쟁점', '', '====', '## 3-1b. 실제 줄 <봉인 날짜>', '', '```sh', 'echo <봉인 커밋>',
                             '```', '', '====', ''])
        # ④ 고정물 (v2.1): 조각 이름 집합 · 남은 자리표 허용 목록 = 이 고정물의 것
        FRAG_SETS = (frozenset({'R-MARK', 'R-00', 'R-01', 'R-05', 'R-06', 'R-07', 'R-10'}), frozenset({'K-01', 'K-03'}))
        ALLOWED_PH = frozenset({'<봉인 가지>', '<봉인 커밋>'})
        p = {}
        for k, t in (('reg', pin), ('cmd', cmdpin)):
            p[k] = os.path.join(td, k + '.md')
            open(p[k], 'w', encoding='utf-8').write(t)

        def wplan(name, obj, text=None):
            q = os.path.join(td, name)
            open(q, 'w', encoding='ascii').write(text if text is not None else json.dumps(obj, indent=1, sort_keys=True))
            return q
        p['plan'] = wplan('plan.json', plan)
        p['s0'] = os.path.join(td, 's0.json')
        s0obj = {'values_um': {'L_par': R.L_PAR_UM, 'r_f': R.VGCF_D_UM / 2.0, 'r_port': R.R_PORT_UM, 'tol_P': 0.07, 'tol_ff': 0.07, 'tol_sj': 0.07}}
        open(p['s0'], 'w', encoding='ascii').write(json.dumps(s0obj, sort_keys=True))
        s0sha = sha(open(p['s0'], 'rb').read())

        def args(reg_text=reg_ins, cmd_text=cmd_ins, date='20261120', branch=None, tag='a', plan_path=None, s0_path=None, final=False):
            ri, ci = os.path.join(td, f'ri_{tag}.md'), os.path.join(td, f'ci_{tag}.md')
            s0p = s0_path or p['s0']
            open(ri, 'w', encoding='utf-8').write(reg_text.replace('<S0SHA>', sha(open(s0p, 'rb').read())))
            open(ci, 'w', encoding='utf-8').write(cmd_text)
            return argparse.Namespace(pin_reg=p['reg'], pin_cmd=p['cmd'], reg_insert=ri, cmd_insert=ci, plan=plan_path or p['plan'], s0_plan=s0p,
                                      chain=chain, seal_date=date, seal_branch=branch, out=None, final=final)

        def fails(a, why, expect=None):
            try:
                build(a, expect=expect)
            except Fail as e:
                return why in str(e)
            return False
        outs1, man1 = build(args(tag='a'), expect=None)
        outs2, man2 = build(args(tag='b'), expect=None)
        sealed = outs1['docs/reviews/rint2_seal_20261120/registration_R_sealed.md'].decode('utf-8')
        marked = outs1[REG_REL].decode('utf-8')
        cmdo = outs1[CMD_REL].decode('utf-8')
        chk('① 같은 입력 = 같은 출력 바이트', outs1 == outs2)
        chk('① 사슬 대조 전부 참', all(man1['checks'].values()) and len(man1['checks']) == 11)
        chk('② 봉인본 블록 = plan-doc 출력 · 해시 = 계획 sha256', sha(open(p['plan'], 'rb').read()) in sealed and sealed.count('rint-r-plan-doc:begin') == 1)
        chk('② 원본 자리 = 원본 + 한 줄 · 해시 칸 ⬜', marked.split('\n')[1].startswith('> 표지 (20261120)') and len(marked.split('\n')) == len(pin.split('\n')) + 1
            and '| 계획 해시 | 계획 | ⬜ |' in marked)
        chk('② 명령 문서 bash 주석만 · 남은 자리표 = <봉인 가지> · <봉인 커밋>', '# ★ 봉인 20261120 · <봉인 가지>' in cmdo
            and man1['remaining_placeholders_in_fragments'] == ['<봉인 가지>', '<봉인 커밋>'])
        chk('② --seal-branch 를 주면 채운다', '# ★ 봉인 20261120 · seal-x' in build(args(branch='seal-x', tag='c'), expect=None)[0][CMD_REL].decode('utf-8'))
        chk('③ 핀 sha256 다르면 거부', fails(args(tag='d'), '≠ 핀 blob', expect={'reg': '0' * 64}))
        chk('③ 머리 글자 줄 둘이면 거부', fails(args(reg_text=reg_ins.replace('@op last 5 | u (위치 불확도) |', '@op last 5 |'), tag='e'), '개 (하나여야)'))
        chk('③ 줄 번호 다르면 거부', fails(args(reg_text=reg_ins.replace('@op last 5 |', '@op last 4 |'), tag='f'), '≠ 적은 4 줄'))
        chk('③ 조각에 블록 표지 글자 = 거부', fails(args(reg_text=reg_ins.replace('~~⬜~~ → **0.07 µm**', '~~⬜~~ <!-- rint-r-plan-doc:end -->'), tag='g'), '블록 표지'))
        chk('③ 조각이 해시 줄 머리 줄을 넣으면 거부', fails(args(reg_text=reg_ins.replace('> 봉인본 <봉인 날짜> · 원본 그대로 + 조각',
                                                                                       '| 계획 해시 | 둘째 | ⬜ |'), tag='h'), '해시 줄 머리'))
        chk('③ 표지 두 줄이면 거부', fails(args(reg_text=reg_ins.replace('봉인 커밋 = 그 파일을 넣은 커밋', '봉인 커밋\n> 둘째'), tag='i'), 'R-MARK = 한 줄'))
        chk('③ 표지가 봉인본을 안 가리키면 거부', fails(args(reg_text=reg_ins.replace('봉인본 `<봉인본>` · ', ''), tag='j'), '가리키지 않는다'))
        chk('③ 날짜 꼴 거부', fails(args(date='2026-11-20', tag='k'), '--seal-date'))
        chk('③ 명령 문서 bash 인자를 바꾸면 거부', fails(args(cmd_text=cmd_ins.replace('# ★ 봉인 <봉인 날짜> · <봉인 가지>', 'python3 y.py --b 2'), tag='l'),
                                                    'bash 블록'))
        chk('③ 블록 자리표 둘이면 거부', fails(args(reg_text=reg_ins.replace('~~⬜~~ → **0.07 µm**', '~~⬜~~ ' + PH_BLOCK), tag='m'), 'R-07 에만'))
        chk('③ S0 해시 칸이 S0 계획과 다르면 거부', fails(args(reg_text=reg_ins.replace('`<S0SHA>`', '`' + '1' * 64 + '`'), tag='n'), '사슬 함수'))
        # ④ v2.1 반례 (리뷰 P2-2 · P3-4 · P3-12) — 계획 꼴 (Q3) · 두 계획 대조 · --final · 조각 꼴 · 자리표 · 날짜 · 가지 · 출력 이름 무관
        raw_plan = open(p['plan'], encoding='ascii').read()
        chk('④ A22 계획 끝 줄바꿈 = 거부 (Q3 꼴)', fails(args(plan_path=wplan('p22.json', None, raw_plan + '\n'), tag='o'), 'Q3 꼴'))
        chk('④ A23 계획 indent 2 = 거부 (Q3 꼴)', fails(args(plan_path=wplan('p23.json', None, json.dumps(plan, indent=2, sort_keys=True)), tag='p'), 'Q3 꼴'))
        chk('④ 계획 칸 차례 (sort_keys 아님) = 거부 (Q3 꼴)', fails(args(plan_path=wplan('p23b.json', None, json.dumps(dict(sorted(plan.items(), reverse=True)),
                                                                                                            indent=1)), tag='p2'), 'Q3 꼴'))
        chk('④ A24 계획 tol_ff ≠ S0 = 거부 (두 계획 대조)', fails(args(plan_path=wplan('p24.json', dict(plan, tol_ff_um=0.0738)), tag='q'), '두 계획 대조'))
        chk('④ A25 계획 len_law 틀림 = 거부 (두 계획 대조)', fails(args(plan_path=wplan('p25.json', dict(plan, len_law='len_scaled_v9')), tag='r'), '두 계획 대조'))
        s0bad = os.path.join(td, 's0_bad.json')
        open(s0bad, 'w', encoding='ascii').write(json.dumps({'values_um': dict(s0obj['values_um'], tol_P=0.08)}, sort_keys=True))
        chk('④ S0 tol_P ≠ tol_ff = 거부 (두 계획 대조)', fails(args(s0_path=s0bad, tag='s'), '두 계획 대조'))
        null4 = dict(plan, max_ladder_points=None, calib_rj_ratio_max=None, sv_cf_threshold=None, sv_cf_scope=None)
        pn = wplan('pnull.json', null4)
        chk('④ --final + 넷 null = 거부 (PLAN_NUMBER_UNREGISTERED)', fails(args(plan_path=pn, tag='t', final=True), 'PLAN_NUMBER_UNREGISTERED'))
        o_c, m_c = build(args(plan_path=pn, tag='u'), expect=None)
        chk('④ --final 없이 넷 null = 만든다 · manifest = 후보 · 봉인 값 아님', '후보 · 봉인 값 아님' in str(m_c.get('seal_status')))
        o_f, m_f = build(args(tag='v', final=True), expect=None)
        chk('④ --final + 넷 채움 = 만든다 · manifest = final', str(m_f.get('seal_status', '')).startswith('final'))
        chk('④ 같은 입력 바이트 · 다른 파일 이름 = manifest 도 같은 바이트 (입력 이름 안 넣음)',
            json.dumps(man1, sort_keys=True, ensure_ascii=False) == json.dumps(man2, sort_keys=True, ensure_ascii=False))
        chk('④ A02 빈 after 블록 = 거부', fails(args(reg_text=reg_ins.replace('====\n\n> 봉인본 <봉인 날짜> · 원본 그대로 + 조각\n====', '====\n===='), tag='w'), '빈 블록'))
        chk('④ A10 끝 칸 글에 줄바꿈 + 표 줄 = 거부', fails(args(reg_text=reg_ins.replace('~~⬜~~ → **0.07 µm**', '~~⬜~~ → **0.07 µm**\n| 계획 해시X | 넣음 | 줄 |'),
                                                            tag='x'), '표 칸 글'))
        chk('④ A11 끝 칸 글에 | = 거부', fails(args(reg_text=reg_ins.replace('~~⬜~~ → **0.07 µm**', '~~⬜~~ → **0.07 µm** | 덧 칸'), tag='y'), '표 칸 글'))
        chk('④ A15 조각 하나 빠짐 (R-10) = 거부', fails(args(reg_text=reg_ins.split('## R-10 · 절')[0], tag='z'), '조각 이름'))
        chk('④ 모르는 조각 이름 (R-16) = 거부', fails(args(reg_text=reg_ins + '\n## R-16 · 덧\n\n@op after 12 - 끝 줄\n\n====\n- 덧 줄\n====\n', tag='z2'),
                                                 '조각 이름'))
        chk('④ A17 모르는 자리표 <봉인본X> = 거부', fails(args(reg_text=reg_ins.replace('--registration ~/dem-ca1/<봉인본>', '--registration ~/dem-ca1/<봉인본X>'),
                                                          tag='z3'), '자리표'))
        chk('④ A30 날짜 20261320 = 거부', fails(args(date='20261320', tag='z4'), '--seal-date'))
        chk('④ A34 가지 seal.lock = 거부', fails(args(branch='seal.lock', tag='z5'), '--seal-branch'))
    finally:
        for k, v in saved_g.items():
            globals()[k] = v
        shutil.rmtree(td, ignore_errors=True)
    print(f'make_sealed_copy selftest: {ok}/{ok + len(bad)} PASS' + (f'   FAILED: {bad}' if bad else ''))
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    for k in ('--pin-reg', '--pin-cmd', '--reg-insert', '--cmd-insert', '--plan', '--s0-plan', '--out'):
        ap.add_argument(k)
    ap.add_argument('--chain', required=True, help='핀 판 scripts/rint_r_chain.py (sha256 = 핀 blob)')
    ap.add_argument('--seal-date')
    ap.add_argument('--seal-branch', default=None)
    ap.add_argument('--final', action='store_true', help='봉인 때 필수 — 결과 전 등록 넷이 다 채워져야 (핀 사슬 require_plan_numbers) · 없으면 후보')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.chain)
    miss = [k for k in ('pin_reg', 'pin_cmd', 'reg_insert', 'cmd_insert', 'plan', 's0_plan', 'out', 'seal_date') if getattr(a, k) is None]
    if miss:
        ap.error('필요한 인자: ' + ' · '.join('--' + m.replace('_', '-') for m in miss))
    try:
        outs, man = build(a)
        write_out(a.out, outs, man)
    except Fail as e:
        print(f'⛔ make_sealed_copy 거부 — {e}', file=sys.stderr)
        return 2
    print(f'make_sealed_copy: 봉인본 {man["sealed_rel"]} sha256 {man["outputs"][man["sealed_rel"]]["sha256"]} · 계획 {man["plan_sha256"]} · '
          f'블록 {man["block_sha256"][:16]}… · 조각 {len(man["fragments"]["sealed"])} + 표지 1 + 명령 {len(man["fragments"]["cmd"])} · '
          f'남은 자리표 {len(man["remaining_placeholders_in_fragments"])} 개 (허용 목록 안) · {man["seal_status"]} → {a.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
