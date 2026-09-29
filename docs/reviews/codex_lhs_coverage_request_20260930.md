# Codex 적대 리뷰 요청 — LHS 피복률 두 묶음 (수확기 item 1–4 · 웹앱 physics v2 cap) · 병합 전 (2026-09-30)

> 1저자 결정 (09-30): *"coverage 관련해서 에이전트 결과를 codex 한테 리뷰를 받으면 좋지 않을까?"* — 에이전트 두 개가 만든 7 커밋을
> **병합하기 전에** 적대 리뷰를 받는다.  이 요청서는 리뷰 대상 · 주장 · 질문 · 재현 방법만 적는다 (판정은 Codex).  발송 = 1저자.
> ⚠ 이 7 커밋은 아직 `claude/stoic-knuth-NObVQ` 에 **없다** — 패치로만 전달한다 (§1).  리뷰 뒤 한 항목씩 병합한다.
> ✅ **1저자 발송 (09-30)** · 고정 스냅샷 = **`2e57dff90`** (이 요청서가 처음 든 커밋 · 패치 7 이 그대로 붙는다 — 확인함).  §4 첫 줄 정정 (아래 · 09-30).
> ⛔ **판정 도착 (09-30) = 묶음 전체 HOLD · 새 P1 2 · P2 3** — `docs/reviews/codex_lhs_coverage_verdict_20260930.md` · 증거 `codex_lhs_coverage_evidence_20260930/` · 원장 `LHSC-01`~`LHSC-10`.
> Codex 가 본 트리 = `da4670594` + 패치 0001–0007 (8 파일 · 줄바꿈 정규화 뒤 우리 `64ae3cba8` 과 바이트 동일) · 우리 트리 재현 = 네 감사 스크립트 전부 같은 결과.
> GO 4 = 0001 (item 4 벽 규칙) · 0002 (item 1 벽 제외 — 분모 보정 proxy 로만) · 0004 (item 3 접촉 문) · 0005 (film_area_physics_v2 — 후보 연산자) · HOLD 3 = 0003 (P2) · 0006 (P1) · 0007 (P1).
> 다음 = 반례를 셀프테스트로 먼저 옮긴 뒤 0006 → 0007 → 0003 수정 → Codex 재검증 → 의존 순서대로 한 항목씩 병합.

## 0. 배경 — 왜 지금

- LHS 인계표 (수영 ML 용) 는 **1저자와 함수 단위로 같이 확인한 열만** 싣는다 (J20-g · `docs/reviews/lhs_handover_judgments_20260924.md`).
  피복률 (coverage) 열은 아직 하나도 실리지 않았다 (지금 실린 웹앱 열 = 계면 개수 `area_<쌍>_n` · SE–SE CN 두 열).
- 09-29 밤 1저자 비준 (*"권고대로"*): ① 수확기 coverage 의 결함 넷 (item 1–4) 수정 ② 웹앱 physics (cap) coverage 의 새 판 (v2) 을 legacy 옆에 **병기**.
  두 에이전트가 각자 워크트리에서 반례 먼저 · 시험 먼저로 구현했다.  둘 다 **옛 키 · 옛 값 바이트 그대로 + 새 키만** 이라고 주장한다
  (예외 = item 4 가 일부러 바꾼 `wall_touch_rule` 문자열과 정확히 접선인 입자의 `wall_touch`).
- 병합 뒤 순서: WSL 재수확 (v3) + 웹앱 `--stop-after coverage` 배치 → 09-29~30 옛 코드 기준선
  (`docs/data/{lhs,lhsx}_{descriptors,webapp_contact}_20260929/`) 과 비교 → 함수 검토 → 표.

## 1. 스냅샷 · 전달 방식

- **기준 커밋 = `da4670594`** (`claude/stoic-knuth-NObVQ` 에 푸시됨).  패치 7 개는 그 위에 순서대로 붙는다 (`git am`).
- 원 커밋 (에이전트 브랜치 · 기준 `e72067854` · 로컬 전용): 수확기 `1dfae6661` → `a2b0b5369` → `69d7cb678` → `7d8f696fc` ·
  cap v2 `166b59724` → `d65afca14` → `59a0e1ecf`.  기준을 `da4670594` 로 옮기며 **충돌 한 곳** (`scripts/lhs_webapp_batch.py` selftest 번호) 을 풀었다 (§5).
- 증거 폴더 `docs/reviews/codex_lhs_coverage_request_20260930/`: `patches/0001–0007-*.patch` · `SHA256SUMS` · `selftests.log` (우리 재실행) · `gate.log` (검토용 묶음 전체 게이트).

## 2. 커밋별 주장 (에이전트 커밋 메시지 요약 — 검증 대상)

| 패치 | 원 SHA | 파일 | 주장 | 시험 (옛 코드 → 새) |
|---|---|---|---|---|
| 0001 | `1dfae6661` | `scripts/lhs_descriptor_harvest.py` | **item 4** 벽 닿음 규칙 하나 — `_wall_dists` (부호 있는 중심–면 거리) · `_wall_contact` (깊이 · 닿음 · 중심 밖 · 통째로 밖 · cap 높이) 를 `_wall_side` · `wall_touch_fractions` · 벽 분할 피복률이 같이 부른다.  규칙 = 겹침 깊이 > 0 (**접선 = 안 닿음**) — 이유: 벽 밖 부피 · 가린 표면이 h > 0 에서만 0 이 아니다 · 09-24/25 수확 JSON `wall_record.*.n_touch` 가 이미 이 규칙.  무작위 200 침대에서 옛 두 규칙이 126 곳 어긋났다 | 100/105 → 105/105 |
| 0002 | `a2b0b5369` | 같은 파일 | **item 1** 벽 분할 · 벽 제외 피복률 (새 키만): `coverage_AM_{P,S,total,only}_wallexcl_pct` · `coverage_wall_split` (상 × 벽 any/floor/plate × 등급 interior/touch/center_out/fully_out).  벽 제외 분모 = 4πr² − ΣA22(AM–AM) − Σ_벽 2πr·clip(r − dist, 0, 2r) · 분모 ≤ 0 은 제외하고 셈 · 근사 (분모의 AM–AM 원판과 cap 곡면이 겹칠 수 있음 · 분자 원판이 cap 안일 수 있음 — 교차 계산 없음).  옛 38 키 = 변경 전 코드 황금 해시 | 108/120 → 120/120 |
| 0003 | `69d7cb678` | 같은 파일 | **item 2** 접촉 면적 대조 `contact_area_check` — 행마다 `plastic_coverage._intersection_disc_area(r1, r2, δ = c_cpl[23])` 와 `c_cpl[22]` 의 차를 허용폭 (6 유효숫자 `%g` 반올림 반폭을 r1 · r2 · δ 로 전파 + 면적 토큰 반폭 · ×1.001 · 부동소수 바닥) 과 비교해 **세기만** (거부 없음 · 주기 플래그별 · 쌍 종류별).  DESC-03 가드를 소스 전체 AST · 허용 이름 하나로 개정 | 120/129 → 131/131 |
| 0004 | `7d8f696fc` | 같은 파일 | **item 3** `contact_gate` — 피복률이 실제로 쓰는 마지막 블록에서 무순서 중복 쌍 · 자기쌍이면 `BedRefusal` · 고아 행은 셈 (`contact_gate` 새 키).  옛 코드는 같은 AM–SE 행 두 번이면 AM_S 피복률 25 → 50 % 를 OK 로 냈다.  130 은 09-29 접촉 감사에서 중복 · 자기쌍 · 고아 0 · lhsx 64 는 재수확 v3 에서 처음 이 문을 지난다 | 130/139 → 139/139 |
| 0005 | `166b59724` | `scripts/plastic_coverage.py` (+ 시험 목록) | **cap v2 면적 함수** `film_area_physics_v2` (legacy `film_area_from_overlap` 한 줄도 안 바꿈): δ/R* < DR_YIELD_ONSET → πR*δ (legacy 탄성과 비트 동일) · 그 위 → A = U = min(A_tabor, A_volume, A_geom) — cap 은 **전체 면적의 상한** · L = max(πR*δ, A_LIGG) > U 이면 U + `cap_conflict` (L1-01) · A_volume = 정확한 전체 lens / (H_FILM_MIN × length_scale) (L1-02 · DESC-03) · 정의역 밖 입력 = 예외.  ⚠ 귀결: 얕은 겹침에서 v2 면적이 πR*δ 보다도 작을 수 있고 (δ/R* 0.01 · r 0.5 µm: A_v2 = 0.4996 πR*δ = 0.2501 A_LIGG) 항복 개시에서 **불연속**으로 떨어진다 (SE–SE r 0.5 µm ×0.0566) | 16/27 → 27/27 |
| 0006 | `d65afca14` | `scripts/coverage_physics_vs_hertzian.py` · `docs/area_contract_20260913.md` §F | **v2 키 병기** `*_physics_v2` (피복률 · 면적 합 · cap 가지 수 · 충돌 수/비율 · 정수 접촉 수 · 상태 · 사유) · 분모 = 4πr² − Σ v2 AM–AM (분자와 같은 장부 — legacy 는 native c_cpl[22]) · 접촉 하나라도 v2 가 거부하면 침대 v2 = 빈칸 + 사유 (**조용한 대체 없음**) · scale ≠ 1000 · δ/면적 열 없음도 빈칸 · legacy 키 · 값 · 순서 = e72067854 코드로 잰 sha256 핀.  ★ 새 결함 (원장 미등재): `<case_id>` 호출이 스크립트 옆 `webapp/` 만 봐서 데이터가 코드 밖인 배치에서 이 단계가 `[skip]` · rc 0 으로 아무것도 안 썼다 → `WEBAPP_*_FOLDER` 를 따르게 함 (그런 배치에서 이제 legacy physics 키도 실제로 쓰인다) | 2/13 → 13/13 |
| 0007 | `59a0e1ecf` | `webapp/app.py` · `scripts/lhs_webapp_batch.py` · `webapp/test_pipeline_provenance.py` · 계약 §F | `run_pipeline(stop_after='coverage')` — 접촉 → 피복 (legacy + v2) 에서 멈춤 · 이 모드에서 피복 단계는 required + 내용 검증 (`coverage_status_physics_v2` 를 이번 실행이 썼는가) · 밖의 값은 ValueError · 배치 `--stop-after coverage` · 산출 폴더에 모드를 섞지 않는 관문 (세 모드).  인계표 생성기는 아직 contact 만 알아 coverage 폴더를 거부 (fail-closed · 후속) | provenance 189/198 → 198/198 · 배치 21/23 → 23/23 (병합 뒤 29/29) |

## 3. 질문

**Q1 (0001 · 접선 규칙)** 겹침 깊이 > 0 (접선 = 안 닿음) 을 모든 소비자가 쓰는가 — 옛 `≤` 에 기댄 경로가 남았나?  덤프가 6 유효숫자 (`SELF-63`) 라
"정확한 접선" 판정 자체가 반올림 폭 안에서 흔들리는데, 이 규칙이 그 폭에 대해 안정한가 (접선 부근 입자 수 · 결과 민감도)?
⚠ 에이전트가 적었듯 생성기 열 사전 (`wall_touch_frac_*` · "z − r ≤ 0 · z + r ≥ plate_z") 은 옛 문구다 — 병합 때 맞춘다.

**Q2 (0002 · 벽 제외 분모)** 4πr² − ΣA22 − Σ cap 의 근사 (겹치는 두 차감 · cap 안 분자) 가 벽 제외 피복률을 어느 쪽으로 · 얼마나 치우치게 하나?
분모 ≤ 0 제외가 조용한 선택 편향이 되지 않나?  바닥 (SE 물성 평면 = 분리막 proxy · `LHS-14`) 과 플래튼 (SUS · AM 물성) 을 나눈 것이 맞나?

**Q3 (0003 · 면적 대조 허용폭)** 허용폭 규칙이 6 유효숫자 반올림만 있는 입력을 **모두** 덮고 (거짓 경보 0), Hertz 면적 (πR*δ) 대입이나
3e-5 상대 오차는 **모두** 잡는가?  DESC-03 가드 개정 (소스 전체 AST · 허용 이름 `_intersection_disc_area` 하나 · 금지 모양 여섯) 이
원래 뜻 (수확기는 Physics 피복률 경로를 부르지 않는다) 을 더 넓게 지키나, 새 구멍이 있나?

**Q4 (0004 · 접촉 문)** 문보다 **먼저** 피복률을 계산하는 경로가 남았나?  주기 경계 · MPI 고스트에서 LIGGGHTS 가 한 쌍을 두 행으로 낼 수 있는
정상 경우가 있다면 (130 은 0 건 · lhsx 64 는 미감사) 거부가 과잉인가?  고아 행을 `coverage_hertz` dict 에만 두고 JSON 에 안 싣는 것이 맞나?

**Q5 (0005 · v2 면적 계약)** cap 을 "전체 면적 상한" 으로 두고 L > U 면 U 를 내는 것 (legacy 는 하한 max 를 먼저) 이 피복률에 쓸 면적으로 옳은가?
얕은 겹침에서 πR*δ 보다 작아지고 항복 개시에서 불연속 (×0.0566) 인 면적으로 만든 피복률을 **인계 열**로 쓸 수 있나 — 매끈하게 이어야 하나,
표지만 달면 되나?  A_volume 의 `H_FILM_MIN × length_scale` (덤프 단위 막 두께) 변환이 단위상 맞나 (`scale` = 1000 가정)?

**Q6 (0006 · v2 키 · 조용한 대체 없음)** 침대 단위 빈칸 (접촉 하나라도 거부) 이 너무 엄격하지 않나 (한 행의 NaN 이 침대 전체를 지움)?
legacy 바이트 동일 핀 (e72067854 코드를 합성 침대에 돌린 sha256) 이 legacy 경로의 **모든** 산출 (키 · 값 · 순서 · `coverage_per_am.csv` · 반환값) 을 덮나?
`WEBAPP_*_FOLDER` 수정으로 **배치 레이아웃에서** legacy physics 키가 이제 쓰이는 것 — 웹앱 주 경로 · 코퍼스 스크립트 (`full_metrics.json` 을 읽는 쪽) 에
보이는 행동 변화가 있나?

**Q7 (0007 · stop_after='coverage')** "required + 내용 검증" 이 옛 산출이 남은 폴더 (이전 실행의 `full_metrics.json` 에 같은 키가 이미 있음) 에서
거짓 done 을 내지 않나?  세 모드 섞기 관문에 빠진 방향이 있나?

**Q8 (병합 충돌 해결)** §5 의 `lhs_webapp_batch.py` 해결 (지금 브랜치의 mono 이름 접기 시험 ⑭–⑭f 를 먼저 · cap v2 시험을 ⑮ · ⑯ 으로) 에서
두 블록 사이에 넘어가는 상태 (`FakeA.mode` · `FakeTMR.m` · 수확 JSON 을 3-type 으로 되돌림) 에 숨은 의존이 있나?

**Q9 (전체)** 선언한 둘 (`wall_touch_rule` 문자열 · 접선 입자의 `wall_touch`) 밖에서 **기존 산출값**을 바꾸는 곳이 있나?  남은 조용한 대체 · 조용한 skip 이 있나?

## 4. 재현

```bash
git fetch origin claude/stoic-knuth-NObVQ && git checkout -b cov-review 2e57dff90
git am docs/reviews/codex_lhs_coverage_request_20260930/patches/*.patch
python3 scripts/lhs_descriptor_harvest.py --selftest
python3 scripts/plastic_coverage.py --selftest
python3 scripts/coverage_physics_vs_hertzian.py --selftest
python3 scripts/lhs_webapp_batch.py --selftest
python3 webapp/test_pipeline_provenance.py
python3 scripts/lhs_design_dataset.py --selftest
bash scripts/check_all.sh
```

⚠ **정정 (09-30)**: 첫 판은 `git checkout -b cov-review da4670594` 였다 — 그 커밋에는 패치 폴더가 없어 그대로 치면 `git am` 이 실패한다.
`2e57dff90` = `da4670594` + 문서만 (요청서 · 증거 · prereg · 진행) 이라 패치 7 이 같은 결과로 붙는다 (확인: 7 커밋 · 8 파일 · 검토용 묶음과 같은 diffstat).

## 5. 우리 재실행 결과 · 병합 충돌

- 7 커밋을 `da4670594` 위에 `cherry-pick -x` 로 쌓았다 (로컬 `review-coverage-20260930`): 0001–0006 충돌 없음 · 0007 에서 `scripts/lhs_webapp_batch.py` **한 곳**.
  원인 = 두 쪽이 selftest 끝의 같은 자리에 각자 ⑭ 블록을 넣었다 (지금 브랜치 `70e1203be` 의 mono 이름 접기 시험 ⑭–⑭f · cap v2 의 `--stop-after coverage` 시험 ⑭–⑮).
  해결 = 둘 다 살림 · 지금 브랜치 블록을 먼저 · cap v2 블록 번호를 ⑮ · ⑯ (변수 `r14`/`rc14`/`st14` → `r15`/`rc15`/`st15`) 로 · 충돌 구역 밖은 자동 병합 결과와 한 글자도 다르지 않다.
- 셀프테스트 (검토용 묶음 · `selftests.log`): 수확기 **139/139** · `plastic_coverage` **27/27** · `coverage_physics_vs_hertzian` **13/13** · 배치 **29/29** ·
  파이프라인 **198/198** · 인계표 생성기 **113/113** — 에이전트 보고 수와 같다 (배치는 병합 뒤 29).
- 전체 게이트 (검토용 묶음): **통과** — `bash scripts/check_all.sh` (검토용 묶음 = `da4670594` + 패치 7) · 74 줄 · ✗ 0 · `✓ 전부 통과` (`gate.log`).  에이전트 쪽 게이트는 워크트리 격리 가드로 mixer launcher 단계 하나를 못 돌렸다고 적었는데, 이번 재실행은 그 단계까지 돌았다.
- 패치에 모델 식별자 없음 · 끝줄 `Co-Authored-By: Claude` 로 통일돼 있다.

## 6. 받고 싶은 것

- 커밋마다 **GO / HOLD** (HOLD 면 반례 — 입력 · 기대 · 실제).
- **P1** (값이 틀린다 · 조용한 대체 · 옛 값 변경) / **P2** (한정어 · 문서 · 시험 공백) 구분.
- 병합 전 최소 수정 목록.  원장 번호는 우리가 매긴다 (`findings.json` 은 이 요청에서 안 건드렸다 — 0006 의 새 결함 포함).

## 7. 범위 밖

- 인계표에 어떤 열을 실을지 (1저자 · 함수 검토 J20-g).  `H_FILM_MIN` · `DR_YIELD_ONSET` 같은 물성 상수값 자체.
- network · Stage E (legacy 그대로 — v2 는 coverage 쪽만 · `docs/area_contract_20260913.md` §F).
