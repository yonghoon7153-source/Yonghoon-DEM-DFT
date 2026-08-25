#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""webapp 데이터(uploads·results·archive·mpm_lab) 복구 — Supabase 버킷 ↔ 로컬.

★ 왜 필요했나 (2026-08-25): 윈도우 재설치로 WSL 이 통째로 날아갔다.  코드는 git 에 있어
  `clone` 한 번에 돌아왔지만 **webapp 데이터는 git 에 없다** — 케이스 0건으로 떴다.
  `webapp/storage_sync.py` 에 `sync_remote_to_dir` 이 이미 있었는데 **부르는 자리가 없었다**
  (업로드 방향만 웹앱이 자동으로 쓴다).  ⇒ 그 함수를 쓰는 복구 진입점을 만든다.

⚠ 자격증명은 **환경변수**로만 받는다 (파일에 적지 않는다):
    SUPABASE_URL · SUPABASE_KEY · SUPABASE_BUCKET(기본 dem-data)

  python3 scripts/restore_webapp_data.py --check        # 버킷에 무엇이 있나 (읽기만)
  python3 scripts/restore_webapp_data.py --restore      # 전부 내려받기
  python3 scripts/restore_webapp_data.py --restore --only results
  python3 scripts/restore_webapp_data.py --selftest

⚠ **덮어쓰기 주의**: `--restore` 는 원격 파일을 로컬 같은 경로에 쓴다.  로컬에 이미 케이스가
  있으면 `--check` 로 먼저 세어 볼 것 (기본은 **비어 있을 때만** 진행하고, 채워져 있으면
  `--force` 를 요구한다 — 복구가 멀쩡한 데이터를 덮는 사고를 막는다).
"""
from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _p in (os.path.join(_ROOT, 'webapp'),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

#: 웹앱이 쓰는 네 폴더 — 원격 prefix 는 `storage_sync` 가 업로드할 때 쓰는 것과 같아야 한다.
FOLDERS = ('results', 'uploads', 'archive', 'mpm_lab')


def _data_root():
    return os.environ.get('DEM_WEB_DATA') or os.path.join(os.path.expanduser('~'),
                                                          'Yonghoon-DEM-DFT')


def _load():
    try:
        import storage_sync as S
    except Exception as e:                                         # noqa: BLE001
        raise SystemExit(f'storage_sync 를 못 읽는다 ({type(e).__name__}: {e}) — '
                         f'리포 루트에서 실행할 것')
    if not S.SUPABASE_URL or not S.SUPABASE_KEY:
        raise SystemExit(
            '⛔ SUPABASE_URL / SUPABASE_KEY 가 없다.\n'
            '   이 값들은 옛 머신의 셸 환경에 있었고 **git 에는 없다** (자격증명이라 당연하다).\n'
            '   Supabase 대시보드 → Project Settings → API 에서 다시 받아:\n'
            "     export SUPABASE_URL='https://<project>.supabase.co'\n"
            "     export SUPABASE_KEY='<service_role 또는 anon key>'\n"
            '   ⚠ ~/.bashrc 에 넣되 **리포에는 커밋하지 말 것**.')
    S.init()
    return S


def check():
    S = _load()
    print(f'버킷 {S.SUPABASE_BUCKET} @ {S.SUPABASE_URL}')
    root = _data_root()
    total = 0
    for f in FOLDERS:
        try:
            remote = S.list_files(f, limit=1000)
        except Exception as e:                                     # noqa: BLE001
            print(f'  {f:9} 원격 조회 실패 ({type(e).__name__}: {e})')
            continue
        n_rem = len(remote or [])
        loc = os.path.join(root, 'webapp', f)
        n_loc = len([d for d in os.listdir(loc)]) if os.path.isdir(loc) else 0
        total += n_rem
        flag = '  ← 복구 대상' if n_rem and not n_loc else ''
        print(f'  {f:9} 원격 {n_rem:>5} 파일 · 로컬 {n_loc:>5} 항목{flag}')
    print(f'\n원격 합계 {total} 파일 · 로컬 루트 {root}')
    if total == 0:
        print('⚠ 원격이 비어 있다 — 이 버킷에는 백업이 없다.  아래 §다른 경로 를 볼 것:\n'
              '  ① 옛 WSL 디스크 이미지 `ext4.vhdx` (Windows.old 나 백업 드라이브)\n'
              '     → 그게 살아 있으면 **전체 복구**가 되므로 가장 먼저 확인할 것\n'
              '  ② GPU 호스트(kgy 등)에 남은 런 출력 — webapp 케이스가 아니라 원자료다\n'
              '  ③ 복구 불가면: 케이스는 다시 돌려야 한다 (코드·규약·원장은 전부 git 에 있다)')
    return 0


def restore(only=None, force=False):
    S = _load()
    root = _data_root()
    targets = [only] if only else list(FOLDERS)
    for f in targets:
        if f not in FOLDERS:
            raise SystemExit(f'알 수 없는 폴더 {f} — 가능: {list(FOLDERS)}')
        loc = os.path.join(root, 'webapp', f)
        n_loc = len(os.listdir(loc)) if os.path.isdir(loc) else 0
        if n_loc and not force:
            print(f'  {f:9} 건너뜀 — 로컬에 이미 {n_loc}개 있다.  덮으려면 --force '
                  f'(복구가 멀쩡한 데이터를 덮는 사고를 막는다)')
            continue
        os.makedirs(loc, exist_ok=True)
        print(f'  {f:9} 내려받는 중 → {loc}')
        S.sync_remote_to_dir(f, loc)
        print(f'  {f:9} 완료 — 로컬 {len(os.listdir(loc))}개 항목')
    print('\n끝.  `dem5002` 로 다시 띄워 케이스 수를 확인할 것.')
    return 0


def _selftest():
    n = [0, 0]

    def chk(m, ok):
        n[1] += 1
        n[0] += bool(ok)
        print(f'  {"PASS" if ok else "FAIL"}  {m}')

    chk('① 네 폴더가 웹앱 설정과 같다',
        set(FOLDERS) == {'results', 'uploads', 'archive', 'mpm_lab'})
    #  자격증명이 없을 때 **조용히 아무것도 안 하지 않고** 안내하며 멈춘다
    old = (os.environ.pop('SUPABASE_URL', None), os.environ.pop('SUPABASE_KEY', None))
    try:
        import importlib
        import storage_sync as S
        importlib.reload(S)
        try:
            _load()
            ok = False
        except SystemExit as e:
            ok = 'SUPABASE_URL' in str(e) and '대시보드' in str(e)
        chk('② ★ 자격증명이 없으면 **어디서 받는지 알려주며** 멈춘다 (조용한 no-op 금지)', ok)
    finally:
        for k, v in zip(('SUPABASE_URL', 'SUPABASE_KEY'), old):
            if v is not None:
                os.environ[k] = v
    chk('③ 데이터 루트가 DEM_WEB_DATA 를 따른다',
        _data_root().endswith('Yonghoon-DEM-DFT') or bool(os.environ.get('DEM_WEB_DATA')))
    print(f'\nrestore_webapp_data selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--check', action='store_true', help='버킷에 무엇이 있나 (읽기만)')
    ap.add_argument('--restore', action='store_true')
    ap.add_argument('--only', default='', help=f'한 폴더만 {FOLDERS}')
    ap.add_argument('--force', action='store_true', help='로컬이 비어 있지 않아도 덮어쓴다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.check:
        raise SystemExit(check())
    if a.restore:
        raise SystemExit(restore(a.only or None, a.force))
    ap.print_help()
