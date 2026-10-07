#!/usr/bin/env python3
"""LHS 배포 표 = 정본 인계표의 **열 부분집합** — 만들기 · 대조 (값 · 행 순서 · 열 사전을 한 글자도 안 바꾼다).

배포 표는 새 계산을 하지 않는다.  정본 인계표 (`docs/data/{lhs,lhsx}_handover_<날짜>.csv` + `_columns.tsv`) 에서
열을 고르기만 한다 — 값의 정의 · 관문은 생성기 `scripts/lhs_design_dataset.py` 소관이다.
배포 v1 (`8b84ba476`, `docs/data/lhs_release_20261001/`) 은 이 방식으로 **바이트 재현**된다 (csv 기본 quoting · 줄 끝 '\\n').

사용:
  # 만들기 — 열 목록은 옛 배포 열 사전 (첫 열) + --add 로 받는다
  python3 scripts/lhs_release_build.py --handover docs/data/lhs_handover_20261001.csv \\
      --columns-from docs/data/lhs_release_20261001/lhs_release_20261001_columns.tsv --add am_ionic_isolated_pct \\
      --out docs/data/lhs_release_<날짜>/lhs_release_<날짜>
  # 대조 — 배포 ⊆ 인계표 (행 · 순서 · 값 · 열 사전 행)
  python3 scripts/lhs_release_build.py --check --handover docs/data/lhs_handover_20261001.csv \\
      --release docs/data/lhs_release_20261001/lhs_release_20261001
  # 부록 — 부록 전용 열 (H12 민감도 `*_hertz_h12` · 열 사전 판정 '부록 전용') 은 --appendix 로 따로 만든 파일에만 (주 배포 표에 넣으면 거부)
  #   ★ 10-06 밤 G2R-01 — τ 모드 열을 실으면 (주 · 부록 둘 다) 인계표 행마다 역할 표기가 공용 세대 계약 (tau_flux.row_generation_problems) 을 통과해야
  #   한다 (이름만으로는 주 Hertz 이름 아래 들어온 H12 숫자를 못 본다 — 만들기 거부 · 대조 문제)
  python3 scripts/lhs_release_build.py --appendix --handover … --columns-from <case_id 한 줄 열 사전> --add tau2_ion_hertz_h12 … --out …_h12
  # ML 배포 프로필 (LREL-02 · 03 — 만들기 · 대조 둘 다) — 키 유일 · 기대 ID 집합 (설계 CSV case_id) · 적격성 세 열 · 열 사전 참조 표지
  python3 scripts/lhs_release_build.py --check --profile ml_v1 --expect-ids docs/data/lhs_design_20260818.csv --handover … --release …
  python3 scripts/lhs_release_build.py --selftest
  # ★ 배포 v1.3 최종판 (10-07 미리 준비 · 실제 자료는 Codex 세대 2 GO + 새 194 배치 뒤에만) — 명령 전문 = docs/reviews/lhs_release_v13_plan_20261007.md
  python3 scripts/lhs_release_build.py --v13 --batch-root <배치 뿌리> --codex-verdict <GO 판정문> --out-dir <배포 폴더>   # 단계 A + B + 대조
  #   발사 봉인 (manifest code_hashes) 과 다른 봉인 파일이 있으면 거부 — 값과 무관한 변경 (웹앱 화면 문구) 만 [--allow-seal-diff <파일>] 로 명시 승인
  #   배치 관문 (⓪ 감사 seal_audit.json · ⓪b 다시 읽기 reread.json) = 필수 · 판정 · 이 배치 뿌리 · manifest · 봉인 지문에 결합 (G2RR3-01 · build · check 같은 함수)
  #   — 옛 · 부분 · 실패 기록을 들여다볼 때만 [--diagnostic-batch-gate] (README · 빌드 manifest 에 NOT FOR RELEASE · 리포 밖 · --v13-check 배포 대조 거부)
  python3 scripts/lhs_release_build.py --v13 --dry-run --handover-dir <세대 1 인계표 폴더> --out-dir <리포 밖 스크래치>   # 경로만 (DRYRUN_)
  python3 scripts/lhs_release_build.py --v13-check --release-dir <배포 폴더> --handover-dir <인계표 폴더> [--dry-run]
  시험: scripts/test_lhs_release_v13.py

키 (case_id) 는 늘 유일해야 한다 (인계표 · 배포 둘 다 — LREL-03).  프로필은 부분집합 충실성 위에 **용도 계약**을 더한다 (범용 부분집합 도구에
모든 용도의 열을 강제하지 않는다 — Codex 배포 v1.1 최종 리뷰 LHSREL-02 해제 조건).
"""
import argparse
import collections
import csv
import datetime
import functools
import glob
import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

KEY = 'case_id'
#: ★ 10-06 저녁 세대 2 (1저자 비준 C1-3) — 부록 전용 열 = 기본 학습 열 아님 (H12 민감도 = 행마다 H0 와 짝인 **두 규약의 쌍대응 시나리오** · 오차막대 · 상하한 · 신뢰구간 아님 — Codex G2R-04).
#:   잡는 길 둘: 이름 꼴 (`*_hertz_h12` · `f_ion_hertz_h12_gap`) 또는 인계표 열 사전 판정에 '부록 전용' (생성기 `TAU_NET_VERDICT_H12`).
#:   주 배포 표에 넣으면 거부 — `--appendix` 로 만든 부록 파일에만 싣는다.  옛 배포 (v1 · v1.1 · v1.2 · Physics 부록) 에는 해당 열이 없다 (selftest ⑬).
APPENDIX_ONLY_RE = re.compile(r'.+_hertz_h12(_gap)?')
APPENDIX_VERDICT_MARK = '부록 전용'
#: ★ LREL-02 · 03 (Codex 배포 v1.1 최종 리뷰 10-01 · 1저자 비준 10-06) — ML 배포 프로필.  ml_v1 = 주 배포 표 (부록은 ① 만):
#:   ① 키 유일 · 기대 ID 집합 (--expect-ids = 설계 CSV 의 case_id 열 · 또는 한 줄 한 ID) 과 같은 집합 · 같은 수 (같은 행 수의 대체 · 중복 거부)
#:   ② 적격성 세 열 (생성기 ELIGIBILITY_COLS) 이 있고 행마다 허용 값 · 정합 (생성기 `eligibility_problems` — 사본 금지)
#:   ③ 열 사전이 이 배포에 없는 정본 인계표 열을 가리키면 그 이름 바로 뒤에 REF_MARK — 배포 표만 받은 사람이 없는 열을 찾지 않게 (사전 문구 = 생성기 소관)
PROFILES = ('ml_v1',)
REF_MARK = '(정본 인계표 열)'
#: 열 사전의 '<모드>' 틀 참조 (예: ion_net_band_frac_<모드>) 를 펼칠 모드 — 생성기 TAU_NET_MODES 와 같은 셋 (모르는 모드는 틀 참조로 안 잡힌다)
REF_MODES = ('hertz', 'physics', 'hertz_h12')
#: ★ 10-06 밤 G2R-01 (Codex 세대 2 적대 리뷰 §2 · 1저자 비준) — 부록 · 주 열을 **이름**으로만 가르면 (APPENDIX_ONLY_RE · 열 사전 판정) 주 Hertz 이름 아래
#:   이미 들어온 H12 숫자를 못 본다.  τ 모드 열 (f_ion · tau2_ion · tau_ion · ion_net_* × hertz · physics · hertz_h12) 을 실을 때는 인계표 행마다 그 행의
#:   역할 표기 (ion_net_<협착 · ψ · 면적 규칙 · 전극 · bulk · 면적 모드>_<모드> · 세대 칸 ion_net_generation) 가 공용 세대 계약
#:   (`tau_flux.row_generation_problems` · `generation_mixing_problem` — 생성기 · 웹앱 정지 계약과 같은 표) 을 통과해야 한다 (만들기 거부 · 대조 문제).
TAU_MODE_COL_RE = re.compile(r'(f_ion|tau2_ion|tau_ion|ion_net_[a-z0-9_]+?)_(hertz_h12|hertz|physics)(_gap)?')


class ReleaseError(RuntimeError):
    """배포 표를 만들거나 대조할 수 없다 — 사유를 그대로 보고한다."""


def _read_csv(path):
    with open(path, encoding='utf-8', newline='') as f:
        r = csv.reader(f)
        head = next(r)
        rows = [row for row in r]
    if len(set(head)) != len(head):
        raise ReleaseError(f'{path}: 열 이름 중복')
    for i, row in enumerate(rows, 2):
        if len(row) != len(head):
            raise ReleaseError(f'{path}:{i} 칸 수 {len(row)} ≠ 머리 {len(head)}')
    return head, rows


def _read_tsv(path):
    with open(path, encoding='utf-8', newline='') as f:
        rows = list(csv.reader(f, delimiter='\t'))
    if not rows:
        raise ReleaseError(f'{path}: 비었다')
    return rows[0], rows[1:]


def _cols_path(prefix):
    return prefix + '_columns.tsv'


def _prefix(csv_path):
    if not csv_path.endswith('.csv'):
        raise ReleaseError(f'{csv_path}: .csv 가 아니다')
    return csv_path[:-4]


def appendix_only(columns, cdict=None, chead=None):
    """columns 중 부록 전용 열 (이름 꼴 · 또는 열 사전 판정 '부록 전용') — 순서 그대로."""
    vi = chead.index('verdict') if chead and 'verdict' in chead else None
    out = []
    for c in columns:
        row = (cdict or {}).get(c)
        if APPENDIX_ONLY_RE.fullmatch(c) or (vi is not None and row is not None and len(row) > vi and APPENDIX_VERDICT_MARK in row[vi]):
            out.append(c)
    return out


def _appendix_problem(columns, cdict, chead, appendix):
    ap_ = appendix_only(columns, cdict, chead)
    if ap_ and not appendix:
        return (f'부록 전용 열 {ap_} — 주 배포 표에 넣지 않는다 (기본 학습 열 아님 · H12 민감도 = 부록 · 10-06 1저자 비준 C1-3) — '
                '--appendix 로 부록 파일을 따로 만든다')
    return ''


def tau_role_problems(head, rows, columns):
    """columns (배포할 열) 에 τ 모드 열이 있으면 인계표 행마다 공용 세대 계약 → 문제 목록 ([] = 통과 · τ 모드 열이 없으면 늘 [] — 그 숫자가 배포에 없다).
    행의 역할 표기는 배포에 싣지 않은 열이어도 인계표에 있으면 본다 (숫자의 출처 = 그 행) · 세대 칸이 없는 계약 전 인계표 (v1.2) 는 있는 표기만 본다."""
    if not any(TAU_MODE_COL_RE.fullmatch(c) for c in columns):
        return []
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    import tau_flux as TF                                                # noqa: E402 — 세대 계약의 정본 (사본 금지)
    drows = [dict(zip(head, r)) for r in rows]
    probs = []
    for r in drows:
        g, pp = TF.row_generation_problems(r)
        if pp:
            probs.append(f'{r.get(KEY)}: τ 열의 역할 · 세대 계약 위반 ({g or "?"}) — {pp[0]}' + (f' 외 {len(pp) - 1}' if len(pp) > 1 else '')
                         + ' (G2R-01 — 열 이름이 아니라 그 행의 역할 표기로 본다)')
    if not probs:
        mix = TF.generation_mixing_problem([dict(r, case=r.get(KEY)) for r in drows])
        if mix:
            probs.append(f'τ 열의 세대 — {mix}')
    return probs


def _dup_keys(head, rows):
    """키 열 (case_id) 의 빈 값 · 중복 → (빈 칸 수, 중복 키 목록).  키 열이 없으면 (0, None)."""
    if KEY not in head:
        return 0, None
    i = head.index(KEY)
    ks = [r[i] for r in rows]
    return ks.count(''), sorted({k for k in ks if k != '' and ks.count(k) > 1})


def _load_ids(path):
    """기대 ID — CSV 머리에 case_id 가 있으면 그 열 · 아니면 한 줄 한 ID (빈 줄 · '#' 줄 무시).  중복 · 빈 목록이면 ReleaseError."""
    if not path or not os.path.isfile(path):
        raise ReleaseError(f'기대 ID 원천이 없다 ({path!r}) — 프로필은 --expect-ids (설계 CSV) 를 요구한다')
    with open(path, encoding='utf-8-sig', newline='') as f:
        text = f.read()
    lines = text.splitlines()
    if lines and KEY in next(csv.reader([lines[0]])):
        ids = [r.get(KEY, '') for r in csv.DictReader(io.StringIO(text))]
    else:
        ids = [ln.strip() for ln in lines if ln.strip() and not ln.lstrip().startswith('#')]
    if not ids or '' in ids or len(set(ids)) != len(ids):
        raise ReleaseError(f'기대 ID 원천 {path} 이 비었거나 빈 ID · 중복이 있다')
    return ids


def dangling_refs(rel_cols, handover_cols, dict_rows):
    """열 사전 행 (첫 칸 = 열 이름) 의 글에서 '이 배포에 없는 정본 인계표 열' 참조 중 바로 뒤에 REF_MARK 가 없는 것 → [(행 열, 참조)].
    참조 = 인계표 열 이름과 같은 낱말 (영숫자 · 밑줄 · 한글) · '<모드>' 틀 (REF_MODES 로 펼쳐 하나라도 인계표에만 있으면)."""
    shipped, hs = set(rel_cols), set(handover_cols)
    out = []
    for row in dict_rows:
        text = ' '.join(row[1:])
        for m in re.finditer(r'([A-Za-z0-9_]+_)<모드>', text):
            names = {m.group(1) + md for md in REF_MODES} | {m.group(1) + md + '_gap' for md in REF_MODES}
            if any(n in hs and n not in shipped for n in names) and not text[m.end():].lstrip().startswith(REF_MARK):
                out.append((row[0], m.group(0)))
        for m in re.finditer(r'(?<![\w<])(\w+)(?![\w<])', text):
            t = m.group(1)
            if t in hs and t not in shipped and not text[m.end():].lstrip().startswith(REF_MARK):
                out.append((row[0], t))
    return out


def profile_problems(profile, release_prefix, handover_csv, expect_ids, appendix=False):
    """ML 배포 프로필 (PROFILES) 문제 목록 ([] = 통과).  release_prefix 의 CSV · 열 사전 · 인계표 (사전 참조의 열 이름 원천) 를 읽는다."""
    if profile not in PROFILES:
        raise ReleaseError(f'모르는 프로필 {profile!r} (아는 것: {PROFILES})')
    probs = []
    rh, rrows = _read_csv(release_prefix + '.csv')
    n_blank, dups = _dup_keys(rh, rrows)
    if dups is None:
        return [f'배포에 키 열 {KEY} 가 없다']
    if n_blank or dups:
        probs.append(f'배포 키 빈 칸 {n_blank} · 중복 {dups[:5]} (LREL-03)')
    try:
        want = _load_ids(expect_ids)
    except ReleaseError as e:
        probs.append(f'기대 ID — {e} (LREL-03)')
        want = None
    if want is not None:
        got = [r[rh.index(KEY)] for r in rrows]
        if len(got) != len(want) or set(got) != set(want):
            probs.append(f'기대 ID 집합과 다르다 — 행 {len(got)} · 기대 {len(want)} · 배포에만 {sorted(set(got) - set(want))[:5]} · '
                         f'기대에만 {sorted(set(want) - set(got))[:5]} (LREL-03)')
    if appendix:
        return probs
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import lhs_design_dataset as LDD                                     # noqa: E402 — 적격성 규칙의 정본 (사본 금지)
    miss = [c for c in LDD.ELIGIBILITY_COLS if c not in rh]
    if miss:
        probs.append(f'적격성 열이 배포에 없다 {miss} — ML 주 배포는 세 열을 함께 싣는다 (LREL-02)')
    else:
        extra = [c for c in ('calculation_status', 'porosity_sphere_pct_RECORD_ONLY', 'phi_sum_gt_one', *LDD.ELIGIBILITY_COUNTS) if c in rh]
        nbad = 0
        for r in rrows:
            rec = {c: r[rh.index(c)] for c in (*LDD.ELIGIBILITY_COLS, *extra)}
            ep = LDD.eligibility_problems(rec, porosity_pct=rec.get('porosity_sphere_pct_RECORD_ONLY'))
            if ep:
                nbad += 1
                if nbad <= 5:
                    probs.append(f'{r[rh.index(KEY)]}: 적격성 — ' + ' · '.join(ep[:3]) + ' (LREL-02)')
        if nbad > 5:
            probs.append(f'… 적격성 문제 행 모두 {nbad} (LREL-02)')
    hh, _ = _read_csv(handover_csv)
    _, crow = _read_tsv(_cols_path(release_prefix))
    dg = dangling_refs(rh, hh, crow)
    if dg:
        by = {}
        for col, ref in dg:
            by.setdefault(ref, []).append(col)
        for ref, cols in sorted(by.items())[:8]:
            probs.append(f'열 사전이 배포에 없는 정본 인계표 열 {ref} 을 표지 {REF_MARK} 없이 가리킨다 (사전 행 {len(cols)}: {cols[:3]})')
        if len(by) > 8:
            probs.append(f'… 사전 참조 표지 문제 참조 모두 {len(by)}')
    return probs


def build(handover_csv, columns, out_prefix, appendix=False, profile=None, expect_ids=None):
    """columns (순서 그대로) 를 인계표에서 뽑아 `<out_prefix>.csv` · `_columns.tsv` 를 쓴다.
    appendix=False (주 배포) 이면 부록 전용 열 (`appendix_only`) 을 거부한다 · 인계표 키 빈 칸 · 중복이면 거부 (LREL-03) ·
    profile (ml_v1) 이면 쓴 뒤 `profile_problems` 가 문제를 내면 파일을 지우고 거부한다."""
    if not columns or columns[0] != KEY:
        raise ReleaseError(f'첫 열은 {KEY} 여야 한다 (받은 것: {columns[:1]})')
    if len(set(columns)) != len(columns):
        raise ReleaseError('배포 열 목록에 중복이 있다')
    if profile is not None and profile not in PROFILES:
        raise ReleaseError(f'모르는 프로필 {profile!r} (아는 것: {PROFILES})')
    head, rows = _read_csv(handover_csv)
    n_blank, dups = _dup_keys(head, rows)
    if n_blank or dups:
        raise ReleaseError(f'인계표 키 {KEY} 빈 칸 {n_blank} · 중복 {(dups or [])[:5]} — 행 수가 고유 설계 수를 보증하지 않는다 (LREL-03)')
    missing = [c for c in columns if c not in head]
    if missing:
        raise ReleaseError(f'인계표에 없는 열: {missing}')
    ch, crow = _read_tsv(_cols_path(_prefix(handover_csv)))
    cdict = {r[0]: r for r in crow}
    nodict = [c for c in columns if c not in cdict]
    if nodict:
        raise ReleaseError(f'인계표 열 사전에 없는 열: {nodict}')
    apx = _appendix_problem(columns, cdict, ch, appendix)
    if apx:
        raise ReleaseError(apx)
    trp = tau_role_problems(head, rows, columns)                         # ★ 10-06 밤 G2R-01 — 이름이 아니라 행의 역할 표기
    if trp:
        raise ReleaseError(f'τ 열 역할 문제 {len(trp)} — ' + ' | '.join(trp[:4]))
    idx = [head.index(c) for c in columns]
    d = os.path.dirname(out_prefix)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(out_prefix + '.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(columns)
        for row in rows:
            w.writerow([row[i] for i in idx])
    with open(_cols_path(out_prefix), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(ch)
        for c in columns:
            w.writerow(cdict[c])
    if profile is not None:
        pp = profile_problems(profile, out_prefix, handover_csv, expect_ids, appendix=appendix)
        if pp:
            for f_ in (out_prefix + '.csv', _cols_path(out_prefix)):
                if os.path.exists(f_):
                    os.remove(f_)
            raise ReleaseError(f'프로필 {profile} 문제 {len(pp)} — ' + ' | '.join(pp[:4]))
    return len(rows), len(columns)


def check(handover_csv, release_prefix, appendix=False, profile=None, expect_ids=None):
    """배포 ⊆ 인계표 — 행 집합 · 순서 · 값 · 열 사전 행이 모두 같아야 한다.  문제 목록을 돌려준다 (빈 목록 = 통과).
    appendix=False (주 배포) 이면 부록 전용 열이 있는 것도 문제로 보고한다 · 키 빈 칸 · 중복 (인계표 · 배포) 도 문제 (LREL-03) ·
    profile (ml_v1) 이면 `profile_problems` 를 더한다 (LREL-02 · 03)."""
    probs = []
    hh, hrows = _read_csv(handover_csv)
    rh, rrows = _read_csv(release_prefix + '.csv')
    if not rh or rh[0] != KEY:
        probs.append(f'배포 첫 열이 {KEY} 가 아니다')
        return probs
    for lab_, h_, r_ in (('인계표', hh, hrows), ('배포', rh, rrows)):
        n_blank, dups = _dup_keys(h_, r_)
        if n_blank or dups:
            probs.append(f'{lab_} 키 {KEY} 빈 칸 {n_blank} · 중복 {(dups or [])[:5]} — 행 수가 고유 설계 수를 보증하지 않는다 (LREL-03)')
    extra = [c for c in rh if c not in hh]
    if extra:
        probs.append(f'인계표에 없는 배포 열: {extra}')
        return probs
    hk = [r[hh.index(KEY)] for r in hrows]
    rk = [r[0] for r in rrows]
    if rk != hk:
        probs.append(f'행 키 · 순서가 다르다 (인계표 {len(hk)} · 배포 {len(rk)})')
        return probs
    idx = [hh.index(c) for c in rh]
    nbad = 0
    for hr, rr in zip(hrows, rrows):
        for j, i in enumerate(idx):
            if hr[i] != rr[j]:
                nbad += 1
                if nbad <= 5:
                    probs.append(f'{rr[0]} · {rh[j]}: 배포 {rr[j]!r} ≠ 인계표 {hr[i]!r}')
    if nbad > 5:
        probs.append(f'… 값이 다른 칸 모두 {nbad}')
    ch, crow = _read_tsv(_cols_path(_prefix(handover_csv)))
    rch, rcrow = _read_tsv(_cols_path(release_prefix))
    if rch != ch:
        probs.append('열 사전 머리가 다르다')
    cdict = {r[0]: r for r in crow}
    if [r[0] for r in rcrow] != rh:
        probs.append('열 사전 행 순서 ≠ 배포 열 순서')
    for r in rcrow:
        if cdict.get(r[0]) != r:
            probs.append(f'열 사전 행이 인계표와 다르다: {r[0]}')
    apx = _appendix_problem(rh, cdict, ch, appendix)
    if apx:
        probs.append(apx)
    probs += tau_role_problems(hh, hrows, rh)                            # ★ 10-06 밤 G2R-01 — 값 대조만으로는 역할을 못 본다
    if profile is not None:
        probs += profile_problems(profile, release_prefix, handover_csv, expect_ids, appendix=appendix)
    return probs


def _selftest():
    ok = []

    def chk(name, cond, extra=''):
        ok.append(bool(cond))
        print(f"  {'✓' if cond else '✗'} {name}" + (f' — {extra[:300]}' if extra and not cond else ''))

    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, 'h.csv')
        with open(hp, 'w', encoding='utf-8', newline='') as f:
            f.write('case_id,a,b,c\nx1,1,,3.5\nx2,"4,5",6,\n')
        with open(os.path.join(td, 'h_columns.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write('column\tsource\tmeaning\ncase_id\tdesign\t키\na\tw\t뜻 a\nb\tw\t뜻 b\nc\tw\t뜻 c\n')
        out = os.path.join(td, 'rel', 'r')
        n = build(hp, ['case_id', 'c', 'a'], out)
        chk('① 만들기 → 2 행 × 3 열 · 순서 그대로', n == (2, 3)
            and open(out + '.csv', encoding='utf-8').read() == 'case_id,c,a\nx1,3.5,1\nx2,,"4,5"\n')
        chk('② 대조 통과 (빈칸 · 따옴표 칸 그대로)', check(hp, out) == [])
        try:
            build(hp, ['case_id', 'zz'], out + 'b')
            chk('③ 인계표에 없는 열 → 거부', False)
        except ReleaseError as e:
            chk('③ 인계표에 없는 열 → 거부', 'zz' in str(e))
        try:
            build(hp, ['a', 'case_id'], out + 'c')
            chk('④ 첫 열이 case_id 가 아니면 거부', False)
        except ReleaseError:
            chk('④ 첫 열이 case_id 가 아니면 거부', True)
        s = open(out + '.csv', encoding='utf-8').read().replace('x1,3.5,1', 'x1,3.6,1')
        open(out + '.csv', 'w', encoding='utf-8', newline='').write(s)
        chk('⑤ 값 한 칸 바꿈 → 대조 실패', any('3.6' in p for p in check(hp, out)))
        build(hp, ['case_id', 'c', 'a'], out)
        s = open(out + '.csv', encoding='utf-8').read().replace('x2,,"4,5"\n', '')
        open(out + '.csv', 'w', encoding='utf-8', newline='').write(s)
        chk('⑥ 행 빠짐 → 대조 실패', any('행 키' in p for p in check(hp, out)))
        build(hp, ['case_id', 'c', 'a'], out)
        s = open(out + '_columns.tsv', encoding='utf-8').read().replace('뜻 c', '뜻 C')
        open(out + '_columns.tsv', 'w', encoding='utf-8', newline='').write(s)
        chk('⑦ 열 사전 문구 바뀜 → 대조 실패', any('열 사전 행' in p for p in check(hp, out)))
        try:
            build(hp, ['case_id', 'a', 'a'], out + 'd')
            chk('⑧ 중복 열 → 거부', False)
        except ReleaseError:
            chk('⑧ 중복 열 → 거부', True)
        #  ★ 10-06 저녁 세대 2 (1저자 비준 C1-3) — 부록 전용 열 (H12 민감도 · 열 사전 판정 '부록 전용') 은 주 배포 표에 넣지 않는다 (기본 학습 열 아님).
        hp2 = os.path.join(td, 'g.csv')
        with open(hp2, 'w', encoding='utf-8', newline='') as f:
            f.write('case_id,tau2_ion_hertz,tau2_ion_hertz_h12,f_ion_hertz_h12_gap,q\nx1,2.0,1.8,0.1,7\n')
        with open(os.path.join(td, 'g_columns.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write('column\tsource\tverdict\tmeaning\tcaveat\ncase_id\tdesign\t\t키\t\n'
                    'tau2_ion_hertz\ttau_flux\t✅ 싣는다\t주\t\n'
                    'tau2_ion_hertz_h12\ttau_flux\t⚠ 민감도 부록 전용 (H12)\t민감도\t\n'
                    'f_ion_hertz_h12_gap\ttau_flux\t⚠ 민감도 부록 전용 (H12)\t민감도 판 간격\t\n'
                    'q\tw\t⚠ 민감도 부록 전용 (다른 이름)\t이름 꼴 밖 · 판정으로만 잡는다\t\n')
        o2 = os.path.join(td, 'rel2', 'r')
        for nm_, cols_ in (('⑨ H12 열 (tau2_ion_hertz_h12) 을 주 배포에 넣으면 거부', ['case_id', 'tau2_ion_hertz', 'tau2_ion_hertz_h12']),
                           ('⑨b H12 판 간격 열 (f_ion_hertz_h12_gap — 꼬리 _gap) 도 거부', ['case_id', 'f_ion_hertz_h12_gap']),
                           ('⑨c 이름 꼴 밖이어도 인계표 열 사전 판정이 "부록 전용" 이면 거부', ['case_id', 'q'])):
            try:
                build(hp2, cols_, o2 + 'x')
                chk(nm_, False)
            except ReleaseError as e:
                chk(nm_, '부록 전용' in str(e) and '--appendix' in str(e))
            except TypeError as e:                                   # noqa: PERF203
                chk(f'{nm_} ({e})', False)
        try:
            n2 = build(hp2, ['case_id', 'tau2_ion_hertz_h12', 'f_ion_hertz_h12_gap'], o2 + '_h12', appendix=True)
            chk('⑩ --appendix (부록 파일) 이면 H12 열을 싣는다 · 대조도 appendix 로 통과',
                n2 == (1, 3) and check(hp2, o2 + '_h12', appendix=True) == [])
            chk('⑪ 부록 파일을 주 배포로 대조하면 (appendix 없이) 문제로 보고', any('부록 전용' in p for p in check(hp2, o2 + '_h12')))
        except (ReleaseError, TypeError) as e:
            chk(f'⑩ --appendix ({type(e).__name__}: {e})', False)
            chk('⑪ 부록 파일 대조 (못 만듦)', False)
        n3 = build(hp2, ['case_id', 'tau2_ion_hertz'], o2 + '_main')
        chk('⑫ 주 열만이면 그대로 (부록 전용 열 판정이 다른 열을 막지 않는다)', n3 == (1, 2) and check(hp2, o2 + '_main') == [])
    #  ⑬ 실데이터 — 커밋된 배포 v1.2 (주 · Physics 부록) 는 그대로 대조 통과 (부록 전용 판정은 옛 배포를 바꾸지 않는다)
    here = os.path.dirname(os.path.abspath(__file__))
    hd = os.path.join(here, '..', 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006')
    rd = os.path.join(here, '..', 'docs', 'data', 'lhs_release_20261006_v12')
    if os.path.isdir(hd) and os.path.isdir(rd):
        pr13 = []
        for pre in ('lhs', 'lhsx'):
            for suf in ('', '_physics'):
                pr13 += check(os.path.join(hd, f'{pre}_handover_v12_20261006.csv'), os.path.join(rd, f'{pre}_release_20261006_v12{suf}'))
        chk('⑬ 실데이터 — 배포 v1.2 주 표 · Physics 부록 (lhs · lhsx) 대조 통과 그대로' + (f' — {pr13[:2]}' if pr13 else ''), pr13 == [])
    #  ═══ ⑭–⑲ LREL-02 · 03 (Codex 배포 v1.1 최종 리뷰 10-01 §3 · 1저자 비준 10-06 — 반례 먼저) ═══════════════════════════════════════════
    #   LREL-03 "130 행" ≠ "130 개 고유 설계" — 키 중복 (같은 행 수의 대체) 을 빌더 · 대조가 통과시켰다 → 키 유일은 늘 · 기대 ID 집합은 프로필에서
    #   LREL-02 적격성 세 열을 뺀 배포 (130 × 86) 가 check() 문제 [] 였다 → ML 배포 프로필 (ml_v1) 에서 세 열 필수 · 허용 값 · 정합
    #   + 열 사전이 배포에 없는 정본 인계표 열을 표지 없이 가리키면 프로필 문제 (사전 문구 = 생성기 · 배포 표만 받은 사람이 없는 열을 찾지 않게)
    def _probs(fn):
        try:
            return fn()
        except ReleaseError as e:
            return [f'ReleaseError: {e}']
        except Exception as e:                                       # noqa: BLE001
            return [f'{type(e).__name__}: {e}']
    with tempfile.TemporaryDirectory() as td:
        hp = os.path.join(td, 'h.csv')
        elig = ('physical_target_status', 'hold_reason_codes', 'boundary_state')
        with open(hp, 'w', encoding='utf-8', newline='') as f:
            f.write('case_id,a,physical_target_status,hold_reason_codes,boundary_state,c\n'
                    'x1,1,OK,,INSIDE,5\nx2,2,HOLD,BOUNDARY_CENTER_OUT,CENTER_CROSSED,6\n')
        with open(os.path.join(td, 'h_columns.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write('column\tsource\tmeaning\ncase_id\tdesign\t키\na\tw\t뜻 a — c (정본 인계표 열) 와 같이 본다\n'
                    'physical_target_status\th\t적격성\nhold_reason_codes\th\t코드\nboundary_state\th\t경계\nc\tw\t뜻 c\n')
        ids = os.path.join(td, 'ids.csv')
        with open(ids, 'w', encoding='utf-8', newline='') as f:
            f.write('case_id,block\nx1,bimodal\nx2,bimodal\n')
        out = os.path.join(td, 'rel', 'r')
        hd = os.path.join(td, 'hdup.csv')
        with open(hd, 'w', encoding='utf-8', newline='') as f:
            f.write('case_id,a\nx1,1\nx1,1\n')
        with open(os.path.join(td, 'hdup_columns.tsv'), 'w', encoding='utf-8', newline='') as f:
            f.write('column\tsource\tmeaning\ncase_id\tdesign\t키\na\tw\t뜻 a\n')
        p14 = _probs(lambda: [str(build(hd, ['case_id', 'a'], out + 'd'))])
        chk('⑭ ★ LREL-03 — 인계표 키 중복 (x1 두 번 · 행 수 2) 이면 만들기 거부', any('ReleaseError' in p and '중복' in p for p in p14), repr(p14))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out + 'dd.csv', 'w', encoding='utf-8', newline='') as f:
            f.write('case_id,a\nx1,1\nx1,1\n')
        with open(out + 'dd_columns.tsv', 'w', encoding='utf-8', newline='') as f:
            f.write('column\tsource\tmeaning\ncase_id\tdesign\t키\na\tw\t뜻 a\n')
        p15 = _probs(lambda: check(hd, out + 'dd'))
        chk('⑮ ★ LREL-03 — 인계표 · 배포가 같은 키 중복 (행 키 · 순서는 같다) 이어도 대조가 문제로 보고', any('중복' in p for p in p15), repr(p15))
        build(hp, ['case_id', 'a', 'c'], out + 'n')                       # 적격성 세 열을 뺀 배포 (Codex export_omitted_eligibility 축소판)
        p16 = _probs(lambda: check(hp, out + 'n', profile='ml_v1', expect_ids=ids))
        chk('⑯ ★ LREL-02 — 적격성 세 열을 뺀 주 배포를 ml_v1 프로필로 대조하면 문제 (옛 대조는 [] — 부분집합 충실성만 봤다)',
            any('적격성' in p for p in p16) and check(hp, out + 'n') == [], repr(p16))
        p16b = _probs(lambda: [str(build(hp, ['case_id', 'a', 'c'], out + 'nb', profile='ml_v1', expect_ids=ids))])
        chk('⑯b ★ LREL-02 — ml_v1 프로필로 만들 때 적격성 열이 빠지면 만들기 거부', any('ReleaseError' in p and '적격성' in p for p in p16b), repr(p16b))
        _probs(lambda: [str(build(hp, ['case_id', 'a', *elig, 'c'], out + 'ok', profile='ml_v1', expect_ids=ids))])
        p17 = _probs(lambda: check(hp, out + 'ok', profile='ml_v1', expect_ids=ids))
        chk('⑰ ml_v1 — 키 · 기대 ID · 적격성 세 열 · 사전 참조 표지 (c 가 배포에 있어도 표지는 무해) 가 맞으면 통과', p17 == [], repr(p17))
        s17 = open(out + 'ok.csv', encoding='utf-8').read() if os.path.exists(out + 'ok.csv') else ''
        with open(out + 'bad.csv', 'w', encoding='utf-8', newline='') as f:
            f.write(s17.replace('x2,2,HOLD,BOUNDARY_CENTER_OUT,CENTER_CROSSED', 'x2,2,HOLD,,CENTER_CROSSED'))
        if os.path.exists(out + 'ok_columns.tsv'):
            shutil.copyfile(out + 'ok_columns.tsv', out + 'bad_columns.tsv')
        p17b = _probs(lambda: profile_problems('ml_v1', out + 'bad', hp, ids))
        chk('⑰b ★ LREL-02 — 적격성 정합 위반 (HOLD 인데 보류 코드 없음 · CENTER_CROSSED 인데 BOUNDARY_CENTER_OUT 없음) 이면 프로필 문제 (생성기 같은 함수)',
            any('x2' in p and '적격성' in p for p in p17b), repr(p17b))
        ids2 = os.path.join(td, 'ids2.csv')
        with open(ids2, 'w', encoding='utf-8', newline='') as f:
            f.write('case_id\nx1\nx3\n')
        p18 = _probs(lambda: check(hp, out + 'ok', profile='ml_v1', expect_ids=ids2))
        chk('⑱ ★ LREL-03 — 기대 ID 집합 (설계 CSV case_id) 과 다르면 (x2 ↔ x3) 프로필 문제', any('기대 ID' in p for p in p18), repr(p18))
        p18b = _probs(lambda: check(hp, out + 'ok', profile='ml_v1'))
        chk('⑱b 프로필에 기대 ID 원천이 없으면 문제 (기대 ID 없이 "완전" 을 말하지 않는다)',
            any('기대 ID' in p and 'Error' not in p.split(':')[0] for p in p18b), repr(p18b))
        _probs(lambda: [str(build(hp, ['case_id', 'a', *elig], out + 'dg', profile=None))])
        sdg = open(out + 'dg_columns.tsv', encoding='utf-8').read() if os.path.exists(out + 'dg_columns.tsv') else ''
        with open(out + 'dg_columns.tsv', 'w', encoding='utf-8', newline='') as f:
            f.write(sdg.replace('c (정본 인계표 열) 와 같이 본다', 'c 와 같이 본다'))
        with open(os.path.join(td, 'h2.csv'), 'w', encoding='utf-8', newline='') as f, open(hp, encoding='utf-8') as g:
            f.write(g.read())
        with open(os.path.join(td, 'h2_columns.tsv'), 'w', encoding='utf-8', newline='') as f, open(os.path.join(td, 'h_columns.tsv'), encoding='utf-8') as g:
            f.write(g.read().replace('c (정본 인계표 열) 와 같이 본다', 'c 와 같이 본다'))
        p19 = _probs(lambda: profile_problems('ml_v1', out + 'dg', os.path.join(td, 'h2.csv'), ids))
        chk('⑲ ★ 열 사전이 배포에 없는 정본 인계표 열 (c) 을 표지 없이 가리키면 프로필 문제 · 표지 "(정본 인계표 열)" 가 있으면 통과',
            any('c' in p and '사전' in p for p in p19)
            and _probs(lambda: profile_problems('ml_v1', out + 'ok', hp, ids)) == [], repr(p19))
    #  ⑲b 실데이터 — 배포 v1.2 주 표 둘 (설계 CSV 기대 ID) 은 키 · 기대 ID · 적격성 = 통과 · 사전 참조만 문제 (v1.2 사전 문구는 표지 전 — README 가 정정판)
    here = os.path.dirname(os.path.abspath(__file__))
    hd_ = os.path.join(here, '..', 'docs', 'data', 'lhs_network194_11fcf91e8', 'handover_v12_20261006')
    rd_ = os.path.join(here, '..', 'docs', 'data', 'lhs_release_20261006_v12')
    if os.path.isdir(hd_) and os.path.isdir(rd_):
        kinds = []
        for pre, dsg in (('lhs', 'lhs_design_20260818.csv'), ('lhsx', 'lhsx_design_adapted_20260929.csv')):
            pp = _probs(lambda: profile_problems('ml_v1', os.path.join(rd_, f'{pre}_release_20261006_v12'),
                                                 os.path.join(hd_, f'{pre}_handover_v12_20261006.csv'),
                                                 os.path.join(here, '..', 'docs', 'data', dsg)))
            kinds.append((pre, [p for p in pp if '사전' not in p], sum('사전' in p for p in pp)))
        chk('⑲b 실데이터 — 배포 v1.2 주 표 (lhs · lhsx) ml_v1: 키 · 기대 ID (설계 CSV) · 적격성 문제 0 · 사전 참조 표지 문제만 남는다 (v1.2 문구 = 표지 전)',
            all(not k[1] and k[2] > 0 for k in kinds), repr(kinds))
    #  ═══ ⑳ G2R-01 (Codex 세대 2 적대 리뷰 §2 · 1저자 비준 10-06 밤 — 반례 먼저) — 열 이름만으로 부록 · 주 열을 가르면 주 Hertz 이름 아래 이미 들어온
    #   H12 숫자를 못 본다.  τ 모드 열을 실을 때 그 행의 역할 표기 (인계표의 ion_net_<협착 · ψ · 면적 규칙 · 전극 · bulk · 면적 모드>_<모드> · 세대 칸) 가
    #   공용 세대 계약 (tau_flux.row_generation_problems) 을 통과해야 한다.  역할 표기 오라클 = 아래 손 칸 (도우미 상수를 베끼지 않는다).
    G2H = {'constriction': 'maxwell_halfspace', 'psi': '', 'area_rule': 'hertz_ccpl22', 'electrode': 'dirichlet_exact', 'bulk': 'cylinder_half_d',
           'area_mode': 'hertz'}
    G2P = {'constriction': 'mikic_psi_multiply', 'psi': 'multiply', 'area_rule': 'physics_g2', 'electrode': 'dirichlet_exact',
           'bulk': 'cylinder_half_d', 'area_mode': 'physics'}
    G2H12 = {'constriction': 'mikic_psi_multiply', 'psi': 'multiply', 'area_rule': 'hertz_ccpl22', 'electrode': 'dirichlet_exact',
             'bulk': 'sphere_segment', 'area_mode': 'hertz'}
    G1H = dict(G2H, electrode='virtual_source_legacy')
    G1P = {'constriction': 'mikic_psi_divide', 'psi': 'legacy_divide', 'area_rule': 'physics_g1', 'electrode': 'virtual_source_legacy',
           'bulk': 'cylinder_half_d', 'area_mode': 'physics'}
    NOREC = {k: '' for k in G2H}

    def _row(case, gen, h, p, h12, tau=('2.0', '3.0', '2.5')):
        r = {'case_id': case, 'tau2_ion_hertz': tau[0], 'tau2_ion_physics': tau[1], 'tau2_ion_hertz_h12': tau[2], 'ion_net_generation': gen}
        for m, meta in (('hertz', h), ('physics', p), ('hertz_h12', h12)):
            r.update({f'ion_net_{b}_{m}': v for b, v in meta.items()})
        return r

    def _hand(td_, name, rows):
        head = list(rows[0])
        hp_ = os.path.join(td_, name + '.csv')
        with open(hp_, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, lineterminator='\n')
            w.writerow(head)
            for r in rows:
                w.writerow([r[c] for c in head])
        with open(os.path.join(td_, name + '_columns.tsv'), 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, delimiter='\t', lineterminator='\n')
            w.writerow(['column', 'source', 'verdict', 'meaning'])
            for c in head:
                w.writerow([c, 'tau_flux' if c != KEY else 'design',
                            '⚠ 민감도 부록 전용 (H12)' if c.endswith('_hertz_h12') else '✅ 싣는다', '뜻 ' + c])
        return hp_
    with tempfile.TemporaryDirectory() as td:
        ok_rows = [_row('x1', 'g2', G2H, G2P, G2H12), _row('x2', 'g2', G2H, G2P, G2H12)]
        bad_rows = [_row('x1', 'g2', G2H, G2P, G2H12), _row('x2', 'g2', G2H12, G2P, G2H12, tau=('1.6', '3.0', '1.6'))]   # x2 = H12 를 주 자리에
        hp_ok, hp_bad = _hand(td, 'ok', ok_rows), _hand(td, 'bad', bad_rows)
        p20 = _probs(lambda: [str(build(hp_ok, ['case_id', 'tau2_ion_hertz', 'tau2_ion_physics'], os.path.join(td, 'r_ok')))])
        chk('⑳a 양성 — 세대 2 행 (주 Hertz = H0 표기 · physics · H12) 의 주 τ 열 → 만들기 · 대조 통과',
            p20 == ['(2, 3)'] and _probs(lambda: check(hp_ok, os.path.join(td, 'r_ok'))) == [], repr(p20))
        p20b = _probs(lambda: [str(build(hp_bad, ['case_id', 'tau2_ion_hertz'], os.path.join(td, 'r_bad')))])
        chk('⑳b ★ G2R-01 — 주 Hertz 칸 이름 (tau2_ion_hertz) 아래 H12 표기 행 (x2: 협착 mikic_psi_multiply · bulk sphere_segment) 이면 만들기 거부 '
            '(옛: 이름만 보고 통과)', any('ReleaseError' in p and 'x2' in p and '역할' in p for p in p20b), repr(p20b))
        shutil.copyfile(os.path.join(td, 'r_ok.csv'), os.path.join(td, 'r_cp.csv'))
        shutil.copyfile(os.path.join(td, 'r_ok_columns.tsv'), os.path.join(td, 'r_cp_columns.tsv'))
        p20c = _probs(lambda: check(hp_bad, os.path.join(td, 'r_cp'), appendix=False))
        chk('⑳c ★ 대조도 같은 계약 — 값 · 행이 같은 배포를 H12 표기 행이 섞인 인계표에 대조하면 역할 문제 (값 대조만으로는 못 본다)',
            any('x2' in p and '역할' in p for p in p20c), repr(p20c))
        p20d = _probs(lambda: [str(build(hp_bad, ['case_id', 'tau2_ion_hertz_h12'], os.path.join(td, 'r_bad_h12'), appendix=True))])
        chk('⑳d 부록도 같은 계약 — 행 계약이 깨진 인계표에서는 H12 부록 열도 거부 (행 하나의 표기가 틀리면 그 행의 세대가 확정되지 않는다)',
            any('ReleaseError' in p and '역할' in p for p in p20d), repr(p20d))
        p20e = _probs(lambda: [str(build(hp_bad, ['case_id'], os.path.join(td, 'r_bad_key')))])
        chk('⑳e τ 모드 열을 안 실으면 역할 계약을 걸지 않는다 (그 숫자가 배포에 없다)', p20e == ['(2, 1)'], repr(p20e))
        g1 = _hand(td, 'g1', [_row('y1', 'inferred_legacy', G1H, G1P, NOREC, tau=('2.0', '3.0', '')),
                              _row('y2', 'inferred_legacy', G1H, G1P, NOREC, tau=('2.1', '3.1', ''))])
        p20f = _probs(lambda: [str(build(g1, ['case_id', 'tau2_ion_hertz', 'tau2_ion_physics'], os.path.join(td, 'r_g1')))])
        mixed = _hand(td, 'mixed', [_row('z1', 'g2', G2H, G2P, G2H12), _row('z2', 'inferred_legacy', G1H, G1P, NOREC, tau=('2.0', '3.0', ''))])
        p20g = _probs(lambda: [str(build(mixed, ['case_id', 'tau2_ion_hertz'], os.path.join(td, 'r_mixed')))])
        chk('⑳f 옛 세대 행 (inferred_legacy · 표기 = 이력 사실) 은 통과 · 세대 2 행과 한 배포에 섞이면 거부 (세대 섞임)',
            p20f == ['(2, 3)'] and any('ReleaseError' in p and '세대' in p for p in p20g), repr((p20f, p20g)))
    print(f"{sum(ok)}/{len(ok)}  {'✓ 전부 통과' if all(ok) else '✗ 실패 있음'}")
    return 0 if all(ok) else 1


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
#  배포 v1.3 — 최종판 (1저자 10-06 밤 *"v1.3 에 최종이라고 하고 확실하게 넘겨주자"* · 10-07 *"v1.3 생성기를 Codex 판정과 동시에 미리 준비"*)
#    = 세대 2 망 값 + #1 ML 표 (빈칸 뜻대로) · #2 f 타깃 · 관통 분류 안내 · #5 porosity–σ–CN 재적합 · τ 표시 이름 (수송 tortuosity) · se_isolated_pct
#  ⛔ 실제 v1.3 자료는 Codex 세대 2 GO + 새 194 배치 (봉인 manifest `expected_network_generation = g2`) 뒤에만 만든다 — 그 전에는 --dry-run
#    (DRYRUN_ 표지 · docs/data 밖) 로 경로만 돈다.  명령 = `docs/reviews/lhs_release_v13_plan_20261007.md`.
#  구조: 단계 A (`stage_handovers_v13` — 배치 뿌리에서 인계표 생성기 CLI 를 --tau-batch-manifest 와 함께 · 세대 2 아닌 · 섞인 배치는 생성기
#    `load_tau_results` 가 거부) → 단계 B (`build_v13` — 인계표 → 세대 관문 · τ 다시 읽기 (`load_tau_results` 같은 배치 기대 세대 · 칸 대조) ·
#    배포 표 (열 부분집합 · `build` · 프로필 ml_v1) · 빈칸 뜻 · ML 표 · 재적합 · README · 빌드 manifest → `check_v13` 통과 뒤에만 폴더를 세운다).
# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V13_DATASETS = ('lhs', 'lhsx')
V13_GENERATION = 'g2'
V13_DRY_PREFIX = 'DRYRUN_'
V13_DRY_BANNER = 'DRY RUN — not a release'
#: 인계표 생성기 입력 (v1.2 WSL 실행 기록 `docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/wsl_run_20261006.md` 와 같은 짝 ·
#:   194 실행기 COHORT_SPECS 와 같은 원천 — 배치 manifest plan.cohorts 와 `v13_manifest_inputs_problems` 가 대조한다).
V13_INPUTS = {
    'lhs': {'design': '', 'expect_ids': 'docs/data/lhs_design_20260818.csv', 'harvest': 'docs/data/lhs_descriptors_cov_1e09f661d',
            'union': 'docs/data/lhs_union_20260927/lhs130_union.tsv', 'n': 130},
    'lhsx': {'design': 'docs/data/lhsx_design_adapted_20260929.csv', 'expect_ids': 'docs/data/lhsx_design_adapted_20260929.csv',
             'harvest': 'docs/data/lhsx_descriptors_cov_1e09f661d', 'union': 'docs/data/lhs_union_20260927/lhsx64_union.tsv', 'n': 64},
}
#: 생성기 묶음 — v1.2 다섯 + 망 τ + 유도 묶음 se_isolation (고립 전해질 · 생성기 `WA_SE_ISO_GROUP`)
V13_WEBAPP_GROUPS = 'contact,percolation,f1,fracture,area,tau,se_isolation'
#: 열 명세의 바탕 = 커밋된 v1.2 배포 열 사전 첫 열 (값 · 순서 그대로 이어받는다 — v1.1 → v1.2 와 같은 방식)
V13_BASE_FROM = {ds: f'docs/data/lhs_release_20261006_v12/{ds}_release_20261006_v12_columns.tsv' for ds in V13_DATASETS}
V13_PHYSICS_BASE_FROM = {ds: f'docs/data/lhs_release_20261006_v12/{ds}_release_20261006_v12_physics_columns.tsv' for ds in V13_DATASETS}
#: v1.3 주 표에 더하는 열 — 새 열 se_isolated_pct · 세대 2 출처 (세대 칸 + 주 Hertz 의 역할 표기 넷) · 완료 압력 셋 (DESC-06)
V13_MAIN_ADD = ('se_isolated_pct', 'ion_net_generation', 'ion_net_constriction_hertz', 'ion_net_area_rule_hertz', 'ion_net_electrode_hertz',
                'ion_net_bulk_hertz')
V13_PRESS_ADD = ('press_target_mpa', 'press_last_loop_mpa', 'press_reached')
V13_PHYSICS_ADD = ('ion_net_generation', 'ion_net_constriction_physics', 'ion_net_psi_physics', 'ion_net_area_rule_physics',
                   'ion_net_electrode_physics', 'ion_net_bulk_physics')
#: H12 민감도 부록 (선택 · --h12-appendix — 1저자 결정 대기 · 기본 학습 열 아님 · 부록 전용 판정)
V13_H12_COLUMNS = ('case_id', 'f_ion_hertz_h12', 'tau2_ion_hertz_h12', 'tau_ion_hertz_h12', 'ion_net_status_hertz_h12',
                   'ion_net_status_reason_hertz_h12', 'ion_net_generation', 'ion_net_constriction_hertz_h12', 'ion_net_psi_hertz_h12',
                   'ion_net_bulk_hertz_h12', 'ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis')

#: ★ #1 빈칸 뜻 — 닫힌 어휘 (v1.1 README §3-1 · v1.2 §3-1 · Codex 5차 QV2).  배포 CSV 의 빈칸은 뜻이 여럿이다 — ML 표는 빈칸이 있는 열마다 바로 뒤에
#:   `<열>__blank` (코드) 를 붙인다.  규칙 (`v13_blank_reason`) 에 없는 빈칸 · 빈칸이어야 할 칸의 값은 만들기 거부 (추측으로 코드를 달지 않는다).
V13_BLANK_CODES = {
    'NA_PHASE_ABSENT': '그 상 (AM_P · AM_S) 이 없는 mono 침대 — 정의되지 않음 (0 이 아니다 · 설계 block 이 정한다)',
    'NA_ZERO_CONTACTS': '그 쌍 · AM–AM 접촉 0 개 — 평균 · 파괴 단계가 정의되지 않음 (개수 · 총합은 측정된 0 으로 값이 있다)',
    'NA_NOT_PERCOLATING': '관통 SE 성분 없음 (percolation_pct = 0) — 관통 성분 기준 양 (se_se_cn_perc · _n_perc · _eff_area_perc · 기하학적 tortuosity) '
                          '이 정의되지 않음',
    'INF_NOT_PERCOLATING': '관통 이온 경로 없음 (ion_net_status = NOT_PERCOLATING) — 수송 tortuosity T · √T = 물리적 무한대의 저장 표현 '
                           '(같은 행 f = 0.0 은 값으로 실려 있다) · 기술적 결측이 아니다',
    'NOT_COMPUTED': '기술적 실패 (ion_net_status = NOT_COMPUTED · 사유 = ion_net_status_reason) — 값 없음 · 무한대로 읽지 않는다',
    'HOLD_BAND_FALLBACK': '등록된 과학적 HOLD (솔버 띠 규칙이 L0 아님 · BAND_FALLBACK) — 값 없음',
    'EMPTY_NO_REASON': '텍스트 칸의 빈칸 = 사유 없음 (빈 집합) — hold_reason_codes (적격성 OK 행) · ion_net_status_reason (NOT_COMPUTED 가 아닌 행)',
}
V13_ML_SUFFIX = '__blank'
V13_ML_CLASS = 'ion_percolates_hertz'
_V13_PHASE_TOKEN = re.compile(r'(?<![A-Za-z0-9])AM_([PS])(?![A-Za-z0-9])')
_V13_PHASE_SPECIAL = {'d_am_p_um': {'AM_P'}, 'd_am_s_um': {'AM_S'}, 'size_ratio_P_over_S': {'AM_P', 'AM_S'}}
_V13_BLOCK_PHASES = {'bimodal': {'AM_P', 'AM_S'}, 'mono_AM_P': {'AM_P'}, 'mono_AM_S': {'AM_S'}}
_V13_NONPERC_COLS = ('se_se_cn_perc', 'se_se_cn_n_perc', 'se_se_cn_eff_area_perc', 'tortuosity_SE_wall', 'tortuosity_SE_wall_median')
_V13_FRAC_RE = re.compile(r'fracture_index_force|n_total_AM_AM_force|frac_[a-z]+_force_pct|n_[a-z]+_force_AM_AM')
_V13_TAU_VALUE_RE = re.compile(r'(f_ion|tau2_ion|tau_ion)_(hertz_h12|hertz|physics)')
_V13_TAU_REASON_RE = re.compile(r'ion_net_status_reason_(hertz_h12|hertz|physics)')
_V13_VALUE_STATUSES = ('OK', 'MODEL_BELOW_CONTINUUM_BOUND')

#: ML 열 역할 (닫힌 표 — v1.1 README §2 · v1.2 §2 · Codex 5차 QV2 · QV3).  여기 없는 열은 v1.2 주 표 열 목록 (Y) 이거나 거부.
V13_ROLE_FIXED = {
    'case_id': 'ID', 'dataset': 'DATASET', V13_ML_CLASS: 'Y_CLASS',
    'am_pct': 'X', 'ps_frac': 'X', 'd_am_p_um': 'X', 'd_am_s_um': 'X', 'd_se_um': 'X',
    'block': 'X_DERIVED', 'ps_label': 'X_DERIVED', 'r_AM_P_um': 'X_DERIVED', 'r_AM_S_um': 'X_DERIVED', 'r_SE_um': 'X_DERIVED',
    'size_ratio_P_over_S': 'X_DERIVED', 'size_ratio_AM_over_SE': 'X_DERIVED',
    'loading_mAh_cm2': 'CONST', 'pressure_MPa': 'CONST', 'e_se_gpa': 'CONST', 'rve_um': 'CONST',
    'ion_sigma0_mScm': 'CONST', 'ion_sigma0_T_C': 'CONST', 'phi_basis': 'CONST', 'L_basis': 'CONST', 'ion_net_generation': 'CONST',
    'ion_net_constriction_hertz': 'CONST', 'ion_net_area_rule_hertz': 'CONST', 'ion_net_electrode_hertz': 'CONST', 'ion_net_bulk_hertz': 'CONST',
    'press_target_mpa': 'CONST', 'press_reached': 'CONST', 'press_last_loop_mpa': 'DIAG',
    'physical_target_status': 'FLAG', 'hold_reason_codes': 'FLAG', 'boundary_state': 'FLAG',
    'ion_net_status_hertz': 'STATUS', 'ion_net_status_reason_hertz': 'STATUS',
    'n_AM_P_measured': 'RESULT_COUNT', 'n_AM_S_measured': 'RESULT_COUNT', 'n_SE_measured': 'RESULT_COUNT',
    'f_ion_hertz': 'Y_TARGET', 'tau2_ion_hertz': 'Y_IDENTITY', 'tau_ion_hertz': 'Y_IDENTITY', 'se_isolated_pct': 'Y',
}
V13_ROLE_MEANING = {
    'ID': '키 — 특징 금지',
    'DATASET': '데이터셋 표지 (lhs = 130 · lhsx = 64 · 전부 SE-rich — 분포가 다르다 · 섞을 때 함께 둔다)',
    'X': '자유 설계 노브 — 설계 → 구조 예측의 입력',
    'X_DERIVED': '설계의 재표현 — 같은 정보 (넣어도 독립 정보가 늘지 않는다)',
    'CONST': '194 행 상수 (규약 · 세대 · 목표압) — 특징 · 타깃 금지',
    'DIAG': '진단 기록 — 특징 · 타깃 아님',
    'FLAG': '적격성 표지 — 특징 금지 (물리 타깃 적격성 · HOLD 포함/제외 민감도 구분)',
    'STATUS': '수송 지표 상태 — 값과 반드시 같이 읽는다 (특징 아님 · Codex 5차 QV2)',
    'RESULT_COUNT': '실측 입자 수 (시뮬레이션 결과) — 설계 → 구조 예측의 X 로 쓰면 누설',
    'Y': '구조 결과 — 타깃 후보 (항등식으로 묶인 열은 한 묶음에서 하나만 독립)',
    'Y_TARGET': '이온 수송 1차 타깃 (#2 — f · 유한 · 비관통 = 0.0)',
    'Y_IDENTITY': '항등식 유도 (T = φ_SE,mc/f · √T) — f 와 같이 타깃 · 특징으로 쓰지 않는다',
    'Y_CLASS': '관통 분류 타깃 (#2 — 1 = 관통 · 0 = 비관통)',
    'BLANK_CODE': '바로 왼쪽 열의 빈칸 뜻 (코드 · 값이 있으면 빈칸) — 결측 표지로만',
}

#: #5 재적합 — 등록식 (σ_ionic T1 의 porosity · CN 부분 · CLAUDE.md "σ_ionic form FINALIZED") 의 동결 상수는 생산 코드에서 읽는다 (사본 금지)
REFIT_SCHEMA = 'lhs_v13_refit_porosity_sigma_cn/v1'
REFIT_FIT_STATUSES = ('OK', 'MODEL_BELOW_CONTINUUM_BOUND')
REFIT_SKIP_STATUSES = ('NOT_PERCOLATING', 'NOT_COMPUTED', 'BAND_FALLBACK')
REFIT_NEEDS = ('ion_net_status_hertz', 'f_ion_hertz', 'phi_se_mass_conserving', 'porosity_union_exact_pct', 'se_se_cn', 'ps_frac',
               'r_AM_S_um', 'r_AM_P_um')
REFIT_MIN_ROWS = 5
REFIT_ROW_COLS = ('dataset', 'case_id', 'ion_net_status_hertz', 'included', 'excluded_reason', 'porosity_union_exact_pct',
                  'phi_se_mass_conserving', 'se_se_cn', 'f_ion_hertz', 'g_phys', 'phi_c_eff', 'phi_eff', 'x_collapse', 'ln_f',
                  'ln_f_locked', 'resid_locked', 'ln_f_free', 'resid_free')
REFIT_STEM = 'lhs_v13_refit_porosity_sigma_cn'
V13_MANIFEST_SCHEMA = 'lhs_release_v13_build/v2'      # v2 (10-07 G2RR3-01) = batch_gate (관문 결과 · 모드 · 배치 뿌리) · diagnostic · 판정 필드 기록
V13_MANIFEST_NAME = 'v13_build_manifest.json'
_V13_FLOAT_RTOL = 1e-9


def _ldd():
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    import lhs_design_dataset as LDD                                     # noqa: E402 — 열 사전 · 관문 · τ 원천의 정본
    return LDD


def _tf():
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    import tau_flux as TF                                                # noqa: E402 — 세대 계약의 정본
    return TF


def _gcp():
    """σ_ionic 등록식의 동결 상수 · 크기 게이트 (generate_comparison_plots — 생산 코드 · 사본 금지).  matplotlib 을 끌어오므로 재적합 때만."""
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    import generate_comparison_plots as G                                # noqa: E402
    return G


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _v13_num(v):
    if v in (None, ''):
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _v13_rel(path):
    """리포 안이면 상대 경로 · 아니면 이름만 (사용자 홈 경로를 산출에 새기지 않는다)."""
    p = os.path.abspath(path)
    try:
        r = os.path.relpath(p, REPO)
    except ValueError:
        return os.path.basename(p)
    return os.path.basename(p) if r.startswith('..') else r


@functools.lru_cache(maxsize=None)
def _v13_tsv_cols(rel):
    _, rows = _read_tsv(os.path.join(REPO, rel))
    return tuple(r[0] for r in rows)


def v13_columns(dataset, kind='main', press=True):
    """v1.3 열 명세 — main = v1.2 주 표 열 (순서 그대로) + V13_MAIN_ADD + (완료 압력 V13_PRESS_ADD) · physics = v1.2 부록 + 세대 2 표기 ·
    h12 = 민감도 부록 (선택).  H12 · physics 값 열은 주 표에 들어가지 않는다."""
    if dataset not in V13_DATASETS:
        raise ReleaseError(f'모르는 데이터셋 {dataset!r} (아는 것: {V13_DATASETS})')
    if kind == 'main':
        cols = list(_v13_tsv_cols(V13_BASE_FROM[dataset])) + list(V13_MAIN_ADD) + (list(V13_PRESS_ADD) if press else [])
    elif kind == 'physics':
        cols = list(_v13_tsv_cols(V13_PHYSICS_BASE_FROM[dataset])) + list(V13_PHYSICS_ADD)
    elif kind == 'h12':
        cols = list(V13_H12_COLUMNS)
    else:
        raise ReleaseError(f'모르는 표 종류 {kind!r} (main · physics · h12)')
    if len(set(cols)) != len(cols) or cols[0] != KEY:
        raise ReleaseError(f'{dataset} {kind} 열 명세 — 중복이 있거나 첫 열이 {KEY} 가 아니다')
    return cols


@functools.lru_cache(maxsize=None)
def _v13_y_set():
    s = set()
    for ds in V13_DATASETS:
        s.update(_v13_tsv_cols(V13_BASE_FROM[ds]))
    return frozenset(c for c in s if c not in V13_ROLE_FIXED)


def v13_role(col):
    """ML 열 역할 (닫힌 표) — 모르는 열은 ReleaseError (기본 역할로 흘리지 않는다)."""
    if col.endswith(V13_ML_SUFFIX):
        v13_role(col[:-len(V13_ML_SUFFIX)])
        return 'BLANK_CODE'
    if col in V13_ROLE_FIXED:
        return V13_ROLE_FIXED[col]
    if col in _v13_y_set():
        return 'Y'
    raise ReleaseError(f'열 {col!r} 의 ML 역할을 모른다 — V13_ROLE_FIXED 또는 v1.2 주 표 열 목록에 있어야 한다 (기본 역할로 흘리지 않는다)')


def _v13_phases(col):
    if col in _V13_PHASE_SPECIAL:
        return _V13_PHASE_SPECIAL[col]
    return {'AM_' + m for m in _V13_PHASE_TOKEN.findall(col)}


def v13_blank_reason(row, col):
    """그 행 · 그 열의 칸이 **빈칸이어야 하는** 뜻 (V13_BLANK_CODES 의 코드) · 값이어야 하면 None.  규칙은 같은 행의 설계 block · 개수 · 상태가 정한다."""
    ph = _v13_phases(col)
    if ph:
        have = _V13_BLOCK_PHASES.get(row.get('block'))
        if have is None:
            raise ReleaseError(f'{row.get(KEY)}: 설계 block {row.get("block")!r} 을 모른다 — 상 부재를 가를 수 없다')
        if ph - have:
            return 'NA_PHASE_ABSENT'
    m = re.fullmatch(r'(area_.+)_mean', col)
    if m and _v13_num(row.get(m.group(1) + '_n')) == 0:
        return 'NA_ZERO_CONTACTS'
    if (col == 'am_am_mean_area' or _V13_FRAC_RE.fullmatch(col)) and _v13_num(row.get('am_am_n_contacts')) == 0:
        return 'NA_ZERO_CONTACTS'
    if col in _V13_NONPERC_COLS and _v13_num(row.get('percolation_pct')) == 0:
        return 'NA_NOT_PERCOLATING'
    m = _V13_TAU_VALUE_RE.fullmatch(col)
    if m:
        st = row.get(f'ion_net_status_{m.group(2)}', '')
        if st == 'NOT_PERCOLATING':
            return None if m.group(1) == 'f_ion' else 'INF_NOT_PERCOLATING'
        if st == 'NOT_COMPUTED':
            return 'NOT_COMPUTED'
        if st == 'BAND_FALLBACK':
            return 'HOLD_BAND_FALLBACK'
        return None
    m = _V13_TAU_REASON_RE.fullmatch(col)
    if m:
        return None if row.get(f'ion_net_status_{m.group(1)}') == 'NOT_COMPUTED' else 'EMPTY_NO_REASON'
    if col == 'hold_reason_codes':
        return 'EMPTY_NO_REASON' if row.get('physical_target_status') == 'OK' else None
    return None


def v13_blank_problems(rows, cols):
    """빈칸 일관성 (양방향) — 문제 목록 ([] = 통과): 규칙에 없는 빈칸 · 빈칸이어야 할 칸의 값 · 상태 ↔ f 모순 (NOT_PERCOLATING 이면 f = 0 ·
    OK · MBCB 이면 f > 0)."""
    probs = []
    for r in rows:
        case = r.get(KEY, '?')
        for c in cols:
            if c == KEY:
                continue
            try:
                want = v13_blank_reason(r, c)
            except ReleaseError as e:
                probs.append(str(e))
                continue
            v = r.get(c, '')
            if want is None and v == '':
                probs.append(f'{case} · {c}: 설명 안 되는 빈칸 (빈칸 뜻 규칙에 없다 — 추측으로 코드를 달지 않는다)')
            elif want is not None and v != '':
                probs.append(f'{case} · {c}: 값 {v!r} 이 있는데 빈칸 ({want}) 이어야 한다')
        for c in cols:
            m = _V13_TAU_VALUE_RE.fullmatch(c)
            if not m or m.group(1) != 'f_ion' or r.get(c, '') == '':
                continue
            st, fv = r.get(f'ion_net_status_{m.group(2)}', ''), _v13_num(r.get(c))
            if st == 'NOT_PERCOLATING' and fv != 0.0:
                probs.append(f'{case} · {c}: 상태 NOT_PERCOLATING 인데 f = {r.get(c)!r} (0.0 이어야 — 물리적 0)')
            elif st in _V13_VALUE_STATUSES and not (fv is not None and fv > 0.0):
                probs.append(f'{case} · {c}: 상태 {st} 인데 f = {r.get(c)!r} (유한 양수여야)')
    return probs


def _v13_class(r):
    """관통 분류 (#2) — ('1' | '0' | '', 코드).  percolation_pct 가 있으면 관통 판정과 같아야 (tau_flux G2)."""
    st = r.get('ion_net_status_hertz', '')
    if st in _V13_VALUE_STATUSES:
        v, code = '1', ''
    elif st == 'NOT_PERCOLATING':
        v, code = '0', ''
    elif st == 'NOT_COMPUTED':
        v, code = '', 'NOT_COMPUTED'
    elif st == 'BAND_FALLBACK':
        v, code = '', 'HOLD_BAND_FALLBACK'
    else:
        raise ReleaseError(f'{r.get(KEY)}: ion_net_status_hertz {st!r} — 모르는 상태 (관통 분류를 정할 수 없다)')
    pp = _v13_num(r.get('percolation_pct'))
    if v and pp is not None and (pp > 0.0) != (v == '1'):
        raise ReleaseError(f'{r.get(KEY)}: 관통 분류 {v} ↔ percolation_pct {pp!r} 모순 (tau_flux G2 — 솔버 관통 = 그래프 관통)')
    return v, code


def v13_ml_table(by_ds):
    """#1 ML 표 — {데이터셋: (배포 열, 배포 행)} → ({데이터셋: (ML 열, ML 행)}, ML 열 사전 행 [dataset 키 포함]).
    값 칸은 배포 그대로 (채우지 않는다) · 빈칸이 있는 열 (두 데이터셋 합집합) 뒤에 `<열>__blank` (코드 · 값이 있으면 빈칸) · 둘째 열 dataset ·
    끝 열 ion_percolates_hertz (관통 분류).  빈칸 뜻을 정할 수 없는 칸이 하나라도 있으면 거부."""
    for ds, (cols, rows) in by_ds.items():
        p = v13_blank_problems(rows, cols)
        if p:
            raise ReleaseError(f'{ds}: 빈칸 뜻을 정할 수 없는 칸 {len(p)} — ML 표를 만들지 않는다: ' + ' | '.join(p[:4]))
        for c in cols:
            v13_role(c)
    blank_cols = {c for _ds, (cols, rows) in by_ds.items() for c in cols if c != KEY and any(r.get(c, '') == '' for r in rows)}
    tables = {}
    for ds, (cols, rows) in by_ds.items():
        mcols = [KEY, 'dataset']
        for c in cols:
            if c == KEY:
                continue
            mcols.append(c)
            if c in blank_cols:
                mcols.append(c + V13_ML_SUFFIX)
        mcols.append(V13_ML_CLASS)
        out = []
        for r in rows:
            o = {KEY: r[KEY], 'dataset': ds}
            for c in cols:
                if c == KEY:
                    continue
                o[c] = r.get(c, '')
                if c in blank_cols:
                    o[c + V13_ML_SUFFIX] = (v13_blank_reason(r, c) or '') if o[c] == '' else ''
            o[V13_ML_CLASS], code = _v13_class(r)
            if code:
                o[V13_ML_CLASS + V13_ML_SUFFIX] = code
            out.append(o)
        tables[ds] = (mcols, out)
    if any(V13_ML_CLASS + V13_ML_SUFFIX in o for _mc, out in tables.values() for o in out):
        for ds, (mc, out) in tables.items():
            mc.append(V13_ML_CLASS + V13_ML_SUFFIX)
            for o in out:
                o.setdefault(V13_ML_CLASS + V13_ML_SUFFIX, '')
    drows = []
    for ds, (mc, out) in tables.items():
        for c in mc:
            role = v13_role(c)
            src = c[:-len(V13_ML_SUFFIX)] if c.endswith(V13_ML_SUFFIX) else c
            cc = c if c.endswith(V13_ML_SUFFIX) else c + V13_ML_SUFFIX
            cnt = collections.Counter(o.get(cc) for o in out if o.get(cc)) if cc in mc else collections.Counter()
            if role == 'BLANK_CODE':
                meaning = f'{src} 의 빈칸 뜻 (값이 있으면 빈칸) — 코드: ' + ' · '.join(f'{k} = {V13_BLANK_CODES[k]}' for k in sorted(cnt))
            elif c == KEY:
                meaning = '설계 ID (키)'
            elif c == 'dataset':
                meaning = V13_ROLE_MEANING['DATASET']
            elif c == V13_ML_CLASS:
                meaning = ('관통 분류 (#2) — 1 = 관통 (ion_net_status_hertz OK · MODEL_BELOW_CONTINUUM_BOUND) · 0 = 비관통 (NOT_PERCOLATING — f = 0 · '
                           'T = ∞) · 빈칸 = 기술 실패 · HOLD (코드 열) · percolation_pct > 0 과 같은 판정 (관문)')
            else:
                meaning = f'배포 열 사전 (같은 이름) · 역할 = {V13_ROLE_MEANING[role]}'
            drows.append({'dataset': ds, 'column': c, 'role': role, 'source_column': src,
                          'blank_codes': ' · '.join(f'{k}:{n}' for k, n in sorted(cnt.items())), 'meaning': meaning})
    return tables, drows


def v13_ml_decode(mcols, mrows):
    """ML 표 → (배포 열, 배포 행) — dataset · 코드 열 · 관통 분류 열을 뺀다 (되읽기 검산)."""
    cols = [c for c in mcols if c != 'dataset' and not c.endswith(V13_ML_SUFFIX) and c != V13_ML_CLASS]
    return cols, [{c: r.get(c, '') for c in cols} for r in mrows]


def v13_se_isolated_problems(rows):
    """se_isolated_pct = 100 − top_reachable_pct · ≤ 100 − percolation_pct (생성기 관문 S1 · S2 를 그대로 다시 부른다 — 사본 금지)."""
    LDD = _ldd()
    probs = []
    for r in rows:
        if 'se_isolated_pct' not in r:
            probs.append(f'{r.get(KEY)}: se_isolated_pct 열이 없다')
            continue
        try:
            n = LDD._se_iso_gates(r.get(KEY), r)
        except LDD.FillRefusal as e:
            probs.append(str(e))
            continue
        if n == 0:
            probs.append(f'{r.get(KEY)}: se_isolated_pct · top_reachable_pct 가 둘 다 빈칸 — 배포 행은 값이 있어야 한다')
    return probs


def v13_generation_problems(rows, dry_run=False):
    """인계표 행의 망 세대 → (세대, 문제).  행마다 공용 세대 계약 (tau_flux.row_generation_problems) → 섞임 (generation_mixing_problem) →
    v1.3 = g2 만 (dry-run 이면 세대를 기록만 하고 통과 · 섞임 · 계약 위반은 dry-run 이어도 문제)."""
    TF = _tf()
    probs, gens = [], set()
    for r in rows:
        g, pp = TF.row_generation_problems(r)
        if pp:
            probs.append(f'{r.get(KEY)}: 세대 계약 위반 ({g or "?"}) — {pp[0]}' + (f' 외 {len(pp) - 1}' if len(pp) > 1 else ''))
        elif not g:
            probs.append(f'{r.get(KEY)}: τ 표기가 없다 (망 레코드 없음) — 배포 행은 망 세대가 정해져야 한다')
        gens.add(g)
    if not probs:
        mix = TF.generation_mixing_problem([dict(r, case=r.get(KEY)) for r in rows])
        if mix:
            probs.append(mix)
    gens.discard('')
    gen = next(iter(gens)) if len(gens) == 1 else ('mixed' if gens else '')
    if not probs and gen != V13_GENERATION and not dry_run:
        probs.append(f'망 세대 {gen!r} — v1.3 (최종판) 은 세대 2 ({V13_GENERATION}) 값만 싣는다 (세대 1 원천은 --dry-run 으로만)')
    return gen, probs


def v13_manifest_generation(manifest):
    """배치 manifest 의 기대 세대 (생성기 `tau_manifest_expected_generation` — 같은 함수) = g2 여야 한다."""
    LDD = _ldd()
    try:
        g = LDD.tau_manifest_expected_generation(manifest)
    except LDD.FillRefusal as e:
        raise ReleaseError(f'배치 manifest — {e}') from None
    if g != V13_GENERATION:
        raise ReleaseError(f'배치 manifest 기대 세대 {g!r} ≠ {V13_GENERATION} — v1.3 (최종판) 은 세대 2 배치만 싣는다')
    return g


def v13_manifest_inputs_problems(manifest):
    """배치 manifest plan.cohorts (수확 · union · 설계) ↔ V13_INPUTS — 다른 원천으로 돈 배치를 v1.3 입력과 섞지 않는다."""
    try:
        m = manifest if isinstance(manifest, dict) else json.load(open(manifest, encoding='utf-8'))
    except (OSError, ValueError) as e:
        return [f'배치 manifest 를 못 읽었다 ({type(e).__name__})']
    co = {c.get('name'): c for c in ((m.get('plan') or {}).get('cohorts') or []) if isinstance(c, dict)}
    probs = []
    for ds in V13_DATASETS:
        c, inp = co.get(ds), V13_INPUTS[ds]
        if c is None:
            probs.append(f'manifest plan.cohorts 에 {ds} 가 없다')
            continue
        if os.path.basename(str(c.get('harvest_dir') or '').rstrip('/')) != os.path.basename(inp['harvest']):
            probs.append(f'{ds}: 배치 수확 {c.get("harvest_dir")!r} ≠ v1.3 입력 {inp["harvest"]}')
        if (c.get('union') or '') != inp['union']:
            probs.append(f'{ds}: 배치 union {c.get("union")!r} ≠ {inp["union"]}')
        if (c.get('design') or '') != inp['design']:
            probs.append(f'{ds}: 배치 설계 {c.get("design")!r} ≠ {inp["design"]!r}')
    return probs


#: ⓪ 봉인 감사 · ⓪b 게시 다시 읽기 기록 — 194 실행기 후속 명령이 배치 뿌리에 쓰는 이름 (세대 2 등록 `lhs_network_batch_registration_20261007_g2.md` §5-2 · §5-3).
#:   ★ 10-07 G2RR3-01 (Codex 세대 2 재검증 3 §3) — 옛 판은 감사 기록의 sha256 만 적고 판정을 읽지 않았고, 다시 읽기 기록이 없거나 · 깨졌거나 · 필드가 비면
#:   경고만 하고 만들었다 (= 기록을 못 읽으면 더 적게 검사 — 실제 build_v13 이 21 파일 묶음을 만들고 check_v13 문제 0).  이제 실제 배포는 두 기록이 **필수**이고
#:   내용을 판정한다 (`v13_batch_gate_problems` — build_v13 · 단계 A · check_v13 이 같은 함수) · 이 배치 뿌리 · 이 manifest · 이 발사 봉인 지문의 증거여야 한다.
#:   옛 · 부분 · 실패 기록은 진단 모드 (`--diagnostic-batch-gate` · README · 빌드 manifest 에 NOT FOR RELEASE · 리포 밖 · check_v13 배포 대조 거부) 에서만 만든다.
V13_BATCH_GATE_FILES = ('seal_audit.json', 'reread.json')
V13_REREAD_SET = 'production194'          # ★ 10-07 G2RR2-02 — ⓪b 다시 읽기의 등록 집합 (g2_network_reread --expect-set production194)
V13_REREAD_N = 194                         #   그 집합의 고정 크기 (run_network_194_parallel.REGISTERED_ID_SETS — 시험이 대조)
#: ★ 10-07 G2RR3-01 — 생산 배포가 받는 봉인 판정 = **SEALED 만** (세대 2 등록 §5-2 "기록 전부 SEALED").  실행기 audit 의 rc 0 은 SEAL_OK 셋을 받지만
#:   배포는 좁다: SEALED_DIRTY_ALLOWED (추적 파일이 바뀐 트리에서 --allow-dirty 로 돈 시도 — 봉인 코드 해시는 같아도 등록 §1 "봉인 커밋 · dirty 0" 밖) ·
#:   SEALED_LEGACY (역사 형식 = 이 배포가 아니다) 는 받지 않는다 — 그런 배치를 싣는 판단이 필요하면 진단 모드로 기록만 하고 1저자 결정 (새 등록) 으로.
V13_AUDIT_SEALED = ('SEALED',)
#: ★ 10-07 G2RR4-01 ③ · G2RR4-03 (Codex 세대 2 재검증 4 §2 · §4 Q3) — 이 등록 집합의 배포 = **import 관측을 켠 실행만** (등록 §4 본 실행 `run --observe-imports` ·
#:   실행기 run 이 생산 계획에 강제).  배치 manifest observe_imports true · 감사 기록에 관측 객체 · 관측된 완료 시도가 등록 케이스 전부 — 관측 결손을 정상으로 받지 않는다.
V13_IMPORT_OBS_REQUIRED = ('production194',)
V13_GATE_SCHEMA = 'lhs_release_v13_batch_gate/v1'        # 빌드 manifest batch_gate (모드 · 배치 뿌리 · manifest sha256 · 문제)
V13_DIAG_BANNER = 'NOT FOR RELEASE — diagnostic build (batch gate evidence not accepted)'
_V13_HEX64 = re.compile(r'[0-9a-f]{64}')
#: 빌드 manifest 에 남기는 기록 필드 (check_v13 이 지금 배치 뿌리에서 다시 만든 기록과 맞댄다 — 기록 ≠ 지금 = 문제)
_V13_REREAD_REC_KEYS = ('schema', 'n_fail', 'expected_generation', 'expected_set', 'expected_n', 'read_n', 'set_equal', 'launcher_root',
                        'manifest_sha256', 'seal_fp', 'launch_sha')
_V13_AUDIT_REC_KEYS = ('schema', 'root', 'seal_fp', 'launch_sha', 'refused', 'verdicts', 'merged', 'expected_network_generation')


def _sha256_or_none(path):
    try:
        return _sha256(path)
    except OSError:
        return None


def _v13_git(*args):
    """이 체크아웃 (REPO) 의 git 출력 한 덩이 — git 이 없거나 실패하면 None (기록만 · 판정에 쓰지 않는다)."""
    try:
        r = subprocess.run(['git', '-C', REPO, *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def v13_seal_drift(manifest):
    """배치 manifest 의 발사 봉인 코드 지문 (`code_hashes` — 194 실행기가 워커 체크아웃에서 잰 값 · 10-05 판부터 있는 키) ↔ 이 체크아웃의 같은 파일.

    인계 생성기 (단계 A) 의 τ 출처 관문 P4 · 배포 때 τ 다시 읽기는 **이 체크아웃의** tau_flux · pipeline_service 를 부른다 — 봉인 파일이 발사 때와
    다르면 배치와 다른 코드로 τ 를 읽는다.  반환 dict:
      sealed (봉인 파일 수) · sealed_changed (지금 지문 ≠ 기록 · 파일이 없거나 · 리포 밖 경로 (절대 · ..) · 빈 기록 = 다름 · 정렬) ·
      handover · handover_changed (`handover_code_hashes` — 10-07 실행기부터 · 없으면 None = 모름) · git_head · git_dirty_tracked (기록만).
    code_hashes 가 없거나 비었으면 ReleaseError (194 실행기 manifest 가 아니다 — 무엇과 대조할지 모른다)."""
    try:
        m = manifest if isinstance(manifest, dict) else json.load(open(manifest, encoding='utf-8'))
    except (OSError, ValueError) as e:
        raise ReleaseError(f'배치 manifest 를 못 읽었다 ({type(e).__name__})') from None
    ch = m.get('code_hashes')
    if not isinstance(ch, dict) or not ch:
        raise ReleaseError('배치 manifest 에 발사 봉인 코드 지문 (code_hashes) 이 없다 — 194 실행기 manifest 가 아니다 (무엇과 대조할지 모른다)')

    def changed(d):
        out = []
        for rel, h in d.items():
            r = str(rel)
            if os.path.isabs(r) or '..' in r.replace('\\', '/').split('/') or not h or _sha256_or_none(os.path.join(REPO, r)) != h:
                out.append(r)
        return sorted(out)
    hh = m.get('handover_code_hashes')
    dirty = _v13_git('status', '--porcelain', '--untracked-files=no')
    return {'sealed': len(ch), 'sealed_changed': changed(ch),
            'handover': len(hh) if isinstance(hh, dict) else None,
            'handover_changed': changed(hh) if isinstance(hh, dict) else None,
            'git_head': _v13_git('rev-parse', 'HEAD'),
            'git_dirty_tracked': (len([ln for ln in dirty.splitlines() if ln.strip()]) if dirty is not None else None)}


def v13_seal_gate(manifest, allow_seal_diff=None):
    """발사 봉인 관문 — 봉인 파일이 다르면 거부 (값과 무관한 변경 = --allow-seal-diff <파일> 명시 승인 · 기록).  반환 (code_identity dict, 경고 목록).
    인계 도구 (handover_code_hashes) 다름 = 경고 (등록 §3 ⚠ — v1.3 생성기 변경은 예상된 일 · 그 커밋을 등록 §9 에 적는다) · 쓰이지 않은 승인 = 경고."""
    d = v13_seal_drift(manifest)
    #  승인 철자 정규화 ('./webapp/app.py' · 'webapp\\app.py' = manifest 키 'webapp/app.py') — 리포 밖 · 절대 경로는 그대로 (어떤 키와도 안 맞는다)
    allow = sorted({os.path.normpath(str(x).replace('\\', '/')).replace(os.sep, '/') for x in (allow_seal_diff or ()) if str(x).strip()})
    bad = [f for f in d['sealed_changed'] if f not in allow]
    if bad:
        raise ReleaseError(f'발사 봉인 파일 {len(bad)} 이 이 체크아웃과 다르다 {bad[:6]} — 인계 생성기 τ 출처 관문 (P4) · 배포 τ 다시 읽기가 배치와 다른 코드로 돈다.  '
                           '발사 체크아웃 (봉인 파일이 같은 커밋) 에서 만들거나, 값과 무관한 변경 (예: 웹앱 화면 문구) 이면 --allow-seal-diff <파일> 로 명시 승인 '
                           '(README · 빌드 manifest 에 기록)')
    warns = []
    unused = [f for f in allow if f not in d['sealed_changed']]
    if unused:
        warns.append(f'--allow-seal-diff {unused} — 발사 기록과 같은 파일 (또는 봉인 밖 파일) 이라 쓰이지 않은 승인')
    if d['handover_changed']:
        warns.append(f'인계 생성기 · 다시 읽기 도구 지문 ≠ 발사 기록 (handover_code_hashes) {d["handover_changed"]} — v1.3 생성기 변경 '
                     f'(세대 2 등록 §3 ⚠ "그 커밋을 §9 에 적는다") · 이 빌드 git HEAD = {d["git_head"]}')
    elif d['handover_changed'] is None:
        warns.append('배치 manifest 에 handover_code_hashes 가 없다 — 인계 도구 지문 대조 못 함 (10-07 전 실행기)')
    if d['git_dirty_tracked']:
        warns.append(f'이 체크아웃에 커밋 안 된 추적 파일 변경 {d["git_dirty_tracked"]} 줄 — 빌드 코드 신원 = git HEAD + 빌드 manifest code 지문')
    return dict(d, allowed=[f for f in allow if f in d['sealed_changed']]), warns


def _np194():
    """194 실행기 모듈 — 발사 봉인 지문 `code_fp` · 등록 집합 `REGISTERED_ID_SETS` · `ids_digest` · 감사 스키마 `LAUNCH_SEAL_SCHEMA` (정본 · 사본 금지)."""
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    import run_network_194_parallel as NP                                # noqa: E402
    return NP


def _g2rr():
    """세대 2 다시 읽기 도구 — 기록 스키마 `SCHEMA` (정본)."""
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    import g2_network_reread as RR                                       # noqa: E402
    return RR


def _v13_same_path(a, b):
    """두 경로가 같은 곳인가 (realpath · normcase — 기록된 문자열 철자가 아니라 위치를 맞댄다)."""
    return os.path.normcase(os.path.realpath(str(a))) == os.path.normcase(os.path.realpath(str(b)))


def _v13_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _v13_registered(expect_set):
    """등록 집합 이름 → (수, ids 지문) — 실행기 표 (production194 = 등록 지문 · pilot3 = 세 쌍에서 잰 지문)."""
    NP = _np194()
    reg = NP.REGISTERED_ID_SETS.get(expect_set)
    if reg is None:
        raise ReleaseError(f'모르는 등록 집합 {expect_set!r} — {sorted(NP.REGISTERED_ID_SETS)}')
    if 'ids_sha256' in reg:
        return reg['n'], reg['ids_sha256']
    return len(reg['pairs']), NP.ids_digest(reg['pairs'])


def _v13_gate_load(path):
    """관문 기록 하나를 **한 번** 읽는다 → (sha256 | None, 값, 사유).  사유 = 'absent' (없음) · 'invalid (…)' (못 읽음 · 깨진 JSON) · '' (읽었다) —
    기록 (sha256) 과 판정 (값) 이 같은 바이트에서 나온다."""
    if not os.path.isfile(path):
        return None, None, 'absent'
    try:
        with open(path, 'rb') as f:
            raw = f.read()
    except OSError as e:
        return None, None, f'invalid ({type(e).__name__})'
    sha = hashlib.sha256(raw).hexdigest()
    try:
        return sha, json.loads(raw.decode('utf-8')), ''
    except ValueError as e:                                              # UnicodeDecodeError · JSONDecodeError
        return sha, None, f'invalid ({type(e).__name__})'


def v13_batch_identity(batch_root):
    """배치 뿌리의 실행 신원 → (dict(root, manifest_sha256, seal_fp, launch_sha), 문제 목록).  관문 기록 둘이 결합돼야 할 대상:
    root = realpath · manifest_sha256 = 지금 manifest 바이트 · seal_fp = manifest seal.code_fp (= code_hashes 의 지문 `code_fp` 이어야 — 아니면 봉인이 자기
    해시 지도와 어긋난다) · launch_sha = manifest git.sha.  못 정한 값은 None (그 결합 대조는 건너뛰고 문제는 여기서 낸다)."""
    mp = os.path.join(batch_root, 'manifest.json')
    sha, man, why = _v13_gate_load(mp)
    ident = {'root': os.path.realpath(str(batch_root)), 'manifest_sha256': sha, 'seal_fp': None, 'launch_sha': None, 'observe_imports': None}
    if why or not isinstance(man, dict):
        return ident, [f'배치 manifest {mp} 를 못 읽었다 ({why or type(man).__name__}) — 실행 신원 (봉인 지문 · 발사 sha) 을 모른다']
    ident['observe_imports'] = man.get('observe_imports')        # ★ G2RR4-03 — 관측을 켠 실행인가 (감사 관측 판정 `v13_audit_observation_problems` 이 본다)
    probs = []
    s = man.get('seal') if isinstance(man.get('seal'), dict) else {}
    fp = s.get('code_fp')
    if not (isinstance(fp, str) and _V13_HEX64.fullmatch(fp)):
        probs.append(f'배치 manifest seal.code_fp {fp!r} — 발사 봉인 지문이 없다 (194 실행기 v3 manifest 가 아니다)')
    elif _np194().code_fp(man.get('code_hashes')) != fp:
        probs.append(f'배치 manifest seal.code_fp {fp[:12]}… ≠ code_hashes 의 지문 {str(_np194().code_fp(man.get("code_hashes")))[:12]}… — '
                     '발사 봉인이 자기 해시 지도와 어긋난다')
    else:
        ident['seal_fp'] = fp
    g = man.get('git') if isinstance(man.get('git'), dict) else {}
    if isinstance(g.get('sha'), str) and g['sha']:
        ident['launch_sha'] = g['sha']
    else:
        probs.append(f'배치 manifest git.sha {g.get("sha")!r} — 발사 커밋 신원이 없다')
    return ident, probs


def _v13_bind_problems(rec, ident, root_key):
    """기록 ↔ 이 배치의 실행 신원 — 배치 뿌리 (위치) · 봉인 지문 · 발사 sha (+ 다시 읽기는 manifest sha256).  root_key = 기록의 배치 뿌리 필드 이름."""
    p = []
    rv = rec.get(root_key)
    if not isinstance(rv, str) or not rv:
        p.append(f'{root_key} {rv!r} — 어느 배치 뿌리의 기록인지 없다')
    elif not _v13_same_path(rv, ident['root']):
        p.append(f'{root_key} {rv!r} ≠ 이 배치 뿌리 {ident["root"]!r} — 다른 배치의 기록')
    for k in ('seal_fp', 'launch_sha') + (('manifest_sha256',) if root_key == 'launcher_root' else ()):
        if ident.get(k) and rec.get(k) != ident[k]:
            got = rec.get(k) if rec.get(k) is None else str(rec.get(k))[:16]
            p.append(f'{k} {got!r} ≠ 이 배치 {str(ident[k])[:16]!r}…' + (' — 기록 뒤 manifest 가 바뀌었거나 다른 배치' if k == 'manifest_sha256'
                                                                     else ' — 다른 발사 (봉인 · 커밋) 의 기록'))
    return p


def v13_audit_problems(a, batch_root, why='', ident=None, expect_set=V13_REREAD_SET):
    """⓪ 봉인 감사 기록 (`run_network_194_parallel.py audit --root <ROOT> --json <ROOT>/seal_audit.json` 의 dict) 판정 → 문제 목록 ([] = 통과).
    읽기 · 꼴 (스키마 = 실행기 `LAUNCH_SEAL_SCHEMA`#audit · refused 아님 · 실행 형식 자격 current · 문제 0) · 이 배치 (배치 뿌리 · 봉인 지문 · 발사 sha) ·
    판정 (봉인 판정 = V13_AUDIT_SEALED 만 · 합 = 등록 수 · merged = same 만 · 합 = 등록 수 · 요약 = 행에서 다시 센 값 · 행의 (케이스, 코호트) = 등록 집합 ID 지문 ·
    기대 세대 선언 g2 · generation / input / import 관측 문제 · code_root_changed_now 전부 **빈 목록**).  수치 허용치 · σ 조건은 두지 않는다
    (정직한 실패 행은 등록 §5-1 · 다시 읽기 M2 · 생성기 관문 소관)."""
    if why == 'absent':
        return ['없다 — 등록 §5-2 ⓪ 봉인 감사 (`run_network_194_parallel.py audit --root <ROOT> --json <ROOT>/seal_audit.json`) 를 먼저 · 실제 배포는 이 기록이 필수']
    if why:
        return [f'못 읽는다 ({why}) — 손상된 감사 기록을 받지 않는다']
    if not isinstance(a, dict):
        return [f'객체가 아니다 ({type(a).__name__}) — 감사 기록의 꼴이 아니다']
    NP = _np194()
    if ident is None:
        ident = v13_batch_identity(batch_root)[0]
    p = []
    sch = NP.LAUNCH_SEAL_SCHEMA + '#audit'
    if a.get('schema') != sch:
        p.append(f'schema {a.get("schema")!r} ≠ {sch!r} — 지금 실행기의 감사 기록이 아니다')
    if a.get('refused') not in (None, False):
        p.append(f'refused {a.get("refused")!r} — 실행기가 판정표 없이 감사를 거부했다')
    el = a.get('eligibility') if isinstance(a.get('eligibility'), dict) else {}
    if el.get('kind') != 'current' or el.get('problems'):
        p.append(f'실행 형식 자격 {el.get("kind")!r} (문제 {el.get("problems")!r:.200}) — current · 문제 0 이어야 (historical · invalid 는 생산 배포가 아니다)')
    p += _v13_bind_problems(a, ident, 'root')
    n_reg, ids_reg = _v13_registered(expect_set)
    v, m, rows = a.get('verdicts'), a.get('merged'), a.get('cases')
    for nm, d, ok_keys in (('verdicts', v, V13_AUDIT_SEALED), ('merged', m, ('same',))):
        if not isinstance(d, dict) or not all(_v13_int(x) for x in d.values()):
            p.append(f'{nm} {d!r:.200} — 정수 개수 dict 가 아니다')
            continue
        nz = {k: x for k, x in d.items() if x}
        bad = {k: x for k, x in nz.items() if k not in ok_keys}
        if bad:
            p.append(f'{nm} 에 {bad} — 생산 배포는 {"/".join(ok_keys)} 만 받는다'
                     + (' (UNSEALED · NO_RECORD · SEALED_DIRTY_ALLOWED · SEALED_LEGACY 거부 — 등록 §5-2 "기록 전부 SEALED")' if nm == 'verdicts'
                        else ' (differs · missing · not_merged · synthesized_failed = merged 가 케이스 폴더 기록과 다르거나 없다)'))
        if sum(nz.values()) != n_reg:
            p.append(f'{nm} 합 {sum(nz.values())} ≠ 등록 집합 {expect_set} {n_reg}')
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        p.append(f'cases (행) 가 목록이 아니다 ({type(rows).__name__})')
    else:
        pairs = [(r.get('case'), r.get('cohort')) for r in rows]
        if len(set(pairs)) != len(pairs) or len(pairs) != n_reg or NP.ids_digest(pairs) != ids_reg:
            p.append(f'행의 (케이스, 코호트) {len(pairs)} (고유 {len(set(pairs))}) ≠ 등록 집합 {expect_set} ({n_reg} · ID 지문 {ids_reg[:12]}…) — 다른 계획의 감사')
        for nm, col in (('verdicts', 'verdict'), ('merged', 'merged')):
            d = a.get(nm)
            if isinstance(d, dict) and dict(collections.Counter(r.get(col) for r in rows)) != {k: x for k, x in d.items() if x}:
                p.append(f'{nm} 요약 {d} ≠ 행에서 다시 센 값 {dict(collections.Counter(r.get(col) for r in rows))} — 요약 · 행이 어긋난 감사 기록')
    if a.get('generation_declared') is not True or a.get('expected_network_generation') != V13_GENERATION:
        p.append(f'기대 망 세대 선언 {a.get("generation_declared")!r} · {a.get("expected_network_generation")!r} — 선언된 {V13_GENERATION} 이어야')
    for k in ('generation_problems', 'input_problems', 'import_observation_problems', 'code_root_changed_now'):
        x = a.get(k)
        if not isinstance(x, list):
            p.append(f'{k} {x!r:.120} — 목록이 없다 (지금 실행기의 감사 기록이 아니다)')
        elif x:
            p.append(f'{k} {len(x)} — {x[:3]!r:.300} (빈 목록이어야)')
    p += v13_audit_observation_problems(a, ident, expect_set)
    return p


def v13_audit_observation_problems(a, ident, expect_set=V13_REREAD_SET):
    """★ 10-07 G2RR4-01 ③ · G2RR4-03 (Codex 세대 2 재검증 4 §2 · §4 Q3) — 감사 기록의 import 관측 객체 (`import_observation`) ↔ 최상위 요약
    (`import_observation_problems`) · 관측 필수 배치 (등록 집합 ∈ V13_IMPORT_OBS_REQUIRED) 의 관측 결손 → 문제 목록.
    옛 관문은 최상위 요약 목록만 봤다 — 관측 객체 안의 problems · outside 가 있어도 최상위 [] 면 통과 · 관측 객체가 없어도 · observe_imports false 여도 통과.
      · 객체가 있으면: dict · problems · outside = 목록 · 둘 다 빈 목록 · 그 내용이 최상위 요약에 다 실렸다 (요약이 상세를 덮지 않는다) · 프로세스 수 셋 = 정수
      · 관측 필수 배치: 배치 manifest observe_imports true · 객체 있음 · 프로세스 > 0 · 관측된 완료 시도 (케이스) ⊇ 등록 케이스 전부"""
    p = []
    req = expect_set in V13_IMPORT_OBS_REQUIRED
    oi = (ident or {}).get('observe_imports')
    if req and oi is not True:
        p.append(f'배치 manifest observe_imports {oi!r} — 등록 집합 {expect_set} 의 배포는 import 관측을 켠 실행만 (G2RR4-03 · 등록 §4 `run --observe-imports`)')
    io_ = a.get('import_observation')
    top = a.get('import_observation_problems')
    if io_ is None:
        if req:
            p.append('import_observation 없음 — 관측 필수 배치 (G2RR4-03) 의 감사에 관측 객체가 없다 · 관측 결손을 정상으로 받지 않는다 (G2RR4-01)')
        return p
    if not isinstance(io_, dict):
        return p + [f'import_observation {type(io_).__name__} — 관측 객체가 아니다 (G2RR4-01)']
    inner, outside = io_.get('problems'), io_.get('outside')
    if not isinstance(inner, list) or not isinstance(outside, list):
        p.append(f'import_observation.problems · outside 가 목록이 아니다 ({type(inner).__name__} · {type(outside).__name__}) — 관측 상세를 모른다 (G2RR4-01)')
    else:
        if inner:
            p.append(f'import_observation.problems {len(inner)} — {inner[:3]!r:.300} (빈 목록이어야 · G2RR4-01)')
        if outside:
            p.append(f'import_observation.outside {outside[:4]} — 봉인 밖 모듈을 실제로 읽었다 (빈 목록이어야 · G2RR4-01)')
        tl = top if isinstance(top, list) else []
        lost = [x for x in inner if x not in tl] + [f for f in outside if not any(isinstance(t, str) and str(f) in t for t in tl)]
        if lost:
            p.append(f'관측 내부 문제 · 봉인 밖 모듈 {len(lost)} 이 최상위 import_observation_problems 에 없다 {lost[:3]!r:.200} — 요약이 상세를 덮는다 (G2RR4-01)')
    for k in ('n_processes', 'n_started', 'n_finalized'):
        if not _v13_int(io_.get(k)):
            p.append(f'import_observation.{k} {io_.get(k)!r} — 정수가 아니다 (G2RR4-01)')
    if req:
        if _v13_int(io_.get('n_processes')) and io_['n_processes'] <= 0:
            p.append('import_observation.n_processes 0 — 관측 필수 배치인데 관측 기록이 없다 (G2RR4-01 · G2RR4-03)')
        ca = io_.get('completed_attempts')
        if not isinstance(ca, list) or not all(isinstance(x, (list, tuple)) and len(x) == 3 for x in ca):
            p.append(f'import_observation.completed_attempts {str(ca)[:80]} — [케이스, run, 시도] 목록이 아니다 (G2RR4-01)')
        else:
            try:
                need = {c for c, _h in _np194().registered_id_set(expect_set)['pairs']}
            except Exception as e:                                       # noqa: BLE001 — 기준을 못 세우면 통과로 치지 않는다
                p.append(f'등록 집합 {expect_set} 을 못 세웠다 ({type(e).__name__}: {e}) — 관측 완료 시도를 대조할 기준이 없다 (G2RR4-01)')
            else:
                gap = sorted(need - {str(x[0]) for x in ca})
                if gap:
                    p.append(f'import_observation.completed_attempts 가 등록 케이스 {len(gap)} 를 안 덮는다 (첫 {gap[:3]}) — 관측된 완료 시도 = 등록 {len(need)} '
                             '전부여야 (G2RR4-01)')
    return p


def v13_reread_problems(r, batch_root, why='', ident=None, expect_set=V13_REREAD_SET):
    """⓪b 다시 읽기 기록 (`g2_network_reread.py --launcher-root <ROOT> --expect-set production194 --json <ROOT>/reread.json` 의 dict) 판정 → 문제 목록.
    스키마 = 도구 정본 (v3 — 실행 신원) · n_fail = 정수 (bool 아님) 0 · 기대 세대 g2 · 등록 집합 (이름 · 기대 = 읽음 = 등록 수 · 같음 True · 빠진 · 남는 = 빈 목록) ·
    이 배치 (launcher_root = 배치 뿌리 · manifest_sha256 = 지금 manifest · seal_fp · launch_sha) · ★ G2RR4-01 상세 (meta · cases · checks — 필수 검사 ID ·
    bool · 상세 실패 재계수 = n_fail · 상세 (케이스, 코호트) = 등록 집합 · 케이스 수 = read_n · M3 = 최상위 — 생산자 `launcher_detail_problems`)."""
    if why == 'absent':
        return ['없다 — 등록 §5-3 ⓪b 다시 읽기 (`g2_network_reread.py --launcher-root <ROOT> --expect-set production194 --json <ROOT>/reread.json`) 를 먼저 · '
                '실제 배포는 이 기록이 필수']
    if why:
        return [f'못 읽는다 ({why}) — 손상된 다시 읽기 기록을 받지 않는다']
    if not isinstance(r, dict):
        return [f'객체가 아니다 ({type(r).__name__} — 예: null) — 다시 읽기 기록의 꼴이 아니다']
    if ident is None:
        ident = v13_batch_identity(batch_root)[0]
    p = []
    sch = _g2rr().SCHEMA
    if r.get('schema') != sch:
        p.append(f'schema {r.get("schema")!r} ≠ {sch!r} — 지금 도구의 기록이 아니다 (옛 기록 = 실행 신원 없음 · 진단 모드에서만)')
    nf = r.get('n_fail')
    if not _v13_int(nf):
        p.append(f'n_fail {nf!r} — 정수가 아니다 (null · bool · 문자열 · 결손 = 판정을 모른다)')
    elif nf != 0:
        p.append(f'n_fail {nf} — 다시 읽기 실패 (등록 §5-3 "rc 1 이면 인계하지 않는다")')
    if r.get('expected_generation') != V13_GENERATION:
        p.append(f'기대 세대 {r.get("expected_generation")!r} ≠ {V13_GENERATION} (등록 §5-3)')
    n_reg = _v13_registered(expect_set)[0]
    if not (r.get('expected_set') == expect_set and _v13_int(r.get('expected_n')) and _v13_int(r.get('read_n')) and r.get('expected_n') == n_reg
            and r.get('read_n') == n_reg and r.get('set_equal') is True):
        p.append(f'등록 집합 {r.get("expected_set")!r} · 기대 {r.get("expected_n")!r} · 읽음 {r.get("read_n")!r} · 같음 {r.get("set_equal")!r} — v1.3 은 등록 집합 '
                 f'{expect_set} ({n_reg}) 을 전부 다시 읽은 배치만 싣는다 (G2RR2-02)')
    if r.get('missing') != [] or r.get('extra') != []:
        p.append(f'missing {r.get("missing")!r:.120} · extra {r.get("extra")!r:.120} — 빈 목록이어야')
    p += _v13_bind_problems(r, ident, 'launcher_root')
    #  ★ 10-07 G2RR4-01 (Codex 세대 2 재검증 4 §2) — 상세 (meta · cases · checks) ↔ 요약 · 상세 실패 재계수 = n_fail · 상세 (케이스, 코호트) = 등록 집합 · 필수 검사 ID —
    #    생산자 쪽 상세 계약 한 함수 (`g2_network_reread.launcher_detail_problems` · 사본 금지).  옛 판은 요약만 읽어 meta M2 ok=false (n_fail 0) · cases=[] 를 받았다.
    try:
        pairs = _np194().registered_id_set(expect_set)['pairs']
    except Exception as e:                                               # noqa: BLE001 — 기준을 못 세우면 통과로 치지 않는다
        p.append(f'등록 집합 {expect_set} 을 못 세웠다 ({type(e).__name__}: {e}) — 상세를 대조할 기준이 없다 (G2RR4-01)')
    else:
        p += [f'상세 (G2RR4-01) — {x}' for x in _g2rr().launcher_detail_problems(r, pairs)]
    return p


def v13_batch_gate_problems(batch_root):
    """★ 10-07 G2RR3-01 — 배치 관문 판정 (등록 §5-2 ⓪ 감사 · §5-3 ⓪b 다시 읽기) — **build_v13 · 단계 A · check_v13 이 이 한 함수**.
    → (기록 {이름: None (없음) | dict(sha256, read, + 판정 필드 사본)}, 문제 목록 (['<이름> — <사유>', …] · [] = 통과)).
    배치 뿌리의 실행 신원 (`v13_batch_identity`) · 감사 (`v13_audit_problems`) · 다시 읽기 (`v13_reread_problems`) · 기록과 판정은 같은 바이트에서."""
    ident, probs = v13_batch_identity(batch_root)
    probs = [f'manifest — {p}' for p in probs]
    rec = {}
    for name, judge, keys in (('seal_audit.json', v13_audit_problems, _V13_AUDIT_REC_KEYS), ('reread.json', v13_reread_problems, _V13_REREAD_REC_KEYS)):
        sha, j, why = _v13_gate_load(os.path.join(batch_root, name))
        if why == 'absent':
            rec[name] = None
        else:
            rec[name] = dict({'sha256': sha, 'read': why or 'ok'}, **{k: (j.get(k) if isinstance(j, dict) else None) for k in keys})
        probs += [f'{name} — {p}' for p in judge(j, batch_root, why=why, ident=ident)]
    return rec, probs


def v13_batch_gate_files(batch_root):
    """배치 뿌리의 관문 기록 (`v13_batch_gate_problems` 의 기록 반쪽) — 빌드 manifest `batch_gate_files` 에 남기고 check_v13 이 지금 파일에서 다시 만든 것과 맞댄다."""
    return v13_batch_gate_problems(batch_root)[0]


def v13_batch_gate_check(batch_root, diagnostic=False):
    """배치 관문 (`v13_batch_gate_problems`) → (관문 dict, 경고 목록).  관문 dict = 빌드 manifest 의 batch_gate (스키마 · 모드 · 배치 뿌리 realpath ·
    manifest sha256 · 문제) + files (기록).
    실제 배포 (diagnostic False) — 문제가 하나라도 있으면 ReleaseError (★ G2RR3-01: 옛 판은 없거나 못 읽으면 경고만 · 감사 판정은 읽지 않았다).
    진단 모드 (diagnostic True · NOT FOR RELEASE) — 문제를 경고 · 관문 dict 에 남기고 계속 (옛 · 부분 기록을 들여다볼 때만 · check_v13 배포 대조는 거부)."""
    rec, probs = v13_batch_gate_problems(batch_root)
    gate = {'schema': V13_GATE_SCHEMA, 'mode': 'diagnostic' if diagnostic else 'release', 'batch_root': os.path.realpath(str(batch_root)),
            'manifest_sha256': _sha256_or_none(os.path.join(batch_root, 'manifest.json')), 'problems': probs, 'files': rec}
    if probs and not diagnostic:
        raise ReleaseError(f'배치 관문 증거 문제 {len(probs)} (G2RR3-01 — 등록 §5-2 ⓪ 감사 · §5-3 ⓪b 다시 읽기) — ' + ' | '.join(probs)
                           + ' — 실제 배포는 두 기록이 이 배치 뿌리 · manifest · 발사 봉인 지문에 대해 통과여야 한다 (옛 · 부분 기록을 들여다볼 때만 '
                             '--diagnostic-batch-gate · NOT FOR RELEASE)')
    return gate, ([f'({V13_DIAG_BANNER}) 배치 관문 {p}' for p in probs] if diagnostic else [])


def v13_handover_argv(dataset, batch_root, handover_csv, pressure=None, python=None):
    """단계 A — 인계표 생성기 CLI (리포 루트에서 돈다): 망 τ 원천 + 배치 manifest 기대 세대 (`--tau-batch-manifest` → 생성기
    `load_tau_results(expected_generation=)` — 세대 2 아닌 · 섞인 배치는 거기서 거부) · v1.3 묶음 (se_isolation 포함) · 완료 압력."""
    inp = V13_INPUTS[dataset]
    a = [python or sys.executable, os.path.join(REPO, 'scripts', 'lhs_design_dataset.py'), '--export-handover', handover_csv]
    if inp['design']:
        a += ['--design', inp['design']]
    a += ['--harvest', inp['harvest'], '--union', inp['union'],
          '--webapp', os.path.join(batch_root, 'merged', dataset), '--webapp-groups', V13_WEBAPP_GROUPS,
          '--tau-results', os.path.join(batch_root, 'merged', dataset, 'results'),
          '--tau-batch-manifest', os.path.join(batch_root, 'manifest.json')]
    a += ['--pressure-record', pressure] if pressure else ['--pressure-unverified']
    return a


def stage_handovers_v13(batch_root, handover_out, date, pressure=None, pressure_unverified=False, python=None, allow_seal_diff=None,
                        diagnostic=False):
    """단계 A — 배치 뿌리 → 인계표 둘 (`<ds>_handover_v13_<date>.csv` + 열 사전 · 제외 노트 · τ 출처 부록).  manifest = g2 · 원천 대조 ·
    발사 봉인 대조 (`v13_seal_gate`) · 배치 관문 (⓪ 감사 · ⓪b 다시 읽기 — `v13_batch_gate_check` · build · check 와 같은 함수) 먼저 — 생성기를 부르기 전에
    거부한다 (diagnostic = 진단 모드 · 관문 문제를 경고로)."""
    man = os.path.join(batch_root, 'manifest.json')
    v13_manifest_generation(man)
    mp = v13_manifest_inputs_problems(man)
    if mp:
        raise ReleaseError('배치 manifest ↔ v1.3 입력 — ' + ' | '.join(mp))
    _ci, w1 = v13_seal_gate(man, allow_seal_diff)
    _gate, w2 = v13_batch_gate_check(batch_root, diagnostic=diagnostic)
    for w in w1 + w2:
        print('  ⚠ 단계 A', w)
    if os.path.exists(handover_out) and os.listdir(handover_out):
        raise ReleaseError(f'인계표 산출 폴더 {handover_out} 가 비어 있지 않다 — 새 폴더에 만든다 (덮어쓰지 않는다)')
    os.makedirs(handover_out, exist_ok=True)
    for ds in V13_DATASETS:
        pr = (pressure or {}).get(ds)
        if pr is None and not pressure_unverified:
            cand = os.path.join(batch_root, 'pressure', f'{ds}_pressure_record.tsv')
            if not os.path.isfile(cand):
                raise ReleaseError(f'{ds}: 완료 압력 기록이 없다 ({cand}) — scripts/lhs_pressure_record.py 로 만들거나 --pressure-unverified (명시 승인 · DESC-06)')
            pr = cand
        argv = v13_handover_argv(ds, batch_root, os.path.join(handover_out, f'{ds}_handover_v13_{date}.csv'),
                                 pressure=None if pressure_unverified else pr, python=python)
        r = subprocess.run(argv, cwd=REPO, capture_output=True, text=True)
        if r.returncode != 0:
            raise ReleaseError(f'{ds}: 인계표 생성기 rc {r.returncode} — ' + ' / '.join((r.stderr or r.stdout or '').strip().splitlines()[-4:]))
        print(f'  ✓ 단계 A {ds}: ' + ((r.stdout or '').strip().splitlines() or [''])[0])
    return handover_out


def v13_reread_tau(dataset, batch_root, handover_rows, expected_generation):
    """τ 다시 읽기 — 생성기 `load_tau_results` (출처 관문 P0–P4 · 배치 manifest 기대 세대) 를 배포 때 한 번 더 부르고 인계표 τ 칸과 맞댄다.
    문제 목록 ([] = 같다).  load_tau_results 의 거부는 문제로 전파한다 (삼키지 않는다)."""
    LDD, TF = _ldd(), _tf()
    try:
        wv = LDD.load_webapp(os.path.join(batch_root, 'merged', dataset))
        res = LDD.load_tau_results(os.path.join(batch_root, 'merged', dataset, 'results'), wv, expected_generation=expected_generation)
    except LDD.FillRefusal as e:
        return [f'{dataset}: τ 다시 읽기 거부 — {e}']
    cases = (res or {}).get('cases') or {}
    ok_st = tuple(getattr(LDD, 'WA_OK_STATUS', ('done', 'partial')))
    hk = {r.get(KEY): r for r in handover_rows if r.get('wa_status', 'done') in ok_st}
    probs = []
    if set(cases) != set(hk):
        probs.append(f'{dataset}: τ 다시 읽기 케이스 집합 ≠ 인계표 — 다시 읽음에만 {sorted(set(cases) - set(hk))[:5]} · '
                     f'인계표에만 {sorted(set(hk) - set(cases))[:5]}')
    for c in sorted(set(cases) & set(hk)):
        cells = (cases[c] or {}).get('cells') or {}
        for col in TF.column_names():
            if col not in hk[c]:
                probs.append(f'{dataset} · {c}: 인계표에 τ 열 {col} 이 없다')
            elif str(cells.get(col, '')) != str(hk[c][col]):
                probs.append(f'{dataset} · {c} · {col}: 인계표 {hk[c][col]!r} ≠ 다시 읽음 {cells.get(col)!r}')
    return probs


# ── #5 porosity–σ–CN 재적합 ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def _refit_consts():
    G = _gcp()
    return {'phi_c_P': float(G.SE_PHI_C_P), 'phi_c_S': float(G.SE_PHI_C_S), 'delta': float(G.SE_SAT_DELTA), 'r_cut_um': 3.5,
            'gate_exponent': 2.0, 'locked_alpha': 0.5, 'locked_beta': float(G.SE_CN_EXP),
            'source': ('scripts/generate_comparison_plots.py — SE_PHI_C_P · SE_PHI_C_S · SE_SAT_DELTA · SE_CN_EXP · _sat_g_smooth (σ_ionic T1 등록식 '
                       '동결값 · CLAUDE.md "σ_ionic form FINALIZED" — φ_eff^½ · CN²)')}


def _refit_gate(p, r_s, r_p):
    """크기 게이트 g = min(3.5 / r_AM_eff, 1)^2 · r_AM_eff = (1 − p)·r_AM_S + p·r_AM_P (생산 `_sat_g_smooth` 그대로)."""
    if r_s is None and r_p is None:
        raise ReleaseError('재적합 — r_AM_S · r_AM_P 가 둘 다 없다 (크기 게이트를 정할 수 없다 · 라벨 게이트로 바꾸지 않는다)')
    return float(_gcp()._sat_g_smooth(p, r_s, r_p))


def _refit_phi_eff(phi, g):
    """φ_eff = √[(φ − φc_eff)² + (δ·g)²] · φc_eff = (1 − g)·φc_P + g·φc_S (생산 `_sat_baselog` 와 같은 식 · 같은 상수)."""
    c = _refit_consts()
    phic = (1.0 - g) * c['phi_c_P'] + g * c['phi_c_S']
    return math.sqrt((phi - phic) ** 2 + (c['delta'] * g) ** 2 + 1e-12)


def _refit_gate_selfcheck():
    """생산 게이트가 기록한 상수 (r_cut 3.5 · 지수 2) 와 같은가 — 바뀌었으면 요약의 상수 표가 거짓이 된다."""
    a, b = _refit_gate(1.0, None, 7.0), _refit_gate(0.0, 1.0, None)
    if abs(a - 0.25) > 1e-12 or abs(b - 1.0) > 1e-12:
        raise ReleaseError(f'재적합 — 생산 크기 게이트가 기록 상수 (r_cut 3.5 · 지수 2) 와 다르다 (g(7 µm) = {a!r}) — _refit_consts 를 먼저 고칠 것')


def _refit_ols(X, y):
    import numpy as np
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ (X.T @ y)
    e = y - X @ b
    h = np.einsum('ij,jk,ik->i', X, XtX_inv, X)
    n, k = X.shape
    s2 = float((e ** 2).sum()) / (n - k) if n > k else float('nan')
    se = np.sqrt(np.diag(XtX_inv) * s2)
    return b, e, h, se


def _refit_stats(y, e, h, ds_of):
    import numpy as np
    sst = float(((y - y.mean()) ** 2).sum())
    sse = float((e ** 2).sum())
    loo = e / (1.0 - h)
    out = {'r2': 1.0 - sse / sst if sst > 0 else float('nan'),
           'loocv_r2': 1.0 - float((loo ** 2).sum()) / sst if sst > 0 else float('nan'),
           'resid_sd': float(np.sqrt(sse / len(y))), 'by_dataset': {}}
    for ds in sorted(set(ds_of)):
        m = np.array([d == ds for d in ds_of])
        yd, ed = y[m], e[m]
        sd = float(((yd - yd.mean()) ** 2).sum())
        out['by_dataset'][ds] = {'n': int(m.sum()), 'bias': float(ed.mean()), 'resid_sd': float(np.sqrt((ed ** 2).mean())),
                                 'r2': (1.0 - float((ed ** 2).sum()) / sd) if (m.sum() >= 2 and sd > 0) else None}
    return out


def refit_porosity_sigma_cn(rows, dry_run=False):
    """#5 porosity–σ–CN 재적합 — 아무 인계표 · 배포 표의 행 (dataset 열 필요) → {'summary', 'rows'}.

    대상 = ln f_ion_hertz (f = σ_eff/σ₀ · L_mc 기준 · Hertz) · 관통 행만 (상태 OK · MODEL_BELOW_CONTINUUM_BOUND — 값 유지 행을 사후에 빼지 않는다) ·
    비관통 · 기술 실패 · HOLD 행은 적합 밖 (사유 표 · 행은 남긴다 — 분류 가지).
    φ_eff = σ_ionic 등록식의 SAT-blend 관통 거리 (φ = phi_se_mass_conserving · 동결 φc_P 0.200 · φc_S 0.195 · δ 0.040 · 크기 게이트 — 생산 코드에서 읽는다).
      locked: ln f = a + ½·ln φ_eff + 2·ln CN_SE-SE   (등록식 지수 그대로 · 자유 매개변수 a 하나)
      free:   ln f = a + α·ln φ_eff + β·ln CN_SE-SE   (지수 다시 적합)
    porosity 는 φ_SE,mc = (1 − ε_union)·(SE/고체) 로 들어온다 (설계 → 구조 ML 이 내는 ε · CN 을 f 로 잇는 근사).  f_p · coverage · τ 항은 넣지 않는다
    (τ 는 f 의 항등식 — 누설).  LOOCV = 해석적 hat 행렬.  결정적 (같은 입력 = 같은 JSON)."""
    import numpy as np
    rows = list(rows)
    if not rows:
        raise ReleaseError('재적합 — 행이 없다')
    miss = [c for c in (KEY, 'dataset') + REFIT_NEEDS if any(c not in r for r in rows)]
    if miss:
        raise ReleaseError(f'재적합 입력 열이 없다: {miss}')
    _refit_gate_selfcheck()
    c0 = _refit_consts()
    out_rows, X, ds_of, excl = [], [], [], collections.Counter()
    for r in rows:
        st = r.get('ion_net_status_hertz', '')
        o = {k: '' for k in REFIT_ROW_COLS}
        o.update({k: r.get(k, '') for k in ('dataset', 'case_id', 'ion_net_status_hertz', 'porosity_union_exact_pct', 'phi_se_mass_conserving',
                                              'se_se_cn', 'f_ion_hertz')})
        if st in REFIT_SKIP_STATUSES:
            o.update(included='0', excluded_reason=st)
            excl[st] += 1
            out_rows.append(o)
            continue
        if st not in REFIT_FIT_STATUSES:
            raise ReleaseError(f'{r.get(KEY)}: 재적합 — 모르는 상태 {st!r}')
        f, phi, cn, p = (_v13_num(r.get(k)) for k in ('f_ion_hertz', 'phi_se_mass_conserving', 'se_se_cn', 'ps_frac'))
        if f is None or f <= 0 or phi is None or phi <= 0 or cn is None or cn <= 0 or p is None:
            raise ReleaseError(f'{r.get(KEY)}: 재적합 — 관통 행인데 f · φ_SE,mc · CN · ps_frac 가 유한 양수가 아니다 ({f!r} · {phi!r} · {cn!r} · {p!r})')
        g = _refit_gate(p, _v13_num(r.get('r_AM_S_um')), _v13_num(r.get('r_AM_P_um')))
        pe = _refit_phi_eff(phi, g)
        o.update(included='1', g_phys=repr(g), phi_c_eff=repr((1.0 - g) * c0['phi_c_P'] + g * c0['phi_c_S']), phi_eff=repr(pe),
                 x_collapse=repr(math.sqrt(pe) * cn ** 2), ln_f=repr(math.log(f)))
        X.append((math.log(pe), math.log(cn), math.log(f)))
        ds_of.append(str(r.get('dataset')))
        out_rows.append(o)
    n = len(X)
    if n < REFIT_MIN_ROWS:
        raise ReleaseError(f'재적합 — 관통 행 {n} < {REFIT_MIN_ROWS} (적합하지 않는다)')
    A = np.array(X, dtype=float)
    lpe, lcn, y = A[:, 0], A[:, 1], A[:, 2]
    yl = y - c0['locked_alpha'] * lpe - c0['locked_beta'] * lcn
    a_l = float(yl.mean())
    e_l = yl - a_l
    st_l = _refit_stats(y, e_l, np.full(n, 1.0 / n), ds_of)
    st_l.update(params={'a': a_l, 'alpha': c0['locked_alpha'], 'beta': c0['locked_beta']},
                se={'a': float(np.sqrt(float((e_l ** 2).sum()) / (n - 1) / n))}, n_free=1)
    Xf = np.column_stack([np.ones(n), lpe, lcn])
    b, e_f, h_f, se_f = _refit_ols(Xf, y)
    st_f = _refit_stats(y, e_f, h_f, ds_of)
    st_f.update(params={'a': float(b[0]), 'alpha': float(b[1]), 'beta': float(b[2])},
                se={'a': float(se_f[0]), 'alpha': float(se_f[1]), 'beta': float(se_f[2])}, n_free=3)
    j = 0
    for o in out_rows:
        if o['included'] != '1':
            continue
        o.update(ln_f_locked=repr(float(y[j] - e_l[j])), resid_locked=repr(float(e_l[j])), ln_f_free=repr(float(y[j] - e_f[j])),
                 resid_free=repr(float(e_f[j])))
        j += 1
    summary = {
        'schema': REFIT_SCHEMA, 'dry_run': bool(dry_run),
        'target': 'ln f_ion_hertz (f = σ_eff/σ₀ · 무차원 · L_mc 기준 · Hertz 망) — 관통 행만 (상태 OK · MODEL_BELOW_CONTINUUM_BOUND)',
        'forms': {'locked': 'ln f = a + 0.5·ln φ_eff + 2·ln CN_SE-SE  (σ_ionic T1 등록식 지수 · 자유 매개변수 a)',
                  'free': 'ln f = a + α·ln φ_eff + β·ln CN_SE-SE  (지수 다시 적합)'},
        'phi_eff': ('φ_eff = √[(φ_SE,mc − φc_eff)² + (δ·g)²] · φc_eff = (1 − g)·φc_P + g·φc_S · g = min(r_cut / r_AM_eff, 1)^2 · '
                    'r_AM_eff = (1 − p)·r_AM_S + p·r_AM_P (p = ps_frac · mono 는 있는 상만) · φ_SE,mc = phi_se_mass_conserving'),
        'cn': 'CN_SE-SE = se_se_cn (SE 1 개당 SE 접촉 수 · 전 SE 평균 · 벽 입자 포함)',
        'porosity': 'porosity_union_exact_pct 는 φ_SE,mc = (1 − ε/100)·se_of_solid_vol 로 들어온다 (그림 가로축 · 행 표에 병기)',
        'constants': c0, 'fit_statuses': list(REFIT_FIT_STATUSES), 'n_total': len(rows), 'n_fit': n,
        'excluded': dict(sorted(excl.items())), 'n_fit_by_dataset': dict(sorted(collections.Counter(ds_of).items())),
        'fits': {'locked': st_l, 'free': st_f},
        'caveats': ['모델 내부 관계 — 고정 접촉망 · 면적 · 협착 · 경계 규약에서 계산한 f 의 근사식 · 실험 절대값 · 실물 순위 · COMSOL 물성 아님',
                    '지수 (α · β) 는 이 코퍼스 · 이 규약의 적합값 — 물리 상수로 인용하지 않는다',
                    'f_p (관통 분율) · coverage · τ 항을 넣지 않았다 — τ 는 f 의 항등식 (누설) · 관통 여부는 분류 가지 (ion_percolates_hertz)',
                    '두 데이터셋 (130 · 64 SE-rich) 은 분포가 다르다 — by_dataset 편향 · R² 를 따로 본다',
                    'LOOCV = 해석적 hat 행렬 (OLS) — 변수 선택 · φc 재선정은 하지 않았다 (동결값)']}
    return {'summary': summary, 'rows': out_rows}


def refit_from_csv(path_by_ds, dry_run=False):
    """#5 — 아무 인계표 · 배포 CSV ({데이터셋: 경로}) 에서 재적합 (요약에 입력 파일 sha256)."""
    rows = []
    for ds, p in path_by_ds.items():
        h, rr = _read_csv(p)
        for r in rr:
            d = dict(zip(h, r))
            d['dataset'] = ds
            rows.append(d)
    fit = refit_porosity_sigma_cn(rows, dry_run=dry_run)
    fit['summary']['inputs'] = {ds: {'file': os.path.basename(p), 'sha256': _sha256(p)} for ds, p in path_by_ds.items()}
    return fit


def _v13_close(a, b, path='$'):
    """재현 비교 (부동소수 상대 1e-9) — 다른 첫 자리의 경로 · 같으면 ''."""
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            return f'{path}: 키 {sorted(set(a) ^ set(b))[:4]}'
        for k in sorted(a):
            d = _v13_close(a[k], b[k], f'{path}.{k}')
            if d:
                return d
        return ''
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return f'{path}: 길이 {len(a)} ≠ {len(b)}'
        for i, (x, y) in enumerate(zip(a, b)):
            d = _v13_close(x, y, f'{path}[{i}]')
            if d:
                return d
        return ''
    if isinstance(a, bool) or isinstance(b, bool) or a is None or b is None or isinstance(a, str) or isinstance(b, str):
        return '' if a == b else f'{path}: {a!r} ≠ {b!r}'
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if (isinstance(a, float) and math.isnan(a)) and (isinstance(b, float) and math.isnan(b)):
            return ''
        return '' if math.isclose(a, b, rel_tol=_V13_FLOAT_RTOL, abs_tol=1e-12) else f'{path}: {a!r} ≠ {b!r}'
    return '' if a == b else f'{path}: {a!r} ≠ {b!r}'


def _v13_rows_close(ra, rb):
    """재적합 행 표 비교 — 숫자 칸은 상대 1e-9 · 나머지는 글자 그대로."""
    if len(ra) != len(rb):
        return f'행 수 {len(ra)} ≠ {len(rb)}'
    for i, (x, y) in enumerate(zip(ra, rb)):
        for k in REFIT_ROW_COLS:
            a, b = x.get(k, ''), y.get(k, '')
            if a == b:
                continue
            fa, fb = _v13_num(a), _v13_num(b)
            if fa is None or fb is None or not math.isclose(fa, fb, rel_tol=_V13_FLOAT_RTOL, abs_tol=1e-12):
                return f'{x.get("case_id")} · {k}: {a!r} ≠ {b!r}'
    return ''


def _v13_write_csv(path, head, rows, bom=False):
    with open(path, 'w', encoding='utf-8-sig' if bom else 'utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(head)
        for r in rows:
            w.writerow([r.get(c, '') for c in head] if isinstance(r, dict) else r)


def _v13_write_refit(fit, stage, prefix, dry_run):
    """재적합 산출 — 행 CSV · 요약 JSON · Origin 워크시트 셋 (1 줄 Long Name · 2 줄 Units · utf-8-sig · LF) + GUIDE · 미리보기 png · svg."""
    s = fit['summary']
    _v13_write_csv(os.path.join(stage, f'{prefix}{REFIT_STEM}_rows.csv'), list(REFIT_ROW_COLS), fit['rows'])
    with open(os.path.join(stage, f'{prefix}{REFIT_STEM}_summary.json'), 'w', encoding='utf-8', newline='') as f:
        f.write(json.dumps(s, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
    od, pd = os.path.join(stage, 'origin'), os.path.join(stage, 'previews')
    os.makedirs(od, exist_ok=True)
    os.makedirs(pd, exist_ok=True)
    lab = {'lhs': 'LHS', 'lhsx': 'LHSx'}
    rows = fit['rows']
    inc = [r for r in rows if r['included'] == '1']

    def lnf_free(r):
        return float(r['ln_f_free'])                                    # 행 표의 예측 그대로 (식을 다시 쓰지 않는다)
    _v13_write_csv(os.path.join(od, f'{prefix}v13_refit_porosity_f.csv'), ['Dataset', 'Case', 'Porosity', 'f', 'SE–SE CN', 'Percolating'],
                   [['', '', '%', '1', '1', '1 = yes'] ] + [[lab.get(r['dataset'], r['dataset']), r['case_id'], r['porosity_union_exact_pct'],
                                                             r['f_ion_hertz'], r['se_se_cn'], '1' if r['included'] == '1' else '0'] for r in rows],
                   bom=True)
    _v13_write_csv(os.path.join(od, f'{prefix}v13_refit_collapse.csv'),
                   ['Dataset', 'Case', 'φ_eff^0.5·CN^2', 'f', 'f (locked fit)'],
                   [['', '', '1', '1', '1']] + [[lab.get(r['dataset'], r['dataset']), r['case_id'], r['x_collapse'], r['f_ion_hertz'],
                                                 repr(math.exp(float(r['ln_f_locked'])))] for r in inc], bom=True)
    _v13_write_csv(os.path.join(od, f'{prefix}v13_refit_parity.csv'), ['Dataset', 'Case', 'f (DEM network)', 'f (free fit)', 'f (locked fit)'],
                   [['', '', '1', '1', '1']] + [[lab.get(r['dataset'], r['dataset']), r['case_id'], r['f_ion_hertz'], repr(math.exp(lnf_free(r))),
                                                 repr(math.exp(float(r['ln_f_locked'])))] for r in inc], bom=True)
    with open(os.path.join(od, f'{prefix}GUIDE.md'), 'w', encoding='utf-8', newline='') as f:
        f.write((f'> ⚠ {V13_DRY_BANNER}\n\n' if dry_run else '')
                + '# Origin 가이드 — v1.3 porosity–σ–CN 재적합 (#5)\n\n'
                '- 가져오기: CSV 를 Origin 에 끌어 놓기 → Header Lines: **Long Name = 1 줄 · Units = 2 줄** · Data Start = 3 줄 (utf-8 · BOM).\n'
                f'- `{prefix}v13_refit_porosity_f.csv` — 가로 Porosity (%) · 세로 f (log) · 색 = SE–SE CN · 모양 = Dataset · Percolating = 0 행은 f = 0 '
                '(로그 축에 못 그린다 — 따로 표시하거나 뺀다 · 지우지 않는다).\n'
                f'- `{prefix}v13_refit_collapse.csv` — 가로 φ_eff^0.5·CN^2 · 세로 f (log–log) · 등록식 (locked) 선 = f (locked fit) 열.\n'
                f'- `{prefix}v13_refit_parity.csv` — 가로 f (DEM network) · 세로 f (free fit) · 1:1 선 (log–log).\n'
                '- 서식 = 랩 BML 표준 (`docs/report_making_principles.md` — 레이어 12 × 9 cm · Aptos · 테두리) · 미리보기 `../previews/` 는 Liberation Sans.\n'
                '- 식 · 상수 · 한정어 = 요약 JSON (`../' + f'{prefix}{REFIT_STEM}_summary.json`) — 모델 내부 관계 · 지수를 물리 상수로 인용하지 않는다.\n')
    _v13_refit_figure(fit, pd, prefix, dry_run)


def _v13_refit_figure(fit, pd, prefix, dry_run):
    """미리보기 (세 패널 · 한 패널 한 축) — (a) f vs porosity (색 = CN · 단일 색상 순차) (b) 붕괴 f vs φ_eff^½·CN² + 등록식 선 (c) 대각 (free)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    rows, s = fit['rows'], fit['summary']
    inc = [r for r in rows if r['included'] == '1']
    exc = [r for r in rows if r['included'] != '1']
    GRAY, C1, C2 = '#404040', '#2a78d6', '#eb6834'
    color = {'lhs': C1, 'lhsx': C2}
    mark = {'lhs': 'o', 'lhsx': 's'}
    name = {'lhs': 'LHS (130)', 'lhsx': 'LHSx, SE-rich (64)'}
    cmap = LinearSegmentedColormap.from_list('cn_blue', ['#bcd5f2', '#2a78d6', '#0d2f5c'])
    fr, lk = s['fits']['free'], s['fits']['locked']
    with plt.rc_context({'font.family': ['Liberation Sans', 'DejaVu Sans'], 'font.size': 10, 'axes.edgecolor': GRAY, 'axes.labelcolor': GRAY,
                         'xtick.color': GRAY, 'ytick.color': GRAY, 'xtick.direction': 'out', 'ytick.direction': 'out', 'axes.linewidth': 1.0,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'lhs_v13_refit'}):
        fig, axs = plt.subplots(1, 3, figsize=(14.0, 4.6))
        a1, a2, a3 = axs
        cns = [float(r['se_se_cn']) for r in inc]
        vmin, vmax = (min(cns), max(cns)) if cns else (0.0, 1.0)
        for ds in ('lhs', 'lhsx'):
            R = [r for r in inc if r['dataset'] == ds]
            if R:
                sc = a1.scatter([float(r['porosity_union_exact_pct']) for r in R], [float(r['f_ion_hertz']) for r in R],
                                c=[float(r['se_se_cn']) for r in R], cmap=cmap, vmin=vmin, vmax=vmax, marker=mark[ds], s=22,
                                edgecolors='white', linewidths=0.4, label=name[ds])
        np_ = [r for r in exc if r['excluded_reason'] == 'NOT_PERCOLATING']
        fl = min((float(r['f_ion_hertz']) for r in inc), default=1e-3) / 3.0
        if np_:
            a1.scatter([float(r['porosity_union_exact_pct']) for r in np_], [fl] * len(np_), marker='x', s=22, color='#8a8986', linewidths=1.0,
                       label=f'No ion through path ({len(np_)}, f = 0, drawn at floor)')
        a1.set_yscale('log')
        a1.set_xlabel('Porosity, union (%)')
        a1.set_ylabel('f = σ_eff / σ₀ (Hertz)')
        if inc:
            cb = fig.colorbar(sc, ax=a1, pad=0.02)
            cb.set_label('SE–SE CN')
        from matplotlib.lines import Line2D                              # 범례 표지 = 모양만 (색은 CN 막대가 말한다)
        hl = [Line2D([], [], ls='', marker=mark[ds], color='#8a8986', markersize=5, label=name[ds]) for ds in ('lhs', 'lhsx')]
        if np_:
            hl.append(Line2D([], [], ls='', marker='x', color='#8a8986', markersize=5, label=f'No ion through path ({len(np_)}, f = 0, at floor)'))
        a1.legend(handles=hl, frameon=False, fontsize=8, loc='lower left', bbox_to_anchor=(0.0, 0.10))   # 바닥 표지 줄 위 · 빈 왼쪽 아래
        for ds in ('lhs', 'lhsx'):
            R = [r for r in inc if r['dataset'] == ds]
            if R:
                a2.scatter([float(r['x_collapse']) for r in R], [float(r['f_ion_hertz']) for r in R], marker=mark[ds], s=18, facecolors='none',
                           edgecolors=color[ds], linewidths=1.0, label=name[ds])
        xs = sorted(float(r['x_collapse']) for r in inc)
        if xs:
            a2.plot([xs[0], xs[-1]], [math.exp(lk['params']['a']) * xs[0], math.exp(lk['params']['a']) * xs[-1]], color=GRAY, lw=1.2, ls='--',
                    label=f'locked: f = e^a·φ_eff^0.5·CN² (R² {lk["r2"]:.3f})')
        a2.set_xscale('log')
        a2.set_yscale('log')
        a2.set_xlabel('φ_eff^0.5 · CN²')
        a2.set_ylabel('f')
        a2.legend(frameon=False, fontsize=8, loc='upper left')
        for ds in ('lhs', 'lhsx'):
            R = [r for r in inc if r['dataset'] == ds]
            if R:
                a3.scatter([float(r['f_ion_hertz']) for r in R], [math.exp(float(r['ln_f_free'])) for r in R], marker=mark[ds], s=18,
                           facecolors='none', edgecolors=color[ds], linewidths=1.0, label=name[ds])
        fv = [float(r['f_ion_hertz']) for r in inc] + [math.exp(float(r['ln_f_free'])) for r in inc]
        if fv:
            lo, hi = min(fv) / 1.3, max(fv) * 1.3
            a3.plot([lo, hi], [lo, hi], color=GRAY, lw=1.0, ls='-', label='1:1')
        p = fr['params']
        a3.set_xscale('log')
        a3.set_yscale('log')
        a3.set_xlabel('f (DEM network)')
        a3.set_ylabel(f'f (free fit: α {p["alpha"]:.3f} · β {p["beta"]:.3f})')
        a3.legend(frameon=False, fontsize=8, loc='upper left',
                  title=f'R² {fr["r2"]:.3f} · LOOCV {fr["loocv_r2"]:.3f} · n {s["n_fit"]}', title_fontsize=8)
        for ax, t in zip(axs, 'abc'):
            ax.text(-0.14, 1.03, f'({t})', transform=ax.transAxes, fontsize=11, fontweight='bold', color=GRAY, va='bottom')
        foot = ('Network model descriptor (fixed contact network · Hertz) — not an experimental value · exponents are corpus fits, not physical constants · '
                'φ_eff = SAT-blend distance from the frozen σ_ionic thresholds')
        if dry_run:
            foot = f'{V13_DRY_BANNER} (generation-1 input) · ' + foot
        fig.text(0.5, 0.005, foot, ha='center', va='bottom', fontsize=7.5, color='#666666')
        fig.tight_layout(rect=(0, 0.05, 1, 1), w_pad=2.0)
        fig.savefig(os.path.join(pd, f'{prefix}v13_refit_porosity_sigma_cn.png'), dpi=200, metadata={'Software': None})
        fig.savefig(os.path.join(pd, f'{prefix}v13_refit_porosity_sigma_cn.svg'), metadata={'Date': None})
        plt.close(fig)


# ── 빌드 · 대조 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
def _v13_handover(handover_dir, ds):
    """인계표 폴더에서 `<ds>_handover_*.csv` 정확히 하나 + 열 사전 · τ 출처 부록."""
    c = sorted(glob.glob(os.path.join(handover_dir, f'{ds}_handover_*.csv')))
    if len(c) != 1:
        raise ReleaseError(f'{handover_dir}: {ds}_handover_*.csv 가 {len(c)} 개 — 정확히 하나여야 한다 {[os.path.basename(x) for x in c]}')
    stem = c[0][:-4]
    for suf in ('_columns.tsv', '_tau_provenance.tsv'):
        if not os.path.isfile(stem + suf):
            raise ReleaseError(f'{os.path.basename(stem)}{suf} 가 없다 — 인계표 묶음이 아니다')
    return c[0]


def _v13_prefix(dry_run):
    return V13_DRY_PREFIX if dry_run else ''


def _v13_out_guard(out_dir, dry_run, diagnostic=False):
    a = os.path.abspath(out_dir)
    if (dry_run or diagnostic) and (a + os.sep).startswith(REPO + os.sep):
        raise ReleaseError(f'{"dry-run" if dry_run else "진단 (NOT FOR RELEASE)"} 산출을 리포 안 ({_v13_rel(a)}) 에 쓰지 않는다 — docs/data 의 배포 폴더와 섞이거나 '
                           '커밋되지 않게 · 리포 밖 스크래치에')
    if os.path.exists(a) and (not os.path.isdir(a) or os.listdir(a)):
        raise ReleaseError(f'산출 폴더 {a} 가 이미 있고 비어 있지 않다 — 새 폴더에 만든다 (덮어쓰지 않는다)')
    return a


def _v13_status_counts(rows, col):
    return dict(sorted(collections.Counter(r.get(col, '') for r in rows).items()))


def _v13_iso_stats(rows):
    """고립 열이 비관통에 몰리는가 — (관통 · 비관통) × (am_ionic_isolated_pct · se_isolated_pct) 평균 · 최대."""
    out = {}
    for col in ('am_ionic_isolated_pct', 'se_isolated_pct'):
        for lab, sel in (('perc', lambda r: r.get('ion_net_status_hertz') in _V13_VALUE_STATUSES),
                         ('nonperc', lambda r: r.get('ion_net_status_hertz') == 'NOT_PERCOLATING')):
            v = [_v13_num(r.get(col)) for r in rows if sel(r) and col in r]
            v = [x for x in v if x is not None]
            out[f'{col}:{lab}'] = (len(v), (sum(v) / len(v)) if v else None, max(v) if v else None)
    return out


def build_v13(*, out_dir, handover_dir, batch_root=None, date=None, dry_run=False, codex_verdict=None, h12_appendix=False,
              pressure_unverified=False, transfer_text=None, allow_seal_diff=None, diagnostic=False):
    """단계 B — 인계표 (둘) → v1.3 배포 묶음 (out_dir).  실제 (dry_run False): Codex 판정문 · 배치 뿌리 (manifest g2 · 원천 대조 · 발사 봉인 대조 ·
    배치 관문 = ⓪ 감사 · ⓪b 다시 읽기 (★ G2RR3-01 — 두 기록 필수 · 판정 · 이 배치에 결합 · check_v13 과 같은 함수) · τ 다시 읽기) · 인계표 세대 g2 ·
    완료 압력 열 (없으면 --pressure-unverified 명시 승인) 필수.  봉인 파일이 발사 때와 다르면 거부 —
    값과 무관한 변경이면 allow_seal_diff (--allow-seal-diff) 로 명시 승인 · 기록.  dry-run: 세대 1 원천 허용 · 빠진 v1.3 열은 기록하고 뺀다 ·
    파일 이름 DRYRUN_ · README 첫 줄 "DRY RUN — not a release" · 리포 안 (docs/data 포함) 거부.  임시 폴더에 다 만들고 `check_v13` 통과 뒤에만 out_dir 로 옮긴다
    (거부 · 실패면 산출 폴더가 남지 않는다).  transfer_text = Codex GO 판정문의 전달 문안 파일 (있으면 README "외부 검토" 에 그대로 · sha256 기록 —
    README 를 만든 뒤 손으로 고치면 빌드 manifest 의 sha256 이 어긋난다).
    diagnostic (--diagnostic-batch-gate · 실제 경로만) = 진단 모드 — 배치 관문 문제를 경고로 남기고 만든다 · README 첫 줄 · 빌드 manifest 에 NOT FOR RELEASE ·
    리포 안 거부 · check_v13 배포 대조는 거부 (진단 대조 `check_v13(…, diagnostic=True)` 만 통과).  반환 = 보고 dict."""
    date = date or datetime.date.today().strftime('%Y%m%d')
    if diagnostic and dry_run:
        raise ReleaseError('--diagnostic-batch-gate 는 실제 경로 (배치 뿌리 · 배치 관문) 에만 — dry-run 은 배치 관문을 보지 않는다')
    tt = None
    if transfer_text:
        if not os.path.isfile(transfer_text):
            raise ReleaseError(f'전달 문안 파일 {transfer_text!r} 이 없다')
        tt = {'file': _v13_rel(transfer_text), 'sha256': _sha256(transfer_text), 'text': open(transfer_text, encoding='utf-8').read().strip()}
    if not re.fullmatch(r'\d{8}', str(date)):
        raise ReleaseError(f'날짜 {date!r} — YYYYMMDD')
    out_abs = _v13_out_guard(out_dir, dry_run, diagnostic)
    pre = _v13_prefix(dry_run)
    warnings = []
    man_info = code_identity = gate = None
    if not dry_run:
        if not codex_verdict or not os.path.isfile(codex_verdict):
            raise ReleaseError(f'Codex 세대 2 판정문 (GO) 이 없다 ({codex_verdict!r}) — v1.3 은 GO 뒤에만 만든다 (--codex-verdict)')
        if not batch_root:
            raise ReleaseError('--batch-root (배치 뿌리 — τ 다시 읽기 · manifest 기대 세대) 가 없다 — 실제 v1.3 은 load_tau_results 로 다시 읽은 뒤에만 만든다')
        mpath = os.path.join(batch_root, 'manifest.json')
        g_man = v13_manifest_generation(mpath)
        mp = v13_manifest_inputs_problems(mpath)
        if mp:
            raise ReleaseError('배치 manifest ↔ v1.3 입력 — ' + ' | '.join(mp))
        man_info = {'path': _v13_rel(mpath), 'sha256': _sha256(mpath), 'expected_network_generation': g_man}
        code_identity, w_seal = v13_seal_gate(mpath, allow_seal_diff)          # 발사 봉인 ↔ 이 체크아웃 (세대 2 등록 §3)
        gate, w_gate = v13_batch_gate_check(batch_root, diagnostic=diagnostic)  # ⓪ 감사 · ⓪b 다시 읽기 (등록 §5-2 · §5-3 · G2RR3-01 — check 와 같은 함수)
        warnings += w_seal + w_gate
    elif allow_seal_diff:
        raise ReleaseError('--allow-seal-diff 는 실제 v1.3 (배치 뿌리 · 발사 봉인 대조) 에만 쓴다 — dry-run 은 봉인 대조를 하지 않는다')
    LDD = _ldd()
    hand, hrows, gens, missing = {}, {}, {}, {}
    for ds in V13_DATASETS:
        hp = _v13_handover(handover_dir, ds)
        head, rows = _read_csv(hp)
        drows = [dict(zip(head, r)) for r in rows]
        hand[ds], hrows[ds] = (hp, head), drows
        g, gp = v13_generation_problems(drows, dry_run=dry_run)
        if gp:
            raise ReleaseError(f'{ds}: 세대 관문 {len(gp)} — ' + ' | '.join(gp[:3]))
        gens[ds] = g
        bad = [r.get(KEY) for r in drows if 'wa_status' in r and r['wa_status'] not in LDD.WA_OK_STATUS]
        if bad:
            raise ReleaseError(f'{ds}: 웹앱 배치 done · partial 이 아닌 행 {bad[:5]} — 최종판은 194/194 완주 배치만')
        with open(hp[:-4] + '_tau_provenance.tsv', encoding='utf-8', newline='') as f:
            prov = {r['case']: r for r in csv.DictReader(f, delimiter='\t')}
        if set(prov) != {r[KEY] for r in drows}:
            raise ReleaseError(f'{ds}: τ 출처 부록 케이스 ≠ 인계표 케이스')
        stale = sorted(c for c, r in prov.items() if r.get('same_generation_checks') != ';'.join(LDD.TAU_SAME_GEN_CHECKS))
        if stale:
            msg = (f'{ds}: τ 출처 부록 same_generation_checks 가 지금 목록 ({len(LDD.TAU_SAME_GEN_CHECKS)} 검사) 과 다른 케이스 {len(stale)} '
                   f'(예 {stale[0]}) — 옛 생성기로 만든 인계표')
            if not dry_run:
                raise ReleaseError(msg)
            warnings.append(msg)
        if 'se_isolated_pct' in head:
            sp = v13_se_isolated_problems(drows)
            if sp:
                raise ReleaseError(f'{ds}: se_isolated_pct 항등식 {len(sp)} — ' + ' | '.join(sp[:3]))
    tau_reread = 'not_performed (dry run — 세대 1 원천 · τ 원천 폴더 없음)'
    if not dry_run:
        rp = []
        for ds in V13_DATASETS:
            rp += v13_reread_tau(ds, batch_root, hrows[ds], V13_GENERATION)
        if rp:
            raise ReleaseError(f'τ 다시 읽기 문제 {len(rp)} (load_tau_results · 배치 manifest 기대 세대 g2) — ' + ' | '.join(rp[:4]))
        tau_reread = 'performed'
    stage = out_abs + f'.partial-{os.getpid()}'
    if os.path.exists(stage):
        shutil.rmtree(stage)
    os.makedirs(stage)
    try:
        specs = {}
        press_ok = all(c in hand[ds][1] for ds in V13_DATASETS for c in V13_PRESS_ADD)
        if not press_ok and not dry_run and not pressure_unverified:
            raise ReleaseError('인계표에 완료 압력 열 (press_*) 이 없다 — --pressure-record 로 만든 인계표이거나 --pressure-unverified (명시 승인 · DESC-06)')
        for ds in V13_DATASETS:
            head = hand[ds][1]
            #  완료 압력 열: 실제 + 명시 승인 (--pressure-unverified) 이면 명세에서 뺀다 (README · manifest 에 미검사 표지) · dry-run 은 빠진 열로 기록
            kinds = [('main', v13_columns(ds, 'main', press=(press_ok or dry_run))), ('physics', v13_columns(ds, 'physics'))]
            if h12_appendix:
                kinds.append(('h12', v13_columns(ds, 'h12')))
            for kind, cols in kinds:
                mc = [c for c in cols if c not in head]
                if mc:
                    if not dry_run:
                        raise ReleaseError(f'{ds} {kind}: 인계표에 없는 v1.3 열 {mc} — 지금 생성기 (v1.3 묶음 · 세대 2 배치) 로 만든 인계표가 아니다')
                    missing.setdefault(ds, [])
                    missing[ds] += [c for c in mc if c not in missing[ds]]
                    cols = [c for c in cols if c in head]
                if kind == 'h12' and not any(_V13_TAU_VALUE_RE.fullmatch(c) for c in cols):
                    warnings.append(f'{ds}: H12 열이 인계표에 없어 H12 부록을 만들지 않았다')
                    continue
                specs[(ds, kind)] = cols
            if not press_ok:
                warnings.append('완료 압력 미검사 (DESC-06) — press_* 열 없음' + (' (dry run)' if dry_run else ' (--pressure-unverified 명시 승인)'))
        files = {}
        for (ds, kind), cols in specs.items():
            hp = hand[ds][0]
            suf = {'main': '', 'physics': '_physics', 'h12': '_h12'}[kind]
            prefix = os.path.join(stage, f'{pre}{ds}_release_{date}_v13{suf}')
            expect = os.path.join(REPO, V13_INPUTS[ds]['expect_ids'])
            if kind == 'main' and dry_run:
                build(hp, cols, prefix)
                for p_ in profile_problems('ml_v1', prefix, hp, expect):
                    if '열 사전이' in p_ or '사전 참조' in p_:
                        warnings.append(f'{ds}: {p_} (세대 1 인계표 사전 문구 — 지금 생성기는 표지를 단다)')
                    else:
                        raise ReleaseError(f'{ds} 프로필 ml_v1 — {p_}')
            else:
                build(hp, cols, prefix, appendix=(kind != 'main'), profile='ml_v1', expect_ids=expect)
            bp = v13_blank_problems(hrows[ds], cols)
            if bp:
                raise ReleaseError(f'{ds} {kind}: 빈칸 뜻 문제 {len(bp)} — ' + ' | '.join(bp[:3]))
        rel_main = {ds: os.path.join(stage, f'{pre}{ds}_release_{date}_v13.csv') for ds in V13_DATASETS}
        by_ds = {}
        for ds in V13_DATASETS:
            h, rr = _read_csv(rel_main[ds])
            by_ds[ds] = (h, [dict(zip(h, r)) for r in rr])
        tables, drows = v13_ml_table(by_ds)
        for ds, (mc, mr) in tables.items():
            mp_ = os.path.join(stage, f'{pre}{ds}_mltable_{date}_v13')
            _v13_write_csv(mp_ + '.csv', mc, mr)
            with open(mp_ + '_columns.tsv', 'w', encoding='utf-8', newline='') as f:
                w = csv.writer(f, delimiter='\t', lineterminator='\n')
                w.writerow(['column', 'role', 'source_column', 'blank_codes', 'meaning'])
                for d in drows:
                    if d['dataset'] == ds:
                        w.writerow([d['column'], d['role'], d['source_column'], d['blank_codes'], d['meaning']])
        fit = refit_from_csv(rel_main, dry_run=dry_run)
        _v13_write_refit(fit, stage, pre, dry_run)
        ctx = {'date': date, 'dry_run': dry_run, 'gens': gens, 'missing': missing, 'warnings': warnings, 'hand': hand, 'hrows': hrows,
               'by_ds': by_ds, 'tables': tables, 'fit': fit, 'codex_verdict': _v13_rel(codex_verdict) if codex_verdict else None,
               'manifest': man_info, 'tau_reread': tau_reread, 'press_ok': press_ok, 'specs': specs, 'stage': stage, 'pre': pre,
               'h12': any(k[1] == 'h12' for k in specs), 'transfer': tt, 'code_identity': code_identity, 'gate': gate,
               'gate_files': (gate or {}).get('files'), 'diagnostic': bool(diagnostic)}
        with open(os.path.join(stage, f'{pre}README.md'), 'w', encoding='utf-8', newline='') as f:
            f.write(_v13_readme(ctx))
        for root, _dirs, fs in os.walk(stage):
            for n in sorted(fs):
                p_ = os.path.join(root, n)
                files[os.path.relpath(p_, stage).replace(os.sep, '/')] = _sha256(p_)
        import numpy
        import matplotlib
        man = {'schema': V13_MANIFEST_SCHEMA, 'dry_run': bool(dry_run), 'date': date, 'generation': gens, 'tau_reread': tau_reread,
               'codex_verdict': ctx['codex_verdict'], 'batch_manifest': man_info, 'pressure_verified': bool(press_ok),
               'missing_columns': missing, 'warnings': warnings, 'h12_appendix': ctx['h12'],
               'transfer_text': ({k: v for k, v in tt.items() if k != 'text'} if tt else None),
               'code_identity': code_identity, 'batch_gate_files': (gate or {}).get('files'), 'diagnostic': bool(diagnostic),
               'batch_gate': ({k: v for k, v in gate.items() if k != 'files'} if gate else None),
               'handover': {ds: {'file': _v13_rel(hand[ds][0]), 'sha256': _sha256(hand[ds][0]), 'rows': len(hrows[ds]), 'cols': len(hand[ds][1])}
                            for ds in V13_DATASETS},
               'code': {n: _sha256(os.path.join(REPO, 'scripts', n)) for n in ('lhs_release_build.py', 'lhs_design_dataset.py', 'tau_flux.py',
                                                                                 'generate_comparison_plots.py')},
               'python': sys.version.split()[0], 'numpy': numpy.__version__, 'matplotlib': matplotlib.__version__,
               'files': dict(sorted(files.items()))}
        with open(os.path.join(stage, f'{pre}{V13_MANIFEST_NAME}'), 'w', encoding='utf-8', newline='') as f:
            f.write(json.dumps(man, ensure_ascii=False, indent=1, sort_keys=True) + '\n')
        cp = check_v13(stage, handover_dir, dry_run=dry_run, diagnostic=diagnostic)
        if cp:
            raise ReleaseError(f'만든 묶음 대조 실패 {len(cp)} — ' + ' | '.join(cp[:4]))
        if os.path.isdir(out_abs):
            os.rmdir(out_abs)
        os.rename(stage, out_abs)
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return {'out_dir': out_abs, 'dry_run': dry_run, 'diagnostic': bool(diagnostic), 'generation': gens, 'missing_columns': missing,
            'warnings': warnings, 'tau_reread': tau_reread, 'n_files': len(files)}


def check_v13(release_dir, handover_dir, dry_run=False, diagnostic=False):
    """v1.3 묶음 대조 — 문제 목록 ([] = 통과).  빌드 manifest 의 파일 sha256 · 배포 ⊆ 인계표 (주 = 프로필 ml_v1 · 부록 = appendix) · 빈칸 일관성 ·
    ML 표 = 배포에서 다시 만든 표 (글자 그대로) · se_isolated 항등식 · 세대 (실제 = g2) · 재적합 재현 (상대 1e-9) · README 표지 ·
    ★ 10-07 G2RR3-01 실제 경로 = 배치 관문을 빌드가 기록한 배치 뿌리에서 **같은 함수** (`v13_batch_gate_problems`) 로 다시 판정 · 빌드 기록 (sha256 · 판정 필드) ·
    배치 manifest sha256 = 지금 파일 · 관문 모드 = 대조 모드.  diagnostic = 진단 묶음 대조 (관문 문제는 기록된 대로 두고 NOT FOR RELEASE 표지를 본다 —
    배포 대조 (diagnostic False) 는 진단 묶음을 거부한다)."""
    pre = _v13_prefix(dry_run)
    probs = []
    mpath = os.path.join(release_dir, f'{pre}{V13_MANIFEST_NAME}')
    try:
        man = json.load(open(mpath, encoding='utf-8'))
    except (OSError, ValueError) as e:
        return [f'빌드 manifest {os.path.basename(mpath)} 를 못 읽었다 ({type(e).__name__})']
    if man.get('schema') != V13_MANIFEST_SCHEMA:
        probs.append(f'빌드 manifest schema {man.get("schema")!r} ≠ {V13_MANIFEST_SCHEMA!r} — 지금 생성기의 묶음이 아니다 (옛 빌드 = 배치 관문 판정 기록 없음 · G2RR3-01)')
    if bool(man.get('dry_run')) != bool(dry_run):
        probs.append(f'빌드 manifest dry_run {man.get("dry_run")!r} ≠ 대조 모드 {dry_run!r}')
    if diagnostic and dry_run:
        probs.append('진단 (--diagnostic-batch-gate) 과 dry-run 을 함께 대조하지 않는다 — 진단은 실제 경로 (배치 관문) 에만')
    if bool(man.get('diagnostic')) != bool(diagnostic):
        probs.append(f'빌드 manifest diagnostic {man.get("diagnostic")!r} ≠ 대조 모드 {diagnostic!r}'
                     + (f' — 진단 묶음 ({V13_DIAG_BANNER}) 은 배포가 아니다 (G2RR3-01)' if man.get('diagnostic') else ''))
    date = man.get('date')
    for rel, sha in (man.get('files') or {}).items():
        p = os.path.join(release_dir, rel)
        if not os.path.isfile(p):
            probs.append(f'파일 없음: {rel}')
        elif _sha256(p) != sha:
            probs.append(f'sha256 다름: {rel}')
    LDD = _ldd()
    by_ds = {}
    for ds in V13_DATASETS:
        try:
            hp = _v13_handover(handover_dir, ds)
        except ReleaseError as e:
            probs.append(str(e))
            continue
        hh, hr = _read_csv(hp)
        hrows = [dict(zip(hh, r)) for r in hr]
        g, gp = v13_generation_problems(hrows, dry_run=dry_run)
        probs += [f'{ds}: {p}' for p in gp]
        if (man.get('generation') or {}).get(ds) != g:
            probs.append(f'{ds}: 빌드 manifest 세대 {(man.get("generation") or {}).get(ds)!r} ≠ 인계표 {g!r}')
        expect = os.path.join(REPO, V13_INPUTS[ds]['expect_ids'])
        for suf, appx in (('', False), ('_physics', True), ('_h12', True)):
            prefix = os.path.join(release_dir, f'{pre}{ds}_release_{date}_v13{suf}')
            if not os.path.isfile(prefix + '.csv'):
                if suf != '_h12':
                    probs.append(f'{ds}: 배포 파일 없음 {os.path.basename(prefix)}.csv')
                continue
            pp = check(hp, prefix, appendix=appx, profile=None if (dry_run and not appx) else 'ml_v1', expect_ids=expect)
            probs += [f'{ds}{suf}: {p}' for p in pp]
            if dry_run and not appx:
                probs += [f'{ds}: {p}' for p in profile_problems('ml_v1', prefix, hp, expect) if not ('열 사전이' in p or '사전 참조' in p)]
            rh, rr = _read_csv(prefix + '.csv')
            rrows = [dict(zip(rh, r)) for r in rr]
            hk = {r[KEY]: r for r in hrows}
            probs += [f'{ds}{suf}: {p}' for p in v13_blank_problems([hk.get(r[KEY], r) for r in rrows], rh)]
            if suf == '':
                by_ds[ds] = (rh, rrows)
                if 'se_isolated_pct' in rh:
                    probs += [f'{ds}: {p}' for p in v13_se_isolated_problems(rrows)]
                elif not dry_run:
                    probs.append(f'{ds}: 주 표에 se_isolated_pct 가 없다')
    if len(by_ds) == len(V13_DATASETS):
        try:
            tables, drows = v13_ml_table(by_ds)
        except ReleaseError as e:
            probs.append(f'ML 표를 다시 만들 수 없다 — {e}')
            tables = {}
        for ds, (mc, mr) in tables.items():
            mp = os.path.join(release_dir, f'{pre}{ds}_mltable_{date}_v13.csv')
            buf = io.StringIO()
            w = csv.writer(buf, lineterminator='\n')
            w.writerow(mc)
            for r in mr:
                w.writerow([r.get(c, '') for c in mc])
            try:
                got = open(mp, encoding='utf-8', newline='').read()
            except OSError:
                probs.append(f'{ds}: ML 표 없음')
                continue
            if got != buf.getvalue():
                probs.append(f'{ds}: ML 표 ≠ 배포에서 다시 만든 표 (빈칸 코드 · 값 · 열)')
            dec_cols, dec_rows = v13_ml_decode(mc, [dict(zip(mc, row)) for row in list(csv.reader(io.StringIO(got)))[1:]])
            if dec_cols != by_ds[ds][0] or [[r[c] for c in dec_cols] for r in dec_rows] != [[r.get(c, '') for c in dec_cols] for r in by_ds[ds][1]]:
                probs.append(f'{ds}: ML 표 되읽기 ≠ 배포 열 · 값')
        try:
            fit = refit_from_csv({ds: os.path.join(release_dir, f'{pre}{ds}_release_{date}_v13.csv') for ds in V13_DATASETS}, dry_run=dry_run)
            sp = os.path.join(release_dir, f'{pre}{REFIT_STEM}_summary.json')
            d = _v13_close(json.load(open(sp, encoding='utf-8')), json.loads(json.dumps(fit['summary'], ensure_ascii=False, sort_keys=True)))
            if d:
                probs.append(f'재적합 요약 ≠ 다시 적합한 값 (refit) — {d}')
            rp = os.path.join(release_dir, f'{pre}{REFIT_STEM}_rows.csv')
            rh_, rr_ = _read_csv(rp)
            d2 = _v13_rows_close([dict(zip(rh_, r)) for r in rr_], fit['rows'])
            if d2:
                probs.append(f'재적합 행 표 ≠ 다시 적합한 값 (refit) — {d2}')
        except (ReleaseError, OSError, ValueError) as e:
            probs.append(f'재적합 재현 실패 (refit) — {type(e).__name__}: {e}')
    rd = os.path.join(release_dir, f'{pre}README.md')
    if not os.path.isfile(rd):
        probs.append(f'README 없음 ({pre}README.md)')
    else:
        rtxt = open(rd, encoding='utf-8').read()
        first = (rtxt.splitlines() or [''])[0]
        if dry_run and V13_DRY_BANNER not in first:
            probs.append('dry-run README 첫 줄에 "DRY RUN — not a release" 표지가 없다')
        if not dry_run and 'DRY RUN' in rtxt:
            probs.append('실제 배포 README 에 DRY RUN 표지가 있다')
        if diagnostic and V13_DIAG_BANNER not in first:
            probs.append(f'진단 README 첫 줄에 "{V13_DIAG_BANNER}" 표지가 없다')
        if not diagnostic and 'NOT FOR RELEASE' in rtxt:
            probs.append('배포 README 에 NOT FOR RELEASE 표지가 있다 — 진단 묶음이다 (G2RR3-01)')
    if not dry_run:
        if man.get('tau_reread') != 'performed':
            probs.append(f'τ 다시 읽기 {man.get("tau_reread")!r} — 실제 배포는 load_tau_results 로 다시 읽어야 한다')
        if not man.get('codex_verdict'):
            probs.append('빌드 manifest 에 Codex 판정문이 없다')
        ci = man.get('code_identity')
        if not isinstance(ci, dict) or not isinstance(ci.get('sealed_changed'), list) or not ci.get('sealed'):
            probs.append('빌드 manifest 에 발사 봉인 대조 (code_identity) 가 없다 — 실제 배포는 배치 manifest code_hashes 와 대조한 뒤에만')
        else:
            un = [f for f in ci['sealed_changed'] if f not in (ci.get('allowed') or [])]
            if un:
                probs.append(f'발사 봉인과 다른 파일 {un} 이 명시 승인 (--allow-seal-diff) 목록에 없다')
        #  ★ 10-07 G2RR3-01 — 배치 관문을 빌드가 기록한 배치 뿌리에서 같은 함수로 다시 판정 (옛 판: 빌드 manifest 의 기록이 읽히는 정수 n_fail 일 때만 봤다 —
        #    기록이 없거나 · null 이면 검사 0 · 감사 판정은 보지 않았다).  빌드 기록 = 지금 배치 뿌리의 기록 (빌드 뒤 증거 교체 · 기록 고침을 잡는다)
        probs += v13_batch_gate_recheck(man, diagnostic=diagnostic)
    return probs


def v13_batch_gate_recheck(man, diagnostic=False):
    """check_v13 의 배치 관문 재판정 (실제 경로) — 빌드 manifest (dict) → 문제 목록.  batch_gate (스키마 · 모드 = 대조 모드 · 배치 뿌리) 가 있어야 ·
    그 배치 뿌리에서 `v13_batch_gate_problems` (build_v13 · 단계 A 와 같은 함수) 를 다시 돌린다 → 기록 ≠ 지금 · manifest sha256 ≠ 지금 · (배포 대조면) 관문 문제."""
    bg = man.get('batch_gate')
    want = 'diagnostic' if diagnostic else 'release'
    if not isinstance(bg, dict) or bg.get('schema') != V13_GATE_SCHEMA or not isinstance(bg.get('batch_root'), str) or not bg.get('batch_root'):
        return [f'빌드 manifest 에 배치 관문 결과 (batch_gate · {V13_GATE_SCHEMA}) 가 없다 — 실제 배포는 ⓪ 감사 · ⓪b 다시 읽기를 판정한 빌드만 (G2RR3-01)']
    probs = []
    if bg.get('mode') != want:
        probs.append(f'빌드 관문 모드 {bg.get("mode")!r} ≠ 대조 모드 {want!r}'
                     + (f' — 진단 묶음 ({V13_DIAG_BANNER}) 은 배포로 대조하지 않는다 (G2RR3-01)' if bg.get('mode') == 'diagnostic' else ''))
    br = bg['batch_root']
    if not os.path.isdir(br):
        return probs + [f'빌드가 판정한 배치 뿌리 {br} 가 없다 — 배치 관문을 다시 판정할 수 없다 (G2RR3-01 · check_v13 은 같은 관문을 다시 돈다)']
    rec_now, gp_now = v13_batch_gate_problems(br)
    rec = man.get('batch_gate_files') if isinstance(man.get('batch_gate_files'), dict) else {}
    diff = [n for n in V13_BATCH_GATE_FILES if rec.get(n) != rec_now.get(n)]
    if diff:
        probs.append(f'빌드 manifest 의 배치 관문 기록 ≠ 지금 배치 뿌리 {diff} (sha256 · 판정 필드) — 빌드 뒤 증거가 바뀌었거나 기록이 고쳐졌다 (G2RR3-01)')
    m_now = _sha256_or_none(os.path.join(br, 'manifest.json'))
    if bg.get('manifest_sha256') != m_now or (man.get('batch_manifest') or {}).get('sha256') != m_now:
        probs.append(f'배치 manifest sha256 (지금 {str(m_now)[:12]}…) ≠ 빌드 기록 — 빌드 뒤 배치 manifest 가 바뀌었다 (G2RR3-01)')
    if not diagnostic:
        probs += [f'배치 관문 (G2RR3-01) {p}' for p in gp_now]
    return probs


def _v13_fmt(x, nd=3):
    return '—' if x is None else (f'{x:.{nd}f}' if isinstance(x, float) else str(x))


def _v13_readme(ctx):
    """v1.3 README — 수 · 파일 · sha256 은 산출에서 센다 (손으로 적지 않는다).  1저자가 보내기 전에 읽고 고친다 (판정문 문안이 다르면 판정문 우선)."""
    d, dry, pre, st = ctx['date'], ctx['dry_run'], ctx['pre'], ctx['stage']
    fit = ctx['fit']['summary']
    fr, lk = fit['fits']['free'], fit['fits']['locked']
    gen_txt = ' · '.join(f'{ds} = `{ctx["gens"][ds]}`' for ds in V13_DATASETS)
    L = []
    if dry:
        L += [f'> ⚠ {V13_DRY_BANNER} — 세대 1 원천 (커밋된 v1.2 인계표) 으로 v1.3 생성기 경로만 돌린 것.  수영 님께 보내지 않는다 · 값 인용 금지.', '']
    if ctx.get('diagnostic'):
        _gp = (ctx.get('gate') or {}).get('problems') or []
        L += [f'> ⚠ {V13_DIAG_BANNER} — 배치 관문 증거 (⓪ 감사 · ⓪b 다시 읽기) 가 통과가 아닌 채 진단 모드 (--diagnostic-batch-gate) 로 만든 것 '
              f'(문제 {len(_gp)} · "외부 검토" 절).  수영 님께 보내지 않는다 · 값 인용 금지 · check_v13 배포 대조는 이 묶음을 거부한다 (G2RR3-01).', '']
    L += [f'# LHS 구조 디스크립터 — 배포 v1.3 최종판 ({d} · 접촉망 세대 {ctx["gens"].get("lhs")})', '',
          '> 수영 님 ML 용 구조 디스크립터 + 접촉망 수송 지표 — **v1.3 = 최종판** (1저자 10-06 밤 *"v1.3 에 최종이라고 하고 확실하게 넘겨주자"*).',
          '> v1.2 (`docs/data/lhs_release_20261006_v12/`) 의 열 · 값 규약을 이어받고 더한 것: **세대 2 망 값** · **ML 표 (빈칸 뜻 코드 · #1)** · '
          '**f 타깃 + 관통 분류 안내 (#2)** · **porosity–σ–CN 재적합 (#5)** · 표시 이름 **수송 tortuosity** · 새 열 **`se_isolated_pct`**.',
          f'> 정본 인계표 = {" · ".join("`" + _v13_rel(ctx["hand"][ds][0]) + "`" for ds in V13_DATASETS)} · 재현 명령 = §10.', '',
          '## 외부 검토 — 먼저 읽을 것', '']
    if dry:
        L += ['- (dry run) Codex 판정 · 배치 manifest · τ 다시 읽기 없음 — 이 묶음은 생성기 시험 산출이다.']
    else:
        mi = ctx['manifest'] or {}
        if ctx.get('transfer'):
            L += [f'> **전달 문단 (판정문 그대로 · `{ctx["transfer"]["file"]}` · sha256 `{ctx["transfer"]["sha256"]}`)**:', '>']
            L += [('> ' + ln) if ln.strip() else '>' for ln in ctx['transfer']['text'].splitlines()]
            L += ['']
        L += [f'- Codex 세대 2 판정문 (GO): `{ctx["codex_verdict"]}` — 이 배포는 GO 뒤에만 만든다.  판정문의 전달 문안이 이 README 와 다르면 **판정문이 우선**이다.',
              f'- 배치 manifest: `{mi.get("path")}` (sha256 `{mi.get("sha256")}` · expected_network_generation = `{mi.get("expected_network_generation")}`) · '
              f'τ 다시 읽기 (생성기 `load_tau_results` · 같은 기대 세대 · 인계표 τ 칸 대조) = **{ctx["tau_reread"]}**.']
        ci, gf, gt = ctx.get('code_identity') or {}, ctx.get('gate_files') or {}, ctx.get('gate') or {}
        hc = ci.get('handover_changed')
        L += [f'- 코드 신원 (세대 2 등록 §3): 발사 봉인 (배치 manifest `code_hashes`) {ci.get("sealed")} 파일 — '
              + ('이 빌드 체크아웃과 **같다**' if not ci.get('sealed_changed') else
                 f'다른 파일 {ci.get("sealed_changed")} = **명시 승인 `--allow-seal-diff`** (값과 무관한 변경이라는 판단 — 1저자)')
              + ' · 인계 생성기 · 다시 읽기 도구 (`handover_code_hashes`) '
              + ('기록 없음 (대조 못 함)' if hc is None else ('= 발사 기록' if not hc else f'**≠ 발사 기록** {hc} (v1.3 생성기 변경 — 등록 §9 에 이 커밋)'))
              + f' · 빌드 git HEAD `{ci.get("git_head")}` · 커밋 안 된 추적 파일 변경 {ci.get("git_dirty_tracked")} 줄.',
              '- 배치 관문 (등록 §5-2 · §5-3 · ★ G2RR3-01 — 두 기록 필수 · build · 단계 A · check_v13 이 같은 판정 `v13_batch_gate_problems`): ' + ' · '.join(
                  f'`{n}` ' + ('**없음**' if gf.get(n) is None else f'sha256 `{gf[n]["sha256"]}`'
                                + (f' (n_fail {gf[n].get("n_fail")} · 기대 세대 `{gf[n].get("expected_generation")}` · 등록 집합 `{gf[n].get("expected_set")}` '
                                   f'{gf[n].get("read_n")}/{gf[n].get("expected_n")})' if n == 'reread.json'
                                   else f' (봉인 판정 {gf[n].get("verdicts")} · merged {gf[n].get("merged")})'))
                  for n in V13_BATCH_GATE_FILES)
              + (f' — **통과**: ⓪ 감사 = 실행 형식 자격 current · 봉인 판정 {"/".join(V13_AUDIT_SEALED)} 만 {V13_REREAD_N} · merged same · 등록 ID · 기대 세대 '
                 f'{V13_GENERATION} · 세대 · 입력 지문 · import 관측 문제 0 / ⓪b 다시 읽기 = n_fail 0 · {V13_GENERATION} · {V13_REREAD_SET} '
                 f'{V13_REREAD_N}/{V13_REREAD_N} · 둘 다 이 배치 뿌리 (`{_v13_rel(gt.get("batch_root") or "")}`) · 이 manifest · 이 발사 봉인 지문의 기록'
                 if not gt.get('problems') else
                 f' — **문제 {len(gt["problems"])} ({V13_DIAG_BANNER})**: ' + ' | '.join(gt['problems'][:8]))]
    L += [f'- 완료 압력 (DESC-06): ' + ('`press_*` 열 — 압밀 루프가 목표 300 MPa 에서 빠져나온 기록 (마지막 프레임 응력이 아니다)' if ctx['press_ok']
                                      else '**미검사** (press_* 열 없음)'),
          '- 5차 판정 (`docs/reviews/codex_review_rglr3_reverify_20261006.md` §6 · §7) 의 사용 조건은 그대로다: 모델 내부 ML 기술자 · 기본 = Hertz · '
          'Physics = opt-in 부록 · 상태 열 필수 · 실험 절대값 타깃 · 실물 순위 · COMSOL 물성 대입 금지 · T ≥ 1 이나 상태 OK 도 물리 정확도 인증이 아니다.', '',
          '## 0. 바뀐 것 (v1.2 → v1.3)', '', '| 무엇 | 내용 |', '|---|---|',
          (f'| 망 세대 | {gen_txt} — Physics = ψ 곱셈 · 면적 physics_g2 · 정확 Dirichlet 전극 '
           '(세대 2 · 1저자 비준 10-06 저녁) · Hertz (H0) 간선은 세대 1 과 같고 전극만 바뀌었다 (σ 상대 ~1e-5) |')
          if all(g == V13_GENERATION for g in ctx['gens'].values()) else
          (f'| 망 세대 | {gen_txt} — **세대 2 가 아니다** (dry run · 세대 1 원천 — 실제 v1.3 은 세대 2 배치 값만 싣는다 · 생성기가 거부) |'),
          '| 새 열 | `se_isolated_pct` (고립 전해질 · §5) · 세대 2 출처 `ion_net_generation` · `ion_net_constriction_hertz` · `ion_net_area_rule_hertz` · '
          '`ion_net_electrode_hertz` · `ion_net_bulk_hertz` (194 행 상수 — 출처 표지)' + (' · 완료 압력 `press_target_mpa` · `press_last_loop_mpa` · `press_reached`'
                                                                                       if ctx['press_ok'] else '') + ' |',
          f'| ML 표 (#1) | `{pre}<ds>_mltable_{d}_v13.csv` — 배포 열 + 빈칸 코드 열 (`<열>__blank`) + `dataset` + 관통 분류 `{V13_ML_CLASS}` (§2 · §3) |',
          f'| 재적합 (#5) | `{pre}{REFIT_STEM}_*` + `origin/` + `previews/` (§6) |',
          '| 표시 이름 | `tau2_ion_*` = **수송 tortuosity** (제곱근 아님) — 열 사전 · 웹앱 · COMSOL 2D 내보내기 같은 이름 (§4) |']
    if ctx['missing']:
        L += [f'| (dry run) 빠진 v1.3 열 | ' + ' · '.join(f'{ds}: {", ".join(v)}' for ds, v in ctx['missing'].items()) + ' — 세대 1 인계표에 없다 |']
    L += ['', '## 1. 파일', '', '| 파일 | 행 × 열 | sha256 |', '|---|---|---|']
    for root, _dirs, fs in sorted(os.walk(st)):
        for n in sorted(fs):
            if n in (f'{pre}README.md', f'{pre}{V13_MANIFEST_NAME}'):     # 자기 자신 · manifest 는 아래 한 줄 (쓰는 중인 파일의 해시를 적지 않는다)
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, st).replace(os.sep, '/')
            if n.endswith('.csv'):
                with open(p, encoding='utf-8-sig', newline='') as f:
                    rr = list(csv.reader(f))
                shape = f'{len(rr) - 1} × {len(rr[0]) if rr else 0}'
            else:
                shape = '—'
            L.append(f'| `{rel}` | {shape} | `{_sha256(p)}` |')
    L += [f'| `{pre}README.md` · `{pre}{V13_MANIFEST_NAME}` | — | (빌드 manifest 가 모든 파일의 sha256 을 적는다) |', '',
          '한 행 = 한 침대 (300 MPa 압밀 뒤 한 프레임) · `case_id` 키 · 행 순서 = v1.2 와 같다.  두 데이터셋을 합칠 때는 `dataset` 표지를 둔다 (ML 표에는 있다).', '',
          '## 2. 빈칸 뜻 (#1 — ML 표)', '',
          '배포 CSV 의 빈칸은 뜻이 여럿이다 — **0 으로 채우지도, 한꺼번에 버리지도 않는다.**  ML 표는 배포 값 칸을 그대로 두고 (채우지 않았다 · 되읽기 검산), '
          '빈칸이 있는 열마다 바로 뒤에 `<열>__blank` (코드 · 값이 있는 칸은 빈칸) 를 붙였다.  코드 규칙은 같은 행의 설계 `block` · 접촉 개수 · 상태 열이 정하고, '
          '규칙에 없는 빈칸이나 빈칸이어야 할 칸의 값이 하나라도 있으면 생성기가 만들기를 거부한다.', '',
          '| 코드 | 뜻 | 130 | 64 |', '|---|---|---|---|']
    cnt = {ds: collections.Counter(v for o in ctx['tables'][ds][1] for k, v in o.items() if k.endswith(V13_ML_SUFFIX) and v) for ds in ctx['tables']}
    for k, v in V13_BLANK_CODES.items():
        L.append(f'| `{k}` | {v} | {cnt.get("lhs", {}).get(k, 0)} | {cnt.get("lhsx", {}).get(k, 0)} |')
    L += ['', '- 쓰는 법: `NA_*` = 결측 표지 (그 특징을 못 쓰는 행 — 0 대입 금지 · 모델이 결측을 못 받으면 표지 열과 함께) · `INF_NOT_PERCOLATING` = T · √T 의 '
          '무한대 (회귀 타깃으로 쓰지 말고 §3 의 분류 가지로) · `NOT_COMPUTED` · `HOLD_BAND_FALLBACK` = 그 칸만 제외 사유 (무한대 아님) · `EMPTY_NO_REASON` = 빈 집합.',
          f'- 열 역할 = ML 열 사전 (`{pre}<ds>_mltable_{d}_v13_columns.tsv` 의 role) — ' + ' · '.join(f'`{k}` {v}' for k, v in V13_ROLE_MEANING.items()) + '.', '',
          '## 3. 타깃 — `f_ion_hertz` 와 관통 분류 (#2)', '']
    for ds in V13_DATASETS:
        sc = _v13_status_counts(ctx['by_ds'][ds][1], 'ion_net_status_hertz')
        L.append(f'- {ds} 상태 (`ion_net_status_hertz`): ' + ' · '.join(f'{k} {v}' for k, v in sc.items()))
    L += ['- **이온 수송 타깃은 `f_ion_hertz`** (= σ_eff/σ₀ · 무차원 · 유한 — 비관통 행 = **0.0 = 물리적 0**, 결측이 아니다).  `tau2_ion_hertz` (수송 tortuosity T) · '
          '`tau_ion_hertz` (√T) 는 비관통에서 ∞ (빈칸) 라 그대로는 회귀 타깃이 아니다 · T = φ_SE,mc / f 항등식이라 **f 를 예측하면서 T · √T 를 특징으로 넣지 않는다**.',
          f'- **2 단계 (권장)**: ① 관통 분류 `{V13_ML_CLASS}` (ML 표 · 1 = 관통 · 0 = 비관통 · `percolation_pct > 0` 과 같은 판정) → ② 관통 행에서 f (또는 폴드 안에서 고른 '
          '변환 log f) 회귀.  예측 f = P(관통) × E[f | 관통] 로 묶을 수 있다 (hurdle).  비관통 행을 지우면 전도 가능한 하위집합만 남는다 — 지우지 않는다.',
          '- 고립 열은 비관통 침대에 몰린다 → **관통 여부를 먼저 분류**한다 (평균 · 최대, 관통 / 비관통):']
    for ds in V13_DATASETS:
        s = _v13_iso_stats(ctx['by_ds'][ds][1])
        parts = []
        for col in ('am_ionic_isolated_pct', 'se_isolated_pct'):
            a, b = s.get(f'{col}:perc'), s.get(f'{col}:nonperc')
            if a and a[0]:
                parts.append(f'`{col}` 관통 {_v13_fmt(a[1], 1)} · 최대 {_v13_fmt(a[2], 1)} / 비관통 {_v13_fmt(b[1], 1) if b[0] else "—"} · '
                             f'최대 {_v13_fmt(b[2], 1) if b[0] else "—"} (n {a[0]} · {b[0]})')
        L.append(f'  - {ds}: ' + (' · '.join(parts) if parts else '(열 없음)'))
    L += ['- 다른 모드 — Physics 부록 = opt-in (기본 학습 열 아님 · 면적과 협착식이 함께 다른 규약의 결합 민감도 · Codex QV3) · H12 = 민감도 부록 '
          + ('(이 묶음에 있다 · 부록 전용)' if ctx['h12'] else '(이 묶음에 없다)') + '.', '',
          '## 4. 표시 이름 — 수송 tortuosity (τ 명명 규약)', '', '| 열 | 이름 · 뜻 |', '|---|---|',
          '| `tau2_ion_<모드>` | **수송 tortuosity** T = φ_SE,mc / f (**제곱근 아님** = 문헌의 tortuosity factor · Tjaden κ = τ² · Landesfeind τ · COMSOL τ_F) · 키는 tau2 그대로 |',
          '| `tau_ion_<모드>` | √T (유도량) — "수송 tortuosity" 라 부르지 않는다 · Dijkstra 경로 길이비의 뜻도 아니다 · COMSOL 입력 아님 |',
          '| `f_ion_<모드>` | f = σ_eff/σ₀ (무차원) — 판 간격 해를 질량보존 두께로 재척도한 값 (L_mc 에서 다시 푼 해가 아니다) |',
          '| `tortuosity_SE_wall` | **기하학적 tortuosity** — 경계 띠 SE 중심 쌍의 최단경로 / 그 쌍의 z 간격 (수송 τ 아님 · 수송 쪽 짝 = `tau2_ion_hertz`) |', '',
          '## 5. 새 열 `se_isolated_pct` (고립 전해질)', '',
          '- = **100 − `top_reachable_pct`** — 등록된 상단 2r 경계 띠 (분리막 쪽) 와 SE 접촉 그래프로 이어지지 않은 SE 의 비율 (%).  AM 경로 고립 '
          '(`am_ionic_isolated_pct` = 100 − `ionic_active_pct`) 과 같은 규칙 · 생성기가 유도 (재실행 없음) · 관문 S1 (= 100 − top) · S2 (≤ 100 − `percolation_pct`).',
          '- 한정: 분리막 쪽 띠에 앉은 외톨이 SE (접촉 0) 를 연결로 세어 고립을 **약간 적게** 잡는다 · 큰 값은 비관통 침대에 몰린다 (§3) → 관통 분류 먼저.',
          '- 그래프 지표다 — 실제 분리막 접촉 · 계면 저항 · 이온 전류를 계산하지 않는다.', '',
          '## 6. porosity–σ–CN 재적합 (#5)', '',
          f'- 대상: {fit["target"]} · n = {fit["n_fit"]} (' + ' · '.join(f'{k} {v}' for k, v in fit['n_fit_by_dataset'].items()) + ') · 적합 밖: '
          + (' · '.join(f'{k} {v}' for k, v in fit['excluded'].items()) or '없음') + ' (행은 표에 남긴다).',
          f'- φ_eff: {fit["phi_eff"]}.  상수 = σ_ionic T1 등록식 동결값 (φc_P {fit["constants"]["phi_c_P"]} · φc_S {fit["constants"]["phi_c_S"]} · '
          f'δ {fit["constants"]["delta"]} · r_cut {fit["constants"]["r_cut_um"]} µm · 게이트 지수 {fit["constants"]["gate_exponent"]}) — 생산 코드에서 읽었다.', '',
          '| 식 | a | α | β | R² | LOOCV R² | 잔차 sd (ln) | 편향 130 | 편향 64 |', '|---|---|---|---|---|---|---|---|---|']
    for nm, fx in (('locked (½ · 2)', lk), ('free', fr)):
        p, se = fx['params'], fx['se']
        bd = fx['by_dataset']
        L.append(f'| {nm} | {_v13_fmt(p["a"], 3)} ± {_v13_fmt(se.get("a"), 3)} | {_v13_fmt(p["alpha"], 3)}'
                 + (f' ± {_v13_fmt(se.get("alpha"), 3)}' if 'alpha' in se else '') + f' | {_v13_fmt(p["beta"], 3)}'
                 + (f' ± {_v13_fmt(se.get("beta"), 3)}' if 'beta' in se else '')
                 + f' | {_v13_fmt(fx["r2"], 3)} | {_v13_fmt(fx["loocv_r2"], 3)} | {_v13_fmt(fx["resid_sd"], 3)} | '
                 f'{_v13_fmt((bd.get("lhs") or {}).get("bias"), 3)} | {_v13_fmt((bd.get("lhsx") or {}).get("bias"), 3)} |')
    L += ['', f'- 파일: `{pre}{REFIT_STEM}_rows.csv` (행마다 φ_eff · 예측 · 잔차) · `{pre}{REFIT_STEM}_summary.json` · Origin 워크시트 `origin/` (1 줄 Long Name · '
          f'2 줄 Units · GUIDE) · 미리보기 `previews/{pre}v13_refit_porosity_sigma_cn.png` · `.svg`.',
          '- 한정: ' + ' · '.join(fit['caveats']) + '.', '',
          '## 7. Physics 부록 (opt-in) · H12', '']
    for ds in V13_DATASETS:
        sc = _v13_status_counts(ctx['hrows'][ds], 'ion_net_status_physics')
        L.append(f'- {ds} Physics 상태: ' + ' · '.join(f'{k} {v}' for k, v in sc.items()))
    L += ['- 기본 학습 열에 자동 포함하지 않는다 · `MODEL_BELOW_CONTINUUM_BOUND` 행은 값 유지 + 표지 — 그 행만 지우고 나머지 Physics 의 타당성을 주장하지 않는다 (Codex QV3).',
          '- 세대 2 Physics = ψ 곱셈 + 면적 physics_g2 + 정확 Dirichlet (출처 표지 열 — 부록에 있다) · Hertz 와 Physics 의 차이를 "소성 접촉 면적만의 민감도" 로 읽지 않는다.', '',
          '## 8. 규약 (v1.2 README §3 · §4 그대로 — 요지)', '',
          '- 상태 열 (`ion_net_status_hertz`) 을 값과 같이 읽는다 · 숫자 열만 골라 dropna / 0 채움 하는 학습 코드는 충분하지 않다 (Codex QV2).',
          '- 항등식 묶음에서 하나만 독립 타깃: ε + φ_SE,mc + φ_AM,mc = 1 · T = φ_SE,mc/f · √T · `se_isolated_pct` = 100 − `top_reachable_pct` · `am_ionic_isolated_pct` = 100 − '
          '`ionic_active_pct` · 이온 분할 셋 = 100 · 파괴 · 면적 · F1 항등식 (v1.2 §3-2).',
          '- 총량 열 (`area_*_total` · `n_*` · 개수) 은 정규화해서 쓴다 · CN · 비율 열에는 벽 효과가 섞여 있다 (`wall_touch_frac_*`).',
          '- σ basis — `f_ion_hertz` × σ₀ (3.0 mS/cm) 는 L_mc 재척도 σ 다 (웹앱 화면 · 보고 덱의 판 간격 해와 무표지 혼용 금지 · Codex QV5).',
          '- 적격성 HOLD (`physical_target_status`) 는 그대로 — 행을 지우지 않는다 · 에뮬레이터 (HOLD 포함) ↔ 물리 타깃 후보 (HOLD 불허) 를 구분해 보고한다.',
          '- 변수 선택 · 스케일링 · 변환 · 초매개변수는 학습 폴드 안에서 (중첩 CV) · 130 ↔ 64 이동 성능을 무작위 CV 와 따로 보고한다.', '',
          '## 9. AI 도구에 붙여 넣을 프롬프트', '', '```',
          f'너는 고체전지 복합 양극 DEM 시뮬레이션 데이터로 ML 을 하는 조수다.  데이터 = {pre}lhs_mltable_{d}_v13.csv (130 행) · {pre}lhsx_mltable_{d}_v13.csv',
          '(64 행, 전부 SE-rich — 분포가 달라 dataset 표지를 둔다).  한 행 = 300 MPa 로 압밀한 전극 침대 하나.  열 역할은 *_mltable_*_columns.tsv 의',
          'role 열 · 뜻은 배포 *_columns.tsv 와 README (README 가 정정판).  *_physics.csv 는 부록이다 — 요청받기 전에는 쓰지 마라.',
          '1) X = role X 다섯 (am_pct · ps_frac · d_am_p_um · d_am_s_um · d_se_um).  X_DERIVED 는 같은 정보 · CONST · FLAG · ID · STATUS 는 특징이 아니다.',
          '   RESULT_COUNT (실측 입자 수) · 두께 · CN 같은 결과를 설계 → 구조 예측의 X 로 쓰면 누설이다.',
          '2) 빈칸은 <열>__blank 코드가 뜻을 정한다.  0 으로 채우지 마라.  NA_* = 결측 표지 · INF_NOT_PERCOLATING = 무한대 (관통 경로 없음) ·',
          '   NOT_COMPUTED · HOLD_BAND_FALLBACK = 그 칸만 제외 · EMPTY_NO_REASON = 빈 집합.',
          f'3) 이온 수송 타깃 = f_ion_hertz (유한 · 비관통 0.0).  먼저 {V13_ML_CLASS} (1 관통 · 0 비관통) 를 분류하고 관통 행에서 f (또는 폴드 안에서',
          '   고른 log f) 를 회귀하라.  tau2_ion_hertz (수송 tortuosity T) · tau_ion_hertz (√T) 는 role Y_IDENTITY — f 와 항등식 (T = φ_SE,mc/f) 이라',
          '   f 를 예측하면서 특징으로 넣지 마라.  tortuosity_SE_wall 은 기하학적 tortuosity (다른 양) 다.',
          '4) 항등식 열을 독립 타깃처럼 세지 마라 (README §8).  총량 열은 정규화하라.  se_isolated_pct · am_ionic_isolated_pct 는 비관통에 몰린다.',
          '5) physical_target_status = HOLD 행은 지우지 말고 에뮬레이터 (HOLD 포함) 와 물리 타깃 후보 (HOLD 불허) 를 구분해 보고하라.',
          '6) 값은 고정 접촉망 · 면적 · 협착 · 경계 규약의 모델 기술자다 — 실험값 · 실물 순위 · COMSOL 물성으로 바꾸어 쓰지 마라.',
          f'7) {REFIT_STEM}_summary.json 의 식은 이 코퍼스의 근사 관계다 — 지수를 물리 상수로 인용하지 마라.',
          '8) 변수 선택 · 스케일링 · 초매개변수는 학습 폴드 안에서 (중첩 CV) · 130 과 64 의 이동 성능을 따로 · 불확실성을 함께 보고하라.', '```', '',
          '## 10. 재현', '',
          '- 생성기: `scripts/lhs_release_build.py --v13` (단계 A = 인계표 생성기 `scripts/lhs_design_dataset.py --export-handover … --webapp-groups '
          f'{V13_WEBAPP_GROUPS} --tau-results … --tau-batch-manifest …` · 단계 B = 이 묶음 · 대조 `--v13-check`) — 명령 전문 = '
          '`docs/reviews/lhs_release_v13_plan_20261007.md`.',
          f'- 빌드 manifest `{pre}{V13_MANIFEST_NAME}` = 인계표 sha256 · 코드 sha256 · 파일 sha256 · 코드 신원 (발사 봉인 대조 · 명시 승인 · git HEAD) · '
          '배치 관문 기록 (⓪ 감사 · ⓪b 다시 읽기 sha256) · 경고.']
    if ctx['warnings']:
        L += ['', '### 경고 (빌드가 기록)', ''] + [f'- {w}' for w in ctx['warnings']]
    return '\n'.join(L) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description='LHS 배포 표 = 인계표 열 부분집합 (만들기 · 대조)')
    ap.add_argument('--handover', help='정본 인계표 CSV (옆에 _columns.tsv)')
    ap.add_argument('--columns-from', help='열 목록을 첫 열에서 읽을 열 사전 TSV (옛 배포)')
    ap.add_argument('--add', action='append', default=[], help='뒤에 붙일 열 (여러 번)')
    ap.add_argument('--out', help='산출 접두사 (…/<이름> → <이름>.csv · <이름>_columns.tsv)')
    ap.add_argument('--check', action='store_true', help='대조만')
    ap.add_argument('--release', help='대조할 배포 접두사')
    ap.add_argument('--appendix', action='store_true',
                    help='부록 파일 (부록 전용 열 — H12 민감도 `*_hertz_h12` · 열 사전 판정 "부록 전용" — 을 싣는다 · 없으면 그 열을 거부)')
    ap.add_argument('--profile', choices=PROFILES, default=None,
                    help='ML 배포 프로필 (LREL-02 · 03) — 키 유일 · 기대 ID 집합 · 적격성 세 열 · 열 사전 참조 표지 (부록은 키 · ID 만)')
    ap.add_argument('--expect-ids', default=None, help='(--profile) 기대 ID — 설계 CSV (case_id 열) 또는 한 줄 한 ID')
    #  ── v1.3 최종판 (docs/reviews/lhs_release_v13_plan_20261007.md) ──
    ap.add_argument('--v13', action='store_true',
                    help='배포 v1.3 만들기 — 실제: --batch-root (단계 A 인계표 생성 + τ 다시 읽기) · --codex-verdict · --out-dir / '
                         'dry-run: --dry-run --handover-dir (세대 1 원천 허용 · DRYRUN_ 표지 · docs/data 밖)')
    ap.add_argument('--v13-check', action='store_true', help='배포 v1.3 묶음 대조 (--release-dir · --handover-dir · dry-run 묶음이면 --dry-run)')
    ap.add_argument('--batch-root', default=None, help='(--v13) 새 194 배치 뿌리 (manifest.json · merged/<ds>/results · pressure/)')
    ap.add_argument('--handover-dir', default=None, help='(--v13 · --v13-check) 인계표 폴더 (<ds>_handover_*.csv 하나씩 + 열 사전 · τ 출처 부록)')
    ap.add_argument('--handover-out', default=None, help='(--v13 단계 A) 인계표 산출 폴더 (기본 <batch-root>/handover_v13_<date>)')
    ap.add_argument('--out-dir', default=None, help='(--v13) 배포 묶음 폴더 (새 폴더 · 실제 = docs/data/lhs_release_<date>_v13)')
    ap.add_argument('--release-dir', default=None, help='(--v13-check) 대조할 배포 묶음 폴더')
    ap.add_argument('--date', default=None, help='(--v13) 파일 이름 날짜 YYYYMMDD (기본 오늘)')
    ap.add_argument('--dry-run', action='store_true', help='(--v13 · --v13-check) DRY RUN — 세대 1 원천 허용 · 파일 이름 DRYRUN_ · 배포 아님')
    ap.add_argument('--codex-verdict', default=None, help='(--v13 실제) Codex 세대 2 GO 판정문 경로 (README · 빌드 manifest 에 적는다)')
    ap.add_argument('--pressure-record', action='append', default=[], metavar='DS=TSV',
                    help='(--v13 단계 A) 완료 압력 기록 (기본 <batch-root>/pressure/<ds>_pressure_record.tsv)')
    ap.add_argument('--pressure-unverified', action='store_true', help='(--v13) 완료 압력 기록 없이 만든다는 명시 승인 (DESC-06 · README 에 미검사 표지)')
    ap.add_argument('--h12-appendix', action='store_true', help='(--v13) H12 민감도 부록도 만든다 (부록 전용 · 기본 학습 열 아님 — 1저자 결정)')
    ap.add_argument('--transfer-text', default=None,
                    help='(--v13) Codex GO 판정문의 전달 문안 (텍스트 파일) — README 외부 검토 절에 그대로 · sha256 기록 (README 를 손으로 고치지 않는다)')
    ap.add_argument('--allow-seal-diff', action='append', default=[], metavar='FILE',
                    help='(--v13 실제) 발사 봉인 (배치 manifest code_hashes) 과 다른 파일 하나를 명시 승인 (값과 무관한 변경 — 예: 웹앱 화면 문구 · '
                         '여러 번 · README · 빌드 manifest 에 기록).  없으면 봉인 파일이 다를 때 거부한다')
    ap.add_argument('--diagnostic-batch-gate', action='store_true',
                    help='(--v13 · --v13-check 실제 경로) 진단 모드 — 배치 관문 증거 (⓪ 감사 seal_audit.json · ⓪b 다시 읽기 reread.json) 의 결손 · 손상 · 옛 · '
                         '실패 기록을 경고로 남기고 만든다 · README 첫 줄 · 빌드 manifest 에 NOT FOR RELEASE · 리포 밖에만 · --v13-check 배포 대조는 거부 '
                         '(진단 대조는 이 표지와 함께 · G2RR3-01).  없으면 관문 문제 하나라도 = 거부')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    try:
        if a.v13_check:
            if not (a.release_dir and a.handover_dir):
                ap.error('--v13-check 에는 --release-dir 와 --handover-dir 가 필요하다')
            probs = check_v13(a.release_dir, a.handover_dir, dry_run=a.dry_run, diagnostic=a.diagnostic_batch_gate)
            for p in probs:
                print('⛔', p)
            print(('✓ v1.3 묶음 대조 통과' + (f' ({V13_DRY_BANNER})' if a.dry_run else '') + (f' ({V13_DIAG_BANNER})' if a.diagnostic_batch_gate else ''))
                  if not probs else f'✗ 문제 {len(probs)}')
            return 0 if not probs else 3
        if a.v13:
            if not a.out_dir:
                ap.error('--v13 에는 --out-dir 가 필요하다')
            date = a.date or datetime.date.today().strftime('%Y%m%d')
            hdir = a.handover_dir
            if a.dry_run:
                if not hdir:
                    ap.error('--v13 --dry-run 에는 --handover-dir 가 필요하다 (세대 1 원천 = 커밋된 v1.2 인계표 폴더)')
            elif not hdir:
                if not a.batch_root:
                    raise ReleaseError('--v13 (실제) 에는 --batch-root 가 필요하다 (단계 A 인계표 생성 · τ 다시 읽기)')
                if not a.codex_verdict or not os.path.isfile(a.codex_verdict):
                    raise ReleaseError(f'Codex 세대 2 판정문 (GO) 이 없다 ({a.codex_verdict!r}) — 단계 A 전에 멈춘다')
                pr = {}
                for kv in a.pressure_record:
                    k, _, v = kv.partition('=')
                    if k not in V13_DATASETS or not v:
                        raise ReleaseError(f'--pressure-record {kv!r} — DS=TSV (DS = {V13_DATASETS})')
                    pr[k] = v
                hdir = a.handover_out or os.path.join(a.batch_root, f'handover_v13_{date}')
                stage_handovers_v13(a.batch_root, hdir, date, pressure=pr, pressure_unverified=a.pressure_unverified,
                                    allow_seal_diff=a.allow_seal_diff, diagnostic=a.diagnostic_batch_gate)
            rep = build_v13(out_dir=a.out_dir, handover_dir=hdir, batch_root=a.batch_root, date=date, dry_run=a.dry_run,
                            codex_verdict=a.codex_verdict, h12_appendix=a.h12_appendix, pressure_unverified=a.pressure_unverified,
                            transfer_text=a.transfer_text, allow_seal_diff=a.allow_seal_diff, diagnostic=a.diagnostic_batch_gate)
            for w in rep['warnings']:
                print('⚠', w)
            kind = 'DRY RUN 묶음' if a.dry_run else (f'진단 묶음 ({V13_DIAG_BANNER})' if a.diagnostic_batch_gate else '배포 묶음')
            print(f'✓ v1.3 {kind} {rep["out_dir"]} — 파일 {rep["n_files"]} · 세대 {rep["generation"]} · '
                  f'τ 다시 읽기 {rep["tau_reread"]} · 대조 통과 (check_v13)' + (f' · 빠진 v1.3 열 {rep["missing_columns"]}' if rep['missing_columns'] else ''))
            return 0
        if a.check:
            if not (a.handover and a.release):
                ap.error('--check 에는 --handover 와 --release 가 필요하다')
            probs = check(a.handover, a.release, appendix=a.appendix, profile=a.profile, expect_ids=a.expect_ids)
            for p in probs:
                print('⛔', p)
            print('✓ 배포 ⊆ 인계표 (행 · 순서 · 값 · 열 사전)' if not probs else f'✗ 문제 {len(probs)}')
            return 0 if not probs else 3
        if not (a.handover and a.columns_from and a.out):
            ap.error('만들기에는 --handover · --columns-from · --out 이 필요하다')
        _, rows = _read_tsv(a.columns_from)
        cols = [r[0] for r in rows] + list(a.add)
        n, k = build(a.handover, cols, a.out, appendix=a.appendix, profile=a.profile, expect_ids=a.expect_ids)
        probs = check(a.handover, a.out, appendix=a.appendix, profile=a.profile, expect_ids=a.expect_ids)
        if probs:
            for p in probs:
                print('⛔', p)
            return 3
        print(f'✓ {a.out}.csv  {n} 행 × {k} 열 · 대조 통과')
        return 0
    except ReleaseError as e:
        print('⛔', e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
