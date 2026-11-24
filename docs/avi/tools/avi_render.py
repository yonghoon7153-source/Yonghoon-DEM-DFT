#!/usr/bin/env python3
"""AVI renderer: scenes.json + timeline -> frames -> ffmpeg (H.264 + AAC).

Elements are rendered once into sprites (shapes 3x supersampled, premultiplied
box downsample; text drawn at 1x by PIL) and composited per frame.  Only frames
whose state signature changes are recomposed; identical frames are re-sent to
ffmpeg as the same bytes (cheap), so long holds cost almost nothing.
"""
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

import avi_style as S
import avi_timeline as T

SS = 3
INF = 1e9


# ------------------------------------------------------------------ easing
def clamp01(x):
    return 0.0 if x <= 0 else (1.0 if x >= 1 else float(x))


def ease_out(p):
    p = clamp01(p)
    return 1 - (1 - p) ** 3


def ease_in_out(p):
    p = clamp01(p)
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


# ------------------------------------------------------------------ sprite helpers
class Sprite:
    __slots__ = ("rgb", "a", "x0", "y0", "smap", "L")

    def __init__(self, rgb, a, x0, y0, smap=None, L=None):
        self.rgb, self.a, self.x0, self.y0, self.smap, self.L = rgb, a, x0, y0, smap, L


def _bbox_pad(x0, y0, x1, y1, pad=6):
    return int(math.floor(x0 - pad)), int(math.floor(y0 - pad)), int(math.ceil(x1 + pad)), int(math.ceil(y1 + pad))


class Canvas:
    """Supersampled drawing canvas for one sprite in canvas coordinates."""

    def __init__(self, x0, y0, x1, y1, ss=SS):
        self.x0, self.y0 = x0, y0
        self.w, self.h = max(1, x1 - x0), max(1, y1 - y0)
        self.ss = ss
        self.img = Image.new("RGBA", (self.w * ss, self.h * ss), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def p(self, x, y):
        return ((x - self.x0) * self.ss, (y - self.y0) * self.ss)

    def s(self, v):
        return v * self.ss

    def finish(self):
        a = np.asarray(self.img, np.float32)
        ss = self.ss
        al = a[..., 3:4] / 255.0
        pm = a[..., :3] * al
        h, w = self.h, self.w
        pm = pm[:h * ss, :w * ss].reshape(h, ss, w, ss, 3).mean(axis=(1, 3))
        al = al[:h * ss, :w * ss].reshape(h, ss, w, ss, 1).mean(axis=(1, 3))
        rgb = np.where(al > 1e-6, pm / np.maximum(al, 1e-6), 0.0).astype(np.float32)
        return rgb, al[..., 0].astype(np.float32)


def text_layer(rgb, a, x0, y0, items):
    """Draw 1x text items onto an existing sprite (premultiplied over)."""
    h, w = a.shape
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    for it in items:
        f = S.font(it.get("weight", "bold"), it["size"])
        d.text((it["x"] - x0, it["y"] - y0), it["text"], font=f, fill=S.col(it["color"]) + (255,),
               anchor=it.get("anchor", "mm"))
    t = np.asarray(img, np.float32)
    ta = t[..., 3] / 255.0
    out_a = ta + a * (1 - ta)
    out_rgb = np.where(out_a[..., None] > 1e-6,
                       (t[..., :3] * ta[..., None] + rgb * (a * (1 - ta))[..., None]) / np.maximum(out_a, 1e-6)[..., None],
                       0.0)
    return out_rgb.astype(np.float32), out_a.astype(np.float32)


def path_smap(points, a, x0, y0, step=1.0):
    """Arc-length parameter (px) of the nearest path point, for draw-on reveals."""
    from scipy.spatial import cKDTree
    pts = np.asarray(points, float)
    seg = np.diff(pts, axis=0)
    seglen = np.hypot(seg[:, 0], seg[:, 1])
    L = float(seglen.sum())
    samples, svals = [], []
    acc = 0.0
    for (p0, d, l) in zip(pts[:-1], seg, seglen):
        n = max(2, int(l / step) + 1)
        for k in range(n):
            u = k / (n - 1)
            samples.append(p0 + d * u)
            svals.append(acc + l * u)
        acc += l
    tree = cKDTree(np.array(samples))
    ys, xs = np.nonzero(a > 0.001)
    smap = np.full(a.shape, np.inf, np.float32)
    if len(xs):
        _, idx = tree.query(np.c_[xs + x0 + 0.5, ys + y0 + 0.5])
        smap[ys, xs] = np.asarray(svals)[idx]
    return smap, L


def dash_segments(points, on, off):
    """Split a polyline into dash segments (list of polylines)."""
    pts = np.asarray(points, float)
    out, cur = [], []
    state_on, left = True, on
    cur = [pts[0]]
    for p0, p1 in zip(pts[:-1], pts[1:]):
        d = p1 - p0
        L = float(np.hypot(*d))
        pos = 0.0
        while pos < L - 1e-9:
            step = min(left, L - pos)
            q = p0 + d * ((pos + step) / L)
            if state_on:
                cur.append(q)
            pos += step
            left -= step
            if left <= 1e-9:
                if state_on and len(cur) >= 2:
                    out.append(cur)
                state_on = not state_on
                left = on if state_on else off
                cur = [q] if state_on else []
    if state_on and len(cur) >= 2:
        out.append(cur)
    return out


def arrow_head(c, tip, frm, size, color):
    tip = np.asarray(tip, float)
    d = tip - np.asarray(frm, float)
    n = d / (np.hypot(*d) + 1e-9)
    perp = np.array([-n[1], n[0]])
    b = tip - n * size
    pts = [tip, b + perp * size * 0.45, b - perp * size * 0.45]
    c.d.polygon([c.p(*q) for q in pts], fill=color + (255,))


# ------------------------------------------------------------------ elements
class Elem:
    default_in = "fade"
    in_dur = 0.3

    def __init__(self, spec):
        self.spec = spec
        self.id = spec["id"]
        self.z = spec.get("z", 0)
        self.pivot = (float(spec.get("x", 0)), float(spec.get("y", 0)))
        self.base_scale = float(spec.get("scale", 1.0))
        self.t_in = 0.0
        self.anim = spec.get("anim", self.default_in)
        self.dur = float(spec.get("dur", self.in_dur))
        self.t_out = INF
        self.out_dur = 0.3
        self.dims = []      # (t, target, dur)
        self.moves = []     # (t, dur, x, y, scale)
        self.spins = []     # (t0, t1, rps)
        self._cache = {}
        self.built = False

    # --- geometry, overridden
    def build(self, dim):
        raise NotImplementedError

    def sprite(self, dim_level, prog=1.0, value=None, angle=0.0):
        key = "n"
        if key not in self._cache:
            self._cache["n"] = self.build(False)
            self._cache["d"] = self.build(True)
        n, d = self._cache["n"], self._cache["d"]
        if dim_level <= 0.001:
            return n
        if dim_level >= 0.999:
            return d
        k = ("mix", round(dim_level, 2))
        if k not in self._cache:
            rgb = n.rgb * (1 - dim_level) + d.rgb * dim_level
            self._cache[k] = Sprite(rgb.astype(np.float32), np.maximum(n.a, d.a), n.x0, n.y0, n.smap, n.L)
        return self._cache[k]

    # --- state at time t
    def state(self, t):
        if t < self.t_in or t >= self.t_out + self.out_dur:
            return None
        p = (t - self.t_in) / max(1e-6, self.dur)
        alpha, scale, prog, dy = 1.0, self.base_scale, 1.0, 0.0
        if self.anim == "fade":
            alpha = ease_out(p)
        elif self.anim == "pop":
            alpha = ease_out(min(1.0, p * 1.8))
            scale *= 0.55 + 0.45 * ease_out(p)
        elif self.anim in ("draw", "grow"):
            prog = ease_in_out(p) if self.anim == "draw" else ease_out(p)
            alpha = 1.0
        elif self.anim == "count":
            prog = ease_out(p)
            alpha = ease_out(min(1.0, p * 3))
        elif self.anim == "slide":
            alpha = ease_out(p)
            dy = 22 * (1 - ease_out(p))
        elif self.anim == "none":
            pass
        if t >= self.t_out:
            alpha *= 1 - ease_out((t - self.t_out) / self.out_dur)
        dim = 0.0
        for (td, target, dd) in self.dims:
            if t >= td:
                q = ease_out((t - td) / dd)
                dim = dim + (target - dim) * q
        x, y = self.pivot
        sc_move = 1.0
        for (tm, dm, mx, my, ms) in self.moves:
            if t >= tm:
                q = ease_in_out((t - tm) / dm)
                x = x + (mx - x) * q
                y = y + (my - y) * q
                sc_move = sc_move + (ms - sc_move) * q
        angle = 0.0
        for (t0, t1, rps) in self.spins:
            if t >= t0:
                tt = min(t, t1) - t0
                angle += 360.0 * rps * tt
        return dict(alpha=alpha, scale=scale * sc_move, prog=prog, dim=dim, x=x, y=y + dy, angle=angle % 360.0, t=t)

    def sig(self, st):
        return (self.id, round(st["alpha"], 3), round(st["scale"], 3), round(st["prog"], 3), round(st["dim"], 2),
                round(st["x"], 1), round(st["y"], 1), round(st["angle"], 0))

    def draw_into(self, frame, st):
        sp = self.sprite(st["dim"], st["prog"], None, st["angle"])
        blit(frame, sp, st, self.pivot)


def scaled_sprite(sp, scale, pivot):
    """Scale a sprite around pivot (canvas coords).  Returns new Sprite."""
    h, w = sp.a.shape
    nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
    pm = np.concatenate([sp.rgb * sp.a[..., None], sp.a[..., None] * 255.0], axis=2)
    img = Image.fromarray(np.clip(pm, 0, 255).astype(np.uint8), "RGBA")
    img = img.resize((nw, nh), Image.BILINEAR)
    arr = np.asarray(img, np.float32)
    a = arr[..., 3] / 255.0
    rgb = np.where(a[..., None] > 1e-4, arr[..., :3] / np.maximum(a[..., None], 1e-4), 0.0)
    px, py = pivot
    x0 = px + (sp.x0 - px) * scale
    y0 = py + (sp.y0 - py) * scale
    return Sprite(rgb.astype(np.float32), a.astype(np.float32), x0, y0)


def blit(frame, sp, st, pivot, alpha_mul=1.0):
    a = sp.a
    if sp.smap is not None and st["prog"] < 0.999:
        lim = st["prog"] * sp.L
        a = a * np.clip((lim - sp.smap) / 1.5 + 1.0, 0.0, 1.0)
    use = Sprite(sp.rgb, a, sp.x0, sp.y0)
    if abs(st["scale"] - 1.0) > 1e-3:
        use = scaled_sprite(use, st["scale"], pivot)
    dx, dy = st["x"] - pivot[0], st["y"] - pivot[1]
    x0 = int(round(use.x0 + dx))
    y0 = int(round(use.y0 + dy))
    h, w = use.a.shape
    H, W = frame.shape[:2]
    fx0, fy0 = max(0, x0), max(0, y0)
    fx1, fy1 = min(W, x0 + w), min(H, y0 + h)
    if fx1 <= fx0 or fy1 <= fy0:
        return
    sx0, sy0 = fx0 - x0, fy0 - y0
    al = use.a[sy0:sy0 + (fy1 - fy0), sx0:sx0 + (fx1 - fx0)] * (st["alpha"] * alpha_mul)
    if al.max() <= 0:
        return
    rgb = use.rgb[sy0:sy0 + (fy1 - fy0), sx0:sx0 + (fx1 - fx0)]
    reg = frame[fy0:fy1, fx0:fx1]
    reg += (rgb - reg) * al[..., None]


def _c(spec, key, dim, default=None):
    c = S.col(spec.get(key, default))
    if c is None:
        return None
    return S.dim_col(c) if dim else c


class Circle(Elem):
    default_in = "pop"

    def build(self, dim):
        s = self.spec
        x, y, r = float(s["x"]), float(s["y"]), float(s["r"])
        sw = float(s.get("sw", 3))
        fill = _c(s, "fill", dim)
        stroke = _c(s, "stroke", dim)
        x0, y0, x1, y1 = _bbox_pad(x - r - sw, y - r - sw, x + r + sw, y + r + sw)
        c = Canvas(x0, y0, x1, y1)
        bb = [c.p(x - r, y - r), c.p(x + r, y + r)]
        if fill:
            c.d.ellipse(bb, fill=fill + (255,))
        if stroke:
            dash = s.get("dash")
            if dash:
                on, off = (dash if isinstance(dash, list) else (10, 8))
                circ = 2 * math.pi * r
                n = max(4, int(circ / (on + off)))
                for k in range(n):
                    a0 = 360.0 * k / n - 90
                    a1 = a0 + 360.0 / n * on / (on + off)
                    c.d.arc(bb, a0, a1, fill=stroke + (255,), width=int(round(c.s(sw))))
            else:
                c.d.ellipse(bb, outline=stroke + (255,), width=int(round(c.s(sw))))
        rgb, a = c.finish()
        items = []
        if s.get("label"):
            lc = _c(s, "label_color", dim, "white" if fill and fill != S.dim_col(S.WHITE) else "ink")
            ly = y if not s.get("sublabel") else y - s.get("label_size", 30) * 0.32
            items.append(dict(text=s["label"], x=x, y=ly, size=s.get("label_size", 30),
                              weight=s.get("label_weight", "bold"), color=lc))
            if s.get("sublabel"):
                items.append(dict(text=s["sublabel"], x=x, y=y + s.get("label_size", 30) * 0.55,
                                  size=s.get("sublabel_size", int(s.get("label_size", 30) * 0.6)),
                                  weight="bold", color=lc))
        if items:
            rgb, a = text_layer(rgb, a, x0, y0, items)
        smap = L = None
        if self.anim == "draw":
            ang = np.linspace(-math.pi / 2, 1.5 * math.pi, 361)
            pts = np.c_[x + r * np.cos(ang), y + r * np.sin(ang)]
            smap, L = path_smap(pts, a, x0, y0)
        return Sprite(rgb, a, x0, y0, smap, L)


class Dots(Elem):
    """Many small circles.  points=[[x,y,r],...]; optional 'to' targets for a move."""
    default_in = "pop"
    in_dur = 0.25

    def __init__(self, spec):
        super().__init__(spec)
        self.dot_anim = self.anim          # per-dot animation
        self.anim = "none"                 # group itself does not pop/scale
        self.pts = [list(map(float, p)) for p in spec["points"]]
        self.to = spec.get("to")
        self.stagger = float(spec.get("stagger", 0.03))
        self.move_t = None
        self.move_dur = float(spec.get("move_dur", 0.9))
        self.move_stagger = float(spec.get("move_stagger", 0.02))
        self.dot_cache = {}

    def _dot(self, r, dim):
        key = (round(r, 2), dim)
        if key not in self.dot_cache:
            fill = _c(self.spec, "fill", dim, "indigo")
            stroke = _c(self.spec, "stroke", dim)
            sw = float(self.spec.get("sw", 2))
            x0, y0, x1, y1 = _bbox_pad(-r - sw, -r - sw, r + sw, r + sw, pad=3)
            c = Canvas(x0, y0, x1, y1)
            bb = [c.p(-r, -r), c.p(r, r)]
            if fill:
                c.d.ellipse(bb, fill=fill + (255,))
            if stroke:
                c.d.ellipse(bb, outline=stroke + (255,), width=int(round(c.s(sw))))
            rgb, a = c.finish()
            self.dot_cache[key] = Sprite(rgb, a, x0, y0)
        return self.dot_cache[key]

    def dot_states(self, st):
        t = st["t"]
        out = []
        n = len(self.pts)
        for i, (x, y, r) in enumerate(self.pts):
            ti = self.t_in + i * self.stagger
            if t < ti:
                continue
            p = (t - ti) / self.dur
            if self.dot_anim == "pop":
                al = ease_out(min(1, p * 1.8))
                sc = 0.4 + 0.6 * ease_out(p)
            else:
                al = ease_out(p)
                sc = 1.0
            if self.to is not None and self.move_t is not None and t >= self.move_t + i * self.move_stagger:
                q = ease_in_out((t - self.move_t - i * self.move_stagger) / self.move_dur)
                tx, ty = self.to[i][0], self.to[i][1]
                x, y = x + (tx - x) * q, y + (ty - y) * q
            out.append((i, x, y, r, al, sc))
        return out

    def sig(self, st):
        ds = self.dot_states(st)
        anim = any(al < 0.999 or abs(sc - 1) > 1e-3 for (_, _, _, _, al, sc) in ds)
        moving = (self.to is not None and self.move_t is not None and
                  self.move_t <= st["t"] <= self.move_t + self.move_dur + len(self.pts) * self.move_stagger)
        key = (self.id, len(ds), round(st["alpha"], 3), round(st["dim"], 2), round(st["x"], 1), round(st["y"], 1),
               round(st["scale"], 3))
        if anim or moving:
            return key + (round(st["t"], 3),)
        return key + (moving,)

    def draw_into(self, frame, st):
        dx, dy = st["x"] - self.pivot[0], st["y"] - self.pivot[1]
        for (i, x, y, r, al, sc) in self.dot_states(st):
            sp = self._dot(r * sc * st["scale"], st["dim"] > 0.5)
            px = self.pivot[0] + (x - self.pivot[0]) * st["scale"] + dx
            py = self.pivot[1] + (y - self.pivot[1]) * st["scale"] + dy
            blit(frame, sp, dict(st, scale=1.0, x=px, y=py, prog=1.0), (0, 0), alpha_mul=al)


class Text(Elem):
    default_in = "fade"

    def build(self, dim):
        s = self.spec
        size = s.get("size", S.SIZE["label"])
        f = S.font(s.get("weight", "bold"), size)
        color = _c(s, "color", dim, "ink")
        lines = str(s["text"]).split("\n")
        gap = s.get("line_gap", 1.32)
        lh = size * gap
        boxes = [f.getbbox(l, anchor="lm") for l in lines]
        widths = [b[2] - b[0] for b in boxes]
        wmax = max(widths) if widths else 0
        x, y = float(s["x"]), float(s["y"])
        align = s.get("align", "center")
        n = len(lines)
        ys = [y + (i - (n - 1) / 2) * lh for i in range(n)]
        if s.get("valign") == "top":
            ys = [y + size * 0.6 + i * lh for i in range(n)]
        x0 = x - (wmax / 2 if align == "center" else (wmax if align == "right" else 0)) - 12
        y0 = ys[0] - size
        x1 = x0 + wmax + 24
        y1 = ys[-1] + size
        X0, Y0, X1, Y1 = _bbox_pad(x0, y0, x1, y1, pad=10)
        h, w = Y1 - Y0, X1 - X0
        rgb = np.zeros((h, w, 3), np.float32)
        a = np.zeros((h, w), np.float32)
        if s.get("highlight"):
            c = Canvas(X0, Y0, X1, Y1)
            for l, yy, ww in zip(lines, ys, widths):
                lx = x - ww / 2 if align == "center" else (x - ww if align == "right" else x)
                c.d.rectangle([c.p(lx - 6, yy + size * 0.02), c.p(lx + ww + 6, yy + size * 0.52)],
                              fill=_c(s, "highlight_color", dim, "lavfill") + (255,))
            rgb, a = c.finish()
        if s.get("box"):
            c = Canvas(X0, Y0, X1, Y1)
            bx = s["box"]
            padx, pady = bx.get("pad_x", 14), bx.get("pad_y", 8)
            bx0 = x - wmax / 2 - padx if align == "center" else (x - wmax - padx if align == "right" else x - padx)
            rect = [c.p(bx0, ys[0] - size * 0.62 - pady), c.p(bx0 + wmax + 2 * padx, ys[-1] + size * 0.62 + pady)]
            fill = S.col(bx.get("fill")) if bx.get("fill") else None
            if fill and dim:
                fill = S.dim_col(fill)
            stroke = S.col(bx.get("stroke", "ink"))
            if dim:
                stroke = S.dim_col(stroke)
            c.d.rounded_rectangle(rect, radius=c.s(bx.get("radius", 3)), fill=(fill + (255,)) if fill else None,
                                  outline=stroke + (255,) if stroke else None, width=int(c.s(bx.get("sw", 2))))
            rgb2, a2 = c.finish()
            rgb, a = rgb2, a2
        items = []
        for l, yy, ww in zip(lines, ys, widths):
            if align == "center":
                items.append(dict(text=l, x=x, y=yy, size=size, weight=s.get("weight", "bold"), color=color, anchor="mm"))
            elif align == "right":
                items.append(dict(text=l, x=x, y=yy, size=size, weight=s.get("weight", "bold"), color=color, anchor="rm"))
            else:
                items.append(dict(text=l, x=x, y=yy, size=size, weight=s.get("weight", "bold"), color=color, anchor="lm"))
        rgb, a = text_layer(rgb, a, X0, Y0, items)
        return Sprite(rgb, a, X0, Y0)


class Number(Elem):
    """Big number with small unit; anim 'count' counts from 'start' to 'value'."""
    default_in = "count"
    in_dur = 0.9

    def fmt(self, v):
        dec = int(self.spec.get("decimals", 0))
        return f"{v:.{dec}f}"

    def sprite(self, dim_level, prog=1.0, value=None, angle=0.0):
        s = self.spec
        v0, v1 = float(s.get("start", 0.0)), float(s["value"])
        v = v0 + (v1 - v0) * prog
        txt = self.fmt(v) if prog < 0.999 else (s.get("display") or self.fmt(v1))
        dimb = dim_level > 0.5
        key = (txt, dimb, round(prog, 2) if self.anim == "count" and s.get("color_count", True) else 1)
        if key not in self._cache:
            size = s.get("size", S.SIZE["big"])
            usize = s.get("unit_size", int(size * 0.42))
            f = S.font(s.get("weight", "bold"), size)
            fu = S.font(s.get("unit_weight", "bold"), usize)
            c1 = S.col(s.get("color", "indigo"))
            if self.anim == "count" and s.get("color_count", True) and prog < 0.999:
                lav = S.dim_col(c1)
                c1 = tuple(int(round(lav[k] + (c1[k] - lav[k]) * prog)) for k in range(3))
            if dimb:
                c1 = S.dim_col(c1)
            cu = S.col(s.get("unit_color", s.get("color", "indigo")))
            if dimb:
                cu = S.dim_col(cu)
            unit = s.get("unit", "")
            prefix = s.get("prefix", "")
            wp = fu.getlength(prefix) if prefix else 0
            gapp = size * 0.08 if prefix else 0
            wn = f.getlength(txt)
            wu = fu.getlength(unit) if unit else 0
            gapu = size * 0.06 if unit else 0
            tw = wp + gapp + wn + gapu + wu
            x, y = float(s["x"]), float(s["y"])
            align = s.get("align", "center")
            lx = x - tw / 2 if align == "center" else (x - tw if align == "right" else x)
            X0, Y0, X1, Y1 = _bbox_pad(lx, y - size * 0.9, lx + tw, y + size * 0.35, pad=10)
            rgb = np.zeros((Y1 - Y0, X1 - X0, 3), np.float32)
            a = np.zeros((Y1 - Y0, X1 - X0), np.float32)
            items = []
            if prefix:
                items.append(dict(text=prefix, x=lx, y=y, size=usize, weight=s.get("unit_weight", "bold"),
                                  color=cu, anchor="ls"))
            nx = lx + wp + gapp
            items.append(dict(text=txt, x=nx, y=y, size=size, weight=s.get("weight", "bold"), color=c1, anchor="ls"))
            if unit:
                items.append(dict(text=unit, x=nx + wn + gapu, y=y, size=usize, weight=s.get("unit_weight", "bold"),
                                  color=cu, anchor="ls"))
            rgb, a = text_layer(rgb, a, X0, Y0, items)
            self._cache[key] = Sprite(rgb, a, X0, Y0)
        return self._cache[key]


class Line(Elem):
    default_in = "draw"
    in_dur = 0.6

    def build(self, dim):
        s = self.spec
        pts = [tuple(map(float, p)) for p in s["points"]]
        sw = float(s.get("sw", 3))
        color = _c(s, "color", dim, "ink")
        arr = np.asarray(pts)
        ah = float(s.get("arrow_size", 18)) if s.get("arrow") else 0
        X0, Y0, X1, Y1 = _bbox_pad(arr[:, 0].min() - sw - ah, arr[:, 1].min() - sw - ah,
                                   arr[:, 0].max() + sw + ah, arr[:, 1].max() + sw + ah)
        c = Canvas(X0, Y0, X1, Y1)
        dash = s.get("dash")
        seglist = dash_segments(pts, *(dash if isinstance(dash, list) else (12, 9))) if dash else [pts]
        for seg in seglist:
            c.d.line([c.p(*q) for q in seg], fill=color + (255,), width=max(1, int(round(c.s(sw)))), joint="curve")
            if s.get("round", True):
                rr = c.s(sw) / 2
                for q in (seg[0], seg[-1]):
                    qx, qy = c.p(*q)
                    c.d.ellipse([qx - rr, qy - rr, qx + rr, qy + rr], fill=color + (255,))
        if s.get("arrow") in ("end", "both"):
            arrow_head(c, pts[-1], pts[-2], ah, color)
        if s.get("arrow") in ("start", "both"):
            arrow_head(c, pts[0], pts[1], ah, color)
        rgb, a = c.finish()
        smap, L = path_smap(pts, a, X0, Y0) if self.anim == "draw" else (None, None)
        return Sprite(rgb, a, X0, Y0, smap, L)


class Area(Elem):
    default_in = "fade"

    def build(self, dim):
        s = self.spec
        pts = [tuple(map(float, p)) for p in s["points"]]
        arr = np.asarray(pts)
        X0, Y0, X1, Y1 = _bbox_pad(arr[:, 0].min(), arr[:, 1].min(), arr[:, 0].max(), arr[:, 1].max())
        c = Canvas(X0, Y0, X1, Y1)
        c.d.polygon([c.p(*q) for q in pts], fill=_c(s, "fill", dim, "lavfill") + (255,))
        rgb, a = c.finish()
        a = a * float(s.get("opacity", 1.0))
        return Sprite(rgb, a, X0, Y0)


class Rect(Elem):
    default_in = "fade"

    def build(self, dim):
        s = self.spec
        x, y, w, h = float(s["x"]), float(s["y"]), float(s["w"]), float(s["h"])
        sw = float(s.get("sw", 2.5))
        X0, Y0, X1, Y1 = _bbox_pad(x - w / 2 - sw, y - h / 2 - sw, x + w / 2 + sw, y + h / 2 + sw)
        c = Canvas(X0, Y0, X1, Y1)
        fill = _c(s, "fill", dim)
        stroke = _c(s, "stroke", dim)
        rect = [c.p(x - w / 2, y - h / 2), c.p(x + w / 2, y + h / 2)]
        rad = c.s(s.get("radius", 0))
        if s.get("dash") and stroke:
            if fill:
                c.d.rounded_rectangle(rect, radius=rad, fill=fill + (255,))
            pts = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)]
            dash = s["dash"] if isinstance(s["dash"], list) else (10, 7)
            for seg in dash_segments(pts, *dash):
                c.d.line([c.p(*q) for q in seg], fill=stroke + (255,), width=max(1, int(round(c.s(sw)))))
        else:
            c.d.rounded_rectangle(rect, radius=rad, fill=(fill + (255,)) if fill else None,
                                  outline=(stroke + (255,)) if stroke else None,
                                  width=max(1, int(round(c.s(sw)))) if stroke else 0)
        rgb, a = c.finish()
        if s.get("label"):
            lc = _c(s, "label_color", dim, "ink")
            rgb, a = text_layer(rgb, a, X0, Y0, [dict(text=s["label"], x=x, y=y + s.get("label_dy", 0),
                                                      size=s.get("label_size", 28), weight=s.get("label_weight", "bold"),
                                                      color=lc)])
        smap = L = None
        if self.anim == "grow":
            if s.get("grow_dir", "x") == "x":
                pts = [(x - w / 2, y), (x + w / 2, y)]
            else:
                pts = [(x, y + h / 2), (x, y - h / 2)]
            smap, L = path_smap(pts, a, X0, Y0)
        return Sprite(rgb, a, X0, Y0, smap, L)


class Person(Elem):
    default_in = "fade"

    def build(self, dim):
        s = self.spec
        x, y, sz = float(s["x"]), float(s["y"]), float(s.get("size", 60))
        color = _c(s, "color", dim, "ink")
        X0, Y0, X1, Y1 = _bbox_pad(x - sz * 0.5, y - sz * 0.75, x + sz * 0.5, y + sz * 0.75)
        c = Canvas(X0, Y0, X1, Y1)
        hr = sz * 0.22
        c.d.ellipse([c.p(x - hr, y - sz * 0.7), c.p(x + hr, y - sz * 0.7 + 2 * hr)], fill=color + (255,))
        c.d.rectangle([c.p(x - sz * 0.32, y - sz * 0.18), c.p(x + sz * 0.32, y + sz * 0.42)], fill=color + (255,))
        rgb, a = c.finish()
        return Sprite(rgb, a, X0, Y0)


class Mixer(Elem):
    """Vessel outline + rotating chopper blades (spin keyframes)."""
    default_in = "fade"

    def sprite(self, dim_level, prog=1.0, value=None, angle=0.0):
        key = (round(angle / 4) * 4 % 360, dim_level > 0.5)
        if key not in self._cache:
            s = self.spec
            x, y, r = float(s["x"]), float(s["y"]), float(s["r"])
            color = S.col(s.get("color", "ink"))
            bcol = S.col(s.get("blade_color", "indigo"))
            if key[1]:
                color, bcol = S.dim_col(color), S.dim_col(bcol)
            sw = float(s.get("sw", 3))
            X0, Y0, X1, Y1 = _bbox_pad(x - r - sw, y - r - sw, x + r + sw, y + r + sw)
            c = Canvas(X0, Y0, X1, Y1)
            c.d.ellipse([c.p(x - r, y - r), c.p(x + r, y + r)], outline=color + (255,), width=int(c.s(sw)))
            nb = int(s.get("blades", 4))
            br = r * float(s.get("blade_len", 0.42))
            for k in range(nb):
                th = math.radians(key[0] + 360.0 * k / nb)
                c.d.line([c.p(x, y), c.p(x + br * math.cos(th), y + br * math.sin(th))], fill=bcol + (255,),
                         width=int(c.s(sw * 1.6)))
            hub = r * 0.05
            c.d.ellipse([c.p(x - hub, y - hub), c.p(x + hub, y + hub)], fill=bcol + (255,))
            rgb, a = c.finish()
            self._cache[key] = Sprite(rgb, a, X0, Y0)
        return self._cache[key]


class Group(Elem):
    """Static composite of primitives drawn into one sprite (e.g. AFM cantilever)."""
    default_in = "fade"

    def build(self, dim):
        s = self.spec
        bb = s["bbox"]
        X0, Y0, X1, Y1 = _bbox_pad(*bb)
        c = Canvas(X0, Y0, X1, Y1)
        texts = []
        for p in s["parts"]:
            k = p["k"]
            colr = S.col(p.get("color", "ink"))
            if dim:
                colr = S.dim_col(colr)
            if k == "line":
                c.d.line([c.p(*q) for q in p["points"]], fill=colr + (255,), width=int(c.s(p.get("sw", 3))),
                         joint="curve")
            elif k == "circle":
                x, y, r = p["x"], p["y"], p["r"]
                fill = S.col(p.get("fill")) if p.get("fill") else None
                if fill and dim:
                    fill = S.dim_col(fill)
                c.d.ellipse([c.p(x - r, y - r), c.p(x + r, y + r)], fill=(fill + (255,)) if fill else None,
                            outline=colr + (255,) if p.get("stroke", True) else None,
                            width=int(c.s(p.get("sw", 2.5))))
            elif k == "rect":
                x, y, w, h = p["x"], p["y"], p["w"], p["h"]
                fill = S.col(p.get("fill")) if p.get("fill") else None
                if fill and dim:
                    fill = S.dim_col(fill)
                c.d.rectangle([c.p(x - w / 2, y - h / 2), c.p(x + w / 2, y + h / 2)],
                              fill=(fill + (255,)) if fill else None,
                              outline=colr + (255,) if p.get("stroke", True) else None, width=int(c.s(p.get("sw", 2.5))))
            elif k == "poly":
                fill = S.col(p.get("fill", p.get("color", "ink")))
                if dim:
                    fill = S.dim_col(fill)
                c.d.polygon([c.p(*q) for q in p["points"]], fill=fill + (255,))
            elif k == "text":
                texts.append(dict(text=p["text"], x=p["x"], y=p["y"], size=p.get("size", 24),
                                  weight=p.get("weight", "bold"), color=colr, anchor=p.get("anchor", "mm")))
        rgb, a = c.finish()
        if texts:
            rgb, a = text_layer(rgb, a, X0, Y0, texts)
        return Sprite(rgb, a, X0, Y0)


class ImageEl(Elem):
    default_in = "fade"

    def build(self, dim):
        s = self.spec
        im = Image.open(s["path"]).convert("RGBA")
        sc = float(s.get("img_scale", 1.0))
        if abs(sc - 1) > 1e-3:
            im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        arr = np.asarray(im, np.float32)
        a = arr[..., 3] / 255.0
        rgb = arr[..., :3]
        if dim:
            rgb = rgb * 0.35 + np.array(S.BG, np.float32) * 0.65
        x0 = float(s["x"]) - im.width / 2
        y0 = float(s["y"]) - im.height / 2
        return Sprite(rgb.astype(np.float32), a.astype(np.float32), x0, y0)


KINDS = {"circle": Circle, "dots": Dots, "text": Text, "number": Number, "line": Line, "area": Area,
         "rect": Rect, "person": Person, "mixer": Mixer, "group": Group, "image": ImageEl}


def source_spec(spec):
    """'source' = small grey line, convenience kind."""
    d = dict(spec)
    d["type"] = "text"
    d.setdefault("size", S.SIZE["source"])
    d.setdefault("weight", "medium")
    d.setdefault("color", "src")
    return d


# ------------------------------------------------------------------ scheduling
def make(spec):
    if spec["type"] == "source":
        spec = source_spec(spec)
    return KINDS[spec["type"]](spec)


def schedule(ep, tl):
    reg = {}
    alive = []
    order = []
    for shot in tl["shots"]:
        ts = shot["t_start"]
        here = []
        for spec in shot.get("elements", []):
            eid = spec["id"]
            if spec.get("keep"):
                if eid not in reg:
                    raise SystemExit(f"keep: unknown element {eid} in shot {shot['id']}")
                el = reg[eid]
                el.t_out = INF
                md = float(spec.get("move_dur", 0.55))
                mt = T.resolve(spec.get("move_at", "shot+0.0"), tl, shot)
                if any(k in spec for k in ("x", "y", "scale")):
                    lx, ly = el.pivot
                    if el.moves:
                        lx, ly = el.moves[-1][2], el.moves[-1][3]
                    ls = el.moves[-1][4] if el.moves else 1.0
                    el.moves.append((mt, md, float(spec.get("x", lx)), float(spec.get("y", ly)),
                                     float(spec.get("scale", ls))))
                if spec.get("state") == "dim":
                    el.dims.append((T.resolve(spec.get("dim_at", "shot+0.0"), tl, shot), 1.0, 0.3))
                elif spec.get("state") == "normal":
                    el.dims.append((T.resolve(spec.get("dim_at", "shot+0.0"), tl, shot), 0.0, 0.3))
                if spec.get("out"):
                    el.t_out = T.resolve(spec["out"], tl, shot)
                if spec.get("spin"):
                    for sp in spec["spin"]:
                        el.spins.append((T.resolve(sp[0], tl, shot), T.resolve(sp[1], tl, shot), float(sp[2])))
                if spec.get("move_dots_at") and isinstance(el, Dots):
                    el.move_t = T.resolve(spec["move_dots_at"], tl, shot)
                here.append(el)
                continue
            if eid in reg:
                raise SystemExit(f"duplicate element id {eid} (use keep)")
            el = make(spec)
            el.t_in = T.resolve(spec.get("at", "shot+0.3"), tl, shot)
            if spec.get("dim"):
                el.dims.append((T.resolve(spec["dim"], tl, shot), 1.0, 0.3))
            if spec.get("undim"):
                el.dims.append((T.resolve(spec["undim"], tl, shot), 0.0, 0.3))
            if spec.get("out"):
                el.t_out = T.resolve(spec["out"], tl, shot)
            for mv in spec.get("moves", []):
                el.moves.append((T.resolve(mv["at"], tl, shot), float(mv.get("dur", 0.55)),
                                 float(mv.get("x", el.pivot[0])), float(mv.get("y", el.pivot[1])),
                                 float(mv.get("scale", 1.0))))
            for sp in spec.get("spin", []):
                el.spins.append((T.resolve(sp[0], tl, shot), T.resolve(sp[1], tl, shot), float(sp[2])))
            if isinstance(el, Dots) and spec.get("move_dots_at"):
                el.move_t = T.resolve(spec["move_dots_at"], tl, shot)
            reg[eid] = el
            order.append(el)
            here.append(el)
        for el in alive:
            if el not in here and el.t_out >= INF:
                el.t_out = ts
        alive = here
    return order


# ------------------------------------------------------------------ captions
class Captions:
    def __init__(self, tl):
        self.caps = tl["captions"]
        self.cache = {}
        self.on = np.array([c["on"] for c in self.caps])

    def index(self, t):
        i = int(np.searchsorted(self.on, t, side="right")) - 1
        if i < 0:
            return None
        c = self.caps[i]
        return i if c["on"] <= t < c["off"] else None

    def sprite(self, i):
        if i not in self.cache:
            cfg = S.CAPTION
            txt = self.caps[i]["text"]
            f = S.font(cfg["font"], cfg["size"])
            tw = f.getlength(txt)
            bw = int(round(tw + 2 * cfg["pad_x"]))
            bh = cfg["box_h"]
            x0 = int(round(S.W / 2 - bw / 2))
            y0 = int(round(cfg["cy"] - bh / 2))
            rgb = np.zeros((bh, bw, 3), np.float32)
            a = np.full((bh, bw), S.CAP_BOX_ALPHA, np.float32)
            if cfg.get("radius", 0) > 0:
                c = Canvas(x0, y0, x0 + bw, y0 + bh)
                c.d.rounded_rectangle([c.p(x0, y0), c.p(x0 + bw, y0 + bh)], radius=c.s(cfg["radius"]),
                                      fill=(0, 0, 0, 255))
                rgb, a = c.finish()
                a = a * S.CAP_BOX_ALPHA
            rgb, a = text_layer(rgb, a, x0, y0, [dict(text=txt, x=S.W / 2, y=cfg["cy"] + 1, size=cfg["size"],
                                                      weight=cfg["font"], color=cfg["color"], anchor="mm")])
            self.cache[i] = Sprite(rgb, a, x0, y0)
        return self.cache[i]


# ------------------------------------------------------------------ frames
class Renderer:
    def __init__(self, ep, tl):
        self.ep, self.tl = ep, tl
        self.elems = sorted(schedule(ep, tl), key=lambda e: e.z)
        self.caps = Captions(tl)
        self.bg = S.paper_texture()

    def signature(self, t):
        sig = []
        vis = []
        for e in self.elems:
            st = e.state(t)
            if st is None or st["alpha"] <= 0.002:
                continue
            sig.append(e.sig(st))
            vis.append((e, st))
        ci = self.caps.index(t)
        return tuple(sig) + (("cap", ci),), vis, ci

    def compose(self, vis, ci):
        frame = self.bg.copy()
        for e, st in vis:
            e.draw_into(frame, st)
        if ci is not None:
            sp = self.caps.sprite(ci)
            blit(frame, sp, dict(alpha=1.0, scale=1.0, prog=1.0, x=0, y=0), (0, 0))
        return np.clip(frame + 0.5, 0, 255).astype(np.uint8)

    def frame_at(self, t):
        _, vis, ci = self.signature(t)
        return self.compose(vis, ci)

    def render(self, out, audio=None, crf=18, threads=1, t0=0.0, t1=None, log_every=300):
        fps = S.FPS
        dur = self.tl["duration"] if t1 is None else t1
        n = int(math.ceil((dur - t0) * fps))
        cmd = ["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{S.W}x{S.H}", "-r", str(fps), "-i", "-"]
        if audio:
            cmd += ["-ss", f"{t0:.3f}", "-i", audio]
        else:
            cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
        cmd += ["-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage",
                "-crf", str(crf), "-pix_fmt", "yuv420p", "-threads", str(threads), "-c:a", "aac", "-b:a", "192k",
                "-ar", "48000", "-t", f"{n / fps:.3f}", "-movflags", "+faststart", out]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        prev_sig, buf = None, None
        uniq = 0
        for i in range(n):
            t = t0 + i / fps
            sig, vis, ci = self.signature(t)
            if sig != prev_sig:
                buf = self.compose(vis, ci).tobytes()
                prev_sig = sig
                uniq += 1
            p.stdin.write(buf)
            if log_every and i % log_every == 0:
                print(f"  frame {i}/{n} t={t:6.1f}s unique={uniq}", file=sys.stderr, flush=True)
        p.stdin.close()
        rc = p.wait()
        if rc != 0:
            raise SystemExit(f"ffmpeg failed rc={rc}")
        return dict(frames=n, unique=uniq)


def stills(rend, times, out_dir, prefix="still", width=None):
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for t in times:
        img = Image.fromarray(rend.frame_at(t))
        if width:
            img = img.resize((width, int(width * S.H / S.W)), Image.LANCZOS)
        pth = os.path.join(out_dir, f"{prefix}_{t:07.2f}.png")
        img.save(pth)
        paths.append(pth)
    return paths


def contact_sheet(paths, out, cols=4, label=True):
    from PIL import ImageFont
    ims = [Image.open(p) for p in paths]
    w, h = ims[0].size
    lab = 24 if label else 0
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * (h + lab)), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    f = S.font("bold", 18)
    for i, (im, pth) in enumerate(zip(ims, paths)):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        sheet.paste(im, (x, y + lab))
        if label:
            d.text((x + 6, y + 2), os.path.basename(pth).rsplit(".", 1)[0], fill=(200, 0, 0), font=f)
    sheet.save(out, quality=85)
    return out
