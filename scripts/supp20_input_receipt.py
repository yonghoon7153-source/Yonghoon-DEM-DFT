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
  ⑤ ★ 10-14 SUPR-01 · SUPR-02 (Codex 보충 20 수정 재검증 §4 · §5 · 수정 계획 `docs/reviews/supr_fix_plan_20261014.md` · 1저자 Q1–Q3 (가)) — 발사 사전 점검 증거 =
     실행기 완료 영수증 (`run … --dry-run --observe-imports --preflight-receipt P.json` 이 쓴 JSON + 실행기가 직접 잡은 전체 로그 P.log).  P0–P10 = 실행기
     `preflight_receipt_checks` (로그 sha256 · INPUT_DIGEST_JSON 한 줄 · 완료 · 실제 종료코드 · 관측 · 필수 세 검사 · argv = 등록 명령 · 코드 · 세대 · 원자료 ·
     이 체크아웃 재계산 · 승인 SHA) + E1 (로그 지문 = 등록 §2 = 반입 재계산 — 코호트 TSV sha 포함) · E2 (봉인 지문 = 등록 §3).  텍스트 · grep 로그 단독
     (`--dry-run-log`) = E0 실패 (옛 판: 다른 TSV 로 돈 로그 · 잘린 로그 · 필수 줄이 빠진 로그가 rc 0).  승인 SHA (`--approved-sha`) 를 주면 사전 점검 · manifest 의
     git 기록과 접두 대조 (P10 · F7 · G7) · 주지 않으면 notes 에 경고 (실패 아님).
  ⑥ ★ 10-15 (나′) 대기 지문 (1저자 10-15 Q1 (나′)) — 등록 문서의 선택 선언 `code_fp_pending <64 hex>` (비준 · 재등록 전의 새 봉인 지문) 를 읽어 D1 상세에만 싣는다
     (값 둘 이상 · 등록 §3 과 같음 = R0 문제).  발사 대조 D1 · E2 · F5 · G5 = 등록 §3 값만 (대기 선언은 통과시키지 않는다 — 비준 · 재등록 전 발사 불가) ·
     selftest 만 선언된 대기 상태를 기록 종류별 정확한 실패 집합으로 받는다 (컨테이너 {D1} · 사전 점검 {D1 · E2} · 발사 manifest 둘 {D1 · F5 · G5}).
  ⑦ ★ 10-16 L214R-04 (Codex LHS214 재검증 판정문 §5 · 수정 계획 `docs/reviews/lhs214r_fix_plan_20261016.md` Q4 = 1저자 비준) — 등록 code_fp = **활성 §3 (`## 3.` 절)
     안의** `code_fp <64 hex>` 만 읽는다.  옛 판은 문서 전체의 같은 기계 구문을 읽어, 안내된 비준 단계 (§3 갱신 + 대기 선언 삭제 + 역사 표 보존) 가 R0 · D1
     (registered None) 였다.  등록 문서 · 역사 표는 고치지 않는다 · §3 제목이 없거나 둘이면 R0 · 대기 선언 · 발사 대조 규칙은 ⑥ 그대로 (selftest ⑫).
값의 정본은 실행기 함수 (`run_network_194_parallel` — registered_id_set · build_plan · cohort_specs · plan_input_digest · registered_production_set ·
print_followups · preflight_receipt_checks · parse_preflight_log · launch_eligibility · production_observation_problem) 와 등록 문서 · 수확 묶음 README 다 —
값을 이 파일에 베껴 두지 않는다 (r2 대조의 허용 차이 두 칸만 README 끝 문장을 옮긴 상수 · 묶음 폴더 이름 둘).

  python3 scripts/supp20_input_receipt.py                                       # 컨테이너 범위 (발사 전 칸)
  python3 scripts/supp20_input_receipt.py --preflight-receipt P.json --approved-sha <발사 커밋>   # + 발사 사전 점검 완료 영수증 (+ 같은 이름 .log)
  python3 scripts/supp20_input_receipt.py --manifest R/manifest.json --primary-manifest R194/manifest.json --approved-sha <발사 커밋>   # + 실제 발사 manifest
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


_MD_HEADING = re.compile(r'^(#{1,6})[ \t]+(\S.*?)[ \t]*$')
_MD_FENCE = re.compile(r'^[ \t]{0,3}(```|~~~)')


def _md_section(text, num):
    """등록 문서의 '## <num>.' 절 (제목 줄 포함 · 다음 같은 수준 이하 (#  · ##) 제목 앞까지) → (글, 사유).  ★ 10-16 L214R-04.
    코드 울타리 (``` · ~~~) 안의 '#' 줄은 제목이 아니다 · 그 제목이 없거나 둘 이상이면 (None, 사유) — 활성 절을 정할 수 없다 (fail-closed)."""
    lines = text.split('\n')
    heads, fence = [], None
    for i, ln in enumerate(lines):
        f_ = _MD_FENCE.match(ln)
        if f_:
            fence = None if fence == f_.group(1) else (fence or f_.group(1))
            continue
        if fence is None:
            m_ = _MD_HEADING.match(ln)
            if m_:
                heads.append((i, len(m_.group(1)), m_.group(2)))
    hit = [h for h in heads if h[1] == 2 and re.match(rf'{re.escape(str(num))}\.(\s|$)', h[2])]
    if len(hit) != 1:
        return None, f'§{num} 제목 (## {num}.) ' + ('없음' if not hit else f'둘 이상 (줄 {[h[0] + 1 for h in hit]})')
    i0, lv, _t = hit[0]
    i1 = next((h[0] for h in heads if h[0] > i0 and h[1] <= lv), len(lines))
    return '\n'.join(lines[i0:i1]), ''


def registration_values(reg_doc=REG_DOC, readme=RUNS_README):
    """등록 문서 §2 · §3 + 수확 묶음 README 의 값 → (dict, 문제 목록).  손으로 옮겨 적지 않고 문서에서 읽는다 (문서 오타 = 재계산과 다름 = rc 1).
    ★ 10-15 (나′) + 선택 항목 code_fp_pending (대기 지문 선언 — 없으면 None · 문제 아님 · 값 둘 이상 · 등록 §3 과 같음 = 문제 · 값 None).
    ★ 10-16 L214R-04 (Codex LHS214 재검증 판정문 §5 · 1저자 Q4) — code_fp = **활성 §3 (`## 3.` 절) 안의** `code_fp <64 hex>` 만 (자리 하나 · 값 하나).  역사 표 ·
      초안 표 (§9 등) 에 같은 기계 구문으로 남은 옛 값은 읽지 않는다 (비준 전환 = §3 갱신 + 대기 선언 삭제 + 역사 표 보존 이 rc 0 이 되게 · 문서 · 역사는 고치지 않는다).
      §3 제목이 없거나 둘이면 문제 (값 None) · 문서 전체 토큰으로 대신하지 않는다.  대기 선언은 예전처럼 문서 전체에서 읽고 발사 대조에는 쓰지 않는다."""
    out, probs = {}, []
    try:
        t = _rp(reg_doc).read_text(encoding='utf-8')
    except OSError as e:
        return out, [f'등록 문서 {reg_doc} 를 못 읽었다 ({type(e).__name__})']
    s3, s3_why = _md_section(t, 3)
    design = NP.COHORT_SPECS[COHORT]['design']
    for k, kind, how in (('n', 're', r'^\|\s*케이스 수\s*\|\s*(\d+)\b'),
                         ('ids_sha256', 're', r'^\|\s*`ids_sha256`[^|\n]*\|\s*`([0-9a-f]{64})`'),
                         ('raw_sha256_table_sha256', 're', r'^\|\s*`raw_sha256_table_sha256`\s*\|\s*`([0-9a-f]{64})`'),
                         ('cohort_tsv_sha256', 're', r'^\|\s*코호트 TSV sha256\s*\|\s*`([0-9a-f]{64})`'),
                         ('code_fp', 's3', r'`code_fp ([0-9a-f]{64})`'),
                         ('harvest_pin', 're', r'재수확 r3 \(`([0-9a-f]{7,40})`\)'),
                         ('design_csv_sha256', 'after', f'(설계 `{SUPP_DESIGN}`'),
                         ('adapter_csv_sha256', 'after', f'설계 어댑터 출력 = `{design}`')):
        if kind == 's3':                     # ★ L214R-04 — 활성 §3 안에서만
            v, why = _one(how, s3) if s3 is not None else (None, s3_why)
            why = f'§3 안 {why}' if (why and s3 is not None) else why
        else:
            v, why = _one(how, t) if kind == 're' else _sha_after(t, how)
        if why:
            probs.append(f'등록 문서 {k} — {why}')
        out[k] = int(v) if (k == 'n' and v is not None) else v
    #  ★ 10-15 (나′) 대기 지문 (1저자 10-15 Q1 (나′)) — 선택 항목 `code_fp_pending <64 hex>` (비준 · 재등록 전의 새 봉인 지문 선언).  0 개 = None (문제 아님) ·
    #    서로 다른 값 둘 이상 = 문제 · 등록 §3 code_fp 와 같음 = 모순 (문제) — 문제면 값 None.  읽어서 D1 상세에만 싣는다: 발사 대조 (D1 · E2 · F5 · G5) 는 등록 값만 본다.
    v, why = _one(r'`code_fp_pending ([0-9a-f]{64})`', t)
    if why and why != '자리 없음':
        probs.append(f'등록 문서 code_fp_pending — {why}')
    elif v is not None and v == out.get('code_fp'):
        probs.append('등록 문서 code_fp_pending — 등록 §3 code_fp 와 같다 (모순 선언 · 대기 지문은 등록 값과 달라야 한다)')
        v = None
    out['code_fp_pending'] = v
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


class _Receipt:
    def __init__(self):
        self.checks = []

    def add(self, cid, name, ok, detail=''):
        self.checks.append(dict(id=cid, name=name, ok=bool(ok), detail=detail if not ok else ''))
        return bool(ok)


_HEX_SHA = re.compile(r'^[0-9a-f]{7,40}$')


def _preflight_registration_checks(R, pv, dg, reg):
    """★ 10-14 SUPR-01 — 사전 점검 완료 영수증 (실행기 대조 P0–P10 은 따로) 의 등록 값 대조 (E) — 실행기는 등록 문서 §2 · §3 값을 모른다.
      E1 로그 INPUT_DIGEST_JSON (한 줄) = 등록 §2 = 반입 파일 재계산 (실행기 plan_input_digest · INPUT_DIGEST_KEYS 전부 · 코호트 TSV sha 포함)
      E2 봉인 지문 code_fp (로그 코드 줄 · 영수증) = 등록 §3 · CODE_FILES 수"""
    pl = pv.get('parsed') or {}
    dls = pl.get('input_digest') or []
    logged = dls[0][1] if len(dls) == 1 else None
    want = dict(n=reg.get('n'), ids_sha256=reg.get('ids_sha256'), raw_sha256_table_sha256=reg.get('raw_sha256_table_sha256'), missing_raw_sha=[],
                cohort_tsv_sha256={COHORT: reg.get('cohort_tsv_sha256')})
    keys = NP.INPUT_DIGEST_KEYS
    differ = {k: dict(logged=(logged or {}).get(k), registered=want.get(k), recomputed=dg.get(k)) for k in keys
              if not (isinstance(logged, dict) and logged.get(k) == want.get(k) == dg.get(k))}
    R.add('E1', f'사전 점검 로그 {NP.INPUT_DIGEST_LINE} (한 줄) = 등록 §2 = 반입 파일 재계산 — {" · ".join(keys)} 전부 (코호트 TSV sha 포함 · SUPR-01)',
          isinstance(logged, dict) and sorted(logged) == sorted(keys) and all(reg.get(k) for k in ('n', 'ids_sha256', 'raw_sha256_table_sha256', 'cohort_tsv_sha256'))
          and not differ, dict(n_lines=len(dls), parsed=isinstance(logged, dict), differ=differ))
    codes = pl.get('code') or []
    c = codes[0] if len(codes) == 1 else None
    rec = pv.get('receipt') if isinstance(pv.get('receipt'), dict) else {}
    R.add('E2', '사전 점검 봉인 지문 code_fp (로그 코드 줄 하나 · 영수증) = 등록 §3 · CODE_FILES 수 = 실행기',
          c is not None and bool(reg.get('code_fp')) and c[4] == reg.get('code_fp') == rec.get('code_fp') and c[5] == str(len(NP.CODE_FILES)),
          dict(log=codes[:2], receipt=rec.get('code_fp'), registered=reg.get('code_fp')))


def _load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8')), ''
    except (OSError, ValueError) as e:
        return None, f'{type(e).__name__}: {e}'


def _manifest_checks(R, label, path, want_set, reg, dg=None, approved_sha=None):
    """실제 발사 manifest 대조 (F = 보충 · G = 194) — 실행 형식 자격 · 등록 생산 집합 · (보충) 입력 지문 · 관측 ON · 봉인 지문 · 깨끗한 트리 · (보충) 인계 도구 지문 ·
    (★ 10-14 Q3 — 승인 SHA 를 주면) git.sha = 승인 SHA."""
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
    if approved_sha:
        a = str(approved_sha).strip().lower()
        R.add(f'{label}7', f'{want_set} manifest git.sha = 승인 SHA (7–40 hex · 접두 · 1저자 Q3 — H1 은 두 manifest 의 상호 일치일 뿐)',
              bool(_HEX_SHA.match(a)) and isinstance(g.get('sha'), str) and bool(re.fullmatch(r'[0-9a-f]{40}', g['sha'])) and g['sha'].startswith(a),
              dict(manifest=g.get('sha'), approved=a))
    return man


def receipt(*, reg_doc=REG_DOC, readme=RUNS_README, harvest=None, cohort=None, dry_run_log=None, preflight_receipt=None, approved_sha=None, manifest=None,
            primary_manifest=None, r3_tgz=R3_TGZ, r2_tgz=R2_TGZ, notes=None) -> dict:
    """영수증 dict (schema · scope · checks · recorded · manual · notes · rc).  rc = 0 이면 기계로 대조한 칸이 전부 같다 (발사 승인 아님).
    ★ 10-14 — preflight_receipt = 실행기 `run --dry-run --preflight-receipt` 의 완료 영수증 JSON (+ 같은 이름 .log) · dry_run_log (텍스트 로그) = 받지 않는다 (E0) ·
    approved_sha = 저자 발사 승인 커밋 (주면 사전 점검 · manifest git 기록과 대조 · 주지 않으면 notes 에 경고)."""
    R = _Receipt()
    notes = dict(notes or {})
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
    R.add('D1', '이 체크아웃의 봉인 32 code_fp = 등록 §3 (수치 봉인 무변경)', fp_now is not None and fp_now == reg.get('code_fp'),
          dict(now=fp_now, registered=reg.get('code_fp'), pending=reg.get('code_fp_pending')))       # ★ 10-15 (나′) 판정식 그대로 (등록 값만) · 상세에 대기 지문
    #  ── 발사 사전 점검 (주면) — ★ 10-14 SUPR-02 · 1저자 Q2 (가): 실행기 완료 영수증 + 그 실행기가 잡은 전체 로그만 받는다 ──
    scope = 'container'
    pv = None
    if dry_run_log or preflight_receipt:
        scope = 'preflight'
    if dry_run_log:
        R.add('E0', '텍스트 · grep 로그 (--dry-run-log) 단독은 사전 점검 증거가 아니다 (SUPR-02 · 1저자 Q2 (가) · 판정문 §5 — 잘린 · 거른 · 필수 줄이 빠진 로그를 가를 수 없다)',
              False, f'{dry_run_log} — 실행기 `run --root <R> --cohorts {COHORT} --dry-run --observe-imports --preflight-receipt <P>.json` 이 쓴 완료 영수증 JSON '
                     '(+ 같은 이름 .log = 실행기 자신이 잡은 전체 로그) 을 --preflight-receipt 로 주라 · 셸 tee · grep 로그와 그 종료코드는 실행기 증거가 아니다')
    if preflight_receipt:
        pv = NP.preflight_receipt_checks(preflight_receipt, expect_set=SET, approved_sha=approved_sha)
        for c in pv['checks']:
            R.add(c['id'], c['name'], c['ok'], c['detail'])
        _preflight_registration_checks(R, pv, dg, reg)
    sman = pman = None
    if manifest:
        scope = 'launch'
        sman = _manifest_checks(R, 'F', manifest, SET, reg, dg, approved_sha=approved_sha)
    if primary_manifest:
        scope = 'launch'
        pman = _manifest_checks(R, 'G', primary_manifest, 'production194', reg, approved_sha=approved_sha)
    if not approved_sha:
        notes['approved_sha'] = ('⚠ --approved-sha 없음 — 사전 점검 · manifest 의 git 기록을 저자 발사 승인 핀과 기계로 대조하지 않았다 (경고 · 실패 아님 · 1저자 Q3) · '
                                 '발사 핀 확인 = 손으로')
    elif not (preflight_receipt or manifest or primary_manifest):
        notes['approved_sha'] = f'⚠ --approved-sha {approved_sha} — 대조할 발사 기록 (--preflight-receipt · --manifest · --primary-manifest) 이 없어 대조하지 않았다'
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
                            r2_bundle=str(r2_tgz), dry_run_log=dry_run_log, preflight_receipt=preflight_receipt,
                            preflight_receipt_sha256=_sha(preflight_receipt) if preflight_receipt else None, preflight_log=(pv or {}).get('log'),
                            approved_sha=approved_sha, manifest=manifest, primary_manifest=primary_manifest),
                recorded=dict(git=dict(sha=git.get('sha'), dirty=git.get('dirty'), porcelain=git.get('porcelain', [])[:10]), code_fp=fp_now,
                              tool_sha256={rel: NP.sha256_file(NP.ROOT / rel) for rel in TOOL_PINS}),
                checks=R.checks, warnings=list((pv or {}).get('warnings') or []), manual=[dict(item=m, verified_by_tool=False) for m in MANUAL], notes=notes, rc=rc)


def print_receipt(rec, out=print):
    out(f'══ 보충 20 입력 지문 영수증 ({rec["schema"]} · 범위 {rec["scope"]} · git {str(rec["recorded"]["git"]["sha"])[:12]}'
        f'{" dirty" if rec["recorded"]["git"]["dirty"] else ""})')
    for c in rec['checks']:
        out(f'  {"✓" if c["ok"] else "✗"} {c["id"]:3s} {c["name"]}' + ('' if c['ok'] else f'  — {json.dumps(c["detail"], ensure_ascii=False, default=str)[:400]}'))
    for w in rec.get('warnings') or []:
        out(f'  ⚠ 경고 — {w}')
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
        chk(f'{name} → rc 1 · 실패 칸 ⊇ {sorted(ids)}', rec.get('rc') == 1 and set(ids) <= b, sorted(b) or rec.get('error'))

    def rsafe(**kw):
        """receipt() — 옛 판에 없는 인자 (preflight_receipt · approved_sha) 는 TypeError → rc None 으로 남긴다 (반례 먼저 · selftest 가 서지 않게)."""
        try:
            return receipt(**kw)
        except TypeError as e:
            return dict(rc=None, checks=[], error=f'TypeError: {e}')

    def cdet(rec, cid):
        """칸 cid 의 상세 dict — 통과 칸 · 없는 칸 · dict 가 아닌 상세 = {}."""
        for c in rec.get('checks', []):
            if c['id'] == cid:
                return c['detail'] if isinstance(c.get('detail'), dict) else {}
        return {}

    def cdet_raw(rec, cid):
        return next((c.get('detail') for c in rec.get('checks', []) if c['id'] == cid), None)

    def e2_fp(rec):
        """E2 상세의 지문 두 값만 (로그 코드 줄 = git 짧은 sha 를 싣는다 — 실패 사유 출력에 커밋 번호를 남기지 않는다)."""
        return {k: cdet(rec, 'E2').get(k) for k in ('registered', 'receipt')}

    #  ★ 10-15 (나′) 봉인 지문 상태 (1저자 10-15 Q1 (나′)) — 시험은 상태를 먼저 정하고 기대 실패 집합을 그 상태로 정확히 적는다.  도구의 발사 대조 (D1 · E2 · F5 · G5) 는
    #    상태와 무관하게 등록 §3 값만 본다 (대기 선언은 통과시키지 않는다 — 비준 · 재등록 전 발사 불가) · 아래 집합은 시험의 기대일 뿐 도구 동작이 아니다.
    def fp_state(reg_, now):
        """(상태, 사유) — registered = 체크아웃 지문 = 등록 §3 · pending = 대기 선언 하나 · 체크아웃 = 대기 ≠ 등록 · undeclared = 그 밖 (시험 실패 · 사유)."""
        r_, p_ = reg_.get('code_fp'), reg_.get('code_fp_pending')
        if not r_:
            return 'undeclared', ('등록 §3 code_fp 를 못 읽었다 (None — 값이 둘이면 이렇게 된다 · 새 지문을 `code_fp <hex>` 둘째 값으로 적은 옛 초안 꼴 = '
                                  '대기 선언 `code_fp_pending <hex>` 이 아니다)')
        if now is not None and now == r_:
            return 'registered', ''
        if p_ and p_ != r_ and now == p_:
            return 'pending', ''
        return 'undeclared', (f'체크아웃 지문 {str(now)[:12]}… ≠ 등록 §3 {r_[:12]}… · 대기 선언 '
                              + (f'{p_[:12]}… ≠ 체크아웃 (다른 코드)' if p_ else '없음 (읽은 값 None)'))
    #: pending 상태에서 실패해도 되는 칸 = "등록 §3 지문 = 체크아웃 (또는 그 체크아웃이 만든 기록) 지문" 계열만 — 기록 종류별 정확한 집합.
    #:   container = D1 · preflight (진짜 실행기 dry-run 영수증 = 체크아웃 지문을 싣는다) = D1 · E2 · launch (합성 manifest 둘 = code_hashes 가 이 체크아웃 → 봉인 = 체크아웃 지문) =
    #:   D1 · F5 · G5 (H1 = 두 봉인이 같아 같음 · P7 = 영수증 = 체크아웃이라 같음)
    PEND = dict(container={'D1'}, preflight={'D1', 'E2'}, launch={'D1', 'F5', 'G5'})
    spec = NP.COHORT_SPECS[COHORT]
    fp_now = NP.code_fp(NP.code_hashes())
    base = receipt()
    reg = base['registration']['values']
    R_reg, P_reg = reg.get('code_fp'), reg.get('code_fp_pending')
    state, why_state = fp_state(reg, fp_now)

    def pend(kind):
        return set(PEND[kind]) if state == 'pending' else set()

    def fp_why_ok(rec, ids_, r_, p_):
        """지문 계열 실패 칸이 '등록 값 ≠ 체크아웃 지문' 그 이유로 실패했나 — 상세 값 (D1 now · registered · pending / E2 receipt · registered / F5 · G5 봉인 · dirty)."""
        ok_ = True
        if 'D1' in ids_:
            d_ = cdet(rec, 'D1')
            ok_ = ok_ and d_.get('now') == fp_now and d_.get('registered') == r_ and d_.get('pending', 'ABSENT') == p_
        if 'E2' in ids_:
            d_ = cdet(rec, 'E2')
            ok_ = ok_ and d_.get('registered') == r_ and d_.get('receipt') == fp_now
        for g_ in ('F5', 'G5'):
            if g_ in ids_:
                ok_ = ok_ and cdet(rec, g_) == dict(code_fp=fp_now, dirty=False)
        return ok_
    print(f'  (나′) 봉인 지문 상태 = {state} — 체크아웃 {str(fp_now)[:12]}… · 등록 §3 {str(R_reg)[:12]}… · 대기 선언 '
          + (f'{P_reg[:12]}…' if P_reg else '없음') + (f' — {why_state}' if why_state else ''))
    ids0 = {c['id'] for c in base['checks']}
    common0 = (base['scope'] == 'container' and ids0 == {'R0', 'A1', 'A2', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'D1'} and len(base['manual']) == 3
               and not any(m['verified_by_tool'] for m in base['manual']))
    if state == 'registered':
        ok0 = common0 and base['rc'] == 0
    elif state == 'pending':
        ok0 = common0 and base['rc'] == 1 and bad_ids(base) == PEND['container'] and fp_why_ok(base, PEND['container'], R_reg, P_reg)
    else:
        ok0 = False
    chk(f'S0 ★ 10-15 (나′) 정상 (커밋된 실물 · 컨테이너 범위) [상태 {state}] — registered (체크아웃 = 등록 §3) = rc 0 · 대조 칸 R0 · A1 · A2 · B1–B3 · C1–C4 · D1 전부 같음 / '
        'pending (대기 선언 하나 · 체크아웃 = 대기 ≠ 등록) = rc 1 · 실패 칸 정확히 {D1} · D1 상세 now = 대기 · registered = 등록 · pending = 대기 / undeclared = FAIL · '
        '범위 container · 수동 칸 셋', ok0, dict(state=state, why=why_state, bad=sorted(bad_ids(base)), D1=cdet(base, 'D1')))
    dg0 = base['recomputed']['input_digest']
    chk('S0b 다시 계산 = 등록 §2 (케이스 20 · ids 991cf115… · raw a7aaa3c8… · 코호트 TSV 69d3f913…) · 등록 §3 code_fp e8b2496b… · ★ 10-15 (나′) 대기 선언이 있으면 = 1818e3ad… '
        '(★ 10-16 L214R 수정 반영 지문 — 커밋마다 갱신 · 진행 기록 10-16) — 값은 문서 · 반입 파일에서 (도구에 사본 없음 · 값 None 안전)',
        dg0.get('n') == 20 and str(dg0.get('ids_sha256')).startswith('991cf115') and str(dg0.get('raw_sha256_table_sha256')).startswith('a7aaa3c8')
        and str((dg0.get('cohort_tsv_sha256') or {}).get(COHORT)).startswith('69d3f913') and str(R_reg or '').startswith('e8b2496b')
        and (P_reg is None or str(P_reg).startswith('1818e3ad')), (dg0, R_reg, P_reg))
    with tempfile.TemporaryDirectory(prefix='supp20_receipt_') as td:
        td = Path(td)
        rtxt = _rp(REG_DOC).read_text(encoding='utf-8')

        def s3_span(t_):
            """시험 쪽 §3 자리 (도구 파서와 따로 — 맨 '## 3.' 제목 줄부터 다음 '## ' 제목 앞까지) → (시작, 끝) · 없으면 (None, None)."""
            i3_ = t_.find('\n## 3.')
            if i3_ < 0:
                return None, None
            i4_ = t_.find('\n## ', i3_ + 1)
            return i3_, (i4_ if i4_ >= 0 else len(t_))

        def reg_variant(name, registered, pending=(), old_second=None, old_second_at='s3'):
            """★ 10-15 (나′) 등록 문서 사본 — 지문 토큰만 바꾼다 (다른 칸은 실물 그대로 · 실물이 옛 초안 꼴이든 대기 선언 꼴이든 같은 결과):
            모든 `code_fp <hex>` → `code_fp <registered>` · 있던 대기 선언 `code_fp_pending <hex>` → 맨 hex (선언 아님) · pending 값마다 대기 선언 한 줄 ·
            old_second = 옛 초안 꼴 둘째 값 (`code_fp <hex>`) 한 줄 — ★ 10-16 L214R-04: 파서가 활성 §3 만 읽으므로 자리를 고른다 ('s3' = §3 끝 · 'end' = 문서 끝 = §3 밖)."""
            t_ = re.sub(r'`code_fp ([0-9a-f]{64})`', f'`code_fp {registered}`', rtxt)
            t_ = re.sub(r'`code_fp_pending ([0-9a-f]{64})`', r'`\1`', t_)
            for v_ in pending:
                t_ += f'\n| 대기 지문 (selftest 사본) | `code_fp_pending {v_}` |\n'
            if old_second and old_second_at == 's3':
                _i3, _i4 = s3_span(t_)
                line_ = f'\n- 개정 초안 (옛 꼴 · selftest 사본 · §3 안): `code_fp {old_second}`\n'
                t_ = (t_[:_i4] + line_ + t_[_i4:]) if _i3 is not None else (t_ + line_)
            elif old_second:
                t_ += f'\n| 개정 초안 (옛 꼴 · selftest 사본 · §3 밖) | `code_fp {old_second}` |\n'
            p_ = td / f'reg_fp_{name}.md'
            p_.write_text(t_, encoding='utf-8')
            return str(p_)

        def reg_ratify(name, new_fp):
            """★ 10-16 L214R-04 — Codex 변이 minimal_activate_section3 그대로 (판정문 §5 · 등록 문서가 안내한 비준 단계): 대기 선언 삭제 · 활성 §3 의
            `code_fp <hex>` 만 new_fp 로 · 역사 표 (같은 기계 구문 옛 값) 는 그대로.  → (경로, 정보 — §3 안 토큰을 바꿨나 · §3 밖 역사 토큰 (new_fp 와 다른 값) ·
            합성 역사 행을 붙였나).  실물에 그런 역사 토큰이 없으면 (미래 판) 같은 기계 구문의 역사 행 하나를 붙여 조건을 늘 시험한다."""
            t_ = re.sub(r'`code_fp_pending [0-9a-f]{64}`', '(대기 선언 삭제 — selftest 비준 전환 사본)', rtxt)
            _i3, _i4 = s3_span(t_)
            m_ = re.search(r'`code_fp ([0-9a-f]{64})`', t_[_i3:_i4]) if _i3 is not None else None
            if m_:
                a_ = _i3 + m_.start()
                t_ = t_[:a_] + f'`code_fp {new_fp}`' + t_[a_ + len(m_.group(0)):]
                _i3, _i4 = s3_span(t_)
            hist_ = sorted({v for v in re.findall(r'`code_fp ([0-9a-f]{64})`', t_[:_i3] + t_[_i4:]) if v != new_fp}) if _i3 is not None else []
            synth_ = not hist_
            if synth_:
                t_ += f'\n| §3 코드 신원 (selftest 역사 사본 · 원문 보존) | `code_fp {R_SIM}` |\n'
                hist_ = [R_SIM]
            p_ = td / f'reg_ratify_{name}.md'
            p_.write_text(t_, encoding='utf-8')
            return str(p_), dict(in_s3=bool(m_), old=(m_.group(1) if m_ else None), history=hist_, synthetic_history=synth_,
                                 pending_left=bool(re.search(r'`code_fp_pending [0-9a-f]{64}`', t_)))
        #  ⓕ 비준 쌍둥이 — 등록 §3 := 체크아웃 지문 · 대기 선언 없음 (비준 · 재등록 뒤의 꼴).  판별 문서 DISC = 상태 registered 면 실물 · 아니면 이 쌍둥이 —
        #  pending 에서는 D1 · E2 · F5 · G5 가 이미 실패라, 그 칸을 겨눈 음성 대조 (S7l · S8e · S8f) 를 이미 실패 중인 칸으로 통과시키지 않으려고 쌍둥이에서 판별한다
        #  (쌍둥이의 정상 기록 = rc 0 · S11f · S11f2 · S11f3).
        TWIN = reg_variant('twin', registered=fp_now)
        DISC = REG_DOC if state == 'registered' else TWIN
        disc_lbl = '실물' if DISC == REG_DOC else '비준 쌍둥이 ⓕ'

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
        for k, ids in (('raw_sha256_table_sha256', {'B3'}), ('ids_sha256', {'A1', 'B3'}), ('cohort_tsv_sha256', {'B3'}), ('code_fp', {'D1'})):
            v = reg.get(k)
            if not v:
                chk(f'S4 등록 문서 {k} 오타 (끝 한 글자)', False, f'등록 문서 {k} 값을 못 읽어 (None · 상태 {state}) 오타 반례를 만들 수 없다')
                continue
            bad_v = v[:-1] + ('0' if v[-1] != '0' else '1')
            p = td / f'reg_{k}.md'
            p.write_text(rtxt.replace(v, bad_v), encoding='utf-8')
            r4 = receipt(reg_doc=str(p))
            if k != 'code_fp':
                expect(f'S4 등록 문서 {k} 오타 (끝 한 글자)', r4, ids)
                continue
            d4 = cdet(r4, 'D1')
            chk(f"S4 등록 문서 code_fp 오타 (끝 한 글자) → rc 1 · 실패 칸 ⊇ ['D1'] · ★ 10-15 (나′) D1 상세 registered = 문서에서 읽은 오타 값 · now = 체크아웃 [상태 {state}] "
                '(pending 에서는 D1 이 이미 실패라 값까지 본다 — 이미 실패 중인 칸으로 통과시키지 않는다)',
                r4.get('rc') == 1 and 'D1' in bad_ids(r4) and d4.get('registered') == bad_v and d4.get('now') == fp_now, (sorted(bad_ids(r4)), d4))
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
        #  ⑦ ★ 10-14 SUPR-01 · SUPR-02 (Codex 보충 20 수정 재검증 §4 · §5 · 1저자 Q1 · Q2 · Q3 (가)) — 발사 사전 점검 증거 = 실행기 완료 영수증 JSON + 그 실행기가 잡은 전체 로그.
        #    반례 먼저 (판정문 §4 최소 해결 ③ · §5 ④ · 계획 §3 ①): 진짜 실행기 dry-run (NP.main — build_plan · plan_input_digest · print_preflight · 완료 영수증) 을 이 체크아웃에서
        #    돌린다.  대역 = git_info (깨끗한 트리 · 이 체크아웃 HEAD) · raw_problems (원 dump 는 WSL 에만) · _guard_posix (윈도 검토 환경) 셋 + 한 번 잰 진짜 값의 재사용
        #    (derive_generation · code_dependency_closure · lazy_import_census — 시간만 줄인다).  봉인 32 · 계획 · 입력 지문 · 화면 · 영수증 · 종료코드는 진짜다.
        #    옛 판 = 텍스트 로그 (tee · grep) 를 읽어 다른 TSV 로 돈 로그 · 중단 사유 앞에서 잘린 로그 · 필수 줄 셋이 빠진 로그가 rc 0 (Codex 반례 로그 다섯 = ⑩).
        plan = plan_for()
        IDL = getattr(NP, 'INPUT_DIGEST_LINE', 'INPUT_DIGEST_JSON')
        MARK = getattr(NP, 'PREFLIGHT_COMPLETE_MARK', 'PREFLIGHT_DRY_RUN_COMPLETE rc 0')
        TICKS = ('전이 의존 닫힘', '지연 import 분류', 'fork · 프로세스 풀 API')            # 화면의 필수 세 검사 줄 (실행기 print_preflight)
        GREP = ('코드 ', '기대 망 세대', '전이 의존', '지연 import', 'fork', '입력 지문', '원자료 · 메시 문제', '⛔')   # 등록 §4 의 옛 grep -E 그대로
        g_now = NP.git_info()
        sha_now = g_now['sha'] if re.fullmatch(r'[0-9a-f]{40}', str(g_now.get('sha') or '')) else 'ab' * 20

        def git_clean(*_a, **_k):
            return dict(sha=sha_now, short=sha_now[:9], branch='HEAD', dirty=False, porcelain=[])

        def git_dirty(*_a, **_k):
            return dict(sha=sha_now, short=sha_now[:9], branch='HEAD', dirty=True, porcelain=[' M scripts/se_material.py'])
        cache = dict(gen=NP.derive_generation(NP.ROOT), clo=NP.code_dependency_closure(), lazy=NP.lazy_import_census())

        @contextlib.contextmanager
        def np_patch(**kw):
            old = {k: getattr(NP, k) for k in kw}
            for k, v in kw.items():
                setattr(NP, k, v)
            try:
                yield
            finally:
                for k, v in old.items():
                    setattr(NP, k, v)
        (td / 'pf').mkdir()
        (td / 'screens').mkdir()

        def npdry(tag, *extra, observe=True, receipt_on=True, cohort_path=None, harvest_path=None, git=None, raw=None):
            """진짜 실행기 `run --root R --cohorts lhss --dry-run (--observe-imports) (--preflight-receipt P)` → (rc, P, 화면 파일).  화면 = 사용자가 tee 로 받는 것."""
            R_, P_ = td / f'root_{tag}', td / 'pf' / f'{tag}_preflight.json'
            argv = ['run', '--root', str(R_), '--cohorts', COHORT, '--dry-run', *(['--observe-imports'] if observe else []),
                    *(['--preflight-receipt', str(P_)] if receipt_on else []), *extra]
            sp_ = dict(spec, **({'cohort': str(cohort_path)} if cohort_path else {}), **({'harvest': str(harvest_path)} if harvest_path else {}))
            buf = io.StringIO()
            with np_patch(git_info=git or git_clean, raw_problems=raw or (lambda *a, **k: []), _guard_posix=lambda: None,
                          derive_generation=lambda *a, **k: dict(cache['gen']), code_dependency_closure=lambda *a, **k: dict(cache['clo']),
                          lazy_import_census=lambda *a, **k: dict(cache['lazy']), COHORT_SPECS=dict(NP.COHORT_SPECS, **{COHORT: sp_})):
                with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                    try:
                        rc_ = NP.main(argv)
                    except SystemExit as e:
                        rc_ = e.code if isinstance(e.code, int) else 2
            scr = td / 'screens' / f'{tag}.log'
            scr.write_bytes(buf.getvalue().encode('utf-8'))
            return rc_, str(P_), str(scr)

        def rlog(p):
            """영수증 JSON · 그 로그 글 (없거나 못 읽으면 {} · '')."""
            try:
                r_ = json.loads(Path(p).read_text(encoding='utf-8'))
                return r_, Path(r_['log']['path']).read_bytes().decode('utf-8')
            except (OSError, ValueError, KeyError, TypeError):
                return {}, ''
        n_forge = [0]

        def forge(src, tag, edit_log=None, edit_rec=None, resha=True, log_text=None):
            """영수증 사본 — 로그 고침 (edit_log · 또는 log_text 통째) · JSON 고침 (edit_rec) · resha = 로그 sha256 · 바이트를 고친 로그에 맞춰 다시 적는다
            (영수증까지 함께 위조해도 내용 대조가 따로 잡는가).  원본이 없으면 (옛 판) 없는 경로를 돌려준다."""
            n_forge[0] += 1
            r_, t_ = rlog(src)
            d_ = td / 'forge' / f'{n_forge[0]:02d}_{tag}'
            if not r_:
                return str(d_ / 'missing_preflight.json')
            t_ = log_text if log_text is not None else (edit_log(t_) if edit_log else t_)
            d_.mkdir(parents=True)
            lp_ = d_ / Path(r_['log']['path']).name
            lp_.write_bytes(t_.encode('utf-8'))
            r_['log']['path'] = str(lp_)
            if resha:
                r_['log'].update(sha256=hashlib.sha256(t_.encode('utf-8')).hexdigest(), bytes=len(t_.encode('utf-8')))
            if edit_rec:
                edit_rec(r_)
            rp_ = d_ / Path(src).name
            rp_.write_text(json.dumps(r_, ensure_ascii=False), encoding='utf-8')
            return str(rp_)

        def drop_ticks(t):
            return '\n'.join(ln for ln in t.split('\n') if not ln.strip().startswith(TICKS))

        def cut_before(t, pred):
            ls = t.split('\n')
            i_ = next((k for k, ln in enumerate(ls) if pred(ln)), len(ls))
            return '\n'.join(ls[:i_]) + ('\n' if i_ else '')

        def grep_reg(t):
            return '\n'.join(ln for ln in t.split('\n') if any(k in ln for k in GREP))

        def text_file(name, text):
            p_ = td / 'screens' / name
            p_.write_bytes(text.encode('utf-8'))
            return str(p_)

        def is_mark(ln):
            return ln.strip() == MARK

        #  (i) 정상 — 등록 명령 그대로
        rc_p, P_pos, S_pos = npdry('pos')
        r_pos = rsafe(preflight_receipt=P_pos)
        w_pf = pend('preflight')
        chk('S7 ★ (i) 정상 — 진짜 실행기 dry-run (등록 명령 run --cohorts lhss --dry-run --observe-imports --preflight-receipt) rc 0 → 영수증 JSON + 전체 로그 → rc 0 · '
            '범위 preflight · P0–P9 (실행기 대조) · E1 (로그 INPUT_DIGEST_JSON = 등록 §2 = 반입 재계산) · E2 (봉인 지문 = 등록 §3) 같음 · 승인 SHA 없음 = 경고 기록 (실패 아님) · '
            f'★ 10-15 (나′) [상태 {state}] pending = rc 1 · 실패 칸 정확히 {{D1 · E2}} (영수증 = 체크아웃 지문 · 상세 = 등록 §3 ≠ 체크아웃)',
            rc_p == 0 and r_pos.get('rc') == (1 if w_pf else 0) and bad_ids(r_pos) == w_pf and fp_why_ok(r_pos, w_pf, R_reg, P_reg) and r_pos.get('scope') == 'preflight'
            and {f'P{i}' for i in range(10)} | {'E1', 'E2'} <= {c['id'] for c in r_pos.get('checks', [])} and 'approved_sha' in (r_pos.get('notes') or {}),
            (rc_p, sorted(bad_ids(r_pos)), r_pos.get('error'), e2_fp(r_pos)))
        rp_pos, lt_pos = rlog(P_pos)
        chk('S7u 영수증 종료코드 = 실행기 CLI 종료코드 (정상 0 — 셸 tee · grep 종료코드가 아니다) · 영수증 로그 = 실행기 화면 (영수증 안내 줄 앞까지 같은 바이트)',
            rp_pos.get('exit_code') == rc_p == 0 and bool(lt_pos) and Path(S_pos).read_bytes().decode('utf-8').startswith(lt_pos), (rp_pos.get('exit_code'), rc_p))
        #  (a) SUPR-01 — 같은 20 ID · raw 표 · 코호트 TSV 첫 행 deck_sha256 한 글자만 다름 (실제 build_plan · plan_input_digest · print_preflight)
        tsv_a = td / 'cohort_deck1.tsv'
        ls_a = _rp(spec['cohort']).read_bytes().decode('utf-8').split('\n')
        h_a = next(k for k, ln in enumerate(ls_a) if ln.startswith('case\t'))
        cells_a = ls_a[h_a + 1].split('\t')
        col_a = ls_a[h_a].split('\t').index('deck_sha256')
        cells_a[col_a] = ('0' if cells_a[col_a][0] != '0' else '1') + cells_a[col_a][1:]
        ls_a[h_a + 1] = '\t'.join(cells_a)
        tsv_a.write_bytes('\n'.join(ls_a).encode('utf-8'))
        rc_a, P_a, _s = npdry('tsv1', cohort_path=tsv_a)
        r_a = rsafe(preflight_receipt=P_a)
        _ra, lt_a = rlog(P_a)
        dl_a = [ln.strip() for ln in lt_a.split('\n') if ln.strip().startswith(IDL + ' ')]
        try:
            lg_a = json.loads(dl_a[0][len(IDL):]) if len(dl_a) == 1 else {}
        except ValueError:
            lg_a = {}
        chk('S7a ★ (a) SUPR-01 — 같은 20 ID · raw 표 · 코호트 TSV 첫 행 deck_sha256 한 글자만 바꾼 파일로 돈 진짜 dry-run (실행기 rc 0 · 새 꼴 로그가 그 TSV sha 를 싣는다) → '
            '값으로 거부: 실패 칸 = E1 (로그 = 등록 §2 = 반입 재계산) · P9 (영수증 지문 = 이 체크아웃 재계산) 둘뿐 · 부재가 아니라 값 · '
            f'★ (나′) [상태 {state}] pending 이면 + D1 · E2 (정확히)',
            rc_a == 0 and r_a.get('rc') == 1 and bad_ids(r_a) == {'E1', 'P9'} | w_pf and fp_why_ok(r_a, w_pf, R_reg, P_reg)
            and (lg_a.get('cohort_tsv_sha256') or {}).get(COHORT) == _sha(tsv_a) != reg.get('cohort_tsv_sha256')
            and lg_a.get('raw_sha256_table_sha256') == reg.get('raw_sha256_table_sha256') and lg_a.get('ids_sha256') == reg.get('ids_sha256'),
            (rc_a, sorted(bad_ids(r_a)), lg_a.get('cohort_tsv_sha256'), r_a.get('error')))
        rc_at, _p, S_at = npdry('tsv1_txt', cohort_path=tsv_a, receipt_on=False)
        r_at = rsafe(dry_run_log=S_at)
        chk('S7a-t (a) 같은 반례의 텍스트 화면 (tee) 을 --dry-run-log 로 → rc 1 (옛 판 = rc 0 오수용 · 판정문 §4 검산)', rc_at == 0 and r_at.get('rc') == 1,
            (rc_at, r_at.get('rc'), sorted(bad_ids(r_at))))
        ALT = REPO / 'docs/reviews/codex_sup20_fix_reverify_evidence_20261014/evidence/receipt_extra/alternate_cohort.tsv'
        rc_a2, P_a2, _s = npdry('tsv2', cohort_path=ALT)
        r_a2 = rsafe(preflight_receipt=P_a2)
        chk('S7a2 (a) Codex 반례 TSV 그대로 (evidence/receipt_extra/alternate_cohort.tsv · sha256 8d5dcbd2… = 판정문 §4 변이값) → 값으로 거부 (실패 칸 = E1 · P9 둘뿐 · '
            f'★ (나′) [상태 {state}] pending 이면 + D1 · E2 · 정확히)',
            ALT.is_file() and str(_sha(ALT)).startswith('8d5dcbd2') and rc_a2 == 0 and bad_ids(r_a2) == {'E1', 'P9'} | w_pf and fp_why_ok(r_a2, w_pf, R_reg, P_reg),
            (rc_a2, sorted(bad_ids(r_a2)), r_a2.get('error')))
        #  (b) SUPR-02 — 관측 OFF (등록 생산 계획 · --observe-imports 없이) = 실행기 사전 점검 ⛔ · 멈춰도 영수증
        rc_b, P_b, _s = npdry('off', observe=False)
        r_b = rsafe(preflight_receipt=P_b)
        rb_, lt_b = rlog(P_b)
        chk('S7b ★ (b) SUPR-02 관측 OFF — 실행기 ⛔ rc 2 · 멈춰도 영수증 (completed false · 실제 종료코드 2 · 멈춘 사유) → 거부 (P3 완료 · P4 관측 ⊆ 실패 칸)',
            rc_b == 2 and rb_.get('exit_code') == 2 and rb_.get('completed') is False and bool(rb_.get('stop')) and '⛔' in lt_b
            and r_b.get('rc') == 1 and {'P3', 'P4'} <= bad_ids(r_b), (rc_b, rb_.get('exit_code'), sorted(bad_ids(r_b)), r_b.get('error')))
        rc_bt, _p, S_bt = npdry('off_txt', observe=False, receipt_on=False)
        chk('S7b-t (b) 관측 OFF 전체 화면을 --dry-run-log 로 → rc 1 (옛 판도 rc 1 — 판정문 §5 대조)', rc_bt == 2 and rsafe(dry_run_log=S_bt).get('rc') == 1, rc_bt)
        #  (c) 같은 OFF 로그를 첫 ⛔ 앞에서 자름
        def is_stop(ln):
            return '⛔' in ln
        expect('S7c1 (c) 관측 OFF 로그를 첫 ⛔ 앞에서 자름 (영수증 그대로 — sha · 바이트 다름)',
               rsafe(preflight_receipt=forge(P_b, 'c1', edit_log=lambda t: cut_before(t, is_stop), resha=False)), {'P1'})

        def flip_ok(r_):
            r_.update(completed=True, exit_code=0, stop=[], completion_marker=MARK, observe_imports=True)
        expect('S7c2 (c) 같은 잘린 로그 + 영수증 위조 (sha · 바이트 맞춤 · 완료 · 종료 0 · 관측 true 로 바꿈) → 내용으로 거부 (완료 표지 없음 P3 · argv 에 관측 없음 P4)',
               rsafe(preflight_receipt=forge(P_b, 'c2', edit_log=lambda t: cut_before(t, is_stop), edit_rec=flip_ok)), {'P3', 'P4'})
        r_ct = rsafe(dry_run_log=text_file('off_cut.log', cut_before(Path(S_bt).read_bytes().decode('utf-8'), is_stop)))
        chk('S7c-t (c) 관측 OFF 화면을 ⛔ 앞에서 자른 텍스트 → rc 1 (옛 판 = rc 0 오수용 · 판정문 §5 표 셋째 줄)', r_ct.get('rc') == 1, sorted(bad_ids(r_ct)))
        #  (d) 정상 로그에서 필수 세 줄 삭제
        expect('S7d1 (d) 정상 로그에서 전이 의존 · 지연 import · fork 줄 셋 삭제 (영수증 그대로)',
               rsafe(preflight_receipt=forge(P_pos, 'd1', edit_log=drop_ticks, resha=False)), {'P1'})
        expect('S7d2 (d) 같은 삭제 + 영수증 sha · 바이트 맞춤 → 내용으로 거부 (필수 세 줄 없음 P5)', rsafe(preflight_receipt=forge(P_pos, 'd2', edit_log=drop_ticks)), {'P5'})
        rc_pt, _p, S_pt = npdry('pos_txt', receipt_on=False)
        txt_pt = Path(S_pt).read_bytes().decode('utf-8')
        r_dt = rsafe(dry_run_log=text_file('pos_drop.log', drop_ticks(txt_pt)))
        chk('S7d-t (d) 정상 화면에서 세 줄 삭제한 텍스트 → rc 1 (옛 판 = rc 0 오수용 · 판정문 §5 표 넷째 줄)', rc_pt == 0 and r_dt.get('rc') == 1, (rc_pt, sorted(bad_ids(r_dt))))
        #  (e) 등록 §4 옛 grep 으로 거른 로그
        expect('S7e1 (e) 등록 §4 옛 grep 으로 거른 로그를 전체 로그 자리에 (영수증 그대로)', rsafe(preflight_receipt=forge(P_pos, 'e1', edit_log=grep_reg, resha=False)), {'P1'})
        expect('S7e2 (e) 같은 grep 로그 + 영수증 sha 맞춤 → 내용으로 거부 (INPUT_DIGEST_JSON 없음 P2 · 완료 표지 없음 P3)',
               rsafe(preflight_receipt=forge(P_pos, 'e2', edit_log=grep_reg)), {'P2', 'P3'})
        r_et = rsafe(dry_run_log=text_file('pos_grep.log', grep_reg(txt_pt)))
        chk('S7e-t (e) grep 로그 단독 (--dry-run-log) → rc 1 · 사유 E0 (텍스트 로그 단독은 증거 아님 — 옛 판 = rc 0 · 옛 S7b 가 통과로 적었던 꼴)',
            r_et.get('rc') == 1 and 'E0' in bad_ids(r_et), sorted(bad_ids(r_et)))
        #  (f) 정상 로그를 완료 표지 앞에서 자름
        expect('S7f1 (f) 정상 로그를 완료 표지 앞에서 자름 (영수증 그대로)', rsafe(preflight_receipt=forge(P_pos, 'f1', edit_log=lambda t: cut_before(t, is_mark), resha=False)),
               {'P1'})
        expect('S7f2 (f) 같은 자름 + 영수증 sha 맞춤 → 내용으로 거부 (완료 표지 없음 P3)', rsafe(preflight_receipt=forge(P_pos, 'f2', edit_log=lambda t: cut_before(t, is_mark))),
               {'P3'})
        r_ft = rsafe(dry_run_log=text_file('pos_cut.log', cut_before(txt_pt, lambda ln: ln.strip().startswith('══ --dry-run') or is_mark(ln))))
        chk('S7f-t (f) 정상 화면을 dry-run 끝 줄 앞에서 자른 텍스트 → rc 1 (옛 판 = rc 0 — 완료를 보지 않았다)', r_ft.get('rc') == 1, sorted(bad_ids(r_ft)))
        #  (g) 영수증 JSON 값 — 종료코드 · 완료 · 관측 · 필수 검사 · schema
        for nm, ed, ids in (('exit_code 2', lambda r_: r_.update(exit_code=2), {'P3'}), ('exit_code true (bool)', lambda r_: r_.update(exit_code=True), {'P3'}),
                            ('completed false', lambda r_: r_.update(completed=False), {'P3'}),
                            ('observe_imports false', lambda r_: r_.update(observe_imports=False), {'P4'}),
                            ('observe_imports 키 없음', lambda r_: r_.pop('observe_imports', None), {'P4'}),
                            ('필수 검사 fork_census 없음', lambda r_: (r_.get('checks') or {}).pop('fork_census', None), {'P5'}),
                            ('필수 검사 지연 import ok = "true" (문자열)', lambda r_: ((r_.get('checks') or {}).get('lazy_import_census') or {}).update(ok='true'), {'P5'}),
                            ('schema 다름', lambda r_: r_.update(schema='np194_preflight_receipt/v0'), {'P0'})):
            expect(f'S7g (g) 영수증 JSON {nm} (로그 그대로)', rsafe(preflight_receipt=forge(P_pos, 'g', edit_rec=ed)), ids)
        #  (h) 로그 sha 불일치 · 영수증 없음
        expect('S7h (h) 로그 끝에 한 바이트 (영수증 그대로 — sha · 바이트 다름)', rsafe(preflight_receipt=forge(P_pos, 'h', edit_log=lambda t: t + ' ', resha=False)), {'P1'})
        expect('S7h2 영수증 JSON 자체가 없다', rsafe(preflight_receipt=str(td / 'pf' / 'nope_preflight.json')), {'P0'})
        #  Q3 — 승인 SHA (접두 7–40 · 부재 = 경고)
        r_j1 = rsafe(preflight_receipt=P_pos, approved_sha=sha_now[:7])
        chk('S7j ★ Q3 승인 SHA (접두 7) = 사전 점검 git 기록 · 로그 코드 줄 짧은 sha → rc 0 · P10 같음 · 경고 없음 · '
            f'★ (나′) [상태 {state}] pending = rc 1 · 실패 칸 정확히 {{D1 · E2}} (P10 은 같음)',
            r_j1.get('rc') == (1 if w_pf else 0) and bad_ids(r_j1) == w_pf and fp_why_ok(r_j1, w_pf, R_reg, P_reg)
            and 'P10' in {c['id'] for c in r_j1.get('checks', [])} and 'approved_sha' not in (r_j1.get('notes') or {}),
            (sorted(bad_ids(r_j1)), r_j1.get('error')))
        expect('S7j2 Q3 다른 승인 SHA', rsafe(preflight_receipt=P_pos, approved_sha=('0' if sha_now[0] != '0' else '1') + sha_now[1:7]), {'P10'})
        expect('S7j3 Q3 승인 SHA 꼴 (16 진 아님)', rsafe(preflight_receipt=P_pos, approved_sha='xyz1234'), {'P10'})
        #  등록 명령 밖 인자 (argv = 등록 명령)
        rc_k1, P_k1, _s = npdry('k_raw', '--allow-missing-raw')
        r_k1 = rsafe(preflight_receipt=P_k1)
        chk(f'S7k1 등록 명령 밖 인자 --allow-missing-raw (dry-run 은 끝까지 rc 0) → 실패 칸 = P6 (argv) 하나 (★ (나′) [상태 {state}] pending 이면 + D1 · E2 · 정확히)',
            rc_k1 == 0 and r_k1.get('rc') == 1 and bad_ids(r_k1) == {'P6'} | w_pf and fp_why_ok(r_k1, w_pf, R_reg, P_reg),
            (rc_k1, sorted(bad_ids(r_k1)), r_k1.get('error')))
        rc_k2, P_k2, _s = npdry('k_cohort', f'--{COHORT}-cohort', str(_rp(spec['cohort'])))
        r_k2 = rsafe(preflight_receipt=P_k2)
        chk('S7k2 --lhss-cohort 로 같은 경로를 덮어씀 (지문 같음) → 실패 칸 = P6 하나 (경로 덮어쓰기는 등록 명령이 아니다 — 지문 대조와 따로 · '
            f'★ (나′) [상태 {state}] pending 이면 + D1 · E2 · 정확히)',
            rc_k2 == 0 and r_k2.get('rc') == 1 and bad_ids(r_k2) == {'P6'} | w_pf and fp_why_ok(r_k2, w_pf, R_reg, P_reg), (rc_k2, sorted(bad_ids(r_k2)), r_k2.get('error')))
        rc_k3, P_k3, _s = npdry('k_case', '--case', 'lhss_001')
        expect('S7k3 --case lhss_001 (한 케이스 · 일반 계획)', rsafe(preflight_receipt=P_k3), {'P6', 'P9', 'E1'})
        #  코드 신원 · 트리 · 입력 · 세대 · 원자료
        fp_real = NP.code_fp(NP.code_hashes())
        expect(f'S7l 봉인 지문 다른 로그 + 영수증 (sha 맞춤) — ★ (나′) 판별 문서 = {disc_lbl} (상태 {state} · pending 에서는 E2 가 이미 실패라 쌍둥이에서 판별)',
               rsafe(preflight_receipt=forge(P_pos, 'l', edit_log=lambda t: t.replace(fp_real, 'e' * 64), edit_rec=lambda r_: r_.update(code_fp='e' * 64)),
                     reg_doc=DISC), {'P7', 'E2'})
        rc_m, P_m, _s = npdry('dirty', git=git_dirty)
        expect('S7m 추적 파일이 바뀐 트리 (--allow-dirty 없음 · 실행기 ⛔ rc 2)', rsafe(preflight_receipt=P_m), {'P3', 'P7'})
        rc_m2, P_m2, _s = npdry('dirty_ok', '--allow-dirty', git=git_dirty)
        expect('S7m2 같은 트리 + --allow-dirty (dry-run 은 끝까지)', rsafe(preflight_receipt=P_m2), {'P6', 'P7'})

        def _raw7(d):
            j = json.loads((d / 'lhss_007.json').read_text(encoding='utf-8'))
            j['raw']['atom']['sha256'] = 'f' * 64
            (d / 'lhss_007.json').write_text(json.dumps(j), encoding='utf-8')
        rc_n, P_n, _s = npdry('rawtab', harvest_path=hcopy('h_raw_pf', _raw7))
        expect('S7n 수확 JSON raw sha 하나 다른 수확 폴더로 돈 dry-run (같은 20 ID · 실행기 rc 0)', rsafe(preflight_receipt=P_n), {'E1', 'P9'})
        rc_o, P_o, _s = npdry('gen21', harvest_path=hcopy('h21_pf', lambda d: shutil.copy2(d / 'lhss_020.json', d / 'lhst_045_6m.json')))
        expect('S7o 수확 폴더에 후막 하나 더 (21 · 일반 계획 · 실행기 rc 0)', rsafe(preflight_receipt=P_o), {'E1', 'P9'})
        expect('S7p 기대 망 세대 None (로그 · 영수증 함께 · sha 맞춤)',
               rsafe(preflight_receipt=forge(P_pos, 'p', edit_log=lambda t: t.replace("): 'g2' · 세대 계약 문제", "): None · 세대 계약 문제"),
                                             edit_rec=lambda r_: (r_.get('generation') or {}).update(generation=None))), {'P8'})
        rc_q, P_q, _s = npdry('rawprob', raw=lambda *a, **k: [('lhss_001', 'atom 파일 없음: /x/atom.liggghts')])
        expect('S7q 원자료 · 메시 문제 1 건 (실행기 ⛔ rc 2)', rsafe(preflight_receipt=P_q), {'P3', 'P8'})

        def dup_digest(t):
            out_ = []
            for ln in t.split('\n'):
                out_.append(ln)
                if ln.strip().startswith(IDL + ' '):
                    out_.append(ln)
            return '\n'.join(out_)
        expect('S7r INPUT_DIGEST_JSON 줄이 둘 (같은 값 · sha 맞춤)', rsafe(preflight_receipt=forge(P_pos, 'r', edit_log=dup_digest)), {'P2', 'E1'})
        expect('S7s INPUT_DIGEST_JSON 값이 JSON 아님 (sha 맞춤)',
               rsafe(preflight_receipt=forge(P_pos, 's', edit_log=lambda t: re.sub(r'(?m)^(\s*' + re.escape(IDL) + r' ).*$', r'\1{broken', t))), {'P2', 'E1'})

        def drop_tsv_key(t):
            out_ = []
            for ln in t.split('\n'):
                if ln.strip().startswith(IDL + ' '):
                    d_ = json.loads(ln.strip()[len(IDL):])
                    d_.pop('cohort_tsv_sha256', None)
                    ln = ln[:ln.index(IDL)] + IDL + ' ' + json.dumps(d_, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
                out_.append(ln)
            return '\n'.join(out_)
        expect('S7s2 INPUT_DIGEST_JSON 에 코호트 TSV 키 없음 (로그 · 영수증 함께 · sha 맞춤)',
               rsafe(preflight_receipt=forge(P_pos, 's2', edit_log=drop_tsv_key, edit_rec=lambda r_: (r_.get('input_digest') or {}).pop('cohort_tsv_sha256', None))),
               {'P2', 'E1', 'P9'})
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
        ms0 = man(plan, dg0, 'rootS')
        rm = receipt(manifest=ms0, primary_manifest=mp194)
        w_l = pend('launch')
        chk('S8 실제 발사 manifest 둘 (보충 · 194 · 다른 ROOT · 같은 발사 커밋 · 관측 ON) → rc 0 · 범위 launch · F0–F6 · G0–G2 · G4 · G5 · H1 같음 · '
            f'★ (나′) [상태 {state}] pending = rc 1 · 실패 칸 정확히 {{D1 · F5 · G5}} (합성 manifest 둘의 봉인 = 이 체크아웃 지문 · H1 = 두 봉인이 같아 같음)',
            rm['rc'] == (1 if w_l else 0) and bad_ids(rm) == w_l and fp_why_ok(rm, w_l, R_reg, P_reg) and rm['scope'] == 'launch'
            and {'F1', 'F3', 'F4', 'F6', 'G1', 'G2', 'H1'} <= {c['id'] for c in rm['checks']}, sorted(bad_ids(rm)))
        expect('S8b 보충 manifest 관측 끔 (observe_imports false)', receipt(manifest=man(plan, dg0, 'rS_obs', observe_imports=False)), {'F4'})
        expect('S8c 보충 manifest input_digest raw sha 표 다름', receipt(manifest=man(plan, dict(dg0, raw_sha256_table_sha256='2' * 64), 'rS_dg')), {'F3'})
        p21 = plan_for(harvest=hcopy('h_thick2', lambda d: shutil.copy2(d / 'lhss_020.json', d / 'lhst_045_6m.json')))
        expect('S8d 보충 manifest 계획 = 일반 계획 (후막 하나 더 · 21)', receipt(manifest=man(p21, NP.plan_input_digest(p21), 'rS_gen')), {'F2', 'F3'})
        expect(f'S8e 보충 manifest git.dirty true — ★ (나′) 판별 문서 = {disc_lbl} (pending 에서는 F5 가 이미 실패라 쌍둥이에서 판별)',
               receipt(manifest=man(plan, dg0, 'rS_dirty', git=dict(sha='ab' * 20, short='abababab', dirty=True)), reg_doc=DISC), {'F5'})

        def _other_fp(m):
            h = dict(m['code_hashes'], **{NP.CODE_FILES[0]: '0' * 64})
            return h
        mo = man(plan, dg0, 'rS_fp', code_hashes=_other_fp)
        mj = json.loads(Path(mo).read_text(encoding='utf-8'))
        mj['seal']['code_fp'] = NP.code_fp(mj['code_hashes'])                       # 봉인이 자기 해시 지도와는 맞다 (자격 current) · 등록 §3 과 다르다
        Path(mo).write_text(json.dumps(mj), encoding='utf-8')
        expect(f'S8f 보충 manifest 발사 봉인 지문 ≠ 등록 §3 (자기 해시 지도와는 일관) — ★ (나′) 판별 문서 = {disc_lbl} (pending 에서는 F5 가 이미 실패라 쌍둥이에서 판별)',
               receipt(manifest=mo, reg_doc=DISC), {'F5'})
        rsame = receipt(manifest=man(plan, dg0, 'root194', fname='manifest_supp.json'), primary_manifest=mp194)
        expect('S8g 보충 · 194 manifest 가 같은 ROOT 폴더 (나머지 칸은 정상)', rsame, {'H1'})
        chk(f'S8g2 같은 반례 — 실패 칸은 H1 하나 (보충 · 194 manifest 각자는 정상 · ★ (나′) [상태 {state}] pending 이면 + D1 · F5 · G5 · 정확히)',
            bad_ids(rsame) == {'H1'} | w_l and fp_why_ok(rsame, w_l, R_reg, P_reg), sorted(bad_ids(rsame)))
        expect('S8h 194 자리에 보충 manifest (등록 집합 production194 아님)', receipt(manifest=man(plan, dg0, 'rS2'), primary_manifest=man(plan, dg0, 'rP2')),
               {'G2'})
        expect('S8i 보충 manifest 인계 도구 지문 ≠ 이 체크아웃 (다른 체크아웃에서 만든 영수증)',
               receipt(manifest=man(plan, dg0, 'rS_ho', handover_code_hashes=lambda m: {k: '9' * 64 for k in m['handover_code_hashes']})), {'F6'})
        expect('S8j 보충 manifest 없음 · 깨진 JSON', receipt(manifest=str(td / 'nope.json')), {'F0'})
        #  ★ 10-14 Q3 (판정문 §6 "추가 범위 주의" — H1 은 두 manifest 의 상호 일치일 뿐 승인 핀과의 일치가 아니다) — 승인 SHA 를 주면 manifest git.sha 도 대조
        rmk = rsafe(manifest=man(plan, dg0, 'rS_ap'), primary_manifest=mp194, approved_sha='abababa')
        chk(f'S8k Q3 승인 SHA (접두 7) = 두 manifest git.sha → rc 0 · F7 · G7 같음 · ★ (나′) [상태 {state}] pending = rc 1 · 실패 칸 정확히 {{D1 · F5 · G5}} (F7 · G7 은 같음)',
            rmk.get('rc') == (1 if w_l else 0) and bad_ids(rmk) == w_l and fp_why_ok(rmk, w_l, R_reg, P_reg)
            and {'F7', 'G7'} <= {c['id'] for c in rmk.get('checks', [])}, (sorted(bad_ids(rmk)), rmk.get('error')))
        expect('S8k2 Q3 다른 승인 SHA (manifest 둘)', rsafe(manifest=man(plan, dg0, 'rS_ap2'), primary_manifest=mp194, approved_sha='1234567'), {'F7', 'G7'})
        #  ⑨ 읽기 전용 — 정상 영수증을 만든 뒤 리포 입력 파일 sha 가 그대로
        snap = {rel: _sha(_rp(rel)) for rel in (REG_DOC, RUNS_README, R3_TGZ, R2_TGZ, SUPP_DESIGN, spec['design'], spec['cohort'], spec['union'])}
        rsafe(preflight_receipt=P_pos)
        chk('S9 읽기 전용 — 영수증을 만들어도 등록 문서 · README · 묶음 둘 · 설계 · 어댑터 · 코호트 TSV · union 바이트 그대로',
            snap == {rel: _sha(_rp(rel)) for rel in snap}, snap)
        #  ⑩ ★ 10-14 Codex 반례 로그 다섯 (판정문 §7 · 증거 evidence/receipt_extra · 바이트 그대로 읽기만) — 텍스트 로그 단독 · 정상 영수증에 넣은 위조 포장 둘 다 거부
        EVD = REPO / 'docs/reviews/codex_sup20_fix_reverify_evidence_20261014/evidence/receipt_extra'
        for k, nm in enumerate(('wrong_tsv_full_log.log', 'wrong_tsv_registered_grep.log', 'observation_off_full_log.log',
                                'observation_off_truncated_before_stop.log', 'missing_three_prerequisite_lines.log')):
            p_ = EVD / nm
            rt_ = rsafe(dry_run_log=str(p_)) if p_.is_file() else {}
            chk(f'S10 Codex 반례 로그 {nm} → --dry-run-log 로 rc 1 (옛 판: observation_off_full_log 만 rc 1)', p_.is_file() and rt_.get('rc') == 1,
                (p_.is_file(), rt_.get('rc'), sorted(bad_ids(rt_))))
            rw_ = rsafe(preflight_receipt=forge(P_pos, f'codex{k}', log_text=p_.read_bytes().decode('utf-8') if p_.is_file() else ''))
            expect(f'S10b Codex 반례 로그 {nm} 를 정상 영수증의 로그 자리에 (sha 맞춘 위조 포장) → 내용으로 거부 (INPUT_DIGEST_JSON 없음 P2 · 완료 표지 없음 P3)',
                   rw_, {'P2', 'P3'})
        r_e0 = rsafe(dry_run_log=str(EVD / 'wrong_tsv_full_log.log'))
        chk('S10c 텍스트 로그 단독의 사유 = E0 (실행기 완료 영수증을 --preflight-receipt 로 주라는 안내)', 'E0' in bad_ids(r_e0), sorted(bad_ids(r_e0)))
        #  ⑪ ★ 10-15 (나′) 봉인 지문 대기 선언 (1저자 10-15 Q1 (나′)) — 등록 문서 사본 (지문 토큰만 바꿈 · reg_variant) 으로 도구 · 상태 판정을 본다.  실물 상태와 무관하게
        #    같은 답이 나오도록 모의 등록 값 (R_SIM · 체크아웃 지문과 다름) · 모의 대기 값 (P_SIM · P_SIM2) 을 쓴다.  발사 대조 (D1 · E2 · F5 · G5) 는 대기 선언과 무관하게 등록 값만.
        R_SIM = hashlib.sha256(b'supp20_input_receipt selftest: registered (simulated)').hexdigest()
        P_SIM = hashlib.sha256(b'supp20_input_receipt selftest: pending (simulated) 1').hexdigest()
        P_SIM2 = hashlib.sha256(b'supp20_input_receipt selftest: pending (simulated) 2').hexdigest()

        def r0_says(rec, word):
            return any(word in str(x) for x in (cdet_raw(rec, 'R0') or []))
        #  ⓐ 옛 초안 꼴 — 새 지문을 `code_fp <hex>` 둘째 값으로 (10-15 게이트 실패의 꼴) · ★ 10-16 L214R-04: 파서가 활성 §3 만 읽으므로 둘째 값을 §3 안에 둔다
        #     (같은 꼴이 §3 밖 = 역사 · 초안 표면 활성 값으로 읽지 않는다 → S12b)
        ra = receipt(reg_doc=reg_variant('a_old', registered=R_SIM, old_second=fp_now))
        va = ra['registration']['values']
        chk('S11a ★ (나′) ⓐ 옛 초안 꼴 (새 지문을 `code_fp <hex>` 둘째 값으로 적은 등록 문서 — §3 안 · L214R-04) → rc 1 · 실패 칸 정확히 {R0 · D1} '
            '(값이 둘 = 등록 §3 을 못 읽음 · code_fp None) · 상태 판정 = undeclared (시험 충돌 없음)',
            ra['rc'] == 1 and bad_ids(ra) == {'R0', 'D1'} and va.get('code_fp') is None and r0_says(ra, '값이 둘 이상') and fp_state(va, fp_now)[0] == 'undeclared',
            (sorted(bad_ids(ra)), cdet_raw(ra, 'R0'), fp_state(va, fp_now)))
        #  ⓑ 대기 선언 값 둘 (서로 다름) — 등록 = 체크아웃 (D1 은 같음 → R0 만 겨눈다)
        rb = receipt(reg_doc=reg_variant('b_two', registered=fp_now, pending=(P_SIM, P_SIM2)))
        chk('S11b ★ (나′) ⓑ 대기 선언 값 둘 (서로 다름 · 등록 §3 = 체크아웃) → rc 1 · 실패 칸 정확히 {R0} (code_fp_pending 값이 둘 이상) · 읽은 대기 값 None',
            rb['rc'] == 1 and bad_ids(rb) == {'R0'} and r0_says(rb, 'code_fp_pending') and 'code_fp_pending' in rb['registration']['values']
            and rb['registration']['values'].get('code_fp_pending') is None, (sorted(bad_ids(rb)), cdet_raw(rb, 'R0')))
        #  ⓒ 대기 = 등록 (모순 선언) — 등록 = 체크아웃
        rcm = receipt(reg_doc=reg_variant('c_same', registered=fp_now, pending=(fp_now,)))
        chk('S11c ★ (나′) ⓒ 대기 선언 = 등록 §3 (모순 선언 · 등록 = 체크아웃) → rc 1 · 실패 칸 정확히 {R0} (대기 = 등록) · 읽은 대기 값 None',
            rcm['rc'] == 1 and bad_ids(rcm) == {'R0'} and r0_says(rcm, 'code_fp_pending') and 'code_fp_pending' in rcm['registration']['values']
            and rcm['registration']['values'].get('code_fp_pending') is None, (sorted(bad_ids(rcm)), cdet_raw(rcm, 'R0')))
        #  ⓓ 대기 선언 + 체크아웃 = 대기 → 상태 pending · 도구 발사 대조 = 거짓 (컨테이너 D1 · 사전 점검 E2 · 발사 F5 · G5)
        pdoc = reg_variant('d_pend', registered=R_SIM, pending=(fp_now,))
        rd = receipt(reg_doc=pdoc)
        vd = rd['registration']['values']
        chk('S11d ★ (나′) ⓓ 대기 선언 + 체크아웃 = 대기 (등록 §3 = 모의 값) → 상태 pending · 도구 D1 = 거짓 (발사 대조 = 등록 값만 — 대기 선언이 통과시키지 않는다) · '
            'rc 1 · 실패 칸 정확히 {D1} · D1 상세 now = 대기 · registered = 등록 · pending = 대기',
            fp_state(vd, fp_now)[0] == 'pending' and vd.get('code_fp_pending') == fp_now and rd['rc'] == 1 and bad_ids(rd) == {'D1'}
            and fp_why_ok(rd, {'D1'}, R_SIM, fp_now), (fp_state(vd, fp_now), sorted(bad_ids(rd)), cdet(rd, 'D1')))
        rd2 = rsafe(preflight_receipt=P_pos, reg_doc=pdoc)
        chk('S11d2 ★ (나′) ⓓ 같은 문서 · 정상 사전 점검 영수증 (S7) → rc 1 · 실패 칸 정확히 {D1 · E2} (E2 = 등록 값만 · 상세 registered = 등록 · receipt = 체크아웃)',
            rd2.get('rc') == 1 and bad_ids(rd2) == {'D1', 'E2'} and fp_why_ok(rd2, {'D1', 'E2'}, R_SIM, fp_now), (sorted(bad_ids(rd2)), e2_fp(rd2), rd2.get('error')))
        rd3 = receipt(manifest=ms0, primary_manifest=mp194, reg_doc=pdoc)
        chk('S11d3 ★ (나′) ⓓ 같은 문서 · 정상 발사 manifest 둘 (S8) → rc 1 · 실패 칸 정확히 {D1 · F5 · G5} (발사 봉인 = 등록 값만)',
            rd3['rc'] == 1 and bad_ids(rd3) == {'D1', 'F5', 'G5'} and fp_why_ok(rd3, {'D1', 'F5', 'G5'}, R_SIM, fp_now), (sorted(bad_ids(rd3)), cdet(rd3, 'F5')))
        #  ⓔ 대기 선언 없음 + 체크아웃 ≠ 등록 = undeclared (시험이 실패해야 하는 상태) · ⓔ′ 대기 선언 있음 · 체크아웃 ≠ 대기 (다른 코드) = undeclared
        re1 = receipt(reg_doc=reg_variant('e_none', registered=R_SIM))
        s_e1 = fp_state(re1['registration']['values'], fp_now)
        chk('S11e ★ (나′) ⓔ 대기 선언 없음 + 체크아웃 ≠ 등록 §3 → 상태 undeclared (사유 있음 · 시험이 실패해야 하는 상태) · 도구 = rc 1 · 실패 칸 정확히 {D1}',
            s_e1[0] == 'undeclared' and bool(s_e1[1]) and re1['rc'] == 1 and bad_ids(re1) == {'D1'}, (s_e1, sorted(bad_ids(re1))))
        re2 = receipt(reg_doc=reg_variant('e_other', registered=R_SIM, pending=(P_SIM,)))
        s_e2 = fp_state(re2['registration']['values'], fp_now)
        chk('S11e2 ★ (나′) ⓔ′ 대기 선언 있음 (도구가 읽음 = 모의 대기 값) · 체크아웃 ≠ 대기 (다른 코드) → 상태 undeclared · 도구 = rc 1 · 실패 칸 정확히 {D1}',
            re2['registration']['values'].get('code_fp_pending') == P_SIM and s_e2[0] == 'undeclared' and bool(s_e2[1]) and re2['rc'] == 1 and bad_ids(re2) == {'D1'},
            (s_e2, re2['registration']['values'].get('code_fp_pending'), sorted(bad_ids(re2))))
        #  ⓕ 정상 비준 상태 (합성 — 등록 §3 := 체크아웃 지문 · 대기 선언 없음) = rc 0 — 쌍둥이 TWIN · S7l · S8e · S8f 판별의 기준
        rf = receipt(reg_doc=TWIN)
        chk('S11f ★ (나′) ⓕ 정상 비준 상태 (합성 — 등록 §3 := 체크아웃 지문 · 대기 선언 없음 · 다른 칸은 실물) → 상태 registered · rc 0 (대조 칸 전부 같음)',
            fp_state(rf['registration']['values'], fp_now)[0] == 'registered' and rf['rc'] == 0, (fp_state(rf['registration']['values'], fp_now), sorted(bad_ids(rf))))
        rf2 = rsafe(preflight_receipt=P_pos, reg_doc=TWIN)
        chk('S11f2 ★ (나′) ⓕ 같은 쌍둥이 · 정상 사전 점검 영수증 (S7) → rc 0 (pending 의 E2 실패 = 지문 하나뿐 · S7l 판별의 기준)', rf2.get('rc') == 0,
            (sorted(bad_ids(rf2)), rf2.get('error')))
        rf3 = receipt(manifest=ms0, primary_manifest=mp194, reg_doc=TWIN)
        chk('S11f3 ★ (나′) ⓕ 같은 쌍둥이 · 정상 발사 manifest 둘 (S8) → rc 0 (pending 의 F5 · G5 실패 = 지문 하나뿐 · S8e · S8f 판별의 기준)', rf3['rc'] == 0,
            sorted(bad_ids(rf3)))
        #  ⑫ ★ 10-16 L214R-04 (Codex LHS214 재검증 판정문 §5 · 수정 계획 lhs214r_fix_plan_20261016 Q4 = 1저자 비준) — 파서가 **활성 §3 의 code_fp 만** 읽는다
        #    (역사 표 · 초안 표의 같은 기계 구문 `code_fp <hex>` = 읽지 않음 · 등록 문서 · 역사 표는 고치지 않는다).  반례 먼저 — 고치기 전 판은 문서 전체의 토큰을 읽어
        #    안내된 비준 단계 (§3 갱신 + 대기 선언 삭제 + 역사 표 보존) 가 R0 · D1 (registered None) 였다 (ⓕ 쌍둥이는 전역 치환이라 이 구멍을 놓쳤다).
        #    대기 선언은 여전히 발사 허용값이 아니다 (D1 · E2 · F5 · G5 = 등록 §3 값만) · 상충 대기 = R0 (그대로).
        rat_doc, rat = reg_ratify('min', fp_now)
        r12a = receipt(reg_doc=rat_doc)
        v12a = r12a['registration']['values']
        chk('S12a ★ L214R-04 비준 전환 (Codex minimal_activate_section3 — 대기 선언 삭제 · 활성 §3 만 체크아웃 지문으로 · 역사 표의 옛 `code_fp <hex>` 보존) → rc 0 · '
            '읽은 등록 §3 = 체크아웃 · 대기 None (고치기 전: R0 · D1 · registered None)',
            rat['in_s3'] and bool(rat['history']) and not rat['pending_left'] and r12a['rc'] == 0 and v12a.get('code_fp') == fp_now
            and v12a.get('code_fp_pending') is None, (sorted(bad_ids(r12a)), cdet_raw(r12a, 'R0'), cdet(r12a, 'D1'), rat))
        r12a2 = rsafe(preflight_receipt=P_pos, reg_doc=rat_doc)
        chk('S12a2 ★ L214R-04 같은 비준 전환 사본 · 정상 사전 점검 영수증 (S7) → rc 0 (E2 = 활성 §3 값 · 역사 값을 읽지 않는다)',
            rat['in_s3'] and bool(rat['history']) and r12a2.get('rc') == 0, (sorted(bad_ids(r12a2)), e2_fp(r12a2), r12a2.get('error')))
        r12a3 = receipt(manifest=ms0, primary_manifest=mp194, reg_doc=rat_doc)
        chk('S12a3 ★ L214R-04 같은 비준 전환 사본 · 정상 발사 manifest 둘 (S8) → rc 0 (F5 · G5 = 활성 §3 값)',
            rat['in_s3'] and bool(rat['history']) and r12a3['rc'] == 0, sorted(bad_ids(r12a3)))
        #  옛 초안 꼴이 §3 밖 (10-15 게이트 실패의 실제 자리 = §9 표) — 활성 값도 대기 선언도 아니다 → 발사 대조는 §3 값 그대로 (그 토큰이 체크아웃과 같아도 통과 못 함)
        rg = receipt(reg_doc=reg_variant('g_out', registered=R_SIM, old_second=fp_now, old_second_at='end'))
        vg = rg['registration']['values']
        chk('S12b ★ L214R-04 옛 초안 꼴 (`code_fp <체크아웃>`) 이 §3 밖 (역사 · 초안 표) → 읽지 않음 · rc 1 · 실패 칸 정확히 {D1} · 읽은 등록 §3 = 모의 값 · 대기 None · '
            '상태 undeclared (그 토큰이 체크아웃과 같아도 활성 · 대기 값이 아니다 — 고치기 전: R0 · D1)',
            rg['rc'] == 1 and bad_ids(rg) == {'D1'} and vg.get('code_fp') == R_SIM and vg.get('code_fp_pending') is None
            and fp_state(vg, fp_now)[0] == 'undeclared' and cdet(rg, 'D1').get('registered') == R_SIM and cdet(rg, 'D1').get('now') == fp_now,
            (sorted(bad_ids(rg)), cdet_raw(rg, 'R0'), cdet(rg, 'D1')))
        #  대기 선언 + §3 밖 역사 토큰 (같은 기계 구문 · 체크아웃과 같은 값) — 대기 · 역사 어느 쪽도 발사 허용값이 아니다 (D1 · E2 · F5 · G5 = 등록 §3 값만)
        hdoc = reg_variant('h_pend_hist', registered=R_SIM, pending=(fp_now,), old_second=fp_now, old_second_at='end')
        rh = receipt(reg_doc=hdoc)
        vh = rh['registration']['values']
        chk('S12c ★ L214R-04 대기 선언 (= 체크아웃) + §3 밖 역사 토큰 (= 체크아웃) · 등록 §3 = 모의 값 → 상태 pending · rc 1 · 실패 칸 정확히 {D1} · D1 상세 registered = §3 · '
            'pending = 체크아웃 (대기 선언이 발사 허용값이 되지 않는다 — 고치기 전: R0 · D1)',
            fp_state(vh, fp_now)[0] == 'pending' and rh['rc'] == 1 and bad_ids(rh) == {'D1'} and fp_why_ok(rh, {'D1'}, R_SIM, fp_now),
            (fp_state(vh, fp_now), sorted(bad_ids(rh)), cdet(rh, 'D1')))
        rh2 = rsafe(preflight_receipt=P_pos, reg_doc=hdoc)
        chk('S12c2 ★ L214R-04 같은 문서 · 정상 사전 점검 영수증 → rc 1 · 실패 칸 정확히 {D1 · E2} (E2 = 등록 §3 값만)',
            rh2.get('rc') == 1 and bad_ids(rh2) == {'D1', 'E2'} and fp_why_ok(rh2, {'D1', 'E2'}, R_SIM, fp_now), (sorted(bad_ids(rh2)), e2_fp(rh2), rh2.get('error')))
        rh3 = receipt(manifest=ms0, primary_manifest=mp194, reg_doc=hdoc)
        chk('S12c3 ★ L214R-04 같은 문서 · 정상 발사 manifest 둘 → rc 1 · 실패 칸 정확히 {D1 · F5 · G5} (발사 봉인 = 등록 §3 값만)',
            rh3['rc'] == 1 and bad_ids(rh3) == {'D1', 'F5', 'G5'} and fp_why_ok(rh3, {'D1', 'F5', 'G5'}, R_SIM, fp_now), (sorted(bad_ids(rh3)), cdet(rh3, 'F5')))

        def with_pending(src, name, vals):
            """비준 전환 사본 (역사 표 보존) 에 대기 선언 줄을 붙인 사본."""
            t_ = Path(src).read_text(encoding='utf-8')
            for v_ in vals:
                t_ += f'\n| 대기 지문 (selftest 사본) | `code_fp_pending {v_}` |\n'
            q_ = td / f'reg_ratify_{name}.md'
            q_.write_text(t_, encoding='utf-8')
            return str(q_)
        #  상충 대기 (역사 표를 보존한 비준 사본 위) — 대기 = 활성 §3 (모순) · 대기 값 둘 = R0 (그대로)
        ri = receipt(reg_doc=with_pending(rat_doc, 'i_same', (fp_now,)))
        chk('S12d ★ L214R-04 역사 표 보존 비준 사본 + 대기 선언 = 활성 §3 (모순) → rc 1 · 실패 칸 정확히 {R0} · 읽은 대기 None (고치기 전: R0 · D1)',
            ri['rc'] == 1 and bad_ids(ri) == {'R0'} and r0_says(ri, 'code_fp_pending') and ri['registration']['values'].get('code_fp_pending') is None,
            (sorted(bad_ids(ri)), cdet_raw(ri, 'R0')))
        rj = receipt(reg_doc=with_pending(rat_doc, 'j_two', (P_SIM, P_SIM2)))
        chk('S12d2 ★ L214R-04 역사 표 보존 비준 사본 + 대기 선언 값 둘 (서로 다름) → rc 1 · 실패 칸 정확히 {R0} · 읽은 대기 None (고치기 전: R0 · D1)',
            rj['rc'] == 1 and bad_ids(rj) == {'R0'} and r0_says(rj, 'code_fp_pending') and rj['registration']['values'].get('code_fp_pending') is None,
            (sorted(bad_ids(rj)), cdet_raw(rj, 'R0')))
        #  §3 자리 — 제목이 없거나 둘이면 활성 값을 정할 수 없다 (fail-closed · R0 · 문서 전체 토큰으로 대신하지 않는다)
        q12 = td / 'reg_no_s3.md'
        q12.write_text(rtxt.replace('\n## 3.', '\n## 삼.', 1), encoding='utf-8')          # §3 제목만 지움 (토큰은 그대로)
        rk = receipt(reg_doc=str(q12))
        chk('S12e ★ L214R-04 §3 제목 (## 3.) 없음 → rc 1 · R0 (§3 자리 없음) · D1 · 읽은 code_fp None (고치기 전: §3 와 무관하게 문서 전체에서 읽음)',
            rk['rc'] == 1 and {'R0', 'D1'} <= bad_ids(rk) and r0_says(rk, '§3') and rk['registration']['values'].get('code_fp') is None,
            (sorted(bad_ids(rk)), cdet_raw(rk, 'R0')))
        q12 = td / 'reg_two_s3.md'
        q12.write_text(rtxt + f'\n## 3. 코드 신원 (selftest 중복)\n\n- 봉인 32 · `code_fp {R_reg}`\n', encoding='utf-8')
        rl = receipt(reg_doc=str(q12))
        chk('S12e2 ★ L214R-04 §3 제목 둘 (같은 등록 값을 담은 중복 절) → rc 1 · R0 (§3 자리 둘 이상) · 읽은 code_fp None (고치기 전: 값이 하나라 R0 통과)',
            rl['rc'] == 1 and 'R0' in bad_ids(rl) and r0_says(rl, '§3') and rl['registration']['values'].get('code_fp') is None,
            (sorted(bad_ids(rl)), cdet_raw(rl, 'R0')))
        #  울타리 (```) 안의 '#' 줄은 제목이 아니다 — §3 을 거기서 끊지 않는다 (지킴 시험 · 고치기 전 판도 통과)
        s3a, _s3b = s3_span(rtxt)
        jfp = rtxt.find('`code_fp ', s3a) if s3a is not None else -1
        lfp = rtxt.rfind('\n', 0, jfp) if jfp >= 0 else -1
        fence = '\n```bash\n## 4. 울타리 안 (제목 아님)\n# 주석\n```\n'
        q12 = td / 'reg_fence.md'
        q12.write_text((rtxt[:lfp] + fence + rtxt[lfp:]) if lfp >= 0 else (rtxt + fence), encoding='utf-8')
        rfe = receipt(reg_doc=str(q12))
        chk('S12f L214R-04 지킴 — §3 안 code_fp 줄 앞 울타리 (```) 에 "## 4." · "# 주석" 줄 → 제목으로 보지 않음 · 읽은 등록 §3 = 실물 값 · R0 통과',
            lfp >= 0 and rfe['registration']['values'].get('code_fp') == R_reg and 'R0' not in bad_ids(rfe), (sorted(bad_ids(rfe)), cdet_raw(rfe, 'R0')))
    print(f'\nsupp20_input_receipt selftest: {ok}/{ok + len(fail)} PASS' + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description='보충 20 (supp20) 입력 지문 영수증 — 읽기 전용 (Codex 보충 20 지원 검토 Q6 · 수정 계획 sup20_fix_plan_20261012 §3)')
    ap.add_argument('--selftest', action='store_true', help='반례 시험 (raw sha 표 · TSV 한 바이트 · ID · 등록 값 오타 · 일반 계획 강등 · 묶음 · 사전 점검 영수증 · manifest)')
    ap.add_argument('--preflight-receipt', default='',
                    help='★ 10-14 발사 사전 점검 완료 영수증 JSON (실행기 run --root R --cohorts lhss --dry-run --observe-imports --preflight-receipt P.json 이 쓴 것 · '
                         '같은 이름 .log 를 함께 읽는다)')
    ap.add_argument('--approved-sha', default='', help='★ 10-14 저자 발사 승인 커밋 (7–40 hex · 사전 점검 · manifest git 기록과 접두 대조 · 주지 않으면 경고)')
    ap.add_argument('--dry-run-log', default='',
                    help='(10-14 부터 받지 않는다 — 텍스트 · grep 로그 단독은 증거가 아니다 · 주면 E0 실패 · 대신 --preflight-receipt)')
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
                  preflight_receipt=a.preflight_receipt or None, approved_sha=a.approved_sha or None,
                  manifest=a.manifest or None, primary_manifest=a.primary_manifest or None, notes=notes)
    print_receipt(rec)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    return rec['rc']


if __name__ == '__main__':
    sys.exit(main())
