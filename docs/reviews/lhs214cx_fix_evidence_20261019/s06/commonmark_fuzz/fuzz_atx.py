"""읽기 전용 — 0 열 ATX 제목 인식 (`supp20_input_receipt._md_atx`) 을 markdown-it-py 3.0.0 commonmark (Codex oracle 과 같은 판) 과 줄 단위로 대조하고,
옛 식 `^(#{1,6})[ \\t]+(\\S.*?)[ \\t]*$` 과도 비교한다 (★ 10-19 L214R-S06 증거).
줄 = `#` 1–8 개 + 꼬리 조각 (space · tab · NBSP · U+2003 · FF · U+2028 · 글자 · `#` · 백슬래시 · '3.' …) 0–4 개.
python3 -I fuzz_atx.py <markdown-it-py 를 설치한 폴더> <우리 트리> <out.json>   (설치 = pip install --target <폴더> markdown-it-py==3.0.0 · 리포 의존 아님)"""
import contextlib
import hashlib
import io
import itertools
import json
import re
import sys
from pathlib import Path

PYLIB, TREE, OUT = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
sys.path[:0] = [str(PYLIB), str(TREE / 'scripts')]
sys.dont_write_bytecode = True
from markdown_it import MarkdownIt  # noqa: E402
import markdown_it  # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):
    import supp20_input_receipt as sr  # noqa: E402

OLD = re.compile(r'^(#{1,6})[ \t]+(\S.*?)[ \t]*$')
SEC3 = re.compile(r'3\.(\s|$)')
md = MarkdownIt('commonmark')
TOK = ['', ' ', '\t', ' ', ' ', 'a', '#', '##', '3.', '\\', '\x0c', ' ', 'b c', '\\#', '3. x']
lines = sorted({'#' * n + ''.join(c) for n in range(1, 9) for k in range(0, 5) for c in itertools.product(TOK, repeat=k)})


def oracle(ln):
    """(수준, 내용) | None — markdown-it-py 가 이 줄 하나를 첫 블록 제목으로 읽으면 (내용 = 그 구현의 .strip() — 모든 Unicode 공백)."""
    t = md.parse(ln + '\n')
    if t and t[0].type == 'heading_open' and t[0].map and t[0].map[0] == 0:
        return int(t[0].tag[1]), t[1].content
    return None


KEYS = ('mismatch_heading', 'mismatch_level', 'mismatch_title', 'new_vs_old_added', 'new_vs_old_removed', 'sec3_new_vs_old_diff')
stats = dict(lines=len(lines), heading_cm=0, **{k: 0 for k in KEYS})
examples = {k: [] for k in KEYS}


def ex(key, item):
    stats[key] += 1
    if len(examples[key]) < 12:
        examples[key].append(item)


for ln in lines:
    cm, new, mo = oracle(ln), sr._md_atx(ln), OLD.match(ln)
    old = (len(mo.group(1)), mo.group(2)) if mo else None
    stats['heading_cm'] += cm is not None
    if (cm is None) != (new is None):
        ex('mismatch_heading', [ln, cm, new])
        continue
    if cm is not None:
        if cm[0] != new[0]:
            ex('mismatch_level', [ln, cm, new])
        if new[1].strip() != cm[1]:                  # 우리 제목 = space · tab 만 뗀다 → 비교는 같은 .strip() 위에서
            ex('mismatch_title', [ln, cm, new])
    if (old is None) != (new is None):
        ex('new_vs_old_added' if old is None else 'new_vs_old_removed', [ln, old, new])
    s_old = old is not None and old[0] == 2 and bool(SEC3.match(old[1]))     # §3 식별 (수준 2 · 제목 '3.') — 옛 식 ↔ 새 인식
    s_new = new is not None and new[0] == 2 and bool(SEC3.match(new[1]))
    if s_old != s_new:
        ex('sec3_new_vs_old_diff', [ln, old, new])
res = dict(markdown_it_version=markdown_it.__version__, preset='commonmark',
           tool_sha256=hashlib.sha256((TREE / 'scripts/supp20_input_receipt.py').read_bytes()).hexdigest(), stats=stats, examples=examples)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps(dict(tool_sha256=res['tool_sha256'][:12], **stats), ensure_ascii=False))
for k, v in examples.items():
    if v:
        print(k, [repr(x[0]) for x in v[:6]])
