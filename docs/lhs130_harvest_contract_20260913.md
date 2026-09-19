# LHS 130 수확 계약 — 판정문 §7 을 도구에 고정한 기록 (2026-09-13)

> 판정 = `docs/reviews/codex_verdict_lhs_descriptors_20260913.md` (**HOLD**) · 원장 `DESC-01~09`.
> 도구 = `scripts/lhs_descriptor_harvest.py` (`--selftest`, CI·`check_all` 양 레인 배선).
> ⚠ **이 문서는 계약이지 결과가 아니다.**  130 배치의 실제 수치는 아직 하나도 없다.

## 왜 이 순서인가 — 선례가 있다

`lhs_perc_extract.py` 는 *"추출기와 경계 fixture 를 **결과 전에** 커밋해야 이 규약이 실재한다"*
(Codex R11 B1) 로 만들어졌다.  같은 이유로 이 수확기도 **130 dump 를 하나도 읽기 전에** 짰다.
런이 끝난 뒤 수확기를 짜면 규약이 데이터를 보고 정해지고, 그때는 계약이 아니다.

## 계약 6개 ↔ 구현 ↔ 그것을 지키는 검사

| § | 계약 | 구현 | 검사 (`--selftest`) |
|---|---|---|---|
| ① | 일곱 별칭 → 원필드/계산식/단위/통계량 정확 매핑.  **전체 Hertz 는 실측 입자수 가중** | docstring §계약① 표 · `coverage_hertz()` | ④ 판정문 반례 재현 — P 1개 10 % · S 3개 90 % → **70 %** (상평균평균 50 · 총면적비 30 · 질량가중 18 이 **아니다**) |
| ② | φ 는 τ·전도도 성공과 **무관하게** 기하에서 | `volumes_and_phi()` — 호출 경로에 τ 가 없다 | ① `DESC-01` 반례: τ 가 `NOT_PERCOLATING` 인데 `phi_se`·`phi_am` 이 나온다 + closure 항등식 |
| ③ | τ 의 관통성·경계·표본·절단·실패 사유 명시.  불량 기하를 유효 0 으로 안 채움 | `tortuosity_se()` — **fallback source 승격 없음** · 쌍은 **같은 성분 안에서만** · 상태코드 | ② `DESC-02①` 비관통 → `None`/`NOT_PERCOLATING` · ③ `DESC-02②` 무경로 쌍이 예산을 안 먹는다 |
| ④ | 표준 scale 에서 Hertz 보존 · Physics/rough/Laplace/Stage E **대체 금지** | 면적/면적 비 · `plastic_coverage` 를 **부르지 않는다** | ⑤ scale ×1000 불변 · ⑪ `contact_area` 열 없으면 거부 · ⑬ 정적으로 `plastic_coverage` 부재 |
| ⑤ | frozen130 ID ↔ 최종 pressure/timestep · raw hash · phase map · 상 개수 · target 별 상태 | `harvest()` — TIMESTEP 일치 강제 · sha256 · `--n-types` 필수 · `plate_z` **추정 금지** | ⑧ `DESC-06` 프레임 혼합 거부 · ⑨ 플래튼 높이 추정 거부 · ⑩ 선언 밖 type·경계 플래그 거부 |
| ⑥ | **130 단독 코퍼스 먼저**.  291 병합은 별도 판단 | 자기 JSON 만 낸다 | ⑬ 정적으로 `design_performance_corpus`·`full_metrics` 부재 |

⑫ 는 **변이 대조**다 — TIMESTEP 가드를 퇴행시키면 ⑧ 이 **실제로 뚫려야** 통과한다.
(`PA12-09`: 어댑터의 음성대조 ⑨ 는 `SystemExit` 이면 아무거나 성공으로 세어 **장식**이었다.
그래서 여기 `neg()` 는 **오류 종류**를 요구한다.)

## 이 도구가 legacy 와 **다른** 자리 — 같은 컬럼에 섞지 말 것 (`DESC-04`)

| 축 | legacy (`dem_analysis_core`) | 이 수확기 |
|---|---|---|
| τ source | 바닥판 없으면 **위판 성분의 최저 z 를 승격** (`:502-509`) | 승격 **없음** — 없으면 `NOT_PERCOLATING` |
| τ 쌍 예산 | `src × top` 전수 shuffle 200 (무경로 쌍 포함, `:517`) | **같은 성분 안에서만** 200 |
| τ 슬래브 | own-radius×2 → 벽 15/85 % → **관측 SE z 범위** 15/85 % 3중 fallback (`:404`) | 고체(AM∪SE) z 범위 양 끝, 두께 `r_SE,max`.  fallback 없음 |
| τ 통계량 | `mean`·`median`·`recommended` 가 한 이름 아래 | 이름으로 가름 — 별칭 `tortuosity_dijkstra_SE` = **`tau_mean`**(절단본), `tau_mean_untruncated`·`n_truncated` 동시 보고 |
| φ_AM | `1 − φ_SE − ε/100` **잔차** (`analyze_contacts.py:434`) | `Σ_{i∈AM} V_i / V_B` **직접 합** |
| 플래튼 높이 | mesh 없으면 최고 입자 **중심** 추정 (`:110`) | **추정 금지** — `--mesh` 또는 `--plate-z` 택일 |

⇒ 두 계열의 τ·φ 를 한 열에 섞으면 **보정 방식이 섞인 채로** 학습된다.
`tau_convention` 필드가 매 행에 박혀 나온다.

## 학습에서의 취급 — 일곱 열 ≠ 일곱 독립 회귀 (`DESC-07`)

- `ε_sphere = 100(1 − φ_SE − φ_AM)` — 291 DEM 열에서 최대 절댓값 **2.22e−16** 으로 재현된다.
  ⇒ 세 독립 응답으로 **세지 않는다**.  (`closure_residual` 이 매 행에 나온다.)
- `C_total = (N_P C_P + N_S C_S)/(N_P+N_S)` — **실측 입자수**까지 주어지면 전체 피복률에
  추가 정보가 없다.  ⚠ 행마다 가중치가 달라 *"세 coverage 열의 rank 가 항상 2"* 라는 뜻은 **아니다**.
- ⚠ 예측 시점에 실현 `N_P`/`N_S` 를 모르는 모델이면 **관측 N 을 몰래 넣어** total 을 예측했다고
  하면 안 된다.  설계 추정 N 과 dump 실측 N 도 구분한다.
- 권고 기본 출력 = `phi_SE`·`phi_AM`, **존재상별** Hertz `C_P`·`C_S`, **검증된 관통** graph 의 τ.
  전체 coverage 와 ε 는 파생/QC.

## 결측을 다섯 종류로 가른다 (`DESC-05`)

`OK` · `N_A_PHASE_ABSENT`(없는 상 — 존재하는데 무접촉인 **0** 과 다르다) · `NOT_PERCOLATING` ·
**`ELECTRODE_BAND_EMPTY`** · `NO_VALID_SAMPLED_PAIR` · `FREE_SURFACE_INVALID`(분모 붕괴 —
무접촉 0 과 다르다) · `INPUT_MISSING`.
⛔ **한 타깃이 미정의라고 다른 타깃이 있는 행을 통째로 버리지 않는다.**

★ **여섯 번째가 2026-09-19 에 늘었다** (`LHS-08`).  `NOT_PERCOLATING` 하나가 **두 원인**을
접고 있었다 — ⓐ 전극 밴드에 SE 가 0 명이라 볼 성분이 애초에 없던 경우와 ⓑ 밴드는 찼는데
어떤 성분도 못 잇던 경우.  **처방이 정반대**다(ⓐ = 규약, ⓑ = 물리)인데 산출물이 같아
실물 130 중 **116** 이 어느 쪽인지 판별 불가였다.  ⇒ ⓐ 는 `ELECTRODE_BAND_EMPTY`,
그리고 두 경우 모두 `tau_detail.band_detail` 에 **세는 수**를 남긴다.
⚠ 이것은 `DESC-05` 의 *"결측을 종류로 가른다"* 가 **한 겹 더 필요했다**는 뜻이다 —
종류를 다섯으로 가르고도 그 중 하나가 두 사유를 담고 있으면 같은 false-green 이 난다.

## 아직 안 한 것 (정직하게)

- ⬜ **130 dump 를 하나도 읽지 않았다.**  이 컨테이너에 배치 데이터가 없다.
- ⬜ `--batch` 모드 (설계 CSV join · ID↔최종 pressure 대조) 미구현.  단건 경로만 있다.
- ⬜ 291 코퍼스의 `d_am` · `use_porosity_pct` 정리 (`DESC-08`) — **별개 사안**이다.
- ⚠ **미실행 8개는 무작위 결측이 아니다** (`DESC-09`): 전부 `mono_AM_S` 이고
  `mono_AM_S × d_SE = 2 µm` 다섯 점(105·108·109·110·111)이 **전부** 그 목록에 있어 그 수준의
  관측이 **0 개**다.  공변량·가중치로 못 살린다 ⇒ 교정된 완료분으로 **탐색 학습은 가능**하나
  130-domain 최종 성능·순위로 보고하지 않는다.
- ⚠ `44/130` 은 `phi_se_est` 기반 **사전 추정 BELOW flag (33.846 %)** 이지
  *"44 % 가 실측 σ_ion = 0"* 이 아니다 — 일곱 측정 열은 **130 행 전부 빈칸**이다.
- ⚠ `finite_size_flag` 는 진단 라벨로 타당하지만 **설계 변수의 결정론적 함수**라
  "공변량으로 넣으면 유한크기 효과가 제거된다" 는 보장이 아니다 ⇒ **고정 finite-box 규약 안의
  예측**으로 해석한다.
