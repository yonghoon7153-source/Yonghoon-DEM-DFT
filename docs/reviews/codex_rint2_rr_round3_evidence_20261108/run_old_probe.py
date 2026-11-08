import hashlib, json, os, sys
from pathlib import Path

root = Path(__file__).resolve().parent
repo = Path(os.environ.get('RINT_REVIEW_REPO', str(root / 'package' / 'repo'))).resolve()
src = repo / 'docs/reviews/codex_rint2_rr_round2_evidence_20261105/runtime_review/probe_runtime.py'
out = root / 'round2_replay'
out.mkdir(exist_ok=True)
(root / 'temp').mkdir(exist_ok=True)
os.environ['TEMP'] = os.environ['TMP'] = str(root / 'temp')
original = src.read_text(encoding='utf-8')
needle = "REPO = HERE.parent / 'received' / 'repo'"
assert original.count(needle) == 1
adapted = original.replace(needle, "REPO = Path(" + repr(str(repo)) + ")")
start = adapted.index('# Documentary source availability/hashes,')
end = adapted.index('# Known open PC6-05:', start)
# The narrowed package omits the historical 93-file report_c_raw archive.
# Skip its two availability checks; do not count them as executed or passed.
adapted = adapted[:start] + "# Skipped: report_c_source_manifest_count and report_c_source_hashes (not packaged).\n\n" + adapted[end:]
# Windows only: disk regular files do not implement POSIX O_NONBLOCK.
# This does not validate FIFO, Linux flock, /proc access or process containment.
if os.name == 'nt':
    adapted = adapted.replace('import rint_r_chain as r', "os.O_NONBLOCK = getattr(os, 'O_NONBLOCK', 0)\nimport rint_r_chain as r", 1)
dest = out / 'probe_runtime.py'
dest.write_text(adapted, encoding='utf-8', newline='\n')
(out / 'adaptation.json').write_text(json.dumps({'source': str(src.relative_to(repo)), 'source_sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'adapted_sha256': hashlib.sha256(dest.read_bytes()).hexdigest(), 'changes':['REPO path only', 'Windows missing O_NONBLOCK is 0 for regular synthetic files'], 'skipped':['report_c_source_manifest_count','report_c_source_hashes'], 'skip_reason':'historical report_c_raw is outside this 660-file package', 'oracles_changed':False, 'field_qualification':False}, indent=2), encoding='utf-8')
sys.argv = [str(dest)]
exec(compile(adapted, str(dest), 'exec'), {'__name__':'__main__', '__file__':str(dest)})
