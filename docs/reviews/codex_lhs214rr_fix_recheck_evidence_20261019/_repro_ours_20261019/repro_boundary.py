"""읽기 전용 — R01 경계 시험 E 의 실 사슬 입력 (우리 등록값 · Codex 정확 경계값) 에서 이 환경의 H0 raw q.
python3 -B repro_boundary.py <우리 트리> <out.json>"""
import contextlib
import io
import json
import math
import os
import platform
import sys
from pathlib import Path
TREE, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
os.chdir(TREE)
sys.path[:0] = [str(TREE / 'scripts'), str(TREE / 'webapp')]
sys.dont_write_bytecode = True
import numpy as np  # noqa: E402
import scipy  # noqa: E402
import network_conductivity as nc  # noqa: E402
from test_lhs214_model_limit import chain_bed  # noqa: E402
SETS = {'ours_registered': (0.500000001, 0.7281737983374794, {'next': 0.7281737983374881, 'eq': 0.7281737983374882, 'prev': 0.7281737983374883}),
        'codex_exact': (0.500000001001, 0.7281737983374794, {'next': 0.7281737983380614, 'eq': 0.7281737983380615, 'prev': 0.7281737983380616})}
TARGET = {'next': math.nextafter(1.5, 2.0), 'eq': 1.5, 'prev': math.nextafter(1.5, 0.0)}
res = {'env': dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, machine=platform.machine(), system=platform.system())}
for lab, (area, bx, bys) in SETS.items():
    A, C, plate, _b = chain_bed(1.0, area=area)
    out = {}
    for k, by in bys.items():
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            du = nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1, plate, bx, by, None, contact_mode='hertzian')
        c = du['solve_certificate_full']
        T, Ar, _w = nc._geometry_TA(c['geometry'])
        q = (c['I_bottom'] / c['delta_V']) * T / Ar
        out[k] = dict(raw_q=repr(q), target=repr(TARGET[k]), hit=q == TARGET[k], ulp_off=round((q - TARGET[k]) / math.ulp(1.5)),
                      status=du.get('sigma_full_status'), reason=du.get('sigma_full_reason'))
    res[lab] = out
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(res, ensure_ascii=False))
