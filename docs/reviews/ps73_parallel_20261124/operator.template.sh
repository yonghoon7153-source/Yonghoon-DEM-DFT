(
set -euo pipefail
umask 077
mode=$1
[[ $# -eq 1 ]]
case "$mode" in GO_PS73_PARALLEL_ONCE|STATUS|RETURN|RESUME) ;; *) exit 2;; esac
base=$(cd -- "$(dirname -- "$0")" && pwd)
bundle='@TARBALL@'
sha='@TAR_SHA@'
manifest='@MANIFEST_SHA@'
ctl=$(mktemp -d)
ssh() { command ssh -o ControlMaster=auto -o ControlPersist=120 -o ControlPath="$ctl/%C" "$@"; }
scp() { command scp -o ControlMaster=auto -o ControlPersist=120 -o ControlPath="$ctl/%C" "$@"; }
trap 'command ssh -o ControlPath="$ctl/%C" -O exit -p "$IBBP" "$IBB" >/dev/null 2>&1 || true' EXIT
task=ps73_isolated_1124
if [[ $mode == GO_PS73_PARALLEL_ONCE ]]; then
  printf '%s  %s\n' "$sha" "$base/$bundle" | sha256sum -c --strict -
  ssh -p "$IBBP" "$IBB" 'set -eu; umask 077; test "$(hostname -s)" = ibb-master; test ! -L "$HOME/ps73_isolated_1124"; if test -e "$HOME/ps73_isolated_1124"; then test -f "$HOME/ps73_isolated_1124/code/SOURCE_SHA256SUMS" && test ! -e "$HOME/ps73_isolated_1124/intent.json" || { echo "EXISTING_DISPATCH use STATUS"; exit 2; }; else mkdir "$HOME/ps73_isolated_1124"; fi'
  # Upload under a fresh name. The installed code is never replaced.
  tmp=$(ssh -p "$IBBP" "$IBB" 'cd "$HOME/ps73_isolated_1124" && mktemp -d upload_XXXXXXXX')
  [[ "$tmp" =~ ^upload_[A-Za-z0-9]{8}$ ]]
  scp -P "$IBBP" "$base/$bundle" "$IBB:$task/$tmp/source.tar.gz"
  ssh -p "$IBBP" "$IBB" "bash -s -- $tmp $sha $manifest" <<'INSTALL'
set -euo pipefail
umask 077
cd "$HOME/ps73_isolated_1124"
( cd "$1" && printf '%s  source.tar.gz\n' "$2" | sha256sum -c --strict - &&
  mkdir src && tar -xzf source.tar.gz -C src && cd src &&
  printf '%s  SOURCE_SHA256SUMS\n' "$3" | sha256sum -c --status - && sha256sum -c --status SOURCE_SHA256SUMS )
if [[ ! -d code ]]; then mv -Tn "$1/src" code; fi
INSTALL
fi
run() {
 ssh -p "$IBBP" "$IBB" "bash -s -- $1 $manifest" <<'REMOTE'
set -euo pipefail
umask 077
unset BASH_ENV ENV PYTHONPATH PYTHONHOME
cd "$HOME/ps73_isolated_1124/code"
printf '%s  SOURCE_SHA256SUMS\n' "$2" | sha256sum -c --status -
sha256sum -c --status SOURCE_SHA256SUMS
py="$HOME/.conda/envs/myenv/bin/python3"
printf '%s  %s\n' 561c350efec08f1712162c4d649f4b668bacceb68388e973efec964f0073cd92 "$py" | sha256sum -c --status -
exec "$py" -I -B site_ops.py "$1"
REMOTE
}
if [[ $mode == RETURN ]]; then
  row=$(run RETURN)
  read -r dir digest completeness <<< "$row"
  [[ "$dir" =~ ^return_[A-Za-z0-9_]+$ && "$digest" =~ ^[a-f0-9]{64}$ && "$completeness" =~ ^(PARTIAL|FINAL)$ ]]
  localdir=$(mktemp -d "$base/ps73_parallel_return_XXXXXXXX")
  scp -P "$IBBP" "$IBB:$task/$dir/ps73_return.zip" "$localdir/ps73_return.zip"
  ( cd "$localdir" && printf '%s  ps73_return.zip\n' "$digest" > ARCHIVE_SHA256SUMS &&
    sha256sum -c --strict ARCHIVE_SHA256SUMS && unzip -q ps73_return.zip && sha256sum -c --strict SHA256SUMS )
  printf 'RETURN_DIR=%s\nSTATUS=%s\n' "$localdir" "$completeness"
else
  run "$mode"
  if [[ $mode == GO_PS73_PARALLEL_ONCE || $mode == RESUME ]]; then
    run INITIAL_STATUS
  fi
fi
)
