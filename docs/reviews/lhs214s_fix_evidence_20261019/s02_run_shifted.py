"""L214R-S02 증거 — R01 경계 시험 파일을 그대로 불러 등록 입력 E_BY 만 box_y ULP 이동 (Codex 환경 꼴 재현) 한 뒤 main() 실행.  시험 파일 바이트는 바꾸지 않는다.
python3 -B run_shifted.py <시험 파일> <이동 ULP>"""
import hashlib
import importlib.util
import math
import sys
from pathlib import Path
path, shift = Path(sys.argv[1]).resolve(), int(sys.argv[2])
print(f'시험 파일 {path} sha256 {hashlib.sha256(path.read_bytes()).hexdigest()} · E_BY 이동 {shift:+d} ULP')
spec = importlib.util.spec_from_file_location('t_r01_shifted', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def mv(v):
    for _ in range(abs(shift)):
        v = math.nextafter(v, math.inf if shift > 0 else 0.0)
    return v


m.E_BY = {k: mv(v) for k, v in m.E_BY.items()}
print('E_BY =', m.E_BY)
sys.exit(m.main())
