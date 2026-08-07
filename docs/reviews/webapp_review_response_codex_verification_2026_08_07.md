# DFT Web Dashboard 대응 보고서 — Codex 재검증

- 검증일: 2026-08-07
- 검증 대상: `docs/reviews/webapp_review_response_2026_08_07.md`
- 대상 대응 커밋: `f2cf68c7`, `8c23a6da`
- 검증 환경: Windows PowerShell + WSL/Linux 교차검증
- 판정: **대부분 유효하지만 완료 판정에는 중요한 반박 3건이 있다.**

## 1. Git 동기화

`origin/claude/friendly-meitner-lldvar`를 fetch한 뒤 현재 Codex 브랜치에 rebase했다.

- 현재 브랜치: `Codex/friendly-meitner-lldvar`
- 현재 HEAD: `8c23a6da30babf17b9b9b5735f0e0ff80cb76d88`
- Claude 원격 대비: `0 ahead / 0 behind`
- Codex 원격 대비: `2 ahead / 0 behind`
- rebase 충돌: 없음
- 검증 종료 시 작업 트리: 깨끗함

## 2. §7 재현 명령

보고서에 적힌 다음 세 명령을 Windows PowerShell에서 그대로 실행했다.

```bash
python3 tools/db/validate_canonical.py --show
python3 webapp/tests/test_webapp.py
python3 -m compileall -q webapp/
```

세 명령 모두 동일하게 실패했다.

```text
python3 : 'python3' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는
프로그램 이름으로 인식되지 않습니다.
```

즉 §7 명령 블록은 현재 Windows 전용 worktree에서 그대로 재현되지 않는다.

### 2.1 Windows 동등 명령

Windows에 설치된 `python`을 쓰고 UTF-8 모드를 강제해 다시 실행했다.

```powershell
python -X utf8 tools/db/validate_canonical.py --show
python -X utf8 webapp/tests/test_webapp.py
python -X utf8 -m compileall -q webapp/
```

결과:

| 검사 | 결과 |
|---|---|
| canonical validator | 통과 — 27항목, 출처 배선 22/27, 대조 실패 0 |
| webapp 회귀 테스트 | **14/15 통과** |
| compileall | 통과 |

`-X utf8` 없이 validator를 실행하면 `⚠` 문자 출력에서 Windows 기본 CP949
`UnicodeEncodeError`가 난다. 따라서 Windows용 재현 명령에는 실행명과 콘솔 인코딩을
둘 다 반영해야 한다.

### 2.2 Windows 코멘트 동시성 반례

실패한 테스트는 다음과 같다.

```text
test_comment_writes_survive_concurrency
24 요청 중 16건만 저장
```

원인은 `webapp/data.py:3127-3146`에 있다. Windows에서는 `fcntl`을 import할 수 없고,
이 경우 파일을 열기만 한 뒤 실제 잠금 없이 임계구역으로 들어간다.

- 구현: `webapp/data.py:3127-3146`
- 회귀 테스트: `webapp/tests/test_webapp.py:169-186`

반면 WSL/Linux에서 같은 저장 함수에 100개 프로세스를 동시에 걸면 다음과 같이 통과했다.

```text
REQUESTS 100 OK 100 SAVED_DELTA 100 UNIQUE_IDS 100
```

따라서 `fcntl.flock` 수정은 Render의 단일 Linux 인스턴스에는 유효하다. 다만
“테스트 15개 전부 통과”는 플랫폼 한정 주장이어야 하고, Windows 로컬 쓰기는 아직
다중 프로세스 안전하지 않다.

## 3. §6 확인 요청

### 3.1 Windows 실기 업로드 → 개념 첨부 조회

실제 Windows Flask test client로 다음 흐름을 실행했다.

1. 임시 개념 문서 생성
2. `/api/concept-upload/<cid>`에 CSV 업로드
3. `concept_attachments()`로 첨부 재수집
4. `/concept/<cid>` 렌더 확인
5. `/api/file/<rel>`로 파일 본문 조회
6. Codex가 만든 probe 파일만 제거

결과:

```text
UPLOAD_STATUS 200
REL docs/uploads/codex_windows_upload_probe/codex-windows-path-probe.csv
HAS_BACKSLASH False
CONCEPT_STATUS 200
CONCEPT_HAS_REL True
FILE_STATUS 200
FILE_BYTES_OK True
```

판정: **통과.** Windows에서도 저장 경로가 `docs/uploads/...` POSIX 형식으로 반환되고,
개념 첨부 수집·페이지 렌더·파일 조회가 모두 정상 동작한다.

근거 코드:

- 업로드 저장과 문서 경로 기록: `webapp/data.py:2755-2799`
- 첨부 재수집과 `.as_posix()`: `webapp/data.py:2611-2642`
- 파일 조회와 업로드 API: `webapp/app.py:398-421`

### 3.2 `ICOHP_PS` comp1: −5.938 vs −5.944

판정: **−5.938이 정본이다.** 직접 산출 JSON의 원값은 `−5.9381`이다.

```text
db/properties/per_bond_json/bonds_comp1_k444.json:38
P-S.icohp_eV = -5.9381
```

`−5.944`는 더 오래된 요약 파일과 이를 복사한 Nd 비교표에 남아 있다.

- `db/properties/bonds.json:129` — `−5.944`
- `db/properties/nd_icohp.json:118` — `−5.944`

Git 이력상 `−5.944` 요약은 2026-06-03에 들어왔고, 동일 분석 도구의 직접 one-shot
출력 `−5.9381`은 2026-06-05에 추가됐다. 두 자료 모두 k444/4.0 Å 계열을 주장하므로,
차이를 cutoff 규약으로 설명할 근거는 부족하다. **오래된 요약값 drift**로 보는 게 맞다.

검증된 레지스트리 배선 후보:

```text
source_path: db/properties/per_bond_json/bonds_comp1_k444.json
source_key:  /icohp_per_bond_type_eV/P-S/icohp_eV
resolved:    -5.9381
```

레지스트리 표시는 세 자리 반올림값 `−5.938`을 유지할 수 있다.

### 3.3 comp2 gap·ICOHP 원 출처

#### `ICOHP_PS = −5.913`

다음 배선으로 resolver가 정확히 `−5.913`을 읽는다.

```text
source_path: db/properties/comp2_icohp_origin.csv
source_key:  /[?bond=P-S]/ICOHP_eV_mean
resolved:    -5.913
```

근거 원자료는 `db/properties/comp2_icohp_origin.csv:2`다. 계산 방법과 결합 수는
`db/compositions/comp2.json:290-317`에도 기록돼 있다.

#### `gap_eV = 2.04`

기존 값의 출처는 다음과 같이 배선할 수 있다.

```text
source_path: db/properties/electronic.json
source_key:  /band_gaps/[?id=comp2]/gap_eV
resolved:    2.04
```

하지만 `db/properties/electronic.json:13-17`이 명시하듯 이 값은 legacy DOS-threshold
판독값이다. `db/compositions/comp2.json:35-37`도 fixed-occ 재검증 대기라고 적고 있다.

판정:

- legacy 값의 provenance 배선은 가능
- fixed-occupation nscf 고유값 정본으로 승격은 불가
- `gap-fixedocc-eigenvalue-v1` 비교 묶음에는 넣으면 안 됨
- comp2 fixed-occ nscf를 새로 계산하기 전까지 자동순위·레이더에서 제외해야 함

### 3.4 3-seed/4-seed 동일 group

시드 수만 다르고 다음 조건이 같으므로, 3-seed와 4-seed를 같은 프로토콜 group에 두는
원칙 자체에는 동의한다.

- UMA-s-1p1(omat)
- 600/800/1000 K
- MSD 2–50 ps
- 온도별 시드 평균 → Arrhenius 적합
- Nernst–Einstein, Haven=1
- `n_seed`와 uncertainty를 별도 표시

다만 LPSOCl을 현재 `status: canonical`로 둔 것은 반박된다.

- 레지스트리 canonical 지정: `db/properties/canonical_registry.json:170-178`
- LPSOCl 600 K 게이트 실패: `db/properties/msd_3sys_200ps_origin.csv:9-16`
- β=0.61 및 인용 보류 판정: `kb/open_items.md:17-24`

LPSOCl 600 K는 4시드 앙상블 평균에서도 `β=0.615 < 0.8`이다. 현재 `Ea=0.2867 eV`는
이 실패한 온도점을 포함한 3점 적합이므로 canonical 판정에 쓸 수 없다.

현재 `test_md_ea_groups_are_separated()`는 `n_seed >= 3`만 확인한다
(`webapp/tests/test_webapp.py:52-61`). 따라서 β 게이트 실패를 잡지 못하면서 테스트는
통과하는 false positive다.

권장 판정:

- modelc·B₂O₃: `md-ea-multiseed-v1` canonical 유지 가능
- LPSOCl: 같은 protocol group은 유지할 수 있지만, 600 K 게이트 해결 전까지
  `provisional` 또는 인용 보류
- canonical MD 테스트에 온도별 앙상블 β 게이트를 추가

## 4. 추가 반박 — “원자료 한 곳만 고치면 화면 갱신”

이 주장은 절반만 맞다.

화면은 `source_path/source_key`를 resolve한 값을 직접 쓰지 않고, 레지스트리에 복제된
`value`를 읽는다.

- 화면용 값 구성: `webapp/data.py:338-350`
- `canonical_map()`이 `entry["value"]` 반환: `webapp/canonical.py:138-144`
- 원자료 resolve는 별도 validator에서만 수행: `webapp/canonical.py:101-122`

따라서:

- 레지스트리만 고치면 화면은 갱신되지만 원자료 대조가 실패한다.
- 원자료만 고치면 화면은 그대로고 validator만 실패한다.

이번 수정의 정확한 성과는 **숫자 이중화를 제거한 것**이 아니라,
`data.py`의 숨은 정본을 DB 레지스트리로 옮기고 **원자료 drift를 실패로 드러내게 만든 것**이다.
이전보다 훨씬 안전하지만, “원자료 한 곳만 수정하면 자동 갱신”까지 달성한 구조는 아니다.

## 5. 최종 판정

| 항목 | 판정 |
|---|---|
| canonical 원자료 대조 | ✅ 배선 22/27, 불일치 0 |
| compare/radar protocol 분리 | ✅ 기본 구현 유효 |
| 공개 mutation 잠금 | ✅ 기본 403 |
| Markdown URL 방어 | ✅ 회귀 테스트 통과 |
| Windows 업로드·POSIX 경로 | ✅ 실기 통과 |
| Linux 코멘트 동시성 | ✅ 100/100 |
| Windows 코멘트 동시성 | ⛔ 24요청 중 16저장 |
| comp1 ICOHP 정본 | ✅ −5.938 (`−5.9381` 반올림) |
| comp2 ICOHP 출처 | ✅ 배선 가능 |
| comp2 gap 출처 | 🟡 legacy 출처만 배선 가능, fixed-occ 정본 없음 |
| LPSOCl Ea canonical | ⛔ 600 K β 게이트 실패로 인용 보류 |
| §7 Windows 재현성 | ⛔ `python3` 실행명·CP949 문제 |
| “원자료 한 곳 수정” | 🟡 화면 정본은 단일화됐지만 원자료와 값 복제는 남음 |

핵심 수정 우선순위는 다음 세 가지다.

1. LPSOCl `MD_Ea_eV`를 canonical에서 내리고 β 게이트 메타데이터·회귀 검사를 추가
2. Windows 코멘트 잠금을 `msvcrt`/portalocker/SQLite 중 하나로 구현
3. Windows용 검증 명령을 `py -3 -X utf8 ...` 형태로 함께 제공
