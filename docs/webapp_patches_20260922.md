# 병합 요청 — 웹앱 패치 2건 (`f58c71d6e` · `514691646`, 2026-09-22)

> 대상 브랜치 `claude/sdcp-dem-manuscript-si-pqwtv8`.  1저자 비준 받고 진행했다.
> 앞선 인계 문서 `docs/handoff_review_20260922.md` 와 **겹치지 않는다** — 그 문서는
> 09-22 오전까지의 153 커밋이고, 이 문서는 그 **뒤**에 붙은 2 커밋이다.

## 0. 한 줄

오래된 케이스 하나를 다시 돌렸더니 **결함 두 개**가 겹쳐 있었다 — ⓐ venv 에 패키지가
빠져 있었고 ⓑ 그것을 고치자 드러난 자리에서, **원자의 99.75 %가 상(phase) 없이 계산되는
데도 파이프라인이 멈추지 않는** 것이 보였다.  ⓑ 쪽에서 크래시가 **우연히** false-green 을
막고 있었다.

## 1. 범위 (실측)

```
git log --oneline f58c71d6e~1..514691646
```

| 커밋 | 주제 |
|---|---|
| `f58c71d6e` | 웹앱 파이썬 환경 감사·복구 도구 |
| `514691646` | atom-type ↔ 상 매핑을 덱에서 읽고 덤프로 검증 |

6 파일 · **+1,131 / −4**.  신규 3 (`scripts/webapp_env_audit.py` ·
`scripts/setup_webapp_env.sh` · `scripts/type_map_resolve.py`) · 수정 3
(`scripts/analyze_contacts.py` · `webapp/app.py` · `docs/reviews/selftest_inventory.tsv`).

⛔ **계산 산출물은 한 바이트도 안 건드렸다.**  `docs/data/` · 원장(`claims.json` ·
`findings.json`) · 사전등록 문서 · 덱 생성기 전부 무변경.  판정·수치에 영향 없다.

## 2. 발단 — 케이스 `260922_092001_0853b1`

`ModuleNotFoundError: No module named 'networkx'` 로 실패.  진단이 **두 번 틀렸고**,
둘 다 실측이 반증했다.  이 기록을 남기는 이유는 같은 오판을 반복하지 않기 위해서다.

### 오진 ① — "낡은 인스턴스가 bare `python3` 로 떠 있다 ⇒ 죽여야 한다"

반증: `/proc/<pid>/environ` 이 `VIRTUAL_ENV=~/Yonghoon-DEM-DFT/.venv` 를 보여줬다.
웹앱은 **venv 안에서 정상으로** 돌고 있었다.  추측대로 프로세스를 죽였으면 사용자
세션을 세웠다.  ⇒ **프로세스를 추측으로 죽이지 않는다. `/proc` 에 물어본다.**

### 오진 ② — "시스템 파이썬에 전부 깔아야 한다"

반증: 빠진 것은 `networkx` · `adjustText` · `tabulate` **세 개**뿐이었고 전부 venv 문제였다.
시스템(apt) 설치는 그 웹앱이 보지도 않는다.

### 근본 원인 (실측)

```
git log -1 --format='%ad %h' --date=short -S networkx -- webapp/requirements.txt
→ 2026-04-24 660600a44
```

`networkx` · `adjustText` · `tabulate` 셋 다 **같은 커밋** `660600a44` 에서
`webapp/requirements.txt` 에 들어왔고, 그 venv 는 그 **전에** 만들어져 `pip install -r`
이 다시 안 돌았다.  ⇒ **규약(requirements)은 자랐는데 환경은 안 자랐고, 그것을 강제하는
것이 아무것도 없었다** = CLAUDE.md 규율 ④ 의 환경 판.

## 3. 패치 ① `f58c71d6e` — 환경

### `scripts/webapp_env_audit.py` (신설 · selftest 11/11 · 3.4 s · stdlib 만)

필요 패키지를 **상수로 박지 않는다**.  매번 `webapp/*.py` · `scripts/*.py` 를 AST 로
전수 파싱해 최상위 import 를 뽑고, 분류표에 없는 HARD import 가 하나라도 있으면 거부한다.
목록을 손으로 적으면 규율 ⑤ 의 사각지대("후보를 고르는 코드가 곧 사각지대다")가 그대로
재현된다.  `requirements.txt` 도 읽지 않는다 — **낡는 쪽은 둘 다**이기 때문이다.

★ `try/except ImportError` 안과 함수 안의 import 를 HARD 에서 **뺀다**.  이 구분이 없으면
`taichi` · `cupy` · `mph` 까지 설치 대상이 돼 설치가 통째로 실패한다.  실측: `taichi` 는
HARD 지만 MPM 스크립트 6개 전용이라 웹앱 분석 경로와 무관하다.

판정 결과 (실측):

| 반드시 | 옵션 |
|---|---|
| `numpy` 340파일 · `pandas` 73 · `scipy` 59 · `matplotlib` 52 · `networkx` 2 · `sklearn` 2 · `flask` 2 · `requests` 1 | `adjustText` `markdown` `jinja2` `werkzeug` `cupy` `mph` `h5py` `skopt` `pybamm` `trimesh` `skimage` `shapely` `weasyprint` `anthropic` … |

### `scripts/setup_webapp_env.sh` (신설 · 199 줄)

핵심은 설치가 아니라 **안전장치 둘**이다.

1. **venv 를 추측하지 않는다** — 돌고 있는 웹앱 프로세스의 `VIRTUAL_ENV` 를 읽는다.
   후보를 고르면 `~/ddvenv` 같은 엉뚱한 데 깔린다.  서로 다른 venv 로 여러 개 떠 있으면
   **거부**하고 프로세스를 죽이지 않는다.
2. **이미 깔린 코어를 절대 업그레이드하지 않는다** — 웹앱이 그 venv 로 돌고 있어
   `numpy`/`scipy` 의 `.so` 가 실행 중에 교체되면 죽는다.  `pip --dry-run` 으로 계획을
   먼저 보고 코어를 건드리면 `rc=1` 로 거부한다.

★ 스모크가 **모든 종료 경로**에서 돈다 (규칙 J) — 죽었던 모듈을 실제로 import 한다.
"깔 것이 없다" 경로에서도 돈다: 안 그러면 ABI 가 깨진 venv 가 "완전하다" 로 초록을 낸다.
(초판이 실제로 그랬고 고쳤다.)

실측 3 경로: 빈 venv 설치 → 재검증·스모크 통과 `rc=0` · 낡은 numpy(1.23.5) → `numpy 1.23.5
→ 2.4.6` 을 잡아 거부 `rc=1` · 완전한 venv → 스모크만 돌고 `rc=0`.

## 4. 패치 ② `514691646` — atom-type ↔ 상 매핑

### 무슨 일이 있었나

`dem_scripts/ps_sweep_6mah_20260914/in.ps_10_0_r45.liggghts` 세대 덱은 `create_box 3` 에
**1:AM_P · 2:AM_S · 3:SE** 다.  P:S=10:0 팔은 AM_S 질량분율이 0 이라
(`pdd_mix … pts1 0.816 pts3 0.184`) **type 2 가 설계상 0개**이고 SE 는 type 3 에 있다.
그런데 `webapp/app.py` 가 standard 모드에서 `f'1:{am_type_name},2:SE'` 로 **SE 를 type 2 에
박아** 있었다.

실측 (사용자 덤프 `atom_3640000.liggghts`):

```
type 1 :      403개 ( 0.253 %)  r 4.5000e-03
type 3 :  158,749개 (99.747 %)  r 5.0000e-04
(type 2 없음)
```

결과:

- type 3 = 원자의 **99.75 %** 가 아무 상에도 안 붙어 `?` 가 됐다
  (분석 로그: `?-AM_P: 92,268` · `?-?: 442,426` · `AM전체-SE: 0` · `SE-SE CN: 0.00` ·
  `Percolation: 0.0%`)
- 그런데도 파이프라인은 **멈추지 않고** porosity 15.82 % · AM-AM CN 3.64 · 응력 CV 206.8 % ·
  파괴지수 0.218 을 **그럴듯하게 전부** 뽑았다
- 마지막 `save_results` 의 배위수 루프가 빈 배열(type 2)에 `np.min` 을 걸어 **우연히** 터졌다

⇒ **크래시가 false-green 을 우연히 막고 있었다.**  안 터졌으면 상(phase) 없이 계산된
리포트가 초록으로 나갔다.

### 왜 손으로 적게 돼 있었나 — 그럴 필요가 없었다

옛 `app.py` 는 **덤프를 열어 반지름까지 읽어 놓고** type 1 만 보고 AM_P/AM_S 를 정한 뒤
SE 는 확인조차 안 했다.  정보를 쥐고 버린 것이다.

그리고 덤프에는 `SE` 라는 글자가 없지만(`id type x y z radius …` 뿐) **덱에는 있다**:

```
fix pts3 all particletemplate/sphere 22600001 atom_type 3 density constant 2000 radius constant ${r_SE}
```

`atom_type 3` ↔ `${r_SE}` 는 **추정이 아니라 선언**이고, 덱은 매번 같이 업로드된다
(1저자 확인).

### `scripts/type_map_resolve.py` (신설 · selftest 16/16 · 0.1 s)

덱의 `particletemplate/sphere` 줄을 읽어 상을 정하고 **덤프의 실제 타입·반지름과 대조**한다.
세 가지를 **거부**한다:

| 거부 | 왜 |
|---|---|
| 덤프에 있는데 map 에 없는 타입 | 이번 사고 그 자체 (99.75 % 가 `?` 가 된다) |
| 덱 반지름 ≠ 덤프 반지름 | 덱과 덤프가 **같은 런이 아닐** 수 있다 |
| 모르는 변수 이름 | **추측하지 않는다** |

반대로 map 에 있는데 덤프에 0개인 타입은 **정상**일 수 있어(P:S=10:0 의 AM_S) note 로만 낸다.

규율 ① 준수: 덱 수식 평가기를 새로 짜지 않고 `scripts/parse_liggghts.py` 의
`_eval_liggghts_expr` 를 재사용한다 (그래서 numpy 의존이 붙는다).

### `scripts/analyze_contacts.py` — **계산 전** fail-closed 게이트

덤프에 있는데 map 에 없는 타입이 있으면 몫(99.75 %)과 반지름을 적어 **`rc=2` 로 즉시**
거부한다.  실측: 3원자 합성 케이스에서 `contacts.csv` 를 열기도 **전에** 거부한다.

그리고 빈 타입의 배위수는 크래시가 아니라 `—` 로 낸다.  (124행 `particle_info` 루프가
이미 `if not sub: continue` 로 같은 규약을 쓰고 있었고 **이 루프만 빠져 있었다**.)

⚠ 이 관용이 안전한 **유일한** 이유가 위 게이트다 — 게이트 없이 관용만 넣으면 틀린 map 이
**조용히 통과**한다.  그래서 둘을 한 커밋에 넣었다.  분리해 병합하지 말 것.

`main()` 의 반환값이 실제 종료코드가 되도록 `sys.exit(main())` 로 바꿨다 (전엔 `return` 이
무시돼 게이트가 rc 를 못 냈다).

### `webapp/app.py` — 업로드 기본값

덱 판독으로 바꾸되 **fail-open** 이다 (덱 없이 올릴 수도 있고, 여기서 막으면 올리지도
못한다).  못 읽으면 옛 반지름 규칙으로 되돌리고 그 사실을 `type_map_notes` 에 남긴다.
사용자가 직접 적은 값은 **이긴다**(의도적인 경우가 있다) 대신 덱 판독과 다르면 경고를
기록한다.  `meta.json` 에 `type_map_resolved` · `type_map_notes` 신설 — **보이지 않으면
없는 것과 같다.**

## 5. 무엇이 **안** 바뀌었나 — 병합 신뢰의 핵심

- ⚠ **옛 세대 덱(`create_box 2`, 변수 `r_AM` 하나)의 상 라벨 규칙은 그대로다.**
  `dem_scripts/case09_E15x.liggghts` 류는 지금까지 반지름 `> 0.004`(sim) 로 AM_P/AM_S 를
  갈라 왔고, **170여 케이스 코퍼스의 상 라벨이 거기 걸려 있다.**  그 규칙을 `r_AM` 총칭
  변수일 때만 적용하도록 **보존**했고, selftest ②②b 가 이를 고정한다
  (`r_AM 3.0e-3 → 1:AM_S,2:SE` · `r_AM 6.0e-3 → 1:AM_P,2:SE`).
- 사용자가 직접 적은 `type_map` 은 여전히 최우선이다.
- 이미 분석이 끝난 케이스는 재분석하지 않으면 아무것도 바뀌지 않는다.
- 솔버·물리·수치 경로 무변경.

## 6. 검증 절차 — 이 순서로

```bash
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git log --oneline f58c71d6e~1..514691646
python3 scripts/webapp_env_audit.py --selftest      # 11/11
python3 scripts/type_map_resolve.py --selftest      # 16/16
bash scripts/setup_webapp_env.sh --check            # 이 기계 환경이 성립하는가 (설치 안 함)
```

★ **판별력 확인** (검사가 공허하지 않음을 보는 법) — `scripts/type_map_resolve.py` 의
selftest ④ 가 사고 당시 map 을 그 덤프에 대면 **반드시 거부**하고, ⑤ 가 올바른 map 은
**통과**시킨다.  ⑩ 은 `webapp/app.py` 가 이 모듈을 실제로 쓰는지 보는 경계 계약이고,
**배선 전에는 실제로 FAIL 이었다**.

실물 대조 (덱·덤프를 손에 쥔 경우):

```bash
python3 scripts/type_map_resolve.py --deck <in.*.liggghts> --atoms <atom_*.liggghts>
python3 scripts/type_map_resolve.py --atoms <atom_*.liggghts> --check-map "1:AM_P,2:SE"
```

두 레인 (필수):

```bash
bash scripts/check_all.sh --selftest    # RC 0
bash scripts/check_all.sh               # RC 0
```

⚠ **얕은 클론에서는 게이트가 거짓 실패를 낸다** — 옛 SHA 도달성 검사 3건이 무너진다
(검사기 자신이 `git fetch --unshallow` 를 지시한다).  CI 는 `fetch-depth: 0` 이어야 한다.

## 7. 병합 시 충돌 가능 지점

| 파일 | 자리 | 비고 |
|---|---|---|
| `webapp/app.py` | import 블록 (기존 `press_units` 줄 바로 뒤) | 한 줄 추가 |
| `webapp/app.py` | 업로드의 기본 `type_map` 블록 | 옛 반지름 로직은 **되돌림 경로로 보존**돼 있다 — 병합 시 지우지 말 것 |
| `webapp/app.py` | `meta` 딕셔너리 | 키 2개 추가 |
| `scripts/analyze_contacts.py` | import · 배위수 루프 · `main()` 머리 · `__main__` | 4곳 |
| `docs/reviews/selftest_inventory.tsv` | 끝 2줄 추가 | 끝 개행 유지 |

## 8. 남은 것 · 미검증

- ⚠ 이 게이트는 **contact 분석에만** 걸린다.  다른 소비자(STEP3 σ · STEP4 등)가 같은
  `type_map` 을 받는 경로는 아직 검증되지 않았다.  `resolve`/`validate` 를 그쪽에도
  태우는 것이 다음 단계다.
- 업로드 UI 의 `type_map` 입력칸 플레이스홀더가 `1:AM_P,2:AM_S,3:SE` 인데, P:S=10:0 덱에는
  그 값이 **함정**이다 (type 2 가 0개).  자동판독이 붙었으니 칸을 비우면 되지만,
  플레이스홀더 문구 자체는 아직 그대로다.
- 이미 `?` 로 계산돼 저장된 옛 케이스가 더 있는지 **전수 확인하지 않았다.**
  `?` 는 `contacts_analyzed.csv` 의 타입 라벨에 남으므로 스윕으로 찾을 수 있다.

## 9. 수용 체크리스트

- [ ] `webapp_env_audit --selftest` 11/11
- [ ] `type_map_resolve --selftest` 16/16 (특히 ④ 음성 대조 · ⑤ 판별력)
- [ ] `check_all.sh --selftest` RC 0 · `check_all.sh` RC 0 (**얕은 클론이 아닐 것**)
- [ ] 옛 세대 덱 케이스 1건을 재분석해 상 라벨이 **안 바뀌는지** 확인
- [ ] `ps_sweep` 팔 1건을 칸 비우고 업로드해 `type_map_resolved` 가 맞게 찍히는지 확인
