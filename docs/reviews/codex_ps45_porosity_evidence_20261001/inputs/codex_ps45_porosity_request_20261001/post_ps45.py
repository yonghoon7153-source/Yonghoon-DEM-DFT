#!/usr/bin/env python3
"""ps45 5 침대 → LHS 배포 v1.1 과 **같은 생성기 · 같은 관문 · 같은 배포 열** (로컬 후처리 · 읽기 전용 · 리포를 고치지 않는다).

    python3 post_ps45.py --tar ~/ps45_lhs_<D>.tar.gz --sha256 <WSL 이 찍은 값> --out <dir>     # 본번
    python3 post_ps45.py --dir <풀린 산출 폴더> --out <dir>                                       # 이미 풀었으면
    python3 post_ps45.py --replay lhs130 --out <dir>                                               # 건조 시험 (커밋된 v1.1 원천)
    python3 post_ps45.py --replay lhsx64 --out <dir>
    python3 post_ps45.py --selftest                                                                # 둘 다 + tar 안전 시험

무엇을 하나 (본번)
  ① 코드 고정 — 배포 v1.1 커밋 `c981d77f0` 의 생성기 · 배포 빌더 · census · v1.1 열 사전을 `git archive` 로 꺼낸다 (작업 트리 · HEAD 를 쓰지 않는다 ·
     다른 작업자가 v1.1 폴더를 고치고 있어도 GO 받은 그 바이트를 쓴다).
  ② 입력 대조 (fail-closed · rc 2) — tar sha256 · RUN_MANIFEST (워크트리 커밋 = 1e09f661d 수확 · d1ec42fba 웹앱/union/감사) ·
     수확 배치 sha_verified · 웹앱 배치 stop_after=contact · 실행 커밋 · 수확 JSON 세대 (키 집합 · 규약 문자열 = v1.1 수확 JSON 과 같아야).
  ③ 인계표 = v1.1 과 **같은 CLI · 같은 인자** (`lhs_design_dataset.py --export-handover … --union … --webapp … --webapp-groups contact,percolation`).
     생성기가 거부하면 (FillRefusal) 행마다 따로 불러 **모든** 거부 사유를 모은다 — 표를 만들지 않는다 (rc 1).
  ④ 배포 = `lhs_release_build.py --columns-from <v1.1 열 사전>` → 머리 = v1.1 배포 머리와 **열 이름 · 순서 그대로**인지 · 열 사전 행이 같은지.
  ⑤ 행 관문 — 웹앱 상태 done · 퍼콜 감사 CLEAN · 수확 상태 · 벽 τ 상태 · 단계 rc · 같은 프레임 대조 (r45 union 요약 · ps45 킷 · §5-B 표) —
     실패해도 **행을 지우지 않는다** (표 · 요약에 그대로 두고 표지 · rc 3).
  ⑥ `ps45_release_5rows.csv` (+ `_columns.tsv`) · `ps45_summary.json` (덱용 값 · 한정어 · 편차 · 관문).

건조 시험 (`--replay`) — 같은 ①③④ 를 커밋된 v1.1 원천 (수확 1e09f661d · 웹앱 d1ec42fba · union 09-27 · 설계) 의 일부 행으로 돌리고,
  나온 배포 행이 커밋된 v1.1 배포 CSV 의 그 행과 **바이트 동일**한지 · 열 사전 파일이 **바이트 동일**한지 본다 (인자 배선 시험).
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEF_REPO = '/home/user/Yonghoon-DEM-DFT'
PIN = 'c981d77f005dc0c2eea495e4be1e5d61ea481bca'          # 배포 v1.1 커밋 — 생성기 · 배포 빌더 · v1.1 열 사전
SHA_H = '1e09f661d83edd674a1686b22552f609b61a34b6'        # 수확 (5번 봉인 · v1.1 수확 원천 `lhs_descriptors_cov_1e09f661d`)
SHA_W = 'd1ec42fbad2a5995059577c77031d8573a3ce3cd'        # 웹앱 접촉 단계 (v1.1 원천 `lhs_webapp_contact_d1ec42fba`) · union · 퍼콜 감사
GEN = 'scripts/lhs_design_dataset.py'
REL = 'scripts/lhs_release_build.py'
CENSUS = 'docs/data/case_master_column_census_20260919.tsv'
V11 = 'docs/data/lhs_release_20261001_v11'
V11_COLS = {'lhs130': f'{V11}/lhs_release_20261001_v11_columns.tsv', 'lhsx64': f'{V11}/lhsx_release_20261001_v11_columns.tsv'}
V11_CSV = {'lhs130': f'{V11}/lhs_release_20261001_v11.csv', 'lhsx64': f'{V11}/lhsx_release_20261001_v11.csv'}
#: v1.1 원천 (README §8) — 건조 시험 · 수확 JSON 세대 대조에 쓴다
REPLAY = {
    'lhs130': dict(design='docs/data/lhs_design_20260818.csv', harvest='docs/data/lhs_descriptors_cov_1e09f661d',
                   union='docs/data/lhs_union_20260927/lhs130_union.tsv', webapp='docs/data/lhs_webapp_contact_d1ec42fba',
                   cases=('lhs00_000', 'lhs00_018', 'lhs00_100', 'lhs00_115', 'lhs00_118')),
    'lhsx64': dict(design='docs/data/lhsx_design_adapted_20260929.csv', harvest='docs/data/lhsx_descriptors_cov_1e09f661d',
                   union='docs/data/lhs_union_20260927/lhsx64_union.tsv', webapp='docs/data/lhsx_webapp_contact_d1ec42fba',
                   cases=('lhsx_001', 'lhsx_003', 'lhsx_010', 'lhsx_040')),
}
#: 덱용 요약 값 (배포 열 이름 그대로) — ps45_summary.json 의 values
SUMMARY_COLS = (
    'n_AM_P_measured', 'n_AM_S_measured', 'n_SE_measured',
    'porosity_union_exact_pct', 'thickness_wall_gap_um', 'thickness_mass_conserving_um',
    'phi_se_mass_conserving', 'phi_am_mass_conserving', 'se_of_solid_vol', 'se_rich',
    'se_se_cn', 'se_se_cn_std', 'am_se_cn_mean', 'AM_P_se_cn_mean', 'AM_S_se_cn_mean', 'am_se_cn_surface_weighted', 'am_am_cn',
    'coverage_AM_P_hertz_pct', 'coverage_AM_S_hertz_pct', 'coverage_AM_total_hertz_pct',
    'percolation_pct', 'top_reachable_pct', 'n_components',
    'tortuosity_SE_wall', 'tortuosity_SE_wall_median',
    'am_ionic_isolated_pct', 'ionic_dead_pct', 'ionic_no_se_pct', 'AM_P_ionic_active_pct', 'AM_S_ionic_active_pct',
    'am_vulnerable_pct', 'AM_P_vulnerable_pct', 'AM_S_vulnerable_pct',
    'se_largest_comp_frac', 'se_largest_comp_wall_span_frac',
)
#: 인계표 (배포 밖) 에서 함께 싣는 것 — 1σ · 상태 · 같은-프레임 대조용
EXTRA_COLS = ('porosity_union_exact_se_pct', 'porosity_sphere_pct_RECORD_ONLY', 'tortuosity_SE_wall_status', 'timestep', 'wa_status',
              'wa_failed_stages', 'phi_se_status', 'coverage_AM_P_hertz_pct_status', 'coverage_AM_S_hertz_pct_status',
              'coverage_AM_total_hertz_pct_status', 'deck_sha256', 'atom_sha256', 'contact_sha256', 'mesh_sha256', 'boundary_model_id',
              'union_pair_upper_bound_ok')
ELIG_COLS = ('physical_target_status', 'hold_reason_codes', 'boundary_state')
QUALIFIERS = {
    '공통': 'DEM 모델 값 (강체 구 · 연화 탄성 E_SE 1.35 GPa) — 고정 finite-box DEM 규약의 수치적 구조량 · 실험값이 아니다 · 입자 모양 변형 (소성) 없음 · '
            '조성마다 침대 1 개 (시드 산포 미측정)',
    'codex_scope': 'Codex 최종 판정 (docs/reviews/codex_lhs_release_final_verdict_20261001.md · 반입 중) 의 GO = **고정 v1.1 산출물 (194 행)** 의 DEM 계산값 전달에 한정 · '
                   '"미래 생성본 자동 승인 아님" · 물리 타깃 인증 HOLD 유지 ⇒ ps45 5 행은 같은 코드 · 같은 관문으로 만든 **새 생성본**이라 그 GO 밖이다 — '
                   '"v1.1 과 같은 코드 · 관문으로 계산" 은 쓸 수 있고 "Codex 검증 값" 은 쓸 수 없다',
    'design': 'am_pct = AM 질량 % (AM+SE 고체 중) · ps_frac = AM 중 AM_P 질량 몫 (AM 밀도 같아 부피 몫과 같음 · 개수 몫 아님)',
    'porosity_union_exact_pct': '정확 union (입자 겹침을 뺀 형상의 빈 부피 · MC 4×10⁶ 점 ± 1σ ≈ 0.02 %p — "exact" 는 합집합 정의라는 뜻이지 MC 오차 0 이 아니다 · '
                                '마지막 자릿수를 정밀도로 인용하지 말 것 · LHSREL-06) — 소성 압밀에서 밀려난 재료를 고체로 안 세는 상한 규약 · '
                                '웹앱 기본 ε_sphere (구 부피 합) 와 다른 양 · 두 값을 섞지 말 것',
    'thickness': 'thickness_wall_gap_um = 같은 프레임의 플래튼 − 바닥 (측정) · thickness_mass_conserving_um = union 과 같은 장부의 유도값 — "실제 두께" 는 벽 간격',
    'phi': 'phi_*_mass_conserving = (1 − ε_union) × 부피 몫 — φ_SE + φ_AM + ε_union = 1 · 독립 측정 아님 (레시피 · 두께로 정해짐)',
    'coverage': 'coverage_*_hertz_pct = 기하 교차 원판 면적 (LIGGGHTS c_cpl[22]) 기반 피복률 — 이름의 hertz 는 물려받은 이름 · 소성 (physics) 보정 피복률 아님 · '
                '벽 · 플래튼에 닿은 면은 분모에 남는다',
    'cn': 'CN = 상의 전 입자 평균 (접촉 0 · 벽 접촉 입자 포함) — 벽 효과가 섞인다 · ps45 두께 (≈ 111–117 µm) 는 130 (설계 29–52 µm) 의 2–4 배라 '
          '벽에 닿은 입자 비율이 다르다 — wall_touch_frac_* 를 함께 볼 것',
    'percolation_pct': '위 · 아래 2r 띠를 잇는 SE 덩어리에 든 SE 비율 — 그래프 관통이지 전류 계산이 아니다 · 0.0 = 잇는 덩어리 없음',
    'tortuosity': 'τ 는 벽 인접 띠에서 고른 같은 성분의 SE 중심 쌍에 대해 기하 최단경로 길이를 **그 쌍의 z 방향 중심 간격**으로 나눈 값 (두께로 나누지 않는다 · '
                  'v1.1 README §4 의 "길/두께" 는 틀린 문구 — LHSREL-05) · 최대 200 쌍 평균 · 중앙값 · **수송 τ 가 아니다** (협착 · 병목 안 봄) · '
                  'COMSOL/EIS 입력 τ (τ_Laplace,eff) 는 이 표에 없다 · 비관통이면 빈칸',
    'am_ionic_isolated_pct': '이온 경로 고립 = 등록된 상단 2r 경계 띠와 SE 접촉 그래프로 연결되지 않은 AM 비율 (= 100 − ionic_active_pct) — 실제 분리막 접촉 · '
                             '계면저항 · 이온 전류는 계산하지 않는다 (LHSREL-05 권고 문안) · **그래프 지표**',
    'am_vulnerable_pct': '고립 **위험** = SE 접촉 0–1 개인 AM 비율 (접촉 개수) — 경로 기준 고립과 다른 양',
    'se_largest_comp': '가장 큰 SE 덩어리 (SE 수 기준) 의 SE 비율 · 그 덩어리 두께 방향 폭 / 벽 간격 (표면 기준이라 관통 침대는 1 을 조금 넘는다)',
    'eligibility': 'physical_target_status HOLD 는 지우지 않는다 — 사유 = hold_reason_codes (BOUNDARY_CENTER_OUT · NEGATIVE_POROSITY) · boundary_state.  '
                   'OK 는 등록한 두 HOLD 원인이 없다는 뜻에 한정 (물리 검증 완료 아님) · HOLD 포함/제외 비교를 타당성 증거로 쓰지 않는다 (Codex 최종 판정 §4)',
    'sigma': '전도도 (σ_ion · σ_e · κ) 는 LHS 배포 범위 밖 — 이 표 · 이 요약에 없다.  덱에 σ 를 이 표의 값으로 적지 말 것',
    'cohort': '6 mAh/cm² · 두께 ≈ 111–117 µm · 입자 ≈ 16 만 · 바닥 벽 재질 = AM (type 1 · 생산 real_4 덱) — LHS 130 (2 mAh · 바닥 SE · J17) · '
              '64 와 분포 · 프로토콜이 다르다.  같은 표에 섞어 경향을 내지 말 것 (데이터셋 표지를 둔다)',
}


DEVIATIONS_STATIC = (
    '설계행 출처 — 130 은 lhs_design_20260818.csv (build() 산출) · ps45 는 덱에서 읽은 값 (make_ps45_design.py · 칸마다 출처 ps45_design_sources.tsv).  '
    '열 사전의 설계 열 문구는 생성기 고정 문구 ("LHS 설계 열 …") 그대로다 — 뜻은 같고 출처 문구만 다르다',
    'block — 0:10 · 10:0 은 질량분율 0 인 상을 선언한 3-type 덱이라 생성기 계약상 "bimodal" (J20-k (B): 수확 n_types 3 은 mono_* 를 받지 않는다).  '
    'LHS mono (mono_AM_P · mono_AM_S) 는 2-type 덱이다.  물리 모드는 요약의 physical_mode · 없는 상의 크기 칸은 130 mono 규약대로 빈칸',
    '웹앱 접촉 단계 — v1.1 코드 (d1ec42fba lhs_webapp_batch.resolve_mode) 는 0:10 · 10:0 을 REFUSED 한다 (덱 판독이 입자 0 개 상을 빼서 2 상 · 수확 JSON 3 상).  '
    '그 두 행의 웹앱 열 (CN · AM–SE CN · 고립 위험 · 퍼콜 · 이온 고립) 은 **측정 안 됨** (빈칸 = N/A 가 아니다) — 채우려면 관문 수정 = 새 커밋 (저자 결정)',
    'union — 130 의 union TSV 는 09-27 WSL 파일판 (sha256 앞 7f013f635a496147) · ps45 는 d1ec42fba 리포판 (같은 식 · 같은 난수열 · seed = crc32(case) — '
    '09-29 r45 union (a7350572f) 값과 대조)',
    '수확기 selftest — d1ec42fba 판으로 돌렸다 (1e09f661d 의 ⑰ 고정값 비교가 WSL numpy 에서 1 ULP — LHS-24 · 두 커밋의 차이는 selftest 뿐)',
    '코호트 — 130 은 area_s2_cohort.tsv · 64 는 _cohort.tsv (그때 봉인) · ps45 는 같은 도구 (seal_area_cohort @ 1e09f661d) 로 이번에 봉인',
    '덤프 — 웹앱 업로드 덤프 (09-22 · 09-25) · ibb post 폴더의 마지막 덤프인지는 미확인 (ps45 사전등록 §2 ⚠) — d_h 킷 · 09-29 union 과 같은 프레임',
    '침대 (설계 아님 · 프로토콜) — 6 mAh/cm² (130 = 2) · 입자 ≈ 16 만 (130 상한 10 만) · 바닥 벽 재질 type 1 = AM (130 = SE · J17) · '
    'maxattempt 10000 · processors * * 1 (삽입만) · 조성마다 시드 1 개',
    'Codex 최종 판정의 GO 는 고정 v1.1 산출물 (194 행) 에 한정 ("미래 생성본 자동 승인 아님") — ps45 5 행은 같은 코드 · 관문 · 열의 새 생성본이라 GO 밖',
)


class InputError(RuntimeError):
    pass


# ───────────────────────────── 작은 도구 ─────────────────────────────
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def num(v):
    if v in (None, ''):
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return v
    s = str(v)
    if s in ('True', 'False'):
        return s == 'True'
    try:
        x = float(s)
    except ValueError:
        return s
    return int(x) if (x.is_integer() and '.' not in s and 'e' not in s.lower()) else x


def read_csv(p):
    with open(p, encoding='utf-8', newline='') as fh:
        r = csv.DictReader(fh)
        return list(r.fieldnames or []), list(r)


def read_tsv(p):
    with open(p, encoding='utf-8', newline='') as fh:
        return list(csv.reader(fh, delimiter='\t'))


def git(repo, *a, binary=False):
    r = subprocess.run(['git', '-C', repo, *a], capture_output=True)
    if r.returncode != 0:
        raise InputError(f'git {" ".join(a)} 실패: {r.stderr.decode(errors="replace").strip()}')
    return r.stdout if binary else r.stdout.decode().strip()


def pin_tree(repo, dest, extra=()):
    """배포 v1.1 커밋의 파일을 `git archive` 로 꺼낸다 — 작업 트리 · HEAD 를 쓰지 않는다.  (경로, blob, HEAD 와 같은가) 기록을 돌려준다."""
    paths = [GEN, REL, CENSUS, V11_COLS['lhs130'], V11_COLS['lhsx64'], V11_CSV['lhs130'], V11_CSV['lhsx64'],
             'docs/data/lhs_descriptors_cov_1e09f661d/lhs00_000.json', 'docs/data/lhs_webapp_contact_d1ec42fba/metrics_flat.csv'] + list(extra)
    git(repo, 'cat-file', '-e', PIN + '^{commit}')
    data = git(repo, 'archive', '--format=tar', PIN, '--', *paths, binary=True)
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        safe_extract(tf, dest)
    rec = []
    for p in (GEN, REL, CENSUS, V11_COLS['lhs130'], V11_COLS['lhsx64']):
        b_pin = git(repo, 'rev-parse', f'{PIN}:{p}')
        try:
            b_head = git(repo, 'rev-parse', f'HEAD:{p}')
        except InputError:
            b_head = None
        rec.append(dict(path=p, blob_pin=b_pin, blob_head=b_head, head_equal=(b_pin == b_head)))
    return rec


def safe_extract(tf, dest):
    """tar 안전 풀기 — 절대 경로 · '..' · 링크 · 장치 파일은 거부한다."""
    root = os.path.realpath(dest)
    for m in tf.getmembers():
        name = m.name
        if name.startswith('/') or os.path.isabs(name) or '..' in name.replace('\\', '/').split('/'):
            raise InputError(f'tar 항목 경로가 안전하지 않다: {name!r}')
        if m.issym() or m.islnk() or m.isdev() or m.isfifo():
            raise InputError(f'tar 항목이 링크 · 장치다: {name!r}')
        tgt = os.path.realpath(os.path.join(root, name))
        if not (tgt == root or tgt.startswith(root + os.sep)):
            raise InputError(f'tar 항목이 풀 폴더 밖을 가리킨다: {name!r}')
    for m in tf.getmembers():
        if m.isdir():
            os.makedirs(os.path.join(root, m.name), exist_ok=True)
            continue
        f = tf.extractfile(m)
        out = os.path.join(root, m.name)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, 'wb') as fh:
            shutil.copyfileobj(f, fh)


def load_pinned_generator(pin_root):
    p = os.path.join(pin_root, GEN)
    spec = importlib.util.spec_from_file_location('lhs_design_dataset_pinned', p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ───────────────────────────── 생성기 · 배포 ─────────────────────────────
def run_generator(pin_root, design, harvest, union, webapp, out_csv, log):
    #  ⚠ 생성기는 상대 경로를 **자기 리포 루트** (고정 트리) 기준으로 푼다 — 전부 절대 경로로 넘긴다 (첫 건조 시험에서 잡힘)
    design, harvest, union, webapp, out_csv = (os.path.abspath(x) for x in (design, harvest, union, webapp, out_csv))
    cmd = [sys.executable, os.path.join(pin_root, GEN), '--export-handover', out_csv, '--design', design, '--harvest', harvest,
           '--union', union, '--webapp', webapp, '--webapp-groups', 'contact,percolation']
    r = subprocess.run(cmd, capture_output=True, text=True)
    log.append(dict(step='generator', cmd=' '.join(cmd), rc=r.returncode, stdout=r.stdout[-6000:], stderr=r.stderr[-6000:]))
    return r.returncode


def diagnose_rows(pin_root, design, harvest, union, webapp):
    """생성기가 거부했을 때 — 같은 모듈 (고정 커밋) 의 build_handover 를 행마다 따로 불러 **모든** 거부 사유를 모은다."""
    G = load_pinned_generator(pin_root)
    with open(design, encoding='utf-8-sig') as fh:
        rows = list(csv.DictReader(fh))
    harv = G.load_harvest(harvest)
    uv = G.load_union(union)
    wv = G.load_webapp(webapp, None)
    out = {}
    for r in rows:
        try:
            G.build_handover([r], harv, union=uv, webapp=wv, webapp_groups='contact,percolation')
            out[r['case_id']] = None
        except G.FillRefusal as e:
            out[r['case_id']] = str(e)
        except Exception as e:                                       # noqa: BLE001
            out[r['case_id']] = f'{type(e).__name__}: {e}'
    return out


def run_release(pin_root, handover_csv, cols_tsv, out_prefix, log):
    handover_csv, cols_tsv, out_prefix = (os.path.abspath(x) for x in (handover_csv, cols_tsv, out_prefix))
    cmd = [sys.executable, os.path.join(pin_root, REL), '--handover', handover_csv, '--columns-from', cols_tsv, '--out', out_prefix]
    r = subprocess.run(cmd, capture_output=True, text=True)
    log.append(dict(step='release_build', cmd=' '.join(cmd), rc=r.returncode, stdout=r.stdout[-3000:], stderr=r.stderr[-3000:]))
    return r.returncode


def compare_columns(pin_root, cohort, out_prefix):
    """배포 머리 · 열 사전 ↔ v1.1 (고정 커밋 바이트)."""
    v_head = read_csv(os.path.join(pin_root, V11_CSV[cohort]))[0]
    o_head = read_csv(out_prefix + '.csv')[0]
    v_dict = {r[0]: r for r in read_tsv(os.path.join(pin_root, V11_COLS[cohort]))[1:]}
    o_rows = read_tsv(out_prefix + '_columns.tsv')
    diff = [r[0] for r in o_rows[1:] if v_dict.get(r[0]) != r]
    return dict(header_equal=(v_head == o_head), n_cols=len(o_head), n_cols_v11=len(v_head),
                missing=[c for c in v_head if c not in o_head], extra=[c for c in o_head if c not in v_head],
                columns_tsv_rows_differ=diff,
                columns_tsv_bytes_equal=(open(out_prefix + '_columns.tsv', 'rb').read()
                                         == open(os.path.join(pin_root, V11_COLS[cohort]), 'rb').read()))


# ───────────────────────────── 건조 시험 ─────────────────────────────
def replay(repo, cohort, out, cases=None):
    """커밋된 v1.1 원천의 일부 행 → 같은 생성기 · 배포 빌더 → 커밋된 v1.1 배포 행과 바이트 비교."""
    spec = REPLAY[cohort]
    cases = list(cases or spec['cases'])
    out = os.path.abspath(out)
    os.makedirs(out, exist_ok=True)
    pin = os.path.join(out, f'_pin_{PIN[:9]}')
    if os.path.exists(pin):
        shutil.rmtree(pin)
    pinrec = pin_tree(repo, pin, extra=[spec['design'], spec['harvest'], spec['union'], spec['webapp']])
    with open(os.path.join(pin, spec['design']), encoding='utf-8-sig') as fh:
        rd = csv.DictReader(fh)
        head, rows = rd.fieldnames, [r for r in rd if r['case_id'] in set(cases)]
    if len(rows) != len(cases):
        raise InputError(f'설계에 없는 건조 시험 행: {sorted(set(cases) - {r["case_id"] for r in rows})}')
    rows.sort(key=lambda r: cases.index(r['case_id']))
    dsub = os.path.join(out, f'replay_{cohort}_design.csv')
    with open(dsub, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, head, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)
    log = []
    hcsv = os.path.join(out, f'replay_{cohort}_handover.csv')
    rc = run_generator(pin, dsub, os.path.join(pin, spec['harvest']), os.path.join(pin, spec['union']),
                       os.path.join(pin, spec['webapp']), hcsv, log)
    rep = dict(cohort=cohort, cases=cases, pin=PIN, pinned_files=pinrec, generator_rc=rc)
    if rc != 0:
        rep['refusals'] = diagnose_rows(pin, dsub, os.path.join(pin, spec['harvest']), os.path.join(pin, spec['union']),
                                        os.path.join(pin, spec['webapp']))
        rep['ok'] = False
        rep['log'] = log
        return rep
    prefix = os.path.join(out, f'replay_{cohort}_release')
    rc2 = run_release(pin, hcsv, os.path.join(pin, V11_COLS[cohort]), prefix, log)
    rep['release_rc'] = rc2
    if rc2 != 0:
        rep['ok'] = False
        rep['log'] = log
        return rep
    #  행 바이트 비교 — 같은 csv 작성기 (기본 quoting · '\n') 라 줄 문자열이 같아야 한다
    v_lines = open(os.path.join(pin, V11_CSV[cohort]), encoding='utf-8').read().split('\n')
    o_lines = open(prefix + '.csv', encoding='utf-8').read().split('\n')
    v_by = {ln.split(',', 1)[0]: ln for ln in v_lines[1:] if ln}
    diffs = []
    for ln in o_lines[1:]:
        if not ln:
            continue
        cid = ln.split(',', 1)[0]
        if v_by.get(cid) != ln:
            a, b = next(csv.reader([ln])), next(csv.reader([v_by.get(cid, '')]))
            hd = next(csv.reader([o_lines[0]]))
            cell = [(hd[i], a[i], b[i] if i < len(b) else None) for i in range(len(a)) if i >= len(b) or a[i] != b[i]]
            diffs.append(dict(case=cid, n_cells=len(cell), first=cell[:5]))
    rep['rows_byte_equal'] = (not diffs) and (len([x for x in o_lines[1:] if x]) == len(cases))
    rep['row_diffs'] = diffs
    rep['columns'] = compare_columns(pin, cohort, prefix)
    rep['summary_probe'] = summarize_rows(prefix + '.csv', hcsv, {})['rows'][:2]      # 요약 작성기도 같은 행으로 시험
    rep['ok'] = bool(rep['rows_byte_equal'] and rep['columns']['header_equal'] and rep['columns']['columns_tsv_bytes_equal'])
    rep['log'] = log
    return rep


# ───────────────────────────── 본번 입력 대조 ─────────────────────────────
def find_root(d):
    for dirpath, _dirs, files in os.walk(d):
        if 'RUN_MANIFEST.json' in files:
            return dirpath
    raise InputError(f'{d}: RUN_MANIFEST.json 이 없다 — run_ps45_lhs_wsl.sh 의 산출이 아니다')


def check_inputs(root, design_rows, pin_root):
    """fail-closed — 산출이 v1.1 과 같은 코드 · 같은 단계에서 나왔는가.  (문제 목록, 정보) 를 돌려준다."""
    probs, info = [], {}
    man = json.load(open(os.path.join(root, 'RUN_MANIFEST.json'), encoding='utf-8'))
    info['manifest'] = {k: man.get(k) for k in ('schema', 'started', 'finished', 'one', 'deck_from', 'dump_root', 'worktrees', 'stages',
                                                'python', 'versions', 'dirty_after')}
    wt = man.get('worktrees') or {}
    if (wt.get('harvest') or {}).get('sha') != SHA_H:
        probs.append(f'수확 워크트리 커밋 {(wt.get("harvest") or {}).get("sha")} ≠ {SHA_H[:9]}')
    if (wt.get('webapp') or {}).get('sha') != SHA_W:
        probs.append(f'웹앱 워크트리 커밋 {(wt.get("webapp") or {}).get("sha")} ≠ {SHA_W[:9]}')
    if man.get('one'):
        probs.append(f'ONE 모드 산출 ({man.get("one")}) — 한 건 시간 시험이다 · 5 침대 전 건으로 다시 돌릴 것')
    if man.get('beds_table') != 'builtin':
        probs.append(f'시험용 침대 표로 돈 산출 ({man.get("beds_table")}) — 본번이 아니다')
    want = [r['case_id'] for r in design_rows]
    #  코호트
    coh = os.path.join(root, 'cohort', 'ps45_cohort.tsv')
    if not os.path.isfile(coh):
        probs.append('cohort/ps45_cohort.tsv 없음')
        crow = {}
    else:
        lines = [ln for ln in open(coh, encoding='utf-8').read().splitlines() if not ln.lstrip().startswith('#')]
        crow = {r['case']: r for r in csv.DictReader(lines, delimiter='\t')}
        info['cohort_header'] = [ln for ln in open(coh, encoding='utf-8').read().splitlines() if ln.startswith('#')][:2]
        for c in want:
            r = crow.get(c)
            if r is None:
                probs.append(f'{c}: 코호트에 없다')
            elif r.get('status') != 'RAW_OK' or r.get('n_types') != '3':
                probs.append(f'{c}: 코호트 상태 {r.get("status")} · n_types {r.get("n_types")} (RAW_OK · 3 이어야)')
    #  수확
    hdir = os.path.join(root, 'harvest')
    bs = os.path.join(hdir, '_batch_summary.json')
    if not os.path.isfile(bs):
        probs.append('harvest/_batch_summary.json 없음')
    else:
        b = json.load(open(bs, encoding='utf-8'))
        info['harvest_batch'] = dict(n_target=b.get('n_target'), n_ok=b.get('n_ok'), sha_verified=b.get('sha_verified'))
        if b.get('sha_verified') is not True:
            probs.append('수확 배치가 --verify-sha 로 돌지 않았다')
        bad = [r['case'] for r in b.get('records', []) if r.get('status') != 'OK']
        if bad:
            probs.append(f'수확 실패 행: {bad}')
    ref = json.load(open(os.path.join(pin_root, 'docs/data/lhs_descriptors_cov_1e09f661d/lhs00_000.json'), encoding='utf-8'))
    for c in want:
        p = os.path.join(hdir, f'{c}.json')
        if not os.path.isfile(p):
            probs.append(f'{c}: 수확 JSON 없음')
            continue
        h = json.load(open(p, encoding='utf-8'))
        if set(h) != set(ref):
            probs.append(f'{c}: 수확 JSON 키 집합이 v1.1 수확 (1e09f661d) 과 다르다 — 빠짐 {sorted(set(ref) - set(h))[:5]} · '
                         f'더함 {sorted(set(h) - set(ref))[:5]}')
        for k in ('measurement_protocol_id',):
            a, b_ = (h.get('handover_qc') or {}).get(k), (ref.get('handover_qc') or {}).get(k)
            if a != b_:
                probs.append(f'{c}: {k} {a!r} ≠ v1.1 {b_!r}')
        if (h.get('tau_wall_detail') or {}).get('tau_convention') != (ref.get('tau_wall_detail') or {}).get('tau_convention'):
            probs.append(f'{c}: 벽 τ 규약이 v1.1 수확과 다르다')
        r = crow.get(c) or {}
        for k, ck in (('atom', 'atom_sha256'), ('contact', 'contact_sha256'), ('deck', 'deck_sha256')):
            if r and ((h.get('raw') or {}).get(k) or {}).get('sha256') != r.get(ck):
                probs.append(f'{c}: 수확 {k} sha ≠ 봉인 코호트')
    #  웹앱 접촉 단계
    wdir = os.path.join(root, 'webapp_contact')
    st = json.load(open(os.path.join(wdir, 'status.json'), encoding='utf-8')) if os.path.isfile(os.path.join(wdir, 'status.json')) else None
    if st is None:
        probs.append('webapp_contact/status.json 없음')
    else:
        runs = st.get('runs') or []
        info['webapp_runs'] = runs
        if st.get('schema') != 'lhs_webapp_batch/v1' or st.get('stop_after') != 'contact':
            probs.append(f'웹앱 배치 schema {st.get("schema")} · stop_after {st.get("stop_after")} (lhs_webapp_batch/v1 · contact 이어야 — v1.1 원천과 같은 단계)')
        if not runs or any(r.get('git_sha') != SHA_W for r in runs):
            probs.append(f'웹앱 배치 실행 커밋 {[r.get("git_sha", "")[:9] for r in runs]} — 전부 {SHA_W[:9]} 이어야 (세대 혼합 금지 · SELF-76)')
        cs = st.get('cases') or {}
        info['webapp_status'] = {c: dict(status=(cs.get(c) or {}).get('status'), why=(cs.get(c) or {}).get('why'),
                                         elapsed_s=(cs.get(c) or {}).get('elapsed_s')) for c in want}
        miss = [c for c in want if c not in cs]
        if miss:
            probs.append(f'웹앱 배치가 시도하지 않은 침대: {miss}')
        #  metrics_flat 머리 ⊆ v1.1 (d1ec42fba) 웹앱 머리 — 같은 웹앱 세대인가
        mf = os.path.join(wdir, 'metrics_flat.csv')
        if os.path.isfile(mf):
            hd = read_csv(mf)[0]
            ref_hd = set(read_csv(os.path.join(pin_root, 'docs/data/lhs_webapp_contact_d1ec42fba/metrics_flat.csv'))[0])
            extra_k = [k for k in hd if k not in ref_hd]
            info['webapp_metrics_cols'] = dict(n=len(hd), not_in_v11_header=extra_k)
            if extra_k:
                probs.append(f'웹앱 metrics_flat 에 v1.1 (d1ec42fba · 130) 머리에 없는 키 {len(extra_k)} 개 {extra_k[:5]} — 다른 웹앱 세대')
    #  union
    up = os.path.join(root, 'union', 'ps45_union.tsv')
    if not os.path.isfile(up):
        probs.append('union/ps45_union.tsv 없음')
    else:
        with open(up, encoding='utf-8') as fh:
            ur = {r['case']: r for r in csv.DictReader(fh, delimiter='\t')}
        info['union_status'] = {c: (ur.get(c) or {}).get('status') for c in want}
    #  퍼콜 감사
    pa = os.path.join(root, 'perc_audit', 'perc_audit.tsv')
    info['perc_audit'] = {}
    if os.path.isfile(pa):
        with open(pa, encoding='utf-8') as fh:
            for r in csv.DictReader(fh, delimiter='\t'):
                info['perc_audit'][r['case']] = dict(status=r.get('status'), verdict=r.get('verdict'), why=r.get('why'))
    else:
        info['perc_audit_missing'] = True
    return probs, info, man


#: 0:10 · 10:0 재실행 (LHS-28 관문 수정 커밋 · 1저자 10-01) — 웹앱 접촉 단계의 **계산 코드**는 d1ec42fba 와 같아야 한다:
#:   두 커밋 사이 webapp/ · scripts/ 의 .py 변경이 이 목록 안이어야 (관문 파일 하나 + 접촉 단계가 부르지 않는 B 단계 · 시험 파일).
FIX_ALLOWED_PY = ('scripts/lhs_webapp_batch.py', 'scripts/lhs_design_dataset.py', 'scripts/lhs_release_build.py',
                  'webapp/test_png_transparent_export.py')
FIX_STATIC_NOTE = ('웹앱 접촉 단계 — 0:10 · 10:0 은 v1.1 코드 (d1ec42fba) 관문에서 REFUSED (덱 판독이 입자 0 개 상을 빼서 2 상 · 수확 JSON 3 상) → '
                   'LHS-28 관문 수정 커밋으로 그 두 침대만 재실행해 합쳤다.  계산 코드 (run_pipeline 과 그 아래) 는 d1ec42fba 와 같다 — '
                   '두 커밋 사이 .py 변경 = 관문 파일 + 접촉 단계 밖 파일뿐 (summary inputs.webapp_fix.code_diff_py) · 나머지 세 침대는 d1ec42fba 원래 행 그대로')


def find_dir_with(d, name):
    for dirpath, _dirs, files in os.walk(d):
        if name in files:
            return dirpath
    raise InputError(f'{d}: {name} 이 없다')


def merge_webapp_fix(repo, root, fix_root, fix_commit, pin_root, out_dir):
    """0:10 · 10:0 재실행 산출을 원래 웹앱 산출 (d1ec42fba) 에 합친다 — 원래 폴더는 그대로 두고 `out_dir/webapp_contact_merged` 에 새로 쓴다.

    (문제 목록, 정보, 합친 폴더 | None).  fail-closed: 재실행 = 원래 REFUSED 침대와 **정확히 같은 집합** · 전부 done · 같은 프레임 (네 파일 sha =
    수확 JSON) · `type_map_absent` = 수확 phase_counts 의 0 상 · 실행 커밋 = fix_commit (깨끗함) · 두 커밋 사이 계산 코드 변경 없음 · 원래 done 행은 안 바꾼다.
    """
    probs, info = [], dict(fix_commit=fix_commit)
    st0 = json.load(open(os.path.join(root, 'webapp_contact', 'status.json'), encoding='utf-8'))
    pf = os.path.join(fix_root, 'status.json')
    if not os.path.isfile(pf):
        return [f'재실행 status.json 없음: {fix_root}'], info, None
    stf = json.load(open(pf, encoding='utf-8'))
    if stf.get('schema') != 'lhs_webapp_batch/v1' or stf.get('stop_after') != 'contact':
        probs.append(f'재실행 schema {stf.get("schema")} · stop_after {stf.get("stop_after")} (lhs_webapp_batch/v1 · contact 이어야)')
    runs = stf.get('runs') or []
    info['fix_runs'] = runs
    if not runs or any(r.get('git_sha') != fix_commit or r.get('dirty') for r in runs):
        probs.append(f'재실행 커밋 {[str(r.get("git_sha"))[:9] for r in runs]} · dirty {[r.get("dirty") for r in runs]} — '
                     f'전부 {fix_commit[:9]} · 깨끗해야')
    refused = sorted(c for c, r in (st0.get('cases') or {}).items() if (r or {}).get('status') == 'REFUSED')
    fc = stf.get('cases') or {}
    info['refused_in_original'] = refused
    info['fix_cases'] = {c: dict(status=r.get('status'), why=r.get('why'), type_map=r.get('type_map'),
                                 type_map_absent=r.get('type_map_absent'), elapsed_s=r.get('elapsed_s')) for c, r in fc.items()}
    if sorted(fc) != refused:
        probs.append(f'재실행 침대 {sorted(fc)} ≠ 원래 REFUSED {refused} — 원래 done 행은 바꾸지 않고 · 빠진 침대도 없어야')
    for c, r in fc.items():
        if r.get('status') != 'done':
            probs.append(f'{c}: 재실행 상태 {r.get("status")} ({r.get("why")})')
        hp = os.path.join(root, 'harvest', f'{c}.json')
        if not os.path.isfile(hp):
            probs.append(f'{c}: 수확 JSON 없음')
            continue
        h = json.load(open(hp, encoding='utf-8'))
        for k in ('atom', 'contact', 'mesh', 'deck'):
            if (r.get('sha') or {}).get(k) != ((h.get('raw') or {}).get(k) or {}).get('sha256'):
                probs.append(f'{c}: 재실행 {k} sha ≠ 수확 JSON — 다른 프레임')
        pc, tm = h.get('phase_counts') or {}, h.get('type_map') or {}
        want = ','.join(f'{t}:{ph}' for t, ph in sorted(tm.items(), key=lambda kv: int(kv[0])) if pc.get(ph) == 0)
        if not want or r.get('type_map_absent') != want:
            probs.append(f'{c}: type_map_absent {r.get("type_map_absent")!r} ≠ 수확 phase_counts 의 0 상 {want!r}')
    mff = os.path.join(fix_root, 'metrics_flat.csv')
    if not os.path.isfile(mff):
        probs.append('재실행 metrics_flat.csv 없음')
        return probs, info, None
    hd0, rows0 = read_csv(os.path.join(root, 'webapp_contact', 'metrics_flat.csv'))
    hdf, rowsf = read_csv(mff)
    ref_hd = set(read_csv(os.path.join(pin_root, 'docs/data/lhs_webapp_contact_d1ec42fba/metrics_flat.csv'))[0])
    extra = [k for k in hdf if k not in ref_hd]
    if extra:
        probs.append(f'재실행 metrics_flat 에 v1.1 (d1ec42fba · 130) 머리에 없는 키 {len(extra)} 개 {extra[:5]}')
    if sorted(r['case'] for r in rowsf) != sorted(fc):
        probs.append(f'재실행 metrics_flat 행 {sorted(r["case"] for r in rowsf)} ≠ 재실행 침대 {sorted(fc)}')
    if {r['case'] for r in rowsf} & {r['case'] for r in rows0}:
        probs.append('재실행 행이 원래 metrics_flat 에 이미 있다 — 원래 행을 덮지 않는다')
    try:
        git(repo, 'cat-file', '-e', fix_commit + '^{commit}')
        ch = [p for p in git(repo, 'diff', '--name-only', SHA_W, fix_commit).splitlines()
              if p.endswith('.py') and p.startswith(('webapp/', 'scripts/'))]
        info['code_diff_py'] = ch
        bad = [p for p in ch if p not in FIX_ALLOWED_PY]
        if bad:
            probs.append(f'd1ec42fba ↔ {fix_commit[:9]} 사이 계산 코드 변경 {bad} — 같은 웹앱 세대가 아니다')
        if 'scripts/lhs_webapp_batch.py' not in ch:
            probs.append(f'{fix_commit[:9]} 에 관문 수정 (scripts/lhs_webapp_batch.py) 이 없다')
    except InputError as e:
        probs.append(f'재실행 커밋 확인 실패: {e}')
    md = os.path.join(out_dir, 'webapp_contact_merged')
    if os.path.exists(md):
        shutil.rmtree(md)
    os.makedirs(md)
    st = json.loads(json.dumps(st0))
    for c, r in fc.items():
        rr = dict(r)
        rr['merged_from'] = dict(commit=fix_commit, why='LHS-28 관문 수정 뒤 재실행 (원래 REFUSED)',
                                 original_refusal=(st0['cases'].get(c) or {}).get('why'))
        st['cases'][c] = rr
    st['runs'] = list(st0.get('runs') or []) + [dict(x, merged_fix=True) for x in runs]
    st['merged_fix'] = dict(commit=fix_commit, cases=sorted(fc))
    _write_json(os.path.join(md, 'status.json'), st)
    cols = list(hd0) + [k for k in hdf if k not in hd0]
    with open(os.path.join(md, 'metrics_flat.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for r in sorted(rows0 + rowsf, key=lambda x: x['case']):
            w.writerow({k: r.get(k, '') for k in cols})
    return probs, info, md


# ───────────────────────────── 요약 · 관문 ─────────────────────────────
def summarize_rows(release_csv, handover_csv, ctx):
    """배포 행 + 인계표 보조 열 → 조성별 값 · 표지.  ctx = dict(expect, info, manifest, design)."""
    _h, rel = read_csv(release_csv)
    _hh, hand = read_csv(handover_csv)
    hby = {r['case_id']: r for r in hand}
    exp = (ctx.get('expect') or {}).get('cases') or {}
    info = ctx.get('info') or {}
    man = ctx.get('manifest') or {}
    dby = {r['case_id']: r for r in (ctx.get('design') or [])}
    out = []
    for r in rel:
        c = r['case_id']
        h = hby.get(c, {})
        e = exp.get(c)
        vals = {k: num(r.get(k)) for k in SUMMARY_COLS}
        aux = {k: num(h.get(k)) for k in EXTRA_COLS}
        np_, ns_ = num(r.get('n_AM_P_measured')) or 0, num(r.get('n_AM_S_measured')) or 0
        mode = ('bimodal (AM_P + AM_S)' if (np_ and ns_) else
                ('단일 AM_P (3-type 덱 · AM_S 질량분율 0)' if np_ else ('단일 AM_S (3-type 덱 · AM_P 질량분율 0)' if ns_ else '?')))
        gates, xch = {}, {}
        #  G1 웹앱 상태 — done 이 아니면 웹앱 열 (CN · AM–SE · 퍼콜 · 이온 · 고립 위험) 이 빈칸이다
        ws = h.get('wa_status')
        why = ((info.get('webapp_status') or {}).get(c) or {}).get('why')
        gates['webapp_done'] = dict(ok=(ws == 'done'), value=ws, why=why)
        #  G2 퍼콜 감사 (J20-b 규칙 ⓑ — CLEAN 이어야 퍼콜 열이 명목 정의)
        pa = (info.get('perc_audit') or {}).get(c)
        if pa is None:
            gates['perc_audit_clean'] = dict(ok=None, value='감사 없음' if ctx else 'n/a')
        else:
            gates['perc_audit_clean'] = dict(ok=(pa.get('verdict') == 'CLEAN'), value=pa.get('verdict'), why=pa.get('why'))
        #  G3 수확 상태 — 있는 상 = OK · 없는 상 = N_A_PHASE_ABSENT
        bad = []
        if h.get('phi_se_status') != 'OK':
            bad.append(f'phi {h.get("phi_se_status")}')
        for ph, n_ in (('AM_P', np_), ('AM_S', ns_)):
            s_ = h.get(f'coverage_{ph}_hertz_pct_status')
            if (n_ and s_ != 'OK') or (not n_ and s_ != 'N_A_PHASE_ABSENT'):
                bad.append(f'coverage_{ph} {s_} (입자 {n_})')
        gates['harvest_status'] = dict(ok=not bad, value=bad or 'OK')
        #  G4 벽 τ 상태
        ts = h.get('tortuosity_SE_wall_status')
        gates['tau_wall_status'] = dict(ok=ts in ('OK', 'NOT_PERCOLATING'), value=ts)
        #  G5 단계 rc (본번만)
        stg = man.get('stages') or {}
        if stg:
            badst = {k: v for k, v in stg.items() if k in ('seal', 'harvest', 'union') and v not in (0, '0')}
            gates['stage_rc'] = dict(ok=not badst, value=stg)
        #  X 같은 프레임 대조 (본번만 · 기대값이 있을 때)
        if e:
            def xc(name, got, want, tol, hard=True):
                if want is None:                     # 기대값이 없다 = 검사하지 않음 (실패 아님)
                    xch[name] = dict(ok=None, got=got, want=None, tol=tol, hard=hard, note='기대값 없음 — 검사 안 함')
                    return
                if got is None:                      # 기대값은 있는데 값이 없다 = 실패 (빈칸을 통과로 읽지 않는다)
                    xch[name] = dict(ok=False if hard else None, got=None, want=want, tol=tol, hard=hard)
                    return
                ok = abs(float(got) - float(want)) <= tol
                xch[name] = dict(ok=ok if hard else (ok or None), got=got, want=want, tol=tol, hard=hard)
            xc('n_AM_P', vals['n_AM_P_measured'] if np_ else 0, e['n_AM_P'], 0)
            xc('n_AM_S', vals['n_AM_S_measured'] if ns_ else 0, e['n_AM_S'], 0)
            xc('n_SE', vals['n_SE_measured'], e['n_SE'], 0)
            xc('atom_step', aux['timestep'], e['atom_step'], 0)
            xc('sphere_porosity_vs_kit_pct', aux['porosity_sphere_pct_RECORD_ONLY'], e['kit_sphere_pct'], 1e-6)
            xc('thickness_wall_gap_vs_kit_um', vals['thickness_wall_gap_um'], e['kit_thickness_um'], 1e-6)
            xc('union_exact_vs_r45_pct', vals['porosity_union_exact_pct'], e['union_exact_pct'], 5e-5)
            xc('union_exact_se_vs_r45_pct', aux['porosity_union_exact_se_pct'], e['union_exact_se_pct'], 5e-5)
            xc('thickness_vs_r45_um', vals['thickness_wall_gap_um'], e['thickness_um'], 5e-4)
            #  피복률 ↔ 업로드 시점 (09-22/25) 웹앱 값 — 코드 세대가 달라 **정보** (일치하면 같은 c_cpl[22] 식 · 같은 프레임의 덤 증거)
            xc('coverage_AM_P_vs_kit_pct (정보)', vals['coverage_AM_P_hertz_pct'], e.get('kit_cov_AM_P'), 1e-9, hard=False)
            xc('coverage_AM_S_vs_kit_pct (정보)', vals['coverage_AM_S_hertz_pct'], e.get('kit_cov_AM_S'), 1e-9, hard=False)
            d = dby.get(c) or {}
            if d.get('ps45_deck_sha256') and aux.get('deck_sha256') is not None:
                xch['deck_sha256_vs_repo_deck'] = dict(ok=(str(aux['deck_sha256']) == d['ps45_deck_sha256']), got=aux['deck_sha256'],
                                                       want=d['ps45_deck_sha256'], hard=False,
                                                       note='다르면 업로드 덱을 썼다 (DECK_FROM=upload) — 편차로 적는다')
        #  B 추가 관문 (값을 바꾸지 않는다 · Codex 최종 판정 LHSREL-01 · 02 · 04 의 해제 증거 형태 — 같은 생성기가 막지 않는 빈틈을 이 표에서만 본다)
        hn = {k: num(h.get(k)) for k in ('V_SE_full_um3', 'V_AM_full_um3')}
        n_ph = {'전체': (np_ or 0) + (ns_ or 0), 'AM_P': np_ or 0, 'AM_S': ns_ or 0}
        bad1 = []
        for lab, pre in (('전체', 'ionic_'), ('AM_P', 'AM_P_ionic_'), ('AM_S', 'AM_S_ionic_')):
            for st_ in ('active', 'dead', 'no_se'):
                v = num(r.get(f'{pre}{st_}_pct')) if lab != '전체' or st_ != 'active' else num(r.get('ionic_active_pct'))
                if v is None:
                    continue
                cnt = v * n_ph[lab] / 100.0
                if not (isinstance(v, (int, float)) and 0.0 <= v <= 100.0 and -1e-6 <= cnt <= n_ph[lab] + 1e-6):
                    bad1.append(f'{lab} {st_} {v}')
        gates['xtra_ionic_bounds (LHSREL-01)'] = dict(ok=not bad1, value=bad1 or 'OK')
        ps_, hc_, bs_ = r.get('physical_target_status'), r.get('hold_reason_codes') or '', r.get('boundary_state')
        codes = [c_ for c_ in hc_.split('|') if c_]
        ok2 = (ps_ in ('OK', 'HOLD') and bs_ in ('INSIDE', 'CENTER_CROSSED', 'FULLY_OUT')
               and set(codes) <= {'BOUNDARY_CENTER_OUT', 'NEGATIVE_POROSITY'} and ((ps_ == 'HOLD') == bool(codes)))
        gates['xtra_eligibility (LHSREL-02)'] = dict(ok=ok2, value=dict(status=ps_, codes=codes, boundary=bs_))
        eps, phs, sos = vals.get('porosity_union_exact_pct'), vals.get('phi_se_mass_conserving'), vals.get('se_of_solid_vol')
        if None not in (eps, phs, sos, hn['V_SE_full_um3'], hn['V_AM_full_um3']):
            sos_h = hn['V_SE_full_um3'] / (hn['V_SE_full_um3'] + hn['V_AM_full_um3'])
            ok4 = (0.0 <= sos <= 1.0 and abs(phs - (1.0 - eps / 100.0) * sos) <= 1e-9 and abs(sos - sos_h) <= 1e-9)
            gates['xtra_se_fraction_ledger (LHSREL-04)'] = dict(ok=ok4, value=dict(se_of_solid_vol=sos, from_harvest_volumes=sos_h,
                                                                                    phi_se_expected=(1.0 - eps / 100.0) * sos, phi_se=phs))
        else:
            gates['xtra_se_fraction_ledger (LHSREL-04)'] = dict(ok=False, value='값 없음')
        hard_fail = [k for k, g in gates.items() if g.get('ok') is False]
        hard_fail += [k for k, x in xch.items() if x.get('ok') is False and x.get('hard', True)]
        out.append(dict(case_id=c, ps_label=r.get('ps_label'), ps_frac=num(r.get('ps_frac')), physical_mode=mode,
                        webapp_case_id=(e or {}).get('webapp_case_id'), atom_step=aux.get('timestep'),
                        values=vals, values_aux={k: aux[k] for k in ('porosity_union_exact_se_pct', 'porosity_sphere_pct_RECORD_ONLY',
                                                                     'tortuosity_SE_wall_status', 'wa_status', 'union_pair_upper_bound_ok',
                                                                     'boundary_model_id')},
                        eligibility={k: r.get(k) for k in ELIG_COLS},
                        gates=gates, xchecks=xch, row_ok=not hard_fail, row_fail=hard_fail))
    return dict(rows=out)


def post(args):
    args.out = os.path.abspath(args.out)
    os.makedirs(args.out, exist_ok=True)
    t0 = time.time()
    log = []
    #  ① 입력 (tar → 풀기)
    tar_sha = None
    if args.tar:
        tar_sha = sha256_file(args.tar)
        if args.sha256 and tar_sha != args.sha256.lower():
            raise InputError(f'tar sha256 {tar_sha} ≠ 받은 값 {args.sha256} — 전송 손상 · 다른 묶음')
        xdir = os.path.join(args.out, 'input')
        if os.path.exists(xdir):
            shutil.rmtree(xdir)
        with tarfile.open(args.tar) as tf:
            safe_extract(tf, xdir)
        root = find_root(xdir)
    else:
        root = find_root(args.dir)
    #  ② 코드 고정
    pin = os.path.join(args.out, f'_pin_{PIN[:9]}')
    if os.path.exists(pin):
        shutil.rmtree(pin)
    pinrec = pin_tree(args.repo, pin)
    with open(args.design, encoding='utf-8-sig') as fh:
        design = list(csv.DictReader(fh))
    expect = json.load(open(args.expect, encoding='utf-8')) if args.expect else {}
    probs, info, man = check_inputs(root, design, pin)
    wdir = os.path.join(root, 'webapp_contact')
    fix_tar_sha = None
    if args.webapp_fix_tar or args.webapp_fix_dir:
        if not args.fix_commit:
            raise InputError('--webapp-fix-* 에는 --fix-commit (관문 수정 커밋 전체 sha) 이 필요하다')
        if args.webapp_fix_tar:
            fix_tar_sha = sha256_file(args.webapp_fix_tar)
            if args.webapp_fix_sha256 and fix_tar_sha != args.webapp_fix_sha256.lower():
                raise InputError(f'재실행 tar sha256 {fix_tar_sha} ≠ 받은 값 {args.webapp_fix_sha256}')
            fx = os.path.join(args.out, 'input_fix')
            if os.path.exists(fx):
                shutil.rmtree(fx)
            with tarfile.open(args.webapp_fix_tar) as tf:
                safe_extract(tf, fx)
            fix_root = find_dir_with(fx, 'status.json')
        else:
            fix_root = args.webapp_fix_dir
        p2, i2, md = merge_webapp_fix(args.repo, root, fix_root, args.fix_commit, pin, args.out)
        i2['tar_sha256'] = fix_tar_sha
        info['webapp_fix'] = i2
        probs += [f'재실행: {p}' for p in p2]
        if md:
            wdir = md
            for c, r in (i2.get('fix_cases') or {}).items():
                if c in (info.get('webapp_status') or {}):
                    info['webapp_status'][c] = dict(status=r.get('status'), why=r.get('why'), elapsed_s=r.get('elapsed_s'))
    rep = dict(schema='ps45_lhs_post/v1', when=time.strftime('%Y-%m-%dT%H:%M:%S'), tar=args.tar and os.path.basename(args.tar),
               tar_sha256=tar_sha, sha256_expected=args.sha256,
               code=dict(generator_release=PIN, harvest=SHA_H, webapp_union_audit=SHA_W,
                         **({'webapp_fix_0_10_10_0': args.fix_commit} if (args.webapp_fix_tar or args.webapp_fix_dir) else {})),
               pinned_files=pinrec, design=os.path.basename(args.design), design_sha256=sha256_file(args.design),
               expect=os.path.basename(args.expect) if args.expect else None, input_checks=probs, inputs=info, qualifiers=QUALIFIERS)
    if probs and not args.force_inputs:
        rep['verdict'] = 'INPUT_REFUSED'
        _write_json(os.path.join(args.out, 'ps45_summary.json'), rep)
        for p in probs:
            print('⛔ 입력:', p)
        return 2
    #  ③ 인계표 (v1.1 과 같은 CLI · 같은 인자)
    hcsv = os.path.join(args.out, 'ps45_handover.csv')
    rc = run_generator(pin, args.design, os.path.join(root, 'harvest'), os.path.join(root, 'union', 'ps45_union.tsv'),
                       wdir, hcsv, log)
    rep['generator_rc'] = rc
    if rc != 0:
        rep['refusals_by_row'] = diagnose_rows(pin, args.design, os.path.join(root, 'harvest'), os.path.join(root, 'union', 'ps45_union.tsv'),
                                               wdir)
        rep['verdict'] = 'GENERATOR_REFUSED'
        rep['log'] = log
        _write_json(os.path.join(args.out, 'ps45_summary.json'), rep)
        print('⛔ 생성기 거부 — 표를 만들지 않는다.  행별 사유:')
        for c, m in rep['refusals_by_row'].items():
            print(f'   {c}: {m or "이 행은 혼자 통과 — 다른 행의 거부로 표 전체가 서지 않았다 (부분 표는 만들지 않는다)"}')
        return 1
    #  ④ 배포 (v1.1 열 사전의 열 · 순서)
    prefix = os.path.join(args.out, 'ps45_release_5rows')
    rc2 = run_release(pin, hcsv, os.path.join(pin, V11_COLS['lhs130']), prefix, log)
    rep['release_rc'] = rc2
    if rc2 != 0:
        rep['verdict'] = 'RELEASE_BUILD_FAILED'
        rep['log'] = log
        _write_json(os.path.join(args.out, 'ps45_summary.json'), rep)
        print('⛔ 배포 빌더 실패 —', log[-1]['stderr'] or log[-1]['stdout'])
        return 1
    rep['columns'] = compare_columns(pin, 'lhs130', prefix)
    #  ⑤ 행 관문 · 요약
    s = summarize_rows(prefix + '.csv', hcsv, dict(expect=expect, info=info, manifest=man, design=design))
    rows = s['rows']
    want = [r['case_id'] for r in design]
    got = [r['case_id'] for r in rows]
    rep['rows'] = rows
    rep['row_count'] = dict(design=len(want), release=len(got), missing=[c for c in want if c not in got],
                            unique_keys=(len(set(got)) == len(got)), same_set_and_order=(got == want))   # LHSREL-03 — 행 수 ≠ 고유 설계 보증
    fails = {r['case_id']: r['row_fail'] for r in rows if not r['row_ok']}
    col_ok = rep['columns']['header_equal']
    rep['by_ps'] = {r['ps_label']: dict(case_id=r['case_id'], physical_mode=r['physical_mode'], row_ok=r['row_ok'],
                                        webapp_columns=('측정됨' if r['gates']['webapp_done']['value'] == 'done'
                                                        else f"측정 안 됨 (배치 {r['gates']['webapp_done']['value']} — 빈칸 = N/A 아님)"),
                                        **r['values'], porosity_union_exact_se_pct=r['values_aux']['porosity_union_exact_se_pct'],
                                        tortuosity_SE_wall_status=r['values_aux']['tortuosity_SE_wall_status'], **r['eligibility'])
                    for r in rows}
    rep['deviations_static'] = list(DEVIATIONS_STATIC)
    rep['deviations_run'] = _run_deviations(man, rows, info)
    if info.get('webapp_fix'):
        wf = info['webapp_fix']
        rep['deviations_static'] = [FIX_STATIC_NOTE if x.startswith('웹앱 접촉 단계 — v1.1 코드') else x for x in rep['deviations_static']]
        for c, r in (wf.get('fix_cases') or {}).items():
            rep['deviations_run'].append(f"{c}: 웹앱 접촉 단계 = {wf['fix_commit'][:9]} 재실행 (LHS-28 관문 수정 · type_map_absent {r.get('type_map_absent')} · "
                                         f"d1ec42fba 와 다른 .py = {wf.get('code_diff_py')})")
    with open(os.path.join(args.out, 'ps45_row_flags.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['case_id', 'ps_label', 'physical_mode', 'row_ok', 'row_fail', 'wa_status', 'webapp_columns',
                    'perc_audit', 'physical_target_status', 'hold_reason_codes'])
        for r in rows:
            ws = r['gates']['webapp_done']['value']
            w.writerow([r['case_id'], r['ps_label'], r['physical_mode'], r['row_ok'], '|'.join(r['row_fail']), ws,
                        '측정됨' if ws == 'done' else '측정 안 됨 (빈칸 = N/A 아님 · 배치 ' + str(ws) + ')',
                        r['gates']['perc_audit_clean'].get('value'), r['eligibility']['physical_target_status'], r['eligibility']['hold_reason_codes']])
    keys_ok = rep['row_count']['unique_keys'] and rep['row_count']['same_set_and_order']
    rep['verdict'] = ('PASS' if (not fails and col_ok and not rep['row_count']['missing'] and keys_ok) else 'ROW_GATES_FAILED')
    rep['elapsed_s'] = round(time.time() - t0, 1)
    rep['log'] = log
    _write_json(os.path.join(args.out, 'ps45_summary.json'), rep)
    print(f"→ {prefix}.csv  {len(got)} 행 × {rep['columns']['n_cols']} 열 · v1.1 머리 동일 {col_ok} · 열 사전 행 차이 {len(rep['columns']['columns_tsv_rows_differ'])}")
    for r in rows:
        v = r['values']
        print(f"  {r['ps_label']:>5} {r['case_id']:<12} 웹앱 {r['gates']['webapp_done']['value']:<8} · union {v['porosity_union_exact_pct']} · "
              f"벽 간격 {v['thickness_wall_gap_um']} · SE–SE CN {v['se_se_cn']} · 퍼콜 {v['percolation_pct']} · τ_geo {v['tortuosity_SE_wall']} · "
              f"{r['eligibility']['physical_target_status']} · {'OK' if r['row_ok'] else '✗ ' + ','.join(r['row_fail'])}")
    print(f"판정 {rep['verdict']} → {os.path.join(args.out, 'ps45_summary.json')}")
    return 0 if rep['verdict'] == 'PASS' else 3


def _run_deviations(man, rows, info):
    out = []
    for item in [x for x in str((man or {}).get('deck_used') or '').split(';') if x]:
        case, _, how = item.partition('=')
        if how.startswith('upload') or ('무시' in how and '업로드 덱 0 개' not in how):
            out.append(f'{case}: 덱 = {how} — 리포 덱 (dem_scripts/ps_sweep_6mah_20260914) 과 바이트가 다를 수 있다')
    for r in rows:
        if r['gates']['webapp_done']['value'] != 'done':
            out.append(f"{r['case_id']}: 웹앱 접촉 단계 {r['gates']['webapp_done']['value']} — 웹앱 열 빈칸 ({r['gates']['webapp_done'].get('why')})")
    for k, v in ((man or {}).get('dirty_after') or {}).items():
        if v:
            out.append(f'{k} 워크트리 추적 파일이 실행 뒤 바뀌었다: {v[:5]}')
    return out


def _write_json(p, obj):
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1, default=str)
        fh.write('\n')


def _selftest(repo):
    ok = []

    def chk(name, cond, extra=''):
        ok.append(bool(cond))
        print(f"  {'✓' if cond else '✗'} {name}" + (f'   {extra}' if extra else ''))
    with tempfile.TemporaryDirectory() as td:
        #  tar 안전
        bad = os.path.join(td, 'bad.tar')
        with tarfile.open(bad, 'w') as tf:
            ti = tarfile.TarInfo('../evil.txt')
            ti.size = 1
            tf.addfile(ti, io.BytesIO(b'x'))
        try:
            with tarfile.open(bad) as tf:
                safe_extract(tf, os.path.join(td, 'x'))
            chk('① tar 의 ".." 경로 거부', False)
        except InputError:
            chk('① tar 의 ".." 경로 거부', True)
        bad2 = os.path.join(td, 'bad2.tar')
        with tarfile.open(bad2, 'w') as tf:
            ti = tarfile.TarInfo('a/link')
            ti.type = tarfile.SYMTYPE
            ti.linkname = '/etc/passwd'
            tf.addfile(ti)
        try:
            with tarfile.open(bad2) as tf:
                safe_extract(tf, os.path.join(td, 'y'))
            chk('② tar 의 심볼릭 링크 거부', False)
        except InputError:
            chk('② tar 의 심볼릭 링크 거부', True)
        chk('③ num() — 빈칸 None · 정수 · 실수 · 참/거짓', num('') is None and num('46') == 46 and num('2.5') == 2.5 and num('True') is True
            and num('OK') == 'OK')
        for coh in ('lhs130', 'lhsx64'):
            rep = replay(repo, coh, os.path.join(td, coh))
            chk(f'④ 건조 시험 {coh} — 배포 행 바이트 동일 · 머리 동일 · 열 사전 바이트 동일',
                rep.get('ok'), f"rows_byte_equal={rep.get('rows_byte_equal')} cols={(rep.get('columns') or {}).get('header_equal')} "
                               f"tsv={(rep.get('columns') or {}).get('columns_tsv_bytes_equal')} refusals={rep.get('refusals')}")
    print(f"post_ps45 selftest {sum(ok)}/{len(ok)} {'✓' if all(ok) else '✗'}")
    return 0 if all(ok) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='ps45 → LHS 배포 v1.1 같은 생성기 · 관문 · 배포 열 (로컬 후처리)')
    ap.add_argument('--repo', default=DEF_REPO, help='리포 (git archive 로 c981d77f0 파일을 꺼낸다 — 작업 트리는 읽지 않는다)')
    ap.add_argument('--tar', help='run_ps45_lhs_wsl.sh 산출 tar.gz')
    ap.add_argument('--sha256', help='WSL 이 찍은 tar sha256 (다르면 거부)')
    ap.add_argument('--dir', help='이미 풀린 산출 폴더')
    ap.add_argument('--design', default=os.path.join(HERE, 'ps45_design.csv'))
    ap.add_argument('--expect', default=os.path.join(HERE, 'ps45_expect.json'), help='같은-프레임 대조 기대값 ("" = 끔)')
    ap.add_argument('--out', default=os.path.join(HERE, 'post_out'))
    ap.add_argument('--replay', choices=sorted(REPLAY), help='건조 시험 — 커밋된 v1.1 원천의 일부 행')
    ap.add_argument('--cases', default='', help='--replay 행 (쉼표) · 비우면 기본 행')
    ap.add_argument('--force-inputs', action='store_true', help='입력 대조 실패를 무시하고 진행 (진단 전용 · 산출에 남는다)')
    ap.add_argument('--webapp-fix-tar', help='0:10 · 10:0 재실행 묶음 (LHS-28 관문 수정 커밋 · webapp_contact_fix/{status.json,metrics_flat.csv})')
    ap.add_argument('--webapp-fix-sha256', help='재실행 묶음 sha256 (WSL 이 찍은 값)')
    ap.add_argument('--webapp-fix-dir', help='이미 풀린 재실행 산출 폴더 (status.json · metrics_flat.csv)')
    ap.add_argument('--fix-commit', help='관문 수정 커밋 전체 sha — 재실행 runs 의 git_sha 와 같아야')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest(a.repo)
    try:
        if a.replay:
            rep = replay(a.repo, a.replay, a.out, [c for c in a.cases.split(',') if c] or None)
            _write_json(os.path.join(a.out, f'replay_{a.replay}_report.json'), rep)
            print(f"건조 시험 {a.replay} — 행 {rep.get('cases')} · 생성기 rc {rep.get('generator_rc')} · 배포 rc {rep.get('release_rc')} · "
                  f"행 바이트 동일 {rep.get('rows_byte_equal')} · 머리 동일 {(rep.get('columns') or {}).get('header_equal')} · "
                  f"열 사전 바이트 동일 {(rep.get('columns') or {}).get('columns_tsv_bytes_equal')} → {'✓' if rep.get('ok') else '✗'}")
            return 0 if rep.get('ok') else 3
        if not (a.tar or a.dir):
            ap.error('--tar 또는 --dir (또는 --replay · --selftest)')
        if a.expect == '':
            a.expect = None
        return post(a)
    except InputError as e:
        print('⛔', e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
