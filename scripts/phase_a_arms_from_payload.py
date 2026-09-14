#!/usr/bin/env python3
"""Phase A 웹앱 payload → 판정기 팔 JSON **어댑터**.

    python3 scripts/phase_a_arms_from_payload.py --dir <payload> --out <팔 JSON>
    python3 scripts/phase_a_arms_from_payload.py --selftest

━━ 왜 필요한가 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
러너(`sdcp_gain_vox015_8arm.sh`)는 **웹앱 payload** 를 낸다 — `p2_*.json`, 팔당 150 MB,
`mpm_metrics.step3.*` 밑에 σ_e 가 들어 있다.  그런데 `phase_a_order_verdict.py` 는
**평평한 스키마**(`role`/`vgcf_wt`/`vox`/`origin`/`sigma_e`)를 읽는다.  판정기가 러너보다
먼저 쓰여서(2026-09-09) 그 사이를 잇는 것이 **없었다** — 32팔을 다 돌리고 나서야 드러났다.

⚠ 기존 `reduce_arm_payloads.py` 는 여기 못 쓴다.  그것은 **SBE/DBE 2역할 16팔 cohort**
전용이라 4조성 × 8 origin 을 *origin 중복* 으로 보고 진단 모드에서도 거부한다.  그 거부는
**옳다** (표지 없는 부분 cohort 가 `p2_*.json` 이름으로 리포에 들어가는 것을 막는 장치다).
⇒ 축소기를 고치는 것이 아니라 **다른 도구**가 필요했다.  이것이 그 도구다.

━━ 규율 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
★ **조성·격자·origin 을 파일명에서 읽지 않는다** (대상의 자기 신고 대신 원자료):
    vgcf_wt ← `mpm_metrics.additives.VGCF.wt_pct`
    vox     ← `…step3.vox_um`,  그리고 `…step3.manifest.vox_um` 과 **일치해야** 한다
    origin  ← `…step3.manifest.origin_shift_um` 을 `run_receipt.json` 의 `origins` 에서 찾은 **색인**
  파일명은 **교차확인용**으로만 쓴다 — `VGCF_PTFE_<k>_1` 의 k 가 매니페스트 wt% 와 어긋나면
  **거부**한다 (라벨 오류가 잡히는 자리이지, 파일명을 믿는 자리가 아니다).

★ **봉인 축을 매번 재확인한다** (사전등록 §5): `sigma_ptfe_S_cm == 0` · receipt 의
  `fibre_stamp=segment` · `ptfe_stamp=centerline` · `bridge_um=0.24` · `vox_um`.

⚠⚠ **수렴 표지가 없으면 거부한다.**  판정기는 `cg_info` 가 없으면 0(수렴)으로 읽는다
  (`int(a.get('cg_info', 0) or 0)`) — 즉 **모르는 것이 조용히 초록이 된다**.  이 어댑터는
  그 자리를 막는다: payload 에서 수렴 표지를 하나도 못 찾으면 `step3` 키 목록을 찍고
  **중단**한다.  "수렴했는지 알 수 없다" 가 "수렴했다" 로 승격되면 안 된다.

⚠ 이 도구는 **판정하지 않는다**.  팔 JSON 을 만들 뿐이고 판정은
  `phase_a_order_verdict.py --dir <out>` 이 한다 (설계 격자점이 비면 그쪽이 거부한다).
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import math
import os
import re
import subprocess
import sys

#: 사전등록 §5 봉인 축 (receipt 에서 확인).  ⚠ 결과를 보고 바꾸지 말 것.
SEAL = {'fibre_stamp': 'segment', 'ptfe_stamp': 'centerline', 'bridge_um': 0.24}

#: payload 에서 찾는 수렴 표지 (하나라도 있으면 통과, 전무하면 거부)
#  ⚠ 2026-09-12 (Codex PA12) — 러너가 실제로 쓰는 이름은 `cg_resid` 인데 이 목록에 없어서
#    **잔차가 안 옮겨졌다**.  h015 32팔의 잔차가 그렇게 사라졌고, payload 4.6 GB 를 지운 뒤
#    러너 로그에서 겨우 회수했다.  이름 변주를 넉넉히 받는다 — 빠뜨리면 조용히 사라진다.
CONV_KEYS = ('cg_info', 'unconverged', 'converged', 'resid', 'residual',
             'cg_resid', 'cg_residual', 'final_resid', 'max_resid',
             'n_iter', 'cg_iters', 'iters')

#: 팔의 역할.  ⚠ **하드코딩하지 않는다** — 옛 판은 `'role': 'primary'` 를 박아 두고 파일명에도
#  role 을 안 넣어서, QC 디렉터리를 같은 `--out` 으로 변환하면 **primary 팔을 그대로 덮었다**
#  (Codex PA12-05).  role 은 CLI/receipt 에서 오고, 파일명에 실리고, 덮어쓰기는 거부된다.
ROLES = ('primary', 'qc')

#: 파일명에서 조성을 읽는 **교차확인 전용** 패턴
FNAME_RE = re.compile(r'VGCF_PTFE_(\d+)_(\d+)')

_SCR = os.path.dirname(os.path.abspath(__file__))


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _get(d, *path, default=None):
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def _tool_sha():
    try:
        r = subprocess.run(['git', '-C', _SCR, 'rev-parse', 'HEAD'],
                           capture_output=True, text=True, timeout=10)
        return r.stdout.strip()[:12] if r.returncode == 0 else None
    except Exception:
        return None


def read_receipt(path):
    """receipt 를 읽고 봉인 축을 확인한다."""
    if not os.path.exists(path):
        raise SystemExit(f'⛔ receipt 가 없다: {path} — 봉인 축을 확인할 수 없으면 팔을 만들지 않는다')
    r = json.load(open(path))
    origins = r.get('origins')
    if not isinstance(origins, list) or not origins:
        raise SystemExit('⛔ receipt 에 origins 배열이 없다')
    if len({tuple(map(float, o)) for o in origins}) != len(origins):
        raise SystemExit('⛔ receipt 의 origins 에 중복이 있다')
    bad = [f'{k}={r.get(k)!r} (봉인 {v!r})' for k, v in SEAL.items() if r.get(k) != v]
    if bad:
        raise SystemExit('⛔ 봉인 축이 receipt 와 다르다 — 판정용 팔을 만들지 않는다:\n  '
                         + '\n  '.join(bad))
    return r


def _origin_index(shift, origins, tol=1e-9):
    for i, o in enumerate(origins):
        if len(o) == len(shift) and all(abs(float(a) - float(b)) <= tol
                                        for a, b in zip(o, shift)):
            return i
    return None


def arm_from_payload(d, receipt, fname, role='primary'):
    """payload 하나 → 평평한 팔 dict.  어긋나면 ValueError."""
    s = _get(d, 'mpm_metrics', 'step3')
    if not isinstance(s, dict):
        raise ValueError('mpm_metrics.step3 이 없다')
    man = s.get('manifest')
    if not isinstance(man, dict):
        raise ValueError('step3.manifest 가 없다')

    sig = s.get('sigma_e_eff_S_cm')
    if not isinstance(sig, (int, float)) or not math.isfinite(sig) or sig <= 0:
        raise ValueError(f'sigma_e_eff_S_cm 이 유한 양수가 아니다 ({sig!r})')

    vox, vox_m = s.get('vox_um'), man.get('vox_um')
    if vox is None or vox_m is None:
        raise ValueError('vox_um 이 step3 또는 manifest 에 없다')
    if abs(float(vox) - float(vox_m)) > 1e-12:
        raise ValueError(f'vox 가 step3({vox}) 와 manifest({vox_m}) 에서 다르다')

    sp = man.get('sigma_ptfe_S_cm')
    if sp is None or float(sp) != 0.0:
        raise ValueError(f'봉인 축 위반 — sigma_ptfe_S_cm={sp!r} (0 이어야 한다)')

    vg = _get(d, 'mpm_metrics', 'additives', 'VGCF')
    if not isinstance(vg, dict) or 'wt_pct' not in vg:
        raise ValueError('additives.VGCF.wt_pct 가 없다 — 조성을 파일명에서 읽지 않는다')
    wt = float(vg['wt_pct'])

    m = FNAME_RE.search(fname)
    if not m:
        raise ValueError(f'파일명에서 조성 토큰을 못 읽었다 ({fname}) — 교차확인 불가')
    if abs(float(m.group(1)) - wt) > 1e-9:
        raise ValueError(f'조성 불일치 — 파일명 {m.group(1)} wt% vs 매니페스트 {wt} wt%')
    pt = _get(d, 'mpm_metrics', 'additives', 'PTFE', 'wt_pct')
    if pt is None or abs(float(m.group(2)) - float(pt)) > 1e-9:
        raise ValueError(f'PTFE 불일치 — 파일명 {m.group(2)} wt% vs 매니페스트 {pt!r}')

    shift = man.get('origin_shift_um')
    if not isinstance(shift, (list, tuple)):
        raise ValueError('manifest.origin_shift_um 이 없다')
    oi = _origin_index([float(x) for x in shift], receipt['origins'])
    if oi is None:
        raise ValueError(f'origin_shift_um={list(shift)} 이 receipt 의 origins 에 없다')

    conv = {k: s[k] for k in CONV_KEYS if k in s}
    conv.update({k: man[k] for k in CONV_KEYS if k in man})
    if not conv:
        raise ValueError('수렴 표지가 없다 (' + '/'.join(CONV_KEYS) + ') — '
                         '모르는 것을 수렴으로 읽지 않는다.  step3 키: '
                         + ', '.join(sorted(s)[:30]))

    arm = {'role': role, 'vgcf_wt': wt, 'ptfe_wt': float(pt),
           'vox': float(vox), 'origin': oi, 'sigma_e': float(sig),
           'source_file': fname, 'origin_shift_um': [float(x) for x in shift],
           'sigma_vgcf_S_cm': man.get('sigma_vgcf_S_cm'),
           'vgcf_n_objects': vg.get('n_objects'),
           'input_digest': man.get('input_digest')}
    arm.update(conv)
    return arm


def build(d, out, receipt_path=None, role='primary', force=False):
    if role not in ROLES:
        raise SystemExit(f'⛔ 알 수 없는 role {role!r} — {ROLES}')
    receipt_path = receipt_path or os.path.join(d, 'run_receipt.json')
    receipt = read_receipt(receipt_path)
    r_role = receipt.get('role')
    if r_role is not None and r_role != role:
        raise SystemExit(f'⛔ receipt 의 role={r_role!r} 과 --role {role!r} 이 다르다 — '
                         '어느 쪽이 맞는지 사람이 정한다 (조용히 한쪽을 고르지 않는다)')
    #  ★ 한 출력 디렉터리에 역할을 섞지 않는다.  판정기는 `<out>/arms/*.json` 을 통째로
    #    읽으므로 섞이면 QC 가 주 판정에 들어간다.
    _sum = os.path.join(out, '_adapter_summary.json')
    if os.path.exists(_sum):
        try:
            prev = json.load(open(_sum)).get('role', 'primary')
        except Exception:
            prev = None
        if prev is not None and prev != role:
            raise SystemExit(f'⛔ {out} 은 이미 role={prev!r} 의 팔을 담고 있다 (지금 {role!r}) — '
                             '역할마다 --out 을 나눈다')
    files = sorted(p for p in glob.glob(os.path.join(d, 'p2_*.json')))
    if not files:
        raise SystemExit(f'⛔ {d} 에 p2_*.json 이 없다 — 빈 glob 로 진행하지 않는다')
    arms, bad, seen = [], [], {}
    for p in files:
        fn = os.path.basename(p)
        try:
            payload = json.load(open(p))
            a = arm_from_payload(payload, receipt, fn, role=role)
        except Exception as e:
            bad.append(f'{fn}: {e}')
            continue
        key = (round(a['vgcf_wt'], 6), round(a['vox'], 6), a['origin'])
        if key in seen:
            bad.append(f'{fn}: 설계 칸 중복 {key} (앞선 {seen[key]})')
            continue
        seen[key] = fn
        a['source_sha256'] = _sha256(p)
        arms.append(a)
    if bad:
        raise SystemExit('⛔ 읽을 수 없는 팔이 있다 — 하나라도 어긋나면 만들지 않는다:\n  '
                         + '\n  '.join(bad))
    # ★ 팔 디렉터리에는 **팔만** 둔다 — 판정기는 `*.json` 을 통째로 읽고 파싱 못 하는
    #   파일이 하나라도 있으면 거부한다 (fail-closed).  요약·receipt 를 섞으면 그 거부에
    #   걸린다 (2026-09-12 실측).  그래서 `<out>/arms/` 에 팔을, `<out>/` 에 메타를 둔다.
    adir = os.path.join(out, 'arms')
    os.makedirs(adir, exist_ok=True)
    #  ★ role 이 파일명에 실린다 (primary 는 기존 이름 유지 = 옛 32팔과 호환).
    #    그리고 **이미 있으면 거부한다** — 이름 규칙만으로는 실수를 못 막는다 (PA12-05).
    tgt = []
    for a in arms:
        tag = '' if a['role'] == 'primary' else f"{a['role']}_"
        tgt.append((a, os.path.join(
            adir, f"arm_{tag}w{a['vgcf_wt']:g}_v{a['vox']:g}_o{a['origin']}.json")))
    exist = [os.path.basename(n) for _, n in tgt if os.path.exists(n)]
    if exist and not force:
        raise SystemExit('⛔ 이미 있는 팔을 덮어쓰려 한다 — 다른 --out 을 쓰거나 --force:\n  '
                         + '\n  '.join(exist[:8])
                         + (f'\n  … 총 {len(exist)}개' if len(exist) > 8 else ''))
    for a, n in tgt:
        json.dump(a, open(n, 'w'), ensure_ascii=False, indent=1)
    json.dump(receipt, open(os.path.join(out, 'run_receipt.json'), 'w'),
              ensure_ascii=False, indent=1)
    summary = {'n_arms': len(arms), 'role': role, 'tool_sha': _tool_sha(),
               'receipt_digest': receipt.get('receipt_digest'),
               'receipt_code_sha': receipt.get('code_sha'),
               'seal': {k: receipt.get(k) for k in SEAL},
               'cells': sorted([a['vgcf_wt'], a['vox'], a['origin']] for a in arms),
               'sigma_e': {f"{a['vgcf_wt']:g}/{a['vox']:g}/{a['origin']}": a['sigma_e']
                           for a in arms}}
    summary['arms_dir'] = adir
    json.dump(summary, open(os.path.join(out, '_adapter_summary.json'), 'w'),
              ensure_ascii=False, indent=1)
    return arms, summary


# ───────────────────────────── selftest ─────────────────────────────
def _payload(wt=1.0, ptfe=1.0, vox=0.15, shift=(0.0, 0.0, 0.0), sig=0.002, **kw):
    man = {'vox_um': vox, 'origin_shift_um': list(shift), 'sigma_ptfe_S_cm': 0.0,
           'sigma_vgcf_S_cm': 78.5398, 'input_digest': 'abc123'}
    man.update(kw.pop('man', {}))
    s = {'sigma_e_eff_S_cm': sig, 'vox_um': vox, 'manifest': man, 'cg_info': 0}
    s.update(kw.pop('step3', {}))
    return {'mpm_metrics': {'step3': s,
                            'additives': {'VGCF': {'wt_pct': wt, 'n_objects': 1000},
                                          'PTFE': {'wt_pct': ptfe}}}}


def _selftest():
    import shutil
    import tempfile
    ok = [True]

    def chk(name, cond):
        print(('  ✓ ' if cond else '  ✗ ') + name)
        ok[0] &= bool(cond)

    origins = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.075], [0.0, 0.075, 0.0]]
    rcpt = {'origins': origins, 'receipt_digest': 'd0', 'code_sha': 'deadbeef',
            'fibre_stamp': 'segment', 'ptfe_stamp': 'centerline', 'bridge_um': 0.24}

    td = tempfile.mkdtemp()
    try:
        src, out = os.path.join(td, 'src'), os.path.join(td, 'out')
        os.makedirs(src)
        json.dump(rcpt, open(os.path.join(src, 'run_receipt.json'), 'w'))
        for k, wt in ((1, 1.0), (4, 4.0)):
            for i, sh in enumerate(origins):
                json.dump(_payload(wt=wt, shift=sh, sig=0.002 * (1 + k)),
                          open(os.path.join(src, f'p2_VGCF_PTFE_{k}_1_a{i}.json'), 'w'))
        arms, summ = build(src, out)
        chk('① 정상 경로 6팔', len(arms) == 6 and summ['n_arms'] == 6)
        chk('② origin 이 receipt 색인으로 매겨진다',
            sorted({a['origin'] for a in arms}) == [0, 1, 2])
        chk('③ 판정기 필수 키가 다 있다',
            all(all(k in a for k in ('role', 'vox', 'origin', 'sigma_e', 'vgcf_wt'))
                for a in arms))
        chk('④ 요약이 tool_sha·receipt 를 남긴다',
            'tool_sha' in summ and summ['receipt_code_sha'] == 'deadbeef')
        chk('⑮ 팔 디렉터리에 팔만 있다 (판정기가 *.json 을 통째로 읽는다)',
            sorted(os.listdir(os.path.join(out, 'arms'))) ==
            sorted(f"arm_w{a['vgcf_wt']:g}_v{a['vox']:g}_o{a['origin']}.json" for a in arms)
            and set(os.listdir(out)) == {'arms', 'run_receipt.json', '_adapter_summary.json'})

        def neg(name, mutate, src_extra=None):
            d2 = os.path.join(td, 'n_' + name)
            shutil.copytree(src, d2)
            mutate(d2)
            try:
                build(d2, os.path.join(td, 'o_' + name))
                chk(name, False)
            except SystemExit:
                chk(name, True)
            except Exception:
                chk(name, False)

        def _w(d2, fn, obj):
            json.dump(obj, open(os.path.join(d2, fn), 'w'))

        neg('⑤ 수렴 표지 없음 → 거부',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a0.json',
                          {'mpm_metrics': {'step3': {'sigma_e_eff_S_cm': 0.002,
                                                     'vox_um': 0.15,
                                                     'manifest': {'vox_um': 0.15,
                                                                  'origin_shift_um': [0.0, 0.0, 0.0],
                                                                  'sigma_ptfe_S_cm': 0.0}},
                                           'additives': {'VGCF': {'wt_pct': 1.0},
                                                         'PTFE': {'wt_pct': 1.0}}}}))
        neg('⑥ 파일명↔매니페스트 조성 불일치 → 거부',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a0.json', _payload(wt=3.0)))
        neg('⑦ sigma_ptfe ≠ 0 (봉인 위반) → 거부',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a0.json',
                          _payload(man={'sigma_ptfe_S_cm': 1.0})))
        neg('⑧ vox 가 step3↔manifest 에서 다름 → 거부',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a0.json',
                          _payload(man={'vox_um': 0.25})))
        neg('⑨ origin 이 receipt 에 없음 → 거부',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a0.json',
                          _payload(shift=(9.0, 9.0, 9.0))))
        neg('⑩ σ_e 비물리 → 거부',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a0.json', _payload(sig=0.0)))
        neg('⑪ 설계 칸 중복 → 거부',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a2.json', _payload(wt=1.0, shift=(0.0, 0.0, 0.0))))
        neg('⑫ receipt 봉인 축 위반 → 거부',
            lambda d2: json.dump({**rcpt, 'ptfe_stamp': 'volume'},
                                 open(os.path.join(d2, 'run_receipt.json'), 'w')))
        neg('⑬ receipt 없음 → 거부',
            lambda d2: os.remove(os.path.join(d2, 'run_receipt.json')))
        # ══ PA12-05 회귀 — QC 변환이 primary 를 덮으면 안 된다 ══
        qsrc = os.path.join(td, 'qsrc')
        os.makedirs(qsrc)
        json.dump(rcpt, open(os.path.join(qsrc, 'run_receipt.json'), 'w'))
        for k, wt in ((1, 1.0),):
            for i, sh in enumerate(origins):
                json.dump(_payload(wt=wt, shift=sh, sig=0.009),      # 다른 σ = 덮이면 티가 난다
                          open(os.path.join(qsrc, f'p2_VGCF_PTFE_{k}_1_a{i}.json'), 'w'))
        _pri = os.path.join(out, 'arms', 'arm_w1_v0.15_o0.json')
        _sig_before = json.load(open(_pri))['sigma_e']
        try:
            build(qsrc, out, role='qc')
            chk('⑯ QC 를 primary 디렉터리에 변환하면 거부된다', False)
        except SystemExit as e:
            chk('⑯ QC 를 primary 디렉터리에 변환하면 거부된다 (역할 혼합)',
                'role' in str(e))
        chk('⑰ ★ primary 팔의 σ 가 그대로다 (옛 판은 여기서 덮였다)',
            json.load(open(_pri))['sigma_e'] == _sig_before)
        qout = os.path.join(td, 'qout')
        qarms, qsumm = build(qsrc, qout, role='qc')
        chk('⑱ 별도 --out 이면 QC 가 만들어진다', len(qarms) == 3 and qsumm['role'] == 'qc')
        chk('⑲ ★ QC 파일명에 role 이 실린다 (primary 이름과 충돌 불가)',
            all(f.startswith('arm_qc_') for f in os.listdir(os.path.join(qout, 'arms'))))
        chk('⑳ 팔의 role 이 하드코딩 primary 가 아니다',
            all(a2['role'] == 'qc' for a2 in qarms))
        try:
            build(qsrc, qout, role='qc')
            chk('㉑ 같은 디렉터리 재변환은 거부된다 (덮어쓰기 금지)', False)
        except SystemExit as e:
            chk('㉑ 같은 디렉터리 재변환은 거부된다 (덮어쓰기 금지)', '덮어쓰' in str(e))
        chk('㉒ --force 면 통과한다 (의도적 재생성 경로는 남긴다)',
            len(build(qsrc, qout, role='qc', force=True)[0]) == 3)
        chk('㉓ ★ cg_resid 가 CONV_KEYS 에 있다 (h015 잔차가 이것 때문에 사라졌다)',
            'cg_resid' in CONV_KEYS)
        _r = arm_from_payload(_payload(man={'cg_resid': 9.9e-09}), rcpt,
                              'p2_VGCF_PTFE_1_1_a0.json')
        chk('㉔ cg_resid 가 팔로 실제로 옮겨진다', _r.get('cg_resid') == 9.9e-09)
        neg('⑭ 빈 glob → 거부',
            lambda d2: [os.remove(os.path.join(d2, f))
                        for f in os.listdir(d2) if f.startswith('p2_')])
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print('  ' + ('전부 통과' if ok[0] else '실패 있음'))
    return 0 if ok[0] else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='Phase A payload → 판정기 팔 JSON 어댑터 (판정은 안 한다)')
    ap.add_argument('--dir', help='payload 디렉터리 (p2_*.json + run_receipt.json)')
    ap.add_argument('--receipt', help='receipt 경로 (기본 <dir>/run_receipt.json)')
    ap.add_argument('--out', help='팔 JSON 을 쓸 디렉터리')
    ap.add_argument('--role', default='primary', choices=list(ROLES),
                    help='이 디렉터리의 팔 역할 (기본 primary).  QC 는 --role qc 로, '
                         '주 판정 디렉터리와 다른 --out 에 쓴다')
    ap.add_argument('--force', action='store_true',
                    help='이미 있는 팔을 덮어쓴다 (기본 거부 — PA12-05 재발 방지)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.dir or not a.out:
        raise SystemExit('--dir 와 --out 이 필요하다 (또는 --selftest)')
    arms, summ = build(a.dir, a.out, a.receipt, role=a.role, force=a.force)
    print(f'✓ 팔 {len(arms)} 개 → {a.out}')
    for w in sorted({x['vgcf_wt'] for x in arms}):
        g = sorted(x['sigma_e'] for x in arms if x['vgcf_wt'] == w)
        print(f'  VGCF {w:g} wt%  n={len(g)}  σ_e {g[0]:.6g} … {g[-1]:.6g} S/cm')
    print(f"  ★ 판정: python3 scripts/phase_a_order_verdict.py --dir {os.path.join(a.out, 'arms')}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
