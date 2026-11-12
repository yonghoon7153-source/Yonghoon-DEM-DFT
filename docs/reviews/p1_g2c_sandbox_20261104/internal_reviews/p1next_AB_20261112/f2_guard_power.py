"""2 회차 고침 산술 (읽기만 · LIGGGHTS · ibb · 실행 없음) — 초안 A 15-5b 지표 고르기.
리뷰 2 회차 산술 (r2_cont_guard.py · r2_alt_metrics.py) 의 읽기 함수 · r 정의를 그대로 쓰고,
|Ft| 가중 reset 몫 (W) 의 정직 값과 소실 반례 (시험 쪽 Ft -> 0 근사 · 감쇠 몫 무시) 를 셈.
쓰임: python3 -I f2_guard_power.py <기준 A(N) 쌍 덤프> <정직 시험 B 쌍 덤프> <정직 시험 C 쌍 덤프>
"""
import hashlib
import sys

sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0] if '/' in sys.argv[0] else '.')
from r2_cont_guard import read_pairs, norm  # noqa: E402


def r_of(fo, ft):
    n = norm(fo)
    return norm([ft[c] - fo[c] for c in range(3)]) / n if n > 0 else None


def metrics(o, t):
    common = sorted(set(o) & set(t))
    tot = sum(norm(o[k]['ft']) for k in common)
    rs, cnt, w, col, colw = [], 0, 0.0, 0, 0.0
    for k in common:
        fo, ft = o[k]['ft'], t[k]['ft']
        n = norm(fo)
        r = r_of(fo, ft)
        if r is None:
            continue
        rs.append(r)
        if r > 0.5:
            cnt += 1
            w += n
        if norm(ft) < 0.5 * n:
            col += 1
            colw += n
    rs.sort()
    return {'common': len(common), 'missing': len(set(o) - set(t)), 'extra': len(set(t) - set(o)),
            'count_share': cnt / len(common), 'W': w / tot, 'r_median': rs[len(rs) // 2],
            'collapse_share': col / len(common), 'collapse_W': colw / tot}


def zero(t, keys):
    out = {}
    for k, v in t.items():
        out[k] = dict(v)
        if k in keys:
            out[k]['ft'] = [0.0, 0.0, 0.0]
    return out


def hfrac(key):
    h = hashlib.sha256(('%d-%d' % key).encode()).hexdigest()
    return int(h[:12], 16) / float(16 ** 12)


def main(a_path, b_path, c_path):
    _, a = read_pairs(a_path)
    _, b = read_pairs(b_path)
    _, c = read_pairs(c_path)
    # 쌍 위치 (원자 i · j 좌표 = 열 1-6) 다시 읽기 — read_pairs 는 힘만 담음
    pos = {}
    with open(a_path, encoding='ascii') as f:
        lines = f.read().splitlines()
    h = next(i for i, x in enumerate(lines) if x.startswith('ITEM: ENTRIES'))
    for ln in lines[h + 1:]:
        if not ln.strip():
            continue
        v = [float(x) for x in ln.split()]
        i, j = int(v[6]), int(v[7])
        key = (min(i, j), max(i, j))
        pi, pj = (v[0], v[1]), (v[3], v[4])
        # 큰 tag 쪽 원자 좌표 (11-02 보고 §2-2 · 덤프되는 사본 = 큰 tag 쪽) · 작은 tag 쪽
        big = pi if i > j else pj
        small = pj if i > j else pi
        pos[key] = {'big': big, 'small': small}
    print('정직 B <-> A(N) (주기 파일 · 한 step 늦은 이력):', {k: round(x, 5) if isinstance(x, float) else x for k, x in metrics(a, b).items()})
    print('정직 C <-> A(N) (명령 파일):', {k: round(x, 5) if isinstance(x, float) else x for k, x in metrics(a, c).items()})
    tot = sum(norm(a[k]['ft']) for k in a)
    keys_all = set(a)
    flag1 = {k for k, v in a.items() if v['flag'] == 1}
    print('\n소실 반례 (정직 B 위에 겹침 · 시험 Ft -> 0 근사):')
    print('  전부 잃음          ', round(metrics(a, zero(b, keys_all))['W'], 4))
    m = metrics(a, zero(b, flag1))
    print('  표지 1 쌍만 (n=%d · 쌍 몫 %.4f · |Ft| 몫 %.4f)' % (len(flag1), len(flag1) / len(a), sum(norm(a[k]['ft']) for k in flag1) / tot),
          'W', round(m['W'], 4), 'count', round(m['count_share'], 4))
    # 3x2x1 하위영역 (상자 0.012 x 0.012 · 하위영역 0.004 x 0.006) · 한 랭크 몫 잃음
    for side in ('big', 'small'):
        ws = []
        for ix in range(3):
            for iy in range(2):
                ks = {k for k, p in pos.items() if int(p[side][0] / 0.004) == ix and int(p[side][1] / 0.006) == iy}
                m = metrics(a, zero(b, ks))
                ws.append((ix, iy, len(ks), round(m['W'], 4), round(m['count_share'], 4)))
        print('  한 하위영역 (3x2x1 · 쌍 자리 = %s tag 원자) (ix, iy, n, W, count):' % side, ws)
    # 2x2x1 · 6x4x1 도 (원 쓴 NP 4 · 24 꼴)
    for (nx, ny) in ((2, 2), (6, 4)):
        ws, cs, nw = [], [], 0
        for ix in range(nx):
            for iy in range(ny):
                ks = {k for k, p in pos.items() if min(int(p['big'][0] / (0.012 / nx)), nx - 1) == ix and min(int(p['big'][1] / (0.012 / ny)), ny - 1) == iy}
                m = metrics(a, zero(b, ks))
                ws.append(m['W'])
                cs.append(m['count_share'])
                nw += m['W'] > 0.05
        print('  한 하위영역 (%dx%dx1 · 큰 tag) W 최소 %.4f 최대 %.4f (W > 0.05 = %d/%d) · count 최소 %.4f 최대 %.4f'
              % (nx, ny, min(ws), max(ws), nw, nx * ny, min(cs), max(cs)))
    # 무작위 몫 p (결정적 해시)
    for p in (0.02, 0.05, 0.10, 0.20):
        ks = {k for k in a if hfrac(k) < p}
        m = metrics(a, zero(b, ks))
        print('  무작위 몫 %.2f (n=%d)' % (p, len(ks)), 'W', round(m['W'], 4), 'count', round(m['count_share'], 4))
    # |Ft| 하위 q 몫만 잃음 · 상위 q 몫만 잃음
    srt = sorted(a, key=lambda k: norm(a[k]['ft']))
    for q in (0.10, 0.25, 0.50, 0.60, 0.70, 0.80):
        ks = set(srt[:int(q * len(srt))])
        m = metrics(a, zero(b, ks))
        print('  |Ft| 하위 %.2f 잃음 (|Ft| 몫 %.4f)' % (q, sum(norm(a[k]['ft']) for k in ks) / tot), 'W', round(m['W'], 4), 'count', round(m['count_share'], 4))
    for q in (0.01, 0.02, 0.05):
        ks = set(srt[-int(q * len(srt)):])
        m = metrics(a, zero(b, ks))
        print('  |Ft| 상위 %.2f 잃음 (|Ft| 몫 %.4f)' % (q, sum(norm(a[k]['ft']) for k in ks) / tot), 'W', round(m['W'], 4), 'count', round(m['count_share'], 4))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
