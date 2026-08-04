#!/usr/bin/env python3
"""AM_P/AM_S 라벨 불변식 — 옵션 조합과 무관하게 성립해야 하는 것을 검사.

배경 (2026-08-04 실측 사고)
────────────────────────────
0:10 케이스(4587개 전부 r=2µm = 소립 AM_S)가 scaffold 에 **전부 type1(AM_P)** 로 찍혔다.
원인 사슬: webapp 의 s4grid=1 이 poly/SC 분리 플래그를 STEP4-전용 게이트 안에 가둬 드롭
→ 생성기 _es_split_req=False → 레거시 'sdcp_mono_amp' 관례(단분산 → 크기 무관 전부 AM_P).
결과: (a) 코퍼스 coverage_AM_P 열에 6µm/2µm 혼재, (b) mpm3d_compaction 사이클 변형이
2µm SC 입자에 poly 팽창(부호 반대) 적용.

이건 **함수 안 버그가 아니라 기능 사이 배선** 문제라 디프-단위 코드리뷰가 놓친다.
그래서 리뷰 대신 불변식으로 고정한다:

  ★ 불변식: scaffold 의 type 은 **어떤 플래그 조합에서도** 입자 반지름과 일치해야 한다.
            r ≥ 문턱 → type1(AM_P),  r < 문턱 → type2(AM_S).  '관례' 는 없다.

  python3 scripts/test_am_label_invariant.py     # 종료코드 0=PASS
"""
import csv
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UM_PER_LU = 1000.0


def _mk_case(tmp, radii_lu):
    """최소 케이스 폴더 — atoms.csv 만 있으면 생성기가 scaffold 를 뽑는다."""
    case = os.path.join(tmp, 'case_x')
    os.makedirs(case, exist_ok=True)
    rng_seed = 0
    with open(os.path.join(case, 'atoms.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id', 'type', 'x', 'y', 'z', 'radius'])
        i = 1
        for r in radii_lu:                       # AM (type 1/2 는 생성기가 다시 정한다 — 그게 검사 대상)
            rng_seed += 1
            w.writerow([i, 1, 0.001 * (rng_seed % 40), 0.001 * (rng_seed // 40 % 40),
                        0.005 + 0.0001 * rng_seed, r])
            i += 1
        for k in range(60):                      # SE 약간 (생성기 최소 요건)
            w.writerow([i, 3, 0.001 * (k % 40), 0.001 * (k // 40), 0.002, 0.0005])
            i += 1
    return case


def _run_gen(case, extra):
    out = tempfile.mkdtemp(prefix='kit_')
    cmd = [sys.executable, os.path.join(ROOT, 'scripts', 'mpm_input_from_case.py'),
           '--results', case, '--out', out, '--case', 'test_x'] + extra
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return out, r


def _read_types(out):
    rows = []
    with open(os.path.join(out, 'am_scaffold.csv')) as f:
        for ln in f:
            if ln.startswith('#'):
                continue
            p = ln.split(',')
            if len(p) >= 5:
                rows.append((int(p[0]), float(p[4])))
    return rows


def main():                                                        # noqa: C901
    ok = tot = 0

    def chk(name, cond, extra=''):
        nonlocal ok, tot
        tot += 1
        ok += 1 if cond else 0
        print(f"  {'✓' if cond else '✗ FAIL'} {name}" + (f' — {extra}' if extra else ''))

    beds = {                                     # LIGGGHTS LU (1 LU = 1000 µm)
        'mono_small_0:10': [0.002] * 40,         # 2µm 전부 — 사고 재현 지점
        'mono_large_10:0': [0.006] * 12,
        'bimodal_7:3': [0.006] * 8 + [0.002] * 30,
        'mono_r4um': [0.004] * 20,               # 반경 4µm(지름 8) — 문턱 3.5µm 초과라 AM_P.
                                                 #   ⚠ '이종기술 mono 4µm 단결정' 은 **지름** 4µm
                                                 #   = 반경 2µm → AM_S (mono_small 쪽이 그 경우)
    }
    combos = {
        'default': [],
        'split_preset': ['--step4-sc-poly-preset'],
        'split_explicit': ['--step4-ds-poly', '4e-15', '--step4-ds-sc', '3e-15'],
        'grid_flags_only': [],                   # (웹앱 s4grid 경유 시 생성기에 남는 것 = 없음)
    }
    print('★ 불변식: type = (r ≥ 문턱 → 1) / (r < 문턱 → 2), 모든 베드 × 모든 플래그 조합')
    with tempfile.TemporaryDirectory() as tmp:
        for bed, radii in beds.items():
            case = _mk_case(tmp, radii)
            for combo, extra in combos.items():
                out, r = _run_gen(case, extra)
                if not os.path.isfile(os.path.join(out, 'am_scaffold.csv')):
                    err = (r.stderr or r.stdout or '').strip().splitlines()
                    # mono 베드 + i0 분리 등 정당한 거부는 불변식 위반이 아니다
                    chk(f'{bed} × {combo}: 생성 실패가 명시적 에러인가',
                        r.returncode != 0 and bool(err), (err[-1][:70] if err else '무음 실패'))
                    continue
                rows = _read_types(out)
                thr_lu = 3.5 / UM_PER_LU
                rmin, rmax = min(r_ for _, r_ in rows), max(r_ for _, r_ in rows)
                if rmax / max(rmin, 1e-12) > 1.4:          # bimodal → 기하중앙 문턱
                    thr_lu = (rmin * rmax) ** 0.5
                bad = [(t, r_) for t, r_ in rows
                       if (t == 1) != (r_ >= thr_lu)]
                chk(f'{bed} × {combo}: 라벨=크기 일치 (n={len(rows)})',
                    not bad,
                    '' if not bad else f'위반 {len(bad)}개, 예: type{bad[0][0]} r={bad[0][1]*1e3:.1f}µm')
    print(f"AM-LABEL INVARIANT {ok}/{tot} {'PASS' if ok == tot else 'FAIL'}")
    return 0 if ok == tot else 1


if __name__ == '__main__':
    sys.exit(main())
