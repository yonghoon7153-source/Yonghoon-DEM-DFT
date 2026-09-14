"""dd_shims 3자 대조 — 우리 shim · Octave 내장 · Python 포팅.

무엇을 증명하나:
  · `quantile` shim ≡ Octave 내장 `quantile`(method 5). Octave 의 method 5 는
    MATLAB 의 정의((i-0.5)/n plotting position)와 같으므로, 이 일치는 우리
    shim 이 **MATLAB 정의를 구현했다**는 제3자 확인이다.
  · `quantile` shim ≡ Python `matlab_quantile`.
  · `sgolayfilt` shim ≡ Python `sgolay`(scipy savgol_filter, mode='interp').
    특히 **가장자리** 구간 — model.py 가 "완전히 같은 수는 아닐 수 있다" 고
    적어 둔 바로 그 자리다.
  · `findpeaks` shim ≡ Python `scipy.signal.find_peaks(prominence=...)`.
    위치(1-based↔0-based)와 **개수**까지 본다.

무엇을 증명 못 하나:
  MathWorks 의 진짜 `sgolayfilt`·`findpeaks`. 이 컨테이너에 Signal Processing
  Toolbox 가 없다. `findpeaks` 는 Octave core 에도 없어서(`exist` → 0) 3자
  대조가 아니라 **shim↔scipy 2자** 대조다 — 제3의 독립 구현이 없다.
  평탄 꼭대기 규약은 scipy 쪽에 맞춰져 있고 MathWorks 와 다를 수 있다
  (dd_shims/findpeaks.m 머리말).

  ⚠ 사용자 기계에는 툴박스 **라이선스가 있다**(2026-09-10 `license('test')`
    4종 전부 1). 설치하면 `addpath(...,'-end')` 때문에 진짜 함수가 이기고
    shim 은 안 쓰인다. 그때 `dd_eval` 이 CSV 에 적는 `# impl_sgolayfilt,matlab`
    이 그 사실의 증거이고, 그 산출을 이 shim 기준 산출과 비교하면 **MathWorks
    구현과 우리 정의의 차이**가 처음으로 측정된다.
"""
import sys, csv, pathlib
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from scipy.signal import find_peaks
from bms_balancing.model import matlab_quantile, sgolay

D = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".") / "cases"
P = np.loadtxt(D/"pvals.csv")
names = ['n1','n2','n4_int','n5_unsort','n7_dup','n50_rand','n101_ramp','n500_ocv']
vec = {n: np.atleast_1d(np.loadtxt(D/f"vec_{n}.csv")) for n in names}

def load(fn):
    out = {}
    with open(fn) as fh:
        for r in csv.DictReader(fh):
            key = (r["kind"], r["vec"], r["arg1"], r["arg2"], int(r["idx"]))
            out[key] = float(r["value"])
    return out

BASE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
oct_native, oct_shim = load(BASE/"res_oct_native.csv"), load(BASE/"res_oct_shim.csv")

def rpt(title, pairs):
    if not pairs:
        print(f"  {title}: (없음)"); return 0.0
    d = np.array([abs(a-b) for a,b in pairs])
    rel = np.array([abs(a-b)/max(abs(b),1e-12) for a,b in pairs])
    print(f"  {title}: n={len(pairs)}  max|Δ|={d.max():.3e}  max rel={rel.max():.3e}")
    return d.max()

print("=== 1. quantile ===")
py_q, sh_q, nv_q = [], [], []
for n in names:
    for p in P:
        k = ("quantile", n, f"{p:.17g}", "", 1)
        pyv = matlab_quantile(vec[n], p)
        py_q.append((pyv, oct_shim[k])); sh_q.append((oct_shim[k], oct_native[k]))
worst_a = rpt("shim(MATLAB용) vs Python matlab_quantile", py_q)
worst_b = rpt("shim vs Octave core quantile(method 5)", sh_q)

print("=== 2. sgolayfilt ===")
maxes = {}
with open(D/"sgcases.csv") as fh:
    for r in csv.DictReader(fh):
        n, od, fl = r["vec"], int(r["order"]), int(r["framelen"])
        x = vec[n]
        pyy = sgolay(x, od, fl)
        shy = np.array([oct_shim[("sgolay", n, str(od), str(fl), k+1)] for k in range(len(x))])
        d = np.abs(pyy - shy)
        maxes[(n,od,fl)] = d.max()
        # 가장자리와 내부를 나눠서 본다 — 다르면 가장자리에서 갈린다
        m = (fl-1)//2
        edge = max(d[:m].max() if m else 0.0, d[-m:].max() if m else 0.0)
        core = d[m:len(x)-m].max()
        print(f"  {n:11s} order={od} f={fl:2d}: max|Δ|={d.max():.3e}  (가장자리 {edge:.3e} / 내부 {core:.3e})")
worst_c = max(maxes.values())

print("=== 3. findpeaks (shim vs scipy — 제3 구현 없음) ===")
fp_bad, fp_n = [], 0
with open(D/"fpcases.csv") as fh:
    for r in csv.DictReader(fh):
        n, prom = r["vec"], float(r["prominence"])
        x = np.atleast_1d(np.loadtxt(D/f"fpvec_{n}.csv"))
        key = f"{prom:.17g}"
        cnt = int(oct_shim[("findpeaks", n, key, "", 0)])
        sh = [int(oct_shim[("findpeaks", n, key, "", k+1)]) for k in range(cnt)]
        py = (find_peaks(x, prominence=prom)[0] + 1).tolist()   # 1-based 로 맞춘다
        fp_n += 1
        if sh != py:
            fp_bad.append((n, prom, sh, py))
        print(f"  {n:8s} prom={prom:<5g} n={cnt:<4d} {'일치' if sh == py else 'X 불일치'}")
for n, prom, sh, py in fp_bad:
    print(f"  ! {n} prom={prom:g}: shim={sh}  scipy={py}")
print(f"  → {fp_n - len(fp_bad)}/{fp_n} 조합 일치")

print()
print(f"WORST quantile shim-vs-python : {worst_a:.3e}")
print(f"WORST quantile shim-vs-octave : {worst_b:.3e}")
print(f"WORST sgolay  shim-vs-python  : {worst_c:.3e}")
print(f"findpeaks shim-vs-scipy      : {fp_n - len(fp_bad)}/{fp_n} 조합 일치")
ok = (worst_a < 1e-12 and worst_b < 1e-12 and worst_c < 1e-9 and not fp_bad)
print("RESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
