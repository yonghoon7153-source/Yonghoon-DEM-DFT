"""KG50R-F01 새 관문 하나씩 끈 사본 (스크래치) → V 묶음 시험 (test_vonly.py) — 잡힘 / 생존.
   python3 -I mutate_f01.py <고친 resume_ckpt.sh> <test_vonly.py> <출력 폴더> [변이 이름,…]
   잡힘 = V 시험 하나라도 FAIL · 생존 = V 시험 전부 PASS 그대로 (그 관문을 V 시험이 보지 않는다)."""
import os
import re
import subprocess
import sys

tool, vonly, outd = sys.argv[1:4]
src = open(tool, encoding='utf-8').read()
os.makedirs(outd, exist_ok=True)

MUT = [
    ('F01-1', '① 값 다름 문제 (setup_values em != er)', "            elif em != er:\n", "            elif False:\n"),
    ('F01-2', '① 상수 아님 → 실행 상태 값 표지 (sub_text)', "    if why:\n        return RT0 + '실행 상태 값",
     "    if False:\n        return RT0 + '실행 상태 값"),
    ('F01-3', '① 상수 아님 문제 줄 (setup_values)', "            elif RT0 in er or RT0 in em:\n", "            elif False:\n"),
    ('F01-4', '① · ③ 펼칠 수 없음 문제 줄 (setup_values)', "            if em is None or er is None:\n                probs.append(",
     "            if em is None or er is None:\n                (lambda *a: None)("),
    ('F01-5', '② 끝 상태 = 펼친 줄 대조 (state_cmp)', "            if xM is not None and xR is not None and xM.get(k) != xR.get(k):\n",
     "            if False:\n"),
    ('F01-6', '② 판 메시 file 이름 허용 = 펼친 줄도 (state_cmp)', "              and mesh_file(xM.get(k) or '', xR.get(k) or '') is None):\n",
     "              and False):\n"),
    ('F01-7', '③ 흐름 · 변수 바꾸는 줄 (var_env)', "        if w[0] in FLOWV or any(x[0] in FLOWV | {'variable'} for x in nested(w)):\n",
     "        if False:\n"),
    ('F01-8', '③ run every 안 명령 (nested)', "        elif cw[0] == 'run' and 'every' in cw[2:]:\n            cs = [x for x in cw[cw.index('every', 2) + 2:] if x != 'NULL']",
     "        elif False:\n            cs = [x for x in cw[cw.index('every', 2) + 2:] if x != 'NULL']"),
    ('F01-9', '③ python = 흐름 (FLOWV)', "FLOWV = {'label', 'jump', 'next', 'python', 'partition'}", "FLOWV = {'label', 'jump', 'next', 'partition'}"),
    ('F01-34', '③ partition = 흐름 (FLOWV)', "FLOWV = {'label', 'jump', 'next', 'python', 'partition'}", "FLOWV = {'label', 'jump', 'next', 'python'}"),
    ('F01-35', '③ 겹친 명령 (nested · 한 층만으로)', "            out.append(xw)\n            todo.append(xw)\n", "            out.append(xw)\n"),
    ('F01-36', '② 끝 상태 변수 표 못 정함 (xstate)', "                 if (k[0] == 'variable' and endwhy) else", "                 if False else"),
    ('F01-10', '③ variable 이름 · 꼴 자리 치환 (var_env)', "        if len(wp) < 3 or any(s < wp[2][1] for s, _, _, _ in subs):\n",
     "        if len(wp) < 3:\n"),
    ('F01-11', '① 템플릿 fix 짝 (check)', "                tpl[i] = mi\n", "                pass\n"),
    ('F01-12', 'isubs 따옴표 (" · \' 뒤집기)', "        if ch == '\"':\n            dq = not dq\n        elif ch == \"'\":\n            sq = not sq\n        i += 1\n    return out",
     "        i += 1\n    return out"),
    ('F01-13', 'isubs $(...)', "            elif nx == '(':\n", "            elif False:\n"),
    ('F01-14', 'isubs 한 글자 $c', "            elif re.fullmatch(r'[A-Za-z0-9_]', nx):\n", "            elif False:\n"),
    ('F01-15', 'isubs } 없는 ${', "                if j < 0:\n                    out.append((i, n, 'x', l[i:]))\n                    return out\n                out.append((i, j + 1, 'v', l[i + 2:j]))",
     "                if j < 0:\n                    return out\n                out.append((i, j + 1, 'v', l[i + 2:j]))"),
    ('F01-16', 'fwhy 수학 함수 허용 (MATHF)', "MATHF = {'sqrt', 'exp', 'ln', 'log', 'abs', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'ceil', 'floor', 'round'}",
     "MATHF = set()"),
    ('F01-17', 'fwhy 비교 연산자 허용', "        elif t[i:i + 2] in ('==', '!=', '<=', '>='):\n            i += 2\n", "        elif False:\n            i += 2\n"),
    ('F01-18', 'fwhy 논리 연산자 거부', "        elif ch in '&|!':\n            return '논리 연산자", "        elif ch in '&|!':\n            i += 1\n            continue\n            return '논리 연산자"),
    ('F01-19', 'fwhy 이름 낱말 (thermo · 함수 · PI) 거부',
     "            return '%s%s (실행 상태 낱말 · 함수 · 등록 상수 목록 밖)' % (t[i:j], '()' if t[j:j + 1] == '(' else '')",
     "            i = j\n            continue"),
    ('F01-20', 'sub_text string 값 공백 · 따옴표 거부', r"""    if env[x][0] == 'string' and re.search('[ \t"\']', bare(t)):""", "    if False:"),
    ('F01-21', 'sub_text bare() (표지 안 공백은 수)', r"""re.search('[ \t"\']', bare(t))""", r"""re.search('[ \t"\']', t)"""),
    ('F01-22', 'expand v_ string 수 글', "                    elif NUMLIT.fullmatch(dy[1]):\n", "                    elif False:\n"),
    ('F01-23', 'expand v_ string = equal 값 하나', "                    if dy[1][:1] == VAL0 and mark_end(dy[1], 0) == len(dy[1]):\n", "                    if False:\n"),
    ('F01-24', 'expand v_ string 수 글 아님 거부',
     "                        return None, 'v_%s — string 값 [%s] 이 수 글이 아님 (LIGGGHTS 는 atof)' % (y, show(dy[1]))",
     "                        out.append(VAL0 + dy[1] + VAL1)"),
    ('F01-25', 'expand equal 밖 꼴 (atom) 거부', "    if st != 'equal':\n        return None, '%s 변수 %s 는", "    if False:\n        return None, '%s 변수 %s 는"),
    ('F01-26', 'expand 순환 참조', "    if x in seen or len(seen) > 64:\n", "    if False:\n"),
    ('F01-27', 'expand v_x[…] 거부', "                if body[j:j + 1] == '[':\n", "                if False:\n"),
    ('F01-28', 'var_env 못 펼치는 변수 유지 (delete 전)', "        elif old is not None and old[0] == 'bad':\n            pass", "        elif False:\n            pass"),
    ('F01-29', 'var_env 다른 꼴 다시 정의', "        elif old is not None and old[0] != st:\n", "        elif False:\n"),
    ('F01-30', 'var_env 인자 수 하나', "        elif len(wp) != 4:\n", "        elif False:\n"),
    ('F01-31', 'var_env 따옴표 낱말 안 치환', "            env[x] = (st, wp[3][2]) if not subs else ('bad'", "            env[x] = (st, wp[3][2]) if True else ('bad'"),
    ('F01-32', 'var_env 못 읽는 variable 줄', "            if l.split()[0] == 'variable':\n", "            if False:\n"),
    ('F01-33', '① 순서 대조 짝 (setup_order 가 돌려줌)', "        pairs.append((ri[n] if ri is not None else n, Mq[k][0]))\n", "        pass\n"),
]

if len(sys.argv) > 4:          # 골라 돌리기 — 넷째 인자 = 변이 이름 쉼표 목록
    keep = set(sys.argv[4].split(','))
    MUT = [m for m in MUT if m[0] in keep]
rows = []
for mid, what, old, new in MUT:
    assert src.count(old) == 1, (mid, src.count(old))
    p = os.path.join(outd, 'resume_ckpt_%s.sh' % mid.replace('-', '_'))
    with open(p, 'w', encoding='utf-8') as f:
        f.write(src.replace(old, new))
    r = subprocess.run([sys.executable, '-I', vonly, '--script', p], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1200)
    out = r.stdout.decode('utf-8', 'replace')
    last = out.strip().splitlines()[-1] if out.strip() else ''
    fails = [re.match(r'FAIL (V[0-9]+[a-z]?) ', l).group(1) for l in out.splitlines() if re.match(r'FAIL (V[0-9]+[a-z]?) ', l)]
    uniq = []
    for x in fails:
        if x not in uniq:
            uniq.append(x)
    caught = r.returncode != 0 and bool(fails)
    rows.append((mid, what, '잡힘' if caught else '생존', last, ' '.join(uniq)))
    with open(os.path.join(outd, '%s.log' % mid), 'w', encoding='utf-8') as f:
        f.write(out)
    print('%-7s %-4s %-22s %s · %s' % (mid, '잡힘' if caught else '생존', last, what, ' '.join(uniq)), flush=True)
print('── 변이 %d · 잡힘 %d · 생존 %d' % (len(rows), sum(r[2] == '잡힘' for r in rows), sum(r[2] == '생존' for r in rows)))
