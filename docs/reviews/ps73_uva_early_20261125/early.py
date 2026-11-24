"""Release a single UVa NP6 job into the existing parallel journal, using UC's slot."""
import fcntl
import os
from pathlib import Path
import re
import socket
import sys

GO = "GO_PS73_UVA_EARLY_ONCE"
MANIFEST = "fb53fb1c1eaee6ef289d7353ac7a3fc211c20322dbed872fb2e601563e470858"
UC_SHA = "4e38d5f19569f5c5e5e59f354bcf295bddaa87f7fec5e16ebc551bed6a4cee89"
SOURCE_SHA = "c3105bb5a48dfab9150e4421d47c540eb66a68e761cd474f366573f4f6a9fbda"
INTENT_SHA = "fd569f6cdb44068abb45b6dec3980dd6bef9b41e457864974d0b235d4747d9a4"

def validate_sources(site, folder):
    p = site.p
    e = site.e
    p.need(socket.gethostname().split(".")[0] == "ibb-master", "wrong login host")
    p.need(not any(k.startswith(("SLURM_", "SBATCH_", "SALLOC_", "SRUN_")) for k in os.environ), "login shell required")
    p.need(folder.parent == site.OPS and folder.resolve() == folder, "wrong dispatch location")
    for name, checksum in [("intent.json", INTENT_SHA), ("source.json", SOURCE_SHA), ("results/UC.json", UC_SHA)]:
        p.need(p.digest(site.OPS / name) == checksum, "unexpected receipt " + name)
    p.need(p.digest(site.HERE/"SOURCE_SHA256SUMS") == MANIFEST, "original worker identity")
    uc = p.read(site.result("UC"))
    receipt = uc["receipt"]
    acct = site.acct("373359")
    p.need(receipt["job"] == "373359" and receipt["arm"] == "UC" and receipt["technical_ok"] is True
           and receipt["control_ok"] is True and receipt["runner_rc"] == 0
           and acct["state"] == "COMPLETED" and acct["exit_code"] == "0:0", "UC control or terminal receipt")
    p.need(p.read(site.OPS/"attempts"/"UT"/"000001"/"ack.json")["job"] == "373358", "UT identity")
    e.reserved()
    kit = e.original.pinned_kit(e.ROOT)
    e.reader(kit)
    _, _, _, source = e.inputs(kit, "UVa")
    p.need(source == receipt["identity"] == p.read(site.OPS/"source.json"), "restored S0 differs")

def launch(site, folder):
    p = site.p
    validate_sources(site, folder)
    hold = site.OPS / "results" / "UVa.hold.json"
    owned = folder / "scheduling-only.json"
    journal = site.OPS / "attempts" / "UVa"
    first = journal / "000001"
    staged = folder / "segment"
    claim = folder / "dispatch-claim.json"
    ack = folder / "dispatch-ack.json"
    if not owned.exists():
        p.publish(owned, {"arm":"UVa", "reason":"UC slot early dispatch in progress", "mode":GO})

    def owns_hold():
        return hold.is_file() and hold.samefile(owned)

    def release_hold():
        if owns_hold():
            hold.unlink()

    if hold.exists():
        p.need(owns_hold(), "existing UVa hold requires review")
    if site.attempts("UVa"):
        p.need((first/"ack.json").is_file(), "original submission ambiguous; inspect STATUS")
        existing = p.read(first/"ack.json")
        if claim.exists():
            p.need(ack.is_file() and existing == p.read(ack), "competing allocations; inspect STATUS")
        release_hold()
        print("ALREADY_ACKNOWLEDGED UVa", existing["job"], flush=True)
        return

    if claim.exists() and not ack.exists():
        raise ValueError("AMBIGUOUS early submission; inspect STATUS; no retry")
    if not owns_hold():
        os.link(owned, hold)
    try:
        if not claim.exists():
            # The incumbent's single writer only dispatches a first UVa after writing UB's result.
            # Checking this after the hold is visible closes the race with that writer.
            if site.result("UB").exists() or (site.OPS/"results"/"UB.hold.json").exists() or site.last("UB")[1]["state"] != "RUNNING":
                print("ORIGINAL_MONITOR_OWNS_UVa", flush=True)
                return
            p.need(not site.attempts("UVa") and not site.result("UVa").exists(), "original monitor already owns UVa")
            journal.mkdir(parents=True, exist_ok=True)
            staged.mkdir(exist_ok=True)
            projected = site.capacity(6)
            record = {"arm":"UVa", "previous":None, "resume":None, "projected_user_cpus":projected,
                      "authorization":GO, "control_job":"373359", "control_receipt_sha256":UC_SHA}
            p.publish(claim, record)
            argv = ["sbatch","--parsable","--no-requeue","--nodes=1","--ntasks=6","--cpus-per-task=1",
                    "--partition=cpu","--qos=cpu-60","--time=5-00:00:00","--job-name=ps73_UVa",
                    "--chdir="+str(folder),"--output="+str(folder/"slurm-%j.out"),"--error="+str(folder/"slurm-%j.err"),
                    str(folder/"worker.sh"),str(site.HERE),str(first),MANIFEST]
            response = site.command(argv).strip()
            p.need(re.fullmatch(r"[1-9]\d*(?:;[A-Za-z0-9_.-]+)?", response), "AMBIGUOUS sbatch response")
            p.publish(ack, dict(record, job=response.split(";")[0]))
        # Only publish a fully acknowledged segment. The original monitor can never see a partial ack.
        for name, src in [("claim.json", claim), ("ack.json", ack)]:
            dst = staged / name
            if dst.exists():
                p.need(dst.samefile(src), "stage identity changed")
            else:
                os.link(src, dst)
        p.need(not first.exists(), "claim collision")
        staged.rename(first)
        release_hold()
        record = p.read(ack)
        print("ACKNOWLEDGED UVa JOB_ID=%s NP6 PROJECTED=%d/60" % (record["job"], record["projected_user_cpus"]), flush=True)
    finally:
        if not claim.exists():
            release_hold()

def main():
    folder = Path(__file__).resolve().parent
    code = folder.parent / "code"
    sys.path.insert(0, str(code))
    import site_ops as site
    if sys.argv[1:] != [GO]:
        raise ValueError("expected early UVa GO")
    # A repeated operator invocation cannot enter launch while the first is submitting.
    with (folder/"dispatch.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        launch(site, folder)
    # The original monitor handles timeouts, NP6 restarts and final selection. If it exited
    # cleanly during the transfer, its existing RESUME uses the same exclusive monitor lock.
    if not (site.OPS/"final.json").exists() and not (site.OPS/"results"/"UB.hold.json").exists():
        site.main(["RESUME"])

if __name__ == "__main__":
    os.umask(0o077)
    try:
        main()
    except Exception as exc:
        print("EARLY_UVA_STOP", str(exc), file=sys.stderr, flush=True)
        raise SystemExit(2)
