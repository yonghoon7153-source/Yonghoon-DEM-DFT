#!/usr/bin/env python3
"""LHS 구조 디스크립터 **일괄 수확** — `lhs_descriptor_harvest.py` 를 케이스마다 돌린다.

왜 이 스크립트가 있나 (2026-09-17, 원장 `LHS-02`)
───────────────────────────────────────────────────────────────────────────────
`lhs_descriptor_harvest.py` 는 **케이스 단위** 도구다 (`--case --atom --contact
--mesh/--plate-z --n-types`).  130 개를 한 번에 도는 배치가 없어서 측정 7열이
`0/130` 으로 비어 있었고, 그것이 경향 분석 전체의 병목이었다.

★ **원자료가 있는 127 건은 지금 수확할 수 있다** — 나머지를 기다릴 필요가 없다.

⚠ 코호트 131 행 = RAW_OK 127 + `RAW_MISSING_CONTACT` **3** (`lhs00_034` · `lhs00_089` ·
  `lhs00_098`) + 케이스가 아닌 행 1 (`perc`).  ⛔ 옛 표기 *"남은 2 건"* 은 **틀렸다**
  (034 가 빠져 있었다, 2026-09-17).  사유도 "아직 도는 중" 이 아니라 **contact 덤프 결손**이다:
  089·098 은 봉인(2026-09-14) 시점에 진행 중이었으니 끝나면 채워지지만, **034 는 사유가
  같은지 확인되지 않았다** — 그냥 기다리면 오지 않을 수 있다.
  ⇒ 나중에 채울 때는 `--case lhs00_034` 처럼 **한 건씩** 돌려 실제로 열리는지 본다.

⛔ **짝짓기 규칙을 여기서 새로 만들지 않는다** (규율 ①).
   atom↔contact 짝은 `docs/data/area_s2_cohort.tsv` 에 **이미 봉인돼 있다**
   (`atom_file` · `contact_file` + 각 `sha256`).  그 파일이 정본이다.
   ⚠ 짝의 step 이 어긋나는 것은 **정상**이다 — 생산이 읽는 atom 덤프와 contact 덤프가
     5,000 스텝 어긋난다 (같은 정지 단계, 원장 `SELF-30`).  그것을 "고치려" 하지 말 것.

⚠ **`--n-types` 는 자동 추론하지 않는다.**  수확기 자신이 거부한다 ("AM_P 가 0개면
  오사상된다").  코호트 TSV 의 `n_types` 열을 그대로 넘긴다
  (실측 대응: bimodal→3 97건 · mono_AM_S→2 15건 · mono_AM_P→2 15건).

⚠ **플래튼(mesh)은 TSV 에 없다** — 유일하게 이 스크립트가 고르는 값이다.  그래서
  고른 근거를 **매 케이스마다 기록**한다 (`mesh_pick` = exact | none — `latest_le` 는 LHS-11 로 폐지).
  ⛔ 못 찾으면 추측하지 않고 그 케이스를 **건너뛰고 사유를 남긴다**.

사용 (저자 기계)
───────────────────────────────────────────────────────────────────────────────
    python3 scripts/lhs_harvest_batch.py --skip-sha --out-dir docs/data/lhs_descriptors
    python3 scripts/lhs_harvest_batch.py --verify-sha            # 느리지만 봉인 대조
    python3 scripts/lhs_harvest_batch.py --case lhs00_098        # 나중에 1건만 채우기

⚠ `--verify-sha` / `--skip-sha` 중 **하나를 반드시 골라야 한다**.  기본값을 두지 않는 것은
  의도한 것이다 — 봉인 대조를 했는지 안 했는지가 산출물에 남아야 한다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COHORT = ROOT / 'docs' / 'data' / 'area_s2_cohort.tsv'
HARVEST = ROOT / 'scripts' / 'lhs_descriptor_harvest.py'


def require_harvest(path: Path) -> None:
    """수확기가 **실제로 있는지** 먼저 본다 — dry-run 에서도 선다.

    ⚠ 이 검사가 없어서 실사고가 났다 (2026-09-17).  `ROOT` 는 이 스크립트의
      `parent.parent` 라, 리포 밖(`/tmp/lhsh/`)에 복사해 돌리면 `ROOT=/tmp` 가 되고
      `HARVEST=/tmp/scripts/lhs_descriptor_harvest.py` 라는 **없는 경로**가 된다.
      그런데 dry-run 은 수확기를 부르지 않으므로 `127/127 DRY_RUN` 으로 **초록**이
      나온다 — 실행하면 127 건이 전부 `HARVEST_FAILED` 로 죽는다.
      = CLAUDE.md 규율 ⑤ 의 false-green 이 **경로 층**에서 재현된 것이다.
      ⇒ 리허설이 본번과 **같은 전제**를 밟게 만든다.
    """
    if not path.is_file():
        sys.exit(
            f'⛔ 수확기가 없다 — {path}\n'
            f'   이 스크립트의 ROOT 는 자기 위치에서 정해진다 (parent.parent = {ROOT}).\n'
            f'   리포 밖에 복사해 돌리면 수확기를 못 찾는다.\n'
            f'   ⇒ **리포 체크아웃 안에서** 돌릴 것:\n'
            f'        cd ~/Yonghoon-DEM-DFT && python3 scripts/lhs_harvest_batch.py ...')

RE_STEP = re.compile(r'_(\d+)\.liggghts$')
RE_MESH = re.compile(r'mesh_(\d+)\.stl$', re.I)


def read_cohort(path: Path):
    """봉인된 코호트를 읽는다 — `#` 주석 줄은 헤더가 아니다.

    ⚠ 이 한 줄이 실제로 사고를 냈다: 주석을 헤더로 읽으면 `csv.DictReader` 가
      0 행을 돌려주고 검사가 **조용히 초록**이 된다 (CLAUDE.md 규율 ⑤).
    """
    lines = [l for l in path.read_text(encoding='utf-8').splitlines(keepends=True)
             if not l.lstrip().startswith('#')]
    return list(csv.DictReader(lines, delimiter='\t'))


def sha256_of(p: Path, _buf=1 << 20) -> str:
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        while True:
            b = fh.read(_buf)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def step_of(name: str) -> int | None:
    m = RE_STEP.search(name)
    return int(m.group(1)) if m else None


def pick_mesh(atom: Path):
    """플래튼 STL 을 고르고 **고른 근거를 같이 돌려준다**.

    exact     — atom 과 같은 step 의 mesh 가 있다 (가장 좋다)
    latest_le — 같은 step 이 없어 atom step **이하**의 최신 것을 썼다
    none      — 없다 ⇒ 호출부가 이 케이스를 건너뛴다

    ⛔ atom step **위**의 mesh 는 고르지 않는다 — 플래튼이 그 뒤로 더 내려갔을 수 있어
      침대와 다른 시점의 경계를 쓰게 된다.
    """
    post = atom.parent
    if not post.is_dir():
        return None, 'none', 'post 디렉터리 없음'
    cand = []
    for p in post.glob('mesh_*.stl'):
        m = RE_MESH.search(p.name)
        if m:
            cand.append((int(m.group(1)), p))
    if not cand:
        return None, 'none', 'mesh_*.stl 없음'
    a = step_of(atom.name)
    if a is not None:
        for s, p in cand:
            if s == a:
                return p, 'exact', f'step {s}'
        le = [(s, p) for s, p in cand if s <= a]
        #  ⛔ LHS-11 (2026-09-24): 옛 판은 여기서 `latest_le` 로 **조용히** 이른 메시를 썼다 — 97/130 건이 평균 150만 step
        #    이른 (압축 중) 플래튼을 받아 porosity 가 부풀었다 (옮길 때 메시를 문자열 정렬로 골라 99만대만 넘어온 탓).
        #    같은 step 이 없으면 **거부**한다 — 원본에서 같은 step 메시를 받아 올 것.
        if le:
            s, p = max(le)
            return None, 'none', f'같은 step 메시 없음 — atom step {a} · 아래 최신 mesh step {s} (차 {a - s}) · 거부 (LHS-11)'
        return None, 'none', f'atom step {a} 이하의 mesh 가 없다'
    return None, 'none', 'atom step 미상 — 메시 시점을 맞출 수 없어 거부 (LHS-11)'


def remap(path_str: str, frm: str, to: str) -> Path:
    if frm and to and path_str.startswith(frm):
        return Path(to + path_str[len(frm):])
    return Path(path_str)


def run_one(row, args, out_dir: Path):
    case = row['case']
    rec = {'case': case, 'n_types': row.get('n_types'),
           'design_family': row.get('design_family')}
    atom = remap(row['atom_file'], args.root_from, args.root_to)
    contact = remap(row['contact_file'], args.root_from, args.root_to)
    rec['atom'] = str(atom)
    rec['contact'] = str(contact)

    for label, p in (('atom', atom), ('contact', contact)):
        if not p.is_file():
            rec.update(status='MISSING_RAW', why=f'{label} 파일 없음: {p}')
            return rec

    if args.verify_sha:
        for label, p, want in (('atom', atom, row.get('atom_sha256')),
                               ('contact', contact, row.get('contact_sha256'))):
            if not want:
                rec.update(status='NO_SEAL_SHA', why=f'{label} sha 가 TSV 에 없다')
                return rec
            got = sha256_of(p)
            if got != want:
                rec.update(status='SHA_MISMATCH',
                           why=f'{label} 봉인 {want[:12]}… ≠ 실제 {got[:12]}…')
                return rec
        rec['sha_verified'] = True
    else:
        #  ⚠ 안 했다는 사실을 산출물에 남긴다 — "했는지 모르는" 상태를 만들지 않는다.
        rec['sha_verified'] = False

    mesh, pick, why = pick_mesh(atom)
    rec['mesh_pick'] = pick
    rec['mesh_why'] = why
    if mesh is None:
        rec.update(status='NO_MESH', why=f'플래튼을 못 골랐다 — {why}')
        return rec
    rec['mesh'] = str(mesh)

    nt = (row.get('n_types') or '').strip()
    if nt not in ('2', '3'):
        rec.update(status='BAD_NTYPES', why=f'n_types={nt!r} — 2 또는 3 이어야 한다')
        return rec

    out_json = out_dir / f'{case}.json'
    cmd = [sys.executable, str(HARVEST), '--case', case,
           '--atom', str(atom), '--contact', str(contact),
           '--mesh', str(mesh), '--n-types', nt, '--out', str(out_json)]
    if args.allow_any_bc:
        cmd.append('--allow-any-bc')
    rec['cmd'] = ' '.join(cmd)
    if args.dry_run:
        rec.update(status='DRY_RUN')
        return rec
    try:
        pr = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        rec.update(status='TIMEOUT', why=f'{args.timeout}s 초과')
        return rec
    rec['rc'] = pr.returncode
    if pr.returncode != 0:
        rec.update(status='HARVEST_FAILED',
                   why=(pr.stderr or pr.stdout or '').strip().splitlines()[-1:] or ['(출력 없음)'])
        return rec
    rec.update(status='OK', out=str(out_json))
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(description='LHS 디스크립터 일괄 수확 (LHS-02)')
    ap.add_argument('--cohort', default=str(COHORT))
    ap.add_argument('--out-dir', default=str(ROOT / 'docs' / 'data' / 'lhs_descriptors'))
    ap.add_argument('--case', action='append', default=[],
                    help='이 케이스만 (여러 번 줄 수 있다). 생략하면 RAW_OK 전부')
    ap.add_argument('--root-from', default='',
                    help='TSV 경로의 접두사 (예 /home/yonghoon71/lhs_local)')
    ap.add_argument('--root-to', default='', help='실제 경로 접두사로 치환')
    #  ⚠ `required=True` 로 두면 `--selftest` 까지 막힌다 (검사는 이 선택과 무관하다).
    #    그래서 그룹은 선택적으로 두고, **실제로 돌 때만** 아래에서 강제한다.
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--verify-sha', action='store_true',
                   help='봉인 sha256 과 대조한다 (느리다 — 127×2 파일)')
    g.add_argument('--skip-sha', action='store_true',
                   help='대조를 건너뛴다.  산출물에 sha_verified=false 로 남는다')
    ap.add_argument('--allow-any-bc', action='store_true')
    ap.add_argument('--dry-run', action='store_true', help='명령만 짜고 돌리지 않는다')
    ap.add_argument('--timeout', type=int, default=1800)
    ap.add_argument('--summary', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not (a.verify_sha or a.skip_sha):
        ap.error('--verify-sha 또는 --skip-sha 중 하나를 골라야 한다 — '
                 '봉인 대조를 했는지가 산출물에 남아야 하므로 기본값을 두지 않는다')
    a.verify_sha = bool(a.verify_sha)

    #  ⛔ dry-run 이든 본번이든 **똑같이** 여기서 선다 (리허설이 본번과 같은 전제를 밟도록).
    require_harvest(HARVEST)

    rows = read_cohort(Path(a.cohort))
    if not rows:
        sys.exit(f'⛔ 코호트가 0 행이다 — {a.cohort} (주석 줄만 읽은 것은 아닌지 확인)')
    pick = [r for r in rows if r['status'] == 'RAW_OK']
    if a.case:
        want = set(a.case)
        pick = [r for r in rows if r['case'] in want]
        miss = want - {r['case'] for r in pick}
        if miss:
            sys.exit(f'⛔ 코호트에 없는 케이스: {sorted(miss)}')

    out_dir = Path(a.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f'수확 대상 {len(pick)} 건 · sha 대조 {"함" if a.verify_sha else "**안 함**"}'
          + ('  · DRY-RUN' if a.dry_run else ''))

    recs, n_ok = [], 0
    for i, r in enumerate(pick, 1):
        rec = run_one(r, a, out_dir)
        recs.append(rec)
        ok = rec['status'] in ('OK', 'DRY_RUN')
        n_ok += ok
        mark = '✓' if ok else '⛔'
        extra = '' if ok else f"  {rec.get('why')}"
        print(f'  [{i:>3}/{len(pick)}] {mark} {rec["case"]:<14} {rec["status"]}{extra}')

    summary = {'n_target': len(pick), 'n_ok': n_ok,
               'sha_verified': a.verify_sha, 'dry_run': a.dry_run,
               'cohort': a.cohort, 'out_dir': str(out_dir), 'records': recs}
    sp = Path(a.summary) if a.summary else out_dir / '_batch_summary.json'
    sp.write_text(json.dumps(summary, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'\n  성공 {n_ok} / {len(pick)}  → 요약 {sp}')
    if n_ok != len(pick):
        print('  ⛔ 실패가 있다 — 요약의 `why` 를 볼 것.  '
              '빈칸을 0 으로 채우지 말 것 (LHS-02 의 취지).')
        return 1
    return 0


def _selftest():
    import tempfile
    fail = []

    def chk(name, cond, extra=''):
        (print if cond else (lambda s: (fail.append(name), print(s))[1]))(
            f'  {"✓" if cond else "✗"} {name}' + (f'   {extra}' if extra else ''))

    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        #  ── 주석 줄을 헤더로 읽지 않는다 (실사고 재현) ──
        tsv = t / 'c.tsv'
        tsv.write_text('# 주석\ncase\tstatus\tn_types\tatom_file\tcontact_file\n'
                       'x1\tRAW_OK\t3\t/a/atom_100.liggghts\t/a/contact_95.liggghts\n',
                       encoding='utf-8')
        rows = read_cohort(tsv)
        chk('★★ `#` 주석 줄을 헤더로 읽지 않는다 (0행 false-green 방지)',
            len(rows) == 1 and rows[0]['case'] == 'x1', f'n={len(rows)}')

        #  ── mesh 고르기 ──
        post = t / 'post'
        post.mkdir()
        atom = post / 'atom_2425000.liggghts'
        atom.write_text('x')
        chk('mesh 가 없으면 `none` — 추측하지 않는다', pick_mesh(atom)[1] == 'none')
        (post / 'mesh_2420000.stl').write_text('x')
        m, pk, why = pick_mesh(atom)
        chk('★ LHS-11: 같은 step 이 없으면 **거부** (`none`) — 이른 메시로 내려가지 않는다', pk == 'none' and m is None, why)
        (post / 'mesh_2425000.stl').write_text('x')
        m, pk, why = pick_mesh(atom)
        chk('★★ 같은 step 이 있으면 `exact` 를 고른다', pk == 'exact' and m.name == 'mesh_2425000.stl')
        (post / 'mesh_2430000.stl').write_text('x')
        m, pk, why = pick_mesh(atom)
        chk('★★ atom step **위**의 mesh 는 고르지 않는다 (침대와 다른 시점의 경계)',
            m.name == 'mesh_2425000.stl', m.name)
        atom2 = post / 'atom_2000000.liggghts'
        atom2.write_text('x')
        chk('★ atom 보다 이른 mesh 만 있어도 거부 (`none`)', pick_mesh(atom2)[1] == 'none')

        #  ── step 파서 ──
        chk('step 파서', step_of('atom_2425000.liggghts') == 2425000)
        chk('step 없는 이름은 None', step_of('atom.liggghts') is None)

        #  ── 경로 치환 ──
        chk('root 치환', str(remap('/a/b/c', '/a', '/z')) == '/z/b/c')
        chk('접두사가 다르면 그대로', str(remap('/q/b', '/a', '/z')) == '/q/b')

        #  ── sha ──
        f = t / 'f'
        f.write_bytes(b'hello')
        chk('sha256', sha256_of(f) == hashlib.sha256(b'hello').hexdigest())

        #  ── 누락은 건너뛰고 **사유를 남긴다** ──
        class A:
            root_from = root_to = ''
            verify_sha = False
            allow_any_bc = False
            dry_run = True
            timeout = 60
        rec = run_one({'case': 'x', 'n_types': '3', 'design_family': 'bimodal',
                       'atom_file': '/nope/atom_1.liggghts',
                       'contact_file': '/nope/contact_1.liggghts'}, A(), t)
        chk('★★ 원자료가 없으면 `MISSING_RAW` 로 **사유와 함께** 선다 (조용히 넘기지 않는다)',
            rec['status'] == 'MISSING_RAW' and 'atom' in rec['why'])
        rec = run_one({'case': 'x', 'n_types': '9', 'design_family': 'bimodal',
                       'atom_file': str(atom), 'contact_file': str(atom)}, A(), t)
        chk('★ n_types 가 2·3 이 아니면 거부 (자동 추론하지 않는다)',
            rec['status'] == 'BAD_NTYPES')
        rec = run_one({'case': 'x', 'n_types': '3', 'design_family': 'bimodal',
                       'atom_file': str(atom), 'contact_file': str(atom)}, A(), t)
        chk('★ 정상 입력은 DRY_RUN 까지 간다', rec['status'] == 'DRY_RUN', rec.get('why', ''))
        chk('★★ sha 대조를 **안 했다는 사실**이 기록에 남는다', rec.get('sha_verified') is False)
        chk('★ 고른 mesh 의 근거가 기록에 남는다', rec.get('mesh_pick') in ('exact', 'latest_le'))

        #  ── ★★ 실사고 재현: 리포 밖에서 돌리면 수확기를 못 찾는다 ──
        #     dry-run 이 `127/127` 초록을 내고 본번이 127건 전부 죽은 사고 (2026-09-17).
        missing = t / 'nope' / 'lhs_descriptor_harvest.py'
        try:
            require_harvest(missing)
            hit = False
        except SystemExit as e:
            hit = '수확기가 없다' in str(e)
        chk('★★ 수확기가 없으면 **선다** — 없는 경로로 돌지 않는다', hit)

        real = t / 'lhs_descriptor_harvest.py'
        real.write_text('#')
        try:
            require_harvest(real)
            ok = True
        except SystemExit:
            ok = False
        chk('수확기가 있으면 통과한다', ok)

        #  ⛔ 핵심 — **dry-run 에서도** 선다.  리허설이 본번과 같은 전제를 밟아야
        #     "127/127 DRY_RUN" 이 실행 가능성을 뜻하게 된다.
        #  ⚠ `import lhs_harvest_batch` 는 __main__ 으로 돌 때 **두 번째 사본**을 만든다 —
        #    그 사본의 전역을 바꿔도 지금 도는 코드에는 영향이 없다 (이 검사가 그걸 잡았다).
        #    지금 **도는** 모듈을 잡아야 한다.
        _self = sys.modules[__name__]
        _keep = _self.HARVEST
        _self.HARVEST = missing
        try:
            rc = main(['--skip-sha', '--dry-run', '--cohort', str(tsv),
                       '--out-dir', str(t / 'o')])
            stopped = False
        except SystemExit as e:
            stopped = '수확기가 없다' in str(e)
        finally:
            _self.HARVEST = _keep
        chk('★★★ **dry-run 도** 같은 전제에서 선다 (리허설 false-green 차단)', stopped)

    print('\nlhs_harvest_batch SELFTEST %d PASS %s'
          % (16 - len(fail), 'ALL GREEN' if not fail else f'FAIL {fail}'))
    return 1 if fail else 0


if __name__ == '__main__':
    raise SystemExit(main())
