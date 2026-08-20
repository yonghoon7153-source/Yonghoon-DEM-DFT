#!/usr/bin/env python3
"""check_script_claims.py — 세미나 대본의 수치 주장을 db/properties 원자료에 대조한다.

왜 이 도구인가 (2026-08-20)
  덱 대본에 **DB 가 이미 반증한 문장**이 들어갔다:
    · "47 완주, 나머지 미완" — cascade_v23_ranked_v2.csv 는 89/89 네 축이 다 차 있고
      47 은 2026-06-25 스냅숏 등재 수(산화물37+불화물10)일 뿐이다.
    · "평균 30개 구조" — 실측 평균은 35.8, 30은 중앙값이다 (최대도 150 이 아니라 120).
  원인은 repo 크기가 아니라 **대본이 그림을 보고 쓰였다는 것**이다. 그림 범례가 틀리면
  대본도 같이 틀린다. 근거를 사람 기억이 아니라 **기계 경로**에 두는 게 유일한 방어다.
  (같은 처방을 db/governance/artifacts.json 이 산출물에 대해 이미 하고 있다.)

  ⛔ 그리고 이 도구 자신이 낼 뻔한 더 큰 사고를 함께 기록한다 (FORBIDDEN 주석 참조):
    "세 도핑 수준" 을 전역 금지로 걸었더니 **맞는 문장까지** 위반으로 잡았고, 나는 그걸
    믿고 고칠 뻔했다. 검사기가 근거 없이 넓게 잡으면 그 검사기를 믿고 맞는 걸 고치게 된다.

무엇을 하나
  대본 md 에서 아래 패턴을 찾아 원자료와 대조한다. 불일치는 종료코드 1.
    ① 금지 문구 (DB 가 반증한 서술)
    ② 등록된 수치 주장 (CLAIMS) — 파일에서 실제로 계산해 비교

이 도구가 **못 하는 것**
  · 대본의 물리 해석이 옳은지 판정하지 않는다. **숫자와 금지 문구**만 본다.
  · 등록되지 않은 새 주장은 못 잡는다 — CLAIMS 에 추가해야 검사된다.
    ⇒ 새 수치를 대본에 쓰면 **여기 등록하는 것까지가 한 작업**이다.
  · 그림(png) 안의 범례·축 라벨은 못 읽는다. 그림이 틀린 건 사람이 봐야 한다.

  python3 tools/seminar/check_script_claims.py --selftest
  python3 tools/seminar/check_script_claims.py kb/seminars/cascade_deck_8to12_script_2026_08_20.md
  python3 tools/seminar/check_script_claims.py --all          # kb/seminars/*.md 전부
"""
import argparse, csv, json, re, statistics, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB = ROOT / "db" / "properties"


# ── 원자료에서 값을 뽑는 함수들 (전부 파일을 실제로 읽는다) ───────────────────
def _rows(name):
    p = DB / name
    # ⚠ CSV 주석이 `"# ...` 처럼 **따옴표로 열리는** 경우가 있다 (cascade_pool_accounting.csv).
    #   startswith("#") 만 보면 그 줄이 헤더로 잡혀 KeyError 가 난다 — 2026-08 에 이미 한 번
    #   당한 버그다(PERATOM PDOS CSV). 두 형태를 다 거른다.
    lines = [l for l in p.read_text(encoding="utf-8").splitlines(True)
             if not l.startswith(("#", '"#'))]
    return list(csv.DictReader(lines))


def f_distinct_concentrations():
    return sorted({r["concentration"] for r in _rows("cascade_v23_all.csv")})


def f_n_structures():
    return len(_rows("cascade_v23_all.csv"))


def f_structures_per_item():
    from collections import Counter
    c = Counter(r["dopant"] for r in _rows("cascade_v23_all.csv"))
    v = list(c.values())
    return {"mean": round(statistics.mean(v), 1), "median": int(statistics.median(v)),
            "min": min(v), "max": max(v), "n_items": len(c)}


def f_axes_complete():
    rows = _rows("cascade_v23_ranked_v2.csv")
    ax = ("de", "ox_V", "E_GPa", "pugh")
    full = [r for r in rows if all(r[a] and r[a].strip() not in ("", "nan", "NA") for a in ax)]
    return {"n_pool": len(rows), "n_complete": len(full)}


def f_pool_planned_scored():
    for r in _rows("cascade_pool_accounting.csv"):
        if r["anion_family"] == "TOTAL":
            return {"planned": int(r["n_planned"]), "scored": int(r["n_scored"])}
    raise RuntimeError("TOTAL 행이 없다")


def f_47_split():
    from collections import Counter
    rows = _rows("cascade_seminar_pool_attrition_273_to_47.csv")
    inn = [r for r in rows if r["included_in_47_pool"] == "1"]
    out = [r for r in rows if r["included_in_47_pool"] != "1"]
    return {"n_in": len(inn), "n_out": len(out), "n_total": len(rows),
            "families_out": sorted(Counter(r["family"] for r in out))}


def f_volume_gate():
    d = json.loads((DB / "cascade_volume_gate_review.json").read_text(encoding="utf-8"))
    g = d["gates"]
    return {"cut": g["current_abs"]["cut_abs_dV"], "dropped": g["current_abs"]["dropped"],
            "alt_resid": g["alt_A_within_species_residual"]["dropped"],
            "alt_shape": g["alt_B_shape"]["dropped"]}


# ── 등록된 주장 ──────────────────────────────────────────────────────────────
# (설명, 대본에서 찾을 정규식, 원자료 계산 함수, 기대값 판정 함수)
CLAIMS = [
    ("구조 총수 3,615", r"3,?615", f_n_structures, lambda v: v == 3615),
    ("항목당 구조 중앙 30", r"중앙값?\s*30", f_structures_per_item, lambda v: v["median"] == 30),
    ("항목당 구조 평균 36", r"평균은?\s*36", f_structures_per_item, lambda v: round(v["mean"]) == 36),
    ("항목당 구조 범위 15~120", r"적은 건 15개, 많은 건 120개", f_structures_per_item,
     lambda v: v["min"] == 15 and v["max"] == 120),
    ("91 계획 / 89 점수", r"91개를 계획했고 \*\*89개", f_pool_planned_scored,
     lambda v: v["planned"] == 91 and v["scored"] == 89),
    ("네 축 89/89 완전", r"89/89", f_axes_complete, lambda v: v["n_complete"] == v["n_pool"] == 89),
    ("47 대 44 분할", r"빠진 44|나머지 44", f_47_split, lambda v: v["n_in"] == 47 and v["n_out"] == 44),
    ("부피 컷 25 % · 100종 탈락", r"25 ?% 를 넘긴 구조들이고.*?100개", f_volume_gate,
     lambda v: v["cut"] == 0.25 and v["dropped"] == 100),
    ("부피 게이트 대안 111 / 78", r"111개.*?78개", f_volume_gate,
     lambda v: v["alt_resid"] == 111 and v["alt_shape"] == 78),
]

# ── 금지 문구 (패턴, 문맥패턴 or None, 사유) ─────────────────────────────────
#
# ⛔⛔ 2026-08-20 교훈 — **전역 금지 규칙이 맞는 문장을 틀리게 만들 뻔했다.**
#   "세 도핑 수준" 을 전역 금지로 걸었더니 10장(자리 선호)까지 위반으로 잡혔다.
#   그런데 10장은 **다른 캠페인**이다:
#     site_preference_raw_78.csv — 78 = 26 산화물 × 3 nominal x, x_nominal 이 실제로 갈린다
#     cascade_v23_all.csv        — 3,615행 전부 x=0.25 로 붕괴
#   x 붕괴는 cascade 에만 해당한다. 그래서 규칙에 **문맥**을 붙인다: 문맥패턴이 있으면
#   **같은 절 안에** 그 문맥이 같이 있을 때만 위반이다.
#   ⇒ 검사기가 근거 없이 넓게 잡으면, 그 검사기를 믿고 맞는 걸 고치게 된다.
FORBIDDEN = [
    # 면제 문맥: 두 캠페인의 **구분을 설명하는** 절은 위반이 아니다 (그게 정답이다).
    (r"세 도핑 수준|묽게\s*·?\s*중간\s*·?\s*진하게|도핑 수준의 폭",
     r"(?!x)(?:3,?615|cascade_v23_all|구조 총수|배치를 전부)(?!x)",
     "cascade 캠페인(3,615구조)의 x 라벨은 **실측 전부 0.25** 다. "
     "⚠ 단 10장(site_preference_raw_78, 26×3 nominal x)에서는 '세 도핑 수준' 이 **맞다** — 섞지 말 것."),
    (r"나머지 (44|사십사).{0,12}(미완|unfinished)", None,
     "44 는 미완이 아니다 — cascade_v23_ranked_v2.csv 에서 네 축이 89/89 채워져 있다."),
    (r"평균\s*30\s*개?\s*구조|30 structures on average", None,
     "30 은 중앙값이다. 평균은 35.8 이다."),
    (r"많은 건 150", None,
     "최대는 120 이다 (cascade_v23_all.csv)."),
    (r"작년 6월|2026-06-29 snapshot", None,
     "9장 컬러바는 89종 2026-08-13 판이다. 6월 스냅숏 단서는 낡았다."),
    (r"47\s*→\s*1\s*로 걸러|최종 승자", None,
     "codex_C 판정: 47→11 은 역사적 규칙 교집합, 11→1 은 로스터 상대 진단값이다."),
]


def check(path: Path):
    txt = path.read_text(encoding="utf-8")
    # ⚠ 금지 문구는 "고친 것" 절에서 **인용**될 수밖에 없다. 정정 마커가 같은 줄에 있으면
    #   그건 위반이 아니라 **기록**이다 — 안 그러면 정정을 적을수록 위반이 늘어난다.
    #   (첫 판은 줄 시작 문자만 봐서 '👉 ... "세 도핑 수준" 이라고 써서 틀렸다' 를 위반으로 셌다.)
    MARK = ("⛔", "❌", "✗", "틀렸다", "말하지 말 것", "고칠 것", "옛 문구", "교체",
            "이전 대본", "이전 판", "낡았다", "반증", "금지", "부르지 않", "라고 하면")
    # ★ 정정 기록 **절 전체**를 면제한다. 제목 줄에 금지 문구가 들어가는 건 피할 수 없다
    #   ("### (1) '세 도핑 수준' 은 없다"). 줄 단위 마커만으로는 그 제목을 못 살린다.
    #   면제 절: 제목에 §0 / '고친 것' / '정정' 이 들어간 절 ~ 다음 같은 깊이 제목 전까지.
    keep, skip = [], False
    for l in txt.splitlines():
        if l.startswith("## "):
            skip = ("§0" in l) or ("고친 것" in l) or ("정정" in l)
        if not skip:
            keep.append(l)
    body = "\n".join(l for l in keep
                     if not l.lstrip().startswith("> ") and not any(m in l for m in MARK))
    bad = []
    # 문맥 규칙은 **절 단위**로 본다 (## 제목 기준).
    sections, cur = [], []
    for l in body.splitlines():
        if l.startswith("## ") and cur:
            sections.append("\n".join(cur)); cur = []
        cur.append(l)
    sections.append("\n".join(cur))
    for pat, ctx, why in FORBIDDEN:
        for sec in sections:
            m = re.search(pat, sec)
            if not m:
                continue
            if ctx and not re.search(ctx, sec):
                continue          # 문맥이 없으면 이 절에서는 위반이 아니다
            # ★ 두 캠페인의 구분을 설명하는 절은 면제 — 그게 정답이기 때문이다.
            if re.search(r"site_preference|자리 선호|nominal x|섞지 말|다른 캠페인", sec):
                continue
            bad.append(f"⛔ 금지 문구 '{m.group(0)}' — {why}")
            break
    for desc, pat, fn, ok in CLAIMS:
        if not re.search(pat, txt, re.S):
            continue                      # 이 대본이 그 주장을 안 하면 넘어간다
        try:
            val = fn()
        except Exception as e:
            bad.append(f"⛔ {desc}: 원자료를 못 읽었다 ({e})")
            continue
        if not ok(val):
            bad.append(f"⛔ {desc}: 대본이 주장하지만 원자료는 {val} 이다")
    return bad


def selftest():
    import tempfile
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        if not c:
            ok = False

    # 원자료 접근이 실제로 되는지 (양성)
    chk(f_n_structures() == 3615, f"구조 총수 {f_n_structures()} = 3615")
    chk(f_distinct_concentrations() == ["0.25"],
        f"concentration 유일값 {f_distinct_concentrations()} — 도핑 수준은 하나뿐")
    sp = f_structures_per_item()
    chk(sp["median"] == 30 and sp["max"] == 120,
        f"항목당 구조 중앙 {sp['median']} · 최대 {sp['max']}")
    chk(sp["mean"] != 30, f"[음성] 평균({sp['mean']})은 30 이 아니다 — 평균/중앙값 혼동을 잡는다")
    ax = f_axes_complete()
    chk(ax["n_complete"] == ax["n_pool"] == 89, f"네 축 완전 {ax}")
    s47 = f_47_split()
    chk(s47["n_in"] == 47 and s47["n_out"] == 44, f"47/44 분할 {s47['n_in']}/{s47['n_out']}")

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "t.md"

        # [음성] 금지 문구를 심으면 반드시 잡혀야 한다
        # [음성] ★ 2026-08-20 near-miss: 문맥이 다르면 같은 문구도 위반이 아니다
        p.write_text("## 10장\n막대는 세 도핑 수준의 폭입니다. 26 산화물 × 3 nominal x.",
                     encoding="utf-8")
        chk(check(p) == [], "[음성] 자리선호(10장) 문맥의 '세 도핑 수준' 은 위반이 아니다")
        p.write_text("## 11장\n구조 3,615개를 배치를 전부 만들었고 막대는 세 도핑 수준입니다.",
                     encoding="utf-8")
        chk(any("세 도핑 수준" in x for x in check(p)),
            "[음성] cascade(3,615) 문맥에서는 같은 문구가 위반이다")

        p.write_text("나머지 44 는 미완입니다.", encoding="utf-8")
        chk(any("미완이 아니다" in x for x in check(p)), "[음성] '나머지 44 미완' 검출")

        p.write_text("화합물 하나가 평균 30 개 구조가 됐고", encoding="utf-8")
        chk(any("중앙값이다" in x for x in check(p)), "[음성] '평균 30개' 검출")

        p.write_text("적은 건 15 개, 많은 건 150 개고요", encoding="utf-8")
        chk(any("최대는 120" in x for x in check(p)), "[음성] '많은 건 150' 검출")

        # [음성] 정정 기록으로서의 인용은 잡으면 안 된다 (거짓 양성 방지)
        p.write_text('> 이전 대본: *"막대는 세 도핑 수준의 폭입니다"*\n'
                     '⛔ 틀렸다. 실측은 x=0.25 하나다.\n', encoding="utf-8")
        chk(check(p) == [], "[음성] 인용된 정정 기록은 위반으로 안 센다")

        # [음성] 틀린 수치 주장은 잡혀야 한다
        p.write_text("총 3,615 개입니다. 중앙값 30 · 평균은 36 입니다.", encoding="utf-8")
        chk(check(p) == [], "[양성] 맞는 수치 주장은 통과")

        # 깨끗한 문서는 통과
        p.write_text("아무 수치도 없는 문장입니다.", encoding="utf-8")
        chk(check(p) == [], "[양성] 주장 없는 문서는 통과")

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--all", action="store_true", help="kb/seminars/*.md 전부")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    targets = [Path(p) for p in a.paths]
    if a.all:
        targets += sorted((ROOT / "kb" / "seminars").glob("*.md"))
    if not targets:
        ap.error("대본 경로나 --all 을 줘라")
    nbad = 0
    for t in targets:
        bad = check(t)
        if bad:
            nbad += len(bad)
            print(f"\n{t.relative_to(ROOT)}")
            for b in bad:
                print(f"  {b}")
        else:
            print(f"✅ {t.relative_to(ROOT)}")
    if nbad:
        print(f"\n⛔ {nbad}건 — 대본이 원자료와 어긋난다")
    return 1 if nbad else 0


if __name__ == "__main__":
    sys.exit(main())
