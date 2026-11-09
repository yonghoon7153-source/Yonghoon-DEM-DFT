# -*- coding: utf-8 -*-
"""사전 공격 15 탐침 공용 — 코드 사본 (PA15_TREE · 기본 = pa15/tree) 의 사슬 · 시험 모듈을 불러 시험 고정물 · rr4 도우미를 쓴다 (합성 · 실제 실행 없음)."""
import contextlib
import copy
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

PA15 = Path(__file__).resolve().parent.parent
TREE = Path(os.environ.get('PA15_TREE', str(PA15 / 'tree')))
sys.path.insert(0, str(TREE / 'scripts'))
import test_rint_r_chain as T   # noqa: E402
import rint_r_chain as RR       # noqa: E402

T.RR = RR
_OUT = PA15 / 'out' / 'td'
_OUT.mkdir(parents=True, exist_ok=True)
T.TD = tempfile.mkdtemp(prefix='pa15_', dir=str(_OUT))
with contextlib.redirect_stdout(io.StringIO()):
    T.fixtures()
MACH = T.MACH
N1, N2, N3 = T.RR4_N1, T.RR4_N2, T.RR4_N3


def tags(prob):
    return T.rr4_tag(prob)


def places(atts, machine=MACH):
    """[결과 줄 자격 (폴더 증거만으로 쓴 줄 = 원장 소비자 시험), 차례 [멈춤, 표지], 사슬 [멈춤, 표지]]."""
    return T.rr4_places(atts, machine=machine)


def cli(tag, atts, machine=MACH):
    """실제 git 원장 + recover CLI → [rc, 결과 줄 자격, 커밋 글 표지, 다시 셈 사유]."""
    return T.rr4_cli(tag, atts, machine=machine)


def writer(atts, machine=MACH):
    """공통 검증 결과 줄 쓰기 함수를 직접 (`attempt_result` · 원장 = 끝 시도 결과 줄 없음 · 같은 바탕) → (자격, 사유)."""
    st = RR.ledger_parse(''.join(RR.ledger_line(x) for x in T.rr4_lines(atts, machine=machine, last_result=False)).encode('utf-8'))
    n = len(atts)
    f, s = atts[-1]
    line, why = RR.attempt_result(n, f, s, 'recover', st)
    return line['resume_ok'], why


def three(name, mk, machine=MACH):
    """세 자리 (결과 줄 쓰기 = 직접 함수 + 실제 recover CLI · 차례 · 사슬) → dict.  mk(tag) = 새 시나리오."""
    out = {'name': name}
    try:
        out['writer'] = list(writer(mk(f'{name}_w'), machine=machine))
        out['writer'][1] = (tags(out['writer'][1]), (out['writer'][1] or '')[:200])
    except Exception as e:   # noqa: BLE001
        out['writer'] = f'exc {type(e).__name__}: {e}'[:300]
    try:
        out['places'] = places(mk(f'{name}_p'), machine=machine)
    except Exception as e:   # noqa: BLE001
        out['places'] = f'exc {type(e).__name__}: {e}'[:300]
    try:
        out['cli'] = cli(name, mk(f'{name}_c'), machine=machine)
    except Exception as e:   # noqa: BLE001
        out['cli'] = f'exc {type(e).__name__}: {e}'[:300]
    return out


def accepted(o):
    """세 자리 모두 통과 (결과 줄 True · 차례 None · 사슬 None · CLI 자격 True)?"""
    w, p, c = o.get('writer'), o.get('places'), o.get('cli')
    return (isinstance(w, list) and w[0] is True and isinstance(p, list) and p[1] is None and p[2] is None
            and isinstance(c, list) and c[1] is True)


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
