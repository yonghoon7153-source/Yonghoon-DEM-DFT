# Crop the four attached renders to content (alpha bbox) and give the two bed renders the same
# tone curve as the 22 GPa bed already in the slide (PowerPoint brightness +20 % / contrast +20 %
# cached in image7.png). One LUT per channel, derived once from the pooled raw beds, applied to both.
import sys, numpy as np
from PIL import Image
S = sys.argv[1]
ref = np.asarray(Image.open(S + '/arr_x/u/ppt/media/image7.png').convert('RGBA'))
def load(k): return np.asarray(Image.open(f'{S}/arr_img/att{k}.webp').convert('RGBA'))
def crop(a):
    ys, xs = np.where(a[..., 3] > 8); return a[ys.min():ys.max()+1, xs.min():xs.max()+1]
beds = {11: crop(load(2)), 33: crop(load(4))}
paths = {11: crop(load(1)), 33: crop(load(3))}
op = lambda a: a[..., 3] > 200
q = np.linspace(0, 100, 1001)
luts = []
for c in range(3):
    raw = np.concatenate([b[..., c][op(b)] for b in beds.values()]).astype(float)
    tgt = ref[..., c][op(ref)].astype(float)
    xr, yt = np.percentile(raw, q), np.percentile(tgt, q)
    xr, idx = np.unique(xr, return_index=True); yt = np.maximum.accumulate(yt[idx])
    luts.append(np.clip(np.interp(np.arange(256), xr, yt), 0, 255).astype(np.uint8))
for e, b in beds.items():
    o = b.copy()
    for c in range(3): o[..., c] = luts[c][b[..., c]]
    Image.fromarray(o).save(f'{S}/arr_work/new/bed_E{e}.png')
for e, p in paths.items():
    Image.fromarray(p).save(f'{S}/arr_work/new/path_E{e}.png')
def cls(a):
    rgb = a[..., :3][op(a)].astype(float); lum = rgb.mean(1)
    return rgb[lum > 120].mean(0).round(1).tolist(), rgb[lum < 60].mean(0).round(1).tolist(), round(float((lum > 120).mean()), 3)
print('ref E22 ', cls(ref))
for e in beds: print('bed E%d' % e, cls(np.asarray(Image.open(f'{S}/arr_work/new/bed_E{e}.png'))), np.asarray(Image.open(f'{S}/arr_work/new/bed_E{e}.png')).shape)
for e in paths: print('path E%d' % e, np.asarray(Image.open(f'{S}/arr_work/new/path_E{e}.png')).shape)
print('LUT R at 18,98,146,154:', [int(luts[0][v]) for v in (18, 98, 146, 154)])
