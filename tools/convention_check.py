#!/usr/bin/env python3
"""물리 규약 회귀 가드 — 같은 규약이 여러 파일에 복사돼 있어도 갈라지지 않게 한다.

배경: tools/ 에 MSD 구현 8개·아레니우스 적합 6개가 흩어져 있다 (2026-08-11 실측).
2026-08-11 기준으로는 **갈라지지 않았다** — 이 도구는 그 상태를 유지시키는
회귀 가드지, 지금 있는 문제를 고치는 도구가 아니다. 그래서 얇게 만든다.

검사 대상은 **틀리면 논문 숫자가 바뀌는 것** 둘 + 무해한 것 하나(경고):
  ① D 추출 = 자유절편 (MSD = c + 6Dt). 원점강제(msd/(6t))는 D 가 케이지 절편에
     오염된다 — 2026-08-11 β 게이트 사태의 뿌리.
  ② MSD 창 = 2–50 ps (CLAUDE.md 정본). 창이 다르면 Ea 가 242 meV 까지 움직인다.
     **변수 대입뿐 아니라 argparse 기본값도 본다** (⑥ — 2026-09-08 추가).
  ③ (경고) kB 자릿수 — 상대차 1e-7 이라 무해. 통일만 권고.

의도적으로 **검사하지 않는 것**: 아레니우스 온도 집합. 타당한 변이(타당성 스캔
300–1000 K, 6점 진단, 3점 정본)가 많아 경고가 소음이 된다.

사용:
  python3 tools/convention_check.py              # 물리 규약
  python3 tools/convention_check.py --selftests  # 전 도구 selftest 스윕 (죽은 시험 탐지)

이 도구가 **못 하는 것**: 정규식 기반이라 AST 수준 우회를 못 본다 —
변수를 경유한 계산(`den = 6*t; D = msd/den`), 다른 모듈에서 import 한 창 상수,
동적으로 만든 창은 안 잡힌다. 통과가 곧 정합성 보증은 아니다.
argparse 검사(⑥)도 **리터럴 2-튜플만** 본다: `default=list(CAMPAIGN_WIN)` 처럼
상수를 경유하거나 `default=[-8.0, 5.0]` 처럼 음수인 창은 안 본다(후자는 DOS eV 창
같은 다른 물리량이라 일부러 뺀 것이다). **셸 러너가 넘기는 인자는 전혀 안 본다** —
`run_*.sh` 가 `--fit_window_ps` 를 빼먹었는지는 여기서 안 잡힌다(사람이 봐야 한다).

쓰기:
  python3 tools/convention_check.py            # 검사 (exit 1 = 위반)
  python3 tools/convention_check.py --selftest # 자체 시험 (음성 경로 포함)
"""
import re
import re as _re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
KB_CANON = "8.617333262e-5"

#: 원점강제 D 추출 — 규약 위반
FORCED_D = re.compile(r"(?:msd|MSD)[^\n=]{0,20}/\s*\(?\s*6(?:\.0)?\s*\*", re.I)
#: 자유절편 적합 (있으면 정상)
FREE_FIT = re.compile(r"polyfit\([^)]*,\s*1\s*\)")
#: MSD 창 — 이름에 window 가 든 **변수 대입**만 본다.
#  (본문 아무 데나 있는 2-튜플을 잡으면 set_xlim(1.3, 2.1) 같은 게 걸려 오탐이 된다)
WINDOW_ASSIGN = re.compile(r"^\s*(\w*[Ww][Ii][Nn][Dd][Oo][Ww]\w*)\s*(?::[^=]+)?=\s*(.+)$")
#: 창 이름이 **단위를 스스로 밝히면** MSD 시간창(ps) 규약과 무관하다.
#:   실물: `tools/xrd/phase_fingerprint.py` 의 `window_2theta=(8.0, 11.0)` 은 도(°)다.
#:   이런 오탐을 EXEMPT 로 덮으면 그 파일의 **진짜** 위반까지 같이 눈이 먼다 —
#:   그래서 파일을 면제하지 않고 판정을 고친다. (2026-09-06)
WINDOW_NON_TIME = re.compile(
    r"(?i)_(2theta|theta|deg|degrees?|ang|angstrom|nm|ev|kev|cm|wavenumber|q|k|bin|px)$")
TUPLE2 = re.compile(r"\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)")
KB_HIT = re.compile(r"8\.617[0-9]*e-0?5")
CANON_WINDOW = (2.0, 50.0)

#: ⑥ argparse **기본값** 창 (2026-09-08 추가)
#:   ⛔ 왜 따로 보나: ② 의 WINDOW_ASSIGN 은 **변수 대입**만 본다. 그런데 실제로 새고
#:     있던 자리는 생산 MD 드라이버의 **argparse 기본값**이었다 — 러너가 `--fit_window_ps`
#:     를 안 적으면 그 기본값이 그대로 논문 숫자가 된다. 이 검사기가 "0 위반" 을 찍는
#:     동안 `disorder_ensemble_diffusion.py` 는 5–40, `aimd_mlip.py` 는 2–20 으로 돌았다.
#:     **통과했다는 것과 안 봤다는 것은 다르다** — 이 항목이 그 차이를 메운다.
#:   ⚠ 음수 창은 일부러 안 본다 (`--window default=[-8.0, 5.0]` = DOS eV 창).
#:     자릿수만 보는 TUPLE2 규약을 그대로 따른다.
ARG_CALL = re.compile(r"add_argument\(")
ARG_OPT = re.compile(r"^\s*[\"']--?([\w\-]+)[\"']")
ARG_DEFAULT2 = re.compile(
    r"default\s*=\s*[\[(]\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*[\])]")

#: ④ 캐스케이드 그룹핑 — `dopant` 를 **그대로** 그룹 키로 쓰면 `WO3` 와 `WO3+Clrich` 가
#:   다른 종이 되고, 라벨 사이에서 변형이 바뀐 종이 통째로 사라진다.
#:   2026-08-16 하루에 세 번 밟았다 (조성족 감사 · scatter 감사 81 vs 90 · 슬롯 후보 40 vs 50).
#:   정본은 tools/cascade/cascade_ids.py 의 base_species() 다.
#:   ⚠ **읽기·정렬은 안 잡는다.** `[r["dopant"] for r in pool]` 처럼 이미 base 인 자료를
#:     읽는 곳까지 잡으면 오탐이 15건 나온다 (funnel['pool']·themes['dopants'] 는 47종
#:     전부 접미사 없음 — 실측 확인). 잡는 것은 **행을 종별로 묶는 대입**뿐이다.
#:     그게 종이 사라지는 유일한 경로다. 정렬 키로 raw 를 쓰는 것은 순서만 바뀐다.
RAW_DOPANT_GROUP = re.compile(
    r"""(?x)
    (?: ^\s*\w+ \s*\[ [^\]]*\[["']dopant["']\] [^\]]* \] [^=\n]* =   # by[r["dopant"]][x] =
      | \.setdefault\(\s*\w+\[["']dopant["']\]                          # .setdefault(r["dopant"]
    )""")
#: 그 줄/근처에 이게 있으면 **의도적으로 raw 를 쓴 것**으로 본다.
#:   `.split("+")[0]` 는 base_species 를 손으로 쓴 것이라 통과시킨다 (8곳이 이미 그렇게 한다).
#:   `PLAIN variant` / `plain 전용` 은 그 자료가 설계상 plain 만 담는다는 표시다.
RAW_DOPANT_OK = re.compile(
    r"""base_species|variant_key|by_base\s*=\s*False|raw 의도|variant 구별"""
    r"""|\.split\(\s*["']\+["']\s*\)"""          # r["dopant"].split("+")[0]
    r"""|PLAIN variant|plain 전용|함정을 재현""")

#: 규약에서 의도적으로 벗어난 파일 — 사유를 반드시 적는다 (빈 사유 금지)
EXEMPT = {
    "tools/ionic/md_temperature_feasibility.py":
        "D 추출이 아니라 역산: 게이트 MSD 도달 t_min = MSD/(6D)",
    "tools/ionic/beta_null_test.py":
        "창 사다리가 목적 — (2,50)(10,50)(25,100)(50,200) 을 일부러 훑는다",
    "tools/ionic/msd_refit_window.py":
        "창 민감도 진단 도구 — 여러 창이 존재 이유",
    "tools/ionic/msd_diffusive_check.py":
        "창 스캔 진단 도구 — --scan 이 여러 창을 훑는다",
    "tools/comp1_v3/b2o3_all_bond_lengths.py":
        "MSD 창이 아니라 **결합길이 창(Å)** 이다 — DECOMP_WINDOWS[('B','S')]=(1.60,2.40) 처럼 "
        "단위가 ps 가 아니라 Å 다. 시간창 규약과 무관한 오탐 (2026-08-25)",
}


def scan(path: Path):
    """파일 하나에서 규약 위반 후보를 뽑는다. (violations, warnings)"""
    try:
        rel = str(path.relative_to(REPO))
    except ValueError:          # selftest 의 임시 경로
        rel = path.name
    text = path.read_text(errors="ignore")
    viol, warn = [], []
    if rel in EXEMPT:
        return viol, warn

    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if FORCED_D.search(line) and not FREE_FIT.search(line):
            viol.append((rel, i, "원점강제 D 추출 — 자유절편(MSD=c+6Dt)이 정본", line.strip()))
        m = WINDOW_ASSIGN.match(line)
        if m and not WINDOW_NON_TIME.search(m.group(1)) and not AUX_WINDOW_OK.search(
                line + "\n" + (text.splitlines()[i - 2] if i >= 2 else "")):
            for a, b in TUPLE2.findall(m.group(2)):
                w = (float(a), float(b))
                if w != CANON_WINDOW:
                    viol.append((rel, i, f"MSD 창 {w} — 정본은 {CANON_WINDOW} ps",
                                 line.strip()))
        for k in KB_HIT.findall(line):
            if k != KB_CANON:
                warn.append((rel, i, f"kB {k} → {KB_CANON} 권고 (상대차 1e-7, 무해)"))
        # 영국식 철자 — **문자열 리터럴 안**만 본다 (화면에 나가는 글)
        #   `brit-ok: <사유>` 주석이 그 줄이나 바로 윗줄에 있으면 건너뛴다. 철자를
        #   **찾아내는 쪽** 코드(검출 단어 목록)가 스스로에게 걸리는 것을 막는다.
        if rel.startswith(("tools/seminar", "tools/figures")) and not BRIT_OK.search(
                line + "\n" + (text.splitlines()[i - 2] if i >= 2 else "")):
            for q in _re.findall(r"[\"']([^\"']{4,})[\"']", line):
                for w in BRIT_RE.findall(q):
                    warn.append((rel, i, f"영국식 철자 '{w}' → '{BRIT_US[w.lower()]}' "
                                         f"(발표 영어는 미국식 통일)"))
        if RAW_DOPANT_GROUP.search(line):
            # 사유 주석이 블록 위쪽에 붙는 일이 흔해 앞을 넉넉히 본다 (4줄은 짧았다)
            ctx = "\n".join(text.splitlines()[max(0, i - 9):i + 2])
            if not RAW_DOPANT_OK.search(ctx):
                viol.append((rel, i,
                             "raw `dopant` 로 그룹핑 — WO3 와 WO3+Clrich 가 갈린다. "
                             "cascade_ids.base_species() 를 쓸 것 "
                             "(변형 구별이 목적이면 variant_key() + 사유 주석)",
                             line.strip()))

    # ── ⑥ argparse 기본 창 ────────────────────────────────────────────────
    #   줄 단위로는 못 본다 — add_argument 가 여러 줄에 걸친다 (aimd_mlip.py:264-266).
    lines = text.splitlines()
    for m in ARG_CALL.finditer(text):
        ln = text.count("\n", 0, m.start()) + 1
        if ln <= len(lines) and lines[ln - 1].lstrip().startswith("#"):
            continue                       # 주석 안의 예시는 코드가 아니다
        chunk = text[m.end():m.end() + 400].split("add_argument(")[0]
        o = ARG_OPT.match(chunk)
        if not o:
            continue
        opt = o.group(1)
        if "window" not in opt.lower() or WINDOW_NON_TIME.search(opt):
            continue
        d = ARG_DEFAULT2.search(chunk)
        if not d:
            continue                       # 기본값 없음 = 필수 인자 → 위반 아님(오히려 안전)
        w = (float(d.group(1)), float(d.group(2)))
        if w != CANON_WINDOW:
            viol.append((rel, ln,
                         f"argparse 기본 MSD 창 {w} — 정본은 {CANON_WINDOW} ps. "
                         f"창을 안 적은 러너는 이 값으로 돈다",
                         f"--{opt}  default={list(w)}"))
    return viol, warn


#: 발표·그림에 나가는 영어는 **미국식 철자**로 통일한다 (1저자 지적 2026-08-18:
#:   "계속 유럽체 하는데 coloured 처럼 이런거 조심해"). 슬라이드 한 장에 colour/color
#:   가 섞이면 그 자체가 눈에 띈다. 주석은 검사하지 않는다 — 화면에 안 나가므로.
BRIT_US = {
    "coloured": "colored", "colour": "color", "colours": "colors",
    "colouring": "coloring", "normalise": "normalize", "normalised": "normalized",
    "normalisation": "normalization", "analyse": "analyze", "analysed": "analyzed",
    "behaviour": "behavior", "neighbour": "neighbor", "neighbours": "neighbors",
    "optimise": "optimize", "optimised": "optimized", "favour": "favor",
    "optimiser": "optimizer", "normaliser": "normalizer", "analyser": "analyzer",
    "centre": "center", "modelling": "modeling", "labelled": "labeled",
    "sulphur": "sulfur", "catalogue": "catalog", "ageing": "aging",
    "defence": "defense", "fibre": "fiber", "utilise": "utilize",
}
BRIT_RE = _re.compile(r"\b(" + "|".join(sorted(BRIT_US, key=len, reverse=True)) + r")\b", _re.I)
#: 철자 검사를 끄는 표시 — 사유를 뒤에 적는다 (`# brit-ok: 검출용 단어 목록`).
BRIT_OK = _re.compile(r"brit-ok\s*:")
#: 보조 창 표시 — **기록 전용 열**로 선언된 비정본 MSD 창 (2026-10-05 추가)
#:   실물: `tools/ionic/glass_v2_readout.py` 의 `WINDOW_AUX = (50.0, 200.0)` — 회신 CO 개정
#:   (2026-10-04 비준)이 "2–50 ps 주 판정 그대로 · 50–200 ps 는 기록 전용 열" 로 사전등록했다.
#:   EXEMPT 로 파일을 덮으면 같은 파일의 주 창 `WINDOW` 까지 눈이 먼다 → 줄 단위로만 끈다.
#:   `aux-window-ok: <사유>` 가 그 줄이나 바로 윗줄에 있어야 하고 **사유가 비면 안 된다**
#:   (brit-ok 와 같은 창 규칙 — 두 줄 위면 다시 잡는다).
AUX_WINDOW_OK = _re.compile(r"aux-window-ok\s*:\s*\S")


def check(root=None):
    root = root or (REPO / "tools")
    viol, warn = [], []
    for p in sorted(root.rglob("*.py")):
        if p.name == "convention_check.py":
            continue
        v, w = scan(p)
        viol += v
        warn += w
    return viol, warn



# ── 셸 러너 ↔ 파이썬 도구의 **필수 인자** 대조 (2026-09-09 추가) ──────────────
#: ⛔⛔ 왜 생겼나 — 2026-08-30 에 `run_anneal.py` 의 `--seed` 를 **필수**로 만들었다
#:   (회신 AL 해제조건 2 · 비결정 endpoint 차단). 그런데 부르는 쪽인
#:   `tier_cascade.sh` 를 안 고쳤고, **열흘 동안 아무도 몰랐다.**
#:   2026-09-09 에 273 캐스케이드를 던졌더니 Stage 01–03 을 30분씩 정상으로 돌고
#:   Stage 04 에서 전부 `error: the following arguments are required: --seed` 로 죽었다.
#:   도구 하나를 엄격하게 만들면 부르는 쪽이 조용히 깨진다 — 그걸 기계가 봐야 한다.
#:
#: ⛔ 이 검사가 **못 하는 것**
#:   · 인자의 **값**이 맞는지는 안 본다. `--seed` 가 있으면 통과다.
#:   · 변수로 조립한 호출(`CMD="python3 $TOOL"; $CMD`)은 못 본다 — 리터럴만 본다.
#:   · 파이썬이 파이썬을 부르는 것은 안 본다 (subprocess 인자 조립은 형태가 너무 다양하다).
_RE_REQ = re.compile(
    r"""add_argument\(\s*['"](--[A-Za-z0-9_-]+)['"](?P<rest>[^)]*)\)""", re.S)
_RE_PYCALL = re.compile(r"""python3?\s+(?:-u\s+)?(tools/[A-Za-z0-9_/.-]+\.py)""")


def _required_flags(py: Path):
    """그 도구의 `required=True` 인 롱플래그 집합. 못 읽으면 빈 집합."""
    try:
        src = py.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return set()
    out = set()
    for m in _RE_REQ.finditer(src):
        if "required=True" in (m.group("rest") or ""):
            out.add(m.group(1))
    return out


def check_shell_calls(root=None):
    """tools/**/*.sh 안의 `python3 tools/x.py …` 호출이 x.py 의 필수 인자를 다 넘기나.

    → [(sh경로:줄, 도구, 빠진 플래그들)]
    """
    base = Path(root) if root else REPO
    bad = []
    for sh in sorted((base / "tools").rglob("*.sh")):
        try:
            lines = sh.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        i = 0
        while i < len(lines):
            m = _RE_PYCALL.search(lines[i])
            if not m:
                i += 1
                continue
            # ⚠ 오탐 회귀 (2026-09-09 실측 2건) — `echo "다음: python3 tools/x.py …"` 같은
            #   **안내문**은 실행이 아니다. 두 파일이 그렇게 걸렸다(cube_diff · qe_to_vasp).
            #   판정: 호출 앞에 echo/ts/printf/# 가 있거나, 그 줄이 따옴표 안이면 건너뛴다.
            _head = lines[i][:m.start()]
            if re.search(r"(^|[;&|]|\bthen\b)\s*(echo|printf|ts|log|LOG|cat)\b", _head) \
                    or _head.lstrip().startswith("#") \
                    or _head.count('"') % 2 == 1 or _head.count("'") % 2 == 1:
                i += 1
                continue
            tool = base / m.group(1)
            # 호출은 백슬래시 연속줄로 이어진다 — 끊길 때까지 모은다
            j, chunk = i, lines[i]
            while chunk.rstrip().endswith("\\") and j + 1 < len(lines):
                j += 1
                chunk += " " + lines[j]
            req = _required_flags(tool)
            miss = sorted(f for f in req if f not in chunk)
            if miss:
                bad.append((f"{sh.relative_to(base)}:{i+1}", m.group(1), miss))
            i = j + 1
    return bad


# ── selftest 스윕 (2026-08-31 추가) ──────────────────────────────────────
#: 왜 여기인가: 이 파일은 "같은 규약이 조용히 갈라지는 것" 을 막는 가드다.
#:   **죽은 selftest** 도 같은 병이다 — 2026-08-31 스윕에서 `codoping_ml.py` 의
#:   `--selftest` 가 존재하지 않는 함수를 부르며 `NameError` 로 죽어 있었다.
#:   그 도구는 한 번도 시험된 적이 없었고 아무도 몰랐다.
SWEEP_TIMEOUT_S = 120
#: 인자가 더 필요해 rc≠0 인 것은 실패가 아니다 (argparse 필수인자)
SWEEP_NOT_FAILURE = ("required", "expected one argument", "the following arguments")


def sweep_selftests(root=None, verbose=False):
    """`--selftest` 를 가진 **.py 도구 전부**를 돌려 죽은 것을 찾는다.

    → (pass, fail, skip, [(경로, rc, 마지막줄)])

    ⛔ 이 함수가 **못 하는 것**
      · selftest 의 **내용**이 의미 있는지는 모른다. 통과한다는 것만 본다
        (양성만 있는 selftest 는 통과해도 아무것도 보증하지 않는다 — CLAUDE.md).
      · `.sh` 러너와 `__pycache__` 는 제외한다 (파이썬이 아니다).
      · 타임아웃(%d s)을 넘으면 실패가 아니라 skip 이다 — 느린 것과 죽은 것은 다르다.
    """ % SWEEP_TIMEOUT_S
    import subprocess
    root = Path(root or REPO)
    tools = sorted(p for p in (root / "tools").rglob("*.py")
                   if "__pycache__" not in p.parts
                   and "--selftest" in p.read_text(errors="ignore"))
    ok = fails = skipped = 0
    bad = []
    for p in tools:
        try:
            r = subprocess.run([sys.executable, str(p), "--selftest"],
                               capture_output=True, text=True,
                               timeout=SWEEP_TIMEOUT_S, cwd=str(root))
        except subprocess.TimeoutExpired:
            skipped += 1
            if verbose:
                print("  ⏱ %s" % p.relative_to(root))
            continue
        out = (r.stdout or "") + (r.stderr or "")
        if r.returncode == 0:
            ok += 1
            if verbose:
                print("  ✔ %s" % p.relative_to(root))
            continue
        if any(k in out for k in SWEEP_NOT_FAILURE):
            skipped += 1                       # 인자 부족 — 시험 실패가 아니다
            continue
        fails += 1
        last = [x for x in out.strip().splitlines() if x.strip()]
        bad.append((str(p.relative_to(root)), r.returncode,
                    last[-1][:110] if last else ""))
    return ok, fails, skipped, bad


def cmd_sweep(verbose=False):
    ok, fails, skipped, bad = sweep_selftests(verbose=verbose)
    for path, rc, last in bad:
        print("  \u26d4 rc=%s  %s\n       %s" % (rc, path, last))
    print("selftest 스윕: PASS %d \u00b7 FAIL %d \u00b7 skip %d" % (ok, fails, skipped))
    return 1 if fails else 0


def main():
    if "--selftests" in sys.argv:
        return cmd_sweep("-v" in sys.argv or "--verbose" in sys.argv)
    viol, warn = check()
    print("=== 물리 규약 검사 ===")
    print(f"면제 {len(EXEMPT)}건 (사유 명시됨)\n")
    print(f"위반 ({len(viol)}):")
    for rel, ln, why, src in viol:
        print(f" ✗ {rel}:{ln} — {why}\n     {src}")
    print(f"\n경고 ({len(warn)}):")
    for rel, ln, why in warn[:10]:
        print(f" ⚠ {rel}:{ln} — {why}")
    if len(warn) > 10:
        print(f"   … 외 {len(warn) - 10}건")

    # ── 셸 러너 ↔ 파이썬 도구 필수 인자 (2026-09-09) ────────────────────────
    #   도구 하나를 엄격하게 만들면 부르는 쪽이 조용히 깨진다. 열흘 뒤 273 캐스케이드가
    #   Stage 04 에서 전부 죽고서야 알았다 — 그건 사람이 아니라 기계가 볼 일이다.
    sh_bad = check_shell_calls()
    print(f"\n셸 러너 필수 인자 누락 ({len(sh_bad)}):")
    for where, tool, miss in sh_bad:
        print(f" ✗ {where} → {tool} 에 {' '.join(miss)} 를 안 넘긴다")

    if not viol and not sh_bad:
        print("\nRESULT: 0 위반 — 2026-08-11 기준선 유지")
    return 1 if (viol or sh_bad) else 0


def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as d:
        t = Path(d)
        # 음성: 위반이 있는 파일을 못 잡으면 실패
        (t / "bad.py").write_text(
            "D = msd / (6.0 * t)\n"
            "WINDOW = (10.0, 100.0)  # msd window\n"
            "KB = 8.617e-5\n")
        # 양성: 정상 파일에서 오탐이 나면 실패
        (t / "good.py").write_text(
            "c, m = np.polyfit(t, msd, 1)\nD = m / 6.0\n"
            "WINDOW = (2.0, 50.0)  # msd window\n"
            f"KB = {KB_CANON}\n")
        # 주석 줄은 무시해야 한다
        (t / "comment.py").write_text("# D = msd / (6.0 * t) 라고 쓰면 안 된다\n")
        # 오탐 회귀: 'window' 단어가 라벨에 든 plot 호출은 창 대입이 아니다
        (t / "plotlabel.py").write_text(
            'ax.set_xlabel("stable window")\nax.set_xlim(1.3, 2.1)\n')
        # 오탐 회귀 (2026-09-06): 이름이 단위를 밝힌 창은 시간창이 아니다 (XRD 2θ · Å · eV)
        (t / "unitwindow.py").write_text(
            "window_2theta = (8.0, 11.0)\n"
            "WINDOW_EV = (0.5, 3.0)\n"
            "bond_window_ang = (1.60, 2.40)\n")
        # ── 셸 러너 ↔ 필수 인자 (2026-09-09) ──────────────────────────────
        #   ⛔음성: 필수 인자를 빠뜨린 호출을 못 잡으면 실패
        (t / "tool_req.py").write_text(
            "import argparse\n"
            "p = argparse.ArgumentParser()\n"
            "p.add_argument('--out', required=True)\n"
            "p.add_argument('--seed', type=int, required=True)\n"
            "p.add_argument('--device', default='cuda')\n")
        (t / "caller_bad.sh").write_text(
            "python3 tools/tool_req.py \\\n    --out x \\\n    --device cuda\n")
        (t / "caller_good.sh").write_text(
            "python3 tools/tool_req.py \\\n    --out x --seed 1 \\\n    --device cuda\n")
        _shroot = t / "_sh"
        (_shroot / "tools").mkdir(parents=True)
        (_shroot / "tools" / "tool_req.py").write_text((t / "tool_req.py").read_text())
        (_shroot / "tools" / "caller_bad.sh").write_text((t / "caller_bad.sh").read_text())
        (_shroot / "tools" / "caller_good.sh").write_text((t / "caller_good.sh").read_text())
        # ⛔음성 회귀: echo 안내문은 실행이 아니다 (2026-09-09 실측 오탐 2건)
        (_shroot / "tools" / "caller_echo.sh").write_text(
            'echo "다음: python3 tools/tool_req.py --out x"\n')
        _sc = check_shell_calls(_shroot)
        if [x for x in _sc if "caller_echo" in x[0]]:
            print("⛔ selftest: echo 안내문을 실행으로 오탐했다"); ok = False
        _bad = [x for x in _sc if "caller_bad" in x[0]]
        _good = [x for x in _sc if "caller_good" in x[0]]
        if not (_bad and _bad[0][2] == ["--seed"]):
            print("⛔ selftest: 필수 인자 누락(--seed)을 못 잡았다:", _sc); ok = False
        if _good:
            print("⛔ selftest: 정상 호출을 오탐했다:", _good); ok = False

        # ⛔ 그렇다고 다 통과시키면 안 된다 — 단위를 안 밝힌 창은 여전히 잡아야 한다
        (t / "unitwindow_bad.py").write_text(
            "fit_window = (10.0, 100.0)\n"
            "window_ps = (10.0, 100.0)\n")
        # 보조 창 표시 (2026-10-05): 사유 있는 aux-window-ok 는 그 줄만 끈다
        (t / "auxwin_good.py").write_text(
            "WINDOW = (2.0, 50.0)\n"
            "WINDOW_AUX = (50.0, 200.0)  # aux-window-ok: 회신 CO 기록 전용 열\n"
            "# aux-window-ok: 진단 창\n"
            "WINDOW_DIAG = (10.0, 100.0)\n")
        # ⛔음성: 사유가 비거나 · 두 줄 위에 있거나 · 표시 없는 창은 그대로 잡는다 (3 건)
        (t / "auxwin_bad.py").write_text(
            "WINDOW_AUX = (50.0, 200.0)  # aux-window-ok:\n"
            "# aux-window-ok: 두 줄 위\n"
            "x = 1\n"
            "WINDOW_FAR = (50.0, 200.0)\n"
            "WINDOW_AUX2 = (50.0, 200.0)  # 표시 없음\n")
        # ⑥ argparse 기본값 (2026-09-08) — **여기가 실제로 새던 자리다.**
        #   음성: 창을 2–20 으로 되돌린 파일을 검사기가 잡아야 한다. 못 잡으면
        #   "0 위반" 은 규약이 지켜졌다는 뜻이 아니라 **안 봤다**는 뜻이다.
        (t / "argwin_bad.py").write_text(
            'ap.add_argument("--fit_window_ps", type=float, nargs=2,\n'
            '                default=[2.0, 20.0],\n'
            '                help="MSD linear-fit window (ps)")\n')
        (t / "argwin_bad2.py").write_text(
            'ap.add_argument("--fit_window_ps", type=float, nargs=2, default=[5.0, 40.0])\n')
        (t / "argwin_good.py").write_text(
            'ap.add_argument("--fit_window_ps", type=float, nargs=2, default=[2.0, 50.0])\n'
            'ap.add_argument("--window_2theta", type=float, nargs=2, default=[8.0, 11.0])\n'
            'ap.add_argument("--energy_window", type=float, nargs=2, default=[-6, 6])\n'
            'ap.add_argument("--fit_window_ps", type=float, nargs=2, required=True)\n'
            'ap.add_argument("--prod_ps", type=float, default=200.0)\n'
            '# ap.add_argument("--fit_window_ps", nargs=2, default=[5.0, 40.0])  # 옛 판\n')

        for name, want_v, want_w, label in [
                ("bad.py", 2, 1, "위반 검출"), ("good.py", 0, 0, "오탐 없음"),
                ("comment.py", 0, 0, "주석 무시"),
                ("plotlabel.py", 0, 0, "plot 라벨 오탐 없음"),
                ("unitwindow.py", 0, 0, "단위 밝힌 창(2θ/eV/Å) 오탐 없음"),
                ("unitwindow_bad.py", 2, 0, "⛔음성: 단위 안 밝힌 창은 그대로 잡는다"),
                ("auxwin_good.py", 0, 0, "aux-window-ok 표시(같은 줄·윗줄)는 그 줄만 끈다"),
                ("auxwin_bad.py", 3, 0,
                 "⛔음성: aux-window-ok 사유 없음·두 줄 위·표시 없음은 잡는다"),
                ("argwin_bad.py", 1, 0,
                 "⛔음성: argparse 기본값을 2–20 으로 되돌리면 잡는다 (여러 줄)"),
                ("argwin_bad2.py", 1, 0, "⛔음성: 5–40 도 잡는다 (한 줄)"),
                ("argwin_good.py", 0, 0,
                 "argparse 오탐 없음 (2–50 · 2θ · 음수 eV 창 · 기본값 없음 · 주석)")]:
            v, w = scan(t / name)
            # scan 은 REPO 기준 상대경로를 쓰므로 임시경로엔 rglob 대신 직접 호출
            got = (len(v), len(w))
            if got != (want_v, want_w):
                print(f" ✗ {label}: {name} → 위반{got[0]}·경고{got[1]} "
                      f"(기대 {want_v}·{want_w})")
                ok = False
            else:
                print(f" ✓ {label}: {name}")
        # ── ④ raw dopant 그룹핑 (2026-08-16) ──────────────────────────────
        for nm, body, want in (
            ("raw 그룹핑 대입을 잡는다", 'by[r["dopant"]][r["lab"]] = r', True),
            ("setdefault 도 잡는다", 'o.setdefault(r["dopant"], {})[x] = v', True),
            ("음성: base_species 는 통과", 'by[base_species(r["dopant"])][r["lab"]] = r', False),
            ('음성: .split("+") 는 통과',
             'c.setdefault(r["dopant"].split("+")[0],[]).append(r)', False),
            ("음성: 읽기만 하면 통과", 'x = [r["dopant"] for r in pool]', False),
            ("음성: 정렬 키는 통과", 'sorted(rows, key=lambda r: r["dopant"])', False),
            ("음성: 사유 주석이 위에 있으면 통과",
             '# variant 구별\n' + 'y=1\n' * 6 + 'by[r["dopant"]][r["lab"]] = r', False),
        ):
            f = t / ("raw_%d.py" % abs(hash(nm)))
            f.write_text(body + "\n", encoding="utf-8")
            hit = any("raw `dopant`" in v[2] for v in scan(f)[0])
            ok &= (hit == want)
            print(("  ✓ " if hit == want else "  ✗ ") + f"[raw-dopant] {nm}")

    # ── ⑤ 영국식 철자 (2026-08-18) ────────────────────────────────────────
    #   이 규칙은 rel 경로가 tools/figures|seminar 로 시작할 때만 돈다 → 임시
    #   디렉터리로는 못 시험한다. 진짜 경로에 잠깐 파일을 놓고 반드시 지운다.
    probe = REPO / "tools" / "figures" / "_conv_probe_tmp.py"
    try:
        for nm, body, want in (
            ("문자열 안 영국식을 잡는다", 'ax.set_xlabel("coloured by site")', True),
            ("음성: 미국식은 통과", 'ax.set_xlabel("colored by site")', False),
            ("음성: 주석은 안 본다 (화면에 안 나감)", '# coloured 라고 쓰지 말 것', False),
            ("음성: brit-ok 가 같은 줄에 있으면 통과",
             'W = ("coloured", "colour")  # brit-ok: 검출용 단어 목록', False),
            ("음성: brit-ok 가 윗줄에 있어도 통과",
             '# brit-ok: 검출용 단어 목록\nW = ("coloured", "colour")', False),
            ("brit-ok 가 두 줄 위면 다시 잡는다",
             '# brit-ok: 사유\nx = 1\nW = ("coloured", "colour")', True),
        ):
            probe.write_text(body + "\n", encoding="utf-8")
            hit = any("영국식 철자" in w[2] for w in scan(probe)[1])
            ok &= (hit == want)
            print(("  ✓ " if hit == want else "  ✗ ") + f"[영국식 철자] {nm}")
    finally:
        probe.unlink(missing_ok=True)

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
