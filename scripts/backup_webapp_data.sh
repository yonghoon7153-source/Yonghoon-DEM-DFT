#!/usr/bin/env bash
# webapp 데이터를 **WSL 밖**(외장 D 등)으로 백업 — 그리고 **안 됐으면 시끄럽게 군다**.
#
# ★★ 왜 (2026-08-25): 윈도우 재설치로 WSL(`ext4.vhdx`)이 통째로 사라지며 웹앱 케이스
#   169건을 잃었다.  코드는 git 에 있어 살았고, 숫자는 `docs/data/case_master.csv` 로
#   되살렸지만 그림·3D·원본 덤프는 못 돌아왔다.  **WSL 안에만 있는 데이터는 윈도우와
#   운명을 같이 한다.**
#
# ⚠⚠ 설계 원칙 — 오늘 하루 잡은 결함이 전부 같은 병이었다 ("선언은 됐는데 실행이 안 됨"):
#   · 백업이 **돌았는지**가 아니라 **파일이 실제로 늘었는지**를 확인한다
#   · 성공하면 스탬프를 남기고, 런처가 그 **나이를 매번 보여준다** (침묵 = 실패로 보이게)
#   · rsync 가 없으면 조용히 넘어가지 않고 **멈춘다**
#
#   bash scripts/backup_webapp_data.sh                 # DEM_WEB_BACKUP 으로 백업
#   DEM_WEB_BACKUP=/mnt/d/dem-backup bash scripts/backup_webapp_data.sh
#   bash scripts/backup_webapp_data.sh --check         # 상태만 (쓰지 않음)
#   bash scripts/backup_webapp_data.sh --restore       # 백업 → WSL 로 되돌리기
set -uo pipefail

SRC="${DEM_WEB_DATA:-$HOME/Yonghoon-DEM-DFT}/webapp"
DST="${DEM_WEB_BACKUP:-/mnt/d/dem-backup/webapp}"
STAMP="$SRC/.last_backup"
MODE=run
for a in "$@"; do
  case "$a" in
    --check) MODE=check;;
    --restore) MODE=restore;;
    -h|--help) sed -n '1,25p' "$0"; exit 0;;
    *) echo "알 수 없는 인자: $a"; exit 2;;
  esac
done

_count() { find "$1" -type f 2>/dev/null | wc -l; }
_cases() { find "$1/results" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l; }

echo "[백업] 원본 $SRC"
echo "[백업] 대상 $DST"

if [ "$MODE" = check ]; then
  echo "  원본  파일 $(_count "$SRC") · 케이스 $(_cases "$SRC")"
  if [ -d "$DST" ]; then
    echo "  백업  파일 $(_count "$DST") · 케이스 $(_cases "$DST")"
  else
    echo "  백업  **없음** — 아직 한 번도 안 떴다"
  fi
  if [ -f "$STAMP" ]; then
    _age=$(( ( $(date +%s) - $(stat -c %Y "$STAMP") ) / 86400 ))
    echo "  마지막 성공: $(cat "$STAMP")  (${_age}일 전)"
  else
    echo "  마지막 성공: **기록 없음**"
  fi
  exit 0
fi

command -v rsync >/dev/null 2>&1 || {
  echo "[백업] ⛔ rsync 가 없다 — 조용히 넘어가지 않는다.  설치:  sudo apt install -y rsync"
  exit 1; }

if [ "$MODE" = restore ]; then
  [ -d "$DST" ] || { echo "[백업] ⛔ 백업이 없다: $DST"; exit 1; }
  echo "[백업] ← 되돌리기 (기존 파일은 **덮지 않는다**: --ignore-existing)"
  mkdir -p "$SRC"
  rsync -a --info=stats2 --ignore-existing "$DST/" "$SRC/" || exit 1
  echo "[백업] ✓ 복원 후 케이스 $(_cases "$SRC")건"
  exit 0
fi

[ -d "$SRC" ] || { echo "[백업] ⛔ 원본이 없다: $SRC"; exit 1; }
_n_src=$(_count "$SRC")
[ "$_n_src" -gt 0 ] || { echo "[백업] ⛔ 원본이 비어 있다 — **빈 것으로 백업을 덮지 않는다**"; exit 1; }

#  대상 상위가 마운트돼 있나 (D 를 안 꽂고 돌리면 WSL 안에 가짜 백업이 생긴다)
_top="$(dirname "$(dirname "$DST")")"
case "$DST" in
  /mnt/*) mountpoint -q "$(echo "$DST" | cut -d/ -f1-3)" 2>/dev/null || {
            echo "[백업] ⛔ $(echo "$DST" | cut -d/ -f1-3) 가 마운트돼 있지 않다."
            echo "        외장을 안 꽂은 채 돌리면 **WSL 안에 가짜 백업**이 생겨 같이 죽는다."
            exit 1; };;
esac
mkdir -p "$DST" || { echo "[백업] ⛔ 대상을 만들 수 없다: $DST"; exit 1; }

_before=$(_count "$DST")
echo "[백업] rsync 중… (원본 파일 $_n_src)"
rsync -a --delete --info=stats2 "$SRC/" "$DST/" \
  --exclude '.last_backup' --exclude 'dem_webapp.log' --exclude 'dem_webapp.pid' \
  || { echo "[백업] ⛔ rsync 실패 — 스탬프를 남기지 않는다 (실패를 성공으로 기록하지 않는다)"; exit 1; }

_after=$(_count "$DST")
_c_src=$(_cases "$SRC"); _c_dst=$(_cases "$DST")
echo "[백업] 대상 파일 $_before → $_after · 케이스 원본 $_c_src ↔ 백업 $_c_dst"
#  ★ **돌았다** 가 아니라 **맞다** 를 확인한다 (오늘 잡은 결함의 교훈)
if [ "$_c_src" != "$_c_dst" ]; then
  echo "[백업] ⛔ 케이스 수가 안 맞는다 ($_c_src ≠ $_c_dst) — 스탬프 안 남긴다"
  exit 1
fi
date -Iseconds > "$STAMP"
echo "[백업] ✓ 완료 · 스탬프 $(cat "$STAMP")"
echo "[백업]   되돌리기:  bash scripts/backup_webapp_data.sh --restore"
