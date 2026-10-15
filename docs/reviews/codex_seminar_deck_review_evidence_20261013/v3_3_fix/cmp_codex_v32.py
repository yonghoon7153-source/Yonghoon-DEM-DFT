"""Compare decks against the Codex v3.2 re-check evidence — read-only, independent of the producer code.
Per slide: a:t + m:t text runs (document order), notes runs, image sha256 (sorted), OMML (m:oMathPara C14N) —
the same reading rule as `extract()` in docs/reviews/codex_seminar_v32_recheck_evidence_20261015/inspect_deck.py
(that script is NOT run here; the rule is re-implemented).

python3 -I cmp_codex_v32.py <codex evidence pptx.json> <delivered v3.2 pptx> <rebuilt v3.2 base pptx> <v3.3 pptx> <out.json>

(1) delivered v3.2 deck   == Codex evidence, 18 / 18 slides   (this reader reproduces Codex's reading)
(2) rebuilt v3.2 base     == Codex evidence, 18 / 18 slides   (the v3.3 build starts from what Codex reviewed)
(3) v3.3 unchanged slides == Codex evidence (1 2 4 6 8 9 10 12 14 16 17 18)
(4) v3.3 changed slides   : which of texts / notes / media / equations differ — expected (3 texts notes) (5 notes) (7 texts)
                            (11 texts notes media) (13 notes) (15 texts notes); slide 3 equations and pictures identical
"""
import hashlib
import json
import posixpath
import sys
import zipfile

from lxml import etree

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}
UNCHANGED = (1, 2, 4, 6, 8, 9, 10, 12, 14, 16, 17, 18)
CHANGED = (3, 5, 7, 11, 13, 15)
EXPECT_DIFF = {3: {'texts', 'notes'}, 5: {'notes'}, 7: {'texts'}, 11: {'texts', 'notes', 'media'}, 13: {'notes'}, 15: {'texts', 'notes'}}
KEYS = ('texts', 'notes', 'media', 'equations')


def texts(el):
    return el.xpath('.//a:t/text() | .//m:t/text()', namespaces=NS)


def extract(path):
    slides = []
    with zipfile.ZipFile(path) as z:
        def rels(part):
            rp = posixpath.dirname(part) + '/_rels/' + posixpath.basename(part) + '.rels'
            if rp not in z.namelist():
                return []
            return [(n.get('Target'), n.get('Type'), n.get('TargetMode') == 'External') for n in etree.fromstring(z.read(rp))]
        pres = etree.fromstring(z.read('ppt/presentation.xml'))
        prel = {n.get('Id'): n.get('Target') for n in etree.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
        for sid in pres.findall('p:sldIdLst/p:sldId', NS):
            part = posixpath.normpath('ppt/' + prel[sid.get('{%s}id' % NS['r'])])
            root = etree.fromstring(z.read(part))
            notes, media = [], []
            for tgt, typ, ext in rels(part):
                if ext:
                    continue
                loc = posixpath.normpath(posixpath.dirname(part) + '/' + tgt)
                if typ.endswith('/notesSlide'):
                    notes = texts(etree.fromstring(z.read(loc)))
                if typ.endswith('/image'):
                    media.append(hashlib.sha256(z.read(loc)).hexdigest())
            eq = [etree.tostring(e, method='c14n').decode() for e in root.xpath('.//m:oMathPara', namespaces=NS)]
            slides.append(dict(texts=texts(root), notes=notes, media=sorted(media), equations=eq))
    return slides


def codex(path):
    ev = json.load(open(path, encoding='utf-8'))['slides']
    return [dict(texts=s['texts'], notes=s['notes'], media=sorted(m['sha256'] for m in s['media']), equations=s['equations']) for s in ev]


def same(a, b):
    return {k: a[k] == b[k] for k in KEYS}


ev = codex(sys.argv[1])
d32, base, d33 = extract(sys.argv[2]), extract(sys.argv[3]), extract(sys.argv[4])
res = dict(delivered_v32_vs_codex=[], rebuilt_v32_base_vs_codex=[], v33_unchanged_vs_codex=[], v33_changed_vs_codex=[])
for i in range(1, 19):
    res['delivered_v32_vs_codex'].append(dict(slide=i, **same(d32[i - 1], ev[i - 1])))
    res['rebuilt_v32_base_vs_codex'].append(dict(slide=i, **same(base[i - 1], ev[i - 1])))
for i in UNCHANGED:
    res['v33_unchanged_vs_codex'].append(dict(slide=i, **same(d33[i - 1], ev[i - 1])))
for i in CHANGED:
    s = same(d33[i - 1], ev[i - 1])
    diff = {k for k, v in s.items() if not v}
    res['v33_changed_vs_codex'].append(dict(slide=i, differs=sorted(diff), expected=sorted(EXPECT_DIFF[i]), as_expected=diff == EXPECT_DIFF[i]))
ok1 = all(all(r[k] for k in KEYS) for r in res['delivered_v32_vs_codex'])
ok2 = all(all(r[k] for k in KEYS) for r in res['rebuilt_v32_base_vs_codex'])
ok3 = all(all(r[k] for k in KEYS) for r in res['v33_unchanged_vs_codex'])
ok4 = all(r['as_expected'] for r in res['v33_changed_vs_codex'])
res['summary'] = dict(delivered_v32_identical_to_codex_reading=ok1, rebuilt_v32_base_identical_to_codex_reading=ok2,
                      v33_unchanged_12_identical_to_codex_v32=ok3, v33_changed_6_differ_only_as_expected=ok4,
                      codex_v32_pptx_sha256='1b6988f3e55dc6bcf7e81d0ba4ec35b11ed2a0790a1357ba6e6185d22b08f28d',
                      files={k: hashlib.sha256(open(p, 'rb').read()).hexdigest() for k, p in
                             (('codex_pptx_json', sys.argv[1]), ('delivered_v32', sys.argv[2]), ('rebuilt_v32_base', sys.argv[3]),
                              ('v33', sys.argv[4]))})
json.dump(res, open(sys.argv[5], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k in ('delivered_v32_vs_codex', 'rebuilt_v32_base_vs_codex', 'v33_unchanged_vs_codex'):
    bad = [r for r in res[k] if not all(r[x] for x in KEYS)]
    print(k, 'all identical' if not bad else bad)
print('v33_changed_vs_codex', [(r['slide'], r['differs']) for r in res['v33_changed_vs_codex']])
print(res['summary'])
