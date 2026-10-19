"""L214R-S02 증거 (시간) — R01 경계 시험 파일 여러 판을 불러 묶음별 벽시계 시간 · E0 탐색 시간 · 범위 밖 실패 경로 시간을 잰다 (판정 아님 · 시험 파일 바이트 그대로).
python3 -B s02_timing.py <리포 루트> <시험 파일> [<시험 파일> …]
  · 묶음 = R · E · E′ · E″ (있으면) · E5 · C · B — 각 판을 따로 불러 (모듈 이름 분리) 한 번씩 · 출력은 버리고 PASS/전체 수만 적는다.
  · e0_search 에 kmax 가 있는 판 (둘째 축) 만: 등록 출발 · E″ 두 출발의 탐색 시간 · 범위 밖 실패 (E″b 출발 · kmax 3 = 면적 7 개) → 면적당 시간 × 129 (상한 64 의 추정) ·
    전 범위 실패 상한 (세 경계 대신 이웃한 넷 = 한 면적에서 동시에 못 나온다 — 격자 간격 1.414 ulp > 4/3 · 129 면적 전부 실패 · 직접 잰 값)."""
import contextlib
import importlib.util
import io
import math
import sys
import time
from pathlib import Path

root = Path(sys.argv[1]).resolve()
for p in (str(root / 'scripts'), str(root / 'webapp')):
    if p not in sys.path:
        sys.path.insert(0, p)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def timed(fn):
    t = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        fn()
    return time.perf_counter() - t


for i, f in enumerate(sys.argv[2:]):
    m = load(Path(f).resolve(), f't_timing_{i}')
    import hashlib
    print(f'== {f} sha256 {hashlib.sha256(Path(f).read_bytes()).hexdigest()[:16]}…')
    state = {'tmp': []}
    secs = [('R', 'sec_R'), ('E', 'sec_E'), ('E′', 'sec_E_shift'), ('E″', 'sec_E2'), ('E5', 'sec_E5'), ('C', 'sec_C'), ('B', 'sec_B')]
    tot = 0.0
    try:
        for lab, fn in secs:
            if not hasattr(m, fn):
                print(f'   {lab:3s} (없음)')
                continue
            ok0, f0 = m._ok, len(m._fail)
            dt = timed(lambda: getattr(m, fn)(state))
            tot += dt
            print(f'   {lab:3s} {dt:6.2f} s · PASS {m._ok - ok0}/{m._ok - ok0 + len(m._fail) - f0}')
    finally:
        import shutil
        for d in state['tmp']:
            shutil.rmtree(d, ignore_errors=True)
    print(f'   합계 {tot:6.2f} s · PASS {m._ok}/{m._ok + len(m._fail)}')
    import inspect
    two_axis = hasattr(m, 'e0_search') and 'kmax' in inspect.signature(m.e0_search).parameters
    if not two_axis:
        continue
    import network_conductivity as nc
    for lab, a0 in (('등록', m.E_AREA), ('E″a', m.E2_START['a']), ('E″b', m.E2_START['b'])):
        t = time.perf_counter()
        r = m.e0_search(nc, a0, m.E_BX, m.E_BY)
        print(f'   e0_search {lab:4s} {time.perf_counter() - t:6.2f} s · 시도 {len(r["tried"])} · 찾음 {not r["probs"]}')
    t = time.perf_counter()
    r = m.e0_search(nc, m.E2_START['b'], m.E_BX, m.E_BY, kmax=3)
    dt = time.perf_counter() - t
    n = len(r['tried'])
    print(f'   범위 밖 실패 (E″b 출발 · kmax 3) {dt:6.2f} s · 면적 {n} · 찾음 {not r["probs"]} · 면적당 {dt / n:.3f} s → 129 면적 추정 {dt / n * 129:6.1f} s')
    q0 = m.E_Q
    m.E_Q = {'n2': math.nextafter(math.nextafter(1.5, 2.0), 2.0), 'next': q0['next'], 'eq': q0['eq'], 'prev': q0['prev']}
    by0 = dict(m.E_BY, n2=m.E_BY['next'])
    t = time.perf_counter()
    try:
        r = m.e0_search(nc, m.E_AREA, m.E_BX, by0)
    finally:
        m.E_Q = q0
    dt = time.perf_counter() - t
    print(f'   전 범위 실패 상한 (이웃한 경계 넷 · kmax {m.E_AREA_ULP}) {dt:6.2f} s · 면적 {len(r["tried"])} · 찾음 {not r["probs"]}')
