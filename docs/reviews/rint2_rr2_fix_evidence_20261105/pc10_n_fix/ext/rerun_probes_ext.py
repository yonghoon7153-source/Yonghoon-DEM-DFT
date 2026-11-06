"""PC10 확장 — 탐침을 고치지 않고 이 판 (사본 나무 · 리포 밖) 에서 다시 돌려 지난 판 (8933b6781) 결과와 행을 대조한다 (관찰 기록 · 판정 아님).

usage: python3 -I rerun_probes_ext.py <사본 나무> <출력 폴더>
  사본 나무 = scripts/ (+ 고정물이 읽는 문서) · git 저장소 아님.  탐침 = 고치지 않은 원본 (바이트 sha256 을 적는다):
    ① 사전 공격 11 (이 폴더 pa11_probes/ = 그 회차 탐침 사본) probe_rej · probe_rr · probe_rr2 — 지난 판 결과 = pa11_probes/*_fixed.json (8933b6781)
    ② 사전 공격 10 리뷰어 (../../preattack10/) probe_units · probe_units2 · probe_ledger · probe_rcscan — 지난 판 = ../probe_rerun/*_after.json
    ③ PC10 고침 새 발견 (../../preattack10_fix/new_findings/probe_new.py) — 지난 판 = ../probe_rerun/probe_new_after.json
  행 = 탐침 JSON 의 첫 층 (rows 가 있으면 rows) · 모듈 경로 · 임시 폴더 · sha 칸은 대조에서 뺀다.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
HERE = Path(__file__).resolve().parent
EV = HERE.parent.parent                                      # docs/reviews/rint2_rr2_fix_evidence_20261105
SCR = TREE / 'scripts'
SKIP_KEYS = {'td', 'module', 'module_sha256', 'chain_module', 'is_new'}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def rows(d):
    r = d.get('rows', d) if isinstance(d, dict) else d
    if not isinstance(r, dict):
        return {'_value': r}
    out = {}
    for k, v in r.items():
        if k in SKIP_KEYS:
            continue
        if isinstance(v, dict) and k in ('L_run_log_text', 'SU_read'):
            for kk, vv in v.items():
                out[f'{k}/{kk}'] = vv
        else:
            out[k] = v
    return out


def scrub(v):
    """매번 다른 글 (임시 경로 · 원장 커밋 40 hex) 을 대조에서 뺀다 — /tmp/… = <tmp> · 40 hex = <sha>."""
    s = json.dumps(v, ensure_ascii=False, sort_keys=True)
    s = re.sub(r'/tmp/[^"\s\\]*', '<tmp>', s)
    return json.loads(re.sub(r'\b[0-9a-f]{40}\b', '<sha>', s))


PROBES = [
    # (이름, 탐침 경로, argv 꼴, 지난 판 결과)
    ('pa11_rej', HERE / 'pa11_probes' / 'probe_rej.py', 'tree', HERE / 'pa11_probes' / 'probe_rej_fixed.json'),
    ('pa11_rr', HERE / 'pa11_probes' / 'probe_rr.py', 'tree', HERE / 'pa11_probes' / 'probe_rr_fixed.json'),
    ('pa11_rr2', HERE / 'pa11_probes' / 'probe_rr2.py', 'tree', HERE / 'pa11_probes' / 'probe_rr2_fixed.json'),
    ('pa10_units', EV / 'preattack10' / 'probe_units.py', 'rr_scripts', EV / 'pc10_n_fix' / 'probe_rerun' / 'probe_units_after.json'),
    ('pa10_units2', EV / 'preattack10' / 'probe_units2.py', 'rr_scripts', EV / 'pc10_n_fix' / 'probe_rerun' / 'probe_units2_after.json'),
    ('pa10_ledger', EV / 'preattack10' / 'probe_ledger.py', 'scripts', EV / 'pc10_n_fix' / 'probe_rerun' / 'probe_ledger_after.json'),
    ('pa10_rcscan', EV / 'preattack10' / 'probe_rcscan.py', 'scripts', EV / 'pc10_n_fix' / 'probe_rerun' / 'probe_rcscan_after.json'),
    ('pc10_new', EV / 'preattack10_fix' / 'new_findings' / 'probe_new.py', 'scripts', EV / 'pc10_n_fix' / 'probe_rerun' / 'probe_new_after.json'),
]

OUT.mkdir(parents=True, exist_ok=True)
summary = {'tree_chain_sha256': sha(SCR / 'rint_r_chain.py'), 'tree_test_sha256': sha(SCR / 'test_rint_r_chain.py'), 'probes': {}}
for nm, probe, kind, prev in PROBES:
    outj = OUT / f'{nm}.json'
    argv = {'tree': [str(TREE), str(outj)], 'rr_scripts': [str(SCR), str(SCR), str(outj)], 'scripts': [str(SCR), str(outj)]}[kind]
    p = subprocess.run([sys.executable, '-I', '-B', str(probe), *argv], cwd=str(OUT), capture_output=True, text=True, timeout=3600)
    (OUT / f'{nm}.out').write_text(p.stdout + p.stderr, encoding='utf-8')
    rec = {'probe': str(probe.relative_to(EV)) if EV in probe.parents else str(probe), 'probe_sha256': sha(probe), 'rc': p.returncode}
    if outj.exists():
        a, b = rows(json.loads(prev.read_text(encoding='utf-8'))), rows(json.loads(outj.read_text(encoding='utf-8')))
        diff = {k: {'prev_8933b6781': scrub(a.get(k)), 'ext': scrub(b.get(k))} for k in sorted(set(a) | set(b)) if scrub(a.get(k)) != scrub(b.get(k))}
        rec.update(n_rows=len(set(a) | set(b)), n_diff=len(diff), diff=diff)
    else:
        rec['error'] = 'no output'
    summary['probes'][nm] = rec
    print(nm, 'rc', p.returncode, 'rows', rec.get('n_rows'), 'diff', rec.get('n_diff'), flush=True)
(OUT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
