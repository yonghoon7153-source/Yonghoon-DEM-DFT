"""회신 DP 고침 변이 검사 — DP 판 (../li2s2_dp_mutation_2026_11_04/dp_mutate.py) 의 287 개를 가져오되 DP 고침으로 자리가 바뀐 4 개는
새 자리로 옮기고, DP 고침 자리 (DQ1–) 와 회신 DP P2-2 로 '같은 결과' 설명에서 뺀 직접 진입 엄격 판독 넷 (DQ14–DQ17) 을 더한다.
실행 · 판정은 DL 판과 같다 (저장소 밖 복사본 · 작업자 · which = run / drv / both · 주석 중간 자리는 '  #' 를 붙인다 — DP 판 _keep_comment).
옵션: --dry · --only=접두 (쉼표로 여럿) · --tag=이름 · --failfast · --workers=N.
뺀 것 (같은 결과 — 시험이 못 가르는 것이 맞다 · 회신 DP 표를 따라 범위를 좁혀 적는다):
  · persist_observed 의 즉시 저장 끄기 — **같은 프로세스 안에서는** 끝 처리가 같은 장부를 저장한다. 급작스러운 종료 (kill -9 · 정전) 에서는 다르다 —
    그 경우는 이 시험 틀 (한 프로세스) 로 재현하지 않는다 (즉시 저장은 그 경우를 위한 운영 근거 · 회신 DP Q6).
  · 시드 루프의 판정 상태 엄격 판독 끄기 — 조건부: 바로 앞 ①-4 가 그 판정을 원자료로 **다시 썼을 때만** 같은 열쇠 둘이 남을 수 없다.
    다시 못 쓰면 (written False) ①-4 가 멈춘다 (DQ7 이 그 멈춤을 깬다) — 그래서 루프에 닿는 판정은 늘 새로 쓴 것이다.
  · 확인 경로의 '적기 실패 → 거부' return 끄기 — 그 실행이 과학적이라 선언 문제 목록이 늘 비어 있지 않아 바로 아래가 같은 코드로 거부한다 (회신 DP 동의).
  · 확인 구간 (확인 기록 저장 · STOP 지우기 · 확인 끝 표시) 끄기 — 그 사이 신호로 끊겨도 확인 기록은 저장되고 STOP 이 남아 다음 확인이 같은 기록을
    다시 쓰지 않는다 (같은 결과 · 구간은 기록 정리용).
  (처음엔 _ledger_check 의 꼴 검사 끄기도 '뒤 원소 검사가 같은 장부를 invalid 로' 라고 뺐는데 틀렸다 — 빈 객체 stop_history ({}) 는 뒤 원소 검사가
   못 본다. 시험 (요약 · stop_history 빈 객체) 을 더하고 DQ18 (소비자) · DQ19 (러너) 로 깬다.)"""
import importlib.util, pathlib, sys

REPO = pathlib.Path("/home/user/Yonghoon-DEM-DFT")
_spec = importlib.util.spec_from_file_location("dp_mutate", REPO / "db/raw/li2s2_dp_mutation_2026_11_04/dp_mutate.py")
dp = importlib.util.module_from_spec(_spec)
_argv = sys.argv; sys.argv = [sys.argv[0]]
_spec.loader.exec_module(dp)
sys.argv = _argv
dl = dp.dl
RUNR, DRVR = dl.RUNR, dl.DRVR

MOVED = {
 "R4_launch_ledger": ("R4_launch_ledger", RUNR, [
     ("                led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n                save_ledger()",
      "                led[\"runs\"].append(ent); state[\"entry\"], state[\"t0\"] = ent, t0\n                pass"),
     ("                    save_ledger()                            # ⭐ 띄운 직후", "                    pass                                     # ⭐ 띄운 직후")], "run"),
 "DP51_persist_revert_off": ("DP51_persist_revert_off", RUNR, [
     ("                        r_.clear(); r_.update(old_)          # 교체 전 실패", "                        pass  # 교체 전 실패")], "run"),
 "DP57_ledger_keys_optional": ("DP57_ledger_keys_optional", DRVR, [
     ("            out.append(f\"장부에 {k} 가 없다\")", "            led[k] = []")], "both"),
 "DP58_ledger_elems_off": ("DP58_ledger_elems_off", DRVR, [
     ("        elif not all(isinstance(x, dict) for x in led[k]):\n            out.append(f\"장부 {k} 원소가 객체가 아니다\")",
      "        elif False:\n            out.append(f\"장부 {k} 원소가 객체가 아니다\")")], "both"),
}
F = lambda name, anchor, repl, which="drv", where=DRVR: (name, where, [(anchor, repl)], which)
NC = '__import__("contextlib").nullcontext()'
NEW = [
 # ── P0-1 · P2-1: 저장 경계의 신호
 F("DQ1_persist_section_off", "                with _critical():                            # ⭐ 회신 DP P0-1 — 메모리 변경",
   f"                with {NC}:                            # ⭐ 회신 DP P0-1 — 메모리 변경", "run", RUNR),
 F("DQ2_after_replace_revert", "                    except _AfterReplace:\n                        raise                                # 디스크에 새 행이 있다",
   "                    except ZeroDivisionError:\n                        raise                                # 디스크에 새 행이 있다", "run", RUNR),
 F("DQ3_stop_section_off", "        with _critical():                                    # ⭐ 회신 DP P2-1",
   f"        with {NC}:                                    # ⭐ 회신 DP P2-1", "run", RUNR),
 F("DQ4_stop_after_replace_flag_off", "            except _AfterReplace:\n                state[\"stopped\"] = True                      # 디스크에 이 STOP 이 있다",
   "            except ZeroDivisionError:\n                state[\"stopped\"] = True                      # 디스크에 이 STOP 이 있다", "run", RUNR),
 F("DQ5_after_replace_plain", "                raise _AfterReplace(f\"교체 뒤 디렉터리 fsync 실패 ({type(e_).__name__}: {e_})\") from e_",
   "                raise", "run", RUNR),
 F("DQ6_attempt_section_off", "            with _critical():                                # ⭐ 회신 DP — 폴더 · 실행 전 기록 · 장부 행을",
   f"            with {NC}:                                # ⭐ 회신 DP — 폴더 · 실행 전 기록 · 장부 행을", "run", RUNR),
 # ── P1-1: written False · 현재 폴더 미해결 기록
 F("DQ7_rejudge_written_off", "                if now_.get(\"written\") is False:             # ⭐ 회신 DP P1-1", "                if False:", "run", RUNR),
 F("DQ8_end_written_off", "            if v.get(\"written\") is False:                    # ⭐ 회신 DP P1-1", "            if False:", "run", RUNR),
 F("DQ9_summary_unresolved_off", "            if rprob_:\n                ver[(s, sd)] = {\"status\": \"invalid\"", "            if False:\n                ver[(s, sd)] = {\"status\": \"invalid\"", "both"),
 F("DQ10_summary_none_status_off",
   "            if rprob_ is None and any(isinstance(r_, dict) and r_.get(\"status\") is None for _, r_, part_ in recs_ if not part_):",
   "            if False:", "both"),
 # ── P1-2: 요약의 장부 검사
 F("DQ11_record_tmp_off", "    invalid.extend(record_tmp_problems(out_root))", "    pass", "both"),
 F("DQ12_same_run_conflict_off", "            if st_l in (\"pass\", \"fail\") and st_f in (\"pass\", \"fail\") and st_l != st_f:", "            if False:", "both"),
 F("DQ13_same_run_melt_off", "            elif mf_ and st_f == \"pass\":", "            elif False:", "both"),
 # ── P2-2: 직접 진입 엄격 판독 (DP 판에서 '같은 결과' 로 뺐던 넷)
 F("DQ14_card_strict_off", "    d = loads_strict(pathlib.Path(card).read_text(encoding=\"utf-8\"))   # ⭐ 회신 DO P1 — 카드도",
   "    d = json.loads(pathlib.Path(card).read_text(encoding=\"utf-8\"))   # ⭐ 회신 DO P1 — 카드도"),
 F("DQ15_band_strict_off", "    d = loads_strict(q.read_text(encoding=\"utf-8\"))          # ⭐ 회신 DO P1 — G4 밴드 카드도",
   "    d = json.loads(q.read_text(encoding=\"utf-8\"))          # ⭐ 회신 DO P1 — G4 밴드 카드도"),
 F("DQ16_gate_plan_strict_off", "    plan = loads_strict((run / \"plan.json\").read_text(encoding=\"utf-8\"))   # ⭐ 회신 DO P1 (예외 → 판정이",
   "    plan = json.loads((run / \"plan.json\").read_text(encoding=\"utf-8\"))   # ⭐ 회신 DO P1 (예외 → 판정이"),
 F("DQ18_consumer_ledger_shape_off", "        if shp_:\n            raise ValueError(\" · \".join(shp_))\n        runs, stop_hist = led[\"runs\"], led[\"stop_history\"]",
   "        if False:\n            raise ValueError(\" · \".join(shp_))\n        runs, stop_hist = led[\"runs\"], led[\"stop_history\"]", "both"),
 F("DQ19_runner_ledger_shape_off", "                if shp_:\n                    raise ValueError(\"장부 꼴이 아니다 — \" + \" · \".join(shp_))",
   "                if False:\n                    raise ValueError(\"장부 꼴이 아니다 — \" + \" · \".join(shp_))", "run", RUNR),
 F("DQ17_seed_gate_plan_strict_off", "    plan = loads_strict((run / \"plan.json\").read_text(encoding=\"utf-8\")) if (run / \"plan.json\").exists() else {}",
   "    plan = json.loads((run / \"plan.json\").read_text(encoding=\"utf-8\")) if (run / \"plan.json\").exists() else {}"),
]

_dp_names = {m[0] for m in dp.MUT}
assert set(MOVED) <= _dp_names, f"옮길 변이가 DP 판에 없다: {sorted(set(MOVED) - _dp_names)}"   # 이름이 틀리면 옮김이 조용히 빠진다
MUT = [MOVED.get(m[0], m) for m in dp.MUT] + NEW
MUT = [(m[0], m[1], dp._keep_comment(m[2]), m[3]) for m in MUT]   # 옮긴 것까지 (이미 '#' 가 있으면 그대로)
dl.MUT = MUT
TAG = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--tag=")), "dq")
dp.TAG = TAG
FAILFAST = "--failfast" in sys.argv
dp.FAILFAST = FAILFAST
WORKERS = int(next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--workers=")), dl.N_WORKERS))

if __name__ == "__main__":
    bad = dl.check_anchors()
    if bad:
        print("\n".join(bad)); sys.exit(2)
    names = [mu[0] for mu in MUT]
    assert len(names) == len(set(names)), "변이 이름이 겹친다"
    import builtins
    nbad = []
    for name, rel, reps, which in MUT:                       # 문법이 깨지는 변이가 없는지 먼저 (DP 판 무효 20 의 교훈)
        f = REPO / rel; s = f.read_text(encoding="utf-8")
        for o_, n_ in reps:
            s = s.replace(o_, n_, 1)
        try:
            compile(s, str(f), "exec")
        except SyntaxError as e:
            nbad.append(f"{name}: {e.msg}")
    if nbad:
        print("문법 오류 변이:\n" + "\n".join(nbad)); sys.exit(2)
    print(f"변이 {len(MUT)} 개 (DP 판 {len(dp.MUT)} · 자리 옮김 {len(MOVED)} · DQ {len(NEW)}) · 자리 모두 한 번씩 · 모두 컴파일됨", flush=True)
    if "--dry" in sys.argv:
        sys.exit(0)
    only = [a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")]
    todo = [mu for mu in MUT if not only or any(mu[0].startswith(p) for p in only[0].split(","))]
    mirrors = [dp.make_mirror(i) for i in range(WORKERS)]
    print(f"작업자 {WORKERS} · 러너 첫 빨강 멈춤 {'켬' if FAILFAST else '끔'} · 복사본 mut_{TAG}_w*", flush=True)
    import queue, threading
    q = queue.Queue()
    for mu in todo:
        q.put(mu)
    lock, results = threading.Lock(), []

    def worker(m):
        while True:
            try:
                mu = q.get_nowait()
            except queue.Empty:
                return
            line = dl.run_one((mu, m))
            with lock:
                results.append(line)
                print(line, flush=True)

    ts = [threading.Thread(target=worker, args=(m,)) for m in mirrors]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    n_red = sum("⭕ 빨강" in x for x in results)
    print(f"끝: 빨강 {n_red} / {len(todo)}")
