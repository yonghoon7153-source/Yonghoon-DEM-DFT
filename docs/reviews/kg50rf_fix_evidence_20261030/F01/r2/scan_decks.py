# scan real kg50 decks: non-ASCII placement vs LIGGGHTS comment rule, '&' continuation forms, control chars
import glob, re, sys, os
WT = sys.argv[1]
os.chdir(WT)
fs = sorted(set(glob.glob('docs/data/kg50_*/**/*.liggghts', recursive=True)
                + glob.glob('docs/reviews/codex_kg50*/**/*.liggghts', recursive=True)))
CWS = b' \t\n\v\f\r'


def lig_lines(data):
    # LIGGGHTS Input::file(): fgets lines; if last non-space char (C isspace) is '&', next line overwrites from that '&'
    phys = data.split(b'\n')
    phys = [p + b'\n' for p in phys[:-1]] + ([phys[-1]] if phys[-1] else [])
    out, line, first = [], b'', None
    for k, p in enumerate(phys):
        if first is None:
            first = k
        line = line + p
        m = len(line) - 1
        while m >= 0 and line[m] in CWS:
            m -= 1
        if m >= 0 and line[m:m + 1] == b'&':
            line = line[:m]
            continue
        out.append((first, k, line))
        line, first = b'', None
    if line:
        out.append((first, len(phys) - 1, line))
    return out


def comment_pos(cmd):
    q = None
    for k in range(len(cmd)):
        ch = cmd[k:k + 1]
        if ch == b'#' and q is None:
            return k
        if q is not None and ch == q:
            q = None
        elif q is None and ch in (b'"', b"'"):
            q = ch
    return -1


tot = dict(files=0, na_lines=0, na_outside_comment=0, amp_cont=0, amp_in_comment=0, amp_nospace=0, ctl=0, cr=0, nbsp=0)
bad = []
for f in fs:
    b = open(f, 'rb').read()
    tot['files'] += 1
    tot['cr'] += b.count(b'\r')
    tot['nbsp'] += b.count(' '.encode())
    for c in b:
        if (c < 32 and c not in (9, 10, 13)) or c == 127:
            tot['ctl'] += 1
    for a, z, cmd in lig_lines(b):
        if z > a:
            tot['amp_cont'] += 1
            # was the '&' itself inside a comment?  (join happens regardless in LIGGGHTS)
            phys = b.split(b'\n')[a]
            cp = comment_pos(phys)
            if cp >= 0:
                tot['amp_in_comment'] += 1
            # no whitespace before '&'?
            st = phys.rstrip(b' \t\r')
            if st.endswith(b'&') and len(st) > 1 and st[-2:-1] not in (b' ', b'\t'):
                tot['amp_nospace'] += 1
                bad.append(('nospace&', f, a + 1, phys[:80]))
        if any(c > 127 for c in cmd):
            tot['na_lines'] += 1
            cp = comment_pos(cmd)
            pre = cmd if cp < 0 else cmd[:cp]
            if any(c > 127 for c in pre):
                tot['na_outside_comment'] += 1
                bad.append(('NA-outside-comment', f, a + 1, cmd[:100]))
print(tot)
for x in bad[:30]:
    print(x)
