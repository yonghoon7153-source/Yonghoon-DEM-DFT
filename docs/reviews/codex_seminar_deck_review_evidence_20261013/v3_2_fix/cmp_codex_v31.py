"""Compare decks against the Codex v3.1 closure evidence (per-slide a:t runs, notes, media sha256) — read-only.
Run from the worktree root:
  python3 -I cmp_codex_v31.py <evidence pptx.json> <base_v31.pptx> <v32.pptx> <out.json>
Checks:
  (1) rebuilt v3.1 base deck  == Codex-closed v3.1 deck (all 17 slides: texts, notes, media)
  (2) v3.2 untouched slides   == Codex-closed v3.1 slides (citation renumbering applied; the added 'Bridge' line removed)"""
import hashlib
import json
import re
import sys
import zipfile

from lxml import etree

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
CITE_MAP = {7: 2, 15: 3, 12: 10, 16: 11}
UNTOUCHED = {1: 1, 2: 2, 4: 5, 6: 7, 8: 4, 18: 17}          # v3.2 → v3.1


def renum(t):
    """same rule as build_seminar_v32.renum (single or comma-separated citation lists)"""
    def rep(mo):
        return '[' + ', '.join(str(CITE_MAP.get(int(n), int(n))) for n in mo.group(1).split(',')) + ']'
    return re.sub(r'\[(\d+(?:\s*,\s*\d+)*)\]', rep, t)


def rels_of(z, part):
    d, f = part.rsplit('/', 1)
    rp = f'{d}/_rels/{f}.rels'
    if rp not in z.namelist():
        return {}
    out = {}
    for r in etree.fromstring(z.read(rp)):
        tgt = r.get('Target')
        if r.get('TargetMode') == 'External':
            continue
        parts = (d + '/' + tgt).split('/')
        stack = []
        for p in parts:
            if p == '..':
                stack.pop()
            elif p not in ('', '.'):
                stack.append(p)
        out[r.get('Id')] = ('/'.join(stack), r.get('Type'))
    return out


def deck(path):
    z = zipfile.ZipFile(path)
    pres = etree.fromstring(z.read('ppt/presentation.xml'))
    prel = rels_of(z, 'ppt/presentation.xml')
    slides = []
    for sid in pres.findall('p:sldIdLst/p:sldId', NS):
        part = prel[sid.get('{%s}id' % NS['r'])][0]
        root = etree.fromstring(z.read(part))
        bridge_ids = set()
        for sp in root.iter('{%s}sp' % NS['p']):
            c = sp.find('.//p:cNvPr', NS)
            if c is not None and c.get('name') == 'Bridge':
                bridge_ids.add(id(sp))
        texts = []
        for t in root.iter('{%s}t' % NS['a']):
            anc = t
            inside_bridge = False
            while anc is not None:
                if id(anc) in bridge_ids:
                    inside_bridge = True
                    break
                anc = anc.getparent()
            if not inside_bridge:
                texts.append(t.text or '')
        rel = rels_of(z, part)
        media = sorted(hashlib.sha256(z.read(p)).hexdigest() for p, ty in rel.values() if ty.endswith('/image'))
        notes = ''
        for p, ty in rel.values():
            if ty.endswith('/notesSlide'):
                nroot = etree.fromstring(z.read(p))
                for sp in nroot.iter('{%s}sp' % NS['p']):
                    ph = sp.find('.//p:nvPr/p:ph', NS)
                    if ph is not None and ph.get('type') == 'body':
                        notes = '\n'.join(''.join(t.text or '' for t in para.iter('{%s}t' % NS['a']))
                                          for para in sp.iter('{%s}p' % NS['a']))
        slides.append(dict(texts=texts, notes=notes.strip(), media=media))
    return slides


ev = json.load(open(sys.argv[1], encoding='utf-8'))['slides']
base, v32 = deck(sys.argv[2]), deck(sys.argv[3])
res = dict(base_vs_codex=[], v32_untouched_vs_codex=[])


def norm_notes(x):
    return '\n'.join(x) if isinstance(x, list) else x


for i, e in enumerate(ev, 1):
    b = base[i - 1]
    res['base_vs_codex'].append(dict(slide=i, texts=b['texts'] == e['texts'],
                                     notes=b['notes'] == norm_notes(e['notes']).strip(),
                                     media=b['media'] == sorted(m['sha256'] for m in e['media'])))
for n, o in UNTOUCHED.items():
    e, s = ev[o - 1], v32[n - 1]
    want_texts = [renum(t) for t in e['texts']]
    res['v32_untouched_vs_codex'].append(dict(v32_slide=n, v31_slide=o,
                                              texts=s['texts'] == want_texts or ''.join(s['texts']) == ''.join(want_texts),
                                              notes=s['notes'] == renum(norm_notes(e['notes']).strip()),
                                              media=s['media'] == sorted(m['sha256'] for m in e['media'])))
ok1 = all(r['texts'] and r['notes'] and r['media'] for r in res['base_vs_codex'])
ok2 = all(r['texts'] and r['notes'] and r['media'] for r in res['v32_untouched_vs_codex'])
res['summary'] = dict(base_identical_to_codex_v31=ok1, untouched_identical_to_codex_v31=ok2,
                      codex_v31_pptx_sha256='73fa2dc3b5629eabb9ec744b47495512db477dd962753a003820ad02b525401b')
json.dump(res, open(sys.argv[4], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k in ('base_vs_codex', 'v32_untouched_vs_codex'):
    bad = [r for r in res[k] if not (r['texts'] and r['notes'] and r['media'])]
    print(k, 'all identical' if not bad else bad)
print(res['summary'])
