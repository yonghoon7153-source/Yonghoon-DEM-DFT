#!/usr/bin/env python3
"""S3 코호트 봉인 — raw 가용성 **전수** 목록 + 파일 지문 → `docs/data/area_s2_cohort.tsv`.

계약 §5-v3 ③ (Codex 2라운드): *"raw 가용성 전수 목록·포함/제외 사유·파일 지문을 독립적으로
봉인하고, **build_network 성공 여부를 본 뒤 제외하지 말고** 가용 원자료의 기술적 실패를
상태로 보존"*.

★ 이 도구는 **솔버를 부르지 않는다**.  파일이 있는지·해시가 무엇인지·덱이 어느 설계족인지만
  적는다.  포함/제외는 이 파일이 정하고, 이후 S3 런은 이 목록 **전부**를 돌려 실패를 REFUSED 로
  보존한다 (성공한 것만 골라 코호트를 만들지 않는다).
★ 지문 = atom·contact 덤프와 덱의 sha256.  S3 매니페스트가 같은 지문을 적어야 대조가 성립한다.
★ 설계족은 덱 첫 줄 주석 `# lhs00_100: mono_AM_S (2-type) | LHS design` 에서 읽는다 —
  Codex 가 지적한 사실(mono 15+15, bimodal 0)이 여기 **열로** 남는다.

사용:
  python3 scripts/seal_area_cohort.py --webapp ~/lhs_local --deck-dir ~/lhs_local \\
      --out docs/data/area_s2_cohort.tsv
  python3 scripts/seal_area_cohort.py --selftest
"""
from __future__ import annotations
import argparse
import datetime as _dt
import hashlib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


_PC = _load('_pc_seal', SCRIPTS / 'plastic_coverage.py')

COLS = ['case', 'status', 'design_family', 'n_types', 'deck', 'deck_sha256',
        'atom_file', 'atom_sha256', 'contact_file', 'contact_sha256', 'reason']
HEAD_RE = re.compile(r'^#\s*(\S+):\s*(\S+)\s*\((\d+)-type\)')


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def design_family(deck: Path):
    """덱 첫 줄 주석에서 (family, n_types).  없으면 ('UNKNOWN', '')."""
    try:
        first = deck.read_text(encoding='utf-8', errors='replace').splitlines()[0]
    except Exception:
        return 'UNKNOWN', ''
    m = HEAD_RE.match(first.strip())
    return (m.group(2), m.group(3)) if m else ('UNKNOWN', '')


def seal_case(case_dir: Path, deck_dir: Path | None) -> dict:
    """한 케이스 — **거부하지 않는다**.  없는 것은 status 로 적는다."""
    row = {k: '' for k in COLS}
    row['case'] = case_dir.name
    dk = None
    for cand in ([deck_dir / case_dir.name / f'input_{case_dir.name}.liggghts',
                  deck_dir / f'input_{case_dir.name}.liggghts'] if deck_dir else []) + \
                [case_dir / f'input_{case_dir.name}.liggghts']:
        if cand.is_file():
            dk = cand; break
    hit = None
    for d in [case_dir] + sorted(q for q in case_dir.glob('post_*') if q.is_dir()):
        a, c = _PC._find_case_files(str(d))
        if a and c and a.endswith('.liggghts') and c.endswith('.liggghts'):
            hit = (Path(a), Path(c)); break
    problems = []
    row['design_family'] = 'UNKNOWN'          # 덱이 없거나 헤더가 없으면 UNKNOWN (빈 문자열 금지)
    if dk is None:
        problems.append('DECK_MISSING')
    else:
        row['deck'] = str(dk); row['deck_sha256'] = sha256(dk)
        row['design_family'], row['n_types'] = design_family(dk)
    if hit is None:
        a = _PC._pick_latest(str(case_dir), 'atom_*.liggghts')
        for d in sorted(q for q in case_dir.glob('post_*') if q.is_dir()):
            a = a or _PC._pick_latest(str(d), 'atom_*.liggghts')
        problems.append('RAW_MISSING_CONTACT' if a else 'RAW_MISSING_ATOM')
    else:
        row['atom_file'], row['contact_file'] = str(hit[0]), str(hit[1])
        row['atom_sha256'], row['contact_sha256'] = sha256(hit[0]), sha256(hit[1])
    row['status'] = 'RAW_OK' if not problems else '+'.join(problems)
    row['reason'] = ('포함: 원자료·덱 실재 (솔버 성공 여부는 보지 않았다)' if not problems
                     else '제외 사유 = ' + ', '.join(problems) + ' (기술적 결손; 솔버 이전)')
    return row


def seal(root: Path, deck_dir: Path | None):
    rows = [seal_case(d, deck_dir) for d in sorted(q for q in root.iterdir() if q.is_dir())
            if d.name != 'done.txt']
    return rows


def write_tsv(rows, out: Path, root: Path):
    sha = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--short=9', 'HEAD'],
                         capture_output=True, text=True).stdout.strip()
    fam = {}
    for r in rows:
        fam[r['design_family']] = fam.get(r['design_family'], 0) + 1
    hdr = [f'# S3 코호트 봉인 — raw 가용성 전수 목록 (계약 §5-v3 ③).  생성 {_dt.date.today().isoformat()} · 도구 커밋 {sha}',
           f'# root = {root}',
           '# ⛔ 솔버를 부르지 않았다 — 포함/제외는 파일 실재로만.  이 목록 전부를 S3 가 돌리고 실패는 REFUSED 로 보존한다.',
           '# 설계족 분포: ' + ' · '.join(f'{k} {v}' for k, v in sorted(fam.items())),
           '# ⚠ 설계족이 mono 뿐이면 AREA-11(AM_P–AM_S · AM_P 반경 이종쌍) 효과는 이 코호트로 검증할 수 없다.',
           '\t'.join(COLS)]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(hdr) + '\n' + '\n'.join('\t'.join(r[k] for k in COLS) for r in rows) + '\n',
                   encoding='utf-8')


def _selftest() -> int:
    import tempfile
    ok = True
    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)
    print('코호트 봉인')
    t = Path(tempfile.mkdtemp())
    def mk(name, fam='mono_AM_S (2-type)', atom=True, contact=True, deck=True):
        d = t / name; p = d / f'post_{name}'; p.mkdir(parents=True)
        if deck:
            (d / f'input_{name}.liggghts').write_text(f'# {name}: {fam} | LHS design\nvariable r_SE equal 0.001\n')
        if atom:
            (p / 'atom_100.liggghts').write_text('ITEM: ATOMS id type radius x y z\n1 1 0.0005 0 0 0\n')
        if contact:
            (p / 'contact_100.liggghts').write_text('ITEM: ENTRIES c_cpl[1]\n')
        return d
    mk('lhs00_900'); mk('lhs00_901', fam='bimodal (3-type)'); mk('lhs00_902', contact=False)
    mk('lhs00_903', deck=False); mk('lhs00_904', atom=False, contact=False)
    rows = seal(t, t)
    by = {r['case']: r for r in rows}
    chk('① 전수: 폴더 5개 전부 행이 있다 (성공한 것만 고르지 않는다)', len(rows) == 5, str([r['case'] for r in rows]))
    chk('② RAW_OK 케이스는 세 파일 sha256 이 64자', by['lhs00_900']['status'] == 'RAW_OK'
        and all(len(by['lhs00_900'][k]) == 64 for k in ('atom_sha256', 'contact_sha256', 'deck_sha256')))
    chk('③ 설계족을 덱 헤더에서 읽는다', by['lhs00_900']['design_family'] == 'mono_AM_S'
        and by['lhs00_901']['design_family'] == 'bimodal' and by['lhs00_901']['n_types'] == '3')
    chk('④ 결손은 거부가 아니라 상태다', by['lhs00_902']['status'] == 'RAW_MISSING_CONTACT'
        and by['lhs00_903']['status'] == 'DECK_MISSING' and by['lhs00_904']['status'] == 'RAW_MISSING_ATOM',
        str({k: by[k]['status'] for k in ('lhs00_902', 'lhs00_903', 'lhs00_904')}))
    # ⑤ 판별력: 파일 한 바이트를 바꾸면 지문이 바뀐다
    p = t / 'lhs00_900' / 'post_lhs00_900' / 'atom_100.liggghts'
    before = by['lhs00_900']['atom_sha256']
    p.write_text(p.read_text() + ' ')
    after = seal_case(t / 'lhs00_900', t)['atom_sha256']
    chk('⑤ 판별력: 원자료 1바이트 변화 → sha256 변화', before != after)
    out = t / 'cohort.tsv'; write_tsv(rows, out, t)
    txt = out.read_text(encoding='utf-8')
    chk('⑥ TSV 헤더에 설계족 분포와 "솔버를 부르지 않았다" 가 있다',
        '설계족 분포: UNKNOWN 1 · bimodal 1 · mono_AM_S 3' in txt and '솔버를 부르지 않았다' in txt)
    print('코호트 봉인 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description='S3 코호트 봉인 (raw 전수 + sha256, 솔버 무관)')
    ap.add_argument('--webapp', default='', help='케이스 폴더들을 담은 root (예: ~/lhs_local)')
    ap.add_argument('--deck-dir', default='')
    ap.add_argument('--out', default=str(ROOT / 'docs' / 'data' / 'area_s2_cohort.tsv'))
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.webapp:
        print('⛔ --webapp 이 필요하다'); return 2
    root = Path(a.webapp).expanduser().resolve()
    deck = Path(a.deck_dir).expanduser().resolve() if a.deck_dir else None
    rows = seal(root, deck)
    if not rows:
        print(f'⛔ {root} 에 케이스 폴더가 없다'); return 2
    write_tsv(rows, Path(a.out), root)
    st = {}
    for r in rows:
        st[r['status']] = st.get(r['status'], 0) + 1
    fam = {}
    for r in rows:
        fam[r['design_family']] = fam.get(r['design_family'], 0) + 1
    print(f'케이스 {len(rows)} · 상태 {st} · 설계족 {fam}')
    print(f'→ {a.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
