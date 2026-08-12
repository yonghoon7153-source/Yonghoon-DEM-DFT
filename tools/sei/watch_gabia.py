#!/usr/bin/env python3
"""watch_gabia.py — gabia 전체 상황판 (SEI DFT + 갭 + SDCP + **NEB** + 디스크).

    watch -n 120 python3 tools/sei/watch_gabia.py
    python3 tools/sei/watch_gabia.py --selftest     # 서버 없이 파서 검증

왜 이 화면인가
  2026-08-06 서버가 재부팅되면서 tmux 세션과 돌던 계산이 전부 죽었다. 그럴 때 제일
  먼저 알아야 할 건 "무엇이 살아남았고 무엇을 다시 걸어야 하나" 다. 그래서 진행률보다
  **단계별 완료 매트릭스**를 먼저 띄운다 — 러너가 resume-safe 라 끝난 단계는 안 다시 돈다.

  ⚠ 갭은 03 단계(fixed-occ nscf)의 고유값이 정본이다. DOS 문턱 판독 금지.

이 도구가 **못 하는 것**
  · NEB 완주 시각을 예측하지 못한다 — 총 경로 스텝 수를 미리 알 수 없다.
    대신 "오차 → 문턱" 과 "마지막 갱신" 으로 살아 있는지/줄고 있는지만 본다.
  · 장벽을 인용하지 못한다. 수치 정본은 collect_neb.py 다 (게이트·전하 규약 포함).
  · 원격에서 돌지 않는다 — gabia 안에서 실행하는 화면이다.
"""
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime

#: SEI DFT 작업 루트 — **여러 개**. frozen-4f 재계산은 별도 폴더라
#:  한 곳만 보면 "미착수" 로 보인다 (2026-08-12 실제로 그랬다: LiNdO₂·Nd₂S₃ 는
#:  이미 6단계 완주였는데 화면은 vc-rlx 만 ✓ 로 찍고 있었다).
SEI = os.environ.get("SEI",
                     "/data/work/runs/sei_dft:/data/work/runs/sei_dft_frozen4f")
SDCP_VASP = "/data/work/runs/sdcp_v2/phaseB_vasp"
#: NEB 작업 루트 — **여러 개**를 콜론/쉼표로 준다. 같은 상(li3nd)이 경로마다
#:  다른 홉을 뜻할 수 있어(b→c vs c→c) 루트를 갈라 보여 준다.
NEBW = os.environ.get("NEBW",
                      "/data/work/runs/sei_neb_v2:/data/work/runs/sei_neb_v2_ccpath")


def split_roots(spec):
    """콜론/쉼표 목록 → 존재하는 디렉터리만. 없는 경로는 조용히 버리지 않고 돌려준다."""
    out, missing = [], []
    for x in re.split(r"[:,]", spec or ""):
        x = x.strip()
        if not x:
            continue
        (out if os.path.isdir(x) else missing).append(x)
    return out, missing


def root_label(d):
    """루트 짧은 이름 — sei_neb_v2 → v2 · sei_neb_v2_ccpath → v2_ccpath."""
    b = os.path.basename(d.rstrip("/"))
    return b[len("sei_neb_"):] if b.startswith("sei_neb_") else b


def run_note(d):
    """작업 폴더의 _NOTE.txt — 이미 판정된 건에 대해 낡은 조언을 반복하지 않기 위해.

    ⚠ 판정 자체는 kb 에 있다. 여기 두는 건 **이 실행 폴더가 무엇인지** 한 줄이다
      (환경 상태). 파일이 없으면 아무것도 안 한다.
    """
    p = os.path.join(d, "_NOTE.txt")
    try:
        return open(p, encoding="utf-8").read().strip().splitlines()[0][:88]
    except (OSError, IndexError):
        return None
STAGES = [("01_vcrelax", "vc-rlx"), ("02_scf", "scf"), ("03_nscf_gap", "gap"),
          ("04_nscf_dos", "dos-k"), ("05_dos", "dos"), ("06_projwfc", "pdos")]
BAR = "─" * 76
RY_EV = 13.605693122994
#: 대칭 동등 끝점이 이보다 벌어지면 둘 중 하나가 미수렴이다 (실측: 미수렴 시 57 meV).
#: etot_conv_thr 1e-4 Ry(=1.4 meV)·forc 여유를 감안한 값.
EP_TOL_MEV = 5.0
#: 비대칭 상이라도 두 Li 자리 차가 이보다 크면 이완 미완/끝점 구성 오류를 먼저 의심한다.
EP_BIG_MEV = 500.0
_ACT = re.compile(r"activation energy\s*\((->|<-)\)\s*=\s*(-?[\d.]+)\s*eV")
_IMGROW = re.compile(r"^\s*\d+\s+(-?[\d.]+)\s+(-?[\d.]+)\s+([TF])\s*$", re.M)
_TOTEN = re.compile(r"^!\s+total energy\s+=\s+(-?[\d.]+)\s+Ry", re.M)


def sh(c):
    try:
        return subprocess.run(c, shell=True, capture_output=True, text=True,
                              timeout=10).stdout
    except Exception:
        return ""


def done(d, stem):
    """단계 완료 판정. pw.x/dos.x/projwfc.x 다 'JOB DONE' 을 찍는다."""
    o = os.path.join(d, stem + ".out")
    if not os.path.isfile(o):
        return " "
    try:
        tx = open(o, errors="ignore").read()
    except OSError:
        return "?"
    if "JOB DONE" in tx:
        return "✓"
    if "Error in routine" in tx or "%%%%" in tx or "MPI_ABORT" in tx:
        return "✗"
    return "▸"          # 시작은 했는데 안 끝났다 (재부팅으로 끊긴 것)


def relax_end(p):
    """pw.x relax 출력 → (에너지 eV, 상태문자). 상태: ✓수렴 ▸진행/절단 ✗오류 ·없음.

    ⚠ 마지막 '!  total energy' 만 읽으면 **이완이 안 끝난 잡도 값이 나온다** — 그 값으로
      끝점 차를 재면 장벽이 아니라 미수렴을 재게 된다(2026-08-12 li3nd 2.07 eV 사례).
      그래서 'End of BFGS Geometry Optimization' + 'JOB DONE' 을 같이 본다.
    """
    try:
        t = open(p, errors="ignore").read()
    except OSError:
        return None, "·"
    if re.search(r"Error in routine|%%%%|MPI_ABORT", t):
        return None, "✗"
    v = _TOTEN.findall(t)
    e = float(v[-1]) * RY_EV if v else None
    done = "End of BFGS Geometry Optimization" in t and "JOB DONE" in t
    return e, ("✓" if done else ("▸" if e is not None else "·"))


def read_gap(path):
    """gap.json 하나 → (레코드, None) 또는 (None, 손상 사유).

    ⚠ 2026-08-11 실측 — gap 이 **문자열**인 파일 하나가 정렬 키에서 TypeError 를 내
      상황판 전체를 죽였다(③④ 가 아예 안 나옴). 감시 화면은 나쁜 데이터 한 줄에
      죽으면 안 된다. 그렇다고 조용히 버리지도 않는다 — 손상은 손상이라고 띄운다.
    """
    tag = os.path.basename(os.path.dirname(path))
    try:
        d = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"읽기 실패: {type(e).__name__}"
    if not isinstance(d, dict):
        return None, f"dict 가 아님: {type(d).__name__}"
    # ⚠ NOT_APPLICABLE 은 손상이 아니라 **판정**이다 — 4f 를 원자가에 둔 PP 로는
    #   SCF 해가 금속이라 fixed-occ 갭이라는 양이 성립하지 않는다 (Nd 계열).
    #   손상으로 찍고 "nscf 를 다시 돌려라" 고 하면 틀린 조언이다.
    #   ⚠⚠ 2026-08-12 재발 — `gap` 만 봤는데 실제 파일은 `gap: null` 이고 판정은
    #     `verdict`/`electronic_class` 에 있다. 필드를 잘못 봐서 다시 "손상" 으로 찍혔다.
    _v = {str(d.get(k) or "").upper() for k in ("gap", "verdict", "electronic_class")}
    if _v & {"NOT_APPLICABLE", "N/A", "NA", "METAL"}:
        return None, ("금속 해 — 갭 미정의 (**손상 아님**). 재계산 불필요. "
                      + str(d.get("reason") or "")[:60])
    try:
        for k in ("vbm", "cbm", "gap"):
            d[k] = float(d[k])
    except (KeyError, TypeError, ValueError):
        return None, f"수치 필드 손상: gap={d.get('gap')!r}"
    d.setdefault("tag", tag)
    return d, None


def _neb_rows(ss):
    """NEB 표의 행들을 찍는다. 루트마다 호출한다 (같은 상이 루트별로 다른 홉이다)."""
    for s in ss:
        # 대칭 동등이면 Δ끝점이 0 이어야 한다 / 비대칭이면 두 자리 에너지 차라 정상
        if s["ep_dE_meV"] is None:
            dep = "—"
        elif s["eqv"] is True:
            dep = f"{s['ep_dE_meV']:+.0f}mV{'✓' if abs(s['ep_dE_meV']) <= EP_TOL_MEV else '⛔'}"
        else:
            dep = f"{s['ep_dE_meV']:+.0f}mV·"          # · = 비대칭이라 검사 안 함
        err = f"{s['err']:.3f}→{s['thr'] or 0.05:.2f}" if s["err"] is not None else "—"
        it = (f"{s['state']}it{s['it']}" if s["it"]
              else {"◦": "◦SCF", "✗": "✗", " ": "—"}.get(s["state"], s["state"]))
        ea = f"{s['ea']:.3f}" if s["ea"] is not None else "—"
        age = f"{s['age_min']:.0f}분" if s["age_min"] is not None else "—"
        print(f"   {s['tag']:11s}{s['ep_mark']:>5s} {dep:>11s}  "
              f"{it:>5s} {err:>13s} {ea:>9s} {age:>7s}")


def neb_status(d):
    """상(phase) 폴더 하나의 NEB 상태. 화면과 selftest 가 같은 함수를 쓴다.

    끝점 축퇴 검사가 이 함수의 핵심이다 — **대칭 동등**(meta.json 의
    endpoints_symmetry_equivalent)인데 두 끝점 에너지가 벌어지면 장벽이 아니라
    미수렴을 보고 있는 것이다. 비대칭 상에서는 벌어지는 게 정상이라 검사하지 않는다.
    """
    r = {"tag": os.path.basename(d), "state": " ", "it": None, "err": None,
         "thr": None, "ea": None, "ep_mark": "  ", "ep_dE_meV": None,
         "eqv": None, "age_min": None, "alerts": []}
    meta = {}
    mp = os.path.join(d, "meta.json")
    if os.path.isfile(mp):
        try:
            meta = json.load(open(mp, encoding="utf-8"))
        except (OSError, ValueError):
            r["alerts"].append(f"{r['tag']}: meta.json 손상 — 대칭 게이트를 못 켠다")
    r["eqv"] = meta.get("endpoints_symmetry_equivalent")
    r["thr"] = meta.get("path_thr")

    # ── 끝점 ──
    ei, mi = relax_end(os.path.join(d, "ep_initial", "relax.out"))
    ef, mf = relax_end(os.path.join(d, "ep_final", "relax.out"))
    r["ep_mark"] = mi + mf
    if "▸" in r["ep_mark"]:
        r["alerts"].append(f"{r['tag']}: 끝점 이완이 **안 끝났다**(BFGS 미완/JOB DONE 없음) — "
                           f"마지막 에너지는 수렴값이 아니다. Δ끝점을 믿지 말 것")
    if "✗" in r["ep_mark"]:
        r["alerts"].append(f"{r['tag']}: 끝점 relax.out 에 오류")
    if ei is not None and ef is not None:
        r["ep_dE_meV"] = (ef - ei) * 1000.0
        ad = abs(r["ep_dE_meV"])
        if r["eqv"] is True and ad > EP_TOL_MEV:
            r["alerts"].append(
                f"{r['tag']}: 끝점이 **대칭 동등**인데 {r['ep_dE_meV']:+.0f} meV 벌어졌다 "
                f"(>{EP_TOL_MEV:.0f}) — 한쪽이 미수렴이다. NEB 장벽을 인용하지 말 것")
        # 비대칭이라도 크기는 본다 — 두 Li 자리의 에너지 차가 이 정도로 벌어지는 일은
        # 드물다. 보통은 이완 미완이거나 끝점 구성이 잘못된 것이다 (판정이 아니라 확인 요청).
        elif r["eqv"] is not True and ad > EP_BIG_MEV:
            r["alerts"].append(
                f"{r['tag']}: 비대칭이라 끝점 차는 정상이지만 {r['ep_dE_meV']:+.0f} meV 는 "
                f"두 Li 자리 차로는 크다 (>{EP_BIG_MEV:.0f}) — 이완 완료·자리 배정을 확인할 것")

    # ── 경로 ──
    out = os.path.join(d, "neb.out")
    if not os.path.isfile(out):
        return r
    try:
        t = open(out, errors="ignore").read()
    except OSError:
        return r
    r["age_min"] = (datetime.now().timestamp() - os.path.getmtime(out)) / 60.0
    if re.search(r"unable to launch|could not access or execute|command not found", t):
        r["state"] = "✗"
        r["alerts"].append(f"{r['tag']}: neb.x 실행 자체가 실패했다 — 안 돌고 있다")
        return r
    if re.search(r"Error in routine|%%%%|MPI_ABORT", t):
        r["state"] = "✗"
        r["alerts"].append(f"{r['tag']}: neb.out 에 오류 — tail 을 볼 것")
        return r
    fwd = [float(v) for k, v in _ACT.findall(t) if k == "->"]
    r["it"] = len(fwd)
    r["ea"] = fwd[-1] if fwd else None
    k = t.rfind("error (eV/A)")
    if k > 0:
        rows = _IMGROW.findall(t[k:])
        free = [float(e) for _en, e, fz in rows if fz == "F"] or \
               [float(e) for _en, e, _fz in rows]
        r["err"] = max(free) if free else None
    if "neb: convergence achieved" in t:
        r["state"] = "✓"
    else:
        # ◦ = 돌기 시작했는데 첫 경로 스텝이 아직 안 나왔다 (이미지 7개 SCF 중).
        #   미착수(공백)와 구분해야 한다 — 안 그러면 "안 걸렸나?" 하고 또 건다.
        r["state"] = "▸" if fwd else "◦"
        if r["age_min"] is not None and r["age_min"] > 30:
            r["alerts"].append(f"{r['tag']}: neb.out 이 {r['age_min']:.0f}분째 조용하다 "
                               f"— 프로세스가 살아 있는지 확인할 것")
    return r


def selftest():
    """양성 + **음성** 경로. 음성이 없으면 통과해도 아무것도 보증 못 한다."""
    import shutil
    import tempfile
    td = tempfile.mkdtemp(prefix="watch_gabia_st_")
    ok = True

    def mk(tag, eqv, e_ini, e_fin, neb_body=None, thr=0.05, converged=True):
        d = os.path.join(td, tag)
        tail = ("     End of BFGS Geometry Optimization\n   JOB DONE.\n"
                if converged else "")           # 없으면 = 이완이 아직 안 끝난 출력
        for ep, e in (("ep_initial", e_ini), ("ep_final", e_fin)):
            os.makedirs(os.path.join(d, ep), exist_ok=True)
            if e is not None:
                open(os.path.join(d, ep, "relax.out"), "w").write(
                    f"!    total energy              =    {e / RY_EV:.8f} Ry\n" + tail)
        json.dump({"endpoints_symmetry_equivalent": eqv, "path_thr": thr},
                  open(os.path.join(d, "meta.json"), "w"))
        if neb_body is not None:
            open(os.path.join(d, "neb.out"), "w").write(neb_body)
        return d

    def chk(cond, msg):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + msg)
        ok &= bool(cond)

    body = ("     activation energy (->) =   0.286745 eV\n"
            "     activation energy (<-) =   0.286712 eV\n"
            "     image        energy (eV)        error (eV/A)        frozen\n\n"
            "         1     -1234.567890            0.001000            T\n"
            "         2     -1234.500000            0.083000            F\n")
    # 양성 ①: 대칭 동등 + 끝점 일치 + 진행 중
    s = neb_status(mk("li2s", True, -100.0, -100.001, body))
    chk(s["state"] == "▸" and s["it"] == 1 and abs(s["err"] - 0.083) < 1e-9
        and not s["alerts"], f"대칭 동등·끝점 1 meV·진행중 → 경고 없음 ({s['alerts']})")
    # 양성 ②: 수렴
    s = neb_status(mk("li2o", True, -100.0, -100.0,
                      body + "     neb: convergence achieved in 12 iterations\n"))
    chk(s["state"] == "✓", "수렴 문자열 → ✓")
    # 음성 ①: 대칭 동등인데 끝점 57 meV — 미수렴 (2026-08 실측 사고)
    s = neb_status(mk("li2s_bad", True, -100.0, -100.057, body))
    chk(any("대칭 동등" in x for x in s["alerts"]),
        f"대칭 동등 + 끝점 57 meV → 경고 ({s['ep_dE_meV']:+.0f} meV)")
    # 음성 ②: **비대칭**은 끝점이 벌어져도 정상 — 잘못된 경고를 내면 안 된다
    s = neb_status(mk("li3nd", False, -100.0, -100.412, body))
    chk(not s["alerts"], f"비대칭 + 끝점 412 meV → 경고 없음 (정상) ({s['alerts']})")
    # 음성 ③: 실행 실패를 미수렴과 구분
    s = neb_status(mk("li3p", False, None, None,
                      "mpirun was unable to launch the specified application\n"))
    chk(s["state"] == "✗" and any("실행 자체가 실패" in x for x in s["alerts"]),
        "mpirun 실패 → ✗ (미수렴 아님)")
    # 음성 ④: 끝점만 있고 neb 미착수 — 경고 없이 공백
    s = neb_status(mk("licl", True, -100.0, -100.0, None))
    chk(s["state"] == " " and s["it"] is None and not s["alerts"],
        "neb.out 없음 → 미착수(공백) · 오경고 없음")
    # 음성 ⑤-a: 끝점 이완이 안 끝났는데 마지막 에너지가 있다 (li3nd 2026-08-12 사례)
    s = neb_status(mk("li3nd_trunc", False, -100.0, -102.072, body, converged=False))
    chk(s["ep_mark"] == "▸▸" and any("안 끝났다" in x for x in s["alerts"]),
        f"BFGS 미완 → ▸ + 경고 (mark={s['ep_mark']})")
    # 음성 ⑤-b: 이완은 끝났지만 비대칭 차가 2.07 eV — 크기 자체를 확인하라고 해야 한다
    s = neb_status(mk("li3nd_big", False, -100.0, -102.072, body))
    chk(any("두 Li 자리 차로는 크다" in x for x in s["alerts"]),
        f"비대칭 2072 meV → 확인 요청 ({s['ep_dE_meV']:+.0f} meV)")
    # 양성: 비대칭 412 meV 는 문턱 아래라 조용해야 한다 (위 음성 ④ 와 짝)
    s = neb_status(mk("li3nd_ok", False, -100.0, -100.412, body))
    chk(not s["alerts"], f"비대칭 412 meV → 여전히 조용 ({s['alerts']})")
    # 상태 ◦: neb.out 은 있는데 첫 경로 스텝 전 — 미착수와 구분해야 한다
    s = neb_status(mk("li2s_scf", True, -100.0, -100.0, "     Self-consistent Calculation\n"))
    chk(s["state"] == "◦" and not s["it"], f"neb 시작·에너지 전 → ◦ (state={s['state']!r})")
    # 음성 ⑤: meta.json 손상 → 대칭 게이트를 켤 수 없다고 말해야 한다
    d = mk("li3po4g", True, -100.0, -100.5, body)
    open(os.path.join(d, "meta.json"), "w").write("{oops")
    s = neb_status(d)
    chk(any("meta.json 손상" in x for x in s["alerts"]) and s["eqv"] is None,
        "meta.json 손상 → 경고 + 대칭 판정 보류")

    # ── gap.json 파서 (2026-08-11 상황판 전체를 죽인 그 입력) ──
    def gj(tag, body):
        p = os.path.join(td, tag)
        os.makedirs(p, exist_ok=True)
        open(os.path.join(p, "gap.json"), "w").write(body)
        return os.path.join(p, "gap.json")

    r, why = read_gap(gj("ok", '{"tag":"li2s","vbm":1.0,"cbm":4.4,"gap":3.4,'
                               '"verdict":"절연체"}'))
    chk(r is not None and abs(r["gap"] - 3.4) < 1e-9, "정상 gap.json → 레코드")
    # 음성 ⑥: gap 이 문자열 — 실측 크래시 재현. 정렬 가능한 float 이거나 손상이거나 둘 중 하나
    r, why = read_gap(gj("strgap", '{"tag":"x","vbm":"?","cbm":"?","gap":"oops"}'))
    chk(r is None and "손상" in why, f"gap 이 문자열 → 손상 처리 ({why})")
    # ★ NOT_APPLICABLE 은 판정이지 손상이 아니다 — 재실행 조언을 하면 안 된다
    r, why = read_gap(gj("na", '{"tag":"nd2o3","gap":"NOT_APPLICABLE"}'))
    chk(r is None and "금속 해" in why and "수치 필드 손상" not in why,
        f"NOT_APPLICABLE → 금속 해 판정 (재실행 조언 아님)")
    # 음성 ⑦: 깨진 JSON / 필드 누락 / 리스트
    chk(read_gap(gj("brk", "{oops"))[0] is None, "깨진 JSON → 손상 처리")
    chk(read_gap(gj("nofield", '{"tag":"x"}'))[0] is None, "필드 누락 → 손상 처리")
    chk(read_gap(gj("lst", "[1,2,3]"))[0] is None, "dict 아님 → 손상 처리")
    # 정렬이 실제로 되는지 (크래시 지점 재현)
    recs = [read_gap(gj("a", '{"vbm":0,"cbm":5,"gap":5.0}'))[0],
            read_gap(gj("b", '{"vbm":0,"cbm":3,"gap":3.0}'))[0]]
    try:
        srt = [x["tag"] for x in sorted(recs, key=lambda x: -x["gap"])]
        chk(srt == ["a", "b"], f"정렬 통과 (내림차순 {srt})")
    except TypeError as e:
        chk(False, f"정렬에서 TypeError — 실측 크래시 재발: {e}")
    # ── 다중 NEB 루트 (2026-08-12) ─────────────────────────────────────────
    #   같은 상 이름이 루트마다 **다른 홉**이다 (sei_neb_v2 = b→c ·
    #   sei_neb_v2_ccpath = c→c). 한 표에 섞으면 어느 쪽 숫자인지 알 수 없다.
    r1 = os.path.join(td, "nebA"); r2 = os.path.join(td, "nebB")
    os.makedirs(os.path.join(r1, "li3nd")); os.makedirs(os.path.join(r2, "li3nd"))
    got, miss = split_roots(f"{r1}:{r2}")
    chk(got == [r1, r2] and not miss, f"콜론 목록 → 루트 2개 ({len(got)})")
    got2, miss2 = split_roots(f"{r1}, {r2}")
    chk(got2 == [r1, r2], "쉼표+공백 목록도 받는다")
    # ★ 음성: 없는 경로를 **조용히 버리지 않는다** (오타를 눈치채야 한다)
    got3, miss3 = split_roots(f"{r1}:/nope/xyz")
    chk(got3 == [r1] and miss3 == ["/nope/xyz"],
        f"없는 루트는 missing 으로 돌려준다 ({miss3})")
    chk(split_roots("")[0] == [] and split_roots(":  :")[0] == [],
        "빈 목록/구분자만 → 빈 결과 (예외 아님)")
    chk(root_label("/a/b/sei_neb_v2_ccpath") == "v2_ccpath"
        and root_label("/a/b/other") == "other", "루트 짧은 이름")
    # ★ 음성: 두 루트의 같은 상이 **섞이지 않는지** — 태그가 아니라 루트로 갈린다
    lbl = [root_label(x) for x in got]
    chk(len(set(lbl)) == 2, f"같은 상이 있어도 루트 라벨로 구분된다 ({lbl})")
    chk(run_note(r1) is None, "_NOTE.txt 없으면 아무것도 안 한다")
    open(os.path.join(r1, "_NOTE.txt"), "w").write("c→c 진짜 경로\n둘째 줄은 무시\n")
    chk(run_note(r1) == "c→c 진짜 경로", f"_NOTE.txt 첫 줄만 ({run_note(r1)})")
    # ── 금속 판정 (2026-08-12 **재발** — 필드를 잘못 봐서 두 번 났다) ──────────
    #   실제 파일은 gap: null 이고 판정은 verdict/electronic_class 에 있다.
    #   "손상" 으로 찍고 nscf 재계산을 시키면 틀린 조언이다.
    d0, e0 = read_gap(gj("li3nd", json.dumps(
        {"gap": None, "verdict": "NOT_APPLICABLE", "electronic_class": "metal",
         "reason": "electronic_class=metal — 금속엔 VBM/CBM 이 없다"})))
    chk(d0 is None and e0 and "손상 아님" in e0 and "재계산 불필요" in e0,
        f"gap:null + verdict:NOT_APPLICABLE → 금속 판정 ({str(e0)[:40]})")
    d1, e1 = read_gap(gj("m2", json.dumps({"gap": "NOT_APPLICABLE"})))
    chk(d1 is None and e1 and "손상 아님" in e1, "gap 필드에 직접 와도 잡는다")
    # ★ 음성: 진짜 손상은 여전히 손상이어야 한다 (금속으로 봐주면 안 된다)
    d2, e2 = read_gap(gj("broke", json.dumps({"gap": "abc", "vbm": 1, "cbm": 2})))
    chk(d2 is None and e2 and "손상" in e2 and "아님" not in e2,
        f"파싱 불가 값은 여전히 **손상** ({str(e2)[:36]})")
    shutil.rmtree(td, ignore_errors=True)
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if "--selftest" in sys.argv:
    sys.exit(selftest())

print("=" * 76)
gpu = sh("nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total "
         "--format=csv,noheader,nounits").strip()
tmux = [t.split(":")[0] for t in sh("tmux ls").splitlines() if t.strip()]
# ⚠ 대괄호 트릭 — 그냥 'pw.x' 로 쓰면 pgrep 을 띄운 sh 자신이 잡혀 **항상 ≥1** 이 된다.
#   그러면 "0 이면 죽은 것" 판정이 영원히 안 걸린다 (2026-08-11 스모크 테스트에서 발견).
pw = len([x for x in sh(r"pgrep -f '[p]w\.x|[d]os\.x|[p]rojwfc\.x'").split() if x])
up = sh("uptime -p").strip() or sh("uptime").strip()
print(f"gabia · {datetime.now():%m-%d %H:%M} · GPU {gpu or '?'} · "
      f"QE 프로세스 {pw} · tmux {' '.join(tmux) or '없음'}")
print(f"가동 {up}")
print(BAR)

# ── 1) SEI DFT 단계 매트릭스 ────────────────────────────────────────────────
sei_roots, sei_missing = split_roots(SEI)
for m in sei_missing:
    print(f"① ⚠ SEI 루트 없음: {m}")
# (루트, 태그) 목록 — 같은 태그가 여러 루트에 있으면 **둘 다** 보여 준다.
#   덮어쓰면 어느 폴더의 결과인지 모르게 되고, 오늘 그것 때문에 완주한 계산을
#   미착수로 읽었다.
pairs = [(r, os.path.basename(x)) for r in sei_roots
         for x in sorted(glob.glob(os.path.join(r, "*"))) if os.path.isdir(x)]
tags = [t for _r, t in pairs]
multi = len(sei_roots) > 1
if not pairs:
    print(f"⛔ {sei_roots or SEI} 에 작업 폴더가 없다 — build_dft_inputs.py 부터.")
else:
    print(f"① SEI DFT — {len(pairs)}종 × 6단계   (✓ 완료 · ▸ 중단 · ✗ 오류 · 공백 미착수)")
    print("   " + " " * 26 + "  ".join(f"{s:>6s}" for _, s in STAGES))
    # ⚠ 화면은 **감시용**이다. 완주하고 건강한 것은 한 줄로 접고, 손볼 게 있는 것만
    #   펼친다 (2026-08-12: 13종 × 6단계를 다 찍으니 ④ NEB 가 화면 밖으로 밀렸다).
    ndone = 0
    _cur = None
    _folded = {}
    for _root, t in pairs:
        if multi and _root != _cur:
            if _cur is not None and _folded.get(_cur):
                print(f"     ✓ 완주 {len(_folded[_cur])}: "
                      + " · ".join(_folded[_cur]))
            _cur = _root
            _n = run_note(_root)
            print(f"   ┌ {root_label(_root)}" + (f"  — {_n}" if _n else ""))
        d = os.path.join(_root, t)
        marks = [done(d, stem) for stem, _ in STAGES]
        gj = os.path.join(d, "gap.json")
        g = ""
        if os.path.isfile(gj):
            try:
                j = json.load(open(gj))
                g = f"  gap {j['gap']:6.3f} eV  {j['verdict']}"
            except Exception:
                g = "  (gap.json 손상)"
        if all(m == "✓" for m in marks) and os.path.isfile(gj):
            ndone += 1
        print(f"   {t:26s}" + "  ".join(f"{m:>6s}" for m in marks) + g)
    print(f"\n   완주 {ndone}/{len(tags)}")

    # 끊긴 것 = 재부팅 피해. 러너가 resume-safe 라 그냥 다시 걸면 된다.
    broken = [t for r, t in pairs
              if any(done(os.path.join(r, t), s) == "▸" for s, _ in STAGES)]
    if broken and pw == 0:
        print(f"\n   ⚠ 중단된 조성 {len(broken)}개: {', '.join(broken)}")
        print("     러너는 resume-safe 다 — 끝난 단계는 건너뛰므로 그냥 다시 걸면 된다:")
        print("       tmux new -s seidft -d \"bash tools/sei/run_sei_dft.sh 2>&1 "
              "| tee -a ~/logs/sei_dft.log\"")

    # ★ 실행 바이너리 — kb 에 "미설치" 라고 적어 두고 낡은 사례가 있다
    #   (neb.x: 2026-06-01 "미설치" → 실제로는 있고 지금 돌고 있다. 그 기록이
    #    "UMA NEB 로 전체 대체" 라는 설계 결정의 근거였다.)
    # ⚠ 빌드가 **여러 개**다 (gpu/cpu). 하나만 보면 "ph.x 없음" 으로 또 속는다 —
    #   실제로 ph.x·epsilon.x·ld1.x 는 CPU 빌드에만 있다 (2026-08-12 실측).
    qb = sorted(glob.glob("/data/apps/qe-*/bin")) + sorted(glob.glob("/data/work/apps/qe-*/bin"))
    want = ("pw.x", "neb.x", "ph.x", "epsilon.x", "dos.x", "projwfc.x", "ld1.x")
    if qb:
        for b in qb:
            have = {os.path.basename(x) for x in glob.glob(os.path.join(b, "*"))}
            print(f"   QE {os.path.basename(os.path.dirname(b)):16s} "
                  + " ".join(f"{w}{'✓' if w in have else '✗'}" for w in want))
    else:
        print("   ⚠ QE 빌드 디렉터리를 못 찾았다 (/data/apps/qe-* · /data/work/apps/qe-*)")

    # ★ 환경 상태는 **기록해 두면 낡는다** — 화면에 상시 띄워야 5일 뒤에 안 속는다.
    #   (2026-08-12: kb 가 "frozen-4f 없음" 이라 5일간 막힌 줄 알았는데 이미 있었다.)
    nd = sorted(glob.glob("/data/work/pseudo/Nd*.[uU][pP][fF]"))
    if nd:
        for f in nd:
            z = None
            try:
                t = open(f, errors="ignore").read(400000)
                m = re.search(r'z_valence\s*=\s*"?\s*([\d.eE+-]+)', t, re.I)
                z = float(m.group(1)) if m else None
            except OSError:
                pass
            kind = ("frozen-4f ✓" if z and 10.0 <= z <= 12.5 else
                    "4f-in-valence ⛔ 갭 불가" if z and 13.0 <= z <= 16.0 else "?")
            print(f"   Nd PP  {os.path.basename(f):44s} z={z}  {kind}")

print(BAR)

# ── 2) 갭 결산 ─────────────────────────────────────────────────────────────
# ⚠ 2026-08-11 실측 — gap 이 **문자열**인 gap.json 하나가 정렬 키에서 TypeError 를 내
#   상황판 전체를 죽였다(③④ 가 아예 안 나옴). 감시 화면이 나쁜 데이터 한 줄에 죽으면
#   안 된다 — 숫자가 아닌 레코드는 **버리지 말고 '손상' 로 따로 세워** 보여 준다.
gaps, gaps_bad = [], []
_seen_gap = set()
for j in sorted((g for r in sei_roots
                 for g in glob.glob(os.path.join(r, "*", "gap.json"))),
                key=lambda x: ("frozen4f" not in x, x)):   # frozen4f 를 먼저 = 정본 우선
    _tag = os.path.basename(os.path.dirname(j))
    if _tag in _seen_gap:
        continue                       # 같은 상이 두 루트에 있으면 정본 하나만
    _seen_gap.add(_tag)
    rec, why = read_gap(j)
    (gaps if rec else gaps_bad).append(rec or (os.path.basename(os.path.dirname(j)), why))
if gaps or gaps_bad:
    print("② 갭 (fixed-occ nscf 고유값 — DOS 문턱 아님)")
    print(f"   {'상':26s} {'VBM':>8s} {'CBM':>8s} {'gap(eV)':>9s}  판정")
    # ⚠ 2026-08-12 — 태그에 Nd 가 있으면 무조건 "4f valence 진단용" 을 붙이고 있었다.
    #   PP 가 frozen-4f 로 바뀐 뒤에도 그대로 붙어 **멀쩡한 값을 진단용으로 깎았다**.
    #   화면이 낡은 주장을 재생산한 사례다 — 라벨은 **실제 PP 의 z_valence** 로 정한다.
    ndz = None
    for f in sorted(glob.glob("/data/work/pseudo/Nd*.[uU][pP][fF]")):
        try:
            m = re.search(r'z_valence\s*=\s*"?\s*([\d.eE+-]+)',
                          open(f, errors="ignore").read(400000), re.I)
            ndz = float(m.group(1)) if m else ndz
        except OSError:
            pass
    for d in sorted(gaps, key=lambda x: -x["gap"]):
        nd = "Nd" in str(d["tag"]) or "nd2" in str(d["tag"])
        if not nd:
            flag = ""
        elif ndz is None:
            flag = "  ⚠ Nd PP 를 못 읽었다 — 4f 취급 미상"
        elif 10.0 <= ndz <= 12.5:
            flag = "  · frozen-4f (z=%.0f)" % ndz
        else:
            flag = "  ⚠ 4f valence (z=%.0f) — 진단용" % ndz
        print(f"   {str(d['tag']):26s} {d['vbm']:8.3f} {d['cbm']:8.3f} "
              f"{d['gap']:9.3f}  {d.get('verdict', '?')}{flag}")
    for tag, why in gaps_bad:
        print(f"   {tag:26s} {'—':>8s} {'—':>8s} {'—':>9s}  ⛔ {why}")
    if gaps:
        print("   ⚠ PBE 갭은 넓은 갭 절연체에서 30–50% 과소 — 실험값과 나란히 놓지 말 것")
    if any("손상" in w for _t, w in gaps_bad):
        print("   ⛔ 손상된 gap.json 은 03 단계(nscf)를 다시 돌려야 한다 — extract_gap.py 재실행")
    if any("금속 해" in w for _t, w in gaps_bad):
        print("   🟡 금속 해는 재실행으로 안 풀린다 — PP 문제다 (kb/open_items.md §O)")
else:
    print("② 갭 — 아직 gap.json 이 없다")

print(BAR)

# ── 3) SDCP 외주 번들 (**가장 최근 것**) ────────────────────────────────────
#   ⚠ 옛 판은 2026-08-08 납품 zip 하나를 고정으로 가리켰다. 새 번들을 만들어도
#     화면은 계속 옛것을 "준비됨" 이라 찍었다 (2026-08-12 정정).
_bd = sorted(glob.glob(os.path.expanduser("~/Yonghoon-DEM-DFT/bundles/*/MANIFEST.json")),
             key=os.path.getmtime, reverse=True)
if _bd:
    _m = _bd[0]
    try:
        _mm = json.load(open(_m, encoding="utf-8"))
        _sub = _mm.get("submission") or {}
        _z = os.path.dirname(_m) + ".zip"
        print(f"③ SDCP 외주 번들 — {os.path.basename(os.path.dirname(_m))}  "
              f"잡 {_mm.get('n_jobs','?')} · static {_sub.get('n_static','?')} + "
              f"dense {_sub.get('n_dense_mandatory','?')}"
              + (f" · zip {os.path.getsize(_z)//1024} KB" if os.path.isfile(_z) else ""))
        print(f"   범위: {str(_mm.get('claim_scope',''))[:88]}")
    except (OSError, ValueError) as e:
        print(f"③ SDCP 외주 번들 — MANIFEST 읽기 실패 ({type(e).__name__})")
elif os.path.isfile(SDCP_VASP + ".zip"):
    print(f"③ SDCP 외주 번들 — 새 번들 없음. 옛 납품 zip 만 있다 ({SDCP_VASP}.zip)")
else:
    print("③ SDCP 외주 번들 — 없음 (tools/sdcp/vasp_handoff_bundle.py 로 생성)")

print(BAR)

# ── 4) SEI NEB ─────────────────────────────────────────────────────────────
roots, missing_roots = split_roots(NEBW)
neb_pid = len([x for x in sh(r"pgrep -f '[n]eb\.x'").split() if x])
by_root = [(d, [neb_status(x) for x in sorted(glob.glob(os.path.join(d, "*")))
                if os.path.isdir(x)]) for d in roots]
nebs = [s for _d, ss in by_root for s in ss]
for m in missing_roots:
    print(f"④ ⚠ NEB 루트 없음: {m}")
if not nebs:
    print(f"④ SEI NEB — {roots or NEBW} 에 상 폴더가 없다 (build_neb_inputs.py 부터)")
else:
    print(f"④ SEI NEB — 루트 {len(by_root)}개 · neb.x 프로세스 {neb_pid}"
          f"   (✓수렴 ▸진행 ◦SCF중 ✗오류 공백 미착수)")
    print(f"   {'상':11s}{'끝점':>5s} {'Δ끝점':>11s}  {'경로':>5s} {'오차→문턱':>13s}"
          f" {'Ea→(eV)':>9s} {'갱신':>7s}")
    for _d, _ss in by_root:
        note = run_note(_d)
        print(f"   ┌ {root_label(_d)}"
              + (f"  — {note}" if note else "")
              + ("" if _ss else "   (상 폴더 없음)"))
        _neb_rows(_ss)
    alerts = [a for s in nebs for a in s["alerts"]]
    if alerts:
        print()
        for a in alerts:
            print(f"   ⚠ {a}")
    if neb_pid == 0 and any(s["state"] == "▸" for s in nebs):
        print("   ⚠ ▸(진행중) 인데 neb.x 프로세스가 0 — 죽었다. tmux 세션을 확인할 것")

# ── 5) 디스크 ──────────────────────────────────────────────────────────────
df = sh("df -h /data | tail -1").split()
if len(df) >= 5:
    print(f"\n디스크 /data  {df[2]} 사용 / {df[1]}  (여유 {df[3]}, {df[4]})")
print(BAR)
