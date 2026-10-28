# 테스트 전용: gen 이 만든 덱을 작게 (상자 0.02 · H 0.03 · run 짧게 · 판 빠르게) — 구조(마커·run·restart·덤프 간격 비율)는 그대로
import sys, re
for f in sys.argv[2:]:
    t = open(f).read(); ps = sys.argv[1]
    def rep(a, b, n=None):
        global t
        c = t.count(a)
        assert c >= 1 and (n is None or c == n), (f, a, c)
        t = t.replace(a, b)
    rep('region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box', 'region reg_box block 0.0 0.02 0.0 0.02 -0.01 1.0 units box', 1)
    t = re.sub(r'region reg_mix block 0\.0 0\.05 0\.0 0\.05 0\.005 \S+ units box', 'region reg_mix block 0.0 0.02 0.0 0.02 0.005 0.035 units box', t)
    if 'print "====== PHASE 1: SETTLING' in t:
        rep('restart 50000 ', 'restart 500 ', 2)
        assert t.count('run 200000') == 2
        t = t.replace('run 200000', 'run 3000', 1); t = t.replace('run 200000', 'run 2000', 1)   # settle 3000 · stab 2000
        rep('thermo          1000', 'thermo          100', 1); rep('thermo 1000', 'thermo 100', 1)
        rep('mesh/stl 5000', 'mesh/stl 100', 1); rep('custom 5000', 'custom 100', 1)
        rep('    run 5000', '    run 100', 1)
        rep('variable press_speed equal 0.01', f'variable press_speed equal {ps}', 1)
        rep('local 10000', 'local 500', 1)
        rep('run 100000', 'run 1500', 1)
        t = t.replace('vertex 0.05 0.05', 'vertex 0.02 0.02').replace('vertex 0.05 0.0', 'vertex 0.02 0.0').replace('vertex 0.0 0.05', 'vertex 0.0 0.02')
        rep('/0.0025/', '/0.0004/', 1); rep('/ 0.0025 /', '/ 0.0004 /', 1)
    open(f, 'w').write(t)
    print('reduced', f.split('/')[-1], 'runs:', re.findall(r'^\s*run\s+(\d+)', t, re.M))
