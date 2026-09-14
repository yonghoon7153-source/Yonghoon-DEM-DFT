"""62차 δ′ (P0-6 · P0-7) — **producer scope 를 Python 의 규칙과 per-module 로.**

리뷰어 판정문의 셋째 문장: producer scope 모델이 아직 Python 과 다르다 —
class→method · definition head · crossed scoring module 셋 다 **digest 같고
계산은 1→9**.

  · P0-6 (a) class 본문의 결속이 **method 안까지** 적용된다. Python 에서 class
    본문의 이름은 method 에 안 보인다 — method 안의 `getattr` 은 builtin 이다.
  · P0-6 (b) 매개변수가 **definition head**(default · decorator · annotation)
    에 적용된다. Python 은 그것들을 정의 시점에 **바깥 scope** 에서 평가한다 —
    거기 `getattr` 은 매개변수가 아니라 builtin 이다.
  · P0-7 건너간 `src.scoring` 의 node 를 **primary 의 symbol table**(능력 별칭 ·
    이름 공간 대상 · import 이름 · 상수)로 분석한다. scoring 이 자기 module
    에서 `GET = getattr` 을 두면 primary 의 `caps` 에는 없어 안 잡힌다.

61차 P1-4 가 comprehension 에서 낸 것과 같은 형태 — scope 의 **목록**이 아니라
scope 의 **규칙**(무엇이 어디서 평가되는가)이 Python 보다 작았다.

`[고침]` `_scoped_shadows()` 가 definition head 를 바깥 집합으로, class 본문의
결속을 자식 scope 에 안 물려주고(comprehension 의 첫 iterable 만 class 본문을
본다), `_producer_closure()` 가 module 마다 자기 symbol table 을 만든다.
"""
from __future__ import annotations

import ast
import builtins
import sys
import textwrap
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
if str(REPO / "docs" / "22p_gap") not in sys.path:
    sys.path.insert(0, str(REPO / "docs" / "22p_gap"))


def _rp():
    import row_projection as rp

    return rp


def _shadow_map(node):
    return {id(n): sh for n, sh in _rp()._scoped_shadows(node)}


def _tables(src: str):
    """`_producer_closure()` 가 primary 에 대해 만드는 symbol table 그대로."""
    rp = _rp()
    tree = ast.parse(src)
    mods = rp._crossed_modules(src)
    return (mods, rp._source_reflection_locals(tree),
            rp._module_string_consts(tree), rp._namespace_capabilities(src),
            rp._namespace_targets(src, mods), rp._imported_module_names(src))


# ── P0-6 (a) class 본문 → method ──────────────────────────────────────────
_CLASS_LOCAL = textwrap.dedent('''
    import src.scoring as sc

    class C:
        for getattr in (None,):          # class 본문의 결속 — method 에는 안 보인다
            pass
        H = getattr                      # 여기서는 그 결속이 보인다

        def m(self):
            g = [getattr][0]             # Python: builtin — 능력이 값으로 흐른다
            return g(sc, "add_error_columns")
''')
# `[getattr][0]` 로 감싸는 이유: 벌거벗은 `g = getattr` 은 58차 L9-b 의 별칭
# 고정점(`_namespace_capabilities`)이 `g` 를 능력으로 따라가 **다른 층**에서
# 걸린다. 감싼 값은 그 층이 못 따라가므로 shadow 면제 하나만 남는다 — 그것이
# 리뷰어가 잰 "digest 같고 계산은 1→9" 의 형태다.


def test_python_really_hides_class_locals_from_methods():
    ns: dict = {}
    exec(compile(textwrap.dedent('''
        class C:
            for getattr in (None,):
                pass
            def m(self):
                return getattr
    '''), "<cls>", "exec"), ns)                              # noqa: S102
    assert ns["C"]().m() is builtins.getattr, (
        "class 본문의 이름이 method 에 보였다 — 이 시험의 전제가 틀렸다")


def test_the_analyzer_does_not_carry_class_locals_into_methods():
    """★ P0-6 (a) — method 안의 `getattr` load 는 class 본문의 `for getattr`
    로 가려지면 안 된다."""
    tree = ast.parse(_CLASS_LOCAL)
    cls = tree.body[1]
    m = cls.body[2]
    load = m.body[0].value.value.elts[0]                     # `[getattr][0]`
    got = _shadow_map(cls)[id(load)]
    assert "getattr" not in got, (
        f"class 본문의 결속이 method 의 load 를 가렸다: {sorted(got)} — "
        "Python 은 그렇게 동작하지 않는다 (62차 P0-6)")


def test_class_locals_still_shadow_inside_the_class_body():
    """반대 방향 — class 본문 **안에서는** 가린다 (거부가 넓어지면 안 된다)."""
    tree = ast.parse(_CLASS_LOCAL)
    cls = tree.body[1]
    h = cls.body[1].value                                    # `H = getattr`
    assert "getattr" in _shadow_map(cls)[id(h)]


def test_a_class_local_does_not_exempt_a_capability_in_a_method():
    """★ P0-6 (a) 끝까지 — guard 가 method 의 `g = getattr` 를 거부해야 한다."""
    rp = _rp()
    cls = ast.parse(_CLASS_LOCAL).body[1]
    with pytest.raises(SystemExit, match="능력을 값으로"):
        rp._assert_no_dynamic_resolution(cls, "C", *_tables(_CLASS_LOCAL))


# ── P0-6 (b) definition head ─────────────────────────────────────────────
_HEAD_DEFAULT = textwrap.dedent('''
    import src.scoring as sc

    def f(getattr, k=[getattr][0](sc, "add_error_columns")):
        h = getattr                      # 본문에서는 매개변수다
        return k                         # default 는 정의 시점에 module 을 열었다
''')

_HEAD_DECORATOR = textwrap.dedent('''
    import src.scoring as sc

    def keep(cap):
        def deco(fn):
            return fn
        return deco

    @keep([getattr][0](sc, "add_error_columns"))   # decorator 인자도 바깥 scope 다
    def f(getattr):
        return None
''')
# head 안에서 **직접** 이름 공간을 연다 — 매개변수 `g` 로 받아 본문에서 부르면
# 60차 P0-10("호출자가 준 이름을 부른다")이 먼저 걸린다. 리뷰어의 형태는
# 정의 시점 평가 그 자체다.

_HEAD_ANNOTATION = textwrap.dedent('''
    import src.scoring as sc

    def f(getattr, x: [getattr][0] = None):
        return None
''')


def test_python_really_evaluates_defaults_in_the_enclosing_scope():
    ns: dict = {}
    exec(compile("def f(getattr, g=getattr):\n    return g\n",
                 "<head>", "exec"), ns)                       # noqa: S102
    assert ns["f"](None) is builtins.getattr, (
        "default 가 매개변수를 봤다 — 이 시험의 전제가 틀렸다")


def test_the_analyzer_does_not_shadow_the_default_with_the_parameter():
    """★ P0-6 (b) — default 안의 `getattr` load 는 매개변수 `getattr` 로 가려지면
    안 된다. 본문의 load 는 그대로 가려진다."""
    fn = ast.parse(_HEAD_DEFAULT).body[1]
    default_load = fn.args.defaults[0].func.value.elts[0]    # `[getattr][0](…)`
    body_load = fn.body[0].value                             # `h = getattr`
    sm = _shadow_map(fn)
    assert "getattr" not in sm[id(default_load)], (
        f"매개변수가 definition head 를 가렸다: {sorted(sm[id(default_load)])} "
        "(62차 P0-6)")
    assert "getattr" in sm[id(body_load)], "본문의 매개변수 shadow 가 사라졌다"


def test_the_analyzer_does_not_shadow_the_decorator_with_the_parameter():
    fn = ast.parse(_HEAD_DECORATOR).body[2]
    deco_load = fn.decorator_list[0].args[0].func.value.elts[0]
    assert "getattr" not in _shadow_map(fn)[id(deco_load)], (
        "매개변수가 decorator 인자를 가렸다 (62차 P0-6)")


def test_the_analyzer_does_not_shadow_the_annotation_with_the_parameter():
    fn = ast.parse(_HEAD_ANNOTATION).body[1]
    ann_load = fn.args.args[1].annotation.value.elts[0]
    assert "getattr" not in _shadow_map(fn)[id(ann_load)], (
        "매개변수가 annotation 을 가렸다 (62차 P0-6)")


def test_a_lambda_default_is_evaluated_outside_the_lambda():
    tree = ast.parse("k = lambda getattr, g=[getattr][0]: g\n")
    lam = tree.body[0].value
    default_load = lam.args.defaults[0].value.elts[0]
    assert "getattr" not in _shadow_map(lam)[id(default_load)], (
        "lambda 의 매개변수가 자기 default 를 가렸다 (62차 P0-6)")


@pytest.mark.parametrize("src,idx", [(_HEAD_DEFAULT, 1), (_HEAD_DECORATOR, 2)])
def test_a_parameter_does_not_exempt_a_capability_in_the_head(src, idx):
    """★ P0-6 (b) 끝까지 — guard 가 head 의 능력 값 흐름을 거부해야 한다."""
    rp = _rp()
    fn = ast.parse(src).body[idx]
    with pytest.raises(SystemExit, match="능력을 값으로"):
        rp._assert_no_dynamic_resolution(fn, "f", *_tables(src))


def test_a_comprehension_in_a_class_body_sees_only_its_first_iterable():
    """class 본문의 comprehension — Python 은 **첫 iterable 만** class 본문에서
    평가하고 나머지는 class 이름을 못 본다. 규칙을 통째로 옮기면 여기가
    반대로 틀린다 (61차 P1-4 와 같은 경계)."""
    src = textwrap.dedent('''
        class C:
            for getattr in (None,):
                pass
            xs = [getattr for _ in [getattr]]
    ''')
    cls = ast.parse(src).body[0]
    comp = cls.body[1].value
    first_iter = comp.generators[0].iter.elts[0]             # class 본문에서 평가
    elt = comp.elt                                           # 자식 scope
    sm = _shadow_map(cls)
    assert "getattr" in sm[id(first_iter)]
    assert "getattr" not in sm[id(elt)]


# ── P0-7 crossed module 의 symbol table ──────────────────────────────────
def _real_sources():
    src = (REPO / "docs" / "22p_gap" / "row_projection.py").read_text(
        encoding="utf-8")
    sc = (REPO / "src" / "scoring.py").read_text(encoding="utf-8")
    return src, sc


def test_a_capability_alias_inside_the_scoring_module_is_refused():
    """★ P0-7 — scoring 이 **자기 module** 에서 `GET = getattr` 을 두고 그것을
    값으로 흘리면, primary 의 `caps` 에는 `GET` 이 없어 통과했다. 건너간
    module 은 자기 symbol table 로 분석돼야 한다."""
    rp = _rp()
    src, sc = _real_sources()
    assert "src.scoring:add_error_columns" in rp._producer_closure(src, sc), (
        "fixture 전제가 깨졌다 — add_error_columns 가 닫힘에 없다")
    anchor = "    out = df.copy()\n    for k in MODES:"
    assert sc.count(anchor) == 1, "fixture 전제가 깨졌다 — anchor 가 하나가 아니다"
    sc2 = sc.replace("def add_error_columns(",
                     "GET = getattr\n\n\ndef add_error_columns(", 1)
    sc2 = sc2.replace(anchor, "    out = df.copy()\n    g = GET\n    for k in MODES:", 1)
    with pytest.raises(SystemExit, match="능력을 값으로"):
        rp._producer_closure(src, sc2)


def test_a_namespace_alias_inside_the_scoring_module_is_refused():
    """★ P0-7 — 대상 쪽도 같다: scoring 이 `M = sys.modules[__name__]` 이 아니라
    `import src.scoring as me` 같은 자기 이름 공간 별칭을 두고 `getattr(me, k)`
    로 열면 primary 의 `targets` 에는 `me` 가 없어 "이름 공간이 아님이 증명됐다"
    가 됐다."""
    rp = _rp()
    src, sc = _real_sources()
    anchor = "    out = df.copy()\n    for k in MODES:"
    sc2 = sc.replace("def add_error_columns(",
                     "import src.scoring as me\n\n\ndef add_error_columns(", 1)
    sc2 = sc2.replace(anchor, "    out = df.copy()\n    _ = getattr(me, tol)\n"
                              "    for k in MODES:", 1)
    with pytest.raises(SystemExit, match="이름 공간|계산해서"):
        rp._producer_closure(src, sc2)


def test_the_unmodified_scoring_module_still_passes_its_own_table():
    """양성 대조 — 실제 scoring.py 는 자기 symbol table 로도 통과해야 한다."""
    rp = _rp()
    src, sc = _real_sources()
    rp._producer_closure(src, sc)
