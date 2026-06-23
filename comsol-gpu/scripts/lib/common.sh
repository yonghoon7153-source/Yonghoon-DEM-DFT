#!/usr/bin/env bash
# 공통 헬퍼 — 다른 스크립트에서 `source` 한다.
# (단독 실행용 아님)

# --- 경로 (이 파일: comsol-gpu/scripts/lib/common.sh) ---
_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$(dirname "$_LIB_DIR")"
PIPELINE_ROOT="$(dirname "$SCRIPTS_DIR")"   # comsol-gpu/
REPO_ROOT="$(dirname "$PIPELINE_ROOT")"     # 레포 루트
CONFIG_DIR="$PIPELINE_ROOT/config"
MODELS_DIR="$PIPELINE_ROOT/models"
RESULTS_DIR="$PIPELINE_ROOT/results"
BENCH_DIR="$PIPELINE_ROOT/benchmarks"

# --- 로깅 ---
if [ -t 1 ]; then
  C_RED=$'\033[31m'; C_GRN=$'\033[32m'; C_YEL=$'\033[33m'; C_BLU=$'\033[34m'; C_RST=$'\033[0m'
else
  C_RED=; C_GRN=; C_YEL=; C_BLU=; C_RST=
fi
log_info(){ printf '%s[INFO]%s %s\n' "$C_BLU" "$C_RST" "$*"; }
log_ok(){   printf '%s[ OK ]%s %s\n' "$C_GRN" "$C_RST" "$*"; }
log_warn(){ printf '%s[WARN]%s %s\n' "$C_YEL" "$C_RST" "$*" >&2; }
log_err(){  printf '%s[FAIL]%s %s\n' "$C_RED" "$C_RST" "$*" >&2; }
die(){ log_err "$*"; exit 1; }

require_cmd(){ command -v "$1" >/dev/null 2>&1 || die "필수 명령 없음: $1"; }

# --- 서버/COMSOL 설정 로드 ---
load_server_env(){
  local f="$CONFIG_DIR/server.env"
  if [ -f "$f" ]; then
    set -a; # shellcheck disable=SC1090
    . "$f"; set +a
  else
    log_warn "config/server.env 없음 — 예시에서 복사: cp config/server.env.example config/server.env"
  fi
  : "${COMSOL_BIN:=comsol}"
}

# comsol 바이너리 위치 resolve. 성공 시 경로 echo + return 0
find_comsol(){
  if command -v "${COMSOL_BIN:-comsol}" >/dev/null 2>&1; then
    command -v "${COMSOL_BIN:-comsol}"; return 0
  fi
  local p
  for p in /usr/local/comsol*/multiphysics/bin/comsol \
           /usr/local/comsol*/bin/comsol \
           /opt/comsol*/multiphysics/bin/comsol \
           /opt/comsol*/bin/comsol \
           /usr/local/COMSOL*/multiphysics/bin/comsol \
           "$HOME"/comsol*/multiphysics/bin/comsol \
           "$HOME"/comsol*/bin/comsol; do
    [ -x "$p" ] && { echo "$p"; return 0; }
  done
  return 1
}

# --- 모델 설정 로드: load_model_env <name> ---
load_model_env(){
  local name="$1"
  local f="$CONFIG_DIR/models/${name}.env"
  [ -f "$f" ] || die "모델 설정 없음: config/models/${name}.env"
  # 기본값 초기화
  MODEL_NAME="$name"; MPH_FILE=""; STUDY=""; SOLVER=""; USE_GPU="false"
  NP=""; HWACC=""; EXTRA_FLAGS=""; NOTES=""
  # shellcheck disable=SC1090
  . "$f"
  [ -n "$MPH_FILE" ] || die "$f: MPH_FILE 미설정"
  # 상대경로는 PIPELINE_ROOT 기준 절대경로로
  case "$MPH_FILE" in
    /*) : ;;
    *) MPH_FILE="$PIPELINE_ROOT/$MPH_FILE" ;;
  esac
  [ -f "$MPH_FILE" ] || die "모델 파일 없음: $MPH_FILE  (서버에 scp로 올렸나요?)"
  : "${NP:=4}"
}
