"""데이터 로더 — BMS 쪽 원자료는 **저장소에 넣지 않는다.**

원자료(반쪽전지·풀셀 xlsx, 문헌 OCP)는 규진팀 것이고 공개 저장소에 올릴지는
우리가 정할 일이 아니다. 그래서 이 하네스는 경로를 밖에서 받는다:

    export BMS_DATA_ROOT=/…/electrode_balancing_blend
    python -m bms_balancing.verify …

`--data-root` 인자가 있으면 그것이 이긴다. 산출은 요약 표(CSV/MD)만 남긴다.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd

STATES = ["pristine", "100", "200", "300_0009", "300_0147"]

#: 풀셀 워크북(`현차_풀셀_정리.xlsx`)의 상태별 컬럼쌍 (0-based, main_blend_final.m 의 1-based 와 대응)
FULL_COL = {"pristine": 0, "100": 1, "200": 2, "300_0009": 3, "300_0147": 4}

#: 반쪽전지 파일 이름 — 소스마다 다르다
HALF_FILE = {
    "GITT": {s: f"{s}.xlsx" for s in STATES},
    "step_005C": {s: f"{s}_005C.xlsx" for s in STATES},
}

#: **알려진 의도적 부재** — 그 소스로는 그 상태를 애초에 재지 않았다 (Codex R10 P1-2: "알려진 부재는 source 별
#: 명시적 allowlist 로 표현한다"). 이 목록에 있으면 모집단에서 **빠지는 것이 맞고**, 없는데 파일이 없으면 그것은
#: `missing_input` 이다 — 둘을 코드가 구분하지 못하면 축소된 roster 가 complete 를 참칭한다.
#: 근거(실측, 사용자 기계 U14 산출): `out/matrix_300_0147.csv` 는 step_005C 16 행뿐이고 GITT 행이 없다 ·
#: `out/degeneracy_300_0147_Li.json` 의 half_cell 은 step_005C · 나머지 세 상태의 matrix 는 두 소스 32 행이다 ·
#: `run_states.sh` 의 `pick_src` 주석("300_0147 이 GITT 에만 없어서 degeneracy 가 죽었다", 2026-09-10 실측).
HALF_CELL_ABSENT = frozenset({("GITT", "300_0147")})

SI_SOURCES = ["Baggetto", "Friedrich", "Jiang", "Kunz", "Li", "Lu",
              "Sethuraman", "Wetjen"]


def data_root(explicit: str | None = None) -> Path:
    root = explicit or os.environ.get("BMS_DATA_ROOT")
    if not root:
        raise SystemExit(
            "BMS 원자료 경로를 모른다. --data-root 또는 BMS_DATA_ROOT 로 "
            "electrode_balancing_blend 디렉터리를 가리켜라.")
    p = Path(root)
    if not (p / "data" / "literature").is_dir():
        raise SystemExit(f"{p} 아래에 data/literature 가 없다 — 경로가 맞나?")
    return p


def half_cell_path(root: Path, source: str, state: str) -> Path:
    return root / "data" / "half_cell" / source / HALF_FILE[source][state]


def declared_states(source: str, include_pristine: bool = False) -> list:
    """그 소스의 **정본 roster** — 선언된 상태에서 알려진 부재(`HALF_CELL_ABSENT`)를 뺀 것 (Codex R10 P1-2).

    파일 존재는 보지 않는다. 존재 확인으로 모집단을 줄이면 없는 것이 애초에 요청되지 않은 것처럼 보인다 (R9-04).
    """
    return [s for s in STATES
            if (include_pristine or s != "pristine")
            and s in HALF_FILE.get(source, {}) and (source, s) not in HALF_CELL_ABSENT]


def full_cell_workbook(root: Path) -> Path:
    d = root / "data" / "full_cell" / "large_cell_033C"
    # `sorted` 는 장식이 아니다: MATLAB 쪽(`dd_eval.m`·`dd_verify.m`)은 `dir()`
    # 이 주는 **이름순** 목록의 첫 항목을 쓴다. `Path.glob` 은 순서를 보장하지
    # 않으므로(파일시스템 순서), 후보가 둘 이상이면 두 구현이 **다른 파일**을
    # 골라 놓고 그걸 "포팅 불일치" 로 오해하게 된다.
    cands = sorted((p for p in d.glob("*.xlsx")
                    if "pristine" not in p.name and "300cycle" not in p.name),
                   key=lambda p: p.name)
    if not cands:
        raise SystemExit(f"{d} 에서 상태별 풀셀 워크북을 못 찾았다")
    if len(cands) > 1:
        print(f"[data] 풀셀 워크북 후보가 {len(cands)}개다 — 이름순 첫 것을 쓴다: "
              f"{cands[0].name} (나머지: {', '.join(p.name for p in cands[1:])})",
              file=sys.stderr)
    return cands[0]


class InputBytes:
    """입력 파일의 **한 번 읽은 bytes** 와 그 bytes 의 sha256 (Codex R6-03). 파싱도 해시도 이 bytes 로 한다 —
    경로를 다시 열면 그 사이 재-export 된 다른 파일을 해시하게 된다 (A 로 계산하고 B 의 서명을 적는다)."""
    __slots__ = ("path", "data", "sha256")
    def __init__(self, path, data: bytes):
        import hashlib
        self.path, self.data, self.sha256 = str(path), data, hashlib.sha256(data).hexdigest()
    def stream(self):
        import io
        return io.BytesIO(self.data)
    def identity(self) -> dict:
        return {"path": self.path, "sha256": self.sha256}


def read_input(path) -> InputBytes:
    return InputBytes(path, Path(path).read_bytes())


def load_full_cell(root: Path, state: str, workbook: Path | None = None, identity: dict | None = None):
    """2행 헤더(1행=상태명, 2행=단위) 워크북에서 그 상태의 (capacity, voltage).
    `workbook` 을 주면 그 파일을 읽는다 (R6 내부 F4). `identity` dict 를 주면 **실제로 파싱한 bytes** 의 경로·sha256 을
    채운다 (Codex R6-03)."""
    src = read_input(workbook or full_cell_workbook(root))
    if identity is not None:
        identity.update(src.identity())
    df = pd.read_excel(src.stream(), header=None, skiprows=2)
    col = FULL_COL[state]
    c = pd.to_numeric(df[2 * col], errors="coerce")
    v = pd.to_numeric(df[2 * col + 1], errors="coerce")
    ok = c.notna() & v.notna()
    return c[ok].to_numpy(float), v[ok].to_numpy(float)


#: 정본 로스터 밖의 문헌 한 파일을 받을 때 쓰는 소스 라벨 — `SI_SOURCES` 에 넣지 않는다
#: (거기 넣으면 `canonical_combo_keys` 의 32 조합이 바뀌어 정본 산출 전체가 흔들린다).
EXTERNAL_SI_SOURCE = "external"


def load_literature_file(path, identity: dict | None = None):
    """**한 파일**에 든 Si·Gr 문헌 곡선 → `load_literature` 와 같은 4 튜플.

    pyDMA 예제(`pydma_example_Si_Gr_literature.xlsx`)의 레이아웃이다: 한 시트에
    `Si_capacity`·`Si_voltage`·`Gr_capacity`·`Gr_voltage` 가 있고 **열마다 길이가 달라** NaN 꼬리가 다르다
    (MATLAB `run_validation.m` 도 열마다 `~isnan` 으로 따로 자른다). 여기서도 열별로 자른다 — 행 단위
    `dropna` 는 가장 짧은 열에 맞춰 다른 곡선을 잘라낸다.

    `identity` 를 주면 `{"gr": …, "si": …}` 를 **같은 파일**로 채운다. 한 파일이 두 곡선을 다 주므로
    두 역할의 sha256 이 같은 것이 사실이고, receipt 역할 넷(`REQUIRED_ROLES`)은 그대로 지켜진다.
    """
    src = read_input(Path(path))
    df = pd.read_excel(src.stream())
    need = ("Si_capacity", "Si_voltage", "Gr_capacity", "Gr_voltage")
    missing = [c for c in need if c not in df.columns]
    if missing:
        raise SystemExit(f"{path}: 문헌 열이 없다 {missing} — 필요한 열 {list(need)}")
    if identity is not None:
        ident = src.identity()
        identity.update({"gr": dict(ident), "si": dict(ident)})
    col = lambda c: df[c].dropna().to_numpy(float)
    return col("Si_capacity"), col("Si_voltage"), col("Gr_capacity"), col("Gr_voltage")


def load_literature(root: Path, si_source: str = "Li", identity: dict | None = None):
    """Gr 은 항상 Si_Gr_literature_OCP.xlsx, Si 만 선택 소스로 교체. `identity` 를 주면 파싱한 bytes 의 경로·sha256 을
    `{"gr": …, "si": …}` 로 채운다 (Codex R6-03)."""
    lit = root / "data" / "literature"
    gr_in = read_input(lit / "Si_Gr_literature_OCP.xlsx")
    si_in = read_input(lit / "Si_OCP_sources" / f"{si_source}.csv")
    if identity is not None:
        identity.update({"gr": gr_in.identity(), "si": si_in.identity()})
    gr = pd.read_excel(gr_in.stream())
    gr_c = gr["Gr_capacity"].dropna().to_numpy(float)
    gr_v = gr["Gr_voltage"].dropna().to_numpy(float)
    si = pd.read_csv(si_in.stream())
    return (si["normalizedCapacity"].to_numpy(float),
            si["voltage"].to_numpy(float), gr_c, gr_v)
