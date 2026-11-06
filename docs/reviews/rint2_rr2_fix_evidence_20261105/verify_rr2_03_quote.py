"""RR2-03 (11-05) — 등록 R §7-1 ⑫ 의 11-05 정정이 인용한 코드 한정어가 `scripts/carbon_junction.py` CJUNC_QUALIFIERS 넷째 줄의 바이트 그대로 · 문서에 한 번인지 ·
넓은 옛 문구가 취소선 안에만 남았는지 · 임의 교차 · 비스듬한 접합을 식 검증이라고 쓰지 않았는지 본다 (읽기만).

  python3 -I verify_rr2_03_quote.py <작업 트리>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / 'scripts'))
import carbon_junction as CJ                                    # noqa: E402

reg = (ROOT / 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md').read_text(encoding='utf-8')
line = [ln for ln in reg.splitlines() if ln.startswith('필수 한정어:')]
assert len(line) == 1
ln = line[0]
i12 = ln.index('⑫')
i13 = ln.index('⑬')
item = ln[i12:i13]
fix = item[item.index('→ 11-05 정정 (RR2-03'):]
q = re.findall(r'\*"(.+?)"\*', fix)
code = CJ.CJUNC_QUALIFIERS[3]
rest = re.sub(r'~~.+?~~', '', item)                             # 취소선 밖 (지금 유효한 글)
out = {
    'quotes_in_fix': len(q),
    'quote_bytes': len(q[0].encode('utf-8')) if q else None,
    'quote_is_code_substring': bool(q) and q[0] in code,
    'quote_count_in_registration': reg.count(q[0]) if q else None,
    'broad_phrases_outside_strike': [w for w in ('분산판 = 전송선 · 식 검증', '코드 한정어 같은 문구') if w in rest],
    'ranges_in_fix': ('Δ/λ 0.02 – 0.63' in fix, 'q 0.4 – 19' in fix),
    'axial_share_sentence': '긴 접촉 포화 = 축저항 몫을 뺀 접합 기여분' in fix,
    'no_arbitrary_claim': '임의 교차 · 비스듬한 접합은 식 검증되지 않았다' in fix,
}
ok = (out['quotes_in_fix'] == 1 and out['quote_is_code_substring'] and out['quote_count_in_registration'] == 1 and not out['broad_phrases_outside_strike']
      and all(out['ranges_in_fix']) and out['axial_share_sentence'] and out['no_arbitrary_claim'])
out['ok'] = ok
print(json.dumps(out, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
