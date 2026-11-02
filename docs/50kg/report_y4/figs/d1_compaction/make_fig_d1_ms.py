#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""50kg D1 (kg50_d1_b50 · SE D50 1 µm) 압밀 곡선 — 세 패널 왼쪽 열 (두께 · 판 속도 · 판 압력) · Origin CSV · .ogs · 미리보기 PNG/SVG ·
key_numbers_d1_ms.json · 오른쪽 3D 단계 프레임 표 (1저자 11-02 *"이 그림도 50Kg_D1 기준으로 만들면 좋을듯"*).

    python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py             # 산출 (결정적 — 다시 돌려도 같은 바이트)
    python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py --atomtop   # + 원자 기준 그림 (raw/kg50_d1_atomtop.csv 없으면 거부)
    python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py --selftest  # 반례 시험 (합성 로그 · 리포 자료 안 읽음)

본보기 = ps73 ms 판 (`docs/data/ps73_compaction_curve_20261006/make_fig_ms.py` · `make_fig_velocity_ms.py` · 그 README §5 · §7 · §8) 의
서식 · 축 · Origin CSV (1 줄 Long Name · 2 줄 Units · C 열 Source).  로그 읽기 = ps73 생성기와 같은 `scripts/compaction_curve.py`
(`parse_log` · `resolve` · `_phase_at` — thermo 블록 · run 마다 첫 줄 (설정 줄) 버림 · 단계 표지 · 판정 줄 · 사본 금지).

입력 (리포 · 읽기만):
  docs/data/kg50_d1_end_20261031/kg50_d1_b50_log.liggghts — 본 런 로그 (덱 명령 되풀이 포함 · 20,001 → 2,785,002)
  docs/data/kg50_d1_end_20261031/README.md — 로그 · 덱 · 끝 덤프 sha256 · 끝 판 높이 기록 (mesh_end 122.596 µm)
  docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts — 리포 덱 (로그 안 덱과 설정이 같은지)
  docs/50kg/report_y4/draft2/data/D1/{metrics_D1.json, curve_D1.csv} — 초안 2 압밀 곡선 (다른 코드로 읽은 값과 대조 · 단계 표 ε_sphere 참고값)
값:
  시간 (ms) = step × dt × 1000 (dt = 로그 안 덱 `variable dt` = 모든 숫자 `timestep`) — 축척 덱의 시간 (실제 압착 시간 아님)
  두께 (µm) = 판 위치 (덱으로 계산 — 메시 덤프는 리포에 없다): 안정화 = `PLATE HEIGHT` 고정 · 압축 = press_speed 등속 하강 ·
             이완 = 고정 → 끝 값을 mesh_end (6 유효숫자) 와 대조 (반올림 반폭 안이어야 한다)
  판 속도 (µm/s) = press_speed (덱 m/s) × 1e6 / r 배율 · 압력 (MPa) = thermo `pressMPa` / P 배율 (Scale 머리 r×1000 · P×0.001)
정착 (Particle packing) 구간 두께 = 원자 위치가 필요한데 리포에 없다 → 판 기준 그림에는 그리지 않는다 (README §4).
1저자 11-02 밤 (ps73 옛 그림과 대조): ① 정착 구간을 0 ms 부터 · 끊긴 y 축 · 시작 빨간 화살표 ② 한 곡선 = 원자 기준 (모든 원자의 max(z + r)) ·
Origin 꼴 ③ 압력 슬라이드판 (판 정지 뒤 = ps73 README §5 의 모식 감쇠 · 원값판은 따로) — ③ = 바로 (README §7) · ①② = D1 런 기계에서
`cluster/d1_atomtop_cluster.py` 가 만든 CSV 를 `raw/kg50_d1_atomtop.csv` 에 넣은 뒤 (README §8 · 검사 ①–⑪ 통과해야 그린다 · 없으면 지어내지 않는다).
"""
import csv
import hashlib
import itertools
import json
import math
import re
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True   # 리포 모듈 (scripts · ps73 · cluster) 을 읽기만 한다 — 남의 폴더에 __pycache__ 를 쓰지 않는다
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
import compaction_curve as CC  # noqa: E402  ps73 생성기와 같은 로그 읽기 규칙 (사본 금지)

LOG = ROOT / 'docs/data/kg50_d1_end_20261031/kg50_d1_b50_log.liggghts'
D1_README = ROOT / 'docs/data/kg50_d1_end_20261031/README.md'
DECK = ROOT / 'docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50.liggghts'
INSERT_DECK = ROOT / 'docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50/input_kg50_d1_b50_insert.liggghts'
METRICS = ROOT / 'docs/50kg/report_y4/draft2/data/D1/metrics_D1.json'
CURVE_D1 = ROOT / 'docs/50kg/report_y4/draft2/data/D1/curve_D1.csv'
#: D1 README §1 표 · §2 표의 기록 — 생성기가 README 글에 같은 글자가 있는지 확인한다 (README 와 상수가 갈리면 멈춘다)
LOG_SHA256 = '6a90f706da68e3d5041ff063d0ffd4f61e9d89a5823f29e0755a23ed679bc1b5'
DECK_SHA256 = '514afdb705613dab876c9c0ff5c1f2fef3fad3e029d71778875c08b89edfde91'
ATOM_END_SHA256 = 'e55bb3f44c138cf824837f9dd17775eaea5cc1148b28a8c1d4c07c57a3aec635'
MESH_END_SHA256 = 'ec99971a2e7f27e1baeedbdab72e6f3c2db52239cc318671142931d56592fe16'
MESH_END_TEXT = '판 높이 122.596 µm (mesh_end)'
#: D1 런 폴더 (리포 기록: docs/data/kg50_decks_20261027_v3_b50/README.md §3 — 삽입 런 `cd $HOME/simulation/kg50_d1_b50` · 끝 묶음 접두 `kg50_d1_b50/`)
RUN_PARENT, RUN_CASE = '$HOME/simulation', 'kg50_d1_b50'
TAR_TAG = 'kg50_d1_stage_frames_20261102'

ORIGIN, PREV = HERE / 'origin', HERE / 'previews'
FIGSIZE = None   # (W, H) in — 슬라이드 칸 크기로 그리기 (1저자 11-03 *"글씨가 보이게 들어가려면 사이즈가 충족"*) · None = 4.3 × 7.2 · 이때 y 이름 두 줄
KEY_JSON = HERE / 'key_numbers_d1_ms.json'
STAGE_CSV = HERE / 'stage_frames_d1.csv'
FIG_NAME = 'd1_ms_compaction_3panel'
CSV_NAMES = {'thickness': 'd1_ms_thickness_plate', 'velocity': 'd1_ms_plate_velocity', 'pressure': 'd1_ms_pressure'}

XLABEL = 'Time (ms)'          # 1저자 슬라이드 축 이름 (ps73 미리보기 = 'Simulation time (ms)' — 한정어는 README §5 · 캡션에)
X0, X1 = 0.0, 2800.0          # ms — 0 (투입) ~ 끝 2,785.002 ms + 여유
STL_HALF_ULP_DECK = 5e-7      # mesh STL 꼭짓점 = 6 유효숫자 (0.122596 덱 m) → 반올림 반폭 5e-7 덱 m = 0.0005 µm
STAGE_P_MPA = 50.0            # 오른쪽 3D 단계 "50 MPa"
SLOPE_REL = 1e-9              # 판 궤적 기울기 자기검사 (상대)
GRAY, LIGHT, RED = '#404040', '#9AA0A8', '#F14040'
COLORS = {'thickness': '#7030A0', 'velocity': '#4FBDFF', 'pressure': '#F14040'}   # 1저자 슬라이드 (11-02): 두께 보라 · 판 속도 파랑 · 압력 빨강
OGS_RGB = {'thickness': '112,48,160', 'velocity': '79,189,255', 'pressure': '241,64,64'}
XTICK_MAJOR = 500             # ms — 슬라이드와 같은 눈금 (0 … 2500 · 축 끝 2800 = 런 끝 2,785.002 를 덮는다)
THICK_YLIM = (115, 155)       # µm — 위쪽에 가로 단계 이름 자리
SRC = {'noplate': 'no plate (0 by definition)', 'thermo': 'measured (thermo pressMPa)',
       'placed': 'plate placed (log PLATE HEIGHT)', 'stab': 'plate fixed (stabilization · deck)',
       'c_start': 'compression start (deck press_speed)', 'comp': 'compression (deck press_speed · computed)',
       'stop': 'plate stop (loop exit)', 'relax': 'plate fixed (relaxation · deck)', 'end': 'end of run (= mesh_end check)'}
_NUM = r'[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?'


def _load(name, path):
    """리포 안 모듈을 경로로 읽는다 (`python3 -I` = 스크립트 폴더가 sys.path 에 없다) — 사본 대신 그 파일을 쓴다."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


#: 원자 기준 두께 (1저자 11-02 밤 *"첫번째부터 예전처럼 particle packing 도"*) — D1 런 기계에서 `cluster/d1_atomtop_cluster.py` 가 만든 CSV.
#: step 목록 · 머리 · 런 폴더 sha256 = 그 스크립트의 상수 그대로 (사본 금지) · PCHIP = ps73 생성기 함수 그대로.
CLUSTER = _load('d1_atomtop_cluster', HERE / 'cluster' / 'd1_atomtop_cluster.py')
PS73 = _load('ps73_make_fig_ms', ROOT / 'docs/data/ps73_compaction_curve_20261006/make_fig_ms.py')
ATOMTOP_CSV = HERE / 'raw' / 'kg50_d1_atomtop.csv'
ATOMTOP_HEAD = list(CLUSTER.HEAD)
ATOMTOP_EARLY = list(CLUSTER.REPLAY_STEPS) + [s for s, _ in CLUSTER.CKPTS]
ATOMTOP_DUMPS = list(CLUSTER.DUMP_STEPS)
ATOMTOP_SHA = dict(CLUSTER.SHA)
#: 원 삽입 런 화면 (끝 묶음 멤버 `kg50_d1_b50/log_kg50_d1_b50_ins.out` · sha256 a83ee39e… = ATOMTOP_SHA · 묶음 sha256 = D1 README §1) 의 값
REPLAY_REF = {1: (168457, '0.11946798'), 1000: (168457, '0.17034351'), 2000: (168457, '0.23018355'), 3000: (168457, '0.29890105'), 4000: (168457, '0.37462336'), 5000: (168457, '0.45695706'), 6000: (168457, '0.54772567'), 7000: (168457, '0.64616151'), 8000: (168457, '0.75103338'), 9000: (168457, '0.86357835'), 10000: (168457, '0.98082832'), 11000: (168457, '1.104255'), 12000: (168457, '1.2338527'), 13000: (168457, '1.3650701'), 14000: (168457, '1.499203'), 15000: (168457, '1.6376978'), 16000: (168457, '1.7822583'), 17000: (168457, '1.9289022'), 18000: (168457, '2.079641'), 19000: (168457, '2.2333726'), 20000: (168457, '2.3892872')}
INSERT_REF = ('inserted 168457 particle templates', '(mass 9.557438e-01) at step 1')
KE_RTOL = 1e-6                # 재개 G1 규칙 (ps73 과 같다) — 체크포인트 · 재현 KE ↔ 원 로그 (상대)
OUTLIER_MIN_UM = 20.0         # 뺄 점 = 튀어 오른 입자 하나 (윗면 − p99.9 ≥ 20 µm) 일 때만 (ps73 규칙 · 기본은 아무것도 안 뺀다)
INTERP_DT_MS = 1.0            # 앞 구간 (첫 점 → 첫 원 덤프) PCHIP 채움 간격 (ps73 과 같다)
SLIDE_TAU_STEP = 15000        # 압력 슬라이드판 모식 감쇠 시간 상수 (ps73 make_fig.py 값 · 그림용 — 자료에서 정한 값 아님)
HI_SPAN_UM = 20.0             # 끊긴 y 축 위 범위 높이 (아래 범위와 같은 µm/높이 축척)
GAP_FRAC = 0.06               # 끊긴 자리 높이 (아래 범위 높이의 몫)
HI_FRAC = None                # 위 범위 눈에 보이는 높이 (아래 범위 높이의 몫) · None = 같은 µm/높이 축척 · 1저자 11-03 ps73 옛 그림처럼 위 띠를 좁게 (--hi-frac)
SRC_REPLAY, SRC_CKPT, SRC_DUMP = 'replay (insertion · NP 1)', 'checkpoint (run 0)', 'atom dump'
SRC_INTERP = 'interpolated (PCHIP between measured points)'
SRC_SCHEMATIC = 'schematic relaxation (모식 · not measured)'
SRC_FREEFALL = 'schematic free fall from insertion (모식 · not measured)'
CKPT_STEPS = [s for s, _ in CLUSTER.CKPTS]   # 기본판 (1저자 11-02 밤 — 재현 없음) 의 앞 구간 측정점 = 체크포인트 run 0 열 개
FIG_SLIDE, FIG_AT, FIG_AT_SLIDE = FIG_NAME + '_slide', FIG_NAME + '_atomtop', FIG_NAME + '_atomtop_slide'
CSV_SLIDE, CSV_AT = 'd1_ms_pressure_slide', 'd1_ms_thickness_atomtop'


# ───────────────────────────── 덱 설정 (로그 안 명령 되풀이 · 또는 덱 글) ─────────────────────────────
def _one(pattern, text, what):
    hits = re.findall(pattern, text, re.M)
    if len(hits) != 1:
        raise ValueError(f'{what}: {len(hits)} 줄 (하나여야 한다)')
    return hits[0]


def deck_settings(text):
    """로그 (LIGGGHTS 머리 · 명령 되풀이 = 변수 풀린 줄 포함) 또는 덱 글 → 설정.  어긋나면 ValueError (fail-closed).
    단위 = `units si` · Scale 머리 `# Scale: r×A, E×B, P×C` (길이 µm/덱 m = 1e6/A · 실제 MPa = 덱 MPa / C) ·
    dt = `variable dt` = 모든 숫자 `timestep` (로그면 풀린 숫자 줄이 있어야 한다) · 판 속도 = `variable press_speed` = 모든
    move/mesh linear z 성분 (옆으로 0) · 압력 면적 = `pressMPa` 식 = 판정 식 `current_press` = 상자 x·y (로그) ·
    `PLATE HEIGHT` = Z_MAX + r_AM_P + plate_margin (로그) · 압축 루프 `run N` · atom · mesh 덤프 간격 · 덤프 폴더."""
    is_log = text.startswith('LIGGGHTS (')
    body = '\n'.join(ln.split('#', 1)[0].rstrip() for ln in text.splitlines())
    units = _one(r'^\s*units\s+(\S+)\s*$', body, 'units')
    if units != 'si':
        raise ValueError(f'units {units} (si 여야 한다 — dt 초 · 길이 덱 m · 압력 Pa)')
    s_r, s_e, s_p = (float(v) for v in _one(rf'^#\s*Scale:\s*r×({_NUM}),\s*E×({_NUM}),\s*P×({_NUM})\s*$', text, 'Scale 머리'))
    if s_r <= 0 or s_p <= 0:
        raise ValueError(f'Scale 배율 r×{s_r} · P×{s_p}')
    dt = float(_one(rf'^\s*variable\s+dt\s+equal\s+({_NUM})\s*$', body, 'variable dt'))
    ts = re.findall(r'^\s*timestep\s+(\S+)\s*$', body, re.M)
    num_ts = [t for t in ts if t != '${dt}']
    if dt <= 0 or not ts or (is_log and not num_ts) or any(not re.fullmatch(_NUM, t) or float(t) != dt for t in num_ts):
        raise ValueError(f'timestep {ts} ≠ variable dt {dt}')
    speed = float(_one(rf'^\s*variable\s+press_speed\s+equal\s+({_NUM})\s*$', body, 'variable press_speed'))
    mv = re.findall(r'^\s*fix\s+\S+\s+\S+\s+move/mesh\s+mesh\s+\S+\s+linear\s+(\S+)\s+(\S+)\s+(\S+)\s*$', body, re.M)
    if not mv or (is_log and all(vz == '-${press_speed}' for _, _, vz in mv)):
        raise ValueError(f'move/mesh linear 줄 {mv} (로그면 풀린 숫자 줄이 있어야 한다)')
    speeds = set()
    for vx, vy, vz in mv:
        if float(vx) != 0.0 or float(vy) != 0.0:
            raise ValueError(f'판이 옆으로 움직인다: {vx} {vy}')
        speeds.add(speed if vz == '-${press_speed}' else -float(vz))
    if speeds != {speed} or speed <= 0:
        raise ValueError(f'판 속도 {sorted(speeds)} ≠ press_speed {speed}')
    target = float(_one(rf'^\s*variable\s+target_press\s+equal\s+({_NUM})\s*$', body, 'variable target_press'))
    area = float(_one(rf'^\s*variable\s+pressMPa\s+equal\s+abs\(f_top_mesh\[3\]\)/({_NUM})/1000000\s*$', body, 'pressMPa 식'))
    judge_areas = {float(a) for a in re.findall(
        rf'^\s*variable\s+current_press\s+equal\s+"abs\(f_top_mesh\[3\]\)\s*/\s*({_NUM})\s*/\s*1000000"\s*$', body, re.M)}
    if judge_areas != {area}:
        raise ValueError(f'판정 식 면적 {sorted(judge_areas)} ≠ pressMPa 면적 {area}')
    out = {'units': units, 'scale_r': s_r, 'scale_E': s_e, 'scale_P': s_p, 'um_per_deck_m': 1e6 / s_r, 'mpa_per_deck_mpa': 1.0 / s_p,
           'dt_s': dt, 'press_speed_deck_m_s': speed, 'target_deck': target, 'target_mpa': target / s_p, 'area_deck_m2': area,
           'r_am_p_deck': float(_one(rf'^\s*variable\s+r_AM_P\s+equal\s+({_NUM})\s*$', body, 'variable r_AM_P')),
           'plate_margin_deck': float(_one(rf'^\s*variable\s+plate_margin\s+equal\s+({_NUM})\s*$', body, 'variable plate_margin'))}
    if is_log:                                       # read_restart 출력 · 판 높이 출력 = 로그에만 (덱 글에는 region · print 명령)
        x0, y0, _, x1, y1, _ = (float(v) for v in _one(
            rf'^\s*orthogonal box = \(({_NUM}) ({_NUM}) ({_NUM})\) to \(({_NUM}) ({_NUM}) ({_NUM})\)\s*$', body, 'orthogonal box'))
        if abs((x1 - x0) * (y1 - y0) - area) > 1e-12 * max(1.0, area):
            raise ValueError(f'상자 x·y 면적 {(x1 - x0) * (y1 - y0)} ≠ pressMPa 면적 {area}')
        zmax = float(_one(rf'^\s*=+\s*Z_MAX \(center\):\s*({_NUM})\s*=+\s*$', body, 'Z_MAX 출력'))
        plate = float(_one(rf'^\s*=+\s*PLATE HEIGHT:\s*({_NUM})\s*=+\s*$', body, 'PLATE HEIGHT 출력'))
        if abs(plate - (zmax + out['r_am_p_deck'] + out['plate_margin_deck'])) > 1e-12:
            raise ValueError(f'PLATE HEIGHT {plate} ≠ Z_MAX {zmax} + r_AM_P + plate_margin')
        out.update(box_xy_deck=[x0, x1, y0, y1], zmax_center_deck=zmax, plate_z0_deck=plate)
    out['loop_run_steps'] = int(_one(r'^\s*label\s+loop_press\s*\n\s*run\s+(\d+)\s*$', body, '압축 루프 run'))
    ad = re.findall(r'^\s*dump\s+dmp_atom\s+all\s+custom\s+(\d+)\s+(\S+)/atom_\*\.liggghts\b', body, re.M)
    md = re.findall(r'^\s*dump\s+dmp_mesh\s+all\s+mesh/stl\s+(\d+)\s+(\S+)/mesh_\*\.stl\b', body, re.M)
    if len(ad) != 1 or len(md) != 1 or ad[0][1] != md[0][1]:
        raise ValueError(f'atom · mesh 덤프 줄 {ad} · {md}')
    if re.search(r'^\s*undump\s+dmp_(atom|mesh)\s*$', body, re.M):
        raise ValueError('undump dmp_atom/dmp_mesh — 덤프가 끝까지 이어진다는 가정이 깨진다')
    out.update(atom_dump_every=int(ad[0][0]), mesh_dump_every=int(md[0][0]), post_dir=ad[0][1])
    return out


# ───────────────────────────── thermo 곡선 (compaction_curve 규칙) ─────────────────────────────
def read_curve(log_path, target_deck, loop_run_steps):
    """로그 → 행 (설정 줄 뺌 · 단계) · 단계 경계 · 판정 줄 · KE 참고 (설정 줄 포함 · 처음 것).  어긋나면 ValueError.
    C1 압력 열 · 유한 · C4 판정 줄 = 같은 step thermo · 목표 = 덱 하나 · 마지막만 목표 이상 · PHASE 4 = 루프 탈출 · C6 step 엄격 증가 ·
    압축 run 이 loop_run_steps 마다 빈틈없이 이어진다 · read_restart 파일 step = 첫 thermo step (하나의 런 조각)."""
    seg = CC.resolve(CC.parse_log(str(log_path)))
    if not seg['blocks']:
        raise ValueError('thermo 블록이 없다')
    prob, bounds = [], {}
    for step, num, name in seg['marks']:
        if step is None or str(num) in bounds:
            prob.append(f'PHASE {num} 표지 (step {step}) 가 풀리지 않거나 둘')
        else:
            bounds[str(num)] = {'step': step, 'name': name}
    if sorted(bounds) != ['1', '2', '3', '4']:
        raise ValueError(f'단계 표지 1–4 가 하나씩이 아니다: {sorted(bounds)} · {prob}')
    if not bounds['1']['step'] < bounds['2']['step'] < bounds['3']['step'] < bounds['4']['step']:
        raise ValueError(f'단계 경계 순서 {bounds}')
    for b in seg['blocks']:
        if len(b['cols']) < 2 or b['cols'][1] != 'Atoms':
            prob.append(f'thermo 머리 {b["cols"]} — 둘째 열이 Atoms 가 아니다')
    rows, ke = [], {}
    for b in seg['blocks']:
        kc = b['cols'].index('KinEng') if 'KinEng' in b['cols'] else None
        for i, (step, vals) in enumerate(b['rows']):
            if kc is not None:
                ke.setdefault(step, (int(vals[1]), vals[kc]))
            if i == 0:
                continue                                   # 설정 줄 (run 마다 첫 줄) 버림 — compaction_curve 와 같은 규칙
            rows.append({'step': step, 'atoms': int(vals[1]), 'short': len(b['rows']) <= CC.SHORT_BLOCK_ROWS,
                         'p_deck': vals[b['pcol']] if b['pcol'] is not None else None})
    for r in rows:
        r['phase'] = CC._phase_at(bounds, r['step'])
    st = [r['step'] for r in rows]
    if any(s2 <= s1 for s1, s2 in zip(st, st[1:])):
        prob.append('C6 step 이 엄격히 증가하지 않는다')
    nopc = [r['step'] for r in rows if r['phase'] >= 2 and r['p_deck'] is None and not r['short']]
    if nopc:
        prob.append(f'C1 단계 ≥ 2 thermo 에 압력 열이 없다 (step {nopc[0]} 외 {len(nopc) - 1})')
    bad = [r['step'] for r in rows if r['p_deck'] is not None and not math.isfinite(r['p_deck'])]
    if bad:
        prob.append(f'C1 비유한 압력 {len(bad)} 줄 (첫 step {bad[0]})')
    b3, b4 = bounds['3']['step'], bounds['4']['step']
    judges = []
    for step, x, t, blk in seg['judges']:
        p = next((v[blk['pcol']] for s, v in blk['rows'] if s == step), None) if blk and blk['pcol'] is not None else None
        if step is None or x is None or t is None or p is None or not (math.isfinite(x) and math.isfinite(p)):
            prob.append(f'C4 판정 줄 (step {step}) 을 thermo 와 대조할 수 없다')
        elif abs(x - p) > 1e-12 + CC.JUDGE_REL * max(abs(x), abs(p)):
            prob.append(f'C4 판정 줄 {x!r} ≠ thermo {p!r} (step {step})')
        judges.append((step, x, t))
    if not judges:
        prob.append('C4 판정 줄이 없다')
    else:
        if {t for _, _, t in judges} != {target_deck}:
            prob.append(f'C4 판정 목표 {sorted({str(t) for _, _, t in judges})} ≠ 덱 target_press {target_deck}')
        if judges[-1][1] is None or judges[-1][1] < target_deck or any(x is None or x >= target_deck for _, x, _ in judges[:-1]):
            prob.append('C4 마지막 판정 줄만 목표 이상이어야 한다 (루프 탈출 규칙)')
        if judges[-1][0] != b4:
            prob.append(f'C4 PHASE 4 표지 step {b4} ≠ 루프 탈출 판정 줄 step {judges[-1][0]}')
        want = list(range(b3 + loop_run_steps, b4 + 1, loop_run_steps))
        if [s for s, _, _ in judges] != want or (b4 - b3) % loop_run_steps:
            prob.append(f'압축 run 이 {loop_run_steps} step 씩 이어지지 않는다 (판정 줄 {len(judges)} · 기대 {len(want)})')
    rs = seg['restarts']
    d = re.findall(r'(\d+)', Path(rs[0]).name) if rs else []
    if len(rs) != 1 or not d or int(d[-1]) != seg['first']:
        prob.append(f'read_restart {rs} 의 step ≠ 첫 thermo step {seg["first"]}')
    if prob:
        raise ValueError(' | '.join(prob))
    return {'rows': rows, 'bounds': bounds, 'judges': judges, 'ke': ke, 'first_step': seg['first'], 'last_step': seg['last'],
            'read_restart': rs[0], 'n_blocks': len(seg['blocks'])}


# ───────────────────────────── 판 궤적 · 속도 · 압력 ─────────────────────────────
def plate_model(b2, b3, b4, end, z0_deck, speed, dt):
    """판 높이 (덱 m) 함수 — [b2, b3] 고정 · (b3, b4] 등속 하강 · (b4, end] 고정.  판 놓기 전 · 끝 뒤 step = ValueError."""
    if not (b2 < b3 < b4 < end):
        raise ValueError(f'단계 경계 순서 {b2} {b3} {b4} {end}')

    def z(step):
        if step < b2 or step > end:
            raise ValueError(f'step {step} 은 판이 있는 구간 [{b2}, {end}] 밖')
        return z0_deck - speed * dt * (min(max(step, b3), b4) - b3)
    return z


def check_plate_end(z_end_deck, mesh_end_um, um_per_deck_m, half_ulp_deck=STL_HALF_ULP_DECK):
    """계산한 끝 판 높이 ↔ mesh_end (6 유효숫자) — (잔차 µm, 허용 µm).  반올림 반폭 밖이면 ValueError."""
    res_um = z_end_deck * um_per_deck_m - mesh_end_um
    tol_um = half_ulp_deck * um_per_deck_m * 1.0001
    if not abs(res_um) <= tol_um:
        raise ValueError(f'계산 끝 판 높이 {z_end_deck * um_per_deck_m:.6f} µm ≠ mesh_end {mesh_end_um} µm (잔차 {res_um:+.6f} > ±{tol_um:.6f})')
    return res_um, tol_um


def thickness_series(zfn, bnd, every, ms_per_step, um_per_deck_m):
    """판 위치 (ms, µm, 출처) — 메시 덤프 step (every 마다 · 클러스터 mesh_<step>.stl 과 같은 자리) + 단계 모서리 넷."""
    b2, b3, b4, end = bnd
    corner = {b2: SRC['placed'], b3: SRC['c_start'], b4: SRC['stop'], end: SRC['end']}
    grid = set(range((b2 // every + 1) * every, end + 1, every)) | set(corner)

    def src(s):
        if s in corner:
            return corner[s]
        return SRC['stab'] if s < b3 else (SRC['comp'] if s < b4 else SRC['relax'])
    return [(s * ms_per_step, zfn(s) * um_per_deck_m, src(s)) for s in sorted(grid)]


def velocity_series(bnd, v_um_s, ms_per_step):
    """계단 선 7 점 (ms, µm/s, 출처) — 판 없음 0 · 판 놓음 · 압축 시작에서 0 → v · 판 정지에서 v → 0 · 런 끝."""
    b2, b3, b4, end = (s * ms_per_step for s in bnd)
    return [(0.0, 0.0, SRC['noplate']), (b2, 0.0, SRC['placed']), (b3, 0.0, SRC['stab']), (b3, v_um_s, SRC['c_start']),
            (b4, v_um_s, SRC['stop']), (b4, 0.0, SRC['relax']), (end, 0.0, SRC['end'])]


def pressure_series(rows, mpa_per_deck, ms_per_step):
    """(step, MPa) 원값 + (ms, MPa, 출처) 그림 점 — (0 ms, 0 MPa, 판 없음) 하나 + 단계 ≥ 2 thermo 원값.
    판을 놓은 뒤 첫 압력은 0 이어야 한다 (판은 맨 위 입자 위 틈을 두고 놓인다 — 아니면 거부)."""
    px = [(r['step'], r['p_deck'] * mpa_per_deck) for r in rows if r['phase'] >= 2 and r['p_deck'] is not None]
    if not px or px[0][1] != 0.0:
        raise ValueError(f'판을 놓은 뒤 첫 압력이 0 이 아니다: {px[:1]}')
    return px, [(0.0, 0.0, SRC['noplate'])] + [(s * ms_per_step, p, SRC['thermo']) for s, p in px]


# ───────────────────────────── 3D 단계 프레임 ─────────────────────────────
def dump_steps(b3, end, every):
    """압축 시작 (b3) 뒤 atom 덤프 step — every 의 배수 (설정 줄 step 이 배수가 아니면 그 자리에는 안 쓴다) + 끝 덤프 (atom_end · 끝 step)."""
    return list(range((b3 // every + 1) * every, end + 1, every)) + ([end] if end % every else [])


def stage_table(px, bounds, dumps, end, zfn, um_per_deck_m, atoms_at, ms_per_step, p_stage=STAGE_P_MPA):
    """오른쪽 3D 네 단계 → 사건 step · 가장 가까운 atom 덤프 (같은 거리면 뒤) · 반대쪽 덤프 · 사건과 같은 단계의 가장 가까운 덤프 (권고).
    사건: Initial compression = 압축 시작 (PHASE 3 경계) · 50 MPa = 압축 중 압력이 처음 p_stage 이상인 thermo 줄 · 300 MPa = 판 정지
    (PHASE 4 경계 = 루프 탈출) · After relaxation = 런 끝.  ValueError = 압축 중 p_stage 에 닿지 않음."""
    b3, b4 = bounds['3']['step'], bounds['4']['step']
    pmap = dict(px)
    c50 = next((s for s, p in px if b3 < s <= b4 and p >= p_stage), None)
    if c50 is None:
        raise ValueError(f'압축 중 {p_stage:g} MPa 에 닿은 thermo 줄이 없다')
    events = [('initial_compression', 'Initial compression', b3, 3), ('p50', f'{p_stage:g} MPa', c50, 3),
              ('p300_stop', '300 MPa (plate stop)', b4, 3), ('after_relaxation', 'After relaxation', end, 4)]

    def info(s):
        return {'step': s, 'ms': s * ms_per_step, 'phase': CC._phase_at(bounds, s), 'pressure_mpa': pmap.get(s),
                'plate_um': zfn(s) * um_per_deck_m, 'atoms': atoms_at.get(s)}
    out = []
    for key, label, ev, ev_phase in events:
        near = min(dumps, key=lambda d: (abs(d - ev), -d))
        other = [d for d in dumps if (d - ev) * (near - ev) < 0]
        other = min(other, key=lambda d: abs(d - ev)) if other else None
        same = [d for d in dumps if CC._phase_at(bounds, d) == ev_phase]
        rec = min(same, key=lambda d: (abs(d - ev), -d)) if same else None
        out.append({'stage': key, 'label': label, 'event': info(ev), 'event_phase': ev_phase,
                    'nearest': dict(info(near), delta_steps=near - ev),
                    'other_side': None if other is None else dict(info(other), delta_steps=other - ev),
                    'recommended': None if rec is None else dict(info(rec), delta_steps=rec - ev),
                    'nearest_is_same_phase': CC._phase_at(bounds, near) == ev_phase})
    return out


def dump_names(step, end, post_dir):
    if step == end:
        return f'{post_dir}/atom_end_{end}.liggghts', f'{post_dir}/mesh_end_{end}.stl'
    return f'{post_dir}/atom_{step}.liggghts', f'{post_dir}/mesh_{step}.stl'


def cluster_command(steps, end, post_dir, atoms_at, parent=RUN_PARENT, case=RUN_CASE, tag=TAR_TAG):
    """1저자가 클러스터에서 붙여 넣을 명령 (`bash -s` · 오류면 그 자리에서 멈춤 — 로그인 셸은 닫히지 않는다 · 주소 · 포트 없음).
    ① 같은 런인지 = 끝 묶음 atom_end · mesh_end sha256 (리포 기록) ② atom 덤프마다 머리 TIMESTEP · 원자 수 = 이 로그의 thermo ③ 크기 ·
    sha256 목록 + tgz (홈 폴더에 씀 · 런 폴더는 읽기만 · 묶음 안 경로 = `<case>/post_…/…` — 끝 묶음과 같은 꼴)."""
    files = [f'{case}/{f}' for s in steps for f in dump_names(s, end, post_dir)]
    a_end, m_end = (f'{case}/{f}' for f in dump_names(end, end, post_dir))
    chk = '\n'.join(f'check {case}/{dump_names(s, end, post_dir)[0]} {s} {atoms_at[s]}' for s in steps)
    return ("bash -s <<'EOF'\nset -euo pipefail\n"
            f'cd "{parent}"   # D1 런 폴더 = {parent}/{case} (리포 기록: docs/data/kg50_decks_20261027_v3_b50/README.md §3)\n'
            f'printf "%s  %s\\n" {ATOM_END_SHA256} {a_end} {MESH_END_SHA256} {m_end} | sha256sum -c -   # 같은 런 (끝 묶음 기록)\n'
            'check() { t=$(sed -n 2p "$1"); n=$(sed -n 4p "$1"); [ "$t" = "$2" ] && [ "$n" = "$3" ] || '
            '{ echo "STOP $1: TIMESTEP $t atoms $n (expected $2 $3)"; exit 1; }; }\n'
            f'{chk}\n'
            f'F="{" ".join(files)}"\n'
            'ls -l $F\n'
            f'sha256sum $F > "$HOME/{tag}.sha256"\n'
            f'tar czf "$HOME/{tag}.tgz" $F\n'
            f'sha256sum "$HOME/{tag}.tgz" "$HOME/{tag}.sha256"\n'
            'EOF')


# ───────────────────────────── 압력 슬라이드판 (ps73 README §5 선례 — 이완 = 모식 감쇠) ─────────────────────────────
def slide_series(px, b4, end, ms_per_step, tau_step=None):
    """ps73 `make_fig_ms.slide_series` 와 같은 식 — 판 정지 (b4) 까지 thermo 원값 · 그 뒤 p_end + (p_c − p_end)·exp(−(s − b4)/τ) 를
    1,000 step 마다 (τ = 15,000 step = 그림용 · 자료에서 정한 값 아님 · 끝 값 p_end 만 계산값).  원값판은 따로 둔다 (`pressure_series`).
    ps73 보다 엄격한 곳 하나: 마지막 압력 줄 = 런 끝 · 정지 → 끝 = 1,000 step 의 배수 (모식 마지막 점이 런 끝에 선다) — 아니면 거부.
    → ([(ms, MPa, 출처)], [(step, 모식 MPa)])."""
    tau = SLIDE_TAU_STEP if tau_step is None else tau_step
    comp = [(s, p) for s, p in px if s <= b4]
    if not comp or comp[-1][0] != b4:
        raise ValueError('판 정지 step 의 압력 줄이 없다')
    if px[-1][0] != end:
        raise ValueError(f'마지막 압력 줄 step {px[-1][0]} ≠ 런 끝 {end}')
    if end <= b4 or (end - b4) % 1000:
        raise ValueError(f'판 정지 {b4} → 런 끝 {end} 이 1,000 step 의 배수가 아니다 (모식 마지막 점이 런 끝에 서지 않는다)')
    p_c, p_end = comp[-1][1], px[-1][1]
    sch = [(s, p_end + (p_c - p_end) * math.exp(-(s - b4) / tau)) for s in range(b4 + 1000, end + 1, 1000)]
    return ([(0.0, 0.0, SRC['noplate'])] + [(s * ms_per_step, p, SRC['thermo']) for s, p in comp]
            + [(s * ms_per_step, p, SRC_SCHEMATIC) for s, p in sch]), sch


# ───────────────────────────── 원자 기준 두께 (클러스터 CSV — 1저자 11-02 밤 · README §8) ─────────────────────────────
_AT_INT = ('step', 'dump_timestep', 'n_header', 'n_rows', 'n_bad_lines', 'bytes')
_AT_FLT = ('ztop_um', 'zc_max_um', 'ztop_radius_um', 'ztop_p999_um')
_AT_SRC = {'replay': SRC_REPLAY, 'checkpoint': SRC_CKPT, 'atom dump': SRC_DUMP}


def require_atomtop(path):
    """정착 (Particle packing) 구간은 원자 위치에서만 그린다 — CSV 가 없으면 거부 (모형 곡선 · 판 높이 · 덱 투입 높이로 지어내지 않는다)."""
    if path is None or not Path(path).is_file():
        raise ValueError(f'원자 기준 두께 CSV 가 없다 ({path}) — 정착 구간을 지어내지 않는다.  README §8 의 명령으로 D1 런 기계에서 만든 '
                         f'kg50_d1_atomtop.csv 를 {rel(ATOMTOP_CSV)} 에 넣은 뒤 다시 돌린다')
    return Path(path)


def read_atomtop(path):
    """클러스터 CSV → (행들, 메타).  머리 = 클러스터 스크립트 HEAD · 끝의 `#insertion` · `#insertion_orig` · `#sha256` 줄 = 메타 (겹치면 거부)."""
    with open(path, newline='', encoding='utf-8') as f:
        rd = csv.reader(f)
        head = next(rd, None)
        if head != ATOMTOP_HEAD:
            raise ValueError(f'원자 기준 두께 CSV 머리가 다르다: {head}')
        rows, meta = [], {'sha256': {}}
        for r in rd:
            if not r:
                continue
            if r[0].startswith('#'):
                key = r[0][1:]
                if key in ('mode', 'insertion', 'insertion_orig', 'script_sha256') and len(r) == 2 and key not in meta:
                    meta[key] = r[1]
                elif key == 'sha256' and len(r) == 3 and r[1] not in meta['sha256']:
                    meta['sha256'][r[1]] = r[2]
                else:
                    raise ValueError(f'메타 줄을 모르거나 겹친다: {r[:2]}')
                continue
            if len(r) != len(head):
                raise ValueError(f'열 수 {len(r)} ≠ {len(head)}: {r[:2]}')
            d = dict(zip(head, r))
            try:
                for k in _AT_INT:
                    d[k] = int(d[k])
                for k in _AT_FLT:
                    d[k] = float(d[k])
            except ValueError as e:
                raise ValueError(f'step {d.get("step")}: 숫자가 아니다 ({e})') from None
            if not all(math.isfinite(d[k]) for k in _AT_FLT):
                raise ValueError(f'step {d["step"]}: 비유한 값')
            rows.append(d)
    return rows, meta


def _int_or_none(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _ke_same(a, b):
    try:
        fa, fb = float(a), float(b)
    except (TypeError, ValueError):
        return False
    return math.isfinite(fa) and math.isfinite(fb) and abs(fa - fb) <= KE_RTOL * abs(fb)


def check_atomtop(rows, meta, main_ke, radii_um, ms_per_step=1e-3, replay_ref=None, sha_ref=None, script_ref=None):
    """ps73 `check_scan` · `check_early` 의 D1 판 — 문제 목록 (빈 목록 = 통과).
    ① step = 계획 (재현 1 · 1,000 → 체크포인트 → 원 atom 덤프) 그대로 · 출처 열 · time_ms = step × dt  ② 덤프 TIMESTEP = step
    ③ 머리 원자 수 = 줄 · 깨진 줄 0  ④ 원 덤프 파일 시각이 step 순서 (궤적 잇기)  ⑤ 재현 · 체크포인트 덤프 원자 수 = 그 런 로그 ·
    원 덤프 원자 수 = 본 로그 그 step  ⑥ p99.9 ≤ 윗면 · 중심 ≤ 윗면  ⑦ 맨 위 입자 반경 = 덱 반경
    ⑧ KE (상대 1e-6) — 재현 = 원 삽입 로그 (같은 궤적) · 체크포인트 = 본 로그 (원 런 상태) · 클러스터가 읽은 원 로그 값 = 리포 기록
    ⑨ 재현 · 원 삽입 줄 = 168,457 개 · 질량 9.557438e-01  ⑩ 런 폴더 파일 sha256 = 리포 기록 (같은 런)
    ⑪ CSV 를 만든 스크립트 sha256 = 리포의 cluster/d1_atomtop_cluster.py.
    원자 수 감소 · 맨 위가 판보다 높은 것 = 거부가 아니라 기록 (원자 기준 값 그대로 · ps73 1저자 *"하나의 기준"*).
    replay_ref · sha_ref · script_ref = 시험용 (기본 = 리포 기록 REPLAY_REF · ATOMTOP_SHA · 리포 클러스터 스크립트 sha256)."""
    replay_ref = REPLAY_REF if replay_ref is None else replay_ref
    sha_ref = ATOMTOP_SHA if sha_ref is None else sha_ref
    script_ref = sha256_file(HERE / 'cluster' / 'd1_atomtop_cluster.py') if script_ref is None else script_ref
    prob = []
    mode = meta.get('mode')
    if mode not in ('ckpt', 'replay'):
        prob.append(f'⑫ #mode {mode!r} — ckpt (기본 · 재현 없음) 또는 replay 여야 한다')
    steps = [int(r['step']) for r in rows]
    want = (ATOMTOP_EARLY if mode == 'replay' else CKPT_STEPS) + ATOMTOP_DUMPS
    if steps != want:
        prob.append(f'① step 목록 ≠ 계획 (빠짐 {sorted(set(want) - set(steps))[:5]} · 남음 {sorted(set(steps) - set(want))[:5]} · '
                    f'중복 {len(steps) - len(set(steps))})')
    for r in rows:
        s, n = int(r['step']), int(r['n_header'])
        kind = 'replay' if s in replay_ref else ('checkpoint' if s in ATOMTOP_EARLY else 'atom dump')
        if r['source'] != kind:
            prob.append(f'① {s}: 출처 {r["source"]!r} ≠ {kind!r}')
        if str(r['time_ms']) != f'{s * ms_per_step:.3f}':
            prob.append(f'① {s}: time_ms {r["time_ms"]} ≠ step × dt')
        if int(r['dump_timestep']) != s:
            prob.append(f'② {s}: 덤프 TIMESTEP {r["dump_timestep"]}')
        if n != int(r['n_rows']) or int(r['n_bad_lines']):
            prob.append(f'③ {s}: 원자 수 머리 {n} · 줄 {r["n_rows"]} · 깨진 줄 {r["n_bad_lines"]}')
        zt, zc, zp = float(r['ztop_um']), float(r['zc_max_um']), float(r['ztop_p999_um'])
        if not (zp <= zt and zc <= zt):
            prob.append(f'⑥ {s}: p99.9 {zp} · 중심 {zc} · 윗면 {zt}')
        if not any(abs(float(r['ztop_radius_um']) - v) <= 1e-9 * max(1.0, v) for v in radii_um):
            prob.append(f'⑦ {s}: 맨 위 입자 반경 {r["ztop_radius_um"]} µm ∉ 덱 반경 {sorted(radii_um)}')
        if kind == 'atom dump':
            ref = main_ke.get(s)
            if ref is None or int(ref[0]) != n:
                prob.append(f'⑤ {s}: 원 덤프 원자 수 {n} ≠ 본 로그 {ref[0] if ref else "없음"}')
            continue
        ref = replay_ref.get(s) if kind == 'replay' else main_ke.get(s)
        if _int_or_none(r['run_log_atoms']) != n:
            prob.append(f'⑤ {s}: 덤프 원자 수 {n} ≠ 그 런 로그 {r["run_log_atoms"]}')
        if ref is None:
            prob.append(f'⑧ {s}: 참고 KE 없음')
            continue
        if not _ke_same(r['run_log_ke'], ref[1]):
            prob.append(f'⑧ {s}: KE {r["run_log_ke"]} ≠ 원 로그 {ref[1]}')
        if not _ke_same(r['orig_log_ke'], ref[1]) or _int_or_none(r['orig_log_atoms']) != int(ref[0]):
            prob.append(f'⑧ {s}: 클러스터가 읽은 원 로그 ({r["orig_log_atoms"]} · {r["orig_log_ke"]}) ≠ 리포 기록 ({ref[0]} · {ref[1]})')
        if int(ref[0]) != n:
            prob.append(f'⑧ {s}: 원자 수 {n} ≠ 원 로그 {ref[0]}')
    dumps = [r for r in rows if r['source'] == 'atom dump']
    back = [(int(a['step']), a['mtime'], b['mtime']) for a, b in zip(dumps, dumps[1:]) if b['mtime'] < a['mtime']]
    if back:
        prob.append(f'④ 원 덤프 파일 시각이 거꾸로 가는 곳 {len(back)} — 처음 {back[:3]}')
    for key in (('insertion', 'insertion_orig') if mode == 'replay' else ('insertion_orig',)):
        line = meta.get(key) or ''
        if not all(x in line for x in INSERT_REF):
            prob.append(f'⑨ {key} 줄이 원 삽입 기록과 다르다: {line!r}')
    if mode != 'replay' and 'insertion' in meta:
        prob.append('⑨ 재현 없는 판 (#mode ckpt) 에 재현 삽입 줄이 있다')
    if meta.get('sha256') != sha_ref:
        prob.append(f'⑩ 런 폴더 sha256 ≠ 리포 기록: {meta.get("sha256")}')
    if meta.get('script_sha256') != script_ref:
        prob.append(f'⑪ CSV 를 만든 스크립트 sha256 {meta.get("script_sha256")} ≠ 리포 cluster/d1_atomtop_cluster.py')
    return prob


def atomtop_series(rows, ms_per_step=1e-3, interp=True, drop=None):
    """(ms, µm, 출처) — 원자 기준 하나 (ps73 `thickness_series` 와 같은 규칙): 재현 → 체크포인트 → 원 덤프 (값 = max(z + r)) ·
    앞 구간 (첫 점 → 첫 원 덤프) 만 측정점 사이를 PCHIP 로 1 ms 마다 채운다 (채운 점 = 측정 아님 · 출처 열에 표시).
    drop = 뺄 step (기본 없음) — 그 점이 외톨이 (윗면 − p99.9 ≥ 20 µm) 일 때만 빼고 아니면 거부한다."""
    drop = drop or {}
    have = {int(r['step']) for r in rows}
    if set(drop) - have:
        raise ValueError(f'뺄 점이 자료에 없다: {sorted(set(drop) - have)}')
    for r in rows:
        if int(r['step']) in drop and float(r['ztop_um']) - float(r['ztop_p999_um']) < OUTLIER_MIN_UM:
            raise ValueError(f'뺄 점 {r["step"]} 이 외톨이가 아니다 (윗면 − p99.9 = {float(r["ztop_um"]) - float(r["ztop_p999_um"]):.3f} µm)')
    out = []
    for r in rows:
        s = int(r['step'])
        if s in drop:
            continue
        if r['source'] not in _AT_SRC:
            raise ValueError(f'{s}: 모르는 출처 {r["source"]!r}')
        out.append((s, float(r['ztop_um']), _AT_SRC[r['source']]))
    if interp:
        n_knot = sum(1 for p in out if p[2] != SRC_DUMP) + 1
        if not 2 <= n_knot <= len(out):
            raise ValueError('앞 구간 매듭이 모자란다 (재현 · 체크포인트 · 첫 원 덤프)')
        knots = out[:n_knot]
        every = round(INTERP_DT_MS / ms_per_step)
        known = {s for s, _, _ in knots}
        s0, s1 = knots[0][0], knots[-1][0]
        q = [k * every for k in range(s0 // every + 1, s1 // every + 1) if s0 < k * every < s1 and k * every not in known]
        vals = PS73.pchip([s * ms_per_step for s, _, _ in knots], [z for _, z, _ in knots], [s * ms_per_step for s in q])
        out = sorted(out + [(s, v, SRC_INTERP) for s, v in zip(q, vals)], key=lambda p: p[0])
    ser = [(s * ms_per_step, z, src) for s, z, src in out]
    if any(b[0] <= a[0] for a, b in zip(ser, ser[1:])):
        raise ValueError('두께 점의 시각이 엄격히 증가하지 않는다')
    return ser


def free_fall_h(t_ms, h20_um, t20_ms, g, v0, um_per_m):
    """정착 구간 첫 측정점 (t20 · h20) 에서 거꾸로 이은 윗면 높이 — 감쇠 무시 자유 낙하 (1저자 11-02 밤 *"10g 로 그린 다음 이으면"*):
    h(t) = h20 + v0·(t20 − t) + ½·g·(t20² − t²)  (덱 단위 — t s · v0 m/s · g m/s² · 길이 덱 m → µm).  t = t20 이면 정확히 h20."""
    t, t20 = t_ms * 1e-3, t20_ms * 1e-3
    return h20_um + (v0 * (t20 - t) + 0.5 * g * (t20 * t20 - t * t)) * um_per_m


def free_fall_series(h20_um, t20_ms, g, v0, um_per_m, dt_ms=INTERP_DT_MS):
    """0 ms 부터 dt 마다 t20 앞까지 (t20 = 측정점이라 뺀다) 모식 점 (ms, µm, 출처 = 모식)."""
    return [(k * dt_ms, free_fall_h(k * dt_ms, h20_um, t20_ms, g, v0, um_per_m), SRC_FREEFALL)
            for k in range(int(t20_ms // dt_ms) + 1) if k * dt_ms < t20_ms]


def free_fall_check(h0_um, region_top_um, r_max_um):
    """h(0) ↔ 투입 영역 위끝 (중심이 놓이는 한계) · 윗면 한계 (위끝 + 최대 반경) — 넘어도 자르지 않고 표지만 (1저자 11-02 밤)."""
    return {'h0_um': h0_um, 'region_top_um': region_top_um, 'h0_le_region_top': h0_um <= region_top_um,
            'surface_bound_um': region_top_um + r_max_um, 'h0_le_surface_bound': h0_um <= region_top_um + r_max_um, 'clipped': False}


def packing_series(rows, mode, ms_per_step, g, v0, um_per_m, drop=None):
    """원자 기준 한 곡선 — replay 판 = 측정 그대로 (atomtop_series) · ckpt 판 (기본) = 0 → 첫 체크포인트 (20,001) 를 자유 낙하 모식으로 앞에 잇는다."""
    ser = atomtop_series(rows, ms_per_step, drop=drop)
    if mode == 'replay':
        return ser
    if mode != 'ckpt' or not ser or ser[0][2] != SRC_CKPT:
        raise ValueError(f'#mode {mode!r} · 첫 점 {ser[:1]} — 기본판은 첫 측정점이 체크포인트여야 한다')
    return free_fall_series(ser[0][1], ser[0][0], g, v0, um_per_m) + ser


def deck_free_fall(insert_text, um_per_m):
    """삽입 덱 → 자유 낙하 모식의 상수 (중력 · 투입 초속 · 투입 영역 위끝) + 무시한 감쇠의 크기 (γ · 상별 m/γ · SE 감쇠 낙하 거리)."""
    body = '\n'.join(ln.split('#', 1)[0].rstrip() for ln in insert_text.splitlines())
    g = float(_one(rf'^\s*fix\s+gravi\s+all\s+gravity\s+({_NUM})\s+vector\s+0(?:\.0)?\s+0(?:\.0)?\s+-1(?:\.0)?\s*$', body, '중력'))
    vx, vy, vz = (float(v) for v in _one(rf'^\s*vel\s+constant\s+({_NUM})\s+({_NUM})\s+({_NUM})\s*&?\s*$', body, '투입 초속'))
    if vx != 0.0 or vy != 0.0 or vz >= 0.0:
        raise ValueError(f'투입 초속 {vx} {vy} {vz} — 아래 방향 하나여야 한다')
    zb = _one(rf'^\s*region\s+reg_mix\s+block\s+{_NUM}\s+{_NUM}\s+{_NUM}\s+{_NUM}\s+({_NUM})\s+({_NUM})\s+units\s+box\s*$', body, '투입 영역')
    gamma = float(_one(rf'^\s*fix\s+damp\s+all\s+viscous\s+({_NUM})\s*$', body, '감쇠'))
    rvar = {k: float(v) for k, v in re.findall(rf'^\s*variable\s+(r_\w+)\s+equal\s+({_NUM})\s*$', body, re.M)}
    tmpl = re.findall(r'^\s*fix\s+pts\d\s+all\s+particletemplate/sphere\s+\d+\s+atom_type\s+(\d)\s+density\s+constant\s+'
                      rf'({_NUM})\s+radius\s+constant\s+\$\{{(r_\w+)\}}', body, re.M)
    tau = {f'type{t}_r{rvar[rv] * um_per_m:g}um': (float(rho) * 4.0 / 3.0 * math.pi * rvar[rv] ** 3) / gamma for t, rho, rv in tmpl}
    return {'g': g, 'v0': -vz, 'region_z_um': [float(zb[0]) * um_per_m, float(zb[1]) * um_per_m], 'region_top_um': float(zb[1]) * um_per_m,
            'r_max_um': max(rvar[rv] for _, _, rv in tmpl) * um_per_m, 'gamma_viscous': gamma, 'tau_damp_s': tau}


def broken_ranges(series, b2_ms, tick=5.0):
    """끊긴 y 축 두 범위 ((위 아래끝, 위 위끝), (아래 아래끝, 아래 위끝)) — 아래 = 판 놓은 뒤 모든 점 (+ 위쪽 단계 이름 자리 10 µm) ·
    위 = 시작 (투입 높이) 을 담는 HI_SPAN_UM 높이 (같은 µm/높이 축척).  위 범위가 시작을 못 담거나 아래 범위와 겹치면 (끊을 틈 없음) 거부."""
    after = [z for t, z, _ in series if t >= b2_ms]
    if not series or not after:
        raise ValueError('판 놓은 뒤 두께 점이 없다')
    lo = (tick * math.floor((min(after) - 5.0) / tick), tick * math.ceil((max(after) + 10.0) / tick))
    hi1 = tick * math.ceil((max(z for _, z, _ in series) + 5.0) / tick)
    hi = (hi1 - HI_SPAN_UM, hi1)
    y0 = series[0][1]
    if not hi[0] < y0 < hi[1]:
        raise ValueError(f'시작 높이 {y0:.3f} µm 가 위 범위 {hi} 밖 (시작보다 높은 점이 있다)')
    if not hi[0] > lo[1]:
        raise ValueError(f'위 범위 {hi} 가 아래 범위 {lo} 와 겹친다 — 끊을 틈이 없다')
    return hi, lo


# ───────────────────────────── 대조 (초안 2) ─────────────────────────────
def crosscheck_draft2(metrics, curve_rows, ours):
    """초안 2 (make_fig_p2_aux.branches 경로) ↔ 이 생성기 — 같은 로그를 다른 코드로 읽은 값이 같아야 한다.  (문제 목록, 통계)."""
    prob, c = [], metrics.get('compaction', {})
    pairs = [('compress_start_step', ours['b3']), ('stop_step', ours['b4']), ('n_compress_runs', ours['n_runs']),
             ('plate_z0_um', ours['z0_um']), ('z_end_pred_um', ours['z_end_um']), ('z_end_mesh_um', ours['mesh_end_um']),
             ('p_t0minus_MPa', ours['p_stop']), ('p_relax_first_MPa', ours['p_relax_first']), ('p_end_MPa', ours['p_end']),
             ('n_load_rows', ours['n_load']), ('n_relax_rows', ours['n_relax'])]
    for k, v in pairs:
        if k not in c or not abs(float(c[k]) - float(v)) <= 1e-9 * max(1.0, abs(float(v))):
            prob.append(f'metrics {k} {c.get(k)} ≠ {v}')
    pz = dict(ours['px'])
    dz = dp = 0.0
    n = 0
    for r in curve_rows:
        s = int(r['step'])
        if s not in pz:
            prob.append(f'curve_D1 step {s} 이 이 곡선에 없다')
            continue
        n += 1
        d_p = abs(float(r['plate_pressure_MPa']) - pz[s])
        d_z = abs(float(r['plate_gap_um']) - ours['zfn_um'](s)) if r['branch'] == 'loading' else 0.0
        if not (math.isfinite(d_p) and math.isfinite(d_z)):          # max(0.0, nan) = 0.0 — NaN 이 조용히 사라지지 않게 줄마다 본다
            prob.append(f'curve_D1 step {s} 비유한 값')
            continue
        dp, dz = max(dp, d_p), max(dz, d_z)
    if n != ours['n_load'] + ours['n_relax']:
        prob.append(f'curve_D1 행 {n} ≠ 압축 + 이완 {ours["n_load"] + ours["n_relax"]}')
    if not (dz <= 1e-6 and dp <= 1e-6):
        prob.append(f'curve_D1 판 높이 최대 차 {dz:.3g} µm · 압력 최대 차 {dp:.3g} MPa')
    return prob, {'n_rows_compared': n, 'max_abs_plate_um': dz, 'max_abs_pressure_mpa': dp}


# ───────────────────────────── 산출 ─────────────────────────────
def write_origin_csv(path, head, units, rows):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, lineterminator='\n')    # LF 고정 (.gitattributes)
        w.writerow(head)
        w.writerow(units)
        w.writerows(rows)


def ogs_text(name, what, color, y_from, y_to, y_inc, ylabel, bounds_ms, target=None):
    """ps73 .ogs 와 같은 BML 서식 (바깥 틱 · 위/오른쪽 축선 · #404040 · 10 × 8 cm · Aptos 28 pt) — 단계 경계 점선 셋."""
    ax = ('layer.unit = 3; layer.width = 10; layer.height = 8;\n'
          'layer.x.color = color(64,64,64); layer.x.thickness = 1; layer.x.ticks = 10;\n'
          'layer.x.ticklength = 6; layer.x.tickthickness = 1; layer.x.mticklength = 3; layer.x.mtickthickness = 1;\n'
          'layer.x.label.font = font(Aptos); layer.x.label.pt = 28; layer.x.label.color = color(64,64,64);\n'
          'layer.y.color = color(64,64,64); layer.y.thickness = 1; layer.y.ticks = 10;\n'
          'layer.y.ticklength = 6; layer.y.tickthickness = 1; layer.y.mticklength = 3; layer.y.mtickthickness = 1;\n'
          'layer.y.label.font = font(Aptos); layer.y.label.pt = 28; layer.y.label.color = color(64,64,64);\n'
          'layer.x2.showAxes = 3; layer.x2.color = color(64,64,64); layer.x2.thickness = 1; layer.x2.ticks = 0; layer.x2.showLabels = 0;\n'
          'layer.y2.showAxes = 3; layer.y2.color = color(64,64,64); layer.y2.thickness = 1; layer.y2.ticks = 0; layer.y2.showLabels = 0;\n'
          f'layer.x.from = {X0:g}; layer.x.to = {X1:g}; layer.x.inc = {XTICK_MAJOR}; layer.x.minor = 1;\n'
          f'page.margincontrol = 1;\nlabel -xb {XLABEL};\n')
    vb = ''.join(f'draw -n b{i} -l -v {t:.3f}; b{i}.linetype = 3; b{i}.color = color(154,160,168);\n'
                 for i, t in enumerate(bounds_ms, start=2))
    tgt = f'draw -n tgt -l -h {target:g}; tgt.linetype = 2; tgt.color = color(64,64,64);\n' if target is not None else ''
    marks = ' · '.join(f'{t:.3f}' for t in bounds_ms)
    return (f'// {name}.ogs — 50kg D1 (kg50_d1_b50 · SE D50 1 µm) 압밀 곡선 ({what})\n'
            f'// 사용: {name}.csv 를 가져온 워크북을 활성으로 두고 Script Window 에 붙여 넣기 → Enter.\n'
            f'// 결과: 새 그래프 + BML 서식 · 단계 경계 점선 셋 ({marks} ms = 판 놓음 · 압축 시작 · 판 정지).  C 열 (Source) 은 그리지 않는다.\n'
            'string bk$ = %H;\n'
            'plotxy iy:=[%(bk$)]1!(1,2) plot:=200 ogl:=<new>;\n'
            f'set %C -c color({color}); set %C -w 1500;\n' + ax +
            f'layer.y.from = {y_from:g}; layer.y.to = {y_to:g}; layer.y.inc = {y_inc:g}; layer.y.minor = 1;\nlabel -yl {ylabel};\n' + vb + tgt)


def _mpl_setup():
    """미리보기 공통 서식 (ps73 서식 · 이 기계에 Aptos 가 없어 Liberation Sans — Origin 결과로 바꿔 끼운다)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family': 'Liberation Sans', 'font.size': 11, 'axes.edgecolor': GRAY, 'axes.labelcolor': GRAY,
                         'xtick.color': GRAY, 'ytick.color': GRAY, 'axes.linewidth': 1.0, 'xtick.direction': 'out',
                         'ytick.direction': 'out', 'xtick.major.size': 5, 'ytick.major.size': 5, 'xtick.minor.size': 2.5,
                         'ytick.minor.size': 2.5, 'xtick.minor.visible': True, 'ytick.minor.visible': True,
                         'axes.labelsize': 12, 'svg.hashsalt': 'd1ms', 'mathtext.fontset': 'custom',   # s⁻¹ (U+207B 없는 글꼴)
                         'mathtext.rm': 'Liberation Sans', 'mathtext.it': 'Liberation Sans:italic', 'mathtext.bf': 'Liberation Sans:bold',
                         'mathtext.sf': 'Liberation Sans', 'mathtext.cal': 'Liberation Sans', 'mathtext.tt': 'Liberation Mono'})
    if FIGSIZE:                                           # 슬라이드 칸 크기 = 1:1 로 붙이므로 글씨를 그 크기에 맞춘다
        plt.rcParams.update({'font.size': 9, 'axes.labelsize': 9.5, 'xtick.major.size': 4, 'ytick.major.size': 4,
                             'xtick.minor.size': 2, 'ytick.minor.size': 2})
    return plt


def _line_at(series, x):
    """점 사이 직선 (그린 선과 같다) 의 x 에서의 값."""
    ts, zs = [p[0] for p in series], [p[1] for p in series]
    k = max(i for i in range(len(ts) - 1) if ts[i] <= x) if x < ts[-1] else len(ts) - 2
    return zs[k] + (zs[k + 1] - zs[k]) * (x - ts[k]) / (ts[k + 1] - ts[k])


def _break_scale(lo, hi, gap=GAP_FRAC):
    """끊긴 y 축 변환 (matplotlib `function` 축척) — 아래 범위 → 0–1 · 끊긴 자리 → 1–1+gap · 위 범위 → 아래와 같은 µm/높이 축척."""
    import numpy as np
    (lo0, lo1), (hi0, hi1) = lo, hi
    span = lo1 - lo0
    k_hi = (HI_FRAC / (hi1 - hi0)) if HI_FRAC else 1.0 / span     # 위 범위 축척 (None = 아래와 같은 µm/높이)

    def fwd(y):
        y = np.asarray(y, dtype=float)
        return np.where(y <= lo1, (y - lo0) / span, np.where(y >= hi0, 1 + gap + (y - hi0) * k_hi, 1 + gap * (y - lo1) / (hi0 - lo1)))

    def inv(u):
        u = np.asarray(u, dtype=float)
        return np.where(u <= 1, lo0 + u * span, np.where(u >= 1 + gap, hi0 + (u - 1 - gap) / k_hi, lo1 + (u - 1) / gap * (hi0 - lo1)))
    return fwd, inv


def draw_preview(tser, vser, pser, bounds_ms, arrows, stem, ranges=None, start_arrow=None, outdir=None):
    """세 패널 왼쪽 열 미리보기 (ps73 서식 · 이 기계에 Aptos 가 없어 Liberation Sans — Origin 결과로 바꿔 끼운다).
    1저자 슬라이드 배치 (11-02): 단계 이름 가로 · Particle packing 왼쪽 위 (그 구간 자료 없음 → 화살표 없음) · Stabilization = 경계 바로 오른쪽 ·
    평평한 선 위 · Compression = 기운 선 위 · Relaxation = 끝 근처 + 빨간 화살표가 끝 구간을 아래로 가리킴 · 목표 300 MPa 점선 없음 · 압력 원값 그대로.
    arrows = [(x_tip, y_tip, x_tail, y_tail)] 데이터 좌표 — 자료가 있는 점만 가리킨다.
    ranges = 끊긴 y 축 ((위 범위), (아래 범위)) — 원자 기준 판 (두께 패널 하나에 두 범위 · 같은 µm/높이 축척 · 끊긴 자리 = 흰 띠 + 빗금 ·
    단계 이름 높이 = 이름 폭 안 곡선 최댓값 위) · start_arrow = 정착 시작 (첫 자료 점) 을 가리키는 빨간 화살표 (원자 기준 판만)."""
    plt = _mpl_setup()
    from matplotlib.ticker import FixedLocator, FuncFormatter, MultipleLocator
    if ranges is None:
        fig, axs = plt.subplots(3, 1, sharex=True, figsize=FIGSIZE or (4.3, 7.2))
    else:
        (hi0, hi1), (lo0, lo1) = ranges
        top = 1 + GAP_FRAC + (HI_FRAC if HI_FRAC else (hi1 - hi0) / (lo1 - lo0))   # 아래 범위 = 다른 두 패널과 같은 높이
        fig, axs = plt.subplots(3, 1, sharex=True, figsize=FIGSIZE or (4.3, 7.2 * (2 + top) / 3),
                                gridspec_kw={'height_ratios': [top, 1, 1]})
    b2, b3, b4 = bounds_ms
    nl = '\n' if FIGSIZE else ' '                       # 슬라이드 칸 = 패널이 낮아 y 이름 두 줄 (ps73 슬라이드 그림과 같다)
    spec = [(tser, 'thickness', 'Thickness (µm)', THICK_YLIM, 10),
            (vser, 'velocity', r'Plate velocity' + nl + r'(µm s$^{-1}$)', (0, 15), 5),
            (pser, 'pressure', 'Measured pressure' + nl + '(MPa)', (0, 330), 100)]
    for ax, (ser, key, ylabel, ylim, ystep) in zip(axs, spec):
        ax.tick_params(top=False, right=False, which='both')
        ax.plot([t for t, _, _ in ser], [y for _, y, _ in ser], '-', color=COLORS[key], lw=1.6)
        for t in bounds_ms:
            ax.axvline(t, color=LIGHT, lw=0.9, ls=':')
        if key == 'thickness' and ranges is not None:
            ax.set_yscale('function', functions=_break_scale((lo0, lo1), (hi0, hi1)))
            ax.set_ylim(lo0, hi1)
            half = ystep / 2
            if HI_FRAC:                                   # 좁힌 위 띠 = 20 µm 간격 큰 눈금만 (1저자 11-03 · 옛 ps73 그림처럼)
                grid = [k * half for k in range(math.ceil(lo0 / half), math.floor(lo1 / half) + 1)]
                hmaj = [k * 20.0 for k in range(math.ceil(hi0 / 20.0), math.floor(hi1 / 20.0) + 1)]
                ax.yaxis.set_major_locator(FixedLocator([y for y in grid if y % ystep == 0] + hmaj))
                ax.yaxis.set_minor_locator(FixedLocator([y for y in grid if y % ystep != 0]))
            else:
                grid = [k * half for r0, r1 in ((lo0, lo1), (hi0, hi1)) for k in range(math.ceil(r0 / half), math.floor(r1 / half) + 1)]
                ax.yaxis.set_major_locator(FixedLocator([y for y in grid if y % ystep == 0]))
                ax.yaxis.set_minor_locator(FixedLocator([y for y in grid if y % ystep != 0]))
        else:
            ax.set_ylim(*ylim)
            ax.yaxis.set_major_locator(MultipleLocator(ystep))
            ax.yaxis.set_minor_locator(MultipleLocator(ystep / 2))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _p: '0' if abs(y) < 1e-12 else f'{y:g}'))   # 보고 원칙 "0.0 → 0"
        ax.set_ylabel(ylabel)
    ax = axs[0]                                           # 단계 이름 · 화살표 = 두께 패널만 (모두 가로)
    ts = [t for t, _, _ in tser]

    def zline(x):                                         # 두께 선의 높이 (점 사이 직선 — 그린 선과 같다)
        return _line_at(tser, x)
    kw = dict(fontsize=9, color=LIGHT)
    mask = dict(boxstyle='square,pad=0.05', facecolor='white', edgecolor='none')   # 단계 경계 점선이 글 뒤로 가려진다 (글 ↔ 선 겹침 없음)
    st = ax.text(b2 + 15, zline(b2) + 0.8, 'Stabilization', ha='left', va='bottom', bbox=mask, zorder=3, **kw)   # 경계 바로 오른쪽 · 평평한 선 위
    xc = (b3 + b4) / 2
    cp = ax.text(xc, zline(xc - 300) + 1.5, 'Compression', ha='center', va='bottom', **kw)     # 기운 선 위 (글 왼쪽 끝에서도 선 위)
    rl = ax.text(X1 - 12, zline(ts[-1]) + 6.0, 'Relaxation', ha='right', va='bottom', bbox=mask, zorder=3, **kw)  # 끝 근처 · 아래 화살표
    arrowprops = dict(arrowstyle='-|>', color=RED, lw=1.2, shrinkA=0, shrinkB=1.5, mutation_scale=8)
    for x, y, xt, yt in arrows:
        ax.annotate('', xy=(x, y), xytext=(xt, yt), textcoords='data', arrowprops=arrowprops)
    sa = None if start_arrow is None else ax.annotate('', xy=start_arrow[:2], xytext=start_arrow[2:], textcoords='data', arrowprops=arrowprops)
    axs[-1].set_xlim(X0, X1)
    axs[-1].xaxis.set_major_locator(MultipleLocator(XTICK_MAJOR))
    axs[-1].xaxis.set_minor_locator(MultipleLocator(XTICK_MAJOR / 2))
    axs[-1].set_xlabel(XLABEL)
    fig.align_ylabels(axs)
    # Particle packing = 9 pt 가로 · 위 패널 테두리 위 (축 밖) · x = 0 ms 왼쪽 맞춤 (1저자 슬라이드 11-02) — 판 기준 그림 = 화살표 없음 (그 구간 자료 없음) ·
    # 원자 기준 그림 = start_arrow 가 첫 자료 점 (재현 step 1) 을 가리킨다
    pk = ax.annotate('Particle packing', xy=(X0, 1.0), xycoords=('data', 'axes fraction'), xytext=(0, 3), textcoords='offset points',
                     ha='left', va='bottom', annotation_clip=False, **kw)
    fig.tight_layout(pad=0.4, h_pad=0.6)                  # 축 밖 이름 자리를 위 여백으로 잡는다 (그림 크기 그대로)
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    if ranges is not None:                                # 원자 기준 곡선은 평평하지 않다 — 이름 폭 안의 곡선 최댓값 위로 (이름 ↔ 곡선 겹침 없음)
        inv = ax.transData.inverted()
        for txt, gap_um in ((st, 0.8), (cp, 1.5), (rl, 6.0)):
            bb = txt.get_window_extent(r)
            xa, xb = sorted(inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y0)])[:, 0])
            inside = [z for t, z, _ in tser if xa <= t <= xb]
            txt.set_y(max([zline(min(max(xa, ts[0]), ts[-1])), zline(min(max(xb, ts[0]), ts[-1]))] + inside) + gap_um)
        import matplotlib.patches as mpatches
        u_lo, u_hi = 1.0 / top, (1.0 + GAP_FRAC) / top     # 끊긴 자리 (축 높이 몫)
        ax.add_patch(mpatches.Rectangle((-0.02, u_lo), 1.04, u_hi - u_lo, transform=ax.transAxes, facecolor='white', edgecolor='none',
                                        zorder=4, clip_on=False))
        for xe in (0.0, 1.0):
            for ue in (u_lo, u_hi):
                ax.plot([xe - 0.015, xe + 0.015], [ue - 0.012, ue + 0.012], transform=ax.transAxes, color=GRAY, lw=1.0, clip_on=False, zorder=5)
        fig.canvas.draw()
    boxes = {t.get_text(): t.get_window_extent(r) for t in (pk, st, cp, rl)}
    if boxes['Particle packing'].y0 < ax.get_window_extent(r).y1 or boxes['Particle packing'].y1 > fig.bbox.y1:
        raise ValueError('Particle packing 이름이 위 패널 테두리 위 (그림 안) 에 있지 않다')
    names = list(boxes)
    hit = [(a, c) for i, a in enumerate(names) for c in names[i + 1:] if boxes[a].overlaps(boxes[c])]
    if sa is not None:
        hit += [('start arrow', n) for n in names if sa.arrow_patch.get_window_extent(r).overlaps(boxes[n])]
    if hit:
        raise ValueError(f'단계 이름끼리 겹친다: {hit}')
    out = PREV if outdir is None else Path(outdir)
    fig.savefig(out / f'{stem}.png', dpi=300)
    fig.savefig(out / f'{stem}.svg', metadata={'Date': None})
    plt.close(fig)


def draw_preview_broken(tser, vser, pser, bounds_ms, ranges, stem, outdir=None):
    """원자 기준 판 (정착 구간 포함 · 끊긴 y 축) — 정착 시작 빨간 화살표 = 첫 자료 점 (투입 재현 step 1) 을 위 오른쪽에서 가리킨다 ·
    이완 화살표 = 이완 구간 가운데의 원자 기준 값을 위에서 가리킨다 (둘 다 자료 점 · 화살표 좌표를 돌려준다 → key JSON)."""
    (_, hi1), _ = ranges
    t0, y0 = tser[0][0], tser[0][1]
    start = (t0, y0, t0 + 170.0, y0 + 0.55 * (hi1 - y0))
    x_rel = (bounds_ms[2] + tser[-1][0]) / 2
    y_rel = _line_at(tser, x_rel)
    arrows = [(x_rel, y_rel, x_rel, y_rel + 5.6)]
    draw_preview(tser, vser, pser, bounds_ms, arrows, stem, ranges=ranges, start_arrow=start, outdir=outdir)
    return {'packing_start': list(start), 'relaxation_end_segment': list(arrows[0])}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rel(p):
    return Path(p).resolve().relative_to(ROOT).as_posix()


def free_fall_record(at, um):
    """key JSON atomtop.free_fall — 기본판 (ckpt) 만: 식 · 상수 · h(0) 대조 · 무시한 감쇠의 크기 (SE 감쇠 낙하 거리 어림)."""
    if at['meta']['mode'] != 'ckpt':
        return None
    ffp, ser = at['ffp'], at['ser']
    h20, t20 = next((t, z) for t, z, s in ser if s == SRC_CKPT)[::-1]
    g, v0, gam = ffp['g'], ffp['v0'], ffp['gamma_viscous']
    t20s = t20 * 1e-3
    damped = {}
    for k, tau in ffp['tau_damp_s'].items():           # 선형 끌림 v' = g − v/τ (v0 아래 방향) 의 t20 동안 낙하 ↔ 감쇠 없는 낙하
        vt = g * tau
        fall = vt * t20s + (v0 - vt) * tau * (1 - math.exp(-t20s / tau))
        damped[k] = {'tau_s': tau, 'fall_um_damped': fall * um, 'fall_um_undamped': (v0 * t20s + 0.5 * g * t20s ** 2) * um}
    return {'what': 'schematic (모식) — 0 → 20 ms drawn backwards from the first measured top (checkpoint 20,001) as a free fall; '
                    'not measured · marked only in CSV Source / README (not on the figure)',
            'formula': f'h(t) = {h20:.6g} + {v0:g}·({t20s:g} − t) + ½·{g:g}·({t20s:g}² − t²)  [deck units: s · m/s · m/s²; ×{um:g} µm per deck m]',
            'g_deck_m_s2': g, 'v0_deck_m_s': v0, 't20_ms': t20, 'h20_um_measured': h20, 'h0_um': ser[0][1], 'fall_um': ser[0][1] - h20,
            'check': at['ffcheck'], 'damping_neglected': {'fix_viscous_gamma': gam, 'per_phase': damped,
                                                          'note': 'fix viscous F = −γ·v on every particle — m/γ is short for SE (τ ≈ 0.09 s) '
                                                                  'so an SE top particle would fall less than the drawn curve; AM (τ ≈ 55 s) is undamped'},
            'source_label': SRC_FREEFALL}


def atomtop_summary(at, arrows, zfn, um):
    """원자 기준 두께 기록 (key JSON) — 측정 · 채움 수 · 끊긴 자리에 가려진 측정점 · 외톨이 후보 (빼지 않는다 — 1저자 결정) ·
    판과의 관계 (맨 위가 판에 닿은 첫 덤프 · 중심이 판 위인 덤프) · 원자 수 변화 · KE 대조."""
    rows, ser, ((h0, h1), (l0, l1)) = at['rows'], at['ser'], at['ranges']
    dumps = [r for r in rows if r['source'] == 'atom dump']
    plate = {r['step']: zfn(r['step']) * um for r in dumps}
    over = [(round(r['ztop_um'] - plate[r['step']], 3), r['step']) for r in dumps]
    esc = [r['step'] for r in dumps if r['zc_max_um'] > plate[r['step']]]
    counts = [[rows[0]['step'], rows[0]['n_header']]] + [[r2['step'], r2['n_header']] for r1, r2 in zip(rows, rows[1:])
                                                         if r2['n_header'] != r1['n_header']]
    return {
        'status': 'SUPPLIED — checks passed (check_atomtop ①–⑫)', 'mode': at['meta']['mode'],
        'csv_in': {'path': rel(ATOMTOP_CSV), 'sha256': sha256_file(ATOMTOP_CSV), 'run_folder_sha256': at['meta']['sha256'],
                   'insertion_line': at['meta'].get('insertion')},
        'definition': 'max(z + r) over all atoms (µm) — not filtered by the plate · one criterion from t = 0 (ps73 README §7)',
        'n_points': len(ser), 'n_measured': sum(1 for p in ser if p[2] in (SRC_REPLAY, SRC_CKPT, SRC_DUMP)),
        'n_interpolated': sum(1 for p in ser if p[2] == SRC_INTERP), 'n_schematic_free_fall': sum(1 for p in ser if p[2] == SRC_FREEFALL),
        'early_measured': [[r['step'], r['source'], r['ztop_um'], r['ztop_p999_um']] for r in rows if r['source'] != 'atom dump'],
        'first': list(ser[0]), 'end': list(ser[-1]),
        'ranges_um': {'upper': [h0, h1], 'lower': [l0, l1], 'scale': 'same µm per height in both ranges'},
        'hidden_in_break': {'measured': [[round(t, 3), round(z, 3), s] for t, z, s in ser
                                         if l1 < z < h0 and s in (SRC_REPLAY, SRC_CKPT, SRC_DUMP)],
                            'n_interpolated_or_schematic': sum(1 for _, z, s in ser if l1 < z < h0 and s in (SRC_INTERP, SRC_FREEFALL))},
        'free_fall': free_fall_record(at, um),
        'outlier_candidates_top_minus_p999_ge_20um': [[r['step'], round(r['ztop_um'] - r['ztop_p999_um'], 3)] for r in rows
                                                      if r['ztop_um'] - r['ztop_p999_um'] >= OUTLIER_MIN_UM],
        'outlier_note': 'not dropped — drawn as measured (ps73 dropped one bounced particle only after the 1st author asked)',
        'first_dump_top_reaches_plate': next((r['step'] for r in dumps if r['ztop_um'] >= plate[r['step']]), None),
        'dumps_top_center_above_plate': {'n': len(esc), 'first': esc[0] if esc else None},
        'max_top_minus_plate_um': list(max(over)) if over else None,
        'atom_count_changes': counts,
        'ke_checks': [[r['step'], r['source'], r['run_log_ke'], r['orig_log_ke']] for r in rows if r['source'] != 'atom dump'],
        'arrows': arrows, 'csv_out': f'origin/{CSV_AT}.csv', 'previews': [f'previews/{FIG_AT}.png', f'previews/{FIG_AT_SLIDE}.png']}


def main(require_packing=False):
    if sha256_file(LOG) != LOG_SHA256 or sha256_file(DECK) != DECK_SHA256:
        raise SystemExit(f'⛔ 로그 · 리포 덱 sha256 ≠ D1 README 기록 ({rel(LOG)} · {rel(DECK)})')
    readme = D1_README.read_text(encoding='utf-8')
    if not all(x in readme for x in (LOG_SHA256, DECK_SHA256, ATOM_END_SHA256, MESH_END_SHA256, MESH_END_TEXT)):
        raise SystemExit('⛔ D1 README 기록 (로그 · 덱 · atom_end · mesh_end sha256 · 끝 판 높이) 이 이 생성기의 상수와 다르다')
    try:
        dk = deck_settings(LOG.read_text(encoding='utf-8'))
        repo_dk = deck_settings(DECK.read_text(encoding='utf-8'))
        same = ('units', 'scale_r', 'scale_E', 'scale_P', 'dt_s', 'press_speed_deck_m_s', 'target_deck', 'area_deck_m2', 'r_am_p_deck',
                'plate_margin_deck', 'loop_run_steps', 'atom_dump_every', 'mesh_dump_every', 'post_dir')
        diff = [k for k in same if dk[k] != repo_dk[k]]
        if diff:
            raise ValueError(f'로그 안 덱 ↔ 리포 덱 설정 다름: {diff}')
        cv = read_curve(LOG, dk['target_deck'], dk['loop_run_steps'])
        ms_per_step, um, mpa = dk['dt_s'] * 1e3, dk['um_per_deck_m'], dk['mpa_per_deck_mpa']
        b = {k: v['step'] for k, v in cv['bounds'].items()}
        end = cv['last_step']
        bnd = (b['2'], b['3'], b['4'], end)
        meta = json.loads(METRICS.read_text(encoding='utf-8'))
        mesh_end_um = float(meta['compaction']['z_end_mesh_um'])
        if f'{mesh_end_um:.3f}' not in MESH_END_TEXT:
            raise ValueError(f'metrics_D1.json mesh_end {mesh_end_um} µm ≠ D1 README ({MESH_END_TEXT})')
        zfn = plate_model(*bnd, dk['plate_z0_deck'], dk['press_speed_deck_m_s'], dk['dt_s'])
        z_end = zfn(end)
        res_um, tol_um = check_plate_end(z_end, mesh_end_um, um)
        slope = (zfn(b['4']) - zfn(b['3'])) / ((b['4'] - b['3']) * dk['dt_s'])
        if not abs(-slope - dk['press_speed_deck_m_s']) <= SLOPE_REL * dk['press_speed_deck_m_s']:
            raise ValueError(f'판 궤적 기울기 {-slope} ≠ press_speed')
        tser = thickness_series(zfn, bnd, dk['mesh_dump_every'], ms_per_step, um)
        v_um_s = dk['press_speed_deck_m_s'] * um
        vser = velocity_series(bnd, v_um_s, ms_per_step)
        px, pser = pressure_series(cv['rows'], mpa, ms_per_step)
        atoms_at = {r['step']: r['atoms'] for r in cv['rows']}
        pmap = dict(px)
        load = [(s, p) for s, p in px if b['3'] < s <= b['4']]
        relax = [(s, p) for s, p in px if s > b['4']]
        ours = {'b3': b['3'], 'b4': b['4'], 'n_runs': len(cv['judges']), 'z0_um': dk['plate_z0_deck'] * um, 'z_end_um': z_end * um,
                'mesh_end_um': mesh_end_um, 'p_stop': pmap[b['4']], 'p_relax_first': relax[0][1], 'p_end': relax[-1][1],
                'n_load': len(load), 'n_relax': len(relax), 'px': px, 'zfn_um': lambda s: zfn(s) * um}
        with open(CURVE_D1, newline='', encoding='utf-8') as f:
            crow = list(csv.DictReader(f))
        xprob, xstat = crosscheck_draft2(meta, crow, ours)
        if xprob:
            raise ValueError('초안 2 대조 실패 — ' + ' | '.join(xprob[:6]))
        dumps = dump_steps(b['3'], end, dk['atom_dump_every'])
        stages = stage_table(px, cv['bounds'], dumps, end, zfn, um, atoms_at, ms_per_step)
        sser, sch = slide_series(px, b['4'], end, ms_per_step)
        # 원자 기준 두께 — 클러스터 스크립트의 계획 (step · sha256) 이 이 로그 · 덱과 같은지 (CSV 가 오기 전에도 확인한다)
        deck_body = '\n'.join(ln.split('#', 1)[0].rstrip() for ln in DECK.read_text(encoding='utf-8').splitlines())
        every_rs = int(_one(r'^\s*restart\s+(\d+)\s+\S+/restart_settling_\*\.bin\s*$', deck_body, '정착 restart 간격'))
        radii_um = {float(_one(rf'^\s*variable\s+{v}\s+equal\s+({_NUM})\s*$', deck_body, v)) * um for v in ('r_AM_P', 'r_AM_S', 'r_SE')}
        early_want = (sorted(REPLAY_REF) + [cv['first_step']] + list(range(every_rs, b['2'], every_rs)) + [b['2'] - 1]
                      + list(range((b['2'] // every_rs + 1) * every_rs, b['3'], every_rs)))
        if early_want != ATOMTOP_EARLY or dumps != ATOMTOP_DUMPS:
            raise ValueError(f'클러스터 스크립트 step 계획 ≠ 이 로그 · 덱 일정 ({early_want} · 덤프 {len(dumps)})')
        no_ke = [s for s in ATOMTOP_EARLY[len(REPLAY_REF):] + ATOMTOP_DUMPS if s not in cv['ke']]
        if no_ke:
            raise ValueError(f'본 로그에 KE · 원자 수 줄이 없는 step: {no_ke[:5]}')
        sha_repo = {'log.liggghts': LOG_SHA256, 'input_kg50_d1_b50.liggghts': DECK_SHA256,
                    'input_kg50_d1_b50_insert.liggghts': sha256_file(INSERT_DECK)}
        if any(ATOMTOP_SHA[k] != v for k, v in sha_repo.items()):
            raise ValueError('클러스터 스크립트 sha256 ≠ 리포 로그 · 덱')
        at = None
        if require_packing or ATOMTOP_CSV.is_file():
            require_atomtop(ATOMTOP_CSV)
            at_rows, at_meta = read_atomtop(ATOMTOP_CSV)
            at_prob = check_atomtop(at_rows, at_meta, cv['ke'], radii_um, ms_per_step)
            if at_prob:
                raise ValueError('원자 기준 두께 CSV 검사 실패 — ' + ' | '.join(at_prob[:6]))
            ffp = deck_free_fall(INSERT_DECK.read_text(encoding='utf-8'), um)
            aser = packing_series(at_rows, at_meta['mode'], ms_per_step, ffp['g'], ffp['v0'], um)
            at = {'rows': at_rows, 'meta': at_meta, 'ser': aser, 'ranges': broken_ranges(aser, b['2'] * ms_per_step), 'ffp': ffp,
                  'ffcheck': free_fall_check(aser[0][1], ffp['region_top_um'], ffp['r_max_um']) if at_meta['mode'] == 'ckpt' else None}
            if at['ffcheck'] and not at['ffcheck']['h0_le_region_top']:
                print(f'⚠ 자유 낙하 모식 h(0) {aser[0][1]:.3f} µm > 투입 영역 위끝 {ffp["region_top_um"]:g} µm — 자르지 않았다 '
                      f'(윗면 한계 = 위끝 + 최대 반경 {at["ffcheck"]["surface_bound_um"]:g} µm · key JSON atomtop.free_fall)')
        else:
            stale = [p for p in (ORIGIN / f'{CSV_AT}.csv', ORIGIN / f'{CSV_AT}.ogs', PREV / f'{FIG_AT}.png', PREV / f'{FIG_AT_SLIDE}.png')
                     if p.exists()]
            if stale:
                raise ValueError(f'원자 기준 산출물이 있는데 CSV ({rel(ATOMTOP_CSV)}) 가 없다 — 낡은 그림을 두지 않는다: {[rel(p) for p in stale]}')
    except ValueError as e:
        raise SystemExit(f'⛔ {e}')
    eps_d2 = {int(r['step']): float(r['eps_sphere_pct']) for r in crow}
    for st in stages:
        for role in ('event', 'nearest', 'other_side', 'recommended'):
            if st[role] is not None:
                st[role]['eps_sphere_pct_draft2'] = eps_d2.get(st[role]['step'])
                if role != 'event':
                    st[role]['atom_file'], st[role]['mesh_file'] = dump_names(st[role]['step'], end, dk['post_dir'])
    tar_steps = sorted({st[r]['step'] for st in stages for r in ('nearest', 'recommended') if st[r] is not None})
    cmd = cluster_command(tar_steps, end, dk['post_dir'], atoms_at)
    bounds_ms = [b['2'] * ms_per_step, b['3'] * ms_per_step, b['4'] * ms_per_step]
    x_rel = (b['4'] + end) / 2 * ms_per_step                         # 이완 구간 (판 고정) 가운데 — 화살표가 끝 구간을 아래로 가리킨다
    arrows = [(x_rel, zfn(end) * um, x_rel, zfn(end) * um + 5.6)]    # 투입 시작은 자료 없음 → 화살표 없음

    for p in (ORIGIN, PREV):
        p.mkdir(exist_ok=True)
    write_origin_csv(ORIGIN / f'{CSV_NAMES["thickness"]}.csv', ['Time', 'Thickness', 'Source'], ['ms', 'µm', ''],
                     [(f'{t:.3f}', f'{z:.4f}', s) for t, z, s in tser])
    write_origin_csv(ORIGIN / f'{CSV_NAMES["velocity"]}.csv', ['Time', 'Plate velocity', 'Source'], ['ms', 'µm/s', ''],
                     [(f'{t:.3f}', f'{v:g}', s) for t, v, s in vser])
    write_origin_csv(ORIGIN / f'{CSV_NAMES["pressure"]}.csv', ['Time', 'Measured pressure', 'Source'], ['ms', 'MPa', ''],
                     [(f'{t:.3f}', f'{p:.8g}', s) for t, p, s in pser])
    ogs = [('thickness', '시간 (ms)–두께 (판 위치 · 덱으로 계산)', *THICK_YLIM, 10, 'Thickness (\\g(m)m)'),
           ('velocity', '시간 (ms)–판 속도 · 덱 press_speed', 0, 15, 5, 'Plate velocity (\\g(m)m s\\+(-1))'),
           ('pressure', '시간 (ms)–판 압력 (thermo 원값)', 0, 330, 100, 'Measured pressure (MPa)')]   # 목표 점선 없음 (1저자 슬라이드)
    for key, what, y0, y1, yi, ylab in ogs:
        (ORIGIN / f'{CSV_NAMES[key]}.ogs').write_text(ogs_text(CSV_NAMES[key], what, OGS_RGB[key], y0, y1, yi, ylab, bounds_ms),
                                                      encoding='utf-8')
    draw_preview(tser, vser, pser, bounds_ms, arrows, FIG_NAME)
    # 압력 슬라이드판 (1저자 11-02 밤 *"pressure 도 저 진동 안 생기게"* — ps73 README §5 선례 · 원값판은 위에 그대로)
    write_origin_csv(ORIGIN / f'{CSV_SLIDE}.csv', ['Time', 'Measured pressure', 'Source'], ['ms', 'MPa', ''],
                     [(f'{t:.3f}', f'{p:.8g}', s) for t, p, s in sser])
    (ORIGIN / f'{CSV_SLIDE}.ogs').write_text(ogs_text(CSV_SLIDE, '시간 (ms)–판 압력 슬라이드판 (판 정지까지 thermo 원값 · 그 뒤 이완 = 모식 감쇠)',
                                                      OGS_RGB['pressure'], 0, 330, 100, 'Measured pressure (MPa)', bounds_ms), encoding='utf-8')
    draw_preview(tser, vser, sser, bounds_ms, arrows, FIG_SLIDE)
    at_arrows = None
    if at is not None:                                   # 원자 기준 두께 (정착 구간부터 한 곡선 · 끊긴 y 축) — 원값 압력판 · 슬라이드판
        (h0, h1), (l0, l1) = at['ranges']
        write_origin_csv(ORIGIN / f'{CSV_AT}.csv', ['Time', 'Thickness', 'Source'], ['ms', 'µm', ''],
                         [(f'{t:.3f}', f'{z:.3f}', s) for t, z, s in at['ser']])
        (ORIGIN / f'{CSV_AT}.ogs').write_text(
            ogs_text(CSV_AT, f'시간 (ms)–두께 (원자 기준 = 모든 원자의 max(z + r) · 0 ms 부터) · y 축 끊기 = GUI 한 번: Y 축 대화상자 Breaks 탭에서 '
                             f'끊기를 켜고 From {l1:g} To {h0:g}', OGS_RGB['thickness'], l0, h1, 10, 'Thickness (\\g(m)m)', bounds_ms),
            encoding='utf-8')
        at_arrows = draw_preview_broken(at['ser'], vser, pser, bounds_ms, at['ranges'], FIG_AT)
        draw_preview_broken(at['ser'], vser, sser, bounds_ms, at['ranges'], FIG_AT_SLIDE)
    with open(STAGE_CSV, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['stage', 'event_step', 'event_pressure_MPa', 'role', 'dump_step', 'delta_steps', 'dump_phase', 'pressure_MPa',
                    'plate_um', 'atoms', 'eps_sphere_pct_draft2', 'atom_file', 'mesh_file'])
        for st in stages:
            ev, seen = st['event'], set()
            for role in ('nearest', 'other_side', 'recommended'):
                d = st[role]
                if d is None:
                    continue
                if d['step'] in seen:                       # 권고 = 가장 가까운 것과 같으면 한 줄 (role 에 둘 다)
                    continue
                roles = [r for r in ('nearest', 'other_side', 'recommended') if st[r] is not None and st[r]['step'] == d['step']]
                seen.add(d['step'])
                w.writerow([st['stage'], ev['step'], f'{ev["pressure_mpa"]:.8g}', '+'.join(roles), d['step'], d['delta_steps'], d['phase'],
                            f'{d["pressure_mpa"]:.8g}', f'{d["plate_um"]:.4f}', d['atoms'],
                            '' if d['eps_sphere_pct_draft2'] is None else f'{d["eps_sphere_pct_draft2"]:.4f}', d['atom_file'], d['mesh_file']])

    on = {f'{t:g}': next(([s, p] for s, p in load if p >= t), None) for t in (0.1, 1.0, 10.0, 50.0, 100.0, 200.0, 300.0)}
    counts = [[cv['rows'][0]['step'], cv['rows'][0]['atoms']]] + [[r2['step'], r2['atoms']] for r1, r2 in zip(cv['rows'], cv['rows'][1:])
                                                                 if r2['atoms'] != r1['atoms']]
    ke_steps = sorted({cv['first_step'], b['2'] - 1} | set(range(50000, b['3'], 50000)))
    fnz = next(((s, p) for s, p in load if p != 0.0), None)      # 판이 침대에 처음 닿은 때 (압력 첫 0 아닌 thermo 줄)
    p_stop_v, p_end_v = pmap[b['4']], px[-1][1]
    key = {
        'what': '50kg D1 (kg50_d1_b50 · SE D50 1 µm) compaction curve — left column of the ps73-style slide (thickness · plate velocity · '
                'measured pressure) · stage frames for the right-side 3D pore renders',
        'generator': rel(Path(__file__)),
        'inputs': {'log': {'path': rel(LOG), 'sha256': LOG_SHA256}, 'deck_repo': {'path': rel(DECK), 'sha256': DECK_SHA256},
                   'd1_readme': rel(D1_README), 'draft2_metrics': rel(METRICS), 'draft2_curve': rel(CURVE_D1)},
        'deck': {k: dk[k] for k in ('units', 'scale_r', 'scale_E', 'scale_P', 'um_per_deck_m', 'mpa_per_deck_mpa', 'dt_s',
                                     'press_speed_deck_m_s', 'target_deck', 'target_mpa', 'area_deck_m2', 'box_xy_deck', 'r_am_p_deck',
                                     'plate_margin_deck', 'zmax_center_deck', 'plate_z0_deck', 'loop_run_steps', 'atom_dump_every',
                                     'mesh_dump_every', 'post_dir')},
        'x_axis': {'label': XLABEL, 'time_ms': f'step × {ms_per_step:g} (= step × dt {dk["dt_s"]:g} s × 1000 · dt from the deck echo in the log)',
                   'range_ms': [X0, X1],
                   't0': f'step 0 = start of the insertion-only run (NP 1 · insertion at step 1); this log starts at step {cv["first_step"]} '
                         f'(read_restart {cv["read_restart"]})',
                   'note': 'scaled deck time (Scale r×1000 · E×0.001 · P×0.001) — not the real pressing time (ps73 README §5)'},
        'phase_bounds_step': {'packing_settling': [1, b['2'] - 1], 'plate_placed_stabilization': b['2'], 'compression_start': b['3'],
                              'relaxation_plate_stop': b['4'], 'end': end},
        'phase_bounds_ms': {'packing_settling_start': 0.0, 'plate_placed_stabilization': b['2'] * ms_per_step,
                            'compression_start': b['3'] * ms_per_step, 'relaxation_plate_stop': b['4'] * ms_per_step, 'end': end * ms_per_step},
        'phase_markers_in_log': cv['bounds'],
        'compression': {'n_runs': len(cv['judges']), 'steps': b['4'] - b['3'], 'duration_ms': (b['4'] - b['3']) * ms_per_step,
                        'duration_s': round((b['4'] - b['3']) * dk['dt_s'], 12)},
        'thickness': {'definition': 'plate position (bottom wall z = 0 → plate), computed from the deck: fixed at PLATE HEIGHT during '
                                    'stabilization · −press_speed·dt per step during compression · fixed during relaxation',
                      'plate_z0_um': dk['plate_z0_deck'] * um, 'zmax_center_at_settling_end_um': round(dk['zmax_center_deck'] * um, 9),
                      'stop_um': zfn(b['4']) * um, 'end_um_computed': z_end * um, 'end_um_mesh_end': mesh_end_um,
                      'residual_um': res_um, 'tolerance_um': tol_um, 'descent_um': round((dk['plate_z0_deck'] - z_end) * um, 9),
                      'n_points': len(tser), 'grid': f'mesh-dump steps (every {dk["mesh_dump_every"]}) + four phase corners',
                      'packing_segment': 'NOT DRAWN in the plate figures (no plate before step '
                                         f'{b["2"]}) — the atom-top figures draw it from the cluster CSV (one criterion · README §8)'},
        'velocity': {'deck_m_per_s': dk['press_speed_deck_m_s'], 'um_per_s': v_um_s, 'mm_per_s': v_um_s / 1000.0,
                     'note': 'real length per simulation second (ps73 README §8)', 'series': [list(p) for p in vser]},
        'pressure': {'source': 'thermo pressMPa × 1000 (setup line of every run dropped · scripts/compaction_curve.py rule)',
                     'n_points': len(pser), 'prepended': list(pser[0]), 'first_step_ge_mpa': on,
                     'first_nonzero_in_compression': None if fnz is None else {'step': fnz[0], 'ms': fnz[0] * ms_per_step, 'mpa': fnz[1],
                                                                               'plate_um': zfn(fnz[0]) * um},
                     'stop': [b['4'], pmap[b['4']]], 'relax_first': list(relax[0]), 'relax_min': list(min(relax, key=lambda t: t[1])),
                     'end': list(relax[-1]), 'max': list(max(px, key=lambda t: t[1])), 'target_mpa': dk['target_mpa']},
        'atoms': {'count_changes': counts, 'note': 'SE lost at the start of relaxation (D1 README §2)'},
        'checks': {'deck_log_vs_repo_deck': 'same settings', 'judge_lines_vs_thermo': len(cv['judges']),
                   'plate_end_vs_mesh_end': {'residual_um': res_um, 'within_um': tol_um},
                   'draft2_crosscheck': dict(xstat, status='same'),
                   'mesh_dumps': 'not in the repository — plate position checked only at the end (mesh_end)'},
        'arrows': {'relaxation_end_segment': {'x_ms': arrows[0][0], 'y_um': arrows[0][1], 'drawn': True,
                                              'note': 'points down to the fixed-plate relaxation segment (1st author slide layout)'},
                   'packing_start': {'drawn': False, 'why': 'plate figures: no thickness data before plate placement (packing segment not '
                                                            'drawn) — drawn in the atom-top figures (atomtop.arrows)'}},
        'figures': {'plate_raw': f'previews/{FIG_NAME}.png', 'plate_slide': f'previews/{FIG_SLIDE}.png',
                    'atomtop_raw': f'previews/{FIG_AT}.png' if at else None, 'atomtop_slide': f'previews/{FIG_AT_SLIDE}.png' if at else None,
                    'rule': 'one criterion per figure — plate figures = plate position · atom-top figures = max(z + r) of all atoms (never mixed)'},
        'pressure_slide': {
            'what': 'slide version (1st author 11-02 night: no post-stop ringing) — measured thermo up to the plate stop, then a schematic '
                    'decay (모식 · not measured) to the end value · ps73 README §5 precedent · raw version kept (d1_ms_pressure.csv)',
            'formula': f'p(s) = {p_end_v:.8g} + ({p_stop_v:.8g} − {p_end_v:.8g})·exp(−(s − {b["4"]})/{SLIDE_TAU_STEP}) every 1,000 steps after the stop',
            'tau_step': SLIDE_TAU_STEP, 'tau_ms': SLIDE_TAU_STEP * ms_per_step,
            'tau_note': 'figure-only constant (ps73 make_fig.py value) — not from the data; only the end value is computed',
            'p_stop_mpa': p_stop_v, 'p_end_mpa_computed': p_end_v, 'schematic_end_mpa': sch[-1][1],
            'schematic_end_minus_computed_mpa': sch[-1][1] - p_end_v, 'n_points': len(sser), 'n_schematic': len(sch),
            'raw_relaxation_replaced': {'n_rows': len(relax), 'first': list(relax[0]), 'min': list(min(relax, key=lambda t: t[1])),
                                        'max': list(max(relax, key=lambda t: t[1])), 'end': list(relax[-1])},
            'csv': f'origin/{CSV_SLIDE}.csv', 'ogs': f'origin/{CSV_SLIDE}.ogs', 'preview': f'previews/{FIG_SLIDE}.png'},
        'atomtop': atomtop_summary(at, at_arrows, zfn, um) if at else {
            'status': 'NOT_SUPPLIED — the packing segment is not drawn (generator refuses to invent it; `--atomtop` exits)',
            'csv_expected': rel(ATOMTOP_CSV), 'cluster_script': rel(HERE / 'cluster' / 'd1_atomtop_cluster.py'),
            'cluster_script_sha256': sha256_file(HERE / 'cluster' / 'd1_atomtop_cluster.py'),
            'plan_steps': {'default_no_replay': {'checkpoints_run0': CKPT_STEPS, 'atom_dumps': len(ATOMTOP_DUMPS)},
                           'with_replay_option': sorted(REPLAY_REF)},
            'ke_reference': {'replay_from_insertion_log': {str(k): list(v) for k, v in REPLAY_REF.items()},
                             'checkpoints_from_main_log': {str(s): list(cv['ke'][s]) for s in ATOMTOP_EARLY[len(REPLAY_REF):]}},
            'insertion_decision': 'no insertion replay by default (1st author 11-02 night: draw 0 → 20 ms as a free fall at the packing '
                                  'gravity and join it) — cluster = 10 checkpoint run-0 dumps + scan (≈10 min); 0 → 20.001 ms = schematic '
                                  'free fall (모식) h(t) = h20 + v0·(t20 − t) + ½·g·(t20² − t²) anchored at the measured 20,001-step top, '
                                  'g · v0 from the insert deck, damping neglected; the full insertion replay (4,584 s ≈ 76 min) stays '
                                  'behind --with-replay',
            'free_fall_constants': deck_free_fall(INSERT_DECK.read_text(encoding='utf-8'), um)},
        'stage_frames': stages,
        'cluster_tar': {'steps': tar_steps, 'run_dir': f'{RUN_PARENT}/{RUN_CASE}', 'bundle': f'$HOME/{TAR_TAG}.tgz', 'command': cmd},
        'packing_segment_requirements': {
            'checkpoints_run0': [f'{RUN_CASE}/restart_{RUN_CASE}/{ck}' for _, ck in CLUSTER.CKPTS],
            'ke_reference_from_log': {str(s): list(cv['ke'][s]) for s in ke_steps if s in cv['ke']},
            'insertion_replay': 'input_kg50_d1_b50_insert.liggghts at NP 1 (same as the insertion run) + atom dump; check inserted counts '
                                'and KE against log_kg50_d1_b50_ins.out (end bundle member · sha256 in the cluster script)',
            'atom_dumps_for_one_criterion': f'{len(dumps) - 1} compression/relaxation dumps (every {dk["atom_dump_every"]}) + atom_end',
            'how': 'cluster/d1_atomtop_cluster.py (README §8)',
        },
    }
    KEY_JSON.write_text(json.dumps(key, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'dt {dk["dt_s"]:g} s · ms/step {ms_per_step:g} · 판 {dk["plate_z0_deck"] * um:.6f} → {z_end * um:.6f} µm (mesh_end {mesh_end_um} · '
          f'잔차 {res_um:+.6f} µm) · 압축 {len(cv["judges"])} run = {(b["4"] - b["3"]) * ms_per_step:g} ms · 정지 {pmap[b["4"]]:.5f} MPa · '
          f'끝 {relax[-1][1]:.5f} MPa · 판 속도 {v_um_s:g} µm/s · 초안 2 대조 {xstat["n_rows_compared"]} 행 같음')
    for st in stages:
        n, r = st['nearest'], st['recommended']
        print(f'  {st["label"]:<22} 사건 {st["event"]["step"]:>9,} ({st["event"]["pressure_mpa"]:.2f} MPa) → 가장 가까운 덤프 {n["step"]:,} '
              f'(Δ {n["delta_steps"]:+,} · 단계 {n["phase"]} · {n["pressure_mpa"]:.2f} MPa) · 권고 {r["step"]:,}')


# ───────────────────────────── 자기 시험 (합성 로그) ─────────────────────────────
def _synth_log(**kw):
    """D1 로그 꼴의 작은 합성 로그 — 정착 1,000 · zmax run 1 · 안정화 2,000 · 압축 5 run × run_len · 이완 3,000 · run 0.
    kw (반례): judge_bias · targets · phase4_shift · drop_pcol · nan_at · run_len · last_p · mid_hit · restart_step · plate ·
    dt_line · ts_line · move_line · scale_line · area · units."""
    g = kw.get
    run_len = g('run_len', 5000)
    s_set, s_ss = 20001, 21001
    b2, b3 = s_ss + 1, s_ss + 1 + 2000
    n_runs = 5
    b4 = b3 + n_runs * run_len
    gap = 1000 if g('phase4_shift') else 0
    end = b4 + gap + 3000
    k = g('last_p', 0.301) / (b4 - b3 - 8000)

    def pc(s):
        if g('mid_hit') and s == b3 + 2 * run_len:
            return 0.35
        return max(0.0, (s - (b3 + 8000)) * k)

    def block(cols, s0, s1, fn, every=1000):
        steps = [s0] + list(range((s0 // every + 1) * every, s1, every)) + [s1]
        return ['    ' + '    '.join(cols)] + [fn(s) for s in steps] + [f'Loop time of 1.0 on 20 procs for {s1 - s0} steps with 168457 atoms', '']

    def row_p(s, pfn, atoms=168457):
        if g('nan_at') == s:
            return f'{s:>9} {atoms:>8} {1e-6:>14.8g} {0.0:>14.8g} {"nan":>14}'
        return f'{s:>9} {atoms:>8} {1e-6:>14.8g} {0.0:>14.8g} {pfn(s):>14.8g}'

    pcol = ['Step', 'Atoms', 'KinEng', 'CPU', 'pressMPa']
    L = ['LIGGGHTS (Version LIGGGHTS-PUBLIC 3.8.0)',
         g('scale_line', '# Scale: r×1000, E×0.001, P×0.001'), g('units', 'units           si'),
         'variable target_press equal 0.30          # 300 MPa × 0.001', 'variable r_AM_P  equal 3e-3',
         g('dt_line', 'variable dt      equal 1.0e-6'), 'variable plate_margin equal 0.003', 'timestep        ${dt}',
         g('ts_line', 'timestep        1e-06'), f'read_restart    restart_x/restart_settling_{g("restart_step", s_set)}.bin',
         '  orthogonal box = (0 0 -0.01) to (0.05 0.05 1)', 'thermo_style    custom step atoms ke cpu',
         'print "====== PHASE 1: SETTLING ======"', '====== PHASE 1: SETTLING ======', 'run 1000']
    L += block(pcol[:4], s_set, s_ss, lambda s: f'{s:>9} {168457:>8} {2.0:>14.8g} {0.0:>14.8g}')
    L += ['thermo_style    custom step atoms c_zmax', 'run 1']
    L += block(['Step', 'Atoms', 'zmax'], s_ss, s_ss + 1, lambda s: f'{s:>9} {168457:>8} {0.13944572:>14.8g}', every=10 ** 9)
    L += ['====== Z_MAX (center): 0.139445726030801 ======', f'====== PLATE HEIGHT: {g("plate", 0.145445726030801)!r} ======',
          'dump dmp_mesh all mesh/stl 5000 post_x/mesh_*.stl top_mesh', '====== PHASE 2: STABILIZE ======',
          'variable pressMPa equal abs(f_top_mesh[3])/' + g('area', '0.0025') + '/1000000',
          'thermo_style    custom step atoms ke cpu v_pressMPa', 'run 2000']
    if g('drop_pcol'):
        L += block(pcol[:4], b2, b3, lambda s: f'{s:>9} {168457:>8} {1e-6:>14.8g} {0.0:>14.8g}')
    else:
        L += block(pcol, b2, b3, lambda s: row_p(s, lambda _s: 0.0))
    L += ['====== PHASE 3: COMPRESSION (Speed 0.01) ======', 'dump dmp_atom all custom 50000 post_x/atom_*.liggghts id type x y z radius',
          'variable press_speed equal 0.01', 'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -${press_speed}',
          g('move_line', 'fix move_press all move/mesh mesh top_mesh linear 0.0 0.0 -0.01'), 'label loop_press', f'    run {run_len}']
    targets = g('targets', [0.3] * n_runs)
    for i in range(n_runs):
        s0, s1 = b3 + i * run_len, b3 + (i + 1) * run_len
        L += block(pcol, s0, s1, lambda s: row_p(s, pc))
        x = pc(s1) * ((1 + g('judge_bias', 0.0)) if i == n_runs - 1 else 1)
        L += ['    variable current_press equal "abs(f_top_mesh[3]) / 0.0025 / 1000000"',
              f'Current Pressure: {x!r} MPa (Target: {targets[i]!r})']
    L += ['unfix move_press']
    if gap:                                                    # 루프 탈출과 PHASE 4 표지 사이에 run 하나 더 (표지가 다른 step 으로 풀린다)
        L += block(pcol, b4, b4 + gap, lambda s: row_p(s, lambda _s: 0.2))
    relax_p = lambda s: 0.156 + 0.05 * math.exp(-(s - b4) / 1000.0)  # noqa: E731
    L += ['====== PHASE 4: RELAXATION ======', 'run 3000']
    L += block(pcol, b4 + gap, end, lambda s: row_p(s, relax_p, 168457 if s < b4 + 2000 else 168452))
    L += ['run 0', '    ' + '    '.join(pcol), row_p(end, lambda _s: 0.161, 168452), 'Loop time of 1e-05 on 20 procs for 0 steps', '']
    return '\n'.join(L) + '\n', {'b2': b2, 'b3': b3, 'b4': b4, 'end': end, 'k': k}


def selftest():
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        ok, fail = ok + bool(cond), fail + (not cond)
        print(('PASS ' if cond else 'FAIL ') + name)

    def raises(fn):
        """거부 = ValueError 만 (다른 예외 · 통과 = 실패 — 기능을 뺀 판 (NotImplementedError) 이 반례를 통과하지 못하게)."""
        try:
            fn()
        except ValueError:
            return True
        except Exception:            # noqa: BLE001
            return False
        return False

    def safe(fn, default=None):
        try:
            return fn()
        except Exception:            # noqa: BLE001
            return default

    with tempfile.TemporaryDirectory(prefix='d1ms_') as tmp:
        counter = itertools.count()

        def curve(**kw):
            text, bb = _synth_log(**kw)
            p = Path(tmp) / f'log_{next(counter)}.txt'
            p.write_text(text, encoding='utf-8')
            return text, bb, p

        text, b, path0 = curve()
        dk = safe(lambda: deck_settings(text), {})
        chk('D0 합성 로그 덱: dt · 판 속도 · 배율 · 면적 · 목표 · 판 높이 · 루프 run · 덤프 간격 · 덤프 폴더',
            dk.get('dt_s') == 1e-6 and dk.get('press_speed_deck_m_s') == 0.01 and dk.get('um_per_deck_m') == 1000.0
            and dk.get('mpa_per_deck_mpa') == 1000.0 and dk.get('area_deck_m2') == 0.0025 and dk.get('target_mpa') == 300.0
            and dk.get('plate_z0_deck') == 0.145445726030801 and dk.get('loop_run_steps') == 5000 and dk.get('atom_dump_every') == 50000
            and dk.get('mesh_dump_every') == 5000 and dk.get('post_dir') == 'post_x')
        for name, kw in [('D1 timestep ≠ variable dt', {'ts_line': 'timestep 2e-06'}),
                         ('D2 variable dt 둘', {'dt_line': 'variable dt equal 1.0e-6\nvariable dt equal 2.0e-6'}),
                         ('D3 판이 옆으로 움직인다', {'move_line': 'fix m all move/mesh mesh top linear 0.001 0.0 -0.01'}),
                         ('D4 판 속도 둘 (숫자 줄 ≠ press_speed)', {'move_line': 'fix m all move/mesh mesh top linear 0.0 0.0 -0.02'}),
                         ('D5 Scale 머리 없음', {'scale_line': '# (no scale)'}),
                         ('D6 pressMPa 면적 ≠ 판정 식 · 상자 x·y 면적', {'area': '0.0036'}),
                         ('D7 PLATE HEIGHT ≠ Z_MAX + r_AM_P + margin', {'plate': 0.1455}),
                         ('D8 units ≠ si', {'units': 'units lj'}),
                         ('D9 로그에 풀린 timestep 숫자 줄 없음', {'ts_line': ''}),
                         ('D10 로그에 풀린 move/mesh 숫자 줄 없음', {'move_line': ''})]:
            t2, _ = _synth_log(**kw)
            chk(name + ' = 거부', raises(lambda: deck_settings(t2)))
        chk('D11 PLATE HEIGHT 둘 = 거부', raises(lambda: deck_settings(text + '====== PLATE HEIGHT: 0.15 ======\n')))
        chk('D12 undump dmp_atom (덤프 끊김) = 거부', raises(lambda: deck_settings(text + 'undump dmp_atom\n')))
        deck_only = '\n'.join(ln for ln in text.splitlines()[1:] if not re.match(r'\s*(=|orthogonal|timestep\s+1e|fix move_press .* -0\.01)', ln))
        dd = safe(lambda: deck_settings(deck_only), {})
        chk('D13 덱 글 (LIGGGHTS 머리 없음 · ${dt} · ${press_speed} 만) = 읽힘 · 판 높이 없음',
            dd.get('dt_s') == 1e-6 and dd.get('press_speed_deck_m_s') == 0.01 and 'plate_z0_deck' not in dd)

        cv = safe(lambda: read_curve(path0, 0.3, 5000))
        chk('L0 합성 로그: 단계 경계 · 판정 줄 5 · 설정 줄 버림 · 경계 줄의 단계 · KE 참고 (설정 줄 포함)',
            cv is not None and [cv['bounds'][k]['step'] for k in '1234'] == [20001, b['b2'], b['b3'], b['b4']]
            and len(cv['judges']) == 5 and cv['last_step'] == b['end'] and cv['first_step'] == 20001
            and all(r['step'] != 20001 for r in cv['rows']) and cv['ke'].get(20001) == (168457, 2.0)
            and {r['phase'] for r in cv['rows'] if r['step'] == b['b4']} == {3} and {r['phase'] for r in cv['rows'] if r['step'] == b['b3']} == {2})
        for name, kw in [('L1 판정 줄 ≠ thermo', {'judge_bias': 0.01}),
                         ('L2 목표 둘', {'targets': [0.3, 0.3, 0.25, 0.3, 0.3]}),
                         ('L3 단계 ≥ 2 긴 블록에 압력 열 없음', {'drop_pcol': True}),
                         ('L4 비유한 압력', {'nan_at': b['b3'] + 6998}),
                         ('L5 마지막 판정 < 목표 (루프 탈출 안 함)', {'last_p': 0.29}),
                         ('L6 중간 판정이 목표 이상 (더 일찍 나갔어야)', {'mid_hit': True}),
                         ('L7 read_restart step ≠ 첫 thermo step', {'restart_step': 20000}),
                         ('L8 PHASE 4 표지 ≠ 루프 탈출 step', {'phase4_shift': True})]:
            _, _, p2 = curve(**kw)
            chk(name + ' = 거부', raises(lambda: read_curve(p2, 0.3, kw.get('run_len', 5000))))
        _, _, p4 = curve(run_len=4000)
        cv4 = safe(lambda: read_curve(p4, 0.3, 4000))
        chk('L9 run 4,000 덱 = 그 길이로 이어짐 (일반화) · 5,000 으로 읽으면 거부',
            cv4 is not None and len(cv4['judges']) == 5 and raises(lambda: read_curve(p4, 0.3, 5000)))
        chk('L10 판정 목표 ≠ 덱 target_press = 거부', raises(lambda: read_curve(path0, 0.25, 5000)))

        z = safe(lambda: plate_model(200002, 400002, 2685002, 2785002, 0.145445726030801, 0.01, 1e-6))
        chk('T1 판 궤적: 안정화 고정 · 압축 등속 · 이완 고정 · 끝 122.595726 µm',
            z is not None and z(200002) == z(400002) == 0.145445726030801 and abs(z(500002) * 1000 - 144.445726030801) < 1e-9
            and z(2685002) == z(2785002) and abs(z(2785002) * 1000 - 122.595726030801) < 1e-9)
        chk('T2 판 놓기 전 · 끝 뒤 step = 거부', z is not None and raises(lambda: z(200001)) and raises(lambda: z(2785003)))
        chk('T3 단계 경계 순서 어긋남 = 거부', raises(lambda: plate_model(400002, 200002, 2685002, 2785002, 0.1454, 0.01, 1e-6)))
        r = safe(lambda: check_plate_end(0.122595726030801, 122.596, 1000.0))
        chk('T4 끝 대조: 잔차 −0.000274 µm (반폭 0.0005 안) = 통과', r is not None and abs(r[0] + 0.000273969199) < 1e-9)
        chk('T5 끝 대조: mesh_end 122.597 (1 nm 어긋남) = 거부', raises(lambda: check_plate_end(0.122595726030801, 122.597, 1000.0)))
        chk('T6 끝 대조: 판 속도 0.0101 로 계산한 끝 = 거부',
            raises(lambda: check_plate_end(plate_model(200002, 400002, 2685002, 2785002, 0.145445726030801, 0.0101, 1e-6)(2785002), 122.596, 1000.0)))
        chk('T7 끝 대조: NaN = 거부', raises(lambda: check_plate_end(float('nan'), 122.596, 1000.0)))
        ts = safe(lambda: thickness_series(z, (200002, 400002, 2685002, 2785002), 5000, 1e-3, 1000.0), [])
        chk('T8 두께 점: 메시 step 517 + 모서리 4 · 시각 엄격 증가 · 모서리 출처',
            len(ts) == 521 and all(q[0] > p[0] for p, q in zip(ts, ts[1:])) and ts[0][2] == SRC['placed'] and ts[-1][2] == SRC['end']
            and abs(ts[0][1] - 145.445726030801) < 1e-9 and any(t == 2685.002 and s == SRC['stop'] for t, _, s in ts))
        vs = velocity_series((200002, 400002, 2685002, 2785002), 10.0, 1e-3)
        chk('V1 판 속도 계단 7 점 · 400.002 → 2685.002 ms 만 10 µm/s',
            [v for _, v, _ in vs] == [0, 0, 0, 10.0, 10.0, 0, 0] and [t for t, _, _ in vs] == [0.0, 200.002, 400.002, 400.002, 2685.002, 2685.002, 2785.002])
        if cv is not None:
            px, ps = safe(lambda: pressure_series(cv['rows'], 1000.0, 1e-3), (None, None))
            chk('P1 압력: 앞에 (0 ms, 0 MPa, 판 없음) · 단계 ≥ 2 원값 × 1000',
                ps is not None and ps[0] == (0.0, 0.0, SRC['noplate']) and len(ps) == len(px) + 1 and px[0] == (b['b2'] + 998, 0.0))
            rows_bad = [dict(rr, p_deck=(0.001 if rr['phase'] == 2 else rr['p_deck'])) for rr in cv['rows']]
            chk('P2 판 놓은 뒤 첫 압력 ≠ 0 = 거부', raises(lambda: pressure_series(rows_bad, 1000.0, 1e-3)))
            zs = plate_model(b['b2'], b['b3'], b['b4'], b['end'], 0.145445726030801, 0.01, 1e-6)
            dps = dump_steps(b['b3'], b['end'], 5000)
            am = {rr['step']: rr['atoms'] for rr in cv['rows']}
            st = safe(lambda: stage_table(px, cv['bounds'], dps, b['end'], zs, 1000.0, am, 1e-3), []) if px else []
            want50 = next(s for s, p in px if b['b3'] < s and p >= 50.0) if px else None
            chk('S1 단계 표: 50 MPa = 압축 중 처음 ≥ 50 thermo 줄 · 가장 가까운 덤프 · 반대쪽 덤프',
                len(st) == 4 and st[1]['event']['step'] == want50 and st[1]['nearest']['step'] == min(dps, key=lambda d: (abs(d - want50), -d))
                and st[1]['other_side'] is not None and (st[1]['other_side']['step'] - want50) * st[1]['nearest']['delta_steps'] < 0)
            chk('S2 판 정지: 가장 가까운 덤프가 이완 단계면 표지 · 권고 = 같은 압축 단계 덤프 · 끝 = atom_end (Δ 0 · 반대쪽 없음)',
                len(st) == 4 and st[2]['nearest']['phase'] == 4 and not st[2]['nearest_is_same_phase']
                and st[2]['recommended']['phase'] == 3 and st[2]['recommended']['step'] < b['b4']
                and st[3]['nearest']['step'] == b['end'] and st[3]['nearest']['delta_steps'] == 0 and st[3]['other_side'] is None)
            chk('S3 압축 중 그 압력에 닿지 않으면 거부', bool(px) and raises(lambda: stage_table(px, cv['bounds'], dps, b['end'], zs, 1000.0, am, 1e-3,
                                                                                           p_stage=400.0)))
        else:
            for nm in ('P1', 'P2', 'S1', 'S2', 'S3'):
                chk(nm + ' (합성 로그 읽기 실패)', False)
        dsr = dump_steps(400002, 2785002, 50000)
        chk('S4 덤프 일정: 압축 시작 400,002 뒤 첫 덤프 450,000 · 50,000 마다 · 끝 덤프 2,785,002 (47 + 1)',
            dsr[:2] == [450000, 500000] and dsr[-2:] == [2750000, 2785002] and len(dsr) == 48)
        cmd = safe(lambda: cluster_command([450000, 2785002], 2785002, 'post_kg50_d1_b50', {450000: 168457, 2785002: 168452}), '')
        chk('C1 클러스터 명령: bash -s · set -e · 끝 묶음 sha256 둘 · TIMESTEP/원자 수 검사 · 주소 · 포트 없음',
            cmd.startswith("bash -s <<'EOF'\nset -euo pipefail") and ATOM_END_SHA256 in cmd and MESH_END_SHA256 in cmd
            and 'check kg50_d1_b50/post_kg50_d1_b50/atom_450000.liggghts 450000 168457' in cmd
            and 'kg50_d1_b50/post_kg50_d1_b50/mesh_end_2785002.stl' in cmd and '@' not in cmd and 'scp' not in cmd and 'ssh' not in cmd)
        chk('C2 클러스터 명령: 로그에 없는 step 의 원자 수를 모르면 거부 (KeyError — 지어내지 않는다)',
            safe(lambda: cluster_command([450001], 2785002, 'p', {}), 'refused') == 'refused')
        pth = Path(tmp) / 'o.csv'
        write_origin_csv(pth, ['Time', 'Thickness', 'Source'], ['ms', 'µm', ''], [('0.000', '1.0000', 'x')])
        raw = pth.read_bytes()
        chk('C3 Origin CSV: BOM · LF · 머리 두 줄', raw.startswith(b'\xef\xbb\xbfTime,Thickness,Source\nms,') and b'\r' not in raw)
        met = {'compaction': {'compress_start_step': 3, 'stop_step': 4, 'n_compress_runs': 1, 'plate_z0_um': 1.0, 'z_end_pred_um': 0.5,
                              'z_end_mesh_um': 0.5, 'p_t0minus_MPa': 300.0, 'p_relax_first_MPa': 200.0, 'p_end_MPa': 150.0,
                              'n_load_rows': 1, 'n_relax_rows': 1}}
        ours = {'b3': 3, 'b4': 4, 'n_runs': 1, 'z0_um': 1.0, 'z_end_um': 0.5, 'mesh_end_um': 0.5, 'p_stop': 300.0, 'p_relax_first': 200.0,
                'p_end': 150.0, 'n_load': 1, 'n_relax': 1, 'px': [(4, 300.0), (5, 200.0)], 'zfn_um': lambda s: 0.5}
        rows_ok = [{'branch': 'loading', 'step': '4', 'plate_pressure_MPa': '300.0', 'plate_gap_um': '0.5'},
                   {'branch': 'fixed_height_relaxation', 'step': '5', 'plate_pressure_MPa': '200.0', 'plate_gap_um': '0.5'}]
        chk('X1 초안 2 대조: 같으면 통과', safe(lambda: crosscheck_draft2(met, rows_ok, ours)[0]) == [])
        chk('X2 초안 2 대조: 판 높이 0.01 µm 다름 = 문제', bool(safe(lambda: crosscheck_draft2(met, [dict(rows_ok[0], plate_gap_um='0.51'), rows_ok[1]], ours)[0], [])))
        chk('X3 초안 2 대조: 끝 압력 다름 = 문제', bool(safe(lambda: crosscheck_draft2({'compaction': dict(met['compaction'], p_end_MPa=150.1)},
                                                                                rows_ok, ours)[0], [])))
        chk('X4 초안 2 대조: 행 하나 빠짐 = 문제', bool(safe(lambda: crosscheck_draft2(met, rows_ok[:1], ours)[0], [])))
        chk('X5 초안 2 대조: 압력 NaN = 문제', bool(safe(lambda: crosscheck_draft2(met, [dict(rows_ok[0], plate_pressure_MPa='nan'), rows_ok[1]], ours)[0], [])))

        # ── 압력 슬라이드판 (ps73 README §5 선례: 판 정지까지 원값 · 그 뒤 끝 값으로 가는 모식 감쇠 · 원값판은 따로) ──
        b4s, ends = 2685002, 2785002
        px_s = [(400002, 0.0)] + [(s, 0.3 * (s - 400002) / (b4s - 400002) * 1000.0) for s in range(401000, b4s, 1000)] + [(b4s, 300.58919)] + \
               [(s, 156.0 + (s % 7)) for s in range(2686000, ends, 1000)] + [(ends, 156.15118)]
        px_copy = list(px_s)
        sl = safe(lambda: slide_series(px_s, b4s, ends, 1e-3, tau_step=15000))
        if sl is not None:
            ser, sch = sl
            comp = [p for p in ser if p[2] != SRC_SCHEMATIC]
            chk('R1 슬라이드: 정지까지 원값 그대로 (앞 0 ms 점 포함) · 원값 목록은 안 바뀜',
                comp[0] == (0.0, 0.0, SRC['noplate']) and [(round(t / 1e-3), p) for t, p, _ in comp[1:]] == [(s, p) for s, p in px_s if s <= b4s]
                and px_s == px_copy)
            chk('R2 슬라이드: 정지 뒤 1,000 step 마다 p_end + (p_c − p_end)·exp(−Δ/τ) · 마지막 = 런 끝 · 출처 = 모식',
                len(sch) == 100 and sch[0][0] == b4s + 1000 and sch[-1][0] == ends
                and abs(sch[0][1] - (156.15118 + (300.58919 - 156.15118) * math.exp(-1000 / 15000))) < 1e-12
                and all(p[2] == SRC_SCHEMATIC for p in ser if p[0] > b4s * 1e-3 + 1e-9) and '모식' in SRC_SCHEMATIC)
        else:
            chk('R1 슬라이드 (구현 없음)', False)
            chk('R2 슬라이드 (구현 없음)', False)
        chk('R3 슬라이드: 정지 step 압력 줄 없음 = 거부', raises(lambda: slide_series([p for p in px_s if p[0] != b4s], b4s, ends, 1e-3, tau_step=15000)))
        chk('R4 슬라이드: 정지 → 끝이 1,000 step 배수가 아님 (끝 값이 계산값이 아니게 됨) = 거부',
            raises(lambda: slide_series(px_s + [(ends + 500, 156.0)], b4s, ends + 500, 1e-3, tau_step=15000)))

        # ── 원자 기준 두께 (클러스터 CSV) — 새 구간 · 검사 · 끊긴 y 축 · CSV 없으면 정착 구간 거부 ──
        chk('A0 클러스터 CSV 없음 = 정착 구간 거부 (지어내지 않는다)', raises(lambda: require_atomtop(None))
            and raises(lambda: require_atomtop(Path(tmp) / 'nope.csv')))
        ckpt_steps = [s for s in ATOMTOP_EARLY if s not in REPLAY_REF]
        main_ke = {s: (168457, f'{1e-5 * (i + 1):.8g}') for i, s in enumerate(ckpt_steps)}
        main_ke.update({s: (168457 if s < 2689000 else 168452, '1e-07') for s in ATOMTOP_DUMPS})

        def synth_rows(mode='replay'):
            zck = {20001: 200.0, 50000: 150.0, 100000: 143.0, 150000: 142.6, 200000: 142.5, 200001: 142.5, 250000: 142.6, 300000: 142.7,
                   350000: 142.8, 400000: 142.9}
            out = []
            for s in (ATOMTOP_EARLY if mode == 'replay' else [x for x in ATOMTOP_EARLY if x not in REPLAY_REF]):
                zt = 325.0 - 120.0 * (s - 1) / 19999 if s in REPLAY_REF else zck[s]      # 재현 = 325 → 205 µm 낙하 (합성)
                rep = s in REPLAY_REF
                ref = REPLAY_REF[s] if rep else main_ke[s]
                out.append({'step': s, 'time_ms': f'{s * 1e-3:.3f}', 'ztop_um': zt, 'source': 'replay' if rep else 'checkpoint',
                            'dump_file': f'work:dump/atom_{s}.liggghts', 'dump_timestep': s, 'n_header': ref[0], 'n_rows': ref[0],
                            'n_bad_lines': 0, 'zc_max_um': zt - 0.5, 'ztop_id': '7', 'ztop_type': '3', 'ztop_radius_um': 0.5,
                            'ztop_p999_um': zt - 0.3, 'bytes': 1000, 'mtime': '2026-11-03T00:00:00',
                            'run_log': 'log.replay' if rep else f'log.ckpt_{s}', 'run_log_atoms': ref[0], 'run_log_ke': ref[1],
                            'orig_log': 'log_kg50_d1_b50_ins.out' if rep else 'log.liggghts', 'orig_log_atoms': ref[0], 'orig_log_ke': ref[1]})
            for i, s in enumerate(ATOMTOP_DUMPS):
                zt = 142.9 - 19.2 * i / (len(ATOMTOP_DUMPS) - 1)
                n = main_ke[s][0]
                out.append({'step': s, 'time_ms': f'{s * 1e-3:.3f}', 'ztop_um': zt, 'source': 'atom dump',
                            'dump_file': f'run:post_kg50_d1_b50/atom_{s}.liggghts', 'dump_timestep': s, 'n_header': n, 'n_rows': n,
                            'n_bad_lines': 0, 'zc_max_um': zt - 0.5, 'ztop_id': '9', 'ztop_type': '3', 'ztop_radius_um': 0.5,
                            'ztop_p999_um': zt - 0.3, 'bytes': 2000, 'mtime': f'2026-10-30T{i // 60:02d}:{i % 60:02d}:00',
                            'run_log': '', 'run_log_atoms': '', 'run_log_ke': '', 'orig_log': 'log.liggghts', 'orig_log_atoms': n,
                            'orig_log_ke': '1e-07'})
            return out
        meta_ok = {'mode': 'replay',
                   'insertion': 'INFO: Particle insertion ins_mix: inserted 168457 particle templates (mass 9.557438e-01) at step 1',
                   'insertion_orig': 'INFO: Particle insertion ins_mix: inserted 168457 particle templates (mass 9.557438e-01) at step 1',
                   'sha256': dict(ATOMTOP_SHA), 'script_sha256': sha256_file(HERE / 'cluster' / 'd1_atomtop_cluster.py')}

        def write_at(rows, meta=meta_ok, head=None):
            p = Path(tmp) / f'atomtop_{next(counter)}.csv'
            with open(p, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f, lineterminator='\n')
                w.writerow(head or ATOMTOP_HEAD)
                for r in rows:
                    w.writerow([r.get(k, '') for k in ATOMTOP_HEAD])
                for key in ('mode', 'insertion', 'insertion_orig'):
                    if key in meta:
                        w.writerow(['#' + key, meta[key]])
                for k in sorted(meta['sha256']):
                    w.writerow(['#sha256', k, meta['sha256'][k]])
                w.writerow(['#script_sha256', meta['script_sha256']])
            return p
        radii = {3.0, 2.0, 0.5}
        rd = safe(lambda: read_atomtop(write_at(synth_rows())))
        chk('A1 클러스터 CSV 읽기 · 검사: 정상 합성 = 문제 없음',
            rd is not None and len(rd[0]) == len(ATOMTOP_EARLY) + len(ATOMTOP_DUMPS) and safe(lambda: check_atomtop(rd[0], rd[1], main_ke, radii)) == [])
        chk('A2 머리 다름 = 거부', raises(lambda: read_atomtop(write_at(synth_rows(), head=ATOMTOP_HEAD[:-1] + ['x']))))
        at_i = lambda rows, st: next(i for i, r in enumerate(rows) if r['step'] == st)  # noqa: E731  행을 step 으로 찾는다 (계획 길이와 무관)
        for name, mut in [('A3 체크포인트 하나 빠짐', lambda r: r.pop(at_i(r, 100000))),
                          ('A4 덤프 TIMESTEP ≠ step', lambda r: r[at_i(r, 650000)].update(dump_timestep=1)),
                          ('A5 머리 원자 수 ≠ 줄 수', lambda r: r[at_i(r, 1150000)].update(n_rows=168456)),
                          ('A6 체크포인트 KE ≠ 본 로그 (원 런 상태 아님)', lambda r: r[at_i(r, 50000)].update(run_log_ke='0.5')),
                          ('A7 재현 1,000 step KE ≠ 원 삽입 로그 (궤적 갈림)', lambda r: r[at_i(r, 1000)].update(run_log_ke='0.1704')),
                          ('A7b 재현 20,000 step KE ≠ 원 삽입 로그 (끝에서 갈림)', lambda r: r[at_i(r, 20000)].update(run_log_ke='2.3893')),
                          ('A8 덤프 원자 수 ≠ 본 로그', lambda r: r[at_i(r, 1650000)].update(n_header=5, n_rows=5)),
                          ('A9 덤프 파일 시각 거꾸로', lambda r: r[at_i(r, 1050000)].update(mtime='2026-10-29T00:00:00')),
                          ('A10 덱에 없는 반경', lambda r: r[at_i(r, 20001)].update(ztop_radius_um=1.0)),
                          ('A11 윗면 < 중심 · p99.9 > 윗면', lambda r: r[at_i(r, 600000)].update(ztop_p999_um=999.0)),
                          ('A12 time_ms ≠ step × dt', lambda r: r[at_i(r, 20001)].update(time_ms='20.000')),
                          ('A13 깨진 줄', lambda r: r[at_i(r, 1250000)].update(n_bad_lines=2))]:
            rows = synth_rows()
            mut(rows)
            got = safe(lambda: check_atomtop(rows, meta_ok, main_ke, radii))
            chk(name + ' = 문제', bool(got))
        got = safe(lambda: check_atomtop(synth_rows(), dict(meta_ok, insertion='inserted 168000 particle templates'), main_ke, radii))
        chk('A14 재현 삽입 줄 ≠ 원 로그 = 문제', bool(got))
        got = safe(lambda: check_atomtop(synth_rows(), dict(meta_ok, sha256=dict(ATOMTOP_SHA, **{'log.liggghts': '0' * 64})), main_ke, radii))
        chk('A16 런 폴더 sha256 ≠ 리포 기록 (다른 런 · 바뀐 로그) = 문제', bool(got))
        got = safe(lambda: check_atomtop(synth_rows(), dict(meta_ok, script_sha256='0' * 64), main_ke, radii))
        chk('A20 CSV 를 만든 스크립트 ≠ 리포 클러스터 스크립트 (고친 사본 · 옛 판) = 문제', bool(got))
        # ── 이음 시험: 클러스터 스크립트 scan() 이 쓴 CSV 를 이 생성기가 그대로 읽고 검사한다 (가짜 런 · work 폴더 · 원자 3 개 덤프) ──
        import contextlib
        import io
        run_d, work_d = Path(tmp) / 'run', Path(tmp) / 'work'
        (run_d / f'post_{CLUSTER.CASE}').mkdir(parents=True)
        (work_d / 'dump').mkdir(parents=True)
        ins_line = 'INFO: Particle insertion ins_mix: inserted 168457 particle templates (mass 9.557438e-01) at step 1'
        thermo = lambda pairs: '    Step    Atoms         KinEng            CPU \n' + ''.join(f'{st:>8} {na:>8} {ke_:>14} 0.0 \n' for st, na, ke_ in pairs) + 'Loop time\n'  # noqa: E731

        def dump(path, step, top):
            path.write_text(f'ITEM: TIMESTEP\n{step}\nITEM: NUMBER OF ATOMS\n3\nITEM: BOX BOUNDS pp pp ff\n0 0.05\n0 0.05\n-0.01 1\n'
                            f'ITEM: ATOMS id type x y z radius vx\n1 1 0 0 0.05 0.003 0\n2 3 0 0 {top - 0.0005:.6f} 0.0005 0\n3 3 0 0 0.02 0.0005 0\n',
                            encoding='utf-8')
        ke_of = {st: f'{1e-4 * (i + 1):.8g}' for i, st in enumerate(ATOMTOP_EARLY + ATOMTOP_DUMPS)}
        (run_d / 'log_kg50_d1_b50_ins.out').write_text(ins_line + '\n' + thermo([(st, 3, ke_of[st]) for st in sorted(REPLAY_REF)]), encoding='utf-8')
        (run_d / 'log.liggghts').write_text(thermo([(st, 3, ke_of[st]) for st in ATOMTOP_EARLY[2:] + ATOMTOP_DUMPS]), encoding='utf-8')
        for nm in ('input_kg50_d1_b50.liggghts', 'input_kg50_d1_b50_insert.liggghts'):
            (run_d / nm).write_text('# fake deck\n', encoding='utf-8')
        (work_d / 'log.replay').write_text(ins_line + '\n' + thermo([(st, 3, ke_of[st]) for st in sorted(REPLAY_REF)]), encoding='utf-8')
        for i, st in enumerate(ATOMTOP_EARLY):
            dump(work_d / 'dump' / f'atom_{st}.liggghts', st, 0.300 - 0.001 * i)
            if st not in REPLAY_REF:
                (work_d / f'log.ckpt_{st}').write_text(thermo([(st, 3, ke_of[st])]), encoding='utf-8')
        for st in ATOMTOP_DUMPS:
            nm = f'atom_end_{st}.liggghts' if st == CLUSTER.END_STEP else f'atom_{st}.liggghts'
            dump(run_d / f'post_{CLUSTER.CASE}' / nm, st, 0.142 - 1e-8 * st)
        with contextlib.redirect_stdout(io.StringIO()) as so:
            csv_out = safe(lambda: CLUSTER.scan(str(run_d), str(work_d), with_replay=True))
        ri = safe(lambda: read_atomtop(csv_out)) if csv_out else None
        sha_fake = {nm: sha256_file(run_d / nm) for nm in ATOMTOP_SHA}
        pr = safe(lambda: check_atomtop(ri[0], ri[1], {st: (3, ke_of[st]) for st in ATOMTOP_EARLY[2:] + ATOMTOP_DUMPS}, {3.0, 0.5},
                                        replay_ref={st: (3, ke_of[st]) for st in REPLAY_REF}, sha_ref=sha_fake), ['ERR']) if ri else ['ERR']
        chk('I1 이음: 클러스터 scan() CSV (머리 · 값 꼴 · 메타 줄) = 생성기 read_atomtop · check_atomtop 통과 · 곡선 시작 300 µm · KE_CHECK 줄',
            pr == [] and abs(ri[0][0]['ztop_um'] - 300.0) < 1e-6 and len(safe(lambda: atomtop_series(ri[0]), [])) > 60
            and f'KE_CHECK {len(ATOMTOP_EARLY)}/{len(ATOMTOP_EARLY)}' in so.getvalue())
        pr2 = safe(lambda: check_atomtop(ri[0], ri[1], {st: (3, ke_of[st]) for st in ATOMTOP_EARLY[2:] + ATOMTOP_DUMPS}, {3.0, 0.5},
                                         replay_ref={st: (3, ke_of[st]) for st in REPLAY_REF}), []) if ri else []
        chk('I2 이음: 가짜 런 폴더 sha256 ≠ 리포 기록 = 문제 (⑩)', any(x.startswith('⑩') for x in pr2))
        # ── 기본판 (1저자 11-02 밤: 재현 없음 · 체크포인트 + 훑기) — 0 → 20 ms = 첫 측정점 (20,001) 에서 거꾸로 잇는 자유 낙하 모식 ──
        with contextlib.redirect_stdout(io.StringIO()) as so3:
            csv3 = safe(lambda: CLUSTER.scan(str(run_d), str(work_d)))
        r3 = safe(lambda: read_atomtop(csv3)) if csv3 else None
        pr3 = safe(lambda: check_atomtop(r3[0], r3[1], {st: (3, ke_of[st]) for st in CKPT_STEPS + ATOMTOP_DUMPS}, {3.0, 0.5},
                                         sha_ref=sha_fake), ['ERR']) if r3 else ['ERR']
        chk('I3 이음 (기본판): 클러스터 scan() 재현 없이 = #mode ckpt · #insertion 없음 · 체크포인트 10 + 덤프 48 · 생성기 검사 통과 · KE_CHECK 10/10',
            pr3 == [] and r3[1].get('mode') == 'ckpt' and 'insertion' not in r3[1] and len(r3[0]) == len(CKPT_STEPS) + len(ATOMTOP_DUMPS)
            and f'KE_CHECK {len(CKPT_STEPS)}/{len(CKPT_STEPS)}' in so3.getvalue())
        meta_ck = {k: v for k, v in meta_ok.items() if k != 'insertion'}
        meta_ck['mode'] = 'ckpt'
        rc = safe(lambda: read_atomtop(write_at(synth_rows('ckpt'), meta=meta_ck)))
        chk('C1 기본판 CSV (체크포인트 10 + 덤프 48 · #mode ckpt) 읽기 · 검사 = 문제 없음',
            rc is not None and safe(lambda: check_atomtop(rc[0], rc[1], main_ke, radii)) == [])
        chk('C2 #mode ckpt 인데 재현 행이 있다 = 문제', bool(safe(lambda: check_atomtop(synth_rows('replay'), meta_ck, main_ke, radii))))
        chk('C3 #mode replay 인데 재현 삽입 줄 없음 = 문제',
            bool(safe(lambda: check_atomtop(synth_rows('replay'), dict(meta_ck, mode='replay'), main_ke, radii))))
        chk('C4 #mode 없음 · 모르는 값 = 문제', bool(safe(lambda: check_atomtop(synth_rows('ckpt'), {k: v for k, v in meta_ck.items() if k != 'mode'},
                                                                               main_ke, radii)))
            and bool(safe(lambda: check_atomtop(synth_rows('ckpt'), dict(meta_ck, mode='both'), main_ke, radii))))
        ffs = safe(lambda: free_fall_series(290.0, 20.001, 98.1, 0.5, 1000.0), [])
        d_um = (0.5 * 0.020001 + 0.5 * 98.1 * 0.020001 ** 2) * 1000.0
        chk('F1 자유 낙하 모식: h(t) = h20 + v0·(t20 − t) + ½g(t20² − t²) · 0 ms 부터 1 ms 마다 20 ms 까지 (20.001 = 측정점이라 뺌) · '
            'h(0) = h20 + 29.62 µm · 아래로만 · 출처 = 모식 · 20.001 에서 정확히 h20',
            len(ffs) == 21 and ffs[0][0] == 0.0 and abs(ffs[0][1] - (290.0 + d_um)) < 1e-9 and abs(d_um - 29.622) < 1e-3
            and all(t < 20.001 for t, _, _ in ffs) and all(b[1] < a[1] for a, b in zip(ffs, ffs[1:]))
            and all('모식' in src for _, _, src in ffs)
            and safe(lambda: free_fall_h(20.001, 290.0, 20.001, 98.1, 0.5, 1000.0)) == 290.0)
        fc = safe(lambda: free_fall_check(325.4, 322.7, 3.0), {})
        chk('F2 h(0) 대조: 투입 영역 위끝 322.7 µm 를 넘으면 표지 (자르지 않음 · 값 그대로) · 윗면 한계 = 위끝 + 최대 반경',
            fc.get('h0_um') == 325.4 and fc.get('h0_le_region_top') is False and fc.get('h0_le_surface_bound') is True
            and abs(fc.get('surface_bound_um', 0) - 325.7) < 1e-9 and safe(lambda: free_fall_check(300.0, 322.7, 3.0), {}).get('h0_le_region_top') is True)
        ps = safe(lambda: packing_series(synth_rows('ckpt'), 'ckpt', 1e-3, 98.1, 0.5, 1000.0), [])
        chk('F3 기본판 곡선: 0 ms 모식 h(0) → … → 20 ms 모식 → 20.001 측정점 (= h20) · 20.001 전 채움 없음 · 시각 엄격 증가 · 끝 = 원 덤프',
            bool(ps) and ps[0][0] == 0.0 and '모식' in ps[0][2] and abs(ps[0][1] - (200.0 + d_um)) < 1e-9
            and next(p for p in ps if '모식' not in p[2]) == (20.001, 200.0, SRC_CKPT)
            and not any(src == SRC_INTERP and t < 20.001 for t, _, src in ps) and all(b[0] > a[0] for a, b in zip(ps, ps[1:]))
            and ps[-1][2] == SRC_DUMP and safe(lambda: packing_series(synth_rows('replay'), 'replay', 1e-3, 98.1, 0.5, 1000.0), [])[0][2] == SRC_REPLAY)
        rows_m = synth_rows()
        rows_m[at_i(rows_m, 150000)].update(orig_log_ke='3e-05')
        chk('A18 클러스터가 읽은 원 로그 KE ≠ 리포 기록 (런 KE 는 같아도) = 문제', bool(safe(lambda: check_atomtop(rows_m, meta_ok, main_ke, radii))))
        rows_m = synth_rows()
        rows_m[at_i(rows_m, 200000)].update(run_log_atoms=168400)
        chk('A19 체크포인트 덤프 원자 수 ≠ 그 run 0 로그 = 문제', bool(safe(lambda: check_atomtop(rows_m, meta_ok, main_ke, radii))))
        pdup = write_at(synth_rows())
        with open(pdup, 'a', encoding='utf-8') as f:
            f.write('#insertion,dup\n')
        chk('A16b 메타 줄 겹침 (#insertion 둘) = 거부', raises(lambda: read_atomtop(pdup)))
        rows_o = synth_rows()
        chk('A17 뺄 점이 외톨이가 아니면 거부 (ps73 규칙: 윗면 − p99.9 ≥ 20 µm 일 때만)', raises(lambda: atomtop_series(rows_o, drop={50000: 'x'})))
        rows_o[at_i(rows_o, 50000)].update(ztop_p999_um=124.0)
        ser_o = safe(lambda: atomtop_series(rows_o, drop={50000: 'bounced'}), [])
        chk('A17b 외톨이 점은 빼고 앞뒤 측정점을 잇는다 (50 ms 점 없음 · 채움으로 메움)',
            bool(ser_o) and not any(abs(t - 50.0) < 1e-9 and s != SRC_INTERP for t, _, s in ser_o)
            and any(abs(t - 50.0) < 1e-9 and s == SRC_INTERP for t, _, s in ser_o))
        ser = safe(lambda: atomtop_series(synth_rows()), [])
        meas = [p for p in ser if p[2] != SRC_INTERP]
        n_fill = sum(1 for k in range(1, 450) if k * 1000 not in set(ATOMTOP_EARLY))      # 1 ms 격자 중 측정점이 아닌 자리
        chk(f'A15 새 구간: 0.001 ms 재현점 (325 µm) 부터 · 측정점 그대로 · 0–450 ms 사이만 PCHIP 채움 {n_fill} · 시각 엄격 증가',
            bool(ser) and ser[0] == (0.001, 325.0, SRC_REPLAY) and len(meas) == len(ATOMTOP_EARLY) + len(ATOMTOP_DUMPS)
            and sum(1 for p in ser if p[2] == SRC_INTERP) == n_fill and all(0.001 < t < 450.0 for t, _, s in ser if s == SRC_INTERP)
            and all(b[0] > a[0] for a, b in zip(ser, ser[1:])) and ser[-1][2] == SRC_DUMP and abs(ser[-1][0] - 2785.002) < 1e-9)
        br = safe(lambda: broken_ranges(ser, 200.002)) if ser else None
        chk('B1 끊긴 y 축: 위 = 시작점 · 아래 = 판 놓은 뒤 전부 · 위 아래 사이 틈',
            br is not None and br[0][0] < 325.0 < br[0][1] and br[1][0] <= min(z for t, z, _ in ser if t >= 200.002)
            and br[1][1] >= max(z for t, z, _ in ser if t >= 200.002) and br[0][0] > br[1][1])
        flat = [(t, 145.0 if t < 1.5 else z, s) for t, z, s in ser]
        chk('B2 시작이 아래 범위와 겹침 (끊을 틈 없음) = 거부', bool(ser) and raises(lambda: broken_ranges(flat, 200.002)))
        rows_low = synth_rows()
        for i, r in enumerate(rows_low):                              # 시작이 낮은 침대 (160 µm) — 곡선 전체를 다시 만든다 (채운 점도 새 매듭에서)
            if r['step'] <= 50000:
                zv = 160.0 - 0.25 * i
                r.update(ztop_um=zv, zc_max_um=zv - 0.5, ztop_p999_um=zv - 0.3)
        low = safe(lambda: atomtop_series(rows_low), [])
        chk('B2b 시작 (160 µm) 이 위 범위 안이지만 위 범위가 아래 범위 (115–155) 와 겹침 = 거부',
            bool(low) and max(z for _, z, _ in low) == 160.0 and raises(lambda: broken_ranges(low, 200.002)))
        if ser and br is not None and sl is not None:
            vs_t = velocity_series((200002, 400002, 2685002, 2785002), 10.0, 1e-3)
            res = safe(lambda: draw_preview_broken(ser, vs_t, sl[0], [200.002, 400.002, 2685.002], br, 'selftest_broken', outdir=Path(tmp)), 'ERR')
            chk('B3 끊긴 축 그림 (합성 · 슬라이드판 압력) 이 그려진다 · 이름 · 화살표 겹침 검사 통과',
                res != 'ERR' and (Path(tmp) / 'selftest_broken.png').is_file())
        else:
            chk('B3 끊긴 축 그림 (구현 없음)', False)
    print(f'make_fig_d1_ms selftest: {ok} PASS · {fail} FAIL')
    return fail == 0


if __name__ == '__main__':
    if '--selftest' in sys.argv[1:]:
        sys.exit(0 if selftest() else 1)
    av = sys.argv[1:]
    if '--figsize' in av:                                 # 슬라이드 칸 크기 · 미리보기만 다른 폴더 (리포 산출 안 건드림)
        i = av.index('--figsize')
        FIGSIZE = (float(av[i + 1]), float(av[i + 2]))
    if '--preview-dir' in av:
        PREV = Path(av[av.index('--preview-dir') + 1])
    if '--hi-span' in av:                                 # 끊긴 축 위 범위 높이 (µm) · 1저자 11-03 20 ms 점 (296 µm) 이 보이게
        HI_SPAN_UM = float(av[av.index('--hi-span') + 1])
    if '--hi-frac' in av:                                 # 위 범위 눈에 보이는 높이 (아래 범위의 몫)
        HI_FRAC = float(av[av.index('--hi-frac') + 1])
    main(require_packing='--atomtop' in av)
