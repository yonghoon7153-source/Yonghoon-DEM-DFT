---
title: "EG 프롬프트 — b2o3 9 단계 DFT 도구 v2 (Codex EF NO-GO 고침) 재확인: 한 출력 = 한 실행 · k 격자 대조 · 전자 수 · BFGS 기준 · 다시 결속 · EOS 보류 대상 null — DFT 진입 GO 여부 (DFT 결과 0 건)"
date: 2026-11-13
updated: 2026-11-13
tags: [review, b2o3, dft, qe, eos, kprobe, readout, codex, prompt, letter]
letter: EG
track: b2o3
channel: codex
kind: prompt
status: 작성 2026-11-13 · gabia v2 검사 전 (결과를 §4 에 넣은 뒤 발송) · 코드 기준 = 이 편지를 들인 커밋 (브랜치 claude/evac-2026-11-12) · 앞 편지 EF (NO-GO · v1 4b95dedb)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = b2o3 UMA-MD / B₂O₃ 계산 쪽 (1저자 = 사용자). ⛔ b2o3 전도도 (D · Ea · σ) 값은 싣지 않는다 (08-25 마감 · 인용 불가).
> ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_EG_reply_b2o3_dft_stage9_v2_2026_11_13.md` 로 원문 보존.
> ⚠ GO 가 와도 **개정 5 는 사용자가 비준**한다 (리뷰 GO ≠ 카드 비준) · 비준 전에는 GPU DFT 를 던지지 않는다.

---

**[b2o3 · 9 단계 DFT] EF NO-GO 고침 (v2) 재확인 — DFT 진입 GO 여부 (DFT 결과 0 건)**

## 0. 무엇을 묻나

EF 회신 (NO-GO · P1 6 · P2 6 · v1 커밋 4b95dedb · 도구 sha256 559f0152) 을 고친 v2 다. DFT 결과는 여전히 0 건 (GPU 잡 하나도 안 돌았다). 바뀐 것은 도구 `tools/doping/b2o3_bo_dft.py` (v2 · `reject` 명령 추가) · 실행기 `tools/doping/run_force_check_scf.sh` (`_gpu_guard`) · 카드 `개정_5_9단계_DFT_운영_2026_11_13` 의 v2 문구 · 결정 `D-2026-11-13-b2o3-bo-placement-amend5-dft` 의 status_history (여전히 proposed). 판 고정 판독기 (`b2o3_bo_readout.py` 872d91f7… = 12b8bdef) 는 그대로다.

v2 sha256 — 도구 `4e865e5c3e5785b24955b2805d11fe3f3905ca5ae1fc0911acd513f96e2f9048` · 실행기 `9157ca2cd953555a34e16bf2b51e6a3de1f3a71676ea4085ae29ef7c4923a04e` · 변이 시험 `tools/doping/b2o3_bo_dft_mutations.py` `0c8ef4871c0b82abab17190eb535ddc5af736f933fcbd2d7a1fad6c285ff9f93` (새 파일 · 아래 §3). 커밋은 이 편지를 들인 커밋이고, gabia 가 그 판을 꺼낸 HEAD 를 §4 에 적는다.

**묻는 것**: EF 의 반례가 v2 에서 막히는지 (재현해 보고) · 고치면서 새로 생긴 구멍이 있는지 → GO / 조건부 GO / NO-GO.

## 1. EF 지적 → v2 고침

| EF | v2 에서 한 것 | 위치 | selftest 반례 |
|---|---|---|---|
| **P1-1** 실행 섞임 | **한 출력 = 한 실행**: `Program PWSCF` 머리 1 · `JOB DONE` 1 · 설정 줄 (cutoff 둘 · 전자 수 · k 점 수 · conv_thr · 교환상관 · 결정 축 · 처음 좌표 · 부피 · alat) **각 한 번** · 이완은 문턱 둘 · nstep 각 한 번 · **JOB DONE 뒤에 계산 기록** (`!` 에너지 · 힘 · 응력 · bfgs · Final energy · 최종 좌표 · 머리 · k 점 수 · cutoff · 수렴 · 전자 수) **없음** · **SCF 출력은 `!` 한 번 · 이완은 `!` 수 = `bfgs converged in N scf cycles` 의 N** (중간에 끼워 넣거나 빠진 조각). 재시작 이어 붙이기는 지원하지 않는다 (실행기가 `> scf.out` 으로 덮어쓰고 nowf 라 재개가 없다) | `parse_pw_out` (`n_runs` · `n_job_done` · `once` · `once_relax` · `after_done`) · `out_problems` | ENCUT 40 · 미완료 둘째 실행 붙임 · 완료 relax 뒤 재시작 머리만 · 머리 없이 `!` 에너지 조각 · 머리 없이 cutoff 줄 · 느슨한 문턱 줄 한 번 더 · 단일점에 SCF 조각 (`!` 둘) · 이완 `!` 2 대 BFGS 3 |
| **P1-2** 다시 결속 | 계획을 다시 결속할 때 **구조를 8 단계 기록 (`_struct`) 에서 다시 찾아 계획의 구조 {rel · sha256} 와 대조** · **k 판 자격을 소비 단계에서도 같은 함수로** (`_k_main_check`: 3×2×1 = 탐침 판정 고리 없음 · 4×2×1 = 같은 8 단계 결과 sha 의 '발동' 탐침 판정이 있고 출력에서 다시 내도 발동) · 계획에 저장된 계약 · 유사포텐셜 기록도 지금 값과 대조 | `_rebind_plan` · `_k_main_check` | 이름은 cfg0003 그대로 · 구조를 같은 가족 다른 런 것으로 + 입력 · 해시 같이 고침 · k_main 을 4×2×1 로 + 입력 · 해시 같이 고침 (after_kprobe 없음) · 3×2×1 계획에 탐침 고리 · 발동 안 한 판정으로 4×2×1 · 다른 8 단계 결과 파일 계획에 남의 발동 판정 · 계약 (여유 0.10 → 0.05) · 가전자 기록 손댐 |
| **P1-3** 탐침 격자 | 입력에 **nosym** (시간 반전만 · 대칭 축소 없음) → 출력의 k 점 직교 좌표 (2π/alat) 를 출력의 결정 축으로 분수 좌표로 바꿔 **요청 격자 (shift 0) 위에 있는지 → 가중치 몫 (w·N/2 ∈ {1, 2}) → 격자 전체를 정확히 한 번씩 · 합 2** 를 본다. 점 수 비교가 아니다 | `kmesh_problems` | 탐침 출력이 3×2×1 목록 (4 점 · 같은 에너지) · 단일점 출력이 4×2×1 목록 · 단위 시험 (줄임 · 안 줄임 (noinv 꼴) 통과 · shift · 점 빠짐 · 가중치 1.5 배 · 짝 점 5/6 · 대칭 축소 · 더 성긴 격자) |
| **P1-4** 이완 기준 | 출력의 `(criteria: energy < … Ry, force < … Ry/Bohr)` 줄 · 머리의 `energy/force convergence thresh.` · `nstep` 이 계약 (1e-5 · 1e-3 · 200) 과 같음 · **마지막 힘 블록 (원자 수만큼 다 읽음) 의 모든 성분 ≤ 1e-3 Ry/Bohr** (벡터 크기 아님) | `out_problems` (relax) | 기준 1e-2 · 1e-1 · 머리 문턱 1e-4 · nstep 50 · 마지막 힘 성분 0.05 |
| **P1-5** 전자 수 | 유사포텐셜 가전자 수를 계획에 기록 (UPF v1 `Z valence` 줄 · v2 `z_valence` 속성) · 출력 전자 수 = Σ 조성 × 가전자 − 총전하 (입력에 `tot_charge = 0.0` 명시) · **결측 거부** · PP 마다 출력 Zval = 계획 | `pseudo_record` · `upf_zval` · `out_problems` | 595 · 줄 삭제 · S Zval 5 · 가전자 못 읽는 UPF |
| **P1-6** EOS 보류 대상 | EOS 필요면 `stage10` · `electronic_targets` **둘 다 null** · 이완 구조는 `relaxed` 에 진단 자료로만 (`relaxed_note`) | `read_relax` | 세 가족 |P| 2.5 GPa · 차 0.095 + |P| 1.9 |
| P2 저장만 하던 증거 | 앞 단계 판정을 **통째로 다시 내서** 저장된 판정과 대조 (`_norm_v` — 도구 경로만 빼고 sha 로) — 행 · 대표 · 순서 · 차 · G5 · 문장 · 출력 sha256 · k 점 수 · 다음 잡 · 기준 셀 · 발동 · 쌍 | `_rebind_sp` · `_rebind_kp` | 단일점 판정의 순서 · 문장 · G5 · 출력 sha 손댐 · 탐침 판정의 출력 sha 전부 0 · 이완 잡 목록 · 쌍 값 |
| P2 경로 기준 | 잡 · 구조 · 출력 · 안정성 · 전자구조 대상 = **계획 폴더 기준** {rel · sha256} · 판정 사이 고리 = 그 판정 파일 폴더 기준 · `rel_base` 를 적는다 | `stage10` · `read_relax` | 대상 경로가 계획 폴더 기준으로 실재 · sha256 일치 |
| P2 깨진 바이트 | utf-8 **strict** · 실패는 `decode_error` 로 기록 · 거부 (표시용으로만 대체 문자) | `parse_pw_out` | `1.0E-\xff08` |
| P2 CRLF | 모든 파일을 utf-8 · LF **바이트**로 쓴다 (`_write_bytes`) · 읽기도 바이트에서 | `_write_bytes` · `_load` · `parse_pw_in` | 도구가 쓴 파일 (계획 · 입력 · 판정 · 이완 구조) 에 CR 없음 |
| P2 GPU 확인 | 실행기 `_gpu_guard`: `MIN_FREE_MIB>0` 이거나 `GPU_EXCLUSIVE=1` 이면 nvidia-smi 없음 · 조회 실패 · 빈 값 · 숫자 아님 → **시작 안 함** · `GPU_EXCLUSIVE=1` 이면 compute 프로세스가 하나라도 있으면 시작 안 함. **보장 범위는 잡 시작 때뿐** — 도는 중에 올라오는 잡은 못 막는다 (공통 잠금 없음) → 카드에 운영 규칙으로 적었다 (9 단계 동안 gabia 에 다른 GPU 잡을 띄우지 않는다) | `run_force_check_scf.sh` | 실행기 selftest 20/20 (모의 nvidia-smi 9 경우 포함) |
| P2 거부 잡 재실행 | `reject --plan … --stage sp|kprobe|relax [--verdict …]` — 판독기 검사에 걸린 출력만 `scf.out.rejected.N` 으로 **옮긴다** (지우지 않는다 · 번호를 덮지 않는다 · 입력이 기록과 다른 잡은 손대지 않는다 · 판정 → 계획 고리가 이 계획이어야) → 실행기는 scf.out 이 없는 잡만 처음부터 다시 | `reject_outputs` · `_jobs_for_reject` | 걸린 출력 하나만 `.rejected.1` · 두 번째는 `.rejected.2` · 다른 계획의 판정 거부 |

그 밖에 고친 것: 이미 있는 잡 입력 · 이완 구조 파일은 같은 바이트일 때만 둔다 (다르면 멈춤 · 덮지 않는다).

## 2. 카드 문구 (개정 5 v2 · EF Q4 · Q5 · Q7)

- **판정 범위 (Q4)**: 이온 이완 판정 = '각 초기 가족에서 사전 규칙으로 선택한 대표 구조를 공통 기준 셀에서 이온 이완한 에너지 비교' — 이 수렴 설정 (forc 1e-3 Ry/Bohr ≈ 0.0257 eV/Å · etot 1e-5 Ry — 연속 이온 단계 사이 변화 기준이지 남은 최소화 오차의 상한이 아니다 · nstep 200) 과 고정 기준 셀에 **조건부**. 가족 전체의 DFT 최저 · 자유 셀 바닥상태가 아니다 · 0.10 eV 는 판정 여유이지 인증된 정확도가 아니다. 수렴 재확인은 이번 판에 넣지 않았다 (판정을 조건부로 둔 쪽). 도구 판정 파일의 `scope` 문장 · 금지 서술 셋 추가.
- **'UMA 기하 그대로' 는 단일점에만** (Q4) — 이완은 기준 셀로 옮겨 Cartesian 기하가 바뀐다.
- **EOS 다음 판 (Q5)**: 이번 판은 EOS 를 하지 않고 확실히 멈춘다. 설계할 때 이미 본 압력 · 에너지를 밝히고 새 단계 전에 규칙을 고정한다 · '결과 전에 정했다' 고 소급하지 않는다.
- **nowf (Q7)**: 중단 잡은 처음부터 · 후속 전자구조에서 파동함수가 필요하면 그 단계가 따로 만든다.

## 3. 시험

- **selftest 119/119** (v1 66) — 위 표의 반례 전부를 거부 이유 (메시지 문구) 까지 확인한다 · 양성 경로 (6 단일점 → 탐침 → 이완 → EOS 생략 → 10 단계 두 갈래 · 발동 경로 · 4×2×1 판) 는 v1 그대로 지나간다. 8 단계 결속은 selftest 에서 `_FakeRD` (`anneal_readout` · `verify_screen_verdict` · `load_records` 만 가짜 · `eos_robust` · `end_motif` · `_core` · `CONTRACT` 는 진짜 판 고정 판독기).
- **깨기 (변이) 73/73 빨강** (로컬 · `python3 tools/doping/b2o3_bo_dft_mutations.py` 로 재현 — 약 6 분 · CPU 1 코어 · `--selftest` 는 변이 대상이 도구에 정확히 한 번씩 있고 바꾼 소스가 문법상 맞는지만 몇 초에 본다) — 검사 한 줄씩 끄고 selftest 가 빨개지는지 (출력 검사 33 · k 격자 4 · 단계 출력 3 · 유사포텐셜 3 · 다시 결속 13 · 판정 사슬 8 · 10 단계 · EOS 보류 3 · 쓰기 · 덮지 않음 · 거부 6). 첫 판은 69/71 이었다 — '가중치 몫' (시험의 기대 문구가 넓어서 다른 거부 메시지에도 걸렸다) · '계약 같음' (계획에 저장된 계약을 손대는 시험이 없었다) 이 초록이었고 시험을 넣어 71/71 → 그 뒤 `!` 수 검사 둘을 더해 73 개. 깨진 검사가 나쁜 출력을 통과시키면 뒤 단계가 판정 파일을 써 버려 selftest 가 중간에 멈추는 경우 ('crash') 는 그 변이의 자기 시험에서 먼저 ✗ 가 난 것을 확인했다 (변이마다 처음 ✗ 난 시험 이름을 기록 · 변이 소스 73 개 모두 문법 오류 없음).
- **실제 QE 7.4.1 출력 5 개로 파서 · 검사 대조** (저장소 `db/raw`): nosym 출력 셋 (`ndo_site_eos_2026_10_16/MLi_04_x108` · `MP_07_x100` (relax 2×2×1) · `nd_q2_decomp_2026_10_23/run_kgy/host` (relax 3×3×2 · 10 점)) 은 k 격자 검사 통과 · `MLi_04_x108` 은 계약만 그 잡의 설정 (원자 수 58 · mv smearing · 그 PP 이름) 으로 바꾸면 **v2 검사 전부 통과** (전자 수 298 = Σ 조성 × Zval · Zval · BFGS 기준 · 머리 문턱 · nstep · 마지막 힘 성분 6.8e-4 · 응력 위치 · 부피 · 처음 좌표 · 셀) · 대칭 축소 출력 (`li2s_neb_cellconv_2026_10_09/c444/li2s/ep_initial` · 2 Sym. Ops) 은 k 격자 검사가 '−k 와 같은데 가중치가 둘 몫 (대칭 축소)' 으로 거부.
- **'한 출력 = 한 실행' 규칙을 저장소의 실제 PWSCF 출력 전부 (238 개) 에 걸어 봤다**: JOB DONE 이 있는 고정셀 단일 실행 **221 개 (scf 180 · relax 41) 모두 설정 줄 각 한 번 · JOB DONE 뒤 계산 기록 없음 · utf-8 정상** · SCF 177 개는 `!` 정확히 하나 (0 개 셋은 nscf 류 — 이 단계에 없다) · relax 41 개 모두 `!` 수 = BFGS 가 센 SCF 수 (JOB DONE 뒤는 '=---=' 줄과 `Warning: ieee_… is signaling` 뿐) · vc-relax 11 개는 최종 scf 가 설정 줄을 한 번 더 찍어 '한 번씩' 검사에 걸린다 (이 단계는 vc-relax 를 쓰지 않는다 — 걸리는 게 맞다) · JOB DONE 없는 6 개는 미완료.

## 4. gabia 검사 (v2 · GPU 안 씀)

(사용자 실행 뒤 채운다 — worktree · 도구 · 실행기 sha256 · selftest · 실행기 selftest · 새 검사 폴더 prepare (8 단계 실제 데이터 결속 · 입력 6 · nosym · tot_charge · 가전자 기록) · 입력 지문 · 깨기 숫자 · 커밋)

## 5. 일부러 안 한 것

- EOS 절차 — 생략 불가면 멈춘다 (안정성 · 전자구조 대상 null).
- 수렴 재확인 (더 엄한 문턱으로 다시 이완) — 판정을 이 설정에 조건부로 두는 쪽을 골랐다.
- GPU 공통 잠금 — 시작 때 확인 + 운영 규칙. UMA 실행기와 잠금을 나누는 공사는 이 단계 밖이다.
- 재시작 이어 붙이기 지원 — 거부만 한다 (실행기 덮어쓰기 · nowf).
- 이완 뒤 골격 판정 — B · P 배위 · O 끝 꼴은 기록만 (카드 G7).

## 6. 질문

- **Q1** EF 의 반례 (P1-1 … P1-6 · P2 6) 가 v2 에서 막히나 — 가능하면 EF 때의 재현 자료로 다시 돌려 보고.
- **Q2** '한 출력 = 한 실행' (설정 줄 각 한 번 · JOB DONE 뒤 계산 기록 없음) 에 남은 구멍이 있나 — 특히 JOB DONE **앞에** 끼워 넣은 조각 · 둘째 실행의 일부만 남은 파일.
- **Q3** k 격자 대조가 QE 7.4.1 nosym 출력과 맞나 — noinv 꼴 (안 줄인) 목록도 통과시키는 것 · 가중치 합 2 (nspin 1) 가정 · 축 · k 좌표 출력 자릿수 (F11.6 · F12.7) 로 1e-4 허용이 충분한지.
- **Q4** DY 확인 4 (EOS 의 (E, P, V) 결과 파일 결속) 를 이제 해제할 수 있나.
- **Q5** 판정 범위 문장 · EOS 다음 판 원칙 · GPU 보장 범위 문구가 EF Q4 · Q5 · P2-5 의 뜻에 맞나.
- **Q6** `reject` 절차로 P2-6 이 닫히나.
- **Q7** DFT 진입 전에 더 닫을 것이 있나 — 없으면 사용자 비준만 남는가.

## 7. 회신 형식

GO / 조건부 GO / NO-GO 한 줄 → P0–P3 (파일:줄 · 재현 · 최소 수정) → Q1–Q7 → DFT 진입 전 마지막 확인 목록.
