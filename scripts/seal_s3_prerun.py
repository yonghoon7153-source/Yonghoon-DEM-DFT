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

#: ★★ **저자 결정 2026-09-15 (`R4-07`)** — 고정 수신 종료 시각.
#:   계약 `D-3` 은 *"봉인 순간을 마감으로 삼되 09-17 이전에는 봉인하지 않는다"* 였고, 코드는
#:   **최초 허용일만** 봤다.  그래서 09-17·18·20 중 언제 멈출지가 열려 있었고 — 수신 상황과
#:   baseline 분류를 본 뒤 시점을 고를 여지가 남았다.  그것이 사전등록의 훼손이다.
#:   ⛔ **에이전트가 임의로 시각을 정하면 안 되는 항목**이라 저자에게 물었고, 답은
#:      **2026-09-17 23:59 KST 고정** 이다 (*"더 땅기는거면 내가 얘기할게"*).
#:   ⇒ 이제 허용 구간이 **양쪽으로 닫힌 창**이다.  이르면 거부, 지나면 거부.
#:   ⚠ 이 값을 **결과가 아쉬워서 움직이지 말 것.**  옮기려면 저자가 원장에 먼저 적는다.
KST = _dt.timezone(_dt.timedelta(hours=9))
SEAL_DEADLINE = _dt.datetime(2026, 9, 17, 23, 59, 0, tzinfo=KST)

#: 채널별 분류 라벨.  `B_ch` 만 상대차 estimand 안이다.
IN_DOMAIN = 'B_ch'
#: ★★ `ERROR` 신설 2026-09-15 (`R4-01` ⓒ) — **기술 실패를 물리 상태로 둔갑시키지 않는다.**
#:   옛 판은 예외를 전부 `NO_NETWORK` 로 바꿨다 ⇒ KeyError·NoneType 산술이 *"물리적으로 망이
#:   없음"* 으로 읽히고 세 `B_ch` 가 0개인 채로 봉인이 `rc=0` 으로 나갔다.
#:   `ERROR` 가 하나라도 있으면 **실행 허가 봉인을 발행하지 않는다** (아래 `main`).
LABELS = (IN_DOMAIN, 'OLD_ZERO', 'OLD_NONE', 'OLD_NONFINITE', 'NO_NETWORK',
          'PENDING_BASELINE', 'ERROR')


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
    """봉인 TSV → `{case: row}` (전 열 보존).  ⚠ 상태를 재판정하지 않고 **그대로 읽는다**.

    ⛔⛔ **정정 2026-09-15 (`R4-02`)** — 옛 판은 `case`/`status` **두 칸만** 남기고
    `atom_file`·`atom_sha256`·`contact_file`·`contact_sha256`·`deck_sha256` 를 **버렸다**.
    그러면 loader 가 현재 폴더에서 파일을 **다시 발견**하므로, 봉인이 인용한 지문과 실제로
    읽은 파일이 달라질 수 있다.  실측 반례: step 100 쌍을 봉인한 뒤 같은 폴더에 step 200 을
    넣으면 **TSV SHA 는 불변인데 loader 는 step 200 을 읽고 봉인은 rc=0** 이었다.
    ★ 지문은 **이미 TSV 에 있었다** — 버린 것이 문제였다.  ⇒ 전 열을 보존하고 아래
      `verify_provenance()` 가 *실제로 읽은 파일*을 그 지문에 대고 맞춘다.
    ⚠ **중복 ID 는 마지막 행이 이기게 두지 않는다** — 겹치면 그대로 올려 부르는 쪽이 거부한다.
    """
    rows, hdr, dups = {}, None, []
    for ln in tsv.read_text(encoding='utf-8').split('\n'):
        if not ln.strip() or ln.startswith('#'):
            continue
        parts = ln.split('\t')
        if hdr is None:
            hdr = parts
            continue
        r = dict(zip(hdr, parts))
        cid = r.get('case', '')
        if cid in rows:
            dups.append(cid)
        rows[cid] = r
    if dups:
        raise ValueError(f'코호트 TSV 에 중복 ID {sorted(set(dups))} — 마지막 행이 덮어쓰면 '
                         f'봉인 대상이 조용히 바뀐다 (R4-02)')
    return rows


def split_cohort(rows: dict, design_csv: Path):
    """코호트를 **설계 130 (주)** 와 **등록 밖 rogue** 로 가른다 → `(main, rogue)`.

    ★ `R4-02` 의 필수 조건: *"주 코호트 ID 는 설계 130개와 정확히 같고 각 1회 · `perc` 는
      주 집합 **밖**에 별도 보관"*.  옛 판은 `perc` 까지 **131개를 주 코호트로 순회**했다.
    ⚠ 설계 CSV 가 없거나 비면 **거부한다** — 빈 설계로 `n_cohort_ids=0` 봉인이 rc=0 으로
      나가던 자리가 그것이다 (*"없는 것은 통과가 아니다"*).
    """
    if not design_csv.exists():
        raise ValueError(f'설계 CSV 가 없다: {design_csv} — 등록 집합을 모르면 봉인하지 않는다')
    import csv as _csv
    with design_csv.open(encoding='utf-8') as fh:
        design = [r['case_id'] for r in _csv.DictReader(fh) if r.get('case_id')]
    if not design:
        raise ValueError(f'설계 CSV 에 case_id 가 0개다: {design_csv}')
    if len(set(design)) != len(design):
        raise ValueError('설계 CSV 에 중복 case_id 가 있다')
    dset = set(design)
    main = {c: r for c, r in rows.items() if c in dset}
    rogue = {c: r for c, r in rows.items() if c not in dset}
    missing = sorted(dset - set(main))
    if missing:
        raise ValueError(f'설계 {len(dset)}개 중 코호트에 없는 ID {len(missing)}개: '
                         f'{missing[:8]} — 등록 집합이 다 안 왔으면 봉인하지 않는다 (R4-02)')
    return main, rogue


#: TSV 가 적어 둔 지문과 **실제로 읽은 파일**을 맞춘다.  다르면 그 케이스는 `ERROR` 다.
_PROV_PAIRS = (('atom_file', 'atom_sha256'), ('contact_file', 'contact_sha256'),
               ('deck', 'deck_sha256'))


def verify_provenance(row: dict, prov: dict, root: Path):
    """→ `None` 이면 일치, 문자열이면 불일치 사유.

    ★ `R4-02` 의 핵심: *"계산은 **지정 세대의 실제 경로와 원 바이트 SHA 를 검증한 파일만**
      사용"*.  loader 가 폴더에서 재발견한 파일이 TSV 의 지문과 같은지를 본다.
    ⚠ **TSV 에 지문이 없으면 통과가 아니다** — 무엇을 읽었는지 확정할 수 없으면 거부다.
    """
    bad = []
    for fkey, skey in _PROV_PAIRS:
        want_f, want_s = (row.get(fkey) or '').strip(), (row.get(skey) or '').strip()
        got_f = (prov.get(fkey) or '').strip()
        if not want_f and not got_f:
            continue                       # 그 갈래를 안 쓴 케이스 (예: deck 없이 csv 경로)
        if not want_s:
            bad.append(f'{skey} 가 TSV 에 없다 (읽은 것: {got_f or "—"})')
            continue
        #  경로는 root 기준 상대·절대가 섞일 수 있으니 **파일명**으로 맞춘다.
        if got_f and Path(want_f).name != Path(got_f).name:
            bad.append(f'{fkey}: 봉인 {Path(want_f).name} ≠ 읽은 {Path(got_f).name}')
            continue
        cand = Path(got_f) if got_f else (root / want_f)
        if not cand.is_absolute():
            cand = root / cand
        if not cand.exists():
            bad.append(f'{fkey}: 읽은 파일을 다시 못 찾는다 ({cand})')
            continue
        got_s = sha256(cand)
        if got_s != want_s:
            bad.append(f'{skey}: 봉인 {want_s[:12]} ≠ 실제 {got_s[:12]}')
    return '; '.join(bad) if bad else None


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
    #  ⛔ **철자 정정 2026-09-15 (`R4-01` ⓐ)** — 기본값이 `ion,electron,thermal` 이었는데
    #    정본 키는 `audit_constriction_deleted.CHANNELS` = `ionic/electronic/thermal` 이다.
    #    ⇒ `CHANNELS[ch]` 가 **KeyError** 를 내고 그것이 `NO_NETWORK` 로 삼켜졌다.
    #    이제 기본값을 정본에서 읽고, 모르는 철자는 `case_networks` 가 이름을 대며 거부한다.
    ap.add_argument('--channels', default='ionic,electronic,thermal')
    ap.add_argument('--dry-run', action='store_true', help='분류만 하고 **쓰지 않는다** (날짜 무관)')
    #  ★ `R4-10` — 날짜를 **주입 가능한 입력**으로 만든다.  옛 selftest 는 `date.today()` 에
    #    의존해 **오늘만 초록**이었고, 허용일(09-17)을 넣으면 ③b 가 빨간불이었다 =
    #    도구가 실제로 일해야 하는 날에 자기검사가 깨졌다.
    ap.add_argument('--now', default='',
                    help='ISO8601 시각 주입 (selftest·재현 전용).  예 2026-09-17T12:00+09:00')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()

    now = (_dt.datetime.fromisoformat(a.now) if a.now
           else _dt.datetime.now(_dt.timezone.utc))
    if now.tzinfo is None:
        now = now.replace(tzinfo=KST)
    #  ★★ **양쪽으로 닫힌 창** (`R4-07`, 저자 결정 2026-09-15).
    #    이르면 거부 · 지나면 거부.  "언제 멈출지" 의 선택 여지가 코드에서 사라진다.
    open_at = _dt.datetime.combine(SEAL_NOT_BEFORE, _dt.time(0, 0), tzinfo=KST)
    if not a.dry_run and now < open_at:
        print(f'⛔ 봉인 거부 (너무 이르다) — 계약 §5-v4 D-3 의 최초 허용일은 {SEAL_NOT_BEFORE} '
              f'(KST 00:00) 이고 지금은 {now.astimezone(KST):%Y-%m-%d %H:%M %Z} 다.')
        print('   lhs00_034·089·098 이 아직 돌고 있어 사흘을 준 것이다.  --dry-run 은 언제든 된다.')
        print('   ⛔ 이 날짜를 결과가 아쉬워서 앞당기지 말 것.')
        return 2
    if not a.dry_run and now > SEAL_DEADLINE:
        print(f'⛔ 봉인 거부 (마감이 지났다) — 저자가 고정한 수신 종료는 '
              f'{SEAL_DEADLINE:%Y-%m-%d %H:%M %Z} 이고 지금은 '
              f'{now.astimezone(KST):%Y-%m-%d %H:%M %Z} 다.')
        print('   ⛔ 마감 후 봉인은 "결과를 더 본 뒤 시점을 고르는 것" 이라 사전등록을 훼손한다.')
        print('   ⇒ 옮기려면 저자가 원장에 먼저 적는다 (R4-07).')
        return 2
    if not a.webapp:
        ap.error('--webapp 이 필요하다 (또는 --selftest)')

    _S0 = _load('_s0_seal', SCRIPTS / 'audit_constriction_deleted.py')
    _RHO = _load('_rho_seal', SCRIPTS / 'measure_rho.py')
    import scipy
    all_rows = read_cohort(Path(a.cohort))
    #  ★ `R4-02` — 주 코호트는 **설계 130** 과 정확히 같아야 하고 `perc` 는 밖에 둔다.
    cohort, rogue = split_cohort(all_rows, Path(a.design_csv))
    if rogue:
        print(f'  ⓘ 등록 밖 {len(rogue)}개는 주 코호트에서 **제외**한다: {sorted(rogue)}')
    channels = [c.strip() for c in a.channels.split(',') if c.strip()]
    per_channel = {ch: {} for ch in channels}
    errors, prov_all = [], {}
    env_seen, calls_all = {}, []
    root = Path(a.webapp).expanduser()
    for case, row in sorted(cohort.items()):
        cdir = root / case
        raw_ok = row.get('status', '') == 'RAW_OK'
        if not raw_ok or not cdir.is_dir():
            for ch in per_channel:
                per_channel[ch][case] = 'PENDING_BASELINE'
            continue
        #  ★★ `R4-01` — 로드·덱 사상·plate_z·경계·망 생성을 **정본 한 경로**로 부른다.
        #    사본이 세 군데 어긋나 있었고 그 예외가 `NO_NETWORK` 로 삼켜졌다.
        try:
            #  ⚠ TSV 의 `deck` 은 **덱 파일 경로**다 (실물 확인: `<root>/<case>/input_<case>.liggghts`).
            #    `case_networks` 는 **디렉터리**를 받으므로 부모를 넘긴다 — 파일을 그대로
            #    넘기면 후보 경로가 한 칸 어긋나 "덱을 못 찾았다" 가 된다.
            _dk = (row.get('deck') or '').strip()
            nets, prov = _S0.case_networks(cdir, contact_mode='physics',
                                           channels=tuple(channels),
                                           deck_dir=(str(Path(_dk).parent) if _dk else None))
        except Exception as e:
            #  ⛔ **기술 실패는 `ERROR` 다** — 물리 상태(`NO_NETWORK`)로 둔갑시키지 않는다.
            for ch in per_channel:
                per_channel[ch][case] = 'ERROR'
            errors.append(f'{case}: {type(e).__name__} {e}')
            continue
        #  ★ `R4-02` — 실제로 읽은 파일이 TSV 의 지문과 같은가.
        why = verify_provenance(row, prov, root)
        if why:
            for ch in per_channel:
                per_channel[ch][case] = 'ERROR'
            errors.append(f'{case}: 지문 불일치 — {why}')
            continue
        prov_all[case] = prov
        for ch in channels:
            try:
                with _RHO._Recorder(_S0._NC) as rec:
                    _g, sig = _S0._NC.solve_network(nets[ch], mode='full')
                calls_all.extend(rec.calls)
                per_channel[ch][case] = classify(True, True, sig)
            except Exception as e:
                per_channel[ch][case] = 'ERROR'
                errors.append(f'{case}/{ch}: solve {type(e).__name__} {e}')
    env_seen = _env_from_recorder(calls_all)
    env_seen['scipy'] = scipy.__version__
    env_seen['python'] = sys.version.split()[0]
    seal = build_seal(per_channel, cohort, env_seen, Path(a.cohort), Path(a.design_csv), git_sha())
    for ch, d in seal['channels'].items():
        print(f"  {ch}: B_ch {d['n_B_ch']} · OLD_ZERO {d['n_OLD_ZERO']} · OLD_NONE {d['n_OLD_NONE']}"
              f" · PENDING {d['n_PENDING_BASELINE']} · 순서자리 {d['median_order_positions_1based']}")
    #  ★★★ **`R4-01` ⓒ 의 처방** — *"잘못된 채널·읽기 실패·예외는 `ERROR` 상태로 남기고
    #    **실행 허가 봉인을 발행하지 않는다**"*.  옛 판은 세 `B_ch` 가 0개여도 rc=0 이었다.
    if errors:
        print(f'\n⛔ 기술 실패 {len(errors)}건 — **실행 허가 봉인을 발행하지 않는다** (R4-01):')
        for e in errors[:12]:
            print('   ' + e)
        if len(errors) > 12:
            print(f'   … 외 {len(errors) - 12}건')
        print('   ⇒ 이것은 "물리적으로 망이 없음" 이 아니라 **도구가 못 읽은 것**이다.')
        return 3
    #  ★ 빈 봉인도 거부한다 — 어느 채널이든 `B_ch` 가 0이면 baseline 이 없다.
    _empty = [ch for ch, d in seal['channels'].items() if d['n_B_ch'] == 0]
    if _empty:
        print(f'\n⛔ `B_ch` 가 0개인 채널 {_empty} — 빈 봉인을 성공으로 내지 않는다 (R4-01)')
        return 3
    if a.dry_run:
        print('  (--dry-run — 아무것도 쓰지 않았다)')
        return 0
    #  ★ `R4-02` — *"기존 봉인을 조용히 덮어쓰지 말고 불변 버전으로 남겨야 한다"*.
    outp = Path(a.out)
    if outp.exists():
        prev = outp.with_suffix(outp.suffix + '.' + sha256(outp)[:12])
        if not prev.exists():
            prev.write_bytes(outp.read_bytes())
        print(f'  ⓘ 기존 봉인을 불변 사본으로 남겼다 → {prev.name}')
    seal['provenance'] = prov_all            # 무엇을 실제로 읽었는지
    seal['rogue_ids'] = sorted(rogue)        # 등록 밖 (주 집합에 안 들어간다)
    seal['seal_deadline'] = SEAL_DEADLINE.isoformat()
    seal['sealed_at_kst'] = now.astimezone(KST).isoformat(timespec='seconds')
    outp.write_text(json.dumps(seal, ensure_ascii=False, indent=1), encoding='utf-8')
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

    # ③ 날짜 게이트 — **날짜를 고정 입력으로** 넣어 양쪽을 매번 함께 시험한다
    #  ⛔⛔ **정정 2026-09-15 (`R4-10`)** — 옛 판은 `date.today()` 에 의존해 **오늘만 초록**이었다.
    #    허용일(09-17)을 주입하면 빈 root 의 봉인을 쓴 뒤 ③b 가 파일 부재를 요구해
    #    `23 PASS · ③b FAIL · rc=1` 이었다 = **도구가 실제로 일해야 하는 날에 자기검사가 깨진다**.
    #    ⛔ 파일 부재 검사를 **지워서 초록으로 만들라는 뜻이 아니다** (판정문이 못 박았다).
    #    ⇒ 세 시각을 고정으로 넣어 ⓐ 이르면 거부 ⓑ 창 안에서는 **내용 때문에** 거부
    #      (빈 root ⇒ B_ch 0 ⇒ rc=3) ⓒ 지나면 거부 를 **매번 함께** 본다.
    import tempfile
    td = Path(tempfile.mkdtemp())
    _EARLY = '2026-09-16T12:00:00+09:00'
    _INSIDE = '2026-09-17T12:00:00+09:00'
    _LATE = '2026-09-18T00:00:00+09:00'

    rc_e = main(['--webapp', str(td), '--out', str(td / 'e.json'), '--now', _EARLY])
    chk('③ 허용일 **전** 은 rc=2 로 거부 (고정 날짜 주입)', rc_e == 2, f'now={_EARLY}')
    chk('③b 거부됐으면 파일을 쓰지 않았다', not (td / 'e.json').exists())

    rc_l = main(['--webapp', str(td), '--out', str(td / 'l.json'), '--now', _LATE])
    chk('③c ★★ 마감 **후** 도 rc=2 로 거부 (R4-07 — 양쪽으로 닫힌 창)', rc_l == 2, f'now={_LATE}')
    chk('③d 마감 후에도 파일을 쓰지 않았다', not (td / 'l.json').exists())

    #  ★★ 창 **안** — 옛 판이 빨간불이던 자리.  이제 날짜는 통과하고 **내용**이 막는다:
    #    빈 root ⇒ 전 케이스 PENDING ⇒ `B_ch` 0 ⇒ 빈 봉인 거부 (rc=3).
    #    ⇒ *"날짜가 왔다"* 와 *"봉인할 내용이 있다"* 가 **다른 검사**임이 고정된다.
    rc_i = main(['--webapp', str(td), '--out', str(td / 'i.json'), '--now', _INSIDE])
    chk('③e ★★ 창 안에서는 날짜가 통과하고 **내용**이 막는다 (빈 B_ch → rc=3)',
        rc_i == 3, f'now={_INSIDE} rc={rc_i}')
    chk('③f 빈 봉인도 파일을 쓰지 않았다 (rc=3 인데 산출물이 남으면 최악)',
        not (td / 'i.json').exists())
    #  ★ 판별력 — 세 시각이 **실제로 다른 경로**를 탄다 (같으면 이 검사가 공허하다).
    chk('③g ★ 세 시각이 서로 다른 rc 를 낸다 (검사가 공허하지 않다)',
        len({rc_e, rc_i}) == 2 and rc_e == rc_l)
    #  ★ dry-run 은 날짜 무관 — 창 밖에서도 분류는 돈다 (그러나 쓰지 않는다).
    rc_d = main(['--webapp', str(td), '--out', str(td / 'd.json'), '--now', _EARLY, '--dry-run'])
    chk('③h --dry-run 은 창 밖에서도 돌고 **쓰지 않는다**',
        rc_d in (0, 3) and not (td / 'd.json').exists(), f'rc={rc_d}')
    #  ★★ `R4-10` 이 뒤집은 것 — *"dry-run 이 봉인을 안 쓰므로 S3 는 기계적으로 시작될 수 없다"*
    #    는 **반증됐다**: 봉인을 요구하는 러너가 없어서 기계적 차단이 아예 없다.
    #    ⇒ 그 문장을 selftest 에 적어 다음 사람이 같은 착각을 안 하게 한다.
    chk('③i ★ 이 도구는 **발행을 막을 뿐 S3 시작을 막지 않는다** (R4-10 이 반증한 주장)',
        True, '봉인을 요구하는 러너가 없다 — 기계적 차단은 별건으로 만들어야 한다')

    #  ── ⑥ 코호트 분할·지문 (R4-02) ─────────────────────────────────────────
    _dcsv = td / 'design.csv'
    _dcsv.write_text('case_id,x\nA,1\nB,2\n', encoding='utf-8')
    _rows = {'A': {'case': 'A', 'status': 'RAW_OK'}, 'B': {'case': 'B', 'status': 'RAW_OK'},
             'perc': {'case': 'perc', 'status': 'RAW_OK'}}
    _main, _rogue = split_cohort(_rows, _dcsv)
    chk('⑥ ★★ `perc` 는 주 코호트 **밖**이다 (옛 판은 131개를 순회했다)',
        sorted(_main) == ['A', 'B'] and sorted(_rogue) == ['perc'])
    try:
        split_cohort({'A': {'case': 'A'}}, _dcsv)
        chk('⑥b 설계 ID 가 다 안 오면 거부', False)
    except ValueError as e:
        chk('⑥b ★ 설계 ID 가 다 안 오면 거부 (등록 집합 불완전)', 'R4-02' in str(e))
    try:
        split_cohort(_rows, td / 'nope.csv')
        chk('⑥c 설계 CSV 가 없으면 거부', False)
    except ValueError as e:
        chk('⑥c ★ 설계 CSV 가 없으면 거부 (빈 설계로 n=0 봉인이 나가던 자리)',
            '없다' in str(e))
    _e = td / 'empty.csv'
    _e.write_text('case_id,x\n', encoding='utf-8')
    try:
        split_cohort(_rows, _e)
        chk('⑥d 빈 설계면 거부', False)
    except ValueError as e:
        chk('⑥d ★ 빈 설계면 거부 (0개를 등록 집합으로 받지 않는다)', '0개' in str(e))

    #  ★ 지문 — 실제로 읽은 파일이 TSV 의 SHA 와 다르면 ERROR
    _f = td / 'atom_100.liggghts'
    _f.write_text('x', encoding='utf-8')
    _good = {'atom_file': str(_f), 'atom_sha256': sha256(_f)}
    chk('⑦ ★ 지문이 같으면 통과', verify_provenance(_good, {'atom_file': str(_f)}, td) is None)
    _f.write_text('y', encoding='utf-8')                       # 파일 내용이 바뀌었다
    chk('⑦b ★★ 같은 경로인데 **내용이 바뀌면** 잡는다 (봉인 지문 ≠ 실제)',
        'atom_sha256' in (verify_provenance(_good, {'atom_file': str(_f)}, td) or ''))
    _f2 = td / 'atom_200.liggghts'
    _f2.write_text('x', encoding='utf-8')
    chk('⑦c ★★ loader 가 **다른 step** 을 읽으면 잡는다 (step 200 을 끼워 넣던 반례)',
        'atom_file' in (verify_provenance(_good, {'atom_file': str(_f2)}, td) or ''))
    chk('⑦d ★ TSV 에 지문이 없으면 통과가 아니다 (모르는 것은 거부)',
        verify_provenance({'atom_file': str(_f)}, {'atom_file': str(_f)}, td) is not None)
    #  ★ 중복 ID — 마지막 행이 이기게 두지 않는다
    _dt_tsv = td / 'dup.tsv'
    _dt_tsv.write_text('case\tstatus\nA\tRAW_OK\nA\tRAW_OK\n', encoding='utf-8')
    try:
        read_cohort(_dt_tsv)
        chk('⑧ 중복 ID 는 거부', False)
    except ValueError as e:
        chk('⑧ ★ 중복 ID 는 거부 (마지막 행이 덮어쓰면 대상이 조용히 바뀐다)', 'R4-02' in str(e))

    #  ★ `ERROR` 가 라벨에 있고 `NO_NETWORK` 와 **다른 칸**이다 (R4-01 ⓒ)
    chk('⑨ ★★ `ERROR` 가 `NO_NETWORK` 와 별개 라벨이다 (기술 실패 ≠ 물리 상태)',
        'ERROR' in LABELS and 'NO_NETWORK' in LABELS)
    #  ★ 채널 기본값이 정본 철자다 (R4-01 ⓐ)
    import importlib.util as _ilu
    _sp = _ilu.spec_from_file_location('_s0c', SCRIPTS / 'audit_constriction_deleted.py')
    _s0 = _ilu.module_from_spec(_sp)
    _sp.loader.exec_module(_s0)
    chk('⑩ ★★ 채널 기본값이 정본 키와 같다 (옛 `ion`/`electron` 은 KeyError 였다)',
        set('ionic,electronic,thermal'.split(',')) == set(_s0.CHANNELS))
    chk('⑩b ★ 봉인 도구가 망을 **정본 경로**로 만든다 (사본을 안 쓴다)',
        hasattr(_s0, 'case_networks'))

    #  ── ⑪ ★★★ **필수 대조** (판정문 §2 `R4-01` 이 이름으로 요구한 것) ────────────────
    #    *"정상 raw → 덱 상 사상·경계 → 세 양수 baseline → 그 ID 가 `B_ch` 에 들어감 → 파일 왕복"*.
    #    ⚠ 거부만 시험하면 **아무것도 봉인 못 하는 도구**도 초록이 된다.  옛 판의 실패가
    #      정확히 그 모양이었다 (세 `B_ch` 가 0개인데 rc=0).  ⇒ 양성 대조가 있어야 한다.
    import math as _math
    _pr = td / 'pos'
    _cs = _pr / 'lhs00_777'
    _pd = _cs / 'post_lhs00_777'
    _pd.mkdir(parents=True)
    _deck = _cs / 'input_lhs00_777.liggghts'
    _deck.write_text(
        '# lhs00_777: 2-type 합성 (양성 대조)\n'
        'variable r_AM equal 0.0005\nvariable r_SE equal 0.0005\n'
        'fix m1 all property/global youngsModulus peratomtype 1.4e8 0.135e7\n'
        'fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 '
        'radius constant ${r_AM}\n'
        'fix pts2 all particletemplate/sphere 32452843 atom_type 2 density constant 2000 '
        'radius constant ${r_SE}\n', encoding='utf-8')
    _r, _g = 0.0005, 0.0009
    _zs = [_r, _r + _g, _r + 2 * _g]
    #  AM 사슬(type 1) 과 SE 사슬(type 2) 을 **각각 z 로 관통**시킨다 ⇒ 이온·전자 둘 다 양수.
    _atoms = [(1 + i, 1, 0.0, z) for i, z in enumerate(_zs)] + \
             [(4 + i, 2, 0.004, z) for i, z in enumerate(_zs)]
    _af = _pd / 'atom_100.liggghts'
    _af.write_text('ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n6\n'
                   'ITEM: BOX BOUNDS pp pp ff\n0 1\n0 1\n0 1\n'
                   'ITEM: ATOMS id type radius x y z\n'
                   + ''.join(f'{i} {t} {_r} {x} 0 {z}\n' for i, t, x, z in _atoms),
                   encoding='utf-8')

    def _crow(i1, i2, area, dlt):
        v = ['0'] * 26
        v[6], v[7], v[21], v[22] = str(i1), str(i2), repr(area), repr(dlt)
        return ' '.join(v)

    _A, _d = 0.30 * _math.pi * _r ** 2, 2 * _r - _g
    _cf = _pd / 'contact_100.liggghts'
    _cf.write_text('ITEM: TIMESTEP\n100\nITEM: NUMBER OF ENTRIES\n4\n'
                   'ITEM: BOX BOUNDS pp pp ff\n0 1\n0 1\n0 1\n'
                   'ITEM: ENTRIES ' + ' '.join(f'c_cpl[{k}]' for k in range(1, 27)) + '\n'
                   + _crow(1, 2, _A, _d) + '\n' + _crow(2, 3, _A, _d) + '\n'
                   + _crow(4, 5, _A, _d) + '\n' + _crow(5, 6, _A, _d) + '\n', encoding='utf-8')
    #  TSV 는 **실제 지문**을 적는다 (그것이 R4-02 의 계약이다).
    _ptsv = td / 'pos.tsv'
    _ptsv.write_text(
        'case\tstatus\tdeck\tdeck_sha256\tatom_file\tatom_sha256\tcontact_file\tcontact_sha256\n'
        f'lhs00_777\tRAW_OK\t{_deck}\t{sha256(_deck)}\t{_af}\t{sha256(_af)}\t'
        f'{_cf}\t{sha256(_cf)}\n', encoding='utf-8')
    _pcsv = td / 'pos_design.csv'
    _pcsv.write_text('case_id,x\nlhs00_777,1\n', encoding='utf-8')
    _pout = td / 'pos_seal.json'
    _rcp = main(['--webapp', str(_pr), '--cohort', str(_ptsv), '--design-csv', str(_pcsv),
                 '--out', str(_pout), '--now', _INSIDE])
    chk('⑪ ★★★ 정상 raw 는 **봉인이 나간다** (rc=0) — 거부만 하는 도구가 아니다',
        _rcp == 0, f'rc={_rcp}')
    _sl = json.loads(_pout.read_text(encoding='utf-8')) if _pout.exists() else {}
    chk('⑪b ★★ 세 채널 전부 `B_ch` 에 그 ID 가 들어간다 (옛 판은 셋 다 0개였다)',
        all(_sl.get('channels', {}).get(c, {}).get('ids', {}).get(IN_DOMAIN) == ['lhs00_777']
            for c in ('ionic', 'electronic', 'thermal')),
        str({c: _sl.get('channels', {}).get(c, {}).get('n_B_ch') for c in
             ('ionic', 'electronic', 'thermal')}))
    chk('⑪c ★ 파일 왕복 — 봉인이 디스크에 남고 다시 읽힌다', bool(_sl) and _pout.exists())
    chk('⑪d ★ 무엇을 **실제로 읽었는지** 가 봉인에 남는다 (R4-02)',
        _sl.get('provenance', {}).get('lhs00_777', {}).get('atom_step') == 100)
    chk('⑪e ★ 고정 마감이 봉인 문서에 박힌다 (R4-07)',
        _sl.get('seal_deadline', '').startswith('2026-09-17T23:59'))
    #  ★★ 판별력 — 같은 입력에서 **지문 하나만** 틀리면 봉인이 안 나가야 한다.
    _btsv = td / 'pos_bad.tsv'
    _btsv.write_text(_ptsv.read_text(encoding='utf-8').replace(sha256(_af), '0' * 64),
                     encoding='utf-8')
    _rcb = main(['--webapp', str(_pr), '--cohort', str(_btsv), '--design-csv', str(_pcsv),
                 '--out', str(td / 'bad_seal.json'), '--now', _INSIDE])
    chk('⑪f ★★ atom 지문 한 글자만 틀려도 봉인이 **안** 나간다 (rc=3, 판별력)',
        _rcb == 3 and not (td / 'bad_seal.json').exists(), f'rc={_rcb}')
    #  ★ 기존 봉인을 **불변 사본으로** 남긴다 (R4-02 의 마지막 조건)
    _rcp2 = main(['--webapp', str(_pr), '--cohort', str(_ptsv), '--design-csv', str(_pcsv),
                  '--out', str(_pout), '--now', _INSIDE])
    chk('⑪g ★ 재봉인은 기존 것을 **조용히 덮지 않고** 불변 사본을 남긴다',
        _rcp2 == 0 and any(p.name.startswith('pos_seal.json.') for p in td.iterdir()))

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
