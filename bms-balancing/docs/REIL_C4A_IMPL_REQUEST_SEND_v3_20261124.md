# Codex 발송 프롬프트 — REIL C4-A 구현 요청서 v3 재검토 · 2026-11-24 KST

> v2 재검토 회신 (2026-11-08 · 원장 §130 · REVISION_REQUIRED_BEFORE_IMPLEMENTATION_AND_TEST_APPROVAL · 남은 N1 · N3 · N4 · N6 + 비차단 C2) 을 반영해 구현 요청서 v3 를 썼다
> (문서만 · 실행 0). v1 · v2 는 그대로 두었다. 아래 `---` 사이가 붙여 넣을 본문이다. 검토자가 저장소를 읽을 수 없으면 본문의 표에 있는 파일을 첨부한다.

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL **C4-A 구현 요청서 v3** 의 재검토를 부탁드립니다. 2026-11-08 의 v2 재검토 (고정 기준 pin `fa502acb68f6d103a880d9431bb2e3f1c4013588`) 가 남긴 네 묶음 N1 · N3 · N4 · N6 의
subissue 열둘과 비차단 C2 를 §0 대응표로 하나씩 답했습니다. 문서 범위에서 종결된 N2 · N5 · N7 · C1 은 v2 그대로입니다. 요청서 v1 · v2 와 검토 근거는 바꾸지 않았습니다.

- 브랜치 `claude/14-gate-code-review-9qkx05` · 기준 pin `fa502acb` (재검토의 고정 기준 — 원격 HEAD 라는 주장이 아님) · v3 · 이 발송문 · 원장 §131 이 든 커밋: `<발송 때 적는다>`.
- 인용한 `scripts/` · `tests/` 의 행 번호는 pin 의 바이트입니다 (작성 때 pin ↔ HEAD · 작업 트리의 `bms-balancing/scripts` · `bms-balancing/tests` 차이 0).

| 파일 (bms-balancing 기준) | 무엇 |
|---|---|
| `docs/REIL_C4A_IMPL_REQUEST_v3_20261124.md` (96,546 B · sha256 `2156f12d35c05c3a41307c4c254ce0bf836f9bdcbc33485c1eba2bb995d71c5b`) | 구현 요청서 v3 — §0 대응표 (subissue 키마다 변경 위치 · 해결 방식 · 유지 제한) · I1–I7 · 승인 결속 · 판정 · 시험 · 함수별 허용표 · 절차 · 마감 연결표 · 사용자 몫 (U2 · U4 · U5) |
| `docs/REIL_C4A_IMPL_REQUEST_v2_20261106.md` (34,092 B · `d85e9a64…`) · `docs/REIL_C4A_IMPL_REQUEST_20261106.md` (15,873 B · `86f2d631…`) | v2 · v1 (보존) |
| `reviews/review_reil_c4a_impl_v2_prereview_20261108/` | v2 재검토 회신 보존본 (원장 §130) |
| `docs/REIL_PREREQUISITES_STATUS_20261004.md` §130 · §131 | 원장 — 회신 반입 · 이번 작성 기록 |
| `docs/REIL_C4A_SCOPE_v2_20261106.md` (`605520b8…`) · `docs/REIL_C4_APPROVAL_REQUEST_v2_20261013.md` (`22dcc8e5…`) | 기준 범위안 · 채택된 C4 요청 v2 |
| `scripts/reil_c4_h.py` · `scripts/reil_c4_hb.py` · `scripts/reil_c4_monitor.py` · `scripts/reil_c4e_run.py` · `scripts/reil_c4e1_launch.py` · `tests/test_reil_c4_0a.py` · `tests/test_reil_c4_0a_fix.py` · `tests/test_reil_c4_0b1.py` · `tests/test_reil_c4_0b1_fix.py` · `tests/test_reil_c4_0b1_fix2.py` · `tests/test_reil_c4_0b2.py` · `tests/test_reil_c4e.py` · `tests/test_reil_c4e1_launch.py` · `tests/test_reil_c4e1_runner.py` · `reviews/prereview_pybamm_reil_20261003/external/util_LFP.py.txt` | 인용한 연결부 (행 번호 = pin `fa502acb`) |

v2 → v3 에서 바뀐 것 (지적별 요지 · 자세한 것은 v3 §0):

| 지적 | v3 의 답 | 위치 |
|---|---|---|
| N1 `allowlist` | 파일 단위 표 → 시험 함수 단위 표 (정적 상한 규칙 R1–R7 · 소스 행) — 0b1* / 0b2* 의 supervise fork K5 · 0a / c4e 중단 시험의 K4 · K6 ⊂ K3 (git 하나가 둘을 함께 예약) · 0b2 `test_c_8` K5 ≤ 2. launcher 회귀 파일의 함수별 수치는 같은 규칙으로 b0 에서 봉인 (v3 에는 규칙 · helper 상한만) | §6-2 · §7 |
| N1 `coverage` | 수집 전 설치 (`-p` 사전 적재) · 수집 뒤 별칭 감사 (기본인자 · from-import · 전역이 원본이면 실패) · 단계 귀속 (collect / setup / call / teardown / session) · fork 자식 상속 + 시작 / 끝 기록 · spawn / forkserver 차단 · 분리 해석기 자식은 생성 · 프로그램 sha · 종료 · 그룹 빔까지 (안의 호출 · 손주는 세지 않는다고 명시) | §3 I7 · §9 |
| N1 `before_call` | 잠금 → 허용 · 상한 확인 → 예약 → 원 함수 / 위반이면 차단 (원 함수 미실행 · 원인 · 수 · `CallBlocked` · 그 nodeid 실패 · 세션 멈춤) · 세션 끝 대조는 보조 | §3 I7 |
| N1 `bootstrap` | b0 준비 · 봉인 (계수기 완성본 · 자체 검증 T16a–j 포함 · 실행 0) → b1 수집 1 회 → b2 RED 1 회 (자체 검증 먼저 · 실패면 대상 전에 멈춤 · 판정 분리) → c 구현 · GREEN | §7 · §6-1 |
| N3 `distinct` | exact = (overflow 0 · 잘림 0) · n_distinct = len(keys) + int(overflow > 0) (exact false 면 하한) · 집계는 "잘린 키 기준" · T11 에 접두사 충돌 · N2 의 기대 dict 값은 그대로 | §3 I3 · §6-1 |
| N3 `retained_bytes` | 주장 = 키 payload ≤ 4,800 B + 보관 객체 개수 · 총 메모리 바이트 상한은 주장하지 않음 · 고정 총량은 U4 (미채택) | §3 I3 · §11 |
| N3 `stderr` | 1 GiB = 감시 표본 중지 임계값으로 한정 · 확인 사슬 ①–⑤ (감시 · runner_a P6 · run-a `final_record` · launcher_a 자식 종료 뒤 · 외곽 / 판정기) 와 책임자 · 초과 → 유효성 false · 인계 0 · 후속 wave 0 · 실제 쓰기 상한은 U5 (미채택) | §3 I3 · I1 · I5 · §8 |
| N4 `late_completion` | 루프 안: 마지막 완료가 첫 시작 + 900 안에 관측될 때만 닫힘 · 아니면 초과 (진행 중 · 완료 하한) · 미확인 모두 중지 · 루프 뒤: 행의 `t_end` 로 WITHIN / EXCEEDED / UNDETERMINED / INCOMPLETE (P5) | §3 I4 · I1 · §6-1 T12 · T17 |
| N4 `late_row_validation` | runner_a P4 가 모든 COMPLETED (최종 drain 포함) 를 같은 N5 판정 함수로 재검증 · 최초 사유 유지 · `post_checks` · 지속 중지 · 인계 제외 · ROW_INTEGRITY_A 필수 필드 정정 | §3 I1 · I4 · §5-1 · §6-1 T17 |
| N4 `cleanup_gate` | P1–P3 실패 → HB 반환 전 문자열 `global_stop` + runner_a 안의 지속 중지 (뒤 호출은 supervise 0) · T10 에 None + alive 1 · drain false | §3 I1 · §6-1 T10 |
| N4 `time_boundaries` | 중지 / 정상 정리 경로와 drain 구분 (40 · 80 s 는 join 배분 · wall 상한 아님) · 절대 시각 사슬 D_prep · D_meas · D_clean · D_rec · 기록 창 = t_rec0 → D_rec (정리 포함 안 함) · 단계 절대 마감 = 외곽 감시 기한 · v2 의 합은 그대로 · 자식 기한 28,500 s 는 산술 (미채택) | §8 · §6-1 T18 |
| N6 `approval_binding` | 승인 § 안의 `c4a-approval` 블록 (kind `C4A_EXECUTION` · decision `APPROVED` · scope · 승인한 요청서 경로 · sha) + 실행 요청서의 `c4a-binding` 블록 ↔ 실제 소비값 · T14 에 무관 · 거절 · 구현 전용 · 블록 둘 · 동시 교체 · 결속 값 불일치 | §4-2 · §6-1 T14 |
| C2 | 미완 행의 unit = 계획 매핑 · 원행에 unit 이 있으면 먼저 불일치 판정 (덮어쓰지 않음) · T07 | §5-1 · §6-1 |

질문 여섯:

1. §0 의 대응이 N1 · N3 · N4 · N6 의 subissue 열둘과 C2 를 닫습니까? 빠지거나 새로 생긴 문제가 있습니까?
2. N1 `allowlist` · `coverage` — 시험 함수별 정적 상한 (R1–R7 · §6-2 의 표) 과, launcher 회귀 파일의 함수별 K3 / K6 / K4 수치를 b0 에서 같은 규칙으로 구해 수집 전에 봉인하는 방식이
   "RED 전 고정" 을 채웁니까 (아니면 그 수치를 요청서에 먼저 적어야 합니까)? 분리된 `-I` 해석기 자식 안의 호출과 손주를 세지 않고 생성 · 프로그램 신원 · 종료 · 그룹 빔까지로 주장을
   좁힌 것이 받아들일 수 있는 범위입니까?
3. N1 `before_call` · `bootstrap` — 호출 전 잠금 · 예약 · 차단 순서 (§3 I7) 와, 자체 검증 (T16a–j · 부정 경로는 하위 pytest 안에서) 을 RED 한 번 안에서 대상보다 먼저 돌리고 하나라도
   실패하면 대상 전에 멈추는 방식 (§7 b2 · v2 의 RED 시간 상한 안) 이 "계수기 자체 검증 ↔ 대상 골격의 기대 RED 실패 분리" 를 채웁니까? 별도 실행이 맞다면 그 실행의 시간 상한은 새
   숫자라 사용자 몫이 됩니다.
4. N3 — exact · 하한의 의미 · 보관량 주장을 키 payload 4,800 B 와 객체 개수로 좁힌 것 · 1 GiB 를 표본 중지 임계값으로 한정하고 확인 사슬 ①–⑤ 와 책임자를 둔 것이 충분합니까?
   (U4 · U5 는 미채택 선택지로만 두었습니다.)
5. N4 — 루프 안의 unit 닫힘 (관측 증명이 없으면 "미확인" 도 중지) 과 runner_a 의 P4 · P5 · P1–P3 · §8 의 시간 경계 (기록 창 t_rec0 → D_rec · 정리 경로 둘 · 여유 300 s 의 자리 ·
   자식 기한 산술) 가 맞습니까? 루프 안 "미확인" 을 중지 대신 t_end 판정으로 미루는 편이 낫다면 그 방향으로 고치겠습니다.
6. N6 — `c4a-approval` 블록 (종류 · 결정 · 범위 · 승인 sha) 과 실행 요청서의 `c4a-binding` 블록을 통한 전이 결속, T14 의 부정 사례가 충분합니까?

이 발송은 실행 지시가 아닙니다. 이번 작업은 문서 작성과 코드 읽기뿐이고, 구현 · 시험 · pytest 수집 · 대상 import · 설치 · 자료 개봉 · 맞춤 · 실행 · COMSOL 은 0 회입니다. 요청서 v3 와
회신은 **구현 · 시험 · 실행 승인이 아니며**, 구현 승인은 사용자가 따로 합니다. **U2 (전체 10 h 배분) 는 미선택**이고 (단계 28,800 s · 전체 36,000 s 는 산술만 수용된 제안), v3 의
U4 · U5 와 자식 기한 산술 28,500 s 도 채택하지 않았습니다.

---
