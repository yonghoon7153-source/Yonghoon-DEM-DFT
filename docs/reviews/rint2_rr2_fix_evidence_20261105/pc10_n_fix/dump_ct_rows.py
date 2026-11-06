"""PC10-08 · 09 · 10 (N1 · N2 · N4) + 같은 부류 — 시험 CT01–CT04 의 행 전체를 JSON 으로 (고치기 전 · 뒤 대조 · 판정 아님 · 시험이 판정한다).
python3 -I dump_ct_rows.py <scripts 폴더 (rint_r_chain.py · test_rint_r_chain.py)> <출력 json>"""
import contextlib
import hashlib
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

SD = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(SD))
import test_rint_r_chain as T  # noqa: E402
import rint_r_chain as RR  # noqa: E402

T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pc10_dump_')
out = {'module_sha256': hashlib.sha256(Path(RR.__file__).read_bytes()).hexdigest(),
       'test_sha256': hashlib.sha256(Path(T.__file__).read_bytes()).hexdigest()}
try:
    with contextlib.redirect_stdout(io.StringIO()):
        T.fixtures()
    rows, k = {}, 0
    for code in T.CT_PRODUCER:
        for nm, rec in T.CT_RECS:
            for lk, log in T.CT_LOGS:
                k += 1
                f, s = T.ct_summary(f'D1_{k}', code, rec, log)
                fl = RR.result_fields(f, s)
                rows[f'{code}/{nm}/{lk}'] = [fl['cause'], fl['resume_ok']]
    f, s = T.ct_summary('D1_prestart', 'TIME_LIMIT', None, None)
    fl = RR.result_fields(f, s)
    rows['TIME_LIMIT/prestart_nolog'] = [fl['cause'], fl['resume_ok']]
    out['CT01'] = rows
    rows, logs = {}, dict(T.CT_LOGS)
    for nm, end, lk, _w in T.CT02_ROWS:
        f = T.pc_folder(f'D2_{nm}', {T.PC_MARK: '{}\n'})
        T.pc_group(f, T.LG_RUN, end, logs[lk])
        c, ok = RR.orphan_cause(f)
        rows[nm] = [c, ok, RR.result_fields(f, None)['resume_ok']]
    out['CT02'] = rows
    out['CT03'] = {nm: T.ct03_row(f'D3_{nm}', body) for nm, body, _o in T.CT03_BODIES}
    ct04 = {}
    for nm, end, code, rec, _c, _ok in T.CT04_ROWS:
        r = T.rc_recover_resume(f'D4_{nm}', dict({'by': 'chain', 'confirmed': True}, **end), T.RC02_LOG, prep=T.ct04_prep(code, rec))
        ct04[nm] = {kk: v for kk, v in r.items() if kk != 'tail'}
    ct04['N4'] = T.ct04_n4('D4_N4')
    out['CT04'] = ct04
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
Path(sys.argv[2]).write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True, default=repr) + '\n', encoding='utf-8')
print(json.dumps({kk: (len(v) if isinstance(v, dict) else v) for kk, v in out.items()}, ensure_ascii=False))
