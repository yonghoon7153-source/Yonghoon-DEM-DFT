# ibb 원 런 폴더에서 돌리는 읽기 전용 스캔 (1저자 10-08 밤) — 1저자에게 대화로 보낸 heredoc 과 같은 코드 (이 머리말만 더함).
#   cd ~/dem_test/ps45/ps_7_3_r45 && nice -n 19 python3 -I atom_top_scan.py
# 원 런 atom 덤프 post_ps_7_3_r45/atom_<step>.liggghts 마다: 덤프 머리 TIMESTEP · 원자 수 · 깨진 줄 · 맨 위 중심 max(z) ·
# 맨 위 윗면 max(z + r) 와 그 입자 (id · type · r) · 윗면 p99.9 · 파일 크기 · 수정 시각 → ~/ps73_atom_top_20261008.csv.
# 값 단위 = 덱 m (× 1000 = µm).  검사 · 그림 = make_fig_ms.py (check_scan ①–⑦).
import glob, os, re, csv, time, sys
D = 'post_ps_7_3_r45'
OUT = os.path.expanduser('~/ps73_atom_top_20261008.csv')
pat = re.compile(r'atom_(\d+)\.liggghts$')
files = sorted((int(pat.search(p).group(1)), p) for p in glob.glob(os.path.join(D, 'atom_*.liggghts')) if pat.search(p))
print('atom 덤프', len(files), '장'); sys.stdout.flush()
rows, bad = [], []
for k, (step, p) in enumerate(files):
    with open(p) as f:
        head = [f.readline() for _ in range(9)]
        ts, n = int(head[1]), int(head[3])
        cols = head[8].split()[2:]
        iz, ir, ii, it = cols.index('z'), cols.index('radius'), cols.index('id'), cols.index('type')
        tops, zc, best, badline = [], -1e9, None, 0
        for line in f:
            t = line.split()
            if len(t) != len(cols):
                badline += 1; continue
            z = float(t[iz]); r = float(t[ir]); h = z + r
            tops.append(h)
            if z > zc: zc = z
            if best is None or h > best[0]: best = (h, t[ii], t[it], r)
    cnt = len(tops)
    if ts != step or cnt != n or badline: bad.append((step, ts, n, cnt, badline))
    tops.sort()
    p999 = tops[int(0.999 * (cnt - 1))] if cnt else float('nan')
    st = os.stat(p)
    b = best or (float('nan'), '', '', float('nan'))
    rows.append([step, ts, n, cnt, badline, '%.9g' % zc, '%.9g' % b[0], b[1], b[2], '%.9g' % b[3], '%.9g' % p999,
                 st.st_size, time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(st.st_mtime))])
    if (k + 1) % 50 == 0: print('  ', k + 1, '/', len(files), step); sys.stdout.flush()
with open(OUT, 'w', newline='') as fo:
    w = csv.writer(fo)
    w.writerow(['step', 'dump_timestep', 'n_header', 'n_rows', 'n_bad_lines', 'zc_max_deck_m', 'ztop_max_deck_m',
                'ztop_id', 'ztop_type', 'ztop_radius_deck_m', 'ztop_p999_deck_m', 'bytes', 'mtime'])
    w.writerows(rows)
mt = [r[-1] for r in rows]
print('step', rows[0][0] if rows else None, '→', rows[-1][0] if rows else None, '· 간격', sorted({b[0] - a[0] for a, b in zip(rows, rows[1:])}))
print('어긋남', len(bad), bad[:5], '· mtime 단조 증가', all(a <= b for a, b in zip(mt, mt[1:])))
print('→', OUT)
