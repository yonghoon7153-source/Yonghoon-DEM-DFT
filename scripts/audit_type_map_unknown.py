#!/usr/bin/env python3
"""저장된 케이스 전수에서 **상(phase) 라벨이 안 붙은 원자·접촉**을 찾는다.

★ 존재 이유 (2026-09-22, webapp 패치 §8 세 번째 항목)
    `type_map_resolve` 는 **앞으로** 들어오는 덱을 fail-closed 로 막는다.  그러나
    이미 **`?` 로 계산돼 저장된 옛 케이스**가 더 있는지는 전수 확인되지 않았다.
    실사고(케이스 `260922_092001_0853b1`)에서 SE(type 3)가 원자의 **99.75 %**였는데
    아무 상에도 안 붙어 `?` 가 됐고, 파이프라인은 멈추지 않고 porosity·CN·파괴지수를
    **그럴듯하게** 다 뽑았다.  ⇒ 같은 일이 일어난 옛 케이스의 저장된 수치는 **무효**다.

★ 왜 `?` 만 훑으면 안 되나 — **같은 실패가 파일마다 다른 표식으로 남는다** (실측):

    analyze_contacts.py:800  df_atom['type_name'] = df_atom['type'].map(type_map)
                             → 맵에 없으면 **NaN** (CSV 에는 **빈 칸**)
    analyze_contacts.py:804  id_to_type = {...: type_map.get(a['type'], '?') ...}
                             → 맵에 없으면 **'?'**

    `contacts_analyzed.csv` 만 `?` 로 훑는 스윕은 `atoms_analyzed.csv` 쪽 누락을
    통째로 못 본다.  ⇒ 이 도구는 **두 표식을 모두** 본다.
    (③ CLI 기본값 `-t 1:AM,2:SE` 는 2상이라, 3상 덱을 `-t` 없이 돌리면 type 3 이 전부 `?`.)

★ 규율 ⑤ — "후보를 고르는 코드가 곧 사각지대다"
    이 도구는 이름 조각으로 케이스를 **고르지 않는다**.  준 뿌리 밑의 디렉터리를 전수로
    걷고, **본 것과 못 본 것을 같이 보고**한다.  케이스가 0건이면 **초록이 아니라 거부**다
    (rc=2) — 빈 스윕이 조용히 통과하는 것이 이 리포가 반복해 당한 false-green 이다.

종료 코드
    0  깨끗함 (케이스 ≥ 1건, 미상 라벨 0)
    1  미상 라벨이 있는 케이스 발견  ← 저장된 수치를 믿으면 안 되는 케이스
    2  거부 — 케이스 0건 · 헤더 없음 · 사용법 오류 (fail-closed)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import tempfile

# `?` 외에도 "라벨이 안 붙었다" 를 뜻하는 표식 전부.  빈 문자열이 여기 있는 이유는
# pandas 가 NaN 을 CSV 에 **빈 칸**으로 쓰기 때문이다 (위 docstring 참조).
UNKNOWN_TOKENS = frozenset({'?', '', 'nan', 'NaN', 'None', 'none'})

CONTACT_CSV = 'contacts_analyzed.csv'
ATOM_CSV = 'atoms_analyzed.csv'

# 이 열들이 헤더에 없으면 "미상 0건" 이 아니라 **거부**다 (조용히 통과하지 않는다).
CONTACT_COLS = ('type1', 'type2')
ATOM_COLS = ('type', 'type_name')


def _is_unknown(v) -> bool:
    return (v if isinstance(v, str) else '').strip() in UNKNOWN_TOKENS


def scan_contacts(path):
    """-> (n_rows, n_unknown, {라벨: 개수}, error|None)"""
    counts = {}
    n_rows = n_bad = 0
    with open(path, newline='', encoding='utf-8', errors='replace') as fh:
        rd = csv.DictReader(fh)
        if rd.fieldnames is None:
            return 0, 0, {}, 'CSV 에 헤더가 없다'
        missing = [c for c in CONTACT_COLS if c not in rd.fieldnames]
        if missing:
            return 0, 0, {}, '열 없음: %s' % ','.join(missing)
        for row in rd:
            n_rows += 1
            t1, t2 = row.get('type1'), row.get('type2')
            if _is_unknown(t1) or _is_unknown(t2):
                n_bad += 1
                key = '-'.join(sorted([(t1 or '').strip() or '<빈칸>',
                                       (t2 or '').strip() or '<빈칸>']))
                counts[key] = counts.get(key, 0) + 1
    return n_rows, n_bad, counts, None


def scan_atoms(path):
    """-> (n_rows, n_unknown, {미상 type: 개수}, error|None)"""
    counts = {}
    n_rows = n_bad = 0
    with open(path, newline='', encoding='utf-8', errors='replace') as fh:
        rd = csv.DictReader(fh)
        if rd.fieldnames is None:
            return 0, 0, {}, 'CSV 에 헤더가 없다'
        missing = [c for c in ATOM_COLS if c not in rd.fieldnames]
        if missing:
            return 0, 0, {}, '열 없음: %s' % ','.join(missing)
        for row in rd:
            n_rows += 1
            if _is_unknown(row.get('type_name')):
                n_bad += 1
                k = (row.get('type') or '').strip() or '<빈칸>'
                counts[k] = counts.get(k, 0) + 1
    return n_rows, n_bad, counts, None


def find_case_dirs(roots):
    """뿌리들 밑의 **모든** 디렉터리를 걷고 두 CSV 중 하나라도 가진 곳을 케이스로 본다.

    ⚠ 이름으로 거르지 않는다 (규율 ⑤).  대신 '봤지만 CSV 가 없던' 디렉터리 수를
    같이 돌려주어, 스윕이 실제로 무엇을 덮었는지 말할 수 있게 한다.
    """
    cases, seen_dirs, missing_root = [], 0, []
    for root in roots:
        if not os.path.isdir(root):
            missing_root.append(root)
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            seen_dirs += 1
            fs = set(filenames)
            has_c, has_a = CONTACT_CSV in fs, ATOM_CSV in fs
            if has_c or has_a:
                cases.append((dirpath, has_c, has_a))
    cases.sort()
    return cases, seen_dirs, missing_root


def audit(roots):
    cases, seen_dirs, missing_root = find_case_dirs(roots)
    out = {
        'roots': list(roots),
        'roots_missing': missing_root,
        'dirs_walked': seen_dirs,
        'cases_found': len(cases),
        'cases_both_csv': 0,
        'cases_partial_csv': [],
        'read_errors': [],
        'dirty': [],
        'clean': [],
    }
    for dirpath, has_c, has_a in cases:
        if has_c and has_a:
            out['cases_both_csv'] += 1
        else:
            out['cases_partial_csv'].append(
                {'case': dirpath, 'has_contacts': has_c, 'has_atoms': has_a})
        rec = {'case': dirpath,
               'contacts': {'rows': 0, 'unknown': 0, 'labels': {}},
               'atoms': {'rows': 0, 'unknown': 0, 'types': {}}}
        if has_c:
            n, bad, lab, err = scan_contacts(os.path.join(dirpath, CONTACT_CSV))
            if err:
                out['read_errors'].append({'file': os.path.join(dirpath, CONTACT_CSV),
                                           'error': err})
            rec['contacts'] = {'rows': n, 'unknown': bad, 'labels': lab}
        if has_a:
            n, bad, ty, err = scan_atoms(os.path.join(dirpath, ATOM_CSV))
            if err:
                out['read_errors'].append({'file': os.path.join(dirpath, ATOM_CSV),
                                           'error': err})
            rec['atoms'] = {'rows': n, 'unknown': bad, 'types': ty}
        tot = rec['contacts']['unknown'] + rec['atoms']['unknown']
        (out['dirty'] if tot else out['clean']).append(rec)
    return out


def verdict(res):
    """-> (rc, 한 줄 사유).  ⚠ 케이스 0건과 읽기 실패는 **초록이 아니다**."""
    if res['cases_found'] == 0:
        return 2, '케이스 0건 — 뿌리가 틀렸거나 코퍼스가 여기 없다 (fail-closed)'
    if res['read_errors']:
        return 2, '읽기/헤더 오류 %d 건 — 판정 불가' % len(res['read_errors'])
    if res['dirty']:
        return 1, '미상 라벨 케이스 %d / %d' % (len(res['dirty']), res['cases_found'])
    return 0, '%d 케이스 전부 깨끗' % res['cases_found']


def _pct(a, b):
    return (100.0 * a / b) if b else 0.0


def report(res, max_show=40):
    print('뿌리        : %s' % ', '.join(res['roots']))
    if res['roots_missing']:
        print('  ⚠ 없는 뿌리: %s' % ', '.join(res['roots_missing']))
    print('걸은 디렉터리: %d' % res['dirs_walked'])
    print('케이스      : %d  (두 CSV 다 있음 %d · 한쪽만 %d)'
          % (res['cases_found'], res['cases_both_csv'], len(res['cases_partial_csv'])))
    for p in res['cases_partial_csv'][:max_show]:
        print('  ⚠ 한쪽만: %s  (contacts=%s atoms=%s)'
              % (p['case'], p['has_contacts'], p['has_atoms']))
    for e in res['read_errors'][:max_show]:
        print('  ⛔ 읽기 오류: %s — %s' % (e['file'], e['error']))
    print('')
    rc_pre, why_pre = verdict(res)
    if rc_pre == 2:
        # ⚠ 판정 불가일 때 ✅ 를 찍지 않는다.  케이스 0건에 "미상 라벨 없음" 을 먼저
        #   내보내면 이 도구가 막으려는 false-green 을 도구 자신이 화면에 내게 된다
        #   (초판이 실제로 그랬다).
        print('⛔ 판정 불가 — %s' % why_pre)
    elif not res['dirty']:
        print('✅ 미상 라벨 없음 (%d 케이스)' % len(res['clean']))
    else:
        print('⛔ 미상 라벨 케이스 %d 건 — 저장된 수치를 믿으면 안 된다:'
              % len(res['dirty']))
        for r in res['dirty'][:max_show]:
            c, a = r['contacts'], r['atoms']
            print('  %s' % r['case'])
            if c['unknown']:
                print('     contacts %d/%d (%.2f %%)  %s'
                      % (c['unknown'], c['rows'], _pct(c['unknown'], c['rows']),
                         dict(sorted(c['labels'].items(), key=lambda kv: -kv[1])[:5])))
            if a['unknown']:
                print('     atoms    %d/%d (%.2f %%)  미상 type: %s'
                      % (a['unknown'], a['rows'], _pct(a['unknown'], a['rows']),
                         dict(sorted(a['types'].items(), key=lambda kv: -kv[1])[:5])))
        if len(res['dirty']) > max_show:
            print('  … 그리고 %d 건 더' % (len(res['dirty']) - max_show))
    rc, why = verdict(res)
    print('')
    print('판정: rc=%d — %s' % (rc, why))
    return rc


# ---------------------------------------------------------------- selftest
def _w(path, header, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def _selftest():
    ok = True

    def chk(name, cond, detail=''):
        nonlocal ok
        print('%s: %s  %s' % (name, detail, 'OK' if cond else '**FAIL**'))
        if not cond:
            ok = False

    with tempfile.TemporaryDirectory() as td:
        # ── 깨끗한 케이스
        good = os.path.join(td, 'corpus', 'case_good')
        _w(os.path.join(good, CONTACT_CSV), ['id1', 'id2', 'type1', 'type2', 'contact_type'],
           [[1, 2, 'AM_P', 'SE', 'AM_P-SE'], [2, 3, 'SE', 'SE', 'SE-SE']])
        _w(os.path.join(good, ATOM_CSV), ['id', 'type', 'type_name'],
           [[1, 1, 'AM_P'], [2, 3, 'SE'], [3, 3, 'SE']])

        # ── 실사고 재현: type 3 (SE) 가 맵에 없어 `?` — 접촉의 대부분이 오염
        bad_c = os.path.join(td, 'corpus', 'case_qmark')
        rows = [[1, 2, 'AM_P', '?', 'AM_P-?']] * 399 + [[3, 4, 'AM_P', 'AM_P', 'AM_P-AM_P']]
        _w(os.path.join(bad_c, CONTACT_CSV), ['id1', 'id2', 'type1', 'type2', 'contact_type'], rows)
        _w(os.path.join(bad_c, ATOM_CSV), ['id', 'type', 'type_name'],
           [[1, 1, 'AM_P'], [2, 3, '']])

        # ── 원자 쪽에만 빈 칸 (접촉은 멀쩡) — `?` 스윕이 놓치는 부류
        bad_a = os.path.join(td, 'corpus', 'case_blank_only')
        _w(os.path.join(bad_a, CONTACT_CSV), ['id1', 'id2', 'type1', 'type2', 'contact_type'],
           [[1, 2, 'AM_P', 'SE', 'AM_P-SE']])
        _w(os.path.join(bad_a, ATOM_CSV), ['id', 'type', 'type_name'],
           [[1, 1, 'AM_P'], [2, 2, ''], [3, 2, '']])

        # ── 한쪽 CSV 만 있는 케이스
        part = os.path.join(td, 'corpus', 'case_partial')
        _w(os.path.join(part, ATOM_CSV), ['id', 'type', 'type_name'], [[1, 1, 'AM_P']])

        # ── 케이스가 아닌 잡동사니 디렉터리 (이름으로 거르지 않는다는 것의 대조)
        os.makedirs(os.path.join(td, 'corpus', 'reports', 'figures'), exist_ok=True)

        res = audit([os.path.join(td, 'corpus')])
        rc, why = verdict(res)
        names = {os.path.basename(r['case']) for r in res['dirty']}

        chk('① 전수 수집', res['cases_found'] == 4,
            '케이스 4건 수집 (이름으로 거르지 않는다) — 실제 %d' % res['cases_found'])
        _q = next((r for r in res['dirty']
                   if os.path.basename(r['case']) == 'case_qmark'), None)
        chk('② 실사고 재현', _q is not None and _q['contacts']['unknown'] == 399,
            "`?` 접촉 399/400 을 잡는다 — 실제 %s"
            % (_q['contacts']['unknown'] if _q else '케이스를 못 찾음'))
        chk('③ 다른 표식', 'case_blank_only' in names,
            'atoms 의 **빈 칸**만 있어도 잡는다 — `?` 만 훑으면 놓치는 부류')
        chk('④ 판별력 (음성 대조)', 'case_good' not in names and 'case_partial' not in names,
            '멀쩡한 케이스는 통과한다 — 무조건 거부하는 검사가 아니다')
        chk('⑤ 부분 커버리지 보고', len(res['cases_partial_csv']) == 1,
            '한쪽 CSV 만 있는 케이스를 **초록으로 숨기지 않는다**')
        chk('⑥ 오염 판정', rc == 1, 'rc=1 — %s' % why)

        # ── 케이스 0건이면 거부 (fail-closed)
        res0 = audit([os.path.join(td, 'empty_root')])
        rc0, why0 = verdict(res0)
        chk('⑦ 빈 스윕 거부', rc0 == 2,
            '케이스 0건은 **초록이 아니다** (rc=%d) — 이 리포가 반복해 당한 false-green' % rc0)

        # ── 깨끗한 코퍼스만 주면 통과 (⑦ 과 짝이 되어 판별력을 세운다)
        res1 = audit([good])
        rc1, _ = verdict(res1)
        chk('⑧ 양성 대조', rc1 == 0, '깨끗한 코퍼스는 rc=0')

        # ── 열이 없으면 "미상 0건" 이 아니라 거부
        noh = os.path.join(td, 'nohdr', 'case_x')
        _w(os.path.join(noh, CONTACT_CSV), ['id1', 'id2'], [[1, 2]])
        res2 = audit([os.path.join(td, 'nohdr')])
        rc2, why2 = verdict(res2)
        chk('⑨ 헤더 없음 거부', rc2 == 2,
            'type1/type2 가 없으면 조용히 0건으로 넘어가지 않는다 — %s' % why2)

    print('SELFTEST PASS' if ok else 'SELFTEST FAIL')
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='저장된 케이스에서 상 라벨이 안 붙은 원자/접촉을 전수로 찾는다',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='rc: 0 깨끗 · 1 오염 케이스 있음 · 2 거부(케이스 0건/헤더 없음)')
    ap.add_argument('roots', nargs='*', default=None,
                    help='훑을 뿌리 (기본: webapp/results webapp/archive webapp/uploads)')
    ap.add_argument('--json', dest='json_out', metavar='PATH',
                    help='결과를 JSON 으로 저장')
    ap.add_argument('--max-show', type=int, default=40, help='화면에 보일 최대 건수')
    ap.add_argument('--selftest', action='store_true', help='자기검사')
    args = ap.parse_args(argv)

    if args.selftest:
        return _selftest()

    roots = args.roots or ['webapp/results', 'webapp/archive', 'webapp/uploads']
    res = audit(roots)
    rc = report(res, args.max_show)
    if args.json_out:
        with open(args.json_out, 'w', encoding='utf-8') as fh:
            json.dump(res, fh, indent=1, ensure_ascii=False)
        print('JSON: %s' % args.json_out)
    return rc


if __name__ == '__main__':
    sys.exit(main())
