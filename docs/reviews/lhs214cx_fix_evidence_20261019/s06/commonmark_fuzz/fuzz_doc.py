"""읽기 전용 — 등록 파서 `_md_section(doc, 3, strip_code=True)` 를 markdown-it-py 3.0.0 commonmark (Codex oracle 과 같은 판) 과 문서 단위로 대조 (★ 10-19 L214R-S06 증거).
지원 범위 꼴만 (0 열 ATX 제목 — 빈 제목 포함 · 울타리 코드 블록 · 문단): doc = '## 3. A' + 줄 N 개 (아래 SLOTS 의 모든 조합) + 값 줄.
대조 = (가) 활성 §3 이 정확히 하나인가 · (나) 값 줄이 §3 안 · 울타리 코드 밖인가.
python3 -I fuzz_doc.py <markdown-it-py 를 설치한 폴더> <우리 트리> <out.json> <N>   (설치 = pip install --target <폴더> markdown-it-py==3.0.0 · 리포 의존 아님)"""
import contextlib
import hashlib
import io
import itertools
import json
import re
import sys
from pathlib import Path

PYLIB, TREE, OUT, NS = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]), int(sys.argv[4])
sys.path[:0] = [str(PYLIB), str(TREE / 'scripts')]
sys.dont_write_bytecode = True
from markdown_it import MarkdownIt  # noqa: E402
import markdown_it  # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import supp20_input_receipt as sr  # noqa: E402

md = MarkdownIt('commonmark')
VAL = '`code_fp ' + 'ab' * 32 + '`'
SLOTS = ['', 'text', '#', '##', '## ', '#\t', '##  ', '#  ', '###', '### x', '# x', '## x', '## 3. dup', '```', '~~~', '````', '```x',
         '~~~~ y', '#5', '\\##', '##########', '## ##']
SEC3 = re.compile(r'3\.(\s|$)')


def oracle(doc, vidx):
    """None = 활성 §3 이 하나가 아님 · True/False = 값 줄 (vidx) 이 §3 안 · 코드 블록 밖인가 (맨 위 수준 제목만 · map = [시작, 끝) 줄)."""
    toks = md.parse(doc)
    heads = [(t.map[0], int(t.tag[1]), toks[i + 1].content) for i, t in enumerate(toks) if t.type == 'heading_open' and t.level == 0]
    codes = [t.map for t in toks if t.type in ('fence', 'code_block')]
    hit = [h for h in heads if h[1] == 2 and SEC3.match(h[2])]
    if len(hit) != 1:
        return None
    i0 = hit[0][0]
    i1 = next((h[0] for h in heads if h[0] > i0 and h[1] <= 2), 10 ** 9)
    return (i0 <= vidx < i1) and not any(a <= vidx < b for a, b in codes)


def ours(doc):
    body, _why = sr._md_section(doc, 3, strip_code=True)
    return None if body is None else VAL in body.split('\n')


#  oracle 의 map 뜻 확인 (알려진 꼴)
assert oracle('## 3. A\n' + VAL + '\n', 1) is True
assert oracle('## 3. A\n##\n' + VAL + '\n', 2) is False
assert oracle('## 3. A\n```\n' + VAL + '\n```\n', 2) is False
assert oracle('## 3. A\n```\n```\n' + VAL + '\n', 3) is True
assert oracle('## 3. A\n```\n' + VAL + '\n', 2) is False          # 닫히지 않은 울타리 = 문서 끝까지 코드

n = mism = none_both = in_both = out_both = 0
examples = []
for combo in itertools.product(SLOTS, repeat=NS):
    lines = ['## 3. A', *combo, VAL]
    doc = '\n'.join(lines) + '\n'
    o, u = oracle(doc, len(lines) - 1), ours(doc)
    n += 1
    if o != u:
        mism += 1
        if len(examples) < 20:
            examples.append(dict(lines=lines, oracle=o, ours=u))
    elif o is None:
        none_both += 1
    elif o:
        in_both += 1
    else:
        out_both += 1
res = dict(markdown_it_version=markdown_it.__version__, preset='commonmark',
           tool_sha256=hashlib.sha256((TREE / 'scripts/supp20_input_receipt.py').read_bytes()).hexdigest(), slots=SLOTS, nslots=NS, docs=n,
           mismatches=mism, agree_no_unique_s3=none_both, agree_value_in_s3=in_both, agree_value_not_in_s3=out_both, examples=examples)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps({k: (v[:12] if k == 'tool_sha256' else v) for k, v in res.items() if k not in ('examples', 'slots')}, ensure_ascii=False))
for e in examples[:4]:
    print(e)
