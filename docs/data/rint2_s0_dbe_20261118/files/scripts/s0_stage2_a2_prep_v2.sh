# S0 단계 2 두 번째 시도 준비 2 판 (11-18 · kgy) — 옛 침대 = 러너 규칙이 kgy 에서 고르는 런 (원본 쓰기 0 · 보기 링크만 다시 잇기)
# 1 판 사전 점검 = 08-12 런에 fibre_kind 없음 (거부) · 러너 (sdcp_gain_vox015_8arm.sh run_arm) 는 죽은 latest_run 을 '없음' 으로 보고 마지막 run_* 를 쓴다
set -u
O=$HOME/sdcp/kit_DBE; V=$HOME/sdcp/s0view_20261118/kit_DBE; N=$HOME/sdcp/kit_DBE_sdcp1um_vgcf100
L=$HOME/sdcp/ca1_logs; D=$HOME/sdcp/ca1_s0_dbe; S1=$HOME/s0_stage2_20261118.sh; S2=$HOME/s0_stage2_20261118_a2.sh
fail(){ echo "⛔ $* — 여기서 멈춤 (발사 안 함)"; exit 1; }
pgrep -af '^[^ ]*python[0-9.]* [^ ]*ca_s0_census[.]py' && fail "S0 프로세스가 아직 돈다"
echo "== 1. 옛 kit_DBE 런 폴더 (읽기만) =="
for d in "$O"/run_*/; do echo "$(basename "$d") · se_dump $([ -f "$d/se_dump.npy" ] && echo 있음 || echo 없음) · kind: $(cd "$d" && ls *_kind.npy 2>/dev/null | tr '\n' ' ')"; done
echo "== 2. 러너 규칙 (run_arm 첫 줄 그대로) 이 고르는 런 =="
KIT=$O
if [ -e "$KIT/latest_run" ]; then RUN="$(cd "$KIT/latest_run" && pwd)"
else
  RUN=""; for d in "$KIT"/run_*; do [ -f "$d/se_dump.npy" ] && RUN="$(cd "$d" && pwd)"; done
fi
[ -n "$RUN" ] || fail "러너 규칙으로도 런 없음"
echo "러너가 고르는 런 = $(basename "$RUN")"
echo "== 3. 보기 latest_run 을 그 런으로 (보기 = 1 판이 만든 링크 폴더 · 원본 쓰기 0) =="
[ -d "$V" ] || fail "보기 폴더가 없다: $V"
[ -z "$(find "$V" -mindepth 1 -maxdepth 1 -not -type l)" ] || fail "보기 폴더에 링크가 아닌 것이 있다"
ln -sfn "$RUN" "$V/latest_run" || fail "latest_run 다시 잇기"
echo "보기 latest_run -> $(readlink "$V/latest_run") · 원본 latest_run -> $(readlink "$O/latest_run")"
echo "== 4. 사전 점검 (census 와 같은 입력 함수 · 새 침대 · 옛 침대) =="
cd "$HOME/dem-ca1" && . "$HOME/dem-venv/bin/activate" || fail venv
python3 - "$N" "$V" <<'PY' || fail "사전 점검 실패"
import sys, os
sys.path.insert(0, 'scripts')
import ca_s0_census as C
for p in sys.argv[1:]:
    rec = C.kit_input_record(p)
    print(os.path.basename(p), 'run', os.path.basename(C.find_run_dir(p)))
    for role, x in sorted(rec['files'].items()):
        print('  ', role, x['bytes'], x['sha256'][:16], x['path'].replace(os.path.expanduser('~'), '~'))
    print('   metrics', rec['metrics'], 'settings', (rec['settings_sha256'] or '')[:16])
PY
echo "== 5. 새 스크립트 (옛 침대 경로만 보기로 · 나머지 첫 스크립트와 같음) =="
for p in "${D}_a1" "$L/s0_stage2_a1.log" "$L/s0_stage2_a1_nohup.out" "$S2"; do [ -e "$p" ] && fail "이미 있다: $p"; done
sed "s#--kit ~/sdcp/kit_DBE --out#--kit $V --out#" "$S1" > "$S2"
[ "$(grep -c -- "--kit $V --out" "$S2")" = 1 ] || fail "새 스크립트 치환"
diff "$S1" "$S2"
echo "== 6. 첫 시도 기록 옆으로 (지우지 않음) → 발사 =="
if [ -e "$D" ]; then mv "$D" "${D}_a1" || fail "mv $D"; fi
mv "$L/s0_stage2.log" "$L/s0_stage2_a1.log" && mv "$L/s0_stage2_nohup.out" "$L/s0_stage2_a1_nohup.out" || fail "로그 이름 바꾸기"
nohup bash "$S2" > "$L/s0_stage2_nohup.out" 2>&1 &
sleep 15; echo "발사 · S0 프로세스 $(pgrep -f '^[^ ]*python[0-9.]* [^ ]*ca_s0_census[.]py' | wc -l) 개 (1 이면 정상) · 보기: tail -f $L/s0_stage2.log"
