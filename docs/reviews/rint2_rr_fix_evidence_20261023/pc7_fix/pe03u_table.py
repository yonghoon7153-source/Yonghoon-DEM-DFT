"""PE03u 표를 지금 사슬로 셈 (고치기 전 · 뒤 대조 · 값 · σ 없음)."""
import sys
import tempfile
from pathlib import Path

WT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(WT / 'scripts'))
import rint_r_chain as RR  # noqa: E402
import test_rint_r_chain as TM  # noqa: E402

TM.RR = RR
TM.TD = tempfile.mkdtemp(prefix='pe03u_tab_', dir=sys.argv[2])
rows_bad, n = [], 0
for nm, (ce, by_log) in TM.PE03_ROWS.items():
    for lk, want_c in by_log.items():
        n += 1
        end = {'by': 'recover', 'cause': 'parent_dead', 'rc': None, 'confirmed': True}
        if ce is not None:
            end['chain_end'] = dict(ce, confirmed=False, ended_utc='2026-11-02T00:00:00Z')
        f = TM.pc_folder(f'T_{nm}_{lk}', {TM.PC_MARK: '{}\n'})
        TM.pc_group(f, 'L01_floor', end, '[p2] run\n' + (TM.PE03_LOGS[lk] + '\n' if TM.PE03_LOGS[lk] else ''))
        r = RR.attempt_result_line(1, f, None, 'recover')
        if r['cause'] != want_c:
            rows_bad.append((nm, lk, r['cause'], want_c))
print('rows', n, 'bad', len(rows_bad))
for x in rows_bad:
    print(' ', x)
