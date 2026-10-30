#!/usr/bin/env python3
"""50kg/batch 4차년도 DEM 보고 (7쪽 · 초안 1) — 원자료 읽기 (덱 · manifest · 끝 상태 묶음 · 계획 · 물성 기록).

생성기 (`build_kg50_report_y4.py`) 와 그림 스크립트 (`figs/make_figs_p1.py`) 가 같은 함수로 같은 값을 읽는다.
1쪽의 숫자는 전부 여기서 빌드 때 읽는다 (덱 실행 줄 · manifest · 끝 상태 덤프 · 물성 기록 문서) — 손으로 적은 숫자 없음.

읽는 것 (리포 안 · 읽기 전용):
  · 덱 넷 — v3 `docs/data/kg50_decks_20261027_v3_b50/` (D0.7 · D1 · D2) · v2 `docs/data/kg50_decks_20261026_v2/kg50_d3_b50_s1/` (D3 = 등록 §3 본 비교 자리)
    → sha256 = 그 manifest 의 `deck_sha256` (다르면 멈춤)
  · 끝 상태 묶음 둘 (tgz 를 디스크에 풀지 않고 멤버만 메모리로) — D3 `docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_end_20261027.tgz` ·
    D2 `docs/data/kg50_d2_end_20261030/kg50_d2_end_20261030_4files.tgz` → 묶음 · 멤버 sha256 = 그 폴더 기록 (README · inputs_sha256.txt)
  · 단위 = 덱 머리 `# Scale: r×1000, E×0.001, P×0.001` (길이 = µm × 1/1000 · 영률 · 압력 = 실제 × 0.001) — 이 줄이 없거나 다르면 멈춤
  · SE 영률 물성 = `docs/sulfide_se_mechanical_anchors.md` 표 (우리 DFT E_VRH · Bazzoun 2026 DEM 문헌 입력)
  · 7쪽 제목 · 결론의 꼴 = `docs/50kg/kg50_report_plan_fix_plan_20261030.md` §2 (비준 3판)
"""
import hashlib
import json
import math
import re
import tarfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

V3 = 'docs/data/kg50_decks_20261027_v3_b50'
V2 = 'docs/data/kg50_decks_20261026_v2'
D3_DIR = 'docs/data/kg50_d3_cell_verdict_20261027'
D2_DIR = 'docs/data/kg50_d2_end_20261030'
PLAN = 'docs/50kg/kg50_report_plan_fix_plan_20261030.md'
ANCHORS = 'docs/sulfide_se_mechanical_anchors.md'
#: 덱 머리의 단위 줄 (생성기 make_se_size_decks.py 가 쓰는 줄 · 이 문자열 그대로여야 한다)
SCALE_LINE = '# Scale: r×1000, E×0.001, P×0.001'
LEN_SIM_TO_UM = 1000.0          # 덱 길이 (m) × 1000 = 실제 µm  (r×1000: 실제 3 µm → 덱 3e-3)
E_SIM_TO_PA = 1.0 / 0.001        # 덱 영률 (Pa) / 0.001 = 실제 Pa
P_SIM_TO_MPA = 1.0 / 0.001       # 덱 압력 (덱 MPa) / 0.001 = 실제 MPa

#: 비교 침대 넷 — 순서 = 계획 비교 순서 0.7 → 1 → 2 → 3 (분석 계획 Q4)
BEDS = [
    dict(key='d07', case='kg50_d07_b50', deck=f'{V3}/kg50_d07_b50/input_kg50_d07_b50.liggghts', manifest=f'{V3}/manifest.json',
         end=None, status='[D0.7 본 런 전]'),
    dict(key='d1', case='kg50_d1_b50', deck=f'{V3}/kg50_d1_b50/input_kg50_d1_b50.liggghts', manifest=f'{V3}/manifest.json',
         end=None, status='[D1 해석 진행 중]'),
    dict(key='d2', case='kg50_d2_b50', deck=f'{V3}/kg50_d2_b50/input_kg50_d2_b50.liggghts', manifest=f'{V3}/manifest.json',
         end=dict(tgz=f'{D2_DIR}/kg50_d2_end_20261030_4files.tgz', record=f'{D2_DIR}/README.md',
                  deck='kg50_d2_b50/input_kg50_d2_b50.liggghts',
                  atom='kg50_d2_b50/post_kg50_d2_b50/atom_end_4015002.liggghts',
                  mesh='kg50_d2_b50/post_kg50_d2_b50/mesh_end_4015002.stl'),
         status=None),
    dict(key='d3', case='kg50_d3_b50_s1', deck=f'{V2}/kg50_d3_b50_s1/input_kg50_d3_b50_s1.liggghts', manifest=f'{V2}/manifest.json',
         end=dict(tgz=f'{D3_DIR}/kg50_d3_end_20261027.tgz', record=f'{D3_DIR}/README.md', member_record=f'{D3_DIR}/inputs_sha256.txt',
                  deck='kg50_d3_b50_s1/input_kg50_d3_b50_s1.liggghts',
                  atom='kg50_d3_b50_s1/post_kg50_d3_b50_s1/atom_end_4575002.liggghts',
                  mesh='kg50_d3_b50_s1/post_kg50_d3_b50_s1/mesh_end_4575002.stl'),
         status=None),
]
TYPE_AM, TYPE_SE = 1, 3


class SourceError(RuntimeError):
    pass


def need(cond, msg):
    if not cond:
        raise SourceError(msg)


def rp(rel):
    return REPO / rel


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(rel):
    return sha256_bytes(rp(rel).read_bytes())


# ───────────────────────────── 덱 ─────────────────────────────

def _strip_comment(line):
    """LIGGGHTS 주석 (# 뒤) 을 뗀다 — 큰따옴표 안의 # 는 남긴다."""
    out, q = [], False
    for ch in line:
        if ch == '"':
            q = not q
        if ch == '#' and not q:
            break
        out.append(ch)
    return ''.join(out).rstrip()


def exec_lines(text):
    return [s for s in (_strip_comment(l) for l in text.split('\n')) if s.strip()]


_NUM = r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)'


def _one(lines, pattern, what):
    hits = [re.fullmatch(pattern, l.strip()) for l in lines]
    hits = [h for h in hits if h]
    need(len(hits) == 1, f'deck: {what} — 실행 줄 {len(hits)} 개 (정확히 하나여야 한다) · 패턴 {pattern}')
    return hits[0].groups()


def parse_deck(text, case):
    """덱 실행 줄에서 값 (덱 단위) 을 읽고 실제 단위로 바꾼다.  줄이 없거나 둘이면 멈춘다."""
    need(text.count(SCALE_LINE) == 1, f'deck {case}: 단위 줄 "{SCALE_LINE}" 이 정확히 한 번 있어야 한다')
    L = exec_lines(text)
    d = {}
    d['r_am_sim'] = float(_one(L, rf'variable\s+r_AM_P\s+equal\s+{_NUM}', 'r_AM_P')[0])
    d['r_se_sim'] = float(_one(L, rf'variable\s+r_SE\s+equal\s+{_NUM}', 'r_SE')[0])
    d['target_sim'] = float(_one(L, rf'variable\s+target_press\s+equal\s+{_NUM}', 'target_press')[0])
    d['press_speed_sim'] = float(_one(L, rf'variable\s+press_speed\s+equal\s+{_NUM}', 'press_speed')[0])
    d['dt'] = float(_one(L, rf'variable\s+dt\s+equal\s+{_NUM}', 'dt')[0])
    bx = _one(L, rf'region\s+reg_box\s+block\s+{_NUM}\s+{_NUM}\s+{_NUM}\s+{_NUM}\s+{_NUM}\s+{_NUM}\s+units\s+box', 'reg_box')
    d['box_sim'] = tuple(float(v) for v in bx)
    E = _one(L, rf'fix\s+m1\s+all\s+property/global\s+youngsModulus\s+peratomtype\s+{_NUM}\s+{_NUM}\s+{_NUM}', 'youngsModulus')
    d['E_sim'] = tuple(float(v) for v in E)
    nu = _one(L, rf'fix\s+m2\s+all\s+property/global\s+poissonsRatio\s+peratomtype\s+{_NUM}\s+{_NUM}\s+{_NUM}', 'poissonsRatio')
    d['nu'] = tuple(float(v) for v in nu)
    t1 = _one(L, rf'fix\s+pts1\s+all\s+particletemplate/sphere\s+(\d+)\s+atom_type\s+1\s+density\s+constant\s+{_NUM}\s+radius\s+constant\s+\$\{{r_AM_P\}}', 'pts1 (AM)')
    t3 = _one(L, rf'fix\s+pts3\s+all\s+particletemplate/sphere\s+(\d+)\s+atom_type\s+3\s+density\s+constant\s+{_NUM}\s+radius\s+constant\s+\$\{{r_SE\}}', 'pts3 (SE)')
    d['rho_am_kgm3'], d['rho_se_kgm3'] = float(t1[1]), float(t3[1])
    mix = _one(L, rf'fix\s+pdd_mix\s+all\s+particledistribution/discrete\s+(\d+)\s+2\s+pts1\s+{_NUM}\s+pts3\s+{_NUM}', 'pdd_mix')
    d['w_am'], d['w_se'] = float(mix[1]), float(mix[2])
    ins = _one(L, r'print\s+"====== INSERTED \$\{n_ins\} / (\d+) \(floor (\d+) = 99%\) ======"', 'INSERTED 검사 줄')
    am = _one(L, r'print\s+"====== AM \$\{n_am_ins\} / (\d+) \(gate (\d+)-(\d+)\) ======"', 'AM 검사 줄')
    se = _one(L, r'print\s+"====== SE \$\{n_se_ins\} / (\d+) \(gate (\d+)-(\d+)\) ======"', 'SE 검사 줄')
    d['n_total_plan'], d['n_am_plan'], d['n_se_plan'] = int(ins[0]), int(am[0]), int(se[0])
    d['am_gate'], d['se_gate'] = (int(am[1]), int(am[2])), (int(se[1]), int(se[2]))
    need(d['n_total_plan'] == d['n_am_plan'] + d['n_se_plan'], f'deck {case}: 계획 합 ≠ AM + SE')
    # 실제 단위
    d['r_am_um'] = d['r_am_sim'] * LEN_SIM_TO_UM
    d['r_se_um'] = d['r_se_sim'] * LEN_SIM_TO_UM
    d['d_am_um'] = 2 * d['r_am_um']
    d['d50_se_um'] = 2 * d['r_se_um']
    d['E_am_GPa'] = d['E_sim'][0] * E_SIM_TO_PA / 1e9
    d['E_se_GPa'] = d['E_sim'][2] * E_SIM_TO_PA / 1e9
    d['target_MPa'] = d['target_sim'] * P_SIM_TO_MPA
    d['box_x_um'] = (d['box_sim'][1] - d['box_sim'][0]) * LEN_SIM_TO_UM
    d['box_y_um'] = (d['box_sim'][3] - d['box_sim'][2]) * LEN_SIM_TO_UM
    d['rho_am_gcc'] = d['rho_am_kgm3'] / 1000.0
    d['rho_se_gcc'] = d['rho_se_kgm3'] / 1000.0
    d['monodisperse'] = True            # 두 템플릿 모두 `radius constant` (위 패턴이 강제)
    return d


def normalize_deck(text, case, r_se_text):
    """덱 실행 줄에서 케이스 이름 · SE 반지름 · 시드 · 계획 입자 수 (검사 구간) · SE D50 표기를 자리표로 바꾼다 (덱 넷 대조용)."""
    out = []
    tag = case.upper()
    for l in exec_lines(text):
        s = l.replace(case, '<CASE>').replace(tag, '<CASE>')
        s = re.sub(r'(variable\s+r_SE\s+equal\s+)' + re.escape(r_se_text), r'\1<RSE>', s)
        s = re.sub(r'(particletemplate/sphere\s+)\d+', r'\1<SEED>', s)
        s = re.sub(r'(particledistribution/discrete\s+)\d+', r'\1<SEED>', s)
        s = re.sub(r'(insert/pack\s+seed\s+)\d+', r'\1<SEED>', s)
        s = re.sub(r'(INSERTED \$\{n_ins\} / )\d+( \(floor )\d+', r'\1<N>\2<N>', s)
        s = re.sub(r'(SE \$\{n_se_ins\} / )\d+( \(gate )\d+-\d+', r'\1<N>\2<N>-<N>', s)
        s = re.sub(r'(\$\{n_ins\} < )\d+', r'\1<N>', s)
        s = re.sub(r'(\$\{n_se_ins\} < )\d+( \|\| \$\{n_se_ins\} > )\d+', r'\1<N>\2<N>', s)
        s = re.sub(r'SE D50 [\d.]+um', 'SE D50 <D>um', s)
        out.append(s)
    return out


def read_manifest_case(rel, case):
    m = json.loads(rp(rel).read_text(encoding='utf-8'))
    hits = [c for c in m['cases'] if c['case'] == case]
    need(len(hits) == 1, f'manifest {rel}: case {case} 가 정확히 하나여야 한다')
    return m, hits[0]


# ───────────────────────────── 끝 상태 묶음 ─────────────────────────────

def _recorded_tgz_sha(record_rel, tgz_name):
    t = rp(record_rel).read_text(encoding='utf-8')
    lines = [l for l in t.split('\n') if tgz_name in l and 'sha256' in l]
    shas = sorted({m for l in lines for m in re.findall(r'`([0-9a-f]{64})`', l)})
    need(len(shas) == 1, f'{record_rel}: {tgz_name} 의 sha256 기록이 하나여야 한다 ({shas})')
    return shas[0]


def _recorded_member_shas(end):
    """멤버 sha256 기록 — D3 = inputs_sha256.txt (`sha  ./path`) · D2 = README 표 (`| path | 바이트 | `sha` |`)."""
    rec = {}
    if 'member_record' in end:
        for l in rp(end['member_record']).read_text(encoding='utf-8').split('\n'):
            m = re.fullmatch(r'([0-9a-f]{64})\s+\./(\S+)', l.strip())
            if m:
                rec[m.group(2)] = m.group(1)
    else:
        for l in rp(end['record']).read_text(encoding='utf-8').split('\n'):
            m = re.fullmatch(r'\|\s*(\S+)\s*\|\s*[\d,]+\s*\|\s*`([0-9a-f]{64})`\s*\|', l.strip())
            if m:
                rec[m.group(1)] = m.group(2)
    return rec


def parse_atom_dump(blob):
    lines = blob.decode('ascii').split('\n')
    i = lines.index('ITEM: TIMESTEP')
    step = int(lines[i + 1])
    n = int(lines[lines.index('ITEM: NUMBER OF ATOMS') + 1])
    j = next(k for k, l in enumerate(lines) if l.startswith('ITEM: BOX BOUNDS'))
    bounds = lines[j].split()[3:]
    box = [tuple(float(v) for v in lines[j + 1 + k].split()) for k in range(3)]
    h = next(k for k, l in enumerate(lines) if l.startswith('ITEM: ATOMS'))
    cols = lines[h].split()[2:]
    rows = lines[h + 1:h + 1 + n]
    need(len(rows) == n and all(rows), 'atom dump: 줄 수 ≠ NUMBER OF ATOMS')
    data = np.array(' '.join(rows).split(), dtype=float).reshape(n, len(cols))
    c = {k: q for q, k in enumerate(cols)}
    return dict(step=step, n=n, box=box, bounds=bounds, cols=cols,
                id=data[:, c['id']].astype(int), type=data[:, c['type']].astype(int),
                x=data[:, c['x']], y=data[:, c['y']], z=data[:, c['z']], r=data[:, c['radius']])


def parse_mesh_z(blob):
    zs = [float(m) for m in re.findall(r'vertex\s+\S+\s+\S+\s+(\S+)', blob.decode('ascii'))]
    need(len(zs) == 6 and max(zs) - min(zs) == 0.0, f'mesh: 평평한 두 면 (꼭짓점 6, z 같음) 이 아니다 ({zs})')
    return zs[0]


def read_end_state(bed):
    """끝 상태 묶음에서 덱 · atom · mesh 멤버를 메모리로 읽는다 (sha256 = 기록) — 디스크에 풀지 않는다."""
    end = bed['end']
    tgz = end['tgz']
    tgz_sha = sha256_file(tgz)
    need(tgz_sha == _recorded_tgz_sha(end['record'], Path(tgz).name), f'{tgz}: sha256 ≠ 기록')
    rec = _recorded_member_shas(end)
    out = dict(tgz=tgz, tgz_sha256=tgz_sha, members={})
    with tarfile.open(rp(tgz), 'r:gz') as tf:
        blobs = {}
        for k in ('deck', 'atom', 'mesh'):
            name = end[k]
            m = tf.getmember(name)
            need(m.isfile(), f'{tgz}: {name} 가 파일이 아니다')
            b = tf.extractfile(m).read()
            s = sha256_bytes(b)
            need(rec.get(name) == s, f'{tgz}: {name} sha256 {s[:12]}… ≠ 기록 {str(rec.get(name))[:12]}…')
            blobs[k] = b
            out['members'][name] = s
    out['deck_sha256'] = out['members'][end['deck']]
    a = parse_atom_dump(blobs['atom'])
    out['atoms'] = a
    out['step'] = a['step']
    out['plate_z_sim'] = parse_mesh_z(blobs['mesh'])
    out['plate_z_um'] = out['plate_z_sim'] * LEN_SIM_TO_UM
    out['n_am'] = int((a['type'] == TYPE_AM).sum())
    out['n_se'] = int((a['type'] == TYPE_SE).sum())
    need(out['n_am'] + out['n_se'] == a['n'], 'atom dump: AM · SE 밖의 형식 (type) 이 있다')
    return out


# ───────────────────────────── 계획 · 물성 기록 ─────────────────────────────

def plan_rows():
    """비준 3판 7쪽 표 (§2) — [(쪽, 제목, 주 그림, 보조, 결론의 꼴)] · 마크다운 강조 (*, `) 는 뗀다."""
    t = rp(PLAN).read_text(encoding='utf-8')
    sec = t.split('## 2.', 1)[1].split('\n## ', 1)[0]
    rows = []
    for l in sec.split('\n'):
        m = re.fullmatch(r'\|\s*(\d)\s*\|(.+)\|', l.strip())
        if not m:
            continue
        cells = [c.strip().replace('*', '').replace('`', '') for c in m.group(2).split('|')]
        need(len(cells) == 4, f'plan §2 row {m.group(1)}: 칸 넷이 아니다')
        rows.append(dict(page=int(m.group(1)), title=cells[0], main=cells[1], aux=cells[2], conclusion=cells[3]))
    need([r['page'] for r in rows] == list(range(1, 8)), f'plan §2: 쪽 1–7 이 아니다 ({[r["page"] for r in rows]})')
    return rows


def se_modulus_anchors():
    """SE 영률 물성 — 우리 DFT E_VRH · DEM 문헌 입력 (Bazzoun 2026) — `docs/sulfide_se_mechanical_anchors.md` 표 줄."""
    t = rp(ANCHORS).read_text(encoding='utf-8')
    m = re.search(r'^\|\s*우리 DFT \(E_VRH / modelc\)\s*\|\s*([\d.]+) / ([\d.]+) GPa\s*\|', t, flags=re.M)
    b = re.search(r'^\|\s*Bazzoun 2026 \(같은 재료·같은 코드\)\s*\|\s*([\d.]+) GPa\s*\|', t, flags=re.M)
    need(m and b, f'{ANCHORS}: DFT E_VRH · Bazzoun 줄을 찾지 못했다')
    return dict(dft_evrh_GPa=float(m.group(1)), dft_modelc_GPa=float(m.group(2)), bazzoun_GPa=float(b.group(1)))


# ───────────────────────────── 1쪽 자료 ─────────────────────────────

def throat_factor():
    """세 구가 맞닿은 평면 목의 내접원 지름 / 구 지름 = 2/√3 − 1 (이상화)."""
    return 2.0 / math.sqrt(3.0) - 1.0


def load_all(with_end=True):
    """침대 넷의 덱 · manifest · (있으면) 끝 상태 → dict.  모든 대조가 여기서 일어난다 (실패 = SourceError)."""
    beds = []
    for b in BEDS:
        text = rp(b['deck']).read_text(encoding='utf-8')
        sha = sha256_bytes(text.encode('utf-8'))
        man, mc = read_manifest_case(b['manifest'], b['case'])
        need(sha == mc['deck_sha256'], f"{b['deck']}: sha256 ≠ manifest deck_sha256")
        d = parse_deck(text, b['case'])
        need(abs(d['r_se_um'] - mc['r_se_um']) < 1e-12 and abs(d['r_am_um'] - mc['r_am_um']) < 1e-12, f"{b['case']}: 덱 반지름 ≠ manifest")
        need(abs(d['d50_se_um'] - mc['d50_se_um']) < 1e-12, f"{b['case']}: 덱 D50 ≠ manifest")
        need(d['n_am_plan'] == mc['counts_pred']['AM_P'] and d['n_se_plan'] == mc['counts_pred']['SE'], f"{b['case']}: 계획 수 ≠ manifest")
        need(abs(d['box_x_um'] - mc['box_um']) < 1e-9 and abs(d['box_y_um'] - mc['box_um']) < 1e-9, f"{b['case']}: 영역 ≠ manifest")
        need(abs(d['w_am'] - mc['am_mass']) < 1e-12, f"{b['case']}: AM 질량분율 ≠ manifest")
        need(abs(d['rho_am_gcc'] - mc['dens_g_cm3']['AM']) < 1e-12 and abs(d['rho_se_gcc'] - mc['dens_g_cm3']['SE']) < 1e-12,
             f"{b['case']}: 진밀도 ≠ manifest")
        rse_text = _one(exec_lines(text), rf'variable\s+r_SE\s+equal\s+{_NUM}', 'r_SE')[0]
        rec = dict(b, sha256=sha, deck_vals=d, manifest_case=mc, manifest_config=man['config'],
                   norm=normalize_deck(text, b['case'], rse_text), endstate=None)
        if with_end and b['end']:
            es = read_end_state(b)
            need(es['deck_sha256'] == sha, f"{b['case']}: 끝 상태 묶음 안 덱 ≠ 리포 덱")
            need(abs(es['atoms']['box'][0][1] - es['atoms']['box'][0][0] - d['box_sim'][1] + d['box_sim'][0]) < 1e-12, f"{b['case']}: 덤프 상자 ≠ 덱")
            r_am = es['atoms']['r'][es['atoms']['type'] == TYPE_AM]
            r_se = es['atoms']['r'][es['atoms']['type'] == TYPE_SE]
            need(np.all(r_am == d['r_am_sim']) and np.all(r_se == d['r_se_sim']), f"{b['case']}: 덤프 반지름 ≠ 덱 (단분산)")
            need(d['am_gate'][0] <= es['n_am'] <= d['am_gate'][1] and d['se_gate'][0] <= es['n_se'] <= d['se_gate'][1],
                 f"{b['case']}: 끝 상태 상별 수가 덱 검사 구간 밖")
            rec['endstate'] = es
        beds.append(rec)
    # 덱 넷 = 같은 실행 줄 (케이스 이름 · SE 반지름 · 시드 · 계획 SE 수 · D50 표기 빼고)
    ref = beds[0]['norm']
    for r in beds[1:]:
        need(r['norm'] == ref, f"덱 실행 줄이 {beds[0]['case']} 와 {r['case']} 사이에서 등록한 자리 밖에서 다르다")
    common = {}
    for k in ('r_am_um', 'w_am', 'w_se', 'rho_am_gcc', 'rho_se_gcc', 'E_am_GPa', 'E_se_GPa', 'target_MPa', 'box_x_um', 'box_y_um',
              'n_am_plan', 'press_speed_sim', 'dt'):
        vals = {r['deck_vals'][k] for r in beds}
        need(len(vals) == 1, f'공통 조건 {k} 가 덱마다 다르다: {vals}')
        common[k] = vals.pop()
    for k in ('loading_target_mah_cm2', 'cap_mah_g', 'loading_pred_mah_cm2'):
        vals = {r['manifest_case'][k] for r in beds}
        need(len(vals) == 1, f'manifest {k} 가 케이스마다 다르다: {vals}')
        common[k] = vals.pop()
    need(len({r['deck_vals']['d50_se_um'] for r in beds}) == len(beds), 'SE D50 이 겹친다 (입도마다 덱 하나)')
    common['d_am_um'] = 2 * common['r_am_um']
    common['throat_um'] = throat_factor() * common['d_am_um']
    common['seeds_per_size'] = 1           # 입도마다 덱 하나 (BEDS 의 D50 이 서로 다름 · 위에서 강제)
    common['anchors'] = se_modulus_anchors()
    return beds, common


# ───────────────────────────── 표기 ─────────────────────────────

SUP = str.maketrans('0123456789-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻')


def fmt_count(n):
    """입자 수: 네 자리까지 그대로 · 다섯 자리 이상 = a.bcd × 10ⁿ (천 단위 콤마 쓰지 않음 · 보고 원칙 §6)."""
    n = int(n)
    if n < 10000:
        return str(n)
    e = int(math.floor(math.log10(n)))
    return f'{n / 10 ** e:.3f} × 10{str(e).translate(SUP)}'


def fmt_g(v, nd=3):
    """정수에 가까우면 정수 · 아니면 유효 소수 nd 자리 이하 (끝 0 없음)."""
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    s = f'{v:.{nd}f}'.rstrip('0').rstrip('.')
    return s


def bed_label(b):
    return 'D' + fmt_g(b['deck_vals']['d50_se_um'])


if __name__ == '__main__':
    beds, common = load_all()
    for b in beds:
        d = b['deck_vals']
        es = b['endstate']
        print(bed_label(b), b['case'], 'D50', d['d50_se_um'], 'plan', d['n_am_plan'], d['n_se_plan'],
              'end' if es else '-', (es['step'], es['n_am'], es['n_se'], round(es['plate_z_um'], 3)) if es else b['status'])
    print({k: v for k, v in common.items() if k != 'anchors'}, common['anchors'])
