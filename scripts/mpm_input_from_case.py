#!/usr/bin/env python3
"""DEM case → MPM input package (the webapp '[MPM input 변환]' button calls this).

From a webapp case's results dir (atoms.csv + full_metrics.json) it writes, into
<out>/ , the ready-to-run MPM input:
  • am_scaffold.csv  (type,x,y,z,r — AM_P=1/AM_S=2, the fixed skeleton)
  • se_scaffold.csv  (type,x,y,z,r — SE=3, the real seed positions)
  • run_mpm.sh       (mpm3d_compaction --se-dump … + mpm_webapp_payload …, with the
                      case's DEM porosity wired into --target-porosity)
  • mpm_input.json   (provenance: case id, n_AM, n_SE, DEM porosity/thickness)
Run run_mpm.sh on a GPU box; it produces mpm_metrics.json + mpm_payload.json, which
you upload back to the case (→ results/<case>/mpm_payload.json) for the viewer/compare.

  python3 scripts/mpm_input_from_case.py --results webapp/results/<case_id> --out /tmp/mpm_in
"""
import argparse
import csv
import json
import math
import os
import re


def expand_sched(seq, warn=print):
    """★Zive Loop 전개: {'k':'l','to':T,'n':N} = [T..직전] 블록을 총 N회 반복 ("Go to step T, N cycles").
    → [(원본 스텝 idx, cyc, step)] 평면 리스트.  킷 생성 시점에 평면화하므로 step4_only.sh 는 단순
    순차 유지(재개·부분실패 연속성 보존).

    ★cyc 출처 단일화: Loop 블록에 든 스텝의 cyc 는 **루프 회차(1..N)로만** 매긴다.  수동 n 을 함께
    쓰면 산출물명 step4_sched{i}n{cyc} 가 충돌해 결과가 조용히 덮어써지기 때문(예: 스텝0 n=3 +
    Loop×3 → n3 두 번; 2026-07-27 적대검증서 발견·수정).  무시된 수동 n 은 warn 으로 알린다.

    §F1: v1 은 각 런이 독립 초기상태 → 프로토콜 반복이지 상태-체이닝 열화 사이클이 아니다
    (그건 v2 chaining / R_int(N) 문헌투영 몫).  cyc 태그는 R_int(N) 축 라벨."""
    covered = set()
    for i, st in enumerate(seq):
        if st['k'] == 'l':
            covered |= {j for j in range(st['to'] - 1, i) if seq[j]['k'] != 'l'}
    ovr = sorted(j for j in covered if int(seq[j].get('n', 1) or 1) > 1)
    if ovr and warn:
        warn(f'  ⚠ Loop 블록 안 스텝 {[j + 1 for j in ovr]} 의 수동 cyc(n)은 무시 — '
             f'cyc 는 Loop 회차(1..N)로 자동 부여 (산출물명 충돌 방지)')
    flat = []
    for i, st in enumerate(seq):
        if st['k'] == 'l':
            blk = [(j, seq[j]) for j in range(st['to'] - 1, i) if seq[j]['k'] != 'l']
            for c in range(2, int(st['n']) + 1):             # 1회차 = 아래 원본 pass(cyc 1)
                flat += [(j, c, s) for j, s in blk]
        else:
            flat.append((i, 1 if i in covered else max(int(st.get('n', 1) or 1), 1), st))
    return flat


def _find_atom_dump(results_dir):
    """The FINAL-state raw LIGGGHTS atom dump (highest timestep) in the case dir, if present.
    The webapp keeps atom_<step>.liggghts (app.detect_mode reads it for type count); it carries the
    per-atom σ_zz virial (c_strs[3]) the analyzed atoms.csv strips → lets us get the REAL f_AM."""
    cands = []
    try:
        for f in os.listdir(results_dir):
            if f.startswith('atom') and f.endswith('.liggghts'):
                m = re.search(r'(\d+)', f)
                cands.append((int(m.group(1)) if m else -1, os.path.join(results_dir, f)))
    except OSError:
        return None
    return max(cands)[1] if cands else None      # highest timestep = the compacted 300-MPa state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', required=True, help='case results dir (has atoms.csv, full_metrics.json)')
    ap.add_argument('--case', default='', help='case id (provenance)')
    ap.add_argument('--out', required=True, help='output dir for the MPM input package')
    ap.add_argument('--type-map', default='', help='LIGGGHTS type map e.g. "1:AM_P,2:AM_S,3:SE" or '
                    '"1:AM_P,2:SE" — SE is NOT always type 3 (a no-AM_S case is type 2); parsed for SE vs AM')
    ap.add_argument('--max-points', type=float, default=90e6,
                    help='MPM point budget: auto-pick n_grid so est. points <= this (default 90M ~12GB, '
                         'fast frames).  The 209k-SE / 301M-pt case at n_grid 384 was too heavy and kept '
                         'dying — this caps it.  Raise for more SE resolution (slower/heavier).')
    ap.add_argument('--n-grid', type=int, default=0,
                    help='explicit lateral n_grid (0 = auto from RVE box + --max-points).')
    ap.add_argument('--add-recipe', default='', help='conductive-additive recipe baked into run_mpm.sh, e.g. '
                    '"AM:SE:VGCF=72:27:1" or "AM:SE:VGCF:PTFE=80:18:1:1" (Stage-1 carbon).  Empty = no carbon.')
    ap.add_argument('--add-l-cv', type=float, default=0.4, help='fibre length variation baked into run_mpm.sh.')
    ap.add_argument('--collector-rint', type=float, default=-1.0,
                    help='selected collector R_int (Ω·cm²; manuscript Fig6e cycled: bare-Al 110 / DBE 46 / '
                         'C-SUS primer 30 / ideal 0).  <0 = none — payload still reports every preset.')
    ap.add_argument('--collector-name', default='', help='collector preset label (metrics provenance)')
    ap.add_argument('--collector-scenario', default='', choices=('', 'sbe', 'dbe', 'csus', 'sus'),
                    help='anchors-CSV scenario key of the selected collector — run_mpm.sh의 payload 호출에 '
                         '전달돼 selected에 pristine 짝값(시간-일관 BOL)이 병기됨.  ⚠ 리뷰 CRITICAL 재발 '
                         '방지: webapp이 이 플래그를 보내므로 여기서 안 받으면 킷 생성이 argparse 500으로 죽음.')
    ap.add_argument('--step3-vox', type=float, default=0.4,
                    help='STEP3 σ-solve voxel size (µm) baked into run_mpm.sh.  0.4 default (σ 검증값); '
                         '0.25/0.2 = finer necks/SDCP-channels for the current-density FIELD figure '
                         '(dof∝1/vox³ — heavier CG).  Does NOT change porosity/thickness/coverage/econn.')
    ap.add_argument('--mixing', default='thinky', choices=['ballmill', 'thinky', 'handmix'],
                    help='Super P dispersion baked into run_mpm.sh (thinky = lit dry-process coating).')
    ap.add_argument('--no-dilate', action='store_true',
                    help='skip the VGCF-recipe --dilate-z auto-bake → regenerate the UN-dilated '
                         'bracket-floor zip (volume-fill/strut lower bound) without hand-editing run_mpm.sh.')
    ap.add_argument('--fibre-stiff', action='store_true',
                    help='force --fibre-stiff even for a NON-VGCF recipe.  For any VGCF recipe it is now '
                         'AUTO-baked into run_mpm.sh (VGCF as a LOAD-BEARING rigid strut = the physical model, '
                         'Cho-2024 direction), so you never need this flag for VGCF.  See mpm3d_compaction.py.')
    ap.add_argument('--step4-crates', default='',
                    help='STEP4-v2 방전 C-rate 목록 (쉼표, 예 "0.5,1").  비면 그리드 export까지만 '
                         '(step4_grid.npz는 항상 저장); 지정 시 run_mpm.sh가 payload 후 각 rate를 '
                         '순차로 step4_dyn.py에 태움 (한 rate 실패해도 다음 rate 계속).  '
                         'OCP 앵커(anchor_params/)는 GPU 박스에서 step4_pybamm_anchor --export-params로 '
                         '1회 생성해두면 됨 — 없으면 STEP4는 안내만 하고 SKIP.')
    ap.add_argument('--step4-charge', default='',
                    help='STEP4-v2 충전(CCCV) C-rate 목록 (쉼표) — CC 충전 → v_max 도달 시 CV 홀드 '
                         '(step4_dyn --charge --cv-hold).  방전 rate들 다음에 순차 실행.')
    ap.add_argument('--step4-grid-only', action='store_true',
                    help='STEP4 grid까지만 — step4_grid.npz 만들고 step4_dyn(v2 방전솔브)는 스킵 '
                         '(C-rate/충전/스케줄 선택 무시).  나중에 step4_dyn 을 직접 태워 재개 가능.')
    ap.add_argument('--step4-sched', default='',
                    help='★Zive-style 충방전 스케줄 (JSON) — 지정 시 crates/charge 대신 순서대로 실행. '
                         '형식 [{"k":"c|d","r":rate,"v":vlim,"i":icut,"n":cyc}]: k=c충전CCCV/d방전, '
                         'r=C-rate, v=컷오프(충전 v_max/방전 v_min), i=CV종지(충전만), n=사이클번호(R_int(N) 태그·메타). '
                         'charge-first, per-step 컷오프.  각 스텝=독립 STEP4 1런 (v1: chaining 없음).')
    ap.add_argument('--step4-vmin', type=float, default=3.0,
                    help='STEP4 방전 컷오프 전압 [V vs Li] (기본 3.0; 실험 2.5~4.25면 2.5).')
    ap.add_argument('--step4-vmax', type=float, default=4.5,
                    help='STEP4 충전 컷오프 전압 [V vs Li] (기본 4.5; 실험이면 4.25).')
    ap.add_argument('--step4-icut', type=float, default=0.05,
                    help='CCCV 충전의 CV-종지 전류 |I|/I_1C (기본 0.05; "1C→0.5C서 끝"이면 0.5).')
    ap.add_argument('--step4-solver-cap', type=float, default=0.0,
                    help='STEP4 e-망 σ-대비 상한(MPM_S4_CONTRAST_CAP 기본값, 0=OFF).  near-null 수렴정체 '
                         '완화용: 200 → CG iter ×5.2 실측(docs/step4_bottleneck_analysis_20260727.md) 이나 '
                         'σ_eff −7.8% → σ-메트릭 보고는 uncapped 런으로.  런타임 env 가 이 기본값을 override.')
    ap.add_argument('--step4-x0', type=float, default=None,
                    help='STEP4 방전창 시작 stoich(충전끝/저리튬) 오버라이드 — 기본 None=params_json(0.2638).')
    ap.add_argument('--step4-x100', type=float, default=0.9084,
                    help='STEP4 방전창 끝 stoich(방전끝/고리튬) — 기본 0.9084 = NMC811 vs-Li GITT 실측 max '
                         'stoich(ASSB 반쪽셀 실제 방전끝, --step4-vmin 2.5와 함께 전 SOC를 2.5V 단자까지).  '
                         'params_json(Chen 흑연셀-창 0.854=vs-Li 3.5V 조기종료)를 덮어씀 — Chen 창으로 '
                         '되돌리려면 --step4-x100 0.854.  x>0.854 OCP-shape는 Chen 소폭 외삽(끝점 0.9084는 '
                         'GITT 앵커) — 정밀 tail은 실측 GITT OCP splice 필요.  ⚠ 창 넓힘 → I_1C 재계산(전류 ~9%%↑).')
    ap.add_argument('--step4-r-int', type=float, default=None, dest='step4_r_int',
                    help='집전체 직렬 R_int [Ω·cm²] = ★풀셀 축 (기본 None = 전극-내부 R_int=0 유지). '
                         '측정 앵커 docs/data/rint_eis_anchors.csv: C-SUS pristine≈10/aged 30, '
                         'DBE 12/46, SBE 18/110 (pristine=panel-e 근사, aged=1000cyc@2C).  '
                         '⚠ pristine 값=BOL 전극과 시간-일관; aged 값은 "fresh 전극+aged 접촉" 민감도 '
                         '시나리오로 라벨(§6.1).  런타임 MPM_S4_RINT env로 override; 산출물명에 _rint<값> 태그.')
    # ── bimodal poly/SC 전기화학 분리 (STEP4 per-particle D_s/i0; 기본 미사용 = 공유물성) ──
    #    값은 문헌앵커만 (§F1, docs/ncm_sc_poly_electrochem_anchors.md) — 기본값 제공 안 함.
    ap.add_argument('--step4-ds-poly', type=float, default=None,
                    help='대립 poly AM(r≥split) D_s [m²/s] — --step4-ds-sc와 쌍으로만; env MPM_S4_DS_POLY')
    ap.add_argument('--step4-ds-sc', type=float, default=None,
                    help='소립 single-crystal AM D_s [m²/s] — --step4-ds-poly와 쌍; env MPM_S4_DS_SC')
    ap.add_argument('--step4-i0-poly', type=float, default=None,
                    help='poly AM i0_ref [A/m²] — --step4-i0-sc와 쌍; env MPM_S4_I0_POLY')
    ap.add_argument('--step4-i0-sc', type=float, default=None,
                    help='SC AM i0_ref [A/m²] — --step4-i0-poly와 쌍; env MPM_S4_I0_SC')
    ap.add_argument('--step4-am-split-um', type=float, default=3.5,
                    help='poly/SC 분류 반경 문턱 [µm] (r≥split=poly; 12:4µm(직경) 베드=반경 6:2 분리)')
    ap.add_argument('--step4-sc-poly-preset', action='store_true',
                    help='★문헌 프리셋 (2026-07-21 확정): docs/data/sc_poly_preset.csv 정본에서 '
                         'D_s poly/SC를 해석해 주입 (현행: poly 4e-15 Chen2020 / SC 3e-15 '
                         'Trevisanello 밴드 기하중앙; i0는 분리값 문헌 부재 확정 → 공유 유지).  '
                         'SDCP-150 계열 원장 방식 — 값이 갱신되면 CSV만 고치면 전 경로 반영.  '
                         '--step4-ds-poly 명시값과 동시 지정은 모호 → 거부')
    a = ap.parse_args()
    if a.step4_sc_poly_preset:
        if a.step4_ds_poly is not None or a.step4_i0_poly is not None:
            ap.error('--step4-sc-poly-preset과 명시 --step4-ds-poly/--step4-i0-poly 동시 지정 불가 '
                     '(어느 값이 이겼는지 모호 — 하나만)')
        _pre_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', 'docs', 'data', 'sc_poly_preset.csv')
        try:
            with open(_pre_csv, newline='') as _pf:
                _pre = {row['key']: row for row in csv.DictReader(_pf)}
            a.step4_ds_poly = float(_pre['d_s_poly']['value'])
            a.step4_ds_sc = float(_pre['d_s_sc']['value'])
            if float(_pre['am_split_um']['value']) > 0:
                a.step4_am_split_um = float(_pre['am_split_um']['value'])
            print(f"  ★ SC/poly 문헌 프리셋 (정본 {os.path.basename(_pre_csv)}): "
                  f"D_s poly={a.step4_ds_poly:g} / SC={a.step4_ds_sc:g} m²/s, "
                  f"split r≥{a.step4_am_split_um:g}µm; i0 분리 없음(부재 확정)")
        except (OSError, KeyError, ValueError) as _pe:
            ap.error(f'sc_poly_preset.csv 해석 실패 ({_pe!r}) — 정본 CSV 확인: {_pre_csv}')
    if a.step4_r_int is not None and a.step4_r_int < 0:
        # 음수는 step4_dyn이 조용히 R_int=0으로 clamp → 파일명/라벨(_rint-5)이 적용 안 된 직렬항을
        # 주장하게 됨(리뷰 CONFIRMED #2) — 생성 시점에 명시적으로 거부.
        ap.error('--step4-r-int must be >= 0 (Ω·cm²)')
    if (a.step4_ds_poly is None) != (a.step4_ds_sc is None):
        ap.error('--step4-ds-poly/--step4-ds-sc must be given together (반쪽 지정 금지)')
    if (a.step4_i0_poly is None) != (a.step4_i0_sc is None):
        ap.error('--step4-i0-poly/--step4-i0-sc must be given together')
    for _nm, _v in (('--step4-ds-poly', a.step4_ds_poly), ('--step4-ds-sc', a.step4_ds_sc),
                    ('--step4-i0-poly', a.step4_i0_poly), ('--step4-i0-sc', a.step4_i0_sc)):
        if _v is not None and _v <= 0:
            ap.error(f'{_nm} must be > 0')
    _es_split_req = a.step4_ds_poly is not None or a.step4_i0_poly is not None
    if _es_split_req and a.step4_am_split_um <= 0:
        # split≤0 은 전 입자 poly로 침묵 퇴화 — 파일명 _dsP..S.. 태그가 허위가 됨 (음수 rint와
        # 같은 '생성 시점 명시적 거부' 계열, 리뷰 #15).  베드-분리 검증은 atoms 파싱 뒤 아래에서.
        ap.error('--step4-am-split-um must be > 0 (µm 반경 문턱)')
    os.makedirs(a.out, exist_ok=True)

    def _parse_rates(s):                                     # STEP4 체크박스 (0.02–5C 화이트리스트)
        out = []
        for _tok in (s or '').split(','):
            _tok = _tok.strip()
            if _tok:
                try:
                    _v = float(_tok)
                    if 0.02 <= _v <= 5.0 and _v not in out:
                        out.append(_v)
                except ValueError:
                    pass
        return out
    s4_rates = _parse_rates(a.step4_crates)
    s4_chg = _parse_rates(a.step4_charge)
    # ★Zive-style 충방전 스케줄 (JSON) — 지정 시 crates/charge 대신 순서대로 실행
    s4_sched = None
    if a.step4_sched:
        try:
            _sc = json.loads(a.step4_sched)
        except Exception as e:
            ap.error(f'--step4-sched JSON 파싱 실패: {e}')
        if not isinstance(_sc, list) or not _sc:
            ap.error('--step4-sched는 비어있지 않은 리스트여야 함')
        s4_sched = []
        for i, st in enumerate(_sc):
            k = str(st.get('k', '')).lower()
            if k not in ('c', 'd', 'r', 'l'):
                ap.error(f'step {i}: k는 "c"(충전CCCV)/"d"(방전)/"r"(rest)/"l"(Loop) — got {st.get("k")!r}')
            if k == 'l':                                    # ★Loop (Zive "Go to step T, N cycles"):
                try:                                        #   스텝 to(1-base)로 이동해 [to..직전] 블록 총 n회
                    _to = int(st['to']); _ln = int(st.get('n', 2))
                except (KeyError, TypeError, ValueError):
                    ap.error(f'step {i}: Loop는 to(되돌아갈 스텝 번호 1-base)·n(총 반복) 필요')
                if not (1 <= _to <= i):
                    ap.error(f'step {i}: Loop to={_to} 는 1..{i}(자기 앞) 이어야 함')
                if _ln < 2:
                    ap.error(f'step {i}: Loop n≥2 (1회면 Loop 불필요)')
                if any(e['k'] == 'l' for e in s4_sched[_to - 1:i]):
                    ap.error(f'step {i}: 중첩 Loop 미지원 (v1)')
                if not any(e['k'] in ('c', 'd') for e in s4_sched[_to - 1:i]):
                    ap.error(f'step {i}: Loop 블록 [{_to}..{i}]에 충전/방전 스텝 없음')
                s4_sched.append({'k': 'l', 'to': _to, 'n': _ln})
                continue
            if k == 'r':                                    # rest(완화 I=0) — v1 독립런서 무동작(프로토콜 표시만)
                s4_sched.append({'k': 'r', 't': float(st.get('t', 1.0)), 'n': int(st.get('n', 1))})
                continue
            try:
                r = float(st['r'])
            except Exception:
                ap.error(f'step {i}: r(C-rate) 필요')
            if not (r > 0):
                ap.error(f'step {i}: rate>0 필요 (got {r})')
            entry = {'k': k, 'r': r,
                     'v': float(st.get('v', a.step4_vmax if k == 'c' else a.step4_vmin)),
                     'n': int(st.get('n', 1))}
            if k == 'c':
                entry['i'] = float(st.get('i', a.step4_icut))
            s4_sched.append(entry)

    atoms = os.path.join(a.results, 'atoms.csv')
    if not os.path.exists(atoms):
        raise SystemExit(f'no atoms.csv in {a.results}')
    fm = {}
    fmp = os.path.join(a.results, 'full_metrics.json')
    if os.path.exists(fmp):
        fm = json.load(open(fmp))
    ip = {}
    ipp = os.path.join(a.results, 'input_params.json')
    if os.path.exists(ipp):
        ip = json.load(open(ipp))
    # per-case pressing pressure → MPM --target-gpa (material E_SE/σ_y stay the CALIBRATED
    # MPM champion, NOT read from the DEM — frame[4]: MPM is calibrated independently).
    if ip.get('target_pressure_MPa') is not None:
        press_gpa = float(ip['target_pressure_MPa']) / 1000.0
    elif ip.get('target_press_sim') is not None:
        tp = float(ip['target_press_sim'])
        press_gpa = tp if tp < 10 else tp / 1000.0          # sim 0.30 = 0.30 GPa = 300 MPa
    else:
        press_gpa = 0.30
    press_gpa = round(press_gpa, 4)

    # which atom types are SE?  from the type_map — SE is NOT always type 3 (a no-AM_S case is
    # "1:AM_P,2:SE").  Fallback to the legacy type-3 convention if no map.
    se_types = set()
    for tok in (a.type_map or '').split(','):
        if ':' in tok:
            tid, lab = tok.split(':', 1)
            if 'SE' in lab.upper():
                try:
                    se_types.add(int(tid))
                except ValueError:
                    pass
    if not se_types:
        se_types = {3}

    # split atoms.csv (id,type,x,y,z,radius; LIGGGHTS box units): SE by the type map, AM = the rest
    am_raw, se_rows = [], []
    with open(atoms) as f:
        rd = csv.DictReader(f)
        cols = {c.lower(): c for c in rd.fieldnames}
        tk = cols.get('type'); xk = cols.get('x'); yk = cols.get('y'); zk = cols.get('z')
        rk = cols.get('radius') or cols.get('r')
        for row in rd:
            t = int(float(row[tk])); rec = [t, row[xk], row[yk], row[zk], row[rk]]
            (se_rows if t in se_types else am_raw).append(rec)
    if not se_rows:
        raise SystemExit(f'no SE atoms (se_types={sorted(se_types)}, type_map={a.type_map!r}) — '
                         f'check the type map / atom types in atoms.csv')

    # AM_P (large) vs AM_S (small) by RADIUS — the physical distinction (AM_P polycrystalline
    # ~6µm / AM_S single-crystal ~2µm), robust to the type-number convention.
    # ── 두 분류 경로 (사용자 확정 2026-07-22, 이종기술) ────────────────────────────────
    # [기본, 체크 OFF] mono-size → AM_P (2026-07-14, 3.18mAh_SDCP 관례): DEM 케이스가
    #   mono-AM을 "AM_S"로 표기해도 SDCP manuscript NCM은 다결정 → MPM/STEP3 재료 배정은
    #   AM_P(σ_P=5 mS/cm)가 의도된 값.  bimodal → 케이스-내 상대 크기 중앙점 분리.
    # [체크 ON, _es_split_req = poly/SC D_s 분리 프리셋/명시] AM_S/AM_P를 ★절대 크기 문턱★
    #   (--step4-am-split-um, 반경 µm)으로 판정 → σ_e 재료(STEP3)와 D_s(STEP4)를 함께 크기-분리.
    #   소립 단결정 r<split = AM_S(σ_S=10 mS/cm, GB無), 대립 다결정 r≥split = AM_P(σ_P=5).
    #   mono 4µm 단결정(이종기술 No.1/No.2) → 전부 AM_S; mono 대립 → 전부 AM_P; bimodal → 혼합.
    #   (기본 mono→AM_P의 SDCP 관례를 이 경로에서만 덮어씀 — 단결정 실험의 정직한 재료 배정.)
    am_rows = []
    _ds_scalar = None            # mono 베드 + poly/SC 분리 요청 → 단일 클래스 scalar D_s [m²/s]
    _ds_scalar_cls = None        # 'sc' | 'poly' (scalar D_s가 어느 클래스인지 — 라벨/태그용)
    if am_raw:
        radii = [float(r[4]) for r in am_raw]
        rmin, rmax = min(radii), max(radii)
        if _es_split_req:
            # ⚠ 반경은 LIGGGHTS box units — µm로 변환 후 절대 문턱과 비교 (규약: 1 LU = 1000µm,
            #   SE 0.0005 LU = 0.5µm; mpm3d_compaction um_box=1000/scl 과 동일).  변환 없이 raw LU를
            #   3.5와 비교하면 bimodal(0.002·0.006 LU)이 둘 다 <3.5 → 전부 AM_S 오분류.
            _UM_PER_LU = 1000.0
            split_r = a.step4_am_split_um                                  # µm 반경 문턱
            for rec in am_raw:
                rec[0] = 1 if float(rec[4]) * _UM_PER_LU >= split_r else 2  # 절대 문턱(µm): AM_P=1 / AM_S=2
                am_rows.append(rec)
            _n_po = sum(1 for r_ in am_rows if r_[0] == 1)
            _n_sc = len(am_rows) - _n_po
            # mono 베드(한 클래스만) → split 불가 → 그 클래스의 scalar D_s (분리 태그 허위 방지).
            #   σ_e 재료는 위 절대-문턱 분류로 이미 정직 배정됨 (mono-SC → 전부 AM_S=σ_S).
            if _n_po == 0 or _n_sc == 0:
                if a.step4_i0_poly is not None:
                    ap.error(f'--step4-i0-poly/sc 분리는 mono 베드(AM 반경 '
                             f'{rmin * _UM_PER_LU:.2f}–{rmax * _UM_PER_LU:.2f}µm, split {split_r:g}µm에서 '
                             f'전부 {"AM_S" if _n_po == 0 else "AM_P"})에 적용 불가 — '
                             f'i0 분리 빼거나 bimodal 케이스 사용')
                if a.step4_ds_poly is not None:
                    _ds_scalar = a.step4_ds_sc if _n_po == 0 else a.step4_ds_poly
                    _ds_scalar_cls = 'sc' if _n_po == 0 else 'poly'
        else:
            thr = (rmin * rmax) ** 0.5 if rmax / max(rmin, 1e-12) > 1.4 else -1.0
            for rec in am_raw:
                rec[0] = 1 if (thr < 0 or float(rec[4]) >= thr) else 2      # AM_P=1 / AM_S=2 by size
                am_rows.append(rec)

    def write_csv(path, rows, note):
        with open(path, 'w', newline='') as f:
            f.write(f'# type,x,y,z,r  # {note}\n')
            w = csv.writer(f)
            for r in rows:
                w.writerow([r[0], f'{float(r[1]):.6f}', f'{float(r[2]):.6f}',
                            f'{float(r[3]):.6f}', f'{float(r[4]):.6f}'])
    write_csv(os.path.join(a.out, 'am_scaffold.csv'), am_rows,
              f'AM scaffold (AM_P=1,AM_S=2) — case {a.case}')
    write_csv(os.path.join(a.out, 'se_scaffold.csv'), se_rows,
              f'SE seed positions (col 0 = original atom type; MPM uses x,y,z,r) — case {a.case}')

    # ── 취성 crack-void 스캐폴드 (DEM 초기압밀 Auerbach 파괴 → per-AM 심각도) ────────────────
    #   frame[5]: DEM = WHERE(어디 균열), MPM = 형태(SE가 열린 crack-void로 흘러듦).  am_scaffold 와 행-정렬.
    #   ★void 부피분율(frag 0.15 / pulv 0.35) = ASSUMED-FORM → run_mpm.sh 에서 MPM_FRACTURE=1 로 opt-in
    #   (기본 OFF = 생산 default bitwise-동일 유지, §F1).  CSV 는 항상 생성(데이터/검토용).
    _frac_note = ''
    try:
        import sys as _sys
        _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from dem_fracture_scaffold import build_fracture_scaffold, write_fracture_scaffold
        _cont = os.path.join(a.results, 'contacts.csv')
        _meta = os.path.join(a.results, 'meta.json')
        if os.path.exists(_cont):
            _amp = os.path.join(a.out, 'am_scaffold.csv')
            _atoms_p = os.path.join(a.results, 'atoms.csv')
            _sc, _rk, _fp, _st = build_fracture_scaffold(_atoms_p, _cont, _meta, _amp)
            if _st['r_med'] > 0 and _st['match_dist_max'] > 0.5 * _st['r_med']:
                _frac_note = (f'  ⚠ 취성 생략 — 위치매칭 최대 {_st["match_dist_max"]:.2g} > 0.5·r_med '
                              f'{_st["r_med"]:.2g} (am_scaffold↔atoms 불일치 가능)')
            else:
                write_fracture_scaffold(os.path.join(a.out, 'fracture_scaffold.csv'), _sc, _rk, _fp)
                _nfp = _st['n_frag'] + _st['n_pulv']
                _frac_note = (f'  fracture_scaffold.csv ({_st["n_frag"]} frag + {_st["n_pulv"]} pulv → '
                              f'crack-void; run_mpm.sh 에 MPM_FRACTURE=1 로 적용)' if _nfp else
                              '  fracture_scaffold.csv (frag/pulv 0 → crack-void near-null; 취성은 수송 f_intact만)')
        else:
            _frac_note = '  (contacts.csv 없음 → 취성 스캐폴드 생략; DEM contacts 있는 케이스에서만 생성)'
    except Exception as _e:                                    # 취성 실패가 킷 생성을 절대 막지 않음
        _frac_note = f'  ⚠ 취성 스캐폴드 생성 실패 ({type(_e).__name__}: {_e}) — 킷은 정상, 취성만 생략'

    poro = fm.get('porosity')
    tgt = round(float(poro) / 100.0, 4) if poro is not None else 0.16
    # PRODUCTION = pure scaffold + hold; NO injected conditional (FINAL LOGIC, 2026-06-27).
    # The wallP conditional — --am-load-frac (Love-Weber f_AM skeleton-spring) + --floor-porosity
    # (a DEM−5 HARD porosity clamp) — was a CORNER patch that stopped the SE-poor/mono-large
    # over-compression by CLAMPING porosity at DEM−margin.  But a porosity clamp MASKS the true
    # DEM↔MPM gap, and that gap IS the validity certificate (§13/§16: regime-gate, NOT a clamp).
    # Final logic: run the MPM PURE (SE bears the load → plastic void-fill).  In-envelope cases
    # reproduce experiment (real_14 15.93 ≈ DEM 15.6 ≈ FIB-SEM 9–19 %); the out-of-envelope corner
    # (SE-sub-functional + thin = not a manufacturable cell, §16-lit) HONESTLY over-compresses, and
    # the un-clamped |DEM − MPM| gap flags it (large gap → trust DEM, not the MPM number).  The
    # conditional + --se-am-drag/--am-jam survive as OPT-IN flags in mpm3d_compaction.py for
    # experiments; production never injects them.  (Dead-patch history: troubleshooting §15/§16 + git.)
    case = a.case or os.path.basename(a.results.rstrip('/'))
    # lateral RVE box (LIGGGHTS units) → MPM scl = WIDTH/lateral_box and adaptive n_grid.  Prefer
    # input_params box_x; else the atom lateral extent (periodic box ≈ max x,y).  Thick films are
    # TALLER than this lateral, so MPM auto-extends the z grid (non-cubic) to fit — see run script.
    box_x = ip.get('box_x') or ip.get('box_x_sim')
    if not box_x:
        allxy = [float(r[1]) for r in (am_rows + se_rows)] + [float(r[2]) for r in (am_rows + se_rows)]
        box_x = max(allxy) if allxy else 0.05
    box_x = round(float(box_x), 6)
    # adaptive lateral resolution: keep SE ≈ 3.5 cells (real_14 0.05→384) so the calibration
    # transfers; but CAP by a POINT BUDGET so big-SE cases stay GPU-tractable AND finish (the
    # 209k-SE case at n_grid 384 = 301M pts kept dying/crawling).  est. points = PPC·V_SE·(n/box)³.
    V_SE = sum((4.0 / 3.0) * math.pi * float(r[4]) ** 3 for r in se_rows)   # total SE volume (box³ units)
    PPC = 8                                                     # MPM particles per cell (2×2×2)
    n_design = int(round(384 * box_x / 0.05))                  # resolution-matched to real_14
    if a.n_grid > 0:
        n_grid_mpm = max(64, a.n_grid)                         # explicit override
    elif V_SE > 0:
        n_budget = int(box_x * (a.max_points / (PPC * V_SE)) ** (1.0 / 3.0))
        n_grid_mpm = max(128, min(384, n_design, n_budget))
    else:
        n_grid_mpm = max(128, min(384, n_design))
    est_pts = int(PPC * V_SE * (n_grid_mpm / box_x) ** 3) if V_SE > 0 else 0
    # per-case SE stiffness — physically-faithful mapping (CLAUDE.md CORRECTION 1):
    # the DEM E_eff softening (1.35 GPa × the case ratio) is the GRANULAR-REARRANGEMENT
    # proxy = the SHEAR part ONLY.  So scale the MPM shear modulus μ by the case ratio
    # while HOLDING the bulk modulus K at the real-LPSC champion value (K=25.5 GPa, what
    # ν=0.49 gives at E=1.53), then back out (E, ν) for the MPM.  Normal range (×0.5–×1.5)
    # ≈ proportional-E with ν≈0.49 (×1.0 → exactly E=1.53/ν=0.49); extreme softening keeps
    # K ≫ press → no volumetric over-crush (proportional-E would let K fall toward press).
    # MPM lame(): μ=E/(2(1+ν)), K=E/(3(1-2ν)) → E=9Kμ/(3K+μ), ν=(3K-2μ)/(2(3K+μ)).
    e_se_dem = fm.get('e_se_eff_gpa')
    E_STD_DEM, E_CHAMP, NU_CHAMP = 1.35, 1.53, 0.49
    K_CHAMP = E_CHAMP / (3.0 * (1.0 - 2.0 * NU_CHAMP))      # 25.5 GPa (real LPSC bulk)
    MU_CHAMP = E_CHAMP / (2.0 * (1.0 + NU_CHAMP))           # 0.513 GPa (soft shear proxy)
    se_ratio = float(e_se_dem) / E_STD_DEM if e_se_dem else 1.0
    mu_se_mpm = MU_CHAMP * se_ratio                         # shear scales with the granular proxy
    if e_se_dem:
        e_se_mpm = round(9.0 * K_CHAMP * mu_se_mpm / (3.0 * K_CHAMP + mu_se_mpm), 4)
        nu_se_mpm = round((3.0 * K_CHAMP - 2.0 * mu_se_mpm) /
                          (2.0 * (3.0 * K_CHAMP + mu_se_mpm)), 5)  # 5 dp: K stable near ν→0.5
    else:
        e_se_mpm, nu_se_mpm = E_CHAMP, NU_CHAMP
    prov = {'case': case, 'n_AM': len(am_rows), 'n_SE': len(se_rows),
            'dem_porosity_pct': poro, 'dem_thickness_um': fm.get('thickness_um'),
            'dem_coverage_AM_P_mean': fm.get('coverage_AM_P_mean'),
            'dem_coverage_AM_S_mean': fm.get('coverage_AM_S_mean'),
            'dem_e_se_eff_gpa': e_se_dem, 'se_ratio_vs_1p35': round(se_ratio, 4),
            'mpm_e_se_gpa': e_se_mpm, 'mpm_nu_se': nu_se_mpm,
            'mpm_K_se_gpa': round(K_CHAMP, 2), 'mpm_mu_se_gpa': round(mu_se_mpm, 4),
            'press_gpa': press_gpa, 'target_porosity': tgt,
            'lateral_box': box_x, 'mpm_n_grid': n_grid_mpm, 'mpm_est_points': est_pts,
            'step4_crates': s4_rates, 'step4_charge_crates': s4_chg,
            'step4_r_int_ohm_cm2': a.step4_r_int,
            'step4_am_electro_split': (
                None if a.step4_ds_poly is None and a.step4_i0_poly is None
                # mono 베드 → scalar D_s (분리 아님); σ_e 재료는 크기-분류로 배정됨.
                else {'mode': 'mono_scalar', 'class': _ds_scalar_cls, 'd_s': _ds_scalar,
                      'am_split_um': a.step4_am_split_um,
                      'sigma_e_am': ('AM_S=10mS/cm' if _ds_scalar_cls == 'sc' else 'AM_P=5mS/cm')}
                if _ds_scalar is not None
                else {'mode': 'bimodal_split', 'ds_poly': a.step4_ds_poly, 'ds_sc': a.step4_ds_sc,
                      'i0_poly': a.step4_i0_poly, 'i0_sc': a.step4_i0_sc,
                      'am_split_um': a.step4_am_split_um}),
            # 재료 크기-분류 경로: split 요청 시 절대 문턱, 아니면 SDCP 관례(mono→AM_P).
            'am_material_class_mode': ('size_absolute' if _es_split_req else 'sdcp_mono_amp')}
    json.dump(prov, open(os.path.join(a.out, 'mpm_input.json'), 'w'), indent=2)

    # Stage-1 carbon: append the additive flags to the compaction step if a recipe was given,
    # and carry the per-point phase into the payload (so the 도전재 3D viewer can colour the carbon)
    # A3 binder physics baked EXPLICITLY (non-monotonic PTFE cohesion: peak at --binder-opt-wt,
    # decays for over-application). These equal the mpm3d_compaction defaults, but writing them
    # makes the run self-documenting that A3 is applied. Pressure-regime propping (yield at
    # σ_y=0.05 GPa) is automatic from the PTFE material vs --target-gpa.
    # VGCF present → bake the SEM-consistent AM-position-dependent buckle morphology by default (the
    # electrode-faithful VGCF shape; fibre_rod_mpm_design §SOLUTION).  Volume/porosity-neutral, so it never
    # changes the porosity result; it just makes the seeded fibres wavy like real VGCF instead of straight.
    _buckle = '--fibre-buckle ' if 'VGCF' in a.add_recipe.upper() else ''
    # --fibre-stiff AUTO-baked for any VGCF recipe (like --fibre-buckle): real graphite VGCF (E~200 GPa,
    # σ_y ≫ 0.3 GPa press) is a LOAD-BEARING rigid strut that RESISTS compaction, NOT a passive void-
    # filler → this is the physical VGCF model (Cho-2024 conflicting-roles direction; see
    # docs/fibre_rod_mpm_design.md §COMPACTION-RESISTANCE).  So every VGCF run is strut by default (no
    # manual flag / sed needed); the --fibre-stiff CLI flag still force-enables it for a non-VGCF recipe.
    _stiff = '--fibre-stiff ' if ('VGCF' in a.add_recipe.upper() or a.fibre_stiff) else ''
    # --fibre-align AUTO for any FIBRE (VGCF or PTFE): press-induced IN-PLANE alignment.  λ_z = axial stretch
    # of the bed under the uniaxial compaction the fibres underwent WITH it = (1−ε_loose)/(1−ε_DEM),
    # ε_loose≈0.44 (random loose packing pre-press), ε_DEM = this case's compacted porosity → non-circular
    # (from the compaction ratio), morphology-faithful (real 300-MPa fibres tilt in-plane).  PTFE fibrils
    # tilt in-plane under the same uniaxial press as VGCF; SuperP (0D, no long axis) is correctly excluded.
    _eps_dem = (float(poro) / 100.0) if poro else 0.15
    _rc = a.add_recipe.upper()
    # --dilate-z AUTO for STIFF-fibre (VGCF) recipes: bed prop-open the frozen-AM MPM cannot produce
    # emergently (skeleton rearrangement = granular/DEM-class).  λ_dz = (1+φ_VGCF)·(1−ε_DEM)/(1−ε_real);
    # ε_real = ε_DEM + Δε_cho(w) interpolated from docs/data/vgcf_dilate_cho_calibrated.csv — the ONE
    # in-repo Cho-2024-anchored curve (dem_perturbation.py driver C: Balberg-percolation-gated,
    # A_cho=1.568; SUPERSEDES the first-cut linear 0.5pp/wt% which disagreed with it below 2wt% —
    # the curve is NET vs no-additive, negative below rod percolation where volume-fill dominates).
    # ⚠ anchor caveats carry over (campaign doc): Cho = 433 MPa·other composition, TWO points (0/2wt%)
    # → slope ±~50%; onset constant spans [0.7 Balberg … 5.4 Philipse]·D/L.  Soft additives (PTFE/
    # SuperP, σ_y<press) flow into pores instead of propping → EXCLUDED.  Thickness/porosity respond
    # BY CONSTRUCTION; coverage/network/SE-strain respond EMERGENTLY on the dilated bed (z-affine =
    # die-press global mode; local non-affine rearrangement stays DEM territory).  --no-dilate
    # regenerates the un-dilated bracket-floor zip (no sed needed).
    _dilate = ''; _dz = 1.0; _eps_real = _eps_dem
    _wts = {}
    if a.add_recipe:
        import sys as _sys                                              # robust regardless of caller cwd
        _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            import additives as _adds                                   # canonical recipe parser + DENS
            _parse, _awt, _DENS = _adds.parse_recipe, _adds.additive_wt, _adds.DENS
        except ImportError as _e:                                       # numpy-less env → verbatim inline
            print(f'⚠ additives import failed ({_e}) → inline parse/DENS copies (keep in sync w/ additives.py)')
            def _parse(s):                                              # = additives.parse_recipe verbatim
                keys, vals = s.split('=')
                keys = keys.split(':'); vals = [float(v) for v in vals.split(':')]
                return dict(zip(keys, vals))
            def _awt(wt):                                               # = additives.additive_wt verbatim
                return {k: float(wt[k]) for k in ('VGCF', 'SuperP', 'PTFE', 'SDCP') if wt.get(k, 0) > 0}
            _DENS = {'AM': 4.80, 'SE': 2.00, 'VGCF': 2.00}              # = additives.DENS subset
        try:
            _wts = _awt(_parse(a.add_recipe))                           # {'VGCF':1.0,...} — AM/SE ignored
        except Exception as _e:
            raise SystemExit(f'--add-recipe {a.add_recipe!r} unparseable ({_e}) — '
                             f"expected 'VGCF:PTFE=1:1' / 'PTFE=0.5' / 'AM:SE:VGCF=72:27:1'")
    _wv = float(_wts.get('VGCF', 0.0))
    if _wv > 0.0 and poro and not a.no_dilate:
        _wt_tot = sum(_wts.values())                                    # additive wt% only (AM/SE excluded)
        _r3 = lambda rows: sum(float(r[4]) ** 3 for r in rows)          # Σr³ ∝ volume (4π/3 cancels)
        _v_am, _v_se = _r3(am_rows), _r3(se_rows)
        _m_base = _v_am * _DENS['AM'] + _v_se * _DENS['SE']             # single-source densities (additives.DENS)
        _v_vgcf = (_m_base * (_wv / 100.0) / max(1.0 - _wt_tot / 100.0, 1e-6)) / _DENS['VGCF']
        _phi = _v_vgcf / max(_v_am + _v_se, 1e-12)                      # VGCF vol / base-solid vol
        _curve = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              'docs', 'data', 'vgcf_dilate_cho_calibrated.csv')
        _pts = []                                                       # (wt%, Δε_pp) net-vs-no-additive
        with open(_curve) as _f:
            for _row in csv.reader(_f):
                try:
                    _pts.append((float(_row[0]), float(_row[3])))
                except (ValueError, IndexError):
                    continue                                            # header/comment lines
        _pts.sort()
        _w = min(max(_wv, _pts[0][0]), _pts[-1][0])                     # clamp to the calibrated range
        _dpp = _pts[-1][1]
        for (_w0, _d0), (_w1, _d1) in zip(_pts, _pts[1:]):
            if _w0 <= _w <= _w1:
                _dpp = _d0 + (_d1 - _d0) * (_w - _w0) / max(_w1 - _w0, 1e-9)
                break
        _eps_real = min(max(_eps_dem + _dpp / 100.0, 0.01), 0.60)
        _dz = (1.0 + _phi) * (1.0 - _eps_dem) / max(1.0 - _eps_real, 1e-6)
        if not (1.0 <= _dz <= 1.35):                                    # sanity gate: a λ outside this is a
            print(f'⚠ dilate-z λ={_dz:.4f} outside [1.0,1.35] — clamped; check recipe/porosity inputs')
            _dz = min(max(_dz, 1.0), 1.35)                              # parse/input bug, not physics
        _dz = round(_dz, 4)
        _dilate = f'--dilate-z {_dz} ' if _dz > 1.0 else ''
    # --fibre-align AUTO for any FIBRE (VGCF or PTFE): press-induced IN-PLANE alignment.  λ_z = axial
    # stretch of the bed under the uniaxial compaction the fibres underwent WITH it = (1−ε_loose)/(1−ε),
    # ε_loose≈0.44.  ε = ε_real when dilation is baked (the dilated bed's own compaction endpoint —
    # keeps the two auto-flags on ONE porosity narrative), else the case ε_DEM.  PTFE fibrils tilt
    # in-plane under the same uniaxial press as VGCF; SuperP (0D, no long axis) is correctly excluded.
    _eps_align = _eps_real if _dilate else _eps_dem
    _lam_z = round(min(1.0, (1.0 - 0.44) / max(1.0 - _eps_align, 1e-6)), 3)
    _align = f'--fibre-align {_lam_z} ' if ('VGCF' in _rc or 'PTFE' in _rc) else ''
    # strut vs dilation: λ_dz already encodes the FULL Cho prop-open; the rigid strut is a partial
    # mechanistic model of the SAME mechanism (+0.75pp @4wt% on the frozen bed) → stacking them
    # double-counts.  Dilation SUPERSEDES the auto-strut; --fibre-stiff CLI still force-enables.
    if _dilate and not a.fibre_stiff:
        _stiff = ''
    # step-2 payload must live on the SAME frame as the dilated run: pass λ_dz through (AM + seed-SE
    # rebuilt dilated in the viz) and target the dilated ε_real — else voxelize pins the void back to
    # ε_DEM exactly and the viewer/coverage compare a dilated SE cloud against un-dilated AM spheres.
    tgt_pay = round(_eps_real, 4) if _dilate else tgt
    pay_dilate = f' --dilate-z {_dz}' if _dilate else ''
    add_flags = (f' \\\n  --add-recipe "{a.add_recipe}" --add-l-cv {a.add_l_cv} --mixing {a.mixing} '
                 f'--coh-ptfe 0.10 --binder-opt-wt 1.5 {_buckle}{_stiff}{_align}{_dilate}'
                 f'--save-phase phase.npy --save-fibre fibre.npy --save-fibre-dia fibre_dia.npy'
                 if a.add_recipe else '')
    pay_phase = ' --phase phase.npy --fibre fibre.npy --fibre-dia fibre_dia.npy' if a.add_recipe else ''
    pay_coll = (f' --collector-rint {a.collector_rint:g} --collector-name {a.collector_name}'
                + (f' --collector-scenario {a.collector_scenario}' if a.collector_scenario else '')
                if a.collector_rint >= 0 and a.collector_name else '')
    # STEP3 voxel + field-cloud budget: finer vox resolves necks/SDCP channels for the paper FIELD
    # figure but needs more field points to actually SEE the extra resolution (dof∝1/vox³).
    _fmax = 90000 if a.step3_vox >= 0.4 else (200000 if a.step3_vox >= 0.25 else 300000)
    _gpu = ' --step3-gpu'                                    # GPU by default for ALL vox (CuPy cuSPARSE);
    #   auto-falls back to scipy CPU if CuPy/CUDA missing → same σ, never breaks.  Big win at fine vox,
    #   still a speedup at 0.4.  (--no-gpu isn't baked; delete this flag from run_mpm.sh to force CPU.)
    # RUN_DIR 태그: 레시피 쌍 형식([A-Za-z0-9._]) — run_ 폴더 이름에 박혀 어떤 런인지 자명
    run_tag = 'plain'
    if a.add_recipe and '=' in a.add_recipe:
        _ks, _vs = a.add_recipe.split('=', 1)
        _kl, _vl = _ks.split(':'), _vs.split(':')
        if len(_kl) == len(_vl):
            run_tag = '_'.join(f'{k}{v}' for k, v in zip(_kl, _vl) if k not in ('AM', 'SE'))
    run_tag = re.sub(r'[^A-Za-z0-9._]', '', run_tag.replace(':', '_')) or 'plain'
    # STEP4 체크박스: 미선택 = 그리드 export까지만 (step4_grid.npz 항상 저장 — 나중에 rate만
    # 골라 step4_only.sh로 재개 가능); 선택 = payload 후 각 C-rate를 순차 자동 실행.
    if a.step4_grid_only:                                      # ★grid까지만 = C-rate 무시(v2 스킵)
        s4_rates, s4_chg, s4_sched = [], [], None
    s4_block = ''
    if s4_rates or s4_chg or s4_sched:
        _dis = ' '.join(f'{v:g}' for v in s4_rates)
        _chg = ' '.join(f'{v:g}' for v in s4_chg)
        _win = (('' if a.step4_x0 is None else f' --x0 {a.step4_x0:g}')
                + ('' if a.step4_x100 is None else f' --x100 {a.step4_x100:g}'))   # ASSB vs-Li 창 오버라이드
        _cut = f'--v-min {a.step4_vmin:g} --v-max {a.step4_vmax:g}{_win}'    # 컷오프 + 창 (사용자 설정)
        _icut = f'--i-cut-frac {a.step4_icut:g}'
        # ★풀셀 축 (--step4-r-int): 직렬 R_int 주입 + 산출물 _rint 태그 (전극-내부 기본은 무주입 = R_int=0).
        #   런타임 MPM_S4_RINT env가 킷 생성값을 override (pristine↔aged 스윕을 재생성 없이).
        _rv = None if a.step4_r_int is None else f'{a.step4_r_int:g}'
        _rint = '' if _rv is None else f' --r-int-ohm-cm2 "${{MPM_S4_RINT:-{_rv}}}"'
        _rtag = '' if _rv is None else f'_rint${{MPM_S4_RINT:-{_rv}}}'
        _rlab = '' if _rv is None else f' · ★풀셀 축: R_int=${{MPM_S4_RINT:-{_rv}}} Ωcm² 직렬'
        # ★bimodal poly/SC 전기화학 분리: per-particle D_s/i0 주입 + env override + 산출물 태그
        #   (태그에 값 포함 — 무태그 덮어쓰기로 baseline npz 를 잃는 rint 교훈 재적용)
        _es, _estag, _eslab = '', '', ''
        if _ds_scalar is not None:
            # mono 단결정/다결정 베드 (poly/SC 분리 체크 ON, 한 클래스만) → 단일 scalar D_s.
            #   σ_e 재료는 위 절대-문턱 분류로 이미 분리됨 (mono-SC → AM_S=σ_S 10 mS/cm).
            _es += f' --d-s "${{MPM_S4_DS:-{_ds_scalar:g}}}"'
            _estag += f'_ds${{MPM_S4_DS:-{_ds_scalar:g}}}'
            _eslab = (f' · ★{"SC 단결정" if _ds_scalar_cls == "sc" else "poly 다결정"} 단일 '
                      f'D_s={_ds_scalar:g} m²/s (mono, σ_e '
                      f'{"AM_S=10" if _ds_scalar_cls == "sc" else "AM_P=5"} mS/cm)')
        elif a.step4_ds_poly is not None:
            _es += (f' --d-s-poly "${{MPM_S4_DS_POLY:-{a.step4_ds_poly:g}}}"'
                    f' --d-s-sc "${{MPM_S4_DS_SC:-{a.step4_ds_sc:g}}}"')
            _estag += f'_dsP${{MPM_S4_DS_POLY:-{a.step4_ds_poly:g}}}S${{MPM_S4_DS_SC:-{a.step4_ds_sc:g}}}'
        if a.step4_i0_poly is not None and _ds_scalar is None:
            _es += (f' --i0-poly "${{MPM_S4_I0_POLY:-{a.step4_i0_poly:g}}}"'
                    f' --i0-sc "${{MPM_S4_I0_SC:-{a.step4_i0_sc:g}}}"')
            _estag += f'_i0P${{MPM_S4_I0_POLY:-{a.step4_i0_poly:g}}}S${{MPM_S4_I0_SC:-{a.step4_i0_sc:g}}}'
        if a.step4_ds_poly is not None and _ds_scalar is None:
            _es += f' --am-split-um {a.step4_am_split_um:g}'
            _eslab = f' · ★poly/SC 분리(split r≥{a.step4_am_split_um:g}µm)'
        _dis_loop = f'''  for CR in {_dis}; do
    echo "[run_mpm] STEP4 방전 ${{CR}}C start $(date)  (컷오프 {a.step4_vmin:g}–{a.step4_vmax:g} V{_rlab}{_eslab})"
    python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \\
      --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \\
      --c-rate ${{CR}} {_cut}{_rint}{_es} --gpu --out "step4_c${{CR}}{_rtag}{_estag}.npz" --viz-out "step4_viz_c${{CR}}{_rtag}{_estag}.json" \\
      || echo "[run_mpm] STEP4 방전 ${{CR}}C FAILED — 다음 rate 계속 (위 트레이스 참조)"
    echo "[run_mpm] STEP4 방전 ${{CR}}C end $(date)"
  done
''' if s4_rates else ''
        _chg_loop = f'''  for CR in {_chg}; do
    echo "[run_mpm] STEP4 충전(CCCV) ${{CR}}C start $(date)  (CV@{a.step4_vmax:g}V → I<{a.step4_icut:g}C 종지{_rlab}{_eslab})"
    python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \\
      --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \\
      --c-rate ${{CR}} --charge --cv-hold {_cut} {_icut}{_rint}{_es} --gpu \\
      --out "step4_chg_c${{CR}}{_rtag}{_estag}.npz" --viz-out "step4_viz_chg_c${{CR}}{_rtag}{_estag}.json" \\
      || echo "[run_mpm] STEP4 충전 ${{CR}}C FAILED — 다음 rate 계속 (위 트레이스 참조)"
    echo "[run_mpm] STEP4 충전(CCCV) ${{CR}}C end $(date)"
  done
''' if s4_chg else ''
        # ★Zive 스케줄: 순서 있는 per-step 시퀀스 (charge-first, per-step 컷오프) — crates/charge 대체
        # ★Loop 전개: {'k':'l','to':T,'n':N} = [T..직전] 블록을 총 N회 반복 (Zive "Go to step T, N cycles").
        #   전개는 킷 생성 시점(평면화) — step4_only.sh 는 단순 순차 유지(재개·부분실패 연속성 보존).
        #   cyc 태그 자동 부여(1회차=원본 pass=수동 n, 반복=2..N).  v1 정직성(§F1): 각 런 독립 초기상태
        #   → 프로토콜 반복이지 상태-체이닝 열화 사이클 아님(그건 v2 chaining/R_int(N) 문헌투영 몫) —
        #   cyc 태그는 R_int(N) 축 라벨.  per-step 컷오프(V/CV-I) 달성 = 다음 스텝 = "조건 달성시 next".
        _sched_loop = ''
        s4_sched_flat = expand_sched(s4_sched) if s4_sched else []
        if s4_sched:
            _sl = []
            for _i, _cyc, _st in s4_sched_flat:
                if _st['k'] == 'r':                          # rest = 프로토콜 표시 (v1 독립런 → 모델 무동작)
                    _sl.append(f'  echo "[run_mpm] STEP4 스케줄[{_i}]cyc{_cyc} Rest {_st["t"]:g}min '
                               f'— v1 독립런: 모델 무동작(프로토콜 표시; 완화 모델은 v2 chaining)"')
                    continue
                _cr = f"{_st['r']:g}"
                _o = f"step4_sched{_i:02d}n{_cyc}"
                if _st['k'] == 'c':
                    _pc = f"--v-min {a.step4_vmin:g} --v-max {_st['v']:g}{_win}"
                    _sl.append(
                        f'  echo "[run_mpm] STEP4 스케줄[{_i}] 충전 {_cr}C '
                        f'(CV@{_st["v"]:g}V I<{_st["i"]:g}C cyc{_cyc}{_rlab}{_eslab}) $(date)"\n'
                        f'  python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \\\n'
                        f'    --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \\\n'
                        f'    --c-rate {_cr} --charge --cv-hold {_pc} --i-cut-frac {_st["i"]:g}{_rint}{_es} --gpu \\\n'
                        f'    --out "{_o}_chg_c{_cr}{_rtag}{_estag}.npz" --viz-out "{_o}_viz_chg_c{_cr}{_rtag}{_estag}.json" \\\n'
                        f'    || echo "[run_mpm] 스케줄[{_i}]cyc{_cyc} 충전 {_cr}C FAILED — 다음 스텝 계속"')
                else:
                    _pc = f"--v-min {_st['v']:g} --v-max {a.step4_vmax:g}{_win}"
                    _sl.append(
                        f'  echo "[run_mpm] STEP4 스케줄[{_i}] 방전 {_cr}C '
                        f'(>={_st["v"]:g}V cyc{_cyc}{_rlab}{_eslab}) $(date)"\n'
                        f'  python3 "$SCR/step4_dyn.py" --grid step4_grid.npz \\\n'
                        f'    --ocp-csv "$AP/ocp_nmc811_chen2020.csv" --params-json "$AP/params_nmc811_chen2020.json" \\\n'
                        f'    --c-rate {_cr} {_pc}{_rint}{_es} --gpu \\\n'
                        f'    --out "{_o}_c{_cr}{_rtag}{_estag}.npz" --viz-out "{_o}_viz_c{_cr}{_rtag}{_estag}.json" \\\n'
                        f'    || echo "[run_mpm] 스케줄[{_i}]cyc{_cyc} 방전 {_cr}C FAILED — 다음 스텝 계속"')
            _sched_loop = '\n'.join(_sl) + '\n'
        _run_loops = _sched_loop if s4_sched else (_dis_loop + _chg_loop)
        _n_base = sum(1 for s in (s4_sched or []) if s['k'] != 'l')
        _s4head = ((f"# 3) STEP4-v2 — ★Zive 스케줄 {len(s4_sched)}스텝"
                    + (f" (Loop 전개 → 총 {len(s4_sched_flat)}런)" if len(s4_sched_flat) > _n_base else "")
                    + " 순차 (charge-first, per-step 컷오프).")
                   if s4_sched else
                   f"# 3) STEP4-v2 시간전개 — 방전({_dis or '없음'}) → 충전 CCCV({_chg or '없음'}) 순차.")
        s4_body = f'''{_s4head}
#    각 런은 독립 초기상태 (방전 = x0 충전상태에서, 충전 = x100 방전상태에서 시작).  그리드는 STEP 2가 export.
# ★STEP4 솔버 노브 (2026-07-27 near-null 대수술; docs/step4_bottleneck_analysis_20260727.md)
#   기본값 = 권장값.  런타임 env 로 override 가능 (예: MPM_S4_CONTRAST_CAP=200 bash step4_only.sh).
#   prune_float: 집전체·AM 무접촉 부유 e-클러스터 제거 = 정확특이 블록 소거(해-불변, GPU-CG 회생)
#   ew        : Eisenstat-Walker inexact Newton (초기 반복 느슨 → 총 CG 일량 절감; 최종 수렴판정 동일)
#   gpu_amg   : AMG apply 를 GPU V-cycle 미러로 (빌드는 CPU 1회; cupy 없으면 자동 CPU 폴백)
#   contrast_cap: e-망 σ대비 상한 (0=OFF).  200 → CG iter ×5.2 실측이나 σ_eff −7.8% →
#                 ★수렴 정체 시에만, 그리고 σ-메트릭 보고는 uncapped 런으로 (npz meta 에 태그됨)
export MPM_S4_PRUNE_FLOAT="${{MPM_S4_PRUNE_FLOAT:-1}}"
export MPM_S4_EW="${{MPM_S4_EW:-1}}"
export MPM_S4_GPU_AMG="${{MPM_S4_GPU_AMG:-1}}"
export MPM_S4_CONTRAST_CAP="${{MPM_S4_CONTRAST_CAP:-{a.step4_solver_cap:g}}}"
echo "[run_mpm] STEP4 솔버: prune=$MPM_S4_PRUNE_FLOAT ew=$MPM_S4_EW gpu_amg=$MPM_S4_GPU_AMG cap=$MPM_S4_CONTRAST_CAP"
AP=""
for d in "$KIT/anchor_params" "$KIT/../anchor_params"; do [ -f "$d/ocp_nmc811_chen2020.csv" ] && AP="$d" && break; done
if [ -z "$AP" ]; then
  echo "[run_mpm] STEP4 SKIP — OCP 앵커 없음 (anchor_params/ocp_nmc811_chen2020.csv)."
  echo "          1회 생성: python3 $SCR/step4_pybamm_anchor.py --export-params   (pybamm 필요)"
  echo "          그 뒤 재개: bash step4_only.sh"
else
{_run_loops}fi
'''
        s4_block = s4_body
    # run script: edit paths/GPU as needed, then run on a GPU box
    run = f"""#!/usr/bin/env bash
# MPM run for case {case} — generated by mpm_input_from_case.py
# SE (K-fixed): E_SE={e_se_mpm} GPa ν={nu_se_mpm}  (bulk K={prov['mpm_K_se_gpa']} GPa real-LPSC,
#   shear μ={prov['mpm_mu_se_gpa']} GPa = ×{prov['se_ratio_vs_1p35']} champion; from DEM E_eff {e_se_dem} GPa),
#   press {press_gpa} GPa.  n_grid {n_grid_mpm} → est ~{est_pts / 1e6:.0f}M points (budget {a.max_points / 1e6:.0f}M)
#   — kept tractable so the run FINISHES.  More SE resolution: regenerate with a higher
#   --max-points (heavier/slower) or edit --n-grid below.  If it OOMs, lower --n-grid / raise --gpu-mem.
set -uo pipefail
# ── 경로 자립: KIT = zip 푼 폴더(입력 csv), SCR = 레포 scripts/ (킷 폴더 또는 그 부모에서 탐색) ──
KIT="$(cd "$(dirname "$0")" && pwd)"
SCR=""; for c in "$KIT/scripts" "$KIT/../scripts"; do [ -d "$c" ] && SCR="$(cd "$c" && pwd)" && break; done
if [ -z "$SCR" ]; then
  echo "[run_mpm] ABORT — scripts/ 를 못 찾음: 레포 루트(또는 scripts 심링크 있는 폴더)에 킷을 푸세요."
  exit 1
fi
# ── scripts 자동 최신화 (kit-gen↔runtime 버전 스큐 방지 = "--x100 unrecognized" 재발 차단; 끄기 MPM_NO_PULL=1) ──
if [ -z "${{MPM_NO_PULL:-}}" ] && [ -d "$SCR/../.git" ]; then
  echo "[run_mpm] git pull --ff-only (scripts 최신화)…"
  ( cd "$SCR/.." && git pull --ff-only ) || echo "  ⚠ git pull 스킵 — 기존 스크립트로 진행 (필요시 수동 pull)"
fi
# ── one GPU = one run: GPU 경합 방지 (산출물 충돌은 아래 RUN_DIR 격리가 원천 차단).  MPM_FORCE=1 로 무시 ──
if [ -z "${{MPM_DETACHED:-}}" ] && [ -z "${{MPM_FORCE:-}}" ] && pgrep -f 'mpm3d_compaction.py' >/dev/null 2>&1; then
  echo "[run_mpm] ABORT — an MPM run is already active (pgrep mpm3d_compaction).  one GPU = one run."
  echo "          wait for FINAL / 'kill <PID>' first, or 'MPM_FORCE=1 bash run_mpm.sh' to override."
  exit 1
fi
# ── self-detach: an SSH drop must NOT kill the run (the foreground run kept dying on disconnect). ──
# ── RUN_DIR = 런 전용 폴더: 모든 산출물이 여기에만 쓰임 → 다른 킷/이전 런과 절대 안 섞이고
#    (2026-07-17 SBE↔DBE 루트-덮어쓰기·mv-레이스 사고 재발 방지), 진행 중 외부 정리 작업의
#    영향도 없음.  완료 시 $KIT/latest_run 심링크가 이 폴더를 가리킴. ──
if [ -z "${{MPM_DETACHED:-}}" ]; then
  export MPM_DETACHED=1
  export RUN_DIR="$KIT/run_{run_tag}_$(date +%Y%m%d_%H%M%S)_$$"
  mkdir -p "$RUN_DIR"
  log="$RUN_DIR/mpm_run.log"
  echo "→ detached — survives SSH drop.  run dir: $RUN_DIR"
  setsid nohup bash "$0" "$@" >"$log" 2>&1 </dev/null &
  echo "   PID $!     follow: tail -f $log     stop: kill $!"
  exit 0
fi
cd "$RUN_DIR"
# ===== actual run (detached; all output → this run dir only) =====
echo "[run_mpm] $(hostname) start $(date)  n_grid={n_grid_mpm}  est_pts~{est_pts / 1e6:.0f}M  dir=$RUN_DIR"
# ── v3 열화-근접 옵션 (기본 안전 = 기존 convention 유지; §F1) ──────────────────────────────
#   MPM_FRACTURE=1        → 초기압밀 취성 crack-void (ASSUMED-FORM void frag0.15/pulv0.35; DEM=WHERE, MPM=형태)
#   MPM_PERIODIC_SIGMA=1  → STEP3 σ 측면 주기BC (bulk-RVE 정합; ⚠기존 corpus=절연벽 through-thickness → 전환 시 재run)
#   Joule 발열맵(#29) = 기본 ON (순수 진단 q∝|J|²/σ, σ/porosity 불변 → hot-spot '어디서 발열')
FRAC=()
if [ "${{MPM_FRACTURE:-0}}" = "1" ] && [ -f "$KIT/fracture_scaffold.csv" ]; then
  FRAC=(--fracture-scaffold "$KIT/fracture_scaffold.csv" --fracture-min-stage fragmentation)
  echo "[run_mpm] ★ MPM_FRACTURE=1 → 취성 crack-void 적용 (ASSUMED-FORM void; DEM 취성 위치 기반)"
fi
PSIG=(); [ "${{MPM_PERIODIC_SIGMA:-0}}" = "1" ] && {{ PSIG=(--periodic); echo "[run_mpm] ★ MPM_PERIODIC_SIGMA=1 → STEP3 σ 주기BC (bulk-RVE)"; }}
# 1) plastic compaction of the REAL SE around the fixed AM scaffold (periodic x,y RVE = DEM 'boundary p p f')
python3 "$SCR/mpm3d_compaction.py" \\
  --am-scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" --periodic \\
  --lateral-box {box_x} --n-grid {n_grid_mpm} --arch cuda --gpu-mem 28 --protocol hold --frames 150 \\
  --e-se {e_se_mpm} --nu-se {nu_se_mpm} --target-gpa {press_gpa} \\
  --save-se se_dump.npy --save-dg se_dump_dg.npy --save-eps se_dump_eps.npy --save-metrics mpm_metrics.json{add_flags} "${{FRAC[@]}}" \\
  || {{ echo "[run_mpm] STEP 1 (compaction) FAILED — see the trace above.  NOT running the payload: it would"; \\
        echo "          rebuild mpm_payload.json from the STALE se_dump.npy of a PREVIOUS run and report a"; \\
        echo "          leftover porosity as if it were this run.  Fix the error and re-run."; exit 1; }}
# 2) webapp payload (AM spheres + SE surface + seed/compacted + raw metrics)
#    + STEP3 σ_e 저항망 (전도상 voxel Kirchhoff, 풀해상도 — metrics.step3.sigma_e_eff + 입자별 je;
#      상대비교용 σ표는 metrics에 기록됨.  끄기: --no-step3)
python3 "$SCR/mpm_webapp_payload.py" \\
  --se se_dump.npy --scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" \\
  --n-vox 192 --tri-step 4 --smooth 1.5 --target-porosity {tgt_pay} --eps se_dump_eps.npy{pay_dilate} \\
  --void-max 180000 --step3-vox {a.step3_vox:g} --field-max-points {_fmax}{_gpu} --joule-heat "${{PSIG[@]}}" --metrics-json mpm_metrics.json --case {case}{pay_phase}{pay_coll} --save-step4-grid step4_grid.npz --out mpm_payload.json \\
  || {{ echo "[run_mpm] STEP 2 (payload) FAILED — 압밀(se_dump.npy)은 무사하니 원인 수정 후 payload만 재실행:"; \\
        echo "          cd $RUN_DIR && bash $KIT/step4_only.sh 는 STEP4용이고, payload는:"; \\
        echo "          sed -n '/mpm_webapp_payload/,/--out mpm_payload.json/p' $KIT/run_mpm.sh > payload_only.sh && bash payload_only.sh"; \\
        echo "          (흔한 원인: pip 모듈 누락 — python3 -m pip install scikit-image scipy)"; exit 1; }}
{s4_block}ln -sfn "$RUN_DIR" "$KIT/latest_run"
touch "$RUN_DIR/mpm_done.marker"     # ★ 완료 마커 — '한 줄' 명령의 poll(until test -f latest_run/mpm_done.marker)용
echo "[run_mpm] DONE $(date) → 결과 폴더: $RUN_DIR  ($KIT/latest_run 심링크 = 여기)"
echo "          upload mpm_payload.json + mpm_metrics.json back to the case in the webapp"
echo "          (additive run이면 mpm_metrics.json의 step3.sigma_e_eff_S_cm = STEP3 σ_e — viewer 전류밀도 모드로 색칠)"
echo "          (step4 결과: step4_c*.npz/step4_chg_c*.npz = 곡선 시계열, step4_viz_*.json = 뷰어 st4 입력)"
echo "          (오래된 run_* 폴더는 디스크 차면 지워도 됨 — 산출물 회수 후)"
"""
    rp = os.path.join(a.out, 'run_mpm.sh')
    open(rp, 'w').write(run); os.chmod(rp, 0o755)
    if s4_rates or s4_chg or s4_sched:                       # 재개/단독 실행용 — 압밀 재실행 없이 STEP4만
        s4_only = ('#!/usr/bin/env bash\nset -uo pipefail\n'
                   '# STEP4만 (재개/단독) — 사용법: bash step4_only.sh [런폴더]   (기본: latest_run)\n'
                   'KIT="$(cd "$(dirname "$0")" && pwd)"\n'
                   'SCR=""; for c in "$KIT/scripts" "$KIT/../scripts"; do [ -d "$c" ] && SCR="$(cd "$c" && pwd)" && break; done\n'
                   '[ -z "$SCR" ] && { echo "scripts/ 못 찾음 — 레포 루트에 킷을 푸세요"; exit 1; }\n'
                   '# scripts 자동 최신화 (버전 스큐 방지; 끄기 MPM_NO_PULL=1)\n'
                   'if [ -z "${MPM_NO_PULL:-}" ] && [ -d "$SCR/../.git" ]; then ( cd "$SCR/.." && git pull --ff-only ) || echo "  ⚠ git pull 스킵 — 기존 스크립트로 진행"; fi\n'
                   'RUN="${1:-$KIT/latest_run}"\n'
                   '[ -f "$RUN/step4_grid.npz" ] || { echo "step4_grid.npz 없음: $RUN — run_mpm.sh 먼저 (payload가 그리드 export)"; exit 1; }\n'
                   'if [ -z "${S4_DETACHED:-}" ]; then\n'
                   '  export S4_DETACHED=1\n'
                   '  log="$RUN/step4_run_$(date +%Y%m%d_%H%M%S).log"\n'
                   '  echo "→ detached — log: $log"\n'
                   '  setsid nohup bash "$0" "$@" >"$log" 2>&1 </dev/null &\n'
                   '  echo "   PID $!     follow: tail -f $log"\n'
                   '  exit 0\nfi\ncd "$RUN"\n' + s4_body)
        sp = os.path.join(a.out, 'step4_only.sh')
        open(sp, 'w').write(s4_only); os.chmod(sp, 0o755)
    # ── A-1 사이클 열화 앵커 companion (real_degrading_electrode §3 A-1) — 이 킷 스캐폴드 + 케이스
    #    설정(box_x/n_grid/E_SE/ν/press)으로 바로 실행.  webapp 킷에 항상 포함(zip = dir 전체).
    #    ★plain 문자열 + __TOKEN__ 치환 (f-string 아님 → bash ${}/$() 리터럴; \<newline> 회피 위해
    #    배열은 () 안 다줄, 명령은 한 줄). ──────────────────────────────────────────────────────
    a1_tmpl = ('#!/usr/bin/env bash\n'
               'set -uo pipefail\n'
               '# A-1 MPM 사이클 열화 앵커 — pristine(N0) + 충전앵커(SC-5.1%/poly팽창) + ΔV심화(-5.9%)\n'
               '#   → cycle_geom_debond 로 기하 debond/void.  ⚠ 충전-상태(가역 SOC breathing) 스냅샷 =\n'
               '#   영구 fade 아님; 비가역화 판정은 ledger 캘리브(A-3 --mpm-anchor).  사용: bash run_a1_anchors.sh\n'
               'KIT="$(cd "$(dirname "$0")" && pwd)"\n'
               'SCR=""; for c in "$KIT/scripts" "$KIT/../scripts"; do [ -d "$c" ] && SCR="$(cd "$c" && pwd)" && break; done\n'
               '[ -z "$SCR" ] && { echo "scripts/ 못 찾음 — 레포 루트에 킷을 푸세요"; exit 1; }\n'
               'if [ -z "${MPM_NO_PULL:-}" ] && [ -d "$SCR/../.git" ]; then ( cd "$SCR/.." && git pull --ff-only ) || echo "  ⚠ git pull 스킵"; fi\n'
               'OUT="$KIT/a1_anchors"; mkdir -p "$OUT"\n'
               'if [ -z "${A1_DETACHED:-}" ]; then\n'
               '  export A1_DETACHED=1\n'
               '  log="$OUT/a1_run_$(date +%Y%m%d_%H%M%S).log"\n'
               '  echo "→ detached — log: $log"\n'
               '  setsid nohup bash "$0" "$@" >"$log" 2>&1 </dev/null &\n'
               '  echo "   PID $!     follow: tail -f $log"\n'
               '  exit 0\n'
               'fi\n'
               'COMMON=(--am-scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" --periodic\n'
               '        --lateral-box __BOX__ --n-grid __NG__ --arch cuda --gpu-mem 28 --protocol hold --frames 150\n'
               '        --e-se __ESE__ --nu-se __NUSE__ --target-gpa __PRESS__)\n'
               'run_one() { local lab="$1"; shift; echo "=== A-1 앵커: $lab ==="; '
               'python3 "$SCR/mpm3d_compaction.py" "${COMMON[@]}" "$@" --save-metrics "$OUT/m_${lab}.json" '
               '|| { echo "FAIL $lab — 위 트레이스"; exit 1; }; }\n'
               'run_one N0\n'
               'run_one charged --cycle-deform --cycle-n 1 --cycle-dv-sc -0.051 --cycle-dv-poly 0.059 --dv-pct-poly 0.30\n'
               'run_one charged_deep --cycle-deform --cycle-n 2 --cycle-dv-sc -0.059 --cycle-dv-poly 0.059 --dv-pct-poly 0.30\n'
               'echo "=== 기하 debond/void (pristine 대비) ==="\n'
               'python3 "$SCR/cycle_geom_debond.py" "$OUT/m_N0.json" "$OUT/m_charged.json" "$OUT/m_charged_deep.json" --csv "$OUT/a1_debond.csv"\n'
               'echo "완료 → $OUT/ (m_*.json 앵커, a1_debond.csv 기하 debond/void).  ⚠ 충전상태(가역); ledger가 비가역 판정."\n')
    a1 = (a1_tmpl.replace('__BOX__', f'{box_x}').replace('__NG__', f'{n_grid_mpm}')
          .replace('__ESE__', f'{e_se_mpm}').replace('__NUSE__', f'{nu_se_mpm}')
          .replace('__PRESS__', f'{press_gpa}'))
    ap1 = os.path.join(a.out, 'run_a1_anchors.sh')
    open(ap1, 'w').write(a1); os.chmod(ap1, 0o755)
    print(f'MPM input for case "{case}" → {a.out}/')
    if _frac_note.strip():
        print('  [취성]' + _frac_note)
    print(f'  am_scaffold.csv ({len(am_rows)} AM)  se_scaffold.csv ({len(se_rows)} SE)  '
          f'run_mpm.sh  mpm_input.json  (target_porosity={tgt})'
          + (f'  step4_only.sh  [★Zive 스케줄 {len(s4_sched)}스텝: '
             + ' → '.join(('휴%gm' % s['t']) if s['k'] == 'r'
                          else ('↻스텝%d ×%d회' % (s['to'], s['n'])) if s['k'] == 'l'
                          else (('충' if s['k'] == 'c' else '방') + ('%gC' % s['r']))
                          for s in s4_sched) + ']'
             if s4_sched else
             f'  step4_only.sh  [STEP4 방전: {", ".join(f"{v:g}C" for v in s4_rates) or "—"}'
             f' / 충전CCCV: {", ".join(f"{v:g}C" for v in s4_chg) or "—"}]'
             if (s4_rates or s4_chg) else
             ('  [★STEP4 grid까지만 (v2 스킵 — step4_grid.npz 만 생성)]' if a.step4_grid_only
              else '  [STEP4 미선택 — 그리드 export까지]'))
          + '  run_a1_anchors.sh  [A-1 사이클 열화 앵커: pristine+충전+ΔV심화 → 기하 debond/void]')


if __name__ == '__main__':
    main()
