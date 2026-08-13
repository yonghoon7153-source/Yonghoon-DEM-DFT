#!/usr/bin/env bash
# V100 반납 전 **수확** — 재생성 불가한 것부터 작은 tarball 하나로.
#
# 우선순위 (재생성 가능성 기준):
#   ★★★ 측정값·매니페스트·로그·**실제 실행된 명령**  → 재생성 불가.  이 스크립트가 담는다.
#   ★★  침대 (se_dump/fibre/fibre_dia/phase/am_scaffold) → 킷에서 **결정론적 재생성 가능**
#        (CL-10 에서 확인: porosity 7.386→7.368 %, thickness 72.484→72.534 µm).
#        단 압밀에 ~2 h GPU 씩 든다 → 용량이 되면 같이 가져갈 것 (아래 ② 참조).
#   ★   payload 점군 (140 MB×N) → 침대에서 재생성.  기본 제외.
#
# 사용 (V100):
#   bash ~/dem-sk/scripts/harvest_v100.sh
#   # → ~/v100_harvest_<날짜>.tar.gz  (수 MB)
set -uo pipefail
OUT="$HOME/v100_harvest_$(date +%Y%m%d_%H%M).tar.gz"
STAGE="$(mktemp -d)"
mkdir -p "$STAGE/logs" "$STAGE/cmds" "$STAGE/metrics"

echo "══ ① 측정값 추출 (payload → step3 블록만) ═══════════════"
python3 - "$STAGE/metrics" <<'PY'
import glob, json, os, sys
dst = sys.argv[1]
roots = [os.path.expanduser('~/sdcp'), os.path.expanduser('~/Yonghoon-DEM-DFT/se_curve')]
n = 0
for root in roots:
    for f in glob.glob(os.path.join(root, '**', 'mpm_payload*.json'), recursive=True):
        try:
            d = json.load(open(f))
        except Exception as e:
            print(f'  ⚠ 못 읽음 {f}: {e}'); continue
        s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}
        m = d.get('mpm_metrics') or {}
        small = {'_src': os.path.relpath(f, os.path.expanduser('~')),
                 '_bytes': os.path.getsize(f),
                 '_mtime': os.path.getmtime(f),
                 'step3': {k: v for k, v in s.items()
                           if k not in ('phi', 'cond') and not isinstance(v, list)},
                 'manifest': s.get('manifest'),
                 'porosity_settled_pct': m.get('porosity_settled_pct'),
                 'thickness_um': m.get('thickness_um'),
                 'n_grid': m.get('n_grid'), 'nz': m.get('nz'), 'n_pts': m.get('n_pts'),
                 'am_load_split': m.get('am_load_split'),
                 'coverage_boundary': m.get('coverage_boundary')}
        name = (os.path.relpath(f, os.path.expanduser('~'))
                .replace('/', '__').replace('.json', '.small.json'))
        json.dump(small, open(os.path.join(dst, name), 'w'), ensure_ascii=False, indent=1,
                  default=str)
        n += 1
print(f'  {n} payload → step3 요약 추출')
PY

echo "══ ② 로그 · 실제 실행된 명령 ═══════════════════════════"
for d in "$HOME/sdcp" "$HOME/Yonghoon-DEM-DFT/se_curve"; do
  [ -d "$d" ] || continue
  find "$d" -maxdepth 3 \( -name '*.log' -o -name 'g5_*.sh' -o -name 'gc*.sh' \
       -o -name 'payload_*.sh' -o -name 'run_mpm.sh' -o -name 'mpm_done.marker' \) \
       -size -20M 2>/dev/null | while read -r f; do
    rel="${f#$HOME/}"; rel="${rel//\//__}"
    case "$f" in *.log) cp "$f" "$STAGE/logs/$rel" ;; *) cp "$f" "$STAGE/cmds/$rel" ;; esac
  done
done
echo "  로그 $(ls -1 "$STAGE/logs" 2>/dev/null | wc -l) · 명령 $(ls -1 "$STAGE/cmds" 2>/dev/null | wc -l)"

echo "══ ③ 침대 지문 (재생성 검증용) ═════════════════════════"
python3 - "$STAGE" <<'PY'
import glob, hashlib, json, os, sys
out = {}
for f in sorted(glob.glob(os.path.expanduser('~/sdcp/**/*.npy'), recursive=True)
                + glob.glob(os.path.expanduser('~/Yonghoon-DEM-DFT/se_curve/**/*.npy'),
                            recursive=True)
                + glob.glob(os.path.expanduser('~/sdcp/**/*scaffold*.csv'), recursive=True)):
    h = hashlib.md5()
    with open(f, 'rb') as fh:                     # 앞 8 MB 만 — 지문이면 충분하고 빠르다
        h.update(fh.read(8 << 20))
    out[os.path.relpath(f, os.path.expanduser('~'))] = {
        'md5_head8M': h.hexdigest(), 'bytes': os.path.getsize(f)}
json.dump(out, open(os.path.join(sys.argv[1], 'bed_fingerprints.json'), 'w'), indent=1)
tot = sum(v['bytes'] for v in out.values())
print(f'  {len(out)} 파일 · 총 {tot/2**30:.2f} GiB  (지문만 저장; 실물은 ② 로 별도 판단)')
PY

echo "══ ④ 환경 ═════════════════════════════════════════════"
{ echo "date: $(date -Iseconds)"; echo "host: $(hostname)";
  echo "dem-sk HEAD: $(git -C "$HOME/dem-sk" rev-parse --short HEAD 2>/dev/null)";
  echo "python: $(python3 -V 2>&1)";
  python3 -c "import numpy,scipy;print('numpy',numpy.__version__,'scipy',scipy.__version__)" 2>&1
  command -v nvidia-smi >/dev/null && nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
  echo "--- disk ---"; df -h "$HOME" | tail -1; } > "$STAGE/env.txt" 2>&1

tar -czf "$OUT" -C "$STAGE" .
rm -rf "$STAGE"
echo
echo "✓ $OUT  ($(du -h "$OUT" | cut -f1))"
echo
echo "── 로컬에서 받기 ──────────────────────────────────────"
echo "  scp v100:$(basename "$OUT") ."
echo
echo "── ② 침대 실물 (선택) — 용량 크지만 압밀 ~2 h/침대 절약 ──"
for d in "$HOME/sdcp"/kit_* "$HOME/Yonghoon-DEM-DFT/se_curve"/kit_*; do
  [ -d "$d" ] || continue
  printf '  %-52s %s\n' "${d#$HOME/}" "$(du -sh "$d" 2>/dev/null | cut -f1)"
done
echo "  예:  rsync -avP --include='*/' --include='se_dump.npy' --include='fibre*.npy' \\"
echo "         --include='phase.npy' --include='*scaffold*.csv' --exclude='*' \\"
echo "         v100:~/sdcp/ ./v100_beds/"
