# ps73 원 런 atom 덤프 다시 훑기 v2 (1저자 10-08 밤) — ibb 원 런 폴더에서 읽기만.
#   cd ~/dem_test/ps45/ps_7_3_r45 && nice -n 19 python3 -I scan_v2.py
# v1 (`../atom_top_scan.py`) 과 다른 점: 같은 step 판 메시 (post_ps_7_3_r45/mesh_<step>.stl · 꼭짓점 z 평균 · 평판 아니면 거부) 를 읽어
#   중심이 판보다 **위** 인 입자 (판을 뚫고 나간 입자 — v1 결과에서 1.58 s 부터 맨 위 입자가 이것이었다) 를 따로 세고,
#   침대 맨 위 (판 아래 입자만의 max(z + r) · 중심 max · p99.9) 를 낸다.  값 단위 = 덱 m (× 1000 = µm).  CSV 줄 끝 = LF.
import glob, os, re, csv, sys
D = 'post_ps_7_3_r45'
OUT = os.path.expanduser('~/ps73_atom_top_v2_20261008.csv')
pat = re.compile(r'atom_(\d+)\.liggghts$')


def plate_z(step):
    zs = []
    with open(os.path.join(D, 'mesh_%d.stl' % step)) as f:
        for ln in f:
            t = ln.split()
            if len(t) == 4 and t[0] == 'vertex':
                zs.append(float(t[3]))
    if not zs or max(zs) - min(zs) > 1e-7:
        raise SystemExit('판 STL %d: 꼭짓점 %d · z 폭 %s — 평판 아님' % (step, len(zs), (max(zs) - min(zs)) if zs else None))
    return sum(zs) / len(zs)


files = sorted((int(pat.search(p).group(1)), p) for p in glob.glob(os.path.join(D, 'atom_*.liggghts')) if pat.search(p))
print('atom 덤프', len(files), '장'); sys.stdout.flush()
rows = []
for k, (step, p) in enumerate(files):
    pz = plate_z(step)
    with open(p) as f:
        head = [f.readline() for _ in range(9)]
        ts, n = int(head[1]), int(head[3])
        cols = head[8].split()[2:]
        iz, ir, ii, it = cols.index('z'), cols.index('radius'), cols.index('id'), cols.index('type')
        tops, zc, best, bad, cnt, top_all, above = [], -1e9, None, 0, 0, -1e9, []
        for line in f:
            t = line.split()
            if len(t) != len(cols):
                bad += 1; continue
            z = float(t[iz]); r = float(t[ir]); h = z + r; cnt += 1
            if h > top_all: top_all = h
            if z > pz:
                above.append((z, t[ii], t[it])); continue
            tops.append(h)
            if z > zc: zc = z
            if best is None or h > best[0]: best = (h, t[ii], t[it], r)
    tops.sort()
    above.sort(reverse=True)
    rows.append([step, ts, n, cnt, bad, '%.9g' % pz, len(above), ' '.join('%s:%s' % (a[1], a[2]) for a in above[:5]),
                 '%.9g' % above[0][0] if above else '', '%.9g' % top_all,
                 '%.9g' % zc, '%.9g' % best[0], best[1], best[2], '%.9g' % best[3], '%.9g' % tops[int(0.999 * (len(tops) - 1))]])
    if (k + 1) % 50 == 0: print('  ', k + 1, '/', len(files), step, '판 위', len(above)); sys.stdout.flush()
with open(OUT, 'w', newline='') as fo:
    w = csv.writer(fo, lineterminator='\n')
    w.writerow(['step', 'dump_timestep', 'n_header', 'n_rows', 'n_bad_lines', 'plate_z_deck_m', 'n_above_plate', 'above_ids',
                'above_zc_max_deck_m', 'ztop_all_max_deck_m', 'zc_bed_max_deck_m', 'ztop_bed_max_deck_m', 'ztop_bed_id',
                'ztop_bed_type', 'ztop_bed_radius_deck_m', 'ztop_bed_p999_deck_m'])
    w.writerows(rows)
na = [r[6] for r in rows]
print('판 위 입자 수: 처음', na[0], '· 최대', max(na), '(step', rows[na.index(max(na))][0], ') · 끝', na[-1])
print('→', OUT)
