"""Patch the scratch carbon_junction.py copy with the new top-level items (by name, via ast spans)."""
import ast
import sys

D = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/'
TARGET = sys.argv[1] if len(sys.argv) > 1 else D + 'impl/carbon_junction.py'
SRC = sys.argv[2] if len(sys.argv) > 2 else None
PARTS = [D + 'new_cj_parts.py', D + 'new_cj_parts2.py', D + 'new_cj_parts3.py', D + 'new_cj_parts4.py']


def spans(text):
    """top-level name → (start line idx 0-based incl. decorators/leading comment block, end idx exclusive)."""
    tree = ast.parse(text)
    out = {}
    for node in tree.body:
        name = None
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
            start = min([d.lineno for d in node.decorator_list] + [node.lineno]) - 1
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
            start = node.lineno - 1
        else:
            continue
        out[name] = (start, node.end_lineno)
    return out


def parts_src():
    got = {}
    for p in PARTS:
        t = open(p, encoding='utf-8').read()
        lines = t.split('\n')
        for name, (a, b) in spans(t).items():
            got[name] = '\n'.join(lines[a:b])
    return got


new = parts_src()
text = open(SRC or TARGET, encoding='utf-8').read()
lines = text.split('\n')
sp = spans(text)

# plan: old name → list of new names (replacement group) ; None = delete ; insertions after anchor
REPLACE = {
    'CJUNC_MODEL_VERSION': ['CJUNC_MODEL_VERSION'],
    'CJUNC_SELF_LC_RULE': ['CJUNC_SELF_LC_RULE'],
    'CJUNC_SELF_S_RULE': ['CJUNC_SELF_S_RULE'],
    'CJUNC_PORT_RULE': ['CJUNC_PORT_RULE'],
    'CJUNC_SELF_RULE': ['CJUNC_SELF_RULE', 'CJUNC_PIECE_RULE', 'CJUNC_SV_CF_KIND', 'CJUNC_SV_CF_RULE'],
    'CJUNC_QUALIFIERS': ['CJUNC_QUALIFIERS'],
    '_self_is_junction': None,          # keep (handled by INSERT_AFTER)
    '_segments_of': ['_closed_path', '_segments_of'],
    '_positions': ['_positions'],
    'cjunc_registry': ['cjunc_registry'],
    '_distinct_instances': ['_distinct_instances'],
    '_self_instances': ['_continuity', '_pos_arc_ranges', '_arc_gap', '_pos_pair_sd', '_self_pairs', '_pair_groups',
                        '_group_cp', '_touch_len_pairs', '_self_instances'],
    '_touch_len_sets': [],
    '_self_geometry': [],
    '_merge_instances': ['_merge_instances'],
    '_port_why': [],
    '_piece_cand': ['_piece_cand', '_side_cand', '_port_take'],
    '_ports': ['_ports'],
    '_touch_runs': ['_touch_runs', '_touch_runs_on'],
    '_divide_runs': ['_divide_runs', '_divide_runs_idx'],
    '_n_sub': ['_n_sub'],
    '_subedges': ['_subedges'],
    '_census': ['_census'],
    '_sdcp_bridging': ['@keep', '_sv_split'],
    'cjunc_plan': ['cjunc_plan'],
    'cjunc_require_quantitative': ['cjunc_require_quantitative'],
    'CjuncAssembler': ['CjuncAssembler'],
}
INSERT_AFTER = {'_self_is_junction': ['_self_floor', '_distinct_keep', '_ring_alias', '_sv_cut_rows']}

used = set()
edits = []   # (start, end, replacement text)
for old, group in REPLACE.items():
    if group is None:
        continue
    if old not in sp:
        raise SystemExit(f'target has no {old}')
    a, b = sp[old]
    chunks = []
    for nm in group:
        if nm == '@keep':
            chunks.append('\n'.join(lines[a:b]))
            continue
        if nm not in new:
            raise SystemExit(f'parts have no {nm}')
        chunks.append(new[nm])
        used.add(nm)
    is_assign = old.isupper() or old.startswith('CJUNC')
    sep = '\n' if is_assign else '\n\n\n'
    edits.append((a, b, sep.join(chunks)))
for old, group in INSERT_AFTER.items():
    a, b = sp[old]
    chunks = ['\n'.join(lines[a:b])] + [new[nm] for nm in group]
    used.update(group)
    edits.append((a, b, '\n\n\n'.join(chunks)))
missing = sorted(set(new) - used)
if missing:
    raise SystemExit(f'unused parts: {missing}')
edits.sort()
for x in range(len(edits) - 1):
    if edits[x][1] > edits[x + 1][0]:
        raise SystemExit(f'overlap {edits[x][:2]} {edits[x + 1][:2]}')
out = []
cur = 0
for a, b, rep in edits:
    out.extend(lines[cur:a])
    out.append(rep)
    cur = b
out.extend(lines[cur:])
res = '\n'.join(out)
# collapse >2 blank lines between top-level defs (deleted functions leave gaps)
import re
res = re.sub(r'\n{4,}(?=(def |class |# ═))', '\n\n\n', res)
open(TARGET, 'w', encoding='utf-8').write(res)
ast.parse(res)
print('patched', TARGET, len(res.split(chr(10))), 'lines')
