# MIP-01 수령 및 비활성 검증기 경로 보존 수정 후보 — 2026-11-09

## 1. 바탕과 수령

새 가지는 `codex/mixer-path-fix-1109`다. 확인한 B 최신 `69d714d094c4d210e5bf931d5c520e64ca0a751d`에서 시작했고, 앞선 비활성 준비 후보 `73e659273fd2ed6406a4c90011fc6079c7adf95f`를 `cherry-pick -x`한 선행 사본은 `2ac1a2482f0290566ac1d67d972f7c9544a9d291`이다. 추가 61파일의 blob이 모두 같다. 기존 가지·B에는 쓰지 않았으며 rebase·force·amend·동기 merge는 없다.

독립 판정은 자산·메타·정책 한정 수용과 **MIP-01/P2 한 건 OPEN**, 새 P1/P3 없음이다. 수령 ZIP SHA256은 `18d6945be87b88c044fd934d8254658f02ff8855109bb6bdf8f60aa39ea78b0c`다. 339파일의 CRC·경로·중복과 해시 목록 338/338·184/184·40/40을 확인했다. 원요청 185파일은 수령 ZIP의 `package/` 185파일과 각각 바이트 동일하다. 원요청 ZIP 자체가 내장됐다고 주장하지 않는다. 원 검토·원 ZIP은 수정하지 않았다.

## 2. 수정과 검증

수정 커밋은 `<<sha:Fix inactive mixer evidence path isolation>>`이다. 기존 폴더에서는 `verify_inactive.py`의 사전 경로 검사만 바꾼다. 기존 조상 링크 거부 후 candidate/evidence 경로를 정규화하고, 네 모드 모두 동일 경로·양방향 포함을 디렉터리 생성과 파일 쓰기 전에 거부한다. 후보43·의존86·자산40·메타8·결속·source inventory는 그대로다.

새 시험은 같은 소스로 수정 전후를 대조한다. 경로 중첩 36조건, 정상 형제 경로 4모드, 원 반례 뒤 재검사 1회를 구분하며, 메서드 수나 준비14·기존 loader5와 합산하지 않는다. 수정 전의 실패 수를 입력 오염 건수로 바꾸어 적지 않는다. 최종 수치·소스 해시·입력 보존은 `docs/reviews/mixer_inactive_path_fix_20261109/verification_summary.json`, 원로그는 전달 증거에 있다. Windows 시험 harness의 첫 argv 준비 실패는 대상 red와 분리 보존한다.

## 3. Claude 인계와 반박 창

- **반박 창 재확인 필요:** MIP-01/P2의 공통 경로 가드, 쓰기 전 거부, 파일·디렉터리 그래프 보존, 정상 형제 경로 회귀. 요청서는 `docs/reviews/mixer_inactive_path_fix_20261109/review_request.md`이며 전달 ZIP의 `SOURCE_PIN.txt`가 최종 핀이다. 발송은 1저자다.
- **Claude 반입:** 원 후보가 이미 반입됐다면 선행 사본을 중복 반입하지 않고 수정 커밋을 `cherry-pick -x`한다. 원 후보가 없다면 선행 사본과 수정 커밋 순서다. 원 핀·B·사본·수정 핀은 전달 대응표에서 구분한다.
- `ledger_proposal.json`은 MIP-01 `claimed_fixed`와 재확인 대기만 제안한다. 원장·공유 기록은 수정하지 않았다. 독립 종결·`verified`를 주장하지 않는다. 이전 MLA/MLAR/MGS 지적을 다시 열지 않는다.

전체 HOLD, 연구 결과0이다. Rint 파일, 실제 값·원자료, 연구 호스트·계산·제출·MPI, 운영 재봉인·예약 해제는 다루지 않았다. 채택된 믹서 정책은 유지하되 현장 자격·wave 승인·실행 GO를 대신하지 않는다. 이번 수정은 LHS·DEM 세대2의 진행이나 판정을 바꾸지 않는다.
