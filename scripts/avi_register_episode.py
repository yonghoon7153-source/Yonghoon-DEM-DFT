#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AVI 꾸러미 (또는 편 폴더) → 웹앱 영상 폴더에 등록 (1저자 11-24).

    python3 -I scripts/avi_register_episode.py ep01_mixer.zip                     # 꾸러미
    python3 -I scripts/avi_register_episode.py ep01_mixer.zip --replace           # 이미 있는 편을 바꾼다 (옛 판 = .replaced/ 보관)
    python3 -I scripts/avi_register_episode.py <편 폴더> --id ep01_mixer [--internal] [--video …] [--deny-list …]   # 폴더를 바로

등록 자리 = --folder · 없으면 환경 변수 WEBAPP_VIDEO_FOLDER · 없으면 webapp/videos/ (git 밖 · 웹앱 app.py 와 같은 규칙).
폴더를 주면 avi_package_episode.py 와 같은 함수로 임시 꾸러미를 만들어 **같은 등록 함수** (webapp/video_library.register_bundle) 로 넣는다 —
웹앱 화면의 올리기와도 같은 함수 · 같은 검사 (zip-slip · 심볼릭 링크 · 크기 · SHA256SUMS · INTERNAL 표지 · 공개 안전 검사).
rc 0 = 등록 · 1 = 거부 (사유 · 이미 있음 포함) · 2 = 사용법.  화면 = 웹앱 /videos/<id>.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'webapp'))
import video_library as V  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description='AVI 꾸러미 zip (또는 편 폴더) 를 웹앱 영상 폴더에 등록한다.')
    ap.add_argument('source', help='꾸러미 zip 또는 편 폴더')
    ap.add_argument('--folder', help='등록 자리 (없으면 WEBAPP_VIDEO_FOLDER · 없으면 webapp/videos/)')
    ap.add_argument('--replace', action='store_true', help='같은 편이 있으면 바꾼다 (옛 판은 .replaced/ 에 보관)')
    g = ap.add_argument_group('편 폴더를 바로 등록할 때 (avi_package_episode.py 와 같은 뜻)')
    g.add_argument('--id', dest='ep_id', help='편 id (폴더일 때 꼭)')
    g.add_argument('--internal', action='store_true', help='내부판 (공개 금지)')
    g.add_argument('--video', help='영상 mp4 를 따로 고른다')
    g.add_argument('--title', help='제목')
    g.add_argument('--series', help='시리즈 이름')
    g.add_argument('--number', type=int, help='편 번호')
    g.add_argument('--updated', help='갱신 날짜 YYYY-MM-DD')
    g.add_argument('--deny-list', help='내부 숫자 목록 파일 (리포 · 꾸러미 밖)')
    g.add_argument('--no-probe', action='store_true', help='ffprobe 로 길이를 재지 않는다')
    a = ap.parse_args(argv)
    folder = a.folder or V.default_folder()
    src = Path(a.source)
    try:
        if src.is_dir():
            if not a.ep_id:
                print('✗ 편 폴더를 등록하려면 --id 가 필요하다', file=sys.stderr)
                return 2
            res = V.register_dir(src, folder, ep_id=a.ep_id, replace=a.replace, via='cli', internal=a.internal, video=a.video,
                                 title=a.title, series=a.series, number=a.number, updated=a.updated, deny_list=a.deny_list,
                                 probe=not a.no_probe)
        else:
            res = V.register_bundle(src, folder, replace=a.replace, via='cli')
    except V.BundleError as e:
        print(f'✗ 등록하지 않았다 — {e}', file=sys.stderr)
        return 1
    man = res['manifest']
    vis = '내부판 (공개 금지)' if man['visibility'] == 'internal' else '공개판'
    print(f"✓ 등록 {res['id']} — {vis} · 파일 {len(man['files'])} 개 · 꾸러미 sha256 {res['bundle_sha256'][:16]}…")
    print(f"   자리 {res['path']}")
    if res.get('replaced_to'):
        print(f"   옛 판 보관 {res['replaced_to']}")
    print(f"   화면 /videos/{res['id']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
