"""내부 반박 리뷰 2 회차 산술 (읽기만): 15-5b 지표의 정직 흐름 여유 + 대안 지표 (|Ft| 가중 · 무너짐 몫).
쓰임: python3 -I r2_alt_metrics.py <기준 쌍 덤프> <시험 쌍 덤프>"""
import sys
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0] if '/' in sys.argv[0] else '.')
from r2_cont_guard import read_pairs, norm


def main(o_path, t_path):
    _, o = read_pairs(o_path)
    _, t = read_pairs(t_path)
    common = sorted(set(o) & set(t))
    tot, wbad, collapse, small = 0.0, 0.0, 0, 0
    fts = sorted(norm(o[k]['ft']) for k in common)
    p10 = fts[int(0.10 * (len(fts) - 1))]
    big_reset, big_n = 0, 0
    for k in common:
        fo, ft = o[k]['ft'], t[k]['ft']
        n = norm(fo)
        r = norm([ft[c] - fo[c] for c in range(3)]) / n
        tot += n
        if r > 0.5:
            wbad += n
            if n < p10:
                small += 1
        if norm(ft) < 0.5 * n:
            collapse += 1
        if n >= p10:
            big_n += 1
            big_reset += r > 0.5
    print(t_path.split('run40000/')[-1], 'common', len(common),
          '| |Ft|-weighted reset', round(wbad / tot, 5),
          '| collapse(|Ft_t|<0.5|Ft_o|)', collapse, round(collapse / len(common), 5),
          '| reset among |Ft_o|<p10', small, '| reset_frac among |Ft_o|>=p10', round(big_reset / big_n, 5), 'p10', p10)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
