#!/usr/bin/env python3
"""test_v3_compute.py — v3 묶음 K(/compute 생성기)의 회귀 시험.

여기 담은 건 전부 **실제로 나가고 있던 것**이다 (2026-09-08 전수조사 P0-23·24·25 + 폴백).
  · MD 스크립트가 존재하지 않는 fairchem API(`OCPCalculator`)를 불렀다 — 첫 import 에서 죽는다
  · 같은 화면이 "--save_traj 없이 돌리지 않는다" 를 가르치는데 그 화면이 만든 스크립트에
    궤적 저장이 없었다
  · 9회 루프가 `atoms` 하나를 재사용해 **시드가 독립이 아니었다**
  · Nd 경고가 VASP 키워드 `ISPIN=2` 를 QE 에 권하고, Hubbard 를 &SYSTEM 안에 넣으라 했고,
    repo 어디에도 없는 PP 이름을 줬다 (실측: gabia 의 Nd PP 는 frozen-4f 라 U 를 걸 대상이 없다)
  · `pseudo_dir = './pseudo   # ← 교체'` — 주석이 Fortran 문자열 **안**이라 QE 가 경로
    전체를 리터럴로 읽었다. KISTI 갈래만 절대경로라 **세 서버 중 둘에서만 조용히** 깨졌다
  · 레시피 없는 조성 6개에 폴백을 씌워 db/structures 에 없는 cif 로 입력을 만들어 줬다

⚠ 시험마다 **음성 경로**를 같이 둔다 — "옛 형태로 되돌리면 실패" 가 이 파일의 목적이다.
⛔ 이 시험이 **못 하는 것**: 생성된 입력을 QE 로 실제로 돌려 보지 않는다. 문법·경로가
  서버에서 진짜 맞는지는 여전히 사람이 확인해야 한다 (화면도 그렇게 말한다).

    pytest webapp/tests/test_v3_compute.py -q
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A       # noqa: E402
import data as D      # noqa: E402


@pytest.fixture(scope="module")
def client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


# ── P0-23 · MD 산출물 ────────────────────────────────────────────────────────
def test_md_uses_canonical_driver_not_a_hand_written_script():
    """MD 갈래는 스크립트를 짓지 않고 **정본 드라이버**를 부른다."""
    r = D.compute_preview("b2o3", "md")
    blob = (r.get("runner") or "") + (r.get("input") or "")
    assert r.get("runner"), "MD 인데 붙여넣기 블록이 없다"
    assert "disorder_ensemble_diffusion.py" in blob, \
        "정본 드라이버를 안 부른다 — 화면이 두 번째 MD 구현을 갖게 된다"
    # ⛔음성: 죽은 API 가 돌아오면 실패 (붙여넣으면 첫 import 에서 죽는다)
    assert "OCPCalculator" not in blob, \
        "존재하지 않는 fairchem API 가 되살아났다 (정본은 pretrained_mlip + FAIRChemCalculator)"


def test_md_block_spells_out_every_convention():
    """창·궤적·시드를 **인자로 적는다.** 기본값은 기록이 아니다."""
    r = D.compute_preview("modelc", "md")
    run = r["runner"]
    assert "--save_traj" in run, \
        "궤적 저장이 없다 — 화면이 바로 위에서 금지한 바로 그것 (12런·21런 유실)"
    assert "--fit_window_ps 2 50" in run, "MSD 창 2–50 ps 를 명시하지 않는다"
    assert "--seed" in run, "시드를 명시하지 않는다"
    assert "--prod_ps 200" in run, "생산 200 ps 를 명시하지 않는다"
    # ⛔음성: 시드가 한 프로세스 안에서 돌면 독립이 아니다 → 호출을 나눠야 한다
    assert run.count("--seed") == 1 and 'for S in' in run, \
        "시드를 드라이버 호출 밖 루프로 나누지 않는다 (atoms 재사용 = 시드 비독립)"
    assert "pgrep" in run, "중복 실행 가드가 없다 (CLAUDE.md 공통 관례)"
    assert "nvidia-smi" in run, "pw.x·UMA 동시 실행 가드가 없다"


def test_md_note_keeps_absolute_sigma_prohibition():
    r = D.compute_preview("modelc", "md")
    txt = (r.get("note") or "") + " ".join(r.get("warn") or [])
    assert "절대값 인용 금지" in txt or "절대값" in txt, "σ 절대값 인용 금지가 사라졌다"


# ── P0-24 · Nd 처방 ──────────────────────────────────────────────────────────
def test_nd_prescription_is_qe_and_pp_conditional():
    r = D.compute_preview("modelc_nd_doped", "scf")
    blob = (r["input"] or "") + " ".join(r.get("warn") or [])
    # ⛔음성: VASP 키워드가 QE 화면에 다시 나오면 실패
    assert "ISPIN" not in blob, "ISPIN 은 VASP 키워드다 — QE 는 nspin"
    assert "nspin" in blob, "QE 쪽 키워드(nspin)를 안 알려준다"
    # QE 7.x 의 Hubbard 는 &SYSTEM 안이 아니라 독립 카드다
    assert "HUBBARD" in r["input"], "Hubbard 카드 안내가 없다"
    sysblk = r["input"].split("&SYSTEM", 1)[1].split("&ELECTRONS", 1)[0]
    assert "HUBBARD" not in sysblk and "Hubbard" not in sysblk, \
        "Hubbard 를 &SYSTEM 안에 넣으라고 한다 (QE 7.x 는 독립 카드)"
    # PP 조건부여야 한다 — frozen-4f 면 U 를 걸 대상이 없다
    assert "frozen-4f" in blob and "z_valence" in blob, \
        "PP 조건부가 아니다 — frozen-4f PP 에 U 를 권하면 QE 가 죽거나 조용히 무시한다"


def test_nd_pseudo_name_exists_in_the_repo_convention():
    """PP 이름은 생성기(tools/doping/generate_dft_inputs.py)와 같은 것이어야 한다."""
    gen = (ROOT / "tools" / "doping" / "generate_dft_inputs.py").read_text(errors="ignore")
    assert D.PSEUDO_LIB["Nd"] in gen, \
        f"Nd PP 이름 {D.PSEUDO_LIB['Nd']} 가 생성기 표에 없다 (화면 전용 이름 금지)"
    # ⛔음성: 옛 이름은 repo 어디에도 없었다
    assert D.PSEUDO_LIB["Nd"] != "Nd.GGA-PBE-paw.UPF", "존재하지 않는 옛 PP 이름이 돌아왔다"


# ── P0-25 · pseudo_dir 주석이 문자열 안 ──────────────────────────────────────
@pytest.mark.parametrize("cid", ["comp1", "comp2", "modelc", "modelc_v3",
                                 "lpsocl", "b2o3", "modelc_nd_doped"])
def test_no_comment_inside_any_quoted_namelist_value(cid):
    """⛔음성: 따옴표 **안**에 `#` 이 들어가면 QE 가 경로 전체를 리터럴로 읽는다."""
    inp = D.compute_preview(cid, "scf")["input"]
    assert inp, f"{cid} 입력이 없다"
    for ln in inp.splitlines():
        if "=" not in ln or "'" not in ln:
            continue
        val = ln.split("'", 2)
        if len(val) >= 2:
            assert "#" not in val[1], \
                f"{cid}: namelist 문자열 안에 주석이 있다 → {ln.strip()}"
    assert "pseudo_dir = './pseudo'" in inp or "pseudo_dir = '/" in inp, \
        f"{cid}: pseudo_dir 값이 닫힌 문자열이 아니다"


def test_pseudo_dir_guidance_survives_outside_the_string():
    """주석을 뺐다고 **안내까지** 사라지면 안 된다 — 밖(`!` 줄)에 남아야 한다."""
    inp = D.compute_preview("comp1", "scf")["input"]
    head = inp.split("&CONTROL", 1)[0]
    assert head.lstrip().startswith("!"), "상대경로인데 교체 안내가 없다"
    assert "pseudo" in head
    # ⛔음성: KISTI 는 절대경로라 그 안내가 붙으면 안 된다 (거짓 안내는 소음이다)
    k = D.compute_preview("lpsocl", "scf")["input"]
    assert k.startswith("&CONTROL"), "절대경로 서버에까지 교체 안내를 붙인다"


# ── 폴백 제거 (fail-closed) ─────────────────────────────────────────────────
@pytest.mark.parametrize("cid", ["comp3", "comp4", "comp5", "vgcf_hbn", "lic6"])
def test_unregistered_compositions_fail_closed(cid):
    """레시피가 없으면 **만들지 않는다.** 옛 폴백은 없는 cif 로 입력을 만들어 줬다."""
    if cid not in D.COMPOSITIONS:
        pytest.skip(f"{cid} 은 이 브랜치 COMPOSITIONS 에 없다")
    r = D.compute_preview(cid, "scf")
    assert r["input"] is None and r["runner"] is None, \
        f"{cid}: 레시피가 없는데 입력을 만들어 준다"
    assert "등록" in (r.get("note") or ""), f"{cid}: 왜 안 만드는지 화면에 안 적는다"


def test_registered_compositions_still_generate():
    """⛔음성: fail-closed 를 넓히다가 정상 조성까지 막으면 안 된다."""
    for cid in D.COMPUTE_SETTINGS:
        r = D.compute_preview(cid, "scf")
        assert r["input"], f"{cid}: 등록된 조성인데 입력이 안 나온다"


def test_existing_fail_closed_branches_kept_their_reasons():
    """sdcp→ORCA · li3n+md→금지 두 갈래는 **사유가 있는 거절**이라 유지된다."""
    s = D.compute_preview("sdcp", "scf")
    assert s["input"] is None and "ORCA" in (s.get("note") or ""), "SDCP ORCA 안내가 사라졌다"
    l = D.compute_preview("li3n", "md")
    assert l["input"] is None and "Li₃N" in (l.get("note") or ""), "Li₃N UMA 금지 안내가 사라졌다"
    assert "일반" not in (l.get("note") or ""), "구체적 사유가 일반 문구로 덮였다"


# ── 화면 ────────────────────────────────────────────────────────────────────
def test_compute_page_renders_runner_even_without_an_input_file(client):
    """⛔음성: 템플릿이 `d.input` 만 보면 MD 러너가 화면에서 통째로 사라진다."""
    body = client.get("/compute").get_data(as_text=True)
    assert body and "cmp-out" in body
    assert "if(d.runner)" in body, \
        "입력 없이 러너만 있는 갈래를 안 그린다 (MD 가 그 갈래다)"


def test_compute_page_still_teaches_the_rules(client):
    body = client.get("/compute").get_data(as_text=True)
    for k in ("--save_traj", "2–50 ps", "ldd", "OMP_NUM_THREADS"):
        assert k in body, f"규율 문구가 사라졌다: {k}"
