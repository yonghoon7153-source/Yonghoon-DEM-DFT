#!/usr/bin/env python3
"""봉인 꼴 트리의 두 문서 (봉인본 · kgy 명령 문서) + 원본 자리의 울타리 명령을 사슬 · S0 argparse 로 대조 — 리포 무변경 · 결과 0 건 · σ 없음 · 단계 함수 = 받기만.

    python3 -I check_sh_commands.py <봉인 꼴 트리 (scripts · docs)> <봉인본 리포 상대 자리> <가짜 홈 (없어야)> --expect sealed=13+1,kgy=14+1
    python3 -I check_sh_commands.py --selftest <봉인 꼴 트리> <봉인본 리포 상대 자리> --expect sealed=13+1,kgy=14+1

v2.1 (11-17 · 내부 반박 리뷰 P2-1 · P3-11 고침 · 자기 시험 = 리뷰 변이 D1–D10 + 새 검사 반례 · 고치기 전 판에서 먼저 돌려 빠뜨림을 보았다):
  · 모든 울타리 (```sh · ```bash · 그 밖) 를 읽는다 — 도구 이름이 든 조각이 `python3? <…>/<도구>` 꼴이 아니면 = 못 읽은 줄 = 문제
    (첫 낱말이 git · ls · cp … = 도구 이름이 인자로만 나온 줄 · 따로 센다) · ```sh 밖 · ```bash 밖 울타리의 도구 줄 = 문제
  · ```bash = 인자 계약 꼴 (리포 시험 K01 이 원본 자리 · 명령 문서의 이 꼴을 사슬 argparse 와 대조 · --registration · --r-doc 없음 = 설계) → 따로 센다
  · ```sh = 실제 실행 줄 → 사슬 명령마다 `--registration` = <가짜 홈>/dem-ca1/<봉인본> · S0 단계 2 마다 `--r-doc` = <봉인본> (리포 상대 그대로) ·
    사다리 · 단위 · 점 = 원장 시도 꼴 + `--cjunc-store ~/ca1_cjstore` (글자 그대로 · Q4) · 합치기 = --attempt · --cjunc-store 없음 ·
    사다리 · 예측 --max-hours 168 · --machine ∈ 허용 목록 · 사다리 --law P0 = kgy · P1 = gabia (Q6 · ledger --add ladder:<법칙> 도)
  · 기대 셈 (--expect · 독립 셈과 맞춘 값) ≠ 읽은 sh 명령 수 = 문제 · sh 명령 0 개 = 문제 · 원본 자리의 sh 실행 줄 = 문제
  · 종류마다 두 문서의 인자 이름 집합이 같다 · 한 문서에만 있는 종류 = 문제 (사다리 dry-run 만 허용 · 명령 문서 §3-1b (4) 에만)
  · 보지 않는 것: `--out` 값 · 단위 이름 ↔ 기계 첫 배정 · 줄 순서 (사슬이 결과 전에 막는 것 = `--target` · 대상 ↔ 법칙 · 기계 ↔ 항목)
방법 = 봉인 후보 v1 `evidence/tools/apply_and_check.py` (시험 K01 과 같은 꼴: 자리표 <…> → '1' · `\\` 이음 · 주석 줄 뺌 · && | ; 로 가름 ·
단계 함수 · S0 `verify_plan_commit` 를 바꿔 끼워 argparse 만) + `~/` → 가짜 홈 (저장본 폴더 = 실제 0755 폴더).  화면의 가짜 홈 · 트리 경로 = 자리표.
"""
import contextlib
import io
import json
import os
import re
import shlex
import sys
from pathlib import Path

KGY_REL = 'docs/reviews/rint2_kgy_commands_20261020.md'
ORIG_REL = 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md'


# ── 자기 시험 (11-17 · v2.1 · 내부 반박 리뷰 P2-1 변이 D1–D10 + 새 검사 반례 · 고치기 전 도구에서 먼저 돌려 빠뜨림을 본 뒤 고쳤다) ──
def _fence_spans(text, kind):
    """```<kind> 울타리 안 글자 자리 (시작 · 끝) 목록 — 도구와 같은 울타리 셈 (줄 앞뒤 빈칸을 걷은 줄이 ``` 로 시작하면 울타리 줄)."""
    spans, pos, fence, beg = [], 0, None, 0
    for ln in text.split('\n'):
        s = ln.strip()
        if s.startswith('```'):
            if fence is None:
                fence, beg = s[3:].strip(), pos + len(ln) + 1
            else:
                if fence == kind:
                    spans.append((beg, pos))
                fence = None
        pos += len(ln) + 1
    return spans


def _rep_in(text, kind, old, new):
    """``` <kind> 울타리 안의 첫 `old` 를 `new` 로 — 없으면 시험 오류 (변이 자리 없음 = 그 경우 실패)."""
    for a, b in _fence_spans(text, kind):
        i = text.find(old, a, b)
        if i >= 0:
            return text[:i] + new + text[i + len(old):]
    raise AssertionError(f'변이 자리 없음 ({kind} · {old[:60]!r})')


def _fence_lines(text, kind):
    """첫 ```<kind> 울타리의 여는 줄 · 닫는 줄 번호 (0 부터)."""
    lines, fence, at = text.split('\n'), None, None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith('```'):
            if fence is None:
                fence, at = s[3:].strip(), i
            else:
                if fence == kind:
                    return lines, at, i
                fence = None
    raise AssertionError(f'```{kind} 울타리 없음')


def _drop_fence(text, kind):
    lines, a, b = _fence_lines(text, kind)
    return '\n'.join(lines[:a] + lines[a + 1:b] + lines[b + 1:])


def _retag_fence(text, kind, new):
    lines, a, _b = _fence_lines(text, kind)
    lines[a] = lines[a].replace('```' + kind, '```' + new, 1)
    return '\n'.join(lines)


def _drop_line_in(text, kind, prefix):
    for a, b in _fence_spans(text, kind):
        seg = text[a:b].split('\n')
        for k, ln in enumerate(seg):
            if ln.startswith(prefix):
                return text[:a] + '\n'.join(seg[:k] + seg[k + 1:]) + text[b:]
    raise AssertionError(f'변이 자리 없음 (줄 {prefix[:60]!r})')


def _parse_expect(s):
    out = {}
    for part in s.split(','):
        k, _, v = part.partition('=')
        c, _, s0 = v.partition('+')
        if not (k and c.isdigit() and s0.isdigit()):
            raise SystemExit(f'--expect 꼴 = sealed=<사슬>+<S0>,kgy=<사슬>+<S0> · {s!r}')
        out[k] = (int(c), int(s0))
    if set(out) != {'sealed', 'kgy'}:
        raise SystemExit(f'--expect 이름 = sealed · kgy · {sorted(out)}')
    return out


def _fmt_expect(e):
    return ','.join(f'{k}={e[k][0]}+{e[k][1]}' for k in ('sealed', 'kgy'))


def _selftest(argv):
    """argv: <봉인 꼴 트리> <봉인본 리포 상대 자리> --expect sealed=<n>+<m>,kgy=<n>+<m> (= 그 트리 그대로의 셈).
    경우마다 임시 트리 (scripts = 원 트리 심볼릭 링크 · 문서 셋 = 변이) 에서 이 파일을 python3 -I 로 따로 돌려 rc (와 표지 글자) 를 본다."""
    import argparse as _ap
    import shutil as _sh
    import subprocess as _sp
    import tempfile as _tf
    p = _ap.ArgumentParser(prog='check_sh_commands.py --selftest')
    p.add_argument('tree')
    p.add_argument('sealed_rel')
    p.add_argument('--expect', required=True)
    a = p.parse_args(argv)
    tree = os.path.abspath(a.tree)
    exp0 = _parse_expect(a.expect)
    base = {k: Path(tree, rel).read_text(encoding='utf-8') for k, rel in (('sealed', a.sealed_rel), ('kgy', KGY_REL), ('orig', ORIG_REL))}
    reg = '~/dem-ca1/' + a.sealed_rel

    def m(**kw):
        def f(d):
            d = dict(d)
            for k, fn in kw.items():
                d[k] = fn(d[k])
            return d
        return f

    def ex(sealed=(0, 0), kgy=(0, 0)):
        return {'sealed': (exp0['sealed'][0] + sealed[0], exp0['sealed'][1] + sealed[1]), 'kgy': (exp0['kgy'][0] + kgy[0], exp0['kgy'][1] + kgy[1])}

    d1 = lambda t: _rep_in(t, 'sh', f'--init --plan ~/sdcp/ca1_plan.json --registration {reg}', '--init --plan ~/sdcp/ca1_plan.json')

    def d10(t):
        old = 'nohup python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder'
        t = _rep_in(t, 'sh', old, 'nohup python3 -I ~/dem-ca1/scripts/rint_r_chain.py --stage ladder')
        i = t.find('nohup python3 -I ~/dem-ca1/scripts/rint_r_chain.py --stage ladder')
        j = t.find(f' --registration {reg}', i)
        assert j > i, '변이 자리 없음 (D10 --registration)'
        return t[:j] + t[j + len(f' --registration {reg}'):]

    def d13(t):
        for aa, bb in _fence_spans(t, 'bash'):
            mo = re.compile(r'python3 (\S*rint_r_chain\.py)').search(t, aa, bb)
            if mo:
                return t[:mo.start()] + 'python3 -I ' + mo.group(1) + t[mo.end():]
        raise AssertionError('변이 자리 없음 (D13)')

    cases = [
        ('D0 그대로', m(), ex(), 0, None),
        ('D1 봉인본 원장 --init 줄 --registration 지움', m(sealed=d1), ex(), 1, None),
        ('D2 봉인본 sh 울타리 지움', m(sealed=lambda t: _drop_fence(t, 'sh')), ex(), 1, None),
        ('D3 봉인본 원장 --init 줄 = python3 -I + --registration 지움', m(sealed=lambda t: _rep_in(
            t, 'sh', f'python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --init --plan ~/sdcp/ca1_plan.json --registration {reg}',
            'python3 -I ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --init --plan ~/sdcp/ca1_plan.json')), ex(), 1, None),
        ('D4 D1 + 그 울타리 = bash', m(sealed=lambda t: _retag_fence(d1(t), 'sh', 'bash')), ex(), 1, None),
        ('D5 명령 문서 --max-hours 160', m(kgy=lambda t: _rep_in(t, 'sh', '--max-hours 168', '--max-hours 160')), ex(), 1, None),
        ('D6 명령 문서 --registration = 원본 자리', m(kgy=lambda t: _rep_in(t, 'sh', f'--registration {reg}', '--registration ~/dem-ca1/' + ORIG_REL)), ex(), 1, None),
        ('D7 명령 문서 S0 --r-doc 지움', m(kgy=lambda t: _rep_in(t, 'sh', f' --r-doc {a.sealed_rel}', '')), ex(), 1, None),
        ('D8 명령 문서 S0 --r-doc = 원본 자리', m(kgy=lambda t: _rep_in(t, 'sh', f'--r-doc {a.sealed_rel}', '--r-doc ' + ORIG_REL)), ex(), 1, None),
        ('D8b 명령 문서 S0 줄 python3 -u + --r-doc 지움', m(kgy=lambda t: _rep_in(_rep_in(
            t, 'sh', 'python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 2', 'python3 -u ~/dem-ca1/scripts/ca_s0_census.py --stage 2'),
            'sh', f' --r-doc {a.sealed_rel}', '')), ex(), 1, None),
        ('D9 명령 문서 --cjunc-store ~/p6_cjstore (Q4 표지)', m(kgy=lambda t: _rep_in(t, 'sh', '--cjunc-store ~/ca1_cjstore', '--cjunc-store ~/p6_cjstore')),
         ex(), 1, '(Q4)'),
        ('D10 명령 문서 사다리 nohup 줄 python3 -I + --registration 지움', m(kgy=d10), ex(), 1, None),
        ('D11 봉인본 recover 줄 지움 + 기대 셈 맞춤 (한 문서에만 있는 종류)', m(sealed=lambda t: _drop_line_in(
            t, 'sh', 'python3 ~/dem-ca1/scripts/rint_r_chain.py --stage recover')), ex(sealed=(-1, 0)), 1, '한 문서에만'),
        ('D12 그대로 + 기대 셈 틀림', m(), ex(kgy=(1, 0)), 1, '기대 셈'),
        ('D13 명령 문서 bash (계약 꼴) 사슬 줄 python3 -I', m(kgy=d13), ex(), 1, '못 읽은 줄'),
        ('D14 봉인본 sh 울타리 = shell', m(sealed=lambda t: _retag_fence(t, 'sh', 'shell')), ex(), 1, 'sh · bash 밖'),
        ('D15 원본 자리에 sh 사슬 줄', m(orig=lambda t: t + '\n```sh\npython3 ~/dem-ca1/scripts/rint_r_chain.py --stage plan-doc --plan ~/sdcp/ca1_plan.json '
                                         '--check-doc\n```\n'), ex(), 1, '원본 자리'),
        ('D16 명령 문서 사다리 P0 dry-run --machine gabia (Q6 표지)', m(kgy=lambda t: _rep_in(
            t, 'sh', '--machine kgy --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_ladder_P0 --dry-run',
            '--machine gabia --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_ladder_P0 --dry-run')), ex(), 1, '(Q6)'),
        ('D2b D2 + 기대 셈 0 (sh 명령 0 개)', m(sealed=lambda t: _drop_fence(t, 'sh')), {'sealed': (0, 0), 'kgy': exp0['kgy']}, 1, 'sh 명령 0'),
    ]
    td = _tf.mkdtemp(prefix='csc_selftest_')
    ok, bad, rows = 0, [], []
    try:
        for name, fn, exp, want, marker in cases:
            tag = name.split()[0]
            try:
                docs = fn(base)
            except AssertionError as e:
                bad.append(f'{tag}: {e}')
                rows.append(f'{tag} | 변이 못 만듦 | {e}')
                continue
            t = os.path.join(td, 't_' + tag)
            for rel in (a.sealed_rel, KGY_REL, ORIG_REL):
                os.makedirs(os.path.dirname(os.path.join(t, rel)), exist_ok=True)
            os.symlink(os.path.join(tree, 'scripts'), os.path.join(t, 'scripts'))
            for k, rel in (('sealed', a.sealed_rel), ('kgy', KGY_REL), ('orig', ORIG_REL)):
                Path(t, rel).write_text(docs[k], encoding='utf-8')
            r = _sp.run([sys.executable, '-I', os.path.abspath(__file__), t, a.sealed_rel, os.path.join(td, 'h_' + tag), '--expect', _fmt_expect(exp)],
                        capture_output=True, text=True)
            good = r.returncode == want and (marker is None or marker in r.stdout)
            last = (r.stdout.strip().splitlines() or [''])[-1]
            rows.append(f'{tag} | 기대 rc {want}{" + " + repr(marker) if marker else ""} | 실제 rc {r.returncode} | {"PASS" if good else "FAIL"} | {last[:150]}')
            if good:
                ok += 1
            else:
                bad.append(tag)
    finally:
        _sh.rmtree(td, ignore_errors=True)
    for r_ in rows:
        print(r_)
    print(f'check_sh_commands selftest: {ok}/{len(cases)} PASS' + (f'   FAILED: {bad}' if bad else ''))
    return 0 if not bad else 1


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == '--selftest':
    sys.exit(_selftest(sys.argv[2:]))


TOOLS = ('rint_r_chain.py', 'ca_s0_census.py')
ALLOWED = ('kgy', 'gabia', 'v100')
STORE_RAW = '~/ca1_cjstore'                 # 1저자 11-17 봉인 후보 Q4 — R 저장본 = 기계마다 새 빈 폴더 (글자 그대로 · ~ 는 실행 셸이 편다)
LAW_MACHINE = {'P0': 'kgy', 'P1': 'gabia'}  # 1저자 11-17 봉인 후보 Q6 — 사다리 P0 = kgy · P1 = gabia
ONLY_ONE_OK = {'ladder_dry'}                # 한 문서에만 있어도 되는 종류 (사다리 dry-run = 명령 문서 §3-1b (4) 에만 · 설계)
#: 도구 이름이 인자 (파일 경로) 로만 나오는 줄의 첫 낱말 — 부르는 줄이 아니다 (예: same-version 손 확인 `git diff --quiet … scripts/ca_s0_census.py`)
NONINV_OK = ('git', 'ls', 'cp', 'cat', 'grep', 'sha256sum', 'test', 'echo', 'printf')
_SPLIT = re.compile(r'\s(?:&&|\|\||\||;)\s')
_PY = re.compile(r'(^|/)python3?$')


def scan(path):
    """문서 하나의 모든 울타리 (```sh · ```bash · 그 밖) 를 읽는다 — 논리 줄 (`\\` 이음 · 주석 줄 뺌 · 자리표 <…> → '1') 을 && · || · | · ; 로 갈라
    도구 (사슬 · S0) 를 부르는 조각 = `python3? <…>/<도구>` 꼴만 읽는다.  도구 이름이 든 조각인데 그 꼴이 아니면 = 못 읽은 줄 (첫 낱말이 NONINV_OK 면
    인자로만 나온 줄 · 따로 센다).  → {'cmds': [(울타리, 줄, 도구, 인자 (raw))], 'unread': [(울타리, 줄, 조각)], 'argonly': [(울타리, 줄, 첫 낱말)]}"""
    out = {'cmds': [], 'unread': [], 'argonly': []}
    fence, buf, start = None, '', 0
    for i, ln in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        s = ln.strip()
        if s.startswith('```'):
            fence = (s[3:].strip() or '(없음)') if fence is None else None
            buf = ''
            continue
        if fence is None:
            continue
        if not buf:
            if not s or s.startswith('#'):
                continue
            start = i
        cont = s.endswith('\\')
        buf += ' ' + (s[:-1] if cont else s)
        if cont:
            continue
        line, buf = re.sub(r'<[^<>]*>', '1', buf), ''
        for seg in _SPLIT.split(line):
            if not any(t in seg for t in TOOLS):
                continue
            try:
                toks = shlex.split(seg, comments=True)
            except ValueError:
                out['unread'].append((fence, start, seg.strip()[:120]))
                continue
            for tool in TOOLS:
                named = [k for k, t in enumerate(toks) if t == tool or t.endswith('/' + tool)]
                if not named:
                    continue
                at = [k for k in named if k > 0 and _PY.search(toks[k - 1])]
                if not at:
                    w = [t for t in toks if t not in ('nohup', 'exec', 'time')]
                    if w and w[0] in NONINV_OK:
                        out['argonly'].append((fence, start, w[0]))
                    else:
                        out['unread'].append((fence, start, seg.strip()[:120]))
                    continue
                args, skip = [], False
                for t in toks[at[0] + 1:]:
                    if skip:
                        skip = False
                        continue
                    if t == '>':
                        skip = True
                        continue
                    if re.match(r'^\d*>', t) or t == '&':
                        continue
                    args.append(t)
                out['cmds'].append((fence, start, tool, args))
    return out


class _Took(Exception):
    pass


def check(tree, sealed_rel, fakehome, expect):
    """→ (화면 줄, 문제 목록).  사슬 · S0 argparse = 그 트리의 scripts (단계 함수 · S0 관문 = 받기만 · 리포 무변경 · 결과 0 건 · σ 없음)."""
    sys.path.insert(0, str(Path(tree) / 'scripts'))
    import rint_r_chain as RR  # noqa: E402
    import ca_s0_census as S0m  # noqa: E402
    fh = Path(fakehome)
    assert not fh.exists(), fakehome
    (fh / STORE_RAW[2:]).mkdir(parents=True)
    os.chmod(fh / STORE_RAW[2:], 0o755)
    reg_abs = str(fh / 'dem-ca1' / sealed_rel)
    docs = (('sealed', Path(tree) / sealed_rel), ('kgy', Path(tree) / KGY_REL), ('orig', Path(tree) / ORIG_REL))
    got = {}

    def _stub(a, contract=None):
        got['a'] = a
        return 0

    def _vpc(*_a, **_k):
        raise _Took()
    saved = {k: getattr(RR, k) for k in ('stage_ladder', 'stage_predict', 'stage_verdict', 'stage_ledger', 'stage_recover', 'stage_plan_doc')}
    saved_vpc = S0m.verify_plan_commit
    for k in saved:
        setattr(RR, k, _stub)
    S0m.verify_plan_commit = _vpc
    kinds, bad, counts, regvals, rdocs = {}, [], {}, {}, {}

    def home(t):
        return t.replace('~/', str(fh) + '/', 1) if t.startswith('~/') else t
    try:
        for dn, path in docs:
            sc = scan(path)
            c = counts[dn] = {'sh_chain': 0, 'sh_s0': 0, 'bash_chain': 0, 'bash_s0': 0, 'unread': len(sc['unread']), 'argonly': len(sc['argonly']),
                              'other': 0}
            for fence, ln, seg in sc['unread']:
                bad.append(f'{dn}:{ln} 못 읽은 줄 (```{fence} · 도구 이름이 있는데 `python3? <…>/<도구>` 꼴이 아니다) — {seg[:90]!r}')
            for fence, ln, tool, raw in sc['cmds']:
                short = 'chain' if tool == 'rint_r_chain.py' else 's0'
                if fence == 'bash':
                    c['bash_' + short] += 1            # 인자 계약 꼴 (리포 시험 K01 이 원본 자리 · 명령 문서의 이 꼴을 argparse 와 대조 · --registration 없음 = 설계)
                    continue
                if fence != 'sh':
                    c['other'] += 1
                    bad.append(f'{dn}:{ln} sh · bash 밖 울타리 (```{fence}) 의 도구 줄')
                    continue
                c['sh_' + short] += 1
                if dn == 'orig':
                    bad.append(f'{dn}:{ln} 원본 자리 (봉인 전 판 + 표지 한 줄) 에 sh 실행 줄')
                    continue
                args = [home(t) for t in raw]
                if short == 's0':
                    stage = raw[raw.index('--stage') + 1] if '--stage' in raw[:-1] else None
                    if stage != '2':
                        bad.append(f'{dn}:{ln} S0 명령 --stage {stage}')
                        continue
                    err = io.StringIO()
                    try:
                        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                            rc = S0m.main(args)
                        bad.append(f'{dn}:{ln} S0 단계 2 → rc {rc} (관문 앞 인자 검사) · {(err.getvalue().strip().splitlines() or [""])[-1][:160]}')
                        continue
                    except _Took:
                        pass
                    except SystemExit as e:
                        bad.append(f'{dn}:{ln} S0 단계 2 → argparse rc {e.code}')
                        continue
                    rdoc = raw[raw.index('--r-doc') + 1] if '--r-doc' in raw[:-1] else None
                    rdocs.setdefault(dn, set()).add(rdoc)
                    if rdoc != sealed_rel:
                        bad.append(f'{dn}:{ln} S0 단계 2 --r-doc = {rdoc!r} (≠ {sealed_rel!r})')
                    kinds.setdefault((dn, 's0-2'), set()).add(frozenset(t for t in raw if t.startswith('--')))
                    continue
                if '--cjunc-store' in raw:
                    v = raw[raw.index('--cjunc-store') + 1] if '--cjunc-store' in raw[:-1] else None
                    if v != STORE_RAW:
                        bad.append(f'{dn}:{ln} --cjunc-store {v!r} ≠ {STORE_RAW} (Q4 · 기계마다 새 빈 폴더)')
                got.clear()
                err = io.StringIO()
                try:
                    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                        rc = RR.main(args, contract=object())
                except SystemExit as e:
                    rc = f'argparse rc {e.code} · {(err.getvalue().strip().splitlines() or [""])[-1][:160]}'
                if rc != 0 or 'a' not in got:
                    bad.append(f'{dn}:{ln} {raw[:2]} → {rc}')
                    continue
                a = got['a']
                if a.stage == 'predict':
                    k = 'unit' if a.unit else 'point' if a.point else ('merge_x' if a.expand else 'merge') if a.merge else 'predict'
                elif a.stage == 'ledger':
                    k = 'ledger_init' if a.init else 'ledger_add'
                elif a.stage == 'verdict':
                    k = 'reverify' if a.reverify else 'verdict'
                elif a.stage == 'ladder':
                    k = 'ladder_dry' if a.dry_run else 'ladder'
                else:
                    k = a.stage
                kinds.setdefault((dn, k), set()).add(frozenset(t for t in raw if t.startswith('--') and t != '--machine'))
                regvals.setdefault(dn, set()).add(a.registration)
                if '--registration' not in raw or a.registration != reg_abs:
                    bad.append(f'{dn}:{ln} {k} --registration = {a.registration!r} (≠ 봉인본 {reg_abs!r})')
                if k in ('ladder', 'unit', 'point') and not (a.ledger and a.attempt is not None and a.cjunc_store):
                    bad.append(f'{dn}:{ln} {k} = 원장 시도 꼴 + 저장본이 아니다')
                if k in ('ladder', 'ladder_dry', 'unit', 'point') and '--cjunc-store' not in raw:
                    bad.append(f'{dn}:{ln} {k} 에 --cjunc-store {STORE_RAW} 가 없다 (Q4)')
                if k in ('merge', 'merge_x') and (a.attempt is not None or a.cjunc_store):
                    bad.append(f'{dn}:{ln} {k} 에 --attempt · --cjunc-store')
                if a.stage in ('ladder', 'predict') and a.max_hours != 168.0:
                    bad.append(f'{dn}:{ln} --max-hours {a.max_hours}')
                if a.machine is not None and a.machine not in ALLOWED:
                    bad.append(f'{dn}:{ln} --machine {a.machine}')
                if k in ('ladder', 'ladder_dry') and LAW_MACHINE.get(a.law) != a.machine:
                    bad.append(f'{dn}:{ln} {k} --law {a.law} --machine {a.machine} (Q6 · P0 = kgy · P1 = gabia)')
                if k == 'ledger_add' and (a.ledger_target or '').startswith('ladder:'):
                    law = a.ledger_target.split(':')[1] if a.ledger_target.count(':') == 1 else None
                    if law in LAW_MACHINE and LAW_MACHINE[law] != a.machine:
                        bad.append(f'{dn}:{ln} ledger --add {a.ledger_target} --machine {a.machine} (Q6)')
    finally:
        for k, v in saved.items():
            setattr(RR, k, v)
        S0m.verify_plan_commit = saved_vpc
    for dn in ('sealed', 'kgy'):
        want, c = expect[dn], counts[dn]
        if (c['sh_chain'], c['sh_s0']) != want:
            bad.append(f'{dn}: 기대 셈 사슬 {want[0]} + S0 {want[1]} ≠ 읽은 sh 명령 {c["sh_chain"]} + {c["sh_s0"]}')
        if c['sh_chain'] + c['sh_s0'] == 0:
            bad.append(f'{dn}: sh 명령 0 개 (실행 줄 울타리가 없다)')
    rows = [f'# 봉인본 {sealed_rel} · 가짜 홈 = <가짜 홈> · 기대 셈 {_fmt_expect(expect)} · 저장본 {STORE_RAW} (Q4) · 사다리 기계 {LAW_MACHINE} (Q6)']
    for dn, c in counts.items():
        rows.append(f'{dn}: sh 블록 사슬 명령 {c["sh_chain"]} · S0 명령 {c["sh_s0"]} · 계약 꼴 (bash) 사슬 {c["bash_chain"]} · S0 {c["bash_s0"]} · '
                    f'그 밖 울타리 {c["other"]} · 도구 이름이 인자로만 나온 줄 {c["argonly"]} · 못 읽은 줄 {c["unread"]} · '
                    f'--registration 값 {sorted(v.replace(str(fh), "<가짜 홈>") for v in regvals.get(dn, set()))} · S0 --r-doc 값 {sorted(map(str, rdocs.get(dn, set())))}')
    allk = sorted({k for _d, k in kinds})
    for k in allk:
        r, g = kinds.get(('sealed', k), set()), kinds.get(('kgy', k), set())
        same = (r == g) if r and g else None
        rows.append(f'  {k:12s} 봉인본 {len(r)} 집합 · kgy {len(g)} 집합 · 두 문서 같음 {same}' + (f' · 인자 {sorted(next(iter(r or g)))}' if (r or g) else ''))
        if r and g and r != g:
            bad.append(f'{k}: 두 문서 인자 이름 다름 — 봉인본 {sorted(sorted(x) for x in r)} ↔ kgy {sorted(sorted(x) for x in g)}')
    only = [k for k in allk if bool(kinds.get(('sealed', k))) != bool(kinds.get(('kgy', k)))]
    rows.append(f'한 문서에만 있는 종류 {only} (허용 = {sorted(ONLY_ONE_OK)})')
    for k in only:
        if k not in ONLY_ONE_OK:
            bad.append(f'{k}: 한 문서에만 있는 종류 (허용 = {sorted(ONLY_ONE_OK)})')
    real = str(Path(tree, 'scripts').resolve().parent)
    return rows, [b.replace(str(fh), '<가짜 홈>').replace(real, '<트리>').replace(str(tree), '<트리>') for b in bad]


def main(argv):
    import argparse
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('tree')
    p.add_argument('sealed_rel')
    p.add_argument('fakehome')
    p.add_argument('--expect', required=True, help='sealed=<사슬>+<S0>,kgy=<사슬>+<S0> — 두 문서 sh 블록의 기대 명령 수 (독립 셈과 맞춘 값)')
    a = p.parse_args(argv)
    rows, bad = check(os.path.abspath(a.tree), a.sealed_rel, os.path.abspath(a.fakehome), _parse_expect(a.expect))
    for r in rows:
        print(r)
    print('문제', json.dumps(bad, ensure_ascii=False) if bad else '없음')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
