#!/usr/bin/env python3
"""A-2(a) 기하 debond / void 궤적 — MPM 재변형 앵커의 *정당한* 산출만 (M3 재작성판).

`mpm3d_compaction.py --cycle-deform --save-metrics` 가 낸 앵커 metrics JSON 여러 개(N=0 기저 +
N>0 재변형)를 받아 **AM-SE 분리 = 기하 debond(N)** 와 **void(N)** 궤적으로 리포트한다.

★ 이것이 "crack" 이 아닌 이유 (real_degrading_electrode_design §3 A-2, 적대리뷰 M3):
  현 J2 MPM 엔 응력장·crack 필드가 없다(szz = 0차원 전역 스칼라, von Mises 는 σ_y 클램프).
  그래서 여기 나오는 건 MPM 의 *검증된 강점*인 **coverage(=AM-SE 접촉 기하) 변화 + void-fill
  재유동** 뿐 — AM 수축/팽창으로 SE 접촉이 열리면 coverage 가 떨어지고(=기하 debond), 열린
  공간을 SE 가 다 못 메우면 void 가 는다.  이걸 "응력-파괴/취성 crack" 으로 부르지 **않는다**.
  진짜 취성 파괴(G_c/K_IC, LPSCl 0.23)는 FEM/phase-field 소관(A-2(b), frame[5]) — 미구현.

★★ 가역 vs 비가역 주의 (적대리뷰 전기화학#1 + 물리 개념노트, 2026-07-22) ★★
  A-1 앵커는 **충전-상태(charge-STATE) 기하** = 방전 시 되돌아가는 **가역 SOC breathing**(SC 격자수축
  −5.1%는 방전서 복원)이다.  그러므로 이 도구의 debond(N)/void(N)는 그 자체로 **영구 열화가 아니라
  "충전상태 접촉 간극"**이다.  **영구(비가역) 열화 궤적이 되려면** 앵커의 ΔV가 *누적 비가역 변형*
  (소성 재유동으로 접촉이 안 닫힘 / 입계 crack void)을 담아야 하고, 그건 풀 MPM 재평형(GPU) + ledger
  CZM/δcr·re-contact 게이트가 판정한다.  → 단일 충전 스냅샷의 Δ를 "영구 fade"로 읽지 말 것.

라벨: 전 산출은 **기하(geometric) · MPM void-fill · 충전상태(가역) · ASSUMED-FORM(v1)**.  N-사이
궤적/법칙 + 비가역화 판정은 ledger(A-3) 소관이며 여기선 앵커 점만 찍는다(보간 안 함).

사용법:
  python3 scripts/cycle_geom_debond.py N0.json N5.json N10.json [--csv out.csv]
  python3 scripts/cycle_geom_debond.py --selftest
"""
import json
import sys


_VOID_KEYS = ('porosity_settled_pct', 'porosity_at_target_pct')   # void = 다공도 (settled 우선)


def _void(m):
    for k in _VOID_KEYS:
        v = m.get(k)
        if v is not None:
            return float(v), k
    return None, None


def _rec(path_or_dict):
    """metrics dict/JSON → 앵커 레코드 (N, void, coverage, thickness, evict, labels)."""
    if isinstance(path_or_dict, dict):
        m = path_or_dict
    else:
        with open(path_or_dict) as _f:                  # (m7) leak-free + surfaces path in error
            m = json.load(_f)
    cyc = m.get('cycle_deform')                         # None = pristine (no --cycle-deform)
    void, void_src = _void(m)
    # ★ (code M1) baseline = TRULY undeformed only.  --cycle-n defaults to 0 while --cycle-dv-sc/-poly
    #   default nonzero, so a --cycle-deform run that FORGOT --cycle-n emits a DEFORMED geometry tagged
    #   N=0 → must NOT be mistaken for pristine.  Require ΔV≈0 (a deformed anchor always has nonzero ΔV).
    _dv_mag = ((abs(float(cyc.get('dv_sc') or 0.0)) + abs(float(cyc.get('dv_poly') or 0.0))) if cyc else 0.0)
    is_baseline = (cyc is None) or (int(cyc.get('N', 0)) == 0 and _dv_mag < 1e-9)
    return {
        'source': '<dict>' if isinstance(path_or_dict, dict) else path_or_dict,
        'N': int(cyc.get('N', 0)) if cyc else 0,        # (m4) safe access (foreign JSON may omit N)
        'is_baseline': is_baseline,
        'void_pct': void, 'void_src': void_src,
        'cov_AM_P': m.get('coverage_AM_P_pct'), 'cov_AM_S': m.get('coverage_AM_S_pct'),
        'thickness_um': m.get('thickness_um'),
        'dv_sc': cyc.get('dv_sc') if cyc else None,
        'dv_poly': cyc.get('dv_poly') if cyc else None,
        'dv_pct_poly': cyc.get('dv_pct_poly') if cyc else None,
        'se_evict_pct': cyc.get('se_evict_pct') if cyc else None,
        'assumed_form': bool(cyc.get('assumed_form')) if cyc else None,
    }


def _dsub(a, b):
    return None if (a is None or b is None) else round(float(a) - float(b), 3)


def trajectory(records):
    """정렬된 앵커 레코드 → 기하 debond/void 궤적 (기저 N=0 대비 Δ).

    debond = coverage LOSS (기저−현) ≥0 ⇒ AM-SE 접촉 이탈;  void_incr = 다공도 증가 (현−기저).
    """
    recs = sorted(records, key=lambda r: r['N'])
    base = next((r for r in recs if r['is_baseline']), None)
    if base is None:
        base = recs[0]                                   # 기저 없음 → 최저 N 을 기저로(경고는 report 에서)
    out = []
    for r in recs:
        out.append({
            **r,
            'is_ref': r is base,
            'void_incr_pp': _dsub(r['void_pct'], base['void_pct']),          # +pp = 새 void
            'debond_AM_P_pp': _dsub(base['cov_AM_P'], r['cov_AM_P']),        # +pp = coverage 손실(debond)
            'debond_AM_S_pp': _dsub(base['cov_AM_S'], r['cov_AM_S']),
            'dthickness_um': _dsub(r['thickness_um'], base['thickness_um']),
        })
    return out, base


def report(records, csv_path=None):
    traj, base = trajectory(records)
    print("=" * 96)
    print("A-2(a) 기하 debond / void 궤적 — MPM 재변형 앵커  [geometric · void-fill · 충전상태(가역) · ASSUMED-FORM v1]")
    print("  ⚠ 이것은 crack 이 아님: coverage(기하 접촉) 변화 + void-fill 재유동만.  취성 파괴(G_c)=FEM/")
    print("     phase-field(A-2(b), frame[5], 미구현).  N-사이 보간 안 함(앵커 점만; 궤적법칙=ledger A-3).")
    print("  ⚠ 가역/비가역: Δ 는 충전-상태(방전서 되돌아가는 가역 SOC breathing) 접촉간극 — 그 자체로 영구")
    print("     fade 아님.  영구화 판정 = 풀 MPM 소성 재평형 + ledger CZM/re-contact (docstring 참조).")
    print(f"  기저(N=0 ref) = {base['source']}   void_src={base['void_pct']}% ({base['void_src']})")
    if not any(r['is_baseline'] for r in records):
        print("  ⚠ 진짜 N=0 pristine 앵커 없음 → 최저 N 을 기저로 대용(Δ 는 상대값; pristine 재변형-무 앵커 권장).")
        print("     (--cycle-deform 하면서 --cycle-n 만 빠뜨린 변형-앵커는 이제 pristine 으로 오인 안 함 = 이 경고가 뜸.)")
    print("-" * 96)
    hdr = f"{'N':>4} {'void%':>7} {'Δvoid_pp':>9} {'covP%':>6} {'debP_pp':>8} {'covS%':>6} {'debS_pp':>8} {'thk_um':>7} {'evict%':>7}"
    print(hdr)
    rows = []
    for r in traj:
        def _f(x, w, p='.1f'):
            return (f"{x:>{w}{p}}" if isinstance(x, (int, float)) else f"{'—':>{w}}")
        tag = ' ←ref' if r['is_ref'] else ''
        print(f"{r['N']:>4} {_f(r['void_pct'],7)} {_f(r['void_incr_pp'],9)} "
              f"{_f(r['cov_AM_P'],6)} {_f(r['debond_AM_P_pp'],8)} "
              f"{_f(r['cov_AM_S'],6)} {_f(r['debond_AM_S_pp'],8)} "
              f"{_f(r['thickness_um'],7)} {_f(r['se_evict_pct'],7,'.2f')}{tag}")
        if r['se_evict_pct'] not in (None, 0) and float(r['se_evict_pct']) > 0.5:
            print(f"       ⚠ N={r['N']}: SE 퇴출 {r['se_evict_pct']}% (poly-팽창 삭제, v1 체적 비보존) → 이 void 는 일부 삭제-아티팩트")
        rows.append(r)
    print("=" * 96)
    if csv_path:
        import csv as _csv
        cols = ['source', 'N', 'is_ref', 'void_pct', 'void_incr_pp', 'cov_AM_P', 'debond_AM_P_pp',
                'cov_AM_S', 'debond_AM_S_pp', 'thickness_um', 'dthickness_um', 'se_evict_pct',
                'dv_sc', 'dv_poly', 'dv_pct_poly', 'assumed_form']
        with open(csv_path, 'w', newline='') as f:
            w = _csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print(f"  saved → {csv_path}")
    return traj


def _selftest():
    """합성 앵커 3점(N=0/10/50)으로 궤적 논리 검증 — SC 수축이 coverage 를 떨어뜨리고 void 를 올린다."""
    base = {'porosity_settled_pct': 15.9, 'coverage_AM_P_pct': 74.0, 'coverage_AM_S_pct': 52.0,
            'thickness_um': 30.0}                         # cycle_deform None → pristine 기저
    n10 = {'porosity_settled_pct': 17.4, 'coverage_AM_P_pct': 73.2, 'coverage_AM_S_pct': 48.5,
           'thickness_um': 30.4,
           'cycle_deform': {'N': 10, 'dv_sc': -0.051, 'dv_poly': 0.059, 'dv_pct_poly': 0.30,
                            'se_evict_pct': 0.0, 'assumed_form': True}}
    n50 = {'porosity_settled_pct': 19.8, 'coverage_AM_P_pct': 72.1, 'coverage_AM_S_pct': 44.0,
           'thickness_um': 31.1,
           'cycle_deform': {'N': 50, 'dv_sc': -0.059, 'dv_poly': 0.059, 'dv_pct_poly': 0.30,
                            'se_evict_pct': 0.8, 'assumed_form': True}}
    recs = [_rec(n50), _rec(base), _rec(n10)]             # 일부러 순서 섞음 → 정렬 검증
    traj, b = trajectory(recs)
    ok = 0
    tot = 0
    def chk(name, cond):
        nonlocal ok, tot
        tot += 1
        ok += bool(cond)
        print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    print("=== A-2(a) cycle_geom_debond selftest ===")
    chk("정렬: N 오름차순", [r['N'] for r in traj] == [0, 10, 50])
    chk("기저 = pristine(cycle_deform None)", b['N'] == 0 and b['is_baseline'])
    chk("기저 debond/void = 0", traj[0]['void_incr_pp'] == 0 and traj[0]['debond_AM_S_pp'] == 0)
    chk("N=10 void 증가(+1.5pp)", traj[1]['void_incr_pp'] == 1.5)
    chk("N=10 AM_S debond 양수(SC 수축→접촉 이탈, +3.5pp)", traj[1]['debond_AM_S_pp'] == 3.5)
    chk("N=50 void 최대(+3.9pp)", traj[2]['void_incr_pp'] == 3.9)
    chk("N=50 AM_S debond 단조 증가(>N=10)", traj[2]['debond_AM_S_pp'] > traj[1]['debond_AM_S_pp'])
    chk("AM_P debond < AM_S debond (poly 팽창=접촉 유지, SC 수축=이탈)",
        traj[2]['debond_AM_P_pp'] < traj[2]['debond_AM_S_pp'])
    chk("N=50 evict% 노출(0.8, 비보존 caveat)", traj[2]['se_evict_pct'] == 0.8)
    chk("ASSUMED-FORM 플래그 전파", traj[1]['assumed_form'] is True)
    # ── (code M1) 변형 앵커를 N=0 으로 태깅(--cycle-n 누락) → pristine 오인 금지 ──────────────
    deformed_n0 = {'porosity_settled_pct': 17.4, 'coverage_AM_P_pct': 73.2, 'coverage_AM_S_pct': 48.5,
                   'thickness_um': 30.4,
                   'cycle_deform': {'N': 0, 'dv_sc': -0.051, 'dv_poly': 0.059, 'dv_pct_poly': 0.30,
                                    'se_evict_pct': 0.0, 'assumed_form': True}}
    chk("M1: 변형(ΔV≠0) 앵커가 N=0 이어도 baseline 아님", _rec(deformed_n0)['is_baseline'] is False)
    chk("M1: 진짜 pristine(cycle_deform None)만 baseline", _rec(base)['is_baseline'] is True)
    # ── (m5) 진짜 pristine 없음 → 최저 N 대용 + 경고 경로 ───────────────────────────────────
    traj_np, b_np = trajectory([_rec(n10), _rec(n50)])   # 둘 다 변형 → pristine 없음
    chk("m5: pristine 없으면 최저 N(=10) 을 기저로 대용", b_np['N'] == 10 and traj_np[0]['void_incr_pp'] == 0)
    # ── (m5) coverage 키 결측 → debond None(표에서 '—') , 크래시 없음 ──────────────────────────
    no_cov = {'porosity_settled_pct': 18.0, 'thickness_um': 30.5,
              'cycle_deform': {'N': 20, 'dv_sc': -0.051, 'dv_poly': 0.059, 'assumed_form': True}}
    traj_nc, _ = trajectory([_rec(base), _rec(no_cov)])
    chk("m5: coverage 키 결측 → debond=None(크래시 없음)", traj_nc[1]['debond_AM_P_pp'] is None)
    # ── (m5) void 소스 fallback: settled 없고 at_target 만 ─────────────────────────────────────
    chk("m5: void_src = porosity_at_target_pct fallback",
        _rec({'porosity_at_target_pct': 16.2})['void_src'] == 'porosity_at_target_pct')
    print(f"=== {ok}/{tot} PASS ===")
    print()
    report(recs)                                          # 표 렌더도 예외 없이 도는지
    report([_rec(base), _rec(no_cov)])                    # 결측-coverage 표도 예외 없이(m5)
    return ok == tot


def main(argv):
    if '--selftest' in argv:
        sys.exit(0 if _selftest() else 1)
    csv_path = None
    if '--csv' in argv:
        i = argv.index('--csv')
        csv_path = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    paths = [a for a in argv if not a.startswith('--')]
    if not paths:
        print(__doc__)
        sys.exit(2)
    report([_rec(p) for p in paths], csv_path=csv_path)


if __name__ == '__main__':
    main(sys.argv[1:])
