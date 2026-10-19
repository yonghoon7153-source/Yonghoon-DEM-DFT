"""Path-only adapter for the unchanged independent 2026-10-15 display probe.

The original probe derives its source/evidence root from __file__. Here its
bytes are compiled unchanged while __file__ points into this review. There is
no source-function replacement or production-code patch.
"""
import hashlib
import base64
import json
from pathlib import Path

review = Path(__file__).resolve().parents[1]
original = review / 'probes/display_original.py.b64'
# Exact bytes are stored in Base64 so the self-contained review package also
# preserves the original CRLF newlines and recorded SHA256.
body = base64.b64decode(original.read_text(encoding='ascii'))
assert hashlib.sha256(body).hexdigest() == 'a8815414b3ebf282ad05a987048df9c88255ab03fd541be632b8c4b019020db2'
(review / 'evidence/display_adapter.json').write_text(json.dumps({
    'original': str(original), 'sha256': hashlib.sha256(body).hexdigest(),
    'runtime_file': str(Path(__file__).resolve()),
    'change': '__file__ only: root source/evidence relocation; bytes compiled unchanged',
}, indent=2), encoding='utf-8')
exec(compile(body, str(original), 'exec'), {
    '__name__': '__main__', '__file__': str(Path(__file__).resolve()),
})
