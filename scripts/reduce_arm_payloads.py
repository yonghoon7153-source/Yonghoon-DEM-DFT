#!/usr/bin/env python3
"""팔 payload 를 **판정에 필요한 부분만** 남겨 축소한다 (R8 Q6 ⓐ 종료조건).

★ 왜: 생산 payload 는 LEAN=2(σ_e 전용)에서도 팔당 **127 MB** 다 — SE 표면 삼각형·strain
  점군·morphology 점군 같은 시각화 배열이 함께 들어간다.  16팔 디렉터리가 2.0 GB 이고
  W4+W4b 32팔이면 4 GB 라 **git 에 넣을 수 없다**.  그런데 R8 Q6 [P1] 의 종료조건은
  *"16팔 JSON·receipt 커밋"* 이고, 그것이 없으면 `table_s3_data_20260827.md` §9 의
  provenance 대조는 **한 기계에만 있는 파일에 대한 서술**이라 제3자가 재실행할 수 없다.

★★ 설계 원칙 — **축소본을 판정기가 그대로 읽는다.**
  출력 파일명을 `p2_*.json` 으로 유지하고 `{'step3': {...}}` 구조로 쓴다.  그러면
  `sdcp_gain_verdict.py --dir <축소본> --collect-only` 와 `--compare-dir` 이
  **원본과 똑같이** 동작한다 (`_read()` 가 `d['step3']` 를 먼저 본다).
  ⇒ 커밋된 것이 **설명**이 아니라 **실행 가능한 증거**가 된다.

무엇을 남기나:
  · `step3` 의 스칼라 전부 (σ_e·σ_ion·n_dof·cg_info·cg_resid·unconverged·…)
  · `step3.manifest` **통째로** (input_digest·code_sha·규약 필드 — §9 대조가 쓰는 것)
  · 짧은 리스트 (origin_shift_um 같은 3원소 벡터 등)
무엇을 버리나:
  · 길이 `--max-list` 초과의 리스트/중첩 배열 = 시각화 페이로드
  ⚠ 버린 것은 **조용히 사라지지 않는다** — `_reduced` 에 이름과 길이를 적는다.
    (이 리포가 반복해 배운 것: 없어진 것을 기록하지 않으면 나중에 그것이 없었는지
     버려진 것인지 구분할 수 없다.)

사용:
    python3 scripts/reduce_arm_payloads.py --dir ~/sdcp/prereg_v2_... --out docs/data/w4_...
    python3 scripts/reduce_arm_payloads.py --selftest
"""
import argparse
import glob
import json
import os
import sys

MAX_LIST = 64          # 이보다 긴 리스트 = 배열로 보고 버린다 (origin 3원소 등은 남는다)


def _prune(obj, path, dropped, max_list):
    """긴 배열을 버리고 버린 경로를 `dropped` 에 적는다.  스칼라·짧은 리스트는 그대로."""
    if isinstance(obj, dict):
        return {k: _prune(v, f'{path}.{k}', dropped, max_list) for k, v in obj.items()}
    if isinstance(obj, list):
        if len(obj) > max_list:
            dropped.append({'path': path, 'len': len(obj)})
            return None
        return [_prune(v, f'{path}[]', dropped, max_list) for v in obj]
    return obj


def reduce_one(path, max_list=MAX_LIST):
    """payload 하나 → 축소 dict.  step3 가 없으면 None."""
    with open(path, encoding='utf-8') as fh:
        d = json.load(fh)
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3')
    if s is None:
        return None
    dropped = []
    #  manifest 는 통째로 보존한다 — 길이 제한을 걸지 않는다 (규약 필드가 리스트일 수 있고
    #  §9 대조가 이 블록을 쓴다).  나머지 step3 만 가지친다.
    man = s.get('manifest')
    rest = {k: v for k, v in s.items() if k != 'manifest'}
    out = _prune(rest, 'step3', dropped, max_list)
    if man is not None:
        out['manifest'] = man
    out['_reduced'] = {
        'source': os.path.basename(path),
        'source_bytes': os.path.getsize(path),
        'dropped': dropped,                      # 버린 배열: 이름과 길이
        'tool': 'scripts/reduce_arm_payloads.py',
        'max_list': max_list,
    }
    return {'step3': out}


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='팔 payload 를 step3+manifest 만 남겨 축소한다 (판정기가 그대로 읽는다)')
    ap.add_argument('--dir', help='원본 팔 디렉터리 (p2_*.json 이 있는 곳)')
    ap.add_argument('--out', help='축소본을 쓸 디렉터리 (없으면 만든다)')
    ap.add_argument('--max-list', type=int, default=MAX_LIST,
                    help=f'이보다 긴 리스트는 버린다 (기본 {MAX_LIST})')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not a.dir or not a.out:
        ap.error('--dir 과 --out 이 필요하다 (또는 --selftest)')

    src = sorted(glob.glob(os.path.join(a.dir, 'p2_*.json')))
    if not src:
        raise SystemExit(f'{a.dir} 에 p2_*.json 이 없다')
    os.makedirs(a.out, exist_ok=True)
    tot_in = tot_out = 0
    for p in src:
        red = reduce_one(p, a.max_list)
        if red is None:
            print(f'  SKIP {os.path.basename(p)} — step3 없음')
            continue
        q = os.path.join(a.out, os.path.basename(p))
        with open(q, 'w', encoding='utf-8') as fh:
            json.dump(red, fh, ensure_ascii=False, sort_keys=True)
        bi, bo = os.path.getsize(p), os.path.getsize(q)
        tot_in += bi
        tot_out += bo
        print(f'  {os.path.basename(p):28s} {bi/1e6:8.1f} MB → {bo/1e3:7.1f} kB')
    print(f'\n  {len(src)} 팔: {tot_in/1e6:.0f} MB → {tot_out/1e3:.0f} kB '
          f'({tot_in/max(tot_out,1):.0f}배 축소)')
    print(f'  ★ 확인: python3 scripts/sdcp_gain_verdict.py --dir {a.out} --collect-only')
    return 0


def _selftest():
    import tempfile
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + label)
        ok = ok and bool(cond)

    payload = {
        'step3': {
            'sigma_e_eff_S_cm': 0.0812, 'n_dof': 26816923, 'cg_info': 0,
            'cg_resid': 1e-9, 'unconverged': False,
            'origin_shift_um': [0.0, 0.075, 0.0],            # 짧은 리스트 = 남는다
            'viz_points': list(range(200000)),               # 긴 배열 = 버린다
            'manifest': {'input_digest': 'd1022e090ab625a9', 'code_sha': 'c2f5b047',
                         'vox_um': 0.15, 'ptfe_stamp': 'centerline',
                         'sdcp_bridge_um': 0.01},
        },
        'huge_sibling': list(range(500000)),                 # step3 밖 = 애초에 안 읽는다
    }
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, 'p2_DBE_sph_a0.json')
        with open(src, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh)
        red = reduce_one(src)
        s = red['step3']

        chk('scalar 보존 (σ_e·dof·cg)',
            s['sigma_e_eff_S_cm'] == 0.0812 and s['n_dof'] == 26816923
            and s['cg_info'] == 0 and s['unconverged'] is False)
        chk('짧은 리스트 보존 (origin_shift_um)', s['origin_shift_um'] == [0.0, 0.075, 0.0])
        chk('manifest 통째 보존 (§9 대조가 쓰는 것)',
            s['manifest']['input_digest'] == 'd1022e090ab625a9'
            and s['manifest']['code_sha'] == 'c2f5b047'
            and s['manifest']['sdcp_bridge_um'] == 0.01)
        chk('긴 배열 제거', s['viz_points'] is None)
        #  ★ 이것이 요점 — 버린 것을 **기록**한다.  조용히 사라지면 나중에 "없었다" 와
        #    "버렸다" 를 구분할 수 없다.
        chk('버린 것을 기록한다 (이름 + 길이)',
            any(d['path'] == 'step3.viz_points' and d['len'] == 200000
                for d in s['_reduced']['dropped']))
        chk('축소된다 (원본 대비 1/100 미만)',
            len(json.dumps(red)) * 100 < os.path.getsize(src))

        #  ★★ 계약: 판정기가 축소본을 **원본과 똑같이** 읽어야 한다.
        out = os.path.join(td, 'red')
        os.makedirs(out)
        with open(os.path.join(out, 'p2_DBE_sph_a0.json'), 'w', encoding='utf-8') as fh:
            json.dump(red, fh)
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        try:
            import sdcp_gain_verdict as _v
            rows_o, _ = _v.collect(td)
            rows_r, _ = _v.collect(out)
            same = (rows_o and rows_r
                    and rows_o[0]['sigma_e'] == rows_r[0]['sigma_e']
                    and rows_o[0]['n_dof'] == rows_r[0]['n_dof']
                    and rows_o[0]['cg_info'] == rows_r[0]['cg_info']
                    and rows_o[0]['origin_shift_um'] == rows_r[0]['origin_shift_um']
                    and rows_o[0]['ptfe_stamp'] == rows_r[0]['ptfe_stamp'])
            chk('★ 판정기가 축소본을 원본과 동일하게 읽는다 (collect 대조)', bool(same))
        except Exception as exc:                                   # noqa: BLE001
            chk(f'판정기 대조 (import 실패: {exc})', False)

    print(('\n✓ reduce_arm_payloads selftest PASS' if ok
           else '\n✗ reduce_arm_payloads selftest FAIL'))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
