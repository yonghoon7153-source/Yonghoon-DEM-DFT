---
title: 임피던스 논문 지식 — 무엇을 배웠고 어디에 썼나
created: 2026-09-23
updated: 2026-09-23
type: synthesis
tags: [electrochem]
sources: [raw/papers/ISW1990.md, raw/papers/HIRSCHORN2010.md, raw/papers/SCHOENLEBER2014.md, raw/papers/VADHVA2021.md, raw/papers/LASIA1999.md, raw/papers/ECSIF2019.md]
confidence: medium
explored: false
verificationStatus: unverified
---

# 임피던스 논문 지식 — 무엇을 배웠고 어디에 썼나

EIS 검수(`bml audit`, [[bml-command]])의 판정은 논문 몇 편에 기댄다. 어떤
커패시턴스가 어느 과정인지, 유효 커패시턴스에 어느 저항을 넣는지, KK 검사의 크기를
어떻게 정하는지가 그렇다. 2026-09-23 에 여섯 편을 에이전트가 읽어 **기록 191개**로
정리했다 (ADR 0042). 이 페이지는 그 기록의 지도다. 기록 자체는 코드 옆에 있다.

- 기계용: `packages/wrdkit/src/wrdkit/eis/knowledge/*.json` — `from wrdkit.eis import
  knowledge` 로 `record(id)`, `cite(id)`, `search(topic=…, text=…)`.
- 읽은 노트: `docs/raw/papers/<KEY>.md` — 논문마다 요지, 핵심, 우리 코드와 어긋난 곳.
- 판정 → 근거: `wrdkit/eis/audit.py` 의 `REFERENCES`. `bml audit` 글 끝의 "━━ 근거"
  목록이 이것을 쪽 번호까지 풀어 쓴다.

## 여섯 편

| 키 | 무엇 | 우리에게 가장 쓸모 있는 기록 |
|---|---|---|
| ISW1990 | Irvine·Sinclair·West, *Adv. Mater.* 2, 132 — 커패시턴스로 아크 가르기 | 표 1 (`table1-capacitance-interpretation`), 그림 4b 의 "벌크 반원이 창 밖이면 절편이 R_b" (`bulk-arc-off-scale`), 막는 전극의 수직 스파이크 |
| HIRSCHORN2010 | Hirschorn 외, *Electrochim. Acta* 55, 6218 — CPE 에서 유효 C | 식 (12) 막는 계면은 옴 저항으로 (`brug-surface-blocking-eq12`), 식 (18) 은 두께 방향 분포에만 (`hsu-mansfeld-normal-eq18`), 틀린 식이면 −70 % ~ +100 % |
| SCHOENLEBER2014 | Schönleber 외, *Electrochim. Acta* 131, 20 — lin-KK 의 크기 정하기 | μ = 1 − Σ\|R<0\|/Σ\|R≥0\|, c = 0.85 (`mu-threshold-c`), 잔차는 \|Z\| 대비 (`residuals`), **잔차 수치 기준은 없다** |
| VADHVA2021 | Vadhva 외, *ChemElectroChem* 8, 1930 — 전고체 EIS 리뷰 | 황화물은 벌크·입계가 겹친다 (`sulfide-bulk-gb-overlap`), 직렬 저항이 R_SE,bulk (`in-li-full-cell-assignment`), 진폭 50 mV 미만, 모델 전에 KK |
| LASIA1999 | Lasia, *Modern Aspects of Electrochemistry* 32, 143 — EIS 교과서 장 | KK 는 decade 당 6–7 개 Voigt (`kk-linear-voigt-test`), 막는 계는 어드미턴스로, CPE 지수의 뜻, 모듈러스 가중 |
| ECSIF2019 | ECS Interface 2019 여름호 — Bio-Logic 품질 지표 광고, Gupta·Sakamoto 고분자/LLZTO 계면 | 절대 위상이 얕아도 막는 셀 (`GUPTA2019.blocking-tail-shallow-absolute-phase`, 우리가 그림에서 읽은 것), THD·NSD·NSR 의 정의뿐 |

받은 파일 이름에 속지 않도록: `b113771.pdf` 는 Lasia 의 1999 장이다 (Orazem–Tribollet
교재가 아니다). `…Interface_28_1.pdf` 는 2019 여름호(28권 2호)다.

## 검수와 계산에 들어간 것

| 무엇을 배웠나 | 근거 | 어디에 |
|---|---|---|
| 막는 꼬리의 C 는 Brug 식에 **옴 저항**을 넣는다. 아크 자신의 R (경계값) 로 내면 17 배까지 틀린다 | HIRSCHORN2010 식 (12) | `audit._blocking_capacitance` — 커밋 전 코드의 오류를 에이전트가 짚었다 |
| 벌크 크기 아크가 없으면 벌크는 절편 R0 에 있다: 전해질 = R0 + 입계 크기 아크 | ISW1990 그림 4b, VADHVA2021 그림 9a | `derive.ionic_conductivity`, 검수 `bulk_above_window` (ADR 0041) |
| 유효 C 식은 분포 가정에 따라 0.3–2 배 흔들린다 → 결정된 값도 ×3 흔들어 쪽이 같을 때만 가른다 | HIRSCHORN2010 3.1절 | `capacitance.DETERMINED_SPREAD` |
| 직렬 저항 설명의 "전해질 저항이 아닙니다" 는 황화물에서 틀렸다 | VADHVA2021, ISW1990 | `derive.KINDS[SOLID]` |
| 표 1 의 경계가 우리 표와 같다 (시험이 묶는다) | ISW1990 표 1 | `test_eis_knowledge.py` |
| 막는지는 위상에 더해 꼬리의 방향으로 — 저항이 크면 막는 셀도 마지막 위상이 얕다 (−22 ~ −28°, 꼬리 72–77°) | GUPTA2019 (그림에서 읽음), LASIA1999 (CPE 꼬리 n·90°) | `derive.blocking_verdict` (ADR 0044) |
| 회로보다 먼저 점을 본다 — lin-KK, M 은 μ < 0.85 에서 멈춘다. 잔차 기준(2 %, 잡음 6σ)은 우리 것이다. μ 가 일찍 멈추면(날카로운 아크) 판정하지 않는다 | SCHOENLEBER2014, VADHVA2021, LASIA1999 | `kk.lin_kk`, `audit.audit_spectrum` (ADR 0043) |

## 아직 안 한 것

논문이 권하는데 코드에 아직 없는 것이다. 우선순위 순서로 적는다.

1. **진폭.** 50 mV 를 넘으면 선형성을 의심한다 (VADHVA2021). `amplitude_mv` 는 이미
   저장되어 있다.
2. **저주파 끝이 유도성(+Im)이면** 측정 중 셀이 변한 것일 수 있다 (VADHVA2021,
   LASIA1999).
3. **아크마다 겉보기 εr.** εr = C·l/(A·ε0) 다. 벌크라 부른 아크의 εr 이 10⁴ 이면 누구나
   "벌크가 아니다" 를 확인할 수 있다 (ISW1990).
4. **자동 회로 선택에 AIC** (VADHVA2021). 지금은 χ² 가 가장 작은 것을 고른다.
5. **docstring 고칠 곳** (LASIA1999)
   - n > 1 인 CPE 는 인덕터가 아니라 음의 저항이다.
   - `fit.py` 의 가중은 "모듈러스 가중" 이다.
   - 전송선의 "R_ion/3" 은 막는 계면이거나 Rct ≫ R_ion 일 때만 맞다.
   - 안 막는 셀에 반무한 W 회로를 권하면 안 된다 — W 도 발산한다.

**랩이 정할 것 — Arrhenius 의 세로축.** VADHVA2021 (식 7) 은 전지수의 1/T 을 넣은
ln(σT) 가 Ea 를 맞게 준다고 한다. 우리 `activation_energy` 는 두 기준을 다 내고
(`basis`), 기본은 랩 관행인 ln σ 다. 같은 아홉 점에서 0.328 과 0.353 eV 가 나온다
(ADR 0039). 어느 쪽인지 늘 함께 적으므로 틀린 수는 아니다. 기본값을 바꿀지는 랩이
정한다.

## 함정 — 논문을 그대로 옮기면 틀리는 곳

- **VADHVA2021 식 5** 는 위상을 Re/Im 으로 적었다 (거꾸로다). 우리 `arctan2(Im, Re)` 가
  맞다.
- **GUPTA2019 의 "CPE (F/cm²)"** 는 유효 커패시턴스가 아니라 CPE 의 Q 다. 지수가 0.73–1.0
  이라 2–4 배 크다. 픽스처로 옮기지 않는다.
- **HIRSCHORN2010 에는 power-law 모델도 g(α) 도 없다.** 인용하지 않는다.
- **ISW1990 표 1 은 F 한 열뿐이다.** l/A = 1 cm⁻¹ 은 벌크 값을 끌어낸 문장에만 나온다.
  C·l/A 와 C/A 로 나눈 것은 우리 추론이다 (식 3·4 와 맞는다).
- **VADHVA2021** 은 실험실 전고체 셀에서 수 MHz 까지 인덕턴스가 무시할 만하다고 한다.
  우리 셀은 7 MHz 부터 수백 kHz 까지 유도성이고, `L1` 없이는 꼭대기에서 11–30 % 어긋났다.
  **우리 측정이 이긴다.**
- **SCHOENLEBER2014** 는 식 번호 (20)·(21) 을 두 번씩 쓴다. μ 는 뒤의 (21) 이다.

## 어떻게 확인했나

- 인용이 남은 기록(코드가 인용하는 것)은 원문을 PDF 텍스트와 글자 단위로 대조했다.
- ISW1990 은 텍스트 층이 망가진 스캔이라, 표 1 과 그림 4b·본문은 쪽을 그림으로
  그려서 봤다. 읽은 에이전트와 그것을 받은 세션이 따로 봤다. 사람은 아직 안 봤다
  (`explored: false`).
- 에이전트가 그림에서 읽은 값은 JSON 의 `conditions` 에 그렇다고 적었다 (예: GUPTA2019
  의 위상, SCHOENLEBER2014 의 IS1a M ≈ 37).

다음에 붙일 분석의 순서는 [[extension-roadmap]] 에 있다.
