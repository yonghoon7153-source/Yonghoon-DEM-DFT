#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""wiki lint — 기계 점검 (wiki/SCHEMA.md 의 집행기).

Karpathy LLM-wiki 패턴(구요한 llm-wiki-kit v1.7)의 lint 개념을 이 리포 규약으로
재구현했다.  킷과 다른 검사 (★ = 우리 특칙):
  ★ 모델 ID 패턴 = **오류** (푸시 산출물에 모델 식별자 금지 — 리포 규칙),
    `model:`/`effort:` frontmatter 키도 오류 (author 로 대체).
  ★ sources 는 **리포 상대경로**로 존재 검사 (킷은 위키-내부 raw/ 만) ·
    `litdb-canon:<slug>` 는 형식만 (정본은 다른 브랜치라 로컬 존재검사 불가) ·
    URL 은 통과 · `:line` 접미는 떼고 검사.
  ★ `evidenceScope: single-source` + `confidence: high` = **오류** (킷은 경고;
    greenfield 라 처음부터 막는다 — 근거 폭이 confidence 상한).
  ★ anchored/scope (§F1 · 등급 A/B) enum 검사.
공통 검사: frontmatter 필수키·타입↔폴더 일치·enum·verified 짝필드·위키링크 해소·
링크 2개 미만(경고)·index 양방향 커버리지+Total 카운트·고아(경고)·stale 90일(경고)·
RQ status·description 따옴표(경고).

사용: python3 wiki/tools/lint.py [--selftest]     exit 0 = 오류 없음 (경고 허용)
"""
from __future__ import annotations

import datetime
import glob
import os
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent          # wiki/
REPO = BASE.parent                                             # 리포 루트
DIRS = ['concepts', 'entities', 'comparisons', 'queries', 'guides',
        'questions', 'syntheses']
TYPE_BY_DIR = {'concepts': 'concept', 'entities': 'entity',
               'comparisons': 'comparison', 'queries': 'query', 'guides': 'guide',
               'questions': 'research-question', 'syntheses': 'synthesis'}
REQ = ['title', 'created', 'updated', 'type', 'tags', 'sources', 'confidence',
       'explored', 'verificationStatus', 'author', 'claimType', 'evidenceScope']
ENUMS = {
    'confidence': {'high', 'medium', 'low'},
    'verificationStatus': {'unverified', 'verified', 'disputed'},
    'author': {'agent', 'human', 'both'},
    'claimType': {'definition', 'empirical', 'theoretical', 'historical',
                  'prescriptive', 'interpretive', 'mixed'},
    'evidenceScope': {'single-source', 'multi-source-primary', 'multi-source-mixed',
                      'synthesis-only', 'user-original'},
    'anchored': {'anchored', 'assumed', 'mixed', 'n-a'},
    'scope': {'absolute', 'relative-only', 'n-a'},
    'verifiedBy': {'agent', 'human', 'both'},
}
RQ_STATUS = {'open', 'active', 'answered', 'abandoned'}
STALE_DAYS = 90
#: ★ 모델 식별자 — 페이지 본문/frontmatter 어디에도 금지 (리포 규칙: 푸시 산출물 배제)
MODEL_ID = re.compile(r'claude-(?:opus|sonnet|haiku|fable)[a-z0-9.\-]*', re.I)
LITDB_REF = re.compile(r'^litdb-canon:[a-z0-9_.\-]+$')


def parse_fm(s):
    fm = {}
    for line in s.splitlines():
        m = re.match(r'^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def strip_code(text):
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', '', text)


def split_sources(raw):
    """frontmatter sources 값 → 토큰 리스트.  `[a, b]` 인라인 리스트 규약."""
    raw = raw.strip()
    if raw.startswith('[') and raw.endswith(']'):
        raw = raw[1:-1]
    return [t.strip().strip('"\'') for t in raw.split(',') if t.strip()]


def collect(base=BASE, repo=None, today=None):
    """→ (errors, warnings).  순수 함수 — selftest 가 임시 트리로 부른다."""
    repo = repo or base.parent
    today = today or datetime.date.today()
    errors, warnings = [], []

    pages = {}
    for d in DIRS:
        for f in glob.glob(str(base / d / '*.md')):
            p = pathlib.Path(f)
            if p.stem in pages:
                errors.append(f'{p.name}: 같은 slug 가 {pages[p.stem].parent.name}/ 에도 있음')
            pages[p.stem] = p

    fm_by, outbound = {}, {}
    for stem, p in sorted(pages.items()):
        text = p.read_text(encoding='utf-8')
        rel = f'{p.parent.name}/{p.name}'
        # ★ 모델 ID — frontmatter/본문 전체
        for hit in MODEL_ID.findall(text):
            errors.append(f'{rel}: 모델 ID 금지 — "{hit}" (리포 규칙; author 필드만)')
        m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        if not m:
            errors.append(f'{rel}: frontmatter 없음')
            continue
        fm = parse_fm(m.group(1))
        fm_by[stem] = fm
        for k in ('model', 'effort'):
            if k in fm:
                errors.append(f'{rel}: `{k}:` 키 금지 — author 로 대체 (SCHEMA 경계 규칙 2)')
        for k in REQ:
            if k not in fm:
                errors.append(f'{rel}: frontmatter `{k}` 누락')
        want = TYPE_BY_DIR[p.parent.name]
        if fm.get('type') and fm['type'] != want:
            errors.append(f'{rel}: type={fm["type"]} ≠ 폴더 규약 {want}')
        for k, allowed in ENUMS.items():
            if k in fm and fm[k] and fm[k] not in allowed:
                errors.append(f'{rel}: {k}={fm[k]} — 허용값 {sorted(allowed)}')
        if fm.get('verificationStatus') == 'verified':
            for k in ('verifiedAt', 'verifiedBy'):
                if not fm.get(k):
                    errors.append(f'{rel}: verified 인데 `{k}` 없음')
        if fm.get('type') == 'research-question':
            if fm.get('status') not in RQ_STATUS:
                errors.append(f'{rel}: research-question status={fm.get("status")} — 허용 {sorted(RQ_STATUS)}')
        if fm.get('evidenceScope') == 'single-source' and fm.get('confidence') == 'high':
            errors.append(f'{rel}: single-source 인데 confidence high — 근거 폭이 상한 (SCHEMA)')
        if 'description' in fm and fm['description'] and ':' in fm['description'] \
                and not (fm['description'].startswith('"') or fm['description'].startswith("'")):
            warnings.append(f'{rel}: description 에 콜론 — 따옴표로 감쌀 것 (YAML 보호)')
        # sources 존재 검사
        for src in split_sources(fm.get('sources', '')):
            if src.startswith(('http://', 'https://')):
                continue
            if src.startswith('litdb-canon:'):
                if not LITDB_REF.match(src):
                    errors.append(f'{rel}: litdb 참조 형식 위반 — {src} (litdb-canon:<slug>)')
                continue
            path = src.split(':')[0] if re.search(r':\d+$', src) else src
            if not (repo / path).exists():
                errors.append(f'{rel}: source 경로 없음 — {path}')
        # stale
        try:
            upd = datetime.date.fromisoformat(fm.get('updated', ''))
            if (today - upd).days > STALE_DAYS:
                warnings.append(f'{rel}: stale — updated {fm["updated"]} ({(today - upd).days}일)')
        except ValueError:
            errors.append(f'{rel}: updated 날짜 형식 위반 — {fm.get("updated")!r}')
        links = set(re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]', strip_code(text)))
        outbound[stem] = links
        for tgt in links:
            if tgt not in pages:
                errors.append(f'{rel}: 깨진 위키링크 [[{tgt}]]')
        if len(links) < 2:
            warnings.append(f'{rel}: 위키링크 {len(links)}개 (<2)')

    # 고아 (다른 페이지에서 들어오는 링크 0)
    for stem in pages:
        if not any(stem in lk for s, lk in outbound.items() if s != stem):
            warnings.append(f'{pages[stem].parent.name}/{stem}.md: 고아 — 들어오는 링크 없음')

    # index 양방향
    idx = base / 'index.md'
    if not idx.exists():
        errors.append('index.md 없음')
    else:
        itext = idx.read_text(encoding='utf-8')
        listed = set(re.findall(r'\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]', strip_code(itext)))
        for stem in pages:
            if stem not in listed:
                errors.append(f'index.md: [[{stem}]] 미등록')
        for stem in listed:
            if stem not in pages:
                errors.append(f'index.md: 존재하지 않는 페이지 [[{stem}]]')
        m = re.search(r'Total pages:\s*(\d+)', itext)
        if not m:
            errors.append('index.md: "Total pages: N" 없음')
        elif int(m.group(1)) != len(pages):
            errors.append(f'index.md: Total pages {m.group(1)} ≠ 실제 {len(pages)}')
    return errors, warnings


# ───────────────────────────── selftest ─────────────────────────────

_GOOD_FM = ('---\ntitle: T\ncreated: {d}\nupdated: {d}\ntype: {t}\ntags: [wiki]\n'
            'sources: [{src}]\nconfidence: {conf}\nexplored: false\n'
            'verificationStatus: unverified\nauthor: agent\nclaimType: definition\n'
            'evidenceScope: {es}\n{extra}---\n')


def _mk(base, folder, stem, *, t=None, src='SCHEMA.md', conf='medium',
        es='single-source', extra='', body=''):
    t = t or TYPE_BY_DIR[folder]
    d = datetime.date.today().isoformat()
    (base / folder).mkdir(parents=True, exist_ok=True)
    (base / folder / f'{stem}.md').write_text(
        _GOOD_FM.format(d=d, t=t, src=src, conf=conf, es=es, extra=extra) + body,
        encoding='utf-8')


def _index(base, stems, total=None):
    n = total if total is not None else len(stems)
    (base / 'index.md').write_text(
        f'# Wiki Index\n\nTotal pages: {n}\n\n' +
        '\n'.join(f'- [[{s}]]' for s in stems) + '\n', encoding='utf-8')


def _selftest():
    import shutil
    import tempfile
    ok = fail = 0

    def chk(msg, cond):
        nonlocal ok, fail
        print(('  PASS  ' if cond else '  FAIL  ') + msg)
        ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)

    tmp = pathlib.Path(tempfile.mkdtemp())
    base = tmp / 'wiki'
    try:
        (tmp / 'docs').mkdir(parents=True)
        (tmp / 'docs' / 'real.md').write_text('x', encoding='utf-8')
        base.mkdir()
        (base / 'SCHEMA.md').write_text('s', encoding='utf-8')
        # 서로 링크하는 건강한 페이지 둘 (SCHEMA.md 는 wiki/ 밑이라 repo 상대로 wiki/SCHEMA.md)
        _mk(base, 'concepts', 'alpha', src='docs/real.md, litdb-canon:some-card',
            body='[[beta]] 와 [[beta|별칭]] 그리고 [[beta]]\n[[beta]] [[beta]]\n')
        _mk(base, 'entities', 'beta', src='https://example.com/x',
            body='[[alpha]] 링크 둘: [[alpha]]\n')
        _index(base, ['alpha', 'beta'])
        e, w = collect(base, tmp)
        chk('1) 건강한 위키 = 0 오류', not e)
        chk('2) alpha 링크 1종(beta)뿐 → <2 경고', any('alpha' in x and '<2' in x for x in w))

        # 모델 ID 금지
        _mk(base, 'concepts', 'bad-model', src='docs/real.md',
            body='[[alpha]] [[beta]] 어떤 모델이 썼나: claude-' + 'fable-5\n')
        _index(base, ['alpha', 'beta', 'bad-model'])
        e, _ = collect(base, tmp)
        chk('3) ★ 본문 모델 ID = 오류', any('모델 ID' in x for x in e))
        _mk(base, 'concepts', 'bad-model', src='docs/real.md',
            extra='model: something\n', body='[[alpha]] [[beta]]\n')
        e, _ = collect(base, tmp)
        chk('4) ★ `model:` 키 = 오류', any('`model:` 키 금지' in x for x in e))
        (base / 'concepts' / 'bad-model.md').unlink()
        _index(base, ['alpha', 'beta'])

        # sources
        _mk(base, 'concepts', 'bad-src', src='docs/ghost.md', body='[[alpha]] [[beta]]\n')
        _index(base, ['alpha', 'beta', 'bad-src'])
        e, _ = collect(base, tmp)
        chk('5) ★ 없는 source 경로 = 오류', any('source 경로 없음' in x for x in e))
        _mk(base, 'concepts', 'bad-src', src='litdb-canon:BAD SLUG!', body='[[alpha]] [[beta]]\n')
        e, _ = collect(base, tmp)
        chk('6) ★ litdb-canon 형식 위반 = 오류', any('litdb 참조 형식' in x for x in e))
        _mk(base, 'concepts', 'bad-src', src='scripts/x.py:42', body='[[alpha]] [[beta]]\n')
        (tmp / 'scripts').mkdir(exist_ok=True)
        (tmp / 'scripts' / 'x.py').write_text('', encoding='utf-8')
        e, _ = collect(base, tmp)
        chk('7) `:line` 접미는 떼고 존재 검사', not any('source' in x for x in e))
        (base / 'concepts' / 'bad-src.md').unlink()
        _index(base, ['alpha', 'beta'])

        # single-source + high = 오류 (킷은 경고였다 — 우리 상향)
        _mk(base, 'concepts', 'over', src='docs/real.md', conf='high',
            body='[[alpha]] [[beta]]\n')
        _index(base, ['alpha', 'beta', 'over'])
        e, _ = collect(base, tmp)
        chk('8) ★ single-source+high = 오류', any('근거 폭이 상한' in x for x in e))
        (base / 'concepts' / 'over.md').unlink()

        # index 커버리지 + 카운트
        _index(base, ['alpha'], total=2)
        e, _ = collect(base, tmp)
        chk('9) index 미등록 = 오류', any('미등록' in x for x in e))
        _index(base, ['alpha', 'beta', 'ghost'])
        e, _ = collect(base, tmp)
        chk('10) index 유령 링크 = 오류', any('존재하지 않는' in x for x in e))
        _index(base, ['alpha', 'beta'], total=99)
        e, _ = collect(base, tmp)
        chk('11) Total pages 불일치 = 오류', any('Total pages' in x for x in e))
        _index(base, ['alpha', 'beta'])

        # 깨진 위키링크 · 고아 · 코드 블록 제외
        _mk(base, 'guides', 'gamma', src='docs/real.md',
            body='[[alpha]] [[nope]]\n```\n[[in-code-ignored]]\n```\n')
        _index(base, ['alpha', 'beta', 'gamma'])
        e, w = collect(base, tmp)
        chk('12) 깨진 링크 [[nope]] = 오류 · 코드는 제외',
            any('[[nope]]' in x for x in e) and not any('in-code' in x for x in e))
        chk('13) 고아 경고 (gamma 로 들어오는 링크 없음)', any('gamma' in x and '고아' in x for x in w))

        # RQ status + stale
        _mk(base, 'questions', 'rq1', src='docs/real.md',
            extra='status: wrong\n', body='[[alpha]] [[beta]]\n')
        _index(base, ['alpha', 'beta', 'gamma', 'rq1'])
        e, _ = collect(base, tmp)
        chk('14) RQ status enum = 오류', any('research-question status' in x for x in e))
        old = (base / 'concepts' / 'alpha.md').read_text(encoding='utf-8')
        (base / 'concepts' / 'alpha.md').write_text(
            re.sub(r'updated: .*', 'updated: 2025-01-01', old), encoding='utf-8')
        _, w = collect(base, tmp)
        chk('15) stale 경고 (90일)', any('stale' in x for x in w))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\nwiki lint selftest: {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1


def main():
    if '--selftest' in sys.argv:
        return _selftest()
    errors, warnings = collect()
    for e in errors:
        print(f'ERROR  {e}')
    for w in warnings:
        print(f'warn   {w}')
    n_pages = sum(len(glob.glob(str(BASE / d / "*.md"))) for d in DIRS)
    print(f'\n{n_pages} pages · {len(errors)} errors · {len(warnings)} warnings')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
