#!/usr/bin/env python3
"""P09 — S06 재실행 (HEAD) 의 'docs_same_as_bundle 0/12 · 0/18' 이 등록 문서 비준 (바탕 글 변경) 때문인지 — 같은 생성식을 비준 전 문서 (fe23f2b83) 바탕으로
다시 만들면 Codex 묶음 문서와 바이트 같아야 한다.  또 F (실제 §3 절) 차이가 비준 문안의 §3 뿐인지.
재실행: cd <worktree> && python3 -I p09_s06_docdiff.py <worktree> <s06_out_dir>"""
import hashlib, json, re, subprocess, sys
from pathlib import Path
WT, S06 = Path(sys.argv[1]), Path(sys.argv[2])
BUNDLE = WT / 'docs/reviews/codex_lhs214cx_fix_recheck_evidence_20261020/evidence/s06'
SUPP = 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md'
sys.path.insert(0, str(WT / 'scripts'))
import supp20_input_receipt as sr  # noqa: E402


def show(rev, f):
    return subprocess.run(['git', 'show', f'{rev}:{f}'], cwd=WT, capture_output=True, check=True).stdout.decode('utf-8')


def base_of(registered):
    return re.sub(r"^## 3\.", "## 30.", re.sub(r"`code_fp_pending [0-9a-f]{64}`", "(pending removed for diagnostic)", registered), flags=re.M)


pre_base, head_base = base_of(show('fe23f2b83', SUPP)), base_of(show('HEAD', SUPP))
out = {}
same_pre = same_head = 0
names = sorted(p.name for p in (S06 / 'new_cases').glob('*.md'))
for n in names:
    ours = (S06 / 'new_cases' / n).read_text(encoding='utf-8')
    tail = ours[len(head_base) + 1:] if ours.startswith(head_base + '\n') else None
    bundle = (BUNDLE / 'new_cases' / n).read_bytes().replace(b'\r\n', b'\n').decode('utf-8')
    same_head += ours == bundle
    same_pre += tail is not None and (pre_base + '\n' + tail) == bundle
out['new_cases'] = dict(n=len(names), same_as_bundle_with_head_base=same_head, same_as_bundle_with_pre_base=same_pre)
nl = sorted(p.name for p in (S06 / 'newline_cases').glob('*.md'))
same_pre_nl = 0
for n in nl:
    ours = (S06 / 'newline_cases' / n).read_bytes()
    ending = b'\r\n' if n.endswith('_crlf.md') else (b'\r' if n.endswith('_cr.md') else b'\n')
    lf = ours.replace(ending, b'\n').decode('utf-8') if ending != b'\n' else ours.decode('utf-8')
    if not lf.startswith(head_base + '\n'):
        continue
    tail = lf[len(head_base) + 1:]
    rebuilt = (pre_base + '\n' + tail).replace('\n', ending.decode()).encode('utf-8')
    same_pre_nl += hashlib.sha256(rebuilt).hexdigest() == hashlib.sha256((BUNDLE / 'newline_cases' / n).read_bytes()).hexdigest()
out['newline_cases'] = dict(n=len(nl), same_as_bundle_with_pre_base=same_pre_nl)
# F: 실제 §3 절 — Codex 기록 (비준 전) = 비준 전 문서의 §3 절?
noimp = json.loads((BUNDLE / 'actual_noimpact.json').read_text(encoding='utf-8'))
pre_sec = list(sr._md_section(show('fe23f2b83', SUPP), 3, True))
out['F_codex_record_equals_pre_doc_section'] = pre_sec == noimp['new_section']
print(json.dumps(out, ensure_ascii=False, indent=1))
(S06 / 'p09_docdiff.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
