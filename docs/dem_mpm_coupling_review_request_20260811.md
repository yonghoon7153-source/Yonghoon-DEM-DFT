# DEM–MPM 연계 준비상태 정리 + Codex 리뷰 요청 (2026-08-11)

> ⛔ **이 문서의 §3·§4 초안은 리뷰에서 기각·수정되었다.**  회답과 확정 설계는
> `docs/codex_dem_mpm_response_20260811.md` 를 볼 것.  요점:
> §3 의 "jam 미발화·축퇴는 제외" 는 **post-treatment selection** 이라 **FAIL** 로 바뀌었고
> (판정기 재작성, selftest 10/10), §4 는 "DEM-독립 예측" 이 아니라
> **conditional closure test** 로 명칭·핀 목록이 고쳐졌다.  §2 의 f_AM 브래킷 주장도
> 철회됐다 (phase = AM-AM + 0.5·AM-SE 항등식).  아래는 **리뷰에 제출한 원안** 이다.

대상 독자: Codex (적대 리뷰).  요청: §6 의 질문 6개에 대한 검증·반박.
검증 좌표: 브랜치 `claude/stoic-knuth-NObVQ`, 이 문서 포함 커밋까지의 상태.
핵심 파일: `scripts/mpm3d_compaction.py` · `scripts/dem_am_load_fraction.py` ·
`scripts/heckel_analysis.py` · `scripts/summarize_jam_sweep.py` ·
`docs/mpm_wallP_conditional_troubleshooting.md` ·
`docs/data/heckel_real14_composite_multiP.csv` ·
`docs/data/heckel_sweep_scaffolds/P{100,200,300,600}_{am,se}_scaffold.csv`.

---

## §1 벽/서보 문제 연대기 — 무엇이 걱정이었고 무엇이 남았나

사용자 기억의 원형: "벽이 너무 빨리 내려와 압력이 확 튀고, 그것 때문에 servo 가
바로 걸린다."  실제로는 **세 개의 독립된 문제**였고, 앞 둘은 닫혔으며 셋째가
지금의 검증 대상이다.

| # | 문제 | 기전 | 대응 | 상태 |
|---|---|---|---|---|
| 1 | 재하율 | `vmax = 0.008·(WALL0−FLOOR)` 가 속도를 베드 높이에 비례시킴 → 두꺼운 베드 V/c_S 0.75 | `--platen-mach`(planner 기본 0.03, 항상 명시 출력) + 기하규칙 사용 시 경고 | **닫힘** (73626353) |
| 2 | 첫-접촉 스파이크 → servo 조기발화 → 과소압축(40%) | 큰 AM 이 플래튼에 처음 닿을 때 wallP 순간 스파이크 | arm-after-compaction 가드 (por ≤ por0−Δ 전까지 disarm) | **닫힘** (2026-06-16) |
| 3 | frozen-AM 과압축 (방향이 #2 와 **반대**) | 얼린 AM 은 wallP 기여 정확히 0 → SE servo 가 전체 목표압을 SE 에게 요구 | hold protocol + `--am-jam(-quantile)` + `--am-load-frac`(실측 f_AM) | **재료 완비, 검증 대기** |

#1 의 크기 실측: 같은 베드에서 재하율 교정 효과 σ +4.8 % (작음 — 곡선 절대값 사용
가능); 교정하니 킷 간 배수가 2.96→3.4× 계열로 **늘어** 교정이 결론을 강화
(`docs/se_curve_transfer_verdict_20260806.md` ③④).

## §2 닫힌 것 — 증거 좌표

- **재하율**: `plan_se_curve_targets.py:191` 기본 0.03 · 러너가 `--platen-mach` 항상
  포함 · d_h 색인 인용은 재하율-청정(0.03) 런만 (`fit_dh_collapse.py --mach` 게이트).
- **스파이크 가드**: `mpm3d_compaction.py` servo arm 가드.  ⚠ scaffold(압축 베드)에선
  가드 OFF 가 옳다는 것도 확인돼 있음 (dense 베드 과압축 방지, 2026-06-16 기록).
- **f_AM 실측 4점** (2026-08-07 + 08-11 P200):

  | P (MPa) | contact AM-AM (하한) | per-atom AM-phase (상한) | Hertz 추정 | 추정/실측 |
  |---|---|---|---|---|
  | 100 | 0.517 | 0.7258 | 0.676 | 1.36× |
  | 200 | 0.598 | 0.7676 | 0.789 | 1.32× |
  | 300 | 0.675 | 0.7938 | 0.870 | 1.30× |
  | 600 | 0.620 | 0.7625 | 0.841 | 1.36× |

  Hertz 추정기는 4점 모두 1.3× 과대·튜닝 불가(이력 의존 구성식 vs 정적 스냅샷) →
  **사용 금지 확정**.  Σf·l = atom-virial 로 열 파싱 무결 교차확인.  AM-phase 4점은
  2026-08-11 백필 (같은-덤프 짝 규약 — ⚠ troubleshooting 문서의 0.809 는 **원본**
  real_14 덤프(atom_2060000) 값이고 스윕 P300 덤프는 0.7938; 차 0.015 = 재실행 산포.
  두 열이 같은 모양(300 까지 상승, 600 꺾임)으로 움직이는 것은 브래킷의 자기일관성.)
- **Heckel n=4**: P_y 133 MPa, 1σ [116, 156], R² 0.960.  사전등록 규약 준수 —
  실측점이 볼록 가설 쪽(|Δ| 0.057 vs 직선 0.252)이지만 **곡률 주장 안 함** (0.252 도
  잔차 sd 0.404~0.533 안).  원장: `heckel_real14_composite_multiP.csv` 주석.

## §3 열린 것 ① — jam-quantile 재시험 (사전등록문 초안, 리뷰 대상)

1차 시험(2026-08-07)의 판정은 "어느 q 도 케이스-독립 아님"이었으나 **유효점이
P100+P300 둘뿐**이었다 (P100-q90 jam 미발화 = 시험 대상 아님 — 단 이 제외가
사전등록되지 않았던 것이 교훈; P600 = MPM porosity 0.00 %·DEM ε_union 0.69 % 축퇴).
P200 (ε_union 19.8 %, 축퇴 아님) 이 3점째 후보다.

**사전등록문 초안 (GPU 돌리기 전에 Codex 리뷰를 받는 것이 목적):**

1. 런: q ∈ {90, 95, 100} × P ∈ {100, **200**, 300}.  P600 은 **사전 제외** (축퇴 —
   이번엔 미리 박는다).
2. 유효성 게이트 (사전등록): `stop_mode == am_jam` 인 런만 판정에 넣는다.
   추가 축퇴 게이트: MPM porosity ≥ 2 % **그리고** DEM ε_union ≥ 2 %.
3. 판정 기준: 두께 |Δ| ≤ 1 % (기존 `summarize_jam_sweep.PASS_PCT` 유지) 가 **모든
   유효 압력**에서 성립해야 그 q 를 인정.  유효 압력 < 3 이면 **미결** (n=2 로
   케이스-독립 주장 금지 — 1차의 교훈).
4. 지표는 **두께 고정**.  porosity 는 이번에도 관찰만 (1차의 사후관찰 q=95 porosity
   고름은 가설로만 — 지표를 결과 보고 바꾸지 않는다).
5. 통과해도 주장은 "**압력-독립**"까지만.  "케이스-독립"은 **다른 베드 축**(조성이
   다른 베드)이 필요 — 후보는 kit_ps 5침대 (다만 ⚠ 두께 100 µm 급이라 SE 미해상이
   stop_mode 를 am_jam 쪽으로 편향시킬 수 있음: jam 평면 자체는 AM 위치의 기하량이라
   격자 무관이지만, **게이트 통과율**이 격자에 의존할 수 있다는 한계를 병기).

## §4 열린 것 ② — corner wallP-conditional 검증 (설계, 리뷰 대상)

`--am-load-frac` 의 원래 목적 = regime map 의 실패 corner (mono-large 10:0 ·
SE-poor · thin; 예 `input_1mAh_100_15`, MPM 0 % vs DEM 32.8 %).  6월부터
"corner 런 대기".  이제 f_AM 이 실측이므로 **자유 파라미터 0 의 예측 시험**이 된다:

1. 케이스 선정: regime map 실패 corner 에서 2~3개.  선정 단계에서 atoms.csv 에
   `sigma_zz` 열 존재 확인 (per-atom f_AM 실측 경로; 없으면 그 케이스 제외 —
   Hertz 추정 대체 금지).
2. f_AM: 그 케이스 **자기 덤프**에서 실측.  브래킷 규약 — contact 데이터가 있으면
   [AM-AM, AM-phase] 양끝 다 걸고, 없으면 AM-phase 단독 + "상한 규약" 라벨.
3. 판정: 보정 BC 에서 MPM porosity 가 DEM↔MPM 신뢰 밴드 |gap| ≤ 4 %p (regime map
   의 기존 기준 재사용) 에 드는가.  f_AM 은 측정값이므로 이것은 캘리브레이션이
   아니라 예측이다.
4. ⚠ **`--floor-porosity` 는 검증 런에서 끈다** (flat `--am-load-frac` 만).
   floor 게이트는 "= the case DEM porosity" 를 넣는 설계라, 검증에 쓰면 DEM 답
   주입 = 순환.  production 편의 게이트와 검증 런 규약을 분리한다.

## §5 이번 정리에서 발견·수정한 것

- `--am-load-frac` help 가 **폐기된 v0 von-Mises 공식을 예시**로 들고 있었다
  (v1 Love-Weber 채택·Hertz 금지와 어긋남) → 실측 브래킷 규약으로 교체 (이 커밋).
  계산 경로 무변경 (help 문자열만).
- P200 처리 중 도구 버그 2건 (커밋 136cd010): `vol_and_lens` 가 `rad_by_id` 를
  안 넘겨 교차검증이 등반지름 렌즈(이 기하에서 39 % 오차)로 돌던 것 / manifest
  contacts 문자열이 글자 단위로 순회되던 것.  **기존 3압력 원장의 ε/D 는 기하 경로
  값이라 무영향** — 교차검증 열만 버그를 지나갔다 (주장 검증 환영, §6-Q5).
- `dem_am_load_fraction.py` 의 scipy 를 지연 import 로 — 모듈 최상단 SystemExit 이
  scipy 없는 환경에서 **실측 경로(쓰는 값)까지** 막고 있었다.

## §6 Codex 리뷰 요청 — 질문 6개

- **Q1 (jam 사전등록문, §3)**: 게이트·문턱·표본수·해석 규약에 구멍이 있는가?
  특히 "유효 압력 < 3 = 미결" 과 "porosity 지표 전환 금지" 가 충분히 단단한가?
  1차 시험에서 사전등록 안 된 제외(P100-q90)를 사후 적용한 것과 같은 종류의
  누수가 이 초안에 남아 있는가?
- **Q2 (f_AM 규약)**: servo 보정에 물리적으로 옳은 규약은 어느 쪽인가?
  `dem_am_load_fraction.py` docstring 은 "frozen AM 이 흡수하는 AM-SE 하중은 SE
  wallP 에 도달하지 않으므로 **per-atom AM-phase 가 정확히 스프링이 필요로 하는
  것**"이라 주장하고, 같은 파일이 "AM-AM-only ≤ 참 ≤ AM-phase" 브래킷도 명시한다.
  이 두 서술은 긴장 관계다 — AM-phase 가 "정확"하면 브래킷 상한이 아니라 점추정
  이어야 한다.  per-atom virial 이 AM-SE 접촉력을 반씩 나누는 규약임을 감안할 때
  어느 서술이 맞는지 판정해 달라.  (troubleshooting 문서의 "SE servo 목표
  P·(1−f_AM)" 표는 contact AM-AM 으로 계산돼 있어 셋째 규약처럼 읽힌다.)
- **Q3 (corner 검증 비순환성, §4)**: `--floor-porosity` 를 끄면 corner 시험은
  순환 없이 성립하는가?  AM 스캐폴드 자체가 DEM 산물이라는 점이 "porosity 예측"
  주장을 얼마나 약화시키는가 (jam 시험과 같은 방식으로 정량 서술 가능한가)?
- **Q4 (Heckel n=4 보고)**: `heckel_real14_composite_multiP.csv` 주석과
  `mpm_wallP_conditional_troubleshooting.md` §P200 이 사전등록 규약(곡률 비주장)을
  지켰는지, "볼록 쪽 착지 병기" 가 규약 위반의 우회 서술은 아닌지.
- **Q5 (도구 수정 소급성)**: rad_by_id 수정이 "기존 3압력 원장 무영향" 이라는 주장
  검증 (ε/D = `lens_from_geometry` 경로, 교차검증 열 = `lens_from_contacts` 경로).
  selftest 20/20 중 신규 3개(TypeError·다분산 교차·등반지름 감지선)의 커버리지 평가.
- **Q6 (문서 정합)**: v0 von-Mises 잔재가 다른 곳에 더 있는가?  (이번에 help 1곳
  수정; grep 후보: `von.?Mises.*f_AM`, `phi_AM.*sVM`.)

## §7 리뷰 뒤 실행 순서 (GPU 복구 시)

1. ps_7_3 192@0.03 φ 3점 (가장 쌈, 192 5침대 정식 인용 완성)
2. §3 jam 재시험 (사전등록문이 Q1 통과한 판으로)
3. §4 corner 런 (Q2 의 규약 판정 반영, 브래킷 양끝)

(P100/P600 AM-phase 백필은 GPU 불요라 이미 완료 — §2 표.)
