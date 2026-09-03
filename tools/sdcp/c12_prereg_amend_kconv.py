#!/usr/bin/env python3
"""사전등록 개정 적용기 — δ_k 축 설계 제외 (렌즈2 P0-1 · 렌즈4 P0-2 · 렌즈5 P1-1, 2026-09-03).

⛔ 1저자 결정(A/B/C) 과 "비준" 없이는 돌리지 않는다.

  python3 tools/sdcp/c12_prereg_amend_kconv.py --variant A            # 개정안 삽입 (status proposed)
  python3 tools/sdcp/c12_prereg_amend_kconv.py --variant A --ratify   # + ratification 갱신 (1저자 "비준" 뒤에만)

무엇을 바꾸나
  db/properties/sdcp_c12_claim_prereg_2026_08_31.json
    3_오차예산.축_설계_제외_2026_09_03  ← 새 항 (구조 필드 = 생성기 --no_kconv 가 그대로 복사)
    status_history                     ← proposed (+ ratified)
    ratification                       ← --ratify 때 content_digest 재계산
  db/governance/decisions.json
    D-2026-09-03-sdcp-c12-kconv-axis-excluded ← 새 결정 (proposed → --ratify 때 active)
"""
import argparse, hashlib, json, pathlib, subprocess, sys, datetime

# ⚠ `db` 만 보고 올라가면 **`tools/db/` 에서 멈춘다** (실측 2026-09-03 — 그 상태로 돌리면
#   없는 경로를 읽어 죽는다). 우리가 쓰는 두 하위 디렉터리를 **둘 다** 요구한다.
REPO = pathlib.Path(__file__).resolve()
while not ((REPO / "db" / "properties").is_dir() and (REPO / "db" / "governance").is_dir()):
    REPO = REPO.parent
    if REPO == REPO.parent:
        raise SystemExit("repo 루트를 못 찾았다 (db/properties + db/governance 가 있는 곳)")
PRE = REPO / "db/properties/sdcp_c12_claim_prereg_2026_08_31.json"
DEC = REPO / "db/governance/decisions.json"
KEY = "축_설계_제외_2026_09_03"
DEC_ID = "D-2026-09-03-sdcp-c12-kconv-axis-excluded"
BY = "yonghoon7153@gmail.com"

COMMON = {
    "축": "δ_k",
    "결정": ("δ_k(k 격자 수렴, static 3×4×1 → dense 4×6×1) 축을 **설계에서 뺀다**. dense 2잡이 최장 잡을 "
             "299.6 h 로 만들어 전체 일정을 12.5일로 끌었다 (vasp_cost_estimate 실측: dense 200 h + static 100 h). "
             "static 만이면 최장 111 h · 동시 8잡 기준 8.16일."),
    "50행과의_관계": ("50행 '축이 하나라도 없으면 NUMERIC_BUDGET_INCOMPLETE' 는 **설계에 있는 축이 결측일 때**의 규칙으로 "
                      "읽는다. 설계에서 뺀 축은 '결측' 이 아니라 '미설계' 다 — 분석기가 `axes_not_designed` 로 따로 세고 "
                      "`B_num` 은 시험한 두 축(Δ_vac·δ_gas)만 합산한다. ⚠ 이 재해석은 2026-09-02 비준 이후의 것이라 "
                      "여기서 명시적으로 비준한다. 비준 전 번들(v32–v34)은 이 항 없이 같은 경로를 열었다 — 발송하지 않았다."),
    "잃는_것": ("'전체 값의 0.01 eV 안정성' 을 주장하지 않는다 (`overall_citable_at_0.01eV=False`). 시험한 두 축의 "
                "envelope 만 말한다. `rounded_value_under_tested_axes_eV` 는 '시험한 축 기준' 이라는 한정어를 원고에서 "
                "떼어내지 않는다. verdict 문자열에 '사전등록 축 없음(δ_k)' 꼬리가 붙는다."),
    "⚠_UMA_로_미리_판단_금지": ("조각 간 UMA 비교는 무효(오프셋 sdcp ~1.070 vs ptfe ~0.167 eV · 차등 0.90 eV). "
                                 "|ΔE_ads| 가 클 것이라 가정하지 않는다."),
    "구현": ("tools/sdcp/vasp_handoff_bundle.py — 생성기 `--no_kconv` 가 이 항의 재개 조건을 MANIFEST.kconv_pair 로 "
             "**복사**하고(하드코딩 금지), 분석기는 번들에 실린 이 문서 사본에서 이 항을 읽어 있을 때만 not_designed 경로를 "
             "연다 (없으면 KCONV_OMISSION_UNRATIFIED · 다르면 KCONV_OMISSION_DRIFT). 재개 조건은 D_raw_eV 에 기계로 대어 "
             "`kconv_omission.reopen_eval` 에 남는다 (렌즈2 P1-2)."),
}

VARIANTS = {
    # A — 재개 없음. 프로토콜 §7(|D|<0.05 미해결)·§8(확장 금지) 우선. 경계면 자문만.
    "A": {
        "규칙": ("재개하지 않는다. |D_raw| < 0.05 eV 는 프로토콜 §7 미해결 · §8 '계산을 확장하지 않는다'. "
                 "|D_raw| ≥ 0.05 eV 면 k 가드밴드(0.01 eV)가 부호·판정을 못 바꾼다. 경계 구간 "
                 "0.05 ≤ |D_raw| < 0.06 eV 에서는 분석기가 KCONV_UNTESTED_AXIS_AT_THRESHOLD 자문을 내고 "
                 "원고는 '미시험 축에 판정이 민감하다' 를 적는다 — 계산은 추가하지 않는다."),
        "판정량": "D_raw_eV",
        "문턱_eV": 0.05,
        "가드밴드_eV": 0.01,
        "비교": "boundary",
        "충족시": "자문만 (KCONV_UNTESTED_AXIS_AT_THRESHOLD) — dense 추가 없음 · 원고에 민감성 명시",
        "⛔_사후변경_금지": ("이 조건은 결과를 보기 전에 선언했다. 이 밖의 이유로 dense 를 추가하면 '결과를 보고 "
                             "게이트를 바꾼 것' 이다."),
    },
    # B — 경계 구간(0.05 ≤ |D_raw| < 0.06) 에서만 dense 2잡 추가 (새 번들·봉인·merge 절차 필요).
    "B": {
        "규칙": ("0.05 ≤ |D_raw| < 0.06 eV(문턱 ± k 가드밴드) 이면 dense 2잡(estimand_job_keys 의 E_C_sdcp·E_C_control)을 "
                 "**별도 번들**로 추가해 δ_k 를 실측한다. |D_raw| < 0.05 eV 는 프로토콜 §7 미해결 · §8 확장 금지 — "
                 "재개 대상이 아니다. |D_raw| ≥ 0.06 eV 면 추가하지 않는다."),
        "판정량": "D_raw_eV",
        "문턱_eV": 0.05,
        "가드밴드_eV": 0.01,
        "비교": "boundary",
        "충족시": "dense 2잡을 별도 번들(새 MANIFEST·봉인)로 추가 — 절차 문서 필요 (기존 번들 MANIFEST 변경 금지)",
        "⛔_사후변경_금지": ("이 조건은 결과를 보기 전에 선언했다. 이 밖의 이유로 dense 를 추가하면 '결과를 보고 "
                             "게이트를 바꾼 것' 이다."),
    },
}


def prereg_digest(doc):
    c = {k: v for k, v in doc.items() if k != "ratification"}
    return hashlib.sha256(json.dumps(c, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def dec_digest(x):
    c = {k: v for k, v in x.items() if k != "ratification"}
    return hashlib.sha256(json.dumps(c, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _selftest():
    """⛔ 음성 포함. 양성만 있는 selftest 는 통과해도 아무것도 보증하지 못한다 (CLAUDE.md)."""
    import copy, tempfile
    n = [0, 0]

    def chk(c, m):
        n[0] += 1
        n[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    # 🔴 렌즈6′ P0 회귀 — 기록 digest 가 **최종 문서**의 것이어야 한다.
    doc = {"schema": "x", "3_오차예산": {"정의": "B"}, "status": "proposed",
           "status_history": [{"at": "2026-09-02", "state": "ratified"}]}
    d2 = copy.deepcopy(doc)
    d2["status_history"].append({"at": "2026-09-03", "state": "ratified"})
    d2["status"] = "ratified"
    d2["ratification"] = {"state": "ratified", "content_digest": prereg_digest(d2)}
    chk(prereg_digest(d2) == d2["ratification"]["content_digest"],
        "양성: 문서를 다 고친 뒤 계산한 digest 는 최종 문서와 일치한다")
    d3 = copy.deepcopy(doc)
    _early = prereg_digest(d3)                       # ← 종전 버그: 먼저 계산
    d3["status_history"].append({"at": "2026-09-03", "state": "ratified"})
    d3["status"] = "ratified"
    d3["ratification"] = {"state": "ratified", "content_digest": _early}
    chk(prereg_digest(d3) != _early,
        "⛔음성 렌즈6′ P0: digest 를 **먼저** 뽑고 status/history 를 고치면 어긋난다 "
        "(종전 코드가 이것이었다 — 외주처 --check_governance rc 2)")
    chk(prereg_digest({"a": 1, "ratification": {"x": 1}}) == prereg_digest({"a": 1}),
        "digest 는 ratification 칸을 뺀 내용의 것이다")
    # 재개 조건이 분석기 형식 검사(_kconv_reopen_rule_problems)를 통과하는 모양인가
    for v, r in VARIANTS.items():
        chk(str(r.get("판정량")) == "D_raw_eV" and r.get("비교") in ("abs_lt", "boundary", "none")
            and float(r.get("문턱_eV")) > 0 and str(r.get("충족시") or "").strip(),
            "안 %s 의 재개 조건이 기계 평가 구조를 갖췄다 (판정량·비교·문턱·충족시)" % v)
        chk(r.get("비교") != "boundary" or float(r.get("가드밴드_eV", 0)) > 0,
            "⛔음성: boundary 안 %s 는 가드밴드가 있어야 한다" % v)
    chk(all(str(r.get("판정량")) != "rounded_value_under_tested_axes_eV"
            for r in VARIANTS.values()),
        "⛔음성: 판정량으로 **반올림값**을 쓰지 않는다 (결과 보고 값을 고를 여지)")
    # ⛔ 경로 해석 — **건너뛰지 않는다.** `db` 만 보고 올라가면 `tools/db/` 에서 멈춰
    #   없는 파일을 가리켰고, 종전 selftest 는 `if PRE.is_file()` 로 그것을 조용히 건너뛰었다.
    chk(PRE.is_file() and DEC.is_file(),
        "repo 루트 해석이 맞다 (%s · %s)" % (PRE.is_file(), DEC.is_file()))
    chk(PRE.parent.name == "properties" and DEC.parent.name == "governance"
        and PRE.parts[-3] == "db",
        "대상 경로가 db/properties · db/governance 다 (%s)" % PRE)
    if PRE.is_file():
        # 실물 문서에 적용해도 위 불변량이 서는가 (사본 · repo 미변경)
        real = json.loads(PRE.read_text(encoding="utf-8"))
        real["3_오차예산"][KEY] = {"축": "δ_k"}
        real["status_history"].append({"at": "T", "state": "ratified"})
        real["status"] = "ratified"
        real.pop("ratification", None)
        real["ratification"] = {"content_digest": prereg_digest(real)}
        chk(prereg_digest(real) == real["ratification"]["content_digest"],
            "실물 사전등록 사본에서도 성립한다 (repo 는 안 건드린다)")
    print("selftest %d/%d · %s" % (n[1], n[0], "PASS" if n[1] == n[0] else "FAIL"))
    return 0 if n[1] == n[0] else 1


def main():
    ap = argparse.ArgumentParser()
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--variant", choices=sorted(VARIANTS), required=True)
    ap.add_argument("--ratify", action="store_true", help="1저자 '비준' 뒤에만")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    today = a.date
    now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()

    pre = json.loads(PRE.read_text(encoding="utf-8"))
    sec = pre["3_오차예산"]
    entry = dict(COMMON)
    entry["재개_조건_결과_보기_전에_선언"] = dict(VARIANTS[a.variant])
    entry["선택한_안"] = a.variant
    sec[KEY] = entry
    hist = pre.setdefault("status_history", [])
    if not any(h.get("at") == today and "축_설계_제외" in str(h.get("note", "")) for h in hist):
        hist.append({"at": today, "state": "proposed",
                     "note": ("δ_k 축 설계 제외 + 재개 조건(안 %s) 을 3_오차예산.%s 로 추가 — 렌즈2 P0-1 · 렌즈4 P0-2 · "
                              "렌즈5 P1-1 이 '비준 문서 이탈 · 원장 부재' 를 잡았다. v32–v34 는 이 항 없이 생성됐고 "
                              "발송되지 않았다. ⚠ 비준은 사람 몫." % (a.variant, KEY))})
    if a.ratify:
        # 🔴🔴 렌즈6′ P0 (2026-09-03) — **digest 는 문서를 다 고친 뒤에 계산한다.**
        #   종전엔 digest 를 먼저 뽑고 그 다음에 status_history 와 status 를 바꿔서,
        #   기록된 content_digest 가 최종 문서와 어긋났다. 그러면 ref_doc_state 가
        #   "비준 이후 내용이 바뀌었다" 로 읽어 ratified=False → 그 사전등록으로 만든
        #   번들은 외주처 --check_governance 에서 rc 2 (한 잡도 못 돈다).
        hist.append({"at": today, "state": "ratified",
                     "note": "1저자 비준 (scientific_owner) — δ_k 설계 제외 · 재개 조건 안 %s. DFT 결과 0잡 시점." % a.variant})
        pre["status"] = "ratified"
        pre.pop("ratification", None)          # 지문은 ratification 을 뺀 내용의 것이다
        pre["ratification"] = {
            "state": "ratified", "role": "scientific_owner", "at": today, "by": "1저자",
            "content_digest": prereg_digest(pre),      # ← 마지막에, 최종 내용으로
            "actor_id": BY, "timestamp": now, "commit": head,
            "⛔_무엇에_대한_비준인가": ("이 문서에서 `ratification` 을 뺀 내용의 sha256 이다. "
                                        "한 글자라도 바뀌면 지문이 달라지고 게이트가 재승인을 "
                                        "요구한다 — 비준을 받아 놓고 내용을 고치는 경로를 닫는다."),
        }
        # 자기검사 — 기록한 지문이 최종 문서와 **정말** 같은가 (P0 회귀)
        _re = str(pre["ratification"]["content_digest"])
        if _re != prereg_digest(pre):
            raise SystemExit("⛔ 내부 오류: 기록 digest ≠ 최종 문서 digest (렌즈6′ P0 회귀)")
    else:
        pre["status"] = "proposed"
    PRE.write_text(json.dumps(pre, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    dec = json.loads(DEC.read_text(encoding="utf-8"))
    ds = dec["decisions"]
    ds = [d for d in ds if d.get("id") != DEC_ID]
    d = {
        "id": DEC_ID, "schema_version": 2, "kind": "gate", "scope": "sdcp.c12.error_budget",
        "slot": "kconv_axis_design_exclusion",
        "decision_state": "active" if a.ratify else "proposed",
        "status": "active" if a.ratify else "proposed",
        "applies_to": {"systems": ["sdcp_neutral", "ptfe_c10"], "tasks": ["fragment_contrast"],
                       "methods": ["vasp-544__pbe-u62__mlip-geom-sp"], "use_cases": ["manuscript", "closure"]},
        "title": "C-12 δ_k(k 수렴) 축 설계 제외 + 결과 보기 전 재개 조건 (안 %s)" % a.variant,
        "statement": (entry["결정"] + " 재개 조건: " + VARIANTS[a.variant]["규칙"]),
        "rationale": ("렌즈2 P0-1 · 렌즈4 P0-2 · 렌즈5 P1-1 (2026-09-03): v32–v34 는 사전등록 49행('넘으면')을 근거로 "
                      "δ_k 를 뺐지만 적용 조항은 50행(축 부재 = INCOMPLETE)이고 원장에 기록이 없었다. 종전 재개 조건 "
                      "'|ΔE_ads| < 50 meV → dense 추가' 는 비준 프로토콜 §7·§8 과 정반대였다. 이 결정으로 예외를 "
                      "명시적으로 비준하고 재개 조건을 프로토콜과 정합하게 다시 선언한다."),
        "supersedes": [],
        "depends_on": ["D-2026-08-30-sdcp-c12-path"],
        "record": "db/properties/sdcp_c12_claim_prereg_2026_08_31.json#3_오차예산.%s" % KEY,
        "protocol_ref": "db/properties/sdcp_c12_protocol_2026_08_30.json",
        "review": "kb/reviews/internal_lens_review_c12_v34_2026_09_03.md",
        "method_ref": "tools/sdcp/vasp_handoff_bundle.py (--no_kconv · _prereg_axis_exclusion · _kconv_reopen_eval)",
        "enforcement": ("분석기: 번들 사전등록 사본에 이 항이 없으면 KCONV_OMISSION_UNRATIFIED, MANIFEST 재개 조건이 항과 "
                        "다르면 KCONV_OMISSION_DRIFT, 형식 불량이면 KCONV_OMISSION_UNDECLARED — 모두 estimand 차단. "
                        "재개 조건은 D_raw_eV 에 기계 평가돼 reopen_eval 로 남는다. preflight(--check_governance)에서도 정적 검사."),
        "citable": "no",
        "citable_why": "DFT 결과 0잡 시점. 결과가 나오면 시험한 두 축 조건부로만 보고한다.",
        "date": today,
        "registered_at": today, "registered_by": "agent (1저자 결정 %s 반영)" % a.variant,
        "status_history": [{"at": today, "state": "proposed", "note": "렌즈2·4·5 P0/P1 반영 등록 — 비준은 사람 몫"}],
    }
    if a.ratify:
        d["status_history"].append({"at": today, "state": "active", "note": "1저자 비준 (scientific_owner). 계산 전에 닫았다."})
        d["ratification"] = {
            "state": "ratified", "role": "scientific_owner", "actor_id": BY, "timestamp": now, "commit": head,
            "decision_digest": "sha256:" + dec_digest(d),
            "⚠_digest_의_뜻": "이 지문은 `ratification` 을 뺀 결정 내용의 sha256 이다. 비준 뒤 내용을 고치면 지문이 어긋나 검사가 재승인을 요구한다.",
            "근거": "렌즈2·4·5 (2026-09-03) 가 공통으로 '비준 문서 이탈 · 원장 부재' 를 잡았다. 1저자가 안 %s 를 택해 비준했다." % a.variant,
        }
    ds.append(d)
    dec["decisions"] = ds
    DEC.write_text(json.dumps(dec, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("→ %s : 3_오차예산.%s (안 %s) · status %s" % (PRE.name, KEY, a.variant, pre["status"]))
    print("→ %s : %s (%s)" % (DEC.name, DEC_ID, d["decision_state"]))
    if a.ratify:
        print("   prereg content_digest =", pre["ratification"]["content_digest"])
        print("   decision_digest       =", d["ratification"]["decision_digest"])


if __name__ == "__main__":
    main()
