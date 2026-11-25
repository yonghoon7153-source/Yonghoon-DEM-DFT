---
title: "DX 프롬프트 — 셀구축 v1.2 · b2o3 B·O 배치 카드 개정 1 v1.2: DW 고침 확인 (단계 결속 · 파일럿 시간축 · 비유한 기하 · EOS 기준 순서 · 관측창 문구) · 1 단계 GO 여부 (계산 0 건)"
date: 2026-11-09
updated: 2026-11-09
tags: [review, b2o3, cell-construction, uma, readout, pilot, eos, codex, prompt, letter]
letter: DX
track: b2o3
channel: codex
kind: prompt
status: 발송 2026-11-09 (사용자) → 회신 수령 NO-GO (P1 1 · P2 2 — codex_DX_reply_cell_construction_v1_2_release_2026_11_09.md) · 기준 커밋 93937466 (브랜치 claude/evac-2026-11-08 · 그 뒤 fbdf3e8d 는 이 프롬프트 · 8ef8d029 는 93937466 에 섞인 kgy 정리 기록 오독 줄 되돌림 — 둘 다 b2o3 도구 · 카드 변경 없음) · 앞 편지 DW (NO-GO)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = b2o3 UMA-MD / B₂O₃ 계산 쪽 (1저자 = 사용자). ⛔ b2o3 전도도 (D · Ea · σ) 값은 싣지 않는다 (08-25 마감 · 인용 불가).
> ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_DX_reply_cell_construction_v1_2_release_2026_11_09.md` 로 원문 보존.
> ⚠ 사용자의 조건부 비준 (*'go면 비준이야'*) 은 DW 회신에 걸려 있었고 DW 가 NO-GO 라 쓰이지 않았다 — DX 회신 뒤 사용자에게 **다시 묻는다** (자동 비준 아님).

---

**[b2o3 · 셀구축 v1.2] DW 고침 확인 — 1 단계 (UMA) GO 여부 (계산 0 건)**

## 0. 무엇을 묻나

DW 회신 (`kb/reviews/codex_DW_reply_cell_construction_v1_1_release_2026_11_09.md` · 기준 837cc6e8) 은 NO-GO 였다 — DV 묶음 ①–③ 닫힘 · ④ 판독기가 단계 사이의 입력 · 선택 · 시간을 대조하지 않음 (P1-1 단계 결속 · P1-2 파일럿 시간축 · P1-3 EOS 기준 순서 [DFT 전 조건] · P2 NaN 좌표 → F_free · P3 관측창 /3 근사). 1 단계 전 확인 목록 넷 (단계 연결 · 파일럿 시간축 대조 · 반례 + 양성 시험 · 사용자 비준).

브랜치 `claude/evac-2026-11-08` · b2o3 변경은 **커밋 93937466 하나** (`837cc6e8..93937466` 의 나머지는 litdb · kgy 디스크 기록 · 웹앱 개념 카드 · DW 원문 보존 — b2o3 도구 · 카드와 무관). 생산 UMA · DFT · MD 는 안 돌았다.

**묻는 것**: DW P1-1 · P1-2 · P2 가 닫혔나 → 1 단계 (생성 → UMA 이완 거름 → 연속 파일럿 → 어닐 → 판독) 를 사용자 비준 뒤 시작해도 되나 (GO / 조건부 GO / NO-GO). P1-3 (EOS) · P3 (관측창 문구) 도 닫혔나.

## 1. 항목별 고침 (DW → 어디)

| DW | 고침 | 시험 |
|---|---|---|
| P1-1 단계 결속 | `tools/doping/b2o3_bo_readout.py` 를 **단계 사슬**로 다시 짰다 — `screen` (생성 manifest + 이완만 결과 → 거름 판정 JSON) → `extract` (판정 + 파일럿 런 기록 → 스냅숏 출처 JSON) → `pilot` (출처 + 스냅숏 이완 → 영수증 JSON) → `anneal` (판정 + 영수증 + 어닐 결과). 각 단계는 앞 단계 파일을 **sha256 으로 묶고, 묶인 입력에서 앞 판정 · 영수증을 다시 내서 파일과 같은지** 본다 (손으로 줄인 합집합 · 바꾼 t_a 는 거부). 기록마다 정체성 필수 · `identity_sha` = `identity_sha(identity)` · **시작 파일 sha256** (6 단계 = manifest 의 O 꼴 파일 · 7 단계 런 = 파일럿 구조의 6 단계 post_relax · 스냅숏 이완 = 스냅숏 · 8 단계 = 계획 항목의 6 단계 post_relax) · 단계 · 카드 설정 (모델 · fmax 0.05 · 셀 이완 · 1500 걸음 · dt 2 · 마찰 0.01 · 500 K · 시간 = 파일럿 100 / 8 단계 t_a) 대조 · 계획 밖 기록 · 같은 이름 둘 = 거부. **누락 ≠ 실패**: 거름 누락 → '거름 미완료' (합집합 · 파일럿 없음) · 8 단계 누락 → 판독 거부 · 실패는 G1 분모에 남김 · 6 단계에서 실패한 계획 항목 = 시작 없음 → 돌리지 않고 실패로 셈. k_f 미달 → '거름 보류' [제안 · DW Q2]. `screen --plan_dir` 가 실행기 (`run_uma_kgy.sh CAND`) 용 시작 파일 manifest (pilot · anneal) 를 쓴다 (실행기 해시 단계가 받는 것 확인) | 판독기 selftest **57/57** — 음성: 6 원자급 남의 결과 (시작 sha ≠ manifest) · identity 없음 · identity_sha 불일치 · fmax 0.02 · 계획 밖 기록 · 부분 거름 (누락 21 → 미완료) · k_f 미달 (보류) · 판정 합집합 손 축소 · 어닐 20 ps (t_a 100) · 1000 K · 계획 하나 누락 · 계획 밖 기록 · 생성 CIF 에서 시작 · 다른 판정의 영수증 · 손으로 바꾼 판정 / 영수증 (t_a 100 → 20). 양성: 완결 거름 → 계획 15 (합집합 5) · 실행기 manifest sha · 끝까지 승자 F_B · 실패 기록은 G1 분모 (거부 아님) · 시작 없는 항목 실패로 셈 |
| P1-2 파일럿 시간축 | `tools/doping/run_anneal.py` — 결과 기록 `outputs.md_traj` (상대경로 · sha256 · 저장 간격 · 걸음 · 프레임 수) · `verify_outputs` 가 궤적까지 (sha256 · 프레임 수 = 걸음 // 간격 + 1 · dt = 정체성 dt · 걸음 = 시간 / dt · 프레임마다 원자 수 · 조성 · 기하). 판독기 `extract` 는 **dt · 저장 간격을 명령줄로 받지 않는다** — 런 기록에서만 · 런 = 파일럿 구조 하나 · 시작 sha · 100 ps · 500 K. `pilot` 은 궤적 sha256 (기록 = 출처) → 프레임 번호 (시각 ÷ 간격 · 정수) → 스냅숏 좌표 (궤적 프레임과 1e-6 Å) → 이완 입력 sha256 을 다시 대조 | run_anneal selftest ⑨ (기록 · 간격 변조 · 궤적 변조) · 판독기 음성: 출처 궤적 sha 0 · 프레임 번호 50 → 49 · 저장 간격 500 → 250 · 스냅숏 좌표 교체 (sha 맞춤) · 20 ps 런 · 1000 K · 다른 시작 · md_traj 없음 · 기록 간격 500 → 50 (프레임 수 불일치). 양성: 같은 시각을 기록 간격 250 이면 프레임 40 · 100 · 200 (DW wrong_cadence 의 거울) |
| P1-3 EOS 기준 순서 | `eos_robust` — 보정 전 (기준) 전체 순서 · 0.10 판정을 먼저 내고 2³ 독립 B 조합 **모두가 그대로 지킬 때만** 생략 | Codex 두 반례 (모두 F_P 로 뒤집힘 · 아래 순위 바뀜) → 생략 불가 · 기존 공통 B / 독립 B · 압력 > 2 GPa 시험 유지 |
| P2 비유한 기하 | `run_anneal.geometry_problems` (유한 좌표 · 셀 · 세 방향 주기면 부피 ≠ 0) 를 `verify_outputs` 가 결과 · 궤적 프레임에 적용 · 판독기 `end_motif` 는 기하가 무효면 `invalid` | NaN 좌표 (sha 맞춤) → 실패로 셈 (F_free 아님) · 특이 셀 · end_motif 직접 |
| P3 관측창 | `D-2026-11-09-md-observation-window-amend1` (proposed) 문구: Ea₉₅ = kT·ln(ν₀·t·n / (−ln 0.05)) · /3 은 ≈ 근사로 병기 (1000 K · 0.8 ns 에서 0.00012 eV 낮음) · 예시 값 그대로 | — |

**깨기 (시험이 헛것을 재지 않는지)**: 검사 13 개를 하나씩 끄고 selftest 를 돌려 전부 빨간불을 확인했다 — 정체성 없음 통과 1 · 시작 sha 대조 4 · 설정 1 · 시간 · 온도 4 · 누락 = 미완료 1 · k_f 보류 1 · 판정 다시 내기 2 · 영수증 다시 내기 1 · 프레임 좌표 1 · md_traj 요구 1 · EOS 기준 3 · 기하 2 · 영수증–판정 짝 1. 음성 시험은 **거부 이유 문자열까지** 본다 (다른 데서 멈춘 것을 통과로 세지 않음 · 예외로 터지면 빨간불).

## 2. 판독 계약 (카드 v1.2 · 결과 전)

카드 `db/properties/b2o3_bo_placement_estimand_2026_11_09.json` `개정_1_셀구축_v1_2026_11_09.판독_계약` — DV 계약 그대로 + 새 칸: `단계_결속` · `시작_파일` · `누락_실패` · `k_f_미달` [제안] · `단계_설정` · `파일럿` (⏩ DW P1-2) · `EOS_생략` (기준 순서) · `성공` (기하 유효). `기계_판독_값` 에 `k_f_shortfall` hold · model · relax_fmax · cell_relax · relax_steps · dt_fs · friction · anneal_T_K 를 더했고 selftest 가 도구 CONTRACT 와 대조한다. 절차 `db/properties/cell_construction_protocol_v1_2026_11_09.json` 은 v1.2 · `DW_대응표_2026_11_09` · 6 · 7 · 9 단계에 ⏩ 칸.

## 3. 일부러 안 한 것 (판단 요청)

- 8 단계 seed 는 대조하지 않는다 (실행기 기본 seed + 이름 crc32 — 재현 필요조건일 뿐).
- 파일럿 저장 간격을 카드 값 500 걸음으로 강제하지 않는다 — 기록 간격으로 프레임을 고르고, 시각이 정확히 떨어지지 않으면 멈춘다.
- 8 단계는 파일럿 런과 다른 새 출력 폴더에서 계획 전체를 t_a 로 돌린다 — t_a = 100 이어도 파일럿 런 결과를 8 단계 기록으로 재사용하지 않는다.
- EOS 입력 (가족별 E · P · V) 의 결과 파일 결속은 DFT 단계 앞에 붙인다 (DW 가 DFT 전 조건으로 둔 것).
- 생성기 `verify_manifest` 자체는 판독기 selftest 에서 막아 두고 (생성기 selftest 40/40 몫) 판독기 결속만 시험했다.

## 4. 질문

- **Q1** DW P1-1 · P1-2 · P2 가 닫혔나 — DW 의 같은 반례 (`probe_dw.py`: 남의 결과 · identity 제거 · 20 ps · 1000 K · 합집합 축소 · 부분 거름 · 궤적 sha / 프레임 변조 · 틀린 간격 · NaN) 를 새 CLI (`screen` → `extract` → `pilot` → `anneal`) 로.
- **Q2** 단계 사슬에 아직 묶이지 않은 손잡이가 있나 (예: 판정 · 영수증을 다시 내는 비교의 몸통 · 상대경로 해석 · 실행기 manifest 와 실제 `--xyz` 사이)?
- **Q3** k_f 미달 = 보류 · 6 단계 실패 계획 항목 = 시작 없음 → 실패로 셈 · 위 §3 의 선택이 결과 전 규칙으로 괜찮나?
- **Q4** P1-3 · P3 가 닫혔나?

## 5. 회신 형식

GO / 조건부 GO / NO-GO 한 줄 → P0–P3 (파일:줄 · 재현 · 최소 수정) → Q1–Q4 → 1 단계 시작 전 마지막 확인 목록.
