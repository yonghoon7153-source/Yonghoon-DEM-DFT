"""Our own scope check for verdict §2 (no Codex probe): sealed 32 / handover 2 /
registration docs / fixture constants / FULL policy / code_fp.

usage: python3 -I scope_ours.py <repo_root> <repro_dir>
reads NUL ls-tree dumps <repro_dir>/lstree_{685c2bbdb,34713ac96,HEAD}.z and the
baseline extraction <repro_dir>/base_685c2bbdb/scripts/test_l214r_r01_restored_full.py
"""
import ast
import hashlib
import json
import re
import sys
from pathlib import Path


def load(p):
    rows = {}
    for rec in Path(p).read_bytes().split(b'\0'):
        if not rec:
            continue
        meta, path = rec.split(b'\t', 1)
        mode, typ, sha, size = meta.decode().split()
        rows[path.decode('utf-8')] = sha
    return rows


def assigned(src, names):
    tree = ast.parse(src)
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in names:
                    try:
                        out[t.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        out[t.id] = ast.get_source_segment(src, node.value)
    return out


def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def main():
    repo, repro = Path(sys.argv[1]), Path(sys.argv[2])
    trees = {k: load(repro / f'lstree_{k}.z') for k in ('685c2bbdb', '34713ac96', 'HEAD')}
    runner = (repo / 'scripts/run_network_194_parallel.py').read_text(encoding='utf-8')
    decl = assigned(runner, {'CODE_FILES', 'HANDOVER_FILES'})
    res = {}
    for name in ('CODE_FILES', 'HANDOVER_FILES'):
        paths = list(decl[name])
        res[name] = dict(
            n=len(paths),
            same_685_vs_347=sum(trees['685c2bbdb'].get(p) == trees['34713ac96'].get(p) for p in paths),
            same_347_vs_HEAD=sum(trees['34713ac96'].get(p) == trees['HEAD'].get(p) for p in paths),
            worktree_blob_eq_HEAD=sum(blob((repo / p).read_bytes()) == trees['HEAD'].get(p) for p in paths))
    # code_fp exactly as the Codex scope probe re-derived it (sorted (path, sha256) JSON, compact)
    hashes = {p: hashlib.sha256((repo / p).read_bytes()).hexdigest() for p in decl['CODE_FILES']}
    res['code_fp_rederived'] = hashlib.sha256(json.dumps(sorted(hashes.items()), separators=(',', ':')).encode('utf8')).hexdigest()
    regs = ('docs/reviews/lhs_network_batch_registration_20261007_g2.md',
            'docs/reviews/lhs_network_batch_registration_20261012_supp20.md')
    res['registration_docs_same_685_347_HEAD'] = {p: trees['685c2bbdb'].get(p) == trees['34713ac96'].get(p) == trees['HEAD'].get(p) for p in regs}
    supp = (repo / regs[1]).read_text(encoding='utf-8')
    res['supp20_reg_code_fp_tokens'] = sorted(set(re.findall(r'`code_fp(?:_pending)? ([0-9a-f]{64})`', supp)))
    tools = ('scripts/lhs_release_build.py', 'scripts/network_conductivity.py', 'scripts/tau_flux.py',
             'scripts/run_network_194_parallel.py')
    res['tools_same_685_347_HEAD'] = {p: trees['685c2bbdb'].get(p) == trees['34713ac96'].get(p) == trees['HEAD'].get(p) for p in tools}
    names = {'E_AREA', 'E_BX', 'E_BY'}
    now = assigned((repo / 'scripts/test_l214r_r01_restored_full.py').read_text(encoding='utf-8'), names)
    old = assigned((repro / 'base_685c2bbdb/scripts/test_l214r_r01_restored_full.py').read_text(encoding='utf-8'), names)
    res['fixture_now'] = now
    res['fixture_same'] = now == old
    nc = (repo / 'scripts/network_conductivity.py').read_text(encoding='utf-8')
    tf = (repo / 'scripts/tau_flux.py').read_text(encoding='utf-8')
    res['FULL_Q_GUARD_MAX'] = assigned(nc, {'FULL_Q_GUARD_MAX'}).get('FULL_Q_GUARD_MAX')
    res['producer_strict_lines'] = [(i + 1, l.strip()) for i, l in enumerate(nc.splitlines()) if 'reject = sigma_ratio > FULL_Q_GUARD_MAX' in l]
    res['consumer_strict_lines'] = [(i + 1, l.strip()) for i, l in enumerate(tf.splitlines()) if "q_rec > nc.FULL_Q_GUARD_MAX" in l]
    print(json.dumps(res, ensure_ascii=False, indent=1))
    (repro / 'scope_ours.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
