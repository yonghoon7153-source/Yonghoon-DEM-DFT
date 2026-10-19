"""L214R-S02 증거 (실패 경로) — R01 경계 시험 파일을 그대로 불러 둘째 축 상한 E_AREA_ULP 만 바꿔 main() 실행 (범위 밖 = 전제 불성립 FAIL 이 명시적으로
나오는지 · KeyError 없음 · E4 복원 안 부름 · E5 독립).  시험 파일 바이트는 바꾸지 않는다.
python3 -B s02_run_bound.py <시험 파일> <E_AREA_ULP>"""
import hashlib
import importlib.util
import sys
from pathlib import Path
path, kmax = Path(sys.argv[1]).resolve(), int(sys.argv[2])
print(f'시험 파일 {path} sha256 {hashlib.sha256(path.read_bytes()).hexdigest()} · E_AREA_ULP {kmax}')
spec = importlib.util.spec_from_file_location('t_r01_bound', path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.E_AREA_ULP = kmax
print('E_AREA_ULP =', m.E_AREA_ULP)
sys.exit(m.main())
