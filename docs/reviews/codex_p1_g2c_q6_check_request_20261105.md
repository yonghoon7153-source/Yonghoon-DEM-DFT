# Codex 짧은 확인 요청 — P1 G2c′ 결과 전 예측 다 · 라 · 바 ↔ LIGGGHTS-PUBLIC 3d5c00f 소스 (2026-11-05 · 11-06 다시 씀)

> **리뷰 핀** = 이 요청서를 담은 커밋 · 대상 = `docs/reviews/p1_g2c_compare_definition_20261105.md` §2 · §4 (예측 다 · 라 · 바) · 샌드박스 덱 `docs/reviews/p1_g2c_sandbox_20261104/head.inc` · `docs/reviews/p1_g2c_sandbox_20261104/mat.inc` · `docs/reviews/p1_g2c_sandbox_20261104/R.liggghts` · `docs/reviews/p1_g2c_sandbox_20261104/A2.liggghts` · 소스 = LIGGGHTS-PUBLIC 3d5c00f20519e6bb6eb6756f51f1ad36564e649d (공개 · 아래 줄 번호 = 그 소스의 src/ 아래 파일 · 리포 밖).
> **까닭** — 1저자 11-05 메모 Q6 *"권고대로"* = 샌드박스 전에 짧게 확인 · 틀리면 결과 전에 예측을 고친다.  결과 0 건.  보낼 곳 = Codex 실무 창 (1저자 11-06 전달).
> **11-06 메모** — 11-05 판은 push 전 기계 교체로 사라져 같은 내용으로 다시 썼다 (진행 기록 11-06).

## 0. 이번에 닫는 것 / 닫지 않는 것
- 닫는 것: 예측 다 · 라 · 바 의 소스 근거 (서면 그대로 실행 · 안 서면 줄 · 조건 → 결과 전 날짜 붙인 개정).
- 닫지 않는 것: G2c′ 정의 승인 · P1 수치 인증 · 허용폭 · 복원 판정 · RJ 323957 · MPI · 키트 적용 · 실행 결과 (0 건).

## 1. 우리 소스 읽기 (관찰 · 시험 전)
| # | 소스 줄 (3d5c00f src/) | 읽은 것 |
|---|---|---|
| s1 | pair_gran.cpp 665–667 · 701–702 | setup 이면 shearupdate_ 0 · compute pair/gran/local = computeflag_ 0 · shearupdate_ 0 → 덤프 열은 그 시점 상태로 다시 계산 · 이력 안 바꿈 |
| s2 | tangential_model_history.h 143 · 149–157 · 175–210 · 215 | 이력 갱신 = computeflag ∧ shearupdate 일 때만 · Ft = −kt·shear · 고착 = −γt·vtr 더함 · 미끄럼 = 비율 축소 · 감쇠 없음 |
| s3 | normal_model_hooke_hysteresis.h 156–157 · 165 · 177 · 192 · 120–146 | deltaMax 올림 = 조건 없음 · 응집 갈래 newDeltaMax = 갱신 때만 · kn · kt · γ = 이력 무관 |
| s4 | write_restart.cpp 171 · 178 · 185 | 명령 = lmp->init · setup_pre_exchange · pbc · exchange · borders 뒤 씀 (주기 restart 경로엔 setup_pre_exchange 없음 = 노트 `docs/reviews/p1_g2c_source_check_20261104.md` §2) |
| s5 | 덱 `atom_modify map array sort 0 0` · 직렬 | 원자 정렬 없음 → 다시 읽은 순서 = 쓴 순서 (추정) |

## 2. 질문
- **Q6-1 (다)** BW = `read_restart F` (A 의 주기 restart) → `run 0` (D1) → `write_restart F′` · BR = `read_restart F′` → `run 0` (D2) · `%.17g` → D1 = D2 비트 (쌍 30 열 · 원자 12 열 · 쌍 집합) 인가 · 깨는 경로 (lmp->init · 이웃 목록 · 합산 순서 · 이력 짝 목록 순서 · 바닥 벽 `fix wall/gran` 이력 · 이미지 플래그 등) 는 줄 번호로.
- **Q6-2 (라)** A2 의 `write_restart` 명령 파일로 같은 왕복 (CW → F′ → CR) · CW 덤프 = 11-04 C 덤프와 바이트 같음 (같은 실행 파일).
- **Q6-3 (바)** B · C 두 setup 덤프 (같은 x · v · ω · deltaMax) 의 양쪽 고착 쌍: Δforce = Δforce_tangential = −kt·Δshear (세 성분 · 끝자리 안) · force_normal 차이 = 그 사영 (compute_pair_gran_local.cpp 481–489) · 미끄럼 쌍 = 식 밖 · `rolling_friction cdt` 가 덤프 힘 열에 들어가는 경로.
- **Q6-4** 빠진 것 (setup 의 다른 이력 변경 · 떨어진 쌍 지움 · 새 쌍 · 고스트 쌍) 이 예측을 바꾸면.

## 3. 답 꼴
- 질문마다 맞음 / 틀림 / 조건부 + 소스 줄 · 틀리면 고칠 예측 문장 · 샌드박스를 돌렸다면 따로 적음.
