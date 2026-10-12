"""ps45 다섯 침대의 AM 고체 부피분율 — Codex 판정문 §5-1 (64.7077–64.9201 %) 의 독립 재계산 (읽기 전용 · 새 계산 없음).

    python3 -I ps45_solid_fraction_check.py <리포 루트> <out.json>

Codex 탐침 (composition_basis.py) 과 갈라 둔 것:
  ① 덱은 정규식 하나씩이 아니라 템플릿 줄 (`particletemplate/sphere … atom_type T density constant ρ radius constant ${r_*}`) 을
     통째로 읽어 type ↔ ρ ↔ 반경 변수를 한 줄에서 묶는다 · 질량 가중 = `particledistribution/discrete` 의 (템플릿 이름, 가중) 쌍.
  ② SE 는 덱 상수 반경 × 개수가 아니라 **SE scaffold** (`kit_*__se_scaffold.csv.gz` — 입자마다 반경 · Codex 묶음에는 없던 파일) 의
     행을 직접 더한다 · AM 은 AM scaffold 의 행.
  ③ 개수는 망 표 (`network_cases.tsv` 의 `dump_type_counts`) 와 대조만 한다 (계산에는 scaffold 행).
"""
import csv
import gzip
import json
import math
import os
import re
import sys

BEDS = (('ps_0_10_r45', '0:10'), ('ps_3_7_r45', '3:7'), ('ps_5_5_r45', '5:5'), ('ps_7_3_r45', '7:3'), ('ps_10_0_r45', '10:0'))
RE_VAR = re.compile(r'^variable\s+(r_\w+)\s+equal\s+([0-9.eE+-]+)', re.M)
RE_TPL = re.compile(r'^fix\s+(\w+)\s+all\s+particletemplate/sphere\s+\d+\s+atom_type\s+(\d+)\s+density\s+constant\s+([0-9.eE+-]+)'
                    r'\s+radius\s+constant\s+\$\{(r_\w+)\}', re.M)
RE_PDD = re.compile(r'^fix\s+pdd_mix\s+all\s+particledistribution/discrete\s+\d+\s+(\d+)\s+(.*)$', re.M)


def vol_sum(path):
    tot = {}
    n = {}
    radii = {}
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        head = f.readline()
        case = re.search(r'case\s+(\S+)', head)
        for row in csv.reader(f):
            if not row or row[0].startswith('#'):
                continue
            t, r = int(row[0]), float(row[4]) * 1000.0      # µm
            tot[t] = tot.get(t, 0.0) + 4.0 / 3.0 * math.pi * r ** 3
            n[t] = n.get(t, 0) + 1
            radii.setdefault(t, set()).add(round(r, 9))
    return tot, n, {k: sorted(v) for k, v in radii.items()}, (case.group(1) if case else None)


def main():
    root, out = sys.argv[1:3]
    tsv = {r['bed'] if 'bed' in r else r['P_S']: r for r in csv.DictReader(
        open(os.path.join(root, 'docs/data/ps45_r45_network_g2_20261007/network_cases.tsv'), encoding='utf-8'), delimiter='\t')}
    by_ps = {r['P_S']: r for r in tsv.values()}
    rows = []
    for bed, ps in BEDS:
        deck = open(os.path.join(root, f'dem_scripts/ps_sweep_6mah_20260914/in.{bed}.liggghts'), encoding='utf-8').read()
        rv = {k: float(v) for k, v in RE_VAR.findall(deck)}
        tpl = {name: dict(type=int(t), rho=float(rho), r_um=rv[rvar] * 1000.0) for name, t, rho, rvar in RE_TPL.findall(deck)}
        m = RE_PDD.search(deck)
        toks = m.group(2).split()
        w = {toks[i]: float(toks[i + 1]) for i in range(0, len(toks), 2)}
        assert len(w) == int(m.group(1)), (bed, w)
        w_am = sum(v for k, v in w.items() if tpl[k]['type'] in (1, 2))
        w_se = sum(v for k, v in w.items() if tpl[k]['type'] == 3)
        rho = {tpl[k]['type']: tpl[k]['rho'] for k in tpl}
        assert rho[1] == rho[2], (bed, rho)
        nominal = (w_am / rho[1]) / (w_am / rho[1] + w_se / rho[3])
        nominal_alt = (w_am / 4850.0) / (w_am / 4850.0 + w_se / 1640.0)
        kit = os.path.join(root, f'docs/data/ps45_dh_transfer_20260926/kits/kit_{bed}')
        am, n_am, r_am, case_am = vol_sum(kit + '__am_scaffold.csv.gz')
        se, n_se, r_se, case_se = vol_sum(kit + '__se_scaffold.csv.gz')
        v_am, v_se = sum(am.values()), sum(se.values())
        x = v_am / (v_am + v_se)
        t = by_ps[ps]
        dump = {int(k): int(v) for k, v in (p.split(':') for p in t['dump_type_counts'].split(','))}
        rows.append(dict(
            bed=bed, P_S=ps, case_id=t['case_id'], scaffold_case_ids=[case_am, case_se],
            deck_densities_kg_m3=rho, deck_radii_um={tpl[k]['type']: tpl[k]['r_um'] for k in tpl}, deck_mass_weights=w,
            deck_w_AM=w_am, deck_w_SE=w_se,
            nominal_AM_solid_vol_frac_deck_densities=nominal, nominal_AM_solid_vol_frac_4850_1640=nominal_alt,
            scaffold_counts={'AM': n_am, 'SE': n_se}, scaffold_radii_um={'AM': r_am, 'SE': r_se},
            dump_type_counts=dump,
            counts_match_dump=all(n_am.get(k, 0) == dump.get(k, 0) for k in (1, 2)) and n_se.get(3, 0) == dump.get(3, 0),
            AM_solid_vol_frac_from_scaffolds=x,
            AM_mass_frac_back_at_deck_densities=v_am * rho[1] / (v_am * rho[1] + v_se * rho[3]),
            AM_mass_frac_back_at_4850_1640=v_am * 4850 / (v_am * 4850 + v_se * 1640)))
    xs = [r['AM_solid_vol_frac_from_scaffolds'] for r in rows]
    res = dict(scope='읽기 전용 · 덱 + scaffold (AM · SE 입자 행) · 새 계산 없음', rows=rows,
               min=min(xs), max=max(xs), all_counts_match_dump=all(r['counts_match_dump'] for r in rows))
    json.dump(res, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for r in rows:
        print(f"{r['P_S']:>5} {r['case_id']} 덱 명목 {100 * r['nominal_AM_solid_vol_frac_deck_densities']:.4f} % "
              f"(4.85/1.64 이면 {100 * r['nominal_AM_solid_vol_frac_4850_1640']:.4f} %) · scaffold 구 체적 {100 * r['AM_solid_vol_frac_from_scaffolds']:.4f} % · "
              f"개수 = 덤프 {r['counts_match_dump']} · 질량 되짚기 {100 * r['AM_mass_frac_back_at_deck_densities']:.3f} wt% "
              f"(4.85/1.64 {100 * r['AM_mass_frac_back_at_4850_1640']:.3f})")
    print(f"범위 {100 * res['min']:.4f} – {100 * res['max']:.4f} % · 개수 대조 {res['all_counts_match_dump']}")


if __name__ == '__main__':
    main()
