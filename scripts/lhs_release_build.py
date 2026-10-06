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

키 (case_id) 는 늘 유일해야 한다 (인계표 · 배포 둘 다 — LREL-03).  프로필은 부분집합 충실성 위에 **용도 계약**을 더한다 (범용 부분집합 도구에
모든 용도의 열을 강제하지 않는다 — Codex 배포 v1.1 최종 리뷰 LHSREL-02 해제 조건).
"""
import argparse
import csv
import io
import os
import re
import shutil
import sys
import tempfile

KEY = 'case_id'
#: ★ 10-06 저녁 세대 2 (1저자 비준 C1-3) — 부록 전용 열 = 기본 학습 열 아님 (H12 민감도 = 행마다 [H0, H12] 괄호로 읽는 부록).
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
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    try:
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
