# quotation_ban 을 글자 그대로 · 정규식으로 대 본다 (리포 작업 트리의 claims.json · 읽기만)
import json, re, sys, pathlib
qb = json.load(open('/home/user/Yonghoon-DEM-DFT/docs/reviews/claims.json', encoding='utf-8'))['quotation_ban']
hits = 0
for f in sys.argv[1:]:
    t = pathlib.Path(f).read_text(encoding='utf-8')
    for e in qb:
        pat = e['pattern']
        n_lit = t.count(pat)
        try:
            n_re = len(re.findall(pat, t))
        except re.error:
            n_re = None
        if n_lit or n_re:
            hits += 1
            print(f'{f}: {pat!r} 글자 {n_lit} 정규식 {n_re} ({e["claim"]})')
print('걸린 것', hits, '· 패턴', len(qb), '· 파일', len(sys.argv) - 1)
