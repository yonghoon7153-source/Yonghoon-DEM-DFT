---
title: "EP 회신 — W_ad a5 묶음 (EO 고침) 확인: NO-GO — EO 원래 반례는 막힘 · 숫자를 못 읽는 c2 행 (칸 수만 맞음) 으로 c1 보조 채택 · 'SDA' (콜론 앞) 절단을 0 스텝으로 받음 · 180 h 넘은 시도에 남의 0 초 영수증 한 장으로 c2 실행 · 채택 · 부분 복구 뒤 status.tsv 의 선행 c1 · 완료 시도 run_id · 빈 영수증 칸 · 비 UTF-8 사유 · 장부 순서"
date: 2026-11-23
updated: 2026-11-23
tags: [review, wad, adhesion, vasp, a5, runner, checker, codex, reply, letter]
letter: EP
track: wad
channel: codex
kind: reply
status: 수령 2026-11-23 (사용자 붙여넣기 · 첨부 둘) · NO-GO · 기준 0fbc49760 · MANIFEST f10dedef… · 재승인 조건 ① 숫자를 못 읽는 행으로 단계를 소모하지 않음 ② 현재 시도에 결속된 영수증만 시간 합산 ③ 부분 복구 뒤 남은 c 단 실행 흔적 대조 ④ 시작 · 종료 · 최종 목록의 실행 ID 일치 → 고침 (빌드 기록 ⑨)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-23). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖).
> 첨부 둘 (사용자 업로드) 은 `kb/reviews/codex_EP_evidence_2026_11_23/` 에 그대로: `extra.json` (sha256 29f3bc1e…) · `selected_mutants.log` (sha256 296a2562…). 원문의 `finished_row.json` · `rec_parity.json` · `boundaries.json` 은 업로드되지 않았다.
> 편지: `codex_EP_prompt_wad_a5_eo_fixes_2026_11_23.md` (기준 8fd051a22 → 고침 df5ea438b · 0fbc49760 · MANIFEST f10dedef…).

---

NO-GO — 0fbc49760 묶음의 업체 발송을 보류하세요. EO에서 제시한 원래 반례들은 막혔습니다. 그러나 이번 배포본에서도 숫자를 읽을 수 없는 c2 출력으로 c1 보조값이 채택됐고, 180시간을 초과한 시도에 다른 시도의 영수증 한 장이 섞이자 c2가 실행되고 채택됐습니다. 두 경우 모두 모의 VASP에서 실제 러너 → 반송 검사기 → 수집기까지 재현했습니다.
Q-EP-1 · 완전한 전자 반복행 — NO-GO, P0
SDA:에서 끊긴 첫 행은 이제 종료 8·미채택입니다. 완전한 한 행 뒤의 SDA: 꼬리는 정확히 1행으로 셌고, 정상 7행 중단에서는 c1 보조값을 채택했습니다. 끝 줄바꿈을 요구하는 보수적 규칙은 유지해도 됩니다.

남은 결함은 줄바꿈이 있고 칸 수가 맞으면 숫자가 없어도 통과한다는 것입니다. c2의 유일한 행을 SDA: 1 none missing missing abc bad로 두자 --killed가 0, 재개가 1로 끝났고 c1 보조값이 채택됐습니다. 종료 기록이 남은 실행 실패에서도 똑같은 행이 RUN_FAILED · 1행으로 채택됐습니다. 코드 주석은 후속 판정이 수치를 검사한다고 하지만, 이 두 경로는 그 검사에 도달하지 않습니다. 또한 첫 행이 콜론 직전인 SDA에서 끊기면 --infra-abort가 이를 0스텝으로 받아 재실행까지 허용했습니다. [러너 375행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L375) · [검사기 149행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/tools/wad/build_a5_vasp_package.py#L149) · [실행 실패 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EP_20261123/finished_row.json)

최소 수정은 --killed와 RUN_FAILED가 단계를 소모하기 전에 양의 스텝 번호, 정수 ncg, 필수 실수 칸의 판독 가능성을 같은 함수로 확인하는 것입니다. 유일한 행이 손상됐거나 기대 머리의 일부만 남았으면 검토로 보내세요. 정상 6필드 행과 7필드 행은 모두 허용할 수 있습니다. [VASP의 OSZICAR 열 정의](https://vasp.at/wiki/OSZICAR)
Q-EP-2 · REC1과 시작 기록 — 조건부 GO
EO에서 요구한 문법 일치와 잡 결속은 닫혔습니다. 독립 바이트 입력 376건에서 awk와 Python의 수락 여부와 판독값이 전부 같았습니다. ESC가 든 사유는 왕복됐고, 쉼표 유실 시 c2가 뜨지 않았으며, 공백만 다른 정상 JSON은 통과했습니다. 다른 잡의 attempt.start는 종료 2·미채택이었습니다. 시작 기록의 신원을 모르면 종료 2로 원본을 보존하고, 확인된 장부 충돌은 종료 8로 마감하는 구분에도 동의합니다. [판독 대조 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EP_20261123/rec_parity.json) · [시작 기록 검사 269행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L269)

두 가지는 남습니다. sched_job_id를 빈 문자열로 바꾼 영수증도 양쪽이 유효하다고 보고 c1 보조값을 채택했습니다. 기록 명령이 필수로 요구하는 잡 ID·취소 시각·사유는 읽을 때도 비어 있으면 거부해야 합니다. 또 운영자 사유에 비 UTF-8 바이트 0xE9를 주면 러너가 실제로 그 바이트를 써서, REC1은 통과하고 표준 UTF-8 JSON 판독은 실패했습니다. “러너는 그런 바이트를 쓰지 않는다”는 한계 설명은 정정해야 합니다. [영수증 필드 검사 837행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L837) · [문자열 기록 263행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L263)
Q-EP-3 · 중단 시간과 180시간 상한 — NO-GO, P1
정상 이력의 경계는 정확했습니다. 648,000초에서 A5 재실행 허용, 648,001초에서 종료 5·재실행 없음을 확인했습니다. UNKNOWN을 남긴 채 후속 단이 있는 반송과, 다음 시작보다 늦게 시간을 채운 반송도 LADDER_VIOLATION이었습니다.

문제는 시간을 고를 때 그 영수증이 이 시도의 것인지 확인하지 않는 경로입니다. 648,001초가 기록된 중단 c1은 그 자체로 c2를 막았습니다. 여기에 다른 A5 시도에서 공식 명령으로 발급한 0초짜리 infra_abort.json 한 장을 run/<잡>_c1/에 복사하자, 같은 러너가 c2를 띄우고 종료 0, 검사기 OK, 수집기 a5_c2가 됐습니다. 다른 파일이나 해시는 고치지 않았습니다. 최소 수정은 run_aborted/에서만 장부·폴더·`run_id`와 일치하는 중단 영수증을 시간 출처로 인정하고, 진행 폴더에 중단 영수증이 섞이면 실행 전과 반송 시 모두 거부하는 것입니다. [러너 wall_of 327행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L327) · [검사기 wall_of 2117행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/tools/wad/build_a5_vasp_package.py#L2117)
Q-EP-4 · 장부와 보존 폴더 / 최종 실행 신원 — 부분 해제
항목	판정과 재현	최소 수정
장부 ↔ 보존 폴더	원래 반례 GO, 부분 복구 P1 미해제. 장부만 남으면 종료 8로 정확히 막았습니다. 그러나 부분 복구에서 장부·보존 폴더·시작점이 함께 빠지고 status.tsv에 첫 c1의 SCF_UNVERIFIED 행이 남자, 러너가 시작점을 다시 쓰고 c1을 재실행했습니다. 반송 OK, 새 c1 채택입니다.	시작점 생성과 재실행 전에 status.tsv에 남은 선행 시도가 현재·보존 폴더로 설명되는지 확인하세요. 반송에도 같은 대조가 필요합니다. [러너 814행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L814) · [장부 검사 937행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L937)
같은 초에 끝난 두 묶음 교환	GO. 서로 다른 실행의 tgz와 SHA 파일을 함께 옮겨도 이제 종료 4로 막았습니다.	EO의 이 반례는 해제합니다. [교환 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EP_20261123/boundaries.json)
완료 시도의 신원	조건부, P1. 정상 c1의 attempt.json.run_id 한 필드만 다른 유효 ID로 바꿔도 OK · a5_c1이었습니다. 최종 목록은 시작 기록의 ID를, 시도별 결과는 종료 기록의 ID를 사용합니다.	완료 시도의 run_id와 t_start를 시작 기록에 직접 대조하세요. 최종 발송본에서는 attempts가 빠진 final.json도 재포장 전에 거부해야 합니다. 현재는 재포장과 일반 재실행이 모두 0이고 반송 검사에서야 거부됩니다. [완료 기록 검사 1848행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/tools/wad/build_a5_vasp_package.py#L1848) · [종결 재실행 652행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/db/inputs/wad_a5_vasp_2026_11_20/run_a5.sh#L652)


Q-EP-5 · 추가로 확인된 한계
P2 — 장부와 폴더의 집합이 같아도 사건 순서는 다를 수 있습니다. 실제 중단 순서가 A5 → c1인 모의 이력에서 장부 행과 폴더 번호만 c1#1 → A5#2로 맞바꾸자 재개와 반송이 모두 통과했습니다. 검사기가 사다리 순서로 다시 정렬하기 때문에 장부가 기록한 역순을 놓칩니다. 전역 중단 번호가 발생 순서를 뜻한다면, 재정렬 전에 그 번호 순서와 시작·기록 시각을 대조하세요. [장부 행 검사 2170행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/tools/wad/build_a5_vasp_package.py#L2170) · [시간순 검사 2333행](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/0fbc49760/tools/wad/build_a5_vasp_package.py#L2333)
Q-EP-6 · 발송 판정 — NO-GO
재승인에는 네 가지가 필요합니다. ① 숫자를 판독할 수 없는 행으로 단계를 소모하지 않을 것, ② 현재 시도에 결속된 영수증만 시간 합산에 쓸 것, ③ 부분 복구 뒤 남은 c단 실행 흔적을 대조할 것, ④ 시작·종료·최종 목록의 실행 ID가 일치할 것. 물리 설정이나 사전등록한 수치 문턱을 바꿀 필요는 없습니다.

재빌드 결과는 배포 트리와 바이트 단위로 일치했고 MANIFEST는 f10dedefe8165f64999a0dca9897ef39e951a6c3085a1baa6ee9b0106a1b169c였습니다. 자체시험 211/211 · 313/313 · 194/194, 독립 재실행한 변이 시험 7/7이 통과했고 G5 집계도 기존 JSON과 일치했습니다. 실제 업체 VASP 5.4.4의 c2 출력 형식은 이번 모의 검증 범위 밖입니다. [독립 재현 상세](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EP_20261123/extra.json) · [변이 시험 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EP_20261123/selected_mutants.log)
