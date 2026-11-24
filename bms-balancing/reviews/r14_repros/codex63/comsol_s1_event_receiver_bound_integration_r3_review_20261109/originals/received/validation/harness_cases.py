"""Exactly F01-F10 then L01-L02; first unexpected result ends the one session."""
import json
import sys
import time
from fractions import Fraction
import runtime_support as rt

def require(ok, reason):
    if not ok:
        raise AssertionError(reason)

def raw_new(path, raw):
    with path.open("xb") as f:
        require(f.write(raw) == len(raw), "FIXTURE_SHORT_WRITE")

def mailbox(arena):
    (arena / "mailbox").mkdir(exist_ok=False)
    for n in ("requests", "acks", "consumption"):
        (arena / "mailbox" / n).mkdir(exist_ok=False)

class FakeOwned:
    receiver_pid = 4242
    def __init__(self, alive=True):
        self.alive = alive
        self.poll_calls = 0
    def is_alive(self):
        self.poll_calls += 1
        return self.alive

class Suite:
    def __init__(self, context, started):
        self.ctx = context
        self.m = context["modules"]
        self.started = started
        self.plan = json.loads((rt.TASK / "VALIDATION_PLAN.json").read_text(encoding="utf-8"))
        self.fixtures = {row["id"]: json.loads((rt.TASK / row["fixture"]).read_text(encoding="utf-8"))
                         for row in self.plan["cases"]}
        self.bundle = json.loads((rt.TASK / "fixtures" / "ADMISSION.json").read_text(encoding="utf-8"))
        self.rows = []
        self.owned = None
        self.live = None
        self.counts = {}
        self.entries = []
        self.clock_rows = []
        self.case_evidence = {}
        self.current_id = None
        self.first_error = None

    def budget(self):
        require(time.monotonic() - self.started < 180, "PARENT_SESSION_LIMIT")

    def profile(self, frame, event, arg):
        if event == "call":
            key = frame.f_globals.get("__name__", "") + "." + frame.f_code.co_qualname
            if key in self.counts:
                self.counts[key] += 1
                self.entries.append({"function": key, "file": frame.f_code.co_filename,
                                     "line": frame.f_code.co_firstlineno})

    def expect_error(self, reason, function, *args):
        try:
            function(*args)
        except Exception as error:
            observed = getattr(error, "reason", None)
            require(observed == reason, "WRONG_EXCEPTION:" + repr(observed))
            self.case_evidence.setdefault("expected_errors", []).append(
                {"reason": observed, "type": type(error).__name__, "text": str(error)})
            return error
        raise AssertionError("EXPECTED_EXCEPTION_NOT_RAISED:" + reason)

    def request(self, session):
        p = self.bundle["roles"][0]
        producer = {k: p[k] for k in ("role", "instance_ref", "generation_ref", "process_evidence_ref")}
        return {"kind": "RECEIVER_REQUEST_V1", "session_ref": session, "case_ref": "R01",
                "handoff_ref": session + ":handoff:0001", "request_index": 1,
                "ticket": {"owner_ref": "fixture:owner", "epoch_ref": "fixture:epoch",
                           "run_ref": "fixture:R3", "producer": producer, "version": 0},
                "channel": "normal_delivery", "receiver_ref": "receiver:integration",
                "record_relpath": "R01/normal_delivery/v000000000000.json",
                "record_sha256": "a" * 64, "previous_digest": None}

    def fake_response(self, arena, request_raw, pid=4242, bad_path=False, bad_sha=False,
                      bad_marker=False, oversized=False):
        p = self.m["receiver_protocol"]
        q = json.loads(request_raw.decode("utf-8"))
        common = {k: q[k] for k in ("session_ref", "case_ref", "handoff_ref", "request_index",
                                   "record_sha256", "ticket", "channel", "receiver_ref")}
        common.update(request_sha256=p.digest(request_raw), receiver_pid=pid,
                      status="ACCEPTED", reason=None)
        consumption = dict(common, kind="RECEIVER_CONSUMPTION_V1",
                           record_relpath=q["record_relpath"], fixture_only=True)
        clean = p.canonical_bytes(consumption)
        actual = clean + b" " if bad_sha else clean
        ack = dict(common, kind="RECEIVER_ACK_V1",
                   consumption_ref="../outside.json" if bad_path else "mailbox/consumption/c0001.json",
                   consumption_sha256=p.digest(clean))
        ack_raw = b"x" * 16385 if oversized else p.canonical_bytes(ack)
        raw_new(arena / "mailbox" / "consumption" / "c0001.json", actual)
        raw_new(arena / "mailbox" / "acks" / "a0001.json", ack_raw)
        raw_new(arena / "mailbox" / "acks" / "a0001.ready", b"x" if bad_marker else b"")
        return ack_raw, actual

    def composition(self, arena, owned, ports, session_ref):
        e, o = self.m["event_clock_core"], self.m["state_owner"]
        a = self.m["evidence_admission"].EvidenceAdmission().admit(self.bundle)
        require(a.fixture_only and not a.operational, "ADMISSION_SCOPE_CHANGED")
        core = e.OwnedClockCore(a.expected, e.FailureLatch(a.supplied.producer, a.expected.clock.run_ref))
        owner_ref, epoch = "fixture:owner:" + self.current_id, "fixture:epoch:" + self.current_id
        receiver = "receiver:integration"
        initial = o.Snapshot(o.Ticket(owner_ref, epoch, core.latch.run_ref, core.latch.producer, 0), core, None)
        local = self.m["file_ports"].FilePorts(arena, "R01", initial, receiver)
        holder = {}
        def supplied(stage):
            bound = holder["bound"]
            value = 100 if self.current_id == "L02" and stage == "C5" else 90
            self.clock_rows.append({"stage": stage, "count": value, "request_index": bound.request_count})
            base = a.supplied
            return e.SuppliedCount("fixture:" + self.current_id + ":" + stage, base.clock,
                base.producer, value, "QPC_COUNT", stage, "fixture:stage:" + stage,
                "fixture:integration-only", True, True)
        bound = self.m["bound_ack_session"].BoundAckSession(
            a, Fraction(100, 1), session_ref, owned.receiver_pid, supplied,
            ports.marker, ports.reader, ports.consumption)
        holder["bound"] = bound
        facade = self.m["live_file_transport"].BoundLiveSession(bound, owned)
        bridge = self.m["receiver_bridge"].ReceiverBridge(local, facade, "R01", receiver)
        owner = o.StateOwner(owner_ref, epoch, core, receiver, local, bridge)
        bridge.bind_owner(owner)
        bound.bind_owner(owner)
        return {"admission": a, "local": local, "bound": bound, "bridge": bridge,
                "owner": owner, "ports": ports, "boundary": bound.boundary}

    def save_composition(self, c, result):
        self.case_evidence.update(transition=rt.plain(result),
            owner_view=rt.plain(c["owner"].view),
            bridge_head=rt.plain(c["bridge"].receiver_accepted_head),
            adapter_failure=rt.plain(c["bound"].first_failure),
            adapter_trace=rt.plain(c["bound"].trace),
            request_buffers=rt.plain(c["bound"].requests),
            port_calls=dict(c["ports"].calls), port_trace=list(c["ports"].trace))

    def offline(self, case_id):
        m = self.m
        p = m["receiver_protocol"]
        arena = rt.ARENA / case_id
        arena.mkdir(exist_ok=False)
        if case_id in ("F01", "F02", "F03", "F04", "F05", "F06", "F07"):
            mailbox(arena)
            session = "fixture:" + case_id
            raw = p.canonical_bytes(self.request(session))
            ports = m["live_file_transport"].FileAckPorts(
                arena, session, 4242, lambda: True, clock=lambda: 0,
                sleeper=lambda _: (_ for _ in ()).throw(AssertionError("UNEXPECTED_FIXTURE_SLEEP")))
            if case_id in ("F01", "F02", "F03", "F04", "F05"):
                ack_raw, consumption = self.fake_response(arena, raw, bad_path=case_id == "F05",
                    bad_marker=case_id == "F03", oversized=case_id == "F04")
                io_before = len(rt.IO_EVENTS)
                if case_id == "F03":
                    self.expect_error("ACK_MARKER_INVALID", ports.marker, raw)
                    require(not ports._acks, "DESCRIPTOR_CREATED_FOR_BAD_MARKER")
                    reads = [x for x in rt.IO_EVENTS[io_before:] if not x["writing"] and
                             x["path"] == rt.norm(arena / "mailbox/acks/a0001.json")]
                    require(len(reads) == 0, "BAD_MARKER_OPENED_PAYLOAD")
                elif case_id == "F04":
                    self.expect_error("ACK_FRAME_TOO_LARGE", ports.marker, raw)
                    require(not ports._acks, "DESCRIPTOR_CREATED_FOR_OVERSIZED_ACK")
                    reads = [x for x in rt.IO_EVENTS[io_before:] if not x["writing"] and
                             x["path"] == rt.norm(arena / "mailbox/acks/a0001.json")]
                    require(len(reads) == 1, "ACK_BOUNDED_READ_COUNT")
                else:
                    descriptor = ports.marker(raw)
                    require(descriptor == {"bytes": len(ack_raw), "sha256": p.digest(ack_raw)}, "DESCRIPTOR_MISMATCH")
                    if case_id == "F02":
                        before = dict(ports.calls)
                        self.expect_error("REQUEST_ALREADY_POSTED", ports.marker, raw)
                        require(before == ports.calls, "DUPLICATE_REQUEST_DID_IO")
                    else:
                        returned = ports.reader(raw, descriptor)
                        require(returned is ports._acks[1][1] and returned == ack_raw, "ACK_ORIGINAL_CACHE_NOT_RETURNED")
                        if case_id == "F05":
                            before = len(rt.IO_EVENTS)
                            self.expect_error("CONSUMPTION_PATH_MISMATCH", ports.consumption, returned)
                            require(len(rt.IO_EVENTS) == before, "INVALID_CONSUMPTION_PATH_DID_IO")
                        else:
                            got = ports.consumption(returned)
                            require(got is ports._consumptions[1] and got == consumption, "CONSUMPTION_RAW_CHANGED")
                            require(dict(ports.posted) == {1: raw}, "POSTED_BYTES_CHANGED")
                self.case_evidence["ack_fixture"] = rt.plain(ack_raw)
            elif case_id == "F06":
                response = {}
                def respond(_):
                    require(not response, "FIXTURE_RESPONSE_REPEATED")
                    request_raw = (arena / "mailbox/requests/q0001.json").read_bytes()
                    a, c = self.fake_response(arena, request_raw, bad_sha=True)
                    response.update(ack=a, consumption=c)
                ports.sleeper = respond
                c = self.composition(arena, FakeOwned(), ports, session)
                result = c["owner"].bootstrap("fixture:F06:bootstrap")
                fail = c["bound"].first_failure
                require(not result.normal_complete and result.reason == "DELIVERY_EXCEPTION", "F06_OWNER_RESULT")
                require(fail.reason == "CONSUMPTION_SHA_MISMATCH" and fail.stage == "CONSUMPTION_VALIDATE", "F06_WRONG_REJECTION_PATH")
                require(ports.first_failure is None, "SHA_VALIDATION_MOVED_TO_NEW_PORT")
                require(ports._consumptions[1] == response["consumption"], "F06_CONSUMPTION_CHANGED")
                self.save_composition(c, result)
            else:
                times = iter((0, 5))
                ports.clock = lambda: next(times)
                self.expect_error("ACK_TRANSPORT_TIMEOUT", ports.marker, raw)
                first, detail, before, trace = ports.first_failure, ports.first_failure_detail, dict(ports.calls), list(ports.trace)
                self.fake_response(arena, raw)
                self.expect_error("ACK_TRANSPORT_TIMEOUT", ports.marker, raw)
                self.expect_error("ACK_TRANSPORT_TIMEOUT", ports.reader, raw, {})
                require(ports.first_failure == first and ports.first_failure_detail is detail
                        and ports.calls == before and ports.trace == trace, "LATE_ACK_RESET_OR_IO")
            require(ports.calls == self.fixtures[case_id]["expected_transport_io"], "TRANSPORT_CALL_COUNTS")
            self.case_evidence.update(port_calls=dict(ports.calls), port_trace=list(ports.trace),
                                      first_failure=ports.first_failure, posted=rt.plain(dict(ports.posted)))
        elif case_id == "F08":
            class NeverBound:
                def exchange(self, *args):
                    raise AssertionError("BOUND_REACHED_AFTER_DEAD_PROCESS")
            owned = FakeOwned(False)
            facade = m["live_file_transport"].BoundLiveSession(NeverBound(), owned)
            before = len(rt.IO_EVENTS)
            self.expect_error("RECEIVER_NOT_ALIVE", facade.exchange)
            require(owned.poll_calls == 1 and len(rt.IO_EVENTS) == before, "LIVENESS_BEFORE_BOUND_NOT_ENFORCED")
        elif case_id == "F09":
            f = m["receiver_finish"]
            expected = f.make_finish_expected("fixture:finish", "a"*64, 4242, "b"*64)
            original = p.canonical_bytes(expected)
            wrong = dict(expected, session_ref="fixture:wrong")
            self.expect_error("FINISH_SESSION_MISMATCH", f.validate_finish, p.canonical_bytes(wrong), expected)
            require(p.canonical_bytes(expected) == original, "FINISH_EXPECTED_CHANGED")
            self.case_evidence["normal_finish_granted"] = False
        elif case_id == "F10":
            f = m["receiver_finish"]
            expected = f.make_finish_expected("fixture:finish", "a"*64, 4242, "b"*64)
            timer = {"clock": 0, "sleep": 0}
            def clock():
                timer["clock"] += 1
                return 120
            def sleep(_):
                timer["sleep"] += 1
            before = len(rt.IO_EVENTS)
            self.expect_error("RECEIVER_LIFETIME_EXCEEDED", f.wait_finish, arena, expected, 0, clock, sleep)
            require(timer == {"clock": 1, "sleep": 0} and len(rt.IO_EVENTS) == before, "LIFETIME_NOT_CHECKED_BEFORE_IO")
            self.case_evidence["fake_timer_calls"] = timer
        else:
            raise AssertionError("UNKNOWN_OFFLINE_CASE")
        return self.fixtures[case_id]["expected_reason"]

    def live_case(self, case_id):
        m, p = self.m, self.m["receiver_protocol"]
        if case_id == "L01":
            self.owned = m["receiver_session"].FileReceiverSession(
                rt.ARENA, self.ctx["session_ref"], self.ctx["source_manifest_sha256"],
                self.ctx["child_entry"], self.ctx["engine"])
            ready = self.owned.start()
            ports = m["live_file_transport"].FileAckPorts(
                rt.ARENA, self.ctx["session_ref"], self.owned.receiver_pid, self.owned.is_alive)
            self.live = self.composition(rt.ARENA, self.owned, ports, self.ctx["session_ref"])
            c = self.live
            result = c["owner"].bootstrap("fixture:L01:bootstrap")
            require(result.normal_complete and result.reason is None, "L01_NOT_NORMAL")
            require(c["owner"].view.last_verified_delivered_ticket.version == 0
                    and c["bridge"].receiver_accepted_head.version == 0, "L01_DELIVERED_HEAD")
            require(c["bound"].first_failure is None and c["bound"].request_count == 1, "L01_ADAPTER")
            self.case_evidence["ready"] = ready
            self.save_composition(c, result)
            return "NORMAL_DELIVERY_COMPLETED"
        c = self.live
        require(c is not None and self.owned.is_alive(), "LIVE_INSTANCE_NOT_RETAINED")
        result = c["owner"].assess_count(c["owner"].view.snapshot.ticket, c["admission"].supplied, "fixture:L02:assess")
        fail = c["bound"].first_failure
        require(not result.normal_complete and result.reason == "DELIVERY_EXCEPTION", "L02_OWNER_RESULT")
        require(fail is not None and fail.reason == "DEADLINE_NOT_BEFORE" and fail.stage == "C5", "L02_WRONG_BOUNDARY_REJECTION")
        require(c["bound"].boundary is c["boundary"] and c["bound"].request_count == 2, "BOUNDARY_OR_SESSION_RESET")
        require(c["owner"].view.last_verified_delivered_ticket.version == 0
                and c["bridge"].receiver_accepted_head.version == 0, "L02_DELIVERED_HEAD_ADVANCED")
        require(c["local"]._heads["normal_delivery"].snapshot.ticket.version == 1, "L02_LOCAL_HEAD")
        require(c["ports"].calls["request_writes"] == 2 and c["ports"].calls["request_markers"] == 2
                and c["ports"].calls["ack_reads"] == 2 and c["ports"].calls["reader_calls"] == 2
                and c["ports"].calls["consumption_reads"] == 2, "LIVE_TRANSPORT_COUNTS")
        consumed = json.loads(c["ports"]._consumptions[2].decode("utf-8"))
        require(consumed["ticket"]["version"] == 1 and consumed["status"] == "ACCEPTED", "CHILD_V1_NOT_CONSUMED")
        f = m["receiver_finish"]
        expected = f.make_finish_expected(self.ctx["session_ref"], self.ctx["source_manifest_sha256"],
                                         self.owned.receiver_pid, p.digest(c["bound"].requests[-1]))
        f.publish_finish(rt.ARENA, expected)
        rc = self.owned._proc.wait(timeout=5)
        require(rc == 0, "RECEIVER_EXIT_NONZERO")
        cleanup = self.owned.stop_owned()
        require(cleanup["terminate_calls"] == 0 and cleanup["returncode"] == 0 and cleanup["exited"], "NATURAL_EXIT_CLEANUP")
        lifecycle = json.loads((rt.ARENA / "mailbox/LIFECYCLE.json").read_text(encoding="utf-8"))
        require(lifecycle["status"] == "COMPLETED" and lifecycle["reason"] is None
                and lifecycle["requests_consumed"] == 2 and lifecycle["acks_published"] == 2
                and lifecycle["receiver_pid"] == self.owned.receiver_pid, "LIFECYCLE_MISMATCH")
        child_guard = json.loads((rt.ARENA / "CHILD_GUARD.json").read_text(encoding="utf-8"))
        require(child_guard["guard_events"] == [] and child_guard["target_counts"] == self.plan["child_expected_profile"]
                and child_guard["rc"] == 0, "CHILD_GUARD_OR_PROFILE")
        self.save_composition(c, result)
        self.case_evidence.update(finish=expected, child_consumed_v1=consumed, child_rc=rc,
                                 lifecycle=lifecycle, child_guard=child_guard, cleanup=cleanup,
                                 natural_finish_completed=True,
                                 legacy_cleanup_graceful_field_not_reinterpreted=True)
        return "EXPECTED_C5_REFUSAL_AND_ORDERLY_CHILD_EXIT"

    def run(self):
        require(sorted(x.name for x in rt.RESULTS.iterdir()) == ["session.stderr.txt", "session.stdout.txt"],
                "RESULTS_NOT_LAUNCHER_ONLY")
        require(list(rt.ARENA.iterdir()) == [], "ARENA_NOT_EMPTY")
        for index, row in enumerate(self.plan["cases"]):
            self.current_id = row["id"]
            self.case_evidence, self.clock_rows, self.entries = {}, [], []
            self.counts = {key: 0 for key in self.plan["target_profile_keys"]}
            begin = time.monotonic()
            try:
                self.budget()
                sys.setprofile(self.profile)
                try:
                    reason = self.offline(row["id"]) if row["id"].startswith("F") else self.live_case(row["id"])
                finally:
                    sys.setprofile(None)
                self.budget()
                require(reason == row["expected_reason"], "CASE_REASON_MISMATCH")
                require(self.counts == self.fixtures[row["id"]]["expected_target_counts"], "ACTUAL_FUNCTION_CALL_COUNT_MISMATCH")
                require([x["stage"] for x in self.clock_rows] == self.fixtures[row["id"]]["expected_clock_stages"], "CHECKPOINT_REACH_MISMATCH")
                require(not rt.GUARD_EVENTS, "SCOPE_GUARD_FAILURE")
                record = {"id": row["id"], "status": "PASS", "observed_reason": reason, "expected": self.fixtures[row["id"]],
                          "target_counts": dict(self.counts), "actual_entries": list(self.entries), "clock_calls": list(self.clock_rows),
                          "evidence": self.case_evidence, "elapsed_seconds": time.monotonic() - begin}
                rt.write_new(rt.RESULTS / (row["id"] + ".json"), record)
                self.rows.append({"id": row["id"], "status": "PASS", "reason": reason})
                print(json.dumps(self.rows[-1], ensure_ascii=False), flush=True)
            except BaseException as error:
                sys.setprofile(None)
                self.first_error = {"id": row["id"], "type": type(error).__name__, "text": str(error),
                                    "traceback": rt.traceback.format_exc(), "target_counts": dict(self.counts),
                                    "actual_entries": list(self.entries), "clock_calls": list(self.clock_rows),
                                    "partial_evidence": self.case_evidence, "guard_events": list(rt.GUARD_EVENTS)}
                rt.write_new(rt.RESULTS / "FIRST_ERROR.json", rt.plain(self.first_error))
                self.rows.append({"id": row["id"], "status": "FAIL", "reason": str(error)})
                self.rows += [{"id": rest["id"], "status": "NOT_RUN", "reason": "FIRST_UNEXPECTED_FAILURE"}
                              for rest in self.plan["cases"][index+1:]]
                break
        cleanup = None
        if self.first_error is not None and self.owned is not None:
            cleanup = self.owned.stop_owned()
            rt.write_new(rt.RESULTS / "OWNED_FAILURE_CLEANUP.json", cleanup)
        counts = {status: sum(r["status"] == status for r in self.rows) for status in ("PASS", "FAIL", "NOT_RUN")}
        result = {"kind": "R3_ONE_SESSION_RESULT", "counts": counts, "cases": self.rows,
                  "parent_elapsed_seconds": time.monotonic() - self.started,
                  "child_spawn_count": rt._POPEN_COUNT, "guard_events": list(rt.GUARD_EVENTS),
                  "failure_cleanup": cleanup, "normal_live_completions": sum(r["id"] == "L01" and r["status"] == "PASS" for r in self.rows),
                  "native_ready": False, "contract_adopted": False, "overall": "INCOMPLETE"}
        rt.write_new(rt.RESULTS / "RESULTS.json", result)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        return 0 if counts == {"PASS": 12, "FAIL": 0, "NOT_RUN": 0} else 1

