#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LHS ML 인계 배포 v1.3 (최종판) 생성기 — 시험 먼저 (1저자 10-07 *"v1.3 생성기를 Codex 판정과 동시에 미리 준비"*).

v1.3 = 세대 2 망 값 + #1 ML 표 (빈칸 뜻대로) · #2 f 타깃 · 관통 분류 안내 · #5 porosity–σ–CN 재적합 · τ 표시 이름 (수송 tortuosity) ·
새 열 se_isolated_pct (= 100 − top_reachable_pct).  실제 v1.3 자료는 Codex GO + 새 세대 2 194 배치 뒤에만 만든다 — 이 시험은
① 합성 입력 (세대 2 표기로 옮긴 합성 인계표 · 손 오라클) 과 ② 커밋된 v1.2 원천 (세대 1) 의 DRY RUN 으로 생성기 경로를 돈다.

  V0  API 가 있다
  V1  열 명세 — 주 표 = v1.2 주 표 열 + se_isolated_pct + 세대 2 표기 (Hertz) + 완료 압력 · Physics 부록 = v1.2 부록 + 세대 2 표기 · H12 는 주 표에 없다
  V2  빈칸 뜻 규칙 (닫힌 어휘) — mono 없는 상 · 접촉 0 평균 · 비관통 (N/A) · 비관통 T (∞) · 기술 실패 · HOLD · 빈 사유
  V3  빈칸 일관성 — 설명 안 되는 빈칸 · 빈칸이어야 할 칸의 값 · 상태 ↔ 값 모순을 거부 (양방향)
  V4  열 역할 (ML) — 모든 열이 닫힌 역할 표에 있다 · X = 자유 설계 노브 5 · 모르는 열 = 거부
  V5  ML 표 — 빈칸 코드 열 (두 데이터셋 합집합) · 되읽기 = 배포 값 그대로 · 데이터셋 표지 · 관통 분류 열
  V6  se_isolated_pct 항등식 (= 100 − top_reachable_pct · ≤ 100 − percolation_pct)
  V7  #5 재적합 — 합성 법칙 회복 · 고정 지수 (½ · 2) · 비관통 제외 · 결정적 · 입력 부족 거부
  V8  세대 관문 — g2 통과 · inferred_legacy 는 dry-run 만 · 섞임 · H12 를 주 자리에 = 거부
  V9  배치 manifest 관문 — 선언 없음 · inferred_legacy · g2 · 커밋된 v1.2 manifest = 거부
  V10 단계 A 명령 — 생성기 CLI 에 --tau-batch-manifest · --tau-results · se_isolation 묶음 · 압력 기록
  V11 τ 다시 읽기 배선 — load_tau_results(expected_generation='g2') 호출 · 칸 대조 · 거부 전파
  V12 실제 경로 (합성 세대 2 인계표) — 만들기 → check_v13 통과 · 변조 (ML 코드 · se_isolated · 재적합 · 파일) 검출
  V13 실제 경로 거부 — Codex 판정문 없음 · manifest 세대 · τ 다시 읽기 문제 → 산출 없음
  V14 DRY RUN (커밋된 v1.2 = 세대 1) — dry-run 없이 거부 · dry-run 이면 표지 (DRYRUN_ · "DRY RUN — not a release") · docs/data 아래 거부
  V15 CLI — --v13 --dry-run · --v13-check · dry-run 없는 세대 1 거부 (rc ≠ 0 · 폴더 안 만듦)
  V16 발사 봉인 대조 (세대 2 등록 20261007_g2 §3 · §5) — manifest code_hashes ↔ 지금 체크아웃 (다르면 거부 · --allow-seal-diff 명시 승인 · 기록) ·
      handover_code_hashes 다름 = 경고 · ⓪b 다시 읽기 기록 (reread.json) 실패 = 거부 · 단계 A 도 같은 관문 · CLI ·
      ★ 10-07 G2RR2-02 — 다시 읽기 기록이 등록 집합 production194 전부 (기대 = 읽음 · 같음) 가 아니면 거부 (V16n · V16o)
  V17 ★ 10-07 G2RR3-01 (Codex 세대 2 재검증 3 §3) — 배치 관문 증거 (⓪ 감사 seal_audit.json · ⓪b 다시 읽기 reread.json) = 실제 배포에 **필수** ·
      없음 · 깨짐 · 타입 결손 · 실패 판정 (감사 refused · invalid · UNSEALED · NO_RECORD · merged 다름 · 세대 · 입력 · import 문제 · SEALED_DIRTY_ALLOWED) ·
      다른 배치 뿌리 · 다른 봉인 지문 · manifest 바뀜 = 거부 (build_v13 · 단계 A) · 좋은 묶음의 배치 증거를 바꾸면 check_v13 이 같은 관문으로 다시 판정해 문제 ·
      진단 모드 (--diagnostic-batch-gate) = 옛 · 부분 기록도 만들되 NOT FOR RELEASE 표지 · 배포 대조 거부
  V18 ★ 10-07 G2RR4-01 (Codex 세대 2 재검증 4 §2) — 다시 읽기 상세 (meta · cases · checks) ↔ 요약: 상세 명시 실패를 n_fail 0 이 덮는 기록 · cases=[] · meta=[] ·
      빈 checks (공집합 PASS) · 검사 ID 결손 · 타입 · 중복 · 코호트 · 케이스 수 ≠ read_n · M3 ≠ 최상위 = 거부 / 감사 import 관측 내부 problems · outside 를 최상위 []
      가 덮는 기록 · 관측 객체 없음 · observe_imports false · 완료 시도가 등록 194 를 안 덮음 = 거부 (생산 194 = 관측 필수 · G2RR4-03) · build · check 둘 다
  V19 ★ 10-07 G2RR4-02 — 감사의 실행 단계 ↔ 영수증 결합 기록 (import_observation.stage_binding) 없음 · 스키마 · 시도 키 집합 ≠ 관측된 완료 시도 = 거부
  V20 ★ 10-08 G2RR5-01 (Codex 세대 2 재검증 5 §1) — 결합 기록의 **시도별 값** (생산자 계약 `run_network_194_parallel.stage_binding_record_problems`) ·
      합계 Σ observed ≤ n_finalized ≤ n_started ≤ n_processes: 값 null · parser 결손 · 0 · 계획 밖 · bool · n_finalized 0 · expected 자기모순 ·
      실제 audit CLI 실패 binding (최상위 요약 [] · 유지) = 거부 (build · check) / 정상 · 재시도 이력 (started > finalized) = 통과 (과잉차단 금지)

  python3 scripts/test_lhs_release_v13.py
"""
import collections
import contextlib
import csv
import io
import json
import math
import os
import random
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import lhs_release_build as LRB          # noqa: E402
import lhs_design_dataset as LDD         # noqa: E402
import tau_flux as TF                    # noqa: E402
import run_network_194_parallel as NP194  # noqa: E402  (발사 봉인 지문 code_fp · 등록 집합 · 감사 기록 스키마 — 실행기 정본 · 손 사본 금지)
import g2_network_reread as G2RR         # noqa: E402  (다시 읽기 기록 스키마 — 정본)

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({str(why)[:300]})' if why else ''))
    return cond


def safe(fn, default=None):
    """시험 대상이 없거나 (옛 코드) 예외면 ('ERR', 사유) — 한 시험의 실패가 나머지를 막지 않게."""
    try:
        return fn()
    except (Exception, SystemExit) as e:                                  # noqa: BLE001 — 옛 CLI 는 모르는 인자에 SystemExit
        return ('ERR', f'{type(e).__name__}: {e}') if default is None else default


def is_err(x):
    return isinstance(x, tuple) and len(x) == 2 and x[0] == 'ERR'


def refused(fn, tag=''):
    """fn() 이 ReleaseError (또는 FillRefusal) 로 거부하고 메시지에 tag 가 있으면 True."""
    try:
        fn()
    except Exception as e:                                                # noqa: BLE001
        bad = getattr(LRB, 'ReleaseError', RuntimeError)
        return isinstance(e, (bad, LDD.FillRefusal)) and tag in str(e)
    return False


V12 = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006')
BATCH12 = os.path.join(ROOT, 'docs', 'data', 'lhs_network194_11fcf91e8')
REL12 = os.path.join(ROOT, 'docs', 'data', 'lhs_release_20261006_v12')
DATE = '20991231'

#: 세대 2 역할 표기 오라클 (손 칸 — 도우미 상수를 베끼지 않는다 · lhs_release_build selftest ⑳ 와 같은 값)
G2H = {'constriction': 'maxwell_halfspace', 'psi': '', 'area_rule': 'hertz_ccpl22', 'electrode': 'dirichlet_exact', 'bulk': 'cylinder_half_d',
       'area_mode': 'hertz'}
G2P = {'constriction': 'mikic_psi_multiply', 'psi': 'multiply', 'area_rule': 'physics_g2', 'electrode': 'dirichlet_exact',
       'bulk': 'cylinder_half_d', 'area_mode': 'physics'}
G2H12 = {'constriction': 'mikic_psi_multiply', 'psi': 'multiply', 'area_rule': 'hertz_ccpl22', 'electrode': 'dirichlet_exact',
         'bulk': 'sphere_segment', 'area_mode': 'hertz'}
PRESS = {'press_target_mpa': '300.0', 'press_last_loop_mpa': '300.41', 'press_reached': 'True', 'press_log_sha256': 'a' * 64}


def _read_csv(p):
    with open(p, encoding='utf-8', newline='') as f:
        r = csv.reader(f)
        h = next(r)
        return h, [dict(zip(h, row)) for row in r]


def _write_csv(p, head, rows):
    with open(p, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(head)
        for r in rows:
            w.writerow([r.get(c, '') for c in head])


def make_g2_handover_dir(td, mutate=None):
    """합성 세대 2 인계표 묶음 (테스트 전용) — 커밋된 v1.2 인계표 행 (실값) 을 지금 생성기 스키마로 옮긴다:
    τ 열 = tau_flux.column_names() (세 모드) · 표기 = 세대 2 오라클 · H12 = Hertz 값 복사 · se_isolated_pct = 100 − top_reachable_pct ·
    press_* = 합성 기록 · 열 사전 = 지금 생성기 column_dictionary (웹앱 판정 = 커밋된 194 배치) · τ 출처 부록 = 지금 검사 목록.
    ⚠ 숫자는 세대 1 값 그대로다 — 경로 · 관문 시험이지 세대 2 값이 아니다."""
    os.makedirs(td, exist_ok=True)
    tcols = TF.column_names()
    for ds in ('lhs', 'lhsx'):
        head, rows = _read_csv(os.path.join(V12, f'{ds}_handover_v12_20261006.csv'))
        base = [c for c in head if LDD.tau_net_define(c) is None]
        i = base.index('am_ionic_isolated_pct') + 1
        new_head = base[:i] + ['se_isolated_pct'] + base[i:] + tcols + list(PRESS)
        out = []
        for r in rows:
            o = {c: r.get(c, '') for c in base}
            o['se_isolated_pct'] = repr(100.0 - float(r['top_reachable_pct']))
            for m, src, lab in (('hertz', 'hertz', G2H), ('physics', 'physics', G2P), ('hertz_h12', 'hertz', G2H12)):
                for b in ('f_ion_{}', 'f_ion_{}_gap', 'tau2_ion_{}', 'tau_ion_{}', 'ion_net_status_{}', 'ion_net_status_reason_{}',
                          'ion_net_band_rule_{}', 'ion_net_band_frac_{}', 'ion_net_basis_check_{}'):
                    o[b.format(m)] = r.get(b.format(src), '')
                for k, v in lab.items():
                    o[f'ion_net_{k}_{m}'] = v
            for c in ('ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis'):
                o[c] = r.get(c, '')
            o['ion_net_generation'] = 'g2'
            o.update(PRESS)
            out.append(o)
        if mutate:
            mutate(ds, new_head, out)
        stem = os.path.join(td, f'{ds}_handover_v13_{DATE}')
        _write_csv(stem + '.csv', new_head, out)
        wv = LDD.load_webapp(os.path.join(BATCH12, 'merged', ds))
        with open(stem + '_columns.tsv', 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, ['column', 'source', 'verdict', 'meaning', 'caveat'], delimiter='\t', lineterminator='\n')
            w.writeheader()
            for d in LDD.column_dictionary(new_head, webapp=wv, design_source='(합성)'):
                w.writerow(d)
        with open(os.path.join(V12, f'{ds}_handover_v12_20261006_tau_provenance.tsv'), encoding='utf-8', newline='') as f:
            prov = list(csv.DictReader(f, delimiter='\t'))
        with open(stem + '_tau_provenance.tsv', 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, LDD.TAU_PROVENANCE_COLS, delimiter='\t', lineterminator='\n')
            w.writeheader()
            for p in prov:
                w.writerow(dict(p, same_generation_checks=';'.join(LDD.TAU_SAME_GEN_CHECKS)))
    return td


#: 합성 발사 봉인 (실행기 manifest code_hashes 의 부분집합 · 지금 파일 지문) · 인계 단계 지문 (handover_code_hashes) — 손 목록 (실행기 상수를 베끼지 않는다)
SEAL_FILES = ('scripts/tau_flux.py', 'scripts/network_conductivity.py', 'webapp/pipeline_service.py', 'webapp/app.py')
HANDOVER_FILES = ('scripts/lhs_design_dataset.py', 'scripts/g2_network_reread.py')


def _sha_file(rel):
    return _sha_path(os.path.join(ROOT, rel))


def _sha_path(p):
    return __import__('hashlib').sha256(open(p, 'rb').read()).hexdigest()


#  ⓪b 다시 읽기 기록 (g2_network_reread --launcher-root … --expect-set production194 --json) 의 통과 모양 — 10-07 G2RR2-02 부터 등록 집합 필드 필수 ·
#  ★ 10-07 G2RR3-01 부터 실행 신원 (launcher_root · manifest_sha256 · seal_fp · launch_sha — `rr_bound` 가 배치 뿌리마다 채운다) 필수 · 스키마 = 도구 정본
RR_OK = {'schema': G2RR.SCHEMA, 'expected_generation': 'g2', 'n_fail': 0, 'expected_set': 'production194', 'expected_source': 'registered',
         'expected_n': 194, 'read_n': 194, 'set_equal': True, 'missing': [], 'extra': []}
#: make_batch_root 의 기본 = 이 배치 뿌리 · 이 manifest · 이 발사 봉인 지문에 결합된 통과 기록 (⓪ 감사 · ⓪b 다시 읽기)
GOOD = object()
LAUNCH_SHA = 'ab' * 20
#: 합성 감사 기록의 행 = 등록 집합 production194 (실행기가 커밋된 수확 폴더에서 열거 · 등록 ID 지문과 같아야 한다)
PROD194 = sorted(NP194.registered_id_set('production194')['pairs'], key=lambda x: (x[1], x[0]))


def _man_of(td):
    return json.load(open(os.path.join(td, 'manifest.json'), encoding='utf-8'))


#: ★ 10-07 G2RR4-01 (Codex 세대 2 재검증 4 §2 최소 해결 4 — "상세 없는 옛 정상 픽스처를 계속 정상으로 두면 수정이 약해진다") — 통과 기록 = **상세 꼴 그대로**:
#:   meta = 생산자 `g2_network_reread.run_launcher` 가 내는 열 항목 (M0 · M-plan · M-reg · 코호트마다 M1 · M2 · H1 · M3) · cases = 등록 194 케이스마다
#:   K1–K7 (`reread_case`).  이름 = 생산자 문구의 손 사본 (도구 상수를 베끼지 않는다 — 계약의 ID 는 첫 낱말).  옛 요약 · 신원만인 통과 모양은 이제 정상이 아니다.
RR_CASE_CHECK_NAMES = (
    'K1 게시 — solver success · 도장 valid/success · run id (도장 = full_metrics = active)',
    "K2 세대 계약 + 증서 결합 — 세대 'g2' · 문제 0 (모드 셋 × 가지 셋 증서 · G2R-01 · 02 · G2RR-02)",
    'K3 도장 ↔ 레코드 — 네 세대 값 = 레코드에서 유도한 기대값 (G2RR-01)',
    'K4 망 정지 계약 다시 (①–⑨ · legacy_ok False)',
    "K5 열 역할 — ion_net_generation 'g2' · 행 세대 계약 문제 0 (모드별 협착 · ψ · 면적 · 전극 · bulk 칸)",
    'K6 관통 일치 — 생산자 FULL 상태 ↔ τ 상태 (세 모드)',
    'K7 가지 표 — 공용 계약 (tau_flux.branch_table_problems) 그대로: 숫자 ⇔ 게시 상태 / 숫자 없음 ⇒ 비게시 상태 + 사유 / 상태 기록 결손 = 거부')


def rr_detail(pairs=None, expected_set='production194'):
    """다시 읽기 상세 (meta · cases) — 생산자 꼴 (모두 ok True · 등록 집합 pairs (기본 PROD194) · 코호트 순서 lhs → lhsx)."""
    pairs = sorted(pairs if pairs is not None else PROD194, key=lambda x: (x[1], x[0]))
    cohorts = [h for h in ('lhs', 'lhsx') if any(h == hh for _c, hh in pairs)]
    meta = [dict(name='M0 manifest 기대 세대 선언 (expected_network_generation)', ok=True, detail='g2'),
            dict(name='M-plan manifest plan · cohorts · queue 꼴 (비지 않음 · 중복 · 코호트 소속 — 루프 전)', ok=True, detail=''),
            dict(name=f'M-reg 계획 큐 = 등록 집합 {expected_set} ({len(pairs)})', ok=True, detail='등록에만 [] · 계획에만 [] · 등록 밖 코호트 []')]
    cases = []
    for h in cohorts:
        cl = [c for c, hh in pairs if hh == h]
        meta.append(dict(name=f'M1 {h} 케이스 집합 — 계획 큐 = 배치 기록 ({len(cl)})', ok=True, detail='계획에만 [] · 기록에만 []'))
        meta.append(dict(name=f'M2 {h} 전 케이스 done · partial', ok=True, detail={}))
        cases += [dict(case=c, folder=f'/x/merged/{h}/results/{c}', run_id=f'RUN-{c}', generation='g2', cohort=h, batch='launcher',
                       checks=[dict(name=n, ok=True, detail='') for n in RR_CASE_CHECK_NAMES]) for c in cl]
        meta.append(dict(name=f"H1 {h} 인계 출처 관문 (load_tau_results · P0–P4 · manifest 기대 세대 'g2') · 칸 = case_row", ok=True,
                         detail=f'{len(cl)} 케이스 · 기대 세대 g2 · 칸 다름 []'))
    meta.append(dict(name=f'M3 읽은 고유 (케이스, 코호트) = 등록 집합 {expected_set} — 기대 {len(pairs)} · 읽음 {len(pairs)}', ok=True,
                     detail='빠진 [] · 남는 []', expected_n=len(pairs), read_n=len(pairs), set_equal=True, missing=[], extra=[]))
    return meta, cases


def rr_bound(td):
    """⓪b 다시 읽기 통과 기록 — 이 배치 뿌리 (realpath) · manifest sha256 · 발사 봉인 지문 · 발사 sha 에 결합 (도구 v3 의 실행 신원 필드) ·
    ★ G2RR4-01 상세 (meta · cases — 생산자 꼴)."""
    man = _man_of(td)
    meta, cases = rr_detail()
    return dict(RR_OK, meta=meta, cases=cases, launcher_root=os.path.realpath(td), manifest_sha256=_sha_path(os.path.join(td, 'manifest.json')),
                seal_fp=(man.get('seal') or {}).get('code_fp'), launch_sha=(man.get('git') or {}).get('sha'))


def obs_bound(pairs=None):
    """★ G2RR4-01 ③ — 감사 기록의 import 관측 객체 (`run_network_194_parallel.import_observation` + `import_observation_problems` 가 채우는 키) 의 통과 꼴:
    등록 케이스마다 완료 시도 (run 1 · 시도 1) · 케이스당 다섯 프로세스 (워커 · 파서 · 접촉 분석 · 피복 · 망 솔버) · 문제 0 · 봉인 밖 0."""
    pairs = pairs if pairs is not None else PROD194
    #  ★ G2RR4-02 — 완료 시도마다 실행 단계 ↔ 영수증 결합 기록 (실행기 audit 의 import_observation.stage_binding · 스키마 = 실행기 정본 상수 (옛 실행기면 손 값) ·
    #    열쇠 꼴 '케이스|run|시도')
    #  ★ 10-08 G2RR5-01 — 시도 값 = 생산자 계약 그대로 (배포 관문이 시도마다 읽는다): plan_source = 실행기가 쓰는 출처 문자열 **전체** 의 손 사본
    #    (옛 픽스처의 'worker.json attempts[].stage_plan' 은 그 앞부분만 — 실행기가 쓰지 않는 값)
    sb = dict(schema=getattr(NP194, 'IMPORT_OBS_STAGE_SCHEMA', 'np194_import_obs/stage_binding/v1'),
              attempts={f'{c}|1|1': dict(plan_source='worker.json attempts[].stage_plan (그 시도가 쓴 케이스 기록의 단계)', mode='bimodal',
                                         executed=['parser', 'contact_bimodal', 'coverage', 'network_cli'], skipped=[], in_process=4,
                                         expected={'worker': 1, 'scripts/parse_liggghts.py': 1, 'scripts/analyze_contacts_bimodal.py': 1,
                                                   'scripts/coverage_physics_vs_hertzian.py': 1, 'scripts/network_conductivity.py': 1},
                                         observed={'worker': 1, 'scripts/parse_liggghts.py': 1, 'scripts/analyze_contacts_bimodal.py': 1,
                                                   'scripts/coverage_physics_vs_hertzian.py': 1, 'scripts/network_conductivity.py': 1})
                        for c, _h in sorted(pairs)})
    return dict(n_processes=5 * len(pairs), n_started=5 * len(pairs), n_finalized=5 * len(pairs), processes=[], problems=[], tmp_leftover=[], files=[],
                observed=[], outside=[], completed_attempts=[[c, '1', '1'] for c, _h in sorted(pairs)], unfinalized_noncompleted=[], stage_binding=sb)


def audit_bound(td):
    """⓪ 봉인 감사 통과 기록 (`run_network_194_parallel.py audit --json` 의 키 그대로) — 이 배치 뿌리 · 봉인 지문 · 발사 sha · 등록 194 ID 가 전부
    SEALED · merged same · 레코드 세대 g2 · 실행 형식 자격 current · 문제 목록 전부 빈 목록 · ★ G2RR4-01 import 관측 객체 (생산 194 = 관측 필수 · G2RR4-03)."""
    man = _man_of(td)
    rows = [dict(case=c, cohort=h, record_status='done', n_attempts=1, attempt=1, run=1, form='attempt_seal', verdict='SEALED',
                 why='시작 · 끝 지문 = 발사 봉인 · git sha = 발사 · dirty 아님', record_sha='0' * 64, generation='g2', merged='same') for c, h in PROD194]
    return dict(schema=NP194.LAUNCH_SEAL_SCHEMA + '#audit', root=os.path.realpath(td), audited_at='2099-12-31T00:00:00',
                launch_sha=(man.get('git') or {}).get('sha'), seal_fp=(man.get('seal') or {}).get('code_fp'), code_root=ROOT, code_root_changed_now=[],
                verdicts={'SEALED': len(rows)}, merged={'same': len(rows)}, cases=rows, expected_network_generation='g2', generation_declared=True,
                generation_problems=[], input_problems=[], eligibility=dict(kind='current', historical=None, problems=[], note=''),
                import_observation=obs_bound(), import_observation_problems=[])


def _write_gate(td, name, spec, good):
    """배치 관문 기록 하나 — None = 없음 · GOOD = 결합된 통과 기록 · 호출 가능 = 통과 기록을 받아 바꾼 것 (반환 None 이면 그 자리 수정) ·
    bytes = 그 바이트 그대로 (깨진 JSON · null) · 그 밖 = 그 값 그대로 (정적 dict)."""
    p = os.path.join(td, name)
    if spec is None:
        return
    if isinstance(spec, bytes):
        open(p, 'wb').write(spec)
        return
    if spec is GOOD:
        rec = good(td)
    elif callable(spec):
        rec = good(td)
        rec = spec(rec) or rec
    else:
        rec = spec
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(rec, f)


def make_batch_root(td, gen='g2', code=True, handover=True, alter=None, reread=GOOD, audit=GOOD, man_edit=None):
    """합성 배치 뿌리 — manifest (기대 세대 선언 · 코호트 원천 · 발사 봉인 code_hashes + seal.code_fp · git sha · handover_code_hashes) +
    ⓪ 감사 (seal_audit.json) · ⓪b 다시 읽기 (reread.json) 기록 (τ 다시 읽기는 시험에서 대역).
    code / handover = 지금 체크아웃의 파일 지문 (같다) · alter = {파일: 가짜 지문} (발사 뒤 바뀐 파일 흉내 · 봉인 지문은 바뀐 지도로) ·
    man_edit = 기록을 쓰기 전 manifest 수정 · reread / audit = `_write_gate` 의 spec (기본 GOOD — 이 배치 뿌리에 결합된 통과 기록)."""
    os.makedirs(td, exist_ok=True)
    man = {'schema': 'network_parallel_launcher/v1', 'stop_after': 'network',
           'plan': {'cohorts': [
               {'name': 'lhs', 'harvest_dir': '/x/docs/data/lhs_descriptors_cov_1e09f661d', 'union': 'docs/data/lhs_union_20260927/lhs130_union.tsv',
                'design': ''},
               {'name': 'lhsx', 'harvest_dir': '/x/docs/data/lhsx_descriptors_cov_1e09f661d',
                'union': 'docs/data/lhs_union_20260927/lhsx64_union.tsv', 'design': 'docs/data/lhsx_design_adapted_20260929.csv'}]}}
    if gen is not None:
        man['expected_network_generation'] = gen
    if code:
        man['code_hashes'] = {rel: _sha_file(rel) for rel in SEAL_FILES}
    if handover:
        man['handover_code_hashes'] = {rel: _sha_file(rel) for rel in HANDOVER_FILES}
    for rel, h in (alter or {}).items():
        man['handover_code_hashes' if rel in HANDOVER_FILES else 'code_hashes'][rel] = h
    if code:                                    # 발사 봉인 지문 = code_hashes 의 지문 (실행기 manifest.seal.code_fp · alter 뒤의 지도)
        man['seal'] = {'schema': NP194.LAUNCH_SEAL_SCHEMA, 'code_fp': NP194.code_fp(man['code_hashes'])}
    man['git'] = {'sha': LAUNCH_SHA}
    #  ★ G2RR4-03 — 생산 194 = import 관측을 켠 실행 (실행기 manifest observe_imports · 관측 실행 신원)
    man['observe_imports'] = True
    man['import_obs_run_id'] = 'cd' * 16
    if man_edit:
        man_edit(man)
    with open(os.path.join(td, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(man, f)
    _write_gate(td, 'reread.json', reread, rr_bound)
    _write_gate(td, 'seal_audit.json', audit, audit_bound)
    return td


# ═══ V0 ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V0  API')
API = ('v13_columns', 'v13_blank_reason', 'v13_blank_problems', 'v13_role', 'v13_ml_table', 'v13_ml_decode', 'v13_se_isolated_problems',
       'refit_porosity_sigma_cn', 'refit_from_csv', 'v13_generation_problems', 'v13_manifest_generation', 'v13_handover_argv',
       'v13_reread_tau', 'build_v13', 'check_v13', 'V13_BLANK_CODES', 'v13_seal_drift', 'v13_batch_gate_files')
miss = [a for a in API if not hasattr(LRB, a)]
chk('V0 v1.3 API 가 lhs_release_build 에 있다', not miss, miss)

# ═══ V1 열 명세 ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V1  열 명세')
m_l = safe(lambda: LRB.v13_columns('lhs', 'main'))
m_x = safe(lambda: LRB.v13_columns('lhsx', 'main'))
ph_l = safe(lambda: LRB.v13_columns('lhs', 'physics'))
b12 = [r[0] for r in csv.reader(open(os.path.join(REL12, 'lhs_release_20261006_v12_columns.tsv'), encoding='utf-8'), delimiter='\t')][1:]
b12x = [r[0] for r in csv.reader(open(os.path.join(REL12, 'lhsx_release_20261006_v12_columns.tsv'), encoding='utf-8'), delimiter='\t')][1:]
p12 = [r[0] for r in csv.reader(open(os.path.join(REL12, 'lhs_release_20261006_v12_physics_columns.tsv'), encoding='utf-8'), delimiter='\t')][1:]
ADD = ['se_isolated_pct', 'ion_net_generation', 'ion_net_constriction_hertz', 'ion_net_area_rule_hertz', 'ion_net_electrode_hertz',
       'ion_net_bulk_hertz', 'press_target_mpa', 'press_last_loop_mpa', 'press_reached']
chk('V1a 주 표 (130) = v1.2 주 표 열 (순서 그대로) + se_isolated_pct · 세대 2 표기 (Hertz) · 완료 압력 (끝에)',
    isinstance(m_l, list) and m_l == b12 + ADD, m_l if not isinstance(m_l, list) else [c for c in m_l if c not in b12])
chk('V1b 주 표 (64) = v1.2 주 표 열 + 같은 추가 · H12 · physics 열 없음',
    isinstance(m_x, list) and m_x == b12x + ADD and not any('h12' in c or c.endswith('_physics') for c in m_x), m_x)
chk('V1c Physics 부록 = v1.2 부록 열 + 세대 칸 · Physics 표기 다섯 (협착 · ψ · 면적 규칙 · 전극 · bulk)',
    isinstance(ph_l, list) and ph_l == p12 + ['ion_net_generation', 'ion_net_constriction_physics', 'ion_net_psi_physics',
                                              'ion_net_area_rule_physics', 'ion_net_electrode_physics', 'ion_net_bulk_physics'], ph_l)
chk('V1d 완료 압력 미검사 (--pressure-unverified) 명세는 press_* 를 빼고 나머지 같다',
    safe(lambda: LRB.v13_columns('lhs', 'main', press=False)) == b12 + ADD[:6])

# ═══ V2 빈칸 뜻 규칙 ══════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V2  빈칸 뜻 규칙')
BASE = {'block': 'bimodal', 'percolation_pct': '40.0', 'ion_net_status_hertz': 'OK', 'physical_target_status': 'OK',
        'area_AM_P_AM_P_n': '5', 'am_am_n_contacts': '20', 'ion_net_status_physics': 'OK'}


def br(col, **kv):
    return safe(lambda: LRB.v13_blank_reason(dict(BASE, **kv), col))


cases2 = [
    ('mono_AM_S 의 d_am_p_um', br('d_am_p_um', block='mono_AM_S'), 'NA_PHASE_ABSENT'),
    ('mono_AM_P 의 AM_S_ionic_dead_pct', br('AM_S_ionic_dead_pct', block='mono_AM_P'), 'NA_PHASE_ABSENT'),
    ('mono 의 size_ratio_P_over_S', br('size_ratio_P_over_S', block='mono_AM_P'), 'NA_PHASE_ABSENT'),
    ('mono 의 area_AM_P_AM_S_total', br('area_AM_P_AM_S_total', block='mono_AM_S'), 'NA_PHASE_ABSENT'),
    ('bimodal 의 d_am_p_um = 값', br('d_am_p_um'), None),
    ('AM_P–AM_P 접촉 0 의 평균', br('area_AM_P_AM_P_mean', area_AM_P_AM_P_n='0'), 'NA_ZERO_CONTACTS'),
    ('AM_P–AM_P 접촉 0 의 총합 = 측정된 0 (값)', br('area_AM_P_AM_P_total', area_AM_P_AM_P_n='0'), None),
    ('AM–AM 접촉 0 의 파괴 지수', br('fracture_index_force', am_am_n_contacts='0'), 'NA_ZERO_CONTACTS'),
    ('AM–AM 접촉 0 의 am_am_mean_area', br('am_am_mean_area', am_am_n_contacts='0'), 'NA_ZERO_CONTACTS'),
    ('비관통 se_se_cn_perc', br('se_se_cn_perc', percolation_pct='0.0'), 'NA_NOT_PERCOLATING'),
    ('비관통 기하 τ (tortuosity_SE_wall)', br('tortuosity_SE_wall', percolation_pct='0.0'), 'NA_NOT_PERCOLATING'),
    ('비관통 tau2_ion_hertz = ∞', br('tau2_ion_hertz', ion_net_status_hertz='NOT_PERCOLATING'), 'INF_NOT_PERCOLATING'),
    ('비관통 tau_ion_hertz = ∞', br('tau_ion_hertz', ion_net_status_hertz='NOT_PERCOLATING'), 'INF_NOT_PERCOLATING'),
    ('비관통 f_ion_hertz = 값 (0.0)', br('f_ion_hertz', ion_net_status_hertz='NOT_PERCOLATING'), None),
    ('NOT_COMPUTED 의 f', br('f_ion_hertz', ion_net_status_hertz='NOT_COMPUTED'), 'NOT_COMPUTED'),
    ('BAND_FALLBACK 의 tau2', br('tau2_ion_hertz', ion_net_status_hertz='BAND_FALLBACK'), 'HOLD_BAND_FALLBACK'),
    ('MBCB 의 tau2 = 값', br('tau2_ion_physics', ion_net_status_physics='MODEL_BELOW_CONTINUUM_BOUND'), None),
    ('OK 행 hold_reason_codes 빈칸 = 사유 없음', br('hold_reason_codes'), 'EMPTY_NO_REASON'),
    ('HOLD 행 hold_reason_codes = 값', br('hold_reason_codes', physical_target_status='HOLD'), None),
    ('상태 OK 의 사유 칸 빈칸 = 사유 없음', br('ion_net_status_reason_hertz'), 'EMPTY_NO_REASON'),
    ('NOT_COMPUTED 의 사유 칸 = 값', br('ion_net_status_reason_hertz', ion_net_status_hertz='NOT_COMPUTED'), None),
]
bad2 = [(n, got, want) for n, got, want in cases2 if got != want]
chk(f'V2 빈칸 뜻 {len(cases2)} 경우 (닫힌 어휘 · 값이어야 할 칸 = None)', not bad2, bad2[:4])
codes = safe(lambda: set(LRB.V13_BLANK_CODES), set())
chk('V2b 어휘 = NA_PHASE_ABSENT · NA_ZERO_CONTACTS · NA_NOT_PERCOLATING · INF_NOT_PERCOLATING · NOT_COMPUTED · HOLD_BAND_FALLBACK · EMPTY_NO_REASON',
    codes == {'NA_PHASE_ABSENT', 'NA_ZERO_CONTACTS', 'NA_NOT_PERCOLATING', 'INF_NOT_PERCOLATING', 'NOT_COMPUTED', 'HOLD_BAND_FALLBACK',
              'EMPTY_NO_REASON'}, codes)

# ═══ V3 빈칸 일관성 (양방향) ══════════════════════════════════════════════════════════════════════════════════════════════════════
print('V3  빈칸 일관성')
COLS3 = ['case_id', 'block', 'd_am_p_um', 'coverage_AM_P_hertz_pct', 'percolation_pct', 'f_ion_hertz', 'tau2_ion_hertz', 'ion_net_status_hertz',
         'ion_net_status_reason_hertz', 'physical_target_status', 'hold_reason_codes']
OK3 = [{'case_id': 'a', 'block': 'bimodal', 'd_am_p_um': '9.0', 'coverage_AM_P_hertz_pct': '40.0', 'percolation_pct': '80.0', 'f_ion_hertz': '0.05',
        'tau2_ion_hertz': '5.0', 'ion_net_status_hertz': 'OK', 'ion_net_status_reason_hertz': '', 'physical_target_status': 'OK',
        'hold_reason_codes': ''},
       {'case_id': 'b', 'block': 'mono_AM_S', 'd_am_p_um': '', 'coverage_AM_P_hertz_pct': '', 'percolation_pct': '0.0', 'f_ion_hertz': '0.0',
        'tau2_ion_hertz': '', 'ion_net_status_hertz': 'NOT_PERCOLATING', 'ion_net_status_reason_hertz': '', 'physical_target_status': 'HOLD',
        'hold_reason_codes': 'NEGATIVE_POROSITY'}]
chk('V3a 맞는 표 → 문제 0', safe(lambda: LRB.v13_blank_problems(OK3, COLS3)) == [])


def p3(i, **kv):
    rows = [dict(r) for r in OK3]
    rows[i].update(kv)
    return safe(lambda: LRB.v13_blank_problems(rows, COLS3))


neg3 = [('설명 안 되는 빈칸 (bimodal coverage_AM_P 빈칸)', p3(0, coverage_AM_P_hertz_pct=''), 'a'),
        ('빈칸이어야 할 칸의 값 (mono_AM_S 의 d_am_p_um)', p3(1, d_am_p_um='3.0'), 'b'),
        ('NOT_PERCOLATING 인데 tau2 값', p3(1, tau2_ion_hertz='9.9'), 'b'),
        ('OK 인데 tau2 빈칸', p3(0, tau2_ion_hertz=''), 'a'),
        ('NOT_PERCOLATING 인데 f 빈칸 (0.0 이어야)', p3(1, f_ion_hertz=''), 'b'),
        ('NOT_PERCOLATING 인데 f ≠ 0', p3(1, f_ion_hertz='0.01'), 'b'),
        ('HOLD 인데 사유 빈칸', p3(1, hold_reason_codes=''), 'b')]
bad3 = [n for n, got, case in neg3 if not (isinstance(got, list) and got and any(case in p for p in got))]
chk(f'V3b 반례 {len(neg3)} — 전부 문제로 보고 (그 행 이름과 함께)', not bad3, bad3)

# ═══ V4 열 역할 ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V4  열 역할')
roles = safe(lambda: {c: LRB.v13_role(c) for c in (m_l if isinstance(m_l, list) else [])}, {})
chk('V4a 주 표 열 전부 역할이 있다 (닫힌 표)', bool(roles) and len(roles) == len(m_l if isinstance(m_l, list) else []) and all(roles.values()))
chk('V4b X = 자유 설계 노브 5 개 · f_ion_hertz = 주 타깃 · tau2 · tau = 항등식 유도 (타깃 금지) · 상태 열 · 적격성 · 상수',
    sorted(c for c, r in roles.items() if r == 'X') == sorted(['am_pct', 'ps_frac', 'd_am_p_um', 'd_am_s_um', 'd_se_um'])
    and roles.get('f_ion_hertz') == 'Y_TARGET' and roles.get('tau2_ion_hertz') == 'Y_IDENTITY' and roles.get('tau_ion_hertz') == 'Y_IDENTITY'
    and roles.get('ion_net_status_hertz') == 'STATUS' and roles.get('physical_target_status') == 'FLAG' and roles.get('pressure_MPa') == 'CONST'
    and roles.get('n_SE_measured') == 'RESULT_COUNT' and roles.get('se_isolated_pct') == 'Y', {c: roles.get(c) for c in ('f_ion_hertz', 'tau2_ion_hertz')})
chk('V4c 모르는 열 = 거부 (기본 역할로 흘리지 않는다)', refused(lambda: LRB.v13_role('zz_new_col'), 'zz_new_col'))

# ═══ V5 ML 표 ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V5  ML 표')
COLS5 = ['case_id', 'block', 'am_pct', 'd_am_p_um', 'percolation_pct', 'top_reachable_pct', 'f_ion_hertz', 'tau2_ion_hertz', 'ion_net_status_hertz',
         'ion_net_status_reason_hertz', 'physical_target_status', 'hold_reason_codes']
R5 = {'lhs': [dict(OK3[0], am_pct='80.0', top_reachable_pct='90.0'), dict(OK3[1], am_pct='70.0', top_reachable_pct='20.0')],
      'lhsx': [dict(OK3[0], case_id='x1', am_pct='50.0', top_reachable_pct='99.0', physical_target_status='HOLD', hold_reason_codes='NEGATIVE_POROSITY')]}
ml = safe(lambda: LRB.v13_ml_table({ds: (COLS5, rows) for ds, rows in R5.items()}))
ok5 = isinstance(ml, tuple) and len(ml) == 2 and isinstance(ml[0], dict)
mlt, mld = (ml if ok5 else ({}, []))
mcols = (mlt.get('lhs') or ([], []))[0] if ok5 else []
chk('V5a 열 = case_id · dataset · 배포 열 (빈칸이 있는 열 뒤에 <열>__blank) · 끝에 ion_percolates_hertz · 두 데이터셋 같은 열',
    ok5 and mcols[:2] == ['case_id', 'dataset'] and 'd_am_p_um__blank' in mcols and mcols.index('d_am_p_um__blank') == mcols.index('d_am_p_um') + 1
    and 'tau2_ion_hertz__blank' in mcols and 'am_pct__blank' not in mcols and mcols[-1] == 'ion_percolates_hertz'
    and (mlt.get('lhsx') or ([], []))[0] == mcols, mcols)
rows5 = (mlt.get('lhs') or ([], []))[1] if ok5 else []
b5 = next((r for r in rows5 if r.get('case_id') == 'b'), {})
a5 = next((r for r in rows5 if r.get('case_id') == 'a'), {})
chk('V5b 코드 — mono 없는 상 = NA_PHASE_ABSENT · 비관통 T = INF_NOT_PERCOLATING · f = 0.0 (코드 없음) · OK 행 사유 = EMPTY_NO_REASON · 관통 분류 1/0',
    b5.get('d_am_p_um') == '' and b5.get('d_am_p_um__blank') == 'NA_PHASE_ABSENT' and b5.get('tau2_ion_hertz__blank') == 'INF_NOT_PERCOLATING'
    and b5.get('f_ion_hertz') == '0.0' and 'f_ion_hertz__blank' not in mcols and a5.get('hold_reason_codes__blank') == 'EMPTY_NO_REASON'
    and a5.get('tau2_ion_hertz__blank') == '' and a5.get('ion_percolates_hertz') == '1' and b5.get('ion_percolates_hertz') == '0'
    and b5.get('dataset') == 'lhs', (a5, b5))
dec = safe(lambda: LRB.v13_ml_decode(mcols, rows5))
chk('V5c 되읽기 — ML 표에서 코드 · 표지 · 분류 열을 빼면 배포 열 · 값이 그대로', isinstance(dec, tuple) and dec[0] == COLS5
    and [[r[c] for c in COLS5] for r in dec[1]] == [[r[c] for c in COLS5] for r in R5['lhs']], dec)
roles5 = {d.get('column'): d.get('role') for d in (mld if isinstance(mld, list) else [])}
chk('V5d ML 열 사전 — 열마다 역할 (코드 열 = BLANK_CODE · 분류 = Y_CLASS · dataset = DATASET) · 빈칸 코드 개수',
    roles5.get('d_am_p_um__blank') == 'BLANK_CODE' and roles5.get('ion_percolates_hertz') == 'Y_CLASS' and roles5.get('dataset') == 'DATASET'
    and roles5.get('am_pct') == 'X' and any('NA_PHASE_ABSENT' in str(d.get('blank_codes', '')) for d in (mld if isinstance(mld, list) else [])),
    roles5)
R5b = {'lhs': [dict(OK3[0], am_pct='80.0', top_reachable_pct='90.0', coverage_AM_P_hertz_pct='')]}
chk('V5e 설명 안 되는 빈칸이 있으면 ML 표를 만들지 않는다 (추측으로 코드를 달지 않는다)',
    refused(lambda: LRB.v13_ml_table({'lhs': (COLS5 + ['coverage_AM_P_hertz_pct'], R5b['lhs'])}), 'a'))

# ═══ V6 se_isolated_pct ══════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V6  se_isolated_pct 항등식')
S6 = [{'case_id': 'a', 'top_reachable_pct': '90.0', 'percolation_pct': '85.0', 'se_isolated_pct': repr(10.0)},
      {'case_id': 'b', 'top_reachable_pct': '20.0', 'percolation_pct': '0.0', 'se_isolated_pct': repr(80.0)}]
chk('V6a 맞는 행 → 문제 0', safe(lambda: LRB.v13_se_isolated_problems(S6)) == [])
s6b = safe(lambda: LRB.v13_se_isolated_problems([dict(S6[0], se_isolated_pct='11.0')]))
s6c = safe(lambda: LRB.v13_se_isolated_problems([dict(S6[0], top_reachable_pct='10.0', se_isolated_pct='90.0')]))
s6d = safe(lambda: LRB.v13_se_isolated_problems([{k: v for k, v in S6[0].items() if k != 'se_isolated_pct'}]))
chk('V6b 반례 — 100 − top 아님 · > 100 − percolation · 열 없음 → 문제',
    all(isinstance(x, list) and x for x in (s6b, s6c, s6d)), (s6b, s6c, s6d))

# ═══ V7 재적합 ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V7  porosity–σ–CN 재적합')
rnd = random.Random(7)


def synth_rows(n, alpha, beta, a0, noise=0.0, nonperc=3):
    out = []
    for i in range(n):
        p = rnd.choice([0.0, 0.3, 0.5, 0.7, 1.0])
        rs, rp = rnd.uniform(1.0, 2.5), rnd.uniform(3.0, 6.0)
        phi = rnd.uniform(0.22, 0.75)
        cn = rnd.uniform(2.5, 7.0)
        g = LRB._refit_gate(p, rs if p < 1 else None, rp if p > 0 else None)
        pe = LRB._refit_phi_eff(phi, g)
        lf = a0 + alpha * math.log(pe) + beta * math.log(cn) + rnd.gauss(0.0, noise)
        out.append({'case_id': f's{i:03d}', 'dataset': 'lhs' if i % 3 else 'lhsx', 'ion_net_status_hertz': 'OK', 'f_ion_hertz': repr(math.exp(lf)),
                    'phi_se_mass_conserving': repr(phi), 'porosity_union_exact_pct': repr(100 * (1 - phi / 0.4) if phi < 0.4 else 10.0),
                    'se_se_cn': repr(cn), 'ps_frac': repr(p), 'r_AM_S_um': repr(rs) if p < 1 else '', 'r_AM_P_um': repr(rp) if p > 0 else ''})
    for j in range(nonperc):
        out.append({'case_id': f'n{j}', 'dataset': 'lhs', 'ion_net_status_hertz': 'NOT_PERCOLATING', 'f_ion_hertz': '0.0',
                    'phi_se_mass_conserving': '0.12', 'porosity_union_exact_pct': '20.0', 'se_se_cn': '1.5', 'ps_frac': '0.5', 'r_AM_S_um': '2.0',
                    'r_AM_P_um': '5.0'})
    return out


rows7 = safe(lambda: synth_rows(60, 0.8, 1.6, -3.0, noise=0.0), [])
fit7 = safe(lambda: LRB.refit_porosity_sigma_cn(rows7))
okf = isinstance(fit7, dict) and 'summary' in fit7
fr = (fit7.get('summary') or {}).get('fits', {}).get('free', {}) if okf else {}
lk = (fit7.get('summary') or {}).get('fits', {}).get('locked', {}) if okf else {}
chk('V7a 잡음 없는 합성 법칙 (α 0.8 · β 1.6) — free 적합이 지수를 회복 (1e-6) · R² = 1 · LOOCV ≈ 1',
    okf and abs(fr.get('params', {}).get('alpha', 9) - 0.8) < 1e-6 and abs(fr.get('params', {}).get('beta', 9) - 1.6) < 1e-6
    and abs(fr.get('params', {}).get('a', 9) + 3.0) < 1e-6 and fr.get('r2', 0) > 1 - 1e-9, fr)
chk('V7b locked = 지수 ½ · 2 고정 (등록식 φ_eff^½ · CN²) · 자유 매개변수 1 (a) · LOOCV ≤ R²',
    okf and lk.get('params', {}).get('alpha') == 0.5 and lk.get('params', {}).get('beta') == 2.0 and lk.get('n_free') == 1
    and lk.get('loocv_r2', 9) <= lk.get('r2', -9) + 1e-12, lk)
summ7 = (fit7.get('summary') or {}) if okf else {}
chk('V7c 비관통 3 행은 적합 밖 (사유 NOT_PERCOLATING · 분류 가지) · 표에 행은 남는다 (포함 0)',
    okf and summ7.get('n_fit') == 60 and summ7.get('excluded', {}).get('NOT_PERCOLATING') == 3
    and sum(1 for r in fit7.get('rows', []) if r.get('included') == '0') == 3, summ7.get('excluded'))
rows7n = safe(lambda: synth_rows(80, 0.6, 2.2, -4.0, noise=0.05), [])
f1, f2 = safe(lambda: LRB.refit_porosity_sigma_cn(rows7n)), safe(lambda: LRB.refit_porosity_sigma_cn([dict(r) for r in rows7n]))
chk('V7d 결정적 — 같은 입력 두 번 = 같은 요약 JSON (정렬 키 · repr)', isinstance(f1, dict) and json.dumps(f1, sort_keys=True) == json.dumps(f2, sort_keys=True))
chk('V7e 적합 행 < 5 이면 거부 · 필요한 열이 없으면 거부',
    refused(lambda: LRB.refit_porosity_sigma_cn(rows7[:3]), '') and refused(lambda: LRB.refit_porosity_sigma_cn([{k: v for k, v in r.items()
                                                                                                                     if k != 'se_se_cn'} for r in rows7]), 'se_se_cn'))
chk('V7f 요약 = 식 · 상수 (φc_P 0.200 · φc_S 0.195 · δ 0.040 · r_cut 3.5 · 지수 2 — 등록식 동결값) · 데이터셋별 편향',
    okf and summ7.get('constants', {}).get('phi_c_P') == 0.2 and summ7.get('constants', {}).get('phi_c_S') == 0.195
    and summ7.get('constants', {}).get('delta') == 0.04 and 'lhs' in fr.get('by_dataset', {}) and 'lhsx' in fr.get('by_dataset', {}), summ7.get('constants'))

# ═══ V8 세대 관문 ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V8  세대 관문')


def trow(case, gen, lab_h=G2H, lab_p=G2P, lab_12=G2H12):
    r = {'case_id': case, 'ion_net_generation': gen}
    for m, lab in (('hertz', lab_h), ('physics', lab_p), ('hertz_h12', lab_12)):
        for k, v in (lab or {}).items():
            r[f'ion_net_{k}_{m}'] = v
    return r


G1H = dict(G2H, electrode='virtual_source_legacy')
G1P = {'constriction': 'mikic_psi_divide', 'psi': 'legacy_divide', 'area_rule': 'physics_g1', 'electrode': 'virtual_source_legacy',
       'bulk': 'cylinder_half_d', 'area_mode': 'physics'}
NO12 = {k: '' for k in G2H}
g2rows = [trow('a', 'g2'), trow('b', 'g2')]
legrows = [trow('c', 'inferred_legacy', G1H, G1P, NO12)]
gp = safe(lambda: LRB.v13_generation_problems(g2rows))
chk('V8a 세대 2 행 → (g2, 문제 0)', gp == ('g2', []), gp)
gl = safe(lambda: LRB.v13_generation_problems(legrows))
gld = safe(lambda: LRB.v13_generation_problems(legrows, dry_run=True))
chk('V8b inferred_legacy (세대 1) → 실제 배포는 문제 · dry-run 은 통과 (세대 기록)',
    isinstance(gl, tuple) and not is_err(gl) and gl[1] and gld == ('inferred_legacy', []), (gl, gld))
gm = safe(lambda: LRB.v13_generation_problems(g2rows + legrows, dry_run=True))
chk('V8c 세대 섞임 = dry-run 이어도 문제', isinstance(gm, tuple) and not is_err(gm) and gm[1], gm)
gh = safe(lambda: LRB.v13_generation_problems([trow('d', 'g2', lab_h=G2H12)]))
chk('V8d H12 표기를 주 Hertz 자리에 (G2R-01) = 문제', isinstance(gh, tuple) and not is_err(gh) and gh[1], gh)

# ═══ V9 배치 manifest 관문 ═══════════════════════════════════════════════════════════════════════════════════════════════════════
print('V9  배치 manifest 관문')
with tempfile.TemporaryDirectory() as td9:
    chk('V9a 기대 세대 선언 없는 manifest → 거부', refused(lambda: LRB.v13_manifest_generation(os.path.join(make_batch_root(os.path.join(td9, 'a'), None),
                                                                                                        'manifest.json')), 'expected_network_generation'))
    chk('V9b inferred_legacy 선언 → v1.3 은 거부 (최종판 = 세대 2 만)',
        refused(lambda: LRB.v13_manifest_generation(os.path.join(make_batch_root(os.path.join(td9, 'b'), 'inferred_legacy'), 'manifest.json')), 'g2'))
    chk('V9c g2 선언 → g2', safe(lambda: LRB.v13_manifest_generation(os.path.join(make_batch_root(os.path.join(td9, 'c'), 'g2'), 'manifest.json'))) == 'g2')
chk('V9d 커밋된 v1.2 배치 manifest (11fcf91e8 · 선언 없음) → 거부', refused(lambda: LRB.v13_manifest_generation(os.path.join(BATCH12, 'manifest.json')), ''))

# ═══ V10 단계 A 명령 ═════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V10 단계 A (인계표 생성기 CLI)')
av = safe(lambda: LRB.v13_handover_argv('lhsx', '/R', '/H/lhsx_handover_v13_X.csv', pressure='/R/pressure/lhsx_pressure_record.tsv'))
avu = safe(lambda: LRB.v13_handover_argv('lhs', '/R', '/H/lhs_handover_v13_X.csv', pressure=None))


def _opt(a, k):
    return a[a.index(k) + 1] if isinstance(a, list) and k in a else None


chk('V10a 생성기 CLI — --tau-batch-manifest R/manifest.json · --tau-results R/merged/<ds>/results · --webapp R/merged/<ds> · 묶음 + se_isolation · 압력 기록',
    isinstance(av, list) and _opt(av, '--tau-batch-manifest') == '/R/manifest.json' and _opt(av, '--tau-results') == '/R/merged/lhsx/results'
    and _opt(av, '--webapp') == '/R/merged/lhsx' and set((_opt(av, '--webapp-groups') or '').split(',')) == {
        'contact', 'percolation', 'f1', 'fracture', 'area', 'tau', 'se_isolation'}
    and _opt(av, '--pressure-record') == '/R/pressure/lhsx_pressure_record.tsv' and _opt(av, '--design') == 'docs/data/lhsx_design_adapted_20260929.csv'
    and _opt(av, '--export-handover') == '/H/lhsx_handover_v13_X.csv', av)
chk('V10b 압력 기록 없음 = --pressure-unverified (명시 승인) · 130 은 --design 없음 (기본 설계)',
    isinstance(avu, list) and '--pressure-unverified' in avu and '--pressure-record' not in avu and '--design' not in avu
    and _opt(avu, '--union') == 'docs/data/lhs_union_20260927/lhs130_union.tsv', avu)

#  V10c–e — 단계 A 실행 (subprocess 대역): manifest 관문이 생성기 실행 **전** · 리포 루트에서 · 데이터셋 둘 · 압력 기록 없으면 거부 (명시 승인 없이)
_sp_calls = []


class _FakeRun:
    def __init__(self, rc=0):
        self.returncode, self.stdout, self.stderr = rc, '→ 합성 인계표 (대역)', ''


_orig_run = None
with tempfile.TemporaryDirectory() as td10:
    if hasattr(LRB, 'subprocess'):
        _orig_run = LRB.subprocess.run
        #  생성기 호출 (--export-handover) 만 대역 — 나머지 (git 기록 등) 는 진짜로 돈다
        LRB.subprocess.run = lambda argv, **kw: ((_sp_calls.append((argv, kw.get('cwd'))) or _FakeRun()) if '--export-handover' in argv
                                                 else _orig_run(argv, **kw))
    try:
        b_g2 = make_batch_root(os.path.join(td10, 'b_g2'), 'g2')
        r10c = safe(lambda: LRB.stage_handovers_v13(b_g2, os.path.join(td10, 'h_ok'), DATE, pressure_unverified=True))
        chk('V10c 단계 A — 생성기 두 번 (lhs · lhsx) · 리포 루트에서 · 둘 다 --tau-batch-manifest <배치>/manifest.json · --pressure-unverified',
            not is_err(r10c) and [os.path.basename(c[0][c[0].index('--export-handover') + 1]) for c in _sp_calls]
            == [f'lhs_handover_v13_{DATE}.csv', f'lhsx_handover_v13_{DATE}.csv'] and all(c[1] == ROOT for c in _sp_calls)
            and all(_opt(c[0], '--tau-batch-manifest') == os.path.join(b_g2, 'manifest.json') for c in _sp_calls), (r10c, _sp_calls))
        n0 = len(_sp_calls)
        b_lg = make_batch_root(os.path.join(td10, 'b_lg'), 'inferred_legacy')
        chk('V10d manifest inferred_legacy → 생성기를 부르기 전에 거부', refused(lambda: LRB.stage_handovers_v13(b_lg, os.path.join(td10, 'h_lg'), DATE,
                                                                                                   pressure_unverified=True), 'g2') and len(_sp_calls) == n0)
        chk('V10e 압력 기록이 없고 명시 승인도 없으면 → 거부 (DESC-06)', refused(lambda: LRB.stage_handovers_v13(b_g2, os.path.join(td10, 'h_np'), DATE),
                                                                         'DESC-06') and len(_sp_calls) == n0)
    finally:
        if _orig_run is not None:
            LRB.subprocess.run = _orig_run

# ═══ V11 τ 다시 읽기 배선 ════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V11 τ 다시 읽기 (load_tau_results · 배치 manifest 기대 세대)')
calls = []
_orig = (LDD.load_tau_results, LDD.load_webapp)
TC = TF.column_names()
HROWS = [dict({c: '' for c in TC}, case_id='a', wa_status='done', f_ion_hertz='0.1'), dict({c: '' for c in TC}, case_id='b', wa_status='done')]


def fake_ltr(results_dir, webapp, expected_generation=None):
    calls.append((str(results_dir), expected_generation))
    return {'schema': LDD.TAU_NET_SCHEMA, 'cases': {r['case_id']: {'cells': {c: r[c] for c in TC}} for r in HROWS}}


try:
    LDD.load_tau_results, LDD.load_webapp = fake_ltr, (lambda d, census=None: {'stop_after': 'network', 'status': {}, 'rows': {}})
    p11 = safe(lambda: LRB.v13_reread_tau('lhs', '/R', HROWS, 'g2'))
    chk('V11a load_tau_results(R/merged/lhs/results, expected_generation="g2") 를 부르고 칸이 같으면 문제 0',
        p11 == [] and calls and calls[-1] == (os.path.join('/R', 'merged', 'lhs', 'results'), 'g2'), (p11, calls))
    HROWS2 = [dict(HROWS[0], f_ion_hertz='0.2'), HROWS[1]]
    p11b = safe(lambda: LRB.v13_reread_tau('lhs', '/R', HROWS2, 'g2'))
    chk('V11b 인계표 τ 칸 ≠ 다시 읽은 칸 → 문제 (케이스 · 열)', isinstance(p11b, list) and any('a' in p and 'f_ion_hertz' in p for p in p11b), p11b)

    def boom(*a, **k):
        raise LDD.FillRefusal('τ P4 — 배치 기대 세대 g2 ≠ 레코드 세대 inferred_legacy')
    LDD.load_tau_results = boom
    p11c = safe(lambda: LRB.v13_reread_tau('lhs', '/R', HROWS, 'g2'))
    chk('V11c load_tau_results 거부 (기대 세대 ≠ 레코드) → 문제로 전파 (삼키지 않는다)', isinstance(p11c, list) and any('inferred_legacy' in p for p in p11c), p11c)
finally:
    LDD.load_tau_results, LDD.load_webapp = _orig

# ═══ V12 실제 경로 (합성 세대 2 인계표) ═══════════════════════════════════════════════════════════════════════════════════════════
print('V12 실제 경로 (합성 세대 2 인계표 · τ 다시 읽기 대역)')
_orig_rr = getattr(LRB, 'v13_reread_tau', None)
rr_calls = []
with tempfile.TemporaryDirectory() as td:
    hdir = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    broot = make_batch_root(os.path.join(td, 'batch'), 'g2')
    verdict = os.path.join(td, 'codex_gen2_go.md')
    open(verdict, 'w', encoding='utf-8').write('# GO (합성)\n')
    tfile = os.path.join(td, 'transfer.txt')
    open(tfile, 'w', encoding='utf-8').write('합성 전달 문단 첫 줄 — 판정문 그대로.\n\n둘째 문단.\n')
    out = os.path.join(td, 'release_v13')
    rep = ('ERR', 'not run')
    if _orig_rr is not None:
        LRB.v13_reread_tau = lambda ds, root, rows, gen: rr_calls.append((ds, root, len(rows), gen)) or []
        try:
            rep = safe(lambda: LRB.build_v13(out_dir=out, handover_dir=hdir, batch_root=broot, date=DATE, codex_verdict=verdict,
                                             transfer_text=tfile))
        finally:
            LRB.v13_reread_tau = _orig_rr
    okb = isinstance(rep, dict)
    chk('V12a 만들기 성공 · τ 다시 읽기를 두 데이터셋에 기대 세대 g2 로 불렀다', okb and sorted((c[0], c[3]) for c in rr_calls) == [('lhs', 'g2'), ('lhsx', 'g2')]
        and sorted(c[2] for c in rr_calls) == [64, 130], (rep if not okb else rr_calls))
    names = sorted(os.listdir(out)) if os.path.isdir(out) else []
    want = [f'lhs_release_{DATE}_v13.csv', f'lhs_release_{DATE}_v13_columns.tsv', f'lhsx_release_{DATE}_v13.csv', f'lhs_release_{DATE}_v13_physics.csv',
            f'lhs_mltable_{DATE}_v13.csv', f'lhs_mltable_{DATE}_v13_columns.tsv', 'lhs_v13_refit_porosity_sigma_cn_rows.csv',
            'lhs_v13_refit_porosity_sigma_cn_summary.json', 'README.md', 'v13_build_manifest.json', 'origin', 'previews']
    chk('V12b 산출 — 주 표 · 열 사전 · Physics 부록 · ML 표 · 재적합 (행 · 요약) · README · 빌드 manifest · origin · previews (DRYRUN 표지 없음)',
        all(w in names for w in want) and not any(n.startswith('DRYRUN') for n in names), [w for w in want if w not in names])
    if okb:
        hl, rl = _read_csv(os.path.join(out, f'lhs_release_{DATE}_v13.csv'))
        chk('V12c 주 표 130 × (v1.2 132 + 9) · se_isolated_pct = 100 − top_reachable_pct (전 행) · H12 열 없음',
            len(rl) == 130 and len(hl) == 141 and all(abs(float(r['se_isolated_pct']) - (100 - float(r['top_reachable_pct']))) < 1e-9 for r in rl)
            and not any('h12' in c for c in hl), len(hl))
        prob = safe(lambda: LRB.check_v13(out, hdir))
        chk('V12d check_v13 — 배포 ⊆ 인계표 · ML 표 되읽기 · 빈칸 일관성 · se_isolated · 재적합 재현 · 세대 · sha256 = 문제 0', prob == [], prob)
        man = json.load(open(os.path.join(out, 'v13_build_manifest.json'), encoding='utf-8'))
        chk('V12e 빌드 manifest — dry_run false · 세대 g2 (두 데이터셋) · τ 다시 읽기 수행 · Codex 판정문 · 파일 sha256',
            man.get('dry_run') is False and man.get('generation') == {'lhs': 'g2', 'lhsx': 'g2'} and man.get('tau_reread') == 'performed'
            and man.get('codex_verdict') and isinstance(man.get('files'), dict) and len(man['files']) >= 10, {k: man.get(k) for k in ('dry_run', 'generation')})
        rd = open(os.path.join(out, 'README.md'), encoding='utf-8').read()
        chk('V12f README — v1.3 최종판 · 빈칸 코드 표 (#1) · f_ion_hertz 타깃 · 관통 분류 먼저 (#2) · 재적합 (#5) · 수송 tortuosity · se_isolated_pct · DRY RUN 아님',
            all(k in rd for k in ('v1.3', 'NA_PHASE_ABSENT', 'INF_NOT_PERCOLATING', 'f_ion_hertz', '관통 분류', 'porosity–σ–CN', '수송 tortuosity',
                                  'se_isolated_pct', '제곱근 아님')) and 'DRY RUN' not in rd)
        chk('V12k 전달 문안 (--transfer-text) — README 외부 검토 절에 그대로 (인용) · 빌드 manifest 에 파일 sha256',
            '> 합성 전달 문단 첫 줄 — 판정문 그대로.' in rd and '> 둘째 문단.' in rd
            and (man.get('transfer_text') or {}).get('sha256') == __import__('hashlib').sha256(open(tfile, 'rb').read()).hexdigest(),
            man.get('transfer_text'))

        def tamper(path, old, new, count=1):
            s = open(path, encoding='utf-8').read()
            assert old in s, old
            open(path, 'w', encoding='utf-8', newline='').write(s.replace(old, new, count))
        mlp = os.path.join(out, f'lhs_mltable_{DATE}_v13.csv')
        bak = open(mlp, encoding='utf-8').read()
        tamper(mlp, 'INF_NOT_PERCOLATING', 'NOT_COMPUTED')
        pt = safe(lambda: LRB.check_v13(out, hdir))
        open(mlp, 'w', encoding='utf-8', newline='').write(bak)
        chk('V12g 변조 — ML 표 코드 한 칸 (INF_NOT_PERCOLATING → NOT_COMPUTED) → check_v13 문제', isinstance(pt, list) and pt, pt)
        sp = os.path.join(out, 'lhs_v13_refit_porosity_sigma_cn_summary.json')
        bak = open(sp, encoding='utf-8').read()
        js = json.loads(bak)
        js['fits']['free']['params']['alpha'] = js['fits']['free']['params']['alpha'] + 0.01
        open(sp, 'w', encoding='utf-8').write(json.dumps(js, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
        pt2 = safe(lambda: LRB.check_v13(out, hdir))
        open(sp, 'w', encoding='utf-8', newline='').write(bak)
        chk('V12h 변조 — 재적합 요약 지수 +0.01 → check_v13 문제 (다시 적합한 값과 다르다)', isinstance(pt2, list) and any('재적합' in p or 'refit' in p for p in pt2), pt2)
        os.remove(os.path.join(out, 'README.md'))
        pt3 = safe(lambda: LRB.check_v13(out, hdir))
        chk('V12i 파일 하나 지움 (README) → check_v13 문제 (빌드 manifest 의 파일 목록)', isinstance(pt3, list) and any('README' in p for p in pt3), pt3)
    else:
        for n in ('V12c', 'V12d', 'V12e', 'V12f', 'V12k', 'V12g', 'V12h', 'V12i'):
            chk(f'{n} (만들기 실패로 건너뜀)', False, rep)
    #  V12j — 인계표의 se_isolated_pct 를 (top 은 그대로) 틀리게 → 만들기 거부 (S1 항등식 · 배포 관문)
    hdir2 = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover_bad'),
                                              mutate=lambda ds, h, rows: rows[0].update(se_isolated_pct='99.0') if ds == 'lhs' else None))
    out2 = os.path.join(td, 'release_bad')
    if _orig_rr is not None:
        LRB.v13_reread_tau = lambda *a: []
        try:
            ok12j = refused(lambda: LRB.build_v13(out_dir=out2, handover_dir=hdir2, batch_root=broot, date=DATE, codex_verdict=verdict), 'se_isolated')
        finally:
            LRB.v13_reread_tau = _orig_rr
    else:
        ok12j = False
    chk('V12j 인계표 se_isolated_pct ≠ 100 − top_reachable_pct → 만들기 거부 · 산출 폴더 남지 않음', ok12j and not os.path.exists(out2))

# ═══ V13 실제 경로 거부 ══════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V13 실제 경로 거부')
with tempfile.TemporaryDirectory() as td:
    hdir = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    verdict = os.path.join(td, 'codex.md')
    open(verdict, 'w', encoding='utf-8').write('x\n')
    b_ok, b_leg = make_batch_root(os.path.join(td, 'b_ok'), 'g2'), make_batch_root(os.path.join(td, 'b_leg'), 'inferred_legacy')
    res = {}
    if _orig_rr is not None:
        LRB.v13_reread_tau = lambda *a: []
        try:
            res['verdict'] = refused(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o1'), handover_dir=hdir, batch_root=b_ok, date=DATE, codex_verdict=None),
                                     'Codex')
            res['legacy'] = refused(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o2'), handover_dir=hdir, batch_root=b_leg, date=DATE,
                                                          codex_verdict=verdict), 'g2')
            res['nobatch'] = refused(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o3'), handover_dir=hdir, batch_root=None, date=DATE,
                                                           codex_verdict=verdict), 'batch')
            LRB.v13_reread_tau = lambda *a: ['a: f_ion_hertz 인계표 0.1 ≠ 다시 읽음 0.2']
            res['reread'] = refused(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o4'), handover_dir=hdir, batch_root=b_ok, date=DATE,
                                                          codex_verdict=verdict), 'τ')
        finally:
            LRB.v13_reread_tau = _orig_rr
    chk('V13a Codex 판정문 없음 · manifest inferred_legacy · 배치 뿌리 없음 (τ 다시 읽기 불가) · τ 다시 읽기 문제 → 전부 거부', res == {
        'verdict': True, 'legacy': True, 'nobatch': True, 'reread': True}, res)
    chk('V13b 거부된 실행은 산출 폴더를 남기지 않는다', not any(os.path.exists(os.path.join(td, f'o{i}')) for i in range(1, 5)))

# ═══ V14 DRY RUN (커밋된 v1.2 = 세대 1) ══════════════════════════════════════════════════════════════════════════════════════════
print('V14 DRY RUN (커밋된 v1.2 원천 · 세대 1)')
with tempfile.TemporaryDirectory() as td:
    o_real = os.path.join(td, 'real')
    chk('V14a 세대 1 인계표로 dry-run 없이 → 거부 (세대 · v1.3 = g2) · 폴더 안 만듦',
        refused(lambda: LRB.build_v13(out_dir=o_real, handover_dir=V12, date=DATE, dry_run=False, batch_root=BATCH12,
                                      codex_verdict=os.path.join(ROOT, 'CLAUDE.md')), '') and not os.path.exists(o_real))
    o_dry = os.path.join(td, 'dry')
    rep = safe(lambda: LRB.build_v13(out_dir=o_dry, handover_dir=V12, date=DATE, dry_run=True))
    names = sorted(os.listdir(o_dry)) if os.path.isdir(o_dry) else []
    files = [n for n in names if os.path.isfile(os.path.join(o_dry, n))]
    chk('V14b dry-run — 만들기 성공 · 모든 파일 이름이 DRYRUN_ 로 시작 · origin · previews 도', isinstance(rep, dict) and files and all(n.startswith('DRYRUN_')
        for n in files) and all(n.startswith('DRYRUN_') for d in ('origin', 'previews') for n in (os.listdir(os.path.join(o_dry, d))
                                                                                                    if os.path.isdir(os.path.join(o_dry, d)) else ['x'])),
        rep if not isinstance(rep, dict) else files)
    if isinstance(rep, dict):
        rd = open(os.path.join(o_dry, 'DRYRUN_README.md'), encoding='utf-8').read()
        man = json.load(open(os.path.join(o_dry, 'DRYRUN_v13_build_manifest.json'), encoding='utf-8'))
        chk('V14c 표지 — README 첫 줄 "DRY RUN — not a release" · manifest dry_run true · 세대 inferred_legacy · 빠진 v1.3 열 목록 (se_isolated_pct · 세대 2 표기 · 압력)',
            rd.splitlines()[0].count('DRY RUN — not a release') == 1 and man.get('dry_run') is True
            and man.get('generation') == {'lhs': 'inferred_legacy', 'lhsx': 'inferred_legacy'}
            and all(c in (man.get('missing_columns') or {}).get('lhs', []) for c in ('se_isolated_pct', 'ion_net_electrode_hertz', 'press_reached')),
            (rd.splitlines()[:1], man.get('missing_columns')))
        pd = safe(lambda: LRB.check_v13(o_dry, V12, dry_run=True))
        chk('V14d check_v13 (dry-run) — 배포 ⊆ 인계표 · ML 표 · 빈칸 · 재적합 재현 = 문제 0', pd == [], pd)
        sm = json.load(open(os.path.join(o_dry, 'DRYRUN_lhs_v13_refit_porosity_sigma_cn_summary.json'), encoding='utf-8'))
        chk('V14e 재적합 (세대 1 · DRY RUN) — 관통 행 170 (130 중 106 + 64) · 비관통 24 제외 · 요약 dry_run true',
            sm.get('n_fit') == 170 and sm.get('excluded', {}).get('NOT_PERCOLATING') == 24 and sm.get('dry_run') is True, {k: sm.get(k) for k in ('n_fit', 'excluded')})
        mlh, mlr = _read_csv(os.path.join(o_dry, f'DRYRUN_lhs_mltable_{DATE}_v13.csv'))
        np_ = [r for r in mlr if r.get('ion_net_status_hertz') == 'NOT_PERCOLATING']
        chk('V14f ML 표 (실데이터 세대 1) — 비관통 24 = tau2 INF_NOT_PERCOLATING · 기하 τ NA_NOT_PERCOLATING · 분류 0 · mono 30 = NA_PHASE_ABSENT',
            len(np_) == 24 and all(r['tau2_ion_hertz__blank'] == 'INF_NOT_PERCOLATING' and r['tortuosity_SE_wall__blank'] == 'NA_NOT_PERCOLATING'
                                   and r['ion_percolates_hertz'] == '0' for r in np_)
            and sum(1 for r in mlr if r.get('d_am_p_um__blank') == 'NA_PHASE_ABSENT') == 15
            and sum(1 for r in mlr if r.get('d_am_s_um__blank') == 'NA_PHASE_ABSENT') == 15, len(np_))
    else:
        for n in ('V14c', 'V14d', 'V14e', 'V14f'):
            chk(f'{n} (dry-run 만들기 실패로 건너뜀)', False, rep)
    chk('V14g dry-run 산출을 docs/data 아래로 → 거부 (폴더 안 만듦)',
        refused(lambda: LRB.build_v13(out_dir=os.path.join(ROOT, 'docs', 'data', 'lhs_release_DRYRUN_test_v13'), handover_dir=V12, date=DATE,
                                      dry_run=True), 'docs/data')
        and not os.path.exists(os.path.join(ROOT, 'docs', 'data', 'lhs_release_DRYRUN_test_v13')))

# ═══ V15 CLI ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
print('V15 CLI')
with tempfile.TemporaryDirectory() as td:
    o = os.path.join(td, 'cli_dry')
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        rc = safe(lambda: LRB.main(['--v13', '--dry-run', '--handover-dir', V12, '--out-dir', o, '--date', DATE]), 99)
    chk('V15a --v13 --dry-run → rc 0 · 산출', rc == 0 and os.path.isfile(os.path.join(o, 'DRYRUN_README.md')), (rc, buf.getvalue()[-400:]))
    buf2 = io.StringIO()
    with contextlib.redirect_stdout(buf2), contextlib.redirect_stderr(buf2):
        rc2 = safe(lambda: LRB.main(['--v13-check', '--dry-run', '--handover-dir', V12, '--release-dir', o]), 99)
    chk('V15b --v13-check --dry-run → rc 0', rc2 == 0, (rc2, buf2.getvalue()[-400:]))
    o3 = os.path.join(td, 'cli_real')
    buf3 = io.StringIO()
    with contextlib.redirect_stdout(buf3), contextlib.redirect_stderr(buf3):
        rc3 = safe(lambda: LRB.main(['--v13', '--handover-dir', V12, '--out-dir', o3, '--date', DATE]), 99)
    chk('V15c dry-run 없이 세대 1 원천 → rc ≠ 0 · 폴더 안 만듦', rc3 not in (0, 99) and not os.path.exists(o3), (rc3, buf3.getvalue()[-300:]))

# ═══ V16 발사 봉인 대조 (세대 2 등록 20261007_g2 §3 · §5) ═══════════════════════════════════════════════════════════════════════
#   실행기 manifest 의 code_hashes (봉인 29 — 워커 체크아웃에서 잰 값) ↔ v1.3 을 만드는 체크아웃 · handover_code_hashes (생성기 · 다시 읽기 도구) ·
#   ⓪b 다시 읽기 기록 (reread.json n_fail).  봉인 파일이 다르면 거부 (값과 무관한 변경 = --allow-seal-diff 명시 승인 · 기록) · 인계 도구 다름 = 경고 (등록 §3 ⚠).
print('V16 발사 봉인 대조 (code_hashes · handover_code_hashes · ⓪b 다시 읽기 기록)')


def refusal_msg(fn):
    """fn() 이 ReleaseError · FillRefusal 로 거부하면 그 메시지 · 다른 예외면 'OTHER …' · 통과하면 None."""
    try:
        fn()
    except Exception as e:                                                # noqa: BLE001
        bad = getattr(LRB, 'ReleaseError', RuntimeError)
        return str(e) if isinstance(e, (bad, LDD.FillRefusal)) else f'OTHER {type(e).__name__}: {e}'
    return None


with tempfile.TemporaryDirectory() as td:
    b0 = make_batch_root(os.path.join(td, 'b0'))
    d0 = safe(lambda: LRB.v13_seal_drift(os.path.join(b0, 'manifest.json')))
    chk('V16a 발사 기록 = 지금 파일 → 봉인 다름 0 · 인계 도구 다름 0 · 봉인 파일 수 · git HEAD (40 자리)',
        isinstance(d0, dict) and d0.get('sealed') == len(SEAL_FILES) and d0.get('sealed_changed') == [] and d0.get('handover_changed') == []
        and isinstance(d0.get('git_head'), str) and len(d0['git_head']) == 40, d0)
    b1 = make_batch_root(os.path.join(td, 'b1'), handover=False,
                         alter={'webapp/app.py': '0' * 64, 'scripts/nope_missing.py': 'ab' * 32, '/etc/hostname': 'cd' * 32, '../x.py': 'ef' * 32})
    d1 = safe(lambda: LRB.v13_seal_drift(os.path.join(b1, 'manifest.json')))
    chk('V16b 바뀐 봉인 파일 · 없는 파일 · 리포 밖 경로 (절대 · ..) = 다름 (정렬) · handover 기록 없으면 None (모름 — 같다고 하지 않는다)',
        isinstance(d1, dict) and d1.get('sealed_changed') == sorted(['webapp/app.py', 'scripts/nope_missing.py', '/etc/hostname', '../x.py'])
        and d1.get('handover') is None and d1.get('handover_changed') is None, d1)
    b2 = make_batch_root(os.path.join(td, 'b2'), code=False)
    chk('V16c manifest 에 code_hashes 가 없으면 → 거부 (무엇과 대조할지 모른다 · 194 실행기 manifest 아님)',
        refused(lambda: LRB.v13_seal_drift(os.path.join(b2, 'manifest.json')), 'code_hashes'))

    hd = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    ver = os.path.join(td, 'go.md')
    open(ver, 'w', encoding='utf-8').write('# GO (합성)\n')
    r16 = {}
    if _orig_rr is not None and not is_err(hd):
        LRB.v13_reread_tau = lambda *a: []
        try:
            b_app = make_batch_root(os.path.join(td, 'b_app'), alter={'webapp/app.py': '0' * 64})
            r16['app_msg'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o_app'), handover_dir=hd, batch_root=b_app, date=DATE,
                                                               codex_verdict=ver))
            r16['app_nodir'] = not os.path.exists(os.path.join(td, 'o_app'))
            o_ok = os.path.join(td, 'o_app_allowed')
            r16['app_ok'] = safe(lambda: LRB.build_v13(out_dir=o_ok, handover_dir=hd, batch_root=b_app, date=DATE, codex_verdict=ver,
                                                       allow_seal_diff=['webapp/app.py']))
            if isinstance(r16['app_ok'], dict):
                r16['app_man'] = json.load(open(os.path.join(o_ok, 'v13_build_manifest.json'), encoding='utf-8'))
                r16['app_readme'] = open(os.path.join(o_ok, 'README.md'), encoding='utf-8').read()
                r16['app_check'] = safe(lambda: LRB.check_v13(o_ok, hd))
                #  변조 — 빌드 manifest 의 명시 승인 목록을 비우면 check_v13 이 잡는다 (다른 봉인 파일 ⊄ 승인)
                mp_ = os.path.join(o_ok, 'v13_build_manifest.json')
                bak = open(mp_, encoding='utf-8').read()
                mj = json.loads(bak)
                mj['code_identity']['allowed'] = []
                open(mp_, 'w', encoding='utf-8').write(json.dumps(mj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
                r16['app_tamper'] = safe(lambda: LRB.check_v13(o_ok, hd))
                open(mp_, 'w', encoding='utf-8', newline='').write(bak)
            b_hd = make_batch_root(os.path.join(td, 'b_hd'), alter={'scripts/lhs_design_dataset.py': '1' * 64})
            o_hd = os.path.join(td, 'o_hd')
            r16['hd'] = safe(lambda: LRB.build_v13(out_dir=o_hd, handover_dir=hd, batch_root=b_hd, date=DATE, codex_verdict=ver))
            if isinstance(r16['hd'], dict):
                r16['hd_man'] = json.load(open(os.path.join(o_hd, 'v13_build_manifest.json'), encoding='utf-8'))
                r16['hd_readme'] = open(os.path.join(o_hd, 'README.md'), encoding='utf-8').read()
            b_rf = make_batch_root(os.path.join(td, 'b_rf'), reread=lambda r: dict(r, n_fail=1))
            r16['rf_msg'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o_rf'), handover_dir=hd, batch_root=b_rf, date=DATE,
                                                              codex_verdict=ver))
            b_rl = make_batch_root(os.path.join(td, 'b_rl'), reread=lambda r: dict(r, expected_generation='inferred_legacy'))
            r16['rl_msg'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o_rl'), handover_dir=hd, batch_root=b_rl, date=DATE,
                                                              codex_verdict=ver))
            b_r0 = make_batch_root(os.path.join(td, 'b_r0'))
            o_r0 = os.path.join(td, 'o_r0')
            r16['r0'] = safe(lambda: LRB.build_v13(out_dir=o_r0, handover_dir=hd, batch_root=b_r0, date=DATE, codex_verdict=ver))
            if isinstance(r16['r0'], dict):
                r16['r0_man'] = json.load(open(os.path.join(o_r0, 'v13_build_manifest.json'), encoding='utf-8'))
                #  check_v13 — 빌드 manifest 의 다시 읽기 기록을 일부 집합으로 바꾸면 문제 (G2RR2-02 · ★ G2RR3-01: 기록 ≠ 지금 배치 뿌리)
                _mp = os.path.join(o_r0, 'v13_build_manifest.json')
                _mm = json.load(open(_mp, encoding='utf-8'))
                _mm['batch_gate_files']['reread.json'].update(set_equal=False, read_n=193)
                json.dump(_mm, open(_mp, 'w', encoding='utf-8'))
                r16['r0_tamper'] = safe(lambda: LRB.check_v13(o_r0, hd))
            #  ★ 10-07 G2RR2-02 (Codex 세대 2 재검증 2 §3) — n_fail 0 · g2 여도 등록 집합 (생산 194) 을 다 읽은 기록이 아니면 거부
            r16['rs_msg'] = {}
            for tag, rec in (('일부 집합 (193 · 같음 False)', lambda r: dict(r, read_n=193, set_equal=False, missing=[['lhs00_055', 'lhs']])),
                             ('시범 집합 pilot3', lambda r: dict(r, expected_set='pilot3', expected_n=3, read_n=3)),
                             ('옛 도구 기록 (집합 필드 없음)', lambda r: {k: v for k, v in r.items() if k in ('schema', 'expected_generation', 'n_fail')}),
                             ('0 케이스 (기대 0)', lambda r: dict(r, expected_n=0, read_n=0))):
                b_rs = make_batch_root(os.path.join(td, f'b_rs{len(r16["rs_msg"])}'), reread=rec)
                o_rs = os.path.join(td, f'o_rs{len(r16["rs_msg"])}')
                r16['rs_msg'][tag] = (refusal_msg(lambda: LRB.build_v13(out_dir=o_rs, handover_dir=hd, batch_root=b_rs, date=DATE, codex_verdict=ver)),
                                      os.path.exists(o_rs))
            o_un = os.path.join(td, 'o_unused')
            r16['unused'] = safe(lambda: LRB.build_v13(out_dir=o_un, handover_dir=hd, batch_root=b0, date=DATE, codex_verdict=ver,
                                                       allow_seal_diff=['webapp/app.py']))
            #  승인 경로 철자 — './webapp/app.py' 도 같은 파일 (정규화) · 승인 기록은 manifest 키 철자로
            o_nm = os.path.join(td, 'o_norm')
            r16['norm'] = safe(lambda: LRB.build_v13(out_dir=o_nm, handover_dir=hd, batch_root=b_app, date=DATE, codex_verdict=ver,
                                                     allow_seal_diff=['./webapp/app.py']))
            if isinstance(r16['norm'], dict):
                r16['norm_ci'] = json.load(open(os.path.join(o_nm, 'v13_build_manifest.json'), encoding='utf-8')).get('code_identity')
            #  CLI — --allow-seal-diff 가 build_v13 까지 간다 (인계표 폴더를 주면 단계 A 없이)
            o_cli = os.path.join(td, 'o_cli')
            bufc = io.StringIO()
            with contextlib.redirect_stdout(bufc), contextlib.redirect_stderr(bufc):
                r16['cli_refuse'] = safe(lambda: LRB.main(['--v13', '--handover-dir', hd, '--batch-root', b_app, '--codex-verdict', ver,
                                                           '--out-dir', o_cli, '--date', DATE]), 99)
                r16['cli_ok'] = safe(lambda: LRB.main(['--v13', '--handover-dir', hd, '--batch-root', b_app, '--codex-verdict', ver,
                                                       '--out-dir', o_cli, '--date', DATE, '--allow-seal-diff', 'webapp/app.py']), 99)
            r16['cli_out'] = os.path.isfile(os.path.join(o_cli, 'README.md'))
        finally:
            LRB.v13_reread_tau = _orig_rr
    am = r16.get('app_msg') or ''
    chk('V16d 봉인 파일 (webapp/app.py) 이 발사 기록과 다르면 → 만들기 거부 (파일 이름 · --allow-seal-diff 안내) · 산출 폴더 없음',
        'webapp/app.py' in am and '--allow-seal-diff' in am and not am.startswith('OTHER') and r16.get('app_nodir') is True, am[:300])
    man16 = r16.get('app_man') or {}
    ci = man16.get('code_identity') or {}
    chk('V16e --allow-seal-diff webapp/app.py (명시 승인) → 만들기 성공 · 빌드 manifest code_identity (다른 파일 · 승인 · 봉인 수) · README 에 승인 기록 · check_v13 문제 0',
        isinstance(r16.get('app_ok'), dict) and ci.get('sealed_changed') == ['webapp/app.py'] and ci.get('allowed') == ['webapp/app.py']
        and ci.get('sealed') == len(SEAL_FILES) and '--allow-seal-diff' in (r16.get('app_readme') or '') and r16.get('app_check') == [],
        (r16.get('app_ok') if not isinstance(r16.get('app_ok'), dict) else ci, r16.get('app_check')))
    chk('V16f 변조 — 빌드 manifest 승인 목록을 비우면 (다른 봉인 파일 ⊄ 승인) → check_v13 문제',
        isinstance(r16.get('app_tamper'), list) and any('webapp/app.py' in p for p in r16['app_tamper']), r16.get('app_tamper'))
    hdm = (r16.get('hd_man') or {}).get('code_identity') or {}
    chk('V16g 인계 생성기 지문 ≠ 발사 기록 (handover_code_hashes) → 만들기는 한다 · 경고 (등록 §3 ⚠ — 커밋을 §9 에) · manifest · README 에 기록',
        isinstance(r16.get('hd'), dict) and hdm.get('handover_changed') == ['scripts/lhs_design_dataset.py']
        and any('handover_code_hashes' in w for w in r16['hd'].get('warnings', [])) and 'handover_code_hashes' in (r16.get('hd_readme') or ''),
        (r16.get('hd') if not isinstance(r16.get('hd'), dict) else hdm))
    rf, rl = r16.get('rf_msg') or '', r16.get('rl_msg') or ''
    chk('V16h ⓪b 다시 읽기 기록 (reread.json) 이 실패 (n_fail 1) · 다른 기대 세대 → 만들기 거부 (등록 §5-3)',
        'reread.json' in rf and not rf.startswith('OTHER') and 'reread.json' in rl and not rl.startswith('OTHER'), (rf[:200], rl[:200]))
    r0m = r16.get('r0_man') or {}
    gf = (r0m.get('batch_gate_files') or {})
    bg16 = r0m.get('batch_gate') or {}
    chk('V16i 감사 · 다시 읽기 기록 통과 (n_fail 0 · g2 · 등록 집합 production194 전부 = 기대 194 · 읽음 194 · 같음 · 이 배치 뿌리에 결합) → 만들기 성공 · '
        '두 기록 sha256 · 판정 필드 · 관문 결과 release · 문제 0 · 배치 뿌리 (★ G2RR3-01 — 감사 기록 없음은 이제 경고가 아니라 거부 · V17)',
        isinstance(r16.get('r0'), dict) and (gf.get('reread.json') or {}).get('n_fail') == 0
        and {k: (gf.get('reread.json') or {}).get(k) for k in ('expected_set', 'expected_n', 'read_n', 'set_equal')}
        == {'expected_set': 'production194', 'expected_n': 194, 'read_n': 194, 'set_equal': True}
        and (gf.get('reread.json') or {}).get('sha256') == _sha_path(os.path.join(b_r0, 'reread.json'))
        and (gf.get('seal_audit.json') or {}).get('sha256') == _sha_path(os.path.join(b_r0, 'seal_audit.json'))
        and bg16.get('mode') == 'release' and bg16.get('problems') == [] and bg16.get('batch_root') == os.path.realpath(b_r0)
        and r0m.get('diagnostic') is False and not any('seal_audit.json' in w for w in r16['r0'].get('warnings', [])),
        (r16.get('r0') if not isinstance(r16.get('r0'), dict) else (gf, bg16)))
    rs = r16.get('rs_msg') or {}
    chk('V16n ⓪b 다시 읽기 기록이 n_fail 0 · g2 여도 등록 집합 production194 전부가 아니면 (일부 · pilot3 · 옛 도구 기록 · 0 케이스) → 만들기 거부 · 산출 폴더 없음 (G2RR2-02)',
        len(rs) == 4 and all(m is not None and not m.startswith('OTHER') and 'production194' in m and not made for m, made in rs.values()),
        {k: ((m or '')[:160], made) for k, (m, made) in rs.items()})
    chk('V16o check_v13 — 빌드 manifest 의 다시 읽기 기록을 일부 집합으로 바꾸면 문제 (G2RR2-02 · ★ G2RR3-01 기록 ≠ 지금 배치 뿌리)',
        isinstance(r16.get('r0_tamper'), list) and any(('G2RR2-02' in p_) or ('reread.json' in p_) for p_ in r16['r0_tamper']), r16.get('r0_tamper'))
    try:
        import run_network_194_parallel as _NP194                         # noqa: E402
        _reg = (getattr(_NP194, 'REGISTERED_ID_SETS', None) or {}).get(getattr(LRB, 'V13_REREAD_SET', None)) or {}
    except Exception as e:                                                # noqa: BLE001
        _reg = {'err': repr(e)}
    chk('V16p 빌드의 등록 집합 이름 · 크기 = 실행기 등록 (REGISTERED_ID_SETS · 다시 읽기 --expect-set 과 같은 표)',
        getattr(LRB, 'V13_REREAD_SET', None) == 'production194' and _reg.get('n') == getattr(LRB, 'V13_REREAD_N', None) == 194, _reg)
    un = r16.get('unused')
    chk('V16j 승인했지만 바뀌지 않은 파일 (--allow-seal-diff webapp/app.py · 봉인 같음) → 만들기는 한다 · 경고 (쓰이지 않은 승인)',
        isinstance(un, dict) and any('--allow-seal-diff' in w and 'webapp/app.py' in w for w in un.get('warnings', [])), un)
    nci = r16.get('norm_ci') or {}
    chk('V16m 승인 경로 철자 정규화 — "./webapp/app.py" = webapp/app.py (만들기 성공 · 승인 기록 = manifest 키 철자)',
        isinstance(r16.get('norm'), dict) and nci.get('allowed') == ['webapp/app.py'] and nci.get('sealed_changed') == ['webapp/app.py'],
        r16.get('norm') if not isinstance(r16.get('norm'), dict) else nci)
    chk('V16k CLI --allow-seal-diff — 없으면 rc ≠ 0 · 있으면 rc 0 · 산출',
        r16.get('cli_refuse') not in (0, 99, None) and r16.get('cli_ok') == 0 and r16.get('cli_out') is True,
        (r16.get('cli_refuse'), r16.get('cli_ok'), bufc.getvalue()[-300:] if 'bufc' in dir() else ''))

#  V16l — 단계 A 도 같은 관문 (생성기 실행 전에) · 승인하면 생성기를 부른다
_sp16 = []
with tempfile.TemporaryDirectory() as td:
    if hasattr(LRB, 'subprocess'):
        _orun = LRB.subprocess.run
        LRB.subprocess.run = lambda argv, **kw: (_sp16.append(argv) or _FakeRun()) if '--export-handover' in argv else _orun(argv, **kw)
        try:
            b_a = make_batch_root(os.path.join(td, 'b_a'), alter={'webapp/app.py': '0' * 64})
            m16l = refusal_msg(lambda: LRB.stage_handovers_v13(b_a, os.path.join(td, 'h1'), DATE, pressure_unverified=True))
            n_before = len(_sp16)
            r16l = safe(lambda: LRB.stage_handovers_v13(b_a, os.path.join(td, 'h2'), DATE, pressure_unverified=True, allow_seal_diff=['webapp/app.py']))
        finally:
            LRB.subprocess.run = _orun
    else:
        m16l, n_before, r16l = None, 0, ('ERR', 'no subprocess')
chk('V16l 단계 A — 봉인 다름이면 생성기를 부르기 전에 거부 · 명시 승인이면 생성기 두 번',
    m16l is not None and 'webapp/app.py' in m16l and n_before == 0 and not is_err(r16l) and len(_sp16) == 2, (m16l, n_before, r16l, len(_sp16)))

# ═══ V17 ★ 10-07 G2RR3-01 — 배치 관문 증거 필수 · 판정 · 결합 · build = check 같은 관문 · 진단 모드 ═════════════════════════════════════
#   Codex 세대 2 재검증 3 §3 (`docs/reviews/codex_review_gen2_network_reverify3_20261007.md` · 탐침 release_gate.py · new_gates.py) — 옛 판은 감사 기록의
#   해시만 적고 판정을 안 읽었고, 다시 읽기 기록이 없거나 · `{` · {} · n_fail null 이면 경고만 남기고 실제 build_v13 이 21 파일 묶음을 만들었다
#   (check_v13 문제 0).  [C] = Codex 변이 그대로 · 나머지 = 같은 부류 보강 (감사 없음 · 깨짐 · 다른 배치 뿌리 · 봉인 지문 · 발사 sha · manifest 바뀜 ·
#   타입 · 등록 집합 · 생산 정책 SEALED 만).  변이는 결합된 통과 기록에서 **한 판정만** 틀리게 만든다 (거부 메시지에 그 판정의 꼬리표).
print('V17 배치 관문 증거 (⓪ 감사 · ⓪b 다시 읽기 · G2RR3-01)')


def _aud(**over):
    """감사 통과 기록의 최상위 필드만 바꾸는 변이."""
    return lambda a: dict(a, **over)


def _aud_rows(fn, summary=True, **over):
    """감사 기록의 행을 바꾸는 변이 — summary=True 면 요약 (verdicts · merged) 도 행에서 다시 센다 (요약 ↔ 행 일관 — 그 판정 하나만 실패하게)."""
    def f(a):
        a = json.loads(json.dumps(a))
        fn(a['cases'])
        if summary:
            a['verdicts'] = dict(collections.Counter(r['verdict'] for r in a['cases']))
            a['merged'] = dict(collections.Counter(r['merged'] for r in a['cases']))
        a.update(over)
        return a
    return f


def _row0(**kv):
    return lambda rows: rows[0].update(kv)


def _all_unsealed(rows):
    for r in rows:
        r['verdict'] = 'UNSEALED'


V17_NOID = ('launcher_root', 'manifest_sha256', 'seal_fp', 'launch_sha')
V17_REFUSED_AUDIT = (lambda a: {'schema': a['schema'], 'root': a['root'], 'audited_at': a['audited_at'], 'refused': True,
                                'eligibility': {'kind': 'invalid', 'historical': None, 'problems': ['G2RR2-01 missing input_digest'], 'note': ''}})
V17_VARIANTS = (
    #  (이름, make_batch_root 인자, 거부 메시지에 있어야 할 꼬리표, Codex 변이 표지)
    ('reread 없음', dict(reread=None), 'reread.json', 'C'),
    ('reread 깨진 JSON `{`', dict(reread=b'{'), 'reread.json', 'C'),
    ('reread {}', dict(reread={}), 'reread.json', 'C'),
    ('reread null', dict(reread=b'null'), 'reread.json', 'C'),
    ('reread n_fail null', dict(reread=lambda r: dict(r, n_fail=None)), 'n_fail', 'C'),
    ('reread 명시 n_fail 1', dict(reread=lambda r: dict(r, n_fail=1)), 'n_fail', 'C'),
    ('감사 refused · 자격 invalid', dict(audit=V17_REFUSED_AUDIT), 'seal_audit.json', 'C'),
    ('감사 UNSEALED 194 · generation_problems', dict(audit=_aud_rows(_all_unsealed, generation_problems=["lhs00_000: 레코드 세대 'inferred_legacy' ≠ g2"])),
     'UNSEALED', 'C'),
    ('감사 없음', dict(audit=None), 'seal_audit.json', ''),
    ('감사 깨진 JSON `{`', dict(audit=b'{'), 'seal_audit.json', ''),
    ('감사 null', dict(audit=b'null'), 'seal_audit.json', ''),
    ('reread 다른 배치 뿌리', dict(reread=lambda r: dict(r, launcher_root='/elsewhere/net194_other')), 'launcher_root', ''),
    ('감사 다른 배치 뿌리', dict(audit=_aud(root='/elsewhere/net194_other')), '배치 뿌리', ''),
    ('reread 다른 봉인 지문', dict(reread=lambda r: dict(r, seal_fp='0' * 64)), 'seal_fp', ''),
    ('감사 다른 봉인 지문', dict(audit=_aud(seal_fp='0' * 64)), 'seal_fp', ''),
    ('reread 뒤 manifest 바뀜 (manifest_sha256 다름)', dict(reread=lambda r: dict(r, manifest_sha256='f' * 64)), 'manifest_sha256', ''),
    ('reread 다른 발사 sha', dict(reread=lambda r: dict(r, launch_sha='cd' * 20)), 'launch_sha', ''),
    ('감사 다른 발사 sha', dict(audit=_aud(launch_sha='cd' * 20)), 'launch_sha', ''),
    ('reread 옛 도구 v2 기록 (실행 신원 필드 없음)', dict(reread=lambda r: {k: v for k, v in dict(r, schema='g2_network_reread/v2').items() if k not in V17_NOID}),
     'schema', ''),
    ('reread n_fail True (bool)', dict(reread=lambda r: dict(r, n_fail=True)), 'n_fail', ''),
    ('reread n_fail "0" (문자열)', dict(reread=lambda r: dict(r, n_fail='0')), 'n_fail', ''),
    ('reread missing 비지 않음 (같음 True 인데)', dict(reread=lambda r: dict(r, missing=[['lhs00_055', 'lhs']])), 'missing', ''),
    ('감사 자격 historical', dict(audit=_aud(eligibility=dict(kind='historical', historical='net194_v12_11fcf91e8', problems=[], note=''))), 'historical', ''),
    ('감사 SEALED_DIRTY_ALLOWED 1 (생산 배포 정책 — 받지 않음)', dict(audit=_aud_rows(_row0(verdict='SEALED_DIRTY_ALLOWED'))), 'SEALED_DIRTY_ALLOWED', ''),
    ('감사 NO_RECORD 1', dict(audit=_aud_rows(_row0(verdict='NO_RECORD', record_status=None, merged='synthesized_failed'))), 'NO_RECORD', ''),
    ('감사 merged differs 1', dict(audit=_aud_rows(_row0(merged='differs'))), 'differs', ''),
    ('감사 input_problems', dict(audit=_aud(input_problems=['입력 지문 raw_sha256_table_sha256: 발사 … ≠ 지금 …'])), 'input_problems', ''),
    ('감사 import_observation_problems', dict(audit=_aud(import_observation_problems=['봉인 밖 모듈을 실제로 읽었다: scripts/coating_presets.py'])),
     'import_observation_problems', ''),
    ('감사 code_root_changed_now', dict(audit=_aud(code_root_changed_now=['scripts/tau_flux.py'])), 'code_root_changed_now', ''),
    ('감사 generation_problems 키 없음 (옛 감사)', dict(audit=lambda a: {k: v for k, v in a.items() if k != 'generation_problems'}), 'generation_problems', ''),
    ('감사 요약 ≠ 행 (행 하나 UNSEALED · 요약은 SEALED 194)', dict(audit=_aud_rows(_row0(verdict='UNSEALED'), summary=False)), '행', ''),
    ('감사 등록 밖 케이스 (행 하나 lhs00_999)', dict(audit=_aud_rows(_row0(case='lhs00_999'), summary=False)), 'production194', ''),
    ('감사 193 행 (요약도 193)', dict(audit=_aud_rows(lambda rows: rows.pop())), '194', ''),
    ('manifest 봉인 지문 ≠ code_hashes 지문 (기록은 그 지문에 결합)', dict(man_edit=lambda m: m['seal'].update(code_fp='e' * 64)), 'code_hashes', ''),
)
#: check_v13 재판정 — Codex 변이 전부 + 감사 없음 · 깨짐 · 다른 배치 뿌리 · 다른 봉인 지문
V17_CHECK = tuple(v for v in V17_VARIANTS if v[3] == 'C') + tuple(v for v in V17_VARIANTS if v[0] in (
    '감사 없음', '감사 깨진 JSON `{`', 'reread 다른 배치 뿌리', '감사 다른 봉인 지문'))
V17_DIAG_RR = (lambda r: {k: v for k, v in dict(r, schema='g2_network_reread/v2').items() if k not in V17_NOID})   # 옛 도구 기록 (진단 모드 대상)


def _put_gate(br, reread, audit):
    """배치 뿌리의 두 기록을 spec 으로 다시 쓴다 (없음이면 지운다)."""
    for n_, spec, good in (('reread.json', reread, rr_bound), ('seal_audit.json', audit, audit_bound)):
        p_ = os.path.join(br, n_)
        if os.path.exists(p_):
            os.remove(p_)
        _write_gate(br, n_, spec, good)


r17 = {}
with tempfile.TemporaryDirectory() as td:
    hd17 = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    ver17 = os.path.join(td, 'go.md')
    open(ver17, 'w', encoding='utf-8').write('# GO (합성)\n')
    if _orig_rr is not None and not is_err(hd17):
        LRB.v13_reread_tau = lambda *a: []
        try:
            #  (a) 양성 대조 — 결합된 통과 기록 둘 → 만들기 · check_v13 문제 0 · 관문 결과 기록
            b_good = make_batch_root(os.path.join(td, 'b_good'))
            r17['b_good_real'] = os.path.realpath(b_good)
            o_good = os.path.join(td, 'o_good')
            r17['good'] = safe(lambda: LRB.build_v13(out_dir=o_good, handover_dir=hd17, batch_root=b_good, date=DATE, codex_verdict=ver17))
            if isinstance(r17['good'], dict):
                r17['good_check'] = safe(lambda: LRB.check_v13(o_good, hd17))
                r17['good_man'] = json.load(open(os.path.join(o_good, 'v13_build_manifest.json'), encoding='utf-8'))
                r17['good_readme'] = open(os.path.join(o_good, 'README.md'), encoding='utf-8').read()
            #  (b) 변이마다 build_v13 거부 · 산출 폴더 없음
            r17['build'] = []
            for i, (nm, kw, tag, cx) in enumerate(V17_VARIANTS):
                b_ = make_batch_root(os.path.join(td, f'b17_{i:02d}'), **kw)
                o_ = os.path.join(td, f'o17_{i:02d}')
                m_ = refusal_msg(lambda: LRB.build_v13(out_dir=o_, handover_dir=hd17, batch_root=b_, date=DATE, codex_verdict=ver17))
                r17['build'].append((i, nm, tag, cx, m_, os.path.exists(o_)))
            #  (c) check_v13 — 좋은 묶음의 배치 증거를 변이로 바꾸면 문제 · 빌드 manifest 기록을 지금 파일에 맞춰 위조해도 문제 (같은 관문을 다시 돈다)
            r17['check'] = []
            if isinstance(r17['good'], dict):
                keep = {n_: open(os.path.join(b_good, n_), 'rb').read() for n_ in ('reread.json', 'seal_audit.json')}
                mp17 = os.path.join(o_good, 'v13_build_manifest.json')
                bak17 = open(mp17, encoding='utf-8').read()
                for i, (nm, kw, tag, cx) in enumerate(V17_CHECK):
                    _put_gate(b_good, kw.get('reread', GOOD), kw.get('audit', GOOD))
                    pc = safe(lambda: LRB.check_v13(o_good, hd17))
                    mj = json.loads(bak17)
                    mj['batch_gate_files'] = safe(lambda: LRB.v13_batch_gate_files(b_good), {})
                    open(mp17, 'w', encoding='utf-8').write(json.dumps(mj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
                    forged = safe(lambda: LRB.check_v13(o_good, hd17))
                    open(mp17, 'w', encoding='utf-8', newline='').write(bak17)
                    for n_, b in keep.items():
                        open(os.path.join(b_good, n_), 'wb').write(b)
                    r17['check'].append((i, nm, cx, pc, forged))
                r17['check_restored'] = safe(lambda: LRB.check_v13(o_good, hd17))
                #  빌드 manifest 에 관문 결과 (batch_gate) 가 없는 묶음 (옛 판 빌드) → 문제
                mj = json.loads(bak17)
                mj.pop('batch_gate', None)
                open(mp17, 'w', encoding='utf-8').write(json.dumps(mj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
                r17['check_nogate'] = safe(lambda: LRB.check_v13(o_good, hd17))
                open(mp17, 'w', encoding='utf-8', newline='').write(bak17)
                #  build · 단계 A · check 가 같은 관문 함수 — 그 함수가 문제를 내면 셋 다 막힌다
                fn0 = getattr(LRB, 'v13_batch_gate_problems', None)
                if fn0 is not None:
                    LRB.v13_batch_gate_problems = lambda br: (fn0(br)[0], ['합성 관문 문제 (같은 함수 시험)'])
                    try:
                        r17['same_build'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o17_same'), handover_dir=hd17, batch_root=b_good,
                                                                              date=DATE, codex_verdict=ver17))
                        r17['same_stage'] = refusal_msg(lambda: LRB.stage_handovers_v13(b_good, os.path.join(td, 'h17_same'), DATE, pressure_unverified=True))
                        r17['same_check'] = safe(lambda: LRB.check_v13(o_good, hd17))
                    finally:
                        LRB.v13_batch_gate_problems = fn0
            #  (d) 배치 뿌리가 사라진 묶음 → check_v13 은 관문을 다시 판정할 수 없다 = 문제
            b_gone = make_batch_root(os.path.join(td, 'b_gone'))
            o_gone = os.path.join(td, 'o_gone')
            if isinstance(safe(lambda: LRB.build_v13(out_dir=o_gone, handover_dir=hd17, batch_root=b_gone, date=DATE, codex_verdict=ver17)), dict):
                shutil.rmtree(b_gone)
                r17['gone'] = safe(lambda: LRB.check_v13(o_gone, hd17))
            #  (e) 진단 모드 — 옛 도구 다시 읽기 기록 (실행 신원 없음) + 감사 없음: 배포 = 거부 · 진단 = 만들고 NOT FOR RELEASE · 배포 대조 거부
            b_dg = make_batch_root(os.path.join(td, 'b_diag'), reread=V17_DIAG_RR, audit=None)
            r17['diag_release'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o_diag_rel'), handover_dir=hd17, batch_root=b_dg, date=DATE,
                                                                    codex_verdict=ver17))
            o_dg = os.path.join(td, 'o_diag')
            r17['diag'] = safe(lambda: LRB.build_v13(out_dir=o_dg, handover_dir=hd17, batch_root=b_dg, date=DATE, codex_verdict=ver17, diagnostic=True))
            if isinstance(r17['diag'], dict):
                r17['diag_readme'] = open(os.path.join(o_dg, 'README.md'), encoding='utf-8').read()
                r17['diag_man'] = json.load(open(os.path.join(o_dg, 'v13_build_manifest.json'), encoding='utf-8'))
                r17['diag_check_rel'] = safe(lambda: LRB.check_v13(o_dg, hd17))
                r17['diag_check_diag'] = safe(lambda: LRB.check_v13(o_dg, hd17, diagnostic=True))
                if isinstance(r17.get('good'), dict):
                    r17['good_check_diag'] = safe(lambda: LRB.check_v13(o_good, hd17, diagnostic=True))
            r17['diag_dry'] = refusal_msg(lambda: LRB.build_v13(out_dir=os.path.join(td, 'o_diag_dry'), handover_dir=V12, date=DATE, dry_run=True,
                                                                diagnostic=True))
            _drepo = os.path.join(ROOT, 'docs', 'data', 'lhs_release_DIAG_test_v13')
            r17['diag_repo'] = refusal_msg(lambda: LRB.build_v13(out_dir=_drepo, handover_dir=hd17, batch_root=b_dg, date=DATE, codex_verdict=ver17,
                                                                 diagnostic=True))
            r17['diag_repo_made'] = os.path.exists(_drepo)
            #  (f) CLI — --diagnostic-batch-gate 가 build · check 까지 간다 · 없으면 배포 경로 (거부)
            o_c1, o_c2 = os.path.join(td, 'o17_cli_diag'), os.path.join(td, 'o17_cli_rel')
            buf17 = io.StringIO()
            with contextlib.redirect_stdout(buf17), contextlib.redirect_stderr(buf17):
                r17['cli_build_rel'] = safe(lambda: LRB.main(['--v13', '--handover-dir', hd17, '--batch-root', b_dg, '--codex-verdict', ver17, '--out-dir', o_c2,
                                                              '--date', DATE]), 99)
                r17['cli_build_diag'] = safe(lambda: LRB.main(['--v13', '--handover-dir', hd17, '--batch-root', b_dg, '--codex-verdict', ver17, '--out-dir', o_c1,
                                                               '--date', DATE, '--diagnostic-batch-gate']), 99)
                r17['cli_check_rel'] = safe(lambda: LRB.main(['--v13-check', '--handover-dir', hd17, '--release-dir', o_c1]), 99)
                r17['cli_check_diag'] = safe(lambda: LRB.main(['--v13-check', '--handover-dir', hd17, '--release-dir', o_c1, '--diagnostic-batch-gate']), 99)
            r17['cli_made'] = (os.path.isfile(os.path.join(o_c1, 'README.md')), os.path.exists(o_c2))
        finally:
            LRB.v13_reread_tau = _orig_rr
    #  (g) 단계 A — 같은 관문이 생성기를 부르기 전에 막는다 (Codex 변이 넷) · 결합된 통과 기록이면 생성기 두 번
    _sp17 = []
    if hasattr(LRB, 'subprocess'):
        _orun17 = LRB.subprocess.run
        LRB.subprocess.run = lambda argv, **kw: (_sp17.append(argv) or _FakeRun()) if '--export-handover' in argv else _orun17(argv, **kw)
        try:
            r17['stage'] = {}
            for j, (nm, kw) in enumerate((('reread 없음', dict(reread=None)), ('reread {}', dict(reread={})), ('감사 없음', dict(audit=None)),
                                          ('감사 refused', dict(audit=V17_REFUSED_AUDIT)))):
                b_ = make_batch_root(os.path.join(td, f'b17_sa{j}'), **kw)
                n0 = len(_sp17)
                m_ = refusal_msg(lambda: LRB.stage_handovers_v13(b_, os.path.join(td, f'h17_sa{j}'), DATE, pressure_unverified=True))
                r17['stage'][nm] = (m_, len(_sp17) - n0)
            b_ = make_batch_root(os.path.join(td, 'b17_sa_ok'))
            n0 = len(_sp17)
            r17['stage_ok'] = (safe(lambda: LRB.stage_handovers_v13(b_, os.path.join(td, 'h17_sa_ok'), DATE, pressure_unverified=True)), len(_sp17) - n0)
        finally:
            LRB.subprocess.run = _orun17

gm17 = r17.get('good_man') or {}
gbg17 = gm17.get('batch_gate') or {}
chk('V17a 양성 대조 — 결합된 통과 기록 (감사 · 다시 읽기) → 만들기 · check_v13 문제 0 · 빌드 manifest 관문 결과 release · 문제 0 · 배치 뿌리 · '
    'README 에 관문 통과 (옛 문구 "실패 표지만 읽는다" 없음)',
    isinstance(r17.get('good'), dict) and r17.get('good_check') == [] and gbg17.get('mode') == 'release' and gbg17.get('problems') == []
    and gbg17.get('batch_root') == r17.get('b_good_real') and '실패 표지만 읽는다' not in (r17.get('good_readme') or '')
    and 'G2RR3-01' in (r17.get('good_readme') or ''), (r17.get('good') if not isinstance(r17.get('good'), dict) else (r17.get('good_check'), gbg17)))
for i, nm, tag, cx, m_, made in r17.get('build', []):
    chk(f'V17b{i:02d} {"[Codex] " if cx else ""}{nm} → build_v13 거부 (메시지에 {tag!r}) · 산출 폴더 없음',
        m_ is not None and not m_.startswith('OTHER') and tag in m_ and not made, (m_ or 'BUILT (거부 없음)')[:400])
if not r17.get('build'):
    chk('V17b (변이 만들기 시험 못 함)', False, r17)
for i, nm, cx, pc, forged in r17.get('check', []):
    chk(f'V17c{i:02d} {"[Codex] " if cx else ""}{nm} — 좋은 묶음의 배치 증거를 이것으로 바꾸면 check_v13 문제 · 빌드 manifest 기록을 지금 파일에 맞춰 '
        '위조해도 문제 (같은 관문을 배치 뿌리에서 다시 판정)',
        isinstance(pc, list) and bool(pc) and isinstance(forged, list) and any('G2RR3-01' in p_ for p_ in forged), (pc, forged))
if not r17.get('check'):
    chk('V17c (재판정 시험 못 함 — 좋은 묶음 없음)', False, r17.get('good'))
chk('V17d 되돌린 뒤 check_v13 문제 0 · 빌드 manifest 에 관문 결과 (batch_gate) 가 없으면 문제 · 배치 뿌리가 사라지면 문제',
    r17.get('check_restored') == [] and isinstance(r17.get('check_nogate'), list) and any('batch_gate' in p_ for p_ in r17['check_nogate'])
    and isinstance(r17.get('gone'), list) and any('배치 뿌리' in p_ for p_ in r17['gone']),
    (r17.get('check_restored'), r17.get('check_nogate'), r17.get('gone')))
chk('V17e build_v13 · 단계 A · check_v13 이 같은 관문 함수 (v13_batch_gate_problems) — 그 함수가 문제를 내면 셋 다 거부 · 문제',
    all(isinstance(r17.get(k), str) and '합성 관문 문제' in r17[k] for k in ('same_build', 'same_stage'))
    and isinstance(r17.get('same_check'), list) and any('합성 관문 문제' in p_ for p_ in r17['same_check']),
    {k: r17.get(k) for k in ('same_build', 'same_stage', 'same_check')})
dm17 = r17.get('diag_man') or {}
dbg17 = dm17.get('batch_gate') or {}
chk('V17f 진단 모드 — 옛 도구 다시 읽기 기록 + 감사 없음: 배포 만들기 거부 · --diagnostic-batch-gate 면 만든다 (README 첫 줄 NOT FOR RELEASE · manifest '
    'diagnostic true · 관문 모드 diagnostic · 문제 기록 · 경고)',
    isinstance(r17.get('diag_release'), str) and 'seal_audit.json' in r17['diag_release'] and isinstance(r17.get('diag'), dict)
    and 'NOT FOR RELEASE' in ((r17.get('diag_readme') or '').splitlines() or [''])[0] and dm17.get('diagnostic') is True
    and dbg17.get('mode') == 'diagnostic' and any('seal_audit.json' in p_ for p_ in dbg17.get('problems') or [])
    and any('reread.json' in p_ for p_ in dbg17.get('problems') or []) and any('NOT FOR RELEASE' in w for w in r17['diag'].get('warnings', [])),
    (r17.get('diag_release'), r17.get('diag') if not isinstance(r17.get('diag'), dict) else dbg17))
chk('V17g 진단 묶음 — check_v13 배포 대조 = 문제 (NOT FOR RELEASE) · 진단 대조 = 문제 0 · 배포 묶음을 진단으로 대조 = 모드 다름 문제',
    isinstance(r17.get('diag_check_rel'), list) and any('NOT FOR RELEASE' in p_ for p_ in r17['diag_check_rel']) and r17.get('diag_check_diag') == []
    and isinstance(r17.get('good_check_diag'), list) and bool(r17['good_check_diag']),
    (r17.get('diag_check_rel'), r17.get('diag_check_diag'), r17.get('good_check_diag')))
chk('V17h 진단 모드는 실제 경로에만 (dry-run 과 함께 = 거부) · 산출을 리포 안 (docs/data) 에 = 거부 · 폴더 안 만듦',
    isinstance(r17.get('diag_dry'), str) and not r17['diag_dry'].startswith('OTHER') and isinstance(r17.get('diag_repo'), str)
    and not r17['diag_repo'].startswith('OTHER') and r17.get('diag_repo_made') is False, (r17.get('diag_dry'), r17.get('diag_repo')))
chk('V17i CLI — 옛 · 부분 기록으로 --v13 (표지 없음) = rc ≠ 0 · 폴더 없음 / --diagnostic-batch-gate = rc 0 · 산출 / --v13-check (배포) = rc ≠ 0 · '
    '--v13-check --diagnostic-batch-gate = rc 0',
    r17.get('cli_build_rel') not in (0, 99, None) and r17.get('cli_build_diag') == 0 and r17.get('cli_check_rel') not in (0, 99, None)
    and r17.get('cli_check_diag') == 0 and r17.get('cli_made') == (True, False),
    ({k: r17.get(k) for k in ('cli_build_rel', 'cli_build_diag', 'cli_check_rel', 'cli_check_diag', 'cli_made')},
     buf17.getvalue()[-400:] if 'buf17' in dir() else ''))
st17 = r17.get('stage') or {}
chk('V17j 단계 A — reread 없음 · {} · 감사 없음 · 감사 refused → 생성기를 부르기 전에 거부 · 결합된 통과 기록이면 생성기 두 번',
    len(st17) == 4 and all(m_ is not None and not m_.startswith('OTHER') and n_ == 0 for m_, n_ in st17.values())
    and not is_err((r17.get('stage_ok') or (('ERR', ''), 0))[0]) and (r17.get('stage_ok') or (None, 0))[1] == 2,
    ({k: ((m_ or '')[:120], n_) for k, (m_, n_) in st17.items()}, r17.get('stage_ok')))
chk('V17k 생산 배포 정책 — 받는 봉인 판정 = SEALED 만 (SEALED_DIRTY_ALLOWED · SEALED_LEGACY 는 실행기 audit rc 0 이어도 배포 아님) · 실행기 SEAL_OK 의 부분집합',
    tuple(getattr(LRB, 'V13_AUDIT_SEALED', ())) == ('SEALED',) and set(getattr(LRB, 'V13_AUDIT_SEALED', ('x',))) <= set(NP194.SEAL_OK),
    getattr(LRB, 'V13_AUDIT_SEALED', None))

# ═══ V18 ★ 10-07 G2RR4-01 — 다시 읽기 상세 ↔ 요약 · 감사 관측 내부 ↔ 최상위 · 관측 필수 (build · check) ═══════════════════════════════════════════
#   Codex 세대 2 재검증 4 §2 (`docs/reviews/codex_review_gen2_network_reverify4_20261007.md` · 탐침 release_gate.py) — 옛 관문은 다시 읽기의 요약 (n_fail ·
#   집합 칸 · 신원) 만 읽고 meta · cases 를 읽지 않았다: meta M2 ok=false (n_fail 0 유지) · cases=[] · meta=[] (read_n 194 유지) · 감사 내부 관측 실패 (최상위 [])
#   에서 실제 build_v13 이 묶음을 만들고 check_v13 문제 0.  [C] = Codex 변이 그대로 · 나머지 = 같은 부류 (반례 먼저 — 옛 코드에서 이 시험들이 FAIL).
print('V18 다시 읽기 상세 ↔ 요약 · 감사 관측 (G2RR4-01)')


def _rr_mut(fn):
    """다시 읽기 통과 기록 (상세 포함) 을 깊은 사본으로 바꾸는 변이 — fn(rec) 가 그 자리를 고친다."""
    def f(r):
        r = json.loads(json.dumps(r))
        fn(r)
        return r
    return f


def _meta_ok(prefix, ok):
    return lambda r: next(m for m in r['meta'] if m['name'].startswith(prefix)).update(ok=ok)


def _case_check(i, cid, **kv):
    return lambda r: next(c for c in r['cases'][i]['checks'] if c['name'].startswith(cid + ' ')).update(**kv)


def _codex_shape(r):
    """Codex 탐침의 정상 대조 모양 (release_gate.py) — meta 한 줄 · 케이스마다 K1 하나 (생산자 계약의 검사 ID 결손)."""
    r['meta'] = [dict(name='M2 all completed', ok=True, detail='synthetic gate-only fixture')]
    r['cases'] = [dict(case=c, cohort=h, checks=[dict(name='K1', ok=True, detail='synthetic gate-only fixture')]) for c, h in PROD194]


def _dup_case(r):
    r['cases'][1] = json.loads(json.dumps(r['cases'][0]))


def _wrong_cohort(r):
    r['cases'][0]['cohort'] = 'lhsx'


def _drop_meta(prefix):
    return lambda r: r.__setitem__('meta', [m for m in r['meta'] if not m['name'].startswith(prefix)])


def _obs_mut(**over):
    return lambda a: dict(a, import_observation=dict(a['import_observation'], **over))


V18_VARIANTS = (
    #  (이름, make_batch_root 인자, 거부 메시지에 있어야 할 꼬리표, Codex 변이 표지)
    ('reread meta M2 lhs ok=false · n_fail 0 유지 (상세 명시 실패 ↔ 성공 요약)', dict(reread=_rr_mut(_meta_ok('M2 lhs', False))), 'G2RR4-01', 'C'),
    ('reread cases=[] · meta=[] · read_n 194 · set_equal 유지 (상세 결손)', dict(reread=_rr_mut(lambda r: r.update(cases=[], meta=[]))), 'G2RR4-01', 'C'),
    ('감사 import_observation = {problems: [log truncated] · outside: [scripts/unsealed.py]} (Codex 모양 그대로 · 최상위 import_observation_problems [] 유지)',
     dict(audit=lambda a: dict(a, import_observation={'problems': ['log truncated'], 'outside': ['scripts/unsealed.py']})), 'G2RR4-01', 'C'),
    ('감사 import_observation 내부 problems · outside 만 (다른 칸 정상 · 최상위 [] 유지)',
     dict(audit=_obs_mut(problems=['log truncated'], outside=['scripts/unsealed.py'])), 'G2RR4-01', ''),
    ('reread Codex 탐침 정상 대조 모양 (meta 한 줄 · 케이스마다 K1 하나 — 검사 ID 결손)', dict(reread=_rr_mut(_codex_shape)), 'G2RR4-01', 'C'),
    ('reread 케이스 checks 전부 [] (빈 checks 공집합 PASS)', dict(reread=_rr_mut(lambda r: [c.update(checks=[]) for c in r['cases']])), 'K1', ''),
    ('reread 케이스 하나 K4 빠짐', dict(reread=_rr_mut(lambda r: r['cases'][5].update(checks=[c for c in r['cases'][5]['checks'] if not c['name'].startswith('K4 ')]))),
     'K4', ''),
    ('reread 케이스 검사 ok "True" (문자열)', dict(reread=_rr_mut(_case_check(3, 'K2', ok='True'))), 'bool', ''),
    ('reread 케이스 검사 ok false · n_fail 0 유지', dict(reread=_rr_mut(_case_check(7, 'K6', ok=False))), 'G2RR4-01', ''),
    ('reread 케이스 중복 (한 케이스 두 번 · 다른 하나 빠짐 · 194 행)', dict(reread=_rr_mut(_dup_case)), '중복', ''),
    ('reread 케이스 193 (read_n 194 유지)', dict(reread=_rr_mut(lambda r: r['cases'].pop())), 'read_n', ''),
    ('reread 케이스 코호트 틀림 (lhs 케이스를 lhsx 로)', dict(reread=_rr_mut(_wrong_cohort)), 'production194', ''),
    ('reread meta H1 lhsx 빠짐', dict(reread=_rr_mut(_drop_meta('H1 lhsx'))), 'H1', ''),
    ('reread meta 모르는 검사 Z9', dict(reread=_rr_mut(lambda r: r['meta'].insert(0, dict(name='Z9 합성 검사', ok=True, detail='')))), 'Z9', ''),
    ('reread meta M3 read_n 193 (최상위 194)', dict(reread=_rr_mut(lambda r: r['meta'][-1].update(read_n=193))), 'M3', ''),
    ('reread meta 항목 ok 1 (정수)', dict(reread=_rr_mut(_meta_ok('M0', 1))), 'bool', ''),
    ('reread meta 가 목록이 아님 ({})', dict(reread=_rr_mut(lambda r: r.update(meta={}))), 'meta', ''),
    ('reread n_fail 1 인데 상세 실패 0 (재계수 ≠ n_fail)', dict(reread=_rr_mut(lambda r: r.update(n_fail=1))), '재계수', ''),
    ('manifest observe_imports false (관측 끈 생산 배치)', dict(man_edit=lambda m: m.update(observe_imports=False)), 'observe_imports', ''),
    ('감사 import_observation null (관측 객체 없음)', dict(audit=lambda a: dict(a, import_observation=None)), 'import_observation', ''),
    ('감사 관측 완료 시도 193 케이스 (하나 빠짐)', dict(audit=_obs_mut(completed_attempts=obs_bound()['completed_attempts'][1:])), 'completed_attempts', ''),
    ('감사 관측 n_processes 0 (기록 없음)', dict(audit=_obs_mut(n_processes=0, n_started=0, n_finalized=0)), 'n_processes', ''),
    ('감사 관측 problems 가 목록이 아님 (null)', dict(audit=_obs_mut(problems=None)), 'problems', ''),
)
#: check_v13 재판정 — Codex 변이 넷 + 같은 부류 둘
V18_CHECK = tuple(v for v in V18_VARIANTS if v[3] == 'C') + tuple(v for v in V18_VARIANTS if v[0] in (
    'reread 케이스 checks 전부 [] (빈 checks 공집합 PASS)', 'manifest observe_imports false (관측 끈 생산 배치)'))

r18 = {}
with tempfile.TemporaryDirectory() as td:
    hd18 = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    ver18 = os.path.join(td, 'go.md')
    open(ver18, 'w', encoding='utf-8').write('# GO (합성)\n')
    if _orig_rr is not None and not is_err(hd18):
        LRB.v13_reread_tau = lambda *a: []
        try:
            #  (a) 양성 대조 — 상세 꼴 그대로의 통과 기록 둘 → 만들기 · check_v13 문제 0
            b_ok = make_batch_root(os.path.join(td, 'b18_ok'))
            o_ok = os.path.join(td, 'o18_ok')
            r18['good'] = safe(lambda: LRB.build_v13(out_dir=o_ok, handover_dir=hd18, batch_root=b_ok, date=DATE, codex_verdict=ver18))
            if isinstance(r18['good'], dict):
                r18['good_check'] = safe(lambda: LRB.check_v13(o_ok, hd18))
            r18['good_rr_probs'] = safe(lambda: LRB.v13_reread_problems(json.load(open(os.path.join(b_ok, 'reread.json'), encoding='utf-8')), b_ok))
            r18['good_au_probs'] = safe(lambda: LRB.v13_audit_problems(json.load(open(os.path.join(b_ok, 'seal_audit.json'), encoding='utf-8')), b_ok))
            #  (b) 변이마다 build_v13 거부 · 산출 폴더 없음
            r18['build'] = []
            for i, (nm, kw, tag, cx) in enumerate(V18_VARIANTS):
                b_ = make_batch_root(os.path.join(td, f'b18_{i:02d}'), **kw)
                o_ = os.path.join(td, f'o18_{i:02d}')
                m_ = refusal_msg(lambda: LRB.build_v13(out_dir=o_, handover_dir=hd18, batch_root=b_, date=DATE, codex_verdict=ver18))
                r18['build'].append((i, nm, tag, cx, m_, os.path.exists(o_)))
            #  (c) check_v13 — 좋은 묶음의 배치 증거를 변이로 바꾸면 문제 · 빌드 manifest 기록을 지금 파일에 맞춰 위조해도 문제
            r18['check'] = []
            if isinstance(r18['good'], dict):
                keep = {n_: open(os.path.join(b_ok, n_), 'rb').read() for n_ in ('reread.json', 'seal_audit.json', 'manifest.json')}
                mp18 = os.path.join(o_ok, 'v13_build_manifest.json')
                bak18 = open(mp18, encoding='utf-8').read()
                for i, (nm, kw, tag, cx) in enumerate(V18_CHECK):
                    if kw.get('man_edit'):
                        mj_ = json.loads(keep['manifest.json'])
                        kw['man_edit'](mj_)
                        open(os.path.join(b_ok, 'manifest.json'), 'w', encoding='utf-8').write(json.dumps(mj_))
                    _put_gate(b_ok, kw.get('reread', GOOD), kw.get('audit', GOOD))
                    pc = safe(lambda: LRB.check_v13(o_ok, hd18))
                    mj = json.loads(bak18)
                    mj['batch_gate_files'] = safe(lambda: LRB.v13_batch_gate_files(b_ok), {})
                    open(mp18, 'w', encoding='utf-8').write(json.dumps(mj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
                    forged = safe(lambda: LRB.check_v13(o_ok, hd18))
                    open(mp18, 'w', encoding='utf-8', newline='').write(bak18)
                    for n_, b in keep.items():
                        open(os.path.join(b_ok, n_), 'wb').write(b)
                    r18['check'].append((i, nm, tag, cx, pc, forged))
                r18['check_restored'] = safe(lambda: LRB.check_v13(o_ok, hd18))
        finally:
            LRB.v13_reread_tau = _orig_rr

chk('V18a 양성 대조 — 상세 꼴 그대로의 통과 기록 (meta 열 · 194 케이스 K1–K7 · 감사 관측 객체 · observe_imports) → 만들기 · check_v13 문제 0 · '
    '다시 읽기 · 감사 판정 함수 문제 0',
    isinstance(r18.get('good'), dict) and r18.get('good_check') == [] and r18.get('good_rr_probs') == [] and r18.get('good_au_probs') == [],
    (r18.get('good') if not isinstance(r18.get('good'), dict) else (r18.get('good_check'), r18.get('good_rr_probs'), r18.get('good_au_probs'))))
for i, nm, tag, cx, m_, made in r18.get('build', []):
    chk(f'V18b{i:02d} {"[Codex] " if cx else ""}{nm} → build_v13 거부 (메시지에 {tag!r}) · 산출 폴더 없음',
        m_ is not None and not m_.startswith('OTHER') and tag in m_ and not made, (m_ or 'BUILT (거부 없음)')[:400])
if not r18.get('build'):
    chk('V18b (변이 만들기 시험 못 함)', False, r18)
for i, nm, tag, cx, pc, forged in r18.get('check', []):
    chk(f'V18c{i:02d} {"[Codex] " if cx else ""}{nm} — 좋은 묶음의 배치 증거를 이것으로 바꾸면 check_v13 문제 · 빌드 manifest 기록을 지금 파일에 맞춰 '
        f'위조해도 문제 (같은 관문을 배치 뿌리에서 다시 판정 · 문제에 {tag!r})',
        isinstance(pc, list) and bool(pc) and isinstance(forged, list) and any(tag in p_ for p_ in forged), (pc, forged))
if not r18.get('check'):
    chk('V18c (재판정 시험 못 함 — 좋은 묶음 없음)', False, r18.get('good'))
chk('V18d 되돌린 뒤 check_v13 문제 0', r18.get('check_restored') == [], r18.get('check_restored'))
_dp = getattr(G2RR, 'launcher_detail_problems', None)
chk('V18e 다시 읽기 상세 계약은 생산자 쪽 한 함수 (g2_network_reread.launcher_detail_problems) — 생산자 꼴 = 문제 0 · cases=[] = 문제 · 배포 관문 생산 194 = 관측 필수 표',
    callable(_dp) and _dp(dict(RR_OK, meta=rr_detail()[0], cases=rr_detail()[1]), frozenset(PROD194)) == []
    and bool(_dp(dict(RR_OK, meta=rr_detail()[0], cases=[]), frozenset(PROD194)))
    and 'production194' in (getattr(LRB, 'V13_IMPORT_OBS_REQUIRED', None) or ()),
    (callable(_dp), getattr(LRB, 'V13_IMPORT_OBS_REQUIRED', None)))

# ═══ V19 ★ 10-07 G2RR4-02 — 생산 194 배포 = 실행 단계 ↔ 관측 영수증 결합을 한 감사만 (import_observation.stage_binding) ═══════════════════════════════
#   Codex 세대 2 재검증 4 §3 — 보조 단계 영수증 쌍 결손을 실행기 audit 가 못 봤다.  실행기가 완료 시도마다 단계 계획 ↔ 끝맺은 프로세스를 결합하고 그 기록을 감사에
#   싣는다 → 배포 관문은 그 결합 기록 (스키마 · 시도 = 관측된 완료 시도 · 등록 케이스 전부) 이 없는 감사를 받지 않는다 (결합 전 실행기의 감사 = 거부).
print('V19 감사의 실행 단계 ↔ 영수증 결합 기록 (G2RR4-02)')


def _sb_mut(fn):
    def f(a):
        a = json.loads(json.dumps(a))
        fn(a['import_observation'])
        return a
    return f


def _sb_drop_one(io_):
    k_ = sorted(io_['stage_binding']['attempts'])[0]
    io_['stage_binding']['attempts'].pop(k_)


def _sb_rekey(io_):
    k_ = sorted(io_['stage_binding']['attempts'])[0]
    c_ = k_.split('|')[0]
    io_['stage_binding']['attempts'][f'{c_}|2|2'] = io_['stage_binding']['attempts'].pop(k_)


V19_VARIANTS = (
    ('감사 관측에 stage_binding 없음 (결합 전 실행기의 감사)', dict(audit=_sb_mut(lambda io_: io_.pop('stage_binding'))), 'stage_binding'),
    ('stage_binding 스키마 다름', dict(audit=_sb_mut(lambda io_: io_['stage_binding'].update(schema='np194_import_obs/stage_binding/v0'))), 'stage_binding'),
    ('stage_binding 시도 하나 빠짐 (193 · completed_attempts 194 그대로)', dict(audit=_sb_mut(_sb_drop_one)), 'stage_binding'),
    ('stage_binding 시도 열쇠 ≠ completed_attempts (한 케이스를 run 2 · 시도 2 로)', dict(audit=_sb_mut(_sb_rekey)), 'stage_binding'),
    ('stage_binding attempts 가 dict 가 아님 ([])', dict(audit=_sb_mut(lambda io_: io_['stage_binding'].update(attempts=[]))), 'stage_binding'),
)
r19 = {}
with tempfile.TemporaryDirectory() as td:
    hd19 = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    ver19 = os.path.join(td, 'go.md')
    open(ver19, 'w', encoding='utf-8').write('# GO (합성)\n')
    if _orig_rr is not None and not is_err(hd19):
        LRB.v13_reread_tau = lambda *a: []
        try:
            r19['build'] = []
            for i, (nm, kw, tag) in enumerate(V19_VARIANTS):
                b_ = make_batch_root(os.path.join(td, f'b19_{i:02d}'), **kw)
                o_ = os.path.join(td, f'o19_{i:02d}')
                m_ = refusal_msg(lambda: LRB.build_v13(out_dir=o_, handover_dir=hd19, batch_root=b_, date=DATE, codex_verdict=ver19))
                r19['build'].append((i, nm, tag, m_, os.path.exists(o_)))
            b_g = make_batch_root(os.path.join(td, 'b19_good'))
            r19['good_au'] = safe(lambda: LRB.v13_audit_problems(json.load(open(os.path.join(b_g, 'seal_audit.json'), encoding='utf-8')), b_g))
        finally:
            LRB.v13_reread_tau = _orig_rr
for i, nm, tag, m_, made in r19.get('build', []):
    chk(f'V19a{i:02d} {nm} → build_v13 거부 (메시지에 {tag!r}) · 산출 폴더 없음',
        m_ is not None and not m_.startswith('OTHER') and tag in m_ and not made, (m_ or 'BUILT (거부 없음)')[:400])
if not r19.get('build'):
    chk('V19a (변이 만들기 시험 못 함)', False, r19)
chk('V19b 결합 기록이 있는 감사 (스키마 = 실행기 IMPORT_OBS_STAGE_SCHEMA · 시도 = 완료 시도 194) → 감사 판정 문제 0',
    r19.get('good_au') == [] and getattr(NP194, 'IMPORT_OBS_STAGE_SCHEMA', None) == 'np194_import_obs/stage_binding/v1', r19.get('good_au'))

# ═══ V20 ★ 10-08 G2RR5-01 — 배포 관문이 stage_binding 의 시도별 값 · 합계를 읽는다 (build · check) ═══════════════════════════════════════════
#   Codex 세대 2 재검증 5 §1 (`docs/reviews/codex_review_gen2_network_reverify5_20261007.md` · 탐침 r5_release_contract.py · r5_release_real_binding.py) —
#   옛 관문은 stage_binding 의 스키마 · attempts 가 dict 인지 · 키 집합 = 관측된 완료 시도만 봤다: 시도 값이 null · parser 결손 · parser 0 · 계획 밖 프로세스 ·
#   bool 개수 · n_finalized 0 이어도, 실제 audit CLI 가 낸 실패 binding 에서 최상위 요약 목록 하나만 [] 로 바꿔도 build_v13 이 묶음을 만들고 check_v13 문제 0.
#   변이 = 상세 production194 정상 픽스처 (obs_bound) 위 감사 JSON 만 · [C] = Codex 변이 그대로 · c = 재시도 이력 (과잉차단 금지 — 전체 started = finalized 를
#   요구하지 않는다 · 판정문 §1 · §4 · Q2).  check 쪽 = V17c · V18c 꼴 (좋은 묶음의 감사를 바꿔 다시 판정 + 빌드 manifest 의 캐시 sha256 을 지금 파일에 맞춘 위조).
print('V20 감사 stage_binding 시도별 값 · 합계 (G2RR5-01)')

#: 실제 audit CLI (Codex r5_observation · 한 케이스 합성 감사 · parser 시작 · 끝 영수증 쌍 삭제 · rc 1) 가 낸 감사 JSON — 리포에 커밋된 증거 (읽기만)
V20_REAL_AUDIT = os.path.join(ROOT, 'docs', 'reviews', 'codex_gen2_network_reverify5_evidence_20261007', 'evidence', 'r5_observation_run2',
                              'pair_missing_parse_liggghts', 'audit.json')


def _v20_first(fn):
    """감사 통과 기록 (깊은 사본) 의 첫 결합 시도 (열쇠 순서 첫째) 를 fn(attempts, 열쇠) 로 고치는 변이."""
    def f(a):
        a = json.loads(json.dumps(a))
        at_ = a['import_observation']['stage_binding']['attempts']
        fn(at_, next(iter(at_)))
        return a
    return f


def _v20_real():
    """실제 실패 감사 → (원 열쇠, 실패 binding, 최상위 문제 목록)."""
    real = json.load(open(V20_REAL_AUDIT, encoding='utf-8'))
    k0, bad = next(iter(real['import_observation']['stage_binding']['attempts'].items()))
    return k0, bad, real['import_observation_problems']


def _v20_graft(keep_top):
    """실제 실패 binding 을 첫 결합 시도 자리에 이식 (Codex r5_release_real_binding 과 같은 꼴) — keep_top 이면 그 감사의 최상위 문제 목록도
    (케이스 이름만 바꿔) 싣고, 아니면 최상위 목록 하나만 [] (요약이 상세와 모순)."""
    def f(a):
        a = json.loads(json.dumps(a))
        k0, bad, top = _v20_real()
        at_ = a['import_observation']['stage_binding']['attempts']
        k_ = next(iter(at_))
        at_[k_] = bad
        c0, c_ = k0.split('|')[0], k_.split('|')[0]
        a['import_observation_problems'] = [s.replace(c0, c_) for s in top] if keep_top else []
        return a
    return f


def _v20_retry(a):
    """재시도 이력 (Q2 · 판정문 §4 표) — 한 케이스에 완료 시도 둘 (run 1 · 시도 1 + run 2 · 시도 2 · 둘 다 결합 · expected = observed) + 죽은 시도
    (run 3 · 시도 3) 의 미최종 시작 영수증 하나 (정보) → n_started = n_processes > n_finalized = Σ observed."""
    a = json.loads(json.dumps(a))
    io_ = a['import_observation']
    at_ = io_['stage_binding']['attempts']
    k_ = next(iter(at_))
    c_ = k_.split('|')[0]
    at_[f'{c_}|2|2'] = json.loads(json.dumps(at_[k_]))
    io_['completed_attempts'] = sorted(io_['completed_attempts'] + [[c_, '2', '2']])
    io_['unfinalized_noncompleted'] = [dict(proc='4242-0badc0de', case=c_, run='3', attempt='3')]
    n_ = sum(sum(b_['observed'].values()) for b_ in at_.values())
    io_.update(n_processes=n_ + 1, n_started=n_ + 1, n_finalized=n_)
    return a


V20_PARSER = 'scripts/parse_liggghts.py'
V20_VARIANTS = (
    #  (ID, 이름, make_batch_root 인자, 거부 메시지 · check 문제에 있어야 할 꼬리표, Codex 변이 표지)
    ('a00', '첫 시도 binding 값 = null', dict(audit=_v20_first(lambda at_, k_: at_.__setitem__(k_, None))), 'G2RR5-01', 'C'),
    ('a01', 'expected parser 1 · observed parser 키 삭제', dict(audit=_v20_first(lambda at_, k_: at_[k_]['observed'].pop(V20_PARSER))), 'G2RR5-01', 'C'),
    ('a02', 'observed parser = 0', dict(audit=_v20_first(lambda at_, k_: at_[k_]['observed'].__setitem__(V20_PARSER, 0))), 'G2RR5-01', 'C'),
    ('a03', "observed 에 계획 밖 'scripts/unplanned.py': 1", dict(audit=_v20_first(lambda at_, k_: at_[k_]['observed'].__setitem__('scripts/unplanned.py', 1))),
     'G2RR5-01', 'C'),
    ('a04', 'observed parser = True (bool)', dict(audit=_v20_first(lambda at_, k_: at_[k_]['observed'].__setitem__(V20_PARSER, True))), 'G2RR5-01', 'C'),
    ('a05', 'n_finalized = 0 (binding 그대로)', dict(audit=_obs_mut(n_finalized=0)), 'G2RR5-01', 'C'),
    ('a06', 'expected 에서 parser 삭제 (executed 에는 parser 그대로 — 상세 자기모순)', dict(audit=_v20_first(lambda at_, k_: at_[k_]['expected'].pop(V20_PARSER))),
     'G2RR5-01', ''),
    ('a07', '실제 audit CLI 실패 binding (expected parser 1 · observed 없음) + 최상위 목록 [] (요약만 비움)', dict(audit=_v20_graft(False)), 'G2RR5-01', 'C'),
    ('a08', '같은 실패 binding + 최상위 목록 유지 (회귀 — 지금도 거부)', dict(audit=_v20_graft(True)), 'import_observation_problems', 'C'),
)

r20 = {}
with tempfile.TemporaryDirectory() as td:
    hd20 = safe(lambda: make_g2_handover_dir(os.path.join(td, 'handover')))
    ver20 = os.path.join(td, 'go.md')
    open(ver20, 'w', encoding='utf-8').write('# GO (합성)\n')
    if _orig_rr is not None and not is_err(hd20):
        LRB.v13_reread_tau = lambda *a: []
        try:
            #  (b) 정상 대조 — 상세 194 · 시도마다 expected = observed → 만들기 · check_v13 문제 0
            b_ok = make_batch_root(os.path.join(td, 'b20_ok'))
            o_ok = os.path.join(td, 'o20_ok')
            r20['good'] = safe(lambda: LRB.build_v13(out_dir=o_ok, handover_dir=hd20, batch_root=b_ok, date=DATE, codex_verdict=ver20))
            if isinstance(r20['good'], dict):
                r20['good_check'] = safe(lambda: LRB.check_v13(o_ok, hd20))
            #  (c) 재시도 이력 → 만들기 · check_v13 문제 0 (과잉차단 금지)
            b_rt = make_batch_root(os.path.join(td, 'b20_retry'), audit=_v20_retry)
            o_rt = os.path.join(td, 'o20_retry')
            r20['retry_io'] = {k_: (json.load(open(os.path.join(b_rt, 'seal_audit.json'), encoding='utf-8'))['import_observation'] or {}).get(k_)
                               for k_ in ('n_processes', 'n_started', 'n_finalized')}
            r20['retry'] = safe(lambda: LRB.build_v13(out_dir=o_rt, handover_dir=hd20, batch_root=b_rt, date=DATE, codex_verdict=ver20))
            if isinstance(r20['retry'], dict):
                r20['retry_check'] = safe(lambda: LRB.check_v13(o_rt, hd20))
            #  (a) 변이마다 build_v13 거부 · 산출 폴더 없음
            r20['build'] = []
            for vid, nm, kw, tag, cx in V20_VARIANTS:
                b_ = make_batch_root(os.path.join(td, f'b20_{vid}'), **kw)
                o_ = os.path.join(td, f'o20_{vid}')
                m_ = refusal_msg(lambda: LRB.build_v13(out_dir=o_, handover_dir=hd20, batch_root=b_, date=DATE, codex_verdict=ver20))
                r20['build'].append((vid, nm, tag, cx, m_, os.path.exists(o_)))
            #  (a') check_v13 — 좋은 묶음의 감사를 변이로 바꾸면 문제 · 빌드 manifest 의 기록 (캐시 sha256) 을 지금 파일에 맞춰 위조해도 문제 (같은 관문을 다시 돈다)
            r20['check'] = []
            if isinstance(r20['good'], dict):
                keep = {n_: open(os.path.join(b_ok, n_), 'rb').read() for n_ in ('reread.json', 'seal_audit.json', 'manifest.json')}
                mp20 = os.path.join(o_ok, 'v13_build_manifest.json')
                bak20 = open(mp20, encoding='utf-8').read()
                for vid, nm, kw, tag, cx in V20_VARIANTS:
                    _put_gate(b_ok, kw.get('reread', GOOD), kw.get('audit', GOOD))
                    pc = safe(lambda: LRB.check_v13(o_ok, hd20))
                    mj = json.loads(bak20)
                    mj['batch_gate_files'] = safe(lambda: LRB.v13_batch_gate_files(b_ok), {})
                    open(mp20, 'w', encoding='utf-8').write(json.dumps(mj, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
                    forged = safe(lambda: LRB.check_v13(o_ok, hd20))
                    open(mp20, 'w', encoding='utf-8', newline='').write(bak20)
                    for n_, b in keep.items():
                        open(os.path.join(b_ok, n_), 'wb').write(b)
                    r20['check'].append((vid, nm, tag, cx, pc, forged))
                r20['check_restored'] = safe(lambda: LRB.check_v13(o_ok, hd20))
            #  (e) 배포 관문이 실행기의 한 함수를 부른다 — 그 함수 (대역) 가 문제를 내면 감사 관측 판정에 그 문제가 실린다
            _f0 = getattr(NP194, 'stage_binding_record_problems', None)
            if _f0 is not None:
                NP194.stage_binding_record_problems = lambda k_, rec_: ['합성 시도 계약 문제 (같은 함수 시험)']
                try:
                    r20['same_fn'] = safe(lambda: LRB.v13_audit_observation_problems(
                        json.load(open(os.path.join(b_ok, 'seal_audit.json'), encoding='utf-8')), {'observe_imports': True}))
                finally:
                    NP194.stage_binding_record_problems = _f0
        finally:
            LRB.v13_reread_tau = _orig_rr

chk('V20b 정상 대조 — 상세 194 · 시도마다 expected = observed (생산자 계약 꼴) → 만들기 · check_v13 문제 0',
    isinstance(r20.get('good'), dict) and r20.get('good_check') == [],
    (r20.get('good') if not isinstance(r20.get('good'), dict) else r20.get('good_check')))
_rio = r20.get('retry_io') or {}
chk('V20c 재시도 이력 (한 케이스 완료 시도 2 · 결합 2 · 죽은 시도의 미최종 시작 영수증 1 → n_started > n_finalized) → 만들기 · check_v13 문제 0 '
    '(과잉차단 금지 — 판정문 §1 · Q2)',
    isinstance(r20.get('retry'), dict) and r20.get('retry_check') == [] and isinstance(_rio.get('n_started'), int)
    and _rio['n_started'] > (_rio.get('n_finalized') or 0),
    (_rio, r20.get('retry') if not isinstance(r20.get('retry'), dict) else r20.get('retry_check')))
for vid, nm, tag, cx, m_, made in r20.get('build', []):
    chk(f'V20{vid} [build] {"[Codex] " if cx else ""}{nm} → build_v13 거부 (메시지에 {tag!r}) · 산출 폴더 없음',
        m_ is not None and not m_.startswith('OTHER') and tag in m_ and not made, (m_ or 'BUILT (거부 없음)')[:400])
if not r20.get('build'):
    chk('V20a (변이 만들기 시험 못 함)', False, r20)
for vid, nm, tag, cx, pc, forged in r20.get('check', []):
    chk(f'V20{vid} [check] {"[Codex] " if cx else ""}{nm} — 좋은 묶음의 감사를 이것으로 바꾸면 check_v13 문제 · 빌드 manifest 기록을 지금 파일에 맞춰 '
        f'위조해도 문제 (같은 관문을 배치 뿌리에서 다시 판정 · 문제에 {tag!r})',
        isinstance(pc, list) and bool(pc) and isinstance(forged, list) and any(tag in p_ for p_ in forged), (pc, forged))
if not r20.get('check'):
    chk('V20a (재판정 시험 못 함 — 좋은 묶음 없음)', False, r20.get('good'))
chk('V20d 되돌린 뒤 check_v13 문제 0', r20.get('check_restored') == [], r20.get('check_restored'))
_sbp = getattr(NP194, 'stage_binding_record_problems', None)
_v20k, _v20bad, _v20top = safe(_v20_real, (None, None, None))
_v20ok = obs_bound()['stage_binding']['attempts']
chk('V20e 시도 값 계약 = 실행기 한 함수 (run_network_194_parallel.stage_binding_record_problems) — 픽스처 정상 시도 194 = 문제 0 · 실제 audit CLI 실패 '
    'binding = 문제 · 배포 관문 (v13_audit_observation_problems) 이 그 함수를 부른다 (대역이 낸 문제가 판정에 실린다)',
    callable(_sbp) and all(_sbp(k_, v_) == [] for k_, v_ in _v20ok.items()) and _v20bad is not None and bool(_sbp(_v20k, _v20bad))
    and isinstance(r20.get('same_fn'), list) and any('합성 시도 계약 문제' in str(p_) for p_ in r20['same_fn']),
    (callable(_sbp), _sbp(_v20k, _v20bad) if callable(_sbp) and _v20bad is not None else None, r20.get('same_fn')))

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
if _fail:
    for n in _fail:
        print('  -', n)
    sys.exit(1)
