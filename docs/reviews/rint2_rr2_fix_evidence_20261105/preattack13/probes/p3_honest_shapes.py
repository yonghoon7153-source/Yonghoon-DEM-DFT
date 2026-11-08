"""P3 탐침 — 정직한 생산자 출력 (실제 CLI · 가짜 러너 · 실제 read_run) 의 모든 런 기록을 `arms_read_kind` 로 분류: 사다리 (P0) · 예측 (모서리 ·
origin 팔 고르기 [1,2] · origin8) · 12 단위 + 합치기 (MergeFetch) · 넘침 캠페인 (origin8 8 팔 · 넘침 점 · 끝 합치기).  rc 0 · group_cause None 런인데
verified 아님 = 거짓 거부 (재실행 자격 앞 런 판정이 멈춘다)."""
import json, sys
from collections import Counter
from common import RR, T, setup_fixtures

def classify(label, summ, out):
    runs = (summ or {}).get('runs') or []
    for r in runs:
        if not isinstance(r, dict):
            out['bad'].append((label, 'non-dict', repr(r)[:80])); continue
        k, why = RR.arms_read_kind(r.get('arms_read'), r)
        shape = RR.run_record_shape(r)
        al = r.get('arm_list')
        form = (r.get('arms'), tuple(al) if isinstance(al, list) else al)
        out['forms'][f'{form}|{shape}|{k}'] += 1
        if shape == 'exit_ok' and k != 'verified' and r.get('arms_read'):
            out['bad'].append((label, r.get('name'), shape, k, why, form, r.get('outdir')))

def main():
    setup_fixtures()
    out = {'forms': Counter(), 'bad': [], 'labels': []}
    which = sys.argv[1:] or ['main', 'pred', 'units', 'over']
    if 'main' in which:
        for law in ('P0', 'P1'):
            r = T.s_main(law); classify(f'ladder_{law}', r.get('sum'), out); out['labels'].append(f'ladder_{law}:{(r.get("sum") or {}).get("status")}')
    if 'pred' in which:
        r = T.s_main_predict(); classify('predict', r.get('sum'), out); out['labels'].append(f'predict:{(r.get("sum") or {}).get("status")}')
    if 'units' in which:
        r = T.s_units_main()
        for nm, atts in r['units'].items():
            for j, a in enumerate(atts):
                if a: classify(f'unit:{nm}:{j}', a.get('sum'), out)
        classify('merge', (r.get('m') or {}).get('sum'), out); out['labels'].append(f'merge:{((r.get("m") or {}).get("sum") or {}).get("status")}')
        classify('one', (r.get('one') or {}).get('sum'), out)
    if 'over' in which:
        r = T.s_units_over()
        for k, v in r.items():
            if isinstance(v, dict) and 'sum' in v:
                classify(f'over:{k}', v.get('sum'), out); out['labels'].append(f'over:{k}:{(v.get("sum") or {}).get("status")}')
            elif isinstance(v, dict):
                for kk, vv in v.items():
                    for a in (vv if isinstance(vv, list) else [vv]):
                        if isinstance(a, dict) and 'sum' in a:
                            classify(f'over:{k}:{kk}', a.get('sum'), out)
    print(json.dumps({'labels': out['labels'], 'forms': dict(out['forms']), 'n_bad': len(out['bad']), 'bad': out['bad'][:20]},
                     ensure_ascii=False, indent=1, default=str))

if __name__ == '__main__':
    main()
