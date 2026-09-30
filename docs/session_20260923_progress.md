# 세션 진행 — 2026-09-23

압축 후 이어받은 순서 (1저자): **Lee STEP3 16팔 → FAMV2-01 C→A→B → §12 개정 → 믹서 진단 → 04b**.

## ① Lee STEP3 16팔 — ✅ 발사됨 (09-23 약 10:31 KST, 러너 PID 501405, v100)

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
- ✅ **재발사 (09-23 약 10:31)** — v100 conda env 에 `pip install pyflakes` 후 (리포 pull 없이) 같은 인자로.  게이트 RC=0 · OUT 에 영수증 하나 · 관문 3/3 · `σ_VGCF 100 → 78.5398` · 첫 팔 payload 가 복셀화 중 (CPU 99.8 % · RSS 7.7 GB) 확인.
- ⚠ **헛경보 교훈 (감시)**: 대화형 셸에서 `setsid nohup … &` 의 `$!` 는 **곧 끝나는 부모 PID** 다 — `setsid` 가 프로세스 그룹 리더면 fork 하고 부모는 바로 나간다 (실측: `$!`=501404, 러너=501405).  그 PID 로 감시하면 "⛔ 종료됨" 헛경보가 난다 ⇒ 감시는 **이름으로** (`pgrep -f sdcp_gain_vox015_8arm\.sh` — 조회 전용).
- ⚠ **pull 금지 이유 하나 더**: 러너 영수증(`run_receipt.json`)에 `code_sha` 가 들어간다 — 발사 뒤 pull 하면 영수증이 달라져 러너가 **거부**한다 (재발사 때 pull 하지 않은 이유).
- ⚠ 16팔이 끝날 때까지 v100 리포에서 `git pull` 금지 — 팔마다 새 파이썬이 뜨므로 중간 pull 은 팔마다 `code_sha` 를 가른다.
- 로그의 *"진단 팔 … 생산 규약 아님 (CDXR2-6)"* 은 SDCP 캠페인 기준의 **옛 배너**다 (09-10 기록과 같음) — Phase A 에서는
  centerline + σ_ptfe 0 이 **등록된 규약**이다 (CL-60).  동작은 봉인 그대로.
- ✅ **16/16 완주** (마지막 팔 `p2_VGCF_PTFE_3_1_a7.json` 09-23 18:21, 러너 정상 종료).  러너 로그 끝의 *"계약 봉인을 돌리지 않는다"*
  는 이 러너가 팔만 내고 판정은 캠페인 판정기 소관이라는 뜻.  v100 `git pull` 금지 **해제**.
- 산출물 tgz `…/pa/lee_step3_v015_20260923.tgz` = **327 MB** — LEAN=2 JSON 16개라기엔 크다 (Phase A 104팔 tgz 는 26 KB).
  사용자가 Windows(Administrator) Downloads 로 scp 뒤 업로드 예정 — 업로드가 안 되면 JSON·영수증·로그만 lean 으로 다시 묶는다.
- ✅ **판정선 등록** (사용자 "원하는대로 해" = 비준): `docs/reviews/lee_abs_sigma_e_prereg_20260923.md` (결과 0건 상태 · R 밴드 0.5–2 /
  0.1–10 · 런 전 예상 R ≈ 1.5–2.5 · PTFE 감도 Q 예상 ≈ 0.85 vs Lee 0.44 · 영진 DC 분극 판정선 ≥10 / ≤1 mS/cm).  σ_e 미열람.
- ⚠ lean 재포장 (JSON·log·txt·sh 만) 도 **327 MB 로 같다** — 팔 JSON 하나가 **148 MB** (STEP2 페이로드 시각화 배열).  큰 배열만
  잘라낸 요약 (9 KB) 으로 받았다.
- ✅ **대조 A 판정** (사전등록 §5): 적격 16/16 (수렴 · centerline · segment · bridge 0.24 · vox 0.15 · σ_VGCF 78.5398 · GPU ·
  code_sha = 영수증 · LEAN=2 확인).  Lee 첨가제 조성 σ_e **70.53 ± 0.12 (SE)** · 생산 조성 **59.28 ± 0.12** mS/cm (CV < 0.6 %).
  **R = 2.074 ⇒ 자릿수 정합 (Tier 1)** — 밴드 안 상한 2 를 3.7 % 넘음 (런 전 예상 1.5–2.5 안) · **Q = 0.840 ⇒ 예측 적중** (예상 0.85,
  Lee 보간 0.44).  ⚠ 사용자 정정: 모델 PTFE = **중심선 한 셀 절연뿐** — 표면 코팅 없음 (`ptfe_block_um` 은 SE 이온 셀 전용, 0) ·
  부피도 과소 (한 셀 선 = 실제 PTFE 부피의 **0.40 / 0.41**, 셀 0.15 µm < 피브릴 Ø0.25 µm).  내 첫 문구 "부피로만 반영" 은 부정확했다.  v100 의 2.4 GB 원본 폴더 = 전체 원본.
  ⚠ **정정 (같은 날 밤)**: 여기 적었던 *"유일한 전체 사본"* 은 틀렸다 — 폴더를 통째로 `tar czf` 한 tgz (327,526,584 B) 를
  사용자가 Windows(Administrator) Downloads 로 받았다 (무결성 미확인).  단 **STEP2 침대는 그 tgz 에 없다** (아래 ⑨).

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

## ⑥ 독립 연구 트랙 개설 — Ag–C 인터레이어 점착 (DFT 팀 협업)

`docs/adhesion_agc_interlayer_20260923.md` (우리 쪽 설계·분업) · `docs/dft_request_adhesion_agc_20260923.md` (DFT 팀 전달 원문).  핵심: DEM 은 점착에너지를 **입력**으로 받으므로 W_ad 는 DFT, 구동압 의존 G_c,eff(P) 는 DEM 박리(하한).  ⬜ 계면 정의·범위·자원 저자 결정 대기.
DFT 쪽은 사용자가 다른 대시보드에서 진행한다 (09-23) — 이 세션에서는 요청 원문까지.

- ✅ **문헌 4편 원문 → 정본 litdb 카드** (정본 `62993f64d`; litdb-curator 가 쓰고 내가 정본에서 따로 검증):
  `liao2025_interfacial_adhesion_li_plating_carbon_interlayer` 크롭 17 · `tabakovic2026_mechanical_stress_eis_ica_drt_dfn` 10 ·
  `song2025_porous_argyrodite_modulus_fracture_toughness` 3 · `spencerjolly2023_ag_graphite_interlayer_operando_xrd` 11
  = **41 장, 전부 그림·표 영역** (접촉 시트로 육안 확인 — 페이지 통째 렌더 0) · INDEX 등록 (tabakovic 은 argyrodite
  논문이 아니라 INDEX_DEM 만) · DOI 중복 0.  사용자의 "7번" (후보 표 7번째 줄, 파일명 `7._…`) = Spencer-Jolly 는
  정본에 **없었다** → 새 카드 (Spencer · DOI · "silver-carbon" 으로 papers/ 전수 grep).
- ⛔ 우리 §6 의 *"Liao 적층압 100→400 MPa 에서 4배"* 는 틀렸다 → **lamination(제조 압착)압** (사이클 적층압은 5 MPa 고정).
  결론 1 (*"약한 쪽이 상한"*) 도 실측 9–41 J/m² ≫ 0.20 J/m² 와 맞지 않아 정정.  ⬜ §5-4 압력 축 결정 추가.
- ⚠ Song SI zip 은 macOS 메타데이터(`__MACOSX/`)뿐이다 — 영상 2개(외팔보·파괴 시험) 본체가 없다.  카드는 본문으로 작성.
- 📨 **DFT 쪽 회신 초안 수신** (정본 `06350891d` · `34c7b28ed`, 사용자 전달).  정정 셋을 정본 카드로 **직접 확인한 뒤 수용**:
  Pustorino 0.20 = 비화학량론 대칭 슬랩의 2γ, 화학량론 벽개 0.47 (100) · 0.37 (110) / Maurer 0.26 (논문 셀 밀도) + 방법 산포
  0.19–0.45 가 0.3 경계를 가로지름 / Giovannetti 원문 용어 = weak bonding (Pd 화학흡착 0.52 ⇒ 크기 ≠ 기전).  옛 LPSCl|NCM
  파이프라인 결함 (R-centering 누락 · 셀 겹침 · 5/20 시드 선별 · AFM aJ 오독) 은 DFT 쪽 리뷰 두 편에 기록돼 있어 §2-1 "나란히"
  전제를 내렸다.  트랙 문서 §1 · §2-1 · §3 · §4 · §5 · §6 정정.
  확인 요청 ①②③ 의 DEM 쪽 권고 = §5-5 ~ 5-7: W_sep 헤드라인 수용 + 이완 값 병기로 띠 / "S 바깥 + Li·PS₄ 바깥" 두 면 · (가) 선호 /
  **P2 를 P1 급으로 지금** (Ag 5.7 vol% ⇒ 탄소 계면이 면적 지배).  회신 초안 `docs/dem_reply_to_dft_adhesion_20260923.md` —
  ⬜ **1저자 비준 후 발송**.  → 발송됨 (사용자).
- 📨 **DFT 회신 2 수신 (정본 `d2993a7b7`)** — 우리 권고 셋 **전부 채택**: W_sep 헤드라인 + `W(DFT@UMA)` 병기 / (가) 대칭 슬랩 두 장
  (S 바깥 162원자 · Li·PS₄ 바깥 150원자 · 단면 10.055 Å · `db/structures/wad_se_slabs_2026_09_23/`) / **P2 를 P1 급으로**
  (LPSCl|graphite(0001) 먼저 · P3 범위 밖).  정합 후보 P1 SE 1×2 + Ag(111) 2×7 ≈436원자 · P2 SE 1×3 + 흑연 4×7 ≈820원자.
  비용은 gabia SE|SE 대조 5잡 첫 실측 뒤.  정본 결정 셋·슬랩·빌더 실재 확인 ⇒ 트랙 문서 §5-5~7 **결정됨**으로 갱신.
  ⚠ **최종판 (interim 파일)** 은 한 군데 다르다: 계산기·비용은 외부 리뷰 뒤 — DFT 쪽 자원이 단일 노드 (GPU 48 GB) 뿐이고 클러스터
  접근이 끝나 (KISTI 없이) P1 ~436 · P2 ~820원자 전체 계면의 평면파 DFT 는 못 돌린다.  후보 (a) DFT-검증 MLIP+D3 · (b) 가우스 기저
  DFT 단일점.  헤드라인이 DFT 값인지 MLIP+D3 값인지 확정 전 약속 없음 ⇒ §5-5 "정의 결정 · 계산기 보류" 로 고침.
  ⚠⚠ **최종판 (외부 리뷰 BW 뒤)**: 전체 계면 DFT 분리일은 **약속하지 않는다** — 작은 주기 모델 직접 DFT 와 전체 계면 UMA+D3 **예측**을
  구분 보고 · UMA 예측을 DEM 에 쓰면 **합의한 민감도 시나리오로만** (G_c 범위 = 신뢰구간도 상·하한도 아님) · 848원자 5점 추진 안 함 ·
  P3 보류 · 보고량 이름 "SE 에 정합되도록 변형된 Ag·흑연 박막의 고정기하 분리일".  ⇒ 트랙 §5-5 확정 · §3 "띠" → "민감도 시나리오" ·
  §5-8 시나리오 합의 신설 (⬜).  내가 채팅에 쓴 수용 기준 회신 초안 ("표지+Δ+registry 면 충분") 은 이 입장과 어긋나 **보내지 않는다**.
- ⚠⚠ 내 "16배 규칙 (면적비 ≈ 부피비)" 은 **우리 가정**이다 (DFT 는 두 쌍의 W 만 준다).  면적비는 Delesse(=부피비) 와 표면적 몫
  (∝ V/d) 사이 — Ag 나노입자 + 흑연 조합이면 Ag 몫이 부피비의 10배 이상일 수 있다 ⇒ 트랙 문서 §3 에 **3′ 단 신설** (인터레이어
  DEM 침대에서 상별 접촉 면적비 계산).

## ⑦ 동료(강준희) 카톡 — "복합양극 σ_e 는 0.1~1 mS/cm" 제기 → 반박 발송 (09-23 19시)

- 요지: 동료 표 (Schlautmann 2023 0.38–0.40 · Jung 2022 0.003–0.4 · Lee 2026 0.00178 · Tron 2023 VGCF ≤0.4 / C65 ≤70) + 우리
  대칭셀 0.4→0.5 vs 모델 "54→76" (동료가 뭉뚱그린 값; 원고 페이로드는 **54.5 / 71.4 mS/cm**).
- 반박 근거 (전부 확인): 원장 CL-38 (대칭셀 TLM r_e = 접촉 지배) · CL-46 (같은 재료계 DC 분극 34 · 38.6~65.2 와 같은 자릿수) ·
  정본 카드 lee2026 (σ 시료 = **VGCF 제외**, 0.00178 은 LPSCl 317 nm 코팅 시료 · 무코팅 0.257) · 원고 조성 SBE VGCF/PTFE 3/1.
  동료 표의 C65 행 (≤70) 자체가 탄소 복합체는 수십 mS/cm 임을 보여준다.  배영진 님 수긍.
- 약점 (사용자에게 고지): 모델 절대값은 접촉 이상화 쪽이라 비슷한 조성 문헌 대비 2~4배 높다 · Tron VGCF 행 · Jung 행 원문 미확인 ·
  두께 환산 (원장 72.5 µm 면 0.12→0.15 mS/cm; 동료 0.4→0.5 는 ≈240 µm 역산) · **비(ratio) 로 넘어가면 불리** (모델 비 인용 금지 ·
  σ_SDCP 250 저자 지정값).
- 다음: 영진 님 DC 분극 (두께 2종 요청) — 판정선 초안 `lee_abs_sigma_e_prereg_20260923.md` §2.
- 54.5/71.4 는 DEM 접촉망이 아니라 **MPM 침대 위 복셀 STEP3** 값 — 원고·발표에서 "DEM 값" 이라 부르지 않는다.

## ⑧ Schlautmann 2023 (AEM 13, 2302309) — 중단 → **재실행 완주 · 정본 `e261c2020`** (사용자 PDF 본문 + SI)

확인 항목: ① 측정 시료에 탄소가 있는가 ② 0.38–0.40 mS/cm 의 시료 · 방법 (TLM/DC) · 압력 ③ NCM–NCM 전자 계면 저항 수치
(CL-81 의 빠진 항) ④ SE 입경별 σ_ion · τ (Cronau 대조).  결과는 정본 카드 + 이 파일에 요약.

- ⛔ **정정 (09-23 밤)**: 위 제목의 *"진행 중"* 은 틀렸다.  에이전트 `agent-acad54127e182e645` 는 11:53–12:06 UTC
  (20:53–21:06 KST) 12 분 · 도구 호출 55 회 뒤 *"Request interrupted by user"* 로 멈췄다.  **카드 Write 0 건** — 크롭만 뽑고
  S17·S18 을 보던 중이었다.  정본에 올라간 것 없음 (09-23 밤 fetch 로 `papers/` · `figures/` 에 schlautmann 0).
- ⚠ 그 크롭이 있던 ../litdb-canon 워크트리는 **다음 게이트가 지웠다** — `scripts/check_all.sh` 가 부르는
  `scripts/litdb_promote.py` `--selftest` 가 `cmd_open(force=True)` 로 **공유 경로를 강제 재생성**하고 끝에 `cmd_cleanup` 한다.
  크롭은 업로드 PDF 에서 다시 뽑히므로 실손은 없다.
- ⛔ 위험: litdb 에이전트가 ../litdb-canon 에서 일하는 동안 게이트를 돌리면 **그 작업을 지운다** — 워크트리만이 아니라
  브랜치 `tmp-litdb-promote` 와 에이전트의 `--close` 가 읽는 상태 파일 `.litdb_promote_state.json` 까지 셋 다 공유였다.
- ✅ **수정 (사용자 비준 09-23 밤, `c9b1e4203` · 원장 `SELF-46`)** — `scripts/litdb_promote.py`: selftest 본문이 **전용 임시 이름**으로만 돈다
  (`_selftest_private`) + 새 검사 **(0)**: 공유 이름 자리에 미끼 (워크트리 · 브랜치 · 상태 파일) 를 앉혀 두고 본문 뒤 셋이
  그대로여야 PASS.  재현 먼저 — 전용 이름 전환 없이 (0) **FAIL** (미끼 셋 다 삭제) 확인 → 전환을 넣어 **PASS** (9/9).
  두 번 모두 **실행 중인** Schlautmann 에이전트의 워크트리 · 브랜치 (8ac5c7a3f) · 상태 파일 sha256 불변을 대조했다.
  덤: (5) 를 `dry_run=True` 로 — INDEX 검사가 dry-run 분기보다 앞이라 판정은 같고, 검사가 뚫려도 selftest 가 정본에 푸시 못 한다.
  ⇒ *"에이전트 작업 중 게이트 금지"* **해제**.
- 같은 밤 게이트 실패 1 건 = 그 selftest 의 180 s 시간초과 — 컨테이너 재부팅 직후 부하.  단독 실행 37 s 통과.
- ✅ **재실행 완주 (09-24 새벽)** — 정본 `e261c2020` · 카드 474 줄 · INDEX · INDEX_DEM · comparison 두 파일 · 크롭 32
  (본문 그림 6 · SI 그림 22 · SI 표 ST1–ST4) — 캡션 수를 pdfminer 로 **따로 세어** 일치, 접촉 시트 육안으로 전부 그림·표 영역.
- 원문 대조 (내가 PDF 에서 직접): 복합체는 NCM811 : LPSCl **70:30 wt% 두 성분뿐** (p. 8 *"The two components were
  transferred into a 15 mL ZrO2 cup"*; 본문의 "carbon" 두 번은 합성 앰풀 코팅 · SEM 테이프) ⇒ **무탄소**.  σ_e 실측
  (Table S4, 확대 판독) S/M/L/XL = **0.301 / 0.257 / 0.311 / 0.406 mS/cm** · 시뮬레이션 0.765 / 0.767 / 0.635 / 0.431.
  본문 p. 6 은 *"0.40 (±0.06) for XL and 0.38 (±0.15) for S"* — S 의 0.38 은 표의 0.301 과 어긋난다.
  방법 = 이온차단 대칭셀 EIS-TLM + DC 분극 교차, 측정압 50 MPa · 25 °C.
- ⇒ 동료 표의 *"0.38–0.40 mS/cm"* 는 **무탄소 70:30 복합체** 값이다 — VGCF 3 wt% 전극과 같은 선에 놓을 양이 아니다
  (⑦ 의 반박이 원문으로 확인됨).
- Q3: NCM–NCM 전자 계면 항은 모델 식에만 있고 **분리값 보고 없음** (합만 보고).  Q4: σ_ion 0.254 / 0.199 / 0.153 /
  0.165 mS/cm (S→XL) — 1 µm 미만은 시험하지 않아 Cronau 인자와 모순도 지지도 아니다 (방향만).
- ✅ **정본 쪽 발견 둘 처리** (사용자 비준 09-24 *"권장하는 방향으로 진행해줘"*):
  ① `litdb/comparison_vs_ours_DEM.md` — 작업 브랜치의 실제 스윕 (`check_review_findings.ban_sweep`) 으로 다시 세니 **4줄 8건**
  (2391 행은 이웃 줄 철회 표지로 이미 통과).  1235 · 1427 · 1467 에 철회 표지 + 원장 `CL-24`, 1503 의 `CL-33` hold 값은
  **숫자를 지우고** 원장 인용.  1427 의 vox 범위 오기 (0.4→0.15 → **0.4→0.25**) 도 정정.  수정 뒤 스윕 0 건 = 정본 `e16b480e9`.
  ② 크롭 도구 결함 셋 (ST 표 라벨 · 위 캡션 꼬리줄 · `_shrink` 팔레트 분기) — 재현 먼저 (selftest 48 → 55, 양성 넷은 수정 전
  빨간불).  ⚠ 꼬리줄 첫 수정은 `merge_caption` 재사용이라 **다른 논문 Fig. 8 의 패널 라벨을 잘랐다** → 한 줄짜리 · 왼쪽 끝
  일치 · 간격 ≤ 한 줄로 좁히고 그 회귀를 음성 검사로 고정.  업로드 PDF 11편 드라이런 좌표 전수 비교: 바뀐 것은 schlautmann SI
  표 4장 추가와 fS2 · fS5 · fS7 · fS9 위 끝뿐 (나머지 10편 변화 0), 8장 육안 확인 = 정본 `0627a5dfa`.
- ✅ **카드 4편의 같은 부류 7줄도 정리** (사용자 비준 09-24 *"ㅇㅇ 비준해줘"*) — 정본 `f7977d926`.  (보고 때 "5편" 이라 한 것은
  잘못 센 것이고 **4편**이다.)  `alabdali2023…` 1 (vox 오기 0.15→0.25 포함) · `duquesnoy2020…` 2 (`CL-41` hold 값 삭제 +
  같은 문장의 *"보고값은 하한"* 은 `CL-72` 가 철회한 서술이라 취소선 · 표지) · `nam2026…` 2 · `zhang2026…` 2.
  수정 뒤 정본 litdb 354 파일 스윕: 남은 것은 **논문 자체 수치 오탐 3줄** (`jun2022` · `jung2026` · `kahle2020`) 뿐.
  재발 방지 후보 (미착수): 우리 스윕을 정본 litdb 에도 돌리기 — 지금은 대상 밖이라 이번 7줄 · 4줄이 몇 주씩 살아 있었다.

## ⑨ v100(uma) 인스턴스 — 반납 검토 → **유지** (사용자 결정, 09-23 밤)

- 지금 v100 에서 도는 것 없음 (Lee 16팔 18:21 종료 · SELF-45 09-22 종료).  믹서 13 런은 **WSL**, `ps_*_r45_r3` 는 **ibb**
  (`handoff_review_20260922.md` 런 표) — v100 과 무관.
- 다음 GPU 수요는 **FAMV2 하나** — 봉인 전 저자 결정 셋 (01 관측 사건 · R1 재사용 · 04b) 이 남아 지금 띄울 런이 없다.
  R2 primary n_grid 384 = 32 GB 급 카드 · kgy 카드는 DFT 점유 (`session_20260911_progress.md` §11).
- ★ 사용자: **저장소 1 (`~/runyourai/1`) 은 인스턴스를 없애도 남고, 새 키로 붙여 이어 할 수 있다.**  env `uma`
  (`~/runyourai/1/opt/miniforge3/envs/uma`) · 리포 · Lee 침대 (`pa/kits/VGCF_PTFE_3_{0.5,1}`) · Lee STEP3 원본 · SELF-45 (`rerun/`) ·
  Phase A 판정 원본이 전부 그 안이다.  ⚠ 09-13 까지는 `~/pa/` (저장소 밖) 를 썼고 만료 때 사라졌다.  09-14 재생성 침대가 09-21 에
  0/5 였던 이유는 기록에 없다.
- 이어 쓰기 조건: ① **같은 마운트 경로** `/home/ubuntu/runyourai/1` — conda env 는 경로를 옮기면 깨지고, 런 스크립트가
  `E=/home/ubuntu/runyourai/1/opt/miniforge3/envs/uma/bin` 을 절대경로로 쓴다 ② 저장소 밖 (홈의 나머지 · apt) 은 사라진다 —
  `~/.bashrc` 의 conda init (`(uma)` 자동 활성) · `rsync` (apt 로 설치했었다, `focus_top_defect_20260922.md` §I-7) · `~/.cache`
  ③ 새 인스턴스 GPU 드라이버가 env 의 cupy · taichi 와 맞는지 첫 접속에서 스모크.
- ✅ 사용자 결정: **유지** (*"v100 유지 이유 생겼어 그냥 놔두자"*).  위 조건 셋은 나중에 반납할 때 쓸 점검표로 남긴다
  (홈에 저장소 밖 파일 · 침대 run 디렉터리 위치 · 드라이버 버전).
- ✅ **`pa/` 정리 (09-24)** — Phase A 원본 7 폴더 (약 28.5 GB) 의 요약 (103,697 B) 을 받아 대조: 판정 104 팔의 원본 sha256
  **104/104** · σ_e **104/104** 일치 ⇒ 삭제 승인.  09-14 봉인 이탈 배치 96 팔 (`off`) 의 σ_e 는 요약이 유일한 사본이라
  `docs/data/phase_a_raw_summary_20260924/` 로 커밋 (같은 침대 96 짝의 centerline/off 비 표 = 기술 보고 전용).
  사용자가 7 폴더 삭제 완료 (저장소 1 = `:/mnt/sdb`, 98 G 중 38 G 사용 · 56 G 여유).
  `kits/` 16 GB = **온전한 침대 7 개** (Phase A 5 개 09-14 mach 0.03 · Lee 2 개 09-21/22 mach 0.01 — 7/7 핵심 파일 넷 확인) —
  **유지**.  침대당 2.2–2.4 GB 의 대부분은 `se_dump` 782 MB · `se_dump_eps` · `se_dump_dg` · `fibre` · `fibre_dia` 각 261 MB
  (MPM 출력 — 다시 만들려면 GPU) · `mpm_payload.json` 151 MB.  09-21 기록의 *"침대 0/5"* 는 틀렸다 (그 파일에 정정).

## ⑩ LHS 인계 — 판단 누적 시작 (09-24, 사용자 "이제 lhs 에 집중")

정본 = `docs/reviews/lhs_handover_judgments_20260924.md` (판단 J1–J7, 생길 때마다 더한다).  인계표는 **배포 보류** 유지.
- ⛔ 새 결함 `LHS-10` (P1): φ · porosity 분모가 덤프 상자 바닥 (−10 µm) 기준 — 벽 (z = 0) 이 아니다.  130/130 에서 정확히
  +10.000 µm, φ 가 0.757–0.875 배로 작고 (얇을수록), porosity 중앙 47.2 → 37.5 %.  DESC-07 항등식은 통과 (같은 분모).
- 두께: 지금 φ 와 자기일관인 것은 ① plate_z − z_floor (J2 수정 뒤) — ② 는 φ 까지 함께 옮길 때만 (J3).
- lhsx 확장 64 건 (62 완주) 수확은 LHS-10 수정 뒤 (J7).
- ⛔ 새 결함 `LHS-11` (P1, 판단 J9): 97/130 건의 플래튼이 원자 덤프보다 평균 150만 step 이른 메시 (`latest_le`) — 압축 중 위치라
  porosity 가 부풀었다 (벽 기준 중앙 38.5 % vs 같은 step 메시 33 건 11.0 %, 겹치지 않음).  J5 의 주원인.
- 웹앱 코드로 안 돌린 이유 (J8) = `DESC-01` (τ 없으면 φ 까지 버림 — LHS 는 116 건).  웹앱은 바닥이 맞다 (`V_box = L²·plate_z`).
- 비교 도구 `scripts/lhs_phi_crosscheck.py` (두 코드의 함수를 그대로 호출 · 바닥 틈 + 플래튼 − 고체 윗면) — WSL 실행 대기.
- ✅ 교차검사 WSL 실측 (J10): FLOOR_ONLY 130/130 · 잔차 5.5e-14 %p (세 번째 차이 없음) · 웹앱 porosity 중앙 37.54 % ·
  플래튼 − 고체 윗면 exact −1.2…−0.3 µm / latest_le +8.1…+27.4 µm.  권고 = 두께 · φ · porosity 모두 ② (고체 윗면 − 벽), 비준 대기.
- ✅ J11–J12: 웹앱 방식 1순위 (사용자 지적) · LHS-11 원인 = 옮길 때 메시를 문자열 정렬로 고름 · 같은 step 메시 재반입 → exact 130/130,
  웹앱 규약 porosity 중앙 **9.89 %**.  남은 결함 = LHS-10 (바닥) — 수확기 수정 비준 대기.
- ✅ J13 수확기 수정 (비준): 벽 기준 분모 + 벽 아래 거부 · `latest_le` 폐지 · 교차검사 SAME 강제 (셋 다 빨간불 먼저).  다음 = WSL 130 재수확.
- ⛔ J14 재수확 72/130 — 58 건 거부는 J13 가드 (½·r_max) 가 벽과의 **깊은 겹침** 연속 분포를 자른 것 (d ∝ 최대 AM 반지름,
  corr 0.877) · 예외 4 건 (056 · 079 · 107 · 110) 은 같은 깊이 1.98008 µm = 벽 관통 의심.  권고 = 덱 zplane 직접 확인 + 벽 아래는
  기록만 (비준 대기).
- ✅ J14 비준 (09-24 "ㅇㅇ 비준해줘") · 구현: 가드 삭제 · `check_deck_floor` (CLI `--deck` 필수) · `wall_record` (벽 밖 부피 · 관통 수 ·
  가장 깊은 입자 · (나) 되돌려 놓은 두께/porosity) · 배치가 덱 전달·sha 대조 · 교차검사 칸 (빨간불 12 · 4 · 4 → 초록).  원장 `LHS-12` · `LHS-13`.
- J15 웹앱 porosity 점검 — 식은 완성형, 입력 검사는 비어 있다 (메시 step 불일치 무검사 · 재계산 점검 한쪽만 · 무메시 fallback 등) → `SELF-47~49`.
  Codex 리뷰는 재수확 실측을 붙여서.  다음 = WSL 130 재수확.
- ✅ J16 재수확 130/130 (`4ee1038c3`, WSL) — 교차검사 SAME 130 · exact 130 · 덱 바닥 0 130 → `docs/data/lhs_descriptors_20260924/` ·
  LHS-10 · 11 · 12 claimed_fixed.  새로: 바닥 벽 재질 SE (`LHS-14`) · 음수 ε_sphere 18 건 (`LHS-15`, J6).  다음 = Codex 리뷰 패키지.
- J17 바닥 SE 는 **의도** (사용자: 양극 밑 SE 분리막 · 위 SUS 플런저) → `LHS-14` wontfix · (가) = LHS 고유 · (나) ≈ 단단한 바닥 (생산 덱 비교용, 가설).
  Codex 요청서 `docs/reviews/codex_request_lhs_porosity_thickness_20260924.md` (Q1–Q7).  인계표는 판정까지 보류.
- ✅ Codex 판정 수신 (09-25) → `codex_verdict_lhs_porosity_thickness_20260924.md` 보존 · 원장 `HND-01~06` · J18.  (나) ≈ hard-bottom **철회** ·
  1.98 자리 = 바닥 평면 아래쪽 점착 평형 (q 3 · φf 0.01, 내가 재계산해 6 자리 일치) · 인계 생성기가 벽 QC 를 버리고 음수를 OK 로 냄 (HND-04).
  실행 계획 A–E 비준 대기.  ✅ E: LHS 덱 m6·m7·m8 = 생산 덱 (사용자 grep) → 1.98 기전 재현됨 (조건부).
- ✅ 비준 → A · B · C 구현 (수확기 20 · 생성기 3 빨간불 먼저): STL 평판 검사 · 덱 활성 벽 (fix/unfix · group · 흐름 제어) · cap 깊이 ≠ 접촉 겹침 ·
  상별 cap · (다) clipped · 적격성 (HOLD 코드) · `handover_qc` · τ 벽 밴드 진단 · 생성기 QC 열 46 개 + 기본 스냅샷 09-24.  다음 = WSL 재수확 v2 → 인계표.

## ⑪ Methods SI 표 리뷰 (강준희 09-25) → 출처 정리 · VGCF E 민감도 (비준)
- 다섯 항목 판정: NCM σ_e 1e-2 = 코퍼스 끝점 (문헌: Wang 2018 JPS 393 75 pristine 811 ~4e-3 · Amin&Chiang 2016 SOC 밴드 → "Effective, Ref.") ·
  LPSCl ν 0.3 = Ref. (Cronk 2026 0.3 · Bazzoun 2026 0.37 · 우리 DFT 0.36) · VGCF Ø 0.15 = SEM 실측 있음 (이종기술, 원본 등재 대기) ·
  VGCF E 10 = 미앵커 (Ozkan 2010 단섬유 180–245 GPa) · VGCF σ 100 = 분말급 유효값 (VGCF-H 0.012 Ω·cm = 83 S/cm · 단섬유 1e-4 Ω·cm).
- 관련 선행: 07-02 `--fibre-stiff` strut 극한 (+0.75 %p @4 wt%) · 생산 침대는 dilation 모드 (E=10 실제 사용) · E 스윕은 없었음.
- ✅ 사전등록 `vgcf_e_sensitivity_prereg_20260925.md` · `--add-e-override` 구현 (빨간불 11 → 초록 152/152).  다음 = kgy 3팔.
- 대기: WSL 재수확 v2 · SEM 직경 원본 · Wang 2018 / Endo 2001 / Ozkan 2010 PDF (정본 카드).
- ⚠ 위 첫 줄의 NCM σ_e *"→ Effective, Ref."* 는 **09-25 오후 §1 재검토로 대체** — `Assumed` 유지 + 각주 (문헌 범위 · CL-70 민감도).
  Wang 2018 수치는 원문 미확인 · 모델 논문의 5e-5 는 입력값이지 측정 아님 · 원고 메모 D14 정정 (커밋 `6caa7636d`,
  정본 `docs/reviews/si_table_response_20260925.md` §1).  사용자 결정 대기: A (Assumed + 각주 + SI 그림) vs B (문헌값으로 전 팔 재실행).
  ⚠ LPSCl ν *"= Ref."* 도 §2 에서 같은 기준 (측정인가 · 모델 입력인가) 으로 다시 본다 — 09-03 원고 검토는 관례값이라 `Assumed` 로 정했다.
- ✅ **Wang 2018 원문 확인 (09-25 밤)** — 정본 카드 `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` (canon `35b481d0d`, 그림 20 장 크롭·육안 확인).
  NMC811 σ_e **4.1e-3 S/cm (20 °C, DC 분극)** = 우리 1e-2 의 1/2.4 · **5e-5 는 원문에 없다** (Zhang 2023 귀속 불성립) · 같은 NMC532 에서
  Wang ↔ Amin&Chiang **~3 자릿수** 산포 · 이 논문 σ_i 는 인용 금지.  §1 각주에 S(new2) 투입 · 답변 초안 갱신 · D14 정정.
  결정 A/B 는 **여전히 사용자 대기** (권장 A 유지).  zhang2023 · aminchiang2016 카드 정정 주석은 비준 대기.
- ⛔ **SI Table S2 참고문헌 사고 (09-25 밤, 원장 `SELF-51`)** — 준희: NCM811 E 의 출처 (docx `Ref. S4`) 가 검색되지 않는다 → 확인 결과
  **이 리포가 만든 인용** ("Wang 2020, JPS 470, 228413" — 인용 금지 `CL-90` · 04-29 주석에서 확인 없이 생겨 08-24 원고에서 제목까지 붙음).  ~~`Ref. S5` (Cronau 2021)
  도 오귀속 (3.0 mS/cm 이 원문에 없다).  ⇒ 표의 `Ref.` 두 행이 둘 다 틀렸다~~ (밤 철회 — S5 의 3.0 은 SI 그림 S2c 에 있다, `CL-91`; 아래 3단계)
  (값 140 GPa · 3.0 mS/cm 은 범위 안 — 재계산 불요).
  14 행 전수 재검토 = `docs/reviews/si_table_response_20260925.md` §7.  S4 교체 문헌 (사용자 제공): Sedlatschek *et al.*, JPS 681 (2026) 240276
  — PDF 확인 전 인용 금지.  "Wang 2020" 은 웹앱 툴팁 · 반박 노트 · 논문 초고에도 퍼져 있다 → 내부 서지 점검 + 원고 참고문헌 게이트 제안 (비준 대기).
  ✅ 1단계 커밋 `171934433` (Wang 2020 9곳 · CL-90 등록 · CLAUDE.md 규율 ⑥).  ✅ **σ_grain 3.0 의 뿌리** — ~~04-24 이전부터 출처 없이 존재
  (옛 주석은 1.3 mS/cm)~~ (⛔ 밤 정정: 04-24 이관 문서 `GB_correction_fitting_report.md` 가 3.0 을 **자체 MLIP-MD** (UMA · 300 K 완전결정 ·
  원자료 리포에 없음) 로 적고 참고문헌 목록에 Kraft 2017 을 붙였다 — 1.3 은 펠릿값) → 04-29 `0a040f2b0` *"Sakuda 2013 … single-crystal
  ultrasonic"* → 04-30 `ceee1d812` 가 입자크기 계수에만 "Cronau 2022" → **05-28 `38931e3e7`·`b20930e74` 가 기준값까지 단결정 라벨로 넓힘**.
  ~~Cronau 2021 원문엔 3.0·단결정 없음 (Li₆PS₅Br)~~ (밤 철회 — SI 그림 S2c 에 µC-Li₆PS₅Cl 펠릿 평탄 2.88–3.46, 3.0 은 그 하단),
  Cronau 2022 는 Li₅.₅PS₄.₅Cl₁.₅ 연구 (원문 확인 — 구간값 없음).
  출처 표기 7 파일 정정 (값 불변) · 정본 카드 `d95bda929`.  ✅ **뿌리 감사 5 묶음** (에이전트: SE · AM · DEM · 카드값 · 코드상수) 완료
  — 사용자 비준 *"토큰 많이 들어도 되니 확실하게"*.  결과 목록은 아래 3단계와 다음 정정 묶음 (#46) 에서.
- ✅ **SELF-51 3단계 (09-25 밤) — σ_grain 3.0 은 Cronau 2021 SI 그림 S2c 의 µC-Li₆PS₅Cl 펠릿값이다** (원장 `CL-91`).  논문 에이전트 7 편
  원문 대조 — 정본 canon `729818f95` Cronau 2021 SI · `969a5f922` Cronau 2022 · `7d23f44d9` Sedlatschek 2026 · `eef51c83b` Xu 2017 ·
  `6d641f6cf` Ketter 2025 · `4c8d043c1` Endo 2001 · `ae22bf37b` Ohno 2020 SI (핵심 수치는 내가 PDF 로 재대조).
  - ⛔ 2단계의 *"Cronau 2021 에 3.0 없음 · Br 만 측정"* 철회 — 적층압 ≥146 MPa 평탄 2.88–3.46 mS/cm (판독), 3.0 은 그 하단 · 한 배치
    8 개 연구실 σ25 0.44–2.98 (Ohno SI Table S11, 3.0 = 최댓값 자리).  *단결정* 라벨은 인용 금지 등록 (8 패턴) — 스윕 32 패턴 × 2166 파일 누수 0.
  - Cronau(r_SE) 구간값은 Cronau 2022 원문에 없다 (σ 는 입경이 아니라 밀링 손상을 따른다) → 출처 없는 모델 가정 (값 불변 · 폼 변경은 저자 결정).
  - 표 S2: S4 → Sedlatschek (**140 · Ref. S4 그대로** — 측정 138 ± 24 안, 사용자 결정 09-25 밤; 내 *"140 (S4) 금지"* 는 과해서 철회) · S5 유지 + 각주 · 준희 4 건 ᵃ ᶜ ᵈ 문헌값 확정 (Ketter NCM83 5.22 mS/cm ·
    Deng ν 0.37 · Endo 단섬유 1e4 / 0.8 g cm⁻³ 분말 ≈80 S/cm) — `si_table_response_20260925.md` §7 · §8 · §8-2.
  - ⬜ 새로 드러난 것 (저자 결정): **K_IC(AM_P) 0.3 = Xu 2017 의 소결 펠릿값** (2차입자 0.10 → P_c 1/8.7 → β_F · β_Fe — ③ 후보, 민감도
    {0.10, 0.30} 권고) · `am_load_balance_jam.py` 의 *"NCM811 압입 경도 문헌대 3~6 GPa"* 출처 없음 (NMC532 나노압입 H 8.6 ± 1.3) ·
    κ_SE 0.7 = Ketter 의 **NCM83** 값 (LPSCl 은 0.32) + 지어진 서지 · CL-81 전제 (입력 σ = 펠릿) · 순수 SE 공극 10 % 는 Ohno 연구실 간
    13 ± 5 % 안 (③ 후보에서 완화).
- VGCF E 3 팔 압밀 완주 (kgy): porosity 14.749 · 14.889 · 14.929 % (1 → 100 GPa Δ +0.180 %p ≤ 0.3 ⇒ porosity 축 통과) · E=10 이 Phase A
  재생성값과 동일 · STEP3 (vox 0.15) 진행 중 — 정본 사전등록 §7 (등록 결함: 지표 이름 · E=100 dt 비대칭 · 운영 사고 셋 기록).
- ✅ **VGCF E 민감도 판정 = h0 "2차 입력"** (09-25 19:38 STEP3 완주): σ_e 59.274 · 59.154 · 59.303 mS/cm (1 ↔ 100 GPa Δ 0.05 %, 팔마다
  ≤ 0.25 %) · porosity Δ 0.18 %p — 둘 다 판정선 안.  원자료 `docs/data/vgcf_e_sensitivity_20260925/` · 사전등록 §7-3 · 원장 `SELF-50`
  (metrics `dt` 가 요청값) · 준희 대응 §4 정리 (원고 반영 비준 대기).
- LHS: 130 재수확 v2 + lhsx 64 수확 tgz 수신 (SAME 130 / 64 · 바닥 틈 0).  ⚠ lhsx porosity 중앙 −4.26 % (음수 과반, 130 건은 9.89 %) —
  준희 건 뒤 LHS 트랙 첫 항목.  스냅샷 커밋도 그때.


## ⑫ 인용 뿌리 감사 4단계 · 준희 종합 회신 (09-26)
- 사용자: *"논문에이전트 마무리하고 준희 얘기 대응하자 다 종합해서 · 코드 전수조사"* → 정직 답: 조사는 **전수가 아니었다** (카드 없는 인용 64 %, 형식 사각
  미조사) → 감사 F (247 키 전부) · G (형식 사각 457 줄 · 원고 참고문헌 전부) 로 메움.  종합 = `docs/reviews/citation_root_audit_20260925.md`
  (+ 원문 사본 디렉터리).  남은 사각: 19 키 (느슨한 집계) · 사용자 docx 원본 · 인벤토리 밖 비원고 키 일부.
- 논문 카드 5 편 원문 재대조 ✅ — Sharma (E_AM 140 · ν 0.25 = NMC622 단결정 VRH 140.16 · 0.253) · Stallard (K_IC 0.05–0.3 추정) · Wheatcroft
  (평판 207 · 원뿔 67 MPa) · Shi SI ("1/3" = LPS 유리 1.5 µm) · Böger SI (치밀 LPSCl κ 0.71/0.65).  새 논문 Zhang 2026 XCT-DEM 은 에이전트 진행.
- 준희 회신 최종판 = `docs/reviews/si_table_response_20260925.md` **§9** (표 S2 전 행 · 각주 ᵃ–ⁱ · Methods 두 문장 · 표 각주 ※ (M) ·
  "experimental porosity anchor" 확인 · SI 참고문헌 · 회신문).  `main.tex` σ_grain 잔재 1 문장 정정 (3단계가 놓침).
- ⬜ 사용자 결정: §9-5 여덟 항목 · 종합 §4.  ⬜ 정정 묶음 1–11.

## ⑬ 믹서 L 10 런 재개 도구 (09-26 저녁)
- 18:02–18:07 WSL 이 죽었다 18:27 재부팅 → L 10 런 53–61 % 에서 끊김 (체크포인트 a/b 27–29 MB 온전, 최신 = a 9 · b 1).
- `FORCE=1` 은 처음부터 (런당 4 일 넘게 손실 — 옛 표기 "~3 일" 은 과소) → 체크포인트 재개 도구: `scripts/make_mixer_resume.py` (selftest) · `resume_all.sh` (SMOKE/DRY/발사) ·
  `test_launcher.sh` R①–R③c.  사용자 순서: git pull → SMOKE=L0_s32452843 → DRY=1 → 발사.  prereg §3 2b 에 실행 기록.
- **발사 (09-26 밤)** — 스모크 통과 뒤 `MAXJ=10` 으로 10 런 재개.  `RESUME_STEP` **10/10 = 영수증** `checkpoint_step`: L0 5.8 M · LC_s67867967 5.6 M
  (b 가 더 새 것) · LB3 5.0 M · 나머지 7 런 5.4 M (prereg §3 2b).  ✅ **19:19 watch: 10/10 `실행` · step = 체크포인트 + 5,000** (첫 thermo 줄).
  잃은 계산 (로그 mtime − 체크포인트 mtime) 은 런당 6 분 (L0) ~ 3.5 h (LC_s32452843).  메모리 used 2.4 GiB / 15 GiB — 10 런 합 ≲ 1.7 GB.
- ⚠ **19:24 10 런 다시 정지** (체크포인트 뒤 8–10 k step, 로그 끝 = run 종료 통계 — 외부 원인, 사용자 확인) → 재재개 전 점검 한 블록 (LIGGGHTS 떠 있으면 멈춤 ·
  a/b 가 재개 뒤 새로 쓰였으면 멈춤 · 첫 재개 영수증을 `resume_receipt.first.json` 로 보존) → **19:38 10/10 실행**, 첫 줄 step = 체크포인트 (같은 5.0–5.8 M).
  첫 재개 구간 (~10 분) 은 버림 — 그 구간의 체크포인트 뒤 덤프는 `post_pre_resume_<ckpt>_2/` 로 (L0 128 → 127).  prereg §3 2b.

## ⑭ dem-web / 500 — WSL 크래시로 잘린 meta.json (09-26 저녁)
- uploads/260925_000001_0bee25 (0 B) · 260925_000448_bd85f9 (반쪽) — mtime 18:09·18:10, 권한 0600 = 전날 원자적 쓰기로 만든 파일을
  제자리 `open(…,'w')` 가 잘랐다는 흔적.  사용자가 `.broken_20260926` 로 옮기고 복구 (bd85f9 앞부분 12 키 · 0bee25 는 bd85f9 틀로 재구성, 원래 이름 미상).
- 코드: `list_cases` 가 깨진 meta.json 을 건너뛰고 status `meta_broken` 로 표시 · meta.json 쓰기 7 곳을 `_ps.atomic_write_json`
  (temp→fsync→replace) 으로 · 회귀 `webapp/test_meta_json_robust.py` (옛 판 6 FAIL 재현 → 8/8) · check_all · CI 배선.
- ⚠ **내 재구성 결함 (사용자 지적 "왜 bimodal 뜨지?")** — 0bee25 meta 를 bd85f9 (ps_3_7) 틀로 만들며 **`mode: bimodal` · `type_map 1:AM_P,2:AM_S,3:SE` 까지 복사**했다.
  0bee25 는 ps_0_10 = **AM_S (D4) 단일** (사용자 확인) → 업로드 규칙 (detect_mode: 덤프 타입 수 ≥ 3 → bimodal · `type_map_resolve` 덱+덤프) 으로 다시 읽으면
  **standard · 2:AM_S,3:SE** (repo 덱 `in.ps_0_10_r45.liggghts` 로 확인 — 덱이 선언한 AM_P 는 원자 0 개라 뺀다).  기존 결과는 무영향 (type 1 원자가 없어 상 라벨이 같다) ·
  재분석 경로와 그룹비교 `mode` 열엔 영향.  고침 명령 첫 시도는 system `python3` 에 numpy 가 없어 판독 단계에서 멈췄다 (meta 무변경) → venv python 으로 재시도.
  교훈: 틀에서 복사할 때 **케이스마다 다른 키** (mode · type_map · status) 는 그 케이스 자신의 파일에서 다시 읽는다.
- ✅ **0bee25 고침 완료** (venv python): 덤프 AM_S 4,588 · SE 158,760 (덱 표 4,584 · 158,765 — `volumefraction_region` 삽입이라 개수는 표본 요동, 부분 삽입 흔적 없음)
  → **standard · 2:AM_S,3:SE**.  결과 폴더 둘 다 **✓ 온전** (0 B · 깨진 JSON · 끝줄 잘린 CSV 없음) · 마지막 수정 09-25 00:16 / 01:01 ⇒ 크래시 때 이 두 케이스의
  **분석은 돌고 있지 않았다** (18:09 · 18:10 에 쓰인 것은 meta.json 뿐).  ⇒ 채팅에서 낸 가설 *"웹앱 분석 + 믹서 10 런이 메모리를 바닥냈다"* 는 근거를 잃었다
  (믹서 10 런 ≲ 1.7 GB) — WSL 이 죽은 원인은 **미상**.


## ⑮ NCM 전자전도도 — 비준 3 건 실행 (09-26 밤)
- 보고: NCM σ_e 는 **솔버마다 다른 값**이다 — STEP3 복셀 (SDCP 원고 표 S2) 1.0 × 10⁻² S/cm (결정 6 = A 진행) ‖ DEM 접촉망 50 mS/cm (출처 없음).
- 비준 (사용자, 09-26 밤): ① DEM σ_AM = **A** ② SI 그림 지금 리포 기본 형식 ③ 정본 카드 2장 정정 주석.
- ① 값 50 유지 (재계산 없음) · 틀린 라벨 8 파일 정정 (코드 주석 · 웹앱 툴팁 · 보고서 생성기와 생성본 3 · CLAUDE.md · main.tex) ·
  ⚠ `scripts/network_conductivity.py` 의 주석은 **되돌렸다** — S3 봉인 수치 모듈이라 주석 한 줄도 바이트 지문을 바꿔 봉인된 S3 실런을 거부시킨다
  (게이트의 봉인 selftest 가 잡았다).  정정은 S3 실런 (L2-01) 뒤 · 그 파일만 인용 금지 allowed_in ·
  등급 엔진 ASR_electronic 설명에 한정어 (절대 문턱 — σ_AM 기준 위에서만 뜻) · 원장 `CL-92` (convention) + 인용 금지 5 · 08-25 진행 파일 2 줄 표지.
  스윕 37 × 2176 누수 0 · 방법론 규율 0 오류 (게이트 전 단독 실행).
- ② `scripts/plot_sigma_closure_3x3.py` → `docs/figures/sigma_closure_3x3.png` (+ svg · csv · Origin csv).  원장 CL-70 에서 읽고 9 칸 검산 ·
  selftest 9/9 (음성 대조 3) · 재실행 바이트 동일 (svg 날짜·id 고정) · 인벤토리 등재.  캡션 제안 = si_table_response §1 ④-2.
- ③ canon `d1e64f0a1` — zhang2023 (+9 줄) · aminchiang2016 (+6 줄) 맨 위 정정 주석, 본문 불변.  근거 = wang2018 카드 §3-4 (canon 35b481d0d).
- 남음: 각주 · Methods 문장 · SI 그림의 docx 반영 (사용자) · PLAN 정정 묶음의 나머지 · 19 키 미판정.
- ✅ **최종 (09-26 밤, 사용자 결정)**: 표 S2 3 행 = `1.0 × 10⁻² S cm⁻¹ · Ref. [S(Amin)]` — Amin & Chiang 2016 초록 *"∼10⁻² S cm⁻¹"* (충전 상태).
  긴 각주 ᵇ · Methods 문장은 쓰지 않는다.  준희 답 1) 한 줄로 교체 (si_table_response §9-6).  ⛔ "4.1e-3 / 5e-3 으로 돌렸다" 류 기재는 거절 — 실제 입력은 1.0e-2 (런 기록 AM_S 0.01, AM_P 상 없음).

## ⑯ SI 표 S2 — ν · VGCF σ · VGCF E (09-26 밤)
- ✅ **사용자 결정**: #6 LPSCl ν 0.3 → `Ref. [S(Cronk)]` (Cronk 2026 SI Table S6 — 그 논문의 FEM 입력값, *측정* 이라 쓰지 않는다) ·
  #13 VGCF σ 100 S/cm → `Ref. [S(Endo)] (compressed powder)` (Endo 2001 Fig. 8 흑연화 VGCF 압분체 곡선이 100 을 지난다, ≈0.92 g/cm³ 판독).
  각주 ᵈ · ʰ 삭제 · SI 참고문헌 Cronk 추가 · Wang / Ketter 제외 (ᵇ 미사용) · 준희 답 2) · 4) 교체 (`si_table_response` §9).
- #12 VGCF E 10 GPa — 정본 Lawrence 2008 카드 (canon `0d0c54109`, PDF 직접 대조): 17 가닥 6–207 GPa · 10 GPa 근처 가닥 없음 (6 · 13) ·
  D ≤ 200 nm 9 가닥 23–207 ⇒ 10 GPa 의 출처로 걸 수 없다.  추가 탐색 두 갈래 (CNF · CVD 나노튜브 / 횡방향 탄성률 · 전극 모델 입력값) 도
  없음 (출판사 접근 차단 — 검색 요약 수준).  ⇒ 원장 **`CL-93`**: 10 GPa = 06-24 `862a61833` 모델 선택값 · 원고 침대 전부 이 값 ·
  다른 값을 입력값으로 적으려면 재압밀 · 재계산이 먼저.  각주 ᵍ 없음 · 표 칸은 저자 결정 (§9-5 ⑨).
- σ_e 가 E 에 따라 조금 움직인 이유 (사용자 질문): STEP3 σ_VGCF 는 세 팔 동일 — E 는 MPM 압밀 기하만 바꾼다.  E=100 은 CFL 로
  dt 1.347e-4 → 플래튼 걸음 0.046 µm 라 정지 위치 양자화가 달랐다 (10 → 100 차이 +0.057 µm · +0.04 %p = 한 걸음 크기).
  팔 간 σ_e 차이 ≤ 0.25 % < origin 위상 산포 0.68 % ⇒ 순서는 해석하지 않는다 (prereg §7-3).
- 에이전트 보고 정정: CL-33 금지 패턴이 쪽 범위 표기에 걸린다는 오탐은 우리 스윕 (부분문자열 비교) 에서 재현되지 않는다 — 결함 아님.
- ✅ **기본값 VGCF 100 GPa 로 고정** (사용자: *"앞으로 잘못 안 넣게 100 GPa 로 고정"*) — `mpm3d_compaction.py` ADD_E_NU · 새 세대 `ADD_E_SET_20260926`
  (태그 `ADD_E_SET_20260926_VGCF100GPa`) · selftest 153/153 · 정본 서술 `docs/sdcp_manuscript_anchors.md` ★ADD_E_SET · 원장 `CL-93`.
  이미 돌린 결과는 그대로 (재실행 없음).  이 세대는 CFL dt 가 약 0.67 배 — 두꺼운 침대는 목표 도달 확인.

## ⑰ DFT 5차 회신 최종판 수신 — Ag|그래핀 W (09-26 밤)
- 📨 받은 것: (a)(b) 수용 · **SE 계면 (i) 기준선 없음 확정** (LPSCl|Ag 소모델 프로브 89–109 GB > 48 GB; 예비판 ≈ 246 GB 추정의 하향) ·
  Ag(111)|그래핀 **W_sep 0.435 J/m² (8 Å · 끝점 검사 미통과 라벨) / 0.449 (10 Å)** · PBE+D3(BJ) 조건부 · k 축 수치 미검증 · (iv) PBE 단독 −0.055.
- ✅ 정본 결과 파일 (db/properties/wad_aprime_pilot_result_v2_2026_09_26.json) 로 직접 대조 — registry 4 값 0.4351–0.4355 · ΔD3 0.4905 ·
  G3 FAIL (직접 8→10 Å +0.0136) · G4 k INCOMPLETE 전부 일치.  우리 환산 73 meV/C → 0.4347 J/m² ✓.
- ✅ **사용자 결정 (09-26 밤): SE 쌍 = H (보류)** — DEM 회신 5 비준 · 1저자 발송.  읽기 · 발송문 = `docs/dft_reply5_adhesion_20260926.md` §3.
  결정 뒤 3 단 (DEM 박리) 은 질문 ② 기하 (Ag–C ↔ VGCF 호스트) 부터 · 탄소–탄소 쌍 w 는 문헌 카드 몫.
- 📨 **6차 회신 (09-26 밤)**: 48 GB 안에 드는 SE 소모델 **없음** (Ag 2 층 · 가벼운 퍼텐셜로도 ≈ 61 GB) → SE 쌍 보류 **확정**.  기록 = 같은 파일 §5.

## ⑱ 일괄 런 사전등록 — Phase A 재현 (100 GPa) · ps45 d_h 전이 · d_h 288 (09-26 밤)
- ✅ 사용자 결정: 104 팔 전부 100 GPa 재현 + 같은 기계 10 GPa 대조 32 팔 (짝 비교) · ps45 5 침대 MPM (동결선 288/φ0.75) · d_h 288 8 런 · v100 분담.
- 사전등록 2 건: `docs/reviews/phase_a_replication_vgcf100_prereg_20260926.md` (P1–P5 · 판정선 §4 · kgy 명령 §6 · ≈ 90 GPU-h) ·
  `docs/reviews/ps45_dh_transfer_prereg_20260926.md` (동결선 `docs/data/dh_frozen_288_phi075_20260926.json`: a −0.68317 · b −0.57533 · sd 0.07671 ·
  띠 ±2 sd · TRANSFERS/PARTIAL/FAILS/HOLD · v100 명령 §5).  d_h 288 은 verdict §⑩ (08-11) 그대로.
- 도구 신설 (런 전): `scripts/phase_a_pair_e_arms.py` (짝 비교 · selftest 14/14) · `scripts/score_dh_transfer.py` (동결선 채점 · 12/12) ·
  `fit_dh_collapse.py --freeze-json` (+selftest 12).  SELF-50 → claimed_fixed `248fd9516`.
- 레시피 근거 (에이전트 2 · 파일:행 전수, 스크래치 보존): 원판 STEP2 = 킷 run_mpm.sh K:77,88-94 · STEP3 러너 LEAN=2 centerline 0.24 · physics_protocol_id
  p2-79ade1a5c2b0c9fb · 재압밀 잡음 실측 +0.064 % (kgy E=10 vs v100 원판 3_1 v015 o0) ⇒ 대조군 필요 · d_h 288 ≈ 15 GB (kgy 캡 = min(85 % 총, 90 % 여유)).
- ⚠ 자기매칭 함정 재발 (게이트 런처 명령줄의 "bash scripts/check_all.sh" 를 같은 명령의 kill 루프가 잡아 자살, exit 144) → 런처는 변수 (`G=scripts/check_all; bash "$G.sh"`).

## ⑲ LHS porosity — sphere vs union 전수 · 순수 SE 판정 시험 등록 · Phase A STEP2 통과 (09-27)
- lhsx 64 의 음수 porosity (중앙 −4.26 %) = **SE–SE 겹침 이중계상** (확정 · 판단 J19).  수확 · 덱 결함 아님.  에이전트 진단 + 내 독립 검산 일치.
- 194 건 union 실측 (WSL · `scripts/lhs_union_webapp.py` — 웹앱 함수 + 정확한 MC union): 전부 양수 · 정확 union 중앙 130 **13.60 %** · lhsx **6.55 %** ·
  쌍 렌즈 + 벽 밖 제거 ≈ 정확 (0.004 %p) → `docs/data/lhs_union_20260927/`.  스냅샷 `docs/data/lhs_descriptors_20260925/` · `lhsx_descriptors_20260925/` 커밋.
- 사용자 지적: 복합체 < 순수 SE 는 이원 충전 물리 → 내 "과압축" 표현 철회.  순수 SE 판정 시험 사전등록 `docs/reviews/pure_se_union_prereg_20260927.md`
  (4 침대 · `lhs_ext_materialize.py --pure-se` 신설 · selftest 42/42 · 판정선 Q1–Q3).
- ⚠ 실험 앵커 정정 `SELF-52`: *"Minnmann 순수 SE 10 %"* 는 보정 표적 — 실측 띠 8–19 % (Ohno 2020 등, 정본 카드).  내가 대화에서 되풀이했다.
- Phase A 재현: kgy STEP2 8 침대 통과 (P4 · P5 ✓ · G010 = v100 원판 porosity 소수 셋째 자리까지) · STEP3 는 심링크 경로로 규율 검사 정지 → 실경로로 재발사 (10:10) —
  사전등록 §6 덧붙임에 기록.  v100 d_h 288 3/8 (런당 ≈ 3 h).
- litdb: Franco 랩 프리프린트 2 편 (탄소펠트 섬유 DEM · 이중층 후막 공정) 에이전트 진행 중.

## ⑳ litdb 두 편 정리 · 믹서 중간 M(t) 열람 · 순수 SE 제출 정상화 (09-27 낮)

- litdb (정본 `967bc08c4`): Qin 2026 · Sankar 2026 카드 (`d96e0efa9` · `c29669694`) 의 인덱스 · 비교표 · 출처표 정리.  Qin 카드 수치는 PDF 본문과 전부 일치.
  `extract_figures.py` 결함 — `--clean` 가드가 src 만 봐서 손 크롭 (qin f8) 이 지워질 수 있었고 `--inbox --run` · `--refresh --apply` 는 가드가 없었다
  → `handwork_if_cleaned` · `clean_blockers` 로 세 경로 모두 막음 (selftest 64/64, 실제 폴더로 세 경로 확인).
- LHS 130 대조 (빠른 점검): Qin 의 "같은 φ_AM" 규칙은 우리 DEM 에 안 옮겨진다 — AM-rich 에서도 φ_AM 이 SE 비율을 따라 준다 (기울기 −0.35 ± 0.03, n = 68).
  옮기는 것은 같은 응력 영모형 하나.  비교표 §A 에 '빠른 점검' 으로 적음.
- 믹서: M 첫 열람 **12:14 KST** (결정 커밋 `392bc860e` 뒤) · 곡선 = devlog v09 · 원자료 `docs/data/mixer_interim_20260927/`.  10 런 전부 1.5 바퀴 안에 평탄 ·
  주판정 칸 16×16×4 바퀴 4 구간 시드별 LC − LA = +0.008 · +0.013 · −0.007 · **판정 아님** (첫 판 그림이 8×8×2 를 판정 칸이라 적은 것은 정정 — `5fb05294f`).
  고-Bo AM–AM 팔 (LH, Bo_code ≈ 38.4) 추가는 **Codex 리뷰 뒤** (`docs/reviews/codex_mixer_highbo_request_20260927.md`).
- 순수 SE: 제출 ①②③ 실패 (러너 짝 · 생성기가 AM 템플릿 삭제 · 내 ③ 처방도 틀림) → 외부 검토 생성기로 교체 · SELF-53 · 사전등록 §3 정정 (런 전) ·
  네 번째 제출 231946–49 정상 (3 by 5 by 1 · 삽입 139,706 / 41,394 / 17,463 / 17,463).

## ㉑ 고-Bo 믹서 LH — Codex HOLD 해제조건 반영 (09-27 오후, 발사 전)

- Codex 판정 = **HOLD** (`docs/reviews/codex_mixer_highbo_verdict_20260927.md`, 원장 HB-01~05).  저자 결정 (사용자): **B 먼저** (현 규약 = AM–AM + AM–벽 공동 개입, Bo_code 38.4 = 내부 탐색값) → 차이가 크면 **조건부 A** (AM–AM 단독).
- 재현 시험 먼저 → 수정: `check_contact_validity.py --contract` (옛 모드가 δ/r 2 % 를 통과시키는 것 재현 → 창 전 프레임 · 39 각형 드럼 벽 회전각 반영 + 데이터로 되읽기 · 끝판 · 상별 보존 · 19/19) ·
  `measure_mixing_index.py` (버린 칸이 분리를 숨기는 S² 0 반례 재현 → 상별 유지 부피 · 전 칸 M · 등록 최종값 `planned` = bin 7 25 프레임 · 16/16) ·
  `mixer_deck_diff.py` 신설 (실행 덱 LC → LH 는 허용 다섯 쌍만 · 7/7) · 생성기 `LH` 팔 · LA/LC 설명 정정 (주석 한 줄 — ㉟b) · `gen_all.sh SET=highbo` · 런처 시험 31/31.
- 문서: `docs/reviews/mixer_highbo_prereg_20260927.md` (지위 = 중간 열람 후 설계한 탐색 확장) · 본 캠페인 사전등록 §0 R-3 · R-4 정정 (LA Bo_po **0.444**, ≈ 0.23 철회) · §1 팔 · 계약 행 정정 ·
  §5 결론 문안 (§2 판정선 불변) · v01–v08 세대 표지 · v09 대리 한정어 · 그림 범례 두 줄.
- ⬜ 저자 결정 **D-1** (접촉 계약 1 % 해석 — 09-21 자가 리뷰 충돌 겹침 추정 SE–SE 1.03 % 가 이미 문턱 위) · D-2 (상 대표성 0.90) · D-3 (A 발동 = 큰 차이) · D-4 (스모크 = 생산 첫 시드 bin 0).
  **실데이터에 검사기를 돌리기 전에** 정한다.  그다음 Codex 재리뷰 → L 완주 뒤 발사.
- ✅ 커밋 `6963632a0` (게이트 s25 통과) · 원장 HB-01~04 claimed_fixed (HB-05 는 D-1 전까지 open) · Codex 재리뷰 요청서 `docs/reviews/codex_mixer_highbo_rereview_request_20260927.md` (스냅샷 `6963632a0`, K1–K7).

## ㉒ 순수 SE — r100 두 침대 중간 열람 (2/4) · 남은 두 런 30 MPI 재발사 (09-27 오후)

- r100_a · r100_b 완주 (ERROR 0 · 0.30 도달 뒤 판 고정 이완).  사용자: 남은 둘 멈추고 30 MPI — 결정은 r100 값 전 (`ab745b552`).  재생성 diff = 러너 두 줄뿐 · 새 잡 232358 · 232359 (30 CPU).
- 첫 열람 14:16 KST · tgz sha256 `e71b93b0…` · 원자료 `docs/data/pure_se_r100_20260927/`.  **내부 정확 union 5.815 · 5.768 %** · 잡음 행 0.047 %p · δ/d 0.112 · 배위수 11.67.
  ⛔ Q1 (네 침대 중앙) 은 아직 없다 — 산술: 중앙 ≥ 6.0 % 이려면 r050 · r075 가 둘 다 ≥ 6.19 %.
- ⚠ 러너 `--output=logs/…` 는 제출 폴더 기준 — 케이스 폴더에서 sbatch 했으므로 그 안에 `logs/` 필요 (PENDING 중 mkdir 안내).  CLAUDE.md 에 두 PC 다운로드 경로.
- ⛔ **사고 (원장 `SELF-54`)**: 232358/59 는 `logs/` 부재로 0 초 FAILED (내 지시) · 232384/85 는 **체크포인트 확인 없이 INSERTING 부터** 재발사 → 사용자 취소.  지시문의 두 전제 ("체크포인트는 PHASE 3 에서만" · "재개 첫 thermo 줄 압력 대조") 둘 다 틀림 (선배 세션 지적).
  ✅ 선배 세션이 체크포인트에서 이었다 — r050_a after_settling 200001 → job 233797 · r075_a compress 1500000 → job 233799 (30 MPI · G1/G2/G3).  표준 절차 `docs/resume_ckpt_procedure_20260927.md` + `scripts/resume_ckpt.sh` · `ckpt_watch.sh` · CLAUDE.md 체크리스트 (`2354ff8d7` · `643e32422` · `1b8ef7f67`).
- **22:07 r075_a 완주** (30 MPI · 3,285,000) → 22:2x 결정: 추출 + r050_a 는 60 MPI 로 다시 잇기 (212 k step/h 라) — 명령 = resume_ckpt.sh (사용자 실행).  **22:4x 3/4 열람** (`docs/data/pure_se_r075_20260927/` · prereg §6-0c):
  내부 정확 union **6.549 %** (r100 5.815 · 5.768) · Q1 산술 ⇒ r050 ≥ 6.185 % 이면 중앙 ≥ 6.0.  판정 없음.
- **22:41 r050_a 60 MPI 재개 (`resume_ckpt.sh` 첫 실전, 사용자 실행)**: compress 650000 · 시험 job 233923 · G1 · G2 통과 · **G3 실패** (압력 0 → KE 대체: 원 6.22e-10 vs 재개 7.65e-11 —
  원 로그의 `run 5000` 경계 KE 톱니 ×6.5–6.7 위의 비교 · 왜 튀는지는 모름) → 도구는 본 제출 안 함 → 사용자 결정 (내 권고) **본 job 233951** (60 MPI · PD).  문턱은 안 바꿈.  사유 · 본 런에서 볼 것 ①–③ = prereg §6-0.

## ㉓ 고-Bo 믹서 LH — Codex 재리뷰 = HOLD (09-27 저녁)

- 판정 (`docs/reviews/codex_mixer_highbo_rereview_verdict_20260927.md`, 스냅샷 `6963632a0`): ① 부분 · ② 닫힘 · ③ 부분 · ④ 열림 · HB-01 부분.  B 공동 개입 · 38.4 내부 탐색값은 수용; 막힌 곳은 **검사 · 판독 경로**.
- 합성 반례 8 건 (HBR2-01 ~ 08) 을 **HEAD `643e32422` 에서 전부 재현** (프로브 assert 7/7 · `docs/reviews/codex_mixer_highbo_rereview_evidence_20260927/`): 벽 위상 되읽기 = 겹침 최소화 각도 (참 겹침 2 % → PASS · 5/5 ok / 참 위상 0.5 % → TECH) · 정상 bin 0 스모크 → 미완주 TECH · bin 6 이 2/25 프레임이어도 `flat=true` · 덱 비교기 비대칭/NaN/음수/헤더 PASS · 유지 0.98 인데 S²_keep 0 vs S²_all 0.2 · type 교환 + 반경 절반 PASS · 덤프 32 ms ≫ Hertz 22 µs.
- 원장: HBR2-01~08 등재 (P1 4 · P2 4) · HB-01 · 03 · 04 → open (잔여 명시) · HB-02 → verified (codex, `6963632a0`) · HB-05 open.  CLAUDE.md 믹서 행 · prereg §9 (K1–K5 조건) · §10 (재리뷰 결과).
- ✅ 비준 (사용자: *"권고하는걸로 해줘 ㅇㅇ · 결국에는 결과가 나오는 방향"*) → **같은 밤 수정**: 프로브 경우들을 셀프테스트로 옮겨 **먼저 실패** (검사기 3 · 판독기 KeyError · 비교기 5 + TypeError) 시킨 뒤 고침 —
  검사기 `--contract` 벽 근거 = `post_mesh/` 덤프 > `--phase-receipt` 영수증 > 상·하한 (되읽기 `--diag-fit` 진단만 · 관측량 = 저장 프레임 최대 · 창 계획 격자 결손 TECH · 헤더 · id 별 type/radius · `--expect-types`) ·
  판독기 (계획 덤프 격자로 bin 완전성 · `smoke`/`tech_smoke` 창 분리 · 상별 · 프레임별 유지율 · `qc_repr` D-2) · 비교기 (CED 머리 · 양측 유한 · 비음수 · 대칭 · 증가 방향 · `--expect-deck` · 예정 세 시드 n/N).
  셀프테스트 32/32 · 23/23 · 14/14 · 생성기 89/89 (LH 덱 · 골든 해시 불변 — 주석만 정정) · 런처 31/31.
  문서: prereg §2-4 · §3-2 · §5 · §6 · §8 · **§9 D-1~D-4 확정** · **§12 규칙 원장** (K7) · 본 캠페인 §1 계약 행 · §5 h0 라벨.
  ⚠ 실제 런 (L · LC · LH) 의 벽 판정은 **재개-위상 영수증** (WSL 에서 `mixer_restart_phase_test.py` 한 번) 이 있어야 나온다 — 면을 따라 깔린 침대는 근거 없이는 늘 unidentified 다.
  L 10 런은 계속 (Codex: 중단 · LC 폐기 · 재실행 · 1 % 완화 · 새 Bo/시드 **아님**).

## ㉔ 고-Bo 믹서 LH — 영수증 1차 실측 · Codex 3차 = HOLD (09-27 밤 ~ 09-28 새벽)

- **영수증 WSL 실행** (사용자): 세 번 막혔다 — system python3 에 numpy 없음 · `runs/` 축약 경로 · 0 입자 덱이 `write_restart` 에서 `Atom types must start from 1` (템플릿까지 뺐기 때문) → `04fe95ae8` (삽입만 뺌 · 셀프테스트 ① 을 먼저 실패시킨 뒤).
  네 번째 **통과** (09-28 00:0x): 오차 최대 2.0 × 10⁻⁵° · 리셋 가설과 6.353° · A↔B 꼭짓점 0 m · step 20000 · 25000 · 30000.  바이너리 배너 (compiled 2026-08-25-18:16:51 · 수정 시각 18:16:52) = `LC_s32452843/log.lmp` 첫 줄 ·
  덱 SHA `72b52c17…` = 생성기 `b6d9a2036` 산출과 바이트 동일 (현재 생성기와는 LC 설명 주석 한 줄만 다름).  기록 = `docs/data/mixer_phase_receipt_20260928/` — ⛔ 판정 경로 사용 보류 (아래 HBR3-01 · 02).
- **Codex 3차 (스냅샷 `20568797b`) = HOLD · 조건부 GO 도 없음** — HBR2 닫힘 4 (02 · 03 · 06 · 07 → verified, 한정어) · 부분 4 (01 · 04 · 05 · 08 → 재개방) · HB-01 · K7 부분 · 새 반례 HBR3-01 ~ 08 (원장 신설).
  합성 반례를 **HEAD `04fe95ae8` 에서 수치 505 개 전부 동일**하게 재현 (`docs/reviews/codex_mixer_highbo_rereview2_evidence_20260927/`) · ZIP 의 소스 사본 17 개 = `20568797b` blob 17/17.
  Codex 는 실제 캠페인에서 결함이 났다고 주장하지 않는다 · 문턱 · LC · Bo · seed 변경 요구 없음 · 최소 해제 목록 6 항 (판정문 §4).  ⬜ 수정 계획 = 사용자 비준 대기.
- ⚠ 내 실수 셋 (원장 `SELF-55`): 명령의 경로 · 인터프리터를 그 기계에서 확인하지 않았다 — WSL system python3 · `runs/` 축약 · v100 `~/dem-sk` (09-26 ps45 사전등록, v100 에 없음 · 배치 기본은 `/home/ubuntu/dem-stoic`).
- v100 eq288 (d_h 288 대등화 8 런) **완주** (09-27 22:57:40 · 8/8 EXIT 0 · 288 json 16 개) — 등록된 재적합 세 명령 (`fit_dh_collapse` `--list` · φ 0.75 · φ 0.72) 은 코드 경로 확인 뒤.
- ✅ **비준 ("비준") → 3 차 해제 목록 6 항 수정 (09-28 새벽)** — 반례를 셀프테스트로 먼저 실패시킨 뒤: 영수증 v1 (`mixer_restart_phase_test.py` 17/17 — 캠페인 step 구조 그대로 0 입자 ·
  캠페인 dump 간격 mesh 덤프 · B = `make_mixer_resume.transform` · 실행 직전 봉인 · 기대 step 정확 · 전체 메시 · B = A) · 검사기 55/55 (v1 엄격 소비 · 구간 극값 · mesh 덤프 완결 ·
  계획 t₀ · 프레임 스키마) · 판독기 32/32 (계획 t₀ · E0 t₀ · 격자 밖 · 중복 제외) · `validate_frame` (0.29 s/10 만 입자) · 덱 비교 24/24 (실제 seed 서명) · 런처 58/58
  (`launch_highbo.sh first/rest`) · v09 0.212 = Bo_code · PNG 확인 · prereg §2-2 · §2-3 세 층 · §2-4 · §2-5 · §8 · §12.  세 파일은 에이전트 병렬 (판독기 · 덱 비교 · 런처).
  ★ 발견: ε 를 0.05° 로 **가정**하면 면 가장자리 알 (+0.97 %p) 때문에 벽에 닿은 실제 침대가 전부 TECH — 그래서 v1 은 판정 step 의 **실측** 각 경계를 쓴다 (처방 회전은 입자 무관).
  4 차 요청서 `docs/reviews/codex_mixer_highbo_rereview3_request_20260928.md`.  ⬜ 런별 체크포인트 상태 확인 (3 차 Q1) · WSL 영수증 v1 실행.

## ㉕ v100 d_h 대등화 재적합 · 세대 점검 재현 2 런 · WSL 영수증 v1 (09-28)

- **v100 코드 경로 확정** (`SELF-55` 닫기 조건): `~/Yonghoon-DEM-DFT` (데이터 루트와 같은 체크아웃) @ `93a8b2d27` — eq288 로그 `repo HEAD` · 같은 HEAD 사본 `/home/ubuntu/runyourai/1/Yonghoon-DEM-DFT` ·
  파이썬 = uma (`activate_dem.sh` 가 잡는 `/home/ubuntu/runyourai/1/opt/miniforge3/envs/uma/bin/python3`).  ps45 사전등록 §5 에 반영: C = A 와 같은 코드 (**pull 금지**) · D = 별도 worktree `~/dem-score` ·
  §5-B 정정 (WSL venv python · `--type-map 1:AM_P,2:AM_S,3:SE` · lateral 기대값 0.05 ± 5e-5 — 다섯 덱 box 0.05, 옛 킷 0.050013 은 대체값으로 보임).
- **eq288 재적합** (사용자 실행, 보간 5 · 외삽 0): φ 0.75 **−0.561 / R² 0.914** / sd 0.081 / LOO 0.169 · φ 0.72 **−0.686 / R² 0.863** / sd 0.129 / LOO 0.408 (LOO 최대 = 둘 다 10_0).
  손 재현 일치.  §⑩ 등록 채점: ① 보간 5 ✅ · ② |기울기| 두 φ 모두 ↑ ✅ · ③ R² 두 φ 에서 **반대** ❌ · ④ φ 감도 0.082 → 0.051 (192 0.033 · 순서 반전).
  ⇒ "정밀화가 접힘을 강화한다" 는 φ 0.75 한정 · verdict §⑩-b · CLAUDE.md d_h 절에 날짜 한정.
- ★ **새 한정어**: 대등화 점이 **코드 세대 셋**에 걸친다 (res 08-06/07 · ps_7_3 08-11 게이트 전/후 · eq288 09-27) · ps45 동결선 = 옛 세대 점만.
  → **재현 2 런 발사** (09-28 02:02, v100 `~/rep288` · 태그 `rep288` · mpm3d md5 `866c8ed1` · ps_10_0 ε 11.81 · ps_7_3 ε 11.73 — 원 파일명과 같은 ε) ·
  판정선 = verdict §⑩-b (|Δ ln σ| ≤ 0.01 · |Δ두께| ≤ 0.01 µm, 결과 전 커밋).
- **WSL 영수증 v1**: gen (N1 5,802,624 · 회전 9,066,757 step · 리셋 대안과 79.205° (면 대칭 제외 3.872°)) → `run.sh` A · B **exit 0** →
  analyze **실패 — 완주 표지 하나만**: 예정각 오차 최대 1.92 × 10⁻⁵° · 각 경계 **0.00115°** (등록 상한 0.05° 의 1/43 · 출력 자릿수 한계) · A↔B 0 m · 기대 step A 208 · B 81 완전.
  원인 = 내 생산자가 완주를 `Total wall time` 배너로만 봤는데 이 빌드는 09-21 덱에서 배너를 안 찍는다 — 09-22 E0 3/3 에 실측돼 `run_all.sh` 18행에 이미 있던 사실 (원장 `SELF-56`).
  ✅ 수정 (비준): 완주 = exit 0 ∧ (배너 ∨ 로그의 마지막 thermo step = 끝) · `run.sh` 는 사실만 기록 · `analyze` 가 로그로 판정 (옛 기록이어도 **재실행 없이 analyze 만** 다시) ·
  셀프테스트가 `run.sh` 의 실제 기록 코드를 돌린다 (17 → 20, 옛 코드에서 ⑤ · ⑨ 실패 확인).  ⬜ WSL 에서 pull → analyze 한 줄 → 영수증 커밋.
- ps45 킷 (§5-B): 웹앱 케이스 셋 (ps_10_0 `0853b1` · ps_0_10 `0bee25` · ps_3_7 `bd85f9`) + 5_5 · 7_3 업로드 대기 → 킷 5 개 → v100 C 15 런 (재현 2 런 뒤).

## ㉖ 09-28 오전 — 영수증 v1 통과 · 재현 2 런 재발사 · 주간 리포트 (대피 직전 상태)

- ✅ **WSL 재개-위상 영수증 v1 = 통과** (`ba33a4939` 로 analyze 만 다시, LIGGGHTS 재실행 없음): A 208 step · B 81 step · 예정각 오차 최대 1.92 × 10⁻⁵° ·
  **각 경계 0.00115°** (등록 상한 0.05° 의 약 1/43 — STL 출력 자릿수 한계) · A↔B 0 m · 리셋 간격 (면 대칭 제외) 3.872°.
  ⬜ 파일 `~/phase_v1/receipt_v1.json` (사용자 WSL → Downloads 복사됨) 을 받아 `docs/data/mixer_phase_receipt_20260928/` 에 receipt_v1.json 으로 커밋 ·
  README · 믹서 고-Bo prereg §10 · CLAUDE.md 믹서 줄 (⬜ WSL 영수증 v1 → ✅) 갱신 — 파일이 오기 전에는 판정 경로에 쓰지 않는다.
- ⚠ **v100 재현 2 런 (세대 점검, verdict §⑩-b) 첫 발사 실패** (02:02): `★★ ABORT: numpy+scipy+taichi 되는 venv 없음`.  원인 (로그로 확인) —
  eq288 은 `activate_dem.sh` 가 `~/Yonghoon-DEM-DFT/venv` 를 source 해 `python: /home/ubuntu/runyourai/1/Yonghoon-DEM-DFT/venv/bin/python3` 로 돌았는데,
  이번엔 `(uma)` 셸이라 `activate_dem.sh` 가 venv 를 건너뛰었고 (`CONDA_DEFAULT_ENV` 가 base 가 아니면 건너뜀) `--data ~/rep288` 이라 나머지 후보도 없었다.
  내 첫 추정 ("`~/rep288/venv` 심링크") 은 틀렸다 — 그 길은 `activate_dem.sh` 의 CUDA `LD_LIBRARY_PATH` 설정도 건너뛴다.  원장 `SELF-57`.
  ⇒ **09-28 오전 `conda deactivate` (CONDA_DEFAULT_ENV=없음) 뒤 같은 명령으로 재발사** (PID 1676896).  ⬜ 확인: `grep -m3 -E '^venv:|repo HEAD|ABORT|^=== ' ~/rep288.log`
  의 `venv:` 줄이 eq288 과 같아야 한다.  완료 뒤 대조 명령과 판정선은 verdict §⑩-b (|Δ ln σ| ≤ 0.01 · |Δ두께| ≤ 0.01 µm).
- ✅ **주간 리포트 09-21 ~ 27** = `docs/worklog/weekly_20260927.md` (`/worklog` 에 뜬다 · 처음 보는 사람용 · 인라인 SVG 바닥 검사 그림 · test_worklog 통과).
- ⬜ 남은 일 (우선순위): ① 영수증 파일 커밋 ② rep288 확인 → 결과 대조 ③ Codex 4 차 리뷰 (요청서 §0-b 포함) 처리 ④ 런별 체크포인트 상태 확인 도구 (Codex 3 차 Q1) ⑤ ps45 킷 5 개 (5_5 · 7_3 웹앱 업로드 대기) → v100 15 런 (`~/Yonghoon-DEM-DFT` @`93a8b2d27` 그대로, pull 금지 · conda deactivate 뒤) ⑥ 순수 SE r050 (ibb 233951) 완주 → Q1–Q3 ⑦ Phase A 100 GPa STEP3 (kgy) ⑧ `SELF-52` 정정 ⑨ 배치 ABORT 힌트 결함 (`SELF-57`) 수정안 보고.

## ㉗ 09-28 오전~낮 — 연장 세션 (대피 뒤) · 순수 SE 3/4 완주 · 발표 그림 2 장

- **브랜치**: 배정 브랜치의 커밋 3 개(`f58c71d6e` · `514691646` · `ab4e23250`)가 **이미 stoic-knuth 에 포함**돼 있었고
  stoic-knuth 가 118 커밋 앞서 있었다 ⇒ rebase 도 폐기도 아닌 **단순 fast-forward** 로 맞췄다 (`b195ddb16`, 비준).
  ⚠ 내 첫 확인은 틀렸다 — 브랜치별 fetch 뒤 **중간에 `git fetch origin`(전체)을 끼워 `FETCH_HEAD` 를 덮어써서**
  `ls-tree FETCH_HEAD` 가 다른 계보를 봤고, 인계 문서·진행 문서·믹서 TSV 가 "없다" 고 보고했다 (셋 다 있었다).
  ⇒ **`git cat-file -e FETCH_HEAD:<경로>`** 로 확인하고, 브랜치별 fetch 와 전체 fetch 를 섞지 않는다.

- ✅ **v100 `rep288` 재발사 성공** (`SELF-57` 처방이 통했다): `conda deactivate` (`CONDA_DEFAULT_ENV=없음`) 뒤 발사 →
  로그 `venv: …/scripts/activate_dem.sh · python: /home/ubuntu/runyourai/1/Yonghoon-DEM-DFT/venv/bin/python3` ·
  `repo HEAD : 93a8b2d27` = **eq288 과 같다**.  ⚠ 그런데 PID 1676896 이 10:13 에 이미 `Done` 이고 로그에 `=== ` 블록이
  하나만 보였다 — ⛔ **`grep -m3` 이 3 개에서 잘려 뒤쪽 `ABORT` 를 볼 수 없으므로 완주·실패 어느 쪽도 판정하지 않는다**
  (전수 `grep -c '^=== '` · `grep -nE 'ABORT|Traceback|rc=[1-9]'` 대기).
  ⚠ 로그에 `kit_ps_10_0: 겹침 미보정 (metrics 부재) — ε 목표가 ~1 %p 밀린다` 가 있다 — 판정선이 `|Δ ln σ| ≤ 0.01`
  (verdict §⑩-b) 이므로 **eq288 원 런에도 같은 경고가 있었는지** 먼저 봐야 대조가 성립한다 (같으면 공통모드).

- ✅ **ibb 순수 SE `pse_r050_a` 완주** (job 233951 COMPLETED · step 2,935,000 · `plate_z 0.03021`).
  ⇒ 4 침대 중 **3 개 완주** (`r100_a` · `r100_b` 09-27 · `r050_a` 09-28) · **`pse_r075_a` 만 남았다**.
  ★ 사전등록 `pure_se_union_prereg_20260927.md` §4 로 **지금 갈리는 것**:
  · **Q3 (MODEL / PACKING)** = `r 0.5 → 1.0` 만 필요 ⇒ **판정 가능** · **잡음 행** (`|r100_a − r100_b|`) = **가능**
  · **Q1** = 등록 문구가 "**4 침대 중앙**" ⇒ `r075` 없이 **불가** · **Q2** = `ε_pSE(r_SE)` **보간** 필요 ⇒ **불가**
  ⛔ Q1 을 "3 침대 중앙" 으로 바꾸지 않는다 (값을 본 뒤 정의를 바꾸면 등록 무효).
  측정은 §5 에 등록된 `lhs_union_webapp.py` 그대로 — sphere · 쌍 렌즈 · **정확 union(MC)** 셋을 내고
  접촉 `delta` 열 ↔ 좌표 겹침이 1 % 넘게 어긋나면 `DELTA_MISMATCH` 로 union 을 믿지 않는다.

- **발표 그림 2 장 + 생성기** (주간 보고용, 1저자 요청): 믹서 캠페인 설계·진행 · LHS 공극률 재수립.
  생성기에 **정본 대조 selftest** 를 달았다 — 믹서는 팔 Bo 값을 사전등록 본문에서, LHS 는 건수(97 · 58 · 4)와
  **`open` 인 LHS-1x 집합**을 `findings.json` 에서 실제로 찾는다 (규율 ④: 그림만 조용히 낡는 것을 막는다).
  ★ 그 대조가 실제로 하나를 잡았다 — `LHS-13` 만 `open` 이고 나머지 셋은 `claimed_fixed` 라 그림에 상태 칩을 넣었다.
  ⚠ `claimed_fixed` 는 **검증된 것이 아니다** (재수확 검증 전 · 결과표 배포 보류) — 그림 하단에 그 한정어를 박았다.
  믹서 진행률은 09-27 60–69 % → **09-28 10:07 실측 73–82 %** 로 갱신 (L0 82 · LA 76/76/77 · LB1 76 · LB2 77 ·
  LB3 73 · LC 76/77/79 · E0 3/3 완료).
  ⛔ 슬라이드 금지 표현 (사전등록이 철회·정정한 것): "코팅하면 잘 섞인다" 류 · "코팅" 을 헤드라인 주어로 (R-3 은
  *"AM–AM 점착을 Bo 3.0 → ≈0 으로 끄면"*) · LA 를 "문헌 앵커" 로 (R-4 철회, **내부 기준점** Bo_code 3.0 = Bo_po 0.444) ·
  Bo_code 38.4 를 "문헌 재현" 으로 · 09-27 12:14 중간 곡선값 · 적대 리뷰 HOLD 를 "캠페인 결함" 으로.
  ⚠ 축 라벨은 "AM–AM **명목** 점착" 이다 — HB-03 ⓑ 로 벽 CED 가 대각에 묶여 **AM–AM 을 올리면 AM–벽도 함께** 오른다.

- **믹서 Codex**: 1저자 지시 = **통과할 때까지 리뷰 반복**.  4 차 요청서 **발송됨 — 1저자 확인 (09-28)**.  ⚠ 그 전 내 "발송됨" 서술은 파일 존재에서 추론한 것이었다 (`SELF-59`) — 지금 문장은 확인된 사실이다
  (`codex_mixer_highbo_rereview3_request_20260928.md`).  ⛔ GO 전까지 그 도구로 **발사·판정 결정을 하지 않는다** —
  다만 Codex 는 실제 캠페인 결함을 주장한 적이 없으므로 **런은 계속 돈다** (막히는 것은 판정뿐).

- ⬜ 받을 것: v100 전수 로그 확인 · WSL `receipt_v1.json` · `pse_r075_a` 상태 · 순수 SE 3 침대 union 측정.

### ㉗-1 v100 재현 런 — 재사용된 eq288 점의 실물 (09-28, 사용자 v100)

`~/Yonghoon-DEM-DFT/se_curve/xfer_res_kit_ps_10_0_g288_e1181.json` · **1,503 B · mtime 2026-09-14 10:50**

- ⛔ **세대 오염 확정**: eq288 배치는 09-27 에 돌았지만 이 점은 `--skip-existing` 이 **09-14 파일을 재사용**했다.
  네 킷의 **가운데 ε 점 전부**(`e1201` · `e1185` · `e1189` · `e1181`)가 SKIP 이다 ⇒ 배치 로그의
  `repo HEAD 93a8b2d27` 는 **재사용된 점에는 해당하지 않는다**.  ㉕ 의 "세대 셋" 위에 **한 겹 더** 있다.
- ⚠⚠ **이 JSON 에 코드 출처 필드가 하나도 없다** — `repo_head` · `mpm3d_md5` · `code_sha` · 생성 시각 전부 부재.
  세대를 말해 주는 것은 **파일 mtime 뿐**이다.  Phase A 의 `code_sha=null` (`PASL-03`) 과 **같은 부류의
  결손이 se_curve 파이프라인에서 재발**한 것이다.
- ✅ **frames 우려는 해소됐다 (내 앞선 경고를 정정)**: `frames_budget` **400** 으로 **rep288 과 같다**.
  그리고 `porosity_at_target_pct 11.762` · `settled_over_target 1.3467` 이 **non-None** = 코드가
  `reached` 로 게이트하는 두 필드가 채워졌다 ⇒ **400 프레임으로 목표에 닿았다**.
  ⇒ rep288 xfer 로그의 *"최대 444 프레임 필요"* 는 **WALL0 → WALL_MIN 전 구간 주파의 상한**이지 ε 목표
  도달에 필요한 수가 아니다.  ⇒ **§⑩-b 대조는 성립한다** (공통모드).
- ✅ 침대·격자도 동일: `n_pts` **96,322,600** · `n_grid` 288 · `nz` 651 · `sub` 160 · `mach 0.03` ·
  `dt 0.0002` · `compact_to_pct 11.81` · `protocol hold` · `readout wallP` · `se_frac 0.27` · `n_AM 175`.
- ★ **대조 기준값** (§⑩-b `|Δ두께| ≤ 0.01 µm`): `thickness_um` **108.419** · `porosity_at_target_pct` 11.762 ·
  `settled_over_target` 1.3467 · `final_stress_GPa` 0.4037 (target 0.3 — `hold` 이므로 목표 초과는 정상).
  ~~⚠ 이 JSON 에 **σ 는 없다** — `|Δ ln σ|` 쪽 기준값은 STEP3 산출에서 따로 가져와야 한다.~~
  ⛔ **철회 09-28 (`SELF-61`)** — d_h 판정의 σ 는 **`final_stress_GPa`** (MPM SE 응력) 이다 (`fit_dh_collapse.py:141` · verdict §⑩-b
  *"비교량 = 적합기가 읽는 두 값 (`thickness_um` · `final_stress_GPa`)"*).  STEP3 전도도는 무관하다.  ⇒ ps_10_0 대조 기준 =
  **두께 108.419 µm · σ 0.4037 GPa** — 이 JSON 에 이미 있다.
- ~~⇒ **rep288 무성 종료의 원인은 frames 가 아니다.**  남은 후보는 외부 SIGKILL (호스트 OOM 등) 뿐이고
  아직 미확인이다.  ⛔ 원인 확인 전에는 15 런을 띄우지 않는다.~~
  ⛔ **철회 09-28 11:53 (`SELF-60`) — rep288 은 죽지 않았다.**  v100 `pgrep` = 배치 PID **1676897 생존** · 로그 = 첫 런
  `rep288_kit_ps_10_0_g288_e1181` 09:05:18 시작 뒤 `EXIT=` · `BATCH DONE` · dmesg OOM **없음** = 첫 런 (≈ 3 h) 진행 중.  내가 본
  `Done` 은 셸 작업 래퍼 (1676896) 였다.  frames 결론 (위) 은 그대로 맞다 — 틀린 것은 "죽었다" 는 전제다.

## ㉘ 09-28 낮 — v100 ps45 발사 준비 (오진 둘 정정) · 비준 둘 · 믹서 ④ 착수

- **비준 (1저자, 09-28)**: **J19** (인계표에 union 열 병기 · 구 부피 합 열 유지 — `pure_se_union_prereg_20260927.md` §6-2) ·
  **FAMV2 §12 네 칸** (`01` 관측 사건 = 서보 수렴 두께 · `R1` = ① 현 코드로 `f=0` 팔 재실행 · `04b` = §9 v2 유지 · 기준 상태 지문 =
  내가 30.28 µm 의 출처를 찾아 제안) — ⬜ 반영은 믹서 ④ 뒤에 (§12 봉인 문안 · R1 재실행 명령).
- ⛔ **정정 둘** (㉗-1 에 철회 표지): rep288 은 **살아 있다** (`SELF-60`) · d_h 의 σ = `final_stress_GPa` (`SELF-61`).
- **ps45 침대 = 웹앱 DB 의 `input_6mAh_real_{1..5}_D9`** (D9 = AM_P 지름 9 µm) — 입자 수가 README §2 예측과 맞는다
  (3:7 = 121 · 3,209 · 158,763 ↔ 121 · 3,209 · 158,765 · 0:10 = 0 · 4,588 · 158,760 ↔ 0 · 4,584 · 158,765).
  ⚠ 09-28 오전 기록의 *"5_5 · 7_3 업로드 대기"* 는 낡았다 — 다섯 다 웹앱에 있었고, 없던 것은 **v100 의 킷**이다
  (v100 dry = `SKIP kit_ps_*_r45 — am/se_scaffold.csv 없음` ×5).
- **킷 = `scripts/build_ps45_kits.py`** (selftest 10/10) — §5-B 의 손 절차를 한 번에: P:S 를 이름이 아니라 **입자 수로** 정하고,
  lateral |x − 0.05| ≤ 5e-5 · 덱 이름 ↔ 개수 일치 · 같은 P:S 중복은 **좌표**가 같을 때만 받는다.  WSL 에는 같은 코드를
  heredoc 으로 건넸다 (리포 pull 없이).
- **v100 발사 방식**: rep288 (`--gpu-mem 28`) 과 **동시에 띄우지 않는다** (32 GB) ⇒ `while kill -0 1676897` 대기 → 킷 5 개 재확인 →
  **등록된 §5-C 명령 그대로** (`--skip-existing` 없음 · 태그 `eq288r45`) → `~/eq288r45.log`.  예상 rep288 끝 ≈ 15 시 · ps45 15 런 ≈ 45 h.
  ⬜ 남은 전제 (§2 ⚠): 킷 출력의 `덤프 atom_<step>` = 각 `post_ps_*_r45` 로그의 마지막 step 인지.
- ✅ **킷 5/5 생성 (웹앱 PC, 09-28 낮)** — 케이스 id · 개수 · 덤프는 ps45 사전등록 §5 덧붙임 표.  ⚠ ps_10_0 = **`6e4ff6`**
  (사전등록의 `0853b1` 아님).  ⬜ v100 전송 (tgz) → 풀기 · dry 15 → rep288 PID 대기 발사.
- **믹서 ④ 착수** — `HBR4-04` = **(나)** mesh-dump 판정 분기 비활성화 (1저자 "ㄱㄱ").  `HBR4-01` 반례 3 건
  (B 전부 NaN · 빈 봉인 목록 · 빈 덤프 해시 목록) 을 셀프테스트로 먼저 옮겨 **우리 HEAD 에서 3/3 통과 (= 결함 재현)** 를 확인한 뒤 생산자를 고쳤다 (23/23).
- ✅ **ps45 기록 커밋 `c13b63ba1`** (킷 스크립트 · `SELF-60`/`61` · ㉘ · 사전등록 §5 표).
- **v100 rep288 첫 점 (ps_10_0 ε 11.81, 09-28 12:2x 사용자 v100)**: 기준 `xfer_res_…e1181.json` (09-14) ↔ rep288 (`93a8b2d27`) —
  `thickness_um` 108.419 ↔ 108.419 (Δ 0.000 µm) · `final_stress_GPa` 0.4037 ↔ 0.4039 (Δln 0.000495) · `porosity_at_target_pct` 11.762 = ·
  `settled_over_target` 1.3467 ↔ 1.3472 · `n_pts` 96,322,600 = · `frames_budget` 400 =  → 판정선 (|Δln σ| ≤ 0.01 · |Δ두께| ≤ 0.01 µm) 안.
  JSON 반올림 해상도 (두께 1e-3 µm · Δln ~3e-4) ≪ 판정선.  ⛔ 등록 문구 = **"두 점 모두"** → ps_7_3 (11:58 시작) 전에는 "세대 무해" 라고 쓰지 않는다.
  첫 런 wall 10,382 s · EXIT=0.  ps45 대기 PID 1678034 → rep288 끝나면 자동 발사.
- ✅ **믹서 ④ 수정 (Codex 4 차 해제 목록 7 항 · `HBR4-04` = (나))** — 반례를 셀프테스트로 먼저 옮겨 **옛 코드에서 재현** 확인 (검사기 11 건 · 생산자 3 건 · 런처 9 건 실패) 뒤 수정:
  검사기 73/73 · 생산자 26/26 · 판독기 34/34 · 런처 64/64.  ★ 런처 `HL②e` 는 대역 없이 **진짜 비교기 · 진짜 생성 덱** (허용 다섯 CED ×2) 으로 옛 런처가 **받아서 발사했다**.
  ⚠ v1 영수증 거부 → WSL `analyze` 재실행 필요 · E0 정지 벽 계약 = WSL 에서 세 시드 (명령 prereg §2-4 ③) · 원장 `claimed_fixed` 와 5 차 요청서는 다음 커밋 (수정 커밋 SHA 필요).
- ✅ **수정 커밋 `999a5bf85`** (게이트 두 레인 0) → 원장 HBR4-01~08 `claimed_fixed 999a5bf85` · **5 차 요청서 작성됨**
  (`docs/reviews/codex_mixer_highbo_rereview4_request_20260928.md`) — ⚠ **발송 여부는 1저자 확인 뒤에만** 적는다 (`SELF-59`).
- ★ **1저자 결정 (09-28 오후): 믹서 LH 는 ibb SLURM 20 코어 × 3** (*"ibb로 진행하자 · 1,3 같이 통합 · 2번은 걱정 안 해도"* — 마감).  Q4 (L 완주 뒤) 해제 — 근거 J8 = WSL CPU 경합.
  ① Codex 5 차 GO 와 ③ sbatch 런처를 **한 리뷰로** (5 차 요청서 §5 · 미발송) · ② 기계 · 바이너리 · MPI 분할 차이는 **차단 사유 아님** — 결론 한정어 (사전등록 §0 Q5 · §3-2).
  구현 (시험 먼저 — 옛 코드에서 29 건 실패 재현): 런처 `BACKEND=slurm` (ibb 실물 러너 형식 · 봉인에 러너 · 시작 대조기 sha256 · `jobid` = "뜬 런") ·
  `start_check.py` (job 시작 때 봉인 재대조 — 대기열 틈) · 검사기 `launch_binding` 이 SLURM 봉인이면 `job_start.json` 까지 · 영수증 `run.sh` 의 `LMP_LAUNCH` (ibb `mpirun -np 1`).
  런처 81/81 · 검사기 83/83 · 영수증 도구 28/28.  ⚠ ibb 영수증은 `lmp_mpi` 로 **다시** (WSL 영수증은 08-25 `lmp_serial` 에 묶임 — L/LC 의 측정 기록으로만).
  ⚠ ibb a5/a6 3 job (`a6_p04` ckpt 1,650,000 · `a5_p08`/`a5_p10` 3,600,000) 취소 요청 → 명령만 드림 (이번 실행분 ≈ 3 h/job 손실 경고 · 재개는 `resume_ckpt.sh`).
- ✅ **ibb 준비 (09-28 오후, 1저자 실행)**: 리포 `77919b8` (depth 1) · 입력 tgz (LC 3 덱 = WSL 원본 · E0 기준 런) · `SET=highbo gen_all.sh` LH 3 덱
  (`6d71bd50` · `bf9d54fd` · `36ad6edf` — 컨테이너 재생성과 같다) · 덱 관문 3/3 PASS · E0 세 시드 입력 대조 = 기대 덱 · STL 원본 (WSL).
- ✅ **ibb 영수증 v2 통과 · 커밋** (`docs/data/mixer_phase_receipt_20260928/receipt_v2_ibb.json` · job 235118 · node01 · `lmp_mpi -np 1`): WSL v1 과 **208 행 비트 동일** ·
  소비자 LH 덱 수용 · 런 잇기는 발사 봉인 뒤 (지금은 거부 = 설계).  ⚠ 처음 job 은 `QOSMaxCpuPerUserLimit` 로 대기 — a5/a6 3 job (60 CPU) 을 1저자가 **scancel**
  (234562 · 234563 · 234568) 한 뒤 돌았다.  ⚠⚠ **QOS `cpu-60` = 사용자당 60 CPU = LH 3 × 20 전부** — LH 가 도는 동안 a5/a6 재개 (`resume_ckpt.sh`) 는 같이 못 돈다 (순서 = 1저자).
- WSL 영수증 v2 재분석 = 통과 (1저자 출력 · sha256 `1c9e4e17…`) — ⬜ 파일 미커밋 (L · LC 측정 기록용 · LH 에는 잇지 않는다).
- **5 차 요청서 고정 스냅샷 정정** — 초판은 `999a5bf85` 를 가리켜 §5 SLURM 코드 (`77919b860`) 가 스냅샷 밖이었다 → 스냅샷 = 요청서가 든 커밋 · §4 현황 · §5 추기 (E0 대조 확인) ·
  §6 (ibb 영수증).  1저자: *"게이트 끝나면 요청서 보낼게"* — ⬜ 발송 확인 전 (`SELF-59`).
- ✅ **Codex 5 차 요청서 스냅샷 = `091bb2114`** (영수증 · 요청서 정정 커밋, 게이트 0) — 1저자가 보낸다 (⬜ 발송 확인 전 · `SELF-59`).
- ✅ **J19 구현 (1저자 비준 09-28 *"비준이야"*)** — `scripts/lhs_design_dataset.py` 셀프테스트 ⑱ 13 건을 **먼저** 넣어 옛 코드에서 12 건 실패 (52/64) 확인 → 구현 → 64/64.
  `--export-handover` 가 기본으로 union TSV (`lhs_union_20260927/lhs130_union.tsv`) 를 붙이고 기본 수확 = `lhs_descriptors_20260925` (0924 판엔 `handover_qc` 없음).
  재생성 인계표 `docs/data/lhs_handover_20260928.csv` = 130 × 119 열 (0919 판 63 + HND-04 49 + J19 7) · ε_sphere 중앙 9.89 % (0919 판 47.28 % = 옛 수확) · union 중앙 13.60 % ·
  질량 보존 두께 비 1.015–1.114 · SE-rich (≥ 0.50, ⬜ 저자 확인) 21 · 음수 18.  ⛔ 배포 보류 그대로 · ③ φ union · ④ 적격성 union 은 안 함.
- ✅ **FAM §12-5 봉인 문안 (1저자 비준 09-28 네 칸)** — 01 = 서보 수렴 두께 · R1 = `f = 0` 팔 재실행 (공통 argv 제안 · `--periodic` 없음 = 코드 기본, ⬜ 확인) ·
  04b = §9 v2 유지 · 기준 상태 지문 제안 (real_14 · 260601_122725_63b338 · step 2,060,000 · 30.2845 µm · 창 [29.3716, 31.1884] 유지).
  ⬜ 봉인 전: WSL 원자료 대조 (sha · 같은 step 메시 · 두께 재현) · R2 argv · 동률 폭 · 재시도 규칙 · 기계 (v100 ps45 뒤).  런 0 건.
- ⛔⛔ **E0 정지 벽 계약 = 3/3 REJECT** (09-28 저녁 · 1저자 WSL · 스냅샷 `091bb2114` · 기대 덱 = 실행 덱 · 벽 근거 static):
  입자–입자 δ/r_min 4.681 · 5.453 · 5.763 % (AM_P–SE · 1 % 초과 931 · 899 · 878) · 벽 4.499 · 5.204 · 5.663 % (SE–드럼 · 113 · 98 · 127) · 창 t₀ 385,000 한 프레임.
  덱 영률 = A안 그대로 → 검사기 · 덱 결함 아님.  원인 = 09-21 설계 검증 (SE 0.244 % → "1 % 의 1/3 ✅") 이 SE–SE · 평균 응력만 셌다 (`SELF-62` P1 · 설계 문단 둘에 철회 표지).
  ⇒ 고-Bo §5 선행 2 미충족 = 등록대로면 확장 HOLD · 본 캠페인 §1 계약 행과 §5 "보조 진단" 의 관계 = 저자 결정.  ⛔ 1 % 불변 (K1).
  요청서 §7 · Q6 추가 (발송 전) — 1저자에게 발송 보류 권고.  ⬜ 저자: D-1 개정 여부 · LH 발사 여부 · 본 캠페인 계약 행.
- ✅ **WSL 산출물 반입 (1저자 첨부 · sha256 = WSL 출력)**: `docs/data/mixer_e0_contract_20260928/` (E0 계약 JSON 3 + README — 분위수 · 쌍별 최대: 중앙 0.03 % · p99.9 1.7 % ·
  SE 낀 쌍 전부 3.3–5.8 % · AM 끼리 ≤ 0.055 %) · `docs/data/mixer_phase_receipt_20260928/receipt_v2.json` (WSL v2 = ibb v2 와 값 · 208 행 · 운동 시계 전부 동일).
  `SELF-62` 문구 정밀화: 틀린 것은 전형값이 아니라 **평균 응력 한 값을 최대 천장과 비교한 것** (중앙 0.03 % < 설계 0.244 %).  요청서 §7 에 분포 · 경로.
- ★ **저자 결정 (09-28 밤)**: ① LH **첫 시드를 Codex GO 전 발사** (*"발사할게 q6 보내자"* · 고-Bo §0 Q7 · §12) — 코드 = 스냅샷 `622066f8e` 의 믹서 코드 (ibb `77919b8` · diff 0) ·
  ⛔ bin 0 스모크의 계약 ② 는 D-1 결정 전 금지 · `rest` 대기 · 사슬 결함이 나오면 재발사.  ② 본 캠페인 계약 행 = **보조 진단** (*"결정3 진행해줘 너가 권고 하는 부분으로"* ·
  본 캠페인 §0 · §5 한정어 문안) — ⛔ LC · L 런 계약은 D-1 결정 전 금지.  요청서 §8 (결정 둘 · Q7).  ⬜ D-1 = Codex 답 뒤.
- ✅ **FAM §12-5-4 기준 상태 지문 = 원자료 대조 (09-28 밤 · 1저자 첨부 네 파일)** — 덱 `734fa173…` · atom `079c85f1…` · contact `a609ba94…` ·
  mesh `8cbb6dd0…` (세 덤프 모두 step 2,060,000).  판 메시 2 facet 여섯 꼭짓점 전부 z 0.0302845 → 30.2845 µm = 웹앱 두께 · contact 덤프의 존재 = PHASE 4 (판 고정 완화) ·
  스캐폴드 CSV = 이 덤프 (AM \|Δ\| 1e-6 · SE 주기 최근접 8.66e-7, 1:1).  한정어: 판 고정 ⇒ `t_DEM` 은 PHASE 4 동안 불변 · 정지 양자화 0.05 µm/루프 ·
  판 위로 빠져나간 SE 3 · 전체가 바닥 아래인 SE 109 — 리포 CSV 로 본 *"판이 침대 윗면보다 ≈ 1 µm 낮다"* 의 정체 = 같은 step 의 평평한 판 + DEM 접촉 겹침 · 누출
  (다른 step 메시 · 꼭짓점 평균 편향 가설 기각).  ⚠ **정정**: 첫 채팅 보고의 *"2,060,000 = PHASE 4 의 끝"* 은 확인 밖이었다 — 확인된 것은 PHASE 4 **안**까지
  (마지막 덤프 여부 = 압축 루프 수 N · 312 ≤ N ≤ 331 · ⬜ 로그).  사본 `docs/data/real14_reference_20260928/` (덱 · 메시 · README — atom · contact 는 해시만, ⬜ 커밋 여부 1저자).
- ⛔ **Codex 5 차 v2 (09-28) = HOLD** — 증거 대조 091bb 23/23 · 978158d 12/12 · 매니페스트 51/51.  신규 HBR5-01 (시작 관문이 빈 봉인 통과) · 02 (rest 관문이
  증서 파일만 재해시) · 03 (LC 직렬 ↔ LH MPI20 교락) · 04 (np1 영수증 → np20) · 05 (gen.json 끝 step) · 06 (위치 오차 SE 0.418 %p) · ADD-Q7-01
  (내 결정 3 근거가 거꾸로: §1 계약은 09-22 부터 · §5 "보조 진단" 은 09-27 중간 M 열람 뒤 추가).  ⬜ 기록 · 수정 비준 대기.
- ⚠⚠ **LH 첫 시드 미발사 확인 (09-28 밤, 1저자 ibb)**: `LH_s32452843` 에 생성 입력 (14:16) 만 · 봉인 · jobid · log.lmp 없음 · `squeue` 빈 · sacct 09-27 이후 LH job 0.
  → **저자 결정 "60 다" = 세 시드 × 20 코어 동시** (bin 0 스모크 관문 생략 · §9 D-4 이탈 · 고-Bo §0 Q7′ · §12).  런처 `launch_highbo.sh all` 신설 — 시험 먼저
  (HA①–⑦: 옛 코드에서 양성 5 건 실패 확인 → 구현 → 88/88): `DEVIATION` 문구 필수 · SLURM 판 전용 · 덱 비교 · 세 시드 모두 안 뜸 · 봉인 `stage: all` + `deviation`
  (결정 문구 · 등록 순서 · 생략 관문) · 코호트 · all 뒤 rest 발사 0.
- ✅ **LH 세 시드 발사 (09-28 18:07 KST, 1저자 ibb · 커밋 `caba30c7a`)** — job 236245 (`LH_s32452843`) · 236246 (`LH_s49979687`) · 236247 (`LH_s67867967`) ·
  덱 관문 3/3 PASS (실제 시드 서명 6/6 · LC→LH 허용 B · AM 쌍 CED ×19.08–32.75 · SE 쌍 ×1) · 봉인 lmp `ee2d7726…` · 덱 `6d71bd50`/`bf9d54fd`/`36ad6edf` · 제출 직후 PENDING.
  ✅ 세 job 모두 시작 · `job_start.json` ok = True · reasons [] (1저자 ibb 확인) · ⬜ bin 0 스모크 ① ③ ④ 는 기록으로 (계약 ② 는 D-1 전 금지).
- `watch.sh` SLURM 판 수정 — pid 없이 jobid 만 있는 ibb 런을 ⛔죽음 으로 찍던 결함 (시험 HW①–② 먼저: 옛 판에서 HW① 실패 확인 → 90/90).
- ⛔ **LH 3 런 정지 (09-28 20:23 KST, 1저자 `scancel`)** — *"이거하고서 더 확실하게 돌리는거 어때 · stop 해도 돼"* · *"믹서 관련해서 ibb로 올리는거는 확실하게 하고 올리자"*.
  정지 직전 step 520,000 / 515,000 / 495,000 (5.2–5.5 %) · 덤프 11 / 11 / 10 · 경과 2:15:41 (sacct 3/3 CANCELLED+ · End 20:23:13 — 236246/7 은 1저자 재조회로 확인).
  **부분 런 M · 겹침 미열람** · 폴더 보존.  실측 속도 ⇒ MPI 20 런당 ≈ 41 h (추정).  재발사 = 고-Bo §0 Q8 ①–④ 뒤에만.
- ✅ **Codex 5 차 v2 반영 (09-28 밤, 비준 *"Codex 5차 반영 진행"*)** — 판정문 `docs/reviews/codex_review_mixer_highbo_round5_v2_20260928.md` · 출력 전용 증거 둘
  (매니페스트 51/51) · 원장 HBR5-01~06 + `HBR5-Q7` (= ADD-Q7-01 · ID 규칙상 하이픈 둘 불가) · HBR4-02/03/04/06/07/08 verified (핀 091bb2114) · HBR4-01/05 재개방.
  수정 — **반례 시험 먼저** (옛 코드 실패 확인: 런처 9 FAIL · 생산자 28/30): HBR5-01 `start_check.py` 봉인 모양 먼저 (빈 · 비객체 · nested · 타입) · 비교 무조건 /
  HBR5-02 rest 관문 = bin 0 창 · E0 t₀ 입력 집합을 판독기 파일 규칙 (STEP_RE) 으로 재열거 (중복 · 격자 밖 · 결손 · 다른 파일 거부, bin 1 추가는 통과) /
  HBR5-05 영수증 완주 기준 = 봉인 A/B 덱 (끝 · N1 · 간격 · `run … upto`) · gen.json 대조만 · B 로그 RESUME_STEP = A write_restart step → 런처 98/98 · 생산자 30/30.
  문구: HBR5-06 (SE 0.418 %p) 요청서 · 영수증 README 정정 / 본 캠페인 §0 · §5 = **명시적 후속 개정 · 원 규칙 NOT_MET · Codex 문안** (내 결정 3 근거의 역사 오류 정정).
  커밋된 영수증 v2 두 판: run_total 9,452,094 = 운동 시계 끝 (HBR5-05 반례 미발화).
- 1 % 의 근거 (1저자 질문): 코드 `OVL_CEILING` = *"DEM 연질구 관례"* (인용 없음) + 옛 덱 관찰 (3.5 % 팔 손실 0 · 수십 % 팔 붕괴 = 수치 안정성).
  정본 litdb Paulick 2015 (Powder Technol.) 는 **지름**의 1 % (우리는 반지름 = 2 배 엄격) · *"최대 또는 평균 — 저에너지 응용엔 평균"* · 목적 = 강성 감소의 무해성 + Hertz 소변형.
  믹서 설계 문서는 이 카드를 인용하지 않았다.  E0 는 지름 기준으로도 최대 2.3–2.9 % (여전히 초과) · 평균 기준이면 통과하나 E0 열람 뒤라 사후 개정 → 민감도 근거 필요.
- 📅 **10 월 일정 (1저자 09-28 밤 전달)**: 10/2 까지 파트별 10 여 쪽 + 발표자료 (1. DEM 파트 (미세구조) = 용훈 · 2. DEM 파라미터를 통한 머신러닝 = 수영) →
  10/5 1 차 취합 (스토리 하나로 묶기 어렵다 — 계속 고친다) → 10/7 교수님 인수 · 주간보고.  작업 순서 (1저자): **LHS 인계 먼저 → 후막 바이모달 미세구조**.
- ✅ **LHS J20 코드 (09-28 밤, 비준 네 권고 전부)** — 웹앱 파이프라인 그대로 배치 `scripts/lhs_webapp_batch.py` (selftest 7/7) · `run_pipeline(figures=, auto_db=)`
  (T9 6/6 — 기본값 불변 · 계산 단계 순서 동일) · 수확기 벽 τ 새 열 (⑰ 10/10 · 옛 τ 바이트 동일) · 생성기 `--webapp` ✅ 열 · 같은 프레임 관문 · 열 사전 (⑲ 14/14 ·
  옛 인자 = 09-28 인계표 바이트 동일) · WSL 원샷 `scripts/run_lhs_fill_wsl.sh`.  ⬜ WSL: 한 건 → 전 건 → 묶음 → 커밋 · README · 배포.
- 📥 **Codex 6 차 (09-28 밤) = HOLD** — HBR5-01 · 02 닫힘 · HBR5-05 원 반례만 닫힘 · 새 P1 HBR6-01 (측정 A/B 와 다른 메시의 위상 증서 생산) · HBR6-02 (SE ×14 가
  혼합쌍 · 벽 점착도 바꾼다 — 순수 강성 검증 아님) · P2 HBR6-03 (완료 배너가 끝 step 모순을 덮는다) · Q4 권고 = 같은 환경에서 삽입부터 새 LC ×3 + LH ×3.
  ⬜ 반입 · 원장 · 반례 재현 · 설명 → 비준 (LHS 배치 푸시 뒤).
- ✅ **Codex 6 차 반입 (09-28 밤)** — 판정문 + 증거 28 파일 (매니페스트 바이트 일치 · 소스 사본 23 제외) · 원장: HBR5-01/02/05/06/Q7 → verified (05 는 원 반례만) ·
  새 HBR6-01 (P1) · HBR6-02 (P1 설계) · HBR6-03 (P2) · 믹서 스크립트 5 개가 핀 사본과 sha 동일 → `changed_gen_motion_signature` · `banner_short_tail` 통과 (= 결함) · `permuted_triangles` rc 1 **우리 HEAD 재현**.
  ⬜ 수정 비준 대기 (HBR6-01 · 03 코드 · Q1 · Q5) · 저자 결정: D-1 경로 (§5-3 설계) · Q4 estimand.
- ✅ Ag–C 점착 트랙: DEM 7 차 발송 기록 (`docs/dft_reply7_adhesion_20260928.md`) · BE → CE 정정 · 결정 5 (조성 확정 · 덴카블랙) **닫힘** — DFT 후속 회신 예정.
- ✅ DEM 7 차 **1저자 비준본** 반영 — 기록 §3 을 비준본과 일치 (34/34 줄) · 초안과 다른 곳 = 짝 규칙 **결과 전 원칙 ①–④** (트랙 문서 §5-8 에도 기록).
- ⏸ LHS 인계 **일괄 실행 보류** (1저자 09-28 밤 *"일괄적으로 뽑지 말고 하나하나 코드 확실하게 수정/갱신한 다음에"*) — ✅ 열을 묶음별로 코드 정의부터 감사 (첫 묶음 = 접촉 위상 · z_SE-SE · z_AM-SE · AM_P-SE CN · 표면 가중 · z_AM-AM · 접촉 수).
- ✅ LHS J20-a ① 접촉 위상 ⓐ–ⓓ 구현 (비준 *"권고하는걸로"*): 감사기 (주기 플래그 ↔ 기하 재계수 — 1저자 제안) · 배치 관문 (반례 먼저) · 열 사전 · 벽 접촉 비율 열 — WSL 감사 대기.
- ✅ 믹서: Codex 6 코드 수정 ①–④ **비준** + 시뮬레이션 **진행 비준** (1저자 *"돌려도 돼 · 시뮬레이션 부분은 블랭크로 · 시간 오버돼도 ETA 만"*).
- ✅ HBR6-01 · HBR6-03 수정 `6e7bce4b1` — 반례 넷 (gen 서명 · 면 수 · B 운동 계약 · 배너 끝) 을 셀프테스트로 먼저 옮겨 옛 코드에서 통과 (= 재현) 확인 → 35/35.
- ⬜ 믹서 남은 코드: Q1 관문 ↔ 판독기 차등 시험 (8 경계) · `all` 정책 ID · Q2 순서 불변 비교기 (HBR5-04 — np20 영수증용) · Q5 M-맹검 스모크 래퍼 → 등록 (D-1 §5-3 + Q4 + HBR6-02 불변량) → Codex 7 차 → ibb.
- ✅ **09-29 Q1** — `scripts/mixer_gate_reader_diff.py`: Codex 6 차 §3 의 경계 8 사례 (bin 0 복제 · 격자 밖 · E0 t₀ 복제 · bin 1 복제 · 후속 프레임 · 비정수 주기 1200/1240) 를 리포 모듈로
  다시 만들어 **관문 (launch_highbo.sh rest 파이썬 블록 추출) rc ↔ 판독기 analyse** 를 짝으로 단언 + 기록 2 (Q5 허용목록 투영 rc 0 · 증서 plan 변조 = 신뢰 경계) + **변이 판별력** (관문 bin 식 epsilon
  0.5 로 바꾸면 1200 복제가 rc 0 → 잡힌다).  12/12 · 4.5 s · 등재.
- ✅ **09-29 `all` 정책 파일** (Codex 6 차 §7-2) — `dem_scripts/mixer_20260921/launch_policy.json` (`Q8-2026-09-29-first-smoke-rest` · allowed = first · rest) · 런처 `policy_allows` 관문 (first · rest · all 전부) ·
  봉인 `policy` {file · sha256 · id · allowed} · HA⑧ (기본 정책 + DEVIATION → all 거부 · sbatch 0 · 봉인 0) · HA⑧b (모양 아님 · 파일 없음 → fail-closed) · HA③ 에 정책 기록 검사 → 런처 **100/100** (옛 98).
  ⚠ 옛 코드에서 HA⑧ 이 실패 (all 이 DEVIATION 만으로 열림) 하는 것을 먼저 확인하지는 않았다 — 옛 런처에 정책 개념이 없어 반례가 곧 HA② 자신이다 (98/98 판에서 HA② 통과 = DEVIATION 만으로 열림).
- ✅ **09-29 Q5** — `scripts/mixer_smoke_blind.py`: bin 0 스모크 M-맹검 래퍼 — 판독기 stdout/stderr 가로채기 · **허용목록 투영** (run · provenance · plan · t0_step · smoke.complete/tech_smoke/qc_repr.pass = 관문이 읽는 전부) ·
  전체 결과 `<런>/.smoke_blind/full_<µs>.json` 0600 봉인 ("계산했지만 보지 않았다") · 열람 기록 blind_log.jsonl · 거부/예외/누설 = 화면에 사유 코드만 · plan/t0/provenance 편집 없음.  selftest 11/11 (관문 rc 0 · 복제 → complete=false → 관문 1 · E0 t₀ 둘 → 거부 코드만 · 숨은 결과 키 → Leak 거부 · 모양 다름 · Traceback 비노출 · CLI).
  ⚠ 봉인 파일을 여는 것은 사람의 규율 — 등록 문서에 실패 · 교체 규칙 (QC 실패를 빌미로 유리한 시드만 남기지 않는다) 과 unblind 시점을 적는다.
- ★ **09-29 저자 결정 (믹서)**: D-1 · 재실행 범위 = *"Codex 리뷰 권고대로 · 내가 판단할 근거는 없어"* → 1 % 유지 · §5-3 최소 설계 등록 (b_E 0.02 는 내 제안 · Codex 검토) · Q4 같은 환경 삽입부터 새 LC×3 + LH×3 (WSL LC = 역사적 보조) ·
  *"ibb 에서 돌려야 되는 거 있으면 다 병렬로 코어 분배해서 한번에"* → 전 런 한 번에 제출 (같은 rank 수) · 나머지 시드 job 은 `--hold` 로 잡아 첫 시드 bin 0 M-맹검 스모크 뒤 release (§9 D-4 순서 유지 · Codex Q4 마지막 문단).  등록 문서에 적는다.
- ✅ **LHS 접촉 감사 WSL v1 실측 (09-29 · 1저자 · `~/dem-audit` 워크트리)** — 첫 시도는 내 명령 블록이 브랜치를 막지 않아 evac 체크아웃에서 실패 (합쳐진 것 없음) → 워크트리로 재실행.
  130/130: 프레임 1 · 중복 0 · δ≤0 0 · 플래그 누락 0.  FLAG 113 = 감사기 v1 폭 결함 (`SELF-63`: 0.01 nm < 덤프 6 유효숫자 반폭 0.05 nm) · `029`·`098` 플래그만 4,065·5,024 행 =
  LIGGGHTS `is_periodic_ghost` 띠 (MPI 고스트 · `LHS-16` · 소비자 없음).  ⇒ **v2** (비준 *"비준이고 너가 자기리뷰를 받아봐봐"*): 반올림 폭 실측 판별 ①②③ (양쪽 쌍 δ 대조는 새 검사) ·
  고스트 띠 + 최소 균일 격자 · 덱 없으면 fail-closed — 반례 먼저 (⑫–⑮d) → 24/24 · 합성 6 만 입자 %g 침대에서 반올림 쌍 2 · CLEAN · 1.7 s.
  **자기리뷰 (적대 서브에이전트) 12 항** — P1 둘 (분할면 위 토큰 → false-red · NaN δ → false-green) 포함 전부 반영 (J20-a 절) → 34/34.
  ✅ **WSL v2 실측 (09-29 · 1저자 · `acab799c4` · rc 0)**: 130/130 CLEAN · far 0 · δ 불일치 0 · 반올림 쌍 114 건 (최대 1,090) · 유효숫자 6 · 029/098 플래그만 행 전부 설명됨
  (1x1x24 · 1x1x30 · 예측 누락 0) ⇒ **① 접촉 위상 묶음 인계 적격** (J20-a ① 판정표) · SELF-63 verified · LHS-16 claimed_fixed.  ⬜ JSON 반입 · ② 퍼콜레이션.
- ★ **② 퍼콜레이션 1차 감사 (09-29 · 비준 대기 · J20-b)** — 코드 정의 판독 (`calc_percolation` · `build_network` · `calc_se_se_cn` · 수확기 `percolation` · `tortuosity_se` 벽 밴드) + 읽기 전용 검사기 `scripts/lhs_perc_audit.py` (반례 먼저 · 23/23 · ~1 s).  발견 F1–F8: 경계 폴백 L1/L2 **미기록** (`LHS-17` P2) · 겹침 인공물 · 전자 overlap 미병합 (`LHS-18` · LHS 기하상 0 건 — 여유 최소 +1.47 µm lhs00_075) · 열 뜻 (`LHS-19`) · census 오분류 (`LHS-20`) · 바닥 z = 0 암묵 · 수확기 AM perc ≠ 웹앱 전자 관통 (정의 다름 · 2×2 귀속) · 상자 0.05 기본 (τ 이월) · 단분산 SE 면 웹앱 L0 = 수확기 벽 밴드.  판정 규칙 선등록 (J20-b ⓑ).  ⬜ 비준 → WSL 실행 (ⓐ 명령) → 판정 → ③ φ_SE.
  ✅ **적대 자기리뷰 (서브에이전트) 9 항 반영** (P2 5 · P3 4 · 반례 먼저 · 32/32): 중복/자기쌍 FLAG · 선언 수 대조 · 전자 분율 정본 `active_fractions` 추출 (NC 29/29) · `_xcheck` 네 칸 규칙 ·
  빈 감사 rc 2 · legacy 파싱 엄격 · 예외 행 기록 · 메시 sha · 문서 서술 셋 정정 (`SELF-64`: input_params.json 은 배치가 **만든다** · 겹침 수는 **둘 다** 미병합).
- 믹서 본 캠페인 진행 (1저자 watch 09-29 01:57 KST): E0 3/3 완료* · L0 91 % · LA 84/84/85 · LB1 85 · LB2 86 · LB3 81 · LC 84/85/87 (덤프 169–189) · 메모리 available 12 Gi
  ⇒ 완주 ≈ 09-30 새벽~오전.  두 캠페인 (WSL 본 · ibb 확장 18 런) 은 별개 — 확장 LC 는 같은 환경 대조군이고 본 캠페인 결론에 영향 없음 (1저자 질문에 답함).
- ⛔ **Codex 7 차 (09-29) = HOLD (확인 18 런) · DEV-ONLY 조건부** — 등록 초안 발송 09-29 (첨부 = `ea7cfef96` 판 마크다운 제거본 · SHA 011f7ea8… · 내용 동일).  반입 `docs/reviews/codex_review_mixer_highbo_round7_prereg_20260929.md` + 증거 · **재현 118/118** (우리 HEAD · baseline blob = HEAD 생성기 · 부동소수 1 항 끝자리).
  수용: Q1 F₀ 쌍별 보존 (조건부) · Q2 b_E 정책값 · Q3 n=3 (검정력 미보장 — σ_q .005/.01/.02 → 통과 86/32/6 %) · **Q4 holdout 겸용 동의 · 6 차 §5-3 ⑩ 무조건 코호트 분리 정정** (추가 코호트 0) · Q6 held 제출 · Q7 개발 선행 (기술 선행조건 뒤).
  반례 `HBR7-01`~`06`: E0 검사로 bin 7 ref 인증 불가 (S_R² 1 % → M .117) · soft 1 % 강제 ↔ 계약 밖 비교 충돌 · q 동등성 ≠ 같은 결론 (q̄ −.015 통과인데 soft .086 MID 미달) · u 미정의 · SE 고정 (.04/.14/.24 → .02/.12/.26 실패) · 영구 실패 ↔ unblind 모순 · 벽시계 불변 반례 (11 → 15 h).
  ✅ 등록 **v2** (§0-b 판정 반영 · 개정 이력 · 값은 불변) · 원장 6 건 + HBR6-02 (설계 타당 · 구현 열림) · 모체 §0 Q8 · CLAUDE.md.  ⬜ **저자 결정 D-2** (주장 축소 [권고] vs refinement +18 런) · ⬜ 코드 선행조건 → DEV-ONLY → Codex 8 차.
- ⏱ **ETA (어림 · 09-28 밤)**: 코드 ≈ 09-30 · 등록 + Codex 7 차 GO ≈ 10-01~02 (HOLD 한 번마다 +1–2 일) · ibb 약 11–12 일 (부드러운 LC×3 + LH×3 ≈ 82 h [두 차례 × 41 h/런 추정] + 단단한 팔 6 ≈ 180 h [step ×2.25 추정] + E0) ⇒ **결과 ≈ 10-14 ~ 10-20**.  10/2 보고서의 믹서 절은 블랭크 (1저자 *"시뮬레이션 부분은 블랭크로"*).
- ✅ **② WSL 실측 (09-29 · 1저자 · `c0c2d4f44` · rc 0 · 309.7 s · 한 건 1.4–5.9 s)**: 130/130 CLEAN · SE·AM 밴드 L0 130/130 (폴백 0) · 겹침 0 (SE·AM·수확기) · 재현 = 정본 130/130 · 2×2 SE agree 130 · AM agree 128 + `prod_differ:band` 2 (`107` · `110` = 수확기 슬래브만 비관통 · 인계 열 아님) ·
  SE 관통 106/130 (비관통 24 = 09-19 진단과 같은 집합) · AM 관통 130 · legacy 127 중 불일치 1 = `lhs00_009` (`LHS-04` 그대로 · 웹앱 밴드 규칙 ≠ 솔버 전극 규칙).  ⇒ **② 판정 (규칙 ⓑ) = 명목 정의 그대로 인계 적격** (J20-b ② 판정표 · ⓒ 열 사전 문구 초안 = 생성기 반영 비준 대기 · ⓓ `LHS-20` 저자 결정).
  ⚠ 화면 요약 `box_default_cases: 0` 은 감사기 낡은 키 (`SELF-65` · 항상 0 = 규율 ⑤ 부류) → 반례 ⑭e 를 먼저 심어 옛 코드 실패 확인 뒤 `box_not_lhs_rve_cases` 로 수정 (33/33).  `SELF-64` claimed_fixed (`c0c2d4f44`).  ⬜ TSV/JSON 반입 `docs/data/lhs_perc_audit_20260929/` · → ③ φ_SE (코드 정의부터).
- ★ **09-29 밤 저자 결정 D-2 = (중간)** — 권고 (1) 기각: *"안돼 주장축소하면 이게 차이점이 없잖아 … 중간이라도 해서 결과를 내는게 좋을거 같은데"* · *"우리 믹서 목적은 코팅의 효과를 확실하게 보여주는거야"*.
  ⇒ 등록 **v2.1** (§0 · §0-b · §4-d): 개발 seed 1 (32452843) 에서 `LC_ref` · `LH_ref` 8 바퀴 (짧은 런 연장) + `LC/LH_ref2` (SE ×28) + `LC/LH_ref@dt/2` = 긴 런 6 · r₁ = d₁(ref) − d₁(ref2) · t₁ = d₁(dt) − d₁(dt/2) ·
  **탈락선 |r₁| · |t₁| ≤ 0.05** (정책값 · MID 절반 · Codex 8 검토) — 넘으면 확인 런 전에 수준을 올려 재봉인 (Q4 ⑤) · 통과해도 확인 주장은 (1) 그대로 (n=1 · 자격화 아님 · 개발 증거로 병기).
  목적 문장 §9: 헤드라인 = LC (코팅 대리 = AM–AM 점착 제거) ↔ LH contrast d · 강성 축은 보조축 · "실제 코팅 효과" 금지 유지.  개발 블록 11 런 (E0 5 + 긴 런 6) · ETA 결과 ≈ **10-28~11-05** (+2 주 · NP 실측 뒤 갱신).
  원장 HBR7-01 note · 모체 §0 Q8 · CLAUDE.md.  ⬜ 코드 선행조건 → DEV-ONLY → 탈락선 판정 → Codex 8 차.
- ✅ **Codex 8 차 요청서** (09-29 밤 · *"codex한테 리뷰 다시 받자"*) `docs/reviews/codex_mixer_highbo_round8_request_20260929.md` — 등록 v2.1 (sha256 4a9ec223…) · 질문 Q1–Q6 (τ 0.05 · 궤적 갈림 · 탈락 뒤 절차 · 8 바퀴 연장 · 목적 문장 · NP) · 확인 GO 아님 (DEV-ONLY 11 런 + §4-d 규약 검토).  발송 = 사용자 (기록은 확인 뒤).
- ★ **LHS (09-29 밤 저자)**: ③ 으로 가지 말고 **① 접촉 위상 값을 130 + 64 에 열마다 설명하며 저장** · porosity 는 union 만 배포 (J20-c).  현황: 인계표 09-28 = 설계 + φ · coverage · porosity 5 규약 · 두께 3 규약 (① ② 열 없음) · 64 는 수확 · union 만 (설계 스키마 다름 → 어댑터 필요).
  ⬜ 비준 ⓐ WSL 재수확 v3 + 웹앱 배치 (130 · 64 · [4] 인계표 재생성은 안 돌림) ⓑ 생성기 `--webapp-groups contact` + lhsx 어댑터 (반례 먼저) ⓒ 배포 프로필 (union exact + se_rich · mass-conserving 두께).
- ✅ **LHS 체크리스트** `docs/lhs_handover_checklist_20260929.md` (1저자 09-29 밤 *"확보할 거 · 넘겨줄 거 표로"*) — 묶음별 130/64 상태 · 할 일 8 · 배포 묶음 제안 · union 만 넘기는 이유 · ① 열 한 줄 설명.
- ★ **09-29 밤 마감 결정 (v2.2)**: 저자 *"10월 11일까지 데이터 완성 · 더 압축 안 되나"* → 산술 (ref 팔만 ≈ 8–9 일 · 확인 18 런 ≈ 11.5–12 일 · +선별 ≈ 23 일) 보고 → 저자 *"날 별로 차이 안 나면 확인 18 런 해도 되고"* ⇒ **확인 18 런 먼저** (코드 10-01 · Codex GO · 발사 10-02 가정 시 결과 ≈ 10-13~14) · D-2 선별 6 긴 런 **후행** (사후 강건성 검사 · Q7 · ≈ 10-25).  등록 v2.2 · 요청서 갱신 (Q7 추가 · 발송 가능) · 모체 · CLAUDE.md · 원장 HBR7-01.
- ✅ **64 (lhsx) 인계표 생성** (09-29 밤 · 저자 *"64 도 진행하자"*): `scripts/lhsx_design_adapter.py` (14/14 · 정의는 생성 코드에서 · 입자 수 왕복 · 상자 50 확인) → `docs/data/lhsx_design_adapted_20260929.csv` → 생성기 export →
  `docs/data/lhsx_handover_20260929.csv` 64×121 (union 5.43–9.43 % · 두께 mass-conserving 25.0–44.7 µm · se_rich 64/64 · hold NEGATIVE_POROSITY 60 = 규약) · J20-d · 체크리스트 갱신.  Codex 8 차 묶음 md (`codex_mixer_highbo_round8_bundle_20260929.md`) 사용자에게 전달.
- ✅ **복귀 병합 인계 (09-29 · 1저자 *"저쪽 origin 토큰 풀려서 이제 넘어가도 될듯 · 충돌 안 나게 머지"*)** — `docs/handoff_merge_to_stoic_knuth_20260929.md`: 실측 기하 stoic-knuth `b195ddb16` = merge-base · 이쪽 39 앞섬 · 저쪽 0 ⇒ **fast-forward** (litdb 무침범) · 절차 ⓪–④ · 검사 표 · 넘어간 뒤 상태 표 · 프롬프트.  같은 커밋: 원장 `LHS-21` (mono 실측 AM 개수 미적재 · 130 30 · 64 16) · 체크리스트 mono 문구 정정.
  ⚠ 이 커밋 뒤 pqwtv8 은 **동결** (이쪽 세션은 더 커밋하지 않는다 — 커밋하면 저쪽 fast-forward 가 다시 필요하다).

## ㉙ 2026-09-29 오후 — 병합 복귀 · Codex 8 차 반입 · v2.3 · 9 차 요청서 · 회사 보고 초안 (10-01)

- **복귀 병합 완료**: pqwtv8 → stoic-knuth fast-forward (`7e0f751c8`) · 관문 69 ✓ (`litdb_promote --selftest` rc 124 = 네트워크 → 단독 재실행 rc 0) · push.  인계서 `docs/handoff_merge_to_stoic_knuth_20260929.md` 대로.
- **Codex 8 차 = HOLD · 순서 조건부 수용** — 반입 `codex_review_mixer_highbo_round8_prereg_20260929.md` · 증거 폴더 · **우리 HEAD 재현 15/15 (181 항 동일)** · 원장 `HBR8-01`~`04` open · `HBR7-01`~`06` §11 주석.
  ⇒ 사전등록 **v2.3** (sha256 `e7311197…` · 294 행 — §0-c 신설 · §4-d 선행 규칙 폐기 + 전이표 · §9 헤드라인 = 공동 개입 B · §2 fresh 8 바퀴 · §8-2 ⑥ prefix 조건 · §8-3 비용 범위 · 값 불변) + **9 차 요청서** `codex_mixer_highbo_round9_request_20260929.md`.
  ✅ **저자 결정 (09-29 오후 · *"너가 권고하는 걸로"*)**: ① 주장 범위 수용 (등록 (1) 과 같다) · ② NP 프로브 실측 뒤 · 팔/문턱 유지 · 마감 우선이면 후행 미실행 = "refinement 미측정" 표지 · ③ soft 허용 범위 = 미결 · 결과 전 배정 (Q6).  ⬜ 발송 = 사용자 (요청서 + v2.3).  ⬜ 모체 prereg §0 Q8 에 "AM–AM 제거 대리" 정정 표지 병기.
- **런 상태 (사용자 보고)**: WSL 믹서 본 캠페인 E0 3/3 · L 10 런 88–98 % (완주 ≈ 09-30) → 등록된 8×8×2 · 문턱 5 · HOLD 해소 (b) 로 판정 · v100 rep288 두 점 완주 (ps_10_0 두께 108.419 = 108.419 · Δln σ 0.000495 ✓ · **ps_7_3 e1173 EXIT=0 wall 9395 s — JSON 비교 ⬜**) · ps45 진행 (5_5_r45 e1538 완주 wall 15002 s · e1207 15:45 시작) · kgy 서버 일시 중단 → Phase A 100 GPa STEP3 상태 ⬜ 확인 (러너 SKIP 캐시 = 같은 OUTDIR) · ibb a5/a6 무관.
  ✅ "r075" = 순수 SE union 침대 `pse_r075_a` (SE 반지름 0.75 µm) — **네 침대 완주 · 판정 완료 09-28** (`pure_se_union_prereg_20260927.md` §6-1: Q1 **EDGE** 6.182 % · Q2 **LOOSER** +1.342 %p · Q3 **MODEL** · 하류 J19 구현).
  ⚠ 내가 적은 *"ibb 에서 완주 확인 뒤 Q1–Q3 판정"* 은 **낡은 서술**이었다 (사용자 정정 09-29 — ㉗ 의 *"r075_a 만 남았다"* 는 그 시점 기록).  원장 · prereg 를 먼저 봤어야 했다.
- ★ **회사 보고 자료 (납품 · 저자 09-29 오후)**: *"자료 관련해서 우선 10월 1일까지 초안"* · 주제 키워드 **"이종기술"** · 템플릿 pptx 업로드 (연구개발 추진 내용 칸에 넣으면 됨).  원본 = 세션 업로드 `11fad1f8-…3…2….pptx` · 사본 = 스크래치 `report_1001/template.pptx`.  ⬜ **다음 컨텍스트에서**: 템플릿 슬라이드 구조 읽기 → "연구개발 추진 내용" 초안 (주간보고 `docs/worklog/weekly_20260927.md` · Phase A ORDER-ROBUST · Lee 대조 Tier 1 · LHS 인계 130 + 64 · 믹서 · MPM 하중분담 · SELF-45 원고 회신 — 인용 금지 값 제외 · ban-sweep) → 10-01 초안 → 비준.  ⚠ 원고 값은 `claims.json` `quotation_ban` 대상을 넣지 않는다.
- ★ **저자 역할 (09-29 오후 · 회사 보고 "이종기술")**: **(1) 미세구조 시뮬레이션** — DEM 설명 · 전극 3D 결과 · porosity (전해질 비 · 바이모달 비 · 활물질 크기) · tortuosity · 전도도 → *"바이모달 7:3 이 좋다"* 로 · **(2) 건식 전극 믹싱 시뮬레이션** — 활물질/전해질 응집 구현 · *"코팅으로 활물질 표면 물성 변화 → 균일성 향상 가능"*.
  ⚠ (2) 는 사전등록 한정어를 지킨다 — 믹서 본 캠페인 미판정 (완주 ≈ 09-30) · 고-Bo 는 HOLD · *"실제 코팅 효과"* 문장 금지 (모델 안의 점착 개입 · LC ≠ AM–AM 제거 · HBR8-02) ⇒ 초안은 *"모델에서 점착을 낮춘 조건이 균일성을 높이는지 보는 중"* 으로 쓰고 결과 칸은 판정 뒤 채운다.  (1) 의 "7:3" 은 코퍼스 실측 (P:S 스윕 · Furnas dip AM 70–85 wt%) 으로만 · 철회값 · 인용 금지 값 제외.
- ★ **동료 요청 (09-29 16:25 · 작은태영)**: 저번 **r4.5 침대 5 개 (kit_ps_{0_10,3_7,5_5,7_3,10_0}_r45 · Poly 9 µm) 의 porosity 를 union 규약으로** 계산해 보내기 (구 부피 합 아님 — LHS 인계와 같은 규약 · `docs/data/lhs_union_20260927/` 도구).  ⬜ 다음 컨텍스트: union 스크립트 · r45 덤프 위치 확인 → WSL/v100 명령 → 값 5 개 + 규약 한 줄 (union = 상한 규약) 로 전달.
- ★ **r4.5 union 명령 (09-29 오후 · 동료 요청 · 웹앱 PC)** — 케이스 = ps45 prereg §5-B 킷 표 (웹앱 `input_6mAh_real_{1..5}_D9` · 업로드 덤프 atom 3,640,000 · 3,220,000 · 2,930,000 · 3,210,000 · 3,210,000 · 전부 10,000 배수 = 접촉 덤프 간격과 맞음).
  덱 `p p f` · 바닥 `zplane 0.0` · 상자 0.05 정사각 = 도구 전제와 같다 · `--n-types 3` (다섯 덱 모두 type 1 AM_P · 2 AM_S · 3 SE 선언).  업로드 폴더를 `--scan-root` 로 (같은 step 의 atom · contact · mesh 가 다 있어야 · 없으면 MISSING = fail-closed).
  전달 값 = `mc_void_pct` (정확 union · 상자 [0,Lx)×[0,Ly)×[0, 플래튼)) · ± `mc_void_se_pct`.  ✅ **결과 (09-29 오후 · OK 5/5)** — union 정확 10:0 16.90 · **7:3 16.49** · 5:5 17.67 · 3:7 18.67 · 0:10 20.59 % (± 0.02 · 구 부피 합보다 +1.1–1.5 %p · 겹침/상자 중앙 1.45 %) · delta 검산 1.99e-3 · 저장 `docs/data/ps45_r45_union_20260929/` + COMSOL 인계문 `HANDOVER_COMSOL.md` · ⚠ 조성당 침대 1 개 (시드 산포 미측정) · ⬜ 전 열 TSV 반입 (상별 `mc_*`).
- ★ **Codex 9 차 묶음** `docs/reviews/codex_mixer_highbo_round9_bundle_20260929.md` (요청서 + v2.3 전문 + v2.2→v2.3 diff + 원장 HBR8 · HBR7 · PART 1·2 바이트 동일 검산) — 발송 = 사용자.
- ★ **보고 자료 방침 (저자 09-29 오후)**: 참고 스토리라인 = 한양대 L&F 진도점검 PDF (목표 → 입력 물성 → 설계인자 → 기준 구조 결과 → 영향 분석 → 데이터셋 · ML → 설계안 → 요약) · **DEM 식은 PowerPoint 네이티브 수식 (OMML) 으로** — 저자가 직접 고칠 수 있게.  템플릿 = 3세부 2차년도 진도점검 (슬라이드 8 · 9 = "2차년도 연구개발 추진 내용" 자유 양식).
- ★ **10-01 보고 초안 v1 (09-29 저녁)** — `docs/report_20261001/report_20261001_draft.pptx` (템플릿 "2차년도 연구개발 추진 내용" 자리에 2-1 ~ 2-11 · 생성기 `build_deck.py` · 수식 = OMML 네이티브 · 차트/표 네이티브).
  근거: 사양 5 조성 union (7:3 최소 16.49 %) + 130 설계점 보정 편차 (전해질 부피분율 · 입경 보정 R² 0.86 — 7:3 −16.9 % · 입경 보정을 더해도 −15 % · 0:10 +11.7 % · 탐색적).
  ⬜ 2-5 · 2-8 전도도 · 굴곡도 = 웹앱 PC `extract_r45_metrics.py` 결과 대기 · ⬜ 2-5 그림 두 자리 (3D 뷰어 캡처) · ⬜ 2-10 믹싱 결과 (09-30 완주 뒤).
  ⚠ 2-9 드럼 단면 = 옛 덱 (09-20) 예시 · 옛 요약 (c) 막대는 싣지 않음 (철회된 "문헌 앵커" 라벨 · 옛 세대 수치).  ⚠ 렌더 검사는 LibreOffice (수식은 평문 대체로 보임) — **PowerPoint 에서 수식 열림 확인은 사용자 몫**.
- ★ **Codex 9 차 (09-29 저녁) = 새 P1 없음 · 문서 해제 (범위 한정) · 확인 18 런 HOLD 유지** — 반입 `codex_review_mixer_highbo_round9_prereg_20260929.md` · 증거 폴더 · **우리 파일로 재현 188 항 동일** · 원장 HBR8-01~04 · HBR7-01~06 에 §8-2 문서 상태 주석 (전부 open 유지).
  요지: HBR8-01 핵심 닫힘 · 잔여 = §0 P:14 옛 근거 문장 · HBR8-02/03/04 문서 범위 닫힘 (덱 · 구현 · 비용 증거 별개) · DEV7 은 soft 미정으로 막히지 않음 (ref/ref2 만) · 확인 18 런 = soft 범위를 **발사 봉인 전** 확정 (겹침 QC 를 보고 고르면 M-맹검이어도 사후 선택).
  ⚠ **내 권고 ② 정정**: "마감 우선이면 후행 6 런 미실행" 은 확인 18 런 완료 시간을 줄이지 않는다 (긴 12 런 하한 266 h > 240 h 그대로) — NP 프로브 뒤 마감 연장 또는 설계 변경 (새 estimand) 을 저자가 명시 결정.
  ⬜ 비준 대기: v2.4 문구 정리 (Codex §9 최소 교체문 5 · P:14 · P:51 · P:105/113 · P:153 r·t 경계 · P:167 · P:239 · 8 차 baseline 수치 표지 · P:294 · 요청서 "확인 대기") + 모체 §1-3 정정 표지 · ⬜ 저자 결정: DEV7 순서 (E0 진단 먼저 → LC_ref/LH_ref 회전 권고) · soft 범위 값과 근거 (확인 발사 전).
  ⚠ 관문 첫 실행에서 믹서 런처 시험 1 건 실패 → 단독 100/100 · 재실행 전체 통과 (논문 에이전트 둘이 CPU 를 쓰는 중 · 일시 현상으로 기록 · 재발 시 추적).
- ✅ **kgy Phase A 재현 = 무사 (09-29 20:22 KST 읽기 전용 점검 · 사용자)** — SSH 만 끊겼었다: uptime 101 일 (재부팅 없음) · 러너 `sdcp_gain_vox015_8arm.sh` 살아 있음 (PID 3619897 · 5 h 52 m · 자식 3683383) · GPU 100 % · 7.5 GB.
  진행 = 등록 순서대로: G100 v015 **완주** (09-28 09:31 · 33 파일) → G010 v015 **완주** (09-29 08:28 · 33) → QC **완주** (14:29 · 9) → **G100 v020 진행 중** (14:30 발사 · 19 파일 · 최근 `2_1_a4` · origin [0.1,0,0] · 21.8 M dof ≈ 19 min/팔) → v025 대기.  ⛔ 재개 · 재발사 불요 (`$(date)` OUTDIR 함정 — 다시 치면 새 폴더에서 처음부터).
  ⬜ v020 완주 (≈ 09-30 01:00) · v025 (≈ 07:30) 뒤 §6-4 영수증 · 어댑터 · 판정 (질문 1–3) → `docs/data/phase_a_rep100_2026MMDD/` 커밋.
- ✅ **믹서 v2.4 (09-29 밤 · 저자 위임 *"너가 권고하는 걸로"* · *"긴 확인 12 런만 최소 266 시간 — 진행하자 · ETA 만 확실하면 됨"*)** — Codex 9 차 §9 문구 그대로 · DEV7 순서 (E0 5 → 회전 2 · NP 프로브 = E0_ref 첫 시드 NP 5/10/20 1 h) · soft 진단 범위 **5.8 %** (1 % × 14^(2/3) · F₀ 보존 · 초과 = OUT_OF_RANGE · 범위 불변) · 확인 18 런 진행 · 10-11 달성 불가 명시 · **가정 ETA 10-16 ± 1 (최악 10-20 · 후행 ≈ 10-27)** · 값 불변.
  ⚠ 코드 선행조건 실태: `--stiffen-se` · `--hold-bo-pairwise` **0 건 (미구현)** · policy first-seed-block **0 건** · `--allow E` 있음 (11) ⇒ **다음 컨텍스트 = 코드 착수** (반례 먼저 · 09-30 ~ 10-01).  ⬜ 모체 §1-3 정정 표지.
- ✅ **litdb 정본 2 장 (09-29 밤 · 에이전트 · 검증 = FETCH_HEAD 에 파일 · 그림 37 장)**: `hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd` (`00500b599` · 본문 8 + SI 13 + 표 1 · ⚠ 문턱 라벨 불일치 — 평면/다공 수치는 84.8 mV 기준으로 재현 · "0.4 µm 기준" 인용 금지) · `eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell` (`54ff32184` · 15 장 · 벡터 판독 · ⚠ C/2 충전 RMSE 표 7.4 ↔ 그림 11.7 · 반경 불확도 인자 2 — 저자 확인 전 인용 금지).  ⚠ 정본 `_sources.json` 의 `wang2015_graphite_cleavage_energy` 그림 수 9 ↔ 실제 10 (낡음 · 담당자 수정).
- ✅ **v2.5 중간 판정 (09-29 밤 · 저자 *"8 바퀴를 다 돌리면 좋겠지만 중간에 끊어서 효과가 유의미한 거 보면 들고가도"*)** — §5-a: 4 바퀴에 한 번만 · 세 seed 양수 ∧ Δ3 − u ≥ 0.10 ∧ ≥ 3·(SE3 + u_SE) · 충족 = 4 바퀴 estimand 조기 확정 · 미충족 = 8 바퀴 최종 그대로 · 무익 중단 없음 · 12 런 동시 같은 NP (NP 5 × 12 후보 · 프로브 뒤) · ETA 중간 ≈ 10-10 ± 1.  ⬜ 코드: 판독기 · 래퍼에 bin 3 중간 투영 · Codex 검토.  ★ 코드 1 단계 (생성기 `--stiffen-se --hold-bo-pairwise` · `--dt-factor` · 되읽기 표 B/E · `--allow E` 보강 · DEV 덱) = 구현 에이전트 진행 중.
- ⚠ **LHS φ 권고 정정 (09-29 밤 · 1저자 *"φSE 코드 문제 다시 · 뜻 · 에이전트 도는 동안 LHS 집중"*)** — 판정문 J20-e · 체크리스트 §1 · §6.  φ = 재료 부피 ÷ 두께인데 수확 열은 **DEM 판 간격 H** 로 나눴고 넘기는 두께는 **질량 보존 H_mc** (J19 ②) 다 — 장부 섞임 (계산 결함 아님).  앞 판 ★ (가) (union 점유 · 겹침 = AM) 는 **철회** — H 상자 안 점유율이라 H_mc 와 섞으면 AM 적재량 +3.2 % (130 중앙 · 최대 +10.7 %) · +11.2 % (64 중앙).  새 권고 **(라) φ_i = V_i/(L²·H_mc)** — union 닫힘 잔차 0 (194/194) · 적재량 = 레시피 · SE/고체 = `se_of_solid_vol`.  ⬜ 저자 결정 → 생성기 열 (반례 먼저).  J20-c WSL 명령의 브랜치 pqwtv8 → stoic-knuth 로 정정 표기.
- ✅ **믹서 코드 1 단계 완료 (09-30 · 에이전트 · 검증 = 내 재실행 102/102 · 21/21 · 35/35 · 브랜치 = 원격)** — `83ca909c3` 생성기 · `ea3b27ddc` 되읽기 · `790ddf84c` `--allow E · EB` · `8a0e5b721` 되읽기 문서 · `fe27cedbf` DEV 덱 7 + 증거 (`SHA256SUMS` 55 · `build.sh` 두 번 같은 산출).  dt ×14 3.132e-07 (배수 2.252512 = Codex 2.2525 · √14 아님 — soft dt 는 AM_S 가 정한다) · CED 배수 9 자리 일치 · 기본 옵션 바이트 동일 (09-28 E0 덱 3 개와 같다).  ⚠ 정정: 내가 적은 *"`--allow E` 있음 (11)"* 은 **틀렸다** (문서 속 인용 11 건을 셌다 · 코드는 `choices=A,B`) — prereg §8-3 · CLAUDE.md 에 정정 표기.  ⬜ 2 단계: 정책 `dev` · `--runs` 새 이름 · `expected_deck()` 강성 옵션 · 스모크 필드 · bin 3 투영 · E0 프레임 수 385 → 867 (×14) 디스크 · 생성기 주석 *"dt 는 가장 작은 SE"* 틀림.
- ✅ **LHS φ = (라) 만 (09-29 밤 · 1저자 *"왜 전체에 대해서 뽑고 있는 거야 · φ 는 (라) 에 해당하는 것만"*)** — 생성기 `phi_se_mass_conserving` · `phi_am_mass_conserving` (반례 먼저 84/90 → 90/90) · `lhs_handover_20260929.csv` 130×121 (새 · 열 사전 첫 생성) · `lhsx_handover_20260929.csv` 64×123 · 옛 칸 변경 0 · 닫힘 ≤ 3.3e-16.  ⚠ ① 은 웹앱 **전체**가 아니라 접촉 분석 단계만 (1저자 *"단독적으로 하나씩 돌려서 표를 채워나갈 거야"*) — 전체 한 건 시험: 수확 v3 2/2 OK · 웹앱 `partial` 2/2 (575.6 s · 743.4 s) = 대조 기준.
- ✅ **LHS ① 전용 실행 모드 (09-29 밤 · 1저자 *"ㅇㅇ 단독적으로 하나씩 돌려서 표를 채워나갈 거야"* · 반례 먼저)** — 웹앱 `run_pipeline(stop_after='contact')` (T10 · 182/188 → 188/188) · 배치 `--stop-after contact` (모드 섞기 거부) · 생성기 `--webapp-groups contact` (접촉 단계 산출 열만 · 90/95 → 95/95) · ⚠ ① 사전 중 `A_binding_*_n_contacts` · `n_am_am_contacts_*` 는 뒤 단계 산출이라 이 묶음에서 뺐다.  ⬜ WSL 한 건 대조 (접촉만 = 전체 실행 ① 값) → 전 건.
- ✅ **LHS ① 접촉만 한 건 대조 통과 (09-29 밤 · WSL `~/dem-audit` @ `e833a498d`)** — `lhs00_000` · `lhsx_001`: ① 22 열 값 다름 **0** (전체 실행 ↔ 접촉만) · porosity 같음 · 시간 29.3 s · 92.4 s (전체 575.6 · 743.4 s).  ⬜ 전 건: 수확 v3 130 + 64 → 접촉만 배치 → tgz 송부 → 생성기 `--webapp … --webapp-groups contact` 로 인계표 재생성 (① 열 + 열 사전).
- ⏸ **LHS coverage — 수확 전 점검 (09-29 밤 · 1저자 *"수확하기 전에 coverage 쪽으로 · 모순 없는지 · flag 에 의한 coverage drop · cap 도 인계용으로"*)** — 전 건 수확 **보류** (coverage 결정 뒤).  확인된 것: 인계 coverage = 수확기 `coverage_hertz` (A_dem_geometric · 입자 평균 · 입자수 가중 전체 · mono 는 P/S 빈칸) · 웹앱 `calc_coverage` 같은 식 (분모 ≤ 0 처리만 다름 — LHS 0 건) · 주기 플래그 `c_cpl[9]` 는 coverage 소비자 없음 + ① 감사 130/130 CLEAN (64 미감사) · 벽 접촉 면은 분모에 남는다 (AM–AM 은 빼는데 벽은 안 뺀다 = 불일치 후보 · 크기 미측정 → 수확기에 벽 접촉/안쪽 분리 후보).  **cap (physics) coverage** = 09-19 census 🔧 — 원장 `DESC-03` (단위: 막 두께 SI ↔ 덤프 ×1000 · 부피 cap 1000 배 · 163/163 미결속) · `L1-01` (하한 > 상한이면 하한 반환) · `L1-02` (부피식 0.494 배 · 깊으면 음수) **셋 다 open** · 코드에 계측만 있음 (`plastic_coverage.py:388–411` cap_conflict · V_lens_exact).  ✅ 1저자 결정 (09-29 밤 *"ㅇ 가자"*): **새 판 `_physics_v2` 병기** (코퍼스 · Stage E · σ_thermal T1 physics 타깃 보호) · `L1-01` = **상한** (충돌 시 cap).  ⬜ 확인 대기: cap = 전체 면적 한계로 읽는 것의 귀결 (physics < LIGGGHTS 기하 가능 — 옛 하한 원칙과 충돌) · 부피 = 전체 lens (권고).  비판 리뷰 에이전트 (면적 리뷰 1–5 · L1 · L2) 결과 대기.  ⬜ 코드: `stop_after='coverage'` (접촉 → 피복 단계 · network 없음) 로 ① + cap coverage 한 번에.
- ▶ **09-30 새벽 진행 (컨테이너 재시작 뒤 · 1저자 *"권고대로"*)** — ① WSL 전 건 실행 중 (1저자): 수확 v3 130/130 OK → `docs/data/lhs_descriptors_20260929/` (현 수확기 · coverage 개선 **전**) → 접촉만 배치 130 진행 (건당 1.8–93.5 s · ETA ≈ 1 h) → 이어서 64 → tgz.  ⚠ 수확기 coverage 개선이 들어오면 **수확만** 다시 (웹앱 접촉 배치는 원자료 sha 같아 재실행 불요).  ② 에이전트 셋 (격리 worktree · push 안 함 · 끝나면 내가 병합): (a) 수확기 coverage — 벽 분할 + 벽 제외 coverage 새 키 · 접촉 면적 검산 (플래그 0/1) · 접촉 관문 (고아 행 기록 · 중복/자기쌍 거부) · 벽 규칙 하나로 · LHS-14 확인 (b) cap coverage v2 병기 — 단위 (DESC-03) · 전체 lens (L1-02) · 충돌 시 cap (L1-01) · 분모 같은 장부 · 조용한 대체 금지 · 충돌 수 전파 · `stop_after='coverage'` + 배치 선택지 (c) 믹서 2 단계 남은 ④ (bin 3 중간 투영 · 두 번째 열람 거부) — 앞 에이전트는 재시작으로 끊겼고 ⑥ `e6465354b` · ② `e833a498d` · ③ `4b42179ec` · ①⑤ `e72067854` 은 커밋돼 있다.
- ▶ **09-30 새벽 — WSL 접촉 배치 mono 30 건 REFUSED → 관문 수정 (1저자 비준 · `SELF-66` · 판정 J20-f)** — 130 = done 100 · REFUSED 30 (`lhs00_100–129` = mono 전부 · 실행 전 거부 · 잘못 채운 값 0) · lhsx mono 16 건도 같은 관문.  원인 = 이름 규약 (수확기 `'AM'` ↔ 웹앱 반지름 이름 AM_S/AM_P) — 배치 `fold_single_am` (2-type 끼리 · 수확 {AM, SE} 일 때만 접기 · 웹앱엔 덱 판독 그대로 · `type_map_fold` 기록) · selftest ⑭–⑭f (옛 26/28 → 28/28).  ① 총량 열은 이름 무관 (AM 집합 = 이름에 AM) · ⚠ **상별 ① 열 (`AM_P/AM_S_se_cn_*` · `area_<쌍>_n`) 은 반지름 이름을 따른다** — 설계와 이름이 다른 mono = 130 의 5 (`118 · 121 · 124 · 125 · 126` · WSL 이름과 일치) · 64 의 4 (예측 `lhsx_003 · 017 · 048 · 062`) · 첫 보고의 *"① 에 상별 열 없음"* 은 틀렸다 (정정 J20-f) · ⬜ 저자 결정 (인계표 재생성 전): (A) 권고 mono 상별 = 빈칸 (coverage 와 같은 규약) / (B) 설계 이름으로.  다시 돌리기 = 같은 배치 두 명령 · 같은 `--out-dir` (REFUSED 만 돈다).  믹서 ④ 에이전트 완료 (`a7aa1672a` · 워크트리 · 검증 · 병합 대기) · 수확기 coverage · cap v2 에이전트 진행 중.
- ▶ **09-30 — 1저자 결정 셋 · 믹서 DEV7 발사 준비** — ① LHS: WSL 결과 (수확 v3 · 접촉만 배치 · 코드 `4b42179ec`) 는 **옛 코드 기준선으로 보관** → 수정 코드 결과와 비교 (1저자 *"그대로 두고 이 결과들을 나중에 수정한 코드로 나온 결과랑 비교"*) · 순서 = **코드 갱신 → 같이 확인 → 그 묶음만 실행** (coverage 먼저 · 첫 안내의 *"접촉만 = 접촉 단계만"* 이 14 분석 전체라는 것을 말하지 않은 잘못 — 1저자 지적) · 접촉 단계 함수 검토는 ① 값 함수부터 하나씩 (계면 개수 → SE–SE CN → AM–AM CN → AM 고립).  ② 수확기 coverage 에이전트 **완료** — 워크트리 `worktree-agent-a8425b12f9b01f5bb` 4 커밋 (item 4 `1dfae6661` 벽 닿음 규칙 하나 · item 1 `a2b0b5369` 벽 분할 · 벽 제외 피복률 (새 키만) · item 2 `69d7cb678` c_cpl[22] ↔ 정확한 교차 원판 대조 (진단) · item 3 `7d8f696fc` 접촉 행 문) · selftest 139/139 재확인 · **미병합 (하나씩 비준 뒤)** · cap v2 에이전트 진행 중.  ③ 믹서: 2 단계 ④ 병합 (`71488a043` ← 워크트리 `a7aa1672a` · 셀프테스트 셋 재확인 · 1저자 *"비준 해줘"*) · DEV7 ① `dev-e0` — 컨테이너에서 가짜 SLURM 으로 ibb 명령 그대로 사전 실행: 셀 5 생성 = 커밋된 DEV 덱과 바이트 동일 · 관문 1 코호트 dev-e0 PASS · 관문 2 preflight PASS · sbatch 8 (NP 프로브 `-n 5/10/20` · 1 h + E0 다섯 `-n 20` · 2 일 · QOS cpu-60 · partition cpu) · 디스크 추정 103.1 GB × 1.10 = 113.4 GB · OUT = ibb `$HOME/mixer_dev7_20260930` (리포 밖 · 멈춘 LH `runs/` 와 분리 · 1저자 비준) · LMP = 영수증 v2 ibb 바이너리 경로 · SB_PATH = 09-28 LH 발사 값.  ⬜ ④ 에이전트 등록 모호점 6 (ε_s bin 3 미등록 · 양수 엄격 · 조기 확정 적격 = bin 3 창 · M-맹검 부적격 비소진 · 봉인 뒤 TECH/INELIGIBLE 소진 · 적격 표 투영) = 확인 18 런 봉인 전 저자 결정 (DEV7 무관).
- ▶ **09-30 — ibb a5/a6 정지 (1저자 · 믹서 DEV7 자리 비우기)** — 정지 직전 기록 (1저자 실측): `a6_p04` job 241242 로그 1,797,000 · mesh 1,795,000 · 재시작 체크포인트 **1,750,000** (다시 돌 구간 ≈ 45,000 step) · `a5_p08` 241243 로그 3,665,000 · 체크포인트 **3,650,000** (≈ 15,000) · `a5_p10` 241244 로그 3,663,000 · 체크포인트 **3,650,000** (≈ 10,000) — 대기열 비어 있음 확인.  ⛔ 재개는 `scripts/resume_ckpt.sh` 로만 (CLAUDE.md 체크리스트).  · 믹서: `e854f0a51` 푸시 (④ + 기록) — ibb 첫 시도는 LH 런 폴더 안에서 쳐서 상대 경로가 전부 실패 (셀 0 · 발사 0 · 체크아웃만 `70e1203` 로) → 블록 첫 줄에 리포 루트 이동을 넣어 다시 드림.
- ▶ **09-30 — LHS 접촉 단계 함수 검토 1/4 · 체크리스트 §0 (이번 추출)** — 1저자와 `calc_interface_area` 검토 → ✅ 수정 불요 (1저자 *"오케이 이렇게 가고 추출해보자"*) · 이번 추출 = porosity union · 두께 (mass-conserving) · φ_AM · φ_SE (라) · 계면 개수 `area_<쌍>_n` (앞 셋은 표에 이미 있음 · 계면 개수는 tgz · 생성기 "확인된 열만" · mono 규약 (A)/(B) 결정 뒤) · coverage 는 코드 갱신 중이라 이번 추출에서 뺌 · cap v2 에이전트 **완료** (워크트리 3 커밋 `166b59724` · `d65afca14` · `59a0e1ecf` · 미병합 · 배치 selftest 번호 충돌 1 곳 · 새 결함 등재 필요 — 옛 피복 스크립트가 `WEBAPP_*_FOLDER` 무시) · 체크리스트 `docs/lhs_handover_checklist_20260929.md` §0 · §1 · §2 · §5 갱신.
- ▶ **09-30 01:34 KST — 믹서 DEV7 ① `dev-e0` 발사 ✅ (ibb · 1저자 실행)** — 셀 5 해시 = 커밋 DEV 덱 (`8cef2ffb · d59f5419 · d1ce202b · a08889d2 · 338bffbe`) · 관문 1 코호트 dev-e0 PASS (프로브 포함 8 · E 쌍 2 PASS) · 관문 2 preflight PASS (디스크 필요 103.11 GB × 1.1 ≤ 가용 136,930 GB) · 봉인 git `e854f0a51971` · lmp sha `ee2d77261bac…` (`/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi`) · OUT `$HOME/mixer_dev7_20260930` · job **244220** npprobe5 · **244221** npprobe10 · **244222** npprobe20 (1 h) · **244223** E0_ref_s32452843 · **244224** E0_ref_s49979687 · **244225** E0_ref_s67867967 · **244226** E0_ref2_s32452843 · **244227** E0_ref_dthalf_s32452843 (-n 20 · 2 일 한도).  QOS `cpu-60`: 첫 배정 = 프로브 셋 + E0 하나 = 55 CPU · E0 넷 `QOSMaxCpuPerUserLimit` 대기 (프로브 끝나면 E0 셋 동시).  다음 = E0 다섯 완주 → `mixer_smoke_blind.py --e0-diag` → PASS 면 `dev-rot` (LC_ref_r2 · LH_ref_r2 셀은 그때 같은 방식으로).  ⚠ NP 를 바꿔 60 CPU 를 다 채우는 안 (예: E0 12 코어 × 5) 은 발사 봉인 · fresh 규칙 · 블록 NP 통일 (dev-rot = E0 기록의 NP) 때문에 재발사가 필요 — NP 프로브 결과 (1 h) 를 보고 dev-rot · 확인 런의 NP 를 정한다.
- ▶ **09-30 — 생성기 J20-g (확인된 열만) · J20-f (A) (1저자 비준 *"권고대로"*)** — `WA_REVIEWED` (지금 `area_(.+)_n` 만) · mono 상별 웹앱 열 빈칸 (`n_types` 2 · 없으면 거부) · 열 사전 문구 · 시험 먼저 ⑳a–f (옛 96/101 → 101/101).  ⚠ **절차 실수**: 체크리스트 · 진행 문서 커밋 `c1541c0d3` 을 게이트 결과를 잘못 읽고 푸시했다 — 백그라운드 래퍼 (`…; echo "rc $?"`) 의 종료 코드 0 은 echo 의 것이고 게이트 로그는 ✗ (원인 = 그때 작업 트리의 시험 먼저 ⑳ 이 옛 생성기에서 실패 · 커밋에는 생성기 변경 없음 · 문서 둘만).  다음 전체 게이트 (생성기 포함) 로 확인 · 교훈: 게이트는 로그의 `✓ 전부 통과` 줄로만 판정한다.
- ▶ **09-30 02:07 KST — 층상 믹서 캠페인 완주 2 런 판독 (8 바퀴 · WSL · 판독기 `999a5bf85` 판)** — ✅ **음성 대조 L0 통과**: `planned.M_final` 16×16×4 0.9724 · 12×12×3 0.9934 · 8×8×2 0.9778 (전부 ≥ 0.8 · 평탄 ×3) ⇒ HOLD 아님 · 바닥 8×8×2 8.80 · 11.27 ≥ 5 · `LC_s67867967` 0.9975 / 1.0441 / 0.9229 (평탄 ×3 · 기술 보고 — 짝 LA 미완주) · D-2 QC 6/6 · 원자료 `docs/data/mixer_final_20260930/` · prereg §6 열람 기록.  ⚠ 첫 tgz 는 시스템 python3 에 numpy 가 없어 판독 0 건 (내 명령 잘못 — venv python 으로 다시).  다음 = 8 런 완주 → 10 런 한 판독기 판으로 다시 읽어 §2 판정 + §5 계약 한정어.
- ▶ **09-30 — LHS 접촉 단계 전 건 반입 · 인계표 재생성 (J20-g 적용)** — WSL 배치 130/130 · 64/64 done (1차 `4b42179ec` done 100 · 48 + mono 재실행 `27933b44e` · 두 커밋 사이 접촉 · 수확 코드 변경 없음) · 기준선 tgz ⊂ 최종 tgz (수확 차이 0 · done 행 공통 열 차이 0) → 원자료 `docs/data/{lhs,lhsx}_{descriptors,webapp_contact}_20260929/` (옛 코드 기준선 — coverage 개선 뒤 비교용) → `lhs_handover_20260930.csv` 130×133 · `lhsx_handover_20260930.csv` 64×135 (새 열 = `area_<쌍>_n` 7 + 상태 2 + QC 3 · 옛 칸 변경 0 · mono 상별 빈칸 60 · 32 · bimodal P+S = 전체 전부 · 같은 프레임 ≤ 2.5e-10 %p).  ⚠ 새 발견: 접촉 0 인 쌍은 웹앱이 키를 안 만들어 bimodal 에서 빈칸 (`area_AM_P_AM_P_n` 3 · 6 건 — AM_P 3–16 알) = 뜻은 0 → 1저자 결정 대기.  수확은 v2 로 불렀다 (v3 새 열은 같이 확인 전).
- ▶ **09-30 02:4x — 믹서 DEV7 NP 프로브 실측 (끝 15 분 · 쌓인 E0 침대)**: NP5 21.1 · NP10 41.1 · NP20 68.9 (node02 공유) / 77.8 (node01 E0) step/s · 세 프로브 `TIMEOUT` (1 h 한도 = 설계대로 · watch 의 `⛔죽음` 표시) · 60 CPU 처리량 NP5 253 · NP10 247 · NP20 207–233 · 확인 회전 12 (ref 6 × 21.29 M + soft 6 × 9.45 M step) 산술 makespan: NP20 3 슬롯 ≈ 220–248 h · NP10 6 슬롯 ≈ 208 h · NP5 12 슬롯 ≈ 1,009 h (ref 한 런이 42 일) — ⚠ 회전 없는 E0 값 (회전은 8–18 % 느림 추정) · 메모리 미측정 · prereg §8-3 기록 · ⬜ 확인 블록 NP = 저자.  E0 ETA (78 step/s 가정 · 추정): 첫 E0 ≈ 04:10 · 둘째 · 셋째 ≈ 05:40 · ref2 (1,227,503 step · 첫 E0 뒤 시작) ≈ 08:30 · dthalf (1,735,953 step · 둘째 뒤 시작) ≈ 11:50 KST.
- ▶ **09-30 — J20-h 접촉 0 쌍 = 0 (1저자 *"이렇게 하자"*)**: 생성기 `WA_PAIR_COUNT` (웹앱 행 있음 · 쌍 개수 열 · 값 빠짐 · 두 상 존재 → `0` · mono 상별 · 상 없음 = 빈칸 · `phase_counts` 없으면 거부 · REFUSED 행 제외) · 시험 먼저 ⑳g–l (옛 103/107 → 107/107) · 인계표 재생성 — 바뀐 칸 정확히 3 · 6 (`area_AM_P_AM_P_n` → 0) · 열 목록 그대로.
- ▶ **09-30 03:19 KST — DEV7 E0 진행 · 믹서 저자 결정 둘**: watch — `E0_ref_s32452843` 580,000 (66 %) · `s49979687` 240,000 (27 %) · `s67867967` 250,000 (28 %) · ref2 · dthalf 대기 · 순간 속도 ≈ 62 (첫 E0 · 115 → 94 → 78 → 62 로 계속 감소) · 69 · 71 step/s ⇒ ETA 첫 E0 ≈ 04:45 · 둘째 · 셋째 ≈ 05:50 · ref2 · dthalf 는 그 두 시각에 하나씩 시작 → **다섯 끝 ≈ 11–12 시** (dthalf 가 먼저 들어가면 11 시쯤).
  ✅ **확인 블록 NP = 20** (*"cpu20으로 하자 그럼"*) · **로컬 분배 기각** (근거 = prereg §8-3: §8-1 같은 환경 밖 · 로컬 런당 1 코어 → ref 한 런 11–18 일 · soft 만 로컬로 보내는 분할은 기계 ≡ 강성 수준 · WSL 정지 × 재개 금지) · ⬜ ibb 사용자당 CPU 한도 상향 가능 여부 = 1저자.
  ✅ **동시 실행 = 서로 다른 팔 · 시드 순서 제출** (*"같은거 시드 다른걸 한번에 하지말고 서로 다른걸 돌리자"* · prereg §8-2 ④ · 산술 비용 끝 +3 h · 중간 판정 1.4 h 빠름 · ⬜ 런처 코드).  DEV7 E0 는 E0_ref 세 시드가 이미 돌고 있어 **그대로 둔다** (권고 — 끊고 바꾸면 45 분 × 2 를 버리고 봉인 job 목록이 바뀌는데 줄어드는 것은 ≤ 1 h · 05:50 부터 ref2 · dthalf 는 어차피 같이 돈다).
  LHS: 09-30 판 인계표 4 파일 (130 · 64 · 열 사전 둘) → WSL Downloads (`~/dem-web` 에서 fetch + show · BOM +3 B · 크기 일치) · fetch 전 `origin/…` = `27933b44e` ⇒ 10 런 판독 첫 줄 해시는 `4375ec56c39a` 일 가능성 (두 판 analyse 경로 동일 확인 — `e0_t0_stats` · `bin_of` · `ROW_DIAG` = 옛 인라인 코드와 같은 식).
- ▶ **09-30 — LHS 접촉 ① 둘째 함수 SE–SE CN (J20-i · 1저자 *"비준하고"*)**: `calc_se_se_cn` 코드 수정 불요 · 평균 = 2 × `area_SE_SE_n` / SE 입자 수 130/130 · 64/64 차이 0 → 생성기 `WA_REVIEWED` + 항등식 관문 (어긋나거나 `phase_counts` 없으면 거부) · 시험 먼저 ⑳m–r (옛 107/113 → 113/113) · 인계표 재생성 130×135 · 64×137 (새 열 `se_se_cn` · `se_se_cn_std` · 옛 칸 변경 0 · 배치 원값 260/260 · 128/128) · 같은 함수의 나머지 8 열은 ② · ⑦ · ⑤ 차례 · 새 결함 `LHS-22` (F1 근접쌍 격자 탐색이 주기 영상을 안 봄 · 인계 열 아님).  1저자 새 진행 방식 (*"to-do 를 표로 · 코드 돌리고 · 결과 보고 · 문제 확인"*) — 할 일 표 10 항목 (1 = 믹서 결정 기록 ✅ `e6de920f7` · 2 = 이것 · 3 = coverage 에이전트 7 커밋 Codex 요청서 (1저자 제안) · …).
- ▶ **09-30 — 할 일 표 1 · 2 완료 (`e6de920f7` · `da4670594`) · 3 (coverage 에이전트 Codex 요청서) + 6 (AM–AM CN 검토) 동시 진행** (1저자 *"3번 할때 6번이랑 같이"*) · ibb 사용자당 CPU 한도 상향 = **불가** (1저자) → 확인 블록 NP20 3 슬롯 그대로 (prereg §8-3).
  3: 에이전트 7 커밋을 `da4670594` 위에 cherry-pick (로컬 `review-coverage-20260930` · 원 브랜치 · SHA 그대로) — 충돌 = `lhs_webapp_batch.py` selftest 번호 한 곳 (지금 브랜치 mono 접기 ⑭–⑭f 먼저 · cap v2 ⑮ · ⑯) · 셀프테스트 수확기 139 · plastic_coverage 27 · coverage 13 · 배치 29 · 파이프라인 198 · 생성기 113 전부 통과 · 요청서 `docs/reviews/codex_lhs_coverage_request_20260930.md` + 증거 폴더 (패치 7 · SHA256SUMS · 로그) · 질문 Q1–Q9 · 발송 = 1저자.
  6: `calc_am_am_cn` (`dem_analysis_core.py:347–375` → `analyze_contacts.py:452–458`) — AM 전 입자 (AM_P + AM_S · mono 는 AM) 평균 · P–S 교차 포함 · 모집단 표준편차 · `n_contacts` = Σ/2 · 대조 (커밋된 배치): `am_am_n_contacts` = AM–AM 쌍 개수 합 130/130 · 64/64 · `am_am_cn` = 2 × n / N_AM 130/130 · 64/64 차이 0 · 값 130 1.719–6.633 (중앙 5.148) · 64 0.438–3.970 (중앙 1.934) · `am_am_mean_area` · `am_am_total_area` 는 면적 (⑦ 차례) · ⬜ 1저자 확인 뒤 J20-j (세 열 + 항등식 관문 둘).
- ▶ **09-30 — 할 일 표 6 = LHS 접촉 ① 셋째 함수 AM–AM CN (J20-j · 1저자 *"6번 진행하자 코드 부탁해"*)**: `calc_am_am_cn` 코드 수정 불요 · 관문 둘 (`am_am_n_contacts` = AM–AM 쌍 개수 합 · `am_am_cn` = 2 × 총수 / N_AM · 실측 194/194 차이 0) · 시험 먼저 ⑳s–x (옛 112/119 → 119/119 · ⑳i 재료의 앞뒤를 맞춤) · 인계표 130×138 · 64×140 (새 열 3 · 옛 칸 변경 0 · 원값 390/390 · 192/192) · **mono 의 AM–AM 개수가 돌아옴** (30 · 16 행) · 면적 둘은 ⑦ 차례.  3 = Codex 요청서 · 증거 폴더 커밋 (1저자: 추론 단계만 받음 — 차분히 커밋).
- ▶ **09-30 — 7번 AM 고립 검토 · J20-k 결정 (1저자 *"권고하는대로"*)**: 대조 전부 차이 0 (상별 · 전체 평균 × 입자 수 = 계면 개수 · 표면 가중 = 설계 반경 항등식 · 고립 비율 = 개수 가중) · (C) 웹앱 전체 AM–SE 분포 (std · median · max) 내보내기 → 5번 배치에서 채움 · (B) mono 상별 칸 = 설계 상 칸에 단일 AM 값 (J20-f 개정 · 모든 상별 열 · `LHS-21` 해소) · 7a (웹앱 코드) · 7b (생성기 (B)) = 지금 · 7c (AM–SE CN 10 + 고립 3 + 분포 3 싣기) = coverage 닫힌 뒤 · `LHS-23` 등록 (고립 비율 census 오분류).  `529b495fc` = 요청서 §4 정정 (기준 2e57dff90) · 1저자 발송.
- ✅ **09-30 — 7a (J20-k (C)) 웹앱 전체 AM–SE 분포 내보내기 (시험 먼저)**: `calc_am_isolation_risk` 가 전체 `am_se_cn_median` (float) · `am_se_cn_max` (int) 를 더 내고 `analyze_contacts.py` 가 전체 `am_se_cn_std` · `_median` · `_max` 를 full_metrics 에 싣는다 (추가만 · 옛 키 · 값 그대로) · 새 시험 `analyze_contacts.py --selftest` 12 항 (3 상 · mono 작은 침대를 웹앱과 같은 CLI 로 · 손계산 대조 · 항등식 · mono 전체 = 그 한 상) — 옛 코드 6/12 → 12/12 · 등재 (fast · 1.5 s) · 인계표 무변경 (값은 5번 coverage 배치 뒤 · 7c).
- ✅ **09-30 오전 — Phase A 재현 런 (VGCF 100 GPa) STEP3 완주 · 런 뒤 절차 정정 (판정 전)**: kgy 점검 (1저자 09:22) = pa100 v015 32 · QC 8 · v020 32 · v025 32 (104) · pa010 v015 32 · 러너 종료 · 리포 HEAD `e49847e53` (변경 0).  사전등록 §6-4 명령의 결함 넷 → **§6 덧붙임 ②** (판정 결과 보기 전 · 판정선 불변): ① `.sh` 수집 `-newer 폴더` → 러너 영수증 ~ 마지막 팔 시간 창 (가짜 트리 시험 통과) ② 러너 `run_receipt.json` (code_sha · origins 포함 · `--check-arm` 정본) 을 덮지 않고 `.sh` 영수증은 `sh_receipt/` 에 · digest 대조 ③ 팔별 로그가 없어 로그 대조 생략 · 격자 로그 요약으로 대체 ④ 팔 경로 `…_arms/arms/`.  실행 스크립트 = `docs/reviews/phase_a_rep100_postrun_20260930.sh` (kgy 는 pull 하지 않고 fetch + show).  ⚠ 첫 판은 두 영수증 digest 가 같아야 한다고 가정해 v015 에서 멈췄다 (arms 정의 차이 — 러너 킷당 8 · `.sh` 32 · `SELF-68`) → 러너 선언 축만 대조 + 팔 = arms × 킷으로 정정 (과거 실물 시험 통과).  ⬜ 1저자 재실행 → tgz → `docs/data/phase_a_rep100_20260930/` 커밋 → §9 결과.
- ⛔ **09-30 밤 — Codex 재검증 (coverage 두 묶음 · HOLD 수정 0008–0011) = HOLD · P1 두 건 닫힘 · 새 P1 없음** (`docs/reviews/codex_lhs_coverage_reverify_verdict_20260930.md` · 증거 `codex_lhs_coverage_reverify_evidence_20260930/` · zip sha256 b9f815a5… 1,397,978 B): `LHSC-01` · `02` · `05` · `06` 닫힘 · `LHSC-03` R2 = `_coverage_v2_written` 이 n_am 누락을 0 으로 · 값은 None 만 봐서 생산자 출력 변이 10 종 accepted (n_am 삭제 · 면적 NaN 은 필수 단계 done) · `LHSC-04` R2 = 지원 범위 안 반올림 반례 (반지름 둘이 한 토큰으로 합쳐짐 · diff/B 1.3323976750260462) + "각 입력에 단조" · "포함 경계 불연속" · "구간 상한 없음" 서술 거짓 · 패치 0008 · 0011 GO · 0009 · 0010 HOLD · 반입 정정 = 요청서 "sha 7/7 동일" 거짓 (diff 본문만 동일 · `SELF-67`).  우리 재현: Codex 후보 9 파일 = 검토 worktree `002cc2881` (CRLF 제외 동일) · `audit_delta.py` 를 그 트리에 실행 → 스키마 변이 · 반올림 반례 · 비단조 · 깨끗한 import · 생산자 대조 **전부 동일**.  덤: `SELF-66` (mono type_map 관문) 이 문서 다섯 곳에서 인용되는데 원장에 없었다 → 소급 등재 (claimed_fixed `70e1203be`).  다음 = R2 두 건 수정안 비준 → 반례 먼저 → 재검증.
- ✅ **09-30 저녁 — 7b (J20-k (B)) 생성기: mono 는 설계 상 칸에 단일 AM 값 (1저자 *"4‴ 안보고 7b로 가도 되는거면 그러자"* · 시험 먼저)**: `lhs_design_dataset.py` — 설계 `block` 이 설계 상을 정하고 (`_mono_design_phase` · 수확 `n_types` 2 · `phase_counts` AM 하나 · coverage 상별 N_A · `AM_only` = 전체 와 맞아야 · 어긋나거나 모르면 거부 8 반례) · 수확기 열 (coverage 상별 ← 전체 · `n_AM_*_measured` ← `phase_counts.AM` = **`LHS-21` 해소** · `cov_*_n_valid` ← `counts.AM` · v3 벽 접촉 ← `AM`) · 웹앱 열 (반지름 이름 → 설계 이름 칸으로 옮김 · `_phase_swap` · 두 이름 다 값이면 거부 · 새 열 `wa_mono_phase_name_webapp` · J20-h 0 채움은 설계 상으로 · QC = 웹앱 `coverage_<웹앱 이름>_mean` − 수확 전체) · 열 사전 표지 (상별 열 전부 · 총량 · 설계 열 제외) · 시험 ⑯d–d10 · ⑳b · f · h 개정 + ⑳y–af (옛 코드 117/137 · 실패 20 = 전부 (B) 시험 → 137/137 · ⑳aa 가 QC 블록의 `wp` 변수 충돌을 잡음) · 인계표 재생성 (같은 명령 · 64 는 수확 0925 판) **130×139 · 64×141** — 바뀐 옛 칸 = mono 상별 칸만 240 · 128 (bimodal 0) · 이름 옮김 5 · 4 건 (§0 예측과 같은 9 건) · 설계 상 칸 ↔ 원천 46/46 차이 0 · QC |Δ| ≤ 1.4e-14 · 옛 (A) 판 = `912ceea3b`.
- ⛔ **09-30 — Codex 판정 도착 (3번 요청서 · coverage 두 묶음 · 병합 전) = 전체 HOLD · 새 P1 2 · P2 3** (`docs/reviews/codex_lhs_coverage_verdict_20260930.md` · 증거 `codex_lhs_coverage_evidence_20260930/` · zip sha256 c6cadd76… 862,690 B · 판정문 sha256 f14bd44a… 266 행 · 원장 `LHSC-01`~`10`): Codex 가 본 트리 = `da4670594` + 패치 7 (8 파일 · CRLF 정규화 뒤 우리 `64ae3cba8` 과 바이트 동일 · 제출 패치 sha 7/7 일치) · **우리 트리 재현 (Linux · `2e57dff90` + 패치 7 = `wt_cand`) = 네 감사 스크립트 전부 같은 결과** (경로 · 플랫폼 항목만 다름 — 수확기 selftest 는 여기서 139/139 · τ 중앙값 2.0805329527696066 = 핀 · Windows 의 CRLF · 1 ULP 문제 없음).  P1 = `LHSC-01` v2 피복률 분모 무효 (정사면체 AM 4 겹침 1.2 µm → 음수 분모 · 고립 NaN 반경) 가 **0.0 · ok** (`coverage_physics_vs_hertzian.py:298–342` · `n_free_surface_nonpositive` 를 세고도 사유에 안 넣음) · `LHSC-02` atoms-only 조기 반환 (`app.py:3280 · 3303`) 이 `stop_after='coverage'` 를 계산 없이 success/done (LHS 배치 입구 `stage_case` 는 막지만 공개 계약 충돌).  P2 = `LHSC-03` `_coverage_v2_written` 이 빈 문자열 · `not_run` 도 True · `LHSC-04` item 2 허용폭 = 축별 탐침 합이라 포함 경계에서 순수 반올림을 FLAG (diff/tol 1.18e6) · 깊은 겹침에서 Hertz · 3e-5 치환 누락 (무작위 15,000 건은 0/0 — 전역 보증 아님) · `LHSC-05` AST 가드가 `from scripts import plastic_coverage` · 별칭 `import_module` 을 못 본다.  P3 = `LHSC-06` `coverage_wall` 독스트링 "분자·분모 모두" 부정확 (분자 = 원 AM–SE 합 · ROI 밖 접촉 잔존 → 31.6 % OK 반례) · `LHSC-07` CLI 옛 경로 (`--all` 중첩 archive 조용한 skip rc 0 · 손상 JSON rc 0 — 이번 패치가 만든 것 아님) · `LHSC-08` 벽 규칙 = 저장 좌표의 양의 cap 깊이 (접선 근처 수 미보고) · `LHSC-09` 접촉 문의 단일 영상 전제 (같은 ID 쌍의 다른 영상 접촉 둘 가능 · LHS 실제 발생 주장 없음) + v2 = 미검증 후보 연산자 (개시점 면적 ×0.0566 불연속 · `V_lens/h_min` 상한 가정 미증명).  GO 4 = 0001 · 0002 (분모 보정 proxy 로만) · 0004 · 0005.  다음 (비준 대기) = 반례를 셀프테스트로 먼저 → 0006 → 0007 → 0003 수정 (검토 브랜치) → Codex 재검증 → 의존 순서대로 한 항목씩 병합 → 그 뒤에야 5번 재수확 · coverage 배치.
- ✅ **09-30 — 4′ Codex HOLD 3 건 수정 (저자 비준 "권고대로": 4′ 먼저 · LHSC-01 (a) 침대 빈칸 · LHSC-05 (a) 순수 기하 분리 · 셋 다 고친 뒤 재검증)** — 검토 브랜치 `review-coverage-20260930` 에 반례 먼저 4 커밋: `aba311054` LHSC-01 (v2 `coverage()` 가 반경 · 표면적 유한 양수 · 자유 표면 > 0 을 먼저 보고 아니면 사유 → 침대 빈칸 · `am_denominator_physics_v2` 에 `n_radius_invalid` (새) · `n_free_surface_nonpositive` 를 빈칸에도 · 픽스처 denom_zero · nan_radius · isolated_zero · ⑬ ⑭ 옛 코드 실패 → 15/15) · `471ad778b` LHSC-02/03 (`_atoms_only_refused`: raw · CSV 두 경로 × stop_after → failed · 호출 0 · 파일 없음 · None 그대로 · `_coverage_v2_written` = `COVERAGE_V2_OK_KEYS` 14 / `COVERAGE_V2_DIAG_KEYS` 4 스키마 · T11g–j · 가짜 producer 가 status 한 줄만 쓰던 fixture-drift 를 실제 키 집합으로 · 201/206 → 206/206) · `c125254a9` LHSC-04/05 (`_in_domain_rows` d − |r1 − r2| > 2h(r1) + 2h(r2) + h(δ) → `contact_area_check` 가 포함 경계 · 깊은 겹침 행을 `n_boundary_excluded` 로 따로 셈 · 규칙 문자열 · 새 모듈 `scripts/lens_geometry.py` (교차 원판 · plastic_coverage 는 별칭 · 수확기 의존 0 · 허용 이름 없음) · 가드가 패키지 경유 · importlib 별칭도 잡음 (lint 명시) · 수확기 ㉑′ 5 항 옛 코드 실패 · lens 5/5 · plastic 28/28 · coverage legacy 핀 그대로) · `002cc2881` LHSC-06 (벽 제외 = 분모 보정 proxy 문구).  Codex 스크립트를 고친 트리에 재실행: denominator_zero · nan → blank + 사유 · valid_isolated_zero ok 0.0 · atoms_only failed (파일 없음 · `audit_pipeline.py` 는 read_text 크래시 = 기대 동작 → guard 사본) · status_schema 4/4 False · ast_guard 두 우회 위반 · legacy 6/6 동일 · Codex 행 셋의 `contact_area_check` = 경계 2 · 초과 1.  재검증 요청서 `docs/reviews/codex_lhs_coverage_reverify_request_20260930.md` + 묶음 (패치 0001–0011 · SHA256SUMS · selftests.log · gate.log · fixed_tree_reproduction/) — 발송 = 사용자 · 원장 `LHSC-01`~`06` note 에 수정 커밋 (status 는 병합 뒤 claimed_fixed).
