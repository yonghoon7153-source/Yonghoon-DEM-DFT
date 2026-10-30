# OVITO 렌더 사양 — 50kg 4차년도 DEM 보고 초안 2 (침대 끝 상태 3D)

3D 그림은 1저자가 OVITO · 웹앱에서 만든다.  여기 = 넣을 파일 · 색 · 시점 · 단면 제안 (값 · 계산 없음).

## 1. 파일

| 침대 | 파일 | 입자 | 상자 (µm) | 상태 |
|---|---|---|---|---|
| SE 0.7 µm (D0.7) | — | — | — | 결과 대기 |
| SE 1 µm (D1) | `ovito/D1_end_<step>_um.xyz.gz` (D1 끝 세트가 오면 러너가 만든다) | — | — | 결과 대기 |
| SE 2 µm (D2) | `ovito/D2_end_4015002_um.xyz.gz` | AM 1481 · SE 20872 | 50 × 50 × 122.469 | 판 고정 이완 끝 |
| SE 3 µm (D3) | `ovito/D3_end_4575002_um.xyz.gz` | AM 1482 · SE 6184 | 50 × 50 × 125.877 | 판 고정 이완 끝 |

- 원천 = 끝 세트 묶음의 `atom_end_<step>.liggghts` (덱 단위 × 1000 = µm) · 같은 step 의 contact · mesh 와 한 세트 (`data/<침대>/metrics_<침대>.json` 의 `ovito` · `provenance.end_set`).
- 형식 = 확장 XYZ (gzip · OVITO 가 바로 읽는다: File → Load File).  열:

| 열 | OVITO 속성 | 뜻 |
|---|---|---|
| `species` (글) | Particle Type | 상 이름 — `AM` (NCM) · `SE` |
| `pos` (3) | Position | x · y · z (µm) |
| `radius` | Radius | 반지름 (µm · AM 3 · SE 1 / 1.5) |
| `id` | Particle Identifier | 덤프 id |
| `dump_type` | (사용자 속성) | 덤프 type (1 = AM · 3 = SE) — `type` 이라는 이름은 OVITO 가 Particle Type 으로 읽어 `species` 와 겹치므로 이렇게 둔다 |

- 셀 = `Lattice` 50 × 50 × 끝 판 높이 (mesh) µm · `pbc="T T F"` (x · y 주기 · z 벽).  ⚠ 바닥 · 판 쪽 입자는 벽 · 판을 최대 0.4–1.35 µm 넘는다 (DEM 겹침 · 1쪽 단면은 선에서 잘랐다) — 3D 에서는 그대로 보인다.

## 2. 색 (50kg 계획 덱과 같음)

| 상 | HEX | OVITO RGB (0–1) |
|---|---|---|
| AM (NCM) | `#1A1A1A` | 0.102 · 0.102 · 0.102 |
| SE | `#CDB650` | 0.804 · 0.714 · 0.314 |
| 배경 | 흰색 | 1 · 1 · 1 |

Particle Types 목록에서 `AM` · `SE` 를 골라 색을 넣는다 (반지름 = 파일의 Radius 그대로 · 형식 기본 반지름은 쓰지 않는다).

## 3. 시점 제안

- 계획 덱의 기둥 렌더처럼 비스듬히 위에서: 원근 (Perspective) · 보는 방향 ≈ (1, 1, −0.7) (수평에서 약 30° 내려다봄) · 위 = +z.
- 네 침대를 **같은 배율**로: 첫 침대에서 "Zoom all" 뒤 그 시점 (위치 · 방향 · 시야각) 을 그대로 다른 침대에 쓴다 (Adjust View… 값 복사) — 침대마다 다시 맞추지 않는다.
- 셀 테두리 = 얇은 회색 또는 끔 · 렌더러 = Tachyon (주변광 가림 켬) 또는 OpenGL · 그림 아래 숫자 글 (D_SE · SE 수 · 크기비) 은 1쪽 띠 (`figs/p1_bed_strip.png`) 와 같은 값.

## 4. 단면 (1쪽 단면과 맞추기)

- Slice 수정자: 법선 (0, 1, 0) · 거리 25 µm (y = 25 µm 평면 = `figs/p1_bed_strip` 의 단면 자리) · 얇은 판을 보이려면 Slab width ≈ 6 µm (AM 지름 하나).
- ⚠ OVITO Slice 는 **입자 중심**으로 고른다 (구를 평면에서 자르지 않는다) → 1쪽 단면 (구 ∩ 평면 = 원) 과 같은 그림이 아니다.  캡션에 "중심이 y 25 ± 3 µm 인 입자" 처럼 적는다.

## 5. 쓰지 않을 말

- "300 MPa 상태" — 끝 상태는 판 고정 이완 끝 (끝 판 압력 D2 279.8 · D3 291.4 MPa · 가압 목표 300 MPa · 압력 도달 순간 세트 = 자료 없음).
- 3D 그림의 빈 곳 = 실험 기공 · 성형 후 기공 (언로딩 없음 · DEM 유효 E 규약 · 구 겹침 있음).
- 그림 하나로 입도 경향 판정 (입도별 시드 1).

## 6. (선택) ovito 파이썬

```python
from ovito.io import import_file
from ovito.modifiers import SliceModifier
pipe = import_file('docs/50kg/report_y4/draft2/ovito/D3_end_4575002_um.xyz.gz')
types = pipe.source.data.particles_.particle_types_
types.type_by_name_('AM').color = (0.102, 0.102, 0.102)
types.type_by_name_('SE').color = (0.804, 0.714, 0.314)
pipe.modifiers.append(SliceModifier(normal=(0, 1, 0), distance=25.0, slab_width=6.0))   # 선택
pipe.add_to_scene()
```
