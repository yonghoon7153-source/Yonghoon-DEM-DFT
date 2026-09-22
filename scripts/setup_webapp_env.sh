#!/usr/bin/env bash
# 웹앱 파이썬 환경을 **고친다** (새로 만들지 않는다).
#
# 배경 (2026-09-22): 케이스 260922_092001_0853b1 이 `No module named 'networkx'`
# 로 죽었다.  처음엔 "낡은 인스턴스가 bare python3 로 떠 있다" 로 읽었는데
# 실측(/proc/<pid>/environ)이 반증했다 — 웹앱은 **venv 안에서 정상으로** 돌고
# 있었고, 그 venv 에 networkx 가 없었을 뿐이다.
#
# ⚠⚠ 그래서 이 스크립트의 핵심은 설치가 아니라 **두 개의 안전장치**다:
#   (1) venv 를 **추측하지 않는다** — 돌고 있는 웹앱 프로세스의 VIRTUAL_ENV 를
#       읽는다.  후보를 고르면 ~/ddvenv 같은 엉뚱한 데 깔린다.
#   (2) **이미 있는 패키지를 절대 업그레이드하지 않는다** — 웹앱이 그 venv 로
#       지금 돌고 있다.  numpy/scipy 의 .so 가 실행 중에 교체되면 프로세스가
#       죽는다.  pip --dry-run 으로 계획을 먼저 보고, 코어를 건드리면 거부한다.
#
# ★ 근본 원인 (2026-09-22 실측): networkx·adjustText·tabulate 셋 다 **같은 커밋**
#   `660600a44` (2026-04-24) 에서 webapp/requirements.txt 에 들어왔다.  그 venv 는
#   그 전에 만들어졌고 그 뒤로 `pip install -r` 이 다시 안 돌았다.
#   ⇒ **규약(requirements)은 자랐는데 환경은 안 자랐고, 그것을 강제하는 것이 없었다**
#     = CLAUDE.md 규율 ④ ("정본은 밖으로 강제되지 않으면 새어나간다") 의 환경 판.
#   ⚠ 그래서 이 도구는 requirements.txt 를 안 읽는다 — **import 를 읽는다**.
#     requirements 도 낡을 수 있고, 실제로 낡는 쪽은 둘 다이기 때문이다.
#
# 쓰임:
#   bash scripts/setup_webapp_env.sh            # 진단 + 없는 것만 설치
#   bash scripts/setup_webapp_env.sh --check    # 진단만 (설치 안 함)
#   bash scripts/setup_webapp_env.sh --full     # 선택 패키지까지
#   bash scripts/setup_webapp_env.sh --venv ~/x/.venv
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
AUDIT="$HERE/webapp_env_audit.py"

VENV=""; CHECK=0; FULL=0; MPM=0; YES=0; ALLOW_CORE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --venv) VENV="${2:-}"; shift 2 ;;
    --check) CHECK=1; shift ;;
    --full) FULL=1; shift ;;
    --mpm) MPM=1; shift ;;
    --yes|-y) YES=1; shift ;;
    --allow-core-upgrade) ALLOW_CORE=1; shift ;;
    -h|--help) sed -n '2,28p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "⛔ 모르는 인자: $1"; exit 2 ;;
  esac
done

[ -f "$AUDIT" ] || { echo "⛔ 감사기가 없다: $AUDIT"; exit 1; }
SYSPY="$(command -v python3 || true)"
[ -n "$SYSPY" ] || { echo "⛔ python3 가 없다"; exit 1; }

# ── ① venv 를 돌고 있는 웹앱에게 묻는다 ───────────────────────────────────
if [ -z "$VENV" ]; then
  FOUND=""
  for pd in /proc/[0-9]*; do
    [ -r "$pd/cmdline" ] || continue
    cmd="$(tr '\0' ' ' < "$pd/cmdline" 2>/dev/null)"
    case "$cmd" in
      *app.py*|*gunicorn*webapp*|*flask*run*) ;;
      *) continue ;;
    esac
    ve="$(tr '\0' '\n' < "$pd/environ" 2>/dev/null | sed -n 's/^VIRTUAL_ENV=//p' | head -1)"
    [ -n "$ve" ] || continue
    echo "   돌고 있는 웹앱: pid=$(basename "$pd")  VIRTUAL_ENV=$ve"
    case " $FOUND " in *" $ve "*) ;; *) FOUND="$FOUND $ve" ;; esac
  done
  set -- $FOUND
  if [ "$#" -eq 1 ]; then
    VENV="$1"
    echo "   ⇒ 그 venv 를 고친다 (추측 아님)"
  elif [ "$#" -gt 1 ]; then
    echo "⛔ 웹앱이 서로 다른 venv 로 여러 개 떠 있다:"; for v in "$@"; do echo "     $v"; done
    echo "   --venv <경로> 로 하나를 지정할 것.  (프로세스를 임의로 죽이지 않는다)"
    exit 1
  fi
fi
if [ -z "$VENV" ] && [ -n "${VIRTUAL_ENV:-}" ]; then
  VENV="$VIRTUAL_ENV"; echo "   웹앱이 안 떠 있다 — 지금 활성 venv 를 쓴다: $VENV"
fi
if [ -z "$VENV" ]; then
  echo "⛔ venv 를 못 정했다.  웹앱도 안 떠 있고 VIRTUAL_ENV 도 비어 있다."
  echo "   후보를 훑어볼 것:"
  for c in "$HOME"/Yonghoon-DEM-DFT/.venv "$HOME"/dem-web/.venv "$HOME"/ddvenv "$HOME"/dem-venv; do
    [ -x "$c/bin/python" ] && echo "     있음: $c"
  done
  echo "   골랐으면: bash scripts/setup_webapp_env.sh --venv <경로>"
  exit 1
fi

PY="$VENV/bin/python"
[ -x "$PY" ] || PY="$VENV/bin/python3"
[ -x "$PY" ] || { echo "⛔ 인터프리터가 없다: $VENV/bin/python"; exit 1; }
echo

# ★ 스모크 — 패키지가 있다는 것과 **웹앱이 뜬다는 것**은 다른 얘기다.
#   (규칙 J: --help 생존이 아니라 실물을 돌린다.  죽었던 모듈로 직접 잰다.)
#   ⚠ "깔 것이 없다" 경로에서도 **반드시** 돈다 — 안 그러면 ABI 가 깨진 venv 가
#     "완전하다" 로 초록을 낸다 (규율 ⑤ false-green).
smoke() {
  local rc=0 m err
  echo "── 스모크 (실패했던 모듈을 실제로 import) ──"
  for m in dem_analysis_core network_conductivity generate_comparison_plots grade_engine; do
    err="$("$PY" -c "import sys; sys.path.insert(0,'$ROOT/scripts'); sys.path.insert(0,'$ROOT/webapp'); import $m" 2>&1 | tail -1)"
    if [ -z "$err" ]; then echo "   ✅ $m"; else echo "   ⛔ $m  ::  $err"; rc=1; fi
  done
  return "$rc"
}

OPT=""; [ "$FULL" -eq 1 ] && OPT="$OPT --full"; [ "$MPM" -eq 1 ] && OPT="$OPT --mpm"

# ── ② 진단 (실물 import) ──────────────────────────────────────────────────
"$SYSPY" "$AUDIT" --python "$PY" $OPT
DIAG=$?
if [ "$CHECK" -eq 1 ]; then
  echo; smoke; SM=$?
  [ "$DIAG" -eq 0 ] && [ "$SM" -eq 0 ]; exit $?
fi

MISSING="$("$SYSPY" "$AUDIT" --python "$PY" $OPT --list-missing)"
if [ -z "$MISSING" ]; then
  echo; smoke; RC=$?
  echo
  [ "$RC" -eq 0 ] && echo "✅ 깔 것이 없다 — 환경은 이미 완전하다." \
                  || echo "⛔ 패키지는 다 있는데 import 가 죽는다 (ABI 깨짐 등).  위 줄을 볼 것."
  exit "$RC"
fi

echo; echo "── 설치 대상 ──"; echo "$MISSING" | sed 's/^/   /'; echo

# ── ③ ★ 업그레이드 가드 — 돌고 있는 웹앱을 죽이지 않는다 ──────────────────
# 보호 = "코어" 이면서 **이미 깔려 있는** 것만.  빈 venv 에 numpy 를 새로 까는
# 것은 업그레이드가 아니므로 막으면 안 된다 ⇒ 실물로 물어본다.
PROTECT="$("$PY" - <<'PYX'
import importlib
pipname = {'sklearn': 'scikit-learn'}
for m in ('numpy', 'scipy', 'pandas', 'matplotlib', 'flask', 'sklearn'):
    try:
        importlib.import_module(m)
    except BaseException:
        continue
    print(pipname.get(m, m))
PYX
)"
PLAN="$("$PY" -m pip install --dry-run --disable-pip-version-check $MISSING 2>&1)"
if printf '%s' "$PLAN" | grep -qi "no such option"; then
  echo "⚠ 이 pip 는 --dry-run 을 모른다 (구버전).  계획을 미리 못 본다."
  [ "$YES" -eq 1 ] || { echo "   확인 후 --yes 로 다시 실행할 것."; exit 1; }
else
  WOULD="$(printf '%s' "$PLAN" | sed -n 's/^Would install //p')"
  HIT=""
  for p in $PROTECT; do
    case " $WOULD " in
      *" $p-"*) HIT="$HIT $p" ;;
    esac
  done
  if [ -n "$HIT" ] && [ "$ALLOW_CORE" -eq 0 ]; then
    echo "⛔⛔ 거부 — pip 가 코어 패키지를 건드리려 한다:$HIT"
    echo "   웹앱이 이 venv 로 **지금 돌고 있다**.  실행 중에 numpy/scipy 가 교체되면"
    echo "   그 프로세스는 죽는다.  웹앱을 먼저 내리고 --allow-core-upgrade 로 할 것."
    echo
    echo "   걸린 것 (지금 깔린 판 → pip 가 올리려는 판):"
    for p in $HIT; do
      now="$("$PY" -m pip show "$p" 2>/dev/null | sed -n 's/^Version: //p')"
      to="$(printf '%s\n' "$WOULD" | tr ' ' '\n' | sed -n "s/^${p}-//Ip" | head -1)"
      echo "     $p  ${now:-?}  →  ${to:-?}"
    done
    echo
    echo "   전문:  $PY -m pip install --dry-run $(printf '%s' "$MISSING" | tr '\n' ' ')"
    exit 1
  fi
  echo "   pip 계획: ${WOULD:-(신규만)}"
  echo "   ✅ 코어 패키지를 안 건드린다 — 돌고 있는 웹앱에 안전하다."
fi
echo

# ── ④ 설치 (-U 를 절대 쓰지 않는다) ───────────────────────────────────────
# shellcheck disable=SC2086
"$PY" -m pip install --disable-pip-version-check $MISSING
RC=$?
[ "$RC" -eq 0 ] || { echo; echo "⛔ pip 실패 rc=$RC"; exit "$RC"; }

# ── ⑤ 재검증 (설치가 됐다는 pip 의 말이 아니라 **실물 import**) ───────────
echo; echo "── 재검증 ──"
"$SYSPY" "$AUDIT" --python "$PY" $OPT
RC=$?

# ── ⑥ 스모크
if [ "$RC" -eq 0 ]; then echo; smoke; RC=$?; fi

echo
if [ "$RC" -eq 0 ]; then
  echo "✅ 완료.  ⚠ 돌고 있는 웹앱은 **이미 뜬 인스턴스**라 새 패키지를 못 본다 —"
  echo "   분석은 새 subprocess 로 돌기 때문에 대부분 그대로 먹지만, app.py 가"
  echo "   최상위에서 import 하는 것을 새로 깔았다면 웹앱을 한 번 재시작할 것."
else
  echo "⛔ 아직 누락이 남았다 (위 목록)."
fi
exit "$RC"
