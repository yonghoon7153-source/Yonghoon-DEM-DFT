"""Reproduce a fixed-source AST inventory; never import or run the solver."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import subprocess


PIN = 'c438673b8dac3ce0a54dfcb0de00562a98e1ddf3'
SOURCE = 'scripts/mpm3d_compaction.py'
SOURCE_SHA256 = 'b8bb85278b09e4232c933a868d332eb544b981b75e7367c82ce98b54cce17bdd'
BLOB = 'fb1bf65535135ecdb7acb87833b7acdb389e54db'
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def git(*args):
    return subprocess.check_output([
        'git', '-c', 'core.longpaths=true',
        '-c', 'safe.directory=' + REPO.as_posix(), '-C', str(REPO), *args,
    ])


def root_name(node):
    while isinstance(node, (ast.Subscript, ast.Attribute)):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


def inventory():
    raw = git('show', PIN + ':' + SOURCE)
    if len(raw) != 335832 or hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('Fixed source identity mismatch')
    if git('rev-parse', PIN + ':' + SOURCE).decode().strip() != BLOB:
        raise ValueError('Fixed Git blob mismatch')
    tree = ast.parse(raw.decode('utf-8'))
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    fields = []
    for stmt in ast.walk(main):
        if not isinstance(stmt, ast.Assign) or not isinstance(stmt.value, ast.Call):
            continue
        call = stmt.value
        fn = ast.unparse(call.func)
        if fn not in ['ti.field', 'ti.Vector.field', 'ti.Matrix.field']:
            continue
        if len(stmt.targets) != 1 or not isinstance(stmt.targets[0], ast.Name):
            raise ValueError('Uncovered field declaration')
        offset = {'ti.field': 0, 'ti.Vector.field': 1, 'ti.Matrix.field': 2}[fn]
        components = 1
        for arg in call.args[:offset]:
            if not isinstance(arg, ast.Constant) or type(arg.value) is not int:
                raise ValueError('Uncovered component declaration')
            components *= arg.value
        dtype = ast.unparse(call.args[offset])
        if dtype not in ['ti.f32', 'ti.i32']:
            raise ValueError('Uncovered dtype')
        fields.append(dict(
            name=stmt.targets[0].id, line=stmt.lineno, constructor=fn,
            dtype=dtype, components=components, scalar_bytes=4,
            shape=ast.unparse(call.args[offset + 1]), bytes_per_element=4 * components,
        ))
    fields.sort(key=lambda f: f['line'])
    if len(fields) != 33:
        raise ValueError('Unexpected field count')
    names = {f['name'] for f in fields}
    functions = {}
    for fn in main.body:
        if not isinstance(fn, ast.FunctionDef) or fn.name not in ['load', 'substep', 'rod_pass', 'rod_setv']:
            continue
        writes = {}
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign):
                targets = node.targets
            elif isinstance(node, ast.AugAssign):
                targets = [node.target]
            else:
                continue
            for target in targets:
                name = root_name(target)
                if name in names:
                    writes.setdefault(name, []).append(node.lineno)
        functions[fn.name] = dict(
            start=fn.lineno, end=fn.end_lineno,
            writes={k: sorted(set(v)) for k, v in sorted(writes.items())},
        )
    methods = []
    for node in ast.walk(main):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in names
                and node.func.attr in ['fill', 'from_numpy', 'to_numpy']):
            methods.append(dict(field=node.func.value.id, method=node.func.attr, line=node.lineno))
    coefficients = dict(n=0, grid_nodes=0, mask_nodes=0, nz=0, rod_slots=0, scalar=0)
    shapes = {'n': 'n', '(n_grid, n_grid, nz)': 'grid_nodes', 'nz': 'nz',
              '_rn': 'rod_slots', '()': 'scalar',
              '(n_grid, n_grid, nz) if scaffold_on else (1, 1, 1)': 'mask_nodes'}
    for field in fields:
        bucket = shapes[field['shape']]
        coefficients[bucket] += field['bytes_per_element']
        field['cardinality_symbol'] = bucket
    if coefficients != dict(n=124, grid_nodes=16, mask_nodes=8, nz=16, rod_slots=56, scalar=24):
        raise ValueError('Unexpected payload coefficients')
    sub = next(n for n in main.body if isinstance(n, ast.FunctionDef) and n.name == 'substep')
    return dict(
        source_pin=PIN, path=SOURCE, source_sha256=SOURCE_SHA256,
        git_blob=BLOB, source_bytes=len(raw), inspection='AST only; no module import or execution',
        fields=fields, kernel_assignment_sites=functions,
        array_method_sites=sorted(methods, key=lambda x: x['line']),
        declared_scalar_payload_coefficients=coefficients,
        substep_mentions_se_id_base=any(isinstance(n, ast.Name) and n.id == 'se_id_base'
                                        for n in ast.walk(sub)),
        actual_memory_measured=False, production_changed=False, overall='HOLD',
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Compare with the saved inventory')
    args = parser.parse_args()
    record = inventory()
    data = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if args.check:
        if data != (HERE / 'source_state_inventory.json').read_bytes():
            raise SystemExit('Inventory mismatch')
        print('MATCH: 33 declarations; AST inventory only; solver not imported or executed')
    else:
        print(data.decode('utf-8'), end='')
