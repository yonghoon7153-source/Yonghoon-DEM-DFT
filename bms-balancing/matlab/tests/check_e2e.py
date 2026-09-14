"""두 전사본(Octave dd_eval.m · Python mirror)의 산출을 **수치 허용오차로** 대조.

바이트 대조는 너무 빡빡하다: `linspace` 의 마지막 자리 반올림이 Octave 와
numpy 에서 1 ULP 다르다. 그건 배관 버그가 아니라 부동소수점 차이다. 그래서
여기서는 (a) 상대오차 상한과 (b) **정수인 `dv_n` 은 정확히 일치** 를 본다.
`dv_n` 이 갈리면 분위수 창 경계가 격자점을 하나 먹거나 뱉었다는 뜻이고,
그건 진짜 발견이다.

⚠ 그리고 **fixture 가 진실을 가리는 자리**를 따로 막는다. dQ/dV 항은 보간
  범위에 든 점이 5 개 미만이면 원본 규약대로 `1e6` 을 낸다. 그러면 양쪽 다
  1e6 이라 상대오차 0 으로 **통과해 버린다** — 경로를 아예 안 탔는데 초록불이
  뜬다. 같은 함정을 이 저장소에서 이미 한 번 밟았다(합성 Si/Gr 가 정규화 뒤
  동일해져 γ 가 아무 효과도 없었는데 스모크가 통과). 그래서 아래
  `assert_dqdv_alive` 가 산출이 **degenerate 하지 않다**는 것을 따로 본다.
"""
from __future__ import annotations
import sys, pathlib

TOL_REL = 1e-12          # 부동소수점 잡음 상한 (1 ULP ≈ 2e-16)


def parse(p: pathlib.Path):
    anchors, rows, header = {}, [], []
    for line in p.read_text().splitlines():
        if line.startswith("# ") and "," in line:
            k, _, v = line[2:].partition(",")
            try:
                anchors[k] = float(v)
            except ValueError:
                pass
        elif line.startswith("a_PE"):
            header = [c.strip() for c in line.split(",")]
        elif line and not line.startswith("#"):
            rows.append([float(x) for x in line.split(",")])
    return anchors, rows, header


def assert_dqdv_alive(anchors, rows, header):
    """dQ/dV 경로가 **실제로 계산됐는지** — 통과가 공짜가 아니게."""
    probs = []
    if "rmse_dqdv" not in header:
        return probs                      # 옛 산출이면 볼 것이 없다
    i_u, i_w = header.index("rmse_dqdv"), header.index("rmse_dqdv_w")
    col_u = [r[i_u] for r in rows]
    col_w = [r[i_w] for r in rows]
    if any(v >= 1e6 for v in col_u):
        probs.append("rmse_dqdv 에 1e6 이 있다 — 보간 범위에 5 점도 못 들었다"
                     " (경로를 안 탔는데 양쪽 1e6 이라 조용히 통과할 뻔했다)")
    if anchors.get("n_peaks", 0) < 1:
        probs.append("n_peaks=0 — findpeaks 가 아무것도 못 찾아 가중이 전부 1 이다"
                     " (가중 경로가 무가중과 구별되지 않는다)")
    if anchors.get("dq_nin_p1", 0) < 5:
        probs.append(f"dq_nin_p1={anchors.get('dq_nin_p1')} — 보간에 든 점이 없다")
    if all(abs(a - b) < 1e-15 for a, b in zip(col_u, col_w)):
        probs.append("rmse_dqdv 와 rmse_dqdv_w 가 전부 같다 — 피크 가중이 무효다")
    if len(set(f"{v:.12g}" for v in col_u)) < 2:
        probs.append("rmse_dqdv 가 모든 p 에서 같다 — 파라미터가 도달하지 않았다")
    return probs


def compare(fa: pathlib.Path, fb: pathlib.Path):
    A, RA, HA = parse(fa)
    B, RB, HB = parse(fb)
    problems, worst = [], 0.0
    if HA != HB:
        problems.append(f"열 이름이 다르다: {HA} vs {HB}")
    problems += [f"[{fa.name}] {t}" for t in assert_dqdv_alive(A, RA, HA)]
    problems += [f"[{fb.name}] {t}" for t in assert_dqdv_alive(B, RB, HB)]
    if set(A) != set(B):
        problems.append(f"앵커 이름이 다르다: {sorted(set(A) ^ set(B))}")
    for k in sorted(set(A) & set(B)):
        a, b = A[k], B[k]
        if k == "dv_n":
            if a != b:
                problems.append(f"dv_n 이 다르다: {a:g} vs {b:g} — 분위수 창이 격자점을 먹었다")
            continue
        rel = abs(a - b) / max(abs(b), 1e-30)
        worst = max(worst, rel)
        if rel > TOL_REL:
            problems.append(f"앵커 {k}: {a!r} vs {b!r}  (rel {rel:.3e})")
    if len(RA) != len(RB):
        problems.append(f"행 수가 다르다: {len(RA)} vs {len(RB)}")
    else:
        for i, (ra, rb) in enumerate(zip(RA, RB)):
            for j, (a, b) in enumerate(zip(ra, rb)):
                rel = abs(a - b) / max(abs(b), 1e-30)
                worst = max(worst, rel)
                if rel > TOL_REL:
                    problems.append(f"행 {i} 열 {j}: {a!r} vs {b!r}  (rel {rel:.3e})")
    return problems, worst


if __name__ == "__main__":
    probs, worst = compare(pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]))
    print(f"max rel dev = {worst:.3e}   (허용 {TOL_REL:.0e})")
    for p in probs:
        print("  !", p)
    sys.exit(1 if probs else 0)
