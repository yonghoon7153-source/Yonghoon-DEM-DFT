#!/usr/bin/env python3
"""논문 에이전트 산출물을 **litdb 정본 서랍**에 바로 꽂는 통로 (DFT webapp 즉시 반영).

왜 필요한가 (2026-07-28 실패 사례):
  litdb-curator 는 현재 워크트리의 `litdb/papers/` 에 쓴다. 그런데 **작업 브랜치마다 litdb 가 다르다** —
  이 브랜치(stoic-knuth)의 litdb 는 2026-07-16 **동결 스냅샷**(CLAUDE.md: 추가·수정 금지)이고,
  DFT webapp 의 `/literature` 는 **정본 브랜치**(claude/friendly-meitner-lldvar)의 `litdb/papers/`
  만 읽는다.  그래서 이용민 교수님 DT 논문 5편이 작업 브랜치 `docs/lit_*.md` 에 갇혀
  "먹였는데 webapp 에 없다"가 됐다.  이 스크립트가 그 통로를 자동화한다.

흐름 (커레이터가 이 순서로 쓴다):
  1) `--open`  → 정본 브랜치 워크트리를 만들고 **경로를 stdout 에 출력**
  2) 그 워크트리 안에서 `litdb/papers/<slug>.md` 작성 + `litdb/INDEX.md` 등 갱신
  3) `--close --message "..."` → 정본성 검사 → 커밋 → 푸시(거부 시 rebase 재시도) → 워크트리 정리

정본성 검사(푸시 전 자동): 새 카드가 **DFT webapp 자신의 로더**(webapp/data.py list_papers)로
파싱되는지 확인한다.  제목·`> slug ... type ... digested ...` 메타줄이 빠지면 webapp 목록에
안 뜨므로 여기서 막는다.

CLAUDE.md 규약: litdb 한정 정본 브랜치 커밋/푸시는 **상시 승인**(2026-07-16).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON_BRANCH = 'claude/friendly-meitner-lldvar'
WT_DIR = os.path.join(os.path.dirname(REPO), 'litdb-canon')
TMP_BRANCH = 'tmp-litdb-promote'
STATE = os.path.join(REPO, '.litdb_promote_state.json')       # --open 이 남기는 세션 표식


def _run(args, cwd=REPO, check=True, quiet=False):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        if not quiet:
            sys.stderr.write(f'✗ {" ".join(args[:4])} …\n{r.stderr.strip()[:400]}\n')
        raise SystemExit(1)
    return r


def _wt_exists():
    out = _run(['git', 'worktree', 'list', '--porcelain']).stdout
    return any(ln.split(' ', 1)[1].rstrip() == WT_DIR
               for ln in out.split('\n') if ln.startswith('worktree '))


def cmd_open(force=False):
    if _wt_exists():
        if not force:
            print(WT_DIR)
            print('  (이미 열려 있음 — 그대로 사용.  강제 재생성은 --open --force)', file=sys.stderr)
            return WT_DIR
        cmd_cleanup(quiet=True)
    print('litdb 정본 fetch …', file=sys.stderr)
    _run(['git', 'fetch', 'origin', CANON_BRANCH])
    if os.path.exists(WT_DIR):
        shutil.rmtree(WT_DIR, ignore_errors=True)
    _run(['git', 'branch', '-D', TMP_BRANCH], check=False, quiet=True)
    _run(['git', 'worktree', 'add', WT_DIR, f'origin/{CANON_BRANCH}', '-b', TMP_BRANCH])
    before = _papers_set(WT_DIR)
    json.dump({'worktree': WT_DIR, 'branch': TMP_BRANCH, 'papers_before': sorted(before)},
              open(STATE, 'w'))
    print(f'  워크트리 준비됨 (정본 논문 {len(before)}편)', file=sys.stderr)
    print(f'  → 여기에 litdb/papers/<slug>.md 를 쓰고 litdb/INDEX.md 를 갱신하세요', file=sys.stderr)
    print(WT_DIR)
    return WT_DIR


def _papers_set(wt):
    pd = os.path.join(wt, 'litdb', 'papers')
    if not os.path.isdir(pd):
        return set()
    return {f[:-3] for f in os.listdir(pd) if f.endswith('.md') and not f.startswith('_')}


def _webapp_papers(wt):
    """DFT webapp 자신의 로더로 파싱 — 목록에 뜨는지 여기서 확인."""
    code = ('import sys, json; sys.path.insert(0, "webapp"); import data as D; '
            'print(json.dumps(D.list_papers()))')
    r = subprocess.run([sys.executable, '-c', code], cwd=wt, capture_output=True, text=True)
    if r.returncode != 0:
        return None, r.stderr.strip()[:300]
    try:
        return json.loads(r.stdout.strip().split('\n')[-1]), None
    except Exception as e:
        return None, f'{type(e).__name__}: {e}'


def cmd_check(wt=None, verbose=True):
    """정본성 검사 — 새 카드가 webapp 목록에 뜨는가 + 메타줄이 온전한가."""
    wt = wt or WT_DIR
    if not os.path.isdir(wt):
        raise SystemExit('워크트리 없음 — 먼저 --open')
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    before = set(st.get('papers_before', []))
    now = _papers_set(wt)
    added, removed = sorted(now - before), sorted(before - now)
    papers, err = _webapp_papers(wt)
    problems = []
    if papers is None:
        problems.append(f'webapp 로더 실행 실패: {err}')
    else:
        by = {p['id']: p for p in papers}
        for slug in added:
            p = by.get(slug)
            if p is None:
                problems.append(f'{slug}: webapp 목록에 안 뜸 (파일명/위치 확인)')
                continue
            if not p.get('type'):
                problems.append(f'{slug}: `type` 파싱 실패 — 제목 다음 18줄 안에 '
                                '"> slug `x` · type `Y` · digested `YYYY-MM-DD`" 메타줄 필요')
            if not p.get('digested'):
                problems.append(f'{slug}: `digested` 날짜 파싱 실패 (같은 메타줄)')
            if p.get('title', '').replace(' ', '') == slug.replace('_', ''):
                problems.append(f'{slug}: 제목(# 줄) 없음 — 파일명이 제목으로 대체됨')
    if removed:
        problems.append(f'삭제된 카드 있음: {removed} (정본에서 지우는 건 의도 확인 필요)')
    if verbose:
        print(f'추가 {len(added)}편: {", ".join(added) or "—"}')
        if papers is not None:
            print(f'webapp 인식 총 {len(papers)}편')
            for slug in added:
                p = {q["id"]: q for q in papers}.get(slug)
                if p:
                    print(f'  ✓ [{p["track"]}] {slug}  type={p["type"][:28]!r} digested={p["digested"]}')
        for pb in problems:
            print(f'  ✗ {pb}')
        print('정본성 검사:', 'PASS' if not problems else f'FAIL ({len(problems)}건)')
    return added, problems


def cmd_close(message='', dry_run=False, allow_empty_index=False):
    wt = WT_DIR
    if not os.path.isdir(wt):
        raise SystemExit('워크트리 없음 — 먼저 --open')
    dirty = _run(['git', 'status', '--porcelain'], cwd=wt).stdout.strip()
    if not dirty:
        print('변경 없음 — 정리만 하고 종료'); cmd_cleanup(); return
    added, problems = cmd_check(wt)
    if problems:
        raise SystemExit('✗ 정본성 검사 실패 — 위 문제를 고친 뒤 다시 --close '
                         '(워크트리는 그대로 두었습니다)')
    if added and not allow_empty_index:
        idx = os.path.join(wt, 'litdb', 'INDEX.md')
        txt = open(idx, encoding='utf-8').read() if os.path.exists(idx) else ''
        miss = [s for s in added if s not in txt]
        if miss:
            raise SystemExit(f'✗ INDEX.md 에 등재 안 된 카드: {miss}\n'
                             '  정본 규약상 INDEX 행이 있어야 찾을 수 있습니다. '
                             '추가 후 다시 --close (검사 생략은 --allow-empty-index)')
    msg = message or (f'litdb: add {len(added)} paper card(s) — ' + ', '.join(added[:3])
                      + ('…' if len(added) > 3 else ''))
    if dry_run:
        print(f'[dry-run] 커밋 예정 메시지: {msg}')
        print('[dry-run] 변경:'); print(dirty[:1200]); return
    _run(['git', 'add', '-A'], cwd=wt)
    _run(['git', 'commit', '-q', '-m', msg], cwd=wt)
    ref = f'HEAD:refs/heads/{CANON_BRANCH}'
    r = _run(['git', 'push', 'origin', ref], cwd=wt, check=False, quiet=True)
    if r.returncode != 0:                                      # 다른 세션이 앞서감 → rebase 재시도
        print('  원격이 앞서 있음 → fetch+rebase 후 재푸시', file=sys.stderr)
        _run(['git', 'fetch', 'origin', CANON_BRANCH], cwd=wt)
        _run(['git', 'rebase', f'origin/{CANON_BRANCH}'], cwd=wt)
        _, problems2 = cmd_check(wt, verbose=False)            # rebase 후 재검증
        if problems2:
            raise SystemExit(f'✗ rebase 후 정본성 깨짐: {problems2}')
        _run(['git', 'push', 'origin', ref], cwd=wt)
    print(f'✓ 정본 푸시 완료 → {CANON_BRANCH}  ({len(added)}편)')
    print('  DFT webapp /literature 새로고침하면 보입니다.')
    cmd_cleanup()


def cmd_cleanup(quiet=False):
    if _wt_exists():
        _run(['git', 'worktree', 'remove', WT_DIR, '--force'], check=False, quiet=True)
    if os.path.exists(WT_DIR):
        shutil.rmtree(WT_DIR, ignore_errors=True)
    _run(['git', 'worktree', 'prune'], check=False, quiet=True)
    _run(['git', 'branch', '-D', TMP_BRANCH], check=False, quiet=True)
    if os.path.exists(STATE):
        os.remove(STATE)
    if not quiet:
        print('워크트리 정리 완료')


def _selftest():
    ok = True
    print('litdb_promote selftest')
    wt = cmd_open(force=True)
    o1 = os.path.isdir(os.path.join(wt, 'litdb', 'papers'))
    ok &= o1
    print(f'  (1) 정본 워크트리 열기: {"OK" if o1 else "FAIL"}')
    papers, err = _webapp_papers(wt)
    o2 = papers is not None and len(papers) > 100
    ok &= o2
    print(f'  (2) DFT webapp 로더 동작: {len(papers) if papers else err} → {"OK" if o2 else "FAIL"}')
    # (3) 메타줄 없는 카드는 검사에서 걸려야 한다
    bad = os.path.join(wt, 'litdb', 'papers', 'zz_selftest_bad.md')
    open(bad, 'w', encoding='utf-8').write('본문만 있고 제목도 메타줄도 없음\n')
    added, problems = cmd_check(wt, verbose=False)
    o3 = 'zz_selftest_bad' in added and len(problems) > 0
    ok &= o3
    print(f'  (3) 불완전 카드 거부: 추가감지={("zz_selftest_bad" in added)} 문제={len(problems)}건 '
          f'→ {"OK" if o3 else "FAIL"}')
    # (4) 온전한 카드는 통과해야 한다
    os.remove(bad)
    good = os.path.join(wt, 'litdb', 'papers', 'zz_selftest_good.md')
    open(good, 'w', encoding='utf-8').write(
        '# Selftest Paper — 정본성 검사용\n\n'
        '> slug `zz_selftest_good` · DOI `10.0000/selftest` · type `DEM` · digested `2026-07-28` · status ✅\n\n'
        '## 1. 한 줄 요약\n검사용 임시 카드.\n')
    added, problems = cmd_check(wt, verbose=False)
    o4 = 'zz_selftest_good' in added and not problems
    ok &= o4
    print(f'  (4) 온전한 카드 통과: 문제 {len(problems)}건 → {"OK" if o4 else "FAIL"}')
    # (5) INDEX 미등재는 --close 가 막아야 한다
    try:
        cmd_close(message='selftest', dry_run=False)
        o5 = False
    except SystemExit as e:
        o5 = 'INDEX' in str(e)
    ok &= o5
    print(f'  (5) INDEX 미등재 차단: {"OK" if o5 else "FAIL"}')
    cmd_cleanup(quiet=True)
    print('LITDB-PROMOTE SELFTEST', 'PASS' if ok else 'FAIL')
    return ok


def main():
    ap = argparse.ArgumentParser(
        description='논문 에이전트 산출물 → litdb 정본 서랍 (DFT webapp 즉시 반영)')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--open', action='store_true', help='정본 브랜치 워크트리 열고 경로 출력')
    g.add_argument('--check', action='store_true', help='정본성 검사만 (푸시 안 함)')
    g.add_argument('--close', action='store_true', help='검사 → 커밋 → 푸시 → 정리')
    g.add_argument('--cleanup', action='store_true', help='워크트리만 정리 (버릴 때)')
    g.add_argument('--selftest', action='store_true')
    ap.add_argument('--message', default='', help='--close 커밋 메시지')
    ap.add_argument('--dry-run', action='store_true', help='--close 를 시늉만')
    ap.add_argument('--force', action='store_true', help='--open 시 기존 워크트리 재생성')
    ap.add_argument('--allow-empty-index', action='store_true',
                    help='--close 시 INDEX 등재 검사 생략 (권장 안 함)')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.open:
        cmd_open(force=a.force)
    elif a.check:
        _, pb = cmd_check()
        sys.exit(1 if pb else 0)
    elif a.close:
        cmd_close(message=a.message, dry_run=a.dry_run, allow_empty_index=a.allow_empty_index)
    elif a.cleanup:
        cmd_cleanup()
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
