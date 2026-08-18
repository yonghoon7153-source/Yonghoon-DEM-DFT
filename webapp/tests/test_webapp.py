#!/usr/bin/env python3
"""test_webapp.py — 리뷰(2026-08-07)의 완료 판정 기준을 **자동 검사**로 굳힌다.

왜 이 파일인가
  이 앱은 주석에 과거 회귀를 잔뜩 적어 두는데, 정작 같은 문제가 다시 생기는 걸 막는
  코드는 없었다(리뷰 P2). 여기 담은 건 전부 **실제로 한 번 터졌던 것**들이다.

    pytest webapp/tests/test_webapp.py -q
    python3 webapp/tests/test_webapp.py          # pytest 없이도 돈다
"""
import io
import json
import pytest
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A          # noqa: E402
import canonical as C    # noqa: E402
import data as D         # noqa: E402


# ── 1) 정본 레지스트리 ↔ 원자료 ─────────────────────────────────────────────
def test_registry_matches_sources():
    """레지스트리 값이 source_path/source_key 가 가리키는 원자료와 같아야 한다."""
    bad = C.validate(C.load_registry())
    assert not bad, "원자료와 어긋남:\n" + "\n".join(
        f"  {e.get('metric')}/{e.get('system')}: {w}" for e, w in bad)


def test_no_hardcoded_canonical_numbers():
    """정본 숫자가 data.py 로 되돌아오면 안 된다 — 그게 원래의 drift 원인이었다."""
    src = (ROOT / "webapp" / "data.py").read_text(encoding="utf-8")
    m = re.search(r"^CANONICAL\s*=\s*\{[^}]", src, re.M)
    assert m is None, "data.py 에 CANONICAL 딕셔너리 리터럴이 다시 생겼다 — 레지스트리를 쓸 것"


def test_canonical_entries_have_provenance():
    """status=canonical 이면 반드시 출처와 비교 묶음이 있어야 한다."""
    for e in C.load_registry()["entries"]:
        if e.get("status") != "canonical":
            continue
        assert e.get("source_path") and e.get("source_key"), f"{e['metric']}/{e['system']} 출처 없음"
        assert e.get("comparison_group"), f"{e['metric']}/{e['system']} comparison_group 없음"
        assert e.get("method_id"), f"{e['metric']}/{e['system']} method_id 없음"


# ── 2) 프로토콜 혼합 금지 (이번 리뷰의 핵심) ────────────────────────────────
def test_md_ea_groups_are_separated():
    """단일시드 앵커와 멀티시드 정본이 같은 비교 묶음에 있으면 안 된다."""
    reg = C.load_registry()
    multi = C.canonical_map(reg, "MD_Ea_eV", group="md-ea-multiseed-v1")
    single = C.canonical_map(reg, "MD_Ea_eV_singleseed", group="md-ea-singleseed-anchor-v1")
    assert set(multi) and set(single)
    for e in C.entries(reg, "MD_Ea_eV", group="md-ea-multiseed-v1"):
        assert (e.get("n_seed") or 0) >= 3, f"{e['system']} 이 멀티시드 묶음에 있는데 n_seed={e.get('n_seed')}"
    # 옛 버그의 정확한 형태: modelc 단일시드 0.224 가 멀티시드 묶음에 섞여 있던 것
    assert abs(multi.get("modelc", 0) - 0.197) < 1e-6, "modelc 멀티시드 값이 아니다"


def test_md_ea_beta_gate_blocks_canonical():
    """★ n_seed 만 보면 β 게이트 탈락을 못 잡는다 (2026-08-07 Codex 재검증).

    LPSOCl 은 4-seed 라 n_seed 검사는 통과하는데, 600 K β=0.615 가 Fickian 게이트를
    못 넘어 kb/open_items.md 가 인용 보류로 묶어 둔 값이다. 숫자가 db 와 맞아도
    정본이 아니다 — 게이트를 별도 축으로 검사한다.
    """
    reg = C.load_registry()
    for e in reg["entries"]:
        if e.get("blocking_gate"):
            assert e.get("status") != "canonical", \
                f"{e['metric']}/{e['system']} 이 게이트({e['blocking_gate']}) 미통과인데 canonical 이다"
    lp = [e for e in reg["entries"]
          if (e["metric"], e["system"]) == ("MD_Ea_eV", "lpsocl")]
    assert lp and lp[0]["status"] != "canonical", "LPSOCl Ea 가 다시 canonical 로 올라왔다"
    assert lp[0].get("gate_detail", {}).get("beta_600K", 1.0) < 0.8, "β 근거가 사라졌다"
    # 순위·레이더 집합에서 자동으로 빠져야 한다
    assert "lpsocl" not in C.canonical_map(reg, "MD_Ea_eV", group="md-ea-multiseed-v1")


def _fixture_registry(tmp, gap=2.2309):
    """repo 밖 임시 root 에 원자료 + 레지스트리를 만든다.

    ⚠ 왜 fixture 인가 (2026-08-07 Codex 3라운드): 첫 판은 추적 중인 정본
      `db/properties/lpsocl_dos_gap.json` 을 직접 고쳤다 `finally` 로 되돌렸다.
      정상 종료·일반 예외에서는 복구되지만 **hard kill·전원 손실에서는 정본이 오염된 채
      남는다.** 게다가 다음 실행이 오염된 파일을 backup 으로 덮어써 복구 기준까지 잃는다.
      → 이제 fixture 가 repo 밖에서 완결된다. 정본 파일은 **읽지도 쓰지도 않는다.**
    """
    import json as _j
    src = tmp / "db" / "properties"
    src.mkdir(parents=True, exist_ok=True)
    (src / "fake_gap.json").write_text(_j.dumps({"gap_eV": gap}), encoding="utf-8")
    regp = tmp / "registry.json"
    regp.write_text(_j.dumps({"schema": "canonical_registry/v1", "entries": [
        {"system": "lpsocl", "metric": "gap_eV", "value": 2.2309, "unit": "eV",
         "source_path": "db/properties/fake_gap.json", "source_key": "/gap_eV",
         "method_id": "test", "comparison_group": "gap-fixedocc-eigenvalue-v1",
         "status": "canonical"},
        {"system": "comp1", "metric": "gap_eV", "value": 2.066, "unit": "eV",
         "source_path": "db/properties/fake_gap2.json", "source_key": "/gap_eV",
         "method_id": "test", "comparison_group": "gap-fixedocc-eigenvalue-v1",
         "status": "canonical"},
    ]}), encoding="utf-8")
    (src / "fake_gap2.json").write_text(_j.dumps({"gap_eV": 2.066}), encoding="utf-8")
    return regp


def test_source_edit_propagates_to_screen():
    """"db 한 곳만 고치면 화면이 갱신된다" 를 임시 fixture 로 검증한다.

    드리프트가 나면 (a) 값은 새 값을 쓰고 (b) 순위에서 빠지고 (c) validator 가 실패한다.
    """
    import json as _j
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        regp = _fixture_registry(tmp)
        reg = C.load_registry(regp, root=tmp)
        e = [x for x in reg["entries"] if x["system"] == "lpsocl"][0]
        assert abs(e["value"] - 2.2309) < 1e-6 and e["status"] == "canonical"

        (tmp / "db" / "properties" / "fake_gap.json").write_text(
            _j.dumps({"gap_eV": 2.9999}), encoding="utf-8")
        reg = C.load_registry(regp, root=tmp)
        e = [x for x in reg["entries"] if x["system"] == "lpsocl"][0]
        assert abs(e["value"] - 2.9999) < 1e-6, "원자료를 고쳤는데 값이 안 따라온다"
        assert e["status"] == "unreviewed_drift", "미검토 드리프트 표시가 없다"
        assert "lpsocl" not in C.canonical_map(reg, "gap_eV",
                                               group="gap-fixedocc-eigenvalue-v1"), \
            "미검토 값이 순위 집합에 남아 있다"
        assert C.validate(reg, root=tmp), "드리프트인데 validator 가 통과한다"


def test_source_error_drops_out_of_canonical():
    """★ 원자료를 못 읽으면 stale 값이 정본 자리에 남으면 안 된다 (Codex 3라운드).

    첫 판은 resolve_error 만 적고 status 는 canonical 로 뒀다. 화면 순위는 validator 를
    안 돌리므로 stale 값이 계속 정본으로 쓰였다.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        regp = _fixture_registry(tmp)
        (tmp / "db" / "properties" / "fake_gap.json").unlink()   # 원자료를 없앤다
        reg = C.load_registry(regp, root=tmp)
        e = [x for x in reg["entries"] if x["system"] == "lpsocl"][0]
        assert e["status"] == "source_error", f"status 가 {e['status']} 다 — 자동판정에 남는다"
        assert "lpsocl" not in C.canonical_map(reg, "gap_eV",
                                               group="gap-fixedocc-eigenvalue-v1")
        assert C.validate(reg, root=tmp), "원자료를 못 읽는데 validator 가 통과한다"


def test_running_process_sees_source_change():
    """★ 오래 사는 worker 에서도 db 수정이 다음 요청에 반영돼야 한다 (Codex 3라운드).

    첫 판은 data.py 가 import 때 _REG 를 한 번 만들어, 재시작 전에는 안 바뀌었다.
    """
    import json as _j
    import time as _t
    p = ROOT / "db" / "properties" / "canonical_registry.json"
    before = D.CANONICAL["gap_eV"]["lpsocl"]
    k0 = C._mtime_key()
    # 실제 파일은 안 건드리고, mtime 캐시 키가 원자료를 **포함**하는지만 확인한다
    srcs = {sp for e in _j.loads(p.read_text(encoding="utf-8"))["entries"]
            if (sp := e.get("source_path"))}
    keyed = {k for k, _ in k0}
    assert srcs <= keyed, f"캐시 키가 원자료를 안 본다 — 빠진 것: {srcs - keyed}"
    assert D.CANONICAL["gap_eV"]["lpsocl"] == before
    # CANONICAL 이 전역 스냅샷이 아니라 매번 읽는지
    assert type(D.CANONICAL).__name__ == "_LazyMap", "CANONICAL 이 다시 정적 딕셔너리가 됐다"


def test_non_canonical_status_is_visible_on_screen():
    """★ 자동판정에서 뺐어도 표·카드에는 **왜 빠졌는지**가 보여야 한다 (Codex 3라운드).

    차트에서만 빼면 "표에 있으니 정본이겠지" 로 읽혀 정렬·인용에 그대로 쓰인다.
    """
    c = A.app.test_client()
    cmp_ = c.get("/compare").get_data(as_text=True)
    assert "statusBadge" in cmp_ and "unreviewed_drift" in cmp_, "compare 표에 상태 배지가 없다"
    exp = c.get("/explorer").get_data(as_text=True)
    assert "canonical_status" in (ROOT / "webapp" / "templates" / "explorer.html")\
        .read_text(encoding="utf-8"), "explorer 표에 상태 배지가 없다"
    # 실제로 비정본이 있는 조성 카드에 배지가 뜨는지 (comp2 gap = provisional)
    comp = c.get("/composition/comp2").get_data(as_text=True)
    assert "잠정" in comp
    st = D.canonical_status_for("comp2")
    assert "gap_eV" in st and st["gap_eV"]["status"] != "canonical"


def test_dashboard_ea_card_is_protocol_honest():
    """첫 화면 Ea 카드가 단일시드 값을 '멀티시드'라 부르면 안 된다."""
    cards = [h for h in D.dashboard_highlights() if "Ea" in h["t"]]
    assert cards, "Ea 카드가 없다"
    txt = " ".join(cards[0][k] for k in ("t", "v", "n"))
    assert "0.224" not in cards[0]["v"], "단일시드 0.224 가 다시 카드 값으로 올라왔다"
    assert "멀티시드" in txt
    # 오차막대가 겹치는 modelc/b2o3 를 두고 '최저'를 주장하면 안 된다
    assert "구분 안 됨" in cards[0]["v"], "겹치는 오차막대인데 순위를 주장한다"


def test_gap_card_excludes_legacy_group():
    """갭 순위가 legacy DOS-문턱 값(comp2)을 같은 축에 올리면 안 된다."""
    gm = D.canonical_comparable("gap_eV", "gap-fixedocc-eigenvalue-v1")
    assert "comp2" not in gm
    assert set(gm) == {"comp1", "modelc", "lpsocl", "b2o3"}


def test_compare_page_ships_group_metadata():
    """compare 화면이 강제할 수 있도록 묶음/상태가 실제로 내려가야 한다."""
    b = A.app.test_client().get("/compare").get_data(as_text=True)
    m = re.search(r"const CMETA=(\{.*?\});", b, re.S)
    assert m, "CMETA 가 안 내려간다"
    d = json.loads(m.group(1))
    assert d["MD_Ea_eV|modelc"]["group"] == "md-ea-multiseed-v1"
    assert d["gap_eV|comp2"]["group"] != d["gap_eV|comp1"]["group"], "legacy 갭이 정본과 같은 묶음이다"
    assert "splitByGroup" in b, "묶음 강제 함수가 템플릿에 없다"


def test_uma_forbidden_system_stays_na():
    """UMA 금지 조성(Li3N)은 계산값으로 채워지면 안 된다 (CLAUDE.md)."""
    na = {f"{c}|{k}" for (c, k) in D.NOT_APPLICABLE}
    assert any("li3n" in x.lower() for x in na), "Li3N N/A 표시가 사라졌다"


# ── 3) 라우트 · 데이터 스모크 ──────────────────────────────────────────────
def _routes():
    return sorted({r.rule for r in A.app.url_map.iter_rules()
                   if "GET" in r.methods and "<" not in r.rule
                   and not r.rule.startswith("/static")})


#: 기본 요청에서 **일부러 403** 인 라우트 — fail-closed 가 목적이라 200 이면 오히려 버그다.
GATED_ROUTES = {"/cascade/diagnostic": ("view=diagnostic", 403)}


def test_all_get_routes_200():
    c = A.app.test_client()
    bad = []
    for u in _routes():
        try:
            if u in GATED_ROUTES:
                q, want = GATED_ROUTES[u]
                if c.get(u).status_code != want:
                    bad.append(f"{u} (gated 인데 {want} 가 아니다)")
                elif c.get(f"{u}?{q}").status_code != 200:
                    bad.append(f"{u}?{q} (opt-in 인데 안 열린다)")
                continue
            if c.get(u).status_code != 200:
                bad.append(u)
        except Exception as ex:                      # 렌더 예외도 실패로 잡는다
            bad.append(f"{u} ({ex})")
    assert not bad, f"200 이 아닌 라우트: {bad}"


def test_all_csv_parse():
    import csv
    bad = []
    for p in list((ROOT / "db").rglob("*.csv")) + list((ROOT / "docs" / "figures").rglob("*.csv")):
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                list(csv.reader(f))
        except Exception as ex:
            bad.append(f"{p.relative_to(ROOT).as_posix()}: {ex}")
    assert not bad, bad


def test_no_literal_bold_markers_in_rendered_body():
    """대시보드 카드의 '**' 가 그대로 보이던 회귀 (2026-08-07)."""
    b = A.app.test_client().get("/").get_data(as_text=True)
    body = re.sub(r"<script\b.*?</script>", "", b, flags=re.S)
    body = re.sub(r"<[^>]*>", "", body)
    assert "**" not in body, "대시보드에 처리 안 된 ** 가 남아 있다"


# ── 4) 보안 · 동시성 · 경로 ────────────────────────────────────────────────
#: 쓰기 라우트 — 잠겼을 때 전부 403 이어야 한다.
MUTATION_PROBES = [
    ("POST", "/api/comments/db/properties/electronic.json", {"json": {"text": "x"}}),
    ("DELETE", "/api/comments/db/properties/electronic.json?id=x", {}),
    ("POST", "/api/log", {"json": {"kind": "note", "text": "x"}}),
    ("POST", "/api/file-rename", {"json": {"rel": "a", "name": "b"}}),
    ("POST", "/api/concept-upload/dft", {}),
]


def _readonly_for(env):
    """주어진 환경변수로 app.py 의 잠금 판정만 다시 계산한다 (재import 없이)."""
    on_render = bool(env.get("RENDER") or env.get("RENDER_SERVICE_ID"))
    m = (env.get("ALLOW_MUTATIONS") or "").strip().lower()
    if m in ("1", "true", "yes"):
        allow = True
    elif m in ("0", "false", "no"):
        allow = False
    else:
        allow = not on_render
    return not allow


def test_mutations_locked_on_render_open_locally():
    """의도는 '**원격**이 읽기 전용' 이다 — 로컬까지 잠그면 자기 노트북에서 코멘트를
    못 단다 (2026-08-16 실제로 그랬다). 명시 env 는 양방향으로 이긴다."""
    assert _readonly_for({"RENDER": "1"}) is True, "Render 기본이 열려 있다"
    assert _readonly_for({"RENDER_SERVICE_ID": "x"}) is True
    assert _readonly_for({}) is False, "로컬 기본이 잠겨 있다 — 코멘트를 못 단다"
    assert _readonly_for({"RENDER": "1", "ALLOW_MUTATIONS": "1"}) is False, \
        "Render 에서 명시적 허용이 안 먹는다"
    assert _readonly_for({"ALLOW_MUTATIONS": "0"}) is True, "로컬 명시적 잠금이 안 먹는다"
    for v in ("true", "yes", "TRUE"):
        assert _readonly_for({"ALLOW_MUTATIONS": v}) is False, v
    for v in ("false", "no", "NO"):
        assert _readonly_for({"ALLOW_MUTATIONS": v}) is True, v
    # 음성: 알 수 없는 값은 '허용' 으로 읽으면 안 된다 — 환경 판정으로 떨어진다
    assert _readonly_for({"RENDER": "1", "ALLOW_MUTATIONS": "maybe"}) is True


def test_mutation_routes_return_403_when_locked():
    """잠긴 상태에서는 쓰기 라우트가 전부 403 이어야 한다."""
    if not A.READ_ONLY:
        pytest.skip("이 실행은 쓰기가 열려 있다 (로컬 기본) — 잠금 동작은 위 단위테스트가 본다")
    c = A.app.test_client()
    for m, u, kw in MUTATION_PROBES:
        assert c.open(u, method=m, **kw).status_code == 403, f"{m} {u} 가 안 막혔다"


def test_markdown_blocks_dangerous_url_schemes():
    """`[x](javascript:...)` 가 실행 가능한 href 로 남으면 안 된다 (리뷰 P2 실측)."""
    for bad in ["[a](javascript:alert(1))", "[a](&#106;avascript:alert(1))",
                "[a](data:text/html;base64,PHM+)", "[a](VBscript:msgbox(1))"]:
        h = A.md_html(bad)
        assert "blocked-url" in h and "javascript" not in h.lower(), h
    for good in ["[a](https://x.com)", "[a](docs/f.png)", "[a](#sec)", "[a](docs/한글.pdf)"]:
        assert "blocked-url" not in A.md_html(good), good


def test_paths_are_posix():
    """Windows 에서 역슬래시 경로가 기록돼 첨부가 사라지던 회귀 (리뷰 P2)."""
    src = (ROOT / "webapp" / "data.py").read_text(encoding="utf-8")
    assert not re.search(r"str\(\w[\w.]*\.relative_to\(ROOT\)\)", src), \
        "str(...relative_to(ROOT)) 가 남아 있다 — .as_posix() 를 쓸 것"


def test_comment_writes_survive_concurrency():
    """gunicorn worker 2개에서 마지막 저장이 앞선 저장을 덮던 회귀 (40 요청 → 2 저장)."""
    import multiprocessing as mp
    rel = "db/properties/electronic.json"
    before = len(D.file_comments(rel))
    n = 24
    with mp.Pool(6) as p:
        rs = p.map(_cmt_worker, [(rel, i) for i in range(n)])
    ok = [r for r in rs if r.get("ok")]
    after = len(D.file_comments(rel))
    ids = [r["item"]["id"] for r in ok]
    try:
        assert len(ok) == n, f"{len(ok)}/{n} 만 성공"
        assert after - before == n, f"{after - before}/{n} 만 저장됐다"
        assert len(set(ids)) == n, "코멘트 id 가 겹친다 — 삭제가 엉뚱한 걸 지운다"
    finally:
        for r in ok:
            D.del_file_comment(rel, r["item"]["id"])


def test_comment_writes_survive_heavy_concurrency():
    """★ 100건 반복 스트레스 (2026-08-07 Codex 3라운드).

    24건 1회로는 Windows 의 os.replace PermissionError 간헐 실패를 못 잡았다
    (실측: 12프로세스 x 100건 x 10회 → 6회 실패, 합계 992/1000).
    ⚠ 추적 중인 db/file_comments.json 을 쓰지 않도록 **임시 경로로 갈아끼운다** —
      실패해도 repo 파일이 오염되지 않는다.
    """
    import multiprocessing as mp
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        old = D.COMMENTS_PATH
        try:
            D.COMMENTS_PATH = Path(td) / "file_comments.json"
            rel = "db/properties/electronic.json"
            n = 100
            with mp.Pool(8) as p:
                rs = p.map(_cmt_worker_tmp, [(str(D.COMMENTS_PATH), rel, i) for i in range(n)])
            ok = [r for r in rs if r and r.get("ok")]
            saved = len(D.file_comments(rel))
            ids = [r["item"]["id"] for r in ok]
            errs = {str(r.get("error"))[:80] for r in rs if not (r and r.get("ok"))}
            assert len(ok) == n, f"{len(ok)}/{n} 만 성공 · 오류 {errs}"
            assert saved == n, f"{saved}/{n} 만 저장됐다 (os.replace 재시도 확인)"
            assert len(set(ids)) == n, "코멘트 id 가 겹친다"
        finally:
            D.COMMENTS_PATH = old


def test_mkdir_fallback_stale_lock_recovery():
    """★ mkdir 폴백의 stale lock 회수 — **3케이스 전부** (2026-08-07 Codex 4라운드).

    정상 Windows/Linux 에는 msvcrt/fcntl 이 있어 이 분기가 아예 안 돈다. 그래서 둘 다
    막고 강제로 폴백을 태운다. Codex 지적: 기존 21개가 통과해도 이 경로는 미검증이었다.

    ⚠⚠ 그리고 여기서 `os.kill(pid, 0)` 을 쓰면 안 된다 — Windows CPython 은 그걸
      TerminateProcess 로 보내므로 **살아 있는 주인을 죽인다.** _alive() 가 OS 별로
      갈리는지도 같이 본다.
    """
    import builtins
    import tempfile
    import time as _t
    real = builtins.__import__

    def blocked(name, *a, **k):
        if name in ("fcntl", "msvcrt"):
            raise ImportError(f"blocked {name}")
        return real(name, *a, **k)

    old = D.COMMENTS_PATH
    with tempfile.TemporaryDirectory() as td:
        try:
            D.COMMENTS_PATH = Path(td) / "c.json"
            lock = Path(str(D.COMMENTS_PATH) + ".lock.d")
            own = lock / "owner"
            builtins.__import__ = blocked

            # ① 죽은 주인 + 오래됨 → 회수해야 한다
            lock.mkdir(parents=True, exist_ok=True)
            own.write_text("999999 %f" % (_t.time() - 10000), encoding="utf-8")
            with D._comments_locked(timeout=3):
                pass
            assert not lock.exists(), "죽은 주인의 stale lock 을 회수하지 못했다"

            # ② 살아 있는 주인 → 절대 뺏으면 안 된다
            lock.mkdir(parents=True, exist_ok=True)
            own.write_text(f"{os.getpid()} {_t.time() - 10000}", encoding="utf-8")
            try:
                with D._comments_locked(timeout=0.4):
                    raise AssertionError("살아 있는 주인의 lock 을 뺏었다")
            except TimeoutError:
                pass
            assert lock.exists(), "살아 있는 주인의 lock 이 사라졌다"
            own.unlink(missing_ok=True)
            lock.rmdir()

            # ③ owner 파일 없음(= mkdir 직후 크래시) + 오래됨 → 디렉터리 mtime 으로 회수
            lock.mkdir(parents=True, exist_ok=True)
            os.utime(lock, (_t.time() - 10000, _t.time() - 10000))
            with D._comments_locked(timeout=3):
                pass
            assert not lock.exists(), "owner 없는 stale lock 을 회수하지 못했다"
        finally:
            builtins.__import__ = real
            D.COMMENTS_PATH = old


def test_alive_check_is_not_os_kill_on_windows():
    """★ Windows 에서 `os.kill(pid, 0)` 은 존재 확인이 아니라 **종료 요청**이다.

    CPython 의 Windows os.kill 은 sig 가 CTRL_C/CTRL_BREAK 가 아니면
    TerminateProcess(handle, sig) 로 간다. 소스에 그 분기가 있는지 본다
    (실행 중 프로세스를 죽여 볼 수는 없으므로 구조로 검사한다).
    """
    src = (ROOT / "webapp" / "data.py").read_text(encoding="utf-8")
    i = src.find("def process_alive(")
    assert i > 0, "process_alive() 가 사라졌다"
    body = src[i:i + 4200]
    assert 'os.name == "nt"' in body, "_alive() 에 Windows 분기가 없다"
    nt = body[body.index('os.name == "nt"'):]
    nt = nt[:nt.index("os.kill(")] if "os.kill(" in nt else nt
    assert "OpenProcess" in nt, "Windows 분기가 OpenProcess 를 안 쓴다"
    # os.kill 은 Windows 분기 **밖**에만 있어야 한다
    assert "os.kill" not in nt, "Windows 분기 안에서 os.kill 을 쓴다 — 프로세스를 죽인다"
    # ★ 2차 (Codex 5라운드 Windows 실기): QUERY_LIMITED 만으로는 Wait 가 WAIT_FAILED 다.
    #   구조 검사가 함수 존재만 봐서 이 런타임 권한 오류를 못 잡았다 — 이제 조합을 본다.
    assert "SYNCHRONIZE" in nt, "OpenProcess 에 SYNCHRONIZE 가 없다 — Wait 가 WAIT_FAILED 난다"
    assert "GetExitCodeProcess" in nt and "STILL_ACTIVE" in nt, \
        "Wait 실패 시 GetExitCodeProcess 폴백이 없다"
    assert "WAIT_FAILED" in nt, "WAIT_FAILED 를 구분하지 않는다 — 살아 있는 주인을 죽음으로 오판한다"


def test_alive_treats_unknown_as_alive():
    """★ 판단 불가는 **항상 '살아 있다'** 로 떨어져야 한다 (2026-08-07 Codex 5라운드).

    1차 Windows 수정이 실패한 지점이 정확히 이거다: PROCESS_QUERY_LIMITED_INFORMATION
    만 열면 WaitForSingleObject 가 **WAIT_FAILED(0xFFFFFFFF)** 를 주는데, 코드가
    "WAIT_TIMEOUT 아니면 죽음" 으로 봐서 **살아 있는 주인의 lock 을 뺏었다.**
    가짜 kernel32 로 다섯 경우를 다 태운다.
    """
    import ctypes as _ct
    import types
    real_windll = getattr(_ct, "WinDLL", None)
    old_name = os.name
    #  Wait 반환      GetExitCode 성공?  종료코드   기대 alive
    cases = [
        ("wait_timeout",              0x102,      True,  259, True),
        ("wait_object_0",             0x000,      True,    0, False),
        ("wait_failed + STILL_ACTIVE", 0xFFFFFFFF, True,  259, True),   # ← 회귀 지점
        ("wait_failed + exited",      0xFFFFFFFF, True,    0, False),
        ("wait_failed + 조회 실패",     0xFFFFFFFF, False,   0, True),   # 판단 불가
    ]
    for name, wait_rc, gec_ok, code, want in cases:
        class _OP:                       # OpenProcess 는 restype/argtypes 대입을 받는다
            restype = None
            argtypes = None

            def __call__(self, *a, **k):
                return 1234              # 널이 아닌 핸들

        fake = types.SimpleNamespace(
            OpenProcess=_OP(),
            WaitForSingleObject=lambda h, t, _r=wait_rc: _r,
            CloseHandle=lambda h: 1,
            GetExitCodeProcess=(lambda h, ref, _c=code, _ok=gec_ok:
                                (setattr(ref._obj, "value", _c), 1 if _ok else 0)[1]),
        )
        os.name = "nt"
        _ct.WinDLL = lambda n, use_last_error=False, _f=fake: _f
        try:
            got = D.process_alive(999999)
            assert got is want, f"{name}: alive={got} · 기대={want}"
        finally:
            os.name = old_name
            if real_windll is not None:
                _ct.WinDLL = real_windll


def test_comp2_ordered_and_disorder_are_separate():
    """★ ordered baseline 과 disorder ensemble 을 한 항목에 섞으면 안 된다 (Codex 4라운드).

    0.275 는 ordered single-champion 인데 method_id 가 disorder-ensemble 이었다.
    원자료가 직접 'anion disorder mechanism 을 샘플링하지 않았다'고 적고 있다.
    """
    reg = C.load_registry()
    idx = {(e["metric"], e["system"]): e for e in reg["entries"]}
    o = idx.get(("MD_Ea_eV_ordered", "comp2"))
    d = idx.get(("MD_Ea_eV_disorder", "comp2"))
    assert o and d, "comp2 ordered/disorder 항목이 분리돼 있지 않다"
    assert "ordered" in o["method_id"] and "disorder" not in o["method_id"]
    assert "disorder" in d["method_id"]
    assert o["comparison_group"] != d["comparison_group"], "같은 묶음에 있다"
    assert abs(o["value"] - 0.2754597563) < 1e-9, "ordered 가 정밀 원자료가 아니다"
    assert abs(d["value"] - 0.1512) < 1e-9 and d.get("n_config") == 3, \
        "disorder 는 n_seed 가 아니라 n_config 여야 한다"
    # d=1.00 은 게이트 FAIL 이라 등재하면 안 된다
    assert not any(abs((e.get("value") or 0) - 0.3775) < 1e-9 for e in reg["entries"]), \
        "게이트 FAIL 인 d=1.00 이 레지스트리에 있다"


def test_new_metrics_reach_all_screens():
    """★ 레지스트리에 metric 이 늘면 화면 셋이 자동으로 따라와야 한다 (Codex 5라운드).

    ordered/disorder 로 쪼갠 뒤에도 (a) explorer 는 새 두 metric 을 아예 안 보여줬고
    (b) composition 카드는 label·unit 이 빈칸이었고 (c) compare 는 **옛 0.275 를 같이**
    보여줬다. 원인은 세 템플릿이 metric 목록을 각자 하드코딩한 것이었다.
    """
    import json as _j
    mm = D.metric_meta()
    for k in ("MD_Ea_eV_ordered", "MD_Ea_eV_disorder"):
        assert k in mm and mm[k]["label"] and mm[k]["unit"], f"{k} 의 label/unit 이 없다"
    c = A.app.test_client()
    exp = c.get("/explorer").get_data(as_text=True)
    assert mm["MD_Ea_eV_ordered"]["label"] in exp, "explorer 에 ordered metric 이 없다"
    assert mm["MD_Ea_eV_disorder"]["label"] in exp, "explorer 에 disorder metric 이 없다"
    comp = c.get("/composition/comp2").get_data(as_text=True)
    assert mm["MD_Ea_eV_ordered"]["label"] in comp, "composition 카드에 label 이 없다"
    cmp_ = c.get("/compare").get_data(as_text=True)
    canon = _j.loads(re.search(r"const CANON=(\{.*?\});", cmp_, re.S).group(1))
    assert canon.get("MD_Ea_eV", {}).get("comp2") is None, \
        "옛 MD_Ea_eV comp2(0.275) 가 화면에 남아 있다 — 하드코딩 잔재"
    assert "MD_Ea_eV_ordered" in canon and "MD_Ea_eV_disorder" in canon


def test_comparison_group_id_is_visible():
    """★ 의미를 나눠 놓고도 **어느 묶음인지**가 화면에 안 보이면 나눈 의미가 없다.

    2026-08-07 Codex 6라운드: ordered/disorder 가 둘 다 provisional 이라 canonical
    묶음이 없었고, /compare 는 "비교 가능한 묶음이 없다" 만 찍었다 — 등록 묶음 ID 는
    어디에도 안 나왔다.
    """
    c = A.app.test_client()
    G_ORD, G_DIS = "md-ea-comp2-ordered-provisional", "md-ea-comp2-disorder-d050"
    # ① compare: 묶음이 없을 때 등록 묶음을 나열하는 분기가 있는지 + 셀 툴팁
    cmp_ = c.get("/compare").get_data(as_text=True)
    assert "등록 묶음" in cmp_, "compare 에 '등록 묶음' 표기가 없다"
    assert G_ORD in cmp_ and G_DIS in cmp_, "compare 에 묶음 ID 가 안 내려간다"
    # ② explorer · composition: 배지 툴팁에 묶음 ID
    for u in ("/explorer", "/composition/comp2"):
        t = c.get(u).get_data(as_text=True)
        assert G_ORD in t, f"{u} 에 ordered 묶음 ID 가 없다"
        assert G_DIS in t, f"{u} 에 disorder 묶음 ID 가 없다"
    # ③ 데이터층: 배지에 group 이 실려 있는지
    st = D.canonical_status_for("comp2")
    assert st["MD_Ea_eV_ordered"]["group"] == G_ORD
    assert st["MD_Ea_eV_disorder"]["group"] == G_DIS
    assert st["MD_Ea_eV_ordered"]["why"].startswith("등록 묶음 [")


def test_provenance_open_is_visible_on_screen():
    """★ provenance_open 을 validator 만 찍으면 **사이트에서는 여전히 무경고**다.

    2026-08-07 Codex 6라운드 후속 지적. status 는 canonical 그대로여야 하고
    (값이 틀린 게 아니다 — 순위에서 빼면 과잉), 대신 눈에 보이는 표식이 있어야 한다.
    """
    flags = D.canonical_provenance_flags()
    assert flags, "provenance_open 항목이 하나도 안 잡힌다"
    # status 는 안 내려간다 — 순위에는 남아야 한다
    gm = D.canonical_comparable("gap_eV", "gap-fixedocc-eigenvalue-v1")
    assert set(gm) == {"comp1", "modelc", "lpsocl", "b2o3"}, \
        "provenance_open 이 순위에서 값을 빼 버렸다 — 과잉이다"
    c = A.app.test_client()
    for u in ("/compare", "/explorer", "/composition/comp1"):
        assert "출처⚠" in c.get(u).get_data(as_text=True), f"{u} 에 출처 표식이 없다"


def test_sei_axes_reflect_campaign_state():
    """대시보드가 요청 3축의 상태를 직접 말해야 한다 — 안 그러면 '갭만 했나' 로 읽힌다."""
    ax = D.sei_axes()["axes"]
    assert len(ax) == 3
    names = " ".join(a["n"] for a in ax)
    assert "확산장벽" in names and "형성 전위" in names and "밴드갭" in names
    done = {a["n"]: a["done"] for a in ax}
    assert done["② 형성 전위"] and done["③ 밴드갭 + DOS/PDOS"], "완료 축이 완료로 안 뜬다"
    body = A.app.test_client().get("/").get_data(as_text=True)
    assert "공동연구 요청 3축" in body and "확산장벽" in body


def test_no_hardcoded_metric_lists_in_templates():
    """metric 목록이 템플릿으로 되돌아오면 안 된다 — 그게 위 회귀의 원인이었다."""
    for name in ("explorer.html", "composition.html", "compare.html"):
        t = (ROOT / "webapp" / "templates" / name).read_text(encoding="utf-8")
        assert "MM" in t, f"{name} 이 metric_meta(MM)를 안 쓴다"
        assert "'gap_eV','Band gap'" not in t and "'gap_eV':'eV'" not in t, \
            f"{name} 에 metric 하드코딩이 되살아났다"


def test_evrh_group_respects_source_pairing():
    """★ elastic.json 이 comp1↔comp2 만 완전비교쌍이라 한다 (Codex 5라운드).

    네 조성을 한 묶음으로 자동 순위화하면 method_id 가 맞아도 의미상 틀린다.
    """
    reg = C.load_registry()
    g = {e["system"]: e["comparison_group"] for e in C.entries(reg, "E_VRH_GPa", status=None)}
    assert g.get("comp1") == g.get("comp2"), "comp1↔comp2 가 같은 묶음이 아니다"
    for other in ("modelc", "lpsocl"):
        assert g.get(other) != g.get("comp1"), \
            f"{other} 가 comp1/comp2 완전비교쌍 묶음에 섞여 있다"


def test_status_badge_is_not_duplicated():
    """★ 레지스트리 status 와 옛 PROV 배지가 겹쳐 '잠정' 이 두 번 찍혔다 (Codex 4라운드)."""
    c = A.app.test_client()
    for u in ("/explorer", "/composition/comp2", "/composition/lpsocl"):
        t = c.get(u).get_data(as_text=True)
        dup = re.findall(r">잠정</span>\s*<span class=\"badge\"[^>]*>[^<]*</span>", t)
        assert not dup, f"{u} 에서 배지가 중복된다: {dup[:2]}"
    cmp_ = c.get("/compare").get_data(as_text=True)
    # compare 는 JS 로 그리므로 '둘 다 붙이는' 코드 형태가 남아 있지 않은지 본다
    assert "else if(pr)cell+=" in cmp_, "compare 가 배지를 배타적으로 안 고른다"


def test_seminar_points_at_files_that_exist():
    """★ /seminar 이 **없는 덱**(Research_Seminar_2026_08_cascade.pptx)과 옛 spec 을 가리키고
    있었다 — 다운로드 버튼이 조용히 사라진 상태였다 (2026-08-11 개편). 다시 어긋나지 않게 못 박는다."""
    for key, (name, _note) in D.SEMINAR_DECKS.items():
        assert (D.KB / "seminars" / name).is_file(), f"덱 화이트리스트 '{key}' 가 없는 파일을 가리킨다: {name}"
    assert (D.KB / "seminars" / D.SEMINAR_SCRIPT).is_file(), "정본 대본이 없다"
    live = [k for k, _l, p, _n in D.SEMINAR_DOCS if p.is_file()]
    assert "script" in live, "대본 탭이 안 뜬다 — 경로가 어긋났다"
    assert len(live) >= 4, f"세미나 문서 탭이 너무 적다: {live}"

    c = A.app.test_client()
    t = c.get("/seminar").get_data(as_text=True)
    assert c.get("/seminar/deck?v=release").status_code == 200
    assert c.get("/seminar/deck?v=../../etc/passwd").status_code == 404, "덱 키가 경로로 새면 안 된다"
    for k in live:
        assert f'data-tab="{k}"' in t, f"{k} 탭이 화면에 없다"


def test_seminar_runsheet_tracks_the_script():
    """진행표는 대본을 **파싱**해서 만든다 — 하드코딩하면 대본을 고쳤을 때 조용히 어긋난다."""
    md = (D.KB / "seminars" / D.SEMINAR_SCRIPT).read_text(encoding="utf-8")
    rs = D.seminar_runsheet(md)
    assert len(rs) >= 4, f"Part 를 못 읽었다: {rs}"
    assert all(p["slides"] for p in rs), "슬라이드가 비어 있는 Part 가 있다"
    assert sum(p["seconds"] for p in rs) > 600, "초 배분을 못 읽었다 (⏱ 표기 확인)"
    assert not any("(" in p["title"] for p in rs), f"Part 제목에 괄호 메타가 남았다: {[p['title'] for p in rs]}"
    # 대본에 없는 Part 를 화면이 지어내지 않는지 — 개수가 정확히 같아야 한다
    t = A.app.test_client().get("/seminar").get_data(as_text=True)
    assert len(re.findall(r'class="sem-badge">([A-Z])<', t)) == len(rs)


# ── cascade 화면의 지위 표시 (2026-08-14 개정) ──────────────────────────────
#   화면이 47종 시대 결과를 최신 승인물처럼 보여주던 것을 고쳤다. 그 상태로 되돌아가면
#   사이트가 스스로 모순되므로(승인 0건인데 1위 표가 뜬다) 여기서 잠근다.
def _cascade_html():
    return A.app.test_client().get("/cascade").get_data(as_text=True)


def test_cascade_defaults_to_the_audit_screen():
    """승인된 랭킹이 0건이므로 기본 탭은 결과가 아니라 감사 화면이어야 한다."""
    h = _cascade_html()
    m = re.search(r'<button class="active" data-tab="([a-z0-9]+)"', h)
    assert m, "#tabs 에 active 버튼이 없다"
    assert m.group(1) == "audit", f"기본 탭이 '{m.group(1)}' 이다 — 감사 화면이어야 한다"
    assert re.search(r'<div class="tab-panel active" id="tab-audit"', h), "tab-audit 패널이 active 가 아니다"


def test_cascade_headline_comes_from_the_manifest():
    """타일 숫자는 하드코드가 아니라 manifest 파생이어야 한다 (Codex 리뷰 P1)."""
    t = D.cascade_truth()
    assert t["ok"], f"manifest 가 유효하지 않다: {t.get('problems')} {t.get('stale')}"
    got = {k: v for k, v, _l, _n in t["tiles"]}
    assert got["planned_slots"] == 273 and got["completed_slots"] == 270
    assert got["completed_species"] == 90 and got["historical_snapshot_species"] == 47
    assert got["approved_current_leaderboard_species"] == 0
    assert got["explicit_pair_property_labels"] == 0
    h = _cascade_html()
    assert "승인된 도펀트 랭킹은 0건" in h, "승인 0건 배너가 화면에 없다"
    assert "랭킹된 도펀트</div>" not in h, "47종 타일 라벨이 최상단에 되살아났다"


def test_manifest_tamper_fails_closed():
    """파일이 바뀌었는데 manifest 가 안 따라오면 숫자를 추측하지 말고 막아야 한다."""
    import hashlib
    m = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    for a in m["artifacts"]:
        p = ROOT / a["source_path"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == a["sha256"], (
            f"{a['source_path']} 가 manifest 와 어긋난다 — rebuild_pool_inputs.py 를 다시 돌릴 것")
        assert a["approval_status"] in D._MANIFEST_STATUS
        assert a["use_scope"] in D._MANIFEST_USE_SCOPE
        assert a["actual_x"] == 0.25, "실측 농도는 0.25 다 (라벨 x002/x005/x010 은 농도가 아니다)"
    # 위조 시나리오: status 를 어휘 밖 값으로 바꾸면 ok=False 여야 한다
    orig = D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8")
    try:
        bad = json.loads(orig)
        bad["artifacts"][0]["approval_status"] = "approved_by_nobody"
        D.CASCADE_MANIFEST_PATH.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
        D._load_json.cache_clear() if hasattr(D._load_json, "cache_clear") else None
        assert D.cascade_truth()["ok"] is False, "알 수 없는 status 인데 fail-closed 하지 않았다"
    finally:
        D.CASCADE_MANIFEST_PATH.write_text(orig, encoding="utf-8")
        D._load_json.cache_clear() if hasattr(D._load_json, "cache_clear") else None


def test_na2s_ductility_claim_is_retracted():
    """음의 B_hill 행을 평균에 넣고 역수를 취해 만든 '연성 반증' 은 철회됐다."""
    import csv as _csv
    rows = list(_csv.DictReader(
        l for l in (D.DB / "properties" / "cascade_v23_champions_v2.csv")
        .read_text(encoding="utf-8").splitlines() if not l.startswith("#")))
    bad = [r for r in rows if r["elastic_B_hill_GPa"].strip()
           and float(r["elastic_B_hill_GPa"]) <= 0]
    assert bad, "비물리 행이 사라졌다면 이 회귀 테스트를 갱신할 것"
    rk = {r["dopant"]: r for r in _csv.DictReader(
        l for l in (D.DB / "properties" / "cascade_v23_ranked_v2.csv")
        .read_text(encoding="utf-8").splitlines() if not l.startswith("#"))}
    # 실패 행이 평균에서 빠졌으므로 Na2S 의 B/G 는 1.75 아래여야 한다
    assert 1.0 / float(rk["Na2S"]["pugh"]) < 1.75, "Na2S 가 다시 연성 경험칙을 넘었다 — 가드 확인"
    th = json.loads((D.DB / "properties" / "cascade_v23_themes_v2.json").read_text(encoding="utf-8"))
    assert "어느 것도 B/G>1.75" in th["themes"]["ductility"]["caveat"], "연성 서술이 되돌아갔다"


def test_recovered_ranking_is_gated_server_side():
    """<details> 는 후보명을 초기 DOM 에 다 싣는다 — 서버가 렌더 자체를 막아야 한다."""
    c = A.app.test_client()
    h = _cascade_html()
    assert "/cascade/diagnostic" in h, "acquisition 화면 링크가 없다"
    denied = c.get("/cascade/diagnostic")
    assert denied.status_code == 403, "view=diagnostic 없이 열렸다"
    body = denied.get_data(as_text=True)
    fun = json.loads((D.DB / "properties" / "cascade_screening_funnel_v2.json")
                     .read_text(encoding="utf-8"))
    names = [g for g in (fun.get("gates") or []) if g.get("id") == "G4"]
    ep = (D.load_cascade()["v2"]["meta"].get("funnel_v2") or {}).get("endpoint") or []
    assert ep, "endpoint 목록이 비었다 — 이 테스트를 갱신할 것"
    for sp in ep[:6]:
        assert sp not in body, f"거부 화면에 후보명 {sp} 가 DOM 으로 실렸다"
    allowed = c.get("/cascade/diagnostic?view=diagnostic")
    assert allowed.status_code == 200 and ep[0] in allowed.get_data(as_text=True)


def test_artifact_policy_gates_every_api_path():
    """화면에서 숨긴 artifact 를 API 로 그냥 받을 수 있으면 안 된다 (Codex Round-3 P0-3)."""
    c = A.app.test_client()
    cases = [
        ("/api/file/db/properties/cascade_audit_gate_completeness.csv?dl=1", 200),
        # Round-3 — 종명이 든 감사본은 공개 금지, 익명 공개판이 default_visible
        ("/api/file/docs/figures/cascade/cascade_audit_g4_rescore.png", 403),
        ("/api/file/docs/figures/cascade/cascade_audit_g4_rescore.png?view=diagnostic", 200),
        ("/api/file/docs/figures/cascade/cascade_seminar_g4_anonymized_round3.png", 200),
        ("/api/file/db/properties/cascade_seminar_gate_denominators_round3.csv?dl=1", 200),
        ("/api/file/db/properties/cascade_v23_ranked_v2.csv?dl=1", 403),
        ("/api/file/db/properties/cascade_v23_ranked_v2.csv?dl=1&view=diagnostic", 200),
        ("/api/file/db/properties/cascade_v23_ranked.csv?dl=1", 403),
        ("/api/file/db/properties/cascade_v23_ranked.csv?dl=1&archive=1", 200),
        ("/api/property/cascade_screening_funnel_v2", 403),
        ("/api/property/cascade_screening_funnel_v2?view=diagnostic", 200),
        ("/api/csv/properties/cascade_v23_ranked_v2.csv", 403),
        ("/api/file/db/properties/electronic.json", 200),      # cascade 밖은 통과
    ]
    for url, want in cases:
        got = c.get(url).status_code
        assert got == want, f"{url} → {got} (want {want})"


def test_manifest_has_a_single_owner():
    """생산자 둘이 같은 원장을 통째로 덮어써 상대의 계약 블록을 지웠다 (P0-1)."""
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert man.get("owner") == "tools/cascade/build_cascade_audit_manifest.py"
    for k in ("datasets", "metric_contract", "artifacts", "figures", "supporting_tables"):
        assert k in man, f"원장에 {k} 블록이 없다 — 소유자가 다시 갈라졌다"
    plotter = (ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py").read_text(encoding="utf-8")
    assert 'out = DB / "cascade_audit_manifest.json"' not in plotter, \
        "플로터가 다시 원장을 쓴다 — sidecar 만 써야 한다"
    rebuild = (ROOT / "tools" / "cascade" / "rebuild_pool_inputs.py").read_text(encoding="utf-8")
    assert "cascade_audit_manifest.json" not in rebuild, \
        "rebuild_pool_inputs 가 다시 원장을 쓴다"


def test_artifact_provenance_is_per_file():
    """top-level source_commit 하나로 전부를 덮으면 거짓말이 된다 (P0-2)."""
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    rk = [a for a in man["artifacts"] if a["source_path"].endswith("ranked_v2.csv")][0]
    assert rk["source_commit"] != man["source_commit"], "ranked_v2 가 다시 고정 커밋으로 묶였다"
    assert rk.get("derived_from") == man["source_commit"] and rk.get("override_reason")
    plotter = (ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py").read_text(encoding="utf-8")
    dep = plotter.split("RECOVERED_DERIVED = [")[1].split("]")[0]
    entries = [ln.strip() for ln in dep.splitlines() if ln.strip().startswith('"')]
    assert not any("ranked_v2" in e for e in entries), \
        "ranked_v2 가 다시 패널 의존에 들어갔다 (어느 패널도 안 읽는다)"


def test_g3_phase_set_row_reflects_the_2026_08_16_closure():
    """옛 판은 '합성 id 를 주장하지 마라'였다. 이제 진짜 id 를 싣는다 — 대신 두 가지를 지킨다:
    ① 회수 행이 가정이 아니라 기록으로 바뀌었을 것 ② 조성족 섞임이 open 으로 남아 있을 것."""
    t = D.read_csv("properties/cascade_audit_g3_phase_set.csv")
    rec = [r for r in t["data"] if r["status"] == "recovered_diagnostic"]
    assert rec, "회수 행이 사라졌다"
    assert "phase_set_id" in str(rec[0]["note"]), "무엇으로 닫혔는지가 행에 없다"
    assert not str(rec[0]["phase_set_assumption"] or "").strip(), "닫혔는데 가정 표기가 남아 있다"
    # 민감도 행은 여전히 '이 문턱을 다른 phase set 후보에 쓰지 마라' 여야 한다
    sens = [r for r in t["data"] if r["status"] == "sensitivity-only"]
    assert sens and abs(float(sens[0]["oxidation_onset_V"]) - 2.256) < 1e-9
    # 조성족은 아직 안 닫혔다 — open 행이 사라지면 조용히 닫힌 척이 된다
    op = [r for r in t["data"] if r["status"] == "open"]
    assert op, "조성족 섞임 open 행이 사라졌다"
    assert "Cl-rich" in str(op[0]["note"]) and "B2O3" in str(op[0]["note"])


def test_g4_rescore_carries_pool_metadata():
    """min–max 점수를 고정 물성처럼 읽지 못하게 하는 메타 (P1)."""
    t = D.read_csv("properties/cascade_audit_g4_rescore.csv")
    r = t["data"][0]
    for c in ("pool_id", "normalization_n", "bvs_pool_min", "bvs_pool_max", "actual_x"):
        assert str(r.get(c, "")).strip() != "", f"{c} 가 없다"
    assert float(r["actual_x"]) == 0.25


def test_g5_completeness_separates_presence_from_validity():
    """presence 88/1/1 옆에 validity-aware 86/AlBr3·MgI2·Na2S/AlI3 를 병기해야 한다 (P1)."""
    t = D.read_csv("properties/cascade_audit_gate_completeness.csv")
    g5 = [r for r in t["data"] if r["gate"] == "G5"][0]
    assert g5["validity_aware_all_label_species"] == 86
    assert g5["validity_aware_partial"] == "AlBr3|MgI2|Na2S"
    assert g5["validity_aware_dropped"] == "AlI3"
    assert all(r.get("completeness_basis") for r in t["data"]), "completeness_basis 가 비었다"


def test_public_g4_panel_is_anonymized():
    """Round-3 정책: 후보 identity 는 acquisition 전용. 공개 패널에 종명이 있으면 안 된다."""
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    pub = {f["image"] for f in man["figures"]}
    assert "docs/figures/cascade/cascade_seminar_g4_anonymized_round3.png" in pub
    assert "docs/figures/cascade/cascade_audit_g4_rescore.png" not in pub, \
        "종명이 든 G4 패널이 공개 목록으로 돌아왔다"
    # 익명 CSV 는 종명을 담지 않는다
    t = D.read_csv("properties/cascade_seminar_g4_anonymized_round3.csv")
    ids = {str(r["case_id"]) for r in t["data"]}
    assert ids == {"Case A", "Case B", "Case C", "Case D", "Case E", "Case F"}
    blob = json.dumps(t["data"], ensure_ascii=False)
    for sp in ("B2O3", "Cr2O3", "Ga2O3", "In2O3", "Sc2O3", "Y2O3"):
        assert sp not in blob, f"익명 CSV 에 {sp} 가 남아 있다"
    h = _cascade_html()
    assert "cascade_audit_g4_rescore.png" not in h, "기본 화면이 종명 패널을 띄운다"


def test_gate_denominators_separate_record_from_method():
    """기록이 있다 ≠ 비교 가능하다. G3 는 phase_set_id 를 싣고 나서야 90/90 이 됐다."""
    t = D.read_csv("properties/cascade_seminar_gate_denominators_round3.csv")
    by = {r["gate"]: r for r in t["data"]}
    assert by["G3"]["record_present_species"] == 90
    # 2026-08-16: phase_set_id + 같은 실행 안의 host 측정으로 0 → 90 (270/270 쌍)
    assert by["G3"]["all_label_method_valid_species"] == 90
    assert by["G3"]["status"] == "recovered_diagnostic"
    assert "phase_set_id" in by["G3"]["note"]
    assert by["G5"]["all_label_method_valid_species"] == 86
    assert by["G5"]["partial_species"] == "AlBr3|MgI2|Na2S"
    assert by["G4"]["dropped_species"] == "AlI3|MgI2"
    for g, r in by.items():
        assert r["approved_current_species"] == 0, f"{g} 가 승인된 것처럼 적혀 있다"
    assert "게이트 분모 계약" in _cascade_html()


def test_oxidation_onset_carries_its_composition_family():
    """이름표가 같아도 조성이 다르면 나란히 놓지 않는다 (2026-08-16 Cl-rich 섞임)."""
    pinned = json.loads((ROOT / "db/properties/oxidation_stability_cascade_v3_pinned.json")
                        .read_text(encoding="utf-8"))
    audit = pinned["composition_family_audit"]
    assert audit["counts"] == {"Clrich": 17, "plain": 253}
    assert audit["family_label_inconsistent"] == []
    assert audit["species_with_no_plain_champion"] == ["B2O3"]
    assert set(audit["species_improving_only_as_variant"]) == {"Al2O3", "MoO3", "WO3"}
    # 모든 후보 행이 조성족을 달고 있어야 한다 — 빠진 행은 조용히 비교돼 버린다
    cand = [v for k, v in pinned["results"].items() if "HOST" not in k.split("_")]
    assert len(cand) == 270
    assert all(v.get("composition_family") in ("plain", "Clrich") for v in cand)
    assert all(v["delta_ox_vs_host_V_confounded"] == (v["composition_family"] != "plain")
               for v in cand)
    # DFT-deep B2O3 는 표의 onset 과 **다른 조성**이다 (부호가 반대)
    col = pinned["dft_deep_composition_collision"]["B2O3"]
    assert col["cascade_champion"]["ox_V"] > col["host_ox_V"] > col["dft_deep_cell"]["ox_V"]

    # 47종 pool 로도 새어나가는지 — 오염은 B2O3 1건, 나머지는 plain/degenerate
    pool = json.loads((ROOT / "db/properties/cascade_screening_funnel.json")
                      .read_text(encoding="utf-8"))["pool"]
    bad = [r["dopant"] for r in pool
           if r["ox_composition_family"] in ("unmatched", "unresolved")]
    assert not bad, f"조성족을 못 정한 종: {bad}"
    assert [r["dopant"] for r in pool if r["ox_family_confounded"]] == ["B2O3"]

    seminar = D.read_csv("properties/cascade_seminar_oxidation_transport_47.csv")
    rows = {r["dopant"]: r for r in seminar["data"]}
    assert rows["B2O3"]["ox_composition_family"] == "Clrich"
    assert rows["B2O3"]["plain_champion_exists"] == 0
    # ⛔ 'WO3 가 있으면 WO3, 없으면 Sc2O3' 는 무엇을 검사하는지 불분명하다 (Codex 지적).
    #   여섯 종을 명시하고, 오염은 B2O3 하나뿐임을 그 집합 안에서 확인한다.
    assert set(rows) == {"B2O3", "Cr2O3", "Ga2O3", "In2O3", "Sc2O3", "Y2O3"}
    assert [d for d, r in rows.items() if r["ox_family_confounded"]] == ["B2O3"]


def test_seminar_17d9a373_handoff_contract():
    """세미나 최종 핸드오프(17d9a373)의 회귀 계약 12건을 한 곳에서 잠근다."""
    h = _cascade_html()
    fac = json.loads((ROOT / "db/properties/oxidation_matched_factorial.json")
                     .read_text(encoding="utf-8"))
    nol = json.loads((ROOT / "db/properties/oxidation_matched_factorial_nolis4.json")
                     .read_text(encoding="utf-8"))

    # 1. G3 네 층을 동시에 렌더한다
    for token in ("270/270", "17/17", "0/11"):
        assert token in h, f"G3 상태에 {token} 이 없다"
    assert "approved current ranking" in h.lower() or "승인" in h

    # 2·3. stale / 금지 문구가 **주장으로** 안 나온다.
    #   ⚠ 감사 화면은 "이렇게 말하면 안 된다" 목록을 일부러 띄운다 — 그 블록을 걷어내고 본다.
    #     안 그러면 경고문 자체가 위반으로 잡혀서, 경고를 지우는 게 테스트 통과법이 된다.
    body = re.sub(r"<!--FORBIDDEN-->.*?<!--/FORBIDDEN-->", "", h, flags=re.S)
    assert "<!--FORBIDDEN-->" in h, "금지 목록 블록이 사라졌다"
    assert len(body) < len(h), "금지 목록을 못 걷어냈다 (정규식 확인)"
    for forb in ("method-comparable 0", "effect attribution closed",
                 "Cl 효과는 0", "Cl effect = 0", "11/11 species validated", "9.7배"):
        assert forb not in body, f"금지 문구가 주장으로 화면에 있다: {forb}"
    # 그리고 그 목록에는 여전히 들어 있어야 한다 (경고를 지워서 통과하면 안 된다)
    for forb in ("effect attribution closed", "11/11 species validated"):
        assert forb in h, f"금지 목록에서 {forb} 가 빠졌다"

    # 4. chain audit 이 exact 10 / multi 7 을 재현
    mt = json.loads((ROOT / "db/properties/oxidation_stability_cascade_v3_pinned.json")
                    .read_text(encoding="utf-8"))["composition_family_audit"]["matched_transform"]
    assert mt["counts"] == {"exact": 10, "multi_transform": 7}

    # 5. 두 비율이 분모·non-causal 라벨과 같은 패널에
    assert "9.63" in h and "2.59" in h
    assert "17/253" in h and "11/17" in h and "4/16" in h
    assert "post-selection descriptive association" in h
    for never in ("Cl effect size", "causal enrichment", "success rate"):
        assert never in h, f"'이렇게 부르지 않는다' 목록에 {never} 가 없다"
        assert never not in body, f"{never} 가 목록 밖에서 쓰이고 있다"

    # 6. B2O3 exact composition mismatch → validation link 없음
    assert D.CASCADE_JOIN_STATUS["b2o3"]["validation_link_status"] == "different_composition"

    # 7. ladder4 = 2.356 · S16 · 0.5 LiS4
    lad = {r["cell"]: r for r in D.load_factorial()["included"]["ladder"]}
    assert lad["__ladder4__"]["ox_V"] == 2.356
    assert "S16" in lad["__ladder4__"]["formula"]
    assert "LiS4" in lad["__ladder4__"]["rxn"], "ladder4 에서 LiS4 가 사라졌다"
    assert lad["__ladder3__"]["ox_V"] == 2.140
    assert "MECHANISM HYPOTHESIS" in h, "사다리가 가설 표시 없이 나간다"

    # 8. LiS4 제외판 값 고정
    ex = nol["decomposition"]
    for sp, want in (("WO3", 0.000), ("Al2O3", 0.098), ("MoO3", 0.129), ("B2O3", 0.283)):
        got = ex[sp]["conditional_cl_recipe_contrast_V"]
        assert abs(got - want) < 5e-4, f"{sp} {got} != {want}"
    assert nol["exclusions"] == ["LiS4"]
    assert ex["Al2O3"]["H_plain_V"] == 2.256, "제외판 host 가 2.256 이 아니다"
    assert fac["decomposition"]["Al2O3"]["H_plain_V"] == 2.140
    assert "다른 phase set" in h, "두 판을 섞지 말라는 경고가 화면에 없다"

    # 9. stage 09f 가 current G2/G3 source 로 표시되지 않는다
    gm = dict(D.CASCADE_STAGE_GATE_MAP)
    assert "09f" in gm["G2 / G3 (current)"] and "아니다" in gm["G2 / G3 (current)"]
    assert "NOT A TRUE GRAND-POTENTIAL ESW" in h

    # 10. stage 10/11 은 NOT RUN · 0/270 (unharvested 아님)
    tail = [g for g in D.CASCADE_STAGE_GROUPS if g["id"] == "10-12b"][0]
    blob = " ".join(tail["warnings"])
    assert blob.count("NOT RUN") >= 2 and "0/270" in blob
    assert "unharvested" not in h and "미수확" not in h

    # 11. 기본 DOM 에 archive/diagnostic 후보 행이 없다 (별도 테스트가 상세히 본다)
    assert h.count('"dopant":') == 0

    # 12. manifest 에 두 factorial 원장이 다 등록돼 있다
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    reg = {a["source_path"]: a for a in man["artifacts"]}
    for fn, scope in (("oxidation_matched_factorial.json", "default_visible"),
                      ("oxidation_matched_factorial_nolis4.json", "diagnostic_only")):
        k = f"db/properties/{fn}"
        assert k in reg, f"{fn} 이 원장에 없다"
        assert reg[k]["use_scope"] == scope


def test_default_cascade_does_not_ship_the_superseded_ranking():
    """경고 배너는 접근 정책이 아니다 — archive/diagnostic 행은 초기 DOM 에 없어야 한다.

    ⛔ 2026-08-16 — 기본 `/cascade` 가 47종 rank·score 배열(`var RANKED`)과 90종 테마
      조합 랭킹(`var TDOP`)을 통째로 싣고 있었다. 보안이 아니라 **정책 위반**이다:
      manifest 상 각각 archive_only · diagnostic_only 인데 기본 화면이 "승인된 ranking
      0종" 이라고 쓰면서 순위표를 같이 내보냈다.
    """
    c = A.app.test_client()
    h = c.get("/cascade").get_data(as_text=True)
    assert h.count('"dopant":') == 0, "기본 화면에 후보 행이 있다"
    assert '"rank": 1.0' not in h, "47종 rank 배열이 초기 DOM 에 있다"
    assert h.count("disorder_std") < 10, "90종 테마 배열이 초기 DOM 에 있다"
    assert "보관함 열기" in h and "진단 화면 열기" in h, "opt-in 경로가 화면에 없다"

    # 값을 지운 게 아니다 — 쿼리를 주면 그대로 나온다
    ha = c.get("/cascade?archive=1").get_data(as_text=True)
    assert '"rank": 1.0' in ha and '"dopant": "Sc2O3"' in ha, "보관함에서도 안 나온다"
    assert ha.count("disorder_std") < 10, "archive 가 diagnostic 까지 열어 준다"

    hd = c.get("/cascade?view=diagnostic").get_data(as_text=True)
    assert hd.count("disorder_std") > 10, "진단 화면에서 테마 행이 안 나온다"
    assert '"rank": 1.0' not in hd, "diagnostic 이 archive 까지 열어 준다"

    # diagnostic 라우트는 여전히 opt-in 403
    assert c.get("/cascade/diagnostic").status_code == 403
    assert c.get("/cascade/diagnostic?view=diagnostic").status_code == 200


def test_factorial_does_not_claim_a_closed_causal_attribution():
    """baseline contrast 0 을 'Cl 효과 0' 으로 쓰면 안 된다 (2026-08-16 재감사 P0-1)."""
    f = json.loads((ROOT / "db/properties/oxidation_matched_factorial.json")
                   .read_text(encoding="utf-8"))
    v = f["verdict"]   # 도구가 생성한다 (손편집 금지)
    assert "'Cl 효과는 0'" in v["NO_GO"] and "'인과 귀속 폐쇄'" in v["NO_GO"]
    assert v["three_fields_not_one"]["element_level_causal_attribution"] == "not_claimed"
    assert v["baseline_nonzero_species"] == [], "baseline 이 0 이 아닌 종이 생겼다"
    assert v["conditional_range_V"] == [-0.017, 0.283]
    assert v["mechanism_status"].startswith("hypothesis")
    for sp, d in f["decomposition"].items():
        if not d.get("complete"):
            continue
        # 옛 이름이 남아 있으면 '0 이므로 효과 없음' 으로 다시 읽힌다
        assert "main_Cl_V" not in d and "main_dopant_V" not in d, sp
        assert d["isolated_element_effect"] is False
        # 대수 항등식: total = plain_dopant + conditional
        assert abs(d["total_D_Cl_vs_host_V"]
                   - (d["plain_dopant_recipe_contrast_V"]
                      + d["conditional_cl_recipe_contrast_V"])) < 5e-4, sp
    # baseline 0 인데 conditional 이 0 이 아닌 종이 실제로 있어야 한다 (그게 요점)
    nz = [sp for sp, d in f["decomposition"].items()
          if d.get("complete") and abs(d["baseline_cl_recipe_contrast_V"]) < 1e-9
          and abs(d["conditional_cl_recipe_contrast_V"]) > 1e-9]
    assert set(nz) >= {"Al2O3", "B2O3", "MoO3", "WO3"}, nz

    pin = json.loads((ROOT / "db/properties/oxidation_stability_cascade_v3_pinned.json")
                     .read_text(encoding="utf-8"))
    assert "attribution_closed_2026_08_16" not in pin, "'닫힘' 블록이 남아 있다"
    a = pin["attribution_status_2026_08_16"]
    assert a["element_level_causal_attribution"] == "not_claimed"
    assert a["approved_current_ranking"] == 0
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    g3 = man["metric_contract"]["G3"]
    assert "effect_attributable_chain_rows" not in g3, "한 숫자로 덮는 필드가 남아 있다"
    assert g3["element_level_causal_attribution"] == "not_claimed"


def test_g3_species_pass_is_split_from_attribution():
    """경고만 붙이고 species-level pass 를 유지하면 fail-open 이다 (Codex f9 P0-3)."""
    f = json.loads((ROOT / "db/properties/cascade_screening_funnel.json")
                   .read_text(encoding="utf-8"))
    gs = f["gates"] if isinstance(f.get("gates"), list) else f["gate_blocks"]
    a = [g for g in gs if g["id"] == "G3"][0]["attribution_audit"]
    assert a["g2_survivors"] == 43
    assert a["algorithmic_g3"] == {"pass": 25, "fail": 18}      # 역사 count 는 보존
    assert a["attribution_audit"] == {"supported_pass": 24, "fail": 18, "unresolved": 1}
    assert a["unresolved_species"] == ["B2O3"]
    # 깔때기 기계적 count 는 안 움직여야 한다 (해석만 바뀐 것)
    assert [len(f["pool"])] == [47]


def test_b2o3_page_does_not_claim_a_same_composition_validation():
    """도펀트 라벨만으로 두 조성을 validation 으로 잇지 않는다 (Codex f9 P0-3)."""
    j = D.CASCADE_JOIN_STATUS["b2o3"]
    assert j["validation_link_status"] == "different_composition"
    assert j["composition_match"] is False
    assert j["phase_set_match"] == "unverified"
    assert j["dft_deep_ox_V"] < j["host_ox_V"] < j["cascade_ox_V"], "부호 충돌이 사라졌다"
    c = A.app.test_client()
    h = c.get("/composition/b2o3").get_data(as_text=True)
    assert "Li58P8S41Cl16B2O3" in h and "Li17B2P4S16Cl5O3" in h, "두 조성식이 나란히 없다"
    assert "같은 조성의 검증이 아니다" in h
    assert "그 <b>DFT 심층검증</b>이에요" not in h, "옛 validation 문구가 남아 있다"
    # Nd2O3 는 plain 챔피언이라 이 경고를 달면 안 된다
    hn = c.get("/composition/modelc_nd_doped").get_data(as_text=True)
    assert "같은 조성의 검증이 아니다" not in hn


def test_chain_family_is_not_described_as_one_s_to_cl_swap():
    """17행을 하나의 S→Cl 치환군으로 말하면 거짓이다 (Codex P0-1). 10 exact / 7 multi."""
    pinned = json.loads((ROOT / "db/properties/oxidation_stability_cascade_v3_pinned.json")
                        .read_text(encoding="utf-8"))
    mt = pinned["composition_family_audit"]["matched_transform"]
    assert mt["counts"] == {"exact": 10, "multi_transform": 7}
    bases = sorted({r.split("_")[0] for r in mt["multi_transform_rows"]})
    assert bases == ["B2O3", "MoO3", "WO3"]
    for k, v in pinned["results"].items():
        if v.get("composition_family") == "Clrich":
            assert v["matched_transform_status"] in ("exact", "multi_transform",
                                                     "no_plain_candidate")
            assert v["contrast_scope"] == "multi_intervention_recipe_vs_host"
        elif v.get("composition_family") == "plain":
            assert v["contrast_scope"] == "primary_recipe_vs_host"
            assert v["isolated_dopant_effect"] is False   # plain 도 순수 도펀트 효과 아님

    rate = pinned["composition_family_audit"]["onset_raise_rate"]
    assert rate["enrichment_ratio"] == 9.63, "원계수에서 한 번만 반올림 (9.7 은 이중 반올림)"
    el = rate["eligible_slots_only"]
    assert (el["n_slots"], el["ratio"]) == (33, 2.59)
    assert "사후 기술통계" in rate["caveat"]

    # B2O3 충돌은 '순전히 조성 차이' 로 닫지 않는다
    col = pinned["dft_deep_composition_collision"]["B2O3"]
    assert col["dft_deep_cell"]["phase_set_id"] is None
    assert col["validation_link_status"] == "different_composition"
    b2 = json.loads((ROOT / "db/properties/b2o3_esw.json").read_text(encoding="utf-8"))
    assert b2["composition_collision_2026_08_16"]["phase_set_match"] == "unverified"

    # 화면 문구도 같이 (chain 전체를 단순 치환으로 단정하면 안 된다)
    h = _cascade_html()
    assert "10행" in h and "7행" in h, "exact/multi 분리가 화면에 없다"
    assert "9.7배" not in h, "이중 반올림 9.7 이 화면에 남아 있다"


def test_audit_generator_runs_without_windows_fonts():
    """C:/Windows/Fonts 하나에 묶여 Linux 에서 도구가 아예 안 돌았다 (2026-08-14)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "pca", ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    f = m._font(24, bold=True)
    assert f is not None
    assert m.resolved_font(), "어느 폰트를 썼는지 보고하지 않는다"
    # 폴백 체인에 Windows 밖 경로가 있어야 한다
    assert any(not r.startswith("C:") for _n, r, _b in m._FONT_CHAIN)
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert man["render_provenance"]["figure_font"], "원장에 폰트 provenance 가 없다"


def test_ledger_is_self_contained():
    """원장만 보면 되도록 — 계약 블록이 플로터 sidecar 에만 남아 있으면 안 된다."""
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    for k in ("datasets", "metric_contract", "source_hashes", "recovered_artifacts",
              "render_provenance", "artifacts", "figures", "supporting_tables"):
        assert k in man, f"원장에 {k} 가 없다"
    g = man["recovered_artifacts"]["_gate_completeness"]
    assert g["G3"]["method_status"] == "recovered_diagnostic"   # 2026-08-16 닫힘
    assert str(g["G5"]["validity_aware_all_label_species"]) == "86"
    assert all(str(v["approved_for_current_ranking"]) == "0" for v in g.values())


def test_audit_csvs_are_reproducible_from_the_generator():
    """손으로 고친 CSV 는 재현 불가다 — 생성기가 같은 내용을 만들어야 한다."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "pca2", ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    v = m._elastic_validity_by_species()
    assert v["all_label_valid"] == 86 and v["dropped"] == ["AlI3"]
    assert v["partial"] == ["AlBr3", "MgI2", "Na2S"] and v["usable"] == 89
    src = (ROOT / "tools" / "figures" / "plot_cascade_audit_2026_08.py").read_text(encoding="utf-8")
    assert 'lineterminator="\\n"' in src, "csv.writer 가 다시 CRLF 를 쓴다"
    assert '"phase_set_assumption"' in src, "G3 가정 열이 생성기에 없다"
    assert '"pool_id": "cascade-v23-o37-f10-2026-06"' in src, "G4 pool 메타가 생성기에 없다"


def test_db_property_files_are_lf_pinned():
    """깨끗한 Windows checkout 에서 CRLF 로 바뀌면 해시 대조가 깨진다 (P1)."""
    ga = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    # 광역 규칙(db/properties/*.csv)은 blob 이 CRLF 인 기존 80여 파일을 리플로우시켜서
    # 감사 원장이 해시로 묶는 파일에만 건다. 나머지 이식성은 sha256_lf 가 담당한다.
    assert "db/properties/cascade_audit_*.csv   text eol=lf" in ga
    assert "db/properties/cascade_audit_*.json  text eol=lf" in ga
    for p in sorted((ROOT / "db" / "properties").glob("cascade_audit_*.csv")):
        assert b"\r\n" not in p.read_bytes(), f"{p.name} 이 CRLF 다 (csv.writer 기본값 주의)"
    man = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    for a in man["artifacts"]:
        assert a.get("sha256_lf"), f"{a['source_path']} 에 LF 정규화 해시가 없다"


def test_gate_completeness_is_axis_specific():
    """축마다 분모가 다르다. G3 는 2026-08-16 에 0 → 90 으로 닫혔고, G4 는 아직 historical_only 다."""
    t = D.read_csv("properties/cascade_audit_gate_completeness.csv")
    by = {r["gate"]: r for r in (t.get("data") or [])}
    assert set(by) == {"G1", "G2", "G3", "G4", "G5"}, f"게이트 5개가 아니다: {sorted(by)}"
    assert by["G3"]["all_label_complete_species"] == 90
    assert by["G3"]["method_status"] == "recovered_diagnostic"
    assert "Cl-rich" in str(by["G3"]["note"]), "조성족 섞임이 G3 행에서 사라졌다"
    assert by["G4"]["dropped_species"] == "AlI3|MgI2", "G4 는 MgI2 도 결측이다 (x005 입력 없음)"
    for g, r in by.items():
        assert r["approved_for_current_ranking"] == 0, f"{g} 가 승인된 것처럼 적혀 있다"
    h = _cascade_html()
    assert "recovered_diagnostic" in h, "G3 method status 가 화면에 없다"


def test_lis4_exposure_is_quantified():
    """LiS4 가 든 onset 반응이 몇 건인지 세어 화면 주장과 맞는지 본다."""
    gp = json.loads((D.DB / "properties" / "oxidation_stability_cascade_v2.json")
                    .read_text(encoding="utf-8"))["results"]
    n = sum(1 for r in gp.values() if "LiS4" in (r.get("oxidation_onset_rxn") or ""))
    assert (n, len(gp)) == (124, 270), f"LiS4 노출이 바뀌었다: {n}/{len(gp)}"
    assert "124" in _cascade_html(), "LiS4 노출 수치가 화면에 없다"


def test_audit_figures_are_the_only_default_figures():
    """계약상 기본 공개가 허용된 그림은 5개 audit 패널뿐이다."""
    figs = (D.load_cascade().get("v2") or {}).get("audit_figures") or []
    assert len(figs) == 5, f"audit 패널이 5개가 아니다: {len(figs)}"
    c = A.app.test_client()
    for png, csvp, _t in figs:
        assert (ROOT / png).is_file() and (ROOT / csvp).is_file()
        assert c.get(f"/api/file/{png}").status_code == 200
        assert c.get(f"/api/file/{csvp}?dl=1").status_code == 200


def test_manifest_satisfies_the_audit_generator_contract():
    """manifest 는 Codex 플로터가 검증하는 schema_version 2 계약도 만족해야 한다."""
    m = json.loads(D.CASCADE_MANIFEST_PATH.read_text(encoding="utf-8"))
    assert m.get("schema_version") == 2
    assert m.get("source_commit") == "9abe5105cacafa22ab3e185f09e2a4c37118b9a9"
    assert m["headline"] == {
        "planned_slots": 273, "completed_slots": 270, "completed_species": 90,
        "historical_snapshot_species": 47,
        "approved_current_leaderboard_species": 0,
        "explicit_pair_property_labels": 0,
    }
    assert len(m.get("figures", [])) == 5, "audit figure/CSV 쌍은 정확히 5개여야 한다"
    import hashlib
    for it in m["figures"]:
        for key, hkey in (("image", "image_sha256"), ("csv", "csv_sha256")):
            b = (ROOT / it[key]).read_bytes()
            assert hashlib.sha256(b).hexdigest() == it[hkey], f"{it[key]} 무결성 실패"


def test_legacy_rank_is_labelled_wherever_it_leaks():
    """composition·elements 가 47종 rank 를 상태 없이 현재 판정처럼 보여주면 안 된다."""
    c = A.app.test_client()
    comp = c.get("/composition/b2o3").get_data(as_text=True)
    assert "🤖 Cascade hit" not in comp, "'Cascade hit' 배지가 되살아났다"
    assert "superseded 47종 스냅샷" in comp, "composition 에 지위 표시가 없다"
    el = c.get("/elements").get_data(as_text=True)
    assert "historical 47종" in el, "elements 카드에 지위 표시가 없다"


def test_superseded_and_diagnostic_tabs_are_labelled():
    """47종 판은 superseded, 90종 회수분은 미검증 diagnostic 으로 라벨링돼야 한다."""
    h = _cascade_html()
    assert "superseded 보관함" in h, "47종 리더보드에 superseded 경고가 없다"
    assert "Recovered · unvalidated diagnostic" in h, "90종 탭에 diagnostic 배지가 없다"
    for f, want in [("cascade_screening_funnel.json", "superseded_47species"),
                    ("cascade_screening_funnel_v2.json", "recovered_unvalidated_diagnostic"),
                    ("cascade_v23_themes.json", "superseded_47species"),
                    ("cascade_v23_themes_v2.json", "recovered_unvalidated_diagnostic")]:
        d = json.loads((D.DB / "properties" / f).read_text(encoding="utf-8"))
        assert d.get("status") == want, f"{f} status={d.get('status')} — {want} 이어야 한다"


def test_esw_tab_reads_the_file_its_badge_claims():
    """탭 배지는 90종인데 표는 47종 파일을 읽고 있었다 (Codex 리뷰 P0-2)."""
    casc = D.load_cascade()
    v2ox = (casc.get("v2") or {}).get("oxidation") or {}
    assert len(v2ox.get("data") or []) == 90, "ESW v2 가 90행이 아니다"
    assert len(casc["oxidation"].get("data") or []) < 90, "v1 이 90행이면 이 대비가 무의미"
    h = _cascade_html()
    assert "oxidation_stability_cascade_v2.csv" in h, "ESW 탭이 어느 파일을 쓰는지 안 적혀 있다"
    assert "mp-ID" in h, "ESW phase-set 미기록 한계가 화면에 없다"


def test_page_scope_names_the_real_host_and_concentration():
    """호스트는 Cl:P=1.0 (Li6PS5Cl 계열)이고 라벨 x002/x005/x010 은 셋 다 실측 x=0.25 다."""
    s = D.CASCADE_META["scope"]
    assert "Li₆PS₅Cl" in s and "Cl:P = 1.0" in s, f"호스트 표기가 틀렸다: {s}"
    assert "0.25" in s, "농도 라벨 정정이 scope 에 없다"
    assert "Li₅.₄PS₄.₄Cl₁.₆" not in s, "Model C 로 되돌아갔다"
    for f in ("cascade_screening_funnel.json", "cascade_screening_funnel_v2.json"):
        g4 = [g for g in json.loads((D.DB / "properties" / f).read_text(encoding="utf-8"))["gates"]
              if g["id"] == "G4"][0]
        assert "@x=0.05)" not in g4["metric"], f"{f} G4 metric 이 'x=0.05' 로 되돌아갔다"


def test_g4_circularity_is_stated():
    """blocking 탈락자는 transport_norm 이 0.05 로 강제된다 — 두 독립 신호가 아니다 (P0-5)."""
    src = (ROOT / "tools" / "cascade" / "build_screening_funnel.py").read_text(encoding="utf-8")
    assert "n = GATE_FLOOR" in src, "순환을 만드는 코드가 사라졌다 — 이 테스트를 갱신할 것"
    assert D.G4_DECOMP.get("circularity"), "G4_DECOMP 에 순환 설명이 없다"
    h = _cascade_html()
    assert "독립 두 신호의 AND 가 아니다" in h, "G4 순환이 화면에 없다"


def test_remaining_tabs_declare_their_state():
    """champions·themes·stability·co-doping 이 archive 표시 없이 current 처럼 뜨면 안 된다 (P0-4)."""
    h = _cascade_html()
    for panel, probe in [("tab-champ", "cascade_v23_champions.csv (141행 · 47종)"),
                         ("tab-theme", "cascade_v23_themes.json (47종)"),
                         ("tab-stab", "47종 풀 위에서 돌린 후처리 축"),
                         ("tab-syn", "explicit pair 라벨이 0개다")]:
        assert probe in h, f"{panel} 에 상태 배너가 없다"


def test_g4_is_not_called_li_transport():
    """G4 는 정적 프록시 두 개다. '전도도를 쟀다'로 읽히는 이름을 되살리지 말 것."""
    h = _cascade_html()
    assert "🔋 Li transport" not in h, "탭 이름이 'Li transport' 로 되돌아왔다"
    # 옛 이름은 **폐기 안내문 안에서만** 나와도 된다 — 살아있는 라벨로 다시 쓰이면 안 된다.
    for m in re.finditer("Li 수송 유지", h):
        ctx = h[max(0, m.start() - 260):m.end() + 260]
        assert "폐기" in ctx, f"G4 옛 라벨이 정정 문맥 없이 살아 있다: …{ctx[200:420]}…"
    assert "Adams-2003" in h, "legacy BVS 파라미터 경고가 화면에 없다"
    assert "4 Å foreign-center" in h, "blocking 프록시의 실제 정의가 화면에 없다"
    for f in ("cascade_screening_funnel.json", "cascade_screening_funnel_v2.json"):
        g4 = [g for g in json.loads((D.DB / "properties" / f).read_text(encoding="utf-8"))["gates"]
              if g["id"] == "G4"][0]
        assert "Li 수송" not in g4["label"], f"{f} 의 G4 label 이 되돌아갔다: {g4['label']}"


def test_v2_json_text_does_not_inherit_47_species():
    """빌더가 풀 크기를 하드코딩하면 _v2 설명문만 47종으로 남아 화면이 스스로 모순된다."""
    for f in ("cascade_screening_funnel_v2.json", "cascade_v23_themes_v2.json"):
        d = json.loads((D.DB / "properties" / f).read_text(encoding="utf-8"))
        for key in ("description", "honesty_header"):
            if key in d:
                assert "47종" not in d[key], f"{f}[{key}] 에 '47종' 이 남아 있다"
    d = json.loads((D.DB / "properties" / "cascade_screening_funnel_v2.json").read_text(encoding="utf-8"))
    assert d["pool_provenance"]["pool_size"] == 89, "v2 풀 크기가 89 가 아니다"


def test_gate_audit_counts_only_columns_the_gates_use():
    """옛 감사는 gate 가 **안 쓰는** eos_B0_GPa 를 세고 쓰는 pugh 를 빼서 18종을 부분결측으로
    만들었다 (Codex 리뷰 P0-3). 게이트 입력 정의가 다시 어긋나면 여기서 잡는다."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "rpi", ROOT / "tools" / "cascade" / "rebuild_pool_inputs.py")
    rpi = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rpi)
    champ = set(rpi.GATE_INPUT_COLS["champions"])
    assert "elastic_pugh_GoverB" in champ, "G5 연성축(pugh)이 gate 입력에서 빠졌다"
    assert "eos_B0_GPa" not in champ, "eos_B0_GPa 는 어느 게이트도 쓰지 않는다 — 세면 안 된다"
    assert "eos_B0_GPa" in rpi.NON_GATE_COLS


def test_missing_gate_inputs_are_on_the_default_screen():
    """AlI3 전면 결측 · MgI2 부분 결측 · blocking=0 아티팩트는 기본 화면에 떠 있어야 한다."""
    h = _cascade_html()
    aud = json.loads((D.DB / "properties" / "cascade_pool_audit_v2.json").read_text(encoding="utf-8"))
    assert aud["n_esw"] == 90 and aud["n_evaluable"] == 89
    assert list(aud["dropped"]) == ["AlI3"] and list(aud["partial"]) == ["MgI2"]
    assert aud["n_complete"] == 88
    head = h.split('id="tab-esw"')[0]          # 기본(감사) 화면 범위 안에서만 찾는다
    for probe in ("AlI3", "MgI2", "Li2S", "LiCl"):
        assert probe in head, f"{probe} 가 기본 감사 화면에 없다"


def _cmt_worker_tmp(arg):
    path, rel, i = arg
    D.COMMENTS_PATH = Path(path)          # 자식 프로세스에도 임시 경로를 심는다
    return D.add_file_comment(rel, f"pytest heavy {i}", "pytest")


def _cmt_worker(arg):
    rel, i = arg
    return D.add_file_comment(rel, f"pytest concurrency {i}", "pytest")


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if not (name.startswith("test_") and callable(fn)):
            continue
        try:
            fn()
            print(f"  ✅ {name}")
        except AssertionError as e:
            fails += 1
            print(f"  ⛔ {name}\n       {str(e)[:400]}")
        except Exception as e:
            fails += 1
            print(f"  ⛔ {name} (예외) {type(e).__name__}: {str(e)[:300]}")
    print(f"\n{'✅ 전부 통과' if not fails else f'⛔ 실패 {fails}건'}")
    sys.exit(1 if fails else 0)


# ── 여백 메모 (docnote) ────────────────────────────────────────────────────
#  2026-08-17 1저자 요청: "오른쪽클릭하면 word 처럼 옆에 메모", "search 에서 잡히게",
#  "메모 섹션에서 링크 걸어서 그 메모가 써져있는 페이지로".
#  전부 **한 번 틀릴 수 있는 지점**이라 음성 경로를 같이 건다.
def test_docnote_roundtrip(tmp_path, monkeypatch):
    """메모를 달면 → 검색 색인에 뜨고 → 딥링크가 그 메모를 가리켜야 한다."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    rel = "litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md"
    r = D.add_file_comment(rel, "우리 §20.3 오타 얘기와 같은 건", anchor="Rh · Ho 는 애초에 논문 문제가")
    assert r.get("ok"), r
    nid = r["item"]["id"]
    assert r["item"]["anchor"] == "Rh · Ho 는 애초에 논문 문제가"

    # ① /literature 카드 색인에 '@' 키로 들어간다 (그림 코멘트와 구분되는 키)
    idx = D.paper_comment_search()["anderson2024_llzo_comprehensive_dopant_screening"]
    assert idx.startswith("@ "), idx[:40]
    assert "오타" in idx and "애초에" in idx, "메모 글과 붙인 자리가 **둘 다** 색인돼야 한다"

    # ② 딥링크가 그 메모 id 를 달고 나간다
    c = [x for x in D.comment_all() if x["id"] == nid][0]
    assert D.note_url(c) == f"/literature?open=anderson2024_llzo_comprehensive_dopant_screening&note={nid}"

    # ③ 날짜별로 묶인다
    g = D.notes_by_date()
    assert any(any(i["id"] == nid for i in grp["items"]) for grp in g)


def test_docnote_negative(tmp_path, monkeypatch):
    """음성 경로 — 틀린 입력을 잡아내는지."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    # 없는 파일에는 못 단다 (경로 탈출·유령 키 방어)
    assert D.add_file_comment("litdb/papers/__없는논문__.md", "x", anchor="y").get("error")
    # anchor 없는 코멘트는 anchor 키 자체가 없어야 한다 (옛 기록과 같은 모양)
    D.add_file_comment("db/properties/electronic.json", "그냥 코멘트")
    c = [x for x in D.comment_all() if x["rel"] == "db/properties/electronic.json"][0]
    assert not c["anchor"]
    # → 딥링크에 note= 가 붙으면 안 된다 (붙일 자리가 없다)
    assert "note=" not in D.note_url(c)
    # 그림도 아니고 문서도 아닌 파일은 /files 로 간다
    assert D.comment_origin("db/properties/electronic.json")["kind"] == "파일"
    # 4칸이 아닌 figures 경로를 논문으로 오인하면 안 된다
    assert D.comment_origin("litdb/figures/slug/sub/x.png")["kind"] == "파일"
    # papers 밑이어도 .md 가 아니면 논문이 아니다
    assert D.comment_origin("litdb/papers/x.png")["kind"] == "파일"


def test_notes_page_renders(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    D.add_file_comment("kb/concepts/bvse.md", "여기 R0 값 출처 확인", anchor="softBV")
    A.app.config["TESTING"] = True
    h = A.app.test_client().get("/notes").get_data(as_text=True)
    assert "여기 R0 값 출처 확인" in h
    assert "/concept/bvse?note=" in h, "메모 카드가 그 자리로 가는 딥링크여야 한다"


def test_note_target_gate_is_narrower_than_file_serving():
    """메모 게이트를 넓히다가 **다운로드 화이트리스트**까지 넓히면 안 된다.

    safe_repo_path 는 /api/file 이 쓰는 경로다 — 여기 kb/ 가 들어가면 배포판에서
    kb 전체를 내려받을 수 있게 된다. 두 게이트가 갈려 있는지 못으로 박는다.
    """
    doc = "litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md"
    assert D.safe_note_target(doc) is not None, "메모는 digest 에 달려야 한다"
    assert D.safe_repo_path(doc) is None, "그런데 /api/file 로는 여전히 못 준다"
    assert D.safe_note_target("kb/concepts/bvse.md") is not None
    assert D.safe_repo_path("kb/concepts/bvse.md") is None
    # 음성: 경로 탈출·하위폴더·비-md·화이트리스트 밖
    assert D.safe_note_target("kb/concepts/../../etc/passwd") is None
    assert D.safe_note_target("litdb/papers/sub/x.md") is None
    assert D.safe_note_target("litdb/papers/x.png") is None
    assert D.safe_note_target("kb/results/sei_cc333_nd_lattice_hop_2026_08_17.md") is None
    assert D.safe_note_target("CLAUDE.md") is None


def test_comment_post_and_get_agree(tmp_path, monkeypatch):
    """POST 응답과 GET 응답이 **같은 색인**을 실어야 한다.

    앞 판은 POST 에만 paper 색인이 없어서, 화면이 POST 결과로 검색 색인을
    갱신하려 하면 조용히 헛돌았다 (뒤따르는 GET 이 덮어 증상만 가렸다).
    """
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    A.app.config["TESTING"] = True
    c = A.app.test_client()
    rel = "litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md"
    post = c.post("/api/comments/" + rel, json={"text": "메모", "anchor": "닻"}).get_json()
    get = c.get("/api/comments/" + rel).get_json()
    assert post["paper"] == get["paper"], (post.get("paper"), get.get("paper"))
    assert post["paper"]["cmt"].startswith("@ ")


def test_docnote_edit_keeps_history(tmp_path, monkeypatch):
    """메모 고치기 — 옛 글이 **지워지지 않고** history 에 쌓여야 한다."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    rel = "kb/concepts/bvse.md"
    r = D.add_file_comment(rel, "첫 판단", anchor="softBV")
    cid = r["item"]["id"]

    e = D.edit_file_comment(rel, cid, "다시 보니 R0 출처가 다름")
    assert e.get("ok"), e
    it = e["item"]
    assert it["text"] == "다시 보니 R0 출처가 다름"
    assert it["history"][0]["text"] == "첫 판단", "옛 글이 남아야 한다"
    assert it["edited_at"]
    assert it["id"] == cid and it["anchor"] == "softBV", "id·자리는 안 바뀐다 (딥링크 유지)"

    # 두 번 고치면 이력이 두 판
    D.edit_file_comment(rel, cid, "세 번째")
    it = D.file_comments(rel)[0]
    assert [h["text"] for h in it["history"]] == ["첫 판단", "다시 보니 R0 출처가 다름"]

    # 검색(⌘K)은 **지금 글**로 걸린다 — 옛 글이 label 에 남으면 안 된다.
    # ⚠ 개념 메모는 paper_comment_search(litdb 전용)가 아니라 search_index 담당이다.
    labels = [i["label"] for i in D.search_index() if i["t"] == "메모"]
    assert any("세 번째" in x for x in labels)
    assert not any("첫 판단" in x for x in labels)


def test_docnote_edit_negative(tmp_path, monkeypatch):
    """음성 경로 — 틀린 입력을 잡아내는지."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    rel = "kb/concepts/bvse.md"
    cid = D.add_file_comment(rel, "원본", anchor="a")["item"]["id"]
    assert D.edit_file_comment(rel, "없는id", "x").get("error"), "없는 id 는 거절"
    assert D.edit_file_comment("kb/concepts/없는문서.md", cid, "x").get("error"), "없는 파일은 거절"
    assert D.edit_file_comment(rel, cid, "   ").get("error"), "빈 글은 거절"
    # 같은 글로 고치면 이력을 늘리지 않는다 (헛 판 쌓임 방지)
    r = D.edit_file_comment(rel, cid, "원본")
    assert r.get("unchanged") and not r["item"].get("history")
    assert D.file_comments(rel)[0]["text"] == "원본", "실패해도 원본이 안 망가진다"


def test_docnote_edit_over_http(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    A.app.config["TESTING"] = True
    c = A.app.test_client()
    rel = "litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md"
    cid = c.post("/api/comments/" + rel,
                 json={"text": "처음", "anchor": "닻"}).get_json()["item"]["id"]
    r = c.patch("/api/comments/" + rel, json={"id": cid, "text": "고침"})
    assert r.status_code == 200
    d = r.get_json()
    assert d["item"]["text"] == "고침"
    assert d["paper"]["cmt"].startswith("@ "), "PATCH 도 색인을 같이 준다"
    assert "고침" in d["paper"]["cmt"] and "처음" not in d["paper"]["cmt"]
    assert c.patch("/api/comments/" + rel,
                   json={"id": "없는거", "text": "x"}).status_code == 400


def test_sidebar_rail_toggle_present_and_layered():
    """사이드바 접기 — 버튼·토글·peek 이 모든 페이지에 있고, 층위가 맞아야 한다.

    ⚠ peek 띠의 z-index 가 사이드바(40)보다 높으면 드러난 사이드바의 왼쪽 14px
      클릭이 투명 띠에 먹혀 메뉴를 못 누른다 (2026-08-18 설계 중 실측).
    """
    import re
    A.app.config["TESTING"] = True
    c = A.app.test_client()
    for url in ("/", "/glossary", "/notes", "/literature"):
        h = c.get(url).get_data(as_text=True)
        assert 'id="railbtn"' in h, url
        assert "function toggleRail" in h, url

    css = (D.ROOT / "webapp" / "static" / "css" / "style.css").read_text(encoding="utf-8")
    z_side = int(re.search(r"\.sidebar\{[^}]*z-index:(\d+)", css, re.S).group(1))
    z_peek = int(re.search(r"\.rail-peek\{[^}]*z-index:(\d+)", css, re.S).group(1))
    assert z_peek < z_side, f"peek({z_peek}) 가 사이드바({z_side}) 위에 있으면 클릭을 먹는다"

    # ★ 꽉 차려면 margin-left 와 max-width 를 **둘 다** 풀어야 한다.
    #   margin 만 지우면 max-width:1240px 때문에 가운데에 갇힌다.
    rail = re.search(r"body\.rail \.content\{([^}]*)\}", css).group(1)
    assert "margin-left:0" in rail, rail
    assert "max-width:none" in rail, rail
