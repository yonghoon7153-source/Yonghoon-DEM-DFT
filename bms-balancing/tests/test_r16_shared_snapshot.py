"""R16 — 조건 8 축 ①: export 공통 snapshot (2026-09-16).

리뷰어(R12 §5 답변 3)가 남긴 것: *"full-cell + 문헌 gr/si 는 **한 공통 immutable snapshot** …
**미구현.** 이번 라운드는 identity 를 **대는** 쪽(P1-1)만 넣었고 **주입하는** 쪽은 안 넣었다.
패키지의 `shared_full_cell_mismatch_accepted` 는 여전히 `true` 다."*

무엇이 열려 있었나: 한 명령 안에서 기준(pristine)과 대상이 **같은 workbook 을 각자 읽는다.** 그 사이에
파일이 재-export 되면 두 행이 **다른 bytes** 로 계산되는데, 우리는 그것을 나중에 **적기만** 했다
(`inputs_sha` 가 달라진다). 적는 것과 막는 것은 다르다.

리뷰어가 자리까지 제안했다 (R6_LEDGER "열어 둔 것"): **command/build 경계에서 한 번 읽은 typed
snapshot 을 양쪽에 전달.** 이 라운드가 그것을 넣는다.

  ① `shared_snapshot(root, si_source)` 가 공유 입력(full-cell workbook · 문헌 gr/si)을 **한 번** 읽는다
  ② 그 snapshot 을 받은 `build()` 는 **다시 읽지 않는다** — 같은 명령 안의 모든 행이 같은 bytes 를 본다
  ③ 그래서 실행 중 재-export 가 **행을 갈라놓지 못한다** (막는 쪽으로 옮긴다)

⚠ 이것이 **안 하는 것**: 다른 export 를 비교하는 일 자체를 금지하지 않는다. 그건 명시적 감도 모드의
일이고, 이 라운드는 "한 명령 안에서는 하나" 만 세운다.
"""
from __future__ import annotations

import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tests"))
from bms_balancing import verify as V          # noqa: E402
from test_r6_internal import _synth_root       # noqa: E402


def _bump(path: pathlib.Path):
    """워크북을 **다른 bytes** 로 다시 쓴다 (재-export 흉내) — **값은 그대로** 두고 메타데이터만 바꾼다.

    ⚠ 2026-09-16 실측: 처음에는 pandas 로 읽어 다시 썼는데 **같은 bytes** 가 나왔다 (openpyxl 이
      결정적으로 쓴다). 그러면 이 fixture 는 아무것도 안 바꾸고, 그것을 대조군이 잡아 줬다.
      지금은 문서 속성만 건드려 bytes 가 반드시 달라지게 한다.
    """
    import openpyxl
    wb = openpyxl.load_workbook(path)
    wb.properties.creator = (wb.properties.creator or "") + "-r16"
    wb.save(path)
    return path


def test_r16_71_the_snapshot_reads_the_shared_inputs_once(tmp_path):
    """[R16-71 · ①] 공유 입력을 한 번 읽어 typed snapshot 으로 들고 있는다."""
    src = _synth_root(tmp_path)
    snap = V.shared_snapshot(src, "Li")
    ident = snap.identity()
    assert set(ident) == {"full_cell", "literature"}, sorted(ident)
    assert len(ident["full_cell"]["sha256"]) == 64 and ident["full_cell"]["path"], ident
    assert set(ident["literature"]) == {"gr", "si"}, ident["literature"]
    assert snap.si_source == "Li", snap.si_source


def test_r16_72_two_builds_in_one_command_cannot_disagree(tmp_path):
    """[R16-72 · ③] **본론** — snapshot 을 공유한 두 build 는 실행 중 재-export 에도 갈라지지 않는다.

    이것이 `shared_full_cell_mismatch_accepted: true` 를 닫는 자리다: 전에는 기준과 대상이 각자 읽어서
    그 사이의 재-export 가 두 행을 다른 bytes 로 갈라놓았고 우리는 그것을 **적기만** 했다.
    """
    src = _synth_root(tmp_path)
    snap = V.shared_snapshot(src, "Li")
    a = V.build(src, "GITT", "pristine", "Li", shared=snap)
    _bump(src / "data/full_cell/large_cell_033C/fullcell_states.xlsx")     # 실행 중 재-export
    b = V.build(src, "GITT", "100", "Li", shared=snap)
    assert a.consumed_inputs["full_cell"] == b.consumed_inputs["full_cell"], (
        "한 명령 안에서 공유 입력이 갈렸다", a.consumed_inputs["full_cell"], b.consumed_inputs["full_cell"])
    assert a.consumed_inputs["literature"] == b.consumed_inputs["literature"], "문헌도 같아야 한다"


def test_r16_73_without_the_snapshot_the_hole_is_real(tmp_path):
    """[R16-73 · 양성 대조군] snapshot 없이 각자 읽으면 **실제로 갈린다.**

    이것이 없으면 R16-72 는 "재-export 흉내가 애초에 bytes 를 안 바꿨다" 와 구별되지 않는다.
    """
    src = _synth_root(tmp_path)
    a = V.build(src, "GITT", "pristine", "Li")
    _bump(src / "data/full_cell/large_cell_033C/fullcell_states.xlsx")
    b = V.build(src, "GITT", "100", "Li")
    assert a.consumed_inputs["full_cell"]["sha256"] != b.consumed_inputs["full_cell"]["sha256"], (
        "재-export 가 bytes 를 안 바꿨다 — 그러면 R16-72 는 공허하다")


def test_r16_74_the_commands_build_one_snapshot_and_pass_it_down():
    """[R16-74] 함수만 있고 **명령이 안 쓰면** 축이 안 닫힌다 — 경계에서 만들어 아래로 넘기는지 본다."""
    src = (ROOT / "bms_balancing" / "verify.py").read_text(encoding="utf-8")
    assert "shared_snapshot(" in src, "snapshot 을 만드는 자리가 없다"
    made = src.count("shared = shared_snapshot(")
    assert made >= 2, ("명령 경계에서 만들어야 한다 (matrix·degeneracy 등)", made)
    assert src.count("shared=shared") >= 2, "만들고 아래로 안 넘기면 소용없다"


def test_r16_75_a_snapshot_for_a_different_si_source_is_refused(tmp_path):
    """[R16-75] snapshot 은 자기가 읽은 **그 소스**의 것이다 — 다른 소스로 쓰면 거부한다.

    `Li` 로 읽은 문헌을 `Kunz` 실행에 넘기면 receipt 는 `Kunz` 라고 적히는데 bytes 는 `Li` 다.
    그것은 조용히 틀린 영수증이 되므로 **멈춘다** (부재·불일치는 안전값이 아니다).
    """
    src = _synth_root(tmp_path)
    snap = V.shared_snapshot(src, "Li")
    with pytest.raises(ValueError):
        V.build(src, "GITT", "pristine", "Kunz", shared=snap)
