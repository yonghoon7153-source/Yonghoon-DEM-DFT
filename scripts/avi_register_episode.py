#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AVI 꾸러미 (또는 편 폴더) → 웹앱 영상 폴더에 등록 (1저자 11-24).

    python3 -I scripts/avi_register_episode.py ep01_mixer.zip                     # 꾸러미
    python3 -I scripts/avi_register_episode.py ep01_mixer.zip --replace           # 이미 있는 편을 바꾼다 (옛 판 = .replaced/ 보관)
    python3 -I scripts/avi_register_episode.py <편 폴더> --id ep01_mixer [--internal] [--video …] [--deny-list …]   # 폴더를 바로
    python3 -I scripts/avi_register_episode.py --delete ep01_mixer                 # 지우기 = 보관 폴더로 옮김 (영구 삭제 아님)

등록 자리 = --folder · 없으면 환경 변수 WEBAPP_VIDEO_FOLDER · 없으면 webapp/videos/ (git 밖 · 웹앱 app.py 와 같은 규칙).
폴더를 주면 avi_package_episode.py 와 같은 함수로 임시 꾸러미를 만들어 **같은 등록 함수** (webapp/video_library.register_bundle) 로 넣는다 —
웹앱 화면의 올리기와도 같은 함수 · 같은 검사 (zip-slip · 심볼릭 링크 · 크기 · SHA256SUMS · INTERNAL 표지 · 공개 안전 검사 ·
공개판 = 판 대조 기록 (지금 판 · 다 잰 통과) 필수 — 기록을 본다 · 영상을 다시 재지 않는다).
--delete <편 id> = 같은 지우기 함수 (webapp/video_library.delete_episode · 웹앱 화면의 "삭제" 단추와 같음) — 영구 삭제가 아니다: 편 폴더를
<폴더>/.deleted/<id>__<UTC 시각>/ 로 옮기고 옆에 기록 (<id>__<UTC 시각>.json · 언제 · 명령 / web) 을 남긴다 · 되돌리기 = 그 폴더를 손으로 옮김.
rc 0 = 등록 · 지움 · 1 = 거부 (사유 · 이미 있음 · 없는 편 포함) · 2 = 사용법.  화면 = 웹앱 /videos/<id>.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'webapp'))
import video_library as V  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description='AVI 꾸러미 zip (또는 편 폴더) 를 웹앱 영상 폴더에 등록한다 '
                                             '(--delete = 등록된 편을 보관 폴더 .deleted/ 로 옮긴다).')
    ap.add_argument('source', nargs='?', help='꾸러미 zip 또는 편 폴더 (--delete 때는 주지 않는다)')
    ap.add_argument('--folder', help='등록 자리 (없으면 WEBAPP_VIDEO_FOLDER · 없으면 webapp/videos/)')
    ap.add_argument('--replace', action='store_true', help='같은 편이 있으면 바꾼다 (옛 판은 .replaced/ 에 보관)')
    ap.add_argument('--delete', metavar='ID', help='등록된 편을 지운다 — 영구 삭제가 아니다 (편 폴더를 .deleted/ 로 옮기고 기록을 남긴다 · '
                                                   '되돌리기 = 그 폴더를 손으로 옮김) · 꾸러미 · 폴더 · 등록 옵션과 같이 쓰지 않는다')
    g = ap.add_argument_group('편 폴더를 바로 등록할 때 (avi_package_episode.py 와 같은 뜻)')
    g.add_argument('--id', dest='ep_id', help='편 id (폴더일 때 꼭)')
    g.add_argument('--internal', action='store_true', help='내부판 (공개 금지)')
    g.add_argument('--video', help='영상 mp4 를 따로 고른다')
    g.add_argument('--title', help='제목')
    g.add_argument('--series', help='시리즈 이름')
    g.add_argument('--number', type=int, help='편 번호')
    g.add_argument('--updated', help='갱신 날짜 YYYY-MM-DD')
    g.add_argument('--deny-list', help='내부 숫자 목록 파일 (리포 · 꾸러미 밖)')
    g.add_argument('--no-probe', action='store_true', help='ffprobe 로 길이를 재지 않는다 — --internal (검토 후보) 만 · 공개판은 거부')
    a = ap.parse_args(argv)
    folder = a.folder or V.default_folder()
    if a.delete is not None:
        mixed = [n for n, v in (('꾸러미 · 편 폴더', a.source), ('--replace', a.replace), ('--id', a.ep_id), ('--internal', a.internal),
                                ('--video', a.video), ('--title', a.title), ('--series', a.series), ('--number', a.number),
                                ('--updated', a.updated), ('--deny-list', a.deny_list), ('--no-probe', a.no_probe))
                 if v is not None and v is not False]
        if mixed:
            print(f'✗ --delete 는 {", ".join(mixed)} 와 같이 쓰지 않는다', file=sys.stderr)
            return 2
        try:
            res = V.delete_episode(folder, a.delete, via='cli')
        except V.BundleError as e:
            print(f'✗ 지우지 않았다 — {e}', file=sys.stderr)
            return 1
        print(f"✓ 지움 {res['id']} — 보관 폴더로 옮김 (영구 삭제 아님 · {'깨진 편' if res['state'] == 'broken' else '등록된 편'})")
        print(f"   옮긴 자리 {res['moved_to']}")
        print(f"   기록 {res['record']}")
        print(f"   되돌리기 = 그 폴더를 {res['restore_to']} 로 손으로 옮긴다 (같은 id 편이 없을 때)")
        return 0
    if a.source is None:
        ap.print_usage(sys.stderr)
        print('✗ 꾸러미 zip · 편 폴더 또는 --delete <편 id> 를 준다', file=sys.stderr)
        return 2
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
