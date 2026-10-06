#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""세대 2 망 게시 다시 읽기 (읽기 전용) — Codex 세대 2 재검증 §7-4 · §7 끝 (`docs/reviews/codex_review_gen2_network_reverify_20261006.md`).

§7-4: *"real14 · case15 와 정상 비관통 사례를 새 러너에서 생산 → 후보 검사 → 게시 → 인계까지 통과시킨다.  raw 숫자만 비교하지 말고 게시된 증서 · 도장 ·
진단 상태 · 열 역할을 재독한다."*  §7 끝: *"194 완료 뒤 전체 상태 · ID · 증서와 값의 다시 읽기까지 끝나기 전에는 v1.3 의 최종 학습 인계 GO 로 표현하지 않는다."*
⇒ 게시가 끝난 폴더를 **그대로** 다시 읽어 아래를 판정한다 (아무 파일도 쓰지 않는다 · 계산 경로 없음 — 전부 생산 · 게시 · 인계가 쓰는 **같은 함수**를 부른다 · 규율 ①).

입력 (셋 중 하나):
  --smoke-root S     `scripts/wsl_network_smoke.py` ROOT — smoke_report.json 의 망 정지 (stop_after=network) 케이스 · 폴더 S/work/results/<id>
  --launcher-root R  `scripts/run_network_194_parallel.py` ROOT — manifest 의 기대 세대 (expected_network_generation · 없으면 FAIL) · merged/<코호트>
                     (진짜 배치 기록 status.json · metrics_flat.csv) · merged/<코호트>/results/<case>
                     ★ 10-07 G2RR2-02 — **등록 모드 필수**: --expect-set production194 (등록 ID 지문 194) | pilot3 (시범 세 케이스) · 또는 --expect-case 코호트:케이스
                     (여러 번).  계획 큐 (고칠 수 있는 manifest) 를 자기 자신의 유일한 기대 집합으로 쓰지 않는다.
  --case-dir D       케이스 폴더 하나 (여러 번)

케이스마다 (게시 = 배치 · 스모크 기록이 done 인 폴더):
  K1 게시 — full_metrics network_solver_status success · 도장 (network_provenance.json) valid · success · run id 셋 (도장 · full_metrics · active) 같음
  K2 세대 계약 + 증서 결합 — `tau_flux.network_generation_contract(dual)` → 기대 세대 · 문제 0.  세대 2 계약은 모드 셋 (H0 · H12 · physics) × 가지 셋
     (FULL · CF · 협착-only) 의 수치 증서 결합까지 본다 (가지 · 채널 · 역할 · 전극 · ΔV · 봉인된 기하 · 발행 σ_ratio · σ_dim 재구성 · G2RR-02)
  K3 도장 ↔ 레코드 — `pipeline_service.provenance_generation_problem(도장, dual, 세대)` = [] (네 세대 값 = 레코드에서 유도한 기대값 · G2RR-01)
  K4 망 정지 계약 다시 — `pipeline_service.network_stop_verdict(폴더, run id)` (게시 때 계약 ①–⑨ · legacy_ok False)
  K5 열 역할 — `tau_flux.case_row` 의 ion_net_generation = 기대 세대 · `tau_flux.row_generation_problems(행)` = (세대, []) (모드마다 협착 · ψ · 면적 규칙 ·
     전극 · bulk 칸 = 세대 2 표 — 주 hertz = H0 · hertz_h12 = H12 민감도 · physics)
  K6 관통 일치 — 생산자 FULL 상태 (세 모드) ↔ τ 상태: computed → OK 또는 등록된 과학적 HOLD (NOT_COMPUTED · NOT_PERCOLATING 아님) /
     valid_zero → NOT_PERCOLATING
  K7 가지 표 — ★ 10-07 G2RR2-05: 공용 계약의 결과 그대로 (`tau_flux.branch_table_problems` — 숫자 있음 ⇔ 게시 상태 / 숫자 없음 ⇒ 비게시 상태 + 사유 /
     상태 기록 결손 = 거부 · 별도 자격 없음 · 증서 가지 · 역할 결합은 K2)
  H1 인계 출처 관문 — `lhs_design_dataset.load_tau_results(…, expected_generation=기대 세대)` (P0–P4 · 도장 대조 · 배치 기대 세대 교차 대조) 통과 · 칸 = case_row
     launcher-root = 진짜 배치 기록 · smoke-root · case-dir = 그 폴더에서 만든 한 케이스 배치 기록 (⚠ P1 · P3 은 자기 대조가 된다 — 표지 synth_batch)
  M  (launcher-root) — M0 manifest 기대 세대 선언 · ★ G2RR2-02: M-plan 루프 **전** plan · cohorts · queue 꼴 (비지 않음 · 중복 · 코호트 소속 — 실행기
     `plan_problems`) · M-reg 계획 큐 = 등록 집합 · M1 계획 큐 = 배치 기록 · M2 done/partial 아닌 케이스 = FAIL · M3 루프 **밖** 읽은 고유 집합 = 등록 집합
     (기대 수 · 읽은 수 · 빠진 · 남는 — JSON expected_n · read_n · set_equal).  옛 판은 루프 안에서만 봐서 plan · cohorts 삭제 · 빈 cohorts = 0 케이스 PASS.

판정: rc 0 = 전부 PASS · 1 = FAIL 있음 · 2 = 사용 오류.  --json 이면 케이스마다 판정 · 상태표를 남긴다 (붙여 넣을 것 = 화면 요약).
  JSON 스키마 v2 (10-07) = 등록 집합 필드 (expected_set · expected_n · read_n · set_equal · missing · extra) — v1.3 생성기 (`lhs_release_build`) 는
  expected_set production194 · 기대 = 읽음 = 194 · 같음 True 인 기록만 받는다 (옛 v1 기록 · 일부 · pilot3 = 거부).
⚠ 한계 — 도장 · 레코드 · 모든 사본 · 증서를 한 실행 안에서 일관되게 함께 바꾼 전면 위조는 재계산 없이 못 잡는다 (TAU_SAME_GEN_BASIS · Codex §3 의 "보증 아님" 그대로).
   이 도구의 PASS 는 게시 · 인계가 쓰는 계약을 **지금 파일에** 다시 부른 결과다 — 숫자의 물리적 정확성 · 실험 대조가 아니다.

사용 (WSL · 리포 루트)
  P=~/Yonghoon-DEM-DFT/venv/bin/python
  $P scripts/g2_network_reread.py --smoke-root ~/g2pre_smoke_<sha> --json ~/g2pre_smoke_<sha>/reread.json
  $P scripts/g2_network_reread.py --launcher-root ~/g2pre_pilot_<sha> --expect-set pilot3 --json ~/g2pre_pilot_<sha>/reread.json
  $P scripts/g2_network_reread.py --launcher-root ~/net194_<sha> --expect-set production194 --json ~/net194_<sha>/reread.json
  $P scripts/g2_network_reread.py --selftest
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
for _p in (str(ROOT / 'scripts'), str(ROOT / 'webapp')):
    if _p not in sys.path:
        sys.path.insert(0, _p)

SCHEMA = 'g2_network_reread/v2'     # v2 (10-07 G2RR2-02) = 등록 집합 필드 (expected_set · expected_n · read_n · set_equal · missing · extra)
BRANCHES = (('full', 'sigma_full', 'sigma_full_status', 'sigma_full_reason', 'solve_certificate_full'),
            ('bulk_only', 'sigma_bulk_net', 'sigma_bulk_net_status', 'sigma_bulk_net_reason', 'solve_certificate_bulk_net'),
            ('constriction_only', 'sigma_constr_net', 'sigma_constr_net_status', 'sigma_constr_net_reason', 'solve_certificate_constr_net'))


def _read_json(p):
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def _mods():
    import pipeline_service as ps
    import tau_flux as tf
    import lhs_design_dataset as LDD
    import lhs_webapp_batch as LWB
    return ps, tf, LDD, LWB


def branch_table(tf, dual):
    """모드 × 가지 표 (읽기만) → {모드: {가지: dict(status, reason, value, cert_branch, cert_role, cert_reason)}}."""
    out = {}
    for m in tf.MODES:
        rec = tf.mode_record(dual, m)
        if rec is None:
            out[m] = None
            continue
        row = {}
        for b, qk, sk, rk, ck in BRANCHES:
            c = rec.get(ck) if isinstance(rec.get(ck), dict) else None
            row[b] = dict(status=rec.get(sk), reason=rec.get(rk), value=rec.get(qk),
                          cert=(None if c is None else dict(branch=c.get('branch'), role=c.get('role'), status=c.get('status'),
                                                            method=c.get('method'), reason=c.get('reason'))))
        out[m] = row
    return out


def _k7_problems(tf, dual):
    """K7 — 가지 표 = **공용 계약의 결과 그대로** (`tau_flux.branch_table_problems` — 세대 2 계약 · 정지 계약 ⑨ · 공용 기록 검사 · τ 소비자 · 인계 P4 가
    싣는 같은 결과: 숫자 있음 ⇔ 게시 상태 / 숫자 없음 ⇒ 비게시 상태 + 사유 / 상태 기록 결손 = 거부).  ★ 10-07 G2RR2-05 (Codex 세대 2 재검증 2 §6) — 옛 K7 은
    별도 자격 (숫자 없음 ↔ 상태 None) 을 더했고 공용 계약은 그 결손을 받았다 (진단 가지 다섯 키 삭제 = 게시 done · 인계 통과 · K7 만 거부).  증서 가지 ·
    역할 결합은 K2 (같은 계약의 증서 결합) 가 본다."""
    out = []
    for m in tf.MODES:
        rec = tf.mode_record(dual, m)
        if rec is not None:
            out += [f'{m}.{p}' for p in tf.branch_table_problems(m, rec)]
    return out


def reread_case(cd, expected, ps, tf):
    """케이스 폴더 하나 → dict(case, checks[{name, ok, detail}], generation, statuses, table, row_cells)."""
    cd = Path(cd)
    checks = []

    def ck(name, ok, detail=''):
        checks.append(dict(name=name, ok=bool(ok), detail=str(detail)[:900]))
    fm = _read_json(cd / 'full_metrics.json') or {}
    dual = _read_json(cd / 'network_conductivity_dual.json')
    prov = ps.read_network_provenance(str(cd)) or {}
    rid = fm.get('network_run_id')
    ck('K1 게시 — solver success · 도장 valid/success · run id (도장 = full_metrics = active)',
       fm.get('network_solver_status') == 'success' and prov.get('provenance_state') == 'valid' and prov.get('solver_status') == 'success'
       and isinstance(rid, str) and rid and prov.get('network_run_id') == rid == fm.get('active_network_run_id'),
       f"solver {fm.get('network_solver_status')!r} · 도장 {prov.get('provenance_state')!r}/{prov.get('solver_status')!r} · "
       f"run id {prov.get('network_run_id')!r} · {rid!r} · {fm.get('active_network_run_id')!r}")
    if not isinstance(dual, dict):
        ck('K2 세대 계약 + 증서 결합', False, 'network_conductivity_dual.json 없음 · 못 읽음')
        return dict(case=cd.name, folder=str(cd), checks=checks, generation=None)
    con = tf.network_generation_contract(dual)
    gen = con.get('generation')
    ck(f'K2 세대 계약 + 증서 결합 — 세대 {expected!r} · 문제 0 (모드 셋 × 가지 셋 증서 · G2R-01 · 02 · G2RR-02)',
       gen == expected and not con.get('problems'), f'세대 {gen!r} · {tf.generation_contract_text(con)[:700]}')
    sp = ps.provenance_generation_problem(prov, dual, gen)
    ck('K3 도장 ↔ 레코드 — 네 세대 값 = 레코드에서 유도한 기대값 (G2RR-01)', not sp,
       ' · '.join(sp) or {k: prov.get(k, 'ABSENT') for k in ps.PROVENANCE_GENERATION_KEYS})
    try:
        ok4, why4 = ps.network_stop_verdict(str(cd), rid)
    except Exception as e:                                       # noqa: BLE001 — 판정을 못 내면 통과로 치지 않는다
        ok4, why4 = False, f'{type(e).__name__}: {e}'
    ck('K4 망 정지 계약 다시 (①–⑨ · legacy_ok False)', ok4, why4)
    row = tf.case_row(str(cd))
    rg, rprob = tf.row_generation_problems(row)
    ck(f'K5 열 역할 — ion_net_generation {expected!r} · 행 세대 계약 문제 0 (모드별 협착 · ψ · 면적 · 전극 · bulk 칸)',
       row.get(tf.ROW_GENERATION_COL) == expected and rg == expected and not rprob,
       f'칸 {row.get(tf.ROW_GENERATION_COL)!r} · 행 판정 {rg!r} · {rprob[:3]}')
    statuses = {m: (row.get(f'ion_net_status_{m}'), row.get(f'ion_net_status_reason_{m}')) for m in tf.MODES}
    table = branch_table(tf, dual)
    bad6 = []
    for m in tf.MODES:
        st_full = ((table.get(m) or {}).get('full') or {}).get('status')
        s, r_ = statuses[m]
        if st_full == 'computed' and s in ('NOT_COMPUTED', 'NOT_PERCOLATING', None):
            bad6.append(f'{m}: 생산자 computed ↔ τ {s} ({r_})')
        elif st_full == 'valid_zero' and s != 'NOT_PERCOLATING':
            bad6.append(f'{m}: 생산자 valid_zero ↔ τ {s} ({r_})')
        elif st_full not in ('computed', 'valid_zero'):
            bad6.append(f'{m}: 생산자 FULL 상태 {st_full!r} (게시된 레코드에 있을 수 없는 상태)')
    ck('K6 관통 일치 — 생산자 FULL 상태 ↔ τ 상태 (세 모드)', not bad6, ' · '.join(bad6) or statuses)
    bad7 = _k7_problems(tf, dual)
    ck('K7 가지 표 — 공용 계약 (tau_flux.branch_table_problems) 그대로: 숫자 ⇔ 게시 상태 / 숫자 없음 ⇒ 비게시 상태 + 사유 / 상태 기록 결손 = 거부',
       not bad7, ' · '.join(bad7[:6]))
    return dict(case=cd.name, folder=str(cd), run_id=rid, checks=checks, generation=gen, statuses=statuses, table=table,
                stamp={k: prov.get(k, 'ABSENT') for k in ps.PROVENANCE_GENERATION_KEYS},
                sigma_ratio={m: ((table.get(m) or {}).get('full') or {}).get('value') for m in tf.MODES},
                row_cells={c: tf._cell(row.get(c)) for c in tf.column_names()})


def handover_gate(results_dir, wv, expected, LDD):
    """H1 — 인계 출처 관문 (P0–P4 · 도장 대조 · 배치 기대 세대) → (ok, 사유 · 케이스별 칸)."""
    try:
        tv = LDD.load_tau_results(results_dir, wv, expected_generation=expected)
    except Exception as e:                                       # noqa: BLE001 — FillRefusal · 예외 둘 다 실패
        return False, f'{type(e).__name__}: {e}', {}
    return True, f'{len(tv["cases"])} 케이스 · 기대 세대 {tv.get("expected_generation")!r} · 검사 {tv.get("same_generation_checks")}', \
        {c: r['cells'] for c, r in tv['cases'].items()}


def _link_dir(src, dst):
    """폴더 링크 — symlink · 안 되면 (Windows 권한 WinError 1314 등) 하드링크 사본 · 그것도 안 되면 사본.  읽기 전용 대조라 셋 다 같은 바이트를 본다
    (Codex 재검증 2 §11 — Windows 에서 symlink fixture 가 selftest 를 세웠다)."""
    try:
        os.symlink(src, dst)
        return 'symlink'
    except (OSError, NotImplementedError):
        pass
    try:
        shutil.copytree(src, dst, copy_function=os.link)
        return 'hardlink'
    except OSError:
        shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst)
    return 'copy'


def synth_batch(cd, LWB, tmp: Path):
    """폴더 하나 → 한 케이스 배치 기록 (status.json · metrics_flat.csv) + results/<case> 링크 — smoke · case-dir 의 H1 용 (⚠ P1 · P3 자기 대조)."""
    cd = Path(cd).resolve()
    fm = _read_json(cd / 'full_metrics.json') or {}
    res = tmp / 'results'
    res.mkdir(parents=True, exist_ok=True)
    link = res / cd.name
    if not link.exists():
        _link_dir(cd, link)
    st = dict(schema=LWB.SCHEMA, stop_after='network', harvest_dir='', cohort='', runs=[],
              cases={cd.name: dict(case=cd.name, stop_after='network', status='done', failed_stages=[], network_run_id=fm.get('network_run_id'))})
    rows = {cd.name: dict({k: v for k, v in fm.items() if not isinstance(v, (dict, list))}, case=cd.name)}
    LWB.write_outputs(tmp / 'batch', st, rows)
    return res, tmp / 'batch'


def _cells_match(rc, cells):
    return bool(cells) and rc == cells


def run_smoke_or_dirs(folders, expected, *, out=print):
    ps, tf, LDD, LWB = _mods()
    reports = []
    for cd in folders:
        rep = reread_case(cd, expected, ps, tf)
        tmp = Path(tempfile.mkdtemp(prefix='g2rr_'))
        try:
            res, bdir = synth_batch(cd, LWB, tmp)
            ok, why, cells = handover_gate(res, LDD.load_webapp(bdir), expected, LDD)
            same = _cells_match(rep.get('row_cells'), cells.get(Path(cd).resolve().name))
            rep['checks'].append(dict(name='H1 인계 출처 관문 (load_tau_results · 기대 세대 · 폴더에서 만든 한 케이스 배치 기록 = synth_batch · P1 · P3 자기 대조)',
                                      ok=ok and same, detail=(why if not ok else f'{why} · 칸 = case_row {same}')[:900]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        rep['batch'] = 'synth_batch'
        reports.append(rep)
    return reports


def _np():
    """194 실행기 모듈 (계획 꼴 · ID 지문 · 등록 집합 — 같은 함수 · 사본 금지)."""
    import run_network_194_parallel as NP
    return NP


def registered_expected(name):
    """★ 10-07 G2RR2-02 — 등록 집합 이름 → dict(name, pairs, source) (`run_network_194_parallel.registered_id_set` — production194 = 등록 ID 지문 ·
    pilot3 = 시범 세 케이스)."""
    return _np().registered_id_set(name)


def explicit_expected(specs):
    """'코호트:케이스' 목록 → 명시 등록 집합 (중복 · 꼴 오류 = ValueError)."""
    pairs = []
    for s in specs:
        coh, _, case = str(s).partition(':')
        if not coh or not case:
            raise ValueError(f'--expect-case {s!r} — 코호트:케이스 꼴이어야')
        pairs.append((case, coh))
    if len(set(pairs)) != len(pairs):
        raise ValueError(f'--expect-case 중복 {sorted({p for p in pairs if pairs.count(p) > 1})}')
    return dict(name='explicit', pairs=frozenset(pairs), source='CLI --expect-case')


def run_launcher(root: Path, *, expected=None, out=print):
    """launcher-root — manifest 기대 세대 · ★ 등록 집합 (G2RR2-02) · 코호트별 진짜 배치 기록 · 케이스별 K1–K7 · 코호트별 H1.
    ★ 10-07 G2RR2-02 (Codex 세대 2 재검증 2 §3) — 옛 판은 `cohorts or []` 루프 안에서만 M1 을 봐서 plan · cohorts 를 지우거나 비우면 0 케이스를 읽고 실패 0 =
    rc 0 이었다.  이제 ① 루프 **전에** manifest · plan · cohorts · queue 의 꼴 (비지 않음 · 중복 · 코호트 소속 — 실행기와 같은 `plan_problems`) ②
    계획 큐 = **등록 집합** (expected — 고칠 수 있는 큐를 자기 자신의 기대 집합으로 쓰지 않는다) ③ 루프 **밖에서** 실제로 읽은 고유 (케이스, 코호트)
    집합 = 등록 집합 (M3 · 기대 수 · 읽은 수 · 빠진 · 남는).  expected 가 없으면 FAIL (등록 모드 필수)."""
    ps, tf, LDD, LWB = _mods()
    man = _read_json(root / 'manifest.json')
    meta = []
    if not isinstance(man, dict):
        return [], [dict(name='M0 manifest', ok=False, detail=f'{root}/manifest.json 없음 · 못 읽음')], None
    try:
        exp = LDD.tau_manifest_expected_generation(man)
        meta.append(dict(name=f'M0 manifest 기대 세대 선언 ({LDD.TAU_MANIFEST_GENERATION_KEY})', ok=True, detail=exp))
    except Exception as e:                                       # noqa: BLE001
        exp = None
        meta.append(dict(name=f'M0 manifest 기대 세대 선언 ({LDD.TAU_MANIFEST_GENERATION_KEY})', ok=False, detail=f'{type(e).__name__}: {e}'))
    want = exp or tf.NET_GEN_G2                                  # 케이스 판정은 g2 로 계속 (정보) — H1 은 선언이 있어야 통과
    exp_pairs = frozenset((expected or {}).get('pairs') or ())
    exp_name = (expected or {}).get('name')
    if not exp_pairs:
        meta.append(dict(name='M-reg 등록 집합', ok=False, detail='등록 집합이 없다 (--expect-set · --expect-case) — 계획 큐를 자기 자신의 기대 집합으로 쓰지 않는다'))
    #  ① 루프 전 — 꼴 (실행기와 같은 함수)
    pp = _np().plan_problems(man.get('plan'))
    meta.append(dict(name='M-plan manifest plan · cohorts · queue 꼴 (비지 않음 · 중복 · 코호트 소속 — 루프 전)', ok=not pp, detail=' · '.join(pp)[:900]))
    reports = []
    read = set()
    if not pp:
        plan = man['plan']
        planned_pairs = frozenset((e['case'], e['cohort']) for e in plan['queue'])
        if exp_pairs:
            ec = {h for _c, h in exp_pairs}
            meta.append(dict(name=f'M-reg 계획 큐 = 등록 집합 {exp_name} ({len(exp_pairs)})', ok=planned_pairs == exp_pairs,
                             detail=(f'등록에만 {sorted(exp_pairs - planned_pairs)[:5]} · 계획에만 {sorted(planned_pairs - exp_pairs)[:5]} · '
                                     f'등록 밖 코호트 {sorted({c["name"] for c in plan["cohorts"]} - ec)}')))
        for cs in plan['cohorts']:
            name = cs['name']
            mdir = root / 'merged' / name
            planned = sorted(e['case'] for e in plan['queue'] if e['cohort'] == name)
            try:
                wv = LDD.load_webapp(mdir)
            except Exception as e:                               # noqa: BLE001
                meta.append(dict(name=f'M1 {name} 배치 기록', ok=False, detail=f'{type(e).__name__}: {e}'))
                continue
            st = wv.get('status') or {}
            meta.append(dict(name=f'M1 {name} 케이스 집합 — 계획 큐 = 배치 기록 ({len(planned)})', ok=sorted(st) == planned,
                             detail=f'계획에만 {sorted(set(planned) - set(st))[:5]} · 기록에만 {sorted(set(st) - set(planned))[:5]}'))
            notdone = {c: (r or {}).get('status') for c, r in st.items() if (r or {}).get('status') not in LDD.WA_OK_STATUS}
            meta.append(dict(name=f'M2 {name} 전 케이스 done · partial', ok=not notdone, detail=notdone))
            for c in sorted(st):
                if c in notdone:
                    continue
                rep = reread_case(mdir / 'results' / c, want, ps, tf)
                rep['cohort'] = name
                rep['batch'] = 'launcher'
                read.add((c, name))
                if (st[c] or {}).get('network_run_id') != rep.get('run_id'):
                    rep['checks'].append(dict(name='K1b 배치 기록 run id = 폴더 run id', ok=False,
                                              detail=f"{(st[c] or {}).get('network_run_id')!r} ≠ {rep.get('run_id')!r}"))
                reports.append(rep)
            if exp is None:
                meta.append(dict(name=f'H1 {name} 인계 출처 관문 (기대 세대 교차 대조)', ok=False, detail='manifest 에 기대 세대 선언이 없어 교차 대조를 못 한다'))
                continue
            ok, why, cells = handover_gate(mdir / 'results', wv, exp, LDD)
            bad = [r['case'] for r in reports if r.get('cohort') == name and not _cells_match(r.get('row_cells'), cells.get(r['case']))] if ok else []
            meta.append(dict(name=f'H1 {name} 인계 출처 관문 (load_tau_results · P0–P4 · manifest 기대 세대 {exp!r}) · 칸 = case_row', ok=ok and not bad,
                             detail=(why if not ok else f'{why} · 칸 다름 {bad[:5]}')[:900]))
    #  ③ 루프 밖 — 실제로 읽은 고유 집합 = 등록 집합 (0 케이스 · 일부 코호트만 읽은 성공을 막는다)
    meta.append(dict(name=f'M3 읽은 고유 (케이스, 코호트) = 등록 집합 {exp_name} — 기대 {len(exp_pairs)} · 읽음 {len(read)}',
                     ok=bool(exp_pairs) and read == exp_pairs,
                     detail=f'빠진 {sorted(exp_pairs - read)[:5]} · 남는 {sorted(read - exp_pairs)[:5]}',
                     expected_n=len(exp_pairs), read_n=len(read), set_equal=bool(exp_pairs) and read == exp_pairs,
                     missing=sorted(exp_pairs - read), extra=sorted(read - exp_pairs)))
    return reports, meta, exp


def summarize(reports, meta, *, out=print):
    n_bad = 0
    for m_ in meta:
        out(f'  {"✓" if m_["ok"] else "✗"} {m_["name"]}' + ('' if m_['ok'] else f'  — {m_["detail"]}'))
        n_bad += not m_['ok']
    for r in reports:
        bad = [c for c in r['checks'] if not c['ok']]
        n_bad += len(bad)
        st = r.get('statuses') or {}
        tb = r.get('table') or {}
        diag = {m: {b: ((tb.get(m) or {}).get(b) or {}).get('status') for b in ('bulk_only', 'constriction_only')} for m in tb if tb.get(m)}
        out(f'  {"✓" if not bad else "✗"} {r.get("cohort", "")} {r["case"]} — 세대 {r.get("generation")!r} · '
            f'τ {({m: v[0] for m, v in st.items()})} · σ_ratio {r.get("sigma_ratio")} · CF/협착 {diag}')
        for c in bad:
            out(f'      ✗ {c["name"]} — {c["detail"][:400]}')
    return n_bad


def _parse(argv=None):
    ap = argparse.ArgumentParser(description='세대 2 망 게시 다시 읽기 (읽기 전용 · Codex 세대 2 재검증 §7-4)')
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--smoke-root', default='', help='wsl_network_smoke.py ROOT (망 정지 케이스)')
    g.add_argument('--launcher-root', default='', help='run_network_194_parallel.py ROOT (manifest 기대 세대 · merged 배치 기록)')
    g.add_argument('--case-dir', action='append', default=[], help='케이스 폴더 (여러 번)')
    g.add_argument('--selftest', action='store_true', help='합성 침대 (실 생산자 CLI 게시) 로 양성 · 음성 대조')
    ap.add_argument('--expect-generation', default='g2', help='smoke-root · case-dir 의 기대 세대 (기본 g2 · launcher-root 는 manifest 선언)')
    ap.add_argument('--expect-set', default='', help='launcher-root 의 등록 집합 이름 (production194 · pilot3 — G2RR2-02 · 등록 모드 필수)')
    ap.add_argument('--expect-case', action='append', default=[],
                    help='launcher-root 의 명시 등록 집합 — 코호트:케이스 (여러 번 · --expect-set 대신)')
    ap.add_argument('--json', default='', help='판정 JSON 을 쓸 곳')
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = _parse(argv)
    if a.selftest:
        return _selftest()
    meta, exp = [], a.expect_generation
    expected = None
    if a.launcher_root:
        #  ★ 10-07 G2RR2-02 — 등록 모드 필수 (생산 194 · 시범의 정확한 ID) — 계획 큐를 자기 자신의 기대 집합으로 쓰지 않는다
        if bool(a.expect_set) == bool(a.expect_case):
            print('⛔ --launcher-root 는 등록 집합이 필요하다 — --expect-set (production194 · pilot3) 또는 --expect-case 코호트:케이스 (여러 번) 중 하나만',
                  file=sys.stderr)
            return 2
        try:
            expected = registered_expected(a.expect_set) if a.expect_set else explicit_expected(a.expect_case)
        except Exception as e:                                   # noqa: BLE001 — 등록 집합을 못 세우면 판정하지 않는다
            print(f'⛔ 등록 집합 — {type(e).__name__}: {e}', file=sys.stderr)
            return 2
    elif a.expect_set or a.expect_case:
        print('⛔ --expect-set · --expect-case 는 --launcher-root 에만', file=sys.stderr)
        return 2
    if a.smoke_root:
        sr = Path(a.smoke_root).expanduser().resolve()
        rep = _read_json(sr / 'smoke_report.json') or {}
        ids = [cid for cid, r in (rep.get('reports') or {}).items() if (r or {}).get('stop_after') == 'network']
        notdone = {cid: (rep['reports'][cid] or {}).get('status') for cid in ids if (rep['reports'][cid] or {}).get('status') != 'done'}
        meta.append(dict(name=f'S0 스모크 망 정지 케이스 전부 done ({len(ids)})', ok=bool(ids) and not notdone, detail=notdone or ids))
        folders = [sr / 'work' / 'results' / cid for cid in ids if cid not in notdone]
        reports = run_smoke_or_dirs(folders, exp)
    elif a.launcher_root:
        reports, meta, exp = run_launcher(Path(a.launcher_root).expanduser().resolve(), expected=expected)
    elif a.case_dir:
        reports = run_smoke_or_dirs([Path(p).expanduser().resolve() for p in a.case_dir], exp)
    else:
        print('⛔ --smoke-root · --launcher-root · --case-dir · --selftest 중 하나', file=sys.stderr)
        return 2
    m3 = next((m_ for m_ in meta if m_.get('name', '').startswith('M3')), {})
    print(f'══ 세대 2 망 게시 다시 읽기 — 기대 세대 {exp!r} · 케이스 {len(reports)}'
          + (f' · 등록 집합 {expected["name"]} 기대 {m3.get("expected_n")} · 읽음 {m3.get("read_n")} · 같음 {m3.get("set_equal")}' if expected else ''))
    n_bad = summarize(reports, meta)
    print(f'  {"✓ 전부 통과" if not n_bad else f"✗ {n_bad} 건 실패"}')
    if a.json:
        p = Path(a.json).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(dict(schema=SCHEMA, expected_generation=exp, meta=meta, cases=reports, n_fail=n_bad,
                                     expected_set=(expected or {}).get('name'), expected_source=(expected or {}).get('source'),
                                     expected_n=m3.get('expected_n'), read_n=m3.get('read_n'), set_equal=m3.get('set_equal'),
                                     missing=m3.get('missing'), extra=m3.get('extra')),
                                ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')
    return 0 if not n_bad else 1


# ─────────────────────────────── selftest (합성 침대 · 실 생산자 CLI 게시) ───────────────────────────────
def _selftest() -> int:
    """실 생산자 → 게시 (`test_gen2_publication_handover._publish` — 실 network CLI · 실 `_network_and_stage_e`) 로 만든 폴더를 다시 읽는다.
      양성: 관통 (through) · 정상 비관통 (nonthrough) · GEN2-01 (clamp — physics · H12 협착-only not_computed) · launcher-root 모양 (manifest 선언 g2)
      음성: 증서 자리 바꿔치기 (CF → FULL · 강제 폴더) → K2 · H1 · 도장 네 값 null → K3 · H1 · manifest 기대 세대 없음 → M0 · H1 · 기대 세대 inferred_legacy → H1"""
    fails = []

    def chk(name, ok, why=''):
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok or not why else f'  — {str(why)[:300]}'))
        if not ok:
            fails.append(name)
    sys.path.insert(0, str(ROOT / 'webapp'))
    import app                                                   # noqa: E402
    import test_gen2_publication_handover as PH                  # noqa: E402  (실 생산자 게시 · 강제 폴더 — 같은 도구)
    ps, tf, LDD, LWB = _mods()
    made, tmp = [], Path(tempfile.mkdtemp(prefix='g2rr_st_')).resolve()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            pub = {bed: PH._publish(app, 'baseline', bed=bed) for bed in ('through', 'nonthrough', 'clamp')}
        made += [v[0] for v in pub.values()]
        chk('게시 셋 done (실 생산자 CLI → 정지 계약 → 게시)', all(v[1] == 'done' for v in pub.values()), {k: (v[1], v[2]) for k, v in pub.items()})
        res = {}
        for bed, (d, _st, _f, _rid) in pub.items():
            dst = tmp / f'case_{bed}'
            shutil.copytree(d, dst)
            res[bed] = run_smoke_or_dirs([dst], 'g2')[0]
        okp = {bed: all(c['ok'] for c in r['checks']) for bed, r in res.items()}
        chk(f'양성 — 관통 · 비관통 · GEN2-01 폴더 K1–K7 · H1 전부 통과 {okp}', all(okp.values()),
            {b: [c for c in r['checks'] if not c['ok']][:2] for b, r in res.items()})
        st_nt = res['nonthrough']['statuses']
        chk('비관통 — τ 세 모드 NOT_PERCOLATING · 가지 셋 valid_zero (숫자 없음)',
            all(v[0] == 'NOT_PERCOLATING' for v in st_nt.values())
            and all(d['status'] == 'valid_zero' and d['value'] is None for m in res['nonthrough']['table'].values() if m for d in m.values()), st_nt)
        tc = res['clamp']['table']
        chk('GEN2-01 — physics · H12 협착-only = not_computed zero_resistance_requires_contraction · FULL · CF computed (숫자 · 증서)',
            all(tc[m]['constriction_only']['status'] == 'not_computed'
                and tc[m]['constriction_only']['reason'] == 'zero_resistance_requires_contraction' for m in ('physics', 'hertz_h12'))
            and all(tc[m][b]['status'] == 'computed' and (tc[m][b]['cert'] or {}).get('branch') == b for m in tc for b in ('full', 'bulk_only')),
            {m: {b: (d['status'], d['reason']) for b, d in r.items()} for m, r in tc.items()})
        base, rid = pub['through'][0], pub['through'][3]
        f_cf = PH._force(app, base, rid, 'full_cert_from_cf', tmp / 'forced_cf', stamp='keep')
        r_cf = run_smoke_or_dirs([f_cf], 'g2')[0]
        bad_cf = {c['name'][:2] for c in r_cf['checks'] if not c['ok']}
        chk(f'음성 — 증서 자리 바꿔치기 (CF → FULL · 네 사본 · 도장 그대로) → K2 · H1 실패 {sorted(bad_cf)}', {'K2', 'H1'} <= bad_cf)
        f_null = tmp / 'stamp_null'
        shutil.copytree(base, f_null)
        pv = json.loads((f_null / ps.PROVENANCE_FILE).read_text(encoding='utf-8'))
        pv.update({k: None for k in ps.PROVENANCE_GENERATION_KEYS})
        (f_null / ps.PROVENANCE_FILE).write_text(json.dumps(pv), encoding='utf-8')
        r_null = run_smoke_or_dirs([f_null], 'g2')[0]
        bad_null = {c['name'][:2] for c in r_null['checks'] if not c['ok']}
        chk(f'음성 — 도장 네 세대 값 null (Codex all_null) → K3 · H1 실패 {sorted(bad_null)}', {'K3', 'H1'} <= bad_null)
        r_leg = run_smoke_or_dirs([tmp / 'case_through'], 'inferred_legacy')[0]
        bad_leg = {c['name'][:2] for c in r_leg['checks'] if not c['ok']}
        chk(f'음성 — 기대 세대 inferred_legacy 로 g2 폴더를 읽으면 K2 · K5 · H1 실패 {sorted(bad_leg)}', {'K2', 'K5', 'H1'} <= bad_leg)
        #  launcher-root 모양 — manifest (기대 세대 선언 · 계획) + merged/<코호트> (진짜 배치 기록 모양) + results 링크 (link=True 면 같은 게시 폴더로 symlink)
        def _lroot(name, cohort_cases, decl=None, link=False):
            lr = tmp / f'lroot_{name}'
            plan_q, cohorts = [], []
            for coh, cl in cohort_cases.items():
                mres = lr / 'merged' / coh / 'results'
                mres.mkdir(parents=True)
                cases, rows = {}, {}
                for c, bed in cl:
                    if link:
                        _link_dir(tmp / f'case_{bed}', mres / c)
                    else:
                        shutil.copytree(tmp / f'case_{bed}', mres / c)
                    fm = _read_json(mres / c / 'full_metrics.json') or {}
                    cases[c] = dict(case=c, stop_after='network', status='done', failed_stages=[], network_run_id=fm.get('network_run_id'))
                    rows[c] = dict({k: v for k, v in fm.items() if not isinstance(v, (dict, list))}, case=c)
                    plan_q.append(dict(case=c, cohort=coh))
                LWB.write_outputs(lr / 'merged' / coh, dict(schema=LWB.SCHEMA, stop_after='network', harvest_dir='', cohort='', runs=[], cases=cases), rows)
                cohorts.append(dict(name=coh))
            man = dict(schema='network_parallel_launcher/v1', plan=dict(cohorts=cohorts, queue=plan_q),
                       **({'expected_network_generation': 'g2'} if decl is None else decl))
            (lr / 'manifest.json').write_text(json.dumps(man), encoding='utf-8')
            return lr, man

        def _run_l(lr, expected):
            """run_launcher(lr, expected=…) — ★ G2RR2-02 등록 모드.  옛 코드 (expected 인자 없음) 는 등록 없이 돈다 (반례가 옛 판에서 어떻게 통과하는지 본다)."""
            try:
                return run_launcher(lr, expected=expected)
            except TypeError:
                return run_launcher(lr)

        def _ok_all(reps, meta):
            return all(m_['ok'] for m_ in meta) and all(c['ok'] for r in reps for c in r['checks'])
        _rid = getattr(sys.modules.get(__name__), 'registered_expected', None)
        two = {'lhs': [('lhs99_through', 'through'), ('lhs99_nonthrough', 'nonthrough')]}
        exp_two = dict(name='explicit', pairs=frozenset({('lhs99_through', 'lhs'), ('lhs99_nonthrough', 'lhs')}), source='selftest')
        for label, decl in (('declared', None), ('undeclared', {})):
            lr, _m = _lroot(label, two, decl)
            reps, meta, exp = _run_l(lr, exp_two)
            okl = _ok_all(reps, meta)
            if label == 'declared':
                chk(f'launcher-root 양성 — manifest 선언 g2 · 두 케이스 K1–K7 · 코호트 H1 통과 (exp {exp!r})', okl and exp == 'g2' and len(reps) == 2,
                    [m_ for m_ in meta if not m_['ok']] + [c for r in reps for c in r['checks'] if not c['ok']])
            else:
                badm = {m_['name'][:2] for m_ in meta if not m_['ok']}
                chk(f'launcher-root 음성 — manifest 기대 세대 선언 없음 (194 v1.2 런처 모양) → M0 · H1 실패 {sorted(badm)}', {'M0', 'H1'} <= badm)

        #  ★ 10-07 G2RR2-02 (Codex 세대 2 재검증 2 §3) — 0 케이스 PASS · 등록 집합 · 루프 전 꼴 검사 · 루프 밖 집합 대조 (반례 먼저)
        p3 = {'lhs': [('lhs00_055', 'through'), ('lhs00_128', 'nonthrough')], 'lhsx': [('lhsx_007', 'clamp')]}
        try:
            exp_p3 = _rid('pilot3') if _rid else None
        except Exception as e:                                   # noqa: BLE001
            exp_p3 = None
            print(f'  (등록 집합 pilot3 못 읽음: {type(e).__name__}: {e})')
        lr_p3, m_p3 = _lroot('pilot3', p3)
        reps, meta, exp = _run_l(lr_p3, exp_p3)
        m3 = next((m_ for m_ in meta if m_['name'].startswith('M3')), {})
        chk(f'★ 등록 집합 양성 pilot3 (lhs00_055 · lhs00_128 · lhsx_007) — 두 코호트 · 세 케이스 K1–K7 · H1 통과 · 기대 3 = 읽음 3 (M3 집합 대조) {m3.get("detail", "")[:160]}',
            exp_p3 is not None and _ok_all(reps, meta) and len(reps) == 3 and m3.get('ok') is True and '3' in m3.get('name', ''),
            [m_ for m_ in meta if not m_['ok']][:3])
        bad = {}
        for nm, ed in (('plan 삭제', lambda m_: m_.pop('plan')),
                       ('cohorts=[] (queue 유지)', lambda m_: m_['plan'].update(cohorts=[])),
                       ('cohorts 삭제 (queue 유지)', lambda m_: m_['plan'].pop('cohorts')),
                       ('queue 삭제', lambda m_: m_['plan'].pop('queue')),
                       ('코호트 하나 누락 (lhsx · 그 큐 항목도)', lambda m_: m_['plan'].update(cohorts=[c_ for c_ in m_['plan']['cohorts'] if c_['name'] != 'lhsx'],
                                                                                  queue=[e_ for e_ in m_['plan']['queue'] if e_['cohort'] != 'lhsx'])),
                       ('중복 ID', lambda m_: m_['plan']['queue'].append(dict(m_['plan']['queue'][0]))),
                       ('등록 밖 코호트 (lhsz · 케이스 하나)', lambda m_: (m_['plan']['cohorts'].append(dict(name='lhsz')),
                                                                   m_['plan']['queue'].append(dict(case='lhsz_000', cohort='lhsz')))),
                       ('등록 밖 케이스 (lhs00_999 · 큐에만)', lambda m_: m_['plan']['queue'].append(dict(case='lhs00_999', cohort='lhs')))):
            m2 = json.loads(json.dumps(m_p3))
            ed(m2)
            (lr_p3 / 'manifest.json').write_text(json.dumps(m2), encoding='utf-8')
            reps, meta, exp = _run_l(lr_p3, exp_p3)
            nf = summarize(reps, meta, out=lambda *a, **k: None)
            if nf == 0:
                bad[nm] = (len(reps), [m_['name'][:30] for m_ in meta])
        (lr_p3 / 'manifest.json').write_text(json.dumps(m_p3), encoding='utf-8')
        chk(f'★ G2RR2-02 반례 — plan 삭제 · cohorts=[] · cohorts 삭제 · queue 삭제 · 코호트 하나 누락 · 중복 ID · 등록 밖 코호트 · 등록 밖 케이스 → 전부 FAIL '
            f'(옛: plan · cohorts 셋 · 누락 = 0 케이스 · n_fail 0 · rc 0) {bad or ""}', not bad, repr(bad))
        def _main_rc(argv):
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    return main(argv)
            except SystemExit as e:                              # argparse 거부 (옛 코드에 없는 인자) 도 rc 로
                return e.code if isinstance(e.code, int) else 2
        rc_u = _main_rc(['--launcher-root', str(lr_p3)])
        chk('★ launcher-root 는 등록 모드가 필수 — --expect-set · --expect-case 없이 부르면 사용 오류 rc 2 (mutable 큐를 자기 기대 집합으로 쓰지 않는다)', rc_u == 2, rc_u)
        jp = tmp / 'p3.json'
        rc_j = _main_rc(['--launcher-root', str(lr_p3), '--expect-set', 'pilot3', '--json', str(jp)])
        jj = _read_json(jp) or {}
        chk('★ 판정 JSON 이 기대 수 · 읽은 수 · 집합 대조를 싣는다 (n_fail 만이 아니다) — 기대 3 · 읽음 3 · 같음 · CLI rc 0',
            rc_j == 0 and jj.get('expected_n') == 3 and jj.get('read_n') == 3 and jj.get('set_equal') is True and jj.get('expected_set') == 'pilot3',
            {k: jj.get(k) for k in ('expected_n', 'read_n', 'set_equal', 'expected_set', 'n_fail')})
        #  폴더 링크 — symlink 가 막힌 환경 (Windows WinError 1314 · Codex 재검증 2 §11) 에서도 fixture 가 선다 (하드링크 · 사본)
        _sym = os.symlink

        def _deny(*a, **k):
            raise OSError(1314, '권한 없음 (selftest 흉내)')
        os.symlink = _deny
        try:
            kind_ = _link_dir(tmp / 'case_through', tmp / 'link_fallback')
        finally:
            os.symlink = _sym
        r_lf = run_smoke_or_dirs([tmp / 'link_fallback'], 'g2')[0]
        chk(f'symlink 거부 환경 — 폴더 링크가 {kind_} 로 대체되고 그 폴더가 K1–K7 · H1 통과',
            kind_ in ('hardlink', 'copy') and all(c['ok'] for c in r_lf['checks']), [c for c in r_lf['checks'] if not c['ok']][:2])
        #  생산 194 (합성) — 등록 지문의 194 ID (커밋된 수확 폴더) · 두 코호트 · 케이스 폴더 = 같은 게시 폴더 링크 (K1–K7 · H1 은 폴더마다)
        try:
            exp_194 = _rid('production194') if _rid else None
        except Exception as e:                                   # noqa: BLE001
            exp_194 = None
            print(f'  (등록 집합 production194 못 읽음: {type(e).__name__}: {e})')
        if exp_194 is not None:
            p194 = {}
            for c, h in sorted(exp_194['pairs']):
                p194.setdefault(h, []).append((c, 'through'))
            lr_194, _m194 = _lroot('prod194', p194, link=True)
            reps, meta, exp = _run_l(lr_194, exp_194)
            m3 = next((m_ for m_ in meta if m_['name'].startswith('M3')), {})
            chk('★ 등록 집합 양성 production194 (합성 — 등록 ID 지문 194 · lhs 130 · lhsx 64) — 194 케이스 K1–K7 · 코호트 H1 둘 통과 · M3 기대 194 = 읽음 194',
                _ok_all(reps, meta) and len(reps) == 194 and m3.get('ok') is True, [m_ for m_ in meta if not m_['ok']][:3])
        else:
            chk('★ 등록 집합 양성 production194 (등록 집합 함수 없음 — 옛 코드)', False)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        for d in made:
            shutil.rmtree(d, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
