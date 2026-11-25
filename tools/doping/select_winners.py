#!/usr/bin/env python
"""select_winners.py — extract the per-group winner from UMA screening
results so we can put MLIP post-processing (anneal, EOS, elastic, MD)
on the most-stable structure of every (compound, cation_site, anion_site)
combination.

User feedback: "각 조합에서의 1등들은 다 후처리를 해보자". This script
implements that grouping. Output is a JSON manifest with one entry per
winner that downstream tools can read.

Usage:
  python3 tools/doping/select_winners.py \\
      --results runs/.../uma_results.json \\
      --out runs/.../winners.json \\
      --group_by dopant cation_site anion_site_label
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


def _load_pre(results_path, metric, max_dv, require_converged):
    """uma_results.json → 필터 통과 레코드. (기존 필터 규약 그대로)"""
    data = json.loads(Path(results_path).read_text())
    records = data.get('results', [])
    pre = [r for r in records if 'uma_relaxed' in r and metric in r['uma_relaxed']]
    if max_dv is not None:
        pre = [r for r in pre if abs(r.get('dV_over_V0', 1e9)) <= max_dv]
    if require_converged:
        pre = [r for r in pre if r.get('converged', False)]
    return [r for r in pre if not r['uma_relaxed'].get('outlier_flag', False)]


def _group(pre, group_by):
    g = defaultdict(list)
    for r in pre:
        g[tuple(r.get(k, 'unknown') for k in group_by)].append(r)
    return g


def _champion(group, metric):
    return min(group, key=lambda r: r['uma_relaxed'][metric])


def _pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / (sxx * syy) ** 0.5


def diagnose_best_of_n(dirs_or_files, args):
    """④ A2 — best-of-N 편향을 **재지만 고르지는 않는다**.

    왜 비파괴인가: winners 를 다시 고르면 이미 그 winners 로 돌아간 anneal·bvse·
    elastic 산출물이 더 이상 그 구조를 가리키지 않는다. 파이프라인이 끊긴다.
    그래서 여기서는 (a) 그룹 크기 ↔ 챔피언 점수 상관을 재고, (b) 같은 N 으로
    잘랐을 때 **챔피언이 바뀌는 그룹 비율**만 보고한다.

    ⛔ 못 하는 것: 보정된 순위를 만들지 않는다. 그건 캐스케이드 재실행이 필요하다.
    """
    import random as _rnd
    sizes, champs = [], []
    n_grp = n_changed = n_short = 0
    n_files = 0
    worst = []
    for f in dirs_or_files:
        try:
            pre = _load_pre(f, args.metric, args.max_dv, args.require_converged)
        except Exception as e:
            print(f"  ✗ {f}: {type(e).__name__} {e}")
            continue
        if not pre:
            continue
        n_files += 1
        for key, group in _group(pre, args.group_by).items():
            n_grp += 1
            c_full = _champion(group, args.metric)
            sizes.append(len(group))
            champs.append(c_full['uma_relaxed'][args.metric])
            if len(group) < args.diagnose_best_of_n:
                n_short += 1
                continue
            rng = _rnd.Random(args.fixed_n_seed)
            sub = rng.sample(group, args.diagnose_best_of_n)
            c_sub = _champion(sub, args.metric)
            if c_sub is not c_full:
                n_changed += 1
                d = c_sub['uma_relaxed'][args.metric] - c_full['uma_relaxed'][args.metric]
                worst.append((d, len(group), '/'.join(map(str, key))))

    r = _pearson([float(s) for s in sizes], champs)
    n_eligible = n_grp - n_short
    print(f"\n▸ ④ best-of-N 진단 (N={args.diagnose_best_of_n}, 시드 {args.fixed_n_seed})")
    print(f"  파일 {n_files} · 그룹 {n_grp}")
    print(f"  그룹 크기 범위        : {min(sizes)}~{max(sizes)}  (중앙값 "
          f"{sorted(sizes)[len(sizes)//2]})")
    print(f"  ★ 크기 ↔ 챔피언 ΔE 상관 : r = {r:+.3f}" if r is not None else "  r 계산 불가")
    print(f"     (ΔE 는 낮을수록 좋다 ⇒ **r<0 이면 큰 그룹이 더 좋은 챔피언** = best-of-N 편향)")
    print(f"  균등화 가능 그룹      : {n_eligible} (표본 부족 {n_short}개는 제외하지 않고 표시만)")
    if n_eligible:
        print(f"  ★ **챔피언이 바뀌는 그룹 : {n_changed} ({100.0*n_changed/n_eligible:.1f} %)**")
    if worst:
        worst.sort(key=lambda x: -x[0])
        print(f"  잘랐을 때 가장 나빠지는 그룹 (ΔE 악화폭):")
        for d, ng, k in worst[:5]:
            print(f"    +{d:.4f} eV/atom   n={ng:<4} {k[:56]}")
    print(f"\n  ⛔ 이 진단은 순위를 **고치지 않는다.** 보정된 순위를 실제로 쓰려면 "
          f"캐스케이드를 재실행해야 한다 (winners 가 바뀌면 하류 산출물이 안 맞는다).")
    return 0


def _selftest():
    """④ 진단 로직만 검증 (음성 포함). 서버·데이터 없이 돈다."""
    import random
    n_ok = n_bad = 0

    def chk(c, m):
        nonlocal n_ok, n_bad
        print(("  ✓ " if c else "  ✗ ") + m)
        n_ok, n_bad = n_ok + bool(c), n_bad + (not c)

    chk(abs(_pearson([1, 2, 3], [1, 2, 3]) - 1.0) < 1e-12, "상관: 완전 일치 → +1")
    chk(abs(_pearson([1, 2, 3], [3, 2, 1]) + 1.0) < 1e-12, "상관: 완전 역순 → −1")
    chk(_pearson([1, 1, 1], [1, 2, 3]) is None,
        "[음성] 한쪽이 상수면 None (0 이 아니다 — 0 은 '무상관' 이라는 주장이다)")
    chk(_pearson([1, 2], [1, 2]) is None, "[음성] 표본 3 미만이면 None")

    def mk(dop, n, rng):
        return [{'dopant': dop, 'site': 'X', 'anion_site_label': 'Y', 'dV_over_V0': 0.0,
                 'uma_relaxed': {'de_per_atom_vs_baseline': rng.gauss(0.05, 0.02)}}
                for _ in range(n)]

    # ★ 양성: **같은 분포**인데 크기만 다르면 큰 그룹이 더 좋은 챔피언을 낸다
    rng = random.Random(7)
    pre = mk('BIG', 60, rng) + mk('MID', 30, rng) + mk('SMALL', 15, rng)
    g = _group(pre, ['dopant', 'site', 'anion_site_label'])
    sizes = [len(v) for v in g.values()]
    ch = [_champion(v, 'de_per_atom_vs_baseline')['uma_relaxed']['de_per_atom_vs_baseline']
          for v in g.values()]
    order = sorted(zip(sizes, ch))
    chk(order[0][1] > order[-1][1],
        "★ 같은 분포에서도 **큰 그룹의 챔피언이 더 좋다** — 성능이 아니라 표본 수다")

    # [음성] 크기가 같으면 그 신호가 안 나와야 한다
    rng2 = random.Random(11)
    pre2 = mk('A', 30, rng2) + mk('B', 30, rng2) + mk('C', 30, rng2)
    g2 = _group(pre2, ['dopant', 'site', 'anion_site_label'])
    chk(len({len(v) for v in g2.values()}) == 1 and
        _pearson([float(len(v)) for v in g2.values()],
                 [_champion(v, 'de_per_atom_vs_baseline')['uma_relaxed']
                  ['de_per_atom_vs_baseline'] for v in g2.values()]) is None,
        "[음성] 그룹 크기가 모두 같으면 상관이 None — 편향을 지어내지 않는다")

    chk(_load_pre.__doc__ is not None and _champion(mk('Z', 3, random.Random(1)),
        'de_per_atom_vs_baseline')['uma_relaxed']['de_per_atom_vs_baseline'] ==
        min(r['uma_relaxed']['de_per_atom_vs_baseline']
            for r in mk('Z', 3, random.Random(1))),
        "챔피언은 metric 최솟값이다 (ΔE 는 낮을수록 좋다)")

    print(f"selftest {'PASS' if not n_bad else 'FAIL'} — {n_ok} ok, {n_bad} bad")
    return 1 if n_bad else 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--results',
                  help='uma_results.json from run_uma_screening.py')
    p.add_argument('--results_glob',
                  help='여러 캐스케이드의 uma_results.json 을 **한 프로세스에서** '
                       '(예: "/data/work/runs/*/*/02_screen/uma_results.json")')
    p.add_argument('--exclude', action='append', default=[],
                  help='제외할 경로 부분문자열 (세대 중복 정리용)')
    p.add_argument('--diagnose_best_of_n', type=int, default=None,
                  help='④ A2 **비파괴 진단**: 그룹 크기 ↔ 챔피언 점수 상관과, '
                       '같은 N 으로 잘랐을 때 챔피언이 바뀌는 비율만 보고한다. '
                       'winners 를 다시 쓰지 않는다 — 다시 고르면 이미 그 winners 로 '
                       '돌아간 하류 산출물(anneal·bvse·elastic)이 안 맞는다.')
    p.add_argument('--out', help='Output winners.json (진단 모드면 생략)')
    p.add_argument('--selftest', action='store_true',
                  help='④ 진단 로직만 검증 (음성 경로 포함)')
    p.add_argument('--group_by', nargs='+',
                  default=['dopant', 'site', 'anion_site_label'],
                  help='Grouping keys (default: dopant + cation site + anion site)')
    p.add_argument('--metric', default='de_per_atom_vs_baseline',
                  help='Within-group metric to minimize')
    p.add_argument('--max_dv', type=float, default=0.30,
                  help='Skip records with |ΔV/V0| > this (default 30%%)')
    p.add_argument('--require_converged', action='store_true',
                  help='Drop non-converged records before selecting winners')
    p.add_argument('--fixed_n', type=int, default=None,
                  help='best-of-N 보정: 그룹마다 **같은 수 N 개**만 보고 챔피언을 고른다. '
                       '후보 수가 그룹마다 다르면(우리는 15~150) 많이 뽑힌 그룹이 '
                       '최댓값도 높아진다 — 성능이 아니라 표본 수가 만든 순위다. '
                       'N 미만인 그룹은 **탈락시키지 않고 표시**한다(그것도 정보다).')
    p.add_argument('--fixed_n_seed', type=int, default=0,
                  help='--fixed_n 의 부분표본 추출 시드. 결정론적으로 고정한다.')
    args = p.parse_args()

    if args.selftest:
        return _selftest()
    if args.diagnose_best_of_n:
        import glob as _g
        files = ([f for f in sorted(_g.glob(args.results_glob))
                  if 'bak' not in f and not any(x in f for x in args.exclude)]
                 if args.results_glob else [args.results])
        files = [f for f in files if f]
        if not files:
            print("⛔ 진단할 파일이 없다")
            return 2
        return diagnose_best_of_n(files, args)
    if not args.results or not args.out:
        print("⛔ --results 와 --out 이 필요하다 (또는 --diagnose_best_of_n)")
        return 2

    data = json.loads(Path(args.results).read_text())
    records = data.get('results', [])

    # Filter — drop errored records (no uma_relaxed) and explicit outliers
    pre = [r for r in records if 'uma_relaxed' in r and args.metric in r['uma_relaxed']]
    n_no_uma = len(records) - len(pre)
    if args.max_dv is not None:
        pre = [r for r in pre if abs(r.get('dV_over_V0', 1e9)) <= args.max_dv]
    if args.require_converged:
        pre = [r for r in pre if r.get('converged', False)]
    pre = [r for r in pre if not r['uma_relaxed'].get('outlier_flag', False)]
    print(f"Filtered: {len(records)} → {len(pre)} records "
          f"(dropped {n_no_uma} no-UMA + {len(records) - len(pre) - n_no_uma} "
          f"by filters)")

    # Group + pick winner per group
    groups = defaultdict(list)
    for r in pre:
        key = tuple(r.get(k, 'unknown') for k in args.group_by)
        groups[key].append(r)

    # ── best-of-N 보정 (2026-08-25) ────────────────────────────────────────
    #   ⛔ 실측: 종별 후보 수 15~150 (10배) · 후보 수 ↔ 챔피언 점수 r = +0.321.
    #     많이 뽑힌 종이 최댓값도 높다 = **best-of-N 인공물**이고, 후보 수는 성능이
    #     아니라 화학(치환 가능 자리 수)이 정한다. 같은 N 으로 잘라야 비교가 성립한다.
    #   ⚠ 잘라낸 것을 **버리지 않는다** — 표본이 모자란 그룹을 탈락시키면 그 자체가
    #     또 다른 선택 편향이다. 모자란다고 **표시**하고 남긴다.
    n_short = []
    if args.fixed_n:
        import random as _rnd
        rng = _rnd.Random(args.fixed_n_seed)
        cut = {}
        for key, group in groups.items():
            if len(group) < args.fixed_n:
                n_short.append((key, len(group)))
                cut[key] = group                      # 그대로 둔다
            else:
                cut[key] = rng.sample(group, args.fixed_n)
        groups = cut
        print(f"  best-of-N 보정: 그룹당 {args.fixed_n}개로 균등화 "
              f"(시드 {args.fixed_n_seed}) · 표본 부족 {len(n_short)}그룹")
        for key, n in sorted(n_short, key=lambda x: x[1])[:5]:
            print(f"    ⚠ {'/'.join(map(str, key))}: {n}개 < {args.fixed_n} "
                  f"— 균등화 못 함(그대로 둠, 이 그룹의 순위는 여전히 부풀 수 있다)")

    winners = []
    for key, group in groups.items():
        winner = min(group,
                    key=lambda r: r['uma_relaxed'][args.metric])
        winners.append({
            **winner,
            'group_key': dict(zip(args.group_by, key)),
            'n_in_group': len(group),
            'group_metric_min': winner['uma_relaxed'][args.metric],
            'group_metric_max': max(r['uma_relaxed'][args.metric] for r in group),
            'group_metric_spread': max(r['uma_relaxed'][args.metric] for r in group)
                                   - winner['uma_relaxed'][args.metric],
        })

    # Sort winners by metric (global ranking)
    winners.sort(key=lambda w: w['uma_relaxed'][args.metric])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'provenance': get_provenance(),
        'source': str(args.results),
        'group_by': args.group_by,
        'n_groups': len(groups),
        'metric': args.metric,
        'winners': winners,
    }, indent=2, default=str))

    print(f"\n{'Rank':<5}{'Group':<60}{'ΔE/atom':>10}{'Spread':>10}")
    print('-' * 90)
    for i, w in enumerate(winners[:30], 1):
        grp = '/'.join(str(v) for v in w['group_key'].values())[:58]
        print(f"{i:<5}{grp:<60}"
              f"{w['uma_relaxed'][args.metric]:>+9.4f} "
              f"{w['group_metric_spread']:>+8.4f}")
    print(f"\n✓ {len(winners)} winners → {out}")


if __name__ == '__main__':
    sys.exit(main() or 0)
