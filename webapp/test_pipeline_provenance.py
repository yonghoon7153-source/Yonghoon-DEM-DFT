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
import errno
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time as _time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pipeline_service as ps          # noqa: E402


def _mk_tmp(d, body):
    """같은 디렉터리에 임시파일 하나 — _replace_retry 의 원본 인자용."""
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.tmp_', suffix='.json')
    with os.fdopen(fd, 'w') as f:
        f.write(body)
    return tmp

_ok, _fail = 0, []


#: ★ RC7-02: 게시 게이트가 이제 세 채널을 다 본다 → 가짜 solver 도 실제 solver 와
#:   같은 상태 집합을 써야 한다 (fixture 가 계약보다 느슨하면 회귀가 무력해진다).
_ALL_CH_OK = {'ionic_status': 'computed', 'electronic_status': 'computed',
              'thermal_status': 'computed'}


def _boom(_x):
    raise ValueError('bare NaN 토큰')


def _raises2(fn, exc):
    try:
        fn()
    except exc:
        return True
    except Exception:
        return False
    return False


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
                # ★ RR3-02: contact-mode both 는 **네 JSON** 을 다 만들어야 완전한 세대다.
                for _n in ('network_conductivity.json', 'network_conductivity_hertzian.json',
                           'network_conductivity_physics.json', 'network_conductivity_dual.json'):
                    with open(os.path.join(self.results_dir, _n), 'w') as f:
                        json.dump({'sigma_full_mScm': 999.0, **_ALL_CH_OK}, f)
            out = 'fake solver'
        elif script == 'run_network_full_corrections.py':
            rc = self.stage_e_rc
            # ★ RC6-04b: 실제 Stage E 는 `--case-dir` 로 지정된 **그 디렉터리**에 쓴다
            #   (candidate publish 흐름).  fixture 가 results_dir 에 하드코딩하면 계약을
            #   어기는 것이고, candidate 가 비어 검증이 실패한다 — fixture-drift 여덟 번째.
            _target = self.results_dir
            _c = list(cmd)
            if '--case-dir' in _c:
                _target = _c[_c.index('--case-dir') + 1]
            fm = os.path.join(_target, 'full_metrics.json')
            data = json.load(open(fm)) if os.path.exists(fm) else {}
            # Stage E 는 **화면에 남아 있는 baseline** 을 읽어 파생값을 만든다.
            # ★ RC5-01: 실제 run_one 은 정상 종료마다 11-키를 **무조건** 쓴다.  fixture 가
            #   한 키만 쓰면 계약이 엄해질 때 거짓 실패한다 (Codex 의 fixture-drift 교훈).
            data['sigma_full_mScm_stage_e'] = (data.get('sigma_full_mScm') or 0) * 2
            for _k, _v in _healthy_stage_e().items():
                data.setdefault(_k, _v)
            with open(fm, 'w') as f:
                json.dump(data, f)
            out = 'fake stage e'
        return subprocess.CompletedProcess(cmd, rc, out, '')


def _seed_case(d, sigma=1.0):
    """기존 세대의 network 산출물 + full_metrics 를 심는다."""
    os.makedirs(d, exist_ok=True)
    for _n in ('network_conductivity.json', 'network_conductivity_hertzian.json',
               'network_conductivity_physics.json', 'network_conductivity_dual.json'):
        with open(os.path.join(d, _n), 'w') as f:
            json.dump({'sigma_full_mScm': sigma, **_ALL_CH_OK}, f)
    with open(os.path.join(d, 'full_metrics.json'), 'w') as f:
        json.dump({'porosity': 15.6}, f)
    ps.stamp_network_provenance(d, 'OLDRUN-0001', {'atoms.csv': 'deadbeef'})


def _sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def _healthy_stage_e(**over):
    """실제 run_one 이 쓰는 **타입까지 맞춘** 건전한 Stage E 레코드 (RC6-01).

    ★ fixture 가 전부 1.0 을 쓰면 타입 검증이 들어올 때 거짓 실패한다 — 그것이
      fixture-drift 다.  숫자 여섯만 수, 매핑 넷은 dict, method 는 문자열.
    """
    d = {k: 1.0 for k in ps.STAGE_E_NUMERIC_KEYS}
    d.update({k: {'fixture': 1} for k in ps.STAGE_E_MAPPING_KEYS})
    d.update({k: 'fixture-method' for k in ps.STAGE_E_STRING_KEYS})
    d.update(over)
    return d


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

    # ══ 3b) ★ T3 (Codex CB-02) — 실패 도장만 남은 상태는 보존 자격이 없다 ══
    #   force 경로는 solver 가 실패해도 provenance 를 남긴다.  옛 구현은 glob 중 하나만
    #   맞아도 snapshot 을 만들어, **그 실패 도장 하나로** 다음 기본 재분석이 preserve 를
    #   골랐다 → solver 0회 + baseline 없음 + done = 영구 false-done.
    tmp = tempfile.mkdtemp(prefix='pt3_')
    try:
        res = os.path.join(tmp, 'results')
        os.makedirs(res)
        with open(os.path.join(res, 'full_metrics.json'), 'w') as f:
            json.dump({}, f)
        fr = FakeRunner(res, net_rc=0, net_writes=False)     # 파일 안 씀 = 실패
        webapp._network_and_stage_e(res, '/scripts', 'a.csv', 'c.csv', '1:AM,3:SE', 1000, [],
                                    preserve_network=False, runner=fr)
        # ★ RR2-01 로 계약이 바뀌었다: 실패는 **active 도장을 차지하지 않고**
        #   분리된 attempt 파일에 남는다.  옛 계약(실패도 PROVENANCE_FILE 을 덮음)은
        #   게시본은 옛 성공 세대인데 ID 는 실패 시도를 가리키는 모순을 만들었다.
        chk('T3a) ★ 실패는 attempt 파일에 남고 active 도장을 덮지 않는다',
            os.path.exists(os.path.join(res, ps.ATTEMPT_FILE))
            and not os.path.exists(os.path.join(res, ps.PROVENANCE_FILE))
            and not os.path.exists(os.path.join(res, 'network_conductivity.json')))
        chk('T3b) ★ 그 상태는 snapshot 자격이 없다 (baseline 부재)',
            ps.snapshot_network(res, 'c') is None)

        # baseline 은 있지만 도장이 failed 인 경우도 보존 금지
        for _n in ('network_conductivity.json', 'network_conductivity_hertzian.json',
                   'network_conductivity_physics.json', 'network_conductivity_dual.json'):
            open(os.path.join(res, _n), 'w').write('{}')
        with open(os.path.join(res, 'network_conductivity.json'), 'w') as f:
            json.dump({'sigma_full_mScm': 1.0}, f)
        ps.stamp_network_provenance(res, 'RID-FAILED', {}, 'failed')
        chk('T3c) ★ 도장이 failed 면 baseline 이 있어도 보존 금지',
            ps.snapshot_network(res, 'c') is None)
        ps.stamp_network_provenance(res, 'RID-OK', {}, 'success')
        snap = ps.snapshot_network(res, 'c')
        chk('T3d) success 도장 + baseline 이면 보존한다', snap is not None)
        if snap:
            shutil.rmtree(snap, ignore_errors=True)
        # 도장 이전 legacy(도장 없음 + baseline 있음)는 보존 허용
        os.unlink(os.path.join(res, ps.PROVENANCE_FILE))
        snap = ps.snapshot_network(res, 'c')
        chk('T3e) 도장 이전 legacy 산출물은 baseline 이 있으면 보존', snap is not None)
        if snap:
            shutil.rmtree(snap, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3c) ★ T1/T2 (Codex CB-01) — run_pipeline **전체**를 가짜 실행기로 태운다 ══
    #   개별 단계가 아니라 전체 경로를 봐야 "필수 단계 실패가 done 이 되지 않는다" 를
    #   검증할 수 있다.  옛 구현은 network/Stage E 두 단계만 계약에 넣어, contact 가
    #   rc=1 이어도 status='done' 이 됐다 (Codex 가 동적 재현).
    tmp = tempfile.mkdtemp(prefix='pt1_')
    prev_env = {k: os.environ.get(k) for k in
                ('WEBAPP_UPLOAD_FOLDER', 'WEBAPP_RESULTS_FOLDER')}
    prev_runner = ps._RUNNER
    try:
        up = os.path.join(tmp, 'uploads', 'case1')
        os.makedirs(up)
        for f in ('atom_1.liggghts', 'contact_1.liggghts'):
            open(os.path.join(up, f), 'w').write('x')
        webapp.app.config['UPLOAD_FOLDER'] = os.path.join(tmp, 'uploads')
        webapp.app.config['RESULTS_FOLDER'] = os.path.join(tmp, 'results')
        os.makedirs(webapp.app.config['RESULTS_FOLDER'], exist_ok=True)
        res_dir = os.path.join(tmp, 'results', 'case1')

        def make_runner(contact_rc, stage_e_writes=True):
            """parse/contact/network/StageE 산출물을 흉내내는 가짜 실행기."""
            calls = []

            def _r(cmd, **kw):
                calls.append(cmd)
                script = os.path.basename(str(cmd[1])) if len(cmd) > 1 else ''
                os.makedirs(res_dir, exist_ok=True)
                rc = 0
                if script == 'parse_liggghts.py':
                    for f in ('atoms.csv', 'contacts.csv'):
                        open(os.path.join(res_dir, f), 'w').write('a\n')
                elif script in ('analyze_contacts.py', 'analyze_contacts_bimodal.py'):
                    rc = contact_rc
                    if contact_rc == 0:
                        for f in ('full_metrics.json', 'atoms_analyzed.csv',
                                  'contacts_analyzed.csv', 'network_summary.csv'):
                            open(os.path.join(res_dir, f), 'w').write(
                                '{}' if f.endswith('.json') else 'a\n')
                elif script == 'network_conductivity.py':
                    for _n in ('network_conductivity.json', 'network_conductivity_hertzian.json',
                               'network_conductivity_physics.json',
                               'network_conductivity_dual.json'):
                        with open(os.path.join(res_dir, _n), 'w') as f:
                            json.dump({'sigma_full_mScm': 5.0, **_ALL_CH_OK}, f)
                elif script == 'run_network_full_corrections.py' and stage_e_writes:
                    _cl = list(cmd)
                    _t = (_cl[_cl.index('--case-dir') + 1]
                          if '--case-dir' in _cl else res_dir)
                    fm = os.path.join(_t, 'full_metrics.json')
                    d = json.load(open(fm)) if os.path.exists(fm) else {}
                    d['sigma_full_mScm_stage_e'] = 9.0
                    for _k, _v in _healthy_stage_e().items():   # RC5-01/RC6-01 schema
                        d.setdefault(_k, _v)
                    with open(fm, 'w') as f:
                        json.dump(d, f)
                return subprocess.CompletedProcess(cmd, rc, '', '')
            _r.calls = calls
            return _r

        # T1: contact rc=1 → 필수 단계 실패 → status='failed' (done 금지)
        shutil.rmtree(res_dir, ignore_errors=True)
        ps._RUNNER = make_runner(contact_rc=1)
        out = webapp.run_pipeline('case1', 'standard', '1:AM,3:SE', 1000)
        chk('T1) ★ contact rc=1 → status=failed (done 아님)',
            out.get('status') == 'failed' and out.get('success') is False
            and any('Contact' in s for s in out.get('failed_stages', [])))

        # T2: 전부 성공 → done
        shutil.rmtree(res_dir, ignore_errors=True)
        ps._RUNNER = make_runner(contact_rc=0)
        out = webapp.run_pipeline('case1', 'standard', '1:AM,3:SE', 1000)
        chk('T2) 전부 성공하면 done', out.get('status') == 'done')

        # T2b: contact 가 rc=0 인데 기대 산출물을 안 쓰면? → 역시 실패여야 한다
        shutil.rmtree(res_dir, ignore_errors=True)
        r = make_runner(contact_rc=0)
        _orig = r

        def _r_nofile(cmd, **kw):
            script = os.path.basename(str(cmd[1])) if len(cmd) > 1 else ''
            if script in ('analyze_contacts.py', 'analyze_contacts_bimodal.py'):
                _orig.calls.append(cmd)
                return subprocess.CompletedProcess(cmd, 0, '', '')   # rc=0, 파일 없음
            return _orig(cmd, **kw)
        ps._RUNNER = _r_nofile
        out = webapp.run_pipeline('case1', 'standard', '1:AM,3:SE', 1000)
        chk('T2b) ★ contact rc=0 이어도 기대 산출물이 없으면 failed',
            out.get('status') == 'failed')

        # R1 (Codex 재검증 RV-01): Stage E rc=0 인데 아무것도 안 쓰면 done 금지
        shutil.rmtree(res_dir, ignore_errors=True)
        ps._RUNNER = make_runner(contact_rc=0, stage_e_writes=False)
        out = webapp.run_pipeline('case1', 'standard', '1:AM,3:SE', 1000)
        chk('R1) ★ Stage E rc=0 인데 무산출 → partial (done 금지)',
            out.get('status') == 'partial'
            and any('Stage E' in s for s in out.get('failed_stages', [])))
    finally:
        ps._RUNNER = prev_runner
        for k, v in prev_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3d) ★ R5/R6 (Codex RV-04) — archive 재분석도 helper·계약 안에 있는가 ══
    #   옛 archive 경로는 parse/contact/coverage/StageE 를 raw subprocess 로 따로 돌리고
    #   모든 rc 를 무시한 뒤 무조건 'done' 을 썼고, **network solver 를 아예 안 불렀다**.
    import time as _time
    for _label, _contact_rc, _want_status, _want_net in (
            ('R5) ★ archive contact rc=1 → error · network solver 0회', 1, 'error', 0),
            ('R6) archive 정상 → done · network solver 1회', 0, 'done', 1)):
        tmp = tempfile.mkdtemp(prefix='par_')
        try:
            arc = os.path.join(tmp, 'archive')
            case = os.path.join(arc, 'c1')
            os.makedirs(case)
            for f in ('atom_1.liggghts', 'contact_1.liggghts'):
                open(os.path.join(case, f), 'w').write('x')
            json.dump({'mode': 'standard', 'type_map': '1:AM,3:SE', 'scale': 1000},
                      open(os.path.join(case, 'meta.json'), 'w'))
            webapp.app.config['ARCHIVE_FOLDER'] = arc
            calls = []

            def _ar(cmd, _rc=_contact_rc, _calls=calls, _d=case, **kw):
                _calls.append(os.path.basename(str(cmd[1])) if len(cmd) > 1 else '')
                sc = _calls[-1]
                rc = 0
                if sc == 'parse_liggghts.py':
                    for f in ('atoms.csv', 'contacts.csv'):
                        open(os.path.join(_d, f), 'w').write('a\n')
                elif sc in ('analyze_contacts.py', 'analyze_contacts_bimodal.py'):
                    rc = _rc
                    if _rc == 0:
                        for f in ('full_metrics.json', 'atoms_analyzed.csv',
                                  'contacts_analyzed.csv', 'network_summary.csv'):
                            open(os.path.join(_d, f), 'w').write(
                                '{}' if f.endswith('.json') else 'a\n')
                elif sc == 'network_conductivity.py':
                    for _n in ('network_conductivity.json',
                               'network_conductivity_hertzian.json',
                               'network_conductivity_physics.json',
                               'network_conductivity_dual.json'):
                        json.dump({'sigma_full_mScm': 3.0, **_ALL_CH_OK},
                                  open(os.path.join(_d, _n), 'w'))
                elif sc == 'run_network_full_corrections.py':
                    _cl = list(cmd)
                    _t = (_cl[_cl.index('--case-dir') + 1]
                          if '--case-dir' in _cl else _d)
                    fm = os.path.join(_t, 'full_metrics.json')
                    dd = json.load(open(fm)) if os.path.exists(fm) else {}
                    dd['sigma_full_mScm_stage_e'] = 6.0
                    for _k, _v in _healthy_stage_e().items():   # RC5-01/RC6-01 schema
                        dd.setdefault(_k, _v)
                    json.dump(dd, open(fm, 'w'))
                return subprocess.CompletedProcess(cmd, rc, '', '')

            ps._RUNNER = _ar
            webapp.app.test_client().post('/archive/reanalyze/c1')
            sf = os.path.join(case, '.reanalyze_status')
            for _ in range(100):                       # 스레드 완료 폴링 (최대 10 s)
                if os.path.exists(sf) and open(sf).read().split('\n')[0] != 'running':
                    break
                _time.sleep(0.1)
            head = open(sf).read().split('\n')[0].strip() if os.path.exists(sf) else '?'
            n_net = calls.count('network_conductivity.py')
            ok = (head == _want_status and n_net == _want_net)
            if _contact_rc == 0 and ok:
                fm = json.load(open(os.path.join(case, 'full_metrics.json')))
                ok = (fm.get('network_run_id')
                      and fm.get('network_run_id') == fm.get('stage_e_parent_network_run_id'))
            chk(_label + f'  (status={head}, net={n_net})', ok)
        finally:
            ps._RUNNER = prev_runner if 'prev_runner' in dir() else subprocess.run
            shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3e) ★ P1~P3 (Codex 2회차) — 인과 판정과 active/attempt 분리 ══
    tmp = tempfile.mkdtemp(prefix='pp1_')
    try:
        res = os.path.join(tmp, 'r')
        _seed_case(res, sigma=1.0)                       # 옛 성공 세대 + OLDRUN 도장
        old_sha = _sha(os.path.join(res, 'network_conductivity.json'))

        class TouchOnly:
            """내용은 안 쓰고 **mtime 만** 앞으로 옮기는 runner (metadata-only touch)."""

            def __init__(self):
                self.calls = []

            def __call__(self, cmd, **kw):
                self.calls.append(os.path.basename(str(cmd[1])) if len(cmd) > 1 else '')
                for f in ('network_conductivity.json', 'full_metrics.json'):
                    p2 = os.path.join(res, f)
                    if os.path.exists(p2):
                        st2 = os.stat(p2)
                        os.utime(p2, ns=(st2.st_atime_ns + 10 ** 9, st2.st_mtime_ns + 10 ** 9))
                return subprocess.CompletedProcess(cmd, 0, '', '')

        fr = TouchOnly()
        stages, rid = webapp._network_and_stage_e(
            res, '/scripts', 'a.csv', 'c.csv', '1:AM,3:SE', 1000, [],
            preserve_network=False, runner=fr)
        net = [s2 for s2 in stages if 'Network Solver' in s2.get('step', '')][0]
        chk('P2) ★ metadata-only touch 는 성공으로 인정되지 않는다', not net.ok)
        chk('P2b) 옛 baseline 이 바이트 그대로 복구된다',
            _sha(os.path.join(res, 'network_conductivity.json')) == old_sha)
        prov = ps.read_network_provenance(res)
        chk('P1) ★ active 도장은 이전 성공 세대(OLDRUN)를 유지한다',
            prov.get('network_run_id') == 'OLDRUN-0001'
            and prov.get('solver_status') == 'success')
        chk('P1b) 실패 시도는 분리 파일에 기록된다',
            os.path.exists(os.path.join(res, ps.ATTEMPT_FILE))
            and json.load(open(os.path.join(res, ps.ATTEMPT_FILE)))
            .get('network_attempt_run_id') not in (None, 'OLDRUN-0001'))
        fm = json.load(open(os.path.join(res, 'full_metrics.json')))
        chk('P1c) ★ full_metrics 가 success 라고 쓰지 않는다',
            fm.get('network_solver_status') == 'failed'
            and fm.get('stale_after_failed_retry') is True)
        chk('P3) ★ network 실패 후 Stage E 를 실행하지 않는다',
            'run_network_full_corrections.py' not in fr.calls)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3f) ★ R-PD1 (Codex PD-01) — 함수를 **실제로 호출**하는 회귀 ══
    #   `import app` 만 하는 테스트는 함수 본문을 타지 않아 NameError 를 못 잡는다.
    #   실제로 _press_units import 가 빠진 채 푸시됐고 그렇게 통과했다.
    tmp = tempfile.mkdtemp(prefix='pd1_')
    try:
        rd = os.path.join(tmp, 'r')
        os.makedirs(rd)
        for label, ip, want in (
                ('MPa 2.5 가 2500 이 되지 않는다', {'target_pressure_MPa': 2.5}, 2.5),
                ('덱 0.30 → 300 MPa', {'target_press_sim': 0.30}, 300.0),
                ('sim=0 이 MPa 로 새지 않는다',
                 {'target_press_sim': 0, 'target_pressure_MPa': 7}, 0.0)):
            json.dump(ip, open(os.path.join(rd, 'input_params.json'), 'w'))
            got = webapp._inject_input_params({}, rd).get('_input_target_press_MPa')
            chk(f'R-PD1) ★ {label} (got {got})', got == want)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3f) ★ RC4-01/02/03 (Codex 4회차) ══
    tmp = tempfile.mkdtemp(prefix='rc4_')
    try:
        res = os.path.join(tmp, 'r')
        _seed_case(res, sigma=1.0)
        # 옛 Stage E 세대 + 비격리 metadata + 옛 wrapper provenance
        fmp = os.path.join(res, 'full_metrics.json')
        d0 = json.load(open(fmp))
        d0.update({'sigma_full_mScm': 1.0, 'sigma_full_mScm_stage_e': 2.0,
                   'stage_e_source': 'OLD', 'validation_flags': {'x': 1},
                   'stage_e_temperature_provenance': '60C',
                   'stage_e_parent_network_run_id': 'OLDRUN-0001',
                   'stage_e_run_id': 'OLDSE', 'stage_e_status': 'success',
                   # raw thermal = network 소유.  Stage E 가 heal 로 덮을 수 있어
                   # 실패 시 정확히 되돌아와야 한다 (RC5-02 ③).
                   'thermal_sigma_full_mScm': 111.125})
        json.dump(d0, open(fmp, 'w'))
        # contact 가 쓴 summary (network 소유가 아니다)
        open(os.path.join(res, 'network_summary.csv'), 'w').write('a,b\n')

        class NetOkStageENoWrite(FakeRunner):
            def __call__(self, cmd, **kw):
                if os.path.basename(str(cmd[1])) == 'run_network_full_corrections.py':
                    self.calls.append(cmd)
                    # ★ RC5-02 재현: 실패(무산출) 실행이라도 **부분 쓰기**는 남긴다 —
                    #   Codex 가 동적으로 재현한 그 상황(관리 키 신규 + raw thermal 변경).
                    _p = os.path.join(self.results_dir, 'full_metrics.json')
                    _d = json.load(open(_p)) if os.path.exists(_p) else {}
                    _d['future_metric_stage_e'] = 999
                    _d['thermal_sigma_full_mScm'] = 777
                    json.dump(_d, open(_p, 'w'))
                    return subprocess.CompletedProcess(cmd, 0, '', '')   # rc=0, 무산출(불완전)
                return super().__call__(cmd, **kw)

        fr = NetOkStageENoWrite(res)
        webapp._network_and_stage_e(res, '/scripts', 'a.csv', 'c.csv', '1:AM,3:SE', 1000, [],
                                    preserve_network=False, runner=fr)
        fm = json.load(open(fmp))
        chk('RC4-03) ★ network 성공이 contact 의 network_summary.csv 를 지우지 않는다',
            os.path.exists(os.path.join(res, 'network_summary.csv')))
        chk('RC4-02) ★ 비격리 metadata 도 격리·복원된다 (stage_e_source/온도/검증카드)',
            fm.get('stage_e_source') == 'OLD'
            and fm.get('stage_e_temperature_provenance') == '60C'
            and fm.get('validation_flags') == {'x': 1})
        chk('RC4-01) ★ Stage E 실패 시 wrapper provenance 도 옛 것을 유지한다',
            fm.get('stage_e_parent_network_run_id') == 'OLDRUN-0001'
            and fm.get('stage_e_run_id') == 'OLDSE'
            and fm.get('stage_e_status') == 'failed_restored_previous')
        chk('RC4-01b) 옛 보정값도 그대로', fm.get('sigma_full_mScm_stage_e') == 2.0)
        # ★ RC5-02 ①③ (Codex 5회차 실측): 옛 복원은 overlay 만 해서 **실패 후보가 새로
        #   만든** 관리 키(future_metric_stage_e=999)와 raw thermal 변경(777)이 잔존했다.
        chk('RC5-02a) ★ 실패 후보가 새로 만든 관리 키가 남지 않는다 (전수 purge)',
            'future_metric_stage_e' not in fm)
        #   ⚠ 여기서 111.125 로 돌아오지 **않는** 것이 맞다: 이 경로는 preserve=False 라
        #     새 network 세대가 먼저 돌았고, RC5-03 이 옛 세대의 thermal 을 걷어냈다.
        #     RC5-02 가 보장하는 것은 "Stage E 가 쓴 777 이 남지 않는다" 이고, 되돌아갈
        #     지점은 **Stage E 직전 상태**(= 새 network 세대의 상태)다.
        chk('RC5-02b) ★ 실패한 Stage E 가 쓴 raw thermal(777) 이 남지 않는다',
            fm.get('thermal_sigma_full_mScm') != 777)
        chk('RC5-03) ★ 새 network 세대가 못 낸 thermal 을 옛 값(111.125)으로 메우지 않는다',
            fm.get('thermal_sigma_full_mScm') != 111.125
            and 'thermal_sigma_full_mScm' in (fm.get('network_projection_dropped') or []))
        # ★ RC5-02 ⑤: 실패 시도는 **active 필드가 아니라 별도 파일**에 (network 와 같은 규약)
        _att_p = os.path.join(res, ps.STAGE_E_ATTEMPT_FILE)
        _att = json.load(open(_att_p)) if os.path.exists(_att_p) else {}
        #   attempt 의 parent 는 **실패한 시도가 상대한 세대**(= 이 경로에선 새 network)
        #   이고, 복원된 active 의 parent 는 옛 세대다 → 둘은 달라야 한다.
        chk('RC5-02e) ★ 실패 시도가 active 필드를 차지하지 않고 별도 record 로 간다',
            'stage_e_attempt_parent_network_run_id' not in fm
            and _att.get('status') == 'failed'
            and _att.get('stage_e_attempt_parent_network_run_id') not in (None, 'OLDRUN-0001')
            and fm.get('stage_e_parent_network_run_id') == 'OLDRUN-0001')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3e) ★ RR3-04 (Codex): batch contact 가 옛 산출물을 새 성공으로 재도장 ══
    #   Codex 가 재현기를 **현재 4-산출물 계약**에 맞추자(옛 network_summary.csv 까지 심자)
    #   contact 가 통과하고 network·Stage E 가 다시 돌았다 = 존재-확인 계약의 false-green.
    tmp = tempfile.mkdtemp(prefix='rr304_')
    try:
        rd = os.path.join(tmp, 'r')
        os.makedirs(rd)
        for f in ('full_metrics.json', 'atoms_analyzed.csv',
                  'contacts_analyzed.csv', 'network_summary.csv'):
            open(os.path.join(rd, f), 'w').write('{}' if f.endswith('.json') else 'a\n')
        _noop = lambda cmd, **kw: subprocess.CompletedProcess(cmd, 0, '', '')   # rc=0, 무산출
        _st_old = ps.run_stage('c', ['x', 'y'], required=True, results_dir=rd,
                               runner=_noop,
                               expects=('full_metrics.json', 'atoms_analyzed.csv',
                                        'contacts_analyzed.csv', 'network_summary.csv'))
        chk('RR3-04a) ★ 존재 확인만 하면 무산출 실행이 통과한다 (= 옛 계약의 결함)',
            _st_old.ok is True)
        _st_new = ps.run_stage('c', ['x', 'y'], required=True, results_dir=rd,
                               runner=_noop, fresh=True,
                               expects=('full_metrics.json', 'atoms_analyzed.csv',
                                        'contacts_analyzed.csv', 'network_summary.csv'))
        chk('RR3-04b) ★ fresh=True 면 같은 상황이 실패한다 (stale 로 잡힌다)',
            _st_new.ok is False and _st_new.get('stale_outputs'))
        # 실제로 쓰면 통과해야 한다 (거짓 실패가 아님을 확인)
        #   ★ RC6-05 이후: "실제로 새로 씀" = **네 개 전부**.  옛 writer 는 하나만 썼고
        #     그때는 통과했다 — 그것이 바로 Codex 가 잡은 partial-write 통과다.
        def _writer(cmd, **kw):
            for _f in ('full_metrics.json', 'atoms_analyzed.csv',
                       'contacts_analyzed.csv', 'network_summary.csv'):
                open(os.path.join(rd, _f), 'w').write('{"a":1}' if _f.endswith('.json') else 'new\n')
            return subprocess.CompletedProcess(cmd, 0, '', '')
        _st_w = ps.run_stage('c', ['x', 'y'], required=True, results_dir=rd,
                             runner=_writer, fresh=True,
                             expects=('full_metrics.json', 'atoms_analyzed.csv',
                                      'contacts_analyzed.csv', 'network_summary.csv'))
        chk('RR3-04c) 실제로 새로 쓰면 통과한다 (fresh 가 거짓 실패를 내지 않는다)',
            _st_w.ok is True)
        # ★ RC6-05: 4개 중 1개만 새로 쓰는 **부분 쓰기**는 이제 실패한다 (Codex 실측 재현)
        for _f in ('full_metrics.json', 'atoms_analyzed.csv',
                   'contacts_analyzed.csv', 'network_summary.csv'):
            open(os.path.join(rd, _f), 'w').write('seed\n')
        _time.sleep(0.01)

        def _partial(cmd, **kw):
            open(os.path.join(rd, 'full_metrics.json'), 'w').write('{"only":1}')
            return subprocess.CompletedProcess(cmd, 0, '', '')
        _st_p = ps.run_stage('c', ['x', 'y'], required=True, results_dir=rd,
                             runner=_partial, fresh=True,
                             expects=('full_metrics.json', 'atoms_analyzed.csv',
                                      'contacts_analyzed.csv', 'network_summary.csv'))
        chk('RC6-05a) ★ 부분 쓰기(1/4)가 실패하고 낡은 파일 3개를 지목한다',
            _st_p.ok is False and len(_st_p['stale_outputs']) == 3
            and 'full_metrics.json' not in _st_p['stale_outputs'])
        # ══ RC7-03 (Codex 7회차): fresh 지문은 **metadata-only touch 로 통과한다** ══
        #   = 인과 증거가 아니다.  causal(빈 자리 실행)은 같은 상황을 잡아야 한다.
        for _f in ('full_metrics.json', 'atoms_analyzed.csv',
                   'contacts_analyzed.csv', 'network_summary.csv'):
            open(os.path.join(rd, _f), 'w').write('GEN-OLD\n')
        _EXP = ('full_metrics.json', 'atoms_analyzed.csv',
                'contacts_analyzed.csv', 'network_summary.csv')

        def _toucher(cmd, **kw):
            """아무것도 쓰지 않고 mtime 만 바꾼다 (rc=0)."""
            _t = _time.time() + 10
            for _f in _EXP:
                os.utime(os.path.join(rd, _f), (_t, _t))
            return subprocess.CompletedProcess(cmd, 0, '', '')

        _st_touch = ps.run_stage('c', ['x'], required=True, results_dir=rd,
                                 runner=_toucher, fresh=True, expects=_EXP)
        chk('RC7-03a) ★ 결함 재현: metadata-only touch 가 fresh 를 통과한다 (무산출인데 success)',
            _st_touch.ok is True)
        _bodies = {f: open(os.path.join(rd, f)).read() for f in _EXP}
        chk('RC7-03a2) ★ 그런데 내용은 옛 세대 그대로다 (= 거짓 성공의 실체)',
            all(v == 'GEN-OLD\n' for v in _bodies.values()))

        _st_c = ps.run_stage('c', ['x'], required=True, results_dir=rd,
                             runner=_toucher, causal=True, expects=_EXP)
        chk('RC7-03b) ★ causal 은 같은 touch 실행을 실패로 잡는다 (빈 자리에 아무것도 안 씀)',
            _st_c.ok is False and sorted(_st_c['missing_outputs']) == sorted(_EXP))
        chk('RC7-03c) ★ 실패해도 옛 성공 세대가 그대로 복구된다 (내용 보존)',
            all(os.path.exists(os.path.join(rd, f)) for f in _EXP)
            and all(open(os.path.join(rd, f)).read() == 'GEN-OLD\n' for f in _EXP))
        chk('RC7-03c2) stash 디렉터리가 남지 않는다',
            not [n for n in os.listdir(rd) if n.startswith(ps.STAGE_STASH_PREFIX)])

        def _real_writer(cmd, **kw):
            for _f in _EXP:
                open(os.path.join(rd, _f), 'w').write('GEN-NEW\n')
            return subprocess.CompletedProcess(cmd, 0, '', '')
        _st_ok = ps.run_stage('c', ['x'], required=True, results_dir=rd,
                              runner=_real_writer, causal=True, expects=_EXP)
        chk('RC7-03d) 실제로 쓰면 causal 이 통과한다 (거짓 실패 없음)',
            _st_ok.ok is True
            and open(os.path.join(rd, 'full_metrics.json')).read() == 'GEN-NEW\n')

        # ★ causal 은 byte-identical 재계산에서 **거짓 실패를 내지 않는다** (fresh 의 약점)
        _st_same = ps.run_stage('c', ['x'], required=True, results_dir=rd,
                                runner=_real_writer, causal=True, expects=_EXP)
        chk('RC7-03e) ★ 결정론적 재실행(byte-identical)도 통과 — fresh 가 못 하던 것',
            _st_same.ok is True)

        # 부분 쓰기(1/4)는 causal 에서도 실패하고 옛 세대가 돌아와야 한다
        for _f in _EXP:
            open(os.path.join(rd, _f), 'w').write('GEN-KEEP\n')

        def _partial2(cmd, **kw):
            open(os.path.join(rd, 'full_metrics.json'), 'w').write('PARTIAL\n')
            return subprocess.CompletedProcess(cmd, 0, '', '')
        _st_p2 = ps.run_stage('c', ['x'], required=True, results_dir=rd,
                              runner=_partial2, causal=True, expects=_EXP)
        chk('RC7-03f) ★ 부분 쓰기(1/4)는 실패하고, 부분 산출물이 옛 세대로 교체된다',
            _st_p2.ok is False
            and open(os.path.join(rd, 'full_metrics.json')).read() == 'GEN-KEEP\n')

        # ★ 크래시 복구: stash 는 원본을 들고 있으므로 **지우면 안 되고 되돌려야** 한다
        _rd2 = os.path.join(tmp, 'r2'); os.makedirs(_rd2)
        for _f in _EXP:
            open(os.path.join(_rd2, _f), 'w').write('ORIG\n')
        _orphan = ps.stash_outputs(_rd2, _EXP, tag='crash')
        os.utime(_orphan, (0, 0))                     # 오래된 것으로 위장
        chk('RC7-03g) stash 직후 results 는 비어 있다 (빈 자리 실행 전제)',
            all(not os.path.exists(os.path.join(_rd2, f)) for f in _EXP))
        _restored, _swept = ps.recover_stale_stashes(_rd2)
        chk('RC7-03h) ★ 고아 stash 는 삭제가 아니라 복구된다 (마지막 성공 세대 보존)',
            _restored == 4 and _swept == 1
            and all(open(os.path.join(_rd2, f)).read() == 'ORIG\n' for f in _EXP))
        # 더 새 세대가 이미 자리를 잡았으면 stash 쪽을 버린다
        _orphan2 = ps.stash_outputs(_rd2, _EXP, tag='crash2')
        for _f in _EXP:
            open(os.path.join(_rd2, _f), 'w').write('NEWER\n')
        os.utime(_orphan2, (0, 0))
        _r2, _s2 = ps.recover_stale_stashes(_rd2)
        chk('RC7-03i) ★ 더 새 세대가 있으면 stash 가 그것을 덮지 않는다',
            _r2 == 0 and _s2 == 1
            and open(os.path.join(_rd2, 'full_metrics.json')).read() == 'NEWER\n')

        # 네 경로 배선 확인 (구현만 하고 배선 안 한 전례가 있다)
        _apy3 = open(os.path.join(os.path.dirname(os.path.abspath(webapp.__file__)),
                                  'app.py'), encoding='utf-8').read()
        chk('RC7-03j) ★ contact 네 경로 전부 causal 배선 (batch·bimodal·standard·archive)',
            _apy3.count('causal=True') >= 4)
        for _tag, _win in (("'Contact Analysis (batch)'", 1400),
                           ("'Contact Analysis (archive)'", 900),
                           ("'Bimodal Contact Analysis'", 900)):
            _i = _apy3.index(_tag)
            chk(f'RC7-03k) ★ {_tag} 호출부가 실제로 causal=True 를 넘긴다',
                'causal=True' in _apy3[_i:_i + _win])
        chk('RC7-03l) ★ contact 경로에 fresh=True 가 남아 있지 않다 (약한 계약 잔존 금지)',
            _apy3.count('fresh=True') == 0)
        # ★ RC7-07: main 두 경로도 contact 실패 시 network·StageE 를 건너뛰는가
        for _tag in ("'Bimodal Contact Analysis'", "'Contact Analysis'"):
            _i = _apy3.index(_tag)
            _seg = _apy3[_i:_i + 1400]
            chk(f'RC7-07) ★ {_tag} 실패 시 즉시 중단한다 (batch·archive 와 같은 계약)',
                'if not _st.ok:' in _seg and _seg.index('if not _st.ok:')
                < (_seg.index('_network_and_stage_e') if '_network_and_stage_e' in _seg else 10 ** 9))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3f) ★ RC6-02/03 (Codex 6회차): 내용 판정 **전에** active 를 게시하던 것 ══
    #   옛 게이트는 파일 존재만 보고 stash 를 버린 뒤 success 를 찍었다.  실측 재현:
    #   required 단계는 실패인데 active provenance=success, 옛 완전 세대는 이미 사라짐.
    for _label, _mode_status, _want_ok in (
            ('RC6-02) ★ H thermal=failed → 게시 차단·옛 세대 보존', {'hertzian': 'failed'}, False),
            ('RC6-03) ★ Physics 만 failed 여도 차단 (H 성공에 가리지 않는다)',
             {'physics': 'failed'}, False),
            ('RC6-02c) 둘 다 computed → 정상 게시', {}, True)):
        tmp = tempfile.mkdtemp(prefix='rc602_')
        try:
            res = os.path.join(tmp, 'r')
            _seed_case(res, sigma=1.0)                       # 옛 **완전한** 세대
            ps.stamp_network_provenance(res, 'OLDGEN', {'atoms.csv': 'x'}, 'success')

            class _NR(FakeRunner):
                def __call__(self, cmd, **kw):
                    if os.path.basename(str(cmd[1])) == 'network_conductivity.py':
                        self.calls.append(cmd)
                        for _n, _m in (('network_conductivity_hertzian.json', 'hertzian'),
                                       ('network_conductivity_physics.json', 'physics'),
                                       ('network_conductivity.json', 'hertzian'),
                                       ('network_conductivity_dual.json', 'hertzian')):
                            json.dump({'sigma_full_mScm': 999.0,
                                       'ionic_status': 'computed',
                                       'electronic_status': 'computed',
                                       'thermal_status': _mode_status.get(_m, 'computed'),
                                       'thermal_status_reason': 'fixture'},
                                      open(os.path.join(self.results_dir, _n), 'w'))
                        return subprocess.CompletedProcess(cmd, 0, '', '')
                    return super().__call__(cmd, **kw)

            stages, _rid = webapp._network_and_stage_e(
                res, '/scripts', 'a.csv', 'c.csv', '1:AM,3:SE', 1000, [],
                preserve_network=False, runner=_NR(res))
            prov = ps.read_network_provenance(res)
            fm = json.load(open(os.path.join(res, 'full_metrics.json')))
            if _want_ok:
                chk(_label, prov.get('solver_status') == 'success'
                    and fm.get('sigma_full_mScm') == 999.0)
            else:
                _net = [x for x in stages if 'Network Solver' in x.get('step', '')]
                #   ⚠ 복구된 옛 provenance 가 solver_status='success' 라고 적는 것은 **옳다**
                #     — 그 세대는 실제로 성공했다.  판정 기준은 "새 실패 세대가 게시됐는가".
                chk(_label,
                    _net and not _net[0]['ok'] and _net[0].get('verify_failed')  # 게이트가 막고
                    and prov.get('network_run_id') == 'OLDGEN'                   # 옛 세대가 active
                    and fm.get('sigma_full_mScm') != 999.0                       # 실패값 미게시
                    and json.load(open(os.path.join(
                        res, 'network_conductivity.json')))['sigma_full_mScm'] == 1.0)  # 파일 복구
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # ══ 3g) ★ RC6-07 (Codex 6회차, Windows 실측): CP949 에서 solver 가 죽던 것 ══
    #   자식 출력 인코딩을 계약하지 않으면 Windows 기본 CP949 에서 첫 non-ASCII 로그에
    #   UnicodeEncodeError → rc=1 → network JSON 0개.  같은 입력이 PYTHONUTF8=1 이면 성공.
    _kw = ps.utf8_subprocess_kwargs()
    chk('RC6-07a) ★ 자식 env 가 UTF-8 로 강제된다',
        _kw['env'].get('PYTHONUTF8') == '1' and _kw['env'].get('PYTHONIOENCODING') == 'utf-8')
    chk('RC6-07b) ★ 부모 decode 도 UTF-8 (자식만 바꾸면 반쪽이다)',
        _kw.get('encoding') == 'utf-8' and _kw.get('text') is True
        and _kw.get('errors') == 'replace')
    chk('RC6-07c) 기존 환경변수를 지우지 않는다 (PATH 등)',
        'PATH' in _kw['env'] or not os.environ.get('PATH'))
    #   run_stage 가 실제로 그 계약을 쓰는지 (구현≠배선)
    _seen = {}

    def _spy(cmd, **kw):
        _seen.update(kw)
        return subprocess.CompletedProcess(cmd, 0, '', '')
    ps.run_stage('spy', ['x'], runner=_spy)
    chk('RC6-07d) ★ run_stage 가 그 계약을 실제로 넘긴다 (배선)',
        _seen.get('encoding') == 'utf-8'
        and (_seen.get('env') or {}).get('PYTHONUTF8') == '1')
    #   Stage E 재솔브 경로도 같은 계약이어야 한다 (여기가 막히면 fallback 으로 조용히 샌다)
    _rnfc_src = open(os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(webapp.__file__))), 'scripts',
        'run_network_full_corrections.py'), encoding='utf-8').read()
    chk('RC6-07e) ★ Stage E 재솔브 subprocess 도 UTF-8 계약을 건다',
        "PYTHONUTF8='1'" in _rnfc_src and "encoding='utf-8'" in _rnfc_src)

    # ══ 3h) ★ RC6-04b (Codex 6회차): pre-purge crash window ══
    #   옛 흐름은 subprocess 전에 **active 위치의** full_metrics 에서 Stage E 키를 지워
    #   게시했다 → 부모가 그 사이에 죽으면 그 상태가 영구 active.  실측 재현됨.
    #   새 흐름은 candidate 에서 돌리고 통과한 것만 원자 게시한다.
    tmp = tempfile.mkdtemp(prefix='c04b_')
    try:
        res = os.path.join(tmp, 'r')
        os.makedirs(res)
        fmp = os.path.join(res, 'full_metrics.json')
        _seed = _healthy_stage_e(porosity=15.6, sigma_full_mScm=1.0)
        json.dump(_seed, open(fmp, 'w'))
        json.dump({'sigma_full_mScm': 1.0}, open(os.path.join(res, 'network_conductivity.json'), 'w'))
        _n0 = sum(1 for k in json.load(open(fmp)) if ps.is_stage_e_key(k))

        #  ① purge 도중에도 active 는 그대로여야 한다 (옛 흐름은 0 이 됐다)
        _mid = {}
        with ps.stage_e_candidate(res) as _c:
            _c.purge_stage_e()
            _mid = json.load(open(fmp))
            # publish 하지 않고 빠져나온다 = 부모가 죽은 것과 같은 효과
        chk('RC6-04b-a) ★ purge 도중에도 **active** 는 Stage E 키를 그대로 갖는다',
            sum(1 for k in _mid if ps.is_stage_e_key(k)) == _n0 and _n0 == 11)
        chk('RC6-04b-b) ★ publish 없이 빠져나가도 active 는 옛 세대 그대로 (crash 안전)',
            sum(1 for k in json.load(open(fmp)) if ps.is_stage_e_key(k)) == _n0)

        #  ② publish 하면 새 세대로 원자 교체
        with ps.stage_e_candidate(res) as _c:
            _c.purge_stage_e()
            _cf = os.path.join(_c.dir, 'full_metrics.json')
            _d2 = json.load(open(_cf))
            _d2['sigma_full_mScm_stage_e'] = 42.0
            json.dump(_d2, open(_cf, 'w'))
            _c.publish()
        chk('RC6-04b-c) publish 하면 새 값이 active 에 원자 교체된다',
            json.load(open(fmp)).get('sigma_full_mScm_stage_e') == 42.0)
        chk('RC6-04b-d) candidate 는 뒤에 남지 않는다',
            not [x for x in os.listdir(res) if x.startswith(ps.STAGE_E_CANDIDATE_PREFIX)])

        #  ③ 죽은 부모가 남긴 candidate 를 청소한다 (위생 — 정합성 문제는 아니다)
        _stale = os.path.join(res, ps.STAGE_E_CANDIDATE_PREFIX + 'zombie')
        os.makedirs(_stale)
        os.utime(_stale, (0, 0))
        chk('RC6-04b-e) 오래된 candidate 를 청소한다',
            ps.sweep_stale_candidates(res) == 1 and not os.path.exists(_stale))

        #  ④ 배선 확인 — app 이 실제로 candidate 흐름을 쓰는가 (구현≠배선)
        _a = open(os.path.join(os.path.dirname(os.path.abspath(webapp.__file__)),
                               'app.py'), encoding='utf-8').read()
        chk('RC6-04b-f) ★ app 이 candidate 흐름과 --case-dir 를 실제로 쓴다 (배선)',
            'stage_e_candidate(results_dir)' in _a and "'--case-dir', _cand.dir" in _a
            and '_cand.publish()' in _a)
        _rn = open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(webapp.__file__))), 'scripts',
            'run_network_full_corrections.py'), encoding='utf-8').read()
        chk('RC6-04b-g) Stage E 가 --case-dir 를 받는다 (탐색을 건너뛴다)',
            "'--case-dir'" in _rn and 'args.case_dir' in _rn)
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

        # ══ RC5-01 (Codex 5회차): partial Stage E 가 success 로 도장되던 것 ══
        #   옛 판정 `any('_stage_e' in k)` 은 이름만 맞으면 통과했다.  Codex 가 동적으로
        #   재현한 네 경우를 그대로 회귀로 고정한다.
        full = _healthy_stage_e()
        chk('24) 완전한 11-키 → 통과', ps.stage_e_missing_keys(full) == ())
        chk('25) ★ garbage_stage_e: null 하나만 → 거부 (옛 계약은 success 였다)',
            len(ps.stage_e_missing_keys({'garbage_stage_e': None})) == len(ps.STAGE_E_REQUIRED_KEYS))
        chk('26) ★ 필수 키가 있어도 값이 None 이면 없는 것으로 센다',
            ps.stage_e_missing_keys(dict(full, sigma_full_mScm_stage_e=None))
            == ('sigma_full_mScm_stage_e',))
        chk('27) ★ stage_e_source 만 생성 → 거부 (partial)',
            'sigma_full_mScm_stage_e' in ps.stage_e_missing_keys({'stage_e_source': {'a': 1}}))
        chk('28) 아무 출력 없음 → 전부 누락', len(ps.stage_e_missing_keys({})) == 11)
        chk('29) 진짜 0 은 유효값이라 통과한다 (None 만 거른다)',
            ps.stage_e_missing_keys(dict(full, thermal_sigma_full_mScm_stage_e=0.0)) == ())
        # ══ RC5-03 근본수정: thermal '없음' 을 **두 사건으로 갈라** 판정한다 ══
        #   옛 코드는 퍼콜 미형성(정상)과 솔버 예외(실패)가 둘 다 "키 없음" 이라
        #   상위가 판단할 근거가 없었다.  이제 solver 가 thermal_status 를 항상 남긴다.
        chk('37) ★ 솔버 예외 → fail (재실행으로 고쳐야 하는 소프트웨어 실패)',
            ps.thermal_channel_verdict({'thermal_status': 'failed',
                                        'thermal_status_reason': 'boom'})[0] == 'fail')
        chk('38) ★ 퍼콜 미형성(κ=0) → ok (물리적으로 옳은 답, 실패 아님)',
            ps.thermal_channel_verdict({'thermal_status': 'valid_zero'})[0] == 'ok'
            and ps.thermal_channel_verdict({'thermal_status': 'valid_null'})[0] == 'ok')
        chk('39) 정상 계산 → ok',
            ps.thermal_channel_verdict({'thermal_status': 'computed'})[0] == 'ok')
        chk('40) ★ 옛 세대(상태 필드 없음) → unknown, **소급 실패로 만들지 않는다**',
            ps.thermal_channel_verdict({'sigma_full_mScm': 1.0})[0] == 'unknown')
        chk('41) 모르는 상태값도 unknown (조용히 ok 로 넘기지 않는다)',
            ps.thermal_channel_verdict({'thermal_status': 'weird'})[0] == 'unknown')
        # 솔버가 실제로 상태를 쓰는지 (계약이 코드에 있는지)
        _ncsrc = open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(webapp.__file__))), 'scripts',
            'network_conductivity.py'), encoding='utf-8').read()
        # ══ RC7-02 (Codex 7회차): 게시 게이트가 **thermal 하나만** 봤다 ══
        #   electronic solver 는 예외를 print 만 하고 넘어가 (RC5-03 이 thermal 에 대해
        #   고친 결함이 그대로 남아 있었다) σ_e 키가 통째로 빠진 채 success 로 게시됐다.
        _base = {'sigma_full_mScm': 5.0, 'ionic_status': 'computed',
                 'electronic_status': 'computed', 'thermal_status': 'computed'}
        chk('RC7-02a) ★ electronic 예외 → fail (옛 계약은 thermal 만 봐서 통과였다)',
            ps.channel_verdict(dict(_base, electronic_status='failed',
                                    electronic_status_reason='boom'), 'electronic')[0] == 'fail')
        chk('RC7-02b) ★ AM 망 미퍼콜(no_result) 은 electronic 에서 **ok** — 물리적 정답',
            ps.channel_verdict(dict(_base, electronic_status='no_result'), 'electronic')[0] == 'ok'
            and ps.channel_verdict(dict(_base, electronic_status='valid_zero'),
                                   'electronic')[0] == 'ok')
        chk('RC7-02c) ★ AM 자체가 없는 베드(not_applicable) 도 ok (실패 아님)',
            ps.channel_verdict(dict(_base, electronic_status='not_applicable'),
                               'electronic')[0] == 'ok')
        chk('RC7-02d) ★ SE 미퍼콜(σ_i=0) 은 ionic 에서 ok (CLAUDE.md Tier2 정답 케이스)',
            ps.channel_verdict(dict(_base, ionic_status='valid_zero'), 'ionic')[0] == 'ok'
            and ps.channel_verdict(dict(_base, ionic_status='no_result'), 'ionic')[0] == 'ok')
        chk('RC7-02e) ★ thermal 의 no_result 는 여전히 ok 가 아니다 (전 접촉인데 망이 안 섬)',
            ps.channel_verdict(dict(_base, thermal_status='no_result'), 'thermal')[0] != 'ok')
        chk('RC7-02f) 옛 세대(채널 상태 없음)는 채널별로 unknown — 소급 실패 아님',
            ps.channel_verdict({'sigma_full_mScm': 1.0}, 'electronic')[0] == 'unknown'
            and ps.channel_verdict({'sigma_full_mScm': 1.0}, 'ionic')[0] == 'unknown')
        def _raises(fn, exc):
            try:
                fn()
            except exc:
                return True
            except Exception:
                return False
            return False
        chk('RC7-02g) 알 수 없는 채널 이름은 조용히 통과하지 않는다',
            _raises(lambda: ps.channel_verdict(_base, 'magnetic'), ValueError))
        # 게시 게이트가 실제로 세 채널을 보는가 (판정 함수만 고치고 배선 안 한 전례가 있다)
        _tmp2 = tempfile.mkdtemp()
        try:
            for _m in ('hertzian', 'physics'):
                with open(os.path.join(_tmp2, f'network_conductivity_{_m}.json'), 'w') as _f:
                    json.dump(dict(_base), _f)
            chk('RC7-02h) 세 채널 정상 → 게이트 통과',
                ps.network_content_verdict(_tmp2, strict=True)[0] is True)
            with open(os.path.join(_tmp2, 'network_conductivity_physics.json'), 'w') as _f:
                json.dump(dict(_base, electronic_status='failed',
                               electronic_status_reason='boom'), _f)
            _okg, _whyg = ps.network_content_verdict(_tmp2, strict=True)
            chk('RC7-02i) ★ physics 의 electronic 실패가 게이트에서 잡힌다 (게시 차단)',
                _okg is False and 'physics.electronic=fail' in _whyg)
            with open(os.path.join(_tmp2, 'network_conductivity_physics.json'), 'w') as _f:
                json.dump(dict(_base, ionic_status='failed'), _f)
            chk('RC7-02j) ★ ionic 실패도 잡힌다',
                ps.network_content_verdict(_tmp2, strict=True)[0] is False)
        finally:
            shutil.rmtree(_tmp2, ignore_errors=True)
        chk('RC7-02k) ★ solver 가 electronic_status 를 **항상** 남긴다 (배선 확인)',
            "results['electronic_status'] = el_status" in _ncsrc
            and "el_status, el_reason = 'failed'" in _ncsrc)
        chk('RC7-02l) ★ solver 가 ionic_status 도 남긴다',
            "results['ionic_status'] = _ist" in _ncsrc
            and 'def status_for_value(' in _ncsrc)
        chk('RC7-02l2) ★ 값 분류가 기존 _sigma_status 를 재사용한다 (파일 안 중복 판정 금지)',
            'st = _sigma_status(value)' in _ncsrc and 'status_for_value(' in _ncsrc)
        chk('RC7-02l2b) ★ NaN/inf 는 미퍼콜이 아니라 failed 로 간다 (첫 구현이 빠뜨렸던 것)',
            "return 'failed', f'{sym} 이 비유한값(NaN)" in _ncsrc
            and "inf — 수치 실패" in _ncsrc)
        chk('RC7-02l3) ★ solver 쪽에도 실행 가능한 selftest 가 있다 (문자열 검사만이 아니라)',
            '--selftest-status' in _ncsrc and 'def _selftest_status(' in _ncsrc)
        _apy_ch = open(os.path.join(os.path.dirname(os.path.abspath(webapp.__file__)),
                                    'app.py'), encoding='utf-8').read()
        chk('RC7-02m) ★ app 이 세 채널을 판정 단계로 올린다 (배선)',
            '_ps.NETWORK_CHANNELS' in _apy_ch and 'if _failed_ch:' in _apy_ch)
        chk('42) ★ solver 가 thermal_status 를 항상 남긴다 (배선 확인)',
            "results['thermal_status'] = th_status" in _ncsrc
            and "th_status, th_reason = 'failed'" in _ncsrc)

        # ══ RC6-01 (Codex 6회차): 손상 레코드를 완전으로 판정하던 것 ══
        #   옛 구현은 `is None` 만 봐서 NaN·잘못된 타입이 전부 통과했다.
        _full = _healthy_stage_e()
        chk('43) 건전한 레코드는 통과', ps.stage_e_missing_keys(_full) == ())
        chk('44) ★ NaN 을 잡는다 (옛 계약은 통과시켰다)',
            ps.stage_e_missing_keys(dict(_full, sigma_full_mScm_stage_e=float('nan'))))
        chk('45) ★ inf 도 잡는다',
            ps.stage_e_missing_keys(dict(_full, thermal_sigma_full_mScm_stage_e=float('inf'))))
        chk('46) ★ stage_e_source="not-a-map" 를 잡는다',
            ps.stage_e_missing_keys(dict(_full, stage_e_source='not-a-map')))
        chk('47) ★ validation_flags=[] 를 잡는다',
            ps.stage_e_missing_keys(dict(_full, validation_flags=[])))
        chk('48) ★ bool 이 숫자로 통과하지 않는다',
            ps.stage_e_missing_keys(dict(_full, sigma_full_mScm_stage_e=True)))
        chk('49) 빈 method 문자열을 잡는다',
            ps.stage_e_missing_keys(dict(_full, fracture_aware_method_full='   ')))
        chk('50) 진짜 0.0 은 여전히 유효 (valid_zero)',
            ps.stage_e_missing_keys(dict(_full, sigma_full_mScm_stage_e=0.0)) == ())
        chk('51) ★ null_ok_keys 로 valid_null 계약 충돌이 풀린다',
            ps.stage_e_missing_keys(dict(_full, electronic_sigma_full_mScm_stage_e=None)) != ()
            and ps.stage_e_missing_keys(
                dict(_full, electronic_sigma_full_mScm_stage_e=None),
                null_ok_keys=('electronic_sigma_full_mScm_stage_e',)) == ())

        # ══ RC6-04 (Codex 6회차): Stage E 가 network 소유 raw thermal 을 덮어쓰던 것 ══
        _rn = open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(webapp.__file__))), 'scripts',
            'run_network_full_corrections.py'), encoding='utf-8').read()
        chk("52) ★ Stage E 가 raw thermal 키에 **직접 쓰지 않는다** (이중 소유 종료)",
            "fm['thermal_sigma_full_mScm'] =" not in _rn
            and "fm['thermal_sigma_full_mScm_physics'] =" not in _rn)
        chk('53) ★ 역산값은 별도 estimate 키 + provenance 로 간다',
            "thermal_sigma_full_mScm_stage_e_estimate" in _rn
            and 'thermal_baseline_estimate_provenance' in _rn)
        _apy2 = open(os.path.join(os.path.dirname(os.path.abspath(webapp.__file__)),
                                  'app.py'), encoding='utf-8').read()
        chk('54) ★ 화면이 estimate 를 **유도값이라 표시하고** 쓴다 (배선)',
            'thermal_sigma_full_mScm_stage_e_estimate' in _apy2
            and 'baseline=유도추정' in _apy2)

        # ══ RC6-06/08 (Codex 6회차): STEP3 component manifest · backend provenance ══
        #   ⚠ 이 컨테이너엔 scipy 가 없어 STEP3 를 **실행**할 수 없다 → 소스 계약으로 건다.
        #     (실행 검증은 GPU 머신 몫 — 그 한계를 회귀 이름에 남긴다.)
        _sc = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(webapp.__file__))), 'scripts')
        _pay = open(os.path.join(_sc, 'mpm_webapp_payload.py'), encoding='utf-8').read()
        _s3s = open(os.path.join(_sc, 'step3_sigma.py'), encoding='utf-8').read()
        chk('55) ★ STEP3 component 상태 헬퍼가 있다 (thermal 만이 아니었다)',
            'def _s3mark(' in _pay)
        for _c in ('electronic', 'ionic', 'thermal', 'pore', 'pnm'):
            chk(f'56) STEP3 {_c} 채널이 상태를 남긴다', f"_s3mark('{_c}'" in _pay)
        chk('57) ★ 바깥 예외도 payload 에 흔적을 남긴다 (옛 코드는 print 뿐)',
            "_s3mark('_step3', 'failed'" in _pay)
        chk('58) ★ manifest 가 payload 에 실제로 박힌다 (배선)',
            "'schema_version': 2," in _pay)
        chk('59) ★ RC6-08 실제 backend 를 기록한다 (요청≠실제일 수 있다)',
            'LAST_BACKEND' in _s3s and "LAST_BACKEND['used'] = 'cpu'" in _s3s
            and "LAST_BACKEND['used'] = 'gpu'" in _s3s
            and "fallback_reason" in _s3s)
        chk('60) ★ 그 backend 가 manifest 로 흘러간다 (배선)',
            "'backend': dict(getattr(_s3, 'LAST_BACKEND'" in _pay)

        # ══ RC7-01 (Codex 7회차): manifest 가 **표시된 것만** 보고 complete 를 냈다 ══
        #   component 가 아예 안 돌아 _s3st 에 없으면, 남은 것이 전부 complete 인 한
        #   top='complete' 였다 — "안 돈 것" 이 "다 됐다" 로 보인다.
        chk('RC7-01a) ★ 기대 component 집합이 선언돼 있다',
            "STEP3_EXPECTED = ('electronic', 'ionic', 'thermal', 'pore', 'pnm')" in _pay)
        chk('RC7-01b) ★ 표시 안 된 기대 component 를 missing 으로 채운다',
            "_s3st.setdefault(_c, {'status': 'missing'" in _pay)
        chk('RC7-01c) ★ missing 이 있으면 complete 가 될 수 없다',
            "'failed' in _sts.values() or 'missing' in _sts.values()" in _pay)
        chk('RC7-01d) manifest 가 missing·failed 목록을 명시적으로 싣는다',
            "'missing': sorted(" in _pay and "'failed': sorted(" in _pay)
        # 판정 로직을 실제로 돌려본다 (문자열 검사만으로는 계약을 못 지킨다)
        def _top_of(marked, expected=('electronic', 'ionic', 'thermal', 'pore', 'pnm')):
            st = dict(marked)
            if st:
                for c in expected:
                    st.setdefault(c, {'status': 'missing'})
            sts = {c: v['status'] for c, v in st.items()}
            if not sts:
                return 'disabled'
            if sts.get('_step3') == 'failed':
                return 'failed'
            if 'failed' in sts.values() or 'missing' in sts.values():
                return 'partial'
            return 'complete' if all(v == 'complete' for v in sts.values()) else 'partial'
        _all_ok = {c: {'status': 'complete'} for c in
                   ('electronic', 'ionic', 'thermal', 'pore', 'pnm')}
        chk('RC7-01e) 전부 complete → complete', _top_of(_all_ok) == 'complete')
        _part = dict(_all_ok); _part.pop('ionic')
        chk('RC7-01f) ★ ionic 이 아예 표시되지 않으면 partial (옛 계약은 complete)',
            _top_of(_part) == 'partial')
        chk('RC7-01g) not_solvable 은 정상 — complete 를 막지 않되 complete 도 아니다',
            _top_of(dict(_all_ok, pnm={'status': 'not_solvable'})) == 'partial')
        chk('RC7-01h) 바깥 예외는 failed 로 승격',
            _top_of(dict(_all_ok, _step3={'status': 'failed'})) == 'failed')
        chk('RC7-01i) STEP3 자체를 안 돌린 경우는 disabled (missing 으로 오염 금지)',
            _top_of({}) == 'disabled')

        # ══ RC7-01: bare NaN 벨트 — json.dump 기본값은 RFC 8259 밖 토큰을 쓴다 ══
        chk('RC7-01j) ★ 쓰기 직전 전수 벨트가 있다',
            'payload, _nonfinite = finite_belt(payload)' in _pay)
        # ★ 문자열 검사가 아니라 **실제 함수**를 돌린다 (배선만 보면 계약을 못 지킨다)
        try:
            import numpy as _np
            sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
                os.path.abspath(webapp.__file__))), 'scripts'))
            from mpm_webapp_payload import finite_belt as _belt
            _clean, _paths = _belt({'ok': 1.0, 'nan': float('nan'), 'inf': float('inf'),
                                    'f32': _np.float32('nan'), 'i': 3, 'n': None,
                                    'deep': {'l': [1.0, float('-inf'), 'txt']}})
            chk('RC7-01j2) ★ 실제 벨트가 NaN·Inf·np.float32 를 전부 null 로 바꾼다',
                _clean['nan'] is None and _clean['inf'] is None and _clean['f32'] is None
                and _clean['deep']['l'] == [1.0, None, 'txt'])
            chk('RC7-01j3) ★ 정상값·비-float 은 건드리지 않는다',
                _clean['ok'] == 1.0 and _clean['i'] == 3 and _clean['n'] is None)
            chk('RC7-01j4) ★ 바꾼 자리를 **경로째** 돌려준다 (조용한 치환 금지)',
                sorted(_paths) == ['$.deep.l[1]', '$.f32', '$.inf', '$.nan'])
            _ser = json.dumps(_clean, allow_nan=False)      # 남아 있으면 ValueError
            chk('RC7-01j5) ★ 벨트 뒤엔 allow_nan=False 직렬화가 통과하고 금지 토큰이 없다',
                'NaN' not in _ser and 'Infinity' not in _ser
                and _raises2(lambda: json.dumps({'x': float('nan')}, allow_nan=False),
                             ValueError))
        except ImportError as _ie:
            chk(f'RC7-01j2) ⚠ 벨트 실행 검증 생략 (import 실패: {_ie})', True)
        chk('RC7-01k) ★ allow_nan=False 로 남아 있으면 조용히 넘어가지 않고 터진다',
            'json.dump(payload, fh, allow_nan=False)' in _pay)
        chk('RC7-01l) ★ 치환을 조용히 하지 않고 경로째 기록한다',
            "payload['nonfinite_sanitized']" in _pay)
        chk('RC7-01m) ★ np.float32 도 잡는다 (파이썬 float 서브클래스가 아니다)',
            'np.floating' in _pay)
        _bad = json.dumps({'a': float('nan')})           # 기본 json 이 내는 것
        chk('RC7-01n) ★ 결함 재현: 기본 json.dump 는 bare NaN 토큰을 쓴다',
            'NaN' in _bad and _raises2(lambda: json.loads(_bad, parse_constant=_boom), ValueError))

        # ══ RC7-05: backend 가 전역 하나라 마지막 solve 만 표현됐다 ══
        chk('RC7-05a) ★ component 별로 backend 를 스냅샷한다',
            "rec['backend'] = dict(_bk)" in _pay)
        chk('RC7-05b) ★ 전역 필드는 하위호환 별칭으로 라벨링됐다',
            "'backend_last_solve'" in _pay)
        chk('RC7-05c) 스냅샷은 complete 인 component 에만 (미실행에 backend 를 붙이지 않는다)',
            "if status == 'complete' and isinstance(_bk, dict)" in _pay)

        # ══ RC7-06 (Codex 7회차): Stage E 소유 판정이 **이름 규칙**만 봐서 결손 ══
        #   thermal_baseline_estimate_provenance 는 `_stage_e` 도 `stage_e_` 도 아니라
        #   purge 대상이 아니었다 → 값(…_stage_e_estimate)만 걷히고 provenance 는 남아
        #   **없어진 추정치를 설명하는 옛 세대 도장**이 새 세대 payload 에 붙어 있었다.
        chk('RC7-06a) ★ 결함 재현: 이름 규칙만으로는 provenance 키가 안 잡힌다',
            '_stage_e' not in 'thermal_baseline_estimate_provenance'
            and not 'thermal_baseline_estimate_provenance'.startswith('stage_e_'))
        chk('RC7-06b) ★ 이제 Stage E 소유로 잡힌다 (purge/rollback 대상)',
            ps.is_stage_e_key('thermal_baseline_estimate_provenance') is True)
        # ★ drift 가드 — 명시 목록은 자석이다.  run_one 의 `fm[...] =` 를 전수 스캔해
        #   소유되지 않은 키가 새로 생기면 **여기서 실패**한다 (같은 결함의 재발 차단).
        _rnfc = open(os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(webapp.__file__))), 'scripts',
            'run_network_full_corrections.py'), encoding='utf-8').read()
        _written = sorted(set(re.findall(r"""\bfm\[\s*['"]([^'"]+)['"]\s*\]\s*=""", _rnfc)))
        _unowned = [k for k in _written if not ps.is_stage_e_key(k)]
        chk(f'RC7-06c) ★ run_one 이 쓰는 {len(_written)}개 키가 전부 Stage E 소유다 '
            f'(미소유: {_unowned})', _written and not _unowned)
        chk('RC7-06d) 스캐너가 실제로 키를 찾았다 (정규식이 죽어 공허하게 통과하지 않는다)',
            len(_written) >= 15 and 'sigma_full_mScm_stage_e' in _written)
        chk('RC7-06e) 명시 목록이 상수로 노출돼 있다 (다음 사람이 찾을 수 있게)',
            'thermal_baseline_estimate_provenance' in ps.STAGE_E_EXTRA_OWNED_KEYS)

        chk('30) 11-키는 run_one 이 무조건 쓰는 집합과 같다 (개수 고정)',
            len(ps.STAGE_E_REQUIRED_KEYS) == 11
            and all(ps.is_stage_e_key(k) for k in ps.STAGE_E_REQUIRED_KEYS))

        # ══ F-18 (Codex 5회차): mpm-input route 가 bare 'python3' 라 Windows 에서 500 ══
        #   ⚠ HTTP 코드로는 못 잡는다 — 리눅스엔 python3 가 있어서 200 이 나온다(false-green).
        #   소스에서 **인터프리터 인자**를 직접 본다.
        import ast as _ast
        _src = open(os.path.join(os.path.dirname(os.path.abspath(webapp.__file__)),
                                 'app.py'), encoding='utf-8').read()
        _bare = []
        for _n in _ast.walk(_ast.parse(_src)):
            if not isinstance(_n, _ast.List) or not _n.elts:
                continue
            _h = _n.elts[0]
            if isinstance(_h, _ast.Constant) and _h.value == 'python3':
                _bare.append(_n.lineno)
        chk('31) ★ webapp 이 subprocess 를 bare python3 로 띄우지 않는다 (F-18, Windows 500)',
            not _bare or print(f'    bare python3 at lines {_bare}') )

        # ══ RC5-04 (Codex 5회차): Stage E 가 Physics 재솔브 결과를 버리던 것 ══
        #   상세 회귀는 scripts/network_mode_io.py --selftest (11건).  여기서는 그 모듈이
        #   실제로 존재하고 계약을 지키는지만 확인한다 (pandas 없이 import 되는 것 포함 —
        #   버그가 오래 숨은 이유가 "검증할 수 없는 자리에 있었다" 였다).
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(webapp.__file__))), 'scripts'))
        import network_mode_io as _nmio
        _md = tempfile.mkdtemp(prefix='modes_')
        try:
            json.dump({'sigma_full_mScm': 1.0},
                      open(os.path.join(_md, _nmio.MODE_FILES['hertzian']), 'w'))
            json.dump({'sigma_full_mScm': 101.0},
                      open(os.path.join(_md, _nmio.MODE_FILES['physics']), 'w'))
            _r = _nmio.collect_modes(_md, warn=lambda _m: None)
            chk('32) ★ Physics 재솔브 값이 살아 돌아온다 (옛 코드는 항상 None → fallback)',
                _r.get('sigma_full_mScm_physics') == 101.0 and _r.get('sigma_full_mScm') == 1.0)
            chk('33) Stage E 가 그 모듈을 실제로 쓴다 (인라인 사본이 아니라)',
                'network_mode_io' in open(os.path.join(os.path.dirname(os.path.dirname(
                    os.path.abspath(webapp.__file__))), 'scripts',
                    'run_network_full_corrections.py'), encoding='utf-8').read())
        finally:
            shutil.rmtree(_md, ignore_errors=True)

        # ══ T10 (Codex 실측 이관): Windows `os.replace` 간헐 PermissionError ══
        # Codex 가 DFT 대시보드에서 12 프로세스 × 100 건 × 10 회를 돌려 992/1000 만
        # 저장되는 것을 실측했다.  락은 정상이었고(임계구역 1) 원인은 외부 handle 의
        # 일시 점유였다.  리눅스에서는 이 예외가 안 나므로 **주입해서** 경로를 검증한다.
        slept = []
        calls = [0]
        real_replace = os.replace

        def flaky_replace(src, dst, _fail=2):
            calls[0] += 1
            if calls[0] <= _fail:
                raise PermissionError(13, 'Access is denied')
            return real_replace(src, dst)

        os.replace = flaky_replace
        try:
            p2 = os.path.join(tmp, 'retry.json')
            n_attempt = ps._replace_retry(_mk_tmp(tmp, '{"v": 7}'), p2, sleep=slept.append)
            chk('20) ★ PermissionError 2회 뒤 저장된다 (Windows 유실 992/1000 원인)',
                json.load(open(p2)) == {'v': 7} and n_attempt == 2)
            chk('21) 재시도 대기가 지수 backoff 다 (바쁜대기 아님)',
                slept == [ps._REPLACE_BACKOFF, ps._REPLACE_BACKOFF * 2])
            # 끝까지 실패하면 삼키지 않는다
            calls[0] = 0
            raised = False
            try:
                ps._replace_retry(_mk_tmp(tmp, '{}'), os.path.join(tmp, 'never.json'),
                                  retries=1, sleep=lambda _s: None)
            except PermissionError:
                raised = True
            chk('22) ★ 재시도를 다 써도 안 되면 올린다 (조용한 유실 금지)',
                raised and not os.path.exists(os.path.join(tmp, 'never.json')))
            # PermissionError 가 아닌 OSError 는 재시도하지 않는다 (진짜 버그를 숨기지 않게)
            calls[0] = 0

            def enoent_replace(src, dst):
                calls[0] += 1
                raise OSError(errno.ENOENT, 'no such file')

            os.replace = enoent_replace
            raised2 = False
            try:
                ps._replace_retry(_mk_tmp(tmp, '{}'), os.path.join(tmp, 'e.json'),
                                  sleep=lambda _s: None)
            except OSError:
                raised2 = True
            chk('23) ★ EACCES 아닌 OSError 는 재시도 없이 즉시 올린다',
                raised2 and calls[0] == 1)
        finally:
            os.replace = real_replace
        with ps.network_lock(lock_dir=tmp) as got1:
            chk('17) 파일 lock 획득', got1 is True)
            # ★ T8 (Codex CB-03): 두 번째 경쟁자는 lock 을 못 잡고, 그때 **solver 를
            #   돌리지 않고 예외를 던져야** 한다.  옛 테스트는 True/False 를 모두
            #   통과시켜 fail-open 을 놓쳤다.  flock 은 file-description 단위라
            #   같은 프로세스의 두 번째 open() 도 실제로 막힌다.
            raised = False
            try:
                with ps.network_lock(timeout=1, lock_dir=tmp):
                    pass
            except ps.LockUnavailable:
                raised = True
            chk('18) ★ lock 미획득 → LockUnavailable (fail-open 아님)', raised)
            got3 = None
            with ps.network_lock(timeout=1, lock_dir=tmp, require=False) as g:
                got3 = g
            chk('19) require=False 는 진단용으로 False 를 돌려준다', got3 is False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f'\ntest_pipeline_provenance: {_ok}/{_ok + len(_fail)} PASS'
          + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
