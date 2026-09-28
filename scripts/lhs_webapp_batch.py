#!/usr/bin/env python3
"""LHS 침대를 **웹앱 파이프라인 그대로** 돌려 코퍼스 (`case_master.csv`) 와 **같은 열**을 얻는다.

판단 J20 (1저자 비준 2026-09-28 — "✅ 만 이번에" · "채운 뒤 넘김").

왜 이 스크립트가 있나
───────────────────────────────────────────────────────────────────────────────
인계표 (`docs/data/lhs_handover_*.csv`) 의 측정 열은 수확기 (`lhs_descriptor_harvest.py`) 의
φ · 피복 · 공극률 · τ 뿐이다.  수영 님 ML 이 쓸 **배위수 · 퍼콜 · 응력 · Auerbach 파괴 · 기하 면적**
(09-19 전수 판정 `docs/param_audit_report_20260919.md` §2 의 ✅ 239 열) 은 웹앱 파이프라인만 낸다.

⛔ 그 열을 **새로 구현하지 않는다** (규율 ①).  웹앱 `run_pipeline` 을 그대로 부른다 — 뺀 것은
   그림 단계와 자동 DB 재구축 둘뿐이다 (`run_pipeline(figures=False, auto_db=False)`,
   `webapp/test_pipeline_provenance.py` T9 가 계산 단계 순서가 같다는 것을 지킨다).
   행을 만드는 것도 코퍼스와 같은 `export_master_csv.row_for` 다 ⇒ 열 이름이 코퍼스와 같다.

같은 프레임 보증 (fail-closed)
───────────────────────────────────────────────────────────────────────────────
  • 원자료 짝 (atom · contact · deck) = 봉인 코호트 `docs/data/area_s2_cohort.tsv` (`lhs_harvest_batch` 와 같은 정본)
  • 플래튼 메시 = `lhs_harvest_batch.pick_mesh` — atom 과 **같은 step** 만 (LHS-11)
  • 네 파일의 sha256 = **수확 JSON 의 `raw.*.sha256`** 과 같아야 한다 — 다르면 그 케이스를 거부한다
    (웹앱 열과 수확기 열이 **같은 침대 · 같은 프레임**이어야 한 행에 둘 수 있다)
  • type_map = 덱 판독 (`type_map_resolve`, 업로드 입구와 같은 게이트) = 수확 JSON 의 type_map
  • 스테이징 폴더에는 그 네 파일 링크와 meta.json **만** 둔다 — `run_pipeline` 은 폴더를 glob 한다
    (옛 파일이 남으면 다른 프레임이 섞인다: SELF-47)

⚠ 원격 저장소로 보내지 않는다 — import 전에 `SUPABASE_URL` · `SUPABASE_KEY` 를 빈 값으로 둔다
  (webapp/.env 의 setdefault 가 되살리지 못하게 **pop 이 아니라 빈 문자열**).
⚠ network solver 는 웹앱의 파일 lock 이 기계 전체에서 직렬화한다 — 이 배치는 순차 실행이다.

사용 (원자료가 있는 저자 기계 — WSL)
───────────────────────────────────────────────────────────────────────────────
    python3 scripts/lhs_webapp_batch.py --harvest-dir docs/data/lhs_descriptors_<날짜> \\
        --work ~/lhs_webapp_work --out-dir docs/data/lhs_webapp_<날짜> \\
        [--root-from <코호트 경로 접두사> --root-to <실제 접두사>]
    python3 scripts/lhs_webapp_batch.py … --case lhs00_000       # 한 건 먼저 (시간 · 산출 확인)
    python3 scripts/lhs_webapp_batch.py --selftest

산출 (`--out-dir`)
  • `metrics_flat.csv` — 케이스당 한 행, `row_for` 가 편 **전 열** (✅ 선별은 인계표 생성기가 한다)
  • `status.json`      — 케이스별 상태 (done · partial · failed · REFUSED) · 실패 단계 · 네 파일 sha ·
                          mode · type_map · 경과 시간 + 실행 코드 sha · dirty 여부
  full_metrics.json 원본은 `--work/results/<case>/` 에 남는다 (리포에 넣지 않는다 — 크다).
재개: done · partial 인 케이스는 건너뛴다 (`--force` 로 다시).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import lhs_harvest_batch as HB          # noqa: E402  (코호트 · 경로 치환 · 같은 step 메시 · sha — 새로 만들지 않는다)

SCHEMA = 'lhs_webapp_batch/v1'
DEF_HARVEST = ROOT / 'docs' / 'data' / 'lhs_descriptors_20260925'
KEEP_STATUS = ('done', 'partial')       # 재개 때 건너뛴다 — partial = 선택 단계만 실패 (Stage E 등)
RAW_KEYS = ('atom', 'contact', 'mesh', 'deck')


class Refuse(RuntimeError):
    """이 케이스는 돌리지 않는다 — 사유가 status.json 에 남는다."""


def prepare_env(work: Path) -> None:
    """웹앱 import **전에** 부른다 — 폴더를 작업 폴더로, 원격 저장소는 끈다."""
    os.environ['WEBAPP_UPLOAD_FOLDER'] = str(work / 'uploads')
    os.environ['WEBAPP_RESULTS_FOLDER'] = str(work / 'results')
    os.environ['WEBAPP_ARCHIVE_FOLDER'] = str(work / 'archive')
    #  pop 이 아니라 빈 값 — webapp/.env 로더가 os.environ.setdefault 로 되살리지 못한다
    os.environ['SUPABASE_URL'] = ''
    os.environ['SUPABASE_KEY'] = ''
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    for d in ('uploads', 'results', 'archive'):
        (work / d).mkdir(parents=True, exist_ok=True)


def load_deps():
    """실제 의존 — `prepare_env` 뒤에만 부른다 (app 은 import 시점에 env 를 읽는다)."""
    sys.path.insert(0, str(ROOT / 'webapp'))
    import app as A                     # noqa: E402
    import type_map_resolve as TMR      # noqa: E402
    import export_master_csv as EM      # noqa: E402
    return A, TMR, EM


def code_provenance() -> dict:
    def _git(*a):
        try:
            return subprocess.run(['git', '-C', str(ROOT), *a], capture_output=True, text=True,
                                  timeout=20).stdout.strip()
        except Exception:                                   # noqa: BLE001
            return ''
    return dict(git_sha=_git('rev-parse', 'HEAD'),
                dirty=bool(_git('status', '--porcelain', '--untracked-files=no')))


def stage_case(case: str, row: dict, hj: dict, uploads: Path, root_from: str, root_to: str) -> dict:
    """원자료 네 파일을 `uploads/<case>/` 에 웹앱이 찾는 이름으로 잇는다 — 수확 JSON 과 같은 프레임만."""
    src = dict(atom=HB.remap(row['atom_file'], root_from, root_to),
               contact=HB.remap(row['contact_file'], root_from, root_to),
               deck=HB.remap((row.get('deck') or '').strip(), root_from, root_to))
    for k, p in src.items():
        if not str(p) or not p.is_file():
            raise Refuse(f'{k} 파일 없음: {p}')
    mesh, pick, why = HB.pick_mesh(src['atom'])
    if mesh is None:
        raise Refuse(f'플래튼 메시를 못 골랐다 — {why}')
    src['mesh'] = mesh
    raw = hj.get('raw') or {}
    sha = {}
    for k in RAW_KEYS:
        want = (raw.get(k) or {}).get('sha256')
        if not want:
            raise Refuse(f'수확 JSON 에 {k} sha 가 없다 — 같은 프레임인지 확인할 수 없다')
        got = HB.sha256_of(src[k])
        if got != want:
            raise Refuse(f'{k} sha {got[:12]}… ≠ 수확 JSON {want[:12]}… — 다른 프레임/파일')
        sha[k] = got
    ts = hj.get('timestep')
    if ts is None:
        raise Refuse('수확 JSON 에 timestep 이 없다')
    d = uploads / case
    if d.exists():
        shutil.rmtree(d)                # 옛 파일이 남으면 run_pipeline 의 glob 이 다른 프레임을 섞는다
    d.mkdir(parents=True)
    names = {'atom': f'atom_{ts}.liggghts', 'contact': f'contact_{ts}.liggghts',
             'mesh': f'mesh_{ts}.stl', 'deck': f'input_{case}.liggghts'}
    for k, nm in names.items():
        (d / nm).symlink_to(Path(src[k]).resolve())
    return dict(case_dir=d, src={k: str(v) for k, v in src.items()}, sha=sha, mesh_pick=pick,
                names=names)


def resolve_mode(case_dir: Path, names: dict, hj: dict, A, TMR) -> tuple:
    """(mode, type_map) — 업로드 입구와 같은 판독 · 수확 JSON 과 대조."""
    m, _notes, errs = TMR.resolve_from_files(str(case_dir / names['deck']), str(case_dir / names['atom']))
    if errs or not m:
        raise Refuse(f'type_map 덱 판독 실패: {errs or "빈 map"}')
    want = {str(k): v for k, v in (hj.get('type_map') or {}).items()}
    if {str(k): v for k, v in m.items()} != want:
        raise Refuse(f'type_map 덱 판독 {TMR.format_map(m)} ≠ 수확 JSON {want}')
    mode = A.detect_mode(str(case_dir))
    if (mode == 'bimodal') != (len(m) == 3):
        raise Refuse(f'mode {mode} 이 type 수 {len(m)} 와 맞지 않는다')
    return mode, TMR.format_map(m)


def write_outputs(out_dir: Path, status: dict, rows: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp = out_dir / '.status.json.tmp'
    tmp.write_text(json.dumps(status, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    os.replace(tmp, out_dir / 'status.json')
    cols = ['case']
    for r in rows.values():
        for k in r:
            if k not in cols:
                cols.append(k)
    tmp = out_dir / '.metrics_flat.csv.tmp'
    with open(tmp, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n')
        w.writeheader()
        for c in sorted(rows):
            w.writerow(rows[c])
    os.replace(tmp, out_dir / 'metrics_flat.csv')


def load_previous(out_dir: Path) -> tuple:
    st, rows = None, {}
    p = out_dir / 'status.json'
    if p.exists():
        st = json.loads(p.read_text(encoding='utf-8'))
    q = out_dir / 'metrics_flat.csv'
    if q.exists():
        with open(q, encoding='utf-8', newline='') as fh:
            for r in csv.DictReader(fh):
                rows[r['case']] = {k: v for k, v in r.items() if v != ''}
    return st, rows


def run_batch(args, deps=None) -> int:
    work = Path(args.work).expanduser().resolve()
    out_dir = Path(args.out_dir)
    hdir = Path(args.harvest_dir)
    prepare_env(work)
    A, TMR, EM = deps if deps is not None else load_deps()
    cohort = {r['case']: r for r in HB.read_cohort(Path(args.cohort))}
    cases = sorted(p.stem for p in hdir.glob('*.json') if not p.name.startswith('_'))
    if args.case:
        cases = [c for c in cases if c in set(args.case)]
    prev, rows = load_previous(out_dir)
    status = prev if (prev and prev.get('schema') == SCHEMA) else dict(schema=SCHEMA, cases={})
    status['harvest_dir'] = str(hdir)
    status['cohort'] = str(args.cohort)
    status.setdefault('runs', []).append(dict(started=time.strftime('%Y-%m-%dT%H:%M:%S'),
                                              **code_provenance()))
    n_run = 0
    t_all = time.time()
    for i, case in enumerate(cases, 1):
        old = status['cases'].get(case) or {}
        if old.get('status') in KEEP_STATUS and not args.force:
            continue
        rec = dict(case=case, when=time.strftime('%Y-%m-%dT%H:%M:%S'))
        t0 = time.time()
        try:
            row = cohort.get(case)
            if row is None:
                raise Refuse('봉인 코호트에 없는 케이스')
            hj = json.loads((hdir / f'{case}.json').read_text(encoding='utf-8'))
            st = stage_case(case, row, hj, work / 'uploads', args.root_from, args.root_to)
            mode, tm = resolve_mode(st['case_dir'], st['names'], hj, A, TMR)
            meta = dict(name=case, created='', mode=mode, type_map=tm, type_map_resolved=tm,
                        type_map_notes=['lhs_webapp_batch — 덱 판독 = 수확 JSON'], ps_ratio='',
                        scale=1000, files=sorted(st['names'].values()), status='uploaded')
            (st['case_dir'] / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                                      encoding='utf-8')
            rd = work / 'results' / case
            if rd.exists():
                shutil.rmtree(rd)       # 옛 세대가 섞이지 않게 (run_pipeline 의 인과 계약과 같은 뜻)
            out = A.run_pipeline(case, mode, tm, 1000, figures=False, auto_db=False)
            n_run += 1
            stages = [dict(step=s.get('step'), rc=s.get('rc'), ok=s.get('ok'))
                      for s in (out.get('log') or []) if isinstance(s, dict)]
            rec.update(status=out.get('status') or ('done' if out.get('success') else 'failed'),
                       failed_stages=out.get('failed_stages') or [], stages=stages,
                       mode=mode, type_map=tm, sha=st['sha'], mesh_pick=st['mesh_pick'])
            if (rd / 'full_metrics.json').exists():
                rows[case] = EM.row_for(rd)
                rows[case]['case'] = case
            else:
                rec['status'] = 'failed'
                rec.setdefault('failed_stages', []).append('full_metrics.json 없음')
        except Refuse as e:
            rec.update(status='REFUSED', why=str(e))
        except Exception as e:                              # noqa: BLE001 — 한 케이스가 배치를 세우지 않게
            rec.update(status='failed', why=f'{type(e).__name__}: {e}')
        rec['elapsed_s'] = round(time.time() - t0, 1)
        status['cases'][case] = rec
        write_outputs(out_dir, status, rows)
        left = sum(1 for c in cases[i:] if (status['cases'].get(c) or {}).get('status') not in KEEP_STATUS)
        per = (time.time() - t_all) / max(n_run, 1)
        print(f'[{i}/{len(cases)}] {case} {rec["status"]} {rec["elapsed_s"]} s'
              + (f' · {rec.get("why")}' if rec.get('why') else '')
              + (f' · 남은 {left} 건 ≈ {left * per / 3600:.1f} h' if n_run else ''), flush=True)
    counts = {}
    for r in status['cases'].values():
        counts[r['status']] = counts.get(r['status'], 0) + 1
    print('상태:', counts)
    return 0 if not any(k not in KEEP_STATUS for k in counts) else 1


# ───────────────────────────────── selftest ─────────────────────────────────
def _selftest() -> int:
    fails = []

    def chk(name, ok):
        print(('  ✓ ' if ok else '  ✗ ') + name)
        if not ok:
            fails.append(name)

    tmp = Path(tempfile.mkdtemp(prefix='lhswb_'))
    try:
        raw = tmp / 'raw' / 'lhs00_900' / 'post'
        raw.mkdir(parents=True)
        (raw / 'atom_100.liggghts').write_text('ITEM: TIMESTEP\n100\nITEM: ATOMS id type\n1 1\n2 2\n3 3\n')
        (raw / 'contact_100.liggghts').write_text('ITEM: TIMESTEP\n100\n')
        (raw / 'mesh_100.stl').write_text('solid p\nendsolid p\n')
        (raw / 'mesh_90.stl').write_text('solid old\nendsolid old\n')
        deck = tmp / 'raw' / 'lhs00_900' / 'input_lhs00_900.liggghts'
        deck.write_text('# deck\n')
        coh = tmp / 'cohort.tsv'
        coh.write_text('# 봉인 코호트 (시험)\ncase\tstatus\tn_types\tdeck\tatom_file\tcontact_file\n'
                       f'lhs00_900\tRAW_OK\t3\t{deck}\t{raw / "atom_100.liggghts"}\t{raw / "contact_100.liggghts"}\n',
                       encoding='utf-8')
        hdir = tmp / 'harvest'
        hdir.mkdir()

        def _hj(**over):
            d = dict(case='lhs00_900', timestep=100, type_map={'1': 'AM_P', '2': 'AM_S', '3': 'SE'},
                     raw={k: dict(path=p.name, sha256=HB.sha256_of(p)) for k, p in
                          (('atom', raw / 'atom_100.liggghts'), ('contact', raw / 'contact_100.liggghts'),
                           ('mesh', raw / 'mesh_100.stl'), ('deck', deck))})
            d.update(over)
            return d
        (hdir / 'lhs00_900.json').write_text(json.dumps(_hj()), encoding='utf-8')
        (hdir / '_batch_summary.json').write_text('{}', encoding='utf-8')   # _ 로 시작하면 케이스가 아니다

        calls = []

        class FakeA:
            @staticmethod
            def detect_mode(case_dir):
                return 'bimodal'

            @staticmethod
            def run_pipeline(case, mode, tm, scale, figures=True, auto_db=True):
                calls.append(dict(case=case, mode=mode, tm=tm, figures=figures, auto_db=auto_db,
                                  files=sorted(os.listdir(Path(os.environ['WEBAPP_UPLOAD_FOLDER']) / case))))
                rd = Path(os.environ['WEBAPP_RESULTS_FOLDER']) / case
                rd.mkdir(parents=True, exist_ok=True)
                (rd / 'full_metrics.json').write_text(json.dumps({'se_se_cn': 4.25, 'percolation_pct': 97.0}))
                return {'status': 'done', 'success': True, 'failed_stages': [],
                        'log': [{'step': 'Parse', 'rc': 0, 'ok': True}]}

        class FakeTMR:
            m = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}

            @classmethod
            def resolve_from_files(cls, deck_p, atom_p):
                return dict(cls.m), [], []

            @staticmethod
            def format_map(m):
                return ','.join(f'{t}:{m[t]}' for t in sorted(m))

        class FakeEM:
            @staticmethod
            def row_for(rd):
                d = json.loads((Path(rd) / 'full_metrics.json').read_text())
                return {'case': Path(rd).name, **d}

        work, out = tmp / 'work', tmp / 'out'
        base = ['--harvest-dir', str(hdir), '--cohort', str(coh), '--work', str(work), '--out-dir', str(out)]
        env_keep = {k: os.environ.get(k) for k in ('WEBAPP_UPLOAD_FOLDER', 'WEBAPP_RESULTS_FOLDER',
                                                    'WEBAPP_ARCHIVE_FOLDER', 'SUPABASE_URL', 'SUPABASE_KEY',
                                                    'PYTHONDONTWRITEBYTECODE')}
        deps = (FakeA, FakeTMR, FakeEM)
        try:
            os.environ['SUPABASE_URL'] = 'https://example.invalid'
            rc = run_batch(_parse(base), deps)
            st = json.loads((out / 'status.json').read_text(encoding='utf-8'))
            r0 = st['cases'].get('lhs00_900') or {}
            chk('① 정상 — done · 한 번 실행 · 그림/자동 DB 끔 (figures=False · auto_db=False)',
                rc == 0 and r0.get('status') == 'done' and len(calls) == 1
                and calls[0]['figures'] is False and calls[0]['auto_db'] is False)
            chk('① 원격 저장소 끔 — SUPABASE_URL · KEY 가 빈 값 (pop 이 아니라 빈 문자열)',
                os.environ.get('SUPABASE_URL') == '' and os.environ.get('SUPABASE_KEY') == '')
            chk('① 스테이징 = 같은 step 네 파일 + meta.json 만 (옛 메시 mesh_90 은 안 들어간다)',
                calls[0]['files'] == sorted(['atom_100.liggghts', 'contact_100.liggghts', 'mesh_100.stl',
                                             'input_lhs00_900.liggghts', 'meta.json']))
            chk('① mode · type_map = 덱 판독 (1:AM_P,2:AM_S,3:SE · bimodal)',
                calls[0]['mode'] == 'bimodal' and calls[0]['tm'] == '1:AM_P,2:AM_S,3:SE')
            with open(out / 'metrics_flat.csv', encoding='utf-8') as fh:
                mrows = list(csv.DictReader(fh))
            chk('① metrics_flat.csv — 케이스 한 행 · 웹앱 열 그대로 (se_se_cn 4.25)',
                len(mrows) == 1 and mrows[0]['case'] == 'lhs00_900' and float(mrows[0]['se_se_cn']) == 4.25)
            chk('① status.json — 네 파일 sha · 코드 sha 기록 · _로 시작하는 파일은 케이스가 아니다',
                sorted((r0.get('sha') or {})) == sorted(RAW_KEYS) and 'git_sha' in st['runs'][-1]
                and list(st['cases']) == ['lhs00_900'])
            # ② 재개 — done 은 건너뛴다 · --force 는 다시
            run_batch(_parse(base), deps)
            chk('② 재개: done 케이스는 다시 돌리지 않는다', len(calls) == 1)
            run_batch(_parse(base + ['--force']), deps)
            chk('② --force: 다시 돈다', len(calls) == 2)
            # ③ 다른 프레임 — contact 한 바이트 바꾸면 거부 · 실행 0
            (raw / 'contact_100.liggghts').write_text('ITEM: TIMESTEP\n100\n#\n')
            run_batch(_parse(base + ['--force']), deps)
            r3 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900']
            chk('③ ★ contact sha ≠ 수확 JSON → REFUSED · run_pipeline 호출 없음',
                r3['status'] == 'REFUSED' and 'contact sha' in r3.get('why', '') and len(calls) == 2)
            (raw / 'contact_100.liggghts').write_text('ITEM: TIMESTEP\n100\n')
            # ④ type_map 불일치 — 거부
            FakeTMR.m = {1: 'AM_S', 2: 'AM_P', 3: 'SE'}
            run_batch(_parse(base + ['--force']), deps)
            r4 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900']
            chk('④ ★ 덱 판독 type_map ≠ 수확 JSON → REFUSED · 실행 없음',
                r4['status'] == 'REFUSED' and 'type_map' in r4.get('why', '') and len(calls) == 2)
            FakeTMR.m = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
            # ⑤ 같은 step 메시가 없으면 거부 (LHS-11 — 이른 메시로 대신하지 않는다)
            (raw / 'mesh_100.stl').rename(raw / 'mesh_100.bak')
            run_batch(_parse(base + ['--force']), deps)
            r5 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900']
            chk('⑤ ★ 같은 step 메시 없음 → REFUSED (mesh_90 으로 대신하지 않는다)',
                r5['status'] == 'REFUSED' and len(calls) == 2)
            (raw / 'mesh_100.bak').rename(raw / 'mesh_100.stl')
            # ⑥ 스테이징 폴더의 옛 파일은 지운다 — 남으면 run_pipeline glob 이 다른 atom 을 섞는다
            (work / 'uploads' / 'lhs00_900' / 'atom_50.liggghts').write_text('old')
            run_batch(_parse(base + ['--force']), deps)
            chk('⑥ ★ 스테이징 폴더의 옛 atom 파일은 실행 전에 지워진다',
                len(calls) == 3 and 'atom_50.liggghts' not in calls[-1]['files'])
            # ⑦ 실패가 배치를 세우지 않는다 — 예외는 그 케이스의 failed 로
            _orig = FakeA.run_pipeline

            def _boom(*a, **k):
                raise RuntimeError('solver died')
            FakeA.run_pipeline = staticmethod(_boom)
            rc7 = run_batch(_parse(base + ['--force']), deps)
            r7 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900']
            chk('⑦ 파이프라인 예외 → 그 케이스 failed · 배치 rc 1 (조용히 초록이 아니다)',
                r7['status'] == 'failed' and 'solver died' in r7.get('why', '') and rc7 == 1)
            FakeA.run_pipeline = _orig
        finally:
            for k, v in env_keep.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{"✓ 전부 통과" if not fails else f"✗ {len(fails)} 건 실패"}')
    return 0 if not fails else 1


def _parse(argv=None):
    ap = argparse.ArgumentParser(description='LHS 침대 × 웹앱 파이프라인 일괄 (판단 J20)')
    ap.add_argument('--harvest-dir', default=str(DEF_HARVEST),
                    help='수확 JSON 폴더 — 케이스 목록 · 같은 프레임 sha · type_map 의 기준')
    ap.add_argument('--cohort', default=str(HB.COHORT), help='봉인 코호트 TSV (atom · contact · deck 경로)')
    ap.add_argument('--work', default='', help='작업 폴더 (uploads · results) — 리포 밖 권장')
    ap.add_argument('--out-dir', default='', help='metrics_flat.csv · status.json 을 쓸 곳')
    ap.add_argument('--case', action='append', default=[], help='이 케이스만 (여러 번 가능)')
    ap.add_argument('--root-from', default='', help='코호트 경로 접두사')
    ap.add_argument('--root-to', default='', help='실제 경로 접두사로 치환')
    ap.add_argument('--force', action='store_true', help='done · partial 도 다시 돌린다')
    ap.add_argument('--selftest', action='store_true')
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = _parse(argv)
    if args.selftest:
        return _selftest()
    if not args.work or not args.out_dir:
        print('⛔ --work 와 --out-dir 를 주어야 한다', file=sys.stderr)
        return 2
    return run_batch(args)


if __name__ == '__main__':
    sys.exit(main())
