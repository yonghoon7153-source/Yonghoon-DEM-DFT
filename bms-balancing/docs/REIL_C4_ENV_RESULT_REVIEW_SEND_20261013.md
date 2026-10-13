# Codex 발송 프롬프트 — REIL C4-ENV 결과 검토 (새 봉인을 C4 환경으로 수용할지) · 2026-10-13

> 사용자 결정 (2026-10-13 "권고대로" · 상태 문서 §36) 으로 실행한 C4-ENV 의 결과다 (§37). 아래 `---` 사이가 붙여 넣을 본문이다.
> 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-ENV (새 환경 세대 준비) 를 승인 범위대로 1 회 실행했습니다. 결과를 검토하고, 새 봉인을 C4 환경으로 수용할지 판정해 주세요.
브랜치 `claude/14-gate-code-review-9qkx05` 의 최신 HEAD (이 발송문이 든 커밋) 를 기준으로 보시면 됩니다. 실행 기록 커밋은 `1135624c` 입니다.

## 1. 승인과 실행

- 승인 요청은 지난 회신의 비활성 초안을 채운 것입니다: `bms-balancing/docs/REIL_C4_ENV_APPROVAL_REQUEST_20261013.md`. 고정 표 §1 · 순서 §2 ·
  채택 문구 §6 입니다.
- 사용자 승인 기록은 상태 문서 `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md` §36 (커밋 `e5b7a254`) 입니다. 같은 자리에서 C4-0 범위
  재확인 (`REIL_C4_APPROVAL_REQUEST_v2_20261013.md` §8) 도 받았습니다. C4-0 은 이 검토가 새 봉인을 수용한 뒤에만 시작합니다.
- 결과 요약은 상태 문서 §37 이고, 원문은 `bms-balancing/evidence/reil_c4_env_20261013/` 입니다.
  - 1 회 · S0–S10 전부 rc 0 · 36.4 s / 1,800 s.
  - 디스크 최대 556,020,307 B / 2,000,000,000 B.
  - `check OK`. emit 1 + check 1 이므로 합성 COBYQA 2 회 · Sobol 경로 2 벌입니다.
  - REIL 자료 · pytest · 맞춤 · C5 재측정 · COMSOL 은 0 입니다.

## 2. 결과

| 대상 | 결과 | 원문 |
|---|---|---|
| 내려받기 | 과학 wheel 28 의 이름이 P0 설치 로그의 이름 28 과 정확히 같습니다. 시험 도구 4 는 `이름==판` 이 일치합니다. sha256 은 전부 기록했습니다 | `04_artifacts_science.json` · `04_artifacts_test.json` |
| 바이트 동일 | `COBYQA_OPTIONS.json` · `SOBOL_PHASE_A.json` · `.npy` 6 (옵션 8 · 구현 파일 4 · raw float64 · `.npy` sha) | `09_old_new_diff.json` |
| lock | `#@ python` 3.11.15 → 3.11.17 한 줄과 RECORD sha 4 (cffi · fonttools · numpy · pip) 만 다릅니다. 이 4 개는 bin 행이 있는 배포판 집합과 정확히 같습니다. 머리 · `#@ files` 7187 / 5301 / 1 / 1 · collision 줄 · 30 판 · 나머지 26 RECORD 는 바이트 동일합니다 | 두 봉인의 `REIL_C6.lock.txt` |
| PROFILE | `python.version` · `python.build` 두 값만 다릅니다. 다시 직렬화하면 바이트 동일합니다. BLAS / LAPACK · libc 는 같습니다 | 두 봉인의 `PROFILE.json` |
| RECORD 행 | 30 / 30 통과입니다. wheel 안 RECORD 행은 그대로이고, 나머지는 pip 가 만든 행뿐입니다. bin 첫 줄 10 개는 모두 새 venv 경로입니다. RECORD 원문 30 은 보존했고 새 lock 과 결속을 확인했습니다 | `09_records/` · `09_old_new_diff.json` 의 `record_rows` |
| 새 봉인 | `bms-balancing/reil_c6_rebuild_20261013/` · MANIFEST `4f12094897b53463…bdc` · lock `ea91156c…1faa` · PROFILE `50f2c7fb…a641` | — |
| 보호 · 비밀 | 옛 봉인 · C5 기록 · 스크립트 변경 0 · 비밀값 검사 0 · 저장소 pyc 쓰기 0 | `10_end.json` · `00_s0_precheck.json` |

## 3. 검토해 주실 것

1. old→new 차이가 승인된 허용 차이 (요청 §1-8) 안인지. 대조 도구의 판정은 `allowed_only: true` 입니다. 원문 (두 봉인 · RECORD 원문 30 ·
   `09_old_new_diff.json`) 으로 확인해 주세요.
2. **아직 보지 않으신 코드 두 개:**
   - 대조 도구 `bms-balancing/scripts/reil_c4_env_compare.py` (sha256 `eff94d3d…95e0`) 와 그 자체 확인 23 / 23
     (`evidence/reil_c4_env_compare_selftest_20261013/`).
   - 실행기 `evidence/reil_c4_env_20261013/00_runner.py` (sha256 `5c781a2d…d2cc`). 요청 §2 의 argv · cwd · env 와 같은지 봐 주세요.
3. 승인 문서에 없던 편차 두 가지를 받아들일 수 있는지:
   - (a) 자식 프로세스 env 에서 비밀 형태 변수 15 개를 뺐습니다 (이름만 `*.meta.json` 에 기록).
   - (b) 실행 전에 실행기의 읽기 전용 사전 점검을 한 번 돌렸습니다 (디렉터리 생성 0 · 문제 0 · 실행 1 회와 별개).
4. 새 봉인 `reil_c6_rebuild_20261013/` 을 **C4 환경으로 수용할지.** 수용하시면 다음 둘을 적용합니다:
   - 이번 check 1 회를 C4 의 전체 C6 자기점검 1 회로 인정합니다 (v2 §4-6).
   - C4 실행기는 이 봉인 경로와 MANIFEST `4f120948…` 를 명시 인자로 받습니다. 옛 기본 경로는 쓰지 않습니다.
5. **컨테이너가 C4-0 전에 다시 바뀌는 경우.** venv 가 세션 스크래치에 있어서 생길 수 있는 일입니다. 아래 "동일 아티팩트 복원" 규칙 안에
   대한 의견을 주세요. 지난 회신 §5 의 구분을 구체화한 것이고, 지금 승인을 구하는 것은 아닙니다.

## 4. 동일 아티팩트 복원 규칙 안 (의견 요청 · 미승인)

아래 조건이 **전부** 맞을 때만, 새 차이 검토 없이 "같은 환경" 으로 봅니다:

- interpreter `/usr/bin/python3.11` 의 파일 sha256 `73bf4b06…bb99` · 판 · 빌드 · deb 판이 같다.
- 같은 절대 경로 (`…/scratchpad/reil_c4env/…`) 를 쓴다. 세션이 바뀌어 경로가 달라지면 이 규칙을 쓰지 못한다.
- 내려받은 wheel 32 개의 sha256 이 `04_artifacts_*.json` 과 같다. 다르면 설치 전에 중지한다.
- 요청 §2 와 같은 argv 다.
- 설치된 RECORD 30 + 4 가 보존 원문과 **바이트 동일**하다.
- emit 1 회의 11 파일이 새 봉인과 **바이트 동일**하다 (check 1 회).

한도는 1 회 · 1,800 s · 2,000,000,000 B 입니다. 하나라도 다르면 새 세대로 보고 별도 승인을 받습니다.

## 하지 않은 것 · 회신 형식

REIL 원자료 · pickle · 노트북 개봉 · 맞춤 · pytest 실행 · C4-0 착수 · C5 재측정 · COMSOL. 회신은 다음 형식으로 부탁드립니다: 판정 · 발견
(P1/P2 · 파일:줄 · 최소 조치) · 새 봉인 수용 여부 · 편차 (a)(b) 의견 · 복원 규칙 의견 · `DECISION.json`.

---
