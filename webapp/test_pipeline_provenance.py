#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase B 회귀 — network/Stage E 세대 분리 · 단계 계약 · 프로세스간 lock.

`docs/codex_dem_webapp_code_review_20260807.md` 가 요구한 최소 회귀:
  • preserve 경로에서 **network solver 호출 0회**, force 경로에서 **1회**
  • preserve 경로에서 baseline 과 Stage E 의 parent run ID 가 **같다**
  • 옛 network 파일이 **바이트 그대로** 유지되면서 Stage E 만 정합하게 재생성
  • 필수 단계 실패가 'done' 이 되지 않는다
  • rc=0 이어도 기대 산출물이 없으면 실패 (network CLI 는 파일 없이 exit 0 이 될 수 있다)

subprocess 는 전부 **가짜 실행기**로 바꿔 센다 — 실제 solver 를 돌리지 않는다.

  python3 webapp/test_pipeline_provenance.py
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pipeline_service as ps          # noqa: E402

_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


class FakeRunner:
    """subprocess.run 대역 — 어떤 명령이 몇 번 불렸는지 세고, 산출물을 흉내낸다."""

    def __init__(self, results_dir, net_rc=0, net_writes=True, stage_e_rc=0):
        self.results_dir = results_dir
        self.calls = []
        self.net_rc, self.net_writes, self.stage_e_rc = net_rc, net_writes, stage_e_rc

    def count(self, needle):
        return sum(1 for c in self.calls if any(needle in str(a) for a in c))

    def __call__(self, cmd, **kw):
        self.calls.append(cmd)
        script = os.path.basename(str(cmd[1])) if len(cmd) > 1 else ''
        rc, out = 0, ''
        if script == 'network_conductivity.py':
            rc = self.net_rc
            if self.net_writes:
                # 새 solver 는 새 σ 를 쓴다 — 보존 경로에서 이게 나타나면 안 된다.
                with open(os.path.join(self.results_dir, 'network_conductivity.json'), 'w') as f:
                    json.dump({'sigma_full_mScm': 999.0}, f)
            out = 'fake solver'
        elif script == 'run_network_full_corrections.py':
            rc = self.stage_e_rc
            fm = os.path.join(self.results_dir, 'full_metrics.json')
            data = json.load(open(fm)) if os.path.exists(fm) else {}
            # Stage E 는 **화면에 남아 있는 baseline** 을 읽어 파생값을 만든다.
            data['sigma_full_mScm_stage_e'] = (data.get('sigma_full_mScm') or 0) * 2
            with open(fm, 'w') as f:
                json.dump(data, f)
            out = 'fake stage e'
        return subprocess.CompletedProcess(cmd, rc, out, '')


def _seed_case(d, sigma=1.0):
    """기존 세대의 network 산출물 + full_metrics 를 심는다."""
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'network_conductivity.json'), 'w') as f:
        json.dump({'sigma_full_mScm': sigma}, f)
    with open(os.path.join(d, 'full_metrics.json'), 'w') as f:
        json.dump({'porosity': 15.6}, f)
    ps.stamp_network_provenance(d, 'OLDRUN-0001', {'atoms.csv': 'deadbeef'})


def _sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    import app as webapp                                    # noqa: E402  (Flask 필요)

    # ══ 1) preserve 경로 — solver 0회 · 옛 baseline 유지 · Stage E 가 그것을 본다 ══
    tmp = tempfile.mkdtemp(prefix='pv_')
    try:
        src = os.path.join(tmp, 'src')
        _seed_case(src, sigma=1.0)
        old_sha = _sha(os.path.join(src, 'network_conductivity.json'))
        snap = ps.snapshot_network(src, 'c1')

        res = os.path.join(tmp, 'results')
        os.makedirs(res, exist_ok=True)
        with open(os.path.join(res, 'full_metrics.json'), 'w') as f:
            json.dump({'porosity': 15.6}, f)                # 새 파이프라인이 갓 만든 것
        fr = FakeRunner(res)
        log = []
        stages, run_id = webapp._network_and_stage_e(
            res, '/scripts', 'a.csv', 'c.csv', '1:AM,3:SE', 1000, log,
            preserve_network=True, network_snapshot=snap, runner=fr)

        chk('1) preserve → network solver 호출 0회',
            fr.count('network_conductivity.py') == 0)
        chk('2) preserve → Stage E 는 1회 호출',
            fr.count('run_network_full_corrections.py') == 1)
        chk('3) preserve → 옛 network 파일이 바이트 그대로',
            _sha(os.path.join(res, 'network_conductivity.json')) == old_sha)
        fm = json.load(open(os.path.join(res, 'full_metrics.json')))
        chk('4) preserve → baseline σ 가 옛 값(1.0), 새 solver 값(999) 아님',
            fm.get('sigma_full_mScm') == 1.0)
        chk('5) ★ Stage E 가 그 baseline 을 봤다 (1.0×2=2.0)',
            fm.get('sigma_full_mScm_stage_e') == 2.0)
        chk('6) ★ baseline 과 Stage E parent run ID 일치',
            fm.get('network_run_id') == 'OLDRUN-0001'
            and fm.get('stage_e_parent_network_run_id') == 'OLDRUN-0001')
        shutil.rmtree(snap, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 2) force 경로 — solver 정확히 1회 · 새 세대 도장 ══
    tmp = tempfile.mkdtemp(prefix='pf_')
    try:
        res = os.path.join(tmp, 'results')
        _seed_case(res, sigma=1.0)
        fr = FakeRunner(res)
        log = []
        stages, run_id = webapp._network_and_stage_e(
            res, '/scripts', 'a.csv', 'c.csv', '1:AM,3:SE', 1000, log,
            preserve_network=False, runner=fr)
        chk('7) force → network solver 정확히 1회',
            fr.count('network_conductivity.py') == 1)
        fm = json.load(open(os.path.join(res, 'full_metrics.json')))
        chk('8) force → 새 baseline(999) 이 반영', fm.get('sigma_full_mScm') == 999.0)
        chk('9) force → Stage E 가 새 baseline 을 봤다 (999×2)',
            fm.get('sigma_full_mScm_stage_e') == 1998.0)
        chk('10) force → 새 run_id 로 갱신 (옛 OLDRUN 아님)',
            run_id and run_id != 'OLDRUN-0001'
            and fm.get('network_run_id') == run_id
            and fm.get('stage_e_parent_network_run_id') == run_id)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3) rc=0 인데 산출물이 없으면 실패 (F-05/F-12) ══
    tmp = tempfile.mkdtemp(prefix='pn_')
    try:
        res = os.path.join(tmp, 'results')
        os.makedirs(res)
        with open(os.path.join(res, 'full_metrics.json'), 'w') as f:
            json.dump({}, f)
        fr = FakeRunner(res, net_rc=0, net_writes=False)     # exit 0 인데 파일 안 씀
        stages, _ = webapp._network_and_stage_e(
            res, '/scripts', 'a.csv', 'c.csv', '1:AM,3:SE', 1000, [],
            preserve_network=False, runner=fr)
        net = [s for s in stages if 'Network Solver' in s.get('step', '')][0]
        chk('11) ★ rc=0 이어도 기대 산출물이 없으면 실패로 본다',
            net['rc'] == 0 and not net['ok'] and net['missing_outputs'])
        status, failed = ps.summarize(stages)
        chk('12) ★ 그 실패가 필수 단계라 status=failed (done 이 아니다)',
            status == 'failed' and failed)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 4) 단계 계약 요약기 ══
    S = ps.StageOutcome
    chk('13) 선택 단계만 실패 → partial',
        ps.summarize([S(step='a', ok=True, required=True),
                      S(step='b', ok=False, required=False)])[0] == 'partial')
    chk('14) 전부 성공 → done',
        ps.summarize([S(step='a', ok=True, required=True)])[0] == 'done')

    # ══ 5) atomic write · provenance · lock ══
    tmp = tempfile.mkdtemp(prefix='pa_')
    try:
        p = os.path.join(tmp, 'x.json')
        ps.atomic_write_json(p, {'a': 1})
        chk('15) atomic_write_json 이 임시파일을 남기지 않는다',
            json.load(open(p)) == {'a': 1}
            and not [f for f in os.listdir(tmp) if f.startswith('.tmp_')])
        chk('16) 도장 없는 옛 산출물 → run_id None (조용히 지어내지 않는다)',
            ps.read_network_provenance(tmp).get('network_run_id') is None)
        with ps.network_lock(lock_dir=tmp) as got1:
            chk('17) 파일 lock 획득', got1 is True)
            with ps.network_lock(timeout=1, lock_dir=tmp) as got2:
                # 같은 프로세스의 flock 은 재획득되므로 '거부'를 단정하지 않는다.
                chk('18) 재진입이 예외 없이 처리된다', got2 in (True, False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\ntest_pipeline_provenance: {_ok}/{_ok + len(_fail)} PASS'
          + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
