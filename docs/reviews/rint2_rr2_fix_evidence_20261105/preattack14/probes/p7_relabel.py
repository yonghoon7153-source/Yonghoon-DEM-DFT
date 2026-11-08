"""Copy/new boundary relabeling of an honest RESUME_MISMATCH (mm · source attempt_1 present on the same base) — summary-only edits.
   R1: mark the mismatching rerun L02 as a copy (copied_from 1 · copied += L02) and point rerun at the pre-launch stop L03 → run == rerun branch (no re-compare).
   R2: unmark copy L01 (drop copied_from · copied []) and point rerun at L01 → re-compare runs against attempt_1/L01 (identical copy)."""
import copy, json, hashlib
from pathlib import Path
from lib import RR, T, row

sc = T.scen('PA13', T.pa13_scen)
mm = sc['mm']['b']['sum']
L01 = 'L01_floor'
L02 = mm['resume']['rerun']


def r1(s):
    s = copy.deepcopy(s)
    s['stop'].update(code='TIME_LIMIT', run='L03_point')
    [r for r in s['runs'] if r['name'] == L02][0]['copied_from'] = 1
    s['resume'].update(copied=[L01, L02], rerun='L03_point', compared=[], determinism=None)
    return s


f = T.pa13_folder(sc['mm'], 'p7_R1')
print('R1 (7 summary edits · src keep):', row(f, r1(mm)))

f2 = T.pa13_folder(sc['mm'], 'p7_R2')
left = RR.resume_leftovers(f2.parent / 'attempt_1' / [r for r in mm['runs'] if r['name'] == L01][0]['outdir'])
print('attempt_1/L01 leftovers:', [nm for nm, _ in left])


def r2(s):
    s = copy.deepcopy(s)
    s['stop'].update(code='TIME_LIMIT', run='L03_point')
    [r for r in s['runs'] if r['name'] == L01][0].pop('copied_from')
    od = [r for r in s['runs'] if r['name'] == L01][0]['outdir']
    s['resume'].update(copied=[], rerun=L01, compared=[{'file': nm, 'same': (f2 / od / nm).read_bytes() == raw} for nm, raw in left],
                       determinism='compared' if left else 'assumed')
    return s


print('R2 (6 summary edits · src keep):', row(f2, r2(mm)))
# disk evidence that would bind copy vs new: group launch token of L02 in attempt_2 vs attempt_1 (copy = same bytes · fresh run = new token)
for nm in (L01, L02):
    a2 = f / 'groups' / f'{nm}.launch.json'
    a1 = f.parent / 'attempt_1' / 'groups' / f'{nm}.launch.json'
    h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()[:12] if p.exists() else None   # noqa: E731
    print(f'  groups/{nm}.launch.json  attempt_2 {h(a2)}  attempt_1 {h(a1)}  (copy ⇒ equal · fresh run ⇒ different)')
