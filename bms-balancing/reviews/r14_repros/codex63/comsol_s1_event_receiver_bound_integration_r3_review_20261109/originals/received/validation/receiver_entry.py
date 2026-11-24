import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import runtime_support as rt
counts = {"receiver_worker_candidate.run_receiver": 0, "receiver_worker_candidate._consume_record": 0,
          "receiver_finish.wait_finish": 0, "receiver_finish.validate_finish": 0}
entries = []
def profile(frame, event, arg):
    if event == "call":
        key = frame.f_globals.get("__name__", "") + "." + frame.f_code.co_qualname
        if key in counts:
            counts[key] += 1
            entries.append({"function": key, "file": frame.f_code.co_filename, "line": frame.f_code.co_firstlineno})
try:
    context = rt.initialize("child")
    sys.setprofile(profile)
    try:
        rc = context["modules"]["receiver_worker_candidate"].run_receiver(rt.ARENA, context["session_ref"],
             {"hold_case_ref": "R16", "source_manifest_sha256": context["source_manifest_sha256"]})
    finally:
        sys.setprofile(None)
    rt.write_new(rt.ARENA / "CHILD_GUARD.json", {"kind": "OWNED_RECEIVER_GUARD_RESULT",
                 "target_counts": counts, "actual_entries": entries, "guard_events": rt.GUARD_EVENTS,
                 "rc": rc, "process_creation_count": rt._POPEN_COUNT})
except BaseException:
    sys.setprofile(None)
    rt.traceback.print_exc()
    rc = 1
raise SystemExit(rc)

