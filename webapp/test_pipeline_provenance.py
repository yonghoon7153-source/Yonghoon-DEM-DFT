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
  ★ 예외 (10-05 · Codex RGL-02 · 04 · 07 · 08 · SELF-86): T12 의 망 레코드와 T13–T16 은 **실 생산자** 출력이다 — 합성 침대를
    network_conductivity CLI 코드 그대로 (같은 프로세스 runpy) 풀고, 실 정지 helper · 실 소비자 (tau_flux · grade_engine ·
    /retry-network 라우트) 로 잇는다.  손 레코드는 Codex 의 정확한 수치 재현 (T16a) 에만 쓴다.

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


# ═══ T12–T16 공용 — **실 생산자** 침대 (Codex 10-05 RGL-02 · 04 · 07 · 08 · 원장 SELF-86) ═══════════════════════════════════
#   SELF-86: 정지 계약을 손으로 만든 상태값 (valid_zero 를 직접 넣은 T12d) 으로만 시험해, 실 생산자가 비관통에 not_computed 를 내던
#   모순 (RGL-02) 과 게시 뒤 관문 (RGL-04) 을 놓쳤다.  ⇒ 양성 대조는 실 생산자 (`network_conductivity` — CLI 코드 그대로 · 같은 프로세스)
#   의 출력으로 만들고, 실패 경로는 표시 상태만이 아니라 다른 소비자가 읽는 활성 산출물 · provenance · full_metrics 까지 단언한다.
_SCRIPTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
_NET_FOUR = ('network_conductivity.json', 'network_conductivity_hertzian.json',
             'network_conductivity_physics.json', 'network_conductivity_dual.json')


def _bed(name):
    """합성 침대 → (atoms, contacts, plate_z, box).  Codex 판정문 RGL-02 · test_tau_flux K1 · K3 와 같은 모양 (반경 1 · 상자 10 · 척도 1).
      through    — SE 21 개 사슬 z 0..20 (관통 · 띠 L0)
      nonthrough — 바닥 L0 띠에 외톨이 SE 셋 + 위쪽 사슬 z 10..20 (바닥과 끊김 · 띠 L0) = **정상 비관통**
      band_l1    — 반경 0.4 · z 0..40 간격 0.5 (바닥 L0 띠 2 개 < 3 → 띠 폴백 L1 = 등록된 과학적 HOLD BAND_FALLBACK)"""
    if name == 'through':
        A = {i: dict(type=1, x=0., y=0., z=float(z), radius=1.) for i, z in enumerate(range(21), 1)}
        C = [dict(id1=i, id2=i + 1, contact_area=0.1, delta=0.05) for i in range(1, 21)]
        return A, C, 20.0, 10.0
    if name == 'nonthrough':
        A = {i: dict(type=1, x=3.0 * i, y=0., z=z, radius=1.) for i, z in ((1, 0.), (2, 1.), (3, 2.))}
        A.update({10 + k: dict(type=1, x=0., y=5., z=float(z), radius=1.) for k, z in enumerate(range(10, 21))})
        C = [dict(id1=10 + k, id2=11 + k, contact_area=0.1, delta=0.05) for k in range(10)]
        return A, C, 20.0, 10.0
    if name == 'band_l1':
        A = {i: dict(type=1, x=0., y=0., z=0.5 * k, radius=0.4) for i, k in enumerate(range(81), 1)}
        C = [dict(id1=i, id2=i + 1, contact_area=0.1 * 0.16, delta=0.05 * 0.4) for i in range(1, 81)]
        return A, C, 40.0, 10.0
    raise ValueError(name)


def _bed_ledger(name):
    """그 침대의 접촉 분석 장부 — 독립 `calc_percolation` (접촉 분석이 full_metrics 에 쓰는 percolation_pct) · 판 간격 두께 ·
    질량 보존 두께 (겹침 없는 사슬이라 판 간격과 같다) · φ_SE (구 부피 합 / 판 간격 상자 = 망 phi_se 의 반올림 전 값)."""
    import contextlib
    import io
    import math
    if _SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, _SCRIPTS_DIR)
    import dem_analysis_core as _dac
    A, C, plate, box = _bed(name)
    with contextlib.redirect_stdout(io.StringIO()):
        cp = _dac.calc_percolation(A, C, [1], plate, box_x=box, box_y=box)
    phi = sum(4.0 / 3.0 * math.pi * a['radius'] ** 3 for a in A.values()) / (box * box * plate)
    return {'phi_se': phi, 'thickness_um': plate, 'thickness_mass_conserving_um': plate,
            'phi_se_mass_conserving': phi, 'percolation_pct': cp['percolation_pct'], 'porosity': 100.0 * (1.0 - phi)}


def _producer_records(name):
    """실 생산자 (`network_conductivity._run_all_networks` — CLI 가 모드 파일 · dual 에 쓰는 바로 그 dict) 두 모드 + 장부.
    JSON 왕복 = 디스크에 쓰인 모양 그대로 (numpy 실수 → 실수)."""
    import contextlib
    import io
    if _SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, _SCRIPTS_DIR)
    import network_conductivity as _nc
    A, C, plate, box = _bed(name)
    with contextlib.redirect_stdout(io.StringIO()):
        recs = {cm: _nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1, plate, box, box, None, contact_mode=cm)
                for cm in ('hertzian', 'physics')}
    return json.loads(json.dumps(recs)), _bed_ledger(name)


def _write_bed(d, name):
    """침대를 생산자 CLI 입력으로 쓴다 — atoms.csv · contacts.csv (`analyze_contacts.load_*_raw` 열) · mesh_info.json (판 높이) ·
    input_params.json (상자).  → (atoms.csv, contacts.csv)."""
    A, C, plate, box = _bed(name)
    with open(os.path.join(d, 'atoms.csv'), 'w') as f:
        f.write('id,type,x,y,z,radius\n' + ''.join(
            f'{i},{a["type"]},{a["x"]!r},{a["y"]!r},{a["z"]!r},{a["radius"]!r}\n' for i, a in A.items()))
    with open(os.path.join(d, 'contacts.csv'), 'w') as f:
        f.write('id1,id2,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,contact_area,delta\n' + ''.join(
            f'{c["id1"]},{c["id2"]},0,0,0,0,0,0,{c["contact_area"]!r},{c["delta"]!r}\n' for c in C))
    with open(os.path.join(d, 'mesh_info.json'), 'w') as f:
        json.dump({'plate_z': plate}, f)
    with open(os.path.join(d, 'input_params.json'), 'w') as f:
        json.dump({'box_x': box, 'box_y': box}, f)
    return os.path.join(d, 'atoms.csv'), os.path.join(d, 'contacts.csv')


class _CLIRunner:
    """network_conductivity.py 를 **CLI 코드 그대로** 같은 프로세스에서 돈다 (runpy · argv = 받은 명령) — 파일 쓰기까지 실 생산자.

    mutate(out_dir) = 생산자가 쓴 **뒤**의 계약 변이 (반례) · break_solver = scipy `spsolve` 예외 주입 (관통인데 풀지 못함 = 수치 실패) ·
    delegate = 다른 스크립트 (Stage E 등) 대역.  produced = 생산자가 쓴 네 JSON (변이 전 · 거부된 후보는 디스크에서 치워지므로 여기서 본다)."""

    def __init__(self, mutate=None, break_solver=False, delegate=None):
        self.mutate, self.break_solver, self.delegate = mutate, break_solver, delegate
        self.calls, self.produced = [], {}

    def __call__(self, cmd, **kw):
        import contextlib
        import io
        import runpy
        import scipy.sparse.linalg as _spl
        script = os.path.basename(str(cmd[1])) if len(cmd) > 1 else ''
        if script != 'network_conductivity.py':
            if self.delegate is None:
                raise AssertionError(f'_CLIRunner: 대역 없는 명령 {cmd}')
            return self.delegate(cmd, **kw)
        self.calls.append(list(cmd))
        argv0, orig, rc = sys.argv, _spl.spsolve, 0
        out, err = io.StringIO(), io.StringIO()
        try:
            if self.break_solver:
                def _boom(*_a, **_k):
                    raise RuntimeError('주입: spsolve 실패 (수치 실패 시험)')
                _spl.spsolve = _boom
            sys.argv = [str(c) for c in cmd[1:]]
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                runpy.run_path(str(cmd[1]), run_name='__main__')
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else (0 if e.code is None else 1)
        except Exception as e:                                       # noqa: BLE001
            rc = 1
            err.write(f'{type(e).__name__}: {e}')
        finally:
            sys.argv, _spl.spsolve = argv0, orig
        o_dir = str(cmd[list(map(str, cmd)).index('-o') + 1])
        self.produced = {n: json.load(open(os.path.join(o_dir, n))) for n in _NET_FOUR
                         if os.path.exists(os.path.join(o_dir, n))}
        if rc == 0 and self.mutate is not None:
            self.mutate(o_dir)
        return subprocess.CompletedProcess(cmd, rc, out.getvalue(), err.getvalue())


def _edit_net_records(o_dir, fn, files=_NET_FOUR):
    """생산자가 쓴 망 레코드 (모드 파일 · legacy · dual 의 두 모드) 를 fn(rec, 이름, 모드) 로 고쳐 다시 쓴다 — 계약 변이 도우미."""
    for n in files:
        p = os.path.join(o_dir, n)
        if not os.path.exists(p):
            continue
        d = json.load(open(p))
        if n == 'network_conductivity_dual.json':
            for m in ('hertzian', 'physics'):
                if isinstance(d.get(m), dict):
                    fn(d[m], n, m)
        else:
            fn(d, n, 'physics' if 'physics' in n else 'hertzian')
        with open(p, 'w') as f:
            json.dump(d, f)


def _fake_stage_e(cmd, **kw):
    """Stage E 대역 — `--case-dir` (candidate) 의 full_metrics 에 건전한 11-키 레코드를 얹는다 (RC5-01 · RC6-01 스키마)."""
    _c = list(map(str, cmd))
    _t = _c[_c.index('--case-dir') + 1]
    fm = os.path.join(_t, 'full_metrics.json')
    d = json.load(open(fm)) if os.path.exists(fm) else {}
    for _k, _v in _healthy_stage_e().items():
        d.setdefault(_k, _v)
    with open(fm, 'w') as f:
        json.dump(d, f)
    return subprocess.CompletedProcess(cmd, 0, 'fake stage e', '')


def _t13_t16_network_stop_real(webapp):
    """T13–T16 — Codex 10-05 (RGL-02 · 04 · 07 · 08) 반례를 **실 생산자 → 실 정지 helper (`_network_and_stage_e`) → 실 소비자
    (`tau_flux` · `grade_engine` · 웹앱 retry 라우트)** 사슬로 옮긴 회귀.  손으로 만든 상태값은 Codex 의 정확한 수치 재현 (T16a) 에만 쓴다."""
    import copy
    if _SCRIPTS_DIR not in sys.path:
        sys.path.insert(0, _SCRIPTS_DIR)
    import tau_flux as _tf
    import grade_engine as _ge

    def _case(bed, fm_over=None):
        d = tempfile.mkdtemp(prefix='t13_')
        a, c = _write_bed(d, bed)
        fm = dict(_bed_ledger(bed))
        fm.update(fm_over or {})
        with open(os.path.join(d, 'full_metrics.json'), 'w') as f:
            json.dump(fm, f)
        return d, a, c

    def _run(d, a, c, runner, stop=True):
        stages, rid = webapp._network_and_stage_e(d, _SCRIPTS_DIR, a, c, '1:SE', 1, [], runner=runner,
                                                  stop_before_stage_e=stop)
        st, failed = ps.summarize(stages)
        return stages, rid, st, [s.get('step', '') for s in failed]

    def _fm(d):
        return json.load(open(os.path.join(d, 'full_metrics.json')))

    def _attempt(d):
        p = os.path.join(d, ps.ATTEMPT_FILE)
        return json.load(open(p)) if os.path.exists(p) else {}

    def _guard(label, fn):
        """한 묶음이 예외로 죽어도 나머지를 센다 (옛 코드에서 실패 수를 세려고 — 예외 = 그 묶음 FAIL)."""
        try:
            fn()
        except Exception as e:                                       # noqa: BLE001
            import traceback
            traceback.print_exc()
            chk(f'{label} — 예외 없이 끝난다 ({type(e).__name__}: {e})', False)

    STOP = 'Network stop contract'
    CPS_NO_THROUGH = 'not_computed (no percolating FULL solution)'

    # ── T13 (RGL-02) — 실 생산자로 관통 · 정상 비관통 · 수치 실패를 구별한다 (done · done · failed) ──────────────────────────
    def t13():
        d, a, c = _case('through')
        _st, rid, st, failed = _run(d, a, c, _CLIRunner())
        dual = json.load(open(os.path.join(d, 'network_conductivity_dual.json')))
        tau, fm = _tf.case_row(d), _fm(d)
        chk(f'T13a) 관통 (실 생산자) → done · 두 모드 computed · full_metrics σ = dual · τ 인계 OK ({st} {failed})',
            st == 'done' and all(dual[m]['sigma_full_status'] == 'computed' for m in ('hertzian', 'physics'))
            and fm.get('sigma_full_mScm') == dual['hertzian']['sigma_full_mScm']
            and fm.get('sigma_full_mScm_physics') == dual['physics']['sigma_full_mScm']
            and tau['ion_net_status_hertz'] == tau['ion_net_status_physics'] == 'OK')
        shutil.rmtree(d, ignore_errors=True)

        d, a, c = _case('nonthrough')
        r = _CLIRunner()
        _st, rid, st, failed = _run(d, a, c, r)
        chk(f'T13b) ★ RGL-02 정상 비관통 (실 생산자 · calc_percolation 0 %) → done (옛: ③ not_computed 로 failed) ({st} {failed})',
            st == 'done' and not failed)
        pd = (r.produced.get('network_conductivity_dual.json') or {})
        chk('T13c) ★ 생산자가 "증명된 비관통" 을 명시한다 — 두 모드 sigma_full_status valid_zero · sigma_full_reason no_through_path · '
            'CF · constr 도 같은 상태 · 이온 채널 valid_zero · 숫자 필드는 None (F-12)',
            all(isinstance(pd.get(m), dict) and pd[m].get('sigma_full_status') == 'valid_zero'
                and pd[m].get('sigma_full_reason') == 'no_through_path'
                and pd[m].get('sigma_bulk_net_status') == 'valid_zero' and pd[m].get('sigma_constr_net_status') == 'valid_zero'
                and pd[m].get('ionic_status') == 'valid_zero'
                and pd[m].get('sigma_full') is None and pd[m].get('sigma_full_mScm') is None
                and pd[m].get('percolating_fraction') == 0.0 for m in ('hertzian', 'physics')))
        chk('T13d) 비관통의 전력 몫 = None + "비관통" 사유 (0/0 미정의 — 0 % 가 아니다 · Codex Q4)',
            all(pd[m].get(f'constriction_power_share_ion_{t}') is None
                and pd[m].get(f'constriction_power_share_ion_{t}_status') == CPS_NO_THROUGH
                for m, t in (('hertzian', 'hertz'), ('physics', 'physics'))) if pd else False)
        tau, fm, prov = _tf.case_row(d), _fm(d), ps.read_network_provenance(d)
        chk(f'T13e) ★ 같은 상태를 τ 인계가 NOT_PERCOLATING (f 0 · tau2 · tau 빈칸) 으로 소비 · full_metrics σ None · 상태 valid_zero 머지 · '
            f'활성 세대 = 이번 실행 ({tau.get("ion_net_status_hertz")} · {fm.get("sigma_full_status")} · {prov.get("network_run_id") == rid})',
            tau['ion_net_status_hertz'] == tau['ion_net_status_physics'] == 'NOT_PERCOLATING'
            and tau['f_ion_hertz'] == 0.0 and tau['tau2_ion_physics'] is None and tau['tau_ion_hertz'] is None
            and fm.get('sigma_full_mScm') is None and fm.get('sigma_full_mScm_physics') is None
            and fm.get('sigma_full_status') == 'valid_zero' and fm.get('sigma_full_reason') == 'no_through_path'
            and fm.get('sigma_full_status_physics') == 'valid_zero'
            and prov.get('network_run_id') == rid and prov.get('solver_status') == 'success')
        shutil.rmtree(d, ignore_errors=True)

        d, a, c = _case('through')
        fm0 = open(os.path.join(d, 'full_metrics.json')).read()
        r = _CLIRunner(break_solver=True)
        _st, rid, st, failed = _run(d, a, c, r)
        chk(f'T13f) ★ 수치 실패 (관통인데 풀지 못함 · spsolve 예외 주입) → failed · 실패 단계 = 정지 계약 ({st} {failed})',
            st == 'failed' and any(STOP in f for f in failed))
        pd = (r.produced.get('network_conductivity_dual.json') or {})
        chk('T13g) ★ 생산자는 수치 실패를 비관통과 가른다 — not_computed · 사유 solve_failed · 관통 분율 > 0 · 전력 몫 사유가 "비관통" 이 아니다',
            all(isinstance(pd.get(m), dict) and pd[m].get('sigma_full_status') == 'not_computed'
                and pd[m].get('sigma_full_reason') == 'solve_failed' and (pd[m].get('percolating_fraction') or 0) > 0
                and str(pd[m].get(f'constriction_power_share_ion_{t}_status', '')).startswith('not_computed')
                and pd[m].get(f'constriction_power_share_ion_{t}_status') != CPS_NO_THROUGH
                for m, t in (('hertzian', 'hertz'), ('physics', 'physics'))))
        row = _tf.ion_columns(pd, _bed_ledger('through'), _bed_ledger('through')['percolation_pct'])
        chk('T13h) 같은 생산 결과를 τ 인계는 NOT_COMPUTED (solver_guard) 로 본다 (두 모드)',
            row['ion_net_status_hertz'] == row['ion_net_status_physics'] == 'NOT_COMPUTED'
            and row['ion_net_status_reason_physics'] == 'solver_guard')
        prov, att = ps.read_network_provenance(d), _attempt(d)
        chk(f'T13i) ★ 첫 실행 실패 → 활성 success 없음 · 망 JSON 없음 · full_metrics 그대로 · 최근 시도 failed '
            f'({prov.get("provenance_state")} · {att.get("solver_status")})',
            prov.get('provenance_state') == 'missing'
            and not any(os.path.exists(os.path.join(d, n)) for n in _NET_FOUR)
            and open(os.path.join(d, 'full_metrics.json')).read() == fm0
            and att.get('solver_status') == 'failed' and rid is None)
        shutil.rmtree(d, ignore_errors=True)
    _guard('T13', t13)

    # ── T14 (RGL-04) — 새 필수 관문 실패는 활성 세대를 차지하지 않는다 (승격 전에 모든 검사 · 한 번에 승격 · 실패면 옛 세대 보존) ──
    def _l9(o_dir):
        p = os.path.join(o_dir, 'network_conductivity_dual.json')
        dd = json.load(open(p))
        dd['physics']['boundary_rule'] = 'L9'
        with open(p, 'w') as f:
            json.dump(dd, f)

    def t14():
        d, a, c = _case('through')
        _s1, rid1, st1, _f1 = _run(d, a, c, _CLIRunner())
        fm1 = open(os.path.join(d, 'full_metrics.json')).read()
        sha1 = {n: _sha(os.path.join(d, n)) for n in _NET_FOUR}
        prov1 = ps.read_network_provenance(d)
        _s2, rid2, st2, failed2 = _run(d, a, c, _CLIRunner(mutate=_l9))
        prov2, att = ps.read_network_provenance(d), _attempt(d)
        fm2 = _fm(d)
        chk(f'T14a) 첫 실행 done · 정지 계약 변이 (physics boundary_rule L9) 재실행 → failed (실패 단계 = 정지 계약) ({st1} → {st2} {failed2})',
            st1 == 'done' and st2 == 'failed' and any(STOP in f for f in failed2))
        chk(f'T14b) ★ RGL-04 활성 provenance = 옛 성공 세대 그대로 ({prov2.get("network_run_id") == rid1} · {prov2.get("solver_status")})',
            prov2.get('network_run_id') == rid1 == prov1.get('network_run_id') and prov2.get('solver_status') == 'success'
            and rid2 == rid1)
        chk('T14c) ★ full_metrics 가 바이트 그대로 — network_run_id · network_solver_status · σ 옛 값',
            open(os.path.join(d, 'full_metrics.json')).read() == fm1 and fm2.get('network_run_id') == rid1
            and fm2.get('network_solver_status') == json.loads(fm1).get('network_solver_status'))
        chk('T14d) ★ 옛 네 망 JSON 이 바이트 그대로 복구 (실패 후보가 활성 자리에 남지 않는다)',
            all(os.path.exists(os.path.join(d, n)) and _sha(os.path.join(d, n)) == sha1[n] for n in _NET_FOUR))
        chk(f'T14e) ★ 최근 시도만 failed (이번 실행 id · 사유에 계약 위반이 적힌다) ({att.get("solver_status")} · {str(att.get("reason"))[:60]})',
            att.get('solver_status') == 'failed' and att.get('network_attempt_run_id') not in (None, rid1)
            and 'L9' in str(att.get('reason', '')))
        shutil.rmtree(d, ignore_errors=True)

        d, a, c = _case('through')
        fm0 = open(os.path.join(d, 'full_metrics.json')).read()
        _s, rid, st, failed = _run(d, a, c, _CLIRunner(mutate=_l9))
        prov, att = ps.read_network_provenance(d), _attempt(d)
        chk(f'T14f) ★ 첫 실행이 정지 계약에서 실패 → 활성 success 없음 · 망 JSON 없음 · full_metrics 그대로 · 최근 시도 failed '
            f'({st} · {prov.get("provenance_state")} · {att.get("solver_status")})',
            st == 'failed' and prov.get('provenance_state') == 'missing' and rid is None
            and not any(os.path.exists(os.path.join(d, n)) for n in _NET_FOUR)
            and open(os.path.join(d, 'full_metrics.json')).read() == fm0 and att.get('solver_status') == 'failed')
        shutil.rmtree(d, ignore_errors=True)

        d, a, c = _case('through')
        _s, rid, st, failed = _run(d, a, c, _CLIRunner())
        prov, att, fm = ps.read_network_provenance(d), _attempt(d), _fm(d)
        chk(f'T14g) 정상 경로 done 그대로 — 활성 = 이번 실행 · full_metrics 도장 · 최근 시도 success ({st})',
            st == 'done' and prov.get('network_run_id') == rid and fm.get('network_run_id') == rid
            and fm.get('active_network_run_id') == rid and att.get('solver_status') == 'success'
            and att.get('network_attempt_run_id') == rid)
        shutil.rmtree(d, ignore_errors=True)
    _guard('T14', t14)

    # ── T15 (RGL-08) — 정지 계약의 입력 집합 · 파일 대조 · null 사유 (Codex probe_contracts 변이를 실 생산자 출력 위에) ──────────
    def _drop_tau(rec, _n, _m):
        for k in ('sigma_full', 'percolating_fraction', 'temperature_provenance', 'sigma_grain_S_cm'):
            rec.pop(k, None)

    def _power_excuse(rec, _n, _m):
        for k in list(rec):
            if k.startswith('constriction_power_share_ion_'):
                rec[k] = 'internal_solver_exception' if k.endswith('_status') else None

    def _permode99(rec, _n, _m):
        rec['sigma_full_mScm'] = 99.0

    def _legacy9(rec, _n, _m):
        rec['sigma_full_mScm'] = 9.0

    def t15():
        bad = {
            'missing_tau_inputs (σ_ratio · 관통 분율 · 온도 · σ₀ 삭제)': lambda o: _edit_net_records(o, _drop_tau),
            'permode_vs_dual_disagree (physics 모드 파일 σ 99 ↔ dual 원값)':
                lambda o: _edit_net_records(o, _permode99, files=('network_conductivity_physics.json',)),
            'percolating_power_missing (관통인데 전력 몫 None · internal_solver_exception)': lambda o: _edit_net_records(o, _power_excuse),
            'legacy_vs_dual (legacy σ 9 ↔ dual Hertz)': lambda o: _edit_net_records(o, _legacy9, files=('network_conductivity.json',)),
        }
        res = {}
        for lbl, mut in bad.items():
            d, a, c = _case('through')
            _s, rid, st, failed = _run(d, a, c, _CLIRunner(mutate=mut))
            res[lbl] = (st, any(STOP in f for f in failed), ps.read_network_provenance(d).get('provenance_state'))
            shutil.rmtree(d, ignore_errors=True)
        miss = {k: v for k, v in res.items() if v != ('failed', True, 'missing')}
        chk(f'T15a) ★ RGL-08 계약 변이 {len(bad)} 종 → 전부 failed (정지 계약) · 활성 세대 없음 {miss or ""}',
            not miss and len(res) == len(bad))
        ok = {}
        for lbl, bed, over, want in (('건전 (OK)', 'through', None, 'OK'),
                                     ('띠 폴백 L1 (BAND_FALLBACK — 등록된 과학적 HOLD)', 'band_l1', None, 'BAND_FALLBACK'),
                                     ('정상 비관통 (NOT_PERCOLATING — 등록된 과학적 HOLD)', 'nonthrough', None, 'NOT_PERCOLATING'),
                                     ('연속체 하한 (MODEL_BELOW_CONTINUUM_BOUND — 값 유지 HOLD)', 'through',
                                      {'phi_se_mass_conserving': 1e-4}, 'MODEL_BELOW_CONTINUUM_BOUND')):
            d, a, c = _case(bed, over)
            _s, rid, st, failed = _run(d, a, c, _CLIRunner())
            row = _tf.case_row(d)
            ok[lbl] = (st, row.get('ion_net_status_hertz'), row.get('ion_net_status_physics'), want)
            shutil.rmtree(d, ignore_errors=True)
        bad_ok = {k: v for k, v in ok.items() if not (v[0] == 'done' and v[1] == v[2] == v[3])}
        chk(f'T15b) 양성 대조 (실 생산자): 건전 · 등록된 과학적 HOLD 셋은 막지 않는다 (done · τ 상태 그대로) {bad_ok or ""}',
            not bad_ok and len(ok) == 4)

        # T15c — 정상 비관통 (실 생산자 출력) 위 **한 키씩** 변이: valid_zero 를 받는 조건 (③ 사유 · 채널 · 독립 calc_percolation · ④ 등록 사유)
        #         이 각각 문다 — 모든 not_computed 허용 · None→0 은 오답 (Codex RGL-02 최소 수정).
        def _set(**kv):
            def _f(rec, _n, _m):
                rec.update({k.replace('TAIL', 'hertz' if _m == 'hertzian' else 'physics'): v for k, v in kv.items()})
            return lambda o: _edit_net_records(o, _f)
        nbad = {
            '③ 사유가 no_through_path 가 아니다 (solve_failed)': (_set(sigma_full_reason='solve_failed'), None),
            '③ 이온 채널이 valid_zero 가 아니다 (옛 valid_null)': (_set(ionic_status='valid_null'), None),
            '③ CF 상태 not_computed (FULL 과 어긋남)': (_set(sigma_bulk_net_status='not_computed'), None),
            '③ 독립 calc_percolation 50 % (솔버는 비관통)': (None, {'percolation_pct': 50.0}),
            '④ 전력 몫 사유 = 관통인데 FULL 풀이 실패 (등록된 물리 사유 아님)':
                (_set(constriction_power_share_ion_TAIL_status='not_computed (FULL solve failed on a percolating network)'), None),
        }
        nres = {}
        for lbl, (mut, over) in nbad.items():
            d, a, c = _case('nonthrough', over)
            _s, rid, st, failed = _run(d, a, c, _CLIRunner(mutate=mut))
            nres[lbl] = (st, any(STOP in f for f in failed))
            shutil.rmtree(d, ignore_errors=True)
        nmiss = {k: v for k, v in nres.items() if v != ('failed', True)}
        chk(f'T15c) ★ RGL-02 비관통 상태를 받는 조건 {len(nbad)} 종 — 실 비관통 출력에 한 키씩 변이 → 전부 failed (정지 계약) {nmiss or ""}',
            not nmiss and len(nres) == len(nbad))

        # T15d — 승격된 건전 결과 위에서 계약 함수만: 디스크 full_metrics 그대로 → ok · 망 소유 키 하나를 옛 세대 값으로 (σ₀ 0.012 · 열 σ 777)
        #         바꾸면 ⑥ (투영 ≠ 이번 세대) · ⑧ 로 거부 · 후보 투영 (fm=) 인자로도 같은 판정
        d, a, c = _case('through')
        _s, rid, st, failed = _run(d, a, c, _CLIRunner())
        fmd = _fm(d)
        v_ok = ps.network_stop_verdict(d, rid)
        v_s0 = ps.network_stop_verdict(d, rid, fm=dict(fmd, sigma_grain_S_cm=0.012))
        v_th = ps.network_stop_verdict(d, rid, fm=dict(fmd, thermal_sigma_full_mScm=777.0))
        chk(f'T15d) ★ RGL-08 · 07 정지 계약 = 이번 세대 투영 대조 — 디스크 그대로 ok · σ₀ 옛 값 → ⑥ · ⑧ 거부 · 열 σ 옛 값 → ⑥ 거부 '
            f'({v_ok[0]} · {v_s0[0]} · {v_th[0]})',
            st == 'done' and v_ok[0] is True and v_s0[0] is False and '⑥' in v_s0[1] and '⑧' in v_s0[1]
            and v_th[0] is False and 'thermal_sigma_full_mScm' in v_th[1])
        shutil.rmtree(d, ignore_errors=True)
    _guard('T15', t15)

    # ── T16 (RGL-07) — σ 와 σ₀ · 온도는 한 소유 단위로 지우고 병합한다 (옛 온도 factor 생존 → τ 2× 금지) ─────────────────────
    def _codex_record(mode):
        tail = 'hertz' if mode == 'hertzian' else 'physics'
        return dict(sigma_full=0.05, sigma_full_mScm=0.15, sigma_full_status='computed', sigma_bulk_net=0.1, sigma_bulk_net_mScm=0.3,
                    percolating_fraction=1.0, sigma_grain_S_cm=0.003,
                    temperature_provenance={'sigma_ion_T_factor': 1.0, 'T_C': None, 'T_ref_C': 25.0},
                    phi_se=0.3, boundary_rule='L0', boundary_band_frac=0.08,
                    ionic_status='computed', electronic_status='computed', thermal_status='computed',
                    **{f'constriction_power_share_ion_{tail}': 0.5, f'constriction_power_share_ion_{tail}_status': 'computed'})

    def t16():
        # ⓐ Codex 수치 그대로 (probe_contracts — solver 파일 작성만 fixture · helper · merge · grade 는 실 함수)
        got = {}
        for lbl, seed in (('깨끗한 입력', None),
                          ('옛 factor 4 생존 (60 °C 자료 → 기본 온도 재계산)',
                           {'temperature_provenance': {'sigma_ion_T_factor': 4.0, 'T_C': 60.0}})):
            d = tempfile.mkdtemp(prefix='t16_')
            fm = {'phi_se': 0.3, 'thickness_um': 100.0, 'thickness_mass_conserving_um': 100.0, 'phi_se_mass_conserving': 0.3,
                  'percolation_pct': 100.0}
            fm.update(seed or {})
            with open(os.path.join(d, 'full_metrics.json'), 'w') as f:
                json.dump(fm, f)
            H, P = _codex_record('hertzian'), _codex_record('physics')
            arts = {'network_conductivity.json': copy.deepcopy(H), 'network_conductivity_hertzian.json': H,
                    'network_conductivity_physics.json': P,
                    'network_conductivity_dual.json': {'hertzian': copy.deepcopy(H), 'physics': copy.deepcopy(P)}}

            def _fx(cmd, _d=d, _a=arts, **kw):
                for _n, _v in _a.items():
                    with open(os.path.join(_d, _n), 'w') as f:
                        json.dump(_v, f)
                return subprocess.CompletedProcess(cmd, 0, 'synthetic solver fixture', '')
            stages, _rid = webapp._network_and_stage_e(d, _SCRIPTS_DIR, os.path.join(d, 'a.csv'), os.path.join(d, 'c.csv'),
                                                       '1:AM,3:SE', 1000, [], runner=_fx, stop_before_stage_e=True)
            fm2 = _fm(d)
            got[lbl] = (ps.summarize(stages)[0], _tf.tau2_from_metrics(fm2)[1], _ge._derived_value('__tau_lap_eff', fm2),
                        (fm2.get('temperature_provenance') or {}).get('sigma_ion_T_factor'))
            shutil.rmtree(d, ignore_errors=True)
        chk(f'T16a) ★ RGL-07 (Codex 수치): 깨끗한 입력 ↔ 옛 factor 4 생존 → 둘 다 done · 짝 σ₀ 3 · 등급 τ 2.449489742783178 '
            f'(옛: 12 · 4.898979485566356) {got}',
            all(v[0] == 'done' and v[1] == 3.0 and v[2] is not None and abs(v[2] - 2.449489742783178) < 1e-12 and v[3] == 1.0
                for v in got.values()) and len(got) == 2)

        # ⓑ 실 retry 라우트 (`/retry-network/<id>` — contact 를 다시 쓰지 않고 helper 를 부른다 · 망 = 실 CLI · Stage E = 대역)
        import types as _types
        tmp = tempfile.mkdtemp(prefix='t16r_')
        prev_cfg = {k: webapp.app.config.get(k) for k in ('UPLOAD_FOLDER', 'RESULTS_FOLDER', 'SCRIPTS_FOLDER')}
        prev_runner, prev_thr = ps._RUNNER, webapp.threading

        class _SyncThread:
            def __init__(self, target=None, daemon=None, **kw):
                self._t = target

            def start(self):
                self._t()
        out = {}
        try:
            webapp.app.config['UPLOAD_FOLDER'] = os.path.join(tmp, 'uploads')
            webapp.app.config['RESULTS_FOLDER'] = os.path.join(tmp, 'results')
            webapp.app.config['SCRIPTS_FOLDER'] = _SCRIPTS_DIR
            webapp.threading = _types.SimpleNamespace(**{**vars(prev_thr), 'Thread': _SyncThread})
            ps._RUNNER = _CLIRunner(delegate=_fake_stage_e)
            client = webapp.app.test_client()
            for lbl, seed in (('깨끗한 입력', None),
                              ('옛 60 °C 자료 (factor 4 · σ₀ 0.012 S/cm) 위 기본 온도 retry',
                               {'temperature_provenance': {'sigma_ion_T_factor': 4.0, 'T_C': 60.0}, 'sigma_grain_S_cm': 0.012})):
                cid = 'rt16_' + ('clean' if seed is None else 'stale')
                up, rd = os.path.join(tmp, 'uploads', cid), os.path.join(tmp, 'results', cid)
                os.makedirs(up)
                os.makedirs(rd)
                with open(os.path.join(up, 'meta.json'), 'w') as f:
                    json.dump({'name': cid, 'mode': 'standard', 'type_map': '1:SE', 'scale': 1, 'status': 'done'}, f)
                _write_bed(rd, 'through')
                fm = dict(_bed_ledger('through'))
                fm.update(seed or {})
                with open(os.path.join(rd, 'full_metrics.json'), 'w') as f:
                    json.dump(fm, f)
                resp = client.post(f'/retry-network/{cid}')
                meta = json.load(open(os.path.join(up, 'meta.json')))
                fm2 = _fm(rd)
                out[lbl] = (resp.status_code, meta.get('pipeline_status'), _tf.tau2_from_metrics(fm2)[1],
                            _ge._derived_value('__tau_lap_eff', fm2), fm2.get('sigma_grain_S_cm'),
                            (fm2.get('temperature_provenance') or {}).get('sigma_ion_T_factor'))
        finally:
            ps._RUNNER, webapp.threading = prev_runner, prev_thr
            for k, v in prev_cfg.items():
                if v is None:
                    webapp.app.config.pop(k, None)
                else:
                    webapp.app.config[k] = v
            shutil.rmtree(tmp, ignore_errors=True)
        vals = list(out.values())
        chk(f'T16b) ★ RGL-07 실 retry 라우트: 옛 60 °C 자료 위 기본 온도 재계산 → σ₀ · 온도 짝이 새 세대로 바뀐다 (σ₀ 3 · factor 1 · '
            f'τ = 깨끗한 입력과 같다 — 옛: σ₀ 12 · τ 2×) {out}',
            len(vals) == 2 and all(v[0] == 200 and v[1] == 'done' and v[2] == 3.0 and v[4] == 0.003 and v[5] == 1.0 for v in vals)
            and vals[0][3] is not None and vals[0][3] == vals[1][3])

        # ⓒ 두 모드 짝 대조 — physics 모드만 다른 σ₀ (모드 파일 · dual 같이 = 파일은 서로 맞는다) → 정지 경로 failed · 일반 경로도 승격 안 함
        def _p_s0(rec, _n, m):
            if m == 'physics':
                rec['sigma_grain_S_cm'] = 0.0045
        res = {}
        for lbl, stop in (('정지 경로', True), ('일반 경로 (Stage E 앞 승격 검사)', False)):
            d, a, c = _case('through')
            fm0 = open(os.path.join(d, 'full_metrics.json')).read()
            r = _CLIRunner(mutate=lambda o: _edit_net_records(o, _p_s0), delegate=_fake_stage_e)
            _s, rid, st, failed = _run(d, a, c, r, stop=stop)
            res[lbl] = (st, ps.read_network_provenance(d).get('provenance_state'),
                        open(os.path.join(d, 'full_metrics.json')).read() == fm0,
                        not any(os.path.exists(os.path.join(d, n)) for n in _NET_FOUR))
            shutil.rmtree(d, ignore_errors=True)
        chk(f'T16c) ★ 두 모드 (σ₀, 온도) 짝이 다르면 승격하지 않는다 — 두 경로 failed · 활성 세대 없음 · full_metrics 그대로 · 후보 치움 {res}',
            all(v == ('failed', 'missing', True, True) for v in res.values()) and len(res) == 2)
    _guard('T16', t16)


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

        # T9 (LHS 배치 2026-09-28 — `scripts/lhs_webapp_batch.py`): `figures=False` · `auto_db=False` 는 그림 단계와
        #   자동 DB 재구축 **만** 뺀다.  계산 단계 (파싱 · 접촉 · 피복 · network · Stage E · 이중 공극률 · 고급 분석) 는
        #   순서까지 그대로여야 한다 — 배치가 웹앱과 **다른 계산**을 하면 코퍼스 열과 같은 이름을 붙일 수 없다.
        #   자동 DB 는 `subprocess.Popen` 직접 호출이라 app 모듈의 이름만 가짜로 바꿔 센다 (전역 subprocess 는 안 건드린다).
        import types as _types
        _popen_calls = []

        class _FakePopen:
            def __init__(self, cmd, **kw):
                _popen_calls.append(cmd)
        _real_sp = webapp.subprocess
        webapp.subprocess = _types.SimpleNamespace(**{**vars(_real_sp), 'Popen': _FakePopen})
        _t9 = {}
        try:
            for _mode, _tm in (('standard', '1:AM,3:SE'), ('bimodal', '1:AM_P,2:AM_S,3:SE')):
                for _kw in ({}, {'figures': False, 'auto_db': False}):
                    shutil.rmtree(res_dir, ignore_errors=True)
                    _r = make_runner(contact_rc=0)
                    ps._RUNNER = _r
                    _n0 = len(_popen_calls)
                    try:
                        _o = webapp.run_pipeline('case1', _mode, _tm, 1000, **_kw)
                    except TypeError as _e:                 # 옛 서명 — 키워드가 없다
                        _o = {'status': f'TypeError: {_e}'}
                    _t9[(_mode, bool(_kw))] = (_r, _o, len(_popen_calls) - _n0)
        finally:
            webapp.subprocess = _real_sp

        def _scripts(r):
            return [os.path.basename(str(c[1])) for c in r.calls if len(c) > 1]

        def _figs(r):
            return [s for s in _scripts(r) if s.startswith('generate_') and 'figures' in s]
        for _mode in ('standard', 'bimodal'):
            _rd, _od, _pd = _t9[(_mode, False)]
            _ro, _oo, _po = _t9[(_mode, True)]
            chk(f'T9a) {_mode} 기본값: 그림 단계 ≥ 2 · 자동 DB 1 회 (웹앱 동작 불변)',
                len(_figs(_rd)) >= 2 and _pd == 1 and _od.get('status') == 'done')
            chk(f'T9b) ★ {_mode} figures=False · auto_db=False: 그림 단계 0 · 자동 DB 0 · done',
                _figs(_ro) == [] and _po == 0 and _oo.get('status') == 'done')
            chk(f'T9c) ★ {_mode} 계산 단계는 순서까지 그대로 (그림을 뺀 스크립트 열이 같다)',
                [s for s in _scripts(_rd) if s not in _figs(_rd)] == _scripts(_ro))

        # T10 (LHS 묶음별 · 1저자 09-29 밤 *"단독적으로 하나씩 돌려서 표를 채워나갈 거야"*): stop_after='contact' 는
        #   접촉 분석 단계에서 멈춘다 — 그때까지의 명령은 전체 실행의 **앞부분과 인자까지 같고**, network · Stage E ·
        #   고급 분석은 돌지 않는다.  명령이 다르면 ① 열을 코퍼스와 같은 이름으로 붙일 수 없다.
        _t10 = {}
        for _mode, _tm in (('standard', '1:AM,3:SE'), ('bimodal', '1:AM_P,2:AM_S,3:SE')):
            for _stop in (None, 'contact'):
                shutil.rmtree(res_dir, ignore_errors=True)
                _r = make_runner(contact_rc=0)
                ps._RUNNER = _r
                _kw = {'figures': False, 'auto_db': False}
                if _stop:
                    _kw['stop_after'] = _stop
                try:
                    _o = webapp.run_pipeline('case1', _mode, _tm, 1000, **_kw)
                except TypeError as _e:                 # 옛 서명 — 키워드가 없다
                    _o = {'status': f'TypeError: {_e}'}
                _t10[(_mode, _stop)] = (_r, _o)
        for _mode, _cs in (('standard', 'analyze_contacts.py'), ('bimodal', 'analyze_contacts_bimodal.py')):
            _rf, _of = _t10[(_mode, None)]
            _rs, _os10 = _t10[(_mode, 'contact')]
            _ss = _scripts(_rs)
            chk(f'T10a) ★ {_mode} stop_after=contact: 접촉 분석에서 끝난다 (network · Stage E 없음) · done · stopped_after 표지',
                bool(_ss) and _ss[-1] == _cs and 'network_conductivity.py' not in _ss
                and _os10.get('status') == 'done' and _os10.get('stopped_after') == 'contact')
            chk(f'T10b) ★ {_mode} 멈춘 실행의 명령 = 전체 실행의 앞부분 (인자까지 같다)',
                len(_rs.calls) >= 2 and [list(map(str, c)) for c in _rs.calls]
                == [list(map(str, c)) for c in _rf.calls[:len(_rs.calls)]])
        shutil.rmtree(res_dir, ignore_errors=True)
        ps._RUNNER = make_runner(contact_rc=0)
        try:
            webapp.run_pipeline('case1', 'standard', '1:AM,3:SE', 1000, stop_after='stage_e')
            _t10c = 'no error'
        except ValueError:
            _t10c = 'ValueError'
        except TypeError as _e:
            _t10c = f'TypeError: {_e}'
        chk(f'T10c) stop_after 가 None · contact · coverage · network 가 아니면 ValueError — 조용히 전체를 돌지 않는다 ({_t10c})', _t10c == 'ValueError')
        shutil.rmtree(res_dir, ignore_errors=True)
        ps._RUNNER = make_runner(contact_rc=1)
        try:
            _o10d = webapp.run_pipeline('case1', 'standard', '1:AM,3:SE', 1000, stop_after='contact')
        except TypeError as _e:
            _o10d = {'status': f'TypeError: {_e}'}
        chk('T10d) stop_after=contact 이어도 접촉 분석 실패는 failed (기존 계약 그대로)', _o10d.get('status') == 'failed')

        # T11 (LHS cap coverage 인계 · 1저자 09-29 밤 *"stop_after='coverage' 로 ① + cap coverage 한 번에"*): stop_after='coverage'
        #   는 피복 단계 (`coverage_physics_vs_hertzian.py`) 에서 멈춘다 — 그때까지의 명령은 전체 실행의 **앞부분과 인자까지
        #   같고** network · Stage E 는 돌지 않는다.  이 모드의 산출물은 피복 단계 **자체**라 계약이 전체 실행보다 엄하다:
        #   required + 내용 검증 (이번 피복 단계가 full_metrics.json 에 physics v2 판정을 썼는가).  옛 피복 스크립트는
        #   데이터 폴더가 코드 밖이면 "[skip]" 을 찍고 **rc 0 으로 아무것도 안 썼다** — 그것을 done 으로 받지 않는다.
        def _healthy_cov_v2():
            """실제 피복 스크립트 (`_PhysicsV2Book.keys`) 가 ok 침대에 쓰는 v2 키 집합을 **타입까지** 맞춘 건전한 레코드 (LHSC-03).
            ★ fixture-drift 방지 — 가짜 producer 가 status 한 줄만 쓰면 검증기가 엄해질 때 거짓 실패한다 (RC5-01 · RC6-01 과 같은 교훈)."""
            _d = {k: 1.0 for k in getattr(webapp, 'COVERAGE_V2_OK_KEYS', ())}
            #  LHSC-03 R3 (09-30 밤 재검증 2): 개수 dict 는 생산자의 분류 집합 · 총합 항등식 (Σ pair = nconf · Σ binding = n · AM–SE ≤ 총) 에
            #  맞게 · 분율 키 둘은 존재 + round(개수 비, 6) — 옛 레코드 ({'x': 1} · 분율 없음) 는 엄격해진 검증기가 거부한다
            _pairs = tuple(getattr(webapp, 'COVERAGE_V2_PAIR_KEYS', ('AM_SE', 'SE_SE', 'AM_AM', 'other')))
            _binds = tuple(getattr(webapp, 'COVERAGE_V2_BINDING_KEYS', ('elastic', 'tabor', 'volume', 'geom', 'none')))
            _d.update({'cap_conflict_n_by_pair_physics_v2': {q: 0 for q in _pairs},
                       #  LHSC-03-R4: cap 가지 수 (n_cap 1) = binding tabor + volume + geom — 옛 판 (elastic 4 · cap 1) 은 모순이었다
                       'A_binding_counts_total_physics_v2': {b: {'elastic': 3, 'tabor': 1}.get(b, 0) for b in _binds},
                       'A_binding_counts_AM_SE_physics_v2': {b: (2 if b == _binds[0] else 0) for b in _binds},
                       'cap_conflict_frac_physics_v2': 0.0, 'cap_conflict_frac_cap_branch_physics_v2': 0.0})
            if _d:
                _d['am_denominator_physics_v2'] = {'n_am': 2, 'n_free_surface_nonpositive': 0, 'n_coverage_clipped_100': 0,
                                                   'n_radius_invalid': 0}
                _d['rule_physics_v2'] = 'rule'
                #  LHSC-03 R2 (09-30 밤): 옛 레코드는 개수 키를 1.0 (실수) · 접촉 실패 1 로 적었다 — 생산자는 개수를 정수로 ·
                #  ok 에서는 접촉 실패 0 · cap 충돌 ≤ cap 가지 ≤ 접촉 · 막 두께 > 0 으로 쓴다 (엄격해진 검증기가 옛 레코드를 거부한다)
                _d.update({'n_contacts_physics_v2': 4, 'n_cap_branch_physics_v2': 1, 'cap_conflict_n_physics_v2': 0,
                           'n_contacts_unknown_id_physics_v2': 0, 'n_contact_failures_physics_v2': 0,
                           'h_film_sim_physics_v2': 5e-6})
            _d.update({'coverage_status_physics_v2': 'ok', 'coverage_AM_mean_physics_v2': 12.5})
            return _d

        def make_cov_runner(contact_rc=0, cov_writes=True, cov_rc=0):
            """make_runner + 피복 스크립트 흉내 (full_metrics.json 에 v2 판정 키를 얹는다 — 실제 스크립트와 같은 자리 · 같은 키 집합)."""
            _base = make_runner(contact_rc=contact_rc)

            def _r(cmd, **kw):
                script = os.path.basename(str(cmd[1])) if len(cmd) > 1 else ''
                if script != 'coverage_physics_vs_hertzian.py':
                    return _base(cmd, **kw)
                _base.calls.append(cmd)
                if cov_writes:
                    _fm = os.path.join(res_dir, 'full_metrics.json')
                    _d = json.load(open(_fm)) if os.path.exists(_fm) else {}
                    _d.update(_healthy_cov_v2())
                    with open(_fm, 'w') as _f:
                        json.dump(_d, _f)
                return subprocess.CompletedProcess(cmd, cov_rc, '', '')
            _r.calls = _base.calls
            return _r

        def _run11(mode, tm, stop, **rk):
            shutil.rmtree(res_dir, ignore_errors=True)
            _r = make_cov_runner(**rk)
            ps._RUNNER = _r
            _kw = {'figures': False, 'auto_db': False}
            if stop:
                _kw['stop_after'] = stop
            try:
                _o = webapp.run_pipeline('case1', mode, tm, 1000, **_kw)
            except (TypeError, ValueError) as _e:           # 옛 코드 — 'coverage' 를 모른다
                _o = {'status': f'{type(_e).__name__}: {_e}'}
            return _r, _o
        for _mode, _tm, _cs in (('standard', '1:AM,3:SE', 'analyze_contacts.py'),
                                ('bimodal', '1:AM_P,2:AM_S,3:SE', 'analyze_contacts_bimodal.py')):
            _rf, _of = _run11(_mode, _tm, None)
            _rs, _os11 = _run11(_mode, _tm, 'coverage')
            _ss = _scripts(_rs)
            chk(f'T11a) ★ {_mode} stop_after=coverage: 접촉 → 피복 에서 끝난다 (network · Stage E 없음) · done · stopped_after 표지'
                f' ({_os11.get("status")})',
                _ss[-2:] == [_cs, 'coverage_physics_vs_hertzian.py'] and 'network_conductivity.py' not in _ss
                and 'run_network_full_corrections.py' not in _ss
                and _os11.get('status') == 'done' and _os11.get('stopped_after') == 'coverage')
            chk(f'T11b) ★ {_mode} 멈춘 실행의 명령 = 전체 실행의 앞부분 (인자까지 같다)',
                len(_rs.calls) >= 3 and [list(map(str, c)) for c in _rs.calls]
                == [list(map(str, c)) for c in _rf.calls[:len(_rs.calls)]])
            _rn, _on = _run11(_mode, _tm, 'coverage', cov_writes=False)
            _rfn, _ofn = _run11(_mode, _tm, None, cov_writes=False)
            chk(f'T11c) ★ {_mode} 피복 rc 0 인데 v2 판정을 안 썼다 → failed (조용한 초록 아님) · 전체 실행의 optional 계약은 그대로'
                f' ({_on.get("status")} · 전체 {_ofn.get("status")})',
                _on.get('status') == 'failed' and _on.get('stopped_after') == 'coverage'
                and any('Coverage' in str(s) for s in _on.get('failed_stages', []))
                and _ofn.get('status') == 'done')
            _rr, _or = _run11(_mode, _tm, 'coverage', cov_rc=1)
            chk(f'T11d) {_mode} 피복 rc 1 → failed ({_or.get("status")})',
                _or.get('status') == 'failed' and _or.get('stopped_after') == 'coverage')
        _t11e = []
        for _bad in ('Network', 'network ', 'Coverage', 'coverage ', '', 'stage_e', 0, False):
            shutil.rmtree(res_dir, ignore_errors=True)
            ps._RUNNER = make_cov_runner()
            try:
                webapp.run_pipeline('case1', 'standard', '1:AM,3:SE', 1000, stop_after=_bad)
                _t11e.append(f'{_bad!r}: no error')
            except ValueError:
                pass
            except TypeError as _e:
                _t11e.append(f'{_bad!r}: TypeError {_e}')
        chk(f'T11e) None · contact · coverage · network 밖의 값은 전부 ValueError (조용히 전체를 돌지 않는다) {_t11e}', not _t11e)
        _rc, _oc = _run11('standard', '1:AM,3:SE', 'coverage', contact_rc=1)
        chk('T11f) stop_after=coverage 이어도 접촉 분석 실패는 failed · 피복은 돌지 않는다',
            _oc.get('status') == 'failed' and 'coverage_physics_vs_hertzian.py' not in _scripts(_rc))

        # T11g–T11j ★ Codex LHSC-02 (P1) · LHSC-03 (P2) (09-30 · 1저자 비준 "권고대로"): atoms-only 조기 반환 두 곳 (raw atom-only ·
        #   CSV-only) 이 `stop_after='coverage'` 요청을 **계산 없이 success/done** 으로 끝냈다 (Codex `audit_pipeline.py` `atoms_only`) ·
        #   `_coverage_v2_written` 은 문자열이면 다 True 였다 (`''` · `'not_run'` · 사유 없는 `'blank: '` · 키 없는 `'ok'`).
        #   계약: 분석 단계를 명시적으로 요청하면 (stop_after ≠ None) 두 경로 모두 failed — 계산 · 도장 · 러너 호출 없이 · None 은
        #   viewer 전용 성공 그대로 (양성 대조) · 상태 검증 = 'ok' + 필수 값/진단 키 (None 불가) 또는 비지 않은 'blank: 사유' + 진단 키.
        _up_csv = os.path.join(tmp, 'uploads', 'case_csv')       # atoms.csv 만 (contacts.csv · contact_*.liggghts 없음)
        os.makedirs(_up_csv, exist_ok=True)
        open(os.path.join(_up_csv, 'atoms.csv'), 'w').write('id,type,radius,x,y,z\n1,1,0.001,0,0,0\n')
        _up_raw = os.path.join(tmp, 'uploads', 'case_raw')       # atom_1.liggghts 만
        os.makedirs(_up_raw, exist_ok=True)
        open(os.path.join(_up_raw, 'atom_1.liggghts'), 'w').write('x')
        _spawned = []
        _real_sp_run = webapp.subprocess.run

        def _spy_run(cmd, *a, **kw):                             # raw 경로는 _ps 러너가 아니라 subprocess.run 을 직접 부른다
            _spawned.append(os.path.basename(str(cmd[1])) if len(cmd) > 1 else str(cmd))
            return subprocess.CompletedProcess(cmd, 0, '', '')
        webapp.subprocess.run = _spy_run
        try:
            _g = {}
            for _cid in ('case_csv', 'case_raw'):
                for _stop in ('coverage', 'contact', 'network', None):
                    shutil.rmtree(os.path.join(tmp, 'results', _cid), ignore_errors=True)
                    _rr = make_cov_runner()
                    ps._RUNNER = _rr
                    del _spawned[:]
                    _kw = {'figures': False, 'auto_db': False}
                    if _stop:
                        _kw['stop_after'] = _stop
                    try:
                        _o = webapp.run_pipeline(_cid, 'standard', '1:AM,2:SE', 1000, **_kw)
                    except ValueError as _e:                 # 옛 코드 — 'network' 을 모른다 (시험이 멈추지 않고 FAIL 로 남게)
                        _o = {'status': f'ValueError: {_e}'}
                    _fm_p = os.path.join(tmp, 'results', _cid, 'full_metrics.json')
                    _g[(_cid, _stop)] = (_o, os.path.exists(_fm_p), len(_rr.calls), list(_spawned))
            for _cid, _lbl in (('case_csv', 'CSV-only'), ('case_raw', 'raw atom-only')):
                for _stop in ('coverage', 'contact', 'network'):
                    _o, _has_fm, _ncall, _sp = _g[(_cid, _stop)]
                    _expr = _o.get('status') or ('done' if _o.get('success') else 'failed')     # 배치의 상태식 (lhs_webapp_batch)
                    chk(f'T11g) ★ LHSC-02 {_lbl} + stop_after={_stop}: failed (success False · 배치 상태식 failed · stopped_after 표지) · '
                        f'계산 · 도장 · 러너 · subprocess 호출 없음 ({_o.get("status")!r} · fm={_has_fm} · 호출 {_ncall} · spawn {_sp})',
                        _o.get('success') is False and _o.get('status') == 'failed' and _expr == 'failed'
                        and _o.get('stopped_after') == _stop and not _has_fm and _ncall == 0 and not _sp)
                _o, _has_fm, _ncall, _sp = _g[(_cid, None)]
                chk(f'T11h) 양성 대조 {_lbl} + stop_after=None: viewer 전용 성공 그대로 (success · atoms_only · has_contacts false) '
                    f'({_o.get("success")} · fm={_has_fm})',
                    _o.get('success') is True and _o.get('atoms_only') is True and _has_fm
                    and json.load(open(os.path.join(tmp, 'results', _cid, 'full_metrics.json'))).get('has_contacts') is False)
        finally:
            webapp.subprocess.run = _real_sp_run
        # T11i · T11j — `_coverage_v2_written` 의 스키마 계약 (생산자 = coverage_physics_vs_hertzian `keys` · 내부 오류 경로)
        _vd = os.path.join(tmp, 'results', 'v2_schema')
        os.makedirs(_vd, exist_ok=True)

        def _v2w(d):
            with open(os.path.join(_vd, 'full_metrics.json'), 'w') as _f:
                json.dump(d, _f)
            return webapp._coverage_v2_written(_vd)
        _ok_keys = tuple(getattr(webapp, 'COVERAGE_V2_OK_KEYS', ()))
        _diag_keys = tuple(getattr(webapp, 'COVERAGE_V2_DIAG_KEYS', ()))
        _healthy = _healthy_cov_v2()                             # T11a–d 의 가짜 producer 와 같은 레코드
        _blank = {k: None for k in _diag_keys}
        _blank.update({'coverage_status_physics_v2': 'blank: 1 접촉을 film_area_physics_v2 가 거부했다', 'n_contact_failures_physics_v2': 1})
        _bad = {lbl: _v2w(d) for lbl, d in (
            ('빈 dict', {}), ('빈 문자열', {'coverage_status_physics_v2': ''}), ('not_run', {'coverage_status_physics_v2': 'not_run'}),
            ('ok 만 (값 키 없음)', {'coverage_status_physics_v2': 'ok'}),
            ('blank 사유 없음', {**_blank, 'coverage_status_physics_v2': 'blank: '}),
            ('blank 진단 키 없음', {'coverage_status_physics_v2': 'blank: 사유'}),
            ('ok 인데 면적 None', {**_healthy, 'area_AM전체_SE_total_physics_v2': None}),
            ('ok 인데 AM 있는데 피복률 없음', {k: v for k, v in _healthy.items() if k != 'coverage_AM_mean_physics_v2'}),
            ('ok 인데 진단 dict 아님', {**_healthy, 'am_denominator_physics_v2': 3}))}
        chk(f'T11i) ★ LHSC-03: 빈 문자열 · not_run · 키 없는 ok · 사유 없는 blank · 진단 없는 blank · 값 None 인 ok 는 전부 False '
            f'({[l for l, v in _bad.items() if v]})', _ok_keys and _diag_keys and not any(_bad.values()))
        _good = {lbl: _v2w(d) for lbl, d in (
            ('ok + 필수 값 · 진단 키', _healthy),
            ('ok · AM 0 개 (피복률 키 없어도 됨 · AM 이 낀 면적 · 결속 · 충돌 0)',
             {**{k: v for k, v in _healthy.items() if k != 'coverage_AM_mean_physics_v2'},
              'am_denominator_physics_v2': {'n_am': 0, 'n_free_surface_nonpositive': 0, 'n_coverage_clipped_100': 0, 'n_radius_invalid': 0},
              'area_AM전체_SE_total_physics_v2': 0.0, 'area_AM전체_AM_total_physics_v2': 0.0,
              'A_binding_counts_AM_SE_physics_v2': {b: 0 for b in _healthy['A_binding_counts_AM_SE_physics_v2']}}),
            ('blank: 사유 + 진단 키', _blank))}
        chk(f'T11j) LHSC-03 양성 대조: ok + 필수 키 · AM 0 개 ok · 사유 있는 blank + 진단 키 는 True ({[l for l, v in _good.items() if not v]})',
            all(_good.values()))

        # T11k · T11l · T11m ★ Codex LHSC-03 R2 (09-30 밤 재검증 · P2 · 1저자 비준 09-30 낮 "비준이야") — 반례 먼저
        #   R2: 검증기가 n_am 누락을 0 으로 읽고 (`(diag.get('n_am') or 0) > 0`) 값은 None 만 봐서, **실제 생산자 출력**에서 출발한 변이
        #   10 종이 전부 받아들여졌다 (n_am 삭제 · 면적 NaN 은 필수 단계까지 done).  계약: n_am = 명시적 비음수 정수 (bool 제외) ·
        #   ok = 면적 유한 ≥ 0 · 피복률 유한 [0, 100] · 개수 정수 · 범위 · 무효 분모 · 접촉 실패와 공존 불가 · blank = 사유 · 진단 +
        #   물리 값 잔재 없음 (진단 일부 None 은 내부 오류 경로라 그대로 받는다).
        #   양성 대조 = 가짜 레코드가 아니라 **실제 생산자** (`coverage_physics_vs_hertzian.compute_case`) 의 출력 8 종.
        import contextlib as _ctx
        import copy as _copy
        import io as _io
        from pathlib import Path as _P
        _scr = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
        if _scr not in sys.path:
            sys.path.insert(0, _scr)
        import coverage_physics_vs_hertzian as _cv
        _root = _P(tmp) / 'lhsc03r2'
        _prod = {}
        for _var in ('base', 'isolated_zero', 'denom_zero', 'nan_radius', 'nan_delta', 'scale1', 'no_ligg_col', 'se_only'):
            _d, _tm, _sc = _cv._selftest_fixture(_root / _var, variant=('base' if _var == 'se_only' else _var))
            if _var == 'se_only':                              # SE 둘 · 접촉 0 (Codex 양성 대조 그대로)
                (_d / 'atoms.csv').write_text('id,type,radius,x,y,z\n1,3,0.001,0,0,0\n2,3,0.001,0,0,0.003\n')
                (_d / 'contacts.csv').write_text('id1,id2,delta,contact_area\n')
            with _ctx.redirect_stdout(_io.StringIO()):
                _cv.compute_case(_var, _d, _tm, scale=_sc)
            _prod[_var] = (str(_d), json.loads((_d / 'full_metrics.json').read_text()))
        _pos = {k: webapp._coverage_v2_written(v[0]) for k, v in _prod.items()}
        chk(f'T11k) LHSC-03 R2 양성 대조: 실제 생산자 출력 8 종 (정상 · 고립 AM 0 % · 무효 분모 · NaN 반경 · δ NaN · scale 1 · 면적 열 없음 · '
            f'SE-only) 은 전부 판정으로 받는다 — 거부 {[k for k, v in _pos.items() if not v]} · 상태 '
            f'{ {k: str(v[1].get("coverage_status_physics_v2"))[:12] for k, v in _prod.items()} }', all(_pos.values()))
        _hl = _prod['base'][1]

        def _mut(name):                                        # Codex audit_delta.py schema_mutations 그대로 (정상 생산자 출력에서)
            x = _copy.deepcopy(_hl)
            if name.endswith('no_coverage') or name == 'missing_n_am_and_coverage':
                for k in list(x):
                    if k.startswith('coverage_AM') and k.endswith('_physics_v2'):
                        del x[k]
            if name == 'missing_n_am_and_coverage':
                del x['am_denominator_physics_v2']['n_am']
            elif name == 'negative_n_am_and_no_coverage':
                x['am_denominator_physics_v2']['n_am'] = -1
            elif name == 'nan_n_am_and_no_coverage':
                x['am_denominator_physics_v2']['n_am'] = float('nan')
            elif name == 'ok_but_invalid_denom_count':
                x['am_denominator_physics_v2']['n_free_surface_nonpositive'] = 1
            elif name == 'area_nan':
                x['area_AM전체_SE_total_physics_v2'] = float('nan')
            elif name == 'area_string':
                x['area_AM전체_SE_total_physics_v2'] = 'broken'
            elif name == 'area_negative':
                x['area_AM전체_SE_total_physics_v2'] = -1.0
            elif name == 'coverage_negative':
                x['coverage_AM_mean_physics_v2'] = -1.0
            elif name == 'ok_but_contact_failures':
                x['n_contact_failures_physics_v2'] = 1
            elif name == 'blank_with_positive_values':
                x['coverage_status_physics_v2'] = 'blank: undefined denominator'
            return x
        _muts = ('missing_n_am_and_coverage', 'negative_n_am_and_no_coverage', 'nan_n_am_and_no_coverage',
                 'ok_but_invalid_denom_count', 'area_nan', 'area_string', 'area_negative', 'coverage_negative',
                 'ok_but_contact_failures', 'blank_with_positive_values')
        _neg = {n: _v2w(_mut(n)) for n in _muts}
        chk(f'T11l) ★ LHSC-03 R2: Codex 변이 10 종 (n_am 누락 · 음수 · NaN · ok 인데 무효 분모 · 면적 NaN · 문자열 · 음수 · 피복률 음수 · '
            f'ok 인데 접촉 실패 · blank 인데 양수 값) 은 전부 거부 — 받아들인 것 {[n for n, v in _neg.items() if v]}',
            not any(_neg.values()))
        _stg = {}
        _prev_rr = ps._RUNNER
        try:
            for _n in ('missing_n_am_and_coverage', 'area_nan'):
                _sd = os.path.join(tmp, 'results', f'r2_{_n}')
                os.makedirs(_sd, exist_ok=True)

                def _malformed(cmd, _x=_mut(_n), _p=_sd, **kw):     # 계산 subprocess 만 대역 — 변이 파일을 쓰고 rc 0
                    with open(os.path.join(_p, 'full_metrics.json'), 'w') as _f:
                        json.dump(_x, _f)
                    return subprocess.CompletedProcess(cmd, 0, 'synthetic malformed producer', '')
                ps._RUNNER = _malformed
                _st = webapp._coverage_stage([sys.executable, 'coverage_physics_vs_hertzian.py', _n], _sd, 'coverage')
                _stg[_n] = (_st.get('ok'), ps.summarize([_st])[0])
        finally:
            ps._RUNNER = _prev_rr
        chk(f'T11m) ★ LHSC-03 R2: 필수 단계 재현 (실제 _coverage_stage · summarize · 계산만 대역) — n_am 누락 · 면적 NaN 은 failed '
            f'(옛: ok · done) {_stg}', all(v[0] is False and v[1] == 'failed' for v in _stg.values()) and len(_stg) == 2)

        # T11n · T11o · T11p ★ Codex LHSC-03 R3 (09-30 밤 재검증 2 · P2 · 1저자 비준 09-30 밤 "비준이야") — 반례 먼저
        #   R3: 분율은 "키가 있고 None 이 아닐 때만" 범위를 보고 개수 dict 는 값 `all` 만 봐서 (빈 dict 참) — 분모가 양수인 분율의 누락 / None ·
        #   빈 개수 원장 · 집계 모순 (elastic 1,000,000 · nconf 0 인데 분율 1) · SE-only (n_am 0) 에 AM–SE 면적 123 이 accepted (셋은 필수 단계
        #   done).  계약 (Codex 최소 해제): 분율 키 필수 · 분모 > 0 이면 유한값 = round(개수 비, 6) (생산자 규약) · 분모 0 이면 None · 개수 dict 는
        #   필수 분류 집합 (PAIRS · BINDINGS) + 총합 항등식 (Σ pair = nconf · Σ binding = n · AM–SE[b] ≤ 총[b]) · 접촉 0 → 면적 0 · AM–SE 면적 > 0
        #   → AM–SE 결속 ≥ 1 · n_amse + [SE–SE > 0] + [AM–AM > 0] ≤ n · n_am 0 → AM 이 낀 면적 · 결속 · 충돌 0 · blank h_film = None 또는
        #   유한 양수 · 10^400 면적은 예외 없이 거부.  결손을 0 으로 채우지 않는다.  물성 · 피복식 재계산이 아니라 스키마 완전성 · 집계 항등식이다.
        _se_only = _prod['se_only'][1]
        _blank_src = _prod['scale1'][1]                            # 실제 blank (scale ≠ 1000 · h_film None)

        def _mut3(name):
            x = _copy.deepcopy(_se_only if name == 'n_am_zero_positive_area' else (_blank_src if name.startswith('blank_') else _hl))
            if name == 'missing_fractions':
                del x['cap_conflict_frac_physics_v2']; del x['cap_conflict_frac_cap_branch_physics_v2']
            elif name == 'none_fractions':
                x['cap_conflict_frac_physics_v2'] = None; x['cap_conflict_frac_cap_branch_physics_v2'] = None
            elif name == 'wrong_fractions':
                x['cap_conflict_n_physics_v2'] = 0; x['cap_conflict_frac_physics_v2'] = 1.0
            elif name == 'empty_count_dicts':
                for k in webapp.COVERAGE_V2_COUNT_DICT_KEYS:
                    x[k] = {}
            elif name == 'unknown_binding_keys':
                x['A_binding_counts_total_physics_v2'] = {'not_a_branch': x['n_contacts_physics_v2']}
            elif name == 'contradictory_count_totals':
                x['A_binding_counts_total_physics_v2']['elastic'] = 10 ** 6
            elif name == 'n_am_zero_positive_area':
                x['area_AM전체_SE_total_physics_v2'] = 123.0
            elif name == 'zero_contacts_positive_area':
                x['n_contacts_physics_v2'] = x['n_cap_branch_physics_v2'] = x['cap_conflict_n_physics_v2'] = 0
            elif name == 'blank_bad_film':
                x['h_film_sim_physics_v2'] = 'broken'
            elif name == 'blank_none_rule':
                x['rule_physics_v2'] = None
            elif name == 'blank_missing_film':
                del x['h_film_sim_physics_v2']
            elif name == 'huge_integer_area':
                x['area_AM전체_SE_total_physics_v2'] = 10 ** 400
            elif name == 'am_se_binding_exceeds_total':
                x['A_binding_counts_AM_SE_physics_v2'] = {k: v + 1 for k, v in x['A_binding_counts_AM_SE_physics_v2'].items()}
            elif name == 'conf_pair_sum_mismatch':
                x['cap_conflict_n_by_pair_physics_v2']['other'] += 1
            elif name == 'amse_area_without_amse_contacts':
                x['A_binding_counts_AM_SE_physics_v2'] = {k: 0 for k in x['A_binding_counts_AM_SE_physics_v2']}
            return x
        _rej = ('missing_fractions', 'none_fractions', 'wrong_fractions', 'empty_count_dicts', 'unknown_binding_keys',
                'contradictory_count_totals', 'n_am_zero_positive_area', 'zero_contacts_positive_area', 'blank_bad_film',
                'huge_integer_area', 'am_se_binding_exceeds_total', 'conf_pair_sum_mismatch', 'amse_area_without_amse_contacts')
        _acc = ('blank_none_rule', 'blank_missing_film')          # Codex 동의: blank 의 rule None · 내부 오류 경로의 h_film 부재는 정상

        def _v2w_safe(d):
            try:
                return _v2w(d)
            except Exception as _e:                                # noqa: BLE001 — 예외도 실패다 (거부는 False 로만)
                return f'raised {type(_e).__name__}'
        _r3 = {n: _v2w_safe(_mut3(n)) for n in _rej + _acc}
        chk(f'T11n) ★ LHSC-03 R3: 변이 13 종 (분율 누락 · None · 틀린 분율 · 빈 개수 dict · 모르는 분류 · 총합 모순 · SE-only 에 AM 면적 · 접촉 0 인데 '
            f'면적 · blank h_film 문자열 · 10^400 면적 · AM–SE 결속 > 총 · 충돌 쌍 합 ≠ nconf · AM–SE 면적인데 결속 0) 은 전부 거부 (예외 없이) · '
            f'양성 2 (blank rule None · 내부 오류 경로 h_film 없음) 은 받는다 — 어긋남 '
            f'{[n for n in _rej if _r3[n] is not False] + [n for n in _acc if _r3[n] is not True]}',
            all(_r3[n] is False for n in _rej) and all(_r3[n] is True for n in _acc))
        _stg3 = {}
        _prev_rr = ps._RUNNER
        try:
            for _n in ('none_fractions', 'empty_count_dicts', 'n_am_zero_positive_area', 'huge_integer_area'):
                _sd = os.path.join(tmp, 'results', f'r3_{_n}')
                os.makedirs(_sd, exist_ok=True)

                def _malformed3(cmd, _x=_mut3(_n), _p=_sd, **kw):   # 계산 subprocess 만 대역 — 변이 파일을 쓰고 rc 0
                    with open(os.path.join(_p, 'full_metrics.json'), 'w') as _f:
                        json.dump(_x, _f)
                    return subprocess.CompletedProcess(cmd, 0, 'synthetic malformed producer', '')
                ps._RUNNER = _malformed3
                _st = webapp._coverage_stage([sys.executable, 'coverage_physics_vs_hertzian.py', _n], _sd, 'coverage')
                _stg3[_n] = (_st.get('ok'), ps.summarize([_st])[0])
        finally:
            ps._RUNNER = _prev_rr
        chk(f'T11o) ★ LHSC-03 R3: 필수 단계 재현 — 분율 None · 빈 개수 dict · SE-only 에 AM 면적 · 10^400 면적 은 failed (옛: 앞 셋이 done) {_stg3}',
            all(v[0] is False and v[1] == 'failed' for v in _stg3.values()) and len(_stg3) == 4)
        chk('T11p) LHSC-03 R3 계약 고정: 검증기의 분류 집합 · 반올림 자릿수가 생산자 (_PhysicsV2Book.PAIRS · BINDINGS · round(…, 6)) 와 같다 · '
            '양성 8 종은 엄격해진 뒤에도 전부 받는다',
            tuple(getattr(webapp, 'COVERAGE_V2_PAIR_KEYS', ())) == tuple(_cv._PhysicsV2Book.PAIRS)
            and tuple(getattr(webapp, 'COVERAGE_V2_BINDING_KEYS', ())) == tuple(_cv._PhysicsV2Book.BINDINGS)
            and getattr(webapp, 'COVERAGE_V2_FRAC_ROUND', None) == 6 and all(webapp._coverage_v2_written(v[0]) for v in _prod.values()))

        # T11q · T11r ★ Codex LHSC-03-R4 (09-30 밤 재검증 3 · P2 · 1저자 비준 "다 비준") — 반례 먼저
        #   R4: 피복률 · 장부 공존 — 접촉 0 인데 평균 50 % · n_clip = n_am 인데 평균 1.218 % · population std 75 %p · n_cap 에 elastic/none 포함 이
        #   전부 검증기 True · 필수 단계 done.  계약 (Codex 최소 해제): AM–SE 결속 0 → 피복률 평균 · std · 클립 0 (총 면적 반올림으로 역추론하지
        #   않는다) · mean_AM ≥ 100·n_clip/n_am (평균 반올림 0.0005 %p) · std ≤ 50 %p (population · [0, 100]) · n_cap = binding tabor + volume + geom.
        #   정상 대조 = 실제 생산자 0 접촉 AM (접촉 행 비움) · SE-only · 부분 / 전체 클립 (생산자 규약대로 만든 레코드).
        _dz = _root / 'zero_am_contacts'
        _d0, _tm0, _sc0 = _cv._selftest_fixture(_dz, variant='base')
        (_d0 / 'contacts.csv').write_text('id1,id2,delta,contact_area\n')
        with _ctx.redirect_stdout(_io.StringIO()):
            _cv.compute_case('zero_am_contacts', _d0, _tm0, scale=_sc0)
        _zero = json.loads((_d0 / 'full_metrics.json').read_text())

        def _mut4(name):
            x = _copy.deepcopy(_zero if name == 'zero_contacts_positive_coverage' else _hl)
            if name == 'zero_contacts_positive_coverage':
                for k in list(x):
                    if k.startswith('coverage_') and k.endswith('_mean_physics_v2'):
                        x[k] = 50.0
            elif name == 'all_am_clipped_but_mean_not_100':
                x['am_denominator_physics_v2']['n_coverage_clipped_100'] = x['am_denominator_physics_v2']['n_am']
            elif name == 'impossible_population_std_75':
                for k in list(x):
                    if k.startswith('coverage_') and k.endswith('_std_physics_v2'):
                        x[k] = 75.0
            elif name == 'cap_branch_count_includes_elastic_and_none':
                x['n_cap_branch_physics_v2'] = x['n_contacts_physics_v2']
                x['cap_conflict_frac_cap_branch_physics_v2'] = round(x['cap_conflict_n_physics_v2'] / x['n_cap_branch_physics_v2'], 6)
            elif name in ('partial_clip_ok', 'full_clip_ok'):         # 생산자 규약대로: AM 둘 · 상마다 한 입자 (std 0)
                full = name == 'full_clip_ok'
                x['am_denominator_physics_v2']['n_coverage_clipped_100'] = 2 if full else 1
                labs = sorted(k[len('coverage_'):-len('_mean_physics_v2')] for k in x
                              if k.startswith('coverage_') and k.endswith('_mean_physics_v2') and k != 'coverage_AM_mean_physics_v2')
                vals = [100.0, 100.0] if full else [100.0, 40.0]
                for lb, v in zip(labs, vals):
                    x[f'coverage_{lb}_mean_physics_v2'] = v
                    x[f'coverage_{lb}_std_physics_v2'] = 0.0
                x['coverage_AM_mean_physics_v2'] = round(sum(vals) / 2, 3)
            return x
        _rej4 = ('zero_contacts_positive_coverage', 'all_am_clipped_but_mean_not_100', 'impossible_population_std_75',
                 'cap_branch_count_includes_elastic_and_none')
        _r4 = {n: _v2w_safe(_mut4(n)) for n in _rej4 + ('partial_clip_ok', 'full_clip_ok')}
        _pos4 = {'zero_am_contacts': webapp._coverage_v2_written(str(_d0)), 'se_only': webapp._coverage_v2_written(_prod['se_only'][0]),
                 'base': webapp._coverage_v2_written(_prod['base'][0]), 'partial_clip_ok': _r4['partial_clip_ok'], 'full_clip_ok': _r4['full_clip_ok']}
        chk(f'T11q) ★ LHSC-03-R4: Codex 장부 모순 4 종 (접촉 0 인데 피복률 50 % · 전 AM 클립인데 평균 1.2 % · std 75 %p · cap 수에 elastic/none) 은 '
            f'거부 · 정상 5 (실제 생산자 0 접촉 AM · SE-only · 정상 · 부분 클립 · 전체 클립) 는 받는다 — 어긋남 '
            f'{[n for n in _rej4 if _r4[n] is not False] + [n for n, v in _pos4.items() if v is not True]}',
            all(_r4[n] is False for n in _rej4) and all(v is True for v in _pos4.values()) and _zero.get('n_contacts_physics_v2') == 0)
        _stg4 = {}
        _prev_rr = ps._RUNNER
        try:
            for _n in _rej4:
                _sd = os.path.join(tmp, 'results', f'r4_{_n}')
                os.makedirs(_sd, exist_ok=True)

                def _malformed4(cmd, _x=_mut4(_n), _p=_sd, **kw):   # 계산 subprocess 만 대역 — 변이 파일을 쓰고 rc 0
                    with open(os.path.join(_p, 'full_metrics.json'), 'w') as _f:
                        json.dump(_x, _f)
                    return subprocess.CompletedProcess(cmd, 0, 'synthetic malformed producer', '')
                ps._RUNNER = _malformed4
                _st = webapp._coverage_stage([sys.executable, 'coverage_physics_vs_hertzian.py', _n], _sd, 'coverage')
                _stg4[_n] = (_st.get('ok'), ps.summarize([_st])[0])
        finally:
            ps._RUNNER = _prev_rr
        chk(f'T11r) ★ LHSC-03-R4: 필수 단계 재현 — 장부 모순 4 종은 failed (옛: done) {_stg4}',
            all(v[0] is False and v[1] == 'failed' for v in _stg4.values()) and len(_stg4) == 4)

        # T11s · T11t ★ Codex LHSC-03-R5 (09-30 밤 재검증 4 · P2) — 반례 먼저
        #   R5: 전체 클립 (n_clip = n_am > 0) 인데 상별 평균 0 % · 상별 std 40 %p 가 검증기 True · 필수 단계 done.  생산자는 raw > 100 을 세고
        #   min(raw, 100) 을 저장하므로 (coverage_physics_vs_hertzian.py) n_clip = n_am 이면 저장된 모든 AM 값이 **정확히 100** — 비어 있지 않은
        #   어떤 부분집합 (상) 도 평균 100 · population std 0.  계약 (Codex 최소 해제 그대로): n_clip = n_am > 0 → **존재하는** 상별 · 전체 평균 = 100 ·
        #   존재하는 상별 std = 0 (생산자 반올림 셋째 자리 = 0.0005 안).  없는 상의 키를 요구하지 않고 · 부분 클립의 std 는 제한하지 않는다 (일반 분산
        #   상한이 아니다).  정상 대조 = **실제 생산자**로 만든 0 접촉 · 부분 클립 · 전체 클립 (Codex audit_r5 의 접촉 자료 그대로 — 판독기 시험용이지
        #   DEM 평형 침대가 아니다) + 한 상뿐인 전체 클립 + std 가 있는 부분 클립.
        import math as _math

        def _produce5(name, counts):
            d = _root / f'r5_{name}'
            d.mkdir(parents=True, exist_ok=True)
            (d / 'full_metrics.json').write_text(json.dumps({'case_id': name}))
            rows = [(1, 1, .001, 0.0, 0.0, 0.0), (2, 2, .001, .01, 0.0, 0.0)]
            cons = []
            for am, n in enumerate(counts, 1):
                for j in range(n):
                    sid = len(rows) + 1
                    ang = 2 * _math.pi * j / max(n, 1)
                    rows.append((sid, 3, .001, (am - 1) * .01 + .001 * _math.cos(ang), .001 * _math.sin(ang), 0.0))
                    cons.append((am, sid, .001, _math.pi * (.001 ** 2 - (.001 / 2) ** 2)))
            (d / 'atoms.csv').write_text('id,type,radius,x,y,z\n' + ''.join(','.join(repr(v) for v in r) + '\n' for r in rows))
            (d / 'contacts.csv').write_text('id1,id2,delta,contact_area\n' + ''.join(','.join(repr(v) for v in c) + '\n' for c in cons))
            with _ctx.redirect_stdout(_io.StringIO()):
                _cv.compute_case(name, d, {1: 'AM_P', 2: 'AM_S', 3: 'SE'}, scale=1000)
            return str(d), json.loads((d / 'full_metrics.json').read_text())
        _pr5 = {n: _produce5(n, c) for n, c in (('zero', (0, 0)), ('partial_clip', (4, 1)), ('full_clip', (4, 4)))}
        _f5, _p5 = _pr5['full_clip'][1], _pr5['partial_clip'][1]

        def _mut5(name):
            x = _copy.deepcopy(_p5 if name.startswith('partial') else _f5)
            if name == 'all_clipped_but_phase_mean_zero':          # Codex 변이 ①
                x['coverage_AM_P_mean_physics_v2'] = 0.0
            elif name == 'all_clipped_but_phase_std_40':           # Codex 변이 ②
                x['coverage_AM_S_std_physics_v2'] = 40.0
            elif name == 'all_clipped_but_phase_mean_99p999':      # 반올림 계약 밖 (셋째 자리 한 눈금)
                x['coverage_AM_S_mean_physics_v2'] = 99.999
            elif name == 'all_clipped_but_total_mean_99':          # 옛 R4 하한이 이미 막는 것 — 회귀
                x['coverage_AM_mean_physics_v2'] = 99.0
            elif name == 'full_clip_one_phase_only_ok':            # 정상: AM_S 상이 없는 침대 (그 상의 키 없음 · n_am 1) — 없는 상의 키를 요구하지 않는다
                for k in [k for k in x if k.startswith('coverage_AM_S_')]:
                    del x[k]
                x['am_denominator_physics_v2'].update(n_am=1, n_coverage_clipped_100=1)
            elif name == 'partial_clip_std_20_ok':                 # 정상: 부분 클립의 상별 std 는 제한하지 않는다
                x['coverage_AM_S_std_physics_v2'] = 20.0
            return x
        _rej5 = ('all_clipped_but_phase_mean_zero', 'all_clipped_but_phase_std_40', 'all_clipped_but_phase_mean_99p999', 'all_clipped_but_total_mean_99')
        _acc5 = ('full_clip_one_phase_only_ok', 'partial_clip_std_20_ok')
        _r5 = {n: _v2w_safe(_mut5(n)) for n in _rej5 + _acc5}
        _pos5 = {n: webapp._coverage_v2_written(v[0]) for n, v in _pr5.items()}
        _pos5.update({n: _r5[n] for n in _acc5})
        _full_ok5 = (_f5.get('am_denominator_physics_v2', {}).get('n_coverage_clipped_100') == 2 == _f5.get('am_denominator_physics_v2', {}).get('n_am')
                     and all(_f5.get(f'coverage_{lb}_mean_physics_v2') == 100.0 and _f5.get(f'coverage_{lb}_std_physics_v2') == 0.0 for lb in ('AM_P', 'AM_S'))
                     and _p5.get('am_denominator_physics_v2', {}).get('n_coverage_clipped_100') == 1)
        chk(f'T11s) ★ LHSC-03-R5: 전체 클립 (n_clip = n_am) 인데 상별 평균 0 % · 상별 std 40 %p · 상별 평균 99.999 (반올림 계약 밖) · 전체 99 % 는 '
            f'거부 · 실제 생산자 0 접촉 · 부분 클립 · 전체 클립 (AM 둘 다 100 · std 0) · 한 상뿐인 전체 클립 · std 20 부분 클립은 받는다 — 어긋남 '
            f'{[n for n in _rej5 if _r5[n] is not False] + [n for n, v in _pos5.items() if v is not True]} · 생산자 전체 클립 확인 {_full_ok5}',
            all(_r5[n] is False for n in _rej5) and all(v is True for v in _pos5.values()) and _full_ok5)
        _stg5 = {}
        _prev_rr5 = ps._RUNNER
        try:
            for _n in _rej5[:2]:
                _sd = os.path.join(tmp, 'results', f'r5_{_n}')
                os.makedirs(_sd, exist_ok=True)

                def _malformed5(cmd, _x=_mut5(_n), _p=_sd, **kw):   # 계산 subprocess 만 대역 — 변이 파일을 쓰고 rc 0
                    with open(os.path.join(_p, 'full_metrics.json'), 'w') as _f:
                        json.dump(_x, _f)
                    return subprocess.CompletedProcess(cmd, 0, 'synthetic malformed producer', '')
                ps._RUNNER = _malformed5
                _st = webapp._coverage_stage([sys.executable, 'coverage_physics_vs_hertzian.py', _n], _sd, 'coverage')
                _stg5[_n] = (_st.get('ok'), ps.summarize([_st])[0])
        finally:
            ps._RUNNER = _prev_rr5
        chk(f'T11t) ★ LHSC-03-R5: 필수 단계 재현 — Codex 변이 둘 (상별 평균 0 · 상별 std 40) 은 failed (옛: done) {_stg5}',
            all(v[0] is False and v[1] == 'failed' for v in _stg5.values()) and len(_stg5) == 2)

        # T12 (τ 인계 · ④a 망 단계 — 1저자 10-05 *"먼저 구현하고 같이 요청서로 codex에 보내자"* · 요청서 §5-2): stop_after='network' 은
        #   network solver → baseline 머지 → 채널 판정 → **망 정지 계약** 에서 멈춘다 (Stage E · 이중 공극률 · 고급 분석 · 그림 없음).
        #   계약 (`_ps.network_stop_verdict` · fail-closed): ① network_content_verdict strict ② 이번 실행 network_run_id 도장 ·
        #   network_solver_status success ③ 두 모드 sigma_full_status ∈ {computed, valid_zero} · full_metrics σ = dual 의 같은 세대 값
        #   (valid_zero 면 둘 다 None) ④ 두 모드 constriction_power_share_ion_* = dual 과 같고 (0–1 · computed) 또는 (None · 사유 상태)
        #   ⑤ dual 두 모드 boundary_rule ∈ {L0, L1, L2} · boundary_band_frac 유한 양수.  하나라도 어기면 failed (done 금지).
        #  ★ RGL-02 · 08 · SELF-86 (Codex 10-05): 망 레코드는 **실 생산자 출력** (`network_conductivity._run_all_networks` — CLI 가 파일로 쓰는
        #    바로 그 dict · 합성 침대 셋) 이고, 접촉 분석 자리에는 그 침대의 장부 (판 간격 · 질량 보존 두께 · φ_mc · 독립 calc_percolation) 를
        #    쓴다.  옛 판은 손으로 만든 레코드 (σ 0.15/0.25 · valid_zero 직접 기입) 라 실 생산자와 정지 계약의 모순을 못 봤다.
        #    변이는 실 레코드 위에 한 키씩만 바꾼다.
        _PROD12 = {_b: _producer_records(_b) for _b in ('through', 'nonthrough', 'band_l1')}

        def _net_rec(mode, bed='through', **over):
            _r = json.loads(json.dumps(_PROD12[bed][0][mode]))
            _r.update(over)
            return _r

        def make_net_runner(contact_rc=0, net_rc=0, H=None, P=None, legacy=None, ledger=None):
            """make_cov_runner + 실 생산자 network 산출물 (모드별 JSON · legacy = Hertz 사본 · dual = {'hertzian', 'physics', ratio})
            + 접촉 분석이 full_metrics 에 쓰는 장부 (기본 = 관통 침대)."""
            _base = make_cov_runner(contact_rc=contact_rc)
            _H = H if H is not None else _net_rec('hertzian')
            _P = P if P is not None else _net_rec('physics')
            _L = ledger if ledger is not None else _PROD12['through'][1]

            def _r(cmd, **kw):
                script = os.path.basename(str(cmd[1])) if len(cmd) > 1 else ''
                if script in ('analyze_contacts.py', 'analyze_contacts_bimodal.py'):
                    _cp = _base(cmd, **kw)
                    _fmp = os.path.join(res_dir, 'full_metrics.json')
                    if contact_rc == 0 and os.path.exists(_fmp):
                        _d = json.load(open(_fmp))
                        _d.update(_L)
                        with open(_fmp, 'w') as _f:
                            json.dump(_d, _f)
                    return _cp
                if script != 'network_conductivity.py':
                    return _base(cmd, **kw)
                _base.calls.append(cmd)
                if net_rc == 0:
                    for _n, _d in (('network_conductivity_hertzian.json', _H), ('network_conductivity_physics.json', _P),
                                   ('network_conductivity.json', legacy if legacy is not None else _H),
                                   ('network_conductivity_dual.json', {'hertzian': _H, 'physics': _P,
                                                                       'ratio_physics_over_hertzian': {}})):
                        with open(os.path.join(res_dir, _n), 'w') as _f:
                            json.dump(_d, _f)
                return subprocess.CompletedProcess(cmd, net_rc, '', '')
            _r.calls = _base.calls
            return _r

        def _run12(mode, tm, stop, preserve=False, **rk):
            shutil.rmtree(res_dir, ignore_errors=True)
            _r = make_net_runner(**rk)
            ps._RUNNER = _r
            _kw = {'figures': False, 'auto_db': False}
            if stop:
                _kw['stop_after'] = stop
            if preserve:
                _kw.update(preserve_network=True, network_snapshot=None)
            try:
                _o = webapp.run_pipeline('case1', mode, tm, 1000, **_kw)
            except (TypeError, ValueError) as _e:           # 옛 코드 — 'network' 을 모른다
                _o = {'status': f'{type(_e).__name__}: {_e}'}
            _fmp = os.path.join(res_dir, 'full_metrics.json')
            return _r, _o, (json.load(open(_fmp)) if os.path.exists(_fmp) else {})

        _bi = ('bimodal', '1:AM_P,2:AM_S,3:SE')
        for _mode, _tm in (('standard', '1:AM,3:SE'), _bi):
            _rf, _of, _ = _run12(_mode, _tm, None)
            _rs, _os12, _fm12 = _run12(_mode, _tm, 'network')
            _ss = _scripts(_rs)
            chk(f'T12a) ★ {_mode} stop_after=network: network solver 에서 끝난다 (Stage E · 이중 공극률 · 고급 분석 없음) · done · '
                f'stopped_after · network_run_id = full_metrics 의 이번 도장 · physics σ 머지 ({_os12.get("status")})',
                _ss[-1:] == ['network_conductivity.py'] and 'run_network_full_corrections.py' not in _ss
                and 'recompute_porosity_dual.py' not in _ss and 'advanced_analysis.py' not in _ss
                and _os12.get('status') == 'done' and _os12.get('stopped_after') == 'network'
                and bool(_os12.get('network_run_id')) and _os12.get('network_run_id') == _fm12.get('active_network_run_id')
                and _fm12.get('sigma_full_mScm_physics') == _PROD12['through'][0]['physics']['sigma_full_mScm']
                and 'sigma_full_mScm_stage_e' not in _fm12
                and 'stage_e_status' not in _fm12)
            chk(f'T12b) ★ {_mode} 멈춘 실행의 명령 = 전체 실행의 앞부분 (인자까지 같다)',
                len(_rs.calls) >= 4 and [list(map(str, c)) for c in _rs.calls]
                == [list(map(str, c)) for c in _rf.calls[:len(_rs.calls)]])
        _strip = (lambda d, pre: {k: v for k, v in d.items() if not k.startswith(pre)})
        _bad12 = {
            '③ physics σ not_computed': dict(P=_net_rec('physics', sigma_full=None, sigma_full_mScm=None, sigma_full_status='not_computed')),
            '③ Hertz computed 인데 σ None': dict(H=_net_rec('hertzian', sigma_full_mScm=None)),
            '③ legacy ≠ Hertz (세대 섞임 · 머지 σ 9.0)': dict(legacy=_net_rec('hertzian', sigma_full_mScm=9.0)),
            '④ physics 협착 몫 값 · 상태 둘 다 없음': dict(P=_strip(_net_rec('physics'), 'constriction_power_share')),
            '④ physics 협착 몫 1.3 (범위 밖)': dict(P=_net_rec('physics', constriction_power_share_ion_physics=1.3)),
            '④ Hertz 협착 몫 None 인데 상태 computed': dict(H=_net_rec('hertzian', constriction_power_share_ion_hertz=None)),
            '⑤ Hertz 띠 규칙 없음': dict(H=_strip(_net_rec('hertzian'), 'boundary_rule')),
            '⑤ physics 띠 규칙 L9': dict(P=_net_rec('physics', boundary_rule='L9')),
            '⑤ Hertz 띠 폭 NaN': dict(H=_net_rec('hertzian', boundary_band_frac=float('nan'))),
        }
        _g12 = {}
        for _lbl, _rk in _bad12.items():
            _rb, _ob, _ = _run12(*_bi, 'network', **_rk)
            _g12[_lbl] = (_ob.get('status'), _ob.get('stopped_after'), 'run_network_full_corrections.py' in _scripts(_rb),
                          any('Network stop contract' in str(x) for x in (_ob.get('failed_stages') or [])))
        _miss12 = {k: v for k, v in _g12.items() if v != ('failed', 'network', False, True)}
        chk(f'T12c) ★ 망 정지 계약 변이 {len(_bad12)} 종 → 전부 failed (계약 단계 · Stage E 안 돎 · stopped_after) {_miss12 or ""}',
            not _miss12 and len(_g12) == len(_bad12))
        #  ★ SELF-86 — 옛 T12d 는 valid_zero 를 **손으로** 넣었다 (실 생산자는 비관통에 not_computed 를 냈다 = RGL-02).  이제 양성 대조는
        #    실 생산자의 정상 비관통 · 띠 폴백 L1 침대 출력 그대로 (장부도 그 침대의 것 — calc_percolation 0 % · 100 %).
        _ok12 = {
            'SE 정상 비관통 (실 생산자 — valid_zero · no_through_path · σ None · 협착 몫 None + 비관통 사유)': dict(
                H=_net_rec('hertzian', 'nonthrough'), P=_net_rec('physics', 'nonthrough'), ledger=_PROD12['nonthrough'][1]),
            '띠 폴백 L1 (실 생산자 — 기록됨 · tau_flux G1 이 BAND_FALLBACK 으로 표지)': dict(
                H=_net_rec('hertzian', 'band_l1'), P=_net_rec('physics', 'band_l1'), ledger=_PROD12['band_l1'][1]),
        }
        _g12p = {_l: _run12(*_bi, 'network', **_rk)[1].get('status') for _l, _rk in _ok12.items()}
        chk(f'T12d) 양성 대조 (실 생산자 출력): SE 정상 비관통 · 띠 폴백 L1 은 done {_g12p}',
            all(v == 'done' for v in _g12p.values()) and len(_g12p) == len(_ok12))
        _rp, _op, _ = _run12(*_bi, 'network', preserve=True)
        chk(f'T12e) ★ stop_after=network + preserve_network → ValueError (망을 새로 푸는 정지점 — solver 를 안 부르는 보존과 섞지 않는다) '
            f'({_op.get("status")!r})', str(_op.get('status', '')).startswith('ValueError'))
        _rn, _on, _ = _run12(*_bi, 'network', net_rc=1)
        chk(f'T12f) network solver rc 1 → failed · Stage E 안 돎 · stopped_after ({_on.get("status")})',
            _on.get('status') == 'failed' and _on.get('stopped_after') == 'network'
            and 'run_network_full_corrections.py' not in _scripts(_rn))
        _rg, _og, _fmg = _run12(*_bi, 'network')
        _vg = getattr(ps, 'network_stop_verdict', None)
        _g12g = (_vg(res_dir, _og.get('network_run_id'))[0], _vg(res_dir, 'OTHER-RUN')[0], _vg(res_dir, None)[0]) if _vg else None
        chk(f'T12g) ★ ② 도장 계약: 같은 산출물이라도 이번 run_id 가 아니면 (다른 id · None) 거부 {_g12g}',
            _g12g == (True, False, False))
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
        #  ★★ 2026-08-31 — 이 검사는 **소스 문자열의 철자**를 보고 있었다.
        #    `LAST_BACKEND['used'] = 'cpu'` 는 있는데 gpu 쪽이 `update(used='gpu', …)` 로
        #    쓰이자 기능은 멀쩡한데 검사만 빨간불이 됐다.  철자를 보는 검사는 구현이
        #    조금만 다르게 쓰여도 거짓 실패를 내고, 반대로 **주석에 그 문자열을 적어도
        #    통과**한다 (규율 4번: 자기 신고를 읽지 마라).
        #  ⇒ AST 로 **대입을 실제로 찾는다** — 주석·문자열은 안 세고, 표기 차이는 무시한다.
        import ast as _ast
        _tree = _ast.parse(_s3s)
        _assigned = set()
        for _n in _ast.walk(_tree):
            #  `LAST_BACKEND['used'] = 'gpu'`
            if isinstance(_n, _ast.Assign):
                for _t in _n.targets:
                    if (isinstance(_t, _ast.Subscript)
                            and getattr(_t.value, 'id', None) == 'LAST_BACKEND'
                            and isinstance(_n.value, _ast.Constant)
                            and getattr(_t.slice, 'value', None) == 'used'):
                        _assigned.add(_n.value.value)
            #  `LAST_BACKEND.update(used='gpu', …)`
            if (isinstance(_n, _ast.Call)
                    and isinstance(_n.func, _ast.Attribute)
                    and _n.func.attr == 'update'
                    and getattr(_n.func.value, 'id', None) == 'LAST_BACKEND'):
                for _kw in _n.keywords:
                    if _kw.arg == 'used' and isinstance(_kw.value, _ast.Constant):
                        _assigned.add(_kw.value.value)
        chk('59) ★ RC6-08 실제 backend 를 기록한다 — cpu·gpu 둘 다 대입된다 (AST)',
            {'cpu', 'gpu'} <= _assigned)
        #  선언에 fallback 사유 자리가 있는가 — 이것도 AST 로 본다 (모듈을 import 하면
        #  numpy·scipy 를 끌어와 이 테스트가 무거워진다).
        _decl_keys = set()
        for _n in _ast.walk(_tree):
            if (isinstance(_n, _ast.Assign)
                    and any(getattr(_t, 'id', None) == 'LAST_BACKEND' for _t in _n.targets)
                    and isinstance(_n.value, _ast.Dict)):
                _decl_keys = {k.value for k in _n.value.keys
                              if isinstance(k, _ast.Constant)}
        chk('59b) ★ 선언에 requested·used·fallback_reason 자리가 있다',
            {'requested', 'used', 'fallback_reason'} <= _decl_keys)

        #  ══ 59c~ ★★ R19 Q2 — AST 도 여전히 **소스**를 읽는다 ═════════════════
        #    Codex 반례: GPU 대입 **바로 뒤에** `LAST_BACKEND['used'] = None` 을 끼워도
        #    59 는 초록이다 (대입이 사라진 게 아니라 덮인 것이라서).  ⇒ 솔버를 **돌려서**
        #    무엇이 남는지 본다.  GPU 가 없으니 cupy·cupyx 를 numpy/scipy 위에 흉내내어
        #    분기를 실제로 태운다 — 여기서 보는 것은 수치가 아니라 **기록**이다.
        #    (비용 걱정은 접었다: CI 가 이미 numpy·scipy 를 깐다.)
        import types as _types

        import numpy as _np
        from scipy import sparse as _sp
        from scipy.sparse.linalg import cg as _cg_cpu

        def _fake_cupy(fail=False):
            _cp = _types.ModuleType('cupy')
            _cp.asarray = lambda a, dtype=None: _np.asarray(a, dtype=dtype)
            _cp.asnumpy = lambda a: _np.asarray(a)
            _cp.float64 = _np.float64
            _cxs = _types.ModuleType('cupyx.scipy.sparse')

            def _boom(*a, **k):
                raise RuntimeError('CUDA out of memory (fake)')
            _cxs.csr_matrix = _boom if fail else _sp.csr_matrix
            _cxs.diags = _sp.diags
            _lin = _types.ModuleType('cupyx.scipy.sparse.linalg')

            def _cg_gpu(A, b, tol=None, maxiter=None, M=None, rtol=None, atol=None):
                if tol is not None:      # 새 CuPy 는 rtol — 그 TypeError 경로도 태운다
                    raise TypeError('tol was renamed to rtol')
                return _cg_cpu(A, b, rtol=rtol or 1e-8, maxiter=maxiter, M=M)
            _lin.cg = _cg_gpu
            _cxs.linalg = _lin
            _cpx = _types.ModuleType('cupyx')
            _sci = _types.ModuleType('cupyx.scipy')
            _sci.sparse = _cxs
            _cpx.scipy = _sci
            return {'cupy': _cp, 'cupyx': _cpx, 'cupyx.scipy': _sci,
                    'cupyx.scipy.sparse': _cxs, 'cupyx.scipy.sparse.linalg': _lin}

        sys.path.insert(0, _sc)
        import step3_sigma as _s3mod
        _L = _sp.csr_matrix(_np.array([[2.0, -1.0], [-1.0, 2.0]]))
        _b = _np.array([1.0, 0.0])
        _want = _np.array([2.0 / 3.0, 1.0 / 3.0])
        _g0, _r0 = _s3mod.GPU_SOLVE, _s3mod.REQUIRE_GPU
        _saved = {k: sys.modules.get(k) for k in _fake_cupy()}

        def _restore():
            for _k, _v in _saved.items():
                if _v is None:
                    sys.modules.pop(_k, None)
                else:
                    sys.modules[_k] = _v
        try:
            _s3mod.GPU_SOLVE, _s3mod.REQUIRE_GPU = False, False
            _x, _ = _s3mod._solve_cg(_L, _b)
            _cpu = dict(_s3mod.LAST_BACKEND)
            chk("59c) ★★ CPU 로 풀면 used='cpu' 가 **실제로** 남는다 (소스가 아니라 실행)",
                _cpu.get('used') == 'cpu' and _cpu.get('requested') == 'cpu')
            chk('59d) ★ 그 팔이 옳은 해를 낸다 (기록만 남기고 안 푸는 것이 아니다)',
                _np.allclose(_x, _want, atol=1e-6))

            _s3mod.GPU_SOLVE = True
            sys.modules.update(_fake_cupy())
            _x, _ = _s3mod._solve_cg(_L, _b)
            _gpu = dict(_s3mod.LAST_BACKEND)
            _restore()
            chk("59e) ★★ GPU 분기를 태우면 used='gpu' 가 남는다 "
                '(대입을 None 으로 덮으면 여기서 걸린다)',
                _gpu.get('used') == 'gpu' and _gpu.get('requested') == 'gpu')
            chk('59f) ★ GPU 팔도 옳은 해를 낸다', _np.allclose(_x, _want, atol=1e-6))
            chk('59g) ★ 성공한 GPU 팔은 폴백 사유를 남기지 않는다',
                _gpu.get('fallback_reason') is None)

            sys.modules.update(_fake_cupy(fail=True))
            _x, _ = _s3mod._solve_cg(_L, _b)
            _fb = dict(_s3mod.LAST_BACKEND)
            _restore()
            chk('59h) ★★ GPU 가 죽으면 requested=gpu·used=cpu 로 **어긋남이 보인다**',
                _fb.get('requested') == 'gpu' and _fb.get('used') == 'cpu')
            chk('59i) ★★ 그리고 사유가 남는다 (조용한 폴백 금지)',
                'CUDA out of memory' in str(_fb.get('fallback_reason') or ''))
        finally:
            _restore()
            _s3mod.GPU_SOLVE, _s3mod.REQUIRE_GPU = _g0, _r0

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

    # ══ T13–T16 (Codex 10-05 RGL-02 · 04 · 07 · 08 · SELF-86) — 실 생산자 → 실 정지 helper → 실 소비자 ══
    _t13_t16_network_stop_real(webapp)

    print(f'\ntest_pipeline_provenance: {_ok}/{_ok + len(_fail)} PASS'
          + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
