#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AVI 편 폴더 → 꾸러미 (bundle.zip) — 웹앱 영상 섹션 (/videos) 에 넣을 것 (1저자 11-24).

    python3 -I scripts/avi_package_episode.py <편 폴더> --id ep01_mixer -o ep01_mixer.zip
    python3 -I scripts/avi_package_episode.py <내부판 폴더> --id ep01internal_mixer_b2 --internal -o int.zip
    python3 -I scripts/avi_package_episode.py docs/avi/ep01_mixer --video <리포 밖 mp4> --deny-list <리포 밖 내부 숫자 목록> --id ep01_mixer -o ep01.zip

꾸러미 = 납작한 zip (episode.json + SHA256SUMS + 역할 파일).  넣는 것 = 편 폴더 맨 위 일반 파일 중 역할 있는 것
(mp4 · thumbnail.png · *.srt · script.md · scenes.json · timeline.json · qc.md / qc_*.md · qc_report*.json · rubric*.md · README*.md) ·
하위 폴더 (internal/ · qa/ · v1/ …) · 심볼릭 링크 · 그 밖 파일은 넣지 않는다.
공개판 (기본) = INTERNAL 표지 이름 · internal 폴더 · id 거부 · qc_report 의 internal 칸을 뺀 사본 · 공개 안전 검사 (IP · 포트 · 홈 경로 ·
내부판 파일 이름 · 잡 번호 · 철회값 · --deny-list) 통과 필수.  내부판 (--internal) = 검사는 기록만 · 화면에 빨간 배지.
등록 = scripts/avi_register_episode.py (같은 라이브러리 webapp/video_library.py) · 규칙 = .claude/skills/avi-generate/SKILL.md "웹앱 영상 섹션".
rc 0 = 만듦 · 1 = 거부 (사유) · 2 = 사용법.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'webapp'))
import video_library as V  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser(description='AVI 편 폴더를 웹앱 영상 섹션 꾸러미 (zip) 로 만든다.')
    ap.add_argument('ep_dir', help='편 폴더 (맨 위 파일만 넣는다)')
    ap.add_argument('--id', required=True, dest='ep_id', help='편 id — 소문자 · 숫자 · 밑줄 2-64 자 (예 ep01_mixer)')
    ap.add_argument('-o', '--out', required=True, help='만들 꾸러미 zip 경로')
    ap.add_argument('--internal', action='store_true', help='내부판 (공개 금지) — INTERNAL 표지 이름이 있으면 꼭 붙인다')
    ap.add_argument('--video', help='영상 mp4 를 따로 고른다 (리포 밖 렌더 · 폴더에 mp4 가 둘 이상일 때)')
    ap.add_argument('--title', help='제목 (없으면 scenes.json 의 title)')
    ap.add_argument('--series', help='시리즈 이름 (없으면 scenes.json 의 series)')
    ap.add_argument('--number', type=int, help='편 번호 (없으면 id 의 ep 뒤 숫자)')
    ap.add_argument('--updated', help='갱신 날짜 YYYY-MM-DD (없으면 오늘 · 한국 시간)')
    ap.add_argument('--deny-list', help='내부 숫자 목록 파일 (리포 · 꾸러미 밖) — 한 줄에 하나 · 공개판 글에 있으면 거부 (값은 적지 않는다)')
    ap.add_argument('--no-probe', action='store_true', help='ffprobe 로 길이를 재지 않는다 (timeline.json 의 길이를 쓴다)')
    a = ap.parse_args(argv)
    try:
        man = V.package_episode(a.ep_dir, a.ep_id, a.out, internal=a.internal, video=a.video, title=a.title, series=a.series,
                                number=a.number, updated=a.updated, deny_list=a.deny_list, probe=not a.no_probe)
    except V.BundleError as e:
        print(f'✗ 꾸러미를 만들지 않았다 — {e}', file=sys.stderr)
        return 1
    vis = '내부판 (공개 금지)' if man['visibility'] == 'internal' else '공개판'
    pc = man['public_check']
    print(f"✓ 꾸러미 {Path(a.out).name} — {man['id']} · {vis} · 길이 {V.fmt_clock(man.get('duration_s'))} "
          f"({man.get('duration_source') or '모름'}) · 갱신 {man['updated']}")
    for f in man['files']:
        print(f"   {f['role']:<10} {f['name']}  {V.fmt_size(f['size'])}  sha256 {f['sha256'][:16]}…")
    for d in man.get('derived') or []:
        print(f"   (사본) {d['name']} ← {d['from']} · 뺀 칸 {', '.join(d.get('dropped_keys') or [])}")
    skipped = man.get('_skipped') or []
    if skipped:
        print(f"   넣지 않음 {len(skipped)} 개: " + ' · '.join(f'{n} ({w})' for n, w in skipped[:12])
              + (f' · 그 밖 {len(skipped) - 12} 개' if len(skipped) > 12 else ''))
    dl = pc.get('deny_list')
    print(f"   공개 안전 검사: {'통과' if pc['ok'] else '걸림 ' + str(len(pc['hits'])) + ' 건 (내부판 · 기록만)'} · 규칙 {len(pc['rules'])} 종 · "
          f"글 파일 {pc['files']} 개 · 내부 숫자 목록 {str(dl['n']) + ' 개' if dl else '없이'}")
    print(f"   다음: python3 -I scripts/avi_register_episode.py {a.out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
