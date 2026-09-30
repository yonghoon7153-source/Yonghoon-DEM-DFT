#!/usr/bin/env bash
# Phase A 재현 런 — 런 뒤 · 판정 전 (사전등록 §6-4 정정판 = §6 덧붙임 ② · 판정선 · 문턱 · 인자 불변)
set -euo pipefail
R=~/dem-vgcfE
D=20260927
HEADSHA=$(git -C "$R" rev-parse HEAD)
echo "repo HEAD $HEADSHA · 변경 파일 $(git -C "$R" status --short | wc -l)"

# ── 1. 격자별 .sh 고르기 — 러너 영수증 시각 (시작) ~ 그 격자 마지막 팔 JSON 시각 (격자는 순차 실행) ──
pick () {
  local O="$1" K="$2" N="$3" L n
  L=$(ls -t "$O"/p2_*.json | head -n 1 || true)
  rm -rf "$O/sh" && mkdir -p "$O/sh"
  find "$K" -name 'p2_*.sh' -newer "$O/run_receipt.json" ! -newer "$L" -exec cp -p {} "$O/sh/" \;
  n=$(ls "$O/sh" | wc -l)
  echo "$(basename "$O"): sh $n · $( (grep -ho 'vox_um=[0-9.]*' "$O"/sh/*.sh || true) | sort | uniq -c | tr -s ' ' | tr '\n' ' ')"
  [ "$n" -eq "$N" ] || { echo "⛔ $(basename "$O"): .sh $n 개 (기대 $N) — 멈춘다"; exit 3; }
}
pick ~/pa100/phaseA_v015_$D ~/pa100/kits 32
pick ~/pa100/phaseA_qc_v015_$D ~/pa100/kits 8
pick ~/pa100/phaseA_v020_$D ~/pa100/kits 32
pick ~/pa100/phaseA_v025_$D ~/pa100/kits 32
pick ~/pa010/phaseA_v015_$D ~/pa010/kits 32

# ── 2. .sh 영수증 (옆 폴더 sh_receipt/) — 러너 영수증은 덮지 않는다 · 러너가 선언한 축만 대조 (digest 는 arms 정의가 달라 비교 불가) · 로그 대조 없음 (팔별 로그 없음) ──
for spec in ~/pa100/phaseA_v015_$D:32 ~/pa100/phaseA_qc_v015_$D:8 ~/pa100/phaseA_v020_$D:32 ~/pa100/phaseA_v025_$D:32 ~/pa010/phaseA_v015_$D:32; do
  O=${spec%:*}; N=${spec##*:}
  RS=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('code_sha') or '')" "$O/run_receipt.json")
  if [ -z "$RS" ] || [[ "$HEADSHA" != "$RS"* ]]; then
    echo "⛔ $(basename "$O"): 러너 영수증 code_sha '$RS' 가 HEAD $HEADSHA 와 다르다 — 멈춘다"; exit 3
  fi
  python3 "$R/scripts/phase_a_receipt_from_sh.py" --sh "$O/sh" --out "$O/sh_receipt" \
    --code-sha "${HEADSHA:0:${#RS}}" --expect-arms "$N" --force
  python3 - "$O" "$R" <<'EOF'
import json, sys
sys.path.insert(0, sys.argv[2] + '/scripts'); import run_contract as RC
O = sys.argv[1]
a = json.load(open(O + '/run_receipt.json')); b = json.load(open(O + '/sh_receipt/run_receipt.json'))
#  러너가 **선언한** 축만 대조한다 (계약 검사기와 같은 규칙) — .sh 영수증은 러너가 안 적은 축을 기본값으로 채운다
keys = sorted([k for k in RC.RECEIPT_AXES if a.get(k) is not None] + ['code_sha', 'origins', 'expect_backend'])
diff = [f'{k}: 러너 {a.get(k)!r} ≠ .sh {b.get(k)!r}' for k in keys if a.get(k) != b.get(k)]
extra = sorted(f'{k}={b.get(k)!r}' for k in RC.RECEIPT_AXES if a.get(k) is None and b.get(k) is not None)
ra, rb = a.get('arms'), b.get('arms')
ok = isinstance(ra, int) and ra > 0 and isinstance(rb, int) and rb % ra == 0
print(f'  영수증 대조 — 러너 선언 축 {len(keys)} 개 중 차이 {len(diff)} · 팔 = 러너 {ra} (킷당) × {rb // ra if ok else "?"} 킷 = .sh {rb}',
      '→ 같음' if (ok and not diff) else '→ ⛔ 다름')
for d in diff:
    print('    ', d)
print('    (.sh 만 적은 축 — 대조 안 함:', ', '.join(extra) or '없음', ')')
sys.exit(0 if (ok and not diff) else 3)
EOF
done

# ── 3. 격자 로그 요약 (로그 대조 대신 기록) ──
for L in ~/pa100/step3_v015.log ~/pa100/step3_qc.log ~/pa100/step3_v020.log ~/pa100/step3_v025.log ~/pa010/step3_v015.log; do
  echo "== $L"
  grep -m 1 '^\[p2\] vox' "$L" || echo "  (머리줄 없음)"
  echo "  ABORT/FAILED/Traceback $(grep -cE 'ABORT|FAILED|Traceback' "$L" || true) · SKIP $(grep -c 'SKIP' "$L" || true) · 피크 줄 $(grep -c '피크 호스트 RSS' "$L" || true)"
done

# ── 4. 어댑터 (러너 영수증 = 기본 <dir>/run_receipt.json) ──
for O in ~/pa100/phaseA_v015_$D ~/pa100/phaseA_v020_$D ~/pa100/phaseA_v025_$D ~/pa010/phaseA_v015_$D; do
  python3 "$R/scripts/phase_a_arms_from_payload.py" --dir "$O" --out "${O}_arms"
done
python3 "$R/scripts/phase_a_arms_from_payload.py" --dir ~/pa100/phaseA_qc_v015_$D --out ~/pa100/phaseA_qc_v015_${D}_arms --role qc

# ── 5. 판정 (질문 1) — 팔은 …_arms/arms/ 에 있다 ──
VD=~/pa100/verdict_dir_$D
rm -rf "$VD" && mkdir -p "$VD"
cp ~/pa100/phaseA_v015_${D}_arms/arms/*.json ~/pa100/phaseA_v020_${D}_arms/arms/*.json \
   ~/pa100/phaseA_v025_${D}_arms/arms/*.json ~/pa100/phaseA_qc_v015_${D}_arms/arms/*.json "$VD"/
echo "판정 폴더 팔 $(ls "$VD" | wc -l) (기대 104)"
[ "$(ls "$VD" | wc -l)" -eq 104 ] || { echo "⛔ 104 가 아니다 — 멈춘다"; exit 3; }
python3 "$R/scripts/phase_a_order_verdict.py" --dir "$VD" --out ~/pa100/verdict_G100.json

# ── 6. 짝 비교 (질문 2 · 3) ──
python3 "$R/scripts/phase_a_pair_e_arms.py" --a ~/pa100/phaseA_v015_${D}_arms/arms --b ~/pa010/phaseA_v015_${D}_arms/arms \
  --label-a E100 --label-b E010 --band-pct 1.0 --expect-pairs 32 --out ~/pa100/pair_E100_E010.json
python3 "$R/scripts/phase_a_pair_e_arms.py" --a ~/pa010/phaseA_v015_${D}_arms/arms \
  --b "$R/docs/data/phase_a_104arms_20260921/arms_primary_v015_20260921/arms" \
  --label-a E010_kgy --label-b E010_v100_0921 --band-pct 0.5 --expect-pairs 32 --out ~/pa100/pair_E010_vs_0921.json
echo "완료 — 다음: tgz 묶기"
