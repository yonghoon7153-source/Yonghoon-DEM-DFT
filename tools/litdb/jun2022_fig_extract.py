#!/usr/bin/env python3
"""jun2022 (JMCA 2022, 10, 7888) 본문 그림 실물 검증 — Fig 5 / Fig 3a 마커 좌표 복원.

왜 이 스크립트가 있나
---------------------
digest `litdb/papers/jun2022_argyrodite_ion_cage_size_descriptor.md` 는 2026-07-28 에
Table 1/2 수치와 그림 *설명*을 기록했지만, **그림 위에 실제로 몇 점이 찍혔는지**는 세지 않았다.
2026-08-04 본문(8 pp) 실물 독립 검증에서 그것을 세어 보니 Table 1 의 18배열 중 2개가
Fig 5 에 없었다(§20-N1). 이 스크립트는 그 판정을 재현 가능하게 남긴 것이다.

방법
----
- PyMuPDF 로 페이지를 고배율 렌더 → 순수 파이썬 연결성분(numpy 불필요, 이 머신에 numpy 없음).
- 축 눈금(검은 tick)을 검출해 픽셀→데이터 좌표 보정.
- Fig 5: 파란 마름모 마커만 검출(단일 마커 ≈ 440 px @6×; 그보다 큰 성분은 겹친 마커).
- Fig 3a: 축 보정 검증용. Cl 0 % 곡선의 1200 K 점과 300 K 외삽점 두 점으로
  기울기 → Ea 를 역산해 인쇄값(452 meV)과 대조한다.

사용
----
    python tools/litdb/jun2022_fig_extract.py <pdf>            # 기본: Fig 5
    python tools/litdb/jun2022_fig_extract.py <pdf> --fig3a    # Fig 3a 축 검산

PDF 는 litdb/inbox/ (gitignore) 에 있으므로 경로를 인자로 받는다.
"""
from __future__ import annotations

import io
import sys
from collections import deque

import fitz  # PyMuPDF

# Windows 기본 콘솔 코드페이지(cp949)는 ≈·⛔ 를 못 찍는다 → UTF-8 로 감싼다.
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── Table 1 실물 전사 (2026-08-04, PDF p.4에서 직접 읽음) ──────────────────────
#    (원소, X⁻@4c 배열, STD(Å), Ea(meV), σ^0.8(mS/cm))
#    I 50 %(P2mm) Ea 는 인쇄가 "ᵇ27" — digest §14-D3 판정에 따라 227 로 둔다.
TABLE1 = [
    ("Cl", "0%",        0.2391, 452, 3.3e-3),
    ("Cl", "25%",       0.1034, 193, 9.1),
    ("Cl", "50%P2122",  0.0638, 160, 23.3),
    ("Cl", "50%P2mm",   0.0931, 151, 37.1),
    ("Cl", "75%",       0.0826, 184, 12.1),
    ("Cl", "100%",      0.1336, 339, 0.12),
    ("Br", "0%",        0.2861, 557, 9.8e-5),
    ("Br", "25%",       0.1356, 219, 3.2),
    ("Br", "50%P2122",  0.1166, 194, 8.5),
    ("Br", "50%P2mm",   0.1489, 196, 10.5),
    ("Br", "75%",       0.1046, 188, 10.4),
    ("Br", "100%",      0.2089, 401, 1.7e-2),
    ("I",  "0%",        0.3479, 695, 6.9e-7),
    ("I",  "25%",       0.2265, 255, 1.0),
    ("I",  "50%P2122",  0.2118, 202, 6.1),
    ("I",  "50%P2mm",   0.1676, 227, 3.4),
    ("I",  "75%",       0.2142, 221, 3.4),
    ("I",  "100%",      0.3285, 531, 2.6e-4),
]

FIG5_PAGE, FIG5_CLIP = 6, (54, 50, 281, 247)   # p.7 좌상단
FIG3_PAGE, FIG3_CLIP = 4, (64, 50, 222, 184)   # p.5 패널 (a)


# ── 공통 유틸 ────────────────────────────────────────────────────────────────
def render(pdf, page_idx, clip, zoom):
    doc = fitz.open(pdf)
    pix = doc[page_idx].get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=fitz.Rect(*clip))
    return pix.samples, pix.width, pix.height, pix.n


def components(mask, W, H, min_size):
    """8-이웃 연결성분. mask 는 bytearray(W*H)."""
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
            out.append((len(pts),
                        sum(p % W for p in pts) / len(pts),
                        sum(p // W for p in pts) / len(pts)))
    return out


def group(vals, tol):
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


# ── Fig 5 ───────────────────────────────────────────────────────────────────
def fig5(pdf, zoom=6):
    s, W, H, n = render(pdf, FIG5_PAGE, FIG5_CLIP, zoom)

    def at(x, y):
        i = (y * W + x) * n
        return s[i], s[i + 1], s[i + 2]

    blue = bytearray(W * H)
    dark = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            r, g, b = at(x, y)
            if b > 130 and b - r > 60 and b - g > 40:
                blue[y * W + x] = 1
            if r < 90 and g < 90 and b < 90:
                dark[y * W + x] = 1

    # 축 프레임과 눈금
    vert = [x for x in range(W) if sum(dark[y * W + x] for y in range(H)) > H * 0.45]
    horz = [y for y in range(H) if sum(dark[y * W + x] for x in range(W)) > W * 0.45]
    ax_x, ax_y = vert[0], horz[0]
    xt = group([x for x in range(W)
                if sum(dark[y * W + x] for y in range(ax_y + 3, ax_y + 26)) >= 15], 3)
    if len(xt) != 7:
        raise SystemExit(f"x눈금 7개(0.05..0.35)를 못 찾음: {xt}")
    x0, x1 = xt[0], xt[-1]
    sx = (x1 - x0) / 0.30                       # px per unit STD

    comps = components(blue, W, H, min_size=40)
    unit = sorted(c[0] for c in comps)[len(comps) // 2]   # 단일 마커 크기(중앙값)

    # y 보정: Table 1 에서 확실히 식별되는 두 점으로 잡는다
    #   Cl 50 %(P2122) = (0.0638, 23.3)  /  Cl 0 % = (0.2391, 0.0033)
    def near(std):
        px = x0 + (std - 0.05) * sx
        return min(comps, key=lambda c: abs(c[1] - px))

    a, b = near(0.0638), near(0.2391)
    sy = (b[2] - a[2]) / (23.3 - 0.0033)        # px per mS/cm (아래로 갈수록 σ↓)
    y_zero = b[2] + 0.0033 * sy

    def DX(px):
        return 0.05 + (px - x0) / sx

    def DY(py):
        return (y_zero - py) / sy

    frame_top = min(y for y in range(H) if any(dark[y * W + x] for x in vert[:3]))
    top_sigma = DY(frame_top)   # y축이 실제로 담을 수 있는 σ 상한

    print(f"[Fig 5] 검출 성분 {len(comps)}개 (단일 마커 ≈ {unit} px)")
    print(f"        y축 상한 = {top_sigma:.2f} mS/cm")
    print(f"{'STD':>8} {'sigma':>8} {'중첩':>5}")
    pts = []
    for sz, px, py in sorted(comps, key=lambda c: c[1]):
        std, sig = DX(px), DY(py)
        pts.append((std, sig))
        print(f"{std:8.4f} {sig:8.2f} {sz/unit:5.1f}x")

    print("\n[Table 1 18행 ↔ Fig 5 대조]")
    missing = []
    for el, cfg, std, _ea, sig in TABLE1:
        hit = [p for p in pts if abs(p[0] - std) < 0.004 and abs(p[1] - sig) < 1.2]
        tag = "있음" if hit else "⛔ 없음"
        if not hit:
            reason = "축 상한 초과" if sig > top_sigma else "축 안인데 마커 없음"
            missing.append((el, cfg, std, sig, reason))
            tag += f" ({reason})"
        print(f"  {el:2} {cfg:10} STD={std:.4f} σ={sig:<9.4g} {tag}")
    if missing:
        print(f"\n  ⛔ 그림에 없는 배열 {len(missing)}개:")
        for el, cfg, std, sig, why in missing:
            print(f"     {el} {cfg}  (STD {std}, σ {sig} mS/cm) — {why}")


# ── Fig 3a (축 검산) ─────────────────────────────────────────────────────────
def fig3a(pdf, zoom=16):
    """Cl 0 % 곡선의 1200 K 점과 300 K 외삽점으로 Ea 를 역산 → 인쇄값 452 meV 와 대조."""
    s, W, H, n = render(pdf, FIG3_PAGE, FIG3_CLIP, zoom)

    def dk(x, y):
        i = (y * W + x) * n
        return s[i] < 100 and s[i + 1] < 100 and s[i + 2] < 100

    colsum = [sum(dk(x, y) for y in range(0, H, 2)) for x in range(W)]
    rowsum = [sum(dk(x, y) for x in range(0, W, 2)) for y in range(H)]
    vt = [x for x in range(W) if colsum[x] > H * 0.30]
    hz = [y for y in range(H) if rowsum[y] > W * 0.30]
    left, bottom = vt[0], hz[-1]

    yt = group([y for y in range(400, bottom)
                if sum(dk(x, y) for x in range(left - 45, left - 3)) >= 12], 5)
    xt = group([x for x in range(left, W)
                if sum(dk(x, y) for y in range(bottom + 4, bottom + 47)) >= 12], 5)
    # yt = 10^-4 .. 10^-11 (8개), xt = 1.0 .. 3.5 (6개)
    dec = (yt[-1] - yt[0]) / (len(yt) - 1)
    per_half = (xt[-1] - xt[0]) / (len(xt) - 1)

    def LOGD(py):
        return -4.0 - (py - yt[0]) / dec

    def INVT(px):
        return 1.0 + (px - xt[0]) / per_half * 0.5

    print(f"[Fig 3a] y눈금 {len(yt)}개 / x눈금 {len(xt)}개 검출 → 보정 OK")
    print(f"         10^-4 at py={yt[0]:.0f}, 한 decade = {dec:.1f} px")
    print(f"         1000/T=1.0 at px={xt[0]:.0f}, 0.5 단위 = {per_half:.1f} px")
    print("\n  ※ 마커 좌표는 점선과 겹쳐 자동분리가 어렵다. 아래 두 점은 육안 판독값이며,")
    print("     그 두 점으로 계산한 Ea 를 인쇄값과 대조하는 것이 이 함수의 목적이다.")
    x_hi, logd_hi = 0.816, -4.24     # 1200 K 부근 측정점
    x_lo, logd_lo = 3.333, -9.94     # 300 K 외삽점
    slope = (logd_lo - logd_hi) / (x_lo - x_hi)
    ea = 2.302585 * 8.617333e-5 * 1000.0 * (-slope)
    print(f"\n  Cl 0 %: 기울기 {slope:+.3f} /(1000/T) → Ea = {ea*1000:.0f} meV  (인쇄 452 meV)")
    # 300 K 외삽 D 를 Nernst-Einstein 으로 σ 환산 (24 Li / a≈10 Å 셀)
    d300 = 10 ** logd_lo
    rho = 24 / 1e-21 / 6.02214e23          # mol/cm^3
    sigma = rho * 96485.0 ** 2 / (8.314 * 300.0) * d300     # S/cm
    print(f"  Cl 0 %: D(300 K) = {d300:.2e} cm^2/s → σ(χc=1) = {sigma*1e3:.2e} mS/cm")
    print(f"          Table 1 σ^0.8 = 3.3e-3 → /0.8^7.14 = {3.3e-3/0.8**7.14:.2e} mS/cm")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if "--fig3a" in sys.argv:
        fig3a(sys.argv[1])
    else:
        fig5(sys.argv[1])
