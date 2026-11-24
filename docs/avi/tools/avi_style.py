#!/usr/bin/env python3
"""Reference-matched style constants (measured, see reference_analysis.md)."""
import os

import numpy as np
from PIL import ImageFont

W, H = 1920, 1080
FPS = 30

# colours measured on the reference (RGB)
BG = (247, 237, 228)            # cream background #F7EDE4
INK = (26, 20, 16)              # warm black lines / text
INDIGO = (78, 68, 226)          # single accent
LAV = (214, 200, 222)           # dimmed indigo (indigo ~20-25 % on cream)
LAV_FILL = (232, 224, 246)      # light lavender fill / highlighter band
INK_DIM = (190, 178, 172)       # dimmed ink (~25 %)
GREY = (138, 126, 120)          # mid-grey labels (~50 %)
SRC_GREY = (150, 139, 132)      # source lines
WHITE = (255, 255, 255)
CAP_BOX_ALPHA = 0.64            # caption box = black at 64 % (measured 64-66 %)

PALETTE = {
    "bg": BG, "ink": INK, "indigo": INDIGO, "lav": LAV, "lavfill": LAV_FILL,
    "inkdim": INK_DIM, "grey": GREY, "src": SRC_GREY, "white": WHITE,
}
# dimmed version of each colour (used by the 'dim' animation)
DIM_OF = {INK: INK_DIM, INDIGO: LAV, GREY: (205, 195, 188), WHITE: (250, 246, 242),
          LAV_FILL: (240, 234, 240), LAV: (228, 218, 228), SRC_GREY: (200, 190, 184)}


def col(c):
    if c is None:
        return None
    if isinstance(c, str):
        if c.startswith("#"):
            return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
        return PALETTE[c]
    return tuple(c)


def dim_col(c):
    c = col(c)
    if c is None:
        return None
    if c in DIM_OF:
        return DIM_OF[c]
    # generic: mix 75 % toward background
    return tuple(int(round(0.25 * a + 0.75 * b)) for a, b in zip(c, BG))


HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.environ.get("AVI_FONT_DIR") or os.path.join(os.path.dirname(HERE), "fonts")   # 리포에는 글꼴이 없다 → AVI_FONT_DIR (Pretendard · SIL OFL)
FONTS = {
    "regular": os.path.join(FONT_DIR, "Pretendard-Regular.otf"),
    "medium": os.path.join(FONT_DIR, "Pretendard-Medium.otf"),
    "semibold": os.path.join(FONT_DIR, "Pretendard-SemiBold.otf"),
    "bold": os.path.join(FONT_DIR, "Pretendard-Bold.otf"),
    "extrabold": os.path.join(FONT_DIR, "Pretendard-ExtraBold.otf"),
    "black": os.path.join(FONT_DIR, "Pretendard-Black.otf"),
}
FALLBACK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
_font_cache = {}


def font(weight="semibold", size=40):
    key = (weight, int(size))
    if key not in _font_cache:
        path = FONTS.get(weight, FONTS["semibold"])
        try:
            _font_cache[key] = ImageFont.truetype(path, int(size))
        except OSError:
            _font_cache[key] = ImageFont.truetype(FALLBACK, int(size), index=1)
    return _font_cache[key]


# caption geometry at 1080p (720p measurement x 1.5)
CAPTION = dict(font="semibold", size=50, box_h=86, pad_x=32, cy=976, radius=0,
               max_chars=22, color=WHITE)

# typical sizes (1080p)
SIZE = dict(label=28, small=24, source=22, body=34, title=44, big=78, huge=110)


def paper_texture(w=W, h=H, seed=7, std=1.0):
    """Static cream background with a paper-like mottle (std ~1 level),
    mimicking the measured texture (survives a sigma-8 blur at 0.42)."""
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(seed)
    fields = []
    for sigma, wgt in ((1.0, 0.55), (4.0, 0.5), (12.0, 0.6), (30.0, 0.5)):
        f = gaussian_filter(rng.standard_normal((h, w)).astype(np.float32), sigma, mode="wrap")
        f /= f.std() + 1e-9
        fields.append(wgt * f)
    t = np.sum(fields, axis=0)
    t = t / (t.std() + 1e-9) * std
    img = np.empty((h, w, 3), np.float32)
    for k in range(3):
        img[..., k] = BG[k] + t
    return np.clip(img, 0, 255)
