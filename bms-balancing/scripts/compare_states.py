"""상태·셀을 가로질러 축퇴 폭을 견준다 — §1-10 의 표를 만드는 명령.

왜 스크립트인가: 이 비교를 손으로 하면 그 숫자가 **문서에만 있는 주장**이 된다.
§2 에서 이미 한 번 그렇게 됐고(97 행 원표가 없어 재현이 안 됐다) 그것을
`audit97.py` 로 닫았다. 같은 규율을 여기에도 적용한다.

    python3 scripts/compare_states.py out
    python3 scripts/compare_states.py pouch=out c168=~/dd/cells/c168/out \\
                                      c171=~/dd/cells/c171/out

읽는 것
  `degeneracy_<state>_<si>.json` — 근최적 집합 위의 LAM/LLI 폭 (모델 고정 축)
  `matrix_<state>.csv`           — 모델 선택(Si 8 종)이 만드는 폭 (다른 축)

⚠ 두 축은 **다른 것을 잰다.** 같은 표에 나란히 놓되 합치지 않는다.
⚠ `.meta.json` 이 있으면 설정을 같이 찍는다. 설정이 다른 행끼리는 비교 금지다.
"""
from __future__ import annotations
import csv, json, pathlib, re, sys

MODES = ("LAM_PE", "LAM_NE", "LLI")


#: 정본은 unversioned 이름 하나다. 2026-09-10 에는 `_v2` 가 정본이라 "최신 판" 을 골랐고 그날 옛 판을 읽고 쓴
#: 실수가 세 번 있었다 (README 의 8.93 %p, matlab/README 의 dump 표, 이 스크립트 첫 판). U14 가 `_v2` 를 unversioned
#: 이름으로 재현한 뒤에는 그 규칙이 거꾸로 meta 없는 옛 판을 고르게 했다 — 판 번호는 이제 역사 자료의 표지다.
VER = re.compile(r"_v(\d+)$")   # `_vN` = 옛 판 (역사 자료) — 정본이 아니다 (Codex R6-04)


def _canon_files(d: pathlib.Path, pattern: str, excluded: list | None = None):
    """정본은 **unversioned 이름 하나**다. `_vN` 이 붙은 파일이 out/ 에 남아 있으면 시끄럽게 건너뛴다.

    ⚠ Codex R6-04: "가장 높은 `_vN`" 규칙 때문에 U14 가 정본을 다시 만든 뒤에도 옛 `_v2`(meta 없음)를 골랐다 —
      새 서명·환경 필드가 소비 경로에 안 실렸다. 옛 판은 `out/archive/` 로 (`out/archive/README.md`)."""
    for f in sorted(d.glob(pattern)):
        if f.name.endswith(".meta.json"):
            continue
        if VER.search(f.stem):
            print(f"  ! {f.name}: 판 번호가 붙은 옛 산출 — 정본은 unversioned 이름 하나다; `out/archive/` 로 옮길 것 "
                  f"(Codex R6-04)", file=sys.stderr)
            if excluded is not None:
                excluded.append((f.name, "판 번호가 붙은 옛 산출 (정본 아님)"))
            continue
        yield f


def _read_unit(f: pathlib.Path, excluded: list | None = None):
    """산출 bytes 와 meta 를 한 번씩 읽어 서로 대조한 snapshot → (data, meta). 소비 금지면 (None, None).

    ⚠ R6 내부 F07 · Codex R6-01·02: 경로를 따로 검사하고 따로 읽으면 그 사이 끼어든 정상 게시가 검사를 통과해
      A 데이터에 B meta 가 붙는다. 표는 **이 함수가 돌려준 bytes 만** 소비한다. meta 가 없거나 옛 meta 면 산출이
      현행 schema(run_id 있음) 인 한 미완이다 — 옛 산출(run_id 없음)만 호환 경로로 읽는다."""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from provenance import read_unit
    ok, why, data, meta = read_unit(f)
    if ok is False:
        print(f"  ! {f.name}: 묶음 불일치/미완 ({why}) — 표에서 뺀다 (R6 내부 F07 · Codex R6-01·02)", file=sys.stderr)
        if excluded is not None:
            excluded.append((f.name, why))
        return None, None
    return data, meta


def load_degeneracy(d: pathlib.Path, excluded: list | None = None) -> dict:
    """⚠ Codex R7-01: 뺀 것은 **세어서 돌려줘야** 한다. `excluded` 를 주면 (파일, 이유) 가 쌓인다 — 집계가 "몇 개 중
    몇 개를 봤는가" 를 말할 수 있어야 남은 부분집합을 전체처럼 인증하지 않는다.

    ⚠ Codex R8-01: 전 판은 `out[state] = …` 라 같은 state 의 **다른 Si** 정상 묶음이 서로 덮었다 (Li 가 Kunz 를 지워
      1/1·예). inventory 를 먼저 만들고, state 에 Si 가 하나면 key 는 `state`(옛 소비자 호환), 둘 이상이면 그 state 의
      항목 전부를 `state|si` 로 둔다 — 아무것도 조용히 사라지지 않는다."""
    inventory: list = []
    for f in _canon_files(d, "degeneracy_*.json", excluded):
        m = re.match(r"degeneracy_(.+)_([A-Za-z]+)$", f.stem)
        if not m:
            continue
        data, meta = _read_unit(f, excluded)
        if data is None:
            continue
        try:
            j = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print(f"  ! {f.name} 이 JSON 이 아니다 — 중간에 죽은 산출인가?", file=sys.stderr)
            if excluded is not None:
                excluded.append((f.name, "JSON 이 아니다"))
            continue
        inventory.append((m.group(1), m.group(2), {"si": m.group(2), "j": j, "file": f.name, "meta": meta,
                                                   "run_id": j.get("run_id")}))
    per_state: dict = {}
    for st, si, _ in inventory:
        per_state.setdefault(st, []).append(si)
    out = {}
    for st, si, e in inventory:
        key = st if len(per_state[st]) == 1 else f"{st}|{si}"
        if key in out:                                             # 같은 (state, si) 가 둘 — 이름이 다를 수 없다
            raise RuntimeError(f"{d}: (state={st}, si={si}) 묶음이 둘이다 ({out[key]['file']}, {e['file']})")
        out[key] = e
    return out


def load_matrix_axis(d: pathlib.Path, excluded: list | None = None) -> dict:
    """`matrix_<state>.csv` 에서 **한 축만** 꺼낸다: 반쪽전지 하나 · dQ/dV 끔 · Si 8 종."""
    import io
    out = {}
    for f in _canon_files(d, "matrix_*.csv", excluded):
        st = f.stem[len("matrix_"):]
        data, meta = _read_unit(f, excluded)
        if data is None:
            continue
        all_rows = list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
        rows = [r for r in all_rows if r.get("w_dqdv") and float(r["w_dqdv"]) == 0]
        if not rows:
            continue
        by_src = {}
        for r in rows:
            by_src.setdefault(r["half_cell"], []).append(r)
        per = {}
        for src, rs in by_src.items():
            free = [r for r in rs if not (r.get("bounds") or "").strip("-")
                    and not (r.get("ref_bounds") or "").strip("-")]
            per[src] = {
                "n": len(rs), "n_free": len(free),
                **{k: (max(float(r[f"{k}_pct"]) for r in rs)
                       - min(float(r[f"{k}_pct"]) for r in rs)) for k in MODES},
                **{f"{k}_free": (max(float(r[f"{k}_pct"]) for r in free)
                                 - min(float(r[f"{k}_pct"]) for r in free))
                   if len(free) > 1 else None for k in MODES}}
        rids = {r.get("run_id") for r in all_rows}
        out[st] = {"per": per, "file": f.name, "meta": meta,
                   "run_id": next(iter(rids)) if len(rids) == 1 else None}
    return out


def main() -> int:
    args = sys.argv[1:] or ["out"]
    # ⚠ Codex R9-01: 전 판은 `roots[label] = path` 라 같은 label(암묵적 `out` 포함)의 뒤 인자가 앞 요청을 **지웠다** —
    #   `same=<없는 root> same=<정상 root>` 가 "요청한 root 1 개 · 1/1 · 예 rc 0" 이었고 label 없는 인자 여럿은 전부 `out`
    #   이 됐다. 인자는 순서 있는 목록이고, 중복 label 은 합치지 않고 **판정 전에** 거부한다 (무엇을 요청했는지 모르는
    #   채 판정하지 않는다).
    roots: list = []
    seen: dict = {}
    for a in args:
        label, _, path = a.partition("=")
        if not path:
            label, path = "out", label
        if label in seen:
            print(f"! root label `{label}` 이 중복이다 — 앞 {seen[label]} · 뒤 {path}. 두 요청을 하나로 합치지 않는다; "
                  f"root 마다 다른 label 을 줄 것 (`a=<dir> b=<dir>`) (Codex R9-01) → 판정 없음, 종료 코드 2")
            return 2
        seen[label] = path
        roots.append((label, pathlib.Path(path).expanduser()))

    print("=" * 78)
    print("A. 근최적 집합 위의 폭 — **모델을 고정**했을 때 데이터가 못 가르는 만큼")
    print("=" * 78)
    # ⚠ Codex R7-01: 이 플래그는 True 로 시작해서, 반례인 상태가 **미완으로 빠지면** "예" 로 뒤집혔다 (rc 0).
    #   독자가 미완을 정확히 거부하는 것과, 남은 부분집합을 전체처럼 인증하는 것은 다른 문제다. 후보·검증·제외를
    #   세고, 제외가 있거나 관측이 0 이면 전체 판정을 내지 않는다 (종료 코드도 그것을 말한다).
    ok_llI_narrowest = True
    census = {"candidates": 0, "verified": 0, "excluded": [], "roster": {}}
    for label, d in roots:
        exc: list = []
        # ⚠ Codex R8-01: 명시한 root 는 **하나하나** 후보다. 없거나 비어 있으면 그 root 는 관측 0 이고 전체 판정은
        #   미완이다 — 전 판은 빈 root 가 후보에 안 들어가 `good=… empty=…` 가 1/1·예 rc 0 이었다.
        if not d.is_dir():
            census["roster"][label] = {"dir": str(d), "exists": False, "candidates": 0, "verified": 0, "excluded": 0}
            print(f"\n[{label}] {d} — **디렉터리가 없다** (요청한 root 인데 관측 0)"); continue
        deg = load_degeneracy(d, excluded=exc)
        census["candidates"] += len(deg) + len(exc)
        census["verified"] += len(deg)
        census["excluded"] += [(label, n, why) for n, why in exc]
        census["roster"][label] = {"dir": str(d), "exists": True, "candidates": len(deg) + len(exc),
                                   "verified": len(deg), "excluded": len(exc)}
        if not deg:
            print(f"\n[{label}] {d} — degeneracy 산출 없음"
                  + (f" (제외 {len(exc)})" if exc else "")); continue
        print(f"\n[{label}] {d}")
        srcs = set()
        # ⚠ 2026-09-11 Codex R2-04: `best ± span/2` 는 best 를 중점처럼 보이게 한다.
        #   best 는 경계해에서 구간의 끝점이라 (c168 300_0009 LAM_NE: [2.30, 11.00] 을
        #   2.30±4.35 로 찍어 [−2.05, 6.65] 로 읽혔다) 산출의 min/max 를 그대로 찍는다.
        print(f"  {'state':12}{'src':10}{'LAM_PE best [min,max]':>25}{'LAM_NE':>25}{'LLI':>25}"
              f"  {'최광':7} 파일")
        for st, e in deg.items():
            j = e["j"]
            spans = {k: j[f"{k}_percent"]["span"] for k in MODES}
            best = j["best_modes_percent"]
            widest = max(spans, key=spans.get)
            narrow = min(spans, key=spans.get)
            if narrow != "LLI":
                ok_llI_narrowest = False
            src = j.get("half_cell", "?")
            srcs.add(src)
            cells = "".join(f"{best[k]:8.2f} [{j[f'{k}_percent']['min']:.2f}, "
                            f"{j[f'{k}_percent']['max']:.2f}]".rjust(25) for k in MODES)
            print(f"  {st:12}{src:10}{cells}  {widest:7} {e['file']}")
            b = j.get("best_active_bounds") or []
            rb = j.get("ref_active_bounds") or []
            if b or rb:
                print(f"  {'':12}⚠ 경계 — 대상 {b or '—'} · 기준 {rb or '—'}")
            if e["meta"] and e["meta"].get("starts", 24) < 24:
                print(f"  {'':12}⚠ starts={e['meta']['starts']} — 시험 산출이다")
        if len(srcs) > 1:
            print(f"  ⚠ **반쪽전지 소스가 섞였다** ({', '.join(sorted(srcs))}) — 이 표의")
            print(f"    상태들을 서로 비교하지 마라. 소스가 바뀌면 `E_PE` 가 바뀌고")
            print(f"    그러면 LAM_PE 가 다른 것을 재게 된다 (`prepare_cell.py` 머리말 2번).")
            print(f"    같은 소스끼리만 묶어서 읽을 것.")

    print("\n" + "=" * 78)
    print("B. 모델 선택(Si 8 종)이 만드는 폭 — **다른 축**이다. 위와 합치지 말 것")
    print("=" * 78)
    for label, d in roots:
        mx_exc: list = []
        mx = load_matrix_axis(d, excluded=mx_exc)
        census["excluded"] += [(label, n, why) for n, why in mx_exc]
        if not mx:
            print(f"\n[{label}] matrix 산출 없음"); continue
        print(f"\n[{label}]")
        print(f"  {'state':12}{'source':11}{'n':>3}{'자유':>5}"
              f"{'LAM_PE':>9}{'LAM_NE':>9}{'LLI':>9}{'LLI(자유)':>11}   파일")
        for st, e in mx.items():
            for src, v in e["per"].items():
                fr = v["LLI_free"]
                print(f"  {st:12}{src:11}{v['n']:>3}{v['n_free']:>5}"
                      f"{v['LAM_PE']:>9.3f}{v['LAM_NE']:>9.3f}{v['LLI']:>9.3f}"
                      f"{(f'{fr:.3f}' if fr is not None else '—'):>11}"
                      f"   {e['file']}")

    print("\n" + "=" * 78)
    print("판정")
    print("=" * 78)
    n_cand, n_ok, exc = census["candidates"], census["verified"], census["excluded"]
    print(f"  대조에 쓴 degeneracy 산출: **{n_ok}/{n_cand}** (제외 {len(exc)})")
    for label, name, why in exc:
        print(f"    - [{label}] {name}: {why}")
    # 요청한 root roster — 각 root 가 실제로 관측을 냈는가 (Codex R8-01)
    hollow = [lab for lab, r in census["roster"].items() if not r["exists"] or r["verified"] == 0]
    print(f"  요청한 root {len(census['roster'])} 개 roster:")
    for lab, r in census["roster"].items():
        print(f"    - {lab}: {'있음' if r['exists'] else '**없음**'} · 후보 {r['candidates']} · 검증 {r['verified']}"
              f" · 제외 {r['excluded']}" + ("  ← 관측 0" if lab in hollow else ""))
    if exc or not n_ok or hollow:
        # 반례가 빠진 채 "예" 를 내면 그것이 곧 오인증이다 (Codex R7-01). 부분집합에서 본 것은 범위를 붙여 말한다.
        # 판정 줄의 머리는 그대로 둔다 (도구가 이 줄을 잡는다) — 다만 **절대 "예" 로 끝나지 않는다**
        if n_ok:
            why = (f"제외 {len(exc)} 건" if exc else "") + (" · " if exc and hollow else "") + \
                  (f"관측 0 인 요청 root {hollow}" if hollow else "")
            print(f"  A 축에서 LLI 가 **항상 가장 좁은가**: **미완** — {why} 이 있어 전체 조건을 "
                  f"말할 수 없다. 관측한 {n_ok}/{n_cand} 개 안에서는 LLI 가 "
                  f"{'항상 가장 좁았다' if ok_llI_narrowest else '**항상 가장 좁지는 않았다**'} (그 범위의 진술이다).")
        else:
            print("  A 축에서 LLI 가 **항상 가장 좁은가**: **미완** — 검증된 관측이 0 개다 "
                  "(빈 디렉터리이거나 전부 제외됐다).")
        print("  미완을 닫는 법: 제외된 산출의 게시를 끝내거나(meta 포함) 다시 돌린 뒤 이 명령을 다시 부른다.")
        print("  ⚠ 상대 불확실성(폭/최적값)은 열화가 쌓이면 분모가 커져 작아진다.")
        print("     상태를 가로질러 말할 때는 **절대 폭(%p)** 으로 말할 것.")
        return 2                                    # 2 = 미완 (eval --compare 와 같은 뜻)
    print(f"  A 축에서 LLI 가 **항상 가장 좁은가**: "
          f"{'예' if ok_llI_narrowest else '**아니오** — 상태에 따라 뒤집힌다'}")
    print("  ⚠ 상대 불확실성(폭/최적값)은 열화가 쌓이면 분모가 커져 작아진다.")
    print("     상태를 가로질러 말할 때는 **절대 폭(%p)** 으로 말할 것.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
