"""config.py — yaml 로드 + `extends` 병합 + 스키마 검증 + config 해시.

docs/03_ARCHITECTURE.md 1절. 모든 실행 경로는 이 모듈을 통해 config를 읽는다.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "configs"

# base.yaml에서 반드시 존재해야 하는 키 (누락 시 명확한 에러)
_REQUIRED_PATHS = [
    ("model", "particle_phases"),
    ("parameter_set",),
    ("cell", "upper_voltage_cutoff"),
    ("cell", "lower_voltage_cutoff"),
    ("baseline", "ne_primary_init_conc"),
    ("baseline", "ne_primary_max_conc"),
    ("baseline", "ne_secondary_init_conc"),
    ("baseline", "ne_secondary_max_conc"),
    ("baseline", "pe_init_conc"),
    ("baseline", "pe_max_conc"),
    ("baseline", "ne_porosity"),
    ("baseline", "ne_primary_vf"),
    ("baseline", "ne_secondary_vf"),
    ("baseline", "pe_porosity"),
    ("baseline", "pe_vf"),
    ("discharged_state", "auto_regenerate"),
    ("protocol", "discharge_first"),
    ("protocol", "charge_first"),
    ("mode_protocol",),
    ("solver", "type"),
    ("postprocess", "n_trim"),
    ("postprocess", "n_interp"),
]


class ConfigError(RuntimeError):
    """config 로드/검증 실패."""


def _deep_merge(base: dict, override: dict) -> dict:
    """override가 base 위에 재귀적으로 덮어쓴 새 dict를 반환."""
    out = copy.deepcopy(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def load_config(path: str | Path) -> dict:
    """yaml 로드. `extends: <file>` 가 있으면 그 파일을 먼저 로드해 병합한다."""
    path = Path(path)
    if not path.exists():
        # configs/ 상대 경로 허용
        alt = CONFIG_DIR / path.name
        if alt.exists():
            path = alt
        else:
            raise ConfigError(f"config 파일 없음: {path}")

    with open(path, encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    parent_name = raw.pop("extends", None)
    if parent_name:
        parent = load_config(path.parent / parent_name)
        cfg = _deep_merge(parent, raw)
        # ★ F74 — `extends` 로 재귀 로드된 **부모 파일도 입력이다.** 봉인 목록이
        #   최종 경로 하나만 알면, 부모(base.yaml)를 바꿔도 digest 가 그대로라
        #   실행 결과가 바뀌었는데 검증이 통과한다 (8차 리뷰 발견 3 반례:
        #   PARENT_SEALED=False, AFTER_PARENT_CHANGE_OK=True).
        chain = list(parent.get("_loaded_files") or []) + [str(path)]
    else:
        cfg = raw
        chain = [str(path)]

    cfg["_config_path"] = str(path)
    cfg["_loaded_files"] = chain
    return cfg


def config_dependencies(path: str | Path) -> list[Path]:
    """★ F74 — 이 config 를 로드할 때 실제로 읽히는 파일 전부 (extends 연쇄 포함)."""
    return [Path(p) for p in load_config(path).get("_loaded_files", [str(path)])]


def validate_config(cfg: dict) -> None:
    """필수 키 검증. 누락 시 어떤 키가 없는지 명시하는 에러를 던진다."""
    missing = []
    for key_path in _REQUIRED_PATHS:
        node: Any = cfg
        for k in key_path:
            if not isinstance(node, dict) or k not in node:
                missing.append(".".join(key_path))
                break
            node = node[k]
    if missing:
        raise ConfigError(
            f"config 필수 키 누락: {missing} (파일: {cfg.get('_config_path', '?')})"
        )


def merge_config_docs(docs: list[dict]) -> dict:
    """★ F74/F72 — 이미 읽은 문서들(스냅샷 바이트)로 `extends` 병합을 재현한다.

    `load_config` 는 디스크에서 부모를 다시 읽는다. 스냅샷 이후에 그걸 부르면
    봉인과 읽기 사이가 또 벌어진다. 병합 결과는 파일 **내용**에만 의존하므로,
    스냅샷 문서를 부모→자식 순서로 넘기면 같은 config 가 나온다.
    """
    out: dict = {}
    for d in docs:
        d = dict(d or {})
        d.pop("extends", None)
        out = _deep_merge(out, d)
    return out


def config_hash(cfg: dict) -> str:
    """config 내용의 안정적 해시 (경로 등 메타 키 제외). manifest/캐시 키로 사용."""
    clean = {k: v for k, v in cfg.items() if not k.startswith("_")}
    blob = json.dumps(clean, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]


def baseline_hash(cfg: dict) -> str:
    """완방상태 캐시 무효화 키 — 물리 baseline에 영향을 주는 부분만 해시."""
    relevant = {
        "model": cfg.get("model"),
        "parameter_set": cfg.get("parameter_set"),
        "cell": cfg.get("cell"),
        "baseline": cfg.get("baseline"),
        "discharged_protocol": cfg.get("discharged_state", {}).get("protocol"),
    }
    blob = json.dumps(relevant, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]
