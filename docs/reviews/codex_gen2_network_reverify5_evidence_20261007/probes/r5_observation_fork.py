"""Read-only production census plus inert lexical-limit controls; never fork."""
import argparse, ast, json
from pathlib import Path
import r5_observation as p

examples = {
    'canonical_os_fork': 'import os\nos.fork()\n',
    'multiprocessing': 'import multiprocessing\n',
    'from_os_import_fork': 'from os import fork\nfork()\n',
    'aliased_os_fork': 'import os as operating_system\noperating_system.fork()\n',
    'getattr_os_fork': 'import os\ngetattr(os, "fork")()\n',
}
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-name', default='r5_observation_fork_repeat', help='Fresh evidence subdirectory')
args = parser.parse_args()
if Path(args.output_name).name != args.output_name or args.output_name in ('.', '..'):
    parser.error('--output-name must be one plain subdirectory name')
dest_root = p.R / 'evidence' / args.output_name
if dest_root.exists():
    parser.error(f'{dest_root} already exists; choose a fresh --output-name')
base = dest_root / 'inert_inputs'
rows = []
for label, source in examples.items():
    root = base / label
    dest = root / 'scripts/lhs_webapp_batch.py'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(source, encoding='utf8')
    rows.append(dict(label=label, detected=p.rn.fork_census(root)))
production_refs = []
process_attributes = []
for rel in p.rn.CODE_FILES:
    tree = ast.parse((p.S / rel).read_text(encoding='utf8'), filename=rel)
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr.startswith(('fork', 'posix_spawn', 'spawnl', 'spawnv')):
            process_attributes.append(dict(file=rel, line=node.lineno, expr=ast.unparse(node)))
        if isinstance(node, ast.ImportFrom) and node.module in ('os','pty','multiprocessing','concurrent.futures'):
            for name in node.names:
                if name.name.startswith(('fork','spawn','posix_spawn')) or name.name == 'ProcessPoolExecutor':
                    production_refs.append(dict(file=rel, line=node.lineno, module=node.module, name=name.name))
        if isinstance(node, ast.Import):
            for name in node.names:
                if name.name == 'multiprocessing' or (name.name == 'os' and name.asname):
                    production_refs.append(dict(file=rel, line=node.lineno, module=name.name, alias=name.asname))
out = dict(pinned_production_census=p.rn.fork_census(p.S), pinned_ast_relevant_imports=production_refs,
           pinned_ast_process_attributes=process_attributes, inert_examples=rows,
           interpretation='Pinned CODE_FILES have three os aliases (inspected uses are files/environment), no fork/spawn attributes or from imports. Regex guard is not a general proof against arbitrarily introduced Python fork code.')
p.write(dest_root / 'results.json', out)
print(json.dumps(out, ensure_ascii=False, indent=2))
