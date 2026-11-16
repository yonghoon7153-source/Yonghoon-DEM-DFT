---
title: "EK 회신 — b2o3 9 단계 DFT 도구 v6: 조건부 GO (gabia/Linux 생성 · 판독 범위) · EJ P2 해제 · 실행은 사용자 비준 뒤 · Windows 짧은 경로명 (8.3) 과 긴 이름이 섞이면 같은 파일을 다르게 판단하는 별도 P2 (Linux 생산 경로 차단 사유 아님) · 남은 것 = 사용자 비준 · 실행 직전 GPU 확인"
date: 2026-11-14
updated: 2026-11-14
tags: [review, b2o3, dft, qe, eos, kprobe, readout, codex, reply, letter]
letter: EK
track: b2o3
channel: codex
kind: reply
status: 수령 2026-11-14 (사용자 붙여넣기) · 조건부 GO (gabia/Linux 범위) · 기준 46e21278 (도구 sha256 0c3b7f51 · 실행기 e2d6f728 · 변이 도구 3090ec9f) · 남은 것 = 사용자 개정 5 비준 · Windows 짧은 경로명 P2 는 범위 밖으로 기록
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-14). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖). 같은 붙여넣기 뒤에 붙어 온 kgy 감시 출력 (li2s-3 2 단계) 은 이 회신이 아니라 따로 기록한다.

조건부 GO — 선언한 gabia/Linux에서 생성·판독하는 범위라면 EJ P2를 해제할 수 있어요. 실행은 사용자 비준 뒤입니다. Windows 짧은 경로명에는 별도 P2가 남아요.
기준은 `46e21278`, 세 파일의 지문이 요청문과 일치해요. 함수 비교에서도 변경은 `_commit`과 selftest에 한정됐어요.
긴 절대경로의 검토 폴더에서는 selftest 185/185, 링크 시험 세 건 모두 건너뛰지 않고 통과했어요. 새 중복 검사만 끄면 정확히 그 세 시험이 실패해 182/185가 됐고, 인접한 쓰기 검사 변이 세 건도 탐지했어요. 전체 114개 변이는 이번에 재실행하지 않았어요.
생산 계산은 하지 않았고, 독립 연결 시험의 8단계 계보에는 모의 자료를 사용했어요.
P2 — Windows의 짧은 이름과 긴 이름이 섞이면 같은 파일을 다르게 판단해요.
위치: [b2o3_bo_dft.py (line 1287)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EK_v6_20261114/source/tools/doping/b2o3_bo_dft.py:1287), [실제 경로 비교:1299 (line 1299)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EK_v6_20261114/source/tools/doping/b2o3_bo_dft.py:1299).
재현 환경: Windows·Python 3.12.14의 기본 임시 폴더가 `C:\Users\ADMINI~1\AppData\Local\Temp`인 경우예요.
아직 없는 파일을 가리키는 파일 링크에서:

* 판정 경로의 `resolve()`는 `C:\Users\Administrator\…\scf.in`
* 입력 링크의 `resolve()`는 `C:\Users\ADMINI~1\…\scf.in`

을 반환했어요. 실제로는 같은 파일인데 비교를 통과해서 입력을 판정 JSON으로 덮었어요. 기본 임시 폴더에서 selftest가 183/185였던 원인입니다. 뒤의 입력끼리 충돌 시험은 이 실패가 남긴 파일 때문에 함께 실패했어요. [경로·쓰기 결과 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EK_v6_20261114/native_paths.json)
최소 조치: 이번 운영은 요청서대로 gabia/Linux에서 생성·판독하세요. Windows를 지원 범위에 넣기 전에는 링크를 푼 뒤 존재하는 부모 경로까지 긴 이름으로 정규화하고 이 반례를 추가해야 해요. `TMPDIR`만 긴 경로로 바꾸면 시험은 통과하지만, 임의의 짧은 경로 링크까지 해결됐다는 뜻은 아니에요.
이 Windows 결함을 이번 Linux 생산 경로의 차단 사유로 확대하지는 않아요. 검토 범위에서 추가 P0·P1·P3는 확인하지 못했어요.
Q1–Q3

* Q1 — EJ의 링크 반례 둘은 일반 경로에서 닫혔어요.
디렉터리 링크·파일 링크 모두 ‘겹친다’는 정확한 이유로, 쓰기 전에 거부됐어요. 새 파일과 기존 파일 변경도 없었어요. 추가된 입력끼리 충돌도 동일하게 거부됐고, 정상 경로는 입력 해시까지 일치하며 통과했어요. [독립 재현 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EK_v6_20261114/boundary_results.json)
* Q2 — 선언한 운영 범위에서는 P2를 해제할 수 있어요.
판정 경로를 `seen`에 먼저 넣고 입력·이완 구조를 모두 비교한 뒤 `_pending`과 쓰기로 넘어가는 순서가 맞아요. 기존 폴더 제한과 기존 판정 파일 거부도 유지됐어요. Windows 짧은 이름까지 포함한 범용 경로 동일성 보증으로는 확대하면 안 돼요.
* Q3 — gabia/Linux 운영을 유지한다면 사용자 비준만 남아요.
EI의 좌표 유한성 검사, EH의 숫자·응력 판독, EOS 보류 시 후속 대상 차단은 유지됐어요. 새로운 과학적 문턱이나 추가 계산을 요구하지 않아요. 검토 커밋의 개정 5 결정은 아직 **`proposed`**예요.

DFT 진입 전 마지막 확인 목록

1. 생성·판독을 gabia/Linux의 v6로 수행하고, 코드 지문과 계획 지문을 확인.
2. 사용자가 개정 5를 비준하고 결정 기록을 갱신.
3. 실행 직전 기존 GPU 독점·여유 메모리 확인을 통과한 뒤 시작. 이전에 기록한 여유 메모리 값을 현재 상태로 대신 쓰지 않기.
