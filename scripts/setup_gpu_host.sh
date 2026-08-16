#!/usr/bin/env bash
# 새 GPU 호스트 환경 구성 + **검증** — STEP3 격자/origin 앙상블 런을 돌릴 수 있는 상태로.
#
# ★ 왜 스크립트인가: 환경이 다르면 결과도 다르다.  손으로 깔면 무엇이 깔렸는지 기록이 안
#   남고, 나중에 "그 런이 어느 scipy 였나" 를 못 닫는다.  이 스크립트는 **버전을 고정**하고
#   **검증까지** 한 뒤 요약을 파일로 남긴다.
#
# ★ 이 파이프라인이 실제로 필요한 것 (측정해서 확인함):
#     · numpy · scipy            ← STEP3 유한체적 CG
#     · pyamg (선택)             ← AMG 전처리.  없으면 Jacobi 로 조용히 내려앉는다
#     · cupy  (선택, 강력 권장)  ← `--step3-gpu`.  87M dof 를 CPU CG 로 풀면 매우 느리다
#     · taichi 는 **불필요**     ← mpm_webapp_payload 는 taichi 를 import 하지 않는다
#                                  (MPM 압밀을 다시 돌릴 때만 필요.  침대가 있으면 안 쓴다)
#
# 사용:
#   bash ~/dem-sk/scripts/setup_gpu_host.sh            # 구성 + 검증
#   bash ~/dem-sk/scripts/setup_gpu_host.sh --check    # 검증만 (설치 안 함)
set -uo pipefail
CHECK_ONLY=0
[ "${1:-}" = "--check" ] && CHECK_ONLY=1
REPO="${REPO:-$HOME/dem-sk}"
VENV="${VENV:-$HOME/dem-venv}"
REPORT="$HOME/gpu_host_env_$(date +%Y%m%d_%H%M).txt"
FAIL=0

say() { printf '%s\n' "$*" | tee -a "$REPORT"; }
bad() { say "  ✗ $*"; FAIL=$((FAIL+1)); }
good() { say "  ✓ $*"; }

say "══ ① 호스트 ════════════════════════════════════════════"
say "  host   : $(hostname)  ·  $(date -Iseconds)"
say "  kernel : $(uname -r)"
say "  python : $(python3 -V 2>&1)"
PYMIN=$(python3 -c 'import sys;print(sys.version_info[1])')
if [ "$PYMIN" -lt 8 ]; then bad "python3.8 미만 — 지원 안 함"; else good "python 3.$PYMIN"; fi
say "  RAM    : $(free -g 2>/dev/null | awk '/^Mem:/{print $2" GiB (avail "$7" GiB)"}')"
RAMG=$(free -g 2>/dev/null | awk '/^Mem:/{print $7}')
say "  disk   : $(df -h "$HOME" | tail -1 | awk '{print $4" free of "$2}')"
if command -v nvidia-smi >/dev/null 2>&1; then
  say "  GPU    : $(nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader)"
  GPUMB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
  say "  CUDA   : $(nvidia-smi | sed -n 's/.*CUDA Version: *\([0-9.]*\).*/\1/p' | head -1)"
else
  bad "nvidia-smi 없음 — GPU 솔브 불가 (CPU 로만 가능, 매우 느림)"; GPUMB=0
fi

say ""
say "══ ② 이 격자가 들어가나 (셀당 158 B 실측 기준) ══════════"
python3 - "$GPUMB" "${RAMG:-0}" <<'PY' | tee -a "$REPORT"
import sys
gpu_mb = float(sys.argv[1] or 0); ram_gb = float(sys.argv[2] or 0)
lat, thick, B = 50.0, 117.5, 158
print(f'  {"vox":>7} {"셀":>9} {"필요":>8}   GPU {gpu_mb/1024:.0f} GB · RAM {ram_gb:.0f} GB')
for v in (0.4, 0.3, 0.25, 0.2, 0.15, 0.125):
    n = (lat/v)**2 * (thick/v); g = n*B/1024**3
    ok_gpu = '✓' if g < gpu_mb/1024*0.85 else ('⚠' if g < gpu_mb/1024 else '✗')
    ok_ram = '✓' if g < ram_gb*0.6 else ('⚠' if g < ram_gb else '✗')
    print(f'  {v:>7} {n/1e6:>8.0f}M {g:>7.1f}G   GPU {ok_gpu}   CPU/RAM {ok_ram}')
print('  ⚠ 0.85 여유를 두는 이유: CG 는 해 벡터 여러 개를 동시에 잡는다 (실측 여유 필요)')
PY

if [ "$CHECK_ONLY" = 0 ]; then
  say ""
  say "══ ③ venv + 의존 (버전 **고정**) ═══════════════════════"
  if [ ! -f "$VENV/bin/activate" ]; then
    python3 -m venv "$VENV" || { bad "venv 생성 실패 — python3-venv 를 깔 것"; }
  fi
  # shellcheck disable=SC1091
  . "$VENV/bin/activate" 2>/dev/null || bad "venv 활성화 실패"
  python3 -m pip install -q --upgrade pip setuptools wheel 2>&1 | tail -2 | tee -a "$REPORT"
  if [ "$PYMIN" -le 8 ]; then
    #  py3.8 마지막 지원 버전 — 위로 올리면 설치가 조용히 실패하거나 구버전으로 내려앉는다
    #  scikit-image 는 payload 의 **메쉬(시각화)** 경로가 쓴다.  없으면 강등되지만
    #  (viz_mpm_continuum.mesh_of, 2026-08-16) 있으면 브라우저 표면까지 나온다.
    PKGS="numpy==1.24.4 scipy==1.10.1 pyamg==4.2.3 scikit-image==0.19.3 pyflakes"
  else
    PKGS="numpy scipy pyamg scikit-image pyflakes"
  fi
  say "  설치: $PKGS"
  python3 -m pip install -q $PKGS 2>&1 | tail -3 | tee -a "$REPORT"
  # cupy — CUDA 메이저에 맞춰야 한다 (틀리면 import 는 되고 런타임에 죽는다)
  CUDA_MAJ=$(nvidia-smi 2>/dev/null | sed -n 's/.*CUDA Version: *\([0-9]*\).*/\1/p' | head -1)
  if [ -n "${CUDA_MAJ:-}" ]; then
    say "  cupy: CUDA $CUDA_MAJ 계열 → cupy-cuda${CUDA_MAJ}x"
    python3 -m pip install -q "cupy-cuda${CUDA_MAJ}x" 2>&1 | tail -3 | tee -a "$REPORT"
  fi
fi

say ""
say "══ ④ 검증 — 실제로 import 되고 도는가 ══════════════════"
# shellcheck disable=SC1091
[ -f "$VENV/bin/activate" ] && . "$VENV/bin/activate" 2>/dev/null
python3 - <<'PY' | tee -a "$REPORT"
mods = [('numpy', True), ('scipy', True), ('pyamg', False), ('cupy', False)]
for m, req in mods:
    try:
        mod = __import__(m)
        print(f'  ✓ {m:8s} {getattr(mod, "__version__", "?")}')
    except Exception as e:
        print(f'  {"✗" if req else "○"} {m:8s} 없음 ({type(e).__name__})'
              + ('  ← 필수' if req else '  ← 선택 (없으면 느려지거나 Jacobi 로 내려앉음)'))
try:
    import cupy as cp
    a = cp.arange(1000).sum()
    print(f'  ✓ cupy 실연산 OK (sum={int(a)})')
except Exception as e:
    print(f'  ○ cupy 실연산 불가: {type(e).__name__} — --step3-gpu 쓰지 말 것')
PY

say ""
say "══ 4b 실제 파이프라인 import — 목록이 아니라 **코드**에 물어본다 ═══════"
#  실사고 2026-08-16: 하드코딩한 의존 목록만 보고 넘어갔더니, 판별 런이 SE 점 6,800 만 개를
#  다 읽은 **뒤에** skimage 없음으로 죽었다.  GPU 시간을 그만큼 버렸다.
#  ⇒ 목록을 믿지 말고 **실제 모듈을 import** 해 본다.
IMPCHK="$REPO/scripts/_import_check.py"
cat > "$IMPCHK" <<'PYEOF'
import importlib, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
REQUIRED = ['step3_sigma', 'mpm_webapp_payload', 'viz_mpm_continuum', 'se_material',
            'additives', 'sr01_realbed_ab', 'sr01_stamp_compare', 'fibre_segment_raster']
OPTIONAL = [('skimage', 'mesh (browser surface) - omitted if absent, sigma unaffected'),
            ('cupy', 'GPU solve (--step3-gpu) - CPU CG otherwise'),
            ('pyamg', 'AMG preconditioner - Jacobi otherwise (slower)')]
bad = 0
for m in REQUIRED:
    try:
        importlib.import_module(m)
        print('  OK   ' + m)
    except Exception as e:
        bad += 1
        print('  FAIL ' + m + ': ' + type(e).__name__ + ': ' + str(e))
for m, what in OPTIONAL:
    try:
        importlib.import_module(m)
        print('  OK   ' + m + '   (' + what + ')')
    except Exception:
        print('  --   ' + m + ' absent -> ' + what)
sys.exit(1 if bad else 0)
PYEOF
if (cd "$REPO" && PYTHONUTF8=1 python3 "$IMPCHK" 2>&1 | tee -a "$REPORT"; exit "${PIPESTATUS[0]}"); then
  good "필수 모듈 전부 import 됨"
else
  bad "필수 모듈 import 실패 — 위 FAIL 참조"
fi
rm -f "$IMPCHK"

say ""
say "══ 4c 미정의 이름 (긴 런 뒤 NameError 방지) ═══════════"
if (cd "$REPO" && PYTHONUTF8=1 python3 scripts/check_undefined_names.py \
      scripts/mpm_webapp_payload.py scripts/step3_sigma.py scripts/viz_mpm_continuum.py \
      scripts/additives.py scripts/sr01_stamp_compare.py 2>&1 | tail -3 | tee -a "$REPORT"; \
    exit "${PIPESTATUS[0]}"); then
  good "런 경로에 미정의 이름 없음"
else
  bad "런 경로에 미정의 이름 — 위 참조"
fi

say ""
say "══ ⑤ 리포 selftest (전부 통과해야 런을 시작한다) ═══════"
for s in check_method_discipline fibre_1d_network sr01_staircase_factor \
         sr01_k_grid_sweep step3_transport_resolution sdcp_stamp_confound; do
  if [ ! -f "$REPO/scripts/$s.py" ]; then say "  ○ $s.py 없음 (리포가 낡았나)"; continue; fi
  R=$(cd "$REPO" && PYTHONUTF8=1 python3 "scripts/$s.py" --selftest 2>&1 | grep -oE '[0-9]+/[0-9]+ PASS' | tail -1)
  if [ -n "$R" ] && [ "${R%%/*}" = "$(echo "$R" | sed 's|.*/||;s| PASS||')" ]; then
    good "$s  $R"
  else
    bad "$s  ${R:-실패}"
  fi
done
R=$(cd "$REPO" && PYTHONUTF8=1 python3 scripts/check_method_discipline.py 2>&1 | tail -1)
say "  규율: $R"

say ""
say "══ ⑥ 침대 ═════════════════════════════════════════════"
for K in "$HOME/sdcp"/kit_*; do
  [ -d "$K" ] || continue
  RUN=""
  [ -e "$K/latest_run" ] && RUN="$K/latest_run"
  [ -z "$RUN" ] && for d in "$K"/run_*; do [ -f "$d/se_dump.npy" ] && RUN="$d"; done
  if [ -z "$RUN" ]; then bad "$(basename "$K"): 압밀된 런 없음 (se_dump.npy 부재)"; continue; fi
  MISS=""
  for f in se_dump.npy phase.npy fibre.npy fibre_dia.npy; do
    [ -f "$RUN/$f" ] || MISS="$MISS $f"
  done
  if [ -n "$MISS" ]; then say "  ⚠ $(basename "$K"): 없음 →$MISS"; else
    good "$(basename "$K"): $(du -sh "$RUN" 2>/dev/null | cut -f1)  ($(basename "$(readlink -f "$RUN")"))"
  fi
  [ -f "$K/run_mpm.sh" ] || bad "$(basename "$K"): run_mpm.sh 없음 — 러너가 payload 명령을 못 뽑는다"
done

say ""
if [ "$FAIL" = 0 ]; then
  say "✓ 준비 완료 (실패 0).  요약: $REPORT"
  say "  다음:  . $VENV/bin/activate  후 러너 실행"
else
  say "✗ 실패 $FAIL 건 — 위 ✗ 를 먼저 해결할 것.  요약: $REPORT"
fi
exit $((FAIL > 0))
