"""`artifacts/artifact_index.yaml` 의 **엄격** loader — 한 함수, 모든 reader (75차 G75-N2).

`yaml.safe_load` 는 중복 mapping 키를 조용히 **뒤 값으로 접는다**. 그래서 `runs:` 가 두 번 있거나
같은 실행 이름이 두 번 있거나 한 entry 안에 `payload_index_sha256` 가 두 번 있는 index 를
74차 preflight 가 "형식이 맞다" 고 받았고, 병합 writer 가 접힌 내용을 다시 써서 무관한 항목을
잃었다 (리뷰어 I02·I03·I04). 중복 키는 **불명확한 index** 다 — 어느 값이 정본인지 파일이 말하지
않으므로 사람이 본다. 이 모듈은 그것을 파싱 단계에서 거부하고, index 의 형식 검사(`runs:` mapping 을
담은 mapping, 이름은 str · entry 는 mapping)도 같은 자리에서 한다. `scripts/archive_results.sh` 의
세 reader(진입 preflight · 동명 identity 비교 · 병합 writer)가 전부 이 함수를 쓴다 — 셋이 따로
읽으면 그 사이가 구멍이다.
"""
from __future__ import annotations

import yaml


class DuplicateKeyError(ValueError):
    """같은 mapping 안에 같은 키가 두 번 — index 가 무엇을 말하는지 알 수 없다."""


class IndexShapeError(ValueError):
    """파싱은 됐지만 `runs:` mapping 을 담은 mapping 이 아니다."""


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader + 중복 키 거부. merge key(`<<`)는 SafeLoader 와 같게 flatten 한 뒤 본다."""

    def construct_mapping(self, node, deep=False):  # noqa: D401 — PyYAML hook
        if not isinstance(node, yaml.MappingNode):
            raise yaml.constructor.ConstructorError(
                None, None, f"expected a mapping node, but found {node.id}", node.start_mark)
        self.flatten_mapping(node)
        seen: dict = {}
        for key_node, _value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"found unhashable key ({exc})", key_node.start_mark) from exc
            if key in seen:
                raise DuplicateKeyError(
                    f"중복 mapping 키 {key!r} (line {key_node.start_mark.line + 1}, 먼저 line {seen[key] + 1}) "
                    "— 어느 값이 정본인지 index 가 말하지 않는다 (75차 G75-N2)")
            seen[key] = key_node.start_mark.line
        return super().construct_mapping(node, deep=deep)


def load_index_strict(text: str) -> dict:
    """index 본문을 엄격하게 읽어 `{"runs": {name: entry}, ...}` 를 돌려준다.

    거부 (예외): 중복 키(`DuplicateKeyError`) · YAML 오류(`yaml.YAMLError`) · 형식 밖(`IndexShapeError`:
    최상위가 mapping 이 아니거나 `runs` 가 mapping 이 아니거나 이름이 str 이 아니거나 entry 가 mapping 이
    아님). 빈 파일도 형식 밖이다 — "index 가 있는데 비어 있다" 는 사람이 볼 일이다.
    """
    doc = yaml.load(text, Loader=_StrictLoader)  # noqa: S506 — SafeLoader 파생
    if not isinstance(doc, dict):
        raise IndexShapeError(f"index 최상위가 mapping 이 아니다: {type(doc).__name__}")
    runs = doc.get("runs")
    if not isinstance(runs, dict):
        raise IndexShapeError(f"index 에 `runs:` mapping 이 없다: {type(runs).__name__}")
    for k, v in runs.items():
        if not isinstance(k, str):
            raise IndexShapeError(f"runs 의 이름이 str 이 아니다: {k!r}")
        if not isinstance(v, dict):
            raise IndexShapeError(f"runs[{k!r}] 가 mapping 이 아니다: {type(v).__name__}")
    return doc
