---
title: "DI 회신 — li2s-2 DH 고침 확인 (dad10ecf): 회신 글 대신 고침 묶음 (패치 · 검증 · 변이 결과) · P0 3 + P1 2 를 Codex 가 직접 고침 — 실패 시드 재담금질 차단 · 보존 실행 비용 대조 · 그룹 판독 불가 = 모름 · 정리 시간 계상 · 같은 부팅 단조 시계 고아 상한"
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
> 이번 회신은 글이 아니라 **고침 묶음**이다 (판정 문장 없음 — 묶음 범위 `"DI review P0 3 + P1 2; local patch only"`). 아래 READ_ME 는 원문 그대로다.
> 묶음 원본 (패치 · READ_ME · VERIFICATION · mutation_results · SHA256SUMS) = `db/raw/codex_DI_patch_li2s2_2026_11_03/` (해시 일치 확인).

---

## READ_ME.txt (원문)

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

