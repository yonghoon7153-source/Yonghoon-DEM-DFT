---
title: "EF 프롬프트 — b2o3 B·O 배치 9 단계 DFT 도구 · 카드 개정 5 (결과 전): 출력 결속 · EOS (E, P, V) 결과 파일 결속 (DY 확인 4) · k 탐침 발동 범위 · 기준 셀 · 10 단계 고르기 — DFT 진입 GO 여부 (DFT 결과 0 건)"
date: 2026-11-13
updated: 2026-11-13
tags: [review, b2o3, dft, qe, eos, kprobe, readout, codex, prompt, letter]
letter: EF
track: b2o3
channel: codex
kind: prompt
status: 작성 2026-11-13 · gabia 검사 결과 넣음 · 발송 (사용자) · 코드 기준 커밋 4b95dedb (브랜치 claude/evac-2026-11-12 · 도구 sha256 559f0152) · 앞 편지 DY (GO · 1 단계 UMA)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = b2o3 UMA-MD / B₂O₃ 계산 쪽 (1저자 = 사용자). ⛔ b2o3 전도도 (D · Ea · σ) 값은 싣지 않는다 (08-25 마감 · 인용 불가).
> ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_EF_reply_b2o3_dft_stage9_tools_2026_11_13.md` 로 원문 보존.
> ⚠ GO 가 와도 **개정 5 는 사용자가 비준**한다 (리뷰 GO ≠ 카드 비준) · 비준 전에는 GPU DFT 를 던지지 않는다.

---

**[b2o3 · 9 단계 DFT] 도구 · 카드 개정 5 확인 — DFT 진입 GO 여부 (DFT 결과 0 건)**

## 0. 무엇을 묻나

1 단계 UMA 는 끝났다 (8 단계 54 런 · 8b 진단 사유 ③ — 100 ps 본 판독은 보존 · 최종 UMA 승자 서술은 안 함). 다음은 카드 개정 1 의 9 단계 DFT (가족마다 UMA 최저 둘 = 단일점 6 → 가족 대표 셋 k 탐침 → 가족 대표 셋 고정셀 이온 이완 → 압력 어림으로 EOS 생략 판정) 와 10 단계 고르기다. DY 회신은 **EOS 의 (E, P, V) 결과 파일 결속을 DFT 진입 전 조건**으로 남겼다 (확인 4).

이번에 들인 것:
- `tools/doping/b2o3_bo_dft.py` (새 도구 · `prepare` · `read_sp` · `read_kprobe` · `read_relax`) — 판 고정 판독기 (`b2o3_bo_readout.py` sha256 872d91f7… = 12b8bdef · DY GO 판) 의 `anneal_readout` · `end_motif` · `eos_robust` 를 불러 쓴다 (판독기는 안 고친다). 실행기는 기존 `tools/doping/run_force_check_scf.sh` (12b8bdef 와 바이트 같음).
- 카드 `db/properties/b2o3_bo_placement_estimand_2026_11_09.json` 키 `개정_5_9단계_DFT_운영_2026_11_13` + 결정 `D-2026-11-13-b2o3-bo-placement-amend5-dft` (proposed).
- 회수본 `db/raw/b2o3_bo_stage1_2026_11_13/` (8 단계 결과 · 판독 · 8b 진단 · 끝 구조 — md.traj 는 없다 · SHA256SUMS 267 개).

**묻는 것**: 이 도구 · 운영값으로 9 단계 DFT 를 (사용자 비준 뒤) 시작해도 되나 — GO / 조건부 GO / NO-GO.

## 1. 도구가 하는 것 (단계 사슬)

| 단계 | 하는 것 | 결속 |
|---|---|---|
| prepare | 판 고정 판독기로 8 단계 본 판독을 **다시 내고** 본 판독 파일과 몸통 대조 (보류면 멈춤) → 판독기의 성공 정의 그대로 가족마다 E_post_relax 낮은 순 둘 (같으면 바탕 번호) → 가족 최저 · 성공 수를 본 판독과 대조 → 단일점 입력 (UMA post_relax 기하 그대로 · 셀 포함 · 원자 순서 그대로 · k 3×2×1) · 계획 `dft_plan.json` | 도구 · 판독기 sha256 · 묶인 입력 4 (sha256) · 유사포텐셜 6 (원소 머리 · sha256 · md5) · 구조 파일 sha256 (결과 기록의 outputs.post_relax 와 같아야) · 입력 sha256 |
| read_sp | 계획을 다시 결속 (8 단계 다시 내기 · 고르기 다시 내서 계획과 같음 · **입력을 묶인 구조에서 다시 만들어 sha256 대조**) → 단일점 출력 6 검사 → 가족 대표 = 가족마다 단일점 최저 → 단일점 순서 (G5 기록 · 판정 아님) → 탐침 입력 셋 (같은 구조 · 4×2×1) | 출력마다 아래 §2 검사 · 단계 안 k 점 수 · PWSCF 판 같음 |
| read_kprobe | 단일점 판정을 출력에서 다시 내서 대조 (행 · 대표 · 탐침 잡 입력) → 탐침 출력 셋 → 발동 판정 (§3) → 발동 안 하면 이온 이완 입력 셋 (기준 셀 §4) · 발동하면 멈춤 (다음 = `prepare --k_main 4 2 1 --after_kprobe` 새 폴더 · 그 판은 탐침 없이 이완) | 발동 판정 · 쌍 · 기준 셀 · 이완 잡 입력을 뒤 단계가 다시 낸다 |
| read_relax | 앞 판정 사슬 전부 다시 결속 → 이완 출력 셋 → 가족마다 **(E, P, V) 를 출력에서 읽음** (E = 마지막 '!' = Final energy · P = 마지막 SCF 뒤 응력 kbar ÷ 10 · V = 출력 부피 = V₀ ± 0.01 Å³ · 출력 sha256 을 판정에 적음) → 판 고정 `eos_robust` → EOS 생략이면 DFT 순서 · 승자–차저 0.10 판정 · 10 단계 고르기 · 아니면 'EOS 필요' 에서 멈춤 (고르기 안 함) | 이완 구조 파일 (extxyz · sha256 · 부모 = 단일점 대표 구조 해시) · 기록 (O 끝 꼴 · B · P 배위) |

## 2. 출력 검사 (잡마다 · 하나라도 걸리면 그 단계 판정 안 함)

JOB DONE · '!' 총에너지 · SCF 수렴 (convergence NOT achieved 없음) · 출력에 찍힌 입력 이름 = scf.in · 원자 수 128 · ecutwfc 52 · ecutrho 520 · scf convergence threshold 1.0E-08 · Gaussian smearing 폭 0.0100 · 교환상관 SLA PW PBX PBC · 비스핀 · 유사포텐셜 원소 집합 · 파일 이름 · MD5 (계획 값) · 출력 셀 축 = 입력 셀 (1e-4 Å) · **처음 좌표 = 이 잡 입력의 좌표** (1e-4 Å · 다른 잡 출력 바꿔치기) · prefix (./tmp/<잡>.save · .bfgs) · 단일점 · 탐침은 힘 블록 · 이완은 'bfgs converged' · 최종 좌표 블록 (원소 순서 = 입력) · Final energy = 마지막 '!' (1e-6 Ry) · 응력 (P) 이 마지막 '!' 뒤 · 부피 = V₀. 누락 (출력 없음) 은 실패가 아니다 — 다 돌린 뒤 판독. 실패 잡은 같은 폴더 · 같은 입력으로 다시 (러너가 끝난 잡은 건너뛴다).

파서는 실제 QE 7.4.1 출력 둘 (`db/raw/li2s_neb_cellconv_2026_10_09/c222/li2s/ep_final/relax.out` · `db/raw/lpscl_glass_model_check_2026_10_19/qe_sp/kpt/k222_A_s3/scf.out`) 로 맞췄다 (줄 모양 · 단위). selftest 의 가짜 출력은 이 줄 모양을 흉내 낸다.

## 3. 개정 5 의 운영값 [제안] — 판단 요청

- **SCF**: 개정 1 그대로 (PBE · 52/520 · gaussian 0.01 · nspin 1 · conv_thr 1.0d-8) + mixing plain 0.3 · electron_maxstep 200 · david · disk_io nowf · tprnfor 모든 잡 · tstress 이완만.
- **유사포텐셜 파일**: li/s/cl `_pbe_v1.4.uspp.F.UPF` · `P.pbe-n-rrkjus_psl.1.0.0.UPF` · `B.pbe-n-kjpaw_psl.1.0.0.UPF` · `O.pbe-n-kjpaw_psl.0.1.UPF` (7 월 원본과 바이트 같음은 보증 못 함 — 원본은 저장소 밖 · 기록 · 대조만).
- **k 탐침 발동**: 세 가족 쌍 **모두**에서 (차가 0.05 eV/B₂O₃ 넘게 변함 · 가족 순서 바뀜 · |차| 가 0.10 경계를 건넘) 중 하나 — 개정 1 문구 '가족 차' 를 승자–차저 쌍만으로 읽지 않았다.
- **기준 셀**: host `modelc_V0_k663.xyz` × (1,2,1) 의 cellpar (60° 셋 · V 2432.764) 를 V₀ 2436.33 Å³ (옛 챔피언 BM3) 로 등방 스케일 (×1.000488) → 가족 대표 구조의 **분수 좌표를 그대로** 넣는다. UMA 셀은 host 대비 −0.08 … −2.29 % 작고 각도가 0.2–1° 다르다 (회수본 실측).
- **이온 이완**: bfgs · forc_conv_thr 1.0d-3 Ry/Bohr · etot_conv_thr 1.0d-5 Ry · nstep 200 · 셀 고정.
- **10 단계**: EOS 생략일 때만 — 승자–차저 ≥ 0.10 이면 그 가족의 UMA 어닐 최저 셋 · 아니면 가족마다 최저 하나 · 전자구조 대상 = 이완 셋 (부모 해시).
- **실행**: gabia GPU (한 번에 한 잡) · `MIN_FREE_MIB=45000` (다른 GPU 잡이 있으면 시작 안 함 — UMA 와 동시 금지) · 메모리 프로브 (검사용 CPU · 120 초) 먼저.

⚠ **압력 민감도** (selftest 에서 드러남): 이 셀 (2436 Å³) 에서 −P²V/(2B) 는 |P| 0.3 GPa 에 0.02–0.03 eV · 0.5 GPa 에 0.06–0.09 eV — 0.10 여유와 같은 크기다. 가족 사이 압력이 0.3 GPa 넘게 다르고 차가 0.10 근처면 규칙대로 EOS 로 간다. EOS 절차 (부피 격자 · BM3 · 어느 셀) 는 이 판에 없다 — 생략 불가면 멈추고 어느 셀인지 말한다.

## 4. 시험

selftest **66/66** (양성 · 음성 · 판정 파일 손댐 · 출력 바꿔치기 · 입력 · 계획 sha 를 같이 고친 경우 (mixing_beta) · 발동 경로 · 4×2×1 판 · 가짜 '발동' 판정 · EOS 생략 / 불가 두 가지 · 10 단계 두 갈래). 8 단계 결속은 selftest 에서 가짜 판독기 (`_FakeRD` — `anneal_readout` · `verify_screen_verdict` · `load_records` 만 가짜 · `eos_robust` · `end_motif` · `_core` · `CONTRACT` 는 진짜 판 고정 판독기) 로 돈다.

깨기 **38/38 빨강** — 검사 하나씩 끄고 selftest 가 빨개지는지 (출력 검사 17 · 결속 · 다시 내기 13 · 탐침 3 · 기준 셀 host · 원소 머리 · 고르기 규칙 · 덮지 않음). 처음엔 37/38 이었다 (입력 · 계획 sha 를 같이 고친 경우를 잡는 시험이 없었다 → 넣었다).

회수 구조 여섯 (F_B cfg0040 · cfg0015 · F_P cfg0015 · cfg0019 · F_free cfg0039 · cfg0017) 으로 입력 · 기준 셀 매핑 · 기록을 로컬에서 확인 (P 전부 4 배위 · 끝 꼴 매핑 전후 같음).

**gabia 검사 (2026-11-13 · GPU 안 씀 · 런로그 `9단계_검사_1` · `9단계_검사_2`)**: worktree 4b95dedb · 도구 sha256 OK · selftest 66/66 · 유사포텐셜 md5 li e912e257 · s 88d86576 · cl fc6f6913 · P 8b930f41 · O 0234752a (li · s · cl · P 는 kgy 사본과 같은 md5) · B 는 처음에 없어서 첫 prepare 가 'B 없음' 으로 멈췄다 — **그 전에 8 단계 결속 (판 고정 판독기로 본 판독 다시 내기 · md.traj 검사 포함 · 몸통 대조 · 성공 목록 대조) 은 실제 데이터로 통과했다** (prepare 는 PP 를 보기 전에 결속한다). B 는 gabia 안의 사본 둘 (옛 b2o3 탄성 DFT · lpsocl DFT 폴더 · md5 둘 다 8c825a59) 을 복사 → 두 번째 prepare 통과 (구조 파일 결속 · 단일점 입력 6 · 고른 것은 위 여섯과 같음). 메모리 프로브 (CPU 1 랭크 120 초) 는 FFT 격자 (조밀 3,285,041 G-벡터 · 96×192×486) 까지 · 어림 줄 전에 끝 — 유사 계 실측 (kgy GPU · 120 원자 · 52/520 · 같은 GBRV + P rrkjus: k 1 점 12.35 GB · 8 점 29.36 GB) 으로 이 계 단일점 (k 4 점) ≈ 17–20 GB 어림 (A6000 48 GB).

코드 기준은 커밋 4b95dedb (도구 · 카드 개정 5 · 결정 · 이 편지) — 그 뒤 브랜치 커밋은 런로그 · 미결 리스트 · 이 편지의 검사 결과 문단뿐이다 (도구 변경 없음).

## 5. 일부러 안 한 것

- EOS 절차 (생략 불가일 때) — 멈춘다. 결과를 본 뒤 정하지 않도록 지금 정해 두자는 지적이 있으면 받는다.
- 이완 뒤 골격 판정 — B · P 배위 · O 끝 꼴은 기록만 (카드 G7).
- 단일점 순서의 판정화 — G5 기록 · 'DFT 순위' 라고 쓰지 않는다 (절차 9_DFT_확인 ⛔).
- 다른 기계 · 여러 GPU 병렬.

## 6. 질문

- **Q1** 출력 결속 (§2) 에 구멍이 있나 — 특히 출력 바꿔치기 · 앞 걸음의 압력 · 부피 · 다른 셀 · PP 판 · 재시작 섞임 · 끝나지 않은 relax 를 끝난 것으로 읽는 경로.
- **Q2** DY 확인 4 (EOS 의 (E, P, V) 결과 파일 결속) 가 이것으로 닫혔나.
- **Q3** k 탐침 발동을 세 가족 쌍 모두로 읽은 것 · '0.10 경계 건넘' 을 |차| 기준으로 본 것이 개정 1 (DU P1-5) 의 뜻에 맞나.
- **Q4** 기준 셀 (host 모양 · V₀ 등방 스케일 · 분수 좌표 이식) 과 이완 문턱 (1.0d-3 · 1.0d-5 · 200) 이 0.10 eV/B₂O₃ 판정에 충분한가.
- **Q5** 압력 민감도 (§3 ⚠) 를 보고 — EOS 절차를 지금 (결과 전) 정해 둬야 하나, 생략 불가면 멈추는 지금 판으로 충분한가.
- **Q6** 10 단계 기계화 · 전자구조 대상 계보가 개정 1 · 절차 10_고르기와 맞나.
- **Q7** SCF 운영값 (mixing 0.3 · maxstep 200 · nowf) 과 PP 파일 이름에 문제가 있나.
- **Q8** DFT 진입 전에 더 닫을 것이 있나 — 없으면 사용자 비준만 남는가.

## 7. 회신 형식

GO / 조건부 GO / NO-GO 한 줄 → P0–P3 (파일:줄 · 재현 · 최소 수정) → Q1–Q8 → DFT 진입 전 마지막 확인 목록.
