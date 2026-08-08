#!/usr/bin/env bash
# Self-contained runner for a generated PTFE/LiNiO2 VASP package.
set -uo pipefail

ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT" || exit 1

if [ -f "$ROOT/vendor.conf" ]; then
  # shellcheck source=/dev/null
  . "$ROOT/vendor.conf"
fi
VASP_PP_PATH=${VASP_PP_PATH:-/opt/vasp/potpaw_PBE.54}
VASP_CMD=${VASP_CMD:-"mpirun -np 32 vasp_std"}
VASP_NCORE=${VASP_NCORE:-4}
PYTHON_BIN=${PYTHON_BIN:-python3}
MODE=${1:-help}
ARG=${2:-}
read -r -a VASP_ARGV <<< "$VASP_CMD"
ACTIVE_CHILD_PID=""
ACTIVE_PID_FILE=""

die () { echo "ERROR: $*" >&2; exit 2; }

stop_process_group () {
  local pid=$1 signal=${2:-TERM}
  [ -n "$pid" ] || return 0
  if kill -0 -- "-$pid" 2>/dev/null; then
    kill -s "$signal" -- "-$pid" 2>/dev/null || true
  elif kill -0 "$pid" 2>/dev/null; then
    kill -s "$signal" "$pid" 2>/dev/null || true
  fi
}

process_group_alive () {
  local pid=$1
  kill -0 -- "-$pid" 2>/dev/null || kill -0 "$pid" 2>/dev/null
}

terminate_process_group_bounded () {
  local pid=$1 count
  [ -n "$pid" ] || return 0
  stop_process_group "$pid" TERM
  for count in 1 2 3 4 5 6 7 8 9 10; do
    process_group_alive "$pid" || return 0
    sleep 1
  done
  stop_process_group "$pid" KILL
}

if [ ${#VASP_ARGV[@]} -eq 0 ]; then die "VASP_CMD is empty"; fi
if ! [[ "$VASP_NCORE" =~ ^[1-9][0-9]*$ ]]; then die "VASP_NCORE must be positive"; fi
command -v "$PYTHON_BIN" >/dev/null 2>&1 || die "Python 3.8+ is required ($PYTHON_BIN not found)"
"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,8) else 1)' \
  || die "Python 3.8+ is required: $($PYTHON_BIN --version 2>&1)"
"$PYTHON_BIN" -c 'import ase,numpy' || die "ASE and NumPy are required for structure/geometry gates"

handle_signal () {
  local signal=$1 code=143
  [ "$signal" = INT ] && code=130
  trap - INT TERM
  if [ -n "$ACTIVE_CHILD_PID" ]; then
    # INT/TERM both receive a bounded graceful stop followed by KILL.  Do not
    # wait forever while holding the package flock.
    terminate_process_group_bounded "$ACTIVE_CHILD_PID"
    wait "$ACTIVE_CHILD_PID" 2>/dev/null || true
  fi
  [ -z "$ACTIVE_PID_FILE" ] || rm -f "$ACTIVE_PID_FILE"
  exit "$code"
}

command -v flock >/dev/null 2>&1 || die "flock is required; unsafe mkdir fallback is disabled"
command -v setsid >/dev/null 2>&1 || die "setsid is required for MPI process-group cleanup"
exec 9>"$ROOT/.vasp_run.lock"
flock -n 9 || die "another vasp_run.sh owns this package"
trap 'handle_signal INT' INT
trap 'handle_signal TERM' TERM

verify_inputs () {
  [ -s "$ROOT/VASP_INPUT_MANIFEST.sha256" ] || {
    echo "ERROR: VASP_INPUT_MANIFEST.sha256 is missing" >&2
    return 1
  }
  (cd "$ROOT" && sha256sum -c VASP_INPUT_MANIFEST.sha256 --quiet) || {
    echo "ERROR: immutable VASP input hash check failed" >&2
    return 1
  }
  "$PYTHON_BIN" "$ROOT/vasp_stage.py" list-jobs --vasp-out "$ROOT" >/dev/null
}

write_or_check_runtime_hashes () {
  local run_dir=$1 manifest="$1/RUNTIME_INPUTS.sha256" tmp="$1/.RUNTIME_INPUTS.tmp.$$"
  local metadata="$1/RUNTIME_METADATA.txt" metadata_tmp="$1/.RUNTIME_METADATA.tmp.$$"
  local potcar_sha potcar_titel wavecar_sha=NONE chgcar_sha=NONE
  if [ -s "$manifest" ]; then
    check_runtime_hashes "$run_dir"
  else
    potcar_sha=$(sha256sum "$run_dir/POTCAR" | awk '{print $1}') || return 1
    potcar_titel=$(grep -a 'TITEL' "$run_dir/POTCAR" | sed 's/^[[:space:]]*//' | paste -sd ';' -)
    [ ! -s "$run_dir/WAVECAR" ] || wavecar_sha=$(sha256sum "$run_dir/WAVECAR" | awk '{print $1}')
    [ ! -s "$run_dir/CHGCAR" ] || chgcar_sha=$(sha256sum "$run_dir/CHGCAR" | awk '{print $1}')
    {
      printf 'HOST=%s\n' "$(hostname)"
      printf 'VASP_CMD=%s\n' "$VASP_CMD"
      printf 'VASP_NCORE=%s\n' "$VASP_NCORE"
      printf 'POTCAR_SHA256=%s\n' "$potcar_sha"
      printf 'POTCAR_TITEL=%s\n' "$potcar_titel"
      printf 'INHERITED_WAVECAR_SHA256=%s\n' "$wavecar_sha"
      printf 'INHERITED_CHGCAR_SHA256=%s\n' "$chgcar_sha"
      printf 'PACKAGE_INPUT_MANIFEST_SHA256=%s\n' "$(sha256sum "$ROOT/VASP_INPUT_MANIFEST.sha256" | awk '{print $1}')"
      printf 'POTCAR_COMPONENT_LIBRARY_MANIFEST_SHA256=%s\n' "$(sha256sum "$ROOT/POTCAR_LIBRARY_COMPONENTS.sha256" | awk '{print $1}')"
    } > "$metadata_tmp" || { rm -f "$metadata_tmp"; return 1; }
    mv "$metadata_tmp" "$metadata" || return 1
    (cd "$run_dir" && sha256sum POSCAR INCAR KPOINTS POTCAR.spec SOURCE.json RUNTIME_METADATA.txt) > "$tmp" \
      || { rm -f "$tmp"; return 1; }
    mv "$tmp" "$manifest" || return 1
  fi
}

check_runtime_hashes () {
  local run_dir=$1 manifest="$1/RUNTIME_INPUTS.sha256" expected_potcar actual_potcar
  local expected_library actual_library
  [ -s "$manifest" ] || {
    echo "ERROR: runtime input manifest missing in $run_dir" >&2
    return 1
  }
  (cd "$run_dir" && sha256sum -c RUNTIME_INPUTS.sha256 --quiet) || {
    echo "ERROR: runtime input drift detected in $run_dir" >&2
    return 1
  }
  expected_potcar=$(sed -n 's/^POTCAR_SHA256=//p' "$run_dir/RUNTIME_METADATA.txt")
  [ -n "$expected_potcar" ] || {
    echo "ERROR: POTCAR provenance is missing in $run_dir" >&2; return 1;
  }
  [ -s "$run_dir/POTCAR" ] || {
    echo "ERROR: POTCAR is missing before provenance check in $run_dir" >&2; return 1;
  }
  actual_potcar=$(sha256sum "$run_dir/POTCAR" | awk '{print $1}') || return 1
  [ "$actual_potcar" = "$expected_potcar" ] || {
    echo "ERROR: POTCAR drift detected in $run_dir" >&2; return 1;
  }
  expected_library=$(sed -n 's/^POTCAR_COMPONENT_LIBRARY_MANIFEST_SHA256=//p' \
    "$run_dir/RUNTIME_METADATA.txt")
  [ -n "$expected_library" ] || {
    echo "ERROR: POTCAR component-library provenance is missing in $run_dir" >&2; return 1;
  }
  actual_library=$(sha256sum "$ROOT/POTCAR_LIBRARY_COMPONENTS.sha256" | awk '{print $1}') \
    || return 1
  [ "$actual_library" = "$expected_library" ] || {
    echo "ERROR: POTCAR component-library baseline changed after $run_dir was prepared" >&2
    return 1
  }
}

complete_static () {
  local outcar=$1
  [ -s "$outcar" ] || return 1
  grep -aq "aborting loop because EDIFF is reached" "$outcar" || return 1
  grep -aq "General timing and accounting" "$outcar" || return 1
}

complete_relax () {
  complete_static "$1" || return 1
  grep -aq "reached required accuracy - stopping structural energy minimisation" "$1"
}

job_names () {
  "$PYTHON_BIN" "$ROOT/vasp_stage.py" list-jobs --vasp-out "$ROOT"
}

dense_names () {
  "$PYTHON_BIN" "$ROOT/vasp_stage.py" list-jobs --vasp-out "$ROOT" --dense
}

verify_potcar_library_identity () {
  local baseline="$ROOT/POTCAR_LIBRARY_COMPONENTS.sha256" tmp="$ROOT/.POTCAR_LIBRARY_COMPONENTS.tmp.$$"
  local spec source variant digest
  : > "$tmp" || return 1
  while IFS= read -r spec; do
    [ -n "$spec" ] || continue
    source=""
    for variant in "$VASP_PP_PATH/$spec/POTCAR" "$VASP_PP_PATH/$spec/POTCAR.Z"; do
      if [ -s "$variant" ]; then source=$variant; break; fi
    done
    if [ -z "$source" ]; then
      rm -f "$tmp"
      echo "ERROR: missing $VASP_PP_PATH/$spec/POTCAR[.Z]" >&2
      return 1
    fi
    if [[ "$source" == *.Z ]]; then
      digest=$(zcat "$source" | sha256sum | awk '{print $1}') || { rm -f "$tmp"; return 1; }
    else
      digest=$(sha256sum "$source" | awk '{print $1}') || { rm -f "$tmp"; return 1; }
    fi
    printf '%s  %s\n' "$digest" "$spec" >> "$tmp" || { rm -f "$tmp"; return 1; }
  done < <(awk 'NF >= 2 && $1 !~ /^#/ {print $2}' "$ROOT"/jobs/*/POTCAR.spec | sort -u)
  if [ -s "$baseline" ]; then
    cmp -s "$tmp" "$baseline" || {
      echo "ERROR: POTCAR component library changed after the package baseline was fixed" >&2
      rm -f "$tmp"
      return 1
    }
    rm -f "$tmp"
  else
    mv "$tmp" "$baseline" || return 1
  fi
}

check_potcar_sources () {
  verify_potcar_library_identity || return 1
  echo "POTCAR source library: OK ($VASP_PP_PATH)"
}

validate_potcar () {
  local job_dir=$1 potcar=$2
  local -a elements specs titles pos_species
  mapfile -t elements < <(awk 'NF >= 2 && $1 !~ /^#/ {print $1}' "$job_dir/POTCAR.spec")
  mapfile -t specs < <(awk 'NF >= 2 && $1 !~ /^#/ {print $2}' "$job_dir/POTCAR.spec")
  read -r -a pos_species <<< "$(sed -n '6p' "$job_dir/POSCAR")"
  if [ "${elements[*]}" != "${pos_species[*]}" ]; then
    echo "ERROR: POSCAR/POTCAR.spec order mismatch in $job_dir" >&2
    return 1
  fi
  mapfile -t titles < <(grep -a "TITEL" "$potcar")
  if [ "${#titles[@]}" -ne "${#specs[@]}" ]; then
    echo "ERROR: POTCAR TITEL count mismatch in $job_dir" >&2
    return 1
  fi
  local i
  for i in "${!specs[@]}"; do
    if [[ "${titles[$i]}" != *" ${specs[$i]} "* && "${titles[$i]}" != *" ${specs[$i]}" ]]; then
      echo "ERROR: POTCAR[$i] expected ${specs[$i]}, got ${titles[$i]}" >&2
      return 1
    fi
    [[ "${titles[$i]}" == *"PAW_PBE"* ]] || {
      echo "ERROR: non-PBE POTCAR title: ${titles[$i]}" >&2
      return 1
    }
  done
}

build_potcar () {
  local job_dir=$1 run_dir=$2 potcar="$2/POTCAR" tmp="$2/POTCAR.tmp.$$" spec
  verify_potcar_library_identity || return 1
  : > "$tmp" || return 1
  while IFS= read -r spec; do
    if [ -s "$VASP_PP_PATH/$spec/POTCAR" ]; then
      cat "$VASP_PP_PATH/$spec/POTCAR" >> "$tmp" || { rm -f "$tmp"; return 1; }
    elif [ -s "$VASP_PP_PATH/$spec/POTCAR.Z" ]; then
      zcat "$VASP_PP_PATH/$spec/POTCAR.Z" >> "$tmp" || { rm -f "$tmp"; return 1; }
    else
      rm -f "$tmp"; echo "ERROR: missing POTCAR for $spec" >&2; return 1
    fi
  done < <(awk 'NF >= 2 && $1 !~ /^#/ {print $2}' "$job_dir/POTCAR.spec")
  if [ -s "$potcar" ]; then
    cmp -s "$tmp" "$potcar" || {
      echo "ERROR: existing POTCAR content differs from the fixed component library: $potcar" >&2
      rm -f "$tmp"
      return 1
    }
    rm -f "$tmp"
  else
    mv "$tmp" "$potcar" || return 1
  fi
  validate_potcar "$job_dir" "$potcar"
}

copy_immutable () {
  local source=$1 target=$2
  if [ -e "$target" ]; then
    cmp -s "$source" "$target" || {
      echo "ERROR: existing runtime input differs: $target" >&2; return 1;
    }
  else
    cp "$source" "$target" || return 1
  fi
}

render_incar () {
  local source=$1 target=$2 poscar=$3 recompute_dipol=$4 tmp="$2.tmp.$$" dipol=""
  if [ "$recompute_dipol" -eq 1 ]; then
    dipol=$("$PYTHON_BIN" "$ROOT/vasp_stage.py" direct-com --poscar "$poscar") || return 1
  fi
  {
    if [ -n "$dipol" ]; then
      awk 'toupper($1) != "DIPOL"' "$source"
      printf 'DIPOL = %s\n' "$dipol"
    else
      cat "$source"
    fi
    printf '\n# Runtime hardware setting\nNCORE = %s\n' "$VASP_NCORE"
  } > "$tmp" || { rm -f "$tmp"; return 1; }
  if [ -e "$target" ]; then
    cmp -s "$tmp" "$target" || {
      echo "ERROR: existing runtime INCAR differs: $target" >&2
      rm -f "$tmp"; return 1
    }
    rm -f "$tmp"
  else
    mv "$tmp" "$target" || return 1
  fi
}

prepare_phase () {
  local job_dir=$1 phase=$2 run_dir="$1/$2" source_poscar source_kpoints source_incar dipol=0
  mkdir -p "$run_dir" || return 1
  case "$phase" in
    relax)
      source_poscar="$job_dir/POSCAR"; source_kpoints="$job_dir/KPOINTS"
      source_incar="$job_dir/INCAR.relax"
      ;;
    static)
      complete_relax "$job_dir/relax/OUTCAR" || { echo "ERROR: relax incomplete for $job_dir" >&2; return 1; }
      [ -s "$job_dir/relax/CONTCAR" ] || { echo "ERROR: relax CONTCAR missing" >&2; return 1; }
      source_poscar="$job_dir/relax/CONTCAR"; source_kpoints="$job_dir/KPOINTS"
      source_incar="$job_dir/INCAR.static"; dipol=1
      ;;
    dense)
      complete_static "$job_dir/static/OUTCAR" || { echo "ERROR: static incomplete for $job_dir" >&2; return 1; }
      [ -s "$job_dir/relax/CONTCAR" ] || { echo "ERROR: relax CONTCAR missing" >&2; return 1; }
      source_poscar="$job_dir/relax/CONTCAR"; source_kpoints="$job_dir/KPOINTS.dense"
      source_incar="$job_dir/INCAR.dense"; dipol=1
      ;;
    *) echo "ERROR: unknown phase $phase" >&2; return 1 ;;
  esac
  copy_immutable "$source_poscar" "$run_dir/POSCAR" || return 1
  copy_immutable "$source_kpoints" "$run_dir/KPOINTS" || return 1
  copy_immutable "$job_dir/POTCAR.spec" "$run_dir/POTCAR.spec" || return 1
  copy_immutable "$job_dir/SOURCE.json" "$run_dir/SOURCE.json" || return 1
  render_incar "$source_incar" "$run_dir/INCAR" "$run_dir/POSCAR" "$dipol" || return 1
  build_potcar "$job_dir" "$run_dir" || return 1
  if [ "$phase" = static ]; then
    [ -s "$job_dir/relax/WAVECAR" ] || { echo "ERROR: relax WAVECAR missing" >&2; return 1; }
    [ -s "$job_dir/relax/CHGCAR" ] || { echo "ERROR: relax CHGCAR missing" >&2; return 1; }
    copy_immutable "$job_dir/relax/WAVECAR" "$run_dir/WAVECAR" || return 1
    copy_immutable "$job_dir/relax/CHGCAR" "$run_dir/CHGCAR" || return 1
  elif [ "$phase" = dense ]; then
    [ -s "$job_dir/static/CHGCAR" ] || { echo "ERROR: static CHGCAR missing" >&2; return 1; }
    copy_immutable "$job_dir/static/CHGCAR" "$run_dir/CHGCAR" || return 1
  fi
  write_or_check_runtime_hashes "$run_dir"
}

run_phase () {
  local job_dir=$1 phase=$2 run_dir="$1/$2" launched_pid rc completion_rc=1
  if { [ "$phase" = relax ] && complete_relax "$run_dir/OUTCAR"; } || \
     { [ "$phase" != relax ] && complete_static "$run_dir/OUTCAR"; }; then
    echo "[${job_dir#$ROOT/}/$phase] complete -> skip"; return 0
  fi
  if [ -e "$run_dir/OUTCAR" ] || [ -e "$run_dir/vasp.log" ]; then
    echo "ERROR: incomplete output exists in $run_dir; inspect it, do not overwrite" >&2
    return 1
  fi
  local pid_file="$run_dir/ACTIVE_PID" prior=""
  if [ -s "$pid_file" ]; then
    prior=$(cat "$pid_file" 2>/dev/null || true)
    if [ -n "$prior" ] && kill -0 "$prior" 2>/dev/null; then
      echo "ERROR: a live VASP launcher still owns $run_dir (PID $prior)" >&2
      return 1
    fi
    rm -f "$pid_file"
  fi
  echo "[${job_dir#$ROOT/}/$phase] start $(date -Is)"
  (cd "$run_dir" && exec setsid "${VASP_ARGV[@]}" > vasp.log 2>&1) &
  ACTIVE_CHILD_PID=$!
  launched_pid=$ACTIVE_CHILD_PID
  ACTIVE_PID_FILE="$pid_file"
  printf '%s\n' "$ACTIVE_CHILD_PID" > "$pid_file"
  wait "$launched_pid"; rc=$?
  if [ "$rc" -eq 0 ]; then
    if [ "$phase" = relax ]; then
      complete_relax "$run_dir/OUTCAR" && completion_rc=0
    else
      complete_static "$run_dir/OUTCAR" && completion_rc=0
    fi
  fi
  if [ "$rc" -ne 0 ] || [ "$completion_rc" -ne 0 ] || process_group_alive "$launched_pid"; then
    # The setsid leader may exit before an MPI child.  Clean the whole process
    # group before releasing ACTIVE_PID or the package-wide flock.  Completion
    # failure is handled the same way even when a configurable wrapper exits 0.
    terminate_process_group_bounded "$launched_pid"
  fi
  ACTIVE_CHILD_PID=""
  rm -f "$pid_file"; ACTIVE_PID_FILE=""
  if [ "$rc" -ne 0 ]; then
    echo "ERROR: VASP exited $rc in $run_dir" >&2
    tail -20 "$run_dir/vasp.log" 2>/dev/null || true
    return "$rc"
  fi
  [ "$completion_rc" -eq 0 ] \
    || { echo "ERROR: completion gate failed in $run_dir" >&2; return 1; }
  echo "[${job_dir#$ROOT/}/$phase] complete $(date -Is)"
}

run_job () {
  local name=$1 job_dir="$ROOT/jobs/$1"
  [ -d "$job_dir" ] || { echo "ERROR: unknown job $name" >&2; return 2; }
  prepare_phase "$job_dir" relax && run_phase "$job_dir" relax || return 1
  prepare_phase "$job_dir" static && run_phase "$job_dir" static
}

run_dense_job () {
  local name=$1 job_dir="$ROOT/jobs/$1"
  [ -d "$job_dir" ] || { echo "ERROR: unknown dense job $name" >&2; return 2; }
  prepare_phase "$job_dir" dense && run_phase "$job_dir" dense
}

run_all () {
  local name
  while IFS= read -r name; do [ -n "$name" ] && run_job "$name" || return 1; done < <(job_names)
}

all_coarse_complete () {
  local name
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    complete_relax "$ROOT/jobs/$name/relax/OUTCAR" || return 1
    complete_static "$ROOT/jobs/$name/static/OUTCAR" || return 1
  done < <(job_names)
}

all_dense_complete () {
  local name found=0
  while IFS= read -r name; do
    [ -n "$name" ] || continue; found=1
    complete_static "$ROOT/jobs/$name/dense/OUTCAR" || return 1
  done < <(dense_names)
  [ "$found" -eq 1 ]
}

return_files_present () {
  local include_dense=$1 name phase required path
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    for phase in relax static; do
      for required in POSCAR INCAR KPOINTS POTCAR.spec SOURCE.json OUTCAR OSZICAR; do
        path="$ROOT/jobs/$name/$phase/$required"
        [ -s "$path" ] || { echo "ERROR: required return file missing: $path" >&2; return 1; }
      done
      [ -f "$ROOT/jobs/$name/$phase/vasp.log" ] || {
        echo "ERROR: required return log missing: jobs/$name/$phase/vasp.log" >&2; return 1;
      }
      check_runtime_hashes "$ROOT/jobs/$name/$phase" || return 1
    done
    [ -s "$ROOT/jobs/$name/relax/CONTCAR" ] || {
      echo "ERROR: required relax CONTCAR missing: jobs/$name" >&2; return 1;
    }
  done < <(job_names)
  if [ "$include_dense" -eq 1 ]; then
    while IFS= read -r name; do
      [ -n "$name" ] || continue
      for required in POSCAR INCAR KPOINTS POTCAR.spec SOURCE.json OUTCAR OSZICAR; do
        path="$ROOT/jobs/$name/dense/$required"
        [ -s "$path" ] || { echo "ERROR: required dense return file missing: $path" >&2; return 1; }
      done
      [ -f "$ROOT/jobs/$name/dense/vasp.log" ] || {
        echo "ERROR: required dense log missing: jobs/$name/dense/vasp.log" >&2; return 1;
      }
      check_runtime_hashes "$ROOT/jobs/$name/dense" || return 1
    done < <(dense_names)
  fi
}

run_dense_all () {
  all_coarse_complete || { echo "ERROR: finish all relax/static jobs first" >&2; return 1; }
  "$PYTHON_BIN" "$ROOT/vasp_stage.py" analyze --vasp-out "$ROOT" || return 1
  local name
  while IFS= read -r name; do [ -n "$name" ] && run_dense_job "$name" || return 1; done < <(dense_names)
  "$PYTHON_BIN" "$ROOT/vasp_stage.py" analyze --vasp-out "$ROOT" --require-dense
}

reject_sensitive_backups () {
  local path base
  while IFS= read -r -d '' path; do
    base=${path##*/}
    case "$base" in
      POTCAR|POTCAR.spec|POTCAR.tmp.*|WAVECAR|CHGCAR|CHG) ;;
      *) echo "ERROR: unexpected sensitive/large backup: $path" >&2; return 1 ;;
    esac
  done < <(find "$ROOT/jobs" -type f \
    \( -name 'POTCAR*' -o -name '.POTCAR*' -o -name '#POTCAR#' \
       -o -name 'WAVECAR*' -o -name 'CHGCAR*' -o -name 'CHG*' \) -print0)
  while IFS= read -r -d '' path; do
    echo "ERROR: refusing to archive editor swap/core dump: $path" >&2
    return 1
  done < <(find "$ROOT" -type f \
    \( -name '*.swp' -o -name '*.swo' -o -name '#*#' -o -name 'core' -o -name 'core.*' \) -print0)
}

scope_is_all () {
  "$PYTHON_BIN" -c 'import json; print(json.load(open("VASP_PLAN.json"))["scope"])' | grep -qx all
}

build_archive_allowlist () {
  local list=$1 name phase file rel
  : > "$list" || return 1
  for file in \
    README_GENERATED.md VASP_README_KO.md vasp_run.sh vasp_stage.py \
    vasp_vendor.conf.example vendor.conf VASP_INPUT_MANIFEST.sha256 \
    POTCAR_LIBRARY_COMPONENTS.sha256 \
    VASP_PLAN.json VASP_PLAN.csv UPSTREAM_DFT_HANDOFF.json PACKAGE_COMMIT.txt \
    DENSE_SELECTION.json VASP_RESULTS.csv ADSORPTION_RESULTS.csv \
    ADSORPTION_RESULTS_DENSE.csv VASP_ANALYSIS.json VASP_RESULTS.md; do
    [ ! -f "$ROOT/$file" ] || printf '%s\n' "$file" >> "$list"
  done
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    for file in POSCAR INCAR.relax INCAR.static INCAR.dense KPOINTS KPOINTS.dense POTCAR.spec SOURCE.json; do
      rel="jobs/$name/$file"
      [ ! -f "$ROOT/$rel" ] || printf '%s\n' "$rel" >> "$list"
    done
    for phase in relax static dense; do
      for file in POSCAR INCAR KPOINTS POTCAR.spec SOURCE.json OUTCAR OSZICAR vasp.log \
        CONTCAR RUNTIME_INPUTS.sha256 RUNTIME_METADATA.txt; do
        rel="jobs/$name/$phase/$file"
        [ ! -f "$ROOT/$rel" ] || printf '%s\n' "$rel" >> "$list"
      done
    done
  done < <(job_names)
  LC_ALL=C sort -u -o "$list" "$list"
}

archive_results () {
  local completeness=$1 archive="$ROOT/ptfe_linio2_vasp_results.tar.gz"
  local tmp="$ROOT/../.ptfe_linio2_vasp_results.tar.gz.tmp.$$"
  local allowlist="$ROOT/../.ptfe_linio2_vasp_archive_files.tmp.$$"
  if [ "$completeness" = final ]; then
    verify_potcar_library_identity || return 1
    all_coarse_complete || { echo "ERROR: archive-final requires every relax/static job" >&2; return 1; }
    if scope_is_all; then
      [ -s "$ROOT/DENSE_SELECTION.json" ] || { echo "ERROR: dense selection missing" >&2; return 1; }
      all_dense_complete || { echo "ERROR: archive-final requires selected dense jobs" >&2; return 1; }
      return_files_present 1 || return 1
      "$PYTHON_BIN" "$ROOT/vasp_stage.py" analyze --vasp-out "$ROOT" --require-dense || return 1
    else
      return_files_present 0 || return 1
      "$PYTHON_BIN" "$ROOT/vasp_stage.py" analyze --vasp-out "$ROOT" || return 1
    fi
  else
    "$PYTHON_BIN" "$ROOT/vasp_stage.py" analyze --vasp-out "$ROOT" || true
  fi
  [ ! -e "$archive" ] || { echo "ERROR: archive already exists: $archive" >&2; return 1; }
  [ ! -e "$tmp" ] || { echo "ERROR: temporary archive already exists: $tmp" >&2; return 1; }
  reject_sensitive_backups || return 1
  build_archive_allowlist "$allowlist" || { rm -f "$allowlist"; return 1; }
  tar -C "$ROOT" -czf "$tmp" --no-recursion -T "$allowlist" \
    || { rm -f "$tmp" "$allowlist"; return 1; }
  rm -f "$allowlist"
  if tar -tzf "$tmp" | grep -Eq '(^|/)(POTCAR($|\.tmp|\.bak|\.old)|WAVECAR|CHGCAR|CHG($|\.))'; then
    echo "ERROR: sensitive VASP file survived archive exclusions" >&2
    rm -f "$tmp"
    return 1
  fi
  mv "$tmp" "$archive" || { rm -f "$tmp"; return 1; }
  sha256sum "$archive"
}

verify_inputs || exit 4

echo "PTFE/LiNiO2 VASP | mode=$MODE | NCORE=$VASP_NCORE"
case "$MODE" in
  check) check_potcar_sources ;;
  list) column -s, -t < "$ROOT/VASP_PLAN.csv" 2>/dev/null || cat "$ROOT/VASP_PLAN.csv" ;;
  run-one) [ -n "$ARG" ] || die "run-one needs a job name"; check_potcar_sources && run_job "$ARG" ;;
  run-all) check_potcar_sources && run_all ;;
  collect) "$PYTHON_BIN" "$ROOT/vasp_stage.py" analyze --vasp-out "$ROOT" ;;
  dense) check_potcar_sources && run_dense_all ;;
  archive-final) archive_results final ;;
  archive-partial) archive_results partial ;;
  help|-h|--help)
    cat <<'EOF'
usage: bash vasp_run.sh MODE [JOB]

  check             verify immutable inputs, Python/ASE, and POTCAR library
  list              show the generated job matrix
  run-one JOB       run one exact relax -> static template
  run-all           sequentially run every planned relax -> static template
  collect           parse completed coarse jobs and write analysis files
  dense             select finalists, run 3x4x1 statics, then reanalyze
  archive-final     require all planned work (and dense for all scope), then archive
  archive-partial   archive an explicitly incomplete diagnostic return
EOF
    ;;
  *) die "unknown mode: $MODE" ;;
esac
