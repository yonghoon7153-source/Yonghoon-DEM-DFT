#!/usr/bin/env bash
# v42 산출물 셋 — 번들(zip) · IDENTITY_v42.json · SEND_MAIL_v42.md — 을 **현재 HEAD** 로 다시 만든다.
#   사용: (러너·렌더러 수정을 커밋한 뒤, clean tree 에서)   bash runs/sdcp_c12_2026_08_30/REGEN_v42.sh
#   생성기는 계보가 dirty 면 번들을 만들지 않는다 (회신 BC P0-1) — 그래서 커밋 뒤에 돌린다.
#   argv 는 IDENTITY_v41.json 의 generated_argv 를 **글자 그대로** 쓰고 --out 만 v42 다.
#   ⛔ 이 스크립트가 못 하는 것: 잡 입력이 v41 과 같은지 스스로 보증하지 않는다 — 아래 대조(byte-identical)가 그 몫이다.
set -u
cd "$(git rev-parse --show-toplevel)" || exit 1
D=runs/sdcp_c12_2026_08_30
GO=1
if [ -n "$(git status --porcelain -- tools/sdcp/vasp_handoff_bundle.py tools/sdcp/c12_render_send_mail.py tools/sdcp/c12_make_identity.py db/properties/c12_poses_2026_08_30.json db/governance/decisions.json)" ]; then
  echo "⛔ 생성 계보 파일이 dirty 다 — 먼저 커밋하십시오"; GO=0
fi
COMMIT=$(git rev-parse HEAD)
ARGV_JSON=$(python3 -c 'import json;a=json.load(open("runs/sdcp_c12_2026_08_30/IDENTITY_v41.json"))["generated_argv"];assert a[-2]=="--out";a[-1]="runs/sdcp_c12_2026_08_30/sdcp_c12_v42";print(json.dumps(a))')
mapfile -t ARGV < <(python3 -c 'import json,sys;[print(x) for x in json.loads(sys.argv[1])]' "$ARGV_JSON")
if [ "$GO" = 1 ]; then
  rm -rf "$D/sdcp_c12_v42" "$D/sdcp_c12_v42.zip"
  python3 tools/sdcp/vasp_handoff_bundle.py "${ARGV[@]}" || GO=0
fi
if [ "$GO" = 1 ]; then
  python3 tools/sdcp/vasp_handoff_bundle.py --verify_zip "$D/sdcp_c12_v42.zip" --expect_jobs 19 > /dev/null || { echo "⛔ verify_zip 실패"; GO=0; }
fi
if [ "$GO" = 1 ]; then
  # 잡 입력 동일성: v41 zip 대비 다른 파일은 스크립트·문서·MANIFEST·거버넌스 사본뿐이어야 한다
  T=$(mktemp -d); unzip -q "$D/sdcp_c12_v41.zip" -d "$T"
  DIFF=$(diff -rq "$T/sdcp_c12_v41" "$D/sdcp_c12_v42" | sed 's#.*/sdcp_c12_v41/##; s# and .*##')
  ALLOWED="MANIFEST.json README_REQUEST.md SUBMIT_CONTRACT.md governance/decisions.json run_staged.sh"
  for f in $DIFF; do case " $ALLOWED " in *" $f "*) ;; *) echo "⛔ v41 대비 허용 밖 차이: $f"; GO=0;; esac; done
  echo "v41 대비 다른 파일: $(echo $DIFF | tr '\n' ' ')"
  rm -rf "$T"
fi
if [ "$GO" = 1 ]; then
  python3 tools/sdcp/c12_make_identity.py --bundle "$D/sdcp_c12_v42" --zip "$D/sdcp_c12_v42.zip" --commit "$COMMIT" \
    --argv-json "$ARGV_JSON" --out "$D/IDENTITY_v42.json" \
    --checks "v41 과 잡 집합 동일(19잡, sha16 8a7ae28f) · 19잡 입력 파일 v41 zip 과 바이트 동일 · 회수본 7잡 입력 6파일 동일 · 러너 승계(SKIP_COMPLETE+CONTINUE_FROM) e2e 실물 픽스처 통과 · selftest 전부 통과" || GO=0
fi
if [ "$GO" = 1 ]; then
  python3 tools/sdcp/c12_render_send_mail.py --bundle "$D/sdcp_c12_v42" --zip "$D/sdcp_c12_v42.zip" --commit "$COMMIT" \
    --out "$D/SEND_MAIL_v42.md" --supersedes v41 --changes_md "$D/CHANGES_v42.md" \
    --continue_from_hint /home/kgy/projects/sdcp_c12_v41_2026_09_11/sdcp_c12_v41 \
    --supersede_reason "v41 러너는 같은 extraction 에서 다시 부르면 완주한 잡의 거부를 실패로 세어 2물결(nzmag 2잡)이 열리지 않았습니다 — 09-21 회신에 적어 주신 그대로이고 저희 결함입니다. v42 는 같은 19잡·같은 입력이며 러너·문서만 고쳤고, v41 에서 완주하신 7잡을 승계하는 절차(§1′)를 넣었습니다. 완주하신 7잡은 다시 돌리지 않습니다." || GO=0
fi
if [ "$GO" = 1 ]; then
  sha256sum "$D/sdcp_c12_v42.zip" "$D/sdcp_c12_v42/MANIFEST.json"
  echo "✅ REGEN 완료 (commit $COMMIT)"
else
  echo "⛔ REGEN 미완 — 위 메시지를 보십시오"
fi
