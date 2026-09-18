#!/usr/bin/env python3
"""Phase A 판정기 — VGCF 조성 순서가 격자·origin 전부에서 유지되나 (ORDER-ROBUST/UNRESOLVED).

    python3 scripts/phase_a_order_verdict.py --dir docs/data/phase_a_6mah/arms
    python3 scripts/phase_a_order_verdict.py --selftest

사전등록 = `docs/reviews/phase_a_6mah_order_prereg_20260907.md` §2.  **그 규칙만** 구현한다.

━━ 판정 규칙 (런 전 고정 — 여기서 바꾸지 않는다) ━━━━━━━━━━━━━━━━━━━━━━━━━━━
인접 조성쌍 `k → k+1`, 격자 `h`, origin `o` 에 대해

    d(h, o, k) = log σ_e(w_{k+1}, h, o) − log σ_e(w_k, h, o)

  ORDER-ROBUST      모든 (h, o, k) 에서  d > δ_num
  ORDER-UNRESOLVED  하나라도            d ≤ δ_num

`δ_num = 0.04 %`.  8 origins 는 무작위 표본이 아니라 **완전 nuisance 집합**이므로 산포를
통계로 다루지 않고 **최악 팔을 직접** 본다.  평균·SD·범위는 **기술 보고 전용**이고 게이트가
아니다 (옛 초안의 "origin 산포 문턱" 은 폐기됐다).

━━ fail-closed 조항 (오늘 하루 잡은 결함들의 예방접종) ━━━━━━━━━━━━━━━━━━━━━
① **설계 격자점이 하나라도 비면 판정하지 않는다.**  부분집합을 훑으면 조용히 초록이 된다 —
   CLAUDE.md 규율 ⑤ 의 바로 그 병이고, 72팔 초안이 실제로 그렇게 무너졌다 (CL-71).
② **미수렴·비유한 solve 가 있으면 거부**한다 (CL-30 계열).
③ **exact replay 가 δ_num 을 넘으면 전체 HOLD** — 문턱을 사후 확대하지 않는다.
④ **Secondary(Lee)·QC 는 ORDER-* 판정에 관여하지 못한다** (estimand 분리).
⑤ **δ_num 을 CLI 로 못 바꾼다.**  등록된 값이 상수로 박혀 있다 — 판정 후 문턱을 움직이는
   가장 흔한 사고를 코드가 막는다.  (진단용으로 보고 싶으면 `--what-if` 가 **판정 없이**
   민감도만 찍는다.)

━━ 입력 계약 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`--dir` 아래의 `*.json` 각각이 팔 하나다.  읽는 키 (없으면 거부):

    role        'primary' | 'secondary' | 'qc_replay'
    vgcf_wt     조성 축 (primary/qc)          vox        격자 [µm]
    origin      0..7                          sigma_e    [S/cm]
    unconverged (bool)                        cg_info / resid (선택)

⚠ 대상의 **자기 신고**(예: 팔이 스스로 'ok' 라고 적은 필드)는 읽지 않는다 — 원자료에서
  재계산한다 (CLAUDE.md 규율).
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#  ── 사전등록 상수 — **CLI 로 바꿀 수 없다** ────────────────────────────────────
DELTA_NUM_PCT = 0.04                       # prereg §2
DELTA_NUM = math.log1p(DELTA_NUM_PCT / 100.0)      # log 차로 환산
PREREG = {'vgcf_wts': (1.0, 2.0, 3.0, 4.0), 'voxes': (0.25, 0.20, 0.15), 'n_origin': 8}
_REQUIRED = ('role', 'vox', 'origin', 'sigma_e')


def load_arms(d):
    """팔 JSON 을 읽어 검증한다.  키가 없거나 값이 비물리적이면 **거부**."""
    arms, bad = [], []
    files = sorted(glob.glob(os.path.join(d, '*.json')))
    if not files:
        raise SystemExit(f'⛔ {d} 에 팔 JSON 이 없다 — 빈 glob 로 판정하지 않는다')
    for p in files:
        try:
            a = json.load(open(p))
        except Exception as e:
            bad.append(f'{os.path.basename(p)}: 읽기 실패 {type(e).__name__}'); continue
        miss = [k for k in _REQUIRED if k not in a]
        if miss:
            bad.append(f'{os.path.basename(p)}: 키 없음 {miss}'); continue
        if a['role'] in ('primary', 'qc_replay') and 'vgcf_wt' not in a:
            bad.append(f'{os.path.basename(p)}: primary/qc 인데 vgcf_wt 가 없다'); continue
        s = a['sigma_e']
        if not isinstance(s, (int, float)) or not math.isfinite(s) or s <= 0:
            bad.append(f'{os.path.basename(p)}: sigma_e 가 유한 양수가 아니다 ({s})'); continue
        a['_file'] = os.path.basename(p)
        arms.append(a)
    if bad:
        raise SystemExit('⛔ 읽을 수 없는 팔이 있다 — 판정하지 않는다:\n  ' + '\n  '.join(bad))
    return arms


def check_convergence(arms):
    """② 미수렴·비유한이 하나라도 있으면 거부."""
    bad = [a['_file'] for a in arms
           if a.get('unconverged') or int(a.get('cg_info', 0) or 0) != 0]
    return bad


def check_coverage(primary, prereg=PREREG):
    """① 설계 격자점 전수 확인 — 빠진 칸이 있으면 판정 자체를 하지 않는다."""
    have = {(round(float(a['vgcf_wt']), 6), round(float(a['vox']), 6), int(a['origin']))
            for a in primary}
    want = {(round(w, 6), round(v, 6), o)
            for w in prereg['vgcf_wts'] for v in prereg['voxes']
            for o in range(prereg['n_origin'])}
    return sorted(want - have), sorted(have - want)


def replay_gate(qc, primary, prereg=PREREG):
    """③ exact replay — QC 팔을 **primary 쌍둥이**와 직접 비교한다.

    ⚠⚠ 2026-09-07 (Codex R9, P0-2) — 초판은 **fail-open** 이었다.  QC 끼리만 묶고
    `len(g) < 2` 를 `continue` 로 건너뛰었는데, 계획은 셀마다 primary 1 + QC 1 을 만든다
    ⇒ **모든 묶음이 길이 1** 이라 `rows` 가 비고 `passes = None` 이 되어, 그대로 순서 판정으로
    넘어가 `ORDER-ROBUST` 가 나왔다.  QC 값을 9.9 (참값의 1000배) 로 넣어도 통과했다.
    ★ **음성대조가 한 번도 발화하지 않는 상태였다** — 내가 false-green 을 막으려고 만든
    도구 자신이 오늘 하루 고쳐 온 바로 그 결함을 갖고 있었다.

    ⇒ 세 가지를 fail-closed 로 바꾼다:
      ① QC 는 같은 (조성, vox, origin) 의 **primary 와** 비교한다 (QC 끼리가 아니라).
      ② 짝을 못 찾은 QC 가 하나라도 있으면 **거부**.
      ③ QC 가 **하나도 없으면** 거부 — 음성대조 없이 판정하지 않는다.
    """
    idx = {}
    for a in primary:
        idx[(round(float(a['vgcf_wt']), 6), round(float(a['vox']), 6), int(a['origin']))] = a
    rows, worst, orphan, dup = [], 0.0, [], []
    seen = set()
    for a in qc:
        key = (round(float(a['vgcf_wt']), 6), round(float(a['vox']), 6), int(a['origin']))
        t = idx.get(key)
        if t is None:
            orphan.append(a.get('_file', str(key))); continue
        if key in seen:
            dup.append(a.get('_file', str(key)))
        seen.add(key)
        d = abs(math.log(float(a['sigma_e']) / float(t['sigma_e'])))
        worst = max(worst, d)
        rows.append({'key': list(key), 'abs_log_diff': d, 'pct': 100.0 * (math.exp(d) - 1.0),
                     'qc_file': a.get('_file'), 'primary_file': t.get('_file')})
    out = {'pairs': rows, 'n_qc': len(qc), 'orphan_qc': orphan, 'duplicate_qc': dup,
           'worst_abs_log_diff': worst, 'worst_pct': 100.0 * (math.exp(worst) - 1.0)}
    #  ★★★ PA12-07 (2026-09-18) — **전수를 요구한다.**  옛 판은 `not qc` 만 봐서
    #    정상 8 개 중 **7 개를 지우고 1 개만 남겨도** `ORDER-ROBUST` 가 나왔다.
    #    ⇒ QC 를 (조성, vox) 로 묶고 각 묶음이 `n_origin` 전수인지 본다.
    #  ⚠ 이것은 **등록 밖 게이트가 아니다** — 사전등록 §1 이 `QC exact replay × 8 origin`
    #    을 등록했고, 여기서는 그 등록을 강제할 뿐이다 (문턱을 새로 세우지 않는다).
    _n_o = int(prereg['n_origin'])
    _grp = {}
    for a in qc:
        _grp.setdefault((round(float(a['vgcf_wt']), 6), round(float(a['vox']), 6)),
                        set()).add(int(a['origin']))
    _short = {f'{w:g}/{v:g}': sorted(set(range(_n_o)) - got)
              for (w, v), got in _grp.items() if len(got) < _n_o}
    out['qc_groups'] = {f'{w:g}/{v:g}': sorted(got) for (w, v), got in _grp.items()}
    if not qc:
        out['passes'] = False
        out['refused'] = 'QC(exact replay) 팔이 하나도 없다 — 음성대조 없이 판정하지 않는다'
    elif _short:
        out['passes'] = False
        out['missing_qc_origins'] = _short
        out['refused'] = (f'QC 가 **전수가 아니다** — 사전등록은 origin {_n_o} 개 전수를 '
                          f'등록했는데 빠진 것이 있다: '
                          + ' · '.join(f'{k} 에 origin {v}' for k, v in sorted(_short.items()))
                          + '.  부분집합 음성대조는 조용히 초록이 된다 (PA12-07)')
    elif orphan:
        out['passes'] = False
        out['refused'] = (f'primary 쌍둥이를 못 찾은 QC 가 {len(orphan)} 개 — 무엇과 비교했는지 '
                          f'말할 수 없으면 음성대조가 아니다')
    elif dup:
        out['passes'] = False
        out['refused'] = f'같은 셀에 QC 가 중복 {len(dup)} 개 — 어느 것이 replay 인지 모호하다'
    else:
        out['passes'] = bool(worst <= DELTA_NUM)
    return out


def order_stats(primary, prereg=PREREG):
    """인접쌍 d(h,o,k) 전수.  **최악 팔**이 판정을 정한다."""
    sig = {}
    for a in primary:
        sig[(round(float(a['vgcf_wt']), 6), round(float(a['vox']), 6), int(a['origin']))] = \
            float(a['sigma_e'])
    ws = sorted(prereg['vgcf_wts'])
    ds = []
    for v in prereg['voxes']:
        for o in range(prereg['n_origin']):
            for k in range(len(ws) - 1):
                a, b = sig.get((round(ws[k], 6), round(v, 6), o)), \
                       sig.get((round(ws[k + 1], 6), round(v, 6), o))
                if a is None or b is None:
                    continue                       # ① 이 이미 걸렀다
                ds.append({'vox': v, 'origin': o, 'pair': [ws[k], ws[k + 1]],
                           'd': math.log(b / a), 'pct': 100.0 * (b / a - 1.0)})
    return ds


def verdict(arms):
    """사전등록 §2 그대로.  ⚠ 여기에 새 게이트를 추가하지 말 것 — 등록 밖 판정이 된다."""
    primary = [a for a in arms if a['role'] == 'primary']
    qc = [a for a in arms if a['role'] == 'qc_replay']
    out = {'delta_num_pct': DELTA_NUM_PCT, 'n_primary': len(primary), 'n_qc': len(qc),
           'n_secondary': sum(1 for a in arms if a['role'] == 'secondary')}

    unconv = check_convergence(arms)
    if unconv:
        out.update(order='REFUSED', refused=f'미수렴/비유한 solve {len(unconv)} 팔',
                   unconverged_files=unconv[:20])
        return out
    #  ★★★ PA12-07 (2026-09-18) — **중복 primary 를 거부한다.**
    #    `check_coverage` 는 `have` 를 **집합**으로 세어 중복이 원리적으로 안 보이고,
    #    `order_stats` 의 `sig[key] = …` 는 **마지막 값**이 이긴다.  팔은 `*.json` 을
    #    **파일명 정렬**로 읽으므로 ⇒ 같은 잘못된 중복을 `000_*.json` 로 넣으면 한 판정,
    #    `zzz_*.json` 로 넣으면 다른 판정이 나왔다 = **이름이 결론을 골랐다**.
    #  ⚠ 등록 밖 게이트가 아니다 — 입력이 모호하면 **판정하지 않는다**는 것이고,
    #    사전등록 §2 가 이미 셀당 팔 하나를 전제한다.
    _seen, _dups = set(), []
    for a in primary:
        _k = (round(float(a['vgcf_wt']), 6), round(float(a['vox']), 6), int(a['origin']))
        (_dups.append((a.get('_file'), _k)) if _k in _seen else None)
        _seen.add(_k)
    if _dups:
        out.update(order='REFUSED',
                   refused=(f'primary 가 같은 설계 칸에 **중복** {len(_dups)} 개 — 어느 값이 '
                            f'그 칸인지 모호하다.  옛 판은 파일명 정렬 순서가 이긴 값을 골라 '
                            f'**이름이 결론을 정했다** (PA12-07)'),
                   duplicate_primary=[[f, list(k)] for f, k in _dups[:20]])
        return out
    missing, extra = check_coverage(primary)
    if missing:
        out.update(order='REFUSED',
                   refused=(f'설계 격자점 {len(missing)} 칸이 비었다 — 부분집합으로 판정하면 '
                            f'조용히 초록이 된다 (CL-71)'),
                   missing_cells=[list(m) for m in missing[:20]])
        return out
    if extra:
        out['extra_cells'] = [list(e) for e in extra[:20]]      # 보고만 (등록 밖 팔)

    rep = replay_gate(qc, primary)
    out['replay'] = rep
    if not rep['passes']:
        out.update(order='HOLD',
                   refused=rep.get('refused') or
                   (f'exact replay 가 δ_num 을 넘었다 ({rep["worst_pct"]:.4f} % > '
                    f'{DELTA_NUM_PCT} %) — 문턱을 확대하지 말고 전체 HOLD (prereg §2)'))
        return out

    ds = order_stats(primary)
    ds_sorted = sorted(ds, key=lambda r: r['d'])
    worst = ds_sorted[0]
    ok = worst['d'] > DELTA_NUM
    out.update(order='ORDER-ROBUST' if ok else 'ORDER-UNRESOLVED',
               n_comparisons=len(ds), worst_arm=worst,
               n_violating=sum(1 for r in ds if r['d'] <= DELTA_NUM),
               violations=[r for r in ds_sorted if r['d'] <= DELTA_NUM][:20],
               #  ★ 기술 보고 전용 — 게이트가 **아니다**
               descriptive={'d_median': sorted(r['d'] for r in ds)[len(ds) // 2],
                            'd_min_pct': worst['pct'],
                            'd_max_pct': ds_sorted[-1]['pct']},
               note=('평균·SD·범위는 기술 보고 전용이고 게이트가 아니다.  판정은 **최악 팔** '
                     '하나가 정한다 (prereg §2).'))
    return out


# ═══════════════════════════════════════════════════════════════════════════
def _mk(role, w, v, o, s, **kw):
    d = {'role': role, 'vox': v, 'origin': o, 'sigma_e': s}
    if role != 'secondary':
        d['vgcf_wt'] = w
    d.update(kw); d['_file'] = f'{role}_{w}_{v}_{o}.json'
    return d


def _qc(arms, w=1.0, v=0.15):
    """그 설계의 primary 와 **같은 값**인 QC 8팔 — 정상 음성대조."""
    sig = {(a['vgcf_wt'], a['vox'], a['origin']): a['sigma_e']
           for a in arms if a['role'] == 'primary'}
    return arms + [_mk('qc_replay', w, v, o, sig[(w, v, o)]) for o in range(PREREG['n_origin'])]


def _full(gain=0.05, **kw):
    """설계 전수 팔 — 조성이 오를수록 σ_e 가 `gain` 씩 오른다."""
    return [_mk('primary', w, v, o, 1e-2 * (1 + gain) ** i, **kw)
            for i, w in enumerate(PREREG['vgcf_wts'])
            for v in PREREG['voxes'] for o in range(PREREG['n_origin'])]


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    # ① 깨끗한 단조 = ORDER-ROBUST
    v = verdict(_qc(_full(0.05)))
    chk(f'① 단조 상승 → ORDER-ROBUST (측정 {v["order"]}, 비교 {v.get("n_comparisons")}회)',
        v['order'] == 'ORDER-ROBUST' and v['n_comparisons'] == 4 * 3 * 8 - 3 * 8)
    # ② 팔 **하나**만 역전시켜도 UNRESOLVED — 최악 팔이 판정을 정한다
    arms = _full(0.05)
    for a in arms:
        if a['role'] == 'primary' and a['vgcf_wt'] == 2.0 and a['vox'] == 0.15 and a['origin'] == 3:
            a['sigma_e'] = 1e-2 * 0.5          # 1→2 를 역전시킨다
    v2 = verdict(_qc(arms))
    chk(f'② 96팔 중 **하나**만 역전 → ORDER-UNRESOLVED (위반 {v2.get("n_violating")}건)',
        v2['order'] == 'ORDER-UNRESOLVED' and v2['n_violating'] >= 1)
    # ③ 설계 칸이 비면 **판정하지 않는다** (부분집합 = 조용한 초록)
    v3 = verdict([a for a in _full(0.05) if not (a['vox'] == 0.20 and a['origin'] == 5)])
    chk(f'③ 격자점 결손 → REFUSED (빠진 칸 {len(v3.get("missing_cells", []))}개 보고)',
        v3['order'] == 'REFUSED' and 'missing_cells' in v3)
    # ④ 미수렴이 하나라도 있으면 거부
    au = _full(0.05); au[0]['unconverged'] = True
    chk('④ 미수렴 팔 → REFUSED', verdict(au)['order'] == 'REFUSED')
    ac = _full(0.05); ac[7]['cg_info'] = 30000
    chk('④ cg_info ≠ 0 → REFUSED', verdict(ac)['order'] == 'REFUSED')
    # ⑤ replay 가 δ_num 을 넘으면 전체 HOLD (순서가 아무리 좋아도)
    ar = _qc(_full(0.05))
    for x in ar:                                   # QC 하나만 0.5 % 어긋나게
        if x['role'] == 'qc_replay' and x['origin'] == 0:
            x['sigma_e'] *= 1.005
    vr = verdict(ar)
    chk(f'⑤ replay 0.5 % > δ_num 0.04 % → HOLD (측정 {vr["order"]})', vr['order'] == 'HOLD')
    ar2 = _qc(_full(0.05))                                            # 쌍둥이와 바이트 동일
    chk('⑤ replay 동일 → 통과하고 순서 판정으로 간다',
        verdict(ar2)['order'] == 'ORDER-ROBUST' and verdict(ar2)['replay']['passes'])
    # ★ ⑤b Codex R9 P0-2 — QC 가 **셀당 하나**여도 발화해야 한다 (초판은 fail-open)
    bad_qc = _full(0.05) + [_mk('qc_replay', 1.0, 0.15, o, 9.9) for o in range(8)]
    vb = verdict(bad_qc)
    chk(f'⑤b QC 1개/셀 이고 값이 1000배 틀려도 잡는다 (초판은 ORDER-ROBUST 였다) — {vb["order"]}',
        vb['order'] == 'HOLD')
    ok_qc = _full(0.05) + [_mk('qc_replay', 1.0, 0.15, o, 1e-2) for o in range(8)]
    chk('⑤b QC 가 primary 쌍둥이와 같으면 통과한다',
        verdict(ok_qc)['order'] == 'ORDER-ROBUST')
    chk('⑤c QC 가 아예 없으면 거부 (음성대조 없이 판정하지 않는다)',
        verdict(_full(0.05))['order'] == 'HOLD')
    orph = _full(0.05) + [_mk('qc_replay', 9.0, 0.15, 0, 1e-2)]     # 없는 조성
    chk('⑤d 쌍둥이 없는 QC → 거부', verdict(orph)['order'] == 'HOLD')
    dupq = _full(0.05) + [_mk('qc_replay', 1.0, 0.15, 0, 1e-2)] * 2
    chk('⑤e 같은 셀 QC 중복 → 거부', verdict(dupq)['order'] == 'HOLD')

    # ⑥ Secondary(Lee) 는 판정에 관여하지 않는다
    a6 = (_full(0.05) + [_mk('secondary', None, 0.15, o, 1e-9) for o in range(8)]
          + [_mk('qc_replay', 1.0, 0.15, o, 1e-2) for o in range(8)])
    v6 = verdict(a6)
    chk('⑥ Lee 팔이 아무리 이상해도 ORDER-* 는 안 바뀐다',
        v6['order'] == 'ORDER-ROBUST' and v6['n_secondary'] == 8)
    # ⑦ 딱 문턱 위/아래 — 경계에서 방향이 맞나
    eps = DELTA_NUM_PCT / 100.0
    ax = [_mk('primary', w, v_, o, 1e-2 * (1 + eps * 0.5) ** i)     # δ 의 절반씩만 오름
          for i, w in enumerate(PREREG['vgcf_wts'])
          for v_ in PREREG['voxes'] for o in range(PREREG['n_origin'])]
    chk('⑦ 증분이 δ_num 의 절반이면 UNRESOLVED (문턱이 실제로 문다)',
        verdict(_qc(ax))['order'] == 'ORDER-UNRESOLVED')
    # ⑧ 빈 디렉터리는 거부 (빈 glob 로 조용히 통과하는 사고 방지)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        try:
            load_arms(td); raised = False
        except SystemExit:
            raised = True
    chk('⑧ 빈 디렉터리 → 거부 (빈 glob 가 초록이 되지 않는다)', raised)
    # ⑨ 필수 키가 없으면 거부
    with tempfile.TemporaryDirectory() as td:
        json.dump({'role': 'primary', 'vox': 0.15}, open(os.path.join(td, 'a.json'), 'w'))
        try:
            load_arms(td); raised = False
        except SystemExit:
            raised = True
    chk('⑨ 키 결손 → 거부', raised)
    # ⑩ δ_num 은 등록값에서 파생된다 (코드가 두 곳에서 어긋나지 않는지)
    chk(f'⑩ δ_num {DELTA_NUM_PCT} % ↔ log {DELTA_NUM:.6e} 일관',
        abs((math.exp(DELTA_NUM) - 1) * 100 - DELTA_NUM_PCT) < 1e-12)

    # ── ★★★ PA12-07 재현 (원장의 반례 그대로) ────────────────────────────────
    #  ⓐ QC 전수 — 정상 8개 중 **7개를 지우고 1개만 남겨도** 옛 판은 ORDER-ROBUST 였다.
    _q = _qc(_full(0.05))
    _one = [a for a in _q if a['role'] != 'qc_replay'] + \
           [a for a in _q if a['role'] == 'qc_replay'][:1]
    _v = verdict(_one)
    chk('★⑪ PA12-07 ⓐ QC 8 중 1 개만 있으면 거부 (옛 판은 ORDER-ROBUST)',
        _v['order'] == 'HOLD' and 'QC' in (_v.get('refused') or ''))
    chk('★⑪ 거부 사유가 "전수" 를 말한다',
        '8' in (_v.get('refused') or '') or '전수' in (_v.get('refused') or ''))
    #     음성 대조 — 8 개 다 있으면 통과해야 한다 (과잉차단 아님)
    chk('⑫ QC 8 개 전수면 통과 (과잉차단 음성대조)',
        verdict(_qc(_full(0.05)))['order'].startswith('ORDER'))

    #  ⓑ primary 중복 — 같은 칸을 두 번 넣으면 **파일명 순서가 결론을 골랐다**.
    #    coverage 는 집합이라 못 보고, order_stats 의 dict 는 **마지막 값**을 쓴다.
    def _dup(fname, sig):
        arms = _qc(_full(0.05))
        t = next(a for a in arms if a['role'] == 'primary'
                 and a['vgcf_wt'] == PREREG['vgcf_wts'][0]
                 and a['vox'] == PREREG['voxes'][0] and a['origin'] == 0)
        d = dict(t); d['sigma_e'] = sig; d['_file'] = fname
        return arms + [d]
    _lo = verdict(_dup('000_duplicate.json', 9.9e-2))
    _hi = verdict(_dup('zzz_duplicate.json', 9.9e-2))
    chk('★⑬ PA12-07 ⓑ primary 중복은 **이름과 무관하게** 거부',
        _lo['order'] == 'REFUSED' and _hi['order'] == 'REFUSED')
    #  ⚠⚠ 위 두 줄은 `verdict()` 에 **리스트를 직접** 넘기므로 파일명 정렬을 타지 않는다
    #    — 초판은 그래서 깨진 코드에서도 PASS 했다 (빈 시험).  실제 기전은 `load_arms` 가
    #    `*.json` 을 **파일명 순으로** 읽는 것이므로, 아래는 **진짜 파일**로 재현한다.
    def _verdict_from_files(dupname, dupsig):
        with tempfile.TemporaryDirectory() as td2:
            for a2 in _dup(dupname, dupsig):
                b = dict(a2)
                fn = b.pop('_file')
                json.dump(b, open(os.path.join(td2, fn), 'w'))
            return verdict(load_arms(td2))
    _f_lo = _verdict_from_files('000_duplicate.json', 9.9e-2)
    _f_hi = _verdict_from_files('zzz_duplicate.json', 9.9e-2)
    chk('★⑬ 실제 파일 경로에서도 두 이름의 판정이 같다 (옛 판은 000↔zzz 가 갈렸다)',
        _f_lo['order'] == _f_hi['order'] == 'REFUSED')
    chk('★⑬ 거부 사유가 중복을 말한다', '중복' in (_lo.get('refused') or ''))

    print(f'\nphase_a_order_verdict selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Phase A 조성-순서 판정 (사전등록 §2)')
    ap.add_argument('--dir', default='', help='팔 JSON 디렉터리')
    ap.add_argument('--out', default='')
    ap.add_argument('--what-if', type=float, default=None,
                    help='⚠ **진단 전용** — 다른 δ_num[%%] 에서 최악 팔이 어떻게 되나만 찍는다.  '
                         '판정은 하지 않는다 (등록 문턱은 상수다)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if not a.dir:
        ap.error('--dir 이 필요하다')

    arms = load_arms(a.dir)
    v = verdict(arms)
    print(f"팔 {len(arms)}  (primary {v['n_primary']} · secondary {v['n_secondary']} · QC {v['n_qc']})")
    print(f"δ_num = {DELTA_NUM_PCT} %  (사전등록 상수 — CLI 로 바꿀 수 없다)\n")
    if v['order'] in ('REFUSED', 'HOLD'):
        print(f"  ⛔ **{v['order']}** — {v['refused']}")
        for k in ('missing_cells', 'unconverged_files'):
            if k in v:
                print(f"     {k}: {v[k]}")
    else:
        w = v['worst_arm']
        print(f"  판정 **{v['order']}**")
        print(f"  비교 {v['n_comparisons']}쌍 · 위반 {v['n_violating']}건")
        print(f"  최악 팔: vox {w['vox']} · origin {w['origin']} · {w['pair'][0]}→{w['pair'][1]} wt% "
              f"→ {w['pct']:+.4f} %")
        d = v['descriptive']
        print(f"  (기술 보고 전용) 증분 최소 {d['d_min_pct']:+.4f} % · 최대 {d['d_max_pct']:+.4f} %")
        if v.get('replay', {}).get('passes') is not None:
            print(f"  replay 최악 {v['replay']['worst_pct']:.5f} % "
                  f"({'통과' if v['replay']['passes'] else '초과'})")
        if 'replay_note' in v:
            print(f"  {v['replay_note']}")
    if a.what_if is not None and 'worst_arm' in v:
        wa = math.log1p(a.what_if / 100.0)
        n = sum(1 for r in order_stats([x for x in arms if x['role'] == 'primary'])
                if r['d'] <= wa)
        print(f"\n  ⚠ [진단 전용] δ_num = {a.what_if} % 라면 위반 {n}건 — "
              f"**이것은 판정이 아니다** (등록 문턱은 {DELTA_NUM_PCT} %)")
    if a.out:
        from measure_provenance import provenance
        json.dump({**v, **provenance()}, open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')
