"""Read fixed Git source bytes into AST maps; never import a target module."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DEM_PIN = "36054ada01fd9092ec38dbe32a7a27e9802863ac"
MIXER_PIN = "087ba5eb9a8d1d2c363d265bacfe064116361c80"
SPECS = [
    (DEM_PIN, "scripts/mpm3d_compaction.py",
     "b8bb85278b09e4232c933a868d332eb544b981b75e7367c82ce98b54cce17bdd"),
    (MIXER_PIN, "scripts/mixer_smoke_blind.py",
     "8a7954c6f9ba5808180256a70a6eab999c83bb06fdf5a2367f208f44072fcf8b"),
]


def git(*args):
    return subprocess.check_output([
        "git", "-c", "core.longpaths=true", "-c",
        "safe.directory=" + REPO.as_posix(), "-C", str(REPO), *args])


def source(spec):
    pin, path, expected = spec
    raw = git("show", pin + ":" + path)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected:
        raise ValueError("fixed source SHA mismatch")
    oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if oid != git("rev-parse", pin + ":" + path).decode().strip():
        raise ValueError("fixed Git blob mismatch")
    return ast.parse(raw.decode("utf-8")), dict(
        pin=pin, path=path, bytes=len(raw), sha256=digest, git_blob=oid)


def named_writes(nodes):
    result = {}
    for n in nodes:
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            result.setdefault(n.id, set()).add(n.lineno)
    return result


def calls(nodes, predicate):
    return sorted([
        dict(line=n.lineno, end=n.end_lineno, function=ast.unparse(n.func))
        for n in nodes if isinstance(n, ast.Call) and predicate(n)
    ], key=lambda n: (n["line"], n["function"]))


def dem_map():
    tree, identity = source(SPECS[0])
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    frame = next(n for n in main.body if isinstance(n, ast.For)
                 and isinstance(n.target, ast.Name) and n.target.id == "frame")
    if (frame.lineno, frame.end_lineno) != (3229, 3641):
        raise ValueError("unexpected frame range")
    nodes = list(ast.walk(frame))
    writes = named_writes(nodes)
    setup = named_writes(n for n in ast.walk(main) if 3169 <= getattr(n, "lineno", 0) < frame.lineno)
    mutations = calls(nodes, lambda n: isinstance(n.func, ast.Attribute)
                      and isinstance(n.func.value, ast.Name)
                      and n.func.attr in ("append", "pop", "extend", "clear", "update"))
    mutated = {}
    for c in mutations:
        mutated.setdefault(c["function"].split(".")[0], []).append(c["line"])
    selected = []
    for name in sorted(set(setup) & (set(writes) | set(mutated))):
        selected.append(dict(name=name, setup_lines=sorted(setup[name]),
                             binding_write_lines=sorted(writes.get(name, [])),
                             method_mutation_lines=mutated.get(name, [])))
    field_writes = sorted([
        dict(line=n.lineno, target=ast.unparse(n))
        for n in nodes if isinstance(n, ast.Subscript) and isinstance(n.ctx, ast.Store)
    ], key=lambda n: (n["line"], n["target"]))
    post = [n for n in ast.walk(main) if getattr(n, "lineno", 0) > frame.end_lineno]
    return dict(
        source=identity, scope="static syntax only; no execution or complete alias/dataflow analysis",
        frame_range=[frame.lineno, frame.end_lineno],
        selected_setup_range=[3169, 3228],
        setup_names_mutated_in_frame=selected,
        all_frame_name_store_sites={k: sorted(v) for k, v in sorted(writes.items())},
        direct_subscript_write_sites=field_writes,
        direct_list_mutations=mutations,
        selected_field_calls=calls(nodes, lambda n:
            ast.unparse(n.func) in ("substep", "rod_pass", "rod_setv")
            or (isinstance(n.func, ast.Attribute) and n.func.attr == "fill")),
        frame_print_calls=calls(nodes, lambda n: isinstance(n.func, ast.Name) and n.func.id == "print"),
        frame_control_exits=sorted([
            dict(kind=type(n).__name__, line=n.lineno, end=n.end_lineno)
            for n in nodes if isinstance(n, (ast.Break, ast.Continue, ast.Return, ast.Raise))
        ], key=lambda n: n["line"]),
        post_frame_raise_sites=sorted([
            dict(line=n.lineno, end=n.end_lineno) for n in post if isinstance(n, ast.Raise)
        ], key=lambda n: n["line"]),
        selected_post_frame_writes=calls(post, lambda n:
            ast.unparse(n.func) in ("np.save", "_json.dump", "write_state_npz")),
        selected_post_frame_prints=calls(post, lambda n:
            isinstance(n.func, ast.Name) and n.func.id == "print" and n.lineno < 3736),
        interpretation="Setup intersection is a candidate inventory, not a complete rollback closure.",
    )


def mixer_map():
    tree, identity = source(SPECS[1])
    names = ("run_blind", "_vault", "_blind_log", "run_contract_cert")
    rows = {}
    for name in names:
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
        rows[name] = dict(
            range=[fn.lineno, fn.end_lineno],
            selected_calls=calls(ast.walk(fn), lambda n:
                ast.unparse(n.func) in (
                    "os.open", "os.fdopen", "os.chmod", "os.replace",
                    "json.dump", "_sha_file", "_vault", "_blind_log")
                or (isinstance(n.func, ast.Attribute) and n.func.attr in
                    ("mkdir", "write", "write_text", "open"))),
            handlers=[dict(line=n.lineno, exception=ast.unparse(n.type) if n.type else None)
                      for n in ast.walk(fn) if isinstance(n, ast.ExceptHandler)],
            returns=[dict(line=n.lineno, end=n.end_lineno)
                     for n in ast.walk(fn) if isinstance(n, ast.Return)],
        )
    return dict(source=identity, functions=rows,
                scope="Four functions, source-order sites; not a call-graph, durability, race or runtime proof.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="create new map files exclusively")
    args = parser.parse_args()
    outputs = {"frame_map.json": dem_map(), "mixer_publication_map.json": mixer_map()}
    for name, obj in outputs.items():
        raw = (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()
        path = HERE / name
        if args.write:
            with path.open("xb") as stream:
                stream.write(raw)
        elif path.read_bytes() != raw:
            raise ValueError("map differs: " + name)
        print(name + ": fixed-source AST map matches")


if __name__ == "__main__":
    main()
