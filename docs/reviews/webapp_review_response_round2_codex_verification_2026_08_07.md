# DFT Web Dashboard 대응 보고서 — 2라운드 Codex 실제 검증

- 대상: `docs/reviews/webapp_review_response_round2_2026_08_07.md`
- 검증 기준: `origin/claude/friendly-meitner-lldvar` `a59918e6` 포함
- 검증 환경: Windows, Python 3.14 (`py -3`)
- 판정: **수정 방향은 타당하지만 완료 조건은 아직 미달**

## 1. 요약

| 항목 | 판정 | 실제 결과 |
|---|---|---|
| Windows `msvcrt.locking` 24건 | ✅ 통과 | 24/24 저장, ID 24/24 고유 |
| Windows 100건 스트레스 | ⛔ 간헐 실패 | 10회 중 6회 실패, 합계 992/1000 저장 |
| drift 새 프로세스 반영 + validator 실패 | ✅ 통과 | 2.9999 반영, `unreviewed_drift`, validator 1건 실패 |
| 실행 중 프로세스의 drift 재반영 | ⛔ 실패 | 원자료 3.1111을 읽어도 화면 번들은 2.9999 유지 |
| drift의 순위·비교차트·레이더 제외 | ✅ 통과 | `status == canonical` 조건으로 제외 |
| drift의 비교표·Explorer·조성 카드 처리 | 🟡 불완전 | 값은 표시되며 drift 배지가 없음; Explorer 정렬·인용에도 남음 |
| 원자료 resolve 실패 시 자동판정 제외 | ⛔ 실패 | stale 값이 `canonical` 상태와 순위에 남음 |
| `test_source_edit_propagates_to_screen` 화면 검증 | ⛔ 실패 | 실제 Flask 화면을 검사하지 않음 |
| 위 테스트의 중단 안전성 | ⛔ 실패 | hard kill 시 정본 파일과 `.testbak`이 남을 수 있음 |
| `mkdir` stale lock 복구 | ⛔ 실패 | timeout 뒤 `TimeoutError`; PID/TTL 복구 없음 |
| `−5.944`의 다른 화면 사용 | 🟡 확인 | Nd-doped 조성 비교표가 아직 `−5.944` 표시 |
| comp1 단일시드 Ea 출처 | ✅ 발견 | `li_transport.json`의 4fu natural `Ea_eV = 0.2532` |

## 2. Windows 코멘트 동시 저장

### 2.1 공식 24건 테스트

`test_comment_writes_survive_concurrency()`는 6개 프로세스에서 24건을 쓴다
(`webapp/tests/test_webapp.py:217-239`). Windows에서 실제 `msvcrt` 경로로 실행한 결과:

```text
ok=24/24
saved=24/24
unique_ids=24/24
errors=0
```

전체 테스트도 17개 모두 통과했다.

### 2.2 격리된 100건 스트레스

tracked `db/file_comments.json` 대신 프로세스마다 같은 임시 `COMMENTS_PATH`를 주입했다.
12개 프로세스 × 100건을 10회 반복한 결과:

```text
통과한 run: 4/10
실패한 run: 6/10
저장 합계: 992/1000
실패 run별 저장: 98 또는 99/100
공통 예외: PermissionError [WinError 5] ... os.replace(tmp, COMMENTS_PATH)
```

별도 임계구역 중첩 프로브에서는 `max_simultaneous_critical_sections=1`이었다. 따라서
`msvcrt.locking` 자체는 앱 프로세스를 직렬화했다. 현재 유실은 `_save_comments()`의
`os.replace()`가 Windows의 일시적 대상 파일 점유를 재시도하지 않는 경로에서 발생한다
(`webapp/data.py:3105-3111`). Microsoft/Python 문서도 `msvcrt.locking`이 현재 파일 위치부터
지정 byte 범위를 잠그는 API임을 명시한다. 이 락은 별도 `.lock` 파일에만 걸리므로 JSON
대상 파일을 잠깐 여는 백신·인덱서 같은 외부 handle까지 막지는 않는다.

권장 수정:

1. Windows `PermissionError`/`EACCES`에 한해 `os.replace()`를 짧은 backoff로 제한 재시도한다.
2. 100건 반복 스트레스를 테스트에 추가한다. 24건 1회는 이번 간헐 실패를 못 잡았다.
3. 쓰기 빈도·배포 규모가 커지면 JSON read-modify-write 대신 SQLite WAL로 옮긴다.

## 3. `load_registry(live=True)`와 실제 화면

tracked 원자료를 바꾸지 않고 `canonical.resolve()`만 fixture로 대체했다.

### 3.1 새 프로세스 시작 시

LPSOCl gap 원자료를 2.9999로 반환하게 한 뒤 `data.py`를 새로 import했다.

```text
fresh_data_value=2.9999
fresh_status=unreviewed_drift
fresh_validator_errors=1
fresh_screen_bundle_value=2.9999
fresh_ranking_includes_lpsocl=False
```

이 경로는 회답 주장대로 동작한다. `canonical.py:125-133`이 원자료 값을 채택하고 status를
`unreviewed_drift`로 내리며, `canonical.py:150-155`가 validator 실패를 만든다.

### 3.2 실행 중인 프로세스에서 원자료가 다시 바뀔 때

같은 프로세스에서 resolver 값을 3.1111로 바꿨다.

```text
later_registry_value=3.1111
later_registry_status=unreviewed_drift
running_data_value=2.9999
running_screen_bundle_value=2.9999
```

원인은 `data.py:338-350`이 `_REG`, `CANONICAL`, `CANONICAL_ENTRY`를 module import 때 한 번만
만드는 구조이기 때문이다. `/compare`도 요청마다 reload하지 않고 이 전역 번들을 전달한다
(`webapp/app.py:232-250`). 따라서 현재 `live=True`는 **프로세스 시작 시 live resolve**이지
**실행 중 화면의 live update**는 아니다. 배포 재시작 뒤에는 반영되지만, 장기 실행 worker는
원자료 수정만으로 갱신되지 않는다.

### 3.3 현재 테스트 이름은 실제 검증 범위를 과장한다

`test_source_edit_propagates_to_screen()`은 `C.load_registry()`, `C.canonical_map()`,
`C.validate()`만 검사한다(`webapp/tests/test_webapp.py:100-107`). `D.CANONICAL`, Flask test
client, `/compare`, `/composition`, `/explorer`는 검사하지 않는다. 따라서 현재 테스트는
“registry propagation” 테스트이지 “screen propagation” 테스트가 아니다.

권장 수정:

- registry/source 경로를 주입할 수 있게 만들고 임시 source fixture를 사용한다.
- fresh-process/import 경로와 long-running-process 경로를 별도 테스트로 나눈다.
- “즉시 갱신”이 요구사항이면 요청별 mtime 캐시 reload 또는 명시적 reload endpoint가 필요하다.
  재시작 반영만 요구사항이면 문구를 그 수준으로 낮춘다.

## 4. 실제 정본 파일 수정 테스트의 격리 위험

현재 테스트는 다음 순서다.

1. 실제 `db/properties/lpsocl_dos_gap.json`을 옆의 `.testbak`으로 복사
2. 실제 정본 파일을 2.9999로 덮어쓰기
3. `finally`에서 `.testbak`을 원래 파일로 이동

근거는 `webapp/tests/test_webapp.py:91-109`다. 정상 종료와 일반 예외에서는 복구된다. 실제
전체 테스트 뒤 source hash와 HEAD hash도 모두
`be905ce384a9782edd183da19e6371dd7fdc8c31`로 일치했고 `.testbak`은 없었다.

하지만 `os._exit`, Task Manager 종료, 전원 손실처럼 `finally`를 실행하지 않는 중단에서는
정본이 2.9999인 채 남는다. 다음 테스트가 시작되면 `shutil.copy(p, bak)`가 기존 backup을
덮어쓸 수도 있어 복구 기준까지 잃을 수 있다. **중단 안전성은 없다.** 사용자가 제안한 임시
source fixture가 맞다.

## 5. `unreviewed_drift`의 화면·자동판정 범위

### 5.1 제외되는 곳

- Python 순위/대시보드: `canonical_comparable()`이 기본 status를 `canonical`로 제한
  (`webapp/data.py:359-371`, `webapp/data.py:2398-2405`).
- 비교 막대차트: `splitByGroup()`이 `m.status === 'canonical'`만 유지
  (`webapp/templates/compare.html:41-56`, `87-111`).
- 레이더: 위 필터를 축마다 다시 사용
  (`webapp/templates/compare.html:113-140`).

fixture에서 LPSOCl drift를 넣었을 때 gap 순위에서 빠졌고, 대시보드 최고값도 LPSOCl
2.9999가 아니라 modelc 2.099였다.

### 5.2 남는 곳

`CANONICAL` union은 status와 무관하게 값이 있는 모든 entry를 넣는다
(`webapp/data.py:344-350`). 따라서 drift 값은 다음에 남는다.

- `/compare` 숫자 표: drift status가 아니라 hard-coded `PROV`만 배지로 확인
  (`webapp/templates/compare.html:67-75`).
- `/explorer` 표: 값이 표시되고 정렬·인용 복사 대상이며, 역시 `PROV`만 배지로 확인
  (`webapp/templates/explorer.html:56-75`, `113-140`).
- `/composition/<cid>` 상단 카드: 값이 표시되며 `CANONICAL_PROVISIONAL`에 없으면 경고 없음
  (`webapp/templates/composition.html:19-31`).

실측 fixture:

```text
fresh_composition_card_value=2.9999
fresh_has_visible_provisional_badge=False
```

즉 “순위·차트·레이더 자동판정 제외”는 맞지만 “표·카드·Explorer까지 미검토 상태를 명확히
표시한다”는 아직 아니다. 표에서 값을 숨길 필요까지는 없지만 최소한 `미검토 drift` 배지,
정렬/인용 제외 또는 명시적 opt-in이 필요하다.

### 5.3 더 위험한 `resolve_error` 경로

원자료 resolve를 강제로 실패시킨 격리 프로브 결과:

```text
broken_source_status=canonical
broken_source_stale_value=2.066
broken_source_validator_errors=1
broken_source_in_ranking=True
```

`canonical.py:117-121`은 `resolve_error`만 기록하고 기존 status/value를 유지한다. validator는
실패하지만(`canonical.py:156-158`), 화면 순위는 validator를 실행하지 않으므로 stale 값을
계속 canonical로 사용한다. 이 항목은 `source_error` 같은 비정본 status로 내려 자동판정에서
반드시 빼야 한다.

## 6. `mkdir` 폴백의 stale lock

`fcntl`과 `msvcrt`를 사용할 수 없게 한 뒤 `.lock.d`를 미리 남겨 실행했다.

```text
stale_recovered=False
error=코멘트 락을 못 잡았다 (mkdir 폴백)
```

코드는 디렉터리가 있으면 timeout까지 재시도한 뒤 실패할 뿐이다
(`webapp/data.py:3188-3197`). 생성자 PID, 시작시각, TTL, process-alive 확인이 없어서
프로세스가 죽어 남긴 stale 디렉터리를 스스로 복구할 수 없다. 예외 종료가 `finally`에 도달하면
지우지만 hard kill에는 대응하지 못한다(`webapp/data.py:3199-3205`).

권장 수정은 lock 디렉터리에 owner metadata를 원자적으로 기록하고, 충분히 오래된 lock에 대해
PID 생존 여부를 확인한 뒤에만 회수하는 것이다. 더 단순한 선택은 검증된 cross-platform file
lock 또는 SQLite로 폴백 자체를 없애는 것이다.

## 7. §8 요청 2 — `−5.944` 사용처

실제 데이터층 호출 결과:

```text
icohp_for('comp1')['bonds']['P-S']
  → {'icohp_eV': -5.9381, 'n_bonds': 16}

icohp_for('modelc_nd_doped')['_comparison']['P-S']
  → {'comp1': -5.944, 'modelc': -6.0, 'nd': -5.976, ...}
```

comp1 본딩 페이지는 최신 직접 산출
`db/properties/per_bond_json/bonds_comp1_k444.json:38`을 쓴다. 그러나 Nd-doped 페이지는
`_PREFIX['modelc_nd_doped'] = ['modelc_nd', 'nd_']`와 `*_icohp.json` 후보 탐색
(`webapp/data.py:171-174`, `721-766`) 때문에 `nd_icohp.json`을 읽고, 그 비교 블록의
comp1 `−5.944`를 실제 화면에 표시한다(`db/properties/nd_icohp.json:116-121`).

`bonds.json:124-130`에도 `−5.944`가 남아 있고 구형 figure script/CSV가 이를 사용한다.
현재 comp1 본딩 카드의 직접 원천은 아니지만, 파일 갤러리·문서·재생성 그림에서는 drift가
계속 전파될 수 있다. 두 요약과 파생 figure CSV를 최신 직접 산출 `−5.9381`로 동기화하고,
옛 값이 필요한 경우 `superseded` provenance로 분리하는 편이 맞다.

## 8. §8 요청 3 — `MD_Ea_eV_singleseed` / comp1 원 출처

로컬에서 가장 직접적인 배선 대상은 다음이다.

```json
{
  "source_path": "db/properties/li_transport.json",
  "source_key": "/results/[?id=comp1_v3_4fu_natural]/arrhenius_fit/PAPER_GRADE/Ea_eV"
}
```

resolver 실측값은 `0.2532`다. 근거:

- 항목 ID와 primary 표기: `db/properties/li_transport.json:139-146`
- 600/800/1000 K D: `db/properties/li_transport.json:151-163`
- `Ea_eV = 0.2532`, window 2–50 ps: `db/properties/li_transport.json:165-177`
- 원 궤적 위치: `gabia:/data/work/runs/mlmd_4fu_comp1/`
  (`db/properties/li_transport.json:146`)

다만 **출처 발견과 canonical 승격은 별개**다. 같은 파일은 comp1의 diffusive gate 미통과와
Ea 인용 보류를 명시한다(`db/properties/li_transport.json:317`). `kb/open_items.md:8-15`도
comp1 6/6 β 탈락을 기록한다. 따라서 source는 배선하되 `source_pending → canonical`로 바로
올리면 안 된다. 최소 `provisional`/`blocking_gate`로 유지하고, legacy 단일시드 deck anchor
용도만 허용해야 한다.

## 9. 재현 명령 결과

```powershell
py -3 -X utf8 tools/db/validate_canonical.py --show
# 항목 27 · canonical 23 · provisional 3 · source_pending 1
# 출처 배선 25/27 · 대조 실패 0 · exit 0

py -3 -X utf8 webapp/tests/test_webapp.py
# 17개 통과 (공식 24건 동시성 테스트 포함)

py -3 -m compileall -q webapp/
# exit 0
```

정상 테스트 종료 뒤 `lpsocl_dos_gap.json`과 `file_comments.json`의 content hash는 각각 HEAD와
일치했다. 검증용 임시 source/comment/lock/probe 파일도 모두 제거했다.

## 10. 최종 판정

2라운드의 세 수정은 원래 반박을 제대로 이해하고 고친 방향이다. 특히 LPSOCl β 게이트와
fresh-start drift/validator 결합은 통과한다. 하지만 다음 네 건은 완료 전 차단 항목이다.

1. Windows 100건에서 `os.replace()` 간헐 실패를 재시도 또는 저장소 교체로 막을 것.
2. tracked 정본을 수정하는 테스트를 임시 source fixture로 바꿀 것.
3. 실행 중 화면 갱신 요구사항을 구현하거나 “재시작 시 반영”으로 정확히 명시할 것.
4. `unreviewed_drift`와 `resolve_error`를 모든 자동판정에서 제외하고 표·카드에 상태를 표시할 것.

추가로 `mkdir` stale lock 회수, Nd 비교표의 `−5.944` 동기화, comp1 단일시드 source 배선을
후속으로 처리하면 된다.
