# 현재 전체 게이트 완료 기록

이번 통합 후보에서 전체 `bash scripts/check_all.sh`가 **155 PASS / 0 FAIL, rc 0**으로 완료됐다. 실제 완료 UTC는 `2026-10-23T21:33:35.442636+00:00`다. [영수증](full_gate_receipt.json)과 [원 로그](full_gate/check-all.log)를 따른다.

후보의 원 README·보고서·manifest 문맥 및 이번 트랙의 후보 변경 파일은 [원본 ZIP](history/pre-full-gate-inputs.zip)에 바이트 그대로 보존했다. 독립 보고서, 작성자 원 출력, nested manifest는 수정하지 않았다. 원 기록의 대기 상태는 아래 당시 시점의 상태이며 현재 전체 게이트 미완료를 뜻하지 않는다.

- author/provenance.json#/full_gate: PENDING root integration is the author snapshot
- root_integration/receipt.json#/full_gate: PENDING separate frozen candidate gate is the pre-candidate import snapshot
- root_integration/README.md: direct tests and browser scope before the full gate

현재 outer MANIFEST는 최종 반입 증거의 해시 목록이다. ZIP 안의 원 manifest는 그 후보 스냅샷의 원래 경로 기준을 유지한다. 이 기록은 과학 입력값, 실제 WSL/물리 실행 또는 외부 판정의 완료를 새로 주장하지 않는다.

## 이전 병렬 시도와 현재 순차 재검증

같은 후보의 이전 `d3-verified` 시도는 2026-10-23T20:02:53.269689+00:00에 **154 PASS / 1 FAIL, rc 1**로 끝났다. 마지막 fast-driver 안에서 `scripts/run_network_194_parallel.py --selftest`가 기존 300초 제한에 걸렸고, 그 묶음은 192개 중 191개가 통과했다. [원 실패 로그](history/parallel-timeout-attempt/raw/check-all.log)와 [보존·진단 기록](history/parallel-timeout-attempt/diagnosis.md)을 함께 보존한다.

현재 `d3-serial`은 같은 후보에서 2026-10-23T21:33:35.442636+00:00에 **155 PASS / 0 FAIL, rc 0**으로 완료됐다. 검사 내용, fast-driver의 기본 workers=6, 해당 검사의 300초 제한은 그대로다. 동시 실행을 없앤 재검증이며, 자원 경쟁은 이전 시간 초과의 가능한 설명이지 유일 원인으로 입증한 것은 아니다. [조정기 원본](history/serial-retry-control/controller.json)과 [실행 전 조건](history/serial-retry-control/ready-proof.json)을 따른다.
