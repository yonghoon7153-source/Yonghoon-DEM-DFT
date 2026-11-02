#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 방법 그림 (2D) 웹앱 사본 — docs 원본 폴더를 웹앱 정적 폴더로 그대로 복사하고 대조한다.

    python3 scripts/sync_dem_method_figs_to_webapp.py            # 사본을 원본과 같게 (복사 · 원본에 없는 사본은 지움)
    python3 scripts/sync_dem_method_figs_to_webapp.py --check    # 바꾸지 않고 대조만 (같으면 0 · 다르면 1)

원본 = `docs/50kg/report_y4/figs/p0_dem_method/` (생성기 `docs/50kg/report_y4/figs/make_fig_p0_dem_method.py`).
사본 = `webapp/static/dem_method_figs/files/` — 페이지 `webapp/static/dem_method_figs/index.html` 이 이 사본을 링크한다
(1저자 11-01 *"2d로 지금 그림 넣은것들 webapp에 넣고 뽑을거야"*).  `webapp/app.py` 는 봉인 32
(`scripts/run_network_194_parallel.py` CODE_FILES) 라 라우트를 만들지 않고 Flask 기본 정적 폴더를 쓴다.

그림을 다시 만들면 (생성기) 이 스크립트를 인자 없이 돌려 사본을 맞추고 `--check` 로 확인한다 —
`scripts/check_all.sh` 가 `--check` 를 돈다.  시험 = `webapp/test_dem_method_figs_page.py`.

대조 규칙 (하나라도 어기면 문제):
  · 원본 폴더가 있고 파일이 하나 이상이다 (빈 원본 = 통과가 아니다)
  · 두 폴더의 항목은 일반 파일뿐이다 (하위 폴더 · 심볼릭 링크 = 문제 — 사본은 원본 바이트의 복사본이어야 한다)
  · 파일 이름 집합이 같다 (사본에 빠진 것 · 원본에 없는 것 = 문제)
  · 같은 이름끼리 바이트가 같다 (sha256 을 함께 적는다)
"""
import argparse
import hashlib
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_REL = os.path.join('docs', '50kg', 'report_y4', 'figs', 'p0_dem_method')
DST_REL = os.path.join('webapp', 'static', 'dem_method_figs', 'files')


def _sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 16), b''):
            h.update(blk)
    return h.hexdigest()


def _entries(d):
    """→ (일반 파일 이름 정렬 목록, 문제 목록).  하위 폴더 · 심볼릭 링크 · 그 밖의 항목은 문제로 센다."""
    files, probs = [], []
    for n in sorted(os.listdir(d)):
        p = os.path.join(d, n)
        if os.path.islink(p):
            probs.append(f'심볼릭 링크 — {p} (사본은 일반 파일이어야 한다)')
        elif os.path.isdir(p):
            probs.append(f'하위 폴더 — {p} (이 도구는 한 층만 다룬다)')
        elif os.path.isfile(p):
            files.append(n)
        else:
            probs.append(f'일반 파일이 아님 — {p}')
    return files, probs


def compare(src, dst):
    """→ 문제 목록 (빈 목록 = 사본이 원본과 같다).  아무것도 바꾸지 않는다."""
    if not os.path.isdir(src):
        return [f'원본 폴더가 없다 — {src}']
    s_files, probs = _entries(src)
    if not s_files:
        probs.append(f'원본 폴더에 파일이 없다 — {src} (빈 원본을 같다고 하지 않는다)')
    if not os.path.isdir(dst):
        return probs + [f'사본 폴더가 없다 — {dst}']
    d_files, dprobs = _entries(dst)
    probs += dprobs
    for n in s_files:
        if n not in d_files:
            probs.append(f'사본에 없다 — {n}')
    for n in d_files:
        if n not in s_files:
            probs.append(f'원본에 없는 사본 — {n}')
    for n in s_files:
        if n in d_files:
            a, b = os.path.join(src, n), os.path.join(dst, n)
            ha, hb = _sha(a), _sha(b)
            if ha != hb:
                probs.append(f'바이트가 다르다 — {n} (원본 sha256 {ha[:16]}… · 사본 {hb[:16]}…)')
    return probs


def sync(src, dst):
    """사본 폴더를 원본과 같게 만든다 (복사 · 원본에 없는 일반 파일은 지움) → 끝난 뒤 compare() 결과.

    원본이 비었거나 없으면 아무것도 지우지 않고 문제를 돌려준다 (빈 원본으로 사본을 비우지 않는다).
    """
    if not os.path.isdir(src):
        return [f'원본 폴더가 없다 — {src}']
    s_files, sprobs = _entries(src)
    if sprobs or not s_files:
        return sprobs or [f'원본 폴더에 파일이 없다 — {src}']
    os.makedirs(dst, exist_ok=True)
    d_files, dprobs = _entries(dst)
    if dprobs:
        return dprobs
    for n in d_files:
        if n not in s_files:
            os.remove(os.path.join(dst, n))
    for n in s_files:
        shutil.copyfile(os.path.join(src, n), os.path.join(dst, n))
    return compare(src, dst)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true',
                    help='바꾸지 않고 대조만 한다 (같으면 종료코드 0 · 다르면 1)')
    ap.add_argument('--src', default=os.path.join(ROOT, SRC_REL),
                    help='원본 폴더 (기본 = docs/50kg/report_y4/figs/p0_dem_method)')
    ap.add_argument('--dst', default=os.path.join(ROOT, DST_REL),
                    help='사본 폴더 (기본 = webapp/static/dem_method_figs/files)')
    a = ap.parse_args(argv)
    probs = compare(a.src, a.dst) if a.check else sync(a.src, a.dst)
    n = len(_entries(a.src)[0]) if os.path.isdir(a.src) else 0
    if probs:
        print(f'✗ 사본이 원본과 다르다 ({len(probs)} 건) — 원본 {a.src} · 사본 {a.dst}')
        for p in probs:
            print('   ' + p)
        if a.check:
            print('   → 고치려면: python3 scripts/sync_dem_method_figs_to_webapp.py  (인자 없이)')
        return 1
    print(f'✓ 사본 = 원본 (파일 {n} 개 · 바이트 같음) — {"대조만" if a.check else "복사 뒤 대조"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
