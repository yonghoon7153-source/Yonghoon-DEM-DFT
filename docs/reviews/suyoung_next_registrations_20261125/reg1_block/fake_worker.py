"""Test-only stand-in for `driver.py RUN` inside block test packages (never shipped in a block).

    fake_worker.py RUN --arm NAME --out FOLDER --cpu N --root ROOT

It refuses like the driver when the CPU affinity is not {N} or a thread variable is not 1
(rc 2), appends the arm name to $HOME/fake_worker_calls.log, and writes a synthetic arm with
synth_runs.write_arm (invented numbers, no MPM step).  Per-arm deviations come from
fake_scenario.json next to this file: {"ARM": {"status": "INCOMPLETE"}, ...}.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "BLIS_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("RUN",))
    parser.add_argument("--arm", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cpu", type=int, required=True)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    if os.sched_getaffinity(0) != {args.cpu} or any(os.environ.get(k) != "1" for k in THREADS):
        print("AFFINITY_OR_THREADS_NOT_SET")
        return 2
    with (Path(os.environ["HOME"]) / "fake_worker_calls.log").open("a", encoding="ascii") as log:
        log.write(args.arm + "\n")
    spec_loader = importlib.util.spec_from_file_location("fake_worker_synth", HERE / "synth_runs.py")
    synth = importlib.util.module_from_spec(spec_loader)
    spec_loader.loader.exec_module(synth)
    scenario = json.loads((HERE / "fake_scenario.json").read_text("ascii"))
    spec = synth.Spec(**scenario.get(args.arm, {}))
    return synth.write_arm(args.root, args.arm, args.out, args.cpu, spec, live_environment=True)


if __name__ == "__main__":
    sys.exit(main())
