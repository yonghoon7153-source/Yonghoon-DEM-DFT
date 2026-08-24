# Codex 리뷰 결과 — 화면이 없는 것을 어떻게 말하는가 (승인 보류)

- 과제: [2026-08-24-codex-review-screens-and-partials.md](2026-08-24-codex-review-screens-and-partials.md)
- 범위: `a4459311..fce02f5a` (커밋 11개, 47파일, +3042/−177)
- 결론: **승인 보류.** 12건 — 높음 3 · 중간 7 · 낮음 2
- 대응: **아직 안 함.** 이 문서는 원문 기록이고, 고치는 것은 다음 세션이다.

> Codex 는 첨부 zip 의 `full.diff` 와 `changed/` 최종본으로 검토했고 소스는
> 수정하지 않았다. 판정 입력은 직접 재현했고, 고정 열·범례는 Chromium 에서
> 확인했다. 그쪽 Windows 호스트에서는 Bash/WSL 실행이 막혀 셸 suite 전체는
> 다시 돌리지 못했다.

## 이 세션에서 확인한 것 (다음 사람이 다시 파지 않도록)

**높음 2 는 사실이다.** uPlot 소스로 확인했다 (`uplot@1.6.32`,
`dist/uPlot.cjs.js`):

```
6078  _init()  →  setData(...)  →  autoScaleX()   ← pendScales 만 채운다
6088           →  _setSize(...) →  commit()
4762  commit() →  microTask(_commit)              ← 여기서 setScales() 가 돈다
1474  기본 scale 은 min: inf, max: -inf
```

즉 **생성자가 반환하는 시점에 `scales.x.min` 은 아직 `inf`** 이다.
`Plot.tsx` 의 `homeRef.current = readScales(plot)` 는 `Number.isFinite` 로
거르므로 `{}` 를 저장하고, 그 뒤로:

- `zoomBy()` 는 순회할 축이 없어 아무 일도 안 한다
- `sameView({}, now)` 는 항상 참이라 `zoomed` 가 영영 false
- 결과: **확대는 무반응, 축소·전체는 계속 비활성**

`Plot.test.tsx` 의 대역이 생성자 안에서 scale 을 **동기로** 완성해서 이
회귀를 정답으로 통과시켰다는 지적도 그대로 맞다. 고칠 때 대역도 `ready`
훅 이후로 지연시켜야 한다 — 안 그러면 고친 뒤에도 시험이 못 잡는다.

나머지 11건은 이 세션에서 재현해 보지 않았다. **다음 세션이 각각 재현부터
하고 시작할 것.**

## 높음 3건

### 1. 불완전 사유 판정이 '모름' 을 두 값 중 하나로 단정한다
`packages/wrdkit/src/wrdkit/cycles.py:286-319`

깨지는 입력 셋:

- 스케줄 없는 `charge → rest` 기록이 전류 0 에서 정상 종료해도 `truncated`.
- formation 에만 discharge 가 있고 cycling loop 는 charge-only 이면, 스케줄
  전체를 `any()` 로 훑기 때문에 cycling cycle 도 `truncated`.
- `direction="unknown"` 인 CV-only 방전 스텝은 discharge 선언으로 안 세어
  `no_discharge` 로 뒤집힌다.

앞 둘에서 화면은 "기다리거나 다음 분할 파일을 올리라" 고 하고, 마지막에서는
"영원히 방전하지 않을 프로토콜" 이라고 말한다. §0.3 의 스케줄 정보를 쓰기는
했지만 **현재 cycle 이 속한 phase/loop 를 모르는 상태에서 전역 검색으로
단정**했고, 스케줄 부재·unknown 도 §0.4 처럼 unknown 으로 남기지 않았다.

CV discharge 는 가상 사례가 아니다 (NEWARE 의 CV discharge 설명, BioLogic 의
constant-potential discharge 사례). 다만 WonATech `.wrd` 가 이를 어떻게
직렬화하는지는 이번 자료로 확인하지 못했다 — **unknown 을 absence 로 읽으면
안 된다.**

`packages/wrdkit/tests/test_health.py:103-159` 는 전체 charge-only 와 통상적인
signed charge/discharge 만 다룬다. 스케줄 없음+휴지 종료, phase/loop 방향
불일치, unknown-only 방향이 빠져 있다.

### 2. 실제 uPlot 에서 돋보기 기준 범위가 `{}` 로 저장되어 버튼이 죽는다
`apps/web/src/components/Plot.tsx:216-227, 469-478, 515-543`

재현: 데이터가 있는 아무 그래프나 처음 연 뒤 `확대` 를 누른다. 축은 안 움직이고
`축소`·`전체` 는 계속 비활성.

(근거는 위 "이 세션에서 확인한 것" 참고. 초기 범위는 `ready` 훅이나 첫 scale
commit 뒤에 잡아야 하고, 대역도 그 시점을 지연해야 한다.)

### 3. `.bml/env` 저장 실패 후에도 성공을 출력한다
`tools/bml:2387-2400`; 호출부 `1299, 1317-1321, 1343-1355, 2621-2641`

재현:

- `.bml` 을 일반 사용자에게 읽기 전용으로 만들고 `bml password <암호>` 또는
  `bml host local` 실행.
- 임시 파일 생성과 `mv` 는 실패하지만 각각 "공유 암호를 저장했습니다",
  "공개: 이 기계 안에서만" 을 출력하고 **종료 코드 0**.
- 사용자는 보호됐다고 믿는데 서버에는 옛 암호 또는 무암호 상태가 남는다.

별도 깨지는 입력: `.bml/env` 만 `chmod 000` 이고 상위 폴더는 쓰기 가능하면,
기존 파일을 읽는 `grep` 이 실패한 뒤 **새 key 하나뿐인 임시 파일이 원본을
교체**하여 `WORKBENCH_DATA`, 기존 암호 등 다른 설정을 잃는다.
`chmod 600 ... || true` 도 권한 설정 실패를 숨긴다.

`test_bml_client.sh:87-99, 193-213` 과 `test_bml_data.sh:109-147` 은 정상
파일시스템만 쓴다. 읽기·쓰기·chmod·mv 실패 중 어느 것도 주입하지 않는다.

## 중간 7건

### 4. 옛 DB 행과 `no_steps` 를 '스텝 중간 잘림/구동 중' 으로 추측한다
`packages/wrdkit/src/wrdkit/health.py:177-185, 296-303`

`reason not in ("no_discharge", "no_charge")` 때문에 `incomplete_reason=""` 와
`no_steps` 가 모두 `ends_mid_cycle=True` 다. 둘 다 `state="running"`,
`in_progress_cycle=N`, `cut off mid-step` 근거가 된다. **같은 옛 행을 사이클
표는 "이유 미상 — 재파싱" 이라고 하는데 보고서는 "잘렸으니 구동 중" 이라고
말한다.**

빈 문자열로 옛 행을 보존하고 화면에서 재파싱을 권하는 선택 자체는 맞다.
잘못은 그 값을 소비하는 `health.py` 가 **다시 추측**하는 것이다. 구동 중
vote 는 literal `truncated` 에만 줘야 한다. 빈 사유와 `no_steps` 를
`build_report()` 까지 통과시키는 테스트가 없다.

### 5. `include_partial=true` 가 금지한 부분 용량을 숫자로 내보낸다
`apps/api/app/routers/analysis.py:401-435`, `apps/api/app/services.py:635`,
`apps/web/src/pages/SampleDetail.tsx:559`, `apps/web/src/lib/origin.ts:51-65`

5 mAh 사이클을 방전 중 1.584 mAh 에서 자르면 `profile.capacity[-1]` 도 정확히
1.584… 다. 화면 커서에서 읽히고, **프로파일 복사는 그 배열을 숫자 두 열로
내보내면서 `complete=false` 와 `incomplete_reason` 을 버린다.** Origin 에
붙인 뒤에는 완료 곡선과 구분할 정보가 없다.

기본 꺼짐과 화면 label 은 위험을 낮추지만, 실제 truncated cycle 에서는 §3
("마지막 사이클 값을 절대 보고하지 않는다") 을 못 지킨다. **정상 종료한
`no_charge`/`no_discharge` trace 와 구동 중 truncated trace 를 같은 정책으로
처리하면 안 된다.**

`test_analysis.py:277-299` 는 정상 종료한 charge-only 곡선만 보고,
`origin.test.ts:78-107` 의 profile fixture 도 항상 complete 다.

### 6. 축 고정을 켜도 드래그가 세로축을 바꾼다 (2번 수정 후에는 버튼도)
`apps/web/src/components/Plot.tsx:327-342, 502-505, 519-533`

현재 재현: `yRange={[0,100]}` 또는 `[0,null]` 인 그래프에서 세로 방향으로 drag
zoom. `cursor.drag.y=true` 라 잠근 범위가 움직인다. 두 축을 모두 잠가 버튼이
비활성이어도 drag 는 살아 있다.

2번을 고쳐 `home` 이 채워지면 `zoomBy()` 도 모든 축에 명시적 `setScale()` 을
호출한다. uPlot 은 데이터가 있을 때 명시적으로 준 범위를 `scale.range` 로 다시
고정하지 않는다. 따라서 y lock 도 약 20..80 처럼 바뀐다.

`Plot.test.tsx:421-432` 는 버튼 disabled 만 검사하고 range callback 과 drag 를
구현하지 않는다.

### 7. restart 가 서버를 내린 뒤 실패하면 서버 없는 터널이 남는다
`tools/bml:525-534, 866-870, 1083-1084, 1125-1126, 1212-1218, 3882-3895`

재현: 서버와 share 를 연 뒤 외장 데이터 경로를 분리하고 `bml restart`.
`cmd_stop --keep-tunnel` 이 서버를 먼저 내리고, 이후 `guard_data_dir` 가
종료하므로 `report_failure` 와 `close_tunnel` 을 **안 거친다.** 터널 PID/URL 은
남고 외부에는 계속 5xx 가 보인다. `build_web` 실패와 Ctrl-C/TERM 도 같다.

`test_bml_client.sh:837-848` 은 `cmd_stop --keep-tunnel` 문자열 수와
`report_failure` 안의 `close_tunnel` 존재만 센다. **`guard_data_dir(){ return 1; }`
로 실제 restart 를 깨도 그대로 통과한다** — 이번 범위에서 찾은 대표적인
"구현 문자열을 검사한 시험" 이다.

### 8. install 이 실행기 생성에 실패해도 성공을 출력한다
`tools/bml:3762-3803, 3812-3828`

재현: 쓰기 불가능한 `/tmp/bml-bin` 을 만들고 `./tools/bml install /tmp/bml-bin`.
`cat` 과 `chmod` 가 실패해도 "설치" 를 출력하고 rc 파일까지 고친 뒤 0 으로
끝난다. **최종 실행기에 직접 쓰므로** ENOSPC 나 중단 시 기존 launcher 를 지우고
빈/부분 파일을 남길 수도 있다. 같은 폴더의 임시 파일에 쓰고, 실행 가능성과
내용을 확인한 뒤 `mv` 해야 한다.

`test_bml_install.sh:52-78, 119-159` 는 writable mktemp 경로뿐이라 실패와 부분
쓰기를 못 잡는다.

### 9. 생성 실행기와 rc 가 특수문자 경로를 다시 셸 문법으로 해석한다
`tools/bml:3764-3770, 3813-3819`

저장소를 `/tmp/Battery $100/repo` 에 두고 설치하면 실행기에
`REAL="/tmp/Battery $100/repo/tools/bml"` 이 기록된다. 다음 실행 때 `$1` 이 다시
확장되어 실제 파일이 있어도 다른 경로를 찾는다. 따옴표·역슬래시도 같다.

또 `.bashrc` 에 `# old /home/me/.local/bin` 같은 **주석만 있어도**
`grep -qF "$target"` 가 "이미 그 줄이 있습니다" 로 판단해 PATH 추가를 건너뛴다.

`test_bml_install.sh:59-78, 86-118` 은 안전한 임시 경로의 생성 문자열만 보고,
생성된 wrapper 를 특수문자 경로에서 실제 실행하지 않는다.

### 10. 묶음 구분 행은 가로 스크롤에서 고정되지 않는다
`apps/web/src/pages/Library.tsx:256-260`, `apps/web/src/styles/app.css:596-598`

좁은 Library 화면에서 묶은 뒤 오른쪽으로 스크롤하면 일반 행의 이름은 남지만
묶음 제목은 사라진다. Chromium 재현에서 1400px 표를 `scrollLeft=500` 으로
옮겼을 때 일반 첫 셀은 `left=0`, `colSpan=14` 구분 셀은 `left=-499.5` 였다.
**전체 표 폭인 colspan 셀 자체에 `left:0` 을 줬기 때문**이다.

`library.test.tsx:289-301, 330-353` 은 colSpan 값과 CSS 문자열만 확인해 실제
배치를 못 본다.

## 낮음 2건

### 11. `_partial_cycles` 의 branch flag 가 CELL STATUS 와 모순될 수 있다
`apps/api/app/routers/analysis.py:273-276`,
`packages/wrdkit/src/wrdkit/cycles.py:250-256`

charge/rest-only 입력의 한 점에 `-2e-12 A` 잡음을 넣으면 step mode 와
`incomplete_reason` 은 `no_discharge` 인데 `max_discharge_current_a` 가 생겨
API 는 `has_discharge=true` 를 낸다. 지금 웹은 이 flag 를 안 써서 영향은 낮지만
**응답 자체가 모순**이다. 전류가 정확히 0 인 fixture 만 있어 이 경계가 고정되지
않았다. branch 존재는 `StepSegment`/CELL STATUS 에서 가져오는 편이 맞다.

### 12. 접힌 범례와 정적 캡처에서는 부분 사이클 표시가 사라진다
`apps/web/src/pages/SampleDetail.tsx:184-195, 737-742`,
`apps/web/src/components/Plot.tsx:704-745`

390px 폭·계열 12개에서 마지막 부분 사이클은 접힌 범례 밖에 완전히 숨었다.
곡선의 남은 차이는 1.0px 대 1.6px 인데 swatch 에는 굵기가 반영되지 않고,
부분 사이클이 4개보다 많으면 상단 설명도 앞의 네 개만 나열한다. **캡처만 보면
어느 곡선이 부분인지 알 수 없다.** 펼치기와 hover 로 확인할 수 있어 낮음.

`pages.test.tsx:1438-1455` 는 부분 사이클 하나만 만들고 `PlotLegend` 를 대역
처리한다.

## Codex 가 별도 결함을 못 찾은 것

- 옛 `CycleRecord.incomplete_reason=""` 을 추측해 채우지 않고 "이유 미상/재파싱"
  으로 남기는 **설계 자체는 맞다**.
- `BML_INVOKED_AS` 로 `bml`·`bmlin`·`bmlout` 을 구분하는 방식.
- `sameView` 의 `span*1e-6` 와 `setScale` 훅의 React 상태 갱신. (돋보기의 실제
  blocker 는 2번의 초기 capture 시점이다.)
- 패치노트 endpoint.

## 다음 세션이 할 일

1. **재현부터.** 이 문서의 "재현" 을 각 항목마다 실제로 돌린다. 2번은 이미
   확인했으니 건너뛰어도 된다.
2. 높음 3건 → 중간 7건 → 낮음 2건 순. 5번(§3 위반)은 정책 결정이 먼저다:
   정상 종료한 charge-only trace 와 구동 중 truncated trace를 **가르는 것**이
   답으로 보인다.
3. 7·8번은 같은 뿌리다 — 셸이 실패를 안 본다. `set -e` 는 이 스크립트에
   안 맞으니(의도적으로 `|| true` 를 쓰는 자리가 많다) 함수별로 종료 코드를
   돌려주고 호출부가 보게 고친다.
4. 시험을 고칠 때 **구현 문자열을 세는 것에서 동작을 부르는 것으로** 옮긴다.
   7번의 `guard_data_dir(){ return 1; }` 이 그 본보기다.
5. 고친 뒤 이 문서 옆에 회답을 쓴다 (형식은
   `2026-08-24-codex-screens-reply.md` 참고). **닫았다고 쓰기 전에 각 항목을
   실제로 재현해서 안 나는 것을 확인한다** — 지난 라운드에 그것을 안 하고
   "15건 전부 닫음" 이라고 썼다가 Codex 에게 정정당했다.
