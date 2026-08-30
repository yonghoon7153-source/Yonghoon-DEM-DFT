#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""커밋된 cohort 감사 패키지가 **지금도** 재도출되는지 본다.

    python3 scripts/check_cohort_packages.py            # 리포 전수
    python3 scripts/check_cohort_packages.py --selftest

★ 왜: 원장(`docs/reviews/table_s3_data_20260827.md`)이 *"제3자가 리포만으로 재도출한 값이
  이 문서와 일치한다"* 고 적는데, 그것은 **2026-08-29 에 손으로 한 번 돌린 결과**였고
  그 뒤로 **아무것도 다시 확인하지 않는다**.  누가 패키지를 건드리거나 판정기가 바뀌면
  원장의 그 문장이 조용히 거짓이 된다.  `check_all.sh` 의 "리포가 맞나" 절에 그 자리가
  비어 있었다.

★★ 설계 원칙 — **대상의 자기 신고를 읽지 않는다** (인계 §3-4).
  · 비는 팔의 `sigma_e_eff_S_cm` 에서 **다시 계산**한다.  저장된 판정 필드를 읽지 않는다.
  · 침대(SBE/DBE) 구분은 **파일 이름을 믿지 않고** `input_digest` 로 묶은 뒤,
    이름과 digest 가 어긋나면 **실패**시킨다 (이름은 검사 대상이지 근거가 아니다).
  · 그렇게 얻은 값이 **원장 산문에 그대로 적혀 있는지** 본다.  적혀 있지 않으면
    "커밋됐는데 기록되지 않았다" 로 보고한다 (조용한 유실 방지).

⚠ 이 검사는 **값이 옳은가**를 묻지 않는다.  묻는 것은 *"리포에 있는 것이 원장이
  말하는 것과 같은가"* 다.  물리의 옳고 그름은 사전등록과 판정의 몫이다.

⚠ estimator 는 **쌍대응 비의 산술평균**이다 (개정 A1 등록).  `mean(DBE)/mean(SBE)` 는
  정본이 아니다 — 둘은 6자리에서 갈린다.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import statistics
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, 'docs', 'reviews', 'table_s3_data_20260827.md')
DATA = os.path.join(REPO, 'docs', 'data')
EXPECT_ARMS = 16


def _arms(d):
    """팔 파일 → [(basename, step3 dict)].  `step3` 없는 파일은 실패 사유로 올린다."""
    out, bad = [], []
    for f in sorted(glob.glob(os.path.join(d, 'p2_*.json'))):
        try:
            j = json.load(open(f, encoding='utf-8'))
        except Exception as e:                                   # noqa: BLE001
            bad.append((os.path.basename(f), f'JSON 파싱 실패: {e}')); continue
        s = j.get('step3')
        if not isinstance(s, dict):
            bad.append((os.path.basename(f), '`step3` 가 없다')); continue
        out.append((os.path.basename(f), s))
    return out, bad


def audit(d):
    """한 패키지 → (ratio 또는 None, 문제 목록, 부가 정보).  ratio 는 **재계산**이다."""
    problems, info = [], {}
    arms, bad = _arms(d)
    problems += [f'{n}: {w}' for n, w in bad]
    if not arms:
        return None, problems + ['팔이 하나도 없다'], info

    info['n_arms'] = len(arms)
    if len(arms) != EXPECT_ARMS:
        problems.append(f'팔 {len(arms)}개 — {EXPECT_ARMS}개여야 한다')

    # ── 침대 묶기: digest 가 근거, 이름은 검사 대상 ──────────────────────────
    by_digest, name_of = {}, {}
    for n, s in arms:
        m = s.get('manifest') or {}
        dg = m.get('input_digest')
        if dg is None:
            problems.append(f'{n}: `input_digest` 가 없다 (침대를 특정할 수 없다)'); continue
        by_digest.setdefault(dg, []).append((n, s))
        nm = 'SBE' if '_SBE_' in n else ('DBE' if '_DBE_' in n else None)
        if nm is None:
            problems.append(f'{n}: 이름에서 침대를 못 읽는다')
        else:
            name_of.setdefault(dg, set()).add(nm)
    if len(by_digest) != 2:
        problems.append(f'침대가 {len(by_digest)}개 — 2개(SBE·DBE)여야 한다')
        return None, problems, info
    for dg, names in name_of.items():
        if len(names) != 1:
            problems.append(f'digest {dg[:8]} 에 이름이 섞여 있다: {sorted(names)} '
                            f'— 이름과 침대가 어긋난다')
    if len(problems):
        pass  # 계속 진행해 나머지도 보고한다

    sbe = next((dg for dg, s in name_of.items() if s == {'SBE'}), None)
    dbe = next((dg for dg, s in name_of.items() if s == {'DBE'}), None)
    if sbe is None or dbe is None:
        return None, problems + ['SBE/DBE 를 갈라내지 못했다'], info
    info['digest_SBE'], info['digest_DBE'] = sbe, dbe

    # ── 수렴·규약 ────────────────────────────────────────────────────────────
    pids = set()
    for n, s in arms:
        if s.get('cg_info') != 0:
            problems.append(f'{n}: cg_info={s.get("cg_info")} — 수렴하지 않았다')
        if s.get('unconverged'):
            problems.append(f'{n}: unconverged=True')
        if not ((s.get('_reduced') or {}).get('source_sha256')):
            problems.append(f'{n}: 원본 해시가 없다 (provenance 끊김)')
        pids.add(((s.get('manifest') or {}).get('physics_protocol_id')))
    if len(pids) != 1:
        problems.append(f'규약 해시가 섞여 있다: {sorted(map(str, pids))}')
    info['physics_protocol_id'] = sorted(map(str, pids))[0] if pids else None

    # ── origin factorial: {0, vox/2}³ 이 정확히 8개 ─────────────────────────
    for dg, label in ((sbe, 'SBE'), (dbe, 'DBE')):
        og = []
        for n, s in by_digest[dg]:
            o = (s.get('manifest') or {}).get('origin_shift_um')
            og.append(tuple(round(float(x), 6) for x in o) if o else None)
        if None in og:
            problems.append(f'{label}: origin 이 없는 팔이 있다'); continue
        if len(set(og)) != len(og):
            problems.append(f'{label}: **중복 origin** — 같은 위상을 여러 번 셌다')
        levels = {v for t in og for v in t}
        if len(levels) != 2 or 0.0 not in levels:
            problems.append(f'{label}: origin 수준이 {sorted(levels)} — {{0, vox/2}} 여야 한다')
        elif len(set(og)) != 8:
            problems.append(f'{label}: 완전 factorial 이 아니다 ({len(set(og))}/8 위상)')

    # ── ★ 비 재계산: 쌍대응(origin 키 join) 비의 산술평균 ────────────────────
    def keyed(dg):
        out = {}
        for n, s in by_digest[dg]:
            o = (s.get('manifest') or {}).get('origin_shift_um')
            sig = s.get('sigma_e_eff_S_cm')
            if o is None or sig is None:
                problems.append(f'{n}: origin 또는 σ_e 가 없다'); continue
            out[tuple(round(float(x), 6) for x in o)] = float(sig)
        return out

    S, D = keyed(sbe), keyed(dbe)
    shared = sorted(set(S) & set(D))
    if not shared:
        return None, problems + ['두 침대에 공통 origin 이 없다 — 쌍대응 불가'], info
    if len(shared) != len(S) or len(shared) != len(D):
        problems.append(f'origin 이 짝이 안 맞는다 (공통 {len(shared)} · SBE {len(S)} · DBE {len(D)})')

    ratios = [D[o] / S[o] for o in shared]
    ratio = sum(ratios) / len(ratios)
    info['n_paired'] = len(shared)
    info['ratio'] = round(ratio, 6)
    info['ratio_range'] = (round(min(ratios), 6), round(max(ratios), 6))
    #  ⚠ 나눗수는 **규약**이지 추론이 아니다.  8 위상은 완전 factorial 이라 모집단이고,
    #    그 뜻으로는 n 이 더 옳다.  그러나 원장·판정기가 n−1 로 적으므로 **거기에 맞춘다**
    #    — 여기서만 다르게 쓰면 같은 양이 문서마다 다른 수로 나타난다 (초판이 그랬다).
    #    ⇒ 아래 원장 대조가 이 값도 함께 본다.
    info['origin_phase_sd'] = round(statistics.stdev(ratios), 6) if len(ratios) > 1 else 0.0
    info['sigma_e_SBE_mScm'] = round(1000.0 * sum(S.values()) / len(S), 2)
    info['sigma_e_DBE_mScm'] = round(1000.0 * sum(D.values()) / len(D), 2)
    return ratio, problems, info


def find_packages(root):
    out = []
    for d in sorted(glob.glob(os.path.join(root, '*'))):
        if os.path.isdir(d) and glob.glob(os.path.join(d, 'p2_*.json')):
            out.append(d)
    return out


def run(root=DATA, ledger=LEDGER, quiet=False):
    pkgs = find_packages(root)
    fails = []
    if not quiet:
        print(f'cohort 감사 패키지 {len(pkgs)}개 — {os.path.relpath(root, REPO)}')
    led = open(ledger, encoding='utf-8').read() if os.path.exists(ledger) else ''
    if not led:
        fails.append(f'원장을 못 읽는다: {ledger}')
    for d in pkgs:
        name = os.path.basename(d)
        ratio, problems, info = audit(d)
        for w in problems:
            fails.append(f'{name}: {w}')
        if ratio is None:
            if not quiet:
                print(f'  ✗ {name}  — 비를 못 낸다')
            continue
        r6 = f'{ratio:.6f}'
        #  ★ 원장 산문 대조 — 커밋됐는데 기록되지 않았으면 그것도 결함이다
        recorded = r6 in led
        if not recorded:
            fails.append(f'{name}: 재계산한 비 {r6} 가 원장에 없다 '
                         f'(커밋됐는데 기록되지 않았거나 값이 갈렸다)')
        #  산포도 같이 본다 — 비만 맞고 산포가 갈리면 같은 표를 두 수로 적게 된다
        s6 = f'{info.get("origin_phase_sd", 0.0):.6f}'
        if s6 not in led:
            fails.append(f'{name}: 재계산한 origin-위상 산포 {s6} 가 원장에 없다')
        if not quiet:
            mark = '✓' if recorded and not problems else ('!' if recorded else '✗')
            print(f'  {mark} {name}')
            print(f'      비 {r6}  (원장 {"일치" if recorded else "**불일치/미기록**"})  '
                  f'· 위상 {info.get("n_paired")}  · 산포 {info.get("origin_phase_sd")} '
                  f'(n−1, 원장 규약)')
            print(f'      σ_e  SBE {info.get("sigma_e_SBE_mScm")} · '
                  f'DBE {info.get("sigma_e_DBE_mScm")} mS/cm  · '
                  f'규약 {info.get("physics_protocol_id")}')
    if not quiet:
        print()
        if fails:
            print(f'✗ {len(fails)} 건')
            for f in fails:
                print(f'  · {f}')
        else:
            print('✓ 커밋된 패키지가 전부 원장과 일치한다 '
                  '(⚠ "값이 옳다" 가 아니라 "리포와 원장이 같다" 이다)')
    return 1 if fails else 0


# ── selftest ────────────────────────────────────────────────────────────────
def _fixture(td, name, ratio_scale=1.0, drop=0, dup_origin=False, swap_name=False,
             break_cg=False):
    """16팔 최소 패키지를 만든다.  SBE σ=0.05 고정, DBE = 0.05*1.2*scale."""
    d = os.path.join(td, name)
    os.makedirs(d, exist_ok=True)
    half = 0.075
    origins = [(a, b, c) for a in (0.0, half) for b in (0.0, half) for c in (0.0, half)]
    for bed, dg, base in (('SBE', 'aaaa1111', 0.05), ('DBE', 'bbbb2222', 0.05 * 1.2)):
        for i, o in enumerate(origins):
            if drop and bed == 'DBE' and i >= 8 - drop:
                continue
            oo = list(origins[0]) if (dup_origin and bed == 'DBE' and i == 1) else list(o)
            nm = bed
            if swap_name and bed == 'DBE' and i == 0:
                nm = 'SBE'
            sig = base * (ratio_scale if bed == 'DBE' else 1.0)
            json.dump({'step3': {
                'sigma_e_eff_S_cm': sig,
                'cg_info': 99 if (break_cg and bed == 'SBE' and i == 0) else 0,
                'unconverged': False,
                '_reduced': {'source_sha256': 'f' * 64},
                'manifest': {'input_digest': dg, 'origin_shift_um': oo,
                             'physics_protocol_id': 'p2-test'},
            }}, open(os.path.join(d, f'p2_{nm}_sph_a{i}.json'), 'w'))
    open(os.path.join(d, 'cohort_manifest.json'), 'w').write('{}')
    return d


def selftest():
    import tempfile
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)

    with tempfile.TemporaryDirectory() as td:
        root = os.path.join(td, 'data'); os.makedirs(root)
        _fixture(root, 'good')
        led = os.path.join(td, 'led.md')
        #  전 팔이 같은 값이라 산포는 정확히 0
        open(led, 'w').write('비는 1.200000 이고 산포는 0.000000 이다.\n')

        chk('① 정상 패키지는 통과', run(root, led, quiet=True) == 0)

        r, p, info = audit(os.path.join(root, 'good'))
        chk('② 비를 원자료에서 재계산한다', abs(r - 1.2) < 1e-12)
        chk('③ 위상 8쌍을 잡는다', info['n_paired'] == 8)
        chk('④ 침대를 digest 로 가른다', info['digest_SBE'] != info['digest_DBE'])

        #  ★ 음성 대조 — 검사가 정말 무는가
        open(led, 'w').write('비는 1.111111 이고 산포는 0.000000 이다.\n')
        chk('⑤ ★ 원장과 값이 갈리면 실패', run(root, led, quiet=True) == 1)
        open(led, 'w').write('비는 1.200000 이고 산포는 0.000000 이다.\n')

        _fixture(root, 'drop', drop=2)
        chk('⑥ ★ 팔이 모자라면 실패', run(root, led, quiet=True) == 1)
        import shutil; shutil.rmtree(os.path.join(root, 'drop'))

        _fixture(root, 'dup', dup_origin=True)
        _, p2, _ = audit(os.path.join(root, 'dup'))
        chk('⑦ ★ 중복 origin 을 잡는다 (같은 위상을 여러 번 셈)',
            any('중복 origin' in x for x in p2))
        shutil.rmtree(os.path.join(root, 'dup'))

        _fixture(root, 'swap', swap_name=True)
        _, p3, _ = audit(os.path.join(root, 'swap'))
        chk('⑧ ★ 이름과 digest 가 어긋나면 잡는다 (이름을 믿지 않는다)',
            any('어긋난다' in x for x in p3))
        shutil.rmtree(os.path.join(root, 'swap'))

        _fixture(root, 'cg', break_cg=True)
        _, p4, _ = audit(os.path.join(root, 'cg'))
        chk('⑨ ★ 미수렴 팔을 잡는다', any('수렴하지 않았다' in x for x in p4))
        shutil.rmtree(os.path.join(root, 'cg'))

        #  estimator 가 정본인지 — mean/mean 과 갈리는 값을 만든다.
        #  ⚠ 분모(SBE)가 **상수면 두 estimator 가 수학적으로 같아** 구분이 안 된다
        #    (초판 픽스처가 그랬고 이 시험이 헛돌았다).  SBE 를 위상마다 다르게 준다.
        d5 = _fixture(root, 'est')
        Sv = [0.05 * (1.0 + 0.10 * i) for i in range(8)]
        Dv = [0.06 * (1.0 + 0.03 * (7 - i)) for i in range(8)]
        for i in range(8):
            for bed, vals in (('SBE', Sv), ('DBE', Dv)):
                f = os.path.join(d5, f'p2_{bed}_sph_a{i}.json')
                j = json.load(open(f)); j['step3']['sigma_e_eff_S_cm'] = vals[i]
                json.dump(j, open(f, 'w'))
        r5, _, _ = audit(d5)
        paired = sum(Dv[i] / Sv[i] for i in range(8)) / 8
        unpaired = (sum(Dv) / 8) / (sum(Sv) / 8)
        chk('⑩ ★ 두 estimator 가 실제로 갈리는 픽스처인가 (시험이 헛돌지 않는가)',
            abs(paired - unpaired) > 1e-6)
        chk('⑪ ★ 쌍대응 산술평균이 정본이다 (mean/mean 아님)',
            abs(r5 - paired) < 1e-12 and abs(r5 - unpaired) > 1e-6)
        shutil.rmtree(d5)

    print(f'selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', default=DATA, help='패키지를 찾을 디렉터리')
    ap.add_argument('--ledger', default=LEDGER, help='대조할 원장')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    return selftest() if a.selftest else run(a.root, a.ledger)


if __name__ == '__main__':
    sys.exit(main())
