#!/usr/bin/env python3
"""물리 규약 회귀 가드 — 같은 규약이 여러 파일에 복사돼 있어도 갈라지지 않게 한다.

배경: tools/ 에 MSD 구현 8개·아레니우스 적합 6개가 흩어져 있다 (2026-08-11 실측).
2026-08-11 기준으로는 **갈라지지 않았다** — 이 도구는 그 상태를 유지시키는
회귀 가드지, 지금 있는 문제를 고치는 도구가 아니다. 그래서 얇게 만든다.

검사 대상은 **틀리면 논문 숫자가 바뀌는 것** 둘 + 무해한 것 하나(경고):
  ① D 추출 = 자유절편 (MSD = c + 6Dt). 원점강제(msd/(6t))는 D 가 케이지 절편에
     오염된다 — 2026-08-11 β 게이트 사태의 뿌리.
  ② MSD 창 = 2–50 ps (CLAUDE.md 정본). 창이 다르면 Ea 가 242 meV 까지 움직인다.
  ③ (경고) kB 자릿수 — 상대차 1e-7 이라 무해. 통일만 권고.

의도적으로 **검사하지 않는 것**: 아레니우스 온도 집합. 타당한 변이(타당성 스캔
300–1000 K, 6점 진단, 3점 정본)가 많아 경고가 소음이 된다.

이 도구가 **못 하는 것**: 정규식 기반이라 AST 수준 우회를 못 본다 —
변수를 경유한 계산(`den = 6*t; D = msd/den`), 다른 모듈에서 import 한 창 상수,
동적으로 만든 창은 안 잡힌다. 통과가 곧 정합성 보증은 아니다.

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
WINDOW_ASSIGN = re.compile(r"^\s*\w*[Ww][Ii][Nn][Dd][Oo][Ww]\w*\s*(?::[^=]+)?=\s*(.+)$")
TUPLE2 = re.compile(r"\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*\)")
KB_HIT = re.compile(r"8\.617[0-9]*e-0?5")
CANON_WINDOW = (2.0, 50.0)

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
        if m:
            for a, b in TUPLE2.findall(m.group(1)):
                w = (float(a), float(b))
                if w != CANON_WINDOW:
                    viol.append((rel, i, f"MSD 창 {w} — 정본은 {CANON_WINDOW} ps",
                                 line.strip()))
        for k in KB_HIT.findall(line):
            if k != KB_CANON:
                warn.append((rel, i, f"kB {k} → {KB_CANON} 권고 (상대차 1e-7, 무해)"))
        # 영국식 철자 — **문자열 리터럴 안**만 본다 (화면에 나가는 글)
        if rel.startswith(("tools/seminar", "tools/figures")):
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
    "centre": "center", "modelling": "modeling", "labelled": "labeled",
    "sulphur": "sulfur", "catalogue": "catalog", "ageing": "aging",
    "defence": "defense", "fibre": "fiber", "utilise": "utilize",
}
BRIT_RE = _re.compile(r"\b(" + "|".join(sorted(BRIT_US, key=len, reverse=True)) + r")\b", _re.I)


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


def main():
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
    if not viol:
        print("\nRESULT: 0 위반 — 2026-08-11 기준선 유지")
    return 1 if viol else 0


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

        for name, want_v, want_w, label in [
                ("bad.py", 2, 1, "위반 검출"), ("good.py", 0, 0, "오탐 없음"),
                ("comment.py", 0, 0, "주석 무시"),
                ("plotlabel.py", 0, 0, "plot 라벨 오탐 없음")]:
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

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
