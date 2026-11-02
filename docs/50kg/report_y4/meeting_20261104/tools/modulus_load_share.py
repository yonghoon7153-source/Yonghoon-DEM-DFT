"""50kg 2 µm SE 영률 세 침대 (D2 · D2E05 · D2E15) — 접촉 종류별 σzz 몫 · AM–SE 접촉 압력 (읽기 전용 · 새 정의 없음).

    python3 -I modulus_load_share.py <리포> <출력 폴더> [--data-root <draft2 출력 뿌리 (변형 침대 metrics)>] [침대 …]

값 (침대마다 · 같은 끝 세트 · 같은 접촉력 · 같은 가지 벡터):
  ① Contribution to σ_zz (21 단면 · 하중 가중) = scripts/plane_load_share.py 그대로 (덱 부록 표 · values/szz_share 와 같은 양)
  ② 창 적분 (1/V) Σ_c f_z l_z 의 접촉 종류별 몫 = 같은 함수의 `contribution_sigma_zz_integral_pct` (벽에서 2 r_max 밖 창 · 상자 평균 virial)
  ③ 상자 전체 virial 몫 = Σ_c f_z^up (z_up − z_down) (모든 입자–입자 접촉 · 벽 접촉은 덤프에 없음) — ②의 창 없는 판 (참고)
  ④ AM–SE 접촉 압력 = |F_n| ÷ 접촉 면적 (contact_area = c_cpl[22] · 법선력이 밀어내는 접촉만 = F_n · (x₁ − x₂) > 0) — 접촉 평균 ·
     중앙값 · Σ|F_n| ÷ ΣA (면적 가중) · 단위 MPa = 덱 힘 ÷ 덱 면적 × scale ÷ 1e6
     ⛔ 진단 전용 — 독립 결과가 아니다: 선형 스프링 접촉 (F = k_n δ) + 겹침 기반 면적 (A = π R* δ) 이면 F/A ≈ k_n / (π R*) = 접촉 강성이
     정하는 값 (E_SE^0.8 · R* 에 비례 — 0.675 · 1.35 · 2.025 GPa 예측 비 0.57 · 1 · 1.38 ↔ 실측 0.60 · 1 · 1.33 · 11-02 메인 세션 정정) ·
     덱 · 보고에 쓰지 않는다 (영률 장 검사기가 '접촉점 압력' 낱말을 막는다)
입력 = draft2 metrics_<침대>.json 의 끝 세트 (묶음 sha256 · 멤버 sha256 대조 · 다르면 멈춤) → 빈 작업 폴더 → scripts/parse_liggghts.py (웹앱 파서)
  → atoms.csv · contacts.csv · mesh_info.json · input_params.json.  변형 침대 = 웹앱에 올린 매개 덱 (run_draft2_metrics.e_deck_check ·
  sha256 = 기록) 으로 파싱 (E 덱은 재개 덱이라 상자 줄이 없다).  D2 = 리포 기록 · 변형 = --data-root/data/<침대>/.
"""
import hashlib
import importlib
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

import numpy as np

GROUPS = ('AM–AM', 'AM–SE', 'SE–SE')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_record(R, bed, data_root):
    p = R.BASE_D2_RECORD if bed == 'D2' else Path(data_root) / 'data' / bed / f'metrics_{bed}.json'
    if not p.is_file():
        return None, p
    m = json.loads(p.read_text(encoding='utf-8'))
    if m.get('schema') != R.SCHEMA or m.get('bed') != bed:
        raise SystemExit(f'{p}: schema · 침대 이름이 다르다')
    return m, p


def extract(R, repo, bed, m, indir):
    end = m['provenance']['end_set']
    tgz = Path(end['tgz'])
    tgz = tgz if tgz.is_absolute() else repo / tgz
    raw = tgz.read_bytes()
    if sha(raw) != end['tgz_sha256']:
        raise SystemExit(f'{bed}: 묶음 sha256 ≠ 기록 ({tgz})')
    indir.mkdir(parents=True)
    with tarfile.open(tgz, 'r:gz') as tf:
        for name, rec in end['members'].items():
            b = tf.extractfile(tf.getmember(name)).read()
            if sha(b) != rec['sha256']:
                raise SystemExit(f'{bed}: 멤버 {name} sha256 ≠ 기록')
            if rec['role'] == 'deck' and bed in R.E_BEDS:            # 웹앱과 같은 매개 덱 (상자 줄 있음)
                _d, info = R.deck_check(bed, b)
                b = info['webapp_deck_blob']
                if sha(b) != m['provenance']['deck']['webapp_deck']['sha256']:
                    raise SystemExit(f'{bed}: 매개 덱 sha256 ≠ 기록')
            (indir / Path(name).name).write_bytes(b)
    return dict(tgz=str(tgz), tgz_sha256=end['tgz_sha256'], end_step=end['end_step'])


def virial_and_pressure(res, tmap, scale, plate_z, box):
    import pandas as pd
    a = pd.read_csv(res / 'atoms.csv', low_memory=False)
    c = pd.read_csv(res / 'contacts.csv', low_memory=False)
    ids = a['id'].to_numpy(np.int64)
    order = np.argsort(ids)
    ids = ids[order]
    X = a[['x', 'y', 'z']].to_numpy(float)[order]
    name = np.array([tmap[int(t)] for t in a['type'].to_numpy(np.int64)[order]])
    i1 = np.searchsorted(ids, c['id1'].to_numpy(np.int64))
    i2 = np.searchsorted(ids, c['id2'].to_numpy(np.int64))
    if not (np.all(ids[i1] == c['id1'].to_numpy(np.int64)) and np.all(ids[i2] == c['id2'].to_numpy(np.int64))):
        raise SystemExit('접촉 id 가 atoms 에 없다')
    f = c[['fx', 'fy', 'fz']].to_numpy(float) if {'fx', 'fy', 'fz'} <= set(c.columns) else \
        c[['fn_x', 'fn_y', 'fn_z']].to_numpy(float) + c[['ft_x', 'ft_y', 'ft_z']].to_numpy(float)
    fn = c[['fn_x', 'fn_y', 'fn_z']].to_numpy(float)
    area = c['contact_area'].to_numpy(float)
    l = X[i1] - X[i2]                                               # 가지 벡터 (id2 → id1 · x · y 최소영상)
    bx, by = box
    l[:, 0] -= bx * np.round(l[:, 0] / bx)
    l[:, 1] -= by * np.round(l[:, 1] / by)
    grp = np.array([('AM–AM' if ('AM' in p and 'AM' in q) else 'AM–SE' if ('AM' in p) != ('AM' in q) else 'SE–SE')
                    for p, q in zip(name[i1], name[i2])])
    szz = f[:, 2] * l[:, 2]                                         # f = id1 이 받는 힘 · σ = (1/V) Σ f ⊗ l (압축 양수)
    tot = float(szz.sum())
    V = bx * by * plate_z
    box_share = {g: 100.0 * float(szz[grp == g].sum()) / tot for g in GROUPS}
    box_mpa = tot / V * scale / 1e6
    # AM–SE 접촉 압력 (밀어내는 법선력만)
    push = np.einsum('ij,ij->i', fn, l) > 0
    am_se = (grp == 'AM–SE') & push & np.isfinite(area) & (area > 0)
    fnm = np.linalg.norm(fn, axis=1)
    p = fnm[am_se] / area[am_se] * scale / 1e6
    out = dict(box_virial_share_pct=box_share, box_virial_sigma_zz_mpa=box_mpa, n_contacts=int(len(c)),
               am_se_contact_pressure=dict(mean_MPa=float(p.mean()), median_MPa=float(np.median(p)),
                                          area_weighted_MPa=float(fnm[am_se].sum() / area[am_se].sum() * scale / 1e6),
                                          p10_MPa=float(np.percentile(p, 10)), p90_MPa=float(np.percentile(p, 90)),
                                          n=int(am_se.sum()), n_am_se=int((grp == 'AM–SE').sum()),
                                          n_not_pushing=int(((grp == 'AM–SE') & ~push).sum()),
                                          n_area_le0=int(((grp == 'AM–SE') & push & ~(np.isfinite(area) & (area > 0))).sum())))
    return out


def one(repo, R, PLS, bed, data_root):
    m, p = load_record(R, bed, data_root)
    if m is None:
        return dict(status='NO_RECORD', record=str(p))
    with tempfile.TemporaryDirectory(prefix=f'modls_{bed}_') as td:
        indir = Path(td) / 'in'
        end = extract(R, repo, bed, m, indir)
        res = Path(td) / 'results'
        files = sorted(str(q) for q in indir.iterdir())
        r = subprocess.run([sys.executable, '-I', str(repo / 'scripts/parse_liggghts.py'), *files, '-o', str(res)], capture_output=True, text=True)
        if r.returncode != 0:
            raise SystemExit(f'{bed}: parse_liggghts rc {r.returncode}\n{r.stderr[-800:]}')
        argv = m['provenance']['network_provenance']['argv']
        meta = Path(td) / 'meta.json'
        meta.write_text(json.dumps({'type_map': argv['type_map'], 'scale': argv['scale']}), encoding='utf-8')
        pls = PLS.run_one(res, meta)
        ip = json.loads((res / 'input_params.json').read_text(encoding='utf-8'))
        plate_z = float(json.loads((res / 'mesh_info.json').read_text(encoding='utf-8'))['plate_z'])
        tmap = PLS.parse_type_map(argv['type_map'])
        vp = virial_and_pressure(res, tmap, float(argv['scale']), plate_z, (float(ip['box_x']), float(ip['box_y'])))
    if abs(plate_z * float(argv['scale']) - m['metrics']['plate_z_um']) > 1e-9:
        raise SystemExit(f'{bed}: 판 높이 ≠ metrics')
    mm = m['metrics']
    return dict(status='OK', record=str(p), end_set=end, se_E_GPa=(m.get('variant') or {}).get('se_E_GPa'),
                p_end_MPa=mm['p_end_MPa'], lw_am_nowall_median_MPa=mm['lw_am_nowall_median_MPa'],
                lw_am_over_p_end=mm['lw_am_nowall_median_MPa'] / mm['p_end_MPa'],
                plane21=dict(status=pls['status'], why=pls.get('why'), contribution_sigma_zz_pct=pls['contribution_sigma_zz_pct'],
                             sigma_zz_planes_mean_mpa=pls['sigma_zz_planes_mean_mpa'],
                             conservation_max_over_min=pls['conservation_max_over_min'], balance_residual=pls['balance_residual']),
                window_integral=dict(contribution_pct=pls['contribution_sigma_zz_integral_pct'],
                                     sigma_zz_mpa=pls['sigma_zz_window_integral_mpa'], window_um=pls['window_um']),
                alpha=dict(status=pls['alpha'].get('status'), alpha_zz=pls['alpha'].get('alpha_zz')),
                **vp)


def main():
    repo = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2])
    args = sys.argv[3:]
    data_root = None
    if '--data-root' in args:
        k = args.index('--data-root')
        data_root = args[k + 1]
        args = args[:k] + args[k + 2:]
    beds = args or ['D2', 'D2E05', 'D2E15']
    for p in (repo / 'scripts', repo / 'docs/50kg/report_y4/draft2'):
        sys.path.insert(0, str(p))
    R = importlib.import_module('run_draft2_metrics')
    PLS = importlib.import_module('plane_load_share')
    data_root = Path(data_root) if data_root else R.HERE
    res = {}
    for bed in beds:
        res[bed] = one(repo, R, PLS, bed, data_root)
        c = res[bed]
        if c['status'] == 'OK':
            print(f"{bed}: E {c['se_E_GPa']} · P_end {c['p_end_MPa']:.3f} · σVM_AM/P {c['lw_am_over_p_end']:.4f} · "
                  f"21단면 {', '.join(f'{g} {v:.2f}' for g, v in c['plane21']['contribution_sigma_zz_pct'].items())} ({c['plane21']['status']}) · "
                  f"창적분 {', '.join(f'{g} {v:.2f}' for g, v in c['window_integral']['contribution_pct'].items())} · "
                  f"상자 {', '.join(f'{g} {v:.2f}' for g, v in c['box_virial_share_pct'].items())} (σzz {c['box_virial_sigma_zz_mpa']:.1f} MPa) · "
                  f"AM–SE 압력 평균 {c['am_se_contact_pressure']['mean_MPa']:.1f} · 중앙 {c['am_se_contact_pressure']['median_MPa']:.1f} · "
                  f"면적가중 {c['am_se_contact_pressure']['area_weighted_MPa']:.1f} MPa (n {c['am_se_contact_pressure']['n']})", flush=True)
        else:
            print(f'{bed}: {c["status"]} ({c["record"]})')
    out.mkdir(parents=True, exist_ok=True)
    doc = dict(tool='docs/50kg/report_y4/meeting_20261104/tools/modulus_load_share.py', definition=__doc__.split('\n\n')[1],
               plane_load_share_sha256=sha((repo / 'scripts/plane_load_share.py').read_bytes()), beds=res)
    (out / 'modulus_load_share.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1, default=float) + '\n', encoding='utf-8')
    print('→', out / 'modulus_load_share.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
