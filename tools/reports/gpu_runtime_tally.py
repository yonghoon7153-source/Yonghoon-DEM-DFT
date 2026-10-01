#!/usr/bin/env python3
"""gpu_runtime_tally.py — 한 기간 동안 서버에서 돈 계산의 잡 수·실행 시간을 **출력 파일에 박힌 시간**으로 집계한다 (월별 증빙 · 스케줄러 없는 단일 노드).

    python3 tools/reports/gpu_runtime_tally.py --since 2026-09-01 --until 2026-10-01            # 기본 루트 /data/work/runs · /root/work/runs
    python3 tools/reports/gpu_runtime_tally.py --roots /data/work/runs --since … --until … --keys 3
    python3 tools/reports/gpu_runtime_tally.py --selftest

읽는 것 (파일 안의 시간만 쓴다 — 추측하지 않는다):
  · QE pw.x/neb.x 출력 (이름에 .out · 'Program PWSCF'/'Program NEB'): 'starts on DDMonYYYY at HH:MM:SS' · 'terminated on' ·
    마지막 'PWSCF/NEB : … WALL' · 'JOB DONE.' · 'GPU acceleration is ACTIVE'(GPU) · 'Number of MPI processes'(랭크) ·
    'Program stopped by user request'(EXIT 로 세움). 끝 줄이 없으면(진행 중·중단) 시작~마지막 기록을 ≈ 로 쓴다.
  · ORCA 출력 ('O   R   C   A'): 'TOTAL RUN TIME: d days h hours m minutes s seconds' · 'ORCA TERMINATED NORMALLY' · 'parallel MPI-processes'
  · LOBSTER lobsterout: 'starting on host … on YYYY-MM-DD at HH:MM:SS' · 'using N threads' · 'finished in X h Y min Z s'
  · UMA MD (disorder_ensemble_diffusion): ensemble_results.json 의 runtime_min (끝난 런) · run_meta.json 만 있으면 진행/중단 (≈)
  · UMA 담금질 (melt_quench_uma): result.json 의 run.wall_min · plan.json 만 있으면 진행/중단 (≈)
  · UMA 이완 (relax_uma_d3): relax_meta.json 의 wall_s · calculator.device
기간: 잡의 [시작, 끝] 이 [since, until) 와 겹치면 센다. 시간 합은 기간 안으로 자른 값이다. 'GPU 점유' 는 GPU 잡 구간의 합집합이다.
트랙: 루트 바로 아래 폴더 이름을 TRACKS 정규식으로 나눈다 (못 맞추면 '기타' — 버리지 않고 목록에 남긴다).

⛔ 못 하는 것: 스케줄러 회계(sacct)가 아니다 — 파일에 박힌 시간이다 · 지운 출력은 못 센다 · 복사로 mtime 이 바뀐 파일은 기간이 틀릴 수 있다 ·
  같은 GPU 에 동시에 돈 잡은 잡-시간이 겹쳐 더해진다 (그래서 점유를 합집합으로 따로 낸다) · 랭크·스레드 수를 모르면 1 로 세고 그 수를 밝힌다 ·
  시작 시각이 파일에 없으면 끝 − 실행시간으로 추정한다 · 계산 결과(에너지·물성)는 읽지 않는다.
"""
import argparse
import datetime as dt
import json
import os
import pwd
import grp
import re
import stat
import sys
import time

TRACKS = [
    ("① W_ad interface (DEM input)", r"^wad_"),
    ("② Nd cathode interface (CEI)", r"^(cei_|nd_|icohp|ndo_)"),
    ("③ glass small cell (Li transport)", r"^(lpscl_glass|lpscl_smallcell|glass_)"),
    ("④ crystalline transport · framework · elastic", r"^(b2o3|elastic_|gap_nscf|committee_|modelc_|lpsocl_|lpscl16_)"),
    ("⑤ SDCP self-doping (molecular)", r"^sdcp_"),
]
OTHER = "기타 (트랙 밖)"
PRUNE = re.compile(r"(\.save$|^tmp|^_tmp|^__pycache__$|^\.git$|^wfc)")
MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
HEAD, TAIL = 65536, 262144


def _read_ends(p):
    sz = os.path.getsize(p)
    with open(p, "rb") as f:
        h = f.read(HEAD)
        if sz > HEAD + TAIL:
            f.seek(sz - TAIL)
        t = f.read() if sz > HEAD else b""
    dec = lambda b: b.decode("utf-8", "replace")
    return dec(h), dec(h + t) if sz <= HEAD + TAIL else dec(h) + "\n" + dec(t)


def qe_clock(s):
    """QE 시간 문자열 ('1d 3h20m' · '2h33m' · '5m 4.96s' · '12.34s') → 초."""
    m = re.fullmatch(r"\s*(?:(\d+)d)?\s*(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:([\d.]+)s)?\s*", s)
    if not m or not any(m.groups()):
        return None
    d, h, mi, se = (float(x) if x else 0.0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + se


def _epoch(y, mon, d, H, M, S):
    try:
        return time.mktime((int(y), int(mon), int(d), int(H), int(M), int(S), 0, 0, -1))
    except (ValueError, OverflowError):
        return None


def parse_qe(p, head, text):
    prog = "NEB" if "Program NEB" in head else "PWSCF"
    st = re.search(r"starts on\s+(\d{1,2})([A-Za-z]{3})(\d{4}) at\s+(\d{1,2}):\s*(\d{1,2}):\s*(\d{1,2})", head)
    start = _epoch(st.group(3), MON.get(st.group(2), 0), st.group(1), st.group(4), st.group(5), st.group(6)) if st and st.group(2) in MON else None
    tm = re.findall(r"terminated on:\s+(\d{1,2}):\s*(\d{1,2}):\s*(\d{1,2})\s+(\d{1,2})([A-Za-z]{3})(\d{4})", text)
    end = None
    if tm and tm[-1][4] in MON:
        H, M, S, d, mon, y = tm[-1]
        end = _epoch(y, MON[mon], d, H, M, S)
    walls = re.findall(prog + r"\s*:\s*(.+?)CPU\s+(.+?)WALL", text)
    wall = qe_clock(walls[-1][1]) if walls else None
    mtime = os.path.getmtime(p)
    if end is None:
        end = mtime
    approx = False
    if wall is None:
        if start is not None:
            wall, approx = max(0.0, end - start), True
        else:
            cpu = re.findall(r"total cpu time spent up to now is\s+([\d.]+)\s+secs", text)
            wall, approx = (float(cpu[-1]), True) if cpu else (None, True)
    if start is None and wall is not None:
        start = end - wall
    nproc = re.search(r"Number of MPI processes:\s+(\d+)", head)
    status = ("stopped" if re.search(r"Program stopped by user request|Maximum CPU time exceeded", text)
              else "done" if "JOB DONE." in text else "running/cut")
    return {"kind": "QE " + ("neb.x" if prog == "NEB" else "pw.x"), "gpu": "GPU acceleration is ACTIVE" in head,
            "start": start, "end": end, "wall_s": wall, "approx": approx, "nproc": int(nproc.group(1)) if nproc else None, "status": status}


def parse_orca(p, head, text):
    rt = re.findall(r"TOTAL RUN TIME:\s*(\d+) days (\d+) hours (\d+) minutes (\d+) seconds", text)
    wall = (int(rt[-1][0]) * 86400 + int(rt[-1][1]) * 3600 + int(rt[-1][2]) * 60 + int(rt[-1][3])) if rt else None
    end = os.path.getmtime(p)
    npr = re.search(r"running with\s+(\d+)\s+parallel MPI-processes", text)
    return {"kind": "ORCA", "gpu": False, "start": (end - wall) if wall is not None else None, "end": end, "wall_s": wall,
            "approx": wall is None, "nproc": int(npr.group(1)) if npr else None,
            "status": "done" if "ORCA TERMINATED NORMALLY" in text else "running/cut"}


def parse_lobster(p, head, text):
    st = re.search(r"starting on host .*? on (\d{4})-(\d{2})-(\d{2}) at (\d{2}):(\d{2}):(\d{2})", head)
    start = _epoch(*st.groups()) if st else None
    fin = re.search(r"finished in\s+(\d+)\s*h\s+(\d+)\s*min\s+([\d.]+)\s*s", text)
    wall = int(fin.group(1)) * 3600 + int(fin.group(2)) * 60 + float(fin.group(3)) if fin else None
    end = os.path.getmtime(p)
    approx = False
    if wall is None and start is not None:
        wall, approx = max(0.0, end - start), True
    if start is None and wall is not None:
        start = end - wall
    th = re.search(r"using\s+(\d+)\s+threads", head)
    return {"kind": "LOBSTER", "gpu": False, "start": start, "end": end, "wall_s": wall, "approx": approx or wall is None,
            "nproc": int(th.group(1)) if th else None, "status": "done" if fin else "running/cut"}


def _newest_mtime(d):
    best = 0.0
    for e in os.scandir(d):
        try:
            if e.is_file(follow_symlinks=False):
                best = max(best, e.stat(follow_symlinks=False).st_mtime)
        except OSError:
            pass
    return best


def parse_json_job(p, name):
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:  # noqa: BLE001 — 깨진 JSON 은 잡이 아니다
        return None
    if not isinstance(d, dict):
        return None
    end, folder = os.path.getmtime(p), os.path.dirname(p)
    if name == "ensemble_results.json":
        if "runtime_min" not in d:
            return None                     # 중간 저장본 — run_meta.json 쪽에서 진행 중으로 센다
        wall = float(d["runtime_min"]) * 60
        rm = os.path.join(folder, "run_meta.json")
        start = os.path.getmtime(rm) if os.path.exists(rm) else end - wall
        return {"kind": "UMA MD", "gpu": True, "start": min(start, end - wall), "end": end, "wall_s": wall, "approx": False, "nproc": None, "status": "done"}
    if name == "run_meta.json":
        er = os.path.join(folder, "ensemble_results.json")
        try:
            if os.path.exists(er) and "runtime_min" in json.load(open(er, encoding="utf-8")):
                return None                 # 끝난 런 — ensemble_results.json 쪽에서 센다
        except Exception:  # noqa: BLE001
            pass
        start, last = end, _newest_mtime(folder)
        for sub in os.scandir(folder):      # 온도 하위 폴더의 최신 기록까지
            if sub.is_dir(follow_symlinks=False):
                last = max(last, _newest_mtime(sub.path))
        return {"kind": "UMA MD", "gpu": True, "start": start, "end": max(last, start), "wall_s": max(0.0, last - start), "approx": True, "nproc": None, "status": "running/cut"}
    if name == "result.json" and isinstance(d.get("run"), dict) and "wall_min" in d["run"] and "plan" in d:
        wall = float(d["run"]["wall_min"]) * 60
        return {"kind": "UMA quench", "gpu": True, "start": end - wall, "end": end, "wall_s": wall, "approx": False, "nproc": None, "status": "done"}
    if name == "plan.json" and not os.path.exists(os.path.join(folder, "result.json")) and ("quench_rate" in json.dumps(d) or "T_melt" in json.dumps(d)):
        last = _newest_mtime(folder)
        return {"kind": "UMA quench", "gpu": True, "start": end, "end": max(last, end), "wall_s": max(0.0, last - end), "approx": True, "nproc": None, "status": "running/cut"}
    if name == "relax_meta.json" and "wall_s" in d:
        wall = float(d["wall_s"])
        dev = str((d.get("calculator") or {}).get("device", "cuda")).lower()
        return {"kind": "UMA relax", "gpu": dev != "cpu", "start": end - wall, "end": end, "wall_s": wall, "approx": False, "nproc": None,
                "status": "done" if d.get("converged_fmax") else "unconverged"}
    return None


JSON_NAMES = ("ensemble_results.json", "run_meta.json", "result.json", "plan.json", "relax_meta.json")


def scan(roots, since, until, prune=PRUNE):
    jobs = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not prune.search(d)]
            for fn in filenames:
                p = os.path.join(dirpath, fn)
                try:
                    stt = os.stat(p, follow_symlinks=False)
                except OSError:
                    continue
                if not stat.S_ISREG(stt.st_mode) or stt.st_mtime < since:
                    continue                 # 끝이 기간 앞이면 겹칠 수 없다
                rec = None
                if fn in JSON_NAMES:
                    rec = parse_json_job(p, fn)
                elif fn == "lobsterout" or fn.startswith("lobsterout"):
                    head, text = _read_ends(p)
                    rec = parse_lobster(p, head, text) if "LOBSTER" in head or "finished in" in text else None
                elif re.search(r"\.out(\.|$)", fn):
                    head, text = _read_ends(p)
                    if "Program PWSCF" in head or "Program NEB" in head:
                        rec = parse_qe(p, head, text)
                    elif "O   R   C   A" in head:
                        rec = parse_orca(p, head, text)
                if not rec or rec["start"] is None:
                    continue
                if rec["start"] >= until or rec["end"] < since:
                    continue
                rel = os.path.relpath(p, root)
                rec.update(path=p, rel=rel, root=root, top=rel.split(os.sep)[0], track=track_of(rel.split(os.sep)[0]))
                rec["in_s"] = max(0.0, min(rec["end"], until) - max(rec["start"], since))
                jobs.append(rec)
    return jobs


def track_of(top):
    for name, pat in TRACKS:
        if re.search(pat, top):
            return name
    return OTHER


def union_hours(intervals):
    tot, cur = 0.0, None
    for a, b in sorted(intervals):
        if cur is None or a > cur[1]:
            if cur:
                tot += cur[1] - cur[0]
            cur = [a, b]
        else:
            cur[1] = max(cur[1], b)
    if cur:
        tot += cur[1] - cur[0]
    return tot / 3600


def fmt_dhms(s):
    s = int(round(s or 0)); d, r = divmod(s, 86400); h, r = divmod(r, 3600); m, s = divmod(r, 60)
    return f"{d}-{h:02d}:{m:02d}:{s:02d}"


def ls_line(p, root):
    st = os.stat(p)
    try:
        own, grpn = pwd.getpwuid(st.st_uid).pw_name, grp.getgrgid(st.st_gid).gr_name
    except KeyError:
        own, grpn = str(st.st_uid), str(st.st_gid)
    t = time.strftime("%b %d %H:%M", time.localtime(st.st_mtime))
    return f"{stat.filemode(st.st_mode)} {st.st_nlink} {own} {grpn} {st.st_size:>10d} {t} {os.path.relpath(p, root)}"


def summarize(jobs, since, until):
    from collections import Counter, OrderedDict
    by_kind = Counter(j["kind"] for j in jobs)
    status = Counter(j["status"] for j in jobs)
    gpu = [j for j in jobs if j["gpu"]]
    cpu = [j for j in jobs if not j["gpu"]]
    out = {"n_jobs": len(jobs), "by_kind": dict(by_kind), "status": dict(status),
           "gpu_job_h": sum(j["in_s"] for j in gpu) / 3600,
           "gpu_union_h": union_hours([(max(j["start"], since), min(j["end"], until)) for j in gpu if j["in_s"] > 0]),
           "window_h": (until - since) / 3600,
           "cpu_core_h": sum(j["in_s"] * (j["nproc"] or 1) for j in cpu) / 3600,
           "cpu_nproc_unknown": sum(1 for j in cpu if not j["nproc"]),
           "approx_n": sum(1 for j in jobs if j["approx"])}
    lj = max((j for j in jobs if j["wall_s"]), key=lambda j: j["wall_s"], default=None)
    out["longest"] = None if lj is None else {"wall": lj["wall_s"], "rel": lj["rel"], "kind": lj["kind"], "gpu": lj["gpu"], "status": lj["status"], "approx": lj["approx"]}
    tracks = OrderedDict((n, []) for n, _ in TRACKS + [(OTHER, None)])
    for j in jobs:
        tracks[j["track"]].append(j)
    out["tracks"] = tracks
    return out


def report(jobs, since, until, keys=3, title="GABIA GPU SERVER (RTX A6000)"):
    s = summarize(jobs, since, until)
    bar = "=" * 62
    d0, d1 = dt.date.fromtimestamp(since), dt.date.fromtimestamp(until - 1)
    L = [bar, f"  Campaign total runtime ({d0} ~ {d1}) — {title}", bar, ""]
    if not jobs:
        L += ["> 기간 안에 걸린 계산 출력이 없다 (루트·기간을 확인)", bar]
        return "\n".join(L)
    order = ["QE pw.x", "QE neb.x", "UMA MD", "UMA quench", "UMA relax", "ORCA", "LOBSTER"]
    kinds = " · ".join(f"{k} {s['by_kind'][k]}" for k in order if k in s["by_kind"])
    st = s["status"]
    L += ["> Jobs in window",
          f"  jobs                    : {s['n_jobs']}  ({kinds})",
          f"  done / stopped / unconverged / running-or-cut : {st.get('done', 0)} / {st.get('stopped', 0)} / {st.get('unconverged', 0)} / {st.get('running/cut', 0)}",
          f"  time read from files    : exact {s['n_jobs'] - s['approx_n']} · approx {s['approx_n']} (no end line yet — start→last write)", "",
          "> GPU (RTX A6000 · 1 card)",
          f"  GPU job-hours (in window) : {s['gpu_job_h']:,.1f} h  (jobs sharing the card are counted separately)",
          f"  GPU occupied (union)      : {s['gpu_union_h']:,.1f} h of {s['window_h']:,.0f} h ({100 * s['gpu_union_h'] / s['window_h']:.1f} %)", "",
          "> CPU (MPI ranks / threads from the outputs)",
          f"  core-hours (in window)    : {s['cpu_core_h']:,.1f} core·h" + (f"  (rank count unknown → 1 : {s['cpu_nproc_unknown']} jobs)" if s["cpu_nproc_unknown"] else ""), ""]
    lg = s["longest"]
    if lg:
        L += [f"> longest single run      : {fmt_dhms(lg['wall'])}{' ≈' if lg['approx'] else ''}  {lg['rel']}  ({lg['kind']} · {'GPU' if lg['gpu'] else 'CPU'} · {lg['status']})", ""]
    L.append("> By track (run folders under the roots · key output files = newest first)")
    for name, js in s["tracks"].items():
        if not js:
            continue
        g = sum(j["in_s"] for j in js if j["gpu"]) / 3600
        c = sum(j["in_s"] * (j["nproc"] or 1) for j in js if not j["gpu"]) / 3600
        from collections import Counter
        kc = Counter((j["kind"], "GPU" if j["gpu"] else "CPU") for j in js)
        dc = Counter(j["kind"] for j in js if j["status"] == "done")
        L.append(f"  {name}")
        L.append(f"    jobs {len(js)} · GPU {g:,.1f} h · CPU {c:,.1f} core·h · folders {len(set(j['top'] for j in js))}")
        L.append("    " + " · ".join(f"{k}({dev}) {n} (done {dc.get(k, 0)})" for (k, dev), n in sorted(kc.items())))
        for j in sorted(js, key=lambda j: -j["end"])[:keys]:
            try:
                L.append("      " + ls_line(j["path"], j["root"]))
            except OSError:
                L.append(f"      (사라짐) {j['rel']}")
        if name == OTHER:
            L.append("    folders: " + ", ".join(sorted(set(j["top"] for j in js)))[:300])
    L.append(bar)
    return "\n".join(L)


def _day(s):
    return time.mktime(dt.datetime.strptime(s, "%Y-%m-%d").timetuple())


def _selftest():
    import tempfile
    ok = bad = 0

    def ck(name, cond, info=""):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print(f"  ✗ {name} {info}")
    ck("qe_clock '1d 3h20m' = 98400", qe_clock("1d 3h20m") == 98400)
    ck("qe_clock '5m 4.96s' = 304.96", abs(qe_clock("5m 4.96s") - 304.96) < 1e-9)
    ck("qe_clock '2h33m' = 9180", qe_clock("2h33m") == 9180)
    ck("⛔음성 qe_clock 빈 문자열 → None", qe_clock("   ") is None)
    since, until = _day("2026-09-01"), _day("2026-10-01")
    with tempfile.TemporaryDirectory() as T:
        R = os.path.join(T, "runs")

        def w(rel, txt, mt):
            p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w").write(txt); os.utime(p, (mt, mt)); return p
        ep = lambda s: time.mktime(dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple())
        # ① QE GPU 완주 (시작·끝 줄 있음 · 9월 안)
        w("wad_v4/V4_bound/pw.out", "     Program PWSCF v.7.4.1 starts on 27Sep2026 at 10:52:00\n     Number of MPI processes:                 1\n"
          "     GPU acceleration is ACTIVE.  1 visible GPUs per MPI rank\n ...\n     PWSCF        :   2h30m CPU   2h35m WALL\n\n"
          "   This run was terminated on:  13:27:00  27Sep2026\n\n=------------------------------------------------------------------------------=\n   JOB DONE.\n", ep("2026-09-27 13:27:00"))
        # ② QE CPU 8 랭크 · 8월 31일 시작 9월 1일 끝 (기간으로 잘림)
        w("cei_gap/NdPS4/nscf.out", "     Program PWSCF v.7.4.1 starts on 31Aug2026 at 20:00:00\n     Number of MPI processes:                 8\n"
          "     PWSCF        :   7h50m CPU   8h 0m WALL\n   This run was terminated on:   4:00:00   1Sep2026\n   JOB DONE.\n", ep("2026-09-01 04:00:00"))
        # ③ QE GPU EXIT 로 세움 (끝 줄 · stopped)
        w("elastic_m/strain_23_p.out.stopped_0927", "     Program PWSCF v.7.4.1 starts on 26Sep2026 at 18:11:00\n     GPU acceleration is ACTIVE.\n"
          "     Program stopped by user request\n     PWSCF        :   20h 0m CPU   21h 0m WALL\n   JOB DONE.\n", ep("2026-09-27 15:11:00"))
        # ④ QE GPU 진행 중 (끝 줄 없음 · 9월 30일 시작 · 10월 1일까지 씀 → 9월 안 시간만)
        w("elastic_m/strain_23_m.out", "     Program PWSCF v.7.4.1 starts on 30Sep2026 at 12:00:00\n     GPU acceleration is ACTIVE.\n"
          "     total cpu time spent up to now is     3600.0 secs\n", ep("2026-10-01 02:00:00"))
        # ⑤ ORCA 완주 (8 랭크)
        w("sdcp_n6b/n6.out", "                                 * O   R   C   A *\n   Program running with 8 parallel MPI-processes\n"
          "                             ****ORCA TERMINATED NORMALLY****\nTOTAL RUN TIME: 0 days 3 hours 0 minutes 0 seconds 12 msec\n", ep("2026-09-05 09:00:00"))
        # ⑥ LOBSTER 완주 (스레드 수 없음 → 1)
        w("nd_ppswap/lob/lobsterout", "LOBSTER v5.1.1\nstarting on host gabia on 2026-09-19 at 08:00:00.000 KST\n...\nfinished in 1 h 0 min 0 s 1 ms of wall time\n", ep("2026-09-19 09:00:00"))
        # ⑦ UMA MD 완주 (runtime_min 120) · ⑧ UMA MD 진행 중 (run_meta 만)
        w("b2o3_ev/s2/run_meta.json", json.dumps({"label": "s2"}), ep("2026-09-24 00:00:00"))
        w("b2o3_ev/s2/ensemble_results.json", json.dumps({"label": "s2", "runtime_min": 120.0}), ep("2026-09-24 02:00:00"))
        w("lpscl_glass_main/T550_s3/run_meta.json", json.dumps({"label": "x"}), ep("2026-09-29 10:00:00"))
        w("lpscl_glass_main/T550_s3/T550/msd.json", "{}", ep("2026-09-29 13:00:00"))
        w("lpscl_glass_main/T550_s3/ensemble_results.json", json.dumps({"label": "x", "levels": []}), ep("2026-09-29 12:00:00"))   # 중간 저장본
        # ⑨ UMA 담금질 완주 · ⑩ UMA 이완
        w("lpscl_glass_q/seed5/result.json", json.dumps({"plan": {"seed": 5}, "run": {"wall_min": 30.0}}), ep("2026-09-23 12:00:00"))
        w("wad_s2/V3_s_outer/A/relax/relax_meta.json", json.dumps({"wall_s": 99.0, "converged_fmax": True, "calculator": {"device": "cuda"}}), ep("2026-09-25 22:40:00"))
        # ⛔ 음성: 기간 밖 (8월에 끝남) · QE 도 ORCA 도 아닌 .out · 깨진 JSON · 무관한 result.json · .save 안의 출력(가지치기)
        w("wad_old/pw.out", "     Program PWSCF v.7.4.1 starts on 10Aug2026 at 10:00:00\n     PWSCF        :   1h CPU   1h 0m WALL\n   JOB DONE.\n", ep("2026-08-10 11:00:00"))
        w("cei_gap/notes.out", "just a log line\n", ep("2026-09-10 10:00:00"))
        w("cei_gap/relax_meta.json", "{broken", ep("2026-09-10 10:00:00"))
        w("cei_gap/x/result.json", json.dumps({"ok": 1}), ep("2026-09-10 10:00:00"))
        w("elastic_m/tmp/x.save/pw.out", "     Program PWSCF v.7.4.1 starts on 10Sep2026 at 10:00:00\n     PWSCF        :   1h CPU   1h 0m WALL\n   JOB DONE.\n", ep("2026-09-10 11:00:00"))
        w("misc_run/pw.out", "     Program PWSCF v.7.4.1 starts on 12Sep2026 at 10:00:00\n     PWSCF        :   1h CPU   1h 0m WALL\n   JOB DONE.\n", ep("2026-09-12 11:00:00"))
        jobs = scan([R], since, until)
        by = {j["rel"]: j for j in jobs}
        ck("잡 11 개 (양성 ①–⑩ + 기타 1 · 음성 5 제외)", len(jobs) == 11, sorted(by))
        a = by.get("wad_v4/V4_bound/pw.out", {})
        ck("① QE GPU 완주: WALL 2h35m · done · GPU · 트랙 ①", a.get("wall_s") == 9300 and a.get("status") == "done" and a.get("gpu") and a.get("track", "").startswith("①"), a)
        b = by.get("cei_gap/NdPS4/nscf.out", {})
        ck("② 8월 31일 시작 → 9월 안 4 h 만 · CPU 8 랭크", abs(b.get("in_s", 0) - 4 * 3600) < 1 and b.get("nproc") == 8 and not b.get("gpu"), b)
        c = by.get("elastic_m/strain_23_p.out.stopped_0927", {})
        ck("③ EXIT 로 세운 출력 = stopped (JOB DONE 이 있어도)", c.get("status") == "stopped" and c.get("wall_s") == 21 * 3600, c)
        d = by.get("elastic_m/strain_23_m.out", {})
        ck("④ 진행 중: 시작~마지막 기록 ≈ · 9월 안 12 h 로 잘림", d.get("approx") and d.get("status") == "running/cut" and abs(d.get("in_s", 0) - 12 * 3600) < 1, d)
        e = by.get("sdcp_n6b/n6.out", {})
        ck("⑤ ORCA: 3 h · 8 랭크 · done · 트랙 ⑤", e.get("wall_s") == 10800 and e.get("nproc") == 8 and e.get("status") == "done" and e.get("track", "").startswith("⑤"), e)
        f = by.get("nd_ppswap/lob/lobsterout", {})
        ck("⑥ LOBSTER: 1 h · done · 스레드 모름(None) · 트랙 ②", f.get("wall_s") == 3600 and f.get("nproc") is None and f.get("track", "").startswith("②"), f)
        g = by.get("b2o3_ev/s2/ensemble_results.json", {})
        ck("⑦ UMA MD 완주 runtime_min 120 → 2 h · 트랙 ④", g.get("wall_s") == 7200 and g.get("track", "").startswith("④"), g)
        h = by.get("lpscl_glass_main/T550_s3/run_meta.json", {})
        ck("⑧ UMA MD 진행 중: 중간 저장본은 끝난 런이 아니다 · 하위 폴더 최신 기록까지 3 h ≈", h.get("status") == "running/cut" and abs(h.get("wall_s", 0) - 3 * 3600) < 1
           and "lpscl_glass_main/T550_s3/ensemble_results.json" not in by, h)
        ck("⑨ UMA 담금질 30 min · ⑩ UMA 이완 99 s", by.get("lpscl_glass_q/seed5/result.json", {}).get("wall_s") == 1800
           and by.get("wad_s2/V3_s_outer/A/relax/relax_meta.json", {}).get("wall_s") == 99.0)
        ck("⛔음성: 8월에 끝난 출력 · 아무 .out · 깨진 JSON · 무관한 result.json · .save 안 출력은 안 센다",
           not any(k in by for k in ("wad_old/pw.out", "cei_gap/notes.out", "cei_gap/relax_meta.json", "cei_gap/x/result.json", "elastic_m/tmp/x.save/pw.out")))
        ck("트랙 밖 폴더는 버리지 않고 기타로", by.get("misc_run/pw.out", {}).get("track") == OTHER)
        s = summarize(jobs, since, until)
        gpu_in = (9300 + 21 * 3600 + 12 * 3600 + 7200 + 3 * 3600 + 1800 + 99) / 3600
        ck("GPU 잡-시간 합 = 각 GPU 잡의 9월 안 시간 합", abs(s["gpu_job_h"] - gpu_in) < 1e-6, (s["gpu_job_h"], gpu_in))
        ck("GPU 점유(합집합) ≤ 잡-시간 합 (겹친 잡을 두 번 안 센다)", s["gpu_union_h"] <= s["gpu_job_h"] + 1e-9)
        ck("CPU core·h = 4 h×8 + 3 h×8 + LOBSTER 1 h×1(모름) + 기타 1 h×1(모름)", abs(s["cpu_core_h"] - (32 + 24 + 1 + 1)) < 1e-6 and s["cpu_nproc_unknown"] == 2, (s["cpu_core_h"], s["cpu_nproc_unknown"]))
        ck("최장 런 = EXIT 로 세운 탄성 21 h", s["longest"]["rel"] == "elastic_m/strain_23_p.out.stopped_0927", s["longest"])
        ck("union_hours: [0,2]+[1,3]+[5,6] h = 4 h", abs(union_hours([(0, 7200), (3600, 10800), (18000, 21600)]) - 4) < 1e-9)
        txt = report(jobs, since, until)
        ck("보고서: 머리 · 트랙 ①–⑤ · 기타 · ls 줄", all(t in txt for t in ("Campaign total runtime", "① W_ad", "② Nd", "③ glass", "④ crystalline", "⑤ SDCP", OTHER, "-rw")), txt[:200])
        ck("⛔음성 빈 루트 → '출력이 없다' (0 으로 꾸미지 않는다)", "없다" in report(scan([os.path.join(T, "none")], since, until), since, until))
    print(f"{'✅' if bad == 0 else '⛔'} gpu_runtime_tally selftest {ok}/{ok + bad} 통과")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--roots", nargs="+", default=["/data/work/runs", "/root/work/runs"])
    ap.add_argument("--since", help="YYYY-MM-DD (포함)")
    ap.add_argument("--until", help="YYYY-MM-DD (제외)")
    ap.add_argument("--keys", type=int, default=3, help="트랙마다 찍을 대표 출력 파일 수")
    ap.add_argument("--title", default="GABIA GPU SERVER (RTX A6000)")
    ap.add_argument("--json", help="잡 목록을 JSON 으로도 저장")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.since and a.until):
        ap.error("--since · --until 이 필요하다")
    since, until = _day(a.since), _day(a.until)
    jobs = scan(a.roots, since, until)
    print(report(jobs, since, until, a.keys, a.title))
    if a.json:
        json.dump([{k: v for k, v in j.items() if k != "root"} for j in jobs], open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    return 0


if __name__ == "__main__":
    sys.exit(main())
