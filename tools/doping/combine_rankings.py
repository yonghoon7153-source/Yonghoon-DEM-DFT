#!/usr/bin/env python
"""combine_rankings.py — chain all pipeline outputs into one unified
multi-axis ranking. The factory line's "final assembly".

Each stage in the cascade contributes one ranking axis:

  Stage 02 (UMA screen):          ΔE/atom vs baseline, ΔV/V₀
  Stage 02 (Tier-2):              Li-Li disorder std, dopant blocking,
                                  lattice angle deviation
  Stage 04 (BVSE):                Li migration volume %, BVS std,
                                  Li mobility proxy score
  Stage 05 (anneal):              ΔE_anneal, post-anneal ΔE/atom
  Stage 07 (EOS):                 B0, V0, fit R²
  Stage 08 (elastic):             B, G, E_young, Pugh G/B, Poisson ν

Outputs unified record per structure with ALL metrics joined by name +
several composite rankings:

  rank_by_stability        — lowest post-anneal ΔE/atom
  rank_by_modulus          — highest E_young
  rank_by_mobility         — highest BVSE proxy score
  rank_combined_paper      — weighted blend (stability + modulus + mobility)

Usage:
  python3 tools/doping/combine_rankings.py \\
      --cascade_dir runs/tier_2026_05_16/ \\
      --out runs/tier_2026_05_16/FINAL_RANKING.json
"""
import argparse
import json
import pathlib
from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from _provenance import get_provenance


# NEW-6 fix: stage path fallback list. v1 cascade: 04=bvse, 05=anneal.
# v2 cascade: 04=anneal, 05=bvse. We try v2 path first, then v1.
STAGE_FILE_CANDIDATES = {
    'screening': [('02_screen/uma_results.json',       'results')],
    'winners':   [('03_winners/winners.json',          'winners')],
    'anneal':    [('04_anneal/anneal_results.json',    'results'),
                  ('05_anneal/anneal_results.json',    'results')],
    'bvse':      [('05_bvse/bvs_report.json',          'records'),
                  ('04_bvse/bvs_report.json',          'records')],
    'rerank':    [('06_rerank/post_anneal_ranking.json',
                                                  'ranked_by_post_anneal')],
    'eos':       [('07_eos/postproc_summary.json',     'records')],
    'elastic':   [('08_elastic/postproc_summary.json', 'records')],
}


#: 축별 건강 상태 — normalize() 가 채운다. --status 와 실행 말미 경고가 읽는다.
#   ⛔ 왜 있나: normalize 의 "전부 결측이면 0.5" 규칙이 **조용히** 축 하나를 상수로
#     만들었다. li_mobility_score 가 3,615행 전원 결측이었는데 아무 경고 없이
#     0.5 로 메워져 '3축 랭킹' 이 실제로는 2축이었다 (2026-08-25 발견).
#     같은 일이 다른 축에서 또 나도 안 보이는 것이 진짜 결함이다.
AXIS_HEALTH: dict = {}


def normalize(values, invert=False, label=None):
    """min-max 정규화. 결측/상수 축은 0.5 로 메우되 **그 사실을 기록한다**.

    ⛔ 이 함수가 못 하는 것: 결측을 복구하지 않는다. 0.5 는 '기여 없음' 이지
      '중간값' 이 아니다 — 그 축은 순위에 아무 영향을 못 준다.
    """
    n = len(values)
    arr = np.array([v if v is not None else np.nan for v in values],
                   dtype=float)
    n_ok = int(np.count_nonzero(~np.isnan(arr)))
    state = "ok"
    if np.all(np.isnan(arr)):
        state = "all_missing"
    elif np.nanmax(arr) - np.nanmin(arr) < 1e-12:
        state = "constant"
    if label:
        AXIS_HEALTH[label] = {"n": n, "n_present": n_ok,
                              "coverage_pct": round(100.0 * n_ok / n, 1) if n else 0.0,
                              "state": state,
                              "contributes_to_ranking": state == "ok"}
    if state != "ok":
        return [0.5] * n
    lo = np.nanmin(arr); hi = np.nanmax(arr)
    norm = (arr - lo) / (hi - lo)
    if invert:
        norm = 1 - norm
    return [float(x) if not np.isnan(x) else 0.0 for x in norm]


def load_rows(cd, verbose=False):
    """캐스케이드 하나의 스테이지 산출물을 join 해 구조별 행 리스트로. → list[dict]

    ⛔ 못 하는 것: 값의 옳고 그름을 판정하지 않는다. 없는 스테이지는 조용히 건너뛰지
      않고 verbose 에서 ✗ 로 찍는다 (조용한 no-op 이 이 파이프라인의 상습 결함이다).
    """
    recs: dict[str, dict] = {}

    # Pass 1: union all records keyed by 'name'. Try each candidate path
    # and use the first that exists (handles v1↔v2 cascade layouts).
    for stage_name, candidates in STAGE_FILE_CANDIDATES.items():
        chosen = None
        for rel_path, key in candidates:
            p = cd / rel_path
            if p.exists():
                chosen = (p, key)
                break
        if chosen is None:
            if verbose:
                print(f"  ✗ {stage_name}: no path found "
                      f"(tried {[c[0] for c in candidates]})")
            continue
        path, key = chosen
        d = json.loads(path.read_text())
        records = d.get(key, [])
        if not isinstance(records, list):
            records = []
        for r in records:
            # v4.5.8 fix: postproc (07/08) records all share name='post_relax'
            # (xyz stem). The true winner name is the parent dir of xyz_input.
            # Fall back to r['name'] for other stages whose records carry the
            # winner name directly.
            name = r.get('name', None)
            if name in (None, 'post_relax'):
                xyz = r.get('xyz_input') or r.get('xyz_file')
                if xyz:
                    name = Path(xyz).parent.name
            if not name:
                continue
            if name not in recs:
                recs[name] = {'name': name}
            recs[name][f'_{stage_name}'] = r
        if verbose:
            print(f"  ✓ {stage_name}: {len(records)} records (from {path.name})")
    if verbose:
        print(f"\nJoined: {len(recs)} unique structures")

    # Pass 2: extract per-structure metrics
    rows = []
    for name, blob in recs.items():
        row = {'name': name}
        # ΔE/atom (post-anneal preferred, fallback to screen)
        scr = blob.get('_screening', {}).get('uma_relaxed', {})
        ann = blob.get('_anneal', {})
        if 'E_post_relax' in ann and 'n_atoms' in ann:
            base_E = blob.get('_screening', {}).get('baseline_e_per_atom', None)
            if base_E:
                row['de_per_atom_post_anneal'] = ann['E_post_relax'] / ann['n_atoms'] - base_E
            row['delta_E_anneal_meV'] = ann.get('delta_E_anneal_meV_per_atom', None)
        row['de_per_atom_screen'] = scr.get('de_per_atom_vs_baseline', None)
        row['dV_over_V0'] = blob.get('_screening', {}).get('dV_over_V0', None)
        # Tier-2
        t2 = scr.get('tier2', {})
        row['li_li_disorder_std'] = t2.get('li_li_disorder_std', None)
        row['dopant_blocking_frac'] = t2.get('dopant_blocking_fraction', None)
        # BVSE
        bv = blob.get('_bvse', {})
        row['migration_volume_pct'] = (bv.get('migration_volume_fraction', None) * 100
                                       if bv.get('migration_volume_fraction') is not None
                                       else None)
        row['bvs_li_proxy'] = bv.get('bvs_li_proxy_score', None)
        row['li_mobility_score'] = bv.get('li_mobility_score', None)
        # EOS
        eos = blob.get('_eos', {}).get('eos', {})
        row['B0_GPa'] = eos.get('B0_GPa', None)
        row['V0_per_atom'] = eos.get('V0_per_atom', None)
        # Elastic
        ela = blob.get('_elastic', {}).get('elastic', {})
        row['E_young_GPa'] = ela.get('E_young_GPa', None)
        row['B_hill_GPa'] = ela.get('B_hill_GPa', None)
        row['G_hill_GPa'] = ela.get('G_hill_GPa', None)
        row['pugh_ratio'] = ela.get('pugh_ratio_GoverB', None)
        row['poisson_nu'] = ela.get('poisson_nu', None)
        rows.append(row)
    return rows


def _de_of(r):
    """안정성 축 원값 — post-anneal 우선, 없으면 screen. (기존 표현을 함수화)"""
    return r.get('de_per_atom_post_anneal') or r.get('de_per_atom_screen')


def no_rows_message(cd):
    """구조 0개일 때의 설명. **죽은 축과 구별해서** 말한다.

    ⛔ 왜 필요한가: rows 가 비면 모든 축이 0/0 → 'all_missing' 으로 찍혀
      '축이 죽었다(=backfill 필요)' 처럼 보인다. 실제 원인은 **경로가 틀렸거나
      스테이지 산출물이 없는 것**이라 처방이 정반대다 (2026-08-25).
    """
    lines = [f"⛔ 구조를 하나도 못 읽었다 — 축 문제가 **아니다**.",
             f"   cascade_dir 은 스테이지 폴더를 **직접** 담은 디렉터리다:",
             f"     <cascade_dir>/02_screen/uma_results.json  ← 이런 구조",
             f"   준 경로: {cd}"]
    kids = []
    try:
        kids = sorted(c.name for c in cd.iterdir()
                      if c.is_dir() and (c / '02_screen').is_dir())
    except OSError:
        pass
    if kids:
        lines.append(f"   ★ 이 경로는 **상위 묶음**이다 — 안에 캐스케이드 {len(kids)}개가 있다.")
        lines.append(f"     예: {cd / kids[0]}")
    elif not cd.is_dir():
        lines.append("   ⛔ 그런 디렉터리가 없다.")
    else:
        lines.append("   하위에 02_screen 을 가진 폴더도 없다 — 캐스케이드가 안 돌았거나 다른 위치다.")
    return "\n".join(lines)


def report_axis_health(weights=None):
    """축 건강을 한 화면으로. 죽은 축이 있으면 조용히 넘어가지 않는다. → 죽은 축 수."""
    print("\n▸ 축 건강 (normalize 실측)")
    dead = []
    for lab, h in AXIS_HEALTH.items():
        w = (weights or {}).get(lab)
        wtxt = f" · 가중치 {w:g}" if w is not None else ""
        if h["state"] == "ok":
            print(f"  ✅ {lab:<12} {h['n_present']}/{h['n']} ({h['coverage_pct']}%){wtxt}")
        else:
            dead.append((lab, h, w))
            why = ("전부 결측" if h["state"] == "all_missing" else "전 행 동일값")
            print(f"  ⛔ {lab:<12} {h['n_present']}/{h['n']} ({h['coverage_pct']}%) "
                  f"— {why} → 0.5 상수{wtxt}")
    if dead:
        lost = sum(w for _, _, w in dead if w is not None)
        print(f"\n  ⚠ 죽은 축 {len(dead)}개. 이 축들은 **순위에 기여하지 않는다.**")
        if lost:
            print(f"    가중치 {lost:g} 만큼이 상수로 흡수됐다 — "
                  f"결과를 '{len(AXIS_HEALTH)}축 랭킹' 이라고 부르면 안 된다.")
        print("    → 입력 결측이면 tools/doping/bvse_proxy.py --backfill_glob 먼저.")
    else:
        print("  ✅ 모든 축이 순위에 실제로 기여한다.")
    return len(dead)


def _selftest():
    """normalize / report_axis_health 만 검증. 음성 경로 포함."""
    n_ok = n_bad = 0

    def chk(c, m):
        nonlocal n_ok, n_bad
        print(("  ✓ " if c else "  ✗ ") + m)
        n_ok, n_bad = n_ok + bool(c), n_bad + (not c)

    AXIS_HEALTH.clear()
    v = normalize([1.0, 2.0, 3.0], label='good')
    chk(v == [0.0, 0.5, 1.0], "정상 축은 0..1 로 편다")
    chk(AXIS_HEALTH['good']['contributes_to_ranking'] is True,
        "정상 축은 기여함으로 기록된다")

    v = normalize([1.0, 2.0, 3.0], invert=True, label='inv')
    chk(v == [1.0, 0.5, 0.0], "invert 는 뒤집는다 (낮을수록 좋은 축)")

    # ★ 이 사고를 재현하는 음성 경로
    v = normalize([None, None, None], label='dead')
    chk(v == [0.5, 0.5, 0.5], "[음성] 전부 결측이면 0.5 상수")
    chk(AXIS_HEALTH['dead']['contributes_to_ranking'] is False,
        "[음성] ★ 전부 결측 축은 **기여 안 함**으로 기록된다 — 조용히 넘어가지 않는다")
    chk(AXIS_HEALTH['dead']['state'] == 'all_missing',
        "[음성] 사유가 all_missing 으로 남는다")

    v = normalize([7.0, 7.0, 7.0], label='const')
    chk(AXIS_HEALTH['const']['state'] == 'constant' and
        AXIS_HEALTH['const']['contributes_to_ranking'] is False,
        "[음성] 전 행 동일값도 죽은 축이다 (결측만 잡으면 놓친다)")

    chk(AXIS_HEALTH['dead']['coverage_pct'] == 0.0 and
        AXIS_HEALTH['const']['coverage_pct'] == 100.0,
        "[음성] 커버리지와 기여는 다른 것이다 — const 는 100% 인데도 죽었다")

    # 부분 결측은 살아 있어야 한다 (과잉 차단 방지)
    AXIS_HEALTH.clear()
    v = normalize([1.0, None, 3.0], label='partial')
    chk(AXIS_HEALTH['partial']['contributes_to_ranking'] is True and
        AXIS_HEALTH['partial']['n_present'] == 2,
        "[음성] 일부 결측은 죽은 축이 아니다 — 과잉 차단하지 않는다")
    chk(v[1] == 0.0, "결측 행은 0.0 (최하) 으로 — 0.5 로 메우지 않는다")

    # ★ 구조 0개를 '죽은 축' 과 구별하는가 (2026-08-25 오독 재현)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / 'AlI3_x002' / '02_screen').mkdir(parents=True)
        msg = no_rows_message(root)
        chk('상위 묶음' in msg and 'AlI3_x002' in msg,
            "[음성] 상위 묶음 경로를 주면 '축 문제가 아니라 경로' 라고 말한다")
        chk('backfill' not in msg,
            "[음성] ★ 구조 0개에 backfill 처방을 내리지 않는다 (처방이 정반대)")
        msg2 = no_rows_message(root / 'AlI3_x002')
        chk('상위 묶음' not in msg2 and '02_screen 을 가진 폴더도 없' in msg2,
            "[음성] 잎 경로인데 스테이지 산출물이 없으면 그렇게 말한다")
        chk('그런 디렉터리가 없다' in no_rows_message(root / 'nope'),
            "[음성] 없는 경로는 없다고 말한다")

    dead = report_axis_health({'partial': 0.3})
    chk(dead == 0, "죽은 축이 없으면 0 을 돌려준다")
    AXIS_HEALTH['x'] = {"n": 3, "n_present": 0, "coverage_pct": 0.0,
                        "state": "all_missing", "contributes_to_ranking": False}
    chk(report_axis_health({'x': 0.3}) == 1, "죽은 축이 있으면 개수를 돌려준다")

    # ── A안: 측정된 부분집합에서만 3축 (2026-08-25) ────────────────────────
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        cd = pathlib.Path(td) / 'casc'
        (cd / '02_screen').mkdir(parents=True)
        (cd / '05_bvse').mkdir(parents=True)
        (cd / '08_elastic').mkdir(parents=True)
        # 구조 4개: A·B 만 3축 측정, C·D 는 미측정.
        # C 는 **안정성이 제일 좋다** — 결측이 0.0 이면 C 가 부당하게 밀린다.
        (cd / '02_screen' / 'uma_results.json').write_text(json.dumps({'results': [
            {'name': n, 'uma_relaxed': {'de_per_atom_vs_baseline': de}}
            for n, de in [('A', 0.05), ('B', 0.04), ('C', 0.01), ('D', 0.09)]]}))
        (cd / '05_bvse' / 'bvs_report.json').write_text(json.dumps({'records': [
            {'name': 'A', 'li_mobility_score': 0.9},
            {'name': 'B', 'li_mobility_score': 0.2}]}))
        (cd / '08_elastic' / 'postproc_summary.json').write_text(json.dumps({'records': [
            {'name': 'A', 'elastic': {'E_young_GPa': 30.0}},
            {'name': 'B', 'elastic': {'E_young_GPa': 20.0}}]}))
        rows = load_rows(cd)
        chk(len(rows) == 4, "load_rows: 스테이지 union 으로 구조 4개")
        meas = [r for r in rows if r.get('E_young_GPa') is not None
                and r.get('li_mobility_score') is not None]
        chk(sorted(r['name'] for r in meas) == ['A', 'B'],
            "3축 대상은 modulus·mobility 를 **둘 다** 가진 것만")
        chk(len(meas) == 2 and 'C' not in [r['name'] for r in meas],
            "[음성] ★ 한 축만 있는 구조는 3축에 넣지 않는다")

        AXIS_HEALTH.clear()
        mob_m = normalize([r.get('li_mobility_score') for r in meas], label='mob_m')
        chk(set(mob_m) == {0.0, 1.0} and len(mob_m) == 2,
            "부분집합 안에서 정규화 — 미측정이 0.0 을 받지 않는다")
        # 옛 방식(전체 정규화)과 대조: C 가 0.0 을 받는지
        old_mob = normalize([r.get('li_mobility_score') for r in rows])
        n_zero_old = sum(1 for r, v in zip(rows, old_mob)
                         if r.get('li_mobility_score') is None and v == 0.0)
        chk(n_zero_old == 2,
            "[음성] ★ 옛 방식은 미측정 2개에 0.0(최하)을 줬다 — 이게 고친 대상")

        chk(find_cascades(str(pathlib.Path(td) / '*')) == [cd],
            "find_cascades: 상위 묶음을 줘도 02_screen 가진 잎을 찾는다")
        chk(find_cascades(str(cd)) == [cd],
            "find_cascades: 잎을 직접 줘도 된다")
        chk(find_cascades(str(pathlib.Path(td) / 'nope*')) == [],
            "[음성] 못 찾으면 빈 리스트 — 지어내지 않는다")

    print(f"selftest {'PASS' if not n_bad else 'FAIL'} — {n_ok} ok, {n_bad} bad")
    return 1 if n_bad else 0


def find_cascades(pattern):
    """glob 에서 **02_screen 을 가진 디렉터리만** 골라낸다. bak 경로는 뺀다."""
    import glob as _glob
    seen, out = set(), []
    for hit in sorted(_glob.glob(pattern, recursive=True)):
        d = pathlib.Path(hit)
        if not d.is_dir() or 'bak' in str(d):
            continue
        cands = [d] if (d / '02_screen').is_dir() else [
            c for c in sorted(d.iterdir())
            if c.is_dir() and (c / '02_screen').is_dir() and 'bak' not in c.name]
        for c in cands:
            k = str(c.resolve())
            if k not in seen:
                seen.add(k)
                out.append(c)
    return out


def _batch(args):
    """--cascade_glob: 전수 인구조사. **집계만 하고 순위 파일은 쓰지 않는다.**

    ⛔ 못 하는 것: FINAL_RANKING.json 을 캐스케이드마다 쓰지 않는다 — 그건
      결과를 바꾸는 일이라 잎별 --out 을 명시해 돌려야 한다. 여기서는
      "전체 풀이 몇 개이고 3축 비교가 가능한 게 몇 개인가" 만 센다.
    """
    dirs = find_cascades(args.cascade_glob)
    if not dirs:
        print(f"⛔ 02_screen 을 가진 디렉터리를 못 찾았다: {args.cascade_glob}")
        return 2
    print(f"캐스케이드 {len(dirs)}개 발견\n")
    tot_s = tot_m = 0
    n_none = n_thin = 0
    per = []
    for d in dirs:
        rows = load_rows(d)
        meas = [r for r in rows
                if r.get('E_young_GPa') is not None
                and r.get('li_mobility_score') is not None]
        tot_s += len(rows); tot_m += len(meas)
        if not meas:
            n_none += 1
        elif len(meas) < 2:
            n_thin += 1
        per.append((d.parent.name + '/' + d.name, len(rows), len(meas)))
    print(f"{'cascade':<46}{'구조':>6}{'3축':>6}")
    for name, ns, nm in per[:40]:
        flag = '  ⛔' if nm == 0 else ('  ⚠n=1' if nm < 2 else '')
        print(f"{name[:44]:<46}{ns:>6}{nm:>6}{flag}")
    if len(per) > 40:
        print(f"  … 그 외 {len(per)-40}개 (전체는 --out_csv 로)")
    print(f"\n▸ 전수 집계")
    print(f"  캐스케이드      {len(dirs)}")
    print(f"  구조 전체       {tot_s}")
    print(f"  3축 측정완료    {tot_m}  ({100.0*tot_m/tot_s:.1f}%)" if tot_s else "")
    print(f"  ⛔ 3축 0개      {n_none}개 캐스케이드 — 이 캐스케이드는 3축 순위가 안 나온다")
    print(f"  ⚠ 3축 1개       {n_thin}개 — 표본 1개는 정규화가 상수라 순위 의미 없음")
    if args.out_csv:
        import csv
        with open(args.out_csv, 'w', newline='') as fh:
            w = csv.writer(fh)
            w.writerow(['cascade', 'n_structures', 'n_measured_3axis'])
            w.writerows(per)
        print(f"\n  ✓ 전체 목록 → {args.out_csv}")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--cascade_dir',
                  help='tier_cascade output directory')
    p.add_argument('--out', help='출력 JSON (--status/--selftest 면 생략)')
    p.add_argument('--w_stab', type=float, default=0.4,
                  help='Weight: stability (post-anneal ΔE)')
    p.add_argument('--w_mod', type=float, default=0.3,
                  help='Weight: modulus (E_young)')
    p.add_argument('--w_mob', type=float, default=0.3,
                  help='Weight: Li mobility (BVSE proxy)')
    p.add_argument('--cascade_glob',
                  help='여러 캐스케이드를 **한 프로세스에서** 처리한다 (예: '
                       '"/data/work/runs/*/*"). 02_screen 을 가진 디렉터리만 고른다 — '
                       '상위 묶음 경로를 줘도 알아서 잎을 찾는다. --status 와 같이 쓰면 '
                       '전수 인구조사가 된다. 캐스케이드가 300개라 쉘 for 문은 '
                       'python 을 300번 띄운다(bvse_proxy 와 같은 교훈).')
    p.add_argument('--status', action='store_true',
                  help='축 커버리지만 보고 **아무것도 안 쓴다**. 어느 축이 실제로 '
                       '순위에 기여하는지 확인용 (--out 은 무시된다). '
                       'li_mobility_score 가 전원 결측이라 3축이 실제로 2축이었던 '
                       '2026-08-25 사고 이후 추가.')
    p.add_argument('--out_csv', help='--cascade_glob 전수 목록 CSV')
    p.add_argument('--selftest', action='store_true',
                  help='정규화·축건강 로직만 검증 (음성 경로 포함) — 데이터 없이 돈다')
    args = p.parse_args()

    if args.selftest:
        return _selftest()

    if args.cascade_glob:
        return _batch(args)

    if not args.cascade_dir:
        print("⛔ --cascade_dir 이 필요하다")
        return 2
    if not args.status and not args.out:
        print("⛔ --out 이 필요하다 (또는 --status 로 보기만)")
        return 2
    cd = Path(args.cascade_dir)
    rows = load_rows(cd, verbose=True)

    # v4.5 (D1): per-group n_seeds mean±std. Each tier_cascade winner is
    # one (dopant, sites, seed) configuration; the Pustorino 2025 result
    # that Li ordering causes ~16 GPa B0 spread means single-seed numbers
    # are misleading for paper claims. We aggregate by name-prefix
    # (everything before "_seed{N}") and emit group mean ± std for the
    # main numeric axes. paper Table reporting uses these.
    import re
    NUMERIC_FIELDS = ['de_per_atom_post_anneal', 'de_per_atom_screen',
                      'dV_over_V0', 'migration_volume_pct',
                      'li_mobility_score', 'B0_GPa', 'V0_per_atom',
                      'E_young_GPa', 'B_hill_GPa', 'G_hill_GPa',
                      'pugh_ratio', 'poisson_nu']
    groups: dict[str, list[dict]] = {}
    for r in rows:
        # v4.5.1 CR-A fix: substitute_struct/substitute_compound emit
        # name_s{NN} (NOT _seed{NN}); previous regex matched nothing →
        # grouped_stats was always empty list (reviewer-caught critical).
        m = re.match(r'(.+?)_s\d+$', r['name'])
        gkey = m.group(1) if m else r['name']
        groups.setdefault(gkey, []).append(r)
    grouped_stats = []
    for gkey, group_rows in groups.items():
        if len(group_rows) < 2:
            continue  # std needs ≥2 seeds
        entry = {'group_key': gkey, 'n_seeds': len(group_rows)}
        for field in NUMERIC_FIELDS:
            vals = [r.get(field) for r in group_rows if r.get(field) is not None]
            if len(vals) >= 2:
                arr = np.array(vals, dtype=float)
                entry[f'{field}_mean'] = float(arr.mean())
                entry[f'{field}_std'] = float(arr.std(ddof=1))
                entry[f'{field}_n'] = len(vals)
        grouped_stats.append(entry)

    # Composite axis scores (min-max normalized)
    de_axis = [_de_of(r) for r in rows]
    _W = {'stability': args.w_stab, 'modulus': args.w_mod, 'mobility': args.w_mob}
    if not rows:
        print(f"\n구조 0개 · cascade_dir {cd}")
        print(no_rows_message(cd))
        return 2

    # ── A안 (2026-08-25 채택): 3축 점수는 **측정된 부분집합 안에서만** 낸다 ──
    #   왜: normalize 의 결측→0.0 이 '미측정 = 최악' 으로 채점해 가중치 0.6 이
    #     '측정됐나' 하나로 갈렸다. 상위 10개만 측정되므로 11위 이하는 구조적으로
    #     못 올라온다(안정성을 두 번 세는 셈). 없는 값을 지어내지 않는 유일한 길이
    #     '측정된 것끼리만 비교' 다. 전체 목록은 stability-only 로 따로 낸다.
    #   ⛔ 못 하는 것: 미측정 구조가 실제로 좋은지 나쁜지 말하지 않는다. **모른다**.
    measured = [r for r in rows
                if r.get('E_young_GPa') is not None
                and r.get('li_mobility_score') is not None]
    de_axis_m = [_de_of(r) for r in measured]
    de_norm = normalize(de_axis_m, invert=True, label='stability')
    mod_norm = normalize([r.get('E_young_GPa') for r in measured], label='modulus')
    mob_norm = normalize([r.get('li_mobility_score') for r in measured],
                         label='mobility')

    if args.status:
        print(f"\n구조 {len(rows)}개 · 3축 측정완료 {len(measured)}개 "
              f"({100.0*len(measured)/len(rows):.0f}%) · {cd}")
        if not measured:
            print("  ⛔ 3축 비교 불가 — modulus·mobility 를 **둘 다** 가진 구조가 없다.")
            return 3
        report_axis_health(_W)
        return 0

    for r, ds, ms, mb in zip(measured, de_norm, mod_norm, mob_norm):
        r['score_stability'] = ds
        r['score_modulus'] = ms
        r['score_mobility'] = mb
        r['score_combined'] = (args.w_stab * ds
                              + args.w_mod * ms
                              + args.w_mob * mb)
        r['scored_on'] = 'measured_subset_3axis'

    # 미측정 구조: 3축 점수를 **주지 않는다** (0.0 도 0.5 도 아니고 없음).
    #   '모른다' 를 숫자로 바꾸는 순간 순위가 그 가짜 숫자를 믿기 시작한다.
    stab_all = normalize(de_axis, invert=True)      # 전체 stability-only 축
    for r, ds in zip(rows, stab_all):
        r['score_stability_all'] = ds
        if 'score_combined' not in r:
            r['score_combined'] = None
            r['scored_on'] = 'stability_only_not_measured'

    measured.sort(key=lambda r: -r['score_combined'])
    rows.sort(key=lambda r: -r['score_stability_all'])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        'provenance': get_provenance(),
        'weights': {'stability': args.w_stab, 'modulus': args.w_mod,
                    'mobility': args.w_mob},
        'n_structures': len(rows),
        'n_measured_3axis': len(measured),
        'scoring_policy': {
            'adopted': 'A (2026-08-25)',
            'rule': '3축 결합점수는 modulus·mobility 를 **둘 다** 가진 구조들 '
                    '안에서만 정규화·산출한다. 미측정 구조는 score_combined = null.',
            'why': 'normalize 의 결측→0.0 이 미측정을 최하점으로 채점해 가중치 0.6 이 '
                   '"측정됐나" 하나로 갈렸다. 상위 10개만 측정되므로 11위 이하가 '
                   '구조적으로 못 올라왔다 (안정성 이중계산).',
            'not_claimed': '미측정 구조가 나쁘다는 뜻이 아니다 — 모른다는 뜻이다.',
            'full_list_axis': 'score_stability_all (안정성 단일축, 전체 구조 대상)',
        },
        'ranking_3axis_measured_only': [r['name'] for r in measured],
        'rows': rows,
        'grouped_stats': grouped_stats,  # v4.5 D1: n_seeds mean±std per group
    }, indent=2, default=str))

    # Top-20 table
    print(f"\n{'='*110}")
    print(f"  TOP-20 — 3축 결합점수 (stab×{args.w_stab} + mod×{args.w_mod} + mob×{args.w_mob})")
    print(f"  ⚠ 대상은 **3축 측정완료 {len(measured)}개**뿐이다 (전체 {len(rows)}개 중). "
          f"미측정 {len(rows)-len(measured)}개는 여기 없다 — 나쁘다는 뜻이 아니라 모른다는 뜻이다.")
    print(f"{'='*110}")
    print(f"{'Rank':<5}{'Name':<40}{'ΔE/at':>8}{'V_mig%':>8}{'B0':>8}{'E_y':>8}{'Pugh':>7}"
          f"{'comb':>8}")
    # N-2 fix: distinguish "missing data" (e.g. EOS fit failed → B0=None)
    # from "data is 0". Display 'n/a' for None instead of 0.0.
    def _fmt(v, spec):
        return '   n/a' if v is None else format(v, spec)
    for i, r in enumerate(measured[:20], 1):
        de_raw = r.get('de_per_atom_post_anneal')
        if de_raw is None:
            de_raw = r.get('de_per_atom_screen')
        vmig = r.get('migration_volume_pct')
        b0 = r.get('B0_GPa')
        ey = r.get('E_young_GPa')
        pg = r.get('pugh_ratio')
        print(f"{i:<5}{r['name'][:38]:<40}"
              f"{_fmt(de_raw, '+7.3f'):>7} "
              f"{_fmt(vmig, '6.2f'):>6}% "
              f"{_fmt(b0, '7.1f'):>7} "
              f"{_fmt(ey, '7.1f'):>7} "
              f"{_fmt(pg, '6.3f'):>6} "
              f"{r['score_combined']:>7.3f}")
    print(f"\n✓ 전체 {len(rows)} · 3축 {len(measured)} → {out}")
    if len(rows) != len(measured):
        print(f"  · 전체 목록의 순서는 score_stability_all (안정성 단일축) 기준이다.")

    # ★ 축 건강은 **표 뒤에 반드시 찍는다.** 죽은 축이 조용히 지나가면
    #   '3축 랭킹' 이라는 잘못된 이름이 그대로 하류로 간다 (2026-08-25 사고).
    n_dead = report_axis_health({'stability': args.w_stab, 'modulus': args.w_mod,
                                 'mobility': args.w_mob})
    return 2 if n_dead else 0


if __name__ == '__main__':
    sys.exit(main() or 0)
