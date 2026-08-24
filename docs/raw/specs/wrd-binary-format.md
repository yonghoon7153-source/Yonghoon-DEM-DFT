---
title: WonATech .wrd binary format
created: 2026-08-20
updated: 2026-08-20
type: spec
status: verified-against-reference-file
---

# WonATech / Zive `.wrd` 파일 포맷

Smart Interface (Zive WBCS3000) 가 저장하는 충방전 원본 파일의 구조.
공개 스펙이 없어 실측 파일을 디코딩해서 확정했다. 이 문서는 `packages/wrdkit`
구현의 근거이며, 합성 픽스처 `packages/wrdkit/tests/synthetic.py` 가 여기 적힌
대로 파일을 만들어 낸다 (스펙이 틀리면 테스트가 깨진다).

## 검증에 쓴 파일

| | |
|---|---|
| 이름 | `No_1_dry_0.0316g_13pi_80wt%_0.2C_1000cyc_60oC_012.wrd` |
| 크기 | 19,599,508 B |
| 장비 | WBCS3000S1, S/N `W5K-BCSA0-1801020`, app 1.8.9.0 / fw 1.3.3.0 |
| 내용 | 148,493 샘플 / 45 사이클 / 22 컬럼 |

파서가 파일 끝까지 **남는 바이트 0** 으로 소비했고, 보고된 방전용량과 전류
적분값이 0.06 % 안에서 일치했다 (사이클 5: 4.9114 vs 4.9085 mAh).

## 전체 레이아웃

```
+--------------------------------------------------+ 0
| NRBF 스트림 1 : WbcsFile.Data.DataFileHeader      |  장비 정보 + 스케줄 + 리포트
+--------------------------------------------------+ 19,414
| NRBF 스트림 2 : WbcsFile.Data.DataHeader          |  컬럼 목록
+--------------------------------------------------+ 21,366
| 패킹된 데이터 행 × N (프레이밍 없음)               |  샘플
+--------------------------------------------------+ EOF
```

앞의 두 블록은 .NET `BinaryFormatter` 직렬화 스트림([MS-NRBF])이다. 각각
`MessageEnd`(레코드 타입 11)로 끝나므로, 첫 스트림을 읽은 위치에서 두 번째를
이어 읽으면 된다. 세 번째 블록부터는 NRBF 가 아니라 **고정 스키마의 구조체
배열**이며, 그 스키마는 스트림 2 가 선언한다.

## 스트림 1 — `DataFileHeader`

| 멤버 | 타입 | 비고 |
|---|---|---|
| `Version` | String | 파일 포맷 버전 (`1.3.0.0`) |
| `Model` | String | `WBCS3000S1` |
| `SIFVersion` `SerialNo` `OrderNo` `DeviceType` | String | |
| `AppVer` `FirmVer` | String | |
| `UnitCoulomb` | Boolean | **false = 용량이 Ah, true = C** |
| `BaseTick` | UInt32 | 장비 기본 tick (50,000 = 5 ms) |
| `FileName` | String | 저장 당시의 Windows 절대경로 |
| `StartTime` | DateTime | 상위 2비트 = `DateTimeKind`, 하위 62비트 = tick |
| `Format` | enum `DataFile+eFormat` | 관측값 0 |
| `SeqDataSet` | class | **스케줄 전체** (아래) |
| `StartReport` | class `TestReport` | 조작자가 입력한 셀 정보 |

`TestReport.CellWeight` / `ElectrodeArea` / `CellCapacity` 는 관측 파일에서
각각 `1.0` / `1.0` / `0.0` 이었다 — 기본값 그대로다. 즉 **조작자는 장비에
질량·면적을 입력하지 않는다.** 앱이 질량·면적을 다시 묻는 이유이며,
`WrdMetadata.has_operator_cell_data` 가 이 상태를 구분한다.

### `SeqDataSet` — 스케줄

`SeqDataSet.SeqDataList[0].SchData.SchStepList` 가 스텝 배열이다.
각 `SchStep` 은:

- `Name` — 편집기에서 붙인 이름 (`3STEP` 등, 순서와 무관)
- `Control.Type` (`eCtrlType`) — **0 = CC, 1 = CV, 7 = Rest, 13 = CCCV**
- `Control.Value` — 설정 전류 [A]. **부호가 방향** (+ 충전, − 방전)
- `Control.Value2` — CCCV 의 CV 전압 [V]
- `Control.Value3` — CCCV 의 taper(종료) 전류 [A]
- `Control.Loop.Count` + `CutOffConds.TurnStep` — 루프 대상과 횟수
- `CutOffCondsList[].CutOff1` / `CutOff2` — 종료 조건
  - `Type` (`eCutoffType`): **0 = 시간, 1 = 전압, 15 = 전류**
  - `Condition` (`eCondition`): **0 = 이상(≥), 1 = 이하(≤)**
  - `TimeValue` — tick, `Value` — V 또는 A
  - **`And2` 가 false 면 `CutOff2` 는 무장되지 않은 것**이다 (장비가 30 s 라는
    잔여값을 남겨 두므로 그대로 읽으면 모든 스텝이 30 초에 끝나는 것처럼 보인다)
  - CV taper 컷오프는 `Value` 가 0 이고 `Control.Value3` 을 따른다
- `SampCondList[]` — 로깅 주기. `Enable=true` 이고 `Type=0` 인 항목의
  `TimeValue` 가 시간 기준 샘플링 주기 [tick]

검증 파일의 스케줄을 디코딩한 결과:

```
0: Rest  7200 s
1: CCCV +0.5205 mA -> 3.63 V, taper 0.2603 mA     (formation, 0.1C)
2: Rest  60 s
3: CC    -0.5205 mA -> 1.88 V                      (formation)
4: Rest  60 s
5: CCCV +1.0410 mA -> 3.63 V, taper 0.5205 mA     (cycling, 0.2C)
6: Rest  60 s
7: CC    -1.0410 mA -> 1.88 V
8: Rest  60 s, loop -> '3STEP' x1000
9: Rest  (종료 대기)
```

파일명(`0.2C`, `1000cyc`)과 정확히 일치한다. formation 전류의 2배가 cycling
전류이므로 **C-rate 와 공칭 용량(1.041 mA ÷ 0.2 C = 5.205 mAh)을 역산**할 수 있다.

## 스트림 2 — `DataHeader`

| 멤버 | 타입 | 비고 |
|---|---|---|
| `DataCount` | Int64 | 관측값 **−1** (기록 중 확정되지 않음) |
| `EndTime` | Int64 | 관측값 **−1** (같은 이유) |
| `ColumnList` | `List<UnitDataInfor>` | 컬럼 정의 |

`DataCount` 가 −1 이므로 **행 수는 스캔으로 구해야 한다.**

`UnitDataInfor` 는 `Name`, `Unit`, `DataType` 을 갖는다. `DataType` 은
`System.UnitySerializationHolder` (`System.Type` 의 직렬화 형태)이고, 그 안의
평범한 필드 `Data` 에 .NET 타입명이 문자열로 들어 있다. **자동 프로퍼티가 아니라
평범한 필드**라서 `<Data>k__BackingField` 가 아니라 `Data` 로 찾아야 한다.

## 데이터 행

행 레이아웃은 `ColumnList` 가 선언한 순서·타입 그대로다. 검증 파일의 22 컬럼:

| # | 컬럼 | .NET 타입 | 크기 | 오프셋 |
|---:|---|---|---:|---:|
| 0 | `DATE TIME` | Int64 | 8 | 0 |
| 1 | `CHANNEL` | Int32 | 4 | 8 |
| 2 | `TEST TIME` | Int64 | 8 | 12 |
| 3 | `STEP TIME` | Int64 | 8 | 20 |
| 4 | `CYCLE TIME` | Int64 | 8 | 28 |
| 5 | `STEP INDEX` | Int32 | 4 | 36 |
| 6 | `TOTAL STEP` | Int32 | 4 | 40 |
| 7 | `CYCLE INDEX` | Int32 | 4 | 44 |
| 8 | `RUN STATUS` | Byte | 1 | 48 |
| 9 | `RUNNING STATUS` | Byte | 1 | 49 |
| 10 | `CELL STATUS` | Byte | 1 | 50 |
| 11 | `I RANGE INDEX` | Int32 | 4 | 51 |
| 12 | `I RANGE` | String | **가변** | 55 |
| 13 | `VOLTAGE` | Double | 8 | 56+L |
| 14 | `CURRENT` | Double | 8 | 64+L |
| 15 | `CHARGE Q` | Double | 8 | 72+L |
| 16 | `DISCHARGE Q` | Double | 8 | 80+L |
| 17 | `CHARGE E` | Double | 8 | 88+L |
| 18 | `DISCHARGE E` | Double | 8 | 96+L |
| 19 | `AUX. VOLTAGE` | Double | 8 | 104+L |
| 20 | `TEMPERATURE` | Double | 8 | 112+L |
| 21 | `OCP` | Double | 8 | 120+L |

행 크기 = **128 + L**, `L` = 현재 전류 레인지 문자열 길이.
`I RANGE` 는 **7-bit 길이 접두사 UTF-8 문자열**이라 행이 가변 길이다.
관측된 값: `1A`(L=2) → 130 B, `10mA`(L=4) → 132 B, `1mA`(L=3) → 131 B.
장비가 오토레인징으로 레인지를 바꾸는 순간 행 크기가 바뀐다.

### 단위와 의미

- **시간(`DATE TIME`, `TEST TIME`, `STEP TIME`, `CYCLE TIME`)은 .NET tick =
  100 ns.** 초로 바꾸려면 10,000,000 으로 나눈다. `DATE TIME` 은 0001-01-01
  기준 절대시각, 나머지는 경과시간.
- `VOLTAGE`, `AUX. VOLTAGE`, `OCP` — V. `CURRENT` — A (+ 충전, − 방전).
- `CHARGE Q` / `DISCHARGE Q` — `UnitCoulomb` 이 false 면 **Ah**.
  **사이클마다 0 으로 리셋되는 누적값**이다. 방전 중에는 `CHARGE Q` 가 그 사이클의
  충전 용량으로 고정된 채 `DISCHARGE Q` 만 증가한다.
- `CHARGE E` / `DISCHARGE E` — Wh (같은 규칙).
- `TEMPERATURE` — °C. 검증 파일은 센서 미연결이라 전 구간 0 이었다
  (챔버는 60 °C). **0 을 온도 0 °C 로 오해하면 안 된다.**
- `CELL STATUS` — **1 = 휴지, 3 = 충전, 4 = 방전.** 148,493 행 전체에서 전류
  부호와 완전히 일치했다 (휴지 5,520 행 전부 I=0, 충전 72,823 행 전부 I>0,
  방전 70,150 행 전부 I<0).
- `RUN STATUS` — 검증 파일 전 구간 5.
- `RUNNING STATUS` — 0–255 를 오가며 상태와 상관없음. 카운터로 보인다. 쓰지 않는다.
- `TOTAL STEP` — 전역 스텝 카운터(1부터 단조 증가). **스텝 분할은 이 값의 변화로
  하는 것이 가장 안전하다.**
- `CYCLE INDEX` — 0부터. 검증 파일에서 사이클 0 은 formation(스텝 0–4),
  1 이후가 루프(스텝 5–8)였다.

## Smart Interface 2.13 — 두 번째 모양 (`DataHeaderBase`)

2.13 부터 파일 앞이 달라진다. 스트림이 둘이 아니라 **하나**이고, 그 하나가
옛 헤더를 압축해 들고 있다 (ADR 0016).

```
[스트림 1]  WbcsFile.Data.DataHeaderBase
    Version    string   "1.6.0.0"      우리가 해독한 값은 이것뿐이다
    HeaderSize int32    6767           행 블록이 시작하는 **절대 오프셋**
    HeaderData byte[]   4574 바이트    raw DEFLATE (zlib/gzip 래퍼 없음)
        └─ 풀면 NRBF 스트림 하나
           root = WbcsFile.Data.DataHeaderValues
             Version/Model/SerialNo/OrderNo/DeviceType/AppVer/FirmVer
             UnitCoulomb, BaseTick, FileName, StartTime, Format
             EndTime (DateTime — 1.x 의 tick int64 가 아니다)
             DataCount (int32)
             LastRunStatus, _seqDataSet, _IRangeString, _SeqDHistoryList
[HeaderSize 부터]  행 블록
```

주의할 점 셋.

1. **행은 `HeaderSize` 에서 시작한다.** 스트림이 끝나는 곳이 아니다. 실측
   파일에서 스트림은 4770 에서 끝났는데 `HeaderSize` 는 6767 이었다 — 사이의
   1997 바이트는 쓰이지 않는다. "마지막 스트림 다음" 에서 읽으면 쓰레기를
   행으로 읽는다.
2. **`HeaderData` 는 raw DEFLATE 다.** `zlib.decompress(blob)` 는
   `incorrect header check` 로 실패한다. `zlib.decompress(blob, -15)`.
3. **스케줄은 `_seqDataSet`** 이다 (1.x 는 `SeqDataSet`). 안쪽 구조는 같다.

### 행 레이아웃 (128 바이트 고정, **파일이 선언하지 않는다**)

1.x 는 `DataHeader.ColumnList` 로 컬럼을 선언한다. **2.13 은 하지 않는다** —
그래서 이 표가 유일한 계약이다. 근거는 ADR 0016 에 있고, `synthetic.py` 의
`build_wrd_sif213` 이 같은 표로 파일을 쓴다.

| 오프셋 | 형 | 이름 | 어떻게 확정했나 |
|---:|---|---|---|
| +0 | Int32 | CHANNEL | 27 고정, 헤더의 채널과 일치 |
| +4 | Int64 | TEST TIME | 유일하게 단조 증가, 마지막 41,452 s |
| +12 | Int64 | STEP TIME | 스텝 경계에서 리셋 |
| +20 | Int64 | CYCLE TIME | 사이클 경계에서 리셋 |
| +28 | Int32 | STEP INDEX | 0..8, 여덟 번 변화 |
| +32 | Int32 | TOTAL STEP | 1..9, 헤더의 SchStep 9개와 일치 |
| +36 | Int32 | CYCLE INDEX | 이 조각에서는 0 고정 |
| +40 | Byte | RUN STATUS | **미확정** (5 고정) |
| +41 | Byte | SUB STATUS | **미확정** (초당 여러 번 변한다) |
| +42 | Byte | **CELL STATUS** | 전류 0 인 300행에서 1, 전류 흐르는 41,438행에서 3 |
| +43 | Byte | CONTROL STATUS | 1→평균 0.324 A(CC), 2→0.032 A(CV), 0→0 A |
| +44 | Double | VOLTAGE | 2.585–4.250 V |
| +52 | Double | CURRENT | 0–0.352 A |
| +60 | Double | CHARGE Q | 0–3.661 Ah (MJ1 정격) |
| +68 | Double | DISCHARGE Q | 이 조각은 충전만 하므로 0 |
| +76 | Double | CHARGE E | 0–13.85 Wh |
| +84 | Double | DISCHARGE E | 0 |
| +92 | Double | AUX. VOLTAGE | 이 장비는 0 |
| +100 | Double | TEMPERATURE | 이 장비는 0 |
| +108 | Double | OCP | 2.878–2.879 V (휴지 전압) |
| +116..127 | — | **미상 12바이트** | 이름을 붙이지 않는다 |

1.x 와 다른 점: **DATE TIME 이 없고**, **I RANGE 문자열이 없다** (그래서 행이
가변 길이가 아니다), 상태 바이트가 셋이 아니라 넷이다.

**교차검증**: CC 구간에서 ΔQ ÷ (I·Δt) 의 중앙값 = 1.0000. 전류 단위(A)·용량
단위(Ah)·시간 단위(tick)가 동시에 맞아야 나오는 값이다.

## 파싱 전략

1. 스트림 1 → 장비·스케줄·리포트.
2. 스트림 2 → 컬럼 목록 → 행 레이아웃 계산 (**하드코딩 금지**).
3. 데이터 블록을 한 번 훑어 각 행의 시작 오프셋과 문자열 길이를 기록한다
   (`buf[off+55]` 만 읽으면 되므로 매우 싸다).
4. 문자열 길이가 같은 **연속 구간(run)** 별로 numpy structured dtype
   (`offsets` + `itemsize` 지정)을 만들어 `np.frombuffer` 로 한 번에 읽는다.
   → 148k 행 0.37 s (행 단위 파이썬 루프 대비 5배).
5. 유효하지 않은 행(문자열 길이 접두사가 multi-byte 등)이 나오면 멈추고
   `trailing_bytes` 로 보고한다. 파일 끝의 푸터를 데이터로 오독하지 않는다.

## 아직 모르는 것

- `Format` (`eFormat`) 이 0 이 아닌 파일. EIS(`.wis`) 등 다른 측정은 레이아웃이
  다를 수 있다. 현재 파서는 `data_format` 을 기록만 하고 통과시킨다.
- `eCtrlType` 의 나머지 값 (2–6, 8–12) — 관측 파일에 없었다.
- `RUNNING STATUS` 의 의미.
- 멀티채널 파일에 여러 `CHANNEL` 값이 섞이는지 (검증 파일은 채널 11 단일).

새 값을 만나면 이 문서에 추가하고 `synthetic.py` 에도 반영한다.
