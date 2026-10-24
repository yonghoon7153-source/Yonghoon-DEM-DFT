# 실제 입력·WSL 점검 명령 안내 (2026-10-24 KST)

Claude 메인보드 반입을 기다리는 동안 T12 계약·합성 반례 개발은 계속할 수 있다. 사용자에게 지금 필요한 것은 **보유한 실제 자료와 원본 외부 판정의 전달**이다. 아래 WSL 명령은 사용자가 소유한 장비에서 선택해 실행할 수 있도록 준비했으며, 이 작업에서 사용자 WSL에 접속하거나 실행하지 않았다. 정책 비준은 이미 기록되어 있다.

## 1. 지금 보낼 수 있는 자료

| 대상 | 보내면 다음 작업에 바로 쓰이는 것 | 아직 없는 경우 |
| --- | --- | --- |
| ULPR 외부 반박 | 검토한 전체 커밋 SHA, 원문 판정, 재현 명령·반례·전체 로그. 이번 전달 대상 핀은 `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362` | 외부 판정은 미수령으로 유지하고 로컬 T12 개발 진행 |
| Q7 펠릿 3개 | 시료 ID별 질량(g)·직경(mm)·두께(mm) 및 각각의 불확도, 제조 이력, 측정 하중·상태, 불확도 정의·공유 계통오차, 원본 측정표 | 측정값을 추정해 채우지 않음 |
| Q8 랩 표준 | “10–13%”의 원기록, 시료 수·재료·질량·밀도 기준·두께·공극률 정의·하중/상태, 실험과 모형의 출처 구분 | 숫자만 전달하면 비교 기준을 확정할 수 없음 |
| Q9 두께 상태 | 다이 안 가압/제하/탈형 후/EIS 지그 중 실제 상태, 압력, 제하·재하 이력, 측정 시각, 원기록 | 실험과 DEM의 상태 대응은 미확정 유지 |
| LHS 실제 WSL | 아래 §2 출력. 실제 B7 지정 후에는 §3의 영수증 묶음 | 클라우드 합성 결과를 WSL 결과로 바꾸어 적지 않음 |
| MXD2·D3 | 보유한 실제 형상/CAD·덤프·관측 자료와 출처·단위·측정 상태; 이미 등록된 S1/S3 문서가 있으면 그 원문 | S1 수치·시드·코호트, 통계 폭·불확도·관측 적격성은 빈칸 유지 |

측정표·노트·이미지 등 원래 형식으로 전달해도 된다. `factual-input-form.blank.json`은 수령 항목을 정리하는 양식이며 사용자가 먼저 JSON을 완성해야 하는 관문은 아니다. 경로와 해시만으로 자료의 물리적 적격성을 인증하지 않는다.

## 2. 지금 가능한 WSL 읽기 전용 확인

실제 WSL Bash에서 `TASK_REPO`를 **기존 checkout 최상위 절대 경로**, `TASK_PY`를 **실제로 쓸 Python 실행 파일의 절대 경로**로 먼저 지정한다. 기본값이나 자동 경로 선택은 없다. 아래 블록은 checkout·입력 파일을 바꾸지 않으며 stdout/stderr 전체와 `*_rc`를 함께 전달한다. 환경 변수 전체, remote URL, 인증 정보는 출력하지 않는다. import에 실패하면 설치하거나 우회하지 말고 실패 출력 그대로 전달한다.

```bash
read -r -p '기존 WSL checkout 최상위 절대 경로: ' TASK_REPO
read -r -p '실제 Python 실행 파일 절대 경로: ' TASK_PY
(
  set +e
  : "${TASK_REPO:?기존 WSL checkout 최상위 절대 경로를 지정하세요}"
  : "${TASK_PY:?실제 Python 실행 파일 절대 경로를 지정하세요}"
  [[ "$TASK_REPO" = /* && "$TASK_PY" = /* ]] || exit 2
  [[ -d "$TASK_REPO" && -x "$TASK_PY" ]] || exit 2
  cd -- "$TASK_REPO" || exit
  TASK_TOP=$(git rev-parse --show-toplevel) || exit
  [[ "$(pwd -P)" = "$(cd -- "$TASK_TOP" && pwd -P)" ]] || exit 2
  [[ -f scripts/run_network_194_parallel.py ]] || exit 2

  printf 'checkout=%s\n' "$(pwd -P)"
  git rev-parse HEAD
  TASK_RC=$?; printf 'head_rc=%s\n' "$TASK_RC"; (( TASK_RC == 0 )) || exit "$TASK_RC"
  git status --short --branch
  TASK_RC=$?; printf 'status_rc=%s\n' "$TASK_RC"; (( TASK_RC == 0 )) || exit "$TASK_RC"
  "$TASK_PY" -B -c 'import sys, numpy, scipy, networkx; print("normal", sys.version.split()[0], numpy.__version__, scipy.__version__, networkx.__version__, sys.executable)'
  TASK_RC=$?; printf 'normal_python_rc=%s\n' "$TASK_RC"; (( TASK_RC == 0 )) || exit "$TASK_RC"
  "$TASK_PY" -I -B -c 'import sys, numpy, scipy, networkx; print("isolated", sys.version.split()[0], numpy.__version__, scipy.__version__, networkx.__version__, sys.executable)'
  TASK_RC=$?; printf 'isolated_python_rc=%s\n' "$TASK_RC"; exit "$TASK_RC"
)
TASK_RC=$?; printf 'inventory_rc=%s\n' "$TASK_RC"; (exit "$TASK_RC")
```

`TASK_REPO`/`TASK_PY`가 비었거나 현재 경로가 checkout 최상위가 아니면 멈춘다. 일반 실행과 `-I` 출력의 Python·패키지 버전·실행 파일을 비교한다. 이 확인 자체는 B7 핀 지정이나 발사 자격 판정이 아니다.

이미 있는 **원자료 파일 하나**의 신원도 확인할 수 있다. `TASK_INPUT`에 공유할 원자료 파일의 절대 경로를 지정한다. 파일 내용을 출력하거나 실행하지 않는다. 큰 덤프의 해시 계산은 파일 크기에 따라 시간이 걸린다.

```bash
read -r -p '확인할 기존 원자료 파일 절대 경로: ' TASK_INPUT
(
  set +e
  : "${TASK_INPUT:?확인할 기존 원자료 파일 절대 경로를 지정하세요}"
  [[ "$TASK_INPUT" = /* && -f "$TASK_INPUT" && -r "$TASK_INPUT" ]] || exit 2
  stat --format='bytes=%s modified=%y file=%n' -- "$TASK_INPUT"
  TASK_RC=$?; printf 'stat_rc=%s\n' "$TASK_RC"; (( TASK_RC == 0 )) || exit "$TASK_RC"
  sha256sum -- "$TASK_INPUT"
  TASK_RC=$?; printf 'sha256_rc=%s\n' "$TASK_RC"; exit "$TASK_RC"
)
TASK_RC=$?; printf 'file_inventory_rc=%s\n' "$TASK_RC"; (exit "$TASK_RC")
```

해시 출력과 함께 그 파일이 어떤 시료·실행·측정 상태의 원본인지 적는다. 비밀 파일이나 자격 증명 파일은 대상에 넣지 않는다.

## 3. B7·실제 경로가 생긴 뒤: 기존 LHS 사전 점검

정본은 [기존 묶음](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/854857e576a2a8aba07ec861dbee39d4bb59efae/docs/reviews/lhs214_relaunch_package_20261020.md) §3–5와 [실제 WSL 수령표](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/854857e576a2a8aba07ec861dbee39d4bb59efae/docs/reviews/lhs214_wsl_receipt_checklist_20261024.md)다. 두 링크는 별도 LHS 가지의 전체 리뷰 핀에 고정되어 있다. 새 collector나 자동 발사 스크립트를 만들지 않는다. **이 절은 지금 일괄 실행하는 블록이 아니다.** 각 단계의 원본 출력·종료 코드를 확인하고, 실패하면 그 지점에서 멈춘다.

기존 §3에서 B7은 등록 개정·수정이 들어간 메인보드 **`claude/stoic-knuth-NObVQ`의 push된 전체 40자리 커밋**으로 정의한다. LHS 리뷰 핀 `854857e576a2a8aba07ec861dbee39d4bb59efae`는 이 수정의 참조이며 **B7로 자동 대입하지 않는다**. 메인보드 반입을 미룬 현재 B7은 미지정이다. 다른 후보를 쓰려면 그 후보의 등록·봉인·인계 도구 조건을 먼저 확정해야 한다. 이전 핀의 영수증도 새 핀의 증거로 재사용할 수 없다.

| 먼저 채울 값 | 필요한 조건 |
| --- | --- |
| `TASK_REPO`, `TASK_PY`, `PIN` | 실제 WSL checkout/Python 절대 경로, 실제 B7 전체 SHA. 시작 HEAD=PIN, detached HEAD, tracked dirty 0 |
| `R194`, `RS` | 서로 다른 새 절대 ROOT 경로. 두 경로 모두 미존재, 기존 10-14 ROOT 보존 |
| `PF194`, `PFS` | ROOT 밖의 서로 다른 새 `.json` 절대 경로. 동명 `.log`, `_verify.json`, `_receipt.json`도 미존재 |
| `LOGD`, 반입 경로 | 새 로그 디렉터리와 실제 사용자 다운로드/반입 경로. 기존 PC/계정 경로 예시를 복사하지 않음 |
| 점검자·시각 | 실제 실행자와 시간대. §5 여섯 값의 손 대조 확인자도 기록 |

경로를 다 채우고 정본 §4의 시작 확인을 마친 다음에만 아래 기존 명령을 단계별로 사용한다. 명령은 **그 B7 checkout 최상위에서** 실행한다. 이 표는 명령 서명 안내이며, 출력 저장·종료 코드·후속 확인은 정본 §4와 수령표를 함께 따른다.

| 단계 | 기존 명령/산출물 |
| --- | --- |
| 의존성 확인 | §2의 일반/`-I` 확인. `env.txt`에 두 출력과 실제 종료 코드를 보존 |
| 실제 WSL 자체 시험 | `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` 조건에서 `"${TASK_PY:?}" scripts/wsl_network_smoke.py --selftest`, 같은 도구 `--selftest-real`; `g2_network_reread.py --selftest`, `run_network_194_parallel.py --selftest`, `supp20_input_receipt.py --selftest` |
| 194 수집 | `"${TASK_PY:?}" scripts/run_network_194_parallel.py run --root "${R194:?}" --dry-run --observe-imports --preflight-receipt "${PF194:?}"` |
| 194 검증 | `"${TASK_PY:?}" scripts/run_network_194_parallel.py preflight-verify --receipt "${PF194:?}" --expect-set production194 --approved-sha "${PIN:?}" --json "${PF194%.json}_verify.json"` |
| supp20 수집 | `"${TASK_PY:?}" scripts/run_network_194_parallel.py run --root "${RS:?}" --cohorts lhss --dry-run --observe-imports --preflight-receipt "${PFS:?}"` |
| supp20 검증 | `"${TASK_PY:?}" scripts/supp20_input_receipt.py --preflight-receipt "${PFS:?}" --approved-sha "${PIN:?}" --json "${PFS%.json}_receipt.json"` |

`run`이 들어간 위 두 수집 명령에는 **`--dry-run`이 필수**다. 실제 생산 `run`, 스케줄러 제출·취소, 실물 DEM 언로딩 명령은 이 안내에 포함하지 않는다. 자체 시험과 preflight도 실제 WSL 환경에서 수행한 기록이어야 하며, 현재 이 작업에서 실행하지 않았다.

기존 파이프 명령을 사용할 때는 Python 종료 코드를 `PIPESTATUS[0]`에서 즉시 보존한다. 예를 들어 fast16 한 단계는 다음처럼 원본 로그와 종료 코드를 함께 남긴다. `LOGD`는 위 조건에 맞게 이미 준비된 새 로그 디렉터리여야 하며 이 단계 출력 파일이 이미 있으면 중단한다. 전체 실행 순서를 자동화하는 새 도구가 아니다.

```bash
(
  set +e
  set -o noclobber
  : "${TASK_REPO:?}" "${TASK_PY:?}" "${PIN:?}" "${LOGD:?}"
  [[ "$TASK_REPO" = /* && "$TASK_PY" = /* && "$LOGD" = /* ]] || exit 2
  [[ -x "$TASK_PY" && -d "$LOGD" && "$PIN" =~ ^[0-9a-f]{40}$ ]] || exit 2
  cd -- "$TASK_REPO" || exit
  TASK_TOP=$(git rev-parse --show-toplevel) || exit
  [[ "$(pwd -P)" = "$(cd -- "$TASK_TOP" && pwd -P)" ]] || exit 2
  [[ "$(git rev-parse HEAD)" = "$PIN" ]] || exit 2
  git symbolic-ref -q HEAD >/dev/null 2>&1
  TASK_RC=$?; (( TASK_RC == 1 )) || exit 2
  TASK_DIRTY=$(git status --porcelain --untracked-files=no) || exit
  [[ -z "$TASK_DIRTY" ]] || exit 2
  [[ ! -e "$LOGD/fast16.log" && ! -e "$LOGD/fast16.rc" ]] || exit 2
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    "$TASK_PY" -B scripts/wsl_network_smoke.py --selftest >"$LOGD/fast16.log" 2>&1
  TASK_RC=$?
  printf '%s\n' "$TASK_RC" >"$LOGD/fast16.rc" || exit
  cat -- "$LOGD/fast16.log"
  printf 'fast16_rc=%s\n' "$TASK_RC"
  exit "$TASK_RC"
)
TASK_RC=$?; printf 'step_rc=%s\n' "$TASK_RC"; (exit "$TASK_RC")
```

위 예는 파이프를 쓰지 않아 원래 Python 종료 코드를 그대로 보존한다. 다른 단계도 원본 로그와 각 명령의 종료 코드를 함께 받는다. `tee`/`tail`의 성공을 Python 성공으로 읽지 않는다. 수집 실패 시 남은 부분 로그도 지우거나 성공한 로그로 덮지 않는다.

수령 묶음은 `env.txt`, 다섯 자체 시험 로그·각 종료 코드, 두 preflight JSON/전체 로그, 194 `_verify.json`, supp20 `_receipt.json`, 손 대조표, 전체 로그/영수증 SHA-256, 시작·종료 HEAD/dirty, tgz 자체 SHA-256이다. 194의 n·missing, IDs, raw 표, lhs/lhsx 코호트, code_fp·32파일 수를 등록 §2·§3 전체 값과 실제로 비교한다. 외부 발사 범위 판정은 이 실제 자료를 반입한 뒤에 받는다. S3·v1.3 HOLD와 기존 L214R-S03/S05 한정은 유지한다.

## 4. T12에는 아직 실행 명령이 없는 항목

**P2 생산 덱·결과 전 등록이 없으므로 실행 가능한 P2 발사 명령은 아직 없다.** P1 `run_unload.sh`나 세대 1 `resume_ckpt.sh`를 P2 지원처럼 제시하지 않는다. 아래 실제 값은 [기존 사실 양식](dem_gen2_t12_readiness_evidence_20261024/factual-input-form.blank.json)의 해당 칸으로 받는다. 미제공 값은 `null`/미수령으로 유지한다.

| 필요한 사실 | 받을 원본 |
| --- | --- |
| 결과 전 등록 | P2 bed/arm·seed/코호트·coverage·반복·허용 실패확률·이산 제어 자격 수치; params·활성 머리; R-a 종료/S0; h₀ 기준·환산·시간/step; 선택 케이스·재개 상태표. 문서 경로·전체 SHA-256·등록 시점 |
| 구현 신원 | 실제 producer/consumer 커밋, 생산 덱·params 파일/해시, 프로토콜/팔/침대, 실제 바이너리 해시와 MPI ranks |
| R-a 끝=S0 | 정확한 run/step, dt와 물리 시간 환산, 판/바닥 z·높이·면적·중력·압력·유효 창·힘/KE 근거; 그 시점 atom/contact/wall/mesh/restart/state·질량/상 재고·활성 fix 이력 원본 |
| 실제 자격 | 지정 빌드 이력/문법, 복원 양성·음성, 같은 물리 시간 dt/2, 서보 자격, 단계별 재개 원자료와 종료 기록 |
| 외부 판정 | ULPR 지정 핀 재검토와 세대 2 설계 판정의 실제 원문·대상 SHA·범위·미해결 한정 |

P1에서 발췌한 dt·창 길이·중력·침대명을 P2 등록값으로 복사하지 않는다. R-a/S0와 복원에 관한 합성 fixture는 로컬 구현 증거로만 기록한다. 현재 `physical_ready=false`, `T12=NOT_RUN`이다.

## 5. 이 안내의 근거

- LHS `854857e576a2a8aba07ec861dbee39d4bb59efae`: 위 §3의 고정 링크로 연결한 다시 발사 묶음 §3–5와 실제 WSL 수령표. 수령표는 별도 LHS 가지의 파일이다.
- DEM `2443a63eaa87d52e385a35f8bab4225efa0d25fe`: `docs/reviews/dem_gen2_t12_readiness_20261024.md` §1·3–5 및 위 빈 사실 양식. 기존 양식의 ULPR 참조는 이전 `8347…`임을 보존하며, 최신 소비 계약 재대조는 별도 T12 개발 산출물에 기록한다.
- ULPR 전달 대상 `01c1aaf5be8acdf7d1716f34cc86fc77d8e27362`. 해시가 같다는 사실과 외부 검토가 실제 완료됐다는 사실은 각각 확인한다.

이 안내의 셸 블록은 Bash 구문, 필수 변수 결손, 가짜 Git/Python의 rc 0·7 보존, 기존 로그 재사용 거부, 명시한 합성 파일 해시를 확인했다. 이는 안내 명령의 확인이며 실제 WSL·fast16·preflight·물리 계산의 실행 결과가 아니다.
