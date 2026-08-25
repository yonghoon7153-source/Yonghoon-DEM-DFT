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
#  ⚠⚠ 2026-08-25 실측 — `/mnt/*` 는 DrvFs(NTFS)라 `rsync -a` 의 퍼미션·소유자 보존이
#    `mkstemp … Operation not permitted` 로 **거부된다**.  파일은 옮겨졌는데 exit 23 이 난다.
#    ⇒ 대상이 `/mnt/*` 면 **메타데이터 보존을 끈다** (-rlt).  내용·시각은 그대로 보존된다.
#    ⚠ `--modify-window=1` 은 NTFS 의 2초 타임스탬프 해상도 때문 (없으면 매번 전량 재전송).
RS=(-a)
#  ★ 2026-08-25 — `/etc/wsl.conf` 에 metadata 를 켜면 DrvFs 도 퍼미션·시각을 보존한다.
#    그러면 아래 우회가 **필요 없을 뿐 아니라 해롭다** (시각 미보존 → 매번 전량 재전송).
#    ⇒ 켜져 있으면 감지해서 `-a` 그대로 간다.  **켜졌는지 추측하지 않고 마운트를 읽는다.**
_MNT="$(echo "$DST" | cut -d/ -f1-3)"
_HAS_META=0
case "$DST" in
  /mnt/*) awk -v m="$_MNT" '$2==m && $4 ~ /(^|,)metadata(,|$)/ {found=1} END{exit !found}' \
            /proc/mounts 2>/dev/null && _HAS_META=1;;
esac
if [ "$_HAS_META" = 1 ]; then
  echo "[백업] DrvFs **metadata 켜짐** — 표준 -a 로 간다 (증분 동작)"
fi
case "$DST" in
  /mnt/*)
    if [ "$_HAS_META" = 1 ]; then :; else
    #  ⚠⚠ DrvFs(NTFS) 실측 2026-08-25 — 두 가지가 순서대로 걸렸다:
    #    ① `mkstemp … Operation not permitted`  → `--inplace` (임시파일→rename 을 없앤다)
    #    ② `failed to set times … not permitted` → **`--no-times`** (mtime 설정 자체가 막힌다)
    #  ⇒ 시간을 못 보존하면 rsync 의 기본 비교(크기+시각)가 **매번 전량 재전송**이 된다.
    #    그래서 비교 기준을 바꾼다: 작으면 **체크섬**(정확), 크면 **크기만**(빠름).
    #    ⚠ 크기만 비교는 **같은 크기로 내용만 바뀐 파일을 놓친다** — 그래서 어느 쪽을 쓰는지
    #      매번 찍는다 (조용히 부정확해지지 않게).
    _sz=$(du -sm "$SRC" 2>/dev/null | cut -f1)
    if [ "${_sz:-0}" -le "${DEM_BACKUP_CKSUM_MB:-500}" ]; then
      _CMP=(--checksum); _CMPW="체크섬 (원본 ${_sz} MB — 정확)"
    else
      _CMP=(--size-only); _CMPW="크기만 (원본 ${_sz} MB — 빠름.  ⚠ 같은 크기 수정은 못 잡는다)"
    fi
    RS=(-rl --no-times --no-perms --no-owner --no-group --omit-dir-times --inplace "${_CMP[@]}")
    echo "[백업] DrvFs 모드 · 비교 = $_CMPW"
    echo "[백업]   ★ 영구 해결책은 metadata 마운트다 (그러면 -a 로 정상 동작):"
    echo "[백업]     /etc/wsl.conf 에  [automount]  options = \"metadata,uid=1000,gid=1000\""
    echo "[백업]     그 뒤 PowerShell 에서  wsl --shutdown  (한 번만)"
    fi
    ;;
esac
echo "[백업] rsync 중… (원본 파일 $_n_src)"
#  ⚠ 실패 경로를 **버리지 않는다** — 앞선 판은 tail 에 묻혀 무엇이 안 됐는지 알 수 없었다.
_ERR="$(mktemp)"
rsync "${RS[@]}" --delete --info=stats2 "$SRC/" "$DST/" \
  --exclude '.last_backup' --exclude 'dem_webapp.log' --exclude 'dem_webapp.pid' \
  --exclude '__pycache__/' --exclude '*.pyc' \
  2> >(tee "$_ERR" >&2)
_RC=$?
if [ "$_RC" != 0 ]; then
  echo "[백업] ⛔ rsync 종료코드 $_RC — 스탬프를 남기지 않는다"
  echo "──── 실패한 항목 (앞 15줄) ────"
  grep -E 'rsync:|failed|denied|Permission|not permitted' "$_ERR" | head -15
  echo "────────────────────────────────"
  echo "  · 계속 같은 파일이면 대상에서 지우고 다시:  rm -rf \"$DST\" && $0"
  echo "  · /mnt 옵션으로도 안 되면 WSL 의 metadata 마운트가 필요할 수 있다:"
  echo "      sudo umount /mnt/d && sudo mount -t drvfs D: /mnt/d -o metadata,uid=$(id -u),gid=$(id -g)"
  rm -f "$_ERR"; exit 1
fi
rm -f "$_ERR"

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
