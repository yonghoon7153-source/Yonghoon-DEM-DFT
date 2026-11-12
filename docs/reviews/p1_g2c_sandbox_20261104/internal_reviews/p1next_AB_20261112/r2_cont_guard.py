"""내부 반박 리뷰 2 회차 산술 (읽기만 · 실행 · LIGGGHTS 없음).
초안 A §15-5b 지표 (11-02 rj_g2c_cause_check.py 336-341 정의) 를 11-12 직렬 침대 덤프에 대 본다:
  r = |Ft_t - Ft_o| / |Ft_o| (|Ft_o| > 0) · reset_like = r > 0.5 · 몫 = reset_like / 공통 쌍.
쓰임: python3 -I r2_cont_guard.py <원 (기준) 쌍 덤프> <시험 쌍 덤프> [<원 (기준) 쌍 덤프 > ...]
열 = 30 열 샌드박스 꼴 (1-6 pos · 7-9 id id flag · 10-12 force · 13-15 fn · 16-18 ft · 19-21 torque · 22-25 history · 26 area · 27 delta · 28-30 cp).
"""
import math
import sys


def read_pairs(path):
    with open(path, encoding='ascii') as f:
        lines = f.read().splitlines()
    step = int(lines[lines.index('ITEM: TIMESTEP') + 1])
    h = next(i for i, x in enumerate(lines) if x.startswith('ITEM: ENTRIES'))
    out = {}
    for ln in lines[h + 1:]:
        if not ln.strip():
            continue
        v = [float(t) for t in ln.split()]
        i, j = int(v[6]), int(v[7])
        key = (min(i, j), max(i, j))
        sgn = 1.0 if i < j else -1.0
        assert key not in out, ('dup', key)
        out[key] = {'ft': [sgn * v[15], sgn * v[16], sgn * v[17]],
                    'fn': [sgn * v[12], sgn * v[13], sgn * v[14]],
                    'hist': v[21:25], 'flag': int(v[8])}
    return step, out


def norm(a):
    return math.sqrt(sum(x * x for x in a))


def stats(o, t):
    common = sorted(set(o) & set(t))
    rs, reset, flag_reset = [], 0, 0
    for k in common:
        fo, ft = o[k]['ft'], t[k]['ft']
        n = norm(fo)
        if n > 0:
            r = norm([ft[c] - fo[c] for c in range(3)]) / n
            rs.append(r)
            if r > 0.5:
                reset += 1
                flag_reset += o[k]['flag']
    rs.sort()
    med = rs[len(rs) // 2] if rs else float('nan')
    q95 = rs[int(0.95 * (len(rs) - 1))] if rs else float('nan')
    return {'common': len(common), 'missing': len(set(o) - set(t)), 'extra': len(set(t) - set(o)),
            'n_r': len(rs), 'reset_like': reset, 'reset_frac': reset / len(common) if common else float('nan'),
            'reset_flag1': flag_reset, 'r_median': med, 'r_q95': q95, 'r_max': rs[-1] if rs else float('nan')}


def hist_zero(o):
    """시험 꼴 반례: 시험 쪽 shear 를 0 으로 잃었을 때 (한 증분 · 감쇠 무시 = Ft_t ~ 0) 의 지표."""
    t = {k: {'ft': [0.0, 0.0, 0.0], 'fn': v['fn'], 'hist': [0, 0, 0, v['hist'][3]], 'flag': v['flag']} for k, v in o.items()}
    return t


def subset_zero(o, frac_keys):
    t = {}
    for k, v in o.items():
        t[k] = dict(v)
        if k in frac_keys:
            t[k] = {'ft': [0.0, 0.0, 0.0], 'fn': v['fn'], 'hist': v['hist'], 'flag': v['flag']}
    return t


def main(argv):
    o_path, t_path = argv[1], argv[2]
    so, o = read_pairs(o_path)
    st, t = read_pairs(t_path)
    s = stats(o, t)
    print('ref', o_path.split('run40000/')[-1], 'step', so, '| test', t_path.split('run40000/')[-1], 'step', st)
    print('  ', s)
    # 판별력: 기준 쪽 |shear| > 0 몫 · Ft 0 아닌 몫
    nz_ft = sum(1 for v in o.values() if norm(v['ft']) > 0)
    nz_sh = sum(1 for v in o.values() if norm(v['hist'][:3]) > 0)
    print('   ref pairs', len(o), '|Ft|>0', nz_ft, '|shear|>0', nz_sh, 'flag1', sum(v['flag'] for v in o.values()))
    # 반례 1: 시험이 shear 를 모두 잃음 (Ft ~ 0 근사)
    s0 = stats(o, hist_zero(o))
    print('   [loss-all approx Ft=0]', 'reset_frac', round(s0['reset_frac'], 4), 'r_median', s0['r_median'])
    # 반례 2: 주기 표지 1 쌍 (경계 쌍) 만 이력 잃음
    keys = {k for k, v in o.items() if v['flag'] == 1}
    s1 = stats(o, subset_zero(t, keys) if True else t)
    print('   [loss flag1 only n=%d]' % len(keys), 'reset_frac', round(s1['reset_frac'], 4), 'r_median', s1['r_median'])


if __name__ == '__main__':
    main(sys.argv)
