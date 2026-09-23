# 세션 진행 — 2026-09-23

압축 후 이어받은 순서 (1저자): **Lee STEP3 16팔 → FAMV2-01 C→A→B → §12 개정 → 믹서 진단 → 04b**.

## ① Lee STEP3 16팔 — 발사 명령 전달 (⬜ 발사 확인)

- 러너 = Phase A 0.15 팔을 돌린 **그 러너** `scripts/sdcp_gain_vox015_8arm.sh` (새 명령을 짓지 않는다).
  v100 `/home/ubuntu/runyourai/1/pa/kits` 에서
  `KITS="VGCF_PTFE_3_0.5 VGCF_PTFE_3_1" VOX=0.15 BRIDGE_UM=0.24 PTFE_STAMP=centerline LEAN=2 OUTDIR=…/pa/lee_step3_v015_20260923`.
- 축은 Phase A 0.15 영수증(`docs/data/phase_a_104arms_20260921/arms_primary_v015_20260921/run_receipt.json`)과 같다:
  vox 0.15 · bridge 0.24 · segment · centerline · σ_ptfe 0 · σ_VGCF 78.5398 (직경보존 자동) · `--step3-require-gpu` · LEAN=2.
- ⚠ 함정 둘: ⓐ 러너의 `BRIDGE_UM` 기본은 **0.48** (SDCP 캠페인 값) — 명시 0.24 ⓑ 3_1 팔 태그
  `p2_VGCF_PTFE_3_1_a*` 가 Phase A mach 0.03 팔과 **같은 이름** — 옛 OUTDIR 을 가리키면 SKIP 캐시가 옛 팔을
  "완전" 으로 재사용한다 (영수증에 침대 정체가 없다).  ⇒ 새 OUTDIR · 이미 있으면 발사 안 함.
- 발사 전 preflight: 두 침대 `latest_run` 의 `platen_mach_VcP == 0.01` · `quasistatic_violation False` ·
  `porosity_at_target_pct` non-None · 입력 파일 4 개 · cupy/skimage · `scripts/` dirty 0.
- §6 한정 (결과 표에 병기): *"첨가제 wt% 를 Lee 에 맞추고 AM:SE 는 우리 스캐폴드 값(34.18 vol%)으로 고정한 대조"*.
- ⛔→✓ **첫 발사(09-23 ~10:0x)가 런 전 게이트에서 섰다 — 팔 0, GPU 미사용.**  러너의 미정의 이름 게이트
  (`scripts/check_undefined_names.py`)가 v100 conda env 에 **pyflakes 가 없어** AST 대체 경로로 떨어졌고, 그 경로가
  **오탐 129 건**을 냈다 (pyflakes 로는 0 건 — 여기서 정확히 129 건 재현).  원인 셋: 중첩 함수·lambda 의 **자기 인자**를
  바깥 함수 기준으로 봄(`sr01_stamp_compare.py:476` 의 `chk(c, m)`) · **클로저** · import 시 `dir(__builtins__)` 가 dict.
  ⇒ 즉시 처방 = v100 에 `pip install pyflakes` 후 재발사 · 근본 수정 = 대체 경로를 스코프-근사로 고치고 selftest
  ④⑤⑤b⑥⑦ 이 `with_ast()` 를 **직접** 시험 (먼저 빨간불 129 확인 → 수정 후 0).  옛 selftest ①~③ 은 작은 픽스처라
  이 부류를 못 봤다.
- ⚠ 16팔이 끝날 때까지 v100 리포에서 `git pull` 금지 — 팔마다 새 파이썬이 뜨므로 중간 pull 은 팔마다 `code_sha` 를 가른다.
- 로그의 *"진단 팔 … 생산 규약 아님 (CDXR2-6)"* 은 SDCP 캠페인 기준의 **옛 배너**다 (09-10 기록과 같음) — Phase A 에서는
  centerline + σ_ptfe 0 이 **등록된 규약**이다 (CL-60).  동작은 봉인 그대로.

## ② 믹서 바닥 검사 — HOLD · 원인 = 등록 결함 (prereg §4)

- 세 칸 × 10 런 (`docs/data/mixer_floor_diag_20260923.tsv`).  16×16×4 에서 2.83~3.02 (0/10), 12×12×3 3.24~3.66
  (0/10), 8×8×2 7.97~11.27 (10/10).
- **Popoviciu**: `p_i ∈ [0,1]` ⇒ `S² ≤ 1/4` ⇒ 비의 천장 `0.25/S_R²` = 16×16×4 **3.94~4.10** · 12×12×3 **4.31~4.68**.
  문턱 5 는 두 잔 칸에서 **도달 불가능**.  천장은 E0 의 S_R² 만으로 정해진다 (L 런 값 미사용).
- 층상 정도 `S₀²/0.25` 는 칸에 무관하게 66~81 % — 비의 하락은 전부 S_R² 증가.
- ⇒ 런 계속.  ⬜ HOLD 해소 방식 저자 결정 (권고 (b): 등록된 8×8×2 에 같은 문턱 5).
- ⚠ 판독기는 바닥 검사만 시켜도 **전 프레임 M(t)** 를 계산해 남긴다 — 80 파일을 열지 않고 삭제 (S₀·S_R 만 추출).

## ③ FAMV2-01 코드 수정 C → A → B (`scripts/mpm3d_compaction.py`, selftest 120 → 140)

- C 재현 먼저: 옛 설정점(target)에서 f=0.675 서보가 SE 를 0.0975 → **0.2943** 으로 다시 눌렀다 (빨간불 7).
- A: `am_skeleton_stress()` 매 프레임 · 서보 네 곳이 `target − am_skel` → SE **0.0975** 평형 (초록).
- B: `am_load_guard_errors()` — servo-legacy + f · servo + floor + f (01-b) · load-state + f 를 taichi 초기화 **전**에
  거부.  음성 대조: 가드를 빼면 정확히 세 건만 빨간불.
- f=0 비트 동일 (판정 격자 · 옛 인라인 식 · 설정점).  산출물 `am_load_applied_to` 는 f > 0 일 때만.
- **CPU taichi 스모크** (real_14 scaffold · `--se-frac 0.27` · n_grid 32 · 옛 HEAD 코드 vs 새 코드, 같은 인자):
  - **f=0**: metrics **68 필드 중 67 개 비트 동일** (porosity · 두께 · 응력 · coverage …).  남은 1 개는
    `am_load_split` (R2.5-v2 z-슬라이스 **진단 누산**) — 상대 ≤2e-5 차 (`f_am_cut` 0.99942418 ↔ 0.99942340).
    병렬 원자 누산 순서로 보인다 (이 수정이 안 건드리는 경로).  ⚠ 같은 코드 반복 런으로 **확인하지는 않았다**.
    frame 로그의 유일한 차이도 그 진단(`fAMcut` 0.999 ↔ 1.000, frame 80)뿐 — wall_z·porosity·wallP 는 전 프레임 동일.
  - **f=0.675 · target 0.03**: 설정점이 바뀌어 서보 프로브의 대기 판정이 달라지고 궤적이 **조금** 갈린다
    (예: frame 40 porosity 21.50 ↔ 21.57).  ⚠ 그러나 n_grid 32 장난감 침대는 압력을 못 쌓아(wallP ≤ 0.0068 GPa
    내내) **두 설정점 모두 아래**라 (1−f)·target 평형을 **보여주지 못한다** — 그것은 selftest 의 합성 침대가 보인다.
  - target 0.3 · f=0.675 짝은 같은 이유로 판별력이 없어 중간에 PID 로 껐다 (RC 143).
  - ⚠ **열람 고지**: 스모크 산출물 비교에서 R2.5-v2 진단 `am_load_split` (f_am_cut ≈ 0.9994) 을 봤다 — §9 등록 조건(384 · real_14 SE 덤프)이 아니라 채점 대상이 아니지만, prereg §12-0 에 사실을 적었다.

## ④ §12 개정 (FAMV2-02·03·04·05·07, 결과 0 건)

`docs/reviews/fam_platen_prereg_20260812.md` §12-0 ~ 12-4.  ⬜ 봉인 전 남은 저자 결정: 01 관측 사건 · R1 재사용 ·
04b · 기준 상태 지문 · R2 argv · 동률 폭 · 재시도 규칙 (`codex_fam_r3v2_verdicts_20260922.md` §F-3).

## ⑤ SELF-45 — 회신 **발송됨** (사용자, 수치로) · 완성본은 사용자가 후속 전달.  S14·S15 컬러바 값 제공 완료.
