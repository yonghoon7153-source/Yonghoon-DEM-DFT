#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S0 단계 1 끝-끝 대조 (2026-11-06 · `SELF-155` 고침 · Codex 회차 ② §8 Q8 확인 칸).

같은 픽스처 킷 (scripts/test_ca_s0_census.py 의 write_kit · payload 실물로 생산 raster 입력을 잡는다) 을 S0 단계 1 로 두 번 돈다 —
① 고치기 전 판 = ca_s0_census.py (커밋 39104710a) + 그 모듈의 cj = carbon_junction.py (커밋 3b12fbe2d) · ② 지금 작업 트리 판 (둘 다 새 판).
같은 출력 경로에서 차례로 돌린 뒤 옮긴다 (payload 인자에 경로가 들어간다).  출력 폴더의 파일 목록 · 보고 JSON (모든 칸) · npz (모든 배열 ·
dtype · 모양 · 바이트) · 계획 · 로그 바이트를 비교한다.

다르게 나와야 맞는 칸 (코드 출처 · 시간 — 진실한 새 값인지 본다):
  · 계획 cjunc_plan.json 의 source.tool_sha256 = 그 런을 낸 ca_s0_census.py 의 sha256 (옛 = 39104710a blob · 새 = 지금 파일) → 계획 바이트 ·
    cjunc_plan.sha256 · 보고의 plan.sha256 이 따라 바뀐다 (S0 도구가 바뀌었으므로 계획 해시는 새 값이 맞다)
  · 보고 elapsed_s (잰 시간)
  · ⚠ 보고 code.* (file_digests · tool_sha256) 는 두 런 다 디스크 파일을 해시한다 (이 하네스는 한 프로세스에서 모듈만 바꿔 끼운다) → 두 런 같은
    새 값 (하네스 산물 · 실제 옛 런의 출처 칸이 아님) — 새 판 값이 지금 파일의 sha256 인지만 본다.

  python3 docs/reviews/rint2_s0_mem_fix_20261106/tools/s0_e2e_compare.py [--out FILE.json]

σ · 전류 칸은 S0 가 내지 않는다 (스키마 검사가 막는다) · 킷 폴더는 쓰지 않는다 (S0-3 이 확인) · 결과 폴더는 임시 (끝나면 지운다).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, SCRIPTS)
import numpy as np                     # noqa: E402
import test_ca_s0_census as TS         # noqa: E402  (픽스처만 — 시험 main 은 부르지 않는다)

S0 = TS.S0
REF_CJ, REF_S0 = '3b12fbe2d', '39104710a'
EXPECT_DIFF_REPORT = ('elapsed_s', 'plan.sha256')                     # 보고에서 다르게 나와야 맞는 칸
EXPECT_DIFF_PLAN = ('source.tool_sha256',)                            # 계획에서 다르게 나와야 맞는 칸
EXPECT_DIFF_BYTES = ('cjunc_plan.sha256',)                            # 바이트가 달라야 맞는 파일 (계획 해시)


def load(rel, commit, name):
    src = subprocess.run(['git', '-C', ROOT, 'show', f'{commit}:{rel}'], capture_output=True, check=True).stdout
    d = tempfile.mkdtemp(prefix=f'{name}_')
    p = os.path.join(d, f'{name}.py')
    with open(p, 'wb') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    while d in sys.path:
        sys.path.remove(d)
    return m, hashlib.sha256(src).hexdigest()


def walk_json(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        if list(a) != list(b):
            out.append((path, 'keys', list(a)[:6], list(b)[:6]))
            return
        for k in a:
            walk_json(a[k], b[k], f'{path}.{k}' if path else k, out)
        return
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, 'len', len(a), len(b)))
            return
        for x, (u, v) in enumerate(zip(a, b)):
            walk_json(u, v, f'{path}[{x}]', out)
        return
    if type(a) is not type(b) or a != b:
        if not (isinstance(a, float) and isinstance(b, float) and a != a and b != b):
            out.append((path, 'value', a, b))


def compare_dirs(da, db):
    fa, fb = sorted(os.listdir(da)), sorted(os.listdir(db))
    res = {'files_a': fa, 'files_b': fb, 'files_same': fa == fb, 'json': {}, 'npz': {}, 'bytes': {}}
    for nm in sorted(set(fa) & set(fb)):
        pa, pb = os.path.join(da, nm), os.path.join(db, nm)
        if nm.endswith('.json'):
            with open(pa, encoding='utf-8') as f:
                ja = json.load(f)
            with open(pb, encoding='utf-8') as f:
                jb = json.load(f)
            diffs = []
            walk_json(ja, jb, '', diffs)
            res['json'][nm] = [{'path': p, 'kind': k, 'old': str(x)[:100], 'new': str(y)[:100]} for p, k, x, y in diffs]
        elif nm.endswith('.npz'):
            za, zb = np.load(pa, allow_pickle=False), np.load(pb, allow_pickle=False)
            bad = []
            if sorted(za.files) != sorted(zb.files):
                bad.append(f'키 {sorted(za.files)} ≠ {sorted(zb.files)}')
            for k in sorted(set(za.files) & set(zb.files)):
                x, y = za[k], zb[k]
                if x.dtype.str != y.dtype.str or x.shape != y.shape or np.ascontiguousarray(x).tobytes() != np.ascontiguousarray(y).tobytes():
                    bad.append(k)
            res['npz'][nm] = {'n_arrays': len(za.files), 'different': bad}
        else:
            with open(pa, 'rb') as f:
                ba = f.read()
            with open(pb, 'rb') as f:
                bb = f.read()
            res['bytes'][nm] = {'same': ba == bb, 'len_old': len(ba), 'len_new': len(bb)}
    return res


def kits(tmp):
    out = []
    out.append(('kit_A', TS.write_kit(tmp, 'kit_A', vgcf=[TS.F1], ptfe=[TS.P1], vol={'VGCF': 0.04, 'PTFE': 0.1}), TS.VOX))
    out.append(('kit_J', TS.write_kit(tmp, 'kit_J', vgcf=TS._kit_j_fibres(), ptfe=[TS.J_PTFE], vol={'VGCF': 0.05, 'PTFE': 0.1}), TS.J_H))
    vg, pt = TS._kit_rv()
    out.append(('kit_RV', TS.write_kit(tmp, 'kit_RV', vgcf=vg, ptfe=pt, vol={'VGCF': 0.05, 'PTFE': 0.1}), TS.J_H))
    #  kit_L — 긴 두 점 섬유 (11.3 µm · 선분 하나 → 옛 반지름을 키우고 새 판에서는 조각으로 나뉜다) 가 F1 (x 2.05–5.95 · y 4.55 · z 2.05)
    #  위 0.06 µm 를 지난다 (접합 instance) + kit_J 섬유 셋
    LONG = np.array([[1.0, 1.0, 2.0], [9.0, 9.0, 2.25]])
    out.append(('kit_L', TS.write_kit(tmp, 'kit_L', vgcf=[TS.F1, LONG] + TS._kit_j_fibres(), ptfe=[TS.J_PTFE],
                                      vol={'VGCF': 0.06, 'PTFE': 0.1}), TS.J_H))
    return out


def under(path, prefixes):
    return any(path == e or path.startswith(e + '.') or path.startswith(e + '[') for e in prefixes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    ref_cj, ref_cj_sha = load('scripts/carbon_junction.py', REF_CJ, 'carbon_junction_ref_e2e')
    ref_s0, ref_s0_sha = load('scripts/ca_s0_census.py', REF_S0, 'ca_s0_census_ref_e2e')
    ref_s0.cj = ref_cj                                          # 옛 S0 도구 + 옛 원장 (그 모듈의 cj)
    new_cj_sha = hashlib.sha256(open(os.path.join(SCRIPTS, 'carbon_junction.py'), 'rb').read()).hexdigest()
    new_s0_sha = hashlib.sha256(open(os.path.join(SCRIPTS, 'ca_s0_census.py'), 'rb').read()).hexdigest()
    tmp = tempfile.mkdtemp(prefix='s0e2e_')
    rows = []
    try:
        for nm, kit, vox in kits(tmp):
            outs = {}
            common = os.path.join(tmp, f'out_{nm}')
            for tag, mod in (('old', ref_s0), ('new', S0)):
                mod.run_stage(1, [kit], common, vox=vox, bridge_um=0.48, sdcp_sphere_d=0.30)
                o = os.path.join(tmp, f'out_{nm}_{tag}')
                os.rename(common, o)
                outs[tag] = o
            cmp_ = compare_dirs(outs['old'], outs['new'])
            rn = json.load(open(os.path.join(outs['new'], f's0_stage1_{nm}.json'), encoding='utf-8'))
            ro = json.load(open(os.path.join(outs['old'], f's0_stage1_{nm}.json'), encoding='utf-8'))
            pn = json.load(open(os.path.join(outs['new'], 'cjunc_plan.json'), encoding='utf-8'))
            po = json.load(open(os.path.join(outs['old'], 'cjunc_plan.json'), encoding='utf-8'))
            unexpected = {}
            for f, v in cmp_['json'].items():
                allow = EXPECT_DIFF_PLAN if f == 'cjunc_plan.json' else EXPECT_DIFF_REPORT
                unexpected[f] = [d for d in v if not under(d['path'], allow)]
            dig = {d['file']: d['sha256'] for d in rn['code']['file_digests']}
            row = {'kit': nm, 'vox': vox, 'files_same': cmp_['files_same'], 'files': cmp_['files_a'],
                   'json_unexpected_diffs': unexpected, 'json_all_diff_paths': {f: [d['path'] for d in v] for f, v in cmp_['json'].items()},
                   'npz': cmp_['npz'], 'other_files': cmp_['bytes'],
                   'plan_tool_sha256': {'old': po['source']['tool_sha256'], 'new': pn['source']['tool_sha256']},
                   'plan_sha256': {'old': ro['plan']['sha256'], 'new': rn['plan']['sha256']},
                   'reported_new_file_digests': {'carbon_junction.py': dig.get('carbon_junction.py'), 'ca_s0_census.py': dig.get('ca_s0_census.py')},
                   'blob_sha256': {'carbon_junction_old': ref_cj_sha, 'carbon_junction_new': new_cj_sha,
                                   'ca_s0_census_old': ref_s0_sha, 'ca_s0_census_new': new_s0_sha},
                   'n_instances': rn['junction_census']['n_instances'], 'n_segments': rn['junction_census']['census'].get('n_segments'),
                   'elapsed_s': {'old': ro.get('elapsed_s'), 'new': rn.get('elapsed_s')}}
            bytes_ok = all(v['same'] for k, v in cmp_['bytes'].items() if k not in EXPECT_DIFF_BYTES)
            row['science_identical'] = bool(row['files_same'] and not any(unexpected.values())
                                            and all(not v['different'] for v in cmp_['npz'].values()) and bytes_ok)
            row['provenance_true'] = bool(po['source']['tool_sha256'] == ref_s0_sha and pn['source']['tool_sha256'] == new_s0_sha
                                          and ref_s0_sha != new_s0_sha and ro['plan']['sha256'] != rn['plan']['sha256']
                                          and dig.get('carbon_junction.py') == new_cj_sha and dig.get('ca_s0_census.py') == new_s0_sha
                                          and new_cj_sha != ref_cj_sha)
            rows.append(row)
            print(f"{nm}: 선분 {row['n_segments']} · instance {row['n_instances']} · 파일 {len(row['files'])} 같음 {row['files_same']} · "
                  f"JSON 뜻밖의 차이 {sum(len(v) for v in unexpected.values())} · npz 다른 배열 "
                  f"{sum(len(v['different']) for v in cmp_['npz'].values())} / {sum(v['n_arrays'] for v in cmp_['npz'].values())} · "
                  f"바이트 다른 파일 {[k for k, v in cmp_['bytes'].items() if not v['same']]} · 과학 값 같음 {row['science_identical']} · "
                  f"출처 진실 {row['provenance_true']} · JSON 다른 칸 {row['json_all_diff_paths']}", flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            json.dump({'ref_commits': {'carbon_junction': REF_CJ, 'ca_s0_census': REF_S0}, 'rows': rows}, fh, ensure_ascii=False, indent=1)
    return 0 if all(r['science_identical'] and r['provenance_true'] for r in rows) else 1


if __name__ == '__main__':
    sys.exit(main())
