#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""huang2022 (JACS 2022, ja1c13178) ESI 그림 실물 판독.

litdb/inbox/47. Sup) ... .pdf.
그림 안의 눈금 숫자는 벡터 아웃라인이라 텍스트로 안 잡힌다 → 600 dpi 재렌더 후
축 프레임/눈금을 픽셀로 검출하고, 눈금 값만 사람이 읽어 주입해 보정한다.

사용:
    py -3.14 tools/litdb/huang2022_si_figs.py s4     # Fig S4 Nyquist 9패널 R 판독
    py -3.14 tools/litdb/huang2022_si_figs.py s5     # Fig S5 228/298 K 비교
"""
import glob
import sys

import fitz
from PIL import Image

PDF = glob.glob("litdb/inbox/47*.pdf")[0]
DPI = 600
S = DPI / 72.0

# Fig S4: 9 패널의 백색 배경 사각형(포인트 단위) — get_drawings() 로 얻은 값.
S4_BG = [
    (75.7, 75.4, 221.9, 205.2),
    (224.1, 75.4, 370.3, 205.2),
    (373.3, 75.4, 519.5, 205.2),
    (77.2, 209.7, 223.4, 339.5),
    (224.1, 209.7, 370.3, 339.5),
    (373.3, 209.7, 519.5, 339.5),
    (75.7, 344.0, 221.9, 473.8),
    (224.1, 344.0, 370.3, 473.8),
    (373.3, 344.0, 519.5, 473.8),
]
# 패널 라벨과 축 눈금 값(렌더 이미지에서 사람이 읽음).
S4_META = [
    ("228 K", [0, 1000, 2000, 3000, 4000], [0, 1000, 2000, 3000, 4000]),
    ("240 K", [0, 500, 1000, 1500], [0, 500, 1000, 1500]),
    ("260 K", [0, 100, 200, 300, 400, 500], [0, 100, 200, 300, 400, 500]),
    ("280 K", [0, 50, 100, 150, 200], [0, 50, 100, 150, 200]),
    ("RT (298 K)", [0, 20, 40, 60, 80], [0, 20, 40, 60, 80, 100]),
    ("300 K", [0, 20, 40, 60, 80], [0, 20, 40, 60, 80]),
    ("325 K", [0, 10, 20, 30], [0, 5, 10, 15, 20, 25, 30, 35]),
    ("350 K", [0, 5, 10, 15, 20], [0, 5, 10, 15, 20]),
    ("375 K", [0, 5, 10, 15], [0, 2, 4, 6, 8, 10, 12, 14]),
]


def render(pageno):
    out = f"/tmp/h47/img/p{pageno + 1}_{DPI}.png"
    pix = fitz.open(PDF)[pageno].get_pixmap(dpi=DPI)
    pix.save(out)
    return Image.open(out).convert("RGB")


def runs(idx):
    """연속 정수 리스트 -> [(start, end)]."""
    out = []
    for i in idx:
        if out and i == out[-1][1] + 1:
            out[-1][1] = i
        else:
            out.append([i, i])
    return [tuple(r) for r in out]


def find_frame(px, box, dark=250):
    """box=(x0,y0,x1,y1) 픽셀 범위 안에서 축 프레임 4선 위치."""
    x0, y0, x1, y1 = box
    W, H = x1 - x0, y1 - y0
    col = [sum(1 for y in range(y0, y1) if sum(px[x, y]) < dark) for x in range(x0, x1)]
    row = [sum(1 for x in range(x0, x1) if sum(px[x, y]) < dark) for y in range(y0, y1)]
    cx = runs([i for i, c in enumerate(col) if c > 0.55 * H])
    ry = runs([i for i, c in enumerate(row) if c > 0.55 * W])
    if len(cx) < 2 or len(ry) < 2:
        return None
    L = x0 + sum(cx[0]) / 2
    R = x0 + sum(cx[-1]) / 2
    T = y0 + sum(ry[0]) / 2
    B = y0 + sum(ry[-1]) / 2
    return L, T, R, B


def find_ticks(px, frame, box, axis, dark=250):
    """눈금은 프레임 안쪽을 향한다. 프레임 선 자체(양 끝)는 제외."""
    L, T, R, B = frame
    hits = []
    if axis == "x":
        band = range(int(B) - 13, int(B) - 4)
        for x in range(int(L) - 6, int(R) + 7):
            if sum(1 for y in band if sum(px[x, y]) < dark) >= 7:
                hits.append(x)
        ends = (L, R)
    else:
        band = range(int(L) + 5, int(L) + 14)
        for y in range(int(T) - 6, int(B) + 7):
            if sum(1 for x in band if sum(px[x, y]) < dark) >= 7:
                hits.append(y)
        ends = (T, B)
    pos = [sum(r) / 2 for r in runs(hits)]
    return [p for p in pos if all(abs(p - e) > 4 for e in ends)]


def fit(pos, vals):
    """최소제곱 선형 보정 + 최대잔차."""
    n = len(pos)
    sx, sy = sum(pos), sum(vals)
    sxx = sum(p * p for p in pos)
    sxy = sum(p * v for p, v in zip(pos, vals))
    a = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    b = (sy - a * sx) / n
    return a, b, max(abs(a * p + b - v) for p, v in zip(pos, vals))


def colored(px, frame, pad=18):
    """프레임 안(눈금 길이 밖)의 잉크 픽셀 = 마커. 회색 마커도 잡는다."""
    L, T, R, B = frame
    out = []
    for y in range(int(T) + pad, int(B) - pad):
        for x in range(int(L) + pad, int(R) - pad):
            r, g, b = px[x, y]
            if r + g + b < 700:
                out.append((x, y, (r, g, b)))
    return out


def cluster(pts, tol=9):
    """(x,y) 픽셀 -> 마커 덩어리 중심."""
    pts = sorted(pts)
    seen = set()
    idx = {}
    for i, (x, y, _) in enumerate(pts):
        idx.setdefault((x // tol, y // tol), []).append(i)
    out = []
    for i, (x, y, _) in enumerate(pts):
        if i in seen:
            continue
        stack, comp = [i], []
        seen.add(i)
        while stack:
            j = stack.pop()
            comp.append(j)
            xj, yj, _ = pts[j]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for k in idx.get((xj // tol + dx, yj // tol + dy), ()):
                        if k in seen:
                            continue
                        xk, yk, _ = pts[k]
                        if abs(xk - xj) <= tol and abs(yk - yj) <= tol:
                            seen.add(k)
                            stack.append(k)
        xs = [pts[j][0] for j in comp]
        ys = [pts[j][1] for j in comp]
        out.append((sum(xs) / len(xs), sum(ys) / len(ys), len(comp)))
    return out


def do_s4():
    im = render(7)
    px = im.load()
    print("# Fig S4 (SI p.8) — 600 dpi 픽셀 판독")
    table = []
    for bg, (lab, xv, yv) in zip(S4_BG, S4_META):
        box = tuple(int(v * S) for v in bg)
        fr = find_frame(px, box)
        if not fr:
            print(lab, "frame fail")
            continue
        xt = find_ticks(px, fr, box, "x")
        yt = find_ticks(px, fr, box, "y")
        print("=" * 72)
        print(f"{lab}: frame {[round(v,1) for v in fr]}  ticks x{len(xt)} y{len(yt)}")
        if len(xt) != len(xv) or len(yt) != len(yv):
            print(f"  !! tick 개수 불일치 x{len(xt)}/{len(xv)} y{len(yt)}/{len(yv)}")
            print("   xt", [round(t, 1) for t in xt])
            print("   yt", [round(t, 1) for t in yt])
            continue
        ax, bx, rx = fit(xt, xv)
        ay, by, ry = fit(list(reversed(yt)), yv)
        print(f"  x-cal resid {rx:.4g} (단위 {abs(1/ax):.4g}/px)")
        print(f"  y-cal resid {ry:.4g}")
        ink = colored(px, fr)
        # 범례 마커 제거: 프레임 왼쪽 위 1/3 x 상단 15 % 영역
        ink = [p for p in ink
               if not (p[0] < fr[0] + 0.35 * (fr[2] - fr[0])
                       and p[1] < fr[1] + 0.15 * (fr[3] - fr[1]))]
        if not ink:
            print("  ink 없음")
            continue
        ymax = max(p[1] for p in ink)
        bot = [p for p in ink if p[1] >= ymax - 3]
        zb = ax * (sum(p[0] for p in bot) / len(bot)) + bx
        cl = [c for c in cluster(ink) if c[2] >= 10]
        data = sorted((ax * x + bx, ay * y + by, n) for x, y, n in cl)
        print(f"  ink {len(ink)}px, 병합 마커 {len(data)}")
        print(f"  Z' 범위 {data[0][0]:.5g} .. {data[-1][0]:.5g}")
        print(f"  최저 -Z''(픽셀 최하단) : Z' = {zb:.5g}  (-Z'' = {ay*ymax+by:.4g})")
        near = sorted(data, key=lambda p: p[1])[:6]
        print("  덩어리 하위 6 :", [(round(a, 4), round(b, 4)) for a, b, _ in near])
        table.append((lab, zb))
    print("\n# 요약 (최저 -Z'' 점의 Z' = R_total 근사)")
    for lab, r in table:
        print(f"  {lab:12s} {r:10.4g} ohm")


def do_s5():
    """Fig S5 는 래스터 이미지."""
    im = render(8)
    px = im.load()
    W, H = im.size
    print("# Fig S5 (SI p.9) 600 dpi", im.size)
    # 그림 영역만: PDF 상 이미지 배치 rect
    pg = fitz.open(PDF)[8]
    for b in pg.get_image_info():
        print("  image bbox", [round(v, 1) for v in b["bbox"]], b["width"], b["height"])


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "s4"
    {"s4": do_s4, "s5": do_s5}[what]()
