# MIP-01 잔여 경로 한정 수용 수령 — 2026-11-09

수령 커밋: `<<sha:Record limited acceptance of inactive mixer path fixes>>`. 새 가지 `codex/mixer-path-receipt-1109`, 바탕은 확인한 최신 B `69d714d094c4d210e5bf931d5c520e64ca0a751d`다. 문서4개 추가만이며 코드·시험·기존 문서·Rint·공유 원장을 바꾸지 않았다.

검토 핀 `dcfd62262f101598e4301862e2b3065c44514bb0`의 **MIPR-01/P2 잔여 보완이 수용됐고, 이전 일반 경로 가드와 합쳐 동일 MIP-01의 해당 해제 조건을 충족·한정 종결 가능**으로 수령했다. 새 P1/P2/P3 없음, 별개 P2 중복 계상 없음. namespace 사전 거부·입력 그래프 보존·일반 경로 회귀 범위이며 운영 봉인/실행 승인이 아니다.

수령 ZIP SHA256은 `17c4067801b47720635cddf99732487ef691028594976473d6e43d5ae75cecd9`다. 바이트·중첩 해시·고정 신원 수령 결과와 시험 수 구분은 `docs/reviews/mixer_path_limited_acceptance_20261109/intake_receipt.json`에 있다. 이번 반박 창은 loader5를 다시 실행하지 않았고 수령 창도 본안 시험을 실행하지 않았다. 독립 보조 감사의 61blob/전체tree 가정 오류와 정정 기록은 제품 결함 또는 성공 시험으로 세지 않는다.

확인 당시 B에는 이 준비/경로 후보가 아직 없었다. Claude는 최신 이력·patch-id·blob을 재확인하고 미반입분만 `be4388d0c1d3836bc44df0eada6793fbffdcd6e7` → `d310f741a636954b600c9e4f000bfccba2fee3ce` → `dcfd62262f101598e4301862e2b3065c44514bb0` → 이 수령 순서로 `cherry-pick -x`한다. 첫 준비는 원 `73e659273fd2ed6406a4c90011fc6079c7adf95f`/사본 `2ac1a2482f0290566ac1d67d972f7c9544a9d291`와 준비61blob 동등, 두 번째는 `3ca47af5b0acd1b39c1d437949413ef3ac31b831`와 동등하다. 동등 반입을 중복 적용하지 않는다. 원 증거와 이전 후보 인계 ZIP은 새 Claude 묶음에 원바이트로 담되 리포 반입에서 제외한다.

원장 제안은 동일 MIP-01 `claimed_fixed`에 한정 종결 근거를 보태는 것이다. 두 Codex 창 규약상 `verified` 자동 부여와 직접 적용은 없다. 반입 뒤 대응표·처분 회신이 필요하다. 이전 `PARTIAL_FIX_OPEN`/`PENDING` 문서는 역사로 보존하며 이 수령이 후속 판정을 연결한다. **같은 범위의 새 반박 요청은 없다.**

실제 OS 링크·적대적 동시 변경·타 OS/namespace 전수 자격, 운영 재봉인·현장·host/wave·실행 GO는 별도다. 다른 트랙과 기존 자산·정책 수용 범위는 바꾸지 않는다. 실제 값 열람·연구 실행·제출·MPI·운영 재봉인0, 연구 결과0, **전체 HOLD 유지**다.
