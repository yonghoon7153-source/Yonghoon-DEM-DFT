"""P5b (사전 공격 13 고침 확인 · 탐침 p5 의 사슬 술어 판) — 정직 요약 (사다리 P0 · P1 · 예측 · 'units' 인자 = 12 단위 · 합치기 · 넘침) 의 판독 완료 런 기록 전부에
사슬의 값 꼴 함수 `arm_public_value_problem` (고친 뒤 · read_run 과 한 함수) → 거부 0 이어야 · arms_read_kind = verified 그대로 (고치기 전 판 = 함수 없음 → N/A)."""
import json
import sys

from common import RR, T, setup_fixtures


def main():
    setup_fixtures()
    fn = getattr(RR, 'arm_public_value_problem', None)
    sums = [(f'lad_{law}', T.s_main(law).get('sum')) for law in ('P0', 'P1')]
    sums.append(('pred', T.s_main_predict().get('sum')))
    if 'units' in sys.argv[1:]:
        r = T.s_units_main()
        for nm, atts in r['units'].items():
            for a in atts:
                if a:
                    sums.append((f'unit:{nm}', a.get('sum')))
        sums.append(('merge', (r.get('m') or {}).get('sum')))
        r2 = T.s_units_over()
        for k in ('m2', 'one'):
            sums.append((f'over:{k}', (r2.get(k) or {}).get('sum')))
    runs = arms = 0
    bad, kinds = [], {}
    for lab, s in sums:
        for r in (s or {}).get('runs') or []:
            if RR.run_record_shape(r) != 'exit_ok' or not r.get('arms_read'):
                continue
            runs += 1
            k = RR.arms_read_kind(r.get('arms_read'), r)[0]
            kinds[k] = kinds.get(k, 0) + 1
            for a in r['arms_read']:
                arms += 1
                why = fn(a) if callable(fn) else 'N/A (함수 없음)'
                if why:
                    bad.append((lab, r.get('name'), why))
    print(json.dumps({'fn': callable(fn), 'n_runs': runs, 'n_arm_records': arms, 'kinds': kinds, 'n_rejected': len(bad), 'bad': bad[:10]},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
