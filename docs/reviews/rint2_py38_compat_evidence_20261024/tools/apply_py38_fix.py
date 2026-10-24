"""Python 3.8 호환 수정 (사본에 적용 · 결과 확인용).  Usage: python3 apply_py38_fix.py TREE"""
import sys, pathlib
T = pathlib.Path(sys.argv[1]) / 'scripts'


def rep(rel, old, new, count=1):
    p = T / rel
    s = p.read_text(encoding='utf-8')
    n = s.count(old)
    if n != count:
        raise SystemExit(f'{rel}: 기대 {count} 곳 · 실제 {n} 곳 — {old[:60]!r}')
    p.write_text(s.replace(old, new), encoding='utf-8')
    print(f'  ✓ {rel} ({count})')


# ① ptfe_face_alpha — dict-union
rep('ptfe_face_alpha.py',
    "    return {k: caps[k] for k in ('n_paths', 'n_pieces', 'n_point_pieces', 'n_segments', 'volume_um3')} | {\n"
    "        'dia_classes': dict(caps['dia_classes']), 'volume_basis': VOLUME_BASIS}\n",
    "    #  ⚠ dict-union `|` 금지 — kgy dem-venv = Python 3.8.10 (`|` 는 3.9+ · 10-24 kgy S0 단계 1 이 여기서 TypeError 로 멈췄다)\n"
    "    return {**{k: caps[k] for k in ('n_paths', 'n_pieces', 'n_point_pieces', 'n_segments', 'volume_um3')},\n"
    "            'dia_classes': dict(caps['dia_classes']), 'volume_basis': VOLUME_BASIS}\n")

# ② ca_ext_svcf — math.nextafter (3.9+) → _nextafter (3.9+ = math.nextafter 그대로 · 3.8 = IEEE 754 비트 한 칸)
rep('ca_ext_svcf.py', 'import math\nimport numbers\nimport sys\nfrom fractions import Fraction\n',
    'import math\nimport numbers\nimport struct\nimport sys\nfrom fractions import Fraction\n')
rep('ca_ext_svcf.py', 'def _div_dir(', '''def _nextafter(x, toward):
    """x 다음의 float (toward 쪽) — `math.nextafter` 와 같은 값.  `math.nextafter` 는 3.9+ 이고 kgy dem-venv 는 Python 3.8.10 이다
    (10-24 실측) → 3.8 에서는 IEEE 754 비트 한 칸으로 셈한다 (NaN · ±0 · ±inf · 부호 규칙 = C99 nextafter)."""
    f = getattr(math, 'nextafter', None)
    if f is not None:
        return f(x, toward)
    x, toward = float(x), float(toward)
    if math.isnan(x) or math.isnan(toward):
        return x + toward
    if x == toward:
        return toward
    if x == 0.0:
        return math.copysign(5e-324, toward)
    n = struct.unpack('<q', struct.pack('<d', x))[0]
    n += 1 if (toward > x) == (x > 0.0) else -1
    return struct.unpack('<d', struct.pack('<q', n))[0]


def _div_dir(''')
rep('ca_ext_svcf.py', '        f = math.nextafter(f, math.inf)\n', '        f = _nextafter(f, math.inf)\n')
rep('ca_ext_svcf.py', '        f = math.nextafter(f, -math.inf)\n', '        f = _nextafter(f, -math.inf)\n')

# ③ 시험 파일 — 시험의 기대값은 모듈 함수를 쓰지 않는다 (numpy 의 IEEE nextafter · 독립 구현)
NX = ("#: math.nextafter = 3.9+ (kgy dem-venv = Python 3.8.10 · 10-24) → numpy 의 IEEE nextafter (같은 값 · 모듈 구현과 독립)\n"
      "_nextafter = getattr(math, 'nextafter', None) or (lambda x, y: float(np.nextafter(x, y)))\n")
rep('test_carbon_junction.py', 'math.nextafter(', '_nextafter(', count=4)
rep('test_carbon_junction.py', 'def _qd6_floor(q):', NX + '\n\ndef _qd6_floor(q):')
rep('test_ca_ext_b6.py', 'math.nextafter(', '_nextafter(', count=2)
rep('test_step3_target_cert.py', 'math.nextafter(', '_nextafter(', count=1)

# ③-b test_ca_ext_b6 (math 는 함수 안에서 import · numpy 는 모듈 머리) · test_step3_target_cert
rep('test_ca_ext_b6.py', 'import numpy as np\n', 'import numpy as np\n\n' + NX.replace("getattr(math, 'nextafter', None)", "getattr(__import__('math'), 'nextafter', None)"))
rep('test_step3_target_cert.py', 'import numpy as np\n', 'import numpy as np\n\n' + NX)
#  dict-union 다섯 곳 → {**a, **b}
rep('test_step3_target_cert.py',
    "{k: cs.get(k) for k in ('status', 'pass_d', 'target_lo', 'target_hi')} | {'G*': float(Gs)})",
    "{**{k: cs.get(k) for k in ('status', 'pass_d', 'target_lo', 'target_hi')}, 'G*': float(Gs)})")
rep('test_step3_target_cert.py',
    "{k: c.get(k) for k in ('status', 'pass_d', 'target_lo', 'target_hi')} | {'G*': float(Gs)})",
    "{**{k: c.get(k) for k in ('status', 'pass_d', 'target_lo', 'target_hi')}, 'G*': float(Gs)})")
rep('test_step3_target_cert.py',
    "{k: cb.get(k) for k in ('pass_d', 'target_why', 'target_lo', 'target_hi')} | {'G*': float(Gs)})",
    "{**{k: cb.get(k) for k in ('pass_d', 'target_why', 'target_lo', 'target_hi')}, 'G*': float(Gs)})")
rep('test_step3_target_cert.py', "out[which] = _decisions(c) | {'sigma_hex'", "out[which] = {**_decisions(c), 'sigma_hex'")
rep('test_step3_target_cert.py', "out[f'probe_{variant}_{rt:.0e}'] = _decisions(c) | {'sigma_hex'", "out[f'probe_{variant}_{rt:.0e}'] = {**_decisions(c), 'sigma_hex'")

# ③-c test_rint_r_chain (numpy 없이 뜬다 · RR 은 main 에서) — 3.8 이면 SV 모듈의 같은 함수
rep('test_rint_r_chain.py', 'math.nextafter(', '_nextafter(', count=6)
rep('test_rint_r_chain.py', "RR = None                                                # 사슬 모듈",
    '''def _nextafter(x, toward):
    """math.nextafter (3.9+) — kgy dem-venv = Python 3.8.10 (10-24) 이면 SV 모듈의 같은 함수 (`ca_ext_svcf._nextafter`)."""
    f = getattr(math, 'nextafter', None)
    if f is not None:
        return f(x, toward)
    import ca_ext_svcf
    return ca_ext_svcf._nextafter(x, toward)


RR = None                                                # 사슬 모듈''')

# ④ 시험 심 — venv 의 python 은 심볼릭 링크 · realpath 는 venv 밖 (site-packages 없음) 으로 나간다 → abspath
rep('test_ca_ext_runner.py', "f.write(SHIM.replace('__REAL__', os.path.realpath(sys.executable)))",
    "f.write(SHIM.replace('__REAL__', os.path.abspath(sys.executable)))   # realpath = venv 밖 (kgy dem-venv · 10-24)")
rep('test_rint_r_chain_e2e.py', "f.write(TR.SHIM.replace('__REAL__', os.path.realpath(sys.executable)))",
    "f.write(TR.SHIM.replace('__REAL__', os.path.abspath(sys.executable)))   # realpath = venv 밖 (kgy dem-venv · 10-24)")
print('done')
