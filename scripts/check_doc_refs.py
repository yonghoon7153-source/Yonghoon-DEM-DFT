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

⚠ **길이로 가르지 않는다** (R19 P1-03).  초판은 *"7~12자만 커밋"* 으로 잘랐는데 그러면
  ⓐ 13~15자 축약을 통째로 못 보고 ⓑ 40자 **진짜 커밋** 세 건도 못 봤다.  내용 해시와
  커밋을 가르는 것은 길이가 아니라 **그 줄이 스스로 밝히는 종류**다 (`input_digest`·
  `sha(AM)`·`patch-id`).  길이 창은 7~40 이고, 판별은 `_RE_CONTENT_HASH` 가 한다.

═══ 왜 **전체 토큰**을 확인하나 ═══

초판은 `s[:8] in shorts or s[:7] in shorts` 로 **앞 7~8자만** 봤다.  그래서 실재하는
`7dbf38fb…` 가 있으면 **틀린** `7dbf38f0` 과 `7dbf38f0abcd` 가 둘 다 통과했다 —
검사가 잡으라고 만들어진 바로 그 오타를 통과시킨 것이다 (R19 P1-02).
지금은 토큰 **전체**가 도달 가능한 커밋의 접두인지 본다 (`_resolve`).

⚠ `git cat-file -e` 나 `rev-parse --verify` 로 바꾸지 말 것 — 그것들은 **객체 존재**만
  보므로 리베이스로 버려진 커밋이 로컬에 남아 있으면 통과한다 (원장 실사고:
  `findings.json` 의 `_commit_exists` 항목이 정확히 그 구멍으로 `c0ac0ad8` 8건을
  초록으로 만들었다).  기준은 `rev-list --all` **도달 가능성**이다.

═══ 부재 면제는 **명시 등재**로만 ═══

초판은 그 줄에 `없다`·`오기` 같은 낱말이 있으면 면제했고, 그 면제를 **문서 단위**로
넓혔다.  그러면 무관한 문장 하나가 문서 전체를 가려 준다 — 실측 반례:
`codex_absorb_verdict_20260825.md` 가 07 행에 *"증인이 없다"* 라고 적었다는 이유로
같은 표의 **정말 없는** `c0ac0ad8` 여덟 건이 전부 면제됐다 (그 변경은 이 브랜치에
`8bcfbeff` 로 들어가 있고 원장이 이미 그렇게 적고 있다).
⇒ 면제는 `SHA_EXCEPTIONS` 에 **(문서, 정확한 SHA, 대체 참조, 이유)** 로만 적는다.
  그 SHA 가 나중에 도달 가능해지면 등재 자체가 낡은 것이므로 검사기가 지적한다.
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

#: SHA 부재 예외.  **한 줄에 `문서<TAB>SHA<TAB>대체참조<TAB>이유`.**
#:  ⚠ 문서·SHA 가 **둘 다 정확히** 맞아야 면제된다 (초판의 문서 단위 자연어 면제가
#:    무관한 SHA 까지 가려 준 것이 R19 P1-03 이다).  대체참조가 hex 면 그것도 검증한다.
SHA_EXCEPTIONS = 'docs/reviews/doc_refs_sha_exceptions.tsv'


#: 등재의 **종류** — 이유를 산문으로 두면 검증할 수 없다 (R19 Q5 에서 22건 중 6건이
#: 사실과 달랐다).  종류마다 `ref` 칸의 뜻이 다르고, 검사기가 그것을 **확인한다**.
ALLOW_KINDS = {
    'absent':       '약속했으나 실행/커밋되지 않았다.  ref = `-`',
    'cross_branch': '다른 브랜치가 소유한다.  ref = 브랜치 이름 → 거기서 실재를 확인한다',
    'external':     '리포 밖 1차 증거.  ref = `sha256:<64hex>` 또는 위치 URI (반드시 적는다)',
    'generated':    '생성물·캐시 — 커밋 대상이 아니다.  ref = 만드는 명령',
}


def load_allowlist(root: str, verify_cross: bool = True):
    """→ {경로: (종류, ref, 이유)}.  그리고 확인 가능한 주장은 **확인한다**."""
    fp = os.path.join(root, ALLOWLIST)
    out, bad, soft = {}, [], []
    if not os.path.exists(fp):
        return out, bad, soft
    for i, ln in enumerate(open(fp, encoding='utf-8'), 1):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        parts = [x.strip() for x in ln.split('\t')]
        if len(parts) < 4 or not all(parts[:4]):
            raise SystemExit(f'⛔ {ALLOWLIST}:{i} (경로, 종류, ref, 이유) 4칸이 필요하다 '
                             f'— {ln!r}\n   종류: ' + ' · '.join(ALLOW_KINDS))
        path, kind, ref, why = parts[:4]
        if kind not in ALLOW_KINDS:
            raise SystemExit(f'⛔ {ALLOWLIST}:{i} 알 수 없는 종류 {kind!r} — '
                             + ' · '.join(ALLOW_KINDS))
        if kind == 'external':
            #  1차 증거는 **어디에 있는지**가 최소 요건이다 (빈칸·`-` 는 거부).
            if ref == '-' or len(ref) < 8:
                raise SystemExit(f'⛔ {ALLOWLIST}:{i} external 은 위치나 sha256 을 '
                                 f'적어야 한다 — {ref!r}')
            #  ⚠ 해시가 없으면 **막지는 않되 숨기지도 않는다**.  해시는 그 기계
            #    (사용자 WSL · ibb)에서 받아야 하므로 여기서 만들 수 없다 — 없는 것을
            #    있는 척하지 않고, 그렇다고 리포 전체를 세우지도 않는다.
            #    ⇒ 인용 전에 닫아야 할 **열린 항목**으로 보고한다 (R19 Q5).
            if not re.search(r'sha256:[0-9a-f]{64}', ref):
                soft.append(f'{path} — sha256 없음 (위치만: {ref})')
        if kind == 'cross_branch' and verify_cross:
            #  ★ "다른 브랜치 소관" 은 **확인 가능한 주장**이다.  실측: `webapp/data.py` 를
            #    "그쪽 저장소 소관" 이라 적었는데 실제로는 이 리포의 다른 브랜치에 있었다.
            r = subprocess.run(['git', '-C', root, 'cat-file', '-e', f'{ref}:{path}'],
                               capture_output=True)
            if r.returncode != 0:
                have = subprocess.run(['git', '-C', root, 'rev-parse', '--verify', '-q', ref],
                                      capture_output=True)
                bad.append(f'{path} — {ref} 에서 못 찾았다'
                           + ('' if have.returncode == 0 else f' (그 ref 자체가 없다; '
                                                              f'`git fetch origin {ref}` 후 재검사)'))
        out[path] = (kind, ref, why)
    return out, bad, soft

#: 리포 안 파일로 볼 확장자.
EXTS = ('py', 'sh', 'json', 'csv', 'md', 'mjs', 'js', 'yml', 'yaml', 'liggghts',
        'stl', 'npy', 'txt')

_RE_PATH = re.compile(
    r'`([A-Za-z0-9_][A-Za-z0-9_./+-]*\.(?:' + '|'.join(EXTS) + r'))`')
#: 커밋 축약은 7~12자다.  16자리는 이 리포에서 **내용 해시**(`sha(AM)` · `input_digest`)라
#: 커밋으로 보면 전부 오탐이 된다 (2026-08-31 실측: 그 길이의 오탐이 4/7).
_RE_SHA = re.compile(r'`([0-9a-f]{7,40})`')
#: 그 줄이 **스스로** 이 토큰을 커밋 아닌 **내용 해시**라고 밝힌다 — 종류 판별이지
#: 부재 면제가 아니다.  (부재 면제는 `SHA_EXCEPTIONS` 등재로만 한다.)
_RE_CONTENT_HASH = re.compile(r'digest|sha\(|sha256|SHA-256|patch-id|scaffold')
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


def is_shallow(root: str) -> bool:
    """얕은 클론인가.  ⚠ `rev-list --all` 은 얕아도 **뭔가**를 돌려주므로 그것만으로는
    못 잡는다 (R19 P1-03).  얕으면 도달 가능성 판정 자체가 무의미하다."""
    r = subprocess.run(['git', '-C', root, 'rev-parse', '--is-shallow-repository'],
                       capture_output=True, text=True)
    return r.stdout.strip() == 'true'


class Resolver:
    """토큰 **전체**가 도달 가능한 커밋의 접두인가.

    ⚠ 앞 7~8자만 비교하면 실재하는 `7dbf38fb…` 때문에 **틀린** `7dbf38f0` 이 통과한다
      (R19 P1-02 반례).  길이별 접두 집합을 만들어 **토큰 길이 그대로** 대조한다.
    """

    def __init__(self, shas):
        self._shas = shas
        self._by_len = {}

    def __call__(self, tok: str) -> bool:
        n = len(tok)
        if n not in self._by_len:
            self._by_len[n] = {s[:n] for s in self._shas}
        return tok in self._by_len[n]


def load_sha_exceptions(root: str, resolve=None):
    """→ {(문서, SHA): (대체참조, 이유)}.  등재가 스스로 낡았는지도 본다."""
    fp = os.path.join(root, SHA_EXCEPTIONS)
    out, stale = {}, []
    if not os.path.exists(fp):
        return out, stale
    for ln in open(fp, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        parts = [p.strip() for p in ln.split('\t')]
        if len(parts) < 4 or not all(parts[:4]):
            raise SystemExit(f'⛔ {SHA_EXCEPTIONS}: (문서, SHA, 대체참조, 이유) 4칸이 '
                             f'모두 필요하다 — {ln!r}')
        doc, sha, ref, why = parts[:4]
        if not re.fullmatch(r'[0-9a-f]{7,40}', sha):
            raise SystemExit(f'⛔ {SHA_EXCEPTIONS}: SHA 가 아니다 — {sha!r}')
        if not os.path.exists(os.path.join(root, doc)):
            raise SystemExit(f'⛔ {SHA_EXCEPTIONS}: 없는 문서를 가리킨다 — {doc}')
        if resolve is not None:
            #  ★ 등재가 낡았는지 두 방향으로 본다
            if resolve(sha):
                stale.append(f'{doc}  {sha}  — 이제 도달 가능하다.  등재를 지울 것')
            #  대체참조가 hex 면 그것은 **살아 있어야** 한다 ("이것으로 들어갔다" 는 주장)
            if re.fullmatch(r'[0-9a-f]{7,40}', ref) and not resolve(ref):
                stale.append(f'{doc}  {sha}  — 대체참조 {ref} 가 도달 불가.  주장이 거짓')
        out[(doc, sha)] = (ref, why)
    return out, stale


def scan_text(text: str, root: str, shas: set, shorts: set,
              resolve=None, exceptions=None, rel: str = ''):
    """한 문서의 참조를 분류한다.  → dict(missing, cross, bad_sha, unsure)."""
    if resolve is None:
        resolve = Resolver(shas)
    exceptions = exceptions or {}
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
    #  ★ 문맥은 **표 단위**로도 선다.  마크다운 표는 머리글에서 한 번 "커밋" 이라 밝히고
    #    각 행은 SHA 만 적는다 — 줄 단위로만 보면 그 열을 통째로 못 본다
    #    (실측: `codex_absorb_verdict_20260825.md` 의 `| # | 요지 | 커밋 |` 표 8행).
    table_ctx = False
    for ln in text.split('\n'):
        if ln.lstrip().startswith('|'):
            if _RE_COMMIT_CTX.search(ln):
                table_ctx = True
        else:
            table_ctx = False
        for s in _RE_SHA.findall(ln):
            if s.isdigit():                  # `20260829` 같은 날짜
                continue
            if resolve(s):                   # ★ 토큰 **전체**를 본다 (접두 비교 금지)
                continue
            if _RE_CONTENT_HASH.search(ln):
                out['unsure'].append(s)      # 커밋이 아니다 — 내용 해시라고 줄이 밝힌다
            elif (rel, s) in exceptions:
                out['unsure'].append(s)      # 등재된 부재 — 대체참조와 이유가 있다
            elif _RE_COMMIT_CTX.search(ln) or table_ctx:
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
    allow, allow_bad, allow_soft = load_allowlist(root)
    shas = known_shas(root)
    shorts = {s[:8] for s in shas} | {s[:7] for s in shas}
    if not shas:
        print('⛔ git 히스토리를 못 읽었다 — 얕은 클론이면 SHA 검사가 무의미하다 '
              '(`git fetch --unshallow`)')
        return 1, {}
    #  ★ 얕은 클론은 `rev-list --all` 이 **비어 보이지 않는다** — 잘린 조상이 전부
    #    "없는 커밋" 으로 둔갑해 거짓 경보를 낸다.  숫자가 있다고 안심하면 안 된다.
    if is_shallow(root):
        print('⛔ 얕은 클론이다 — 도달 가능성 판정이 성립하지 않는다 '
              '(`git fetch --unshallow`).  CI 는 `fetch-depth: 0` 이어야 한다.')
        return 1, {}
    resolve = Resolver(shas)
    exceptions, stale_exc = load_sha_exceptions(root, resolve)
    tot = dict(missing=[], cross=[], bad_sha=[], unsure=[], allowed=[])
    n = 0
    for rel in sorted(walk_docs(root)):
        n += 1
        txt = open(os.path.join(root, rel), encoding='utf-8', errors='replace').read()
        got = scan_text(txt, root, shas, shorts, resolve, exceptions, rel)
        for k, v in got.items():
            for x in v:
                if k == 'missing' and x in allow:
                    tot.setdefault('allowed', []).append((rel, x))
                    continue
                tot[k].append((rel, x))
    if stale_exc:
        tot['bad_sha'].append(('(sha_exceptions)', f'낡은 등재 {len(stale_exc)}건'))
    #  ★ allowlist 의 **확인 가능한 주장**이 거짓이면 그것도 오류다 (R19 Q5)
    if allow_bad:
        tot['missing'].append(('(allowlist)', f'확인 실패 {len(allow_bad)}건'))
    if verbose:
        print(f'문서 {n}개 · 커밋 {len(shas)}개 · SHA 예외 {len(exceptions)}건')
        if stale_exc:
            print(f'\n⛔ 낡은 SHA 예외 {len(stale_exc)}건 — {SHA_EXCEPTIONS}')
            for s in stale_exc:
                print(f'  {s}')
        if allow_bad:
            print(f'\n⛔ allowlist 주장 확인 실패 {len(allow_bad)}건 — {ALLOWLIST}')
            for a in allow_bad:
                print(f'  {a}')
        if allow_soft:
            print(f'\n⚠ 리포 밖 1차 증거 {len(allow_soft)}건에 sha256 이 없다 '
                  f'— 그 값을 인용하기 전에 해당 기계에서 받아 적을 것 (오류 아님)')
            for a in allow_soft:
                print(f'  {a}')
        print(f'  ⛔ 없는 경로   {len(tot["missing"])}')
        print(f'  ⛔ 없는 커밋   {len(tot["bad_sha"])}')
        print(f'  · 다른 브랜치 {len(tot["cross"])}  (litdb/·kb/ — 정상)')
        print(f'  · 판단 보류   {len(tot["unsure"])}  (오류로 세지 않는다)')
        print(f'  · 등재 예외   {len(tot.get("allowed", []))}  ({ALLOWLIST})')
        #  ★ 예외가 **쓸모없어졌는지** 도 본다 — 파일이 생겼는데 등재가 남아 있으면
        #    그 등재는 거짓말이 되고, 다음 사람이 "없는 게 정상" 으로 읽는다.
        #  ★ `generated` 는 로컬에 **생기는 것이 정상**이다 (gitignore 대상).  실측:
        #    selftest 를 돌리면 `litdb_cache/…` 가 생겨 옳은 등재가 "낡았다" 고 찍혔다.
        #    그 종류에 대해서는 존재가 아니라 **커밋되지 않는가**를 본다.
        stale = [a for a, (k, _r, _w) in allow.items()
                 if k != 'generated' and os.path.exists(os.path.join(root, a))]
        leaked = []
        for a, (k, _r, _w) in allow.items():
            if k != 'generated' or not os.path.exists(os.path.join(root, a)):
                continue
            _ig = subprocess.run(['git', '-C', root, 'check-ignore', '-q', a],
                                 capture_output=True)
            _tr = subprocess.run(['git', '-C', root, 'ls-files', '--error-unmatch', a],
                                 capture_output=True)
            if _ig.returncode != 0 or _tr.returncode == 0:
                leaked.append(a)
        if leaked:
            print(f'\n⛔ generated 인데 gitignore 밖이거나 커밋돼 있다 {len(leaked)}건')
            for a in leaked:
                print(f'  {a}')
            tot['missing'].append(('(allowlist)', f'generated 누수 {len(leaked)}건'))
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
    g = scan_text('커밋 `deadbeef` 를 참조한다', root, shas, shorts)
    chk('★③ 없는 커밋을 잡는다', g['bad_sha'] == ['deadbeef'], str(g))

    #  ══ R19 P1-02 — 전체 토큰을 봐야 한다 ═════════════════════════════
    #  실재 `aaaaaaaa…` 옆에서 **틀린** 토큰이 앞자리만 같으면 옛 판은 통과시켰다.
    g = scan_text('커밋 `' + 'a' * 7 + 'b`', root, shas, shorts)
    chk('★★ P1-02 앞 7자만 같은 틀린 SHA 를 잡는다', g['bad_sha'] == ['a' * 7 + 'b'], str(g))
    g = scan_text('커밋 `' + 'a' * 8 + 'bcdef`', root, shas, shorts)
    chk('★★ P1-02 접두가 맞아도 뒤가 틀리면 잡는다',
        g['bad_sha'] == ['a' * 8 + 'bcdef'], str(g))
    g = scan_text('커밋 `' + 'a' * 14 + '`', root, shas, shorts)
    chk('★★ P1-03 13~15자 축약도 검사 대상이다 (옛 12자 상한이 통째로 놓쳤다)',
        g['bad_sha'] == [] and g['unsure'] == [], str(g))
    g = scan_text('커밋 `' + 'c' * 14 + '`', root, shas, shorts)
    chk('★★ P1-03 그 길이의 **틀린** SHA 는 잡는다',
        g['bad_sha'] == ['c' * 14], str(g))
    chk('★★ Resolver 는 길이별로 정확 대조', Resolver(shas)('a' * 12)
        and not Resolver(shas)('a' * 11 + 'b'))
    #  ★ 오탐 두 종류 — 실제로 나왔던 것
    g = scan_text('사전등록 `20260829` 판', root, shas, shorts)
    chk('★④ 순수 10진수(날짜)는 커밋으로 안 본다',
        g['bad_sha'] == [] and g['unsure'] == [], str(g))
    g = scan_text('규약 `deadbeef` 로 묶인다', root, shas, shorts)
    chk('★④ 커밋 문맥이 없으면 보류',
        g['bad_sha'] == [] and g['unsure'] == ['deadbeef'], str(g))
    g = scan_text('커밋 `deadbeef` 에서', root, shas, shorts)
    chk('★④ 같은 문자열도 커밋 문맥이면 검사한다', g['bad_sha'] != [], str(g))
    g = scan_text('커밋 `6184147f573f021d` 의 `input_digest`', root, shas, shorts)
    chk('★④ 줄이 내용 해시라 밝히면 커밋으로 안 본다', g['bad_sha'] == [], str(g))
    g = scan_text('| sha(AM) | `6184147f573f021d` |', root, shas, shorts)
    chk('★④ `sha(…)` 표기도 같다', g['bad_sha'] == [], str(g))

    #  ══ R19 P1-03 — 자연어 면제가 **무관한 SHA 를 가려 준다** ═══════════════
    #  Codex 반례: `codex_absorb_verdict_20260825.md` 가 07 행에 "증인이 없다" 라고
    #  적었다는 이유로 같은 표의 정말 없는 `c0ac0ad8` 여덟 건이 전부 면제됐다.
    doc = 'docs/x.md'
    txt = ('| # | 요지 | 커밋 |\n|---|---|---|\n'
           '| 07 | 구현은 옳으나 증인이 없다 | `deadbeef` |\n'
           '| 08 | 무관한 항목 | `feedface` |')
    chk('★★ 표 머리글이 "커밋" 이면 각 행도 검사 대상 (행에는 그 낱말이 없다)',
        scan_text(txt, root, shas, shorts)['bad_sha'] != [], '표 열을 통째로 놓쳤다')
    g = scan_text(txt, root, shas, shorts, rel=doc)
    chk('★★ P1-03 무관한 줄의 "없다" 가 다른 SHA 를 면제하지 않는다',
        sorted(g['bad_sha']) == ['deadbeef', 'feedface'], str(g))
    exc = {(doc, 'deadbeef'): ('8bcfbeff', '리베이스 이전 SHA')}
    g = scan_text(txt, root, shas, shorts, exceptions=exc, rel=doc)
    chk('★★ P1-03 등재된 (문서, SHA) 만 면제된다',
        g['bad_sha'] == ['feedface'], str(g))
    g = scan_text(txt, root, shas, shorts, exceptions=exc, rel='docs/other.md')
    chk('★★ P1-03 다른 문서에서는 같은 SHA 도 면제 안 된다',
        sorted(g['bad_sha']) == ['deadbeef', 'feedface'], str(g))

    #  ══ 등재 자체의 자기검사 ════════════════════════════════════════════
    exdir = tempfile.mkdtemp(prefix='refs_exc_')
    os.makedirs(os.path.join(exdir, 'docs', 'reviews'), exist_ok=True)
    open(os.path.join(exdir, 'docs', 'x.md'), 'w').write('x\n')
    fp = os.path.join(exdir, SHA_EXCEPTIONS)

    def _write(line):
        open(fp, 'w', encoding='utf-8').write(line + '\n')

    _write('docs/x.md\tdeadbeef\t' + 'a' * 40)
    try:
        load_sha_exceptions(exdir)
        chk('★ 이유 없는 등재를 거부', False, '통과해 버렸다')
    except SystemExit:
        chk('★ 이유 없는 등재를 거부', True)
    _write('docs/ghost.md\tdeadbeef\t-\t이유')
    try:
        load_sha_exceptions(exdir)
        chk('★ 없는 문서를 가리키는 등재를 거부', False, '통과해 버렸다')
    except SystemExit:
        chk('★ 없는 문서를 가리키는 등재를 거부', True)
    _write('docs/x.md\tdeadbeef\t-\t이유')
    got, st = load_sha_exceptions(exdir, Resolver(shas))
    chk('★ 옳은 등재는 통과', got == {('docs/x.md', 'deadbeef'): ('-', '이유')} and st == [],
        f'{got} {st}')
    _write('docs/x.md\t' + 'a' * 8 + '\t-\t이유')
    _, st = load_sha_exceptions(exdir, Resolver(shas))
    chk('★★ 도달 가능해진 SHA 의 등재는 낡았다고 지적', len(st) == 1, str(st))
    _write('docs/x.md\tdeadbeef\tfeedface\t이 커밋으로 들어갔다')
    _, st = load_sha_exceptions(exdir, Resolver(shas))
    chk('★★ 대체참조가 도달 불가면 그 주장이 거짓이라고 지적', len(st) == 1, str(st))

    #  ══ R19 Q5 — allowlist 이유가 **확인 가능한 주장**인가 ═══════════════════
    aldir = tempfile.mkdtemp(prefix='refs_al_')
    os.makedirs(os.path.join(aldir, 'docs', 'reviews'), exist_ok=True)
    afp = os.path.join(aldir, ALLOWLIST)

    def _wa(line):
        open(afp, 'w', encoding='utf-8').write(line + '\n')

    _wa('docs/x.csv\t미실행이다')
    try:
        load_allowlist(aldir, verify_cross=False)
        chk('★⑥ 옛 2칸 등재를 거부 (종류·ref 를 요구)', False, '통과해 버렸다')
    except SystemExit:
        chk('★⑥ 옛 2칸 등재를 거부 (종류·ref 를 요구)', True)
    _wa('docs/x.csv\tmaybe\t-\t이유')
    try:
        load_allowlist(aldir, verify_cross=False)
        chk('★⑥ 알 수 없는 종류를 거부', False, '통과해 버렸다')
    except SystemExit:
        chk('★⑥ 알 수 없는 종류를 거부', True)
    _wa('docs/x.csv\texternal\t-\t리포 밖')
    try:
        load_allowlist(aldir, verify_cross=False)
        chk('★⑥ external 인데 위치가 없으면 거부', False, '통과해 버렸다')
    except SystemExit:
        chk('★⑥ external 인데 위치가 없으면 거부', True)
    _wa('docs/x.csv\texternal\tibb ~/dem_test/x\t1차 증거')
    _a, _b, _s = load_allowlist(aldir, verify_cross=False)
    chk('★★⑥ external 인데 sha256 이 없으면 **보고**한다 (막지는 않는다)',
        _b == [] and len(_s) == 1, f'{_b} {_s}')
    _wa('docs/x.csv\texternal\tsha256:' + 'a' * 64 + '\t1차 증거')
    _a, _b, _s = load_allowlist(aldir, verify_cross=False)
    chk('⑥ 해시를 적으면 조용하다', _b == [] and _s == [], f'{_b} {_s}')
    #  ★ cross_branch 는 **그 ref 에서 실제로 찾아본다**.  픽스처에 진짜 git 저장소를
    #    하나 만들어 확인한다 (이 리포를 건드리지 않는다).
    _env = dict(os.environ, GIT_AUTHOR_NAME='t', GIT_AUTHOR_EMAIL='t@t',
                GIT_COMMITTER_NAME='t', GIT_COMMITTER_EMAIL='t@t')

    def _git(*a):
        return subprocess.run(['git', '-C', aldir, *a], capture_output=True, env=_env)
    _git('init', '-q')
    open(os.path.join(aldir, 'docs', 'x.csv'), 'w').write('a\n')
    _git('add', '-A')
    _git('commit', '-qm', 'x')
    if _git('rev-parse', '--verify', '-q', 'HEAD').returncode == 0:
        _wa('docs/x.csv\tcross_branch\tHEAD\t그 ref 에 있다')
        _a, _b, _s = load_allowlist(aldir, verify_cross=True)
        chk('⑥ cross_branch 주장이 참이면 조용하다', _b == [], str(_b))
        _wa('docs/ghost.csv\tcross_branch\tHEAD\t있다고 주장한다')
        _a, _b, _s = load_allowlist(aldir, verify_cross=True)
        chk('★★⑥ cross_branch 주장이 거짓이면 잡는다 (그 ref 에 없다)',
            any('ghost' in x for x in _b), str(_b))
        _wa('docs/x.csv\tcross_branch\torigin/no-such-branch\t있다고 주장한다')
        _a, _b, _s = load_allowlist(aldir, verify_cross=True)
        chk('★⑥ ref 자체가 없으면 그렇게 말한다 (fetch 안내)',
            any('그 ref 자체가 없다' in x for x in _b), str(_b))
    else:
        chk('⑥ cross_branch 검증 (git 없음 — 건너뜀)', True)

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
