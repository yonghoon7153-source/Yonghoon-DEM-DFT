"""Static scan for Python >=3.9 / numpy >=1.25 / scipy >=1.11 runtime features in the import closure (scripts/)."""
import ast, os, sys, json
SCR = sys.argv[1]
ENTRY = sys.argv[2].split(',')
mods = {f[:-3] for f in os.listdir(SCR) if f.endswith('.py')}

def imports_of(path):
    try:
        tree = ast.parse(open(path, encoding='utf-8').read())
    except SyntaxError:
        return set(), None
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                out.add(a.name.split('.')[0])
        elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            out.add(n.module.split('.')[0])
        elif isinstance(n, ast.Call):   # importlib spec_from_file_location(..., os.path.join(..., 'x.py'))
            for a in ast.walk(n):
                if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value.endswith('.py') and a.value[:-3] in mods:
                    out.add(a.value[:-3])
    return {m for m in out if m in mods}, tree

closure, todo, trees = set(), list(ENTRY), {}
while todo:
    m = todo.pop()
    if m in closure: continue
    closure.add(m)
    deps, tree = imports_of(os.path.join(SCR, m + '.py'))
    trees[m] = tree
    todo.extend(deps - closure)

ATTR39 = {'removeprefix', 'removesuffix', 'bit_count', 'file_digest', 'nextafter', 'ulp', 'lcm', 'cbrt', 'exp2',
          'pairwise', 'randbytes', 'waitstatus_to_exitcode', 'is_relative_to', 'with_stem', 'readlink', 'StrEnum', 'TaskGroup'}
NP_NEW = {'trapezoid', 'isdtype', 'unique_counts', 'unique_values', 'unique_inverse', 'unique_all', 'cumulative_sum',
          'cumulative_prod', 'concat', 'permute_dims', 'matrix_transpose', 'bitwise_count', 'astype', 'exceptions', 'dtypes',
          'long', 'ulong', 'vecdot', 'matrix_norm', 'vector_norm', 'acos', 'asin', 'atan', 'atan2', 'acosh', 'asinh', 'atanh',
          'pow', 'bitwise_left_shift', 'bitwise_right_shift', 'bitwise_invert', 'unstack', 'matvec', 'vecmat'}
SP_NEW = {'diags_array', 'eye_array', 'random_array', 'block_array', 'hstack_array', 'csr_array_new'}
hits = []
def add(m, n, kind, txt):
    hits.append((m, getattr(n, 'lineno', 0), kind, txt))
for m in sorted(closure):
    tree = trees.get(m)
    if tree is None:
        add(m, ast.Module(), 'SYNTAX', 'parse fail'); continue
    fut = any(isinstance(n, ast.ImportFrom) and n.module == '__future__' and any(a.name == 'annotations' for a in n.names)
              for n in tree.body)
    for n in ast.walk(tree):
        if isinstance(n, (ast.BinOp, ast.AugAssign)) and isinstance(n.op, ast.BitOr):
            ops = [n.left, n.right] if isinstance(n, ast.BinOp) else [n.target, n.value]
            def dictish(x):
                return isinstance(x, (ast.Dict, ast.DictComp)) or (isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id in ('dict', 'vars'))
            if any(dictish(o) for o in ops):
                add(m, n, 'DICT_UNION', ast.unparse(n)[:110] if hasattr(ast, 'unparse') else '')
        if isinstance(n, ast.Attribute):
            if n.attr in ATTR39:
                add(m, n, 'ATTR39', n.attr)
            base = n.value
            if isinstance(base, ast.Name) and base.id in ('np', 'numpy') and n.attr in NP_NEW:
                add(m, n, 'NUMPY_NEW', 'np.' + n.attr)
            if isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name) and base.value.id in ('np', 'numpy') \
                    and base.attr == 'linalg' and n.attr in NP_NEW:
                add(m, n, 'NUMPY_NEW', 'np.linalg.' + n.attr)
            if n.attr in SP_NEW:
                add(m, n, 'SCIPY_NEW', n.attr)
            if isinstance(base, ast.Name) and base.id == 'functools' and n.attr == 'cache':
                add(m, n, 'ATTR39', 'functools.cache')
        if isinstance(n, ast.Call):
            f = n.func
            fname = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else '')
            for kw in n.keywords:
                if fname == 'zip' and kw.arg == 'strict':
                    add(m, n, 'ZIP_STRICT', 'zip(strict=)')
                if fname in ('cg', 'bicgstab', 'gmres', 'minres', 'cgs', 'qmr', 'lgmres') and kw.arg == 'rtol':
                    add(m, n, 'SCIPY_RTOL', f'{fname}(rtol=)')
                if fname in ('asarray', 'array') and kw.arg == 'copy':
                    pass
        if isinstance(n, ast.Match if hasattr(ast, 'Match') else ()):
            add(m, n, 'MATCH', 'match')
        if not fut and isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.AnnAssign, ast.arg)):
            anns = []
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                anns = [n.returns]
            elif isinstance(n, ast.AnnAssign):
                anns = [n.annotation]
            elif isinstance(n, ast.arg):
                anns = [n.annotation]
            for a in anns:
                if a is None: continue
                for s in ast.walk(a):
                    if isinstance(s, ast.Subscript) and isinstance(s.value, ast.Name) and s.value.id in ('list', 'dict', 'tuple', 'set', 'frozenset', 'type'):
                        add(m, n, 'ANN_GENERIC', ast.unparse(a)[:80])
                        break
                    if isinstance(s, ast.BinOp) and isinstance(s.op, ast.BitOr):
                        add(m, n, 'ANN_UNION', ast.unparse(a)[:80])
                        break
print('closure', len(closure), ':', ' '.join(sorted(closure)))
for h in hits:
    print('%-28s %5d  %-12s %s' % h)
