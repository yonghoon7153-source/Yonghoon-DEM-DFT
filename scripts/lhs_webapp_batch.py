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
    (2-type mono 덱만: 수확기의 'AM' ↔ 웹앱의 반지름 이름 AM_P/AM_S 를 같다고 본다 — `fold_single_am` · 1저자 비준 09-30.
    웹앱에는 덱 판독 map 을 그대로 넘기고, 접은 사실은 status.json 의 `type_map_fold` 에 남는다)
    (3-type 덱의 0 입자 상 — ps_sweep 세대 P:S = 10:0 · 0:10: 덱 판독은 덤프에 0 개인 type 을 뺀다.  덤프의 type 별 개수 =
    수확 `phase_counts` 이고 남은 type 이 번호 · 이름까지 같을 때만 같은 침대로 본다 — `absent_types` · 1저자 10-01.
    뺀 type 은 status.json 의 `type_map_absent` 에 남는다)
  • ★ J20-a ⓑ (1저자 비준 09-28 밤): atom · contact 파일이 **한 프레임**이고 contact 에 **같은 쌍이 두 행** 없어야 한다 —
    웹앱 파서는 파일 안 모든 프레임을 이어 붙이고 (`parse_liggghts`) CN · 접촉 수는 행마다 +1 이다 (DESC-06 · 합성 2 프레임에서
    CN 정확히 2 배).  점검 결과 (`contact_scan` · `atom_frames`) 는 status.json 에 남는다 (δ ≤ 0 행 수 포함 — 거부는 안 한다)
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
    python3 scripts/lhs_webapp_batch.py … --stop-after contact   # ① 접촉 위상만 (묶음별 · 산출 폴더는 따로)
    python3 scripts/lhs_webapp_batch.py … --stop-after coverage  # ① + 피복 (legacy Physics + physics v2 · network 없음)
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
import lhs_descriptor_harvest as H      # noqa: E402  (J20-a ⓑ — 접촉 덤프 점검 · 프레임 수: 감사기 `lhs_contact_audit` 와 같은 함수)
import type_map_resolve as TMR_DUMP     # noqa: E402  (덤프 type 별 개수 — 0 입자 상 관문이 덱 판독과 독립으로 센다)

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
    #  J20-a ⓑ — 웹앱 경로는 행을 거르지 않는다: 한 프레임 · 쌍마다 한 행이 아니면 CN · 접촉 수 · 면적 합이 부푼다 (DESC-06)
    try:
        scan = H.scan_contact_dump(str(src['contact']))
    except H.BedRefusal as e:
        raise Refuse(f'contact 덤프 점검 실패 — {e}')
    n_af = H.count_blocks(str(src['atom']), 'ITEM: TIMESTEP')
    if scan['n_frames'] != 1:
        raise Refuse(f"contact 프레임 {scan['n_frames']} ≠ 1 — 웹앱 파서가 전부 이어 붙여 CN · 접촉 수가 부푼다 (DESC-06)")
    if n_af != 1:
        raise Refuse(f'atom 프레임 {n_af} ≠ 1 — 웹앱 atoms.csv 에 같은 id 가 여러 번 들어간다 (DESC-06)')
    if scan['n_dup_rows'] or scan['n_self_pairs']:
        raise Refuse(f"contact 중복 행 {scan['n_dup_rows']} · 자기쌍 {scan['n_self_pairs']} — 웹앱은 행마다 CN 을 +1 한다")
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
                names=names, contact_scan=scan, atom_frames=int(n_af))


def fold_single_am(got: dict, want: dict) -> bool:
    """2-type (mono) 덱만: 덱 판독의 AM_P/AM_S 를 'AM' 으로 접으면 수확 JSON 과 같은가.

    수확기는 AM 이 한 상인 침대를 'AM' 으로 적는다 (`lhs_perc_extract.TYPE_MAP[2]` — 상별 P/S 칸 N/A 규약).
    웹앱 덱 판독은 같은 입자를 반지름으로 AM_P/AM_S 라 부른다 (`type_map_resolve` · r > 4 µm → AM_P).
    이름만 다르다 — 웹앱의 AM 집합은 '이름에 AM' 이다 (`dem_analysis_core` 714 · 1054).
    ⚠ 접기는 두 쪽 다 2-type 이고 수확 쪽이 정확히 {AM, SE} 일 때만 — 번호가 뒤바뀌거나 SE 가 없으면 여전히 다르다.
    """
    if len(got) != 2 or len(want) != 2 or sorted(want.values()) != ['AM', 'SE']:
        return False
    return {k: ('AM' if v in ('AM_P', 'AM_S') else v) for k, v in got.items()} == want


def absent_types(got: dict, want: dict, dump_types: dict, phase_counts) -> list:
    """3-type 덱의 0 입자 상 (ps_sweep 세대 P:S = 10:0 · 0:10 — 10-01 WSL 실측: 이 관문이 두 조성을 REFUSED).

    덱 판독 (`type_map_resolve.resolve`) 은 덤프에 0 개인 type 을 map 에서 **뺀다** (빈 배열 방지 · 업로드 입구와 같은 규칙).
    수확 JSON 은 덱의 3 type 을 다 적고 그 상의 `phase_counts` 를 0 으로 둔다.  ⇒ 수확 map 에서 0 개인 type 을 빼면
    덱 판독과 **번호 · 이름까지** 같은가.  같으면 뺀 type 번호 (정렬된 문자열 목록), 아니면 [].
    ⚠ 두 출처가 상마다 개수까지 같아야 한다 — 덤프 (`dump_types`, type → {'n'}) 의 type 별 개수 = 수확 `phase_counts` 의 상별 개수.
       하나라도 어긋나거나 · `phase_counts` 가 없거나 · 덤프에 있는 type 이 빠졌거나 · SE 가 남지 않으면 [] (= 거부).
    """
    if len(want) != 3 or not isinstance(phase_counts, dict):
        return []
    n_dump = {str(t): int(d.get('n', 0)) for t, d in (dump_types or {}).items()}
    if set(n_dump) - set(want):
        return []                                           # 덤프에 수확 map 밖의 type 이 있다
    for k, ph in want.items():
        if phase_counts.get(ph) != n_dump.get(k, 0):
            return []                                       # 두 출처의 개수가 다르다 (키 없음 포함)
    gone = sorted(k for k in want if n_dump.get(k, 0) == 0)
    rest = {k: v for k, v in want.items() if k not in gone}
    if not gone or rest != got or 'SE' not in rest.values():
        return []
    return gone


def resolve_mode(case_dir: Path, names: dict, hj: dict, A, TMR) -> tuple:
    """(mode, type_map, 접음 기록, 뺀 type 기록) — 업로드 입구와 같은 판독 · 수확 JSON 과 대조.

    웹앱에 넘기는 map 은 **덱 판독 그대로**다 (접은 이름 · 뺀 type 을 되살리지 않는다 — 업로드 입구와 같은 입력).
    """
    m, _notes, errs = TMR.resolve_from_files(str(case_dir / names['deck']), str(case_dir / names['atom']))
    if errs or not m:
        raise Refuse(f'type_map 덱 판독 실패: {errs or "빈 map"}')
    want = {str(k): v for k, v in (hj.get('type_map') or {}).items()}
    got = {str(k): v for k, v in m.items()}
    fold = absent = ''
    if got != want:
        if fold_single_am(got, want):
            fold = (f'2-type: 덱 판독 {TMR.format_map(m)} ≡ 수확 JSON {want} — 단일 AM 상의 이름만 다르다 '
                    '(수확기 = AM · 웹앱 = 반지름 규칙 AM_P/AM_S)')
        else:
            #  덤프는 진짜 파일을 다시 센다 (덱 판독과 독립 — 시험의 가짜 덱 판독도 이 개수를 못 바꾼다)
            gone = absent_types(got, want, TMR_DUMP.types_in_dump(str(case_dir / names['atom'])), hj.get('phase_counts'))
            if not gone:
                raise Refuse(f'type_map 덱 판독 {TMR.format_map(m)} ≠ 수확 JSON {want}')
            absent = ','.join(f'{k}:{want[k]}' for k in gone)
    mode = A.detect_mode(str(case_dir))
    if (mode == 'bimodal') != (len(m) == 3):
        raise Refuse(f'mode {mode} 이 type 수 {len(m)} 와 맞지 않는다')
    return mode, TMR.format_map(m), fold, absent


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
    stop = getattr(args, 'stop_after', None) or None
    #  묶음별 실행 (1저자 09-29 밤 "단독적으로 하나씩") — 한 산출 폴더에 모드 둘을 섞지 않는다 (섞이면 metrics_flat 의 행마다
    #   채워진 묶음이 달라진다).  옛 폴더 (stop_after 키 없음) = 전체 실행.
    if prev and prev.get('schema') == SCHEMA and (prev.get('stop_after') or None) != stop:
        print(f'⛔ {out_dir} 는 stop_after={prev.get("stop_after")!r} 로 만든 산출 폴더다 — 이번 실행 stop_after={stop!r} 와 섞지 않는다 '
              '(다른 --out-dir 을 쓸 것)', file=sys.stderr)
        return 2
    status = prev if (prev and prev.get('schema') == SCHEMA) else dict(schema=SCHEMA, cases={})
    status['stop_after'] = stop
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
            mode, tm, fold, absent = resolve_mode(st['case_dir'], st['names'], hj, A, TMR)
            if fold:
                rec['type_map_fold'] = fold
            if absent:
                rec['type_map_absent'] = absent
            if fold:
                note = f'lhs_webapp_batch — {fold}'
            elif absent:
                note = (f'lhs_webapp_batch — 3-type 덱 · 덤프 0 개 type {absent} 은 덱 판독이 뺐다 (type_map_resolve · 업로드 입구와 같은 규칙) '
                        '· 수확 phase_counts 와 상마다 개수 같음 · 남은 type = 수확 JSON')
            else:
                note = 'lhs_webapp_batch — 덱 판독 = 수확 JSON'
            meta = dict(name=case, created='', mode=mode, type_map=tm, type_map_resolved=tm,
                        type_map_notes=[note],
                        ps_ratio='',
                        scale=1000, files=sorted(st['names'].values()), status='uploaded')
            (st['case_dir'] / 'meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                                      encoding='utf-8')
            rd = work / 'results' / case
            if rd.exists():
                shutil.rmtree(rd)       # 옛 세대가 섞이지 않게 (run_pipeline 의 인과 계약과 같은 뜻)
            kw = dict(figures=False, auto_db=False)
            if stop:
                kw['stop_after'] = stop           # 전체 실행은 키워드를 넘기지 않는다 (옛 웹앱 서명에서도 돈다)
            out = A.run_pipeline(case, mode, tm, 1000, **kw)
            n_run += 1
            stages = [dict(step=s.get('step'), rc=s.get('rc'), ok=s.get('ok'))
                      for s in (out.get('log') or []) if isinstance(s, dict)]
            rec['stop_after'] = stop
            rec.update(status=out.get('status') or ('done' if out.get('success') else 'failed'),
                       failed_stages=out.get('failed_stages') or [], stages=stages,
                       mode=mode, type_map=tm, sha=st['sha'], mesh_pick=st['mesh_pick'],
                       contact_scan=st['contact_scan'], atom_frames=st['atom_frames'])
            if (rd / 'full_metrics.json').exists():
                rows[case] = EM.row_for(rd)
                rows[case]['case'] = case
                #  physics v2 판정 (피복 단계) — 'blank: …' 도 done 이지만 사유가 status.json 에서 바로 보이게 한다
                if rows[case].get('coverage_status_physics_v2') is not None:
                    rec['coverage_status_physics_v2'] = rows[case]['coverage_status_physics_v2']
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
    v2c = {}
    for r in status['cases'].values():
        if r.get('coverage_status_physics_v2') is not None:
            k = 'ok' if r['coverage_status_physics_v2'] == 'ok' else 'blank'
            v2c[k] = v2c.get(k, 0) + 1
    if v2c:
        print('physics v2 판정:', v2c, '(blank 사유는 status.json · metrics_flat.csv 의 coverage_status_physics_v2)')
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
        _CHD = 'ITEM: ENTRIES c_cpl[7] c_cpl[8] c_cpl[9] c_cpl[22] c_cpl[23]\n'
        C_OK = 'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ENTRIES\n2\n' + _CHD + '1 2 0 0.1 0.01\n2 3 1 0.1 0.02\n'
        (raw / 'contact_100.liggghts').write_text(C_OK)
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
            mode = 'bimodal'

            @classmethod
            def detect_mode(cls, case_dir):
                return cls.mode

            @staticmethod
            def run_pipeline(case, mode, tm, scale, figures=True, auto_db=True, **kw):
                calls.append(dict(case=case, mode=mode, tm=tm, figures=figures, auto_db=auto_db,
                                  passed_stop=('stop_after' in kw), stop_after=kw.get('stop_after'),
                                  files=sorted(os.listdir(Path(os.environ['WEBAPP_UPLOAD_FOLDER']) / case))))
                rd = Path(os.environ['WEBAPP_RESULTS_FOLDER']) / case
                rd.mkdir(parents=True, exist_ok=True)
                _fm = {'se_se_cn': 4.25, 'percolation_pct': 97.0}
                if kw.get('stop_after') == 'coverage':
                    _fm['coverage_status_physics_v2'] = 'blank: 시험'
                (rd / 'full_metrics.json').write_text(json.dumps(_fm))
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
            (raw / 'contact_100.liggghts').write_text(C_OK)
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
            # ⑧–⑩ J20-a ⓑ (1저자 비준 09-28 밤) — 웹앱 파서는 파일 안 모든 프레임을 이어 붙이고 행을 거르지 않는다 (DESC-06).
            #   sha 는 수확 JSON 과 **같게** 맞춰 두고 (다른 관문이 먼저 막지 않게) 새 관문만 시험한다.
            def _reseal():
                (hdir / 'lhs00_900.json').write_text(json.dumps(_hj()), encoding='utf-8')
            n_calls = len(calls)
            (raw / 'contact_100.liggghts').write_text(C_OK + 'ITEM: TIMESTEP\n101\nITEM: NUMBER OF ENTRIES\n1\n' + _CHD + '1 2 0 0.1 0.01\n')
            _reseal()
            run_batch(_parse(base + ['--force']), deps)
            r8 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900']
            chk('⑧ ★ contact 파일에 프레임 2 개 → REFUSED (웹앱 파서가 이어 붙여 CN 2 배) · 실행 없음',
                r8['status'] == 'REFUSED' and '프레임' in r8.get('why', '') and len(calls) == n_calls)
            (raw / 'contact_100.liggghts').write_text(C_OK + '3 2 1 0.1 0.02\n')
            _reseal()
            run_batch(_parse(base + ['--force']), deps)
            r9 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900']
            chk('⑨ ★ 같은 쌍이 두 행 (2–3 · 3–2) → REFUSED (웹앱은 행마다 CN +1) · 실행 없음',
                r9['status'] == 'REFUSED' and '중복' in r9.get('why', '') and len(calls) == n_calls)
            (raw / 'contact_100.liggghts').write_text(C_OK)
            (raw / 'atom_100.liggghts').write_text('ITEM: TIMESTEP\n90\nITEM: ATOMS id type\n1 1\n2 2\n3 3\n'
                                                   'ITEM: TIMESTEP\n100\nITEM: ATOMS id type\n1 1\n2 2\n3 3\n')
            _reseal()
            run_batch(_parse(base + ['--force']), deps)
            r10 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900']
            chk('⑩ ★ atom 파일에 프레임 2 개 → REFUSED · 실행 없음',
                r10['status'] == 'REFUSED' and 'atom 프레임' in r10.get('why', '') and len(calls) == n_calls)
            (raw / 'atom_100.liggghts').write_text('ITEM: TIMESTEP\n100\nITEM: ATOMS id type\n1 1\n2 2\n3 3\n')
            _reseal()
            run_batch(_parse(base + ['--force']), deps)
            r11 = json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900']
            chk('⑪ 깨끗한 한 프레임으로 되돌리면 done · 접촉 점검 기록 (contact_scan: 프레임 1 · 중복 0 · δ≤0 0 · 주기 1)',
                r11['status'] == 'done' and (r11.get('contact_scan') or {}).get('n_frames') == 1
                and (r11.get('contact_scan') or {}).get('n_dup_rows') == 0
                and (r11.get('contact_scan') or {}).get('n_periodic_flag') == 1 and r11.get('atom_frames') == 1)
            # ⑫–⑬ 묶음별 실행 (1저자 09-29 밤 *"단독적으로 하나씩 돌려서 표를 채워나갈 거야"*) — `--stop-after contact` 는
            #   웹앱 파이프라인을 접촉 분석 단계까지만 돌린다 (① 접촉 위상).  산출 폴더에 모드를 새기고, 다른 모드와 섞지 않는다.
            out_c = tmp / 'out_contact'
            base_c = ['--harvest-dir', str(hdir), '--cohort', str(coh), '--work', str(tmp / 'work_c'), '--out-dir', str(out_c)]
            n0 = len(calls)
            try:
                rc12 = run_batch(_parse(base_c + ['--stop-after', 'contact']), deps)
            except SystemExit as e:                         # 옛 파서 — 옵션이 없다
                rc12 = f'SystemExit {e.code}'
            st12 = json.loads((out_c / 'status.json').read_text(encoding='utf-8')) if (out_c / 'status.json').exists() else {}
            chk('⑫ ★ --stop-after contact → run_pipeline(stop_after="contact") · status.json 최상위 · 케이스에 stop_after 기록',
                rc12 == 0 and len(calls) == n0 + 1 and calls[-1].get('stop_after') == 'contact'
                and st12.get('stop_after') == 'contact'
                and (st12.get('cases', {}).get('lhs00_900') or {}).get('stop_after') == 'contact')
            chk('⑫b 전체 실행은 stop_after 키워드를 넘기지 않는다 (옛 웹앱 서명에서도 돈다)',
                not any(c.get('passed_stop') for c in calls[:n0]))
            try:
                rc13 = run_batch(_parse(base + ['--stop-after', 'contact', '--force']), deps)   # out = 전체 실행 폴더
            except SystemExit as e:
                rc13 = f'SystemExit {e.code}'
            chk('⑬ ★ 전체 실행 산출 폴더에 --stop-after contact 를 섞으면 거부 (rc 2 · 실행 0)',
                rc13 == 2 and len(calls) == n0 + 1)
            rc13b = run_batch(_parse(base_c + ['--force']), deps)                              # out_c = 접촉만 폴더
            chk('⑬b ★ 접촉만 폴더에 전체 실행을 섞으면 거부 (rc 2 · 실행 0)', rc13b == 2 and len(calls) == n0 + 1)
            # ⑭ 2-type (mono) 덱 (1저자 비준 09-30) — 수확기는 AM 이 한 상인 침대를 'AM' 으로 적고 (lhs_perc_extract.TYPE_MAP[2]
            #   · 상별 P/S 칸 N/A 규약), 웹앱 덱 판독은 같은 입자를 반지름으로 AM_S/AM_P 라 부른다 (type_map_resolve · r > 4 µm).
            #   이름만 다르다 — 웹앱의 AM 집합은 '이름에 AM' (dem_analysis_core 714 · 1054).  09-29 WSL 실측: 이 관문이 mono 30 건을 전부 거부했다.
            (hdir / 'lhs00_900.json').write_text(json.dumps(_hj(type_map={'1': 'AM', '2': 'SE'})), encoding='utf-8')
            FakeA.mode = 'standard'

            def _run14(m):
                FakeTMR.m = m
                n = len(calls)
                run_batch(_parse(base + ['--force']), deps)
                return json.loads((out / 'status.json').read_text(encoding='utf-8'))['cases']['lhs00_900'], len(calls) - n
            r14, k14 = _run14({1: 'AM_S', 2: 'SE'})
            chk('⑭ ★ 2-type: 수확 {1:AM,2:SE} ↔ 덱 판독 1:AM_S,2:SE → done · 웹앱에는 덱 판독 map 그대로 · 접음 기록',
                r14.get('status') == 'done' and k14 == 1 and calls[-1]['tm'] == '1:AM_S,2:SE'
                and bool(r14.get('type_map_fold')))
            r14b, k14b = _run14({1: 'AM_P', 2: 'SE'})
            chk('⑭b 2-type: 1:AM_P,2:SE 도 같다 (r > 4 µm) → done',
                r14b.get('status') == 'done' and k14b == 1 and calls[-1]['tm'] == '1:AM_P,2:SE')
            r14c, k14c = _run14({1: 'SE', 2: 'AM_S'})
            chk('⑭c ★ 음성: SE 번호가 뒤바뀌면 거부 (접어도 {1:SE,2:AM} ≠ 수확) · 실행 없음',
                r14c.get('status') == 'REFUSED' and 'type_map' in r14c.get('why', '') and k14c == 0)
            r14d, k14d = _run14({1: 'AM_P', 2: 'AM_S'})
            chk('⑭d ★ 음성: SE 없는 두 AM → 거부 · 실행 없음',
                r14d.get('status') == 'REFUSED' and k14d == 0)
            FakeA.mode = 'bimodal'
            r14e, k14e = _run14({1: 'AM_P', 2: 'AM_S', 3: 'SE'})
            chk('⑭e ★ 음성: 수확 2-type ↔ 덱 판독 3-type → 거부 (접기는 2-type 끼리만) · 실행 없음',
                r14e.get('status') == 'REFUSED' and k14e == 0)
            (hdir / 'lhs00_900.json').write_text(json.dumps(_hj()), encoding='utf-8')
            r14f, k14f = _run14({1: 'AM_P', 2: 'AM_S', 3: 'SE'})
            chk('⑭f 3-type 은 그대로 — 같은 이름이면 done · 접음 기록 없음',
                r14f.get('status') == 'done' and k14f == 1 and not r14f.get('type_map_fold'))
            # ⑰ 3-type 덱의 0 입자 상 (ps_sweep 세대 P:S = 10:0 · 0:10 — 10-01 WSL 실측: 두 조성이 이 관문에서 REFUSED).
            #   덱 판독 (`type_map_resolve.resolve`) 은 덤프에 0 개인 type 을 map 에서 **뺀다** (빈 배열 방지 · 업로드 입구와 같은 규칙)
            #   — 수확 JSON 은 덱의 3 type 을 다 적고 그 상의 phase_counts 를 0 으로 둔다.  뺀 type 이 덤프에도 0 개 · phase_counts 도 0
            #   이고 (상마다 두 출처의 개수가 같고) 남은 type 이 번호 · 이름까지 같을 때만 같은 침대로 본다.
            ATOM3 = 'ITEM: TIMESTEP\n100\nITEM: ATOMS id type\n1 1\n2 2\n3 3\n'

            def _bed17(types, counts, tm_deck):
                (raw / 'atom_100.liggghts').write_text('ITEM: TIMESTEP\n100\nITEM: ATOMS id type\n'
                                                       + ''.join(f'{i} {t}\n' for i, t in enumerate(types, 1)))
                hj17 = _hj()
                if counts is not None:
                    hj17['phase_counts'] = counts
                (hdir / 'lhs00_900.json').write_text(json.dumps(hj17), encoding='utf-8')
                FakeA.mode = 'standard'                     # detect_mode = 덤프의 type 수 (2) — 덱 판독 map 2 개와 맞다
                return _run14(tm_deck)
            r17, k17 = _bed17([1, 3, 3], {'AM_P': 1, 'AM_S': 0, 'SE': 2}, {1: 'AM_P', 3: 'SE'})
            chk('⑰ ★ 3-type 덱 · AM_S 0 개 (10:0): 수확 {1:AM_P,2:AM_S,3:SE} ↔ 덱 판독 1:AM_P,3:SE → done · '
                '웹앱에는 덱 판독 map 그대로 · 뺀 type 기록 (type_map_absent) · 접음 기록 없음',
                r17.get('status') == 'done' and k17 == 1 and calls[-1]['tm'] == '1:AM_P,3:SE'
                and r17.get('type_map_absent') == '2:AM_S' and not r17.get('type_map_fold'))
            r17b, k17b = _bed17([2, 3, 3], {'AM_P': 0, 'AM_S': 1, 'SE': 2}, {2: 'AM_S', 3: 'SE'})
            chk('⑰b ★ 3-type 덱 · AM_P 0 개 (0:10): 덱 판독 2:AM_S,3:SE → done · 뺀 type 1:AM_P',
                r17b.get('status') == 'done' and k17b == 1 and calls[-1]['tm'] == '2:AM_S,3:SE'
                and r17b.get('type_map_absent') == '1:AM_P')
            r17c, k17c = _bed17([1, 2, 3], {'AM_P': 1, 'AM_S': 1, 'SE': 1}, {1: 'AM_P', 3: 'SE'})
            chk('⑰c ★ 음성: 덤프에 있는 type (2) 을 덱 판독이 뺐다 → 거부 · 실행 없음',
                r17c.get('status') == 'REFUSED' and 'type_map' in r17c.get('why', '') and k17c == 0)
            r17d, k17d = _bed17([1, 3, 3], {'AM_P': 1, 'AM_S': 5, 'SE': 2}, {1: 'AM_P', 3: 'SE'})
            chk('⑰d ★ 음성: 수확 phase_counts 는 AM_S 5 인데 덤프에 type 2 가 없다 (두 출처 불일치) → 거부',
                r17d.get('status') == 'REFUSED' and k17d == 0)
            r17e, k17e = _bed17([1, 3, 3], {'AM_P': 1, 'AM_S': 0, 'SE': 2}, {1: 'AM_S', 3: 'SE'})
            chk('⑰e ★ 음성: 남은 type 의 이름이 다르다 (덱 판독 1:AM_S ≠ 수확 1:AM_P) → 거부',
                r17e.get('status') == 'REFUSED' and k17e == 0)
            r17f, k17f = _bed17([1, 1, 1], {'AM_P': 3, 'AM_S': 0, 'SE': 0}, {1: 'AM_P'})
            chk('⑰f ★ 음성: SE 가 빠지면 거부 (SE 0 개 침대는 이 규칙 밖)',
                r17f.get('status') == 'REFUSED' and k17f == 0)
            r17g, k17g = _bed17([1, 3, 3], None, {1: 'AM_P', 3: 'SE'})
            chk('⑰g ★ 음성: 수확 JSON 에 phase_counts 가 없으면 (두 출처 교차 확인 불가) 거부',
                r17g.get('status') == 'REFUSED' and k17g == 0)
            r17h, k17h = _bed17([1, 3, 3], {'AM_P': 2, 'AM_S': 0, 'SE': 1}, {1: 'AM_P', 3: 'SE'})
            chk('⑰h ★ 음성: 남은 상의 개수가 덤프와 다르다 (phase_counts AM_P 2 ≠ 덤프 type 1 의 1 개) → 거부',
                r17h.get('status') == 'REFUSED' and k17h == 0)
            #  되돌리기 — 뒤 시험 (⑮ ⑯) 은 3-type 원본으로
            (raw / 'atom_100.liggghts').write_text(ATOM3)
            (hdir / 'lhs00_900.json').write_text(json.dumps(_hj()), encoding='utf-8')
            FakeTMR.m = {1: 'AM_P', 2: 'AM_S', 3: 'SE'}
            FakeA.mode = 'bimodal'
            # ⑮–⑯ cap (physics) coverage v2 인계 (1저자 09-29 밤 — 새 판 병기 · `stop_after='coverage'` 로 ① + cap coverage 한 번에).
            #   `--stop-after coverage` 는 웹앱 파이프라인을 접촉 → 피복 단계까지 돌린다 (network · Stage E 없음).  산출 폴더에
            #   모드를 새기고, 다른 모드 (전체 · 접촉만) 와 어느 방향으로도 섞지 않는다.
            out_v = tmp / 'out_coverage'
            base_v = ['--harvest-dir', str(hdir), '--cohort', str(coh), '--work', str(tmp / 'work_v'), '--out-dir', str(out_v)]
            n1 = len(calls)
            try:
                rc15 = run_batch(_parse(base_v + ['--stop-after', 'coverage']), deps)
            except SystemExit as e:                         # 옛 파서 — choices 에 coverage 가 없다
                rc15 = f'SystemExit {e.code}'
            st15 = json.loads((out_v / 'status.json').read_text(encoding='utf-8')) if (out_v / 'status.json').exists() else {}
            r15 = st15.get('cases', {}).get('lhs00_900') or {}
            chk('⑮ ★ --stop-after coverage → run_pipeline(stop_after="coverage") · status.json 최상위 · 케이스에 stop_after 기록 · '
                'v2 판정 (coverage_status_physics_v2) 이 케이스 기록에 보인다',
                rc15 == 0 and len(calls) == n1 + 1 and calls[-1].get('stop_after') == 'coverage'
                and st15.get('stop_after') == 'coverage' and r15.get('stop_after') == 'coverage'
                and r15.get('coverage_status_physics_v2') == 'blank: 시험')
            _mix = []
            for _lbl, _argv in (('피복만 폴더 ← 접촉만', base_v + ['--stop-after', 'contact', '--force']),
                                ('피복만 폴더 ← 전체', base_v + ['--force']),
                                ('접촉만 폴더 ← 피복만', base_c + ['--stop-after', 'coverage', '--force']),
                                ('전체 폴더 ← 피복만', base + ['--stop-after', 'coverage', '--force'])):
                try:
                    _rc = run_batch(_parse(_argv), deps)
                except SystemExit as e:
                    _rc = f'SystemExit {e.code}'
                if _rc != 2:
                    _mix.append(f'{_lbl}: rc {_rc}')
            chk(f'⑯ ★ 피복만 폴더 ↔ 접촉만 · 전체 폴더 — 어느 방향으로 섞어도 거부 (rc 2 · 실행 0)  {_mix or ""}',
                not _mix and len(calls) == n1 + 1)
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
    ap.add_argument('--stop-after', choices=['contact', 'coverage'], default=None,
                    help='웹앱 파이프라인을 이 단계에서 멈춘다 — contact = 접촉 분석까지 (① 접촉 위상 · network · Stage E 없음) · '
                         'coverage = 접촉 → 피복까지 (① + legacy Physics · physics v2 피복 — `*_physics_v2` 키 · network · '
                         'Stage E 없음; 피복 단계가 v2 판정을 안 쓰면 그 케이스는 failed). '
                         '산출 폴더에 모드가 새겨지고 다른 모드와 섞으면 거부한다')
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
