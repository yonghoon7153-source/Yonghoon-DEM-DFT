---
title: "ER 회신 — W_ad a5 묶음 (EQ 고침 · 트리 관문 하나) 확인: NO-GO — EQ 반례 (남의 killed.json · 완료 반송본 옆 과거 복구 · 잘린 종료 기록 · 재포장 .part) 는 막힘 · 필수 칸 · UTF-8 · 장부 순서 GO · 범위 안 지적: 준비 폴더 이름으로 옮긴 중단 c1 을 러너가 지움 · 마지막 단 종결 (final.json OK · A5 WAVECAR 삭제) 이 검사보다 먼저 · 첫 행 콜론 한 바이트 손상 ('SDA;' · 'SDA') 이 0 스텝 · attempt.json 648,001 → 48,001 한 자리 유실 (이력 행과 대조 안 함) · 기록 명령 둘 겹침 (잠금 없음) · 중간 반송본 전자행 7 개 후퇴 · 확정 영수증 UNKNOWN 후퇴 · 종료 기록 job/stage/attempt · POTCAR.sha256 대조 없음"
date: 2026-11-23
updated: 2026-11-23
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, reply, letter]
letter: ER
track: wad
channel: codex
kind: reply
status: 수령 2026-11-23 (사용자 붙여넣기 · 첨부 둘) · NO-GO · 기준 cc3873047 · MANIFEST 8e295bae… · Q-ER-6 GO · 재승인 핵심 = 0 스텝 오분류 · 시간 기록 충돌 · 중간본 복구 때 증거 유실 · 준비 폴더 삭제 · 종결 · 실행 전 검사의 순서와 대조 항목 → 고침 (빌드 기록 ⑭)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-23). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖).
> 첨부 둘 (사용자 업로드) 은 `kb/reviews/codex_ER_evidence_2026_11_23/` 에 그대로: `selected_mutants.log` (sha256 97328f56… · m141 · m169 · m176 3/3 빨강) · `g5.log` (sha256 34f1f443… — EQ 때 g5.log 와 같은 바이트). 원문의 `er_independent.json` · `er_other.json` · `er_observed_rows.json` · `eq_snapshot.json` · `eq_edges.json` · `eq_probes.json` 은 업로드되지 않았다.
> 편지: `codex_ER_prompt_wad_a5_eq_fixes_2026_11_23.md` (기준 891e106e5 → 고침 c14d52abb · cc3873047 · MANIFEST 8e295bae… · 트리 관문 하나 · 위협 범위 §1b 그대로).

---

NO-GO — `cc3873047` 묶음의 업체 발송을 보류하세요. EQ에서 지적한 잘못 복사된 `killed.json`, 완료 반송본의 과거 복구, 잘린 종료 기록, 재포장 때 사라지던 `.part`는 원래 반례로 다시 확인했고 모두 막혔습니다. 그러나 같은 c1의 두 기록이 648,001초와 48,001초로 충돌해도 c2가 실행·채택됐고, 중간 반송본에 남은 전자행 7개를 0스텝으로 되돌려 재실행할 수 있었습니다. 둘 다 §1b의 단일 손상·복구 범위에 듭니다.
Q-ER-1 · 모든 진입점의 공통 검사 — NO-GO, P1 · 범위 안
두 곳에서 러너가 현장 증거를 먼저 잃습니다.

* 준비 폴더로 잘못 복구한 실행 기록을 삭제합니다. 전자행 7개가 남은 중단 c1 폴더를 같은 단계의 `.prep_…_c1` 이름으로 한 번 옮겼습니다. 재개하자 러너는 그 폴더를 삭제하고 새 ID로 c1을 실행했습니다. 반송은 `OK`, 수집기는 `a5_c2`를 채택했습니다. `.prep_*` 자동 정리 전에 `OSZICAR` 전자행이나 `OUTCAR` 반복 기록이 있으면 폴더를 보존하고 멈춰야 합니다. [이름 검사 517행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc3873047/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L517) · [삭제 943행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc3873047/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L943) · [재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_independent.json)
* 마지막 단계에서는 검사가 종결 처리보다 늦습니다. 모의 c1이 `core.1`을 남기자 포장은 종료 8로 막혔습니다. 그때 이미 `final.json`에는 `OK`가 적혔고 A5의 `WAVECAR`는 삭제됐습니다. 마지막 단계 반환 직후, `drop5`와 `fin5` 전에 같은 검사를 실행하세요. 비표준 MPI 로그나 코어 파일에서 멈추는 정책은 수용할 수 있습니다. 실제 업체 래퍼가 생성하는 파일명 전체는 이번 시험에서 확인하지 못했습니다. [종결 순서 1242행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc3873047/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L1242) · [현장 상태 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_independent.json) · [VASP 공식 출력 파일 목록](https://vasp.at/wiki/Output_files)

Q-ER-2 · 전자행과 24자 제한 — 기존 두 반례 GO, 0스텝 판정 NO-GO · P0 · 범위 안
줄바꿈 없이 끝난 `SDA`와 310자리 숫자는 이제 정확히 차단합니다. 보존된 VASP 5.4.4 출력 20개의 DAV/RMM 2,733행도 전부 통과했습니다. 6필드 100행, 7필드 2,633행입니다. 가장 긴 토큰은 19자였으므로 요청서의 “실물은 16자 이하”는 정정하세요. 24자 제한에는 여유가 있습니다. 업체의 실제 c2 출력 형식은 여전히 미확인입니다. [실물 계수](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_observed_rows.json)
남은 반례는 첫 행의 콜론 한 바이트입니다. `SDA; 1 0 0 0 12 0\n`처럼 `:`가 `;`로 손상되면 `--infra-abort`가 0을 반환해 0스텝으로 접수했습니다. c2가 새로 실행되고 채택됐습니다. `SDA\n`도 같은 결과였습니다. 0스텝 재시도에서는 빈 파일·공백·인식한 열 제목 등 0행으로 설명되는 내용만 허용하고, 그 밖의 첫 데이터 줄은 검토로 보내세요. [행 판독 622–634행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc3873047/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L622) · [기록→재실행→채택 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_other.json)
Q-ER-3 · `killed.json`과 180시간 상한 — 복사 반례 GO, 상한 전체 NO-GO · P0 · 범위 안
완료 c1에 남의 0초 `killed.json`을 넣은 EQ 반례는 종료 8, c2 미실행으로 닫혔습니다. 다음 두 경우에는 상한이 여전히 풀립니다.

1. 종료 기록에서 숫자 한 자리 유실. 러너가 c1의 `attempt.json`과 `status.tsv` 양쪽에 648,001초를 기록한 직후 중단했습니다. 그대로 재개한 대조군은 종료 5였습니다. `attempt.json`에서 첫 숫자 하나만 빠져 48,001초가 되자, 이력 행에 648,001초가 그대로 있는데도 c2 실행 → 반송 `OK` → `a5_c2` 채택이었습니다. 이력 행이 있으면 같은 `run_id`의 `wall_s`와 `elapsed_s`를 합산 전에 대조하세요. 행을 쓰기 직전에 중단된 정상 복구는 계속 허용할 수 있습니다. [이력 대조 378–386행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc3873047/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L378) · [대조군과 한 자리 유실 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_independent.json)
2. 공식 기록 명령 두 개가 겹치면 먼저 수락한 영수증이 덮입니다. 같은 중단 c1에서 `--killed` 두 개가 모두 파일 부재를 확인한 뒤 차례로 쓰게 했습니다. 648,001초와 0초 명령이 모두 종료 0이었고, 최종 기록은 0초, c2는 실행·채택됐습니다. 기록 명령도 검사부터 쓰기 완료까지 같은 배타 잠금을 소유하게 하세요. 충돌하는 두 번째 기록은 기존 영수증을 보존하고 거부해야 합니다. [잠금 확인 743–746행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc3873047/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L743) · [동시 기록 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_other.json)

Q-ER-4 · 기존 반송본과 복구 이력 — 완료본 GO, 중간본 NO-GO · P0 · 범위 안
완료 tgz 옆에서 `run/`만 과거로 복구하면 종료 8, 새 c1·c2 없음, tgz 보존이었습니다. 0바이트 `status.tsv`도 실행 전에 차단했고, 헤더만 있는 정상 중단은 재개됐습니다. [완료본 복구](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/eq_snapshot.json) · [이력 검사](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/eq_edges.json)
반면 중간 tgz에 c1 전자행 7개를 담은 뒤, 같은 c1 폴더 하나를 출력 전 체크포인트로 복구하자 `attempt.start` 바이트와 ID가 같다는 이유로 통과했습니다. `--infra-abort`가 0스텝을 접수했고 새 c1이 실행됐으며 기존 tgz도 덮였습니다. 별도 시험에서는 이미 648,001초로 확정된 영수증이 `UNKNOWN`으로 되돌아갔는데도 `PACK_ONLY=1`이 기존 반송본을 덮었습니다. [중간본 비교 565–584행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc3873047/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L565) · [7행 복구](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_independent.json) · [확정 시간 복구](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_other.json)
최소 수정은 중간본에서 이미 관측한 사실의 후퇴를 거부하는 것입니다. 같은 시도에서 기존 완전 행이 사라지면 보존·중단하고, 영수증 시간은 `UNKNOWN → 확정값`만 허용하세요. 반송본 전체를 바이트로 고정할 필요는 없습니다.
Q-ER-5 · 종료 기록·원자 쓰기·재포장 — 기존 반례 GO, 실행 전 대조는 조건부 · P1 · 범위 안
닫는 `}`가 빠진 종료 기록과 `t_start`가 소수가 된 기록은 모두 종료 8, c1 미실행이었습니다. `.part`, 바뀐 종료 ID, `code=0/state=REVIEW`도 재포장과 일반 재실행에서 차단했습니다. 이때 기존 정상 tgz를 그대로 보존한 것이 맞습니다. [EQ 반례 재실행](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/eq_probes.json)
다만 A5의 `attempt.json.job` 한 글자를 바꾸거나 `POTCAR.sha256` 한 자리를 바꾸면 러너는 각각 종료 0까지 계산합니다. 반송 검사기에서야 `ATTEMPT_MISMATCH`와 `POTCAR_UNVERIFIED`로 탈락했습니다. 러너의 종료 기록 검사에서 `job/stage/attempt`를 시작 기록·폴더와 대조하고, 기록된 POTCAR 해시를 현장에 남는 `POTCAR.sha256`과 대조하세요. POTCAR 본문 반송은 필요하지 않습니다. [러너 463–474행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/cc3873047/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L463) · [두 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/er_independent.json)
Q-ER-6 · 필수 칸·UTF-8·장부 순서 — GO
선언한 여섯 ASCII 공백 기준에서 공백뿐인 스케줄러 ID와 비 UTF-8 입력은 종료 2·파일 미생성이었습니다. 저장 뒤 영수증 바이트가 손상된 경우는 재개 종료 8·c2 미실행이었습니다. 같은 초의 `c1#1 → A5#2` 역순도 양쪽이 막았습니다. 이 세 항목은 해제합니다. [쓰기 대조](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/eq_probes.json) · [읽기·동일 초 대조](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/eq_edges.json)
Q-ER-7 · 발송 — NO-GO
재심에는 위의 0스텝 오분류, 시간 기록 충돌, 중간본 복구 때의 증거 유실, 준비 폴더 삭제, 종결·실행 전 검사의 순서와 대조 항목을 모의 러너에서 다시 확인하면 됩니다. 물리 설정과 사전등록 문턱은 이번 판정에 영향을 주지 않았습니다.
재빌드 배포본은 대상 커밋과 바이트 단위로 일치했고 MANIFEST는 `8e295baea495de906bddb172f14e30a1fe2d58cd93775ddee783c95c0ce0db5d`였습니다. 독립 실행한 자체시험은 266/266 · 313/313 · 194/194, 선택한 변이는 3/3 검출, G5 재수집 JSON은 기존 파일과 동일했습니다. 전체 변이 191개는 이번에 독립 재실행하지 않았습니다. 신규 계산은 모두 모의 VASP였습니다. [변이 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/selected_mutants.log) · [G5 대조](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ER_20261123/g5.log)
