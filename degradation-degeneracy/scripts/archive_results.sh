#!/usr/bin/env bash
# =============================================================================
#  archive_results.sh — 계산 결과를 **외부 clone에서 검증 가능한** 형태로 남긴다
#
#  사용:
#    ./scripts/archive_results.sh                      # 기본 실행 보관
#    ./scripts/archive_results.sh results/halfcell_v3  # 특정 실행만
#
#  왜 필요한가
#  ───────────
#  .gitignore가 results/ 와 *.parquet 을 통째로 제외한다. 용량 때문에 맞는
#  기본값이지만, 그 결과 **계산 결과가 서버에만 존재**하게 된다.
#  V100 컨테이너가 회수되면 fitting 14시간이 사라진다.
#
#  ★ F62 — 무엇을 남길지의 기준이 바뀌었다
#  ───────────────────────────────────────
#  초판의 기준은 "재생성 비용"이었다. 그래서 curves.parquet(재생성 5~8분)을
#  버렸다. 그런데 validate_provenance 는 봉인된 입력을 **다시 해시**한다 (F56).
#  재생성한 curves는 바이트가 달라서 digest가 안 맞는다 — 재생성으로 대체할 수
#  없다. manifest_start.yaml 과 attempts/ 도 마찬가지로 검증기가 디스크에서
#  직접 읽는다 (F57). half-cell 캐시는 .cache/ 가 gitignore라 저장소에 아예 없다.
#
#  즉 기준은 이제 "**clone 한 사람이 이 결과를 검증할 수 있는가**"다.
#  검증에 필요한 것은 비용과 무관하게 전부 남긴다.
#
#    fits.parquet          ★ 조건당 4~10초 × 3,069조건 = 시간 단위
#    manifest.yaml         ★ 서명·run_spec·입력 digest
#    manifest_start.yaml   ★ F57 — 검증기가 디스크에서 읽어 대조한다
#    attempts/*.yaml       ★ F57 — attempt_id 별 시작 기록
#    curves.parquet        ★ F56 — 재생성 불가(바이트가 달라진다). 19 MB지만 남긴다
#    inputs/*_ocp.json     ★ half-cell 캐시. .gitignore 때문에 동봉해야 한다
#    *_summary.yaml, 비교표, figures/*.png    작고 보고서가 읽는다
#
#    degeneracy_map / chunks / completed.jsonl   버린다 (fits에서 재생성)
#
#  복원 — 묶음은 보관 형태이고, 검증은 복원한 뒤에 한다:
#    python -m tools.archive_bundle restore artifacts/halfcell_fit_v4
# =============================================================================
set -uo pipefail   # ★ 개별 실행 실패를 집계해야 하므로 -e 는 쓰지 않는다

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PY="${PYTHON:-python3}"
# ★ 11차 — 보관 위치는 override 가능하다. smoke 의 음성 테스트가 **tracked**
#   artifacts/ 를 건드리면 worktree 가 dirty 가 되어 strict smoke 의 전제
#   (clean 커밋에서 실행)를 스스로 깬다.
DEST="${ARCHIVE_DEST:-artifacts}"
RUNS=("$@")
if [[ ${#RUNS[@]} -eq 0 ]]; then
  # ★ F71/8-4 — 기본 대상이 옛 v1/v2 여서, 새 실행을 묶으려던 사람이 무심코
  #   실행하면 quarantine 산출물만 다시 묶였다. 현재 pipeline 의 구조를 따른다.
  # ★ 13차 발견 4 — 기본 대상이 v3 로 남아 있으면 새 v4 수치 대신 옛 묶음을
  #   인용하게 된다 (계산 blocker 는 아니지만 최종 citation blocker).
  RUNS=(results/grid_curves_v4 results/grid_fit_v4 results/halfcell_fit_v4
        results/paired_fixed5_v4)
fi

mkdir -p "$DEST"
# ★ 13차 발견 8 — 이전 실행이 중단되면 `.previous_*`/`.candidate_*` 가 남아
#   다음 `git add artifacts` 에 옛 중복 묶음이 들어갈 수 있다. 시작 시 정리하되,
#   본 묶음이 사라진 상태면 `.previous_*` 를 **복구**한다 (중단 내구성).
for _prev in "$DEST"/.previous_*; do
  [[ -e "$_prev" ]] || continue
  _base="$(basename "$_prev")"; _base="${_base#.previous_}"; _base="${_base%.*}"
  if [[ -d "$DEST/$_base" ]]; then
    echo "정리: 중단된 실행의 잔여 $_prev 삭제"
    rm -rf "$_prev"
  else
    echo "복구: 중단된 승격을 되돌립니다 $_prev → $DEST/$_base"
    mv "$_prev" "$DEST/$_base"
  fi
done
rm -rf "$DEST"/.candidate_*

n_ok=0
n_bad=0
n_missing=0
n_want=${#RUNS[@]}
promoted=()          # ★ 12차 발견 5-c — 이번에 검증·승격한 묶음만 index 에 넣는다

for run in "${RUNS[@]}"; do
  name="$(basename "$run")"
  if [[ ! -d "$run" ]]; then
    # ★ F89/9차 발견 10 — 기본 대상이 **전부 없어도** "검증 가능 0개, 불완전
    #   0개" + exit 0 으로 끝났다. paired 나 producer 가 보관되지 않은 상태를
    #   완료로 오인하게 된다. 요청한 artifact 가 없으면 실패다.
    printf '없음 (보관 대상 누락): %s\n' "$run"
    n_missing=$((n_missing+1))
    continue
  fi
  out="$DEST/$name"

  printf '\n── %s ──\n' "$name"

  # ★ F80/9-a — provenance.json 을 bundle **전에** 원본 실행 디렉터리에 쓴다.
  #   예전에는 bundle 뒤 묶음 안에 추가해서, 방금 만든 payload digest 목록과
  #   즉시 어긋나 **정상 묶음을 스스로 무효화**했다 (리뷰 실측).
  #   KEEP_FILES 에 provenance.json 이 있으므로 bundle 이 알아서 담는다.
  #   grid producer 는 fitting validator 가 아니라 곡선 validator 로 검증한다 (9-e).
  # ★ 11차 발견 6 — 원본이 검증에 실패하면 **거기서 이 run 은 실패**다. 예전에는
  #   출력만 하고 계속 진행해, stale 원본으로 만든 묶음이 기존 정상 묶음을
  #   덮어썼다 (리뷰 실측: wrapper exit 0 + 마지막 정상 archive 소실).
  if ! "$PY" - "$run" <<'PYEOF'
import json, sys
from pathlib import Path
from src.io import validate_curves_provenance, validate_provenance
from tools.archive_bundle import artifact_kind
run = Path(sys.argv[1])
v = (validate_curves_provenance(run) if artifact_kind(run) == "grid_producer"
     else validate_provenance(run))
(run / "provenance.json").write_text(
    json.dumps(v, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"  원본 provenance: {'통과' if v['ok'] else '실패 — ' + ', '.join(v['fail'][:4])}")
sys.exit(0 if v["ok"] else 1)
PYEOF
  then
    echo "  → 원본이 인용 가능한 상태가 아니라 보관하지 않습니다 (기존 묶음 유지)"
    n_bad=$((n_bad+1))
    continue
  fi

  # ★ 18차 발견 6 — 바이트 무결성만으로는 파생 YAML 이 **최신 의미**를 담는지
  #   증명하지 못한다. v4 에서 실제로 경계 규약 수정 이전 값이 묶음에 들어갔다.
  #   봉인 fits 에서 재계산해 대조하고, 다르면 이 run 은 승격하지 않는다.
  if ! "$PY" -m tools.check_derived_fresh "$run"; then
    echo "  → 파생 산출물이 stale 이라 보관하지 않습니다 (기존 묶음 유지)"
    n_bad=$((n_bad+1))
    continue
  fi

  # ★ 11차 발견 6 — candidate 에 만들고 **전부 통과한 뒤에만** 교체한다.
  #   bundle 종료 코드도 반드시 집계한다 (예전에는 무시하고 ok=1 로 시작했다).
  cand="$DEST/.candidate_$name"
  rm -rf "$cand"
  ok=1
  "$PY" -m tools.archive_bundle bundle "$run" "$cand" || ok=0
  [[ "$ok" == "1" ]] || echo "  bundle 실패 (봉인 불일치 등) — 기존 묶음 유지"

  if [[ "$ok" == "1" ]]; then
    "$PY" -m tools.archive_bundle check "$cand" | sed 's/^/  /' || ok=0
  fi

  # ★ F71 — **격리 복원 검증까지 자동으로 한다.** 원본 results/ 가 남아 있는
  #   서버에서 restore→validate 하면 묶음을 전혀 확인하지 않고 원본을 다시
  #   검증할 수 있다 (8-3). 빈 임시 root 에 풀어서 거기서 검증한다.
  # 원래 상대경로 그대로 격리 root 안에 푼다 — 봉인된 입력 경로가 저장소 root
  # 기준이므로 (F65), run_dir 을 임의로 바꾸면 재해시가 어긋난다.
  if [[ "$ok" == "1" ]]; then
    iso="$(mktemp -d)"
    if "$PY" -m tools.archive_bundle restore "$cand" --repo-root "$iso" >/dev/null 2>&1 \
       && "$PY" - "$iso" "$run" <<'PYEOF' | sed 's/^/  /'
import sys
from pathlib import Path
from src.io import validate_curves_provenance, validate_provenance
from tools.archive_bundle import artifact_kind, nested_runs
iso, run = Path(sys.argv[1]), sys.argv[2]
rd = iso / run
bad = []
for d in [rd] + nested_runs(rd):
    v = (validate_curves_provenance(d) if artifact_kind(d) == "grid_producer"
         else validate_provenance(d, repo_root=iso))
    tag = d.name if d != rd else "본체"
    print(f"격리 복원 검증[{tag}]: "
          + ("통과" if v["ok"] else "실패 — " + ", ".join(v["fail"][:4])))
    if not v["ok"]:
        bad.append(tag)
sys.exit(1 if bad else 0)
PYEOF
    then :; else ok=0; echo "  격리 복원 검증 실패"; fi
    rm -rf "$iso"
  fi

  if [[ "$ok" == "1" ]]; then
    # ★ 12차 — `rm -rf out && mv cand out` 은 두 명령 사이에 중단되면 기존
    #   묶음이 사라진다. 옛 것을 먼저 옆으로 치우고, 새 것을 제자리에 놓은
    #   **뒤에** 지운다 (중단돼도 둘 중 하나는 항상 남는다).
    old=""
    if [[ -d "$out" ]]; then
      old="$DEST/.previous_$name.$$"
      rm -rf "$old"
      # ★ 14차 발견 7 — 첫 이동이 실패한 채 진행하면 뒤의 `mv cand out` 이
      #   기존 묶음 **안으로** candidate 를 중첩시키고 성공(exit 0)으로 끝난다.
      #   실패면 후보를 제거하고 n_bad 로 계상한다 (fail-closed).
      if ! mv "$out" "$old"; then
        echo "  기존 묶음 이동(mv) 실패 — 승격하지 않습니다 (기존 묶음 유지)" >&2
        rm -rf "$cand"
        n_bad=$((n_bad+1))
        continue
      fi
    fi
    if mv "$cand" "$out"; then
      [[ -n "$old" ]] && rm -rf "$old"
    else
      # ★ 13차 발견 8 — 승격이 실패하면 옛 묶음을 되돌린다 (orphan 방지)
      echo "  승격(mv) 실패 — 기존 묶음을 되돌립니다" >&2
      [[ -n "$old" ]] && mv "$old" "$out"
      rm -rf "$cand"
      n_bad=$((n_bad+1))
      continue
    fi
    promoted+=("$name")
    n_ok=$((n_ok+1))
    # ★ 10차 자체 확인 1 / 11차 발견 7 — 진본성 앵커는 **full 64자리**로 남긴다.
    #   payload 목록의 해시 하나가 묶음 전체를 고정한다. 아래 artifact_index.yaml
    #   가 이 값을 커밋되는 형태로 모은다.
    printf '  bundle payload_index_sha256: %s\n' \
      "$(sha256sum "$out/payload_sha256.yaml" | cut -d' ' -f1)"
    printf '  용량 %s\n' "$(du -sh "$out" | cut -f1)"
  else
    rm -rf "$cand"
    n_bad=$((n_bad+1))
    echo "  → 승격하지 않았습니다 (기존 묶음이 있으면 그대로 유지됩니다)"
  fi
done

# ★ 11차 발견 7 — 어느 묶음이 어느 보고서의 근거인지 **자동으로 잇는다.**
#   run 경로 ↔ payload index·fits·curves 의 full 64자리 digest 를 커밋되는
#   목록으로 남긴다. RESULTS.md 의 앵커와 이 파일을 대조하면 된다.
#   승격된 묶음이 하나도 없으면 쓰지 않는다 — 실패한 실행이 인덱스를 건드려
#   "무엇이 근거인가"를 흐리면 안 된다.
if [[ "${#promoted[@]}" -gt 0 ]]; then
"$PY" - "$DEST" "${promoted[@]}" <<'PYEOF'
import hashlib, subprocess, sys
from pathlib import Path
import yaml
from src.io import file_digest
from tools.archive_bundle import artifact_kind
dest, names = Path(sys.argv[1]), sys.argv[2:]

def _sha(p):
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return h.hexdigest()

runs = {}
# ★ 12차 발견 5-c — 이번에 check→격리 복원→validator 를 통과해 **승격한** 것만
#   싣는다 (예전엔 DEST 아래 모든 디렉터리를 무검증으로 순회했다).
for name in names:
    b = dest / name
    pi = b / "payload_sha256.yaml"
    if not pi.is_file():
        continue
    kind = artifact_kind(b)
    ent = {"artifact_kind": kind, "payload_index_sha256": _sha(pi)}
    # ★ 13차 발견 7 — 이 산출물을 **계산한** commit (archive 시점 HEAD 가 아니라).
    #   grid producer 는 curves_manifest 가, fit 은 manifest 가 소유한다.
    # ★ 14차 발견 8 — 그 commit 은 manifest **최상위** git_commit(기록 시점)이
    #   아니라 **계산 시작 커밋**이다: fit 은 서명된 run_spec.git_commit /
    #   start_provenance.git_commit, grid 는 curves_manifest_start.yaml 의
    #   git_commit (시작 기록). 실행 도중 commit 이 움직인 경우는 별도 검사
    #   (git_commit_changed_during_run)가 잡고, 여기는 시작 좌표를 앵커로 쓴다.
    _mm = b / "manifest.yaml"
    _man0 = (yaml.safe_load(_mm.read_text(encoding="utf-8")) or {}) if _mm.is_file() else {}
    ent["source_commit"] = ((_man0.get("run_spec") or {}).get("git_commit")
                            or (_man0.get("start_provenance") or {}).get("git_commit")
                            or _man0.get("git_commit"))
    _cm0 = b / "curves_manifest.yaml"
    if _cm0.is_file():
        _cman0 = yaml.safe_load(_cm0.read_text(encoding="utf-8")) or {}
        _cs0 = b / "curves_manifest_start.yaml"
        _cstart0 = (yaml.safe_load(_cs0.read_text(encoding="utf-8")) or {}) if _cs0.is_file() else {}
        _cc = _cstart0.get("git_commit") or _cman0.get("git_commit")
        if kind == "grid_producer":
            ent["source_commit"] = _cc
        elif _cc and ent.get("source_commit") and _cc != ent["source_commit"]:
            ent["_주의_producer_commit"] = _cc
    rm = b / "restore_map.yaml"
    meta = (yaml.safe_load(rm.read_text(encoding="utf-8")) or {}) if rm.is_file() else {}
    ent["run_dir"] = meta.get("run_dir")
    if (b / "fits.parquet").is_file():
        ent["fits_sha256"] = file_digest(b / "fits.parquet", full=True)
    # ★ 12차 발견 5-a — fit 묶음의 곡선은 root 가 아니라 `inputs/` 에 있다.
    #   manifest 가 서명한 producer curves digest 를 싣고, 동봉된 bytes 를
    #   **재해시해 같은지 확인**한 뒤에만 기록한다.
    mp = b / "manifest.yaml"
    man = (yaml.safe_load(mp.read_text(encoding="utf-8")) or {}) if mp.is_file() else {}
    sealed_curves = ((man.get("run_spec") or {}).get("producer") or {}
                     ).get("curves_sha256")
    local = b / "curves.parquet"
    if not local.is_file():
        for arch_rel, orig in (meta.get("inputs") or {}).items():
            if str(orig).endswith("curves.parquet"):
                local = b / arch_rel
                break
    if local.is_file():
        got = file_digest(local, full=True)
        if kind == "grid_producer" or sealed_curves is None:
            ent["curves_sha256"] = got
        elif got == sealed_curves:
            ent["curves_sha256"] = got
        else:
            ent["curves_sha256"] = None
            ent["_경고"] = (f"동봉 곡선 digest {got[:16]} ≠ 봉인 "
                           f"{str(sealed_curves)[:16]}")
    else:
        ent["curves_sha256"] = sealed_curves
        ent["_주의_곡선"] = "곡선 bytes 가 이 묶음에 없다 (봉인 digest만 기록)"
    runs[name] = ent
# ★ 13차 발견 7 — `source_commit` 은 archive 실행 시점 HEAD 가 아니라 **각
#   산출물을 계산한 commit** 이어야 한다. run 별 manifest.git_commit 을 싣고,
#   전부 같을 때만 top-level 로 축약한다 (다르면 top-level 은 null).
_commits = {n: e.get("source_commit") for n, e in runs.items()}
_uniq = {c for c in _commits.values() if c}
commit = next(iter(_uniq)) if len(_uniq) == 1 else None
if len(_uniq) > 1:
    print(f"  ⚠ 묶음마다 계산 commit 이 다릅니다: {_commits}", file=sys.stderr)
out = dest / "artifact_index.yaml"
# ★ 12차 발견 5-b — 여기 적히는 SHA 는 **계산에 쓴 코드**의 commit 이다.
#   이 파일 자신을 담을 artifact commit 은 아직 존재하지 않으므로 그 이름을
#   쓸 수 없다 (artifact commit A → 이 index 를 갱신하는 commit B 순서).
# ★ 14차 발견 8 — 문구 수정: 실제 워크플로는 `git add artifacts && git commit`
#   **한 번**이라 index 와 묶음은 같은 commit 에 담긴다. 그 commit 의 이름은
#   자기참조라 이 파일 안에 쓸 수 없다 — source_commit(계산 시작 코드 commit)
#   과 혼동하지 말 것.
out.write_text(yaml.safe_dump(
    {"_주의": ("RESULTS.md 의 앵커(fits/curves digest)와 여기 값이 같아야 그 보고서의 "
             "근거 묶음이다. source_commit 은 **계산을 시작한 코드**의 commit 이다. "
             "이 index 와 묶음 bytes 는 `git add artifacts` 로 함께 커밋되며, 그 "
             "artifact commit 의 이름은 자기참조라 여기 쓸 수 없다 (12차 5-b·14차 8)."),
     "source_commit": commit, "runs": runs},
    allow_unicode=True, sort_keys=False), encoding="utf-8")
print(f"\n인덱스: {out} ({len(runs)}개 승격 묶음, full 64자리 digest)")
PYEOF
fi

printf '\n요청 %d개 · 검증 가능 %d개 · 불완전 %d개 · 없음 %d개 · 합계 %s\n' \
  "$n_want" "$n_ok" "$n_bad" "$n_missing" "$(du -sh "$DEST" | cut -f1)"
cat <<'EOF'

다음:
  git add artifacts && git commit -m "chore(artifacts): 계산 결과 보관" && git push

clone 한 쪽에서 복원 + 검증:
  python -m tools.archive_bundle restore artifacts/halfcell_fit_v4
  python -c "from src.io import validate_provenance; import json; \
             print(json.dumps(validate_provenance('results/halfcell_fit_v4'), \
             ensure_ascii=False, indent=2))"
  ./run.sh --mode score --in results/halfcell_fit_v4   # 채점 이후는 몇 초다
EOF

# ★ F71/8-4 — 하나라도 불완전하면 nonzero. 조용히 성공하면 CI·스크립트가
#   "보관됐다"고 믿는다.
[[ "$n_bad" -eq 0 && "$n_missing" -eq 0 ]] || exit 1
