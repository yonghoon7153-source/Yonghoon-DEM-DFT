# 고치기 전 판 (통합 12bc95ce) VP FAIL 까닭 — 로그 FAIL 줄의 자세히 (출력 끝 1500 자) 에서: -C 판정 · 본 흐름 시험 여부 · R7 시간 초과
#   usage: python3 -I why_before.py <before 로그>
import re, sys
for l in open(sys.argv[1], encoding='utf-8'):
    if not l.startswith('FAIL VP'):
        continue
    name = det = l[5:]
    tag = name.split(' ')[0] + (' (-T)' if '→ 본 흐름 (-T)' in l else '')
    if '→ 본 흐름 (-T)' in l:
        # 자세히 = stdout 끝 1500 자 — 정적 대조 줄은 잘려 나갈 수 있어 시험 결과 줄 (🧪 시험만 · G0) 로 본다
        why = ('본 흐름: 시험 냄 · G0–G3 통과 (반례 열림)' if '🧪 시험만 (-T) — G0–G3 통과' in det else
               '본 흐름: 시험 냄' if 'G0 시험 정상 종료' in det else '본 흐름: ' + ('정적 대조 실패' if '정적 대조 실패' in det else '?'))
    elif tag.startswith('VP7'):
        why = 'R7: ' + ('60 초 시간 초과' if '시간 초과' in det else re.search(r'rc (-?\d+)', det).group(0) + (' 통과' if '통과 (문제 0)' in det else ' 다른 판정'))
    else:
        m = re.search(r'재개 덱 정적 대조: (통과|실패) \(문제 (\d+)\)', det)
        why = ('-C 통과 (문제 0) = 반례 열림' if m.group(1) == '통과' else '-C 실패 (문제 %s) = 다른 까닭으로 거부 · 새 문제 줄 없음' % m.group(2)) if m else '?'
    print('%-6s %s' % (tag, why))
