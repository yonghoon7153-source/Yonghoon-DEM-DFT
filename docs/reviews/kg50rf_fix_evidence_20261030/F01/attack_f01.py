"""KG50R-F01 고친 도구 자기 공격 — 작은 덱 짝 (합성 · 체크포인트 restart_settling_50.bin · S0 50) 에 -C.
   기대 = 'rej' (rc 1) · 'acc' (rc 0).  python3 -I attack_f01.py <도구> <작업 폴더>"""
import os
import subprocess
import sys

tool, work = sys.argv[1:3]
os.makedirs(work, exist_ok=True)
TAIL_M = 'restart 10 restart_settling_*.bin\nrun 100\nprint "done"\n'
TAIL_R = 'restart 10 restart_settling_*.bin\nrun 50\nprint "done"\n'


def pair(mpre, rpre):
    return 'units si\n' + mpre + TAIL_M, 'units si\nread_restart restart_settling_50.bin\n' + rpre + TAIL_R


C = [
    ('A1 b = ${a} 정의 앞 a 중간 정의 뺌 (뒤 구간 print 가 씀)', 'rej',
     pair('variable a equal 1\nvariable a equal 2\nvariable b equal ${a}\nvariable a equal 1\n',
          'variable a equal 1\nvariable b equal ${a}\nvariable a equal 1\n')),
    ('A3 b = ${a}*v_c · c 중간 정의 뺌 · timestep ${b}', 'rej',
     pair('variable a equal 2\nvariable b equal ${a}*v_c\nvariable c equal 3\nvariable c equal 4\ntimestep ${b}\nvariable c equal 3\n',
          'variable a equal 2\nvariable b equal ${a}*v_c\nvariable c equal 3\ntimestep ${b}\nvariable c equal 3\n')),
    ('A4 같은 꼴 · c 다시 정의가 timestep 뒤 (두 덱 같음)', 'acc',
     pair('variable a equal 2\nvariable b equal ${a}*v_c\nvariable c equal 3\ntimestep ${b}\nvariable c equal 4\n',
          'variable a equal 2\nvariable b equal ${a}*v_c\nvariable c equal 3\ntimestep ${b}\nvariable c equal 4\n')),
    ('A5 따옴표 안 ${a} 를 담은 equal 을 ${b} 로 씀', 'rej',
     pair('variable a equal 2\nvariable b equal "${a}*2"\ntimestep ${b}\n', 'variable a equal 2\nvariable b equal "${a}*2"\ntimestep ${b}\n')),
    ('A7 timestep ${dt} 가 본 덱에 둘 (끝 = dt 2e-6) · 재개 덱 하나 (앞 것 자리)', 'rej',
     pair('variable dt equal 1e-6\ntimestep ${dt}\nvariable dt equal 2e-6\ntimestep ${dt}\n',
          'variable dt equal 1e-6\ntimestep ${dt}\nvariable dt equal 2e-6\n')),
    ('A17 fix ${g} → unfix → g 바꿈 → fix ${g} (재개 덱 = 앞 fix 만)', 'rej',
     pair('variable g equal 98.1\nfix gr all gravity ${g} vector 0 0 -1\nunfix gr\nvariable g equal 196.2\nfix gr all gravity ${g} vector 0 0 -1\n',
          'variable g equal 98.1\nfix gr all gravity ${g} vector 0 0 -1\n')),
    ('A27 g 98.1 → delete → 196.2 → fix ${g} · 재개 덱 = g 98.1 · fix', 'rej',
     pair('variable g equal 98.1\nvariable g delete\nvariable g equal 196.2\nfix gr all gravity ${g} vector 0 0 -1\n',
          'variable g equal 98.1\nfix gr all gravity ${g} vector 0 0 -1\n')),
    ('A31 fix 이름 자리 치환 fix ${f} · f string 중간 정의 뺌', 'rej',
     pair('variable f string ga\nvariable f string gb\nfix ${f} all gravity 9.8 vector 0 0 -1\nvariable f string ga\n',
          'variable f string ga\nfix ${f} all gravity 9.8 vector 0 0 -1\nvariable f string ga\n')),
    # 10-30 (KG50R-F01): A32 이름표 고침 — 첫 판 이름표 "단일 따옴표 안 겹따옴표 · 그 뒤 $" 는 내용 (따옴표 없음) 과 달랐다 · 따옴표 뒤집기 = A37–A40
    ('A32 대조군 — 상수 하나 (fix ${g} · 두 덱 같은 글자 · 값 같음 · 따옴표 없음)', 'acc',
     pair('variable g equal 9.8\nfix gr all gravity ${g} vector 0 0 -1\n', 'variable g equal 9.8\nfix gr all gravity ${g} vector 0 0 -1\n')),
    ('A33 neigh_modify 묶음 ${n} 중간 정의 뺌', 'rej',
     pair('variable n equal 100\nvariable n equal 200\nneigh_modify one ${n}\nvariable n equal 100\n',
          'variable n equal 100\nneigh_modify one ${n}\nvariable n equal 100\n')),
    ('A34 region ${x} 중간 정의 뺌', 'rej',
     pair('variable x equal 1\nvariable x equal 2\nregion rb block 0 ${x} 0 1 0 1\nvariable x equal 1\n',
          'variable x equal 1\nregion rb block 0 ${x} 0 1 0 1\nvariable x equal 1\n')),
    ('A35 group type ${t} 중간 정의 뺌 (상태 표 밖 명령 · ① 만)', 'rej',
     pair('variable t equal 1\nvariable t equal 2\ngroup g1 type ${t}\nvariable t equal 1\n',
          'variable t equal 1\ngroup g1 type ${t}\nvariable t equal 1\n')),
    ('A36 v_ 가 가리키는 변수가 그 자리에 없음 (재개 덱 · 본 덱은 있음)', 'rej',
     pair('variable c equal 3\nvariable b equal v_c*2\ntimestep ${b}\n', 'variable b equal v_c*2\ntimestep ${b}\nvariable c equal 3\n')),
    # 따옴표 뒤집기 — LIGGGHTS Input::substitute 는 " · ' 를 따로 뒤집고 둘 다 밖일 때의 $ 만 치환 (고정판 input.cpp)
    #   A37 · A39 = 따옴표 안 다른 따옴표 하나 → 그 뒤 ${x} 는 LIGGGHTS 가 치환하지 않음 (글 그대로 · 두 덱 같은 글자) → 받음
    #   A38 · A40 = 다른 따옴표 둘 → 그 뒤 ${x} 를 치환 · x 중간 정의를 뺀 재개 덱 → 값 다름 → 거부
    ('A37 \'…"…\' (겹따옴표 하나) 뒤 ${x} — LIGGGHTS 치환 안 함 · x 중간 정의 뺌', 'acc',
     pair('variable x equal 1\nvariable x equal 2\nfix pr all print 100 \'say"hi\' title ${x}\nvariable x equal 1\n',
          'variable x equal 1\nfix pr all print 100 \'say"hi\' title ${x}\nvariable x equal 1\n')),
    ('A38 \'…"…"…\' (겹따옴표 둘) 뒤 ${x} — LIGGGHTS 치환 · x 중간 정의 뺌', 'rej',
     pair('variable x equal 1\nvariable x equal 2\nfix pr all print 100 \'say"hi"\' title ${x}\nvariable x equal 1\n',
          'variable x equal 1\nfix pr all print 100 \'say"hi"\' title ${x}\nvariable x equal 1\n')),
    ('A39 "…\'…" (홑따옴표 하나) 뒤 ${x} — LIGGGHTS 치환 안 함 · x 중간 정의 뺌', 'acc',
     pair('variable x equal 1\nvariable x equal 2\nfix pr all print 100 "it\'s" title ${x}\nvariable x equal 1\n',
          'variable x equal 1\nfix pr all print 100 "it\'s" title ${x}\nvariable x equal 1\n')),
    ('A40 "…\'…\'…" (홑따옴표 둘) 뒤 ${x} — LIGGGHTS 치환 · x 중간 정의 뺌', 'rej',
     pair('variable x equal 1\nvariable x equal 2\nfix pr all print 100 "it\'\'s" title ${x}\nvariable x equal 1\n',
          'variable x equal 1\nfix pr all print 100 "it\'\'s" title ${x}\nvariable x equal 1\n')),
]
bad = 0
for tag, want, (m, r) in C:
    mp, rp = os.path.join(work, 'm.liggghts'), os.path.join(work, 'r.liggghts')
    open(mp, 'w').write(m)
    open(rp, 'w').write(r)
    p = subprocess.run(['bash', tool, '-C', mp, rp, 'restart_settling_50.bin', '50', work], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode('utf-8', 'replace').splitlines()
    got = 'acc' if p.returncode == 0 else 'rej'
    ok = got == want
    bad += not ok
    f01 = [l.strip()[:220] for l in out if '✗' in l]
    print('%s %-4s (기대 %s) %s · %s' % ('OK ' if ok else 'BAD', got, want, tag, out[-1].strip() if out else ''))
    for l in f01[:3]:
        print('      ' + l)
print('── 공격 %d · 기대와 다름 %d' % (len(C), bad))
