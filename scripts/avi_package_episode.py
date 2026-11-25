#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AVI 편 폴더 → 꾸러미 (bundle.zip) — 웹앱 영상 섹션 (/videos) 에 넣을 것 (1저자 11-24).

    python3 -I scripts/avi_package_episode.py <편 폴더> --id ep01_mixer -o ep01_mixer.zip
    python3 -I scripts/avi_package_episode.py <내부판 폴더> --id ep01internal_mixer_b2 --internal -o int.zip
    python3 -I scripts/avi_package_episode.py docs/avi/ep01_mixer --video <리포 밖 mp4> --deny-list <리포 밖 내부 숫자 목록> --id ep01_mixer -o ep01.zip

꾸러미 = 납작한 zip (episode.json + SHA256SUMS + 역할 파일).  넣는 것 = 편 폴더 맨 위 일반 파일 중 역할 있는 것
(mp4 · thumbnail.png · *.srt · script.md · scenes.json · timeline.json · qc.md / qc_*.md · qc_report*.json · rubric*.md · README*.md) ·
하위 폴더 (internal/ · qa/ · v1/ …) · 심볼릭 링크 · 그 밖 파일은 넣지 않는다.
공개판 (기본 · Codex 11-25 AVI-02 · 1저자 11-25 Q1 · Q2 (가)) = INTERNAL 표지 이름 · internal 폴더 · id 거부 · 넣는 역할 = 영상 · 썸네일 ·
자막 · 시청자 대본 (scenes.json 에서 만든다 — 장면 제목 · 문장 글 + 제작 script.md 의 참고 문헌 목록 줄 · 제작 대본 자체는 안 넣음) ·
공개 장면 (scenes.json 공개 투영) · timeline.json 만 · 제작 기록 (qc · qc_report · rubric · README) = 뺌 (episode.json excluded · derived) ·
공개 안전 검사 (IP · 포트 · 홈 경로 · 내부판 파일 이름 · 잡 번호 · 제작 표지 · 철회값 · git 커밋 식별자 · --deny-list = 수 경계) 통과 필수.
내부판 (--internal) = 모든 역할 · 파일 그대로 · 검사는 기록만 · 화면에 빨간 배지.
판 대조 (둘 다 · Q4 P2-6 · 3 회차 P2-1 · P2-2) = MP4 길이 (ffprobe) ↔ timeline.json 끝 · 자막 수 ↔ 시간표 자막 수 · 자막 마지막 줄 ↔
시간표 마지막 자막 · 자막 마지막 줄 ≤ MP4 길이 (허용 0.5 s) · 장면 파일 문장 (id · 글) ↔ 시간표 문장 — 어긋나면 rc 1 (같은 빌드의 영상 ·
시간표 · 자막 · 장면 파일로 꾸린다).  공개판 = 다섯을 다 재야 (ffprobe 없음 · --no-probe · 시간표 · 자막 · 장면 파일 없음 = rc 1) ·
내부판 (검토 후보) = 못 잰 대조를 episode.json build_check 의 미측정으로 적는다.
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
    ap.add_argument('--no-probe', action='store_true',
                    help='ffprobe 로 길이를 재지 않는다 — 검토 후보 (--internal) 만 (MP4 대조 = 미측정 · 길이 표시 = timeline.json) · 공개판은 거부')
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
        how = V._DERIVED_HOW.get(d.get('method'), d.get('method') or '')
        drop = f" · 뺀 칸 {len(d.get('dropped_keys') or [])} 종" if d.get('dropped_keys') else ''
        refs = f" (참고 문헌 ← {d['refs_from']})" if d.get('refs_from') else ''
        print(f"   (만든 것) {d['name']} ← {d['from']}{refs} · {how}{drop}")
    exc = man.get('excluded') or []
    if exc:
        print(f"   공개판에서 뺀 것 {len(exc)} 개: " + ' · '.join(f"{e['name']} ({e['role']})" for e in exc))
    skipped = man.get('_skipped') or []
    if skipped:
        print(f"   넣지 않음 {len(skipped)} 개: " + ' · '.join(f'{n} ({w})' for n, w in skipped[:12])
              + (f' · 그 밖 {len(skipped) - 12} 개' if len(skipped) > 12 else ''))
    bc = man.get('build_check') or {}
    mp4 = f"{bc['mp4_s']} s" if bc.get('mp4_s') is not None else '못 잼'
    print(f"   판 대조: 통과 · MP4 {mp4} ↔ 시간표 끝 {bc.get('timeline_end_s')} s · 자막 {bc.get('srt_cues')} ↔ 시간표 자막 "
          f"{bc.get('timeline_captions')} · 장면 문장 {bc.get('scene_lines')} ↔ 시간표 문장 {bc.get('timeline_lines')}"
          + (f" · 미측정 {', '.join(bc['not_measured'])}" if bc.get('not_measured') else ''))
    dl = pc.get('deny_list')
    print(f"   공개 안전 검사: {'통과' if pc['ok'] else '걸림 ' + str(len(pc['hits'])) + ' 건 (내부판 · 기록만)'} · 규칙 {len(pc['rules'])} 종 · "
          f"글 파일 {pc['files']} 개 · 내부 숫자 목록 {str(dl['n']) + ' 개' if dl else '없이'}")
    print(f"   다음: python3 -I scripts/avi_register_episode.py {a.out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
