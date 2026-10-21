"""본 가지 문서가 인용한 커밋 중 '로컬 전용' (원격 어디서도 도달 불가) 인 것을 찾는다 — 읽기만."""
import re, subprocess, sys
root = sys.argv[1]
def git(*a):
    return subprocess.run(['git', '-C', root, *a], capture_output=True, text=True).stdout
local_only = set(git('rev-list', '--all', '--not', '--remotes').split())
remote = set(git('rev-list', '--remotes').split())
files = [f for f in git('ls-files').split('\n') if f.endswith(('.md', '.json', '.tsv', '.txt', '.py', '.sh', '.yml', '.csv'))]
rx = re.compile(r'`([0-9a-f]{7,40})`')
hits = {}
for f in files:
    try:
        s = open(f'{root}/{f}', encoding='utf-8', errors='replace').read()
    except (IsADirectoryError, FileNotFoundError):
        continue
    for i, ln in enumerate(s.split('\n'), 1):
        for tok in rx.findall(ln):
            lo = [c for c in local_only if c.startswith(tok)]
            if lo and not any(c.startswith(tok) for c in remote):
                hits.setdefault(tok, []).append(f'{f}:{i}')
for tok, where in sorted(hits.items()):
    br = git('branch', '--contains', tok).split()
    print(tok, len(where), 'refs', '| e.g.', ', '.join(where[:4]), '| branch', ' '.join(b for b in br if b != '+' and b != '*')[:80])
print('TOTAL tokens', len(hits))
