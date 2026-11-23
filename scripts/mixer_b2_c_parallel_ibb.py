"""Run the one-shot B2-C overlap authorized on 2026-11-23."""
from pathlib import Path
import runpy


if __name__ == "__main__":
    controller = runpy.run_path(str(Path(__file__).with_name("mixer_b2_c_ibb.py")))
    raise SystemExit(controller["main"](parallel=True))
