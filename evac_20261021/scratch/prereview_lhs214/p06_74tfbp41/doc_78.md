# LHS 194 망 단계 배치 — 세대 2 실행 등록 (초안 · 2026-10-07 새벽 KST · 결과 0 건) · ⛔ 발사 = Codex GO 뒤

- 근거: Codex 세대 2 재검증 판정 `docs/reviews/codex_review_gen2_network_reverify_20261006.md` §7 — ③ 새 실행 봉인 (새 ROOT · 194 ID · cohort · 원 dump 해시 ·
  전체 전이 코드 의존성 · H0/Physics/H12 기대 조합 · 스키마 · 증서 문턱 · 실패 정책을 기록하고 러너가 재검사 · S3 봉인 별도 갱신) · ④ 실덤프 사전 점검 · ⑤ 음성 대조.
- 1저자 (10-06 밤): 새 194 = Codex GO 뒤 (병렬 안 함) · v1.3 = GO 뒤 한 번에 · v1.3 = 최종판 · 고친 것 셋 (G2RR-01 · 02 · 03) 비준 *"권고대로"*.
- 앞 등록 (형식 · 운영 부분의 원본): `docs/reviews/lhs_network_batch_registration_20261005.md` (19 파일 봉인 · 194 v1.2 배치 `11fcf91e8`).
- 이 문서는 **배치 전에** 커밋한다.  결과를 본 뒤 고치지 않는다 (고치면 §9 덧붙임 + 사유).
- ★★ **10-07 재등록** (Codex 세대 2 재검증 2 = HOLD · `docs/reviews/codex_review_gen2_network_reverify2_20261007.md` · G2RR2-01 ~ 05 수정 · 1저자 *"해결해놔"* =
  판정문의 최소 수정 그대로) — **결과 0 건에서** 다시 등록한다 (사전 점검 · 시범 · 194 모두 아직 · §0 3 항 *"고친 뒤 이 문서를 새로 등록"*).
  바뀐 것: §3 코드 신원 (29 → 32 파일 · `code_fp e8b2496b…`) · §3b 실행 형식 v3 (필수 선언 · 역사 형식 = 등록 + `--historical`) ·
  §1 · §5 다시 읽기 등록 집합 (`--expect-set pilot3` · `production194`) · §1 시범 import 관측 (`--observe-imports`) · §7 S3 봉인 목록.
> ★ **10-07 Codex 재검증 3 뒤 수정 (G2RR3-01 `3f9f86f59` · G2RR3-02 `66c09ef68` · 1저자 *"ㄱㄱ"*)** — 봉인 32 파일 · `code_fp e8b2496b…` 그대로 (실행기 · 다시 읽기 · 배포 생성기는 봉인 밖).  §1 · §5 의 명령은 그대로이고 뜻이 바뀐다: 시범 `--observe-imports` = 프로세스마다 시작 영수증 + 원자적 끝 기록 (신원 · 필수 역할 = 워커 · 망 솔버) → audit 가 빈 · 부분 · 미최종 로그를 거부 · 다시 읽기 JSON v3 = 배치 뿌리 · manifest sha256 · 봉인 지문 · 발사 sha 결합 · v1.3 생성기 = ⓪ 감사 · ⓪b 다시 읽기 **둘 다 필수** · 이 배치 결합 · SEALED 만 (옛 기록 = `--diagnostic-batch-gate` · 배포 아님).  발사 커밋 = 이 수정이 들어간 커밋 이후 (인계 도구 지문은 발사 때 manifest 에 기록).  재검증 4 요청서 = `docs/reviews/codex_gen2_network_reverify4_request_20261007.md`.
  그대로인 것: §2 (194 ID · 코호트 · 원자료 지문 · 09-17 cutoff) · §5 판정 순서 · §6 인계 경로.
  ⛔ 옛 지문 `f3f54951…` (29 파일 · 재검증 2 핀 `9d25757dc` 의 값) · `b313e61a…` (29 파일 · 이 문서 10-07 05:2x 판 — app.py 갱신 뒤) 은 **역사** — 승인값으로 다시 쓰지 않는다 (판정문 §10-2).
  ⛔ 이 재등록은 발사 GO 가 아니다 (판정문 §10-4 *"이번 회신을 자동 또는 조건부 발사 GO 로 읽지 않는다"*) — 재검증 3 · WSL 사전 점검 증거 · 1저자 발사 승인 뒤.
  ⚠ v1.3 화면 패치 (`docs/reviews/lhs_release_v13_display_deferred_20261007.patch` — `webapp/app.py` 를 바꾼다 = 봉인 파일) 는 **발사 뒤에만** 적용한다
  (발사 전에 적용하면 봉인 지문이 바뀌어 이 등록의 배치가 아니다 · 10-07 이 커밋 트리에서 `git apply --check` 통과).
  ⚠ 웹앱 3D 자료 패치 (`docs/reviews/webapp_load_view_deferred_20261007.patch` — #11 AM 만 칠하기 · WEB-06 압축 접촉만 범위 · 같은 봉인 파일 `webapp/app.py`) 도 **발사 뒤** ·
  v1.3 화면 패치와 같은 때 넣는다 (1저자 10-07 Q3 *"권고대로"*) · 두 패치는 순서 무관 (10-07 HEAD `afda0d7ab` 에서 `git apply --check` 양쪽 순서 통과) · 넣은 뒤 `bash scripts/check_all.sh`.
> ★★ **✅ 10-21 · 1저자 비준 — L214 개정 (§9-8 · 결과 열람 뒤 정책 개정 = 10-14 실행 결과를 본 뒤) · 변경 이력 = §9-9** — §3 활성 봉인 지문 = `2149f873…` (§9-8 의 대기 선언을 §3 으로 옮기고 선언은 지웠다 · 10-07 재등록 `e8b2496b…` = 역사) · §5 활성 개정 = §9-8 ①–⑦ · 원문은 각 자리에 그대로.  ⛔ 이 비준은 발사 승인이 아니다 (§9-8 ⑦ B7 — 새 승인 핀 사전 점검 · 1저자 별도 발사 승인) · S3 = 별개 HOLD.

## 0. 순서

1. **지금 (Codex 재검증과 병렬 · 1저자 WSL)** — §1 사전 점검 (§7-4).  격리 ROOT 만 쓴다 · 아무것도 인계하지 않는다 · 결과 = §9 덧붙임 + 재검증 요청서 보충.
2. Codex GO → 1저자 발사 승인 → §4 발사 → §5 판정 · 관문 → §6 인계 v1.3.
3. Codex 가 값에 영향을 주는 결함을 찾으면 고친 뒤 이 문서를 새로 등록한다 (§3 표가 바뀌므로 이 봉인으로는 발사하지 않는다).

## 1. 사전 점검 (판정 §7-4) — 지금 · WSL · 격리 ROOT

목적 = real14 · case15 · 정상 비관통을 **생산 → 후보 검사 → 게시 → 인계** 까지 통과시키고, raw 숫자만이 아니라 게시된 **증서 · 도장 · 진단 상태 · 열 역할**을 다시 읽는다.

| 침대 | 출처 | 경로 |
|---|---|---|
| real14 (33,289 입자 · 106,563 접촉 · 3 상) | 커밋된 `docs/data/real14_reference_20260928/` | `wsl_network_smoke.py` (실제 웹앱 `run_pipeline(stop_after='network')`) |
| case15 (65,970 입자 · 182,995 접촉 · AM_P + SE) | 커밋된 `docs/data/case15_corner_20261001/` (★ 이 커밋에서 스모크에 추가) | 같음 |
| `lhs00_055` (관통 · bimodal · 접촉 가장 적은 관통 lhs) | LHS 코호트 원자료 | 스모크 + **194 실행기 시범** |
| `lhs00_128` (**정상 비관통** · 4,616 접촉 · 비관통 24 중 접촉 가장 적음 · v1.2 τ 두 모드 NOT_PERCOLATING) | 같음 | 같음 |
| `lhsx_007` (관통 · lhsx 접촉 가장 적음) | 같음 | 같음 |

- ⚠ 한정: real14 · case15 는 LHS 코호트가 아니라 194 실행기에 넣을 수 없다 — 생산 · 게시는 실행기의 워커가 부르는 **같은 함수** (`app.run_pipeline(stop_after='network')`) 를
  스모크 도구가 직접 부른다.  실행기 고유 층 (발사 봉인 · 기대 세대 · merge · 배치 기록 · 인계 출처 관문의 진짜 배치 기록) 은 LHS 셋의 시범이 맡는다.
- 다시 읽기 = 새 도구 `scripts/g2_network_reread.py` (읽기 전용 · 게시 · 인계가 쓰는 같은 함수를 지금 파일에 다시 부른다): K1 게시 · K2 세대 계약 + 증서 결합 (모드 셋 × 가지 셋) ·
  K3 도장 ↔ 레코드 · K4 정지 계약 다시 · K5 열 역할 (행 세대 계약) · K6 관통 일치 · K7 가지 표 · H1 인계 출처 관문 (`load_tau_results` · 기대 세대) · (시범) M0–M2 manifest.

```bash
# ── 0. 체크아웃 (detached · 깨끗한 트리) · 파이썬 = 배치 venv ──
cd ~/dem-audit
git fetch origin claude/stoic-knuth-NObVQ
git checkout --detach origin/claude/stoic-knuth-NObVQ
git log -1 --oneline
echo "dirty 줄 수 = $(git status --porcelain --untracked-files=no | wc -l) (0 이어야)"
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1)
$PY -c "import numpy, scipy, networkx; print(numpy.__version__, scipy.__version__, networkx.__version__)"
S=$(git rev-parse --short HEAD); T=$(date +%m%d_%H%M)
DL=/mnt/c/Users/Administrator/Downloads        # 다른 PC 면 /mnt/c/Users/안용훈/Downloads

# ── 1. 도구 자체 시험 (합성 침대 · 몇 분) ──
$PY scripts/g2_network_reread.py --selftest 2>&1 | tail -3
$PY scripts/run_network_194_parallel.py --selftest 2>&1 | tail -2

# ── 2. 봉인 대조 (194 전체 · --dry-run = 아무것도 안 쓴다) — §3 · §2 표와 같아야 ──
$PY scripts/run_network_194_parallel.py run --root ~/net194_g2_drycheck_$T --dry-run 2>&1 | grep -E "코드 |기대 망 세대|전이 의존|지연 import|입력 지문|원자료 · 메시 문제|⛔"
# ⚠ 10-14 정정 (SUPR-02 · 1저자 Q2 (가) · 결과 0 건) — 위 줄 = 원문.  grep 화면은 사전 점검 증거가 아니다 · 관측 플래그 없는 생산 194 dry-run 은 §3b (10-09 비준) 뒤 사전 점검 ⛔ (rc 2).
#   사전 점검 증거 = §4 의 10-14 정정 블록 (--observe-imports --preflight-receipt → preflight-verify --expect-set production194) 과 같은 꼴로 받는다.

# ── 3. 실덤프 — 생산 → 후보 검사 → 게시 (real14 · case15 · LHS 셋 · 망 정지 · 격리 ROOT) ──
SM=~/g2pre_smoke_${S}_$T
$PY scripts/wsl_network_smoke.py --root "$SM" --skip-real14-general --lhs-case lhs00_055 --lhs-case lhs00_128 --lhs-case lhsx_007 2>&1 | tail -40; echo "smoke rc=${PIPESTATUS[0]}"

# ── 4. 게시 다시 읽기 (증서 · 도장 · 진단 상태 · 열 역할 · 인계 출처 관문) ──
$PY scripts/g2_network_reread.py --smoke-root "$SM" --json "$SM/reread.json" 2>&1 | tail -25; echo "reread rc=${PIPESTATUS[0]}"

# ── 5. 새 러너 시범 — LHS 셋을 실제 194 실행기로 (발사 봉인 · 기대 세대 · merge · 감사 · 인계 출처 관문) ──
PL=~/g2pre_pilot_${S}_$T
$PY scripts/run_network_194_parallel.py run --root "$PL" -j 3 --observe-imports --case lhs00_055 --case lhs00_128 --case lhsx_007 2>&1 | tail -20; echo "pilot rc=${PIPESTATUS[0]}"
$PY scripts/run_network_194_parallel.py audit --root "$PL" --tsv "$PL/seal_audit.tsv" --json "$PL/seal_audit.json" 2>&1 | grep -v '^  lhs' | tail -12; echo "audit rc=${PIPESTATUS[0]}"
$PY scripts/g2_network_reread.py --launcher-root "$PL" --expect-set pilot3 --json "$PL/reread.json" 2>&1 | tail -14; echo "reread rc=${PIPESTATUS[0]}"
grep -oE '"(expected_network_generation|launch_format)": "[^"]*"' "$PL/manifest.json" | sort | uniq -c

# ── 6. 묶음 (보고서 · 판정 JSON 만 — 케이스 결과 원본은 빼고) ──
cd ~ && tar czf ~/g2pre_${S}_$T.tar.gz "$(basename "$SM")/smoke_report.json" "$(basename "$SM")/smoke_summary.txt" "$(basename "$SM")/reread.json" \
  "$(basename "$PL")/manifest.json" "$(basename "$PL")/seal_audit.tsv" "$(basename "$PL")/seal_audit.json" "$(basename "$PL")/reread.json" \
  "$(basename "$PL")/merged/merge_report.json" "$(basename "$PL")/progress.tsv" && cp ~/g2pre_${S}_$T.tar.gz "$DL/" && ls -la ~/g2pre_${S}_$T.tar.gz
```

**붙여 넣을 것** — 0 단계 세 줄 (커밋 · dirty 줄 수 · 버전) · 1 단계 끝줄 둘 · 2 단계 grep 줄 · 3 · 4 · 5 단계 화면 끝과 `rc=` 줄 · 묶음 파일 (다운로드 폴더) 첨부.

**기대 (결과 전 등록 — 다르면 그대로 보고 · 고르지 않는다)**

| 단계 | 기대 |
|---|---|
| 1 | `g2_network_reread` ✓ 전부 통과 · 실행기 ✓ 전부 통과 (10-07 재등록 컨테이너 실측 15/15 · 82/82 — 실행기 selftest 는 실제 파이프라인 import 관측 ㉟d · ㉟e 를 돌려 ~1.5 분) · ★ G2RR3 수정 (`3f9f86f59` · `66c09ef68`) 뒤 컨테이너 실측 = **17/17 · 100/100** (10-07 · 이 숫자가 기대값 — 15/15 · 82/82 는 역사) |
| 2 | 코드 줄의 `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71 (CODE_FILES 32)` (10-07 재등록 — 앞 판 `b313e61a…` · `f3f54951…` (29) 는 역사) · 기대 망 세대 `'g2'` · 세대 계약 문제 0 · 모드 `['hertz', 'physics', 'hertz_h12']` · 전이 의존 닫힘 30 ⊆ 32 ✓ · 지연 import 분류 90 · 분류 밖 0 ✓ · 입력 지문 케이스 194 · `ids_sha256 a04282d7…` · `raw_sha256_table_sha256 da7c93f9…` (§2) · 원자료 sha 결손 0 · 원자료 · 메시 문제 0 건 · ⛔ 줄 없음 |
| 3 | `smoke rc=0` — A: real14_network · case15_network = done · 원자료 sha256 = README 표 · 망 정지 계약 통과 · run id 일치 / B: lhs00_055 · lhsx_007 = 두 모드 computed · τ ≠ NOT_COMPUTED · lhs00_128 = 두 모드 valid_zero · τ NOT_PERCOLATING / C: 음성 대조 넷 PASS (RGLR2 수정 뒤 동작 · §9-1 컨테이너 스모크 selftest 의 C 판정 참조) |
| 4 | `reread rc=0` — 다섯 케이스 세대 `'g2'` · K1–K7 · H1 ✓ / **real14 · case15**: τ 세 모드 = OK 또는 등록된 과학적 HOLD (NOT_COMPUTED · NOT_PERCOLATING 아님) · physics 협착-only = `not_computed` (`zero_resistance_requires_contraction` — Codex 직접 풀이: 관통 Rc=0 간선 real14 2,628 · case15 312) · hertz · hertz_h12 협착-only 와 세 모드 CF = 숫자 (증서 결합 통과 — Codex 직접 풀이에서 H0 · H12 clamp · floor 0) / **lhs00_128**: τ 세 모드 NOT_PERCOLATING · 모드 셋 × 가지 셋 valid_zero (숫자 없음 · 증서가 해를 주장하지 않음) / **lhs00_055 · lhsx_007**: 협착-only · CF 상태는 미리 정하지 않는다 (physics · H12 의 R_c = 0 간선 수 · CF `model_over_conduction` 여부는 침대마다 — 화면 그대로 보고) |
| 4 참고 | σ_ratio (화면 `σ_ratio`) 참고값 = Codex 직접 build/solve (`docs/reviews/codex_gen2_network_reverify_evidence_20261006/probes/real_beds.py`) 의 8 자리 반올림 — real14 hertz 0.02102106 · physics 0.03164009 · hertz_h12 0.02494138 / case15 0.00032635 · 0.00036225 · 0.00034587.  **판정 기준 아님** (파이프라인 = 덱 상자 · 메시 판 높이 · 같은 c_cpl[22] · c_cpl[23] — 다르면 그대로 보고) |
| 5 | `pilot rc=0` (세 케이스 done · merge rc 0) · `audit rc=0` (실행 형식 자격 current · SEALED 3 · 레코드 세대 `{'g2': 3}` · 입력 지문 = 발사 기록 ✓ · 실제 import 관측 = 리포 모듈 ⊆ 봉인 CODE_FILES 32 ✓ · ★ G2RR3-02 뒤: 같은 줄에 프로세스 수 (시작 = 끝맺음) · 완료 시도 3 (역할 워커/망 풀이) · `✗ 관측:` 줄 없음) · `reread rc=0` (M0 `'g2'` · M-plan · M-reg · M1 · M2 · M3 기대 3 = 읽음 3 · 같음 · H1 lhs · lhsx ✓ · 세 케이스 K1–K7 ✓ · JSON `expected_set` `pilot3` · `set_equal` true · ★ G2RR3-01 뒤 JSON v3 = `launcher_root` · `manifest_sha256` · `seal_fp` (= `e8b2496b…`) · `launch_sha`) · manifest 줄 넷 = `"expected_network_generation": "g2"` 2 (값 · 봉인 사본) · `"launch_format": "network_parallel_launch/v3"` 2 (값 · 봉인 사본) |

## 2. 대상 · 입력 봉인 (판정 §7-3 "194 ID · cohort · 원 dump 의 해시")

- `lhs` 130 · `lhsx` 64 — 10-05 등록 §1 과 같은 수확 · 코호트 (`docs/data/lhs_descriptors_cov_1e09f661d/` · `docs/data/lhsx_descriptors_cov_1e09f661d/` ·
  `docs/data/area_s2_cohort.tsv` · `docs/data/lhsx_descriptors_20260925/_cohort.tsv`) · 같은 프레임 관문 · 09-17 23:59 KST cutoff 무변경 · 새 코호트 없음.
- 원 dump 해시 = 수확 JSON 의 `raw.{atom,contact,mesh,deck}.sha256` (워커 `lhs_webapp_batch` 의 같은 프레임 관문이 실제 파일과 대조 — 다르면 그 케이스 REFUSED).
  ★ 이번 실행기는 그 지문을 manifest `input_digest` 에 쓰고 `audit` 가 다시 계산해 대조한다 (`plan_input_digest`):

| 항목 | 값 (이 커밋에서 계산 · 실행기 dry-run 이 같은 값을 찍어야) |
|---|---|
| 케이스 수 | 194 (lhs 130 · lhsx 64 · 원자료 sha 결손 0) |
| `ids_sha256` ('case\tcohort' 줄 · (코호트, 케이스) 순) | `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` |
| `raw_sha256_table_sha256` ('case\tcohort\tatom\tcontact\tmesh\tdeck' 줄) | `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` |
| 코호트 TSV sha256 | lhs `32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809` · lhsx `0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45` |

## 3. 코드 신원 (봉인)

- ★★ **10-07 재등록 (G2RR2-03 · 판정문 §4)** — 봉인 29 → **32 파일**: + `scripts/fracture_model.py` (`dem_analysis_core` 의 지연 import — 파괴 모델 상수 ·
  Codex dependency_gap: 그 사본의 K_IC 0.3 → 30 이면 multicrack 100 → 0 인데 옛 29 파일 봉인은 통과) · + `scripts/lhs_union_webapp.py` (`dem_analysis_core` 지연 import —
  τ 의 L_mc · φ_mc 를 내는 정확 union · 우리가 같은 부류로 찾음) · + `scripts/ml_design_structure.py` (`structure_predictor` 모듈 수준 `_restricted()` 안의 import —
  app 을 읽을 때마다 돈다 · 실제 import 관측이 찾음).  바뀐 봉인 파일 둘 = `scripts/tau_flux.py` · `webapp/pipeline_service.py` (G2RR2-04 · 05 `5dde71dcc`).
  ⇒ **`e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`** (10-07 재등록 지문 — ✅ 10-21 · 비준 뒤 역사 · 활성 = 이 절 끝 ✅ 줄 · 기계 구문 `code_fp` 를 떼었다 · §9-9) (런처 `code_fp(code_hashes())` · 이 컨테이너 194 dry-run 이 같은 값).
  정적 닫힘 30 ⊆ 32 (닫힘 밖 둘 = S3 수치 모듈 그대로) · 지연 import 분류 (`lazy_import_census`) 90 · 분류 밖 0 (경로 밖 사유 `DEP_LAZY_OFFPATH` 21) ·
  실제 import 관측 (selftest ㉟d — 합성 se_am 을 실제 `run_pipeline(stop_after='network')` 로 · 단계 하위 프로세스 포함) 리포 모듈 22 ⊆ 32.
  ⚠ 관측 22 는 합성 침대의 표준 경로다 — 실침대 경로는 §1 시범의 `--observe-imports` 가 본다 · 리터럴이 아닌 동적 import 는 정적 분류가 못 본다 (관측이 메운다).
- ⚠ **10-07 05:2x 갱신** — 요청서 핀 `2802c649e` 뒤 `webapp/app.py` 가 한 번 더 바뀌었다 (atom + 판 메시만 올린 케이스의 porosity — atoms-only 경로만 · 망 정지 경로 · 생산 · 게시 · 인계 코드 무변경 · 시험 `webapp/test_atoms_only_porosity.py` 41/41 · `test_pipeline_provenance` 284/284) ⇒ 봉인 지문 `f3f54951…` → `b313e61ab551…` (아래 값 갱신 · 런처 `code_fp(code_hashes())` 로 다시 계산 · 29 파일 중 `webapp/app.py` 한 줄만 바뀜).  발사는 이 지문의 커밋으로.

- 발사 커밋 = 아래 **32 파일** sha256 (= 봉인 지문 `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` · 10-07 재등록 — 앞 판의 29 파일 `b313e61a…` 는 역사 · ⚠ ✅ 10-21 · 비준 뒤 = 이 절 끝 ✅ 줄의 32 파일 · 지문) 과 같은 코드를 담은 커밋 — 이 문서를 담은 커밋 또는
  그 뒤 **문서 · 원장만** 바뀐 커밋.  1저자가 발사 직후 §9 에 `git rev-parse HEAD` · manifest `seal.code_fp` · `expected_network_generation` 을 적는다 (지문이 이 값과 다르면 이 봉인의 배치가 아니다 ·
  추적 파일이 바뀐 트리는 실행기가 거부한다).
- ★ 전이 의존 (판정 §7-3): 10-05 판 19 파일에 **워커의 망 정지 경로가 실제로 import 하는 리포 모듈 10** 을 더해 29 (`CODE_FILES`).  정적 닫힘 (`code_dependency_closure` — 시작점 =
  워커 + 단계 하위 프로세스 스크립트 (parse · 접촉 분석 둘 · 피복 · 망 CLI) · 모듈 수준 import + 경로 위 지연 import (lhs_webapp_batch → app · type_map_resolve · export_master_csv /
  pipeline_service → tau_flux / tau_flux → network_conductivity)) = 27 모듈 ⊆ 29 · 발사 사전 점검이 매번 확인한다 (새 import 가 생기면 발사하지 않는다).  29 중 닫힘 밖 둘
  (`audit_constriction_deleted.py` · `extract_se_network_diagnostics.py`) = S3 수치 모듈 목록 (`seal_s3_prerun.NUMERIC_MODULES`) 이라 10-05 판부터 봉인 — 그대로 둔다.
- ⚠ 새로 봉인한 것 중 **`scripts/lens_geometry.py` 는 σ 에 닿는다** — `plastic_coverage.py:1144` 가 모듈 수준에서 `intersection_disc_area` 를 import 하고 physics g2 면적의 원판 floor 가 그 함수다.
  10-05 판 19 파일 봉인에는 없었다 (그 파일은 10-05 봉인 커밋 `11fcf91e8` 뒤 바뀌지 않았다 — v1.2 값에는 영향 없음 · 봉인 정의의 구멍).

| 파일 | sha256 | 10-05 봉인 대비 |
|---|---|---|
| `scripts/network_conductivity.py` | `da9ecfefd8dc4b84e222140e347e4a718381169f27c88bf56c71ec4a7c2749be` | 바뀜 (`f3f720985` 포함 — sha256 `61f00fef…` → `da9ecfef…` 는 그 커밋 메시지) · **비준 뒤 = §3 끝 ✅ 줄** |
| `scripts/plastic_coverage.py` | `cce27a34c0bf2e4f5c122e43d983aa3414a825ab461a00abd408dba02e151348` | 바뀜 |
| `scripts/audit_constriction_deleted.py` | `180287be199ea60e6a50ba6cd0baf854c18a18568c476f7e0200c2caca3faf9d` | 바뀜 |
| `scripts/extract_se_network_diagnostics.py` | `db7151b51252e60c42c2bc2a2b3173ae6f4b97a94226b51a97b1e357e028ea9a` | 같음 |
| `scripts/dem_analysis_core.py` | `39fb19cb7eb962f11fe88546fa0ad93c4a9074846be13d15b27c2eae44fb620f` | 같음 |
| `scripts/analyze_contacts.py` | `a383ada7aef3d13ba08bd84728a20b6207f9b124a01ce3852c01ae2518ca1aa9` | 같음 |
| `scripts/analyze_contacts_bimodal.py` | `8afcc76030b747d8632014fa5b6cae1c1f066007b9247902caefb05288cf1ca5` | 같음 |
| `scripts/coverage_physics_vs_hertzian.py` | `1bf4ee8c0061e69760596b05318e0b750605e85ad16f34176e74f31db80b6253` | 바뀜 (`69c2adec9` — C2-⑥ 합집합 cap 피복 · LHS-27) |
| `scripts/parse_liggghts.py` | `4fe3f1f32ebc4168978c7278b7a1d37b072d64fbf00e97d0933351337d223425` | 같음 |
| `scripts/se_material.py` | `767a6a383d4581274b07ee79146a53fbe118f1f6eb0acb9ec0a5af21c9c9930c` | 같음 |
| `scripts/metrics_json.py` | `baa671f895dd6103cf95c25647ee45877d98306f00ab15cd3968fbe4354a7702` | 같음 |
| `scripts/tau_flux.py` | `eb9388ec8bd2d40b1c63365ae72b6850e9fc51fd9ce0780df4e557424a1440fb` | 바뀜 (10-07 재등록: + G2RR2-04 · 05 `5dde71dcc` — 앞 판 `6bc4037c…` 대비도 바뀜) · **비준 뒤 = §3 끝 ✅ 줄** |
| `scripts/lhs_webapp_batch.py` | `b9d0199cc1bd23cd1ed5405a283081c2c3a31bc6ce256670c8a9b63d177b5668` | 같음 |
| `scripts/lhs_harvest_batch.py` | `4d798c631ac893ca32018fde58145bc5c8a2e3e2a6423da61cb87bd13599148e` | 같음 |
| `scripts/lhs_descriptor_harvest.py` | `96fa643e309aab46b2a5cbd59e2276ee16b99107a9a7514e5d9fdcaf5c2d8d9e` | 바뀜 (`cc4210080` — LHSC-08 · 분류 불변) |
| `webapp/app.py` | `bd4c25e507e3c7a2b8e35f9b4602f22ab17d8e56fb6f8980021d33323994826b` | 바뀜 (G2RR-01 `e1dab4265` · G2RR-02 `f3f720985` · 3D 뷰어 라우트 `761e32645` · `92839aeb7` 포함) · **비준 뒤 = §3 끝 ✅ 줄** |
| `webapp/pipeline_service.py` | `33a700300e8c650ca953e96b7faaea3010245b63e6d2035d4b73b4a61e1c7843` | 바뀜 (G2RR-01 `e1dab4265` · G2RR-02 `f3f720985` 포함 · 10-07 재등록: + G2RR2-04 `5dde71dcc` — 앞 판 `2414fb21…` 대비도 바뀜) · **비준 뒤 = §3 끝 ✅ 줄** |
| `scripts/export_master_csv.py` | `2899dc2410ad8840dadf41993511c225d60f29f77edfdb2fac6703b25ccf767b` | 같음 |
| `scripts/type_map_resolve.py` | `4a289c6412e4b8e1bc0fba573cb287966dfa00a053399097b587f1e14726bfe5` | 같음 |
| `scripts/lens_geometry.py` | `891ac67f8b6c1b4c7978b5e806800ae74f5c8791928d6ece19a29e5f3b212b77` | 새로 봉인 (σ — 위 ⚠) |
| `scripts/lhs_perc_extract.py` | `0750d0964d006e64934e42e83b98fe0786115440f024fc5215d5d2aaf6396a16` | 새로 봉인 (lhs_descriptor_harvest 모듈 수준) |
| `scripts/press_units.py` | `493fcc42f2ed4b880362c81766004cf96d0f3a3ed8514aeff9cfe6ed387842dd` | 새로 봉인 (app 모듈 수준 · 목표 압력 단위) |
| `scripts/grade_engine.py` | `9a4d27ea9e937298ab84c0cf1bcd4c4f4957317e783247fd047923758dc96efc` | 새로 봉인 (predictor_engine 모듈 수준) |
| `webapp/ledger_view.py` | `ce445f36e01258fb2d46cc8c384b50c7545f87a97e5c1eb4785a0db64a8a7930` | 새로 봉인 (app 모듈 수준) |
| `webapp/mpm_lab_register.py` | `3b8318fb3980f1466ad2bb642f61924de3fb4d55c539690691cc86540f490967` | 새로 봉인 (app 모듈 수준) |
| `webapp/predictor_engine.py` | `9b341d4e1bf74e071888213656afb8dde4de985081d704818ba5d6b629555c2d` | 새로 봉인 (app 모듈 수준) |
| `webapp/security.py` | `6f9e98d8748bdd420e73f1db19df50ede1c5f9ce7fb60a25cdea582583de770f` | 새로 봉인 (app 모듈 수준) |
| `webapp/storage_sync.py` | `352314ffb1908998f51c1ec25289846b3644e736d2d8df5e145c41646edf811a` | 새로 봉인 (app 모듈 수준) |
| `webapp/structure_predictor.py` | `e468d6dfe18db338a6d6afc7ec10fb867464b80a02d17d475ee4ee8068392064` | 새로 봉인 (app 모듈 수준) |
| `scripts/fracture_model.py` | `3cd8dabb3ebaea3950f53951f776fceabc82f9431633587fc7bd85a8dd9d8170` | 새로 봉인 (10-07 재등록 · G2RR2-03 — dem_analysis_core 지연 import · 파괴 상수) |
| `scripts/lhs_union_webapp.py` | `3f06e9d36060a366d79e1abb76b5fe07e23b51d63666f51ba3afeabf64211408` | 새로 봉인 (10-07 재등록 · G2RR2-03 — dem_analysis_core 지연 import · τ 의 L_mc · φ_mc) |
| `scripts/ml_design_structure.py` | `35378c5eedae36a75074279066db1db81617c02c334b5d0e4c7f19a76d0bf628` | 새로 봉인 (10-07 재등록 · G2RR2-03 — structure_predictor 모듈 수준 `_restricted()` 안 · 실제 import 관측이 찾음) |

- 10-05 봉인 19 중 같음 11 · 바뀜 8 · 새로 봉인 10 (10-07 재등록: 새로 봉인 13 = 32 파일).  바뀐 8 파일을 건드린 커밋 (`11fcf91e8` 뒤 · 이 커밋에서 셈) = `50de4e806` · `a0a24c538` · `69c2adec9` · `5c2669538` · `05c60ae2d` ·
  `05977e94a` · `5627a74a6` · `e1dab4265` · `f3f720985` · `761e32645` · `92839aeb7` · `cc4210080` (파일별 귀속은 파일마다 git log 로 — 표에는 확인한 것만 적었다).  ⚠ `webapp/app.py` 는 망과 무관한 화면 라우트만 바꿔도 지문이 바뀐다 — 발사 뒤 그 체크아웃에서 app.py 를 고치지 않는다 (retry 가 거부한다).
- ★ 기대 망 세대 (G2RR-01 · 판정 §2 "새 배치 manifest 의 기대 세대와도 교차 대조"): manifest `expected_network_generation` (+ `seal` 안 사본) = 실행기가 **봉인 코드에서 유도한 값**
  (`derive_generation` — 생산자 `network_conductivity._run_all_networks` 를 망 CLI 와 같은 기본값 (hertzian · physics) 으로 21 구 사슬에 한 번 → 같은 체크아웃의 `tau_flux.network_generation_contract`).
  이 커밋의 유도값 = `'g2'` · 계약 문제 0 · 모드 hertz · physics · hertz_h12.  세대 2 · 문제 0 이 아니면 실행기가 발사하지 않는다 (현행 게시는 세대 2 만 받는다).
  retry = 값 ≠ 봉인 사본 · 워커 체크아웃 코드로 다시 유도한 세대 ≠ 값이면 rc 2 (넘김 불가) · audit = 같은 대조 + done · partial 케이스마다 레코드 세대 = 선언 · 인계 생성기
  `--tau-batch-manifest <ROOT>/manifest.json` = 케이스마다 레코드 세대 = 선언 (없으면 거부).
- 인계 단계 코드 (워커가 돌리지 않는다 — 봉인 판정 밖 · manifest `handover_code_hashes` 에 기록 · 후속 명령이 대조): `scripts/lhs_design_dataset.py`
  `a678994861a179a2c694c4dc093fc67a3a0fa64a90bd99a1eb236417a8a2af7a` · `scripts/g2_network_reread.py` — 이 커밋의 바이트 (값은 §9 에 manifest 에서 옮긴다).
  10-07 재등록: `scripts/lhs_design_dataset.py` `27c9c1a8a680945c5ba60e6717e1d77438a489549a62eb24bddb65223c0a8b29` (`5dde71dcc` — selftest 기대 표지 한 줄 · 값 경로 무변경) ·
  `scripts/g2_network_reread.py` `23a949dfe6aa09d277e0626c2c3a6db3e199de8a42872b375b4e75ae828c467b` (`5dde71dcc` K7 · `17ba65f4e` 등록 집합).
  ⚠ v1.3 의 새 열 · 표 (CLAUDE.md 10-06 밤 목록 — ML 표 · f 타깃 안내 · 재적합 · τ 표시 이름 · `se_isolated_pct`) 가 생성기를 바꾸면 이 지문이 바뀐다 → 그 커밋을 §9 에 적는다.
- ✅ **활성 봉인 (10-21 · 1저자 비준 · §9-8 L214 개정 · 결과 열람 뒤 정책 개정 = 10-14 실행 결과를 본 뒤 · 변경 이력 §9-9)** — 봉인 32 (목록 그대로) · **`code_fp 2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3e`** (실행기 `code_fp(code_hashes())`) = 위 표 28 행 그대로 + 바뀐 4 행:
  `scripts/network_conductivity.py` `a525e2db98fd044f0aa9353b028a3d5c7164c006a8e870dda24e7a0991d9751e` · `scripts/tau_flux.py` `c0a7da6e1b73bea97136f06803810dbe159bf5c4395d8d218a90217a58ef0f78` ·
  `webapp/app.py` `3e82140f47c7e87b138f8a6f24b8f8575bc7476e91b8369b20cdf698b69b4bc1` · `webapp/pipeline_service.py` `8026169f61e8bddcceea3dfb42758bb6a4e599a28271d8159c387dfc2a79d4ef`.
  인계 도구 (HANDOVER_FILES · 봉인 판정 밖 · 발사 manifest `handover_code_hashes` 에 기록) `scripts/lhs_design_dataset.py` `d1815155142e909200053c2d8e9de8c0a88c2dc6d3d9462ad18614a42845e1f0` · `scripts/g2_network_reread.py` `0e2ec7ef37571268b85b0d17b71f7a2858aa2a7e6bcfadf4be1c6b5416dd5cd8` ·
  배포 빌더 `scripts/lhs_release_build.py` `3096e33fd0f1953363bcde251a77368366a0568c923447111a48a873ad4a1383` (빌드 manifest `code` 칸).
  발사 커밋 = B7 승인 핀 (이 비준 문안이 들어간 push 된 본 가지 커밋 · 1저자가 고른 한 SHA · §9-8 ⑦) — 그 체크아웃의 194 dry-run 이 같은 code_fp 를 찍어야.  10-07 재등록 지문 `e8b2496b…` · 위 표 4 행의 옛 값 = 역사 (§9-9).
  사전 점검 화면 기대 (이 지문의 코드 · 결과 전): 기대 망 세대 `g2` · 계약 문제 0 · 모드 hertz · physics · hertz_h12 · 전이 닫힘 30 ⊆ 32 ✓ · 지연 import 분류 92 · 분류 밖 0 ✓ (10-07 의 90 + `webapp/pipeline_service.py` 의 `channel_verdict` · `_stop_num` 안 `tau_flux` import 둘 — 대상 = 봉인 파일) · fork 0 줄 ✓ · 입력 지문 = §2 표 그대로.

## 3b. 실행 형식 v3 (10-07 재등록 · G2RR2-01 · 02 · 판정문 §2 · §3)

- 새 실행 (`run`) 의 manifest = `launch_format: network_parallel_launch/v3` · `seal.schema: launch_seal/v3`.  필수 선언 = 기대 망 세대 (`expected_network_generation` =
  봉인 사본 = `'g2'` · `generation_probe`) · `input_digest` (n · `ids_sha256` = 계획 큐에서 다시 계산 · 원자료 표 지문 · 결손 0 · 코호트 TSV 지문) · `code_hashes` = CODE_FILES ·
  봉인 지문 · 전이 닫힘 · 인계 코드 지문 · git sha · 계획 꼴.  하나라도 없거나 null 이면 실행 형식 자격 invalid — run (쓰기 전 자기 대조) · retry · audit · merge 가
  같은 함수 (`launch_eligibility`) 로 거부한다.  지운 선언을 옛 형식으로 추론하지 않는다.
- 역사 형식 = `HISTORICAL_LAUNCHES` 등록 (10-05 net194 · `11fcf91e8` · 19 파일 `3bc0a116…` · 키 집합 · 봉인 없음) 과 정확히 같을 때만 — `audit --historical` ·
  `merge --historical` 에서만 읽는다 · retry 는 거부.  ⚠ 같은 JSON 안의 사본끼리 대조는 누락 검사이지 독립 증거가 아니다 (판정문 §2 의 한정 그대로).
- 다시 읽기 (`g2_network_reread --launcher-root`) = 등록 집합 필수 — `--expect-set production194` (ids_sha256 `a04282d7…` · lhs 130 · lhsx 64 · 커밋된 수확 폴더에서 열거해
  지문 대조) · `pilot3` (lhs00_055 · lhs00_128 · lhsx_007) · 또는 `--expect-case 코호트:케이스`.  루프 전 계획 꼴 · 루프 밖 집합 대조 · 판정 JSON v2 (`expected_set` ·
  `expected_n` · `read_n` · `set_equal` · `missing` · `extra`).  v1.3 생성기는 production194 전부 (기대 = 읽음 = 194 · 같음) 인 기록만 받는다 (G2RR2-02).
- 시범 import 관측 (`run --observe-imports`) — 워커 · 단계 하위 프로세스가 읽은 리포 모듈을 남기고 audit 가 봉인 ⊇ 관측을 본다 (값에 닿지 않는다).
  §1 시범에서 켠다 — 194 본 실행에서 켤지는 발사 승인 때 1저자가 정한다.
  > ✅ **10-09 1저자 비준 (§9-6)** · ⬜ **제안 (10-07 · Codex 재검증 4 `G2RR4-03` · 1저자 비준 대기 — 등록 기대를 바꾼다 · 위 줄은 원문으로 둔다)**: 194 본 실행도 `--observe-imports` **필수**.
  > 실행기 (`36ba39070`) 가 생산 계획 (계획 큐 = 등록 production194) 을 관측 없이 띄우지 않는다 (사전 점검 ⛔ · `--dry-run` 에도 보인다) · 감사 = 관측을 끈 생산 manifest 를
  > 문제로 (rc 1) · v1.3 배포 관문 = 배치 manifest `observe_imports` true · 감사의 관측 객체 · 관측 내부 문제 0 · 실행 단계 ↔ 영수증 결합 기록 (`stage_binding` — G2RR4-01 ·
  > 02) 이 없으면 받지 않는다.  변경 이력 = §9-4.

## 4. 계산 · 발사 (Codex GO 뒤)

- 웹앱 `run_pipeline(stop_after='network')` = 접촉 → 피복 → 망 솔버 (세 모드 · 세 가지 · 증서) → 망 정지 계약 ①–⑨ (세대 계약 · 증서 결합 · 기술 검사) → 게시 · 도장.
- 실행기 = 10-05 와 같은 구조 — 케이스마다 `lhs_webapp_batch.py --stop-after network --case <c>` 한 번 · 동적 큐 (접촉 수 큰 순) · 레인 기본 20 × 1 스레드 · 케이스별 TMPDIR (망 lock) ·
  메모리 예산 입장 관문 · 산출 `merged/{lhs,lhsx}/`.  10-05 WSL 실측: 194 건 22:13–22:49 KST (36 분 · run 한 번 · retry 0).

```bash
cd ~/dem-audit && git fetch origin claude/stoic-knuth-NObVQ && git checkout --detach <발사 커밋>
PY=$(ls ~/Yonghoon-DEM-DFT/venv/bin/python ~/Yonghoon-DEM-DFT/.venv/bin/python3 2>/dev/null | head -1); R=~/net194_$(git rev-parse --short HEAD)
$PY scripts/run_network_194_parallel.py run --root "$R" --dry-run 2>&1 | grep -E "코드 |기대 망 세대|전이 의존|지연 import|입력 지문|원자료 · 메시 문제|⛔"   # §2 · §3 값과 같아야
$PY scripts/run_network_194_parallel.py run --root "$R" 2>&1 | tee ~/net194_run_$(date +%m%d_%H%M).log | tail -40
```

> ✅ **10-09 1저자 비준 (§9-6)** · ⬜ **제안 — 본 실행 명령 · manifest 확인 (10-07 · `G2RR4-03` · Codex 재검증 4 §4 Q3 · §7-3 · 1저자 비준 대기 · 위 블록은 원문으로 둔다)**.  고친 실행기는 위 둘째 줄
> (관측 플래그 없음) 을 생산 194 에서 사전 점검 ⛔ 로 거부한다.
>
> ```bash
> $PY scripts/run_network_194_parallel.py run --root "$R" --dry-run --observe-imports 2>&1 | grep -E "코드 |기대 망 세대|전이 의존|지연 import|fork|입력 지문|원자료 · 메시 문제|⛔"   # ⛔ 줄 없음 · fork 0 줄 ✓
> $PY scripts/run_network_194_parallel.py run --root "$R" --observe-imports 2>&1 | tee ~/net194_run_$(date +%m%d_%H%M).log | tail -40
> # 시작 직후 (manifest 가 생기면 · 다른 터미널) 와 완료 뒤 두 번 — 관측 표지 · 실행 신원 (각 1 줄 · 값 true · 32 hex)
> grep -oE '"observe_imports": (true|false)' "$R/manifest.json"; grep -oE '"import_obs_run_id": "[0-9a-f]{32}"' "$R/manifest.json"
> # 완료 뒤 — 감사의 관측 · 단계 결합 (기대: audit rc 0 · 시작 = 끝맺음 · 완료 시도 194 · stage_binding 194 · 문제 [])
> $PY scripts/run_network_194_parallel.py audit --root "$R" --tsv "$R/seal_audit.tsv" --json "$R/seal_audit.json" 2>&1 | grep -v '^  lhs' | tail -12; echo "audit rc=${PIPESTATUS[0]}"
> $PY -c "import json,sys; a=json.load(open(sys.argv[1])); o=a['import_observation']; print(o['n_started'], o['n_finalized'], len(o['completed_attempts']), o['stage_binding']['schema'], len(o['stage_binding']['attempts']), a['import_observation_problems'])" "$R/seal_audit.json"
> ```
>
> ✅ **10-14 정정 — 사전 점검 dry-run 줄 (SUPR-02 · 1저자 Q2 (가) · 결과 0 건 · Codex 보충 20 수정 재검증 `docs/reviews/codex_review_sup20_fix_reverify_20261014.md` §5 · 수정 계획
> `docs/reviews/supr_fix_plan_20261014.md` · 위 두 블록의 dry-run 줄은 원문으로 둔다)**.  grep 은 완료 줄 · 문맥을 버리고 셸 종료코드는 실행기 것이 아니다 → 사전 점검 증거 =
> 실행기 완료 영수증 (`--preflight-receipt` — JSON + 실행기가 직접 잡은 전체 로그 · 멈춰도 실제 종료코드 · 멈춘 사유와 함께).  위 제안 블록 첫 줄 대신 쓴다
> (본 실행 줄 · 관측 확인 · 완료 뒤 확인 · 기대 — §2 · §3 값 · ⛔ 없음 · fork 0 줄 — 는 그대로):
>
> ```bash
> PF="${R}_preflight_$(date +%m%d_%H%M%S).json"     # ROOT 밖 · 새 이름 — 같은 이름 .log = 실행기가 직접 잡은 화면 전체
> $PY scripts/run_network_194_parallel.py run --root "$R" --dry-run --observe-imports --preflight-receipt "$PF"; echo "dry-run rc=$?"
> $PY scripts/run_network_194_parallel.py preflight-verify --receipt "$PF" --expect-set production194 --approved-sha <발사 커밋> --json "${PF%.json}_verify.json"; echo "verify rc=$?"   # rc 0 = 칸 전부 같음 (발사 승인 아님)
> grep -E 'INPUT_DIGEST_JSON|코드 ' "${PF%.json}.log"     # 입력 지문 전부 (코호트별 TSV sha 포함) · 봉인 지문 — §2 · §3 표와 손으로 대조
> ```
>
> `preflight-verify` (읽기 전용 · P0–P10 · 실행기 `preflight_receipt_checks`) = 로그 sha256 · `INPUT_DIGEST_JSON` 한 줄 = 영수증 = 이 체크아웃 재계산 · 완료 · 실제 종료코드 0 · 관측 ON ·
> 필수 세 검사 명시 성공 · argv = 등록 명령 · 깨끗한 트리 · code_fp = 이 체크아웃 · 세대 g2 · 원자료 0 · 승인 SHA (`--approved-sha` · 1저자 Q3).  ⚠ 194 쪽에는 §2 표의 값
> (raw 표 `da7c93f9…` · 코호트 TSV lhs `32f00daa…` · lhsx `0b85e858…`) 을 문서에서 읽어 대조하는 칸이 없다 (보충 20 은 `scripts/supp20_input_receipt.py` E1 이 한다) —
> 위 셋째 줄의 로그 값을 §2 와 손으로 대조한다 (옛 grep 줄과 같은 수준 · ID 지문 `a04282d7…` 은 등록 집합 production194 로 기계 대조).  grep · tee 텍스트 로그 단독은 사전 점검
> 증거로 받지 않는다.
>
> ✅ **10-14 Codex 재확인 (핀 `df647d4e3` · `docs/reviews/codex_review_supr_fix_reverify_20261014.md` §3) — 손 대조 = 해제 조건으로 수용 · 1저자 10-14 = 이번 발사는 손 대조 기록 (자동 대조 = v1.3 뒤)**.
> `preflight-verify` rc 0 만으로 §2 일치를 주장하지 않는다 (반례: lhs TSV 끝 개행 하나 — 생성 · 검증이 같은 새 입력을 읽으면 P0–P10 통과 · 원래 입력으로 검증하면 P9 거부).
> 발사 전 기록 (최소) = 영수증 경로 · 로그 sha256 · 승인 핀 · §2 다섯 값 (n · `ids_sha256` · `raw_sha256_table_sha256` · `cohort_tsv_sha256.lhs` · `.lhsx`) 과 §3 code_fp 의 기대 · 실측 **전체 값** · 일치 · 확인자 —
> 그 영수증 = P0–P10 을 통과한 바로 그 실행 (짧은 접두 눈대조 · "P0–P10 통과" 로 대신하지 않는다).  실제 발사 = `--approved-sha <발사 커밋>` · `runner.sha256` = 기록 전용 (P0–P10 이 비교하지 않는다).
>
> ✅ **덧붙임 — 완료 뒤 기대의 재시도 예외 (10-09 1저자 비준 · `G2RR5-04` · Codex 재검증 5 §4 · 위 주석 · 명령은 원문으로 둔다)**.
> 위 주석의 *"시작 = 끝맺음 · 완료 시도 194 · stage_binding 194"* 는 **재시도 없는 1 회 실행**의 기대다.  합격선 = 판정문 §4 권고 문안 그대로:
> *"최종 등록 케이스 집합은 194이고 모두 요구 봉인을 만족한다. 완료 시도 전체의 키 집합과 단계 결합 키 집합이 같고, 각 시도의 expected=observed이다.
> 완료 시도의 미최종 영수증은 없어야 한다. 비완료 시도의 미최종 영수증은 Q2 규칙으로 따로 보고한다. 재시도 없는 경우에 한하여 전체 시작=끝맺음, 완료·결합 시도194를 기대한다."*
> 확인 명령 (합계 대신 — 기대는 줄 끝 주석):
>
> ```bash
> $PY - "$R/seal_audit.json" <<'PY'
> import json, sys
> a = json.load(open(sys.argv[1])); o = a['import_observation']; sb = o['stage_binding']['attempts']
> comp = {'|'.join(map(str, k)) for k in o['completed_attempts']}
> print('케이스', len(a['cases']), '판정', a['verdicts'])                                      # 케이스 194 · {'SEALED': 194}
> print('결합 = 완료 시도', set(sb) == comp, len(sb), len(comp))                               # True (재시도가 있으면 194 보다 클 수 있다)
> print('expected ≠ observed', [k for k, r in sb.items() if r.get('expected') != r.get('observed')][:5])   # []
> print('감사 문제', a['import_observation_problems'][:5])                                      # [] (완료 시도의 미최종 영수증도 여기 문제로 나온다)
> print('완료 아닌 시도의 미최종 영수증 (정보 · Q2)', len(o['unfinalized_noncompleted']))
> print('시작 · 끝맺음 (재시도 없으면 같다)', o['n_started'], o['n_finalized'])
> PY
> ```
>
> v1.3 배포 관문은 같은 내용을 시도마다 실행기 계약 함수로 다시 판정한다 (`G2RR5-01` · `scripts/lhs_release_build.py` `v13_audit_observation_problems`).

## 5. 판정 · 관문 (결과 전 등록)

> ✅ **10-21 · 1저자 비준 (§9-9)** — 이 절의 활성 개정 = §9-8 ①–⑦ (§5-1 모형 한계 = 레코드 게시 가능 · 결과 자격 ①–③ · 공란 의미 ④ · Hertz 주 타깃 ⑤ · 결과 보고 ⑥ · 발사 ⑦ · §5-7 허용 다름 더함) · 아래 원문 1–7 은 그대로 둔다 · 결과 열람 뒤 정책 개정 (10-14 실행 결과를 본 뒤).

1. 케이스마다 `done` / `failed` (+ `failure_kind`) — failed 는 빈칸 + 사유로 싣고 고르지 않는다 (재실행은 봉인 코드 그대로 `retry` 만).
2. `audit` rc 0 = 실행 형식 자격 current · 기록 전부 SEALED · 레코드 세대 전부 `g2` · 입력 지문 = 발사 기록.  rc 1 · 2 이면 인계하지 않는다.
3. `g2_network_reread.py --launcher-root <ROOT> --expect-set production194` rc 0 (M0 · M-plan · M-reg · M1 · M2 · M3 기대 194 = 읽음 194 · 같음 · 케이스마다 K1–K7 ·
   코호트마다 H1) — 판정 §7 끝 "전체 상태 · ID · 증서와 값의 다시 읽기" · 재검증 2 §3 (0 건 · 일부 코호트 PASS 배제).  rc 1 · 2 이면 인계하지 않는다.
4. τ 관문 (`tau_flux`) 진단 표 그대로 — 상태 표지 (NOT_PERCOLATING · NOT_COMPUTED · BAND_FALLBACK · MODEL_BELOW_CONTINUUM_BOUND) 유지.
5. 인계 생성기 관문 (⑤F1 · ⑥R1–R3 · ⑦A1–A5 · τ 출처 P0–P4 · `--tau-batch-manifest` 기대 세대 교차 대조).
6. 계약 상수 (판정 §7-3 "H0/Physics/H12 기대 조합 · 스키마 · 증서 문턱 · 실패 정책") 는 봉인 파일 안에 있다 — 코드 봉인이 고정하고 정지 계약 ⑨ (게시) · 인계 P4 · 다시 읽기 K2 가 같은 함수로 적용한다:
   모드별 모델 조합 = `tau_flux.G2_MODE_CONTRACT` (H0 = maxwell + cylinder_half_d · H12 = mikic_psi_multiply + sphere_segment · physics = mikic + physics_g2 · 셋 다 dirichlet_exact) ·
   증서 문턱 = `network_conductivity.DIRICHLET_CONSERVATION_REL_MAX = DIRICHLET_RESIDUAL_REL_MAX = 1e-6` · 풀이 사다리 (작은 망 spsolve → cg+jacobi → gmres+ilu · 큰 망 cg → spsolve ≤ 250k → cg+jacobi → gmres+ilu) ·
   증서 정책 = `tau_flux.CERT_BRANCH_POLICY` (FULL = 게시면 필수 · CF · 협착-only = 숫자를 실으면 필수 · 결합 · 통과 증서가 없거나 어긋나면 **레코드 전체 거부** — 1저자 결정 10-07 · 정직한 개별 풀이 실패는 그 가지만 NOT_COMPUTED) ·
   GEN2-01 = 협착-only 의 R_c = 0 간선 → 그 가지만 NOT_COMPUTED `zero_resistance_requires_contraction`.  실행기는 이 상수를 따로 다시 선언하지 않는다 (사본 금지 · 규율 ①).
7. 회귀 (v1.2 194 대비): 망 단계 밖 열 (접촉 · 퍼콜 · ⑤⑥⑦ · 피복 기하면적) 은 **같은 값** — 허용되는 다름은 선언된 변경뿐: 전극 정확 Dirichlet (H0 σ 상대 ≤ 1.5e-4 · 설계 기록 §1) ·
   physics = ψ 곱 + physics_g2 (physics 열 전부) · H12 새 열 · CF/협착-only `model_over_conduction` 값 유지 · GEN2-01 협착-only NOT_COMPUTED · 피복 합집합 cap 새 키 (C2-⑥) ·
   단일 스레드 BLAS 의 마지막 자리.  그 밖의 차이는 보고하고 원인을 밝힌 뒤에만 싣는다.

## 6. 인계 v1.3 (§5 통과 뒤 · 1저자 승인 뒤)

- 실행기 merge 가 찍는 후속 명령 (`print_followups`) 그대로 — 이번 판은 기대 세대가 선언된 manifest 이면 ⓪b 다시 읽기 (계획 = 등록 집합이면 `--expect-set production194` ·
  아니면 `--expect-case` 하나씩) · 생성기 `--tau-batch-manifest <ROOT>/manifest.json` · 이름 `_handover_v13_` 을 찍는다.
  ⚠ 찍힌 명령의 `python3` 는 배치 venv (`$PY`) 로 바꿔 쓴다 (10-06 기록: 시스템 python3 = numpy 없음).
- 다시 읽기 검산기 `reread_v12.py` 는 v1.2 전용 (C4 공통 칸 · C8 등록 큐 — G2RR-03 수정) — v1.3 용 검산은 별도 (이 등록 밖 · 자동 배포 관문 아님).

## 7. S3 · 알려진 부작용

- S3 봉인 = 별도 갱신 의무 (판정 §7-3): `network_conductivity.py` sha256 이 `61f00fef…` → `da9ecfef…` (`f3f720985`) · S3 의 `seal_s3_prerun.NUMERIC_MODULES` 넷에는
  `lens_geometry.py` 가 없다 (위 §3 ⚠ 와 같은 구멍) — S3 재봉인 때 넣을지 = 1저자.
  → **10-07 보완 (`2d247a66f` · 재검증 2 §10 *"넣을지 말지를 취향으로 남겨 둘 수 없다"* · 1저자 *"해결해놔"*)**: `NUMERIC_MODULES` 6 (+ `lens_geometry.py` · `se_material.py`) =
  소비자 (`run_s3_psi`) 수치 경로의 정적 닫힘 (`numeric_dependency_problems`) · 봉인 발행 · 소비 둘 다 대조 · 옛 네 모듈 봉인 = 소비 거부 · 실제 import 관측 (selftest ⑮d) 이
  경로 밖 주장을 확인.  코호트 cutoff · baseline 선별 · 봉인 창 무변경 — 새 S3 봉인은 창 (09-17 23:59 KST) 이 닫혀 저자 결정 없이는 못 낸다 ⇒ **S3 실행 = 별도 HOLD** (194 와 순서 독립 · 판정문 §10).
- 옛 ROOT (19 파일 봉인 · 기대 세대 선언 없음) 는 이 실행기로 retry 하면 봉인이 달라 거부된다 — 그 ROOT 의 커밋 실행기로.  감사 (`audit`) 는 그대로 읽는다 (세대 대조 없이 · 표지만).
  → 10-07 G2RR2-01 뒤: 옛 ROOT = 역사 형식 (§3b) — `audit --historical` · `merge --historical` 로만 읽는다 (기본 audit = rc 2 · retry = 거부).
- G2RR-02 이전 세대 2 웹앱 케이스 (`05977e94a` – `70a6d91a4` 코드로 계산) = 증서 결합 키가 없어 숫자 게시 가지에서 거부 → 망 재계산 전 τ NOT_COMPUTED (194 배치와 무관).

## 8. 이탈 기록

- (없음 — 발사 뒤 생기면 여기에)

## 9. 덧붙임 (결과 칸 · 1저자 · 발사 / 사전 점검 뒤)

- 9-1 컨테이너 (이 커밋 · 2026-10-07): 실행기 selftest 68/68 · `g2_network_reread --selftest` 9/9 · `wsl_network_smoke --selftest` 11/11 (커밋 뒤 깨끗한 트리 · 합성 침대 실제
  파이프라인 · 음성 대조 C1 · C1b · C2 · C3 = PASS · 참조 침대 두기 real14 · case15 sha256 = README) · 194 dry-run (이 컨테이너 · 원자료 없음 = `--allow-missing-raw`) 의 기대 세대 `'g2'` ·
  닫힘 27 ⊆ 29 ✓ 줄 확인 · 입력 지문 · code_fp = 같은 함수 (`plan_input_digest` · `code_fp`) 를 실제 194 계획에 불러 §2 · §3 값과 같음 확인.
- 9-1b 컨테이너 (10-07 재등록 · 코드 커밋 `5dde71dcc` · `3b2d1b91e` · `17ba65f4e` · `2d247a66f`): 실행기 selftest 82/82 · `g2_network_reread --selftest` 15/15 · `wsl_network_smoke --selftest` 11/11 (커밋 뒤 깨끗한 트리) · `test_lhs_release_v13` 80/80 · 194 dry-run (이 컨테이너 · `--allow-missing-raw` — 원자료 · 메시 문제 582 건 = 원덤프 없음 · WSL 기대 0) = `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` (CODE_FILES 32) · 기대 세대 `'g2'` · 계약 문제 0 · 모드 `['hertz', 'physics', 'hertz_h12']` · 닫힘 30 ⊆ 32 ✓ · 지연 import 90 · 분류 밖 0 ✓ · 입력 지문 194 · `a04282d7…` · `da7c93f9…` (§2 같음).  ⚠ WSL 원형 실행 아님.
- 9-2 사전 점검 (§1 · WSL · 10-07 14:15 KST · 1저자 · 코드 `c3117438a` · 증거 `docs/reviews/codex_gen2_network_reverify4_precheck_20261007/`): 단계 0 · 1 · 2 · 5 = **기대대로**
  (자체 시험 ✓ · 100/100 · `code_fp e8b2496b…` (32) · 'g2' · 입력 지문 194 · 시범 pilot · audit · reread rc 0 · SEALED 3 · 관측 영수증 시작 15 = 끝맺음 15 · 완료 시도 3 · 다시 읽기 JSON v3) ·
  **단계 3 · 4 = 기대와 다름 — `case15_network` failed** (smoke rc 1 · reread rc 1 = S0 · real14 σ_ratio = 참고값 8 자리 같음 · LHS 셋 · 음성 대조 넷 기대대로).  원인 (우리 컨테이너 재현 같음):
  전자 두 모드 · Hertz 열 = 띠 겹침 B∩T 4 노드 (`boundary_overlap` — 판 간격 19.1455 µm < 4 r_AM 24 µm) · Physics 열 = 덤프 면적 −0.186036 µm² 간선 거부 → WEB-03 Q1 게시 차단 ·
  이온 채널은 계산됨 (Codex 직접 풀이와 같음 · Physics 협착-only 312 간선 not_computed = 기대 그대로).  ⇒ **코드는 등록 계약대로 · 등록 기대 (case15 done) 가 틀렸다** (`SELF-92`).
  이 결과를 본 뒤 §1 기대 · 스모크 기대를 **고치지 않는다**.  194 도달 = 띠 겹침 0/194 · 음수 · 0 덤프 면적 0/194 (기록 · 증거 README §3) · 처리 = 재검증 4 요청서 §4 · Q6 (Codex) ·
  같이 등재 `GEN2-04` (면적 ≤ 0 처리 모드 비대칭) · `WEB-05` (시도 사유 끝 300 자) · ✅ 전체 출력 보충 묶음 (판정문 §8-4 · 1저자 · 증거 README §5 — 자체 시험 rc 0 · 100/100 · 영수증 15 = 15).
  ⚠ 정정 10-07 (`SELF-94` · Codex 재검증 4 §5): 보충 묶음이 채운 것 = 자체 시험 전문 둘 · 시범 3 워커 로그 · 영수증 · run 기록 — 전체 dry-run 원 stdout · 전체 스모크 stdout ·
  게시된 dual/full_metrics 원파일은 아니다 ("전체 출력" 으로 일반화하지 않는다 · 로그 포장만으로 수치 재실행은 요구되지 않았다) · ⚠ case15 음수 면적은 한 행이 아니라 **두 행**
  (31–29241 −0.186036 · 38–29241 −0.186264 µm² — Physics 는 첫 행에서 멈춘다 · 판정문 §6-1).
- 9-3 발사: 커밋 ⬜ · manifest `seal.code_fp` ⬜ · `expected_network_generation` ⬜ · `input_digest.raw_sha256_table_sha256` ⬜
- 9-4 **변경 이력 (10-07 · Codex 재검증 4 `docs/reviews/codex_review_gen2_network_reverify4_20261007.md` 뒤 · 결과 0 건 — 194 미실행)** — ✅ **10-09 1저자 비준 (§9-6)** · ⬜ **제안 · 1저자 비준 대기** (등록 기대를 바꾸는 항목):
  ① **본 실행 관측 필수** (`G2RR4-03` · 판정문 §4 Q3 · §7-3) — §3b · §4 제안 표지 그대로 (실행기 `36ba39070` 사전 점검 ⛔ · 감사 문제 · v1.3 배포 관문 필수 조건).
  ② **case15 = 음성 대조** (판정문 §6-3(b)) — 원 실패 기록 = §9-2 (10-07 14:15 · 고치지 않는다) · 변경 사유 = *"이온 단독 성공을 전체 채널 성공으로 잘못 예상했다"* (`SELF-92`).
     새 기대 (제안 · `scripts/wsl_network_smoke.py` `CASE15_NEGCTL` · 스모크 `case15_network` 의 `[음성 대조]` 검사 넷 — 지정한 실패가 **실제로 발화해야** PASS · whitelist · 이름 PASS 아님):
     이온 직접 풀이 = 두 모드 computed · σ_ratio 8 자리 0.00032635 (Hertz) · 0.00036225 (Physics) · 증서 보존 · 잔차 < 1e-6 / 전자 두 모드 · Hertz 열 = `boundary_overlap` ·
     B∩T = 입자 ID 24 · 40 · 57 · 103 / Physics 열 = 음수 원자료 면적 거부 (`ligg_area < 0` · 음수 행 둘) / 파이프라인 = 게시 차단 (failed · 실패 단계 = 망 솔버) · 반환 run id 없음
     (옛 성공 산출물 재사용 없음) · 인계 숫자 비노출 (τ 세 모드 NOT_COMPUTED · 숫자 칸 없음).  다시 읽기 (`--smoke-root`) = 음성 대조를 S0 에서 빼고 S0b (게시 없음 ∧
     스모크 `[음성 대조]` 판정 PASS) · 표지 없는 failed = S0 실패 그대로.  스모크 전체를 "기대대로 통과" 로 소급 수정하지 않는다 · 얇은 침대 띠 규칙 · 채널별 게시 =
     모형/계약 변경 → 이 194 와 분리 (판정문 §6-3(b)).
  ③ 다음 사전 점검 기대 (제안): §1 단계 3 smoke rc 0 (case15 음성 대조 PASS · 나머지 그대로) · 단계 4 reread rc 0 (S0 · S0b) · 단계 5 audit = 고친 실행기 (`4c8f84928`) 의
     단계 결합 — 옛 실행기 시범 ROOT 는 시도에 stage_plan 이 없어 지금 케이스 기록 (out/status.json stages) 으로 결합 (WSL 에서 다시 확인 ⬜) · 다시 읽기 = 상세 계약 (`942e851fd`).
  ④ 코드 신원: G2RR4-01 `942e851fd` · G2RR4-02 `4c8f84928` · G2RR4-03 `36ba39070` + 스모크 · 다시 읽기 음성 대조 구현 커밋 (이 문서와 같은 커밋) — **봉인 32 파일 불변**
     (`code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`) · 인계 도구 `scripts/g2_network_reread.py` 지문은 바뀐다 (발사 때 manifest `handover_code_hashes` 에 기록 ·
     §3 의 10-07 재등록 지문은 역사).
- 9-5 사전 점검 2 (10-07 22:24 KST · 1저자 WSL · 코드 `839dbac6b` · 재검증 5 첨부 · 증거 `docs/reviews/codex_gen2_network_reverify5_precheck_20261007/`): §9-4 ③ **제안** 기대와 **전부 같음** —
  §1 단계 3 smoke rc 0 (26/26 · case15 `[음성 대조]` 넷 PASS · 나머지 10-07 14:15 와 같은 값) · 단계 4 reread rc 0 (S0 · S0b) · 옛 실행기 시범 ROOT (`c3117438a`) 재감사 = 지금 케이스 기록 stages 로 결합 3 ·
  관측 문제 `[]` · SEALED 3 · 새 시범 (`839dbac6b` · `--observe-imports`) = 시도 사본 (`worker.json attempts[].stage_plan`) 으로 결합 3 · SEALED 3 · 봉인 `code_fp e8b2496b…` (32) 그대로.
  ⚠ §3b · §4 · §9-4 는 아직 ⬜ 1저자 비준 전 [→ 10-09 비준 · §9-6] — 이 줄은 결과 기록이지 비준이 아니다.  194 발사 = Codex GO 뒤 (§0).
- 9-6 **비준 · 변경 이력 (10-09 · Codex 재검증 5 `docs/reviews/codex_review_gen2_network_reverify5_20261007.md` 뒤 · 결과 0 건 — 194 미실행)** — ✅ **1저자 비준 10-09** (대화 *"비준이야"* · 수정 계획 `docs/reviews/g2rr5_fix_plan_20261008.md` Q3 — §3b · §4 · §9-4 제안 + 아래를 한 번에 · 원문은 각 자리에 그대로 · 비준 표지만 더함):
  ① §4 완료 뒤 기대에 재시도 예외 (`G2RR5-04` · §4 덧붙임).
  ② 다음 사전 점검 기대 (§9-4 ③ 갱신 · 고친 도구): 단계 3 smoke = case15 검사 **일곱** (`case15.proc` · `raw_sha` · `nc1_blocked` · `nc2_tau` · `nc3_cause` · `nc4_ionic` · **`nc5_attempt`** = 이번 망 CLI 시도 1 회 · 예외 없음 · rc 0 · per-mode 둘 · 실패 채널 정확히 등록 넷 — `G2RR5-02`) 전부 PASS · smoke rc 0 ·
     단계 4 reread = S0b 가 등록 표지 · 필수 ID 정확히 · 공용 판정 재계산 (`G2RR5-03`) — **10-07 WSL case15 기록은 이제 거부된다** (시도 증거 · 검사 ID 없음 — 의도 · 고친 스모크로 다시 만든다) ·
     단계 5 audit · 배포 관문 = 시도별 결합 값 검사 (`G2RR5-01`).
  ③ 인계 도구 지문 바뀜: `scripts/g2_network_reread.py` (실행기 HANDOVER_FILES) — 발사 manifest 에 기록 · 봉인 32 · `code_fp e8b2496b…` 그대로.
  ④ 같은 비준 (수정 계획 밖 덧붙임 · 1저자 10-09): Q6 = 감사 결합 기록에 분류 밖 단계 칸 (요약만 비운 실패 감사를 배포 관문이 거부 · 기존 pilot 감사는 고친 실행기로 audit 다시 — 읽기 전용) · Q7 = 스모크 실제 case15 두 판을 `--selftest-real` (slow) 로 나눈다 (§1 단계 1 도구 자체 시험에 함께 돌린다) — 둘 다 반영 = 별도 커밋 (⬜ 반영 전) [→ ✅ 반영 10-09: Q6 `7153a7d6a` (결합 기록 v2) · Q7 `7928ff0de` (`--selftest-real`) · WSL 재확인 명령 = `docs/reviews/codex_gen2_network_reverify6_request_20261009.md` 머리].

  | 자리 | 원문 (보존) | 비준 뒤 활성 |
  |---|---|---|
  | §3b 본 실행 관측 | 발사 승인 때 결정 | `--observe-imports` 필수 (§3b 제안) |
  | §4 실행 명령 | `run --root "$R"` (플래그 없음) | §4 제안 블록의 `run --root "$R" --observe-imports` |
  | §4 완료 뒤 기대 | 시작 = 끝맺음 · 194 · 194 | §4 덧붙임 합격선 · 확인 명령 (재시도 예외) |
  | §9-4 사전 점검 기대 | case15 음성 대조 넷 | 위 ② (검사 일곱 · S0b 재판정 · 결합 값) |

  ⚠ 비준은 등록 기대 · 명령의 비준이다 — 194 발사 = Codex GO 뒤 (§0 · 재검증 6) · S3 별개.
- 9-7 **사전 점검 3 = 발사 핀 (10-14 14:19 KST · 1저자 WSL · 핀 `1087a9b2f` — 도구 = Codex SUPR 재확인 핀 `df647d4e3` 과 `scripts/` · `webapp/` diff 0 · 깨끗한 트리)**: Python 3.12.3 · NumPy 2.5.2 · SciPy 1.18.1 · networkx 3.7 · fast16 16/16 · real4 4/4 · `g2_network_reread --selftest` 전부 통과 · 실행기 139/139 · 영수증 도구 88/88 · 194 dry-run (`--observe-imports --preflight-receipt`) rc 0 · `preflight-verify --expect-set production194 --approved-sha` rc 0 (11 칸 · 다름 0) · 영수증 `~/net194_1087a9b2f_preflight_1014_141953` (.json · .log) · 로그 sha256 `0d9dfe83b875451d…` (4,613 B · ⬜ 전체 값 = 1저자 묶음 `lhs_preflight_1087a9b2f_1014_141953.tgz` (sha256 `c75d5a71…`) 받은 뒤).
  **등록 §2 · §3 손 대조** (Codex 재확인 `docs/reviews/codex_review_supr_fix_reverify_20261014.md` §3 최소 기록 · 1저자 화면의 로그 `INPUT_DIGEST_JSON` 줄 · 코드 줄 ↔ 이 문서 §2 표 · §3 · 확인 = 조정자) — 여섯 칸 전부 등록 = 실측 (글자 그대로):
  n 194 · `missing_raw_sha` [] ✓ · `ids_sha256` `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf` ✓ · `raw_sha256_table_sha256` `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784` ✓ · 코호트 TSV lhs `32f00daa8394188d1e72531fd7fda1a8b47a9c279be76311ae7f2afa024b2809` ✓ · lhsx `0b85e8589917c9a3936ce29e9f36326993985ddd113ef32353a4ff96d981cb45` ✓ · code_fp `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` (CODE_FILES 32) ✓.
  ✅ **1저자 발사 승인 10-14** (*"나머지는 다 권고대로"* · *"이거했어"* = 실행) — 핀 `1087a9b2f4a93aa6a3b0debc698a14fffa13488d` · 194 먼저 → 보충 20 · 결과 = 9-3 칸 (완료 뒤 · ⬜).
- 9-8 **개정 초안 — FULL 모형 한계 범주 (10-15 · L214 · ✅ 10-21 · 1저자 비준 = §9-9 (비준 전 표지: ⬜ 1저자 비준 대기) · 결과 열람 뒤 정책 개정)** — 근거 = Codex LHS214 실패 검토 `docs/reviews/codex_review_lhs214_failures_20261014.md` §3 Q1–Q3 · §4 B6 ·
  수정 계획 `docs/reviews/lhs214_fix_plan_20261014.md` (✅ 1저자 10-14 Q1–Q5 권고대로) · 수정 재확인 요청서 `docs/reviews/codex_lhs214_fix_review_request_20261015.md` · 증거 `docs/reviews/lhs214_fix_evidence_20261015/README.md`.
  ⚠ **이력 (결과 열람 뒤)** — 이 개정은 10-14 실행 결과 (194 = done 186 · 실패 8 `lhsx_051` · `053` · `054` · `060`–`064` · 보충 20 = done 14 · 실패 6 · 14 건 모두 상위 사유 `physics.ionic=fail / solve_failed` ·
  `lhsx_054` 단독 진단 q 1.5370331988867802 > 1.5 — 나머지 13 건 원인 미확정) 를 **본 뒤** 쓴 허용 정책 변경이다 (Codex §3 Q1 — 이름만 바꾸는 수정이 아니다 · 과거에 막혔던 레코드의 게시 · 인계가 가능해진다).
  10-14 ROOT · 실패 기록 = 보존 (역사) · 옛 14 건 = 사후 "성공" 전환 없음 (옛 레코드 = 사유 solve_failed · 증서에 거부된 q 기록 없음 → 고친 코드에서도 차단 · Q3 (가) unknown ·
  case ID 허용목록 · 기대 실패 수 고정 없음 — 새 214 실행이 사례마다 다시 판정).
  **바꾸지 않는 것** (결과에 맞춰 바꾸지 않는다 · Q5 (가)): 문턱 1.5 (원 정밀도 엄격 > · q = 1.5 는 computed) · 수치 허용치 1e−6 (전류 보존 · 내부 잔차) · 풀이 사다리 · G > 0 · 병렬 상한 0 < G ≤ 1.1·Σg ·
  ID 집합 (§2 production194 `ids_sha256` `a04282d7…` · 보충 supp20 `991cf115…`) · 원 입력 (§2 원자료 표 · 코호트 TSV) · 실행 형식 v3 · 관측 필수 · §5-1–6 의 기존 차단 정책 (진짜 수치 실패 · 기하 · 세대 무효 · 잘못된 증서).

  | 자리 | 원문 (보존) | 개정 (✅ 10-21 · 비준 · §9-9 — 비준 전 칸 이름: 개정 초안 (⬜ 비준 대기)) |
  |---|---|---|
  | §3 코드 신원 | 봉인 32 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` | 봉인 32 (목록 그대로) · 바뀐 봉인 파일 4 = `scripts/network_conductivity.py` (sha256 `a525e2db98fd044f…`) · `scripts/tau_flux.py` (sha256 `c0a7da6e1b73bea9…`) · `webapp/app.py` (sha256 `3e82140f47c7e87b…`) · `webapp/pipeline_service.py` (sha256 `8026169f61e8bddc…`) ⇒ **`2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb`** (✅ 비준 = §3 활성 지문 (§3 끝 ✅ 줄) · 대기 선언 꼴 (`code_fp_pending`) 은 지웠다 — 비준 전 원문: 대기 지문 — 비준 · 재등록 때 §3 이 이 값으로 바뀌고 이 선언은 지운다 · 그 전 발사 대조 D1 · E2 = 등록 값 그대로 — 194 쪽 = §3 손 대조 · 보충 20 영수증 도구와 같은 규칙 · 실행기 `code_fp(code_hashes())` · ★ 10-19 L214R-R04 반영 값 (10-18 R02 `755325e1…` · R01 `fca3af77…` · 10-16 L214R-09–11 `e76dbe08…` 대체) — L214R 수정 커밋마다 갱신 · 진행 기록 10-19) · 인계 도구 (HANDOVER_FILES · 봉인 판정 밖) `scripts/lhs_design_dataset.py` sha256 `d1815155142e9092…` · `scripts/g2_network_reread.py` `0e2ec7ef37571268…` · 배포 빌더 `scripts/lhs_release_build.py` `3096e33fd0f19533…` (빌드 manifest `code` 칸) · 발사 커밋 = 이 개정과 수정을 담은 본 가지 커밋 (메인 세션이 적는다) — 그 체크아웃의 194 dry-run 이 같은 code_fp 를 찍어야 |
  | §5-1 케이스 판정 | done / failed (+ failure_kind) | 그대로 + 아래 ① 범주의 모형 한계는 진짜 실패가 아니므로 레코드 게시 (done) 가능 — 같은 실행의 다른 채널 · 가지에 진짜 실패가 있으면 failed 그대로 |
  | §5 결과 자격 (신설 ①–③) | — | 범주 · 공용 판정 · 예외 범위 · 우선순위 |
  | §5 공란 의미 (신설 ④) | — | τ NOT_COMPUTED + 사유 정확히 `full_over_conduction` · 배포 빈칸 코드 `NA_MODEL_LIMIT` |
  | §5 Hertz 주 타깃 (신설 ⑤) | — | 주 타깃 (H0) 모형 한계 = 진단 레코드 · 인계표 행 유지 · v1.3 주 타깃 배포 HOLD |
  | §5-7 회귀 허용 다름 | 선언된 변경 목록 | + 모형 한계 범주의 상태 · 사유 · 증서 진단 키 넷 (모형 한계 증서에만) · 전자 · 열 FULL 상태 · 사유 기록 키 넷 (값 칸 아님) · 웹앱 Physics 칸 strict missing — 정상 사례 타깃 수치 = 비트 같음 (A4 · 증거 `a4_no_impact.log`) |

  ① **범주 = 수치 인증 성공 / 출력 채택 거부** — 단상 이온 · 전자 FULL (H0 · H12 · Physics 공통 · 열 제외 — 열 병렬 상한 가드는 실패 그대로) · 수치 증서 통과 (전류 보존 · 내부 잔차 ≤ 1e−6 · 채택 단 = 마지막 시도 pass ·
     0 < G ≤ 1.1·Σg) · 풀이 기하 (판 · 상자 · 척도) 유한 양수 · q = (I_bottom/ΔV)·T/A 유한 · 원 정밀도 엄격 > 1.5 → 가지 상태 not_computed · 사유 `full_over_conduction` · accepted σ · 차원 σ = null ·
     FULL 유도값 (f · τ · 협착 전력 몫 · CF/FULL · Bruggeman/FULL 비) 없음 · 진단 q = FULL 증서의 별도 키 (`q_withheld` 원 값 · `q_guard_max` 1.5 · `guard_policy` `full_single_phase_q_gt_1p5/v1` · `sum_g`) · 채널 상태 `model_limit`.
  ② **공용 판정** = 증서 수준 `network_conductivity.model_limit_certificate_problem` + 레코드 수준 `tau_flux.full_model_limit_problem` (상태 · 사유 정확히 · 값 · 유도값 null · 관통 · 채널 상태 · 증서 · 채널 · 역할 · contact_mode · 전극 · σ₀ 결합 · 자리 모드) —
     생산자 · 일반 게시 · 정지 계약 · τ 0b · 세대 계약 증서 결합 · 다시 읽기 K6 · 인계 P4 (정지 계약 다시) · 배포가 같은 함수.  사유 · 채널 상태 이름만으로는 통과하지 않는다 · 모형 한계 레코드는 세대 표기 결손 면제를 받지 않는다.
  ③ **예외 범위 · 우선순위** — 입력 · 경계 검사 먼저 (`invalid_geometry` · `non_finite` = 기술 실패 · 비관통 판정보다 앞) · 앞 단계 실패 (첫 단 예외 · 미수렴 · 증서 실패 · 병렬 상한 밖) 는 높은 q 로 구제하지 않는다 ·
     같은 실행의 다른 채널 진짜 실패 = failed 우선 · CF · 협착-only 의 q > 1.5 = 기존 `model_over_conduction` (값 유지) · τ 앞 게이트 (띠 폴백 · 관통 불일치 · 온도 짝) 우선 · 옛 레코드 (solve_failed · 거부된 q 기록 없음) = 계속 차단.
  ④ **공란 의미** — τ 인계 = NOT_COMPUTED + 사유 정확히 `full_over_conduction` (기술 실패 사유 목록 밖 · 세부 꼬리 없음) · f · tau2 · tau · f_gap 빈칸 = **미제공** (0 · ∞ · 기술 실패 아님) · 미퍼콜 0 과 구분 (관통 분류 = 1) ·
     배포 빈칸 코드 `NA_MODEL_LIMIT` · 높은 q 로 빠진 값은 무작위 결측이 아니다 (남은 행만으로 코호트 전체를 대표한다고 쓰지 않는다 · 비교는 쌍대응 수 · 제외 사유를 밝힌다) · README 의 Codex Q3 권장 문구는 이 검사가 실제 통과한 뒤에만.
  ⑤ **Hertz 주 타깃** — H0 모형 한계 행 = 진단 레코드 (게시 · 인계표 행 유지) · **v1.3 주 타깃 배포 HOLD** (`lhs_release_build.v13_primary_model_limit_problems` — 실제 빌드 거부 · `check_v13` 문제 · 진단 · dry-run 묶음은 경고로만) ·
     Physics · H12 · 0 · 1.5 대체 금지 · 행 삭제 금지 · 주 타깃 결측을 허용하는 마스크 부분 배포 = 별도 등록 · 1저자 결정 · 집계 · 학습 규약.  Physics · H12 만 모형 한계 = 레코드 게시 · 부록 공란.
  ⑥ **결과 보고 (C9)** — Hertz 주 타깃 가용 수와 Physics 모형 한계 수를 따로 (배포 README 상태 집계 = 모형 한계 별도 줄 · 재적합 제외 사유 `NOT_COMPUTED:full_over_conduction`) · 입력 영수증 ≠ 결과 완료 증서.
  ⑦ **발사 (B7)** — 새 code_fp 하나로 두 새 ROOT (194 · 보충 20) · fast16 · real4 · 전체 사전 점검 로그 + 완료 영수증 · §2 손 대조 · 1저자 발사 승인 · 10-14 ROOT 는 지우지 않는다.  ⚠ 이 초안은 등록 기대의 개정안이다 — 비준 · 발사 승인을 대신하지 않는다 · S3 = 별개 (봉인 수치 모듈 둘이 바뀜 → S3 재봉인 의무 · S3 HOLD 그대로).
- 9-9 **비준 · 변경 이력 (✅ 10-21 · 1저자 비준 · L214 개정 §9-8 · 결과 열람 뒤 정책 개정 — 10-14 실행 결과 (194 done 186 · 실패 8 · 보충 20 done 14 · 실패 6) 를 본 뒤)** — 대화 원문 = 1저자 10-21 (06:10 UTC · 메인 세션) 이 질문 *"[LHS] Q1. 보충 영수증 selftest S0b (121/122) 를 비준 커밋 전에 작은 코드 커밋으로 고칩니다. 시험 먼저 쓰고, 고친 뒤 비준 커밋을 만들고 Codex 확인 요청서를 정리합니다. 발송은 1저자가 합니다."* 에 *"다 진행하자"* · 비준 커밋 = `f82929b06` (메인 세션 · 묶음 §1-4 diff 를 날짜 자리만 채워 넣음) · 이 대화 원문은 같은 날 뒤 커밋에서 채움.
  바뀐 자리 (원문 보존 · 비준 표지 · 기계 구문만 고침): ① §3 활성 봉인 지문 — 10-07 재등록 `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` → `2149f8738bb20b6a311b3c5b344b9745271a3f1324cabfb4582c175c3983c3eb` (§3 끝 ✅ 줄 · 옛 두 줄의 `code_fp` 기계 구문을 떼고 값은 그대로) · ② §3 표의 4 행 = 역사 (옛 값 = 표에 전체 그대로 · 새 값 = §3 끝 ✅ 줄) · ③ §9-8 대기 선언 (`code_fp_pending` 꼴) 삭제 · 머리 · 표 머리 비준 표지 · ④ §5 = §9-8 ①–⑦ 활성 (§5 머리 표지).
  바꾸지 않은 것 = §9-8 '바꾸지 않는 것' 그대로 (문턱 1.5 · 허용치 1e−6 · 사다리 · G > 0 · 병렬 상한 · ID 집합 · 원 입력 · 실행 형식 v3 · 관측 필수 · §5-1–6 기존 차단) · §2 표 · 10-14 ROOT · 실패 기록 (보존 · 사후 성공 전환 없음).
  ⛔ 비준은 등록 기대의 비준이다 — 발사 승인 아님 (§9-8 ⑦ B7 · 새 승인 핀 · 새 ROOT 둘 · 사전 점검 · 1저자 별도 승인) · S3 = 별개 HOLD (S3 수치 모듈 `scripts/network_conductivity.py` 가 바뀜 → S3 재봉인 의무) · v1.3 주 타깃 = H0 모형 한계 HOLD 그대로.
