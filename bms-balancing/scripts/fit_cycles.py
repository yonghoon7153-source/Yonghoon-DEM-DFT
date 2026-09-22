#!/usr/bin/env python3
"""사이클별 α·β 적합 (BML_R1_RESPONSE §9 결정 실험) — `cycles_<cell>_<si>.csv` + `.meta.json` 을 게시한다.

    python3 scripts/fit_cycles.py --data-root <원자료 루트> --half-cell <pristine.xlsx> --full-cell <cycles.xlsx> \\
        --cell L_ref1 --si-source Li [--cycles 0,1,2] [--starts 20] [--seed 0] [--w-dqdv 0] --out <DIR>

원자료 형식은 규진팀 파이프라인이 읽는 그것 — 풀셀 워크북에 '<cycle>_capacity'/'<cycle>_voltage' 열, cycle 0 이 기준행.
산출은 하네스 계약을 지킨다: 행마다 run_id·receipt, sidecar 에 실행 조건·git 전/후·env·argv·roster, 잠금 안 원자적 게시.
다음: `python3 scripts/check_rails.py <DIR>/cycles_<cell>_<si>.csv` (sidecar 의 lb/ub 를 3 층 설정으로 읽는다) ·
`python3 scripts/check_u14.py --new <DIR> --schema-only`.

종료 코드: 0 게시 · 2 입력/인자 문제 (cycle 0 없음 · 모르는 cycle · 파일 없음) · 1 적합 실패.
`--seed` 만 바꿔 두 번 돌려 비교하는 것이 결정 실험의 두 번째 절반이다 (시작점이 정한 적합인가) — `--scale-seed` 는
고정한다 (기본 0). 두 산출의 `scale_*` 열이 같아야 그 차이가 시작점의 것이다.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import sys
import uuid

HERE = pathlib.Path(__file__).resolve().parent
REPO_DIR = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(REPO_DIR))
from bms_balancing import cycles as C           # noqa: E402
from bms_balancing import data as D             # noqa: E402
from bms_balancing import schema as S           # noqa: E402
from bms_balancing.verify import atomic_write_csv, publish_lock   # noqa: E402
from provenance import git_provenance, sidecar_dict               # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-root", default=None, help="data/literature 가 있는 루트 (없으면 BMS_DATA_ROOT)")
    ap.add_argument("--half-cell", required=True, type=pathlib.Path, help="기준(pristine) 반쪽전지 xlsx")
    ap.add_argument("--full-cell", required=True, type=pathlib.Path, help="풀셀 사이클 워크북 ('<cycle>_capacity' 열)")
    ap.add_argument("--cell", required=True, help="셀 라벨 (산출 이름 cycles_<cell>_<si>.csv)")
    ap.add_argument("--si-source", default="Li", choices=(*D.SI_SOURCES, D.EXTERNAL_SI_SOURCE),
                    help=f"정본 8 소스 중 하나, 또는 '{D.EXTERNAL_SI_SOURCE}' (그때는 --literature 필수)")
    ap.add_argument("--literature", default=None, type=pathlib.Path,
                    help="정본 로스터 밖의 문헌 파일 (Si_capacity/Si_voltage/Gr_capacity/Gr_voltage 한 시트) — pyDMA 예제 같은 검증 데이터용. 주면 --si-source 는 external 이어야 한다")
    ap.add_argument("--cycles", default="", help="쉼표 목록 — 비우면 워크북의 전부")
    ap.add_argument("--starts", type=int, default=20, help="MultiStart 시작점 수 (원본 electrode_balancing_blend 은 20)")
    ap.add_argument("--seed", type=int, default=0, help="MultiStart 시작점 seed — 이것만 바꿔 두 번 돌리면 '시작점이 정한 적합인가' 를 묻는다")
    ap.add_argument("--scale-seed", type=int, default=0, help="목적함수 scale 표본 seed (R5-07) — 시작점 실험에서는 고정한다")
    ap.add_argument("--w-dqdv", type=float, default=0.0, help='dQ/dV 항 가중 (원본 기본 0 = "방법3")')
    ap.add_argument("--objective-version", required=True, choices=S.OBJECTIVE_VERSIONS,
                    help="⑥ chain rule 계약 — 어느 미분으로 적합하나. legacy_matlab = 원본 그대로(dv_cell 에 1/a 없음, "
                         "재현용) · chain_rule_v2 = 수학적으로 맞는 미분. **기본값 없음** — 적어야 돈다 (Codex R17 §4)")
    ap.add_argument("--gamma-prefit", action="store_true",
                    help="γ 를 반쪽전지만으로 먼저 적합해 초기값으로 (fit_gamma_si.m · pyDMA Track C 규약)")
    ap.add_argument("--gamma-lb", type=float, default=None, help="γ 하한 (기본 0.0; Track C 는 0.02)")
    # ⚠ 폭 (BML_R1_RESPONSE §12-5): LAM 분할은 이 데이터에서 점추정으로 보고할 수 없다. 켜면 사이클마다
    #   근최적 집합 위의 LAM/LLI 폭을 **이 실행이 쓴 상자에서** 재어 같은 행에 싣는다 (W-11·W-12).
    #   기본은 꺼짐 — 사이클당 SLSQP 를 여러 번 돌리므로 느리다. 끄면 칸이 **비고 0 이 아니다** (W-10).
    ap.add_argument("--widths", action="store_true",
                    help="사이클마다 LAM/LLI 폭을 같이 낸다 (근최적 집합 극값; 느리다)")
    ap.add_argument("--width-tol", type=float, default=0.01,
                    help="폭의 허용 — 최적 목적함수 대비 분수 (기본 0.01 = 1%%). 이 값을 안 밝힌 폭은 인용 불가")
    ap.add_argument("--width-starts", type=int, default=4, help="폭 계산의 시작점 수 (기본 4)")
    # ⚠ W-20 (§15): 켜면 `mode_profile_extrema` 를 같이 돌려 **합집합**을 취한다 — 둘 다 하한이므로 넓은 쪽이
    #   더 나은 하한이다. 기본 0(꺼짐)인 이유는 둘이다: ① 사이클마다 격자×시작점만큼 SLSQP 가 더 돈다
    #   ② 이득이 목적함수 모양에 달렸다 (굽은 골짜기 반례에서는 제약 극값이 이미 더 넓어 합집합 이득 0 — 실측).
    #   켜고 끈 두 산출은 `width_method` 가 달라 `width_report.py` 가 비교를 거부한다.
    ap.add_argument("--width-grid", type=int, default=0,
                    help="폭 격자 점 수 — 0 이면 제약 극값만, >0 이면 mode 프로파일과 합집합 (상태 경로 기본은 21)")
    ap.add_argument("--out", required=True, type=pathlib.Path, help="산출 디렉터리")
    ap.add_argument("--run-id", default=None)
    a = ap.parse_args(argv)
    started = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "git": git_provenance(cwd=str(REPO_DIR), output_roots=(str(a.out), "out"))}
    if not a.half_cell.is_file() or not a.full_cell.is_file():
        print(f"! 입력 파일이 없다: {[str(p) for p in (a.half_cell, a.full_cell) if not p.is_file()]} → 종료 코드 2"); return 2
    if not re_label(a.cell):
        print(f"! --cell 은 산출 이름에 들어간다 — 글자·숫자·_·- 만: {a.cell!r} → 종료 코드 2"); return 2
    try:
        root = D.data_root(a.data_root)
    except SystemExit as e:
        print(f"! {e} → 종료 코드 2"); return 2
    cycles = [int(x) for x in a.cycles.split(",") if x.strip()] if a.cycles else None
    rid = a.run_id or os.environ.get("BMS_RUN_ID") or uuid.uuid4().hex
    try:
        res = C.fit_cycles(root, a.half_cell, a.full_cell, a.si_source, cell=a.cell, cycles=cycles,
                           objective_version=a.objective_version,          # ⑥ — sidecar 에는 settings 로 실린다
                           n_starts=a.starts, seed=a.seed, scale_seed=a.scale_seed, w_dqdv=a.w_dqdv, run_id=rid,
                           literature=a.literature, gamma_prefit=a.gamma_prefit, gamma_lb=a.gamma_lb,
                           widths=a.widths, width_tol=a.width_tol, width_starts=a.width_starts, width_grid=a.width_grid,
                           log=lambda s: print(s, flush=True))
    except (ValueError, KeyError) as e:
        print(f"! {e} → 종료 코드 2"); return 2
    except RuntimeError as e:
        print(f"! 적합 실패: {e} → 종료 코드 1"); return 1
    a.out.mkdir(parents=True, exist_ok=True)
    art = a.out / f"cycles_{a.cell}_{a.si_source}.csv"
    rows = [{k: r.get(k) for k in S.CYCLES_ROW} for r in res["rows"]]
    atomic_write_csv(art, rows, list(S.CYCLES_ROW))
    with publish_lock(art):                                   # 게시와 meta 가 같은 잠금 안 (R5-04)
        data = art.read_bytes()
        pv = git_provenance(cwd=str(REPO_DIR), artifact=str(art), output_roots=(str(a.out), "out"))
        meta = sidecar_dict(art.name, data, run_id=rid, started=started, argv=list(sys.argv), pv=pv, extra={
            "cell": a.cell, "si_source": a.si_source, "starts": int(a.starts), "seed": int(a.seed),
            "literature": (str(a.literature) if a.literature else None),
            "gamma_prefit": bool(a.gamma_prefit), "gamma_lb": a.gamma_lb,
            "widths": bool(a.widths), "width_tol": (float(a.width_tol) if a.widths else None),
            "width_starts": (int(a.width_starts) if a.widths else None),
            "scale_seed": int(a.scale_seed),
            "w_dqdv": float(a.w_dqdv), "cycles": res["cycles"], "status": "complete",
            # ⚠ R16 (조건 8 축 ②): 모집단 선언의 식별자
            "dataset_manifest": D.half_cell_manifest_identity(),
            "data_root": str(root), "half_cell_path": str(a.half_cell), "full_cell_path": str(a.full_cell),
            "consumed_inputs": res["consumed"], **res["settings"]})
        tmp = art.with_name(art.name + ".meta.part")
        tmp.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, art.with_name(art.name + ".meta.json"))
    print(f"\n→ {art}  (행 {len(rows)} · run_id {rid})")
    print("CYCLES_RESULT " + json.dumps({"artifact": str(art), "run_id": rid, "cycles": res["cycles"],
                                          "n_rows": len(rows)}, ensure_ascii=False))
    print(f"다음: python3 scripts/check_rails.py {art}   ·   python3 scripts/check_u14.py --new {a.out} --schema-only")
    return 0


def re_label(s: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_\-]+", s or ""))


if __name__ == "__main__":
    sys.exit(main())
