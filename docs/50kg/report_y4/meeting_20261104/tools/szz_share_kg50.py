"""50kg D1 · D2 · D3 접촉 종류별 σzz 기여 (이종기술 3세부 2차년도 18쪽 '입자 접촉 및 응력 분담' 과 같은 양) — 읽기 전용.

계산 = scripts/plane_load_share.py 그대로 (21 단면 하중 가중 몫 · 벽에서 2 r_max 밖 · 보존 · 평형 검사 · α) — 새 정의 없음.
입력 = 끝 세트 묶음 (판 고정 이완 끝 · atom · contact · mesh 같은 step) — 경로 · sha256 = draft2 metrics_<침대>.json provenance.end_set.
  묶음 sha256 · 멤버 sha256 이 기록과 다르면 멈춘다 → 빈 작업 폴더에 멤버 넷 (basename) → scripts/parse_liggghts.py (웹앱과 같은 파서)
  → atoms.csv · contacts.csv · mesh_info.json · input_params.json → meta.json (type_map · scale = 그 JSON 의 network_provenance.argv).
  묶음이 리포에 없는 침대 (D1 · 62.7 MB · .gitignore) = 낱개 파일 (--loose D1=<폴더>) — 그 폴더의 atom_end · contact_end · mesh_end 를
  기록된 멤버 sha256 과 대조 (다르면 멈춤) · 덱 = 리포 덱 (sha256 = 기록된 덱 멤버).
usage: python3 -I szz_share_kg50.py <리포> <출력 폴더> [--loose D1=<폴더>] [침대 …]   (침대 기본 D3 D2 D1)
"""
import hashlib
import importlib
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

REPO = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
ARGS = sys.argv[3:]
LOOSE = dict(a.split('=', 1) for a in (ARGS[i + 1] for i, x in enumerate(ARGS) if x == '--loose'))
BEDS = [a for i, a in enumerate(ARGS) if a != '--loose' and (i == 0 or ARGS[i - 1] != '--loose')] or ['D3', 'D2', 'D1']
LABEL = {'D3': 'SE3um', 'D2': 'SE2um', 'D1': 'SE1um'}
sys.path.insert(0, str(REPO / 'scripts'))
PLS = importlib.import_module('plane_load_share')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def one(bed, work):
    m = json.loads((REPO / f'docs/50kg/report_y4/draft2/data/{bed}/metrics_{bed}.json').read_text(encoding='utf-8'))
    end = m['provenance']['end_set']
    tgz = REPO / end['tgz']
    if bed in LOOSE:
        return one_loose(bed, work, m, end, Path(LOOSE[bed]))
    if not tgz.is_file():                      # D1 끝 묶음 = 리포 밖 (.gitignore · 62.7 MB) — 없으면 그 침대만 값 없음
        return {'status': 'FAILED', 'why': [f'끝 묶음 없음: {end["tgz"]} (리포 밖 · sha256 {end["tgz_sha256"][:16]}… 묶음을 받아야 계산)'],
                'case_id': m['case'], 'end_set': {'tgz': end['tgz'], 'tgz_sha256': end['tgz_sha256'], 'end_step': end['end_step']}}
    raw = tgz.read_bytes()
    if sha(raw) != end['tgz_sha256']:
        raise SystemExit(f'{bed}: 묶음 sha256 ≠ 기록')
    indir = Path(work) / 'in'
    indir.mkdir(parents=True)
    with tarfile.open(tgz, 'r:gz') as tf:
        for name, rec in end['members'].items():
            b = tf.extractfile(tf.getmember(name)).read()
            if sha(b) != rec['sha256']:
                raise SystemExit(f'{bed}: 멤버 {name} sha256 ≠ 기록')
            (indir / Path(name).name).write_bytes(b)
    return finish(bed, work, m, end, indir, 'tgz')


def one_loose(bed, work, m, end, folder):
    indir = Path(work) / 'in'
    indir.mkdir(parents=True)
    for name, rec in end['members'].items():
        base = Path(name).name
        src_p = folder / base
        if rec['role'] == 'deck' and not src_p.is_file():
            src_p = REPO / m['provenance']['deck']['repo_deck']      # 덱 = 리포 덱 (아래 sha256 대조)
        b = src_p.read_bytes()
        if sha(b) != rec['sha256']:
            raise SystemExit(f'{bed}: {src_p} sha256 {sha(b)[:16]}… ≠ 기록 멤버 {base} {rec["sha256"][:16]}…')
        (indir / base).write_bytes(b)
    return finish(bed, work, m, end, indir, f'loose files = recorded member sha256 ({len(end["members"])})')


def finish(bed, work, m, end, indir, how):
    res = Path(work) / 'results'
    files = sorted(str(p) for p in indir.iterdir())
    r = subprocess.run([sys.executable, '-I', str(REPO / 'scripts/parse_liggghts.py'), *files, '-o', str(res)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f'{bed}: parse_liggghts rc {r.returncode}\n{r.stderr[-800:]}')
    argv = m['provenance']['network_provenance']['argv']
    meta = Path(work) / 'meta.json'
    meta.write_text(json.dumps({'type_map': argv['type_map'], 'scale': argv['scale']}), encoding='utf-8')
    out = PLS.run_one(res, meta)
    out['case_id'] = m['case']
    out['end_set'] = {'tgz': end['tgz'], 'tgz_sha256': end['tgz_sha256'], 'end_step': end['end_step'], 'input': how,
                      'members_sha256': {Path(n).name: r['sha256'] for n, r in end['members'].items()}}
    for k in ('results_dir', 'meta'):          # 지워질 작업 폴더 경로 = 기록에서 뺀다
        out.pop(k, None)
    return out


cases, order = {}, []
for bed in BEDS:
    with tempfile.TemporaryDirectory() as td:
        cases[LABEL[bed]] = one(bed, td)
        order.append(LABEL[bed])
        c = cases[LABEL[bed]]
        print(bed, c.get('status'), c.get('contribution_sigma_zz_pct'), flush=True)
results = {'tool': 'plane_load_share (via szz_share_kg50.py)', 'definition': PLS.DEFINITION,
           'tolerances': {'conservation': PLS.CONSERVE_TOL, 'balance': PLS.BALANCE_TOL, 'alpha_closure_identity': PLS.ALPHA_TOL},
           'n_cuts': PLS.N_CUTS, 'code_sha256': PLS._sha(Path(PLS.__file__)), 'order': order, 'cases': cases}
PLS.write_outputs(results, OUT)
PLS.print_report(results)
