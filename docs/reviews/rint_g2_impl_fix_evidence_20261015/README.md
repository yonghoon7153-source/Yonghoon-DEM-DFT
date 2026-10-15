# Rint G2 ①′ 구현 재검토 반영 (RIMP-01–06) — 우리 트리 재현 · 시험 로그 (2026-10-15)

> **판** — 로그를 낸 판 = **작업 트리 판** — 본 가지 대응 (메인 세션 대조 10-15): 시험 먼저 = `e9d0cd87d` · 최종 = 수정 `25aecac22` (아래 두 HASHES 의 git blob = 그 커밋의 blob) · 내용 해시 = `tests_first/HASHES.txt` (고치기 전) · `final/HASHES.txt` (수정 뒤).
> 시험 4 파일은 두 판에서 같은 blob 이다 (시험 먼저 → 수정 · 시험 무변경).  수정 대상 4 파일의 고치기 전 판 = 본 가지 `44a034534` = Codex 검토 핀 `1087a9b2f` 와 같은 blob.
> 근거 = Codex 재검토 `docs/reviews/codex_review_rint_g2_impl_20261014.md` · 수정 계획 `docs/reviews/rint_g2_impl_fix_plan_20261014.md` (1저자 10-14 Q1–Q6 권고대로) ·
> 재확인 요청서 `docs/reviews/codex_rint_g2_impl_fix_recheck_request_20261015.md`.
> ⚠ Codex 묶음 (`docs/reviews/codex_rint_g2_impl_review_evidence_20261014/`) 의 탐침 · 스크립트는 **실행하지 않았다** (읽기만) — 반례 값을 우리 시험으로 다시 만들었다.
> ⚠ 이 폴더의 PASS 는 기구 · 관문 · 개발 기준해의 증거다 — ①′ 정량 채택 · 생산 · D11 · D12-V · T2/T3 검증이 아니다 (HOLD 그대로) · 웹앱 화면 없음.

## 1. 폴더

| 파일 | 무엇 |
|---|---|
| `tests_first/*.log` · `tests_first/HASHES.txt` | 시험만 넣고 **고치기 전** 실행한 로그 넷 (t2_dev · join · rrm · am_iface) + 그 판 내용 해시 |
| `final/*.log` · `final/*.json` · `final/HASHES.txt` | 수정 뒤 전 시험 · 자체시험 · iface 끔 16 사례 (아래 §2 · §4) + 내용 해시 |
| `off_compat_16.py` | iface 끔 비트 같음 재확인 도구 — 증거 생성 전용 (시험 레인 밖 · `--selftest` 없음) |
| 개발 사다리 재측정 | `docs/data/rint_t2_dev_20261013/t2_dev_v2.json` · README §3-1 (개발 표지) |

로그 끝 줄 `[runlog] cmd: … · rc=… · 초` = 실행 명령 · 종료 코드 · 벽시계 (같은 기계 4 코어 공유 · OMP/OPENBLAS/MKL_NUM_THREADS=1 · nice 10).

## 2. 명령 · rc (고치기 전 → 수정 뒤)

| 명령 (`python3 …`) | 고치기 전 (`tests_first/`) | 수정 뒤 (`final/`) |
|---|---|---|
| `scripts/test_rint_t2_dev.py` | rc 1 · 10 PASS / 10 FAIL — 옛 10/10 · 새 0/13 (D6b 넷 = `offset_um` 인자 없음 실행 1 FAIL) | rc 0 · **23/23** · 1 s |
| `scripts/test_rint_g2_join.py` | rc 1 · 43 / 30 — 옛 40/40 · 새 양성 3 통과 · 새 30 FAIL (J5 마지막 scaffold nan = `TypeError` 로 중단) | rc 0 · **73/73** · 146 s |
| `scripts/test_rint_g2_rrm.py` | rc 1 · 43 / 11 — 옛 39/39 · 새 4 통과 (픽스처 · 음수 rface (옛 판도 rface_mismatch) · 우회 σ 기록 · 양성) · 새 11 FAIL | rc 0 · **54/54** · 4 s |
| `scripts/test_rint_g2_am_iface.py` | rc 1 · 129 / 2 — 옛 126/126 · 새 3 통과 · 새 2 FAIL (음성 · 관문 `vox` 인자 실행) | rc 0 · **132/132** · 7 s |
| `scripts/test_rint_t4_census.py` · `scripts/test_rint_t43_order.py` | (무변경 시험 · 수정 뒤만) | rc 0 · 8/8 · 6/6 |
| `scripts/step3_sigma.py --selftest` · `--selftest-rint` | (무변경) | rc 0 · PASS · PASS |
| `scripts/rint_t41_census.py --selftest` (조인 모듈 소비자) | (무변경) | rc 0 · PASS |
| `off_compat_16.py --old <44a034534 판> --new scripts/step3_sigma.py` | — | rc 0 · **16/16 비트 같음** |
| `off_compat_16.py --old <1d9af09d0 판 (①′ 전)> --new scripts/step3_sigma.py` | — | rc 0 · **16/16 비트 같음** |

합: 기존 229 (126 · 39 · 40 · 8 · 6 · 10) + 두 자체시험 그대로 통과 · 새 검사 67 (T2 13 · 조인 33 · RRM 15 · am_iface 6) · 수정 뒤 296/296.
옛 판 사본 = `git show 44a034534:scripts/step3_sigma.py` · `git show 1d9af09d0:scripts/step3_sigma.py` (리포에 넣지 않음 · sha256 = `final/HASHES.txt` · 둘 다 Codex 묶음의 OFF 비교 두 판과 같은 sha256).

## 3. Codex 반례 값 ↔ 우리 시험 (우리 트리 재현)

| RIMP | Codex 값 (판정문 §) | 우리 시험 | 고치기 전 (우리) | 수정 뒤 |
|---|---|---|---|---|
| 01 | 15° n64 축별: 최대 0.5376755856 · L2 0.01306318860 → 경계 대조 0.006475555385 · 0.0004495112904 (§2) | D7 | 0.5376755856 · 0.0130631886 (같음) | 대조 값 재현 (상대 ≤ 2.4e−10 · 인쇄 10 자리 한계) |
| 01 | 30° n16: 0.5038084527 · 0.04096008793 → 0.01633704071 · 0.003087791839 | D7 | 같음 | 재현 |
| 01 | 이동 45° n128 (tie 0): 0.4439262878 · 0.003883094200 → 0.004030350534 · 0.0009823643239 | D7 | 같음 | 재현 |
| 01 | 15° n64 L1: 0.5324747283 · 0.01282826063 → 0.02030409571 · 0.001406042364 | D7 | 같음 | 재현 |
| 01 | (우리 추가) θ 0 · β 0 · 계면 x = ∓0.78 µm (경계 반 셀 안) — 정확 이산 층 | D6a · D6b | 최대 0.397 · 0.352 | 반올림 안 · 변이 셋 판별 |
| 01 | 45° n128 원점 대칭 (tie 128): Codex Windows 대조 0.005660516619 | D8 (tie 수만) | — | Linux 0.007143742553 — tie 배정 플랫폼 의존 (회귀 밖) |
| 02 | real14 22 행 (id 1 · 201) pos1.x · δ · A = NaN → PASS (§3-1) | J5 | 거부 없음 | `nonfinite_value` |
| 02 | A −1.8247e−06 → PASS · tested 660 → 659 | J5 | 거부 없음 | `area_negative` |
| 02 | 다른 tilt (원자 0.001 · 접촉 0.002) → `box_equal` true · PASS (§3-2) | J5 | 거부 없음 | `box_tilted` (같은 tilt 도) |
| 02 | step 2060000.9 → 2060000 으로 줄어 PASS | J5 | 거부 없음 · step 2060000 | `int_token` · step None |
| 02 | 근동심 면적 100 sim² → tested 0 · uncertified 1 · PASS | J7 (`%g` 로 다시 만듦 — 중심 거리 1e−8 sim · δ 0.00199999) | 거부 없음 | `area_uncertified` (참 면적도) |
| 02 | 조인 → 원장 → 계획 (join=…) → 정량 관문: NaN · 음수 · 기울어진 상자 = 통과 | J8 (+ 16 자리 +1 ppm) | 셋 다 통과 | 조인 REJECT → `join_gate_failed` → 관문 거부 |
| 02 | (우리 추가) A inf · id2 `201.0` · type `1.0` · 머리 수 `33289.0` · 반경 −0.006 · 상자 lo ≥ hi · scaffold nan | J5 | A inf = 거부 없음 (inf − inf = NaN 비교 — 같은 부류) · 비정수 셋 = 거부 없음 · 반경 = 다른 사유 · scaffold nan = 예외 | 사유별 거부 |
| 03 | 16 자리 균일 · +1 ppm (A 1.374448160392321e−06 · 16 자리 포괄 [1.3744467859455032e−06, 1.3744467859455659e−06]) → tested 1 · beyond 0 · PASS (§4) | J6 · J8 | PASS | `numeric_format` (16 자리 기준 자체도) |
| 03 | 끝 0 토큰 `0.0250327 → 0.02503270000000000` (값 같음): 원자 pos 7 행 · 접촉 pos 21 · δ 99,113 행 (§4 한정) | J6 | REJECT (`pos_mismatch` · 사유 다름) | `numeric_format` (입구 · 전역 S 를 올리지 않는다) |
| 03 | 정상 자료 = 6 자리 | J1 · J2 · J6 · J9 | PASS | PASS 유지 — real14 · case15 덤프 실수 토큰 전부 = `'%g' % 값` (고유 토큰 92,752 · 295,718 · 185,269 · 511,051) · 정수 열 전부 정수 문자열 (수정 전 별도 검사) |
| 04 | fixture A σ 0.003334457143882423 · film 67 · cut 85 (§5) | N9b | 0.0033344571438824267 | 같음 |
| 04 | cut 85 삭제 + resolve_k 4→5 / + r 표 비움 → 위반 없음 · σ 0.0040840140889134725 | N9b | 위반 없음 · 풀이 | 위반 (`excluded_without_rejection` 1 · `row_for_excluded_contact` 67 · `plan_not_reproducible` 8) · wrapper 거부 |
| 04 | film 67 행 rface NaN → 위반 없음 · σ 0.0037299595666211234 · unconverged False | N9b | 위반 없음 · 풀이 | `rface_nonfinite` 67 · `rface_mismatch` 67 · `plan_not_reproducible` 1 · 거부 |
| 04 | (우리 추가) k 만 4→5 (행 그대로) · `iface_rrm` 삭제 · 음수 rface · 양성 r = 0 계획 | N9b | 앞 둘 통과 · 음수 = 이미 거부 | 앞 셋 거부 · r = 0 = 위반 없음 |
| 05 | h 0.2 계획 · 같은 sid · h 0.4 솔버 → 풀이 · 실제 막 G 2.5007077522574787e−6 = 기록 6.251769380643698e−7 의 4 배 (§6) | T0-7 | 풀이 (CG 호출 1) | 조립 전 거부 (CG 호출 0) |
| 05 | 정상 재생성 계획 σ 0.0021331551689598217 · A · G 4 배 | T0-7 | 통과 | 통과 (상대 ≤ 1e−9 · A · G 4 배 1e−12) |
| 06 | fixture A 표준 원장 active 152 · cut 0 (실제 67 · 85) (§7) | RRM-7 | 152 · 0 | 67 · 85 · `film_G_S_total = {rrm: ΣG}` |
| 06 | 반쪽 탄소: RRM G 2.7535056597827278e−6 ↔ 상속 2.612935414333538e−6 / 5.027420037705035e−6 | RRM-7 | 상속값이 표준 | 표준 = RRM G · CNC = `iface_cnc_comparison` |

일반 솔버 (`step3_sigma.solve_sigma_z`) 에 RRM 변이 계획을 **직접** 주면 지금도 받는다 (RRM 을 모르는 설계 · 판정문 §5 *"새 결함으로 세지 않았다"*) — N9b 가 그 우회 크기를 기록으로 재현한다 (0.004084014088913466 · 0.0037299595666211278 S/cm).

## 4. iface 끔 비트 같음 (`final/off_compat_16_vs_*.json`)

16 사례 = h 0.1 · 0.2 × 입자 순서 둘 × 브리지 0.24 · 기본 × r1 끔 · 켬 (판정문 §1-2 의 OFF 비교와 같은 격자) · 두 쪽 같은 직접 풀이 (spsolve).
rasterize (sid · pid) + `solve_sigma_z(iface=None, return_field=True)` 전체 반환 dict (키 · 값 · 배열 dtype · 모양 · 바이트 · float = hex) 비교:
수정 뒤 ↔ 고치기 전 (`44a034534`) **16/16 같음** · 수정 뒤 ↔ ①′ 전 (`1d9af09d0` = Codex `source_prior`) **16/16 같음**.
σ 값 ↔ Codex Windows 표 (`docs/reviews/codex_rint_g2_impl_review_evidence_20261014/evidence/off_compatibility.json`) = 끝자리만 다름 (최대 상대 6.9e−15 · 플랫폼 직접 풀이 차 — 같은 기계 old ↔ new 는 비트 같음).
⚠ 16 사례 통과 = 전 입력 공간의 동등성 증명이 아니다.  바뀐 것은 iface 관문 (`iface_require_quantitative(vox=…)`) 뿐이고 iface=None 경로는 그 관문을 부르지 않는다.

## 5. 하지 않은 것 · 한계

- Codex 탐침 재실행 = Codex 몫 (요청서 §3 — 고친 트리에서 기대 결과 · 탐침이 고친 판에서 멈추는 자리 두 곳 표지).
- T2 정식 검증 (flux · 에너지 · 원점 · 3D · tie 규약) · D11 · D12-V 봉인 · ①′ 정량 채택 · 생산 = 이번 범위 밖 (HOLD 그대로).
- 일반 생산 관문의 rface 유한 검사 (RRM 밖 계획 전부) 는 넣지 않았다 (Q3 범위 = wrapper) — 요청서 질문.
- 봉인 32 (`lhs_descriptor_harvest.py` · `lens_geometry.py` 포함) · `findings.json` · CLAUDE.md · 웹앱 = 무변경.
