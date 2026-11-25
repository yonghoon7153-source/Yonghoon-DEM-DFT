---
title: "EI 회신 — b2o3 9 단계 DFT 도구 v4: NO-GO (P1 1 · P2 1 · P3 1) · EH 네 지적 닫힘 · 유한한 분수 좌표 토큰이 셀 변환에서 inf 가 되어 전자구조 대상으로 · 판정 경로가 만들 입력 경로와 겹치면 덮어씀 · '판정은 맨 끝' 변이가 두 동작 · 응력 허용 타당 (상한 0.0057356) · CRLF 거부 = LF 범위 명시 · 쓰기 실패 범위 좁히기 · DY 확인 4 (EOS 결과 파일 결속) 해제 가능"
date: 2026-11-13
updated: 2026-11-13
tags: [review, b2o3, dft, qe, eos, kprobe, readout, codex, reply, letter]
letter: EI
track: b2o3
channel: codex
kind: reply
status: 수령 2026-11-13 (사용자 붙여넣기) · NO-GO · 기준 67cca09c (도구 sha256 c8255d94 · 실행기 e2d6f728 · 변이 도구 bbdbaf66) · 고침 → 다음 편지 EJ
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-13). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖).

NO-GO — EH의 네 지적은 닫혔습니다. 새로 재현한 P1 1건·P2 1건을 고친 뒤 DFT 진입을 승인할 수 있습니다.
기준은 `67cca09c`, 도구 지문은 요청문과 일치합니다. selftest 178/178 · 실행기 24/24 · 변이 109/109를 재현했습니다. 실측 출력 3파일의 응력 119블록도 확인했습니다.
생산 UMA·DFT·MD는 실행하지 않았습니다. 아래 추가 시험은 합성 출력과 분리된 검증 폴더에서 수행했습니다. 정상 연결 시험의 8단계 계보에는 배포 selftest의 모의 자료를 사용했으므로, gabia의 실제 8단계 자료까지 제가 재검증했다는 뜻은 아닙니다.

1. P1 — 토큰은 유한하지만, 좌표 변환에서 생긴 `inf`가 전자구조 대상으로 넘어갑니다.
위치: [b2o3_bo_dft.py (line 1420)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/source/tools/doping/b2o3_bo_dft.py:1420), [대상 승격:1449 (line 1449)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/source/tools/doping/b2o3_bo_dft.py:1449).
재현: 통과하는 이완 출력에서 최종 Li 분수좌표 성분 하나를 `1e308`로 바꿨습니다. 토큰 자체는 유한하므로 판독을 통과하지만, 셀을 곱해 Cartesian 좌표로 바꾸면서 `inf`가 됩니다. 그런데 `read_relax`가 성공하고:
   * `inf`가 들어간 XYZ가 저장됩니다.
   * 해당 XYZ의 해시가 판정에 정상적으로 결속됩니다.
   * 구조 분류는 `invalid`인데 `electronic_targets`에는 포함됩니다.
`allow_nan=False`는 JSON 안의 숫자만 검사합니다. XYZ 본문에 들어간 `inf`까지 검사하지는 않습니다.
최소 수정: 좌표 변환 직후, XYZ 직렬화 전에 실제 `positions`의 유한성을 검사하고 실패하면 파일을 하나도 쓰지 않도록 하세요. 이 반례를 음성시험에 추가하면 됩니다. 유효한 구조의 `mixed`·`unclassified`를 금지하자는 요구는 아닙니다.
이는 손상 출력에 대한 경계시험이며, 실제 QE 계산에서 관측한 현상은 아닙니다. [재현 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/boundary_results.json)
2. P2 — 판정 저장 경로가 앞으로 생성할 입력 경로와 같으면, 만든 입력을 판정 JSON으로 덮습니다.
위치: [b2o3_bo_dft.py (line 1265)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/source/tools/doping/b2o3_bo_dft.py:1265).
재현: 정상 `read_sp`에서 판정의 `out`을 아직 없는 `kprobe/kp_FB_cfg0003/scf.in`으로 지정했습니다. 처음에는 파일이 없으므로 검사를 통과합니다. 이후 탐침 입력을 만들고, 마지막 판정 쓰기가 그 입력을 JSON으로 덮습니다. 함수는 성공 반환하고, 기록된 입력 해시와 디스크 파일의 해시가 달라집니다.
정상 권장 명령이 아니라 `--out` 경로를 잘못 지정한 경우의 결함입니다.
최소 수정: 쓰기 전에 판정·잡 입력·이완 구조의 정규화된 목적 경로를 함께 비교하고, 서로 다른 역할의 경로가 겹치면 거부하세요. 기존 파일의 존재 여부와 별개로 검사해야 합니다. [재현 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/boundary_results.json)
3. P3 — “변이마다 첫 실패가 그 변이의 자기 시험”이라는 설명은 한 곳에서 과합니다.
위치: [b2o3_bo_dft_mutations.py (line 134)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/source/tools/doping/b2o3_bo_dft_mutations.py:134).
`판정은 맨 끝` 변이는 판정을 앞으로 옮기는 동시에, 기존 판정 파일을 거부하는 조건도 끕니다. 실제 첫 실패는 쓰기 순서가 아니라 기존 계획 덮어쓰기 금지 시험입니다.
다만 쓰기 순서 시험이 없는 것은 아닙니다. 제가 기존 파일 거부는 유지하고 순서만 바꾼 별도 변이를 실행하자, 다음 입력 충돌·이완 구조 충돌 시험이 정확히 실패했습니다.
최소 수정: 해당 변이를 한 동작만 바꾸도록 정리하고 설명을 맞추세요. 이것만으로 실행 NO-GO를 유지할 사안은 아닙니다. [독립 변이 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/order_only_mutation.json)

Q1–Q6 답변

* Q1 — EH 네 항목은 닫혔습니다.
힘·좌표 NaN/Inf, 압력 꼬리 글자·NUL, 읽을 수 없는 BFGS, 응력 본문 삭제·머리와 본문 불일치를 모두 거부했습니다. 해당 거부 시험에서 새 파일 없음·기존 파일 바이트 변경 없음을 확인했습니다. `2.50E+01`과 `2.50D+01`은 모두 25 kbar로 읽혀 EOS 보류와 후속 대상 `null`이 유지됐습니다. [상세 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/independent_results.json)
* Q2 — 소비하는 토큰의 엄격 판독은 개선됐지만, 계산 후 유한성까지 닫히지는 않았습니다.
이번 검토에서 추가로 확인한 누락은 P1의 분수좌표 → Cartesian 변환 결과입니다. “입력 토큰이 유한하다”와 “후속 산출물이 유한하다”를 별도로 검사해야 합니다.
* Q3 — 응력 허용치 0.01·0.006 kbar는 타당합니다.
QE 출력 형식에서 P와 kbar 성분은 소수 둘째 자리, Ry/bohr³ 성분은 소수 여덟째 자리입니다. 따라서 최악의 반올림 차이는 각각:
   * P와 대각 평균: `0.005 + 0.005 = 0.010 kbar`
   * 두 단위 비교: `0.005 + 0.5×10⁻⁸×147105.07848 = 0.005735525… kbar`
코드의 `0.006`은 두 번째 상한을 포함합니다. 요청문 §2의 “상한 0.0057”은 0.0057356 또는 약 0.00574로 정정하는 편이 정확합니다. [QE 출력 형식](https://github.com/QEF/q-e/blob/qe-7.4.1/PW/src/stress.f90), [QE 단위 상수](https://github.com/QEF/q-e/blob/qe-7.4.1/Modules/constants.f90)
실측 119블록과 해당 자릿수로 출력한 모의 응력 50,000건은 전부 통과했습니다. 사용자가 보고한 244파일·1016블록 전수검사를 제가 반복한 것은 아닙니다. 또한 CRLF로 변환한 출력은 현재 거부됩니다. 승인 범위는 원래의 Linux LF 출력으로 명시하세요. [검증 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EI_v4_20261113/raw_rounding_results.json)
* Q4 — 기존 ‘검사 뒤 쓰기’ 문제는 고쳤지만, 경로 충돌은 추가로 막아야 합니다.
마지막 입력이나 이완 구조가 충돌하는 경우, 앞쪽 파일부터 써버리던 문제는 해결됐습니다. 남은 것은 P2입니다.
그리고 “쓰기 도중 실패해도 판정 파일은 없다”는 설명은 범위를 좁혀야 합니다. 보조 파일을 쓰다 실패하면 판정은 없지만, 판정 파일 자체를 쓰다 실패하면 부분 파일이 남습니다. 마지막 쓰기에서 일부 바이트를 쓴 뒤 예외를 발생시키자 깨진 JSON이 남았습니다. 유효한 성공 판정이 남는 경우를 재현한 것은 아닙니다. Q4의 설명을 “판정 쓰기 시작 전 실패”로 한정하고, 부분 판정은 거부·보존 후 새 이름으로 재시도한다고 적으면 됩니다.
* Q5 — DY 확인 4의 좁은 조건인 EOS `(E, P, V)` 결과 파일 결속은 해제할 수 있습니다.
이번 반례에서는 값 판독과 압력 검증이 제대로 연결됐고, EOS 보류가 후속 대상 차단으로 이어졌습니다. 다만 EOS 입력 결속의 해제와 후속 구조 파일의 유효성 승인은 별개입니다. 후자는 P1이 남았습니다.
* Q6 — 아직 사용자 비준만 남은 상태는 아닙니다.
P1의 변환 후 유한성 검사와 P2의 목적 경로 충돌 검사가 먼저입니다. 추가 생산 계산이나 새로운 과학적 문턱은 필요하지 않습니다.

DFT 진입 전 마지막 확인 목록

1. P1·P2 수정 후 두 반례가 정확한 이유로 거부되고 새 파일·기존 파일 변경이 없는지 확인.
2. 정상 연결 경로와 EH 네 반례를 유지하고, 수정한 배포판 selftest를 확인.
3. 변이 설명·쓰기 실패 범위를 정정하고 수정판 코드·카드·계획 지문을 맞춤.
4. 사용자가 개정 5를 새로 비준한 뒤 선언된 실행 전 GPU 확인을 수행.

기존 EH 판정을 다시 여는 것은 아닙니다. 이번 재승인의 남은 코드 조건은 위 두 경로입니다.