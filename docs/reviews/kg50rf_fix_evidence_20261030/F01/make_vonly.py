"""시험 파일에서 V 묶음만 도는 사본을 만든다 (변이 시험용 · 머리 (chk · grp) + ok_log + V 묶음 + 끝 줄).
   python3 -I make_vonly.py <scripts/test_resume_ckpt.py> <출력 .py> <리포 뿌리>"""
import sys

src, dst = sys.argv[1:3]
t = open(src, encoding='utf-8').read()
head_end = t.index('    # ── Codex §3 반례 다섯')
v0 = t.index('    # ── V: 10-30 (KG50R-F01')
v1 = t.index("    print('%d PASS · %d FAIL' % (ok, fail))")
assert head_end < v0 < v1
out = t[:head_end] + "    ok_log = trial_log('ok')\n" + t[v0:v1] + t[v1:]
# ROOT 를 원 리포로 (사본은 스크래치에 있다)
root_line = "ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
assert out.count(root_line) == 1
repo = sys.argv[3] if len(sys.argv) > 3 else None
assert repo
out = out.replace(root_line, 'ROOT = %r\n' % repo)
open(dst, 'w', encoding='utf-8').write(out)
print('V 만 사본:', dst, len(out.splitlines()), '줄')
