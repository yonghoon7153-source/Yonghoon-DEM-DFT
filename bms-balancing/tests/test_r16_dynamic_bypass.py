"""R16 — 조건 6(동적 인증): `test_g10` 을 **AST 검사에서 실제 우회 재현으로** 올린다 (2026-09-16).

리뷰어가 R14 §에서 정확히 이렇게 적었다: *"열림. `test_g10` 은 AST 순서 검사이지 **우회 재현이 아니다**."*

무엇을 막는 장치인가 (자체 리뷰 C08 의 남은 절반): 증거 러너 넷은 `sys.path[0]` 이 **저장소 안**(스크립트가
든 디렉터리)이라, 거기 놓인 untracked `traceback.py` 하나가 `import argparse, …, traceback` 줄에서
**봉인(gate) 보다 먼저** 실행될 수 있었다. 그 모듈은 `INSTRUMENT` 밖이라 도구 자신의 봉인에도 안 걸린다.
막는 방법은 **앱 의존성 import 보다 앞에서** `-P -E -B` 로 재실행하는 것이다 (`-P` 가 스크립트 디렉터리를
`sys.path` 에 안 넣는다).

`test_g10` 은 그 재실행 블록이 import 보다 **앞에 있는지** AST 로만 봤다. 그것은 "순서가 맞다" 이지
"우회가 막힌다" 가 아니다 — 재실행이 실패하거나(execv 오류) 플래그가 안 먹거나 파이썬이 `-P` 의 의미를
바꾸면 AST 는 그대로인데 구멍은 열린다.

그래서 **실제로 심어서 돌린다**:

  A (양성 대조군)  재실행 블록을 **지운** 사본 → 심어 둔 모듈이 **실행된다** (표식 파일이 생긴다)
  B (본 시험)      손대지 않은 사본        → 심어 둔 모듈이 **실행되지 않는다**

A 가 없으면 B 는 공허하다 — 심은 것이 애초에 안 도는 것과 구별이 안 된다. 이 저장소가 fixture 감사에서
반복해 본 모양이라(“시험이 처음부터 통과하면 fixture 가 진실을 가린 것”) 양성 대조군을 같이 둔다.

저장소를 더럽히지 않는다: 러너와 `evidence_gate.py` 를 tmp 로 **복사**해 그 사본의 디렉터리에 심는다.
그래서 `sys.path[0]` 은 tmp 이고 저장소 트리에는 아무것도 안 생긴다.
"""
from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]

#: `test_g10` 이 보는 것과 **같은 넷**이어야 한다 — 한쪽만 늘면 동적 인증에 구멍이 남는다 (아래 R16-13 이 댄다).
RUNNERS = ("r7_repros/replay_codex_r7.py", "r9_repros/replay_codex_r9.py",
           "r10_repros/replay_codex_r10.py", "r11_repros/replay_codex_r11.py")

#: 심는 모듈 — stdlib `traceback` 을 가리는 이름이다 (러너 넷이 전부 import 한다).
#: 표식을 남기고 나서 최소 API 를 흉내 내, 우회가 **성공했을 때** 러너가 계속 굴러가게 둔다.
PLANT = '''# 심어 둔 가짜 stdlib 모듈 — 우회가 성공하면 이 줄이 실행된다.
import os, pathlib
pathlib.Path(os.environ["R16_MARKER"]).write_text("hijacked", encoding="utf-8")


def format_exc(*a, **k):
    return ""


def print_exc(*a, **k):
    return None
'''

#: 재실행 블록을 지우는 자리 — 러너 넷이 같은 모양으로 적어 두었다.
_REEXEC = re.compile(r'^if globals\(\)\.get\("__name__"\) == "__main__" and not sys\.flags\.safe_path:',
                     re.MULTILINE)


def _stage(tmp: pathlib.Path, rel: str, *, disarm: bool) -> tuple[pathlib.Path, pathlib.Path]:
    """러너 사본 + `evidence_gate.py` 를 tmp 에 놓고 그 디렉터리에 가짜 모듈을 심는다 → (스크립트, 표식 경로).

    `disarm=True` 면 재실행 블록을 **들여쓰기째** 지운다 — 우회가 실제로 가능한지 보는 양성 대조군이다.
    """
    pkg, name = rel.split("/")
    base = tmp / ("disarmed" if disarm else "armed")
    (base / pkg).mkdir(parents=True)
    shutil.copy(ROOT / "reviews" / "evidence_gate.py", base / "evidence_gate.py")
    src = (ROOT / "reviews" / rel).read_text(encoding="utf-8")

    if disarm:
        m = _REEXEC.search(src)
        assert m, f"{rel}: 재실행 블록을 못 찾았다 — 러너가 바뀌었으면 이 시험을 같이 고친다"
        lines = src.splitlines(keepends=True)
        i = src[:m.start()].count("\n")
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or lines[j][:1] in (" ", "\t")):
            j += 1                                  # 블록 본문(들여쓴 줄과 빈 줄)을 전부 먹는다
        assert any(re.match(r"\s*os\.execv\(", x) for x in lines[i:j]), (rel, "지운 구간에 execv 호출이 없다")
        src = "".join(lines[:i] + lines[j:])
        # 주석에도 `execv` 라는 낱말이 나오므로 **호출문**만 본다
        assert not re.search(r"^\s*os\.execv\(", src, re.MULTILINE), \
            f"{rel}: execv 호출이 남았다 — 대조군이 무장 해제되지 않았다"

    script = base / pkg / name
    script.write_text(src, encoding="utf-8")
    (base / pkg / "traceback.py").write_text(PLANT, encoding="utf-8")
    return script, base / "marker.txt"


def _run(script: pathlib.Path, marker: pathlib.Path):
    """러너 사본을 돌린다 → (표식이 생겼나, 합쳐진 출력). 러너의 **성공** 여부는 이 시험의 주제가 아니다.

    ⚠ 출력을 같이 돌려주는 이유: "표식이 없다" 만으로는 **막힌 것**과 **import 에 닿기도 전에 죽은 것**을
      구별할 수 없다. 러너는 `--expected-head` 를 필수로 요구하므로, argparse 의 usage 가 보이면 그
      프로세스는 `import argparse, …, traceback` 줄을 **이미 지난** 것이다 (같은 한 줄이다).
    """
    import os
    env = dict(os.environ, R16_MARKER=str(marker))
    env.pop("PYTHONPATH", None)
    r = subprocess.run([sys.executable, str(script), "--target", str(ROOT)],
                       cwd=ROOT, capture_output=True, text=True, timeout=300, env=env)
    return marker.exists(), (r.stdout or "") + (r.stderr or "")


@pytest.mark.parametrize("rel", RUNNERS)
def test_r16_11_the_plant_actually_fires_when_the_reexec_is_removed(tmp_path, rel):
    """[R16-11 · 양성 대조군] 재실행 블록을 지우면 심어 둔 모듈이 **실제로 실행된다.**

    이것이 없으면 아래 R16-12 는 "심은 것이 애초에 안 돌았다" 와 구별되지 않는다.
    """
    script, marker = _stage(tmp_path, rel, disarm=True)
    fired, _out = _run(script, marker)
    assert fired is True, (
        f"{rel}: 재실행을 지웠는데도 심은 모듈이 안 돌았다 — 이 반례가 더 이상 반례가 아니거나 "
        f"시험이 다른 것을 재고 있다 (그러면 R16-12 는 공허하다)")


@pytest.mark.parametrize("rel", RUNNERS)
def test_r16_12_the_reexec_actually_blocks_the_hijack(tmp_path, rel):
    """[R16-12 · 본 시험] 손대지 않은 러너에서는 같은 심기가 **실행되지 않는다.**

    `test_g10` 은 재실행 블록이 import 보다 앞에 있는지 AST 로만 봤다 — 순서가 맞다는 것이지 우회가
    막힌다는 것이 아니다. 여기서는 같은 조건으로 실제 프로세스를 띄워 관측한다.
    """
    script, marker = _stage(tmp_path, rel, disarm=False)
    fired, out = _run(script, marker)
    # ① 먼저 **import 줄을 지났다**는 것을 확인한다 — 안 그러면 "표식 없음" 이 공허하다
    assert "--expected-head" in out, (
        f"{rel}: 프로세스가 인자 파싱까지 못 갔다 — import 앞에서 죽었으면 이 시험은 아무것도 안 잰다", out[-800:])
    # ② 그 상태에서 심은 것이 안 돌았다
    assert fired is False, (
        f"{rel}: 봉인 앞에서 심어 둔 모듈이 실행됐다 — `sys.path[0]` 우회가 열려 있다 (자체 리뷰 C08)")


def test_r16_13_the_dynamic_check_covers_the_same_runners_as_the_ast_check():
    """[R16-13] 동적 인증과 AST 검사가 **같은 넷**을 봐야 한다 — 한쪽만 늘면 새 러너가 조용히 안 걸린다.

    `test_g10` 의 목록을 정본으로 읽어 댄다 (개수를 여기 박지 않는다 — R16-4 와 같은 규율).
    """
    src = (ROOT / "tests" / "test_r13_codex.py").read_text(encoding="utf-8")
    m = re.search(r"^RUNNERS = \((.*?)\)$", src, re.MULTILINE | re.DOTALL)
    assert m, "test_g10 의 RUNNERS 목록을 못 찾았다"
    ast_runners = set(re.findall(r'"([^"]+\.py)"', m.group(1)))
    assert ast_runners == set(RUNNERS), ("두 검사의 대상이 갈렸다", sorted(ast_runners), sorted(RUNNERS))


# ── R16-21 ───────────────────────────────────────────────────────────────
def test_r16_21_every_named_substitute_regression_actually_exists():
    """[R16-21] 러너의 `SUBSTITUTES` 가 이름 댄 회귀가 **실재해야** 한다 — 이름만 적으면 그것은 증거가 아니다.

    `closed_with_substitutes` 는 "제외된 leaf 마다 대체 증거의 **이름**이 있다" 로 계산된다. 이름이 사라진
    시험을 가리키면 그 필드는 조용히 거짓이 된다 (R11 P1-9 "신고된 위험은 값으로 소비한다" 의 같은 결).

    2026-09-16: `publish:profile_partial_stdout` 의 대체로 `test_e11_13` 을 등록하면서 같이 넣었다 —
    등록이 **닫힘의 근거**가 되는 순간, 그 등록 자신을 대는 것이 있어야 한다.
    """
    import re as _re
    src = (ROOT / "reviews/r11_repros/replay_codex_r11.py").read_text(encoding="utf-8")
    m = _re.search(r"^SUBSTITUTES = \{(.*?)^\}", src, _re.MULTILINE | _re.DOTALL)
    assert m, "SUBSTITUTES 표를 못 찾았다"
    named = set(_re.findall(r"\b(test_[A-Za-z0-9_]+)", m.group(1)))
    assert named, ("대체 증거에 회귀 이름이 하나도 없다 — 표가 바뀌었으면 이 시험도 같이 본다", m.group(1)[:300])
    have = "\n".join(p.read_text(encoding="utf-8") for p in sorted((ROOT / "tests").glob("test_*.py")))
    # 이름은 **접두**다 — 실제 함수는 `test_e11_13_profile_partial_returns_three_even_without_a_sink` 처럼
    # 뒤에 설명이 붙는다. `\b` 를 붙이면 뒤가 `_` 라 경계가 안 생겨 전부 "없다" 가 된다 (실측).
    missing = sorted(n for n in named if not _re.search(rf"^def {n}", have, _re.MULTILINE))
    assert not missing, ("대체 증거로 이름 댄 회귀가 없다", missing)
