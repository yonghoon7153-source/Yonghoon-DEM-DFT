"""Q3 (나) 사전 공격 — 변이 시험 (도구 사본에 한 곳만 바꿔 QB 묶음을 돌린다 · 도구 원본은 안 건드림).
usage: python3 docs/reviews/kg50_q3b_preattack_20261103/mut.py <출력 폴더> [변이 이름 …]"""
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
src = open(os.path.join(ROOT, 'scripts/resume_ckpt.sh'), encoding='utf-8').read()
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
MUTS = {
    # 순서 고침 끔 (perm = 그대로)
    'M1_no_reorder': ("    slots = [i for i in range(len(P)) if key[i] is not None]\n",
                      "    slots = []\n"),
    # 같은 명령 n 번 → 전부 본 덱 마지막 자리 하나로
    'M2_dups_all_last': ("            j = len(c) - len(mem) + k\n", "            j = len(c) - 1\n"),
    # 같은 명령 n 번 → 본 덱 처음 n 자리 (마지막 n 자리 대신)
    'M3_dups_first_n': ("            j = len(c) - len(mem) + k\n", "            j = k if k < len(c) else -1\n"),
    # 순서 고침의 짝 맞추기만 글자 같음 (판 메시 file 이름 규칙 · mkdir -p 규칙 끔 · 정적 대조는 그대로 prep_eq)
    'M4_reorder_exact_only': ("    cand = [tuple(x for x, m in enumerate(Mp) if prep_eq(l, m)) for l in P]\n",
                              "    cand = [tuple(x for x, m in enumerate(Mp) if l == m) for l in P]\n"),
    # 안정 정렬 깨기 (같은 키 = 역순) — 같은 키는 생기지 않아야 (자리 하나에 한 명령)
    'M6_ties_reversed': ("    for sl, i in zip(slots, sorted(slots, key=lambda i: key[i])):\n",
                         "    for sl, i in zip(slots, sorted(slots, key=lambda i: (key[i], -i))):\n"),
    # 재개 덱에 본 덱보다 많은 같은 명령 (n > m) — 남는 앞 칸도 음수 번호로 본 덱 자리를 받게 (제자리 규칙 깨기)
    'M7_extra_copies_wrap': ("            key[i] = c[j] if j >= 0 else None\n", "            key[i] = c[j]\n"),
}
names = sys.argv[2:] or list(MUTS)
for n in names:
    a, b = MUTS[n]
    assert src.count(a) == 1, (n, src.count(a))
    p = os.path.join(OUT, 'mut_%s.sh' % n)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(src.replace(a, b))
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'scripts/test_resume_ckpt.py'), '--only', 'QB', '--script', p],
                       capture_output=True, text=True, timeout=900, cwd=ROOT)
    lines = r.stdout.strip().splitlines()
    print('==', n, '→', lines[-1] if lines else r.stderr[-300:])
    for l in lines:
        if l.startswith('FAIL'):
            print('    ', l[:120])
