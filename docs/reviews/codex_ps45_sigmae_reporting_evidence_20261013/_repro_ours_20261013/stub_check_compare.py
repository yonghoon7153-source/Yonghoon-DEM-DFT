"""반례 먼저 확인 — compare_probe_outputs 의 selftest 를 엉터리 판정기 둘에 돌린다 (둘 다 FAIL 이 나야 시험이 판별력이 있다)."""
import importlib.util
import math
import sys

spec = importlib.util.spec_from_file_location('cpo', sys.argv[1])
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

print('— 실제 판정기')
rc_real = m._selftest()

orig_classify, orig_same = m.classify, m._same
print('— 스텁 A: 모든 차이를 같음으로 (accept-all)')
m.classify = lambda k, a, b: 'equal'
rc_a = m._selftest()
m.classify = orig_classify

print('— 스텁 B: 옛 대조기 꼴 (파이썬 == · env 범주 없음 · 경로는 한쪽만 꼴이어도 path)')


def naive_same(va, vb):
    if isinstance(va, float) and isinstance(vb, float) and math.isnan(va) and math.isnan(vb):
        return True
    return va == vb


def naive_classify(key, va, vb):
    if naive_same(va, vb):
        return 'equal'
    if isinstance(va, str) and isinstance(vb, str) and (m.PATHY.search(va) or m.PATHY.search(vb)):
        return 'path'
    if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
        if abs(va - vb) <= 1e-12 * max(abs(va), abs(vb), 1e-300):
            return 'float'
    return 'other'


m._same, m.classify = naive_same, naive_classify
rc_b = m._selftest()
m._same, m.classify = orig_same, orig_classify
print('rc real / A / B =', rc_real, rc_a, rc_b)
sys.exit(0 if (rc_real == 0 and rc_a == 1 and rc_b == 1) else 1)
