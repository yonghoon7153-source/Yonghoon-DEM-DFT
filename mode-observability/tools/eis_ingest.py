#!/usr/bin/env python3
"""Su 2024 SI 의 EIS 데이터셋을 재현 가능하게 등록하고 읽는다.

왜 이렇게 나누나
----------------
원본 176파일 90 MB 는 **커밋하지 않는다** (`mode-observability/data/` 는
`.gitignore`). 3자 데이터의 재배포 권리가 불명확하고, 저장소가 부푼다.
대신 두 가지를 커밋한다:

  · `manifests/su2024_eis.tsv` — 파일별 sha256·크기·행수·스펙트럼 수와
    파일명에서 푼 좌표(state·온도·셀). 이것이 "우리가 무엇을 봤는가" 의 정본.
  · 우리가 실제로 쓰는 **파생 소표** (별도 스크립트).

manifest 가 있으면 다른 사람이 같은 zip 을 받아 `--verify` 로 **바이트가 같은
것을 봤는지** 확인할 수 있다. 원본을 나르지 않고 재현성을 지키는 방법이다.

파일 형식 (실측, BioLogic EC-Lab export)
----------------------------------------
    time/s  cycle number  freq/Hz  Re(Z)/Ohm  -Im(Z)/Ohm  |Z|/Ohm  Phase(Z)/deg

**헤더가 있는 파일과 없는 파일이 섞여 있다** (실측: `EIS_state_III_35C01.txt`
는 첫 줄부터 수치다). 그래서 열 순서를 헤더에만 기대지 않고 **물리 항등식**
(`|Z| = hypot(Re, Im)` · `Phase = atan2(Im, Re)`)으로 확인한다 — 헤더는
거짓말할 수 있지만 항등식은 못 한다. 한 파일에 **여러 스펙트럼**이 들어 있고
`cycle number` 로 갈린다 (실측: 4,920행 · 82 스펙트럼 · 0.02 Hz~20 kHz).

파일명: `EIS_state_<로마숫자>_<온도>C<셀번호>.txt`
  · state I~IX — 충방전 사이클 안의 측정 지점 (SOC 축이 아니다; 원문 확인 필요)
  · 온도 25/35/45 °C · 셀 01~08

쓰기
----
    python3 tools/eis_ingest.py --scan          # manifest 생성/갱신
    python3 tools/eis_ingest.py --verify        # 지금 파일이 manifest 와 같은가
    python3 tools/eis_ingest.py --show <파일명> # 한 파일 요약 (스펙트럼·주파수 범위)
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DATA = HERE / "data" / "su2024" / "EIS data"
MANIFEST = HERE / "manifests" / "su2024_eis.tsv"

#: 실측한 열 이름. 이 순서·철자가 아니면 **파일을 읽지 않는다** — 형식이 바뀐
#: 것을 조용히 다른 열로 읽으면 그때부터 모든 수치가 거짓이다.
COLUMNS = ("time/s", "cycle number", "freq/Hz", "Re(Z)/Ohm", "-Im(Z)/Ohm",
           "|Z|/Ohm", "Phase(Z)/deg")

_NAME = re.compile(r"^EIS_state_([IVX]+)_(\d+)C(\d+)\.txt$")
_ROMAN = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
          "VI": 6, "VII": 7, "VIII": 8, "IX": 9}


def parse_name(fn: str) -> dict | None:
    """파일명에서 좌표를 푼다. 규칙에 안 맞으면 None (조용히 추측하지 않는다)."""
    m = _NAME.match(fn)
    if not m:
        return None
    roman, temp, cell = m.group(1), int(m.group(2)), int(m.group(3))
    if roman not in _ROMAN:
        return None
    return {"state": _ROMAN[roman], "state_roman": roman,
            "temp_C": temp, "cell": cell}


def _is_data_row(line: str) -> list[float] | None:
    """이 줄이 계약 열 수만큼의 수치인가. 아니면 None."""
    f = line.split()
    if len(f) != len(COLUMNS):
        return None
    try:
        return [float(x) for x in f]
    except ValueError:
        return None


def _assert_column_identity(rows: list[list[float]], path: Path,
                            probe: int = 64) -> None:
    """열 순서를 **물리 항등식으로 확인**한다 (헤더 유무와 무관).

    ★ 실측 (2026-09-03, 1저자 환경) — 이 데이터셋은 **헤더가 있는 파일과 없는
      파일이 섞여 있다.** `EIS_state_III_35C01.txt` 는 첫 줄부터 수치다.
      헤더가 없다고 읽기를 포기하면 데이터의 상당수를 버리고, 그냥 읽으면
      **열 순서를 가정**하는 것이다 — 가정한 순서가 틀리면 그 뒤 모든 수치가
      조용히 거짓이 된다.

    다행히 이 형식에는 **검사 가능한 항등식**이 둘 있다::

        |Z|      = hypot(Re(Z), Im(Z))          # Im = -( -Im )
        Phase(Z) = atan2(Im(Z), Re(Z))   [deg]

    실측으로 확인했다 (Re 0.29797 · -Im -0.02827 → hypot 0.29931 vs 파일
    0.29930 · atan2 5.41973° vs 파일 5.42007°). 이 둘이 맞으면 3~7열의 의미가
    **가정이 아니라 측정**으로 고정된다. 헤더가 있는 파일에도 똑같이 적용한다
    — 헤더는 거짓말할 수 있지만 항등식은 못 한다.
    """
    import math

    checked = 0
    for r in rows[:probe]:
        re_z, neg_im, abs_z, phase = r[3], r[4], r[5], r[6]
        im_z = -neg_im
        mag = math.hypot(re_z, im_z)
        if abs_z <= 0 or mag <= 0:
            continue                       # 0 근처는 상대오차가 의미 없다
        if abs(mag - abs_z) / abs_z > 1e-3:
            raise SystemExit(
                f"✗ {path.name}: |Z| 가 Re·Im 과 맞지 않는다 "
                f"(hypot {mag:.6g} ≠ 파일 {abs_z:.6g}) — 열 순서가 계약과 "
                "다르다는 뜻이다. 가정하고 읽지 않는다 (fail-closed)")
        want = math.degrees(math.atan2(im_z, re_z))
        if abs(want - phase) > 0.05:
            raise SystemExit(
                f"✗ {path.name}: Phase 가 atan2(Im, Re) 와 맞지 않는다 "
                f"({want:.4f}° ≠ 파일 {phase:.4f}°) — 열 순서가 계약과 "
                "다르다 (fail-closed)")
        checked += 1
    if checked == 0:
        raise SystemExit(
            f"✗ {path.name}: 항등식으로 확인할 수 있는 행이 하나도 없다 — "
            "열 의미를 실물로 고정하지 못하므로 읽지 않는다 (fail-closed)")


def read_spectra(path: Path) -> tuple[bool, list[list[float]]]:
    """(헤더가 있었나, 행들).

    헤더가 있으면 계약 열 이름을 순서대로 확인하고, 없으면 첫 줄부터 데이터로
    읽는다. **어느 쪽이든** 열 순서는 `_assert_column_identity()` 가 물리
    항등식으로 확인한다.
    """
    lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
    if not lines:
        raise SystemExit(f"✗ {path.name} 이 비어 있다")

    first_as_data = _is_data_row(lines[0])
    has_header = first_as_data is None
    if has_header:
        head, body = lines[0], lines[1:]
        pos, ok = 0, True
        for c in COLUMNS:
            i = head.find(c, pos)
            if i < 0:
                ok = False
                break
            pos = i + len(c)
        if not ok:
            raise SystemExit(
                f"✗ {path.name} 의 첫 줄이 데이터도 아니고 계약 헤더도 아니다.\n"
                f"  기대 열: {list(COLUMNS)}\n  실제: {head.strip()[:140]!r}")
    else:
        body = lines

    rows = []
    for ln in body:
        if not ln.strip():
            continue
        r = _is_data_row(ln)
        if r is None:
            raise SystemExit(
                f"✗ {path.name} 에 계약과 다른 행이 있다: {ln[:100]!r}")
        rows.append(r)
    if not rows:
        raise SystemExit(f"✗ {path.name} 에 데이터 행이 없다")
    _assert_column_identity(rows, path)
    return has_header, rows


def summarize(path: Path) -> dict:
    has_header, rows = read_spectra(path)
    cyc = sorted({r[1] for r in rows})
    frq = [r[2] for r in rows]
    return {"rows": len(rows), "spectra": len(cyc), "header": int(has_header),
            "cycle_min": min(cyc) if cyc else float("nan"),
            "cycle_max": max(cyc) if cyc else float("nan"),
            "freq_min": min(frq) if frq else float("nan"),
            "freq_max": max(frq) if frq else float("nan")}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


FIELDS = ("file", "sha256", "bytes", "rows", "spectra", "header", "state",
          "state_roman", "temp_C", "cell", "cycle_min", "cycle_max",
          "freq_min", "freq_max")


def scan() -> list[dict]:
    if not DATA.is_dir():
        raise SystemExit(
            f"✗ 데이터가 없다: {DATA}\n"
            "  zip 을 여기로 풀어라 (원본은 커밋되지 않는다 — .gitignore)")
    out, unnamed = [], []
    for p in sorted(DATA.glob("*.txt")):
        meta = parse_name(p.name)
        if meta is None:
            unnamed.append(p.name)
            continue
        rec = {"file": p.name, "sha256": sha256(p), "bytes": p.stat().st_size}
        rec.update(summarize(p))
        rec.update(meta)
        out.append(rec)
    if unnamed:
        # 조용히 버리지 않는다 — 무엇을 안 세었는지 말한다.
        print(f"⚠ 이름 규칙에 안 맞아 제외한 파일 {len(unnamed)}개: "
              f"{', '.join(unnamed[:5])}{' …' if len(unnamed) > 5 else ''}",
              file=sys.stderr)
    return out


def write_manifest(recs: list[dict]) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(FIELDS)]
    for r in recs:
        lines.append("\t".join(str(r[k]) for k in FIELDS))
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_manifest() -> list[dict]:
    if not MANIFEST.is_file():
        raise SystemExit(f"✗ manifest 가 없다: {MANIFEST} (먼저 --scan)")
    body = MANIFEST.read_text(encoding="utf-8").splitlines()
    head = body[0].split("\t")
    return [dict(zip(head, ln.split("\t"))) for ln in body[1:] if ln.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--scan", action="store_true", help="manifest 생성/갱신")
    g.add_argument("--verify", action="store_true", help="manifest 와 대조")
    g.add_argument("--show", metavar="FILE", help="한 파일 요약")
    a = ap.parse_args()

    if a.show:
        p = DATA / a.show
        if not p.is_file():
            raise SystemExit(f"✗ 없다: {p}")
        s = summarize(p)
        meta = parse_name(p.name) or {}
        print(f"{p.name}")
        print(f"  좌표   state {meta.get('state_roman','?')} · "
              f"{meta.get('temp_C','?')} °C · cell {meta.get('cell','?')}")
        print(f"  행     {s['rows']:,}   스펙트럼 {s['spectra']}")
        print(f"  cycle  {s['cycle_min']:g} … {s['cycle_max']:g}")
        print(f"  freq   {s['freq_min']:.4g} … {s['freq_max']:.4g} Hz")
        print(f"  sha256 {sha256(p)}")
        return 0

    if a.scan:
        recs = scan()
        write_manifest(recs)
        print(f"→ {MANIFEST.relative_to(HERE.parent)}  ({len(recs)}개 파일)")
        temps = sorted({r["temp_C"] for r in recs})
        states = sorted({r["state"] for r in recs})
        cells = sorted({r["cell"] for r in recs})
        print(f"  state {states}")
        print(f"  temp  {temps} °C")
        print(f"  cell  {cells}")
        print(f"  총 행 {sum(r['rows'] for r in recs):,} · "
              f"총 스펙트럼 {sum(r['spectra'] for r in recs):,}")
        return 0

    # --verify
    want = {r["file"]: r for r in read_manifest()}
    have = {p.name for p in DATA.glob("*.txt")} if DATA.is_dir() else set()
    bad = []
    for fn, r in sorted(want.items()):
        p = DATA / fn
        if not p.is_file():
            bad.append(f"{fn}: 없다")
            continue
        got = sha256(p)
        if got != r["sha256"]:
            bad.append(f"{fn}: sha256 다름 ({got[:12]}… ≠ {r['sha256'][:12]}…)")
    extra = sorted(have - set(want))
    if extra:
        print(f"⚠ manifest 에 없는 파일 {len(extra)}개: {', '.join(extra[:5])}")
    if bad:
        print(f"✗ 어긋난 파일 {len(bad)}개:", file=sys.stderr)
        for b in bad[:20]:
            print(f"  {b}", file=sys.stderr)
        return 1
    print(f"✓ {len(want)}개 파일이 manifest 와 바이트까지 같다")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
