#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase A 재실행 배치의 `run_receipt.json` 을 **`.sh` 에서** 유도한다.

    python3 scripts/phase_a_receipt_from_sh.py --sh <재실행 .sh 디렉터리> \
        --out <payload 디렉터리> [--expect-arms 32]
    python3 scripts/phase_a_receipt_from_sh.py --selftest

━━ 왜 필요한가 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`phase_a_rerun_from_sh.py` 는 `--out` 만 새 디렉터리로 옮긴다.  영수증은 **러너가
자기 `$OUTDIR` 에 쓰기 때문에** 재실행 payload 디렉터리에는 안 생긴다.  그런데
`phase_a_arms_from_payload.read_receipt()` 는 영수증이 없으면 팔을 **안 만든다**
(맞는 설계 — 봉인을 확인할 수 없으면 판정용 팔이 아니다).  ⇒ 배치가 멀쩡해도
어댑터가 못 돈다.  2026-09-20 실측: `phaseA_rerun_v{015,020,025}_20260918` 96팔 전부.

━━ ⛔ payload 에서 만들지 않는다 (`PA12-04`) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
영수증은 **선언**이고 매니페스트는 **결과**다 (`run_contract` 머리말).  결과에서
선언을 지어내면 `receipt_match()` 가 자기 자신을 대조하게 되고 — 그러면 2026-08-12
의 *"`--fibre` 가 조용히 꺼졌는데 매니페스트는 `segment` 도장을 달았다"* 같은 사고를
**원리적으로 못 잡는다**.  ⇒ 유일하게 허용되는 출처는 **실행된 `.sh`** 다
(`phase_a_rerun_from_sh` 머리말: *"원본 `.sh` 가 실행 기록 그 자체"*).
이 모듈은 `p2_*.json` 을 **열지 않는다** — 셀프테스트 ⑦ 이 그것을 강제한다.

━━ 어떻게 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`.sh` 의 payload 호출을 `shlex` 로 쪼개 **payload 의 진짜 파서**에 먹인다
(`check_method_discipline` 규칙 M 과 같은 `parse_args` 가로채기).  정적 훑기를 쓰지
않는 이유도 같다 — 다른 모듈이 등록한 옵션이 안 보이고, 기본값을 모른다.
축 목록·CLI↔축 대응·해시는 전부 `run_contract` 에서 **가져다** 쓴다 (사본 금지).

⚠ **`code_sha` 는 지어내지 않는다.**  `.sh` 에 없으면 `null` 로 둔다 — 그러면
  `phase_a_preflight` 가 그것을 문제로 보고하고 어댑터는 `--code-sha-missing-ok
  <이유>` 를 요구한다 (`PASL-03`).  그 경로를 우회하는 것이 이 도구의 목적이 아니다.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import shlex
import subprocess
import sys

_SCR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCR)

import run_contract as RC                                    # noqa: E402

PAYLOAD = 'mpm_webapp_payload.py'

#: 한 옵션이 여러 축을 움직이거나 이름이 안 맞는 자리 — **여기 없는 축은 자동 대응**이다.
#  ⚠ 자동 대응은 `RC.CLI_ACCOUNTING` 에서 뽑는다.  새 축이 생기면 `_axes_from_ns` 의
#    fail-closed 단언이 먼저 터진다 (조용히 빠지지 않는다).
_EXPLICIT = {
    #  지름을 주면 도장이 sphere 로 바뀐다 (payload manifest 와 같은 규칙)
    'sdcp_stamp': lambda ns: ('sphere' if float(getattr(ns, 'step3_sdcp_sphere_d', 0) or 0) > 0
                              else 'point'),
    #  매니페스트가 `_sigma_ion_se_ref` 또는 `sigma_ion_se` 로 적는다 (`--sigma-ion-se`)
    'sigma_ion_se_ref_S_cm': lambda ns: float(getattr(ns, 'sigma_ion_se')),
}

#: `.sh` 토큰 → payload 네임스페이스.  파서를 **실행해서** 잡는다 (규칙 M 과 같은 조각).
_PROBE = r'''
import argparse, importlib, json, sys
class _Got(Exception):
    def __init__(self, ap): self.ap = ap
def _hook(self, *a, **k): raise _Got(self)
_REAL_PA = argparse.ArgumentParser.parse_args
_REAL_PKA = argparse.ArgumentParser.parse_known_args
argparse.ArgumentParser.parse_args = _hook
argparse.ArgumentParser.parse_known_args = _hook
sys.argv = [sys.argv[0]]
m = importlib.import_module('mpm_webapp_payload')
try:
    m.main()
except _Got as g:
    #  ⚠ 둘 다 되돌려야 한다 — `parse_args` 안에서 `parse_known_args` 를 부른다
    argparse.ArgumentParser.parse_args = _REAL_PA
    argparse.ArgumentParser.parse_known_args = _REAL_PKA
    toks = json.load(sys.stdin)
    out = []
    for t in toks:
        out.append(vars(g.ap.parse_args(t)))
    print('\x00JSON\x00' + json.dumps(out, default=str))
    raise SystemExit(0)
raise SystemExit('NO_PARSE_ARGS')
'''


#: ★★ 로그 교차검증 — `.sh` 를 **되만들어** 영수증을 낼 때 그것이 실제로 돈 것과 같은지 본다.
#  ⚠⚠ 로그는 payload 의 stdout 이라 **결과 층**이다 (매니페스트와 같은 자격).  그래서
#    영수증을 로그에서 **만들지 않는다** — 만들면 `PA12-04` 순환 그대로다.  여기서는
#    `.sh` 에서 만든 선언을 로그와 **대조만** 한다: 선언은 여전히 `.sh` 가 낳고,
#    로그는 독립적인 반증 기회를 줄 뿐이다.
#  ⚠ 로그가 안 찍는 축은 **검사되지 않는다** — 그 사실을 통과로 읽지 않도록 도구가
#    "로그가 덮지 못한 축" 을 이름으로 보고한다 (규율 ⑤: 안 본 것을 초록으로 만들지 않는다).
LOG_PATTERNS = {
    'vox_um': (r'vox\s+([0-9.]+)\s*\u00b5m', float),
    'bridge_um': (r'\ubcf4\ub9ac\uc9c0|AM \uc811\ucd09 \ube0c\ub9ac\uc9c0 \ubc18\uacbd \*\*\uace0\uc815\*\* ([0-9.]+) \u00b5m', float),
    'fibre_stamp': (r'\uc12c\uc720 \*\*(\uc120\ubd84|\uc810) \uc2a4\ud0ec\ud504\*\* ON', str),
}
#: 로그가 찍는 LEAN 플래그 (사전등록 §5 = σ_e 전용)
LOG_LEAN = ('--no-ion', '--no-pore', '--no-collector')


def expect_physics(tokens):
    """`.sh` 의 `--expect-physics` 선언 → dict.  **스크립트 안의 명시적 선언**이다.

    ★ 이것이 있으면 유도값을 공짜로 반증할 수 있다.  실측 2026-09-20: 원본 `.sh` 가
      `--step3-vox 0.4` 를 앞에, 진짜 값을 뒤에 둔다 (템플릿 기본값이 남은 형태).
      argparse 는 뒤가 이기지만 **그 규칙에 결론을 걸지 않는다** — 선언과 대조해
      어느 쪽이 이겼는지 실제로 확인한다.
    ⚠ 이 선언은 러너의 계약 검사기가 쓰는 바로 그 문자열이다.  ⛔ 2026-09-18 사고의
      근본 원인은 여기에 `ptfe_stamp` 가 **없어서** 검사 대상이 아니었던 것이다 —
      그래서 이 함수는 "선언에 없는 축" 을 통과로 읽지 않고 **호출자가 이름으로 본다**.
    """
    out = {}
    for i, t in enumerate(tokens):
        if t != '--expect-physics' or i + 1 >= len(tokens):
            continue
        for kv in tokens[i + 1].split(','):
            if '=' not in kv:
                continue
            k, v = kv.split('=', 1)
            k, v = k.strip(), v.strip()
            if v in ('True', 'False'):
                out[k] = (v == 'True')
            else:
                try:
                    out[k] = float(v)
                except ValueError:
                    out[k] = v
    return out


def verify_logs(rec, log_dir, expect=None, pattern='*.log'):
    """영수증(선언) ↔ 로그(결과) 대조 → `(problems, covered, uncovered, n_logs)`.

    ⚠ 로그에서 값을 **가져오지 않는다** — 대조만 한다."""
    import re as _re
    logs = sorted(glob.glob(os.path.join(log_dir, '**', pattern), recursive=True))
    problems, covered = [], set()
    if not logs:
        return [f'로그가 없다: {log_dir}'], covered, set(RC.RECEIPT_AXES), 0
    if expect is not None and len(logs) != expect:
        problems.append(f'로그가 {len(logs)} 개다 (기대 {expect})')
    for lp in logs:
        txt = open(lp, encoding='utf-8', errors='replace').read()
        name = os.path.basename(lp)
        m = _re.search(r'vox\s+([0-9.]+)\s*\u00b5m', txt)
        if m:
            covered.add('vox_um')
            if abs(float(m.group(1)) - float(rec['vox_um'])) > 1e-9:
                problems.append(f'{name}: vox {m.group(1)} ≠ 영수증 {rec["vox_um"]}')
        m = _re.search(r'\ube0c\ub9ac\uc9c0 \ubc18\uacbd \*\*\uace0\uc815\*\* ([0-9.]+)', txt)
        if m:
            covered.add('bridge_um')
            if abs(float(m.group(1)) - float(rec['bridge_um'])) > 1e-9:
                problems.append(f'{name}: bridge {m.group(1)} ≠ 영수증 {rec["bridge_um"]}')
        m = _re.search(r'\uc12c\uc720 \*\*(\uc120\ubd84|\uc810) \uc2a4\ud0ec\ud504\*\* ON', txt)
        if m:
            covered.add('fibre_stamp')
            got = 'segment' if m.group(1) == '\uc120\ubd84' else 'point'
            if got != rec['fibre_stamp']:
                problems.append(f'{name}: fibre_stamp {got} ≠ 영수증 {rec["fibre_stamp"]}')
        miss = [f for f in LOG_LEAN if f not in txt]
        if miss:
            problems.append(f'{name}: LEAN 플래그 없음 — {", ".join(miss)}')
    return problems, covered, set(RC.RECEIPT_AXES) - covered, len(logs)


def payload_calls(sh_dir):
    """`.sh` 디렉터리 → `[(경로, 토큰들)]`.  payload 호출이 없는 `.sh` 는 **이름으로 보고**한다.

    ⚠ 조용히 건너뛰지 않는다 — `phase_a_rerun_from_sh` 가 같은 이유로 그렇게 한다
      (킷 디렉터리에 `harvest.sh` 같은 것이 섞여 있고, 말없이 넘기면 "몇 개를 왜 안
      만들었는지" 가 사라진다 = 규율 ⑤ 의 false-green).
    """
    import phase_a_rerun_from_sh as RS
    hits, skipped = [], []
    for p in sorted(glob.glob(os.path.join(sh_dir, '**', '*.sh'), recursive=True)):
        text = open(p, encoding='utf-8', errors='replace').read()
        try:
            i, j = RS._cmd_span(text)
        except ValueError:
            skipped.append(os.path.basename(p))
            continue
        cmd = text[i:j].replace('\\\n', ' ')
        toks = shlex.split(cmd)
        #  `python3 …/mpm_webapp_payload.py` 앞부분을 떼어 argparse 가 볼 것만 남긴다
        for k, t in enumerate(toks):
            if t.endswith(PAYLOAD):
                toks = toks[k + 1:]
                break
        else:
            skipped.append(os.path.basename(p))
            continue
        hits.append((p, toks))
    return hits, skipped


def namespaces(token_lists, payload_dir=_SCR):
    """토큰 목록 → payload 네임스페이스 목록 (**진짜 파서**로)."""
    if not token_lists:
        return []
    r = subprocess.run([sys.executable, '-c', _PROBE], cwd=payload_dir,
                       input=json.dumps(token_lists), capture_output=True,
                       text=True, timeout=300)
    if r.returncode != 0:
        raise SystemExit('⛔ payload 파서를 못 잡았다 (rc=%d)\n%s'
                         % (r.returncode, (r.stderr or '').strip()[-800:]))
    for line in r.stdout.splitlines()[::-1]:
        if line.startswith('\x00JSON\x00'):
            return [argparse.Namespace(**d) for d in json.loads(line[6:])]
    raise SystemExit('⛔ 파서 출력이 없다:\n' + (r.stdout or '')[-500:])


def _axes_from_ns(ns):
    """네임스페이스 → `RECEIPT_AXES` dict.  **한 축이라도 못 채우면 거부한다.**"""
    inv = {}
    for cli, v in RC.CLI_ACCOUNTING.items():
        if not v:
            continue
        for ax in (v[1] or ()):
            inv.setdefault(ax, cli)
    rec, missing = {}, []
    for ax in RC.RECEIPT_AXES:
        if ax in _EXPLICIT:
            rec[ax] = _EXPLICIT[ax](ns)
            continue
        cli = inv.get(ax)
        dest = cli.lstrip('-').replace('-', '_') if cli else None
        if dest is None or not hasattr(ns, dest):
            missing.append(ax)
            continue
        val = getattr(ns, dest)
        rec[ax] = val if isinstance(val, (bool, str)) or val is None else float(val)
    if missing:
        raise SystemExit('⛔ CLI 에서 못 채운 영수증 축이 있다 — 손으로 채우지 않는다:\n  '
                         + '\n  '.join(missing)
                         + '\n  ⇒ run_contract.CLI_ACCOUNTING 에 그 축을 등재할 것.')
    return rec


def build(sh_dir, out, expect_arms=None, expect_backend='gpu', force=False,
          logs=None, log_glob='*.log'):
    hits, skipped = payload_calls(sh_dir)
    if not hits:
        raise SystemExit(f'⛔ {sh_dir}: payload 호출을 가진 `.sh` 가 없다')
    nss = namespaces([t for _, t in hits])
    axes = [_axes_from_ns(n) for n in nss]

    #  ① 모든 팔이 **같은 규약**이어야 한다 (섞인 디렉터리는 한 실험이 아니다)
    base = axes[0]
    for (p, _), a in zip(hits, axes):
        diff = [f'{k}: {a[k]!r} ≠ {base[k]!r}' for k in RC.RECEIPT_AXES if a[k] != base[k]]
        if diff:
            raise SystemExit(f'⛔ 팔마다 규약이 다르다 — 한 영수증으로 덮을 수 없다\n'
                             f'  {os.path.basename(p)}\n    ' + '\n    '.join(diff))

    #  ①b `--expect-physics` 선언과 대조 — 중복 플래그·순서 함정을 여기서 잡는다
    ep_cov = set()
    for (pth, toks), a in zip(hits, axes):
        dec = expect_physics(toks)
        for k, v in dec.items():
            if k not in RC.RECEIPT_AXES:
                continue
            ep_cov.add(k)
            got = a.get(k)
            same = (abs(float(got) - float(v)) <= 1e-9
                    if isinstance(v, float) and isinstance(got, (int, float))
                    else got == v)
            if not same:
                raise SystemExit(
                    f'⛔ `.sh` 의 --expect-physics 선언과 유도값이 다르다 — 영수증을 만들지 않는다\n'
                    f'  {os.path.basename(pth)}\n    {k}: 유도 {got!r} ≠ 선언 {v!r}\n'
                    f'  ⇒ 중복 플래그나 인자 순서를 의심할 것.')

    #  ② 봉인 (어댑터의 SEAL 을 그대로 쓴다 — 두 벌을 만들지 않는다)
    import phase_a_arms_from_payload as AD
    bad = [f'{k}={base.get(k)!r} (봉인 {v!r})' for k, v in AD.SEAL.items() if base.get(k) != v]
    if bad:
        raise SystemExit('⛔ `.sh` 가 봉인 축을 벗어났다 — 영수증을 만들지 않는다:\n  '
                         + '\n  '.join(bad))

    #  ③ origins = 사전등록 factorial 이어야 한다
    origins = sorted({tuple(round(float(x), 9) for x in (n.step3_origin_shift or (0., 0., 0.)))
                      for n in nss})
    want = RC.expected_origins_for(base['vox_um'])
    if origins != want:
        raise SystemExit('⛔ origin 집합이 사전등록 factorial 이 아니다\n'
                         f'  vox={base["vox_um"]}\n  얻음 {origins}\n  기대 {want}')

    if expect_arms is not None and len(hits) != expect_arms:
        raise SystemExit(f'⛔ 팔이 {len(hits)} 개다 (기대 {expect_arms}) — 부분집합으로 판정하지 않는다')

    rec = dict(base)
    rec['origins'] = [list(o) for o in origins]
    rec['arms'] = len(hits)
    rec['expect_backend'] = expect_backend
    #  ⚠ code_sha 는 `.sh` 가 주지 않으면 **null** 이다.  지어내지 않는다 (PASL-03).
    rec['code_sha'] = None
    rec['receipt_digest'] = RC.receipt_digest(rec)
    rec['declared_axes'] = sorted(ep_cov)          # `--expect-physics` 가 덮은 축
    #  ★ 출처를 영수증 자신에 박는다 — digest 밖이라 기존 해시를 안 건드린다
    h = hashlib.sha256()
    for p, _ in hits:
        h.update(open(p, 'rb').read())
    rec['derived_from'] = 'sh'
    rec['derived_sh_dir'] = os.path.abspath(sh_dir)
    rec['derived_sh_sha256'] = h.hexdigest()[:16]
    rec['derived_sh_files'] = len(hits)

    #  ⑤ 로그 교차검증 — **쓰기 전에** 한다 (어긋나면 영수증을 남기지 않는다)
    log_note = None
    if logs:
        probs, cov, unc, nlog = verify_logs(rec, logs, expect=expect_arms,
                                            pattern=log_glob)
        if probs:
            raise SystemExit('⛔ 로그와 어긋난다 — 영수증을 만들지 않는다 (%d 건):\n  %s'
                             % (len(probs), '\n  '.join(probs[:12])))
        log_note = (nlog, sorted(cov), sorted(unc))
        rec['verified_against_logs'] = nlog
        rec['verified_axes'] = sorted(cov)

    dst = os.path.join(out, 'run_receipt.json')
    if os.path.exists(dst) and not force:
        raise SystemExit(f'⛔ 이미 있다: {dst} — 덮으려면 --force (기존 영수증이 정본일 수 있다)')
    os.makedirs(out, exist_ok=True)
    json.dump(rec, open(dst, 'w', encoding='utf-8'), ensure_ascii=False,
              indent=1, sort_keys=True)
    return rec, dst, skipped, log_note


def _selftest():                                             # noqa: C901
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    import phase_a_arms_from_payload as AD
    chk('① 봉인·축·해시를 전부 남의 것에서 가져온다 (사본 없음)',
        AD.SEAL['ptfe_stamp'] == 'centerline'
        and 'vox_um' in RC.RECEIPT_AXES and callable(RC.receipt_digest))

    def mk_sh(d, name, origin, vox=0.15, ptfe='centerline', extra='',
              decoy=False, declare=None):
        """`decoy` = 실제 `.sh` 처럼 템플릿 기본값 `--step3-vox 0.4` 를 **앞에** 둔다."""
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, name)
        ox, oy, oz = origin
        dec = declare if declare is not None else (
            f'vox_um={vox},bridge_um=0.24,fibre_stamp=segment,'
            f'ptfe_stamp={ptfe},periodic_xy=False')
        open(p, 'w').write(
            '#!/bin/sh\nset -e\n'
            f'python3 /x/{PAYLOAD} '
            + ('--step3-vox 0.4 ' if decoy else '')
            + f'--step3-vox {vox} \\\n'
            f'  --step3-origin-shift {ox} {oy} {oz} \\\n'
            f'  --ptfe-stamp {ptfe} --sigma-ptfe 0 --step3-fibre-stamp segment \\\n'
            f'  --step3-bridge-um 0.24 {extra} --expect-physics {dec} --out /y/p2.json\n')
        return p

    h = round(0.15 / 2, 9)
    facto = [(x, y, z) for x in (0.0, h) for y in (0.0, h) for z in (0.0, h)]

    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            mk_sh(sh, f'p2_K_a{i}.sh', o)
        hits, skipped = payload_calls(sh)
        chk(f'② payload 호출 8 개를 찾는다 (건너뜀 {len(skipped)})',
            len(hits) == 8 and not skipped)

        open(os.path.join(sh, 'harvest.sh'), 'w').write('#!/bin/sh\necho hi\n')
        hits2, skipped2 = payload_calls(sh)
        chk('③ payload 가 아닌 `.sh` 는 **이름으로 보고**한다 (조용히 안 넘긴다)',
            len(hits2) == 8 and skipped2 == ['harvest.sh'])

        out = os.path.join(td, 'out')
        rec, dst, _, _ = build(sh, out, expect_arms=8)
        chk('④ 영수증을 쓴다 + 봉인 3 축이 맞다',
            os.path.exists(dst) and rec['ptfe_stamp'] == 'centerline'
            and rec['fibre_stamp'] == 'segment' and rec['bridge_um'] == 0.24)
        chk('⑤ origins 가 사전등록 factorial 8 개다',
            len(rec['origins']) == 8
            and sorted(map(tuple, rec['origins'])) == RC.expected_origins_for(0.15))
        chk('⑥ code_sha 를 지어내지 않는다 (null)', rec['code_sha'] is None)
        chk('⑦ digest 가 run_contract 의 것과 같다',
            rec['receipt_digest'] == RC.receipt_digest(rec))
        chk('⑧ 어댑터의 read_receipt 가 이 영수증을 받아들인다',
            AD.read_receipt(dst).get('ptfe_stamp') == 'centerline')
        try:
            build(sh, out, expect_arms=8)
            _dup = False
        except SystemExit:
            _dup = True
        chk('⑨ 이미 있으면 덮지 않는다 (--force 필요)', _dup)

    #  ── 음성 대조: 어긋난 것을 **거부**하는가 ───────────────────────────────
    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            mk_sh(sh, f'p2_K_a{i}.sh', o, ptfe=('off' if i == 3 else 'centerline'))
        try:
            build(sh, os.path.join(td, 'o'))
            bad = False
        except SystemExit as e:
            bad = '규약이 다르다' in str(e)
        chk('⑩ 한 팔만 `ptfe_stamp=off` 여도 거부한다', bad)

    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            mk_sh(sh, f'p2_K_a{i}.sh', o, ptfe='off')
        try:
            build(sh, os.path.join(td, 'o'))
            bad = False
        except SystemExit as e:
            bad = '봉인 축을 벗어났다' in str(e)
        chk('⑪ 전 팔이 `off` 면 봉인 이탈로 거부한다 (2026-09-18 사고)', bad)

    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto[:6]):
            mk_sh(sh, f'p2_K_a{i}.sh', o)
        try:
            build(sh, os.path.join(td, 'o'))
            bad = False
        except SystemExit as e:
            bad = 'factorial' in str(e)
        chk('⑫ origin 이 6 개뿐이면 factorial 아님으로 거부한다', bad)

    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            mk_sh(sh, f'p2_K_a{i}.sh', o)
        try:
            build(sh, os.path.join(td, 'o'), expect_arms=32)
            bad = False
        except SystemExit as e:
            bad = '부분집합' in str(e)
        chk('⑬ --expect-arms 가 다르면 거부한다', bad)

    #  ⛔⛔ payload 를 절대 안 연다 (`PA12-04` 순환 금지) — **행동으로** 검사한다.
    #    문자열 검사는 못 쓴다: 이 파일의 픽스처 이름이 `p2_…` 라 자기 자신에 걸린다
    #    (초판이 실제로 그렇게 FAIL 했다).  ⇒ 열면 반드시 터지는 함정을 놓는다 —
    #    `p2_*.json` 을 **디렉터리**로 만들면 어떤 읽기 경로든 IsADirectoryError 로 죽는다
    #    (root 로 돌면 chmod 000 은 안 막힌다).
    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            mk_sh(sh, f'p2_K_a{i}.sh', o)
        out = os.path.join(td, 'out')
        os.makedirs(out)
        for d in (sh, out):                       # 함정: 이름만 payload 인 디렉터리
            os.makedirs(os.path.join(d, 'p2_poison_a0.json'))
        try:
            rec2, _, _, _ = build(sh, out, expect_arms=8)
            trapped = rec2['ptfe_stamp'] == 'centerline'
        except (IsADirectoryError, PermissionError):
            trapped = False
        chk('⑭ payload(`p2_*.json`) 를 하나도 안 읽는다 (PA12-04 순환 금지)', trapped)

    #  ── 로그 교차검증 (실제 런 로그 문장으로) ──────────────────────────────
    REAL = ('  STEP3: 섬유 **선분 스탬프** ON — 도체점 1,067,455\n'
            '  STEP3: AM 접촉 브리지 반경 **고정** 0.24 µm (기본은 1.2·vox = 0.180)\n'
            '  STEP3 σ_e_eff = [봉인] S/cm  (vox 0.15µm, 46,926,476 dof, resid 1.0e-08)\n'
            '  STEP3: --no-collector — 집전체 건너뜀\n'
            '  STEP3: --no-ion — 이온 솔브 건너뜀\n'
            '  STEP3: --no-pore — pore-τ 건너뜀\n')
    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            mk_sh(sh, f'p2_K_a{i}.sh', o)
        lg = os.path.join(td, 'logs')
        os.makedirs(lg)
        for i in range(8):
            open(os.path.join(lg, f'a{i}.log'), 'w').write(REAL)
        rec3, _, _, note = build(sh, os.path.join(td, 'o'), expect_arms=8, logs=lg)
        chk('⑮ 실제 런 로그 문장과 대조 통과 + 덮은 축 3 개를 보고한다',
            note and note[0] == 8 and set(note[1]) == {'vox_um', 'bridge_um', 'fibre_stamp'})
        chk('⑯ 로그가 **못 덮는** 축을 이름으로 남긴다 (침묵 금지)',
            'ptfe_stamp' in note[2] and len(note[2]) >= 10)

        open(os.path.join(lg, 'bad.log'), 'w').write(REAL.replace('vox 0.15µm', 'vox 0.20µm'))
        try:
            build(sh, os.path.join(td, 'o2'), logs=lg)
            caught = False
        except SystemExit as e:
            caught = '로그와 어긋난다' in str(e)
        chk('⑰ 로그의 vox 가 다르면 영수증을 **안 쓴다**', caught
            and not os.path.exists(os.path.join(td, 'o2', 'run_receipt.json')))

        os.remove(os.path.join(lg, 'bad.log'))
        open(os.path.join(lg, 'lean.log'), 'w').write(REAL.replace('--no-ion', '--yes-ion'))
        try:
            build(sh, os.path.join(td, 'o3'), logs=lg)
            caught2 = False
        except SystemExit as e:
            caught2 = 'LEAN' in str(e)
        chk('⑱ LEAN 플래그가 빠진 로그가 하나라도 있으면 거부한다', caught2)

    #  ── `--expect-physics` 선언 대조 (실제 `.sh` 의 중복 플래그 함정 재현) ─────
    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            mk_sh(sh, f'p2_K_a{i}.sh', o, decoy=True)      # ← 0.4 를 앞에 둔다
        rec4, _, _, _ = build(sh, os.path.join(td, 'o'), expect_arms=8)
        chk('⑲ 중복 `--step3-vox 0.4 … 0.15` 에서 **뒤가 이긴다** (실제 `.sh` 형태)',
            abs(rec4['vox_um'] - 0.15) < 1e-12)
        chk('⑳ 선언(--expect-physics)이 덮은 축을 영수증에 남긴다',
            'vox_um' in rec4['declared_axes'] and 'ptfe_stamp' in rec4['declared_axes'])

    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            #  선언만 0.40 으로 어긋나게 — 미끼가 이겼을 때의 신호와 같다
            mk_sh(sh, f'p2_K_a{i}.sh', o, decoy=True,
                  declare='vox_um=0.40,bridge_um=0.24,fibre_stamp=segment')
        try:
            build(sh, os.path.join(td, 'o'))
            caught3 = False
        except SystemExit as e:
            caught3 = '--expect-physics 선언과 유도값이 다르다' in str(e)
        chk('㉑ 선언과 유도값이 다르면 거부한다 (중복 플래그가 이긴 경우를 잡는다)', caught3)

    #  ── 배치가 섞인 로그 디렉터리에서 `--log-glob` 으로 고른다 ────────────────
    with tempfile.TemporaryDirectory() as td:
        sh = os.path.join(td, 'sh')
        for i, o in enumerate(facto):
            mk_sh(sh, f'p2_K_a{i}.sh', o, decoy=True)
        lg = os.path.join(td, 'logs')
        os.makedirs(lg)
        for i in range(8):                                  # 우리 배치
            open(os.path.join(lg, f'v015.a{i}.log'), 'w').write(REAL)
        for i in range(8):                                  # 남의 배치 (vox 0.25)
            open(os.path.join(lg, f'v025.a{i}.log'), 'w').write(
                REAL.replace('vox 0.15µm', 'vox 0.25µm'))
        try:
            build(sh, os.path.join(td, 'x'), logs=lg)
            mixed_caught = False
        except SystemExit as e:
            mixed_caught = '로그와 어긋난다' in str(e)
        chk('㉒ 섞인 로그를 통째로 주면 거부한다 (조용히 통과 안 한다)', mixed_caught)
        _, _, _, note2 = build(sh, os.path.join(td, 'y'), expect_arms=8,
                               logs=lg, log_glob='v015.*.log')
        chk('㉓ --log-glob 으로 자기 배치만 골라 대조한다', note2 and note2[0] == 8)

    print(f'\nphase_a_receipt_from_sh selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description='Phase A 영수증을 `.sh` 에서 유도한다')
    ap.add_argument('--sh', help='재실행 `.sh` 디렉터리 (재귀)')
    ap.add_argument('--out', help='영수증을 쓸 payload 디렉터리')
    ap.add_argument('--expect-arms', type=int, default=None,
                    help='있어야 하는 팔 수 — 다르면 거부한다 (부분집합 방지)')
    ap.add_argument('--expect-backend', default='gpu')
    ap.add_argument('--logs', help='런 로그 디렉터리 — 영수증(선언)을 로그(결과)와 대조한다. '
                    '⚠ 로그에서 값을 가져오지 않는다 (PA12-04)')
    ap.add_argument('--log-glob', default='*.log',
                    help="로그 파일 패턴 — 한 디렉터리에 배치가 섞여 있을 때 (예: 'v015.*.log')")
    ap.add_argument('--force', action='store_true', help='기존 영수증을 덮는다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not (a.sh and a.out):
        ap.error('--sh 와 --out 이 필요하다')
    rec, dst, skipped, log_note = build(a.sh, a.out, a.expect_arms,
                                        a.expect_backend, a.force, a.logs,
                                        a.log_glob)
    print(f'영수증 → {dst}')
    for k in ('vox_um', 'ptfe_stamp', 'fibre_stamp', 'bridge_um', 'arms',
              'code_sha', 'receipt_digest', 'derived_sh_sha256'):
        print(f'  {k:20s} {rec.get(k)!r}')
    print(f'  origins              {len(rec["origins"])} 개')
    if log_note:
        n, cov, unc = log_note
        print(f'  ★ 선언(--expect-physics)이 덮은 축: {", ".join(rec["declared_axes"])}')
        print(f'  ★ 로그 {n} 개와 대조 통과 — 덮은 축 {", ".join(cov)}')
        print(f'  ⚠ 로그가 **못 덮는** 축 {len(unc)} 개 (어댑터가 팔마다 매니페스트로 본다): '
              f'{", ".join(unc)}')
    if skipped:
        print(f'  ⚠ payload 호출 없는 `.sh` {len(skipped)} 개: {", ".join(skipped[:6])}')
    if rec['code_sha'] is None:
        print('\n⚠ `code_sha` 가 null 이다 — 어댑터는 `--code-sha-missing-ok "<이유>"` 를 요구한다.')


if __name__ == '__main__':
    main()
