"""halfcell.py — full-range half-cell OCV 기준 곡선 추출.

────────────────────────────────────────────────────────────────────────
왜 필요한가 ★

지금까지 fitting의 reference는 **기준 셀이 실제로 지나간 구간**(4.2/2.5 V,
0.05C)만 담고 있었다. 그러면 두 가지 문제가 생긴다.

  1) α<1인 조건은 재구성 창이 reference 범위를 넘어서 원리적으로 복원 불가
     (33p의 lb=1.00을 풀어줘도 같은 하한이 사실상 존재)
  2) α·β → 리튬량 환산에 셀별 상수(w_PE, w_NE, κ)가 필요해지고,
     22p가 쓴 "provided half-cell OCV" 기준과 달라진다

22p는 별도 측정한 half-cell OCV를 기준으로 fitting했다. 같은 성격의 기준을
쓰려면 **전극 자체 화학량론에 대한 OCP 곡선**이 필요하다.

두 가지 방법을 제공한다.

  method="ocp" (기본, 권장) — 파라미터셋의 OCP 함수를 직접 평가.
      **화학량론 0~1 전 범위**를 얻는다. 복합 음극은 평형 조건으로 Gr·Si를 분배.
  method="sim"              — 넓은 전압창 시뮬레이션에서 추출.
      셀이 실제 지나간 구간만 (PE y 0.251~0.928) → 전 범위가 아니다.

검증: 두 방법을 겹치는 구간에서 비교하면
    PE 평균차 1.7 mV (최대 4.7)
    NE 평균차 3.8 mV (z 0.02~0.98 구간; 끝단은 흑연 OCP 발산으로 큼)
→ OCP 함수 평가가 시뮬레이션 결과를 정확히 재현한다.

★ 이 기준으로 fitting하면 α·β가 논문 규약의 의미를 정확히 갖는다.
  기준 조건 자체를 fitting한 결과가 그 증거다:
      α_PE,ini = 1.465  →  셀이 PE 전 범위의 1/1.465 = 68.3% 사용
                           (시뮬레이션 관측 0.251~0.928 = 67.7%와 일치)
      β_PE,ini = -0.395 →  x=0에서 y = 0.395/1.465 = 0.270
                           (baseline 17038/63104 = 0.270과 일치)
      α_NE,ini = 1.029  →  NE는 전 범위의 97% 사용 (관측과 일치)
────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.config import baseline_hash

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class HalfCellReference:
    """전극 화학량론 대비 OCP 테이블 (오름차순 정렬)."""

    y_pe: np.ndarray        # 양극 화학량론 (리튬 분율)
    u_pe: np.ndarray        # 양극 OCP [V]
    z_ne: np.ndarray        # 음극 화학량론 (Gr+Si 가중 평균)
    u_ne: np.ndarray        # 음극 bulk OCP [V]

    def as_dict(self) -> dict:
        return {"y_pe": self.y_pe.tolist(), "u_pe": self.u_pe.tolist(),
                "z_ne": self.z_ne.tolist(), "u_ne": self.u_ne.tolist()}

    @classmethod
    def from_dict(cls, d: dict) -> "HalfCellReference":
        return cls(*(np.asarray(d[k], float) for k in ("y_pe", "u_pe", "z_ne", "u_ne")))

    def coverage(self) -> dict:
        return {"pe_min": float(self.y_pe.min()), "pe_max": float(self.y_pe.max()),
                "ne_min": float(self.z_ne.min()), "ne_max": float(self.z_ne.max())}


def _eval_ocp(fn, xs: np.ndarray) -> np.ndarray:
    """pybamm OCP 함수를 점별 평가. (흑연 OCP는 심볼 연산이라 배열 입력 불가)"""
    import pybamm

    out = []
    for xi in xs:
        r = fn(pybamm.Scalar(float(xi)))
        r = r.evaluate() if hasattr(r, "evaluate") else r
        out.append(float(np.asarray(r).ravel()[0]))
    return np.asarray(out)


def compute_halfcell_from_ocp(cfg: dict, n_points: int = 400,
                              branch: str = "delithiation",
                              pe_offset_mv: float = 0.0,
                              ne_offset_mv: float = 0.0,
                              pe_stretch: float = 1.0,
                              ne_stretch: float = 1.0) -> HalfCellReference:
    """★ 진짜 full-range half-cell OCV — 파라미터셋의 OCP 함수를 직접 평가한다.

    시뮬레이션 추출본은 셀이 실제로 지나간 구간(PE y 0.251~0.928)만 담지만,
    OCP 함수는 화학량론 0~1 전 범위를 준다. 22p가 쓴 "provided half-cell OCV"와
    같은 성격이며, 이래야 α·β가 논문 규약의 의미를 정확히 갖는다.

    복합 음극(Gr+Si)은 **평형 조건**으로 푼다:
      같은 전위 U에서 U_gr(x_gr) = U_si(x_si) = U 이므로 각 OCP를 역보간해
      x_gr(U), x_si(U)를 얻고, 용량 가중 평균으로 z(U)를 만든다.
        z = (Q_gr·x_gr + Q_si·x_si)/(Q_gr + Q_si),  Q = c_max·vf
      (이 baseline에서 Gr 83.5%, Si 16.5%)

    branch: Si는 히스테리시스가 있어 가지를 골라야 한다. grid 곡선이 최종 방전
            스텝에서 추출되므로 기본값은 "delithiation"(방전 중 음극은 탈리튬화).

    ★ 왜곡 인자 (`method="ocpbias"` 전용 — 모델 오차 민감도 시험)
      `*_offset_mv`  OCP 전압에 더하는 계통 오프셋 (mV). 기준전극 보정 오차·
                     로트 차이에 해당한다.
      `*_stretch`    화학량론 축 배율. 우리 모델이 전극의 사용 구간을 실제와
                     다르게 알고 있는 경우다 (실측에서 가장 큰 오차원).

      **truth 는 건드리지 않는다** — 왜곡은 fitting 이 쓰는 기준 곡선에만
      들어간다. 그래야 "우리 모델이 틀렸을 때 결론이 얼마나 버티는가" 를
      묻는 것이 된다. 기본값(0·1.0)이면 왜곡 없는 `ocp` 와 배열이 같다.
    """
    import pybamm

    b = cfg["baseline"]
    p = pybamm.ParameterValues(cfg["parameter_set"])
    x = np.linspace(1e-4, 1 - 1e-4, n_points)

    # ── 양극: 화학량론 그대로 ──
    u_pe = _eval_ocp(p["Positive electrode OCP [V]"], x)

    # ── 음극: Gr·Si 평형 분배 ──
    si_key = {"delithiation": "Secondary: Negative electrode delithiation OCP [V]",
              "lithiation": "Secondary: Negative electrode lithiation OCP [V]",
              "mean": "Secondary: Negative electrode OCP [V]"}[branch]
    u_gr = _eval_ocp(p["Primary: Negative electrode OCP [V]"], x)
    u_si = _eval_ocp(p[si_key], x)

    q_gr = b["ne_primary_max_conc"] * b["ne_primary_vf"]
    q_si = b["ne_secondary_max_conc"] * b["ne_secondary_vf"]

    u_grid = np.linspace(min(u_gr.min(), u_si.min()), max(u_gr.max(), u_si.max()),
                         n_points * 2)
    # OCP는 단조감소 → 역보간 위해 뒤집는다. 범위 밖은 포화(0 또는 1).
    x_gr = np.interp(u_grid, u_gr[::-1], x[::-1], left=1.0, right=0.0)
    x_si = np.interp(u_grid, u_si[::-1], x[::-1], left=1.0, right=0.0)
    z = (q_gr * x_gr + q_si * x_si) / (q_gr + q_si)

    # ── 계통 왜곡 (ocpbias) — 기준 곡선에만, truth 에는 없다 ──
    if pe_offset_mv:
        u_pe = u_pe + pe_offset_mv / 1000.0
    if ne_offset_mv:
        u_grid = u_grid + ne_offset_mv / 1000.0
    if pe_stretch != 1.0:
        x = np.clip(x * float(pe_stretch), 0.0, 1.0)
    if ne_stretch != 1.0:
        z = np.clip(z * float(ne_stretch), 0.0, 1.0)

    y_s, u_p = _dedupe_sorted(x, u_pe)
    z_s, u_n = _dedupe_sorted(z, u_grid)
    ref = HalfCellReference(y_pe=y_s, u_pe=u_p, z_ne=z_s, u_ne=u_n)
    log.info("half-cell(OCP 함수) 기준: PE y %.4f~%.4f, NE z %.4f~%.4f (Si 가지=%s)",
             y_s.min(), y_s.max(), z_s.min(), z_s.max(), branch)
    return ref


def _dedupe_sorted(x: np.ndarray, y: np.ndarray) -> tuple:
    """화학량론 오름차순 + 중복 제거 (보간자를 만들 수 있게)."""
    order = np.argsort(x)
    x, y = x[order], y[order]
    keep = np.concatenate([[True], np.diff(x) > 1e-9])
    return x[keep], y[keep]


def compute_halfcell_reference(cfg: dict, v_lo: float = 2.0, v_hi: float = 4.4,
                               c_rate: float = 0.02) -> HalfCellReference:
    """넓은 전압창 저율 사이클 1회로 half-cell OCV 테이블을 만든다."""
    import pybamm

    from src.model import build_model
    from src.runner import build_param, make_solver

    b = cfg["baseline"]
    model = build_model(cfg)
    param = build_param(cfg, {"Upper voltage cut-off [V]": v_hi,
                              "Lower voltage cut-off [V]": v_lo})
    # ★ 충전 먼저 → 마지막 **방전 스텝만** 쓴다.
    #   NE가 composite(current sigmoid 히스테리시스)라 충전·방전 가지의 OCP가 다르다.
    #   두 가지를 한 테이블에 섞으면 같은 화학량론에 값이 두 개가 되어
    #   기준 곡선이 망가진다 (실측: β_NE가 bound까지 달아나고 LAM 오차 0.10).
    #   grid 곡선도 최종 방전 스텝에서 추출하므로 가지를 맞춘다.
    exp = pybamm.Experiment([
        f"Charge at {c_rate}C until {v_hi}V",
        "Rest for 30 minutes",
        f"Discharge at {c_rate}C until {v_lo}V",
    ])
    sol = pybamm.Simulation(model, parameter_values=param, experiment=exp,
                            solver=make_solver(cfg)).solve()

    ys, us_pe, zs, us_ne = [], [], [], []
    for step in sol.cycles[-1].steps[-1:]:      # 최종 방전 스텝만
        c_pe = step["Average positive particle concentration [mol.m-3]"].entries
        c_gr = step["Average negative primary particle concentration [mol.m-3]"].entries
        c_si = step["Average negative secondary particle concentration [mol.m-3]"].entries
        ys.append(c_pe / b["pe_max_conc"])
        us_pe.append(step["X-averaged positive electrode open-circuit potential [V]"].entries)
        # NE는 2상 복합 — 용량 가중 평균 화학량론
        num = c_gr * b["ne_primary_vf"] + c_si * b["ne_secondary_vf"]
        den = (b["ne_primary_max_conc"] * b["ne_primary_vf"]
               + b["ne_secondary_max_conc"] * b["ne_secondary_vf"])
        zs.append(num / den)
        us_ne.append(step["Battery negative electrode bulk open-circuit potential [V]"].entries)

    y, u_p = _dedupe_sorted(np.concatenate(ys), np.concatenate(us_pe))
    z, u_n = _dedupe_sorted(np.concatenate(zs), np.concatenate(us_ne))
    ref = HalfCellReference(y_pe=y, u_pe=u_p, z_ne=z, u_ne=u_n)
    log.info("half-cell 기준 확보: PE y %.3f~%.3f (%d점), NE z %.3f~%.3f (%d점)",
             y.min(), y.max(), len(y), z.min(), z.max(), len(z))
    return ref


#: ★ F64 — **결과를 바꾸는** 생성 인자. 캐시 키와 meta 에 모두 들어가야 한다.
#:   기본값은 `compute_halfcell_from_ocp` / `compute_halfcell_reference` 시그니처와
#:   일치해야 하며, 여기 없는 인자를 추가하면 그 인자는 서명에서 빠진다.
RECIPE_DEFAULTS = {
    "ocp": {"n_points": 400, "branch": "delithiation"},
    # ★ 모델 오차 민감도용 — `ocp` 를 **건드리지 않는다**. 왜곡 인자를 `ocp`
    #   recipe 에 끼우면 recipe_hash 가 바뀌어 기존 half-cell 묶음(v4)의
    #   F74 검증이 통째로 깨진다. 별도 method 라 기존 identity 는 그대로다.
    #   이름에 밑줄·숫자를 쓰지 않는다 — hessian 의 봉인 staging 정규식이
    #   `<16hex>_<method>_<12hex>` 에서 method 를 `[a-z]+` 로 본다.
    "ocpbias": {"n_points": 400, "branch": "delithiation",
                "pe_offset_mv": 0.0, "ne_offset_mv": 0.0,
                "pe_stretch": 1.0, "ne_stretch": 1.0},
    "sim": {"v_lo": 2.0, "v_hi": 4.4, "c_rate": 0.02},
}


def recipe_of(method: str = "ocp", **kw) -> dict:
    """생성 인자를 기본값과 합쳐 **완전한** recipe 로 만든다."""
    if method not in RECIPE_DEFAULTS:
        raise ValueError(f"알 수 없는 method: {method} (가능: {list(RECIPE_DEFAULTS)})")
    r = dict(RECIPE_DEFAULTS[method])
    unknown = set(kw) - set(r)
    if unknown:
        # 조용히 무시하면 "서명에 없는데 결과는 바뀌는" 인자가 생긴다
        raise ValueError(f"method={method}가 모르는 인자: {sorted(unknown)}")
    r.update({k: v for k, v in kw.items() if v is not None})
    return {"method": method, **r}


def recipe_hash(cfg: dict, method: str = "ocp", **kw) -> str:
    """baseline + recipe 를 함께 해시한다 (★ F64)."""
    import hashlib

    payload = {"baseline": baseline_hash(cfg), "recipe": recipe_of(method, **kw)}
    return hashlib.sha1(
        json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:12]


def halfcell_cache_path(cfg: dict, cache_dir: str | Path | None = None,
                        method: str = "ocp", **kw) -> Path:
    """★ F45 — 실제로 쓰이는 캐시 경로. 서명·manifest가 이걸 그대로 써야 한다.

    한때 fitting이 현재 작업 디렉터리의 `.cache/halfcell/*_ocp.json` 을 glob 했다.
    실제 경로는 base config의 `_config_path` 에서 저장소 root 를 계산해 고른
    **하나**이므로, 다른 작업 디렉터리나 외부 --base-config 를 쓰면 실제 사용
    캐시가 서명에서 빠지고, 반대로 무관한 캐시까지 서명에 들어가 resume 을
    불필요하게 막았다.

    ★ F64 — 키에 **recipe 해시**를 넣는다. 예전 키는 `baseline_hash + method`
    뿐이라 `branch`(Si 히스테리시스 가지)나 `n_points` 가 달라도 같은 경로였다.
    그래서 다른 recipe 로 만든 곡선을 같은 경로에 미리 넣어두면 fitting 이 그걸
    쓰고도 검증을 통과했다 — 실측으로 `p_ini[pocv]` 가
    `[1.343, -0.325, 2.429, -0.100]` → `[1.628, -0.404, 1.500, -0.410]` 로 움직였다.
    좌표 원점이 바뀌므로 Case 1 의 모든 수치가 따라 바뀐다.
    """
    root = Path(cfg.get("_config_path", ".")).resolve().parent.parent
    d = Path(cache_dir) if cache_dir else root / ".cache" / "halfcell"
    return d / f"{baseline_hash(cfg)}_{method}_{recipe_hash(cfg, method, **kw)}.json"


def halfcell_meta_path(path: str | Path) -> Path:
    """캐시 JSON 옆의 recipe 기록 파일. 캐시와 함께 봉인된다."""
    p = Path(path)
    return p.with_name(p.stem + ".meta.yaml")


def get_halfcell_reference(cfg: dict, cache_dir: str | Path | None = None,
                           force: bool = False, method: str = "ocp",
                           **kw) -> HalfCellReference:
    """baseline+recipe 해시 키 캐시 → 미스 시 계산 (완방상태와 같은 정책).

    method: "ocp" (기본) — 파라미터셋 OCP 함수 직접 평가, 화학량론 전 범위
            "sim"        — 넓은 전압창 시뮬레이션 추출 (셀이 지나간 구간만)

    ★ F64 — 생성 시 `*.meta.yaml` 에 recipe·생성 코드·환경을 같이 남긴다.
      배열 네 개만 저장하면 "이 숫자가 어떤 recipe 에서 나왔는가"를 파일만
      보고 알 수 없고, 그러면 캐시를 바꿔치기해도 아무도 모른다.
    """
    import yaml

    from src.io import env_fingerprint, source_digest

    path = halfcell_cache_path(cfg, cache_dir, method, **kw)
    recipe = recipe_of(method, **kw)

    # ★ F74 — meta 없는 캐시 적중은 **적중이 아니다** (8차 리뷰 발견 2 부수).
    #   F64 이전에 만들어진 JSON 만 있으면, 안내대로 `python -m src.halfcell` 을
    #   돌려도 hit 로 즉시 반환해 meta 가 영영 생기지 않았다. miss 로 취급해
    #   캐시·meta 를 함께 다시 만든다.
    # ★ 12차 발견 4 — 존재만 보고 반환하면, 다른 runtime·다른 코드로 만든 옛
    #   캐시가 그대로 Case 1 의 좌표 원점이 된다. 완방상태와 같은 정책으로
    #   결정 축(runtime·코드 identity)이 다르면 **미스로 취급해 재계산**한다.
    if not force and path.exists() and halfcell_meta_path(path).exists():
        _meta = yaml.safe_load(
            halfcell_meta_path(path).read_text(encoding="utf-8")) or {}
        from src.baseline import _ENV_KEYS
        _now = {k: env_fingerprint().get(k) for k in _ENV_KEYS}
        _old = {k: (_meta.get("env") or {}).get(k) for k in _ENV_KEYS}
        if _old != _now:
            log.warning("half-cell 캐시가 다른 runtime 에서 계산됨 (차이 %s) — "
                        "미스로 취급해 재계산: %s",
                        [k for k in _ENV_KEYS if _old.get(k) != _now.get(k)], path)
        elif _meta.get("source_digest") != source_digest():
            log.warning("half-cell 캐시가 다른 코드로 계산됨 (%s ≠ %s) — 미스로 "
                        "취급해 재계산: %s", _meta.get("source_digest"),
                        source_digest(), path)
        else:
            log.info("half-cell 기준 캐시 적중: %s", path)
            return HalfCellReference.from_dict(
                json.loads(path.read_text(encoding="utf-8")))

    ref = (compute_halfcell_from_ocp(cfg, **kw) if method in ("ocp", "ocpbias")
           else compute_halfcell_reference(cfg, **kw))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ref.as_dict()), encoding="utf-8")
    halfcell_meta_path(path).write_text(yaml.safe_dump({
        "recipe": recipe,
        "baseline_hash": baseline_hash(cfg),
        "recipe_hash": recipe_hash(cfg, method, **kw),
        "parameter_set": cfg.get("parameter_set"),
        "source_digest": source_digest(),
        "env": env_fingerprint(),
        "coverage": ref.coverage(),
        "cache_file": path.name,
    }, allow_unicode=True, sort_keys=False), encoding="utf-8")
    log.info("half-cell 기준 캐시 저장: %s (recipe %s)", path, recipe)
    return ref


def validate_halfcell_cache(cfg: dict, cache_path: str | Path,
                            meta_doc: dict | None = None,
                            arrays_doc: dict | None = None) -> dict:
    """★ F74 — half-cell 캐시가 **선언된 recipe 로 만들어졌는지** 검증한다.

    8차 리뷰 반례: 정식 경로에 임의 선형 JSON + `baseline_hash: FORGED,
    recipe_hash: FORGED` meta 를 넣어도 fitting 은 meta 에 `recipe` 키가 있는지만
    보고 통과했다 (`META_SOURCE=FORGED_SOURCE, VALIDATOR_OK=True`).

    여기서는 meta 의 선언을 **전부 다시 계산해** 대조한다:
      · baseline_hash == baseline_hash(cfg) 재계산
      · recipe_hash   == recipe_hash(cfg, **recipe) 재계산
      · cache_file    == 실제 파일명
      · 배열: 네 키 존재 · 쌍 길이 일치 · 전부 유한 · 오름차순 · 전 범위 coverage

    한계를 명시한다 — 해시를 올바르게 재계산해 넣고 배열만 바꾼 위조는 구조
    검사로 못 잡는다. 그건 `python -m src.halfcell --verify` (재생성 대조) 가
    잡으며, smoke 가 실제 pybamm 으로 그 경로를 돈다.

    meta_doc/arrays_doc 을 주면 그 문서(스냅샷 바이트)를 검증한다 — 디스크를
    다시 읽으면 봉인과 검증 사이가 또 벌어진다 (F72).
    """
    import numpy as np
    import yaml

    from src.io import source_digest

    cache_path = Path(cache_path)
    checks: dict[str, tuple[bool, str]] = {}
    meta = meta_doc if meta_doc is not None else (
        yaml.safe_load(halfcell_meta_path(cache_path).read_text(encoding="utf-8"))
        if halfcell_meta_path(cache_path).exists() else None)

    checks["meta_존재"] = (bool(meta), "recipe meta(.meta.yaml)가 없다")
    if meta:
        recipe = dict(meta.get("recipe") or {})
        method = recipe.pop("method", None)
        checks["recipe_존재"] = (bool(method), "meta에 recipe/method가 없다")
        if method:
            try:
                want_r = recipe_hash(cfg, method, **recipe)
                want_b = baseline_hash(cfg)
            except Exception as e:  # noqa: BLE001
                checks["해시_재계산"] = (False, f"recipe가 재계산 불가: {e}")
            else:
                checks["baseline_hash_재계산"] = (
                    meta.get("baseline_hash") == want_b,
                    f"meta {meta.get('baseline_hash')} ≠ 재계산 {want_b}")
                checks["recipe_hash_재계산"] = (
                    meta.get("recipe_hash") == want_r,
                    f"meta {meta.get('recipe_hash')} ≠ 재계산 {want_r}")
                checks["경로_recipe_일치"] = (
                    cache_path.name == f"{want_b}_{method}_{want_r}.json",
                    f"캐시 파일명 {cache_path.name}이 재계산 해시와 다르다")
        checks["cache_file_일치"] = (
            meta.get("cache_file") == cache_path.name,
            f"meta.cache_file {meta.get('cache_file')} ≠ {cache_path.name}")
        # ★ 10차 자체 리뷰 — 캐시 키(baseline+recipe)에 **코드**가 없다.
        #   OCP 함수·해석 코드가 바뀐 뒤 옛 캐시를 재사용하면 Case 1 의 좌표
        #   원점이 현재 코드가 만들 값과 조용히 달라진다. 생성 시점의
        #   source_digest 를 대조하고, 다르면 재생성만이 답이다 (수 초).
        checks["코드_identity"] = (
            meta.get("source_digest") == source_digest(),
            f"meta {meta.get('source_digest')} ≠ 현재 {source_digest()} — "
            f"캐시 생성 후 코드가 바뀌었다. "
            f"python -m src.halfcell --config <base> --method <m> --force 로 재생성 (10차)")
        # ★ 12차 발견 4 — 생성 runtime 을 **기록만** 하고 대조하지 않았다.
        #   OCP 평가·보간은 NumPy/SciPy/PyBaMM 에 의존하므로, 다른 runtime 의
        #   캐시가 hit 되면 Case 1 의 좌표 원점이 현재 환경이 만들 값과 달라진다.
        from src.baseline import _ENV_KEYS
        from src.io import env_fingerprint
        _now = {k: env_fingerprint().get(k) for k in _ENV_KEYS}
        _old = {k: (meta.get("env") or {}).get(k) for k in _ENV_KEYS}
        checks["runtime_identity"] = (
            _old == _now,
            f"meta 의 생성 runtime 이 현재와 다르다 (차이: "
            f"{[k for k in _ENV_KEYS if _old.get(k) != _now.get(k)]}) — "
            f"--force --verify 로 재생성 (12차 발견 4)")

    doc = arrays_doc
    if doc is None and cache_path.exists():
        doc = json.loads(cache_path.read_text(encoding="utf-8"))
    if not doc:
        checks["배열_존재"] = (False, "캐시 JSON을 읽지 못했다")
    else:
        keys = ("y_pe", "u_pe", "z_ne", "u_ne")
        missing = [k for k in keys if k not in doc]
        checks["배열_스키마"] = (not missing, f"키 누락: {missing}")
        if not missing:
            a = {k: np.asarray(doc[k], float) for k in keys}
            checks["배열_길이"] = (
                len(a["y_pe"]) == len(a["u_pe"]) and len(a["z_ne"]) == len(a["u_ne"])
                and len(a["y_pe"]) > 10,
                "쌍 길이 불일치 또는 점이 너무 적다")
            checks["배열_유한"] = (
                all(np.isfinite(a[k]).all() for k in keys), "비유한 값이 있다")
            checks["배열_정렬"] = (
                bool(np.all(np.diff(a["y_pe"]) > 0) and np.all(np.diff(a["z_ne"]) > 0)),
                "화학량론 축이 오름차순이 아니다")
            checks["전범위_coverage"] = (
                a["y_pe"].min() <= 0.01 and a["y_pe"].max() >= 0.99
                and a["z_ne"].min() <= 0.01 and a["z_ne"].max() >= 0.99,
                f"전 범위가 아니다 (PE {a['y_pe'].min():.3f}~{a['y_pe'].max():.3f})")

    fail = [k for k, (ok, _) in checks.items() if not ok]
    return {"ok": not fail,
            "checks": {k: "통과" if ok else f"실패 — {why}"
                       for k, (ok, why) in checks.items()},
            "fail": fail, "reasons": [checks[k][1] for k in fail]}


def main() -> None:
    import argparse

    from src.config import load_config, validate_config

    ap = argparse.ArgumentParser(description="full-range half-cell OCV 기준 추출")
    ap.add_argument("--config", default="configs/base.yaml")
    ap.add_argument("--v-lo", type=float, default=2.0)
    ap.add_argument("--v-hi", type=float, default=4.4)
    ap.add_argument("--c-rate", type=float, default=0.02)
    ap.add_argument("--method", default="ocp", choices=["ocp", "sim"],
                    help="ocp=OCP 함수 직접 평가(전 범위) | sim=시뮬레이션 추출")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--verify", action="store_true",
                    help="캐시를 recipe로 **다시 계산해** 배열까지 대조한다 (F74). "
                         "구조·해시 검사가 못 잡는 배열 위조를 잡는 유일한 방법")
    ap.add_argument("--plot", default=None, help="곡선 그림 저장 경로")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = load_config(args.config)
    validate_config(cfg)
    kw = ({} if args.method == "ocp"
          else {"v_lo": args.v_lo, "v_hi": args.v_hi, "c_rate": args.c_rate})
    ref = get_halfcell_reference(cfg, force=args.force, method=args.method, **kw)
    print(json.dumps(ref.coverage(), indent=2))

    if args.verify:
        import numpy as np
        path = halfcell_cache_path(cfg, method=args.method, **kw)
        v = validate_halfcell_cache(cfg, path)
        fresh = (compute_halfcell_from_ocp(cfg, **kw) if args.method == "ocp"
                 else compute_halfcell_reference(cfg, **kw))
        # ★ 10차 — rtol 을 0 으로 **고정**한다. 기본 rtol=1e-5 는 4V 전압에서
        #   ~40µV 의 슬랙이라 미세 변조가 통과한다. 같은 recipe 재생성은
        #   결정론적이므로 절대오차 1e-9 만 허용하면 된다. 길이가 다르면
        #   allclose 가 broadcast 예외로 죽으므로 shape 부터 본다.
        same = all(
            np.shape(getattr(ref, k)) == np.shape(getattr(fresh, k))
            and np.allclose(getattr(ref, k), getattr(fresh, k),
                            rtol=0.0, atol=1e-9)
            for k in ("y_pe", "u_pe", "z_ne", "u_ne"))
        print(json.dumps({"구조검사": v["ok"], "구조검사_실패": v["fail"],
                          "재생성_배열일치": bool(same)}, ensure_ascii=False, indent=2))
        if not (v["ok"] and same):
            # ★ 11차 발견 4 — 캐시 hit 은 옛 배열을 그대로 돌려주고 `--verify` 는
            #   갱신하지 않는다. 코드가 바뀐 뒤 배열이 실제로 같아도
            #   `코드_identity` 로 실패하므로, 운영 명령은 `--force --verify` 다.
            hint = ("\n  캐시를 다시 만들고 검증하세요: "
                    f"python -m src.halfcell --config {args.config} "
                    f"--method {args.method} --force --verify"
                    if (not args.force and v["fail"] == ["코드_identity"] and same)
                    else "")
            raise SystemExit(
                f"--verify 실패: 캐시가 recipe 재생성 결과와 다르다 (F74){hint}")

    if args.plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 2, figsize=(11, 4), constrained_layout=True)
        ax[0].plot(ref.y_pe, ref.u_pe, "b-"); ax[0].set_title("PE half-cell OCV")
        ax[0].set_xlabel("PE stoichiometry y"); ax[0].set_ylabel("U [V]")
        ax[1].plot(ref.z_ne, ref.u_ne, "r-"); ax[1].set_title("NE half-cell OCV")
        ax[1].set_xlabel("NE stoichiometry z"); ax[1].set_ylabel("U [V]")
        for a in ax:
            a.grid(alpha=0.3)
        out = Path(args.plot); out.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out, dpi=150)
        print(f"그림 저장: {out}")


if __name__ == "__main__":
    main()
