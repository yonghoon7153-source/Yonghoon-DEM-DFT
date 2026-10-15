"""시험 먼저 기록 — v3.3 검사 (`build_seminar_v33.selftest_v33` · `make_seminar_figs_v33.check_fig_files`) 를
Codex 가 받은 v3.2 덱 (sha256 1b6988f3…) 과 v3.2 그림 F_p4 (svg · csv) 에 돌려 실패 목록을 모은다 (assert 대신 수집).
리포 · 덱은 읽기만 한다.  v3.2 덱을 '비교 v3.2' 자리에도 넣는다 (바뀌지 않을 장 = 자기 자신과 같음 · 바뀔 장의 고침 = 아직 없음).

python3 testfirst_v33.py <repo> <v3.2 deck.pptx> <v3.1 deck.pptx> <eq deck.pptx> <out.json>
(`-I` 없이 — 그림 검사가 matplotlib 를 부르고, 이 환경의 matplotlib 의존 (dateutil) 이 사용자 site-packages 에 있다)
"""
import hashlib
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

repo, deck32, deck31, eq, out = (Path(a).resolve() for a in sys.argv[1:6])
sem = repo / 'docs/seminar_20261013'
figs = sem / 'figs_v3'
sys.path.insert(0, str(sem))
sys.path.insert(0, str(figs))


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


gen = load(sem / 'build_seminar_v33.py', 'build_seminar_v33')
fm = load(figs / 'make_seminar_figs_v33.py', 'make_seminar_figs_v33')
C = gen.selftest_v33(deck32, repo, figs, deck32, deck31, eq)
fails = C.failed
fig_fails = fm.check_fig_files(figs / 'F_p4.svg', figs / 'F_p4.csv', figs / 'F_p4.svg', figs / 'F_p4.csv')
groups = Counter(n.split(' ')[0] for n, _ in fails)
rec = dict(
    purpose='v3.3 checks run BEFORE the v3.3 build / figure existed: on the Codex-reviewed v3.2 deck and the v3.2 F_p4 figure',
    inputs={'v3.2 deck': sha(deck32), 'v3.1 deck (A5 base)': sha(deck31), 'equation deck (A8)': sha(eq),
            'F_p4.svg (v3.2)': sha(figs / 'F_p4.svg'), 'F_p4.csv (v3.2)': sha(figs / 'F_p4.csv')},
    deck=dict(label=deck32.name, total=len(C.items), failed=len(fails), failed_by_group=dict(sorted(groups.items())),
              failures=[dict(check=n, detail=d) for n, d in fails]),
    figure=dict(candidate='F_p4 (v3.2) checked as if it were F_p4_v33', failed=len(fig_fails), failures=fig_fails))
Path(out).write_text(json.dumps(rec, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(f'deck checks: {len(C.items)} · failed {len(fails)} · by group {dict(sorted(groups.items()))}')
for n, d in fails:
    print(f'  ✗ {n}  {d[:120]}')
print(f'figure checks on v3.2 F_p4: failed {len(fig_fails)}')
for f in fig_fails:
    print(f'  ✗ {f}')
