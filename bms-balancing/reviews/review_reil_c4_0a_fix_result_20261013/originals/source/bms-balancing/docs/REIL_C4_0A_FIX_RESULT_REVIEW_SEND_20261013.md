# Codex 발송 프롬프트 — REIL C4-0a 한정 보완 (C4-0A-N1–N4) 결과 재검토 · 2026-10-13

> 지난 회신 (C4-0a 결과 검토 · 증거 한정 수용 · 종결 보류 · 상태 문서 §42) 의 네 항목을, 사용자 승인 (§43) 범위대로 보완한 결과다 (§44).
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-0a 의 네 P2 항목 (C4-0A-N1–N4) 을 승인 범위대로 한 번 보완했습니다. 재검토해 주세요. 브랜치 `claude/14-gate-code-review-9qkx05` 의
최신 HEAD (이 발송문이 든 커밋) 를 기준으로 보시면 됩니다. 실행 기록 커밋은 `97cad936` 이고, 착수 HEAD 는 `33b58cd7` 입니다.

## 1. 승인과 고정본

- 승인 요청: `bms-balancing/docs/REIL_C4_0A_FIX_APPROVAL_REQUEST_20261013.md`. 사용자 원문 "reil은 승인이야" (§43).
  §6 의 두 선택은 문서의 권장으로 읽었습니다 — GREEN 에 기존 26 포함 · 건조 재실행 없음.
- 승인 **전에** 고정한 두 파일 (커밋 `7e7c0432`):
  - 대조 14: `docs/REIL_C4_0A_FIX_CONTROLS_DRAFT_20261013.py.txt` (`b2137e11…004c`) — 실행 때 `tests/test_reil_c4_0a_fix.py` 로 바이트 그대로 복사.
  - 패치: `docs/REIL_C4_0A_FIX_PATCH_DRAFT_20261013.diff` (`a3f527a4…7874`) — 결과 sha 기대값까지 고정.

## 2. 결과 (원문 `bms-balancing/evidence/reil_c4_0a_fix_20261013/`)

| 단계 | 배정 | 실측 | rc | 결과 |
|---|---|---|---|---|
| 01 identity | 60 s | 21.893 s | 0 | C4-0a 와 같은 스크립트 · 인자 · ok · problems [] |
| 02 RED (새 시험만 · 패치 전) | 600 s | 12.284 s | 1 | 10 실패 · 4 통과 — 승인 문서 §3 의 선언과 같음 (실패 종류 포함) |
| 패치 적용 | — | — | — | 고정본 `git apply` · e3a `33b85537…` · monitor `06445100…` = 기대 |
| 03 GREEN (기존 26 + 새 14 · `-rP`) | 600 s | 18.307 s | 0 | 40 통과 · stderr 0 B · 자동 수정 · 재시험 0 |

- 계산 합 52.484 s / 1,260 s. 끝 기록 103.5 s / 7,200 s 는 커밋 · push · 문서 작성 전 snapshot 입니다 (`04_end.json`).
- RED 의 음성 대조는 대부분 **행동으로** 실패했습니다:
  - n1_a `DID NOT RAISE` — 지금 dryrun 이 바뀐 배열로 계획을 썼다.
  - n2_a · b `COMPLETE` · n2_d `limit_violations` 없음.
  - n3_a `global_stop None` — 대본 multiprocessing 문맥 · 주입 시계 · 실제 프로세스 0.
  - n4_a · b partial 없음 — n4_b 는 실제 fork 작업자.

  `TypeError` (n1_b · c) 와 `AttributeError` (n3_c) 는 구현 전 인터페이스입니다.
- 합성 NSGA2 outcome 을 파일로 남겼습니다 (`02_red.` · `03_green.nsga2_synthetic_outcome.json`):
  - 둘 다 `returned` · 평가 5,000 · 해 50 · 비유한 0 · 경고 0. 벽시계 밖 필드는 같습니다.
  - GREEN 로그의 test_07 출력은 `NSGA2_SYNTHETIC_OUTCOME returned 5000` 입니다.
  - C4-0a GREEN 실행 자체의 분기는 여전히 원문이 없으므로 소급 주장하지 않습니다.

## 3. 고친 것 (패치 · 원 함수 대비)

- **N1** `check_arrays(arrays_dir, *, seal, manifest_sha256)`: 수용 C6 MANIFEST 를 명시 sha 로 인증 → npy 넷을 그 항목에 직접 대조 → 그 뒤 로컬 자기 일치.
  `dryrun` 은 이미 받은 `seal` 을 넘깁니다. CLI 는 그대로입니다.
- **N2** `final_record`: 마지막 쓰기 · 재읽기 · 해시 · 용량 조회 뒤 snapshot 하나로 시간 판정 · 같은 값 반환. 넘으면 `RECORD_INCOMPLETE` (파일 · 해시 ·
  바이트 수 보존). 시간 · 크기 위반을 `limit_violations` 에 둘 다 남깁니다.
- **N3** `Watch.stale(now)` (확인만 · `last_valid` · `samples` 불변). `supervise` 가 RSS 조회 뒤 · 디스크 조회 뒤 · 정상 종료 직전에 두 감시기의
  freshness 를 봅니다. 기존 이유 (마감 재검사 등) 가 먼저입니다.
- **N4** `worker_loop` 의 구조 오류 이벤트에 `partial`. `_states` 가 그 작업 행 (`STARTED_INTERRUPTED` 그대로) 에 `structural_partial` 을 붙입니다.
- 바꾸지 않은 것: `run_e3a_call` · `classify` · 배열 봉인 · C5 코드 · 기존 시험 파일 · 기존 증거.

## 4. 검토해 주실 것

1. 네 보완이 지난 회신의 요구를 채우는지 — 특히 N3 의 freshness 확인 위치 세 곳과 "확인은 표본이 아니다" (n3_c).
2. 대조 14 의 양성 · 음성이 같은 분기를 덮는지. 회신이 요청한 반례가 들어 있습니다:
   - 배열과 로컬 봉인을 함께 바꾼 음성 (n1_a).
   - 마지막 쓰기 · 크기 조회 지연 (n2_a · b).
   - 마지막 디스크 지연과 RSS 공백 (n3_a).
   - worker 경계를 통과한 partial (n4_b).
   - wrapper 내부 오류의 구조 분기 (n4_c · 특성 고정).
3. 밝힐 것 넷:
   - (a) 합성 NSGA2 호출은 승인 문서대로 3 회입니다.
   - (b) RED 에는 `-r` 를 붙이지 않았습니다 (기본 fE). GREEN 로그에 보이는 argparse 오류 문구는 test_08 이 기대하는 SystemExit 의 출력입니다.
   - (c) 단계 실행기는 C4-0a 의 것에서 증거 경로 · scratch 폴더 · env 두 개만 다릅니다 (`00_step_runner.py`).
   - (d) identity 는 컨테이너 재시작 뒤 21.9 s 였고, 원인을 추정하지 않습니다.
4. C4-0a 를 종결할 수 있는지. 종결하면 다음은 C4-0b 의 사용자 확인입니다 — 배열 3 종 (profile Sobol 2 · 동시 Sobol 16 · label-seed) 의 목록 · 배정을
   넣습니다. 지금은 C4-0b · C4-E / A / B · 자료 개봉 · 맞춤 · 설치 · 환경 재구축 · COMSOL 을 하지 않습니다.
