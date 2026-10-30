"""D0.7 -T evidence: original deck -> resume deck diff, and the same transformation as the D2 precedent.

Usage: python3 -I compare_transform.py <repo> <d07_extract_dir> <out_dir>
Classifies every diff line of (original -> resume) for D2 (r4, ran to completion 10-29) and D0.7 (r56, -T 10-30)
after replacing each case's own tag/suffix with placeholders; reports the per-class lines side by side.
"""
import difflib, json, re, sys
from pathlib import Path

repo, x, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
pairs = {
    'D2': (repo / 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/input_kg50_d2_b50.liggghts',
           repo / 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/input_kg50_d2_b50_r4.liggghts', 'kg50_d2_b50', 'r4'),
    'D07': (repo / 'docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/input_kg50_d07_b50.liggghts',
            x / 'kg50_d07_b50/input_kg50_d07_b50_r56.liggghts', 'kg50_d07_b50', 'r56'),
}


def norm(line, tag, sfx):
    s = line.replace(tag, 'CASE').replace(tag.upper(), 'CASE')
    s = re.sub(r'_' + sfx + r'\b', '_SFX', s)
    s = re.sub(r'\(' + sfx + r'\)', '(SFX)', s)
    return s


res = {}
for k, (o, r, tag, sfx) in pairs.items():
    a = o.read_text(encoding='utf-8').split('\n')
    b = r.read_text(encoding='utf-8').split('\n')
    ud = list(difflib.unified_diff(a, b, str(o.name), str(r.name), lineterm='', n=0))
    (out / f'diff_{k}.txt').write_text('\n'.join(ud) + '\n', encoding='utf-8')
    minus = [norm(l[1:], tag, sfx) for l in ud if l.startswith('-') and not l.startswith('---')]
    plus = [norm(l[1:], tag, sfx) for l in ud if l.startswith('+') and not l.startswith('+++')]
    a_norm = set(norm(l, tag, sfx) for l in a)
    moved = [p for p in plus if p in a_norm]          # added lines that exist verbatim in the original (template re-declaration)
    new = [p for p in plus if p not in a_norm]
    res[k] = {'diff_lines': len(minus) + len(plus), 'removed': len(minus), 'added': len(plus),
              'added_from_original': len(moved), 'added_new': new, 'removed_lines': minus,
              'orig_sha_lines': len(a), 'resume_lines': len(b)}
# normalized comparison: new lines and removed lines, with the case's seeds/values masked by "same line in its own original"
cmp = {
    'added_new_same': res['D2']['added_new'] == res['D07']['added_new'],
    'removed_same_count': res['D2']['removed'] == res['D07']['removed'],
    'added_from_original_same_count': res['D2']['added_from_original'] == res['D07']['added_from_original'],
}
num = re.compile(r'\d+(\.\d+)?(e[-+]?\d+)?')
cmp['removed_same_after_number_mask'] = [num.sub('N', l) for l in res['D2']['removed_lines']] == [num.sub('N', l) for l in res['D07']['removed_lines']]
res['compare'] = cmp
(out / 'transform_compare.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
for k in ('D2', 'D07'):
    r = res[k]
    print(k, 'diff lines', r['diff_lines'], '(removed', r['removed'], '· added', r['added'], '= from original', r['added_from_original'], '+ new', len(r['added_new']), ')')
print('new lines identical after tag/suffix normalization:', cmp['added_new_same'])
print('removed lines identical after number masking:', cmp['removed_same_after_number_mask'])
if not cmp['added_new_same']:
    for p, q in zip(res['D2']['added_new'], res['D07']['added_new']):
        if p != q: print('  D2 :', p[:110]); print('  D07:', q[:110])
