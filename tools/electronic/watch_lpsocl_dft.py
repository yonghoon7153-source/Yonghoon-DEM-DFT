#!/usr/bin/env python3
"""watch_lpsocl_dft.py — LPSOCl **ELF + Bader 한 화면** (둘은 체인이라 같이 봐야 한다).

관례:  watch -n 60 python3 tools/electronic/watch_lpsocl_dft.py

왜 합쳤나
  Bader 는 ELF 가 CPU 를 놓아야 시작한다(run_lpsocl_bader_gabia.sh 의 WAIT 루프).
  따로 보면 "Bader 가 왜 안 시작하지"의 답이 항상 다른 창에 있다.

핵심 진단: **속도**
  QE 는 반복마다 `total cpu time spent up to now` 를 찍는다. 그 간격이 곧 반복 비용이고,
  거기에 남은 반복 수를 곱하면 끝나는 시각이 나온다. 이걸 안 보면 "돌고 있다"와
  "이번 생에 안 끝난다"를 구분할 수 없다 — 실제로 k444/ecut80 을 CPU 10코어로 돌려
  반복 1회에 3시간 이상 걸린 적이 있다.
"""
import glob
import os
import re
import subprocess
from datetime import datetime, timedelta

ELF = os.environ.get("ELF_DIR", "/data/work/runs/lpsocl_elf")
BAD = os.environ.get("BADER_DIR", "/data/work/runs/lpsocl_bader")
BAR = "-" * 72
NOW = datetime.now()


def sh(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=15).stdout
    except Exception:
        return ""


def procs(pat):
    """pgrep -f 를 argv 로 — shell 을 끼우면 자기 명령줄을 물어 항상 살아 보인다."""
    try:
        out = subprocess.run(["pgrep", "-f", pat], capture_output=True, text=True,
                             timeout=10).stdout.split()
    except Exception:
        return []
    return out


def ps_info(pids):
    if not pids:
        return []
    o = sh("ps -o pid=,etime=,pcpu=,rss=,cmd= -p " + ",".join(pids))
    return [l.strip() for l in o.splitlines() if l.strip()]


def read(p, n=None):
    try:
        t = open(p, errors="ignore").read()
        return t[-n:] if n else t
    except OSError:
        return ""


def mtime(p):
    try:
        return datetime.fromtimestamp(os.path.getmtime(p))
    except OSError:
        return None


def elf_stage(d):
    """ELF 단계는 **로그 문자열이 아니라 산출 파일**로 판정한다.

    ⚠ run.log 에 `[scf.in] ... -> scf.in (+scf_atomic.in)` 이라는 **입력 생성** 메시지가
      있어서, 'scf_atomic' 문자열 검색은 1단계부터 참이 된다. 실제로 그렇게 오보했다
      (본 scf 중인데 '③ scf_atomic' 으로 표시). 파일은 거짓말하지 않는다.
    """
    import os
    j = lambda f: os.path.join(d, f)
    if os.path.exists(j("lpsocl_rho_atomic.cube")):
        return "⑥ 완료 (rho_atomic 까지)"
    if os.path.exists(j("lpsocl_rho_scf.cube")):
        return "⑤ pp.x rho_atomic 중"
    if os.path.exists(j("lpsocl_elf.cube")):
        return "④ pp.x rho_scf 중"
    if os.path.exists(j("scf_atomic.out")):
        return "③ scf_atomic (본 scf 완료)"
    if os.path.exists(j("scf.out")):
        return "② scf (본 계산)"
    if os.path.isdir(j("pseudo")) and os.listdir(j("pseudo")):
        return "① pseudo 확보"
    return "· 기동 직후"


def scf_speed(out_path, maxstep=200):
    """QE 출력 → (반복수, 초/반복, 최근 accuracy, 예상 남은 시간 문자열)."""
    t = read(out_path)
    if not t:
        return None
    nk = re.search(r"number of k points=\s*(\d+)", t)
    nbnd = re.search(r"number of Kohn-Sham states=\s*(\d+)", t)
    its = re.findall(r"iteration #\s*(\d+)", t)
    # 'total cpu time spent up to now is   1234.5 secs'
    tcs = [float(x) for x in re.findall(r"total cpu time spent up to now is\s+([\d.]+)\s*secs", t)]
    acc = re.findall(r"estimated scf accuracy\s+<\s+([\d.E+-]+)", t)
    conv = re.search(r"convergence has been achieved in\s+(\d+)\s+iterations", t)
    thr = re.search(r"conv_thr\s*=\s*([\d.eEdD+-]+)", t)
    per = None
    if len(tcs) >= 2:
        # 마지막 3구간 평균 — 첫 구간은 초기화가 섞여 과대평가된다
        d = [b - a for a, b in zip(tcs, tcs[1:]) if b > a]
        if d:
            per = sum(d[-3:]) / len(d[-3:])
    return {"nk": nk.group(1) if nk else "?", "nbnd": nbnd.group(1) if nbnd else "?",
            "it": int(its[-1]) if its else 0, "n_marks": len(tcs),
            "elapsed_s": tcs[-1] if tcs else None, "per_it_s": per,
            "acc": acc[-1] if acc else None,
            "converged_in": int(conv.group(1)) if conv else None, "maxstep": maxstep,
            "acc_hist": acc, "conv_thr": (thr.group(1).replace("d", "e").replace("D", "e")
                                          if thr else None)}


def show_scf(tag, out_path, maxstep=200):
    s = scf_speed(out_path, maxstep)
    if not s:
        print(f"  {tag}: (출력 없음 — {out_path})")
        return
    lm = mtime(out_path)
    stale = (NOW - lm).total_seconds() / 60 if lm else None
    print(f"  {tag}: k-points {s['nk']} · bands {s['nbnd']} · "
          f"iteration #{s['it']}/{s['maxstep']}"
          + (f" · accuracy {s['acc']}" if s["acc"] else ""))
    if s["converged_in"]:
        flag = "  ⛔ **가짜 수렴 (maxstep 도달)**" if s["converged_in"] >= s["maxstep"] else "  ✓"
        print(f"     수렴 {s['converged_in']} iterations{flag}")
        return
    if s["per_it_s"]:
        h = s["per_it_s"] / 3600
        # ⚠⚠ **반복 비용만 보고 경보하면 안 된다.** 남은 반복 수는 maxstep 이 아니라
        #   **accuracy 궤적**이 정한다. 실측 두 번(2026-07-28 ELF, 07-29 Bader) 다
        #   "반복당 1h+ = 사실상 안 끝난다" 로 오경보했는데, 각각 15회·17회 만에 끝났다.
        #   도구가 계속 틀린 신호를 주면 언젠가 진짜로 죽이게 된다.
        need, eta, stalled = None, None, False
        try:
            hist = [float(x) for x in (s["acc_hist"] or [])][-4:]
            target = float(s["conv_thr"]) if s["conv_thr"] else 1e-8
            if len(hist) >= 2 and hist[-1] > target > 0:
                import math
                drops = [math.log10(a / b) for a, b in zip(hist, hist[1:]) if b > 0 and a > b]
                rate = sum(drops) / len(drops) if drops else 0.0   # 반복당 자릿수 감소
                if rate > 0.05:
                    need = math.ceil(math.log10(hist[-1] / target) / rate)
                    eta = need * h
                elif len(hist) >= 3:
                    # ⚠ 감소율이 거의 0 인 건 "궤적 부족"이 아니라 **정체 그 자체**다.
                    #   이걸 미상으로 처리하면 SDCP 형 발산(246회 0.51 Ry)을 놓친다.
                    stalled = rate
        except (ValueError, ZeroDivisionError, TypeError):
            pass
        line = f"     반복 1회 ≈ {h:.2f} h · 경과 {s['elapsed_s']/3600:.1f} h"
        if need is not None:
            line += f" · **accuracy 궤적 기준 남은 {need}회 ≈ {eta:.0f} h**"
        else:
            line += f" · maxstep 최악값 {h*max(0, s['maxstep']-s['it']):.0f} h (예상값 아님)"
        print(line)
        if stalled is not False:
            print(f"     ⛔ **정체 — 반복당 자릿수 감소 {stalled:.3f} (거의 0).** "
                  f"accuracy {s['acc']} 가 목표 {s['conv_thr']} 로 갈 기미가 없다. "
                  f"반복을 더 돌리는 건 낭비다 — 믹싱/스미어링/스핀 설정을 손대야 한다.")
        elif need is not None and eta > 48:
            print(f"     ⛔ **궤적으로도 {eta:.0f} h 남는다 = 재설계 필요.** "
                  f"k-mesh/컷오프/믹싱을 손대야 한다.")
        elif need is None and h > 1.0:
            print(f"     ⚠ 반복당 {h:.1f} h — 다만 accuracy 궤적이 아직 부족해 남은 시간은 미상. "
                  f"자릿수가 떨어지고 있으면 그냥 두는 게 맞다.")
    elif s["n_marks"] <= 1:
        print(f"     ⚠ 시간 마크가 {s['n_marks']}개뿐 — **첫 반복도 아직 안 끝났다**"
              + (f" (출력 {stale:.0f}분 정체)" if stale is not None else ""))
        print("     이 상태로 오래면 k-mesh/컷오프가 이 CPU 예산에 안 맞는 것이다.")
    if stale is not None and stale > 60:
        print(f"     ⚠ 출력이 {stale:.0f}분째 갱신 없음 — pcpu 가 0 이면 멈춘 것")


print("=" * 72)
print(f"LPSOCl ELF + Bader   {NOW:%m-%d %H:%M:%S}")
print("=" * 72)
la = open("/proc/loadavg").read().split()[:3] if os.path.exists("/proc/loadavg") else []
ncpu = int(sh("nproc").strip() or 1)
load1 = float(la[0]) if la else 0.0
print(f"CPU {ncpu} cores · load {' '.join(la)}")
# ⚠ **과다구독 탐지.** OMP_NUM_THREADS 를 안 걸면 MPI 랭크마다 코어 수만큼 스레드를 띄운다.
#   실측(2026-07-29): 20코어에 -np 10 → 200 스레드, load 154, SCF 반복 1회 3시간+.
#   반복이 느릴 때 k-mesh 부터 의심하면 엉뚱한 데를 고치게 된다 — 여기부터 본다.
if load1 > 1.5 * ncpu:
    print(f"  ⛔ **과다구독: load {load1:.0f} / {ncpu} cores = {load1/ncpu:.1f}배.** "
          f"스레드가 서로 밟는 중 — 이게 느림의 1순위 원인이다.")
    print("     원인 1순위: OMP_NUM_THREADS 미설정 (랭크당 코어 수만큼 스레드). "
          "OMP_NUM_THREADS=1 로 묶고 -nk 로 k 병렬을 써야 한다.")
cpu_qe = procs(r"qe-7\.4\.1-cpu/bin/(pw|pp)\.x")
gpu_qe = procs(r"qe-.*-gpu/bin/(pw|pp)\.x")
print(f"  CPU QE {len(cpu_qe)} rank · GPU QE {len(gpu_qe)} proc "
      f"(GPU 쪽은 우리 체인과 무관 — Bader 대기 조건에서 제외됨)")
# ⚠ mpirun 런처는 pcpu 0.0 이라 '멈춘 것처럼' 보인다. 실제 계산 랭크를 골라 보여준다.
ranks = [l for l in ps_info(cpu_qe) if "/pw.x" in l or "/pp.x" in l]
for l in ranks[:2] + ps_info(gpu_qe)[:1]:
    print("   " + l[:118])
if ranks:
    try:
        pcpu = [float(l.split()[2]) for l in ranks]
        print(f"   CPU QE 랭크 %CPU: 중앙 {sorted(pcpu)[len(pcpu)//2]:.0f}% "
              f"({len(pcpu)}랭크) — 0 이면 멈춘 것, 100 근처면 정상 계산 중")
    except (ValueError, IndexError):
        pass
gpu = sh("nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits").strip()
if gpu:
    print(f"  VRAM {gpu} MiB  ⚠ pw.x(GPU) 와 UMA 동시 실행은 CLAUDE.md 금지 조합")
print(BAR)

# ── ELF ────────────────────────────────────────────────────────────────
print("① ELF (+CDD)  " + ELF)
elog = os.path.join(ELF, "run.log")
if os.path.isfile(elog):
    t = read(elog)
    print(f"  단계: {elf_stage(ELF)}")
    show_scf("scf.out", os.path.join(ELF, "scf.out"))
    if os.path.exists(os.path.join(ELF, "scf_atomic.out")):
        show_scf("scf_atomic.out", os.path.join(ELF, "scf_atomic.out"), maxstep=1)
    cubes = sorted(glob.glob(os.path.join(ELF, "*.cube")))
    print(f"  cube {len(cubes)}개" + (": " + ", ".join(
        f"{os.path.basename(c)} {os.path.getsize(c)/1e6:.0f}MB" for c in cubes) if cubes else " (아직)"))
    err = [l.strip() for l in t.splitlines() if re.search(r"ERROR|%%%%|forrtl", l)]
    if err:
        print("  ⛔ " + err[-1][:110])
else:
    print("  (미가동)")
print(BAR)

# ── Bader ──────────────────────────────────────────────────────────────
print("② AE Bader (kjpaw + plot_num=17 — 기존 표와 비교 가능)  " + BAD)
blog = os.path.join(BAD, "run.log")
if os.path.isfile(blog):
    t = read(blog)
    for k, name in (("bader -p all_atom", "④ bader"), ("pp.x plot_num=17", "③ pp.x AE"),
                    ("pw.x scf_paw.in", "② scf(kjpaw)"), ("[pseudo] OK", "① pseudo"),
                    ("CPU QE", "⓪ CPU 해방 대기")):
        if k in t:
            print(f"  단계: {name}")
            break
    else:
        print("  단계: ? (기동 직후)")
    wait = [l for l in t.splitlines() if "재확인" in l]
    if wait:
        print(f"  대기 {len(wait)}회 — 마지막: {wait[-1].strip()[:100]}")
    show_scf("scf_paw.out", os.path.join(BAD, "scf_paw.out"))
    s = os.path.join(BAD, "lpsocl_bader_summary.json")
    if os.path.exists(s):
        import json
        try:
            d = json.load(open(s))["per_species"]
            print("  ✅ " + "  ".join(f"{k} {v['mean']:+.3f}" for k, v in d.items()))
            print("     비교: b2o3 P +4.691 / modelc 계열 P +4.34~4.69 (같은 AE·PAW 방법)")
        except Exception:
            print("  (summary 파싱 실패)")
    err = [l.strip() for l in t.splitlines() if l.strip().startswith("ERROR")]
    if err:
        print("  ⛔ " + err[-1][:110])
else:
    print("  (미가동)")
    print("  착수: mkdir -p /data/work/runs/lpsocl_bader && tmux new -s lpsoclbader -d \\")
    print("        'bash tools/electronic/run_lpsocl_bader_gabia.sh > /data/work/runs/lpsocl_bader/run.log 2>&1'")
print(BAR)

# ── 처방 ───────────────────────────────────────────────────────────────
print("처방 (⚠ **ELF 전용** — Bader 엔 적용 금지)")
print("  ⛔ Bader 의 k444 는 **바꾸면 안 된다** — 기존 bader_b2o3_vs_lpscl16.csv 와 같은")
print("     방법이어야 비교가 성립한다. Bader 가 느리면 pool(-nk)만 늘린다.")
print("  ELF 는 실공간 양이라 조밀한 k-mesh 가 필요 없다. gap 2.23 eV 절연체 62원자 셀이면")
print("  k 2×2×2 로 충분하고 비용은 대략 1/8 이다. k 병렬(-npool)도 같이 건다:")
print("    cd /data/work/runs/lpsocl_elf && sed -i 's/^  4 4 4 0 0 0/  2 2 2 0 0 0/' scf.in scf_atomic.in")
print("    mpirun --oversubscribe -np 10 /data/apps/qe-7.4.1-cpu/bin/pw.x -nk 2 -in scf.in > scf.out 2>&1")
print("  ⚠ k-mesh 를 바꾸면 **밀도가 달라진다** — ELF/CDD 는 정성 그림이라 무해하지만,")
print("     이 SCF 로 뽑은 수치를 k444 결과와 같은 표에 넣지 말 것.")
print(f"  로그: tail -f {elog}   ·   tail -f {blog}")
