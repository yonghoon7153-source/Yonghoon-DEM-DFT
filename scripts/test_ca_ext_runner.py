#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② B6 — 러너 `scripts/sdcp_gain_vox015_8arm.sh` 의 다음 세대 손잡이 (시험 먼저 · 2026-10-20).

정본 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §7 (러너 · 영수증 · LEAN 표) · §4-3 · §5-2 (동시 거부) ·
§6 (수렴 증서) · `run_contract` (`ca_ext_request_problem` · `receipt_match` · `next_gen_cert_ok`).
러너에 selftest · 건식 모드가 없다 → **셸을 실제로 부르는** 시험이다:
  · 가짜 `python3` (PATH 맨 앞) — 규율 관문 둘 (`check_method_discipline` 90 s · `check_undefined_names`) 만 건너뛰고 (둘은 따로 게이트),
    payload argv 를 NUL 로 기록한 뒤 진짜 python 으로 넘긴다 → **명령줄 대조** (러너가 실제로 만든 인자 그대로)
  · 침대 = `test_ca_ext_b6.make_fixture` (직렬 VGCF 사슬 · DBE 에 SDCP 점 하나 · vox 1.0) 를 킷 둘 (kit_SBE · kit_DBE) 로 세운다
  · payload 는 진짜로 돈다 (CPU · 팔 하나 1 s 안팎) → 팔 JSON · fresh check_arm (receipt_match) · 수렴 증서까지 실물

  python3 scripts/test_ca_ext_runner.py                    # 전부
  python3 scripts/test_ca_ext_runner.py --only N2,N6       # 이름 접두로 고르기
  python3 scripts/test_ca_ext_runner.py --old-runner PATH  # NB — 끔 경로: 고치기 전 러너와 payload argv · 영수증 바이트 · OUTDIR · 팔 이름 대조

묶음:
  N0  정적 — bash -n · 손잡이 표 (`run_contract.RUNNER_CA_EXT_ENV`) ↔ 선언 칸 정본 · 러너가 표의 이름을 읽는다 · P2_EXTRA 의 rtol = 러너 축
  N1  끔 (기본) — 옛 팔 이름 · 영수증 · payload 인자 그대로 (끔 경로 지킴이)
  N2  탄소 접합 + rtol — payload 인자 · `--expect-physics` ca_ext 칸 · 영수증 요청 · 팔 이름 태그 · p3ca · check_arm · 수렴 증서
  N3  + SDCP 수정자 c = 1 (DBE 근접 1 · SBE 판별 표지 False)
  N4  face_alpha + rtol (LEAN 2) · N5 face_alpha + rtol (LEAN 3 · 이온 증서)
  N6  발사 전 거부 (구조화 사유 · 디렉터리를 만들지 않는다) · N6b payload 도 같은 조합을 거부한다 (러너 거부 ⊆ payload 거부 = 과잉차단 없음)
  N7  OUTDIR · 팔 태그 — 다른 요청 = 다른 이름 · 같은 물리 (표기만 다름) = 같은 이름 (무손실 · 정규) · 선언 칸 · 인자 꼴
  N8  SKIP 캐시 함정 — 옛 팔이 있는 OUTDIR 을 명시해도 옛 팔을 재사용 · 삭제하지 않는다 (CLAUDE.md Lee 절의 함정)
  N9  규율 검사기 격리 — 부모 셸의 새 축 env 가 규칙 L 탐침을 오염시키지 않는다 (격리 목록에서 빼면 오염 = 판별력)
  NB  (--old-runner) 끔 경로 — 고치기 전 러너와 같은 payload argv · 영수증 바이트 · OUTDIR 이름 · 팔 이름 · 매니페스트
⚠ PASS 는 배선 · 계약의 증거이지 R_j 값 · 판정 (R) 의 물리 검증이 아니다.
"""
import argparse
import contextlib
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
RUNNER = os.path.join(SCRIPTS, 'sdcp_gain_vox015_8arm.sh')
MARKER = 'RUNNER' + '_CONFIG_END'                       # 러너의 설정부 끝 표지 (문자열을 이 파일에 통째로 두지 않는다)

import test_ca_ext_b6 as B6                            # noqa: E402 — 침대 · payload 호출 (사본 없음)
import run_contract as RC                              # noqa: E402

ARGS = None
_ok, _fail = 0, []
CASES = []
TD = None                                              # 시험 세션 임시 디렉터리
SHIMDIR = None


def chk(name, cond, why=''):
    global _ok
    cond = bool(cond)
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


def case(tag):
    def deco(fn):
        CASES.append((tag, fn))
        return fn
    return deco


# ═════════════════════════ 공용 — 가짜 python3 · 킷 · 러너 호출 ═════════════════════════
SHIM = r'''#!/usr/bin/env bash
# 가짜 python3 (Rint ② B6 러너 시험) — 규율 관문 둘만 건너뛰고 payload argv 를 NUL 로 남긴 뒤 진짜 python 으로 넘긴다.
case "${1:-}" in
  */check_method_discipline.py|*/check_undefined_names.py)
    echo "[shim] $(basename "$1") 건너뜀 (게이트는 따로 돈다)"; exit 0;;
  */mpm_webapp_payload.py)
    printf '%s\0' "$@" > "$SHIM_LOG/payload_argv.$$"
    if [ -n "${SHIM_PAYLOAD_EXIT:-}" ]; then exit "$SHIM_PAYLOAD_EXIT"; fi;;
esac
exec "__REAL__" "$@"
'''

KIT_SH = r'''#!/usr/bin/env bash
# 시험 킷 (Rint ② B6 러너 시험) — 생산 킷의 payload 호출부 꼴 (python3 … mpm_webapp_payload … --out mpm_payload.json)
python3 "$SCR/mpm_webapp_payload.py" --scaffold am.csv --se se.npy --phase phase.npy --fibre fibre.npy \
  --fibre-dia fibre_dia.npy --n-vox 24 "${PSIG[@]}" \
  --out mpm_payload.json
'''

CJ_ENV = {'CJUNC': '1', 'CJUNC_RJ': '1e6', 'CJUNC_LEN_LAW': 'len_scaled_v0', 'CJUNC_UNREG_LAW': 'cut',
          'CJUNC_S_MIN_UM': '0.5', 'CJUNC_TOL_FF_UM': '0.5', 'CJUNC_PTFE_JLAW': 'P0'}
CJ_REQ = {'R_j_ohm': 1e6, 'len_law': 'len_scaled_v0', 'unreg_law': 'cut', 's_min_um': 0.5, 'tol_ff_um': 0.5, 'ptfe_jlaw': 'P0'}
NEW_ENV_NAMES = ('CJUNC', 'CJUNC_RJ', 'CJUNC_LEN_LAW', 'CJUNC_UNREG_LAW', 'CJUNC_S_MIN_UM', 'CJUNC_TOL_FF_UM', 'CJUNC_PTFE_JLAW',
                 'SDCP_MOD_C', 'STEP3_RTOL')
#: 러너 축 이름꼴 — 부모 셸에서 물려받지 않게 기본 env 에서 걷어낸다
_AXIS_PREFIX = ('SIGMA_', 'SDCP_', 'PTFE_', 'CJUNC', 'STEP3_', 'MPM_', 'P2_')
_AXIS_EXACT = ('LEAN', 'VOX', 'ARMS', 'KITS', 'FIBRE_STAMP', 'BRIDGE_UM', 'OUTDIR', 'EXPECT_PROTOCOL', 'EXPECT_BACKEND',
               'VIRTUAL_ENV')


def base_env(**over):
    e = {k: v for k, v in os.environ.items() if not k.startswith(_AXIS_PREFIX) and k not in _AXIS_EXACT}
    e.update(PATH=SHIMDIR + os.pathsep + os.environ.get('PATH', '/usr/bin:/bin'), MPM_NO_VENV='1',
             PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONIOENCODING='utf-8',
             VOX='1.0', ARMS='1', LEAN='2', PTFE_STAMP='off', EXPECT_BACKEND='cpu')
    for k, v in over.items():
        if v is None:
            e.pop(k, None)
        else:
            e[k] = str(v)
    return e


def make_ws(name):
    ws = os.path.join(TD, name)
    os.makedirs(ws)
    for kit, sdcp in (('kit_SBE', False), ('kit_DBE', True)):
        run = os.path.join(ws, kit, 'run_1')
        os.makedirs(run)
        B6.make_fixture(run, sdcp=sdcp)
        with open(os.path.join(ws, kit, 'run_mpm.sh'), 'w', encoding='utf-8') as f:
            f.write(KIT_SH)
        os.symlink('run_1', os.path.join(ws, kit, 'latest_run'))
    os.makedirs(os.path.join(ws, '_shim'))
    return ws


class Run:
    pass


def run_runner(ws, env_over=None, runner=None, payload_exit=None, timeout=1200):
    """러너를 진짜로 부른다 → rc · 로그 · OUTDIR · 영수증 · 팔 이름 · payload argv (--out 별) · 생성 스크립트."""
    env = base_env(**(env_over or {}))
    env['SHIM_LOG'] = os.path.join(ws, '_shim')
    env['P2_SCR'] = SCRIPTS                             # 고치기 전 러너 사본 (리포 밖 경로) 도 같은 scripts/ 를 쓴다
    if payload_exit is not None:
        env['SHIM_PAYLOAD_EXIT'] = str(payload_exit)
    for f in glob.glob(os.path.join(ws, '_shim', 'payload_argv.*')):    # 이 호출의 argv 만 본다
        os.remove(f)
    before = set(glob.glob(os.path.join(ws, 'prereg_v2_*')))
    p = subprocess.run(['bash', runner or RUNNER], cwd=ws, env=env, capture_output=True, text=True, encoding='utf-8',
                       errors='replace', timeout=timeout, stdin=subprocess.DEVNULL)
    r = Run()
    r.rc, r.log = p.returncode, (p.stdout or '') + (p.stderr or '')
    if env.get('OUTDIR'):
        r.outdir = env['OUTDIR'] if os.path.isdir(env['OUTDIR']) else None
    else:
        new = sorted(set(glob.glob(os.path.join(ws, 'prereg_v2_*'))) - before)
        r.outdir = new[0] if len(new) == 1 else None
    r.new_dirs = sorted(set(glob.glob(os.path.join(ws, 'prereg_v2_*'))) - before)
    r.receipt, r.receipt_bytes = None, None
    if r.outdir and os.path.exists(os.path.join(r.outdir, 'run_receipt.json')):
        r.receipt_bytes = open(os.path.join(r.outdir, 'run_receipt.json'), 'rb').read()
        r.receipt = json.loads(r.receipt_bytes)
    r.arms = sorted(os.path.basename(x) for x in glob.glob(os.path.join(r.outdir or '/nonexistent', 'p2_*.json')))
    r.argv = {}
    for f in glob.glob(os.path.join(ws, '_shim', 'payload_argv.*')):
        toks = open(f, 'rb').read().decode('utf-8').split('\0')
        toks = toks[:-1] if toks and toks[-1] == '' else toks
        out = toks[toks.index('--out') + 1] if '--out' in toks else f
        r.argv[out] = toks
    r.scripts = sorted(glob.glob(os.path.join(ws, 'kit_*', 'run_1', 'p2_*.sh')))
    return r


def reset_ws(ws):
    """같은 경로를 다시 쓰려고 산출물만 지운다 (침대 · 킷은 둔다)."""
    for d in glob.glob(os.path.join(ws, 'prereg_v2_*')):
        shutil.rmtree(d, ignore_errors=True)
    for f in glob.glob(os.path.join(ws, '_shim', '*')) + glob.glob(os.path.join(ws, 'kit_*', 'run_1', 'p2_*')) \
            + glob.glob(os.path.join(ws, 'kit_*', 'run_1', '.peak_rss_*')):
        os.remove(f)


def opt(toks, flag):
    """argv 에서 flag 다음 토큰 (없으면 None · 두 번 나오면 마지막 — argparse 와 같다)."""
    idx = [i for i, t in enumerate(toks) if t == flag]
    return toks[idx[-1] + 1] if idx and idx[-1] + 1 < len(toks) else None


def expect_decl(toks):
    v = opt(toks, '--expect-physics') or ''
    return dict(kv.split('=', 1) for kv in v.split(',') if '=' in kv)


def manifest_of(path):
    d = json.load(open(path, encoding='utf-8'))
    return ((d.get('mpm_metrics') or {}).get('step3') or {}), (((d.get('mpm_metrics') or {}).get('step3') or {}).get('manifest') or {})


def probe(env_over, keys=('OUTDIR', 'NG_TAG', 'NG_ATAG', 'NG_FLAG', 'NG_DECL')):
    """러너 설정부 (표지 앞) 만 실제로 돌려 조립 결과를 읽는다 (규칙 L 의 runner_config 와 같은 방식 · 부작용 없음)."""
    src = open(RUNNER, encoding='utf-8').read()
    head = src[:src.index(MARKER)].rsplit('\n', 1)[0]
    body = head + '\n' + '\n'.join('printf "%s=%s\\n" ' + k + ' "${' + k + '-<UNSET>}"' for k in keys)
    env = base_env(**env_over)
    env.update(P2_SCR=SCRIPTS, P2_SELF=RUNNER)
    p = subprocess.run(['bash', '-s'], input=body, capture_output=True, text=True, encoding='utf-8', errors='replace',
                       env=env, cwd=os.path.join(TD, '_probe'), timeout=120)
    out = {'_rc': p.returncode, '_log': (p.stdout or '') + (p.stderr or '')}
    for ln in (p.stdout or '').splitlines():
        if '=' in ln and ln.split('=', 1)[0] in keys:
            k, v = ln.split('=', 1)
            out[k] = v
    return out


# ═════════════════════════ N0 — 정적 ═════════════════════════
@case('N0 정적 — bash -n · 손잡이 표 · 러너가 표의 이름을 읽는다 · P2_EXTRA 의 rtol = 러너 축')
def t_static():
    bn = subprocess.run(['bash', '-n', RUNNER], capture_output=True, text=True)
    chk('N0a 러너 bash -n', bn.returncode == 0, bn.stderr[-200:])
    tab = getattr(RC, 'RUNNER_CA_EXT_ENV', None)
    names = tuple(n for n, _s, _k in (tab or ()))
    chk('N0b run_contract.RUNNER_CA_EXT_ENV = 러너 손잡이 표 (아홉 이름)', names == NEW_ENV_NAMES, names)
    import ca_ext_cjunc as CW
    cj = {k for _n, s, k in (tab or ()) if s == 'cjunc' and k}
    sd = {k for _n, s, k in (tab or ()) if s == 'sdcp_mod' and k}
    chk('N0c 표의 선언 칸 = ca_ext_cjunc 의 REQUEST_KEYS (사본 없이 같은 집합)',
        cj == set(CW.REQUEST_KEYS_CJUNC) and sd == set(CW.REQUEST_KEYS_SDCP), (sorted(cj), sorted(sd)))
    src = open(RUNNER, encoding='utf-8').read()
    miss = [n for n in NEW_ENV_NAMES if '${' + n + ':-' not in src]
    chk('N0d 러너가 손잡이 아홉을 `${NAME:-}` 로 읽는다 (env 게이트가 "읽지 않는 축" 으로 죽이지 않게)', not miss, miss)
    allowed = re.search(r"^_P2_ALLOWED='([^']*)'", src, re.M)
    chk('N0e P2_EXTRA 허용목록에 --step3-rtol 이 없다 (영수증 · OUTDIR · 증서 대조 = 러너 축 STEP3_RTOL)',
        allowed is not None and '--step3-rtol' not in allowed.group(1).split(), allowed.group(1) if allowed else None)
    chk('N0f PTFE_STAMP 가 face_alpha 를 받는다 (거부 목록이 아니다)',
        re.search(r'^\s*off\|centerline\|face_alpha\)', src, re.M) is not None)
    chk('N0g env 게이트가 CJUNC 이름꼴도 본다 (오타 축 = 죽음)',
        r'CJUNC[A-Z0-9_]*' in src and 'SIGMA_|SDCP_|PTFE_|CJUNC' in src)


# ═════════════════════════ N1 — 끔 (기본) ═════════════════════════
_N1 = {}


@case('N1 끔 (기본) — 옛 팔 이름 · 영수증 · payload 인자 그대로')
def t_off():
    ws = make_ws('n1')
    r = run_runner(ws)
    _N1.update(ws=ws, r=r)
    chk('N1a 러너 rc 0 · 팔 둘 (p2_SBE_a0 · p2_DBE_a0)', r.rc == 0 and r.arms == ['p2_DBE_a0.json', 'p2_SBE_a0.json'],
        (r.rc, r.arms, r.log[-600:]))
    rc = r.receipt or {}
    chk('N1b 영수증에 다음 세대 칸 없음 (ca_ext_request · step3_rtol)', r.receipt is not None
        and 'ca_ext_request' not in rc and 'step3_rtol' not in rc, sorted(rc))
    toks = r.argv.get('p2_SBE_a0.json') or []
    bad = [t for t in toks if t.startswith(('--step3-cjunc', '--step3-sdcp-mod-c', '--step3-rtol'))]
    chk('N1c payload 인자에 새 플래그 없음 · --ptfe-stamp off · 선언에 ca_ext 칸 없음',
        toks and not bad and opt(toks, '--ptfe-stamp') == 'off' and not [k for k in expect_decl(toks) if k.startswith('ca_ext.')],
        (bad, toks[-12:]))
    base = os.path.basename(r.outdir or '')
    chk('N1d OUTDIR 이름에 새 태그 없음 (_cj · _rt · _c0 · _c1)', base and not re.search(r'_cj|_rt|_c[01](_|$)', base), base)
    if r.arms:
        s3, m = manifest_of(os.path.join(r.outdir, 'p2_SBE_a0.json'))
        chk('N1e 팔 매니페스트 = p2 세대 (ca_ext 없음 · 요청 칸 없음)',
            str(m.get('physics_protocol_id', '')).startswith('p2-') and 'ca_ext' not in m and 'ca_ext_requested' not in m,
            m.get('physics_protocol_id'))


# ═════════════════════════ N2 · N3 — 탄소 접합 (+ SDCP 수정자) + rtol ═════════════════════════
_TAG_RE = r'_cj1000000_[0-9a-f]{8}'


def _nextgen_e2e(label, env_over, want_c=None):
    ws = make_ws(label)
    r = run_runner(ws, env_over)
    c_tag = '' if want_c is None else f'_c{want_c}'
    pat = re.compile(r'^p2_(SBE|DBE)' + _TAG_RE + c_tag + r'_rt1em12_a0\.json$')
    chk(f'{label}a 러너 rc 0 · 팔 둘 · 이름 = p2_<침대>_cj1000000_<h8>{c_tag}_rt1em12_a0 (옛 p2_SBE_a0 와 다르다)',
        r.rc == 0 and len(r.arms) == 2 and all(pat.match(a) for a in r.arms), (r.rc, r.arms, r.log[-900:]))
    rc = r.receipt or {}
    req = rc.get('ca_ext_request') or {}
    want_req = {'cjunc': dict(CJ_REQ)}
    if want_c is not None:
        want_req['sdcp_mod'] = {'c': float(want_c)}
    chk(f'{label}b 영수증 — ca_ext_request = 선언 값 (형 맞춤 · float · str) · step3_rtol 1e-12 · 러너 요청 검사 통과',
        req == want_req and rc.get('step3_rtol') == 1e-12 and RC.ca_ext_request_problem(req) is None,
        (req, rc.get('step3_rtol')))
    for bed in ('SBE', 'DBE'):
        name = next((a for a in r.arms if a.startswith(f'p2_{bed}_')), None)
        toks = r.argv.get(name) or []
        vals = {f: opt(toks, f) for f in ('--step3-cjunc-rj', '--step3-cjunc-len-law', '--step3-cjunc-unreg-law',
                                         '--step3-cjunc-s-min-um', '--step3-cjunc-tol-ff-um', '--step3-cjunc-ptfe-jlaw',
                                         '--step3-rtol', '--step3-sdcp-mod-c')}
        ok_vals = (toks.count('--step3-cjunc') == 1 and vals['--step3-cjunc-rj'] is not None
                   and float(vals['--step3-cjunc-rj']) == 1e6 and vals['--step3-cjunc-len-law'] == 'len_scaled_v0'
                   and vals['--step3-cjunc-unreg-law'] == 'cut' and float(vals['--step3-cjunc-s-min-um'] or 'nan') == 0.5
                   and float(vals['--step3-cjunc-tol-ff-um'] or 'nan') == 0.5 and vals['--step3-cjunc-ptfe-jlaw'] == 'P0'
                   and float(vals['--step3-rtol'] or 'nan') == 1e-12
                   and vals['--step3-sdcp-mod-c'] == (None if want_c is None else str(want_c)))
        chk(f'{label}c [{bed}] payload 인자 (명령줄 대조) — 접합 일곱 · rtol · 수정자 c', bool(toks) and ok_vals, vals)
        dec = expect_decl(toks)
        want_keys = {f'ca_ext.cjunc.{k}' for k in CJ_REQ} | ({'ca_ext.sdcp_mod.c'} if want_c is not None else set())
        got = {k for k in dec if k.startswith('ca_ext.')}

        def _same(a, b):
            try:
                return float(a) == float(b)
            except ValueError:
                return a == b
        chk(f'{label}d [{bed}] --expect-physics 선언 = 켠 블록의 칸 전부 · 값 = 영수증 (선언한 축 = 매니페스트 축)',
            got == want_keys and all(_same(dec[f'ca_ext.cjunc.{k}'], v) for k, v in CJ_REQ.items())
            and (want_c is None or float(dec['ca_ext.sdcp_mod.c']) == float(want_c))
            and dec.get('ptfe_stamp') == 'off', sorted(got ^ want_keys))
        s3, m = manifest_of(os.path.join(r.outdir, name)) if (name and r.outdir) else ({}, {})
        pr = ((m.get('ca_ext') or {}).get('cjunc') or {}).get('protocol') or {}
        chk(f'{label}e [{bed}] 팔 = p3ca · ca_ext_record_ok · receipt_match · 수렴 증서 (다음 세대 게시 조건) · protocol R_j 1e6',
            bool(m) and str(m.get('physics_protocol_id', '')).startswith('p3ca-') and RC.ca_ext_record_ok(m) == (True, None)
            and RC.receipt_match(rc, m)[0] and RC.next_gen_cert_ok(s3)[0] and pr.get('R_j_ohm') == 1e6
            and m.get('ca_ext_requested') == (['cjunc'] if want_c is None else ['cjunc', 'sdcp_mod']),
            (name, m.get('physics_protocol_id'), RC.ca_ext_record_ok(m), RC.next_gen_cert_ok(s3)))
        if want_c is not None:
            sev = ((m.get('ca_ext') or {}).get('sdcp_mod') or {}).get('evidence') or {}
            want_disc = bed == 'DBE'
            chk(f'{label}f [{bed}] SDCP 수정자 — c {want_c} · 판별 표지 {want_disc} (DBE 근접 1 · SBE = 구성상 no-op)',
                sev.get('s3_discriminating') is want_disc
                and (((m.get('ca_ext') or {}).get('sdcp_mod') or {}).get('protocol') or {}).get('c') == float(want_c),
                sev)
    base = os.path.basename(r.outdir or '')
    chk(f'{label}g OUTDIR 이름에 새 태그 (_cj1000000_<h8>{c_tag}_rt1em12) · 끔 런과 다른 디렉터리',
        bool(re.search(_TAG_RE + c_tag + '_rt1em12', base)) and base != os.path.basename((_N1.get('r') and _N1['r'].outdir) or ''),
        base)
    return r


@case('N2 탄소 접합 + rtol — 인자 · 선언 · 영수증 · 팔 이름 · p3ca · check_arm · 증서')
def t_cjunc():
    _nextgen_e2e('N2', dict(CJ_ENV, STEP3_RTOL='1e-12'))


@case('N3 탄소 접합 + SDCP 수정자 c = 1 + rtol')
def t_cjunc_c1():
    _nextgen_e2e('N3', dict(CJ_ENV, SDCP_MOD_C='1', STEP3_RTOL='1e-12'), want_c=1)


# ═════════════════════════ N4 · N5 — face_alpha + rtol ═════════════════════════
def _fa_e2e(label, lean):
    ws = make_ws(label)
    r = run_runner(ws, {'PTFE_STAMP': 'face_alpha', 'LEAN': lean, 'STEP3_RTOL': '1e-12'})
    pat = re.compile(r'^p2_(SBE|DBE)_fa_rt1em12_a0\.json$')
    chk(f'{label}a 러너 rc 0 · 팔 둘 · 이름 = p2_<침대>_fa_rt1em12_a0', r.rc == 0 and len(r.arms) == 2
        and all(pat.match(a) for a in r.arms), (r.rc, r.arms, r.log[-900:]))
    rc = r.receipt or {}
    chk(f'{label}b 영수증 — ptfe_stamp face_alpha · step3_rtol 1e-12 · 접합 요청 없음',
        rc.get('ptfe_stamp') == 'face_alpha' and rc.get('step3_rtol') == 1e-12 and 'ca_ext_request' not in rc, rc)
    for bed in ('SBE', 'DBE'):
        name = next((a for a in r.arms if a.startswith(f'p2_{bed}_')), None)
        toks = r.argv.get(name) or []
        chk(f'{label}c [{bed}] payload 인자 — --ptfe-stamp face_alpha · --step3-rtol 1e-12 · 접합 플래그 없음 · 선언 ptfe_stamp',
            opt(toks, '--ptfe-stamp') == 'face_alpha' and float(opt(toks, '--step3-rtol') or 'nan') == 1e-12
            and not [t for t in toks if t.startswith('--step3-cjunc')] and expect_decl(toks).get('ptfe_stamp') == 'face_alpha',
            toks[-14:])
        s3, m = manifest_of(os.path.join(r.outdir, name)) if (name and r.outdir) else ({}, {})
        ion_ok = (lean != '3') or isinstance(s3.get('ion_conv_cert'), dict)
        chk(f'{label}d [{bed}] 팔 = p3ca (ptfe_face) · ca_ext_record_ok · receipt_match · 다음 세대 게시 조건 '
            f'{"(전자 + 이온 증서)" if lean == "3" else "(전자 증서)"}',
            bool(m) and str(m.get('physics_protocol_id', '')).startswith('p3ca-') and 'ptfe_face' in (m.get('ca_ext') or {})
            and RC.ca_ext_record_ok(m) == (True, None) and RC.receipt_match(rc, m)[0] and RC.next_gen_cert_ok(s3)[0] and ion_ok,
            (name, m.get('physics_protocol_id'), RC.next_gen_cert_ok(s3)))


@case('N4 face_alpha + rtol (LEAN 2)')
def t_fa2():
    _fa_e2e('N4', '2')


@case('N5 face_alpha + rtol (LEAN 3 · 이온 증서)')
def t_fa3():
    _fa_e2e('N5', '3')


# ═════════════════════════ N6 — 발사 전 거부 ═════════════════════════
REFUSE = [
    # (이름, env 덧쓰기, 로그에 있어야 할 사유 꼬리)
    ('스위치 값 (CJUNC=yes)', {'CJUNC': 'yes'}, 'RUNNER_CA_EXT|SWITCH|'),
    ('접합 켬 · s_min 없음', dict(CJ_ENV, CJUNC_S_MIN_UM=None), 'RUNNER_CA_EXT|MISSING|'),
    ('접합 켬 · 값 여섯 다 없음', {'CJUNC': '1'}, 'RUNNER_CA_EXT|MISSING|'),
    ('R_j 만 (접합 안 켬)', {'CJUNC_RJ': '1e6'}, 'RUNNER_CA_EXT|FLAG_WITHOUT_CJUNC|'),
    ('SDCP 수정자만 (S2 없이)', {'SDCP_MOD_C': '1'}, 'RUNNER_CA_EXT|NO_CJUNC|'),
    ('수정자 c = 0.5', dict(CJ_ENV, SDCP_MOD_C='0.5'), 'RUNNER_CA_EXT|VALUE|'),
    ('수정자 c = 1.0 (payload 선택지 0 · 1 밖)', dict(CJ_ENV, SDCP_MOD_C='1.0'), 'RUNNER_CA_EXT|VALUE|'),
    ('R_j nan', dict(CJ_ENV, CJUNC_RJ='nan'), 'RUNNER_CA_EXT|VALUE|'),
    ('R_j inf', dict(CJ_ENV, CJUNC_RJ='inf'), 'RUNNER_CA_EXT|VALUE|'),
    ('R_j 1e999 (넘침 → inf)', dict(CJ_ENV, CJUNC_RJ='1e999'), 'RUNNER_CA_EXT|VALUE|'),
    ('R_j 음수', dict(CJ_ENV, CJUNC_RJ='-1e6'), 'RUNNER_CA_EXT|VALUE|'),
    ('R_j 0 (정량 아님)', dict(CJ_ENV, CJUNC_RJ='0'), 'RUNNER_CA_EXT|REQUEST|'),
    ('R_j 끝 공백', dict(CJ_ENV, CJUNC_RJ='1e6 '), 'RUNNER_CA_EXT|VALUE|'),
    ('R_j 유니코드 숫자 (١٠)', dict(CJ_ENV, CJUNC_RJ='١٠'), 'RUNNER_CA_EXT|VALUE|'),
    ('R_j 밑줄 (1_000)', dict(CJ_ENV, CJUNC_RJ='1_000'), 'RUNNER_CA_EXT|VALUE|'),
    ('R_j 변수 참조 ($HOME)', dict(CJ_ENV, CJUNC_RJ='$HOME'), 'RUNNER_CA_EXT|VALUE|'),
    ('미등록 면 법칙 auto', dict(CJ_ENV, CJUNC_UNREG_LAW='auto'), 'RUNNER_CA_EXT|REQUEST|'),
    ('미등록 면 법칙 구분자 (cut;x)', dict(CJ_ENV, CJUNC_UNREG_LAW='cut;x'), 'RUNNER_CA_EXT|VALUE|'),
    ('길이 법칙 다른 판', dict(CJ_ENV, CJUNC_LEN_LAW='len_scaled_v1'), 'RUNNER_CA_EXT|REQUEST|'),
    ('PTFE–접합 P1 (face_alpha 에서만)', dict(CJ_ENV, CJUNC_PTFE_JLAW='P1'), 'RUNNER_CA_EXT|REQUEST|'),
    ('접합 + LEAN 미지정', dict(CJ_ENV, LEAN=None), 'RUNNER_CA_EXT|LEAN|'),
    ('접합 + LEAN 1', dict(CJ_ENV, LEAN='1'), 'RUNNER_CA_EXT|LEAN|'),
    ('접합 + LEAN 4 (필드)', dict(CJ_ENV, LEAN='4'), 'RUNNER_CA_EXT|LEAN|'),
    ('접합 + 점 스탬프', dict(CJ_ENV, FIBRE_STAMP='point'), 'RUNNER_CA_EXT|SEGMENT|'),
    ('접합 + 주기', dict(CJ_ENV, MPM_PERIODIC_SIGMA='1'), 'RUNNER_CA_EXT|PERIODIC|'),
    ('접합 + SDCP 브리지 진단 팔', dict(CJ_ENV, SDCP_SPHERE_D='0.30', SDCP_BRIDGE='0.3'), 'RUNNER_CA_EXT|SDCP_BRIDGE|'),
    ('접합 + σ_VGCF 고정 0', dict(CJ_ENV, SIGMA_VGCF_OVERRIDE='0'), 'RUNNER_CA_EXT|VGCF_INSULATING|'),
    ('접합 + face_alpha (조합 미정의)', dict(CJ_ENV, PTFE_STAMP='face_alpha'), 'RUNNER_CA_EXT|FACE_ALPHA_COMBO|'),
    ('face_alpha + LEAN 미지정', {'PTFE_STAMP': 'face_alpha', 'LEAN': None}, 'RUNNER_CA_EXT|LEAN|'),
    ('face_alpha + LEAN 1', {'PTFE_STAMP': 'face_alpha', 'LEAN': '1'}, 'RUNNER_CA_EXT|LEAN|'),
    ('face_alpha + LEAN 4', {'PTFE_STAMP': 'face_alpha', 'LEAN': '4'}, 'RUNNER_CA_EXT|LEAN|'),
    ('face_alpha + σ_PTFE > 0', {'PTFE_STAMP': 'face_alpha', 'SIGMA_PTFE': '1e-16'}, 'RUNNER_CA_EXT|SIGMA_PTFE|'),
    ('face_alpha + PTFE 차단 (LEAN 3)', {'PTFE_STAMP': 'face_alpha', 'LEAN': '3', 'PTFE_BLOCK_UM': '0.1'},
     'RUNNER_CA_EXT|PTFE_BLOCK|'),
    ('face_alpha + 주기', {'PTFE_STAMP': 'face_alpha', 'MPM_PERIODIC_SIGMA': '1'}, 'RUNNER_CA_EXT|PERIODIC|'),
    ('face_alpha + 점 스탬프', {'PTFE_STAMP': 'face_alpha', 'FIBRE_STAMP': 'point'}, 'RUNNER_CA_EXT|SEGMENT|'),
    ('rtol 1e-10 (봉인 상한 1e-12 밖 · 증서 ⓐ 실패 확정)', {'STEP3_RTOL': '1e-10'}, 'RUNNER_CA_EXT|RTOL|'),
    ('rtol 0', {'STEP3_RTOL': '0'}, 'RUNNER_CA_EXT|RTOL|'),
    ('rtol 글자', {'STEP3_RTOL': '1e-12x'}, 'RUNNER_CA_EXT|VALUE|'),
    ('P2_EXTRA 로 rtol (러너 축으로 옮김)', {'P2_EXTRA': '--step3-rtol 1e-12'}, 'STEP3_RTOL'),
    ('오타 축 (CJUNC_BOGUS)', {'CJUNC_BOGUS': '1'}, 'CJUNC_BOGUS'),
]


@case('N6 발사 전 거부 — 구조화 사유 · rc 2 · 디렉터리를 만들지 않는다')
def t_refuse():
    ws = make_ws('n6')
    for nm, over, code in REFUSE:
        r = run_runner(ws, over)
        chk(f'N6 [{nm}] → rc 2 · `{code}` · 새 디렉터리 없음 · payload 미호출',
            r.rc == 2 and code in r.log and not r.new_dirs and not r.argv, (r.rc, r.new_dirs, r.log.strip()[-260:]))


#: 러너 거부 (러너가 가진 축의 조합) ↔ payload 입구 거부 — 같은 조합을 payload 에 직접 주면 같은 부류로 거부돼야 한다 (러너 = 부분집합)
_L1 = ['--no-step4', '--no-thermal', '--no-trackb', '--no-field']
_L4 = ['--no-step4', '--no-thermal', '--no-trackb', '--no-pore', '--no-collector']
MIRROR = [
    ('접합 + LEAN 1', B6.OFF + _L1 + B6.CJ, 'S2_CJUNC_REFUSED|COLLECTOR|'),
    ('접합 + LEAN 4', B6.OFF + _L4 + B6.CJ, 'S2_CJUNC_REFUSED|FIELD|'),
    ('접합 + LEAN 미지정', B6.OFF + B6.CJ, 'S2_CJUNC_REFUSED|FIELD|'),
    ('접합 + 점 스탬프', B6.OFF + B6.LEAN2 + B6.CJ + ['--step3-fibre-stamp', 'point'], 'S2_CJUNC_REFUSED|SEGMENT|'),
    ('접합 + 주기', B6.OFF + B6.LEAN2 + B6.CJ + ['--periodic'], 'S2_CJUNC_REFUSED|PERIODIC|'),
    ('접합 + SDCP 브리지', B6.OFF + B6.LEAN2 + B6.CJ + ['--step3-sdcp-bridge', '0.3'], 'S2_CJUNC_REFUSED|SDCP_BRIDGE|'),
    ('접합 + σ_VGCF 0', B6.OFF + B6.LEAN2 + B6.CJ + ['--sigma-vgcf', '0'], 'S2_CJUNC_REFUSED|VGCF_INSULATING|'),
    ('접합 + face_alpha', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2 + B6.CJ, 'S2_CJUNC_REFUSED|FACE_ALPHA_COMBO|'),
    ('face_alpha + LEAN 1', ['--ptfe-stamp', 'face_alpha'] + _L1, 'S1_FACE_ALPHA_REFUSED|COLLECTOR|'),
    ('face_alpha + LEAN 4', ['--ptfe-stamp', 'face_alpha'] + _L4, 'S1_FACE_ALPHA_REFUSED|FIELD|'),
    ('face_alpha + σ_PTFE', ['--ptfe-stamp', 'face_alpha', '--sigma-ptfe', '1e-16'] + B6.LEAN2, 'S1_FACE_ALPHA_REFUSED|SIGMA_PTFE|'),
    ('face_alpha + PTFE 차단', ['--ptfe-stamp', 'face_alpha', '--step3-ptfe-block-um', '0.1'] + B6.LEAN3,
     'S1_FACE_ALPHA_REFUSED|PTFE_BLOCK|'),
    ('face_alpha + 주기', ['--ptfe-stamp', 'face_alpha', '--periodic'] + B6.LEAN2, 'S1_FACE_ALPHA_REFUSED|PERIODIC|'),
    ('face_alpha + 점 스탬프', ['--ptfe-stamp', 'face_alpha', '--step3-fibre-stamp', 'point'] + B6.LEAN2,
     'S1_FACE_ALPHA_REFUSED|SEGMENT|'),
]


@case('N6b 러너 거부 ⊆ payload 거부 — 같은 조합을 payload 에 직접 주면 거부 (과잉차단 없음)')
def t_mirror():
    d = os.path.join(TD, 'n6b')
    os.makedirs(d)
    B6.make_fixture(d, sdcp=True)
    for i, (nm, extra, code) in enumerate(MIRROR):
        rc, log, _p = B6.run_payload(d, extra, out=f'mirror_{i}.json')
        chk(f'N6b [{nm}] payload 도 거부 — `{code}`', rc != 0 and code in log, (rc, log.strip()[-220:]))
    rc, log, p = B6.run_payload(d, B6.OFF + B6.LEAN2 + ['--step3-rtol', '1e-10'], out='mirror_rtol.json')
    s3 = B6.s3_of(p)
    cert = s3.get('conv_cert')
    chk('N6b [rtol 1e-10] payload 는 받지만 그 팔은 게시할 수 없다 (증서 ⓐ 실패 · 미수렴) — 러너 거부는 계산 낭비만 막는다',
        rc != 0 or (isinstance(cert, dict) and cert.get('ok') is False and s3.get('unconverged') is True),
        (rc, (cert or {}).get('ok'), s3.get('unconverged'), log.strip()[-200:]))


# ═════════════════════════ N7 — OUTDIR · 팔 태그 (설정부만 실제로 돌린다) ═════════════════════════
@case('N7 OUTDIR · 팔 태그 · 인자 · 선언 — 다른 요청 = 다른 이름 · 같은 물리 = 같은 이름')
def t_names():
    os.makedirs(os.path.join(TD, '_probe'), exist_ok=True)
    base = probe(dict(CJ_ENV))
    chk('N7a 설정부 실행 (접합) — 중단 없음 · 다섯 값이 조립된다', base['_rc'] == 0
        and all(base.get(k, '<UNSET>') != '<UNSET>' for k in ('OUTDIR', 'NG_TAG', 'NG_ATAG', 'NG_FLAG', 'NG_DECL')),
        base['_log'][-300:])
    fl = (base.get('NG_FLAG') or '').split()
    chk('N7b 인자 꼴 — 켜기 + 값 플래그 여섯 (값 = 정규 표기) · 선행 공백', (base.get('NG_FLAG') or '').startswith(' ')
        and fl[:1] == ['--step3-cjunc'] and opt(fl, '--step3-cjunc-rj') == repr(1e6)
        and opt(fl, '--step3-cjunc-s-min-um') == repr(0.5) and opt(fl, '--step3-cjunc-unreg-law') == 'cut'
        and len(fl) == 13, fl)
    dec = dict(kv.split('=', 1) for kv in (base.get('NG_DECL') or '').split(',') if '=' in kv)
    chk('N7c 선언 꼴 — `,ca_ext.cjunc.<칸>=<값>` 여섯 (앞 쉼표 · 러너 선언 뒤에 붙는다)',
        (base.get('NG_DECL') or '').startswith(',ca_ext.cjunc.') and set(dec) == {f'ca_ext.cjunc.{k}' for k in CJ_REQ}, dec)
    off = probe({})
    chk('N7d 끔 — 넷 다 빈 문자열 (옛 조립 그대로)', off['_rc'] == 0
        and all(off.get(k) == '' for k in ('NG_TAG', 'NG_ATAG', 'NG_FLAG', 'NG_DECL')), off)
    same = [probe(dict(CJ_ENV, CJUNC_RJ=v)) for v in ('1000000', '1.0e6', '1e+6', '1E6')]
    chk('N7e 같은 R_j 다른 표기 (1000000 · 1.0e6 · 1e+6 · 1E6) = 같은 OUTDIR · 같은 팔 태그 `_cj1000000_…` (정규 · 같은 물리 = 같은 이름)',
        str(base.get('NG_ATAG', '')).startswith('_cj1000000_')
        and all(s.get('OUTDIR') == base.get('OUTDIR') and s.get('NG_ATAG') == base.get('NG_ATAG') for s in same),
        [base.get('NG_ATAG')] + [s.get('NG_ATAG') for s in same])
    variants = {
        'R_j 1e2': dict(CJ_ENV, CJUNC_RJ='1e2'), 'R_j 1e8': dict(CJ_ENV, CJUNC_RJ='1e8'),
        'R_j 2.5': dict(CJ_ENV, CJUNC_RJ='2.5'), 'R_j 25': dict(CJ_ENV, CJUNC_RJ='25'),
        's_min 0.05': dict(CJ_ENV, CJUNC_S_MIN_UM='0.05'), 'tol_ff 0.05': dict(CJ_ENV, CJUNC_TOL_FF_UM='0.05'),
        'fused': dict(CJ_ENV, CJUNC_UNREG_LAW='fused'), 'c 0': dict(CJ_ENV, SDCP_MOD_C='0'),
        'c 1': dict(CJ_ENV, SDCP_MOD_C='1'), 'rtol 1e-12': dict(CJ_ENV, STEP3_RTOL='1e-12'),
        'rtol 1e-13': dict(CJ_ENV, STEP3_RTOL='1e-13'),
    }
    got = {k: probe(v) for k, v in variants.items()}
    outs = [base.get('OUTDIR')] + [g.get('OUTDIR') for g in got.values()]
    tags = [base.get('NG_ATAG')] + [g.get('NG_ATAG') for g in got.values()]
    chk(f'N7f 요청 {len(outs)} 가지 = OUTDIR {len(set(outs))} 개 · 팔 태그 {len(set(tags))} 개 (전부 다르다 · 2.5 ↔ 25 무손실 · '
        f'R_j 가 같아도 s_min · tol_ff · 법칙이 다르면 다르다)',
        len(set(outs)) == len(outs) and len(set(tags)) == len(tags) and all(outs) and all(tags),
        dict(zip(['base'] + list(got), tags)))
    chk('N7g 읽을 수 있는 태그 — R_j 1e2 → `_cj100_` · 2.5 → `_cj2p5_` · c 1 → `_c1` · rtol 1e-13 → `_rt1em13`',
        got['R_j 1e2'].get('NG_ATAG', '').startswith('_cj100_') and got['R_j 2.5'].get('NG_ATAG', '').startswith('_cj2p5_')
        and got['c 1'].get('NG_ATAG', '').endswith('_c1') and got['rtol 1e-13'].get('NG_ATAG', '').endswith('_rt1em13'),
        {k: got[k].get('NG_ATAG') for k in ('R_j 1e2', 'R_j 2.5', 'c 1', 'rtol 1e-13')})
    fa = probe({'PTFE_STAMP': 'face_alpha', 'STEP3_RTOL': '1e-12'})
    rt = probe({'STEP3_RTOL': '1e-12'})
    chk('N7h face_alpha + rtol — 팔 태그 `_fa_rt1em12` (OUTDIR 은 `_ptsface_alpha` 가 이미 가른다) · 끔 + rtol = `_rt1em12`',
        fa.get('NG_ATAG') == '_fa_rt1em12' and fa.get('NG_TAG') == '_rt1em12' and rt.get('NG_ATAG') == '_rt1em12'
        and fa.get('OUTDIR') != rt.get('OUTDIR'), (fa.get('NG_ATAG'), rt.get('NG_ATAG')))
    zero = probe({'PTFE_STAMP': 'face_alpha', 'SIGMA_PTFE': '0'})
    chk('N7i face_alpha + σ_PTFE 0 은 거부하지 않는다 (payload 도 > 0 만 거부 · 과잉차단 없음)', zero['_rc'] == 0
        and zero.get('NG_ATAG') == '_fa', zero['_log'][-200:])


# ═════════════════════════ N8 — SKIP 캐시 함정 ═════════════════════════
@case('N8 SKIP 캐시 함정 — 옛 팔이 있는 OUTDIR 을 명시해도 재사용 · 삭제하지 않는다')
def t_skip_trap():
    r1 = _N1.get('r')
    if not (r1 and r1.outdir and len(r1.arms) == 2):
        chk('N8 선행 (N1 끔 팔 둘)', False, 'N1 이 팔을 못 만들었다')
        return
    ws = make_ws('n8')
    #  ⚠ 진단 런 (ARMS ≠ 8) 은 사용자 OUTDIR 에도 `_arm1` 을 강제로 붙인다 (R3-CX-09) — 이미 담은 이름이어야 그 디렉터리를 그대로 쓴다
    old = os.path.join(ws, 'old_outdir_arm1')
    os.makedirs(old)
    sha = {}
    for a in r1.arms:                                       # 옛 팔만 (영수증 없이) — 옛 디렉터리 꼴
        shutil.copy2(os.path.join(r1.outdir, a), os.path.join(old, a))
        sha[a] = hashlib.sha256(open(os.path.join(old, a), 'rb').read()).hexdigest()
    r = run_runner(ws, dict(CJ_ENV, OUTDIR=old, STEP3_RTOL='1e-12'), payload_exit=3)
    after = {a: hashlib.sha256(open(os.path.join(old, a), 'rb').read()).hexdigest()
             if os.path.exists(os.path.join(old, a)) else None for a in sha}
    outs = sorted(r.argv)
    chk('N8a 옛 팔을 SKIP (재사용) 하지 않는다', 'SKIP (완전)' not in r.log, r.log[-400:])
    chk('N8b 옛 팔 두 파일이 그대로 (삭제 · 덮어쓰기 없음)', after == sha, after)
    chk('N8c 새 팔은 새 이름으로만 돈다 (payload --out = p2_<침대>_cj…_rt1em12_a0)',
        outs and all(re.match(r'^p2_(SBE|DBE)' + _TAG_RE + r'_rt1em12_a0\.json$', o) for o in outs), outs)


# ═════════════════════════ N9 — 규율 검사기 격리 ═════════════════════════
@case('N9 규율 검사기 격리 — 부모 셸의 새 축 env 가 규칙 L 탐침을 오염시키지 않는다')
def t_isolation():
    import check_method_discipline as CMD
    axes = tuple(getattr(CMD, '_RUNNER_AXES', ()))
    chk('N9a 새 손잡이 아홉이 규율 검사기의 격리 목록 (_RUNNER_AXES) 에 있다', set(NEW_ENV_NAMES) <= set(axes),
        sorted(set(NEW_ENV_NAMES) - set(axes)))
    polluted = dict(CJ_ENV, SDCP_MOD_C='1', STEP3_RTOL='1e-12')
    saved = {k: os.environ.get(k) for k in polluted}
    try:
        os.environ.update(polluted)
        with contextlib.redirect_stdout(io.StringIO()):
            c0 = CMD.runner_config({})
        chk('N9b 오염된 부모 셸 (CJUNC=1 … SDCP_MOD_C=1 · STEP3_RTOL) 에서도 기본 탐침 = 끔 조립 (중단 없음 · LEAN_FLAGS 빈)',
            not c0.get('_aborted') and c0.get('LEAN_FLAGS') == '', c0)
        old_axes = CMD._RUNNER_AXES
        try:
            CMD._RUNNER_AXES = tuple(a for a in old_axes if a not in NEW_ENV_NAMES)
            with contextlib.redirect_stdout(io.StringIO()):
                c1 = CMD.runner_config({})
        finally:
            CMD._RUNNER_AXES = old_axes
        chk('N9c (판별력) 격리 목록에서 새 이름을 빼면 같은 탐침이 오염된다 (중단) — 위 통과가 우연이 아니다',
            bool(c1.get('_aborted')), c1)
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


# ═════════════════════════ NB — 끔 경로 (고치기 전 러너와 대조) ═════════════════════════
@case('NB 끔 경로 — 고치기 전 러너와 payload argv · 영수증 · OUTDIR · 팔 이름 · 매니페스트 대조 (--old-runner)')
def t_old_runner():
    if not ARGS.old_runner:
        print('    (--old-runner 없음 — 건너뜀 · 커밋 증거는 그 인자로 돌린 기록)')
        return
    ws = make_ws('nb')
    for nm, over in (('off LEAN2', {}), ('centerline LEAN3', {'PTFE_STAMP': 'centerline', 'LEAN': '3'})):
        reset_ws(ws)
        ro = run_runner(ws, over, runner=ARGS.old_runner)
        o_scripts = {os.path.basename(s).split('.')[0]: open(s, encoding='utf-8').read() for s in ro.scripts}
        o_mans = {a: manifest_of(os.path.join(ro.outdir, a)) for a in ro.arms} if ro.outdir else {}
        o_out = os.path.basename(ro.outdir or '')
        reset_ws(ws)
        rn = run_runner(ws, over)
        n_scripts = {os.path.basename(s).split('.')[0]: open(s, encoding='utf-8').read() for s in rn.scripts}
        n_mans = {a: manifest_of(os.path.join(rn.outdir, a)) for a in rn.arms} if rn.outdir else {}

        def _strip(sm):
            s3, m = sm
            m = {k: v for k, v in m.items() if k not in ('code_sha', 'exec_env')}
            return json.dumps(m, sort_keys=True), json.dumps({k: v for k, v in s3.items() if k != 'manifest'}, sort_keys=True,
                                                             default=str)
        same_m = (sorted(o_mans) == sorted(n_mans) and all(_strip(o_mans[a]) == _strip(n_mans[a]) for a in o_mans))
        chk(f'NB [{nm}] 두 러너 rc 0 · OUTDIR 이름 · 영수증 바이트 · 팔 이름 · payload argv (명령줄) · 생성 스크립트 · 매니페스트 '
            f'(code_sha · exec_env 빼고) · step3 값 같음',
            ro.rc == 0 and rn.rc == 0 and o_out == os.path.basename(rn.outdir or '') and ro.receipt_bytes == rn.receipt_bytes
            and ro.arms == rn.arms and ro.argv == rn.argv and o_scripts == n_scripts and same_m and len(ro.arms) == 2,
            (ro.rc, rn.rc, o_out, os.path.basename(rn.outdir or ''), ro.arms, rn.arms, ro.argv == rn.argv,
             o_scripts == n_scripts, same_m, ro.log[-300:], rn.log[-300:]))


def main():
    global ARGS, TD, SHIMDIR
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--old-runner', default='', help='고치기 전 러너 사본 (NB 끔 경로 대조)')
    ap.add_argument('--only', default='', help='쉼표로 나눈 이름 접두 (예: N2,N6)')
    ap.add_argument('--keep', action='store_true', help='임시 디렉터리를 남긴다 (진단)')
    ARGS = ap.parse_args()
    TD = tempfile.mkdtemp(prefix='ca_ext_runner_')
    SHIMDIR = os.path.join(TD, '_bin')
    os.makedirs(SHIMDIR)
    with open(os.path.join(SHIMDIR, 'python3'), 'w', encoding='utf-8') as f:
        f.write(SHIM.replace('__REAL__', os.path.realpath(sys.executable)))
    os.chmod(os.path.join(SHIMDIR, 'python3'), 0o755)
    only = [x.strip() for x in ARGS.only.split(',') if x.strip()]
    try:
        for tag, fn in CASES:
            if only and not any(tag.startswith(o) for o in only):
                continue
            print(f'\n── {tag}')
            try:
                fn()
            except Exception as e:                              # noqa: BLE001 — 옛 코드 (API 없음) 도 시험 단위로 기록
                chk(f'{tag.split()[0]}: 실행', False, f'{type(e).__name__}: {e}')
    finally:
        if ARGS.keep:
            print(f'\n  (임시 디렉터리 남김: {TD})')
        else:
            shutil.rmtree(TD, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    main()
