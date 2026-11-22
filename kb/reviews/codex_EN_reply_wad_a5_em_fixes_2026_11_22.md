---
title: "EN 회신 — W_ad a5 묶음 (EM 고침) 확인: NO-GO (P0 1 · P1 3 · P2 1 · P3 1) — EM 의 기존 반례는 막힘 · c2 재시작 실패 뒤 스케줄러 끊김을 --killed 경로가 놓쳐 c1 보조 채택"
date: 2026-11-22
updated: 2026-11-22
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, reply, letter]
letter: EN
track: wad
channel: codex
kind: reply
status: 수령 2026-11-22 (사용자 붙여넣기 + 첨부 둘) · NO-GO · 기준 68f683462 · MANIFEST 8439e129… · 고침 진행 (빌드 기록 ⑥)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-22). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖).
> 첨부 둘 (사용자 업로드) 은 `kb/reviews/codex_EN_evidence_2026_11_22/` 에 그대로: `em_probes.json` (sha256 34f1f443…) · `g5.log` (sha256 0bbc7f9f…).
> 회신이 가리키는 `independent.json` · `missing_start.json` · `terminal.json` 은 업로드되지 않았다 (Codex 쪽에만 있다).
> ⛔ 점착 W 값은 회신에 없다.

---

NO-GO — 커밋 68f683462, MANIFEST 8439e129…의 업체 발송은 보류하세요. EM이 제시한 기존 반례들은 막혔습니다. 다만 c2가 WAVECAR 재시작에 실패한 뒤 스케줄러에 의해 끊기면, 같은 실패를 --killed 경로에서 놓치고 c1 보조값을 자동 채택합니다.
발송을 막는 재현
c2에서 관측한 증거	러너가 끝까지 판정했을 때	모의 스케줄러로 7행 뒤 끊고 --killed로 회수했을 때
OUTCAR ISTART=0, ICHARG=2	종료 8 · RESTART_NOT_HONOURED · 채택 없음	종료 1 · NO_PRIMARY_VALUE · c1 보조 채택
c2에 허용되지 않은 OSZICAR 행 머리 XYZ:	종료 8 · SCF_UNVERIFIED · 채택 없음	종료 1 · NO_PRIMARY_VALUE · c1 보조 채택


P0 — 중단 처리에서 이미 관측된 모순을 버립니다. 러너는 killed.json이 있는 시도에서 행 수와 일부 설정만 확인하고 NEXT를 반환합니다. 검사기도 잘못된 행 머리를 식별하고서 행 수만 사용합니다. 최소 수정은 중단된 c단에서도 원문에 남은 행 형식과 재시작 증거를 검사하고, 모순이 있으면 STOPPED_FOR_REVIEW로 보내는 것입니다. 정상 재시작 후 허용된 행을 남기고 끊긴 양성 대조는 유지하면 됩니다. run_a5.sh:646 · 검사기:1305 · [독립 재현 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EN_20261122/independent.json)
함께 고칠 항목
등급	구체적 실패 시나리오	최소 수정
P1	반송본의 killed.json이 { 한 글자로 잘려도 c1 보조가 채택됐습니다. 별도 시험에서 늦은 infra_abort.json은 LADDER_VIOLATION이었지만, 그 파일만 빠지면 이전 attempt.json.t_end로 순서 검사를 통과해 OK가 됐습니다.	killed.json의 잡·단·`run_id`·행 수·기록 시각을 실제 시도와 대조하세요. run_aborted/의 시도에는 읽을 수 있는 중단 영수증과 기록 시각을 필수로 두세요. 검사기:1272 · 검사기:1532
P1	c1이 0행으로 멈춰 --infra-abort로 보존된 뒤 start_point.json만 유실되면, 재실행이 시작점을 다시 쓰고 c1 주값을 채택했습니다. 재현에서 SHA는 같았지만 새 기록은 이미 실행된 첫 c1보다 2초 늦었습니다.	시작점 최초 생성 전에 run_aborted/의 c1·c2까지 확인하세요. 검사기는 written_s가 최초 c단 시작보다 늦으면 보류해야 합니다. run_a5.sh:733 · [재현 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EN_20261122/missing_start.json)
P1	중간 PACK_ONLY 묶음이 남은 상태에서 최종 포장이 실패하면 종료 4입니다. 여기서 일반 재실행을 하면 새 단은 뜨지 않지만 종료 0과 함께 옛 묶음을 보내라고 안내합니다. 그 묶음에는 final.json이 없고 검사 결과는 LADDER_INCOMPLETE였습니다. PACK_ONLY=1로 다시 포장한 뒤에야 OK였습니다.	재실행 시 반송 묶음 안의 final.json과 현재 파일이 일치하는지 확인하세요. 불일치하면 종료 4와 재포장 안내를 유지하세요. run_a5.sh:461 · [재현 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EN_20261122/terminal.json)
P2	수집기에 c2.status=RUN_FAILED와 osz_rows=0 또는 행 수 결측을 함께 넘기면 두 경우 모두 c1 보조가 채택됐습니다. 검사기가 만든 정상 JSON에서는 0행이 먼저 걸립니다.	수집기의 독립 재검사에서도 RUN_FAILED에 정수 행 수 ≥1을 요구하세요. build_v5_vasp_package.py:1096
P3	README §3의 “지금 단이 미수렴 또는 실행 실패일 때만 다음 단”은 정상 A5 OK → c1에도 적용되는 문장입니다. 실제 러너는 이 경우 c1을 시작합니다.	A5 → c1의 시작점 선택 규칙과 c1 → c2의 진행 규칙을 두 문장으로 나누세요. README.md:44


Q-EN-1–6 판정
질문	판정	근거
1 · P0-1	기존 반례 GO, 전체 NO-GO	상한으로 c2 미실행, 준비만 한 c2, 0행 중단으로 보존된 c2 모두 LADDER_INCOMPLETE이고 채택도 없었습니다. 남은 경로는 위의 7행 중단입니다.
2 · P0-2	조건부	EM의 두 순서를 재실행해 모두 종료 7에서 멈추고, 올바른 중단 기록 뒤 c1 주값으로 회복했습니다. 뒤 단이 있을 때 앞 단의 --infra-abort·`--killed` 거부도 통과했습니다. 시작점·중단 영수증 유실 시의 순서 검증은 남습니다.
3 · P1-1~4	기존 네 항목 GO	수렴한 c1 뒤 재실행은 c2를 띄우지 않았습니다. 0행은 종료 7, 상대 W0는 정상 확인, 경로 오타는 종료 2였습니다. README의 W0 존재·크기·SHA 확인과 none 지침도 충분합니다. 종료 7에서 자동 포장하지 않는 운영은 수용합니다.
4 · P2·P3	조건부	시작점·인용 라벨 전달, 준비 실패 후 재시도, 타 호스트 잠금 거부, A5 설정 대조, 0행 표기, 혼합 폴더 거부는 확인했습니다. start_point.json은 c1 준비 전에 쓰입니다. 준비 실패로 c1 폴더가 없어도 파일이 남았고, 정상 재시도에서는 같은 바이트를 유지했습니다. 따라서 이 파일이 증명하는 것은 ‘시작점 선택’까지입니다.
5 · 새 결함	NO-GO	중단 경로의 잘못된 채택, 영수증 유실, 시작점 재생성, 오래된 반송 묶음 안내를 각각 재현했습니다.
6 · 업체 발송	NO-GO	위 P0·P1의 실패 사례가 수정본에서 차단되고, 정상 중단·재시도·재포장 대조가 계속 통과하는 것을 확인한 뒤 재승인할 수 있습니다.


검증 범위. Linux에서 재빌드한 배포본은 파일 단위로 일치했습니다. selftest는 a5 124/124 · V5 303/303 · round2 194/194, 최근 보강한 변이 m09·`m12`·`m18`은 3/3을 직접 재현했습니다. 전체 51개 변이는 제출 측 결과입니다. 실물 a4 재판독에서 전자 반복행 300/200과 이력 최댓값 44를 확인했고, 기존 G5 집계 JSON도 SHA afecfa08…까지 바이트 일치했습니다. 이번 중단 시험에는 모의 VASP를 사용했습니다. [EM 탐침 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EN_20261122/em_probes.json) · [G5 대조 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EN_20261122/g5.log)
