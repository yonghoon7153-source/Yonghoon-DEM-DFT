#!/usr/bin/env python3
"""Thumbnail: reference layout (measured on the channel's 4 thumbnails) with our own
rendered object (numpy ray casting — no external images).

Layout: off-white background (248,244,240); two-line bold title at the left (x margin
~5 % W, glyph height ~10-14 % H); one keyword in indigo with a lavender highlighter
band; one photographic-looking object on the right with a soft ground shadow.
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw

import avi_style as S

TBG = np.array([248.0, 244.0, 240.0])


def _normalize(v):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)


def powder_scene(seed=4):
    rng = np.random.default_rng(seed)
    big = (np.array([0.0, 1.0, 0.0]), 1.0, "ncm")
    sph = [big]
    r = 0.15
    # SE particles attached to the upper-left / front of the big sphere (partial coverage)
    k = 0
    while k < 26:
        th = rng.uniform(0.15, 1.35)       # polar from +y
        ph = rng.uniform(1.9, 4.4)         # around the left-front side
        n = np.array([math.sin(th) * math.cos(ph), math.cos(th), math.sin(th) * math.sin(ph)])
        c = big[0] + n * (big[1] + r * 0.92)
        if all(np.linalg.norm(c - s[0]) > (r + s[1]) * 0.98 for s in sph[1:]):
            sph.append((c, r, "se"))
            k += 1
    # a clump of SE particles on the ground to the right
    cl = np.array([1.62, 0.0, -0.35])
    k = 0
    tries = 0
    while k < 30 and tries < 4000:
        tries += 1
        c = cl + np.array([rng.normal(0, 0.24), 0.0, rng.normal(0, 0.24)])
        c[1] = r
        # stack: raise until no overlap (simple settling)
        for _ in range(12):
            ov = [s for s in sph[1:] if np.linalg.norm(c - s[0]) < (r + s[1]) * 0.97]
            if not ov:
                break
            c[1] += r * 0.55
        if c[1] > 0.95 or np.linalg.norm(c[[0, 2]] - cl[[0, 2]]) > 0.5:
            continue
        if np.linalg.norm(c - big[0]) < big[1] + r:
            continue
        sph.append((c.copy(), r, "se"))
        k += 1
    # a few loose particles
    for p in ([1.05, r, -0.95], [-1.25, r, -0.65], [2.25, r, 0.15], [0.95, r, 0.65]):
        sph.append((np.array(p), r, "se"))
    return sph


def render_powder(w, h, ss=2, seed=4, light_samples=10, fov_deg=38.0, target=(0.62, 0.70, -0.12), cam_pos=(0.2, 2.35, -6.4)):
    sph = powder_scene(seed)
    W, H = w * ss, h * ss
    cam = np.array(cam_pos, float)
    tgt = np.array(target, float)
    fwd = _normalize(tgt - cam)
    right = _normalize(np.cross(np.array([0, 1.0, 0]), fwd))
    up = np.cross(fwd, right)
    fov = math.radians(fov_deg)
    th = math.tan(fov / 2)
    ys, xs = np.mgrid[0:H, 0:W]
    u = ((xs + 0.5) / W * 2 - 1) * th * (W / H)
    v = (1 - (ys + 0.5) / H * 2) * th
    d = _normalize(fwd[None, None, :] + u[..., None] * right + v[..., None] * up).reshape(-1, 3)
    o = cam
    N = d.shape[0]
    tmin = np.full(N, np.inf)
    sid = np.full(N, -1)
    for i, (c, r, _) in enumerate(sph):
        oc = o - c
        b = d @ oc
        cc = oc @ oc - r * r
        disc = b * b - cc
        ok = disc > 0
        t = np.where(ok, -b - np.sqrt(np.maximum(disc, 0)), np.inf)
        t = np.where(t > 1e-4, t, np.inf)
        better = t < tmin
        tmin[better] = t[better]
        sid[better] = i
    tg = np.where(d[:, 1] < -1e-6, -o[1] / d[:, 1], np.inf)
    ground = (tg < tmin)
    hit = np.isfinite(tmin) & ~ground
    col = np.tile(TBG, (N, 1))
    Lkey = _normalize(np.array([-0.55, 0.95, -0.45]))
    Lfill = _normalize(np.array([0.9, 0.35, -0.6]))
    rng = np.random.default_rng(1)
    # jittered key-light directions for soft shadows
    Ls = []
    for _ in range(light_samples):
        j = Lkey + rng.normal(0, 0.09, 3)
        Ls.append(_normalize(j))

    def occluded(P, Ld):
        occ = np.zeros(len(P), bool)
        for (c, r, _) in sph:
            oc = P - c
            b = oc @ Ld
            cc = np.einsum("ij,ij->i", oc, oc) - r * r
            disc = b * b - cc
            t = -b - np.sqrt(np.maximum(disc, 0))
            occ |= (disc > 0) & (t > 1e-4)
        return occ

    # ---- spheres
    idx = np.where(hit)[0]
    if len(idx):
        P = o + d[idx] * tmin[idx, None]
        C = np.array([sph[i][0] for i in sid[idx]])
        R = np.array([sph[i][1] for i in sid[idx]])
        kind = np.array([sph[i][2] for i in sid[idx]])
        n = (P - C) / R[:, None]
        is_ncm = kind == "ncm"
        if is_ncm.any():
            # agglomerate bumps: nearest of many random 'primary grains' on the unit sphere
            g = rng.normal(size=(700, 3))
            g = _normalize(g)
            nn = n[is_ncm]
            dots = nn @ g.T
            j = np.argmax(dots, axis=1)
            gd = g[j]
            cosd = dots[np.arange(len(j)), j]
            ang = np.arccos(np.clip(cosd, -1, 1))
            bump = np.clip(1 - ang / 0.11, 0, 1)
            pert = _normalize(nn - gd * cosd[:, None])
            nn2 = _normalize(nn + pert * (0.55 * (1 - bump))[:, None] * 0.42)
            n[is_ncm] = nn2
            crev = np.clip((ang - 0.06) / 0.05, 0, 1)   # darker crevices between grains
        lit = np.zeros(len(idx))
        for Ld in Ls:
            sh = ~occluded(P + n * 1e-3, Ld)
            nd = np.clip(n @ Ld, 0, 1)
            lit += sh * nd
        lit /= len(Ls)
        fill = np.clip(n @ Lfill, 0, 1) * 0.25
        # ambient occlusion from nearby spheres + ground
        ao = np.ones(len(idx))
        for (c, r, _) in sph:
            dv = c - P
            dist = np.linalg.norm(dv, axis=1)
            facing = np.clip(np.einsum("ij,ij->i", n, dv) / (dist + 1e-9), 0, 1)
            occ = np.where(dist > r * 1.01, (r / dist) ** 2 * facing, 0)
            ao -= 0.55 * occ
        ao -= 0.35 * np.clip(1 - P[:, 1] / 0.45, 0, 1) * np.clip(-n[:, 1], 0, 1)
        ao = np.clip(ao, 0.25, 1)
        base = np.where(is_ncm[:, None], np.array([46.0, 48.0, 54.0]), np.array([236.0, 230.0, 212.0]))
        if is_ncm.any():
            base[is_ncm] *= (1 - 0.22 * crev)[:, None]
        Hh = _normalize(Lkey[None, :] - d[idx])
        spec = np.clip(np.einsum("ij,ij->i", n, Hh), 0, 1)
        spec = np.where(is_ncm, 0.55 * spec ** 38, 0.18 * spec ** 18)
        amb = 0.32 * ao
        shade = (0.78 * lit + fill) * np.where(is_ncm, 1.0, 0.92) + amb
        c_out = base * shade[:, None] + 255.0 * spec[:, None] * (0.6 + 0.4 * lit[:, None])
        # gentle warm bounce from the ground on lower faces
        c_out += np.array([18.0, 14.0, 8.0]) * np.clip(-n[:, 1], 0, 1)[:, None] * ao[:, None]
        col[idx] = c_out
    # ---- ground shadows / contact occlusion
    gi = np.where(ground)[0]
    if len(gi):
        P = o + d[gi] * tg[gi, None]
        frac = np.zeros(len(gi))
        for Ld in Ls:
            frac += occluded(P + np.array([0, 1e-3, 0]), Ld)
        frac /= len(Ls)
        cont = np.zeros(len(gi))
        for (c, r, _) in sph:
            dxz = np.hypot(P[:, 0] - c[0], P[:, 2] - c[2])
            hgt = max(c[1] - r, 0.0)
            cont += np.exp(-((dxz / (r * 1.25)) ** 2)) * math.exp(-hgt / (r * 0.8)) * 0.8
        dark = np.clip(0.42 * frac + 0.30 * np.clip(cont, 0, 1), 0, 0.68)
        col[gi] = TBG * (1 - dark[:, None]) + np.array([150.0, 140.0, 132.0]) * dark[:, None] * 0.0
    img = col.reshape(H, W, 3)
    alpha = np.zeros(N)
    alpha[hit] = 1.0
    if len(gi):
        alpha[gi] = dark
    alpha = alpha.reshape(H, W)
    if ss > 1:
        img = img.reshape(h, ss, w, ss, 3).mean(axis=(1, 3))
        alpha = alpha.reshape(h, ss, w, ss).mean(axis=(1, 3))
    render_powder.last_alpha = alpha
    return np.clip(img, 0, 255)


def object_png(path, w=520, h=520, ss=2):
    """Transparent PNG of the powder object: spheres opaque, ground shadow as a soft dark veil."""
    rgb = render_powder(w, h, ss=ss)
    a = render_powder.last_alpha
    sphere = np.clip((np.abs(rgb - TBG[None, None, :]).max(axis=2) > 1.5) & (a > 0.98), 0, 1)
    shadow_rgb = np.array([22.0, 16.0, 12.0])          # veil: bg*(1-a) + c*a  ~= bg*(1-dark) as in the thumbnail
    out_rgb = np.where(sphere[..., None] > 0, rgb, shadow_rgb[None, None, :])
    # the ground shadow can reach the image border; fade the veil (not the spheres) to 0 over `fe` px
    # so no straight cut edge shows on the paper (11-24: left border alpha was 23/255)
    fe = 40.0
    yy, xx = np.mgrid[0:h, 0:w]
    m = np.clip(np.minimum.reduce([xx / fe, (w - 1 - xx) / fe, yy / fe, (h - 1 - yy) / fe]), 0, 1)
    m = m * m * (3 - 2 * m)
    out_a = np.where(sphere > 0, a, np.clip(a, 0, 1) * m)
    img = np.concatenate([out_rgb, out_a[..., None] * 255.0], axis=2)
    Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGBA").save(path)
    return path


def make(ep, ep_dir, out="thumbnail.png"):
    th = ep.get("thumb", {})
    lines = th.get("lines", [ep["title"]])
    hl = th.get("highlight")
    W, H = 1280, 720
    from scipy.ndimage import gaussian_filter
    rng = np.random.default_rng(11)
    tex = gaussian_filter(rng.standard_normal((H, W)), 3) * 4.0
    base = np.empty((H, W, 3))
    for k in range(3):
        base[..., k] = TBG[k] + tex
    # object on the right
    ow, oh = int(th.get("obj_w", 560)), int(th.get("obj_h", 560))
    obj = render_powder(ow, oh, ss=2)
    x0 = W - ow - int(th.get("obj_right", 10))
    y0 = (H - oh) // 2 + int(th.get("obj_dy", 20))
    region = base[y0:y0 + oh, x0:x0 + ow]
    # blend: add the object's difference from the plain background, feathered at the region border
    diff = obj - TBG[None, None, :]
    fe = 48.0
    yy, xx = np.mgrid[0:oh, 0:ow]
    m = np.minimum.reduce([xx / fe, (ow - 1 - xx) / fe, yy / fe, (oh - 1 - yy) / fe])
    m = np.clip(m, 0, 1)
    m = m * m * (3 - 2 * m)
    region += diff * m[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    size = int(th.get("size", 104))
    f = S.font("extrabold", size)
    x = 68
    ys = th.get("y", [262, 410])
    for li, text in enumerate(lines):
        y = ys[li]
        if hl and hl in text:
            pre, post = text.split(hl, 1)
            wp = f.getlength(pre)
            wh = f.getlength(hl)
            bb = f.getbbox(hl, anchor="ls")
            top, bot = y + bb[1], y + bb[3]
            band_top = top + 0.48 * (bot - top)
            d.rectangle([x + wp - 6, band_top, x + wp + wh + 6, bot + 0.10 * (bot - top)], fill=(216, 209, 241))
            d.text((x, y), pre, font=f, fill=S.INK, anchor="ls")
            d.text((x + wp, y), hl, font=f, fill=S.INDIGO, anchor="ls")
            d.text((x + wp + wh, y), post, font=f, fill=S.INK, anchor="ls")
        else:
            d.text((x, y), text, font=f, fill=S.INK, anchor="ls")
    path = out if os.path.isabs(out) else os.path.join(ep_dir, out)
    img.save(path)
    return path
