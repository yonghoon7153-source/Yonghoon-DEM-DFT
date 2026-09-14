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


#: ★★ 2026-09-15 (`PA12-02`·`PA12-03`) — **계약을 여기서 다시 쓰지 않는다.**
#:   `run_contract` 가 이미 `expected_origins_for()`(사전등록 factorial)와
#:   `receipt_match()`(영수증 ↔ 매니페스트 축별 대조)를 갖고 있고 판정기도 그것을 쓴다.
#:   어댑터만 그 둘을 **안 부르고** 자기 판을 썼던 것이 PA12-02/03 의 실체다
#:   (규율 ①: "이 리포에 이미 있나" — 있었다).
#:   ⚠ 못 불러오면 **통과시키지 않는다** — 계약을 모르는 채 팔을 만드는 것이 이 도구가
#:     막으려는 바로 그것이다.
def _run_contract():
    import importlib.util as _ilu
    _p = os.path.join(_SCR, 'run_contract.py')
    if not os.path.exists(_p):
        raise SystemExit(f'⛔ run_contract.py 가 없다 ({_p}) — 실행 계약을 확인할 수 없으면 '
                         f'팔을 만들지 않는다')
    _s = _ilu.spec_from_file_location('_rc_for_adapter', _p)
    _m = _ilu.module_from_spec(_s)
    _s.loader.exec_module(_m)
    for _fn in ('expected_origins_for', 'receipt_match'):
        if not hasattr(_m, _fn):
            raise SystemExit(f'⛔ run_contract 에 {_fn} 이 없다 — 계약이 갈렸다')
    return _m


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
    #  ⛔⛔ **정정 2026-09-15 (`PA12-03`)** — 옛 판은 shift 가 **receipt 의 배열에 있나**만 봤다.
    #    그러면 영수증이 애초에 **잘못된 8점**(예: 반-복셀이 아닌 h, 축 편향 z-only)을 담고
    #    있어도 통과하고, 영수증의 **순서만 바꿔도** origin 색인이 뒤집혀 판정이 달라진다.
    #    ⇒ 두 겹으로 막는다: ⓐ 영수증의 origins 집합이 그 vox 의 **사전등록 factorial 과 같아야**
    #      하고 ⓑ 색인을 배열 위치가 아니라 **정렬된 정본 집합**에서 뽑는다 (순서 무관).
    _rc = _run_contract()
    _exp = _rc.expected_origins_for(float(vox))
    if not _exp:
        raise ValueError(f'vox={vox} 에 대한 사전등록 origin factorial 을 계산할 수 없다')
    _got = sorted({tuple(round(float(x), 9) for x in o) for o in receipt['origins']})
    if _got != sorted(_exp):
        raise ValueError(
            f'봉인 축 위반 — receipt 의 origins 가 vox={vox} 의 사전등록 factorial 이 아니다.\n'
            f'  기대 {sorted(_exp)}\n  실제 {_got}\n'
            f'  ⇒ 개수만 맞는 임의의 8점은 위상 앙상블이 아니다 (PA12-03)')
    _key = tuple(round(float(x), 9) for x in shift)
    _canon = sorted(_exp)
    if _key not in _canon:
        raise ValueError(f'origin_shift_um={list(shift)} 이 사전등록 factorial 에 없다 — '
                         f'기대 {_canon}')
    oi = _canon.index(_key)          # ★ 배열 위치가 아니라 정본 집합의 색인 (순열에 불변)

    #  ⛔⛔ **정정 2026-09-15 (`PA12-02`)** — 옛 판은 SEAL 을 **receipt 에만** 물었다.
    #    그러면 *영수증은 정상인데 payload 는 다른 규약으로 돈* 팔이 통과한다.
    #    ⇒ payload 자신의 매니페스트를 영수증과 **축별로** 대조한다 (`run_contract.receipt_match`).
    _ok, _why = _rc.receipt_match(receipt, man, origin=[float(x) for x in shift])
    if not _ok:
        raise ValueError(f'영수증 ↔ payload 매니페스트 불일치 — {_why} (PA12-02)')

    #  ★ `PA12-08` — `add_rng_per_phase` 가 기록만 되고 판정 경로로 안 왔다.  팔에 싣는다.
    #    ⚠ **없으면 None 을 싣는다** (거부하지 않는다) — 옛 세대 payload 에는 이 칸이 없고,
    #      그것을 거부하면 이미 돈 팔을 못 판정한다.  대신 아래 `build()` 가 **팔들 사이의
    #      불일치**를 거부한다 = 섞인 세대가 한 판정에 들어가는 것을 막는다.
    _rng = man.get('add_rng_per_phase')
    if _rng is None:
        _rng = _get(d, 'mpm_metrics', 'add_rng_per_phase')

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
           'input_digest': man.get('input_digest'),
           #  PA12-08 — 판정 경로로 나른다 (build 가 팔 사이 불일치를 거부한다)
           'add_rng_per_phase': _rng,
           #  PA12-04 — 조성 교차확인이 독립이 아니므로(둘 다 같은 producer 가 썼다)
           #  **다른 축**을 하나 더 싣는다: 코드 세대.  영수증의 code_sha 와 대조된다.
           'code_sha': man.get('code_sha') or _get(d, 'mpm_metrics', 'code_sha')}
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

    #  ★★ **`PA12-08`** — 세대 축이 팔들 사이에서 갈리면 한 판정에 **섞인 세대**가 들어간다.
    #    `add_rng_per_phase` 는 상별 난수 배정을 바꾸므로 침대가 달라진다.
    #    ⚠ `None`(옛 세대, 그 칸이 없던 payload)은 **한 값으로 본다** — 없는 것과 다른 것은
    #      다르고, 전부 없으면 그것은 일관된 옛 세대다.  섞이면 거부한다.
    _rngs = {json.dumps(a.get('add_rng_per_phase'), sort_keys=True) for a in arms}
    if len(_rngs) > 1:
        raise SystemExit('⛔ `add_rng_per_phase` 가 팔마다 다르다 — 상별 난수 배정이 갈리면 '
                         '침대가 다른 물건이다.  한 판정에 섞지 않는다 (PA12-08):\n  '
                         + '\n  '.join(sorted(_rngs)[:6]))
    #  ★ **`PA12-04`** — 조성 교차확인은 **독립이 아니다** (파일명과 매니페스트를 같은 producer 가
    #    썼다).  그래서 **다른 축**을 하나 요구한다: 코드 세대가 팔들 사이에 같아야 하고,
    #    영수증이 `code_sha` 를 적었으면 그것과도 같아야 한다.
    #    ⚠ 이것이 PA12-04 를 **닫지는 않는다** — 같은 producer 가 code_sha 도 쓴다.  다만
    #      "한 배치가 한 세대로 돌았나" 는 독립적으로 확인된다.  진짜 독립 확인은 계산기
    #      바깥의 소스 번들 해시이고 그것은 아직 없다.
    _shas = {a.get('code_sha') for a in arms}
    if len(_shas) > 1:
        raise SystemExit('⛔ `code_sha` 가 팔마다 다르다 — 한 배치가 두 세대로 돌았다 '
                         f'(PA12-04): {sorted(str(s)[:12] for s in _shas)}')
    _r_sha = receipt.get('code_sha')
    _a_sha = next(iter(_shas)) if _shas else None
    if _r_sha and _a_sha and str(_r_sha)[:12] != str(_a_sha)[:12]:
        raise SystemExit(f'⛔ 영수증의 code_sha({str(_r_sha)[:12]}) 와 payload 의 '
                         f'({str(_a_sha)[:12]}) 가 다르다 — 러너 의도와 실제가 갈렸다 (PA12-04)')
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
    #  ★★ **`PA12-06`** — 옛 판은 **이름이 같은** 팔만 거부했다.  그래서 같은 `--out` 을 다시 쓰면
    #    이번 배치에 **없는** 설계 칸을 **지난 배치의 팔이 조용히 메웠고**, 판정기는
    #    `<out>/arms/*.json` 을 통째로 읽으므로 *지금 입력 목록과 판정 대상이 달라졌다*.
    #    (`--force` 는 덮어쓰기만 허용했을 뿐 이 유령 팔을 지우지 않는다 = 더 나쁘다.)
    #    ⇒ 디렉터리에 있는 팔 중 **이번 배치가 만들 목록에 없는 것**을 세어 거부한다.
    _want = {os.path.basename(n) for _, n in tgt}
    _have = {os.path.basename(p) for p in glob.glob(os.path.join(adir, '*.json'))}
    _orphan = sorted(_have - _want)
    if _orphan:
        raise SystemExit(
            f'⛔ {adir} 에 **이번 배치가 만들지 않는 팔 {len(_orphan)}개**가 이미 있다 — '
            f'판정기는 이 디렉터리를 통째로 읽으므로 지난 배치가 설계 칸을 메운다 (PA12-06).\n'
            f'  ⇒ 빈 --out 을 쓰거나 그 파일들을 먼저 치운다.  `--force` 로는 안 열린다 '
            f'(덮어쓰기와 유령 팔은 다른 문제다).\n  '
            + '\n  '.join(_orphan[:8])
            + (f'\n  … 외 {len(_orphan) - 8}개' if len(_orphan) > 8 else ''))
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
    #  ⚠ **픽스처는 실물을 닮아야 한다** (2026-09-15).  옛 판의 매니페스트는 봉인 축을
    #    거의 안 담고 있었는데, `receipt_match` 를 배선하자마자 그것이 드러났다 —
    #    *"러너는 bridge_um 을 정했는데 매니페스트에 기록이 없다"*.
    #    ★ **실물로 확인했다**: `docs/data/phase_a_h015_arms/` 의 진짜 매니페스트는 영수증이
    #      선언한 축을 **전부** 갖고 있고 `receipt_match` 가 `True` 를 낸다.  즉 이 게이트는
    #      생산 팔을 거부하지 않는다 — 부실했던 것은 **픽스처**였다.
    #    ⇒ 픽스처에 봉인 축을 채운다.  그러지 않으면 "실물은 통과하는데 검사기는 빨간불" 이
    #      되어, 다음 사람이 게이트를 **느슨하게** 고치는 쪽으로 간다 (거꾸로다).
    man = {'vox_um': vox, 'origin_shift_um': list(shift), 'sigma_ptfe_S_cm': 0.0,
           'sigma_vgcf_S_cm': 78.5398, 'input_digest': 'abc123',
           'fibre_stamp': 'segment', 'ptfe_stamp': 'centerline', 'bridge_um': 0.24,
           'code_sha': 'deadbeef', 'add_rng_per_phase': True}
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

    #  ⛔⛔ **픽스처 정정 2026-09-15 (`PA12-03`)** — 옛 픽스처는 origin 을 **3점**
    #    `[000, 00h, 0h0]` 으로 뒀다.  그것은 사전등록 factorial `{0, vox/2}³` 의 **부분집합**이라
    #    *잘못된 origin 집합을 정상 증인으로 고정하고* 있었다 — `R5CX-04` 가 판정기 픽스처에서
    #    찾은 것과 **같은 부류**이고, 그래서 새 게이트를 넣자마자 이 픽스처가 먼저 걸렸다.
    #    ⇒ 픽스처를 **정본 계약에서 계산해** 쓴다 (손으로 적으면 또 갈린다, 규율 ①).
    origins = [list(o) for o in _run_contract().expected_origins_for(0.15)]
    assert len(origins) == 8, origins        # 계약이 8점이 아니면 픽스처가 거짓말을 한다
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
        #  ⚠ 픽스처가 3 origin → **8 origin**(정본 factorial)으로 바뀌었으므로 2조성 × 8 = 16 팔이다.
        chk('① 정상 경로 16팔 (2조성 × 사전등록 8 origin)',
            len(arms) == 16 and summ['n_arms'] == 16)
        chk('② origin 이 **정렬된 정본 집합**의 색인으로 매겨진다 (배열 위치가 아니다)',
            sorted({a['origin'] for a in arms}) == list(range(8)))
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
        chk('⑱ 별도 --out 이면 QC 가 만들어진다 (1조성 × 사전등록 8 origin)',
            len(qarms) == len(origins) and qsumm['role'] == 'qc')
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
            len(build(qsrc, qout, role='qc', force=True)[0]) == len(origins))
        chk('㉓ ★ cg_resid 가 CONV_KEYS 에 있다 (h015 잔차가 이것 때문에 사라졌다)',
            'cg_resid' in CONV_KEYS)
        _r = arm_from_payload(_payload(man={'cg_resid': 9.9e-09}), rcpt,
                              'p2_VGCF_PTFE_1_1_a0.json')
        chk('㉔ cg_resid 가 팔로 실제로 옮겨진다', _r.get('cg_resid') == 9.9e-09)
        neg('⑭ 빈 glob → 거부',
            lambda d2: [os.remove(os.path.join(d2, f))
                        for f in os.listdir(d2) if f.startswith('p2_')])

        #  ── 새 게이트의 음성 대조 (2026-09-15, PA12-02/03/06/08) ────────────────
        #  ⚠ 통과만 하는 검사는 없는 것과 같다 (`PA12-09` 의 교훈) — 각 게이트를
        #    **퇴행시키는 변이**를 하나씩 주고 실제로 빨간불이 나는지 본다.
        def _rc_mut(d2, **kw):
            r2 = dict(rcpt); r2.update(kw); _w(d2, 'run_receipt.json', r2)

        #  ★ PA12-03 ⓐ — 영수증이 **부분집합**(개수만 적은 8점 아님)을 담으면 거부
        neg('㉕ ★★ 영수증 origins 가 사전등록 factorial 이 아니면 거부 (부분집합)',
            lambda d2: _rc_mut(d2, origins=origins[:3]))
        #  ★ PA12-03 ⓐ — **개수는 8인데 점이 틀린** 경우 (z-only 편향).  R5CX-04 와 같은 변이.
        neg('㉖ ★★ 개수만 8인 z-only 점은 위상 앙상블이 아니다 → 거부',
            lambda d2: _rc_mut(d2, origins=[[0.0, 0.0, 0.075 * i / 7] for i in range(8)]))
        #  ★ PA12-02 — payload 매니페스트가 영수증과 **다른 규약**으로 돌았으면 거부
        neg('㉗ ★★ 매니페스트의 bridge_um 이 영수증과 다르면 거부 (영수증만 정상인 팔)',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a0.json',
                          _payload(shift=origins[0], man={'bridge_um': 0.48})))
        #  ★ PA12-02 — 영수증이 선언한 축의 **기록이 없으면** 통과가 아니다
        neg('㉘ ★ 매니페스트에 봉인 축 기록이 없으면 거부 (없는 것은 통과가 아니다)',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a1.json',
                          {'mpm_metrics': {
                              'step3': {'sigma_e_eff_S_cm': 0.002, 'vox_um': 0.15,
                                        'cg_info': 0,
                                        'manifest': {'vox_um': 0.15,
                                                     'origin_shift_um': list(origins[1]),
                                                     'sigma_ptfe_S_cm': 0.0}},
                              'additives': {'VGCF': {'wt_pct': 1.0}, 'PTFE': {'wt_pct': 1.0}}}}))
        #  ★ PA12-08 — 상별 난수 배정이 팔마다 다르면 침대가 다른 물건이다
        neg('㉙ ★★ `add_rng_per_phase` 가 팔마다 다르면 거부 (섞인 세대)',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a2.json',
                          _payload(shift=origins[2], man={'add_rng_per_phase': False})))
        #  ★ PA12-04 — 한 배치가 두 코드 세대로 돌았으면 거부
        neg('㉚ ★ `code_sha` 가 팔마다 다르면 거부 (두 세대가 섞였다)',
            lambda d2: _w(d2, 'p2_VGCF_PTFE_1_1_a3.json',
                          _payload(shift=origins[3], man={'code_sha': 'feedface'})))

        #  ★★ PA12-06 — **유령 팔**.  이번 배치가 만들지 않는 팔이 디렉터리에 있으면,
        #    판정기가 그것까지 읽어 지난 배치가 설계 칸을 메운다.  `--force` 로도 안 열린다.
        _g = os.path.join(td, 'ghost')
        os.makedirs(os.path.join(_g, 'arms'))
        json.dump({'role': 'primary', 'vgcf_wt': 9.0, 'vox': 0.15, 'origin': 0,
                   'sigma_e': 0.5},
                  open(os.path.join(_g, 'arms', 'arm_w9_v0.15_o0.json'), 'w'))
        for _fc, _lbl in ((False, '기본'), (True, '--force')):
            try:
                build(src, _g, force=_fc)
                chk(f'㉛ ★★ 유령 팔이 있으면 거부 ({_lbl}) — PA12-06', False)
            except SystemExit as e:
                chk(f'㉛ ★★ 유령 팔이 있으면 거부 ({_lbl}) — PA12-06', 'PA12-06' in str(e))
        #  ★ 판별력 — 유령을 치우면 같은 배치가 **통과해야** 한다 (과잉차단 아님).
        os.remove(os.path.join(_g, 'arms', 'arm_w9_v0.15_o0.json'))
        chk('㉜ ★ 유령을 치우면 같은 배치가 통과한다 (과잉차단 음성 대조)',
            len(build(src, _g)[0]) == len(origins) * 2)
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
