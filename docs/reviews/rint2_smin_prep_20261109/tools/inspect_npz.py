import sys, numpy as np
for p in sys.argv[1:]:
    print('==', p)
    with np.load(p, allow_pickle=False) as z:
        for k in z.files:
            a = z[k]
            info = f'{k}: dtype={a.dtype} shape={a.shape}'
            if a.dtype.kind in 'fiub' and a.size:
                af = a.astype(np.float64)
                fin = np.isfinite(af)
                info += f' finite={int(fin.sum())}'
                if fin.any():
                    info += f' min={af[fin].min():.6g} max={af[fin].max():.6g}'
                if a.dtype.kind == 'b':
                    info += f' true={int(a.sum())}'
            elif a.dtype.kind == 'U' and a.size:
                u, c = np.unique(a, return_counts=True)
                info += ' uniq=' + str(dict(zip(u.tolist()[:10], c.tolist()[:10])))
            print(info)
