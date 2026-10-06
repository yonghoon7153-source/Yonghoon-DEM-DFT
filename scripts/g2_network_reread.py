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
  K7 가지 표 — 모드 × 가지: 숫자 있음 ⇔ 상태 computed · model_over_conduction (증서 가지 · 역할 = 자리) / 숫자 없음 ⇒ 상태 valid_zero · not_computed + 사유
  H1 인계 출처 관문 — `lhs_design_dataset.load_tau_results(…, expected_generation=기대 세대)` (P0–P4 · 도장 대조 · 배치 기대 세대 교차 대조) 통과 · 칸 = case_row
     launcher-root = 진짜 배치 기록 · smoke-root · case-dir = 그 폴더에서 만든 한 케이스 배치 기록 (⚠ P1 · P3 은 자기 대조가 된다 — 표지 synth_batch)
  M  (launcher-root) — manifest 기대 세대 선언 · 계획 큐 케이스 집합 = 배치 기록 케이스 집합 · done/partial 아닌 케이스 = FAIL (사유 그대로)

판정: rc 0 = 전부 PASS · 1 = FAIL 있음 · 2 = 사용 오류.  --json 이면 케이스마다 판정 · 상태표를 남긴다 (붙여 넣을 것 = 화면 요약).
⚠ 한계 — 도장 · 레코드 · 모든 사본 · 증서를 한 실행 안에서 일관되게 함께 바꾼 전면 위조는 재계산 없이 못 잡는다 (TAU_SAME_GEN_BASIS · Codex §3 의 "보증 아님" 그대로).
   이 도구의 PASS 는 게시 · 인계가 쓰는 계약을 **지금 파일에** 다시 부른 결과다 — 숫자의 물리적 정확성 · 실험 대조가 아니다.

사용 (WSL · 리포 루트)
  P=~/Yonghoon-DEM-DFT/venv/bin/python
  $P scripts/g2_network_reread.py --smoke-root ~/g2pre_smoke_<sha> --json ~/g2pre_smoke_<sha>/reread.json
  $P scripts/g2_network_reread.py --launcher-root ~/g2pre_pilot_<sha> --json ~/g2pre_pilot_<sha>/reread.json
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

SCHEMA = 'g2_network_reread/v1'
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


def synth_batch(cd, LWB, tmp: Path):
    """폴더 하나 → 한 케이스 배치 기록 (status.json · metrics_flat.csv) + results/<case> 링크 — smoke · case-dir 의 H1 용 (⚠ P1 · P3 자기 대조)."""
    cd = Path(cd).resolve()
    fm = _read_json(cd / 'full_metrics.json') or {}
    res = tmp / 'results'
    res.mkdir(parents=True, exist_ok=True)
    link = res / cd.name
    if not link.exists():
        os.symlink(cd, link)
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


def run_launcher(root: Path, *, out=print):
    """launcher-root — manifest 기대 세대 · 코호트별 진짜 배치 기록 · 케이스별 K1–K7 · 코호트별 H1."""
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
    reports = []
    for cs in (man.get('plan') or {}).get('cohorts') or []:
        name = cs.get('name')
        mdir = root / 'merged' / name
        planned = sorted(e['case'] for e in (man.get('plan') or {}).get('queue') or [] if e.get('cohort') == name)
        try:
            wv = LDD.load_webapp(mdir)
        except Exception as e:                                   # noqa: BLE001
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
    ap.add_argument('--json', default='', help='판정 JSON 을 쓸 곳')
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = _parse(argv)
    if a.selftest:
        return _selftest()
    meta, exp = [], a.expect_generation
    if a.smoke_root:
        sr = Path(a.smoke_root).expanduser().resolve()
        rep = _read_json(sr / 'smoke_report.json') or {}
        ids = [cid for cid, r in (rep.get('reports') or {}).items() if (r or {}).get('stop_after') == 'network']
        notdone = {cid: (rep['reports'][cid] or {}).get('status') for cid in ids if (rep['reports'][cid] or {}).get('status') != 'done'}
        meta.append(dict(name=f'S0 스모크 망 정지 케이스 전부 done ({len(ids)})', ok=bool(ids) and not notdone, detail=notdone or ids))
        folders = [sr / 'work' / 'results' / cid for cid in ids if cid not in notdone]
        reports = run_smoke_or_dirs(folders, exp)
    elif a.launcher_root:
        reports, meta, exp = run_launcher(Path(a.launcher_root).expanduser().resolve())
    elif a.case_dir:
        reports = run_smoke_or_dirs([Path(p).expanduser().resolve() for p in a.case_dir], exp)
    else:
        print('⛔ --smoke-root · --launcher-root · --case-dir · --selftest 중 하나', file=sys.stderr)
        return 2
    print(f'══ 세대 2 망 게시 다시 읽기 — 기대 세대 {exp!r} · 케이스 {len(reports)}')
    n_bad = summarize(reports, meta)
    print(f'  {"✓ 전부 통과" if not n_bad else f"✗ {n_bad} 건 실패"}')
    if a.json:
        p = Path(a.json).expanduser()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(dict(schema=SCHEMA, expected_generation=exp, meta=meta, cases=reports, n_fail=n_bad),
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
        #  launcher-root 모양 — manifest (기대 세대 선언 · 계획) + merged/lhs (진짜 배치 기록 모양) + results 링크
        for label, decl in (('declared', {'expected_network_generation': 'g2'}), ('undeclared', {})):
            lr = tmp / f'lroot_{label}'
            mres = lr / 'merged' / 'lhs' / 'results'
            mres.mkdir(parents=True)
            cases, rows, plan_q = {}, {}, []
            for bed in ('through', 'nonthrough'):
                c = f'lhs99_{bed}'
                shutil.copytree(tmp / f'case_{bed}', mres / c)
                fm = _read_json(mres / c / 'full_metrics.json') or {}
                cases[c] = dict(case=c, stop_after='network', status='done', failed_stages=[], network_run_id=fm.get('network_run_id'))
                rows[c] = dict({k: v for k, v in fm.items() if not isinstance(v, (dict, list))}, case=c)
                plan_q.append(dict(case=c, cohort='lhs'))
            LWB.write_outputs(lr / 'merged' / 'lhs', dict(schema=LWB.SCHEMA, stop_after='network', harvest_dir='', cohort='', runs=[], cases=cases), rows)
            (lr / 'manifest.json').write_text(json.dumps(dict(schema='network_parallel_launcher/v1', plan=dict(cohorts=[dict(name='lhs')], queue=plan_q),
                                                              **decl)), encoding='utf-8')
            reps, meta, exp = run_launcher(lr)
            okl = all(m_['ok'] for m_ in meta) and all(c['ok'] for r in reps for c in r['checks'])
            if label == 'declared':
                chk(f'launcher-root 양성 — manifest 선언 g2 · 두 케이스 K1–K7 · 코호트 H1 통과 (exp {exp!r})', okl and exp == 'g2' and len(reps) == 2,
                    [m_ for m_ in meta if not m_['ok']] + [c for r in reps for c in r['checks'] if not c['ok']])
            else:
                badm = {m_['name'][:2] for m_ in meta if not m_['ok']}
                chk(f'launcher-root 음성 — manifest 기대 세대 선언 없음 (194 v1.2 런처 모양) → M0 · H1 실패 {sorted(badm)}', {'M0', 'H1'} <= badm)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        for d in made:
            shutil.rmtree(d, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
