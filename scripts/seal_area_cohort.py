#!/usr/bin/env python3
"""S3 코호트 봉인 — raw 가용성 **전수** 목록 + 파일 지문 → `docs/data/area_s2_cohort.tsv`.

계약 §5-v3 ③ (Codex 2라운드) + **§5-v4 D-2**(3라운드, 쌍 step 규칙): *"raw 가용성 전수 목록·포함/제외 사유·파일 지문을 독립적으로
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

#: 계약 §5-v4 D-2 — atom 은 contact 과 **같은 step** 이거나 **5,000 step 이내로 뒤**여야 한다.
#  ⚠ 규칙이 계약에만 있으면 샌다 (CLAUDE.md ④).  실제로 `lhs00_029` 가 −150,000 으로 통과했고
#  Codex 가 뒤늦게 잡았다 — 원인은 데이터 결함이 아니라 **전송 누락**이었지만, 도구가 그것을
#  못 본 것이 문제다.  ⇒ 여기서 강제한다.  ⛔ 결과를 보고 이 값을 늘리지 말 것.
#: 쌍 step 허용 간격.
#  ⛔⛔ **2026-09-19 — 5000 → 0.**  옛 값 5000 은 **소비자와 어긋나 있었다**:
#    `lhs_descriptor_harvest.py:404` 는 `ts_a != ts_c` 면 **무조건 거부**한다 (DESC-06).
#    ⇒ 봉인기가 `RAW_OK` 로 통과시킨 62 행을 수확기가 전부 거부했다 = 같은 파이프라인의
#      두 도구가 **같은 축에서 반대 계약**을 쓰고 있었다.  어느 쪽도 단독으로는 틀리지 않아
#      각자 초록이었고, 사이에 낀 62 행은 아무 검사에도 안 걸렸다.
#  ★ 0 으로 맞춘다 — 그리고 `_paired_case_files` 가 애초에 같은 step 만 고르므로
#    이 값은 **이제 방어선**이지 선택 규칙이 아니다.
#  ⚠ 값을 다시 올리려면 **수확기부터** 고칠 것.  여기만 올리면 옛 상태로 돌아간다.
PAIR_MAX_GAP = 0


def step_of(p: Path):
    """(파일명 step, **본문** `ITEM: TIMESTEP` step) — 파일명을 믿지 않는다."""
    m = re.search(r'_(\d+)\.liggghts$', Path(p).name)
    name_step = int(m.group(1)) if m else None
    body = None
    try:
        with open(p, 'r', errors='replace') as f:
            if f.readline().strip().startswith('ITEM: TIMESTEP'):
                body = int(f.readline().strip())
    except Exception:
        body = None
    return name_step, body


RE_DUMP = re.compile(r'_(\d+)\.liggghts$')


def _paired_case_files(d):
    """atom·contact 가 **같은 step** 인 최신 쌍 → (atom, contact) 또는 (None, None).

    ⛔⛔ **2026-09-19 — 여기가 `DESC-06` 이었다.**  옛 판은 공유 헬퍼
      `plastic_coverage._find_case_files` 를 썼고 그것은 `_pick_latest` 를 atom·contact
      **각각 독립으로** 부른다.  그 결과 봉인된 코호트 129 행 중 **62 행**이 서로 다른
      프레임의 쌍을 가리켰고, 수확기(`lhs_descriptor_harvest.py:404`)가 `ts_a != ts_c` 로
      **전부 거부**했다 — 코호트 절반이 원리적으로 수확 불가였다.
      ⚠ 리허설이 `127/127` 초록이었던 것은 **dry-run 이라 수확기를 안 불렀기 때문**이고,
        `lhs_harvest_batch.py:65` 가 그 false-green 을 이미 이름으로 적어 두고 있었다.
    ★ **실측 규약** (사용자 확인 2026-09-19): contact 덤프는 **1만 단위**, atom 은 **5천 단위**로
      쓰인다 ⇒ atom step 집합이 contact 를 **포함**하므로 *"공통 최신"* = *"contact 최신"* 이다.
      실측으로도 어긋난 62 중 **61** 이 공통 step 을 갖는다 (나머지 1 은 부분 전송 탓).
    ⚠ 선택은 **파일명 step** 으로 한다 (싸다).  파일명이 본문과 다른 경우는 호출부의
      `STEP_NAME_MISMATCH` 가 따로 문다 — 두 검사는 서로를 대신하지 않는다.
    """
    import os as _os
    if not _os.path.isdir(d):
        return None, None
    def _by_step(pat):
        out = {}
        for p in Path(d).glob(pat):
            m = RE_DUMP.search(p.name)
            if m:
                out[int(m.group(1))] = p
        return out
    A, C = _by_step('atom_*.liggghts'), _by_step('contact_*.liggghts')
    common = sorted(set(A) & set(C))
    if not common:
        return None, None
    s_ = common[-1]
    return A[s_], C[s_]


#: 경위 문서 — 헤더가 자동 생성이라 손기록이 사라지는 것을 막는 자리 (2026-09-19)
PROVENANCE = 'docs/data/area_s2_cohort_provenance.md'

COLS = ['case', 'status', 'design_family', 'family_source', 'n_types', 'deck', 'deck_sha256',
        'atom_file', 'atom_sha256', 'contact_file', 'contact_sha256',
        'step_atom', 'step_contact', 'step_gap', 'reason']
DESIGN_CSV = ROOT / 'docs' / 'data' / 'lhs_design_20260818.csv'   # 설계족의 **정본** (`block` 열)
BLOCK_NTYPES = {'bimodal': '3', 'mono_AM_S': '2', 'mono_AM_P': '2'}
HEAD_RE = re.compile(r'^#\s*(\S+):\s*(\S+)\s*\((\d+)-type\)')
_SHA_RE = re.compile(r'[0-9a-f]{64}')      # 봉인 지문의 모양 (빈칸은 결손이라 정상)


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def load_design(csv_path: Path | None):
    """설계 CSV → {case_id: block}.  ★ 실측 (2026-09-13): 실제 `lhs00_1xx` 덱의 첫 줄은 내 정규식과
    안 맞아 31건 전부 UNKNOWN 이 됐다.  설계족의 정본은 이 CSV 의 `block` 열이다 (Codex 도 이것으로
    mono 15+15 를 냈다).  덱 헤더는 **보조**로만 쓴다."""
    import csv as _csv
    if not csv_path or not Path(csv_path).is_file():
        return {}
    with Path(csv_path).open(encoding='utf-8') as f:
        return {r['case_id']: r.get('block', '') for r in _csv.DictReader(f) if r.get('case_id')}


def design_family(deck: Path):
    """덱 첫 줄 주석에서 (family, n_types).  없으면 ('UNKNOWN', '')."""
    try:
        first = deck.read_text(encoding='utf-8', errors='replace').splitlines()[0]
    except Exception:
        return 'UNKNOWN', ''
    m = HEAD_RE.match(first.strip())
    return (m.group(2), m.group(3)) if m else ('UNKNOWN', '')


def seal_case(case_dir: Path, deck_dir: Path | None, design: dict | None = None) -> dict:
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
        #  ★ 짝 맞는 최신 쌍을 고른다 (독립 최신 선택이 DESC-06 이었다 — 위 함수 참조)
        pa, pc = _paired_case_files(str(d))
        if pa and pc:
            hit = (pa, pc); break
        #  CSV 로 이관된 옛 케이스는 공유 헬퍼의 폴백을 그대로 쓴다 (덤프가 없다)
        a, c = _PC._find_case_files(str(d))
        if a and c and a.endswith('.csv') and c.endswith('.csv'):
            hit = (Path(a), Path(c)); break
    problems = []
    row['design_family'] = 'UNKNOWN'          # 정본(설계 CSV)에도 덱 헤더에도 없으면 UNKNOWN (빈 문자열 금지)
    row['family_source'] = ''
    if dk is None:
        problems.append('DECK_MISSING')
    else:
        row['deck'] = str(dk); row['deck_sha256'] = sha256(dk)
        fam_hdr, nt_hdr = design_family(dk)
        if fam_hdr != 'UNKNOWN':
            row['design_family'], row['n_types'], row['family_source'] = fam_hdr, nt_hdr, 'deck_header'
    blk = (design or {}).get(case_dir.name, '')
    if blk:
        if row['family_source'] == 'deck_header' and row['design_family'] != blk:
            problems.append('FAMILY_CONFLICT')        # 덱 헤더 ↔ 설계 CSV 가 다르면 거부하지 않고 기록
        row['design_family'], row['n_types'], row['family_source'] = blk, BLOCK_NTYPES.get(blk, ''), 'design_csv'
    if hit is None:
        a = _PC._pick_latest(str(case_dir), 'atom_*.liggghts')
        for d in sorted(q for q in case_dir.glob('post_*') if q.is_dir()):
            a = a or _PC._pick_latest(str(d), 'atom_*.liggghts')
        #  ★ 2026-09-19 — **셋을 가른다.**  `_paired_case_files` 도입 직후 내가 낸 퇴행:
        #    짝 맞는 step 이 없을 뿐 contact 는 **있는데** `RAW_MISSING_CONTACT` 로 적혀
        #    *"있는 파일을 없다고"* 말했다.  진단이 틀리면 다음 사람이 엉뚱한 것을 찾는다.
        _c_any = _PC._pick_latest(str(case_dir), 'contact_*.liggghts')
        for d in sorted(q for q in case_dir.glob('post_*') if q.is_dir()):
            _c_any = _c_any or _PC._pick_latest(str(d), 'contact_*.liggghts')
        if a and _c_any:
            problems.append('REFUSED_INPUT_PAIR_STEP')   # 둘 다 있는데 **같은 step 이 없다**
        else:
            problems.append('RAW_MISSING_CONTACT' if a else 'RAW_MISSING_ATOM')
        #  ★ 계약 §5-v4 D-8 (2026-09-14) — **있는 것은 적는다.**  옛 판은 contact 가 없으면
        #    존재하는 atom 의 경로·지문까지 비웠다.  거짓 `RAW_OK` 는 아니었지만 **pending
        #    입력의 이력이 사라져** 결손 행의 빈 칸을 *"atom 도 없다"* 로 읽게 만들었다
        #    (실제로 `lhs00_029` 의 −150,000 을 쫓을 때 그 빈 칸이 길을 흐렸다).
        #    ⚠ 상태는 그대로 `RAW_MISSING_CONTACT` 다 — 이 줄은 **기록만** 늘리고 판정은
        #      한 글자도 안 바꾼다.  selftest ⑩ 이 상태와 기록을 **같이** 문다.
        if a:
            ap = Path(a)
            row['atom_file'], row['atom_sha256'] = str(ap), sha256(ap)
            _na, _ba = step_of(ap)
            _sa = _ba if _ba is not None else _na
            row['step_atom'] = '' if _sa is None else str(_sa)
    else:
        row['atom_file'], row['contact_file'] = str(hit[0]), str(hit[1])
        row['atom_sha256'], row['contact_sha256'] = sha256(hit[0]), sha256(hit[1])
        #  ★ 계약 §5-v4 D-2 를 **여기서** 건다 — 파일명이 아니라 본문 step 으로.
        na, ba = step_of(hit[0]); nc_, bc = step_of(hit[1])
        if (ba is not None and na is not None and ba != na) or \
           (bc is not None and nc_ is not None and bc != nc_):
            problems.append('STEP_NAME_MISMATCH')      # 파일명이 본문과 다르다
        sa = ba if ba is not None else na
        sc = bc if bc is not None else nc_
        row['step_atom'] = '' if sa is None else str(sa)
        row['step_contact'] = '' if sc is None else str(sc)
        if sa is None or sc is None:
            problems.append('STEP_UNREADABLE')
        else:
            row['step_gap'] = str(sa - sc)
            if not 0 <= sa - sc <= PAIR_MAX_GAP:
                problems.append('REFUSED_INPUT_PAIR_STEP')
    fatal = [x for x in problems if x != 'FAMILY_CONFLICT']
    row['status'] = ('RAW_OK' if not problems else '+'.join(problems))
    if fatal and dk is None and hit is None:
        row['reason'] = '케이스 폴더 아님 — 덱도 원자료도 없다 (행은 남긴다)'
    elif fatal:
        row['reason'] = '제외 사유 = ' + ', '.join(fatal) + ' (기술적 결손; 솔버 이전)'
    else:
        row['reason'] = '포함: 원자료·덱 실재 (솔버 성공 여부는 보지 않았다)'
    if 'FAMILY_CONFLICT' in problems:
        row['reason'] += ' · ⚠ 덱 헤더와 설계 CSV 의 설계족이 다르다 (CSV 채택)'
    return row


def refill_family(tsv: Path, design: dict) -> tuple[int, int]:
    """이미 봉인된 TSV 의 `design_family`/`n_types`/`family_source` 만 설계 CSV 로 채운다.
    ★ 해시 열은 **바이트 단위로 손대지 않는다** — 원자료를 다시 읽지도 않는다.  → (채운 수, 전체)"""
    lines = tsv.read_text(encoding='utf-8').splitlines()
    hdr_i = next(i for i, ln in enumerate(lines) if not ln.startswith('#'))
    cols = lines[hdr_i].split('\t')
    if 'family_source' not in cols:                    # 옛 판 TSV (열 없음) → 열 삽입
        k = cols.index('design_family') + 1
        cols.insert(k, 'family_source')
        rows = []
        for ln in lines[hdr_i + 1:]:
            v = ln.split('\t'); v.insert(k, ''); rows.append(v)
    else:
        rows = [ln.split('\t') for ln in lines[hdr_i + 1:]]
    ix = {c: i for i, c in enumerate(cols)}
    #  ★ 2026-09-14 (판정문 §6.4) — refill 은 봉인 파일을 **다시 쓴다**.  검증 없이 쓰면
    #    손상을 세탁한다.  fail-closed 로 거부한다 (모르면 통과가 아니다).
    _ids = [v[ix['case']] for v in rows if len(v) > ix['case']]
    _dup = sorted({c for c in _ids if _ids.count(c) > 1})
    if _dup:
        raise SystemExit(f'⛔ DUPLICATE_CASE_ID — 봉인 TSV 에 중복 ID 가 있다: {_dup}\n'
                         f'   refill 은 이 파일을 다시 쓰므로 중복을 안고 덮어쓰지 않는다.')
    _bad = []
    for v in rows:
        for c in ('deck_sha256', 'atom_sha256', 'contact_sha256'):
            if c in ix and len(v) > ix[c]:
                h = v[ix[c]]
                if h and not _SHA_RE.fullmatch(h):      # 빈칸은 정상 — 결손이니까
                    _bad.append(f"{v[ix['case']]}:{c}={h[:16]}…")
    if _bad:
        raise SystemExit('⛔ BROKEN_SHA — 지문이 64자 16진수가 아니다: ' + ', '.join(_bad[:8])
                         + ('' if len(_bad) <= 8 else f' … 총 {len(_bad)}건'))
    n = 0
    for v in rows:
        blk = design.get(v[ix['case']], '')
        if blk:
            v[ix['design_family']] = blk; v[ix['n_types']] = BLOCK_NTYPES.get(blk, ''); v[ix['family_source']] = 'design_csv'; n += 1
        elif not v[ix['design_family']]:
            v[ix['design_family']] = 'UNKNOWN'
    fam = {}
    for v in rows:
        fam[v[ix['design_family']]] = fam.get(v[ix['design_family']], 0) + 1
    head = [ln for ln in lines[:hdr_i] if not ln.startswith('# 설계족 분포')]
    head.append('# 설계족 분포: ' + ' · '.join(f'{k} {c}' for k, c in sorted(fam.items()))
                + '   (출처: docs/data/lhs_design_20260818.csv `block` 열; 해시 열은 refill 에서 불변)')
    tsv.write_text('\n'.join(head + ['\t'.join(cols)] + ['\t'.join(v) for v in rows]) + '\n', encoding='utf-8')
    return n, len(rows)


def seal(root: Path, deck_dir: Path | None, design: dict | None = None):
    """봉인 = **등록부 ∪ 디렉터리** 전수.

    ★ 2026-09-14 (3라운드 판정문 §6.4) — 옛 판은 **디렉터리 inventory** 였다.  설계 폴더가
    통째로 없으면 그 ID 의 **행 자체가 사라져**, 읽는 사람은 그 ID 가 애초에 없었는지 폴더가
    없는지 구분할 수 없다 (*"생성기의 성공을 봉인 유효성 검사의 성공으로 읽지 말 것"*).
    계약 `§5-v4 D-1` 이 주 ID 를 `lhs00_000`–`129` 로 **고정**했으므로 봉인은 등록부 전수여야
    한다 — 없는 것은 행이 없는 게 아니라 **`CASE_DIR_MISSING`** 이다.
    ⚠ 등록부로 **좁히지도** 않는다 — 등록 밖 폴더도 행을 남긴다 (전수의 뜻, 검사 ⑪b).
    """
    dirs = {q.name: q for q in root.iterdir() if q.is_dir()}
    rows = [seal_case(dirs[n], deck_dir, design) for n in sorted(dirs)]
    for cid in sorted(set(design or {}) - set(dirs)):
        r = {k: '' for k in COLS}
        blk = (design or {}).get(cid, '')
        r.update(case=cid, status='CASE_DIR_MISSING',
                 design_family=blk or 'UNKNOWN', family_source='design_csv' if blk else '',
                 n_types=BLOCK_NTYPES.get(blk, ''),
                 reason='제외 사유 = CASE_DIR_MISSING — 등록부에는 있으나 케이스 폴더가 없다 '
                        '(행을 없애지 않는다; 솔버 이전)')
        rows.append(r)
    return sorted(rows, key=lambda r: r['case'])


def write_tsv(rows, out: Path, root: Path):
    sha = subprocess.run(['git', '-C', str(ROOT), 'rev-parse', '--short=9', 'HEAD'],
                         capture_output=True, text=True).stdout.strip()
    fam = {}
    for r in rows:
        fam[r['design_family']] = fam.get(r['design_family'], 0) + 1
    hdr = [f'# S3 코호트 봉인 — raw 가용성 전수 목록 (계약 §5-v3 ③ · 쌍 step 규칙 §5-v4 D-2: '
           f'0 ≤ step_atom − step_contact ≤ {PAIR_MAX_GAP}).  생성 {_dt.date.today().isoformat()} · 도구 커밋 {sha}',
           f'# root = {root}',
           '# ⛔ 솔버를 부르지 않았다 — 포함/제외는 파일 실재로만.  이 목록 전부를 S3 가 돌리고 실패는 REFUSED 로 보존한다.',
           '# 설계족 분포: ' + ' · '.join(f'{k} {v}' for k, v in sorted(fam.items())),
           '# ⚠ 설계족이 mono 뿐이면 AREA-11(AM_P–AM_S · AM_P 반경 이종쌍) 효과는 이 코호트로 검증할 수 없다.',
           #  ★★ 2026-09-19 — **경위 포인터는 자동 생성분이다.**  이 헤더는 재봉인할 때마다
           #    통째로 새로 써지므로 손으로 적은 주석이 사라진다 (실제로 하루에 **두 번** 잃었다).
           #    ⇒ 경위는 옆 파일에 두고 여기선 **가리키기만** 한다 — 그 줄은 자동이라 안 지워진다.
           f'# ★ 경위·교훈·ibb 경로·함정: {PROVENANCE}  ← 재봉인해도 그 파일은 안 바뀐다',
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
    # ⑩ **결손 행도 있는 것은 적는다** (계약 §5-v4 D-8) — contact 가 없다고 해서 **존재하는
    #    atom 의 경로·지문까지 비우지 않는다.  거짓 `RAW_OK` 는 아니었지만 pending 입력의
    #    이력이 사라져, 결손 행의 빈 칸을 읽는 사람이 *"atom 도 없다"* 로 오독하게 된다.
    #    ⚠ 상태는 그대로 `RAW_MISSING_CONTACT` 여야 한다 — 이 검사가 그것도 같이 문다.
    _m = by['lhs00_902']
    chk('★⑩ contact 결손이어도 **있는 atom** 의 경로·지문은 적는다 (D-8)',
        _m['status'] == 'RAW_MISSING_CONTACT'
        and _m['atom_file'].endswith('atom_100.liggghts') and len(_m['atom_sha256']) == 64
        and _m['contact_file'] == '' and _m['contact_sha256'] == '',
        f"atom={_m['atom_file'] or '(빈칸)'} · sha={len(_m['atom_sha256'])}자 · "
        f"contact={_m['contact_file'] or '(빈칸)'}")
    chk('⑩b 결손 행의 step 은 atom 쪽만 채워진다 (gap 은 없다)',
        _m['step_atom'] == '100' and _m['step_contact'] == '' and _m['step_gap'] == '',
        f"atom={_m['step_atom']!r} contact={_m['step_contact']!r} gap={_m['step_gap']!r}")
    chk('⑩c atom 도 없는 행은 그대로 빈칸 (없는 것을 지어내지 않는다)',
        by['lhs00_904']['atom_file'] == '' and by['lhs00_904']['atom_sha256'] == '')

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
    # ⑦ 설계 CSV 가 정본 — 덱 헤더가 없어도(실제 lhs00_1xx) 채워지고, 충돌은 기록된다
    dcsv = t / 'design.csv'
    dcsv.write_text('case_id,block\nlhs00_900,mono_AM_P\nlhs00_903,bimodal\nlhs00_901,mono_AM_S\n')
    design = load_design(dcsv)
    r2 = {r['case']: r for r in seal(t, t, design)}
    chk('⑦a 설계 CSV 가 덱 헤더를 이긴다 (source=design_csv)', r2['lhs00_900']['design_family'] == 'mono_AM_P'
        and r2['lhs00_900']['family_source'] == 'design_csv' and r2['lhs00_900']['n_types'] == '2')
    chk('⑦b 덱 없는 케이스도 CSV 로 채워진다', r2['lhs00_903']['design_family'] == 'bimodal'
        and r2['lhs00_903']['status'].startswith('DECK_MISSING'))
    chk('⑦c 덱 헤더 ↔ CSV 충돌은 거부가 아니라 기록 (FAMILY_CONFLICT, CSV 채택)',
        'FAMILY_CONFLICT' in r2['lhs00_901']['status'] and r2['lhs00_901']['design_family'] == 'mono_AM_S')
    chk('⑦d CSV 에 없는 케이스는 덱 헤더 (source=deck_header)', r2['lhs00_902']['family_source'] == 'deck_header')
    # ⑧ refill — 옛 TSV 의 해시는 바이트 불변, 설계족만 채워진다
    before = {ln.split('\t')[0]: ln for ln in out.read_text(encoding='utf-8').splitlines() if not ln.startswith('#')}
    n, tot = refill_family(out, design)
    after_lines = [ln for ln in out.read_text(encoding='utf-8').splitlines() if not ln.startswith('#')]
    cols = after_lines[0].split('\t'); ix = {c: i for i, c in enumerate(cols)}
    after = {ln.split('\t')[0]: ln.split('\t') for ln in after_lines[1:]}
    same_hash = all(before[k].split('\t')[COLS.index('atom_sha256')] == after[k][ix['atom_sha256']]
                    and before[k].split('\t')[COLS.index('deck_sha256')] == after[k][ix['deck_sha256']]
                    for k in after)
    # ══ §5-v4 D-2 회귀 — 쌍 step 규칙을 **도구가** 강제하는가 (R3-06) ══
    t2 = Path(tempfile.mkdtemp())
    def mk2(name, a_name, c_name, a_body=None):
        d = t2 / name; q = d / f'post_{name}'; q.mkdir(parents=True)
        (d / f'input_{name}.liggghts').write_text(f'# {name}: bimodal (3-type) | LHS design\n')
        hdr = f'ITEM: TIMESTEP\n{a_body}\n' if a_body is not None else ''
        (q / a_name).write_text(hdr + 'ITEM: ATOMS id type radius x y z\n1 1 0.0005 0 0 0\n')
        (q / c_name).write_text('ITEM: ENTRIES c_cpl[1]\n')
    mk2('lhs00_910', 'atom_2840000.liggghts', 'contact_2840000.liggghts')      # 같은 step
    mk2('lhs00_911', 'atom_2845000.liggghts', 'contact_2840000.liggghts')      # atom 5,000 뒤
    mk2('lhs00_912', 'atom_2690000.liggghts', 'contact_2840000.liggghts')      # ★ 실제로 걸렸던 −150,000
    mk2('lhs00_913', 'atom_2850000.liggghts', 'contact_2840000.liggghts')      # +10,000 = 규칙 밖
    mk2('lhs00_914', 'atom_2840000.liggghts', 'contact_2840000.liggghts', a_body=2690000)  # 파일명 거짓말
    #  ★★ **실제 코퍼스의 모양** (실측 2026-09-19, ibb `lhs00_089`):
    #     atom  2835000 2840000 2845000 2850000 2855000   ← 5천 단위
    #     contact 2810000 2820000 2830000 2840000 2850000 ← 1만 단위
    #     ⇒ atom 집합이 contact 를 **포함**하므로 공통 최신(= contact 최신)을 골라야 한다.
    #     옛 판은 각각 최신을 골라 (2855000, 2850000) = 수확 불가였다.  62/129 가 이 모양이다.
    mk2('lhs00_915', 'atom_2845000.liggghts', 'contact_2840000.liggghts')
    _q915 = t2 / 'lhs00_915' / 'post_lhs00_915'
    (_q915 / 'atom_2840000.liggghts').write_text('ITEM: ATOMS id type radius x y z\n1 1 0.0005 0 0 0\n')
    b2 = {r['case']: r for r in seal(t2, t2)}
    chk('⑨ 같은 step 쌍은 통과', b2['lhs00_910']['status'] == 'RAW_OK'
        and b2['lhs00_910']['step_gap'] == '0')
    #  ⛔⛔ **계약 개정 2026-09-19** — 옛 ⑨b 는 *'atom 이 5,000 뒤도 통과'* 를 단언했다.
    #    그것이 **소비자와 어긋난 계약**이었다: 수확기는 `ts_a != ts_c` 를 무조건 거부한다.
    #    그래서 봉인 129 행 중 **62 행**이 `RAW_OK` 인 채 수확 불가였다.  ⇒ 단언을 뒤집는다.
    chk('★⑨b 5,000 어긋난 쌍**만** 있으면 거부 (옛 판은 RAW_OK 였다)',
        'REFUSED_INPUT_PAIR_STEP' in b2['lhs00_911']['status'], b2['lhs00_911']['status'])
    chk('⑨c ★ −150,000 은 거부된다 (lhs00_029 가 통과했던 자리)',
        'REFUSED_INPUT_PAIR_STEP' in b2['lhs00_912']['status'], b2['lhs00_912']['status'])
    chk('⑨d +10,000 도 거부된다 (한쪽만 넓지 않다)',
        'REFUSED_INPUT_PAIR_STEP' in b2['lhs00_913']['status'], b2['lhs00_913']['status'])
    chk('⑨e ★ 파일명이 본문과 다르면 잡는다 (파일명을 믿지 않는다)',
        'STEP_NAME_MISMATCH' in b2['lhs00_914']['status'], b2['lhs00_914']['status'])
    chk('★★⑨g 실제 코퍼스 모양 — atom 이 더 최신이어도 **공통 step 쌍**을 고른다',
        b2['lhs00_915']['status'] == 'RAW_OK' and b2['lhs00_915']['step_gap'] == '0',
        f"{b2['lhs00_915']['status']} gap={b2['lhs00_915'].get('step_gap')}")
    chk('★★⑨g 고른 파일이 **더 최신 atom 이 아니다** (2845000 을 버리고 2840000 을 쓴다)',
        b2['lhs00_915']['atom_file'].endswith('atom_2840000.liggghts')
        and b2['lhs00_915']['contact_file'].endswith('contact_2840000.liggghts'),
        b2['lhs00_915']['atom_file'])
    #  ★★ 헤더는 재봉인마다 새로 써진다 — **경위 포인터가 거기 있어야** 손기록이 안 사라진다.
    #    (2026-09-19 하루에 두 번 잃고 나서 세운 규칙.)
    _p2 = t2 / 'hdr_probe.tsv'
    write_tsv(list(b2.values()), _p2, t2)
    _hdr = [ln for ln in _p2.read_text(encoding='utf-8').splitlines() if ln.startswith('#')]
    chk('★⑨h 경위 포인터가 자동 헤더에 실린다 (없으면 재봉인이 기록을 지운다)',
        any(PROVENANCE in ln for ln in _hdr if ln.startswith('#')), str(_hdr[:6]))
    chk('★⑨h 가리키는 경위 파일이 실재한다',
        (ROOT / PROVENANCE).is_file(), PROVENANCE)
    chk('⑨f step 열이 TSV 에 실린다', all(k in COLS for k in ('step_atom', 'step_contact', 'step_gap')))

    chk('⑧ refill: 해시 열 바이트 불변 · 설계족 3/5 채움 · 헤더 분포 갱신', n == 3 and tot == 5 and same_hash
        and after['lhs00_900'][ix['design_family']] == 'mono_AM_P'
        and '설계족 분포: bimodal 1 · mono_AM_P 1 · mono_AM_S 3' in out.read_text(encoding='utf-8'),
        f'{n}/{tot} same_hash={same_hash}')

    #  ── 판정문 §6.4 "봉인 도구가 보증하지 않는 것" 의 남은 둘 (2026-09-14) ─────────────
    #  ⑪ **디렉터리 inventory 라 폴더가 통째로 없으면 행이 사라진다.**  계약 §5-v4 D-1 은
    #     주 ID 를 `lhs00_000`–`129` 로 **고정**했으므로, 봉인은 디렉터리 목록이 아니라
    #     **등록부 전수**여야 한다.  없으면 행이 없어지는 것이 아니라 `CASE_DIR_MISSING` 이다.
    _reg = {'lhs00_900': 'mono_AM_S', 'lhs00_902': 'mono_AM_S', 'lhs00_999': 'bimodal'}
    _r3 = seal(t, t, _reg)
    _b3 = {r['case']: r for r in _r3}
    chk('★⑪ 등록 ID 에 폴더가 없으면 행이 **사라지지 않는다** (CASE_DIR_MISSING)',
        'lhs00_999' in _b3 and _b3['lhs00_999']['status'] == 'CASE_DIR_MISSING'
        and _b3['lhs00_999']['design_family'] == 'bimodal',
        str(sorted(_b3)))
    chk('⑪b 등록 밖 폴더도 여전히 행이 있다 (전수의 뜻 — 등록부로 좁히지 않는다)',
        'lhs00_901' in _b3 and 'lhs00_904' in _b3, str(sorted(_b3)))
    chk('⑪c CASE_DIR_MISSING 행은 지문 칸이 전부 비어 있다 (없는 것을 지어내지 않는다)',
        'lhs00_999' in _b3 and all(_b3['lhs00_999'][k] == '' for k in
            ('deck', 'deck_sha256', 'atom_file', 'atom_sha256', 'contact_file', 'contact_sha256')),
        '행 자체가 없다' if 'lhs00_999' not in _b3 else '')
    #  ⑫ **refill 이 중복 ID·깨진 지문을 검증하지 않는다** — refill 은 봉인 파일을 **다시 쓴다**.
    #     검증 없이 쓰면 손상을 세탁한다.  fail-closed 로 거부한다 (모르면 통과가 아니다).
    _bad = t / 'dup.tsv'
    _base = out.read_text(encoding='utf-8').splitlines()
    _hi = next(i for i, ln in enumerate(_base) if not ln.startswith('#'))
    _bad.write_text('\n'.join(_base + [_base[_hi + 1]]) + '\n', encoding='utf-8')   # 마지막 행 복제
    try:
        refill_family(_bad, {}); _dup_ok = False
    except SystemExit as e:
        _dup_ok = 'DUPLICATE' in str(e)
    chk('★⑫ refill 은 중복 case ID 를 거부한다 (봉인을 다시 쓰기 전에)', _dup_ok)
    _bad2 = t / 'badsha.tsv'
    _v = _base[_hi + 1].split('\t'); _ixc = _base[_hi].split('\t')
    _v[_ixc.index('atom_sha256')] = 'deadbeef'                      # 64자 16진수가 아니다
    _bad2.write_text('\n'.join(_base[:_hi + 1] + ['\t'.join(_v)]) + '\n', encoding='utf-8')
    try:
        refill_family(_bad2, {}); _sha_ok = False
    except SystemExit as e:
        _sha_ok = 'SHA' in str(e)
    chk('★⑫b refill 은 깨진 지문을 거부한다 (빈칸은 정상 — 결손이니까)', _sha_ok)
    _okf = t / 'good.tsv'
    _okf.write_text(out.read_text(encoding='utf-8'), encoding='utf-8')
    try:
        refill_family(_okf, {}); _pass_ok = True
    except SystemExit as e:
        _pass_ok = False
    chk('⑫c 정상 TSV 는 그대로 통과 (검사가 refill 을 죽이지 않는다)', _pass_ok)

    print('코호트 봉인 SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description='S3 코호트 봉인 (raw 전수 + sha256, 솔버 무관)')
    ap.add_argument('--webapp', default='', help='케이스 폴더들을 담은 root (예: ~/lhs_local)')
    ap.add_argument('--deck-dir', default='')
    ap.add_argument('--out', default=str(ROOT / 'docs' / 'data' / 'area_s2_cohort.tsv'))
    ap.add_argument('--design-csv', default=str(DESIGN_CSV), help='설계족 정본 (`case_id`,`block`)')
    ap.add_argument('--refill-family', default='', metavar='TSV',
                    help='이미 봉인된 TSV 의 설계족만 설계 CSV 로 채운다 (해시 불변, 원자료 불필요)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    design = load_design(Path(a.design_csv))
    if a.refill_family:
        n, tot = refill_family(Path(a.refill_family), design)
        print(f'설계족 채움 {n}/{tot} (출처 {a.design_csv}) → {a.refill_family}')
        return 0 if n else 1
    if not a.webapp:
        print('⛔ --webapp 이 필요하다'); return 2
    root = Path(a.webapp).expanduser().resolve()
    deck = Path(a.deck_dir).expanduser().resolve() if a.deck_dir else None
    rows = seal(root, deck, design)
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
