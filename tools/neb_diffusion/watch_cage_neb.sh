#!/bin/bash
# watch_cage_neb.sh — argyrodite_cage_neb.py (UMA CI-NEB) 라이브 상태.
#
# 왜 이 파일인가 (2026-08-20, 코드 규율 사다리 확인)
#   기존 watch_*.sh 는 전부 다른 대상이다: watch_gabia_sdcp.sh/watch_li3n_*.sh 는
#   QE .out(`^!` 총에너지·"JOB DONE") 을 읽고, watch_b2o3_md.sh 는 MD msd.json 을 센다.
#   이 계산은 **ASE FIRE 로그**(스텝·fmax)라 파싱 대상이 아예 다르다 — 확장이 아니라 신설.
#
# 무엇을 보나
#   ① GPU 점유 (pw.x 와 동거 중이면 OOM 위험 — 남은 VRAM 을 경고로 찍는다)
#   ② 프로세스 생존 (죽었는데 로그만 남은 상태를 구분)
#   ③ NEB FIRE 진행: 스텝/400, fmax vs 목표, 최근 추세(제자리인지), 스텝 속도·ETA
#   ④ band → CI 단계 전환 (로그의 헤더 줄 개수로 판별)
#   ⑤ 끝난 판: argyrodite_cage_neb.json 의 누적 기록
#
# 이 도구가 **못 하는 것**
#   · 장벽이 맞는지 판정하지 않는다. 수렴 진행만 본다.
#   · fmax 가 목표 밑으로 내려가도 그게 물리적으로 옳은 경로라는 뜻이 아니다
#     (협동 이동·밴드 불연속 경고는 본 스크립트 print 가 아니라 nohup.out 에 있다).
#   · ETA 는 최근 구간의 산술 외삽이다. FIRE 는 후반이 느려져서 대개 낙관적이다.
#   · 로그가 없으면(끝점 이완 단계) 진행률을 알 수 없다 — nohup.out tail 로만 본다.
#
# 설치·사용 (gabia)
#   위 내용을 /root/watch_cage_neb.sh 로 저장 후:
#     watch -n 30 bash /root/watch_cage_neb.sh
#   저장소 위치가 다르면: REPO=/경로 watch -n 30 bash /root/watch_cage_neb.sh
#
#   python3 tools/neb_diffusion/watch_cage_neb.sh --selftest   # 아래 셀프테스트 참조
#   bash tools/neb_diffusion/watch_cage_neb.sh --selftest

R="${REPO:-/data/work/repo}"
P="$R/db/properties"
FMAX_BAND=0.05
FMAX_CI=0.03
STEPS_MAX=400

# ── 셀프테스트: 가짜 FIRE 로그로 파서를 검증한다 (음성 경로 포함) ──────────────
if [ "$1" = "--selftest" ]; then
    T=$(mktemp -d); ok=1
    # ⚠ 반드시 return 0 — 호출부가 `... && say "✓" || say "✗"` 라서 say 가 비영으로
    #   끝나면 성공 케이스에서도 || 가지가 함께 터진다 (첫 판에서 실제로 그랬다).
    say() { echo "  $1 $2"; if [ "$1" = "✗" ]; then ok=0; fi; return 0; }

    # 양성 ①: band 단계, 헤더 1개
    cat > "$T/a.log" <<'EOF'
      Step     Time          Energy          fmax
FIRE:    0 15:04:22     -456.789012        1.2345
FIRE:    1 15:04:35     -456.812345        0.9876
FIRE:    2 15:04:48     -456.850000        0.4400
EOF
    n=$(grep -ac 'Step.*Time.*Energy.*fmax' "$T/a.log")
    [ "$n" = "1" ] && say "✓" "band 단계 판별 (헤더 1개)" || say "✗" "band 판별 실패: $n"
    f=$(grep -a '^FIRE:' "$T/a.log" | tail -1 | awk '{print $NF}')
    [ "$f" = "0.4400" ] && say "✓" "최신 fmax 추출 0.4400" || say "✗" "fmax 추출 실패: $f"
    s=$(grep -a '^FIRE:' "$T/a.log" | tail -1 | awk '{print $2}')
    [ "$s" = "2" ] && say "✓" "스텝 추출 2" || say "✗" "스텝 추출 실패: $s"

    # 양성 ②: CI 단계 = 헤더 2개 + 스텝 리셋
    cat "$T/a.log" > "$T/b.log"
    cat >> "$T/b.log" <<'EOF'
      Step     Time          Energy          fmax
FIRE:    0 15:20:00     -456.850000        0.0490
FIRE:    1 15:20:14     -456.851000        0.0250
EOF
    n=$(grep -ac 'Step.*Time.*Energy.*fmax' "$T/b.log")
    [ "$n" = "2" ] && say "✓" "CI 단계 판별 (헤더 2개)" || say "✗" "CI 판별 실패: $n"

    # 양성 ③: 에너지에 '*' 가 붙어도 fmax 는 마지막 필드다 (ASE force-consistent 표기)
    printf 'FIRE:    3 15:05:01     -456.900000*       0.1100\n' >> "$T/a.log"
    f=$(grep -a '^FIRE:' "$T/a.log" | tail -1 | awk '{print $NF}')
    [ "$f" = "0.1100" ] && say "✓" "에너지 '*' 표기에도 fmax 정상" || say "✗" "'*' 처리 실패: $f"

    # 음성 ①: FIRE 줄이 없는 로그를 "진행 중"으로 오판하면 안 된다
    printf 'some ase warning\nnothing here\n' > "$T/c.log"
    f=$(grep -a '^FIRE:' "$T/c.log" | tail -1 | awk '{print $NF}')
    [ -z "$f" ] && say "✓" "FIRE 줄 없는 로그를 진행으로 오판하지 않음" || say "✗" "오판: '$f'"

    # 음성 ②: 정체 판별 — 최근 10스텝 fmax 가 안 줄면 잡아내야 한다
    : > "$T/d.log"
    for i in $(seq 0 12); do printf 'FIRE:  %3d 16:00:%02d   -400.0   0.3300\n' "$i" "$i" >> "$T/d.log"; done
    a=$(grep -a '^FIRE:' "$T/d.log" | tail -11 | head -1 | awk '{print $NF}')
    b=$(grep -a '^FIRE:' "$T/d.log" | tail -1 | awk '{print $NF}')
    awk -v a="$a" -v b="$b" 'BEGIN{exit !(a<=b)}' \
        && say "✓" "정체(감소 없음) 검출" || say "✗" "정체를 진행으로 오판"

    # 음성 ③: NUL 오염 로그에서도 grep -a 라 읽혀야 한다
    printf 'FIRE:    9 17:00:00   -400.0   0.2000\n' > "$T/e.log"
    printf '\0\0\0' >> "$T/e.log"
    f=$(grep -a '^FIRE:' "$T/e.log" | tail -1 | awk '{print $NF}')
    [ "$f" = "0.2000" ] && say "✓" "NUL 오염 로그도 grep -a 로 읽힘" || say "✗" "NUL 처리 실패: $f"

    # 음성 ④: 스텝이 리셋됐는데 헤더가 1개면 CI 라고 부르면 안 된다
    n=$(grep -ac 'Step.*Time.*Energy.*fmax' "$T/a.log")
    [ "$n" = "1" ] && say "✓" "헤더 1개면 CI 라 부르지 않음" || say "✗" "단계 오판: $n"

    rm -rf "$T"
    [ "$ok" = 1 ] && { echo "selftest PASS"; exit 0; } || { echo "selftest FAIL"; exit 1; }
fi

echo "════════ $(date '+%m-%d %H:%M:%S')  gabia — argyrodite cage NEB (UMA) ════════"

# ── ① GPU ───────────────────────────────────────────────────────────────────
if command -v nvidia-smi >/dev/null 2>&1; then
    read -r USED TOT <<<"$(nvidia-smi --query-gpu=memory.used,memory.total \
                           --format=csv,noheader,nounits | head -1 | tr -d ',')"
    FREE=$(( TOT - USED ))
    printf "■ GPU  %s / %s MiB  (여유 %s MiB)" "$USED" "$TOT" "$FREE"
    [ "$FREE" -lt 3000 ] && printf "  ⚠ 여유 3 GB 미만 — OOM 위험"
    echo
    nvidia-smi --query-compute-apps=pid,used_memory,process_name \
               --format=csv,noheader 2>/dev/null |
        awk -F', ' '{printf "   pid %-8s %-10s %s\n",$1,$2,$3}'
else
    echo "■ GPU  (nvidia-smi 없음)"
fi

# ── ② 프로세스 생존 ─────────────────────────────────────────────────────────
PIDS=$(pgrep -af 'argyrodite_cage_neb' 2>/dev/null | grep -v 'watch_cage_neb' | awk '{print $1}')
if [ -n "$PIDS" ]; then
    echo "■ 프로세스  ✅ 살아있음  pid: $(echo "$PIDS" | tr '\n' ' ')"
else
    echo "■ 프로세스  ⛔ 없음 — 끝났거나 죽었다 (아래 로그·nohup.out 으로 구분)"
fi

# ── ③④ NEB 진행 ────────────────────────────────────────────────────────────
echo "■ NEB 진행 (db/properties/neb_*.log)"
shopt -s nullglob
LOGS=("$P"/neb_*.log)
if [ ${#LOGS[@]} -eq 0 ]; then
    echo "   (로그 없음 — 아직 끝점 이완 단계이거나 시작 전. nohup.out 참조)"
else
    for L in "${LOGS[@]}"; do
        # 24시간 넘게 안 건드린 로그는 옛 판이므로 한 줄로만
        if [ -n "$(find "$L" -mmin +1440 2>/dev/null)" ]; then
            echo "   $(basename "$L" .log)  (24h+ 정지 — 옛 판)"
            continue
        fi
        NH=$(grep -ac 'Step.*Time.*Energy.*fmax' "$L")
        if [ "$NH" -ge 2 ]; then PHASE="CI"; TGT=$FMAX_CI; else PHASE="band"; TGT=$FMAX_BAND; fi
        LAST=$(grep -a '^FIRE:' "$L" | tail -1)
        if [ -z "$LAST" ]; then
            echo "   $(basename "$L" .log)  [$PHASE] 아직 첫 스텝 전"
            continue
        fi
        STEP=$(echo "$LAST" | awk '{print $2}')
        FMAX=$(echo "$LAST" | awk '{print $NF}')
        AGO=$(grep -a '^FIRE:' "$L" | tail -11 | head -1 | awk '{print $NF}')
        # 현재 단계의 스텝 속도 (마지막 헤더 이후 구간만)
        RATE=$(grep -a '^FIRE:' "$L" | tail -30 |
               awk '{split($3,t,":"); s=t[1]*3600+t[2]*60+t[3];
                     if(NR==1){s0=s;n0=$2} sN=s; nN=$2}
                    END{d=sN-s0; if(d<0)d+=86400; k=nN-n0;
                        if(k>0&&d>0) printf "%.1f", d/k; else printf ""}')
        AGE=$(( ( $(date +%s) - $(stat -c %Y "$L") ) / 60 ))
        printf "   %-28s [%s] step %s/%s  fmax %s → 목표 %s" \
               "$(basename "$L" .log)" "$PHASE" "$STEP" "$STEPS_MAX" "$FMAX" "$TGT"
        awk -v f="$FMAX" -v t="$TGT" 'BEGIN{if(f+0<=t+0) printf "  ✅ 도달"}'
        echo
        printf "        10스텝 전 %s → 지금 %s" "${AGO:-–}" "$FMAX"
        [ -n "$AGO" ] && awk -v a="$AGO" -v b="$FMAX" \
            'BEGIN{if(a+0<=b+0) printf "  ⚠ 감소 없음 (제자리 의심)"}'
        echo
        if [ -n "$RATE" ]; then
            REM=$(( STEPS_MAX - STEP ))
            awk -v r="$RATE" -v n="$REM" 'BEGIN{printf "        %.1f s/step · 남은 %d스텝 최대 %.1f h (FIRE 후반은 더 느려진다)\n", r, n, r*n/3600}'
        fi
        printf "        로그 갱신 %s분 전" "$AGE"
        [ "$AGE" -gt 30 ] && printf "  ⚠ 30분 넘게 무갱신"
        echo
    done
fi

# ── ⑤ 끝난 판 ──────────────────────────────────────────────────────────────
J="$P/argyrodite_cage_neb.json"
if [ -s "$J" ]; then
    echo "■ 완료 기록 ($J)"
    python3 - "$J" <<'PY' 2>/dev/null || echo "   (json 파싱 실패 — 쓰기 중일 수 있다)"
import json, sys
db = json.load(open(sys.argv[1]))
runs = db.get("runs", [])
print(f"   누적 {len(runs)}건")
for r in runs[-6:]:
    ea = r.get("Ea_forward_eV", r.get("Ea_eV"))
    ci = r.get("ci_converged"); bc = r.get("band_converged")
    mark = "✅" if ci else ("△band만" if bc else "⛔미수렴")
    print(f"   {r.get('tag','?'):28s} {mark}  Ea(정) "
          f"{ea if ea is None else format(ea,'.4f')} eV  "
          f"steps {r.get('steps_band','?')}+{r.get('steps_ci','?')}")
PY
else
    echo "■ 완료 기록  (아직 없음)"
fi

# ── nohup.out 최근 단계 ────────────────────────────────────────────────────
for N in "$R/nohup.out" /root/nohup.out; do
    [ -s "$N" ] || continue
    echo "■ $N 최근 5줄"
    grep -a . "$N" | tail -5 | sed 's/^/   /'
    break
done
