# MXD2R 재확인 준비 — 구현 측 제한 재실행 (2026-11-04)

요청서: `docs/reviews/codex_mixer_mxd2r_recheck_request_20261104.md`. **독립 외부 판정 전**이며 MXD2R-01–04 claimed_fixed / MXD2-01 open을 바꾸지 않는다. 새 생산 코드·상주 시험 수정 없음. 합성 덱과 Python 소비자만 실행했고 DEM/LIGGGHTS·WSL·ibb 실행은 하지 않았다.

## 1. 판과 재현

- 실행 기반: `7b51e591e6482484d1b85b237dc0c73936fa96b6`, `codex/mixer-1104`; Python **3.11.17**, NumPy **2.4.6**, Linux, 스레드 환경 네 변수 모두 1. 정확한 해석기·플랫폼·명령·rc·시간·로그 SHA는 `current/run_summary.json`.
- 현재 파일로 직접 실행했다. 네 소비자·시험 파일이 기반 Git blob과 같음을 `claim_audit.json`에, 로컬 import 의존성 12개와 재사용 하네스 7개의 실행 전 SHA 및 실행 후 동일성을 `current/run_summary.json`에 기록했다.
- 최종 리뷰 핀은 배포 ZIP 루트 `PIN.txt`가 정한다. 이 문서 자체의 커밋 SHA를 내부에 넣지 않는다. 리뷰 핀의 실행 소스 SHA를 위 기록과 대조해야 한다.
- `consumer_changes.patch`와 `relevant_commits.txt` = `git diff` / `git log --format='%H %s' 80095a7f0..7b51e591e -- scripts/mixer_deck_readback.py scripts/mixer_deck_diff.py scripts/mixer_smoke_blind.py scripts/test_mixer_d2_consumers.py` (관련 커밋 11개).

```bash
# 전달 PIN.txt의 커밋을 checkout한 Git 저장소 루트에서; 출력 폴더는 새 경로여야 한다.
/workspace/.venvs/yonghoon-dem/bin/python -I -X utf8 -B \
  docs/reviews/mxd2r_recheck_evidence_20261104/tools/run_bounded.py \
  /tmp/mxd2r-recheck-new
# 아래 SHA256SUMS는 이 증거 폴더에서 검사 (자신 제외).
```

해석기 경로는 이 실행 환경의 경로다. 다른 환경에서는 준비된 Python 경로로 바꾼다. 하네스는 스레드 1을 설정하고 `/tmp` 사본에서만 변이한다. 기존 증거를 덮어쓰지 않는다.

**Git 전제:** 위 하네스는 `git rev-parse HEAD`로 실행 판을 기록하므로 **리뷰 PIN을 checkout한 실제 Git 저장소**에서만 실행한다. 전달 ZIP은 선택 파일·증거 스냅샷이며 Git 메타데이터가 없다. ZIP만 풀어 위 하네스를 실행하면 안 되며, 다른 저장소 아래에 풀어 바깥 HEAD를 기록하는 것도 유효한 재현이 아니다. 실행 전 `git rev-parse --show-toplevel`이 사용하는 checkout 루트인지, `git rev-parse HEAD`가 전달 PIN과 같은지 확인한다. ZIP의 개별 파일은 manifest/소스 해시 대조와 코드·증거 검토용이다.

## 2. 이번 실행 결과 (과거 수치와 합산하지 않음)

| 실행 | 결과 | 증거 (`current/` 아래) |
|---|---|---|
| 원본 D2 상주 시험 | **29/29 OK**, 독립 입력 정상 48조합 시험 포함 | `d2_consumers.log` |
| readback / diff 자체시험 | **24/24 · 55/55 PASS** | `readback_selftest.log`, `diff_selftest.log` |
| smoke 자체시험 | **rc 0**; 마지막 `전부 통과` (체크 표시 줄을 시험 수로 세지 않음) | `smoke_selftest.log` |
| 외부 사례 원본, CLI 세 경로 | 정상 0/0/0; 명명 반례 7 + friction 누락 + 음성 대조 2는 각각 1/1/1; traceback 없음 | `current/external_cli_cases/cli_rc_current.json`, 사례별 로그 33개 |
| 사전 공격 v3 | **93/93** 기대·사유 일치 (공통 변조·메타 동반·문자·skin 및 양성 배치) | `preattack_probe_v3.json` |
| 옛 범위 밖 공통 변조 | **17/17**, 각각 세 API FAIL | `outside_scope.json` |
| 생성기 옵션 양성 | 생성된 **18/18 × 네 API PASS**; 별도 rpm 60은 생성기 자체 거부, 합계 `bad 0 of 19` | `positive_extra.log` |
| 선택 변이 (scratch만) | **6/6 탐지**, 변이 없는 대조 rc 0, 사본 복원·추적 소스 동일 확인 | `mutation_subset.json`, `mutation_subset.log`, `run_summary.json` |

CLI 사례 11개는 외부 파일 그대로 읽고 입력 바이트 수·SHA를 저장했다. `crlf_lf_metadata`는 `actual deck file bytes` SHA 사유, `crlf_crlf_metadata`는 CR 179개·LF-only 사유다. 상주 29개, 48조합, 93사례, CLI 33회는 서로 겹치는 검증 층이므로 더해서 독립 시험 수로 쓰지 않는다.

변이 선택은 M01(run 옵션), M06(neigh 인자), M16(정규화 해시), M21(제어 문자), M31(skin 기대를 덱에서 복사), M55(skin 계수 0.5→0.6)이다. 앞 다섯은 해당 반례/사유 시험이 실패하고 M55는 정상 생성기·48조합 양성 시험도 실패한다 (`failing_tests` 목록). 하네스는 rc·실패 메서드를 보존하며 각 변이의 전체 traceback은 저장하지 않는다. **전수 55개 중 선택 6개만 재실행**했다.

## 3. 요청 전 사전 공격 대조

| CLAUDE.md 규칙 | 이번 근거와 경계 |
|---|---|
| ① 숫자·판·전칭 대조 | 위 표를 원본 로그/JSON에 대조. `claim_audit.json`: 기존 상위 SHA256SUMS **80/80**, 하위 **48/48**, 불일치 0 (중첩 목록이며 고유 128개가 아님); 네 파일 기반 일치; 관련 커밋 11개. 기존 문서의 과거 55/55 변이·before 실패는 새 실행으로 세지 않음 |
| ② HOLD 부류 직접 공격 | 29 상주 시험 + 외부 원본 CLI + v3 93사례 + 공통 변조17. 시간·삽입·회전·접촉·바이트 및 `_d2_text_form`/`_d2_generator_form` 범위. 기대 거부 사유는 v3의 `right_reason`과 CLI 원문으로 확인 |
| ③ 독립 반박/변이 | 이번 준비는 외부 독립 반박을 대신하지 않는다. 아래 선택 변이는 구현 측 회귀 민감도 점검이며 전수 55개 재실행이 아님 |
| ④ 요청서 맨 위 범위 구분 | 요청서 첫 표: MXD2R-01–04 개발 소비자 종결만 요청; MXD2-01 전체·실제 실행 GO 제외 |

## 4. 한정과 파일 목록

- **뜻이 같아도 표기가 다르면 거부한다 (생성기 꼴 엄격).** neighbor skin은 이제 생성기 수치와 표기를 고정하지만, 모든 입력의 물리적 정당성을 인증한다는 뜻은 아니다. CED·계획수·dt 등 기존 수치 검사의 허용폭을 이번 문서로 새로 좁히지 않는다.
- LIGGGHTS 실행 의미·Windows·Python 3.8 실행 미확인. 여기의 Linux Python 결과로 그 환경 통과를 주장하지 않는다. Python 3.12+ 합산 반올림과 생성기 식 사본의 잠재 차이는 기존 `docs/reviews/mxd2r_fix_evidence_20261103/mxd2r04/README.md` §6 한정 그대로다.
- 기존 증거의 `ResourceWarning`은 생성기의 파일 열기 경고다. 새 기능 실패나 새 물리 결과로 세지 않는다. 웹앱·전체 게이트는 이 제한 재실행의 대상이 아니다.
- 새 파일: 이 README, 요청서, `claim_audit.json`, `consumer_changes.patch`, `relevant_commits.txt`, `dependency_paths.txt`, `tools/run_bounded.py`, `current/` 명령 로그·JSON, `SHA256SUMS` (이 폴더 파일만, 자기 제외). 외부 ZIP의 파일 manifest와 PIN은 배포 단계에서 별도로 확정한다.
- 재현 의존성: `current/run_summary.json`의 `sources_sha256` 경로 19개 + 외부 `d2/evidence/cases/`의 11사례 × `old.in`, `new.in`, `old.meta.json`, `new.meta.json`. smoke 자체시험의 합성 셀은 `dem_scripts/mixer_20260919/Drum.stl`, `Front.stl`, `Back.stl`을 읽는다 (`claim_audit.json`에 SHA·기반 일치 기록). 원래 판정·수정 증거 README/manifest 및 하위 `q4_skin/`도 검토용으로 동봉한다. 전체 저장소가 필요한 묶음이라고 주장하지 않는다.
