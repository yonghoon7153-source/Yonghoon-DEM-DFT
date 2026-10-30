# replay the pre-attack review's saved attack decks (f01rev/<tag>_main|_resume.liggghts) through the plain CLI
#   bash <tool> -C <main> <resume> <ckpt> <S0> <workdir>
# = f01rev/repro_all.py with the tool path as an argument (decks read-only from f01rev · temp dirs in f01r2/tmp)
#   + A1as · A2as · A7s · C1 (the review's after_settling / synthetic variants saved next to them)
import os, subprocess, tempfile, shutil, hashlib, sys
TOOL = os.path.abspath(sys.argv[1])
SP = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01rev'
TMP = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01r2/tmp'
D2K = ('restart_kg50_d2_b50/restart_settling_20001.bin', '20001')
CK50 = ('restart_kg50_d07_b50/restart_after_settling.bin', '200001')
rows = [('A1', D2K, 'R1'), ('A2', D2K, 'R1'), ('A2p', D2K, 'R1'), ('A1as', CK50, 'R1'), ('A2as', CK50, 'R1'),
        ('A3', D2K, 'R2'), ('A4', D2K, 'R2'), ('A5', D2K, 'R2'),
        ('A9', D2K, 'R3'), ('A10', D2K, 'R3'), ('A11', D2K, 'R3'),
        ('A8', D2K, 'R4'),
        ('A7', CK50, 'R5'), ('A7s', ('restart_after_settling.bin', '100'), 'R5'), ('C1', ('restart_after_settling.bin', '100'), 'R5')]
os.makedirs(TMP, exist_ok=True)
print('tool sha256', hashlib.sha256(open(TOOL, 'rb').read()).hexdigest())
for tag, (ck, s0), r in rows:
    m, rr = os.path.join(SP, tag + '_main.liggghts'), os.path.join(SP, tag + '_resume.liggghts')
    w = tempfile.mkdtemp(prefix='rp_', dir=TMP)
    try:
        p = subprocess.run(['bash', TOOL, '-C', m, rr, ck, s0, w], capture_output=True, text=True)
        last = [l for l in p.stdout.splitlines() if '재개 덱 정적 대조:' in l]
        first = [l for l in p.stdout.splitlines() if l.startswith('  ✗ ')]
        print('%-4s %-3s rc=%d  %s   [main %s · resume %s]' % (tag, r, p.returncode, last[-1].strip() if last else '?',
              hashlib.sha256(open(m, 'rb').read()).hexdigest()[:12], hashlib.sha256(open(rr, 'rb').read()).hexdigest()[:12]))
        for l in first[:2]:
            print('        ' + l.strip()[:230])
    finally:
        shutil.rmtree(w, ignore_errors=True)
