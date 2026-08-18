# Origin 재작도 — 자리 조합 격자 (세미나 10장 오른쪽, confusion-matrix 양식)

원본: `tools/figures/plot_seminar_2026_08.py : fig_site_grid`
데이터: `db/properties/seminar_matrix_site_grid.csv` (Matrix 붙여넣기용)
　　　　`db/properties/seminar_table_site_grid.csv` (행·열 합계 포함)
산출 예: `docs/figures/seminar/step2_site_grid.png`

---

## 1. 데이터 준비 — Matrix Book

`File ▸ New ▸ Matrix` → `Matrix ▸ Set Dimensions` : **3 columns × 3 rows**

값을 그대로 붙여넣습니다 (`seminar_matrix_site_grid.csv` 의 `MATRIX` 블록):

| | 1 | 2 | 3 |
|---|---|---|---|
| **1** | 1050 | 810 | 600 |
| **2** | 375 | 270 | 180 |
| **3** | 120 | 105 | 105 |

⚠ **행 1이 맨 위**입니다 (막대 그림과 반대예요 — Matrix 는 위에서 아래). 위 배치가
그림에 나오는 순서 그대로입니다:

```
행 1 = Li 24g          열 1 = free sulfide
행 2 = P 4b (framework) 열 2 = sulfur in the PS₄ corner
행 3 = Li 48h          열 3 = halide site
```

`Matrix ▸ Set Values ▸ XY Mapping` — X: `From 1 To 3`, Y: `From 1 To 3`

---

## 2. 그래프 생성

Matrix 창 활성화 → `Plot ▸ Contour ▸ **Heatmap**`

또는 Script Window:

```labtalk
plotm im:=<active> plot:=226 ogl:=<new>;   // 226 = heatmap
```

---

## 3. BML 포맷 적용

`site_grid_heatmap.ogs` 를 Script Window 에 붙여넣고 Enter.
레이어 12×9 cm, 축 회색 1 pt, 틱 없음, 라벨 Arial 28 pt 로 잡힙니다.

---

## 4. GUI 추가 작업

### ① 컬러맵 — 흰색 → 네이비 4단

| 단계 | 클릭 경로 |
|---|---|
| 1 | 히트맵 더블클릭 → **Plot Details** |
| 2 | **Colormap** 탭 |
| 3 | `Level` 헤더 클릭 → `Set Levels` → **From 0, To 1050, Increment 150** |
| 4 | `Fill` 헤더 클릭 → `Load Palette` → 없으면 아래 4색으로 **Custom** |

| 위치 | Hex | RGB |
|---|---|---|
| 0 (최소) | `#F7FAFC` | (247, 250, 252) |
| 1/3 | `#BCD7EA` | (188, 215, 234) |
| 2/3 | `#5B93C4` | (91, 147, 196) |
| 1 (최대) | `#16365C` | (22, 54, 92) |

### ② 칸 안 숫자 (첫 줄)

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | 히트맵 더블클릭 → **Label** 탭 | |
| 2 | `Enable` | ☑ |
| 3 | `Label Form` | **Z Value** |
| 4 | `Numeric Format` | Decimal, **소수점 0자리**, `Thousands Separator` ☑ |
| 5 | Font / Size | Arial **Bold** / 16 pt |
| 6 | `Offset Y` | **+3** (칸 중앙에서 살짝 위 — 아래에 % 줄이 들어갈 자리) |

⚠ **`Labels` 체크했는데 안 보이면** — `Colormap` 탭의 `Labels` 를 켠 게 아닌지 보세요.
그건 **컨투어 레벨 라벨**이라 다른 겁니다. `Label` **탭**이 맞습니다.

⚠ 글자색은 칸마다 달라야 합니다 (어두운 칸은 흰 글씨). Origin 은 자동으로 안 해 줍니다 —
5절의 표대로 넣으세요.

### ③ 칸 안 % (둘째 줄) — Text 객체 9개

Origin 히트맵 라벨은 **칸당 값 하나**만 붙습니다. 두 줄은 Text 객체로 얹습니다.

`Insert ▸ Text` → 아래 표대로 9개. 좌표는 축 좌표(X 1–3, Y 1–3) 기준이고,
각 칸 중앙에서 **Y 를 0.18 만큼 아래로** 놓습니다.

Arial **10 pt**, 정렬 가운데.

| # | X | Y | 내용 | 글자색 |
|---|---|---|---|---|
| 1 | 1 | 0.82 | `29 % of all` | `#F8FAFC` |
| 2 | 2 | 0.82 | `22 % of all` | `#F8FAFC` |
| 3 | 3 | 0.82 | `17 % of all` | `#1F2937` |
| 4 | 1 | 1.82 | `10 % of all` | `#1F2937` |
| 5 | 2 | 1.82 | `7 % of all` | `#1F2937` |
| 6 | 3 | 1.82 | `5 % of all` | `#1F2937` |
| 7 | 1 | 2.82 | `3 % of all` | `#1F2937` |
| 8 | 2 | 2.82 | `3 % of all` | `#1F2937` |
| 9 | 3 | 2.82 | `3 % of all` | `#1F2937` |

> **% 줄을 생략해도 됩니다.** 개수만으로도 메시지(아홉 칸이 다 찼다)는 전달됩니다.
> Text 9개가 번거로우면 빼세요 — 그때는 ②의 `Offset Y` 도 0으로 되돌립니다.

### ③′ 첫 줄 숫자의 글자색

②는 전체에 한 색만 줍니다. 어두운 칸 셋만 흰 글씨로 따로 바꿔야 합니다:

| 칸 | 값 | 글자색 |
|---|---|---|
| (1,1) | 1,050 | `#F8FAFC` |
| (1,2) | 810 | `#F8FAFC` |
| 나머지 6칸 | | `#1F2937` |

Label 을 개별로 못 바꾸면 — 라벨을 아예 끄고 **숫자도 Text 객체 9개**로 넣는 게
확실합니다 (위 표의 Y 에서 0.18 을 빼면 첫 줄 자리).

### ④ 축 눈금 이름표

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | X 축 더블클릭 → **Tick Labels** 탭 | |
| 2 | `Type` | **Custom** (또는 `Manual`) |
| 3 | 세 칸에 입력 | `free sulfide` / `sulfur in the PS\-(4) corner` / `halide site` |
| 4 | Y 축도 같은 방식 | `Li 24g` / `P 4b (framework)` / `Li 48h` |
| 5 | **Line and Ticks** 탭 | Major/Minor Ticks: **None** |

줄바꿈이 필요하면 그 칸에서 **`Ctrl+Enter`**.
`PS₄` 의 아래첨자는 **`PS\-(4)`**.

### ⑤ 칸 사이 흰 경계선

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | 히트맵 더블클릭 → **Colormap/Contours** 탭 | |
| 2 | `Line` 헤더 클릭 → `Hide All Lines` 해제 | Color **White**, Width **2.5** |

### ⑥ 컬러바

| 단계 | 클릭 경로 | 설정값 |
|---|---|---|
| 1 | 컬러바 더블클릭 → **Levels** 탭 | 눈금 0, 200, 400 … 1000 |
| 2 | **Labels** 탭 | Arial 9.5 pt, `#404040` |
| 3 | 컬러바 제목 (Text 로 추가) | `structures generated`, Calibri 26 pt, 세로 |
| 4 | **Line and Ticks** 탭 | Outline: **없음** |

---

## 5. 수동 입력 값 (축 제목)

| 위치 | 내용 | 폰트 | 색 |
|---|---|---|---|
| X 축 제목 | `Anion site  (where the dopant's O / halide went)` | Calibri 34 pt | `#404040` |
| Y 축 제목 | `Cation site  (where the dopant metal went)` | Calibri 34 pt | `#404040` |

---

## 6. 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 칸 숫자가 안 보인다 | `Colormap ▸ Labels` 를 켰다 | 그건 컨투어 레벨 라벨. **`Label` 탭**의 Enable |
| 색이 무지개로 나온다 | 기본 팔레트 | Colormap 탭에서 4색 Custom |
| 그림이 위아래 뒤집혔다 | Matrix Y 매핑이 3→1 | `Set Values ▸ XY Mapping` Y: From **1** To **3** |
| 어두운 칸 숫자가 안 읽힌다 | 라벨 색이 전부 검정 | ③′ 표대로 흰 글씨 3칸 |
| 칸 경계가 없다 | Hide All Lines | ⑤ 참조 |
| 축에 1·2·3 이 찍힌다 | Tick Labels Type 이 기본값 | ④ Custom |
| 컬러바 제목이 안 붙는다 | Origin 은 자동 생성 안 함 | Text 객체로 직접 |

---

## 7. 마무리 체크리스트

| # | 항목 | 확인 |
|---|---|---|
| 1 | Fixed Factor 0.7 | ☐ |
| 2 | Layer 12 × 9 cm | ☐ |
| 3 | 축 제목 Calibri 34 pt `#404040` | ☐ |
| 4 | 눈금 이름표 Arial 28 pt, 눈금선 없음 | ☐ |
| 5 | 컬러맵 흰→네이비 4단, 0–1050 | ☐ |
| 6 | 칸 숫자 Arial Bold 16 pt, 어두운 3칸은 흰 글씨 | ☐ |
| 7 | 칸 경계 흰색 2.5 | ☐ |
| 8 | 컬러바 제목 `structures generated` | ☐ |
| 9 | 아홉 칸이 **전부** 값이 있다 (0 없음) | ☐ |

---

## 이 가이드가 못 하는 것

- **칸당 두 줄 라벨을 네이티브로 못 만든다.** Origin 히트맵 라벨은 칸당 값 하나다 —
  둘째 줄(%)은 Text 객체 9개가 확실한 길이고, 생략해도 메시지는 산다.
- 라벨 글자색을 **칸 값에 따라 자동으로** 바꾸지 못한다. 파이썬 쪽은 `house_style.on_fill`
  이 배경 휘도로 자동 판정하지만, Origin 에는 그 기능이 없어 손으로 지정한다.
- Origin 버전별 메뉴 이름 차이를 다 담지 못한다 (2021 이후 기준).
