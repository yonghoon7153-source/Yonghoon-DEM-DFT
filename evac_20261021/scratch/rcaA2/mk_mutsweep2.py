D = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/'
src = open(D + 'mutsweep.py', encoding='utf-8').read()
head, rest = src.split('\nMUTS = [', 1)
body, tail = rest.split('\n]\n', 1)
ns = {}
exec('MUTS = [' + body + '\n]\n', {'CJ': 'carbon_junction.py', 'CW': 'ca_ext_cjunc.py', 'S0': 'ca_s0_census.py', 'S3': 'step3_sigma.py'}, ns)
keep = {'M10': 'KINK,RCA03,SELFD,REC,CEN', 'M12': 'RING', 'M27': 'CEN,KINK-R,RCA03,QD,QC', 'M19': 'SELFD,RCA03,KINK,RING,CEN',
        'M25': 't_plan_commit', 'M26': 'RING'}
sel = []
for m in ns['MUTS']:
    k = m[0].split()[0]
    if k in keep:
        sel.append((m[0], m[1], m[2], m[3], m[4], keep[k]))
new = head + '\nMUTS = ' + repr(sel) + '\n' + tail
new = new.replace("D + 'logs/mutsweep.json'", "D + 'logs/mutsweep2.json'")
open(D + 'mutsweep2.py', 'w', encoding='utf-8').write(new)
print(len(sel))
