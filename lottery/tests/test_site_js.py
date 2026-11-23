"""웹앱 생성기(make.js)의 인기도 계산이 분석 코드(popularity.score_combos)와 같은 값을 내는가.

make.js 의 `// <core>` 구간만 잘라 node 로 돌린다. 화면에 뜨는 '인기 하위 n%'·'1등 시 기대 금액'이
분석과 다르면 생성기가 엉뚱한 조합을 고른다 — 그래서 두 구현을 직접 대조한다.
"""
import json
import re
import shutil
import subprocess

import numpy as np
import pytest

import dataset
import popularity

MAKE_JS = dataset.ROOT / "webapp" / "static" / "js" / "make.js"
S = json.loads((dataset.ROOT / "results" / "analysis.json").read_text(encoding="utf-8"))["lotto"]["popularity"]["score"]


@pytest.mark.skipif(shutil.which("node") is None, reason="node 없음")
def test_js_core_matches_python():
    core = re.search(r"// <core>\n(.*?)// </core>", MAKE_JS.read_text(encoding="utf-8"), re.S).group(1)
    rng = np.random.default_rng(9)
    combos = np.sort(np.argpartition(rng.random((300, 45)), 6, axis=1)[:, :6] + 1, axis=1).tolist()
    combos += [[1, 2, 3, 4, 5, 6], [7, 14, 21, 28, 35, 42], list(S["latest_numbers"])]
    prog = core + f"""
const S = {json.dumps(S)};
const C = {json.dumps(combos)};
console.log(JSON.stringify(C.map(c => {{ const p = popularity(c, S); const sh = comboShape(c);
  return [p.eta, p.share, p.pct, sh.arithmetic, sh.maxRun]; }})));
"""
    out = json.loads(subprocess.run(["node", "-e", prog], capture_output=True, text=True, check=True).stdout)
    eta, share = popularity.score_combos(np.array(combos), S)
    pct = np.interp(eta, S["eta_percentiles"], S["pct"])
    js = np.array([o[:3] for o in out])
    assert np.allclose(js[:, 0], eta, atol=1e-12) and np.allclose(js[:, 1], share, atol=1e-12)
    assert np.allclose(js[:, 2], pct, atol=1e-9)
    assert out[-3][3] is True and out[-3][4] == 6        # 1..6: 같은 간격, 6개 연속
    assert out[-2][3] is True and out[-2][4] == 1        # 7·14·…·42: 같은 간격
