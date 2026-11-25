"""test_v3_composition.py — v3 묶음 D (조성 상세 + 구조·파일 목록) 회귀시험.

무엇을 지키나
  ① `copyComp` 복사문에 **지위가 값과 한 몸으로** 나간다 (P0-04)
  ② Nd ICOHP 표가 CUTOFF ARTIFACT 정정본을 쓴다 — 옛 값은 접힘 + 취소선 (P0-05)
  ③ 조건부 보류된 절대 E_ads 가 헤드라인으로 그냥 뜨지 않는다 (P0-08)
  ④ 다른 계열의 축이 전 조성에 TODO 로 광고되지 않는다 (P0-09)
  ⑤ `ndo_*` Nd 어닐 구조가 화면에 돌아왔고, li3n/vgcf_hbn 소유가 갈렸다
  ⑥ bader 만 있는 ICOHP JSON 에 페이지가 500 이 나지 않는다

⛔ 이 파일이 **못 하는 것**
  · 브라우저를 안 띄운다. 3D 뷰어·Plotly·접힘 애니메이션의 실동작은 못 본다 —
    검사하는 것은 서버가 내려보낸 HTML 문자열이다.
  · 값이 물리적으로 맞는지 보지 않는다. **지위·표기·소유**만 본다.
  · 원장이 파일 단위로만 적어 둔 금지를 값 단위로 좁혀 주지 못한다(그건 원장 일이다).

⚠ 음성 경로(틀린 입력을 잡아내는지)를 반드시 같이 시험한다.
"""
import os
import re
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as A                       # noqa: E402
import canonical as C                 # noqa: E402
import data as D                      # noqa: E402
import decisions_view as V            # noqa: E402


@pytest.fixture()
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


_JS_U = re.compile(r"\\u([0-9a-fA-F]{4})")


def _copy_body(html: str) -> str:
    r"""`copyComp` 본문 — JS 문자열의 `\uXXXX` 는 되돌려 읽는다.

    ⚠ 값·사유를 `|tojson` 으로 싣기 때문에(따옴표·줄바꿈이 들어 있어 그래야 한다)
      HTML 원문에는 한글이 이스케이프돼 있다. 검사는 **실행 시 클립보드에 들어갈 문자열**
      을 봐야 하므로 여기서 되돌린다.
    """
    m = re.search(r"function copyComp\(\)\{.*?\n\}", html, re.S)
    assert m, "copyComp 함수가 화면에서 사라졌다"
    return _JS_U.sub(lambda x: chr(int(x.group(1), 16)), m.group(0))


# ═══════════════════════════════════════════════════════════════════════════
# ① P0-04 — 복사 경로에도 지위가 실린다
# ═══════════════════════════════════════════════════════════════════════════
def test_copy_carries_retraction(client):
    """★ 철회 셀 복사문에 철회 표시가 없으면 실패.

    실측(2026-09-09): `/composition/b2o3` 의 '📋 값 복사' 가 철회값 0.199 를 내보내면서
    마지막 줄에 `(canonical, 방법 표기 포함)` 꼬리표까지 붙였다 — 배지는 화면에만
    있었고 **클립보드에는 없었다**.
    """
    body = _copy_body(client.get("/composition/b2o3").get_data(as_text=True))
    line = [ln for ln in body.split('+"\\n";') if "0.199" in ln]
    assert line, "b2o3 복사문에 MD Ea 줄이 없다 (전제가 깨졌다)"
    assert "철회" in line[0], f"⛔ 철회값 줄에 철회 표시가 없다: {line[0][:200]}"
    assert "대신 쓸 값" in line[0], "대체값(또는 '대체값 없음')이 같이 안 나간다"
    assert "(canonical, 방법 표기 포함)" not in body, \
        "⛔ 철회값이 섞였는데 꼬리말이 여전히 canonical 을 자칭한다"


def test_copy_does_not_over_mark(client):
    """★ 음성 — 멀쩡한 정본값에 금지 딱지가 붙으면 그것도 고장이다.

    과잉 차단은 '안전' 이 아니라 다른 종류의 거짓말이다. comp1 은 철회 항목이 없다.
    """
    body = _copy_body(client.get("/composition/comp1").get_data(as_text=True))
    assert "⛔ 철회 — 인용 금지" not in body, "정본 조성 복사문에 철회 표식이 생겼다"
    assert "인용 금지 값 포함" not in body, "금지 항목이 없는데 금지 꼬리말이 붙었다"
    # comp1 에는 잠정 항목(MD Ea 단일시드 앵커)이 하나 있다 — 그건 **표시돼야** 맞다
    assert "잠정" in body, "잠정 항목의 지위까지 지워 버렸다"


def test_copy_lines_is_derived_from_the_ledger():
    """★ 음성 — 원장에 없는 metric 은 아무 표식도 받지 않는다(지어내지 않는다)."""
    rows = V.copy_lines("b2o3", {"NO_SUCH_METRIC": 1.0}, {"NO_SUCH_METRIC": "가짜"},
                        {"NO_SUCH_METRIC": "eV"})
    assert rows and rows[0]["clean"] is True, "원장에 없는 축에 지위가 붙었다"
    assert "⛔" not in rows[0]["text"] and "⚠" not in rows[0]["text"]


# ═══════════════════════════════════════════════════════════════════════════
# ② P0-05 — CUTOFF ARTIFACT 정정본 승격
# ═══════════════════════════════════════════════════════════════════════════
def test_nd_icohp_table_uses_the_corrected_values(client):
    h = client.get("/composition/modelc_nd_doped").get_data(as_text=True)
    assert "-1.647" in h and "-2.132" in h, "정정본 Li-S/Li-Cl 이 화면에 없다"
    for stale in ("-2.493", "-2.265"):
        for m in re.finditer(re.escape(stale), h):
            near = h[max(0, m.start() - 500):m.start()]
            assert "CUTOFF ARTIFACT" in near, \
                f"⛔ 정정 전 값 {stale} 이 경고 없이 찍힌다 (앞 500자에 정정 문구 없음)"


def test_promotion_needs_an_explicit_correction_record():
    """★ 음성 — 정정 문구가 없으면 **아무것도 승격하지 않는다**.

    승격은 원장이 "Correct values below" 라고 적었을 때만 하는 일이다. 키 이름만 보고
    올리면 비교용 부속표가 조용히 정본이 된다.
    """
    d = {"bonds": {"Li-S": {"ICOHP_total_eV_per_bond": -9.0}},
         "bonds_4.0A_cutoff_for_comparison": {"Li-S": {"icohp_eV": -1.0, "n_bonds": 3}}}
    out = D._promote_corrected_bonds(dict(d))
    assert out["bonds"]["Li-S"]["ICOHP_total_eV_per_bond"] == -9.0, "정정 기록 없이 승격됐다"
    assert "bonds_superseded" not in out

    d["_CORRECTION_TEST"] = "Previous values were CUTOFF ARTIFACTS. Correct values below"
    out2 = D._promote_corrected_bonds(dict(d))
    assert out2["bonds"]["Li-S"]["ICOHP_total_eV_per_bond"] == -1.0, "정정본이 안 올라왔다"
    assert out2["bonds"]["Li-S"]["N"] == 3, "n_bonds → N 정규화가 안 됐다"
    assert out2["bonds_superseded"]["Li-S"]["ICOHP_total_eV_per_bond"] == -9.0, \
        "옛 표가 사라졌다 — 접는 건 되고 지우는 건 안 된다"


# ═══════════════════════════════════════════════════════════════════════════
# ③ P0-08 — 조건부 보류된 절대 E_ads
# ═══════════════════════════════════════════════════════════════════════════
def test_absolute_eads_is_marked_as_held(client):
    h = client.get("/composition/sdcp").get_data(as_text=True)
    i = h.find("-0.7675")
    assert i > 0, "sdcp 절대 E_ads 가 화면에서 사라졌다 (숨기는 건 답이 아니다)"
    seg = h[i:i + 900]
    assert "보류" in seg, "⛔ 조건부 보류된 절대 E_ads 가 아무 표시 없이 헤드라인으로 뜬다"
    assert "인용하지 않아요" in seg or "인용 보류" in seg, \
        "보류 사유가 툴팁에만 있고 본문에 없다"


def test_hold_does_not_spread_to_the_site_contrast():
    """★ 음성 — 같은 파일의 자리대비(dE_site)까지 보류로 번지면 안 된다.

    원장이 그 축은 **영향 없다**고 명시했다(복합체끼리 차라 δ_m·δ_LREAL 이 소거된다).
    파일 단위 위험을 값 단위 금지로 번역하는 것이 이 화면에서 제일 흔한 과잉이다.
    """
    nt = V.metric_notices("sdcp")
    assert nt["SDCP_Eads_eV__sdcp_neutral_Litop"]["hold"] is True
    assert nt["SDCP_dE_site_meV__ptfe_c10_pm1"]["hold"] is False, \
        "자리대비까지 보류로 번졌다 — 원장은 영향 없다고 적었다"


# ═══════════════════════════════════════════════════════════════════════════
# ④ P0-09 — metric 곱집합
# ═══════════════════════════════════════════════════════════════════════════
def test_other_family_axes_are_not_advertised_as_todo(client):
    """SDCP 분자 metric 이 LPSCl 페이지에서 '미계산' 으로 광고되면 안 된다."""
    mm = D.metric_meta()
    sdcp_label = mm["SDCP_Eads_eV__ptfe_c10_Nitop"]["label"]
    h = client.get("/composition/comp1").get_data(as_text=True)
    assert "다른 계열의 축" in h, "다른 계열 축 접힘 줄이 없다"
    # 라벨은 접힘 안에 남아 있어야 한다(삭제 금지) — 단 TODO 타일은 아니어야 한다
    assert sdcp_label in h, "분자계 축이 통째로 사라졌다 — 접는 것과 지우는 것은 다르다"
    tiles = re.findall(r'<div class="metric todo"><div class="mv">TODO</div>'
                       r'<div class="ml">([^<]*)</div>', h)
    assert sdcp_label not in tiles, "⛔ 분자계 축이 여전히 TODO 타일로 광고된다"


def test_same_family_gaps_stay_visible_as_todo():
    """★ 음성 — 같은 계열의 미계산 축까지 접어 버리면 '안 한 일' 이 사라진다.

    comp3(argyrodite)은 gap_eV 값이 없지만, 같은 계열에 등록된 축이므로 TODO 로
    남아야 한다. 이게 접히면 접기 규칙이 과잉이다.
    """
    fams = {k: v.get("family") for k, v in D.COMPOSITIONS.items()}
    vals = D.canonical_values("comp3")
    other = V.other_family_axes("comp3", fams, vals,
                                {k for (k, c) in D.CANONICAL_NA if c == "comp3"})
    assert "gap_eV" not in other, "같은 계열의 미계산 축까지 접혔다"
    assert any(m.startswith("SDCP_") for m in other), "분자계 축이 안 접혔다"


def test_na_is_not_drawn_the_same_as_todo(client):
    """TODO(안 했다) · N/A(성립 안 한다) · 철회(했는데 못 쓴다) 를 같은 기호로 쓰지 않는다."""
    h = client.get("/composition/li3n").get_data(as_text=True)
    assert 'class="metric na"' in h, "N/A 타일이 TODO 와 같은 클래스로 그려진다"
    assert "UMA MLIP 금지 조성" in h, "N/A 사유 문장이 사라졌다"


# ═══════════════════════════════════════════════════════════════════════════
# ⑤ 파일 소유 — ndo prefix · li3n/vgcf_hbn
# ═══════════════════════════════════════════════════════════════════════════
def test_nd_anneal_structures_are_visible_again():
    names = [s["name"] for s in D.structures_for("modelc_nd_doped")]
    assert any(n.startswith("ndo_") for n in names), \
        "09-08 Nd 어닐/Rietveld 구조가 여전히 화면에서만 사라져 있다"
    # 음성 — 남의 페이지로 새면 안 된다
    for cid in ("modelc", "comp1", "b2o3"):
        assert not any(s["name"].startswith("ndo_") for s in D.structures_for(cid)), \
            f"{cid} 가 Nd 구조를 끌어갔다"


def test_li3n_files_have_one_owner():
    """★ 같은 CSV 가 두 조성 페이지에 동시에 뜨면 어느 쪽이 주인인지 화면이 말할 수 없다."""
    v = {d["name"] for d in D.datafiles_for("vgcf_hbn")}
    l3 = {d["name"] for d in D.datafiles_for("li3n")}
    assert not [n for n in v if n.startswith("li3n_")], \
        "vgcf_hbn 이 아직 li3n_* 자료를 자기 것으로 들고 있다"
    assert [n for n in l3 if n.startswith("li3n_")], "li3n 페이지가 자기 자료를 잃었다"


def test_structure_groups_collapse_formats_and_split_vesta():
    g = D.structure_groups("lpsocl")
    assert g["total"] < len(D.structures_for("lpsocl")), "형식 묶기가 전혀 안 됐다"
    for grp in g["groups"]:
        for it in grp["rows"]:
            assert "vesta" not in [f["ext"] for f in it["files"]], \
                "⛔ .vesta 가 3D 줄에 남아 있다 (파서가 없어 눌러도 안 열린다)"
            if it["view"]:
                assert it["view"]["fmt"], "view 로 뽑힌 파일에 파서가 없다"


# ═══════════════════════════════════════════════════════════════════════════
# ⑥ 방어 — bader 만 있는 ICOHP JSON
# ═══════════════════════════════════════════════════════════════════════════
def test_bader_only_json_does_not_500(client, monkeypatch):
    """★ 음성 경로 — 지금 500 이 안 나는 건 우연(비교표가 늘 같이 있었다)이었다."""
    fake = {"system": "fake", "method": "test",
            "bonds": {"Li-S": {"N": 4, "ICOHP_total_eV_per_bond": -2.0}},
            "bader": {"Li": 0.83, "S": -1.1, "n_Li": 4}}
    monkeypatch.setattr(D, "icohp_for", lambda cid: dict(fake))
    r = client.get("/composition/comp1")
    assert r.status_code == 200, "비교표 없는 bader JSON 하나에 페이지가 죽는다"
    assert "Bader 전하" in r.get_data(as_text=True)


# ═══════════════════════════════════════════════════════════════════════════
# ⑦ 살아 있는 결정 스트립
# ═══════════════════════════════════════════════════════════════════════════
def test_live_decisions_strip_is_on_the_page(client):
    live = V.decisions_for("lpsocl")["live"]
    assert live, "전제: lpsocl 에 active 결정이 있다"
    h = client.get("/composition/lpsocl").get_data(as_text=True)
    for d in live:
        assert f'href="/governance#{d["id"]}"' in h, f"{d['id']} 이 화면에서 안 걸린다"
    assert "db/properties/lpsocl_box331_closure_conditions" in h or "닫힘 조건" in h, \
        "닫힘 조건 카드가 조성 페이지에 없다"


def test_global_policies_are_counted_not_pasted(client):
    """★ 전 계 공통 정책(applies_to.systems = '*')을 조성마다 펼치면 고유 판정이 파묻힌다."""
    got = V.decisions_for("lpsocl")
    assert got["n_global"] >= 5, "전 계 정책 카운트가 안 잡힌다"
    assert not [d for d in got["live"] if d["id"] == "D-2026-08-20-source-authority"], \
        "와일드카드 정책이 조성 결정 목록으로 샜다"


def test_decisions_view_selftest_passes():
    """도구가 자기 음성 경로를 스스로 돌린다 (`python3 webapp/decisions_view.py`)."""
    assert V._selftest() == 0
