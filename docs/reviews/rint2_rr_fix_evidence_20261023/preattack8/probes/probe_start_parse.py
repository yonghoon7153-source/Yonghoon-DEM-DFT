"""Start-record parsing classes (unit): duplicate key · NaN · Infinity · non-canonical spacing · string n · float n · NUL in base ·
base not normalised · trailing slash · huge n · CRLF line · BOM.   python3 -I probe_start_parse.py <tree>"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve() / 'scripts'))
import rint_r_chain as RR  # noqa: E402

HDR = {'kind': 'header', 'schema': 'rint-r-ledger-v1', 'plan_sha256': 'a' * 64, 'utc': 't'}
ENT = {'kind': 'entry', 'n': 1, 'target': 'ladder:P0', 'machine': 'kgy', 'resume_of': None, 'plan_sha256': 'a' * 64, 'code_key_sha256': 'b' * 64,
       'env': {}, 'bed': {}, 'utc': 't'}
ST = {'kind': 'start', 'n': 1, 'base': '/srv/runs', 'folder': 'attempt_1', 'host': {'machine_id': None, 'boot_id': 'b', 'pidns': 'p'}, 'utc': 't'}


def L(*lines):
    return ''.join(x if isinstance(x, str) else RR.ledger_line(x) for x in lines).encode('utf-8')


canon = RR.ledger_line(ST)
cases = {
    'ok': L(HDR, ENT, ST),
    'dup_key': L(HDR, ENT, canon.replace('"base":"/srv/runs",', '"base":"/srv/runs","base":"/srv/runs",')),
    'nan_utc': L(HDR, ENT, canon.replace('"utc":"t"', '"utc":NaN')),
    'inf_n': L(HDR, ENT, canon.replace('"n":1', '"n":Infinity')),
    'spacing': L(HDR, ENT, canon.replace('"n":1', '"n": 1')),
    'n_str': L(HDR, ENT, dict(ST, n='1')),
    'n_float': L(HDR, ENT, canon.replace('"n":1,', '"n":1.0,')),
    'nul_base': L(HDR, ENT, dict(ST, base='/srv/\x00runs')),
    'base_dotdot': L(HDR, ENT, dict(ST, base='/srv/x/../runs')),
    'base_slash': L(HDR, ENT, dict(ST, base='/srv/runs/')),
    'n_huge': L(HDR, ENT, dict(ST, n=10 ** 30, folder=f'attempt_{10 ** 30}')),
    'crlf': L(HDR, ENT, canon.replace('\n', '\r\n')),
    'bom': b'\xef\xbb\xbf' + L(HDR, ENT, ST),
    'nbsp_folder': L(HDR, ENT, dict(ST, folder='attempt_1 ')),
    'arabic_digit_folder': L(HDR, ENT, dict(ST, folder='attempt_١')),
}
out = {}
for k, raw in cases.items():
    try:
        st = RR.ledger_parse(raw)
        out[k] = ('accepted', sorted(st['starts']))
    except RR.Stop as e:
        out[k] = ('refused', e.code)
print(json.dumps(out, ensure_ascii=False, indent=1))
