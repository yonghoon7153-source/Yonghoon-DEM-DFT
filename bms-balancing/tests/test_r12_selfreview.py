"""자체 적대적 리뷰 (2026-09-13, 대상 `fbc52bb` · 코드 정본 `4185955`) — Codex 토큰 소진 뒤 내부 6 렌즈.

원시 45 건 → 중복 합쳐 35 건, 그중 `결론이_바뀜` 14 건. 렌즈는 이 저장소가 실제로 뚫렸던 축이다
(sig-완전성 · validator-우회 · 순서-TOCTOU · 파생-보고서 · archive-이식성 · 공정성-의미).

같은 축을 **여러 렌즈가 독립으로** 친 것이 셋이다 (C01 3회 · C04 3회 · C11 3회) — 10 차에서도 그 패턴이
진짜 구멍의 신호였다. 각 시험의 docstring 에 반례와 렌즈 수를 적는다.

⚠ 이 라운드의 발견은 **대부분 직전 라운드(R11)가 "닫았다" 고 적은 것의 반쪽**이다. 그래서 시험 이름에
어느 R11 항목의 후속인지 같이 적는다.
"""
from __future__ import annotations
import csv, hashlib, io, json, os, pathlib, shutil, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest                                                             # noqa: E402
from bms_balancing import schema as S                                     # noqa: E402
from bms_balancing import verify                                          # noqa: E402
from test_review_findings import matrix_row, seal_combo                    # noqa: E402


def _check_u14(*args):
    p = subprocess.run([sys.executable, str(ROOT / "scripts/check_u14.py"), *map(str, args)],
                       capture_output=True, text=True, timeout=300)
    line = next((l for l in p.stdout.splitlines() if l.startswith("PROMOTION ")), None)
    return p.returncode, p.stdout + p.stderr, (json.loads(line[len("PROMOTION "):]) if line else None)


def _receipt(half="1", full="2", gr="3", si="4"):
    return {"half_cell": {"path": "half.xlsx", "sha256": half * 64},
            "full_cell": {"path": "full.xlsx", "sha256": full * 64},
            "literature": {"gr": {"path": "gr.xlsx", "sha256": gr * 64},
                           "si": {"path": "si.csv", "sha256": si * 64}}}


def _meta(art: pathlib.Path, **over):
    data = art.read_bytes()
    m = {"artifact": art.name, "run_id": "R", "sha256": hashlib.sha256(data).hexdigest(),
         "env": {"python": "3.11.0", "numpy": "1.26.0", "scipy": "1.11.0", "pandas": "2.0.0",
                 "platform": "linux-x"},
         "started_utc": "2026-09-13T00:00:00Z", "git_commit_at_start": "0" * 40,
         "git_state_changed_during_run": False, "git_dirty": False, "git_modified_code": [],
         "state": "100", "half_cell_source": "GITT", "si_source": "Li", "starts": 2, "seed": 0,
         "argv": ["run_states.sh"], "roster": S.body_roster(art.name, data)}
    m.update(over)
    art.with_name(art.name + ".meta.json").write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")
    return m


def _publish_matrix(d: pathlib.Path, rows, name="matrix_100.csv", run_id="R", **meta_over):
    """행과 사이드카의 `run_id` 를 **같은 값**으로 묶어 게시한다.

    ⚠ 독립 실행이면 run id 가 달라야 한다 (`verify.run_id_of` 는 시도마다 uuid4) — C02 를 닫은 뒤로 게이트가
      그것을 alias 로 본다. 그래서 baseline 과 candidate 를 만들 때 `run_id` 를 다르게 준다.
    """
    d.mkdir(parents=True, exist_ok=True)
    f = d / name
    verify.atomic_write_csv(f, [dict(r, run_id=run_id) for r in rows], list(S.MATRIX_ROW))
    _meta(f, run_id=run_id, **meta_over)
    return f


def _rows_per_si(tag_half, tag_si, n=4):
    """production 모양: 행마다 receipt 가 다르다.

    `verify.build`(`bms_balancing/verify.py:183`)가 `consumed_inputs` 에 `hb.identity()`(반쪽전지 소스별)와
    `lit_id`(Si 소스별, `:169`)를 담으므로, state 100 의 matrix 32 행에는 half_cell sha 2 종 ·
    literature.si sha 8 종이 들어간다. 행별로 같은 receipt 를 넣는 fixture 는 그 사실을 가린다.
    """
    out = []
    for i in range(n):
        ci = _receipt(half=tag_half, si=(tag_si if i == 0 else "4"))
        rci = _receipt(half="5", si=(tag_si if i == 0 else "4"))
        out.append(matrix_row(si=["Li", "Kunz", "Lu", "Yoon"][i], w_dqdv="0", run_id="R",
                              consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(rci),
                              inputs_sha=S.inputs_digest(ci), ref_inputs_sha=S.inputs_digest(rci)))
    return seal_combo(out)              # 모집단 주장을 행 수와 맞춘다 (자체 리뷰 C05)


# ── C01 · R11 P1-1 의 후속 (렌즈 3곳 독립 재현) ───────────────────────────────────────────────
def test_f01_input_identity_is_compared_per_row_not_collapsed(tmp_path):
    """[C01 · 결론이_바뀜 · sig-완전성 · validator-우회 · 공정성-의미]

    `_receipts_of` 가 행별 receipt 를 `dict.update()` 로 뭉쳐 파일당 `{역할: sha}` **한 벌**만 만들었다.
    그래서 32 행 matrix 에서 마지막 행의 receipt 만 비교됐다 — 앞 31 행이 전혀 다른 입력 bytes 를 먹었다고
    스스로 신고해도 `blocked_by.inputs: 0` · rc 0 · `promotion_eligible: true`.

    양방향이다: 행 **순서만** 뒤집힌 정당한 재실행은 거꾸로 거짓 불일치로 rc 2 가 됐다.

    닫힘 조건: 행 key(`S.matrix_key`) 별로 `{역할: sha}` 를 만들어 key 끼리 대조한다 (순서 무관).
    """
    old, new = tmp_path / "old", tmp_path / "new"
    _publish_matrix(old, _rows_per_si("a", "a"), run_id="R1")
    _publish_matrix(new, _rows_per_si("a", "b"), run_id="R2")            # 첫 행의 literature.si 만 다르다
    rc, text, promo = _check_u14("--new", new, "--old", old)
    assert promo and promo["blocked_by"].get("inputs"), f"마지막 행만 보고 있다:\n{text[-900:]}"
    assert rc == 2 and promo["promotion_eligible"] is False, (rc, text[-600:])

    # 반대 방향: 같은 행 집합을 순서만 뒤집은 정당한 재실행은 막히면 안 된다
    a, b = tmp_path / "ra", tmp_path / "rb"
    rows = _rows_per_si("a", "a")
    _publish_matrix(a, rows, run_id="R1")
    _publish_matrix(b, list(reversed(rows)), run_id="R2")
    rc, text, promo = _check_u14("--new", b, "--old", a)
    assert promo and not promo["blocked_by"].get("inputs"), f"순서만 바뀐 재실행을 거짓 불일치로 막았다:\n{text[-900:]}"


# ── C13 · 같은 뿌리 (sig-완전성) ──────────────────────────────────────────────────────────────
def test_f02_receipt_written_as_json_string_is_not_silently_uncomparable(tmp_path):
    """[C13 · 결론이_바뀜 · sig-완전성]

    degeneracy JSON 의 `consumed_inputs` 가 dict 가 아니라 **JSON 문자열**이면 `receipt_map` 이 `{}` 를 내고,
    양쪽 다 `{}` 라 `if not x and not y: continue` 로 넘어가 `inputs_uncomparable` 조차 안 찍혔다.
    `check_degeneracy` 도 `[]` 였다 (스키마 쪽이 말해 준다는 전제가 거짓이었다) — 서로 다른 반쪽전지를 먹은
    두 실행이 rc 0 · `promotion_eligible: true`.

    닫힘 조건: `receipt_map` 이 `validate_receipt` 와 **같은 정규화**(str 이면 한 겹 decode)를 쓴다.
    """
    a, b = _receipt(half="a"), _receipt(half="b")
    assert S.receipt_map(json.dumps(a)) == S.receipt_map(a), "문자열 receipt 를 dict 와 다르게 읽는다"
    assert S.receipt_map(json.dumps(a)) != S.receipt_map(json.dumps(b))


# ── C32 · 오류 분기 (sig-완전성) ──────────────────────────────────────────────────────────────
def test_f03_identity_error_branch_returns_the_declared_shape(tmp_path):
    """[C32 · 사소 · sig-완전성] `_input_identity_problems` 의 오류 분기가 `list` 를 돌려주는데 호출부는
    2-tuple 로 푼다 → `ValueError: not enough values to unpack`. UTF-8 BOM 이 붙은 degeneracy JSON 이
    도달 경로다 (`read_unit` 은 `utf-8-sig` 라 "일치" 로 통과시킨다). gate 가 traceback 으로 죽고 rc 1 —
    문서상 "숫자가 다름" 으로 오독된다."""
    sys.path.insert(0, str(ROOT / "scripts"))
    import check_u14 as C
    got = C._input_identity_problems("x.json", "degeneracy", b"\xef\xbb\xbf{}", b"{}")
    assert isinstance(got, tuple) and len(got) == 2, f"선언한 모양이 아니다: {type(got).__name__}"


# ── C02 · R11 P1-5 의 후속 (렌즈 2곳) ─────────────────────────────────────────────────────────
def test_f04_byte_identical_copy_is_not_an_independent_baseline(tmp_path):
    """[C02 · 결론이_바뀜 · validator-우회 · 순서-TOCTOU]

    R10 P1-8 이 같은 디렉터리를, R11 P1-5 가 같은 inode 를 막았는데 **바이트 동일 복사**(`cp -a`/`copytree`)가
    세 번째 칸으로 열려 있었다: `samefile` False → rc 0 · `blocked_by.alias: 0` · `promotion_eligible: true`.
    계산을 한 번도 안 하고 승격 증명서를 받는다.

    판별 정보는 이미 손에 있다 — `run_id` 는 시도마다 uuid4 (`verify.run_id_of`) 이므로 독립 실행이면 같을 수
    없다. 그런데 `run_id` 는 `S.ROW_SKIP` 에 있어 숫자 비교에서 빠지고 `S.META_CONTROLS` 에도 없어 아무도 안 봤다.

    닫힘 조건: 두 묶음의 meta `run_id` 가 같으면 alias 로 센다 (inode 가 아니라 실행 identity).
    """
    old = tmp_path / "old"
    _publish_matrix(old, _rows_per_si("a", "a"), run_id="R1")
    new = tmp_path / "new"
    shutil.copytree(old, new)
    assert not os.path.samefile(old / "matrix_100.csv", new / "matrix_100.csv"), "fixture: 별개 inode 여야 한다"
    rc, text, promo = _check_u14("--new", new, "--old", old)
    assert promo and promo["blocked_by"].get("alias"), f"바이트 동일 사본이 독립 baseline 으로 통했다:\n{text[-800:]}"
    assert promo["promotion_eligible"] is False and rc == 2, (rc, text[-500:])

    # 대조군: run_id 가 다른 진짜 재실행은 막히면 안 된다
    _publish_matrix(new, _rows_per_si("a", "a"), run_id="R2")
    rc, text, promo = _check_u14("--new", new, "--old", old)
    assert promo and not promo["blocked_by"].get("alias"), f"독립 재실행을 alias 로 막았다:\n{text[-800:]}"


# ── C03 · R11 P1-9 의 후속 (렌즈 2곳) ─────────────────────────────────────────────────────────
def test_f05_missing_provenance_keys_are_unsafe_not_absent(tmp_path):
    """[C03 · 결론이_바뀜 · validator-우회 · sig-완전성]

    `SAFE_PROVENANCE` 검사가 `if k in meta and meta[k] != want` 라서 **키를 지우면 검사가 안 돌았다.**
    `git_dirty`·`git_modified_code` 는 `META_KEYS` 에도 없어 "새 스키마: 전부 갖췄다" 까지 받았다.
    같은 dirty 트리에서 돈 두 실행 중 **정직하게 신고한 쪽만 rc 2** 이고 입 다문 쪽은 rc 0 — 게이트가 침묵에
    보상을 준다.

    닫힘 조건: 부재를 안전값으로 읽지 않는다 (`meta.get(k, "(없음)") != want`).
    """
    old, honest, silent = tmp_path / "old", tmp_path / "honest", tmp_path / "silent"
    rows = _rows_per_si("a", "a")
    _publish_matrix(old, rows, run_id="R1")
    _publish_matrix(honest, rows, run_id="R2", git_dirty=True,
                    git_modified_code=["bms_balancing/verify.py"])
    _publish_matrix(silent, rows, run_id="R2")
    m = json.loads((silent / "matrix_100.csv.meta.json").read_text(encoding="utf-8"))
    m.pop("git_dirty"); m.pop("git_modified_code")
    (silent / "matrix_100.csv.meta.json").write_text(json.dumps(m, ensure_ascii=False), encoding="utf-8")

    rc_h, _, promo_h = _check_u14("--new", honest, "--old", old)
    rc_s, text_s, promo_s = _check_u14("--new", silent, "--old", old)
    assert promo_h and promo_h["blocked_by"]["provenance"], "대조군(정직한 신고)이 안 막혔다 — fixture 문제"
    assert promo_s and promo_s["blocked_by"].get("provenance"), \
        f"두 key 를 지운 meta 가 통과했다 (게이트가 침묵에 보상):\n{text_s[-800:]}"
    assert rc_s == 2, (rc_s, text_s[-400:])


# ── C12 · 명부 (파생-보고서) ──────────────────────────────────────────────────────────────────
def test_f06_versioned_sibling_in_the_candidate_dir_is_not_silently_dropped(tmp_path):
    """[C12 · 결론이_바뀜 · 파생-보고서]

    후보 디렉터리에 진짜 재실행 `matrix_100_v2.csv`(숫자가 다르다)와 옛 사본 `matrix_100.csv`(정본과 동일)가
    함께 있으면, 게이트는 `_vN` 을 명부에서 조용히 빼고 옛 사본만 대조해 "숫자: 전부 같다" rc 0 ·
    `promotion_eligible: true` 를 냈다. `PROMOTION` JSON 에 `stale` 항목이 **없어서** 자동 소비자는 경고를 볼
    수단이 전혀 없었다 (사람용 한 줄만 있었고, 그 문장은 "정본 디렉터리에 …(새 산출 디렉터리)" 로 자기모순).

    닫힘 조건: `stale` 을 `blocked_by` 로 내보내고, **후보 디렉터리**의 `_vN` 은 승격을 막는다.
    """
    old, new = tmp_path / "old", tmp_path / "new"
    rows = _rows_per_si("a", "a")
    _publish_matrix(old, rows, run_id="R1")
    _publish_matrix(new, rows, run_id="R2")
    moved = [dict(r, LLI_pct="99.0") for r in rows]
    _publish_matrix(new, moved, name="matrix_100_v2.csv", run_id="R2")
    rc, text, promo = _check_u14("--new", new, "--old", old)
    assert promo and promo["blocked_by"].get("stale"), \
        f"후보의 _vN 이 blocked_by 에 안 나온다:\n{text[-900:]}"
    assert promo["promotion_eligible"] is False, (rc, text[-500:])


# ── C14 · 명부 (렌즈 2곳) ─────────────────────────────────────────────────────────────────────
def test_f07_the_roster_counts_every_signed_artifact(tmp_path):
    """[C14 · 결론이_바뀜 · sig-완전성 · 공정성-의미]

    `canonical_names` 가 `degeneracy_*`·`matrix_*`·`profile_gamma_*` 세 glob 만 써서, `run_states.sh` 가 게시하고
    `write_meta` 가 서명하는 `ne_shape_*.csv` 가 **명부 밖**이었다 — 실측으로 `out/` 의 서명된 산출 13 개 중
    12 개만 셌다. 숫자가 바뀌어도, 묶음이 미완이어도 게이트가 못 본다.
    `WORKING_STATE.md` 의 승격 계약 "명부 12/12" 가 실은 13 중 12 였다.

    닫힘 조건: 명부는 **`.meta.json` 이 있는 산출 전부** (허용목록 → 배제목록).
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    import check_u14 as C
    signed = sorted(p.name[:-len(".meta.json")] for p in (ROOT / "out").glob("*.meta.json"))
    roster = sorted(C.canonical_names(ROOT / "out"))
    assert set(signed) == set(roster), f"서명됐지만 명부 밖: {sorted(set(signed) - set(roster))}"


# ── C16 · sig (공정성-의미) ───────────────────────────────────────────────────────────────────
def _degeneracy(d: pathlib.Path, run_id="R", **over):
    """서명된 degeneracy 묶음 하나 — `check_degeneracy` 를 실제로 통과하는 모양이어야 한다."""
    ci, rci = _receipt(), _receipt(half="5")
    j = {"state": "100", "si_source": "Li", "half_cell": "GITT", "w_dqdv": 0.0,
         "tol_percent_of_best": 1.0, "n_starts": 2, "seed": 0, "n_grid": 21, "n_samples": 10,
         "run_id": run_id, "env": {"python": "3.11.0", "numpy": "1.26.0", "scipy": "1.11.0",
                                   "pandas": "2.0.0", "platform": "linux-x"},
         "consumed_inputs": ci, "ref_consumed_inputs": rci, "inputs_sha": S.inputs_digest(ci),
         "n_accepted": 3, "best_obj": 1.0, "best_p": [1.0] * 5, "ref_p": [1.0] * 5,
         "best_modes_percent": {"LAM_PE": 1.0}, "LAM_PE_percent": 1.0, "LAM_NE_percent": 1.0,
         "LLI_percent": 1.0}
    j.update(over)
    d.mkdir(parents=True, exist_ok=True)
    f = d / "degeneracy_100_Li.json"
    f.write_text(json.dumps(j, ensure_ascii=False), encoding="utf-8")
    _meta(f, run_id=run_id)
    return f, j


def test_f08_a_candidate_that_omits_its_own_receipt_is_not_amnestied(tmp_path):
    """[C16 · 숫자가_바뀜 · 공정성-의미]

    `inputs_uncomparable` 은 "정본이 옛 스키마인 것은 새 산출의 계약 위반이 아니다" 라는 이유로 rc 를 안 바꾼다.
    그런데 **새 산출 쪽** 누락도 같은 가지로 흘러 rc 0 이었다 — `who` 문자열은 맞는데 등급이 틀렸다.

    반례는 `ref_consumed_inputs: {}` 다: `schema.check_degeneracy` 가 `and j.get(...)` 로 **빈 dict 를 falsy 로**
    건너뛰어 스키마도 통과시킨다 (R9 Codex 가 같은 자리를 이미 지적했다).

    닫힘 조건: candidate 쪽 누락은 계약 위반(rc 2)이고, 사면은 baseline 쪽에만.
    """
    old, new = tmp_path / "old", tmp_path / "new"
    _degeneracy(old, run_id="R1")
    _, j = _degeneracy(new, run_id="R2", ref_consumed_inputs={})
    # ⚠ Codex R13 P1-2: 전 판은 "스키마가 먼저 막으면 이 축을 못 잰다" 를 **fixture 조건으로 고정**했다 —
    #   그 전제 자체가 구멍이었다 (빈 reference 를 스키마가 안 막았다). 이제 스키마가 **먼저** 막고,
    #   그 뒤에 CLI 도 같은 판정을 내는지 둘 다 본다.
    schema_says = S.check_degeneracy(j)
    assert any("ref_consumed_inputs" in x for x in schema_says), \
        f"빈 reference 를 스키마가 안 막는다 (Codex R13 P1-2): {schema_says}"
    rc, text, promo = _check_u14("--new", new, "--old", old)
    assert rc == 2, f"새 산출이 자기 receipt 를 안 적었는데 rc {rc} 다:\n{text[-900:]}"
    assert promo and promo["promotion_eligible"] is False

    # 대조군: **정본**이 안 적은 것은 사면이다 (rc 는 그대로, 승격 자격만 없다)
    o2, n2 = tmp_path / "o2", tmp_path / "n2"
    _degeneracy(o2, run_id="R1", ref_consumed_inputs={})
    _degeneracy(n2, run_id="R2")
    rc2, text2, promo2 = _check_u14("--new", n2, "--old", o2)
    assert promo2 and promo2["blocked_by"].get("inputs_uncomparable"), text2[-700:]
    assert promo2["promotion_eligible"] is False


# ── C04 · R11 P1-3 의 후속 (렌즈 3곳 독립 재현) ───────────────────────────────────────────────
def _prof_rows(gammas, roster):
    ci, rci = _receipt(), _receipt(half="5")
    out = []
    for g in gammas:
        v = {k: "1.0" for k in S.PROFILE_ROW}
        v.update(gamma_Si=str(g), run_id="R", bounds="-", profile_scale="global",
                 consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(rci),
                 inputs_sha=S.inputs_digest(ci), ref_inputs_sha=S.inputs_digest(rci),
                 gamma_roster=json.dumps(roster))
        out.append({k: v[k] for k in S.PROFILE_ROW})
    return out


def test_f09_gamma_roster_is_bound_to_the_body_not_just_self_consistent(tmp_path):
    """[C04 · 결론이_바뀜 · sig-완전성 · validator-우회 · 공정성-의미]

    `check_gamma_roster` 가 자기 안의 산술(`succeeded + |missing| == requested`)과 `authority == 21` 만 봤다.
    본문과 대보는 줄이 하나도 없어서:
      · 행 3 개인데 `{"authority":21,"requested":3,"succeeded":3,"missing":[]}` → 문제 0 (좁힌 실행이 정본 자리로)
      · 행 21 개인데 `succeeded: 1 · missing 20` → 문제 0
      · roster 가 "γ=0.5 는 실패했다" 는데 본문에 γ=0.5 행이 **있다** → 문제 0
      · `requested=True`(bool)도 정수로 셌다 (`isinstance(True, int)`)

    R11 P1-3 의 방어는 producer(`cmd_profile` 의 `grid_subset`) **한 자리뿐**이었고, canonical 자리에 놓인
    1 행짜리 profile 을 게이트는 21 점 정본과 구별하지 못했다.

    닫힘 조건: roster 를 본문에 묶는다 — `requested == authority`(canonical 주장) · `succeeded == len(rows)` ·
    `missing` 이 본문 γ 와 겹치지 않음 · bool 은 개수가 아니다.
    """
    n = S.CANONICAL_GAMMA_GRID_N
    # ⚠ Codex R13 P1-1: 전 판의 "정직한 전수" 는 `i/(n-1)` = 0~1 이었다. 정본 격자는 0~0.5 다 —
    #   개수만 맞는 가짜 대조군이었고, 그래서 구성원 검사가 없다는 사실이 이 시험에 가려져 있었다.
    ok = _prof_rows(S.canonical_gamma_grid(),
                    {"authority": n, "requested": n, "succeeded": n, "missing": []})
    assert not S.check_rows("profile", ok, list(S.PROFILE_ROW)), "대조군(정직한 전수)이 막혔다"

    narrow = _prof_rows([0.0, 0.25, 0.5], {"authority": n, "requested": 3, "succeeded": 3, "missing": []})
    assert S.check_rows("profile", narrow, list(S.PROFILE_ROW)), "좁힌 격자가 canonical 주장으로 통과했다"

    lying = _prof_rows([0.0, 0.5, 1.0], {"authority": n, "requested": n, "succeeded": n - 1, "missing": [0.5]})
    assert S.check_rows("profile", lying, list(S.PROFILE_ROW)), "성공 수·누락 목록이 본문과 어긋나는데 통과했다"

    boolean = _prof_rows([0.0], {"authority": n, "requested": True, "succeeded": True, "missing": []})
    assert S.check_rows("profile", boolean, list(S.PROFILE_ROW)), "bool 을 개수로 셌다"


# ── C05 · R11 P1-2 의 후속 (렌즈 2곳) ─────────────────────────────────────────────────────────
def test_f10_matrix_seals_its_population_like_profile_does(tmp_path):
    """[C05 · 결론이_바뀜 · validator-우회 · 공정성-의미]

    profile 은 `gamma_roster` 를 **행마다** 봉인하는데 matrix 의 `combo_roster` 는 stdout `SUMMARY` 한 줄에만
    있었다 (`grep -rn combo_roster` → `verify.py` 한 줄, 소비자 0). 그래서 `out/matrix_300_0147.csv` 의 분모가
    32 가 아니라 16 인 이유(`D.HALF_CELL_ABSENT`)를 산출물만 봐서는 알 수 없고, 2/32 행 묶음을 canonical
    자리에 놓아도 게이트는 "전부 갖췄다" 였다. R10 P1-3 이 profile 에 세운 원칙("사라지는 stdout 요약이 아니라
    검증되는 묶음이 스스로 말한다")이 matrix 에는 적용되지 않았다.

    닫힘 조건: matrix 행도 자기 모집단을 봉인하고(`combo_roster`), 그 주장이 본문과 맞는지 본다.
    """
    assert "combo_roster" in S.MATRIX_ROW, "matrix 행에 모집단 주장이 없다"
    ci, rci = _receipt(), _receipt(half="5")
    def row(si, roster):
        return matrix_row(si=si, w_dqdv="0", run_id="R", combo_roster=json.dumps(roster),
                          consumed_inputs=json.dumps(ci), ref_consumed_inputs=json.dumps(rci),
                          inputs_sha=S.inputs_digest(ci), ref_inputs_sha=S.inputs_digest(rci))
    good = {"authority": 2, "requested": 2, "succeeded": 2, "missing_input": [], "failed": [], "absent": []}
    ok = [row("Li", good), row("Kunz", good)]
    assert not S.check_rows("matrix", ok, list(S.MATRIX_ROW)), S.check_rows("matrix", ok, list(S.MATRIX_ROW))
    narrow = [row("Li", {"authority": 32, "requested": 2, "succeeded": 2, "missing_input": [],
                         "failed": [], "absent": []})]
    assert S.check_rows("matrix", narrow, list(S.MATRIX_ROW)), "2/32 묶음이 canonical 주장으로 통과했다"
    lying = [row("Li", dict(good, succeeded=99))]
    assert S.check_rows("matrix", lying, list(S.MATRIX_ROW)), "성공 수가 본문과 어긋나는데 통과했다"


# ── C06 · R11 P1-8 의 후속 (validator-우회) ───────────────────────────────────────────────────
def test_f11_non_finite_scientific_values_are_caught_as_strings_too(tmp_path):
    """[C06 · 결론이_바뀜 · validator-우회]

    `_finite_problems` 가 `str` 에 대해 `return []` 이라, 손으로 쓴 degeneracy JSON 의 `best_obj = "1e999"` ·
    `"Infinity"` · `"nan"` · `"not-a-number"` 가 전부 문제 0 이었다. CSV 쪽은 `float()` 로 강제 파싱하는데
    JSON 쪽만 비대칭이었다. `_num_diff` 도 `float()` 를 쓰므로 양쪽 다 `"1e999"` 면 `inf == inf` 로 숫자 차이도
    0 이다 — P1-8 이 닫았다고 적은 산출 부류(리뷰어의 `degeneracy_infinity` probe 와 같은 것)가 다시 통과했다.

    닫힘 조건: 문자열도 CSV 와 같은 규칙으로 — `float()` 로 파싱되면 유한해야 한다.
    """
    for bad in ("1e999", "-1e999", "Infinity", "nan", "NaN", "inf"):
        assert S._finite_problems(bad, "best_obj"), f"{bad!r} 를 통과시켰다"
    for bad in ("1e999", float("nan")):
        assert S._finite_problems({"best_obj": bad}, "degeneracy"), f"중첩된 {bad!r} 를 통과시켰다"
        assert S._finite_problems([1.0, bad], "best_p"), f"목록 안 {bad!r} 를 통과시켰다"
    # 대조군: 유한한 문자열과 숫자 아닌 문자열(라벨)은 문제가 아니다
    assert not S._finite_problems("1.5", "best_obj")
    assert not S._finite_problems("GITT", "half_cell")


# ── C07 · R11 P1-10 B 의 후속 (순서-TOCTOU) ───────────────────────────────────────────────────
def test_f12_instrument_sealing_bypasses_checkout_filters_like_the_snapshot_does(tmp_path):
    """[C07 · 결론이_바뀜 · 순서-TOCTOU]

    R11 P1-10 B 를 닫으면서 `verify_snapshot_bytes` 에는 `--no-filters` 를 줬는데 바로 위 `instrument_sealed` 에는
    안 줬다 — **한쪽만 닫은 비대칭**이다. committed `.gitattributes` + `clean` 드라이버 하나면 디스크에 주입 코드가
    든 러너가 `ok` 로 봉인되고 그 코드가 실제로 돈다 (렌즈가 marker 를 실행시킨 채 `evidence_eligible: true` ·
    `instrument_sealed: true` · `closed: true` 를 받아냈다).

    닫힘 조건: 도구 봉인도 snapshot 검증과 **같은 플래그**로 — index·filter 를 안 거치는 bytes 를 댄다.
    """
    src = (ROOT / "reviews/evidence_gate.py").read_text(encoding="utf-8")
    seal = src[src.index("def instrument_sealed"):src.index("def index_skip_flags")]
    assert "--no-filters" in seal, "instrument_sealed 이 filter 를 거친 hash-object 를 쓴다 (C07)"


# ── C08 · R11 P1-10 A 의 후속 (순서-TOCTOU) ───────────────────────────────────────────────────
@pytest.mark.parametrize("runner", ["reviews/r7_repros/replay_codex_r7.py",
                                    "reviews/r9_repros/replay_codex_r9.py",
                                    "reviews/r10_repros/replay_codex_r10.py",
                                    "reviews/r11_repros/replay_codex_r11.py"])
def test_f13_runners_isolate_sys_path_before_any_import(runner):
    """[C08 · 결론이_바뀜 · 순서-TOCTOU]

    P1-10 A 는 **bytecode 캐시**만 앞으로 옮겼다. 그보다 먼저 러너의 `import argparse, …, traceback` 줄이 돌고,
    `sys.path[0]` 은 러너가 든 **저장소 안 디렉터리**다 — untracked `traceback.py` 하나면 gate 보다 먼저 실행되고
    `INSTRUMENT` 두 파일 밖이라 봉인에 안 걸린다. 렌즈 실측: 러너가 그 파일을 `dirty_paths` 에 찍으면서
    `evidence_eligible: true` 를 냈고, shim 이 gate 를 `sys.modules` 에 선주입하면 **tracked 러너가 수정된 채로도**
    `dirty_paths: []` · `instrument: ok` · eligible true 였다. 가릴 수 있는 이름이 35 개쯤 된다.

    닫힘 조건: 봉인을 import 보다 **앞**에 둔다 — `-P`(sys.path[0] 삽입 끔) · `-E` 로 한 번 재실행한다.
    """
    src = (ROOT / runner).read_text(encoding="utf-8")
    head = src[:src.index("import evidence_gate")]
    assert "safe_path" in head and "os.execv" in head, \
        f"{runner}: gate import 전에 sys.path[0] 를 끄고 재실행하지 않는다 (C08)"


# ── C09 · 같은 축의 production (순서-TOCTOU) ──────────────────────────────────────────────────
def test_f14_write_meta_heredoc_does_not_import_from_the_cwd():
    """[C09 · 결론이_바뀜 · 순서-TOCTOU]

    `write_meta` 의 heredoc 은 `python3 - <<…` 라 `sys.path[0]` 이 `''`(cwd) 다. 저장소 루트의 untracked
    `hashlib.py` 가 `from provenance import …` 보다 **먼저** 실행되고, 그것이 `provenance` 를 선주입하면 meta 에
    `git_dirty: false` · `git_modified_code: []` 가 찍힌다 — 실제로 untracked 코드가 돌았는데도. `check_u14` 의
    `SAFE_PROVENANCE` 가 바로 그 값을 승격 조건으로 읽으므로 R11 P1-9 반례가 그대로 다시 열린다.

    닫힘 조건: production heredoc 을 `-I -P` 로 부른다 (격리 모드 + cwd 를 path 에 안 넣음).
    """
    sh = (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8")
    bad = [ln for ln in sh.splitlines() if "python3 - " in ln and "-P" not in ln]
    assert not bad, f"cwd 에서 import 하는 heredoc 이 남아 있다: {bad}"


# ── C29 · R11 P2-2 의 후속 (순서-TOCTOU) ──────────────────────────────────────────────────────
def test_f15_shape_result_run_id_comes_from_the_process_not_from_the_meta():
    """[C29 · 서술만_바뀜 · 순서-TOCTOU]

    원장은 `shape_step` 이 `rc ↔ status ↔ namespace ↔ run_id` **네 축**을 댄다고 적었는데, producer 가 run_id 를
    `<artifact>.meta.json` 에서 **읽어서** 보고하고 wrapper 가 같은 파일을 다시 읽어 비교한다 — 항진명제다.
    그 축은 아무것도 재지 않는다.

    닫힘 조건: producer 가 **자기 프로세스가 만든 id** 를 보고한다 (그래야 meta 와의 대조가 실제 대조다).
    """
    import ast
    tree = ast.parse((ROOT / "scripts/ne_shape.py").read_text(encoding="utf-8"))
    dicts = [n for n in ast.walk(tree) if isinstance(n, ast.Dict)
             and any(isinstance(k, ast.Constant) and k.value == "status" for k in n.keys)
             and any(isinstance(k, ast.Constant) and k.value == "run_id" for k in n.keys)]
    assert dicts, "SHAPE_RESULT payload 를 못 찾았다"
    for d in dicts:
        value = next(v for k, v in zip(d.keys, d.values)
                     if isinstance(k, ast.Constant) and k.value == "run_id")
        reads = [n for n in ast.walk(value) if isinstance(n, ast.Attribute)
                 and n.attr in ("read_text", "read_bytes", "loads", "load", "open")]
        assert not reads, f"SHAPE_RESULT 의 run_id 가 파일을 다시 읽는다 ({[n.attr for n in reads]}) — 항진명제다 (C29)"


# ── C31 · 죽은 코드 (순서-TOCTOU) ─────────────────────────────────────────────────────────────
def test_f16_the_bootstrap_helper_has_a_caller_or_does_not_exist():
    """[C31 · 사소 · 순서-TOCTOU] `gate.bootstrap_pycache()` 는 "한 자리에 두려고" 만들었는데 호출자가 0 이었고,
    네 러너가 같은 4 줄을 손으로 베껴 쓰고 있었다 — 다섯 번째 러너가 그 줄을 빠뜨리면 P1-10 A 가 거기서만 다시
    열린다. 있으면 쓰고, 안 쓸 거면 없앤다."""
    gate_src = (ROOT / "reviews/evidence_gate.py").read_text(encoding="utf-8")
    if "def bootstrap_pycache" not in gate_src:
        return                                          # 없앴다 — 그것도 닫힘이다
    callers = subprocess.run(["grep", "-rln", "bootstrap_pycache", "--include=*.py", str(ROOT)],
                             capture_output=True, text=True).stdout.split()
    assert len([c for c in callers if not c.endswith("evidence_gate.py")
                and not c.endswith("test_r12_selfreview.py")]) > 0, "정의만 있고 호출자가 없다 (C31)"


# ── C10 · archive-이식성 ──────────────────────────────────────────────────────────────────────
def test_f17_line_endings_are_pinned_for_every_tracked_file():
    """[C10 · 결론이_바뀜 · archive-이식성]

    `.gitattributes` 가 `*.sh`·`*.py`·`*.csv`·`*.json` 만 `eol=lf` 로 덮어서, `core.autocrlf=true`(git for Windows
    설치 기본값) 체크아웃에서는 나머지 **121/415 파일**(`.md`, codex 밖 `.txt`, `.gitattributes` 자신)이 CRLF 로
    풀렸다. R11 P1-10 B 로 넣은 `verify_snapshot_bytes` 가 그것을 잡아 재생기 **넷이 전부 rc 2** 였다 —
    `git status` 는 0 줄인데 증거가 하나도 안 나온다. R12 요청문의 재현 절차는 옵션 없는 `git clone` 이고,
    `.gitattributes:1` 에는 리뷰어가 Windows autocrlf 작업사본을 쓴다고 우리가 직접 적어 뒀다.

    닫힘 조건: catch-all 로 전 파일의 줄끝을 고정한다 (`reviews/*/codex/** -text` 는 뒤에 있으므로 그대로 이긴다).
    """
    attrs = (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
    live = [l for l in attrs if l.strip() and not l.lstrip().startswith("#")]
    assert live and live[0].split() == ["*", "text=auto", "eol=lf"], \
        f"첫 줄이 catch-all 이 아니다: {live[:1]}"
    assert any(l.startswith("reviews/*/codex/**") and "-text" in l for l in live), \
        "보관 패키지의 -text 예외가 catch-all 뒤에 있어야 한다"
    assert live.index(next(l for l in live if l.startswith("reviews/*/codex/**"))) > 0


# ── C11 · R10 P2-1 의 후속 (렌즈 3곳 독립 재현) ───────────────────────────────────────────────
def test_f18_a_non_promotable_result_is_not_exit_zero(tmp_path):
    """[C11 · 결론이_바뀜 · 공정성-의미 · validator-우회 · 파생-보고서]

    `rc 0` 인데 `promotion_eligible: false` 인 경로가 둘(`inputs_uncomparable`·`baseline_absent`) 생겼는데,
    `WORKING_STATE.md` 의 U18 런북은 문자 그대로 **"0 이었을 때만 정본 교체"** 다. 실제 `out/` 을 baseline 으로 한
    12/12 대조가 정확히 그 상태를 낸다 (`inputs_uncomparable: 16`) — **오늘 U18 을 돌리면 승격 경로가 전부 여기로
    온다.** R10 P2-1 이 subset 에 대해 닫은 축("글자로만 말하면 자동 소비자가 구분 못 한다 → 종료 코드로 가른다")이
    다시 열렸다.

    닫힘 조건: 승격 불가는 rc 0 이 아니다 — 계약이 안 깨졌지만 승격 못 하는 상태에 전용 코드(4)를 준다.
    """
    old, new = tmp_path / "old", tmp_path / "new"
    rows = seal_combo(_rows_per_si("a", "a"))
    # 옛 스키마 정본: 출처 열 자체가 없다 (현행 `out/` 이 정확히 이 모양이다 — 그래서 U18 대조가 전부 이리로 온다)
    old.mkdir(parents=True, exist_ok=True)
    cols = [c for c in S.MATRIX_ROW if c not in ("consumed_inputs", "ref_consumed_inputs",
                                                 "inputs_sha", "ref_inputs_sha")]
    verify.atomic_write_csv(old / "matrix_100.csv",
                            [{c: dict(r, run_id="R1")[c] for c in cols} for r in rows], cols)
    _meta(old / "matrix_100.csv", run_id="R1")
    _publish_matrix(new, rows, run_id="R2")
    rc, text, promo = _check_u14("--new", new, "--old", old)
    assert promo and promo["promotion_eligible"] is False, text[-500:]
    assert rc != 0, f"승격 불가인데 rc 0 이다 — 런북이 이 코드로 정본을 교체한다:\n{text[-700:]}"

    # `--schema-only` 는 **승격을 묻지 않은** 진단이다 — 스키마가 깨끗하면 rc 0 이되 증명서는 아니다 (R11 P1-6).
    #   물어보지 않은 것에 "자격 없음" 코드를 주면 스키마 점검 도구로 못 쓴다.
    rc2, text2, promo2 = _check_u14("--new", new, "--schema-only")
    assert promo2 and promo2["promotion_eligible"] is False and promo2["blocked_by"]["baseline_absent"], \
        (rc2, text2[-400:])

    # 런북과 docstring 이 그 등급을 말한다
    ws = (ROOT / "WORKING_STATE.md").read_text(encoding="utf-8")
    assert "promotion_eligible" in ws, "런북이 아직 rc 만 보고 승격하라고 한다"


# ── C15 · R8-02 축의 구멍 (validator-우회) ────────────────────────────────────────────────────
def test_f19_shape_step_verifies_the_unit_like_the_other_three_steps():
    """[C15 · 숫자가_바뀜 · validator-우회]

    네 production 단계 중 `shape_step` 만 `verify_unit_or_say`·`check_run_id` 를 안 부르고 `BMS_RUN_ID` 도 안
    줬다 — `read_unit` 이 False("meta 의 run_id 가 산출물과 다르다") 인 섞인 묶음에 `STEP_RC=0` "complete" 가
    나왔다 (같은 묶음을 다른 세 단계의 검사로 보면 rc 1). R8-02 가 닫은 "data B / meta A" 축이 거기만 열려 있었다.

    닫힘 조건: `shape_step` 도 자기 시도의 id 를 주입하고, 대조 뒤 묶음 검사를 부른다.
    """
    sh = (ROOT / "scripts/run_states.sh").read_text(encoding="utf-8")
    body = sh[sh.index("shape_step () {"):sh.index("\nfail=0")]
    assert "BMS_RUN_ID" in body, "shape_step 이 이번 시도의 id 를 주입하지 않는다"
    assert "verify_unit_or_say" in body, "shape_step 이 묶음 검사를 안 부른다"


# ── C18 · sig-완전성 ──────────────────────────────────────────────────────────────────────────
def test_f20_every_signed_env_axis_is_compared():
    """[C18 · 숫자가_바뀜 · sig-완전성] `provenance.env_signature()` 는 pandas 를 적는데 `S.ENV_KEYS` 는
    python·numpy·scipy·platform 만 댔다. 과학 입력이 전부 `pd.read_excel` 로 읽히므로 pandas 는 입력 파싱을
    바꿀 수 있는 축이다 — 서명에 적고 안 대면 그 서명은 무엇을 고정하는지 말할 수 없다."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from provenance import env_signature
    assert set(env_signature()) <= set(S.ENV_KEYS), \
        f"서명에만 있고 비교 축에 없는 것: {sorted(set(env_signature()) - set(S.ENV_KEYS))}"


# ── C19 · 순서-TOCTOU ─────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("runner", ["reviews/r7_repros/replay_codex_r7.py",
                                    "reviews/r9_repros/replay_codex_r9.py",
                                    "reviews/r10_repros/replay_codex_r10.py",
                                    "reviews/r11_repros/replay_codex_r11.py"])
def test_f21_runner_exit_code_reflects_evidence_eligibility(runner):
    """[C19 · 숫자가_바뀜 · 순서-TOCTOU] `evidence_eligible: false` 인 실행이 rc 0 으로 끝났다 — P1-11 이 자식에게
    요구한 "payload 를 읽기 전에 rc 를 본다" 를 러너 자신이 어긴다 (기록된 증거 다섯 개가 전부 꼬리에 `rc=0` 을
    달고 있다). 증거가 아닌 실행은 성공 코드로 끝나면 안 된다."""
    import ast
    tree = ast.parse((ROOT / runner).read_text(encoding="utf-8"))
    main = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "main")
    # main 의 **마지막 return** 까지 오는 길에 evidence_eligible 로 갈라지는 분기가 있어야 한다
    guards = [n for n in ast.walk(main) if isinstance(n, ast.If)
              and any(isinstance(x, ast.Constant) and x.value == "evidence_eligible"
                      for x in ast.walk(n.test))]
    assert guards, f"{runner}: 종료 코드가 evidence_eligible 을 안 본다 (C19)"


# ── C33 · sig-완전성 ──────────────────────────────────────────────────────────────────────────
def test_f22_scale_audit_is_not_invisible_in_both_directions():
    """[C33 · 서술만_바뀜 · sig-완전성] `scale_audit_*` 가 `MAY_BE_EMPTY` 와 `ROW_SKIP` **양쪽**에 있어서,
    정본에는 R5-06 의 동치 감사가 있고 재실행에는 빈 칸이어도 "전부 같다 · rc 0 · promotion true" 였다.
    한쪽 carve-out 은 이유가 있어도 둘 다면 그 열은 존재하지 않는 것과 같다."""
    both = set(S.MAY_BE_EMPTY) & S.ROW_SKIP
    assert not both, f"빈 칸도 허용되고 비교에서도 빠지는 열: {sorted(both)}"


# ── C24 · 파생-보고서 · 순서-TOCTOU ───────────────────────────────────────────────────────────
def test_f23_recorded_evidence_json_is_valid_json():
    """[C24 · 사소 · 파생-보고서 · 순서-TOCTOU] 증거 생성 스크립트가 `echo "rc=$?" >> $D/$name` 을 `.json` 에도
    붙여, 기록된 재생기 결과 다섯 개가 `json.load()` 에서 `Extra data` 로 죽었다 — 원장이 "전문은 여기" 라고
    가리키는데 기계가 못 읽는다 (수정 **전** 증거 넷은 정상이라 한 디렉터리 안에서 규약이 달랐다)."""
    for f in sorted((ROOT / "reviews").rglob("replay_ours_*/*.json")):
        json.loads(f.read_text(encoding="utf-8"))       # 죽으면 그것이 발견이다


# ── C20 · C22 · C26 · C27 · 파생-보고서 ───────────────────────────────────────────────────────
def test_f24_documents_quote_the_measured_numbers():
    """[C20·C22·C26·C27 · 파생-보고서] 문서 숫자를 실측과 대조한다. 이번에 어긋난 것:
    `R12_REQUEST.md` 의 namespace 분해가 실측과 **반대**(root 6·data 5 → 5·6)였고 같은 문서 안에서
    `6/6`↔`5+1` 로 갈렸으며, 패키지를 "13 파일" 이라 했는데 서명 파일까지 14 개다.
    (`blocked_by.schema` 가 사람용 출력에 없는 합계 52 인 것은 C22 로 따로 쪼갰다.)"""
    req = (ROOT / "reviews/R12_REQUEST.md").read_text(encoding="utf-8")
    ev = ROOT / "reviews/r11_repros/replay_ours_after_fixes/replay_codex_r11.json"
    if ev.is_file():
        d = json.loads(ev.read_text(encoding="utf-8"))
        from collections import Counter
        ns = Counter(k.split(":")[0] for k, v in d["probes"].items() if v["상태"] == "반례 소멸")
        for name, n in ns.items():
            assert f"{name} {n}" in req, f"요청문의 namespace 분해가 실측과 다르다: {name} {n} (실측) — {dict(ns)}"
    pkg = len(list((ROOT / "reviews/r11_repros/codex").glob("*")))
    assert f"패키지 {pkg}" in req or f"{pkg} 파일" in req, f"패키지 파일 수가 실측({pkg})과 다르다"


# ── C23 · 파생-보고서 ─────────────────────────────────────────────────────────────────────────
def test_f25_every_truncated_list_says_it_was_truncated():
    """[C23 · 서술만_바뀜 · 파생-보고서] 보고 블록 13 개 중 **8 개**가 `--max-show` 에서 잘렸다는 표시 없이 잘렸고
    (`… 외 N` 은 5 곳뿐), `stale` 은 `--max-show` 를 무시하고 `[:6]` 하드코딩이었다. 헤더의 개수와 `blocked_by` 는
    맞으므로 거짓말은 아니지만, 목록만 보고 "이게 전부" 라고 읽게 된다."""
    import re
    src = (ROOT / "scripts/check_u14.py").read_text(encoding="utf-8")
    body = src[src.index("def main("):]
    # `[:a.max_show]` 로 직접 자르는 자리가 남아 있으면 그 목록은 표시 없이 잘린다
    raw = [l.strip() for l in body.splitlines() if "[:a.max_show]" in l and "_show(" not in l and "join(" not in l]
    assert not raw, f"helper 를 안 거치고 자르는 자리: {raw}"
    assert body.count("_show(") >= 8, "잘라 찍는 자리를 helper 하나로 모으지 않았다 (C23)"


# ── C17 · R11 P1-7 의 부작용 (렌즈 2곳) ───────────────────────────────────────────────────────
def test_f26_the_shape_reader_reports_a_rejected_matrix_as_a_missing_pair(tmp_path, monkeypatch):
    """[C17 · 숫자가_바뀜 · 공정성-의미 · validator-우회]

    P1-7 로 reader 가 공용 validator 를 쓰게 되면서 현행 정본 `out/matrix_*.csv` 네 개가 전부 RuntimeError 다
    (옛 스키마라 출처 열이 없다). fail-closed 라 거짓 통과는 아니지만 예외가 `main()` 밖으로 나가서 (a) 게시된
    sidecar 에 그 사실이 안 남고 (b) 사용자가 보는 메시지는 "SHAPE_RESULT 를 내지 않았다" 라 **원인을 안 가린다**.

    닫힘 조건: 거부된 matrix 는 그 상태의 **짝 없음**으로 세고 이유를 `pairing` 에 남긴다 → typed status 가
    정직하게 `partial` 로 나오고 wrapper 메시지가 원인을 가리킨다.
    """
    ns = _mod_ne_shape()
    src = (ROOT / "scripts/ne_shape.py").read_text(encoding="utf-8")
    assert "fitted_pair_info" in src
    # 옛 스키마 묶음에서 reader 를 부르면 거부된다 (그것이 이 발견의 전제다).
    # ⚠ U18b 승격(2026-09-14): 그 표본은 이제 정본이 아니라 **얼려 둔 archive** 다 — `out/matrix_*.csv` 는 새 계약이라
    #   거부되지 않는다. 살아 있는 파이프라인 경로에 표본을 두면 재실행 한 번에 전제가 사라진다 (U14-05 와 같은 축).
    legacy = ROOT / "out" / "archive" / "legacy_r6_u14"
    assert (legacy / "matrix_100.csv").is_file(), "옛 스키마 표본이 사라졌다 (조건 7 의 보존 대상)"
    with pytest.raises(RuntimeError, match="공용 스키마 검증 실패"):
        ns.fitted_pair_info(legacy, "100", "GITT", "Li")
    # 그러나 그 예외가 main 밖으로 새지 않고 이유가 남아야 한다
    caller = src[src.index("def main("):]
    assert "fitted_pair_info" in caller and "except RuntimeError" in caller, \
        "reader 의 거부를 main 이 잡아 이유를 남기지 않는다 (C17)"


def _mod_ne_shape():
    import importlib.util
    spec = importlib.util.spec_from_file_location("r12_ne_shape", ROOT / "scripts/ne_shape.py")
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ROOT / "scripts"))
    spec.loader.exec_module(m)
    return m


# ── C30 · 순서-TOCTOU ─────────────────────────────────────────────────────────────────────────
def test_f27_the_evidence_child_gets_its_own_bytecode_prefix():
    """[C30 · 서술만_바뀜 · 순서-TOCTOU] R11 러너가 evidence 자식의 env 에서 `PYTHONPYCACHEPREFIX` 를 **벗겨** 그
    probe 들이 자기 기법(위조 pyc)을 쓸 수 있게 했는데, 그 결과 실행이 끝난 snapshot 에 `__pycache__` 7 개가
    남는다 — P1-10 A 가 쓰던 바로 그 자리(`reviews/__pycache__/`)를 포함해서. 벗기지 말고 **다른** 임시 prefix 로
    바꾼다 (probe 의 기법은 그대로 성립하고 우리 자리는 안 더럽힌다)."""
    src = (ROOT / "reviews/r11_repros/replay_codex_r11.py").read_text(encoding="utf-8")
    assert "NEEDS_DEFAULT_PYCACHE" in src, "기본 자리를 요구하는 case 를 따로 두지 않는다 (C30)"
    assert "ev_env_isolated" in src and "mkdtemp(prefix=\"evidence-child-pycache-\")" in src, \
        "나머지 자식에게 우리 임시 prefix 를 주지 않는다 (C30)"


# ── C35 · archive-이식성 ──────────────────────────────────────────────────────────────────────
def test_f28_the_replayer_workspace_never_lives_inside_the_tree():
    """[C35 · 사소 · archive-이식성] R11 재생기가 보관 패키지의 상대 경로를 맞추려고 트리 **안에** 자기참조
    symlink 를 만들었다. `finally` 는 파이썬 예외만 덮으므로 SIGTERM 이면 남고, 이번에 넣은 `.gitignore` 규칙이
    그것을 `git status` 에서 감춘다 — 그 뒤 `copytree` 를 쓰는 probe 들이 무한 재귀로 터진다 (실측).
    R9 러너처럼 workspace 를 `tempfile.mkdtemp()` 에 두면 트리에 아무것도 안 남는다."""
    src = (ROOT / "reviews/r11_repros/replay_codex_r11.py").read_text(encoding="utf-8")
    assert "PKG.parent / WSL_REL" not in src, "트리 안에 workspace 를 만든다 (C35)"
    assert "mkdtemp" in src and "WSL_REL" in src
