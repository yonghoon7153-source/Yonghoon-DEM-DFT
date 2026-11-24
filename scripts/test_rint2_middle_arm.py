#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`scripts/rint2_middle_arm.py` 시험 — 부록 팔 등록 `docs/reviews/rint2_middle_arm_ptfe05_sdcp0_registration_20261124.md` §8 (러너 · GPU 없음).

  unshare -pf --mount-proc --kill-child python3 -I -X utf8 -B scripts/test_rint2_middle_arm.py

  T1  봉인 사슬 sha256 앞 16 자리 그대로 · 바뀐 사본은 거부 · 시험 뒤에도 바이트 그대로
  T2  env 차이 = arm 1 {SIGMA_SDCP_OVERRIDE: '0'} · arm 2 {KITS} 정확히 (봉인 R 단위 env = 사슬 runner_env_delta 를 따로 불러 대조 · 합성 계획 · 사다리)
  T3  등록 밖 override · 칸 거부 (등록 표 변이 · 사슬 env 변이 · 금지 env · 킷 이름 · 부모 셸 칸 지움)
  T4  없는 · 꼴 틀린 사다리 거부 (요약 읽기 · 사슬 load_ladders 읽기 · run 은 --out 을 만들지 않는다)
  T5  σ_SDCP 0 = SDCP 셀을 빈칸 (pore) 으로 둔 것과 같은 σ_e — step3_sigma.solve_sigma_z (작은 합성 격자 · 비트 같음 · σ_SDCP > 0 이면 달라짐)
  T6  check-mono (등록 개정 1) — 두 런 증서 띠 (사슬 arm_band) · 위반 = ① 하한 > DBE 상한 = MONO_VIOLATION · 점값 역전 + 겹침 = MONO_UNDETERMINED ·
      PATH_CUT 0 = PASS · SOLVE_FAILED · NOT_COMPUTED = 결손 (0 으로 세지 않음) · 짝 (P · R_j,0 · 원점 · 경계 · env 조립) 다름 = 비교 거부 ·
      변이 (가) 옛 한쪽 띠 규칙 · (나) PATH_CUT · SOLVE_FAILED · 칸 기록 (--record · 리포 밖 · 판정 · 띠) · 진짜 read_run = 거부 (fail-closed)
  T7  plan · run · check-mono 화면 · 매니페스트에 σ 숫자 없음
  R1–R7 run — 있는 --out 거부 · 가짜 bash 러너로 매니페스트 칸 · 러너가 받은 env · 판독 멈춤 기록 · 지금 트리 코드 관문 · NOT_COMPUTED 뒤 다음 런
  P1  Python 3.8 로 두 파일 컴파일 (있을 때)
⚠ 진짜 러너 · LIGGGHTS · MPM 을 돌리지 않는다 — 가짜 러너 · 바꿔 끼운 read_run / load_ladders / run_preflight 는 시험 이름에 적었다.
⚠ PASS = 배선 · 거부 규칙의 증거이지 물리 검증이 아니다.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
DRIVER = SCRIPTS / 'rint2_middle_arm.py'
CHAIN = SCRIPTS / 'rint_r_chain.py'
SHA_PREFIX = '5fbc1c3417f17eba'
KIT2 = 'kit_DBE_ptfe05_sdcp0_vgcf100'
RJ = {'P0': '4250000.0', 'P1': '12300000.0'}
RJ_LO = {'P0': '3000000.0', 'P1': '9000000.0'}
RJ_HI = {'P0': '6000000.0', 'P1': '20000000.0'}
LAD_SHA = {'P0': 'a1' * 32, 'P1': 'b2' * 32}
#: 시험에 넣는 σ (값 봉인 검사 T7 이 화면 · 매니페스트에서 찾는다 · 다른 글자와 겹치지 않게 고른 수)
SIG_R0 = 0.004567891234            # 사다리 R_j,0 확인 팔 σ (load_ladders 의 r0_sigma)
SIG_RUN = 0.000987654321           # 가짜 러너 · 바꿔 끼운 read_run 의 σ
SIG_DBE = 0.00187654321            # check-mono DBE 팔 σ
SIG_HI = 0.00191234567             # check-mono 위반 팔 σ
HEX40 = '9' * 40

MA = None
CH = None
TD = None
FX = {}
CHECKS = []


class Skip(Exception):
    pass


def check(name, desc):
    def deco(fn):
        CHECKS.append((name, desc, fn))
        return fn
    return deco


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


@contextlib.contextmanager
def patched(obj, name, value):
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


@contextlib.contextmanager
def env_set(**kv):
    old = {k: os.environ.get(k) for k in kv}
    for k, v in kv.items():
        os.environ[k] = v
    try:
        yield
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def run_main(argv):
    """드라이버 main 을 이 프로세스에서 → (rc, 화면)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = MA.main([str(x) for x in argv])
    return rc, buf.getvalue()


def run_cli(argv, env=None):
    """드라이버를 새 프로세스로 (-I · -B) → (rc, 화면)."""
    e = dict(os.environ if env is None else env)
    e['PYTHONDONTWRITEBYTECODE'] = '1'
    r = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', str(DRIVER)] + [str(x) for x in argv], cwd=str(ROOT), env=e,
                       capture_output=True, encoding='utf-8', errors='replace', timeout=120)
    return r.returncode, r.stdout + r.stderr


def n_lines(text, suffix):
    return sum(1 for x in text.splitlines() if x.strip().endswith(suffix))


def refused(fn, *a, **k):
    """fn → Refuse 를 내야 한다 → (code, why)."""
    try:
        fn(*a, **k)
    except MA.Refuse as e:
        return e.code, e.why
    raise AssertionError(f'거부되지 않았다: {getattr(fn, "__name__", fn)}')


def sig_forms(x):
    out = {repr(x), str(x)}
    for v in (x, x * 1e3):
        for f in ('.6g', '.5g', '.4g', '.3e', '.4e', '.6e'):
            out.add(format(v, f))
    return sorted(out)


def assert_no_sigma(text, vals, where):
    for v in vals:
        for s in sig_forms(v):
            assert s not in text, f'{where}: σ 글자 {s!r} (값 {v!r}) 가 보인다'


# ═════════════════════════ 고정물 ═════════════════════════
def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(CH.canon_bytes(obj))
    return p


def plan_obj(**over):
    ep = {'max_hours': 168, 'max_attempts': 8, 'allowed_machines': ['gabia', 'kgy'],
          'env_unit': {'python_minor': '3.8', 'numpy': '1.24.4', 'scipy': '1.10.1'}}
    ep.update(CH.EXEC_POLICY_RULES)
    p = {'schema': CH.PLAN_SCHEMA, 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.0, 'tol_ff_um': 0.07381254285530132,
         'step3_rtol': 1e-12, 'p2_extra': '--step3-maxiter 5000000', 'max_ladder_points': 16, 'calib_rj_ratio_max': 'none',
         'sv_cf_threshold': 1.5745499360744093, 'sv_cf_scope': 'all3', 'exec_policy': ep}
    p.update(over)
    return p


def noop(law):
    return {'law': law, 'rj': RJ[law], 'status': 'done', 'ok': True, 'stop': None}


def ladder_summary(law, plan, plan_sha, **over):
    s = {'tool': CH.TOOL, 'schema': CH.SCHEMA, 'stage': 'ladder', 'status': 'CALIBRATED', 'variant': None, 'law': law,
         'plan': {'sha256': plan_sha, 'content': plan}, 'ladder': {'R_j0': RJ[law], 'R_j_lo': RJ_LO[law], 'R_j_hi': RJ_HI[law]},
         'noop': noop(law)}
    s.update(over)
    return s


def make_ladders(name, mut=None):
    """사다리 시도 폴더 둘 (P0 · P1) — mut(law, 요약) 이 요약을 바꾼다 (None = 그대로)."""
    out = []
    for law in CH.LAWS:
        s = ladder_summary(law, FX['plan'], FX['plan_sha'])
        if mut is not None:
            s = mut(law, s)
        d = TD / name / f'ladder_{law}' / 'attempt_1'
        if s is not None:
            write_json(d / 'ladder_summary.json', s)
        out.append(d)
    return out


def fake_code():
    files = [{'file': n, 'sha256': hashlib.sha256(n.encode()).hexdigest()} for n in CH.CODE_FILES]
    rsha = next(f['sha256'] for f in files if f['file'] == CH.RUNNER_NAME)
    ident = {'head': HEX40, 'dirty': False, 'rel': 'scripts/rint_r_chain.py', 'error': None}
    return {'chain': dict(ident), 'runner': dict(ident, rel='scripts/' + CH.RUNNER_NAME), 'runner_path': '/x/' + CH.RUNNER_NAME,
            'files': files, 'runner_files': [dict(f) for f in files], 'runner_sha256': rsha,
            'env': {'unit': {'python_minor': '3.8', 'numpy': '1.24.4', 'scipy': '1.10.1'}, 'record_only': {}}}


def fake_lads():
    return {law: {'dir': str(TD / 'fake_lad' / law), 'summary_sha256': LAD_SHA[law], 'variant': None, 'R_j0': RJ[law],
                  'R_j_lo': RJ_LO[law], 'R_j_hi': RJ_HI[law], 'r0_sigma': SIG_R0, 'noop': noop(law)} for law in CH.LAWS}


def fake_load_ladders(dirs, variant, reg_path, contract, sid_reg, now_code=None):
    """사슬 load_ladders 자리 (원 팔이 없는 시험) — 예측 단계와 같은 꼴의 7 묶음."""
    FX.setdefault('load_calls', []).append({'dirs': list(dirs), 'variant': variant, 'reg': reg_path})
    return fake_lads(), FX['plan'], FX['plan_sha'], fake_code(), None, None, None


def arm_public(p, i, **over):
    a = {'file': Path(p).name, 'index': i, 'sha256': sha(p), 'protocol_id': 'p3ca-0123456789abcdef', 'state': 'positive', 'cg_info': 0,
         'cg_resid': 1e-13, 'imbalance': 2e-9, 'cert_pass': [True, True, True, True], 'sid_fp': 'ab' * 16, 'cg_iters': 123,
         'resolve_iters': 4, 'sv_cf_status': None, 'err_rel': 1e-6}
    a.update(over)
    return a


FAKE_RUNNER = r'''#!/usr/bin/env bash
# 시험용 가짜 러너 — env 를 적고 팔 JSON 자리만 만든다 (풀이 없음)
set -u
mkdir -p "$OUTDIR"
stem="${KITS#kit_}"
if [ -n "${ARM_LIST:-}" ]; then idx="${ARM_LIST//,/ }"; else idx="$(seq 0 $(( ${ARMS:-8} - 1 )))"; fi
env | LC_ALL=C grep -E '^(KITS|OUTDIR|SIGMA_[A-Z_]+|CJUNC[A-Z_]*|SDCP_[A-Z_]+|ARMS|ARM_LIST|MPM_NO_VENV|P2_ATTEMPT|RINT_RUN_TOKEN|LEAN|VOX|PTFE_STAMP|STEP3_RTOL|EXPECT_BACKEND)=' | LC_ALL=C sort > "$OUTDIR/runner_env.txt"
for i in $idx; do
  if printf ',%s,' "${FAKE_ZERO_ARMS:-}" | LC_ALL=C grep -q ",$i,"; then
    printf '{"step3": {"sigma_e_eff_S_cm": 0.0, "reason": "no_plate_contact (합성)", "conv_cert": {"status": "VALID_ZERO_TOPOLOGY", "zero_source": "early_return", "zero_graph": "plate_mask", "reason": "no_plate_contact (합성)"}, "manifest": {"components": {"electronic": {"status": "not_solvable"}}}}, "fake_arm": %s}\n' "$i" > "$OUTDIR/p2_${stem}_fake_a${i}.json"
  else
    printf '{"step3": {"sigma_e_eff_S_cm": 0.000987654321}, "fake_arm": %s}\n' "$i" > "$OUTDIR/p2_${stem}_fake_a${i}.json"
  fi
done
exit 0
'''


def fake_read_run_run(outdir, req, plan, contract, sid_reg, want_sha=None, s0_grid=None, s0_census=None, graph_src=None):
    """run 시험의 read_run 자리 — 가짜 러너 팔 파일 → ARM_PUBLIC + σ (값 봉인 검사용)."""
    FX.setdefault('run_reads', []).append({'name': req['name'], 'kit': req['kit'], 'man_sdcp': CH.MAN_FIXED['sigma_sdcp_S_cm'],
                                           's0_grid': s0_grid, 's0_census': s0_census, 'graph_src': graph_src})
    out = []
    for i in CH.arm_indices(req):
        p = sorted(Path(outdir).glob(f'p2_*_a{i}.json'))[0]
        out.append(dict(arm_public(p, i), sigma=SIG_RUN, target_lo=SIG_RUN * 0.9999, target_hi=SIG_RUN * 1.0001, scale=1.0, dsigma_rel=None,
                        sv_cf=None, sv_graph=None, sv_local=None, dissipation_share=None, n_sdcp_near=0))
    return out


def setup():
    global MA, CH, TD
    TD = Path(tempfile.mkdtemp(prefix='rint2_ma_'))
    spec = importlib.util.spec_from_file_location('rint2_middle_arm', str(DRIVER))
    MA = importlib.util.module_from_spec(spec)
    sys.modules['rint2_middle_arm'] = MA
    spec.loader.exec_module(MA)
    CH = MA.load_chain()
    FX['plan'] = plan_obj()
    FX['plan_file'] = write_json(TD / 'plan' / 'rint_r_plan.json', FX['plan'])
    FX['plan_sha'] = sha(FX['plan_file'])
    FX['lads'] = make_ladders('good')
    FX['root'] = TD / 'kroot'
    FX['root'].mkdir()
    FX['runner'] = TD / 'fake_runner.sh'
    FX['runner'].write_text(FAKE_RUNNER, encoding='utf-8')
    FX['reg'] = TD / 'registration_R_sealed.md'
    FX['reg'].write_text('# 시험 등록 사본 (load_ladders 를 바꿔 끼운 run 시험에서만 쓴다)\n', encoding='utf-8')
    FX['out'] = TD / 'plan_out'


# ═════════════════════════ T1 ═════════════════════════
@check('T1a', '봉인 사슬 파일 sha256 앞 16 자리 = 5fbc1c3417f17eba · 드라이버 상수 · 불러온 모듈 표지가 같다')
def t1a():
    h = sha(CHAIN)
    assert h.startswith(SHA_PREFIX), h
    assert MA.CHAIN_SHA_PREFIX == SHA_PREFIX
    assert MA.chain_sha(CH) == h
    assert Path(CH.__file__).resolve() == CHAIN.resolve()
    assert sys.modules['rint_r_chain'] is CH and callable(CH.runner_env_delta) and CH.DBE_KIT == 'kit_DBE_sdcp1um_vgcf100'
    assert MA.load_chain() is CH                           # 같은 바이트 = 다시 실행하지 않는다


@check('T1b', '한 바이트 바뀐 사슬 사본 = 거부 (CHAIN_SHA_MISMATCH · 실행 전) · 없는 파일 = CHAIN_UNREADABLE')
def t1b():
    d = TD / 't1'
    d.mkdir()
    cp = d / 'rint_r_chain.py'
    cp.write_bytes(CHAIN.read_bytes() + b'\n')
    code, why = refused(MA.load_chain, cp)
    assert code == 'CHAIN_SHA_MISMATCH' and SHA_PREFIX in why, (code, why)
    assert sys.modules['rint_r_chain'] is CH
    code, _ = refused(MA.load_chain, d / 'nope.py')
    assert code == 'CHAIN_UNREADABLE'


# ═════════════════════════ T2 ═════════════════════════
def _ref_env(cl, n, law, outdir):
    """봉인 R 단위 런의 env — 사슬 run_request · runner_env_delta 를 드라이버와 따로 부른다."""
    _nm, req, _k = CH.run_request(CH.UNIT_PREFIX, n, CH.DBE_KIT, cl['role'], law, '0', RJ[law], cl['arms'], cl['sv_cf'], None)
    return req, CH.runner_env_delta(FX['plan'], None, req, outdir)


def _unit_order(law, lads):
    """사슬 unit_runs 가 봉인 단위에 내는 런 차례 (시험 쪽 기록기)."""
    calls = []

    class Rec:
        def run(self, kit, role, law_, c, rj, arms, sv_cf=False):
            calls.append((kit, role, law_, c, rj, arms, bool(sv_cf)))
    pr = CH.Predict(None, lads, None, sv_scope=FX['plan']['sv_cf_scope'])
    CH.unit_runs(pr, Rec(), 'unit', {'law': law, 'c': '0', 'rj_role': 'R_j0'}, lads)
    return calls


@check('T2a', 'arm 1 — 런마다 env 차이 = {SIGMA_SDCP_OVERRIDE: 256.6 → 0} 정확히 · env = 사슬 runner_env_delta (봉인 R 단위 요청) + 그 칸 하나')
def t2a():
    lads = MA.ladders_summary(CH, FX['lads'])['lads']
    for law in CH.LAWS:
        cell = MA.build_cell(CH, 1, law, None, FX['plan'], lads, FX['runner'], FX['root'], FX['out'])
        order = _unit_order(law, lads)
        assert [(c['kit'], c['role'], c['law'], c['c'], c['rj'], c['arms'], c['sv_cf']) for c in (r['call'] for r in cell['runs'])] == order
        assert [r['name'] for r in cell['runs']] == ['U01_corner', 'U02_origin'], [r['name'] for r in cell['runs']]
        assert cell['kit'] == CH.DBE_KIT and cell['rj'] == RJ[law] and cell['unit'] == f'{law}_c0_R_j0'
        for n, r in enumerate(cell['runs'], 1):
            assert r['env_diff'] == {'SIGMA_SDCP_OVERRIDE': {'r_unit': '256.6', 'arm': '0'}}, r['env_diff']
            req, ref = _ref_env(r['call'], n, law, r['outdir'])
            want = dict(ref)
            want['SIGMA_SDCP_OVERRIDE'] = '0'
            assert r['env'] == want, sorted(set(r['env'].items()) ^ set(want.items()))
            assert r['req'] == req
            e = r['env']
            assert (e['KITS'], e['CJUNC_RJ'], e['CJUNC_PTFE_JLAW'], e['SDCP_MOD_C'], e['CJUNC']) == (CH.DBE_KIT, RJ[law], law, '0', '1')
            assert e['OUTDIR'] == str(FX['out'] / r['outdir'].name)
        corner, origin = (r['env'] for r in cell['runs'])
        assert corner['ARMS'] == '1' and 'ARM_LIST' not in corner and corner.get('CJUNC_SV_CF') == '1'
        assert origin['ARM_LIST'] == '1,2' and 'ARMS' not in origin and 'CJUNC_SV_CF' not in origin
        assert [r['outdir'].name for r in cell['runs']] == ['U01_corner_arm1', 'U02_origin_arm2_arml1-2']


@check('T2b', 'arm 2 — 런마다 env 차이 = {KITS: DBE 킷 → 새 킷} 정확히 · 요청 차이 = kit 하나 · σ_SDCP 칸 = 봉인 값 그대로')
def t2b():
    lads = MA.ladders_summary(CH, FX['lads'])['lads']
    for law in CH.LAWS:
        cell = MA.build_cell(CH, 2, law, KIT2, FX['plan'], lads, FX['runner'], FX['root'], FX['out'])
        assert cell['kit'] == KIT2
        for n, r in enumerate(cell['runs'], 1):
            assert r['env_diff'] == {'KITS': {'r_unit': CH.DBE_KIT, 'arm': KIT2}}, r['env_diff']
            req, ref = _ref_env(r['call'], n, law, r['outdir'])
            want = dict(ref)
            want['KITS'] = KIT2
            assert r['env'] == want
            assert r['env']['SIGMA_SDCP_OVERRIDE'] == CH.ENV_FIXED['SIGMA_SDCP_OVERRIDE'] == '256.6'
            assert {k for k in req if req[k] != r['req'][k]} == {'kit'}


@check('T2c', 'plan CLI (새 프로세스 · --ladder-check summary) — 4 칸 · 차이 줄 = 등록 칸뿐 · rc 0')
def t2c():
    rc, out = run_cli(['plan', '--ladder-check', 'summary', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--kit2', KIT2,
                       '--root', FX['root'], '--runner', FX['runner']])
    assert rc == 0, out
    assert out.count('다른 칸: SIGMA_SDCP_OVERRIDE 256.6 → 0') == 4, out
    assert out.count(f'다른 칸: KITS {CH.DBE_KIT} → {KIT2}') == 4, out
    assert 'plan = 4 칸' in out and out.count('[칸] arm') == 4
    assert all(f'CJUNC_RJ={RJ[law]}' in out for law in CH.LAWS)


@check('T2d', '--cjunc-store (사슬 Runner 의 저장본 칸) — 두 env 에 같은 CJUNC_STORE · 차이 칸 그대로 · 꼴 틀린 폴더 (상대 경로) = 거부')
def t2d():
    lads = MA.ladders_summary(CH, FX['lads'])['lads']
    st = TD / 'cjstore'
    st.mkdir(mode=0o755)
    os.chmod(str(st), 0o755)
    assert CH.cjunc_store_dir_problem(str(st)) is None, CH.cjunc_store_dir_problem(str(st))
    for arm, kit in ((1, None), (2, KIT2)):
        cell = MA.build_cell(CH, arm, 'P1', kit, FX['plan'], lads, FX['runner'], FX['root'], FX['out'], cjunc_store=str(st))
        for r in cell['runs']:
            assert r['env']['CJUNC_STORE'] == str(st) and set(r['env_diff']) == set(MA.ARM_DIFF_KEYS[arm])
    rc, out = run_main(['plan', '--ladder-check', 'summary', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--cjunc-store', 'rel/dir'])
    assert rc == 3 and 'NOT_REGISTERED' in out, out


# ═════════════════════════ T3 ═════════════════════════
@check('T3a', 'apply_override — 등록 밖 칸 · 다른 값 · arm 2 의 override · env 에 없는 칸 = UNKNOWN_OVERRIDE')
def t3a():
    env = dict(CH.ENV_FIXED, KITS=CH.DBE_KIT)
    for arm, ov in ((1, {'SIGMA_VGCF_OVERRIDE': '1'}), (1, {'SIGMA_SDCP_OVERRIDE': '5'}), (1, {}),
                    (1, {'SIGMA_SDCP_OVERRIDE': '0', 'LEAN': '3'}), (2, {'SIGMA_SDCP_OVERRIDE': '0'}), (2, {'KITS': KIT2})):
        code, _ = refused(MA.apply_override, env, ov, arm)
        assert code == 'UNKNOWN_OVERRIDE', (arm, ov, code)
    code, _ = refused(MA.apply_override, {'KITS': CH.DBE_KIT}, {'SIGMA_SDCP_OVERRIDE': '0'}, 1)
    assert code == 'UNKNOWN_OVERRIDE'
    assert MA.apply_override(env, {'SIGMA_SDCP_OVERRIDE': '0'}, 1)['SIGMA_SDCP_OVERRIDE'] == '0'
    assert env['SIGMA_SDCP_OVERRIDE'] == '256.6'           # 받은 env 를 고치지 않는다


@check('T3b', '변이 — 등록 표에 칸을 더하면 (arm 1 + LEAN) · 사슬 env 가 킷마다 다른 칸을 내면 (arm 2 + EXTRA) = ENV_DIFF (러너 전)')
def t3b():
    lads = MA.ladders_summary(CH, FX['lads'])['lads']
    with patched(MA, 'ARM_OVERRIDE', {1: {'SIGMA_SDCP_OVERRIDE': '0', 'LEAN': '3'}, 2: {}}):
        code, why = refused(MA.build_cell, CH, 1, 'P0', None, FX['plan'], lads, FX['runner'], FX['root'], FX['out'])
    assert code == 'ENV_DIFF' and 'LEAN' in why, (code, why)
    orig = CH.runner_env_delta

    def mutant(plan, variant, req, outdir):
        d = orig(plan, variant, req, outdir)
        d['EXTRA_KIT_KEY'] = req['kit']
        return d
    with patched(CH, 'runner_env_delta', mutant):
        code, why = refused(MA.build_cell, CH, 2, 'P0', KIT2, FX['plan'], lads, FX['runner'], FX['root'], FX['out'])
        assert code == 'ENV_DIFF' and 'EXTRA_KIT_KEY' in why, (code, why)
        cell = MA.build_cell(CH, 1, 'P0', None, FX['plan'], lads, FX['runner'], FX['root'], FX['out'])   # 킷 같음 = 그 칸도 같음
        assert set(cell['runs'][0]['env_diff']) == {'SIGMA_SDCP_OVERRIDE'}
    with patched(MA, 'ARM_DIFF_KEYS', {1: ('SIGMA_SDCP_OVERRIDE', 'KITS'), 2: ('KITS',)}):
        code, _ = refused(MA.build_cell, CH, 1, 'P0', None, FX['plan'], lads, FX['runner'], FX['root'], FX['out'])
        assert code == 'ENV_DIFF'                          # 빠진 칸 (등록이 바란 KITS 차이가 없다) 도 거부
    with patched(MA, 'ARM_REQ_DIFF', {1: ('kit',), 2: ('kit',)}):   # 요청 칸 대조도 산다 (env 대조와 따로 · 겹쳐 지키는 관문)
        code, why = refused(MA.build_cell, CH, 1, 'P0', None, FX['plan'], lads, FX['runner'], FX['root'], FX['out'])
        assert code == 'ENV_DIFF' and '요청 칸' in why, (code, why)


@check('T3c', '킷 이름 — arm 1 + --kit2 · arm 2 의 없음 · 빈칸 · 빗금 · DBE · SBE 킷 = NOT_REGISTERED · arm 3 · 법칙 P2 거부')
def t3c():
    lads = MA.ladders_summary(CH, FX['lads'])['lads']
    for arm, k in ((1, KIT2), (2, None), (2, 'kit_A B'), (2, 'kit_../x'), (2, 'kit_a/b'), (2, CH.DBE_KIT), (2, CH.SBE_KIT), (2, 'KIT_x'), (3, KIT2)):
        code, _ = refused(MA.resolve_kit, CH, arm, k)
        assert code == 'NOT_REGISTERED', (arm, k, code)
    code, _ = refused(MA.build_cell, CH, 1, 'P2', None, FX['plan'], lads, FX['runner'], FX['root'], FX['out'])
    assert code == 'NOT_REGISTERED'


@check('T3d', '부모 셸 env — 러너가 읽는 칸 (SIGMA_* · KITS · CJUNC_*) 은 사슬 Runner 규칙으로 지워지고 런 env 는 그대로 · SIGMA_VGCF_OVERRIDE = 거부')
def t3d():
    lads = MA.ladders_summary(CH, FX['lads'])['lads']
    par = {'PATH': os.environ.get('PATH', '/usr/bin'), 'SIGMA_SDCP_OVERRIDE': '999', 'KITS': 'kit_EVIL', 'CJUNC_RJ': '1', 'HOME': '/tmp'}
    cell = MA.build_cell(CH, 1, 'P0', None, FX['plan'], lads, FX['runner'], FX['root'], FX['out'], parent_env=par)
    assert {'SIGMA_SDCP_OVERRIDE', 'KITS', 'CJUNC_RJ'} <= set(cell['scrubbed']) and 'PATH' not in cell['scrubbed']
    assert all(r['env']['SIGMA_SDCP_OVERRIDE'] == '0' and r['env']['KITS'] == CH.DBE_KIT for r in cell['runs'])
    mid = MA.middle_runner_class(CH)(FX['runner'], FX['root'], FX['out'], FX['plan'], None, 0.0, None, arm=1, dry=True, parent_env=par)
    assert 'SIGMA_SDCP_OVERRIDE' not in mid.env_base and 'KITS' not in mid.env_base and mid.env_base['PATH'] == par['PATH']
    with env_set(SIGMA_VGCF_OVERRIDE='1'):
        rc, out = run_main(['plan', '--ladder-check', 'summary', '--ladders', *FX['lads'], '--plan', FX['plan_file']])
    assert rc == 3 and 'ENV_SIGMA_VGCF_OVERRIDE' in out, out


# ═════════════════════════ T4 ═════════════════════════
def _bad_ladders(name, mut):
    return make_ladders(name, mut)


@check('T4a', '요약 읽기 — 없는 폴더 · 꼴 틀린 JSON · 상태 · 변이 · 법칙 둘 · R_j,0 없음 · 극한 · no-op · 계획 다름 · 한 폴더 = 거부 (사유에 폴더 · 칸)')
def t4a():
    cases = {
        'missing': (lambda law, s: None if law == 'P1' else s, 'LADDER_SET', 'ladder_summary.json'),
        'not_calibrated': (lambda law, s: dict(s, status='STOPPED'), 'LADDER_NOT_CALIBRATED', 'STOPPED'),
        'variant': (lambda law, s: dict(s, variant='FIBRE'), 'LADDER_SET', 'FIBRE'),
        'two_p0': (lambda law, s: dict(s, law='P0'), 'LADDER_SET', 'P0'),
        'no_rj0': (lambda law, s: dict(s, ladder={'R_j_lo': RJ_LO[law]}), 'LADDER_SET', 'R_j,0'),
        'rj_inf': (lambda law, s: dict(s, ladder=dict(s['ladder'], R_j0='inf')), 'LADDER_SET', 'R_j,0'),
        'rj_text': (lambda law, s: dict(s, ladder=dict(s['ladder'], R_j0='4.25e6')), 'LADDER_SET', 'R_j,0'),
        'noop_bad': (lambda law, s: dict(s, noop=dict(s['noop'], ok='yes')), 'LADDER_SET', 'no-op'),
        'plan_differs': (lambda law, s: dict(s, plan=dict(s['plan'], sha256='c' * 64)) if law == 'P1' else s, 'PLAN_HASH_MISMATCH', '계획'),
        'wrong_tool': (lambda law, s: dict(s, tool='other'), 'LADDER_SET', '사다리 요약'),
    }
    for nm, (mut, want, word) in cases.items():
        dirs = _bad_ladders('t4a_' + nm, mut)
        code, why = refused(MA.ladders_summary, CH, dirs)
        assert code == want and word in why, (nm, code, why)
    d0, d1 = make_ladders('t4a_garbage')
    (d1 / 'ladder_summary.json').write_bytes(b'{"tool": "rint_r_chain", "stage": ')
    code, why = refused(MA.ladders_summary, CH, [d0, d1])
    assert code == 'LADDER_SET' and 'ladder_summary.json' in why and str(Path(d1).resolve()) in why, (code, why)
    code, _ = refused(MA.ladders_summary, CH, [d0])
    assert code == 'LADDER_SET'
    code, _ = refused(MA.ladders_summary, CH, [d0, d0])
    assert code == 'DUPLICATE_RUN'


@check('T4b', '사슬 load_ladders 읽기 (진짜 · 원 팔 없음) — 없음 · 꼴 틀림 = LADDER_SET · 상태 = LADDER_NOT_CALIBRATED · 요약만 맞는 폴더 = 코드 기록 없음 거부 · '
              '--registration 없음 = NO_REGISTRATION')
def t4b():
    d0, d1 = make_ladders('t4b_missing', lambda law, s: None if law == 'P0' else s)
    code, why = refused(MA.ladders_full, CH, [d0, d1], FX['reg'])
    assert code == 'LADDER_SET' and 'ladder_summary.json' in why, (code, why)
    d0, d1 = make_ladders('t4b_garbage')
    (d0 / 'ladder_summary.json').write_bytes(b'\xff\xfe not json')
    code, _ = refused(MA.ladders_full, CH, [d0, d1], FX['reg'])
    assert code == 'LADDER_SET'
    dirs = make_ladders('t4b_stopped', lambda law, s: dict(s, status='STOPPED'))
    code, _ = refused(MA.ladders_full, CH, dirs, FX['reg'])
    assert code == 'LADDER_NOT_CALIBRATED'
    code, why = refused(MA.ladders_full, CH, FX['lads'], FX['reg'])     # 요약 읽기는 받는 폴더 — 원 팔 · 코드 기록이 없다
    assert code == 'CODE_PIN_MISMATCH', (code, why)
    code, _ = refused(MA.ladders_full, CH, FX['lads'], None)
    assert code == 'NO_REGISTRATION'


@check('T4c', 'plan CLI — --plan sha256 ≠ 사다리 계획 = PLAN_HASH_MISMATCH · run — 없는 사다리 = rc 3 · --out 을 만들지 않는다')
def t4c():
    other = write_json(TD / 'plan2' / 'p.json', plan_obj(p2_extra='--step3-maxiter 4000000'))
    rc, out = run_main(['plan', '--ladder-check', 'summary', '--ladders', *FX['lads'], '--plan', other])
    assert rc == 3 and 'PLAN_HASH_MISMATCH' in out, out
    new = TD / 't4c_out'
    rc, out = run_main(['run', '--arm', '1', '--law', 'P0', '--ladders', TD / 'nope0', TD / 'nope1', '--plan', FX['plan_file'],
                        '--registration', FX['reg'], '--root', FX['root'], '--machine', 'kgy', '--out', new])
    assert rc == 3 and 'LADDER_SET' in out and not os.path.lexists(str(new)), out


# ═════════════════════════ T5 ═════════════════════════
@check('T5', 'σ_SDCP 0 = SDCP 셀 (sid 5) 을 빈칸 (sid 0) 으로 둔 격자와 σ_e · n_dof · 잔차 같음 (step3_sigma.solve_sigma_z · 6×6×10 · 비트) · σ_SDCP 256.6 이면 다름')
def t5():
    try:
        import numpy as np
        import step3_sigma as s3
    except Exception as e:                                 # noqa: BLE001
        raise Skip(f'numpy · step3_sigma 를 불러오지 못했다 ({type(e).__name__}: {e})')
    if not hasattr(s3, 'solve_sigma_z') or not hasattr(s3, 'electronic_sigma_table'):
        raise Skip('step3_sigma 에 작은 격자 진입점 (solve_sigma_z · electronic_sigma_table) 이 없다')
    n = (6, 6, 10)
    sid = np.full(n, 6, np.int8)                           # SE (전자 절연)
    sid[:, :, 0] = 1
    sid[:, :, -1] = 2                                      # AM 층 (판 쪽)
    sid[2, 2, 1:-1] = 3                                    # VGCF 기둥 (관통)
    sid[4, 2, 1:4] = 3
    sid[4, 2, 6:9] = 3                                     # 끊긴 VGCF …
    sid[4, 2, 4:6] = 5                                     # … 를 SDCP 가 잇는다
    sid[3, 3, 3:7] = 5                                     # SDCP 덩어리 (VGCF 옆)
    sid[0, 0, 2:4] = 7                                     # PTFE
    vox = 0.15
    kw = dict(z_top_um=n[2] * vox, z_bot_um=0.0)
    t0 = s3.electronic_sigma_table(0.0041, 0.0041, 7853.98, 10.0, 0.0)
    t1 = s3.electronic_sigma_table(0.0041, 0.0041, 7853.98, 10.0, 256.6)
    pore = sid.copy()
    pore[pore == 5] = 0
    with contextlib.redirect_stdout(io.StringIO()):
        a = s3.solve_sigma_z(sid, t0, vox, **kw)
        b = s3.solve_sigma_z(pore, t1, vox, **kw)
        c = s3.solve_sigma_z(sid, t1, vox, **kw)
    assert a['cg_info'] == 0 and b['cg_info'] == 0 and c['cg_info'] == 0
    for k in ('sigma_eff', 'n_dof', 'resid', 'n_through_dof', 'n_plate_vox'):
        assert a[k] == b[k], (k, a[k], b[k])
    assert a['sigma_eff'] > 0 and c['sigma_eff'] > a['sigma_eff'] and c['n_dof'] > a['n_dof']   # 시험이 SDCP 에 민감하다 (빈 시험 아님)


# ═════════════════════════ T6 · check-mono (등록 개정 1 · 1저자 11-24 · Codex SBD S4b) ═════════════════════════
#: 합성 침대 지문 (run_preflight 자리 · R 단위 고정물 'bed' 와 같게) — 값 아님
BED_VIEW = {'files': {'scaffold': {'sha256': 'f1' * 32, 'bytes': 1000}}, 'metrics': {'um_box_um': [10.0, 10.0, 80.0], 'thickness_um': 72.5},
            'settings_sha256': 'e2' * 32}
LINE_RE = re.compile(r'^  U0[12]_(corner|origin) arm [0-2]: (PASS|MONO_UNDETERMINED|MONO_VIOLATION|MISSING — .+)$')
_REC_N = [0]


def _band_rec(s, lo, hi):
    return {'sigma': s, 'err_rel': 1e-6, 'target_lo': lo, 'target_hi': hi, 'scale': 1.0, 'state': 'positive'}


def _zero_rec():
    return {'sigma': 0.0, 'err_rel': 0.0, 'target_lo': None, 'target_hi': None, 'scale': None, 'state': 'zero'}


def _base():
    return _band_rec(SIG_DBE, SIG_DBE * 0.99999, SIG_DBE * 1.00001)


def ent(state, rec=None, why=None):
    return {'state': state, 'rec': rec, 'why': why}


def P(rec):
    return ent(MA.ARM_POS, rec)


def _runs(entries):
    return {'U01_corner': {'role': 'corner', 'idx': [0], 'arms': {0: entries[0]}},
            'U02_origin': {'role': 'origin', 'idx': [1, 2], 'arms': {1: entries[1], 2: entries[2]}}}


def verdicts(rows):
    return [r['verdict'] for r in rows]


def old_one_sided(d_rec, m_rec):
    """옛 규칙 (한쪽 띠만 · 시험 쪽 대조용) — ① 점값 > DBE 띠 위끝 이면 위반 (① 증서 띠를 보지 않는다)."""
    return Fraction(m_rec['sigma']) > CH.arm_band(d_rec)[1]


@check('T6a', '개정 1 단조 판정 (mono_compare · 두 런 다 사슬 arm_band) — 같은 값 · 아래 · DBE 큼 = PASS · 점값 역전 + 구간 겹침 = MONO_UNDETERMINED · '
              '① 하한 > DBE 상한 = MONO_VIOLATION · DBE PATH_CUT + ① 양수 = 위반 · 칸에 두 띠 · 꼴 · 상태 어긋남 거부')
def t6a():
    base = _base()
    below = _band_rec(SIG_DBE * 0.9, SIG_DBE * 0.89999, SIG_DBE * 0.90001)
    inv_in = _band_rec(SIG_DBE * 1.000005, SIG_DBE * 0.999995, SIG_DBE * 1.000015)
    hi_ = _band_rec(SIG_HI, SIG_HI * 0.99999, SIG_HI * 1.00001)
    dbe = _runs([P(base)] * 3)
    rows = MA.mono_compare(CH, dbe, _runs([P(base)] * 3))
    assert verdicts(rows) == ['PASS'] * 3 and [(r['run'], r['arm']) for r in rows] == [('U01_corner', 0), ('U02_origin', 1), ('U02_origin', 2)]
    assert all(r['dbe']['band'] == CH.arm_band(base) and r['arm1']['band'] == CH.arm_band(base) and r['missing'] is None for r in rows)
    assert verdicts(MA.mono_compare(CH, dbe, _runs([P(below), P(inv_in), P(hi_)]))) == ['PASS', 'MONO_UNDETERMINED', 'MONO_VIOLATION']
    assert verdicts(MA.mono_compare(CH, _runs([P(hi_)] * 3), _runs([P(base)] * 3))) == ['PASS'] * 3          # 방향 (DBE 가 크면 PASS)
    cut = ent(MA.ARM_CUT, _zero_rec())
    assert verdicts(MA.mono_compare(CH, _runs([cut, P(base), cut]), _runs([P(base), P(base), cut]))) == ['MONO_VIOLATION', 'PASS', 'PASS']
    assert MA.mono_overall(rows)[0] == 'PASS'
    code, _ = refused(MA.mono_compare, CH, dbe, {'U01_corner': dbe['U01_corner']})
    assert code == 'RUN_SET'
    code, _ = refused(MA.mono_compare, CH, dbe, _runs([P(base), P(dict(base, target_lo=None)), P(base)]))
    assert code == 'ARM_UNREADABLE'
    code, _ = refused(MA.mono_compare, CH, dbe, _runs([ent(MA.ARM_POS, _zero_rec()), P(base), P(base)]))   # 상태 이름 ↔ 사슬 기록 상태
    assert code == 'ARM_STATE'


@check('T6f', '변이 (가) — 옛 규칙 (한쪽 띠만: ① 점값 vs DBE 위끝) 이 위반으로 잘못 잡는 "점값 역전 · 구간 겹침" = 새 규칙 MONO_UNDETERMINED (멈추지 않음) · '
              '① 하한 > DBE 상한 = MONO_VIOLATION (멈춤 · 보고)')
def t6f():
    base = _base()
    over = _band_rec(SIG_DBE * 1.00002, SIG_DBE * 1.000005, SIG_DBE * 1.00003)
    assert old_one_sided(base, over) is True                                   # 옛 규칙 = 위반 (잘못)
    assert CH.arm_band(over)[0] <= CH.arm_band(base)[1]                        # 두 증서 구간이 겹친다 (고정물 확인)
    rows = MA.mono_compare(CH, _runs([P(base)] * 3), _runs([P(over), P(base), P(base)]))
    assert verdicts(rows) == ['MONO_UNDETERMINED', 'PASS', 'PASS'] and MA.mono_overall(rows)[0] == 'NO_VIOLATION'
    sep = _band_rec(SIG_DBE * 1.0001, SIG_DBE * 1.00005, SIG_DBE * 1.00015)
    assert old_one_sided(base, sep) is True and CH.arm_band(sep)[0] > CH.arm_band(base)[1]
    rows = MA.mono_compare(CH, _runs([P(base)] * 3), _runs([P(sep), P(base), P(base)]))
    assert verdicts(rows) == ['MONO_VIOLATION', 'PASS', 'PASS'] and MA.mono_overall(rows)[0] == 'MONO_VIOLATION'
    assert rows[0]['arm1']['band'] == CH.arm_band(sep) and rows[0]['dbe']['band'] == CH.arm_band(base)   # 띠 = 두 쪽 다 같은 함수


@check('T6g', '변이 (나) — PATH_CUT 0 (VALID_ZERO_TOPOLOGY) = 정상 통과 PASS (결손 아님 · 띠 [0, 0]) · SOLVE_FAILED · NOT_COMPUTED = 결손 MISSING (0 으로 세지 않음 · '
              'PASS 에 안 든다 · 띠 없음) · DBE · 양쪽 결손 사유 · 비교 없음 = NO_COMPARISON')
def t6g():
    base = _base()
    cut = ent(MA.ARM_CUT, _zero_rec())
    fail = ent(MA.ARM_FAIL, None, '① NOT_COMPUTED — 수렴 계약 unconv (합성)')
    nc = ent(MA.ARM_NC, None, '① NOT_COMPUTED (ELECTRODE_SHORT) (합성)')
    rows = MA.mono_compare(CH, _runs([P(base)] * 3), _runs([cut, fail, nc]))
    assert verdicts(rows) == ['PASS', 'MISSING', 'MISSING'], verdicts(rows)
    assert rows[0]['arm1']['state'] == MA.ARM_CUT and rows[0]['arm1']['band'] == (0, 0) and rows[0]['missing'] is None
    assert rows[1]['missing'] == {'arm1': 'SOLVE_FAILED'} and rows[1]['arm1']['band'] is None and rows[1]['dbe']['band'] == CH.arm_band(base)
    assert rows[2]['missing'] == {'arm1': 'NOT_COMPUTED'}
    ov, cnt = MA.mono_overall(rows)
    assert ov == 'NO_VIOLATION' and cnt == {'PASS': 1, 'MONO_UNDETERMINED': 0, 'MONO_VIOLATION': 0, 'MISSING': 2}, (ov, cnt)
    rows = MA.mono_compare(CH, _runs([fail, P(base), nc]), _runs([P(base), P(base), fail]))
    assert verdicts(rows) == ['MISSING', 'PASS', 'MISSING'] and rows[0]['missing'] == {'dbe': 'SOLVE_FAILED'}
    assert rows[2]['missing'] == {'dbe': 'NOT_COMPUTED', 'arm1': 'SOLVE_FAILED'}
    assert MA.mono_overall(MA.mono_compare(CH, _runs([fail] * 3), _runs([P(base)] * 3)))[0] == 'NO_COMPARISON'


def _fake_unit(law, base, mut=None):
    """봉인 R 단위 시도 폴더 고정물 (사슬 run_request · record_outdir 로 요청 칸 · 팔 파일 sha256 = arms_read · 침대 = BED_VIEW)."""
    d = base / 'units' / 'attempt_7'
    runs = []
    for n, (role, arms, sv_cf) in enumerate((('corner', 1, True), ('origin', CH.ORIGIN_ARMS, False)), 1):
        _nm, req, _k = CH.run_request(CH.UNIT_PREFIX, n, CH.DBE_KIT, role, law, '0', RJ[law], arms, sv_cf, None)
        od = d / CH.record_outdir(dict(req))
        ar = []
        for i in CH.arm_indices(req):
            p = od / f'p2_{CH.DBE_KIT[4:]}_dbe_a{i}.json'
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps({'fake_dbe_arm': i}), encoding='utf-8')
            ar.append(arm_public(p, i))
        runs.append(dict(req, outdir=od.name, rc=0, seconds=1.0, arms_read=ar, machine='kgy', group_cause=None))
    nm = f'{law}_c0_R_j0'
    s = {'tool': CH.TOOL, 'schema': CH.SCHEMA, 'stage': 'unit', 'status': 'UNIT_DONE', 'stop': None, 'flags': [],
         'attempt': {'n': 7, 'target': f'unit:{nm}', 'machine': 'kgy', 'resume_of': None, 'ledger': '/x/ledger', 'ledger_commit': HEX40},
         'resume': None, 'machine': 'kgy', 'code': fake_code(), 'variant': None, 'kit': CH.DBE_KIT,
         'unit': {'kind': 'unit', 'name': nm, 'target': f'unit:{nm}', 'law': law, 'c': '0', 'rj_role': 'R_j0'},
         'ladders': {L: {'dir': f'/x/{L}', 'summary_sha256': LAD_SHA[L], 'variant': None, 'R_j0': RJ[L], 'R_j_lo': RJ_LO[L],
                         'R_j_hi': RJ_HI[L]} for L in CH.LAWS},
         'plan': {'sha256': FX['plan_sha'], 'content': FX['plan']}, 's0_plan': None, 's0_reports': None, 'after_main': None,
         'sv_cf': {'scope': 'all3', 'threshold': FX['plan']['sv_cf_threshold']},
         'bed': {CH.SBE_KIT: dict(BED_VIEW, settings_sha256='d3' * 32), CH.DBE_KIT: BED_VIEW}, 'checks': None, 'origin': None,
         'env_scrubbed': [], 'sv_graph_source': None, 'runs': runs}
    if mut is not None:
        s = mut(s)
    write_json(d / 'unit_summary.json', s)
    return d


def _mono_reader(bands, stops=None):
    """check-mono 의 read_run 자리 — 폴더 (DBE · arm 1) · 런 이름 · 팔 → 합성 띠 기록 (stops = 그 런에서 낼 사슬 Stop) · 기록 sha256 대조 ·
    MAN_FIXED σ_SDCP 기대값 · 문맥 (sid_reg · S0 씨앗 · 계약) 기록."""
    def rd(outdir, req, plan, contract, sid_reg, want_sha=None, s0_grid=None, s0_census=None, graph_src=None):
        od = Path(outdir)
        tag = 'a1' if (od.parent / MA.MANIFEST).exists() else 'dbe'
        FX.setdefault('mono_reads', []).append((tag, req['name'], CH.MAN_FIXED['sigma_sdcp_S_cm']))
        FX.setdefault('mono_ctx', []).append((id(sid_reg), repr(s0_grid), repr(s0_census), type(contract).__name__))
        files = {int(p.name.rsplit('_a', 1)[1][:-5]): p for p in od.glob('p2_*.json')}
        idx = CH.arm_indices(req)
        assert [sha(files[i]) for i in idx] == list(want_sha), 'want_sha'
        if stops and (tag, req['name']) in stops:
            raise stops[(tag, req['name'])]
        return [dict(bands[(tag, req['name'], i)], index=i, file=files[i].name) for i in idx]
    return rd


def _bands(a1_over=None):
    b = {}
    for tag in ('dbe', 'a1'):
        for nm, idx in (('U01_corner', [0]), ('U02_origin', [1, 2])):
            for i in idx:
                b[(tag, nm, i)] = _base()
    b.update(a1_over or {})
    return b


def arm1_run(name, read=None):
    """arm 1 run 하나 (가짜 러너 · 바꿔 끼운 load_ladders · run_preflight · read_run) → (rc, 화면, out)."""
    out = TD / name
    FX['run_reads'] = []
    pre = lambda *a, **k: {'code': fake_code(), 'bed': {CH.DBE_KIT: BED_VIEW}, 'bed_diff_vs_dbe': []}   # noqa: E731
    with patched(CH, 'load_ladders', fake_load_ladders), patched(MA, 'run_preflight', pre), patched(CH, 'read_run', read or fake_read_run_run):
        rc, txt = run_main(['run', '--arm', '1', '--law', 'P0', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--registration', FX['reg'],
                            '--root', FX['root'], '--machine', 'kgy', '--runner', FX['runner'], '--out', out])
    return rc, txt, out


def mono_cli(dbe, a1, reader=None, record=None):
    """check-mono CLI (이 프로세스) → (rc, 화면, 칸 기록 경로) — reader = read_run 자리 (None = 진짜 사슬 read_run) · 칸 기록 = TD 안 새 파일."""
    if record is None:
        _REC_N[0] += 1
        record = TD / 'records' / f'mono_{_REC_N[0]}.json'
    argv = ['check-mono', '--dbe', dbe, '--arm1', a1, '--record', record]
    if reader is None:
        rc, out = run_main(argv)
    else:
        with patched(CH, 'read_run', reader):
            rc, out = run_main(argv)
    return rc, out, record


def _not_computed_read(name, arm, reason=None):
    """run 시험의 read_run 자리 — 그 런만 사슬 Stop NOT_COMPUTED (그 팔 파일 이름으로 시작하는 사유 · reason = 구조화 사유) · 나머지 = 합성 기록."""
    def rd(outdir, req, *a, **k):
        if req['name'] == name:
            raise CH.Stop('NOT_COMPUTED', f'p2_{CH.DBE_KIT[4:]}_fake_a{arm}.json: 해 상태 (§5-0) 합성 실패', req['name'], reason=reason)
        return fake_read_run_run(outdir, req, *a, **k)
    return rd


def _zero_corner_read(outdir, req, *a, **k):
    """run · check-mono 의 read_run 자리 — U01_corner arm 0 = 영값 위상 (zero · σ 0 · e 0) · 나머지 = 합성 기록."""
    recs = fake_read_run_run(outdir, req, *a, **k)
    if req['name'] == 'U01_corner':
        recs[0].update(state='zero', sigma=0.0, err_rel=0.0, target_lo=None, target_hi=None, scale=None, cert_pass=[True, True, True, False])
    return recs


@check('T6b', 'check-mono CLI (봉인 R 단위 고정물 · R2 꼴 arm 1 런 · read_run = 합성 띠) — 같은 값 = PASS (3/3) rc 0 · 만든 위반 = 그 팔 MONO_VIOLATION rc 1 · '
              '점값 역전 + 겹침 = MONO_UNDETERMINED · NO_VIOLATION rc 0 · arm 1 판독 동안만 MAN_FIXED σ_SDCP = 0 · sid_reg 하나')
def t6b():
    rc, txt, a1 = arm1_run('t6_arm1')
    assert rc == 0, txt
    dbe = _fake_unit('P0', TD / 't6_dbe')
    FX['mono_reads'], FX['mono_ctx'] = [], []
    rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands()))
    assert rc == 0 and 'overall: PASS (3/3)' in out and n_lines(out, ': PASS') == 3, out
    assert len(FX['mono_ctx']) == 4 and len(set(FX['mono_ctx'])) == 1 and FX['mono_ctx'][0][3] == 'RealContract', FX['mono_ctx']   # sid_reg 하나 (DBE ↔ arm 1)
    assert sorted(FX['mono_reads']) == sorted([('dbe', 'U01_corner', 256.6), ('dbe', 'U02_origin', 256.6), ('a1', 'U01_corner', 0.0),
                                                ('a1', 'U02_origin', 0.0)]), FX['mono_reads']
    assert CH.MAN_FIXED['sigma_sdcp_S_cm'] == 256.6
    FX['mono_outs'] = [out]
    viol = {('a1', 'U02_origin', 2): _band_rec(SIG_HI, SIG_HI * 0.99999, SIG_HI * 1.00001)}
    rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands(viol)))
    assert rc == 1 and 'U02_origin arm 2: MONO_VIOLATION' in out and 'overall: MONO_VIOLATION' in out and n_lines(out, ': PASS') == 2, out
    FX['mono_outs'].append(out)
    und = {('a1', 'U01_corner', 0): _band_rec(SIG_DBE * 1.000005, SIG_DBE * 0.999995, SIG_DBE * 1.000015)}
    rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands(und)))
    assert rc == 0 and 'U01_corner arm 0: MONO_UNDETERMINED' in out and 'overall: NO_VIOLATION' in out, out
    FX['mono_outs'].append(out)
    FX['t6'] = (dbe, a1)


@check('T6d', '변이 (나) CLI — ① 모서리 판독 NOT_COMPUTED (구조화 사유 없음) = SOLVE_FAILED 결손 · ① origin ELECTRODE_SHORT (a1) = NOT_COMPUTED · 같은 런 a2 = 판독 중단 결손 · '
              '결손을 PASS · 0 으로 세지 않음 · 다시 읽기 ≠ run 기록 = REPLAY_MISMATCH')
def t6d():
    if 't6' not in FX:
        raise AssertionError('T6b 가 먼저 돌아야 한다')
    dbe = FX['t6'][0]
    rc, txt, a1 = arm1_run('t6d_fail', read=_not_computed_read('U01_corner', 0))
    assert rc == 0, txt
    cause0 = f'p2_{CH.DBE_KIT[4:]}_fake_a0.json: 해 상태 (§5-0) 합성 실패'
    rc, out, rp = mono_cli(dbe, a1, _mono_reader(_bands(), {('a1', 'U01_corner'): CH.Stop('NOT_COMPUTED', cause0, 'U01_corner')}))
    assert rc == 0 and 'U01_corner arm 0: MISSING — ① SOLVE_FAILED' in out and n_lines(out, ': PASS') == 2, out
    assert 'overall: NO_VIOLATION' in out and 'MISSING 1' in out, out
    rec = json.loads(Path(rp).read_text(encoding='utf-8'))
    a0 = rec['arms'][0]
    assert a0['verdict'] == 'MISSING' and a0['arm1']['state'] == 'SOLVE_FAILED' and a0['arm1']['band'] is None and a0['dbe']['band'] is not None
    FX['mono_outs'].append(out)
    rc, txt, a1s = arm1_run('t6d_short', read=_not_computed_read('U02_origin', 1, reason=CH.SHORT_STATUS))
    assert rc == 0, txt
    cause1 = f'p2_{CH.DBE_KIT[4:]}_fake_a1.json: 해 상태 (§5-0) 합성 실패'
    st1 = CH.Stop('NOT_COMPUTED', cause1, 'U02_origin', reason=CH.SHORT_STATUS)
    rc, out, rp = mono_cli(dbe, a1s, _mono_reader(_bands(), {('a1', 'U02_origin'): st1}))
    assert rc == 0 and 'U01_corner arm 0: PASS' in out, out
    assert 'U02_origin arm 1: MISSING — ① NOT_COMPUTED' in out and 'U02_origin arm 2: MISSING — ① NOT_COMPUTED' in out, out
    rec = json.loads(Path(rp).read_text(encoding='utf-8'))
    assert CH.SHORT_STATUS in rec['arms'][1]['arm1']['why'] and 'a1' in rec['arms'][2]['arm1']['why'], rec['arms']
    FX['mono_outs'].append(out)
    st_other = CH.Stop('NOT_COMPUTED', cause0, 'U01_corner', reason=CH.SHORT_STATUS)     # run 기록 = 사유 없음 (SOLVE_FAILED) · 다시 읽기 = 단락
    rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands(), {('a1', 'U01_corner'): st_other}))
    assert rc == 3 and 'REPLAY_MISMATCH' in out, out
    rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands()))                              # run 때 멈춘 런이 지금 읽힘
    assert rc == 3 and 'REPLAY_MISMATCH' in out, out


@check('T6p', 'PATH_CUT CLI — ① 모서리 = VALID_ZERO_TOPOLOGY (팔 JSON 의 증서 · 성분 기록 대조 · 영값 출처 기록) = PASS · 칸 기록 띠 [0, 0] · '
              '판독은 zero 인데 팔 증서가 영값이 아니면 PATH_CUT_UNCONFIRMED 거부')
def t6p():
    if 't6' not in FX:
        raise AssertionError('T6b 가 먼저 돌아야 한다')
    dbe, a1_pos = FX['t6']
    with env_set(FAKE_ZERO_ARMS='0'):
        rc, txt, a1 = arm1_run('t6p_zero', read=_zero_corner_read)
    assert rc == 0, txt
    zb = _bands({('a1', 'U01_corner', 0): _zero_rec()})
    rc, out, rp = mono_cli(dbe, a1, _mono_reader(zb))
    assert rc == 0 and 'U01_corner arm 0: PASS' in out and 'overall: PASS (3/3)' in out, out
    rec = json.loads(Path(rp).read_text(encoding='utf-8'))
    s1 = rec['arms'][0]['arm1']
    assert s1['state'] == 'PATH_CUT' and (Fraction(s1['band']['lo_exact']), Fraction(s1['band']['hi_exact'])) == (0, 0), s1
    assert s1['zero'] == {'status': CH.REG_STATES['zero'][0], 'zero_source': 'early_return', 'zero_graph': 'plate_mask',
                          'reason': 'no_plate_contact (합성)', 'component': 'not_solvable'}, s1
    FX['mono_outs'].append(out)
    rc, out, _rp = mono_cli(dbe, a1_pos, _mono_reader(zb))          # 판독 = zero · 팔 JSON = 양수 꼴 (영값 증서 없음)
    assert rc == 3 and 'PATH_CUT_UNCONFIRMED' in out, out


@check('T6c', 'check-mono 비교 거부 (사유 · rc 3) — R_j,0 · 사다리 sha · 계획 · 런 · 침대 · env 조립 다름 = PAIR_MISMATCH · 단위 꼴 · STOPPED · UNIT_DONE 인데 판독 실패 기록 = '
              'REPLAY_MISMATCH · 매니페스트 RUNNING · 구조 멈춤 (SID_GRID) · 진짜 read_run (가짜 팔) · 거부도 칸 기록 (띠 없음)')
def t6c():
    if 't6' not in FX:
        raise AssertionError('T6b 가 먼저 돌아야 한다')
    dbe, a1 = FX['t6']
    rd = _mono_reader(_bands())
    fid = lambda r: dict(r, arms_read=[{k: x[k] for k in CH.ARM_FILE_ID_KEYS} for x in r['arms_read']])   # noqa: E731
    for nm, mut, want in (
            ('rj', lambda s: dict(s, ladders=dict(s['ladders'], P0=dict(s['ladders']['P0'], R_j0='5000000.0'))), 'PAIR_MISMATCH'),
            ('ladsha', lambda s: dict(s, ladders=dict(s['ladders'], P1=dict(s['ladders']['P1'], summary_sha256='d' * 64))), 'PAIR_MISMATCH'),
            ('plan', lambda s: dict(s, plan=dict(s['plan'], sha256='e' * 64)), 'PAIR_MISMATCH'),
            ('runs', lambda s: dict(s, runs=s['runs'][:1]), 'PAIR_MISMATCH'),
            ('bed', lambda s: dict(s, bed=dict(s['bed'], **{CH.DBE_KIT: dict(BED_VIEW, settings_sha256='0' * 64)})), 'PAIR_MISMATCH'),
            ('law', lambda s: dict(s, unit=dict(s['unit'], rj_role='R_j_hi', name='P0_c0_R_j_hi', target='unit:P0_c0_R_j_hi'),
                                   attempt=dict(s['attempt'], target='unit:P0_c0_R_j_hi')), 'UNIT_SUMMARY'),
            ('status', lambda s: dict(s, status='STOPPED', stop={'code': 'RUNNER_RC'}), 'UNIT_SUMMARY'),
            ('arms_read', lambda s: dict(s, runs=[fid(s['runs'][0])] + s['runs'][1:]), 'REPLAY_MISMATCH')):
        d = _fake_unit('P0', TD / f't6c_{nm}', mut)
        rc, out, rp = mono_cli(d, a1, rd)
        assert rc == 3 and want in out, (nm, out)
    rec = json.loads(Path(rp).read_text(encoding='utf-8'))                 # 거부도 칸 기록 — 짝 · 사유 · 띠 없음
    assert rec['pairing']['ok'] is False and rec['pairing']['code'] == 'REPLAY_MISMATCH' and rec['arms'] == [] and rec['overall'] == 'REFUSED', rec
    rc, out, _rp = mono_cli(TD / 'nowhere', a1, rd)
    assert rc == 3 and 'UNIT_SUMMARY' in out
    m = json.loads((a1 / MA.MANIFEST).read_text(encoding='utf-8'))
    for nm, mm, want in (('running', dict(m, status='RUNNING'), 'MANIFEST'),
                         ('env', dict(m, runs=[dict(m['runs'][0], env=dict(m['runs'][0]['env'], LEAN='3'))] + m['runs'][1:]), 'PAIR_MISMATCH')):
        a1b = TD / f't6c_a1_{nm}'
        shutil.copytree(str(a1), str(a1b))
        write_json(a1b / MA.MANIFEST, mm)
        rc, out, _rp = mono_cli(dbe, a1b, rd)
        assert rc == 3 and want in out, (nm, out)
    sid = CH.Stop('SID_GRID', 'kit|vox=0.15|yield=False|origin=1 의 sid 지문이 앞 런과 다르다 (합성)', 'U02_origin')
    rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands(), {('a1', 'U02_origin'): sid}))
    assert rc == 3 and '거부 [SID_GRID]' in out and 'MISSING' not in out, out   # 구조 멈춤 = 결손으로 세지 않고 비교 거부 (그 이름 그대로)
    rc, out, _rp = mono_cli(dbe, a1)                                            # 진짜 read_run — 가짜 팔 파일은 사슬 계약을 못 지난다
    assert rc == 3 and any(f'거부 [{c}]' in out for c in ('ARM_UNREADABLE', 'GENERATION', 'REJECTED_MARKER', 'ARM_JSON_COUNT')), out


@check('T6h', '봉인 R 단위 NOT_COMPUTED (모서리 판독 SOLVE_FAILED · origin 런 없음) — DBE 쪽 결손 셋 · 비교 없음 = NO_COMPARISON rc 3 · 칸 기록에 사유')
def t6h():
    if 't6' not in FX:
        raise AssertionError('T6b 가 먼저 돌아야 한다')
    _dbe, a1 = FX['t6']
    cause = f'p2_{CH.DBE_KIT[4:]}_dbe_a0.json: 수렴 계약 unconv (합성)'

    def mut(s):
        r0 = dict(s['runs'][0], arms_read=[{k: x[k] for k in CH.ARM_FILE_ID_KEYS} for x in s['runs'][0]['arms_read']])
        return dict(s, status='NOT_COMPUTED', stop={'code': 'NOT_COMPUTED', 'what': 'x', 'cause': cause, 'run': 'U01_corner', 'reason': None},
                    runs=[r0])
    d = _fake_unit('P0', TD / 't6h', mut)
    rc, out, rp = mono_cli(d, a1, _mono_reader(_bands(), {('dbe', 'U01_corner'): CH.Stop('NOT_COMPUTED', cause, 'U01_corner')}))
    assert rc == 3 and 'overall: NO_COMPARISON' in out, out
    assert 'U01_corner arm 0: MISSING — DBE SOLVE_FAILED' in out and 'U02_origin arm 1: MISSING — DBE NOT_COMPUTED' in out, out
    rec = json.loads(Path(rp).read_text(encoding='utf-8'))
    assert rec['overall'] == 'NO_COMPARISON' and rec['counts']['MISSING'] == 3 and all(a['dbe']['band'] is None for a in rec['arms'])
    FX['mono_outs'].append(out)


@check('T6e', '칸 기록 (--record · 리포 밖 · 등록 개정 1 덧붙임) — 팔마다 판정 · 결손 사유 · 두 띠 (사슬 arm_band 정확 분수) · 짝 · 규칙 · 낱말 "고정 기하 벌크 전도 대조" · '
              '리포 안 · 있는 파일 = 거부 (쓰지 않음) · --record 없음 = 인자 오류 · 두 폴더에 파일을 더하지 않는다 · 화면에는 값 없음')
def t6e():
    if 't6' not in FX:
        raise AssertionError('T6b 가 먼저 돌아야 한다')
    dbe, a1 = FX['t6']
    before = sorted(str(p) for p in list(Path(dbe).rglob('*')) + list(Path(a1).rglob('*')))
    und_rec = _band_rec(SIG_DBE * 1.000005, SIG_DBE * 0.999995, SIG_DBE * 1.000015)
    rc, out, rp = mono_cli(dbe, a1, _mono_reader(_bands({('a1', 'U01_corner', 0): und_rec})))
    assert rc == 0, out
    rec = json.loads(Path(rp).read_text(encoding='utf-8'))
    assert rec['tool'] == MA.TOOL and rec['schema'] == MA.MONO_SCHEMA and rec['label'] == MA.MONO_LABEL and '고정 기하 벌크 전도 대조' in rec['label']
    assert rec['pairing'] == {'ok': True} and rec['overall'] == 'NO_VIOLATION' and rec['unit'] == 'P0_c0_R_j0' and rec['rj'] == RJ['P0']
    assert rec['counts'] == {'PASS': 2, 'MONO_UNDETERMINED': 1, 'MONO_VIOLATION': 0, 'MISSING': 0}, rec['counts']
    assert [(a['run'], a['arm'], a['verdict']) for a in rec['arms']] == [('U01_corner', 0, 'MONO_UNDETERMINED'), ('U02_origin', 1, 'PASS'),
                                                                         ('U02_origin', 2, 'PASS')]
    b1, b0 = rec['arms'][0]['arm1']['band'], rec['arms'][0]['dbe']['band']
    assert (Fraction(b1['lo_exact']), Fraction(b1['hi_exact'])) == CH.arm_band(und_rec)
    assert (Fraction(b0['lo_exact']), Fraction(b0['hi_exact'])) == CH.arm_band(_base())
    assert '리포 밖' in rec['value_seal'] and rec['chain_sha256'] == sha(CHAIN)
    after = sorted(str(p) for p in list(Path(dbe).rglob('*')) + list(Path(a1).rglob('*')))
    assert before == after
    inrepo = MA.HERE.parent / 'docs' / 'reviews' / '_rint2_middle_arm_record_should_not_exist.json'   # 실행기가 아는 리포 (= ROOT)
    try:
        rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands()), record=inrepo)
        wrote = inrepo.exists()
    finally:
        if inrepo.exists():                                   # 고장 난 실행기가 썼어도 리포에 남기지 않는다
            inrepo.unlink()
    assert rc == 3 and 'RECORD_IN_REPO' in out and not wrote, out
    other = TD / 'other_checkout'                              # 다른 git 작업 트리 (조상에 .git) — 봉인 체크아웃 · 리포 사본
    (other / '.git').mkdir(parents=True)
    deep = other / 'sub' / 'mono.json'
    rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands()), record=deep)
    assert rc == 3 and 'RECORD_IN_REPO' in out and str(other) in out and not deep.exists() and not deep.parent.exists(), out
    rc, out, _rp = mono_cli(dbe, a1, _mono_reader(_bands()), record=rp)
    assert rc == 3 and 'RECORD_EXISTS' in out, out
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            MA.main(['check-mono', '--dbe', str(dbe), '--arm1', str(a1)])
        raise AssertionError('--record 없이 돌았다')
    except SystemExit as e:
        assert e.code == 2


# ═════════════════════════ R · run ═════════════════════════
@check('R1', 'run — 있는 --out (빈 폴더도) = OUTDIR_EXISTS rc 3 · 그 폴더에 아무것도 쓰지 않는다')
def r1():
    ex = TD / 'r1_exists'
    ex.mkdir()
    rc, out = run_main(['run', '--arm', '1', '--law', 'P0', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--registration', FX['reg'],
                        '--root', FX['root'], '--machine', 'kgy', '--out', ex])
    assert rc == 3 and 'OUTDIR_EXISTS' in out and list(ex.iterdir()) == [], out


def _env_dump(p):
    return dict(line.split('=', 1) for line in Path(p).read_text(encoding='utf-8').splitlines() if '=' in line)


@check('R2', 'run arm 1 (가짜 러너 · 바꿔 끼운 load_ladders · run_preflight · read_run) — rc 0 · 매니페스트 칸 (사슬 sha · env 차이 · 킷 · 법칙 · R_j 출처 · 팔 · '
             '시각 · rc · 팔 파일 sha256) · 러너가 받은 env · MAN_FIXED 바꿈은 판독 동안만')
def r2():
    rc, txt, out = arm1_run('r2_arm1')
    assert rc == 0, txt
    m = json.loads((out / MA.MANIFEST).read_text(encoding='utf-8'))
    assert m['tool'] == MA.TOOL and m['schema'] == MA.SCHEMA and m['status'] == 'DONE' and m['stop'] is None
    assert m['chain']['sha256'] == sha(CHAIN) and m['driver']['sha256'] == sha(DRIVER) and m['runner']['sha256'] == sha(FX['runner'])
    assert (m['arm'], m['law'], m['c'], m['rj_role'], m['rj'], m['kit']) == (1, 'P0', '0', 'R_j0', RJ['P0'], CH.DBE_KIT)
    assert m['override'] == {'SIGMA_SDCP_OVERRIDE': '0'} and m['plan']['sha256'] == FX['plan_sha']
    assert {L: (v['summary_sha256'], v['R_j0']) for L, v in m['ladders'].items()} == {L: (LAD_SHA[L], RJ[L]) for L in CH.LAWS}
    assert m['ladders']['P0']['summary_file'].endswith('ladder_summary.json') and m['ladder_check'] == 'full'
    assert m['start_utc'] and m['end_utc'] and m['machine'] == 'kgy' and m['max_hours'] == 168
    assert [r['name'] for r in m['runs']] == ['U01_corner', 'U02_origin'] and [r['read']['status'] for r in m['runs']] == ['ok', 'ok']
    for r, idx in zip(m['runs'], ([0], [1, 2])):
        assert r['rc'] == 0 and r['group_cause'] is None and r['arm_indices'] == idx
        assert r['env_diff'] == {'SIGMA_SDCP_OVERRIDE': {'r_unit': '256.6', 'arm': '0'}}
        assert r['group']['confirmed'] is True and r['group']['bound'] is True and r['group']['started_utc'] and r['group']['ended_utc']
        od = out / r['outdir']
        assert [a['index'] for a in r['arm_files']] == idx
        for a in r['arm_files']:
            assert a['sha256'] == sha(od / a['file'])
        kind, why = CH.arms_read_kind(r['arms_read'], r)
        assert kind == 'verified', (kind, why)
        assert all('sigma' not in a for a in r['arms_read'])
        env = _env_dump(od / 'runner_env.txt')
        assert env['SIGMA_SDCP_OVERRIDE'] == '0' and env['KITS'] == CH.DBE_KIT and env['CJUNC_RJ'] == RJ['P0']
        assert env['MPM_NO_VENV'] == '1' and env['P2_ATTEMPT'] == '1' and len(env['RINT_RUN_TOKEN']) == 32 and env['OUTDIR'] == str(od)
        assert (env.get('ARMS'), env.get('ARM_LIST'), env.get('CJUNC_SV_CF')) == (('1', None, '1') if idx == [0] else (None, '1,2', None))
    reads = FX['run_reads']
    assert [(x['name'], x['kit'], x['man_sdcp']) for x in reads] == [('U01_corner', CH.DBE_KIT, 0.0), ('U02_origin', CH.DBE_KIT, 0.0)], reads
    assert all(x['s0_grid'] == {} and x['s0_census'] == {} and x['graph_src'] is None for x in reads)
    assert CH.MAN_FIXED['sigma_sdcp_S_cm'] == 256.6
    assert FX['load_calls'][-1]['variant'] is None and FX['load_calls'][-1]['reg'] == str(FX['reg'])
    FX['r2'] = (txt, (out / MA.MANIFEST).read_text(encoding='utf-8'))


@check('R3', 'run arm 2 — 러너 env KITS = 새 킷 · SIGMA_SDCP_OVERRIDE = 봉인 256.6 · 판독 MAN_FIXED 그대로 · 차이 칸 = KITS · arm 2 에 --kit2 없음 = 거부')
def r3():
    out = TD / 'r3_arm2'
    FX['run_reads'] = []
    pre = lambda *a, **k: {'code': fake_code(), 'bed': {KIT2: {'files': {}}}, 'bed_diff_vs_dbe': ['역할 scaffold']}   # noqa: E731
    with patched(CH, 'load_ladders', fake_load_ladders), patched(MA, 'run_preflight', pre), patched(CH, 'read_run', fake_read_run_run):
        rc, txt = run_main(['run', '--arm', '2', '--law', 'P1', '--kit2', KIT2, '--ladders', *FX['lads'], '--plan', FX['plan_file'],
                            '--registration', FX['reg'], '--root', FX['root'], '--machine', 'gabia', '--runner', FX['runner'], '--out', out])
        assert rc == 0, txt
        rc2, txt2 = run_main(['run', '--arm', '2', '--law', 'P1', '--ladders', *FX['lads'], '--plan', FX['plan_file'],
                              '--registration', FX['reg'], '--root', FX['root'], '--machine', 'gabia', '--runner', FX['runner'], '--out', TD / 'r3_nokit'])
    assert rc2 == 3 and 'NOT_REGISTERED' in txt2 and not (TD / 'r3_nokit').exists(), txt2
    m = json.loads((out / MA.MANIFEST).read_text(encoding='utf-8'))
    assert m['kit'] == KIT2 and m['override'] == {} and m['rj'] == RJ['P1'] and m['bed_diff_vs_dbe'] == ['역할 scaffold']
    for r in m['runs']:
        assert r['env_diff'] == {'KITS': {'r_unit': CH.DBE_KIT, 'arm': KIT2}} and r['kit'] == KIT2
        env = _env_dump(out / r['outdir'] / 'runner_env.txt')
        assert env['KITS'] == KIT2 and env['SIGMA_SDCP_OVERRIDE'] == '256.6' and env['CJUNC_RJ'] == RJ['P1'] and env['CJUNC_PTFE_JLAW'] == 'P1'
        assert all(a['file'].startswith('p2_DBE_ptfe05_sdcp0_vgcf100_') for a in r['arm_files'])
    assert [x['man_sdcp'] for x in FX['run_reads']] == [256.6, 256.6] and all(x['s0_grid'] is None for x in FX['run_reads'])
    # 기계 · 시간 관문
    with patched(CH, 'load_ladders', fake_load_ladders):
        rc, txt = run_main(['run', '--arm', '1', '--law', 'P0', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--registration', FX['reg'],
                            '--root', FX['root'], '--machine', 'v100', '--runner', FX['runner'], '--out', TD / 'r3_mach'])
    assert rc == 3 and 'MACHINE_NOT_ALLOWED' in txt and not (TD / 'r3_mach').exists(), txt


@check('R4', 'run — 첫 런 판독이 멈추면 (사슬 Stop) 매니페스트 STOPPED · 멈춤 이름 · 그 런 arms_read = 파일 신원 · 다음 런 없음 · rc 3')
def r4():
    out = TD / 'r4_stop'

    def stop_read(outdir, req, *a, **k):
        raise CH.Stop('MANIFEST_MISMATCH', f'{req["name"]}: sigma_sdcp_S_cm 꼴 (시험)', req['name'])
    pre = lambda *a, **k: {'code': fake_code(), 'bed': {}, 'bed_diff_vs_dbe': []}   # noqa: E731
    with patched(CH, 'load_ladders', fake_load_ladders), patched(MA, 'run_preflight', pre), patched(CH, 'read_run', stop_read):
        rc, txt = run_main(['run', '--arm', '1', '--law', 'P0', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--registration', FX['reg'],
                            '--root', FX['root'], '--machine', 'kgy', '--runner', FX['runner'], '--out', out])
    assert rc == 3 and 'MANIFEST_MISMATCH' in txt, txt
    m = json.loads((out / MA.MANIFEST).read_text(encoding='utf-8'))
    assert m['status'] == 'STOPPED' and m['stop']['code'] == 'MANIFEST_MISMATCH' and m['end_utc']
    r0, r1_ = m['runs']
    assert r0['rc'] == 0 and CH.arms_read_kind(r0['arms_read'], r0)[0] == 'file_ids' and r0['arm_files']
    assert r1_['rc'] is None and r1_['arms_read'] == [] and not (out / r1_['outdir']).exists()
    assert r0['read'] == {'status': 'stopped', 'stop': m['stop']} and r1_['read'] == {'status': 'not_run'}, (r0.get('read'), r1_.get('read'))
    assert CH.MAN_FIXED['sigma_sdcp_S_cm'] == 256.6


@check('R7', '개정 1 — run 은 판독 NOT_COMPUTED (등록 결과) 뒤에도 다음 런을 돈다 · 런마다 read 칸 (ok · not_computed + SOLVE_FAILED | NOT_COMPUTED) · '
             '매니페스트 DONE · 멈춤 없음 · rc 0')
def r7():
    rc, txt, out = arm1_run('r7_fail', read=_not_computed_read('U01_corner', 0))
    assert rc == 0, txt
    m = json.loads((out / MA.MANIFEST).read_text(encoding='utf-8'))
    assert m['status'] == 'DONE' and m['stop'] is None and [r['read']['status'] for r in m['runs']] == ['not_computed', 'ok'], m['runs']
    r0, r1_ = m['runs']
    assert r0['read']['state'] == 'SOLVE_FAILED' and r0['read']['stop']['code'] == 'NOT_COMPUTED' and r0['read']['stop']['reason'] is None, r0['read']
    assert r0['rc'] == 0 and CH.arms_read_kind(r0['arms_read'], r0)[0] == 'file_ids'
    assert r1_['rc'] == 0 and CH.arms_read_kind(r1_['arms_read'], r1_)[0] == 'verified' and (out / r1_['outdir']).is_dir()
    rc, txt, out = arm1_run('r7_short', read=_not_computed_read('U01_corner', 0, reason=CH.SHORT_STATUS))
    assert rc == 0, txt
    m = json.loads((out / MA.MANIFEST).read_text(encoding='utf-8'))
    assert m['runs'][0]['read']['state'] == 'NOT_COMPUTED' and m['runs'][0]['read']['stop']['reason'] == CH.SHORT_STATUS, m['runs'][0]['read']
    assert m['status'] == 'DONE' and m['runs'][1]['read']['status'] == 'ok'


@check('R5', 'run — 진짜 run_preflight (지금 트리 · 바꿔 끼운 load_ladders 의 코드 기록) = CODE_PIN_MISMATCH (고친 트리 · 다른 코드 파일 지문) · 킷 없음 = KIT_MISSING · '
             '--out 을 만들지 않는다')
def r5():
    with patched(CH, 'load_ladders', fake_load_ladders):
        rc, txt = run_main(['run', '--arm', '1', '--law', 'P0', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--registration', FX['reg'],
                            '--root', FX['root'], '--machine', 'kgy', '--runner', FX['runner'], '--out', TD / 'r5_nokit'])
        assert rc == 3 and 'KIT_MISSING' in txt and not (TD / 'r5_nokit').exists(), txt
        (FX['root'] / CH.DBE_KIT).mkdir(exist_ok=True)
        rc, txt = run_main(['run', '--arm', '1', '--law', 'P0', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--registration', FX['reg'],
                            '--root', FX['root'], '--machine', 'kgy', '--runner', FX['runner'], '--out', TD / 'r5_code'])
    assert rc == 3 and 'CODE_PIN_MISMATCH' in txt and not (TD / 'r5_code').exists(), txt


@check('R6', 'run_preflight (사슬 code_record 를 바꿔 끼움) — dirty · HEAD 미확인 · 코드 파일 지문 다름 · 환경 판 다름 = CODE_PIN_MISMATCH · 다 같으면 침대 관문 '
             '(arm 1 = bed_problem · arm 2 = kit_bed · 가짜 킷 = S0_REPORT_MISMATCH) · arm 2 침대 지문 = DBE 대비 다른 역할 기록')
def r6():
    L = {'code': fake_code(), 's0reps': None}
    (FX['root'] / CH.DBE_KIT).mkdir(exist_ok=True)
    (FX['root'] / KIT2).mkdir(exist_ok=True)

    def variant(fn):
        c = fake_code()
        fn(c)
        return lambda runner: c
    cases = (('dirty', lambda c: c['chain'].update(dirty=True), '고쳐진'),
             ('head', lambda c: c['runner'].update(head=None, error='not a git repository'), 'HEAD'),
             ('files', lambda c: [c[k][3].update(sha256='0' * 64) for k in ('files', 'runner_files')], c_name(3)),
             ('env', lambda c: c['env']['unit'].update(numpy='2.4.6'), 'numpy'))
    for nm, fn, word in cases:
        with patched(CH, 'code_record', variant(fn)):
            code, why = refused(MA.run_preflight, CH, 1, CH.DBE_KIT, FX['plan'], L, FX['runner'], FX['root'])
        assert code == 'CODE_PIN_MISMATCH' and word in why, (nm, code, why)
    with patched(CH, 'code_record', lambda runner: fake_code()):
        code, why = refused(MA.run_preflight, CH, 1, CH.DBE_KIT, FX['plan'], L, FX['runner'], FX['root'])
        assert code == 'S0_REPORT_MISMATCH', (code, why)                         # 코드 관문을 지나 침대 관문 (S0 기록 없음 · 빈 킷)
        code, why = refused(MA.run_preflight, CH, 2, KIT2, FX['plan'], L, FX['runner'], FX['root'])
        assert code == 'S0_REPORT_MISMATCH', (code, why)
        view = {'files': {'scaffold': {'sha256': '1' * 64, 'bytes': 9}}, 'metrics': {'um_box_um': None, 'thickness_um': None}, 'settings_sha256': None}
        with patched(CH, 'kit_bed', lambda root, kit: view):
            got = MA.run_preflight(CH, 2, KIT2, FX['plan'], L, FX['runner'], FX['root'])
        assert got['bed'] == {KIT2: view} and got['bed_diff_vs_dbe'] == ['역할 scaffold'] and got['code']['files'] == L['code']['files'], got


def c_name(i):
    return CH.CODE_FILES[i]


# ═════════════════════════ T7 · 값 봉인 ═════════════════════════
@check('T7', '값 봉인 — plan (load_ladders 의 r0_sigma 가 있는 꼴) · run 화면 · 매니페스트 · check-mono 화면 (PASS · MONO_UNDETERMINED · MONO_VIOLATION · MISSING · '
             'NO_COMPARISON) 에 σ 숫자 없음 · check-mono = 팔마다 판정 줄과 overall 뿐 (띠 = 리포 밖 칸 기록에만)')
def t7():
    with patched(CH, 'load_ladders', fake_load_ladders):
        rc, out = run_main(['plan', '--ladders', *FX['lads'], '--plan', FX['plan_file'], '--registration', FX['reg'], '--kit2', KIT2])
    assert rc == 0 and 'plan = 4 칸' in out, out
    vals = (SIG_R0, SIG_RUN, SIG_DBE, SIG_HI)
    assert_no_sigma(out, vals, 'plan')
    if 'r2' not in FX or len(FX.get('mono_outs') or []) < 7:
        raise AssertionError('R2 · T6b · T6d · T6p · T6h 가 먼저 돌아야 한다')
    txt, man = FX['r2']
    assert_no_sigma(txt, vals, 'run 화면')
    assert_no_sigma(man, vals, 'run 매니페스트')
    for i, o in enumerate(FX['mono_outs']):
        assert_no_sigma(o, vals, f'check-mono 화면 {i}')
        lines = [x for x in o.splitlines() if x.strip()]
        assert lines[0].startswith('check-mono ') and lines[-1].startswith('overall: '), lines
        assert all(LINE_RE.match(x) for x in lines[1:-1]), lines


# ═════════════════════════ P1 · Python 3.8 ═════════════════════════
def _py38():
    c = os.environ.get('KGY_PY38') or shutil.which('python3.8')
    for p in ([c] if c else []) + [os.path.expanduser('~/.local/bin/python3.8')]:
        if p and os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


@check('P1', 'Python 3.8 (kgy 판) 로 드라이버 · 시험 두 파일 컴파일 · 3.9+ 함수 (removeprefix · nextafter · functools.cache) 를 쓰지 않는다')
def p1():
    src = DRIVER.read_text(encoding='utf-8')
    for bad in ('.removeprefix(', '.removesuffix(', 'math.nextafter(', 'functools.cache', 'import tomllib', 'zip(strict', 'match '):
        assert bad not in src, bad
    py = _py38()
    if py is None:
        raise Skip('python3.8 없음 (KGY_PY38 · PATH · ~/.local/bin) — 컴파일 대조 건너뜀')
    r = subprocess.run([py, '-I', '-B', '-c', 'import sys\nfor f in sys.argv[1:]:\n    compile(open(f, encoding="utf-8").read(), f, "exec")\n',
                        str(DRIVER), str(Path(__file__).resolve())], capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stderr[-800:]


# ═════════════════════════ 돌리기 ═════════════════════════
def main():
    t0 = time.time()
    h0 = sha(CHAIN)
    try:
        setup()
    except Exception:                                       # noqa: BLE001 — 시험 먼저 (드라이버가 없으면 전부 FAIL)
        traceback.print_exc()
        print(f'FAIL — 준비 실패 ({len(CHECKS)} 시험 못 돔)')
        return 1
    res = []
    try:
        for name, desc, fn in CHECKS:
            t = time.time()
            try:
                fn()
                st, why = 'PASS', ''
            except Skip as e:
                st, why = 'SKIP', str(e)
            except (Exception, SystemExit) as e:            # noqa: BLE001 — argparse 의 SystemExit 도 실패로 센다 (시험 전체가 끊기지 않게)
                st, why = 'FAIL', f'{type(e).__name__}: {e}\n' + ''.join(traceback.format_exc().splitlines(True)[-6:])
            res.append((name, st))
            print(f'{st:4}  {name:4}  {time.time() - t:5.2f} s  {desc}' + (f'\n        {why}' if why else ''))
    finally:
        shutil.rmtree(str(TD), ignore_errors=True)
    if sha(CHAIN) != h0:
        res.append(('T1z', 'FAIL'))
        print('FAIL  T1z  봉인 사슬 파일이 시험 중 바뀌었다')
    n = {k: sum(1 for _n, s in res if s == k) for k in ('PASS', 'FAIL', 'SKIP')}
    print(f'== {n["PASS"]} PASS · {n["FAIL"]} FAIL · {n["SKIP"]} SKIP · {time.time() - t0:.1f} s · 사슬 sha256 {h0[:16]}… 그대로')
    return 1 if n['FAIL'] else 0


if __name__ == '__main__':
    sys.exit(main())
