# REIL C6 국소 보충 — C6-N1 (충돌 예외 범위) · C6-N2 (호출 · 검증 근거) (2026-10-06 · 재실행 0 · 코드 변경 0)

> 부속 D · C6 검토 회신 (`bms-balancing/reviews/prereview_reil_v2_annexD_c6_20261006/` · `C6_SEALED_ARTIFACT_IDENTITY_ACCEPTED_FULL_CLOSEOUT_PENDING_TWO_LOCAL_SUPPLEMENTS`)
> 의 "기존 증거부터 보충" 에 답한다. 새 실행 · 설치 · 환경 재구축 · 재시험 · 자료 개봉 · 봉인 수정은 하지 않았다. 아래 사실은 고정 커밋
> `17e03fa2c149babb760550151955f1c54cd045c3` 의 바이트를 읽어 적은 것이다 (봉인 · 스크립트 · 시험은 그 뒤 바뀌지 않았다 — `git diff 17e03fa2c HEAD`
> 빈 출력). 상태 문서 `REIL_PREREQUISITES_STATUS_20261004.md` §13 이 이 문서를 가리킨다.

## 0. 고정 위치 (정적 열람을 청할 대상)

| 파일 (고정 커밋 `17e03fa2c`) | blob | 이 문서가 가리키는 줄 |
|---|---|---|
| `bms-balancing/scripts/reil_c6_profile.py` | `513a6d736874b95a10d34f648d2d3443fdf6f9a8` (sha256 `17b547f783c055a985d9ad2c4f10768c6d4ecc360f3b8592885988348b219a39`) | 32–33 (`COBYQA_OPTIONS`) · 61–82 (`record_index` · `classify_record_mismatches`) · 89–103 (lock 생성) · 121–154 (`cobyqa_options`) |
| `bms-balancing/tests/test_reil_c6_profile.py` | `2c6556460375c228568cff0e986c9e0d26b160be` | 20–42 (충돌 분류 네 경우) |
| `bms-balancing/scripts/reil_c6_mutation_proof.py` | `f252a9305ecb7ee134f39f4753c3d304a392c363` | 57 · 131 (`lock_collision_line` 변이) |

## 1. C6-N1 — 충돌 예외: 구현은 문서와 **같은 넓이**다 (더 좁지 않다)

### 1-1. 사실

- 구현 (`classify_record_mismatches` · 줄 78): `rel.startswith("../") and disk` — RECORD 경로가 `../` 로 시작하고, 다른 배포판의 RECORD 가 같은 경로를
  주장하며 그 해시가 디스크 해시와 같으면 **어떤 파일이든** 설명된 충돌로 통과한다. 파일 이름 · 위치 · 배포판 · 판에 대한 제한은 없다.
- 따라서 회신의 반례 (`../../../bin/tool` 을 두 배포판이 다른 해시로 주장 · 디스크가 두 번째와 같음) 는 **현 구현에서도 통과한다**. 회신은 문서
  조건의 논리 반례로 냈고, 코드 읽기로 그 넓이가 구현에도 그대로임을 확인했다 (실행 재현은 아니다).
- 시험 네 경우 (줄 20–42) 는 "site-packages 안이면 fatal" · "다른 주장자 없음 fatal" · "디스크가 어느 주장자와도 다름 fatal" 과 LICENSE 통과 하나만
  잰다 — 밖 경로의 **종류**를 묻는 경우는 없다.

### 1-2. 실제로 기록된 한 건 (봉인 안의 결속)

| 항목 | 값 | 봉인 위치 |
|---|---|---|
| 정규화 위치 | `../../../LICENSE` (venv 꼭대기 · RECORD 상대 경로 그대로) | `REIL_C6.lock.txt` 10 행 `#@ collision` |
| 배포판 · 판 | `about-time==4.2.1` (덮인 쪽 · `dist`) · `alive-progress==3.3.0` (디스크 쪽 · `disk_matches`) | 같은 줄 + 13 · 14 행 |
| 두 RECORD 파일 | sha256 `e5a630322aead38c00d7d20ca0050eb7cd2024eb035505a6ef7bab8e5329f0bd` (about-time) · `00c80da0799ae100798d538d9946e030259eae3b2b39cb70f99e7ff6ac7e9be8` (alive-progress) | 13 · 14 행 `# record-sha256` |
| 집계 | `mismatches 1 · explained_collisions 1` | 9 행 `#@ files` |

**적혀 있지 않은 것 (신고):** 그 LICENSE 의 두 expected 해시 (각 RECORD 행의 값) 와 실제 디스크 해시는 lock 에 **값으로 없다**. 두 RECORD 파일의
sha256 이 봉인돼 있으므로 그 값은 **결정돼 있지만** 그 RECORD 파일 자체는 venv 와 함께 사라졌다 (C6 컨테이너 소멸). 지금 꺼내려면 같은 판 wheel 을
다시 받아 RECORD 를 읽어야 하고, 그것은 이번 범위 (재구축 · 설치 0) 밖이다.

### 1-3. 좁힌 예외 계약 (제안 — 구현 변경은 사용자 승인 뒤)

허용 목록 하나 (정확 일치만 통과 · 나머지 RECORD 불일치는 전부 fatal):

| 키 | 값 |
|---|---|
| `path` | `../../../LICENSE` (문자열 정확 일치 — 정규화 뒤 venv 꼭대기 바로 아래 · `bin/` · `share/` · `include/` · 실행 진입점 · venv 밖 해석 · `..` 이 더 많은 경로 모두 불허) |
| 배포판 쌍 | {`about-time` 4.2.1 (덮인 쪽) · `alive-progress` 3.3.0 (디스크 쪽)} — 이름 · 판 · 방향 모두 |
| RECORD 결속 | 두 배포판의 RECORD 파일 sha256 = 위 두 값 (판이 같아도 RECORD 가 다르면 fatal) |
| 해시 결속 | 덮인 쪽 expected · 디스크 쪽 expected · 실제 디스크 해시 셋을 lock 의 `#@ collision` 줄에 **값으로** 적는다 · 실제 = 디스크 쪽 expected |
| 그 밖 | 경로가 밖이라는 것 · 다른 소유자 RECORD 가 맞는다는 것만으로는 통과 없음. 새 충돌이 나오면 봉인 거부 → 사람 판단 → 허용 목록 개정은 새 등록 |

- 구현 범위 (승인되면): `classify_record_mismatches` 를 허용 목록 대조로 바꾸고 RED 시험 둘 (`../../../bin/tool` 반례 · 같은 LICENSE 를 다른 판 / 다른
  RECORD sha 로) 을 먼저 실패로 본 뒤 고친다. 순수 함수라 venv · 자료 없이 시험된다. **이미 만든 봉인 10 파일은 바꾸지 않는다** — lock 의 collision
  줄 형식이 바뀌면 그것은 같은 판 재구축 단계 (P0 승인 범위) 의 새 emit 에서 새 식별로 나온다.
- 지금 봉인을 실패 · 변조로 재분류하지 않는다 (회신 그대로). 이 계약은 C6 검사를 **다시 쓸 때**의 수용 조건이다.

## 2. C6-N2 — 호출 · 검증 근거

### 2-1. 실행 원문: **미보존** (신고)

- `bms-balancing/reil_c6_20261005/C6_RUN.log` 는 README (26 · 62 행) 와 상태 문서 §10 이 가리키지만 **커밋된 적이 없다** — 루트 `.gitignore` 3 행
  `*.log` 가 걸러냈다 (`git check-ignore -v` 실측 · `git log --all -- …/C6_RUN.log` 빈 출력). 그 로그를 쓴 컨테이너는 2026-10-05 서브 세션 종료로
  사라졌다. 85차 게이트에서 같은 원인 (`*.log` 무시 → `git add -f`) 을 배웠는데 이 봉인 커밋에서 되풀이했다.
- 같은 이유로 emit / check · `git archive` 대조 · 변이 12 · 시험 9 · 전체 538 의 **원문 출력 · rc 는 저장소 어디에도 없다**. 남은 것은 커밋 메시지
  (`bdc6b1e72` · `cdec0e646`) 와 상태 문서 §10 의 문장뿐이다 → 9 · 12 · 538 은 **제출자 보고**로 낮춘다 (회신의 구분 그대로). 재실행으로 대신 만들지
  않는다.
- 봉인 README 는 봉인 밖 사람용 기록이지만 바이트를 고치지 않는다 — "`C6_RUN.log` 에 경위" 라는 문장의 정정은 이 문서와 상태 문서 §13 에 둔다.

### 2-2. 옵션 전달 — 남은 근거는 코드뿐이다

- `COBYQA_OPTIONS.json` 의 `options.<이름>.planned` 는 **계획값의 repr** 이고, `synthetic_call` 은 `success` · 경고 목록 · 근사 결과 boolean 만 담는다.
  실제 호출에 넘긴 dict 나 `OptimizeResult` 원문은 기록하지 않았다 — 회신 지적 그대로, 이 JSON 만으로는 8 개 모두 명시 전달을 독립 확인할 수 없다.
- 코드 (줄 32–33 · 128 · 142–143): 표를 만드는 상수 `COBYQA_OPTIONS` 와 호출의 `options=dict(COBYQA_OPTIONS)` 가 **같은 객체에서** 나온다 — 표의 8
  개 이름 · 값이 그대로 호출에 들어간다는 것이 이 정적 구조의 주장이다. 단 이것은 "넘겼다" 까지이고 "SciPy 가 각 값을 실제로 썼다" 는 아니다:
  - `disp=False` · `f_target=-inf` · 4 차원의 `maxfev=2000` · `maxiter=4000` 은 문서상 기본값과 겹친다 → 경고 0 · 성공만으로는 구별되지 않는다.
  - 제약 없는 상자 이차 함수는 `feasibility_tol` 의 효과를 드러내지 않는다.
  - 기록한 것은 SciPy 안 cobyqa 구현 파일 4 개의 sha256 (전달 경로의 바이트 식별) 이지 값별 사용의 관측이 아니다.
- 제안: **좁은 정적 열람 허용** — `reil_c6_profile.py` (blob `513a6d73…`) 줄 32–33 · 121–154 만 (호출부 · 결과 생성부). 값별 사용의 관측 (예: 옵션마다
  기본값과 다른 값을 줘 결과가 갈리는지) 은 새 실행이라 이번 범위 밖 — 필요하면 같은 판 재구축 단계 (P0 승인 범위) 의 항목으로 따로 제안한다.

## 3. 그대로 두는 것 · 확대하지 않는 것 (회신 §4 수용)

- `unhashed=5301` 은 내용 검증이 아니다 · `build_dependencies` 는 빌드 메타데이터지 로딩 환경 관측이 아니다 · 버전 + RECORD 식별은 모든 플랫폼의 동일성이
  아니다 · 변이 12 는 유한 사례다 · checker 와 환경이 함께 바뀐 자기일관 재작성은 고정 커밋 · 기대 MANIFEST 를 밖에 둬야 잡힌다.
- Sobol `rng=` 고정 · 배열 sha256 = 식별 · 정식 봉인은 맞춤 전 같은 판 재생성 대조 — 수용된 경계 그대로.

## 4. 다음

1. 이 보충을 Codex 에 보낸다 (발송은 사용자) — 물음: (a) §1-3 의 좁힌 계약이 C6-N1 종결 조건을 채우는가 · 구현 변경을 C6 종결 전에 해야 하는가 아니면
   같은 판 재구축 단계 전까지면 되는가 (b) §2 의 미보존 신고 + 좁은 정적 열람으로 C6-N2 가 닫히는가.
2. §1-3 구현 (RED 둘 → 허용 목록) 은 **사용자 승인 뒤**에만.
3. C6 이 수용되면 N3 — P0 의 범위 · 예산 · 중단 조건을 사용자에게 따로 요청. 그 전 자료 개봉 · 재구축 · 맞춤 0.

## 5. 덧붙임 — §1-3 허용 목록 구현 (2026-10-06 · 사용자 "권고 사항으로 해줘" · 상태 문서 §14)

위 §0–§4 는 고치지 않는다 (§1-1 의 "구현은 문서와 같은 넓이" 는 고정 커밋 `17e03fa2c` 기준 사실로 남는다).

- **고친 곳:** `bms-balancing/scripts/reil_c6_profile.py` — `EXPLAINED_COLLISIONS` (허용 목록 한 항목 = §1-2 의 위치 · 배포판 쌍 · 판 · RECORD 파일
  sha256 · 방향) · `classify_record_mismatches(mismatches, index, dists=None)` 가 그 목록과 **정확 일치**할 때만 통과 (주장자는 정확히 둘 · 디스크 해시
  = 디스크 쪽 RECORD 값 · `dists` 가 없으면 전부 fatal) · 통과한 충돌은 `covered` / `disk_owner` 의 판 · RECORD sha · expected 해시와 실제 `disk` 해시를
  lock 의 `#@ collision` 줄에 **값으로** 남긴다 · 호출부 하나 (`lock_text`) 가 `dists=prof["dists"]` 를 넘긴다.
- **RED → GREEN:** `bms-balancing/tests/test_reil_c6_profile.py` 에 11 을 더했다 (양성 1 은 기대 출력을 바꿨다 · bms 전체 기대 수 538 → 549). 고치기 전 **12 failed / 8 passed** —
  실제 결함 2 (`../../../bin/tool` 반례를 2 인자 호출에서 설명된 충돌로 통과 · 판 · RECORD 없이 LICENSE 통과) + 새 인자 부재 `TypeError` 10 (무관 예외로
  따로 센다). 고친 뒤 **20 passed**. 반례 범위: 실행 파일 · 판 넷 (덮인 쪽 / 디스크 쪽 × 판 / RECORD) · 방향 뒤바뀜 · 경로 철자 셋 (`../../` · `../../../../`
  · `LICENSE.txt`) · 셋째 주장자.
- **바뀌지 않은 것:** 봉인 `reil_c6_20261005/` 10 파일 · README · 변이 증명 스크립트 (venv 가 없어 실행하지 않았다). 새 lock 형식 (해시 값이 든 collision
  줄) 은 같은 판 재구축 단계의 새 emit 에서 **새 식별**로 나온다 — 그때 `check` 는 옛 봉인과 다르다고 말할 것이고, 그것은 판 이동이 아니라 형식 변경이다
  (옛 봉인을 덮지 않고 새 봉인을 따로 만든다).
- 이 구현으로 §4 의 물음 1 은 "좁힌 계약이 맞는가 · **구현이 그 계약과 같은가**" 로 바뀐다.
