"""Fixed-source syntax audit only. No numerical module is imported."""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PIN = "64e4d213e8267bafaf3ae5af00a42996cefd3f33"
SOURCES = [
    ("scripts/step3_sigma.py", "859310dafac800dc75ecbae36702cb8aab185660abc6675fe4d8b02fc21b459a"),
    ("scripts/carbon_junction.py", "679dbc383c0ae399c33be0102be76a7b1f3db9c93f16dff4eff4b5f7031791cb"),
]


def git(*args):
    return subprocess.check_output([
        "git", "-c", "core.longpaths=true", "-c", "safe.directory=" + REPO.as_posix(),
        "-C", str(REPO), *args])


def read(path, expected):
    raw = git("show", PIN + ":" + path)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected:
        raise ValueError("fixed source mismatch")
    oid = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if oid != git("rev-parse", PIN + ":" + path).decode().strip():
        raise ValueError("fixed blob mismatch")
    return ast.parse(raw.decode("utf-8")), dict(
        pin=PIN, path=path, bytes=len(raw), sha256=digest, git_blob=oid)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    step, sid = read(*SOURCES[0])
    carbon, cid = read(*SOURCES[1])
    solve = next(n for n in step.body if isinstance(n, ast.FunctionDef) and n.name == "solve_sigma_z")
    cls = next(n for n in carbon.body if isinstance(n, ast.ClassDef) and n.name == "CjuncAssembler")
    assemble = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "_assemble")
    # Narrow source regions are explicit; this is not a global call-graph proof.
    region = [n for n in ast.walk(solve) if 2321 <= getattr(n, "lineno", 0) <= 2347]
    branches = sorted([
        dict(line=n.lineno, end=n.end_lineno, condition=ast.unparse(n.test),
             return_lines=sorted(r.lineno for r in ast.walk(n) if isinstance(r, ast.Return)))
        for n in region if isinstance(n, ast.If)
    ], key=lambda v: v["line"])
    binding = []
    for n in region:
        if isinstance(n, ast.Assign):
            binding.append(dict(line=n.lineno, targets=[ast.unparse(t) for t in n.targets],
                                value=ast.unparse(n.value)))
    selected_calls = sorted([
        dict(line=n.lineno, function=ast.unparse(n.func))
        for n in ast.walk(solve) if isinstance(n, ast.Call)
        and ast.unparse(n.func) in ("_cjs.build", "_solve_cg", "_cjs.sv_counterfactual")
    ], key=lambda v: (v["line"], v["function"]))
    returns = sorted([dict(line=n.lineno, end=n.end_lineno,
                           value=ast.unparse(n.value))
                      for n in region if isinstance(n, ast.Return)], key=lambda v: v["line"])
    last = next(n for n in ast.walk(assemble) if isinstance(n, ast.Return) and n.lineno == 2819)
    output_dict = next(n for n in ast.walk(last) if isinstance(n, ast.Dict))
    if not all(isinstance(k, ast.Constant) and type(k.value) is str for k in output_dict.keys):
        raise ValueError("unexpected return keys")
    original_order = next(n for n in ast.walk(assemble)
                          if isinstance(n, ast.Call) and ast.unparse(n.func) == "np.flatnonzero"
                          and n.lineno == 2789)
    obj = dict(
        sources=[sid, cid], function=dict(name=solve.name, range=[solve.lineno, solve.end_lineno]),
        selected_region=[2321, 2347], branches=branches,
        assignments=sorted(binding, key=lambda v: v["line"]),
        early_returns=returns, selected_solver_calls=selected_calls,
        producer_original_order=dict(line=original_order.lineno, expression=ast.unparse(original_order)),
        producer_completed_return=dict(line=last.lineno, keys=[k.value for k in output_dict.keys]),
        scope="AST/source order only; no assembly, solve, values, call-graph closure or ownership proof",
    )
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode()
    out = HERE / "consumer_map.json"
    if args.write:
        with out.open("xb") as f:
            f.write(raw)
    elif out.read_bytes() != raw:
        raise ValueError("consumer map differs")
    print("consumer_map.json: fixed-source AST map matches")


if __name__ == "__main__":
    main()
