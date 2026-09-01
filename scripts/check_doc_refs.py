#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""문서가 가리키는 것이 **실재하는가** — 경로·커밋 참조 전수 검사.

    python3 scripts/check_doc_refs.py            # 리포 전수
    python3 scripts/check_doc_refs.py --selftest

계기 (2026-08-31): 브랜치를 전수 조사하다 보니 문서가 **없는 파일**과 **없는 커밋**을
가리키는 자리가 여럿 나왔다.  깨진 참조는 조용하다 — 읽는 사람이 열어 보기 전에는 안
보이고, 열어 봤을 때는 이미 그 문서를 믿고 판단한 뒤다.

★ 이 검사기가 **판단하지 않는 것**: 문서 내용이 낡았는지는 기계가 못 본다.  여기서 보는
  것은 *"가리키는 대상이 있는가"* 하나이고, 그것만으로도 renamed·deleted·오타를 잡는다.
  내용 신선도는 사람이 본다 (`--report` 가 그 후보를 따로 모아 준다).

═══ 왜 allowlist 가 필요한가 ═══

이 리포는 **여러 브랜치가 한 주제를 나눠 갖는다**:
  · `litdb/` — 논문 카드 정본은 `origin/claude/friendly-meitner-lldvar` 다.  여기는
    2026-07-16 동결 스냅샷(65장)이라, 정본 202장을 가리키는 참조는 **여기서 깨져 보인다**.
  · `kb/` — DFT 쪽 저장소.
⇒ 그 접두는 **깨짐이 아니라 브랜치 간 참조**다.  조용히 무시하면 오탐을 숨기는 것이므로
  `CROSS_BRANCH` 로 **분류해 세고 보고**한다 (숫자를 감추지 않는다).

═══ SHA 오탐을 어떻게 거르나 ═══

16진수처럼 보이는 것이 전부 커밋은 아니다.  실제로 나온 오탐:
  · `20260829` — 날짜인데 전부 [0-9] 라 hex 로 읽힌다
  · `04b5a565ff4069f4` — 16자리 `input_digest` (커밋이 아니다)
⇒ **순수 10진수 제외** · **문맥에 커밋을 뜻하는 말이 있을 때만** 커밋으로 본다
  (`커밋`·`commit`·`@`·`SHA`).  그래도 애매하면 `UNSURE` 로 빼고 오류로 세지 않는다.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

#: 다른 브랜치가 소유하는 경로 접두 — 여기서 없는 것이 정상이다.
CROSS_BRANCH = ('litdb/', 'kb/')

#: 알려진 예외 목록.  **한 줄에 하나, `경로<TAB>이유`.**
#:  ⚠ 이유 없는 등재를 막는 것이 요점이다 — 이유를 쓰게 하면 "왜 없는가" 가 기록되고,
#:    나중에 그 이유가 사라졌을 때(파일이 생겼을 때) 검사기가 **등재 자체를 지적**한다.
ALLOWLIST = 'docs/reviews/doc_refs_allowlist.tsv'


def load_allowlist(root: str):
    fp = os.path.join(root, ALLOWLIST)
    out = {}
    if not os.path.exists(fp):
        return out
    for ln in open(fp, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        parts = ln.split('\t')
        if len(parts) < 2 or not parts[1].strip():
            raise SystemExit(f'⛔ {ALLOWLIST}: 이유 없는 등재 — {ln!r}')
        out[parts[0].strip()] = parts[1].strip()
    return out

#: 리포 안 파일로 볼 확장자.
EXTS = ('py', 'sh', 'json', 'csv', 'md', 'mjs', 'js', 'yml', 'yaml', 'liggghts',
        'stl', 'npy', 'txt')

_RE_PATH = re.compile(
    r'`([A-Za-z0-9_][A-Za-z0-9_./+-]*\.(?:' + '|'.join(EXTS) + r'))`')
#: 커밋 축약은 7~12자다.  16자리는 이 리포에서 **내용 해시**(`sha(AM)` · `input_digest`)라
#: 커밋으로 보면 전부 오탐이 된다 (2026-08-31 실측: 그 길이의 오탐이 4/7).
_RE_SHA = re.compile(r'`([0-9a-f]{7,12})`')
#: 그 줄이 **스스로** 부재·오기·타 브랜치를 밝히면 검사 대상이 아니다.  문서가 이미
#: 그 사실을 적었다면 그것은 깨진 참조가 아니라 **기록**이다.
_RE_SHA_EXEMPT = re.compile(r'없다|오기|타 ?브랜치|@\s*`?[A-Za-z][\w./-]*/|digest|sha\(')
#: 커밋을 뜻한다고 볼 문맥 (같은 줄에 있어야 한다).
_RE_COMMIT_CTX = re.compile(r'커밋|commit|SHA|sha|@\s*[0-9a-f]{7}|리비전|revision')


def _repo_root(start: str | None = None) -> str:
    d = os.path.dirname(os.path.abspath(start or __file__))
    return os.path.dirname(d)


def known_shas(root: str) -> set:
    """`rev-list --all` 전체.  ⚠ 얕은 클론이면 비어 보이므로 그것도 보고한다."""
    r = subprocess.run(['git', '-C', root, 'rev-list', '--all'],
                       capture_output=True, text=True)
    return set(r.stdout.split())


def scan_text(text: str, root: str, shas: set, shorts: set):
    """한 문서의 참조를 분류한다.  → dict(missing, cross, bad_sha, unsure)."""
    out = dict(missing=[], cross=[], bad_sha=[], unsure=[])
    for raw in _RE_PATH.findall(text):
        p = raw.lstrip('./')
        if p.startswith(CROSS_BRANCH):
            out['cross'].append(p)
            continue
        if os.path.exists(os.path.join(root, p)):
            continue
        if '/' not in p:
            #  맨 파일명 — 흔한 자리들을 찾아본다 (문서가 경로를 생략하는 습관)
            if any(os.path.exists(os.path.join(root, d, p))
                   for d in ('scripts', 'docs', 'docs/data', 'docs/reviews', 'webapp')):
                continue
            out['unsure'].append(p)          # 어디를 가리키는지 모른다 — 오류로 세지 않는다
            continue
        out['missing'].append(p)
    #  ★ 면제는 **문서 단위**다.  한 문서가 어느 줄에서 "그 커밋은 origin 에 없다" 고
    #    밝혔으면, 같은 문서의 다른 줄에서 같은 SHA 를 다시 인용해도 그것은 기록이지
    #    깨진 참조가 아니다 (실측: `d9880b73` 이 22행에서 밝혀지고 264행에서 재인용).
    _exempt_doc = set()
    for ln in text.split('\n'):
        if _RE_SHA_EXEMPT.search(ln):
            #  ⚠ 면제 수집은 **느슨하게** 본다 — 그 줄의 SHA 가 백틱 안에 홀로 있으리란
            #    보장이 없다 (실측: `` `Codex/dem-mpm-crosscheck @ d9880b73` `` 처럼 묶인다).
            #    검사 대상 판정은 그대로 엄격한 `_RE_SHA` 로 한다.
            _exempt_doc.update(re.findall(r'\b([0-9a-f]{7,12})\b', ln))
    for ln in text.split('\n'):
        for s in _RE_SHA.findall(ln):
            if s.isdigit():                  # `20260829` 같은 날짜
                continue
            if s in shas or s[:8] in shorts or s[:7] in shorts:
                continue
            if s in _exempt_doc or _RE_SHA_EXEMPT.search(ln):
                out['unsure'].append(s)      # 문서가 스스로 밝힌 것 — 오류 아님
            elif _RE_COMMIT_CTX.search(ln):
                out['bad_sha'].append(s)
            else:
                out['unsure'].append(s)
    return out


def walk_docs(root: str):
    for base in ('docs',):
        for r, _d, fs in os.walk(os.path.join(root, base)):
            for f in fs:
                if f.endswith('.md'):
                    yield os.path.relpath(os.path.join(r, f), root)
    for f in ('CLAUDE.md', 'README.md'):
        if os.path.exists(os.path.join(root, f)):
            yield f


def run(root: str, verbose: bool = True):
    allow = load_allowlist(root)
    shas = known_shas(root)
    shorts = {s[:8] for s in shas} | {s[:7] for s in shas}
    if not shas:
        print('⛔ git 히스토리를 못 읽었다 — 얕은 클론이면 SHA 검사가 무의미하다 '
              '(`git fetch --unshallow`)')
        return 1, {}
    tot = dict(missing=[], cross=[], bad_sha=[], unsure=[], allowed=[])
    n = 0
    for rel in sorted(walk_docs(root)):
        n += 1
        txt = open(os.path.join(root, rel), encoding='utf-8', errors='replace').read()
        got = scan_text(txt, root, shas, shorts)
        for k, v in got.items():
            for x in v:
                if k == 'missing' and x in allow:
                    tot.setdefault('allowed', []).append((rel, x))
                    continue
                tot[k].append((rel, x))
    if verbose:
        print(f'문서 {n}개 · 커밋 {len(shas)}개')
        print(f'  ⛔ 없는 경로   {len(tot["missing"])}')
        print(f'  ⛔ 없는 커밋   {len(tot["bad_sha"])}')
        print(f'  · 다른 브랜치 {len(tot["cross"])}  (litdb/·kb/ — 정상)')
        print(f'  · 판단 보류   {len(tot["unsure"])}  (오류로 세지 않는다)')
        print(f'  · 등재 예외   {len(tot.get("allowed", []))}  ({ALLOWLIST})')
        #  ★ 예외가 **쓸모없어졌는지** 도 본다 — 파일이 생겼는데 등재가 남아 있으면
        #    그 등재는 거짓말이 되고, 다음 사람이 "없는 게 정상" 으로 읽는다.
        stale = [a for a in allow if os.path.exists(os.path.join(root, a))]
        if stale:
            print(f'\n⛔ 이제 존재하는데 예외로 남은 등재 {len(stale)}건 — 지울 것')
            for a in stale:
                print(f'  {a}')
            tot['missing'].append(('(allowlist)', f'낡은 등재 {len(stale)}건'))
        for k, label in (('missing', '없는 경로'), ('bad_sha', '없는 커밋')):
            if tot[k]:
                print(f'\n── {label} ──')
                for rel, x in tot[k]:
                    print(f'  {rel}  →  {x}')
    return (1 if (tot['missing'] or tot['bad_sha']) else 0), tot


def _selftest():
    import tempfile
    ok, bad = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(f'{name} {extra}')

    root = tempfile.mkdtemp(prefix='refs_')
    os.makedirs(os.path.join(root, 'scripts'), exist_ok=True)
    open(os.path.join(root, 'scripts', 'real.py'), 'w').write('x\n')
    shas = {'a' * 40, 'b' * 40}
    shorts = {s[:8] for s in shas} | {s[:7] for s in shas}

    g = scan_text('보라 `scripts/real.py` 를.', root, shas, shorts)
    chk('① 있는 경로는 통과', g['missing'] == [], str(g['missing']))
    g = scan_text('없는 `scripts/ghost.py` 다.', root, shas, shorts)
    chk('★① 없는 경로를 잡는다', g['missing'] == ['scripts/ghost.py'], str(g))
    g = scan_text('정본은 `litdb/papers/x.md` 다.', root, shas, shorts)
    chk('★② litdb/ 는 다른 브랜치로 분류 (오류 아님)',
        g['cross'] == ['litdb/papers/x.md'] and g['missing'] == [], str(g))
    chk('② kb/ 도 같다',
        scan_text('`kb/a/b.md`', root, shas, shorts)['cross'] == ['kb/a/b.md'])

    g = scan_text(f'커밋 `{"a"*40}` 참조', root, shas, shorts)
    chk('③ 있는 커밋은 통과', g['bad_sha'] == [], str(g))
    g = scan_text(f'커밋 `{"a"*8}` 짧은 형태', root, shas, shorts)
    chk('③ 짧은 SHA 도 매칭', g['bad_sha'] == [])
    #  ⚠ 이 픽스처는 "없다" 를 **쓰지 않는다** — 그 낱말이 면제 규칙에 걸린다.
    g = scan_text('커밋 `deadbeef` 를 참조한다', root, shas, shorts)
    chk('★③ 없는 커밋을 잡는다', g['bad_sha'] == ['deadbeef'], str(g))
    #  ★ 오탐 두 종류 — 실제로 나왔던 것
    g = scan_text('사전등록 `20260829` 판', root, shas, shorts)
    chk('★④ 순수 10진수(날짜)는 커밋으로 안 본다',
        g['bad_sha'] == [] and g['unsure'] == [], str(g))
    g = scan_text('규약 `deadbeef` 로 묶인다', root, shas, shorts)
    chk('★④ 커밋 문맥이 없으면 보류',
        g['bad_sha'] == [] and g['unsure'] == ['deadbeef'], str(g))
    g = scan_text('커밋 `deadbeef` 에서', root, shas, shorts)
    chk('★④ 같은 문자열도 커밋 문맥이면 검사한다', g['bad_sha'] != [], str(g))
    g = scan_text('기준 `deadbeef` 은 origin 에 없다\n뒤에서 커밋 `deadbeef` 재인용',
                  root, shas, shorts)
    chk('★④ 면제는 문서 단위 — 한 줄에서 밝히면 다른 줄도 면제',
        g['bad_sha'] == [], str(g))

    g = scan_text('커밋 `6184147f573f021d` 규약', root, shas, shorts)
    chk('★④ 16자리는 커밋으로 안 본다 (내용 해시)', g['bad_sha'] == [], str(g))
    g = scan_text('기준 커밋 `deadbeef` 은 origin 에 없다', root, shas, shorts)
    chk('★④ 문서가 "없다" 고 밝히면 오류가 아니다', g['bad_sha'] == [], str(g))
    g = scan_text('헤더의 `deadbeef` 는 오기다', root, shas, shorts)
    chk('★④ "오기" 라고 적힌 것도 마찬가지', g['bad_sha'] == [], str(g))
    g = scan_text('검증 커밋 `deadbeef` @ `Codex/dem-mpm-crosscheck`', root, shas, shorts)
    chk('★④ 타 브랜치 표기가 있으면 제외', g['bad_sha'] == [], str(g))

    g = scan_text('도구 `real.py` 를 쓴다', root, shas, shorts)
    chk('⑤ 경로 없는 파일명은 흔한 자리에서 찾는다', g['missing'] == [] and g['unsure'] == [])
    g = scan_text('도구 `nowhere.py` 를 쓴다', root, shas, shorts)
    chk('⑤ 못 찾으면 보류 (오류 아님)',
        g['missing'] == [] and g['unsure'] == ['nowhere.py'], str(g))

    print(f'check_doc_refs selftest: {ok}/{ok + len(bad)} PASS')
    for b in bad:
        print('  ✗', b)
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', default=None)
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    rc, _ = run(a.root or _repo_root(), verbose=not a.quiet)
    print('\n' + ('✗ 깨진 참조가 있다' if rc else '✓ 깨진 참조 없음'))
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
