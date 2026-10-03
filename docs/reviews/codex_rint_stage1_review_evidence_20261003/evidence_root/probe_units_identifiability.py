"""Read-only dimensional check of draft 4-3 using the pinned production face function."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source' / 'scripts'))
import step3_sigma as s3


def junction(Rj_ohm, n, h_um):
    sigma = np.full(n, 1e8)  # finite near-equipotential endpoint material, S/cm
    g0 = sigma * h_um
    raw_r = Rj_ohm * n * h_um**2
    correct_r = raw_r * 1e-8
    def actual(r):
        # code conductance [S/cm * um] -> physical [S]
        faces = s3.interface_face_g(g0, sigma, sigma, np.full(n, r), h_um)
        return float(faces.sum() * 1e-4)
    expected_with_half_cells = 1 / (Rj_ohm + 1 / (1e8*h_um*1e-4*n))
    good, bad = actual(correct_r), actual(raw_r)
    assert np.isclose(good, expected_with_half_cells, rtol=1e-13)
    return dict(Rj_ohm=Rj_ohm, n_faces=n, vox_um=h_um,
                draft_literal_r_ohm_cm2=raw_r, converted_r_ohm_cm2=correct_r,
                correct_G_S=good, literal_G_S=bad,
                resistance_inflation=good/bad,
                expected_G_with_bulk_half_cells_S=expected_with_half_cells)


def identifiable():
    # One pellet measurement cannot separate grain and interface parameters.
    L_cm, A_cm2, n = 0.01, 1e-6, 10
    effective_sigma = 0.003
    R_target = L_cm / (effective_sigma*A_cm2)
    rows = []
    for grain_sigma in (0.003, 0.006, 0.03):
        r = (R_target-L_cm/(grain_sigma*A_cm2))*A_cm2/n
        R = L_cm/(grain_sigma*A_cm2) + n*r/A_cm2
        rows.append(dict(grain_sigma_S_cm=grain_sigma, per_boundary_r_ohm_cm2=r,
                         recovered_effective_sigma_S_cm=L_cm/(R*A_cm2)))
    return dict(note='Synthetic 1D identifiability example; not fitted material values.',
                L_um=L_cm*1e4, A_um2=A_cm2*1e8, interfaces=n, rows=rows)


def verify_sources():
    manifest = json.loads((ROOT/'source_manifest.json').read_text(encoding='utf-8'))
    checks=[]
    for entry in manifest['files']:
        data=(ROOT/'source'/entry['path']).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        checks.append(dict(path=entry['path'], git_blob_sha1=blob,
                           sha256=hashlib.sha256(data).hexdigest(),
                           matches_pinned=blob==entry['git_blob_sha1']))
    assert all(e['matches_pinned'] for e in checks), [e for e in checks if not e['matches_pinned']]
    return checks


result = dict(source_verification=verify_sources(),
              junction_units=[junction(100,1,1), junction(1000,4,0.15)],
              identifiability=identifiable())
out=Path(__file__).with_name('probe_units_identifiability.json')
out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='source_verification'},indent=2))
print('PINNED_SOURCE_BLOBS_MATCH',len(result['source_verification']))
