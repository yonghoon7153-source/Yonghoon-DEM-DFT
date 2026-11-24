# WSL30 follow-up: classify the two residues seen in check_wsl30.py (value-blind · read-only).
#   R1 = log.txt lines not found (in order) in log.liggghts      R2 = deck lines not found verbatim in the log.liggghts echo
#   R3 = log.liggghts-only lines that are neither deck lines nor command-like
# Prints only line numbers, the FIRST WORD of a line when it is a plain word (else <num>/<sym>/<blank>), and flags
# (& continuation · # comment · $ variable) — never numbers or text after the first word.  Pattern compared across all 30.
import bisect, os, re
from collections import defaultdict

ROOT = os.path.expanduser(os.environ.get('LHS_ROOT', '~/lhs_local'))
CASES = ['lhs00_%03d' % n for n in range(100, 130)]
CMD = re.compile(r"^\s*(variable|fix|unfix|run|if|jump|label|print|thermo|thermo_style|thermo_modify|dump|undump|dump_modify|"
                 r"include|region|group|compute|uncompute|write_restart|read_restart|restart|neighbor|neigh_modify|timestep|"
                 r"communicate|newton|units|atom_style|atom_modify|boundary|processors|create_box|create_atoms|pair_style|"
                 r"pair_coeff|shell|next|clear|log|echo|set|velocity|delete_atoms|mass|lattice|displace_atoms|"
                 r"soft_particles|hard_particles|modify_timing|reset_timestep)\b")


def lines_of(path):
    with open(path, encoding='utf-8', errors='surrogateescape') as f:
        return [ln.rstrip('\r\n').rstrip() for ln in f.read().splitlines()]


def kind(ln):
    s = ln.strip()
    if not s:
        return '<blank>'
    w = s.split()[0]
    if re.fullmatch(r'[A-Za-z_][A-Za-z_]{0,24}:?', w):
        return w
    if re.fullmatch(r'[-+]?\d[\d.eE+-]*', w):
        return '<num>'
    return '<sym>'


def in_order(small, big):
    pos = defaultdict(list)
    for i, ln in enumerate(big):
        pos[ln].append(i)
    cur, used, miss = -1, set(), []
    for j, ln in enumerate(small):
        lst = pos.get(ln)
        k = bisect.bisect_right(lst, cur) if lst else 0
        if not lst or k == len(lst):
            miss.append(j); continue
        cur = lst[k]; used.add(cur)
    return used, miss


sig, detail = {}, {}
for c in CASES:
    d = os.path.join(ROOT, c)
    lig, txt = lines_of(os.path.join(d, 'log.liggghts')), lines_of(os.path.join(d, 'log.txt'))
    deck = lines_of(os.path.join(d, 'input_%s.liggghts' % c))
    used, miss = in_order(txt, lig)
    ligset = set(lig)
    dset = set(ln for ln in deck if ln.strip())
    r2 = [(i + 1, kind(ln), ('&' if ln.endswith('&') else '') + ('#' if ln.lstrip().startswith('#') else '') + ('$' if '$' in ln else ''))
          for i, ln in enumerate(deck) if ln.strip() and ln not in ligset]
    r1 = [(j + 1, 'head' if j < 60 else ('tail' if j >= len(txt) - 60 else 'mid'), kind(txt[j])) for j in miss]
    r3 = [(i + 1, 'head' if i < 60 else ('tail' if i >= len(lig) - 60 else 'mid'), kind(lig[i])) for i in range(len(lig))
          if i not in used and lig[i] not in dset and not CMD.match(lig[i])]
    sig[c] = (tuple(x[0] for x in r2), tuple((x[1], x[2]) for x in r1), tuple((x[1], x[2]) for x in r3))
    detail[c] = (r2, r1, r3, len(txt), len(lig), len(deck))

r2, r1, r3, nt, nl, nd = detail['lhs00_100']
print('lhs00_100  deck %d 줄 · log.txt %d 줄 · log.liggghts %d 줄' % (nd, nt, nl))
print('R2 덱 줄 (로그 되풀이에 없음) %d:' % len(r2), ' '.join('%d:%s%s' % (a, b, ('[' + f + ']') if f else '') for a, b, f in r2))
print('R1 화면 사본에만 %d:' % len(r1), ' '.join('%d:%s/%s' % x for x in r1))
print('R3 로그에만 (덱 · 명령 아님) %d:' % len(r3), ' '.join('%d:%s/%s' % x for x in r3))
base = sig['lhs00_100']
same = [c for c in CASES if sig[c] == base]
same2 = [c for c in CASES if sig[c][0] == base[0]]
print('패턴이 lhs00_100 과 같은 케이스: 전체 %d/30 · 덱 줄 자리만 %d/30' % (len(same), len(same2)))
diff = [c for c in CASES if sig[c] != base]
for c in diff[:5]:
    a, b, e = sig[c]
    print('  다른 것 %s: R2 %d (자리 같음 %s) · R1 %d (종류 같음 %s) · R3 %d (종류 같음 %s)'
          % (c, len(a), a == base[0], len(b), b == base[1], len(e), e == base[2]))
