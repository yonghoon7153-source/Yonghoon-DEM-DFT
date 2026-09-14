"""dd_shims 대조용 결정론적 테스트 벡터.

세 구현(Octave 내장 · 우리 shim · Python 포팅)이 **같은 수**를 읽어야 하므로
난수를 그 자리에서 만들지 않고 파일로 고정한다 (seed 20260910).

사용: python3 gen_shim_cases.py <작업디렉터리>   → <작업디렉터리>/cases/ 에 쓴다
"""
import sys
import pathlib
import numpy as np

base = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent
d = base / "cases"
d.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(20260910)

vecs = {
    "n1":        np.array([3.5]),                       # 최소 길이
    "n2":        np.array([1.0, 2.0]),
    "n4_int":    np.array([1.0, 2.0, 3.0, 4.0]),
    "n5_unsort": np.array([5.0, 1.0, 4.0, 2.0, 3.0]),   # 정렬 안 된 입력
    "n7_dup":    np.array([2.0, 2.0, 2.0, 5.0, 9.0, 9.0, 1.0]),   # 중복값
    "n50_rand":  rng.normal(3.7, 1.3, 50),
    "n101_ramp": np.linspace(-2.0, 6.0, 101),
    # 실제 pOCV 를 닮은 모양 — 평활 가장자리 처리가 드러나게
    "n500_ocv":  4.2 - 1.2 * np.linspace(0, 1, 500) ** 1.7
                 + 0.01 * np.sin(np.linspace(0, 40, 500)),
}
for k, v in vecs.items():
    np.savetxt(d / f"vec_{k}.csv", v, fmt="%.17g")

# 규진팀 코드가 실제로 쓰는 분위수(0.05·0.15·0.85·0.95)와 양 끝 경계
np.savetxt(d / "pvals.csv",
           np.array([0.0, 0.001, 0.05, 0.15, 0.25, 0.5, 0.75, 0.85, 0.95, 0.999, 1.0]),
           fmt="%.17g")

# sgolayfilt 케이스: (벡터, order, framelen). 규진팀 설정은 order=3, framelen=11.
sg = [("n50_rand", 3, 11), ("n101_ramp", 3, 11), ("n500_ocv", 3, 11),
      ("n500_ocv", 1, 9), ("n500_ocv", 3, 31), ("n50_rand", 1, 5),
      ("n101_ramp", 2, 7), ("n500_ocv", 4, 21)]
with open(d / "sgcases.csv", "w") as fh:
    fh.write("vec,order,framelen\n")
    for a, b, c in sg:
        fh.write(f"{a},{b},{c}\n")

# ── findpeaks 케이스 ────────────────────────────────────────────────────
# ⚠ Octave core 에는 findpeaks 가 없다(`exist('findpeaks')` → 0). 그러므로
#   이 항목만은 **3자 대조가 안 되고** 우리 shim ↔ scipy 2자 대조다.
#   MathWorks 구현과의 알려진 차이(평탄 꼭대기 규약)는 dd_shims/findpeaks.m
#   머리말에 적어 두었다.
fp_rng = np.random.default_rng(20260910)
_v = np.linspace(0, 6 * np.pi, 200)
fpvecs = {
    "simple":  np.array([0., 1., 0., 2., 0., 3., 0., 2., 0., 1., 0.]),
    "plateau": np.array([0., 1., 2., 2., 2., 1., 3., 3., 1., 5., 5., 5., 5., 0.]),
    "flat":    np.zeros(20),                       # 봉우리가 하나도 없다
    "mono":    np.linspace(0, 10, 30),             # 단조 — 끝점은 봉우리가 아니다
    "noisy":   np.sin(_v) + 0.05 * fp_rng.normal(size=_v.size),
    # 실제 dQ/dV 를 닮은 모양 — 큰 봉우리 셋 + 잔물결
    "dqdv":    (3.0 * np.exp(-((_v - 4.0) ** 2) / 0.6)
                + 2.0 * np.exp(-((_v - 9.0) ** 2) / 0.9)
                + 1.2 * np.exp(-((_v - 14.0) ** 2) / 1.4)
                + 0.08 * np.sin(9 * _v)),
    "edge":    np.array([5., 4., 3., 2., 1., 2., 3., 4., 5.]),   # 골짜기뿐
    "two":     np.array([0., 5., 0., 5., 0.]),                   # 동점 봉우리
}
for k, v in fpvecs.items():
    np.savetxt(d / f"fpvec_{k}.csv", v, fmt="%.17g")

FP_PROM = [0.0, 0.1, 0.5, 1.0, 2.0]
with open(d / "fpcases.csv", "w") as fh:
    fh.write("vec,prominence\n")
    for k in fpvecs:
        for pr in FP_PROM:
            fh.write(f"{k},{pr:.17g}\n")

print(f"wrote {len(vecs)} vectors + {len(sg)} sgolay cases + {len(fpvecs)}x{len(FP_PROM)} findpeaks cases -> {d}")
