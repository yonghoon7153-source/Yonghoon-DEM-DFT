"""시험 함수 몇 개를 직접 불러 (화면 600 자 자름 없이) 통과 여부 · 행 수 · 어긋난 행 수 · 어긋난 행 이름을 JSON 으로 — 고치기 전 · 뒤 (사본 둘) 의 같은 시험 판.
python3 -I count_bad.py <scripts 폴더> <검사 이름 쉼표> <출력 json>"""
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
T.TD = tempfile.mkdtemp(prefix='pc10_count_')
want = sys.argv[2].split(',')
out = {'module_sha256': hashlib.sha256(Path(RR.__file__).read_bytes()).hexdigest(),
       'test_sha256': hashlib.sha256(Path(T.__file__).read_bytes()).hexdigest(), 'checks': {}}
try:
    with contextlib.redirect_stdout(io.StringIO()):
        T.fixtures()
    for cid, _title, fn in T.CHECKS:
        if cid not in want:
            continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                ok, why = fn()
        except Exception as e:                                # noqa: BLE001
            ok, why = False, f'{type(e).__name__}: {e}'
        bad = why.get('bad') if isinstance(why, dict) else None
        out['checks'][cid] = {'pass': bool(ok), 'n': why.get('n') if isinstance(why, dict) else None,
                              'n_bad': (why.get('n_bad') if isinstance(why, dict) and 'n_bad' in why else
                                        (why.get('bad_n') if isinstance(why, dict) and 'bad_n' in why else (len(bad) if isinstance(bad, dict) else None))),
                              'bad_keys': sorted(bad)[:200] if isinstance(bad, dict) else None,
                              'detail': None if isinstance(why, dict) else str(why)[:400]}
finally:
    shutil.rmtree(T.TD, ignore_errors=True)
Path(sys.argv[3]).write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True, default=repr) + '\n', encoding='utf-8')
print(json.dumps({k: [v['pass'], v['n'], v['n_bad']] for k, v in out['checks'].items()}, ensure_ascii=False))
