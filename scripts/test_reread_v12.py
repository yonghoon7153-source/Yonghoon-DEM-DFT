#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""194 인계 v1.2 다시 읽기 검산기 (`docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/reread_v12.py`) 의 반례 회귀 — RGLR4-01 · RGLR4-02 · G2RR-03.

  python3 scripts/test_reread_v12.py        # 종료코드 0 = PASS

Codex 5차 재검증 (`docs/reviews/codex_review_rglr3_reverify_20261006.md` §5) 의 실 CLI 반례를 **복사본**에서 그대로 재현한다 (원본은 안 건드린다):
  RGLR4-01  C4 — 옛 인계 공통 칸 하나를 99 로 바꿔도 · 공통 열을 빼도 PASS · rc 0 이었다 (차이를 기록만 하고 실패 목록에 안 넣었다)
  RGLR4-02  C8 — 봉인 감사표의 lhsx_064 행을 lhs00_000 중복으로 바꿔도 SEALED_LEGACY 194 · PASS · rc 0 이었다 (줄 수 · 판정 문자열만 셌다)
            + record sha · record 상태 · 코호트 변조 · C6 출처 부록 중복 행
Codex 세대 2 재검증 (`docs/reviews/codex_review_gen2_network_reverify_20261006.md` §5 · 탐침 `…_evidence_20261006/probes/reread_extra.py`):
  G2RR-03   C8 — 등록 manifest 의 `plan.queue` 가 비어도 (`[]`) · 없어도 (`plan` 삭제) · 첫 ID 를 중복 추가해도 (194 + 1 행) PASS · rc 0 이었다
            (빈 큐면 집합 비교 생략 · 기대 코호트를 인계표로 대체 · dict 변환이 중복을 삼킨다).
            Q 사례는 **작은 리포 사본** (검산기를 같은 상대 경로에 둔다 — 검산기는 자기 자리에서 리포 뿌리를 찾는다) 의 manifest 만 바꿔 실 CLI 로 돌리고,
            출력의 `batch` 경로가 그 사본인지 확인한다 (진짜 manifest 를 조용히 읽은 실행은 통과하지 못한다).
해제 조건 = 위 변조가 **비영 종료** (출력에 차이를 적는 것만으로는 부족) · 원본 (baseline) PASS 유지 · 의도된 변화는 세대별 허용 목록 (기대 칸 수 · 커밋 = 봉인).
⚠ 이 검산기는 **검산 도구**다 — 자동 배포 관문으로 쓰지 않는다 (Codex 5차 QV1).  이 시험은 그 문구가 검산기에 남아 있는지도 본다.
"""
import csv
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BATCH_REL = os.path.join('docs', 'data', 'lhs_network194_11fcf91e8')
HD_REL = os.path.join(BATCH_REL, 'handover_v12_20261006')
HD = os.path.join(ROOT, HD_REL)
VERIFIER = os.path.join(HD, 'reread_v12.py')
#: G2RR-03 작은 리포 사본 — 검산기가 리포 뿌리 아래에서 읽는 파일 (C1–C6 · C8 입력).  τ 원천 tar 는 뺀다 (C7 은 이 사례에서 안 돈다).
MINI_FILES = (os.path.join(BATCH_REL, 'manifest.json'),
              os.path.join(BATCH_REL, 'merged', 'lhs', 'metrics_flat.csv'), os.path.join(BATCH_REL, 'merged', 'lhs', 'status.json'),
              os.path.join(BATCH_REL, 'merged', 'lhsx', 'metrics_flat.csv'), os.path.join(BATCH_REL, 'merged', 'lhsx', 'status.json'),
              os.path.join('docs', 'data', 'lhs_handover_20261001.csv'), os.path.join('docs', 'data', 'lhsx_handover_20261001.csv'),
              os.path.join('docs', 'data', 'lhs_perc_audit_20261001', 'lhs_20261001_d1ec42fba', 'perc_audit.tsv'),
              os.path.join('docs', 'data', 'lhs_perc_audit_20261001', 'lhsx_20261001_d1ec42fba', 'perc_audit.tsv'))

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


def _copy(dst):
    """검산기 입력 (표 · 열 사전 · 출처 부록 · 제외 노트 · 봉인 감사) 만 복사 — τ 원천 tar · 옛 결과 JSON 은 빼고."""
    os.makedirs(dst, exist_ok=True)
    for f in os.listdir(HD):
        if f.endswith(('.csv', '.tsv')):
            shutil.copyfile(os.path.join(HD, f), os.path.join(dst, f))
    return dst


def _read(path, delim=','):
    with open(path, encoding='utf-8', newline='') as fh:
        rows = list(csv.reader(fh, delimiter=delim))
    return rows[0], rows[1:]


def _write(path, head, rows, delim=','):
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, delimiter=delim, lineterminator='\n')
        w.writerow(head)
        w.writerows(rows)


def run(hd, seal=None, extra=()):
    out = os.path.join(hd, '_reread_out.json')
    cmd = [sys.executable, VERIFIER, '--handover-dir', hd, '--out', out] + (['--seal-audit', seal] if seal else []) + list(extra)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    try:
        js = json.load(open(out, encoding='utf-8'))
    except (OSError, ValueError):
        js = {}
    return p.returncode, js, (p.stdout + p.stderr)[-1500:]


def _fails(js):
    return list(js.get('fails') or [])


def _mini_repo(dst, mutate=None):
    """G2RR-03 — 작은 리포 사본: 검산기 · 인계 입력을 같은 상대 경로에 복사하고 **복사한 manifest 만** mutate(m) 로 바꾼다.
    반환 (리포 뿌리, 사본 검산기, 사본 인계 폴더).  검산기는 자기 자리에서 리포 뿌리를 찾으므로 이 사본의 manifest · 병합 기록을 읽는다."""
    for rel_ in MINI_FILES:
        q = os.path.join(dst, rel_)
        os.makedirs(os.path.dirname(q), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, rel_), q)
    hd_ = _copy(os.path.join(dst, HD_REL))
    ver_ = os.path.join(hd_, 'reread_v12.py')
    shutil.copyfile(VERIFIER, ver_)
    if mutate is not None:
        mp = os.path.join(dst, BATCH_REL, 'manifest.json')
        with open(mp, encoding='utf-8') as fh:
            m = json.load(fh)
        mutate(m)
        with open(mp, 'w', encoding='utf-8') as fh:
            json.dump(m, fh, ensure_ascii=False)
    return dst, ver_, hd_


def run_mini(dst, mutate=None):
    """사본 검산기를 실 CLI 로 (봉인 감사 제공) — env 의 REPO 는 뺀다 (검산기가 자기 자리에서 뿌리를 찾게).  반환 (rc, 출력 JSON, 끝 출력, 사본 batch 경로)."""
    repo_, ver_, hd_ = _mini_repo(dst, mutate)
    out = os.path.join(dst, '_reread_out.json')
    env = {k: v for k, v in os.environ.items() if k != 'REPO'}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    cmd = [sys.executable, ver_, '--handover-dir', hd_, '--seal-audit', os.path.join(hd_, 'seal_audit.tsv'), '--out', out]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)
    try:
        js = json.load(open(out, encoding='utf-8'))
    except (OSError, ValueError):
        js = {}
    return p.returncode, js, (p.stdout + p.stderr)[-1500:], os.path.join(repo_, BATCH_REL)


def _same_path(a, b):
    return bool(a) and bool(b) and os.path.realpath(a) == os.path.realpath(b)


def main():
    if not os.path.isfile(VERIFIER):
        chk(f'검산기가 있다 ({VERIFIER})', False)
        return finish()
    src = open(VERIFIER, encoding='utf-8').read()
    chk('V0 검산기 머리말 — 자동 배포 관문이 아니다 (Codex 5차 QV1) · 검산 도구', '배포 관문이 아니다' in src or '배포 관문으로 쓰지 않는다' in src)
    td = tempfile.mkdtemp(prefix='reread_v12_')
    try:
        base = _copy(os.path.join(td, 'base'))
        rc, js, tail = run(base, os.path.join(base, 'seal_audit.tsv'))
        chk('T0 baseline (원본 복사본) — PASS · rc 0 · 실패 0', rc == 0 and js.get('verdict') == 'PASS' and _fails(js) == [], f'rc={rc} · {_fails(js)} · {tail}')
        c8 = js.get('C8_seal_audit') or {}
        chk('T0b baseline C8 — 194 행 · 고유 194 · record sha 194 일치 · 코호트 · 상태 대조', c8.get('n') == 194 and c8.get('n_unique') == 194
            and c8.get('record_sha_match') == 194 and not c8.get('problems'), repr({k: c8.get(k) for k in ('n', 'n_unique', 'record_sha_match', 'problems')}))

        # ── RGLR4-01 — C4 공통 칸 한 칸 변조 (Codex 반례: lhs00_000.coverage_AM_total_hertz_pct 13.64… → 99)
        d1 = _copy(os.path.join(td, 'm1'))
        tp = os.path.join(d1, 'lhs_handover_v12_20261006.csv')
        h, rows = _read(tp)
        ci, ki = h.index('coverage_AM_total_hertz_pct'), h.index('case_id')
        old = next(r[ci] for r in rows if r[ki] == 'lhs00_000')
        for r in rows:
            if r[ki] == 'lhs00_000':
                r[ci] = '99'
        _write(tp, h, rows)
        rc, js, tail = run(d1, os.path.join(d1, 'seal_audit.tsv'))
        chk(f'T1 ★ RGLR4-01 — 공통 칸 한 칸 ({old} → 99) 변조 = FAIL · 비영 종료 · 실패 목록에 lhs:C4',
            rc != 0 and js.get('verdict') == 'FAIL' and any(f.startswith('lhs:C4') for f in _fails(js)), f'rc={rc} · {_fails(js)}')

        # ── RGLR4-01 — 공통 열 탈락 (표 · 열 사전 둘 다에서 빼 C3 은 통과하게 — C4 만 걸려야 한다)
        d2 = _copy(os.path.join(td, 'm2'))
        tp = os.path.join(d2, 'lhs_handover_v12_20261006.csv')
        h, rows = _read(tp)
        ci = h.index('coverage_AM_total_hertz_pct')
        _write(tp, h[:ci] + h[ci + 1:], [r[:ci] + r[ci + 1:] for r in rows])
        dp = os.path.join(d2, 'lhs_handover_v12_20261006_columns.tsv')
        dh, drows = _read(dp, '\t')
        _write(dp, dh, [r for r in drows if r[0] != 'coverage_AM_total_hertz_pct'], '\t')
        rc, js, tail = run(d2, os.path.join(d2, 'seal_audit.tsv'))
        f2 = _fails(js)
        chk('T2 ★ RGLR4-01 — 등록 안 된 공통 열 탈락 = FAIL · 비영 종료 · lhs:C4 (C3 은 통과 — 열 사전도 같이 뺐다)',
            rc != 0 and any(f.startswith('lhs:C4') for f in f2) and not any(f.startswith('lhs:C3') for f in f2), f'rc={rc} · {f2}')

        # ── RGLR4-02 — 봉인 감사: 마지막 lhsx_064 행을 첫 lhs00_000 행으로 (194 줄 · 고유 193 · lhsx_064 증거 없음)
        d3 = _copy(os.path.join(td, 'm3'))
        sp = os.path.join(d3, 'seal_audit.tsv')
        sh, srows = _read(sp, '\t')
        si = sh.index('case')
        chk('T3 픽스처 — 원본 감사표 마지막 행 = lhsx_064 · 첫 행 = lhs00_000', srows[-1][si] == 'lhsx_064' and srows[0][si] == 'lhs00_000',
            f'{srows[-1][si]} · {srows[0][si]}')
        _write(sp, sh, srows[:-1] + [list(srows[0])], '\t')
        rc, js, tail = run(d3, sp)
        chk('T3 ★ RGLR4-02 — 누락 + 중복 교체 (194 줄 · 고유 193) = FAIL · 비영 종료 · C8',
            rc != 0 and any('C8' in f for f in _fails(js)), f'rc={rc} · {_fails(js)}')

        def _seal_mut(tag, fn):
            d_ = _copy(os.path.join(td, tag))
            sp_ = os.path.join(d_, 'seal_audit.tsv')
            sh_, sr_ = _read(sp_, '\t')
            fn(sh_, sr_)
            _write(sp_, sh_, sr_, '\t')
            return run(d_, sp_)

        def _flip_sha(h_, r_):
            i_ = h_.index('record_sha256')
            s_ = r_[5][i_]
            r_[5][i_] = s_[:-1] + ('0' if s_[-1] != '0' else '1')
        rc, js, tail = _seal_mut('m4', _flip_sha)
        chk('T4 ★ RGLR4-02 — record sha 한 글자 변조 = FAIL · 비영 종료 · C8 (병합 기록의 정규 JSON sha 와 대조)',
            rc != 0 and any('C8' in f for f in _fails(js)), f'rc={rc} · {_fails(js)}')

        def _flip_status(h_, r_):
            r_[7][h_.index('record_status')] = 'partial'
        rc, js, tail = _seal_mut('m5', _flip_status)
        chk('T5 ★ record 상태 변조 (done → partial · 병합 기록은 done) = FAIL · C8', rc != 0 and any('C8' in f for f in _fails(js)), f'rc={rc} · {_fails(js)}')

        def _flip_cohort(h_, r_):
            r_[3][h_.index('cohort')] = 'lhsx'
        rc, js, tail = _seal_mut('m6', _flip_cohort)
        chk('T6 ★ 코호트 변조 (lhs 케이스를 lhsx 로) = FAIL · C8', rc != 0 and any('C8' in f for f in _fails(js)), f'rc={rc} · {_fails(js)}')

        # ── C6 출처 부록 — 같은 집합 검사만으로는 중복 행을 못 본다 (행 하나를 덧붙여도 집합은 같다)
        d7 = _copy(os.path.join(td, 'm7'))
        pp = os.path.join(d7, 'lhs_handover_v12_20261006_tau_provenance.tsv')
        ph, prows = _read(pp, '\t')
        _write(pp, ph, prows + [list(prows[0])], '\t')
        rc, js, tail = run(d7, os.path.join(d7, 'seal_audit.tsv'))
        chk('T7 ★ C6 출처 부록 중복 행 (집합은 같다 · 131 행) = FAIL · 비영 종료 · lhs:C6',
            rc != 0 and any(f.startswith('lhs:C6') for f in _fails(js)), f'rc={rc} · {_fails(js)}')

        # ── 의도된 변화 = 세대별 허용 목록 (기대 칸 수까지) — 검산기 모듈을 그 자리에서 불러 상수만 바꿔 본다 (원본 파일은 그대로)
        spec = importlib.util.spec_from_file_location('reread_v12_under_test', VERIFIER)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        has_allow = isinstance(getattr(mod, 'C4_ALLOWED', None), dict)
        chk('T8 허용 목록 상수 C4_ALLOWED 가 있다 · v1.2 세대는 비었다 (옛 인계와 공통 칸 차이 0 · 탈락 0 이 기대값)',
            has_allow and all(not (v or {}).get('diff_cols') and not (v or {}).get('dropped_cols') for v in mod.C4_ALLOWED.values()),
            repr(getattr(mod, 'C4_ALLOWED', None)))
        if has_allow:
            saved = json.loads(json.dumps(mod.C4_ALLOWED))
            try:
                mod.C4_ALLOWED['lhs'] = {'diff_cols': {'coverage_AM_total_hertz_pct': 1}, 'dropped_cols': []}
                rc_a = mod.main(['--handover-dir', d1, '--seal-audit', os.path.join(d1, 'seal_audit.tsv'), '--out', os.path.join(d1, 'allow.json')])
                mod.C4_ALLOWED['lhs'] = {'diff_cols': {'coverage_AM_total_hertz_pct': 2}, 'dropped_cols': []}
                rc_b = mod.main(['--handover-dir', d1, '--seal-audit', os.path.join(d1, 'seal_audit.tsv'), '--out', os.path.join(d1, 'allow2.json')])
                mod.C4_ALLOWED['lhs'] = {'diff_cols': {}, 'dropped_cols': ['coverage_AM_total_hertz_pct']}
                rc_c = mod.main(['--handover-dir', d2, '--seal-audit', os.path.join(d2, 'seal_audit.tsv'), '--out', os.path.join(d2, 'allow3.json')])
            finally:
                mod.C4_ALLOWED.clear()
                mod.C4_ALLOWED.update(saved)
            chk('T9 허용 목록 — 등록한 열 · 기대 칸 수 (1) 가 맞으면 통과 · 칸 수가 다르면 (2) 실패 · 등록한 탈락 열은 통과',
                rc_a == 0 and rc_b != 0 and rc_c == 0, repr((rc_a, rc_b, rc_c)))

        # ── G2RR-03 — 등록 큐 (manifest plan.queue) 변조.  작은 리포 사본의 manifest 만 바꾸고 · 실 CLI · 봉인 감사 제공 · 출력 batch = 사본
        with open(os.path.join(ROOT, BATCH_REL, 'manifest.json'), encoding='utf-8') as fh:
            q_real = (json.load(fh).get('plan') or {}).get('queue')
        q_ok = isinstance(q_real, list) and all(isinstance(e, dict) for e in q_real)
        q_coh = {}
        for e in (q_real if q_ok else []):
            q_coh[e.get('cohort')] = q_coh.get(e.get('cohort'), 0) + 1
        q_ids = [e.get('case') for e in (q_real if q_ok else [])]
        chk('QF 픽스처 — 실제 등록 큐 = 194 행 · lhs 130 · lhsx 64 · 고유 194 · 첫 ID ≠ 끝 ID',
            q_ok and len(q_real) == 194 and q_coh == {'lhs': 130, 'lhsx': 64} and len(set(q_ids)) == 194 and q_ids[0] != q_ids[-1],
            repr((len(q_real) if isinstance(q_real, list) else q_real, q_coh)))
        qd = os.path.join(td, 'q')

        rc, js, tail, bq = run_mini(os.path.join(qd, 'q0'))
        c8 = js.get('C8_seal_audit') or {}
        chk('Q0 G2RR-03 — 사본 manifest 그대로 = PASS · rc 0 · 출력 batch = 사본 · C8 194 행 · 등록 큐 194 · record sha 194 · 문제 0',
            rc == 0 and js.get('verdict') == 'PASS' and _fails(js) == [] and _same_path(js.get('batch'), bq)
            and c8.get('n') == 194 and c8.get('queue_n') == 194 and c8.get('record_sha_match') == 194 and not c8.get('problems'),
            f'rc={rc} · batch={js.get("batch")} · {_fails(js)} · {repr({k: c8.get(k) for k in ("n", "queue_n", "record_sha_match", "problems")})} · {tail}')

        def _q_empty(m):
            m['plan']['queue'] = []

        def _q_plan_absent(m):
            m.pop('plan', None)

        def _q_key_absent(m):
            m['plan'].pop('queue', None)

        def _q_null(m):
            m['plan']['queue'] = None

        def _q_dup_first(m):
            m['plan']['queue'].append(dict(m['plan']['queue'][0]))

        def _q_last_as_first(m):
            m['plan']['queue'][-1] = dict(m['plan']['queue'][0])

        def _q_swap_cohort(m):
            q_ = m['plan']['queue']
            i_ = next(k for k, e in enumerate(q_) if e.get('cohort') == 'lhs')
            j_ = next(k for k, e in enumerate(q_) if e.get('cohort') == 'lhsx')
            q_[i_]['cohort'], q_[j_]['cohort'] = q_[j_]['cohort'], q_[i_]['cohort']

        def _c8_fail(js_):
            return js_.get('verdict') == 'FAIL' and any('C8' in f for f in _fails(js_))

        for tag, fn, label in (('q1', _q_empty, 'Q1 plan.queue = []'), ('q2', _q_plan_absent, 'Q2 plan 삭제'),
                               ('q3', _q_key_absent, 'Q3 queue 키 삭제'), ('q4', _q_null, 'Q4 queue = null')):
            rc, js, tail, bq = run_mini(os.path.join(qd, tag), fn)
            c8 = js.get('C8_seal_audit') or {}
            chk(f'{label} ★ G2RR-03 — 등록 큐 결손 = FAIL · 비영 종료 · C8 · 출력 batch = 사본 · queue_n 0 · 큐 코호트 없는 감사표 194 행의 병합 기록은 대조 안 함 (인계표 대체 없음)',
                rc != 0 and _c8_fail(js) and _same_path(js.get('batch'), bq) and c8.get('queue_n') == 0
                and c8.get('record_unreferenced') == 194 and c8.get('record_sha_match') == 0,
                f'rc={rc} · batch={js.get("batch")} · {_fails(js)} · '
                f'{repr({k: c8.get(k) for k in ("queue_n", "record_unreferenced", "record_sha_match")})}')

        rc, js, tail, bq = run_mini(os.path.join(qd, 'q5'), _q_dup_first)
        c8 = js.get('C8_seal_audit') or {}
        chk('Q5 ★ G2RR-03 — 첫 ID 중복 추가 (194 + 1 행) = FAIL · 비영 종료 · C8 · 출력 batch = 사본 · queue_n 195 (원 행 수) · 고유 194',
            rc != 0 and _c8_fail(js) and _same_path(js.get('batch'), bq) and c8.get('queue_n') == 195 and c8.get('queue_n_unique') == 194,
            f'rc={rc} · batch={js.get("batch")} · {_fails(js)} · {repr({k: c8.get(k) for k in ("queue_n", "queue_n_unique")})}')

        rc, js, tail, bq = run_mini(os.path.join(qd, 'q6'), _q_last_as_first)
        chk('Q6 ★ G2RR-03 — 끝 행을 첫 행 사본으로 교체 (194 행 · 고유 193 · 끝 ID 빠짐) = FAIL · 비영 종료 · C8 · 출력 batch = 사본',
            rc != 0 and _c8_fail(js) and _same_path(js.get('batch'), bq), f'rc={rc} · batch={js.get("batch")} · {_fails(js)}')

        rc, js, tail, bq = run_mini(os.path.join(qd, 'q7'), _q_swap_cohort)
        chk('Q7 ★ G2RR-03 — lhs 하나 · lhsx 하나의 코호트 맞바꿈 (코호트 수 130 · 64 그대로) = FAIL · 비영 종료 · C8 · 출력 batch = 사본',
            rc != 0 and _c8_fail(js) and _same_path(js.get('batch'), bq), f'rc={rc} · batch={js.get("batch")} · {_fails(js)}')
    finally:
        shutil.rmtree(td, ignore_errors=True)
    return finish()


def finish():
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
