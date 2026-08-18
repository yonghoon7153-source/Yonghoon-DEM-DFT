# Origin 재작도 — 음이온 자리 가로 막대 (세미나 10장 왼쪽)

원본: `tools/figures/plot_seminar_2026_08.py : fig_anion_site`
데이터: `db/properties/seminar_table_anion_site.csv`
산출 예: `docs/figures/seminar/step2_anion_site.png`

> ⛔ **색이 바뀌었습니다 (2026-08-18).** 옛 그림은 색을 **순위 자리**로 칠해서
> 할라이드 자리가 황 색, 황 자리 하나가 염소 색이었습니다 — 화학과 반대였어요.
> 아래 표의 색이 정본입니다. 옛 PNG 를 보고 색을 따라 넣지 마세요.

---

## 1. 데이터 준비

새 Worksheet 에 **3행**만 넣습니다. Col(A) 는 **Label(Text)** 타입이어야 합니다.

| | Col(A) — Label | Col(B) — Y |
|---|---|---|
| **이름** | `sublattice` | `n_candidates` |
| 1 | sulfur in the PS₄ corner | 83 |
| 2 | free sulfide | 89 |
| 3 | halide site | 98 |

⚠ **아래에서 위로 커지는 순서**로 넣습니다. Origin 의 가로 막대는 행 1이 **맨 아래**에
그려지므로, 이렇게 넣어야 파이썬 그림과 같은 배치(큰 값이 위)가 됩니다.

**Col(A) 타입 지정** — Col(A) 머리 우클릭 → `Set As` → `Y` 가 아니라,
Script Window 에서:

```labtalk
wks.col1.type = 4;      // 4 = Label(Text)
wks.col2.type = 2;      // 2 = Y
```

`PS₄` 의 아래첨자는 Origin 문법으로 `PS\-(4)` 입니다. 셀에 직접 `PS\-(4) corner` 로
입력하면 렌더링됩니다.

---

## 2. 그래프 생성

Col(B) 선택 → `Plot ▸ Bar, Pie, Area ▸ Bar`

또는 Script Window:

```labtalk
plotxy iy:=(1,2) plot:=101 ogl:=<new>;    // 101 = horizontal bar
```

---

## 3. BML 포맷 적용

`anion_site_barh.ogs` 를 Script Window 에 붙여넣고 Enter.

**실행 후 이렇게 바뀝니다** — 레이어 12×9 cm, 축 회색(#404040) 1 pt,
틱 바깥쪽, 틱 라벨 Arial 28 pt, 위/오른쪽 축은 선만(틱·라벨 없음),
X 축에만 주 격자선.

---

## 4. GUI 추가 작업 (LabTalk 로 안 되는 것)

### ① 막대 색을 **막대마다 다르게**

Origin 의 단일 bar 플롯은 기본이 한 색입니다. 세 막대를 따로 칠하려면:

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | 막대 더블클릭 → **Plot Details** | |
| 2 | **Pattern** 탭 | |
| 3 | `Fill Color` 옆 화살표 → **By Points** | ← 이게 핵심 |
| 4 | `Color List` → **Custom** → 아래 색 3개를 순서대로 | |

| 행 | 부격자 | 색 | RGB |
|---|---|---|---|
| 1 | sulfur in the PS₄ corner | `#DD8F5F` | (221, 143, 95) |
| 2 | free sulfide | `#C05621` | (192, 86, 33) |
| 3 | halide site | `#65A30D` | (101, 163, 13) |

> 황 부격자 둘은 **같은 계열의 진하기 차이**, 할라이드만 다른 색입니다.
> 색으로 "황이냐 염소냐" 가 먼저 보이게 한 것이라, 임의로 바꾸면 의미가 사라집니다.

**`By Points` 가 안 보이면** — Origin 버전에 따라 `Individual Colors` 또는
`Color Mapping` 으로 되어 있습니다. 그것도 없으면 우회:
데이터를 **3개 Y 컬럼**(각각 값 하나 + 빈칸 2개)으로 쪼개서 3개 플롯으로 만들고
플롯마다 `set` 으로 색을 줍니다.

### ② 막대 끝 숫자 (Data Label)

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | 막대 더블클릭 → **Plot Details** | |
| 2 | **Label** 탭 | |
| 3 | `Enable` | ☑ 체크 |
| 4 | `Label Form` | **X Value** ← 가로 막대라 값이 X 축이다 |
| 5 | `Numeric Format` | Decimal, **Decimal Places: 0** |
| 6 | `Position` | **Right** |
| 7 | Font / Size / Color | Arial / **18 pt** / `#6B7280` |

⚠ **가로 막대에서는 `Y Value` 가 아니라 `X Value`** 입니다. 세로 막대 감각으로
`Y Value` 를 고르면 카테고리 번호(1·2·3)가 찍힙니다 — 흔한 실수예요.

### ③ 막대 두께

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | 막대 더블클릭 → **Spacing** 탭 | |
| 2 | `Gap Between Bars (%)` | **44** |

파이썬의 `height=.56` 과 같은 두께입니다 (막대 56 % + 간격 44 %).

### ④ 격자선 — X 축만

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | 축 더블클릭 → **Grids** 탭 | |
| 2 | `Vertical` ▸ Major Grid Lines | ☑ 체크, Color `#E5E7EB`, Width 0.5 |
| 3 | `Horizontal` ▸ Major/Minor | ☐ 모두 해제 |

### ⑤ Y 축 (카테고리 축) 정리

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | Y 축 더블클릭 → **Tick Labels** 탭 | |
| 2 | `Type` | **Tick-indexed string** → Col(A) 지정 |
| 3 | **Line and Ticks** 탭 | Major/Minor Ticks: **None** |

카테고리 축에는 눈금이 필요 없습니다 — 이름표만 남깁니다.

---

## 5. 수동 입력 값 (Text 객체)

| 위치 | 내용 | 폰트 | 색 |
|---|---|---|---|
| X 축 제목 | `number of generated candidates that placed the dopant anion there` | Calibri 34 pt | `#404040` |
| Y 축 제목 | (없음 — 이름표가 곧 설명) | | |

축 제목이 길면 두 줄로 나눠도 됩니다. Origin 에서 줄바꿈은 `Ctrl+Enter`.

---

## 6. 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 막대가 세로로 나온다 | `plot:=100` 을 썼다 | `plot:=101` (가로) |
| 라벨에 1·2·3 이 찍힌다 | Label Form 이 `Y Value` | 가로 막대는 **X Value** |
| Y 축에 1·2·3 이 찍힌다 | Col(A) 가 Label 타입이 아니다 | `wks.col1.type = 4;` |
| 막대 순서가 뒤집혔다 | Origin 은 **행 1 = 맨 아래** | 워크시트 행 순서를 뒤집는다 |
| 색이 세 막대 다 같다 | Fill Color 가 단색 | Pattern 탭 ▸ **By Points** |
| `PS4` 의 4가 안 내려간다 | 일반 텍스트로 입력 | `PS\-(4)` |

---

## 7. 마무리 체크리스트

| # | 항목 | 확인 |
|---|---|---|
| 1 | Fixed Factor 0.7 (`View ▸ Fixed Factor`) | ☐ |
| 2 | Layer 12 × 9 cm | ☐ |
| 3 | 축 제목 Calibri 34 pt `#404040` | ☐ |
| 4 | 틱 라벨 Arial 28 pt `#404040` | ☐ |
| 5 | 막대 3색이 **화학대로** (황 2 = 주황 계열, 할라이드 = 초록) | ☐ |
| 6 | 값 라벨 Arial 18 pt, 소수점 0자리, 막대 오른쪽 | ☐ |
| 7 | 격자선 X 축만 | ☐ |
| 8 | 위/오른쪽 축 = 선만 (틱·라벨 없음) | ☐ |
| 9 | 큰 값(98)이 **맨 위** | ☐ |

---

## 이 가이드가 못 하는 것

- Origin 버전별 메뉴 이름 차이를 다 담지 못한다 (2021 이후 기준으로 썼다).
- `.ogs` 는 **포맷만** 적용한다. 데이터 입력·플롯 생성·Data Label 은 GUI 단계다.
- 파이썬 그림과 픽셀 단위로 같아지지는 않는다 — 폰트 렌더링이 다르다.
