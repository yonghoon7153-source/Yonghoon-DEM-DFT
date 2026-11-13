---
title: "EH 프롬프트 — b2o3 9 단계 DFT 도구 v3 (Codex EG NO-GO 고침) 재확인: 한 계산 상태 블록 문법 · 힘 원자 번호 · reject 대상 다시 결속 · G5 원자료 · GPU 조회 종료코드 · QE 판 고정 — DFT 진입 GO 여부 (DFT 결과 0 건)"
date: 2026-11-13
updated: 2026-11-13
tags: [review, b2o3, dft, qe, eos, kprobe, readout, codex, prompt, letter]
letter: EH
track: b2o3
channel: codex
kind: prompt
status: 작성 2026-11-13 · gabia v3 검사 결과 넣음 (HEAD df8ba73f2 · selftest 142/142 · prepare s9_v3 · reject 시운전) · 발송 2026-11-13 (사용자) → 회신 NO-GO (codex_EH_reply_b2o3_dft_stage9_v3_2026_11_13.md) · 코드 기준 커밋 f6b9d3a6 (브랜치 claude/evac-2026-11-12 · 도구 sha256 f6105cfc · 실행기 e2d6f728 · 변이 도구 760a0fb1) · 앞 편지 EG (NO-GO · v2 328cf95b)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = b2o3 UMA-MD / B₂O₃ 계산 쪽 (1저자 = 사용자). ⛔ b2o3 전도도 (D · Ea · σ) 값은 싣지 않는다 (08-25 마감 · 인용 불가).
> ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_EH_reply_b2o3_dft_stage9_v3_2026_11_13.md` 로 원문 보존.
> ⚠ GO 가 와도 **개정 5 는 사용자가 비준**한다 (리뷰 GO ≠ 카드 비준) · 비준 전에는 GPU DFT 를 던지지 않는다.

---

**[b2o3 · 9 단계 DFT] EG NO-GO 고침 (v3) 재확인 — DFT 진입 GO 여부 (DFT 결과 0 건)**

## 0. 무엇을 묻나

EG 회신 (NO-GO · P1 2 · P2 4 · v2 커밋 328cf95b · 도구 sha256 4e865e5c) 을 고친 v3 다. DFT 결과는 여전히 0 건 (GPU 잡 하나도 안 돌았다). 바뀐 것은 도구 `tools/doping/b2o3_bo_dft.py` (v3) · 실행기 `tools/doping/run_force_check_scf.sh` (GPU 조회 · 시험) · 변이 도구 `tools/doping/b2o3_bo_dft_mutations.py` (실행기 변이 추가) · 카드 `개정_5_9단계_DFT_운영_2026_11_13` 의 v3 문구 · 결정 `D-2026-11-13-b2o3-bo-placement-amend5-dft` 의 status_history (여전히 proposed). 판 고정 판독기 (`b2o3_bo_readout.py` 872d91f7… = 12b8bdef) 는 그대로다.

v3 sha256 — 도구 `f6105cfc2ae933eaf321472d232bca47d4512198a3d68c66a62b0b1804c6ab2e` · 실행기 `e2d6f72873e0e4f646a1a8ff6145c455b93fc39e2a4445486ca22b9721b903a9` · 변이 도구 `760a0fb11b4b67f932f5b2f6b38dae78cfb8d0537a19aaa1a4bd8fa0f7d1a603`. **코드 기준 커밋 `f6b9d3a6`** (도구 · 실행기 · 변이 도구 · 카드 · 결정 · 이 편지 초안) — 그 뒤 커밋은 런로그 · 이 편지 §4 · 미결 목록뿐이다 (코드 변경 없음 · gabia 는 `df8ba73f` 를 꺼냈고 도구 · 실행기 sha256 이 같다).

**묻는 것**: EG 반례가 v3 에서 막히는지 (재현해 보고) · 고치면서 새로 생긴 구멍이 있는지 → GO / 조건부 GO / NO-GO.

## 1. EG 지적 → v3 고침

| EG | v3 에서 한 것 | 위치 | selftest 반례 |
|---|---|---|---|
| **P1-1** 상태 결속 | **블록 문법 = 한 계산 상태** — 블록 표지 (`!` · 힘 · 응력 · bfgs converged · criteria · Final energy · Begin/End final · JOB DONE) 의 위치를 모두 모아 **개수 · 순서**를 본다. SCF: `!` 1 · 힘 1 · 응력 = tstress 면 1 아니면 0 · bfgs · criteria · Final · 최종 좌표 0 · `!` < 힘 (< 응력) < JOB DONE. 이완: SCF 마다 `!` → 힘 → 응력 한 벌이 다음 `!` (마지막은 bfgs converged) 앞에 · bfgs converged → criteria → Final energy → Begin final → End final → JOB DONE 이 한 번씩 이 순서로. **값 (E · 힘 · P · 최종 좌표) 은 이 문법이 맞을 때 마지막 묶음에서만** 읽는다. **마지막 힘 블록은 머리 바로 뒤 연속 행만 읽고 원자 번호가 정확히 1…nat** (누락 · 중복 · 순서). **최종 좌표 블록은 머리 하나 · 좌표 행 (4 칸) 만** | `state_problems` · `_force_rows` · `parse_pw_out` (`_pos`) | EOS 보류 (세 가족 P 2.5 GPa) + JOB DONE 앞 P=0 응력 조각 · 최종 좌표 하나 더 (Li +0.01) · 마지막 힘 0.05 + 작은 힘 블록 · 원자 1 행 빼고 2 행 복제 (128 행 그대로) · 응력이 bfgs converged 뒤 (개수는 맞음) · Final energy 가 최종 좌표 뒤 · 마지막 P 값 깨짐 · 최종 좌표 안 머리 둘 · 단일점에 힘 조각 · 응력 조각 · 원자 번호 · **실측 MLi_04_x108 에 응력 조각 · 원자 1 행 빼고 2 행 복제 · 최종 좌표 하나 더** |
| **P1-2** reject 대상 | 옮길 잡 목록을 **계획 · 앞 판정을 다시 결속해서** 얻는다 — sp = 계획 다시 결속 (8 단계 · 고르기 · 구조 · 입력) · kprobe = 단일점 판정 통째 대조 · relax = 탐침 판정 통째 대조 (**host 필수** · 4×2×1 판은 단일점 판정) · 판정 → 계획 고리 = `--plan`. 옮길 (이 단계) 출력은 이 검증에 쓰지 않는다. **잡 폴더는 단계 폴더 바로 아래 · 이름 꼴** (`sp_{FB,FP,Ffree}_{1,2}_cfgNNNN` · `kp_…_cfgNNNN` · `rx_…_cfgNNNN`) — 경로 문자 · 링크로 밖을 가리키면 거부 (읽기 · 옮기기 공통) | `_jobs_for_reject` · `_verify_for_reject` · `_job_dirs` | `jobs_relax[0].job = ../unrelated` (같은 입력 바이트 · 걸리는 출력) · 선언 안 된 `rx_FB_cfg0099` (입력 해시까지 맞춤) 를 목록에 더함 · host 없이 relax · 링크 · 모르는 가족 · 다른 단계 이름 · 다른 계획의 판정 |
| **P2-1** G5 캐시 | 계획의 8 단계 요약 (순서 · 승자 · 판정 · 차) 을 **다시 낸 본 판독과 통째로 대조** · G5 의 UMA 순서는 다시 낸 본 판독에서 | `_rebind_plan` · `_stage8_summary` · `_build_sp_verdict` | 계획의 순서만 뒤집기 |
| **P2-2** GPU 조회 종료코드 | nvidia-smi 원문 · 종료코드를 먼저 받고 **성공했을 때만** 숫자를 가공 (VRAM · 프로세스 조회 둘 다) | `_gpu_guard` | 46000 을 찍고 exit 9 (독점 · 빈 목록과 같이) · 빈 목록을 찍고 exit 9 |
| **P2-3** nvidia-smi 없음 시험 | 시험이 함수를 실제로 돌려 **종료코드와 거부 이유 (메시지)** 를 같이 본다 · nvidia-smi 없음 시험은 절대경로 `/usr/bin/env` · `/bin/bash` + 빈 PATH · '없다' 이유여야 통과 · 실행기 변이 7 개 (항상 허용 · 존재 검사 · 조회 종료코드 둘 · 숫자 아님 · 문턱 · 다른 프로세스) 를 변이 도구에 더함 | 실행기 selftest · 변이 도구 | 실행기 selftest 24 (v2 20) |
| **P2-4** 판 혼합 복구 | **QE 판 7.4.1 을 계약에 고정** (`qe_version`) — 판이 다른 출력은 **개별 출력 검사**에 걸리므로 reject 가 그 출력만 보존해 옮긴다 (도구가 '어느 것을 버릴지' 고르지 않는다 — 계약이 기준). 단계 안 판 같음 검사는 쓸모가 없어져 뺐다 | `out_problems` · `reject_outputs` | 단일점 하나만 7.3.1 → read_sp 거부 · reject 가 그 하나만 `.rejected.N` |

## 2. 실측 출력으로 확인한 것

- **블록 문법을 저장소의 실제 PWSCF 출력 전부에 걸었다**: JOB DONE 이 있는 고정셀 단일 실행 — SCF 176 (tprnfor · 7.4.1 172 · 옛 6.7MaX 4 — 문법은 판과 무관하게 통과하고 판 고정에는 걸린다) · relax 41 (7.4.1) — **모두 통과** (relax 41 은 SCF 마다 `!` · 힘 · 응력 (tstress 19 · 없는 것 22) 이 한 벌씩 경계 안 · 끝 순서 그대로). tprnfor 없는 SCF 1 개는 '힘 0≠1' 로 걸린다 (이 단계 입력은 늘 tprnfor).
- 최종 좌표 파서: 고정 원자 없는 relax 23 개 전부 읽음 (crystal · angstrom) · **고정 원자 (if_pos 열 7 칸) 가 있는 relax 18 개 (그래파이트 슬랩) 는 못 읽는다** — 이 단계 입력은 고정 원자가 없다 · 범위 밖으로 문서화 (만나면 거부).
- `MLi_04_x108` (nosym · tstress · 58 원자 · SCF 66) 원본은 문법 통과 · P −10.88 kbar · 힘 원자 1…58 · 최종 좌표 58 — EG 의 실측 반례 셋 (P=0 응력 조각 · 원자 1 행 빼고 2 행 복제 · 최종 좌표 하나 더) 은 selftest 안에서 그 파일에 직접 적용해 거부를 확인한다.

## 3. 시험

- **selftest 142/142** (v2 119) — 위 표의 반례 전부를 거부 이유 (메시지 문구) 까지 확인 · 양성 경로 (6 단일점 → 탐침 → 이완 → EOS 생략 → 10 단계 두 갈래 · 발동 경로 · 4×2×1 판 · EOS 보류) 는 그대로 지나간다. 가짜 이완 출력은 이제 실측 문법대로 SCF 마다 응력을 찍는다 (앞 걸음은 다른 값 — 잘못된 묶음을 읽으면 값이 갈린다).
- **깨기 (변이) 87/87 빨강** (로컬 · 변이마다 처음 ✗ = 그 변이의 자기 시험 — 예: 실행기의 nvidia-smi 존재 검사를 끄면 'nvidia-smi 없음 → 그 이유로 물러남' 이 실패한다) — 도구 80 · 실행기 7 (`python3 tools/doping/b2o3_bo_dft_mutations.py` · 약 7 분 · `--selftest` 는 정적 검사만). v2 의 변이 중 없어진 검사 넷 (SCF `!` 한 번 · 옛 힘 블록 · 'bfgs converged 없음' · 단계 안 판 갈림) 은 상태 결속 · 판 고정으로 대체되어 뺐다. 동등 변이 (출력이 같아 시험으로 가를 수 없는 것 — 예: 힘 행 읽기의 '행이 끊기면 끝' 은 verbosity 기본 출력에서 결과가 같다) 는 목록에 넣지 않았다.

## 4. gabia 검사 (v3 · GPU 안 씀)

2026-11-13 · 사용자 실행 · 런로그 `db/properties/b2o3_bo_placement_stage1_runlog_2026_11_09.json` 키 `9단계_v3_검사_2026_11_13`.

- worktree `$R/dft_src_v3` = **HEAD df8ba73f2** · 도구 sha256 `f6105cfc…` **OK** · 실행기 `e2d6f728…` **OK**.
- selftest **142/142** · 실행기 selftest **24 통과 · 0 실패** · 변이 도구 정적 검사 **7/7** (gabia `uma` env python · CPU · 검사용).
- **prepare v3 (새 폴더 `$R/s9_v3`)**: 판 고정 판독기 (872d91f7) 로 8 단계 본 판독을 **실제 데이터 (md.traj 포함) 로 다시 내고** 대조 → 통과 · 단일점 6 잡 (k 3×2×1) · 고른 구조는 v1 · v2 · 로컬 회수본 계산과 같다.
- **reject 시운전 (`--stage sp`)**: 계획 다시 결속 (8 단계 실제 데이터) 통과 → '옮길 출력 없음' (출력이 아직 없다) — EG P1-2 경로가 실제 데이터에서 돈다.
- 입력 지문: 6 입력 모두 `nosym = .true.` · `tot_charge = 0.0` · `disk_io = 'nowf'` · `K_POINTS automatic` / `3 2 1 0 0 0` · 입력 sha256 은 **v2 와 바이트까지 같다** (v3 는 입력 쓰기를 안 바꿨다 · 로컬 재생성과도 6/6 같음) · 계획 `574f066b93416bc4` (도구 sha · 계약 qe_version 이 들어가 v2 와 다름).
- GPU pw.x 경로 `/data/apps/qe-7.4.1-gpu/bin/pw.x` (→ `../PW/src/pw.x` 링크 · 실행 안 함 · 출력의 판 7.4.1 은 판독 때 잡마다 대조).
- GPU 지금: 여유 48,539 MiB · 사용 1 MiB · compute 프로세스 없음 (시작은 안 했다).
- 깨기 87/87 은 로컬 수치다 (gabia 에서는 정적 검사만 · 같은 도구 sha256).

## 5. 일부러 안 한 것

- EOS 절차 — 생략 불가면 멈춘다 (안정성 · 전자구조 대상 null).
- 수렴 재확인 — 판정을 이 설정에 조건부로 둔다.
- GPU 공통 잠금 — 시작 때 확인 + 운영 규칙.
- 재시작 이어 붙이기 · vc-relax · 고정 원자 · verbosity high · 다른 QE 판 — 거부만 한다 (범위 밖).
- 이완 뒤 골격 판정 — 기록만 (카드 G7).

## 6. 질문

- **Q1** EG 의 반례 (P1-1 · P1-2 · P2-1 … P2-4) 가 v3 에서 막히나 — 가능하면 EG 때의 재현 자료 (`probes_v2_results.json` · `raw_results.json`) 로 다시 돌려 보고.
- **Q2** 블록 문법 검사 (개수 · 순서 · 마지막 묶음) 에 남은 구멍이 있나 — 특히 **개수 · 순서를 그대로 두고 블록 내용만 바꾼** 조각 (예: 마지막 묶음 안의 응력 행렬 · 힘 행 값을 다른 계산 것으로) · 중간 SCF 묶음을 통째로 바꿔치기. (출력 파일 sha256 은 판정에 기록되고, 이 도구는 위조 방지 장치가 아니라 섞인 · 잘린 출력을 거르는 장치라는 범위를 전제로.)
- **Q3** reject 대상 결속이 P1-2 를 닫나 — 다시 결속에 앞 단계 출력 (단일점 · 탐침) 이 유효해야 하는 것 (옮길 이 단계 출력은 안 본다) 이 순환인가.
- **Q4** QE 판 고정 (7.4.1) 으로 P2-4 를 닫는 것이 맞나 — 판이 다른 출력을 개별 실패로 보는 것.
- **Q5** DY 확인 4 (EOS 의 (E, P, V) 결과 파일 결속) 를 이제 해제할 수 있나.
- **Q6** DFT 진입 전에 더 닫을 것이 있나 — 없으면 사용자 비준만 남는가.

## 7. 회신 형식

GO / 조건부 GO / NO-GO 한 줄 → P0–P3 (파일:줄 · 재현 · 최소 수정) → Q1–Q6 → DFT 진입 전 마지막 확인 목록.
