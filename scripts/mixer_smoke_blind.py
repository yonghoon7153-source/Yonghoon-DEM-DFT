#!/usr/bin/env python3
"""mixer_smoke_blind.py — bin 0 스모크를 **M 을 보지 않고** 판독해 발사 관문용 증서만 남기는 래퍼 (Codex 6 차 Q5 · 2026-09-29).

왜 — 판독기 `measure_mixing_index.py` 의 일반 CLI 는 JSON 전에 M · S₀² · S_R² 를 화면에 쓴다.  bin 0 스모크는 기술 실패만 거르는
관문인데 (사전등록 §8 · K5) 그때 M 이 보이면 나머지 시드 발사 결정이 결과에 오염된다.  ⇒ 이 래퍼는
  ① 판독기를 **stdout · stderr 를 가로채** 부른다 (판독기의 어떤 출력도 화면에 나오지 않는다)
  ② 전체 결과를 **접근 제한 파일** (<런>/.smoke_blind/full_<시각>.json · 0600) 에 봉인한다 — "계산했지만 보지 않았다" 와 "계산 안 했다" 를
     가른다 (Codex: 감사 가능한 유일한 결과를 폐기할 이유는 없다)
  ③ 증서에는 **명시적 허용목록**만 투영한다 (삭제목록이 아니다 — 판독기에 새 필드가 생겨도 자동 노출되지 않는다):
       run · provenance · plan · t0_step · smoke.complete · smoke.tech_smoke · smoke.qc_repr.pass
     = `launch_highbo.sh rest` 관문이 읽는 전부 (`mixer_gate_reader_diff.py` 의 opaque_allowlisted_certificate 가 rc 0 을 확인)
  ④ 판독기가 거부 (SystemExit · 예외) 하면 그 문구 (S₀² · S_R² 값이 들어 있을 수 있다) 도 봉인 파일에만 두고 화면에는 사유 코드만 낸다
  ⑤ 열람 기록 <런>/.smoke_blind/blind_log.jsonl — 언제 · 누가 · 어느 도구 (sha256) 로 · 무엇을 (투영 필드 목록) 보았는지 · 전체 결과 sha256.
⛔ 이 래퍼는 증서의 plan · t0_step · provenance 를 **손대지 않는다** (판독기 값 그대로) — 그 필드는 신뢰된 주장이라 (Codex §3
  `tampered_certificate_narrows_bin0`) 투영기가 편집하면 관문의 창 정의가 무너진다.
⚠ 래퍼가 막는 것은 **화면 노출**이다 — 봉인 파일을 여는 것은 사람의 규율 (열람하면 blind_log 에 적는다 · 사전등록 §8 ⑤).

    python3 scripts/mixer_smoke_blind.py <OUT>/LH_s32452843 --ref <OUT>/E0_s32452843 --cert <OUT>/LH_s32452843/smoke_cert.json
    python3 scripts/mixer_smoke_blind.py --selftest
rc 0 = 증서 씀 (합격 여부는 관문이 판정한다 — 이 래퍼는 판정하지 않는다) · rc 2 = 판독기 거부 (증서 없음 · 사유는 봉인 파일) · rc 1 = 입력 오류.

★ 2026-09-30 — 강성 축 (사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §6 · §8-2 ⑤ · 코드 선행조건 2 단계 piece 3):
  `--contract` = 강성 축 셀 폴더 (`<E0|LC|LH>_<soft|ref|ref2>[_dthalf][_r<N>]_s<seed>`) 의 **접촉 상태 증서**.
    회전 팔 (LC · LH): bin 0 스모크 허용목록 (위 그대로) + `contact` 블록 (검사기 check_window 를 bin 0 창으로 · 등록 인자) —
    E0 팔: `{run, kind 'e0-contract', contact (전 창 = 계획 t₀), completion (log 마지막 thermo step = run 합 — HBR6-03)}` (판독기 없음 · --ref 불요).
  contact.status = 세 축 분리 (§6 표): 기술 · 원 1 % · soft 범위 → TECH_FAIL / CONTRACT_MET / CONTRACT_NOT_MET / OUT_OF_RANGE.
    ref/ref2 = 계약 팔 (1 % · 범위 없음) · soft = 진단 팔 (등록 5.8 % = 1 % × 14^(2/3) · 넘으면 OUT_OF_RANGE · **올리지 않는다**).
  GATE_TABLE = arm × E × 검사 → rest 해제 관문 (셀프테스트 ⑧ 이 36 칸을 고정 — Codex 7 차 HBR7-02 해결 증거).  M 은 여전히 맹검 (허용목록 투영만).
    python3 scripts/mixer_smoke_blind.py <OUT>/LC_ref_r8_s15485863 --ref <OUT>/E0_ref_s15485863 --cert <증서> --contract [--phase-receipt R]
    python3 scripts/mixer_smoke_blind.py <OUT>/E0_ref_s15485863 --cert <증서> --contract
  `--e0-diag <OUT> --record <OUT>/dev_e0_diag.json` = DEV E0 다섯의 **E0 진단 PASS 기록** (§8-2 ② "① E0 5 런 … → 1 % 계약 · 정규화 · 완주 진단
    (M 미열람 · 허용목록 투영) → ② 통과 시에만 LC_ref · LH_ref 회전 2 런") — 런처 `launch_highbo.sh dev-rot <기록>` 이 이어 본다
    (scripts/mixer_stage_gate.py verify_e0_record: 기록 = 지금 폴더 · 봉인 · 로그 · 도구 · NP).  rc 0 = PASS · 1 = FAIL (기록은 남는다).
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import datetime
import getpass
import hashlib
import io
import json
import os
import socket
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import measure_mixing_index as mi     # noqa: E402
import check_contact_validity as cv   # noqa: E402  (2026-09-30 · piece 3) 접촉 상태
import mixer_deck_diff as dd          # noqa: E402  셀 이름 · 재생성 덱 (단일 출처)
from mixer_restart_phase_test import log_completion   # noqa: E402  완주 = 마지막 thermo step = run 합 (HBR6-03 — 배너는 기록만)
import mixer_stage_gate as sg         # noqa: E402  (piece 1) E0 진단 기록 스키마 · 등록 통과선 · 도구 sha256 — 관문과 한 벌

REG = dict(r_container=0.013138, cells=16, x_cells=4, n_min=20, axis='x')     # 사전등록 §2-3 · §8 ③ — 관문 REG 와 같다 (바꾸지 않는다)
ALLOW_TOP = ('run', 'provenance', 'plan', 't0_step')
ALLOW_SMOKE = ('complete', 'tech_smoke')
ALLOW_QC = ('pass',)
#: 결과 대리량으로 취급하는 키 — 투영 · 화면 어디에도 나오면 안 된다 (자기검사 누설 시험)
RESULT_KEYS = ('M', 'M_final', 'S0', 'SR', 'S0_sq', 'SR_sq', 'rows', 'by_rev', 'flat', 'planned', 'sd', 'M_t')
#: ★ 강성 축 접촉 상태 증서 (2026-09-30 · piece 3) — 관문 (scripts/mixer_stage_gate.py rest-gate) 이 이 모양만 받는다
CONTACT_CERT_SCHEMA = 'mixer_contact_cert/1'
ROT_CERT_KEYS = ALLOW_TOP + ('smoke', 'contact')
E0_CERT_KIND = 'e0-contract'
E0_CERT_KEYS = ('run', 'kind', 'contact', 'completion')
#: ★ arm × E × 검사 → rest 해제 관문 (사전등록 §6 표 · §8-2 ⑤ · Codex 7 차 HBR7-02 "해결 증거: arm×E×검사 종류별 허용/거부표, soft NOT_MET 이
#:   보존되면서 기술 실패는 거부되는 합성 관문 시험").  E0 · LC · LH 는 **수준**으로만 갈린다 (ref2 = ref · DEV 전용).
#:   ref (계약 팔): "원 1 % 물리 적격성 — 통과 필수 · 실패면 해당 확인 주장 HOLD" ⇒ CONTRACT_MET 만.
#:   soft (진단 팔): "평가 · 보고하되 미달이면 NOT_MET 유지" · OUT_OF_RANGE = "같은 조건 재시도로 지우는 TECH 사유 아님 · 팔은 완주 · 값 보존 ·
#:   보고 · 짝 블록의 다른 팔 계속" ⇒ 기술 실패만 거부 ("기술적으로 관측 가능한가 — 같은 기술 계약 필수").
GATE_TABLE = {
    ('ref', 'TECH_FAIL'): False, ('ref', 'CONTRACT_MET'): True, ('ref', 'CONTRACT_NOT_MET'): False, ('ref', 'OUT_OF_RANGE'): False,
    ('soft', 'TECH_FAIL'): False, ('soft', 'CONTRACT_MET'): True, ('soft', 'CONTRACT_NOT_MET'): True, ('soft', 'OUT_OF_RANGE'): True,
}
GATE_WHY = {
    ('ref', 'TECH_FAIL'): '기술 실패 — 관측량 미정의 (§8-4 같은 seed 새 폴더 한 번 재실행)',
    ('ref', 'CONTRACT_NOT_MET'): 'ref 원 1 % 미달 — 해당 확인 주장 HOLD (§6)',
    ('ref', 'OUT_OF_RANGE'): 'ref 에는 soft 범위가 없다 (상태 모순)',
    ('soft', 'TECH_FAIL'): '기술 실패 — soft 도 같은 기술 계약 필수 (§6)',
    ('soft', 'CONTRACT_NOT_MET'): 'soft 원 1 % NOT_MET 보존 (계약 밖 진단) — 관문 통과',
    ('soft', 'OUT_OF_RANGE'): 'soft 진단 범위 5.8 % 초과 — OUT_OF_RANGE 한정어 · 값 보존 · 관문 통과',
}


def gate_decision(level, status):
    """(수준, 상태) → (관문 허용?, 사유).  모르는 수준 · 상태 = 거부 (fail-closed)."""
    lv = 'ref' if level in ('ref', 'ref2') else level
    k = (lv, status)
    if k not in GATE_TABLE:
        return False, f'모르는 조합 (수준 {level!r} · 상태 {status!r})'
    return GATE_TABLE[k], GATE_WHY.get(k, '')


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha_file(p) -> str:
    return _sha_bytes(Path(p).read_bytes())


def project(full: dict) -> dict:
    """전체 판독 결과 → 허용목록 투영 (깊은 복사 · 값 편집 없음).  허용 키가 없으면 KeyError (모양이 다른 판독기 = 거부)."""
    e = {k: copy.deepcopy(full[k]) for k in ALLOW_TOP}
    sm = full['smoke']
    e['smoke'] = {k: copy.deepcopy(sm[k]) for k in ALLOW_SMOKE}
    e['smoke']['qc_repr'] = {k: copy.deepcopy(sm['qc_repr'][k]) for k in ALLOW_QC}
    return e


def _keys(v, out=None):
    out = set() if out is None else out
    if isinstance(v, dict):
        for k, x in v.items():
            out.add(str(k))
            _keys(x, out)
    elif isinstance(v, (list, tuple)):
        for x in v:
            _keys(x, out)
    return out


def leak_check(obj) -> list:
    """투영 안 어느 깊이에도 결과 키가 없는지 (있으면 그 키 목록)."""
    return sorted(k for k in _keys(obj) if k in RESULT_KEYS)


def run_blind(run_dir: str, ref_dir: str, cert: str, reg=REG):
    """판독 → 봉인 → 투영 → 증서.  반환 (rc, 요약 dict)."""
    run_dir, ref_dir = os.path.normpath(run_dir), os.path.normpath(ref_dir)
    vault = Path(run_dir) / '.smoke_blind'
    vault.mkdir(parents=True, exist_ok=True)
    os.chmod(vault, 0o700)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')     # µs — 같은 초의 두 호출도 다른 파일
    buf_out, buf_err = io.StringIO(), io.StringIO()
    full, refused = None, None
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        try:
            full = mi.analyse(run_dir, ref_dir, reg['r_container'], cells=reg['cells'], x_cells=reg['x_cells'],
                              n_min=reg['n_min'], axis=reg['axis'])
        except SystemExit as e:                       # 판독기의 거부 — 문구에 S₀² · S_R² 가 들어 있을 수 있다 → 봉인 파일에만
            refused = dict(kind='SystemExit', message=str(e))
        except Exception as e:                        # noqa: BLE001 — 어떤 예외든 화면에 내지 않는다
            refused = dict(kind=type(e).__name__, message=str(e), traceback=traceback.format_exc())
    record = dict(schema='mixer_smoke_blind_full/1', time_utc=ts, run=run_dir, ref=ref_dir, args=dict(reg),
                  reader_sha256=_sha_file(mi.__file__), wrapper_sha256=_sha_file(__file__),
                  reader_stdout=buf_out.getvalue(), reader_stderr=buf_err.getvalue(), refused=refused, result=full)
    for k in range(1000):                              # O_EXCL — 있는 파일을 덮지 않는다 (같은 µs 면 접미사)
        full_path = vault / (f'full_{ts}.json' if k == 0 else f'full_{ts}_{k}.json')
        try:
            fd = os.open(full_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            break
        except FileExistsError:
            continue
    else:
        raise RuntimeError('봉인 파일 이름을 만들 수 없다')
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        json.dump(record, fh, ensure_ascii=False, indent=1, default=str)
        fh.write('\n')
    os.chmod(full_path, 0o600)
    full_sha = _sha_file(full_path)
    log = dict(time_utc=ts, user=getpass.getuser(), host=socket.gethostname(), tool=os.path.realpath(__file__),
               wrapper_sha256=record['wrapper_sha256'], reader_sha256=record['reader_sha256'], args=dict(reg),
               full_file=str(full_path), full_sha256=full_sha, viewed='projection only' if refused is None else 'refusal code only',
               projected_fields=None, cert=None, cert_sha256=None)
    rc, summary = 2, dict(full_file=str(full_path), full_sha256=full_sha)
    if refused is None:
        try:
            e = project(full)
        except (KeyError, TypeError) as ex:
            refused = dict(kind='ProjectionShape', message=f'{type(ex).__name__}: {ex}')
    if refused is None:
        leaks = leak_check(e)
        if leaks:                                       # 허용목록 안에 결과 키가 숨어 들어왔다 — 증서를 쓰지 않는다
            refused = dict(kind='Leak', message=f'투영 안 결과 키 {leaks}')
    if refused is None:
        body = json.dumps([e], ensure_ascii=False, indent=1) + '\n'
        Path(cert).parent.mkdir(parents=True, exist_ok=True)
        tmp = str(cert) + '.tmp'
        Path(tmp).write_text(body, encoding='utf-8')
        os.replace(tmp, cert)
        log.update(projected_fields=dict(top=list(ALLOW_TOP), smoke=list(ALLOW_SMOKE), qc_repr=list(ALLOW_QC)),
                   cert=os.path.realpath(cert), cert_sha256=_sha_bytes(body.encode('utf-8')))
        rc = 0
        summary.update(cert=str(cert), complete=e['smoke']['complete'], n_tech=len(e['smoke']['tech_smoke']),
                       qc_pass=e['smoke']['qc_repr']['pass'])
    else:
        log['refused_kind'] = refused['kind']
        summary.update(refused_kind=refused['kind'])
    with (vault / 'blind_log.jsonl').open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(log, ensure_ascii=False) + '\n')
    os.chmod(vault / 'blind_log.jsonl', 0o600)
    return rc, summary


def _vault(dirp, prefix, record):
    """0600 봉인 파일 (O_EXCL · 폴더 0700) → (경로, sha256)."""
    dirp = Path(dirp)
    dirp.mkdir(parents=True, exist_ok=True)
    os.chmod(dirp, 0o700)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    for k in range(1000):
        p = dirp / (f'{prefix}_{ts}.json' if k == 0 else f'{prefix}_{ts}_{k}.json')
        try:
            fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            break
        except FileExistsError:
            continue
    else:
        raise RuntimeError('봉인 파일 이름을 만들 수 없다')
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        json.dump(record, fh, ensure_ascii=False, indent=1, default=str)
        fh.write('\n')
    os.chmod(p, 0o600)
    return str(p), _sha_file(p)


def _blind_log(dirp, entry):
    p = Path(dirp) / 'blind_log.jsonl'
    with p.open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(entry, ensure_ascii=False, default=str) + '\n')
    os.chmod(p, 0o600)


def _run_total(run_dir):
    import re as _re
    return sum(int(x) for x in _re.findall(r'^run\s+(\d+)', Path(run_dir, 'in.mixer').read_text(encoding='utf-8'), _re.M))


def _expected_counts(c):
    """생성기 계획의 상별 입자 수 → {타입: 수} (check_window expect_counts — 모체 §2-4 "상별 수 = 계획")."""
    p = dd._gen.plan(dd.GEN_ARGS['n_total'], cgf=dd.GEN_ARGS['cgf'], stiffen_se=c['stiffen_se'])
    return {i + 1: int(p['n'][t]) for i, t in enumerate(dd._gen.TYPES)}


def contact_eval(run_dir, name, bins=None, phase_receipt=None):
    """등록 인자로 check_window → (전체 결과, contact 블록).  인자: n_expected 파일 · 계획 상별 수 · **이름에서 재생성한 기대 덱** (정지 벽 계약 ·
    HBR4-07) · 캠페인 STL · soft 면 등록 범위 5.8 % (ref/ref2 는 없음 = 계약 팔) · (회전 팔) 재개-위상 영수증.
    contact 블록 = 허용목록: 상태 (세 축) · 판정 · 창 · 벽 근거 · 출처 sha256 (검사기 · 덱 · 발사 봉인 · 기대 덱) · 본 프레임 묶음.  M 과 무관."""
    c = dd.parse_cell(name)
    soft = cv.SOFT_RANGE_PCT if c['level'] == 'soft' else None
    try:
        ne = int(Path(run_dir, 'n_expected').read_text(encoding='utf-8').strip())
    except (OSError, ValueError):
        ne = None
    exp_text = dd.cell_expected_deck(name)
    fd, exp = tempfile.mkstemp(suffix='.mixer')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as fh:
            fh.write(exp_text)
        w = cv.check_window(run_dir, ne, expect_counts=_expected_counts(c), phase_receipt=phase_receipt, expect_deck=exp,
                            stl_ref_dir=cv.STL_REF_DIR, bins=bins, soft_range_pct=soft)
    finally:
        os.remove(exp)
    lrp = Path(run_dir, 'launch_record.json')
    block = dict(schema=CONTACT_CERT_SCHEMA, run=name, level=c['level'], arm=c['arm'], bins=w.get('bins'), soft_range_pct=soft,
                 status=copy.deepcopy(w.get('status')), verdict=w.get('verdict'),
                 window=list(w['window']) if w.get('window') else None, n_frames=w.get('n_frames'), wall_basis=w.get('phase_status'),
                 checker_sha256=_sha_file(cv.__file__), deck_sha256=_sha_file(Path(run_dir, 'in.mixer')),
                 launch_record_sha256=_sha_file(lrp) if lrp.is_file() else None, expect_deck_sha256=_sha_bytes(exp_text.encode('utf-8')),
                 frames=mi.frame_bundle([(int(st), p) for st, p in (w.get('frames_evaluated') or [])]))
    return w, block


def run_contract_cert(run_dir, ref_dir, cert, phase_receipt=None, reg=REG):
    """--contract (piece 3) — 회전 팔: 판독 (bin 0 스모크) + contact (bin 0 창) · E0 팔: contact (전 창) + 완주.  반환 (rc, 요약).
    래퍼는 판정하지 않는다 — 상태를 그대로 적고 관문 (GATE_TABLE) 이 판정한다."""
    run_dir = os.path.normpath(run_dir)
    name = os.path.basename(run_dir)
    c = dd.parse_cell(name)
    vault = Path(run_dir) / '.smoke_blind'
    buf_out, buf_err = io.StringIO(), io.StringIO()
    full, w, block, refused = None, None, None, None
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        try:
            if c['arm'] != 'E0':
                full = mi.analyse(run_dir, os.path.normpath(ref_dir), reg['r_container'], cells=reg['cells'], x_cells=reg['x_cells'],
                                  n_min=reg['n_min'], axis=reg['axis'])
            w, block = contact_eval(run_dir, name, bins=(0,) if c['arm'] != 'E0' else None, phase_receipt=phase_receipt)
        except SystemExit as e:
            refused = dict(kind='SystemExit', message=str(e))
        except Exception as e:                                          # noqa: BLE001 — 어떤 예외든 화면에 내지 않는다
            refused = dict(kind=type(e).__name__, message=str(e), traceback=traceback.format_exc())
    comp = None
    if c['arm'] == 'E0' and refused is None:
        tot = _run_total(run_dir)
        lc = log_completion(os.path.join(run_dir, 'log.lmp'), tot)
        comp = dict(complete=lc['complete'], basis=lc['basis'], last_thermo_step=lc['last_thermo_step'], run_total=tot,
                    log_sha256=lc['log_sha256'])
    fp, fsha = _vault(vault, 'contract_full', dict(schema='mixer_contract_full/1', run=run_dir, ref=ref_dir, reg=dict(reg),
                                                      reader_sha256=_sha_file(mi.__file__), checker_sha256=_sha_file(cv.__file__),
                                                      wrapper_sha256=_sha_file(__file__), reader_stdout=buf_out.getvalue(),
                                                      reader_stderr=buf_err.getvalue(), refused=refused, result=full, contact=w,
                                                      completion=comp))
    log = dict(time_utc=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'), user=getpass.getuser(),
               host=socket.gethostname(), tool=os.path.realpath(__file__), wrapper_sha256=_sha_file(__file__), mode='contract-cert',
               full_file=fp, full_sha256=fsha, viewed='projection only' if refused is None else 'refusal code only',
               projected_fields=None, cert=None, cert_sha256=None)
    e = None
    if refused is None:
        try:
            if c['arm'] == 'E0':
                e = dict(run=name, kind=E0_CERT_KIND, contact=block, completion=comp)
            else:
                e = project(full)
                e['contact'] = block
            leaks = leak_check(e)
            if leaks:
                refused = dict(kind='Leak', message=f'투영 안 결과 키 {leaks}')
        except (KeyError, TypeError) as ex:
            refused = dict(kind='ProjectionShape', message=f'{type(ex).__name__}: {ex}')
    if refused is not None:
        log['refused_kind'] = refused['kind']
        log['viewed'] = 'refusal code only'
        _blind_log(vault, log)
        return 2, dict(full_file=fp, full_sha256=fsha, refused_kind=refused['kind'])
    body = json.dumps([e], ensure_ascii=False, indent=1) + '\n'
    Path(cert).parent.mkdir(parents=True, exist_ok=True)
    tmp = str(cert) + '.tmp'
    Path(tmp).write_text(body, encoding='utf-8')
    os.replace(tmp, cert)
    log.update(projected_fields=sorted(e) + [f'contact.{k}' for k in sorted(block)], cert=os.path.realpath(cert),
               cert_sha256=_sha_bytes(body.encode('utf-8')))
    _blind_log(vault, log)
    return 0, dict(full_file=fp, full_sha256=fsha, cert=str(cert), status=block['status']['status'], kind=e.get('kind', 'rotating'))


def e0_diag(out, record, reg=REG):
    """DEV E0 다섯 (E0_ref ×3 · E0_ref2 · E0_ref@dt/2) → **봉인된 E0 진단 기록** (piece 1 · §8-2 ② · §4 a · b · c).  반환 (rc, 기록).
      complete   다섯 다 log 마지막 thermo step = run 합 (mixer_restart_phase_test.log_completion — HBR6-03)
      technical  다섯 다 상태 ≠ TECH_FAIL · 발사 봉인 stage = dev-e0 · 다섯 봉인의 np 가 하나 (블록 NP)
      a          E0_ref ×3 CONTRACT_MET (§4 a "≤ 1 % 3/3")
      b          E0_ref2 CONTRACT_MET ∧ x_hi(E0_ref2) ≤ x_hi(E0_ref_s32452843) + 1e-9 % (§4 b "계약 안 · E_ref 대비 증가하지 않음")
      c          E0_ref@dt/2 CONTRACT_MET ∧ |x_hi 차| ≤ 0.1 %p ∧ |ΔS_R²| / S_R² ≤ 1 % (§4 c) — S_R² = 판독기 e0_t0_stats (등록 칸 · 계획 t₀)
    x = 저장 프레임 최대 (입자–입자 · 벽) — contact_eval (검사기 check_window · 정지 벽 계약 · 이름에서 재생성한 기대 덱).
    ⚠ c 의 사전등록 지위는 '진단' 이다 — 여기서는 fail-closed 로 회전 관문 (dev-rot) 에 넣었다 (보고의 모호점) · dt/2 · ref2 도 ref 수준이라
      CONTRACT_MET 을 요구한다 (fail-closed).  M 은 계산하지 않는다 (E0 뿐) · S_R² 원값은 봉인 파일에만 (기록 = 상대 변화).
    soft 일관성 (§6: "DEV E0_ref 실측 최대 × 5.81 이 5.8 % 를 넘으면 그 사실을 보고하되 범위를 올리지 않는다") 은 **보고만**."""
    out = os.path.normpath(out)
    vault = Path(out) / '.e0_diag'
    rg = sg.E0_DIAG_REG
    buf_out, buf_err = io.StringIO(), io.StringIO()
    runs, fulls, sr2, refused = {}, {}, {}, None
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        try:
            for n in dd.DEV_E0:
                d = os.path.join(out, n)
                w, block = contact_eval(d, n)
                fulls[n] = w
                tot = _run_total(d)
                lc = log_completion(os.path.join(d, 'log.lmp'), tot)
                try:
                    lr = json.loads(Path(d, 'launch_record.json').read_text(encoding='utf-8'))
                except (OSError, ValueError):
                    lr = {}
                st_ = block['status'] or {}
                runs[n] = dict(dir=os.path.realpath(d), deck_sha256=_sha_file(Path(d, 'in.mixer')),
                               launch_record_sha256=sg.sha_or_none(os.path.join(d, 'launch_record.json')),
                               job_start_sha256=sg.sha_or_none(os.path.join(d, 'job_start.json')), log_sha256=lc['log_sha256'],
                               stage=lr.get('stage'), np=(lr.get('slurm') or {}).get('np'), complete=lc['complete'],
                               last_thermo_step=lc['last_thermo_step'], run_total=tot,
                               contact=dict({k: st_.get(k) for k in ('status', 'technical', 'original_1pct', 'x_lo_pct', 'x_hi_pct')},
                                            verdict=block['verdict'], wall_basis=block['wall_basis'], window=block['window'],
                                            frames_sha256=block['frames']['sha256']))
            for n in ('E0_ref_s32452843', 'E0_ref_dthalf_s32452843'):
                st0, p0, cs = mi.e0_t0_stats(os.path.join(out, n), reg['r_container'], cells=reg['cells'], x_cells=reg['x_cells'],
                                             n_min=reg['n_min'], axis=reg['axis'])
                sr2[n] = dict(t0_step=st0, frame=os.path.basename(p0), s2=cs['s2'])
        except SystemExit as e:
            refused = dict(kind='SystemExit', message=str(e))
        except Exception as e:                                          # noqa: BLE001
            refused = dict(kind=type(e).__name__, message=str(e), traceback=traceback.format_exc())
    checks = {}
    if refused is None:
        st = {n: runs[n]['contact']['status'] for n in dd.DEV_E0}
        xh = {n: runs[n]['contact']['x_hi_pct'] for n in dd.DEV_E0}
        nps = {runs[n]['np'] for n in dd.DEV_E0}
        one_np = len(nps) == 1 and isinstance(next(iter(nps)), int) and not isinstance(next(iter(nps)), bool)
        checks['complete'] = dict(pass_=all(runs[n]['complete'] is True for n in dd.DEV_E0))
        checks['technical'] = dict(pass_=(all(st[n] not in (None, 'TECH_FAIL') for n in dd.DEV_E0)
                                          and all(runs[n]['stage'] == 'dev-e0' for n in dd.DEV_E0) and one_np),
                                   np_values=sorted(str(x) for x in nps))
        checks['a'] = dict(pass_=all(st[n] == 'CONTRACT_MET' for n in dd.DEV_E0[:3]), status={n: st[n] for n in dd.DEV_E0[:3]})
        r2, r1 = xh['E0_ref2_s32452843'], xh['E0_ref_s32452843']
        checks['b'] = dict(pass_=(st['E0_ref2_s32452843'] == 'CONTRACT_MET' and r2 is not None and r1 is not None and r2 <= r1 + rg['eps_pct']),
                           x_ref2_pct=r2, x_ref_pct=r1)
        dh = xh['E0_ref_dthalf_s32452843']
        dmax = abs(dh - r1) if (dh is not None and r1 is not None) else None
        s_a, s_b = sr2['E0_ref_s32452843']['s2'], sr2['E0_ref_dthalf_s32452843']['s2']
        rel = abs(s_b - s_a) / s_a if (isinstance(s_a, float) and s_a > 0 and s_a == s_a and s_b == s_b) else None
        checks['c'] = dict(pass_=(st['E0_ref_dthalf_s32452843'] == 'CONTRACT_MET' and dmax is not None and rel is not None
                                  and dmax <= rg['c_dmax_pp'] + rg['eps_pct'] and rel <= rg['c_sr2_rel'] + rg['eps_rel']),
                           dmax_pp=dmax, sr2_rel=rel)
        for v in checks.values():
            v['pass'] = bool(v.pop('pass_'))
    nps_all = {runs[n]['np'] for n in runs}
    np_rec = next(iter(nps_all)) if len(nps_all) == 1 else None
    fp, fsha = _vault(vault, 'e0_diag_full', dict(schema='mixer_e0_diag_full/1', out=out, reg=dict(reg), contact=fulls, sr2=sr2,
                                                     stdout=buf_out.getvalue(), stderr=buf_err.getvalue(), refused=refused))
    verdict = 'PASS' if (refused is None and checks and all(v['pass'] for v in checks.values())) else 'FAIL'
    k14 = 14 ** (2.0 / 3.0)
    rec = dict(schema=sg.E0_DIAG_SCHEMA, verdict=verdict, time_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               out=os.path.realpath(out), np=np_rec, registered=dict(rg), reader=dict(sg.READER_REG), tools=sg.e0_record_tools(),
               runs=runs, checks=checks, refused_kind=(refused or {}).get('kind'),
               soft_range_consistency=[dict(run=n, x_hi_pct=runs[n]['contact']['x_hi_pct'],
                                            soft_predicted_pct=(None if runs[n]['contact']['x_hi_pct'] is None
                                                                else runs[n]['contact']['x_hi_pct'] * k14),
                                            exceeds_soft_range=bool(runs[n]['contact']['x_hi_pct'] is not None
                                                                    and runs[n]['contact']['x_hi_pct'] * k14 > cv.SOFT_RANGE_PCT + cv.SOFT_RANGE_EPS))
                                       for n in dd.DEV_E0[:3] if n in runs],
               vault=dict(file=fp, sha256=fsha),
               blind='M 은 계산하지 않는다 (E0 뿐) · S_R² 원값은 봉인 파일에만 (기록 = 상대 변화) · soft 일관성은 보고만 (범위를 올리지 않는다 · §6)')
    Path(record).parent.mkdir(parents=True, exist_ok=True)
    tmp = str(record) + '.tmp'
    Path(tmp).write_text(json.dumps(rec, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    os.replace(tmp, record)
    _blind_log(vault, dict(time_utc=rec['time_utc'], user=getpass.getuser(), host=socket.gethostname(), mode='e0-diag', full_file=fp,
                           full_sha256=fsha, record=os.path.realpath(record), record_sha256=_sha_file(record), verdict=verdict,
                           wrapper_sha256=_sha_file(__file__), viewed='projection only' if refused is None else 'refusal code only'))
    return (0 if verdict == 'PASS' else 1), rec


def main(argv=None):
    ap = argparse.ArgumentParser(description='bin 0 스모크 M-맹검 래퍼 (Codex 6 차 Q5) · 강성 축 접촉 상태 증서 (--contract)')
    ap.add_argument('run', nargs='?', help='평가 런 폴더 (예 <OUT>/LH_s32452843 · 강성 축 셀 <OUT>/LC_ref_r8_s15485863)')
    ap.add_argument('--ref', help='E0 기준 런 폴더 (회전 팔)')
    ap.add_argument('--cert', help='증서 경로 (관문 rest · confirm-rest 의 입력)')
    ap.add_argument('--contract', action='store_true',
                    help='강성 축 셀: 접촉 상태 증서 (회전 = bin 0 스모크 + contact · E0 = contact + 완주 · --ref 불요) — 사전등록 §6 · §8-2 ⑤')
    ap.add_argument('--phase-receipt', default=None, help='(--contract · 회전 팔) 재개-위상 영수증 — 벽 회전각 근거')
    ap.add_argument('--e0-diag', default=None, metavar='OUT', help='DEV E0 다섯 (강성 축 §8-2 ②) 의 E0 진단 PASS 기록을 쓴다 (--record 필수)')
    ap.add_argument('--record', default=None, help='(--e0-diag) 기록 경로 (예 <OUT>/dev_e0_diag.json — launch_highbo.sh dev-rot 의 인자)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.e0_diag:
        if not a.record or a.run or a.contract:
            ap.error('--e0-diag <OUT> --record <기록> 만 (런 · --contract 와 섞지 않는다)')
        rc, rec = e0_diag(a.e0_diag, a.record)
        ck = rec.get('checks') or {}
        print(f"{'✓' if rc == 0 else '⛔'} E0 진단 {rec['verdict']} → {a.record} · " + ' · '.join(f'{k} {"✓" if v.get("pass") else "✗"}' for k, v in ck.items())
              + (f" · 거부 {rec['refused_kind']}" if rec.get('refused_kind') else '') + ' — M 은 계산하지 않았다 (E0 뿐)')
        return rc
    if a.contract:
        if not (a.run and a.cert):
            ap.error('--contract 는 <run> --cert <cert> 가 필요하다')
        try:
            c_ = dd.parse_cell(os.path.basename(os.path.normpath(a.run)))
        except ValueError as ex:
            print(f'⛔ --contract 는 강성 축 셀 폴더만 — {ex}')
            return 1
        if c_['arm'] != 'E0' and not a.ref:
            ap.error('회전 팔은 --ref <같은 seed · 같은 강성 E0> 가 필요하다')
        for lab, p in (('run', a.run),) + ((('ref', a.ref),) if c_['arm'] != 'E0' else ()):
            if not os.path.isdir(p):
                print(f'⛔ {lab} 폴더 없음: {p}')
                return 1
        rc, s = run_contract_cert(a.run, a.ref, a.cert, phase_receipt=a.phase_receipt)
        if rc == 0:
            print(f"✓ 증서 → {s['cert']} ({s['kind']} · 접촉 상태 {s['status']}) · 전체 결과 봉인 {s['full_file']} (0600 · sha256 "
                  f"{s['full_sha256'][:12]}…) — M 은 화면에 내지 않았다")
        else:
            print(f"⛔ 거부 (사유 코드 {s['refused_kind']}) — 증서 없음.  사유 문구는 봉인 파일 {s['full_file']} 에만 있다")
        return rc
    if not (a.run and a.ref and a.cert):
        ap.error('<run> --ref <ref> --cert <cert> 가 필요하다')
    for lab, p in (('run', a.run), ('ref', a.ref)):
        if not os.path.isdir(p):
            print(f'⛔ {lab} 폴더 없음: {p}')
            return 1
    rc, s = run_blind(a.run, a.ref, a.cert)
    if rc == 0:
        print(f"✓ 증서 → {s['cert']} (complete={s['complete']} · tech_smoke {s['n_tech']} 건 · qc_repr.pass={s['qc_pass']}) · "
              f"전체 결과 봉인 {s['full_file']} (0600 · sha256 {s['full_sha256'][:12]}…) — M 은 화면에 내지 않았다")
    else:
        print(f"⛔ 판독기 거부 (사유 코드 {s['refused_kind']}) — 증서 없음.  사유 문구는 봉인 파일 {s['full_file']} 에만 있다 (열면 blind_log 에 적을 것)")
    return rc


# ──────────────────────────────────────────────────────────────────────────────
def selftest():
    import shutil
    import subprocess
    from mixer_gate_reader_diff import build, REST, FIRST         # 같은 합성 폴더 · 같은 관문 (규율 ①)
    fails = []

    def chk(name, ok):
        print(('  ✓ ' if ok else '  ✗ ') + name)
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory(prefix='smoke_blind_') as tmp:
        td = Path(tmp)
        run, ref, cert, original, invoke = build(td)
        cert.unlink()                                                          # build 가 쓴 '전체' 증서는 버린다 — 래퍼가 다시 쓴다
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        shown = out.getvalue() + err.getvalue()
        e = json.loads(cert.read_text(encoding='utf-8'))[0]
        chk('① 정상: rc 0 · 증서 = 허용목록 정확히 (run · provenance · plan · t0_step · smoke{complete · tech_smoke · qc_repr{pass}})',
            rc == 0 and sorted(e) == sorted(ALLOW_TOP + ('smoke',)) and sorted(e['smoke']) == sorted(ALLOW_SMOKE + ('qc_repr',))
            and list(e['smoke']['qc_repr']) == ['pass'])
        chk('①b 투영 값 = 판독기 값 그대로 (plan · t0_step · provenance 편집 없음)',
            e['plan'] == original['plan'] and e['t0_step'] == original['t0_step'] and e['provenance'] == original['provenance'])
        chk('①c ★ 화면 (stdout · stderr) 에 판독기 출력 · 결과 키 · M 값이 없다',
            not any(k in shown for k in ('M_final', 'S0', 'SR', 'by_rev')) and f"{original['M_final']:.4f}"[:5] not in shown
            and str(original['S0'])[:6] not in shown)
        chk('①d 증서에 결과 키 없음 (leak_check) · 전체 결과는 봉인 파일 (0600) 에 · 열람 기록 1 줄 (projection only · 증서 sha)',
            leak_check(e) == [] and (run / '.smoke_blind').is_dir()
            and all(oct(p.stat().st_mode)[-3:] == '600' for p in (run / '.smoke_blind').glob('full_*.json'))
            and json.loads((run / '.smoke_blind/blind_log.jsonl').read_text(encoding='utf-8').splitlines()[-1])['viewed'] == 'projection only')
        full = json.loads(next((run / '.smoke_blind').glob('full_*.json')).read_text(encoding='utf-8'))
        chk('①e 봉인 파일에는 전체 결과 (M_final · S0 · SR · rows …) 가 있다 = "계산했지만 보지 않았다" (판독기 화면 출력도 같은 파일에 갇힌다)',
            full['result']['M_final'] == original['M_final'] and full['result']['S0'] == original['S0']
            and isinstance(full['reader_stdout'], str) and full['refused'] is None)
        chk('① 관문 (launch_highbo.sh rest 블록) 이 이 증서로 rc 0', invoke()['rc'] == 0)

        src, dup = run / 'post/mix_400.liggghts', run / 'post/copy_400.liggghts'
        shutil.copyfile(src, dup)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc2 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        e2 = json.loads(cert.read_text(encoding='utf-8'))[0]
        chk('② 기술 실패 (bin 0 복제): 래퍼는 판정하지 않고 rc 0 · 증서 complete=false → 관문 rc 1',
            rc2 == 0 and e2['smoke']['complete'] is False and invoke()['rc'] == 1)
        dup.unlink()

        e0dup = ref / 'post/copy_200.liggghts'
        shutil.copyfile(ref / 'post/mix_200.liggghts', e0dup)
        cert.unlink()
        out3 = io.StringIO()
        with contextlib.redirect_stdout(out3), contextlib.redirect_stderr(io.StringIO()):
            rc3 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        logs = [json.loads(l) for l in (run / '.smoke_blind/blind_log.jsonl').read_text(encoding='utf-8').splitlines()]
        chk('③ ★ 판독기 거부 (E0 t₀ 둘): rc 2 · 증서 없음 · 화면에는 사유 코드 (SystemExit) 만 — 거부 문구 (숫자) 는 봉인 파일에',
            rc3 == 2 and not cert.exists() and 'SystemExit' in out3.getvalue() and '계획 t₀' not in out3.getvalue()
            and logs[-1]['viewed'] == 'refusal code only' and logs[-1]['refused_kind'] == 'SystemExit')
        e0dup.unlink()

        #  ④ 누설 시험 — 판독기가 허용 키 안에 결과 대리량을 숨겨 돌려주면 (합성) 증서를 쓰지 않는다
        real = mi.analyse

        def fake(*a_, **k_):
            v = real(*a_, **k_)
            v['smoke']['tech_smoke'] = list(v['smoke']['tech_smoke']) + [{'M_final': v['M_final']}]
            return v
        mi.analyse = fake
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc4 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        finally:
            mi.analyse = real
        chk('④ ★ 허용 키 (tech_smoke) 안에 결과 키가 숨어 오면 Leak 거부 · rc 2 · 증서 없음', rc4 == 2 and not cert.exists())

        #  ⑤ 판독기가 다른 모양 (허용 키 없음) 이면 거부
        mi.analyse = lambda *a_, **k_: {'run': 'x'}
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc5 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        finally:
            mi.analyse = real
        chk('⑤ 판독기 결과에 허용 키가 없으면 ProjectionShape 거부 · rc 2', rc5 == 2 and not cert.exists())

        #  ⑥ 예외 (파일 없음 → 판독기 내부 예외) 도 화면에 traceback 을 내지 않는다
        shutil.rmtree(ref / 'post')
        out6 = io.StringIO()
        with contextlib.redirect_stdout(out6), contextlib.redirect_stderr(io.StringIO()):
            rc6 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        chk('⑥ 판독기 예외/거부: rc 2 · 화면에 Traceback 없음 · 사유 코드만', rc6 == 2 and 'Traceback' not in out6.getvalue())
        #  ⑦ CLI 로도 같은 화면 규율 (서브프로세스 · 정상 폴더 재구성)
        run2, ref2, cert2, orig2, _inv = build(td / 'cli')
        cert2.unlink()
        p = subprocess.run([sys.executable, __file__, str(run2), '--ref', str(ref2), '--cert', str(cert2)],
                           capture_output=True, text=True, encoding='utf-8')
        chk('⑦ CLI 서브프로세스: rc 0 · 증서 · 화면에 M 값 · 결과 키 없음',
            p.returncode == 0 and cert2.is_file() and 'M_final' not in p.stdout + p.stderr
            and f"{orig2['M_final']:.4f}"[:5] not in p.stdout + p.stderr)

    # ══ ⑧~⑭ 2026-09-30 — 강성 축 코드 선행조건 2 단계 piece 3: 접촉 상태 증서 (ref/ref2 = 계약 · soft = 진단 5.8 %) · arm × E × 검사 관문표 ═══
    #    ★ 반례를 먼저 옮겼다 — 옛 래퍼: 상태 필드 · --contract · E0 증서 · 관문표가 없다 (KeyError · argparse) ⇒ ⑧~⑭ 전부 FAIL.
    G = globals()

    def okx(fn):
        try:
            return bool(fn())
        except Exception as e_:                                                   # noqa: BLE001
            print(f'        ({type(e_).__name__}: {str(e_)[:120]})')
            return False

    def _t8():
        gd, tab = G['gate_decision'], G['GATE_TABLE']
        want = {('ref', 'TECH_FAIL'): False, ('ref', 'CONTRACT_MET'): True, ('ref', 'CONTRACT_NOT_MET'): False, ('ref', 'OUT_OF_RANGE'): False,
                ('soft', 'TECH_FAIL'): False, ('soft', 'CONTRACT_MET'): True, ('soft', 'CONTRACT_NOT_MET'): True, ('soft', 'OUT_OF_RANGE'): True}
        rows, bad = [], []
        for arm_ in ('E0', 'LC', 'LH'):
            for lv_ in ('soft', 'ref', 'ref2'):
                for st_ in ('TECH_FAIL', 'CONTRACT_MET', 'CONTRACT_NOT_MET', 'OUT_OF_RANGE'):
                    got = gd(lv_, st_)[0]
                    exp = want[('ref' if lv_ != 'soft' else 'soft', st_)]
                    rows.append((arm_, lv_, st_, got))
                    if got != exp:
                        bad.append((arm_, lv_, st_, got))
        unk = gd('ref', 'PASS')[0] is False and gd('soft', None)[0] is False and gd('hard', 'CONTRACT_MET')[0] is False
        print('        arm × E × 검사 → 관문 (✓ 허용 · ✗ 거부):  ' + '  '.join(f'{a}/{l}/{s_[:12]}={"✓" if g else "✗"}' for a, l, s_, g in rows[:12]) + ' …')
        return not bad and unk and dict(tab) == want and len(rows) == 36
    chk('⑧ ★ arm × E × 검사 관문표 (§6 · Codex 7 차 HBR7-02 해결 증거 · 36 칸) — ref/ref2 (계약 팔): CONTRACT_MET 만 허용 · soft (진단 팔): '
        'TECH_FAIL 만 거부 (CONTRACT_NOT_MET · OUT_OF_RANGE 는 값 보존 · 관문 통과) · E0 · LC · LH 는 수준으로만 갈린다 · 모르는 상태 거부', okx(_t8))

    calls = []
    real_cw = G['cv'].check_window if 'cv' in G else None

    def _fake_cw(status, pp=0.02, extra=None):
        def f(run_dir, n_expected=None, **kw):
            calls.append(dict(run=run_dir, n_expected=n_expected, **{k: v for k, v in kw.items() if k != 'expect_deck'},
                              expect_text=open(kw['expect_deck'], encoding='utf-8').read() if kw.get('expect_deck') else None))
            post = os.path.join(run_dir, 'post')
            fr = sorted(mi.frames(post))[:2] if os.path.isdir(post) else []
            st_ = dict(schema='mixer_contact_status/1', status=status, technical='FAIL' if status == 'TECH_FAIL' else 'OK',
                       original_1pct=None if status == 'TECH_FAIL' else ('MET' if status == 'CONTRACT_MET' else 'NOT_MET'),
                       soft_range=kw.get('soft_range_pct') and ('OUT_OF_RANGE' if status == 'OUT_OF_RANGE' else 'WITHIN'),
                       soft_range_pct=kw.get('soft_range_pct'), x_lo_pct=pp * 100, x_hi_pct=pp * 100, why=[])
            if extra:
                st_.update(extra)
            return dict(verdict='REJECT' if status != 'CONTRACT_MET' else 'PASS', status=st_, bins=sorted(kw['bins']) if kw.get('bins') else None,
                        window=(fr[0][0], fr[-1][0]) if fr else None, n_frames=len(fr), phase_status='static',
                        frames_evaluated=[[int(a_), b_] for a_, b_ in fr], tech=[], reject=[])
        return f

    def _cells(td_):
        """합성 폴더 (build) 를 강성 축 셀 이름으로 — 회전 LC_soft_r8 / LC_ref_r8 · E0 E0_soft / E0_ref (holdout 첫 seed)."""
        run_, ref_, cert_, orig_, _inv = build(td_)
        cert_.unlink()
        s0 = 15485863
        tgt = {}
        for lv_ in ('soft', 'ref'):
            r_ = td_ / f'LC_{lv_}_r8_s{s0}'
            e_ = td_ / f'E0_{lv_}_s{s0}'
            shutil.copytree(run_, r_)
            shutil.copytree(ref_, e_)
            tot = sum(int(x) for x in __import__('re').findall(r'^run\s+(\d+)', (e_ / 'in.mixer').read_text(encoding='utf-8'), __import__('re').M))
            (e_ / 'log.lmp').write_text(f'   Step Atoms KinEng\n{tot - 1:12d} 384 0.0\n{tot:12d} 384 0.0\n', encoding='utf-8')
            tgt[lv_] = (r_, e_)
        return tgt, orig_

    def _t9():
        with tempfile.TemporaryDirectory(prefix='sb_c_') as tmp_:
            td_ = Path(tmp_)
            tgt, orig_ = _cells(td_)
            G['cv'].check_window = _fake_cw('CONTRACT_NOT_MET', pp=0.05)
            try:
                calls.clear()
                out_, err_ = io.StringIO(), io.StringIO()
                with contextlib.redirect_stdout(out_), contextlib.redirect_stderr(err_):
                    rc_ = main([str(tgt['soft'][0]), '--ref', str(tgt['soft'][1]), '--cert', str(td_ / 'c_soft.json'), '--contract'])
                e_ = json.loads((td_ / 'c_soft.json').read_text(encoding='utf-8'))[0]
                c_ = e_['contact']
                k_soft = calls[-1]
                calls.clear()
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    rc2 = main([str(tgt['ref'][0]), '--ref', str(tgt['ref'][1]), '--cert', str(td_ / 'c_ref.json'), '--contract'])
                k_ref = calls[-1]
                e2 = json.loads((td_ / 'c_ref.json').read_text(encoding='utf-8'))[0]
            finally:
                G['cv'].check_window = real_cw
            plan_n = {1: 176, 2: 859, 3: 98965}
            shown = out_.getvalue() + err_.getvalue()
            return (rc_ == 0 and rc2 == 0 and sorted(e_) == sorted(G['ROT_CERT_KEYS']) and c_['schema'] == G['CONTACT_CERT_SCHEMA']
                    and c_['run'] == 'LC_soft_r8_s15485863' and c_['level'] == 'soft' and c_['bins'] == [0] and c_['soft_range_pct'] == 5.8
                    and c_['status']['status'] == 'CONTRACT_NOT_MET' and not mi.verify_frames(str(tgt['soft'][0] / 'post'), c_['frames'])
                    and c_['frames']['files'] and leak_check(e_) == []
                    and k_soft['bins'] == (0,) and k_soft['soft_range_pct'] == 5.8 and k_soft['expect_counts'] == plan_n
                    and os.path.samefile(k_soft['stl_ref_dir'], G['cv'].STL_REF_DIR)
                    and k_soft['expect_text'] == G['dd'].cell_expected_deck('LC_soft_r8_s15485863')
                    and k_ref['soft_range_pct'] is None and e2['contact']['level'] == 'ref' and e2['contact']['soft_range_pct'] is None
                    and e_['plan'] == orig_['plan'] and e_['provenance']['args'] == REG
                    and f"{orig_['M_final']:.4f}"[:5] not in shown and 'M_final' not in shown)
    chk('⑨ ★ --contract 회전 증서 = bin 0 스모크 허용목록 + contact (bins [0] · 상태 · 출처 sha256 · 본 프레임 묶음 — 다시 해시 일치) · soft 는 5.8 % 로 · '
        'ref 는 범위 없이 (계약 팔) 검사기를 부른다 · 계획 상별 수 · 캠페인 STL · 이름에서 재생성한 기대 덱 · 화면에 M 없음', okx(_t9))

    def _t10():
        with tempfile.TemporaryDirectory(prefix='sb_e_') as tmp_:
            td_ = Path(tmp_)
            tgt, _o = _cells(td_)
            G['cv'].check_window = _fake_cw('CONTRACT_MET', pp=0.004)
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    rc_ = main([str(tgt['ref'][1]), '--cert', str(td_ / 'e0.json'), '--contract'])
                e_ = json.loads((td_ / 'e0.json').read_text(encoding='utf-8'))[0]
                lg = tgt['ref'][1] / 'log.lmp'
                lg.write_text(lg.read_text(encoding='utf-8').split('\n')[0] + '\n  100 384 0.0\n', encoding='utf-8')   # 짧은 로그 = 미완주
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    rc2 = main([str(tgt['ref'][1]), '--cert', str(td_ / 'e0b.json'), '--contract'])
                e2 = json.loads((td_ / 'e0b.json').read_text(encoding='utf-8'))[0]
            finally:
                G['cv'].check_window = real_cw
            return (rc_ == 0 and rc2 == 0 and sorted(e_) == sorted(G['E0_CERT_KEYS']) and e_['kind'] == G['E0_CERT_KIND']
                    and e_['contact']['status']['status'] == 'CONTRACT_MET' and e_['contact']['bins'] is None
                    and e_['completion']['complete'] is True and e_['completion']['basis'] == 'last_step'
                    and e2['completion']['complete'] is False and leak_check(e_) == [])
    chk('⑩ ★ E0 증서 (--contract · --ref 없이) = contact (전 창 · 상태) + 완주 (log 마지막 thermo step = run 합 · HBR6-03) — 짧은 로그면 complete false '
        '(래퍼는 판정하지 않는다 · 관문이 거부)', okx(_t10))

    def _t11():
        with tempfile.TemporaryDirectory(prefix='sb_l_') as tmp_:
            td_ = Path(tmp_)
            tgt, _o = _cells(td_)
            G['cv'].check_window = _fake_cw('CONTRACT_MET', extra={'M_final': 0.4})
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    rc_ = main([str(tgt['soft'][0]), '--ref', str(tgt['soft'][1]), '--cert', str(td_ / 'lk.json'), '--contract'])
            finally:
                G['cv'].check_window = real_cw
            return rc_ == 2 and not (td_ / 'lk.json').exists()
    chk('⑪ ★ contact 블록 안에 결과 키 (M_final) 가 숨어 오면 Leak 거부 · rc 2 · 증서 없음 (허용목록 투영 = 상태 필드도 같은 누설 검사)', okx(_t11))

    def _t12():
        with tempfile.TemporaryDirectory(prefix='sb_t_') as tmp_:
            td_ = Path(tmp_)
            tgt, _o = _cells(td_)
            G['cv'].check_window = _fake_cw('TECH_FAIL')
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    rc_ = main([str(tgt['soft'][0]), '--ref', str(tgt['soft'][1]), '--cert', str(td_ / 't.json'), '--contract'])
                e_ = json.loads((td_ / 't.json').read_text(encoding='utf-8'))[0]
            finally:
                G['cv'].check_window = real_cw
            return (rc_ == 0 and e_['contact']['status']['status'] == 'TECH_FAIL'
                    and G['gate_decision']('soft', e_['contact']['status']['status'])[0] is False)
    chk('⑫ 기술 실패 (TECH_FAIL) 도 증서에 그대로 적는다 (래퍼는 판정하지 않는다) — 관문표가 soft 라도 거부한다', okx(_t12))

    def _t13():
        with tempfile.TemporaryDirectory(prefix='sb_n_') as tmp_:
            td_ = Path(tmp_)
            run_, ref_, cert_, _o, _i = build(td_)
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                try:
                    rc_ = main([str(run_), '--ref', str(ref_), '--cert', str(td_ / 'x.json'), '--contract'])
                except SystemExit as e_:
                    rc_ = e_.code
            return rc_ not in (0, None) and not (td_ / 'x.json').exists()
    chk('⑬ --contract 는 강성 축 셀 이름 폴더만 (옛 LH_s… · 프로브 이름 거부 — 수준 · soft 범위를 이름에서 정한다)', okx(_t13))

    def _t14():
        with tempfile.TemporaryDirectory(prefix='sb_x_') as tmp_:
            td_ = Path(tmp_)
            tgt, _o = _cells(td_)
            G['cv'].check_window = _fake_cw('OUT_OF_RANGE', pp=0.07)
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    main([str(tgt['soft'][0]), '--ref', str(tgt['soft'][1]), '--cert', str(td_ / 'o.json'), '--contract'])
                e_ = json.loads((td_ / 'o.json').read_text(encoding='utf-8'))[0]
            finally:
                G['cv'].check_window = real_cw
            logs = [json.loads(l_) for l_ in (tgt['soft'][0] / '.smoke_blind' / 'blind_log.jsonl').read_text(encoding='utf-8').splitlines()]
            full_ = [p_ for p_ in (tgt['soft'][0] / '.smoke_blind').glob('contract_full_*.json')]
            return (e_['contact']['status']['status'] == 'OUT_OF_RANGE' and G['gate_decision']('soft', 'OUT_OF_RANGE')[0] is True
                    and logs[-1]['mode'] == 'contract-cert' and logs[-1]['viewed'] == 'projection only'
                    and full_ and all(oct(p_.stat().st_mode)[-3:] == '600' for p_ in full_))
    chk('⑭ soft OUT_OF_RANGE 는 증서에 그대로 · 관문 통과 (§6 "팔은 완주 · 값 보존 · 짝 블록의 다른 팔 계속") · 전체 결과 (판독기 + 검사기) 는 0600 '
        '봉인 · 열람 기록 mode contract-cert', okx(_t14))
    print()
    if fails:
        print(f'✗ {len(fails)} 건 실패')
        return 1
    print('✓ 전부 통과 — 래퍼는 판독기 출력을 가로채고 허용목록만 투영하며, 거부 · 예외 · 누설을 화면에 내지 않는다.  '
          '⚠ 봉인 파일을 여는 것은 사람의 규율이다 (열람 = blind_log)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
