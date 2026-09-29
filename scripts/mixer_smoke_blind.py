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

★ 2026-09-30 — 중간 판정 **한 번** (사전등록 §5-a v2.5 · 코드 선행조건 2 단계 piece 4):
    python3 scripts/mixer_smoke_blind.py --interim <OUT> --eps <ε 등록.json> [--phase-receipt R]
  확인 회전 12 런이 모두 4 바퀴 (판독기 계획 bin 3 창) 를 지났을 때 — 판독기 bin_window_stats (bin 3 격자 + 계획 t₀ + E0 계획 t₀ **만** 읽는다) →
  d_s = M(LC_ref) − M(LH_ref) · interim_rule (세 seed 양수 ∧ Δ3 − u_mean ≥ 0.10 ∧ ≥ 3·(SE3 + u_SE)) → 허용목록 투영 <OUT>/interim_record.json
  (세 d_s 부호 · Δ3 · SE3 · u 항 · 충족 + d_soft · q 요약 · M-맹검 적격 표) · 전체 결과 0600 봉인 · blind_log (누가 · 언제 · 입력 sha256).
  rc 0 = 봤다 (MET · NOT_MET · INELIGIBLE · TECH — 기록에) · 3 = 사전조건 불성립 (M 미계산 · **소진 아님**: ε 등록 · confirm manifest · 봉인 · 덱 ·
  4 바퀴 전 · ref 접촉 (bin 0–3 창) · ref 바닥 (8×8×2)) · 4 = 이미 봤다 (OUT claim · 기록 · 18 런 표지 — 두 번째 중간 판정은 없다).
  최종 (bin 7 · §5) 판독은 따로다 — 이 모드는 bin 7 을 읽지도 쓰지도 않고, 최종 보고가 interim_record.json 을 무조건 병기한다.
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


# ══ 중간 판정 한 번 (--interim · 2026-09-30 · 강성 축 코드 선행조건 2 단계 piece 4) ═══════════════════════════════════════
#  사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §5-a (v2.5 · 결과 전 등록) — 구현한 문장:
#    "보는 시점 = 한 번: 확인 회전 12 런이 모두 4 바퀴 (판독기 계획 bin 3 창) 를 지난 때.  그 전 · 그 사이에 M 을 보지 않는다 (M-맹검 래퍼 유지).
#     두 번째 중간 판정은 없다."
#    "열람 범위: 중간 판정 때 래퍼가 내놓는 것은 이 절의 통계 (세 d_s 의 부호 · Δ3 · SE3 · 충족 여부) + d_soft(bin 3) · q(bin 3) 의 값 보고용 요약뿐이다 ·
#     M(t) 곡선 전체와 다른 bin 은 최종까지 봉인.  열람 시각 · 파일 sha256 을 기록한다."
#  흐름: ① 이미 본 흔적 (OUT claim · 기록 · 18 런 표지) 이면 rc 4 (소진 — 두 번째 없음)
#        ② M-맹검 사전조건 (못 서면 rc 3 · M 미계산 · **소진 아님**): ε 등록 · 캠페인 동일성 (confirm manifest · 발사 봉인 · 덱) · 덱 코호트 ·
#           12 런 bin 3 계획 격자 완전 + 계획 t₀ · E0 계획 t₀ · 접촉 (회전 = bin 0–3 창 · E0 = 계획 t₀) · 바닥 (8×8×2 ≥ 5)
#           — ref 팔 (LC_ref · LH_ref · E0_ref) 이 접촉 CONTRACT_MET · 바닥 통과가 아니면 조기 확정이 원리상 불가 → M 을 계산하지 않는다
#        ③ claim (O_EXCL · OUT) + 18 런 표지 (O_EXCL) = 소진 — 그 뒤 무슨 일이 나도 기록을 남긴다 (TECH 도 한 번으로 친다)
#        ④ 판독 (판독기 bin_window_stats — bin 3 격자 + 계획 t₀ + E0 계획 t₀ 만) → d_ref · d_soft · q → interim_rule
#        ⑤ 전부 0600 봉인 → 허용목록 투영 = OUT/interim_record.json (O_EXCL) · 화면 · blind_log
#  결과: MET (조기 확정 · 4 바퀴 estimand) · NOT_MET (8 바퀴까지 · §5 최종) · INELIGIBLE (판독 적격 실패 — 8 바퀴까지) · TECH (예외 — 8 바퀴까지).
INTERIM_SCHEMA = 'mixer_interim_look/1'
INTERIM_EPS_SCHEMA = 'mixer_interim_eps/1'
INTERIM_CLAIM_SCHEMA = 'mixer_interim_claim/1'
INTERIM_DIR = '.interim_look'           # OUT/.interim_look/ (0700) · <런>/.interim_look/ (0700)
INTERIM_CLAIM = 'claim.json'            # OUT/.interim_look/claim.json — 있으면 소진
INTERIM_MARKER = 'marker.json'          # <런>/.interim_look/marker.json — 런 폴더가 다른 OUT 으로 가도 한 번 규칙이 따라간다
INTERIM_RECORD = 'interim_record.json'  # OUT/interim_record.json — 허용목록 투영 (= 본 것 전부 · 최종 보고가 무조건 병기)
RC_REFUSED, RC_CONSUMED = 3, 4          # 3 = 사전조건 불성립 (M 미계산 · 소진 아님) · 4 = 이미 봤다 (두 번째 없음)
INTERIM_WINDOW_BINS = tuple(range(mi.INTERIM_BIN + 1))       # 접촉 창 = 계획 t₀ → bin 3 끝 (조기 확정의 관측 창)
INTERIM_TOP = ('schema', 'kind', 'bin', 'revolutions', 'campaign', 'look', 'inputs', 'eligibility', 'statistics', 'outcome', 'next',
               'vault', 'blind')
INTERIM_STATS_REF = ('schema', 'bin', 'seeds', 'n', 'signs', 'delta3', 'se3', 'u_mean', 'u_se', 'lhs', 'mid', 'k_se', 'rhs_se', 'tol',
                     'cond', 'met', 'rule')
INTERIM_STATS_SOFT = ('d_soft', 'q', 'qualifiers', 'why_none', 'note')
INTERIM_RUN_INPUT = ('deck_sha256', 'launch_record_sha256', 'reader_frames', 'ref_frames', 'contact_frames_sha256')
INTERIM_ELIG = ('ok', 'contact', 'floor', 'window', 'qc', 'reasons')
INTERIM_NEXT = {
    'MET': ('조기 확정 — 확인 판정 = "4 바퀴 뒤 LC − LH 차이 · 등록된 중간 판정으로 조기 확정" (4 바퀴 estimand 를 제목 · 표 · 결론에 적는다 · 평탄 조건 '
            '미적용) · 12 런은 멈춰도 된다 (계속 돌리면 8 바퀴 값은 기술 보고만 · 다시 판정하지 않는다)'),
    'NOT_MET': ('8 바퀴까지 계속 — 최종 판정 = §5 그대로 (bin 7 · 2·SE) · 이 중간 값은 최종과 함께 무조건 보고 · 문턱 · seed · 런 길이를 바꾸지 않는다 · '
                '무익 중단 없음 · 8 바퀴 넘어 연장 없음'),
    'INELIGIBLE': ('조기 확정 불가 (판독 적격 실패 — eligibility.reasons) — 8 바퀴까지 계속 · 최종 판정 = §5 그대로 · 이 기록은 최종과 함께 보고'),
    'TECH': ('조기 확정 불가 (기술 실패 — 봉인 파일) — 8 바퀴까지 계속 · 최종 판정 = §5 그대로 · 이 기록은 최종과 함께 보고'),
}


def _rot_cells():
    return [n for n in dd.COHORTS['confirm'] if dd.parse_cell(n)['arm'] != 'E0']


def _e0_of(n):
    c_ = dd.parse_cell(n)
    return f'E0_{c_["level"]}_s{c_["seed"]}'


def _interim_tools():
    return dict(wrapper=_sha_file(__file__), reader=_sha_file(mi.__file__), checker=_sha_file(cv.__file__), deckdiff=_sha_file(dd.__file__),
                stage_gate=_sha_file(sg.__file__))


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')


def load_eps(path):
    """ε 등록 (§5 "seed 별 확정 수치 오차 상한 ε_s … 항목과 값은 결과 전 개발 자료로 배정") → ({seed: ε}, 정보).  fail-closed — ValueError:
    파일 없음 · 스키마 ≠ mixer_interim_eps/1 · registered (등록 위치) 빈칸 · items (항목) 없음 · bins['3'] 없음 (다른 bin 의 값을 옮겨 쓰지 않는다) ·
    seed ≠ 등록 holdout 셋 · 비유한 · 음수 · 불리언.  **0 으로 채우지 않는다** (등록이 명시적으로 0 을 적는 것은 받는다)."""
    if not path:
        raise ValueError('ε 등록 파일이 없다 (--eps) — §5 "ε_s 의 항목과 값은 결과 전 … 배정" (⬜ §10) · 빠진 ε 를 0 으로 채우지 않는다')
    try:
        raw = Path(path).read_bytes()
        d = json.loads(raw)
    except (OSError, ValueError) as e:
        raise ValueError(f'ε 등록 파일을 읽을 수 없다 ({path}: {type(e).__name__})')
    if not isinstance(d, dict) or d.get('schema') != INTERIM_EPS_SCHEMA:
        raise ValueError(f'ε 등록 스키마 ≠ {INTERIM_EPS_SCHEMA}')
    if not (isinstance(d.get('registered'), str) and d['registered'].strip()):
        raise ValueError('ε 등록에 registered (사전등록의 등록 위치 — 결과 전 커밋) 가 없다')
    it = d.get('items')
    if not (isinstance(it, list) and it and all(isinstance(x, str) and x.strip() for x in it)):
        raise ValueError('ε 등록에 items (ε_s 에 든 항목 — 판독기 반올림 · 등록된 결정론적 항) 가 없다')
    b3 = (d.get('bins') or {}).get(str(mi.INTERIM_BIN)) if isinstance(d.get('bins'), dict) else None
    if not isinstance(b3, dict):
        raise ValueError(f'ε 등록에 bin {mi.INTERIM_BIN} 값이 없다 — 다른 bin (예 7) 의 ε 를 bin 3 에 옮겨 쓰지 않는다')
    vals = mi._seed_map(b3, dd.HOLDOUT_SEEDS, f'ε(bin {mi.INTERIM_BIN})', nonneg=True)
    return ({s_: v_ for s_, v_ in zip(dd.HOLDOUT_SEEDS, vals)},
            dict(path=os.path.realpath(path), sha256=_sha_bytes(raw), registered=d['registered'], n_items=len(it)))


def interim_evidence(out):
    """이미 본 흔적 → 경로 목록 (빈 목록 = 아직 안 봤다): OUT claim · OUT 기록 · 18 런 표지."""
    o_ = Path(out)
    ev = [p for p in (o_ / INTERIM_DIR / INTERIM_CLAIM, o_ / INTERIM_RECORD) if p.exists()]
    ev += [o_ / n / INTERIM_DIR / INTERIM_MARKER for n in dd.COHORTS['confirm'] if (o_ / n / INTERIM_DIR / INTERIM_MARKER).exists()]
    return [str(p) for p in ev]


def interim_identity(out):
    """확인 캠페인의 동일성 → (문제, 정보).  confirm-first 가 쓴 confirm_manifest.json (스키마 · complete · 18 칸 = 등록 코호트) · 칸마다 발사 봉인
    sha256 = manifest · 봉인 run/stage = 이름/confirm-first · in.mixer = 봉인의 sha256 (대기 · 실행 중 덱 변경 없음)."""
    pr = []
    mp = Path(out) / 'confirm_manifest.json'
    try:
        raw = mp.read_bytes()
        man = json.loads(raw)
    except (OSError, ValueError) as e:
        return [f'확인 manifest 없음 · 읽기 불가 ({mp}: {type(e).__name__}) — confirm-first 의 캠페인이 아니다'], None
    if not isinstance(man, dict) or man.get('schema') != sg.MANIFEST_SCHEMA or man.get('complete') is not True:
        pr.append(f'확인 manifest 스키마 · complete ≠ {sg.MANIFEST_SCHEMA} · true')
        man = man if isinstance(man, dict) else {}
    cells = {c.get('run'): c for c in man.get('cells') or [] if isinstance(c, dict)}
    if sorted(cells) != sorted(dd.COHORTS['confirm']):
        pr.append(f'manifest 칸 {len(cells)} ≠ 등록 확인 코호트 18')
    info = dict(manifest=dict(path=os.path.realpath(mp), sha256=_sha_bytes(raw)), cells={})
    for n in dd.COHORTS['confirm']:
        d = Path(out) / n
        lr_sha = sg.sha_or_none(str(d / 'launch_record.json'))
        if lr_sha is None or (cells.get(n) or {}).get('launch_record_sha256') != lr_sha:
            pr.append(f'{n}: 발사 봉인이 manifest 와 다르다 (없거나 다시 봉인됐다)')
        lr = sg._seal(str(d)) or {}
        if lr.get('run') != n or lr.get('stage') != 'confirm-first':
            pr.append(f'{n}: 발사 봉인 run/stage {lr.get("run")!r}/{lr.get("stage")!r} ≠ {n}/confirm-first')
        deck = sg.sha_or_none(str(d / 'in.mixer'))
        if deck is None or (lr.get('sha256') or {}).get('in.mixer') != deck:
            pr.append(f'{n}: in.mixer ≠ 발사 봉인 (봉인 뒤 바뀌었거나 없다)')
        info['cells'][n] = dict(launch_record_sha256=lr_sha, deck_sha256=deck)
    return pr, info


def interim_window_problems(run_dir, name=None, e0=False):
    """런 하나의 중간 판정 창 사전조건 → 문제 목록 — 계획 t₀ 덤프 정확히 한 장 · (회전) bin 3 계획 격자 완전 (결손 = 아직 4 바퀴 전 · 중복 ·
    격자 밖 없음).  파일 이름 · 계획 격자만 본다 (M 미계산) — 판독기와 같은 식 (bin_window_files) · mixer_gate_reader_diff 가 전체 판독기와 대조한다."""
    n = name or os.path.basename(os.path.normpath(run_dir))
    try:
        pl = mi.deck_plan(os.path.join(run_dir, 'in.mixer'))
        t0 = mi.planned_t0(pl)
    except (OSError, ValueError, AttributeError) as e:
        return [f'{n}: 덱 계획을 못 읽었다 ({type(e).__name__})']
    pr = []
    post = os.path.join(run_dir, 'post')
    fr = mi.frames(post) if os.path.isdir(post) else []
    k0 = sum(1 for st, _ in fr if st == t0)
    if k0 != 1:
        pr.append(f'{n}: 계획 t₀ {t0} 의 덤프가 {k0} 장 (정확히 1 장이어야 한다)')
    if e0:
        return pr
    w = mi.bin_window_files(post, t0, pl['steps_per_rev'], pl['dump_every'], pl['steps_total'], (mi.INTERIM_BIN,))
    if not w['lattice']:
        pr.append(f'{n}: bin {mi.INTERIM_BIN} 계획 격자가 없다 (덱의 계획 바퀴 수)')
    if w['miss']:
        pr.append(f'{n}: 아직 4 바퀴 전 — bin {mi.INTERIM_BIN} 계획 덤프 결손 {len(w["miss"])}/{len(w["lattice"])} (§5-a "12 런이 모두 4 바퀴를 지난 때")')
    if w['dup'] or w['off']:
        pr.append(f'{n}: bin {mi.INTERIM_BIN} 창 입력 집합 — 중복 {w["dup"][:3]} · 격자 밖 {w["off"][:3]}')
    return pr


def interim_windows(out):
    """12 회전 런 + 6 E0 의 창 사전조건 (interim_window_problems) → 문제 목록."""
    pr = []
    for n in dd.COHORTS['confirm']:
        pr += interim_window_problems(os.path.join(out, n), n, e0=n.startswith('E0_'))
    return pr


def interim_contact(out, phase_receipt=None):
    """18 셀 접촉 상태 (M 과 무관) — 회전 = bin 0–3 창 (계획 t₀ → bin 3 끝 · 그 bin 들의 계획 격자 전부) · E0 = 계획 t₀ (정지 벽 계약).
    → ({이름: 요약}, {이름: 전체})."""
    summ, full = {}, {}
    for n in dd.COHORTS['confirm']:
        c_ = dd.parse_cell(n)
        rot = c_['arm'] != 'E0'
        try:
            w, block = contact_eval(os.path.join(out, n), n, bins=INTERIM_WINDOW_BINS if rot else None,
                                    phase_receipt=phase_receipt if rot else None)
            summ[n] = dict(level=c_['level'], arm=c_['arm'], status=(block.get('status') or {}).get('status'), bins=block.get('bins'),
                           frames_sha256=(block.get('frames') or {}).get('sha256'), checker_sha256=block.get('checker_sha256'))
            full[n] = w
        except (SystemExit, Exception) as e:                            # noqa: BLE001 — 검사 불능 = 기술 실패 (통과가 아니다)
            summ[n] = dict(level=c_['level'], arm=c_['arm'], status='TECH_FAIL', error=type(e).__name__)
            full[n] = dict(error=type(e).__name__, message=str(e))
    return summ, full


def interim_floor(out, reg=REG):
    """12 회전 런의 바닥 검사 (8×8×2 · S₀²/S_R² ≥ 5 · 같은 강성 · seed E0) → {이름: t0_floor 결과} — 계획 t₀ 두 장만 연다 (M(t) 와 무관)."""
    res = {}
    for n in _rot_cells():
        try:
            res[n] = mi.t0_floor(os.path.join(out, n), os.path.join(out, _e0_of(n)), reg['r_container'], n_min=reg['n_min'], axis=reg['axis'])
        except (SystemExit, Exception) as e:                            # noqa: BLE001
            res[n] = {'ratio': None, 'pass': False, 'error': type(e).__name__}
    return res


def _excl_json(path, obj, mode=0o600):
    """O_EXCL 로 새 파일에 JSON (있으면 FileExistsError) → sha256."""
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1, default=str)
        fh.write('\n')
    os.chmod(path, mode)
    return _sha_file(path)


def interim_projection_problems(p):
    """허용목록 투영 (interim_record.json) 의 모양 → 문제 목록 (빈 목록 = 통과).  최상위 · statistics.ref · soft · 요약 · 런별 입력 · 적격 표의 키가
    **정확히** 등록 목록이어야 하고, 어디에도 결과 키 (M · rows · S0 · SR …) 가 없어야 한다 — seed 별 값 · 런별 M 이 숨을 자리가 없다."""
    pr = []
    if not isinstance(p, dict):
        return ['투영이 JSON 객체가 아니다']
    if sorted(p) != sorted(INTERIM_TOP):
        pr.append(f'최상위 키 {sorted(set(p) ^ set(INTERIM_TOP))} ≠ 허용목록')
    st = p.get('statistics') if isinstance(p.get('statistics'), dict) else {}
    if sorted(st) != ['ref', 'soft']:
        pr.append(f'statistics 키 {sorted(st)} ≠ [ref, soft]')
    ref = st.get('ref')
    if ref is not None and (not isinstance(ref, dict) or sorted(ref) != sorted(INTERIM_STATS_REF)):
        pr.append(f'statistics.ref 키 ≠ 허용목록 ({sorted(set(ref or {}) ^ set(INTERIM_STATS_REF))})')
    if isinstance(ref, dict) and (sorted(ref.get('cond') or {}) != ['all_positive', 'mid', 'se']
                                  or any(v not in ('+', '−', '0') for v in (ref.get('signs') or {}).values())):
        pr.append('statistics.ref cond · signs 모양')
    so = st.get('soft')
    if not isinstance(so, dict) or sorted(so) != sorted(INTERIM_STATS_SOFT):
        pr.append(f'statistics.soft 키 ≠ 허용목록 ({sorted(set(so or {}) ^ set(INTERIM_STATS_SOFT))})')
    else:
        for k in ('d_soft', 'q'):
            v = so.get(k)
            if v is not None and (not isinstance(v, dict) or sorted(v) != ['mean', 'n', 'se']):
                pr.append(f'statistics.soft.{k} 키 {sorted(v) if isinstance(v, dict) else type(v).__name__} ≠ [mean, n, se]')
    runs = (p.get('inputs') or {}).get('runs') if isinstance(p.get('inputs'), dict) else None
    if not isinstance(runs, dict) or sorted(runs) != sorted(_rot_cells()):
        pr.append('inputs.runs ≠ 12 회전 런')
    else:
        for n, v in runs.items():
            if not isinstance(v, dict) or sorted(v) != sorted(INTERIM_RUN_INPUT):
                pr.append(f'inputs.runs.{n} 키 ≠ 허용목록 ({sorted(set(v or {}) ^ set(INTERIM_RUN_INPUT))})')
    el = p.get('eligibility')
    if not isinstance(el, dict) or sorted(el) != sorted(INTERIM_ELIG):
        pr.append(f'eligibility 키 ≠ 허용목록 ({sorted(set(el or {}) ^ set(INTERIM_ELIG))})')
    lk = leak_check(p) + sorted(k for k in _keys(p) if k in ('M_bin', 'M_sd', 'M_mean', 'd_ref', 'per_seed', 'd_by_seed', 'values'))
    if lk:
        pr.append(f'결과 키 {sorted(set(lk))}')
    return pr


def _run_input(identity, contact, per, n):
    r = per.get(n) or {}
    pv = r.get('provenance') if isinstance(r.get('provenance'), dict) else {}
    return dict(deck_sha256=identity['cells'][n]['deck_sha256'], launch_record_sha256=identity['cells'][n]['launch_record_sha256'],
                reader_frames=(pv.get('run') or {}).get('frames'), ref_frames=(pv.get('ref') or {}).get('frames'),
                contact_frames_sha256=(contact.get(n) or {}).get('frames_sha256'))


def interim_look(out, eps_path, phase_receipt=None, reg=REG):
    """§5-a 중간 판정 한 번 → (rc, 요약 dict).  rc 0 = 봤다 (기록 · 봉인) · 3 = 사전조건 불성립 (M 미계산 · 소진 아님) · 4 = 이미 봤다."""
    out = os.path.normpath(out)
    vdir = Path(out) / INTERIM_DIR
    base_log = dict(user=getpass.getuser(), host=socket.gethostname(), tool=os.path.realpath(__file__),
                    wrapper_sha256=_sha_file(__file__), mode='interim', out=os.path.realpath(out))

    def _log(entry):
        vdir.mkdir(parents=True, exist_ok=True)
        os.chmod(vdir, 0o700)
        _blind_log(vdir, dict(base_log, time_utc=_now(), **entry))
    #  ① 한 번 규칙 — 이미 본 흔적이면 아무것도 계산하지 않는다
    ev = interim_evidence(out)
    if ev:
        _log(dict(event='refused-consumed', viewed='nothing (second interim look refused)', evidence=ev))
        return RC_CONSUMED, dict(evidence=ev)
    #  ② M-맹검 사전조건 — 못 서면 M 을 계산하지 않고 돌아간다 (소진 아님)
    why = []
    try:
        eps, eps_info = load_eps(eps_path)
    except ValueError as e:
        eps, eps_info = None, None
        why.append(str(e))
    id_pr, identity = interim_identity(out)
    why += id_pr
    coh = dd.check_cohort(out, 'confirm')
    if coh.get('verdict') != 'PASS':
        why.append('덱 코호트 (confirm) ≠ PASS — ' + '; '.join(
            [f'{n}: {v["problems"][0]}' for n, v in (coh.get('dirs') or {}).items() if v.get('problems')][:3]
            + [f'{p_["ref"]}→{p_["new"]} {p_["verdict"]}' for p_ in coh.get('pairs') or [] if p_.get('verdict') != 'PASS'][:2]
            + ([coh['guard']] if coh.get('guard') else [])))
    why += interim_windows(out)
    contact, contact_full, floor = {}, {}, {}
    rx = None
    if phase_receipt:
        rx = dict(path=os.path.realpath(phase_receipt), sha256=sg.sha_or_none(phase_receipt))
    if not why:                                                   # 접촉 · 바닥은 무거우니 앞의 조건이 선 뒤에만
        contact, contact_full = interim_contact(out, phase_receipt)
        floor = interim_floor(out, reg)
        for n, v in contact.items():
            if v['level'] != 'soft' and v['status'] != 'CONTRACT_MET':
                why.append(f'조기 확정 불가 — {n} 접촉 {v["status"]} (ref 팔 · E0_ref 는 창 t₀ → bin 3 끝에서 CONTRACT_MET 이어야 · §6 "실패면 해당 '
                           f'확인 주장 HOLD")')
        for n, v in floor.items():
            if dd.parse_cell(n)['level'] != 'soft' and not v.get('pass'):
                why.append(f'조기 확정 불가 — {n} 바닥 검사 (8×8×2 S₀²/S_R² ≥ 5) 불합격')
    if why:
        pre_p, pre_sha = (_vault(vdir, 'precheck', dict(schema='mixer_interim_precheck/1', out=os.path.realpath(out), why=why,
                                                         contact=contact, contact_full=contact_full, floor=floor, eps=eps_info, cohort=coh))
                          if (contact or floor) else (None, None))
        _log(dict(event='refused-precondition', viewed='refusal reasons only (M not computed · look not consumed)', why=why,
                  precheck_file=pre_p, precheck_sha256=pre_sha))
        return RC_REFUSED, dict(why=why)
    #  ③ 소진 — claim (OUT) 먼저 (동시 실행은 여기서 하나만 산다) · 18 런 표지
    vdir.mkdir(parents=True, exist_ok=True)
    os.chmod(vdir, 0o700)
    look = dict(time_utc=_now(), user=getpass.getuser(), host=socket.gethostname(), tool=os.path.realpath(__file__), tools=_interim_tools())
    claim = dict(schema=INTERIM_CLAIM_SCHEMA, kind='interim', bin=mi.INTERIM_BIN, out=os.path.realpath(out), look=look,
                 manifest=identity['manifest'], eps=eps_info, phase_receipt=rx)
    cp = vdir / INTERIM_CLAIM
    try:
        claim_sha = _excl_json(cp, claim)
    except FileExistsError:
        _log(dict(event='refused-consumed', viewed='nothing (claim race)', evidence=[str(cp)]))
        return RC_CONSUMED, dict(evidence=[str(cp)])
    marker_err = []
    for n in dd.COHORTS['confirm']:
        md = Path(out) / n / INTERIM_DIR
        md.mkdir(exist_ok=True)
        os.chmod(md, 0o700)
        try:
            _excl_json(md / INTERIM_MARKER, dict(schema=INTERIM_CLAIM_SCHEMA, kind='interim', run=n, out=os.path.realpath(out),
                                                 claim_sha256=claim_sha, time_utc=look['time_utc']))
        except FileExistsError:
            marker_err.append(n)
    _log(dict(event='claim', viewed='nothing yet (look claimed — consumed from here)', claim=str(cp), claim_sha256=claim_sha,
              marker_conflict=marker_err))
    #  ④ 판독 (소진 뒤 — 어떤 실패도 기록으로 남긴다 · 중단 (Ctrl-C) 도 TECH 기록을 쓴 뒤 끝난다)
    buf_out, buf_err = io.StringIO(), io.StringIO()
    per, fatal = {}, None
    seeds = tuple(dd.HOLDOUT_SEEDS)
    rule, dref, dsoft, q = None, {}, {}, {}
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        try:
            if marker_err:
                raise RuntimeError(f'런 표지가 이미 있다 {marker_err} (동시 실행 · 복사) — 판독하지 않는다')
            for n in _rot_cells():
                try:
                    per[n] = mi.bin_window_stats(os.path.join(out, n), os.path.join(out, _e0_of(n)), reg['r_container'], mi.INTERIM_BIN,
                                                 cells=reg['cells'], x_cells=reg['x_cells'], n_min=reg['n_min'], axis=reg['axis'])
                except SystemExit as e:
                    per[n] = dict(refused=dict(kind='SystemExit', message=str(e)))
                except Exception as e:                                  # noqa: BLE001
                    per[n] = dict(refused=dict(kind=type(e).__name__, message=str(e), traceback=traceback.format_exc()))

            def mval(n_):
                r_ = per.get(n_) or {}
                return r_.get('M_bin') if (not r_.get('refused') and r_.get('complete')) else None
            for s_ in seeds:
                a_, b_ = mval(f'LC_ref_r8_s{s_}'), mval(f'LH_ref_r8_s{s_}')
                c_, e_ = mval(f'LC_soft_r8_s{s_}'), mval(f'LH_soft_r8_s{s_}')
                dref[s_] = (a_ - b_) if (a_ is not None and b_ is not None) else None
                dsoft[s_] = (c_ - e_) if (c_ is not None and e_ is not None) else None
                q[s_] = (dsoft[s_] - dref[s_]) if (dsoft[s_] is not None and dref[s_] is not None) else None
            if all(v is not None for v in dref.values()):
                rule = mi.interim_rule(dref, eps, seeds)
        except BaseException as e:                                      # noqa: BLE001 — 소진 뒤에는 무엇이 나도 TECH 기록을 남긴다
            fatal = dict(kind=type(e).__name__, message=str(e), traceback=traceback.format_exc())
    #  적격 (판독 뒤) — ref 팔: 창 완전 · 유한 · tech 없음 · D-2 QC
    reasons, window, qc = [], {}, {}
    for n in _rot_cells():
        r_ = per.get(n) or {}
        window[n] = bool(r_ and not r_.get('refused') and r_.get('complete') and not r_.get('tech'))
        qc[n] = bool((r_.get('qc_repr') or {}).get('pass') is True)
        if dd.parse_cell(n)['level'] == 'soft':
            continue
        if not r_ or r_.get('refused'):
            reasons.append(f'{n}: 판독기 거부 ({(r_.get("refused") or {}).get("kind", "없음")}) — 사유는 봉인 파일')
        elif not window[n]:
            reasons.append(f'{n}: bin {mi.INTERIM_BIN} 창 판독 기술 실패 ({len(r_.get("tech") or [])} 건 · 봉인 파일)')
        elif not qc[n]:
            reasons.append(f'{n}: 부피 누락 QC (D-2) 미달 — 선택-셀 M · 조기 확정 결론 불가')
    if fatal:
        outcome = 'TECH'
        reasons.append(f'기술 실패 ({fatal["kind"]}) — 봉인 파일')
    elif reasons or rule is None:
        outcome = 'INELIGIBLE'
    else:
        outcome = 'MET' if rule['met'] else 'NOT_MET'
    #  soft 요약 (값 보고 · 판정 아님) — 세 seed 가 다 유효할 때만 · 한정어
    soft_ok, quals = True, []
    for s_ in seeds:
        cells_ = (f'LC_soft_r8_s{s_}', f'LH_soft_r8_s{s_}', f'E0_soft_s{s_}')
        if dsoft.get(s_) is None or any((contact.get(c_) or {}).get('status') in (None, 'TECH_FAIL') for c_ in cells_):
            soft_ok = False
        for c_ in cells_:
            if (contact.get(c_) or {}).get('status') == 'OUT_OF_RANGE':
                quals.append(f'{c_}: soft 진단 범위 5.8 % 초과 (OUT_OF_RANGE) — soft 수준 d 는 이 한정어와 함께')
        for c_ in cells_[:2]:
            if not (floor.get(c_) or {}).get('pass'):
                quals.append(f'{c_}: 바닥 검사 (8×8×2 S₀²/S_R² ≥ 5) 불합격')
            if window.get(c_) and not qc.get(c_):
                quals.append(f'{c_}: 부피 누락 QC (D-2) 미달 — 선택-셀 M')
    d_soft_sum = mi.value_summary(dsoft, seeds) if soft_ok else None
    q_sum = mi.value_summary(q, seeds) if soft_ok else None
    why_none = None
    if not soft_ok:
        why_none = ('soft 요약 없음 — 세 seed 중 soft 판독 · 접촉 (TECH_FAIL) · E0_soft 가 서지 않은 seed 가 있다 (§8-4 — 부분 요약을 만들지 않는다) · '
                    'q 도 없음')
    elif q_sum is None:
        why_none = 'q 요약 없음 — d_ref 가 서지 않은 seed 가 있다 (ref 판독 적격 실패 · §8-4 "ref 팔 실패 → 그 seed 의 d_ref · q 둘 다 무효")'
    stats = dict(ref={k: copy.deepcopy(rule[k]) for k in INTERIM_STATS_REF} if rule else None,
                 soft=dict(d_soft=d_soft_sum, q=q_sum, qualifiers=quals, why_none=why_none,
                           note='값 보고용 요약 (평균 · SE · n) — 판정 아님 · soft 는 원 1 % NOT_MET 이 보존되는 계약 밖 진단 (§6) · q 동등성 판정은 bin 7 에서만'))
    vault_rec = dict(schema='mixer_interim_full/1', out=os.path.realpath(out), claim=dict(path=str(cp), sha256=claim_sha), reg=dict(reg),
                     eps=dict(info=eps_info, values={str(k): v for k, v in (eps or {}).items()}), per_run=per,
                     d_ref={str(k): v for k, v in dref.items()}, d_soft={str(k): v for k, v in dsoft.items()}, q={str(k): v for k, v in q.items()},
                     rule=rule, contact=contact, contact_full=contact_full, floor=floor, cohort=coh, reader_stdout=buf_out.getvalue(),
                     reader_stderr=buf_err.getvalue(), fatal=fatal, marker_conflict=marker_err, outcome=outcome, reasons=reasons)
    vp, vsha = _vault(vdir, 'interim_full', vault_rec)
    proj = dict(schema=INTERIM_SCHEMA, kind='interim', bin=mi.INTERIM_BIN, revolutions=mi.INTERIM_BIN + 1,
                campaign=dict(out=os.path.realpath(out), manifest=identity['manifest']),
                look=dict(look, viewed_utc=_now()), inputs=dict(eps=eps_info, phase_receipt=rx, claim=dict(path=str(cp), sha256=claim_sha),
                                                                runs={n: _run_input(identity, contact, per, n) for n in _rot_cells()}),
                eligibility=dict(ok=bool(outcome in ('MET', 'NOT_MET')), contact={n: v['status'] for n, v in contact.items()},
                                 floor={n: bool(v.get('pass')) for n, v in floor.items()}, window=window, qc=qc, reasons=reasons),
                statistics=stats, outcome=outcome, next=INTERIM_NEXT[outcome], vault=dict(file=vp, sha256=vsha),
                blind=('§5-a 허용목록 투영 — 세 d_s 의 부호 · Δ3 · SE3 · u 항 · 충족 + d_soft · q 요약 (평균 · SE · n) 만.  seed 별 d · 런별 M · 프레임별 M · '
                       'M(t) · 다른 bin 은 봉인 파일에만 (bin 3 밖 프레임은 읽지도 않았다) · 봉인 파일을 여는 것은 사람의 규율 (blind_log)'))
    bad = interim_projection_problems(proj)
    if bad:                                                        # 투영기가 스스로 허용목록을 어겼다 — 값 · 런별 입력을 비우고 TECH 로만 남긴다
        proj = dict(proj, outcome='TECH', next=INTERIM_NEXT['TECH'],
                    inputs=dict(eps=eps_info, phase_receipt=rx, claim=dict(path=str(cp), sha256=claim_sha),
                                runs={n: dict.fromkeys(INTERIM_RUN_INPUT) for n in _rot_cells()}),
                    statistics=dict(ref=None, soft=dict(d_soft=None, q=None, qualifiers=[], why_none='투영 모양 실패', note=stats['soft']['note'])),
                    eligibility=dict(ok=False, contact={}, floor={}, window={}, qc={},
                                     reasons=reasons + [f'투영 모양 실패 ({len(bad)} 건 — 내용은 blind_log · 기록에 옮기지 않는다)']))
    rp = Path(out) / INTERIM_RECORD
    body = json.dumps(proj, ensure_ascii=False, indent=1, default=str) + '\n'
    fd = os.open(rp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        fh.write(body)
    _log(dict(event='look', viewed='interim allow-list projection', outcome=proj['outcome'], record=str(rp), record_sha256=_sha_file(rp),
              vault_file=vp, vault_sha256=vsha, claim_sha256=claim_sha, projected_fields=list(INTERIM_TOP), projection_problems=bad))
    return 0, dict(record=str(rp), projection=proj)


def interim_screen(rc, s):
    """화면 문구 — 허용목록 투영 (rc 0) · 거부 사유 (rc 3 · M 미계산) · 흔적 (rc 4) 만."""
    if rc == RC_CONSUMED:
        return [f'⛔ 중간 판정은 이미 한 번 했다 — 두 번째 중간 판정은 없다 (§5-a).  흔적: {s["evidence"][:3]}  (최종은 bin 7 · §5 로 따로)']
    if rc == RC_REFUSED:
        return (['⛔ 중간 판정 사전조건 불성립 — M 을 계산하지 않았다 · 소진되지 않았다 (조건이 서면 다시):']
                + [f'   ✗ {w}' for w in s['why'][:20]] + ([f'   … 외 {len(s["why"]) - 20} 건'] if len(s['why']) > 20 else []))
    p = s['projection']
    st = p['statistics']
    L = [f'★ 중간 판정 (bin {p["bin"]} · {p["revolutions"]} 바퀴) — 결과 {p["outcome"]}']
    r = st['ref']
    if r:
        c = r['cond']
        L += ['   세 seed d_s 부호: ' + ' · '.join(f'{s_} {v}' for s_, v in r['signs'].items()),
              f'   Δ3 = {r["delta3"]:.4f} · SE3 = {r["se3"]:.4f} · u_mean = {r["u_mean"]:.4g} · u_SE = {r["u_se"]:.4g}',
              f'   조건: 모두 양수 {"✓" if c["all_positive"] else "✗"} · Δ3 − u_mean ≥ {r["mid"]} {"✓" if c["mid"] else "✗"} · '
              f'Δ3 − u_mean ≥ {r["k_se"]:g}·(SE3 + u_SE) = {r["rhs_se"]:.4f} {"✓" if c["se"] else "✗"}']
    else:
        L.append('   ref 통계 없음 (판독 적격 실패 — 사유 아래)')
    so = st['soft']

    def _ms(v):
        return f'{v["mean"]:.4f} ± {v["se"]:.4f} (n {v["n"]})' if isinstance(v, dict) else '없음'
    L.append(f'   soft 요약 (값 보고 · 판정 아님): d_soft {_ms(so["d_soft"])} · q {_ms(so["q"])}'
             + (f' · 한정어 {len(so["qualifiers"])} 건' if so['qualifiers'] else '') + (f' — {so["why_none"]}' if so['why_none'] else ''))
    L += [f'   ✗ {w}' for w in p['eligibility']['reasons'][:10]]
    L += [f'   다음: {p["next"]}', f'   기록 → {s["record"]} · 전체 결과 봉인 → {p["vault"]["file"]} (0600 · sha256 {p["vault"]["sha256"][:12]}…)']
    return L


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
    ap.add_argument('--interim', default=None, metavar='OUT',
                    help='확인 캠페인 OUT 의 중간 판정 **한 번** (강성 축 §5-a · bin 3 = 4 바퀴) — 허용목록 투영 → <OUT>/interim_record.json · '
                         'rc 0 봤다 · 3 사전조건 불성립 (M 미계산 · 소진 아님) · 4 이미 봤다')
    ap.add_argument('--eps', default=None, help='(--interim) ε 등록 JSON (mixer_interim_eps/1 · bins["3"] = holdout seed 별 ε_s · 결과 전 등록)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.interim:
        if a.run or a.contract or a.e0_diag or a.cert or a.ref or a.record:
            ap.error('--interim <OUT> --eps <ε 등록> [--phase-receipt R] 만 (다른 방식과 섞지 않는다)')
        if not os.path.isdir(a.interim):
            print(f'⛔ OUT 폴더 없음: {a.interim}')
            return 1
        rc, s = interim_look(a.interim, a.eps, phase_receipt=a.phase_receipt)
        try:
            print('\n'.join(interim_screen(rc, s)))
        except Exception as e:                                         # noqa: BLE001 — 기록 · 봉인은 이미 썼다 (화면 문구 실패가 판정을 바꾸지 않는다)
            print(f'⚠ 화면 문구 실패 ({type(e).__name__}) — rc {rc} · 기록 {s.get("record")} 을 연다')
        return rc
    if a.eps:
        ap.error('--eps 는 --interim 과 함께만')
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

    # ══ ⑮~㉓ 2026-09-30 — 강성 축 코드 선행조건 2 단계 piece 4: 중간 판정 한 번 (--interim · 사전등록 §5-a · bin 3 = 4 바퀴) ═══════════
    #    ★ 반례를 먼저 옮겼다 — 옛 래퍼: --interim 없음 (argparse 거부) · 상수 · 투영 검사 없음 ⇒ ⑮~㉓ 전부 FAIL.
    #    고정물 = 합성 확인 캠페인 (18 셀 = 등록 덱 · 캠페인 STL · 봉인 · confirm_manifest) · 검사기만 대역 (M 과 무관) · 판독기는 **진짜**.
    #    구름: 4 모서리 × 4 x-슬랩 × 24 알 (16×16×4 칸마다 24 ≥ n_min · r 0.013138) · 앞 두 모서리 AM a 알 · 뒤 두 모서리 24 − a 알 ⇒
    #    M(a) = (0.25 − ((a − 12)/24)²)/(0.25 − 1/144) (t₀ = 층상 a 24 · E0 = a 10).  bin 3 밖 (t₀ 제외) 은 **쓰레기** — 판독기가 열면 값이 없어진다.
    import numpy as np
    from mixer_gate_reader_diff import _dump as _gdump
    SEEDS = tuple(dd.HOLDOUT_SEEDS)
    ROT = [n_ for n_ in dd.COHORTS['confirm'] if not n_.startswith('E0_')]

    def _Ma(a):
        return (0.25 - ((a - 12) / 24.0) ** 2) / (0.25 - 1.0 / 144.0)

    def _icloud(a, sparse=False):
        P, types, rad = [], [], []
        for j, (y, z) in enumerate([(-.008, -.008), (-.008, .008), (.008, -.008), (.008, .008)]):
            for x in (-.003, -.001, .001, .003):
                for k in range(24):
                    P.append([x, y, z]); types.append(1 if k < (a if j < 2 else 24 - a) else 3); rad.append(1e-5)
        if sparse:                                            # 가운데 칸에 큰 SE 19 알 (n_min 미만 → 버린 칸) ⇒ SE 유지 부피 < 0.9 = D-2 QC 미달
            for k in range(19):
                P.append([0.0, 0.0, 0.0]); types.append(3); rad.append(3e-5)
        P = np.asarray(P)
        n = len(P)
        return dict(id=np.arange(1, n + 1), type=np.asarray(types), x=P[:, 0], y=P[:, 1], z=P[:, 2], radius=np.asarray(rad))

    #  설계 (seed 순서 = 등록 holdout 순서) — ref: d = M(9)−M(4) · M(8)−M(5) · M(9)−M(5) > 0 ⇒ MET (ε 0) · soft: d = M(6)−M(5) · M(8)−M(5) · M(6)−M(4)
    LC_REF, LH_REF, LC_SOFT, LH_SOFT = (9, 8, 9), (4, 5, 5), (6, 8, 6), (5, 5, 4)
    EPS_OK = {'3': {str(s_): 0.0 for s_ in SEEDS}}

    def _ifix(td_, lc_ref=LC_REF, lh_ref=LH_REF, lc_soft=LC_SOFT, lh_soft=LH_SOFT, t0_a=None, sparse=(), eps_bins=EPS_OK):
        out_ = Path(td_) / 'OUT'
        for n_ in dd.COHORTS['confirm']:
            sg._fx_cell(str(out_), n_)
            sg._fx_seal(str(out_), n_, 'confirm-first', 5)
        cells_ = [dict(run=n_, launch_record_sha256=_sha_file(out_ / n_ / 'launch_record.json')) for n_ in dd.COHORTS['confirm']]
        (out_ / 'confirm_manifest.json').write_text(json.dumps(dict(schema=sg.MANIFEST_SCHEMA, complete=True, cells=cells_)), encoding='utf-8')
        A = {}
        for i_, s_ in enumerate(SEEDS):
            A[f'LC_ref_r8_s{s_}'], A[f'LH_ref_r8_s{s_}'] = lc_ref[i_], lh_ref[i_]
            A[f'LC_soft_r8_s{s_}'], A[f'LH_soft_r8_s{s_}'] = lc_soft[i_], lh_soft[i_]
        for n_, a_ in A.items():
            post_ = out_ / n_ / 'post'
            post_.mkdir(exist_ok=True)
            pl = mi.deck_plan(str(out_ / n_ / 'in.mixer'))
            t0 = mi.planned_t0(pl)
            _gdump(post_ / f'mix_{t0}.liggghts', t0, _icloud((t0_a or {}).get(n_, 24)))
            for b_ in range(5):
                lat = sorted(mi.bin_window_files(str(post_), t0, pl['steps_per_rev'], pl['dump_every'], pl['steps_total'], (b_,))['lattice'])
                for st in (lat[:1] if b_ == 4 else lat):
                    if st == t0:
                        continue
                    if b_ == 3:
                        _gdump(post_ / f'mix_{st}.liggghts', st, _icloud(a_, sparse=n_ in sparse))
                    else:
                        (post_ / f'mix_{st}.liggghts').write_text('쓰레기 — 중간 판정의 판독기는 이 파일을 열면 안 된다\n', encoding='utf-8')
        for s_ in SEEDS:
            for lv_ in ('soft', 'ref'):
                d_ = out_ / f'E0_{lv_}_s{s_}'
                (d_ / 'post').mkdir(exist_ok=True)
                t0 = mi.planned_t0(mi.deck_plan(str(d_ / 'in.mixer')))
                _gdump(d_ / 'post' / f'mix_{t0}.liggghts', t0, _icloud(10))
        ep_ = Path(td_) / 'eps.json'
        ep_.write_text(json.dumps(dict(schema='mixer_interim_eps/1', registered='(합성 고정물) 사전등록 §5 ε_s 표',
                                       items=['판독기 float64 — 반올림 항 0 (합성)'], bins=eps_bins)), encoding='utf-8')
        return out_, ep_

    def _imain(argv, status=None, x_pct=None):
        """main(argv) — 검사기만 대역 (sg._fx_fake_cw · 기본 ref CONTRACT_MET · soft CONTRACT_NOT_MET) · 화면 · rc (SystemExit 도 rc 로)."""
        st_ = dict(status or {})
        real_ = G['cv'].check_window
        G['cv'].check_window = sg._fx_fake_cw(lambda n_: st_.get(n_, sg._fx_default_status(n_)), x_pct=x_pct)
        o_, e_ = io.StringIO(), io.StringIO()
        try:
            with contextlib.redirect_stdout(o_), contextlib.redirect_stderr(e_):
                try:
                    rc_ = main(argv)
                except SystemExit as ex_:
                    rc_ = ex_.code if isinstance(ex_.code, int) else 2
        finally:
            G['cv'].check_window = real_
        return rc_, o_.getvalue() + e_.getvalue()

    def _canaries(vals):
        """seed 별 d · 런별 M · q — 화면 · 기록에 나오면 안 되는 표기 (소수 4 자리 · repr 앞 7 자).  소수 3 자리에서 끝나는 '둥근' 값은 뺀다
        (0.2000 · 0.0000 같은 표기는 다른 등록 수치 · u 항과 구별되지 않는다)."""
        out_ = set()
        for v_ in vals:
            if abs(v_ * 1000 - round(v_ * 1000)) < 1e-6:
                continue
            out_ |= {f'{v_:.4f}', repr(float(v_))[:7]}
        return out_

    def _t15():
        with tempfile.TemporaryDirectory(prefix='sb_i1_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            e0 = str(out_ / f'E0_ref_s{SEEDS[0]}')
            before = json.dumps(mi.analyse(str(out_ / ROT[2]), e0, REG['r_container'], cells=REG['cells'], x_cells=REG['x_cells'],
                                           n_min=REG['n_min'], axis=REG['axis']), sort_keys=True, default=str)
            rc_, shown = _imain(['--interim', str(out_), '--eps', str(ep_)])
            rec = json.loads((out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8'))
            st = rec['statistics']['ref']
            d = [_Ma(LC_REF[i_]) - _Ma(LH_REF[i_]) for i_ in range(3)]
            dm = sum(d) / 3
            se = (sum((x - dm) ** 2 for x in d) / 2) ** 0.5 / 3 ** 0.5
            ds = [_Ma(LC_SOFT[i_]) - _Ma(LH_SOFT[i_]) for i_ in range(3)]
            q = [ds[i_] - d[i_] for i_ in range(3)]
            per_run = [_Ma(a_) for a_ in set(LC_REF + LH_REF + LC_SOFT + LH_SOFT)]
            canary = _canaries(d + ds + q + per_run)
            text = (out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8')
            leaked = sorted(c_ for c_ in canary if c_ in shown or c_ in text)
            vault = Path(rec['vault']['file'])
            vj = json.loads(vault.read_text(encoding='utf-8'))
            sm = rec['statistics']['soft']
            after = json.dumps(mi.analyse(str(out_ / ROT[2]), e0, REG['r_container'], cells=REG['cells'], x_cells=REG['x_cells'],
                                          n_min=REG['n_min'], axis=REG['axis']), sort_keys=True, default=str)
            bund_ok = all(not mi.verify_frames(str(out_ / n_ / 'post'), rec['inputs']['runs'][n_]['reader_frames']) for n_ in ROT)
            marks = [out_ / n_ / G['INTERIM_DIR'] / G['INTERIM_MARKER'] for n_ in dd.COHORTS['confirm']]
            logs = [json.loads(l_) for l_ in (out_ / G['INTERIM_DIR'] / 'blind_log.jsonl').read_text(encoding='utf-8').splitlines()]
            res = dict(rc=rc_ == 0, outcome=rec['outcome'] == 'MET' and 'MET' in shown, keys=sorted(rec) == sorted(G['INTERIM_TOP']),
                       shape=G['interim_projection_problems'](rec) == [],
                       stats=(abs(st['delta3'] - dm) < 1e-9 and abs(st['se3'] - se) < 1e-9 and st['signs'] == {str(s_): '+' for s_ in SEEDS}
                              and st['met'] is True and st['u_mean'] == 0 and (st['mid'], st['k_se']) == (0.10, 3.0)),
                       soft=(sm['d_soft'] is not None and abs(sm['d_soft']['mean'] - sum(ds) / 3) < 1e-9 and sm['q'] is not None
                             and abs(sm['q']['mean'] - sum(q) / 3) < 1e-9 and sm['qualifiers'] == []),
                       no_leak=not leaked, vault=(oct(vault.stat().st_mode)[-3:] == '600'
                                                  and abs(vj['per_run'][ROT[0]]['M_bin'] - _Ma(LC_SOFT[0])) < 1e-9),
                       frames=bund_ok and rec['inputs']['eps']['sha256'] == _sha_file(ep_),
                       claim=(out_ / G['INTERIM_DIR'] / G['INTERIM_CLAIM']).is_file() and all(p_.is_file() for p_ in marks),
                       log=logs[-1]['viewed'] == 'interim allow-list projection' and logs[-1]['record_sha256'] == _sha_file(out_ / G['INTERIM_RECORD']),
                       who=bool(rec['look'].get('user')) and bool(rec['look'].get('time_utc')) and rec['look']['tools']['reader'] == _sha_file(mi.__file__),
                       final_separate=before == after and rec['bin'] == 3 and rec['kind'] == 'interim')
            if leaked:
                print(f'        누설: {leaked[:6]}')
            print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
            return all(res.values())
    chk('⑮ ★ 중간 판정 (정상 · MET) — rc 0 · 기록 = 허용목록 정확히 (§5-a: 세 d_s 부호 · Δ3 · SE3 · u 항 · 충족 + d_soft · q 요약) · 값 = 독립 산술 · '
        '화면 · 기록에 seed 별 d · 런별 M · q 값 없음 · 전체 결과는 0600 봉인 · 누가/언제/입력 sha256 (프레임 묶음 = 지금 폴더) · claim + 18 표지 · '
        '최종 (bin 7) 판독 경로는 그대로 (analyse 전후 같음)', okx(_t15))

    def _t16():
        with tempfile.TemporaryDirectory(prefix='sb_i2_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            rc1, _s1 = _imain(['--interim', str(out_), '--eps', str(ep_)])
            rsha = _sha_file(out_ / G['INTERIM_RECORD'])
            vault_n = len(list((out_ / G['INTERIM_DIR']).glob('interim_full_*.json')))
            rc2, s2 = _imain(['--interim', str(out_), '--eps', str(ep_)])
            st = json.loads((out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8'))['statistics']['ref']
            res = dict(first=rc1 == 0, second=rc2 == G['RC_CONSUMED'] and _sha_file(out_ / G['INTERIM_RECORD']) == rsha
                       and len(list((out_ / G['INTERIM_DIR']).glob('interim_full_*.json'))) == vault_n
                       and f"{st['delta3']:.4f}" not in s2 and '두 번째' in s2)
            out2 = td_ / 'OUT2'                                   # 18 런 폴더 + manifest 를 새 OUT 으로 복사 (OUT 의 claim · 기록 없이) — 표지가 따라온다
            out2.mkdir()
            for n_ in dd.COHORTS['confirm']:
                shutil.copytree(out_ / n_, out2 / n_)
            shutil.copyfile(out_ / 'confirm_manifest.json', out2 / 'confirm_manifest.json')
            rc3, s3 = _imain(['--interim', str(out2), '--eps', str(ep_)])
            res['copied_runs'] = rc3 == G['RC_CONSUMED'] and not (out2 / G['INTERIM_RECORD']).exists()
            (out_ / G['INTERIM_DIR'] / G['INTERIM_CLAIM']).unlink()          # OUT 의 claim · 기록을 지워도 런 표지가 남아 거부
            (out_ / G['INTERIM_RECORD']).unlink()
            rc4, _s4 = _imain(['--interim', str(out_), '--eps', str(ep_)])
            res['claim_deleted'] = rc4 == G['RC_CONSUMED']
            print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
            return all(res.values())
    chk('⑯ ★ 두 번째 중간 판정 거부 (§5-a "두 번째 중간 판정은 없다") — 같은 OUT 재실행 rc 4 · 새 봉인 없음 · 기록 불변 · 화면에 값 없음 / 런 폴더를 새 OUT 으로 '
        '복사해도 · OUT 의 claim · 기록을 지워도 런 표지로 거부', okx(_t16))

    def _t17():
        with tempfile.TemporaryDirectory(prefix='sb_i3_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            allowed = set()
            for n_ in ROT:
                c_ = dd.parse_cell(n_)
                pl = mi.deck_plan(str(out_ / n_ / 'in.mixer'))
                t0 = mi.planned_t0(pl)
                w_ = mi.bin_window_files(str(out_ / n_ / 'post'), t0, pl['steps_per_rev'], pl['dump_every'], pl['steps_total'], (3,))
                allowed |= {os.path.realpath(str(out_ / n_ / 'post' / f'mix_{s_}.liggghts')) for s_ in [t0] + sorted(w_['lattice'])}
                e0d = out_ / f'E0_{c_["level"]}_s{c_["seed"]}'
                allowed.add(os.path.realpath(str(e0d / 'post' / f'mix_{mi.planned_t0(mi.deck_plan(str(e0d / "in.mixer")))}.liggghts')))
            seen = []
            rd_, vf_ = mi.read_dump, mi.validate_frame
            mi.read_dump = lambda p_, *a_, **k_: (seen.append(os.path.realpath(p_)), rd_(p_, *a_, **k_))[1]
            mi.validate_frame = lambda p_, *a_, **k_: (seen.append(os.path.realpath(p_)), vf_(p_, *a_, **k_))[1]
            try:
                rc_, _s = _imain(['--interim', str(out_), '--eps', str(ep_)])
            finally:
                mi.read_dump, mi.validate_frame = rd_, vf_
            rec = json.loads((out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8'))
            extra = sorted(set(seen) - allowed)
            if extra:
                print(f'        허용 밖 열람: {extra[:3]}')
            return rc_ == 0 and rec['outcome'] == 'MET' and not extra and set(seen) == allowed
    chk('⑰ ★ 판독기가 연 파일 = 12 런의 계획 t₀ + bin 3 격자 + 같은 강성 · seed E0 계획 t₀ **정확히** (bin 0–2 · 4 는 쓰레기인데 결과 MET — 열었다면 값이 없다)',
        okx(_t17))

    def _t18():
        with tempfile.TemporaryDirectory(prefix='sb_i4_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            n_ = ROT[5]
            pl = mi.deck_plan(str(out_ / n_ / 'in.mixer'))
            t0 = mi.planned_t0(pl)
            last = max(mi.bin_window_files(str(out_ / n_ / 'post'), t0, pl['steps_per_rev'], pl['dump_every'], pl['steps_total'], (3,))['lattice'])
            p_ = out_ / n_ / 'post' / f'mix_{last}.liggghts'
            keep = p_.read_text(encoding='utf-8')
            p_.unlink()                                           # 한 런이 아직 4 바퀴 전 (bin 3 마지막 계획 덤프 없음)
            rc1, s1 = _imain(['--interim', str(out_), '--eps', str(ep_)])
            res = dict(refused=rc1 == G['RC_REFUSED'] and '4 바퀴' in s1 and not (out_ / G['INTERIM_RECORD']).exists()
                       and not (out_ / G['INTERIM_DIR'] / G['INTERIM_CLAIM']).exists()
                       and not any((out_ / m_ / G['INTERIM_DIR'] / G['INTERIM_MARKER']).exists() for m_ in dd.COHORTS['confirm'])
                       and 'Δ3' not in s1)
            p_.write_text(keep, encoding='utf-8')
            rc2, _s2 = _imain(['--interim', str(out_), '--eps', str(ep_)])
            res['later_ok'] = rc2 == 0
            print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
            return all(res.values())
    chk('⑱ 12 런 중 하나가 아직 4 바퀴 전 (bin 3 결손) → rc 3 · M 미계산 · 소진 아님 (claim · 표지 · 기록 없음) — 다 지난 뒤에는 볼 수 있다', okx(_t18))

    def _t19():
        with tempfile.TemporaryDirectory(prefix='sb_i5_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            good = json.loads(ep_.read_text(encoding='utf-8'))
            res = {}
            rc0, s0 = _imain(['--interim', str(out_)])
            res['none'] = rc0 == G['RC_REFUSED'] and 'ε' in s0
            bad = dict(bin7_only=dict(good, bins={'7': good['bins']['3']}),
                       missing_seed=dict(good, bins={'3': {str(SEEDS[0]): 0.0, str(SEEDS[1]): 0.0}}),
                       negative=dict(good, bins={'3': dict(good['bins']['3'], **{str(SEEDS[2]): -0.01})}),
                       nan=dict(good, bins={'3': dict(good['bins']['3'], **{str(SEEDS[2]): float('nan')})}),
                       schema=dict(good, schema='x'), no_items=dict(good, items=[]), no_registered=dict(good, registered=''))
            for k_, v_ in bad.items():
                bp = td_ / f'eps_{k_}.json'
                bp.write_text(json.dumps(v_), encoding='utf-8')
                rc_, _s = _imain(['--interim', str(out_), '--eps', str(bp)])
                res[k_] = rc_ == G['RC_REFUSED']
            res['not_consumed'] = (not (out_ / G['INTERIM_DIR'] / G['INTERIM_CLAIM']).exists() and not (out_ / G['INTERIM_RECORD']).exists())
            print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
            return all(res.values())
    chk('⑲ ★ ε 등록 fail-closed (§5 "ε_s 의 항목과 값은 결과 전 … 배정" · ⬜ §10) — 없음 · bin 7 만 (옮겨 쓰지 않는다) · seed 빠짐 · 음수 · NaN · 스키마 · 항목 없음 · '
        '등록 위치 없음 → rc 3 · 0 으로 채우지 않는다 · 소진 아님', okx(_t19))

    def _t20():
        res = {}
        with tempfile.TemporaryDirectory(prefix='sb_i6_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            s0 = SEEDS[1]
            for lab, st_ in (('ref_notmet', {f'LH_ref_r8_s{s0}': 'CONTRACT_NOT_MET'}), ('e0ref_tech', {f'E0_ref_s{s0}': 'TECH_FAIL'})):
                rc_, s_ = _imain(['--interim', str(out_), '--eps', str(ep_)], status=st_)
                res[lab] = (rc_ == G['RC_REFUSED'] and '조기 확정' in s_ and next(iter(st_)) in s_
                            and not (out_ / G['INTERIM_DIR'] / G['INTERIM_CLAIM']).exists())
        with tempfile.TemporaryDirectory(prefix='sb_i7_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_, t0_a={f'LC_ref_r8_s{SEEDS[2]}': 16})              # ref 런 층상 약함 — 8×8×2 비 4.0 < 5 (16×16×4 의 M 은 정의됨)
            rc_, s_ = _imain(['--interim', str(out_), '--eps', str(ep_)])
            res['ref_floor'] = rc_ == G['RC_REFUSED'] and '바닥' in s_ and not (out_ / G['INTERIM_DIR'] / G['INTERIM_CLAIM']).exists()
        with tempfile.TemporaryDirectory(prefix='sb_i8_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_, t0_a={f'LH_soft_r8_s{SEEDS[0]}': 16})
            rc_, s_ = _imain(['--interim', str(out_), '--eps', str(ep_)], status={f'LC_soft_r8_s{SEEDS[2]}': 'OUT_OF_RANGE'})
            rec = json.loads((out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8'))
            ql = ' '.join(rec['statistics']['soft']['qualifiers'])
            res['soft_pass'] = (rc_ == 0 and rec['outcome'] == 'MET' and 'OUT_OF_RANGE' in ql and f'LC_soft_r8_s{SEEDS[2]}' in ql
                                and f'LH_soft_r8_s{SEEDS[0]}' in ql and rec['statistics']['soft']['d_soft'] is not None)
        print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
        return all(res.values())
    chk('⑳ ★ M-맹검 적격 (접촉 창 bin 0–3 · 바닥 8×8×2) — ref 팔 · E0_ref 가 CONTRACT_MET 아니거나 ref 바닥 미달이면 조기 확정 불가 → rc 3 · M 미계산 · 소진 아님 / '
        'soft 의 OUT_OF_RANGE · 바닥 미달은 막지 않고 soft 요약의 한정어로 (§6 · §8-4)', okx(_t20))

    def _t21():
        with tempfile.TemporaryDirectory(prefix='sb_i9_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_, lc_ref=(9, 5, 9), lh_ref=(4, 6, 5))             # seed 2 = M(5) − M(6) < 0
            rc_, s_ = _imain(['--interim', str(out_), '--eps', str(ep_)])
            rec = json.loads((out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8'))
            st = rec['statistics']['ref']
            rc2, _s2 = _imain(['--interim', str(out_), '--eps', str(ep_)])
            return (rc_ == 0 and rec['outcome'] == 'NOT_MET' and st['met'] is False and st['cond']['all_positive'] is False
                    and st['signs'][str(SEEDS[1])] == '−' and '8 바퀴' in rec['next'] and '8 바퀴' in s_ and rc2 == G['RC_CONSUMED'])
    chk('⑳b 충족 못 함 (한 seed 음수) — rc 0 · NOT_MET · 다음 = 8 바퀴까지 · §5 최종 그대로 · 이 값은 최종과 함께 보고 · 그 뒤 두 번째 판정 거부', okx(_t21))

    def _t22():
        res = {}
        with tempfile.TemporaryDirectory(prefix='sb_ia_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            n_ = f'LH_ref_r8_s{SEEDS[0]}'
            pl = mi.deck_plan(str(out_ / n_ / 'in.mixer'))
            t0 = mi.planned_t0(pl)
            st3 = sorted(mi.bin_window_files(str(out_ / n_ / 'post'), t0, pl['steps_per_rev'], pl['dump_every'], pl['steps_total'], (3,))['lattice'])[4]
            p_ = out_ / n_ / 'post' / f'mix_{st3}.liggghts'
            p_.write_text(p_.read_text(encoding='utf-8').split('ITEM: ATOMS', 1)[1].join(['ITEM: ATOMS', '']), encoding='utf-8')   # 머리 없는 프레임
            rc_, s_ = _imain(['--interim', str(out_), '--eps', str(ep_)])
            rec = json.loads((out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8'))
            rc2, _s2 = _imain(['--interim', str(out_), '--eps', str(ep_)])
            res['tech'] = (rc_ == 0 and rec['outcome'] == 'INELIGIBLE' and rec['statistics']['ref'] is None and n_ in ' '.join(rec['eligibility']['reasons'])
                           and rc2 == G['RC_CONSUMED'] and '8 바퀴' in rec['next'])
        with tempfile.TemporaryDirectory(prefix='sb_ib_') as tmp_:
            td_ = Path(tmp_)
            n_ = f'LC_ref_r8_s{SEEDS[2]}'
            out_, ep_ = _ifix(td_, sparse=(n_,))                                   # 버린 칸에 SE 가 몰린다 → D-2 부피 누락 QC 미달
            rc_, _s = _imain(['--interim', str(out_), '--eps', str(ep_)])
            rec = json.loads((out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8'))
            res['qc'] = (rc_ == 0 and rec['outcome'] == 'INELIGIBLE' and rec['statistics']['ref'] is not None
                         and rec['statistics']['ref']['met'] is True and any(n_ in r_ and 'QC' in r_ for r_ in rec['eligibility']['reasons']))
        with tempfile.TemporaryDirectory(prefix='sb_ie_') as tmp_:
            #  claim 뒤 중단 (Ctrl-C 같은 BaseException) — 옛 초판: 기록 없이 새어 나가 소진만 남았다 (자기 리뷰에서 찾음 · 이 반례로 먼저 재현)
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)

            class _Stop(BaseException):
                pass
            real_bw = mi.bin_window_stats

            def boom(run_dir, *a_, **k_):
                if os.path.basename(os.path.normpath(run_dir)) == ROT[3]:
                    raise _Stop('중단 (합성)')
                return real_bw(run_dir, *a_, **k_)
            mi.bin_window_stats = boom
            try:
                try:
                    rc_, _s = _imain(['--interim', str(out_), '--eps', str(ep_)])
                except BaseException:                                            # noqa: BLE001
                    rc_ = 'crash'
            finally:
                mi.bin_window_stats = real_bw
            rp_ = out_ / G['INTERIM_RECORD']
            rec = json.loads(rp_.read_text(encoding='utf-8')) if rp_.exists() else {}
            lg = out_ / G['INTERIM_DIR'] / 'blind_log.jsonl'
            ev_ = [json.loads(l_).get('event') for l_ in lg.read_text(encoding='utf-8').splitlines()] if lg.exists() else []
            res['interrupt'] = (rc_ == 0 and rec.get('outcome') == 'TECH' and (rec.get('statistics') or {}).get('ref') is None
                                and ev_[-2:] == ['claim', 'look'] and '8 바퀴' in rec.get('next', '')
                                and _imain(['--interim', str(out_), '--eps', str(ep_)])[0] == G['RC_CONSUMED'])
        print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
        return all(res.values())
    chk('㉑ ★ 판독 적격 실패 (봉인 뒤) — ref 런 bin 3 프레임 형식 실패 = INELIGIBLE · 값 없음 / D-2 부피 누락 QC 미달 = INELIGIBLE (값은 보고 · 판정선 충족이어도 '
        '조기 확정 아님) / claim 뒤 중단 (BaseException) = TECH 기록 (claim → look 로그) · 셋 다 소진 · 다음 = 8 바퀴', okx(_t22))

    def _t23():
        res = {}
        with tempfile.TemporaryDirectory(prefix='sb_ic_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            mp_ = out_ / 'confirm_manifest.json'
            keep = mp_.read_text(encoding='utf-8')
            mp_.unlink()
            res['no_manifest'] = _imain(['--interim', str(out_), '--eps', str(ep_)])[0] == G['RC_REFUSED']
            mp_.write_text(keep.replace('"complete": true', '"complete": false'), encoding='utf-8')
            res['partial'] = _imain(['--interim', str(out_), '--eps', str(ep_)])[0] == G['RC_REFUSED']
            mp_.write_text(keep, encoding='utf-8')
            dk = out_ / ROT[4] / 'in.mixer'
            kd = dk.read_text(encoding='utf-8')
            dk.write_text(kd + '# 봉인 뒤 수정\n', encoding='utf-8')
            rc_, s_ = _imain(['--interim', str(out_), '--eps', str(ep_)])
            res['deck'] = rc_ == G['RC_REFUSED'] and ROT[4] in s_
            dk.write_text(kd, encoding='utf-8')
            sg._fx_seal(str(out_), ROT[1], 'confirm-first', 5, note='다시 봉인')
            res['reseal'] = _imain(['--interim', str(out_), '--eps', str(ep_)])[0] == G['RC_REFUSED']
            res['not_consumed'] = not (out_ / G['INTERIM_DIR'] / G['INTERIM_CLAIM']).exists()
        print('        ' + ' · '.join(f'{k_}:{"✓" if v_ else "✗"}' for k_, v_ in res.items()))
        return all(res.values())
    chk('㉒ 캠페인 동일성 (confirm manifest · 발사 봉인 · 덱) — manifest 없음 · 불완전 · 봉인 뒤 덱 수정 · 다시 봉인 → rc 3 · 소진 아님', okx(_t23))

    def _t24():
        #  투영 검사기 자체 — 허용목록 밖 키 · 결과 키 (M · rows · S0 …) · seed 별 값이 숨어 들어오면 문제로 잡는다
        with tempfile.TemporaryDirectory(prefix='sb_id_') as tmp_:
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            rc_, _s = _imain(['--interim', str(out_), '--eps', str(ep_)])
            rec = json.loads((out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8'))
            pp = G['interim_projection_problems']
            v1 = copy.deepcopy(rec); v1['statistics']['ref']['d_by_seed'] = {str(SEEDS[0]): 0.3}
            v2 = copy.deepcopy(rec); v2['inputs']['runs'][ROT[0]]['M_bin'] = 0.5
            v3 = copy.deepcopy(rec); v3['extra'] = 1
            v4 = copy.deepcopy(rec); v4['statistics']['soft']['d_soft']['per_seed'] = [0.1, 0.2, 0.3]
            v5 = copy.deepcopy(rec); v5['eligibility']['rows'] = []
            ok_val = rc_ == 0 and pp(rec) == [] and all(pp(v_) for v_ in (v1, v2, v3, v4, v5))
        with tempfile.TemporaryDirectory(prefix='sb_if_') as tmp_:
            #  투영기 자신이 허용목록을 어기면 (합성: 런별 입력에 M_bin 을 끼운다) — 값 · 런별 입력을 비운 TECH 기록만 쓴다 (새지 않는다)
            td_ = Path(tmp_)
            out_, ep_ = _ifix(td_)
            real_ri = G['_run_input']
            G['_run_input'] = lambda identity, contact, per, n: dict(real_ri(identity, contact, per, n), M_bin=(per.get(n) or {}).get('M_bin'))
            try:
                rc2, s2 = _imain(['--interim', str(out_), '--eps', str(ep_)])
            finally:
                G['_run_input'] = real_ri
            text = (out_ / G['INTERIM_RECORD']).read_text(encoding='utf-8')
            rec2 = json.loads(text)
            ok_self = (rc2 == 0 and rec2['outcome'] == 'TECH' and G['interim_projection_problems'](rec2) == [] and 'M_bin' not in text
                       and rec2['statistics']['ref'] is None and f'{_Ma(LC_REF[0]):.4f}' not in text + s2)
        return ok_val and ok_self
    chk('㉓ 투영 검사기 (interim_projection_problems) — 정상 기록은 문제 0 · seed 별 값 · 런별 M_bin · 허용 밖 최상위 키 · 요약 안 seed 별 목록 · 결과 키 (rows) 가 '
        '들어오면 잡는다 / 투영기가 스스로 어기면 (런별 입력에 M_bin) 값 · 런별 입력을 비운 TECH 기록만 쓴다 (기록 자체는 검사 통과 · 새지 않는다)', okx(_t24))
    print()
    if fails:
        print(f'✗ {len(fails)} 건 실패')
        return 1
    print('✓ 전부 통과 — 래퍼는 판독기 출력을 가로채고 허용목록만 투영하며, 거부 · 예외 · 누설을 화면에 내지 않는다.  '
          '⚠ 봉인 파일을 여는 것은 사람의 규율이다 (열람 = blind_log)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
