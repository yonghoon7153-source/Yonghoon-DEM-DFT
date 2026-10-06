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
  python3 scripts/lhs_release_build.py --appendix --handover … --columns-from <case_id 한 줄 열 사전> --add tau2_ion_hertz_h12 … --out …_h12
  python3 scripts/lhs_release_build.py --selftest
"""
import argparse
import csv
import io
import os
import re
import sys
import tempfile

KEY = 'case_id'
#: ★ 10-06 저녁 세대 2 (1저자 비준 C1-3) — 부록 전용 열 = 기본 학습 열 아님 (H12 민감도 = 행마다 [H0, H12] 괄호로 읽는 부록).
#:   잡는 길 둘: 이름 꼴 (`*_hertz_h12` · `f_ion_hertz_h12_gap`) 또는 인계표 열 사전 판정에 '부록 전용' (생성기 `TAU_NET_VERDICT_H12`).
#:   주 배포 표에 넣으면 거부 — `--appendix` 로 만든 부록 파일에만 싣는다.  옛 배포 (v1 · v1.1 · v1.2 · Physics 부록) 에는 해당 열이 없다 (selftest ⑬).
APPENDIX_ONLY_RE = re.compile(r'.+_hertz_h12(_gap)?')
APPENDIX_VERDICT_MARK = '부록 전용'


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


def build(handover_csv, columns, out_prefix, appendix=False):
    """columns (순서 그대로) 를 인계표에서 뽑아 `<out_prefix>.csv` · `_columns.tsv` 를 쓴다.
    appendix=False (주 배포) 이면 부록 전용 열 (`appendix_only`) 을 거부한다."""
    if not columns or columns[0] != KEY:
        raise ReleaseError(f'첫 열은 {KEY} 여야 한다 (받은 것: {columns[:1]})')
    if len(set(columns)) != len(columns):
        raise ReleaseError('배포 열 목록에 중복이 있다')
    head, rows = _read_csv(handover_csv)
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
    return len(rows), len(columns)


def check(handover_csv, release_prefix, appendix=False):
    """배포 ⊆ 인계표 — 행 집합 · 순서 · 값 · 열 사전 행이 모두 같아야 한다.  문제 목록을 돌려준다 (빈 목록 = 통과).
    appendix=False (주 배포) 이면 부록 전용 열이 있는 것도 문제로 보고한다."""
    probs = []
    hh, hrows = _read_csv(handover_csv)
    rh, rrows = _read_csv(release_prefix + '.csv')
    if not rh or rh[0] != KEY:
        probs.append(f'배포 첫 열이 {KEY} 가 아니다')
        return probs
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
    return probs


def _selftest():
    ok = []

    def chk(name, cond):
        ok.append(bool(cond))
        print(f"  {'✓' if cond else '✗'} {name}")

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
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    try:
        if a.check:
            if not (a.handover and a.release):
                ap.error('--check 에는 --handover 와 --release 가 필요하다')
            probs = check(a.handover, a.release, appendix=a.appendix)
            for p in probs:
                print('⛔', p)
            print('✓ 배포 ⊆ 인계표 (행 · 순서 · 값 · 열 사전)' if not probs else f'✗ 문제 {len(probs)}')
            return 0 if not probs else 3
        if not (a.handover and a.columns_from and a.out):
            ap.error('만들기에는 --handover · --columns-from · --out 이 필요하다')
        _, rows = _read_tsv(a.columns_from)
        cols = [r[0] for r in rows] + list(a.add)
        n, k = build(a.handover, cols, a.out, appendix=a.appendix)
        probs = check(a.handover, a.out, appendix=a.appendix)
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
