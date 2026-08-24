---
title: BioLogic .mpr / .mpt / .mps formats
created: 2026-08-24
updated: 2026-08-24
type: spec
status: verified-against-reference-file
---

# BioLogic EC-Lab `.mpr` · `.mpt` · `.mps`

VSP-300 이 EIS 를 재고 남기는 세 파일의 구조. `packages/wrdkit/eis/biologic.py`
구현의 근거이고, 합성 픽스처 `packages/wrdkit/tests/synthetic_eis.py` 가 여기
적힌 대로 파일을 만든다 — **스펙이 틀리면 테스트가 깨진다.**

## 검증에 쓴 파일

| | |
|---|---|
| 이름 | `260719_No1_55_70um_sym_01_C01.mpr` (+ 짝이 되는 `.mps`) |
| 크기 | 22,512 B |
| 장비 | VSP-300, EC-Lab v11.63 |
| 내용 | PEIS 89점, 7 MHz → 10 mHz, 10 pts/decade, 5 mV, 대칭셀(70 µm) |

읽어 낸 `Re(Z)`·`Im(Z)` 로 다시 계산한 `|Z|` 와 위상이 파일이 따로 저장한
`|Z|/Ohm`·`Phase(Z)/deg` 컬럼과 각각 1e-4·1e-3 상대오차 안에서 일치했다. 두
컬럼이 같은 복소수를 말한다는 뜻이고, 부호를 뒤집어 읽었으면 위상이 통째로
어긋난다.

## `.mpr` — 바이너리 원본

```
0x00  "BIO-LOGIC MODULAR FILE\x1a"  + 공백 패딩
0x34  MODULE ...                    모듈이 파일 끝까지 이어진다
```

### 모듈 헤더 (65 B, 고정)

| 오프셋 | 크기 | 내용 |
|---|---|---|
| 0 | 6 | `MODULE` |
| 6 | 10 | 짧은 이름 — `VMP Set`, `VMP data`, `VMP LOG`, `VMP loop` |
| 16 | 25 | 긴 이름 |
| 41 | 4 | `0xFFFFFFFF` (관측 파일 전부) |
| 45 | 4 | **payload 길이** (uint32) |
| 49 | 4 | 0 |
| 53 | 4 | 모듈 버전 (uint32) — Set=10, data=11, LOG=10 |
| 57 | 8 | 날짜 `MM/DD/YY` |

세 모듈의 `65 + 길이` 합이 파일 크기와 정확히 맞는다 (52 + 6812 + 7480 + 8168
= 22,512). 길이 필드의 위치를 확인한 방법이 이것이다.

### `VMP data` payload

```
+0   uint32   행 수
+4   uint16   컬럼 수          ← uint8 이 아니다
+6   uint16[] 컬럼 id 목록
...  가변 길이 preamble
끝   행 블록 (행 = 컬럼들을 패딩 없이 이어 붙인 것)
```

**컬럼 수는 16비트다.** 8비트로 읽으면 다음 바이트가 첫 컬럼 id 의 하위
바이트가 되어 id 목록 전체가 256배로 어긋난다 — 값이 그럴듯해서 조용히 틀린다.

**preamble 길이는 버전마다 다르다** (이 파일은 1007 B). 그래서 리더는 행 블록을
payload **끝에서부터** 잡는다: `행 시작 = payload 끝 − 행 수 × 행 크기`. 이것은
추측이 아니라 검산이다 — 컬럼 폭이 하나라도 틀리면 행 시작이 헤더를 침범하고,
그때 리더는 멈춘다.

### 컬럼 id

행 크기를 정하는 것이 폭이므로, 폭이 틀리면 **그 뒤의 모든 컬럼이 밀린다.**
모르는 id 는 `UnknownColumn` 으로 멈춘다 (§0.4). 표는
`wrdkit/eis/biologic.py::COLUMNS` 에 있고, 검증 파일이 쓴 것은 다음 16개다.

| id | 이름 | 폭 |
|---|---|---|
| 4 | `time/s` | f8 |
| 13 | `(Q-Qo)/mA.h` | f8 |
| 24 | `cycle number` | f8 |
| 32 | `freq/Hz` | f4 |
| 33 | `\|Ewe\|/V` | f4 |
| 34 | `\|I\|/A` | f4 |
| 35 | `Phase(Z)/deg` | f4 |
| 36 | `\|Z\|/Ohm` | f4 |
| 37 | `Re(Z)/Ohm` | f4 |
| 38 | `-Im(Z)/Ohm` | f4 |
| 39 | `I Range` | u2 |
| 76 | `<I>/mA` | f4 |
| 77 | `<Ewe>/V` | f4 |
| 131 | `Ns` | u2 |
| 169 | `Cs/µF` | f4 |
| 172 | `Cp/µF` | f4 |

합 72 B/행 × 89행 = 6,408 B, payload 7,415 B − preamble 1,007 B 와 일치한다.

### 부호 — 가장 조용한 함정

파일이 저장하는 것은 **`-Im(Z)`** 다. 나이퀴스트 세로축이 그것이기 때문이다.
그대로 `Im(Z)` 로 읽으면 스펙트럼이 실수축을 기준으로 뒤집힌다 — 용량성 아크가
유도성 아크가 되고, 아무것도 예외를 던지지 않으며, 피팅만 수렴하지 않는다.
`wrdkit` 은 읽는 순간 부호를 뒤집어 물리 관례(`Z = Z′ + jZ″`, 커패시터는
`Z″ < 0`)로 맞추고, 파일이 쓴 컬럼은 이름 그대로 `columns` 에 남겨 둔다.

## `.mpt` — ASCII 내보내기

```
EC-Lab ASCII FILE
Nb header lines : 62
...
freq/Hz	Re(Z)/Ohm	-Im(Z)/Ohm	...      ← 62번째 줄
7.000018E+006	7.472730E+000	...        ← 63번째 줄부터 데이터
```

`Nb header lines` 는 **컬럼 이름 줄까지 센다.** 그 다음 줄을 이름으로 읽으면
첫 데이터 행이 이름이 되고, 그러면 `freq/Hz` 를 못 찾아 읽기가 실패한다.

소수점은 **PC 로케일을 따른다.** 한국어 Windows 에서 내보낸 파일은 `7,472730`
이고, 그대로 `float()` 하면 전부 NaN 이 된다.

## `.mps` — 설정 파일

ISO-8859 텍스트, CRLF. `키 : 값` 줄과, 테크닉 블록의 `이름␣␣␣␣값` 2열 레이아웃이
섞여 있다. 스윕에 관한 것만 뽑는다.

| 필드 | 뜻 |
|---|---|
| `Technique :` 다음 줄 | 테크닉 이름 (`Potentio Electrochemical Impedance Spectroscopy`) |
| `fi` + `unit fi` | 시작 주파수 |
| `ff` + `unit ff` | 끝 주파수 |
| `Nd` | decade 당 점 수 |
| `Va (mV)` | 진폭 — 5~10 mV 여야 Butler-Volmer 선형화가 선다 |
| `Na` | 평균 횟수 |

모르는 단위는 환산하지 않고 문자열 그대로 둔다 (§0.4).

## 관련

- ADR 0019 — EIS 를 왜 독자 섹션으로 두는가, 액체와 전고체를 왜 가르는가
- `packages/wrdkit/tests/test_eis_biologic.py` — 이 문서의 주장마다 시험이 하나씩
