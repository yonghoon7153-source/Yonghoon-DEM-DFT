(
set -euo pipefail
umask 077
[[ $# == 1 ]]
mode=$1
case "$mode" in GO_PS73_UVA_EARLY_ONCE|STATUS|RETURN) ;; *) echo 'GO_PS73_UVA_EARLY_ONCE | STATUS | RETURN'; exit 2;; esac
base=$(cd -- "$(dirname -- "$0")" && pwd)
ctl=$(mktemp -d)
ssh() { command ssh -o ControlMaster=auto -o ControlPersist=90 -o ControlPath="$ctl/%C" "$@"; }
scp() { command scp -o ControlMaster=auto -o ControlPersist=90 -o ControlPath="$ctl/%C" "$@"; }
trap 'command ssh -o ControlPath="$ctl/%C" -O exit -p "$IBBP" "$IBB" >/dev/null 2>&1 || true' EXIT
response=$(ssh -p "$IBBP" "$IBB" "bash -s -- $mode" <<'REMOTE'
set -euo pipefail
umask 077
unset BASH_ENV ENV PYTHONPATH PYTHONHOME
[[ $(hostname -s) == ibb-master ]]
root="$HOME/ps73_isolated_1124"
code="$root/code"
addon="$root/early_uva_1125"
py="$HOME/.conda/envs/myenv/bin/python3"
[[ -d "$root" && ! -L "$root" && ! -L "$code" && ! -L "$addon" ]]
(cd "$code" && printf '%s  SOURCE_SHA256SUMS\n' fb53fb1c1eaee6ef289d7353ac7a3fc211c20322dbed872fb2e601563e470858 | sha256sum --strict --status -c - && sha256sum -c --strict --status SOURCE_SHA256SUMS)
printf '%s  %s\n' 561c350efec08f1712162c4d649f4b668bacceb68388e973efec964f0073cd92 "$py" | sha256sum --strict --status -c -
if [[ $1 == GO_PS73_UVA_EARLY_ONCE ]]; then
  if [[ ! -d "$addon" ]]; then
    stage=$(mktemp -d "$root/uva_upload_XXXXXXXX")
    base64 -d > "$stage/package.tar.gz" <<'PAYLOAD'
@PAYLOAD@
PAYLOAD
    (cd "$stage" && printf '%s  package.tar.gz\n' '@SHA@' | sha256sum -c --strict --status - && tar -xzf package.tar.gz)
    mv -Tn -- "$stage" "$addon"
  fi
  cd "$addon"
  printf '%s  SOURCE_SHA256SUMS\n' '@MAN@' | sha256sum --strict --status -c -
  sha256sum -c --strict --status SOURCE_SHA256SUMS
  log=$(mktemp "$addon/dispatch_XXXXXXXX")
  nohup bash -c '"$1" -I -B -u "$2/early.py" GO_PS73_UVA_EARLY_ONCE; rc=$?; echo "$rc" > "$3.rc"; exit "$rc"' ps73 "$py" "$addon" "$log" </dev/null >"$log" 2>&1 &
  echo "EARLY_CONTROLLER_PID=$!"
  for ((i=0; i<30; i++)); do
    if [[ -s "$log.rc" ]]; then cat "$log"; exit "$(cat "$log.rc")"; fi
    sleep 1
  done
  cat "$log"
  echo 'QUERY_STATUS_FOR_UVa_JOB_ID'
elif [[ $1 == STATUS ]]; then
  if [[ -d "$addon" ]]; then
    if [[ -r "$addon/dispatch-ack.json" ]]; then cat "$addon/dispatch-ack.json"
    elif [[ -f "$addon/dispatch-claim.json" ]]; then echo 'EARLY_CLAIM_PRESENT_NO_ACK'
    else echo 'EARLY_SUBMISSION_NOT_RECORDED'; fi
    recent=$(ls -t "$addon"/dispatch_???????? 2>/dev/null | head -n 1) || true
    [[ -z "$recent" ]] || tail -n 4 "$recent"
  fi
  cd "$code"; exec "$py" -I -B site_ops.py STATUS
else
  cd "$code"; exec "$py" -I -B site_ops.py RETURN
fi
REMOTE
) || { rc=$?; printf '%s\n' "$response"; exit "$rc"; }
printf '%s\n' "$response"
if [[ $mode == RETURN ]]; then
  read -r dir digest flag <<< "$response"
  [[ "$dir" =~ ^return_[A-Za-z0-9_]+$ && "$digest" =~ ^[0-9a-f]{64}$ && "$flag" =~ ^(PARTIAL|FINAL)$ ]]
  localdir=$(mktemp -d "$base/ps73_parallel_return_XXXXXXXX")
  scp -P "$IBBP" "$IBB:ps73_isolated_1124/$dir/ps73_return.zip" "$localdir/"
  (cd "$localdir" && printf '%s  ps73_return.zip\n' "$digest" >ARCHIVE_SHA256SUMS &&
    sha256sum -c --strict ARCHIVE_SHA256SUMS && unzip -q ps73_return.zip && sha256sum -c --strict SHA256SUMS)
  printf 'RETURN_DIR=%s\nSTATUS=%s\n' "$localdir" "$flag"
fi
)
