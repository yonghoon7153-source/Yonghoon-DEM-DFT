"""측정된 음극 OCP 가 열화하면서 **모양이 바뀌는가** — γ_Si 를 자유 파라미터로
둘 근거가 있는지 직접 본다.

## 왜 이 질문인가

목적함수는 음극을 **문헌 순수 Si + 순수 Gr 을 γ 로 섞어** 만든다. 그런데 이
셀의 음극은 **실제로 측정돼 있다** (`data/half_cell/<src>/<state>.xlsx` 의
`NE_capacity`/`NE_voltage`). 측정본은 γ 초기값 잡는 데만 쓰인다.

γ 를 자유롭게 두는 정당한 이유는 하나다: 열화하면서 음극 OCP **모양 자체가
바뀌니까** (Si 가 먼저 죽으면 유효 Si 분율이 준다). 파우치 셀은 반쪽전지를
상태마다 따로 쟀으므로 그 전제를 직접 확인할 수 있다.

    측정 곡선이 겹친다   -> γ 를 자유로 둘 근거가 약하다. 측정본을 쓰면
                           '문헌 곡선 선택' 축이 통째로 사라진다
    측정 곡선이 갈린다   -> γ 가 흡수할 실체가 있다. 그러면 적합된 γ 가 그
                           변화를 실제로 따라가는지가 다음 질문

## 무엇을 재나

pristine 대비 각 상태에서
  (a) **측정** E_NE(x) 의 변화량   — 실제로 일어난 일
  (b) **모델** Blend.E(x, γ_적합) 의 변화량 — γ 가 만들어 낸 변화

(b) 가 (a) 보다 훨씬 크면, γ 가 측정된 모양 변화 밖의 것을 흡수했을 가능성이
있다. (b) 가 (a) 보다 훨씬 작으면 적합이 γ 를 그만큼만 움직였다는 뜻이다.

⚠ (b)/(a) 는 **적합이 γ 를 얼마나 움직였나**이지 γ 의 표현력도, 측정 음극이
  블렌드 모양인지의 판정도 아니다 (Codex R2-08 · R3-02: 정확히 `Blend(x, γ)` 인
  합성 곡선에 적합이 고른 쌍을 주면 같은 비가 나온다). 원인(모델 부적합·잡음·
  다른 파라미터의 보상)은 이 스크립트가 가르지 않는다.

  (d) **γ 여유** (Codex R3-03): 기준 γ_ref 에서 합법 상자 [0, 0.5] 까지의 양방향
  Δγ, 합법 γ 전체가 낼 수 있는 최대 변화(격자), (a) 이상을 내는 **가장 가까운
  합법 γ 증인**(없으면 없음). 두 점 secant 를 외삽한 "필요 Δγ" 는 쓰지 않는다 —
  비선형이고, 300_0009 에서 그렇게 구한 ±0.365 는 양쪽 다 상자 밖이었다.
  증인은 진폭의 존재이지 모양 일치가 아니다.

⚠ 둘은 다른 물건이다 (측정본은 실제 음극, 블렌드는 대용품). 그래서 **절대
  값이 아니라 pristine 대비 변화량**을 견준다.

    python3 scripts/ne_shape.py --source GITT --si-source Li

## 명부와 종료 코드 계약 (Codex R8-03 · R9-04 · R9-06 · P2-5)

requested 명부는 **파일 존재를 보기 전에** 고정한다 — 소스에 선언된 상태(`D.HALF_FILE[source]` ∩ `D.STATES`,
pristine 제외) 또는 `--states` 로 명시한 목록. 반쪽전지 파일이 없는 상태는 `missing_input` 으로, matrix 짝이 없는
상태는 `missing`(pair) 으로 **따로** 남는다. 산출 meta 의 typed `status` 와 종료 코드:

    rc 0  complete — requested 전부에 입력과 γ 짝이 있다 → canonical `<write>/ne_shape_<src>_<si>.csv` 에 게시
    rc 1  none     — γ 짝이 하나도 없다 (부분이 아니라 **없음**; 『missing pair 면 rc 3』 보다 먼저 난다)
    rc 3  partial  — 일부만 짝이 있거나 입력이 없는 상태가 있다

none·partial 은 canonical 을 **건드리지 않고** `<write>/partial/` 에만 쓴다 (완전성 판정이 게시보다 먼저다).
"""
from __future__ import annotations
import argparse, csv, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))  # provenance

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
REPO_DIR = pathlib.Path(__file__).resolve().parents[1]   # git 출처는 이 스크립트가 속한 저장소 (R6 내부 F7: cwd 무관)
from bms_balancing import data as D                      # noqa: E402
from bms_balancing.model import LB5, UB5, Blend, HalfCell  # noqa: E402

# ── 종료 코드 계약 (Codex R8-03 · R9-06 · P2-5) — meta 의 typed status 와 1:1 ──────────────────────────────
#   rc 0 = complete : requested 전부에 입력과 γ 짝이 있다 → canonical <write>/ne_shape_<src>_<si>.csv 에 게시
#   rc 1 = none     : γ 짝이 하나도 없다 — 부분이 아니라 없음 (missing pair 면 rc 3 보다 먼저 난다)
#   rc 3 = partial  : 일부만 짝이 있거나 입력이 없는 상태(missing_input)가 있다
#   none·partial 은 canonical 을 건드리지 않고 <write>/partial/ 에만 쓴다 (완전성 판정이 게시보다 먼저다)
EXIT_BY_STATUS = {"complete": 0, "none": 1, "partial": 3, "subset": 3}

GRID = np.linspace(0.02, 0.98, 400)     # 양 끝은 외삽이라 뺀다
GAMMA_GRID = np.linspace(LB5[4], UB5[4], 501)   # (d) 합법 γ 격자 — 0.001 간격


def gamma_headroom(blend: Blend, g_ref: float, da_mV: float) -> dict:
    """(d) 기준 γ_ref 에서 합법 γ 가 낼 수 있는 변화 — 양방향 여유·격자 최대·(a) 증인.

    `witness` 는 |Blend(x,γ) − Blend(x,γ_ref)| 의 최대가 (a) 이상인 합법 γ 중 γ_ref 에
    **가장 가까운** 것 (격자 기준). 없으면 None. 진폭의 존재 증인이지 모양 일치가 아니다.
    """
    base = blend.E(GRID, g_ref)
    amp = np.array([float(np.max(np.abs(blend.E(GRID, g) - base))) * 1e3 for g in GAMMA_GRID])
    i = int(np.argmax(amp))
    reach = np.flatnonzero(amp >= da_mV - 1e-9)
    witness = float(GAMMA_GRID[reach[np.argmin(np.abs(GAMMA_GRID[reach] - g_ref))]]) if reach.size else None
    return {"dneg": float(LB5[4] - g_ref), "dpos": float(UB5[4] - g_ref),
            "fam_max": float(amp[i]), "g_at_max": float(GAMMA_GRID[i]),
            "witness": witness, "wdelta": None if witness is None else witness - g_ref}


def fitted_pair(out_dir: pathlib.Path, state: str, src: str,
                si: str) -> tuple[float, float] | None:
    """`matrix_<state>.csv` 의 **한 행에서** (그 상태의 γ, 그 실행의 기준 γ).

    ⚠ 짝을 같은 행에서 꺼내는 것이 중요하다. `matrix` 는 조합마다 pristine 을
      **다시 적합**하므로, 기준 γ 가 파일마다·조합마다 다르다. 다른 행의 기준을
      가져다 쓰면 있지도 않은 변화를 만들어 낸다.
      (그리고 `matrix_pristine.csv` 는 애초에 없다 — pristine 은 상태가 아니라
      매 실행의 기준이다. 첫 판이 그걸 찾다가 전부 nan 을 냈다.)
    """
    info = fitted_pair_info(out_dir, state, src, si)
    return None if info is None else (info["gamma_target"], info["gamma_ref"])


def fitted_pair_info(out_dir: pathlib.Path, state: str, src: str, si: str):
    """`fitted_pair` 와 같은 선택 + **실제로 소비한 파일의 identity** (Codex R5-05): 경로·sha256·선택한 행.

    소비하는 파일은 `matrix_<state>.csv` 하나(정본, Codex R6-04)이고 untracked 재게시도 그대로 입력이 된다 — git 출처
    (추적 파일)만으로는 그 사실이 남지 않아 두 실행의 meta 가 같았다. 소비한 파일은 tracked 여부와 무관하게 여기서 적는다.
    """
    import hashlib, io
    from provenance import read_unit
    # ⚠ Codex R6-04: 정본은 unversioned 이름 하나. `_vN` 이 남아 있으면 말만 하고 쓰지 않는다 (archive 로).
    stale = sorted(p.name for p in out_dir.glob(f"matrix_{state}_v[0-9]*.csv"))
    if stale:
        print(f"  ! {', '.join(stale)}: 판 번호가 붙은 옛 산출 — 정본은 matrix_{state}.csv 하나다; out/archive/ 로 (Codex R6-04)",
              file=sys.stderr)
    f = out_dir / f"matrix_{state}.csv"
    if f.is_file():
        # R6 내부 F03·F07 · Codex R6-01·02: bytes 와 meta 를 한 번씩 읽어 서로 대조한 snapshot 만 파싱·해시한다
        ok, why, data, _meta = read_unit(f)
        if ok is False:
            raise RuntimeError(f"{f.name}: 묶음 불일치/미완 ({why}) — 섞인 산출을 소비하지 않는다 (R6 내부 F07 · Codex R6-01·02)")
        rows = list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))
        # ⚠ Codex R9-05: 전 판은 첫 match 를 **즉시** 반환했다 — 서명된 matrix 에 (GITT, Li, 0) 이 두 행이면 행 순서가 γ 를
        #   정했다 (0.10 ↔ 0.40, γ 변화 17.59 ↔ 35.73 mV, 둘 다 paired 1/1 rc 0). checker 와 같은 typed validator
        #   (`schema.unique_rows` · 정규화 key: w_dqdv 는 숫자라 "0" 과 "0.0" 은 같은 행) 로 파일 전체의 key 유일성을
        #   먼저 강제한다 — 중복이면 그 파일은 소비하지 않는다.
        from bms_balancing import schema as S
        # ⚠ Codex R11 P1-7: 공용 validator 가 **실패로 판정한 묶음**을 production reader 가 소비하고 있었다 —
        #   `error="optimizer failed"` 인 서명 행의 (γ, γ_ref) 를 정상 과학 입력으로 돌려줬다. 같은 검사를 여기서도.
        header = list(rows[0]) if rows else []
        # ⚠ Codex R13 P1-1 후속: **정본 자리** 규칙(좁힌 실행이 canonical 이름에 앉음)은 산출 내용의 결함이
        #   아니다 — 정직한 subset 도 과학 입력이다. 그 판정은 승격 gate(`check_u14`)가 한다.
        problems = [q for q in S.check_rows("matrix", rows, header, name=f.name)
                    if not q.startswith(S.CANONICAL_SLOT_PREFIX)]
        if problems:
            raise RuntimeError(f"{f.name}: 공용 스키마 검증 실패 {problems[:3]} — 이 묶음은 과학 입력이 아니다 "
                               f"(checker 와 같은 validator 다, Codex R11 P1-7)")
        _, dup, _ = S.unique_rows(rows, S.matrix_key)
        if dup:
            raise RuntimeError(f"{f.name}: 중복 key {dup} — 같은 (half_cell, si, w_dqdv) 행이 둘 이상이다; 첫 행을 고르지 "
                               f"않는다 (Codex R9-05). 재실행으로 유일한 묶음을 만들 것")
        hits = [(i, r) for i, r in enumerate(rows) if S.matrix_key(r) == (src, si, 0.0)]
        if len(hits) > 1:                                   # unique_rows 가 놓칠 수 없지만 계약은 여기에도 적는다
            raise RuntimeError(f"{f.name}: ({src}, {si}, 0) 행이 {len(hits)} 개 — 중복 (Codex R9-05)")
        if hits:
            idx, r = hits[0]
            if not r.get("ref_gamma_Si"):
                return None          # 옛 판 산출 — ref_* 열이 없다
            return {"gamma_target": float(r["gamma_Si"]), "gamma_ref": float(r["ref_gamma_Si"]),
                    "file": str(f), "sha256": hashlib.sha256(data).hexdigest(),
                    "row": {"index": idx, "half_cell": r.get("half_cell"), "si": r.get("si"),
                            "w_dqdv": r.get("w_dqdv"), "run_id": r.get("run_id")}}
    return None


def raw_ne_capacity(path: pathlib.Path) -> float:
    """정규화 **전** 음극 용량. (a) 의 변화가 모양 탓인지 용량 탓인지 가르려고."""
    import pandas as pd
    df = pd.read_excel(path)
    c = pd.to_numeric(df["NE_capacity"], errors="coerce").dropna().to_numpy()
    return float(c.max()) if c.size else float("nan")


def run_started(roots=("out",)) -> dict:
    """계산 **시작** 시각과 그때의 git 상태 — `run_states.sh` 의 `LAST_STARTED_UTC`·`LAST_PRE_PV` 와 같은 역할 (R6 내부
    F04: 뒤에서 한 번 샘플한 값은 "돌린 코드가 commit 과 같았나" 에 거짓 답을 줄 수 있다). `_write_csv` 가 끝 상태와 댄다.
    `roots` 는 산출 자리(코드가 아닌 곳) — 빈 것은 뺀다."""
    import datetime
    from provenance import git_provenance
    return {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "git": git_provenance(cwd=str(REPO_DIR), output_roots=tuple(str(r) for r in roots if r))}


def _row_receipt(consumed, state):
    """행 하나의 receipt — sidecar 의 상태별 dict 를 checker 가 요구하는 **역할** 모양(`schema.SHAPE_ROLES`)으로.

    ⚠ Codex R13 §Q6: shape 의 입력 identity 는 sidecar 에만 상태별로 있었다 — checker 의 receipt 계약(행 key 별 역할·sha,
      R11 P1-1)과 모양이 달라 대조 대상이 아니었다. 역할: matrix(그 상태의 γ 짝) · half_cell(그 상태) · half_cell_pristine
      (기준) · literature.gr · literature.si. 짝 없는 행은 None — receipt 를 지어내지 않는다 (빈 칸은 content 로 막힌다;
      partial 은 success 가 아니다).
    """
    c = consumed if isinstance(consumed, dict) else {}
    mine = c.get(state)
    if not isinstance(mine, dict) or not isinstance(mine.get("matrix"), dict):
        return None
    m = mine["matrix"]
    return {"matrix": {"path": m.get("path") or m.get("file") or "", "sha256": m.get("sha256", ""), "row": m.get("row")},
            "half_cell": mine.get("half_cell"),
            "half_cell_pristine": (c.get("pristine") or {}).get("half_cell"),
            "literature": c.get("literature")}


def _write_csv(d: pathlib.Path, a, rows, cap, base_cap, cwhere, headroom=None, consumed=None,
               pairing=None, status="complete", started=None, argv=None) -> pathlib.Path:
    """표를 그대로 CSV 로. 옆에 `.meta.json` 을 같이 둔다 (run_states.sh 와 같은 규약).

    `cap_delta_pct` 를 **반드시 같이** 남긴다 — `(a) 측정변화` 는 정규화 뒤
    값이라 용량이 크게 변한 상태에서는 순수한 OCP 모양 변화로 읽으면 안 된다.
    그 한정어가 CSV 에서 떨어지면 숫자만 인용된다.
    """
    import json, os, tempfile, uuid
    from bms_balancing import schema as S
    from bms_balancing.verify import publish_lock
    from provenance import git_provenance, sidecar_dict
    d.mkdir(parents=True, exist_ok=True)
    roots = (str(d), str(getattr(a, "out_dir", "") or ""), "out")   # 산출 자리·matrix 입력 자리는 코드가 아니다
    if started is None:          # 직접 호출(리뷰 repro·테스트) — 시작점은 writer 진입이다; `main` 은 입력을 읽기 전 시각을 준다
        started = run_started(roots)
    art = d / f"ne_shape_{a.source}_{a.si_source}.csv"
    # ⚠ R6 내부 F02: 전 판은 최종 경로에 `open("w")` 로 직접 쓰고(비원자) git 조회 뒤 meta 를 따로 썼다 — 잠금·
    #   run_id·sha256 이 없어 두 시도가 끼어들면 CSV=B · meta(consumed_inputs)=A 가 남고 verify_unit 은 '옛 meta'.
    #   run_states 의 게시 규약과 같게: 시도별 임시 → 잠금 안 교체 → 같은 잠금 안에서 sha256 을 meta 에.
    rid = os.environ.get("BMS_RUN_ID") or uuid.uuid4().hex
    globals()["LAST_RUN_ID"] = rid          # 자체 리뷰 C29: 보고는 **이 프로세스가 만든 id** 로 한다
    fh = tempfile.NamedTemporaryFile("w", dir=d, prefix=art.name + ".", suffix=".part", delete=False,
                                     newline="", encoding="utf-8")
    with fh as f:
        w = csv.writer(f, lineterminator="\n")
        # ⚠ Codex R13 §Q6: 열 이름의 정본은 `schema.SHAPE_ROW` 다 — 전 판은 여기 literal 20 개였고 checker 는 shape 라는
        #   종류를 몰라 profile 로 읽었다 (열 19 개가 "모르는 열"). producer 와 checker 가 같은 tuple 을 쓴다.
        header = list(S.SHAPE_ROW)
        w.writerow(header)
        for s_, da, db, ratio, cmax, crms, g, gr, *rest in rows:
            pe_max, pe_rms = (list(rest) + [float("nan"), float("nan")])[:2]
            c = cwhere.get(s_)
            h = (headroom or {}).get(s_)
            rec = _row_receipt(consumed, s_)
            # ⚠ Codex R2-10: 전 판은 `gamma_ref` 열에 **대상** γ 를 썼다. 두 역할을 따로.
            cells = {
                "state": s_, "cap_delta_pct": f"{100*(cap[s_]/base_cap-1):.4f}",
                "gamma_target": f"{g:.6f}" if g is not None else "",
                "gamma_ref": f"{gr:.6f}" if gr is not None else "",
                "measured_shape_mV": f"{da:.6f}", "gamma_shape_mV": f"{db:.6f}", "ratio_b_over_a": f"{ratio:.6f}",
                "blend_vs_meas_max_mV": f"{cmax:.6f}", "blend_vs_meas_rms_mV": f"{crms:.6f}",
                "max_at_x": f"{c[1]:.4f}" if c else "", "frac_over_50mV": f"{c[2]:.4f}" if c else "",
                "pe_shape_max_mV": f"{pe_max:.6f}", "pe_shape_rms_mV": f"{pe_rms:.6f}",
                # (d) γ 여유 (R3-03) — witness 가 빈 칸이면 '격자에서 (a) 를 내는 합법 γ 없음' (delta 와 함께 빈다)
                "legal_dgamma_neg": f"{h['dneg']:.6f}" if h else "", "legal_dgamma_pos": f"{h['dpos']:.6f}" if h else "",
                "gamma_family_max_mV": f"{h['fam_max']:.6f}" if h else "",
                "gamma_at_family_max": f"{h['g_at_max']:.4f}" if h else "",
                "gamma_witness": f"{h['witness']:.4f}" if h and h["witness"] is not None else "",
                "gamma_witness_delta": f"{h['wdelta']:+.4f}" if h and h["witness"] is not None else "",
                "run_id": rid,
                # ⚠ Codex R13 §Q6: 행마다 **자기** receipt (역할 `schema.SHAPE_ROLES`) — `check_u14` 가 두 실행의 입력
                #   identity 를 행 key(state)별로 댄다 (R11 P1-1). 짝 없는 행은 빈 칸 (receipt 를 지어내지 않는다).
                "inputs_sha": S.inputs_digest(rec) if rec else "",
                "consumed_inputs": json.dumps(rec, ensure_ascii=False, sort_keys=True) if rec else "",
            }
            w.writerow([cells[k] for k in header])
    # 산출물 자신의 재작성은 dirty 가 아니다 (R4-07); 저장소는 cwd 무관 (R6 F7); 산출 자리는 코드가 아니다 (R11 P1-9)
    pv = git_provenance(cwd=str(REPO_DIR), artifact=str(art), output_roots=roots)
    # shape 고유 필드 — 공통 축(run_id·sha256·roster·git 전/후·env·argv·시각)은 `provenance.sidecar_dict` 가 붙인다
    extra = {
        "half_cell_source": a.source,
        "si_source": a.si_source, "grid_n": int(GRID.size),
        "grid_range": [float(GRID[0]), float(GRID[-1])],
        "gamma_from": f"{a.out_dir}/matrix_<state>.csv 의 gamma_Si(대상)·ref_gamma_Si(기준)",
        "note": "measured_shape_mV 는 정규화 뒤 값 — cap_delta_pct 와 함께 읽을 것",
        "gamma_grid": [float(GAMMA_GRID[0]), float(GAMMA_GRID[-1]), int(GAMMA_GRID.size)],
        "headroom_note": "gamma_witness 는 (a) 이상의 진폭을 내는 합법 γ 의 존재 증인(격자)이지 "
                         "모양 일치가 아니다; 빈 칸 = 격자에서 없음 (R3-03)",
        # ⚠ Codex R5-05: "코드가 commit 과 같다" 와 "이 입력에서 이 결과가 나왔다" 는 다른 물음이다 —
        #   실제 소비한 matrix 파일(경로·sha256·행)·반쪽전지·문헌 입력의 identity 를 tracked 여부와 무관하게 남긴다.
        "consumed_inputs": consumed or {},
        # ⚠ Codex R8-03: 측정 통계는 모든 측정 행에서, γ-짝 통계는 requested/paired/missing 을 따로 — 어느 부분집합
        #   위의 진술인지 산출이 스스로 말한다
        "pairing": pairing or {},
        # ⚠ Codex R9-06 · P2-5: typed 완전성 — complete 만 canonical 에, none/partial 은 `<write>/partial/` 에 (호출부가 정한다)
        "status": status,
    }
    try:
        with publish_lock(art):                   # 게시와 meta 가 같은 잠금 안 (R5-04 규약)
            os.replace(fh.name, art)
            data = art.read_bytes()               # 잠금 안 **한 번** 읽은 bytes — sha256 과 roster 가 같은 bytes 의 것
            # ⚠ Codex R13 §Q6: U14 sidecar 계약 — `write_meta` 가 세 종류에 적는 것과 같은 축을 `sidecar_dict` 한 자리가 붙인다
            #   (run_id · sha256 · roster(같은 bytes) · git 전/후 · env · argv · 시각). 전 판은 이 중 하나도 없어 gate 가 전부 "누락".
            meta = sidecar_dict(art.name, data, run_id=rid, started=started, argv=argv, pv=pv, extra=extra)
            fd, tmp = tempfile.mkstemp(dir=d, prefix=art.name + ".meta.", suffix=".part")
            with os.fdopen(fd, "w", encoding="utf-8") as mf:
                mf.write(json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
            os.replace(tmp, art.parent / (art.name + ".meta.json"))
    except BaseException:
        pathlib.Path(fh.name).unlink(missing_ok=True)
        raise
    return art


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=None)
    ap.add_argument("--source", default="GITT", choices=list(D.HALF_FILE))
    ap.add_argument("--si-source", default="Li", choices=D.SI_SOURCES)
    ap.add_argument("--out-dir", default="out")
    # ⚠ 이 스크립트는 오래 **출력만** 했다. 그러면 여기서 나온 수치를
    #   FINDINGS 에 적어도 테스트가 재계산할 수 없고, 그건 이 저장소가
    #   반복해서 당한 드리프트 구조다 (정본은 artifact). 그래서 남긴다.
    ap.add_argument("--write", default="out", metavar="DIR",
                    help="산출 CSV 를 쓸 곳. 빈 문자열이면 안 쓴다. complete 만 여기(canonical)에; none/partial 은 "
                         "`<DIR>/partial/` 에 (Codex R9-06)")
    ap.add_argument("--states", default="", metavar="S1,S2",
                    help="정본 roster 의 **부분집합**만 돌린다 (진단용). 정본 roster 는 `D.declared_states(source)` 이고 "
                         "이 옵션은 그것을 **좁히기만** 한다 — 축소 실행은 status `subset` 이라 canonical 에 가지 않고 "
                         "종료 코드 3 이다 (Codex R10 P1-2). 중복·정본에 없는 상태는 거부한다")
    a = ap.parse_args()
    # ⚠ Codex R13 §Q6 (R6 내부 F04 와 같은 축): 시작 시각·git 상태는 **입력을 읽기 전**에 잡는다 — sidecar 가 끝 상태와 댄다.
    started = run_started((a.write, a.out_dir, "out"))

    root = D.data_root(a.data_root)
    out_dir = pathlib.Path(a.out_dir)
    # ⚠ Codex R9-04: 전 판은 `[s for s in D.STATES if half_cell_path(...).is_file()]` — 선언된 상태의 파일이 없으면 그 상태는
    #   requested 에 들기 **전에** 사라져 `{requested:[100], paired:[100], missing:[]}` 1/1 rc 0 이었다. requested 명부는
    #   파일 존재를 보기 전에 고정하고, 입력이 없는 상태는 `missing_input` 으로 따로 센다.
    # ⚠ Codex R10 P1-2: **정본 roster(authority)** 는 caller 가 못 바꾼다. 전 판은 `--states 100` 이 requested 를
    #   통째로 갈아치워 1 행 산출이 status `complete` 로 2 행 canonical 을 덮었고, `--states 100,100` 은 중복을 2/2
    #   complete 로 셌다. 이제 authority = `D.declared_states(source)` (선언 − 알려진 부재) 이고 `--states` 는 그
    #   부분집합만 고를 수 있다 — 축소 실행은 `subset` 이라 canonical 승격 대상이 아니다.
    from bms_balancing import schema as S
    authority = S.canonical_shape_states(a.source)     # checker 와 같은 함수 (= `D.declared_states`, Codex R13 §Q6)
    subset = False
    if a.states:
        requested = [s.strip() for s in a.states.split(",") if s.strip()]
        dup = sorted({s for s in requested if requested.count(s) > 1})
        unknown = [s for s in requested if s not in authority]
        if not requested or dup or unknown:
            print(f"! `--states` 를 받아들일 수 없다 — "
                  + (f"중복 {dup} · " if dup else "")
                  + (f"정본 roster 에 **선언되지 않은** 상태 {unknown} · " if unknown else "")
                  + (f"빈 목록 · " if not requested else "")
                  + f"정본 roster(authority) = {authority} (Codex R10 P1-2) → 종료 코드 2")
            return 2
        subset = list(requested) != list(authority)
        requested_from = "--states (부분집합)" if subset else "--states (정본 roster 와 같다)"
    else:
        requested, requested_from = list(authority), f"D.declared_states({a.source}) — 선언 − 알려진 부재"
    if not D.half_cell_path(root, a.source, "pristine").is_file():
        raise SystemExit(f"`{a.source}` 에 pristine 이 없다 — 기준이 없으면 못 잰다")
    available = [s for s in requested
                 if s in D.HALF_FILE.get(a.source, {}) and D.half_cell_path(root, a.source, s).is_file()]
    missing_input = [s for s in requested if s not in available]
    states = ["pristine"] + available

    # ⚠ Codex R6-03: 반쪽전지 워크북은 상태마다 **한 번 읽은 bytes** 로 HalfCell·raw 용량·identity 를 다 한다.
    #   전 판은 세 번 열었다 — 세 번째(identity) 직전에 재-export 되면 A 로 계산하고 B 의 서명을 적었다.
    hb = {s: D.read_input(D.half_cell_path(root, a.source, s)) for s in states}
    hcs = {s: HalfCell(hb[s].stream(), window=11, poly_order=3) for s in states}
    meas = {s: hcs[s].E_NE(GRID) for s in states}
    # ⚠ Codex R2-07 · L5-F2: 목적함수가 소비하는 반쪽전지 축은 **PE 뿐**이다. 대조 실험
    #   (반쪽전지 고정)의 강도를 말할 수 있는 유일한 양은 E_PE 의 상태별 변화다.
    pe = {s: np.asarray(hcs[s].E_PE(GRID), float) for s in states}
    cap = {s: raw_ne_capacity(hb[s].stream()) for s in states}
    lit_id: dict = {}
    si_c, si_v, gr_c, gr_v = D.load_literature(root, a.si_source, identity=lit_id)
    blend = Blend(si_c, si_v, gr_c, gr_v, window=11, poly_order=3)

    print(f"반쪽전지 {a.source} · 문헌 Si {a.si_source} · requested {len(requested)} 개 ({requested_from}) · 입력 있음 "
          f"{len(available)}" + (f" · **입력 없음(missing_input) {missing_input}**" if missing_input else ""))
    print(f"기준은 pristine. 격자 x={GRID[0]:.2f}~{GRID[-1]:.2f} ({GRID.size}점)\n")

    base_m, base_cap = meas["pristine"], cap["pristine"]
    print(f"{'state':10}{'용량 Δ%':>9}{'γ':>8}"
          f"{'(a) 측정변화':>13}{'(b) γ변화':>11}{'(b)/(a)':>9}"
          f"{'(c) |블렌드−측정|':>19}")
    print(f"{'':10}{'':9}{'':8}{'max mV':>13}{'max mV':>11}{'':9}"
          f"{'max mV':>13}{'rms mV':>6}")
    # ⚠ 자체 리뷰 C17: reader 가 공용 validator 를 쓰게 되면서(R11 P1-7) 옛 스키마 matrix 는 RuntimeError 다.
    #   그 예외가 `main` 밖으로 나가면 (a) sidecar 에 그 사실이 안 남고 (b) wrapper 메시지가 "SHAPE_RESULT 를
    #   내지 않았다" 라 원인을 안 가린다. 거부된 matrix 는 그 상태의 **짝 없음**으로 세고 이유를 남긴다 —
    #   그러면 typed status 가 정직하게 partial 로 나오고 무엇 때문인지도 붙는다.
    infos, rejected = {}, {}
    for s in states:
        if s == "pristine":
            continue
        try:
            infos[s] = fitted_pair_info(out_dir, s, a.source, a.si_source)
        except RuntimeError as e:
            infos[s], rejected[s] = None, str(e)
    if rejected:
        for s, why in rejected.items():
            print(f"  ! {s}: matrix 를 과학 입력으로 쓸 수 없다 — {why}", file=sys.stderr)
    consumed = {s: {"matrix": ({k: v for k, v in i.items() if k not in ("gamma_target", "gamma_ref")} if i else None),
                    "half_cell": hb[s].identity()}
                for s, i in infos.items()}
    consumed["pristine"] = {"half_cell": hb["pristine"].identity()}
    consumed["literature"] = lit_id
    first = states[1] if len(states) > 1 else "100"
    pr = (lambda i: None if i is None else (i["gamma_target"], i["gamma_ref"]))(infos.get(first))
    if pr is not None:
        dc = (blend.E(GRID, pr[1]) - base_m) * 1e3
        print(f"{'pristine':10}{0.0:>9.2f}{pr[1]:>8.4f}"
              f"{'—':>13}{'—':>11}{'—':>9}"
              f"{np.max(np.abs(dc)):>13.1f}{np.sqrt(np.mean(dc**2)):>6.1f}")
    rows, flips, cwhere = [], [], []
    for s in states:
        if s == "pristine":
            continue
        da = float(np.max(np.abs(meas[s] - base_m))) * 1e3
        pair = (lambda i: None if i is None else (i["gamma_target"], i["gamma_ref"]))(infos.get(s))
        if pair is None:
            db, ratio, g, gr = float("nan"), float("nan"), None, None
        else:
            g, gr = pair
            db = float(np.max(np.abs(blend.E(GRID, g) - blend.E(GRID, gr)))) * 1e3
            ratio = db / da if da > 0 else float("inf")
        # (c) **절대 일치** — 모델은 음극 OCP 를 Blend(x, γ) 라고 주장한다.
        #     a_NE·b_NE 는 풀셀 Q 를 전극 x 로 옮길 뿐 **곡선 모양을 못 고친다.**
        #     그러니 이 둘은 그냥 맞아야 한다. 안 맞으면 γ 로도 못 고치고
        #     그 차이는 a_NE·b_NE 로 밀려난다 — 그것이 LAM_NE·LLI 다.
        #   ⚠ **방향 규약**을 먼저 배제한다. `HalfCell` 은 끝점 둘로 방향을
        #     정하고, `Blend` 는 q 를 정렬한다. 둘의 x=0 이 반대 끝을 뜻하면
        #     (c) 가 거대하게 나오고 그것을 "블렌드가 틀렸다" 로 읽게 된다.
        #     그래서 뒤집은 것도 같이 재고 **작은 쪽**을 쓴다.
        if g is not None:
            be = blend.E(GRID, g)
            d_f = (be - meas[s]) * 1e3
            d_r = (be - meas[s][::-1]) * 1e3
            fwd = float(np.max(np.abs(d_f)))
            rev = float(np.max(np.abs(d_r)))
            flipped = rev < fwd
            dc = d_r if flipped else d_f
            cmax, crms = float(np.max(np.abs(dc))), float(np.sqrt(np.mean(dc ** 2)))
            # **어디가** 어긋나는지. max 만 보면 "모양이 아니다" 로 읽히지만,
            # rms 가 훨씬 작으면 어긋남이 **좁은 구간에 몰린** 것이고 그건
            # 전혀 다른 이야기다 (2026-09-10: max 70~147 mV 인데 rms 는
            # 19~24 mV 로 거의 일정했다 — 그걸 놓칠 뻔했다).
            xa = float(GRID[int(np.argmax(np.abs(dc)))])
            over = float(np.mean(np.abs(dc) > 50) * 100)
            cwhere.append((s, xa, over))
            if flipped:
                flips.append((s, fwd, rev))
        else:
            cmax = crms = float("nan")
        d_pe = (pe[s] - pe["pristine"]) * 1e3
        pe_max, pe_rms = float(np.max(np.abs(d_pe))), float(np.sqrt(np.mean(d_pe ** 2)))
        rows.append((s, da, db, ratio, cmax, crms, g, gr, pe_max, pe_rms))
        print(f"{s:10}{100*(cap[s]/base_cap-1):>9.2f}"
              f"{(f'{g:.4f}' if g is not None else '—'):>8}"
              f"{da:>13.2f}{db:>11.2f}{ratio:>9.2f}{cmax:>13.1f}{crms:>6.1f}")

    print("\n(PE 축 — 목적함수가 실제로 소비하는 반쪽전지 곡선) E_PE(state) − E_PE(pristine):")
    for r in rows:
        print(f"    {r[0]:10} max {r[8]:7.2f} mV   rms {r[9]:6.2f} mV")

    # (d) γ 여유 — Codex R3-03. "같은 크기를 낼 Δγ 는 상자 안" 은 여기서 실제로 검사한다.
    headroom = {r[0]: gamma_headroom(blend, r[7], r[1]) for r in rows if r[7] is not None}
    if headroom:
        print(f"\n(d) γ 여유 — 기준 γ_ref 에서 합법 [{LB5[4]:.2f}, {UB5[4]:.2f}] 까지 "
              f"(γ 격자 {GAMMA_GRID.size} 점 · x 격자 {GRID.size} 점):")
        print(f"    {'state':10}{'γ_ref':>7}{'합법 Δγ':>20}{'(a) mV':>9}"
              f"{'합법 γ 최대변화 mV (γ)':>24}{'(a) 를 내는 가장 가까운 합법 γ':>32}")
        for r in rows:
            h = headroom.get(r[0])
            if h is None:
                continue
            legal = f"[{h['dneg']:+.3f}, {h['dpos']:+.3f}]"
            fam = f"{h['fam_max']:.2f} ({h['g_at_max']:.3f})"
            wit = (f"{h['witness']:.3f} (Δ {h['wdelta']:+.3f})" if h["witness"] is not None
                   else "없음 (격자 기준)")
            print(f"    {r[0]:10}{r[7]:>7.4f}{legal:>20}{r[1]:>9.2f}{fam:>24}{wit:>32}")
        print("    ⚠ 증인은 진폭 크기의 존재이지 모양 일치가 아니다. secant 외삽으로 '필요 Δγ' 를 구하지 않는다.")
    # ⚠ Codex R8-03: 전 판은 `ok`(γ 짝이 있는 행)만으로 **측정** 최대까지 계산했다 — state200 이 100 mV 인데 matrix 가
    #   아직 없으면 요약은 "최대 10 mV" 로 끝나고 rc 0 이었다. 측정 통계는 모든 측정 행에서, γ-짝 통계는 짝 있는 행에서,
    #   그리고 requested/paired/missing 을 산출·stdout·종료 코드로 전파한다.
    paired = [r[0] for r in rows if r[3] == r[3]]
    missing_pairs = [st for st in available if st not in paired]
    # ⚠ Codex R9-06 · P2-5: 완전성 판정은 **게시보다 먼저**다. typed status 하나로 세 상태를 가른다 — complete 만 canonical,
    #   none/partial 은 `<write>/partial/` 에. 전 판은 rc 3 을 내면서도 canonical CSV/meta 를 부분 묶음으로 교체했다
    #   (read_unit True — 부분이 정본 자리를 차지했다).
    if not paired:
        status = "none"
    elif subset:
        status = "subset"                                    # 축소 실행은 완전성 주장을 하지 않는다 (Codex R10 P1-2)
    elif not missing_input and not missing_pairs:
        status = "complete"
    else:
        status = "partial"
    pairing = {"authority": authority, "requested": requested, "requested_from": requested_from, "available": available,
               "missing_input": missing_input, "paired": paired, "missing": missing_pairs,
               # ⚠ 자체 리뷰 C17: 공용 validator 가 거부한 matrix 는 "짝 없음" 인데 **왜** 없는지가 산출에 남아야
               #   한다 (옛 스키마라 거부된 것과 파일이 없는 것은 다른 얘기다).
               "rejected_matrix": rejected,
               "note": "measured_* 는 available(입력 있는 requested) 전부에서, gamma_*·ratio 는 paired 에서만 계산한 값이다; "
                       "missing_input 은 측정조차 없다 (Codex R8-03 · R9-04); rejected_matrix 는 공용 validator 가 "
                       "거부한 상태다 (자체 리뷰 C17)"}
    published = None
    if a.write:
        dest = pathlib.Path(a.write) if status == "complete" else pathlib.Path(a.write) / "partial"   # subset 포함
        art = _write_csv(dest, a, rows, cap, base_cap, {c[0]: c for c in cwhere}, headroom, consumed, pairing,
                         status=status, started=started, argv=list(sys.argv))
        published = art
        print(f"\n→ {art}" + ("" if status == "complete" else
                              f"  [{status} — canonical {pathlib.Path(a.write) / art.name} 은 건드리지 않았다 (Codex R9-06)]"))
    # ⚠ Codex R11 P2-2: wrapper 가 **무엇을 읽어야 하는지** producer 가 말한다. 전 판은 wrapper 가 namespace 를
    #   wildcard 로 훑어 옆에 있던 stale canonical 의 status 를 읽었다. 경로·run_id·status 를 한 줄로 낸다.
    import json as _json
    print("SHAPE_RESULT " + _json.dumps(
        {"status": status, "artifact": str(published) if published else None,
         # ⚠ 자체 리뷰 C29: 전 판은 run_id 를 `<산출>.meta.json` 에서 **읽어서** 보고했고 wrapper 가 같은 파일을
         #   다시 읽어 비교했다 — 항진명제라 그 축은 아무것도 재지 않았다. 이 프로세스가 만든 id 를 낸다.
         "run_id": globals().get("LAST_RUN_ID"),
         "authority": authority, "requested": requested, "paired": paired}, ensure_ascii=False))

    print()
    ok = [r for r in rows if r[3] == r[3]]
    print(f"γ 짝: requested {len(requested)} · 입력 있음 {len(available)}"
          + (f" · **입력 없음(missing_input) {missing_input}**" if missing_input else "")
          + f" · paired {len(paired)}/{len(available)}"
          + (f" · **missing {missing_pairs}** (matrix_<state>.csv 없음/짝 없음 — 미계산이지 '증인 없음' 이 아니다)"
             if missing_pairs else "") + f" · status **{status}**")
    if rows:
        print(f"측정된 음극 모양 변화 최대 {max(r[1] for r in rows):.2f} mV (입력 있는 {len(available)} 개 전부에서),")
    if not ok:
        print("γ 짝을 못 찾았다 — `--out-dir` 에 `ref_gamma_Si` 열이 있는")
        print("matrix_<state>.csv 가 있어야 한다 (v2 이후 산출). status none → 종료 코드 1 (부분이 아니라 없음)")
        return EXIT_BY_STATUS["none"]
    worst = max(ok, key=lambda r: r[3])
    print(f"γ 가 만들어 낸 모델 변화 최대 {max(r[2] for r in ok):.2f} mV (paired {len(paired)} 개에서).")
    # ⚠ 아래는 **크기의 기술**이다. 원인 판정(모델 부적합·잡음·보상)은 출력하지 않는다 —
    #   Codex R3-02: 정확히 표현 가능한 곡선에도 같은 비가 나오므로 비로는 가를 수 없다.
    if worst[3] > 3:
        print(f"\n→ 적합이 고른 γ 쌍이 만든 변화가 측정 변화의 **{worst[3]:.1f} 배** ({worst[0]}).")
        print("  γ 가 측정된 모양 변화 밖의 것을 흡수했을 가능성이 있다 — 무엇인지는 이 비로")
        print("  판정하지 않는다.")
    elif worst[3] < 0.34:
        print(f"\n→ **적합이 고른 γ 쌍**이 만든 변화가 측정 변화의 {worst[3]:.2f} 배다 ({worst[0]}).")
        print("  이 비는 적합이 γ 를 얼마나 움직였나이지, γ 의 표현력이나 측정 음극이 블렌드")
        print("  모양인지의 판정이 아니다 (Codex R2-08 · R3-02: 정확히 표현 가능한 곡선에서도")
        print("  같은 비가 나온다). 표현력은 측정 곡선에 γ 를 직접 제약 적합한 잔차로 재야")
        print("  한다 — 미구현. 원인은 이 스크립트가 판정하지 않는다. (a) 크기를 내는 합법 γ 가")
        print("  있는지는 위 (d) 의 증인 열이 말한다.")
    else:
        print(f"\n→ 두 변화가 같은 규모다 (최대 {worst[3]:.1f} 배). 크기만의 비교다 — 방향과")
        print("  모양이 같은지는 따로 봐야 한다.")
    if flips:
        print(f"\n⚠ **방향 규약이 반대다.** {len(flips)} 개 상태에서 측정 곡선을")
        print("   뒤집어야 블렌드와 가까워진다:")
        for s, f, r in flips:
            print(f"     {s:10} 그대로 {f:7.1f} mV → 뒤집으면 {r:7.1f} mV")
        print("   아래 (c) 는 뒤집은 값이다. 이건 모델의 잘못이 아니라 x 축")
        print("   해석의 문제이므로, 그 자체로는 발견이 아니다.")

    cs = [r[4] for r in rows if r[4] == r[4]]
    if cs:
        rmss = [r[5] for r in rows if r[5] == r[5]]
        print(f"\n(c) **절대 일치** — `Blend(x, γ_적합)` 이 측정 음극과 얼마나 맞나")
        print(f"    max |Δ| {min(cs):.1f} ~ {max(cs):.1f} mV   "
              f"rms {min(rmss):.1f} ~ {max(rmss):.1f} mV")
        print(f"    {'state':10}{'max 위치 x':>11}{'|Δ|>50mV 인 격자 비율':>22}")
        for st, xa, over in cwhere:
            print(f"    {st:10}{xa:>11.3f}{over:>21.1f} %")
        spread = max(cs) / max(rmss) if max(rmss) > 0 else float("inf")
        worst_over = max(o for _, _, o in cwhere) if cwhere else 0.0
        print()
        # ⚠ Codex R4-01: 전 판은 `>30 %` 갈래에서 "블렌드가 이 음극의 모양이 아니다 · γ 를 어떻게 고르든
        #   남고 · a_NE·b_NE 가 흡수한다 = 계통 편향" 을 찍었다 — 정확히 `Blend(x, 0.5)` 인 곡선에 선택 쌍
        #   0.15→0.0 을 주면 같은 갈래에 들고, 같은 실행의 (d) 는 γ=0.5 증인을 찾는다. (c) 는 **선택된 γ 에서의
        #   잔차 기술**까지다. 다른 γ 에서 남는지, 어느 파라미터가 흡수하는지는 이 진단이 정하지 않는다.
        if worst_over > 30:
            print(f"    → 선택된 γ 에서 격자의 {worst_over:.0f} % 가 50 mV 이상 벌어진다 (max {max(cs):.1f} ·")
            print(f"      rms {max(rmss):.1f} mV). 이것은 **그 γ 에서의** 잔차 기술이다 — 다른 γ 에서도 남는지는")
            print("      위 (d) 의 증인 열이, 어느 파라미터로 새는지는 별도 실험이 말한다 (R4-01).")
        elif spread > 3:
            print(f"    → max 가 rms 의 {spread:.1f} 배다. 어긋남이 **좁은 구간에**")
            print("      몰려 있다는 뜻이고, 곡선 대부분은 rms 수준으로 맞는다.")
            print("      'max 가 크다' 만으로 모델을 기각하면 안 된다 — 위 'max 위치'")
            print("      가 어디인지(끝단인지 평탄부인지) 보고 판단할 것.")
        else:
            print("    → 어긋남이 곡선 전체에 고르다. rms 를 대표값으로 쓸 것.")
    print("\n⚠ (a) 는 **정규화 뒤** 변화다. 음극 용량이 줄면(위 '용량 Δ%') 곡선이")
    print("   가로로 늘어나 그것만으로도 모양이 바뀐 것처럼 보인다. 용량 변화가")
    print("   큰 상태에서는 (a) 를 순수한 OCP 모양 변화로 읽으면 안 된다.")
    print("⚠ 이것은 **크기 비교**다. 방향이 같은지는 따로 봐야 한다.")
    if status == "subset":
        print(f"⚠ **부분집합(subset)** — 정본 roster {authority} 중 {requested} 만 돌렸다 (`--states`). 이 산출은 "
              f"완전성 주장을 하지 않는다: canonical 에 가지 않고 종료 코드 {EXIT_BY_STATUS['subset']} 다 (Codex R10 P1-2)")
        return EXIT_BY_STATUS["subset"]
    if status == "partial":
        print("⚠ **부분(partial)** — " + (f"입력 없는 상태 {missing_input}" if missing_input else "")
              + (" · " if missing_input and missing_pairs else "")
              + (f"γ 짝이 없는 상태 {missing_pairs}" if missing_pairs else "")
              + f": 위 γ 통계는 paired {paired} 위의 진술이다 → 종료 코드 3 (canonical 승격 아님)")
        return EXIT_BY_STATUS["partial"]                     # 3 = 부분 (eval --compare 와 같은 뜻)
    return EXIT_BY_STATUS["complete"]


if __name__ == "__main__":
    sys.exit(main())
