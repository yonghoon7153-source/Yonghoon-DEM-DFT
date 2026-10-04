#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""τ 결정 16 실행 2단계 ① — 라벨 묶음 (Codex 아님 · τ 적대 리뷰 셋 → 원장 `TAU-01` · `02` · `21` · `08` 라벨) · 웹앱 같은 묶음 (J20-l).

명명 규약 (CLAUDE.md ★★ τ 블록 · 1저자 비준 10-03): COMSOL Tortuosity 칸의 꼴 = **tau2** (= φ·σ₀/σ_full · tortuosity factor) — √ 값
(τ_Laplace,eff) 이 아니다.  배터리 Porous Electrode 노드는 식이 인쇄돼 있지 않다 = "강하게 시사" → tau2 에 "COMSOL 입력" 표지는 GUI Equation
캡처 뒤 (결정 5).  값은 하나도 바꾸지 않는다 — 표기 · 행 추가 · physics 빈칸뿐.

  A  케이스 τ 블록 (`transform_network_summary_4col` → `apply_paper_labels`) — 두 경로 (Step 4 · Step 4b) 가 같은 τ 행을 낸다
     A1 τ 머리 · √ 행 (원 라벨 · 논문 라벨) 에 'COMSOL' · 'EIS' 없음 (TAU-01)
     A2 tau2 행 = φ·σ₀/σ_full (H · P) · σ₀ = 그 런의 σ_grain (`_sigma_grain_context`)
     A3 √ 행 = √tau2 (같은 σ₀ · 같은 반올림 전 값)
     A4 physics σ 가 없으면 physics 칸 '—' (TAU-21) — tau2 · √ · 비율 행 모두 (옛 판 = Hertz 값을 조용히 복사)
     A5 비율 행 이름 = "협착 배수 아님" (TAU-08 라벨 · CLAUDE.md τ 블록) — "Constriction overhead" 없음
  B  번역 · 순서 표 — 새 원 라벨 셋에 논문 라벨이 있고 옛 원 라벨 키는 없다 · 정렬 표 `_CANONICAL_ROW_ORDER` 에 tau2 행이 √ 행 바로 앞
  C  single.html 툴팁 — √ 행 툴팁에 COMSOL · EIS 없음 · "1.4%" · "parameter-free" · "일치" 철회 (TAU-02) · tau2 툴팁 = '강하게 시사' · 'GUI' ·
     σ₀ 짝 · 별칭 표 (PAPER_TO_ORIG) 가 새 논문 라벨 → 새 원 라벨
  D  쉬운 툴팁 `__tau_lap_eff` — "COMSOL/EIS에 넣는" 없음 · tau2 언급
  E  등급 엔진 — √ 축 meaning 에 'COMSOL/EIS input' 없음 · 낡은 "same formula as webapp/app.py:2026" 주석 없음
  F  COMSOL 2D 내보내기 — tau2 행 = φ·σ_grain/σ_full (같은 σ_full) · √ 행 설명에 COMSOL/EIS 입력 주장 없음 · README 검산식 σ_i = φ·σ_grain/tau2
  G  LHS 열 사전 — 벽 τ 문구: tau2 · "COMSOL/EIS 입력 τ 는 τ_Laplace" 없음 · 생성기 selftest ㉓b 가 같은 단언
  H  전달본 정오표 — 배포 v1 · v1.1 폴더에 ERRATA (TSV 는 커밋 바이트 그대로)
  I  기타 자리 — plot_section7 축 이름 · GRADING_STORY · bruggeman 문서 · stage4 PyBaMM 주석

  python3 webapp/test_tau_labels.py
"""
import hashlib
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


NEW_HDR = '── τ 비교 (Dijkstra vs Laplace · tau2 = tortuosity factor) ──'
NEW_TAU2 = 'tau2 = φ·σ₀/σ_full (tortuosity factor · 협착 포함)'
NEW_SQRT = 'τ_Lap,eff = √tau2 (Laplace · 협착 포함)'
NEW_RATIO = 'τ_Lap,eff / τ_Dij (정의가 다른 두 τ 의 비)'
OLD_SQRT = 'τ_Lap_eff ⭐ (Laplace, GB 포함 — COMSOL/EIS)'
OLD_HDR = '── τ 비교 (Dijkstra vs Laplace, COMSOL input = τ_Lap_eff) ──'

# ── A  케이스 τ 블록 ─────────────────────────────────────────────────────────
print('A  케이스 τ 블록 (두 경로)')
import app as webapp   # noqa: E402

MET = {'phi_se': 0.30, 'sigma_full_mScm': 0.12, 'sigma_full_mScm_physics': 0.30, 'sigma_bulk_net_mScm': 0.50,
       'tortuosity_mean': 1.50, 'tortuosity_all_mean': 1.45}
SG, _note = webapp._sigma_grain_context(MET)


def _render(metrics, csv_net_section):
    data = [['Porosity(%)', 15.0], ['── 응력 ──', ''], ['Stress CV(%)', 40.0]]
    if csv_net_section:      # analyze_contacts 가 CSV 에 망 머리를 쓴 경우 → Step 4 건너뛰고 Step 4b 만
        data = [['Porosity(%)', 15.0], ['── Network Solver (Hertzian DEM-native) ──', ''],
                ['σ_ionic (mS/cm)', metrics['sigma_full_mScm']], ['── 응력 ──', ''], ['Stress CV(%)', 40.0]]
    tables = {'network_summary': {'columns': ['지표', '값'], 'data': [list(r) for r in data]}}
    webapp.transform_network_summary_4col(tables, metrics, {})
    raw = [list(r) for r in tables['network_summary']['data']]
    webapp.apply_paper_labels(tables)
    return raw, tables['network_summary']['data']


def _row(rows, label):
    return next((r for r in rows if isinstance(r, list) and r and str(r[0]).strip() == label), None)


def _num(x):
    try:
        return float(str(x).replace('×', ''))
    except (TypeError, ValueError):
        return None


for path_name, csvsec in (('Step 4', False), ('Step 4b', True)):
    raw, paper = _render(dict(MET), csvsec)
    hdr = [r for r in raw if isinstance(r[0], str) and r[0].startswith('── τ')]
    chk(f'A1a [{path_name}] τ 머리 하나 · 새 이름', len(hdr) == 1 and hdr[0][0] == NEW_HDR, repr(hdr))
    tau_rows_raw = [r for r in raw if isinstance(r[0], str) and ('τ_Lap' in r[0] or r[0].startswith('tau2') or r[0].startswith('── τ'))]
    tau_rows_pap = [paper[i] for i, r in enumerate(raw) if r in tau_rows_raw]
    bad = [r[0] for r in tau_rows_raw + tau_rows_pap if ('COMSOL' in str(r[0]) or 'EIS' in str(r[0])) and not str(r[0]).startswith('tau2')]
    chk(f'A1b [{path_name}] √ 행 · 머리 (원 · 논문 라벨) 에 COMSOL · EIS 없음 (TAU-01)', not bad, repr(bad))
    t2 = _row(raw, NEW_TAU2)
    want_h, want_p = MET['phi_se'] * SG / MET['sigma_full_mScm'], MET['phi_se'] * SG / MET['sigma_full_mScm_physics']
    chk(f'A2 [{path_name}] tau2 행 = φ·σ₀/σ_full (H · P)',
        t2 is not None and abs(_num(t2[1]) - round(want_h, 3)) < 1e-9 and abs(_num(t2[2]) - round(want_p, 3)) < 1e-9, repr(t2))
    sq = _row(raw, NEW_SQRT)
    chk(f'A3 [{path_name}] √ 행 = √tau2 (같은 σ₀)',
        sq is not None and abs(_num(sq[1]) - round(math.sqrt(want_h), 2)) < 1e-9
        and abs(_num(sq[2]) - round(math.sqrt(want_p), 2)) < 1e-9, repr(sq))
    rr = _row(raw, NEW_RATIO)
    chk(f'A5 [{path_name}] 비율 행 = "정의가 다른 두 τ 의 비" · 옛 이름 · "Constriction overhead" 없음',
        rr is not None and not any('Constriction overhead' in str(r[0]) for r in paper)
        and _row(raw, 'τ_Lap_eff / τ_Dij') is None, repr(rr))
    #  A4 — physics σ 없음
    m4 = dict(MET); m4.pop('sigma_full_mScm_physics')
    raw4, _ = _render(m4, csvsec)
    t24, sq4, rr4 = _row(raw4, NEW_TAU2), _row(raw4, NEW_SQRT), _row(raw4, NEW_RATIO)
    chk(f'A4 [{path_name}] physics σ 없음 → tau2 · √ · 비율 행의 physics 칸 = "—" (TAU-21 · 옛 판 = Hertz 값 복사)',
        all(r is not None and r[2] == '—' and r[1] not in ('—', '', None) for r in (t24, sq4, rr4)),
        repr((t24, sq4, rr4)))

# ── B  번역 · 순서 표 ─────────────────────────────────────────────────────────
print('B  번역 · 순서 표')
PL, PS = webapp._PAPER_LABEL_MAP, webapp._PAPER_SECTION_MAP
chk('B1 새 원 라벨 셋 (tau2 · √ · 비율) 에 논문 라벨 · 머리 번역 있음',
    all(k in PL for k in (NEW_TAU2, NEW_SQRT, NEW_RATIO)) and NEW_HDR in PS)
chk('B2 √ · 비율 · 머리 번역에 COMSOL · EIS 없음',
    all('COMSOL' not in PL.get(k, '') and 'EIS' not in PL.get(k, '') for k in (NEW_SQRT, NEW_RATIO))
    and 'COMSOL' not in PS.get(NEW_HDR, '') and 'EIS' not in PS.get(NEW_HDR, ''))
chk('B3 옛 원 라벨 키 (√ · 머리 · 옛 비율) 없음 — 화면에서 다시 나타날 길이 없다',
    OLD_SQRT not in PL and OLD_HDR not in PS and 'τ_Lap_eff / τ_Dij' not in PL)
SRC = _read('webapp/app.py')
_ci = SRC.find('_CANONICAL_ROW_ORDER = [')
canon = SRC[_ci:SRC.find(']', SRC.find('Electronic Active AM (%)', _ci))] if _ci >= 0 else ''
chk('B4 정렬 표: tau2 행이 √ 행 바로 앞 · 옛 √ 라벨 없음',
    (f"'{NEW_TAU2}',\n" in canon and canon.find(NEW_TAU2) < canon.find(NEW_SQRT) and OLD_SQRT not in canon), '정렬 표 확인')

# ── C  single.html 툴팁 ────────────────────────────────────────────────────────
print('C  single.html 툴팁 · 별칭')
HTML = _read('webapp/templates/single.html')


def _tip(key):
    i = HTML.find(f"  '{key}': {{")
    if i < 0:
        return ''
    j = HTML.find("\n  },", i)
    return HTML[i:j] if j > 0 else HTML[i:]


tsq, tt2, tdij, tgeom, trat = _tip(NEW_SQRT), _tip(NEW_TAU2), _tip('τ_Dij (Dijkstra, 기하만)'), _tip('τ_Lap_geom (Laplace, GB 제외)'), _tip(NEW_RATIO)
chk('C1 √ 행 툴팁이 있고 COMSOL · EIS 낱말이 없다 (TAU-01)', bool(tsq) and 'COMSOL' not in tsq and 'EIS' not in tsq, tsq[:200])
chk('C2 "1.4%" · "parameter-free" · "external validation" · "일치" 철회 — 수치 없이 (TAU-02 · 결정 8)',
    all(s not in HTML for s in ('1.4% 오차', 'parameter-free external validation', '2.07 (42 vol% CAM)')))
chk('C3 tau2 툴팁 = tortuosity factor · σ₀ 짝 · "강하게 시사" · GUI Equation 확인 전 한정어',
    bool(tt2) and 'tortuosity factor' in tt2 and '강하게 시사' in tt2 and 'GUI' in tt2 and 'σ₀' in tt2, tt2[:200])
chk('C4 Dijkstra · Laplace,bulk · 비율 툴팁에 "COMSOL 입력은 … τ_Lap_eff" 류 안내 없음',
    all(('τ_Lap_eff' not in t or 'COMSOL' not in t) for t in (tdij, tgeom, trat)) and bool(trat))
_ai = HTML.find('const PAPER_TO_ORIG = {')            # 논문 라벨 → 원 라벨 (툴팁 조회 — app.py apply_paper_labels docstring 의 "LABEL_ALIASES")
alias = HTML[_ai:HTML.find('\n};', _ai)] if _ai >= 0 else ''
chk('C5 별칭 표 (PAPER_TO_ORIG): 새 논문 라벨 → 새 원 라벨 (√ · tau2 · 비율) · 옛 √ 키 없음',
    all(f"'{PL.get(k, '@@')}':" in alias and f"'{k}'" in alias for k in (NEW_SQRT, NEW_TAU2, NEW_RATIO))
    and OLD_SQRT not in alias, '별칭 확인')

# ── D  쉬운 툴팁 ──────────────────────────────────────────────────────────────
print('D  쉬운 툴팁')
m = re.search(r"'__tau_lap_eff': '([^']*)'\s*\n\s*'([^']*)'", SRC)
easy = (m.group(1) + m.group(2)) if m else ''
chk('D1 __tau_lap_eff 쉬운 말 — "COMSOL/EIS에 넣는" 없음 · 입력 칸은 제곱 (tau2) 이라고 말한다',
    bool(easy) and 'COMSOL/EIS에 넣는' not in easy and 'tau2' in easy, easy[:160])

# ── E  등급 엔진 ──────────────────────────────────────────────────────────────
print('E  등급 엔진')
import grade_engine as GE   # noqa: E402
ax = next((a for a in GE.AXES if a.get('key') == '__tau_lap_eff'), None) if hasattr(GE, 'AXES') else None
if ax is None:
    for _nm in dir(GE):
        _v = getattr(GE, _nm)
        if isinstance(_v, list) and _v and isinstance(_v[0], dict) and 'key' in _v[0]:
            ax = next((a for a in _v if a.get('key') == '__tau_lap_eff'), None) or ax
GSRC = _read('scripts/grade_engine.py')
chk('E1 √ 축 meaning · label 에 "COMSOL/EIS input" 없음 · tau2 언급',
    ax is not None and 'COMSOL/EIS' not in (ax.get('meaning', '') + ax.get('label', '')) and 'tau2' in ax.get('meaning', ''),
    repr(ax and ax.get('meaning', '')[:120]))
chk('E2 낡은 주석 "same formula as webapp/app.py:2026" · "(COMSOL/EIS input)" 없음',
    'same formula as webapp/app.py:2026' not in GSRC and '(COMSOL/EIS input)' not in GSRC)

# ── F  COMSOL 2D 내보내기 ─────────────────────────────────────────────────────
print('F  COMSOL 2D 내보내기')
import export_comsol_2d as EC   # noqa: E402
with tempfile.TemporaryDirectory() as td:
    cid = 'caseX'
    d = Path(td) / 'webapp' / 'results' / cid
    d.mkdir(parents=True)
    fm = {'phi_se': 0.30, 'sigma_full_mScm_physics': 0.25, 'sigma_full_mScm': 0.12, 'sigma_bulk_net_mScm': 0.5, 'thickness_um': 80.0}
    (d / 'full_metrics.json').write_text(__import__('json').dumps(fm))
    _old_root = EC.ROOT
    try:
        EC.ROOT = Path(td)
        rows = EC.numerical_parameters(Path(td) / cid, {'phase_fracs': {'SE': 30.0, 'void': 15.0}, 'coverage_2d_pct': 50.0})
    except Exception as e:   # noqa: BLE001
        rows = []
        print('    numerical_parameters 실패:', type(e).__name__, e)
    finally:
        EC.ROOT = _old_root
byname = {r['parameter']: r for r in rows}
t2r, sqr = byname.get('tau2'), byname.get('tau_Laplace_eff')
_w = 0.30 * EC.SIGMA_GRAIN_MS / 0.25
chk('F1 tau2 행 = φ·σ_grain/σ_full (같은 σ_full 선택 — physics) · 단위 1',
    t2r is not None and t2r.get('unit') == '1' and float(t2r['value']) == round(_w, 6), repr(t2r))   # 내보내기는 소수 6 자리
chk('F2 √ 행 = √tau2 · 입력 칸 제안 "—" · 설명에 COMSOL · EIS 입력 주장 없음',
    sqr is not None and float(sqr['value']) == round(math.sqrt(_w), 6) and sqr.get('comsol_name') == '—'
    and not any(s in str(sqr) for s in ('COMSOL/EIS', 'COMSOL / EIS', 'EIS input')), repr(sqr))
ESRC = _read('scripts/export_comsol_2d.py')
chk('F3 README 검산식 = σ_i = φ·σ_grain/tau2 · 옛 "σ_grain / (φ·tau_eff²)" 없음',
    'σ_grain / (φ·tau_eff²)' not in ESRC and 'σ_i = φ·σ_grain/tau2' in ESRC)

# ── G  LHS 열 사전 ────────────────────────────────────────────────────────────
print('G  LHS 열 사전')
import lhs_design_dataset as LDD   # noqa: E402
wm = next((t[2] for t in LDD.HANDOVER_TAU_WALL if t[0] == 'tortuosity_SE_wall'), '')
chk('G1 벽 τ 문구: tau2 (= φ_SE·σ₀/σ_full) · "COMSOL/EIS 입력 τ 는 τ_Laplace" 없음',
    'tau2' in wm and 'COMSOL/EIS 입력 τ 는 τ_Laplace' not in wm and '기하 최단경로' in wm, wm[-260:])
LSRC = _read('scripts/lhs_design_dataset.py')
_b = LSRC[LSRC.find("chk('㉓b"):LSRC.find("chk('㉓c")]
chk('G2 생성기 selftest ㉓b 가 새 단언 (tau2 있음 · 옛 문구 없음) 을 강제한다', "'tau2' in _tm" in _b and 'COMSOL/EIS 입력 τ 는 τ_Laplace' in _b, _b[:200])

# ── H  전달본 정오표 ──────────────────────────────────────────────────────────
print('H  전달본 정오표')
REL = ['docs/data/lhs_release_20261001', 'docs/data/lhs_release_20261001_v11']
for rd in REL:
    er = sorted(p for p in os.listdir(os.path.join(ROOT, rd)) if p.startswith('ERRATA'))
    txt = _read(os.path.join(rd, er[0])) if er else ''
    chk(f'H1 {os.path.basename(rd)} 에 ERRATA — tau2 · 값 불변 · √ 값은 입력 칸 값이 아님',
        bool(txt) and 'tau2' in txt and '값' in txt and '불변' in txt, (er, txt[:120]))
    for tsv in sorted(p for p in os.listdir(os.path.join(ROOT, rd)) if p.endswith('_columns.tsv')):
        rel = os.path.join(rd, tsv)
        try:
            head = subprocess.run(['git', '-C', ROOT, 'show', f'HEAD:{rel}'], capture_output=True, check=True).stdout
            same = hashlib.sha256(head).hexdigest() == hashlib.sha256(open(os.path.join(ROOT, rel), 'rb').read()).hexdigest()
        except Exception as e:   # noqa: BLE001
            same, head = False, str(e)
        chk(f'H2 {tsv} = 커밋 바이트 그대로 (전달본은 고치지 않는다)', same)

# ── I  기타 자리 ──────────────────────────────────────────────────────────────
print('I  기타 자리')
chk('I1 plot_section7 축 이름에 COMSOL/EIS 없음', 'COMSOL/EIS' not in _read('scripts/plot_section7_design_rules.py'))
chk('I2 GRADING_STORY √ 행에 COMSOL/EIS input 없음', '| τ_Laplace,eff | 1.0 | COMSOL/EIS input |' not in _read('docs/GRADING_STORY.md'))
chk('I3 bruggeman 문서 √ 행에 "COMSOL · EIS 입력" 없음', 'COMSOL · EIS 입력' not in _read('docs/bruggeman_tortuosity_network_20261002.md'))
chk('I4 stage4 PyBaMM 주석 — tortuosity factor 칸 = tau2 (√ 값 아님)',
    '# ← τ_Laplace,eff' not in _read('docs/stage4_electrochem_research.md'))

print(f'\n{_ok} PASS · {len(_fail)} FAIL')
if _fail:
    for n in _fail:
        print('  -', n)
    sys.exit(1)
