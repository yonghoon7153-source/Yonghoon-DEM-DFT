# 원고 브랜치 전체 흡수 다이제스트 (2026-08-25, stoic-knuth 세션이 읽음)

> 지시: "저쪽 브랜치 다 읽어 — 꽤 많은걸 진행했었어".  정본은 원장(findings SELF-01~11 ·
> claims)과 각 리뷰 문서다.  이 파일은 **무엇이 실제로 돌았고 무엇이 닫혔는지**의 지도다.
> ⛔ CL-33/41/58 hold — 값 인용 금지 (quotation_ban).

## A. 실제로 돌아간 런 (= "꽤 많은 것")

1. **★ 게이트 ⑤ 8팔 완주 (2026-08-24)** — `docs/data/gate5_8arm_point_sg110447_20260824.md`
   vox 0.4 · 점 스탬프 · σ_VGCF 11.0447 · origin 8팔 · 8/8 수렴 · R = **1.615070**
   (비대응 SE 0.52 % 통과 · 쌍대응 0.097 % · 팔간 상관 +0.967).
   ★★ 이 런이 산 것 = **arm 0 단독이 8팔 평균보다 0.47 % 낮았다** ⇒ 단일팔 계통 편향의
   직접 증거 ⇒ **옛 arm-0 factorial 분해(스탬프/σ/교호)는 부호·순서만 유효, 크기 인용 금지.**
   ⚠ vox 0.4 세대라 R 자체는 헤드라인 아님 (진단 자산).
   ⇒ CLAUDE.md "다음 ② 게이트 ⑤ 8팔" 은 **이 형태로 닫혔다** (강도 프로브 격자에서).
2. **kgy 돌연변이 배터리 56/56** + check_all — 컨테이너·실기계 양쪽 초록 (규율 층 전달 조건).
3. **CPU 판별 노브 사전측정** (bridge prereg §3) — 120회 몬테카를로, 채널 A/B 분리 확인.
4. ⚠ **판별 런(A) · D13(B) 은 한 번도 안 돌았다** — 세션 종료 메모가 명시.

## B. 원장 신규 (SELF-01~11 요지)

- **SELF-02/03/04**: 회계 전수화 과정에서 실구멍 — `--dilate-z 1.0719` 가 **생산 킷 둘 다
  켜져 있었고 기록 안 됨** (같은 값이라 과거 SBE↔DBE 대조는 오염 아님, 보증만 부재) ·
  `se_source` 신설 (합성 SE 침대 `SE_PROXY` HOLD — 실측 확인 결과 생산 킷은 실침대) ·
  규약 축 7개 레지스트리 밖 → 등재.
- **SELF-08**: 철회값 스윕이 **원고 생성기(`docs/manuscript_draft/build.js`)를 안 읽었다**
  → .docx 만 고친 수정은 안 내구적.  ⇒ **원고 수정은 생성기로** (W5/W7 에 직결!).
- **SELF-09**: R5 영수증 대조에 **회귀가 아예 없었다** (게이트 지워도 초록).
- **SELF-10**: CL-39 수렴 판정에 판별력 없음 (배치평균은 무편향; 입자별 CV 가 움직임).
- **SELF-11**: Q-B2 후보 = SDCP 접촉 양자화 (A 트랙의 과학적 근거).
- 반복 교훈 ×3: **"검사기를 추가한 것과 그 검사기가 무는 것은 다르다"** — 변이판 FAIL 확인 필수.

## C. PTFE 8팔 크로스리뷰 (2026-08-24) 핵심

- **CDXR2-1 (P1)**: `phase_current_share` 가 자기 docstring 항등식 위반 — 플레이트 커플링
  (σ 비례) 누락.  주기 seam 누락(22.9 %)과 **같은 실패 양식 2회차**.
  ⇒ CL-41 의 "SDCP 1 %" 는 미상 크기만큼 과소.  **불변식 필요**: L 에 들어가는 모든 σ 비례
  항이 분담 합에도 — 유한차분 대조 회귀로 강제.
- **CDXR2-2 (P1)**: `--fibre-dia` 가 raster 에 미배선 (뷰어 전용).  capsule 은 예약값 +
  `unsupported_protocol` abort 로.
- **R2-2**: 1.07–1.11 봉투 철회.  인용 가능: *"σ_SDCP 낮추면 R 비증가 (Rayleigh 단조성),
  크기 미확정."*  닫는 런 스펙 존재: **DBE 만 σ_SDCP {250, 144.338, 83.333} + ±1 % 유한차분**
  (SBE 는 SDCP 없어 불요) — ★ B 트랙이 σ_e(SDCP) 를 재보정하면 이 스펙이 그 후속이다.
- 부피가중 `F_V(h)` 정의 확정 (개수 아님) · partial-volume 을 "작은 σ" 로 구현 금지
  (face-fraction/cut-cell) · 1e-16 14솔브 DROP 유지.

## D. 구조적 사실 (작업 방식에 걸리는 것)

- **p1 → p2 규약 세대 단절** — 옛 팔 전부 `unknown:` → fail-closed HOLD.  의도된 동작.
  판별 런 4개(A)가 vox 0.15/0.125 의 **p2 재실행을 겸한다**.
- **원고는 생성기 산물** — `docs/manuscript_draft/build.js`.  Methods/표 수정은 여기로.
- next_steps 의 옛 순서(census → GPU 재실행)는 handoff 의 A/B 두 트랙으로 **대체**됐다
  (census 아이디어는 기록으로 남음 — 지금 있는 census 는 합성 침대라 인용 불가).
- E 절 확정: 지금 원고에 쓸 수 있는 것 = 기전 서술(하향판) · 방법 · 격자 미수렴을 결과로.
  못 쓰는 것 = σ_e 절대값 · SBE/DBE 비 · p1 값 전부.

## E. 이 세션이 이 브랜치에 더한 것 (2026-08-25)

- `sdcp_ion_calib_prereg_20260825.md` (B 실행 계약, G1 은 v6 본문으로 닫음)
- `week_plan_manuscript_20260825.md` (v6 실물 대조 — **Table S3 이 철회 세대 값**임을 확정,
  S2↔S3 세대 불일치 증거, W1~W7)
- 러너 `SDCP_BRIDGE` 정식 축 (P2_EXTRA 가드가 옳았고, 축·영수증·태그·조립 배선)
- 검사기 프로브 **환경 밀폐** (`_hermetic_env`) — kgy 오탐 L_LEANDEFAULT 의 원인 제거
  (env 만드는 함수가 둘이라 한쪽만 고치면 안 됐다), SBRG_FLAG seed, 변이 리터럴 2건 갱신
- bridge prereg §7 실행 표기 수정 (판정선 불변, 런 전, 결과 0건 상태)
- **★ G2 구현 완료** (커밋 2 = 이 파일과 같은 커밋): PTFE 이온 차단 노브
  `apply_ptfe_blocking` (SE sid 6 → **신설 sid 9 `SE_blk`**, 이온·전자 양쪽 σ=0, 열은 k_SE) ·
  세 σ/k 표를 10 칸으로 확장 · `electronic_sigma_table(sigma_se=…)` = 원장 ④ 전용 훅
  (기본 0 = 생산 불변) · 전극 CLI `--step3-ptfe-block-um` + 규약 축 `ptfe_block_um`
  (PROTOCOL_FIELDS · STRICT_TYPES · FIELD_CONTRACT required_since 2026-08-25 · 매니페스트) ·
  selftest 8종 (`ptfe-block-*`) · **돌연변이 5종** (기대집합을 스크래치에서 선검증 — 5/5 정확).
  ⚠ 배터리 도중 대상 파일을 편집해 그 런을 **오염으로 폐기**하고 재실행한 것도 기록해 둔다
  (심볼릭 트리라 mid-run 편집이 결과를 섞는다 — 다음 세션 주의).
- **펠릿 RVE 측정기 `pellet_rve_sigma.py`** (selftest 11/11) + 러너 `run_pellet_calib.sh`
  (STAGE 1: neat/+SDCP/+PTFE 차단그리드/ρ·d 감도, 시드 4, 팔당 ~4 s CPU) — prereg §8 이행.
  wt→vol 산술이 prereg §1 (9.17/14.60 vol%) 과 selftest 로 맞물림.  T2 스패닝 검출은
  x/y wrap 을 union-find 로 합침 (안 합치면 비퍼콜 주장이 거저 통과한다).
  `apply_ptfe_blocking(periodic_xy=True)` — 전극과 **같은 함수** (R5-CX-09 단일 소스 규약).

## F. 오늘 독해로 추가 확정된 것 (2차분)

- **build.js 전문**: 생성기에는 이미 **S3 전 칸 공백 + ⛔ 배너 + Ref S6~S8** 이 들어 있다 —
  v6 docx 의 철회값은 **옛 생성기 산출**이라는 뜻.  W4 뒤 `node build.js` 재생성이 정답이고
  docx 손편집은 금지 (SELF-08).  D-메모 특기: D9 (식 (2) Joule 를 남기려면 Results 소비처
  필요) · D14 (**AM 클래스 확인 — 침대는 AM_S 10 mS/cm 인데 원고는 polycrystalline 서술 =
  AM_P 5 와 2배 차, 사용자 확인 필요**; VGCF E=10 GPa placeholder → D3 재압밀에 감도 팔 권장) ·
  D16 (DFT 브랜치와 수식 번호 (3)·Ref S1~S5·서지 스타일 맞물림).
- **codex_absorb_verdict (R1~R4 전문)**: 4차까지 전부 NO-GO→대응 완료의 사이클.  GPU 재실행
  조건 = 새 p2 스키마 · clean SHA · 영수증 · census · p1/p2 불혼합 (지금 러너가 충족).
  **Q1: 비(ratio)의 공통모드 상쇄는 보장되지 않는다** (κ_DBE=κ_SBE 근거 없음) — A 트랙
  판별 런이 정확히 이것을 잰다.
- **R5 판정 + R6 요청**: R5 = HOLD (R5-CX-01~11, 전부 대응 커밋 확인).  R6 요청은 스코프를
  **"원고 주장에 코드가 충분한가"** 로 좁혔고 **Codex 회신 대기 상태**다.  R6 요청서가
  자기신고한 것: `_tid` 3연속 결함 → **기대집합 실재 관문(HARNESS_ERROR)** 신설 · `.py` 생성기
  정책 구멍(오늘은 셋 다 깨끗해서 무사했을 뿐).
- **claude_selfreview_ptfe_8arm (독립 자기리뷰)**: ★ B 트랙에 직결 —
  **F-A**: σ_ion(SDCP) 는 MG 역산으로 점 0.066 · **±5 % 오차면 밴드 [0, 0.6]** (절연 극한에서
  둔감) ⇒ 펠릿 RVE 보정(③)도 **밴드로 보고**해야 한다.  **N-5**: 전극 재실행(B-5)에서 PTFE
  스탬프 + σ_i(SDCP) 앵커를 동시에 켜면 이온 비에 반대 방향 두 힘 = **부호 검정으로 등록
  가능한 진짜 미지** (B-5 사전등록에 넣을 것).  **N-1**: 차세대 규약 = PTFE **σ=0 스탬프**
  (`ptfe_zero_dof` 필드가 그 이행 흔적).  **N-2**: PTFE 는 직경 분포(정부피 인발)라 튜브
  스탬프는 성립 안 함 — 절연체의 불변량은 부피가 아니라 **절단 위상**.  **N-4**: σ_SDCP
  필름/펠릿 불확실성의 비 영향 ~1 % 유계.  **Part 4**: **첨가제 web 실현 n=1** — origin 8팔이
  못 덮는 축, SBE/DBE 비에서 상쇄 안 됨 (SI 문장은 "grid-origin ensemble SE" 한정 유지).
- **sdcp_master.md**: ADD_E_SET 정본 = PTFE 1.80 · SDCP 9.00 GPa (⚠ "출처 = 사용자 지정,
  근거 미기재" — Table S2 는 "This work Fig 2g/S6-7" 로 적는다: v6 실물이 measured 로 확인).
  σ_e(SDCP 소재) 150 은 2026-07-10 INTERIM — 현행 250 assumed 와 **계보가 다르다** (250
  출처 질의는 여전히 사용자 회신 대기).  S12: SDCP 단독 dough 불가 → dual-binder 가 물리.
  E_bind DFT 는 오분자로 무효화 → 재계산 스펙만 확정 (방향 doped≫neutral 만 생존).
