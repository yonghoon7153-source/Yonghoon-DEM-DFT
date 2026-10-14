# Codex 짧은 검토 요청 — LHS 214 생산 실행의 망 단계 실패 14 건 · 분류 수정 (가) 설계 (2026-10-14 · 구현 전)

> **리뷰 핀** = 발사 핀 `1087a9b2f4a93aa6a3b0debc698a14fffa13488d` (코드 · 등록 · 실행기 · 영수증 도구 = Codex SUPR 재확인 핀 `df647d4e3` 과 `scripts/` · `webapp/` diff 0) · 실행 결과 기록 커밋 = `268961055` (진행 기록 10-14 오후 · push 뒤).
> 이 요청은 **구현 전 설계 검토**다 — 코드 · 원장 · 등록은 아직 바꾸지 않았다.  1저자 10-14 = 아래 (가) 로 고치자 (비준) · 고치기 전에 Codex 의 판단을 먼저 받는다.

## 1. 사실 (1저자 WSL · 핀 `1087a9b2f` · 사전 점검 = 등록대로 전부 통과 · 194 등록 §2 여섯 칸 손 대조 같음)

| 묶음 | 결과 | 감사 · 다시 읽기 |
|---|---|---|
| production194 (`~/net194_1087a9b2f` · 0.476 h · 최대 동시 16) | done **186** · failed **8** = lhsx_051 · 053 · 054 · 060 · 061 · 062 · 063 · 064 | audit rc 0 (SEALED 194 · merged 194 · 레코드 g2 186 · import 관측 시작 970 = 끝맺음 970 · 완료 시도 186) · reread `--expect-set production194` rc 1 (M2 lhsx 전 케이스 done · partial ✗ · M3 읽은 고유 186 ≠ 194 ✗ — 실패 8 건만) |
| supp20 (`~/netsupp20_1087a9b2f` · 0.084 h) | done **14** · failed **6** = lhss_001 · 003 · 008 · 009 · 011 · 014 | audit rc 0 (SEALED 20 · 관측 100 = 100 · 완료 시도 14) · reread `--expect-set supp20` rc 1 · 사후 영수증 (`--manifest` · `--primary-manifest` · `--approved-sha`) rc 0 (39 칸 · 다름 0) |

- 실패 14 건 모두: 단계 "Network Solver (both modes)" · rc 1 · 신호 없음 · 최대 RSS 0.88–1.94 GB (메모리 아님) · attempt 1.
- `network_attempt.json` (8 건 확인 · 같은 글자): `failure_kind solver` · reason = *"★ 내용 검증 실패 (게시 전 차단): physics.ionic=fail (관통 성분은 있는데 σ_ion 을 풀지 못했다 (solve_failed) — 미퍼콜이 아니다 · 수치 실패 = 게시 차단 (WEB-03 Q1 — 일반 · 정지 경로 모두))"* · `previous_generation_kept false` · `active_status none`.
- lhsx_054 솔버 단독 재실행 (새 임시 폴더 · `network_conductivity.py atoms.csv contacts.csv -t 1:AM_P,2:SE -s 1000 --contact-mode both`): rc 0 · CG (rtol 1e-10) · spsolve 정상 끝 · physics JSON `ionic_status failed` · `ionic_status_reason` = 위 문구 · `constriction_power_share_ion_physics_status 'not_computed (FULL solve failed on a percolating network)'` · physics 전자 · 열 = computed · hertz 이온 = 화면 "Bruggeman EMT overestimation 1.18×" (σ_ratio ≈ 0.66 [화면 판독]).
- 코드 (핀): `scripts/network_conductivity.py:212` `SOLVE_FAILED_REASON` 한 이름이 (예외 · V_source ≤ 0 · Σg 상한 · σ_ratio > 1.5 · 경계 겹침 퇴화) 를 묶는다 · `:1226–1250` FULL 단상 σ_ratio > 1.5 = None (C1-5 — CF · 협착-only 의 q > 1.5 는 값 유지 + `model_over_conduction`).
- 같은 배치의 통과 침대 Physics σ_ratio = 1.04–1.48 (τ `MODEL_BELOW_CONTINUUM_BOUND`) — SE 많은 lhsx · lhss 에 몰림.
- **유력 원인 [확인 전 — 하위 사유가 한 이름이라 분리 기록이 없다]** = Physics FULL q > 1.5 가드가 `solve_failed` 로 표지 → WEB-03 Q1 이 Hertz 포함 레코드 전체를 막음.

## 2. (가) 설계 (1저자 비준 10-14 · 구현 전)

1. `solve_failed` 하위 사유를 갈라 기록 — FULL q > 1.5 = 새 사유 (예 `full_over_conduction`) · 상태 not_computed · 값 미게시 · 진단 q 값만 기록 / 나머지 (예외 · V_source ≤ 0 · Σg 상한 · 경계 겹침 · 증서 실패) 도 이름 분리.
2. 게시 · 정지 계약 · τ · 다시 읽기 · 인계 · 배포 관문: `full_over_conduction` = 등록된 **모형 한계** → 그 모드 채널만 NOT_COMPUTED(사유) · 레코드 게시 · τ 상태 표지.  **진짜 수치 실패는 그대로 게시 차단** (WEB-03 Q1 뜻 유지).
3. 웹앱 같은 묶음 (케이스 페이지 τ 블록 · 상태 문구).
4. 시험 먼저 — 합성 망 FULL q > 1.5 (지금 = 차단 확인 → 고친 뒤 = 채널 NOT_COMPUTED · 레코드 게시) · 다른 solve_failed 경로 = 계속 차단 · 영향 없는 침대 = 비트 동일.
5. 봉인 32 바뀜 → 새 code_fp → 두 등록 §3 재봉인 · 10-14 실행 = 역사 (지우지 않음) · 새 ROOT 둘로 **214 전부 다시** (혼합 봉인 금지 · ≈ 40 분) · 사전 점검 · 손 대조 · 발사 승인 다시.

## 3. 질문

| Q | 질문 | 우리 제안 |
|---|---|---|
| Q1 | (가) 가 WEB-03 Q1 (관통 풀이 실패 = 게시 차단) · C1-5 (FULL q > 1.5 거부) 의 뜻과 맞나 — 아니면 FULL q > 1.5 는 차단으로 남아야 하나 | 맞다 — 값은 계속 거부 (C1-5 유지) · 바뀌는 것은 사유 이름과 "레코드 전체 차단 여부" 뿐 |
| Q2 | 범위 — Physics 만 / 모드 공통 (Hertz FULL q > 1.5 도 채널 NOT_COMPUTED · 레코드 게시) | 모드 공통 분류 · 단 Hertz (주 값) 가 이 사유면 배포 관문이 그 침대를 어떻게 다룰지 = Codex 의견 (이번 214 에는 없음) |
| Q3 | v1.3 — 14 침대의 Physics = NOT_COMPUTED(full_over_conduction) 로 배포 가능한가 (Physics = opt-in 부록 · 주 값 Hertz) | 가능 — 등록 집합 그대로 · 상태 열 필수 |
| Q4 | 다시 발사의 최소 증거 | 위 §2-4 시험 + fast16 · real4 · 두 영수증 · 손 대조 · 214 전부 다시 (부분 retry 아님) |
| Q5 | 214 결과 묶음 (감사 · 다시 읽기 · 영수증) 에서 그 밖에 보이는 문제 | — |

결과 묶음 (화면 · `network_attempt.json` · 단독 재실행 화면) 은 1저자가 함께 붙인다.
