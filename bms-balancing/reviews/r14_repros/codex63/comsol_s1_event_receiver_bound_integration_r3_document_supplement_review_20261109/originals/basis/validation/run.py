import sys
import time
from pathlib import Path
STARTED = time.monotonic()
sys.path.insert(0, str(Path(__file__).resolve().parent))
import runtime_support as rt
import harness_cases
try:
    context = rt.initialize("parent")
    rc = harness_cases.Suite(context, STARTED).run()
except BaseException:
    rt.traceback.print_exc()
    rc = 1
raise SystemExit(rc)

