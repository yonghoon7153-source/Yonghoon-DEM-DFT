"""Codex RGL re-verify probes (10-05 zip, unpacked at scratchpad/codex_rglr) re-run against a given tree.

usage: python3 rglr_after.py <tree_root> <out_dir> [new_network] [independent_lw] [original_g4] [raw18] [handover]
  out_dir = copy of codex_rglr minus source/diffs/inputs/evidence outputs · source/ = manifest paths (+ all scripts/*.py,
  webapp/*.py|json) taken from tree_root.  Every `assert` in probes/network_adversarial.py · probes/lw_replay.py becomes a
  recorded check (they encode the DEFECT outcomes, e.g. band_ratio_nan == done) → probes/<name>.soft_asserts.json.
  Results: out_dir/evidence/network_adversarial.json · lw_replay.json (same schema as Codex's).
"""
import ast, json, os, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ZIP = Path(os.environ.get('CODEX_RGLR_PKG', str(HERE / 'codex_rglr')))  # Codex 10-05 재검증 zip 을 푼 폴더
SOFTEN = ['probes/network_adversarial.py', 'probes/lw_replay.py']
PRELUDE = '''
import atexit as __atexit, json as __json
from pathlib import Path as __P
__SOFT = []
__SOFT_PATH = __P(__file__).with_suffix('.soft_asserts.json')
def __sa(fn, line, src):
    try:
        ok = bool(fn()); __SOFT.append(dict(line=line, src=src, held=ok, error=None))
    except Exception as e:
        __SOFT.append(dict(line=line, src=src, held=None, error=f"{type(e).__name__}: {e}"[:300]))
def __dump():
    __SOFT_PATH.write_text(__json.dumps(__SOFT, indent=1, ensure_ascii=False), encoding='utf-8')
__atexit.register(__dump)
'''


class Soft(ast.NodeTransformer):
    def __init__(self, text):
        self.text = text

    def visit_Assert(self, node):
        src = ast.get_source_segment(self.text, node.test) or ''
        lam = ast.Lambda(args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
                         body=node.test)
        call = ast.Call(func=ast.Name('__sa', ast.Load()), args=[lam, ast.Constant(node.lineno), ast.Constant(src[:200])],
                        keywords=[])
        return ast.copy_location(ast.Expr(call), node)


def soften(path):
    text = path.read_text(encoding='utf-8')
    tree = Soft(text).visit(ast.parse(text))
    body = tree.body
    i = 1 if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], 'value', None), ast.Constant) else 0
    while i < len(body) and isinstance(body[i], ast.ImportFrom) and body[i].module == '__future__':
        i += 1
    tree.body = body[:i] + ast.parse(PRELUDE).body + body[i:]
    ast.fix_missing_locations(tree)
    path.write_text(ast.unparse(tree) + '\n', encoding='utf-8')


def build(tree_root, out):
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(ZIP, out, ignore=shutil.ignore_patterns('source', 'diffs', 'inputs', '__pycache__', 'mplcache'))
    ev = out / 'evidence'
    if ev.exists():
        shutil.rmtree(ev)
    ev.mkdir()
    man = json.loads((ZIP / 'source_manifest.json').read_text(encoding='utf-8'))
    files = man['files']
    paths = list(files) if isinstance(files, dict) else [f['path'] for f in files]
    missing = []
    for p in paths:
        s, d = tree_root / p, out / 'source' / p
        d.parent.mkdir(parents=True, exist_ok=True)
        if s.exists():
            shutil.copy2(s, d)
        else:
            missing.append(p)
    for pat in ('scripts/*.py', 'webapp/*.py', 'webapp/*.json'):
        for s in tree_root.glob(pat):
            d = out / 'source' / s.relative_to(tree_root)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, d)
    for p in SOFTEN:
        soften(out / p)
    return missing


if __name__ == '__main__':
    tree_root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    names = sys.argv[3:] or ['new_network', 'independent_lw']
    miss = build(tree_root, out)
    print('manifest paths missing in tree:', len(miss), miss[:10])
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    r = subprocess.run([sys.executable, str(out / 'run_probes.py'), *names], cwd=out, env=env, capture_output=True,
                       text=True, timeout=3600)
    print('run_probes rc', r.returncode)
    print(r.stdout[-3000:])
    print(r.stderr[-3000:])
    for p in SOFTEN:
        sj = (out / p).with_suffix('.soft_asserts.json')
        if sj.exists():
            soft = json.loads(sj.read_text(encoding='utf-8'))
            print(p, 'asserts', len(soft), 'not held:', [(s['line'], s['src'][:90], s['error']) for s in soft if s['held'] is not True])
