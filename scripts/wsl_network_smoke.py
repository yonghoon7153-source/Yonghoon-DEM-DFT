#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WSL 소형 통합 시험 — 실제 웹앱 파이프라인 · 격리 출력 (Codex RGLR 3차 재검증 10-05 *"격리된 WSL 소형 통합시험 착수 조건부 GO"*).

⛔ 공식 결과 · 인계 · 봉인이 아니다 — 새 ROOT (비어 있지 않으면 거부) 안에만 쓴다 (WEBAPP_*_FOLDER · TMPDIR · cwd 전부 ROOT 안 ·
   원격 저장소 끔 · 그림 · 자동 DB 끔).  리포의 추적 파일을 건드리지 않는다 (피복 단계의 실행 위치 상대 쓰기 LHS-27 도 ROOT 안으로).

케이스 (각각 **자식 프로세스** — 케이스마다 경과 · 최대 RSS (os.wait4) · user/sys 를 잰다 · 194 실행기와 같은 단일 스레드 env):
  A  real_14 (리포 `docs/data/real14_reference_20260928/` — atom · contact .gz · 메시 · 덱 · sha256 = README 표)
       a) 일반 경로 + **실제 Stage E** (figures · auto_db 끔)      b) `stop_after='network'`
     case15 (리포 `docs/data/case15_corner_20261001/` — 같은 꼴 · ★ 10-07 Codex 세대 2 재검증 §7-4) — `stop_after='network'` (`--skip-case15`)
     ⇒ 게시된 증서 · 도장 · 진단 상태 · 열 역할 · 인계 출처 관문의 다시 읽기 = `scripts/g2_network_reread.py --smoke-root <ROOT>` (이 도구는 게시까지)
  B  LHS 코호트 (원자료 = 코호트 TSV 경로 · 같은 프레임 관문 = `lhs_webapp_batch.stage_case` · `resolve_mode` 그대로) — `stop_after='network'`
       기본 고르기 (커밋된 인계표 · 수확 JSON 에서 · 접촉 수 가장 작은 것): 관통 bimodal (lhs) · 비관통 (lhs) · lhsx 한 건
  C  음성 대조 (합성 침대 · 실 network CLI 같은 프로세스 · `webapp/test_pipeline_provenance` 의 도구 · Codex 탐침과 같은 주입) —
       **기대 = 다른 에이전트의 수정 (RGLR2-01 · 02 · 03) 뒤 동작**.  지금 코드에서는 FAIL 이 정상이다 (수정 전 기준선).
       C1 일반 경로 σ_ratio ×4 → failed (+ 양성 대조: 변조 없는 일반 경로 = done)    C1b 일반 경로 L1 + σ_ratio None → failed
       C2 게시 중 I/O 실패 둘 (성공 시도 쓰기 · full_metrics 되돌림) → '되돌림 실패' 상태 (이전 세대 보존 주장 금지) (+ 양성 대조: 한 번 실패 = 이전 세대 그대로)
       C3 거의 정수압 VM 쌍 (순수 함수) → CV 0 (`--vm-expect null` 이면 계산 안 함 = null)

판정 — 케이스 · 대조마다 PASS/FAIL (데이터로).  `smoke_report.json` 하나 + `smoke_summary.txt` 짧은 요약.
  rc 0 = 전부 PASS · 1 = 실데이터 (A · B) 검사 FAIL 있음 · 2 = C (음성 대조) 만 FAIL (수정 전 코드에서 기대되는 결과) · 3 = 사용 오류

사용 (WSL · 리포 루트 · 같은 python)
  P=~/Yonghoon-DEM-DFT/venv/bin/python
  $P scripts/wsl_network_smoke.py --root ~/net_smoke_$(git rev-parse --short HEAD)_$(date +%H%M)
  $P scripts/wsl_network_smoke.py --root … --lhs-case lhs00_055 --lhs-case lhs00_128      # 고르기 바꾸기
  $P scripts/wsl_network_smoke.py --root … --skip-real14-general                        # Stage E 일반 경로 빼기 (빠르게)
  $P scripts/wsl_network_smoke.py --selftest                                             # 이 컨테이너 — 합성 침대 · 실제 파이프라인
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import csv
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'webapp')]

REAL14 = ROOT / 'docs' / 'data' / 'real14_reference_20260928'
REAL14_POROSITY_REF = 15.639            # case_master 106 행 ε_sphere (README 표 · 이 세션 컨테이너 실측 15.639124908717994)
CASE15 = ROOT / 'docs' / 'data' / 'case15_corner_20261001'
#: ★ 10-07 (Codex 세대 2 재검증 §7-4 — real14 · case15 · 정상 비관통을 생산 → 후보 검사 → 게시 → 인계까지) — 커밋된 참조 침대 둘.
#:   (원본 이름 · 업로드 폴더에 둘 이름 · README sha256 표의 이름) — 덤프 둘은 .gz 를 풀어 둔다 (sha256 = 압축 푼 바이트 · README 표).
#:   case15 의 `v4_` 는 첨부 때 붙은 이름 (README) — 업로드 폴더에는 덱의 덤프 이름 꼴 (atom_<step>) 로 둔다 (바이트 그대로 · sha 대조는 README 이름으로).
REFBEDS = {
    'real14': dict(dir=REAL14, deck='input_real_14.liggghts', atom='atom_2060000.liggghts',
                   files=(('atom_2060000.liggghts.gz', 'atom_2060000.liggghts', 'atom_2060000.liggghts'),
                          ('contact_2060000.liggghts.gz', 'contact_2060000.liggghts', 'contact_2060000.liggghts'),
                          ('mesh_2060000.stl', 'mesh_2060000.stl', 'mesh_2060000.stl'),
                          ('input_real_14.liggghts', 'input_real_14.liggghts', 'input_real_14.liggghts'))),
    'case15': dict(dir=CASE15, deck='input_case15.liggghts', atom='atom_1710000.liggghts',
                   files=(('atom_v4_1710000.liggghts.gz', 'atom_1710000.liggghts', 'atom_v4_1710000.liggghts'),
                          ('contact_v4_1710000.liggghts.gz', 'contact_1710000.liggghts', 'contact_v4_1710000.liggghts'),
                          ('mesh_v4_1710000.stl', 'mesh_1710000.stl', 'mesh_v4_1710000.stl'),
                          ('input_case15.liggghts', 'input_case15.liggghts', 'input_case15.liggghts'))),
}


def refbed_sha_table(folder):
    """README 의 sha256 표 (원자료 바이트 · 압축 푼 atom · contact 포함) → {파일 이름: sha256} — 사본을 두지 않고 정본에서 읽는다."""
    import re
    out = {}
    for ln in (Path(folder) / 'README.md').read_text(encoding='utf-8').splitlines():
        m = re.match(r'^([0-9a-f]{64})\s+[\d,]+ B\s+(\S+)', ln)
        if m:
            out[m.group(2)] = m.group(1)
    return out


def real14_sha_table():
    return refbed_sha_table(REAL14)
THREAD_ENV = {'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1',
              'NUMEXPR_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1'}
KEEP = ('done', 'partial')


def now_iso():
    return time.strftime('%Y-%m-%dT%H:%M:%S')


def read_json(p):
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return None


def write_json(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')


def sha256_bytes_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ─────────────────────────────── 고르기 (B) ───────────────────────────────
def pick_lhs_cases():
    """커밋된 인계표 (percolation_pct) · 수확 JSON (contact_scan.n_rows_last · n_types) 에서 접촉 수 가장 작은 관통 bimodal (lhs) ·
    비관통 (lhs) · lhsx 한 건.  → [(case, cohort, 기대 관통 bool)]"""
    import run_network_194_parallel as NP
    out = []
    for fam, csvp in (('lhs', 'docs/data/lhs_handover_20261001.csv'), ('lhsx', 'docs/data/lhsx_handover_20261001.csv')):
        hd = ROOT / NP.COHORT_SPECS[fam]['harvest']
        items = []
        with open(ROOT / csvp, encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                h = read_json(hd / f"{r['case_id']}.json") or {}
                items.append(((h.get('contact_scan') or {}).get('n_rows_last') or 10 ** 9, r['case_id'], int(h.get('n_types') or 0),
                              float(r['percolation_pct'] or 0)))
        items.sort()
        if fam == 'lhs':
            out.append(next((c, fam, True) for k, c, nt, pp in items if pp > 0 and nt == 3))
            out.append(next((c, fam, False) for k, c, nt, pp in items if pp == 0))
        else:
            out.append(next((c, fam, pp > 0) for k, c, nt, pp in items))
    return out


def lhs_expected_perc(case):
    for fam in ('lhs', 'lhsx'):
        with open(ROOT / f'docs/data/{fam}_handover_20261001.csv', encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                if r['case_id'] == case:
                    return fam, float(r['percolation_pct'] or 0) > 0
    return None, None


# ─────────────────────────────── 자식: 한 케이스 ───────────────────────────────
def _setup_child_env(root: Path):
    for k, d in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                 ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
        os.environ[k] = str(root / 'work' / d)
        Path(os.environ[k]).mkdir(parents=True, exist_ok=True)
    os.environ['SUPABASE_URL'] = ''
    os.environ['SUPABASE_KEY'] = ''
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    tempfile.tempdir = None


def collect(app, ps, tf, cid, out, pipeline_s):
    rd = Path(app.get_results_dir(cid))
    fm = read_json(rd / 'full_metrics.json') or {}
    dual = read_json(rd / 'network_conductivity_dual.json') or {}
    modes = {m: {k: (dual.get(m) or {}).get(k) for k in ('sigma_full', 'sigma_full_mScm', 'sigma_full_status', 'sigma_full_reason',
                                                          'boundary_rule', 'percolating_fraction', 'phi_se')}
             for m in ('hertzian', 'physics')}
    stages = [dict(step=s.get('step'), rc=s.get('rc'), ok=s.get('ok'), required=s.get('required'),
                   err=(str(s.get('stderr') or '')[-300:] if s.get('ok') is False or (s.get('rc') not in (0, None)) else ''))
              for s in (out.get('log') or []) if isinstance(s, dict)]
    try:
        tau = tf.case_row(str(rd))
    except Exception as e:                                  # noqa: BLE001
        tau = dict(error=f'{type(e).__name__}: {e}')
    missing = list(ps.stage_e_missing_keys(fm)) if fm else ['(full_metrics 없음)']
    keys = ('sigma_full_mScm', 'sigma_full_mScm_physics', 'electronic_sigma_full_mScm', 'electronic_sigma_full_mScm_physics',
            'thermal_sigma_full_mScm', 'thermal_sigma_full_mScm_physics', 'network_run_id', 'active_network_run_id',
            'network_solver_status', 'stage_e_parent_network_run_id', 'porosity', 'percolation_pct', 'stress_cv',
            'constriction_power_share_ion_hertz', 'constriction_power_share_ion_physics', 'sigma_full_mScm_stage_e',
            'sigma_full_status', 'sigma_full_status_physics')
    return dict(cid=cid, status=out.get('status'), success=out.get('success'), failed_stages=out.get('failed_stages'),
                returned_network_run_id=out.get('network_run_id'), pipeline_s=round(pipeline_s, 2), stages=stages,
                fm={k: fm.get(k) for k in keys}, stage_e_ran=(not missing), stage_e_missing=missing[:5],
                provenance=ps.read_network_provenance(str(rd)), attempt=ps.read_network_attempt(str(rd)),
                status_view=ps.network_status_view(str(rd)), dual=modes,
                tau={k: v for k, v in tau.items() if k.startswith(('ion_net_status', 'f_ion_', 'tau2_ion_', 'tau_ion_', 'error', 'case'))},
                collector='해당 없음 — 웹앱 망 경로에는 STEP3 집전체 (collector) 가 없다 (계획/미계획 = mpm_webapp_payload 생산자 · 이 시험 밖)')


def stage_refbed(kind, cd: Path) -> dict:
    """참조 침대 (REFBEDS) 를 업로드 폴더 cd 에 둔다 → dict(raw_sha_ok, raw_sha, type_map, type_map_errors).
    덤프 둘은 .gz 를 풀고 · README sha256 표 (압축 푼 바이트) 와 대조 · 덱이 선언한 상 매핑 (type_map_resolve — 배치와 같은 함수)."""
    bed = REFBEDS[kind]
    for src, dst, _key in bed['files']:
        if src.endswith('.gz'):
            with gzip.open(bed['dir'] / src, 'rb') as fi, open(cd / dst, 'wb') as fo:
                shutil.copyfileobj(fi, fo)
        else:
            shutil.copy2(bed['dir'] / src, cd / dst)
    sha = {key: sha256_bytes_file(cd / dst) for _src, dst, key in bed['files']}
    want = refbed_sha_table(bed['dir'])
    import type_map_resolve as TMR
    m, _notes, errs = TMR.resolve_from_files(str(cd / bed['deck']), str(cd / bed['atom']))
    #  README 표의 네 파일 (덱 · 메시 · 압축 푼 덤프 둘) 이 전부 표에 있고 같아야 한다 (case15 표의 첨부 zip 줄은 업로드에 없다 — 대조 밖)
    return dict(raw_sha_ok=all(want.get(key) and sha.get(key) == want.get(key) for _src, _dst, key in bed['files']),
                raw_sha={key: (sha.get(key, '')[:12], want.get(key, '')[:12]) for _src, _dst, key in bed['files']},
                type_map=TMR.format_map(m), type_map_errors=errs)


def child_case(spec: dict) -> dict:
    root = Path(spec['root'])
    _setup_child_env(root)
    import app                                             # noqa: E402 — env 뒤
    import pipeline_service as ps
    import tau_flux as tf
    cid, kind, stop = spec['id'], spec['kind'], spec.get('stop')
    cd = Path(os.environ['WEBAPP_UPLOAD_FOLDER']) / cid
    if cd.exists():
        shutil.rmtree(cd)
    cd.mkdir(parents=True)
    rep = dict(id=cid, kind=kind, stop_after=stop)
    if kind in REFBEDS:
        rep.update(stage_refbed(kind, cd))
        rep['mode'] = app.detect_mode(str(cd))
    elif kind == 'lhs':
        import lhs_harvest_batch as HB
        import lhs_webapp_batch as LWB
        import type_map_resolve as TMR
        cohort = {r['case']: r for r in HB.read_cohort(Path(spec['cohort']))}
        hj = read_json(Path(spec['harvest_dir']) / f'{cid}.json') or {}
        try:
            st = LWB.stage_case(cid, cohort[cid], hj, Path(os.environ['WEBAPP_UPLOAD_FOLDER']), spec.get('root_from', ''),
                                spec.get('root_to', ''))
            mode, tm, fold, absent = LWB.resolve_mode(st['case_dir'], st['names'], hj, app, TMR)
        except (LWB.Refuse, KeyError) as e:
            rep.update(status='REFUSED', why=f'{type(e).__name__}: {e}')
            return rep
        rep.update(type_map=tm, mode=mode, type_map_fold=fold, type_map_absent=absent, same_frame='ok',
                   sha={k: v[:12] for k, v in st['sha'].items()}, contact_scan=st['contact_scan'])
    elif kind == 'synthetic':                               # --selftest 전용 — 합성 침대 (CSV 입력)
        import test_pipeline_provenance as TP
        TP._write_bed(str(cd), spec['bed'])
        tm, mode = spec['type_map'], 'standard'
        rd0 = Path(app.get_results_dir(cid))
        rd0.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cd / 'input_params.json', rd0 / 'input_params.json')
        rep.update(type_map=tm, mode=mode)
    else:
        raise ValueError(kind)
    (cd / 'meta.json').write_text(json.dumps(dict(name=cid, created='', mode=rep['mode'], type_map=rep['type_map'],
                                                  type_map_resolved=rep['type_map'], scale=spec.get('scale', 1000),
                                                  files=sorted(os.listdir(cd)), status='uploaded'), ensure_ascii=False),
                                  encoding='utf-8')
    t = time.monotonic()
    kw = dict(figures=False, auto_db=False)
    if stop:
        kw['stop_after'] = stop
    out = app.run_pipeline(cid, rep['mode'], rep['type_map'], spec.get('scale', 1000), **kw)
    rep.update(collect(app, ps, tf, cid, out, time.monotonic() - t))
    return rep


# ─────────────────────────────── 자식: 음성 대조 (C) ───────────────────────────────
def _hashes(d: Path, TP, ps):
    return {n: hashlib.sha256((d / n).read_bytes()).hexdigest() for n in (*TP._NET_FOUR, ps.PROVENANCE_FILE, 'full_metrics.json')
            if (d / n).is_file()}


def control_probe(base: Path, name, *, edit=None, bed='through', stop=True, break_solver=False, repeat=False, crash=None):
    """Codex 탐침 (`network_adversarial.py`) 과 같은 꼴 — 실 network CLI (같은 프로세스) → 실 `_network_and_stage_e` (Stage E 대역)."""
    import app
    import pipeline_service as ps
    import test_pipeline_provenance as TP
    d = Path(tempfile.mkdtemp(prefix=name + '_', dir=base))
    a, c = TP._write_bed(str(d), bed)
    (d / 'full_metrics.json').write_text(json.dumps(TP._bed_ledger(bed)), encoding='utf-8')
    fired = collections.Counter()
    before = {}
    buf = io.StringIO()

    def run(runner):
        return app._network_and_stage_e(str(d), str(ROOT / 'scripts'), a, c, '1:SE', 1, [], runner=runner,
                                        stop_before_stage_e=stop)
    err, stages = None, []
    patches = []
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        if repeat:
            run(TP._CLIRunner())
            before = _hashes(d, TP, ps)
            if crash == 'attempt_and_restore':                  # 정상 CLI 의 **다른** 해 (면적 · δ 절반) — 변조 숫자가 아니다
                with open(c, newline='') as f:
                    rr = csv.DictReader(f)
                    fields, rows = rr.fieldnames, list(rr)
                for row in rows:
                    row['contact_area'] = str(float(row['contact_area']) / 2)
                    row['delta'] = str(float(row['delta']) / 2)
                with open(c, 'w', newline='') as f:
                    w = csv.DictWriter(f, fields)
                    w.writeheader()
                    w.writerows(rows)
        mut = (lambda path: TP._edit_net_records(path, edit)) if edit else None
        cli = TP._CLIRunner(mutate=mut, break_solver=break_solver, delegate=TP._fake_stage_e)
        if crash:
            attempt_file = getattr(ps, 'ATTEMPT_FILE', 'network_attempt.json')
            prefix = getattr(ps, 'PUBLISH_BACKUP_PREFIX', '.publish_backup_')
            orig_aw = ps.atomic_write_json

            def aw(path, *args, **kwargs):
                if crash == 'fm_write' and Path(path).name == 'full_metrics.json':
                    fired['fm_write'] += 1
                    raise OSError('smoke injection: full_metrics write failure')
                if (crash == 'attempt_and_restore' and Path(path).name == attempt_file and args
                        and isinstance(args[0], dict) and args[0].get('latest_attempt_status') == 'success'):
                    fired['attempt_write'] += 1
                    raise OSError('smoke injection: success attempt write failure')
                return orig_aw(path, *args, **kwargs)
            ps.atomic_write_json = aw
            patches.append(('atomic_write_json', orig_aw))
            if crash == 'attempt_and_restore':
                if hasattr(ps, '_replace_retry'):
                    orig_rr = ps._replace_retry

                    def rr_(src, dst, *args, **kwargs):
                        if Path(src).name.startswith(prefix):
                            fired['restore'] += 1
                            raise PermissionError('smoke injection: full_metrics rollback destination unavailable')
                        return orig_rr(src, dst, *args, **kwargs)
                    ps._replace_retry = rr_
                    patches.append(('_replace_retry', orig_rr))
                orig_rep = os.replace

                def rep_(src, dst, *args, **kwargs):              # 되돌림이 os.replace 를 바로 써도 같은 주입 (이름 접두로만)
                    if Path(str(src)).name.startswith(prefix):
                        fired['restore'] += 1
                        raise PermissionError('smoke injection: full_metrics rollback destination unavailable (os.replace)')
                    return orig_rep(src, dst, *args, **kwargs)
                os.replace = rep_
                patches.append(('os.replace', orig_rep))
        try:
            stages, _rid = run(cli)
        except Exception as ex:                             # noqa: BLE001
            err = f'{type(ex).__name__}: {ex}'
        finally:
            for nm, fn in patches:
                if nm == 'os.replace':
                    os.replace = fn
                else:
                    setattr(ps, nm, fn)
    fm = read_json(d / 'full_metrics.json') or {}
    dual = read_json(d / 'network_conductivity_dual.json') or {}
    prov = ps.read_network_provenance(str(d)) or {}
    ui = None
    if hasattr(app, '_network_state_rows') and hasattr(app, '_network_generation'):
        try:
            ui = app._network_state_rows(dict(fm, _network_generation=app._network_generation(str(d))))
        except Exception as e:                              # noqa: BLE001
            ui = [f'UI 행 함수 예외 {type(e).__name__}: {e}']
    after = _hashes(d, TP, ps)
    return dict(name=name, status=('EXCEPTION' if err else ps.summarize(stages)[0]), error=err, fired=dict(fired),
                stages=[dict(step=s.get('step'), rc=s.get('rc'), ok=s.get('ok')) for s in stages],
                candidate_preserved=bool(dual), previous_generation_identical=(before == after) if repeat else None,
                provenance_run_id=prov.get('network_run_id'), fm_run_id=fm.get('network_run_id'),
                fm_sigma=fm.get('sigma_full_mScm'), dual_hertz_sigma=(dual.get('hertzian') or {}).get('sigma_full_mScm'),
                dual_hertz_ratio=(dual.get('hertzian') or {}).get('sigma_full'),
                attempt=ps.read_network_attempt(str(d)), status_view=ps.network_status_view(str(d)), ui_rows=ui,
                log_tail=buf.getvalue()[-600:])


def vm_probe():
    """C3 — Codex `vm_boundary.py` 와 같은 입력 (거의 정수압 · 전개식 근호 < 0 · 정확한 근호 > 0) · 순수 함수 호출."""
    import dem_analysis_core as D

    def rad(t):
        x, y, z = t
        return x ** 2 + y ** 2 + z ** 2 - x * y - y * z - x * z

    def exact(t):
        x, y, z = map(Fraction, t)
        return ((x - y) ** 2 + (y - z) ** 2 + (x - z) ** 2) / 2
    bad = None
    for p in (1000.0 * (1.0 + 0.0731 * k) for k in range(1, 500)):
        for f in (1e-8, 2e-8, 3e-8, 5e-8, 1e-9, 1e-10):
            t = (p, p, p * (1 + f))
            if rad(t) < 0 and exact(t) > 0:
                bad = t
                break
        if bad:
            break
    good = (0., 0., bad[2] - bad[0])

    def atom(t, z):
        return dict(type=1, x=1., y=1., z=z, radius=1., sigma_xx=t[0], sigma_yy=t[1], sigma_zz=t[2])
    with contextlib.redirect_stdout(io.StringIO()):
        v = D.calc_von_mises_stress({1: atom(bad, 1.), 2: atom(good, 2.)}, {1: 'AM_P'}, scale=1., plate_z=10.)
        uni = D.calc_von_mises_stress({1: atom(good, 1.), 2: atom(good, 2.)}, {1: 'AM_P'}, scale=1., plate_z=10.)

    def slim(r):
        r = r if isinstance(r, dict) else {}
        return {k: r.get(k) for k in ('status', 'vm_cv', 'reason', 'contract')}
    return dict(inputs=[list(bad), list(good)], expanded_radicand=rad(bad), exact_radicand=float(exact(bad)),
                exact_vm_equal=(exact(bad) == exact(good)), exact_cv_pct=0.0, actual=slim(v), positive_control=slim(uni))


def child_controls(spec: dict) -> dict:
    root = Path(spec['root'])
    _setup_child_env(root)
    base = root / 'controls'
    base.mkdir(parents=True, exist_ok=True)
    res = {}

    def upd(**kw):
        return lambda rec, n, m: rec.update(kw)
    for name, kw in (('c1_general_positive', dict(stop=False)),
                     ('c1_general_ratio_times4', dict(stop=False, edit=lambda rec, n, m: rec.update(sigma_full=rec['sigma_full'] * 4))),
                     ('c1b_general_band_ratio_missing', dict(stop=False, bed='band_l1', edit=upd(sigma_full=None))),
                     ('c2_single_fault_positive', dict(repeat=True, crash='fm_write')),
                     ('c2_double_fault_rollback', dict(repeat=True, crash='attempt_and_restore'))):
        try:
            res[name] = control_probe(base, name, **kw)
        except Exception as e:                              # noqa: BLE001
            res[name] = dict(name=name, harness_error=f'{type(e).__name__}: {e}')
    try:
        res['c3_vm_near_hydrostatic'] = vm_probe()
    except Exception as e:                                  # noqa: BLE001
        res['c3_vm_near_hydrostatic'] = dict(harness_error=f'{type(e).__name__}: {e}')
    return dict(id='controls', kind='controls', controls=res)


# ─────────────────────────────── 판정 (데이터로) ───────────────────────────────
def judge_c1(pos, neg):
    if not pos or not neg or pos.get('harness_error') or neg.get('harness_error'):
        return 'FAIL', f'시험 도구 오류 — {pos and pos.get("harness_error")} · {neg and neg.get("harness_error")}'
    if pos.get('status') != 'done':
        return 'FAIL', f'양성 대조 (변조 없는 일반 경로) 가 {pos.get("status")} — 대조가 무의미'
    if neg.get('status') != 'failed':
        return 'FAIL', f'σ_ratio ×4 일반 경로가 {neg.get("status")} (게시) — 기대 failed (RGLR2-01 수정 뒤)'
    if neg.get('candidate_preserved') and neg.get('provenance_run_id') and neg.get('dual_hertz_ratio') is not None:
        return 'FAIL', f'failed 인데 변조 후보가 활성 세대로 남았다 (ratio {neg.get("dual_hertz_ratio")})'
    return 'PASS', 'σ_ratio ×4 일반 경로 = failed · 양성 대조 done'


def judge_c1b(neg):
    if not neg or neg.get('harness_error'):
        return 'FAIL', f'시험 도구 오류 — {neg and neg.get("harness_error")}'
    return ('PASS', 'L1 + σ_ratio None 일반 경로 = failed') if neg.get('status') == 'failed' else (
        'FAIL', f'L1 + σ_ratio None 일반 경로가 {neg.get("status")} — 기대 failed (RGLR2-01 수정 뒤)')


def judge_c2(pos, dbl):
    if not pos or not dbl or pos.get('harness_error') or dbl.get('harness_error'):
        return 'FAIL', f'시험 도구 오류 — {pos and pos.get("harness_error")} · {dbl and dbl.get("harness_error")}'
    if not (pos.get('fired') or {}).get('fm_write'):
        return 'FAIL', '양성 대조의 주입 (full_metrics 쓰기 실패) 이 일어나지 않았다 — 시험 도구를 새 코드에 맞출 것'
    if pos.get('status') != 'failed' or pos.get('previous_generation_identical') is not True:
        return 'FAIL', f'양성 대조 (한 번 실패) 가 {pos.get("status")} · 이전 세대 그대로={pos.get("previous_generation_identical")}'
    f = dbl.get('fired') or {}
    if not f.get('attempt_write'):
        return 'FAIL', '이중 실패의 첫 주입 (성공 시도 쓰기) 이 일어나지 않았다 — 시험 도구를 새 코드에 맞출 것'
    if dbl.get('status') != 'failed':
        return 'FAIL', f'게시 중 I/O 실패 둘인데 {dbl.get("status")}'
    mixed = (dbl.get('provenance_run_id') != dbl.get('fm_run_id')) or (dbl.get('dual_hertz_sigma') != dbl.get('fm_sigma'))
    att, view = dbl.get('attempt') or {}, dbl.get('status_view') or {}
    ui_kept = any('이전 성공 세대 그대로' in str(r) for r in (dbl.get('ui_rows') or []))
    if mixed:
        if att.get('previous_generation_kept') is True or view.get('active_status') == 'success' or ui_kept:
            return 'FAIL', (f'섞인 세대 (provenance {dbl.get("provenance_run_id")} ≠ full_metrics {dbl.get("fm_run_id")}) 인데 '
                            f'previous_generation_kept={att.get("previous_generation_kept")} · active_status={view.get("active_status")} · '
                            f'UI "그대로"={ui_kept} — 기대 = 되돌림 실패 상태 (RGLR2-02 수정 뒤)')
        return 'PASS', (f'섞인 세대를 되돌림 실패로 표시 — kept={att.get("previous_generation_kept")} · active={view.get("active_status")} · '
                        f'주입 {f}')
    if dbl.get('previous_generation_identical') is True:
        return 'PASS', f'되돌림이 다른 길로 성공 — 이전 세대 그대로 (주입 {f})'
    return 'FAIL', f'세대는 안 섞였는데 이전 세대가 바뀌었다 (주입 {f})'


def judge_c3(vm, expect='zero'):
    if not vm or vm.get('harness_error'):
        return 'FAIL', f'시험 도구 오류 — {vm and vm.get("harness_error")}'
    a, pc = vm.get('actual') or {}, vm.get('positive_control') or {}
    if not vm.get('exact_vm_equal') or pc.get('status') != 'computed' or pc.get('vm_cv') != 0.0:
        return 'FAIL', f'양성 대조 (같은 VM 두 입자) 가 CV 0 computed 가 아니다: {pc}'
    if expect == 'zero':
        ok = a.get('status') == 'computed' and isinstance(a.get('vm_cv'), (int, float)) and abs(a['vm_cv']) <= 1e-6
        return ('PASS' if ok else 'FAIL'), f'거의 정수압 쌍 → {a} (기대 computed · CV 0 — 정확한 불변량 · RGLR2-03 수정 뒤)'
    ok = a.get('status') != 'computed' and a.get('vm_cv') is None
    return ('PASS' if ok else 'FAIL'), f'거의 정수압 쌍 → {a} (기대 null · 계산 안 함)'


def evaluate(reports: dict, timings: dict, expect_vm='zero', lhs_expect=None) -> list:
    checks = []

    def add(group, name, verdict, detail=''):
        checks.append(dict(group=group, name=name, verdict=verdict, detail=str(detail)[:600]))

    def ok(b):
        return 'PASS' if b else 'FAIL'
    for cid, r in reports.items():
        if cid == 'controls':
            continue
        t = timings.get(cid) or {}
        grp = 'A' if r.get('kind') in (*REFBEDS, 'synthetic') else 'B'
        add(grp, f'{cid}: 자식 프로세스 정상 종료 · 보고서 있음', ok(t.get('rc') == 0 and r.get('id') == cid),
            f'rc {t.get("rc")} {t.get("signal") or ""}')
        if r.get('kind') in REFBEDS:
            add(grp, f'{cid}: 원자료 sha256 = README 표 (압축 푼 바이트)', ok(r.get('raw_sha_ok')), r.get('raw_sha'))
        st, stop = r.get('status'), r.get('stop_after')
        req_bad = [s['step'] for s in r.get('stages') or [] if s.get('required') and not s.get('ok')]
        if stop == 'network':
            add(grp, f'{cid}: stop_after=network → done · Stage E 안 돌았다 · 망 정지 계약 통과',
                ok(st == 'done' and r.get('stage_e_ran') is False
                   and any(str(s.get('step', '')).startswith('Network stop contract') and s.get('ok') for s in r.get('stages') or [])),
                f'status {st} · 실패 단계 {r.get("failed_stages")} · 필수 실패 {req_bad} · Stage E {r.get("stage_e_ran")}')
        elif st is not None:
            add(grp, f'{cid}: 일반 경로 → done/partial (필수 단계 전부 성공) · 실제 Stage E 가 돌았다',
                ok(st in KEEP and not req_bad and r.get('stage_e_ran') is True),
                f'status {st} · 실패 단계 {r.get("failed_stages")} (선택 단계 실패는 partial — advanced_analysis*.py 가 리포에 없다) · '
                f'Stage E {r.get("stage_e_ran")} {r.get("stage_e_missing")}')
            fm = r.get('fm') or {}
            add(grp, f'{cid}: 세대 일치 — full_metrics run_id = provenance = Stage E parent = 반환값',
                ok(fm.get('network_run_id') and fm.get('network_run_id') == (r.get('provenance') or {}).get('network_run_id')
                   == fm.get('stage_e_parent_network_run_id') == r.get('returned_network_run_id')),
                f"{fm.get('network_run_id')} · {(r.get('provenance') or {}).get('network_run_id')} · {fm.get('stage_e_parent_network_run_id')}")
        if st == 'REFUSED':
            add(grp, f'{cid}: 같은 프레임 관문 통과', 'FAIL', r.get('why'))
            continue
        if stop == 'network' and st == 'done':
            fm = r.get('fm') or {}
            add(grp, f'{cid}: 세대 일치 — 반환 run_id = full_metrics = provenance (이번 실행)',
                ok(r.get('returned_network_run_id') and r.get('returned_network_run_id') == fm.get('network_run_id')
                   == (r.get('provenance') or {}).get('network_run_id')),
                f"{r.get('returned_network_run_id')} · {fm.get('network_run_id')} · {(r.get('provenance') or {}).get('network_run_id')}")
        if r.get('kind') == 'lhs' and st == 'done':
            want = (lhs_expect or {}).get(cid)
            sts = {m: (r.get('dual') or {}).get(m, {}).get('sigma_full_status') for m in ('hertzian', 'physics')}
            tau = r.get('tau') or {}
            if want is True:
                add(grp, f'{cid}: 관통 (인계표 percolation_pct > 0) → 두 모드 σ computed · τ 상태 ≠ NOT_COMPUTED',
                    ok(set(sts.values()) == {'computed'} and all(tau.get(f'ion_net_status_{m}') not in (None, 'NOT_COMPUTED')
                                                                 for m in ('hertz', 'physics'))), f'{sts} · {tau}')
            elif want is False:
                add(grp, f'{cid}: 비관통 (percolation_pct 0) → 두 모드 valid_zero · τ NOT_PERCOLATING',
                    ok(set(sts.values()) == {'valid_zero'} and all(tau.get(f'ion_net_status_{m}') == 'NOT_PERCOLATING'
                                                                   for m in ('hertz', 'physics'))), f'{sts} · {tau}')
    g, n = reports.get('real14_general'), reports.get('real14_network')
    if g and n and g.get('status') in KEEP and n.get('status') == 'done':
        keys = ('sigma_full_mScm', 'sigma_full_mScm_physics', 'electronic_sigma_full_mScm', 'thermal_sigma_full_mScm', 'porosity')
        add('A', 'real_14: 일반 경로 ↔ 망 정지 — 망 σ (이온 두 모드 · 전자 · 열) · 공극률 같다 (같은 입력 · 같은 솔버)',
            ok(all(g['fm'].get(k) == n['fm'].get(k) for k in keys)), {k: (g['fm'].get(k), n['fm'].get(k)) for k in keys})
        por = n['fm'].get('porosity')
        add('A', f'real_14: 공극률 ε_sphere ≈ {REAL14_POROSITY_REF} % (case_master · README)',
            ok(isinstance(por, (int, float)) and abs(por - REAL14_POROSITY_REF) < 1e-3), por)
    c = (reports.get('controls') or {}).get('controls') or {}
    if c:
        v, why = judge_c1(c.get('c1_general_positive'), c.get('c1_general_ratio_times4'))
        add('C', 'C1 일반 경로 σ_ratio ×4 → failed (RGLR2-01)', v, why)
        v, why = judge_c1b(c.get('c1b_general_band_ratio_missing'))
        add('C', 'C1b 일반 경로 L1 + σ_ratio None → failed (RGLR2-01)', v, why)
        v, why = judge_c2(c.get('c2_single_fault_positive'), c.get('c2_double_fault_rollback'))
        add('C', 'C2 게시 중 I/O 실패 둘 → 되돌림 실패 상태 · "이전 세대 그대로" 아님 (RGLR2-02)', v, why)
        v, why = judge_c3(c.get('c3_vm_near_hydrostatic'), expect_vm)
        add('C', f'C3 거의 정수압 VM 쌍 → {"CV 0" if expect_vm == "zero" else "null"} (RGLR2-03)', v, why)
    return checks


# ─────────────────────────────── 부모 ───────────────────────────────
def run_child(root: Path, spec: dict, python: str) -> dict:
    cdir = root / 'cases' / spec['id']
    cdir.mkdir(parents=True, exist_ok=True)
    (root / 'tmp' / spec['id']).mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, **THREAD_ENV, PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1', TMPDIR=str(root / 'tmp' / spec['id']))
    env.setdefault('MPLBACKEND', 'Agg')
    spec_p = cdir / 'spec.json'
    write_json(spec_p, spec)
    t0, start = time.monotonic(), now_iso()
    with open(cdir / 'log.txt', 'wb') as log:
        p = subprocess.Popen([python, str(Path(__file__).resolve()), '--_child', str(spec_p)], cwd=str(root), env=env,
                             stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
        _pid, status, ru = os.wait4(p.pid, 0)
    rc = os.waitstatus_to_exitcode(status)
    p.returncode = rc
    sig = None
    if rc < 0:
        import signal as _sg
        with contextlib.suppress(ValueError):
            sig = _sg.Signals(-rc).name
    return dict(rc=rc, signal=sig, start=start, end=now_iso(), wall_s=round(time.monotonic() - t0, 2),
                peak_rss_mb=round(ru.ru_maxrss / 1024, 1), user_s=round(ru.ru_utime, 2), sys_s=round(ru.ru_stime, 2),
                log=str(cdir / 'log.txt'))


def git_short():
    try:
        return subprocess.run(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:                                       # noqa: BLE001
        return ''


def run_smoke(args, jobs, *, out=print) -> int:
    root = Path(args.root).expanduser().resolve()
    if root.exists() and any(root.iterdir()):
        out(f'⛔ ROOT {root} 가 비어 있지 않다 — 새 ROOT 를 쓸 것 (격리 출력)')
        return 3
    root.mkdir(parents=True, exist_ok=True)
    py = args.python or sys.executable
    out(f'══ WSL 소형 통합 시험 — ROOT {root} · 코드 {git_short()[:9]} · 케이스 {len(jobs)} (자식 프로세스 · 단일 스레드 env)')
    reports, timings = {}, {}
    for spec in jobs:
        spec = dict(spec, root=str(root))
        out(f'  ▶ {spec["id"]} ({spec["kind"]}{", stop_after=" + str(spec.get("stop")) if spec["kind"] != "controls" else ""}) …', flush=True)
        t = run_child(root, spec, py)
        rep = read_json(root / 'cases' / spec['id'] / 'report.json') or dict(id=spec['id'], kind=spec['kind'],
                                                                           status='NO_REPORT', why='자식이 보고서를 못 썼다 — log.txt')
        reports[spec['id']], timings[spec['id']] = rep, t
        fm = rep.get('fm') or {}
        out(f'    {spec["id"]}: status {rep.get("status", "—")} · 경과 {t["wall_s"]} s (파이프라인 {rep.get("pipeline_s", "—")} s) · '
            f'최대 RSS {t["peak_rss_mb"]} MB · rc {t["rc"]}{" " + t["signal"] if t["signal"] else ""} · '
            f'σ_ion H/P {fm.get("sigma_full_mScm")} / {fm.get("sigma_full_mScm_physics")} · run_id {rep.get("returned_network_run_id")} · '
            f'Stage E {rep.get("stage_e_ran")}', flush=True)
    lhs_expect = {s['id']: s.get('expect_perc') for s in jobs if s['kind'] == 'lhs'}
    checks = evaluate(reports, timings, args.vm_expect, lhs_expect)
    fail_ab = [c for c in checks if c['verdict'] != 'PASS' and c['group'] in ('A', 'B')]
    fail_c = [c for c in checks if c['verdict'] != 'PASS' and c['group'] == 'C']
    rc = 1 if fail_ab else (2 if fail_c else 0)
    report = dict(schema='wsl_network_smoke/v1', created=now_iso(), root=str(root), git_sha=git_short(), python=py,
                  thread_env=THREAD_ENV, argv=sys.argv, jobs=jobs, timings=timings, reports=reports, checks=checks, rc=rc,
                  note='격리 출력 · 공식 결과 · 인계 아님 (Codex RGLR 3차 재검증 조건부 GO).  C = 수정 뒤 기대 동작 — 수정 전 코드에서는 FAIL 이 정상.')
    write_json(root / 'smoke_report.json', report)
    lines = [f'WSL 소형 통합 시험 {report["created"]} · 코드 {report["git_sha"][:9]} · ROOT {root}', '',
             'case\tstatus\twall_s\tpipeline_s\tpeak_rss_MB\trc\tsigma_ion_H\tsigma_ion_P\tnetwork_run_id\tstage_E']
    for cid, r in reports.items():
        t, fm = timings[cid], (r.get('fm') or {})
        lines.append('\t'.join(str(x) for x in (cid, r.get('status', '—'), t['wall_s'], r.get('pipeline_s', '—'), t['peak_rss_mb'],
                                                t['rc'], fm.get('sigma_full_mScm'), fm.get('sigma_full_mScm_physics'),
                                                r.get('returned_network_run_id'), r.get('stage_e_ran'))))
    lines += ['', f'검사 {len(checks)} · PASS {sum(c["verdict"] == "PASS" for c in checks)} · 실데이터 FAIL {len(fail_ab)} · '
                  f'음성 대조 FAIL {len(fail_c)} (수정 전이면 정상) · rc {rc}']
    for c in checks:
        lines.append(f'  {"✓" if c["verdict"] == "PASS" else "✗"} [{c["group"]}] {c["name"]}' + (f'  — {c["detail"][:220]}'
                                                                                             if c['verdict'] != 'PASS' else ''))
    (root / 'smoke_summary.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    out('\n'.join(lines))
    out(f'══ 보고 {root / "smoke_report.json"} · 요약 {root / "smoke_summary.txt"}')
    return rc


def build_jobs(args) -> list:
    import run_network_194_parallel as NP
    jobs = []
    if not args.skip_real14:
        if not args.skip_real14_general:
            jobs.append(dict(id='real14_general', kind='real14', stop=None))
        jobs.append(dict(id='real14_network', kind='real14', stop='network'))
    if not args.skip_case15:                                # ★ 10-07 §7-4 — case15 (corner · 182,995 접촉) 망 정지
        jobs.append(dict(id='case15_network', kind='case15', stop='network'))
    if not args.skip_lhs:
        picks = ([(c, *lhs_expected_perc(c)) for c in args.lhs_case] if args.lhs_case
                 else [(c, f, e) for c, f, e in pick_lhs_cases()])
        for c, fam, exp in picks:
            if fam is None:
                raise SystemExit(f'⛔ {c} 가 커밋된 인계표 (lhs · lhsx) 에 없다')
            sp = NP.COHORT_SPECS[fam]
            jobs.append(dict(id=c, kind='lhs', stop='network', cohort=str(ROOT / sp['cohort']), harvest_dir=str(ROOT / sp['harvest']),
                             expect_perc=exp, root_from=args.root_from, root_to=args.root_to))
    if not args.skip_controls:
        jobs.append(dict(id='controls', kind='controls'))
    return jobs


def _selftest() -> int:
    """이 컨테이너 — 합성 침대 (CSV 입력) 로 **실제 파이프라인**을 돌려 시험 도구 (자식 · 측정 · 수집 · 판정 · 보고) 를 본다.
    음성 대조 판정 함수는 합성 결과로 변별력을 본다 (수정 전 · 뒤 모양 둘 다).  실 음성 대조도 돌려 '판정이 나온다' 만 본다 (값은 코드 세대에 따른다)."""
    fails = []

    def chk(name, okv, why=''):
        print(('  ✓ ' if okv else '  ✗ ') + name + ('' if okv or not why else f'  — {why}'))
        if not okv:
            fails.append(name)
    # 판정 함수 변별력 (합성)
    pos = dict(status='done')
    chk('판정 C1 — ×4 가 done 이면 FAIL · failed 면 PASS · 양성 대조가 done 이 아니면 FAIL',
        judge_c1(pos, dict(status='done'))[0] == 'FAIL' and judge_c1(pos, dict(status='failed'))[0] == 'PASS'
        and judge_c1(dict(status='failed'), dict(status='failed'))[0] == 'FAIL')
    p2 = dict(status='failed', previous_generation_identical=True, fired={'fm_write': 1})
    mixed_bad = dict(status='failed', fired={'attempt_write': 1, 'restore': 1}, provenance_run_id='OLD', fm_run_id='NEW', fm_sigma=1.0,
                     dual_hertz_sigma=2.0, attempt={'previous_generation_kept': True}, status_view={'active_status': 'success'},
                     ui_rows=[['x', '활성 세대 OLD 의 값 (이전 성공 세대 그대로)']])
    mixed_ok = dict(mixed_bad, attempt={'previous_generation_kept': False}, status_view={'active_status': 'rollback_failed'},
                    ui_rows=[['x', '되돌림 실패']])
    chk('판정 C2 — 섞인 세대 + kept True · active success = FAIL (수정 전 모양) · kept False · rollback_failed = PASS · 주입 안 됨 = FAIL',
        judge_c2(p2, mixed_bad)[0] == 'FAIL' and judge_c2(p2, mixed_ok)[0] == 'PASS'
        and judge_c2(p2, dict(mixed_ok, fired={}))[0] == 'FAIL')
    #  ★ 10-07 §7-4 — 참조 침대 둘 (real14 · case15) 을 업로드 폴더에 두는 단계 (파이프라인 전) — sha256 = README 표 · 덱의 상 매핑
    _st_tmp = Path(tempfile.mkdtemp(prefix='smoke_ref_')).resolve()
    try:
        staged = {}
        for k in REFBEDS:
            (_st_tmp / k).mkdir()
            staged[k] = stage_refbed(k, _st_tmp / k)
        chk('참조 침대 두기 — real14 · case15 원자료 sha256 = README 표 (압축 푼 바이트) · 상 매핑 real14 1:AM_P,2:AM_S,3:SE · case15 1:AM_P,2:SE · 오류 0',
            all(v['raw_sha_ok'] and not v['type_map_errors'] for v in staged.values())
            and staged['real14']['type_map'] == '1:AM_P,2:AM_S,3:SE' and staged['case15']['type_map'] == '1:AM_P,2:SE',
            repr({k: (v['raw_sha_ok'], v['type_map'], v['type_map_errors']) for k, v in staged.items()}))
    finally:
        shutil.rmtree(_st_tmp, ignore_errors=True)
    vm_bad = dict(exact_vm_equal=True, actual={'status': 'computed', 'vm_cv': 100.0}, positive_control={'status': 'computed', 'vm_cv': 0.0})
    vm_ok = dict(vm_bad, actual={'status': 'computed', 'vm_cv': 0.0})
    vm_null = dict(vm_bad, actual={'status': 'invalid', 'vm_cv': None})
    chk('판정 C3 — CV 100 computed = FAIL · CV 0 = PASS (zero) · null = PASS (null) / FAIL (zero)',
        judge_c3(vm_bad)[0] == 'FAIL' and judge_c3(vm_ok)[0] == 'PASS' and judge_c3(vm_null, 'null')[0] == 'PASS'
        and judge_c3(vm_null, 'zero')[0] == 'FAIL')
    # 실제 파이프라인 — 합성 침대 (관통 se_am) 일반 경로 + 망 정지 · 실 음성 대조
    tmp = Path(tempfile.mkdtemp(prefix='smoke_st_')).resolve()
    try:
        a = _parse(['--root', str(tmp / 'root')])
        jobs = [dict(id='syn_general', kind='synthetic', bed='se_am', type_map='1:SE,2:AM_P', scale=1, stop=None),
                dict(id='syn_network', kind='synthetic', bed='se_am', type_map='1:SE,2:AM_P', scale=1, stop='network'),
                dict(id='controls', kind='controls')]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = run_smoke(a, jobs, out=lambda *x, **k: print(*x))
        rep = read_json(tmp / 'root' / 'smoke_report.json') or {}
        r = rep.get('reports') or {}
        t = rep.get('timings') or {}
        chk(f'실제 파이프라인 — 합성 일반 경로 = partial/done · Stage E 돌았다 · 망 정지 = done · Stage E 안 돌았다 (rc {rc})',
            (r.get('syn_general') or {}).get('status') in KEEP and (r.get('syn_general') or {}).get('stage_e_ran') is True
            and (r.get('syn_network') or {}).get('status') == 'done' and (r.get('syn_network') or {}).get('stage_e_ran') is False,
            repr({k: (v.get('status'), v.get('stage_e_ran')) for k, v in r.items()}))
        chk('케이스마다 경과 · 최대 RSS · rc 가 기록된다', all(t.get(k, {}).get('wall_s', 0) > 0 and t.get(k, {}).get('peak_rss_mb', 0) > 0
                                                         and t.get(k, {}).get('rc') == 0 for k in ('syn_general', 'syn_network', 'controls')),
            repr(t))
        A = [c for c in rep.get('checks') or [] if c['group'] == 'A']
        chk(f'A 묶음 검사 (합성) 전부 PASS — {len(A)} 개', A and all(c['verdict'] == 'PASS' for c in A),
            repr([c for c in A if c['verdict'] != 'PASS']))
        C = [c for c in rep.get('checks') or [] if c['group'] == 'C']
        cc = ((r.get('controls') or {}).get('controls')) or {}
        chk(f'C 묶음 — 네 대조 판정이 나온다 (시험 도구 오류 없음 · 지금 코드 결과: {[(c["name"][:3], c["verdict"]) for c in C]})',
            len(C) == 4 and not any('harness_error' in v for v in cc.values())
            and (cc.get('c2_double_fault_rollback') or {}).get('fired', {}).get('attempt_write'),
            repr({k: v.get('harness_error') for k, v in cc.items() if isinstance(v, dict)}))
        chk('보고 파일 둘 · rc 규칙 (A·B FAIL 없으면 C 결과에 따라 0/2)', (tmp / 'root' / 'smoke_summary.txt').exists()
            and rc == (2 if any(c['verdict'] != 'PASS' for c in C) else 0))
        chk('격리 — 리포 추적 파일 무변경 (LHS-27 요약 CSV 포함)', not subprocess.run(
            ['git', '-C', str(ROOT), 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.strip())
        chk('비어 있지 않은 ROOT 거부 (rc 3)', run_smoke(a, jobs[:1], out=lambda *x, **k: None) == 3)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


def _parse(argv=None):
    ap = argparse.ArgumentParser(description='WSL 소형 통합 시험 (격리 출력 · 실제 웹앱 파이프라인)')
    ap.add_argument('--root', default='', help='새 출력 ROOT (비어 있지 않으면 거부)')
    ap.add_argument('--lhs-case', action='append', default=[], help='LHS 케이스 바꾸기 (여러 번 · 기본 = 자동 고르기 셋)')
    ap.add_argument('--skip-real14', action='store_true')
    ap.add_argument('--skip-real14-general', action='store_true', help='real_14 일반 경로 (실제 Stage E) 빼기')
    ap.add_argument('--skip-case15', action='store_true', help='case15 (커밋된 corner 침대 · 망 정지) 빼기')
    ap.add_argument('--skip-lhs', action='store_true', help='LHS 원자료가 없는 기계')
    ap.add_argument('--skip-controls', action='store_true')
    ap.add_argument('--vm-expect', choices=['zero', 'null'], default='zero', help='C3 기대 — zero = CV 0 (안정식) · null = 계산 안 함')
    ap.add_argument('--root-from', default='', help='코호트 경로 접두사 (lhs_webapp_batch 와 같은 뜻)')
    ap.add_argument('--root-to', default='')
    ap.add_argument('--python', default='', help='자식 인터프리터 (기본 = 이것)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--_child', default='', help=argparse.SUPPRESS)
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = _parse(argv)
    if a._child:
        spec = read_json(a._child)
        root = Path(spec['root'])
        try:
            rep = child_controls(spec) if spec['kind'] == 'controls' else child_case(spec)
        except Exception as e:                              # noqa: BLE001 — 보고서에 남긴다 (부모가 FAIL 로 읽는다)
            import traceback
            rep = dict(id=spec['id'], kind=spec['kind'], status='HARNESS_ERROR', why=f'{type(e).__name__}: {e}',
                       traceback=traceback.format_exc()[-3000:])
        write_json(root / 'cases' / spec['id'] / 'report.json', rep)
        return 0 if rep.get('status') != 'HARNESS_ERROR' else 1
    if a.selftest:
        return _selftest()
    if not a.root:
        print('⛔ --root 가 필요하다 (새 출력 폴더)', file=sys.stderr)
        return 3
    if os.name != 'posix' or not hasattr(os, 'wait4'):
        print('⛔ Linux/WSL 전용 (os.wait4)', file=sys.stderr)
        return 3
    return run_smoke(a, build_jobs(a))


if __name__ == '__main__':
    sys.exit(main())
