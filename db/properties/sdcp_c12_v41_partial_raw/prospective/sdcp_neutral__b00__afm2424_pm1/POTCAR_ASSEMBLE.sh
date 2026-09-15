#!/usr/bin/env bash
# 이 잡의 POTCAR 를 만든다. PBE PAW 5.4 세트 경로를 PP 로 준다.
#   PP=/path/to/potpaw_PBE.54 POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh
# ⚠ 종 순서는 이 잡 POSCAR 전용이다 — 다른 잡에 복사하지 말 것.
#   (하나를 돌려 쓰면 에러 없이 **다른 계**를 계산합니다.)
set -euo pipefail
# 🔴 회신 AB P0-8 — 종전엔 POTCAR 를 **제자리에서** 만들고 나중에 검사했다.
#   검사가 실패해 exit 1 이 나도 **완성된 POTCAR 는 남았고**, 이어지는
#   run_job.sh 가 그것으로 VASP 를 돌렸다 — allowlist 실패가 계산 중단으로
#   이어지지 않았다. 임시본에 조립·검증하고 통과 시에만 원자적으로 옮긴다.
trap 'rc=$?; if [ $rc -ne 0 ]; then rm -f POTCAR.tmp POTCAR POTCAR_PROVENANCE.json; echo "  ⛔ 실패 — POTCAR 를 남기지 않았습니다"; fi' EXIT
ORDER="Li_sv Ni_pv O S C H"
SPECIES="Li Ni O S C H"
: "${PP:?PP 를 지정하세요 (PBE PAW 5.4 세트 루트)}"
rm -f POTCAR POTCAR.tmp POTCAR_PROVENANCE.json
srcsha=""
for v in $ORDER; do
  f="$PP/$v/POTCAR"
  [ -f "$f" ] || { echo "⛔ 없음: $f"; exit 1; }
  srcsha="$srcsha $v:$(sha256sum "$f" | cut -d" " -f1)"
  cat "$f" >> POTCAR.tmp
done
# ① 개수
n=$(grep -ac TITEL POTCAR.tmp)
[ "$n" = 6 ] || { echo "⛔ TITEL 6개여야 하는데 $n개"; exit 1; }
# ② 자리별 variant — 토큰 전체 비교 (Ni 가 Ni_pv 에 오탐되지 않게)
i=0
for v in $ORDER; do
  i=$((i+1))
  got=$(grep -a TITEL POTCAR.tmp | sed -n "${i}p" | awk '{print $4}')
  fun=$(grep -a TITEL POTCAR.tmp | sed -n "${i}p" | awk '{print $3}')
  [ "$got" = "$v" ] || { echo "⛔ ${i}번째 TITEL 이 $got — $v 여야 합니다"; exit 1; }
  [ "$fun" = "PAW_PBE" ] || { echo "⛔ ${i}번째가 $fun — PAW_PBE 여야 합니다"; exit 1; }
done
# ③ trusted hash allowlist 대조 (회신 AA P0-2)
#    variant 이름·PAW_PBE·잡 간 일관성은 "전부 같은 잘못된 PP 트리" 를 못 막는다.
#    정본 SHA 는 라이선스상 우리가 못 싣는다 → **외주처 site-local 목록**을 받는다.
if [ -n "${POTCAR_ALLOWLIST:-}" ]; then
  [ -f "$POTCAR_ALLOWLIST" ] || { echo "⛔ allowlist 파일 없음: $POTCAR_ALLOWLIST"; exit 1; }
  for t in $srcsha; do
    v="${t%%:*}"; h="${t#*:}"
    # ★ 해시만 보면 안 된다 — **variant 와 묶여** 있어야 한다.
    #   Li_sv 와 Ni_pv 의 파일이 서로 바뀐 트리는 두 해시가 모두 목록에
    #   있으므로 해시 존재만으로는 통과한다 (2026-08-29 자체 검토).
    grep -E "^$h[[:space:]].*(^|[/[:space:]])$v(/|[[:space:]]|$)" \
         "$POTCAR_ALLOWLIST" > /dev/null || {
      echo "⛔ $v 가 allowlist 의 그 해시와 묶여 있지 않습니다"; echo "   $h";
      echo "   (목록 형식: sha256sum \$PP/<variant>/POTCAR 출력 그대로)"; exit 1; }
  done
  echo "  ✔ allowlist 대조 통과 ($POTCAR_ALLOWLIST)"
else
  echo "⛔ POTCAR_ALLOWLIST 가 지정되지 않았습니다."
  echo "   신뢰하는 PBE.54 세트의 sha256 목록을 **한 번** 만들어 전 잡에 같은"
  echo "   파일을 쓰세요 (잡마다 새로 만들면 아무것도 검증하지 않습니다):"
  echo "     for v in \$(ls \$PP); do sha256sum \$PP/\$v/POTCAR; done > site_allow.txt"
  echo "     POTCAR_ALLOWLIST=/abs/site_allow.txt bash POTCAR_ASSEMBLE.sh"
  echo "   ⛔ 면제(waiver)는 폐지했습니다 (회신 AB P0-8)."
  exit 1
fi
# ④ provenance — 이 파일을 결과와 **함께 반송**해 주세요
python3 - "$srcsha" <<'PY' > POTCAR_PROVENANCE.json
import hashlib, json, sys, os as _os
src = dict(t.split(":", 1) for t in sys.argv[1].split())
titel = [l.strip() for l in open("POTCAR.tmp", errors="ignore") if "TITEL" in l]
print(json.dumps({"schema": "potcar_provenance/v1",
                  "species_order": "Li Ni O S C H".split(),
                  "expected_variants": "Li_sv Ni_pv O S C H".split(),
                  "titel_lines": titel, "source_sha256": src,
                  "allowlist": _os.environ.get("POTCAR_ALLOWLIST"),
                  "allowlist_sha256": (hashlib.sha256(open(
                      _os.environ["POTCAR_ALLOWLIST"],"rb").read()).hexdigest()
                      if _os.environ.get("POTCAR_ALLOWLIST") and
                      _os.path.isfile(_os.environ["POTCAR_ALLOWLIST"]) else None),
                  "allowlist_waived": False,
                  "assembled_sha256": hashlib.sha256(
                      open("POTCAR.tmp","rb").read()).hexdigest()},
                 indent=1, ensure_ascii=False))
PY
mv POTCAR.tmp POTCAR
grep -a TITEL POTCAR
echo "✔ 조립 완료 — 종 순서 Li Ni O S C H · variant·순서·PAW_PBE 확인"
echo "  → POTCAR_PROVENANCE.json (결과와 함께 반송해 주세요)"
