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
  python3 scripts/lhs_release_build.py --selftest
"""
import argparse
import csv
import io
import os
import sys
import tempfile

KEY = 'case_id'


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


def build(handover_csv, columns, out_prefix):
    """columns (순서 그대로) 를 인계표에서 뽑아 `<out_prefix>.csv` · `_columns.tsv` 를 쓴다."""
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


def check(handover_csv, release_prefix):
    """배포 ⊆ 인계표 — 행 집합 · 순서 · 값 · 열 사전 행이 모두 같아야 한다.  문제 목록을 돌려준다 (빈 목록 = 통과)."""
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
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    try:
        if a.check:
            if not (a.handover and a.release):
                ap.error('--check 에는 --handover 와 --release 가 필요하다')
            probs = check(a.handover, a.release)
            for p in probs:
                print('⛔', p)
            print('✓ 배포 ⊆ 인계표 (행 · 순서 · 값 · 열 사전)' if not probs else f'✗ 문제 {len(probs)}')
            return 0 if not probs else 3
        if not (a.handover and a.columns_from and a.out):
            ap.error('만들기에는 --handover · --columns-from · --out 이 필요하다')
        _, rows = _read_tsv(a.columns_from)
        cols = [r[0] for r in rows] + list(a.add)
        n, k = build(a.handover, cols, a.out)
        probs = check(a.handover, a.out)
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
