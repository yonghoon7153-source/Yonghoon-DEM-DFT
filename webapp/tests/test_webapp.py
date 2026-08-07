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


def test_all_get_routes_200():
    c = A.app.test_client()
    bad = []
    for u in _routes():
        try:
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
def test_mutations_locked_by_default():
    """인증이 없으므로 기본은 읽기 전용이어야 한다 (공개 Render 배포)."""
    c = A.app.test_client()
    assert A.READ_ONLY is True, "ALLOW_MUTATIONS 없이 쓰기가 열려 있다"
    probes = [("POST", "/api/comments/db/properties/electronic.json", {"json": {"text": "x"}}),
              ("DELETE", "/api/comments/db/properties/electronic.json?id=x", {}),
              ("POST", "/api/log", {"json": {"kind": "note", "text": "x"}}),
              ("POST", "/api/file-rename", {"json": {"rel": "a", "name": "b"}}),
              ("POST", "/api/concept-upload/dft", {})]
    for m, u, kw in probes:
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
    i = src.find("def _alive(")
    assert i > 0, "_alive() 가 사라졌다"
    body = src[i:i + 2600]
    assert 'os.name == "nt"' in body, "_alive() 에 Windows 분기가 없다"
    nt = body[body.index('os.name == "nt"'):]
    nt = nt[:nt.index("os.kill(")] if "os.kill(" in nt else nt
    assert "OpenProcess" in nt and "WaitForSingleObject" in nt, \
        "Windows 분기가 OpenProcess/WaitForSingleObject 를 안 쓴다"
    # os.kill 은 Windows 분기 **밖**에만 있어야 한다
    assert "os.kill" not in nt, "Windows 분기 안에서 os.kill 을 쓴다 — 프로세스를 죽인다"


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
