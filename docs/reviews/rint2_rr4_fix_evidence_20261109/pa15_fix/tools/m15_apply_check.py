# -*- coding: utf-8 -*-
"""사전 공격 15 변이 목록 (probes/mutate15.py 의 M · 바이트 그대로 읽음) 이 고친 판 사슬에 그대로 적용되나 (찾는 글자가 정확히 한 번) → 변이마다 적용 수."""
import sys
from pathlib import Path

m15 = Path(sys.argv[1]).read_text(encoding='utf-8')
chain = Path(sys.argv[2]).read_text(encoding='utf-8')
ns = {}
exec(m15[m15.index('M = ['):m15.index('\n]\n', m15.index('M = [')) + 3], ns)
for mid, old, _new in ns['M']:
    print(mid, chain.count(old))
