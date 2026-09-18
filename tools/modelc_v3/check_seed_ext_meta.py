#!/usr/bin/env python3
"""check_seed_ext_meta.py — 시드 확장이 **정말 같은 조건인가** (verified-carry 가드).

기존 s2 의 `run_meta.json` 을 읽어 구조·온도·길이·창·실행모드를 대조한다.
하나라도 다르면 **시드 확장이 아니라 다른 계산**이므로 멈춘다.

왜 파일로 뺐나 (2026-09-18)
  종전엔 `run_box331_seed_extension.sh` 의 heredoc 안에 있었다. 그러면
  **시험을 칠 수가 없다.** 이 가드를 한 번 느슨하게 푸는 일이 생겼고
  (아래 legacy 조항), 음성 시험 없이 가드를 푸는 것은 "조용히 틀린 경로" 의
  입구다. 파일로 빼서 `--selftest` 를 달았다.

⛔ 이 도구가 **못 하는 것**
  · 물리를 보지 않는다 — run_meta 의 **선언**만 본다. 실제로 그 설정으로
    돌았는지는 모른다 (드라이버가 거짓말하면 못 잡는다).
  · 게이트 판정(C1–C6)을 하지 않는다. 그건 사전등록 카드 몫이다.
  · run_meta 가 없으면 **통과시킨다** (첫 실행일 수 있다) — 부르는 쪽이 경고한다.

  python3 tools/modelc_v3/check_seed_ext_meta.py <ref_run_meta.json> <v0.xyz> [turbo]
  python3 tools/modelc_v3/check_seed_ext_meta.py --selftest
"""
import json
import os
import sys

#: 실행모드 필드 둘. 커밋 5970c52da (2026-09-11) 가 `--turbo` 와 **이 기록 기능을
#: 같이** 넣었다 — 그래서 "둘 다 없음" 은 그 커밋 이전 판본이라는 **증거**다.
MODE_REQ, MODE_ACT = "uma_inference_mode_requested", "uma_inference_mode"


def compare(meta: dict, v0_basename: str, mode: str) -> tuple[list, list]:
    """(어긋난 것들, 화면에 낼 참고줄). 빈 목록이면 통과."""
    want = {"temperatures": [600, 800, 1000], "prod_ps": 400.0, "equilib_ps": 5.0,
            "fit_window_ps": [2.0, 50.0], "save_traj": True,
            "uma_model": "uma-s-1p1", MODE_REQ: mode}
    notes = []
    # ⭐ **필드 부재는 "다른 설정" 이 아니라 "옛 판본" 이다** (2026-09-18).
    #   lpsocl 9런의 run_meta 에는 두 필드가 **둘 다 없다**. 커밋 5970c52da 가
    #   turbo 경로와 기록 기능을 같이 넣었으므로, 둘 다 없는 파일은 그 이전
    #   판본이 썼고 그 판본엔 turbo 가 **없다** ⇒ 구성상 default.
    #   추론이 아니라 **부재가 증명하는 사실**이다.
    # ⛔ 좁게만 연다:
    #   · 두 필드가 **모두** 부재일 때만 (한쪽만 있으면 안 된다)
    #   · 명시적 null 은 안 된다 (기록은 됐는데 값이 없는 건 다른 사건이다)
    #   · 이번에 원하는 것이 **default** 일 때만 — 옛 런을 turbo 라고
    #     주장하는 것은 근거가 정반대다
    if MODE_REQ not in meta and MODE_ACT not in meta and mode == "default":
        notes.append("⭐ 기존 run_meta 에 실행모드 필드가 **둘 다 없다** → 커밋 5970c52da"
                     "(2026-09-11, --turbo 와 기록 기능 동시 도입) 이전 판본이다."
                     " 그 판본엔 turbo 경로가 없으므로 **구성상 default** 로 본다.")
        want.pop(MODE_REQ)
    bad = []
    for k, v in want.items():
        got = meta.get(k)
        if isinstance(v, list) and isinstance(got, list):
            ok = [float(x) for x in got] == [float(x) for x in v]
        elif isinstance(v, float):
            ok = got is not None and float(got) == v
        else:
            ok = got == v
        if not ok:
            bad.append(f"  {k}: 기존 {got!r} ≠ 이 스크립트 {v!r}")
    if os.path.basename(str(meta.get("v0_xyz", ""))) != v0_basename:
        bad.append(f"  v0_xyz: 기존 {meta.get('v0_xyz')} ≠ {v0_basename}")
    return bad, notes


def _base(**over) -> dict:
    d = {"temperatures": [600.0, 800.0, 1000.0], "prod_ps": 400.0, "equilib_ps": 5.0,
         "fit_window_ps": [2.0, 50.0], "save_traj": True, "uma_model": "uma-s-1p1",
         "v0_xyz": "db/structures/x_relaxV0_3x3x1.xyz"}
    d.update(over)
    return d


def selftest() -> int:
    bad = []

    def chk(c, m):
        print(("  ✓ " if c else "  ⛔ ") + m)
        if not c:
            bad.append(m)

    V0 = "x_relaxV0_3x3x1.xyz"
    # ① 양성 — 옛 판본(두 필드 부재) + default 요청 → 통과, 사유를 화면에 낸다
    b, n = compare(_base(), V0, "default")
    chk(b == [] and n and "5970c52da" in n[0],
        f"[양성] 두 필드 부재 + default → 통과하고 근거를 적는다 ({b})")
    # ② ⛔음성 — 같은 파일에 **turbo** 를 요청하면 **막는다**
    b, _ = compare(_base(), V0, "turbo")
    chk(any(MODE_REQ in x for x in b),
        "⛔음성: 두 필드 부재인데 **turbo 라고 주장**하면 막는다 (근거가 정반대다)")
    # ③ ⛔음성 — 명시적 null 은 부재가 아니다
    b, _ = compare(_base(**{MODE_REQ: None}), V0, "default")
    chk(any(MODE_REQ in x for x in b),
        "⛔음성: 명시적 null 은 **부재가 아니다** — 기록은 됐는데 값이 없는 건 다른 사건")
    # ④ ⛔음성 — 한쪽만 있으면 열지 않는다
    b, _ = compare(_base(**{MODE_ACT: "turbo"}), V0, "default")
    chk(any(MODE_REQ in x for x in b),
        "⛔음성: 한쪽 필드만 있으면 **옛 판본이 아니다** — 열지 않는다")
    # ⑤ 양성 — 둘 다 turbo 로 기록된 런에 turbo 요청
    b, n = compare(_base(**{MODE_REQ: "turbo", MODE_ACT: "turbo"}), V0, "turbo")
    chk(b == [] and n == [], "[양성] turbo 런 + turbo 요청 → 통과, 예외조항 안 탄다")
    # ⑥ ⛔음성 — turbo 런에 default 요청은 막는다 (실행모드를 섞는 것)
    b, _ = compare(_base(**{MODE_REQ: "turbo", MODE_ACT: "turbo"}), V0, "default")
    chk(any(MODE_REQ in x for x in b), "⛔음성: turbo 런에 default 요청 → 막는다")
    # ⑦ ⛔음성 — 예외조항이 **다른 필드까지 봐주지 않는다**
    b, _ = compare(_base(prod_ps=200.0), V0, "default")
    chk(any("prod_ps" in x for x in b),
        "⛔음성: 예외조항을 타도 prod_ps 같은 **다른 어긋남은 그대로 막는다**")
    # ⑧ ⛔음성 — 구조가 다르면 막는다
    b, _ = compare(_base(), "other_relaxV0_3x3x1.xyz", "default")
    chk(any("v0_xyz" in x for x in b), "⛔음성: v0_xyz 가 다르면 막는다")

    print("selftest PASS" if not bad else f"selftest FAIL ({len(bad)})")
    return 0 if not bad else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    ref, v0 = sys.argv[1], sys.argv[2]
    mode = (sys.argv[3] if len(sys.argv) > 3 else "") or "default"
    meta = json.load(open(ref, encoding="utf-8"))
    bad, notes = compare(meta, os.path.basename(v0), mode)
    for n in notes:
        print("  " + n)
    if bad:
        print("⛔ 기존 런과 조건이 다르다 — 시드 확장이 아니라 다른 계산이 된다:")
        print("\n".join(bad))
        return 1
    print(f"  ✓ 기존 s2 와 조건 일치 (n_atoms {meta.get('n_atoms')} · "
          f"supercell {meta.get('supercell')} · 실행모드 {mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
