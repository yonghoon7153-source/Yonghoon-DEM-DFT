---
title: "EQ 회신 — W_ad a5 묶음 (EP 고침) 확인: NO-GO — EP 원래 반례는 막힘 · 위협 범위 §1b 수용 (GO) · 범위 안 지적: 앞 공백 두 칸 뒤 'SDA' 절단 → 0 스텝 · 310 자리 숫자 행 → RUN_FAILED · 648,001 s 완료 시도에 남의 killed.json → c2 채택 · run/ 하나를 옛 체크포인트로 복구하면 유효한 기존 반송본을 덮어씀 · 0 바이트 status.tsv · 잘린 종료 기록으로 계속 · 재포장이 현장 오류를 지움 · final.json code 0 + REVIEW · 공백 세 칸 잡 ID · 저장 뒤 사유 바이트 손상"
date: 2026-11-23
updated: 2026-11-23
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, reply, letter]
letter: EQ
track: wad
channel: codex
kind: reply
status: 수령 2026-11-23 (사용자 붙여넣기 · 첨부 둘) · NO-GO · 기준 891e106e5 · MANIFEST 679d7050… · Q-EQ-7 위협 범위 GO · 재승인 핵심 = 남의 killed.json 으로 상한을 못 넘김 · 복구 중 이전 완료 반송본을 안 덮음 · 깨진 기록은 다음 실행 · 재포장 전에 멈춤 → 고침 (빌드 기록 ⑫)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-23). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖).
> 첨부 둘 (사용자 업로드) 은 `kb/reviews/codex_EQ_evidence_2026_11_23/` 에 그대로: `selected_mutants.log` (sha256 3ebb5a4e…) · `g5.log` (sha256 34f1f443… — EN 때 g5.log 와 같은 바이트). 원문의 `eq_edges.json` · `eq_probes.json` · `eq_snapshot.json` 은 업로드되지 않았다.
> 편지: `codex_EQ_prompt_wad_a5_ep_fixes_2026_11_23.md` (기준 0fbc49760 → 고침 a97eba79f · 891e106e5 · MANIFEST 679d7050… · 위협 범위 §1b).

---

NO-GO — 커밋 `891e106e5`, MANIFEST `679d7050…`의 업체 발송은 보류하세요. EP에서 제시한 원래 반례는 막혔습니다. 하지만 648,001초가 걸린 완료 시도에 다른 시도의 `killed.json` 한 장을 복사하면 c2가 실행되고 채택됩니다. 또 운영자가 `run/` 폴더 하나를 이전 체크포인트로 복구하면, 러너가 해시가 유효한 기존 반송본을 덮어쓰는 것까지 재현했습니다.
Q-EQ-1 · 전자 반복행 — NO-GO, P0 · 범위 안

* 기존의 숫자 없는 `SDA:` 행과 열 첫 칸에서 끊긴 `SDA`는 이제 종료 8·미채택입니다. 보존된 V5 실물 OSZICAR 20개에서도 DAV/RMM 2,733행 전부가 새 판독기를 통과했습니다. 6필드 100행, 7필드 2,633행입니다.
* 첫 전자행 앞에 공백 두 칸만 붙이면 판정이 뒤집힙니다. c2의 마지막 바이트가 `SDA`이면 `--infra-abort`가 0스텝으로 접수하고, 재실행한 c2가 `OK`로 채택됩니다. `SDA`와 `SDA:`는 둘 다 정확히 막혔습니다. 완전한 행에는 들여쓰기를 허용하므로, 잘린 행도 같은 기준으로 읽어야 합니다. 선행 공백을 걷은 뒤 해당 단계의 `SDA`·`CGA` 등 허용 머리의 접두어인지 보세요. 실제 열 제목의 시작인 `N`은 0스텝으로 유지할 수 있습니다. [러너 435–447행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L435) · [독립 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_edges.json)
* 두 자리 지수는 미확인 형식을 검토로 보내는 운영 기준으로 유지해도 됩니다. 다만 지수 자릿수만으로 유한성을 보장하지는 못합니다. 에너지 칸에 310자리 숫자가 든 c2 단 한 행이 `RUN_FAILED`의 근거가 되어 c1 보조값이 채택됐습니다. 숫자 문법 검사에 실제 판독 가능 범위 검사를 더하세요. 업체 5.4.4의 실제 c2 출력 폭은 미확인입니다. [검사기 150–163행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/tools/wad/build_a5_vasp_package.py#L150) · [재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_probes.json) · [VASP의 OSZICAR 열 정의](https://vasp.at/wiki/OSZICAR)

Q-EQ-2 · 시간 출처와 180시간 상한 — NO-GO, P0 · 범위 안
다른 시도의 `infra_abort.json`을 진행 폴더에 복사한 EP 사례는 종료 8, c2 미실행으로 닫혔습니다. 하지만 `killed.json`에도 같은 결속이 필요합니다. 모의 시계로 c1의 실제 종료 기록에 648,001초를 남겼습니다. 그대로 재개하면 종료 5이고 c2가 뜨지 않습니다. 여기에 다른 `run_id`로 정식 발급된 0초 `killed.json` 한 장을 복사하니 종료 0, 반송 검사 `OK`, 수집기 `a5_c2`가 됐습니다.
최소 수정은 양쪽 모두 진행 폴더에 `attempt.json`과 `killed.json`이 공존하면 시간 합산 전에 거부하는 것입니다. 또 `killed.json`만 있는 경우에도 해당 시작 기록과 결속한 뒤 시간을 쓰세요. 러너 자체의 `--killed` 명령은 이미 완료 폴더에 그 파일을 만드는 것을 금지합니다. [러너 342행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L342) · [검사기 2259행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/tools/wad/build_a5_vasp_package.py#L2259) · [대조군과 복사군 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_probes.json)
Q-EQ-3 · 부분 복구와 시도 이력 — NO-GO, P1 · 범위 안
이력 대조를 한 방향으로 둔 결정은 타당합니다. A5가 `attempt.json`을 쓴 직후, `status.tsv`에 첫 행을 쓰기 전에 실제로 모의 러너를 끊었습니다. 온전한 종료 기록으로 정상 재개됐습니다. 반대로 EP처럼 첫 c1 이력 행만 남긴 복구는 종료 8이었고 시작점도 다시 쓰지 않았습니다.
남은 구멍은 `run/` 밖에 남은 완료 증거입니다. 정상 완료 뒤 `run/` 하나만 A5 직후 체크포인트로 복구했습니다. 옆의 기존 `a5_return.tgz`와 SHA는 그대로였고 그 안에는 완료된 c1·c2가 있었습니다. 그런데 러너가 두 단계를 새 ID로 다시 실행하고 기존 tgz를 덮어썼습니다. 새 반송도 `OK`였습니다. 재개 전에 SHA가 맞는 기존 tgz의 `final.json`과 시도 목록을 확인하고, 현재 트리가 그보다 과거이면 원본을 보존한 채 멈추세요. 완료 기록이 없는 중간 포장은 계속 허용할 수 있습니다. [러너 721–730행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L721) · [단일 폴더 복구 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_snapshot.json)
별도로 `status.tsv`가 0바이트이면 러너는 헤더 검사를 건너뛰어 c1·c2를 실행하고, 반송 검사기만 `LADDER_VIOLATION`을 냅니다. 헤더만 있고 이력 행이 0개인 정상 파일은 허용하되, 헤더 자체가 없으면 실행 전에 거부하세요. [러너 382–391행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L382) · [재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_edges.json)
Q-EQ-4 · 시작·종료·최종 기록 — NO-GO, P1 · 범위 안
일반적인 종료 ID 불일치는 검사기가 `ATTEMPT_MISMATCH`로 거부했고, 채택 가능한 반송에서 `final.json`을 빼면 `STOPPED_FOR_REVIEW`였습니다. `attempts`를 뺀 최종 기록도 재포장과 재실행 모두 종료 2였습니다. 다음 두 경로는 열려 있습니다.

1. 잘린 종료 기록으로 계산이 계속됩니다. A5 `attempt.json`에서 마지막 닫는 중괄호 하나만 유실시키자 러너는 c1·c2를 모두 실행하고 종료 0을 냈습니다. `t_start` 뒤에 `.5`가 붙은 경우도 같았습니다. 검사기는 두 반송을 거부했지만 외주 계산은 이미 끝났습니다. 종료 기록을 임시 파일에 완성한 뒤 원자적으로 교체하고, 재개 시 전체 문법과 정수 필드를 확인하세요. [러너 ](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L364)`end_id`[ 364행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L364) · [종료 기록 쓰기 885행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L885) · [재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_probes.json)
2. 재포장이 현장에서 보이는 오류를 반송본에서 지울 수 있습니다. 완료된 c1 폴더에 `infra_abort.json.part` 한 장이 있으면 직접 검사 결과는 `LADDER_VIOLATION`입니다. 같은 폴더를 `PACK_ONLY=1`로 포장하면 종료 0이고, `.part`가 빠진 반송은 `OK`·`a5_c1`이 됩니다. 완료 c1의 종료 ID만 달라져도 재포장 자체는 0입니다. 또 `final.json`이 `code=0, state=REVIEW`인 경우 양쪽 모두 `OK`를 허용했습니다. 완료 묶음을 포장하거나 재사용하기 전에 장부·잔여 파일·종료 ID와 허용된 `code/state` 조합을 함께 확인하세요. [러너 ](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L414)`fin_ok`[ 414행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L414) · [재포장 진입 698행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L698) · [직접 검사와 반송 검사 대조](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_probes.json)

Q-EQ-5 · 필수 칸·UTF-8·장부 순서 — 조건부, 필수 칸은 미해제

* P1 · 범위 안. `""`와 입력 시 비 UTF-8 바이트는 종료 2·파일 미생성으로 정확히 막혔습니다. 그러나 스케줄러 ID에 공백 세 칸을 주면 공식 명령이 영수증을 발급하고 다음 단계가 실행·채택됩니다. 정상 영수증의 사유 한 바이트가 저장 뒤 훼손된 경우도 재개·채택됐습니다. 필수 세 칸에 공백 외 문자가 있는지 쓰기와 읽기 양쪽에서 확인하고, 영수증을 소비할 때도 UTF-8을 검증하세요. 후자는 §1b가 포함한 인코딩 사고입니다. [러너 688–692행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L688) · [공백 입력](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_probes.json) · [읽기 중 손상](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_edges.json)
* P2 · 시간순 검사는 조건부 GO. 시각이 다른 역순 장부는 양쪽이 차단했습니다. 시각을 같은 초로 고정하자 `c1#1 → A5#2`도 통과했습니다. 이 재현은 장부와 폴더 번호를 함께 바꾸므로 §1b상 비차단 참고입니다. 다만 “단계 순서가 시간 검사에 함의된다”는 설명은 고쳐야 합니다. 같은 초에도 단계 역전을 잡겠다면 전역 번호순으로 `A5 ≤ c1 ≤ c2`를 별도 대조하면 됩니다. [러너 329–331행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/891e106e5/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L329) · [동일 초 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/eq_edges.json)

Q-EQ-7 · 위협모델 — GO
§1b를 수용합니다. 운영자가 한 번 수행한 복구를 기준으로 보면 됩니다. `run/` 하나를 되돌리면 그 아래 여러 기록이 자연스럽게 함께 과거로 돌아갑니다. 이번에는 그 복구와 모순되는 완료 tgz까지 남아 있었으므로 검출할 수 있습니다. 반면 모든 독립 기록까지 일관되게 교체한 상황은 선언한 범위 밖으로 두어도 됩니다.
Q-EQ-6 · 발송 — NO-GO
재승인의 핵심은 남의 `killed.json`으로 상한을 넘을 수 없고, 이전 완료 반송본을 복구 과정에서 덮어쓰지 않으며, 깨진 기록이 다음 실행이나 재포장 전에 멈추는 것입니다. 위 수정에는 물리 설정이나 사전등록 문턱 변경이 필요하지 않습니다.
배포본 재빌드와 MANIFEST 10개 항목의 해시 일치를 확인했습니다. 독립 실행한 자체시험은 a5 236/236, V5 313/313, round2 194/194였고, G5 재수집 JSON도 기존 파일과 바이트 단위로 같았습니다. 변이 시험은 제가 선택한 3/3을 재현했고, 전체 140/140은 제출자 보고치입니다. 신규 실행은 모두 모의 VASP였습니다. [변이 시험 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/selected_mutants.log) · [G5 대조](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EQ_20261123/g5.log)
