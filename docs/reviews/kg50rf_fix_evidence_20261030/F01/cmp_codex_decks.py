"""시험 V2–V5 덱 ↔ Codex 사례 덱 대조 (바이트 · \\r 뺀 글) — 시험 모듈의 덱 만들기를 그대로 따라 한다 (Codex 파일 = 읽기만).
   python3 -I cmp_codex_decks.py <작업 트리> <Codex cases 폴더>"""
import hashlib
import os
import sys

REPO, CASES = sys.argv[1:3]
D2D = os.path.join(REPO, 'docs/data/kg50_resume_tests_20261027/d2_main_1028_0942')
d2m = open(os.path.join(D2D, 'input_kg50_d2_b50.liggghts'), encoding='utf-8').read()
d2r = open(os.path.join(D2D, 'input_kg50_d2_b50_r4.liggghts'), encoding='utf-8').read()
FG = 'fix gravi all gravity 98.1 vector 0.0 0.0 -1.0\n'
GP = 'fix gravi all gravity ${g_probe} vector 0.0 0.0 -1.0\n'


def gv(*xs):
    return ''.join(GP if x == 'FIX' else 'variable g_probe equal %s\n' % x for x in xs)


def d2(mrep, rrep, old=FG):
    return d2m.replace(old, mrep), d2r.replace(old, rrep)


TDROP_M = ('units si\r\nvariable dt equal 1e-6\r\nvariable dt equal 2e-6\r\ntimestep ${dt}\r\nvariable dt equal 1e-6\r\n'
           'restart 10 restart_settling_*.bin\r\nrun 100\r\nprint "done"\r\n')
TDROP_R = ('units si\r\nread_restart restart_settling_50.bin\r\nvariable dt equal 1e-6\r\ntimestep ${dt}\r\nvariable dt equal 1e-6\r\n'
           'restart 10 restart_settling_*.bin\r\nrun 50\r\nprint "done"\r\n')
TEAG_M = 'units si\r\nvariable dt equal 1e-6*(step+1)\r\ntimestep ${dt}\r\nrestart 10 restart_settling_*.bin\r\nrun 100\r\nprint "done"\r\n'
TEAG_R = ('units si\r\nread_restart restart_settling_50.bin\r\nvariable dt equal 1e-6*(step+1)\r\ntimestep ${dt}\r\n'
          'restart 10 restart_settling_*.bin\r\nrun 50\r\nprint "done"\r\n')
rows = (('V2', 'd2_drop_intermediate_variable_definition', d2(gv('98.1', '196.2', 'FIX', '98.1'), gv('98.1', 'FIX', '98.1'))),
        ('V3', 'd2_runtime_dependent_eager_variable', d2(gv('98.1*(step+1)', 'FIX'), gv('98.1*(step+1)', 'FIX'))),
        ('V4', 'drop_intermediate_variable_definition', (TDROP_M, TDROP_R)),
        ('V5', 'runtime_dependent_eager_variable', (TEAG_M, TEAG_R)),
        ('V1', 'd2_received_baseline', (d2m, d2r)))
for tag, case, (mt, rt) in rows:
    for side, ours in (('main', mt), ('resume', rt)):
        theirs = open(os.path.join(CASES, case, side + '.liggghts'), 'rb').read()
        ob = ours.encode('utf-8')
        print('%s %-42s %-6s 바이트 같음 %-5s · \\r 뺀 글 같음 %-5s · sha256 앞 16 우리 %s · Codex %s' % (
            tag, case, side, ob == theirs, ob.replace(b'\r', b'') == theirs.replace(b'\r', b''),
            hashlib.sha256(ob).hexdigest()[:16], hashlib.sha256(theirs).hexdigest()[:16]))
