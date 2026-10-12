#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""보충 20 (supp20) 입력 지문 영수증 — **읽기 전용** (리포 · 입력 파일을 고치지 않는다 · --json 을 줄 때만 그 파일 하나를 쓴다).

계기: Codex 보충 20 지원 검토 (`docs/reviews/codex_review_supp20_support_20261012.md` §5 Q6) — 실행기 `registered_id_set('supp20')` 은 **ID 집합 지문**만 본다.
등록 문서 §2 의 원자료 sha 표 · 코호트 TSV 값까지 자동 비교하는 함수는 없었다 (Codex 탐침: raw sha · TSV 바이트를 바꿔도 같은 20 ID 의 등록 판정은 유지) →
**한 영수증에** 대조한다 (수정 계획 `docs/reviews/sup20_fix_plan_20261012.md` §3 · 1저자 Q3 (가)):
  ① ID 지문 — 실행기 등록 표 = 등록 문서 §2 = 커밋된 수확 폴더에서 열거한 값 · 계획 = 등록 집합 supp20 (일반 계획 `--expect-case` 강등 = rc 1)
  ② 등록 §2 값 (케이스 수 · ids · raw_sha256_table · 코호트 TSV) = 반입 파일에서 다시 계산한 값 (실행기 plan_input_digest 그대로) = 발사 dry-run 이 찍은 값 ·
     발사 manifest 의 input_digest
  ③ 수확기 판 (r3 묶음 sha · harvest_head) · 반입 파일 = r3 묶음 바이트 (기술자 20 · 요약 · 코호트 TSV · union) · 설계 CSV · 어댑터 CSV sha · r2 ↔ r3 키별 대조
  ④ 도구 핀 (봉인 32 code_fp = 등록 §3 · 실행기 · 인계 도구 · 배포 생성기 · 이 도구 지문 · git) · 관측 ON · 새 ROOT 둘 (manifest 둘을 주면) —
     사전 점검 (fast16 + real4) 결과 · 저자 발사 승인 = 수동 칸 (이 도구가 인증하지 않는다)
값의 정본은 실행기 함수 (`run_network_194_parallel` — registered_id_set · build_plan · cohort_specs · plan_input_digest · registered_production_set ·
print_followups · print_preflight 줄 꼴 · launch_eligibility · production_observation_problem) 와 등록 문서 · 수확 묶음 README 다 — 값을 이 파일에
베껴 두지 않는다 (r2 대조의 허용 차이 두 칸만 README 끝 문장을 옮긴 상수 · 묶음 폴더 이름 둘).

  python3 scripts/supp20_input_receipt.py                                       # 컨테이너 범위 (발사 전 칸)
  python3 scripts/supp20_input_receipt.py --dry-run-log dry.log                  # + 발사 dry-run 화면 (run --cohorts lhss --dry-run --observe-imports 출력을
                                                                                 #   tee 로 받은 파일 · 등록 §4 의 grep 으로 걸러도 된다)
  python3 scripts/supp20_input_receipt.py --manifest R/manifest.json --primary-manifest R194/manifest.json   # + 실제 발사 manifest (보충 · 194)
  python3 scripts/supp20_input_receipt.py --json receipt.json                    # 영수증 JSON
  python3 scripts/supp20_input_receipt.py --selftest

rc 0 = 기계로 대조한 칸이 전부 같다 · rc 1 = 하나라도 다르거나 못 읽었다 · rc 2 = 사용법 (argparse).
⚠ rc 0 은 **발사 승인이 아니다** — 판정문 §4 ("preflight rc 0 하나로 보충 생산 등록까지 인증" 금지) 와 같은 이유로, 컨테이너 범위 rc 0 = 반입 입력 · 도구 핀이
  등록 §2 · §3 과 같다는 것까지다.  발사 dry-run · manifest 칸은 그 파일을 줄 때만 대조한다 (영수증 scope · manual 칸에 적힌다).
"""
import argparse
import contextlib
import csv
import datetime
import hashlib
import io
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import run_network_194_parallel as NP          # noqa: E402  (등록 집합 · 계획 · 입력 지문 · 후속 명령 · 실행 형식 자격 — 실행기 정본 · 사본 금지)

SCHEMA = 'supp20_input_receipt/v1'
SET, COHORT = 'supp20', 'lhss'
REG_DOC = 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md'
RUNS_README = 'docs/data/lhs_supp_runs_20261006/README.md'
R3_TGZ = 'docs/data/lhs_supp_runs_20261006/lhss_harvest_r3_1e09f661d.tgz'
R2_TGZ = 'docs/data/lhs_supp_runs_20261006/lhss_harvest_20261011_r2.tgz'
R3_TOP, R2_TOP = 'lhss_out_r3_1e09f661d/', 'lhss_out_20261011/'          # 묶음 항목의 한 폴더 (README "29 항목 전부 … 아래" · r2 "30 항목 전부 … 아래")
SUPP_DESIGN = 'docs/data/lhs_supp_design_20261006.csv'
#: r2 ↔ r3 키별 대조의 등록된 결과 (수확 묶음 README 끝 — 공통 키 값 전부 같음 · 다른 키 1 = 수확 체크아웃 경로 · r2 에만 = wall_near_tangent 진단 · r3 에만 0)
R2_DIFF_OK = ('contact_area_check.producer_model.pin_file',)
R2_ONLY_OK = 'wall_near_tangent.'
TOOL_PINS = ('scripts/run_network_194_parallel.py', 'scripts/lhs_release_build.py', 'scripts/supp20_input_receipt.py') + tuple(NP.HANDOVER_FILES)
MANUAL = ('사전 점검 결과 — 발사 핀 fast16 + real4 · 깨끗한 트리 (등록 §0 ⑥ · 194 등록 §1 과 같은 단계)',
          '저자 발사 승인 (판정문 §4 ⑤ — 이 영수증 · 리뷰가 대신하지 않는다)',
          '새 ROOT 둘 · 같은 발사 커밋 — --manifest 와 --primary-manifest 를 둘 다 주면 기계 대조 (아니면 수동)')


def _rp(rel):
    p = Path(rel)
    return p if p.is_absolute() else REPO / p


def _sha(p):
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except OSError:
        return None


def _one(pattern, text):
    """정규식 첫 묶음의 값 — 자리가 없거나 값이 둘 이상 다르면 (None, 사유)."""
    vals = sorted(set(re.findall(pattern, text, re.M)))
    if not vals:
        return None, '자리 없음'
    return (vals[0], '') if len(vals) == 1 else (None, f'값이 둘 이상 {vals}')


def _sha_after(text, anchor):
    """anchor (문서에 한 번) 가 있는 줄에서 anchor 뒤 첫 'sha256 `<64 hex>`'."""
    i = text.find(anchor)
    if i < 0 or text.find(anchor, i + 1) >= 0:
        return None, f'자리 {"없음" if i < 0 else "둘 이상"} ({anchor[:48]})'
    m = re.search(r'sha256 `([0-9a-f]{64})`', text[i:].split('\n', 1)[0])
    return (m.group(1), '') if m else (None, f'{anchor[:48]} 뒤 같은 줄에 sha256 이 없다')


def registration_values(reg_doc=REG_DOC, readme=RUNS_README):
    """등록 문서 §2 · §3 + 수확 묶음 README 의 값 → (dict, 문제 목록).  손으로 옮겨 적지 않고 문서에서 읽는다 (문서 오타 = 재계산과 다름 = rc 1)."""
    out, probs = {}, []
    try:
        t = _rp(reg_doc).read_text(encoding='utf-8')
    except OSError as e:
        return out, [f'등록 문서 {reg_doc} 를 못 읽었다 ({type(e).__name__})']
    design = NP.COHORT_SPECS[COHORT]['design']
    for k, kind, how in (('n', 're', r'^\|\s*케이스 수\s*\|\s*(\d+)\b'),
                         ('ids_sha256', 're', r'^\|\s*`ids_sha256`[^|\n]*\|\s*`([0-9a-f]{64})`'),
                         ('raw_sha256_table_sha256', 're', r'^\|\s*`raw_sha256_table_sha256`\s*\|\s*`([0-9a-f]{64})`'),
                         ('cohort_tsv_sha256', 're', r'^\|\s*코호트 TSV sha256\s*\|\s*`([0-9a-f]{64})`'),
                         ('code_fp', 're', r'`code_fp ([0-9a-f]{64})`'),
                         ('harvest_pin', 're', r'재수확 r3 \(`([0-9a-f]{7,40})`\)'),
                         ('design_csv_sha256', 'after', f'(설계 `{SUPP_DESIGN}`'),
                         ('adapter_csv_sha256', 'after', f'설계 어댑터 출력 = `{design}`')):
        v, why = _one(how, t) if kind == 're' else _sha_after(t, how)
        if why:
            probs.append(f'등록 문서 {k} — {why}')
        out[k] = int(v) if (k == 'n' and v is not None) else v
    try:
        rt = _rp(readme).read_text(encoding='utf-8')
    except OSError as e:
        return out, probs + [f'수확 묶음 README {readme} 를 못 읽었다 ({type(e).__name__})']
    for k, anchor in (('r3_tgz_sha256', f'`{Path(R3_TGZ).name}` ('), ('r2_tgz_sha256', f'`{Path(R2_TGZ).name}` (')):
        v, why = _sha_after(rt, anchor)
        if why:
            probs.append(f'README {k} — {why}')
        out[k] = v
    v, why = _one(r'`harvest_head\.txt` = `([0-9a-f]{40})`', rt)
    if why:
        probs.append(f'README harvest_head — {why}')
    out['harvest_head'] = v
    return out, probs


def plan_for(harvest=None, cohort=None):
    """발사 dry-run 과 같은 계획 (실행기 build_plan · cohort_specs · --cohorts lhss · 순서 cost) — harvest · cohort = 실행기 --lhss-harvest · --lhss-cohort 와 같은 뜻."""
    args = types.SimpleNamespace(**{f'{COHORT}_harvest': harvest or '', f'{COHORT}_cohort': cohort or ''})
    return NP.build_plan([COHORT], NP.cohort_specs(args), (), 'cost')


def followup_reread(plan):
    """실행기 print_followups 가 이 계획에 대해 찍는 ⓪b 다시 읽기 명령 줄 (등록 집합이면 --expect-set · 아니면 --expect-case 나열)."""
    buf = []
    NP.print_followups(Path('/receipt_root'), {'plan': plan, NP.GEN_KEY: NP.CURRENT_GENERATION, 'git': {'short': 'RECEIPT'}}, out=buf.append)
    return [ln for ln in buf if 'g2_network_reread.py' in ln and '--launcher-root' in ln]


def _tar_files(path, top):
    """묶음 → ({항목 이름: 바이트}, 꼴 문제) — 메모리에서만 읽는다 (풀지 않는다) · 절대 경로 · '..' · 링크 · 장치 · 한 폴더 밖 = 문제."""
    files, bad = {}, []
    try:
        with tarfile.open(path, 'r:gz') as tf:
            for m in tf.getmembers():
                if m.name.startswith('/') or '..' in m.name.split('/') or not (m.isfile() or m.isdir()) or not (m.name + '/').startswith(top):
                    bad.append(m.name)
                elif m.isfile():
                    files[m.name] = tf.extractfile(m).read()
    except (OSError, tarfile.TarError) as e:
        bad.append(f'묶음을 못 읽었다 ({type(e).__name__}: {e})')
    return files, bad


def _flat(d, p=''):
    if isinstance(d, dict):
        out = {}
        for k, v in d.items():
            out.update(_flat(v, f'{p}.{k}' if p else k))
        return out
    return {p: d}


def _tsv_cells(b):
    r = list(csv.reader(io.StringIO(b.decode('utf-8')), delimiter='\t'))
    return (r[0] if r else []), {x[0]: x for x in r[1:] if x}


#: 발사 dry-run 화면 (실행기 print_preflight) 의 줄 꼴 — 생산자 문구와 같아야 한다 (selftest 가 진짜 print_preflight 로 만든 화면을 읽어 맞댄다)
_DRY_INPUT = re.compile(r'입력 지문 \(ID · 코호트 · 원자료 sha256 = 수확 JSON raw\) — 케이스 (\S+) · ids_sha256 (\S+) · '
                        r'raw_sha256_table_sha256 (\S+) · 원자료 sha 결손 (\d+)')
_DRY_CODE = re.compile(r'코드 (\S*) \((.*?)\) dirty=(True|False)(.*?) · 봉인 지문 code_fp (\S+) \(CODE_FILES (\d+)\)')
_DRY_GEN = re.compile(r'기대 망 세대 \(' + re.escape(NP.GEN_KEY) + r" — [^)]*\): '?([^' ·]+)'? · 세대 계약 문제 (\d+)")
_DRY_RAW = re.compile(r'원자료 · 메시 문제 (\d+) 건')
_DRY_COHORT = re.compile(r'코호트 (\S+): 수확 (\d+) 건 \(선택 (\d+)\)')
_DRY_TICKS = ('전이 의존 닫힘', '지연 import 분류', 'fork · 프로세스 풀 API')


class _Receipt:
    def __init__(self):
        self.checks = []

    def add(self, cid, name, ok, detail=''):
        self.checks.append(dict(id=cid, name=name, ok=bool(ok), detail=detail if not ok else ''))
        return bool(ok)


def _dry_checks(R, text, dg, reg):
    """발사 dry-run 화면 대조 (E) — 입력 지문 줄 · 코드 줄 · 기대 세대 · 원자료 문제 · ⛔ · ✗."""
    lines = text.splitlines()
    m_in = {m.groups() for m in _DRY_INPUT.finditer(text)}
    want = (str(dg.get('n')), dg.get('ids_sha256'), dg.get('raw_sha256_table_sha256'), str(len(dg.get('missing_raw_sha') or [])))
    reg_t = (str(reg.get('n')), reg.get('ids_sha256'), reg.get('raw_sha256_table_sha256'), '0')
    R.add('E1', 'dry-run 입력 지문 줄 (하나) = 반입 파일 재계산 = 등록 §2 (케이스 · ids · raw sha 표 · 원자료 결손 0)',
          len(m_in) == 1 and next(iter(m_in)) == want == reg_t, dict(dry_run=sorted(m_in), recomputed=want, registered=reg_t))
    m_c = {m.groups() for m in _DRY_CODE.finditer(text)}
    c = next(iter(m_c)) if len(m_c) == 1 else None
    R.add('E2', 'dry-run 코드 줄 (하나) — 깨끗한 트리 (dirty=False) · 봉인 지문 code_fp = 등록 §3 · CODE_FILES 수 = 실행기',
          c is not None and c[2] == 'False' and c[4] == reg.get('code_fp') and c[5] == str(len(NP.CODE_FILES)), sorted(m_c))
    m_g = {m.groups() for m in _DRY_GEN.finditer(text)}
    R.add('E3', f'dry-run 기대 망 세대 = {NP.CURRENT_GENERATION!r} · 세대 계약 문제 0', m_g == {(NP.CURRENT_GENERATION, '0')}, sorted(m_g))
    m_r = set(_DRY_RAW.findall(text))
    R.add('E4', 'dry-run 원자료 · 메시 문제 0 건', m_r == {'0'}, sorted(m_r))
    stop = [ln.strip() for ln in lines if '⛔' in ln]
    tick = [ln.strip() for ln in lines if any(t in ln for t in _DRY_TICKS) and '✗' in ln]
    R.add('E5', 'dry-run 사전 점검 중단 (⛔) 0 · 전이 의존 · 지연 import · fork 줄에 ✗ 없음 (관측 없는 보충 계획 = ⛔ — 등록 §3)', not stop and not tick,
          (stop + tick)[:5])
    m_k = {(a, b, d) for a, b, d in _DRY_COHORT.findall(text)}
    if m_k:                                                  # 등록 §4 grep 은 이 줄을 거른다 — 있을 때만
        R.add('E6', f'dry-run 코호트 줄 = {COHORT} 하나 · 수확 {reg.get("n")} · 선택 {reg.get("n")}', m_k == {(COHORT, str(reg.get('n')), str(reg.get('n')))},
              sorted(m_k))


def _load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8')), ''
    except (OSError, ValueError) as e:
        return None, f'{type(e).__name__}: {e}'


def _manifest_checks(R, label, path, want_set, reg, dg=None):
    """실제 발사 manifest 대조 (F = 보충 · G = 194) — 실행 형식 자격 · 등록 생산 집합 · (보충) 입력 지문 · 관측 ON · 봉인 지문 · 깨끗한 트리 · (보충) 인계 도구 지문."""
    man, why = _load_json(path)
    if not R.add(f'{label}0', f'{want_set} 발사 manifest 읽기 ({path})', isinstance(man, dict), why or type(man).__name__):
        return None
    el = NP.launch_eligibility(man)
    R.add(f'{label}1', f'{want_set} manifest 실행 형식 자격 = current (실행기 launch_eligibility)', el.get('kind') == 'current', el.get('problems', [])[:4])
    nm = NP.registered_production_set(man.get('plan'))
    R.add(f'{label}2', f'{want_set} manifest 계획 = 등록 생산 집합 {want_set} (실행기 registered_production_set)', nm == want_set, repr(nm))
    if dg is not None:
        mdg = man.get('input_digest') if isinstance(man.get('input_digest'), dict) else {}
        bad = [k for k in NP.INPUT_DIGEST_KEYS if mdg.get(k) != dg.get(k)]
        R.add(f'{label}3', f'{want_set} manifest input_digest = 반입 파일 재계산 (= 등록 §2 — B3)', not bad, {k: [mdg.get(k), dg.get(k)] for k in bad})
    pob = NP.production_observation_problem(man)
    R.add(f'{label}4', f'{want_set} import 관측 ON (observe_imports true · 관측 실행 신원 · 실행기 production_observation_problem 없음)',
          man.get('observe_imports') is True and bool(man.get('import_obs_run_id')) and pob is None, pob or repr(man.get('observe_imports')))
    seal = man.get('seal') if isinstance(man.get('seal'), dict) else {}
    g = man.get('git') if isinstance(man.get('git'), dict) else {}
    R.add(f'{label}5', f'{want_set} 발사 봉인 code_fp = 등록 §3 · 깨끗한 트리 (git.dirty false)',
          seal.get('code_fp') == reg.get('code_fp') and g.get('dirty') is False, dict(code_fp=seal.get('code_fp'), dirty=g.get('dirty')))
    if dg is not None:
        now = {rel: NP.sha256_file(NP.ROOT / rel) for rel in NP.HANDOVER_FILES}
        R.add(f'{label}6', f'{want_set} manifest 인계 도구 지문 (handover_code_hashes) = 이 체크아웃 — 영수증은 발사 체크아웃에서 만든다',
              man.get('handover_code_hashes') == now, dict(manifest=man.get('handover_code_hashes'), now=now))
    return man


def receipt(*, reg_doc=REG_DOC, readme=RUNS_README, harvest=None, cohort=None, dry_run_log=None, manifest=None, primary_manifest=None,
            r3_tgz=R3_TGZ, r2_tgz=R2_TGZ, notes=None) -> dict:
    """영수증 dict (schema · scope · checks · recorded · manual · rc).  rc = 0 이면 기계로 대조한 칸이 전부 같다 (발사 승인 아님)."""
    R = _Receipt()
    reg, rp = registration_values(reg_doc, readme)
    R.add('R0', '등록 문서 §2 · §3 · 수확 묶음 README 값을 읽었다 (자리 하나 · 값 하나)', not rp, rp)
    #  ── ① 등록 집합 ──
    tbl = NP.REGISTERED_ID_SETS.get(SET) or {}
    R.add('A1', f'실행기 등록 표 REGISTERED_ID_SETS[{SET!r}] = 등록 문서 §2 (케이스 수 · ids_sha256 · 코호트 {COHORT} 수)',
          reg.get('n') is not None and tbl.get('n') == reg.get('n') and tbl.get('ids_sha256') == reg.get('ids_sha256')
          and tbl.get('cohort_n') == {COHORT: reg.get('n')},
          dict(table={k: tbl.get(k) for k in ('n', 'ids_sha256', 'cohort_n')}, document={k: reg.get(k) for k in ('n', 'ids_sha256')}))
    try:
        regset, why = NP.registered_id_set(SET), ''
    except NP.LaunchError as e:
        regset, why = None, str(e)
    R.add('A2', f'등록 집합 {SET} 성립 — 커밋된 수확 폴더 ({NP.COHORT_SPECS[COHORT]["harvest"]}) 에서 열거 = 등록 (수 · 코호트 · 지문)', regset is not None, why)
    reg_ids = sorted(c for c, _h in (regset or {}).get('pairs', ()))
    #  ── ①② 계획 · 입력 지문 (발사 dry-run 과 같은 함수) ──
    try:
        plan, why = plan_for(harvest, cohort), ''
    except NP.LaunchError as e:
        plan, why = None, str(e)
    nm = NP.registered_production_set(plan) if plan else None
    R.add('B1', f'계획 (실행기 build_plan · --cohorts {COHORT}) = 등록 생산 집합 {SET} — 아니면 일반 계획 (강등 · 판정문 §4)', nm == SET,
          why or f'registered_production_set = {nm!r}')
    rr = followup_reread(plan) if plan else []
    R.add('B2', f'후속 ⓪b 다시 읽기 명령 = --expect-set {SET} (실행기 print_followups) — --expect-case 나열 = 강등',
          len(rr) == 1 and f'--expect-set {SET}' in rr[0] and '--expect-case' not in rr[0], rr[0][:240] if rr else '명령 줄 없음')
    dg = NP.plan_input_digest(plan) if plan else {}
    want = dict(n=reg.get('n'), ids_sha256=reg.get('ids_sha256'), raw_sha256_table_sha256=reg.get('raw_sha256_table_sha256'), missing_raw_sha=[],
                cohort_tsv_sha256={COHORT: reg.get('cohort_tsv_sha256')})
    bad = [k for k in want if dg.get(k) != want[k]]
    R.add('B3', '입력 지문 (실행기 plan_input_digest · 반입 파일에서 다시 계산) = 등록 §2 (케이스 수 · ids · raw sha 표 · 원자료 결손 0 · 코호트 TSV)',
          plan is not None and all(reg.get(k) for k in ('n', 'ids_sha256', 'raw_sha256_table_sha256', 'cohort_tsv_sha256')) and not bad,
          {k: [dg.get(k), want[k]] for k in bad})
    #  ── ③ 수확기 판 · 반입 파일 = r3 묶음 · 설계 · r2 대조 ──
    spec = NP.COHORT_SPECS[COHORT]
    hdir, ctsv, utsv = _rp(harvest or spec['harvest']), _rp(cohort or spec['cohort']), _rp(spec['union'])
    m3, bad3 = _tar_files(_rp(r3_tgz), R3_TOP)
    head = (m3.get(R3_TOP + 'harvest_head.txt') or b'').decode('utf-8', 'replace').strip()
    pin = reg.get('harvest_pin') or ''
    R.add('C1', 'r3 묶음 sha256 = README · 항목 경로 안전 (한 폴더 · 절대 · .. · 링크 없음) · harvest_head = README 값 · 등록 수확기 판 접두',
          _sha(_rp(r3_tgz)) == reg.get('r3_tgz_sha256') and not bad3 and bool(pin) and head == reg.get('harvest_head') and head.startswith(pin),
          dict(sha256=_sha(_rp(r3_tgz)), bad_members=bad3[:5], harvest_head=head, pin=pin))
    dpre = R3_TOP + 'descriptors_r3/'
    case_b = sorted(n[len(dpre):-5] for n in m3 if n.startswith(dpre + 'lhss_') and n.endswith('.json'))
    case_h = sorted(p.stem for p in hdir.glob('*.json') if not p.name.startswith('_')) if hdir.is_dir() else []

    def _same(path, member):
        try:
            return Path(path).read_bytes() == m3.get(member)
        except OSError:
            return False
    diff = [c for c in case_b if c in case_h and not _same(hdir / f'{c}.json', f'{dpre}{c}.json')]
    side = {'_batch_summary.json': _same(hdir / '_batch_summary.json', dpre + '_batch_summary.json'),
            '_cohort.tsv': _same(ctsv, R3_TOP + '_cohort.tsv'), 'union': _same(utsv, R3_TOP + 'lhss20_union_r3.tsv')}
    R.add('C2', f'반입 파일 = r3 묶음 바이트 — 기술자 {reg.get("n")} (ID = 등록 집합) · _batch_summary · 코호트 TSV · union',
          bool(case_b) and case_b == case_h == reg_ids and not diff and all(side.values()),
          dict(bundle_only=sorted(set(case_b) - set(case_h)), harvest_only=sorted(set(case_h) - set(case_b)), not_registered=sorted(set(case_h) ^ set(reg_ids)),
               bytes_differ=diff[:5], side={k: v for k, v in side.items() if not v}))
    R.add('C3', '설계 CSV (보충 설계) · 어댑터 출력 CSV sha256 = 등록 §2',
          _sha(_rp(SUPP_DESIGN)) == reg.get('design_csv_sha256') and _sha(_rp(spec['design'])) == reg.get('adapter_csv_sha256'),
          dict(design=_sha(_rp(SUPP_DESIGN)), adapter=_sha(_rp(spec['design']))))
    m2, bad2 = _tar_files(_rp(r2_tgz), R2_TOP)
    r2 = {n[len(R2_TOP + 'descriptors_r2/'):-5]: n for n in m2 if n.startswith(R2_TOP + 'descriptors_r2/lhss_') and n.endswith('.json')}
    dk, only2, only3, perr = set(), set(), set(), []
    for c in case_b:
        try:
            a, b = _flat(json.loads(m2[r2[c]])), _flat(json.loads(m3[f'{dpre}{c}.json']))
        except (KeyError, ValueError) as e:
            perr.append(f'{c}: {type(e).__name__}')
            continue
        dk |= {k for k in a.keys() & b.keys() if a[k] != b[k]}
        only2 |= a.keys() - b.keys()
        only3 |= b.keys() - a.keys()
    try:
        u2, u3 = _tsv_cells(m2[R2_TOP + 'lhss20_union_r2.tsv']), _tsv_cells(m3[R3_TOP + 'lhss20_union_r3.tsv'])
    except (KeyError, UnicodeDecodeError) as e:
        u2, u3 = None, f'{type(e).__name__}: {e}'
    R.add('C4', 'r2 ↔ r3 키별 대조 (README 끝) — r2 묶음 sha256 = README · 같은 케이스 · 공통 키 값 같음 (수확 체크아웃 경로 1 키만 예외) · r2 에만 = '
                'wall_near_tangent 진단 · r3 에만 0 · union 칸 차이 0',
          _sha(_rp(r2_tgz)) == reg.get('r2_tgz_sha256') and not bad2 and sorted(r2) == case_b and not perr and dk <= set(R2_DIFF_OK)
          and all(k.startswith(R2_ONLY_OK) for k in only2) and not only3 and u2 is not None and u2 == u3,
          dict(sha256=_sha(_rp(r2_tgz)), bad_members=bad2[:5], cases_r2=len(r2), parse=perr[:3], diff_keys=sorted(dk - set(R2_DIFF_OK))[:5],
               r2_only_other=sorted(k for k in only2 if not k.startswith(R2_ONLY_OK))[:5], r3_only=sorted(only3)[:5], union_equal=(u2 == u3)))
    #  ── ④ 도구 핀 ──
    fp_now = NP.code_fp(NP.code_hashes())
    R.add('D1', '이 체크아웃의 봉인 32 code_fp = 등록 §3 (수치 봉인 무변경)', fp_now is not None and fp_now == reg.get('code_fp'), dict(now=fp_now, registered=reg.get('code_fp')))
    #  ── 발사 dry-run · manifest (주면) ──
    scope = 'container'
    if dry_run_log:
        scope = 'dry_run'
        try:
            text = Path(dry_run_log).read_text(encoding='utf-8')
        except OSError as e:
            R.add('E0', f'dry-run 화면 파일 읽기 ({dry_run_log})', False, f'{type(e).__name__}: {e}')
        else:
            _dry_checks(R, text, dg, reg)
    sman = pman = None
    if manifest:
        scope = 'launch'
        sman = _manifest_checks(R, 'F', manifest, SET, reg, dg)
    if primary_manifest:
        scope = 'launch'
        pman = _manifest_checks(R, 'G', primary_manifest, 'production194', reg)
    if isinstance(sman, dict) and isinstance(pman, dict):
        r_s, r_p = os.path.realpath(os.path.dirname(os.path.abspath(manifest))), os.path.realpath(os.path.dirname(os.path.abspath(primary_manifest)))
        gs, gp = (sman.get('git') or {}).get('sha'), (pman.get('git') or {}).get('sha')
        R.add('H1', '새 ROOT 둘 (194 · 보충 manifest 의 폴더가 다르다) · 같은 발사 커밋 (git.sha) · 같은 발사 봉인 지문',
              r_s != r_p and bool(gs) and gs == gp and (sman.get('seal') or {}).get('code_fp') == (pman.get('seal') or {}).get('code_fp'),
              dict(roots=[r_p, r_s], git=[gp, gs]))
    git = NP.git_info()
    rc = 0 if all(c['ok'] for c in R.checks) else 1
    return dict(schema=SCHEMA, scope=scope, generated=datetime.datetime.now().isoformat(timespec='seconds'), registered_set=SET,
                registration=dict(document=reg_doc, values=reg), recomputed=dict(input_digest=dg, registered_ids=reg_ids),
                inputs=dict(harvest=str(hdir), cohort_tsv=str(ctsv), union=str(utsv), design=SUPP_DESIGN, adapter=spec['design'], r3_bundle=str(r3_tgz),
                            r2_bundle=str(r2_tgz), dry_run_log=dry_run_log, manifest=manifest, primary_manifest=primary_manifest),
                recorded=dict(git=dict(sha=git.get('sha'), dirty=git.get('dirty'), porcelain=git.get('porcelain', [])[:10]), code_fp=fp_now,
                              tool_sha256={rel: NP.sha256_file(NP.ROOT / rel) for rel in TOOL_PINS}),
                checks=R.checks, manual=[dict(item=m, verified_by_tool=False) for m in MANUAL], notes=dict(notes or {}), rc=rc)


def print_receipt(rec, out=print):
    out(f'══ 보충 20 입력 지문 영수증 ({rec["schema"]} · 범위 {rec["scope"]} · git {str(rec["recorded"]["git"]["sha"])[:12]}'
        f'{" dirty" if rec["recorded"]["git"]["dirty"] else ""})')
    for c in rec['checks']:
        out(f'  {"✓" if c["ok"] else "✗"} {c["id"]:3s} {c["name"]}' + ('' if c['ok'] else f'  — {json.dumps(c["detail"], ensure_ascii=False)[:400]}'))
    dg = rec['recomputed']['input_digest'] or {}
    out(f'  다시 계산: 케이스 {dg.get("n")} · ids_sha256 {dg.get("ids_sha256")} · raw_sha256_table_sha256 {dg.get("raw_sha256_table_sha256")} · '
        f'코호트 TSV {dg.get("cohort_tsv_sha256")}')
    for m in rec['manual']:
        out(f'  ⬜ 수동 (도구가 인증하지 않음) — {m["item"]}')
    for k, v in rec['notes'].items():
        out(f'  · 기록 {k}: {v}')
    n_bad = sum(not c['ok'] for c in rec['checks'])
    out(f'rc {rec["rc"]} — 대조 {len(rec["checks"])} 칸 · 다름 {n_bad}' + ('' if n_bad else ' (⚠ 발사 승인 아님 — 수동 칸 · 저자 승인은 따로)'))


# ─────────────────────────────────── selftest (반례 먼저 — 수정 계획 §3) ───────────────────────────────────
def _selftest() -> int:
    ok, fail = 0, []

    def chk(name, cond, why=''):
        nonlocal ok
        if cond:
            ok += 1
            print(f'  PASS  {name}')
        else:
            fail.append(name)
            print(f'  FAIL  {name}' + (f'  ({str(why)[:300]})' if why else ''))

    def bad_ids(rec):
        return {c['id'] for c in rec.get('checks', []) if not c['ok']}

    def expect(name, rec, ids):
        """rc 1 + 겨눈 칸 (ids) 이 전부 실패 칸 안 — 엉뚱한 칸의 실패로 통과시키지 않는다."""
        b = bad_ids(rec)
        chk(f'{name} → rc 1 · 실패 칸 ⊇ {sorted(ids)}', rec.get('rc') == 1 and set(ids) <= b, sorted(b))

    spec = NP.COHORT_SPECS[COHORT]
    base = receipt()
    chk('S0 정상 (커밋된 실물 · 컨테이너 범위) → rc 0 · 대조 칸 R0 · A1 · A2 · B1–B3 · C1–C4 · D1 전부 같음 · 범위 container · 수동 칸 셋',
        base['rc'] == 0 and base['scope'] == 'container' and {c['id'] for c in base['checks']} == {'R0', 'A1', 'A2', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'D1'}
        and len(base['manual']) == 3 and not any(m['verified_by_tool'] for m in base['manual']), sorted(bad_ids(base)))
    reg = base['registration']['values']
    dg0 = base['recomputed']['input_digest']
    chk('S0b 다시 계산 = 등록 §2 (케이스 20 · ids 991cf115… · raw a7aaa3c8… · 코호트 TSV 69d3f913…) — 값은 문서 · 반입 파일에서 (도구에 사본 없음)',
        dg0.get('n') == 20 and str(dg0.get('ids_sha256')).startswith('991cf115') and str(dg0.get('raw_sha256_table_sha256')).startswith('a7aaa3c8')
        and str((dg0.get('cohort_tsv_sha256') or {}).get(COHORT)).startswith('69d3f913') and reg.get('code_fp', '').startswith('e8b2496b'), (dg0, reg.get('code_fp')))
    with tempfile.TemporaryDirectory(prefix='supp20_receipt_') as td:
        td = Path(td)

        def hcopy(name, edit=None):
            d = td / name
            shutil.copytree(_rp(spec['harvest']), d)
            if edit:
                edit(d)
            return str(d)

        #  ① raw sha 표 바꿈 — 같은 20 ID (등록 판정 유지 = Codex 탐침) 인데 입력 지문이 다르다
        def _raw(d):
            j = json.loads((d / 'lhss_007.json').read_text(encoding='utf-8'))
            j['raw']['atom']['sha256'] = 'f' * 64
            (d / 'lhss_007.json').write_text(json.dumps(j), encoding='utf-8')
        expect('S1 raw sha 표 바꿈 (lhss_007 raw.atom.sha256 · 같은 20 ID — 등록 판정은 유지)', receipt(harvest=hcopy('h_raw', _raw)), {'B3', 'C2'})
        r1 = receipt(harvest=hcopy('h_raw2', _raw))
        chk('S1b 같은 반례에서 계획은 여전히 등록 집합 supp20 (B1 · B2 통과) — ID 지문만으로는 못 잡는다는 Codex 관찰 그대로 · 잡는 칸 = B3',
            not ({'B1', 'B2'} & bad_ids(r1)) and 'B3' in bad_ids(r1), sorted(bad_ids(r1)))
        #  ② 코호트 TSV 한 바이트
        tsv = td / 'cohort_1byte.tsv'
        b = bytearray(_rp(spec['cohort']).read_bytes())
        i = b.index(b'lhss_001') + 4
        b[i:i + 1] = b'S'
        tsv.write_bytes(bytes(b))
        expect('S2 코호트 TSV 한 바이트 바꿈 (--lhss-cohort 와 같은 뜻)', receipt(cohort=str(tsv)), {'B3', 'C2'})
        #  ③ ID 하나 바꿈 — lhss_005 → lhss_105 (계획이 등록 집합이 아니다 = 일반 계획 · 후속 --expect-case)
        expect('S3 ID 하나 바꿈 (lhss_005 → lhss_105)', receipt(harvest=hcopy('h_id', lambda d: (d / 'lhss_005.json').rename(d / 'lhss_105.json'))),
               {'B1', 'B2', 'B3', 'C2'})
        #  ④ 등록 문서 값 오타 — raw · ids · 코호트 TSV · code_fp 한 글자
        rtxt = _rp(REG_DOC).read_text(encoding='utf-8')
        for k, ids in (('raw_sha256_table_sha256', {'B3'}), ('ids_sha256', {'A1', 'B3'}), ('cohort_tsv_sha256', {'B3'}), ('code_fp', {'D1'})):
            v = reg[k]
            bad_v = v[:-1] + ('0' if v[-1] != '0' else '1')
            p = td / f'reg_{k}.md'
            p.write_text(rtxt.replace(v, bad_v), encoding='utf-8')
            expect(f'S4 등록 문서 {k} 오타 (끝 한 글자)', receipt(reg_doc=str(p)), ids)
        p = td / 'reg_dup.md'
        p.write_text(rtxt + f'\n| `raw_sha256_table_sha256` | `{"0" * 64}` |\n', encoding='utf-8')
        expect('S4b 등록 문서에 같은 칸이 값 둘 (raw sha 표 두 행)', receipt(reg_doc=str(p)), {'R0', 'B3'})
        #  ⑤ 일반 계획 강등 — 계획에 후막 lhst 한 건 더 (21) · 등록 집합이 안 선다 (커밋 수확 폴더가 등록과 다르다 · 19 건)
        expect('S5 일반 계획 강등 — 수확 폴더에 후막 lhst_045_6m 하나 더 (21 건)',
               receipt(harvest=hcopy('h_thick', lambda d: shutil.copy2(d / 'lhss_020.json', d / 'lhst_045_6m.json'))), {'B1', 'B2', 'B3', 'C2'})
        h19 = hcopy('h19', lambda d: (d / 'lhss_013.json').unlink())
        NP.COHORT_SPECS[COHORT] = dict(spec, harvest=h19)
        try:
            r5 = receipt()
        finally:
            NP.COHORT_SPECS[COHORT] = spec
        expect('S5b 일반 계획 강등 — 등록 집합 자체가 안 선다 (커밋된 수확 폴더 19 건 · registered_id_set 거부)', r5, {'A2', 'B1', 'B2', 'B3', 'C2'})
        #  ⑥ ③ 칸 — r3 묶음 · r2 묶음 (바꾼 묶음의 sha 를 README 사본에 적어 sha 칸은 통과시키고 겨눈 칸만 본다)
        def repack(src, dst, top, edit):
            files, _bad = _tar_files(_rp(src), top)
            edit(files)
            with tarfile.open(dst, 'w:gz') as tf:
                for n, data in sorted(files.items()):
                    ti = tarfile.TarInfo(n)
                    ti.size = len(data)
                    tf.addfile(ti, io.BytesIO(data))
            p_ = td / f'README_{Path(dst).stem}.md'
            p_.write_text(_rp(RUNS_README).read_text(encoding='utf-8').replace(_sha(_rp(src)), _sha(dst)), encoding='utf-8')
            return str(dst), str(p_)
        r3x, rx = repack(R3_TGZ, td / 'r3x.tgz', R3_TOP, lambda f: f.__setitem__(R3_TOP + 'descriptors_r3/lhss_002.json',
                                                                                  f[R3_TOP + 'descriptors_r3/lhss_002.json'] + b' '))
        r6 = receipt(r3_tgz=r3x, readme=rx)
        expect('S6 r3 묶음의 기술자 한 바이트 바뀐 묶음 (README sha 도 맞춘 사본 — 반입 파일 ≠ 묶음 바이트)', r6, {'C2'})
        chk('S6a 같은 반례 · README 원본 = 묶음 sha 다름 (C1) 도', 'C1' in bad_ids(receipt(r3_tgz=r3x)), '')
        r3h, rh = repack(R3_TGZ, td / 'r3h.tgz', R3_TOP, lambda f: f.__setitem__(R3_TOP + 'harvest_head.txt', b'cc4210080' + b'0' * 31 + b'\n'))
        expect('S6b r3 묶음 harvest_head = 다른 수확기 판 (README sha 맞춘 사본 · 기술자 그대로)', receipt(r3_tgz=r3h, readme=rh), {'C1'})

        def _r2v(f):
            k = R2_TOP + 'descriptors_r2/lhss_004.json'
            j = json.loads(f[k])
            j['phi_se'] = (j.get('phi_se') or 0) + 1e-9
            f[k] = json.dumps(j).encode('utf-8')
        r2v, r2r = repack(R2_TGZ, td / 'r2v.tgz', R2_TOP, _r2v)
        expect('S6c r2 묶음 공통 키 값 하나 다름 (phi_se + 1e-9 · README sha 맞춘 사본)', receipt(r2_tgz=r2v, readme=r2r), {'C4'})
        r2u, r2ur = repack(R2_TGZ, td / 'r2u.tgz', R2_TOP, lambda f: f.__setitem__(R2_TOP + 'lhss20_union_r2.tsv',
                                                                                    f[R2_TOP + 'lhss20_union_r2.tsv'].replace(b'lhss_001', b'lhss_999', 1)))
        expect('S6d r2 묶음 union 칸 하나 다름 (README sha 맞춘 사본)', receipt(r2_tgz=r2u, readme=r2ur), {'C4'})
        #  ⑦ 발사 dry-run 화면 — 진짜 print_preflight 로 만든 화면 (생산자 줄 꼴과 맞댄다)
        plan = plan_for()
        fp = NP.code_fp(NP.code_hashes())

        def dry(dg=None, dirty=False, stop=(), raw_n=0, gen='g2', fp_to=None, drop=None):
            pf = dict(cpu=dict(cpu_count=20, cpu_affinity=20), mem=dict(MemTotal_GB=64, MemAvailable_GB=60, SwapFree_GB=0, SwapTotal_GB=0),
                      mem_budget_mb=50 * 1024.0, lanes=20, first_lanes_est_mem_GB=1.0, est_mem_largest_mb=600.0, disk_free_GB=100, disk_need_GB=1,
                      est_serial_h=0.5, est_makespan_h=0.1, git=dict(short='0123456789', branch='HEAD', dirty=dirty, porcelain=[' M x.py'] if dirty else []),
                      n_raw_problems=raw_n, generation=dict(generation=gen, problems=[], modes=['hertz', 'physics', 'hertz_h12']),
                      dependency_closure=dict(files=list(NP.CODE_FILES[:5]), errors=[]), lazy_census=dict(n_lazy=3, unclassified=[]), fork_census=[],
                      input_digest=dg or dg0, warn=[], stop=list(stop))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                NP.print_preflight(pf, plan, types.SimpleNamespace(min_free_gb=1.0, network_lock='per-case'), Path('/x/netsupp20_selftest'))
            text = buf.getvalue().replace(fp, fp_to) if fp_to else buf.getvalue()
            if drop:
                text = '\n'.join(ln for ln in text.splitlines() if drop not in ln)
            p = td / f'dry_{len(list(td.glob("dry_*")))}.log'
            p.write_text(text, encoding='utf-8')
            return str(p)

        rd = receipt(dry_run_log=dry())
        chk('S7 dry-run 화면 (print_preflight 그대로 · 관측 ON 계획 · 깨끗한 트리) → rc 0 · 범위 dry_run · E1–E6 같음',
            rd['rc'] == 0 and rd['scope'] == 'dry_run' and {'E1', 'E2', 'E3', 'E4', 'E5', 'E6'} <= {c['id'] for c in rd['checks']}, sorted(bad_ids(rd)))
        grep = td / 'dry_grep.log'                           # 등록 §4 의 grep (코드 · 기대 망 세대 · 전이 의존 · 지연 import · fork · 입력 지문 · 원자료 · ⛔)
        keep = ('코드 ', '기대 망 세대', '전이 의존', '지연 import', 'fork', '입력 지문', '원자료 · 메시 문제', '⛔')
        grep.write_text('\n'.join(ln for ln in Path(dry()).read_text(encoding='utf-8').splitlines() if any(k in ln for k in keep)), encoding='utf-8')
        rg = receipt(dry_run_log=str(grep))
        chk('S7b 등록 §4 grep 으로 거른 화면 → rc 0 (코호트 줄 없음 = E6 생략)', rg['rc'] == 0 and 'E6' not in {c['id'] for c in rg['checks']}, sorted(bad_ids(rg)))
        expect('S7c dry-run 입력 지문 raw sha 표 다름', receipt(dry_run_log=dry(dg=dict(dg0, raw_sha256_table_sha256='0' * 64))), {'E1'})
        expect('S7d dry-run 이 일반 계획 (케이스 21 · ids 다름)', receipt(dry_run_log=dry(dg=dict(dg0, n=21, ids_sha256='1' * 64))), {'E1'})
        expect('S7e dry-run 사전 점검 중단 ⛔ (관측 끈 보충 계획)',
               receipt(dry_run_log=dry(stop=[NP.production_observation_problem(dict(plan=plan, observe_imports=False))])), {'E5'})
        expect('S7f dry-run dirty=True (--allow-dirty 로 돈 화면)', receipt(dry_run_log=dry(dirty=True)), {'E2'})
        expect('S7g dry-run 봉인 지문 다름', receipt(dry_run_log=dry(fp_to='e' * 64)), {'E2'})
        expect('S7h dry-run 입력 지문 줄 없음', receipt(dry_run_log=dry(drop='입력 지문')), {'E1'})
        expect('S7i dry-run 원자료 · 메시 문제 1 건', receipt(dry_run_log=dry(raw_n=1)), {'E4'})
        expect('S7j dry-run 기대 망 세대 None (유도 실패)', receipt(dry_run_log=dry(gen=None)), {'E3'})
        #  ⑧ 실제 발사 manifest — 실행기 cmd_run 이 쓰는 키 (launch_eligibility 가 current 로 읽는 꼴)
        def man(plan_, dg_, root, fname='manifest.json', **over):
            hashes = NP.code_hashes()
            m = dict(schema=NP.SCHEMA, launch_format=NP.LAUNCH_FORMAT, plan=plan_, input_digest=dg_, code_hashes=hashes,
                     code_dependency_closure=list(NP.CODE_FILES), handover_code_hashes={rel: NP.sha256_file(NP.ROOT / rel) for rel in NP.HANDOVER_FILES},
                     git=dict(sha='ab' * 20, short='abababab', dirty=False), observe_imports=True, import_obs_run_id='cd' * 16,
                     generation_probe=dict(generation='g2', problems=[]), **{NP.GEN_KEY: 'g2'},
                     seal=dict(schema=NP.LAUNCH_SEAL_SCHEMA, launch_format=NP.LAUNCH_FORMAT, code_fp=NP.code_fp(hashes), files=len(hashes),
                               **{NP.GEN_KEY: 'g2'}))
            for k, v in over.items():
                m[k] = v(m) if callable(v) else v
            d = td / root
            d.mkdir(exist_ok=True)
            (d / fname).write_text(json.dumps(m), encoding='utf-8')
            return str(d / fname)
        p194 = NP.build_plan(['lhs', 'lhsx'], NP.cohort_specs(types.SimpleNamespace()), (), 'cost')
        mp194 = man(p194, NP.plan_input_digest(p194), 'root194')
        rm = receipt(manifest=man(plan, dg0, 'rootS'), primary_manifest=mp194)
        chk('S8 실제 발사 manifest 둘 (보충 · 194 · 다른 ROOT · 같은 발사 커밋 · 관측 ON) → rc 0 · 범위 launch · F0–F6 · G0–G2 · G4 · G5 · H1 같음',
            rm['rc'] == 0 and rm['scope'] == 'launch' and {'F1', 'F3', 'F4', 'F6', 'G1', 'G2', 'H1'} <= {c['id'] for c in rm['checks']}, sorted(bad_ids(rm)))
        expect('S8b 보충 manifest 관측 끔 (observe_imports false)', receipt(manifest=man(plan, dg0, 'rS_obs', observe_imports=False)), {'F4'})
        expect('S8c 보충 manifest input_digest raw sha 표 다름', receipt(manifest=man(plan, dict(dg0, raw_sha256_table_sha256='2' * 64), 'rS_dg')), {'F3'})
        p21 = plan_for(harvest=hcopy('h_thick2', lambda d: shutil.copy2(d / 'lhss_020.json', d / 'lhst_045_6m.json')))
        expect('S8d 보충 manifest 계획 = 일반 계획 (후막 하나 더 · 21)', receipt(manifest=man(p21, NP.plan_input_digest(p21), 'rS_gen')), {'F2', 'F3'})
        expect('S8e 보충 manifest git.dirty true', receipt(manifest=man(plan, dg0, 'rS_dirty', git=dict(sha='ab' * 20, short='abababab', dirty=True))), {'F5'})

        def _other_fp(m):
            h = dict(m['code_hashes'], **{NP.CODE_FILES[0]: '0' * 64})
            return h
        mo = man(plan, dg0, 'rS_fp', code_hashes=_other_fp)
        mj = json.loads(Path(mo).read_text(encoding='utf-8'))
        mj['seal']['code_fp'] = NP.code_fp(mj['code_hashes'])                       # 봉인이 자기 해시 지도와는 맞다 (자격 current) · 등록 §3 과 다르다
        Path(mo).write_text(json.dumps(mj), encoding='utf-8')
        expect('S8f 보충 manifest 발사 봉인 지문 ≠ 등록 §3 (자기 해시 지도와는 일관)', receipt(manifest=mo), {'F5'})
        rsame = receipt(manifest=man(plan, dg0, 'root194', fname='manifest_supp.json'), primary_manifest=mp194)
        expect('S8g 보충 · 194 manifest 가 같은 ROOT 폴더 (나머지 칸은 정상)', rsame, {'H1'})
        chk('S8g2 같은 반례 — 실패 칸은 H1 하나 (보충 · 194 manifest 각자는 정상)', bad_ids(rsame) == {'H1'}, sorted(bad_ids(rsame)))
        expect('S8h 194 자리에 보충 manifest (등록 집합 production194 아님)', receipt(manifest=man(plan, dg0, 'rS2'), primary_manifest=man(plan, dg0, 'rP2')),
               {'G2'})
        expect('S8i 보충 manifest 인계 도구 지문 ≠ 이 체크아웃 (다른 체크아웃에서 만든 영수증)',
               receipt(manifest=man(plan, dg0, 'rS_ho', handover_code_hashes=lambda m: {k: '9' * 64 for k in m['handover_code_hashes']})), {'F6'})
        expect('S8j 보충 manifest 없음 · 깨진 JSON', receipt(manifest=str(td / 'nope.json')), {'F0'})
        #  ⑨ 읽기 전용 — 정상 영수증을 만든 뒤 리포 입력 파일 sha 가 그대로
        snap = {rel: _sha(_rp(rel)) for rel in (REG_DOC, RUNS_README, R3_TGZ, R2_TGZ, SUPP_DESIGN, spec['design'], spec['cohort'], spec['union'])}
        receipt(dry_run_log=dry())
        chk('S9 읽기 전용 — 영수증을 만들어도 등록 문서 · README · 묶음 둘 · 설계 · 어댑터 · 코호트 TSV · union 바이트 그대로',
            snap == {rel: _sha(_rp(rel)) for rel in snap}, snap)
    print(f'\nsupp20_input_receipt selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='보충 20 (supp20) 입력 지문 영수증 — 읽기 전용 (Codex 보충 20 지원 검토 Q6 · 수정 계획 sup20_fix_plan_20261012 §3)')
    ap.add_argument('--selftest', action='store_true', help='반례 시험 (raw sha 표 · TSV 한 바이트 · ID · 등록 값 오타 · 일반 계획 강등 · 묶음 · dry-run · manifest)')
    ap.add_argument('--dry-run-log', default='', help='발사 dry-run 화면 파일 (run --cohorts lhss --dry-run --observe-imports 출력 · 등록 4 절의 grep 결과도 된다)')
    ap.add_argument('--manifest', default='', help='실제 보충 발사 ROOT 의 manifest.json')
    ap.add_argument('--primary-manifest', default='', help='같은 날 194 발사 ROOT 의 manifest.json (새 ROOT 둘 · 같은 발사 커밋 대조)')
    ap.add_argument('--lhss-harvest', default='', help='수확 폴더 (실행기 --lhss-harvest 와 같은 뜻 · 기본 = 실행기 COHORT_SPECS)')
    ap.add_argument('--lhss-cohort', default='', help='코호트 TSV (실행기 --lhss-cohort 와 같은 뜻 · 기본 = 실행기 COHORT_SPECS)')
    ap.add_argument('--registration', default=REG_DOC, help='등록 문서 (기본 = 보충 20 등록)')
    ap.add_argument('--precheck-note', default='', help='사전 점검 결과 메모 (기록만 · 도구가 인증하지 않는다)')
    ap.add_argument('--approval-note', default='', help='저자 발사 승인 메모 (기록만 · 도구가 인증하지 않는다)')
    ap.add_argument('--json', default='', help='영수증 JSON 을 쓸 곳 (주지 않으면 아무 파일도 안 쓴다)')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    notes = {k: v for k, v in (('precheck', a.precheck_note), ('approval', a.approval_note)) if v}
    rec = receipt(reg_doc=a.registration, harvest=a.lhss_harvest or None, cohort=a.lhss_cohort or None, dry_run_log=a.dry_run_log or None,
                  manifest=a.manifest or None, primary_manifest=a.primary_manifest or None, notes=notes)
    print_receipt(rec)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    return rec['rc']


if __name__ == '__main__':
    sys.exit(main())
