#!/usr/bin/env python3
"""50kg 4차년도 DEM 보고 초안 2 — 침대별 지표 러너 (끝 세트 하나 → 검토된 웹앱 파이프라인 → metrics_<침대>.json) + 병합.

    # 침대 하나 (D2 · D3 = 리포 기록과 대조 · D1 · D0.7 = 받은 묶음 · 기록 없으면 sha256 만 적는다)
    python3 -P docs/50kg/report_y4/draft2/run_draft2_metrics.py run --bed D2 \\
        --tgz docs/data/kg50_d2_end_20261030/kg50_d2_end_20261030_4files.tgz \\
        --log docs/data/kg50_d2_end_20261030/kg50_d2_b50_log.liggghts
    # 병합 (data/<침대>/metrics_<침대>.json 전부 → metrics_all.csv · 없는 침대 = 결과 대기)
    python3 -P docs/50kg/report_y4/draft2/run_draft2_metrics.py merge
    # 한 번에 (run → merge → 그림)
    python3 -P docs/50kg/report_y4/draft2/run_draft2_metrics.py add --bed D1 --tgz <D1 끝 묶음> --log <D1 로그>

비교 상태 = **판 고정 이완 끝 세트 하나** (1저자 10-30 · `draft2_fix_plan_20261030.md` §3 · `K50Y4-01`):
  atom_end_<S> · contact_end_<S> · mesh_end_<S> 가 **같은 S** 로 다 있어야 한다 (덤프 머리 TIMESTEP 까지 대조) — 하나라도 없거나 S 가 다르면 거부.
  압력 도달 순간 세트 = NOT_AVAILABLE (자료 없음) — 이 러너는 이완 끝 프레임을 300 MPa 상태로 부르지 않는다.

값의 출처 (새 지표 정의 없음 — 기존 함수 · 기존 출력의 집계만):
  · 웹앱 `run_pipeline(stop_after='network', figures=False, auto_db=False)` — 업로드 (`/upload` · Flask 시험 클라이언트 · 격리 폴더) 까지
    `docs/data/kg50_d3_cell_verdict_20261027/{upload_cases,run_cases}.py` 와 같은 호출.  지표 = full_metrics.json
    (dem_analysis_core.run_full_analysis: calc_porosity_dual · calc_porosity_union_exact · calc_interface_area · calc_coverage ·
    calc_percolation · calc_se_se_cn · calc_tortuosity_all · calc_ionic_active_am · calc_overlap_ratio · calc_love_weber_stress …) ·
    망 = network_conductivity (Hertz 주 · Physics 민감도) · `tau_flux.case_row` (f · 수송 tortuosity = φ_SE·σ₀/σ_eff · 제곱근 아님) ·
    다섯 판정 값 = `kg50_d3_cell_verdict.extract` (상태 · 유한성 검사 포함).
  · 입자 · 접촉별 집계 (z 구간 · AM 하나당 · 문턱별): 같은 결과 폴더의 atoms.csv · contacts.csv · coverage_per_am.csv · percolation_sets.json
    + `coverage_physics_vs_hertzian.union_coverage_bed` (AM 별 합집합 cap 피복) · `calc_love_weber_stress(return_arrays=True)` (입자별 σ_VM) ·
    `lhs_union_webapp.coverage` (정확 합집합 몬테카를로 점의 공극 표지 — calc_porosity_union_exact 와 같은 씨앗 · 같은 점) ·
    `calc_overlap_ratio` 의 접촉별 정의 (δ / min(r₁, r₂)).  집계마다 웹앱 전체 값과 대조한다 (어긋나면 멈춘다).
  · 압밀 곡선 = 로그 (`figs/make_fig_p2_aux.parse_log` · `branches` — 초안 1 보조 그림과 같은 함수) · ε_sphere = 1 − ΣV구 / (Lx·Ly·판 높이).
  · 1쪽 단면 = `figs/make_figs_p1.section_circles` (y = 상자 가운데) · OVITO 사본 = 끝 atom 덤프 (µm · 확장 XYZ · gzip).

알려진 침대 (D2 · D3) 는 Codex 독립 재계산 값 (ε_sphere · 이완 끝 판 압력) 과 출력 자릿수까지 같아야 한다 — 다르면 rc 3 으로 멈춘다.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
for p in (REPO / 'scripts', REPO / 'webapp', HERE.parent, HERE.parent / 'figs', HERE):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import kg50_y4_sources as src  # noqa: E402

SCHEMA = 'kg50_y4_draft2_metrics/v1'
DATA = HERE / 'data'
OVITO = HERE / 'ovito'
#: 침대 순서 = 비교 순서 0.7 → 1 → 2 → 3 (분석 계획 Q4) · 덱 · manifest = kg50_y4_sources.BEDS 와 같다
BED_ORDER = ('D0.7', 'D1', 'D2', 'D3')
CASE = {'D0.7': 'kg50_d07_b50', 'D1': 'kg50_d1_b50', 'D2': 'kg50_d2_b50', 'D3': 'kg50_d3_b50_s1'}
#: 리포에 기록이 있는 끝 묶음 (묶음 · 멤버 sha256 대조) — D1 · D0.7 은 받은 뒤 이 표에 넣거나 --record 로 준다
RECORDS = {
    'D2': dict(tgz='docs/data/kg50_d2_end_20261030/kg50_d2_end_20261030_4files.tgz', record='docs/data/kg50_d2_end_20261030/README.md',
               log='docs/data/kg50_d2_end_20261030/kg50_d2_b50_log.liggghts'),
    'D3': dict(tgz='docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_end_20261027.tgz', record='docs/data/kg50_d3_cell_verdict_20261027/README.md',
               member_record='docs/data/kg50_d3_cell_verdict_20261027/inputs_sha256.txt',
               log='docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_b50_s1_log.liggghts'),
}
#: Codex 독립 재계산 (`docs/reviews/codex_kg50_y4_draft1_review_20261030/codex_review_kg50_y4_draft1_20261030.md` §3) — 출력 자릿수 그대로
CODEX = {
    'D2': dict(eps_sphere_pct=('16.7379229', 7), p_end_MPa=('279.79158', 5), end_step=4015002, stop_step=3915002,
               p_t0minus_MPa=('300.23909', 5), p_relax_first_MPa=('287.18633', 5), n_am=1481, n_se=20872),
    'D3': dict(eps_sphere_pct=('18.9575565', 7), p_end_MPa=('291.37440', 5), end_step=4575002, stop_step=4475002,
               p_t0minus_MPa=('300.63094', 5), p_relax_first_MPa=('295.59389', 5), n_am=1482, n_se=6184),
}
N_ZBINS = 10                      # z 구간 수 (바닥 0 → 판 높이 · 같은 폭) — 기존 입자 · 점 출력을 중심 z 로 묶는다
OVERLAP_THRESHOLDS = (0.0, 2.0, 5.0, 10.0)   # % · Zhou 2025 표 1 의 문턱 (카드 tailored_cathode_microstructure_low_pressure_assb)
SIM_PA_TO_MPA = 1.0e-3            # 덱 단위 응력 (Pa) × 1000 = 실제 Pa → MPa (dem_analysis_core 머리: real(MPa) = sim × SCALE / 1e6)
TOOL_FILES = ('scripts/dem_analysis_core.py', 'scripts/analyze_contacts.py', 'scripts/parse_liggghts.py', 'scripts/network_conductivity.py',
              'scripts/tau_flux.py', 'scripts/coverage_physics_vs_hertzian.py', 'scripts/lhs_union_webapp.py',
              'scripts/kg50_d3_cell_verdict.py', 'webapp/app.py', 'webapp/pipeline_service.py',
              'docs/50kg/report_y4/kg50_y4_sources.py', 'docs/50kg/report_y4/figs/make_fig_p2_aux.py',
              'docs/50kg/report_y4/figs/make_figs_p1.py', 'docs/50kg/report_y4/draft2/run_draft2_metrics.py')
TOOL_FUNCTIONS = (
    'webapp.app./upload (Flask test client) + run_pipeline(stop_after="network", figures=False, auto_db=False)',
    'scripts/analyze_contacts.py → dem_analysis_core.run_full_analysis (calc_porosity_dual · calc_porosity_union_exact · '
    'calc_interface_area · calc_coverage · calc_percolation · calc_se_se_cn · calc_am_am_cn · calc_tortuosity_all · '
    'calc_ionic_active_am · calc_overlap_ratio · calc_am_isolation_risk · calc_love_weber_stress)',
    'scripts/coverage_physics_vs_hertzian.py (coverage_per_am.csv · union_coverage_bed)',
    'scripts/network_conductivity.py (hertzian · physics · hertz_h12) → tau_flux.case_row',
    'scripts/kg50_d3_cell_verdict.extract (porosity · coverage Hertz/Physics · σ_ion · tau2 상태 검사)',
    'dem_analysis_core.calc_love_weber_stress(return_arrays=True) · calc_overlap_ratio · get_plate_z · _get_box_xy',
    'analyze_contacts.load_atoms_raw · load_contacts_raw',
    'lhs_union_webapp.coverage (calc_porosity_union_exact 와 같은 씨앗 · 같은 점 · z 구간 집계)',
    'docs/50kg/report_y4/figs/make_fig_p2_aux.parse_log · branches (로그 압밀 곡선)',
    'docs/50kg/report_y4/figs/make_figs_p1.section_circles (y = 상자 가운데 단면)',
)


class RunError(RuntimeError):
    pass


def need(cond, msg):
    if not cond:
        raise RunError(msg)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_path(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            h.update(blk)
    return h.hexdigest()


def relpath(p):
    p = Path(p).resolve()
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


def git_state():
    def g(*a):
        r = subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True)
        return r.returncode, r.stdout.strip()
    rc, head = g('rev-parse', 'HEAD')
    rc2, _ = g('diff', '--quiet', 'HEAD', '--')
    return dict(head=head if rc == 0 else None, tracked_clean=(rc2 == 0))


# ───────────────────────────── 1. 끝 세트 (같은 step 세 파일 + 덱) ─────────────────────────────

_SAFE = re.compile(r'^[A-Za-z0-9_.\-/]+$')


def pick_members(tf, case, prefix):
    """묶음 안에서 이 침대의 덱 · atom_end · contact_end · mesh_end 를 고른다 — 같은 S 가 아니면 거부 (K50Y4-01 소비자 규칙)."""
    names = [m for m in tf.getmembers() if m.name.startswith(prefix)]
    need(names, f'묶음에 접두 {prefix!r} 로 시작하는 멤버가 없다')
    pat = {'atom': re.compile(r'(?:^|/)atom_end_(\d+)\.liggghts$'), 'contact': re.compile(r'(?:^|/)contact_end_(\d+)\.liggghts$'),
           'mesh': re.compile(r'(?:^|/)mesh_end_(\d+)\.stl$')}
    found = {k: [] for k in pat}
    for m in names:
        for k, rx in pat.items():
            hit = rx.search(m.name)
            if hit:
                found[k].append((m, int(hit.group(1))))
    for k, v in found.items():
        need(len(v) == 1, f'{k}_end 멤버가 정확히 하나여야 한다 — {len(v)} 개 ({[m.name for m, _ in v]}) · 결손 세트 거부')
    steps = {k: v[0][1] for k, v in found.items()}
    need(len(set(steps.values())) == 1, f'끝 세트 step 이 다르다 {steps} — 같은 step 세트만 받는다 (K50Y4-01)')
    decks = [m for m in names if re.search(rf'(?:^|/)input_{re.escape(case)}\.liggghts$', m.name)]
    need(len(decks) <= 1, f'덱 input_{case}.liggghts 멤버가 여럿이다 ({[m.name for m in decks]})')
    out = dict(atom=found['atom'][0][0], contact=found['contact'][0][0], mesh=found['mesh'][0][0])
    if decks:                                # 없으면 리포 덱 (manifest deck_sha256 대조) — read_end_set 이 채운다
        out['deck'] = decks[0]
    for k, m in out.items():
        need(m.isfile() and _SAFE.match(m.name) and not m.name.startswith('/') and '..' not in m.name.split('/'),
             f'멤버 {m.name!r} — 일반 파일 · 안전한 이름이 아니다')
    return out, steps['atom']


def dump_timestep(blob):
    lines = blob[:4096].decode('ascii', errors='strict').split('\n')
    need(lines[0].strip() == 'ITEM: TIMESTEP', '덤프 첫 줄이 ITEM: TIMESTEP 이 아니다')
    return int(lines[1])


def read_end_set(bed, tgz, prefix, work, record=None, member_record=None):
    """묶음 → (blobs, info).  멤버만 메모리로 읽고 빈 작업 폴더에 basename 으로 쓴다 (실행 · import 없음)."""
    case = CASE[bed]
    tgz = Path(tgz)
    info = dict(tgz=relpath(tgz), tgz_sha256=sha256_path(tgz), tgz_bytes=tgz.stat().st_size, prefix=prefix, members={},
                tgz_record=None, member_record=None)
    if record:
        rec_sha = src._recorded_tgz_sha(relpath(record), tgz.name)
        need(rec_sha == info['tgz_sha256'], f'{tgz}: sha256 {info["tgz_sha256"][:12]}… ≠ 기록 {rec_sha[:12]}…')
        info['tgz_record'] = dict(file=relpath(record), match=True)
    with tarfile.open(tgz, 'r:gz') as tf:
        mem, step = pick_members(tf, case, prefix)
        blobs = {k: tf.extractfile(m).read() for k, m in mem.items()}
    for k, m in mem.items():
        info['members'][m.name] = dict(role=k, bytes=len(blobs[k]), sha256=sha256_bytes(blobs[k]))
    info['deck_source'] = 'tgz member'
    if 'deck' not in blobs:                  # 묶음에 덱이 없다 → 리포 덱 (deck_check 가 manifest deck_sha256 와 대조)
        b = next(x for x in src.BEDS if x['case'] == case)
        blobs['deck'] = src.rp(b['deck']).read_bytes()
        info['deck_source'] = f'repo {b["deck"]} (묶음에 덱 멤버 없음)'
    if record or member_record:
        end = dict(record=relpath(record)) if record else {}
        if member_record:
            end['member_record'] = relpath(member_record)
        rec = src._recorded_member_shas(end)
        bad = {n: (v['sha256'][:12], str(rec.get(n))[:12]) for n, v in info['members'].items() if rec.get(n) != v['sha256']}
        need(not bad, f'멤버 sha256 ≠ 기록: {bad}')
        info['member_record'] = dict(file=end.get('member_record') or end.get('record'), match=True, n=len(info['members']))
    t_atom, t_contact = dump_timestep(blobs['atom']), dump_timestep(blobs['contact'])
    need(t_atom == step and t_contact == step, f'덤프 머리 TIMESTEP (atom {t_atom} · contact {t_contact}) ≠ 파일 이름 step {step}')
    indir = Path(work) / 'in'
    indir.mkdir(parents=True, exist_ok=False)
    paths = {}
    for k in ('deck', 'atom', 'contact', 'mesh'):
        p = indir / (Path(mem[k].name).name if k in mem else f'input_{case}.liggghts')
        p.write_bytes(blobs[k])
        paths[k] = p
    info['end_step'] = step
    info['same_step_set'] = dict(atom=t_atom, contact=t_contact, mesh_name_step=step, ok=True)
    return blobs, paths, info


# ───────────────────────────── 2. 덱 · 덤프 · ε_sphere · 로그 ─────────────────────────────

def deck_check(bed, blob):
    """묶음 안 덱 = 리포 덱 = manifest deck_sha256 (kg50_y4_sources.BEDS 와 같은 자리)."""
    b = next(x for x in src.BEDS if x['case'] == CASE[bed])
    text = blob.decode('utf-8')
    sha = sha256_bytes(blob)
    repo_sha = src.sha256_file(b['deck'])
    _man, mc = src.read_manifest_case(b['manifest'], b['case'])
    need(sha == repo_sha == mc['deck_sha256'], f'{bed}: 묶음 덱 {sha[:12]}… · 리포 덱 {repo_sha[:12]}… · manifest {mc["deck_sha256"][:12]}… 가 같지 않다')
    d = src.parse_deck(text, b['case'])
    return d, dict(repo_deck=b['deck'], manifest=b['manifest'], sha256=sha)


def eps_sphere(atoms, d, plate_z_um):
    v = float(np.sum(4.0 / 3.0 * np.pi * (atoms['r'] * src.LEN_SIM_TO_UM) ** 3))
    return v, 100.0 * (1.0 - v / (d['box_x_um'] * d['box_y_um'] * plate_z_um))


def log_curve(bed, log_path, atoms, plate_z_sim, step, d):
    """초안 1 보조 그림과 같은 함수 (make_fig_p2_aux.branches) — 가압 가지 · 판 고정 이완 가지."""
    import make_fig_p2_aux as P2
    es = dict(atoms=atoms, plate_z_sim=plate_z_sim, plate_z_um=plate_z_sim * src.LEN_SIM_TO_UM, step=step)
    fake = {bed: dict(case=CASE[bed], endstate=es)}
    common = dict(press_speed_sim=d['press_speed_sim'], dt=d['dt'], box_x_um=d['box_x_um'], box_y_um=d['box_y_um'],
                  target_MPa=d['target_MPa'])
    br = P2.branches(fake, {bed: str(log_path)}, common)[bed]
    load, relax = br['load'], br['relax']
    return dict(log=relpath(log_path), log_sha256=br['log_sha256'], log_bytes=br['log_bytes'], compress_start_step=br['s0'],
                stop_step=br['s_end'], n_compress_runs=br['n_runs'], plate_z0_um=br['plate_z0_um'], z_end_pred_um=br['z_end_pred_um'],
                z_end_mesh_um=br['z_end_mesh_um'], p_t0minus_MPa=load[-1][1], p_relax_first_MPa=relax[0][1], p_end_MPa=relax[-1][1],
                eps_sphere_fixed_pct=relax[-1][3], n_load_rows=len(load), n_relax_rows=len(relax),
                p_threshold_display_MPa=P2.P_CONTACT_MPA), load, relax


def codex_check(bed, vals):
    """알려진 침대 = Codex 독립 재계산 값과 출력 자릿수까지 같아야 한다."""
    out = {}
    for k, ref in CODEX.get(bed, {}).items():
        got = vals.get(k)
        if got is None:
            out[k] = dict(expected=ref[0] if isinstance(ref, tuple) else ref, got=None, match=False)
        elif isinstance(ref, tuple):
            txt, nd = ref
            ok = f'{got:.{nd}f}' == txt
            out[k] = dict(expected=txt, got=f'{got:.{nd}f}', got_full=got, match=ok)
        else:
            out[k] = dict(expected=ref, got=got, match=(got == ref))
    return out


# ───────────────────────────── 3. 웹앱 망 정지 파이프라인 ─────────────────────────────

def webapp_env(work):
    web = Path(work) / 'web'
    for k, sub in (('WEBAPP_UPLOAD_FOLDER', 'uploads'), ('WEBAPP_RESULTS_FOLDER', 'results'),
                   ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
        os.environ[k] = str(web / sub)
        os.makedirs(os.environ[k], exist_ok=True)
    os.environ['SUPABASE_URL'] = ''
    os.environ['SUPABASE_KEY'] = ''
    return web


def run_webapp(bed, paths):
    """`/upload` (Flask 시험 클라이언트) → run_pipeline(stop_after='network') — kg50 D3 칸 판정과 같은 호출."""
    cwd = os.getcwd()
    os.chdir(REPO / 'webapp')
    try:
        import app as A
        need(A.app.config['UPLOAD_FOLDER'] == os.environ['WEBAPP_UPLOAD_FOLDER'], '웹앱 업로드 폴더가 격리 폴더가 아니다')
        need(A.app.config['RESULTS_FOLDER'] == os.environ['WEBAPP_RESULTS_FOLDER'], '웹앱 결과 폴더가 격리 폴더가 아니다')
        c = A.app.test_client()
        files = [paths['deck'], paths['atom'], paths['contact'], paths['mesh']]
        handles = [open(f, 'rb') for f in files]
        try:
            data = {'case_name': CASE[bed], 'mode': 'auto', 'type_map': '', 'ps_ratio': 'P only', 'scale': '1000',
                    'files': [(h, Path(f).name) for h, f in zip(handles, files)]}
            r = c.post('/upload', data=data, content_type='multipart/form-data')
        finally:
            for h in handles:
                h.close()
        need(r.status_code == 200, f'/upload {r.status_code}: {r.get_data(as_text=True)[:300]}')
        cid = r.get_json()['case_id']
        meta = json.loads((Path(os.environ['WEBAPP_UPLOAD_FOLDER']) / cid / 'meta.json').read_text(encoding='utf-8'))
        with A.app.app_context():
            res = A.run_pipeline(cid, meta['mode'], meta['type_map'], int(meta.get('scale', 1000)),
                                 figures=False, auto_db=False, stop_after='network')
    finally:
        os.chdir(cwd)
    steps = [dict(step=s.get('step'), rc=s.get('rc')) for s in res.get('log', [])]
    need(res.get('status') == 'done' and res.get('stopped_after') == 'network',
         f'run_pipeline 상태 {res.get("status")!r} · 실패 {res.get("failed_stages")} · {steps}')
    rdir = Path(os.environ['WEBAPP_RESULTS_FOLDER']) / cid
    return cid, meta, rdir, dict(status=res['status'], stopped_after=res['stopped_after'], network_run_id=res.get('network_run_id'),
                                 stages=steps)


# ───────────────────────────── 4. 입자 · 접촉 · 점 출력의 집계 ─────────────────────────────

def _close(a, b, rtol=1e-9, atol=0.0):
    return a is not None and b is not None and abs(float(a) - float(b)) <= atol + rtol * abs(float(b))


def aggregates(rdir, fm, meta, plate_z_um_mesh):
    """기존 함수 · 기존 출력의 집계 — 새 정의 없음.  웹앱 전체 값과 맞지 않으면 멈춘다."""
    import analyze_contacts as AC
    import dem_analysis_core as DAC
    import coverage_physics_vs_hertzian as CPH
    import lhs_union_webapp as U
    import pandas as pd
    import type_map_resolve as TMR
    type_map = TMR.parse_map(meta['type_map'])
    am_t = {k for k, v in type_map.items() if 'AM' in v}
    se_t = {k for k, v in type_map.items() if v == 'SE'}
    need(len(am_t) == 1 and len(se_t) == 1, f'type_map {meta["type_map"]!r} — AM · SE 형식이 하나씩이 아니다')
    scale = float(meta.get('scale', 1000))
    atoms_raw, _ = AC.load_atoms_raw(str(rdir / 'atoms.csv'))
    contacts_raw, _ = AC.load_contacts_raw(str(rdir / 'contacts.csv'))
    plate_z, pz_src = DAC.get_plate_z(str(rdir), atoms_raw, scale)
    need(pz_src == 'mesh' and abs(plate_z * scale - plate_z_um_mesh) < 1e-9, f'판 높이 {plate_z} ({pz_src}) ≠ 끝 mesh')
    box_x, box_y = DAC._get_box_xy(str(rdir))
    chk = {}

    # 4a. 접촉별 겹침 비율 (calc_overlap_ratio 와 같은 식) · AM 별 AM–SE 접촉 수 · 상대 SE
    ov = DAC.calc_overlap_ratio(atoms_raw, contacts_raw)
    chk['overlap_mean_vs_webapp'] = _close(ov['mean'], fm['overlap_mean'], rtol=1e-12)
    am_ids = sorted(a for a, v in atoms_raw.items() if v['type'] in am_t)
    se_ids = sorted(a for a, v in atoms_raw.items() if v['type'] in se_t)
    n_amse = {a: 0 for a in am_ids}
    max_ratio = {a: 0.0 for a in am_ids}          # δ / min(r₁, r₂) — calc_overlap_ratio 의 접촉별 식
    max_ratio_sum = {a: 0.0 for a in am_ids}      # δ / (r₁ + r₂) — Zhou 2025 카드의 "두 입자 반경합 대비" (같은 δ · 정규화만 다름)
    partners = {a: set() for a in am_ids}
    ratios_all, ratios_amse, ratios_amse_sum = [], [], []
    for c in contacts_raw:
        i1, i2 = c['id1'], c['id2']
        if i1 not in atoms_raw or i2 not in atoms_raw:
            continue
        delta = abs(c.get('delta', 0))
        r = rs = None
        if delta > 0:
            r_eff = min(atoms_raw[i1]['radius'], atoms_raw[i2]['radius'])
            if r_eff > 0:
                r = delta / r_eff * 100
                ratios_all.append(r)
                rs = delta / (atoms_raw[i1]['radius'] + atoms_raw[i2]['radius']) * 100
        t1, t2 = atoms_raw[i1]['type'], atoms_raw[i2]['type']
        am = i1 if (t1 in am_t and t2 in se_t) else (i2 if (t2 in am_t and t1 in se_t) else None)
        if am is None:
            continue
        se = i2 if am == i1 else i1
        n_amse[am] += 1
        partners[am].add(se)
        if r is not None:
            ratios_amse.append(r)
            ratios_amse_sum.append(rs)
            max_ratio[am] = max(max_ratio[am], r)
            max_ratio_sum[am] = max(max_ratio_sum[am], rs)
    chk['overlap_mean_recomputed'] = _close(float(np.mean(ratios_all)), ov['mean'], rtol=1e-12)
    chk['am_se_cn_mean'] = _close(float(np.mean([n_amse[a] for a in am_ids])), fm['am_se_cn_mean'], rtol=1e-12)
    thr, thr_sum = {}, {}
    for T in OVERLAP_THRESHOLDS:
        k = sum(1 for a in am_ids if n_amse[a] > 0 and max_ratio[a] > T)
        thr[f'{T:g}'] = dict(n_am=k, frac_pct=100.0 * k / len(am_ids))
        k2 = sum(1 for a in am_ids if n_amse[a] > 0 and max_ratio_sum[a] > T)
        thr_sum[f'{T:g}'] = dict(n_am=k2, frac_pct=100.0 * k2 / len(am_ids))
    amse_arr = np.array(ratios_amse)
    amse_sum_arr = np.array(ratios_amse_sum)

    # 4b. SE 망과 연결된 AM (연결성 기준) — calc_ionic_active_am 과 같은 규칙: 위쪽에 닿는 SE 성분 (percolation_sets.json) 과 접촉한 AM
    ps = json.loads((rdir / 'percolation_sets.json').read_text(encoding='utf-8'))
    top_reach = {int(x) for x in ps['top_reachable']}
    chk['top_reachable_pct'] = _close(100.0 * len(top_reach) / len(se_ids), fm['top_reachable_pct'], rtol=1e-12)
    connected = {a: bool(partners[a] & top_reach) for a in am_ids}
    chk['se_connected_am_pct'] = _close(100.0 * sum(connected.values()) / len(am_ids), fm['ionic_active_pct'], rtol=1e-12)

    # 4c. AM 별 피복 (Hertz 계열 = coverage_per_am.csv) · AM–SE 계면 면적 · 합집합 cap 피복 (union_coverage_bed 의 AM 별 값)
    cpa = pd.read_csv(rdir / 'coverage_per_am.csv')
    cpa_ids = [int(x) for x in cpa['am_id']]
    need(sorted(cpa_ids) == am_ids, 'coverage_per_am.csv 의 AM id ≠ atoms.csv')
    cov_h = dict(zip(cpa_ids, cpa['coverage_hertzian_pct'].astype(float)))
    area_h = dict(zip(cpa_ids, cpa['A_AM_SE_hertzian_um2'].astype(float)))
    am_lbl = type_map[next(iter(am_t))]
    chk['coverage_hertz_mean'] = _close(float(np.mean(list(cov_h.values()))), fm[f'coverage_{am_lbl}_mean'], atol=1e-3, rtol=0)
    tot_area = fm[f'area_{am_lbl}_SE_total']
    chk['area_am_se_total'] = _close(float(sum(area_h.values())), tot_area, atol=len(am_ids) * 5e-5, rtol=0)
    atoms_df = pd.read_csv(rdir / 'atoms.csv')
    contacts_df = pd.read_csv(rdir / 'contacts.csv', low_memory=False)
    box, why = CPH.read_box_xy(rdir)
    ukeys, uper = CPH.union_coverage_bed(atoms_df, contacts_df, type_map, scale=scale, box_xy=box, box_reason=why)
    need(ukeys.get('coverage_status_physics_union') == 'ok', f'union_coverage_bed 상태 {ukeys.get("coverage_status_physics_union")!r}')
    chk['coverage_physics_union_mean'] = (ukeys[f'coverage_{am_lbl}_mean_physics_union'] == fm[f'coverage_{am_lbl}_mean_physics_union'])
    cov_u = {int(k): (None if v is None else float(v)) for k, v in uper.items()}

    # 4d. Love–Weber 입자 응력 (같은 함수 · return_arrays) — 웹앱 CV 와 대조 · 벽 · 판 접촉 입자 = 함수의 nowall 규칙으로 표지
    lw = DAC.calc_love_weber_stress(atoms_raw, contacts_raw, type_map, plate_z, box_x=box_x, box_y=box_y,
                                    plate_z_source=pz_src, return_arrays=True)
    need(lw['status'] == 'OK', f'Love–Weber 상태 {lw["status"]}')
    chk['lw_cv_vs_webapp'] = _close(lw['vm_cv'], fm['stress_cv_lw'], rtol=1e-12)
    lw_vm = dict(zip(lw['ids'], np.asarray(lw['arrays_vm'], dtype=float) * SIM_PA_TO_MPA))
    z_um = {a: atoms_raw[a]['z'] * scale for a in atoms_raw}
    r_um = {a: atoms_raw[a]['radius'] * scale for a in atoms_raw}
    H = plate_z * scale
    wall = {a: (z_um[a] - r_um[a] < 0.0) or (z_um[a] + r_um[a] > H) for a in atoms_raw}

    # 4e. 국소 공극률 (정확 합집합) — calc_porosity_union_exact 와 같은 씨앗 · 같은 점 → 점의 공극 표지를 z 로 묶는다
    ids = sorted(atoms_raw)
    X = np.array([[atoms_raw[i]['x'], atoms_raw[i]['y'], atoms_raw[i]['z']] for i in ids], dtype=float)
    R = np.array([atoms_raw[i]['radius'] for i in ids], dtype=float)
    notSE = np.zeros(len(ids), dtype=bool)
    lx, ly = float(box_x), float(box_y)
    mc_n = int(fm['union_exact_mc_n'])
    seed = zlib.crc32(f'{len(ids)}:{plate_z:.9g}:{lx:.9g}:{ly:.9g}:{float(R.sum()):.9g}'.encode())
    need(seed == fm['union_exact_mc_seed'], f'몬테카를로 씨앗 {seed} ≠ 웹앱 {fm["union_exact_mc_seed"]}')
    rng = np.random.default_rng(seed)
    edges_sim = np.linspace(0.0, plate_z, N_ZBINS + 1)
    n_all = np.zeros(N_ZBINS, dtype=np.int64)
    n_void = np.zeros(N_ZBINS, dtype=np.int64)
    done = void_total = 0
    while done < mc_n:
        m = min(U.MC_CHUNK, mc_n - done)
        Q = rng.random((m, 3)) * np.array([lx, ly, plate_z])
        cs, ca = U.coverage(X, R, notSE, 0.0, lx, 0.0, ly, Q)
        v = ~cs & ~ca
        void_total += int(v.sum())
        b = np.clip(np.searchsorted(edges_sim, Q[:, 2], side='right') - 1, 0, N_ZBINS - 1)
        n_all += np.bincount(b, minlength=N_ZBINS)
        n_void += np.bincount(b[v], minlength=N_ZBINS)
        done += m
    chk['union_exact_total_vs_webapp'] = (100.0 * void_total / mc_n == fm['porosity_union_exact_pct'])

    # 4f. z 구간 표 (중심 z 로 묶음)
    edges = edges_sim * scale
    zrows = []
    for k in range(N_ZBINS):
        lo, hi = edges[k], edges[k + 1]
        inb = (lambda a: lo <= z_um[a] < hi) if k < N_ZBINS - 1 else (lambda a: lo <= z_um[a] <= hi)
        am_b = [a for a in am_ids if inb(a)]
        se_b = [a for a in se_ids if inb(a)]
        p = n_void[k] / n_all[k]
        row = dict(bin=k, z_lo_um=lo, z_hi_um=hi, z_mid_um=0.5 * (lo + hi), n_mc=int(n_all[k]),
                   por_union_pct=100.0 * p, por_union_se_pct=100.0 * math.sqrt(p * (1 - p) / n_all[k]),
                   am_n=len(am_b), am_connected_pct=(100.0 * sum(connected[a] for a in am_b) / len(am_b)) if am_b else None)
        for ph, grp in (('am', am_b), ('se', se_b)):
            vals = np.array([lw_vm[a] for a in grp if not wall[a]])
            row[f'lw_{ph}_n'] = int(len(vals))
            row[f'lw_{ph}_wall_excluded'] = int(sum(1 for a in grp if wall[a]))
            for q, nm in ((50, 'median'), (25, 'q25'), (75, 'q75')):
                row[f'lw_{ph}_{nm}_MPa'] = float(np.percentile(vals, q)) if len(vals) else None
        zrows.append(row)

    # 4g. AM 하나당 표
    per_am = []
    for a in am_ids:
        per_am.append(dict(am_id=a, z_um=z_um[a], n_am_se=n_amse[a], area_am_se_um2=area_h[a], coverage_hertz_pct=cov_h[a],
                           coverage_physics_union_pct=cov_u.get(a), max_overlap_am_se_pct=max_ratio[a],
                           max_overlap_am_se_sum_pct=max_ratio_sum[a], se_connected=int(connected[a]),
                           lw_vm_MPa=lw_vm[a], wall_touch=int(wall[a])))

    def dist(xs):
        xs = np.asarray(xs, dtype=float)
        return dict(n=int(xs.size), mean=float(xs.mean()), std=float(xs.std()), median=float(np.median(xs)),
                    p10=float(np.percentile(xs, 10)), p90=float(np.percentile(xs, 90)), min=float(xs.min()), max=float(xs.max()))
    lw_phase = {}
    for ph, grp in (('AM', am_ids), ('SE', se_ids)):
        vals = [lw_vm[a] for a in grp if not wall[a]]
        lw_phase[ph] = dict(nowall=dist(vals), n_wall_excluded=int(sum(1 for a in grp if wall[a])))
    summ = dict(
        overlap_threshold=dict(definition='δ / min(r₁, r₂) × 100 (calc_overlap_ratio 의 접촉별 식) · AM 하나에 AM–SE 접촉 중 문턱 초과가 하나라도 있으면 셈 · '
                               '분모 = 전체 AM', thresholds_pct=list(OVERLAP_THRESHOLDS), by_threshold=thr,
                               am_se_contact_ratio=dist(amse_arr) if amse_arr.size else None, all_contacts=ov,
                               definition_card='δ / (r₁ + r₂) × 100 — Zhou 2025 카드 (tailored_cathode_microstructure_low_pressure_assb) 의 '
                                               '"두 입자 반경합 대비 overlap" · 같은 접촉 δ · 정규화만 다름 (새 물리량 아님)',
                               by_threshold_card=thr_sum,
                               am_se_contact_ratio_card=dist(amse_sum_arr) if amse_sum_arr.size else None),
        per_am=dict(n_am_se=dist([n_amse[a] for a in am_ids]), area_am_se_um2=dist(list(area_h.values())),
                    coverage_hertz_pct=dist(list(cov_h.values())),
                    coverage_physics_union_pct=dist([v for v in cov_u.values() if v is not None]),
                    am_surface_um2=4.0 * math.pi * (atoms_raw[am_ids[0]]['radius'] * scale) ** 2),
        se_connected=dict(n_am=len(am_ids), n_connected=int(sum(connected.values())),
                          pct=100.0 * sum(connected.values()) / len(am_ids)),
        love_weber=dict(status=lw['status'], vm_cv=lw['vm_cv'], type_stress_ratio={k: v['ratio'] for k, v in lw['type_stress'].items()},
                        by_phase_MPa=lw_phase, wall_rule='z − r < 0 (바닥) 또는 z + r > 판 높이 (판) — calc_love_weber_stress 의 nowall 규칙 · '
                        '결측 벽 힘을 복원한 값 아님', quantity=lw['quantity'],
                        unit='MPa (덱 단위 Pa × 1e-3 · 덱 머리 P×0.001 규약)'),
        zbins=dict(n=N_ZBINS, rule='바닥 z = 0 → 판 높이 같은 폭 · 입자 = 중심 z · 공극 = 정확 합집합 몬테카를로 점의 z',
                   mc_n=mc_n, mc_seed=seed),
    )
    need(all(v is True for v in chk.values()), f'집계 ↔ 웹앱 대조 실패: {[k for k, v in chk.items() if v is not True]}')
    return summ, per_am, zrows, chk


# ───────────────────────────── 5. 단면 · OVITO 사본 ─────────────────────────────

def section_rows(atoms, d):
    import make_figs_p1 as P1
    y0_um = d['box_y_um'] / 2
    rows = P1.section_circles(atoms, y0_um / src.LEN_SIM_TO_UM, d['box_x_um'] / src.LEN_SIM_TO_UM, d['box_y_um'] / src.LEN_SIM_TO_UM)
    return y0_um, [dict(phase='AM' if t == src.TYPE_AM else 'SE', particle_id=pid, x_um=x * src.LEN_SIM_TO_UM, z_um=z * src.LEN_SIM_TO_UM,
                        section_radius_um=rr * src.LEN_SIM_TO_UM, periodic_shift_um=sh * src.LEN_SIM_TO_UM) for pid, t, x, z, rr, sh in rows]


def write_ovito(bed, atoms, d, plate_z_um, step, out_dir):
    """확장 XYZ (µm) — species = 상 이름 (AM · SE → OVITO 입자 형식) · dump_type = 덤프 type (1 · 3) · gzip (mtime 0 · 같은 바이트)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    order = np.argsort(atoms['id'])
    head = (f'Lattice="{d["box_x_um"]:g} 0 0 0 {d["box_y_um"]:g} 0 0 0 {plate_z_um:.6f}" Origin="0 0 0" pbc="T T F" '
            f'Properties=species:S:1:pos:R:3:radius:R:1:id:I:1:dump_type:I:1 '
            f'case={CASE[bed]} step={step} units=um state=fixed_plate_relaxation_end cell_z=end_mesh_plate')
    buf = io.StringIO()
    buf.write(f'{len(order)}\n{head}\n')
    for k in order:
        t = int(atoms['type'][k])
        ph = 'AM' if t == src.TYPE_AM else 'SE'
        buf.write(f'{ph} {atoms["x"][k] * 1000:.6f} {atoms["y"][k] * 1000:.6f} {atoms["z"][k] * 1000:.6f} '
                  f'{atoms["r"][k] * 1000:.6g} {int(atoms["id"][k])} {t}\n')
    raw = buf.getvalue().encode('ascii')
    p = out_dir / f'{bed}_end_{step}_um.xyz.gz'
    bio = io.BytesIO()
    with gzip.GzipFile(filename='', mode='wb', fileobj=bio, mtime=0, compresslevel=9) as gz:
        gz.write(raw)
    p.write_bytes(bio.getvalue())
    return dict(file=relpath(p), bytes=p.stat().st_size, sha256=sha256_path(p), raw_sha256=sha256_bytes(raw), n=int(len(order)),
                columns=['species', 'x_um', 'y_um', 'z_um', 'radius_um', 'id', 'dump_type'])


# ───────────────────────────── 6. 쓰기 ─────────────────────────────

def write_csv(path, rows, cols=None):
    cols = cols or (list(rows[0].keys()) if rows else [])
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(cols)
        for r in rows:
            w.writerow(['' if r.get(c) is None else (f'{r[c]:.9g}' if isinstance(r[c], float) else r[c]) for c in cols])


def pick(fm, *keys):
    return {k: fm.get(k) for k in keys}


def run_bed(bed, tgz, log, prefix=None, record=None, member_record=None, work=None, keep_work=False):
    need(bed in CASE, f'모르는 침대 {bed!r} (가능: {", ".join(BED_ORDER)})')
    need(log or bed not in CODEX, f'{bed}: Codex 대조 침대는 로그가 필요하다 (--log)')
    case = CASE[bed]
    prefix = f'{case}/' if prefix is None else prefix
    known = RECORDS.get(bed, {})
    if record is None and known and relpath(tgz) == known['tgz']:
        record, member_record = REPO / known['record'], (REPO / known['member_record']) if known.get('member_record') else None
    work = Path(work) if work else Path(tempfile.mkdtemp(prefix=f'kg50y4d2_{bed}_'))
    work.mkdir(parents=True, exist_ok=True)
    need(not any(work.iterdir()), f'작업 폴더 {work} 가 비어 있지 않다 (새 빈 폴더만)')
    print(f'[{bed}] work = {work}', flush=True)
    try:
        blobs, paths, info = read_end_set(bed, tgz, prefix, work, record, member_record)
        d, deck_info = deck_check(bed, blobs['deck'])
        atoms = src.parse_atom_dump(blobs['atom'])
        need(atoms['step'] == info['end_step'], 'atom step ≠ 끝 세트 step')
        plate_z_sim = src.parse_mesh_z(blobs['mesh'])
        plate_z_um = plate_z_sim * src.LEN_SIM_TO_UM
        n_am = int((atoms['type'] == src.TYPE_AM).sum())
        n_se = int((atoms['type'] == src.TYPE_SE).sum())
        need(n_am + n_se == atoms['n'], 'AM · SE 밖의 type')
        need(np.all(atoms['r'][atoms['type'] == src.TYPE_AM] == d['r_am_sim']) and np.all(atoms['r'][atoms['type'] == src.TYPE_SE] == d['r_se_sim']),
             '덤프 반지름 ≠ 덱 (단분산)')
        need(d['am_gate'][0] <= n_am <= d['am_gate'][1] and d['se_gate'][0] <= n_se <= d['se_gate'][1], '끝 상태 상별 수가 덱 검사 구간 밖')
        v_solid, eps = eps_sphere(atoms, d, plate_z_um)
        print(f'[{bed}] step {info["end_step"]} · AM {n_am} · SE {n_se} · 판 {plate_z_um:.6f} µm · ε_sphere {eps:.9f} %', flush=True)
        curve = load = relax = None
        if log:
            curve, load, relax = log_curve(bed, log, atoms, plate_z_sim, info['end_step'], d)
            need(abs(curve['eps_sphere_fixed_pct'] - eps) < 1e-9, '로그 판 고정 ε ≠ 끝 덤프 ε_sphere')
            print(f'[{bed}] 로그: 정지 step {curve["stop_step"]} · t=0⁻ {curve["p_t0minus_MPa"]:.5f} · 이완 첫 {curve["p_relax_first_MPa"]:.5f} · '
                  f'끝 {curve["p_end_MPa"]:.5f} MPa', flush=True)
        vals = dict(eps_sphere_pct=eps, end_step=info['end_step'], n_am=n_am, n_se=n_se)
        if curve:
            vals.update(p_end_MPa=curve['p_end_MPa'], stop_step=curve['stop_step'], p_t0minus_MPa=curve['p_t0minus_MPa'],
                        p_relax_first_MPa=curve['p_relax_first_MPa'])
        cx = codex_check(bed, vals) if bed in CODEX else {}
        if cx and not all(v['match'] for v in cx.values()):
            raise RunError('Codex 값과 다름 — 멈춤: ' + json.dumps({k: v for k, v in cx.items() if not v['match']}, ensure_ascii=False))
        # 웹앱
        webapp_env(work)
        cid, meta, rdir, pipe = run_webapp(bed, paths)
        print(f'[{bed}] run_pipeline {pipe["status"]} · {cid}', flush=True)
        fm = json.loads((rdir / 'full_metrics.json').read_text(encoding='utf-8'))
        prov = json.loads((rdir / 'network_provenance.json').read_text(encoding='utf-8'))
        import kg50_d3_cell_verdict as V
        import tau_flux as TF
        ex = V.extract(str(rdir), meta)
        row = TF.case_row(str(rdir))
        #  같은 식 · 다른 합산 순서 (덤프 단위 ↔ µm) — 차이 = 부동소수 반올림뿐 (D3 실측 2.3e-11 %p)
        need(_close(fm['porosity'], eps, rtol=1e-9), f'웹앱 porosity {fm["porosity"]} ≠ 독립 ε_sphere {eps}')
        need(abs(fm['thickness_um'] - plate_z_um) < 1e-9, '웹앱 두께 ≠ 끝 mesh')
        summ, per_am, zrows, chk = aggregates(rdir, fm, meta, plate_z_um)
        am_lbl = ex['am_phase']
        y0_um, sec = section_rows(atoms, d)
        ov = write_ovito(bed, atoms, d, plate_z_um, info['end_step'], OVITO)
        out = DATA / bed
        out.mkdir(parents=True, exist_ok=True)
        write_csv(out / f'per_am_{bed}.csv', per_am)
        write_csv(out / f'zprof_{bed}.csv', zrows)
        write_csv(out / f'section_{bed}.csv', sec)
        if curve:
            crow = [dict(branch='loading', step=s, plate_pressure_MPa=p, plate_gap_um=z, eps_sphere_pct=e) for s, p, z, e in load]
            crow += [dict(branch='fixed_height_relaxation', step=s, plate_pressure_MPa=p, plate_gap_um=z, eps_sphere_pct=e) for s, p, z, e in relax]
            write_csv(out / f'curve_{bed}.csv', crow)
        metrics = dict(
            eps_sphere_pct=eps, eps_sphere_webapp_pct=fm['porosity'], eps_union_exact_pct=fm['porosity_union_exact_pct'],
            eps_union_exact_se_pct=fm['porosity_union_exact_se_pct'], eps_union_pair_pct=fm['porosity_union'],
            overlap_fraction_pct=fm['overlap_fraction_pct'], wall_overhang_over_Vbox_pct=fm['wall_overhang_over_Vbox_pct'],
            plate_z_um=plate_z_um, v_sphere_sum_um3=v_solid, thickness_mass_conserving_um=fm['thickness_mass_conserving_um'],
            phi_se_mass_conserving=fm['phi_se_mass_conserving'], phi_am_mass_conserving=fm['phi_am_mass_conserving'],
            p_end_MPa=curve['p_end_MPa'] if curve else None, p_t0minus_MPa=curve['p_t0minus_MPa'] if curve else None,
            p_relax_first_MPa=curve['p_relax_first_MPa'] if curve else None,
            am_se_cn_mean=fm['am_se_cn_mean'], am_se_cn_std=fm['am_se_cn_std'], am_se_cn_median=fm['am_se_cn_median'],
            se_se_cn_mean=fm['se_se_cn'], se_se_cn_std=fm['se_se_cn_std'], am_am_cn_mean=fm['am_am_cn'],
            coverage_hertz_pct=fm[f'coverage_{am_lbl}_mean'], coverage_hertz_std=fm[f'coverage_{am_lbl}_std'],
            coverage_physics_union_pct=fm[f'coverage_{am_lbl}_mean_physics_union'],
            coverage_physics_union_std=fm[f'coverage_{am_lbl}_std_physics_union'],
            area_am_se_total_um2=fm[f'area_{am_lbl}_SE_total'], area_am_se_n_contacts=fm[f'area_{am_lbl}_SE_n'],
            area_am_se_per_contact_mean_um2=fm[f'area_{am_lbl}_SE_mean'],
            area_am_se_per_am_mean_um2=summ['per_am']['area_am_se_um2']['mean'],
            area_am_se_per_am_median_um2=summ['per_am']['area_am_se_um2']['median'],
            percolation_pct=fm['percolation_pct'], top_reachable_pct=fm['top_reachable_pct'],
            se_connected_am_pct=fm['ionic_active_pct'], am_ionic_isolated_pct=fm['am_ionic_isolated_pct'],
            tau_geo_all=fm['tortuosity_all_recommended'], tau_geo_all_mean=fm['tortuosity_all_mean'],
            tau_geo_all_median=fm['tortuosity_all_median'], tau_geo_all_std=fm['tortuosity_all_std'], tau_geo_all_n=fm['tortuosity_all_n'],
            f_ion_hertz=row['f_ion_hertz'], tau2_ion_hertz=row['tau2_ion_hertz'], ion_net_status_hertz=row['ion_net_status_hertz'],
            f_ion_physics=row['f_ion_physics'], tau2_ion_physics=row['tau2_ion_physics'], ion_net_status_physics=row['ion_net_status_physics'],
            phi_basis=row['phi_basis'], L_basis=row['L_basis'], ion_sigma0_solver_mScm=row['ion_sigma0_mScm'],
            sigma_ion_hertz_solver_mScm=fm['sigma_full_mScm'],
            constriction_power_share_ion_hertz=fm['constriction_power_share_ion_hertz'],
            overlap_ratio_mean_pct=fm['overlap_mean'], overlap_ratio_max_pct=fm['overlap_max'], overlap_pct_above_5=fm['overlap_pct_above_5'],
            **{f'am_frac_overlap_gt_{k}_pct': v['frac_pct'] for k, v in summ['overlap_threshold']['by_threshold'].items()},
            **{f'am_frac_overlap_card_gt_{k}_pct': v['frac_pct'] for k, v in summ['overlap_threshold']['by_threshold_card'].items()},
            am_se_overlap_ratio_median_pct=summ['overlap_threshold']['am_se_contact_ratio']['median'],
            am_se_overlap_ratio_card_median_pct=summ['overlap_threshold']['am_se_contact_ratio_card']['median'],
            lw_status=fm['stress_lw_status'], lw_cv_pct=fm['stress_cv_lw'],
            lw_ratio_am=fm.get(f'stress_ratio_{am_lbl}_lw'), lw_ratio_se=fm.get('stress_ratio_SE_lw'),
            lw_am_nowall_median_MPa=summ['love_weber']['by_phase_MPa']['AM']['nowall']['median'],
            lw_se_nowall_median_MPa=summ['love_weber']['by_phase_MPa']['SE']['nowall']['median'],
        )
        rec = dict(
            schema=SCHEMA, bed=bed, case=case, d50_se_um=d['d50_se_um'], d_am_um=d['d_am_um'],
            frame=dict(state='판 고정 이완 끝 (atom · contact · mesh 같은 step)', end_step=info['end_step'],
                       same_step_set=info['same_step_set'], pressure_reached_frame='NOT_AVAILABLE (자료 없음 — 압축 정지 step 에 덤프 없음)',
                       target_pressure_MPa=d['target_MPa'], note='이완 끝 프레임을 300 MPa 상태로 부르지 않는다'),
            inventory=dict(n_am=n_am, n_se=n_se, n_am_plan=d['n_am_plan'], n_se_plan=d['n_se_plan']),
            metrics=metrics,
            verdict_extract=dict(values=ex['values'], notes=ex['notes'], am_phase=am_lbl, code_sha=ex['code_sha'],
                                 network_run_id=ex['network_run_id'], ion_net_electrode_hertz=ex['ion_net_electrode_hertz'],
                                 ion_net_area_rule_hertz=ex['ion_net_area_rule_hertz'], f_ion_hertz=ex['f_ion_hertz']),
            tau_flux_row={k: v for k, v in row.items() if k != 'case'},
            aggregates=summ, aggregate_checks=chk, codex_check=cx, compaction=curve, section=dict(y0_um=y0_um, n_rows=len(sec)),
            ovito=ov,
            provenance=dict(end_set=info, deck=deck_info, network_provenance=prov, pipeline=pipe, webapp_case_id=cid, meta_type_map=meta['type_map'],
                            git=git_state(), tool_files={f: sha256_path(REPO / f) for f in TOOL_FILES}, tool_functions=list(TOOL_FUNCTIONS),
                            env=dict(python=platform.python_version(), numpy=np.__version__)),
        )
        (out / f'metrics_{bed}.json').write_text(json.dumps(rec, ensure_ascii=False, indent=1, default=float) + '\n', encoding='utf-8')
        print(f'[{bed}] → {relpath(out)}/metrics_{bed}.json · 집계 대조 {sum(chk.values())}/{len(chk)} · Codex {cx and all(v["match"] for v in cx.values())}',
              flush=True)
        return rec
    finally:
        if not keep_work:
            shutil.rmtree(work, ignore_errors=True)


# ───────────────────────────── 7. 병합 ─────────────────────────────

MERGE_COLS = ('bed', 'case', 'status', 'd50_se_um', 'end_step', 'n_am', 'n_se', 'plate_z_um', 'eps_sphere_pct', 'eps_union_exact_pct',
              'p_end_MPa', 'p_t0minus_MPa', 'am_se_cn_mean', 'se_se_cn_mean', 'am_am_cn_mean', 'coverage_hertz_pct',
              'coverage_physics_union_pct', 'area_am_se_per_am_mean_um2', 'area_am_se_per_contact_mean_um2', 'f_ion_hertz', 'tau2_ion_hertz',
              'f_ion_physics', 'tau2_ion_physics', 'tau_geo_all', 'se_connected_am_pct', 'percolation_pct', 'top_reachable_pct',
              'constriction_power_share_ion_hertz', 'overlap_ratio_mean_pct', 'am_frac_overlap_gt_0_pct', 'am_frac_overlap_gt_2_pct',
              'am_frac_overlap_gt_5_pct', 'am_frac_overlap_gt_10_pct', 'am_frac_overlap_card_gt_0_pct', 'am_frac_overlap_card_gt_2_pct',
              'am_frac_overlap_card_gt_5_pct', 'am_frac_overlap_card_gt_10_pct', 'am_se_overlap_ratio_median_pct',
              'am_se_overlap_ratio_card_median_pct', 'lw_cv_pct', 'lw_ratio_am', 'lw_ratio_se', 'lw_am_nowall_median_MPa',
              'lw_se_nowall_median_MPa', 'phi_se_mass_conserving', 'code_sha', 'tgz_sha256')


def load_beds():
    out = {}
    for bed in BED_ORDER:
        p = DATA / bed / f'metrics_{bed}.json'
        if p.exists():
            rec = json.loads(p.read_text(encoding='utf-8'))
            need(rec.get('schema') == SCHEMA and rec.get('bed') == bed, f'{p}: schema · 침대 이름이 다르다')
            out[bed] = rec
    return out


def merge():
    beds = load_beds()
    decks = {src.bed_label(b): b for b in src.load_all(with_end=False)[0]}
    rows = []
    for bed in BED_ORDER:
        r = {c: None for c in MERGE_COLS}
        r.update(bed=bed, case=CASE[bed], d50_se_um=decks[bed]['deck_vals']['d50_se_um'])
        if bed in beds:
            rec = beds[bed]
            m = rec['metrics']
            r.update({k: m.get(k) for k in MERGE_COLS if k in m})
            r.update(status='ok', end_step=rec['frame']['end_step'], n_am=rec['inventory']['n_am'], n_se=rec['inventory']['n_se'],
                     code_sha=rec['provenance']['network_provenance'].get('code_sha'), tgz_sha256=rec['provenance']['end_set']['tgz_sha256'])
        else:
            r['status'] = '결과 대기'
        rows.append(r)
    write_csv(HERE / 'metrics_all.csv', rows, list(MERGE_COLS))
    print('metrics_all.csv:', ', '.join(f'{r["bed"]}={r["status"]}' for r in rows))
    return rows


def selftest():
    """끝 세트 소비자 시험 (K50Y4-01 · 같은 step 세트만 · 결손 · 엇갈림 거부) — 합성 묶음 (가짜 덤프 · 리포 D3 덱)."""
    case = CASE['D3']
    deck = src.rp(next(x for x in src.BEDS if x['case'] == case)['deck']).read_bytes()

    def dump(step, extra=''):
        return f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n0\n{extra}'.encode()

    def tgz(path, members):
        with tarfile.open(path, 'w:gz') as tf:
            for name, blob in members.items():
                ti = tarfile.TarInfo(name)
                ti.size = len(blob)
                tf.addfile(ti, io.BytesIO(blob))
    S = 4575002
    base = {f'{case}/input_{case}.liggghts': deck, f'{case}/post_{case}/atom_end_{S}.liggghts': dump(S),
            f'{case}/post_{case}/contact_end_{S}.liggghts': dump(S), f'{case}/post_{case}/mesh_end_{S}.stl': b'solid x\nendsolid x\n'}
    cases = [
        ('같은 step 세트 (양성)', base, True),
        ('덱 없음 → 리포 덱 (양성)', {k: v for k, v in base.items() if 'input_' not in k}, True),
        ('contact 결손', {k: v for k, v in base.items() if 'contact_' not in k}, False),
        ('mesh 결손', {k: v for k, v in base.items() if 'mesh_' not in k}, False),
        ('contact step 다름', {**{k: v for k, v in base.items() if 'contact_' not in k},
                              f'{case}/post_{case}/contact_end_{S - 2}.liggghts': dump(S - 2)}, False),
        ('atom 둘', {**base, f'{case}/post_{case}/atom_end_{S - 100000}.liggghts': dump(S - 100000)}, False),
        ('머리 TIMESTEP ≠ 이름', {**base, f'{case}/post_{case}/atom_end_{S}.liggghts': dump(S - 1)}, False),
        ('덱 둘', {**base, f'other/input_{case}.liggghts': deck}, None),     # 접두 밖 = 무시 → 양성
        ('접두 밖 멤버만', {f'x/{k}': v for k, v in base.items()}, False),
    ]
    ok = 0
    with tempfile.TemporaryDirectory(prefix='kg50y4d2_selftest_') as td:
        for i, (name, mem, expect) in enumerate(cases):
            p = Path(td) / f'c{i}.tgz'
            tgz(p, mem)
            try:
                _b, _p, info = read_end_set('D3', p, f'{case}/', Path(td) / f'w{i}')
                got = True
            except RunError as e:
                got, info = False, str(e)
            want = True if expect is None else expect
            res = 'PASS' if got == want else 'FAIL'
            ok += res == 'PASS'
            print(f'  [{res}] {name} → {"수락" if got else "거부"}' + ('' if got else f' ({str(info)[:70]})'))
    print(f'selftest {ok}/{len(cases)}')
    return 0 if ok == len(cases) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('selftest')
    for name in ('run', 'add'):
        s = sub.add_parser(name)
        s.add_argument('--bed', required=True, choices=BED_ORDER)
        s.add_argument('--tgz', required=True, help='끝 세트 묶음 (atom_end · contact_end · mesh_end 같은 step + 덱)')
        s.add_argument('--log', default=None, help='LIGGGHTS 로그 (압밀 곡선 · 이완 끝 판 압력) — 없으면 그 칸 빈칸')
        s.add_argument('--prefix', default=None, help='묶음 안 침대 폴더 접두 (기본 <case>/)')
        s.add_argument('--record', default=None, help='묶음 · 멤버 sha256 기록 (README 표) — D2 · D3 는 자동')
        s.add_argument('--member-record', default=None, help='멤버 sha256 목록 (sha  ./path) — D3 는 자동')
        s.add_argument('--work', default=None, help='빈 작업 폴더 (기본 = 새 임시 폴더)')
        s.add_argument('--keep-work', action='store_true')
    sub.add_parser('merge')
    a = ap.parse_args(argv)
    if a.cmd == 'selftest':
        return selftest()
    try:
        if a.cmd in ('run', 'add'):
            run_bed(a.bed, a.tgz, a.log, a.prefix, a.record, a.member_record, a.work, a.keep_work)
        if a.cmd in ('merge', 'add'):
            merge()
        if a.cmd == 'add':
            import make_draft2_figs as F
            F.build_all()
    except RunError as e:
        print(f'STOP: {e}', file=sys.stderr)
        return 3
    return 0


if __name__ == '__main__':
    sys.exit(main())
