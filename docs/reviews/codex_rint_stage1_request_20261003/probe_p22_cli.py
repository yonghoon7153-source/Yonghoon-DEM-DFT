#!/usr/bin/env python3
"""Codex 요청 탐침 P2-2 — `--step3-rint-e/-i` 의 조용한 실패 (실물 파서로 확인).

`mpm_webapp_payload.main()` 이 만드는 **실제 파서**를 `parse_args` 가로채기로 얻는다 (규칙 M 과 같은 방식 —
필터를 쓰지 않고 실물을 잡는다).  그 파서로 세 경우를 본다:
  ① 값 없는 플래그 → [] → `parse_rint_table([])` = None → 항이 **조용히 꺼진다**
  ② 플래그 두 번 → 마지막 목록만 남는다 (첫 목록은 **조용히 버려진다**)
  ③ 전자 솔브에 SE|SE 쌍 → 거부되지 않는다 (전자 표에서 SE σ = 0 · SE 복셀 pid = −1 → 걸리는 면 0)

실행: 리포 뿌리에서 `python3 docs/reviews/codex_rint_stage1_request_20261003/probe_p22_cli.py`
"""
import argparse
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import mpm_webapp_payload as payload  # noqa: E402
from step3_sigma import parse_rint_table  # noqa: E402


class _Got(Exception):
    pass


def real_parser():
    cap = {}
    orig = argparse.ArgumentParser.parse_args

    def grab(self, *a, **k):
        cap['p'] = self
        raise _Got()

    argparse.ArgumentParser.parse_args = grab
    argv0 = sys.argv
    sys.argv = ['mpm_webapp_payload.py']
    try:
        payload.main()
    except _Got:
        pass
    finally:
        argparse.ArgumentParser.parse_args = orig
        sys.argv = argv0
    return cap['p']


if __name__ == '__main__':
    p = real_parser()
    for label, argv in (
        ('① 값 없는 플래그', ['--step3-rint-e']),
        ('② 플래그 두 번', ['--step3-rint-e', 'AM_S|VGCF=1e-3', '--step3-rint-e', 'AM_P|VGCF=2e-3']),
        ('③ 전자 솔브에 SE|SE', ['--step3-rint-e', 'SE|SE=1e-3']),
    ):
        ns, _ = p.parse_known_args(argv)
        v = ns.step3_rint_e
        print(f'{label}: argv {argv[1:]} → 인자 {v} → 솔버 표 {parse_rint_table(v)}')
