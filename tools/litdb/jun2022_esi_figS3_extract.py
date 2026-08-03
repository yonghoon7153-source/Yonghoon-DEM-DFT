#!/usr/bin/env python3
"""jun2022 ESI Fig S3(a) 실물 검증 — chi_c^7.14 회귀의 산점도 마커 복원.

왜 이 스크립트가 있나
---------------------
digest §8.3 은 2026-07-28 판독에서 Fig S3(a) 를 *"결정화도 0.57–1.0 구간의 8점 남짓,
R² 없음, 오른쪽 끝 (1.0, 1.0) 점은 데이터가 아니라 정의상 앵커이고 **지수 7.14 는 사실상
그 앵커가 결정한다**"* 고 적었다. 앞부분은 세어 보지 않은 추정이었고, 굵은 부분은
**검증되지 않은 인과 주장**이었다. 이 스크립트가 둘 다 실제로 판정한다:

  (1) 마커가 정확히 몇 개이고 (1,1) 앵커가 눈금과 정확히 일치하는가
  (2) 앵커를 빼고 다시 피팅하면 지수가 얼마인가 — 즉 앵커가 지수를 정하는가
  (3) 논문이 보고하지 않은 R² 는 얼마인가

방법은 `jun2022_fig_extract.py` 와 같다(순수 파이썬 연결성분, 이 머신에 numpy 없음).
축 보정은 눈금을 직접 검출한다 — Fig S3(a) 의 눈금은 스파인 **바깥쪽**으로 뻗는다.

사용
----
    python tools/litdb/jun2022_esi_figS3_extract.py <esi.pdf>

ESI PDF 는 litdb/inbox/ (gitignore) 에 있으므로 경로를 인자로 받는다.
"""
from __future__ import annotations

import io
import math
import sys
from collections import deque

import fitz  # PyMuPDF

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PAGE, CLIP, ZOOM = 11, (72, 85, 300, 262), 8   # ESI p.12 좌측 패널 (a)
XTICK_LABELS = [0.6, 0.8, 1.0]                 # 주눈금 (부눈금 0.7/0.9 는 제외)
YTICK_LABELS = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]  # 위 → 아래
PRINTED_EXPONENT = 7.14


def render(pdf):
    doc = fitz.open(pdf)
    pix = doc[PAGE].get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=fitz.Rect(*CLIP))
    return pix.samples, pix.width, pix.height, pix.n


def group(vals, tol=8):
    if not vals:
        return []
    out, cur = [], [vals[0]]
    for a in vals[1:]:
        if a - cur[-1] <= tol:
            cur.append(a)
        else:
            out.append(sum(cur) / len(cur))
            cur = [a]
    out.append(sum(cur) / len(cur))
    return out


def components(mask, W, H, min_size):
    seen = bytearray(W * H)
    out = []
    for start in range(W * H):
        if not mask[start] or seen[start]:
            continue
        q = deque([start])
        seen[start] = 1
        pts = []
        while q:
            c = q.popleft()
            pts.append(c)
            cx, cy = c % W, c // W
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        k = ny * W + nx
                        if mask[k] and not seen[k]:
                            seen[k] = 1
                            q.append(k)
        if len(pts) >= min_size:
            xs = [p % W for p in pts]
            ys = [p // W for p in pts]
            out.append({"n": len(pts), "cx": sum(xs) / len(xs), "cy": sum(ys) / len(ys),
                        "w": max(xs) - min(xs) + 1, "h": max(ys) - min(ys) + 1})
    return out


def fit_loglog(pts):
    """y = x^n 을 log-log 원점통과 최소제곱: n = sum(lx*ly)/sum(lx^2)."""
    num = den = 0.0
    for x, y in pts:
        lx, ly = math.log(x), math.log(y)
        num += lx * ly
        den += lx * lx
    return num / den


def fit_linear(pts, lo=1.0, hi=30.0, iters=80):
    """y = x^n 을 선형공간 SSE 최소화로 (황금분할)."""
    def sse(nn):
        return sum((y - x ** nn) ** 2 for x, y in pts)
    gr = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    for _ in range(iters):
        c, d = b - gr * (b - a), a + gr * (b - a)
        if sse(c) < sse(d):
            b = d
        else:
            a = c
    return (a + b) / 2


def r2(pts, nn):
    ys = [y for _, y in pts]
    my = sum(ys) / len(ys)
    ss_res = sum((y - x ** nn) ** 2 for x, y in pts)
    ss_tot = sum((y - my) ** 2 for y in ys)
    return 1 - ss_res / ss_tot


def main(pdf):
    s, W, H, n = render(pdf)

    def bl(x, y):
        i = (y * W + x) * n
        return s[i] < 110 and s[i + 1] < 110 and s[i + 2] < 110

    black = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            if bl(x, y):
                black[y * W + x] = 1

    # ── 스파인: 가장 긴 세로선 / 가로선 ──────────────────────────────────────
    col = [(x, sum(1 for y in range(int(H * .1), int(H * .87)) if bl(x, y)))
           for x in range(int(W * .2), W)]
    row = [(y, sum(1 for x in range(int(W * .23), W) if bl(x, y)))
           for y in range(int(H * .09), int(H * .87))]
    xspine = max(col, key=lambda t: t[1])[0]
    ybot = max((t for t in row if t[0] > H * .6), key=lambda t: t[1])[0]
    print(f"렌더 {W}x{H} @zoom{ZOOM} | 좌스파인 x={xspine} | 하단축 y={ybot}")

    # ── 눈금: 스파인 바깥쪽으로 뻗는 짧은 선 ────────────────────────────────
    yt = group([y for y in range(int(H * .1), ybot - 2)
                if sum(1 for x in range(xspine - 27, xspine - 1) if bl(x, y)) >= 16])
    xt = group([x for x in range(xspine + 2, W - 2)
                if sum(1 for y in range(ybot + 2, ybot + 32) if bl(x, y)) >= 16])
    print(f"  y주눈금 {len(yt)}개 px={[round(v,1) for v in yt]}")
    print(f"  x주눈금 {len(xt)}개 px={[round(v,1) for v in xt]}")
    if len(yt) != len(YTICK_LABELS) or len(xt) != len(XTICK_LABELS):
        print("  ⚠ 눈금 개수가 기대와 다르다 — 양끝만으로 선형 보정한다")

    sx = (XTICK_LABELS[-1] - XTICK_LABELS[0]) / (xt[-1] - xt[0])
    sy = (YTICK_LABELS[0] - YTICK_LABELS[-1]) / (yt[-1] - yt[0])

    def to_data(cx, cy):
        return (XTICK_LABELS[0] + (cx - xt[0]) * sx,
                YTICK_LABELS[-1] + (yt[-1] - cy) * sy)

    # ── 마커: 꽉 찬 정사각형 + 플롯 프레임 안쪽 ──────────────────────────────
    #    inset 수식(sigma_exp = sigma_calc chi^7.14)과 축 라벨 글자가
    #    크기만으로는 마커와 구별되지 않는다 → 채움비(면적/외접박스)로 거른다.
    #    실제 마커는 속이 찬 정사각형이라 채움비 ~0.99, 글자는 그보다 훨씬 낮다.
    marks = [c for c in components(black, W, H, 200)
             if 16 <= c["w"] <= 28 and 16 <= c["h"] <= 28
             and 0.8 <= c["w"] / c["h"] <= 1.25
             and c["n"] / (c["w"] * c["h"]) > 0.92
             and c["cx"] > xspine and c["cy"] < ybot]
    pts = sorted(to_data(c["cx"], c["cy"]) for c in marks)
    print(f"\n  ── 복원된 마커 {len(pts)}개 ──")
    print(f"  {'chi_c':>7} {'sig_exp/sig_calc':>17}   {'chi_c^7.14':>11} {'실측/예측':>10}")
    for X, Y in pts:
        pred = X ** PRINTED_EXPONENT
        print(f"  {X:7.4f} {Y:17.4f}   {pred:11.4f} {Y/pred:10.2f}x")

    anchor = [p for p in pts if p[0] > 0.97 and p[1] > 0.90]
    data = [p for p in pts if not (p[0] > 0.97 and p[1] > 0.90)]
    print(f"\n  (1,1) 앵커 {len(anchor)}개 "
          f"{'좌표 ' + f'({anchor[0][0]:.4f}, {anchor[0][1]:.4f})' if anchor else ''}"
          f" | 실측 데이터점 {len(data)}개 (chi_c {min(p[0] for p in data):.3f}"
          f"–{max(p[0] for p in data):.3f})")

    # ── 지수 재피팅 ─────────────────────────────────────────────────────────
    print(f"\n  ── 지수 재피팅 ── (인쇄값 {PRINTED_EXPONENT})")
    print(f"  {'집합':<22} {'N':>3} {'log-log 피팅':>13} {'선형공간 피팅':>14} "
          f"{'R²@7.14':>9} {'R²@최적':>9}")
    for tag, subset in (("앵커 포함 전체", pts), ("앵커 제외 (실측만)", data)):
        nl = fit_loglog(subset)
        nlin = fit_linear(subset)
        print(f"  {tag:<22} {len(subset):3d} {nl:13.2f} {nlin:14.2f} "
              f"{r2(subset, PRINTED_EXPONENT):9.3f} {r2(subset, nlin):9.3f}")

    print(f"\n  주: (1,1) 은 log-log 공간에서 (0,0) 이라 원점통과 피팅에 "
          f"가중이 0 이다.\n"
          f"      앵커의 역할은 지수를 '정하는' 것이 아니라 **계수를 1 로 고정**해\n"
          f"      1-파라미터 형태 y = chi^n 을 강제하는 것이다.")

    # ── 잔차 규모: 같은 결정화도에서 세로로 얼마나 벌어지나 ──────────────────
    print(f"\n  ── 같은 chi_c 에서의 세로 산포 (회귀가 설명 못 하는 부분) ──")
    for i, (X1, Y1) in enumerate(data):
        for X2, Y2 in data[i + 1:]:
            if abs(X1 - X2) < 0.03:
                hi_, lo_ = max(Y1, Y2), min(Y1, Y2)
                print(f"  chi_c {X1:.3f} vs {X2:.3f} (차 {abs(X1-X2):.3f}): "
                      f"비 {Y1:.4f} vs {Y2:.4f}  →  {hi_/lo_:.1f}배")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python tools/litdb/jun2022_esi_figS3_extract.py <esi.pdf>")
    main(sys.argv[1])
