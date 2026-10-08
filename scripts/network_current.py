#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""망 해의 간선별 전류 — 케이스마다 한 번 남기는 덤프 (dump) + DEM 3D 뷰어 '⚡ 전류 흐름' (net_current) 이 읽는 자료 (payload).

왜 따로 있나
  `network_conductivity.py` 는 FULL 풀이마다 간선 전류 I = g·(V1 − V2) 와 노드 전위를 이미 계산한다 (`solve_network(return_field=True)`).
  그러나 그것을 디스크에 쓰는 것은 `--dump-raw-dir` 를 줄 때뿐이고, 웹앱 망 단계 (`app._network_and_stage_e`) 는 그 깃발을 넘기지 않는다
  ⇒ 웹앱 케이스에는 간선 전류가 없다.  망 단계 · 봉인 · 게시 계약은 **건드리지 않는다** — 대신 이 도구가 같은 풀이를 한 번 더 돌린다:

    python3 scripts/network_current.py dump <케이스 결과 폴더>

  · argv = 그 케이스 망 도장 (`network_provenance.json` 의 argv — 웹앱이 실제로 넘긴 type_map · scale · contact_mode) 그대로 + `--dump-raw-dir`.
    도장이 없으면 짐작하지 않는다 (`--type-map` · `--scale` 명시 · 출처 = cli 로 기록).
  · `-o` = **옆 폴더** (임시) — 게시된 네 JSON · 도장 · full_metrics 를 한 바이트도 바꾸지 않는다.  CLI 가 `-o` 에서 읽는 두 파일
    (mesh_info.json → 판 높이 · input_params.json → 상자) 만 사본으로 둔다 (없으면 없는 그대로 — CLI 의 같은 폴백).
  · 입력 해시 (atoms.csv · contacts.csv) 가 도장과 다르면 거부 (다른 침대의 전류가 된다) · 풀이 뒤에도 다시 본다.
  · 옆 폴더 네 JSON 을 게시 네 JSON 과 대조해 manifest 에 남긴다 (identical = 같은 코드 · 같은 입력 · 같은 argv 의 같은 해 ·
    differs = 코드 세대가 다르다 — 뷰어가 경고).  거부하지 않는다 (그림은 지금 코드의 해 — 그 사실을 화면이 말한다).
  · 망 전역 lock (`pipeline_service.network_lock`) 안에서 푼다 — 웹앱 망 풀이와 동시에 돌지 않는다 (OOM · 게시 중 읽기).
  · 결과 = `<결과 폴더>/network_raw_dump/` — 이름이 망 산출물 glob `network_raw_*` (`pipeline_service.NETWORK_ARTIFACT_GLOBS`) 안이라
    다음 망 재계산 (stash) 이 옛 세대와 **함께** 치운다 (성공 = 버림 · 실패 = 되돌림) ⇒ 덤프가 자기 세대보다 오래 남지 않는다.
    둘 = 이온 · 전자 × Hertz · Physics 의 edges · nodes (.csv.gz) + solution (.json) · manifest.json (마지막에 쓴다 · 원자적 교체).
    열 채널은 남기지 않는다 (이 보기의 범위 밖 · real14 원 덤프 96 MB 중 56 MB).

뷰어 자료 (`current_payload` — 웹앱 `/results/<id>/network-current` · `/archive/results/<folder>/network-current`)
  · 상위 N 간선 (|I| 내림차순 · 동률 = id 순) — 양 끝 위치 · 반경 (µm = sim × scale · 3d-data 와 같은 좌표) · |I|/I_전체 · 전위 · 주기 경계 표지
  · ★ 10-07 (1저자 결정 · 웹앱 묶음 #17) — 간선마다 접촉 전류 밀도 j = |I_c| / A_c (A cm⁻² · @1V 프로브) · A_c = 같은 풀이의 접촉 면적
    (덤프 A_used) · 뷰어는 j 로 칠한다 (옛 |I|/I_전체 몫 표시는 없앴다 — 몫 s 는 자료에만 남긴다).  @1C = @1V × I_1C / I_1V (선형) —
    I_1C / A_상자 = j_1C = Q_areal × 1 h⁻¹ (리포 규약 · 케이스 표 등급 Q_areal = grade_engine `__Q_areal_mAhcm2`).  `density` 묶음 참조.
  · 방향 = 전위 강하: a = 높은 전위 끝 (바닥 띠 1 V → 위 띠 0 V · 정확 Dirichlet 프로브 해 — 충방전 방향이 아니다)
  · I_전체 = 해의 G (ΔV = 1 · solution.G_eff) · 한 간선의 |I| ≤ I_전체 (두 단자 저항망 — 등전위면 단면 논증)
  · z-단면 전류 몫 — 두 띠 사이 평면 32 개 (z ≤ z_k 쪽 노드 집합의 단면 전류): 전 간선 Σ = I_전체 (보존 검산) · 상위 N 의 몫 평균 · 최소 · 최대
    (띠 노드 중 전류가 0 이 아닌 것만 띠 범위를 정한다 — 전류 0 인 띠 노드는 단면 합에 기여하지 않는다)
  · 소산 몫 Σ_N I²R / Σ I²R (Tellegen: Σ I²R = ΔV · I_전체 → 검산)
  · 0 전류 간선 (|I| ≤ 1e-12 · I_전체 — 한 띠 안 두 노드 등) 은 돌려주지 않고 센다
  · 게시 σ 대조 (해의 σ/σ₀ 8 자리 = 게시 sigma_full · electronic_sigma_full) · 세대 대조 (manifest run id = 활성 도장 run id · 활성 세대 유효)
  · ★ 10-08 고르기 (1저자 *"애초에 상위 20000 으로만 한 이유 · 좀더 모델 최적화로 숫자 조절"* → Q1 · Q2 권고대로) — `top` 하나로 받는다
    (webapp/app.py = 194 봉인 파일 · 문자열을 그대로 넘긴다):
      정수 N        = 옛 뜻 그대로 (상위 N · 1 … TOP_MAX 로 자름 · 옛 꼴 `edges` · 옛 키 값 무변경 — 키 `selection` 하나만 더함)
      'shareP'      = 전류 몫 P % (1–99) — |I| 큰 순으로 세어 상위 k 접촉의 단면 몫 (32 단면 평균 · 위 z-단면 몫과 같은 잣대) 이 처음 P % 에
                      닿는 k (그 케이스의 전류 분포가 정하는 숫자 · 단면이 없는 해면 경로 기본 TOP_DEFAULT 로 그리고 사유를 적는다)
      'all'         = 0 아닌 전류 접촉 전부
    이름 고르기 (share · all) 는 압축 꼴 (`packing` nodes_v1) — 입자 표 `nodes` (id · x · y · z · r — 옛 꼴과 같은 반올림) 한 번 +
    `edges_c` (a · b = 입자 표 번호 · j) — 값은 옛 꼴과 같고 싣는 꼴만 다르다 (옛 꼴은 접촉마다 양 끝 좌표를 따로 실어 ps45 이온 전부 ≈ 40 만
    접촉 = 101 MB · 압축 꼴 ≈ 19 MB).  `selection` = 고르기 종류 · 개수 · 세 몫 (SHARE_CHOICES) 의 개수 (share_n) · 0 아닌 전류 접촉 수.

  python3 scripts/network_current.py show <케이스 결과 폴더> [--channel ionic] [--mode hertzian] [--top 2000 | share80 | all]   # 경로가 낼 요약
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NC_SCRIPT = os.path.join(HERE, 'network_conductivity.py')

#: 덤프 폴더 — ★ 망 산출물 glob `network_raw_*` 안 (다음 망 재계산이 옛 세대와 함께 치운다).  점 접두 임시 이름은 어떤 glob 에도 안 걸린다.
DUMP_DIRNAME = 'network_raw_dump'
_PARTIAL_PREFIX = '.network_raw_dump.partial-'
_OLD_PREFIX = '.network_raw_dump.old-'
MANIFEST = 'manifest.json'
SCHEMA = 'network_current_dump/v1'
CHANNELS = ('ionic', 'electronic')
MODES = ('hertzian', 'physics')
TOP_DEFAULT = 5000                     # 경로 기본 (top 없음 · CLI) · real14 이온 = 단면 전류 평균 36 % · 10-08 전까지 뷰어 기본이기도 했다
TOP_MAX = 20000                        # 정수 고르기 상한 (옛 꼴 그대로 · 10-06 에 근거 기록 없이 정한 값 — 이름 고르기 share · all 은 이 상한 밖)
SHARE_CHOICES = (50, 80, 95)           # 뷰어가 보이는 전류 몫 (%) — 10-08 1저자 Q1 권고대로
VIEWER_DEFAULT = 'share50'             # 뷰어 기본 (viewer3d.js applyNetCurrentMode 의 top 과 같은 값 — 시험이 대조) · 1저자 Q2 = 전류 50 %
PACKING_COMPACT = 'nodes_v1'           # 이름 고르기의 꼴 — 입자 표 한 번 + 접촉 = 입자 번호 둘 + j
ZCUT_PLANES = 32
ZERO_REL = 1e-12                       # |I| ≤ ZERO_REL · I_전체 = 0 전류 간선 (띠 안 · 막다른 가지)
CLOSE_REL = 1e-9                       # 게시 JSON 대조 — 수치만 이 상대차 안이면 close (같은 해 · 마지막 자리)
NET_FOUR = ('network_conductivity.json', 'network_conductivity_hertzian.json',
            'network_conductivity_physics.json', 'network_conductivity_dual.json')
#: 게시 σ 대조 — 모드 파일 · 채널 키 (생산자 `_run_all_networks` 가 쓰는 이름 그대로)
PUBLISHED_FILE = {'hertzian': 'network_conductivity_hertzian.json', 'physics': 'network_conductivity_physics.json'}
SIGMA_KEY = {'ionic': 'sigma_full', 'electronic': 'electronic_sigma_full'}
#: 채널 키 머리 — 게시 모드 파일에서 그 채널의 증서 · mS/cm 열 (`_run_all_networks` 가 쓰는 이름 그대로)
CHANNEL_PREFIX = {'ionic': '', 'electronic': 'electronic_'}
WEBAPP_CONTACT_MODE = 'both'           # 웹앱 망 단계 argv (`app._network_and_stage_e`) — 그 외 값의 도장은 웹앱 세대가 아니다

#  ★ 10-07 (1저자 결정 · 웹앱 묶음 #17) — 접촉 전류 밀도 (A cm⁻²) · 두 틀 (@1V · @1C)
J_UNIT = 'A cm^-2'
#: 1 µm 정규화 해 → A cm⁻²: 해는 σ₀ = 1 · 길이 µm 로 푼다 (R = L / (σ_rel π r²) [1/µm]) ⇒ I_실 [A] = I_정규 [µm] × σ₀ [S/µm] × 1 V ·
#  σ₀ [S/µm] = σ₀ [S/cm] × 1e-4 · A [cm²] = A [µm²] × 1e-8  ⇒  j [A/cm²] = I_정규 × σ₀ [S/cm] × 1e4 / A [µm²]
J_PER_NORM = 1e4
J_RULE = ('j_c = |I_c| / A_c — I_c = 1 V 프로브 FULL 해의 간선 전류 (바닥 띠 1 V → 위 띠 0 V · 실단위 = 정규화 해 × σ₀ · '
          'j = I_정규 × σ₀ [S/cm] × 1e4 / A [µm²]) · A_c = 같은 풀이가 그 간선에 쓴 접촉 면적 (덤프 A_used: Hertz = c_cpl[22] 원판 · '
          'Physics = 세대 2 면적) · A cm⁻² · 모델의 접촉망 풀이 (측정 전류 아님)')
C1_RULE = ('@1C = @1V × I_1C / I_1V — 선형 환산 (같은 색 · 다른 숫자) · I_1C / A_상자 = j_1C = Q_areal × 1 h⁻¹ (리포 규약 — '
           'mpm_webapp_payload j_1C_mA_cm2 · 뷰어 @1C 운전) · I_1V / A_상자 = ⟨J⟩_1V (이 해의 단면 평균 전류 밀도) · 전류 보존 가정 — '
           '망 전체가 1C 전류를 끝에서 끝까지 나른다고 볼 때의 값 (반응 분포 없음 · 분리막 쪽 단면의 값에 해당)')
C1_SOURCE = ('Q_areal = 케이스 표 등급 축 __Q_areal_mAhcm2 (grade_engine · full_metrics thickness_um · porosity · am_se_ratio + '
             'input_params — 웹앱 _inject_input_params 와 같은 map_input_params) × 1 h⁻¹ = mA cm⁻²')


class DumpRefused(RuntimeError):
    """덤프를 만들지 않는다 — 사유는 메시지 (게시 파일은 그대로)."""


def tag(mode, channel):
    return f'{mode}_{channel}'


def dump_dir(results_dir):
    return os.path.join(results_dir, DUMP_DIRNAME)


def how_to(results_dir):
    """뷰어 · 404 가 보여 주는 한 줄 — 이 프로세스 (웹앱) 의 파이썬 · 이 파일의 절대 경로 · 그 케이스 결과 폴더 (어디서 붙여 넣어도 같은 환경)."""
    return f'{shlex.quote(sys.executable or "python3")} {shlex.quote(os.path.abspath(__file__))} dump {shlex.quote(str(results_dir))}'


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _read_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
        return d if isinstance(d, dict) else None
    except (OSError, ValueError):
        return None


def _find(d, stem):
    """덤프 폴더의 표 — 도구 판 (.csv.gz) 또는 CLI 원 판 (.csv)."""
    for ext in ('.csv.gz', '.csv'):
        p = os.path.join(d, stem + ext)
        if os.path.exists(p):
            return p
    return None


# ═══════════════════════════════ 덤프 (한 번 실행) ═══════════════════════════════

def _webapp_ps():
    """웹앱 `pipeline_service` (도장 · 입력 해시 · 망 lock · 세대 검사 — 사본 금지 · 같은 함수를 부른다)."""
    wa = os.path.join(ROOT, 'webapp')
    if wa not in sys.path:
        sys.path.insert(0, wa)
    import pipeline_service
    return pipeline_service


def _json_diff(a, b, path='', out=None):
    """두 JSON 값의 차이 → out {'n': 수, 'max_rel': 수치 최대 상대차, 'other': 수치 아닌 차이 수, 'first': [경로 …]}."""
    if out is None:
        out = {'n': 0, 'max_rel': 0.0, 'other': 0, 'first': []}

    def _hit(rel=None):
        out['n'] += 1
        if rel is None:
            out['other'] += 1
        else:
            out['max_rel'] = max(out['max_rel'], rel)
        if len(out['first']) < 10:
            out['first'].append(path or '/')
    num = (int, float)
    if isinstance(a, bool) or isinstance(b, bool) or not (isinstance(a, num) and isinstance(b, num)):
        if isinstance(a, dict) and isinstance(b, dict):
            for k in sorted(set(a) | set(b), key=str):
                if k not in a or k not in b:
                    path_k = f'{path}/{k}'
                    out['n'] += 1
                    out['other'] += 1
                    if len(out['first']) < 10:
                        out['first'].append(path_k)
                else:
                    _json_diff(a[k], b[k], f'{path}/{k}', out)
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                _hit()
            for i, (x, y) in enumerate(zip(a, b)):
                _json_diff(x, y, f'{path}[{i}]', out)
        elif a != b:
            _hit()
        return out
    if a != b:
        fa, fb = float(a), float(b)
        if math.isfinite(fa) and math.isfinite(fb):
            _hit(abs(fa - fb) / max(abs(fa), abs(fb), 1e-300))
        else:
            _hit()
    return out


def compare_published(side_dir, results_dir):
    """옆 폴더 (지금 코드 · 같은 입력 · 같은 argv) 네 JSON ↔ 게시 네 JSON → {'status', 'files': {이름: {...}}}.

    status: identical (네 파일 바이트 동일) · equal (값 같음 · 형식만 다름) · close (수치만 상대 ≤ CLOSE_REL — 반복 풀이의 합산 순서 등
    마지막 자리) · differs (값이 다르다 — 코드 세대 차이 · 게시 후 손댐) · no_published (게시 파일이 하나라도 없다)."""
    rank = {'identical': 0, 'equal': 1, 'close': 2, 'differs': 3, 'no_published': 4}
    files, worst = {}, 'identical'
    for n in NET_FOUR:
        ps_, pp = os.path.join(side_dir, n), os.path.join(results_dir, n)
        if not os.path.exists(pp) or not os.path.exists(ps_):
            st = {'status': 'no_published' if not os.path.exists(pp) else 'differs',
                  'note': '게시 파일 없음' if not os.path.exists(pp) else '다시 푼 쪽에 파일 없음'}
        elif _sha256(ps_) == _sha256(pp):
            st = {'status': 'identical'}
        else:
            a, b = _read_json(ps_), _read_json(pp)
            if a is None or b is None:
                st = {'status': 'differs', 'note': 'JSON 을 못 읽음'}
            else:
                d = _json_diff(a, b)
                status = ('equal' if d['n'] == 0 else
                          'close' if (d['other'] == 0 and d['max_rel'] <= CLOSE_REL) else 'differs')
                st = {'status': status, 'n_diff': d['n'], 'max_rel': d['max_rel'],
                      'n_non_numeric': d['other'], 'first': d['first']}
        files[n] = st
        if rank[st['status']] > rank[worst]:
            worst = st['status']
    return {'status': worst, 'files': files}


def _gzip_copy(src, dst):
    """재현 가능한 gzip (mtime 0 · 파일 이름 없음 — 같은 내용 = 같은 바이트)."""
    with open(src, 'rb') as fi, open(dst, 'wb') as fo:
        with gzip.GzipFile(filename='', mode='wb', fileobj=fo, compresslevel=6, mtime=0) as gz:
            shutil.copyfileobj(fi, gz, 1 << 20)


def make_dump(results_dir, modes=MODES, gzip_csv=True, lock_timeout=None, work_dir=None, keep_work=False,
              allow_input_mismatch=False, allow_invalid_generation=False, type_map=None, scale=None,
              python=None, log=print):
    """케이스 결과 폴더에 `network_raw_dump/` 를 만든다 → manifest (dict).  만들지 않으면 DumpRefused (게시 파일은 그대로)."""
    ps = _webapp_ps()
    rd = os.path.realpath(results_dir)
    atoms, contacts = os.path.join(rd, 'atoms.csv'), os.path.join(rd, 'contacts.csv')
    for p in (atoms, contacts):
        if not os.path.exists(p):
            raise DumpRefused(f'{os.path.basename(p)} 없음 — 망 입력이 없는 폴더 ({rd})')
    bad = [m for m in modes if m not in MODES]
    if bad or not modes:
        raise DumpRefused(f'모드 {bad or modes} — 허용 {MODES}')

    prov = ps.read_network_provenance(rd)
    if prov.get('provenance_state') == 'invalid':
        raise DumpRefused(f'망 도장 손상 ({prov.get("note")}) — 게시 세대를 확인할 수 없다')
    pargv = dict(prov.get('argv') or {})
    if pargv:
        argv_source = ps.PROVENANCE_FILE
        argv = {'type_map': pargv.get('type_map'), 'scale': pargv.get('scale'), 'contact_mode': pargv.get('contact_mode')}
        if not argv['type_map'] or argv['scale'] in (None, ''):
            raise DumpRefused(f'도장 argv 에 type_map · scale 이 없다 ({pargv}) — 웹앱이 넘긴 값을 확인할 수 없다')
        if argv['contact_mode'] != WEBAPP_CONTACT_MODE:
            raise DumpRefused(f'도장 contact_mode {argv["contact_mode"]!r} ≠ 웹앱 망 단계 {WEBAPP_CONTACT_MODE!r} — 웹앱 세대가 아니다')
        for k, v in (('type_map', type_map), ('scale', scale)):
            if v is not None and str(v) != str(argv[k]):
                raise DumpRefused(f'--{k.replace("_", "-")} {v!r} ≠ 도장 {argv[k]!r} — 게시된 풀이와 다른 argv 로는 만들지 않는다')
    else:
        if not type_map or scale in (None, ''):
            raise DumpRefused('망 도장 (network_provenance.json) 에 argv 가 없다 — 웹앱이 넘긴 type_map · scale 을 짐작하지 않는다.  '
                              '그 케이스 meta.json 의 type_map · scale 을 --type-map · --scale 로 넘길 것')
        argv_source = 'cli'
        argv = {'type_map': str(type_map), 'scale': str(scale), 'contact_mode': WEBAPP_CONTACT_MODE}
        log('  ⚠ 도장 argv 없음 — 명시 인자로 푼다 (게시 세대 대조는 아래 JSON 대조로만)')

    want_dig = dict(prov.get('input_digests') or {})
    py = python or sys.executable
    t0 = time.time()
    log('  망 lock 잡는 중 (웹앱 망 풀이가 돌고 있으면 끝날 때까지 기다린다)…')
    try:
        lock_cm = ps.network_lock(timeout=lock_timeout)
        lock_cm.__enter__()
    except ps.LockUnavailable as e:
        raise DumpRefused(f'망 lock 미획득 — 웹앱 망 풀이가 도는 중일 수 있다 ({e})') from e
    side = None
    try:
        for n in os.listdir(rd):                                # 이 도구가 남긴 옛 임시 (lock 안 = 다른 실행 없음)
            if n.startswith((_PARTIAL_PREFIX, _OLD_PREFIX)):
                shutil.rmtree(os.path.join(rd, n), ignore_errors=True)
        prob = ps.network_generation_problem(rd)
        if prob and not allow_invalid_generation:
            raise DumpRefused(f'활성 망 세대가 확정되지 않았다 ({prob}) — 웹앱 망 단계를 다시 돌린 뒤 만들 것')
        dig0 = {n: ps.file_digest(os.path.join(rd, n)) for n in ('atoms.csv', 'contacts.csv')}
        mism = {n: (want_dig.get(n), dig0[n]) for n in dig0 if n in want_dig and want_dig[n] != dig0[n]}
        if mism and not allow_input_mismatch:
            raise DumpRefused(f'입력 해시 ≠ 도장 {mism} — 게시 뒤 입력이 바뀌었다 (다른 침대의 전류가 된다).  웹앱 망 단계를 다시 돌릴 것')
        if not want_dig:
            log('  ⚠ 도장에 입력 해시가 없다 — 입력 대조 없이 푼다')
        side = tempfile.mkdtemp(prefix='netcur_side_', dir=work_dir)
        for n in ('mesh_info.json', 'input_params.json'):
            if os.path.exists(os.path.join(rd, n)):
                shutil.copy2(os.path.join(rd, n), os.path.join(side, n))
        raw = os.path.join(side, 'raw')
        cmd = [py, NC_SCRIPT, atoms, contacts, '-o', side, '-t', str(argv['type_map']), '-s', str(argv['scale']),
               '--contact-mode', WEBAPP_CONTACT_MODE, '--dump-raw-dir', raw]
        log('  실행: ' + shlex.join(cmd))
        with open(os.path.join(side, 'solver.log'), 'w', encoding='utf-8') as lf:
            rc = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT).returncode
        if rc != 0:
            with open(os.path.join(side, 'solver.log'), encoding='utf-8', errors='replace') as lf:
                tail = lf.read()[-1500:]
            raise DumpRefused(f'network_conductivity.py rc {rc} — 덤프 없음.  로그 끝:\n{tail}')
        dig1 = {n: ps.file_digest(os.path.join(rd, n)) for n in ('atoms.csv', 'contacts.csv')}
        if dig1 != dig0:
            raise DumpRefused(f'풀이 도중 입력이 바뀌었다 ({dig0} → {dig1}) — 덤프 없음')
        pub = compare_published(side, rd)
        part = tempfile.mkdtemp(prefix=_PARTIAL_PREFIX, dir=rd)
        files, present = {}, {}
        for m in modes:
            for ch in CHANNELS:
                t = tag(m, ch)
                srcs = [os.path.join(raw, f'{k}_{t}.csv') for k in ('edges', 'nodes')] + [os.path.join(raw, f'solution_{t}.json')]
                present[t] = all(os.path.exists(s) for s in srcs)
                if not present[t]:
                    continue                                    # 그 채널 관통 해 없음 (예: AM 망 미퍼콜) — 생산자가 덤프를 안 썼다
                for s in srcs:
                    nm = os.path.basename(s) + ('.gz' if (gzip_csv and s.endswith('.csv')) else '')
                    dst = os.path.join(part, nm)
                    (_gzip_copy if nm.endswith('.gz') else shutil.copy2)(s, dst)
                    files[nm] = {'bytes': os.path.getsize(dst), 'sha256': _sha256(dst)}
        manifest = {
            'schema': SCHEMA,
            'created_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'code_sha': ps.code_sha(),
            'solver': 'network_conductivity.py',
            'argv': argv, 'argv_source': argv_source,
            'cmd': cmd,
            'network_run_id': prov.get('network_run_id'),
            'provenance_code_sha': prov.get('code_sha'),
            'provenance_solver_status': prov.get('solver_status'),
            'input_digests': dig0, 'input_digests_provenance': want_dig,
            'input_mismatch_allowed': bool(mism),
            'generation_problem': prob or '',
            'published_match': pub,
            'modes': list(modes), 'channels': list(CHANNELS), 'present': present,
            'gzip': bool(gzip_csv),
            'files': files,
            'solve_wall_s': round(time.time() - t0, 1),
            'note': ('같은 CLI 를 옆 폴더 (-o) 로 + --dump-raw-dir — 게시 파일 무변경.  간선 전류 = 1 V 프로브 FULL 해 (바닥 띠 1 V · 위 띠 0 V · '
                     '정확 Dirichlet) · 모델의 접촉망 풀이 (측정 전류 아님)'),
        }
        with open(os.path.join(part, MANIFEST), 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        os.chmod(part, 0o755)                                   # mkdtemp 는 0700 — 케이스 폴더의 다른 산출물과 같은 권한으로
        final, old = dump_dir(rd), None
        if os.path.exists(final):
            old = os.path.join(rd, _OLD_PREFIX + uuid.uuid4().hex[:8])
            os.rename(final, old)
        os.rename(part, final)
        if old:
            shutil.rmtree(old, ignore_errors=True)
        return manifest
    finally:
        lock_cm.__exit__(None, None, None)
        if side and not keep_work:
            shutil.rmtree(side, ignore_errors=True)
        elif side:
            log(f'  옆 폴더 보존: {side}')


# ═══════════════════════════════ 뷰어 자료 (경로) ═══════════════════════════════

def _err(status, error, message, **kw):
    body = {'ok': False, 'error': error, 'message': message}
    body.update(kw)
    return status, body


def _box(results_dir):
    ip = _read_json(os.path.join(results_dir, 'input_params.json')) or {}
    try:
        return float(ip.get('box_x', 0.05)), float(ip.get('box_y', 0.05))
    except (TypeError, ValueError):
        return 0.05, 0.05


def _generation(results_dir, man):
    prov = _read_json(os.path.join(results_dir, 'network_provenance.json')) or {}
    try:
        import tau_flux as _tf
        prob = _tf.network_generation_problem(results_dir)
    except Exception as e:                                     # noqa: BLE001 — 확인 불가는 표지로 (조용히 유효라 하지 않는다)
        prob = f'세대 검사 도우미를 못 불렀다 ({type(e).__name__}) — 활성 세대 미확인'
    out = {'active_network_run_id': prov.get('network_run_id'), 'problem': prob or ''}
    if man is None:
        out.update(dump_network_run_id=None, match=None, note='manifest 없음 (CLI 원 덤프) — 덤프 세대 미확인')
    elif man.get('network_run_id') is None:
        out.update(dump_network_run_id=None, match=None,
                   note='도장 없는 케이스로 만든 덤프 (argv = 명시 인자) — 덤프 세대 미확인 · 게시 σ 대조로만 확인')
    else:
        out.update(dump_network_run_id=man.get('network_run_id'),
                   match=bool(man.get('network_run_id') == prov.get('network_run_id') and not prob))
    return out


def _sigma_check(results_dir, mode, channel, sol):
    p = os.path.join(results_dir, PUBLISHED_FILE[mode])
    if mode == 'hertzian' and not os.path.exists(p):
        p = os.path.join(results_dir, 'network_conductivity.json')     # 옛 legacy 이름 (= Hertz 결과)
    pub = _read_json(p)
    try:
        dv = round(float(sol.get('sigma_ratio')), 8)
    except (TypeError, ValueError):
        dv = None
    pv = (pub or {}).get(SIGMA_KEY[channel])
    if pub is None or pv is None:
        return {'match': None, 'published': pv, 'dump': dv, 'source': f'{os.path.basename(p)}:{SIGMA_KEY[channel]}',
                'note': '게시 σ 없음 — 대조 불가'}
    return {'match': bool(dv is not None and dv == pv), 'published': pv, 'dump': dv,
            'source': f'{os.path.basename(p)}:{SIGMA_KEY[channel]}'}


def _pos_finite(v):
    """유한 양수 → float · 그 밖 (None · bool · 문자열 · 0 · 음수 · NaN · inf) → None."""
    if isinstance(v, bool):
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if (math.isfinite(x) and x > 0) else None


def _published_mode(results_dir, mode):
    p = os.path.join(results_dir, PUBLISHED_FILE[mode])
    if mode == 'hertzian' and not os.path.exists(p):
        p = os.path.join(results_dir, 'network_conductivity.json')     # 옛 legacy 이름 (= Hertz 결과)
    return os.path.basename(p), _read_json(p)


def _sigma0(results_dir, mode, channel):
    """그 채널 · 모드 풀이의 σ₀ (S/cm) — (값, 출처) · 못 찾으면 (None, 사유).  짐작하지 않는다 (상수 기본값으로 떨어지지 않는다).

    사다리: ① 게시 증서 `<채널>solve_certificate_full.sigma_bulk_S_cm` (G2RR-02 결합 — 채널 · 모드가 맞을 때만) →
    ② 이온만 `sigma_grain_S_cm` (게시 파일 최상위) → ③ 게시 `<채널>sigma_full_mScm ÷ (σ/σ₀ × 1000)` (둘 다 반올림 저장 — 상대 ~1e-6 한계)."""
    fname, pub = _published_mode(results_dir, mode)
    if pub is None:
        return None, (f'게시 파일 {PUBLISHED_FILE[mode]}' + (' · network_conductivity.json' if mode == 'hertzian' else '')
                      + ' 없음 — σ₀ 미확인 (전류 밀도 계산 불가)')
    pre = CHANNEL_PREFIX[channel]
    cert = pub.get(pre + 'solve_certificate_full')
    if isinstance(cert, dict):
        s = _pos_finite(cert.get('sigma_bulk_S_cm'))
        ch_ok = cert.get('channel') in (None, channel)
        md_ok = cert.get('contact_mode') in (None, mode)
        if s is not None and ch_ok and md_ok:
            return s, f'{fname}:{pre}solve_certificate_full.sigma_bulk_S_cm'
    if channel == 'ionic':
        s = _pos_finite(pub.get('sigma_grain_S_cm'))
        if s is not None:
            return s, f'{fname}:sigma_grain_S_cm'
    ms, q = _pos_finite(pub.get(pre + 'sigma_full_mScm')), _pos_finite(pub.get(SIGMA_KEY[channel]))
    if ms is not None and q is not None:
        return ms / (q * 1000.0), (f'{fname}:{pre}sigma_full_mScm ÷ ({SIGMA_KEY[channel]} × 1000) — 두 열 모두 반올림 저장 '
                                   '(반올림 한계 상대 ~1e-6)')
    return None, f'{fname} 에 σ₀ (증서 · sigma_grain_S_cm · mS/cm 열) 가 없다 — σ₀ 미확인 (전류 밀도 계산 불가)'


def _box_area_um2(results_dir, mode, channel):
    """그 풀이의 상자 단면 (µm²) — (값, 출처).  ① 게시 증서 geometry (풀이가 σ 환산에 쓴 기하) → ② input_params.json box × scale (도장 argv)."""
    fname, pub = _published_mode(results_dir, mode)
    cert = (pub or {}).get(CHANNEL_PREFIX[channel] + 'solve_certificate_full')
    if isinstance(cert, dict) and isinstance(cert.get('geometry'), dict):
        g = cert['geometry']
        bx, by, sc = (_pos_finite(g.get(k)) for k in ('box_x', 'box_y', 'scale'))
        if bx and by and sc:
            return bx * by * sc * sc, f'{fname}:{CHANNEL_PREFIX[channel]}solve_certificate_full.geometry'
    ip = _read_json(os.path.join(results_dir, 'input_params.json')) or {}
    prov = _read_json(os.path.join(results_dir, 'network_provenance.json')) or {}
    bx, by = _pos_finite(ip.get('box_x')), _pos_finite(ip.get('box_y'))
    sc = _pos_finite((prov.get('argv') or {}).get('scale'))
    if bx and by and sc:
        return bx * by * sc * sc, 'input_params.json box × network_provenance argv scale'
    return None, '상자 단면 미확인 (증서 geometry · input_params box 없음)'


def c1_scaling(results_dir, j_mean_1V):
    """@1C 환산 — I_1C / I_1V = j_1C / ⟨J⟩_1V (새 C-rate 식이 아니다: j_1C = Q_areal × 1 h⁻¹ · Q_areal = 케이스 표 등급 축과 같은 함수).

    → {'status': 'ok' | 'unavailable', 'reason', 'Q_areal_mAh_cm2', 'j_1C_A_cm2', 'factor', 'defaults_used', 'source', 'rule'}.
    두께 (full_metrics thickness_um) 가 없으면 환산하지 않는다 · AM:SE 비 · 공극률이 없으면 등급 엔진이 쓰는 기본값 (wt_AM 0.80 · 고체 0.85)
    으로 낸 값을 표지한다 (케이스 표의 Q_areal 과 같은 값 — 숨기지 않는다)."""
    out = {'status': 'unavailable', 'reason': None, 'Q_areal_mAh_cm2': None, 'j_1C_A_cm2': None, 'factor': None,
           'capacity_mAh_g': None, 'defaults_used': [], 'source': C1_SOURCE, 'rule': C1_RULE}
    fm = _read_json(os.path.join(results_dir, 'full_metrics.json'))
    if fm is None:
        out['reason'] = 'full_metrics.json 없음 (접촉 분석 산출이 없다) — Q_areal 미확인'
        return out
    if _pos_finite(fm.get('thickness_um')) is None:
        out['reason'] = 'full_metrics.json 에 thickness_um 없음 — Q_areal (= 두께 × 고체 × AM 부피 몫 × ρ × C) 미확인'
        return out
    try:
        import grade_engine as _G
    except Exception as e:                                     # noqa: BLE001 — 환산만 못 한다 (사유)
        out['reason'] = f'grade_engine 을 못 불렀다 ({type(e).__name__}) — Q_areal 미확인'
        return out
    ip = _read_json(os.path.join(results_dir, 'input_params.json')) or {}
    m = dict(fm)
    m.update(_G.map_input_params(ip, None))
    has_ratio = any(isinstance(m.get(k), str) and ':' in m.get(k) for k in ('am_se_ratio', '_input_am_se_ratio'))
    try:
        eps = float(m.get('porosity'))
        has_eps = math.isfinite(eps)
    except (TypeError, ValueError):
        has_eps = False
    if not has_ratio:
        out['defaults_used'].append('am_se_ratio 없음 → 등급 엔진 기본 wt_AM 0.80')
    if not has_eps:
        out['defaults_used'].append('porosity 없음 → 등급 엔진 기본 고체 0.85')
    q = _pos_finite(_G._derived_value('__Q_areal_mAhcm2', m))
    if q is None:
        out['reason'] = 'Q_areal 을 낼 수 없다 (등급 엔진 값 없음)'
        return out
    out['Q_areal_mAh_cm2'] = q
    out['j_1C_A_cm2'] = q * 1e-3
    # ★ 10-08 (1저자 Q3 · 랩 표준 200 mAh/g) — 이 Q_areal 의 비용량 기준 (등급 엔진 C_AM_MAHG).  Q_areal ∝ C_AM 이라 뷰어가 고른 비용량으로
    #   Q_areal · 배율을 선형 환산한다 (webapp/app.py = 194 봉인 — 비용량을 경로 인자로 받지 않는다).
    out['capacity_mAh_g'] = getattr(_G, 'C_AM_MAHG', None)
    if _pos_finite(j_mean_1V) is None:
        out['reason'] = '⟨J⟩_1V 미확인 (σ₀ · 상자 단면) — 배율 I_1C / I_1V 를 정할 수 없다'
        return out
    out['factor'] = out['j_1C_A_cm2'] / float(j_mean_1V)
    out['status'] = 'ok'
    return out


def parse_top(top):
    """`top` → ('count', N) · ('share', P) · ('all', None) · None (잘못된 값).
    정수 = 옛 뜻 그대로 (None · '' = 경로 기본 TOP_DEFAULT · 1 … TOP_MAX 로 자름) · 'shareP' = 전류 몫 P % (P = 1–99 정수) · 'all' = 전부."""
    if top in (None, ''):
        return ('count', TOP_DEFAULT)
    if isinstance(top, str):
        s = top.strip()
        if s == 'all':
            return ('all', None)
        if s.startswith('share'):
            d = s[5:]
            if d.isascii() and d.isdigit() and len(d) <= 2 and 1 <= int(d) <= 99:
                return ('share', int(d))
            return None
    try:
        n = int(top)
    except (TypeError, ValueError):
        return None
    return ('count', max(1, min(TOP_MAX, n)))


def current_payload(results_dir, channel='ionic', mode='hertzian', top=None, scale=1000.0):
    """경로 본문 → (HTTP 상태, dict).  덤프 없음 = 404 (만드는 명령) · 잘못된 인자 = 400.
    `top` = 정수 (옛 꼴 · 상위 N) · 'shareP' (전류 몫 P %) · 'all' — `parse_top` · 모듈 머리 10-08 고르기 절."""
    import numpy as np
    import pandas as pd
    if channel not in CHANNELS:
        return _err(400, 'bad_channel', f'채널 {channel!r} — 이 보기는 {CHANNELS} (열 채널 · 다른 망은 범위 밖)')
    if mode not in MODES:
        return _err(400, 'bad_mode', f'모드 {mode!r} — {MODES}')
    parsed = parse_top(top)
    if parsed is None:
        return _err(400, 'bad_top', f'top {top!r} — 정수 (상위 N) · shareP (전류 몫 P % · P = 1–99) · all')
    requested = None if top in (None, '') else str(top).strip()
    kind, kval = parsed
    compact = kind in ('share', 'all')                            # 이름 고르기 = 압축 꼴 (단면이 없어 경로 기본으로 그려도 꼴은 요청대로)
    top = kval if kind == 'count' else None
    try:
        scale = float(scale)
    except (TypeError, ValueError):
        scale = 1000.0
    rd = os.path.realpath(results_dir)
    dd = dump_dir(rd)
    if not os.path.isdir(dd):
        return _err(404, 'no_dump',
                    '이 케이스에는 망 해의 간선별 전류가 저장돼 있지 않다 (웹앱 망 단계는 --dump-raw-dir 를 넘기지 않는다).  '
                    '아래 명령을 리포 위치에서 한 번 실행하면 같은 풀이의 전류가 이 케이스 폴더 network_raw_dump/ 에 남는다 '
                    '(게시 값 무변경 · real14 기준 약 1 분).',
                    how_to=how_to(rd), results_dir=rd)
    t = tag(mode, channel)
    ef, nf, sf = _find(dd, f'edges_{t}'), _find(dd, f'nodes_{t}'), os.path.join(dd, f'solution_{t}.json')
    sol = _read_json(sf)
    man = _read_json(os.path.join(dd, MANIFEST))
    if not ef or not nf or sol is None:
        why = ('덤프에 이 채널 · 모드가 없다 — 그 망이 관통하지 않았거나 (예: AM 망 미퍼콜) 덤프를 그 모드 없이 만들었다'
               + (f' (manifest present: {man.get("present")})' if man else ''))
        return _err(404, 'no_channel', why, how_to=how_to(rd), results_dir=rd)
    try:
        I_tot = float(sol.get('G_eff'))
    except (TypeError, ValueError):
        I_tot = float('nan')
    if not (math.isfinite(I_tot) and I_tot > 0):
        return _err(422, 'bad_solution', f'해의 G = {sol.get("G_eff")!r} — 전류 몫을 정의할 수 없다')

    e = pd.read_csv(ef, usecols=lambda c: c in ('id1', 'id2', 'V1', 'V2', 'I', 'R_total', 'A_used'))
    nd = pd.read_csv(nf, usecols=['id', 'x', 'y', 'z', 'radius', 'V'])
    nidx = pd.Index(nd['id'].to_numpy(dtype=np.int64))
    i1 = nidx.get_indexer(e['id1'].to_numpy(dtype=np.int64))
    i2 = nidx.get_indexer(e['id2'].to_numpy(dtype=np.int64))
    keep = (i1 >= 0) & (i2 >= 0)
    n_missing = int((~keep).sum())
    n_perc = int(len(e))
    id1 = e['id1'].to_numpy(dtype=np.int64)[keep]
    id2 = e['id2'].to_numpy(dtype=np.int64)[keep]
    V1, V2 = e['V1'].to_numpy(float)[keep], e['V2'].to_numpy(float)[keep]
    I = e['I'].to_numpy(float)[keep]
    R = e['R_total'].to_numpy(float)[keep]
    AC = e['A_used'].to_numpy(float)[keep] if 'A_used' in e.columns else None     # 그 풀이의 접촉 면적 (µm²)
    i1, i2 = i1[keep], i2[keep]
    X, Y, Z, RAD, VN = (nd[c].to_numpy(float) for c in ('x', 'y', 'z', 'radius', 'V'))
    aI = np.abs(I)
    P = I * I * R
    power_tot = float(P.sum())
    power_identity_rel = abs(power_tot - I_tot) / I_tot

    # z-단면 — 두 띠 (전류가 0 이 아닌 띠 노드) 사이 평면.  S_k = {z ≤ Z_k} 의 단면 전류 = I_전체 (띠 노드가 모두 한쪽).
    inc = np.bincount(i1, weights=aI, minlength=len(nd)) + np.bincount(i2, weights=aI, minlength=len(nd))
    act = inc > ZERO_REL * I_tot
    bot, topb = act & (VN == 1.0), act & (VN == 0.0)
    z1, z2 = Z[i1], Z[i2]
    zcut = None
    flux = None
    if bot.any() and topb.any():
        z_lo, z_hi = float(Z[bot].max()), float(Z[topb].min())
        if z_hi > z_lo:
            planes = z_lo + (np.arange(ZCUT_PLANES) + 0.5) * (z_hi - z_lo) / ZCUT_PLANES
            up = (z1[:, None] <= planes) & (z2[:, None] > planes)
            dn = (z2[:, None] <= planes) & (z1[:, None] > planes)
            flux = np.where(up, I[:, None], 0.0) - np.where(dn, I[:, None], 0.0)
            tot = flux.sum(axis=0) / I_tot
            zcut = {'planes': ZCUT_PLANES, 'z_lo_um': round(z_lo * scale, 6), 'z_hi_um': round(z_hi * scale, 6),
                    'identity_max_dev': float(np.abs(tot - 1.0).max())}

    bx, by = _box(rd)
    wrap = (np.abs(X[i1] - X[i2]) > bx / 2.0) | (np.abs(Y[i1] - Y[i2]) > by / 2.0)
    nz = aI > ZERO_REL * I_tot
    n_zero = int((~nz).sum())
    order = np.lexsort((id2, id1, -aI))                          # |I| 내림차순 · 동률 = (id1, id2)
    order = order[nz[order]]
    n_nz = int(len(order))
    # ★ 10-08 전류 몫 사다리 — 상위 k 접촉의 단면 몫 (32 단면 평균 · 아래 zcut.share_mean 과 같은 잣대) = Σ_{i<k} (간선 i 의 단면 평균 순 흐름) / I_전체.
    #   단면 평균은 간선마다 미리 평균해도 같다 (선형) — n × 32 사본 없이 n 길이 누적 하나.  단면이 없는 해 (띠 없음 · 겹침) = None.
    ladder = (np.cumsum(flux.mean(axis=1)[order]) / I_tot) if (flux is not None and n_nz) else None

    def _n_share(p):
        if ladder is None:
            return None
        hit = np.flatnonzero(ladder >= p / 100.0)
        return int(hit[0]) + 1 if hit.size else n_nz          # 끝까지 못 닿으면 (수치 잔차) 전부
    fallback = None
    if kind == 'share':
        top = _n_share(kval)
        if top is None:
            fallback = (f'전류 몫 잣대 (높이 단면) 를 정할 수 없는 해 — 전류가 흐르는 전극 띠 노드가 없거나 두 띠가 겹친다 · '
                        f'경로 기본 (상위 {TOP_DEFAULT}) 으로 그림')
            kind, kval, top = 'count', TOP_DEFAULT, TOP_DEFAULT
    elif kind == 'all':
        top = n_nz
    sel = order[:top]
    seld = sel[~wrap[sel]]
    selection = {'kind': kind, 'requested': requested, 'share_pct': kval if kind == 'share' else None, 'n': int(len(sel)),
                 'n_nonzero': n_nz, 'share_n': ({str(p): _n_share(p) for p in SHARE_CHOICES} if ladder is not None else None),
                 'fallback': fallback, 'packing': PACKING_COMPACT if compact else 'edges'}
    if zcut is not None:
        sh = flux[sel].sum(axis=0) / I_tot
        shd = flux[seld].sum(axis=0) / I_tot
        zcut.update(share_mean=float(sh.mean()), share_min=float(sh.min()), share_max=float(sh.max()),
                    drawn_share_mean=float(shd.mean()), drawn_share_min=float(shd.min()))

    # ★ 10-07 (#17) 접촉 전류 밀도 — j = |I| σ₀ 1e4 / A_c (A cm⁻² · @1V) · ⟨J⟩_1V = I_전체 σ₀ 1e4 / A_상자 · @1C 배율 (c1_scaling)
    sigma0, s0_src = _sigma0(rd, mode, channel)
    a_box, box_src = _box_area_um2(rd, mode, channel)
    j_reason = None
    if AC is None:
        j_reason = '덤프 edges 표에 A_used (접촉 면적) 열이 없다 — 전류 밀도 계산 불가 (덤프를 지금 코드로 다시 만들 것)'
    elif sigma0 is None:
        j_reason = s0_src
    j_mean = (I_tot * sigma0 * J_PER_NORM / a_box) if (sigma0 is not None and a_box) else None

    def _jc(k):
        if j_reason is not None:
            return None, (None if AC is None else (float(AC[k]) if math.isfinite(AC[k]) else None))
        a = float(AC[k])
        if not (math.isfinite(a) and a > 0):
            return None, (a if math.isfinite(a) else None)
        return float(aI[k] * sigma0 * J_PER_NORM / a), a

    def _p(k):
        return [round(float(X[k]) * scale, 6), round(float(Y[k]) * scale, 6), round(float(Z[k]) * scale, 6)]
    edges = nodes_c = edges_c = None
    if not compact:                                              # 옛 꼴 — 접촉마다 dict (정수 고르기 · 옛 키 값 그대로)
        edges = []
        for k in sel:
            fwd = V1[k] >= V2[k]                                 # a = 높은 전위 끝 (전류 a → b)
            ka, kb = (i1[k], i2[k]) if fwd else (i2[k], i1[k])
            jk, ak = _jc(k)
            edges.append({'a': _p(ka), 'b': _p(kb), 'ra': round(float(RAD[ka]) * scale, 6), 'rb': round(float(RAD[kb]) * scale, 6),
                          'ia': int(id1[k] if fwd else id2[k]), 'ib': int(id2[k] if fwd else id1[k]),
                          's': float(aI[k] / I_tot), 'va': float(V1[k] if fwd else V2[k]), 'vb': float(V2[k] if fwd else V1[k]),
                          'w': int(bool(wrap[k])), 'j': jk, 'ac': ak})
        jv = [x['j'] for x in edges]
    else:                                                        # 압축 꼴 — 입자 표 한 번 + 접촉 = 입자 번호 둘 + j (옛 꼴과 같은 식 · 같은 반올림)
        fw = V1[sel] >= V2[sel]
        ka_, kb_ = np.where(fw, i1[sel], i2[sel]), np.where(fw, i2[sel], i1[sel])
        uniq, inv = np.unique(np.concatenate([ka_, kb_]), return_inverse=True)
        inv = np.asarray(inv).reshape(-1)
        m = len(sel)
        nid = nd['id'].to_numpy(dtype=np.int64)
        nodes_c = {'id': [int(v) for v in nid[uniq]],
                   'x': [round(float(X[k]) * scale, 6) for k in uniq], 'y': [round(float(Y[k]) * scale, 6) for k in uniq],
                   'z': [round(float(Z[k]) * scale, 6) for k in uniq], 'r': [round(float(RAD[k]) * scale, 6) for k in uniq]}
        if j_reason is not None:
            jv = [None] * m
        else:
            a_ = AC[sel]
            ok_a = np.isfinite(a_) & (a_ > 0)
            with np.errstate(divide='ignore', invalid='ignore'):
                jarr = aI[sel] * sigma0 * J_PER_NORM / a_                # _jc 와 같은 연산 순서 (같은 비트)
            jv = [float(v) if o else None for v, o in zip(jarr, ok_a)]
        edges_c = {'a': inv[:m].tolist(), 'b': inv[m:].tolist(), 'j': jv}
    jj = [x for x in jv if x is not None and x > 0]
    density = {
        'unit': J_UNIT, 'rule': J_RULE, 'probe': '1 V (바닥 띠 1 V → 위 띠 0 V · 정확 Dirichlet)',
        'area_column': 'A_used' if AC is not None else None,
        'sigma0_S_cm': sigma0, 'sigma0_source': s0_src if sigma0 is not None else None,
        'box_area_um2': a_box, 'box_source': box_src,
        'j_mean_1V': j_mean,
        'j_min_1V': min(jj) if jj else None, 'j_max_1V': max(jj) if jj else None,
        'n_no_area': int(sum(1 for x in jv if x is None)) if j_reason is None else 0,
        'reason': j_reason,
        'c1': c1_scaling(rd, j_mean),
    }
    body = {
        'ok': True, 'channel': channel, 'mode': mode, 'top': top, 'selection': selection, 'scale': scale,
        'n_perc_edges': n_perc, 'n_perc_nodes': int(len(nd)), 'n_returned': int(len(sel)), 'n_zero_current': n_zero,
        'n_missing_position': n_missing, 'n_wrap_returned': int(wrap[sel].sum()),
        'I_total': I_tot, 'I_total_source': f'solution_{t}.json:G_eff (ΔV = 1)',
        'share_max': float(aI[sel].max() / I_tot) if len(sel) else None,
        'share_min': float(aI[sel].min() / I_tot) if len(sel) else None,
        'zcut': zcut,
        'power_share': float(P[sel].sum() / power_tot) if power_tot > 0 else None,
        'power_identity_rel': float(power_identity_rel),
        'sum_abs_share': float(aI[sel].sum() / aI.sum()) if aI.sum() > 0 else None,
        'box': {'x': round(bx * scale, 6), 'y': round(by * scale, 6)},
        'sigma_check': _sigma_check(rd, mode, channel, sol),
        'generation': _generation(rd, man),
        'dump': ({'schema': man.get('schema'), 'created_at': man.get('created_at'), 'code_sha': man.get('code_sha'),
                  'published_match': (man.get('published_match') or {}).get('status'), 'argv_source': man.get('argv_source')}
                 if man else None),
        'probe': '1 V 프로브 FULL 해 — 바닥 띠 1 V · 위 띠 0 V (정확 Dirichlet) · R_total = R_bulk + R_c',
        'density': density,
    }
    if compact:
        body.update(packing=PACKING_COMPACT, nodes=nodes_c, edges_c=edges_c)
    else:
        body['edges'] = edges
    return 200, body


# ═══════════════════════════════ CLI ═══════════════════════════════

def _cmd_dump(a):
    modes = tuple(m.strip() for m in a.modes.split(',') if m.strip())
    rd = os.path.realpath(a.results_dir)
    print(f'[network_current] 덤프 — {rd}')
    try:
        man = make_dump(rd, modes=modes, gzip_csv=not a.no_gzip, lock_timeout=a.lock_timeout, work_dir=a.work_dir,
                        keep_work=a.keep_work, allow_input_mismatch=a.allow_input_mismatch,
                        allow_invalid_generation=a.allow_invalid_generation, type_map=a.type_map, scale=a.scale)
    except DumpRefused as e:
        print(f'  ✗ 덤프 안 함: {e}', file=sys.stderr)
        return 2
    size = sum(f['bytes'] for f in man['files'].values())
    pm = man['published_match']['status']
    print(f'  ✓ {dump_dir(rd)}  ({len(man["files"])} 파일 · {size / 1e6:.1f} MB · 풀이 {man["solve_wall_s"]} s)')
    print(f'  게시 JSON 대조: {pm}' + ('' if pm in ('identical', 'equal', 'close') else
                                    '  ⚠ 게시 값과 다른 해 — 코드 세대가 다르다.  웹앱에서 이 케이스 망 단계를 다시 돌린 뒤 이 명령을 다시 (뷰어도 경고한다)'))
    absent = [t for t, ok in man['present'].items() if not ok]
    if absent:
        print(f'  관통 해가 없어 빠진 채널 · 모드: {absent}')
    print("  웹앱: DEM 3D → View Mode '⚡ 전류 흐름 (접촉 전류 밀도 A cm⁻² · 상위 접촉)'")
    return 0


def _cmd_show(a):
    st, body = current_payload(a.results_dir, channel=a.channel, mode=a.mode, top=a.top, scale=a.scale)
    if st != 200:
        print(json.dumps(body, ensure_ascii=False, indent=2))
        return 1
    z = body.get('zcut') or {}
    sl = body.get('selection') or {}
    print(f"{body['channel']} · {body['mode']} · 관통 간선 {body['n_perc_edges']} · 돌려준 {body['n_returned']} "
          f"(0 전류 {body['n_zero_current']} · 주기 경계 {body['n_wrap_returned']})")
    if sl.get('kind') == 'share':
        print(f"고르기: 전류 {sl['share_pct']} % → 상위 {sl['n']} 접촉 (0 아닌 전류 접촉 {sl['n_nonzero']} · 꼴 {sl['packing']})")
    elif sl.get('kind') == 'all':
        print(f"고르기: 전부 {sl['n']} 접촉 (꼴 {sl['packing']})")
    else:
        print(f"고르기: 상위 {body['top']}" + (f"  ⚠ {sl['fallback']}" if sl.get('fallback') else ''))
    if sl.get('share_n'):
        print('전류 몫 → 접촉 수: ' + ' · '.join(f'{p} % = {n}' for p, n in sl['share_n'].items()))
    print(f"I_전체 {body['I_total']:.6g} · 단면 몫 평균 {z.get('share_mean')} (최소 {z.get('share_min')} · 최대 {z.get('share_max')}) · "
          f"보존 편차 {z.get('identity_max_dev')} · 소산 몫 {body['power_share']} · Tellegen {body['power_identity_rel']:.2e}")
    print(f"게시 σ 대조 {body['sigma_check']} · 세대 {body['generation']}")
    dn = body.get('density') or {}
    c1 = dn.get('c1') or {}

    def _g(v, f=1.0):
        return f'{float(v) * f:.4g}' if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v)) else '—'
    if dn.get('reason'):
        print(f"전류 밀도: 계산 불가 — {dn['reason']}")
    else:
        print(f"전류 밀도 (A cm⁻² @1V · A_c = {dn.get('area_column')}) — 그린 접촉 {_g(dn.get('j_min_1V'))} … {_g(dn.get('j_max_1V'))} · "
              f"단면 평균 ⟨J⟩ {_g(dn.get('j_mean_1V'))} · σ₀ {dn.get('sigma0_S_cm')} S/cm ({dn.get('sigma0_source')})"
              + (f" · 면적 없는 접촉 {dn['n_no_area']}" if dn.get('n_no_area') else ''))
        if c1.get('status') == 'ok':
            f = float(c1['factor'])
            print(f"@1C (× {f:.4g} = I_1C / I_1V · Q_areal {_g(c1.get('Q_areal_mAh_cm2'))} mAh/cm²) — "
                  f"{_g(dn.get('j_min_1V'), f)} … {_g(dn.get('j_max_1V'), f)} A cm⁻²"
                  + (f" · ⚠ 기본값 {c1['defaults_used']}" if c1.get('defaults_used') else ''))
        else:
            print(f"@1C 환산 불가 — {c1.get('reason')}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='망 해의 간선별 전류 — 덤프 한 번 (dump) · 뷰어 자료 요약 (show)')
    sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('dump', help='케이스 결과 폴더에 network_raw_dump/ 를 만든다 (웹앱과 같은 풀이 · 옆 폴더 · 게시 파일 무변경)')
    d.add_argument('results_dir', help='케이스 결과 폴더 (atoms.csv · contacts.csv · network_provenance.json 이 있는 곳)')
    d.add_argument('--modes', default=','.join(MODES), help='남길 접촉 면적 모드 (쉼표) — hertzian · physics')
    d.add_argument('--no-gzip', action='store_true', help='edges · nodes 표를 압축하지 않는다')
    d.add_argument('--lock-timeout', type=float, default=None, help='망 lock 대기 초 (기본 = 끝까지 기다림)')
    d.add_argument('--work-dir', default=None, help='옆 폴더를 만들 곳 (기본 = 시스템 임시)')
    d.add_argument('--keep-work', action='store_true', help='옆 폴더 (다시 푼 네 JSON · solver.log) 를 지우지 않는다')
    d.add_argument('--allow-input-mismatch', action='store_true', help='입력 해시가 도장과 달라도 푼다 (manifest 에 기록 · 권하지 않음)')
    d.add_argument('--allow-invalid-generation', action='store_true', help='활성 망 세대가 확정되지 않아도 푼다 (권하지 않음)')
    d.add_argument('--type-map', default=None, help='도장에 argv 가 없을 때만 — 그 케이스 meta.json 의 type_map')
    d.add_argument('--scale', default=None, help='도장에 argv 가 없을 때만 — 그 케이스 meta.json 의 scale')
    s = sub.add_parser('show', help='경로 /network-current 가 낼 요약 (브라우저 없이 확인)')
    s.add_argument('results_dir')
    s.add_argument('--channel', default='ionic', choices=CHANNELS)
    s.add_argument('--mode', default='hertzian', choices=MODES)
    s.add_argument('--top', default=str(TOP_DEFAULT),
                   help='정수 N (상위 N 접촉) · shareP (전류 몫 P 퍼센트 · P = 1–99 · 예 share80) · all (전부)')
    s.add_argument('--scale', type=float, default=1000.0, help='표시 좌표 배율 (meta.json scale)')
    a = ap.parse_args(argv)
    return _cmd_dump(a) if a.cmd == 'dump' else _cmd_show(a)


if __name__ == '__main__':
    sys.exit(main())
