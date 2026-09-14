#!/usr/bin/env python3
"""U14/U18 재실행 점검 — 새 산출이 (a) producer 스키마를 **내용까지** 담고 (b) 정본과 같은 명부·같은 실행 조건이며
(c) **같은 숫자**인가.

R6 내부 리뷰가 게시·서명 경로를 고쳤다 (`reviews/R6_LEDGER.md`). 계산 경로는 안 건드렸으므로 재실행의 숫자는
정본과 **비트 단위로 같아야 한다**. 다르면 그것이 발견이다 — 먼저 볼 축은 F3(라이브러리 버전)이고, 새 meta 의
`env` 가 그때 처음 근거를 준다. 그래서 재실행은 `OUT=out_u14` 처럼 **다른 디렉터리로** 받고 이 스크립트로 댄 뒤에만
정본을 교체한다 (정본을 먼저 덮으면 비교 대상이 사라진다).

    python3 scripts/check_u14.py --new out_u14            # 정본 out/ 과 대조
    python3 scripts/check_u14.py --new out_u14 --old out --schema-only   # 스키마만 (구조 검사는 전부 한다)
    python3 scripts/check_u14.py --new out_part --subset  # 명시적 부분 재실행 — 범위(k/N)를 찍고, 승격 근거가 아니다

⚠ Codex R9-02: 전 판은 **new 에 있는 파일만** 순회했다 — 정본 12 개 중 1 개만 재실행해도 "산출 1 개 · 전부 같다 · rc 0".
  명부(roster)는 정본과 새 산출의 canonical 이름 **합집합**이고, 정본에 있는데 새 산출에 없는 것은 실패다. 부분
  재실행은 `--subset` 으로 계약을 명시해야 하고, 그때도 범위(k/N)를 찍으며 승격 대상이 아니다.
⚠ Codex R9-03: 전 판은 열 **이름**만 봤다 — 과학 열(`LLI_pct`)이 사라져도, 출처 열 값이 전부 비어도, 실행 조건(n_starts·
  seed·n_grid·n_samples·tol)이 바뀌어도 "전부 갖췄다 · 게시·서명만 바뀌었다". 스키마의 정본은 `bms_balancing/schema.py`
  하나이고 (producer 가 같은 것을 assert 한다) 검사는 필수 셀 nonempty · 숫자 파싱 · receipt(역할·path·64-hex·재계산
  digest) · 중복 key · 실행 조건 대조까지다 — `--schema-only` 도 구조 검사는 전부 한다.

종료 코드: 0 = 명부·스키마·조건·환경 갖췄고 숫자 동일이며 **승격 가능** · 1 = 숫자가 다름 · 2 = 명부/스키마/내용/조건/환경
불일치 · 묶음 미완 · 파일 없음 · candidate 와 baseline 이 같은 디렉터리 · 3 = 명시한 부분 재실행(`--subset`)이 정본 명부를
덜 덮었다 · **4 = 승격 대조를 물었는데 답을 낼 수 없다**
(입력 identity 를 댈 수 없다 — 자체 리뷰 C11: 전 판은 이것도 0 이었고 U18 런북이 "0 이었을 때만 정본 교체" 라
승격 불가 상태에서 정본을 바꿨다). `--schema-only` 는 승격을 묻지 않은 진단이므로 스키마가 깨끗하면 0 이고,
승격 자격이 없다는 것은 `PROMOTION` 의 `promotion_eligible`·`baseline_absent` 가 말한다.
마지막 줄 `PROMOTION {…}` 이 같은 판정을 machine-readable 로 낸다 (`promotion_eligible` 은 rc 0 에서만 true).
"""
from __future__ import annotations
import argparse, csv, io, json, os, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from bms_balancing import schema as S          # noqa: E402  — producer·checker·reader 의 한 정본 (Codex R9-03)

VER = re.compile(r"_v(\d+)$")          # `matrix_300_0009_v2.csv` — 옛 리비전의 out/ 에만 있는 판 번호 (현행 정본은 unversioned, Codex R6-04)

# 산출 종류별 필수 필드 — **schema.py 가 정본**이고 여기는 이름만 빌린다 (Codex R8-02 · R9-03)
JSON_KEYS = S.DEGENERACY_KEYS
PROVENANCE_COLS = S.PROVENANCE_COLS
MATRIX_COLS = S.MATRIX_ROW
PROFILE_COLS = S.PROFILE_ROW
META_KEYS = ("run_id", "sha256", "artifact", "env", "started_utc",
             "git_commit_at_start", "git_state_changed_during_run")
#: meta 에서 "같은 실행" 이려면 **양쪽에 있고 같아야** 하는 조건 — schema.py 가 정본 (Codex R9-03 C · R10 P1-7).
#: 종류별로 다르다 (shape 는 `S.meta_controls("shape")`, Codex R13 §Q6) — 검사는 `S.meta_controls(kind)` 를 부른다.
META_CONTROLS = S.META_CONTROLS
#: 승격되려면 meta 가 담아야 하는 값 (있기만 한 것이 아니라 **그 값**이어야 한다, Codex R11 P1-9). 전 판은 candidate 가
#: `git_dirty: true` · 바뀐 코드 목록 · bogus start commit · `git_state_changed_during_run: true` 를 **명시해도**
#: rc 0 · promotion true 였다 — 신고된 위험을 gate 가 소비하지 않았다.
SAFE_PROVENANCE = {"git_dirty": False, "git_state_changed_during_run": False, "git_modified_code": []}
#: sidecar 에 반드시 있어야 하는 실행 기록 — argv·roster 는 R9 P2-4 가 만든 것인데 gate 가 요구하지 않았다 (R11 P1-6)
META_REQUIRED = ("argv", "roster")
#: 산출로 세는 확장자 — 명부는 **배제목록**이다 (자체 리뷰 C14). `.log`·`.lock`·`.part` 는 산출이 아니다.
ARTIFACT_SUFFIXES = frozenset({".csv", ".json"})

# 대조할 **수치** 필드 (스키마·provenance 필드는 당연히 다르다 — 숫자만 본다)
JSON_NUM = ("n_accepted", "best_obj", "best_p", "ref_p", "best_modes_percent",
            "LAM_PE_percent", "LAM_NE_percent", "LLI_percent",
            "LAM_PE_percent_observed_cloud", "LAM_NE_percent_observed_cloud",
            "LLI_percent_observed_cloud")
ROW_SKIP = S.ROW_SKIP                  # 출처 문자열은 숫자가 아니다


#: 정본 선택 정책 — 두 규칙은 **호출 모드로** 갈린다 (Codex R7-04). docstring 으로만 갈라 두면 현행 디렉터리에도
#: 역사 규칙이 걸린다: 현행 독자는 `_v2` 를 경고·제외하고 A 를 쓰는데 이 도구는 `_v2`(B) 를 골라 "전부 같다" rc 0 을
#: 냈다 (`_v2` 를 지우면 같은 대조가 차이 2 건 rc 1). `--old-rev` 로 **명시한 역사 리비전**에서만 최고판을 쓴다.
POLICY = {"current": "현행 디렉터리 — 정본은 unversioned 이름 하나, 판 번호가 붙은 형제는 쓰지 않는다 (Codex R6-04·R7-04)",
          "historical": "역사 리비전 — 그 커밋 당시의 정본, 즉 가장 높은 판 (`--old-rev` 로 명시했을 때만)"}


def baseline_for(new_file: pathlib.Path, old: pathlib.Path, policy: str = "current",
                 stale: list | None = None) -> pathlib.Path | None:
    """`new_file` 에 대응하는 옛 정본. `policy`:

    - `current`   : 같은(unversioned) 이름 하나. `_vN` 형제는 **쓰지 않고** `stale` 에 적어 보고한다.
    - `historical`: 그 리비전 당시의 정본 = 가장 높은 판 (`_v2` 가 있으면 그것).

    ⚠ U14-02: 전 판은 이름으로만 골라 `degeneracy_300_0009_Li.json`(v1, 힌트 격자 이전)과 댔다. 그 리비전의 정본은
      `_v2` 였고, 그래서 재실행이 v2 를 그대로 재현했는데도 span 0.0908 → 2.5826 이 "숫자가 움직였다" 로 나왔다.
    ⚠ Codex R7-04: 그 규칙이 현행 디렉터리에도 걸려 있었다 — 그래서 정책을 **인자로** 받는다 (주석이 아니라).
    """
    stem, suffix = new_file.stem, new_file.suffix
    base = VER.sub("", stem)
    cands = []
    for f in old.glob(f"{base}*{suffix}"):
        if f.name.endswith(".meta.json"):
            continue
        st = VER.sub("", f.stem)
        if st != base:
            continue
        m = VER.search(f.stem)
        if m and policy == "current":
            if stale is not None:
                stale.append(f.name)
            continue
        cands.append((int(m.group(1)) if m else 1, f))
    return max(cands)[1] if cands else None


def _same_dir(a: pathlib.Path, b: pathlib.Path) -> bool:
    """두 디렉터리가 같은 object 인가 — symlink·`.` 같은 별칭까지 (Codex R10 P1-8)."""
    try:
        if a.exists() and b.exists():
            return os.path.samefile(a, b)
    except OSError:
        pass
    return os.path.realpath(a) == os.path.realpath(b)


def _kind(f: pathlib.Path) -> str:
    """산출 종류 — `schema.kind_of` 한 자리 (Codex R13 §Q6). ⚠ 전 판은 "json 이면 degeneracy · `matrix_` 면 matrix ·
    아니면 profile" 이라 `ne_shape_*.csv` 도 모르는 이름도 profile 로 읽었다. 모르는 이름은 ValueError — 호출부가
    구조화된 스키마 오류로 센다."""
    return S.kind_of(f.name)


def canonical_names(d: pathlib.Path, policy: str = "current", stale: list | None = None) -> set:
    """디렉터리의 산출 **명부** — canonical basename 집합 (Codex R9-02).

    `current` 는 unversioned 이름만 (`_vN` 은 `stale` 에 적고 명부에서 뺀다), `historical` 은 `_vN` 을 뗀 이름으로 센다
    (그 리비전의 정본이 `_v2` 여도 명부의 항목은 하나다). `.meta.json` 은 산출이 아니다.
    """
    names = set()
    if not d.is_dir():
        return names
    # ⚠ 자체 리뷰 C14 (렌즈 2곳): 전 판은 세 종류만 glob 해서 `run_states.sh` 가 게시하고 `write_meta` 가 서명하는
    #   `ne_shape_*.csv` 가 **명부 밖**이었다 (실측: 서명 13 개 중 12 개만 셌다). 숫자가 바뀌어도 묶음이 미완이어도
    #   게이트가 못 봤다. 허용목록을 **배제목록**으로 뒤집는다.
    #
    #   ⚠ "사이드카가 있는 것만" 으로 좁히면 안 된다 — 서명이 없는 산출이 명부에서 조용히 빠지는 것은 이 발견과
    #     **같은 부류의 버그**다 (옛 스키마 정본은 meta 가 없다). 산출 자리에 있는 것은 전부 명부에 넣고,
    #     묶음이 미완인지는 `_unit` 이 따로 말한다.
    for f in sorted(d.glob("*")):
        if not f.is_file() or f.name.endswith(".meta.json") or f.name.startswith("."):
            continue
        if f.suffix.lower() not in ARTIFACT_SUFFIXES:
            continue                                        # 로그·잠금·임시 파일은 산출이 아니다
        if VER.search(f.stem) and policy == "current":
            if stale is not None:
                stale.append(f.name)
            continue
        names.add(VER.sub("", f.stem) + f.suffix)
    return names


def _csv_rows(data: bytes):
    """검증된 bytes → (행 목록, 헤더). 헤더 순서는 producer 가 정렬해 쓰므로 검사는 이름으로만 한다."""
    rd = csv.DictReader(io.StringIO(data.decode("utf-8-sig")))
    rows = list(rd)
    return rows, list(rd.fieldnames or [])


#: "키가 아예 없다" 를 값과 구별하는 표식 — 부재를 안전값으로 읽지 않기 위한 것 (자체 리뷰 C03)
_ABSENT = "(없음)"


def _show(items, n, render=lambda x: f"  - {x}"):
    """목록을 잘라 찍되 **잘렸다는 것을 항상 말한다** (자체 리뷰 C23).

    전 판은 보고 블록 13 개 중 8 개가 표시 없이 잘렸고(`… 외 N` 은 5 곳뿐) `stale` 은 `--max-show` 를 무시하고
    `--max-show` 를 무시한 하드코딩이었다. 헤더 개수와 `blocked_by` 는 맞으니 거짓말은 아니지만, 목록만 보고 "이게 전부" 라고
    읽게 된다.
    """
    for x in list(items)[:n]:
        print(render(x))
    if len(items) > n:
        print(f"  … 외 {len(items) - n}")


def _peek_meta(art: pathlib.Path) -> dict:
    """사이드카를 **판정 없이** 열어 본다 (alias 판별용 run id). 못 읽으면 빈 dict — 그때는 `_unit` 이 말한다."""
    m = art.with_name(art.name + ".meta.json")
    try:
        return json.loads(m.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}


def _unit(f: pathlib.Path):
    """검증된 (data, meta) snapshot 만 — 경로를 따로 읽지 않는다 (Codex R8-02). → (ok, why, data, meta)"""
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    from provenance import read_unit
    return read_unit(f)


def _receipts_of(kind: str, data: bytes) -> dict:
    """묶음이 신고한 입력 identity → `{"target": {행 key: {역할: sha}}, "ref": …}` (Codex R11 P1-1).

    ⚠ 자체 리뷰 C01 (렌즈 3곳 독립 재현): 전 판은 행별 receipt 를 `dict.update()` 로 뭉쳐 파일당 한 벌만
      만들었다 — 그래서 **마지막 행**의 receipt 만 비교됐다. production 의 matrix 는 행마다 입력이 다르다
      (`verify.build` 가 `hb.identity()`(반쪽전지 소스별)와 `lit_id`(Si 소스별)를 담는다: state 100 은 32 행에
      half_cell sha 2 종 · literature.si sha 8 종). 31 행의 입력 identity 가 대조 대상이 아니었고, 거꾸로
      행 **순서만** 바뀐 정당한 재실행은 거짓 불일치로 막혔다. 행 key 로 담아 key 끼리 댄다.
    """
    if kind == "degeneracy":
        j = S.json_bytes(data)
        return {"target": {None: S.receipt_map(j.get("consumed_inputs"))},
                "ref": {None: S.receipt_map(j.get("ref_consumed_inputs"))}}
    rows, _ = _csv_rows(data)
    key = S.row_key(kind)
    out: dict = {"target": {}, "ref": {}}
    for r in rows:
        try:
            k = key(r)
        except (TypeError, ValueError):
            continue                                     # 숫자가 아닌 key 는 스키마 쪽이 이미 문제로 센다
        for side, col in (("target", "consumed_inputs"), ("ref", "ref_consumed_inputs")):
            raw = r.get(col)
            if raw:
                try:
                    out[side][k] = S.receipt_map(json.loads(raw))
                except (TypeError, ValueError):
                    pass
    return out


def _input_identity_problems(name: str, kind: str, odata: bytes, data: bytes) -> list:
    """두 실행이 **같은 입력 bytes** 를 먹었는가. 다르면 그것은 재현이 아니라 다른 계산이다 (Codex R11 P1-1)."""
    try:
        a, b = _receipts_of(kind, odata), _receipts_of(kind, data)
    except (ValueError, KeyError) as e:
        # ⚠ 자체 리뷰 C32: 전 판은 여기서 **list** 를 돌려줬는데 호출부는 2-tuple 로 풀어 ValueError 로 죽었다
        #   (BOM 이 붙은 JSON 산출이 도달 경로다). 선언한 모양을 지킨다.
        return [f"{name}: 입력 identity 를 읽지 못했다 ({e})"], []
    problems, uncomparable = [], []
    for side in ("target", "ref"):
        x, y = a[side], b[side]
        if not x and not y:
            continue                                     # 둘 다 receipt 가 없다 (옛 산출) — 스키마 쪽이 이미 말한다
        if not x or not y:
            # ⚠ 한쪽만 입력을 적었다. 역할별로 16 줄을 뿜는 것은 거짓이다 — 진실은 "**댈 수 없다**" 한 줄이고,
            #   그것은 숫자 mismatch 가 아니라 승격 불가 사유다 (정본이 옛 스키마면 여기로 온다).
            who = "정본이" if not x else "새 산출이"
            uncomparable.append(f"{name}: {side} 입력 identity 를 {who} 안 적었다 — 같은 입력을 먹었다고 말할 수 "
                                f"없다 (승격 불가)")
            continue
        # 행 key 끼리 댄다 (C01). 한쪽에만 있는 key 는 숫자 비교가 이미 "정본에만/새 산출에만" 으로 센다.
        for k in sorted(set(x) & set(y), key=str):
            where = f"{name}" if k is None else f"{name}:{k}"
            _compare_roles(where, side, x[k], y[k], problems, uncomparable)
    return problems, uncomparable


def _compare_roles(where: str, side: str, x: dict, y: dict, problems: list, uncomparable: list) -> None:
    """한 행(또는 JSON 한 묶음)의 `{역할: sha}` 두 벌을 댄다 — C01 이 행 단위로 내려보낸 뒤의 알맹이."""
    if not x and not y:
        return
    if not x or not y:
        # ⚠ 자체 리뷰 C16: 사면의 근거는 **정본의 나이**다 (옛 스키마로 만든 산출은 새 산출의 계약 위반이 아니다).
        #   전 판은 candidate 쪽 누락까지 같은 가지로 흘려 rc 0 을 줬다 — `who` 는 맞는데 등급이 틀렸다.
        #   새 산출이 자기 입력을 안 적은 것은 그냥 계약 위반이다.
        if not y:
            problems.append(f"{where}: {side} 입력 identity 를 **새 산출이** 안 적었다 — 자기가 먹은 입력을 "
                            f"신고하지 않은 묶음은 승격 대상이 아니다")
            return
        uncomparable.append(f"{where}: {side} 입력 identity 를 정본이 안 적었다 — 같은 입력을 먹었다고 말할 수 "
                            f"없다 (승격 불가)")
        return
    for role in sorted(set(x) | set(y)):
        if x.get(role) != y.get(role):
            problems.append(f"{where}: {side} 입력 {role} 의 identity 가 다르다 — 정본 {str(x.get(role))[:12]}… → "
                            f"새 {str(y.get(role))[:12]}… (같은 입력이 아니면 재현이 아니다)")


def _num_diff(a, b, path="", added=None):
    """같은 모양의 두 값에서 다른 스칼라를 [(경로, 옛, 새)] 로. 숫자는 문자열이어도 float 로 댄다.

    ⚠ U14-02: 정본에 **없던 필드**(스키마 추가분 — `grid_pct`·`attainable_pct` 등)는 `None → [값]` 이 되어 전부
      diff 로 세어졌다 (618 건 중 대부분). 새 필드는 스키마 얘기지 숫자가 움직인 것이 아니다 — `added` 로 뺀다.
    """
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            kp = f"{path}.{k}" if path else k
            if k not in a and added is not None:
                added.append(kp); continue
            out += _num_diff(a.get(k), b.get(k), kp, added)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, f"길이 {len(a)}", f"길이 {len(b)}"))
        else:
            for i, (x, y) in enumerate(zip(a, b)):
                out += _num_diff(x, y, f"{path}[{i}]", added)
    else:
        try:
            if float(a) == float(b):
                return out
        except (TypeError, ValueError):
            if a == b:
                return out
        out.append((path, a, b))
    return out


def check(new: pathlib.Path, old: pathlib.Path | None, schema_only=False, policy: str = "current") -> dict:
    """새 산출을 명부·스키마·내용·조건·숫자로 대조한다 → 결과 dict (main 이 찍고 종료 코드를 정한다).

    키: seen · missing(열/키 이름 누락) · content(값이 스키마가 아님 — 빈 셀·숫자 아님·receipt·중복 key) · diffs(숫자) ·
    added(정본에 없던 필드) · paired · stale · broken(묶음 불일치/미완) · controls(실행 조건 불일치) ·
    roster_missing(정본에 있는데 새 산출에 없음) · roster_extra(새 산출에만) · n_old · n_new.
    """
    R: dict = {"seen": 0, "missing": [], "content": [], "diffs": [], "added": [], "paired": [], "stale": [],
               "broken": [], "controls": [], "env": [], "alias": [], "provenance": [], "inputs": [],
               "inputs_uncomparable": [], "env_uncomparable": [],
               "roster_missing": [], "roster_extra": [], "stale_new": [], "n_old": 0, "n_new": 0}
    new_stale: list = []          # 후보 디렉터리의 `_vN` — C12 로 blocked_by 에 나간다
    # ⚠ `.meta.json` 은 산출이 아니다 — `degeneracy_*.json` glob 이 `degeneracy_100_Li.json.meta.json` 까지
    #   먹어서 meta 를 산출로 점검했다 (TOCTOU 렌즈 N02 가 소비자 glob 에서 확인한 것과 같은 종류).
    new_names = canonical_names(new, "current", new_stale)
    # ⚠ 자체 리뷰 C12: 전 판은 후보의 `_vN` 을 명부에서 조용히 빼고 옛 사본만 대조해 "숫자 전부 같다" rc 0 ·
    #   promotion true 를 냈다 (진짜 재실행이 무시됐다). `PROMOTION` 에 `stale` 항목이 없어 자동 소비자는 볼
    #   수단도 없었다. **후보 쪽** stale 은 따로 세어 승격을 막는다 (정본 쪽 `_vN` 은 지금처럼 경고로 둔다).
    R["stale_new"] = list(new_stale)
    R["stale"] += [f"{n} (새 산출 디렉터리)" for n in new_stale]
    R["n_new"] = len(new_names)
    if old is not None:
        # ⚠ Codex R9-02: 명부는 new 가 아니라 **정본 ∪ new** 다. 정본에 있는데 new 에 없는 것은 "안 본 것" 이지 "같은 것" 이
        #   아니다 — 전 판은 new 의 1 개만 돌고 "전부 같다" 였다.
        old_names = canonical_names(old, policy, R["stale"])
        R["n_old"] = len(old_names)
        R["roster_missing"] = sorted(old_names - new_names)
        R["roster_extra"] = sorted(new_names - old_names)
    for name in sorted(new_names):
        f = new / name
        R["seen"] += 1
        # ⚠ Codex R8-02: data 와 meta 를 따로 읽고 필드 존재만 보면, 다른 정상 시도가 data 만 게시한 중단 상태
        #   (data B / meta A) 가 "전부 갖췄다 · 전부 같다 · rc 0" 이 된다. 검증된 snapshot 만 검사한다.
        ok, why, data, meta = _unit(f)
        if ok is False:
            R["broken"].append(f"{f.name}: 묶음 불일치/미완 — {why}"); continue
        try:
            kind = _kind(f)
        except ValueError as e:
            R["content"].append(f"{f.name}: 모르는 산출 종류 — {e} (Codex R13 §Q6)"); continue
        j = rows = hdr = None
        if kind == "degeneracy":
            # ⚠ Codex R13 P2-3: 전 판은 `decode("utf-8")` + 맨 `json.loads` 라 BOM 하나에
            #   `JSONDecodeError` 가 그대로 올라가 rc 1 로 죽었다 — `PROMOTION` 도 안 찍혀
            #   자동 소비자가 실패 원인을 분류할 수 없었다. CSV 쪽은 이미 `utf-8-sig` 를 쓰는데
            #   JSON 만 비대칭이었다. 읽기는 같은 규칙으로, 파싱 실패는 **구조화된 스키마 오류**로.
            try:
                j = S.json_bytes(data)
            except (UnicodeDecodeError, ValueError) as e:
                R["content"].append(f"{f.name}: JSON 을 읽을 수 없다 ({type(e).__name__}: {e}) "
                                    f"— 스키마 오류다 (Codex R13 P2-3)")
                continue
            R["missing"] += [f"{f.name}: {k}" for k in JSON_KEYS if j.get(k) in (None, "")]
            R["content"] += [f"{f.name}: {p}" for p in S.check_degeneracy(j) if not p.startswith("키 없음")]
        else:
            rows, hdr = _csv_rows(data)
            R["missing"] += [f"{f.name}: {c}" for c in S.required_columns(kind) if c not in hdr]
            # ⚠ Codex R9-03: 열 이름 다음은 **값**이다 — 필수 셀 nonempty · 숫자 파싱 · receipt · 중복 key (schema-only 에서도)
            R["content"] += [f"{f.name}: {p}" for p in S.check_rows(kind, rows, hdr, name=f.name)
                             if not p.startswith("열 없음")]
        if meta is None:
            R["missing"].append(f"{f.name}: .meta.json 없음")
        else:
            R["missing"] += [f"{f.name}.meta: {k}" for k in META_KEYS if meta.get(k) is None]
            # ⚠ Codex R11 P1-6: 실행 조건·argv·roster 는 **묶음의 스키마**다 — 비교 모드에서만 보면 schema-only 가
            #   그 축을 통째로 건너뛴다 (전 판은 지워도 통과했다).
            R["missing"] += [f"{f.name}.meta: {k}" for k in (*S.meta_controls(kind), *META_REQUIRED)
                             if meta.get(k) in (None, "")]
            if not (isinstance(meta.get("env"), dict) and meta["env"]):
                R["missing"].append(f"{f.name}.meta: env 가 비어 있다")
            # ⚠ Codex R11 P1-9: 신고된 위험은 값으로 소비한다 (있기만 하면 되는 것이 아니다).
            # ⚠ 자체 리뷰 C03 (렌즈 2곳): 전 판은 `if k in meta` 라 **키를 지우면 검사가 안 돌았다** — 같은 dirty
            #   트리에서 돈 두 실행 중 정직하게 신고한 쪽만 rc 2 이고 입 다문 쪽은 rc 0 이었다 (게이트가 침묵에
            #   보상). 부재는 안전값이 아니다.
            for k, want in SAFE_PROVENANCE.items():
                if meta.get(k, _ABSENT) != want:
                    got = meta.get(k, _ABSENT)
                    R["provenance"].append(f"{f.name}.meta:{k} = {got!r} (승격 조건은 {want!r})")
            # ⚠ sidecar 의 roster 는 본문에서 유도된 값이어야 한다 — 같은 함수로 다시 유도해 댄다 (Codex R9 P2-4 의
            #   봉인이 실제로 그 본문의 것인지). 어긋나면 그 sidecar 는 이 묶음의 것이 아니다.
            try:
                want_roster = S.body_roster(f.name, data)
            except (ValueError, KeyError):
                want_roster = None
            if want_roster is not None and meta.get("roster") not in (None, "") and meta["roster"] != want_roster:
                R["content"].append(f"{f.name}.meta:roster 가 본문에서 유도한 명부와 다르다 — {meta['roster']} ≠ {want_roster}")
            # ⚠ Codex R13 §Q6: shape 의 typed status·pairing 은 sidecar 에만 있다 — 정본 모집단·본문과 여기서 댄다
            if kind == "shape" and rows is not None:
                R["content"] += [f"{f.name}: {q}" for q in S.check_shape_meta(meta, rows, f.name)]
            start = str(meta.get("git_commit_at_start") or "")
            if start and not re.fullmatch(r"[0-9a-f]{40}", start):
                R["provenance"].append(f"{f.name}.meta:git_commit_at_start 가 40-hex 커밋이 아니다 ({start!r})")
        if schema_only or old is None:
            continue
        o = baseline_for(f, old, policy, R["stale"])
        if o is None:
            continue                                            # roster_extra 가 이미 말한다
        R["paired"].append((f.name, o.name))
        # ⚠ Codex R11 P1-5: 디렉터리가 달라도 **파일이 같은 inode** 면 자기대조다 (hardlink/symlink). data 와 meta 를
        #   각각 본다 — 전 판은 디렉터리만 보고 rc 0 · promotion true 를 냈다.
        for a_, b_, what in ((f, o, "산출"), (f.with_name(f.name + ".meta.json"),
                                              o.with_name(o.name + ".meta.json"), "meta")):
            if a_.exists() and b_.exists() and os.path.samefile(a_, b_):
                R["alias"].append(f"{f.name}: 새 산출과 정본의 {what} 가 **같은 object** 다 (hardlink/symlink) — "
                                  f"독립 baseline 이 아니다")
        # ⚠ 자체 리뷰 C02 (렌즈 2곳): inode 만 보면 `cp -a` 로 만든 바이트 동일 사본이 독립 baseline 으로 통했다
        #   (계산을 한 번도 안 하고 승격 증명서). `run_id` 는 시도마다 uuid4 이므로 **독립 실행이면 같을 수 없다** —
        #   그런데 `ROW_SKIP` 에 있어 숫자 비교에서 빠지고 `META_CONTROLS` 에도 없어 아무도 안 봤다.
        _orid = _peek_meta(o).get("run_id")
        if meta and _orid and meta.get("run_id") == _orid:
            R["alias"].append(f"{f.name}: 새 산출과 정본의 run id 가 같다 ({_orid!r}) — 같은 시도의 사본이지 "
                              f"독립 baseline 이 아니다 (run id 는 시도마다 새로 만든다)")
        ook, owhy, odata, ometa = _unit(o)
        if ook is False:
            R["diffs"].append((f"{o.name}", "정본 묶음 불일치/미완", owhy)); continue
        # ⚠ Codex R9-03 C: 실행 조건이 다르면 같은 실행의 재현이 아니다 — 숫자가 같아도 승격 대상이 아니다.
        # ⚠ Codex R10 P1-7: 전 판은 **양쪽에 key 가 있을 때만** 댔다 — candidate 에서 `state`·`starts` 를 지우면
        #   검사가 잠들고 rc 0 "전부 같다" 였다. 필수 control 은 **있어야** 하고, `env` 는 존재가 아니라 **값**을 댄다.
        if meta and ometa:
            for k in S.meta_controls(kind):
                if k not in ometa or k not in meta:
                    R["controls"].append((f"{f.name}.meta:{k}", ometa.get(k, "(없음)"), meta.get(k, "(없음)")))
                elif _num_diff(ometa[k], meta[k]):
                    R["controls"].append((f"{f.name}.meta:{k}", ometa[k], meta[k]))
            # ⚠ U18-03 (2026-09-13 실측): 옛 정본은 `env` 를 안 적는다 (그 계약이 R10 P1-7 뒤에 생겼다). 그것을
            #   "다른 기계다"(계약 위반, rc 2)로 세면 **정본의 나이**를 새 산출의 위반으로 청구하는 것이다 —
            #   자체 리뷰 C16 이 입력 identity 축에서 닫은 바로 그 비대칭. 정본이 없으면 **대조 불가**(승격만
            #   불가), 새 산출이 없으면 계약 위반이다 (후자는 위의 `env 가 비어 있다` 가 schema-only 에서도 잡는다).
            if not (isinstance(ometa.get("env"), dict) and ometa["env"]):
                R["env_uncomparable"].append(
                    f"{f.name}.meta: env 를 **정본이** 안 적었다 — 같은 환경에서 돌았다고 말할 수 없다 (승격 불가)")
            else:
                R["env"] += [f"{f.name}.meta:{x}" for x in S.env_problems(ometa.get("env"), meta.get("env"))]
        # ⚠ Codex R11 P1-1: 각 receipt 가 **자기 안에서** 유효한 것과 두 실행이 **같은 입력**을 먹은 것은 다른 문제다.
        #   `ROW_SKIP` 이 identity 를 숫자 비교에서 빼기 때문에, 네 digest 가 전부 달라도 rc 0 · promotion true 였다.
        #   역할별 sha 를 정규화해 대조한다 — 다르면 숫자 비교 전에 막는다.
        _mismatch, _uncomparable = _input_identity_problems(f.name, kind, odata, data)
        R["inputs"] += _mismatch
        R["inputs_uncomparable"] += _uncomparable
        if kind == "degeneracy":
            a = S.json_bytes(odata)
            for k in S.DEGENERACY_CONTROLS:
                if k in a and k in j and _num_diff(a[k], j[k]):
                    R["controls"].append((f"{f.name}:{k}", a[k], j[k]))
            for k in JSON_NUM:
                if k not in a and k in j:                        # 정본에 없던 필드 = 스키마 추가분 (U14-02)
                    R["added"].append(f"{f.name}:{k}"); continue
                sub: list = []
                R["diffs"] += [(f"{f.name}:{k}{p and '.' + p}", x, y) for p, x, y in _num_diff(a.get(k), j.get(k), added=sub)]
                R["added"] += [f"{f.name}:{k}.{x}" for x in sub]
        else:
            # ⚠ Codex R8-05: dict comprehension 은 같은 key 의 앞 행을 **조용히** 지운다 — 변환 전에 유일성을 센다.
            #   reader(ne_shape)·checker 가 같은 typed validator 를 쓴다 (Codex R9-05: w_dqdv 는 숫자 key).
            key = S.row_key(kind)
            orows, _ = _csv_rows(odata)
            A, dupA, nA = S.unique_rows(orows, key)
            B, dupB, nB = S.unique_rows(rows, key)
            for side, dup in (("정본", dupA), ("새 산출", dupB)):
                for k in dup:
                    R["diffs"].append((f"{f.name}:{k}", f"{side}에 중복 key", "행을 셀 수 없다 (Codex R8-05)"))
            if nA != nB:
                R["diffs"].append((f"{f.name}", f"정본 행 {nA}", f"새 산출 행 {nB}"))
            for k in sorted(set(A) | set(B), key=str):
                if k not in A or k not in B:
                    R["diffs"].append((f"{f.name}:{k}", "정본에만" if k in A else "새 산출에만", "")); continue
                R["added"] += [f"{f.name}:{c}" for c in sorted(set(B[k]) - set(A[k]) - ROW_SKIP)]
                for c in sorted(set(A[k]) & set(B[k]) - ROW_SKIP):
                    R["diffs"] += [(f"{f.name}:{k}:{c}", x, y) for _, x, y in _num_diff(A[k][c], B[k][c])]
    R["added"] = sorted(set(R["added"])); R["stale"] = sorted(set(R["stale"]))
    return R


def renormalize(new: pathlib.Path) -> int:
    """U14-01 뒷수습 — 이미 게시된 CSV 가 CRLF 면 LF 로 고치고 meta 를 **다시 서명**한다.

    재실행 없이 bytes 를 바꾸는 것이므로 조건을 건다: 파싱한 셀이 **완전히 같아야** 한다 (줄끝만 다르다는 증명).
    하나라도 다르면 그 파일은 건드리지 않는다 — 그때는 재실행이 답이다. 무엇을 했는지는 meta 에 적는다.
    """
    import datetime, hashlib
    touched, refused, skipped = [], [], []
    for f in sorted(new.glob("*.csv")):
        raw = f.read_bytes()
        lf = raw.replace(b"\r\n", b"\n")
        if lf != raw:                               # 디스크가 CRLF 면 먼저 LF 로 (셀이 같을 때만)
            if list(csv.reader(raw.decode("utf-8").splitlines())) != list(csv.reader(lf.decode("utf-8").splitlines())):
                refused.append(f"{f.name} (줄끝 말고 다른 것이 바뀐다)"); continue
        m = f.with_name(f.name + ".meta.json")
        if not m.is_file():
            skipped.append(f"{f.name} (meta 없음 — 옛 산출)")
            if lf != raw:
                f.write_bytes(lf); touched.append(f"{f.name} (줄끝만, 서명 없음)")
            continue
        meta = json.loads(m.read_text(encoding="utf-8"))
        want = meta.get("sha256")
        if not want:                                # 옛 meta (R5 이전) — 서명이 없으니 다시 서명할 것도 없다
            skipped.append(f"{f.name} (옛 meta — sha256 없음)")
            if lf != raw:
                f.write_bytes(lf); touched.append(f"{f.name} (줄끝만, 서명 없음)")
            continue
        # ⚠ 기록된 해시가 **어느 줄끝**의 것이든, 지금 bytes 의 줄끝 변형 중 하나와 맞으면 "줄끝만 다르다" 가
        #   증명된다 (git 정규화는 CRLF→LF, Windows 체크아웃은 LF→CRLF — 양쪽 다 본다).
        crlf = lf.replace(b"\n", b"\r\n")
        if want not in {hashlib.sha256(x).hexdigest() for x in (raw, lf, crlf)}:
            refused.append(f"{f.name} (meta 의 sha256 이 줄끝 변형 어느 것과도 안 맞는다 — 내용이 다르다)"); continue
        if want == hashlib.sha256(lf).hexdigest() and lf == raw:
            continue                                # 이미 LF 이고 서명도 그것 — 할 일 없음
        f.write_bytes(lf)
        meta["sha256"] = hashlib.sha256(lf).hexdigest()
        meta["bytes_renormalized"] = {
            "what": "CRLF→LF", "why": "U14-01 — writer 가 CRLF 를 썼고 git 은 LF 로 저장한다 (서명이 fresh clone 에서 깨진다)",
            "verified": "기록된 sha256 이 지금 bytes 의 줄끝 변형과 맞는다 (내용은 같고 줄끝만 다르다)",
            "utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        m.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        touched.append(f.name)
    print(f"줄끝 정규화: {len(touched)} 개 처리" + (f" — {', '.join(touched)}" if touched else " (고칠 것이 없다)"))
    if skipped:
        print(f"  meta 없는 옛 산출 {len(skipped)} — 서명이 없어 다시 서명할 것도 없다: {', '.join(skipped[:12])}"
              + (f" … 외 {len(skipped) - 12}" if len(skipped) > 12 else ""))
    if refused:
        print(f"! 손대지 않음 {len(refused)}: {', '.join(refused)}")
        print("  내용이 다르다는 뜻이다 — 재실행이 답이다 (bytes 를 손으로 고치면 서명의 뜻이 사라진다).")
    return 1 if refused else 0


def extract_rev(rev: str, dest: pathlib.Path, repo: pathlib.Path) -> int:
    """`<rev>` 의 `out/` 을 `dest` 로 꺼낸다 — 정본을 git 에서 직접 읽는다.

    ⚠ 2026-09-12: `git show <rev> --name-only` 는 그 커밋이 **바꾼** 파일을 주지 트리를 주지 않는다. 그걸로
      정본을 모으면 디렉터리가 비고 전부 "정본에 없음" 으로 나온다. 트리는 `git ls-tree -r` 다.
    """
    import subprocess
    dest.mkdir(parents=True, exist_ok=True)
    try:
        names = subprocess.run(["git", "ls-tree", "-r", "--name-only", rev, "--", "out"],
                               cwd=repo, capture_output=True, text=True, check=True).stdout.split()
    except subprocess.CalledProcessError as e:
        print(f"! `{rev}` 를 읽지 못했다: {e.stderr.strip()}"); return 0
    n = 0
    for name in names:
        rel = pathlib.PurePosixPath(name)
        # `out/` **바로 아래**의 산출만 — `out/bms97/`·`out/recompare/`·`out/cells_*/` 는 다른 축이고,
        # basename 만 떼면 이름이 부딪친다.
        if len(rel.parts) != 2 or rel.suffix not in (".json", ".csv"):
            continue
        # ⚠ `<rev>:<path>` 는 **저장소 루트** 기준이다. cwd 가 하위 디렉터리면 `:./` 를 써야 여기 기준이 된다.
        r = subprocess.run(["git", "show", f"{rev}:./{name}"], cwd=repo, capture_output=True)
        if r.returncode != 0:
            continue
        (dest / rel.name).write_bytes(r.stdout); n += 1
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", required=True, help="재실행 산출 디렉터리 (예: out_u14)")
    ap.add_argument("--old", default="out", help="정본 디렉터리 (기본 out)")
    ap.add_argument("--old-rev", default=None, metavar="REV",
                    help="정본을 디렉터리 대신 **git 커밋**에서 읽는다 (예: `HEAD^`) — 재실행이 out/ 을 이미 "
                         "덮었을 때. 손으로 `git show` 를 엮지 않게 한다")
    ap.add_argument("--schema-only", action="store_true", help="숫자 대조 없이 스키마·내용(구조) 검사만")
    ap.add_argument("--subset", action="store_true",
                    help="명시적 **부분** 재실행 계약 (Codex R9-02): 정본 명부 중 일부만 새로 만들었다. 없는 항목을 실패로 세지 "
                         "않는 대신 범위(k/N)를 찍고, 결과는 승격 근거가 아니다")
    ap.add_argument("--max-show", type=int, default=20)
    ap.add_argument("--baseline-policy", choices=("auto", "current", "historical"), default="auto",
                    help="정본 선택 규칙 (Codex R7-04). auto = `--old-rev` 면 historical, 아니면 current. "
                         "옛 커밋의 out/ 을 **손으로 풀어** `--old` 로 줄 때는 historical 을 명시할 것 — 그 시절 "
                         "정본은 가장 높은 `_vN` 이다 (U14-02)")
    ap.add_argument("--renormalize", action="store_true",
                    help="U14-01 뒷수습: CRLF 로 게시된 CSV 를 LF 로 고치고 meta 를 다시 서명한다 "
                         "(파싱한 셀이 완전히 같을 때만 — 아니면 그 파일은 건드리지 않는다)")
    a = ap.parse_args()
    import tempfile
    new = pathlib.Path(a.new)
    if not new.is_dir():
        print(f"! {new} 가 없다"); return 2
    if a.renormalize:
        return renormalize(new)
    old = None if a.schema_only else pathlib.Path(a.old)
    tmp = None
    if a.old_rev and not a.schema_only:
        tmp = tempfile.TemporaryDirectory(); old = pathlib.Path(tmp.name)
        n = extract_rev(a.old_rev, old, pathlib.Path(__file__).resolve().parents[1])
        print(f"정본을 `{a.old_rev}` 에서 읽었다 — 산출 {n} 개")
        if not n:
            print("! 그 커밋의 out/ 이 비었다 — 리비전이 맞나?"); return 2
    if old is not None and not old.is_dir():
        print(f"! 정본 디렉터리 {old} 가 없다"); return 2
    # ⚠ Codex R10 P1-8: candidate 와 baseline 이 **같은 object** 면 그 대조는 자기대조다 — 전 판은 같은 디렉터리를
    #   둘 다 주면 rc 0 · roster 1/1 · "전부 같다" 를 내서, baseline 을 이미 덮었거나 애초에 없던 상태와 구별되지
    #   않았다. 경로 문자열이 아니라 samefile/realpath 로 본다 (`--old-rev` 의 immutable bytes 는 별도 임시 경로다).
    if old is not None and _same_dir(new, old):
        print(f"! `--new` 와 `--old` 가 **같은 디렉터리**다 ({new}) — 독립 baseline 이 아니면 승격 판정이 성립하지 "
              f"않는다 (자기대조). 재실행은 별도 destination 으로 받고 정본은 그대로 두거나 `--old-rev` 로 커밋에서 "
              f"읽을 것 (Codex R10 P1-8)"); return 2
    policy = a.baseline_policy if a.baseline_policy != "auto" else ("historical" if a.old_rev else "current")
    R = check(new, old, a.schema_only, policy)
    seen, missing, content, diffs = R["seen"], R["missing"], R["content"], R["diffs"]
    added, paired, stale, broken = R["added"], R["paired"], R["stale"], R["broken"]
    controls, r_missing, r_extra, env_bad = R["controls"], R["roster_missing"], R["roster_extra"], R["env"]
    alias, prov_bad, inputs_bad = R["alias"], R["provenance"], R["inputs"]
    inputs_unk, stale_new, env_unk = R["inputs_uncomparable"], R["stale_new"], R["env_uncomparable"]
    print(f"산출 {seen} 개 점검 ({new})")
    if old is None:
        print("  (`--schema-only`: baseline 도 대조도 없다 — **승격 증명서가 아니다**. 스키마·내용·조건만 본다, "
              "Codex R11 P1-6)")
    if old is not None:
        print(f"  정본 선택 정책: **{policy}** — {POLICY[policy]}")
        print(f"  명부(roster): 정본 {R['n_old']} · 새 산출 {R['n_new']} · 대조 {len(paired)}"
              + (f" — **부분 계약(subset) {len(paired)}/{R['n_old']}**" if a.subset else ""))
    for n, o in paired:
        if n != o:
            print(f"  정본 선택: {n} ↔ **{o}** ({POLICY[policy].split('— ')[-1]})")
    if stale:
        print(f"  ! 정본 디렉터리에 판 번호가 붙은 형제 {len(stale)} 개 — 쓰지 않았다 (`out/archive/` 로 옮길 것): "
              + ", ".join(stale[:a.max_show])
              + (f" … 외 {len(stale) - a.max_show}" if len(stale) > a.max_show else ""))
    if not seen:
        print("! 점검할 산출이 없다 — 경로가 맞나?"); return 2
    if r_missing and not a.subset:
        print(f"\n■ 명부(roster) 불일치 — 정본에 있는데 새 산출에 **없음** {len(r_missing)}/{R['n_old']} (Codex R9-02). 부분 "
              f"재실행이면 `--subset` 으로 계약을 명시할 것 — 그래도 승격 대상은 명부 전부({R['n_old']} 개)를 다시 만든 묶음뿐이다")
        _show(r_missing, a.max_show, lambda n: f"  - {n}: 새 산출에 없음")
    elif r_missing:
        print(f"\n  부분 계약(subset): 정본 명부 {R['n_old']} 개 중 {len(paired)} 개만 대조 ({len(paired)}/{R['n_old']}) — "
              f"새 산출에 없음 {len(r_missing)}: {', '.join(r_missing[:a.max_show])}\n"
              f"  → 이 결과는 **부분** 진술이고 승격 근거가 아니다 (전부를 다시 만든 묶음만 정본을 대신한다)")
    if r_extra:
        print(f"\n■ 명부(roster) 불일치 — 새 산출에만 있음 {len(r_extra)} (정본에 없음): {', '.join(r_extra[:a.max_show])}")
    if broken:
        # ⚠ Codex R8-02: 묶음이 안 맞는 산출은 스키마도 숫자도 **대조하지 않는다** — 어느 쪽 bytes 인지 모른다
        print(f"\n■ 묶음 불일치/미완 {len(broken)} — data 와 meta 가 같은 시도의 것이 아니다 (다른 시도가 data 만 게시했거나 "
              f"게시가 중단됐다). 이 산출은 검사하지 않았다 → 게시를 끝내거나(meta) 다시 돌린 뒤 재검사")
        _show(broken, a.max_show)
        for b in []:
            print(f"  - {b}")
    # ⚠ 자체 리뷰 C22: 이 분해는 사람용 출력과 `PROMOTION` 이 **같은 수**를 쓰게 하려고 밖에 둔다
    prov_only = [m for m in missing if m.rsplit(": ", 1)[-1] in PROVENANCE_COLS]
    rest = [m for m in missing if m not in prov_only]
    if missing:
        if rest:
            print(f"\n■ 새 스키마 누락 {len(rest)} — 옛 코드로 만든 산출이거나 묶음이 미완이다 (재실행이 이 트리에서 돌았는지 확인)")
            _show(rest, a.max_show)
            for m in []:
                print(f"  - {m}")
        if prov_only:
            print(f"\n■ 기준/대상 입력 **출처 열** 누락 {len(prov_only)} — 이 산출은 **provenance-incomplete** 다 "
                  f"(R7-03·R8-04 스키마 이전 실행). 수치는 그대로 인용할 수 있으나 기준 입력의 출처는 그 묶음에서 회수되지 "
                  f"않는다; 실제 재실행(U18)으로 별도 위치에 만들어 비교·승격한다 — 현재 pathname 해시로 소급 채우지 않는다")
            _show(prov_only, a.max_show)
            for m in []:
                print(f"  - {m}")
    if content:
        print(f"\n■ 내용 검사 실패 {len(content)} — 열은 있는데 값이 스키마가 아니다 (빈 필수 셀 · 숫자 아님 · receipt 의 역할/path/"
              f"64-hex/재계산 digest · 중복 key) (Codex R9-03)")
        _show(content, a.max_show)
        for c in []:
            print(f"  - {c}")
    if not missing and not content:
        print("  새 스키마: 전부 갖췄다 (열·키 이름 + 필수 셀·숫자·receipt·중복 key — `bms_balancing/schema.py` 정본)")
    if alias:
        print(f"\n■ **독립 baseline 이 아니다** {len(alias)} — candidate 와 baseline 이 같은 object 를 가리킨다 "
              f"(hardlink/symlink). 자기대조는 승격 근거가 아니다 (Codex R11 P1-5)")
        _show(alias, a.max_show)
        for x in []:
            print(f"  - {x}")
    if inputs_bad:
        print(f"\n■ **입력 identity 불일치** {len(inputs_bad)} — 두 실행이 먹은 입력 bytes 가 다르다. 숫자가 같아도 "
              f"그것은 같은 실행의 재현이 아니다 (Codex R11 P1-1)")
        _show(inputs_bad, a.max_show)
        for x in []:
            print(f"  - {x}")
    if inputs_unk:
        print(f"\n■ **입력 identity 대조 불가** {len(inputs_unk)} — 한쪽이 자기 입력을 안 적었다 (정본이 옛 스키마면 "
              f"여기로 온다). 숫자가 같아도 **같은 입력을 먹었다는 증명은 없다** → 승격 불가 (Codex R11 P1-1)")
        _show(inputs_unk, a.max_show)
        for x in []:
            print(f"  - {x}")
    if prov_bad:
        print(f"\n■ **provenance 가 안전하지 않다** {len(prov_bad)} — 산출 스스로 신고한 위험이다 (git_dirty · 실행 중 "
              f"상태 변경 · 바뀐 코드 · 시작 커밋). 승격은 safe 값 자체를 요구한다 (Codex R11 P1-9)")
        _show(prov_bad, a.max_show)
        for x in []:
            print(f"  - {x}")
    if env_bad:
        print(f"\n■ **환경(env) 불일치** {len(env_bad)} — 정본을 만든 기계와 다른 조합이다 (R6 내부 F3: scipy 1.11↔1.17 "
              f"에서 savgol 이 ULP 로 갈리고 L-BFGS-B 최적점이 달라진다). 숫자가 같아도 같은 실행의 재현이 아니다 "
              f"(Codex R10 P1-7)")
        _show(env_bad, a.max_show)
        for e in []:
            print(f"  - {e}")
    if env_unk:
        print(f"\n■ **환경(env) 대조 불가** {len(env_unk)} — **정본이** 환경을 안 적었다 (옛 스키마면 여기로 온다). "
              f"새 산출의 계약 위반이 아니므로 rc 2 가 아니지만, 같은 환경의 재현이라고 말할 수 없다 → 승격 불가 "
              f"(U18-03 · 자체 리뷰 C16 과 같은 비대칭)")
        _show(env_unk, a.max_show)
    if controls:
        print(f"\n■ 실행 조건 불일치 {len(controls)} — 같은 실행의 재현이 아니다 (n_starts · seed · n_grid · n_samples · tol · "
              f"state · 소스; Codex R9-03). 숫자가 같아도 승격 대상이 아니다")
        _show(controls, a.max_show, lambda t: f"  - {t[0]}: 정본 {t[1]!r} → 새 {t[2]!r}")
        for p, x, y in []:
            print(f"  - {p}: 정본 {x} → 새 {y}")
    if old is not None:
        if added:
            print(f"\n  정본에 없던 필드 {len(added)} — 스키마 추가분이다 (숫자가 움직인 것이 아니다): "
                  + ", ".join(sorted({x.split(":")[-1].split(".")[-1] for x in added})[:12]))
        if diffs:
            print(f"\n■ 정본과 **다른 숫자** {len(diffs)} — 계산 경로는 안 고쳤으므로 같아야 한다.")
            print("   먼저 볼 축: meta 의 `env`(python·numpy·scipy) 가 정본을 만든 기계와 같은가 (R6 내부 F3:")
            print("   scipy 1.11↔1.17 에서 savgol 이 ULP 로 갈리고 L-BFGS-B 최적점이 달라진다).")
            _show(diffs, a.max_show, lambda t: f"  - {t[0]}: 정본 {t[1]} → 새 {t[2]}")
        elif (broken or r_extra or controls or env_bad or missing or content or alias or prov_bad or inputs_bad
              or (r_missing and not a.subset)):
            # ⚠ Codex R10 P1-7: 계약이 깨진 대조에서 "전부 같다" 를 찍으면 그 줄만 인용된다. 숫자가 같아도 **같은
            #   실행의 재현이 아니다** — 명부·스키마·내용·조건·환경 중 하나라도 깨졌으면 미완이라고 말한다.
            print("  숫자: 대조 **미완** — 명부/묶음/스키마/내용/조건/환경 문제를 뺀 나머지만 같다 (전체를 말할 수 없다)")
        elif a.subset and r_missing:
            print(f"  숫자: 대조한 {len(paired)}/{R['n_old']} 개는 정본과 같다 — **부분(subset)** 진술, 승격 아님")
        elif inputs_unk or env_unk:
            # 숫자는 전부 같다. 다만 **같은 입력·같은 환경에서 돌았다는 증명**이 없으므로 승격 근거는 아니다
            # (Codex R11 P1-1 · U18-03).
            why = " · ".join(x for x in ("입력 identity" if inputs_unk else "", "환경" if env_unk else "") if x)
            print(f"  숫자: 정본({old})과 전부 같다 — 그러나 {why} 를 댈 수 없어 **승격 대상은 아니다**")
        else:
            print(f"  숫자: 정본({old})과 전부 같다 — 게시·서명만 바뀌었다")
    contract_broken = bool(missing or broken or content or controls or env_bad or r_extra
                           or alias or prov_bad or inputs_bad or stale_new
                           or (r_missing and not a.subset))
    # ⚠ 자체 리뷰 C11 (렌즈 3곳): 승격 불가인데 rc 0 인 경로가 둘 생겼고(`inputs_uncomparable`·`baseline_absent`),
    #   `WORKING_STATE.md` 의 U18 런북은 문자 그대로 "0 이었을 때만 정본 교체" 다 — 실제 `out/` 을 baseline 으로 한
    #   대조가 정확히 그 상태를 낸다. R10 P2-1 이 subset 에 대해 닫은 축(글자가 아니라 종료 코드로 가른다)이
    #   다시 열렸다. **승격 불가는 rc 0 이 아니다** — 계약은 안 깨졌지만 승격 못 하는 상태에 4 를 준다.
    #   ⚠ 단, `--schema-only` 는 **승격을 묻지 않은** 진단이다 (물어보지 않은 것에 "자격 없음" 코드를 주면 스키마
    #     점검 도구로서 못 쓴다). 그 모드의 비승격은 `promotion_eligible: false` + `baseline_absent` 가 이미
    #     구조적으로 말한다 (R11 P1-6). 4 는 **승격 대조를 물었는데 답을 못 내는** 경우만이다.
    not_promotable = bool(inputs_unk or env_unk)
    rc = 2 if contract_broken else (1 if diffs else (3 if (a.subset and r_missing) else
                                                     (4 if not_promotable else 0)))
    # ⚠ Codex R10 P2-1: "부분 · 승격 아님" 을 **글자로만** 말하면 자동 소비자는 full equality 와 구분할 수 없다.
    #   종료 코드로 가르고(3 = 부분), 판정을 machine-readable 한 줄로 낸다.
    # ⚠ Codex R11 P1-6: **schema-only 는 승격 증명서가 아니다.** baseline 도 대조도 없는 실행이 `promotion_eligible:
    #   true` 를 내면 그 줄만 인용된다 — 구조상 언제나 false 이고 `baseline_absent` 를 blocker 로 적는다.
    baseline_absent = old is None
    # ⚠ Codex R11 P1-1: 입력 identity 를 **댈 수 없는** 대조는 rc 를 바꾸지 않는다 (정본이 옛 스키마인 것은 새 산출의
    #   계약 위반이 아니다) — 그러나 "같은 입력의 재현" 을 증명하지 못하므로 승격 자격은 없다.
    promotion = {"promotion_eligible": rc == 0 and not baseline_absent,
                 "rc": rc, "subset": bool(a.subset),
                 "roster": {"old": R["n_old"], "new": R["n_new"], "compared": len(paired),
                            "missing_in_new": r_missing, "extra_in_new": r_extra},
                 # ⚠ 자체 리뷰 C22: 사람용은 "새 스키마 누락" 과 "출처 열 누락" 으로 갈라 찍는데 기계용은 둘을 합친
                 #   수 하나만 냈다 — 그 합계는 출력 어디에도 없고 문서는 전부 갈라진 두 수를 인용한다.
                 "blocked_by": {"schema": len(rest), "provenance_cols": len(prov_only),
                                "content": len(content), "unit": len(broken),
                                "controls": len(controls), "env": len(env_bad), "numbers": len(diffs),
                                "alias": len(alias), "provenance": len(prov_bad), "inputs": len(inputs_bad),
                                "inputs_uncomparable": len(inputs_unk), "env_uncomparable": len(env_unk),
                                "stale": len(stale_new),
                                "baseline_absent": int(baseline_absent)},
                 "policy": policy, "new": str(new), "old": (str(old) if old is not None else None)}
    print("PROMOTION " + json.dumps(promotion, ensure_ascii=False))
    return rc


if __name__ == "__main__":
    sys.exit(main())
