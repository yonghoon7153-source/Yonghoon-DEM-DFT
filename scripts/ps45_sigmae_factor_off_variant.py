#!/usr/bin/env python3
"""ps45 σ_e 보고 전용 실행 변형 — PC 크기 인자 끔 · 공통 기준값 4.1 mS/cm · 다섯 전자 망 진단 (Hertz H0 주 · Physics g2 등록 감도).

등록 (결과 전) = `docs/reviews/ps45_sigmae_factor_off_registration_20261013.md` · 근거 = Codex 10-13 판정
`docs/reviews/codex_review_ps45_sigmae_reporting_20261013.md` §3-3 · §4 (가′) · §8 · 원장 `PS45E-03` (예방 조건 — 실행 중 교체한 모형은 자기 manifest 를 가져야 한다).

무엇을 하나
  • 저장된 g2 배치의 케이스 입력 (`<inputs-root>/<case_id>/atoms.csv · contacts.csv · mesh_info.json · input_params.json` — 망 솔버 CLI 가 읽은 그 파일들) 을
    **읽기만** 하고, 케이스마다 전자 망 (AM–AM) 을 팔 넷으로 푼다 — `network_conductivity._run_all_networks` 의 전자 호출과 같은 인자
    (`run_decomposition(..., am_types, scale, plate_z, box_x, box_y, sigma_bulk, type_map, contact_mode, mode='electronic')` · ψ 배치 · 면적 규칙 = 모듈 기본):
        control_hertz_on   hertzian · PC 인자 켬 · σ 0.05     관문 — 저장 증서 q 재현 (입력 · 코드 결합 · 보고값 아님)
        main_hertz_off     hertzian · PC 인자 끔 · σ 0.0041   **주 값**
        control_physics_on physics  · PC 인자 켬 · σ 0.05     관문
        sens_physics_off   physics  · PC 인자 끔 · σ 0.0041   등록 감도
  • PC 인자 끔 = 실행 중 `network_conductivity.sigma_AM_relative` 를 상수 1 로 바꾸는 것 (파일은 그대로 · 끝나면 되돌린다 · 예외에도).
    기준값은 모듈 상수 (`SIGMA_AM_ELECTRONIC` = 0.05) 를 건드리지 않고 `sigma_bulk=` 인자로만 준다 (증서 `sigma_bulk_S_cm` = 0.0041 로 남는다).
  • 패치가 실제로 켜졌는지 = 합성 균일 반경 PC 만 망의 OFF/ON = 35/8 (실행 앞 · 뒤) · SC 만 = 1 (비트) · 실데이터 SC 만 (0:10) OFF = ON (비트) 관문.
  • 별도 출력 폴더 (새 빈 폴더 · 리포 · 입력 뿌리 · 배치 출력 · 웹앱 서빙 폴더 밖) 에 표 · 레코드 · 로그 · **manifest** 를 쓴다 — manifest 필수 칸이 하나라도 비면
    manifest.json 을 쓰지 않는다 (표 = `*.REFUSED.tsv` · `manifest.REFUSED.json`).

무엇을 하지 않나
  • 봉인 32 파일 · 생산 JSON · TSV · 상태 · code_fp · 웹앱 · 194 · 보충 20 · v1.3 을 바꾸지 않는다 · 이온 · 열 망을 풀지 않는다 · DEM 을 돌리지 않는다.
  • 섞인 침대를 배율 · 보간으로 채우지 않는다 · 결과를 보고 팔 · 기준값 · 케이스를 바꾸지 않는다 (등록 §1 · §2 가 상수로 박혀 있다 — CLI 로 못 바꾼다).

사용 (1저자 WSL — 등록 §5 명령 그대로)
    python3 scripts/ps45_sigmae_factor_off_variant.py --selftest
    python3 scripts/ps45_sigmae_factor_off_variant.py --check-only --inputs-root ~/ps45_network_g2_0801d4ceb/work/results --out ~/ps45_sigmae_factor_off_20261013
    python3 scripts/ps45_sigmae_factor_off_variant.py --inputs-root ~/ps45_network_g2_0801d4ceb/work/results --out ~/ps45_sigmae_factor_off_20261013
rc: 0 = 다섯 케이스 ok · manifest.json · 1 = manifest 는 썼지만 케이스 · 실행 문제 있음 (표에 상태) · 2 = 관문 거부 (아무것도 안 썼거나 REFUSED 표지).
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import datetime as _dt
import hashlib
import io
import json
import math
import os
import platform
import subprocess
import sys
import tarfile
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

SCHEMA = 'ps45_sigmae_factor_off_variant/v1'
KIND = 'report-only model variant'
REG_DOC = 'docs/reviews/ps45_sigmae_factor_off_registration_20261013.md'
TSV_REL = 'docs/data/ps45_r45_network_g2_20261007/network_cases.tsv'
ARCHIVE_REL = 'docs/data/ps45_r45_network_g2_20261007/raw/ps45_network_g2.tgz'
#: 등록 §3 G0 — 결과 전 고정 (CLI 로 못 바꾼다)
ARCHIVE_SHA256 = '076727a8f0f1e263349a9f50c4aca5afdb112b16c3b4193bc9f8c9573fcf608f'
EXPECTED_NC_SHA256 = 'da9ecfefd8dc4b84e222140e347e4a718381169f27c88bf56c71ec4a7c2749be'   # = 실행 핀 0801d4ceb 의 network_conductivity.py
EXPECTED_CODE_FP = 'e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71'     # 봉인 32 (run_network_194_parallel.code_fp)
REGISTERED_CASES = (('260925_000001_0bee25', '0:10'), ('260925_000448_bd85f9', '3:7'), ('260925_000513_123978', '5:5'),
                    ('260925_000559_082983', '7:3'), ('260922_222828_6e4ff6', '10:0'))
SIGMA_BASE_S_CM = 0.05      # 저장 g2 실행의 전자 기준값 (= network_conductivity.SIGMA_AM_ELECTRONIC)
SIGMA_REF_S_CM = 0.0041     # 4.1 mS/cm — 공통 기준값 (PC · SC 같음 · 조건부 지정 참조값)
SIGMA_REF_LABEL = ('4.1 mS/cm = 20 °C NMC811 소결 (SPS) 다결정 펠릿 문헌 (Wang 2018) 의 약 4 mS/cm 를 참고한 지정 참조값 · PC · SC 공통 · '
                   '조건부 (우리 입자 고유값 · PC/SC 실측값 아님)')
ARMS = (
    dict(name='control_hertz_on', contact_mode='hertzian', factor='on', sigma_S_cm=SIGMA_BASE_S_CM, role='gate'),
    dict(name='main_hertz_off', contact_mode='hertzian', factor='off', sigma_S_cm=SIGMA_REF_S_CM, role='main'),
    dict(name='control_physics_on', contact_mode='physics', factor='on', sigma_S_cm=SIGMA_BASE_S_CM, role='gate'),
    dict(name='sens_physics_off', contact_mode='physics', factor='off', sigma_S_cm=SIGMA_REF_S_CM, role='sensitivity'),
)
CONTROL_OF = {'hertzian': 'control_hertz_on', 'physics': 'control_physics_on'}
VARIANT_OF = {'hertzian': 'main_hertz_off', 'physics': 'sens_physics_off'}
INPUT_FILES = ('atoms.csv', 'contacts.csv', 'mesh_info.json', 'input_params.json')
CONTROL_Q_RTOL = 1e-9       # 대조 팔 q ↔ 저장 증서 q (같은 입력 · 같은 코드면 비트 같음이 기대 — 반올림 차 여유)
PROBE_RTOL = 1e-12          # 합성 PC 만 망 OFF/ON = 35/8
PC_RATIO = 35.0 / 8.0       # 1 / f_P(4.5 µm) — f = 1/(1+(4.5/2)^1.5) = 8/35
CASE_STATUSES = ('ok', 'inputs_refused', 'control_mismatch', 'error')
BATCH_SCHEMAS = ('webapp_network_batch/v1',)
SERVED_ENV = ('WEBAPP_UPLOAD_FOLDER', 'WEBAPP_RESULTS_FOLDER', 'WEBAPP_ARCHIVE_FOLDER')
THREAD_ENV = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS')
MANIFEST_REQUIRED = ('schema', 'kind', 'registration', 'wrapper', 'git', 'code', 'environment', 'sigma_ref_S_cm', 'sigma_ref_label',
                     'sigma_base_S_cm', 'arms', 'factor_patch', 'archive', 'tsv', 'inputs_root', 'out', 'cases', 'factor_probe',
                     'outputs', 'production_inputs_unchanged', 'run_status', 'run_problems', 'created_utc', 'created_kst')
FACTOR_PATCH = dict(target='network_conductivity.sigma_AM_relative', replacement='constant 1.0 (모든 AM 입자 σ_rel = 1 · PC 크기 인자 끔)',
                    scope='factor=off 팔 안에서만 · 끝나면 원 함수로 되돌림 (예외 포함)', source_files_modified=False,
                    note='원 코드 파일 불변 · 실행 모형 변경 — report-only model variant (원 생산물과 같은 모형이 아니다 · PS45E-03)')


class Refuse(Exception):
    """관문 거부 — 아무것도 쓰지 않고 rc 2."""


# ── 작은 도우미 ─────────────────────────────────────────────────────────────────────────────────────────

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def json_safe(v):
    """numpy · 비유한 실수 · 튜플 → JSON 안전 (NaN · inf = None)."""
    if isinstance(v, dict):
        return {str(k): json_safe(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, set)):
        return [json_safe(x) for x in (sorted(v) if isinstance(v, set) else v)]
    if v is None or isinstance(v, (bool, str)):
        return v
    try:
        import numpy as np
        if isinstance(v, np.bool_):
            return bool(v)
        if isinstance(v, np.integer):
            return int(v)
        if isinstance(v, np.floating):
            v = float(v)
    except ImportError:                                   # pragma: no cover
        pass
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return v if math.isfinite(v) else None
    return str(v)


def now_stamps():
    t = _dt.datetime.now(_dt.timezone.utc)
    return t.isoformat(timespec='seconds'), t.astimezone(_dt.timezone(_dt.timedelta(hours=9))).isoformat(timespec='seconds')


def parse_type_map(s):
    out = {}
    for pair in str(s).split(','):
        k, v = pair.split(':')
        out[int(k)] = v.strip()
    return out


def q_from_cert(cert):
    """증서 → 반올림 전 q = I_bottom / ΔV × g_to_q (Codex 판정 §2-2 의 재구성) · 못 내면 None."""
    if not isinstance(cert, dict):
        return None
    ib, dv, g = cert.get('I_bottom'), cert.get('delta_V'), cert.get('g_to_q')
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) for x in (ib, dv, g)):
        return None
    if not all(math.isfinite(float(x)) for x in (ib, dv, g)) or float(dv) <= 0:
        return None
    return float(ib) / float(dv) * float(g)


def _real(p):
    return os.path.realpath(os.path.abspath(os.path.expanduser(str(p))))


def _inside(child, parent):
    c, p = _real(child), _real(parent)
    return c == p or c.startswith(p.rstrip(os.sep) + os.sep)


def _ancestors(p):
    p = _real(p)
    out = [p]
    while True:
        q = os.path.dirname(p)
        if q == p:
            return out
        out.append(q)
        p = q


# ── 관문: 출력 폴더 (생산 폴더 거부) ─────────────────────────────────────────────────────────────────────

def out_dir_problems(out, inputs_root, env=None):
    """→ 문제 목록 (빈 목록 = 쓸 수 있음).  생산물 옆에 쓰지 않는다: 리포 · 입력 뿌리 · 배치 출력 · 웹앱 서빙 폴더 · 다른 실행의 manifest 폴더."""
    env = os.environ if env is None else env
    probs = []
    o = _real(out)
    if os.path.exists(o):
        if not os.path.isdir(o):
            probs.append(f'--out {o} 이 파일이다')
        elif os.listdir(o):
            probs.append(f'--out {o} 이 비어 있지 않다 (새 빈 폴더만 — 옛 결과를 덮지 않는다)')
    if inputs_root:
        ir = _real(inputs_root)
        if _inside(o, ir):
            probs.append(f'--out {o} 이 입력 뿌리 {ir} 안이다 (생산 결과 폴더)')
        if _inside(ir, o):
            probs.append(f'--out {o} 이 입력 뿌리 {ir} 의 조상이다')
    for a in _ancestors(o):
        if os.path.exists(os.path.join(a, '.git')):
            probs.append(f'--out {o} 이 git 체크아웃 {a} 안이다 (리포 · 작업트리에 쓰지 않는다 — 반입은 따로)')
        st = os.path.join(a, 'status.json')
        if os.path.isfile(st):
            try:
                sch = json.load(open(st, encoding='utf-8')).get('schema')
            except Exception:                              # noqa: BLE001
                sch = None
            if sch in BATCH_SCHEMAS:
                probs.append(f'--out {o} 이 배치 출력 {a} 안이다 (status.json schema {sch})')
        if os.path.isdir(os.path.join(a, 'work', 'results')) and os.path.isdir(os.path.join(a, 'solver_output')):
            probs.append(f'--out {o} 이 배치 출력 꼴 (work/results + solver_output) {a} 안이다')
        if a != o and os.path.isfile(os.path.join(a, 'manifest.json')):
            probs.append(f'--out {o} 이 다른 실행의 manifest 폴더 {a} 안이다')
    for k in SERVED_ENV:
        v = env.get(k)
        if v and _inside(o, v):
            probs.append(f'--out {o} 이 웹앱 서빙 폴더 {k}={v} 안이다')
    return probs


# ── 등록 표 · 저장 원자료 ──────────────────────────────────────────────────────────────────────────────

def load_registered(tsv_path, archive_path, registered=REGISTERED_CASES, expected_archive_sha=ARCHIVE_SHA256):
    """등록 표 (TSV) · 저장 원자료 (tgz) → dict(problems, tsv_sha256, archive_sha256, cases={id: 저장 기록}).  읽기만."""
    probs = []
    a_sha = sha256_file(archive_path)
    if a_sha != expected_archive_sha:
        probs.append(f'원자료 tgz sha256 {a_sha} ≠ 등록 {expected_archive_sha}')
    rows = list(csv.DictReader(open(tsv_path, encoding='utf-8'), delimiter='\t'))
    ids = [r.get('case_id') for r in rows]
    reg_ids = [c for c, _ in registered]
    if len(ids) != len(set(ids)):
        probs.append(f'표에 case_id 중복 {sorted(i for i in set(ids) if ids.count(i) > 1)}')
    if len(reg_ids) != len(set(reg_ids)):
        probs.append('등록 케이스 목록에 중복')
    if sorted(set(ids)) != sorted(set(reg_ids)):
        probs.append(f'표 case_id {sorted(set(ids))} ≠ 등록 {sorted(set(reg_ids))}')
    lab = {r.get('case_id'): r.get('P_S') for r in rows}
    for c, l in registered:
        if c in lab and lab[c] != l:
            probs.append(f'{c}: 표 P_S {lab[c]!r} ≠ 등록 {l!r}')
    cases = {}
    with tarfile.open(archive_path) as t:
        status = json.load(t.extractfile('status.json'))
        sc = status.get('cases') or {}
        for c, l in registered:
            st = sc.get(c)
            if not isinstance(st, dict):
                probs.append(f'{c}: 저장 status.json 에 케이스 없음')
                continue
            modes = {}
            for cm in ('hertzian', 'physics'):
                name = f'solver_output/{c}/network_conductivity_{cm}.json'
                try:
                    rec = json.load(t.extractfile(name))
                except (KeyError, AttributeError):
                    probs.append(f'{c}: 저장 {name} 없음')
                    continue
                cert = rec.get('electronic_solve_certificate_full')
                modes[cm] = dict(q=q_from_cert(cert), sigma_full=rec.get('electronic_sigma_full'),
                                 sigma_full_mScm=rec.get('electronic_sigma_full_mScm'), n_nodes=rec.get('electronic_n_nodes'),
                                 n_edges=rec.get('electronic_n_edges'), boundary_rule=rec.get('electronic_boundary_rule'),
                                 percolating_fraction=rec.get('electronic_percolating_fraction'), status=rec.get('electronic_status'),
                                 geometry=(cert or {}).get('geometry'), sigma_bulk_S_cm=(cert or {}).get('sigma_bulk_S_cm'),
                                 area_binding_counts_physics=rec.get('electronic_area_binding_counts_physics'))
                if modes[cm]['q'] is None:
                    probs.append(f'{c}: 저장 {cm} 전자 증서에서 q 를 못 낸다')
            cases[c] = dict(label=l, type_map=st.get('type_map'), scale=st.get('scale'), dump_type_counts=st.get('dump_type_counts'),
                            n_contact_rows=(st.get('contact_scan') or {}).get('n_rows_last'), source_sha256=st.get('source_sha256') or {},
                            atom_step=st.get('atom_step'), modes=modes)
    return dict(problems=probs, tsv_sha256=sha256_file(tsv_path), archive_sha256=a_sha, cases=cases)


# ── 관문: 케이스 입력 ──────────────────────────────────────────────────────────────────────────────────

def _geometry_of(case_dir, scale):
    mesh = json.load(open(os.path.join(case_dir, 'mesh_info.json'), encoding='utf-8'))
    ip = json.load(open(os.path.join(case_dir, 'input_params.json'), encoding='utf-8'))
    return dict(plate_z=mesh['plate_z'], box_x=ip.get('box_x', 0.05), box_y=ip.get('box_y', 0.05), scale=scale)


def case_input_problems(case_dir, arc):
    """가벼운 관문 (CSV 를 읽지 않는다): 네 파일 · 저장 기록 · 기하 = 저장 증서 기하.  → (문제 목록, 기하 | None)."""
    probs = []
    miss = [f for f in INPUT_FILES if not os.path.isfile(os.path.join(case_dir, f))]
    if miss:
        return [f'입력 파일 없음 {miss} ({case_dir})'], None
    if not arc or not arc.get('modes'):
        return ['저장 기록 없음'], None
    try:
        geo = _geometry_of(case_dir, arc.get('scale'))
    except Exception as e:                                   # noqa: BLE001
        return [f'기하 읽기 실패 ({type(e).__name__}: {e})'], None
    for cm, m in arc['modes'].items():
        g = m.get('geometry') or {}
        for k in ('plate_z', 'box_x', 'box_y', 'scale'):
            if g.get(k) != geo.get(k):
                probs.append(f'기하 {k} = {geo.get(k)!r} ≠ 저장 {cm} 증서 {g.get(k)!r}')
    return probs, geo


def load_case(case_dir, arc, geo, log=print):
    """CSV 를 망 솔버 CLI 와 같은 함수로 읽는다 → (case dict, 문제 목록)."""
    from analyze_contacts import load_atoms_raw, load_contacts_raw
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        atoms, _ = load_atoms_raw(os.path.join(case_dir, 'atoms.csv'))
        contacts, _ = load_contacts_raw(os.path.join(case_dir, 'contacts.csv'))
    log(buf.getvalue().rstrip())
    tm = parse_type_map(arc['type_map'])
    am_types = [k for k, v in tm.items() if 'AM' in v]
    probs = []
    try:
        want_atoms = sum(int(v) for _, v in (p.split(':') for p in str(arc.get('dump_type_counts')).split(',')))
    except ValueError:
        want_atoms = None
    if want_atoms is None or len(atoms) != want_atoms:
        probs.append(f'입자 수 {len(atoms)} ≠ 저장 덤프 개수 {arc.get("dump_type_counts")!r}')
    if arc.get('n_contact_rows') is not None and len(contacts) != int(arc['n_contact_rows']):
        probs.append(f'접촉 행 {len(contacts)} ≠ 저장 contact_scan.n_rows_last {arc["n_contact_rows"]}')
    scale = arc['scale']
    radii = {}
    for a in atoms.values():
        lbl = tm.get(a['type'])
        if lbl and 'AM' in lbl:
            radii.setdefault(lbl, set()).add(round(float(a['radius']) * scale, 9))
    am_ids = {aid for aid, a in atoms.items() if a['type'] in am_types}
    n_zero = sum(1 for c in contacts if c['id1'] in am_ids and c['id2'] in am_ids and not (c['contact_area'] > 0))
    case = dict(atoms=atoms, contacts=contacts, am_types=am_types, type_map=tm, scale=scale, plate_z=geo['plate_z'],
                box_x=geo['box_x'], box_y=geo['box_y'],
                info=dict(n_atoms=len(atoms), n_contacts=len(contacts), am_types=am_types, type_map=arc['type_map'],
                          am_radii_um={k: sorted(v) for k, v in radii.items()}, n_am_am_zero_area=n_zero,
                          sc_only=('AM_P' not in tm.values() and 'AM_S' in tm.values()),
                          pc_only=('AM_S' not in tm.values() and 'AM_P' in tm.values())))
    return case, probs


def upload_copy_check(inputs_root, case_id, arc):
    """배치 작업 폴더의 업로드 사본 (`<inputs_root>/../uploads/<id>/`) 이 저장 실행 source_sha256 과 같은가 — 기록만 (없으면 None)."""
    up = os.path.join(os.path.dirname(_real(inputs_root)), 'uploads', case_id)
    want = arc.get('source_sha256') or {}
    if not os.path.isdir(up) or not want:
        return None
    out = {}
    for name, sha in want.items():
        p = os.path.join(up, name)
        out[name] = (os.path.isfile(p) and sha256_file(p) == sha)
    return out


# ── PC 인자 끔 (실행 중 교체 · 파일 불변) ────────────────────────────────────────────────────────────────

@contextlib.contextmanager
def factor_off(nc):
    """`nc.sigma_AM_relative` → 상수 1 (PC 크기 인자 끔).  끝나면 (예외 포함) 원 함수로 되돌린다."""
    orig = nc.sigma_AM_relative

    def _sigma_rel_off(r_um, particle_type):            # noqa: ARG001 — 등록 §1: 모든 AM 입자 σ_rel = 1
        return 1.0
    nc.sigma_AM_relative = _sigma_rel_off
    try:
        yield _sigma_rel_off
    finally:
        nc.sigma_AM_relative = orig


def run_arm(nc, case, arm, patcher=factor_off):
    """한 팔 = 전자 망 한 번 (`_run_all_networks` 의 전자 호출과 같은 인자) → (요약 레코드, 원 결과 dict, 로그)."""
    buf = io.StringIO()
    ctx = patcher(nc) if arm['factor'] == 'off' else contextlib.nullcontext()
    with ctx, contextlib.redirect_stdout(buf):
        res = nc.run_decomposition(case['atoms'], case['contacts'], case['am_types'], case['scale'], case['plate_z'],
                                   case['box_x'], case['box_y'], sigma_bulk=arm['sigma_S_cm'], type_map=case['type_map'],
                                   contact_mode=arm['contact_mode'], mode='electronic')
    rec = dict(arm=arm['name'], contact_mode=arm['contact_mode'], factor=arm['factor'], sigma_S_cm=arm['sigma_S_cm'], role=arm['role'])
    if not res:
        rec.update(status='no_result', reason='run_decomposition returned no result (AM 망 없음)', q_raw=None, certificate=None,
                   certificate_problem='결과 없음')
        return rec, res, buf.getvalue()
    cert = res.get('solve_certificate_full')
    cprob = nc.certificate_problem(cert) if cert is not None else '증서 없음'
    q_cert = q_from_cert(cert)
    #  ★ 받아들인 해만 값으로 — 증서 문제 없음 · 상태 computed · 게시 σ 있음.  거부된 풀이 (가드 · 증서 실패) 의 전류로 q 를 만들지 않는다
    #    (그 q 는 q_cert_unaccepted 진단 칸에만 · 표에는 안 간다).
    accepted = (cprob is None and res.get('sigma_full_status') == 'computed' and res.get('sigma_full') is not None)
    q = q_cert if accepted else None
    rec.update(
        q_raw=q, q_cert_unaccepted=(None if accepted else q_cert), q_published=res.get('sigma_full'),
        sigma_mScm_unrounded=(q * arm['sigma_S_cm'] * 1000.0 if q is not None else None),
        sigma_mScm_published=res.get('sigma_full_mScm'),
        published_matches_raw=(None if q is None else (round(q, 8) == res.get('sigma_full')
                                                      and round(q * arm['sigma_S_cm'] * 1000.0, 6) == res.get('sigma_full_mScm'))),
        status=res.get('sigma_full_status'), reason=res.get('sigma_full_reason'),
        certificate_problem=cprob,
        certificate=json_safe(cert),
        sigma_bulk_net_status=res.get('sigma_bulk_net_status'), sigma_constr_net_status=res.get('sigma_constr_net_status'),
        q_bulk_net_raw=q_from_cert(res.get('solve_certificate_bulk_net')),
        q_constr_net_raw=q_from_cert(res.get('solve_certificate_constr_net')),
        n_nodes=res.get('n_nodes'), n_edges=res.get('n_edges'), boundary_rule=res.get('boundary_rule'),
        percolating_fraction=res.get('percolating_fraction'), area_binding_counts_physics=json_safe(res.get('area_binding_counts_physics')),
        n_floor_only=res.get('n_floor_only'), n_clamp_zero=res.get('n_clamp_zero'), resistance_model=res.get('resistance_model'),
        psi_placement=res.get('psi_placement'), area_rule=res.get('area_rule'), electrode_model=res.get('electrode_model'),
        R_brug_over_full=res.get('R_brug_over_full'),
        constriction_power_share=json_safe({k: v for k, v in res.items() if str(k).startswith('constriction_power_share_el_')}))
    return rec, res, buf.getvalue()


def control_problems(rec, arc_mode):
    """대조 팔 ↔ 저장 증서 (같은 입력 · 같은 코드 · 같은 모형이면 같아야 한다)."""
    probs = []
    if rec.get('certificate_problem'):
        probs.append(f'대조 팔 증서 문제: {rec["certificate_problem"]}')
    q, qa = rec.get('q_raw'), (arc_mode or {}).get('q')
    if q is None or qa is None:
        probs.append(f'q 없음 (대조 {q!r} · 저장 {qa!r})')
    elif abs(q - qa) > CONTROL_Q_RTOL * abs(qa):
        probs.append(f'q {q!r} ≠ 저장 {qa!r} (상대 {abs(q - qa) / abs(qa):.3g} > {CONTROL_Q_RTOL:g})')
    for k in ('n_nodes', 'n_edges', 'boundary_rule'):
        if rec.get(k) != (arc_mode or {}).get(k):
            probs.append(f'{k} {rec.get(k)!r} ≠ 저장 {(arc_mode or {}).get(k)!r}')
    g = (rec.get('certificate') or {}).get('geometry')
    if g != (arc_mode or {}).get('geometry'):
        probs.append(f'증서 기하 {g!r} ≠ 저장 {(arc_mode or {}).get("geometry")!r}')
    return probs


# ── 패치 양성 대조 (합성 망 · 실제 생산 함수) ────────────────────────────────────────────────────────────────

def synthetic_case(kind, r=4.5, delta=0.1, box=30.0):
    """3 열 × 5 층 · 같은 반경 구 15 · 접촉 22 · 접촉 면적 = 정확 교차 원판.  kind = pc · sc · mixed."""
    d = 2 * r - delta
    pattern = [[1, 2, 1], [1, 2, 2], [2, 2, 1], [1, 1, 2], [2, 1, 1]]
    atoms = {}
    for row in range(5):
        for col in range(3):
            aid = 1 + row * 3 + col
            ty = {'pc': 1, 'sc': 2}.get(kind) or pattern[row][col]
            atoms[aid] = dict(type=ty, x=r + col * d, y=r, z=r + row * d, radius=r)
    area = math.pi * (r * r - (d / 2) ** 2)
    contacts = []
    for row in range(5):
        for col in range(3):
            aid = 1 + row * 3 + col
            for other in ([aid + 3] if row < 4 else []) + ([aid + 1] if col < 2 else []):
                contacts.append(dict(id1=aid, id2=other, delta=delta, contact_area=area, fn=1.0, ft=0.0,
                                     fn_x=0.0, fn_y=0.0, fn_z=1.0, ft_x=0.0, ft_y=0.0, ft_z=0.0))
    tm = {'pc': {1: 'AM_P'}, 'sc': {2: 'AM_S'}}.get(kind) or {1: 'AM_P', 2: 'AM_S'}
    return dict(atoms=atoms, contacts=contacts, am_types=sorted(tm), type_map=tm, scale=1.0, plate_z=2 * r + 4 * d, box_x=box, box_y=box)


def factor_probe(nc, patcher=factor_off):
    """등록 §3 G1 — 패치가 실제로 켜졌는가: PC 만 OFF/ON = 35/8 (세 가지 · 두 모드) · SC 만 = 1 (비트) · 혼합 ≠ 35/8 · 패치 뒤 원 함수 복원."""
    orig = nc.sigma_AM_relative
    out = dict(checks=[], passed=True)

    def chk(name, ok, val=None):
        out['checks'].append(dict(name=name, ok=bool(ok), value=json_safe(val)))
        out['passed'] = out['passed'] and bool(ok)
    for cm in ('hertzian', 'physics'):
        for kind in ('pc', 'sc', 'mixed'):
            case = synthetic_case(kind)
            on, _, _ = run_arm(nc, case, dict(name='probe_on', contact_mode=cm, factor='on', sigma_S_cm=SIGMA_BASE_S_CM, role='probe'), patcher)
            off, _, _ = run_arm(nc, case, dict(name='probe_off', contact_mode=cm, factor='off', sigma_S_cm=SIGMA_BASE_S_CM, role='probe'), patcher)
            ratios = {}
            for key in ('q_raw', 'q_bulk_net_raw', 'q_constr_net_raw'):
                a, b = on.get(key), off.get(key)
                ratios[key] = (b / a) if (a and b) else None
            if kind == 'pc':
                chk(f'{cm}/pc OFF/ON = 35/8 (FULL · CF · 협착만)',
                    all(v is not None and abs(v - PC_RATIO) <= PROBE_RTOL * PC_RATIO for v in ratios.values()), ratios)
            elif kind == 'sc':
                chk(f'{cm}/sc OFF = ON (비트)', all(on.get(k) == off.get(k) and on.get(k) is not None
                                                   for k in ('q_raw', 'q_bulk_net_raw', 'q_constr_net_raw')), ratios)
            else:
                v = ratios['q_raw']
                chk(f'{cm}/mixed OFF/ON ∉ {{1, 35/8}} (배율로 못 바꾼다)',
                    v is not None and abs(v - 1) > 1e-6 and abs(v - PC_RATIO) > 1e-6, ratios)
    chk('패치 뒤 원 함수 복원', nc.sigma_AM_relative is orig)
    chk('모듈 기준값 SIGMA_AM_ELECTRONIC 불변 (0.05)', nc.SIGMA_AM_ELECTRONIC == SIGMA_BASE_S_CM, nc.SIGMA_AM_ELECTRONIC)
    return out


# ── 코드 · 환경 · git ──────────────────────────────────────────────────────────────────────────────────

def code_state(repo):
    import run_network_194_parallel as R194
    h = R194.code_hashes(repo)
    return dict(code_hashes=h, code_fp=R194.code_fp(h),
                network_conductivity_sha256=sha256_file(os.path.join(repo, 'scripts', 'network_conductivity.py')))


def git_state(repo):
    def g(*a):
        r = subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else None
    head = g('rev-parse', 'HEAD')
    st = g('status', '--porcelain', '--untracked-files=no')
    return dict(head=head, dirty=(None if st is None else bool(st)), dirty_lines=(st.splitlines() if st else []))


def environment():
    import numpy
    import scipy
    env = dict(python=sys.version, platform=platform.platform(), numpy=numpy.__version__, scipy=scipy.__version__,
               threads={k: os.environ.get(k) for k in THREAD_ENV})
    for mod in ('networkx', 'pandas'):
        try:
            env[mod] = __import__(mod).__version__
        except ImportError:
            env[mod] = None
    return env


def imported_repo_modules(repo):
    out = {}
    for name, m in sorted(sys.modules.items()):
        f = getattr(m, '__file__', None)
        if f and _inside(f, repo) and os.path.isfile(f):
            out[os.path.relpath(_real(f), _real(repo)).replace(os.sep, '/')] = sha256_file(f)
    return out


# ── manifest ───────────────────────────────────────────────────────────────────────────────────────────

def manifest_problems(m, registered=REGISTERED_CASES, expected_nc_sha=EXPECTED_NC_SHA256, expected_code_fp=EXPECTED_CODE_FP,
                      expected_archive_sha=ARCHIVE_SHA256, out_dir=None):
    """manifest 필수 칸 · 등록 값 · 산출 해시 → 문제 목록 (빈 목록 = manifest.json 을 쓸 수 있다)."""
    p = []
    if not isinstance(m, dict):
        return ['manifest 가 dict 가 아니다']
    for k in MANIFEST_REQUIRED:
        if k not in m:
            p.append(f'필수 칸 없음: {k}')
        elif k != 'run_problems' and m[k] in (None, '', [], {}):
            p.append(f'필수 칸 비었음: {k}')
    if p:
        return p
    if m['schema'] != SCHEMA or m['kind'] != KIND:
        p.append(f'schema · kind = {m["schema"]!r} · {m["kind"]!r}')
    if m['sigma_ref_S_cm'] != SIGMA_REF_S_CM:
        p.append(f'sigma_ref_S_cm {m["sigma_ref_S_cm"]!r} ≠ 등록 {SIGMA_REF_S_CM}')
    if m['sigma_base_S_cm'] != SIGMA_BASE_S_CM:
        p.append(f'sigma_base_S_cm {m["sigma_base_S_cm"]!r} ≠ 등록 {SIGMA_BASE_S_CM}')
    if m['arms'] != [dict(a) for a in ARMS]:
        p.append('팔 정의 ≠ 등록 §2')
    mains = [a for a in m['arms'] if isinstance(a, dict) and a.get('role') == 'main']
    if len(mains) != 1 or mains[0].get('contact_mode') != 'hertzian' or mains[0].get('factor') != 'off' \
            or mains[0].get('sigma_S_cm') != SIGMA_REF_S_CM:
        p.append(f'주 팔 ≠ (hertzian · 인자 끔 · {SIGMA_REF_S_CM}) — {mains!r}')
    if m['factor_patch'] != FACTOR_PATCH:
        p.append('factor_patch 표지 ≠ 등록')
    reg = m['registration']
    if not isinstance(reg, dict) or reg.get('path') != REG_DOC or not reg.get('sha256'):
        p.append(f'registration = {reg!r} (경로 {REG_DOC} · sha256 필수)')
    w = m['wrapper']
    if not isinstance(w, dict) or not w.get('path') or not w.get('sha256'):
        p.append('wrapper 경로 · sha256 필수')
    gs = m['git']
    if not isinstance(gs, dict) or not gs.get('head') or gs.get('dirty') is None:
        p.append(f'git = {gs!r} (head · dirty 필수)')
    elif gs.get('dirty') and gs.get('clean_required', True):
        p.append(f'git 트리 dirty (추적 파일 변경 {len(gs.get("dirty_lines") or [])} 줄) — 깨끗한 체크아웃에서만')
    c = m['code']
    if not isinstance(c, dict):
        p.append('code 칸 꼴')
    else:
        if c.get('network_conductivity_sha256') != expected_nc_sha:
            p.append(f'network_conductivity.py sha256 {c.get("network_conductivity_sha256")} ≠ 등록 {expected_nc_sha}')
        if expected_code_fp is not None and (c.get('code_fp_before') != expected_code_fp or c.get('code_fp_after') != expected_code_fp):
            p.append(f'봉인 code_fp 전 {c.get("code_fp_before")} · 후 {c.get("code_fp_after")} ≠ 등록 {expected_code_fp}')
        if c.get('code_hashes_before') != c.get('code_hashes_after') or not c.get('code_hashes_before'):
            p.append('봉인 파일 해시가 실행 전후 다르다 (또는 없다)')
        if c.get('sigma_am_electronic_module') != SIGMA_BASE_S_CM:
            p.append(f'모듈 SIGMA_AM_ELECTRONIC {c.get("sigma_am_electronic_module")!r} ≠ {SIGMA_BASE_S_CM}')
    a = m['archive']
    if not isinstance(a, dict) or a.get('sha256') != expected_archive_sha:
        p.append(f'archive sha256 ≠ 등록 {expected_archive_sha}')
    t = m['tsv']
    if not isinstance(t, dict) or not t.get('sha256'):
        p.append('tsv sha256 필수')
    fp = m['factor_probe']
    if not isinstance(fp, dict) or not (fp.get('before') or {}).get('passed') or not (fp.get('after') or {}).get('passed'):
        p.append('인자 끔 양성 대조 (실행 앞 · 뒤) 통과 필수')
    if m['production_inputs_unchanged'] is not True:
        p.append('입력 파일이 실행 중 바뀌었다 (또는 기록 없음)')
    if m['run_status'] not in ('ok', 'cases_not_ok', 'failed'):
        p.append(f'run_status {m["run_status"]!r}')
    if not isinstance(m['run_problems'], list):
        p.append('run_problems 는 목록')
    cases = m['cases']
    reg_ids = [cid for cid, _ in registered]
    if not isinstance(cases, list) or [x.get('case_id') for x in cases if isinstance(x, dict)] != reg_ids:
        p.append(f'케이스 목록 ≠ 등록 (순서 · 중복 · 결손 포함) {reg_ids}')
    else:
        for x in cases:
            cid = x.get('case_id')
            if x.get('status') not in CASE_STATUSES:
                p.append(f'{cid}: status {x.get("status")!r}')
                continue
            if x.get('status') != 'inputs_refused':
                ih = x.get('inputs_sha256') or {}
                if sorted(ih) != sorted(INPUT_FILES) or not all(ih.values()):
                    p.append(f'{cid}: 입력 네 파일 sha256 필수')
            if x.get('status') in ('ok', 'control_mismatch'):
                arms = x.get('arms') or {}
                if sorted(arms) != sorted(a_['name'] for a_ in ARMS):
                    p.append(f'{cid}: 팔 기록 ≠ 등록 넷')
                for an, r in arms.items():
                    if r.get('status') in ('computed', 'model_over_conduction') and not isinstance(r.get('certificate'), dict):
                        p.append(f'{cid}/{an}: 계산된 팔인데 수치 증서 없음')
                    if r.get('factor') != dict((a_['name'], a_['factor']) for a_ in ARMS).get(an):
                        p.append(f'{cid}/{an}: 인자 상태 기록 ≠ 등록')
    outs = m['outputs']
    if not isinstance(outs, list) or not outs:
        p.append('outputs 목록 필수')
    elif out_dir is not None:
        for o in outs:
            fpath = os.path.join(out_dir, o.get('path', ''))
            if not os.path.isfile(fpath) or sha256_file(fpath) != o.get('sha256'):
                p.append(f'출력 {o.get("path")} 해시 불일치 · 없음')
    return p


TSV_COLS = ('case_id', 'P_S', 'case_status', 'main_q', 'main_sigma_ref_mScm', 'main_sigma_ref_mScm_6dp', 'main_status', 'main_reason',
            'main_certificate_problem', 'sens_physics_q', 'sens_physics_sigma_ref_mScm', 'sens_physics_status',
            'readout_on_hertz_sigma_ref_mScm', 'readout_on_physics_sigma_ref_mScm', 'off_over_on_hertz', 'off_over_on_physics',
            'control_hertz_rel_diff', 'control_physics_rel_diff', 'n_nodes', 'n_edges', 'boundary_rule', 'am_radii_um',
            'sigma_ref_S_cm', 'factor_main', 'basis')


def tsv_row(x):
    arms = x.get('arms') or {}
    ok = x.get('status') == 'ok'
    m, s = arms.get('main_hertz_off') or {}, arms.get('sens_physics_off') or {}
    ch, cp = arms.get('control_hertz_on') or {}, arms.get('control_physics_on') or {}

    def v(val):
        return '' if (val is None or not ok) else repr(val)
    row = dict(case_id=x['case_id'], P_S=x.get('P_S'), case_status=x.get('status'),
               main_q=v(m.get('q_raw')), main_sigma_ref_mScm=v(m.get('sigma_mScm_unrounded')),
               main_sigma_ref_mScm_6dp=v(m.get('sigma_mScm_published')), main_status=m.get('status') or '', main_reason=m.get('reason') or '',
               main_certificate_problem=m.get('certificate_problem') or '',
               sens_physics_q=v(s.get('q_raw')), sens_physics_sigma_ref_mScm=v(s.get('sigma_mScm_unrounded')),
               sens_physics_status=s.get('status') or '',
               readout_on_hertz_sigma_ref_mScm=v(None if ch.get('q_raw') is None else ch['q_raw'] * SIGMA_REF_S_CM * 1000.0),
               readout_on_physics_sigma_ref_mScm=v(None if cp.get('q_raw') is None else cp['q_raw'] * SIGMA_REF_S_CM * 1000.0),
               off_over_on_hertz=v((x.get('derived') or {}).get('off_over_on_hertzian')),
               off_over_on_physics=v((x.get('derived') or {}).get('off_over_on_physics')),
               control_hertz_rel_diff=repr((x.get('derived') or {}).get('control_rel_diff_hertzian')),
               control_physics_rel_diff=repr((x.get('derived') or {}).get('control_rel_diff_physics')),
               n_nodes=m.get('n_nodes') if m.get('n_nodes') is not None else '', n_edges=m.get('n_edges') if m.get('n_edges') is not None else '',
               boundary_rule=m.get('boundary_rule') or '', am_radii_um=json.dumps((x.get('inputs') or {}).get('am_radii_um'), ensure_ascii=False),
               sigma_ref_S_cm=repr(SIGMA_REF_S_CM), factor_main='off (sigma_AM_relative = 1 · 실행 중 교체)',
               basis='report-only model variant — 원 생산값 아님 · readout_on_* = PC 인자 켬 기존 해의 4.1 환산 (감도)')
    return row


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(json_safe(obj), f, ensure_ascii=False, indent=1)


# ── 실행 ───────────────────────────────────────────────────────────────────────────────────────────────

def run(repo, inputs_root, out, *, registered=REGISTERED_CASES, tsv_path=None, archive_path=None, expected_archive_sha=ARCHIVE_SHA256,
        expected_nc_sha=EXPECTED_NC_SHA256, expected_code_fp=EXPECTED_CODE_FP, require_clean=True, check_only=False, log=print, patcher=factor_off):
    """→ (rc, manifest | None).  rc 2 = 관문 거부 (쓰기 0 또는 REFUSED 표지)."""
    tsv_path = tsv_path or os.path.join(repo, TSV_REL)
    archive_path = archive_path or os.path.join(repo, ARCHIVE_REL)
    import network_conductivity as nc
    # ── G0 ──
    pre = []
    pre += out_dir_problems(out, inputs_root)
    if not os.path.isdir(_real(inputs_root)):
        pre.append(f'--inputs-root {inputs_root} 이 폴더가 아니다')
    reg_doc = os.path.join(repo, REG_DOC)
    if not os.path.isfile(reg_doc):
        pre.append(f'등록 문서 없음 {REG_DOC}')
    gs = git_state(repo)
    gs['clean_required'] = bool(require_clean)
    if require_clean and (gs['dirty'] is None or gs['dirty']):
        pre.append(f'git 트리가 깨끗하지 않다 (추적 파일 변경 {len(gs["dirty_lines"])} 줄 · head {gs["head"]}) — 깨끗한 체크아웃에서만')
    cs0 = code_state(repo)
    if cs0['network_conductivity_sha256'] != expected_nc_sha:
        pre.append(f'network_conductivity.py sha256 {cs0["network_conductivity_sha256"]} ≠ 등록 {expected_nc_sha}')
    if expected_code_fp is not None and cs0['code_fp'] != expected_code_fp:
        pre.append(f'봉인 code_fp {cs0["code_fp"]} ≠ 등록 {expected_code_fp}')
    if nc.SIGMA_AM_ELECTRONIC != SIGMA_BASE_S_CM:
        pre.append(f'모듈 SIGMA_AM_ELECTRONIC {nc.SIGMA_AM_ELECTRONIC} ≠ {SIGMA_BASE_S_CM}')
    regd = load_registered(tsv_path, archive_path, registered, expected_archive_sha)
    pre += regd['problems']
    light = {}
    for cid, _ in registered:
        cp, geo = case_input_problems(os.path.join(_real(inputs_root), cid), regd['cases'].get(cid))
        light[cid] = (cp, geo)
        if check_only:
            log(f'  {cid}: ' + ('입력 관문 통과 · 기하 = 저장 증서' if not cp else ' · '.join(cp)))
    if pre:
        for x in pre:
            log('⛔ ' + x)
        return 2, None
    if check_only:
        bad = [cid for cid, (cp, _) in light.items() if cp]
        log('check-only: 관문 G0 통과 · 케이스 입력 관문 ' + ('5/5 통과' if not bad else f'실패 {bad}') + ' · 풀이 · 쓰기 없음')
        return (0 if not bad else 1), None
    # ── G1 (앞) ──
    probe_before = factor_probe(nc, patcher)
    if not probe_before['passed']:
        log('⛔ 인자 끔 양성 대조 (앞) 실패 — 패치가 켜지지 않았다: ' + json.dumps(probe_before, ensure_ascii=False)[:2000])
        return 2, None
    os.makedirs(_real(out), exist_ok=True)
    out = _real(out)
    outputs, cases, run_problems = [], [], []
    unchanged_all = True
    for cid, lab in registered:
        arc = regd['cases'].get(cid) or {}
        case_dir = os.path.join(_real(inputs_root), cid)
        x = dict(case_id=cid, P_S=lab, status=None, problems=[], arms={}, derived={}, inputs=None, inputs_sha256=None,
                 upload_copy_matches_archived=None)
        cp, geo = light[cid]
        if cp:
            x.update(status='inputs_refused', problems=cp)
            cases.append(x)
            log(f'⛔ {cid} ({lab}) 입력 관문: ' + ' · '.join(cp))
            continue
        ih0 = {f: sha256_file(os.path.join(case_dir, f)) for f in INPUT_FILES}
        x['inputs_sha256'] = ih0
        x['upload_copy_matches_archived'] = upload_copy_check(inputs_root, cid, arc)
        try:
            case, lp = load_case(case_dir, arc, geo, log=log)
        except Exception as e:                               # noqa: BLE001
            x.update(status='error', problems=[f'입력 읽기 실패 {type(e).__name__}: {e}'])
            cases.append(x)
            continue
        x['inputs'] = dict(case['info'], geometry=geo)
        if lp:
            x.update(status='inputs_refused', problems=lp)
            cases.append(x)
            log(f'⛔ {cid} ({lab}) 입력 결합: ' + ' · '.join(lp))
            continue
        for arm in ARMS:
            try:
                rec, res, alog = run_arm(nc, case, arm, patcher)
            except Exception as e:                           # noqa: BLE001
                rec, res, alog = dict(arm=arm['name'], factor=arm['factor'], status='error', reason=f'{type(e).__name__}: {e}',
                                      q_raw=None, certificate=None, certificate_problem='예외'), None, ''
            x['arms'][arm['name']] = rec
            rp = f'records/{cid}__{arm["name"]}.json'
            write_json(os.path.join(out, rp), dict(case_id=cid, arm=arm, summary=rec, result=res))
            lp_ = f'logs/{cid}__{arm["name"]}.log'
            os.makedirs(os.path.join(out, 'logs'), exist_ok=True)
            with open(os.path.join(out, lp_), 'w', encoding='utf-8', newline='\n') as f:
                f.write(alog)
            outputs += [rp, lp_]
            log(f'  {cid} ({lab}) {arm["name"]}: q {rec.get("q_raw")!r} · σ {rec.get("sigma_mScm_unrounded")!r} mS/cm · {rec.get("status")}')
        cprob = []
        for cm in ('hertzian', 'physics'):
            ctl = x['arms'][CONTROL_OF[cm]]
            arm_ = (arc.get('modes') or {}).get(cm)
            pr = control_problems(ctl, arm_)
            cprob += [f'{cm}: {s}' for s in pr]
            qa, qc, qv = (arm_ or {}).get('q'), ctl.get('q_raw'), x['arms'][VARIANT_OF[cm]].get('q_raw')
            x['derived'][f'control_rel_diff_{cm}'] = (abs(qc - qa) / abs(qa)) if (qa and qc is not None) else None
            x['derived'][f'off_over_on_{cm}'] = (qv / qc) if (qc and qv is not None) else None
        info = case['info']
        if info['sc_only']:
            same = all(x['arms'][VARIANT_OF[cm]].get('q_raw') == x['arms'][CONTROL_OF[cm]].get('q_raw')
                       and x['arms'][CONTROL_OF[cm]].get('q_raw') is not None for cm in ('hertzian', 'physics'))
            x['derived']['sc_only_off_equals_on'] = same
            if not same:
                run_problems.append(f'{cid}: SC 만 침대인데 인자 끔 q ≠ 켬 q (G4) — 패치가 SC 를 건드렸다')
        if info['pc_only']:
            for cm in ('hertzian', 'physics'):
                r_ = x['derived'].get(f'off_over_on_{cm}')
                x['derived'][f'pc_only_ratio_minus_35_8_{cm}'] = (r_ - PC_RATIO) if r_ is not None else None
        x['status'] = 'control_mismatch' if cprob else 'ok'
        x['problems'] = cprob
        if cprob:
            log(f'⛔ {cid} ({lab}) 대조 팔 ≠ 저장: ' + ' · '.join(cprob))
        ih1 = {f: sha256_file(os.path.join(case_dir, f)) for f in INPUT_FILES}
        if ih1 != ih0:
            unchanged_all = False
            run_problems.append(f'{cid}: 입력 파일이 실행 중 바뀌었다')
        cases.append(x)
    # ── G1 (뒤) · 봉인 뒤 ──
    probe_after = factor_probe(nc, patcher)
    cs1 = code_state(repo)
    if not probe_after['passed']:
        run_problems.append('인자 끔 양성 대조 (뒤) 실패')
    if cs1['code_hashes'] != cs0['code_hashes']:
        run_problems.append('봉인 파일이 실행 중 바뀌었다')
    run_status = 'failed' if run_problems else ('ok' if all(c['status'] == 'ok' for c in cases) else 'cases_not_ok')
    tsv_rel = 'factor_off_electronic.tsv'
    with open(os.path.join(out, tsv_rel), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=TSV_COLS, delimiter='\t', lineterminator='\n')
        w.writeheader()
        for x in cases:
            w.writerow(tsv_row(x))
    outputs.append(tsv_rel)
    created_utc, created_kst = now_stamps()
    man = dict(
        schema=SCHEMA, kind=KIND,
        registration=dict(path=REG_DOC, sha256=sha256_file(reg_doc)),
        wrapper=dict(path=os.path.relpath(_real(__file__), _real(repo)).replace(os.sep, '/'), sha256=sha256_file(__file__)),
        git=gs,
        code=dict(network_conductivity_sha256=cs0['network_conductivity_sha256'], network_conductivity_sha256_expected=expected_nc_sha,
                  code_fp_before=cs0['code_fp'], code_fp_after=cs1['code_fp'], code_fp_expected=expected_code_fp,
                  code_hashes_before=cs0['code_hashes'], code_hashes_after=cs1['code_hashes'],
                  imported_repo_modules=imported_repo_modules(repo), sigma_am_electronic_module=nc.SIGMA_AM_ELECTRONIC,
                  psi_placement_default=getattr(nc, 'PSI_PLACEMENT_DEFAULT', None), area_rule_default=getattr(nc, 'AREA_RULE_DEFAULT', None)),
        environment=environment(),
        sigma_ref_S_cm=SIGMA_REF_S_CM, sigma_ref_label=SIGMA_REF_LABEL, sigma_base_S_cm=SIGMA_BASE_S_CM,
        arms=[dict(a) for a in ARMS], factor_patch=dict(FACTOR_PATCH),
        archive=dict(path=os.path.relpath(_real(archive_path), _real(repo)).replace(os.sep, '/') if _inside(archive_path, repo) else _real(archive_path),
                     sha256=regd['archive_sha256']),
        tsv=dict(path=os.path.relpath(_real(tsv_path), _real(repo)).replace(os.sep, '/') if _inside(tsv_path, repo) else _real(tsv_path),
                 sha256=regd['tsv_sha256']),
        inputs_root=_real(inputs_root), out=out, cases=cases,
        factor_probe=dict(before=probe_before, after=probe_after),
        outputs=[dict(path=o, sha256=sha256_file(os.path.join(out, o))) for o in outputs],
        production_inputs_unchanged=unchanged_all, run_status=run_status, run_problems=run_problems,
        created_utc=created_utc, created_kst=created_kst)
    return finalize(out, man, registered=registered, expected_nc_sha=expected_nc_sha, expected_code_fp=expected_code_fp,
                    expected_archive_sha=expected_archive_sha, log=log)


def finalize(out, man, *, log=print, **kw):
    """manifest 를 검사하고 통과할 때만 manifest.json 을 쓴다 (아니면 manifest.REFUSED.json + 표 = *.REFUSED.tsv)."""
    probs = manifest_problems(man, out_dir=out, **kw)
    if probs:
        write_json(os.path.join(out, 'manifest.REFUSED.json'), dict(problems=probs, manifest=man))
        t = os.path.join(out, 'factor_off_electronic.tsv')
        if os.path.isfile(t):
            os.replace(t, os.path.join(out, 'factor_off_electronic.REFUSED.tsv'))
        for x in probs:
            log('⛔ manifest: ' + x)
        return 2, None
    write_json(os.path.join(out, 'manifest.json'), man)
    log(f'manifest.json · run_status {man["run_status"]} · 케이스 ' + ' · '.join(f'{c["P_S"]} {c["status"]}' for c in man['cases']))
    for x in man['run_problems']:
        log('⚠ ' + x)
    return (0 if man['run_status'] == 'ok' else 1), man


# ── 자체시험 (반례 먼저) ────────────────────────────────────────────────────────────────────────────────

def _write_case_inputs(d, case):
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'atoms.csv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id,type,x,y,z,radius\n')
        for aid, a in sorted(case['atoms'].items()):
            f.write(f'{aid},{a["type"]},{a["x"]!r},{a["y"]!r},{a["z"]!r},{a["radius"]!r}\n')
    with open(os.path.join(d, 'contacts.csv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('id1,id2,fn_x,fn_y,fn_z,ft_x,ft_y,ft_z,contact_area,delta\n')
        for c in case['contacts']:
            f.write(f'{c["id1"]},{c["id2"]},0.0,0.0,1.0,0.0,0.0,0.0,{c["contact_area"]!r},{c["delta"]!r}\n')
    json.dump(dict(plate_z=case['plate_z']), open(os.path.join(d, 'mesh_info.json'), 'w'))
    json.dump(dict(box_x=case['box_x'], box_y=case['box_y']), open(os.path.join(d, 'input_params.json'), 'w'))


def _make_synthetic_world(tmp, nc):
    """합성 다섯 케이스 (SC 만 · 혼합 셋 · PC 만) + 저장 원자료 tgz (대조 팔과 같은 호출로 만든 전자 레코드) + 등록 표."""
    kinds = (('syn_sc', '0:10', 'sc'), ('syn_37', '3:7', 'mixed'), ('syn_55', '5:5', 'mixed'), ('syn_73', '7:3', 'mixed'), ('syn_pc', '10:0', 'pc'))
    batch = os.path.join(tmp, 'batch')
    inputs_root = os.path.join(batch, 'work', 'results')
    stage = os.path.join(tmp, 'stage')
    status = dict(schema='webapp_network_batch/v1', cases={})
    for cid, lab, kind in kinds:
        case = synthetic_case(kind)
        _write_case_inputs(os.path.join(inputs_root, cid), case)
        tm = ','.join(f'{k}:{v}' for k, v in sorted(case['type_map'].items()))
        counts = {}
        for a in case['atoms'].values():
            counts[a['type']] = counts.get(a['type'], 0) + 1
        status['cases'][cid] = dict(type_map=tm, scale=1.0, dump_type_counts=','.join(f'{k}:{v}' for k, v in sorted(counts.items())),
                                    contact_scan=dict(n_rows_last=len(case['contacts'])), source_sha256={})
        for cm in ('hertzian', 'physics'):
            with contextlib.redirect_stdout(io.StringIO()):
                res = nc.run_decomposition(case['atoms'], case['contacts'], case['am_types'], 1.0, case['plate_z'], case['box_x'],
                                           case['box_y'], sigma_bulk=SIGMA_BASE_S_CM, type_map=case['type_map'], contact_mode=cm,
                                           mode='electronic')
            rec = {'electronic_sigma_full': res.get('sigma_full'), 'electronic_sigma_full_mScm': res.get('sigma_full_mScm'),
                   'electronic_n_nodes': res.get('n_nodes'), 'electronic_n_edges': res.get('n_edges'),
                   'electronic_boundary_rule': res.get('boundary_rule'), 'electronic_percolating_fraction': res.get('percolating_fraction'),
                   'electronic_status': 'computed', 'electronic_solve_certificate_full': res.get('solve_certificate_full'),
                   'electronic_area_binding_counts_physics': res.get('area_binding_counts_physics')}
            write_json(os.path.join(stage, 'solver_output', cid, f'network_conductivity_{cm}.json'), rec)
    write_json(os.path.join(stage, 'status.json'), status)
    write_json(os.path.join(batch, 'status.json'), status)
    os.makedirs(os.path.join(batch, 'solver_output'), exist_ok=True)
    tgz = os.path.join(tmp, 'syn_archive.tgz')
    with tarfile.open(tgz, 'w:gz') as t:
        t.add(os.path.join(stage, 'status.json'), arcname='status.json')
        t.add(os.path.join(stage, 'solver_output'), arcname='solver_output')
    tsv = os.path.join(tmp, 'syn_cases.tsv')
    with open(tsv, 'w', encoding='utf-8', newline='\n') as f:
        f.write('case_id\tP_S\n' + ''.join(f'{c}\t{l}\n' for c, l, _ in kinds))
    return dict(inputs_root=inputs_root, batch=batch, tgz=tgz, tsv=tsv, registered=tuple((c, l) for c, l, _ in kinds))


def _selftest():
    import network_conductivity as nc
    ok, bad = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(f'{name} {extra}'.strip())

    def section(label, fn, n_expected):
        """한 묶음 — 예외가 나도 다음 묶음으로 간다 (그 묶음에서 못 센 시험은 FAIL 로 센다)."""
        before = ok + len(bad)
        try:
            fn()
        except Exception as e:                               # noqa: BLE001
            bad.append(f'{label} 예외 {type(e).__name__}: {e}')
        done = ok + len(bad) - before
        for i in range(max(0, n_expected - done)):
            bad.append(f'{label} 시험 미실행 #{i + 1} (앞 단계 실패)')
    tmp = tempfile.mkdtemp(prefix='ps45e_')
    quiet = (lambda *a, **k: None)
    st = {}

    def s1():
        # ── ① 출력 폴더 관문 (생산 폴더 거부) ──
        inputs_root = os.path.join(tmp, 'b', 'work', 'results')
        os.makedirs(os.path.join(inputs_root, 'c1'))
        el = os.path.join(tmp, 'elsewhere')
        chk('①a 입력 뿌리 안 = 거부', out_dir_problems(os.path.join(inputs_root, 'c1', 'out'), inputs_root, env={}) != [])
        chk('①b 입력 뿌리 자체 = 거부', out_dir_problems(inputs_root, inputs_root, env={}) != [])
        chk('①c 입력 뿌리의 조상 = 거부', any('조상' in s for s in out_dir_problems(os.path.join(tmp, 'b', 'work'), inputs_root, env={})))
        json.dump({'schema': 'webapp_network_batch/v1'}, open(os.path.join(tmp, 'b', 'status.json'), 'w'))
        chk('①d 배치 출력 (status.json schema) 안 = 거부', any('배치 출력' in s for s in out_dir_problems(os.path.join(tmp, 'b', 'mine'), el, env={})))
        os.makedirs(os.path.join(tmp, 'g', '.git'))
        chk('①e git 체크아웃 안 = 거부', any('git' in s for s in out_dir_problems(os.path.join(tmp, 'g', 'x', 'out'), el, env={})))
        os.makedirs(os.path.join(tmp, 'full'))
        open(os.path.join(tmp, 'full', 'a.txt'), 'w').write('x')
        chk('①f 비어 있지 않은 폴더 = 거부', any('비어' in s for s in out_dir_problems(os.path.join(tmp, 'full'), el, env={})))
        served = os.path.join(tmp, 'served', 'results')
        os.makedirs(served)
        chk('①g 웹앱 서빙 폴더 (env) 안 = 거부', any('서빙' in s for s in out_dir_problems(os.path.join(served, 'x'), el,
                                                                                    env={'WEBAPP_RESULTS_FOLDER': served})))
        os.makedirs(os.path.join(tmp, 'w2', 'work', 'results'))
        os.makedirs(os.path.join(tmp, 'w2', 'solver_output'))
        chk('①h 배치 꼴 (work/results + solver_output) 안 = 거부', out_dir_problems(os.path.join(tmp, 'w2', 'x'), el, env={}) != [])
        os.makedirs(os.path.join(tmp, 'prev'))
        json.dump({}, open(os.path.join(tmp, 'prev', 'manifest.json'), 'w'))
        chk('①i 다른 실행 manifest 폴더 안 = 거부', any('manifest' in s for s in out_dir_problems(os.path.join(tmp, 'prev', 'n'), el, env={})))
        os.symlink(os.path.join(tmp, 'b'), os.path.join(tmp, 'link_to_batch'))
        chk('①j 심볼릭 링크로 배치 안 = 거부 (실제 경로)', out_dir_problems(os.path.join(tmp, 'link_to_batch', 'o'), el, env={}) != [])
        fresh = out_dir_problems(os.path.join(tmp, 'fresh_out'), inputs_root, env={})
        chk('①k 새 빈 폴더 (생산 밖) = 허용', fresh == [], str(fresh))

    def s2():
        # ── ② 인자 끔 패치 · 양성 대조 (실제 생산 함수 · 합성 망) ──
        orig = nc.sigma_AM_relative
        pb = factor_probe(nc)
        chk('②a 합성 PC 만 OFF/ON = 35/8 · SC 만 = 1 (비트) · 혼합 ∉ {1, 35/8} · 두 모드 · 복원 → 양성 대조 통과', pb.get('passed') is True,
            str([c for c in pb.get('checks', []) if not c['ok']]))

        @contextlib.contextmanager
        def noop_patch(nc_):
            yield None
        pn = factor_probe(nc, noop_patch)
        chk('②b 패치가 아무것도 안 하면 (no-op) 양성 대조 실패', pn.get('passed') is False)
        inside = None
        try:
            with factor_off(nc):
                inside = nc.sigma_AM_relative(4.5, 'AM_P')
                raise RuntimeError('일부러')
        except RuntimeError:
            pass
        chk('②c 패치 안 = σ_rel(4.5, AM_P) 1', inside == 1.0, repr(inside))
        chk('②d 예외 뒤에도 원 함수 복원 · PC 인자 8/35', nc.sigma_AM_relative is orig and abs(orig(4.5, 'AM_P') - 8 / 35) < 1e-15)
        chk('②e 모듈 기준값 불변 (0.05)', nc.SIGMA_AM_ELECTRONIC == SIGMA_BASE_S_CM)
        mixed = next(((c.get('value') or {}).get('q_raw') for c in pb.get('checks', []) if 'hertzian/mixed' in c.get('name', '')), None)
        chk('②f 혼합 Hertz FULL OFF/ON = Codex 3.154656902 (배율 아님)', mixed is not None and abs(mixed - 3.154656902) < 1e-8, repr(mixed))

    def s3():
        # ── ③ 대조 팔 관문 ──
        case = synthetic_case('mixed')
        rec, _, _ = run_arm(nc, case, ARMS[0])
        arc_ok = dict(q=rec['q_raw'], n_nodes=rec['n_nodes'], n_edges=rec['n_edges'], boundary_rule=rec['boundary_rule'],
                      geometry=rec['certificate']['geometry'])
        chk('③a 같은 값 = 통과', control_problems(rec, arc_ok) == [])
        chk('③b 저장 q 상대 1e-6 어긋남 = 거부', control_problems(rec, dict(arc_ok, q=arc_ok['q'] * (1 + 1e-6))) != [])
        chk('③c 간선 수 다름 = 거부', control_problems(rec, dict(arc_ok, n_edges=arc_ok['n_edges'] + 1)) != [])
        chk('③d 기하 다름 = 거부', control_problems(rec, dict(arc_ok, geometry=dict(arc_ok['geometry'], plate_z=1.0))) != [])
        chk('③e 저장 q 없음 = 거부', control_problems(rec, dict(arc_ok, q=None)) != [])
        # 가드에 걸린 풀이 (Codex 반례 꼴 — 일부러 작은 상자 4 µm · 인자 끔이면 FULL q > 1.5 → 솔버가 거부) 의 전류로 값을 만들지 않는다
        g_off, _, _ = run_arm(nc, synthetic_case('mixed', box=4.0), ARMS[1])
        chk('③f 가드 거부 풀이 = q_raw None (표에 안 감) · 진단 칸에만', g_off.get('q_raw') is None and g_off.get('status') != 'computed'
            and g_off.get('q_cert_unaccepted') is not None and g_off.get('certificate_problem'), repr({k: g_off.get(k) for k in ('status', 'q_raw', 'q_cert_unaccepted')}))

    def s4():
        # ── ④ 끝-끝 (합성 다섯 케이스 · CSV · tgz · 실제 생산 함수) ──
        world = _make_synthetic_world(os.path.join(tmp, 'world'), nc)
        a_sha = sha256_file(world['tgz'])
        cur = code_state(ROOT)
        kw = dict(registered=world['registered'], tsv_path=world['tsv'], archive_path=world['tgz'], expected_archive_sha=a_sha,
                  expected_nc_sha=cur['network_conductivity_sha256'], expected_code_fp=cur['code_fp'], require_clean=False, log=quiet)
        st.update(world=world, a_sha=a_sha, kw=kw, out1=os.path.join(tmp, 'out1'))
        rc, man = run(ROOT, world['inputs_root'], st['out1'], **kw)
        st['man'] = man
        chk('④a 정상 = rc 0 · manifest.json · 다섯 ok', rc == 0 and man is not None and os.path.isfile(os.path.join(st['out1'], 'manifest.json'))
            and [c['status'] for c in man['cases']] == ['ok'] * 5, f'rc {rc}')
        byid = {c['case_id']: c for c in (man or {}).get('cases', [])}
        chk('④b SC 만 = 인자 끔 q 와 켬 q 비트 같음 (G4)', (byid.get('syn_sc') or {}).get('derived', {}).get('sc_only_off_equals_on') is True)
        r_pc = (byid.get('syn_pc') or {}).get('derived', {}).get('off_over_on_hertzian')
        chk('④c PC 만 (균일 반경) OFF/ON = 35/8 (기록)', r_pc is not None and abs(r_pc - PC_RATIO) < 1e-12, repr(r_pc))
        r_mx = (byid.get('syn_37') or {}).get('derived', {}).get('off_over_on_hertzian')
        chk('④d 혼합 OFF/ON ≠ 35/8 (보간 · 배율 금지 근거)', r_mx is not None and abs(r_mx - PC_RATIO) > 1e-3, repr(r_mx))
        m_main = ((byid.get('syn_37') or {}).get('arms') or {}).get('main_hertz_off') or {}
        chk('④e 주 팔 증서 σ_bulk = 0.0041 · 표 σ = q × 4.1', (m_main.get('certificate') or {}).get('sigma_bulk_S_cm') == SIGMA_REF_S_CM
            and m_main.get('q_raw') is not None and abs(m_main['sigma_mScm_unrounded'] - m_main['q_raw'] * 4.1) < 1e-12 * max(1.0, m_main['q_raw'] * 4.1))
        tp = os.path.join(st['out1'], 'factor_off_electronic.tsv')
        rows = list(csv.DictReader(open(tp, encoding='utf-8'), delimiter='\t')) if os.path.isfile(tp) else []
        chk('④f 표 다섯 행 · 등록 순서 · 값 채움', [r['case_id'] for r in rows] == [c for c, _ in world['registered']]
            and all(r['main_sigma_ref_mScm'] for r in rows))
        mk = {k: kw[k] for k in ('registered', 'expected_nc_sha', 'expected_code_fp', 'expected_archive_sha')}
        st['mk'] = mk
        chk('④g manifest 다시 검사 = 문제 0', man is not None and manifest_problems(man, out_dir=st['out1'], **mk) == [])
        rc2, _ = run(ROOT, world['inputs_root'], st['out1'], **kw)
        chk('④h 같은 --out 다시 (비어 있지 않음) = rc 2', rc2 == 2)
        rc3, _ = run(ROOT, world['inputs_root'], os.path.join(world['inputs_root'], 'x'), **kw)
        chk('④i --out 이 입력 뿌리 안 = rc 2 · 쓰기 없음', rc3 == 2 and not os.path.exists(os.path.join(world['inputs_root'], 'x')))
        rc4, _ = run(ROOT, world['inputs_root'], os.path.join(tmp, 'out4'), **dict(kw, registered=world['registered'][:4]))
        chk('④j 등록 표 ≠ 등록 케이스 (넷) = rc 2 · 쓰기 없음', rc4 == 2 and not os.path.exists(os.path.join(tmp, 'out4')))
        rc5, _ = run(ROOT, world['inputs_root'], os.path.join(tmp, 'out5'), **dict(kw, expected_nc_sha='0' * 64))
        chk('④k network_conductivity.py 해시 ≠ 등록 = rc 2 · 쓰기 없음', rc5 == 2 and not os.path.exists(os.path.join(tmp, 'out5')))
        rc6, _ = run(ROOT, world['inputs_root'], os.path.join(tmp, 'out6'), **dict(kw, expected_archive_sha='f' * 64))
        chk('④l 원자료 tgz 해시 ≠ 등록 = rc 2', rc6 == 2 and not os.path.exists(os.path.join(tmp, 'out6')))
        rc7, _ = run(ROOT, world['inputs_root'], os.path.join(tmp, 'out7'), **dict(kw, patcher=lambda nc_: contextlib.nullcontext()))
        chk('④m 패치가 안 켜지면 (no-op) = rc 2 · 쓰기 없음', rc7 == 2 and not os.path.exists(os.path.join(tmp, 'out7')))
        # 대조 불일치: 케이스 하나의 contacts.csv 첫 접촉 면적 × 1.5 (행 수 같음) → control_mismatch · 그 행 값 비움 · rc 1
        cpath = os.path.join(world['inputs_root'], 'syn_55', 'contacts.csv')
        orig_bytes = open(cpath, 'rb').read()
        lines = orig_bytes.decode().splitlines()
        first = lines[1].split(',')
        first[8] = repr(float(first[8]) * 1.5)
        open(cpath, 'w', encoding='utf-8', newline='\n').write('\n'.join([lines[0], ','.join(first)] + lines[2:]) + '\n')
        try:
            out8 = os.path.join(tmp, 'out8')
            rc8, man8 = run(ROOT, world['inputs_root'], out8, **kw)
            st8 = {c['case_id']: c['status'] for c in (man8 or {}).get('cases', [])}
            t8 = os.path.join(out8, 'factor_off_electronic.tsv')
            rows8 = list(csv.DictReader(open(t8, encoding='utf-8'), delimiter='\t')) if os.path.isfile(t8) else []
            chk('④n 입력이 저장 실행과 다르면 control_mismatch · 그 행 값 비움 · 다섯 행 그대로 · rc 1',
                rc8 == 1 and st8.get('syn_55') == 'control_mismatch' and len(rows8) == 5
                and [r['main_sigma_ref_mScm'] for r in rows8 if r['case_id'] == 'syn_55'] == [''], f'rc {rc8} {st8}')
        finally:
            open(cpath, 'wb').write(orig_bytes)
        # 기하 어긋남: mesh_info.json plate_z × 1.01 → inputs_refused · rc 1
        mpath = os.path.join(world['inputs_root'], 'syn_73', 'mesh_info.json')
        mo = open(mpath, 'rb').read()
        json.dump(dict(plate_z=json.loads(mo)['plate_z'] * 1.01), open(mpath, 'w'))
        try:
            rc9, man9 = run(ROOT, world['inputs_root'], os.path.join(tmp, 'out9'), **kw)
            st9 = {c['case_id']: c['status'] for c in (man9 or {}).get('cases', [])}
            chk('④o 기하 ≠ 저장 증서 = inputs_refused · rc 1', rc9 == 1 and st9.get('syn_73') == 'inputs_refused', f'rc {rc9} {st9}')
        finally:
            open(mpath, 'wb').write(mo)
        rcc, _ = run(ROOT, world['inputs_root'], os.path.join(tmp, 'outc'), **dict(kw, check_only=True))
        chk('④p --check-only = rc 0 · 쓰기 없음', rcc == 0 and not os.path.exists(os.path.join(tmp, 'outc')))

    def s5():
        # ── ⑤ manifest 필수 칸 · 등록 값 (거부) ──
        man, mk, out1 = st.get('man'), st.get('mk'), st.get('out1')
        if not man or not mk:
            raise RuntimeError('④a manifest 없음 — ⑤ 전제 실패')
        missing = [k for k in MANIFEST_REQUIRED if not manifest_problems({x: v for x, v in man.items() if x != k}, **mk)]
        chk('⑤a 필수 칸 하나씩 지우기 = 전부 거부', missing == [], str(missing))

        def mutated(**over):
            m2 = json.loads(json.dumps(man))
            m2.update(over)
            return manifest_problems(m2, **mk)
        arms2 = [dict(a) for a in ARMS]
        arms2[1]['factor'] = 'on'
        chk('⑤b 주 팔 인자 켬 = 거부', mutated(arms=arms2) != [])
        arms3 = [dict(a) for a in ARMS]
        arms3[1]['contact_mode'] = 'physics'
        chk('⑤c 주 팔 physics = 거부', mutated(arms=arms3) != [])
        chk('⑤d σ_ref 0.05 = 거부', mutated(sigma_ref_S_cm=0.05) != [])
        chk('⑤e 케이스 하나 빠짐 = 거부', mutated(cases=man['cases'][:4]) != [])
        chk('⑤f 케이스 중복 = 거부', mutated(cases=man['cases'] + man['cases'][:1]) != [])
        chk('⑤g 봉인 해시 전후 다름 = 거부', mutated(code=dict(man['code'], code_hashes_after={'x': 'y'})) != [])
        chk('⑤h 양성 대조 실패 기록 = 거부', mutated(factor_probe=dict(before=dict(passed=False), after=dict(passed=True))) != [])
        chk('⑤i git dirty (깨끗함 요구) = 거부', mutated(git=dict(man['git'], dirty=True, clean_required=True)) != [])
        chk('⑤j 계산된 팔에 증서 없음 = 거부', mutated(cases=[dict(c, arms={k: dict(v, certificate=None) for k, v in c['arms'].items()})
                                                     for c in json.loads(json.dumps(man['cases']))]) != [])
        chk('⑤k factor_patch 표지 바뀜 = 거부', mutated(factor_patch=dict(FACTOR_PATCH, source_files_modified=True)) != [])
        chk('⑤l 입력 바뀜 기록 = 거부', mutated(production_inputs_unchanged=False) != [])
        tpath = os.path.join(out1, 'factor_off_electronic.tsv')
        tb = open(tpath, 'rb').read()
        try:
            open(tpath, 'ab').write(b'# tampered\n')
            chk('⑤m 산출 파일이 manifest 해시와 다르면 = 거부', manifest_problems(man, out_dir=out1, **mk) != [])
        finally:
            open(tpath, 'wb').write(tb)
        chk('⑤n 되돌리면 = 문제 0', manifest_problems(man, out_dir=out1, **mk) == [])
        outf = os.path.join(tmp, 'outf')
        os.makedirs(outf)
        open(os.path.join(outf, 'factor_off_electronic.tsv'), 'w').write('x\n')
        rcf, _ = finalize(outf, {x: v for x, v in man.items() if x != 'git'}, log=quiet, **mk)
        chk('⑤o finalize 거부 = rc 2 · manifest.json 없음 · REFUSED 표지', rcf == 2 and not os.path.exists(os.path.join(outf, 'manifest.json'))
            and os.path.isfile(os.path.join(outf, 'manifest.REFUSED.json')) and os.path.isfile(os.path.join(outf, 'factor_off_electronic.REFUSED.tsv')))

    def s6():
        # ── ⑥ 등록 상수 (결과 전 고정 · 실제 리포 파일) ──
        regd = load_registered(os.path.join(ROOT, TSV_REL), os.path.join(ROOT, ARCHIVE_REL))
        chk('⑥a 등록 다섯 ID = 리포 표 · 원자료 tgz 해시 = 등록 (실제 파일)', regd['problems'] == [], str(regd['problems']))
        chk('⑥b 주 팔 = hertzian · 끔 · 0.0041 · 감도 = physics · 끔',
            ARMS[1] == dict(name='main_hertz_off', contact_mode='hertzian', factor='off', sigma_S_cm=0.0041, role='main')
            and ARMS[3]['contact_mode'] == 'physics' and ARMS[3]['factor'] == 'off')
        qh = {cid: ((regd['cases'].get(cid) or {}).get('modes', {}).get('hertzian') or {}).get('q') for cid, _ in REGISTERED_CASES}
        chk('⑥c 저장 증서 q × 4.1 = Codex 환산 (0:10 0.390802 · 10:0 0.106783 · 6 자리)',
            None not in qh.values() and round(qh['260925_000001_0bee25'] * 4.1, 6) == 0.390802
            and round(qh['260922_222828_6e4ff6'] * 4.1, 6) == 0.106783, repr(qh))
        nb = {cid: regd['cases'][cid]['modes']['physics']['area_binding_counts_physics'] for cid, _ in REGISTERED_CASES}
        chk('⑥d 저장 전자 Physics 결속 = 전부 native_unsupported_pair (PS45E-02 근거)',
            all(list((v or {}).keys()) == ['native_unsupported_pair'] for v in nb.values()), repr(nb))

    try:
        for label, fn, n in (('①', s1, 11), ('②', s2, 6), ('③', s3, 6), ('④', s4, 16), ('⑤', s5, 15), ('⑥', s6, 4)):
            section(label, fn, n)
    finally:
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    n = ok + len(bad)
    print(f'ps45_sigmae_factor_off_variant selftest {ok}/{n}' + ('' if not bad else '\n  FAIL: ' + '\n  FAIL: '.join(bad)))
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='ps45 σ_e 보고 전용 실행 변형 (PC 크기 인자 끔 · 공통 기준값 4.1 mS/cm · 다섯 전자 망) — 등록 '
                                             + REG_DOC)
    ap.add_argument('--inputs-root', help='저장 g2 배치의 케이스 결과 폴더 (<배치>/work/results — 읽기만)')
    ap.add_argument('--out', help='새 빈 출력 폴더 (리포 · 입력 뿌리 · 배치 출력 · 웹앱 서빙 폴더 밖)')
    ap.add_argument('--check-only', action='store_true', help='관문만 (등록 · 코드 · 출력 폴더 · 케이스 입력 기하) — 풀이 · 쓰기 없음')
    ap.add_argument('--selftest', action='store_true', help='자체시험 (반례 · 합성 다섯 케이스 끝-끝)')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.inputs_root or not a.out:
        ap.error('--inputs-root 와 --out 이 필요하다')
    rc, _ = run(ROOT, a.inputs_root, a.out, check_only=a.check_only)
    return rc


if __name__ == '__main__':
    sys.exit(main())
