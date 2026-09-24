# Codex 리뷰 요청 — LHS 130 인계표의 **두께 · porosity · φ 정의** (벽 겹침 · 분리막 바닥 · 음수 porosity)

> 작성 2026-09-24 · 브랜치 `claude/stoic-knuth-NObVQ` · 데이터 커밋 **`425cee222`** (재수확 130/130)
> 목적 = LHS 130 인계표 (설계 → 구조 데이터셋, 외부 전달 예정) 를 **재생성하기 전에** 두께 · porosity · φ 의 정의를 확정한다.
> 판단 기록 = `docs/reviews/lhs_handover_judgments_20260924.md` (J1–J17) · 데이터 = `docs/data/lhs_descriptors_20260924/README.md` ·
> 결함 원장 = `docs/reviews/findings.json` (`LHS-10` ~ `LHS-15` · `SELF-47` ~ `SELF-49`)
>
> ⚠ **설계 재심이 아니다.**  130 설계점 · 덱 · 타깃 목록 (`docs/data/lhs_design_20260818.csv`) 은 그대로다.
> 쟁점은 셋 — **벽과 겹친 부피를 어떻게 셀지 · 두께를 어디서 잴지 · 음수 porosity 를 어떻게 다룰지**.
> 인계표는 이 리뷰 판정까지 **배포 보류**다.

---

## 0. 오늘 (09-24) 고친 것 — 배경

| 원장 | 무엇이 틀렸나 | 고친 것 |
|---|---|---|
| `LHS-10` | 수확기 분모 바닥이 덤프 상자 바닥 (벽보다 10 µm 아래) | 벽 z = 0 에서 잰다 — 웹앱 `calc_porosity` 와 같은 식 (커밋 `0424795d6`) |
| `LHS-11` | 97/130 이 원자 덤프보다 이른 (압축 중) 플래튼 메시 | 같은 step 메시만 받는다 · 원본에서 재반입 (옮길 때 문자열 정렬이 원인) |
| `LHS-12` | 새 가드 (입자 바닥이 벽 아래 ½·r_max 넘으면 거부) 가 58 건 거부 — 연속 분포를 자름 | 가드 삭제 · 바닥은 덱 `zplane` 으로 직접 확인 · 벽 밖 부피는 **기록** (커밋 `4ee1038c3`) |

결과 (커밋 `425cee222`): 수확 130/130 · 교차검사 (수확기 함수 ↔ 웹앱 함수를 같은 덤프에 호출) **SAME 130** (잔차 5.6e-14 %p) ·
플래튼 − 고체 윗면 −1.21 … −0.27 µm.  옛 판 대비 porosity −15.8 … −48.6 %p · φ_SE ×1.21–2.01.

## 1. 덱 (130 건 공통 — 사용자 grep, `lhs00_000` bimodal · `lhs00_110` mono)

```
boundary        p p f
region reg_box block 0.0 0.05 0.0 0.05 -0.01 1.0 units box          # 길이 ×1000 스케일: sim 0.001 = 실물 1 µm
fix m1 all property/global youngsModulus peratomtype 1.4e8 1.4e8 0.135e7   # AM_P AM_S SE (mono: 1.4e8 0.135e7)
fix m2 all property/global poissonsRatio peratomtype 0.25 0.25 0.30
fix m9 all property/global characteristicVelocity scalar 2.0
fix zwall_bot all wall/gran model hooke/hysteresis tangential history rolling_friction cdt primitive type 3 zplane 0.0   # 바닥 = SE 물성 (mono: type 2)
fix top_mesh all mesh/surface/stress file plate_<case> type 1 ...          # 플래튼 = AM 물성
fix gravi all gravity 98.1 vector 0.0 0.0 -1.0      # 삽입 단계 → 가압 단계는 9.81
```

★ **바닥 SE 는 의도다** (저자 09-24): 실제 양극 가압에서 양극 밑은 **SE 분리막**, 위는 **SUS 플런저** (AM 물성으로 충분).
생산 덱 (`docs/data/phase_a_6mah/in.real_4.liggghts`) 은 바닥 · 플래튼 **모두 AM (type 1)** — LHS 와 생산 코퍼스의 계통 차이다 (`LHS-14`, wontfix).

## 2. 정의 (현재 코드)

- **(가) 주 값 = 웹앱 ε_sphere** — ε = 1 − ΣV / (L_x·L_y·plate_z) · φ_SE = V_SE / (…) · φ_AM = V_AM / (…) · 두께 = plate_z (벽 z = 0 부터).
  plate_z = 같은 step 플래튼 STL 꼭짓점 z 평균 (평판).  ΣV 는 **구 부피 전부** — 벽 밖으로 나간 부분도 센다.
- **(나) 되돌려 놓기** (`wall_record.pushback`) — 벽 밖 cap 부피 V_out (바닥 아래 + 플래튼 위, 구 cap π h²(3r − h)/3) 를 벽 안으로
  되돌려 얇은 고체층으로 쌓았다고 본다: H′ = plate_z + V_out / (L_x·L_y) · ε′ = 1 − ΣV / (L_x·L_y·H′).  물질 · 빈틈 보존, 두께만 증가.
- **(다) 잘라내기** (구현 안 함) — 벽 밖 부피를 버린다: ε″ = 1 − (ΣV − V_out) / (L_x·L_y·plate_z).
- ε_union (웹앱 `calc_porosity_dual`) 은 **입자쌍 렌즈만** 뺀다 — 벽 겹침은 안 뺀다.
- 코드: `scripts/lhs_descriptor_harvest.py` (`check_deck_floor` · `volumes_and_phi` · `_wall_side`) · `scripts/lhs_harvest_batch.py`
  (`pick_mesh` · `run_one`) · `scripts/lhs_phi_crosscheck.py` · 웹앱 `scripts/dem_analysis_core.py:35` · `scripts/parse_liggghts.py:314`.
- 인계표 생성기: `scripts/lhs_design_dataset.py` (`--harvest` · `--export-handover`) — 아직 옛 판 (09-19) 을 기본값으로 가리킨다 (재생성 전).

## 3. 실측 (130 건)

| 양 | 중앙 | p90 | 최대 | 최소 |
|---|---|---|---|---|
| (가) porosity (%) | 9.89 | 21.9 | 27.1 | **−2.43** |
| (나) − (가) porosity (%p) | 0.61 | 1.06 | 2.53 | 0.19 |
| (나) 두께 증가 (µm) | 0.23 | 0.41 | 1.07 | 0.09 |
| 바닥 밖 부피 / ΣV (%) | 0.60 | 1.43 | 4.39 | 0.19 |
| 플래튼 밖 부피 / ΣV (%) | 0.08 | 0.16 | 0.21 | 0.02 |

- 설계군별 (가) 중앙 · (나) − (가) 중앙 (최대): bimodal (100) 9.32 · 0.60 (1.45) · mono_AM_S (15) 12.46 · 0.48 (1.00) ·
  **mono_AM_P (15) 11.00 · 1.20 (2.53)**.
- 가장 깊이 박힌 입자의 상: AM_P 66 · AM_S 33 · AM (mono) 29 · SE 2.  깊이 ∝ 가장 큰 AM 반지름 (corr log 0.877 — 판단 J14).
  겹침/반지름 중앙 0.61 · p90 1.98 · 최대 4.87.
- 중심이 바닥 **아래**인 입자가 있는 케이스 **42** (AM_S 618 개 · SE 62 · AM 2) · 통째로 바닥 아래 15 케이스 (최대 21 개, 대부분 SE) ·
  통째로 플래튼 위 3 케이스 (SE).
- 가장 깊은 입자의 겹침/반지름이 **정확히 1.98** 인 케이스 9 (r = 1 µm 7 · r = 0.5 µm 2) — 입자 윗면이 바닥 위 0.02·r.  독립 런에서 같은
  비율이 반복된다 (`LHS-13`, 원인 미상).  부피 몫은 무시할 만하다 (고체의 0.005–0.007 %).
- **음수 ε_sphere**: (가) **18** 건 (bimodal 14 · mono_AM_P 2 · mono_AM_S 2, −2.43 … −0.09 %) · (나) 16 건 ⇒ 벽이 아니라 **입자끼리**
  겹침 과다 (`LHS-15`).  생산 코퍼스는 음수 ε_sphere 케이스를 코퍼스 밖에 둬 왔다.

## 4. 질문

**Q1. 주 값.**  바닥이 의도된 SE 분리막일 때 인계표의 주 porosity · φ 는 (가) · (나) · (다) 중 무엇이어야 하나?
우리 가설 (판단 J17): (가) = LHS 고유 값 (분리막 위에서 누른 침대 그대로), (나) ≈ "바닥이 단단했다면" — 생산 덱 (바닥 AM) 코퍼스와
나란히 볼 때의 값.  이 해석이 맞나?  (나) 의 "균일한 얇은 층" 가정이 한쪽으로 치우치나 (실제로 단단한 바닥이면 하중을 받는 알이
통째로 올라가 두께가 더 늘 수 있다)?

**Q2. 두께.**  인계표의 두께 측정값은 plate_z (틀 간격) · H′ ((나)) · 고체 윗면 기반 중 무엇이어야 하나?  실험 두께 (마이크로미터 ·
단면 SEM) 와 비교할 때 어느 것이 대응하나?  porosity 와 두께는 **한 정의에서 같이** 나와야 한다는 원칙 (판단 J3) 을 지키는가?

**Q3. 바닥 확인.**  덱의 `wall/gran … primitive … zplane` 이 0 인지를 직접 읽는 것 (`check_deck_floor`) 으로 "벽 = 0" 가정의 점검이
충분한가?  빠진 경우 (메시 바닥 · 여러 벽 · 런 중 `unfix` 등) 는?

**Q4. 벽 관통.**  중심이 바닥 아래인 입자가 42 케이스에 있고, 겹침/반지름 1.98 자리가 9 케이스에서 반복된다.  LIGGGHTS `wall/gran`
primitive 면 (양면 여부 · hooke/hysteresis · SE 물성 벽) 에서 이것이 어떤 기전으로 생기나?  케이스를 무효로 할 수치 결함의 신호인가,
기록만 하면 되는가?

**Q5. 음수 porosity.**  18 건 (ε_sphere < 0) 을 설계 → 구조 데이터셋에서 어떻게 다뤄야 하나 — 표지만 달기 · 회귀 타깃에서 빼기 ·
ε_union 병기 · 다른 규약?  φ_SE + φ_AM > 1 이 타깃에 들어가는 문제를 포함해서.

**Q6. 웹앱 쪽 구멍** (판단 J15): 메시 step 을 원자 덤프와 맞춰 보지 않는다 (`SELF-47`) · 재계산 도구의 점검이 플래튼이 **낮을 때만**
잡는다 (`SELF-48`) · 무메시 fallback · 음수 무경고 등 (`SELF-49`).  기존 생산 코퍼스를 위해 지금 고쳐야 할 것은?  코퍼스 전수 점검
(플래튼 − 고체 윗면) 이 필요한가?

**Q7. 빠뜨린 것.**  분리막과 서로 박힌 경계에서 φ · coverage · τ 의 정의에 더 걸리는 것이 있나?

## 5. 원하는 답의 형식

- 질문마다 **판정 (ACCEPT / REVISE / REJECT)** + 근거 (덱 · 코드 · 수치 인용) + 고칠 것.
- 인계표에 넣을 **열 이름 · 정의 제안** (주 값 · 보조 값 · 표지).
- 모르는 것은 "모른다" 로 적을 것 — 추정으로 메우지 말 것.

## 6. 읽을 것

- 판단 기록 `docs/reviews/lhs_handover_judgments_20260924.md` — J1 (ε_sphere 기록 전용) · J3 (두께 원칙) · J11 (웹앱 1순위) · J14 · J16 · J17.
- 데이터 `docs/data/lhs_descriptors_20260924/README.md` · 케이스별 `lhs00_*.json` 의 `wall_record` · `deck_floor` ·
  교차검사 표 `_phi_crosscheck.tsv` · 수확 요약 `docs/data/lhs_descriptors_20260924/_batch_summary.json`.
- 코드 `scripts/lhs_descriptor_harvest.py` · `scripts/lhs_harvest_batch.py` · `scripts/lhs_phi_crosscheck.py` · `scripts/dem_analysis_core.py` ·
  `scripts/parse_liggghts.py` · `scripts/recompute_porosity_dual.py` · `scripts/analyze_contacts.py`.
- 코호트 `docs/data/area_s2_cohort.tsv` (atom · contact · deck 짝과 sha 봉인).
