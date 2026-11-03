---
title: "DI 회신 — li2s-2 DH 고침 확인 (dad10ecf): NO-GO · P0 3 (fail 시드 재담금질 · 보존 실행 비용 누락 · 프로세스 조회 불가 = 빈 그룹) · P1 2 (정리 시간 · 벽시계 역행) → Codex 가 고침 묶음까지 (패치 · 검증 · 변이) — 실패 시드 재담금질 차단 · 보존 실행 비용 대조 · 그룹 판독 불가 = 모름 · 정리 시간 계상 · 같은 부팅 단조 시계 고아 상한"
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, reply, letter, patch]
letter: DI
date: 2026-11-03
track: li2s
channel: codex
kind: reply
status: 수령 2026-11-03 (사용자 업로드 zip `li2s2_DI_fixes_dad10ecf.zip` · 원문 READ_ME 그대로 · 검증 · 변이 결과는 JSON 원문을 표로 · 묶음 원본은 db/raw/codex_DI_patch_li2s2_2026_11_03/) → 패치 그대로 적용 (b7d11f81)
confidence: medium
verificationStatus: verified
verifiedAt: 2026-11-03
verifiedBy: self
explored: false
authoredBy: external
claimType: mixed
evidenceScope: multi-source-primary
---

> 프롬프트: `codex_DI_prompt_li2s2_dh_fixes_2026_11_03.md` (기준 커밋 `dad10ecf`) · 트랙 li2s-2 (논문 1저자 = 외부 · 위임 10-30).
> 회신 = **검토 글 (NO-GO · P0 3 · P1 2 · 사용자가 11-03 붙여넣음)** + 사용자 'ㄱㄱ' 뒤 Codex 가 만든 **고침 묶음** (zip). 둘 다 아래에 원문 그대로다.
> `<codex>` = `C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_DI_20261103`.
> 묶음 원본 (패치 · READ_ME · VERIFICATION · mutation_results · SHA256SUMS) = `db/raw/codex_DI_patch_li2s2_2026_11_03/` (해시 일치 확인).

---

## 검토 글 (원문)

NO-GO — 첫 담금질 실행은 아직 보류입니다. P0 3건, P1 2건이 남습니다.

dad10ecf의 DH 수정분을 확인했습니다. 기존 반례 상당수는 막혔지만, 옆으로 옮긴 과거 실행을 다루는 경로와 프로세스 종료 확인에 구멍이 남았습니다.

드라이버 191건, 러너 47건 통과를 재현했습니다. 러너는 Windows에서 실행했으므로 Linux 전용 실제 프로세스 시험은 제외했습니다. 아래 추가 검증은 합성 산출물과 가짜 시계·프로세스를 사용했고, 실제 판정 함수와 러너 제어 흐름을 실행했습니다. UMA·MD·DFT는 실행하지 않았습니다. 제시한 변이시험 53건 전체는 별도로 재현하지 않았습니다.

1. P0 — 과학적으로 탈락한 시드도 폴더를 옮기면 재담금질할 수 있습니다.
   [li2s2_stage1_runner.py (line 447)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:447)
   현재 러너는 해당 경로의 판정 파일이 없으면 새 실행을 허용합니다. 장부에 남은 **같은 계·시드의 이전 fail**은 재실행 금지에 연결되지 않습니다.
   직접 재현한 순서는 다음과 같습니다.
   - A12의 최종 PS₄ 보존율이 기준을 못 넘도록 설정 → fail.
   - A는 4/5 통과, 다음 단계 선정 시드는 [11, 13].
   - A/seed12를 A/seed12.failed_archive로 옮기고 재시작.
   - 러너가 A12를 다시 실행하고 통과 결과를 받아, A는 5/5·선정 시드는 **[11, 12]**로 변경. 종료코드 0.
   이는 카드의 **"미통과 시드는 기록·제외하고 다시 담금질하지 않는다"**와 충돌합니다. invalid 복구를 열면서 fail까지 복구할 수 있게 된 것입니다.
   최소 수정: 실행 허용 여부를 폴더 존재가 아니라 그 시드의 전체 실행 이력으로 판단하세요. 과학적 fail은 유지하고, 재시도는 특정 이전 run_id의 기술적 무효 판정과 복구 사유에 연결해야 합니다. 새 run_id만 발급하는 것으로는 부족합니다.
2. P0 — 옆으로 옮긴 실행의 비용 행이 빠져도 장부 검사를 통과합니다.
   [melt_quench_uma.py (line 1189)](<codex>/source/tools/ionic/melt_quench_uma.py:1189), [같은 파일:1216 (line 1216)](<codex>/source/tools/ionic/melt_quench_uma.py:1216)
   ledger_check가 비용과 연결하는 대상은 현재 정규 경로에 있는 판정뿐입니다. 보존한 seed11.invalid_*의 실행은 검사 대상에서 빠집니다.
   문서에 적힌 복구 절차 그대로 시험했습니다. A11 invalid → 폴더 보존 → ack → 정상 10런을 완료하면 장부는 11런, 합성 비용은 52 h입니다. 여기서 보존된 invalid 실행의 장부 행 하나만 제거했더니:
   - 과거 폴더는 그대로 존재.
   - 비용은 50 h로 감소.
   - invalid=[], pending=[].
   - 묶음은 stage1_pass, 러너도 rc=0.
   최소 수정: 현재 채택된 실행과 보존·중단된 실행을 모두 포함하는 실행 목록을 만들고, 모든 실행의 run_id와 비용 행을 대조하세요. 과거 실행을 통과 시드 수에서 제외하는 것과, 비용 검증 대상에서 제외하는 것은 다릅니다.
3. P0 — 프로세스 정보를 읽지 못한 경우를 '그룹이 비었다'로 처리합니다.
   [li2s2_stage1_runner.py (line 218)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:218), [같은 파일:232 (line 232)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:232)
   _group_members는 /proc/<pid>/stat의 모든 OSError를 무시하고, _pg_alive는 나머지 예외도 False로 바꿉니다.
   대표는 종료됐고 남은 일꾼의 stat 읽기에 PermissionError가 발생하도록 주입했습니다. 실제 함수 반환은:
   members=[]
   pg_alive=False
   group_empty=True
   signals=[]
   즉, 종료를 확인하지 못했는데 신호도 보내지 않고 정리 완료로 기록합니다. 이 재현은 읽기 실패를 주입한 제어 흐름 시험이며, 실제 kgy에서 권한 오류가 발생했다고 주장하는 것은 아닙니다.
   최소 수정: 살아 있음 / 비었음 / 확인 불가를 구분하세요. 조회 도중 사라진 프로세스와 권한·입출력·해석 오류를 같은 것으로 처리하면 안 됩니다. 확인 불가이면 실행 항목을 닫지 않고 재개도 막아야 합니다. 전체 /proc를 읽을 수 없는 환경에서는 자기 그룹의 부재를 확인할 수 있는 별도 경로가 필요합니다.
4. P1 — 정상 종료 뒤 그룹 정리에 쓴 시간이 비용에서 빠집니다.
   [li2s2_stage1_runner.py (line 523)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:523)
   el을 계산한 뒤에 stop_child()를 호출하고, 정리 전 el을 그대로 장부와 상한 판정에 사용합니다.
   시험 카드의 상한을 50.1 h로 두고, 실행 10건을 각 5 h·그룹 정리를 각 60초로 설정했습니다. 실제 실행＋정리는 50.1667 h인데 장부는 50 h, 묶음은 stage1_pass, rc=0이었습니다. 이 숫자는 실제 캠페인 비용이 아닌 합성 시험값입니다.
   최소 수정: 그룹 정리 후 경과시간을 다시 계산해 finish와 종료 후 상한 검사에 같은 값을 사용하세요. 상한·녹음 중단 경로는 이미 정리 후 시간을 재고 있으므로 정상 종료 경로도 맞추면 됩니다.
5. P1 — time.time() 차이는 항상 보수적인 경과시간이 아닙니다.
   [li2s2_stage1_runner.py (line 295)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:295), [같은 파일:413 (line 413)](<codex>/source/tools/ionic/li2s2_stage1_runner.py:413)
   실행 중 시스템 시계가 뒤로 보정되면 비용이 줄어듭니다. 합성 시험에서 첫 실행 중 시계를 4시간 되돌리자, 실제 실행 합계 50 h가 장부에서 46 h가 되어 47 h 상한 아래로 통과했습니다.
   최소 수정: 실행 중 경과시간과 종료 대기는 단조 시계를 사용하세요. 재시작 후 고아 실행의 상한도 동일 호스트·부팅 구간의 지속 가능한 시계 기록 등으로 근거를 확인해야 합니다. 확인할 수 없다면 upper_bound로 확정하지 말고 비용 미확정으로 남기면 됩니다. Python도 time.time()의 역행 가능성과 monotonic()의 차이를 명시합니다. Python 시간 함수 문서

DH 지적별 판정은 다음과 같습니다.
- DH P0-1 장부: 부분 해제. 빈 장부·현재 실행 한 행 누락·음수 비용은 무효, 미종료 비용은 대기, 장부 없는 산출물은 rc=10으로 거부했습니다. 다만 위의 보존된 실행 비용 누락은 남습니다.
- DH P0-2 실행 식별: 기존 반례 해제. A11 폴더를 A12로 복사하면 무효·rc=27·추가 실행 0건입니다. 이번 문제는 식별자 중복이 아니라 같은 시드의 재시도 자격입니다.
- DH P0-3 그룹 정리: 부분 해제. 대표가 먼저 끝나도 남은 일꾼에 TERM→KILL을 보내는 흐름은 확인했습니다. 다만 조회 실패를 빈 그룹으로 판정하는 경로가 남습니다. 실제 Linux 프로세스 시험은 여기서 재검증하지 못했습니다.
- DH P1-4 invalid 구분: 기존 반례 해제. invalid는 비영구 STOP·rc=27이고, 문서대로 복구하면 이전 비용을 유지합니다. 그러나 그 복구가 과학적 fail에도 적용되는 문제를 닫아야 합니다.
- DH P1-5 재판정 이력: 해제. final.xyz 변경 후 재판정할 때 이전 판정 전체·이전/새 지문·변경 파일·사유가 남는 것을 확인했습니다.

새 질문 다섯 개에 대한 답입니다.

Q1 — 고아 실행의 보수 상한: 조건부 찬성입니다.
그룹의 종료를 확인했고 시간차가 유효하다면, 오래 비운 기간까지 포함해 과다 계상하는 방식은 가능합니다. 더 정밀한 드라이버 종료 기록을 반드시 요구하지는 않습니다. 다만 현재는 위 P0-3과 P1-5 때문에 "종료 확인 시각−시작"이 항상 확인된 상한이라는 보장은 없습니다. 드라이버 종료 시각만 추가해도 남은 일꾼의 종료까지 증명되지는 않습니다.

Q2 — 현재 판정이 없는 실행을 비용으로만 더하기: 용도 분리는 맞지만 현재 구현은 부족합니다.
중단·무효 실행을 통과 시드 수에 넣지 않는 것은 맞습니다. 그래도 실행 신원·보존 위치·비용·재시도 자격은 계속 검사해야 합니다. 특히 과학적 fail은 비용만 남기고 판정에서 사라지면 안 됩니다.

Q3 — pgrp 밖으로 나가는 손자를 놓치는 한계: 제한된 운영 가정으로는 수용 가능합니다.
확인한 PyTorch 2.8.0의 Inductor 작업자 생성 경로에는 새 세션·그룹을 만드는 Popen 옵션이 없습니다. 따라서 일반적인 해당 경로가 그룹을 상속한다는 판단에는 근거가 있습니다. 그러나 이것이 모든 UMA·Torch 실행과 외부 실행 래퍼를 보증하지는 않습니다. PyTorch 2.8.0 작업자 생성 코드

현재 단일 러너의 지원 범위를 명시하고 그룹을 이탈시키는 실행 래퍼를 지원하지 않는 방식은 가능합니다. 이번 승인에 cgroup 전면 도입까지 요구하지는 않습니다. 다만 지원하는 그룹조차 조회 실패 때 비었다고 판단하는 P0-3은 별개입니다.

Q4 — 러너 전용 판정: 찬성입니다.
--print_cmd는 명령 확인용으로 남기고, 손 실행을 자동으로 공식 시드에 포함하지 않는 것이 맞습니다. 나중에 손 실행을 수용하려면 UUID를 붙이는 것뿐 아니라 실제 실행·비용·산출물을 등록하는 절차가 필요합니다.

Q5 — 새 조용히 틀린 경로: 위 다섯 건입니다. 핵심은 현재 경로에서 사라진 실행도 과학적 이력과 비용에서는 사라지면 안 된다는 점입니다.

재승인 때는 우선 실패 시드 재시도 차단, 보존된 실행까지 비용 대조, 프로세스 조회 불가 시 종료 확정 금지의 세 P0를 닫아 주세요. 비용 시간 처리 두 P1도 같은 수정에서 함께 고치는 것을 권합니다.

재현 증거는 [기존 반례 및 추가 시험 결과](<codex>/scratch/di_probe_oyvrqcgt/results.json)와 [구조 탈락 재시도·시계 역행 시험 결과](<codex>/scratch/di_probe_jjwvtasw/results.json)에 보존했습니다. 원 저장소는 수정하지 않았습니다.

---

(사용자 → Codex: "ㄱㄱ" · 오후 7:30)

(Codex · 11분 30초 작업 뒤) DI의 P0 3건·P1 2건 수정본을 만들었어요.
- 드라이버 191건, 러너 56건 통과.
- 수정사항을 일부러 되돌린 6개 변이 모두 시험에서 검출.
- 패치 적용 및 적용 후 파일 해시 일치 확인.
[수정본·적용 패치·검증 기록 ZIP](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/fix_DI_20261103/li2s2_DI_fixes_dad10ecf.zip)

dad10ecf 기준 별도 사본입니다. 원격 저장소 반영과 실제 계산은 하지 않았어요. Linux의 실제 프로세스 종료 시험은 남아 있어 실행 승인은 아직 보류입니다.


## 지적 ↔ 적용한 고침 ↔ 우리 Linux 확인 (2026-11-03)

| DI 지적 | 패치 (b7d11f81) | 시험 (Linux 러너 58/58) |
|---|---|---|
| P0-1 fail 시드 재담금질 | 러너: 같은 계 · 시드의 이전 실행에 invalid 아닌 판정 (pass · fail · 미해결) 이 있으면 재담금질 거부 · invalid 재시도는 그 run_id 에 묶인 ack 된 STOP 이 있어야 · 소비자: 장부의 과학적 fail 을 다른 실행으로 대체하면 무효 | `DI 음성: 과학적 fail 폴더를 옮겨도 같은 시드를 재담금질하지 않는다` ⭕ |
| P0-2 보존 실행 비용 | `attempt_inventory` — 현재 · 보존 폴더의 stage1_attempt.json · plan.json 신원을 모두 장부와 대조 (없음 · 다른 시드 = 무효) · 담금질 전에 stage1_attempt.json | `DI 음성: 보존된 invalid 실행의 비용 행만 없어져도 묶음 무효` ⭕ · `DI 양성: plan 전 중단에도 실행 전 기록` ⭕ |
| P0-3 조회 불가 = 빈 그룹 | `_group_members` 가 사라진 프로세스 (ENOENT · ESRCH) 만 넘기고 권한 · I/O · 형식 오류는 '모름' (`_GroupStateUnknown`) · 자기 그룹 ESRCH 로만 부재 확정 · `_pg_alive` 모름 = None → 재개 거부 · `stop()` 은 모름이면 group_empty 거짓 | `DI 음성: /proc 권한 오류는 빈 그룹이 아니며` ⭕ · `DI 양성: ESRCH 확인이면 부재` ⭕ · `DI 음성: 그룹 조회 불가(None)면 재개 거부` ⭕ · 진짜 프로세스 그룹 셋 ⭕ |
| P1-4 정리 시간 누락 | 정상 끝에서 그룹 정리 **뒤에** 경과를 잰다 | `DI 음성: 그룹 정리 60초도 비용에 포함` ⭕ |
| P1-5 time.time 역행 | 러너 기본 시계 = time.monotonic · 고아 상한 = 같은 호스트 · boot_id 의 CLOCK_BOOTTIME 차 (아니면 비용 미확정) | `DI 음성: 벽시계 4 h 역행해도 비용 안 줄어듦` ⭕ · `DI 음성/양성: 고아 상한은 같은 부팅의 단조 시계만` ⭕ |

- Codex 가 남긴 승인 보류 사유 (Linux 실제 프로세스 종료 시험) → 이 컨테이너 (Linux) 에서 실행 · 통과 (러너 58/58 · 시험 뒤 남은 프로세스 0).

## 고침 묶음 — READ_ME.txt (원문)

```
DI 수정본 — dad10ecf 기준 적용용 패치

수정 파일은 tools/ionic/melt_quench_uma.py, tools/ionic/li2s2_stage1_runner.py 두 개입니다.
실패 시드의 재담금질 차단, 보존된 실행 비용 대조, 그룹 조회 불가 시 차단,
그룹 정리 시간 계상, 단조 시계와 동일 부팅 근거에 의한 고아 실행 비용 처리를 반영했습니다.
runner selftest에 9개 검사를 추가했습니다. 기존의 invalid 복구 양성 경로도 통과합니다.

저장소 루트에서 먼저 git apply --check li2s2_DI_fixes.patch로 확인하고,
충돌이 없을 때 git apply li2s2_DI_fixes.patch로 적용할 수 있습니다.
기준 커밋 이후 두 파일이 수정되었다면 새 변경을 덮어쓰지 말고 해당 차이를 대조해야 합니다.

검증: 드라이버 191/191, 러너 56/56 (Windows worker thread).
수정 6가지를 각각 되돌린 변이본은 모두 해당 음성시험에서 실패했습니다.
패치는 git apply --check 및 실제 적용 후 두 파일 SHA 일치를 확인했습니다.
Linux 전용 실제 프로세스 시험은 이 환경에서 실행하지 못했습니다.
배포 환경에서 두 도구의 --selftest를 실행하고 남은 프로세스가 없는지 확인해야 합니다.
이 묶음은 코드 수정·검증 자료이며 실제 담금질을 시작하거나 proposed 결정을 active로 바꾸지 않았습니다.

보존 폴더는 기존 run_root/A 또는 B 아래에 둡니다. 같은 시드의 과학적 pass/fail은 재실행할 수 없습니다.
invalid 재시도는 이전 run_id를 명시한 STOP 확인과 연결되며 이전 실행 비용도 남습니다.
새 실행에는 stage1_attempt.json이 생깁니다. plan 생성 이전에 중단돼도 이 파일을 보존해야 합니다.
옛 고아 실행에 단조 시계/부팅 기록이 없으면 비용 미확정으로 막힙니다. 0이나 UTC 어림으로 대체하지 않습니다.
```

## VERIFICATION.json (요지 · 원문은 db/raw)

- 기준 커밋 `dad10ecf327fe836b4d807a60cba4cc7056cc778` · 범위: DI review P0 3 + P1 2; local patch only
- 파일: `tools/ionic/melt_quench_uma.py` bc325e25ef7f2bba → ca81a6c3d554ce13 · `tools/ionic/li2s2_stage1_runner.py` ee20b434b428b590 → f52cf9fd48af8340
- 드라이버 selftest 191/191 · 러너 selftest (Windows 작업 스레드) 56 통과 · POSIX 전용 시험: not executed
- git apply --check True · 적용 왕복 SHA 일치 True · 코드 밖 파일 그대로 True
- 한계 (원문): Actual Linux process-group tests not run here. / No UMA/MD/DFT run. / No remote repo update or push. / Existing proposed governance decision unchanged. / Orphan executions without a matching host/boot clock remain cost-unknown; UTC difference is not substituted. / Archived attempts must stay inside the same run root A/B folders. Deleting all independent records is outside recovery capability.

## mutation_results.json (원문을 표로)

| 변이 | 통과 | 실패 |
|---|---|---|
| baseline | 11 | 0 |
| retry_guard_removed | 10 | 1 |
| archive_cost_join_removed | 10 | 1 |
| proc_error_swallowed | 10 | 1 |
| cleanup_cost_omitted | 10 | 1 |
| wallclock_duration | 10 | 1 |
| cross_boot_cost_accepted | 9 | 2 |

## 우리 쪽 확인 (2026-11-03 · Linux)

- 패치를 그대로 적용 (`git apply` · 두 파일이 묶음 사본과 바이트 일치 · 커밋 `b7d11f81`).
- 드라이버 selftest 191/191 · 러너 selftest **58/58** (묶음이 못 돌린 진짜 Linux 프로세스 그룹 시험 2 포함) · 시험 뒤 남은 프로세스 0.
- 변이 검사는 실행 기록 `회신_DI_2026_11_03` 에 (저장소 밖 복사본).

