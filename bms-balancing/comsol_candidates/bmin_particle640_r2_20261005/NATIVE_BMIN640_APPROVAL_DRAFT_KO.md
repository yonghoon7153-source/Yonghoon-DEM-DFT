# 비활성 native B-min640 승인 초안 (r2) — 실행 명령으로 사용 금지

approved=false / usable=false. 이 문서는 사용자 승인도, 실제 approval / release / USER_DECISION 파일도 아니다. 변경부 기능 검증 (`VALIDATION_REQUEST_KO.md`)
과 그 수용은 아직 없다. 순서는 B-min v2 §8 그대로 — 후보 제출 · 검토 → 변경부 검증 별도 승인 · 수행 · 수용 → **그 뒤에** 이 초안의 별도 승인 → 실행 →
결과 수신 검토.

고정 식별: run_id `bmin_particle640_candidate_001` · 실행 기계의 root
`C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/bmin_particle640_offline_preparation_20261004/` (이 저장소의
`comsol_candidates/bmin_particle640_r2_20261005/candidate/` 내용을 그 root 에 그대로 둔다 — v1 · r1 꾸러미가 아니다) · manifest SHA
`4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25`.

## 추후 사용자에게 요청할 한 건

**정책 무변경 · 같은 provisional 모델 · fresh t = 0 → 150 s · 입자 반경 메시 Nel 320 → 640 (두 전극) 한정 공간 민감도 최대 1 회.** 물리 300 (120 / 60 / 120) ·
0.1C 정전류 충전 · σ 1e−20 · threshold 0 · 기존 초기화 / 물성 / OCP / guard / 시간 cap / rtol 1e−6 / 초기 step 1e−5 / strict / all stored 그대로 · 요청 1,637
시각 (NORMAL480 목록의 앞 1,637 개). compile ≤ 1 · batch ≤ 1 · solve ≤ 1 · 추가 control 0 · 자동 재시도 0 · 자동 연장 0. 저장 MPH 에서 이어 풀지 않는다.

기준은 NORMAL480 의 `run/tables` 9 파일 (`BASELINE_IDENTITIES.json`) — 실행 기계의 결속 경로에 그 크기 · SHA-256 그대로 있어야 하고, 하나라도 다르면
compile 전에 멈춘다 (entry `BASELINE_IDENTITY`).

일반 사용자 Windows PowerShell 5.1 NoProfile 전경 · 고정 Python 에서 새 두 challenge 를 사용자가 직접 입력한다. AI 대리 입력 · 별도 C2 check-only 없음.
명령 argv / cwd 는 `candidate/COMMAND_MAP.json` 에 정확한 배열로 고정했고 지금은 사용할 수 없다 (`currently_usable` false). cwd 는 기존
`outputs/b020_profile_unit_stages_20260927/src`. 전달 ZIP 의 사본에서 실행하지 않는다.

요청 16 코어 · 시작 디스크 ≥ 15 GiB · RAM 은 관측만. 예산 제안 (`RESOURCE_BUDGET_KO.md`): 사전 / 입력 180 · compile + batch 공유 9,000 · 소유 정리 합계 120 ·
분석 900 · 로컬 전달 300 · 부모 전체 10,500 초. 실제 150 s 비용 · peak RAM 은 모른다. 시간 초과 · 정책 / 식별 불일치 · 경로 충돌 · 첫 오류는 보존하고
멈춘다. 다른 프로세스 종료 · 자동 재시도 · 다른 shell / 권한 / 정책 fallback · 미사용 예산 전용은 없다.

## 필수 선행

변경부 수용에 결속된 새 검증 release (`VALIDATION_RELEASE.json` — `changed_branch_validation` PASS · `manifest_bytes_unchanged_since_validation` true) ·
현재 source / prefs 식별 · security 값 · 실행 경로 확인 · NORMAL480 기준 9 파일의 실제 경로 · 바이트 관측 · 이 후보와 위험 / 횟수 / 예산에 대한
사용자 별도 명시 승인. 현재 prefs 값을 미래 승인값으로 추정해 적지 않았다. `NATIVE_APPROVAL_FIELD_SPEC.json` 의 필드 (`native_bmin640_one_shot` 등) 에
결속한 실제 파일은 그때만 허용된 run 밖 경로에 만든다. 봉인 `CODE_MANIFEST` / `CONTRACT` 의 false 플래그는 고치지 않는다.

예정 경로 (root 아래): `future_run_001` · `future_parent_001` · `future_authorizations/{bmin640_001.json, VALIDATION_RELEASE.json, USER_DECISION.json}` —
지금 모두 없고, 충돌하면 삭제 / 재사용 / 새 이름으로 우회하지 않는다.

## 결과의 세 필드 (결과를 보기 전에 고정 — B-min v2 §6 · SPEC §44-2)

| 필드 | 값 |
|---|---|
| `native_completion` | `NORMAL_150S_COMPLETED` (정확히 150 s 저장 · native 정상 종료 · 자식 rc 0 · 보호 중단 없음) · `PROTECTIVE_STOP` · `NOT_ESTABLISHED` (원인 함께) |
| `evidence_validity` | I-1 기준 바이트 · I-2 설정 read-back (NORMAL480 과 `study_tlist` 접두 외 차이 0) · I-3 메시 read-back (120 / 60 / 120 · Nel 640 / 640 · 단일 Time-Dependent Solver 구간 안의 DOF 줄 정확히 하나 — 그 줄 전체가 (앞뒤 공백 허용) 한 DOF 문장이어야 하고 solved > 0 · 예상 156,925+12 와 다른 유효값은 기록만) · I-4 · I-5 guard / 범위 / 유한 / 단위 · I-6 Li · 전압 항등식 · 초기 Li · I-7a/b/c 요청 1,637 · 주 비교 301 · 좌표 · I-8 예산 — 모두 성립하면 `VALID` |
| `mesh_comparison` | 한도와 같으면 허용한다 (≤). 모든 유효 조건이 성립할 때 max \|ΔV\| ≤ 0.001 V **그리고** 두 전극 max \|Δx_surface\| ≤ 1e−4 이면 `WITHIN_LIMITS_THIS_WINDOW`, 어느 하나라도 **엄격히 크면** `EXCEEDS_LIMITS` 다. 앞 두 필드 중 하나라도 성립하지 않으면 `INCONCLUSIVE` |

최종 값은 부모의 POST_WRITE 콘솔 줄 (`USER_PARENT_FINAL_RETURN` 의 `fields`) 이다. r1 (BMIN-N1 — r2 에서 바뀌지 않음): `native_completion` 은 부모가 스스로 확인한
native 축 (`GNativeAxis` — 자식 반환 · run / manifest 결속 · 종료 증거 · consumer 라벨 일치) 이고, 비교 · 증거 · 분석 · 전달이 실패해도 그대로 남는다.
부모가 받아들인 정상 결과만 consumer 의 비교 판정을 싣고, 그 밖은 `evidence_validity` INVALID · `mesh_comparison` `INCONCLUSIVE` 다. 부모 성공 상태는 `AWAITING_BMIN640_150S_EXTERNAL_ACCEPTANCE` — 외부 결과 수신 검토 전이다. 원래 overall / normal gate INCOMPLETE ·
실효 정책 UNVERIFIED 를 보존한다. NoExit 의 OS rc = null · 사용자 프롬프트 복귀는 OS 종료코드가 아니다. rc 0 이나 ZIP 만으로 비교 PASS 가 되지 않고,
유효한 비교의 한도 초과를 solver 실패로 바꾸지 않는다.

`WITHIN_LIMITS_THIS_WINDOW` 가 뜻하는 것은 "이 입력 · 입자 축 · 120–150 s · 선언 표본에서 320 ↔ 640 두 설정 간 관측 차이가 비교 한도 안" 까지다 — 오차
상한 · 수렴 차수 · 참값 정확도 · 물리 축 · 480 s 후반 · 유한 σ 를 주장하지 않는다.

이 초안은 다른 공간 축 (물리 메시) · 창 밖 구간의 새 독립 수용 · 480 s 전체 · 960 s · 유한 σ · 장기 운전 · 초기 공간 시험 / rtol30 / 0–480 s 분석의 재판정을
포함하지 않는다.
