#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WSL 소형 통합 시험 — 실제 웹앱 파이프라인 · 격리 출력 (Codex RGLR 3차 재검증 10-05 *"격리된 WSL 소형 통합시험 착수 조건부 GO"*).

⛔ 공식 결과 · 인계 · 봉인이 아니다 — 새 ROOT (비어 있지 않으면 거부) 안에만 쓴다 (WEBAPP_*_FOLDER · TMPDIR · cwd 전부 ROOT 안 ·
   원격 저장소 끔 · 그림 · 자동 DB 끔).  리포의 추적 파일을 건드리지 않는다 (피복 단계의 실행 위치 상대 쓰기 LHS-27 도 ROOT 안으로).

케이스 (각각 **자식 프로세스** — 케이스마다 경과 · 최대 RSS (os.wait4) · user/sys 를 잰다 · 194 실행기와 같은 단일 스레드 env):
  A  real_14 (리포 `docs/data/real14_reference_20260928/` — atom · contact .gz · 메시 · 덱 · sha256 = README 표)
       a) 일반 경로 + **실제 Stage E** (figures · auto_db 끔)      b) `stop_after='network'`
     case15 (리포 `docs/data/case15_corner_20261001/` — 같은 꼴 · ★ 10-07 Codex 세대 2 재검증 §7-4) — `stop_after='network'` (`--skip-case15`)
       ★ 10-07 G2RR4-03 (재검증 4 §6-3(b)) = **음성 대조** (`CASE15_NEGCTL`): 게시 차단 · τ 비노출 · 원인 발화 (원덤프 직접 6 조합 — 전자 · Hertz 열 B∩T 넷 ·
       Physics 열 음수 면적 거부) · 이온 정상 이 `[음성 대조]` 검사 넷으로 실제 발화해야 PASS (whitelist 아님 · 등록 §9-4 제안 · ⬜ 1저자 비준)
       ★ 10-08 G2RR5-02 (재검증 5 §2) — + ⑤ 실제 망 시도: 기록기 (`network_cli_recorder` — `pipeline_service._RUNNER` 를 그대로 통과 · 봉인 무변경) 가 이번 시도의
       망 CLI 호출 · 예외 · rc · per-mode 산출물 (sha256 · 채널 상태 · 사유) 을 적고, 그것이 등록한 내용 거부 (실패 넷 · 이온 정상) 여야 PASS — 예외 · rc ≠ 0 ·
       per-mode 없음 = TECH (실행 실패 · PASS 아님 → rc 1).  단계 기록은 구조 필드 (missing_outputs · stale_outputs · verify_failed) 를 남긴다
     ⇒ 게시된 증서 · 도장 · 진단 상태 · 열 역할 · 인계 출처 관문의 다시 읽기 = `scripts/g2_network_reread.py --smoke-root <ROOT>` (이 도구는 게시까지)
  B  LHS 코호트 (원자료 = 코호트 TSV 경로 · 같은 프레임 관문 = `lhs_webapp_batch.stage_case` · `resolve_mode` 그대로) — `stop_after='network'`
       기본 고르기 (커밋된 인계표 · 수확 JSON 에서 · 접촉 수 가장 작은 것): 관통 bimodal (lhs) · 비관통 (lhs) · lhsx 한 건
  C  음성 대조 (합성 침대 · 실 network CLI 같은 프로세스 · `webapp/test_pipeline_provenance` 의 도구 · Codex 탐침과 같은 주입) —
       **기대 = 다른 에이전트의 수정 (RGLR2-01 · 02 · 03) 뒤 동작**.  지금 코드에서는 FAIL 이 정상이다 (수정 전 기준선).
       C1 일반 경로 σ_ratio ×4 → failed (+ 양성 대조: 변조 없는 일반 경로 = done)    C1b 일반 경로 L1 + σ_ratio None → failed
       C2 게시 중 I/O 실패 둘 (성공 시도 쓰기 · full_metrics 되돌림) → '되돌림 실패' 상태 (이전 세대 보존 주장 금지) (+ 양성 대조: 한 번 실패 = 이전 세대 그대로)
       C3 거의 정수압 VM 쌍 (순수 함수) → CV 0 (`--vm-expect null` 이면 계산 안 함 = null)

판정 — 케이스 · 대조마다 PASS/FAIL (데이터로).  `smoke_report.json` 하나 + `smoke_summary.txt` 짧은 요약.
  rc 0 = 전부 PASS · 1 = 실데이터 (A · B) 검사 FAIL (또는 TECH = 실행 실패) 있음 · 2 = C (음성 대조) 만 FAIL (수정 전 코드에서 기대되는 결과) · 3 = 사용 오류

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


#: ★ 10-07 G2RR4-03 (Codex 세대 2 재검증 4 §6-3(b)) — case15 = **음성 대조** (얇은 corner 침대 · 판 간격 19.1455 µm < 4 r_AM): 이온 채널은 정상으로 풀리고, 전자 두 모드 ·
#:   Hertz 열 = 띠 겹침 (boundary_overlap · B∩T 입자 ID 24 · 40 · 57 · 103) · Physics 열 = 음수 원자료 접촉 면적 거부 (두 행 31–29241 · 38–29241) → 망 게시 차단 (WEB-03 Q1).
#:   그 지정한 실패가 **실제로 발화해야** PASS — whitelist · 이름으로 PASS 하지 않는다 · 스모크 전체를 소급 "기대대로" 로 바꾸지 않는다 (원 실패 기록 = 등록 §9-2 · 10-07 14:15 ·
#:   이 기대 = 등록 §9-4 제안 · ⬜ 1저자 비준).  이온 참고값 = Codex 재검증 4 §6-1 직접 풀이 (σ_ratio 8 자리 · 우리 재현 같음) · 증서 문턱 = network_conductivity 1e-6.
CASE15_NEGCTL = dict(tag='case15_publication_blocked', b_and_t_ids=(24, 40, 57, 103), negative_rows=((31, 29241), (38, 29241)),
                     ionic_ref8={'hertzian': 0.00032635, 'physics': 0.00036225}, cert_max=1e-6,
                     overlap_channels=('electronic_hertzian', 'electronic_physics', 'thermal_hertzian'), refuse_channel='thermal_physics',
                     refuse_text='ligg_area < 0', solver_step='Network Solver (both modes)',
                     #  ★ 10-08 G2RR5-02 (Codex 세대 2 재검증 5 §2) — 실제 망 시도 (⑤): 이번 시도의 망 CLI = 정확히 1 회 · 예외 없음 · rc 0 · per-mode 둘 → 그 산출물의
                     #    채널 상태 · 사유 (`{채널}_status` · `{채널}_status_reason`) 가 아래 표 그대로.  값 = 10-08 이 컨테이너 실제 case15 (커밋된 원자료 · 통과 기록기로
                     #    엿본 첫 실행 · WSL 10-07 제출 기록의 시도 사유와 같다): 실패 상태 = 'failed' (`pipeline_service._CHANNEL_FAIL_STATES`) · 겹침 사유 = 생산자
                     #    `_channel_solve_failure` 가 `network_conductivity.BOUNDARY_OVERLAP_REASON` 을 괄호로 싣는 꼴 · Physics 열 = 솔버 ValueError 그대로
                     #    (원자료 탐침의 오류 문자열과 같은 바이트) · 이온 두 모드 = 'computed' (사유 칸 없음)
                     attempt_modes=('hertzian', 'physics'), attempt_channels=('ionic', 'electronic', 'thermal'),
                     attempt_ok_status='computed', attempt_fail_status='failed', overlap_token='(boundary_overlap)', overlap_reason='boundary_overlap',
                     refuse_prefix='ValueError: ',
                     attempt_table={'hertzian.ionic': 'computed', 'physics.ionic': 'computed',
                                    'hertzian.electronic': 'boundary_overlap', 'physics.electronic': 'boundary_overlap',
                                    'hertzian.thermal': 'boundary_overlap', 'physics.thermal': 'ligg_area_negative'})

#: ★ 10-08 G2RR5-02 (Codex 세대 2 재검증 5 §2 · Q2 (가) 봉인 밖) — 실제 망 시도 기록기 (`network_cli_recorder` · 음성 대조 표지가 있을 때만 `child_case`).
#:   `pipeline_service._RUNNER` (봉인 쪽이 주입용으로 둔 모듈 훅 · 봉인 파일 무변경) 를 **그대로 통과시키며** 망 CLI (cmd[1] = network_conductivity.py) 호출마다
#:   호출 수 · 입력 CSV 둘의 `pipeline_service.file_digest` (시도 기록 input_digests 와 같은 함수) · 예외 종류 (적고 다시 올린다) · returncode · 반환 **직후**
#:   (봉인 쪽 내용 검증 · 후보 폐기 전) per-mode 두 JSON 의 sha256 · 채널마다 상태 · 사유를 적는다 (읽기만) → 보고 `attempt_evidence`.
ATTEMPT_EVIDENCE_SCHEMA = 'wsl_network_smoke/attempt_evidence/v1'
NETWORK_CLI = 'network_conductivity.py'
NETWORK_MODES = ('hertzian', 'physics')


def _per_mode_read(out_dir, channels) -> dict:
    """망 CLI 반환 직후 per-mode JSON 둘 → {모드: None (파일 없음) | dict(sha256 · bytes · channels {채널: dict(status, reason)} · read_error)} (읽기만)."""
    pm = {}
    for m in NETWORK_MODES:
        p = (Path(out_dir) / f'network_conductivity_{m}.json') if out_dir else None
        if p is None or not p.is_file():
            pm[m] = None
            continue
        d = dict(sha256=None, bytes=None, channels=None, read_error=None)
        try:
            b = p.read_bytes()
            d.update(sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))
            j = json.loads(b.decode('utf-8'))
            if isinstance(j, dict):
                d['channels'] = {ch: dict(status=j.get(f'{ch}_status'),
                                          reason=(None if j.get(f'{ch}_status_reason') is None else str(j.get(f'{ch}_status_reason'))[:600]))
                                 for ch in channels}
            else:
                d['read_error'] = f'JSON 최상위가 객체가 아니다 ({type(j).__name__})'
        except (OSError, ValueError) as e:                  # UnicodeDecodeError ⊂ ValueError
            d['read_error'] = f'{type(e).__name__}: {e}'[:300]
        pm[m] = d
    return pm


@contextlib.contextmanager
def network_cli_recorder(ps):
    """`ps._RUNNER` 를 그대로 통과시키는 기록기로 감싼다 (with 블록 동안) → 기록 dict (calls 목록 — 망 CLI 호출 하나에 하나).
    인자 · 반환 객체 · 예외는 바꾸지 않는다 (기록 자체의 실패는 기록 칸에만) · 끝나면 (예외로 끝나도) 원래 훅으로."""
    ev = dict(schema=ATTEMPT_EVIDENCE_SCHEMA, hook='pipeline_service._RUNNER', calls=[])
    orig = ps._RUNNER
    channels = tuple(getattr(ps, 'NETWORK_CHANNELS', ('ionic', 'electronic', 'thermal')))

    def recorder(cmd, *args, **kwargs):
        try:
            hit = isinstance(cmd, (list, tuple)) and len(cmd) > 1 and Path(str(cmd[1])).name == NETWORK_CLI
        except Exception:                                   # noqa: BLE001 — 판별 실패 = 기록 안 함 (호출은 그대로)
            hit = False
        if not hit:
            return orig(cmd, *args, **kwargs)
        call = dict(n=len(ev['calls']) + 1, script=NETWORK_CLI, input_digests=None, exception=None, exception_text=None,
                    returncode=None, per_mode=None)
        ev['calls'].append(call)
        out_dir = None
        try:
            call['input_digests'] = {Path(str(p)).name: ps.file_digest(str(p)) for p in cmd[2:4]}
            a = [str(x) for x in cmd]
            out_dir = a[a.index('-o') + 1] if '-o' in a[:-1] else None
        except Exception as e:                              # noqa: BLE001 — 기록 실패는 기록으로 (호출은 그대로)
            call['record_error'] = f'{type(e).__name__}: {e}'[:300]
        try:
            res = orig(cmd, *args, **kwargs)
        except BaseException as e:
            call['exception'] = type(e).__name__
            call['exception_text'] = str(e)[:300]
            raise
        try:
            call['returncode'] = getattr(res, 'returncode', None)
            call['per_mode'] = _per_mode_read(out_dir, channels)
        except Exception as e:                              # noqa: BLE001
            call['record_error'] = f'{type(e).__name__}: {e}'[:300]
        return res
    ps._RUNNER = recorder
    try:
        yield ev
    finally:
        ps._RUNNER = orig


def case15_channel_probe(cd: Path, type_map='1:AM_P,2:SE') -> dict:
    """★ 10-07 G2RR4-03 — case15 음성 대조의 원인 증거 (읽기만): 업로드 폴더의 압축 푼 원덤프 (atom · contact) · STL 꼭짓점 (판 높이) · atom BOX (상자) →
    실제 `network_conductivity.build_network` · `solve_network` 를 채널 셋 × 모드 둘 (Codex 재검증 4 탐침 case15_channels 와 같은 꼴 · 문서 상수를 쓰지 않는다).
    → dict(atoms · contacts · plate_um · box_um · negative_area [[id1, id2, µm², δ µm]] · channels {채널_모드: dict(value · status · reason · 보존 · 잔차 · B∩T) | dict(error)})."""
    import network_conductivity as nc
    bed = REFBEDS['case15']
    files = {dst: Path(cd) / dst for _src, dst, _key in bed['files']}
    atom_p = files[bed['atom']]
    contact_p = next(p for n, p in files.items() if n.startswith('contact_'))
    stl_p = next(p for n, p in files.items() if n.endswith('.stl'))

    def rows(p, tag):
        with open(p, encoding='utf-8') as fh:
            head = None
            for line in fh:
                if line.startswith(tag):
                    head = line[len(tag):].split()
                    break
            return [dict(zip(head or [], x.split())) for x in fh if x.strip() and not x.startswith('ITEM')]
    A = {int(r['id']): dict(type=int(r['type']), **{k: float(r[k]) for k in ('x', 'y', 'z', 'radius')}) for r in rows(atom_p, 'ITEM: ATOMS')}
    C = [dict(id1=int(float(r['c_cpl[7]'])), id2=int(float(r['c_cpl[8]'])), contact_area=float(r['c_cpl[22]']), delta=float(r['c_cpl[23]']))
         for r in rows(contact_p, 'ITEM: ENTRIES')]
    zs = [float(s.split()[3]) for s in stl_p.read_text(encoding='utf-8').splitlines() if s.strip().startswith('vertex')]
    plate = sum(zs) / len(zs)
    with open(atom_p, encoding='utf-8') as fh:
        for line in fh:
            if line.startswith('ITEM: BOX BOUNDS'):
                break
        bounds = [[float(x) for x in next(fh).split()[:2]] for _ in range(3)]
    box = [b[1] - b[0] for b in bounds[:2]]
    tm = {int(k): v for k, v in (x.split(':') for x in str(type_map).split(','))}
    se = sorted(t for t, lab in tm.items() if lab == 'SE')
    am = sorted(t for t, lab in tm.items() if lab.startswith('AM'))
    out = dict(atoms=len(A), contacts=len(C), plate_um=round(plate * 1000, 6), box_um=[round(b * 1000, 6) for b in box],
               negative_area=[[c['id1'], c['id2'], round(c['contact_area'] * 1e6, 6), round(c['delta'] * 1000, 6)] for c in C if c['contact_area'] < 0],
               channels={})
    for mode, target in (('ionic', se), ('electronic', am), ('thermal', sorted(se + am))):
        for cm in ('hertzian', 'physics'):
            with contextlib.redirect_stdout(io.StringIO()):
                try:
                    n = nc.build_network(A, C, target, 1000., plate, box_x=box[0], box_y=box[1], type_map=tm, mode=mode, contact_mode=cm)
                    val = nc.solve_network(n, mode='full')
                    si = (n.get('solve_info') or {}).get('full') or {}
                    d = dict(value=list(val) if isinstance(val, (list, tuple)) else val, status=si.get('status'), reason=si.get('reason'),
                             conservation_rel=si.get('conservation_rel'), residual_rel=si.get('residual_rel'),
                             intersection=sorted(int(x) for x in (set(n.get('bottom') or ()) & set(n.get('top') or ()))))
                except Exception as e:                       # noqa: BLE001 — 음성 대조의 기대 거부 (Physics 열) 도 여기로 온다 — 기록한다
                    d = dict(error=f'{type(e).__name__}: {e}')
            out['channels'][f'{mode}_{cm}'] = d
    return out


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
    #  ★ 10-08 G2RR5-02 — 단계 기록은 실행 결과 **구조 필드**를 그대로 남긴다 (missing_outputs · stale_outputs · verify_failed — `run_stage` 의 StageOutcome ·
    #    없는 칸 = None 그대로 · 판정은 이 필드로).  끝 300 자 err 는 사람이 읽는 진단 칸일 뿐 (판정에 쓰지 않는다 · 늘려 grep 하지 않는다 — WEB-05 와 구분).
    stages = [dict(step=s.get('step'), rc=s.get('rc'), ok=s.get('ok'), required=s.get('required'),
                   **{k: (list(s[k]) if isinstance(s.get(k), (list, tuple)) else s.get(k)) for k in ('missing_outputs', 'stale_outputs', 'verify_failed')},
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
    #  ★ 10-08 G2RR5-02 — 음성 대조면 이번 시도의 망 CLI 호출을 그대로 통과시키며 기록한다 (`network_cli_recorder` · 끝나면 원래 훅)
    with (network_cli_recorder(ps) if spec.get('negative_control') else contextlib.nullcontext()) as attempt_ev:
        out = app.run_pipeline(cid, rep['mode'], rep['type_map'], spec.get('scale', 1000), **kw)
    rep.update(collect(app, ps, tf, cid, out, time.monotonic() - t))
    if spec.get('negative_control'):
        #  ★ G2RR4-03 — 음성 대조 (case15): 표지 + 원인 증거 (원덤프 → 실제 build_network · solve_network 6 조합 · 파이프라인 뒤 · 읽기만) — 판정은 부모 evaluate
        #  ★ 10-08 G2RR5-02 — + 실제 시도 증거 (위 기록기 — 원자료 탐침은 보조 증거로 남는다)
        rep['negative_control'] = spec['negative_control']
        rep['attempt_evidence'] = attempt_ev
        try:
            rep['negctl'] = case15_channel_probe(cd, rep['type_map'])
        except Exception as e:                              # noqa: BLE001 — 증거를 못 만들면 그대로 남긴다 (판정 = FAIL)
            rep['negctl'] = dict(error=f'{type(e).__name__}: {e}')
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


def _hex64(s):
    return isinstance(s, str) and len(s) == 64 and all(c in '0123456789abcdef' for c in s)


def _int0(v):
    """정수 0 (bool 아님)."""
    return isinstance(v, int) and not isinstance(v, bool) and v == 0


def _attempt_class(st, ng):
    """기록기가 읽은 per-mode 채널 기록 dict(status, reason) → 등록 표의 분류 (computed · boundary_overlap · ligg_area_negative) · 그 밖 = 그대로 적은 문자열."""
    if not isinstance(st, dict):
        return 'missing'
    s, rs = st.get('status'), ('' if st.get('reason') is None else str(st.get('reason')))
    if s == ng['attempt_ok_status']:
        return 'computed'
    if s == ng['attempt_fail_status'] and ng['overlap_token'] in rs:
        return 'boundary_overlap'
    if s == ng['attempt_fail_status'] and rs.startswith(ng['refuse_prefix']) and ng['refuse_text'] in rs:
        return 'ligg_area_negative'
    return f'{s}: {rs[:80]}'


def _raw_class(d, ng):
    """원자료 탐침 (`case15_channel_probe`) 의 채널 결과 → 같은 분류."""
    if not isinstance(d, dict):
        return 'missing'
    if d.get('error') is not None:
        e = str(d['error'])
        return 'ligg_area_negative' if (e.startswith(ng['refuse_prefix']) and ng['refuse_text'] in e) else f'error: {e[:80]}'
    if d.get('status') == 'computed':
        return 'computed'
    if d.get('reason') == ng['overlap_reason']:
        return 'boundary_overlap'
    return f'{d.get("status")}/{d.get("reason")}'


def case15_attempt_verdict(r, ng=None):
    """★ 10-08 G2RR5-02 (Codex 세대 2 재검증 5 §2) — case15 음성 대조 ⑤ 실제 망 시도 → (판정, 세부).  판정 = PASS · TECH · FAIL.
      TECH (실행 실패 — 지정한 내용 거부가 아니다): 망 CLI 호출 0 회 · 예외 (PermissionError · FileNotFoundError · TimeoutExpired …) · rc ≠ 0 · per-mode 산출물 없음 · 못 읽음 ·
           망 솔버 단계 rc ≠ 0 · 산출 결손 (missing_outputs) · stale
      FAIL: 실제 시도 증거 없음 (기록기 없는 옛 기록) · 호출 2 회 이상 · 단계 기록 결손 · 내용 검증 거부가 아님 · 실패 채널 집합 ≠ 등록 넷 (+ 이온 computed 둘) ·
           Physics 열 거부 문자열 ≠ 원자료 탐침 오류 · 시도 기록 (단계 · 상태 · input_digests) ↔ 기록기 어긋남 · 원자료 탐침과 다른 원인
    300 자 err · 시도 사유 문자열은 보지 않는다 — 기록기의 구조 증거와 단계 구조 필드로만 판정한다."""
    ng = ng or CASE15_NEGCTL
    ev = r.get('attempt_evidence')
    if not isinstance(ev, dict) or not isinstance(ev.get('calls'), list):
        return 'FAIL', '실제 시도 증거 없음 (attempt_evidence) — 이번 망 CLI 시도를 확인할 수 없다 (G2RR5-02 이전 기록 · 기록기 없음)'
    calls = ev['calls']
    if not calls:
        return 'TECH', '망 CLI 호출 0 회 — 솔버가 실행되지 않았다 (lock · 흔적 격리 · 실행 경계) — 지정한 내용 거부가 아니다'
    if len(calls) != 1 or not isinstance(calls[0], dict):
        return 'FAIL', f'망 CLI 호출 {len(calls)} 회 — 정확히 1 회여야'
    c = calls[0]
    if c.get('exception') is not None:
        return 'TECH', f'망 CLI 실행 예외 {c.get("exception")} ({str(c.get("exception_text"))[:120]}) — 실행 실패 (지정한 내용 거부 아님)'
    if not _int0(c.get('returncode')):
        return 'TECH', f'망 CLI rc {c.get("returncode")!r} — 실행 실패 (지정한 내용 거부 아님)'
    pm = c.get('per_mode') if isinstance(c.get('per_mode'), dict) else {}
    miss = [m for m in ng['attempt_modes'] if not (isinstance(pm.get(m), dict) and _hex64(pm[m].get('sha256')) and isinstance(pm[m].get('channels'), dict))]
    if miss:
        return 'TECH', f'per-mode 산출물 없음 · 못 읽음 {miss} — 실행 실패 (지정한 내용 거부 아님)'
    sv = [s for s in (r.get('stages') or []) if isinstance(s, dict) and s.get('step') == ng['solver_step']]
    if len(sv) != 1:
        return 'FAIL', f'망 솔버 단계 기록 {len(sv)} 개 — 하나여야'
    s = sv[0]
    if not _int0(s.get('rc')) or s.get('missing_outputs') != [] or s.get('stale_outputs') != []:
        return 'TECH', (f'망 솔버 단계 rc {s.get("rc")!r} · 산출 결손 {s.get("missing_outputs")!r} · stale {s.get("stale_outputs")!r} — 실행 실패 '
                        '(지정한 내용 거부 아님)')
    if s.get('verify_failed') is not True or s.get('ok') is not False:
        return 'FAIL', f'망 솔버 단계가 내용 검증 거부가 아니다 (verify_failed {s.get("verify_failed")!r} · ok {s.get("ok")!r})'
    got = {f'{m}.{ch}': _attempt_class((pm[m].get('channels') or {}).get(ch), ng) for m in ng['attempt_modes'] for ch in ng['attempt_channels']}
    if got != ng['attempt_table']:
        return 'FAIL', f'실패 채널 집합 ≠ 등록 — 다름 {({k: (v, ng["attempt_table"].get(k)) for k, v in got.items() if v != ng["attempt_table"].get(k)})}'
    raw = (r.get('negctl') or {}).get('channels') if isinstance(r.get('negctl'), dict) else None
    raw = raw if isinstance(raw, dict) else {}
    for k, cls in ng['attempt_table'].items():
        m, ch = k.split('.')
        if cls == 'ligg_area_negative' and ((pm[m].get('channels') or {}).get(ch) or {}).get('reason') != (raw.get(f'{ch}_{m}') or {}).get('error'):
            return 'FAIL', (f'{k} 거부 문자열 ≠ 원자료 탐침 오류 — {((pm[m].get("channels") or {}).get(ch) or {}).get("reason")!r} ↔ '
                            f'{(raw.get(f"{ch}_{m}") or {}).get("error")!r}')
    att = r.get('attempt') if isinstance(r.get('attempt'), dict) else {}
    dg = c.get('input_digests')
    if not (isinstance(dg, dict) and len(dg) == 2 and all(isinstance(v, str) and v for v in dg.values())) or att.get('input_digests') != dg:
        return 'FAIL', f'시도 기록 input_digests {att.get("input_digests")!r} ≠ 기록기 {dg!r} — 이 시도의 입력이 아니다'
    if att.get('stage') != ng['solver_step'] or att.get('latest_attempt_status') != 'failed':
        return 'FAIL', f'시도 기록 단계 {att.get("stage")!r} · 상태 {att.get("latest_attempt_status")!r} — 망 솔버 단계 · failed 여야'
    rawc = {k: _raw_class(raw.get(f'{k.split(".")[1]}_{k.split(".")[0]}'), ng) for k in ng['attempt_table']}
    if rawc != got:
        return 'FAIL', f'원자료 탐침의 원인 ≠ 이번 시도 — 다름 {({k: (got.get(k), v) for k, v in rawc.items() if v != got.get(k)})}'
    return 'PASS', (f'망 CLI 1 회 · rc 0 · per-mode 둘 (sha256 {pm["hertzian"]["sha256"][:12]} · {pm["physics"]["sha256"][:12]}) · 실패 = 등록 넷 · 이온 computed 둘 · '
                    f'단계 rc 0 · 결손 0 · 내용 검증 거부 · 시도 기록 = 망 솔버 단계 · digest {dg} · 원자료 탐침과 같은 원인')


def negative_control_checks(add, ok, cid, r):
    """★ 10-07 G2RR4-03 — case15 음성 대조 판정 (A 묶음 · 이름 앞 '[음성 대조]') — 지정한 실패가 실제로 발화하고 이온 채널은 정상이어야 PASS.
      ① 게시 차단 — status failed · 실패 단계 = 망 솔버 (both modes) · Stage E 안 돌았다 · 반환 run id 없음 (첫 실행 · 활성 세대 없음 = 옛 성공 산출물 재사용 없음)
      ② 인계 숫자 비노출 — τ 세 모드 상태 NOT_COMPUTED (숫자 칸 없음)
      ③ 원인 발화 (원덤프 직접 6 조합) — 전자 두 모드 · Hertz 열 = boundary_overlap · B∩T = 입자 ID 24 · 40 · 57 · 103 · Physics 열 = 음수 원자료 면적 거부 · 음수 행 = 둘
      ④ 이온 정상 — 두 모드 computed · σ_ratio 참고 8 자리 · 증서 보존 · 잔차 < 1e-6
      ⑤ ★ 10-08 G2RR5-02 실제 망 시도 — 이번 시도의 망 CLI 가 실제로 돌아 등록한 내용 사유로 거부됐다 (`case15_attempt_verdict` · 실행 실패 = TECH)
    ③ · ④ (원자료 탐침 · 파이프라인 뒤 별도 계산) 는 보조 증거 — 이번 시도의 원인 증서는 ⑤ 다."""
    ng = CASE15_NEGCTL
    tag = f'{cid}: [음성 대조]'
    add('A', f'{tag} 게시 차단 — failed · 실패 단계 {ng["solver_step"]} · Stage E 안 돌았다 · 반환 run id 없음 (옛 성공 산출물 재사용 없음)',
        ok(r.get('status') == 'failed' and ng['solver_step'] in (r.get('failed_stages') or []) and r.get('stage_e_ran') is False
           and not r.get('returned_network_run_id')),
        f'status {r.get("status")} · 실패 단계 {r.get("failed_stages")} · Stage E {r.get("stage_e_ran")} · run id {r.get("returned_network_run_id")}')
    tau = r.get('tau') or {}
    sts = {m: tau.get(f'ion_net_status_{m}') for m in ('hertz', 'physics', 'hertz_h12')}
    nums = {k: v for k, v in tau.items() if k.startswith(('f_ion_', 'tau2_ion_', 'tau_ion_')) and v not in (None, '')}
    add('A', f'{tag} 인계 숫자 비노출 — τ 세 모드 NOT_COMPUTED · 숫자 칸 없음', ok(set(sts.values()) == {'NOT_COMPUTED'} and not nums), f'{sts} · 숫자 {nums}')
    neg = r.get('negctl') if isinstance(r.get('negctl'), dict) else {}
    ch = neg.get('channels') if isinstance(neg.get('channels'), dict) else {}
    ids = list(ng['b_and_t_ids'])
    ov = {k: ((ch.get(k) or {}).get('reason'), (ch.get(k) or {}).get('intersection')) for k in ng['overlap_channels']}
    refuse = str((ch.get(ng['refuse_channel']) or {}).get('error') or '')
    rows_ = sorted(tuple(int(v) for v in x[:2]) for x in (neg.get('negative_area') or []) if isinstance(x, (list, tuple)) and len(x) >= 2)
    add('A', f'{tag} 원인 발화 (원덤프 직접 6 조합) — 전자 두 모드 · Hertz 열 boundary_overlap · B∩T = 입자 ID {ids} · Physics 열 음수 원자료 면적 거부 · '
             f'음수 행 {len(ng["negative_rows"])}',
        ok(bool(ch) and all(v == ('boundary_overlap', ids) for v in ov.values()) and ng['refuse_text'] in refuse
           and rows_ == sorted(ng['negative_rows'])),
        f'겹침 {ov} · Physics 열 {refuse[:120]!r} · 음수 행 {rows_} · 증거 오류 {neg.get("error")}')
    ion = {}
    for m, ref in ng['ionic_ref8'].items():
        d = ch.get(f'ionic_{m}') or {}
        v = (d.get('value') or [None, None])
        q = v[1] if isinstance(v, (list, tuple)) and len(v) > 1 else None
        ion[m] = (d.get('status'), None if not isinstance(q, (int, float)) else round(q, 8), d.get('conservation_rel'), d.get('residual_rel'))
    add('A', f'{tag} 이온 정상 — 두 모드 computed · σ_ratio 참고 8 자리 {ng["ionic_ref8"]} · 증서 보존 · 잔차 < {ng["cert_max"]}',
        ok(all(s == 'computed' and q == ng['ionic_ref8'][m] and isinstance(c, (int, float)) and isinstance(e, (int, float))
               and c < ng['cert_max'] and e < ng['cert_max'] for m, (s, q, c, e) in ion.items())), ion)
    v5, d5 = case15_attempt_verdict(r, ng)
    add('A', f'{tag} 실제 망 시도 — 이번 시도의 망 CLI 1 회 · 예외 없음 · rc 0 · per-mode 둘 · 실패 채널 = 등록 넷 (전자 두 모드 · Hertz 열 boundary_overlap · '
             f'Physics 열 음수 면적 거부) · 이온 computed · 단계 rc 0 · 결손 0 · 내용 검증 거부 · 시도 기록 = 기록기 digest · 원자료 탐침과 같은 원인 (실행 실패 = TECH)',
        v5, d5)


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
        if r.get('negative_control') == CASE15_NEGCTL['tag']:
            negative_control_checks(add, ok, cid, r)
            continue
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
def smoke_rc(checks) -> int:
    """rc 규칙 (`run_smoke` · selftest 같은 함수) — 0 = 전부 PASS · 1 = 실데이터 (A · B) 검사가 PASS 아님 (FAIL · ★ 10-08 G2RR5-02 TECH = 실행 실패) ·
    2 = C (음성 대조 대조군) 만 FAIL."""
    if any(c.get('verdict') != 'PASS' and c.get('group') in ('A', 'B') for c in checks):
        return 1
    return 2 if any(c.get('verdict') != 'PASS' and c.get('group') == 'C' for c in checks) else 0


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
    rc = smoke_rc(checks)
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
        lines.append(f'  {"✓" if c["verdict"] == "PASS" else "✗"} [{c["group"]}{"" if c["verdict"] in ("PASS", "FAIL") else " · " + str(c["verdict"])}] '
                     f'{c["name"]}' + (f'  — {c["detail"][:220]}' if c['verdict'] != 'PASS' else ''))
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
        #  ★ G2RR4-03 (Codex 세대 2 재검증 4 §6-3(b)) — 음성 대조: 게시 차단 + 지정한 원인 발화가 기대 (등록 §9-4 제안 · ⬜ 1저자 비준 · 원 실패 기록 §9-2)
        jobs.append(dict(id='case15_network', kind='case15', stop='network', negative_control=CASE15_NEGCTL['tag']))
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


#: ★ 10-08 G2RR5-02 selftest (a) — Codex `r5_case15_pipeline_fault` 꼴: 커밋된 case15 원자료로 실제 child_case 를 **같은 프로세스**에서 돌리되
#:   `pipeline_service._RUNNER` 가 망 CLI (cmd[1] = network_conductivity.py) 호출 **하나만** PermissionError 로 거부한다 (소스 무변경 · 다른 단계는 원래 실행기).
#:   자식 프로세스 (부트 = 이 문자열) 로 띄워 env · cwd · import 를 selftest 와 떼어 둔다.  argv = scripts 폴더 · ROOT · 출력 JSON.
_RC15_FAULT_BOOT = r'''
import contextlib, io, json, sys
from pathlib import Path
scripts, root, outp = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
sys.path[:0] = [scripts]
import wsl_network_smoke as smoke
smoke._setup_child_env(root)
import pipeline_service as ps
real, denied = ps._RUNNER, []


def deny(cmd, *a, **k):
    if len(cmd) > 1 and Path(str(cmd[1])).name == 'network_conductivity.py':
        denied.append(Path(str(cmd[1])).name)
        raise PermissionError('smoke selftest injected solver executable denied (G2RR5-02 · Codex r5_case15_pipeline_fault)')
    return real(cmd, *a, **k)


ps._RUNNER = deny
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rep = smoke.child_case(dict(root=str(root), id='case15_network', kind='case15', stop='network',
                                    negative_control=smoke.CASE15_NEGCTL['tag']))
    restored = ps._RUNNER is deny
finally:
    ps._RUNNER = real
outp.write_text(json.dumps(dict(report=rep, denied=len(denied), recorder_restored=restored), ensure_ascii=False, default=str),
                encoding='utf-8')
'''


def _rc15_launch(base: Path) -> dict:
    """★ 10-08 G2RR5-02 selftest — 실제 case15 두 판을 띄운다 (판정 = `_rc15_judge` · selftest 의 마지막 묶음).
    (a) `_RC15_FAULT_BOOT` (망 CLI 만 PermissionError) · (b) 주입 없음 = 실제 `run_smoke` (case15 + 합성 망 정지 한 건 — 인계 도구 다시 읽기의 S0 짝).
    둘 다 자기 ROOT (리포 밖 · cwd · TMPDIR) — 실제 판 ≈ 120 s (이 컨테이너 · WSL 46 s) 라 다른 묶음과 겹쳐 돌린다 (--run-fast 의 180 s 예산)."""
    import threading
    tag = CASE15_NEGCTL['tag']
    ra, rb = base / 'fault', base / 'positive'
    (ra / 'tmp').mkdir(parents=True)
    env = dict(os.environ, **THREAD_ENV, PYTHONDONTWRITEBYTECODE='1', PYTHONUNBUFFERED='1', TMPDIR=str(ra / 'tmp'))
    env.setdefault('MPLBACKEND', 'Agg')
    log_a = open(ra / 'log.txt', 'wb')
    pa = subprocess.Popen([sys.executable, '-c', _RC15_FAULT_BOOT, str(ROOT / 'scripts'), str(ra), str(ra / 'out.json')],
                          cwd=str(ra), env=env, stdin=subprocess.DEVNULL, stdout=log_a, stderr=subprocess.STDOUT)
    res = {}

    def run_b():
        try:
            jobs = [dict(id='case15_network', kind='case15', stop='network', negative_control=tag),
                    dict(id='syn_network', kind='synthetic', bed='se_am', type_map='1:SE,2:AM_P', scale=1, stop='network')]
            res['rc'] = run_smoke(_parse(['--root', str(rb)]), jobs, out=lambda *x, **k: None)
        except BaseException as e:                          # noqa: BLE001 — 판정 쪽이 읽는다
            res['error'] = f'{type(e).__name__}: {e}'
    th = threading.Thread(target=run_b, name='smoke-selftest-case15-positive', daemon=True)
    th.start()
    return dict(base=base, t0=time.monotonic(), pa=pa, log_a=log_a, ra=ra, rb=rb, th=th, res=res)


def _rc15_judge(st: dict, chk) -> None:
    """★ 10-08 G2RR5-02 selftest — 실제 case15 두 판 판정 (a) 주입 = 실제 시도 검사 TECH · case15 PASS 아님 · 스모크 rc 1 /
    (b) 양성 = rc 0 · case15 검사 전부 PASS (실제 시도 포함) · 고정 토큰 / (b) ROOT → 인계 도구 다시 읽기 (--smoke-root) rc 0."""
    st['th'].join(timeout=1500)
    try:
        rc_a = st['pa'].wait(timeout=1500)
    except subprocess.TimeoutExpired:
        st['pa'].kill()
        rc_a = None
    st['log_a'].close()
    wall = round(time.monotonic() - st['t0'], 1)
    ng = CASE15_NEGCTL
    out_a = read_json(st['ra'] / 'out.json') or {}
    rep_a = out_a.get('report') if isinstance(out_a.get('report'), dict) else {}
    cs_a = evaluate({'case15_network': rep_a}, {'case15_network': dict(rc=rc_a)}) if rep_a else []
    c15a = [c for c in cs_a if c['name'].startswith('case15_network:')]
    att_a = next((c for c in c15a if '실제 망 시도' in c['name']), None)
    ev_a = rep_a.get('attempt_evidence') if isinstance(rep_a.get('attempt_evidence'), dict) else {}
    calls_a = ev_a.get('calls') if isinstance(ev_a.get('calls'), list) else []
    sv_a = next((s for s in rep_a.get('stages') or [] if isinstance(s, dict) and s.get('step') == ng['solver_step']), {})
    _src = globals().get('smoke_rc')
    rc_rule_a = _src(cs_a) if _src else (1 if any(c['verdict'] != 'PASS' and c['group'] in ('A', 'B') for c in cs_a) else 0)
    chk(f'★ G2RR5-02 실제 case15 (a · {wall} s) — child_case + pipeline_service._RUNNER 가 망 CLI 만 PermissionError (Codex r5_case15_pipeline_fault 꼴) → '
        f'실제 시도 검사 TECH · case15 PASS 아님 · 스모크 rc 1 (옛: 6/6 PASS) — 판정 {[(c["name"][16:34], c["verdict"]) for c in c15a]} · rc {rc_rule_a}',
        rc_a == 0 and out_a.get('denied') == 1 and out_a.get('recorder_restored') is True and att_a is not None and att_a['verdict'] == 'TECH'
        and bool(c15a) and not all(c['verdict'] == 'PASS' for c in c15a) and rc_rule_a == 1
        and len(calls_a) == 1 and calls_a[0].get('exception') == 'PermissionError'
        and sv_a.get('rc') == 1 and bool(sv_a.get('missing_outputs')) and sv_a.get('verify_failed') is True,
        repr((rc_a, out_a.get('denied'), out_a.get('recorder_restored'), att_a, calls_a[:1], sv_a))[:700])
    rep_b = read_json(st['rb'] / 'smoke_report.json') or {}
    r15 = ((rep_b.get('reports') or {}).get('case15_network')) or {}
    c15b = [c for c in rep_b.get('checks') or [] if str(c.get('name', '')).startswith('case15_network:')]
    att_b = next((c for c in c15b if '실제 망 시도' in c['name']), None)
    ev_b = r15.get('attempt_evidence') if isinstance(r15.get('attempt_evidence'), dict) else {}
    calls_b = ev_b.get('calls') if isinstance(ev_b.get('calls'), list) else []
    pm_b = ((calls_b[0] if calls_b else {}).get('per_mode')) or {}
    tok = {f'{m}.{c}': (((pm_b.get(m) or {}).get('channels') or {}).get(c) or {}) for m in ('hertzian', 'physics') for c in ('ionic', 'electronic', 'thermal')}
    raw_err = ((((r15.get('negctl') or {}).get('channels') or {}).get('thermal_physics')) or {}).get('error')
    pinned = (all(tok[f'{m}.ionic'].get('status') == 'computed' and tok[f'{m}.ionic'].get('reason') is None for m in ('hertzian', 'physics'))
              and all(tok[k].get('status') == 'failed' and '(boundary_overlap)' in str(tok[k].get('reason'))
                      for k in ('hertzian.electronic', 'physics.electronic', 'hertzian.thermal'))
              and tok['physics.thermal'].get('status') == 'failed' and str(tok['physics.thermal'].get('reason')).startswith('ValueError: ')
              and 'ligg_area < 0' in str(tok['physics.thermal'].get('reason')) and tok['physics.thermal'].get('reason') == raw_err)
    sv_b = next((s for s in r15.get('stages') or [] if isinstance(s, dict) and s.get('step') == ng['solver_step']), {})
    chk(f'★ G2RR5-02 실제 case15 (b · 양성) — 주입 없음 (실제 run_smoke) → rc 0 · case15 검사 일곱 전부 PASS (실제 시도 포함) · 망 CLI 1 회 · rc 0 · per-mode 둘 · '
        f'고정 토큰 (failed + "(boundary_overlap)" 셋 · failed + ValueError "ligg_area < 0" = 원자료 탐침 오류 · 이온 computed 둘) · 단계 rc 0 · 결손 0 · 내용 검증 거부 '
        f'— 판정 {[(c["name"][16:34], c["verdict"]) for c in c15b]}',
        st['res'].get('rc') == 0 and len(c15b) == 7 and all(c.get('verdict') == 'PASS' for c in c15b) and att_b is not None
        and len(calls_b) == 1 and calls_b[0].get('exception') is None and calls_b[0].get('returncode') == 0 and pinned
        and sv_b.get('rc') == 0 and sv_b.get('missing_outputs') == [] and sv_b.get('stale_outputs') == [] and sv_b.get('verify_failed') is True,
        repr((st['res'], [(c['name'][16:40], c['verdict'], c['detail'][:80]) for c in c15b if c.get('verdict') != 'PASS'], tok, sv_b))[:900])
    jp = st['base'] / 'reread_positive.json'
    try:
        pr = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'g2_network_reread.py'), '--smoke-root', str(st['rb']), '--json', str(jp)],
                            cwd=str(st['base']), env=dict(os.environ, **THREAD_ENV, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(st['base'])),
                            capture_output=True, text=True, timeout=900)
        prc, ptail = pr.returncode, (pr.stdout + pr.stderr)[-400:]
    except Exception as e:                                  # noqa: BLE001
        prc, ptail = None, f'{type(e).__name__}: {e}'
    jj = read_json(jp) or {}
    mm = {('S0b' if str(m.get('name', '')).startswith('S0b') else str(m.get('name', ''))[:2]): m.get('ok') for m in jj.get('meta') or []}
    chk('★ G2RR5-02 · 03 실제 case15 (b) 스모크 ROOT → 인계 도구 다시 읽기 (g2_network_reread --smoke-root) rc 0 · S0 (합성 망 정지 done · K1–K7 · H1) · '
        'S0b (등록 음성 대조) 통과 — 고친 생산자의 실제 기록을 소비자가 받는다',
        prc == 0 and mm == {'S0': True, 'S0b': True} and jj.get('n_fail') == 0 and len(jj.get('cases') or []) == 1, repr((prc, mm, ptail))[:700])


def _selftest() -> int:
    """이 컨테이너 — 합성 침대 (CSV 입력) 로 **실제 파이프라인**을 돌려 시험 도구 (자식 · 측정 · 수집 · 판정 · 보고) 를 본다.
    음성 대조 판정 함수는 합성 결과로 변별력을 본다 (수정 전 · 뒤 모양 둘 다).  실 음성 대조도 돌려 '판정이 나온다' 만 본다 (값은 코드 세대에 따른다).
    ★ 10-08 G2RR5-02 — 마지막 묶음 = 커밋된 case15 원자료의 실제 두 판 ((a) 망 CLI 만 PermissionError · (b) 주입 없음 + 인계 도구 다시 읽기) — 맨 처음에 띄워
    다른 묶음과 겹쳐 돌리고 맨 끝에 판정한다."""
    fails = []

    def chk(name, okv, why=''):
        print(('  ✓ ' if okv else '  ✗ ') + name + ('' if okv or not why else f'  — {why}'))
        if not okv:
            fails.append(name)
    _rc15_base = Path(tempfile.mkdtemp(prefix='smoke_rc15_')).resolve()
    _rc15 = None
    try:
        _rc15 = _rc15_launch(_rc15_base)
        _selftest_body(chk)
        _rc15_judge(_rc15, chk)
    finally:
        if _rc15 is not None:
            if _rc15['pa'].poll() is None:
                _rc15['pa'].kill()
                _rc15['pa'].wait()
            _rc15['th'].join(timeout=1500)
            with contextlib.suppress(Exception):
                _rc15['log_a'].close()
        shutil.rmtree(_rc15_base, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


def _selftest_body(chk) -> None:
    """`_selftest` 의 합성 · 판정 함수 · 참조 침대 묶음 (실제 case15 두 판과 겹쳐 돈다)."""
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
    #  ★ 10-07 G2RR4-03 (Codex 세대 2 재검증 4 §6-3(b)) — case15 = 음성 대조: 지정한 실패 (게시 차단 · 전자 · Hertz 열 boundary_overlap B∩T 넷 · Physics 열 음수 원자료
    #    면적 거부 · 음수 행 둘) 와 이온 정상 (참고 8 자리 · 증서) 이 **실제로 발화해야** PASS — whitelist · 이름 PASS 아님 (반례 먼저: 옛 판정 = done 이어야 PASS)
    _ng = globals().get('CASE15_NEGCTL') or {}
    _ids = [24, 40, 57, 103]
    #  ★ 10-08 G2RR5-02 — 양성 픽스처의 실제 시도 값 = 이 컨테이너 실제 case15 (커밋된 원자료) 첫 실행: 망 CLI 1 회 · rc 0 · per-mode 둘 · 이온 computed (사유 없음) ·
    #    전자 두 모드 · Hertz 열 failed + '(boundary_overlap)' · Physics 열 failed + 솔버 ValueError (원자료 탐침 오류와 같은 문자열) · 단계 rc 0 · 결손 0 · 내용 검증 거부 ·
    #    시도 기록 = 망 솔버 단계 · input_digests (WSL 제출 기록과 같은 값)
    _DIG = {'atoms.csv': 'e140e28d3daf3ad7', 'contacts.csv': 'bcb53e13d2cc69be'}
    _OVR = '관통 성분은 있는데 {s} 을 풀지 못했다 (boundary_overlap) — 미퍼콜이 아니다 · 수치 실패 = 게시 차단 (WEB-03 Q1 — 일반 · 정지 경로 모두)'
    _REF = 'ValueError: physics_g2: 간선 (31, 29241) — ligg_area < 0 (-0.186036)'
    _NC4 = ['network_conductivity.json', 'network_conductivity_hertzian.json', 'network_conductivity_physics.json', 'network_conductivity_dual.json']

    def _pm(over=None):
        pm = {'hertzian': dict(sha256='1' * 64, channels=dict(ionic=dict(status='computed', reason=None),
                                                           electronic=dict(status='failed', reason=_OVR.format(s='σ_e')),
                                                           thermal=dict(status='failed', reason=_OVR.format(s='κ')))),
              'physics': dict(sha256='2' * 64, channels=dict(ionic=dict(status='computed', reason=None),
                                                          electronic=dict(status='failed', reason=_OVR.format(s='σ_e')),
                                                          thermal=dict(status='failed', reason=_REF)))}
        for k, v in (over or {}).items():
            m, c = k.split('.')
            pm[m]['channels'][c] = v
        return pm

    def _ev(n_calls=1, **call):
        c = dict(n=1, script='network_conductivity.py', input_digests=dict(_DIG), exception=None, exception_text=None, returncode=0, per_mode=_pm())
        c.update(call)
        return dict(schema='wsl_network_smoke/attempt_evidence/v1', hook='pipeline_service._RUNNER',
                    calls=[dict(c, n=i + 1) for i in range(n_calls)])

    def _solver(**kw):
        d = dict(step='Network Solver (both modes)', rc=0, ok=False, required=True, missing_outputs=[], stale_outputs=[], verify_failed=True, err='')
        d.update(kw)
        return [dict(step=s, rc=0, ok=True, required=s != 'Coverage Physics vs Hertzian', missing_outputs=[], stale_outputs=[], verify_failed=False, err='')
                for s in ('Parse', 'Contact Analysis', 'Coverage Physics vs Hertzian')] + [d]

    def _c15(**over):
        ch = dict(ionic_hertzian=dict(value=[0.1704582, 0.0003263508], status='computed', reason='', conservation_rel=2e-9, residual_rel=1e-10,
                                      intersection=[]),
                  ionic_physics=dict(value=[0.1892075, 0.0003622472], status='computed', reason='', conservation_rel=5e-9, residual_rel=1e-10,
                                     intersection=[]),
                  electronic_hertzian=dict(value=[None, None], status='not_computed', reason='boundary_overlap', intersection=list(_ids)),
                  electronic_physics=dict(value=[None, None], status='not_computed', reason='boundary_overlap', intersection=list(_ids)),
                  thermal_hertzian=dict(value=[None, None], status='not_computed', reason='boundary_overlap', intersection=list(_ids)),
                  thermal_physics=dict(error=_REF))
        ch.update(over.pop('channels', {}))
        r = dict(id='case15_network', kind='case15', stop_after='network', negative_control=_ng.get('tag', 'case15_publication_blocked'),
                 status='failed', failed_stages=['Network Solver (both modes)'], stage_e_ran=False, returned_network_run_id=None, raw_sha_ok=True,
                 stages=_solver(),
                 attempt=dict(schema='network_attempt/v2', latest_attempt_status='failed', solver_status='failed', failure_kind='solver',
                              stage='Network Solver (both modes)', input_digests=dict(_DIG),
                              reason=f'… physics.thermal=fail ({_REF})'),
                 attempt_evidence=_ev(),
                 tau={f'ion_net_status_{m}': 'NOT_COMPUTED' for m in ('hertz', 'physics', 'hertz_h12')},
                 negctl=dict(plate_um=19.1455, negative_area=[[31, 29241, -0.186036, 1.05114], [38, 29241, -0.186264, 1.0512]], channels=ch))
        r.update(over)
        return r

    def _c15_eval(rep):
        cs = evaluate({'case15_network': rep}, {'case15_network': dict(rc=0)})
        return [c for c in cs if '[음성 대조]' in c['name']]
    _neg_cases = (
        ('기대 그대로 (게시 차단 · 원인 넷 · 이온 정상)', _c15(), True),
        ('게시됨 (done · run id) — 음성 대조가 발화하지 않았다', _c15(status='done', failed_stages=[], returned_network_run_id='RUN-x'), False),
        ('B∩T ID 둘뿐 (24 · 40)', _c15(channels=dict(electronic_hertzian=dict(value=[None, None], status='not_computed', reason='boundary_overlap',
                                                                           intersection=[24, 40]))), False),
        ('Physics 열이 풀렸다 (음수 면적 거부 없음)', _c15(channels=dict(thermal_physics=dict(value=[1.0, 0.1], status='computed', reason='',
                                                                                  conservation_rel=1e-9, residual_rel=1e-10, intersection=[]))), False),
        ('음수 면적 행 하나', _c15(negctl=dict(_c15()['negctl'], negative_area=[[31, 29241, -0.186036, 1.05114]])), False),
        ('이온 증서 보존 잔차 1e-3', _c15(channels=dict(ionic_hertzian=dict(value=[0.17, 0.0003263508], status='computed', reason='',
                                                                           conservation_rel=1e-3, residual_rel=1e-10, intersection=[]))), False),
        ('τ 숫자 노출 (hertz OK)', _c15(tau={'ion_net_status_hertz': 'OK', 'ion_net_status_physics': 'NOT_COMPUTED',
                                             'ion_net_status_hertz_h12': 'NOT_COMPUTED'}), False),
        ('원인 증거 없음 (negctl 없음)', _c15(negctl=None), False),
    )
    _neg_res = {nm: _c15_eval(rp) for nm, rp, _w in _neg_cases}
    chk('★ G2RR4-03 case15 음성 대조 판정 — 기대 그대로 = [음성 대조] 검사 전부 PASS (4 개 이상) · 게시됨 · B∩T 둘 · Physics 열 풀림 · 음수 행 하나 · 이온 증서 잔차 · '
        'τ 숫자 노출 · 원인 증거 없음 = 각각 FAIL 하나 이상 (옛 판: case15 도 done 이어야 PASS)',
        bool(_ng) and all((len(_neg_res[nm]) >= 4 and all(c['verdict'] == 'PASS' for c in _neg_res[nm])) if w
                          else any(c['verdict'] != 'PASS' for c in _neg_res[nm]) for nm, _rp, w in _neg_cases),
        repr({nm: [(c['name'][:40], c['verdict']) for c in v] for nm, v in _neg_res.items()})[:600])
    _jobs15 = [j for j in build_jobs(_parse(['--root', '/x', '--skip-real14', '--skip-lhs', '--skip-controls'])) if j['id'] == 'case15_network']
    chk('★ G2RR4-03 case15 작업 = 음성 대조 표지 (case15_publication_blocked — 게시 차단 기대) · 망 정지',
        bool(_ng) and len(_jobs15) == 1 and _jobs15[0].get('negative_control') == 'case15_publication_blocked' == _ng.get('tag')
        and _jobs15[0].get('stop') == 'network', repr(_jobs15))
    #  ★ 10-08 G2RR5-02 (Codex 세대 2 재검증 5 §2) — 실제 망 시도 검사 (반례 먼저 · 옛 판정 = 넷 PASS · 6/6): 이번 시도의 망 CLI 가 실행조차 못 했으면
    #    (예외 · rc ≠ 0 · per-mode 없음) TECH · 돌았는데 등록과 다른 결과 · 증거 없음 · 결합 어긋남 (호출 수 · 시도 기록 digest) = FAIL — 어느 쪽도 PASS 가 아니다.
    #    300 자 문자열을 grep 하지 않는다 — 판정은 기록기의 구조 증거 (호출 · 예외 종류 · rc · per-mode sha256 · 채널 상태 · 사유) 와 단계 구조 필드로.
    _perm = 'PermissionError: smoke selftest injected solver executable denied'
    _none2 = dict(hertzian=None, physics=None)
    _att_vs = (
        ('PermissionError — 단계 rc 1 · per-mode 없음 · 시도 사유 PermissionError (Codex unexpected_failure_record · r5_case15_pipeline_fault 꼴)',
         _c15(stages=_solver(rc=1, missing_outputs=list(_NC4), err=_perm),
              attempt=dict(_c15()['attempt'], reason=f'{_perm}; hertzian: 파일 없음; physics: 파일 없음; per-mode 산출물이 하나도 없다'),
              attempt_evidence=_ev(exception='PermissionError', exception_text='smoke selftest injected', returncode=None, per_mode=_none2)), 'TECH'),
        ('실행 파일 없음 (FileNotFoundError)', _c15(stages=_solver(rc=1, missing_outputs=list(_NC4), err='FileNotFoundError: python'),
                                               attempt_evidence=_ev(exception='FileNotFoundError', returncode=None, per_mode=_none2)), 'TECH'),
        ('시간 초과 (TimeoutExpired)', _c15(stages=_solver(rc=1, missing_outputs=list(_NC4), err='TimeoutExpired: timed out'),
                                          attempt_evidence=_ev(exception='TimeoutExpired', returncode=None, per_mode=_none2)), 'TECH'),
        ('rc 1 + Traceback · per-mode 없음', _c15(stages=_solver(rc=1, missing_outputs=list(_NC4), err='Traceback (most recent call last): …'),
                                                attempt_evidence=_ev(returncode=1, per_mode=_none2)), 'TECH'),
        ('rc 0 인데 per-mode 없음', _c15(stages=_solver(missing_outputs=list(_NC4)), attempt_evidence=_ev(per_mode=_none2)), 'TECH'),
        ('rc 0 · per-mode 있음 · 실패 채널 집합이 다름 (이온 Physics 실패)',
         _c15(attempt_evidence=_ev(per_mode=_pm({'physics.ionic': dict(status='failed', reason=_OVR.format(s='σ_ion').replace('boundary_overlap', 'solve_failed'))}))),
         'FAIL'),
        ('rc 0 · per-mode 있음 · 전자 Hertz 사유가 boundary_overlap 아님',
         _c15(attempt_evidence=_ev(per_mode=_pm({'hertzian.electronic': dict(status='failed', reason=_OVR.format(s='σ_e').replace('boundary_overlap', 'solve_failed'))}))),
         'FAIL'),
        ('망 CLI 두 번', _c15(attempt_evidence=_ev(n_calls=2)), 'FAIL'),
        ('시도 기록 input_digests ≠ 기록기 digest', _c15(attempt=dict(_c15()['attempt'], input_digests=dict(_DIG, **{'atoms.csv': '0' * 16}))), 'FAIL'),
        ('실제 시도 증거 자체가 없음 (G2RR5-02 이전 기록)', _c15(attempt_evidence=None), 'FAIL'),
    )

    def _c15_all(rep):
        cs = evaluate({'case15_network': rep}, {'case15_network': dict(rc=0)})
        return [c for c in cs if c['name'].startswith('case15_network:')]

    def _att(cs):
        return next((c for c in cs if '실제 망 시도' in c['name']), None)
    _pos = _c15_all(_c15())
    _att_res = {}
    for nm, rp, want in _att_vs:
        cs = _c15_all(rp)
        a_ = _att(cs)
        _att_res[nm] = ((a_ or {}).get('verdict'), all(c['verdict'] == 'PASS' for c in cs), want)
    chk('★ G2RR5-02 실제 망 시도 검사 (합성) — 양성 = case15 검사 일곱 전부 PASS (실제 시도 포함) · PermissionError · FileNotFoundError · TimeoutExpired · '
        'rc 1 + Traceback · rc 0 인데 per-mode 없음 = TECH · 다른 실패 채널 집합 둘 · 두 번 · digest 어긋남 · 증거 없음 = FAIL (옛 판정: 전부 6/6 PASS)',
        len(_pos) == 7 and all(c['verdict'] == 'PASS' for c in _pos) and (_att(_pos) or {}).get('verdict') == 'PASS'
        and all(v == want and not allp for v, allp, want in _att_res.values()),
        repr(([(c['name'][16:40], c['verdict']) for c in _pos], {k[:24]: v for k, v in _att_res.items()}))[:700])
    #  ★ 10-08 G2RR5-02 — 기록기는 **그대로 통과**시킨다: 인자 · 결과 객체 · 예외를 바꾸지 않는다 · 망 CLI (cmd[1] = network_conductivity.py) 호출만 적는다 ·
    #    반환 직후 per-mode 두 파일의 sha256 · 채널 상태 · 사유를 읽기만 · 끝나면 (예외로 끝나도) 원래 훅으로
    _rec = globals().get('network_cli_recorder')
    _rec_ok, _rec_why = False, '기록기 없음 (network_cli_recorder — 옛 코드)'
    if _rec is not None:
        import types
        _rt = Path(tempfile.mkdtemp(prefix='smoke_rec_')).resolve()
        try:
            for n_ in ('atoms.csv', 'contacts.csv'):
                (_rt / n_).write_text(n_ * 3, encoding='utf-8')
            seen_, sent_ = [], subprocess.CompletedProcess(['x'], 0, '', '')
            pm_bytes = {}

            def _fake(cmd, *a_, **k_):
                seen_.append((list(cmd), a_, dict(k_)))
                if Path(str(cmd[1])).name == 'network_conductivity.py':
                    if 'boom' in cmd:
                        raise PermissionError('boom')
                    for m_ in ('hertzian', 'physics'):
                        b_ = json.dumps({'ionic_status': 'computed', 'electronic_status': 'failed', 'electronic_status_reason': f'x (boundary_overlap) {m_}',
                                         'thermal_status': 'computed'}).encode()
                        (_rt / f'network_conductivity_{m_}.json').write_bytes(b_)
                        pm_bytes[m_] = hashlib.sha256(b_).hexdigest()
                return sent_
            ns_ = types.SimpleNamespace(_RUNNER=_fake, file_digest=lambda p: 'd:' + Path(str(p)).name, NETWORK_CHANNELS=('ionic', 'electronic', 'thermal'))
            cmd_ = ['py', '/x/scripts/network_conductivity.py', str(_rt / 'atoms.csv'), str(_rt / 'contacts.csv'), '-o', str(_rt), '-t', '1:SE']
            raised_ = None
            with _rec(ns_) as ev_:
                r1_ = ns_._RUNNER(['py', '/x/scripts/parse_liggghts.py', 'a'], capture_output=True, timeout=None)
                r2_ = ns_._RUNNER(cmd_, capture_output=True, timeout=None, cwd=None)
                try:
                    ns_._RUNNER(cmd_ + ['boom'], capture_output=True, timeout=None)
                except PermissionError as e_:
                    raised_ = e_
            back1_ = ns_._RUNNER is _fake
            try:
                with _rec(ns_):
                    raise RuntimeError('body')
            except RuntimeError:
                pass
            back2_ = ns_._RUNNER is _fake
            c0_ = (ev_.get('calls') or [{}])[0]
            c1_ = (ev_.get('calls') or [{}, {}])[-1]
            _rec_ok = (r1_ is sent_ and r2_ is sent_ and isinstance(raised_, PermissionError) and str(raised_) == 'boom' and back1_ and back2_
                       and len(ev_.get('calls') or []) == 2 and seen_[1] == (cmd_, (), dict(capture_output=True, timeout=None, cwd=None))
                       and c0_.get('returncode') == 0 and c0_.get('exception') is None
                       and c0_.get('input_digests') == {'atoms.csv': 'd:atoms.csv', 'contacts.csv': 'd:contacts.csv'}
                       and all((c0_.get('per_mode') or {}).get(m_, {}).get('sha256') == pm_bytes.get(m_) for m_ in ('hertzian', 'physics'))
                       and (c0_.get('per_mode') or {}).get('physics', {}).get('channels', {}).get('electronic') == dict(status='failed',
                                                                                                                  reason='x (boundary_overlap) physics')
                       and c1_.get('exception') == 'PermissionError' and c1_.get('returncode') is None)
            _rec_why = repr((ev_, back1_, back2_))[:600]
        except Exception as e_:                             # noqa: BLE001
            _rec_why = f'{type(e_).__name__}: {e_}'
        finally:
            shutil.rmtree(_rt, ignore_errors=True)
    chk('★ G2RR5-02 기록기 = 그대로 통과 — 망 CLI 아닌 호출 · 망 CLI 호출 모두 같은 결과 객체 · 인자 그대로 · 예외 그대로 다시 올림 (종류 기록) · 망 CLI 만 기록 (입력 digest · rc · '
        'per-mode sha256 · 채널 상태 · 사유) · 끝나면 원래 훅 (몸통이 예외여도)', _rec_ok, _rec_why)
    #  ★ G2RR4-03 — case15 원인 증거를 커밋된 원자료에서 실제로 (실제 build_network · solve_network · 6 조합 · Codex 재검증 4 §6-1 과 같은 꼴) → 음성 대조 판정 통과
    _st15 = Path(tempfile.mkdtemp(prefix='smoke_c15_')).resolve()
    try:
        tm15 = stage_refbed('case15', _st15)['type_map']
        _probe = globals().get('case15_channel_probe')
        t15 = time.monotonic()
        neg15 = _probe(_st15, tm15) if _probe else {}
        v15 = _c15_eval(dict(_c15(), negctl=neg15))
        chk(f'★ G2RR4-03 case15 원자료 직접 6 조합 ({time.monotonic() - t15:.0f} s) — 판 {neg15.get("plate_um")} µm · 음수 면적 행 '
            f'{len(neg15.get("negative_area") or [])} · 전자 · Hertz 열 B∩T = 24 · 40 · 57 · 103 · Physics 열 음수 면적 거부 · 이온 참고 8 자리 · 증서 → '
            '[음성 대조] 원인 · 이온 검사 PASS',
            bool(neg15) and bool(v15) and all(c['verdict'] == 'PASS' for c in v15),
            repr(([(c['name'][:50], c['verdict'], c['detail'][:120]) for c in v15 if c['verdict'] != 'PASS'],
                  {k: (v.get('reason'), v.get('intersection'), v.get('error')) for k, v in (neg15.get('channels') or {}).items()}))[:700])
    finally:
        shutil.rmtree(_st15, ignore_errors=True)
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
