# R3 줄 읽기 대조: 새 deck() (고친 도구) ↔ 리뷰어 LIGGGHTS 흉내 (f01rev/a12_ligread.py 의 lig_commands · 고정판 Input::file()/parse()) ↔ 옛 deck()
#   대상 = 리포 kg50 덱 151 (docs/data/kg50_* · docs/reviews/codex_kg50*) + 리뷰어 R3 반례 덱 셋 (A9 재개 · A10 재개 · A11 본)
#   usage: python3 -I reader_diff.py <worktree> <새 도구> <옛 도구>
import glob, os, re, sys
WT, NEW, OLD = (os.path.abspath(x) for x in sys.argv[1:4])
REV = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01rev'


def load(tool):
    s = open(tool, encoding='utf-8').read()
    a = s.index("deckcheck(){ python3 - \"$@\" <<'PY'\n") + len("deckcheck(){ python3 - \"$@\" <<'PY'\n")
    ns = {'__name__': 'deck'}
    exec(compile(s[a:s.index("\nif len(sys.argv) == 3 and sys.argv[1] == '--strip-comments':", a)], tool, 'exec'), ns)
    return ns


src = open(os.path.join(REV, 'a12_ligread.py'), encoding='utf-8').read()
lns = {'__name__': 'lig', '__file__': os.path.join(REV, 'a12_ligread.py')}
exec(compile(src[:src.index('\ndef deck_of(')], 'a12_ligread', 'exec'), lns)
lig = lns['lig_commands']
new, old = load(NEW), load(OLD)
os.chdir(WT)
fs = sorted(set(glob.glob('docs/data/kg50_*/**/*.liggghts', recursive=True) + glob.glob('docs/reviews/codex_kg50*/**/*.liggghts', recursive=True)))
fs += [os.path.join(REV, x) for x in ('A9_resume.liggghts', 'A10_resume.liggghts', 'A11_main.liggghts')]
cnt = dict(files=0, new_eq_lig=0, new_rejects=0, new_ne_lig=0, old_eq_lig=0, old_ne_lig=0, new_eq_old=0)
for f in fs:
    cnt['files'] += 1
    L = lig(f)
    O = old['deck'](f)
    try:
        N = new['deck'](f)
    except new['DeckRead'] as e:
        cnt['new_rejects'] += 1
        print('새 판 거부 %-60s %s · 옛 deck() = LIGGGHTS %s' % (os.path.relpath(f, WT) if f.startswith(WT) else os.path.basename(f), str(e)[:90], O == L))
        cnt['old_eq_lig' if O == L else 'old_ne_lig'] += 1
        continue
    cnt['new_eq_lig' if N == L else 'new_ne_lig'] += 1
    cnt['old_eq_lig' if O == L else 'old_ne_lig'] += 1
    cnt['new_eq_old'] += N == O
    if N != L or O != L:
        print('다름 %-60s 새=LIGGGHTS %s · 옛=LIGGGHTS %s · 새 %d 명령 · LIGGGHTS %d · 옛 %d' % (
            os.path.relpath(f, WT) if f.startswith(WT) else os.path.basename(f), N == L, O == L, len(N), len(L), len(O)))
print(cnt)
