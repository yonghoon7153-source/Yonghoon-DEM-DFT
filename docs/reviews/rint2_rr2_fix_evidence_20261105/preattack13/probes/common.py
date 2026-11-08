"""공용 — 시험 모듈 (test_rint_r_chain) 을 라이브러리로 불러 RR · TD 를 채운다 (main 은 부르지 않는다)."""
import sys, tempfile, os
SCRIPTS = os.environ.get('PA13_SCRIPTS', '/home/user/pa13/scripts')
sys.path.insert(0, SCRIPTS)
import rint_r_chain as RR          # noqa: E402
import test_rint_r_chain as T      # noqa: E402
T.RR = RR
T.TD = tempfile.mkdtemp(prefix='pa13_probe_')

def setup_fixtures():
    T.fixtures()
