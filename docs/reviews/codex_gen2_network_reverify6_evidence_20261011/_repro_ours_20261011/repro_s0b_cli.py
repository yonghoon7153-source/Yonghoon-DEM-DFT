"""재검증 6 G2RR6-01 — Codex S0b CLI 반례 일곱을 우리 트리 사본에서 재현 (읽기 전용 · 스크래치).

사용: python3 -I -B repro_s0b_cli.py <tree> <evidence_dir> <out_json>
  tree         = git archive HEAD (scripts · webapp) 를 푼 사본
  evidence_dir = Codex 묶음 evidence/ (r6_s0b_<label>.input.json — 신뢰하지 않는 입력 · JSON 으로만 읽는다)
정상 관통 · 비관통 · clamp 게시 폴더 = 이 트리의 실 생산자 게시 (test_gen2_publication_handover._publish) — Codex 와 같은 방식.
"""
import contextlib
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

tree, evd, out = (Path(a).resolve() for a in sys.argv[1:4])
sys.path[:0] = [str(tree / 'scripts'), str(tree / 'webapp')]
import site                                # noqa: E402 — -I 는 사용자 site 를 끈다 (requests 등) · 경로만 명시로 더한다
sys.path.append(site.getusersitepackages())

import g2_network_reread as RR            # noqa: E402
import app                                 # noqa: E402
import test_gen2_publication_handover as PH  # noqa: E402

LABELS = ('positive', 'raw_sha_missing', 'raw_sha_mismatch', 'negative_area_positive', 'negative_area_missing',
          'raw_sha_flag_false', 'actual_permission_error')
CODEX = {'positive': (0, 0), 'raw_sha_missing': (0, 0), 'raw_sha_mismatch': (0, 0), 'negative_area_positive': (0, 0),
         'negative_area_missing': (0, 0), 'raw_sha_flag_false': (1, 1), 'actual_permission_error': (1, 1)}
tmp = Path(tempfile.mkdtemp(prefix='r6_s0b_'))
with contextlib.redirect_stdout(io.StringIO()):
    pub = {bed: PH._publish(app, 'baseline', bed=bed) for bed in ('through', 'nonthrough', 'clamp')}
rows = []
for lab in LABELS:
    doc = json.loads((evd / f'r6_s0b_{lab}.input.json').read_text(encoding='utf-8'))
    sm = tmp / f'smoke_{lab}'
    (sm / 'work' / 'results').mkdir(parents=True)
    for bed, (d, _st, _f, _rid) in pub.items():
        shutil.copytree(d, sm / 'work' / 'results' / bed)
    (sm / 'smoke_report.json').write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
    jp = tmp / f'out_{lab}.json'
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = RR.main(['--smoke-root', str(sm), '--json', str(jp)])
        except SystemExit as e:                  # noqa: PERF203
            rc = e.code
    j = json.loads(jp.read_text(encoding='utf-8')) if jp.exists() else {}
    r15 = (doc.get('reports') or {}).get('case15_network')
    pure = RR.case15_negctl_s0b_problems('case15_network', r15, doc.get('checks'), (doc.get('timings') or {}).get('case15_network'))
    s0b = next((m for m in j.get('meta') or [] if str(m.get('name', '')).startswith('S0b')), {})
    rows.append(dict(label=lab, rc=rc, n_fail=j.get('n_fail'), codex_rc_nfail=list(CODEX[lab]),
                     same_as_codex=[rc, j.get('n_fail')] == list(CODEX[lab]), s0b_ok=s0b.get('ok'),
                     s0b_detail=(str(s0b.get('detail'))[:400]), pure_problems=[p[:300] for p in pure],
                     meta_ok={str(m.get('name', ''))[:3]: m.get('ok') for m in j.get('meta') or []}))
summary = dict(tree_head=(tree / 'HEAD_SHA').read_text().strip(), published={k: v[1] for k, v in pub.items()}, rows=rows,
               all_same_as_codex=all(r['same_as_codex'] for r in rows))
out.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding='utf-8')
for r in rows:
    print(f"{r['label']:26s} rc {r['rc']} n_fail {r['n_fail']} · Codex {r['codex_rc_nfail']} · same {r['same_as_codex']} · 순수 문제 {len(r['pure_problems'])}")
print('all_same_as_codex', summary['all_same_as_codex'], '· published', summary['published'])
shutil.rmtree(tmp, ignore_errors=True)
