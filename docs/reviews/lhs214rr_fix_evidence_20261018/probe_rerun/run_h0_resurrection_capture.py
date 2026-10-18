"""파생 래퍼 — Codex probes/consumer_h0_resurrection.py 를 바이트 그대로 compile · exec 하고, 예외가 나면 그때까지의 report 를 저장한다 (탐침 무변경 · 수정 뒤 코드에서 탐침이
옛 동작 (load_tau_results 통과) 을 전제한 자리에서 멈추므로 · 정지 · 다시 읽기 판정값을 남기려는 것뿐)."""
import json, sys, traceback, hashlib
from pathlib import Path
probe = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
src = probe.read_bytes()
sys.path.insert(0, str(probe.parent))
ns = {'__file__': str(probe), '__name__': '__main__'}
err = None
try:
    exec(compile(src, str(probe), 'exec'), ns)
except BaseException as e:
    err = ''.join(traceback.format_exception(type(e), e, e.__traceback__))[-3000:]
rep = ns.get('report', {})
out.write_text(json.dumps({'probe_sha256': hashlib.sha256(src).hexdigest(), 'exception': err, 'report': rep}, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
print(json.dumps({'exception_tail': (err or '')[-400:], 'keys': sorted(rep)}, ensure_ascii=False))
