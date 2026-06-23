#!/usr/bin/env python3
"""COMSOL batch 로그 + nvidia-smi 샘플 → 지표 추출 / 벤치마크 요약.

표준 라이브러리만 사용 (서버 의존성 최소화).

모드 1 (단일 실행):  --log ... --gpu-csv ... --model ... --json out.json
모드 2 (벤치 요약):  --summarize-bench --cpu-model A --gpu-model B --results DIR --csv f.csv
"""
import argparse
import csv
import datetime
import glob
import json
import os
import re
import sys


def read(path):
    try:
        with open(path, "r", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def parse_comsol_log(text):
    """COMSOL batch 로그에서 DOF/시간/메모리/솔버 흔적/에러 추출 (best-effort)."""
    m = {}
    dof = re.findall(r"degrees of freedom solved for:\s*([\d,]+)", text, re.I)
    m["dof"] = int(dof[-1].replace(",", "")) if dof else None

    st = re.findall(r"Solution time:\s*([\d.]+)\s*s", text, re.I)
    if not st:
        st = re.findall(r"\bTime:\s*([\d.]+)\s*s", text, re.I)
    m["solution_time_s"] = float(st[-1]) if st else None

    mems_mb = []
    for val, unit in re.findall(r"(?:Physical memory|Memory):\s*([\d.]+)\s*(GB|MB)", text, re.I):
        mems_mb.append(float(val) * (1024.0 if unit.upper() == "GB" else 1.0))
    m["peak_mem_MB"] = max(mems_mb) if mems_mb else None

    found = [s for s in ("cuDSS", "GPU", "MUMPS", "PARDISO", "SPOOLES")
             if re.search(re.escape(s), text, re.I)]
    m["solver_mentions"] = found

    m["errors"] = re.findall(r"^.*\b(?:Error|out of memory|failed to)\b.*$", text, re.I | re.M)[:10]
    return m


def parse_gpu_csv(path):
    util, mem = [], []
    if not path or not os.path.exists(path):
        return {"gpu_max_util": None, "gpu_max_mem_MiB": None, "gpu_samples": 0}
    with open(path) as f:
        for i, line in enumerate(f):
            if i == 0 and "timestamp" in line.lower():
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                try:
                    util.append(float(parts[1]))
                    mem.append(float(parts[2]))
                except ValueError:
                    pass
    return {
        "gpu_max_util": max(util) if util else None,
        "gpu_max_mem_MiB": max(mem) if mem else None,
        "gpu_samples": len(util),
    }


def is_gpu_confirmed(log_m, gpu_m):
    mentions = [s.lower() for s in log_m.get("solver_mentions", [])]
    sig_log = ("cudss" in mentions) or ("gpu" in mentions)
    sig_util = (gpu_m.get("gpu_max_util") or 0) >= 10
    return bool(sig_log or sig_util), {"log_signal": sig_log, "util_signal": sig_util}


def fmt(v):
    if v is None:
        return "?"
    if isinstance(v, float):
        return f"{v:,.1f}"
    return f"{v:,}" if isinstance(v, int) else str(v)


def print_summary(o):
    print("\n──────── 실행 요약 ────────")
    print(f"  모델            : {o.get('model')}")
    print(f"  솔버(라벨)      : {o.get('solver_label')}   GPU 의도: {o.get('use_gpu_intended')}")
    print(f"  DOF             : {fmt(o.get('dof'))}")
    print(f"  솔루션 시간     : {fmt(o.get('solution_time_s'))} s")
    print(f"  wall-clock      : {fmt(o.get('wall_s'))} s")
    print(f"  피크 메모리     : {fmt(o.get('peak_mem_MB'))} MB")
    print(f"  GPU 최대 사용률 : {fmt(o.get('gpu_max_util'))} %   VRAM: {fmt(o.get('gpu_max_mem_MiB'))} MiB")
    if o.get("use_gpu_intended") and not o.get("gpu_confirmed"):
        print("  ⚠ GPU 의도했으나 사용 흔적 없음 → 모델 Direct 솔버가 cuDSS인지/저장됐는지 확인!")
    elif o.get("gpu_confirmed"):
        print("  ✅ GPU 사용 확인됨")
    if o.get("solver_mentions"):
        print(f"  로그 솔버 흔적  : {', '.join(o['solver_mentions'])}")
    if o.get("errors"):
        print(f"  ⚠ 에러/경고     : {len(o['errors'])}건 (batchlog 확인)")
    print("───────────────────────────\n")


def cmd_single(a):
    log_m = parse_comsol_log(read(a.log))
    gpu_m = parse_gpu_csv(a.gpu_csv)
    conf, sig = is_gpu_confirmed(log_m, gpu_m)
    out = {
        "model": a.model,
        "solver_label": a.solver,
        "use_gpu_intended": str(a.use_gpu).lower() == "true",
        "wall_s": float(a.wall) if a.wall else None,
        "gpu_confirmed": conf,
        "gpu_signals": sig,
    }
    out.update(log_m)
    out.update(gpu_m)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
    print_summary(out)


def latest_metrics(results_dir, model):
    files = sorted(glob.glob(os.path.join(results_dir, model, "*", "metrics.json")))
    if not files:
        return None
    with open(files[-1]) as f:
        return json.load(f)


def cmd_bench(a):
    cpu = latest_metrics(a.results, a.cpu_model)
    gpu = latest_metrics(a.results, a.gpu_model)
    if not cpu or not gpu:
        print("벤치 요약 실패: 두 모델의 metrics.json을 찾지 못함", file=sys.stderr)
        sys.exit(1)

    ts = datetime.datetime.now().isoformat(timespec="seconds")
    header = ["timestamp", "run", "model", "solver", "use_gpu", "dof",
              "solution_time_s", "wall_s", "peak_mem_MB", "gpu_max_util",
              "gpu_max_mem_MiB", "gpu_confirmed"]
    write_header = not os.path.exists(a.csv)
    with open(a.csv, "a", newline="") as f:
        w = csv.writer(f)
        if write_header:
            w.writerow(header)
        for tag, m in (("cpu", cpu), ("gpu", gpu)):
            w.writerow([ts, tag, m.get("model"), m.get("solver_label"),
                        m.get("use_gpu_intended"), m.get("dof"),
                        m.get("solution_time_s"), m.get("wall_s"),
                        m.get("peak_mem_MB"), m.get("gpu_max_util"),
                        m.get("gpu_max_mem_MiB"), m.get("gpu_confirmed")])

    def t(m):
        return m.get("solution_time_s") or m.get("wall_s")

    tc, tg = t(cpu), t(gpu)
    print("\n════════ 벤치마크: CPU vs GPU ════════")
    print(f"  이름      : {a.name}")
    print(f"  DOF       : {fmt(gpu.get('dof') or cpu.get('dof'))}")
    print(f"  CPU 시간  : {fmt(tc)} s   (솔버 {cpu.get('solver_label')})")
    print(f"  GPU 시간  : {fmt(tg)} s   (솔버 {gpu.get('solver_label')}, 사용확인={gpu.get('gpu_confirmed')})")
    if tc and tg and tg > 0:
        sp = tc / tg
        verdict = "GPU 유리" if sp > 1.1 else ("GPU 이득 미미" if sp > 0.9 else "GPU가 더 느림")
        print(f"  ▶ Speedup : {sp:.2f}×  ({verdict})")
    if not gpu.get("gpu_confirmed"):
        print("  ⚠ GPU 실행에서 GPU 사용이 확인되지 않음 — 비교가 무의미할 수 있음 (cuDSS 설정 확인)")
    print(f"  CSV       : {a.csv}")
    print("══════════════════════════════════════\n")


def main():
    p = argparse.ArgumentParser(description="COMSOL 로그/GPU 샘플 파서")
    p.add_argument("--summarize-bench", action="store_true")
    # 단일 실행
    p.add_argument("--log")
    p.add_argument("--gpu-csv", dest="gpu_csv")
    p.add_argument("--model")
    p.add_argument("--solver")
    p.add_argument("--use-gpu", dest="use_gpu", default="false")
    p.add_argument("--wall")
    p.add_argument("--json")
    # 벤치 요약
    p.add_argument("--cpu-model")
    p.add_argument("--gpu-model")
    p.add_argument("--results")
    p.add_argument("--csv")
    p.add_argument("--name", default="bench")
    a = p.parse_args()
    if a.summarize_bench:
        cmd_bench(a)
    else:
        cmd_single(a)


if __name__ == "__main__":
    main()
