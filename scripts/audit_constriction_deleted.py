#!/usr/bin/env python3
"""S0 — **협착 항이 삭제된 간선이 몇 개인가** (면적 계약 §4, 계산 불변).

정본 계약 = `docs/area_contract_20260913.md`.  원장 = `SELF-28` · `AREA-01`~`AREA-04`.
적대 검토 = `docs/reviews/codex_verdict_area_contract_20260913.md`.

⛔⛔ **초판(커밋 9392860a8)은 HOLD 였다** — Codex 가 네 P1 을 냈다.  초판은 helper 를
**다시 구현**해 세었고 그래서 생산 솔버와 모집단·입력 경로가 갈렸다:
  · `AREA-01` δ 부재/0 을 건너뛰었다.  솔버는 **native contact_area** 를 쓴다
    ⇒ 합성 반례에서 S0 **0 %** ↔ 솔버 **100 %**.
  · `AREA-02` S0 는 **raw 행**, 솔버는 정렬 ID쌍 key 의 **마지막 채택 행**만 센다
    ⇒ **90 %** ↔ **0 %** (반대 방향도 재현).
  · Hertz 대조가 생산 Hertz 가 아니었다 (생산 Hertz 가지엔 ψ 삭제가 **없다**)
    ⇒ S0 100 % ↔ 실제 `Rc = 5.206583187 > 0`.
  · helper 예외가 **비삭제**로 집계됐고 오류 카운터가 없었다.
  · `_pair_kind` 가 *"AM 이 아니면 SE"* 였다 (미등록 type9 가 AM_SE 로).
  · ★ selftest 가 **판별력 0** 이었다 — 소스 문자열 존재만 봐서, `R_constriction = 0`
    대입을 `R_Maxwell` 로 바꿔 실제 Rc 가 **0 → 0.20771261697** 이 돼도 **13/13 PASS**.
    (`SELF-25`·`L4-03` 과 같은 부류이고 이번엔 **내가 만든 계측기**에서 났다.)

★★ **2판의 설계 = 다시 구현하지 않는다.  솔버를 부른다.**
`network_conductivity.build_network(..., contact_mode=...)` 를 **그대로 호출**하고 돌려받은
간선에서 `R_constriction == 0` 을 센다.  그러면
  · δ 부재/0 의 native 면적 fallback  (AREA-01)
  · 정렬 ID쌍 dedup 과 마지막-채택  (AREA-02)
  · 채널별 상 필터 (ionic=SE–SE · electronic=AM–AM · thermal=전부)
  · Hertz-명명 가지에 ψ 삭제가 없다는 사실
이 **전부 솔버의 것**이 된다 — 우리가 흉내 낼 여지가 없다.
⇒ selftest 도 구조적으로 판별력을 갖는다: 솔버의 `Rc = 0` 분기를 바꾸면 이 수가 **반드시**
움직인다 (회귀 ⑥ 이 그것을 강제한다).

★ 문턱 자체는 기록으로만 남긴다 (판정용 아님):
    Rc = 0 분기  <=>  psi <= 1e-4  <=>  a/r_min >= 0.99784556531
                <=>  A >= 0.9956957722087699 * pi * r_min^2
⚠ **문서의 옛 등가식은 틀렸다** (Codex [P2]) — `psi` **정확히 0** 은 `A/(pi r^2) >= 1` 이고
  `Rc = 0` 분기는 그보다 **낮은** 0.99570 에서 이미 켜진다.  둘은 다른 문턱이다.

⚠ **계산을 바꾸지 않는다** — 읽기 전용이다.  솔버도 코퍼스도 건드리지 않는다.
⚠ `Rc = 0` 은 **협착 항** 삭제다.  보통 `R_bulk` 는 남는다 — 간선 삭제나 총저항 0 과
  섞지 말 것 (그것은 `L2-10` 의 다른 양이다).
⚠ box_x/box_y 는 `d_ij` → `R_bulk` 에만 들어가고 `R_constriction` 에는 안 들어간다
  ⇒ 삭제 집계는 상자 크기에 **불변**이다 (그래서 넉넉히 준다).
⚠ 이 컨테이너에는 원 접촉 자료가 없다 — **코퍼스가 있는 머신에서** 돌린다.

사용:
  python3 scripts/audit_constriction_deleted.py --webapp ~/Yonghoon-DEM-DFT/webapp
  python3 scripts/audit_constriction_deleted.py --webapp <경로> --limit 5
  python3 scripts/audit_constriction_deleted.py --webapp <경로> --out-csv docs/data/s0.csv
  python3 scripts/audit_constriction_deleted.py --selftest
"""
from __future__ import annotations
import argparse
import csv
import importlib.util
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / 'scripts'


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


#  규율 (1): 케이스 탐색·로딩은 **이 리포에 이미 있다** — 다시 짜지 않는다.
#  `extract_se_network_diagnostics` 의 로더는 2026-09-13 에 L4-06(내용 지문 중복제거)·
#  L4-07(메타 병합)로 고쳐졌으므로 그 수정을 그대로 물려받는다.
_SED = _load('_sed_loader', SCRIPTS / 'extract_se_network_diagnostics.py')
#  ★★ 2판의 핵심 — 면적 helper 를 다시 구현하지 않고 **솔버를 부른다** (AREA-01/02).
_NC = _load('_nc_solver', SCRIPTS / 'network_conductivity.py')
#  ★ 원본 덤프(`post_*/atom_*.liggghts` + `contact_*.liggghts`) 파서는 리포에 이미 있다 —
#    `plastic_coverage.py` 의 `_find_case_files` · `parse_atoms_auto` · `parse_contacts_auto`
#    (규율 ①: 다시 짜지 않는다).  지난 S0 는 `parse_liggghts.py` 가 변환한 CSV 를 읽었고,
#    이 경로는 그 변환을 건너뛴다.  두 경로가 같은 간선을 내는지는 ⑫ 와 `--expect-csv` 가 본다.
_PC = _load('_pc_parsers', SCRIPTS / 'plastic_coverage.py')

#  LHS 덱 규약: `variable r_SE equal 0.001` = 1 µm ⇒ sim 단위 = mm ⇒ sim→µm 배율 1000
#  (`lhs_ext_materialize.py` · `design_performance_dataset.py` 의 `'scale': 1000`).
#  ⚠ 이 도구의 **모든 집계는 scale 에 불변**이다 — ψ 는 a_eff/r_min 비이고 L1 집계도 같은
#    간선 안의 비교라 배율이 상쇄된다 (selftest ⑫c 가 1000 ↔ 1e6 으로 확인).  µm 값 표기에만 쓴다.
RAW_SCALE_UM_PER_SIM = 1000.0


MATCH_STEPS = False     # True 면 atom 덤프를 **마지막 contact 덤프와 같은 step** 으로 고른다 (SELF-30)


def _step_of(path) -> int:
    return int(''.join(ch for ch in Path(path).name if ch.isdigit()) or '0')


def _raw_dump_dir(case_dir: Path):
    """`case_dir` 자체 또는 `post_*/` 에서 (atom, contact) 원본 덤프 → (dir, atom, contact) | None.

    기본 = 생산과 같은 규칙 (`_find_case_files`: atom·contact 각각 **마지막**).  LHS 실측(ibb `lhs00_000`):
    atom 은 5000 간격 405개(마지막 2,425,000), contact 는 마지막 `run 100000` 동안 10000 간격 10개(마지막
    2,420,000) ⇒ 생산은 **5,000 스텝 어긋난 쌍**을 읽는다 (같은 정지 단계).  `MATCH_STEPS` 면 contact 의
    마지막 step 과 **같은 step 의 atom 덤프**를 고른다 — 그 차이가 census 를 움직이는지 재는 용도.
    """
    cands = [case_dir] + sorted(q for q in case_dir.glob('post_*') if q.is_dir())
    for d in cands:
        a, c = _PC._find_case_files(str(d))
        if a and c and a.endswith('.liggghts') and c.endswith('.liggghts'):
            if MATCH_STEPS:
                want = _step_of(c)
                same = [q for q in Path(d).glob('atom_*.liggghts') if _step_of(q) == want]
                if same:
                    a = str(same[0])
                else:
                    raise ValueError(f'{case_dir.name}: contact step {want} 과 같은 atom 덤프가 없다 (--match-steps)')
            return d, a, c
    return None


def discover_raw_cases(root: Path) -> list[Path]:
    """`root/<case>/post_*/` 에 원본 덤프가 있는 케이스 폴더들 (이름순).  CSV 층 없음."""
    out = []
    if not root.is_dir():
        return out
    for d in sorted(q for q in root.iterdir() if q.is_dir()):
        if _raw_dump_dir(d):
            out.append(d)
    return out


def load_case_any(case_dir: Path):
    """→ (atoms, type_map, scale, meta, contacts, source).  CSV 층이 있으면 `_SED` 그대로,
    없으면 원본 덤프.  두 경로의 **출력 형태는 같다** (⑫a 가 동일 자료로 대조)."""
    if (case_dir / 'atoms.csv').exists() and (case_dir / 'contacts.csv').exists():
        atoms, tm, scale, meta = _SED.load_case(case_dir)
        return atoms, tm, scale, meta, _SED.load_contacts(case_dir), 'csv'
    hit = _raw_dump_dir(case_dir)
    if not hit:
        raise ValueError(f'{case_dir.name}: atoms.csv/contacts.csv 도, post_*/ 원본 덤프도 없다')
    d, af, cf = hit
    ra = _PC.parse_atoms_auto(af)
    rc = _PC.parse_contacts_auto(cf)
    if not ra or not rc:
        raise ValueError(f'{case_dir.name}: 덤프 파싱 결과가 비었다 (atoms {len(ra)} · contacts {len(rc)})')
    atoms = {aid: {'type': int(v['type']), 'radius': float(v['r']),
                   'x': float(v['pos'][0]), 'y': float(v['pos'][1]), 'z': float(v['pos'][2])}
             for aid, v in ra.items()}
    contacts = [{'id1': int(c['id1']), 'id2': int(c['id2']),
                 'contact_area': float(c['contactArea']), 'delta': float(c['delta'])}
                for c in rc]
    meta = {'source': 'raw_dump', 'atom_file': af, 'contact_file': cf,
            'scale': RAW_SCALE_UM_PER_SIM}
    return atoms, {}, RAW_SCALE_UM_PER_SIM, meta, contacts, 'raw'


def compare_to_expect(rows, expect_csv: Path, chans):
    """지난 S0 CSV 와 케이스별 대조 → (mismatches, n_compared, missing_here, extra_here).
    보는 열: n_contact_rows · type_hist · 채널별 n_edges/n_deleted.  **어느 하나라도** 다르면
    mismatch 다 — 새 경로(원본 덤프)가 옛 경로(CSV)를 재현하지 못한다는 뜻이다."""
    with expect_csv.open(encoding='utf-8') as f:
        exp = {r['case']: r for r in csv.DictReader(f)}
    here = {r['case']: r for r in rows}
    keys = ['n_contact_rows', 'type_hist'] + [f'{c}_{k}' for c in chans for k in ('n_edges', 'n_deleted')]
    mism = []
    for name in sorted(set(exp) & set(here)):
        for k in keys:
            if k not in exp[name]:
                continue
            a, b = str(exp[name][k]).strip(), str(here[name][k]).strip()
            if a != b:
                mism.append((name, k, a, b))
    return mism, len(set(exp) & set(here)), sorted(set(exp) - set(here)), sorted(set(here) - set(exp))


#  기록용 문턱 (판정에 쓰지 않는다 — 판정은 솔버의 `R_constriction` 이 한다)
PSI_FLOOR = 1e-4
S_STAR = 1.0 - PSI_FLOOR ** (2.0 / 3.0)          # 0.99784556531
AREA_FRAC = S_STAR ** 2                           # 0.9956957722087699

#: 채널 → (build_network mode, target_types 선택자).
#  ⚠ 채널 필터는 `mode` 가 아니라 **`target_types`** 로 걸린다 (`network_conductivity.py:251`).
#    생산 `main` 이 그렇게 만든다:
#      ionic      target_types = [k for k,v in type_map.items() if v == 'SE']
#      electronic am_types     = [k for k,v in type_map.items() if 'AM' in v]
#      thermal    전부 (thermal 가지는 `:246` 에서 필터를 건너뛴다)
#    처음에 셋 다 전체 type 을 넘겼더니 ionic·electronic 이 AM–SE 를 **받아 버렸다**
#    (selftest ⑤a·⑤b 가 빨간불).  그 반례를 그대로 검사로 남긴다.
CHANNELS = {
    'ionic':      ('ionic',      lambda tm: {k for k, v in tm.items() if v == 'SE'}),
    'electronic': ('electronic', lambda tm: {k for k, v in tm.items() if 'AM' in str(v)}),
    'thermal':    ('thermal',    lambda tm: set(tm)),
}

#: 허용 상 이름 — 미등록 type 을 조용히 SE 로 만들지 않는다 (Codex [P2])
_AM = frozenset({'AM_P', 'AM_S', 'AM'})
_SE = frozenset({'SE'})


def _pair_kind(t1, t2):
    """상 쌍 분류.  **모르는 상은 `UNKNOWN`** 이다 (옛 판은 "AM 이 아니면 SE" 였다)."""
    def k(t):
        if t in _AM:
            return 'AM'
        if t in _SE:
            return 'SE'
        return '?'
    a, b = k(t1), k(t2)
    if '?' in (a, b):
        return 'UNKNOWN'
    return {('AM', 'AM'): 'AM_AM', ('SE', 'SE'): 'SE_SE'}.get((a, b), 'AM_SE')


def type_map_from_deck(deck_path):
    """LIGGGHTS 덱에서 **type → 상** 지도를 유도한다.  두 신호를 교차확인한다.

    ★ 왜 필요한가 (실측): LHS 코퍼스는 **케이스마다 type 구성이 다르다**.
      `lhs00_000` 은 헤더가 `bimodal (3-type)` 인데 `lhs00_100` 의 원자 분포는
      `{1: 796, 2: 30315}` 로 **type 3 이 0개**다.  하나를 박아 두면 채널 분류가 통째로
      틀린다 — `AREA-02`(모집단이 조용히 달라진다)를 재생산하는 자리다.

    신호 ①  `fix pts<N> ... particletemplate/sphere ... atom_type <T> ... radius constant ${VAR}`
             → VAR 이름(`r_AM_P` · `r_AM_S` · `r_SE`)이 상을 말한다.
    신호 ②  `fix m1 ... youngsModulus peratomtype E1 E2 ...`
             → **연화된 값**(<1e7 sim)이 SE 다 (AM 은 1.4e8).

    ⛔ 둘이 어긋나거나 어느 하나라도 못 읽으면 **거부**한다 (추측하지 않는다).
    """
    txt = Path(deck_path).read_text(errors='replace')
    tm, src = {}, {}
    for raw in txt.split('\n'):
        line = raw.split('#', 1)[0].strip()
        if 'particletemplate/sphere' not in line:
            continue
        toks = line.split()
        t = var = None
        for i, w in enumerate(toks):
            if w == 'atom_type' and i + 1 < len(toks):
                try:
                    t = int(toks[i + 1])
                except ValueError:
                    pass
            if w == 'radius' and i + 2 < len(toks) and toks[i + 1] == 'constant':
                var = toks[i + 2]
        if t is None or not var:
            continue
        u = var.upper().strip('${}')
        #  ⚠ 순서가 중요하다 — mono 케이스는 `${r_AM}` 로 **접미사가 없다**
        #    (`lhs00_100: mono_AM_S (2-type)` 의 덱이 그렇다).  AM_P/AM_S 를 먼저 보고
        #    그 다음 SE, 마지막에 맨 AM.
        ph = ('AM_P' if 'AM_P' in u else
              'AM_S' if 'AM_S' in u else
              'SE'   if 'SE'   in u else
              'AM'   if 'AM'   in u else None)
        if ph is None:
            raise ValueError(f'{deck_path}: atom_type {t} 의 반경 변수 {var!r} 에서 '
                             f'상을 못 읽는다 (AM_P·AM_S·AM·SE 중 하나여야 한다)')
        if t in tm and tm[t] != ph:
            raise ValueError(f'{deck_path}: atom_type {t} 가 {tm[t]} 와 {ph} 로 중복 정의')
        tm[t] = ph
        src[t] = var
    if not tm:
        raise ValueError(f'{deck_path}: particletemplate/sphere 를 못 찾았다')

    #  ── 신호 ② 로 **교차확인** ────────────────────────────────────────────
    es = []
    for raw in txt.split('\n'):
        line = raw.split('#', 1)[0].strip()
        if 'youngsModulus' in line and 'peratomtype' in line:
            for p in line.split('peratomtype')[-1].split():
                try:
                    es.append(float(p))
                except ValueError:
                    break
            break
    if es:
        soft = {i + 1 for i, e in enumerate(es) if e < 1e7}
        declared_se = {t for t, v in tm.items() if v == 'SE'}
        if soft and declared_se and soft != declared_se:
            raise ValueError(
                f'{deck_path}: 두 신호가 어긋난다 — 템플릿이 말하는 SE={sorted(declared_se)} '
                f'인데 youngsModulus 의 연화 type={sorted(soft)} (E={es}).  추측하지 않는다.')
    return tm, src


def audit_case(case_dir, contact_mode='physics', channels=('ionic', 'electronic', 'thermal'),
               deck_dir=None):
    """한 케이스 — **솔버가 만든 간선**에서 `R_constriction == 0` 을 센다.

    ⚠ 예외를 **비삭제로 만들지 않는다** — 실패는 `error` 로 올리고 `None` 을 돌려준다
    (옛 판은 helper 예외를 삼켜 분모에는 남기고 삭제는 0 으로 셌다).
    """
    atoms, type_map, scale, _meta, contacts, source = load_case_any(case_dir)
    #  ★ 덱이 있으면 **그것이 정본**이다 — meta.json 의 손으로 적은 지도보다 우선한다
    #    (케이스마다 type 구성이 다르다는 것을 실측으로 확인했다).
    deck_used = ''
    if source == 'raw' and not deck_dir:
        raise ValueError(f'{case_dir.name}: 원본 덤프 경로에는 type_map 이 없다 — --deck-dir 필수')
    if deck_dir:
        cands = [Path(deck_dir) / case_dir.name / f'input_{case_dir.name}.liggghts',
                 Path(deck_dir) / f'input_{case_dir.name}.liggghts']
        dk = next((p for p in cands if p.is_file()), None)
        if dk is None:
            raise ValueError(f'덱을 못 찾았다: {[str(p) for p in cands]}')
        type_map, _src = type_map_from_deck(dk)
        deck_used = str(dk)
    if not contacts:
        raise ValueError('접촉 행이 0개')
    plate_z = _SED.estimate_plate_z(atoms)
    #  box: 최소영상이 절대 안 걸리게 넉넉히 (삭제 집계는 상자에 불변 — 헤더 참조)
    span = max((max(a['x'] for a in atoms.values()) - min(a['x'] for a in atoms.values()),
                max(a['y'] for a in atoms.values()) - min(a['y'] for a in atoms.values()),
                1e-9))
    box = span * 1000.0

    from collections import Counter as _C
    type_hist = _C(a['type'] for a in atoms.values())
    all_types = sorted(type_hist)
    row = {'case': case_dir.name, 'contact_mode': contact_mode, 'source': source,
           'atom_step': _step_of(_meta.get('atom_file', '')) if _meta.get('atom_file') else '',
           'contact_step': _step_of(_meta.get('contact_file', '')) if _meta.get('contact_file') else '',
           'n_contact_rows': len(contacts),
           'type_hist': ';'.join(f'{t}:{type_hist[t]}' for t in all_types),
           'type_map': ';'.join(f'{k}={v}' for k, v in sorted(type_map.items())),
           'deck': deck_used}
    for ch in channels:
        mode, pick = CHANNELS[ch]
        tt = pick(type_map)
        #  ⚠ 빈 선택을 **전체로 대체하지 않는다** — 그러면 채널 필터가 조용히 사라진다.
        if not tt:
            raise ValueError(
                f'채널 {ch}: type_map 에서 고른 target_types 가 비었다.  '
                f'type_map={dict(sorted(type_map.items()))} · '
                f'원자 type 분포={dict(type_hist)}')
        net = _NC.build_network(atoms, contacts, tt, scale,
                                plate_z, box_x=box, box_y=box,
                                mode=mode, type_map=type_map,
                                contact_mode=contact_mode)
        #  `build_network:196` 은 `target_ids` 가 비면 **None** 을 돌려준다.
        if net is None:
            n_hit = sum(type_hist[t] for t in tt if t in type_hist)
            raise ValueError(
                f'채널 {ch}: build_network 가 None (해당 상의 입자가 없다).  '
                f'target_types={sorted(tt)} · 그 type 의 원자 {n_hit}개 · '
                f'원자 type 분포={dict(type_hist)} · '
                f'type_map={dict(sorted(type_map.items()))}')
        edges = net['edges'] if isinstance(net, dict) else net[1]
        n = d = 0
        by_kind = {}
        l1 = _l1_counters()
        for e in edges:
            kd = _pair_kind(type_map.get(e['type1'], '?'), type_map.get(e['type2'], '?'))
            n += 1
            dele = (e['R_constriction'] == 0.0)
            d += 1 if dele else 0
            s_ = by_kind.setdefault(kd, [0, 0])
            s_[0] += 1
            s_[1] += 1 if dele else 0
            _l1_tally(l1, e)
        row[f'{ch}_n_edges'] = n
        row[f'{ch}_n_deleted'] = d
        row[f'{ch}_deleted_pct'] = round(100.0 * d / n, 4) if n else 0.0
        for kd in ('AM_AM', 'AM_SE', 'SE_SE', 'UNKNOWN'):
            nn, dd = by_kind.get(kd, (0, 0))
            row[f'{ch}_{kd}_n'] = nn
            row[f'{ch}_{kd}_deleted'] = dd
        #  L1-01 · L1-02 는 채널 무관 간선 성질이라 **전 간선 채널(thermal)** 에서만 적는다.
        #  (같은 간선을 세 번 세지 않는다.)
        if ch == 'thermal':
            for k, v in l1.items():
                row[f'l1_{k}'] = v
    return row


# ── L1-01 · L1-02 — 실제 간선에서 (i) 하한>상한 (ii) 정확 lens 가 a_eff 를 바꾸는가 ──
#    `plastic_coverage.py` 가 계측만 붙이고 값은 안 바꿨다 (저자 결정 선행).  여기서는
#    솔버가 만든 간선의 `A_components` 를 읽어 **코퍼스 크기**를 잰다.  합성 스윕
#    (`plastic_coverage.py --audit-l1`) 은 코퍼스 발생률이 아니다 — 이것이 그 값이다.
def _l1_counters():
    return {'n_ladder': 0, 'n_cap_conflict': 0, 'n_vol_neg': 0,
            'n_exact_avail': 0, 'n_A_final_changed': 0, 'n_a_eff_changed': 0,
            'n_rc_branch_changed': 0,
            #  P2-R2-08 — 협착 항 삭제(Rc==0)를 **두 부류**로 가른다:
            #    floor_only  = ψ ≤ 1e-4 인데 s_clamped < 1  (모델의 양수를 floor 가 지운다)
            #    clamp_zero  = s_raw ≥ 1 → clamp 로 s = 1, ψ = 0 (A_surface 를 원판으로 읽어 강제된 0)
            #  ⚠ binding=geom/tabor 로 나누면 틀린다 — δ=.12 는 tabor 결속인데 이미 s_raw 1.124 (Codex).
            'n_rc0': 0, 'n_rc0_floor_only': 0, 'n_rc0_clamp_zero': 0}


def _s_raw_clamped(e):
    """솔버가 쓴 a = √(A_contact/π) 와 r_min 에서 (s_raw, s_clamped).  `network_conductivity.py:323·386·395`."""
    A = e.get('A_contact') or 0.0
    r_min = min(e['r1'], e['r2'])
    a = math.sqrt(A / math.pi) if A > 0 else 0.0
    if r_min <= 0:
        return 0.0, 0.0
    return a / r_min, min(a, r_min) / r_min


def _l1_tally(c, e):
    #  삭제 부류 (사다리 도달 여부와 무관하게 Rc==0 인 간선 전부)
    if e.get('R_constriction') == 0.0:
        c['n_rc0'] += 1
        s_raw, s_cl = _s_raw_clamped(e)
        if s_raw >= 1.0:
            c['n_rc0_clamp_zero'] += 1
        elif s_cl < 1.0:
            c['n_rc0_floor_only'] += 1
    comp = e.get('A_components')
    if not comp or comp.get('cap_conflict') is None:
        return                                # 탄성 조기반환 / no_delta — 사다리에 안 옴
    c['n_ladder'] += 1
    if comp['cap_conflict']:
        c['n_cap_conflict'] += 1
    vl = comp.get('V_overlap_legacy_um3')
    if vl is not None and vl < 0:
        c['n_vol_neg'] += 1
    ave = comp.get('A_volume_exact_um2')
    if ave is None or comp.get('A_tabor_um2') is None or comp.get('A_geom_um2') is None:
        return
    c['n_exact_avail'] += 1
    lower = comp['A_lower_um2']
    A_exact = max(lower, min(comp['A_tabor_um2'], ave, comp['A_geom_um2']))
    A_legacy = comp['A_final_um2']
    if A_exact != A_legacy:
        c['n_A_final_changed'] += 1
    r_min = min(e['r1'], e['r2'])
    a_l = min(math.sqrt(A_legacy / math.pi) if A_legacy > 0 else 0.0, r_min)
    a_e = min(math.sqrt(A_exact / math.pi) if A_exact > 0 else 0.0, r_min)
    if a_e != a_l:
        c['n_a_eff_changed'] += 1
    #  ψ 분기 (≤1e-4 → R_c=0) 가 갈리는가 — `network_conductivity.py:396-401` 과 같은 식
    def _branch(a):
        psi = max(1.0 - a / r_min, 0.0) ** 1.5 if r_min > 0 else 0.0
        return psi > 1e-4
    if _branch(a_e) != _branch(a_l):
        c['n_rc_branch_changed'] += 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description='협착 항이 삭제된 **간선** 비율 (면적 계약 S0, 2판 — 솔버 호출)')
    ap.add_argument('--contact-mode', default='physics',
                    choices=['physics', 'hertzian'],
                    help='솔버의 contact_mode.  생산 Physics 가지가 기본. '
                         'hertzian 은 ψ 삭제 가지를 **타지 않는다** (대조용).')
    ap.add_argument('--channels', default='ionic,electronic,thermal',
                    help='채널 — ionic=SE–SE · electronic=AM–AM · thermal=전부')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--out-csv', default='')
    #  ⚠ CLAUDE.md 가 경고한 자리 — **코드 폴더 ≠ 데이터 폴더**.
    ap.add_argument('--webapp', default='',
                    help='results/ · archive/ 가 있는 폴더.  env AUDIT_WEBAPP 도 가능.')
    ap.add_argument('--deck-dir', default='',
                    help='LIGGGHTS 덱이 있는 폴더 — `<deck-dir>/<case>/input_<case>.liggghts`.  '
                         '주면 **덱에서 type_map 을 유도**한다 (meta.json 보다 우선).')
    ap.add_argument('--expect-csv', default='',
                    help='지난 S0 산출 CSV — 케이스별 n_contact_rows·type_hist·n_edges·n_deleted 를 '
                         '대조한다.  하나라도 다르면 rc=4 (새 경로가 옛 경로를 재현하지 못함).')
    ap.add_argument('--match-steps', action='store_true',
                    help='atom 덤프를 마지막 contact 덤프와 같은 step 으로 고른다 (기본은 생산과 같이 각각 마지막; SELF-30)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    global MATCH_STEPS
    MATCH_STEPS = bool(a.match_steps)
    if MATCH_STEPS:
        print('⚠ --match-steps: atom 덤프를 contact 의 마지막 step 에 맞춘다 (생산 규칙과 다르다 — 민감도 측정용)')

    import os as _os
    wp = a.webapp or _os.environ.get('AUDIT_WEBAPP', '')
    if wp:
        _SED.WEBAPP = Path(wp).expanduser().resolve()
    print(f'webapp = {_SED.WEBAPP}')
    if not _SED.WEBAPP.is_dir():
        print(f'\n⛔ 그런 폴더가 없다: {_SED.WEBAPP}')
        return 2
    subs = [d for d in ('results', 'archive') if (_SED.WEBAPP / d).is_dir()]
    flat = False
    if not subs:
        #  results/·archive/ 층이 없으면 **폴더 자체**가 케이스들을 담고 있는지 본다
        #  (`~/lhs_local/lhs00_100/atoms.csv` 같은 로컬 보관 폴더).  없으면 **왜** 못 찾았는지
        #  실제 파일 목록을 찍는다 — 경로를 두 번 물어보지 않기 위해 (2026-09-13 실사고).
        flat = bool(_SED.discover_cases(flat=True))
        raw = [] if flat else discover_raw_cases(_SED.WEBAPP)
        if not flat and not raw:
            print(f'\n⛔ {_SED.WEBAPP} 안에 results/ 도 archive/ 도 없고, 직접 담긴 케이스도 없다')
            print(_SED.case_layout_report(_SED.WEBAPP))
            print('  (또는 케이스 폴더마다 post_*/atom_*.liggghts + contact_*.liggghts + input_<case>.liggghts)')
            return 2
        print('  하위: (없음 — 폴더가 케이스를 직접 담고 있다: '
              + ('flat CSV 모드)' if flat else f'**원본 덤프 모드**, {len(raw)}개 · scale={RAW_SCALE_UM_PER_SIM:g})'))
    else:
        raw = []
        print(f'  하위: {", ".join(subs)}')

    chans = tuple(c.strip() for c in a.channels.split(',') if c.strip())
    bad = [c for c in chans if c not in CHANNELS]
    if bad:
        print(f'⛔ 모르는 채널: {bad}')
        return 2

    cases = raw if raw else _SED.discover_cases(flat=flat)
    if a.limit:
        cases = cases[:a.limit]
    print(f'케이스 {len(cases)}개 · contact_mode={a.contact_mode} · 채널 {",".join(chans)}')
    print(f'기록용 문턱: A >= {AREA_FRAC:.16f} · π · r_min²   '
          f'(판정은 솔버의 R_constriction 이 한다)')
    if not cases:
        print('\n⛔ 접촉 자료를 못 찾았다 — atoms.csv + contacts.csv + (input_params|meta).json')
        return 1

    rows, errs = [], []
    for i, d in enumerate(cases):
        try:
            r = audit_case(d, contact_mode=a.contact_mode, channels=chans,
                           deck_dir=(a.deck_dir or None))
        except Exception as e:                      # ⚠ 실패를 **비삭제로 만들지 않는다**
            errs.append((d.name, f'{type(e).__name__}: {e}'))
            print(f'  [{i+1:>3}/{len(cases)}] {d.name[:34]:34s}  ⛔ {type(e).__name__}')
            continue
        rows.append(r)
        pc = r.get(f'{chans[0]}_deleted_pct', 0.0)
        print(f'  [{i+1:>3}/{len(cases)}] {r["case"][:34]:34s} '
              f'{chans[0]} {r.get(chans[0]+"_n_edges",0):>8,d} edge  삭제 {pc:>6.2f} %')

    if errs:
        print(f'\n⛔ 실패 {len(errs)}건 — **집계를 발행하지 않는다** (부분 census 금지):')
        for nm, msg in errs[:10]:
            print(f'    {nm}: {msg}')
        return 3
    if not rows:
        print('집계할 행이 없다.')
        return 1

    print('\n═══ 간선 가중 집계 ═══')
    print(f'  케이스 {len(rows)} (실패 0)')
    for ch in chans:
        n = sum(r[f'{ch}_n_edges'] for r in rows)
        d = sum(r[f'{ch}_n_deleted'] for r in rows)
        print(f'  {ch:11s} 삭제 {d:>10,d} / {n:>10,d} = '
              f'{(100.0*d/n if n else 0.0):7.3f} %')
        for kd in ('AM_AM', 'AM_SE', 'SE_SE', 'UNKNOWN'):
            nn = sum(r[f'{ch}_{kd}_n'] for r in rows)
            dd = sum(r[f'{ch}_{kd}_deleted'] for r in rows)
            if nn:
                print(f'      {kd:8s} {dd:>10,d} / {nn:>10,d} = {100.0*dd/nn:7.3f} %')
    print('\n⚠ 이것은 **협착 항** 삭제다 (R_bulk 는 보통 남는다).  간선 삭제·총저항 0 과 다르다.')
    print('⚠ 채널별로 따로 읽을 것 — AM–SE 비율을 이온망 하한으로 쓰지 않는다 (AREA-02).')

    if 'thermal' in chans and any('l1_n_ladder' in r for r in rows):
        tot = {k: sum(r.get(f'l1_{k}', 0) for r in rows) for k in _l1_counters()}
        nl = tot['n_ladder']; ne = tot['n_exact_avail']
        pc = lambda k, den: (100.0 * tot[k] / den) if den else 0.0
        print('\n═══ L1-01 · L1-02 (전 간선, 사다리 도달분) ═══')
        print(f'  사다리 도달 간선                     : {nl:>10,d}')
        print(f'  L1-01 cap_conflict (하한 > 상한)     : {tot["n_cap_conflict"]:>10,d} = {pc("n_cap_conflict", nl):7.3f} %')
        print(f'  L1-02 legacy V_overlap < 0           : {tot["n_vol_neg"]:>10,d} = {pc("n_vol_neg", nl):7.3f} %')
        print(f'  정확 lens 계산 가능                  : {ne:>10,d}')
        print(f'  정확 lens 로 A_final 이 바뀜         : {tot["n_A_final_changed"]:>10,d} = {pc("n_A_final_changed", ne):7.3f} %')
        print(f'  정확 lens 로 **a_eff** 가 바뀜       : {tot["n_a_eff_changed"]:>10,d} = {pc("n_a_eff_changed", ne):7.3f} %')
        print(f'  정확 lens 로 ψ 분기(R_c=0)가 바뀜    : {tot["n_rc_branch_changed"]:>10,d} = {pc("n_rc_branch_changed", ne):7.3f} %')
        print('  ⚠ a_eff 가 바뀐 간선 수는 σ 변화량이 아니다 (I²R 기여도 미측정).')
        print('  ⚠ 값은 안 바꿨다 — 저자 결정(전체 lens 인가 상별 몫인가) 뒤에 세대 2 로.')
        n0 = tot['n_rc0']
        print('\n═══ 삭제(Rc=0)의 두 부류 — P2-R2-08 (전 간선) ═══')
        print(f'  Rc == 0 간선                         : {n0:>10,d}')
        print(f'    clamp_zero (s_raw ≥ 1 → s=1, ψ=0)   : {tot["n_rc0_clamp_zero"]:>10,d} = {pc("n_rc0_clamp_zero", n0):7.3f} %')
        print(f'    floor_only (ψ ≤ 1e-4 이고 s < 1)    : {tot["n_rc0_floor_only"]:>10,d} = {pc("n_rc0_floor_only", n0):7.3f} %')
        print('  ⚠ clamp_zero 는 a=b 의 독립 측정이 아니다 — A_surface 를 원판으로 읽어 강제된 s=1 이다.')
        print('  ⚠ floor_only 만이 "모델의 양수를 floor 가 지운" 부류다 (올바른 ψ 배치에서도 양수).')

    if a.out_csv:
        p = Path(a.out_csv)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        print(f'\n→ {p}')

    if a.expect_csv:
        mism, n_cmp, missing, extra = compare_to_expect(rows, Path(a.expect_csv), chans)
        print(f'\n═══ 지난 S0 CSV 와 대조 ({a.expect_csv}) ═══')
        print(f'  겹치는 케이스 {n_cmp} · 지난 CSV 에만 {len(missing)} · 이번에만 {len(extra)}')
        if mism:
            print(f'  ⛔ 불일치 {len(mism)}건 — **새 경로가 옛 경로를 재현하지 못한다**:')
            for name, k, va, vb in mism[:20]:
                print(f'    {name:14s} {k:26s} 지난={va}  이번={vb}')
            return 4
        print('  ✓ 겹치는 케이스 전부에서 n_contact_rows · type_hist · 채널별 n_edges/n_deleted 일치')
    return 0


def _selftest() -> int:
    """★ **판별력**이 핵심이다 — 초판은 소스 문자열 존재만 봐서 Rc=0 분기를 바꿔도 13/13 PASS 였다.

    2판은 실제 `build_network` 를 돌려 그 출력을 세므로, ⑥ 이 *"솔버 분기를 바꾸면 이 수가
    움직인다"* 를 **직접** 확인한다.
    """
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(('  ✓ ' if cond else '  ✗ ') + name + (f'   {extra}' if extra else ''))
        ok = ok and bool(cond)

    print('협착 삭제 census (S0 2판 — 솔버 호출)')

    R = 1.0                                    # sim 반경
    scale = 1.0

    def net(rows, mode='thermal', cm='physics'):
        atoms = {1: {'type': 1, 'radius': R, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                 2: {'type': 3, 'radius': R, 'x': 2 * R, 'y': 0.0, 'z': 0.0}}
        tm = {1: 'AM_P', 3: 'SE'}
        #  ⚠ 생산과 같은 방식 — 채널 필터는 target_types 가 건다
        tt = CHANNELS[{'ionic': 'ionic', 'electronic': 'electronic'}.get(mode, 'thermal')][1](tm)
        n = _NC.build_network(atoms, rows, tt, scale, 10.0,
                              box_x=1e4, box_y=1e4, mode=mode, type_map=tm,
                              contact_mode=cm)
        e = n['edges'] if isinstance(n, dict) else n[1]
        return e

    deep = {'id1': 1, 'id2': 2, 'contact_area': 0.998 * math.pi * R * R, 'delta': 0.0}
    shallow = {'id1': 1, 'id2': 2, 'contact_area': 1e-6, 'delta': 1e-6}

    # ── ① AREA-01: δ=0 인데 native 면적이 크면 **솔버는 삭제**한다 ──────────
    e = net([deep])
    chk('①a AREA-01: δ=0 · native 면적 0.998πr² → 간선 1개', len(e) == 1)
    chk('①b AREA-01: 그 간선의 R_constriction 이 **0** (옛 S0 는 이걸 0 %로 셌다)',
        len(e) == 1 and e[0]['R_constriction'] == 0.0,
        f"Rc={e[0]['R_constriction'] if e else '—'}")

    # ── ② 대조: 얕은 접촉은 삭제되지 않는다 (게이트가 "항상 삭제" 가 아니다) ─
    e = net([shallow])
    chk('② 대조: 얕은 접촉은 Rc > 0',
        len(e) == 1 and e[0]['R_constriction'] > 0.0,
        f"Rc={e[0]['R_constriction'] if e else '—'}")

    # ── ③ AREA-02: 같은 ID쌍 여러 행 → **간선 1개**, 마지막 행이 이긴다 ─────
    e = net([deep] * 9 + [shallow])
    chk('③a AREA-02: raw 10행 → 간선 **1개** (옛 S0 는 10행을 셌다)', len(e) == 1)
    chk('③b AREA-02: 마지막이 shallow 이면 **삭제 아님** (옛 S0 는 90 % 삭제)',
        len(e) == 1 and e[0]['R_constriction'] > 0.0)
    e = net([shallow] * 9 + [deep])
    chk('③c AREA-02: 마지막이 deep 이면 **삭제** (옛 S0 는 10 %)',
        len(e) == 1 and e[0]['R_constriction'] == 0.0)

    # ── ④ Hertz-명명 가지에는 ψ 삭제가 없다 ────────────────────────────────
    e = net([deep], cm='hertzian')
    chk('④ 생산 Hertz 가지는 같은 접촉에서 Rc > 0 (옛 S0 는 100 % 삭제로 셌다)',
        len(e) == 1 and e[0]['R_constriction'] > 0.0,
        f"Rc={e[0]['R_constriction'] if e else '—'}")

    # ── ⑤ 채널 필터가 솔버의 것이다 ────────────────────────────────────────
    chk('⑤a ionic 은 AM–SE 를 안 받는다', len(net([deep], mode='ionic')) == 0)
    chk('⑤b electronic 도 AM–SE 를 안 받는다', len(net([deep], mode='electronic')) == 0)
    chk('⑤c thermal 은 받는다', len(net([deep], mode='thermal')) == 1)
    chk('⑤d 상 분류가 "AM 이 아니면 SE" 가 아니다 — 미등록은 UNKNOWN',
        _pair_kind('AM_P', 'type9') == 'UNKNOWN' and _pair_kind('?', '?') == 'UNKNOWN'
        and _pair_kind('AM_P', 'SE') == 'AM_SE')

    # ── ⑥ ★★ 판별력: 솔버의 Rc=0 분기를 바꾸면 이 census 가 **반드시** 움직인다 ─
    src = (SCRIPTS / 'network_conductivity.py').read_text(encoding='utf-8')
    mutated = src.replace('                R_constriction = 0.0\n',
                          '                R_constriction = R_Maxwell\n', 1)
    chk('⑥a 변이 지점이 실재한다 (소스가 바뀌었다)', mutated != src)
    import types as _t
    m = _t.ModuleType('_nc_mut')
    m.__file__ = str(SCRIPTS / 'network_conductivity.py')
    sys.path.insert(0, str(SCRIPTS))
    exec(compile(mutated, m.__file__, 'exec'), m.__dict__)
    atoms = {1: {'type': 1, 'radius': R, 'x': 0.0, 'y': 0.0, 'z': 0.0},
             2: {'type': 3, 'radius': R, 'x': 2 * R, 'y': 0.0, 'z': 0.0}}
    em = m.build_network(atoms, [deep], {1, 3}, scale, 10.0, box_x=1e4, box_y=1e4,
                         mode='thermal', type_map={1: 'AM_P', 3: 'SE'},
                         contact_mode='physics')
    em = em['edges'] if isinstance(em, dict) else em[1]
    chk('⑥b ★ 변이판에서는 같은 접촉이 **삭제되지 않는다** — 이 검사에 판별력이 있다 '
        '(초판은 이 변이에도 13/13 PASS 였다)',
        len(em) == 1 and em[0]['R_constriction'] != 0.0,
        f"변이 Rc={em[0]['R_constriction'] if em else '—'}")

    # ── ⑦ 문턱 기록값 (판정용 아님) ────────────────────────────────────────
    chk('⑦ 기록 문턱 A/(πr²) = 0.9956957722087699 (ψ 정확 0 인 1 과 **다르다**)',
        abs(AREA_FRAC - 0.9956957722087699) < 1e-15, f'{AREA_FRAC!r}')

    # ── ⑨ 덱에서 type_map 유도 — **케이스마다 다르다** (실측 두 종류) ──────
    import tempfile as _tf
    tdir = Path(_tf.mkdtemp())
    bi = tdir / 'input_bi.liggghts'
    bi.write_text(
        '# lhs00_000: bimodal (3-type) | LHS design\n'
        'fix m1 all property/global youngsModulus peratomtype 1.4e8 1.4e8 0.135e7\n'
        'fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 '
        'radius constant ${r_AM_P}\n'
        'fix pts2 all particletemplate/sphere 15485867 atom_type 2 density constant 4800 '
        'radius constant ${r_AM_S}\n'
        'fix pts3 all particletemplate/sphere 32452843 atom_type 3 density constant 2000 '
        'radius constant ${r_SE}\n')
    mo = tdir / 'input_mono.liggghts'
    mo.write_text(
        '# lhs00_100: mono_AM_S (2-type) | LHS design\n'
        'fix m1 all property/global youngsModulus peratomtype 1.4e8 0.135e7\n'
        'fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 '
        'radius constant ${r_AM}\n'
        'fix pts2 all particletemplate/sphere 32452843 atom_type 2 density constant 2000 '
        'radius constant ${r_SE}\n')
    chk('⑨a 3-type 덱 → {1:AM_P, 2:AM_S, 3:SE}',
        type_map_from_deck(bi)[0] == {1: 'AM_P', 2: 'AM_S', 3: 'SE'},
        str(type_map_from_deck(bi)[0]))
    chk('⑨b ★ 2-type mono 덱 → {1:AM, 2:SE} (접미사 없는 `${r_AM}` — 실측 반례)',
        type_map_from_deck(mo)[0] == {1: 'AM', 2: 'SE'},
        str(type_map_from_deck(mo)[0]))
    chk('⑨c 그 둘이 **다르다** — 하나를 박아 두면 채널 분류가 틀린다',
        type_map_from_deck(bi)[0] != type_map_from_deck(mo)[0])
    bad = tdir / 'input_bad.liggghts'
    bad.write_text(
        'fix m1 all property/global youngsModulus peratomtype 0.135e7 1.4e8\n'
        'fix pts1 all particletemplate/sphere 1 atom_type 1 density constant 4800 '
        'radius constant ${r_AM}\n'
        'fix pts2 all particletemplate/sphere 2 atom_type 2 density constant 2000 '
        'radius constant ${r_SE}\n')
    try:
        type_map_from_deck(bad); raised = False
    except ValueError:
        raised = True
    chk('⑨d 대조: 두 신호(템플릿 이름 ↔ 연화 영률)가 어긋나면 **거부**한다', raised)

    # ── ⑧ 계약·판정문이 실재하고 서로를 가리키는가 ─────────────────────────
    doc = ROOT / 'docs' / 'area_contract_20260913.md'
    ver = ROOT / 'docs' / 'reviews' / 'codex_verdict_area_contract_20260913.md'
    chk('⑧ 계약·판정문 둘 다 있다', doc.exists() and ver.exists())

    # ── ⑩ L1-01 · L1-02 집계가 실제 간선에서 **판별력 있게** 돈다 ──────────
    #    (a) 얕은 겹침 + 큰 native 면적 → 하한 > 상한 → cap_conflict 가 세어진다
    #    (b) 깊은 겹침 → cap_conflict 아님 (검사가 "항상 켜짐" 이 아니다)
    #    (c) 정확 lens 가 a_eff 를 실제로 바꾸는 간선 / 안 바꾸는 간선이 **둘 다** 있다
    #  ⚠ 위 `net()` 은 R = 1 sim 단위 = **1 m 구**다 (SI 상수 앞에서 volume cap 이
    #    천문학적으로 커져 절대 결속하지 않는다).  L1-02 는 **실제 규모**(R = 0.5 µm,
    #    sim = m, scale = 1e6)에서만 볼 수 있다 — 첫 판이 여기서 빨간불을 냈다.
    R_si = 0.5e-6
    Rs_ = R_si / 2.0

    def net_si(rows, cm='physics'):
        atoms = {1: {'type': 1, 'radius': R_si, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                 2: {'type': 3, 'radius': R_si, 'x': 2 * R_si, 'y': 0.0, 'z': 0.0}}
        tm = {1: 'AM_P', 3: 'SE'}
        tt = CHANNELS['thermal'][1](tm)
        n = _NC.build_network(atoms, rows, tt, 1e6, 10.0,
                              box_x=1.0, box_y=1.0, mode='thermal', type_map=tm,
                              contact_mode=cm)
        return n['edges'] if isinstance(n, dict) else n[1]

    conf = {'id1': 1, 'id2': 2, 'contact_area': 2.0 * math.pi * Rs_ * (0.01 * Rs_),
            'delta': 0.01 * Rs_}                       # ligg ≈ 2×Hertz > Tabor (얕음)
    c1 = _l1_counters(); [_l1_tally(c1, e_) for e_ in net_si([conf])]
    chk('⑩a L1-01: 얕은 겹침 + 큰 native 면적 → cap_conflict 1/1',
        c1['n_ladder'] == 1 and c1['n_cap_conflict'] == 1, str(c1))
    deep2 = {'id1': 1, 'id2': 2, 'contact_area': 0.0, 'delta': 0.5 * Rs_}
    c2 = _l1_counters(); [_l1_tally(c2, e_) for e_ in net_si([deep2])]
    chk('⑩b 대조: 깊은 겹침은 cap_conflict 0/1', c2['n_ladder'] == 1 and c2['n_cap_conflict'] == 0,
        str(c2))
    #  (c) volume 이 결속하는 중간 겹침 — 정확 lens(≈2배) 가 a_eff 를 바꾼다
    mid = {'id1': 1, 'id2': 2, 'contact_area': 0.0, 'delta': 0.05 * Rs_}
    c3 = _l1_counters(); [_l1_tally(c3, e_) for e_ in net_si([mid])]
    lower_wins = {'id1': 1, 'id2': 2, 'contact_area': 0.9 * math.pi * R_si * R_si,
                  'delta': 0.05 * Rs_}
    c4 = _l1_counters(); [_l1_tally(c4, e_) for e_ in net_si([lower_wins])]
    chk('⑩c L1-02 판별력: volume 결속 간선은 a_eff 가 바뀌고, 하한이 이기는 간선은 안 바뀐다',
        c3['n_exact_avail'] == 1 and c3['n_a_eff_changed'] == 1
        and c4['n_exact_avail'] == 1 and c4['n_a_eff_changed'] == 0,
        f'volume결속 {c3["n_a_eff_changed"]}/1 · 하한승 {c4["n_a_eff_changed"]}/1 · '
        f'mid binding={net_si([mid])[0]["A_components"]["binding"]}')
    chk('⑩d 계측 키가 솔버 간선의 A_components 에 실린다',
        all(k in net_si([mid])[0]['A_components'] for k in
            ('cap_conflict', 'A_lower_um2', 'A_upper_um2', 'V_overlap_legacy_um3',
             'V_lens_exact_um3', 'A_volume_exact_um2')))
    #  (e) 1 m 구 픽스처에서는 volume 이 **절대** 안 결속한다 — 위 경고의 실증
    c5 = _l1_counters(); [_l1_tally(c5, e_) for e_ in net([{'id1': 1, 'id2': 2,
                                                            'contact_area': 0.0,
                                                            'delta': 0.05 * R / 2.0}])]
    chk('⑩e 대조: 1 m 구 픽스처는 volume 이 안 결속한다 (규모 없는 검사는 공허하다)',
        c5['n_exact_avail'] == 1 and c5['n_a_eff_changed'] == 0)

    # ── ⑪ flat 폴더 발견 + 진단 (2026-09-13 실사고: `--webapp ~/lhs_local` 이 rc=2) ─
    fdir = Path(_tf.mkdtemp())
    case = fdir / 'lhs00_900'
    case.mkdir()
    (case / 'atoms.csv').write_text('id,type,radius,x,y,z\n1,1,0.5,0,0,0\n')
    (case / 'contacts.csv').write_text('id1,id2,contact_area,delta\n')
    (case / 'meta.json').write_text('{}')
    (fdir / 'not_a_case').mkdir()
    saved = _SED.WEBAPP
    try:
        _SED.WEBAPP = fdir
        chk('⑪a results/·archive/ 없는 폴더: 기본 발견은 0개', _SED.discover_cases() == [])
        chk('⑪b 같은 폴더를 flat 으로 보면 케이스 1개', [d.name for d in _SED.discover_cases(flat=True)] == ['lhs00_900'])
        rep = _SED.case_layout_report(fdir)
        chk('⑪c 진단이 실제 하위 폴더와 필요한 파일을 찍는다',
            'lhs00_900/' in rep and 'not_a_case/' in rep and 'atoms.csv + contacts.csv' in rep)
    finally:
        _SED.WEBAPP = saved

    # ── ⑫ 원본 덤프 경로 == CSV 경로 (같은 자료, 두 형식) · scale 불변 · expect-csv 판별력 ─
    #    2026-09-13 실사고: `~/lhs_local` 은 post_*/ 원본 덤프만 있고 CSV 층이 없었다.
    rdir = Path(_tf.mkdtemp())
    #  (i) 원본 덤프 케이스  rdir/lhs00_901/post_lhs00_901/{atom,contact}_100.liggghts + 덱
    rc_ = rdir / 'lhs00_901'; pdir = rc_ / 'post_lhs00_901'; pdir.mkdir(parents=True)
    (rc_ / 'input_lhs00_901.liggghts').write_text(
        '# lhs00_901: mono_AM_S (2-type) | LHS design\n'
        'variable r_AM equal 0.0005\nvariable r_SE equal 0.0005\n'
        'fix m1 all property/global youngsModulus peratomtype 1.4e8 0.135e7\n'
        'fix pts1 all particletemplate/sphere 15485863 atom_type 1 density constant 4800 '
        'radius constant ${r_AM}\n'
        'fix pts2 all particletemplate/sphere 32452843 atom_type 2 density constant 2000 '
        'radius constant ${r_SE}\n')
    #  세 입자: AM(1) · SE(2) · SE(3).  접촉 1–2 (깊음, geom 결속 → 삭제) · 2–3 (얕음)
    (pdir / 'atom_100.liggghts').write_text(
        'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ATOMS\n3\n'
        'ITEM: BOX BOUNDS pp pp ff\n0 1\n0 1\n0 1\n'
        'ITEM: ATOMS id type radius x y z\n'
        '1 1 0.0005 0 0 0.0005\n2 2 0.0005 0.0008 0 0.0005\n3 2 0.0005 0.0017995 0 0.0005\n')
    def _crow(i1, i2, area, dlt):
        v = ['0'] * 26
        v[6], v[7], v[21], v[22] = str(i1), str(i2), repr(area), repr(dlt)
        return ' '.join(v)
    (pdir / 'contact_100.liggghts').write_text(
        'ITEM: TIMESTEP\n100\nITEM: NUMBER OF ENTRIES\n2\n'
        'ITEM: BOX BOUNDS pp pp ff\n0 1\n0 1\n0 1\n'
        'ITEM: ENTRIES ' + ' '.join(f'c_cpl[{k}]' for k in range(1, 27)) + '\n'
        + _crow(1, 2, 0.998 * math.pi * 0.0005 ** 2, 0.0002) + '\n'
        + _crow(2, 3, 1e-9, 5e-7) + '\n')
    #  (ii) 같은 자료를 CSV 층으로  rdir_csv/lhs00_901/{atoms,contacts}.csv + meta.json + 덱
    cdir = Path(_tf.mkdtemp()); cc = cdir / 'lhs00_901'; cc.mkdir()
    (cc / 'atoms.csv').write_text('id,type,radius,x,y,z\n1,1,0.0005,0,0,0.0005\n'
                                  '2,2,0.0005,0.0008,0,0.0005\n3,2,0.0005,0.0017995,0,0.0005\n')
    (cc / 'contacts.csv').write_text('id1,id2,contact_area,delta\n'
                                     f'1,2,{0.998 * math.pi * 0.0005 ** 2!r},0.0002\n2,3,1e-09,5e-07\n')
    (cc / 'meta.json').write_text('{"scale": 1000}')
    (cc / 'input_lhs00_901.liggghts').write_text((rc_ / 'input_lhs00_901.liggghts').read_text())

    A_r = load_case_any(rc_); A_c = load_case_any(cc)
    chk('⑫a 원본 덤프 경로와 CSV 경로가 **같은 atoms·contacts** 를 낸다',
        A_r[5] == 'raw' and A_c[5] == 'csv' and A_r[0] == A_c[0] and A_r[4] == A_c[4]
        and A_r[2] == A_c[2] == 1000.0,
        f'raw {len(A_r[0])} atoms/{len(A_r[4])} contacts · csv {len(A_c[0])}/{len(A_c[4])}')
    chk('⑫a′ 원본 덤프 발견: post_*/ 를 가진 케이스만 (CSV 층 없는 폴더)',
        [d.name for d in discover_raw_cases(rdir)] == ['lhs00_901']
        and discover_raw_cases(cdir) == [])
    r_raw = audit_case(rc_, channels=('ionic', 'thermal'), deck_dir=str(rdir))
    r_csv = audit_case(cc, channels=('ionic', 'thermal'), deck_dir=str(cdir))
    _skip = ('source', 'deck', 'atom_step', 'contact_step')     # 경로별로 당연히 다른 메타 열
    same = {k: v for k, v in r_raw.items() if k not in _skip} == \
           {k: v for k, v in r_csv.items() if k not in _skip}
    chk('⑫b 두 경로의 census 행이 동일 (source·deck 제외) — 삭제·L1 집계 포함', same,
        f"thermal 삭제 {r_raw.get('thermal_n_deleted')}/{r_raw.get('thermal_n_edges')} · "
        f"cap_conflict {r_raw.get('l1_n_cap_conflict')}")
    chk('⑫b′ 그 픽스처에 판별력이 있다 (삭제 1 · 비삭제 1)',
        r_raw.get('thermal_n_edges') == 2 and r_raw.get('thermal_n_deleted') == 1)
    #  (iii) scale 불변 — 같은 자료를 1000 과 1e6 으로 풀어도 집계가 같다
    def _counts(scale_):
        atoms_, _tm, _sc, _m, cts, _src = load_case_any(rc_)
        tm = {1: 'AM', 2: 'SE'}
        n = _NC.build_network(atoms_, cts, set(tm), scale_, _SED.estimate_plate_z(atoms_),
                              box_x=1e3, box_y=1e3, mode='thermal', type_map=tm,
                              contact_mode='physics')
        es = n['edges'] if isinstance(n, dict) else n[1]
        c = _l1_counters(); [_l1_tally(c, e_) for e_ in es]
        return sum(1 for e_ in es if e_['R_constriction'] == 0.0), c
    chk('⑫c 집계는 scale 에 불변 (1000 ↔ 1e6: 삭제 수 · L1 집계 동일)',
        _counts(1000.0) == _counts(1e6), f'{_counts(1000.0)}')
    #  (iv) expect-csv 판별력 — 한 숫자를 바꾸면 반드시 잡힌다
    ecsv = rdir / 'expect.csv'
    with ecsv.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(r_csv.keys())); w.writeheader(); w.writerow(r_csv)
    mism, ncmp, _mi, _ex = compare_to_expect([r_raw], ecsv, ('ionic', 'thermal'))
    bad_row = dict(r_raw); bad_row['thermal_n_deleted'] = int(bad_row['thermal_n_deleted']) + 1
    mism2, _n2, _a, _b = compare_to_expect([bad_row], ecsv, ('ionic', 'thermal'))
    chk('⑫d expect-csv: 같으면 불일치 0 · 삭제 수 하나를 바꾸면 **반드시** 잡힌다',
        ncmp == 1 and mism == [] and len(mism2) == 1 and mism2[0][1] == 'thermal_n_deleted',
        f'{mism2}')

    # ── ⑬ P2-R2-08: 삭제 부류가 결속 라벨이 아니라 s_raw/s_clamped 로 갈린다 ────────
    #    r_SE .5 / r_AM 6 µm · scale 1000 · ligg 0 (Codex 경계: floor 시작 0.10233796 · s=1 시작
    #    0.10263268 · geom 시작 0.16291922).  δ=.1025 → floor_only · δ=.12 → clamp_zero (tabor 결속!)
    def net_pair(delta_um):
        sc = 1000.0
        atoms = {1: {'type': 3, 'radius': 0.5 / sc, 'x': 0.0, 'y': 0.0, 'z': 0.0},
                 2: {'type': 1, 'radius': 6.0 / sc, 'x': (6.5 - delta_um) / sc, 'y': 0.0, 'z': 0.0}}
        rows = [{'id1': 1, 'id2': 2, 'contact_area': 0.0, 'delta': delta_um / sc}]
        n = _NC.build_network(atoms, rows, {1, 3}, sc, 10.0, box_x=1e3, box_y=1e3,
                              mode='thermal', type_map={1: 'AM_P', 3: 'SE'}, contact_mode='physics')
        return (n['edges'] if isinstance(n, dict) else n[1])[0]
    e_f = net_pair(0.1025); e_c = net_pair(0.12); e_p = net_pair(0.10)
    cf = _l1_counters(); _l1_tally(cf, e_f)
    cc = _l1_counters(); _l1_tally(cc, e_c)
    cp = _l1_counters(); _l1_tally(cp, e_p)
    chk('⑬a δ=.1025: Rc=0 · s<1 → floor_only (ψ ≤ 1e-4 가 모델의 양수를 지운다)',
        cf['n_rc0'] == 1 and cf['n_rc0_floor_only'] == 1 and cf['n_rc0_clamp_zero'] == 0,
        f"s_raw={_s_raw_clamped(e_f)[0]:.6f} binding={e_f['A_components']['binding']}")
    chk('⑬b δ=.12: **tabor 결속인데** s_raw > 1 → clamp_zero (Codex: 1.1244)',
        cc['n_rc0'] == 1 and cc['n_rc0_clamp_zero'] == 1 and cc['n_rc0_floor_only'] == 0
        and e_c['A_components']['binding'] == 'tabor' and _s_raw_clamped(e_c)[0] > 1.1,
        f"s_raw={_s_raw_clamped(e_c)[0]:.6f} binding={e_c['A_components']['binding']}")
    chk('⑬c 대조: δ=.10 은 Rc > 0 (어느 부류도 아님)', cp['n_rc0'] == 0 and e_p['R_constriction'] > 0)

    # ── ⑫e --match-steps: contact 의 마지막 step 과 같은 atom 을 고른다 (SELF-30) ───────
    (pdir / 'atom_105.liggghts').write_text((pdir / 'atom_100.liggghts').read_text())   # 더 늦은 atom 덤프
    global MATCH_STEPS
    d_def = _raw_dump_dir(rc_)
    MATCH_STEPS = True
    try:
        d_mat = _raw_dump_dir(rc_)
    finally:
        MATCH_STEPS = False
    chk('⑫e 기본은 각각 마지막(atom 105 · contact 100), --match-steps 는 같은 step(atom 100)',
        _step_of(d_def[1]) == 105 and _step_of(d_def[2]) == 100 and _step_of(d_mat[1]) == 100,
        f'기본 atom {_step_of(d_def[1])} / match atom {_step_of(d_mat[1])}')

    print('협착 삭제 census SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
