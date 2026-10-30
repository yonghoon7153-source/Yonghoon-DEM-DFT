# 통합 도구 = F01 정적 대조 heredoc + F02 그 밖 (바이트 같음) 확인 — usage: python3 -I compose_check.py <기준 77c24237> <F01 38e1eff5> <F02 e5a61181> <통합 12bc95ce>
#   (도구 판 = git show <커밋>:scripts/resume_ckpt.sh — bf8cf21c6 · c24fef721 · d23a865a3 · 통합 가지의 4865ba895)
import hashlib, sys
HEAD = "deckcheck(){ python3 - \"$@\" <<'PY'\n"


def parts(p):
    s = open(p, encoding='utf-8').read()
    a = s.index(HEAD)
    b = s.index("\nPY\n}", a)
    return hashlib.sha256(s.encode()).hexdigest()[:12], s[:a], s[a:b], s[b:]


base, f01, f02, comb = (parts(p) for p in sys.argv[1:5])
print('sha256 앞 12: 기준 %s · F01 %s · F02 %s · 통합 %s' % (base[0], f01[0], f02[0], comb[0]))
print('heredoc (정적 대조): 통합 == F01 %s · F02 == 기준 %s' % (comb[2] == f01[2], f02[2] == base[2]))
print('heredoc 뒤 (러너 · 제출): 통합 == F02 %s · F01 == 기준 %s' % (comb[3] == f02[3], f01[3] == base[3]))
print('heredoc 앞 (머리 주석 · 인자): 통합 == F01 == F02 == 기준 %s' % (comb[1] == f01[1] == f02[1] == base[1]))
