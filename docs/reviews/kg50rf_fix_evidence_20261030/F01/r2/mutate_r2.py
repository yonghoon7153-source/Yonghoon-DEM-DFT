# 변이 시험 (10-30 KG50R-F01 2 판 · 사전 공격 R1–R8): 새 관문을 하나씩 약하게 한 도구 사본 → 시험 (--only VP 먼저 · VP 에서 살아남으면 전체)
#   usage: python3 -I mutate_r2.py <도구> <시험> <출력 폴더> [이름,…]
#   사본 = 도구 글에서 한 곳씩 바꿈 (바꿀 글이 정확히 한 번 · 되돌리면 도구와 바이트 같음 = 확인) · 결과 = <출력>/mutation_r2.txt · 로그 <출력>/logs/
import os, re, subprocess, sys, hashlib
TOOL, TEST, OUT = (os.path.abspath(x) for x in sys.argv[1:4])
SEL = sys.argv[4].split(',') if len(sys.argv) > 4 else None
SRC = open(TOOL, encoding='utf-8').read()
TMP = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01r2/tmp'
MUT = [
    ('R1a', 'R1 키 자리 $ 검사 끔', "        if kp:\n            probs.append('%s 상태 표 키 자리에", "        if False:\n            probs.append('%s 상태 표 키 자리에"),
    ('R1b', 'R1 fix 스타일 자리 뺌', "KEYPOS = {'fix': (1, 3),", "KEYPOS = {'fix': (1,),"),
    ('R1c', 'R1 unfix 뺌', "'unfix': (1,), 'fix_modify': (1,),", "'unfix': (), 'fix_modify': (1,),"),
    ('R1d', 'R1 region 뺌', "'region': (1, 2),", "'region': (),"),
    ('R1e', 'R1 pair_coeff 뺌', "'pair_coeff': (1, 2),", "'pair_coeff': (),"),
    ('R1f', 'R1 compute 뺌', "'compute': (1,), 'uncompute'", "'compute': (), 'uncompute'"),
    ('R1g', 'R1 dump 뺌', "'dump': (1,),\n", "'dump': (),\n"),
    ('R1h', 'R1 *_modify 셋 뺌', [("'fix_modify': (1,),", "'fix_modify': (),"), ("'compute_modify': (1,),", "'compute_modify': (),"),
                                  ("'dump_modify': (1,),", "'dump_modify': (),")]),
    ('R1i', 'R1 uncompute · undump 뺌', [("'uncompute': (1,),", "'uncompute': (),"), ("'undump': (1,),", "'undump': (),")]),
    ('R1j', 'R1 variable 이름 뺌', "'variable': (1,)}", "'variable': ()}"),
    ('R2a', 'R2 run every 검사 끔', "            if any((words(c) or [''])[0] not in IFOK for c in cs):", "            if False:"),
    ('R2b', 'R2 run every 안 jump 받음', "            if any((words(c) or [''])[0] not in IFOK for c in cs):",
     "            if any((words(c) or [''])[0] not in IFOK | {'jump'} for c in cs):"),
    ('R2c', 'R2 partition 검사 끔', "            if (words(part_cmd(l)) or [''])[0] not in IFOK:", "            if False:"),
    ('R2d', 'R2 unsupported 의 partition 안 명령 끔', "        if c == 'partition' and len(cw) > 3:", "        if False:"),
    ('R3a', 'R3 제어 글자 검사 끔', "            if (c < 32 and c != 9 and not (c == 13 and j == len(p) - 1)) or c == 127:", "            if False:"),
    ('R3b', 'R3 \\r 아무 데나 받음', "not (c == 13 and j == len(p) - 1)", "not (c == 13)"),
    ('R3c', 'R3 주석 밖 비 ASCII 받음', "        bad = [x for x in c if x > 127]", "        bad = []"),
    ('R3d', 'R3 주석 규칙 = 옛 규칙 (같은 따옴표만 닫음)', "        elif c in (34, 39):\n            q = c\n    return b",
     "        elif c in (34, 39) and q is None:\n            q = c\n    return b"),
    ('R3e', 'R3 & 이음에 공백 넣음 (옛 규칙)', "                line = full[:m - 1]\n", "                line = full[:m - 1] + b' '\n"),
    ('R3f', 'R3 줄 끝 공백에 NBSP (유니코드 공백 · 옛 rstrip)', "            while m > 0 and full[m - 1] in CWS:",
     "            while m > 0 and (full[m - 1] in CWS or full[m - 1] in (0xa0, 0xc2)):"),
    ('R3g', 'R3 check() 앞 덱 읽기 거부 끔 (도구 오류로 떨어짐)', "        return rd, []\n", "        pass\n"),
    ('R4a', 'R4 print file 검사 끔', "        print_file_reads(R, q, '재개 덱', probs)  # 10-30 사전 공격 R4", "        pass"),
    ('R4b', 'R4 읽는 명령 = 준비 구간 안만', "            for j in range(i + 1, len(L)):\n                wj = words(L[j]) or ['']",
     "            for j in range(i + 1, min(n, len(L))):\n                wj = words(L[j]) or ['']"),
    ('R4c', 'R4 이름에 $ 검사 끔', "                dyn = '$' in t or any(", "                dyn = False and any("),
    ('R5a', 'R5 흐름 줄 검사 끔', "        flow_before_write(M[:pM], probs)          # 10-30 사전 공격 R5", "        pass"),
    ('R5b', 'R5 겹친 명령 안 봄', "        hit = [x[0] for x in [w] + nested(w) if x and x[0] in FLOW5]", "        hit = [x[0] for x in [w] if x and x[0] in FLOW5]"),
    ('R5c', 'R5 clear 뺌', "FLOW5 = {'label', 'jump', 'clear', 'python'}", "FLOW5 = {'label', 'jump', 'python'}"),
    ('R5d', 'R5 python 뺌', "FLOW5 = {'label', 'jump', 'clear', 'python'}", "FLOW5 = {'label', 'jump', 'clear'}"),
    ('R5e', 'R5 label 뺌', "FLOW5 = {'label', 'jump', 'clear', 'python'}", "FLOW5 = {'jump', 'clear', 'python'}"),
    ('R6a', 'R6 있는지 = 치환 전 이름 (옛)', "                same_or_mesh(a, b, W, notes, probs, what, nfx)", "                same_or_mesh(a, b, W, notes, probs, what)"),
    ('R6b', 'R6 펼친 이름 표지 검사 끔', "            elif any(c in nfx for c in (VAL0, VAL1, RT0, RT1)):", "            elif False:"),
    ('R6c', 'R6 뒤 구간 file 이름 $ 검사 끔', "                if '$' in nf or '$' in (mesh_file(b, a) or ''):", "                if False:"),
    ('R6d', 'R6 mesh_file 낱말 = 모든 공백 (옛 split)', "    ta, tb = re.split('[ \\t]+', a.strip(' \\t')), re.split('[ \\t]+', b.strip(' \\t'))",
     "    ta, tb = a.split(), b.split()"),
    ('R7a', 'R7 expand 고리 안 상한 끔', "        if size > XCAP:\n            return None, xcap_why(x)              # 10-30 사전 공격 R7",
     "        if False:\n            return None, xcap_why(x)              # 10-30 사전 공격 R7"),
    ('R7b', 'R7 expand 끝 상한 끔', "    if size > XCAP:\n        return None, xcap_why(x)\n    t = VAL0", "    if False:\n        return None, xcap_why(x)\n    t = VAL0"),
    ('R7c', 'R7 var_env 정의 글 상한 끔', "            if not bad and len(b) > XCAP:", "            if False:"),
    ('R7d', 'R7 expand 상한 둘 다 끔', [("        if size > XCAP:\n            return None, xcap_why(x)              # 10-30 사전 공격 R7",
                                     "        if False:\n            return None, xcap_why(x)              # 10-30 사전 공격 R7"),
                                    ("    if size > XCAP:\n        return None, xcap_why(x)\n    t = VAL0", "    if False:\n        return None, xcap_why(x)\n    t = VAL0")]),
    ('M16', 'R8 group 을 값 대조에서 뺌 (리뷰어 M16)', "if not w or w[0] in ('print', 'if') or mkdir_key(w) is not None:",
     "if not w or w[0] in ('print', 'if', 'group') or mkdir_key(w) is not None:"),
]


def make(m):
    # 바꿀 글 = 도구에 정확히 한 번 · 그 자리 (번호) 에서 바꾸고, 같은 자리에서 되돌려 도구와 바이트 같은지 본다
    reps = m[2] if isinstance(m[2], list) else [(m[2], m[3])]
    s, done = SRC, []
    for a, b in reps:
        assert s.count(a) == 1, (m[0], a, s.count(a))
        i = s.index(a)
        s = s[:i] + b + s[i + len(a):]
        done.append((i, a, b))
    back = s
    for i, a, b in reversed(done):
        assert back[i:i + len(b)] == b, (m[0], 'revert place')
        back = back[:i] + a + back[i + len(b):]
    assert back == SRC, (m[0], 'revert differs')
    return s


def run(script, only):
    env = dict(os.environ, TMPDIR=TMP)
    args = ['nice', '-n', '10', sys.executable, '-I', TEST, '--script', script] + (['--only', 'VP'] if only else [])
    r = subprocess.run(args, capture_output=True, text=True, env=env, timeout=5400, cwd=os.path.dirname(os.path.dirname(TEST)))
    out = r.stdout + r.stderr
    tot = re.findall(r'(\d+) PASS · (\d+) FAIL', out)
    fails = [l.split(' → ')[0][5:].split(' ')[0] for l in out.splitlines() if l.startswith('FAIL ')]
    return out, (tot[-1] if tot else ('?', '?')), fails


os.makedirs(os.path.join(OUT, 'logs'), exist_ok=True)
os.makedirs(TMP, exist_ok=True)
res = []
for m in MUT:
    if SEL and m[0] not in SEL:
        continue
    p = os.path.join(OUT, 'mut_%s.sh' % m[0])
    with open(p, 'w', encoding='utf-8') as f:
        f.write(make(m))
    out, tot, fails = run(p, True)
    scope = 'VP'
    if tot[1] == '0':                     # VP 에서 살아남음 → 전체
        out, tot, fails = run(p, False)
        scope = '전체'
    with open(os.path.join(OUT, 'logs', '%s.log' % m[0]), 'w', encoding='utf-8') as f:
        f.write(out)
    caught = tot[1] not in ('0', '?')
    line = '%-4s %-4s %-20s %s · %s' % (m[0], '잡힘' if caught else '생존', '%s PASS · %s FAIL (%s)' % (tot[0], tot[1], scope), m[1],
                                         ' '.join(sorted(set(fails)))[:200])
    print(line, flush=True)
    res.append(line)
    os.remove(p)
with open(os.path.join(OUT, 'mutation_r2.txt'), 'a', encoding='utf-8') as f:
    f.write('도구 sha256 %s\n' % hashlib.sha256(SRC.encode()).hexdigest())
    for l in res:
        f.write(l + '\n')
