"""Rebuild the pinned, self-contained RT development reader with two header edits."""
import argparse
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_READER = 'b58dbd74d73dbe8fb046e83ad78d266c3bb207cd04410c6a599e3a610d28a9a4'
EDITS = [
    ('p1_rt_numeric_preparation_20261117/rt_numeric.py',
     b"if lines[8] != 'ITEM: ENTRIES ' + ' '.join(expected):",
     b"if lines[8] not in (header, header + ' '):",
     b"        header = 'ITEM: ENTRIES ' + ' '.join(expected)\n"),
    ('p1_rt_consumer_preparation_20261117/rt_contract.py',
     b"lines[8]!='ITEM: ATOMS '+' '.join(ATOM_COLS):",
     b"lines[8] not in (header, header + ' '):",
     b"        header = 'ITEM: ATOMS ' + ' '.join(ATOM_COLS)\n"),
]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def replace_once(raw, before, after):
    if raw.count(before) != 1:
        raise ValueError("previous reader source does not match")
    return raw.replace(before, after, 1)


def render():
    folder = HERE.parent / 'p1_rt_consumer_preparation_20261117'
    spec = importlib.util.spec_from_file_location('consumer', folder / 'prepare_consumer.py')
    prior = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prior)
    raw, _ = prior.standalone(HERE.parents[2] / 'docs/data/ps45_unload_20261009')
    if digest(raw) != BASE_READER:
        raise ValueError("unexpected base reader")
    for path, old, new, declaration in EDITS:
        source = (HERE.parent / path).read_bytes()
        start = source.rindex(b'\n', 0, source.index(old)) + 1
        updated = source[:start] + declaration + replace_once(source[start:], old, new)
        raw = replace_once(raw, source.hex().encode(), updated.hex().encode())
        raw = replace_once(raw, digest(source).encode(), digest(updated).encode())
    compile(raw, 'read_rt_grammar_v2.py', 'exec')
    return raw


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    output = parser.parse_args().output
    with output.open('xb') as stream:
        stream.write(render())
