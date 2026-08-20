---
title: extension roadmap
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [design, roadmap]
sources: [docs/adr/0002-own-wrd-parser.md, docs/adr/0001-store-raw-capacity-only.md]
confidence: medium
explored: false
verificationStatus: unverified
---

# 확장 로드맵 — 충방전 다음에 무엇이 오는가

충방전 경로가 템플릿이다. 새 분석은 같은 모양으로 붙으면 정규화·내보내기·
비교·그룹을 그대로 물려받는다. 절차는
`.claude/skills/adding-an-analysis/SKILL.md`.

## 이미 가능한 것 (새 코드 없이)

| 하고 싶은 것 | 방법 |
|---|---|
| 쿨롱효율 장기 추세 | `/api/compare/cycles?metric=coulombic_efficiency` |
| 사이클 수명 곡선 | `metric=discharge_capacity` 또는 `retention` |
| 분극 증가 추적 | `metric=voltage_hysteresis` — 실측 파일에서 0.040 → 0.408 V |
| 에너지 효율 | `metric=energy_efficiency` |

새 화면을 만들기 전에 **이걸로 답이 되는지 먼저 확인**한다.

## 1. dQ/dV (ICA) · dV/dQ — 가장 가깝다

이미 있는 `Profile` 의 순수 변환이다. 파서도 DB 도 건드리지 않는다.

- `wrdkit/ica.py`: `differential_capacity(profile, smoothing)` →
  `(voltage, dq_dv)`. 미분은 노이즈를 증폭하므로 **평활 방법이 결과를 좌우한다** —
  knee 검출과 같은 태도로, 방법을 하나로 정하지 말고 고를 수 있게 한다.
- 축은 전압, 값은 dQ/dV. 정규화는 기존 `ResolvedCell.divisor()` 를 그대로 쓴다.
- 화면은 `<Plot>` 재사용. 사이클 겹쳐 그리면 상전이 피크 이동이 보인다.

주의: CV 구간에서는 전압이 거의 일정해 dV → 0 이다. 그 구간을 잘라내지 않으면
발산한다. `CELL STATUS` 와 스케줄의 taper 조건으로 CC 구간만 고른다.

## 2. 미분 용량 기반 열화 모드 분해 (LLI / LAM)

ICA 위에 얹는다. 피크 면적과 위치의 변화를 추적해 리튬 재고 손실과 활물질
손실을 나눈다. **먼저 ICA 가 안정적으로 나와야 한다.**

## 3. EIS — 파일 포맷 조사가 먼저

`.wrd` 의 `eFormat` 은 관측 파일에서 0(사이클링)이었다. EIS 는 다른 확장자
(`.wis` 로 추정)이거나 다른 format 값일 것이다. **추측해서 파서를 쓰지 않는다.**

순서:

1. 실제 EIS 파일을 하나 확보한다.
2. `docs/raw/specs/` 에 포맷을 기록한다 — `wrd-binary-format.md` 와 같은 방식으로,
   무엇을 어떻게 확인했는지까지.
3. `synthetic.py` 에 그 포맷을 쓰는 코드를 넣는다. 쓸 수 있으면 이해한 것이다.
4. 그다음에 파서.

Nyquist 화면은 `<Plot>` 로 그린다 (Z' vs −Z''). 축 비율을 1:1 로 고정해야
반원이 반원으로 보인다.

## 4. EIS 등가회로 피팅

`R0 + (R1||CPE1) + (R2||CPE2) + W` 류의 모델을 복소 비선형 최소자승으로 맞춘다.
scipy 없이 하려면 Levenberg–Marquardt 를 직접 구현해야 하는데, 여기서는
**scipy 의존을 받아들이는 편이 낫다** — knee 의 조각선형 회귀와 달리 닫힌 해가
없다. ADR 로 남기고 `wrdkit[eis]` extra 로 격리한다.

피팅 결과는 **초기값과 가중치에 민감**하다. 반드시 잔차와 신뢰구간을 함께
보고하고, 수렴하지 않으면 숫자를 내지 않는다.

## 5. DRT

EIS 스펙트럼의 이완 시간 분포. Tikhonov 정칙화가 필요하고, **정칙화 파라미터
λ 가 결과를 지배한다**. knee 와 같은 문제다: 값 하나를 고르지 말고, λ 를
바꿔 가며 볼 수 있게 하고 선택을 화면에 남긴다.

EIS 가 안정적으로 들어온 다음의 일이다.

## 6. 그 밖에

- **GITT / 확산계수**: 스케줄에 펄스+휴지가 있으면 `segment_steps` 가 이미
  나눈다. `wrdkit/gitt.py` 로 붙일 수 있다.
- **율특성(rate capability)**: 사이클마다 C-rate 가 다른 스케줄. `CycleRecord`
  에 이미 `max_discharge_current_a` 가 있어 `c_rate` 로 그룹지을 수 있다.
- **온도 보정**: `temperature` 컬럼이 0 이 아닌 파일이 생기면.

## 무엇을 하든

1. `wrdkit` 에 순수 함수 + 합성 픽스처 테스트가 먼저다.
2. raw 단위만 저장한다 (ADR 0001).
3. 못 하는 것은 이유와 함께 `None` 을 돌려준다.
4. 실측 파일로 물리 검증을 한다.

## 관련

- [[bml-command]] — 개발 중에는 `bml dev` 로 띄우면 고칠 때마다 바로 반영된다
- [[wsl-setup]] — Windows/WSL 에서 개발할 때는 저장소를 `/mnt/c` 밖에 둬야
  파일 변경 감지가 동작한다
- `.claude/skills/adding-an-analysis/SKILL.md` — 새 분석을 붙이는 절차
