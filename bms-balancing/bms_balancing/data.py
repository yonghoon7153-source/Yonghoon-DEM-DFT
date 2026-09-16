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

#: 반쪽전지 모집단 선언의 **정본** — 코드가 아니라 자료에 대한 사실이라 파일에 둔다 (조건 8 축 ②, R16).
#: 코드 상수로 두면 모집단이 조용한 편집 한 줄로 바뀌고 그 변경의 근거가 어디에도 안 남는다.
HALF_CELL_MANIFEST = Path(__file__).resolve().parent.parent / "datasets" / "half_cell.manifest.json"


class ManifestError(RuntimeError):
    """dataset manifest 를 **읽지 못했거나 형식이 틀렸다.**

    전용 예외인 이유: 부르는 쪽이 `except Exception` 으로 삼키면 빈 allowlist 가 되고, 빈 allowlist 는
    "알려진 부재가 없다" 는 **주장**이다 — 못 읽은 것과 같은 값이면 안 된다 (자체 리뷰 C03 · R11 P1-9).
    """


def load_half_cell_manifest(path=None) -> dict:
    """모집단 선언을 읽고 **형식을 댄다** → 검증된 dict. 어긋나면 `ManifestError` 로 멈춘다.

    요구: `manifest_version`(1 이상 정수) · `dataset_id` · `declared_sources`/`declared_states` 목록 ·
    `absent` 목록. `absent` 항목마다 선언 안의 source/state 이고 **근거**(`why` + 비어 있지 않은
    `evidence`)와 기록자(`recorded_utc`·`recorded_by`)가 있어야 한다 — 근거 없이 모집단을 줄이지 않는다.
    """
    import json as _json
    p = Path(path) if path is not None else HALF_CELL_MANIFEST
    try:
        raw = p.read_bytes()
    except OSError as e:
        raise ManifestError(f"dataset manifest 를 못 읽었다 ({p}): {e} — 빈 allowlist 로 넘어가지 않는다") from None
    try:
        doc = _json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise ManifestError(f"dataset manifest 가 JSON 이 아니다 ({p}): {e}") from None
    if not isinstance(doc, dict):
        raise ManifestError(f"dataset manifest 가 객체가 아니다 ({p})")
    v = doc.get("manifest_version")
    if not (isinstance(v, int) and not isinstance(v, bool) and v >= 1):
        raise ManifestError(f"dataset manifest 에 manifest_version 이 없다/잘못됐다 ({v!r})")
    if not doc.get("dataset_id"):
        raise ManifestError("dataset manifest 에 dataset_id 가 없다 — 어느 데이터셋의 선언인지 말해야 한다")
    srcs, sts = doc.get("declared_sources"), doc.get("declared_states")
    if not (isinstance(srcs, list) and srcs and isinstance(sts, list) and sts):
        raise ManifestError("dataset manifest 에 declared_sources/declared_states 선언이 없다")
    absent = doc.get("absent")
    if not isinstance(absent, list):
        raise ManifestError("dataset manifest 에 absent 목록이 없다 — 빈 목록이면 `[]` 라고 **적어야** 한다")
    for e in absent:
        if not isinstance(e, dict) or e.get("source") not in srcs or e.get("state") not in sts:
            raise ManifestError(f"absent 항목이 선언 밖의 source/state 를 가리킨다: {e!r}")
        if not (e.get("why") and isinstance(e.get("evidence"), list) and e["evidence"]):
            raise ManifestError(f"absent 항목에 근거가 없다 ({e.get('source')}/{e.get('state')}) — "
                                f"근거 없이 모집단에서 빼지 않는다")
        if not (e.get("recorded_utc") and e.get("recorded_by")):
            raise ManifestError(f"absent 항목에 기록자/시각이 없다 ({e.get('source')}/{e.get('state')})")
    doc["_bytes"] = raw
    return doc


def half_cell_manifest_identity(path=None) -> dict:
    """산출에 적을 **모집단 선언의 식별자** — version · dataset_id · 그 파일 bytes 의 sha256.

    파일로 옮기기만 하고 산출이 그것을 안 적으면, 나중에 그 파일이 바뀌었을 때 어느 산출이 어느 선언으로
    만들어졌는지 말할 수 없다 (자체 리뷰 C18 의 "적고 안 대면 무엇을 고정하는지 말할 수 없다").
    """
    import hashlib as _h
    doc = load_half_cell_manifest(path)
    return {"version": doc["manifest_version"], "dataset_id": doc["dataset_id"],
            "sha256": _h.sha256(doc["_bytes"]).hexdigest()}


#: **알려진 의도적 부재** — 그 소스로는 그 상태를 애초에 재지 않았다 (Codex R10 P1-2). 정본은 위 manifest 다;
#: 여기 값은 그것을 읽은 **결과**이고, 읽기 실패는 import 시점에 `ManifestError` 로 멈춘다 (빈 집합이 아니다).
HALF_CELL_ABSENT = frozenset((e["source"], e["state"]) for e in load_half_cell_manifest()["absent"])

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
    return load_full_cell_from(src, state, identity=identity)


def load_full_cell_from(src, state: str, identity: dict | None = None):
    """**이미 읽은 bytes** 에서 그 상태의 (capacity, voltage) — 공통 snapshot 이 부르는 길 (조건 8 축 ①).

    경로를 다시 열지 않는다. 한 명령 안의 여러 행이 같은 workbook 을 각자 읽으면 그 사이의 재-export 가
    행을 갈라놓는데, 우리는 그것을 **적기만** 했다 (`shared_full_cell_mismatch_accepted: true`).
    """
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
