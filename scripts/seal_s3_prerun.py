#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S3 **런 전 봉인** — 계약 `docs/area_contract_20260913.md` §5-v4 A·B 를 파일로 찍는다.

    python3 scripts/seal_s3_prerun.py --webapp ~/lhs_local --dry-run   # 언제든 (안 쓴다)
    python3 scripts/seal_s3_prerun.py --webapp ~/lhs_local             # 2026-09-17 이후
    python3 scripts/seal_s3_prerun.py --selftest

═══ 무엇을 봉인하나 (§5-v4 B "S3 런 전에 봉인할 것") ══════════════════════════════════
  · 비교 세대 (git sha) · 코호트 TSV·설계 CSV 지문
  · **채널별 대상 ID** — `B_ch`(σ_old > 0 유효·유한) · `OLD_ZERO` · `OLD_NONE` ·
    `PENDING_BASELINE` · `NO_NETWORK` · `OLD_NONFINITE`
  · solver 환경 — scipy 판 · **실제 rtol/atol** · maxiter · 전처리기 · fallback ·
    **양쪽 최종 채택 상태**
  · ρ 집계식과 **순서통계 자리** (|B_ch| 가 정한다 — 옛 30건의 15·16번째를 옮겨 쓰지 않는다)

═══ 왜 날짜를 코드가 막나 ═══════════════════════════════════════════════════════════
§5-v4 D-3 은 *"baseline 봉인은 2026-09-17 이전에 하지 않는다"* 를 **런 전에** 등록했다 —
`lhs00_034·089·098` 이 아직 클러스터에서 돌고 있어 사흘을 준 것이다.  규칙이 문서에만
있으면 샌다 (CLAUDE.md ④, 실제로 `lhs00_029` 에서 겪었다) ⇒ **여기서 막는다.**
⛔ 이 날짜를 결과가 아쉬워서 앞당기지 말 것.  `--dry-run` 은 언제든 되고 아무것도 안 쓴다.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'

#: §5-v4 D-3 에 **런 전에** 등록된 수신 마감.  ⛔ 앞당기지 말 것.
SEAL_NOT_BEFORE = _dt.date(2026, 9, 17)

#: 채널별 분류 라벨.  `B_ch` 만 상대차 estimand 안이다.
IN_DOMAIN = 'B_ch'
LABELS = (IN_DOMAIN, 'OLD_ZERO', 'OLD_NONE', 'OLD_NONFINITE', 'NO_NETWORK', 'PENDING_BASELINE')


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SCRIPTS))
    spec.loader.exec_module(m)
    return m


def sha256(p) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def git_sha() -> str:
    return subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'],
                          capture_output=True, text=True).stdout.strip()


def classify(raw_ok: bool, net_ok: bool, sigma_old) -> str:
    """§5-v4 A 의 정의역 분류.  **순서가 곧 규칙이다.**

    ⚠ `PENDING_BASELINE`(원자료가 없어 baseline 자체가 미정)과 `OLD_NONE`(풀었는데 해가
      없다)은 **다른 상태**다.  섞으면 R3-01 이 지적한 그 혼동이 된다.
    """
    if not raw_ok:
        return 'PENDING_BASELINE'
    if not net_ok:
        return 'NO_NETWORK'
    if sigma_old is None:
        return 'OLD_NONE'
    try:
        v = float(sigma_old)
    except (TypeError, ValueError):
        return 'OLD_NONE'
    if not math.isfinite(v):
        return 'OLD_NONFINITE'
    if v <= 0.0:
        return 'OLD_ZERO'
    return IN_DOMAIN


def order_positions(n: int):
    """|B_ch| = n 일 때 중앙값이 쓰는 **순서통계 자리** (1-기준).

    ⚠ 짝수면 두 자리의 평균이다.  옛 30건 분석의 15·16번째를 새 집합에 그대로 쓰지 않는다
      (§5-v4 A-1) — 자리는 **그 집합의 크기**가 정한다.
    """
    if n <= 0:
        return []
    return [n // 2 + 1] if n % 2 else [n // 2, n // 2 + 1]


def read_cohort(tsv: Path):
    """봉인 TSV → {case: (status, raw_ok)}.  ⚠ 상태를 재판정하지 않고 **그대로 읽는다**."""
    rows, hdr = {}, None
    for ln in tsv.read_text(encoding='utf-8').split('\n'):
        if not ln.strip() or ln.startswith('#'):
            continue
        parts = ln.split('\t')
        if hdr is None:
            hdr = parts
            continue
        r = dict(zip(hdr, parts))
        rows[r['case']] = (r.get('status', ''), r.get('status', '') == 'RAW_OK')
    return rows


def build_seal(per_channel: dict, cohort: dict, env: dict, tsv: Path, design: Path,
               generation: str) -> dict:
    """분류 결과 → 봉인 문서.  **숫자를 만들지 않고 세기만 한다.**"""
    out = {
        'contract': 'docs/area_contract_20260913.md §5-v4 A·B',
        'sealed_utc': _dt.datetime.now(_dt.timezone.utc).isoformat(timespec='seconds'),
        'generation_git_sha': generation,
        'cohort_tsv': str(tsv), 'cohort_tsv_sha256': sha256(tsv) if tsv.exists() else '',
        'design_csv': str(design), 'design_csv_sha256': sha256(design) if design.exists() else '',
        'n_cohort_ids': len(cohort),
        'solver_env': env,
        'rho_rule': ('d ≥ 10 이고 d ≥ 2ρ → h1 · 그 외 ρ > 3 → UNRESOLVED_NUMERIC · '
                     '그 외 d < 3 → h0 · 나머지 BOTH_REJECTED  (d = median(|Δ|) %, 둘 다 유한 비음수)'),
        'undetermined_rule': ('B_ch 안의 REFUSED 는 하한 0 · 상한 +∞ 의 중앙값 순서통계 경계로 '
                              '두 라벨을 내고 **같을 때만** 발행한다 (다르면 UNDETERMINED_COHORT). '
                              '+∞ 는 경계 계산용이지 관측값이 아니다.'),
        'channels': {},
    }
    for ch, by_case in per_channel.items():
        groups = {lab: sorted(c for c, l in by_case.items() if l == lab) for lab in LABELS}
        n = len(groups[IN_DOMAIN])
        out['channels'][ch] = {
            'n_' + lab: len(groups[lab]) for lab in LABELS
        }
        out['channels'][ch]['median_order_positions_1based'] = order_positions(n)
        out['channels'][ch]['ids'] = groups
    return out


def _env_from_recorder(rec_calls: list) -> dict:
    """실제 솔버 호출 기록 → 봉인할 환경.  ⚠ **기본값을 적지 않고 실제 쓰인 값**을 적는다."""
    eff = [c for c in rec_calls if c.get('fn') == 'cg' and c.get('result') != 'TypeError']
    return {
        'n_cg_calls': len(eff),
        'fallback_seen': len(eff) > 1,
        'rtol_used': sorted({c.get('rtol_used') for c in eff if c.get('rtol_used') is not None}),
        'atol_used': sorted({c.get('atol_used') for c in eff if c.get('atol_used') is not None}),
        'maxiter': sorted({c.get('maxiter') for c in eff if c.get('maxiter') is not None}),
        'preconditioner': sorted({bool(c.get('M')) for c in eff}),
        'final_adopted_info': eff[-1].get('info') if eff else None,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='S3 런 전 봉인 (계약 §5-v4 A·B)')
    ap.add_argument('--webapp', default='', help='케이스 폴더 root (예: ~/lhs_local)')
    ap.add_argument('--cohort', default=str(ROOT / 'docs' / 'data' / 'area_s2_cohort.tsv'))
    ap.add_argument('--design-csv', default=str(ROOT / 'docs' / 'data' / 'lhs_design_20260818.csv'))
    ap.add_argument('--out', default=str(ROOT / 'docs' / 'data' / 's3_prerun_seal.json'))
    ap.add_argument('--channels', default='ion,electron,thermal')
    ap.add_argument('--dry-run', action='store_true', help='분류만 하고 **쓰지 않는다** (날짜 무관)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()

    today = _dt.date.today()
    if not a.dry_run and today < SEAL_NOT_BEFORE:
        print(f'⛔ 봉인 거부 — 계약 §5-v4 D-3 이 등록한 마감은 {SEAL_NOT_BEFORE} 이고 오늘은 {today} 다.')
        print('   lhs00_034·089·098 이 아직 돌고 있어 사흘을 준 것이다.  --dry-run 은 언제든 된다.')
        print('   ⛔ 이 날짜를 결과가 아쉬워서 앞당기지 말 것.')
        return 2
    if not a.webapp:
        ap.error('--webapp 이 필요하다 (또는 --selftest)')

    _S0 = _load('_s0_seal', SCRIPTS / 'audit_constriction_deleted.py')
    _RHO = _load('_rho_seal', SCRIPTS / 'measure_rho.py')
    import scipy
    cohort = read_cohort(Path(a.cohort))
    per_channel = {ch: {} for ch in a.channels.split(',')}
    env_seen, calls_all = {}, []
    root = Path(a.webapp).expanduser()
    for case, (_st, raw_ok) in sorted(cohort.items()):
        cdir = root / case
        for ch in per_channel:
            if not raw_ok or not cdir.is_dir():
                per_channel[ch][case] = 'PENDING_BASELINE'
                continue
            try:
                atoms, type_map, scale, _m, contacts, _src = _S0.load_case_any(cdir)
                mode, pick = _S0.CHANNELS[ch]
                net = _S0._NC.build_network(atoms, contacts, pick(type_map), scale, None,
                                            mode=mode, type_map=type_map, contact_mode='physics')
                if net is None:
                    per_channel[ch][case] = 'NO_NETWORK'
                    continue
                with _RHO._Recorder(_S0._NC) as rec:
                    _g, sig = _S0._NC.solve_network(net, mode='full')
                calls_all.extend(rec.calls)
                per_channel[ch][case] = classify(True, True, sig)
            except Exception as e:                        # 실패를 조용히 통과시키지 않는다
                per_channel[ch][case] = 'NO_NETWORK'
                print(f'  ⚠ {case}/{ch}: {type(e).__name__} {e}')
    env_seen = _env_from_recorder(calls_all)
    env_seen['scipy'] = scipy.__version__
    env_seen['python'] = sys.version.split()[0]
    seal = build_seal(per_channel, cohort, env_seen, Path(a.cohort), Path(a.design_csv), git_sha())
    for ch, d in seal['channels'].items():
        print(f"  {ch}: B_ch {d['n_B_ch']} · OLD_ZERO {d['n_OLD_ZERO']} · OLD_NONE {d['n_OLD_NONE']}"
              f" · PENDING {d['n_PENDING_BASELINE']} · 순서자리 {d['median_order_positions_1based']}")
    if a.dry_run:
        print('  (--dry-run — 아무것도 쓰지 않았다)')
        return 0
    Path(a.out).write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {a.out}')
    return 0


def _selftest() -> int:
    ok, fail = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        if cond:
            ok += 1
        else:
            fail.append(name)

    # ① 분류 — PENDING_BASELINE 과 OLD_NONE 은 **다른 상태**다 (R3-01 의 핵심)
    chk('① raw 없음 → PENDING_BASELINE', classify(False, True, 1.0) == 'PENDING_BASELINE')
    chk('①b 망 없음 → NO_NETWORK', classify(True, False, 1.0) == 'NO_NETWORK')
    chk('①c 해 없음 → OLD_NONE', classify(True, True, None) == 'OLD_NONE')
    chk('①d σ=0 → OLD_ZERO (상대차 정의역 밖)', classify(True, True, 0.0) == 'OLD_ZERO')
    chk('①e 음수도 OLD_ZERO 쪽 (σ_old > 0 만 정의역)', classify(True, True, -1e-9) == 'OLD_ZERO')
    chk('①f NaN → OLD_NONFINITE', classify(True, True, float('nan')) == 'OLD_NONFINITE')
    chk('①g inf → OLD_NONFINITE', classify(True, True, float('inf')) == 'OLD_NONFINITE')
    chk('①h 정상 → B_ch', classify(True, True, 1.2e-4) == IN_DOMAIN)
    chk('★①i raw 없음이 해 있음보다 **먼저** 걸린다 (섞으면 R3-01 의 혼동)',
        classify(False, True, 1.0) == 'PENDING_BASELINE')

    # ② 순서통계 자리 — **집합 크기가 정한다**
    chk('② n=130 이면 65·66번째', order_positions(130) == [65, 66])
    chk('②b n=127 이면 64번째', order_positions(127) == [64])
    chk('②c n=30 이면 15·16번째 (옛 분석이 쓰던 자리)', order_positions(30) == [15, 16])
    chk('②d n=0 이면 자리 없음', order_positions(0) == [])
    chk('★②e 옛 자리를 새 집합에 쓰지 않는다 (130 ≠ 30 의 자리)',
        order_positions(130) != order_positions(30))

    # ③ 날짜 게이트 — 계약 §5-v4 D-3 을 **코드가** 막는다
    import tempfile
    td = Path(tempfile.mkdtemp())
    rc = main(['--webapp', str(td), '--out', str(td / 'x.json')])
    early = _dt.date.today() < SEAL_NOT_BEFORE
    chk('③ 마감 전 봉인은 rc=2 로 거부 (오늘이 마감 전일 때만 유효한 검사)',
        (rc == 2) if early else True, f'today={_dt.date.today()} not_before={SEAL_NOT_BEFORE}')
    chk('③b 거부됐으면 파일을 쓰지 않았다', not (td / 'x.json').exists())

    # ④ 봉인 문서 — 세기만 하고 숫자를 만들지 않는다
    per = {'ion': {'a': IN_DOMAIN, 'b': 'OLD_NONE', 'c': 'PENDING_BASELINE', 'd': IN_DOMAIN}}
    seal = build_seal(per, {'a': ('', True), 'b': ('', True), 'c': ('', False), 'd': ('', True)},
                      {'scipy': '1.18.1'}, td / 'none.tsv', td / 'none.csv', 'deadbeef')
    ion = seal['channels']['ion']
    chk('④ B_ch 2 · OLD_NONE 1 · PENDING 1',
        (ion['n_B_ch'], ion['n_OLD_NONE'], ion['n_PENDING_BASELINE']) == (2, 1, 1))
    chk('④b 순서자리는 |B_ch| 가 정한다 (n=2 → 1·2번째)',
        ion['median_order_positions_1based'] == [1, 2])
    chk('④c ID 목록이 라벨마다 보존된다', ion['ids'][IN_DOMAIN] == ['a', 'd'])
    chk('④d 규칙 문구가 봉인에 들어간다 (+∞ 경계·ρ 순서)',
        '+∞' in seal['undetermined_rule'] and 'UNRESOLVED_NUMERIC' in seal['rho_rule'])
    chk('④e 세대(git sha)와 계약 참조가 들어간다',
        seal['generation_git_sha'] == 'deadbeef' and '§5-v4' in seal['contract'])

    # ⑤ 솔버 환경 — **실제 쓰인 값**만 적는다
    env = _env_from_recorder([{'fn': 'cg', 'rtol_used': 1e-5, 'atol_used': 1e-8, 'maxiter': None,
                               'M': False, 'info': 1},
                              {'fn': 'cg', 'rtol_used': 1e-5, 'atol_used': 1e-8, 'maxiter': 5000,
                               'M': True, 'info': 0}])
    chk('⑤ fallback 을 본다', env['fallback_seen'] is True and env['n_cg_calls'] == 2)
    chk('⑤b 최종 **채택** 해의 info (첫 해 1 이 아니라 0)', env['final_adopted_info'] == 0)
    chk('⑤c 전처리기 사용 여부가 둘 다 기록된다', env['preconditioner'] == [False, True])

    print('S3 런 전 봉인 SELFTEST', f'{ok} PASS', 'ALL GREEN' if not fail else f'FAIL {fail}')
    return 0 if not fail else 1


if __name__ == '__main__':
    raise SystemExit(main())
