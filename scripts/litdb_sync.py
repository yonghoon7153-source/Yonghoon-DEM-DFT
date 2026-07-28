#!/usr/bin/env python3
"""litdb 통합 인덱서 — 흩어진 논문 digest 를 한 곳에서 찾을 수 있게 (브랜치 체크아웃 불필요).

왜 필요한가 (2026-07-28 실측 문제):
  논문 에이전트가 만든 digest 가 **세 군데 다른 서랍**에 흩어져 있었다 —
    ① `litdb/papers/*.md`  정본 브랜치 claude/friendly-meitner-lldvar (118장)
    ② `docs/lit_*.md`      작업 브랜치 claude/solid-state-cathode-improvement-hevry0 (29장)
                            ← **이용민 교수님 DT 계보 4편이 여기 있었다**(416~628줄 풀 digest)
    ③ `litdb/papers/*.md`  이 브랜치의 2026-07-16 동결 스냅샷 (65장)
  그 결과 "이용민 논문이 litdb 에 없다"는 **오진**이 나왔다.  실제로는 있었고, 다른 서랍이라
  안 보였을 뿐이다.  또 webapp 에는 litdb 참조가 0건이라, 파이프라인이 문헌을 볼 수 없었다.

무엇을 하나:
  git plumbing(`git ls-tree` / `git show`)으로 **어떤 브랜치도 체크아웃하지 않고** 모든 digest 를
  읽어 로컬 캐시 + 검색 인덱스를 만든다.  worktree 도, 브랜치 전환도 필요 없다.
  캐시는 재생성 가능하므로 gitignore 대상 (정본은 여전히 각 브랜치의 원본).

사용:
  python3 scripts/litdb_sync.py --sync              # 전 브랜치 스캔 → 캐시+인덱스 갱신
  python3 scripts/litdb_sync.py --search "이용민 digital twin"
  python3 scripts/litdb_sync.py --show park2020_digitaltwin_assb_foundational
  python3 scripts/litdb_sync.py --stats             # 서랍별 통계 + 중복 진단
  python3 scripts/litdb_sync.py --selftest
"""
import argparse
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(REPO, 'litdb_cache')
INDEX = os.path.join(CACHE, 'index.json')

# 서랍 정의 — (브랜치 glob 우선순위, 경로 패턴, 종류).  우선순위 = 같은 슬러그 충돌 시 이기는 순서.
DRAWERS = [
    {'name': 'canonical', 'branch': 'claude/friendly-meitner-lldvar',
     'pattern': r'^litdb/papers/(?!_TEMPLATE)[^/]+\.md$', 'kind': 'card', 'rank': 0,
     'note': 'litdb 정본 서랍 (CLAUDE.md 단일-서랍 규칙)'},
    {'name': 'worknotes', 'branch': 'claude/solid-state-cathode-improvement-hevry0',
     'pattern': r'^docs/lit_[^/]+\.md$', 'kind': 'note', 'rank': 1,
     'note': '건식후막 작업 브랜치의 풀 digest (정본 미승격)'},
    {'name': 'frozen', 'branch': 'claude/stoic-knuth-NObVQ',
     'pattern': r'^litdb/papers/(?!_TEMPLATE)[^/]+\.md$', 'kind': 'card', 'rank': 2,
     'note': '이 브랜치의 2026-07-16 동결 스냅샷 (참조 전용)'},
]
# 인덱스에 함께 실을 큐레이션/포지셔닝 문서 (카드가 아니라 맥락 문서)
CONTEXT_DOCS = [
    ('claude/solid-state-cathode-improvement-hevry0', 'docs/literature_yonsei_dtbl_2026.md'),
    ('claude/solid-state-cathode-improvement-hevry0', 'docs/positioning_vs_geodict.md'),
    ('claude/solid-state-cathode-improvement-hevry0', 'litdb/DRY_THICKFILM_INDEX.md'),
    ('claude/friendly-meitner-lldvar', 'litdb/INDEX.md'),
    ('claude/friendly-meitner-lldvar', 'litdb/comparison_vs_ours.md'),
]


def _git(*args, ok_fail=False):
    r = subprocess.run(['git', '-C', REPO] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        if ok_fail:
            return None
        raise SystemExit(f'git {" ".join(args[:2])} 실패: {r.stderr.strip()[:200]}')
    return r.stdout


def _ref(branch):
    """origin/<branch> 우선, 없으면 로컬 <branch>.  둘 다 없으면 None."""
    for ref in (f'origin/{branch}', branch):
        if _git('rev-parse', '--verify', '-q', ref, ok_fail=True):
            return ref
    return None


def _slug(path):
    b = os.path.basename(path)[:-3]                          # .md 제거
    return b[4:] if b.startswith('lit_') else b              # docs/lit_x.md ↔ papers/x.md 슬러그 통일


def _title(text, slug):
    for ln in text.split('\n'):
        if ln.startswith('# '):
            return ln[2:].strip()
    return slug


def sync(verbose=True):
    os.makedirs(CACHE, exist_ok=True)
    entries, missing = {}, []
    for d in DRAWERS:
        ref = _ref(d['branch'])
        if ref is None:
            missing.append(d['branch']); continue
        listing = _git('ls-tree', '-r', '--name-only', ref) or ''
        pat = re.compile(d['pattern'])
        n = 0
        for path in listing.split('\n'):
            if not path or not pat.match(path):
                continue
            text = _git('show', f'{ref}:{path}', ok_fail=True)
            if text is None:
                continue
            slug = _slug(path)
            rec = {'slug': slug, 'title': _title(text, slug), 'drawer': d['name'],
                   'branch': d['branch'], 'path': path, 'kind': d['kind'], 'rank': d['rank'],
                   'lines': text.count('\n') + 1, 'chars': len(text)}
            fn = f"{d['name']}__{slug}.md"
            with open(os.path.join(CACHE, fn), 'w', encoding='utf-8') as fh:
                fh.write(text)
            rec['cache_file'] = fn
            entries.setdefault(slug, []).append(rec)
            n += 1
        if verbose:
            print(f"  [{d['name']:9s}] {d['branch'][:44]:44s} {n:4d}장")
    ctx = []
    for branch, path in CONTEXT_DOCS:
        ref = _ref(branch)
        if ref is None:
            continue
        text = _git('show', f'{ref}:{path}', ok_fail=True)
        if text is None:
            continue
        fn = 'context__' + os.path.basename(path)
        with open(os.path.join(CACHE, fn), 'w', encoding='utf-8') as fh:
            fh.write(text)
        ctx.append({'path': path, 'branch': branch, 'cache_file': fn,
                    'title': _title(text, os.path.basename(path)), 'lines': text.count('\n') + 1})
    # 슬러그별 대표 = rank 최소(정본 우선).  나머지는 also_in 으로 보존 — 어느 서랍에 뭐가 있는지 투명.
    flat = []
    for slug, recs in sorted(entries.items()):
        recs.sort(key=lambda r: r['rank'])
        head = dict(recs[0])
        head['also_in'] = [{'drawer': r['drawer'], 'branch': r['branch'], 'path': r['path'],
                            'lines': r['lines'], 'cache_file': r['cache_file']} for r in recs[1:]]
        flat.append(head)
    idx = {'schema': 'litdb-index-v1', 'repo': REPO, 'n_slugs': len(flat),
           'n_files': sum(1 + len(e['also_in']) for e in flat), 'missing_branches': missing,
           'drawers': [{k: d[k] for k in ('name', 'branch', 'kind', 'note')} for d in DRAWERS],
           'context_docs': ctx, 'entries': flat}
    with open(INDEX, 'w', encoding='utf-8') as fh:
        json.dump(idx, fh, ensure_ascii=False, indent=1)
    if verbose:
        print(f"  [context  ] 큐레이션·포지셔닝 문서 {len(ctx)}건")
        print(f"→ 슬러그 {len(flat)}개 (파일 {idx['n_files']}개) → {INDEX}")
        if missing:
            print(f"  ⚠ 접근 불가 브랜치: {missing} (git fetch 필요할 수 있음)")
    return idx


def load_index():
    if not os.path.exists(INDEX):
        raise SystemExit('인덱스 없음 — 먼저: python3 scripts/litdb_sync.py --sync')
    return json.load(open(INDEX, encoding='utf-8'))


def _body(rec):
    p = os.path.join(CACHE, rec['cache_file'])
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''


def search(query, idx=None, limit=15, snippet_chars=260):
    """토큰 AND 점수 검색 — 제목 가중 5, 본문 1, 슬러그 3.  한국어/영어 혼용 그대로 동작."""
    idx = idx or load_index()
    toks = [t for t in re.split(r'\s+', query.strip().lower()) if t]
    if not toks:
        return []
    out = []
    for rec in idx['entries']:
        body = _body(rec)
        bl, tl, sl = body.lower(), rec['title'].lower(), rec['slug'].lower()
        if not all((t in bl or t in tl or t in sl) for t in toks):
            continue
        score = sum(5 * tl.count(t) + 3 * sl.count(t) + bl.count(t) for t in toks)
        pos = min((bl.find(t) for t in toks if bl.find(t) >= 0), default=0)
        s = max(0, pos - snippet_chars // 3)
        snip = re.sub(r'\s+', ' ', body[s:s + snippet_chars]).strip()
        out.append({**{k: rec[k] for k in ('slug', 'title', 'drawer', 'branch', 'path', 'lines')},
                    'also_in': rec.get('also_in', []), 'score': score, 'snippet': snip})
    out.sort(key=lambda r: -r['score'])
    return out[:limit]


def get_card(slug, drawer=None, idx=None):
    idx = idx or load_index()
    for rec in idx['entries']:
        if rec['slug'] != slug:
            continue
        if drawer and rec['drawer'] != drawer:
            for alt in rec.get('also_in', []):
                if alt['drawer'] == drawer:
                    return {**rec, **alt, 'body': open(os.path.join(CACHE, alt['cache_file']),
                                                       encoding='utf-8').read()}
        return {**rec, 'body': _body(rec)}
    return None


def stats(idx=None):
    idx = idx or load_index()
    by = {}
    for rec in idx['entries']:
        by[rec['drawer']] = by.get(rec['drawer'], 0) + 1
        for a in rec['also_in']:
            by[a['drawer']] = by.get(a['drawer'], 0) + 1
    dup = [r for r in idx['entries'] if r['also_in']]
    print(f"슬러그 {idx['n_slugs']} · 파일 {idx['n_files']}")
    for d in idx['drawers']:
        print(f"  {d['name']:9s} {by.get(d['name'], 0):4d}장  — {d['note']}")
    print(f"\n중복 슬러그(여러 서랍 동시 존재) {len(dup)}건 — 대표는 rank 우선(정본>작업>동결):")
    for r in dup[:10]:
        print(f"  · {r['slug'][:52]:52s} {r['drawer']}({r['lines']}줄)"
              + ''.join(f" + {a['drawer']}({a['lines']})" for a in r['also_in']))
    if len(dup) > 10:
        print(f"  … 외 {len(dup) - 10}건")
    only = {}
    for r in idx['entries']:
        if not r['also_in']:
            only.setdefault(r['drawer'], []).append(r['slug'])
    print("\n한 서랍에만 있는 것 (= 다른 서랍에서 안 보이던 것):")
    for d, ss in sorted(only.items()):
        print(f"  {d:9s} {len(ss):4d}장" + (f"  예: {', '.join(ss[:3])}" if ss else ''))
    print(f"\n맥락 문서 {len(idx['context_docs'])}건: "
          + ', '.join(os.path.basename(c['path']) for c in idx['context_docs']))


def _selftest():
    ok = True
    print('litdb_sync selftest')
    idx = sync(verbose=False)
    o1 = idx['n_slugs'] > 50 and idx['n_files'] >= idx['n_slugs']
    ok &= o1
    print(f'  (1) 스캔: 슬러그 {idx["n_slugs"]} · 파일 {idx["n_files"]}  {"OK" if o1 else "FAIL"}')
    # (2) 흩어진 서랍이 실제로 합쳐졌나 — worknotes 전용 카드가 잡혀야 함
    wn = [e for e in idx['entries'] if e['drawer'] == 'worknotes']
    o2 = len(wn) > 0
    ok &= o2
    print(f'  (2) 작업브랜치 digest 흡수: {len(wn)}장  {"OK" if o2 else "FAIL"}')
    # (3) 이번 오진의 원인이던 이용민 DT 논문이 검색되나
    hits = search('digital twin', idx=idx, limit=50)
    yml = [h for h in hits if 'park2020' in h['slug'] or 'lim2025' in h['slug']
           or 'kim2024_digital' in h['slug'] or 'song2025' in h['slug']]
    o3 = len(yml) >= 3
    ok &= o3
    print(f'  (3) 이용민 DT 계보 검색: {len(yml)}편 '
          f'({", ".join(h["slug"][:28] for h in yml[:4])})  {"OK" if o3 else "FAIL"}')
    # (4) 카드 본문 로드 + 대표 선택 규칙(정본 우선)
    dupes = [e for e in idx['entries'] if e['also_in']]
    o4 = True
    if dupes:
        r = dupes[0]
        o4 = r['rank'] <= min(_d['rank'] for _d in DRAWERS if _d['name']
                              in [a['drawer'] for a in r['also_in']] + [r['drawer']])
    c = get_card(idx['entries'][0]['slug'], idx=idx)
    o4 &= bool(c and c.get('body'))
    ok &= o4
    print(f'  (4) 대표선택(정본 우선) + 본문 로드: {"OK" if o4 else "FAIL"}')
    # (5) 검색 정확도 — AND 조건, 없는 토큰이면 0건
    o5 = len(search('zzzznotarealtoken', idx=idx)) == 0 and len(search('LPSCl', idx=idx)) > 0
    ok &= o5
    print(f'  (5) 검색 AND/공집합 규약: {"OK" if o5 else "FAIL"}')
    print('LITDB-SYNC SELFTEST', 'PASS' if ok else 'FAIL')
    return ok


def main():
    ap = argparse.ArgumentParser(description='litdb 통합 인덱서 (전 브랜치, 체크아웃 불필요)')
    ap.add_argument('--sync', action='store_true', help='전 브랜치 스캔 → 캐시/인덱스 갱신')
    ap.add_argument('--search', default='', help='전문 검색 (토큰 AND)')
    ap.add_argument('--show', default='', help='슬러그로 카드 본문 출력')
    ap.add_argument('--drawer', default='', help='--show 시 특정 서랍 판본 선택')
    ap.add_argument('--limit', type=int, default=15)
    ap.add_argument('--stats', action='store_true')
    ap.add_argument('--json', action='store_true', help='검색 결과를 JSON 으로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.sync:
        print('litdb 전 브랜치 스캔 (체크아웃 없음 — git plumbing):')
        sync()
        return
    if a.stats:
        stats(); return
    if a.search:
        res = search(a.search, limit=a.limit)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1)); return
        print(f'"{a.search}" → {len(res)}건\n')
        for r in res:
            extra = ''.join(f" +{x['drawer']}" for x in r['also_in'])
            print(f"● [{r['drawer']}{extra}] {r['slug']}  ({r['lines']}줄, score {r['score']})")
            print(f"  {r['title'][:110]}")
            print(f"  … {r['snippet'][:200]}\n")
        return
    if a.show:
        c = get_card(a.show, drawer=a.drawer or None)
        if not c:
            print(f'없음: {a.show}  (--search 로 슬러그 확인)'); sys.exit(1)
        print(f"# 서랍 {c['drawer']} · 브랜치 {c['branch']} · {c['path']}\n")
        print(c['body'])
        return
    ap.print_help()


if __name__ == '__main__':
    main()
