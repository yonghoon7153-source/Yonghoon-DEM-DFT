# Codex 짧은 재확인 요청 (초안) — Rint G2 ①′ 구현 재검토 반영 RIMP-01–06 (수정 diff + 탐침 재실행)

> ⛔ **Codex 재확인 (10-15) = 수정 전체 종결 HOLD** — RIMP-01 · 03 · 04 · 05 · 06 범위 한정 닫힘 · RIMP-02 부분 · 새 P2 `RIMPR-01` · P3 `RIMPR-02` · 판정문 `docs/reviews/codex_review_rint_g2_impl_fix_recheck_20261015.md` (증거 `docs/reviews/codex_rint_g2_impl_fix_recheck_evidence_20261015/`).

> **지위** — 초안 · **발송 = 1저자 (아직 보내지 않음)**.  1저자 10-14 비준 (*"권고대로"* — 수정 계획 `docs/reviews/rint_g2_impl_fix_plan_20261014.md` Q1–Q6) 의 수정 묶음.
> **리뷰 핀 = 이 요청서가 든 본 가지 커밋** (번호는 발송 때 1저자가 적는다 · 바로 다음 원장 커밋이 기록한다) — 본 가지 순서: 시험 먼저 `e9d0cd87d` → 수정 `25aecac22` → 문서 · 증거 · 이 요청서 (작업 트리 커밋 번호는 적지 않는다 · SELF-116).
> 직전 판정: Codex 재검토 (10-14 · 검토 핀 `1087a9b2f` · `docs/reviews/codex_review_rint_g2_impl_20261014.md`) = RINTV-01 · 02 범위 한정 닫힘 · 새 P2 다섯 (`RIMP-01`–`05`) · P3 하나 (`RIMP-06`) ·
> **①′ 정량 채택 · 생산 HOLD** — 이 묶음은 그 HOLD 를 풀자는 요청이 **아니다**.  계약 정본 = v2 + v3 + v3.1.  웹앱 화면 없음 (기구 · 시험 전용 · `PROTOCOL_FIELDS` · payload CLI · 생산 기본값 무변경).
> 증거 = `docs/reviews/rint_g2_impl_fix_evidence_20261015/` (시험 먼저 판 · 최종 판 로그 · 명령 · rc · 내용 해시 · README) · 개발 사다리 재측정 = `docs/data/rint_t2_dev_20261013/` (README §3-1 · `t2_dev_v2.json`).

## 0. 무엇을 봐 달라는가

1. RIMP-01–06 각각이 판정문의 최소 해결 (§2–§7) 을 채웠는가 — 아래 §1 (수정 ↔ 시험 · 고치기 전 → 뒤).
2. Codex 탐침을 **고친 트리**에서 다시 돌려 반례가 전부 막히고 정상 (real14 · case15 · D19 양성 · 정상 RRM · 정상 계획) 이 그대로인지 — §3 (탐침별 기대 · 탐침이 고친 판에서 멈추는 자리 둘).
3. 수정이 새로 넓힌 것 · 남긴 것에 대한 질문 — §4.

## 1. RIMP ↔ 수정 ↔ 시험 (고치기 전 → 뒤)

| ID | 비준 (Q) | 수정 (요지 · 파일) | 시험 (새 검사 · 고치기 전 → 뒤) |
|---|---|---|---|
| `RIMP-01` P2 | Q1 (가) | `scripts/rint_t2_dev.py` — 셀 중심과 경계면 중심이 계면의 반대편인 경계 반 셀 = `g_b = h²/(d_c/σ_c + d_f/σ_f + 1e4·r_face)` (d_c + d_f = h/2 · u 선형 보간 · r_face = 그 축 내부 막 면과 같은 법칙 · 변이 포함 · 판정문 §2 의 교차 연결 꼴) · 교차 아님 = 2σh 그대로 · `Mms(offset_um)` (평면 법선 이동) · `with_r_face` · 출력 `n_bc_cross` · `tie_count` · `boundary_rule` · 사다리 배치에 이동 45° · v2 산출 별도 파일 (v1 보존) | `scripts/test_rint_t2_dev.py` D6a · D6b · D7 · D8 — 13 검사 **0/13 → 13/13** (파일 10/20 → 23/23): 정확 이산 층 (θ 0 · β 0 · 계면이 경계 반 셀 안 · 고치기 전 최대 0.397 · 0.352 → 반올림 안) · tie 없는 15° n64 · 30° n16 · 이동 45° n128 (+ 15° n64 L1) = 판정문 §2 대조 값 재현 (상대 ≤ 2.4e−10) · tie · 교차 수 |
| `RIMP-02` P2 | Q2 (가) | `scripts/rint_iface_join.py` — 관문 계산 **전** 입구 검사 e1–e5: 유한 (scaffold · 원자 · 접촉 · 상자) · 반경 > 0 · 상자 hi > lo · 정확 정수 토큰 (step · 머리 수 · id · type — `int(float(…))` 없음) · 직교 상자만 (`xy xz yz` 머리 = `box_tilted` 명시 거부 · 상자 동일 = 머리 · 경계 줄 **전 토큰**) → 하나라도 걸리면 REJECT (관문 생략 · 사유만) · AM–AM 면적 행: 음수 = `area_negative` · 포괄 미인증 = `area_uncertified` → PASS = 전 AM–AM 행 인증 (`area_all_certified`) · AM–AM 밖 행의 음수 면적 = 수만 기록 · 조인 판 `g_geo_g_frame_v2` | `scripts/test_rint_g2_join.py` J5 · J7 · J8 · J9 — 고치기 전 실패 (J5 끝 scaffold nan = `TypeError` 예외) → 뒤 전부 통과 (파일 43/73 → 73/73) |
| `RIMP-03` P2 | Q2 (가) | 같은 파일 — e5 **6 유효숫자 `%g` 생산 포맷만** (토큰 = `'%g' % 값` · 원자 · 접촉 실수 열 + 상자 경계) · 다른 정밀도 · 끝 0 · 혼합 = `numeric_format` · 봉인 helper (`lhs_descriptor_harvest._contact_area_rows` · `AREA_CHECK_SIGFIG = 6`) 무변경 — 지원 형식을 helper 의 고정 6 자리 가정과 같게 묶는다 (S 전달 안 함) | J6 · J8 (16 자리 균일 · +1 ppm · 끝 0 토큰 둘 · 정상 = g6) |
| `RIMP-04` P2 | Q3 (가) | `scripts/rint_rrm_reference.py` `rrm_check` — ① recipe (`iface_rrm.resolve_k` · r 표 · 예외 법칙) 모양 · 값 ② 행 값 (rface 유한 · ≥ 0 · 절단 = tombstone · 막 행 rface 0 = 그 접점 등록 r = 0 일 때만) ③ 기대 접점 · 적격성 재계산 (막 후보를 r 표 **없이** 원장에서 · 빠진 접점 (r 없음 · 기울기 · 미해상) = 계획 거부 사유 수로 덮여야 · 덮이지 않으면 `excluded_without_rejection` · 빠진 접점의 막 행 = 위반) ④ 재현 결합 (기록된 recipe 로 `rrm_plan` 재생성 → 행 · 거부 사유 · 행 수 비트 같음) · `rrm_solve` = 그 검사를 솔브 앞에서 (모든 RRM 실행) | `scripts/test_rint_g2_rrm.py` N9b (복합 변이 셋 + k 만 · 기록 삭제 · 음수 · 양성 r = 0 · 우회 σ 기록) |
| `RIMP-05` P2 | Q4 (가) | `scripts/step3_sigma.py` `iface_require_quantitative(…, vox=)` — 솔버가 자기 vox 를 넘긴다 · 유한 양수 · 계획 vox = 계획 원장 vox = 솔버 vox (float64 같음) 아니면 조립 **전** 거부 · `vox=None` (직접 호출) = 검사 안 함 · iface=None 경로 무변경 | `scripts/test_rint_g2_am_iface.py` T0-7 (음성: 같은 sid · 같은 계획 · h 0.2 ↔ 0.4 = CG 호출 0 거부 · 양성: 정상 재생성 계획 σ 0.0021331551689598217 · A · G 4 배 · 관문 인자 경계) — 파일 129/131 → 132/132 |
| `RIMP-06` P3 | Q3 (가) | 같은 RRM 모듈 `rrm_plan` — 표준 `iface_contact_ledger` = 실제 RRM 행에서 다시 셈 (`summary_source = rrm_rows` · film_faces.active · cut_faces · `film_G_S_total = {rrm}` · `rface_ohm_cm2 = {rrm}` · `n_realized` · `A_film_sum_um2` · `a_lt_h`) · 원장 기하 키만 CNC 요약에서 그대로 · CNC 값 = `iface_cnc_comparison` (기록) · `cnc_comparison` (계획: rface_c · rface_remove · rface_renorm · carbon_cover · realized) · `iface_carbon_cover` = None (+ 상태 문구) · 계획 `realized` = RRM 기준 접점 | RRM-7 (film 67 · cut 85 · 순수 막 G = 행 합 = 접점 기록 · CNC = 별도 이름공간 · 반쪽 탄소 37 · 42 · G 2.7535056597827278e−6 ↔ CNC 2.612935414333538e−6 / 5.027420037705035e−6 · 풀이 기록) — RRM 파일 43/54 → 54/54 |

- 기존 시험 229 (am_iface 126 · rrm 39 · join 40 · t4_census 8 · t43_order 6 · t2_dev 10) + `step3_sigma.py --selftest` · `--selftest-rint` 그대로 통과 · `rint_t41_census.py --selftest` (조인 모듈 소비자) 통과 · 새 검사 67 → 수정 뒤 296/296 (증거 §2).
- **iface 끔 = 비트 같음** — 수치 OFF 16 사례 (판정문 §1-2 와 같은 격자) 를 수정 뒤 ↔ 고치기 전 (`44a034534` 의 `step3_sigma.py` = 검토 핀 blob) · 수정 뒤 ↔ ①′ 전 (`1d9af09d0` = 묶음 `source_prior`) 로 다시: rasterize · 전체 반환 dict · 배열 바이트 **16/16 · 16/16 같음** (증거 §4 · σ 는 Windows 표와 끝자리 차 ≤ 6.9e−15 상대 = 플랫폼).
- 봉인 32 (`run_network_194_parallel.CODE_FILES` — `lhs_descriptor_harvest.py` · `lens_geometry.py` 포함) · `seal_s3_prerun.NUMERIC_MODULES` 6 = 무변경 (수정 넷은 둘 다 밖).

## 2. 숫자 (개발 · 보고 — 합격선 아님)

### 2-1. T2-1′ 개발 사다리 재측정 (`docs/data/rint_t2_dev_20261013/README.md` §3-1 · **개발 표지** — D11 · D12-V 근거 아님)

| θ · 이동 | 법칙 | L2 오차 (n 8 → 128) | 최대 (n 128) | 경계 교차 (n 8 → 128) | tie |
|---|---|---|---|---|---|
| 0° | L1 = 축별 | 1.9e−16 … 2.0e−14 (반올림) | 5.4e−14 | 0 | 0 |
| 15° | 축별 | 8.9e−3 · 3.8e−3 · 1.2e−3 · 4.5e−4 · 1.6e−4 | 3.4e−3 | 0 · 0 · 0 · 2 · 0 | 0 |
| 15° | L1 | 9.8e−3 · 5.1e−3 · 2.9e−3 · 1.4e−3 · 6.7e−4 | 1.1e−2 | 0 · 0 · 0 · 2 · 0 | 0 |
| 30° | 축별 | 1.2e−2 · 3.1e−3 · 1.2e−3 · 3.8e−4 · 1.3e−4 | 2.3e−3 | 0 · 2 · 0 · 0 · 0 | 0 |
| 30° | L1 | 9.4e−3 · 4.5e−3 · 1.7e−3 · 9.6e−4 · 4.9e−4 | 5.0e−3 | 0 · 2 · 0 · 0 · 0 | 0 |
| 45° | L1 = 축별 | 2.5e−2 · 8.1e−3 · 3.4e−3 · 1.7e−3 · 8.5e−4 | 7.1e−3 | 2 | n (플랫폼 의존 배정) |
| 45° · 0.001 µm | L1 = 축별 | 2.1e−2 · 1.0e−2 · 4.8e−3 · 2.3e−3 · 9.8e−4 | 4.0e−3 | 2 | 0 |

- v1 의 뾰족점 (15° n64 L2 1.3e−2 · 최대 0.538 / 30° n16 4.1e−2 · 0.504) = 그 격자에서만 경계 반 셀 교차 2 — 사라짐 · 45° 0.44 고원 사라짐 (n128 0.443 → 7.1e−3 · 이동 45° 4.0e−3).
- v1 해석 두 줄 (*"계단 기하의 교대"* · *"45° 0.44 = tie 점 판정 한계"*) **철회** (README ★) — tie · 원점 규약은 D12-V 몫으로 따로 남는다.
- 관측 L2 차수 (n 64 → 128) 축별 1.49 · 1.54 · 1.01 · 1.20 / L1 1.07 · 0.98 · 변이 셋 = 정답 L2 의 136–1,450 배 — 개발 관찰 · 수렴 판정 아님.

### 2-2. 정상 자료 형식 (RIMP-03 범위 근거)

real14 · case15 의 원자 · 접촉 덤프 실수 토큰 (x · y · z · radius / pos · c_cpl[22] · c_cpl[23] · c_cpl[9]) 고유 92,752 · 295,718 · 185,269 · 511,051 개 **전부 `'%g' % 값` 과 같은 문자열** · id · type 열 전부 정수 문자열 (수정 전 별도 검사) — 6 자리 `%g` 전용 계약이 정상 두 침대를 바꾸지 않는다 (J1 · J2 · J9 PASS 유지 · real14 AM–AM 660 · case15 119 행 전부 인증 · case15 의 음수 면적 2 행 = AM_P–SE = 조인 면적 인증 밖 · 기록만).

## 3. Codex 탐침 재실행 요청 (고친 트리 — 묶음의 source/scripts 대신 리뷰 핀의 `scripts/` · 탐침 = `docs/reviews/codex_rint_g2_impl_review_evidence_20261014/probes/`)

| 탐침 | 기대 (고친 트리) |
|---|---|
| `docs/reviews/codex_rint_g2_impl_review_evidence_20261014/probes/rrm_probe.py` | `rrm()`: `cut_rows_removed_k_changed` · `_rtable_removed` · `nan_rface` → `rrm_check` 위반 있음 · `rrm_solve` = `ValueError` (탐침이 잡아 문자열로 적는다) · `production_gate` (일반 관문) = accept 그대로 (설계 · 공개 범위) · `stored_summary` = film 67 · cut 85 · `film_G_S_total = {rrm}` · `geometry()` carbon_half: 표준 요약 = RRM G 2.7535056597827278e−6 (CNC = `iface_cnc_comparison`).  `mms()`: 15° n64 · 30° n16 최대 오차 = 이전 대조 값 (0.006475555385 · 0.01633704071).  ⚠ `boundary_control()` 은 고친 harness 위에 같은 보정을 **한 번 더** 얹는다 (조립된 대각에서 2σh 를 빼고 새 g 를 더함) → 고친 트리에서는 `before` 가 이전 `after` 값과 같아야 하고 `after` 는 뜻이 없다 |
| `docs/reviews/codex_rint_g2_impl_review_evidence_20261014/probes/join_adversarial.py` | 변이 넷 (음수 · NaN 셋) · 다른 tilt · step 2060000.9 = 전부 REJECT (`area_negative` · `nonfinite_value` · `box_tilted` · `int_token`) · baseline PASS |
| `docs/reviews/codex_rint_g2_impl_review_evidence_20261014/probes/join_synthetic.py` | ⚠ 합성 덤프가 `%.15e` (16 유효숫자) 라 **기준 (baseline) 부터** `numeric_format` REJECT → 탐침이 `base['g_geo']['delta_bound_um']` 에서 `KeyError` 로 멈춘다 (입구 실패 기록에는 관문 요약이 없다 — `g_geo = {skipped, n_scaffold}`).  같은 반례를 `%g` 로 다시 만든 우리 J7 · J8 을 보거나 탐침의 `fmt` 를 `'%g' % x` 로 바꿔 돌려 주길 — 그때 기대 = 음수 · NaN 셋 · tilt · 근동심 100 sim² 전부 REJECT · 계획 `join_gate_failed` · 정량 관문 거부 |
| `docs/reviews/codex_rint_g2_impl_review_evidence_20261014/probes/join_global_precision.py` | 원자 · 접촉 끝 0 토큰 둘 = `numeric_format` REJECT (옛 `pos_mismatch` · `delta_pos_mismatch` 대신 입구에서) |
| `docs/reviews/codex_rint_g2_impl_review_evidence_20261014/probes/owner_vox_mismatch.py` | `mismatched` 행 (h 0.2 계획 · h 0.4 솔버) = `solve_sigma_z` 가 `ValueError` (탐침이 예외를 잡지 않아 거기서 멈춘다) · `matching` · `rebuilt_scaled` = 그대로 (σ 0.0021331551689598217 · A · G 4 배) |
| `docs/reviews/codex_rint_g2_impl_review_evidence_20261014/probes/off_compatibility.py` (`source_prior` ↔ 고친 `step3_sigma.py`) | 16/16 같음 (우리 재현: 증거 §4) |
| `docs/reviews/codex_rint_g2_impl_review_evidence_20261014/probes/owner_independent.py` | 변화 없음 (소유권 규칙 · T4 무변경) |

## 4. 질문

1. **(RIMP-01 경계 규약)** 교차 반 셀 = (u 선형 보간 거리 분할 + 같은 축 법칙의 r_face) 로 충분한가?  꼭짓점 셀 (경계면 둘이 교차) 은 면마다 독립 처리했다 · 경계면 중심이 다른 상이면 Dirichlet 값 = 그 상의 정답 φ (면 중심) — 이 조합에 남은 구멍이 있는가?
2. **(RIMP-01 tie)** 45° 원점 대칭 (tie n 셀) 은 배정이 플랫폼 반올림에 걸려 회귀 (D7) 에서 뺐다 (tie 수만 D8 에 기록) — 이 범위가 맞는가, 아니면 harness 에 tie 규칙을 지금 등록해야 하는가 (D12-V 전)?
3. **(RIMP-02 입구 실패 기록)** 입구 실패 = 관문 계산을 생략한 REJECT (사유만 · `g_geo` · `g_frame` = skipped) 로 둔 것 · 미인증 면적 = 별도 상태가 아니라 거부 사유 (`area_uncertified` · REJECT) 로 둔 것이 판정문 §3 *"거부 또는 미인증 상태 (PASS 와 분리)"* 를 채우는가?
4. **(RIMP-02 범위)** 조인이 인증하는 면적 = AM–AM 행뿐이라 AM–AM 밖 행의 음수 면적은 수만 기록 (case15 AM_P–SE 2 행 · PASS 유지) — 동의하는가?
5. **(RIMP-03 형식 증명)** "토큰 = `'%g' % float(토큰)`" 를 6 자리 균일 생산 포맷의 계약으로 쓴 것 (상자 경계 포함 · 정수 열 = 정수 문자열) 이 판정문 §4 의 *"균일 포맷 보증 또는 혼합 거부"* 를 채우는가?
6. **(RIMP-04 결합)** ④ 재현 결합은 `rrm_plan` 자체를 다시 부른다 (독립 아님) — 독립 층은 ③ (원장 · 기록 k · r 표에서 기대 접점 · 적격성 · owner 면 전수) 이다.  이 두 층 구성이 *"메타데이터로 검사 집합을 비울 수 없게"* 를 채우는가?
7. **(RIMP-04 · 05 범위 밖 하나)** 일반 생산 관문 (`iface_require_quantitative`) 에도 rface 유한 · ≥ 0 검사를 넣어야 하는가 (지금은 RRM wrapper 만 · 비준 Q3 범위)?
8. **(RIMP-05)** vox 결합 = 허용폭 없는 float64 같음 · `vox=None` (직접 호출) = 검사 안 함 — 이 계약이 맞는가?
9. **(RIMP-06 키 변경)** RRM 계획의 표준 요약에서 `film_G_S_total` · `rface_ohm_cm2` 의 키가 CNC 판 이름 (`remove_area` · `renormalize`) 에서 `rrm` 으로 바뀌고 `iface_carbon_cover` = None 이 된다 — 일반 소비자 호환 · 표지로 충분한가?

기존 HOLD (D11 · D16-dev · D17 · D19 · D21 저자 결정 · D12-V 봉인 · T2/T3 독립 검증 · 실행 영수증) 는 이번에 정하지 않는다 — **이번 수정 뒤 한 번에 보고** (수정 계획 Q6).
