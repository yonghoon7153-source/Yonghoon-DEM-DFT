# Rint ② kgy 명령 — 다음 세대 침대 재압밀 (VGCF E 100 GPa) · S0 표현 원장 · 런 사슬 꼴 (2026-10-20 · 결과 0 건)

> **지위** — 1저자가 kgy 에서 그대로 붙이는 명령 문서 · 런 결과 0 건 · σ 런 없음.  주소 · 포트는 적지 않는다.
> **근거** — 1저자 10-20: 설계 §10 N1–N18 *"다 권고대로 해"* · 다음 세대 침대 = **SBE · DBE 둘 다 VGCF E 100 GPa 로 다시 압밀** ·
> VGCF voxel σ = 두 전극 같은 값 하나 (직경 보존 · Endo 단섬유 → 7,854 S/cm · Q5) · 보정 손잡이 = R_j,0 하나 (SBE 1.63) · DBE 4.68 에 맞추지 않음.
> 압밀 명령 = 등록 v2 `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` §7 R0 · R1 (10-19) + SBE 원 침대 `docs/reviews/table_s3_data_20260827.md` §1.
> S0 = 설계 v1 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §2 · 등록 R 초안 `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §2-1 · §10 · §11 ·
> 도구 `scripts/ca_s0_census.py` · 시험 `scripts/test_ca_s0_census.py` (108 PASS · 변이 14/14 잡힘) → ✅ **10-20 밤 2 일 차 판 `aef62d81a`** (SCHEMA `ca-s0-census-v2`):
> 판정 · 보고 접합 census = `carbon_junction.cjunc_registry` **같은 함수** (`junction_census` · s_min 없음 = 같은 가닥 후보 전부 + 경로 호 길이 s 후보별 목록 · 긴 접촉 수 · L_c 분포 · 길이 법칙 배율 합 ·
> `s0_junctions_<킷>.npz`) · α 분포 = S1 `ptfe_face_alpha` 함수 (`alpha_census`) · 옛 B0 미리보기 = `census_preview` 블록 (status `b0_preview` · 판정 · 보고에 안 씀) 으로 남김 · 시험 121 PASS · σ 칸 없음 (솔브 0) 그대로.
> **이름 (10-20 확정)** — 새 킷 = `~/sdcp/kit_SBE_vgcf100` · `~/sdcp/kit_DBE_sdcp1um_vgcf100` · 현 세대 `~/sdcp/kit_SBE` · `~/sdcp/kit_DBE_sdcp1um` 은 **그대로** (건드리지 않는다).
> **코드** — 재압밀 = `~/dem-anchor1019b` (`298a73197` · R1 · 최종 16 팔과 같은 코드) · S0 = 새 작업 트리 `~/dem-ca1` (S0 도구가 든 가지 커밋 · 메인이 옮긴 뒤) · 파이썬 = `~/dem-venv`.
> **표지** — [리포] 리포 기록 · [우리 산술] 그 값으로 한 계산 · [합성] 합성 시험 (실침대 아님 · 인용 불가) · (어림) · ⬜ = 할 일.
> **★ 개정 (10-21 · Codex 판정문 `docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md` · 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` · 1저자 10-21 Q1–Q12 권고대로 + Q13 (가) — Q13 = 진행 기록 10-21 02 의 막는 것 E6 결정 (가) · 수정 계획 문서에는 Q12 까지 (1저자 결정의 리포 기록 = 메인 몫))** — 판정문 §0: S0 단계 1 (새 SBE 기하 · 읽기 전용) = **조건부 GO** (원본 경로 · 표본화 · 침대 지문 보존 · `s_min` 은 자동 파생값이 아님을 명시) · S0 단계 2 (DBE 기하) = **조건부 GO** — 문턱 전부와 s_min 선택 절차를 DBE 열람 전에 개정 · 봉인 (등록 R §2-1 · §2-1b) + 재방문 셀 · 긴 접촉 · 덮임 census 를 보탠 뒤 · 재압밀 자체는 판정문 표에 따로 없다 (σ 를 보지 않는 침대 준비 · 수정 계획 §3 = 바로 가능) · σ 를 여는 런 (숫자 탐침 제외) = Codex 재검토 GO · 등록 비준 뒤.  바뀐 자리 = §1-0 · §1-1 (Q13 (가) — 새 킷 payload 줄에서 `--joule-heat` · `--save-step4-grid` 를 빼는 sed + 확인 grep) · §1-4b (판정문 §5-2 의 재압밀 추가 기록 칸 · 실행 코드 지문) · §1-5 · §2 (새 census 칸 · s_min 개발 단계 · 계획 해시 둘) · §3 (사슬 실제 명령) · §4 ⑥ · §5.  철회 문장은 `~~ ~~` · 결과 0 건.
> **★ 개정 2 (10-21 · 사전 리뷰 (설계 · 등록 쪽 PRE-design · 구현 쪽 PRE-impl · 리포 밖 · 메인 세션 기록) · 1저자 10-21 *"권고대로 해"* Q-A–Q-G · 등록 R 4판 · 설계 4판과 짝)** — 바뀐 자리 = §0 (실행 순서 = 주 판정 먼저 · 감도 그 뒤 · Q-F) · §2-2 (단계 2 전 세 숫자 · Q-G) · §2-3 (단계 2 작업 트리 = §2-1 개정 커밋 자체 · census · registry 같은 판 확인 · R 런 계획 · s_min 손 확인 — PRE-design-04 · 14) · §3 (주 판정 먼저 · Q-F · 끝 origin · Q-E) · §5.  철회 문장은 `~~ ~~` · **새 숫자 없음** · 결과 0 건.
> **★ 개정 3 (10-22 · 사전 리뷰 2 회차 PF2 · 1저자 10-22 Q1 (다) · Q2 · Q3 권고대로 · 등록 R §2-1 · §10-1 · §11 과 짝)** — 바뀐 자리 = §0 (②b ⑥ 숫자 탐침 = 단계 2 앞) · §2-2 (개정 커밋 하나 전에 ⑥) · §2-2b (⑥ 명령 · 옛 §3 (2) 에서 옮김) · §3 (사다리 `--s0-stage2-report` · (2) 철회 표지) · §5 (PRE2-design-01 · Q2) · §0 ④ · §3 시간 (PRE2-design-03 · Q3 — 등록 R §10-4 다시 어림 값 · 새 계산 아님) · (PF2 D · PRE2-design-02 · 08) §3 사다리 `--s0-stage1-report` · 깨끗한 트리 · `--machine` 주석 · §2-3 손 확인 주석 (S0 보고 지문 일곱) · §5.  철회 문장은 `~~ ~~` · 새 숫자 없음 · 결과 0 건.
> **★ 개정 3 이어 (10-22 · PF2 F · 사전 리뷰 2 회차 PRE2-design-04 · 05 · 07 · 결정 없음 · 결과 0 건)** — 바뀐 자리 = §2-2 (단계 2 관문이 결과 전 등록 숫자 넷 · `tol_ff` 를 본다 = 지금 동작 · SV 끊는 범위 = Q-D 로 닫힘 · 모서리 묶는 법 = 등록 R §10-2 ㉟) · §2-3 (단계 2 명령 `--r-plan-path` · 관문이 보는 것 · 남은 손 확인 = `same-version` · `s_min` 값) · §3 (사다리 `--s0-plan` · 감도 단계 `--after-main` = 등록 R §10-1 블록과 같은 인자 · 지킴 = `scripts/test_rint_r_chain.py` K01 · 3판 · 4판 규칙은 사슬에 들어갔다 · `<V>_UNCHECKED` 자리 = `assemble` · 시험 V02).  철회 문장은 `~~ ~~` · 새 숫자 없음.
> **★ 개정 4 (10-28 · 1저자 *"Rint 권고대로"* · 등록 R §10-5 가 ① · 묶음 C 코드 보고 `docs/reviews/rint2_rr_fix_evidence_20261023/REPORT_C.md` §11 ① · 결과 0 건)** — `--machine <기계 이름표>` = **필수** (사다리 · 예측 · 원장 `--add` · 없으면 rc 2 · 계획 허용 목록 밖 = `MACHINE_NOT_ALLOWED`) — 바뀐 자리 = §3 머리 CLI 줄 둘 · §3 블록 주석 · 사다리 · 예측 명령 줄 · §5 기록 줄 · 옛 `[--machine]` (선택 · 기록만) 철회.  판정 `--ledger` · 원장 시도 꼴 명령 줄 = 이 개정 밖 (등록 R §10-5 가 ⑨).
> **★ 개정 5 (10-28 밤 · 사전 공격 5 회차 봉인 전 남은 #4 · 1저자 10-28 밤 *"rint는 권고대로"* · 수정 계획 `docs/reviews/rint2_pc5_fix_plan_20261028.md` · 등록 R §10-1 · §10-5 아 와 짝 · 결과 0 건)** — 바뀐 자리 = §3 실제 명령 블록: (2b) 시도 원장 (`--stage ledger --init` 한 번 · 시도마다 `--add`) · 사다리 · 예측 = 원장 시도 꼴 (`--ledger` · `--attempt` · 시도 폴더 `<--out>/attempt_<n>/`) · `--dry-run` = 그 둘 없이 · 예측 `--ladders` · 판정 `--runs` · 감도 `--after-main` = 원장 채택 시도 폴더 · 판정 `--ledger` · 멈춘 사슬 뒤 `--stage recover` (다른 부팅 = 운영자 확인 표지 `--operator-confirm` · `--operator-why`) · 두 문서 인자 집합 = 시험 `scripts/test_rint_r_chain.py` K01.

## 0. 순서 한눈에

| # | 무엇 | 기계 | 시간 (어림) | 끝나면 |
|---|---|---|---|---|
| ① | 재압밀 SBE → DBE (차례로 · 한 GPU) · (10-21) 새 킷 = payload 두 토큰 뺀 판 (§1-1 · Q13 (가)) | kgy GPU | 침대당 ≈ 1.5–2 h · 둘 ≈ 3–4 h (§1-3) | §1-4 · §1-4b (10-21) 검사 출력 보내기 |
| ②′ | (선택 · 지금 가능 · ①과 무관) S0 **도구 시험** — 현 세대 `kit_SBE` (옛 VGCF 10 GPa 침대) | kgy CPU | ≈ 15–30 분 (§2-1b) | 화면 요약 보내기 — **s_min · 문턱 결정에 쓰지 않는다** |
| ② | S0 단계 1 — SBE 새 침대 | kgy CPU | 침대당 ≈ 15–30 분 (§2-2) | 보고 · 계획 보내기 → ~~등록 R §2-1 개정 커밋~~ (10-22 · Q2) ②b 뒤 개정 커밋 하나 |
| ②b | (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 1저자 Q2) ⑥ 숫자 탐침 — SBE · σ 봉인 · **단계 2 앞** (§2-2b · 옛 자리 = §3 (2)) → Codex 요청 (기하 + 반복 수) → 회신 → 세 숫자 → 등록 R §2-1 개정 커밋 **하나** (숫자 + S0 계획 해시 + R 런 계획 해시 (maxiter 포함) + s_min) | kgy GPU | ⬜ (탐침이 잰다) | 반복 수 · 잔차 · 시간 보내기 (σ 없이) |
| ③ | S0 단계 2 — DBE 새 침대 (+ 옛 `kit_DBE`) · (10-21 · Q-G) **그 전에** 세 숫자 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱) = 1저자 · Codex 회신 뒤 · 등록 R 개정 커밋 (§2-2 끝) | kgy CPU | 침대당 ≈ 15–30 분 | 보고 보내기 (10-22 · Q2 — 이 보고의 봉인 계획 해시를 R 런 사슬이 대조) |
| ④ | 런 사슬 | — | — | ⛔ **발사 금지** (§3 · 등록 R §11 관문 뒤) · (10-21 · Q-F) 순서 = **주 판정 먼저** (SBE 보정 + 끝 origin + DBE 네 모서리 × 세 R + origin · 78 팔 ~~≈ 56 h · 부담 ×1.7–2 = 95–112 h [우리 산술 · 등록 R §10-4]~~ → (10-22 · PRE2-design-03 · Q3) ≈ 191–231 h [추정 · 합성 침대 반복 비 · 등록 R §10-4 다시 어림] · ⑥ 실측 직후 = 결정점 · 10-31 에 안 끝나면 판정 없이 진행 보고만 · 팔은 줄이지 않는다) → 10-31 판정 = 주 판정만 (한정어 *"감도 미완료"*) → 감도 (264 팔 ≈ 231 h · ×1.7–2 = 392–462 h · 옛 어림) · GPU 추가 = 1저자 (Q3-b 미답) |

## 1. ① 재압밀 — VGCF E 10 → 100 GPa 한 가지만

### 1-0. 무엇이 같고 무엇이 바뀌나

- **같은 것** — `kit_SBE` 와 옛 `kit_DBE` 의 압밀 명령 = 같은 명령 (조성만 3:1 ↔ 3:0.5:0.5) [리포 · 등록 v2 §7 R0] · `kit_DBE_sdcp1um` = 그 명령 + 아래 두 플래그 [R1]: `--mixing thinky` · `--seed 3` · `--n-grid 263` · `--frames 150` ·
  `--protocol hold` · `--lateral-box 0.05` · `--dilate-z 1.0719` · `--coh-ptfe 0.10` · `--binder-opt-wt 1.5` · `--fibre-buckle --fibre-align 0.606` · V/c_P 0.2717.
  - SBE `kit_SBE` — 08-27 런 `run_VGCF3_PTFE1_20260827_134104_3672586` · 세대 `ADD_E_SET_20260818_9.0GPa` · VGCF 10 GPa = **그때 코드 기본값** (압밀 줄에 VGCF override 없음 — §1-1 의 grep 으로 확인) [리포 · Table S3 §1].
  - DBE `kit_DBE_sdcp1um` — 10-19 R1 다섯째 시도 = 옛 `kit_DBE` 명령 + `--sdcp-agg-d 1.0 --add-e-override VGCF=10` · `--gpu-mem 28 → 20` [리포 · 등록 v2 §7].
- **바꾸는 것 하나** — VGCF E 10 → **100 GPa** = 지금 코드의 기본 세대 `ADD_E_SET_20260926` (VGCF 100 · PTFE 1.80 · SDCP 9.00 · SuperP 0.50 — 08-18 세대와
  VGCF 하나만 다르다 · 등록 v2 §7 시도 1 줄 · 원장 `CL-93`).
  - DBE: 압밀 줄에서 ` --add-e-override VGCF=10` 을 **뺀다** — `VGCF=100` 으로 적지 않는 이유: override 가 있으면 침대 표지 `E_anchor` 가
    `ADD_E_SET_20260926+override:VGCF=100.0GPa` 가 되어 기본 세대 표지 `ADD_E_SET_20260926_VGCF100GPa` 와 문자열이 갈린다 (`scripts/mpm3d_compaction.py` 195–206 행) —
    두 새 침대가 **같은 표지**를 갖게 한다.
  - SBE: 압밀 줄의 물리는 그대로 (override 가 처음부터 없다) · `--gpu-mem 28 → 20` 만 (R1 과 같은 자원 조정 · 물리 무관 · 모자라면 자동으로 낮춘다).
  - 시드 · 나머지 전부 그대로.  ~~**payload 줄은 건드리지 않는다** (러너가 팔마다 그 줄을 다시 뽑는다 — `sr01_stamp_compare.extract_payload_cmd`).~~
  - **(10-21 · 1저자 Q13 (가) · 진행 기록 10-21 02 E6) payload 줄에서 `--joule-heat` · `--save-step4-grid step4_grid.npz` 두 토큰만 뺀다** — 러너가 팔마다 그 줄을 다시 뽑아 (`sr01_stamp_compare.extract_payload_cmd`) 다음 세대 플래그를 붙이는데, 다음 세대 payload 는 두 플래그를 거부한다 (기반 `47d23baba` 의 `scripts/mpm_webapp_payload.py` 901–904 행 (탄소 접합) · 1729–1732 행 (face_alpha) · 사유 `JOULE` · `STEP4_GRID`) → 그대로면 사슬 첫 런 (바닥) 이 RUNNER_RC 로 멈춘다 (시험 `scripts/test_rint_r_chain_e2e.py` E6).  나머지 payload 토큰 그대로 · 현 세대 두 킷 (`kit_SBE` · `kit_DBE_sdcp1um`) 은 그대로 · 두 토큰은 압밀 · 침대 기하에 안 들어간다 (payload = 압밀 뒤 후처리 — Joule 지도 · STEP4 격자 저장) → 새 킷의 압밀 뒤 기본 payload 에는 Joule 지도 · `step4_grid.npz` 가 없다 (다음 세대 런은 둘을 쓰지 않는다 · S0 도구는 `--save-step4-grid` 가 있으면 자기 출력 폴더로 돌릴 뿐이다 — 기반 `47d23baba` 의 `scripts/ca_s0_census.py` 960–962 행).

### 1-1. 새 킷 폴더 — 입력만 복사 · scripts 링크 · run_mpm.sh 한 줄

```bash
. ~/dem-venv/bin/activate && which python3           # dem-venv 의 python3 이어야 (R1 시도 3 = 다른 venv → GLIBC 오류)
cd ~/sdcp && ls -d kit_SBE kit_DBE_sdcp1um && test ! -e kit_SBE_vgcf100 && test ! -e kit_DBE_sdcp1um_vgcf100 && echo OK-새이름-비어있음
git -C ~/dem-anchor1019b log --oneline -1           # 298a73197 이어야 (R1 · 최종 16 팔과 같은 코드)
git -C ~/dem-anchor1019b status --porcelain --untracked-files=no | head    # 아무것도 안 나와야 (dirty 아님)

# 현 세대 두 킷의 압밀 줄 — override · 프레임 · 플래튼 규칙 · 시드 (읽기만)
grep -n -- '--add-e-override\|--sdcp-agg-d\|--gpu-mem\|--frames\|--platen-mach\|--allow-fast-platen\|--seed' kit_SBE/run_mpm.sh kit_DBE_sdcp1um/run_mpm.sh
# (10-21 · Q13 (가)) payload 줄의 두 토큰 · STEP4 사슬 줄 (읽기만) — 킷마다 --joule-heat 한 번 · --save-step4-grid 한 번 · step4_dyn 0 이어야 아래 sed 가 맞는다
grep -n -- '--joule-heat\|--save-step4-grid\|step4_dyn' kit_SBE/run_mpm.sh kit_DBE_sdcp1um/run_mpm.sh

# 입력만 복사 — 런 폴더 · latest_run · scripts 링크 제외 (⚠ 'run_*/' 끝 슬래시 = 디렉터리만 · 파일 run_mpm.sh 는 남는다 · SELF-123)
rsync -a --exclude 'run_*/' --exclude latest_run --exclude scripts kit_SBE/ kit_SBE_vgcf100/
rsync -a --exclude 'run_*/' --exclude latest_run --exclude scripts kit_DBE_sdcp1um/ kit_DBE_sdcp1um_vgcf100/
ln -s ~/dem-anchor1019b/scripts kit_SBE_vgcf100/scripts
ln -s ~/dem-anchor1019b/scripts kit_DBE_sdcp1um_vgcf100/scripts
ls -la kit_SBE_vgcf100 kit_DBE_sdcp1um_vgcf100       # run_mpm.sh · am_scaffold.csv · se_scaffold.csv … 있고 run_* 디렉터리 · latest_run 없음

# 한 줄씩 바꾼다
sed -i 's/ --add-e-override VGCF=10\b//' kit_DBE_sdcp1um_vgcf100/run_mpm.sh
sed -i 's/--gpu-mem 28\b/--gpu-mem 20/' kit_SBE_vgcf100/run_mpm.sh
# (10-21 · 1저자 Q13 (가)) payload 줄에서 두 토큰만 뺀다 — 다음 세대 payload 가 거부 (JOULE · STEP4_GRID · 진행 기록 10-21 02 E6)
sed -i -e 's/ --joule-heat\b//' -e 's/ --save-step4-grid step4_grid\.npz\b//' kit_SBE_vgcf100/run_mpm.sh kit_DBE_sdcp1um_vgcf100/run_mpm.sh

# 확인 — (10-21) 각각 두 줄만 달라야 한다 (DBE = 압밀 줄의 override 토큰 + payload 줄의 두 토큰 · SBE = 압밀 줄의 gpu-mem + payload 줄의 두 토큰 · 2판 "한 줄만" 은 철회)
diff kit_DBE_sdcp1um/run_mpm.sh kit_DBE_sdcp1um_vgcf100/run_mpm.sh
diff kit_SBE/run_mpm.sh kit_SBE_vgcf100/run_mpm.sh
diff kit_DBE_sdcp1um/run_mpm.sh kit_DBE_sdcp1um_vgcf100/run_mpm.sh | grep -c '^[<>]'          # 4 (바뀐 두 줄의 옛 · 새)
diff kit_SBE/run_mpm.sh kit_SBE_vgcf100/run_mpm.sh | grep -c '^[<>]'                          # 4
grep -c -- '--add-e-override' kit_SBE_vgcf100/run_mpm.sh kit_DBE_sdcp1um_vgcf100/run_mpm.sh    # 둘 다 0
grep -c -- '--sdcp-agg-d 1.0' kit_DBE_sdcp1um_vgcf100/run_mpm.sh                             # 1 (SDCP 1 µm 그대로)
grep -c -- '--joule-heat' kit_SBE_vgcf100/run_mpm.sh kit_DBE_sdcp1um_vgcf100/run_mpm.sh        # 둘 다 0
grep -c -- '--save-step4-grid' kit_SBE_vgcf100/run_mpm.sh kit_DBE_sdcp1um_vgcf100/run_mpm.sh   # 둘 다 0
grep -c -- 'step4_grid\|step4_dyn' kit_SBE_vgcf100/run_mpm.sh kit_DBE_sdcp1um_vgcf100/run_mpm.sh   # 둘 다 0 (0 이 아니면 그 격자를 읽는 STEP4 줄이 남았다)
grep -c -- 'mpm_webapp_payload' kit_SBE_vgcf100/run_mpm.sh kit_DBE_sdcp1um_vgcf100/run_mpm.sh  # 옛 킷과 같은 수 (payload 줄은 남는다)
```

- ~~`diff` 가 두 줄 이상이거나 grep 수가 다르면~~ → (10-21) 바뀐 줄이 둘 (`grep -c '^[<>]'` = 4) 이 아니거나 grep 수가 위 주석과 다르면 **발사하지 말고** 그 출력을 보내 주세요 (override 가 다른 꼴 — `=` · 따옴표 — 로 적혀 있으면 sed 가 안 맞는다 · payload 두 토큰이 서로 다른 줄에 있으면 `^[<>]` 가 6 이 된다 · STEP4 사슬 줄이 있으면 그 줄은 사람이 본 뒤 정한다).

### 1-2. 발사 — 차례로 (한 GPU · run_mpm.sh 의 *one GPU = one run* 가드)

```bash
nvidia-smi --query-gpu=memory.used,memory.total --format=csv    # 다른 작업 몫 (R1 때 12.4 GB — --gpu-mem 은 자동으로 낮춘다)
pgrep -af mpm3d_compaction.py || echo 'MPM 없음'                 # 돌고 있으면 run_mpm.sh 가 ABORT 한다

# SBE 먼저 — run_mpm.sh 가 스스로 분리 (setsid) 하고 런 폴더 · PID 를 찍는다
cd ~/sdcp/kit_SBE_vgcf100 && MPM_NO_PULL=1 bash run_mpm.sh
tail -f ~/sdcp/kit_SBE_vgcf100/run_*/mpm_run.log                  # 'FINAL' · '[run_mpm] DONE' 까지 (Ctrl-C 는 tail 만 끈다)

# SBE 가 끝난 뒤 DBE (완료 마커로 확인)
test -f ~/sdcp/kit_SBE_vgcf100/latest_run/mpm_done.marker && cd ~/sdcp/kit_DBE_sdcp1um_vgcf100 && MPM_NO_PULL=1 bash run_mpm.sh
tail -f ~/sdcp/kit_DBE_sdcp1um_vgcf100/run_*/mpm_run.log
```

- 실패하면 (OOM · 다른 venv · 가드) 그 로그 끝을 보내 주세요 — R1 은 다섯째 시도에서 섰다 (OOM 셋 · venv 하나 · 등록 v2 §7).  같은 킷을 다시 발사하면 새 런 폴더가 생기고 `latest_run` 은 마지막 완주 런을 가리킨다.

### 1-3. 시간 (어림)

- 프레임당 substep 40 (`--sub` 기본) · 프레임 150 — VGCF 100 GPa 는 dt 만 줄이고 (§1-5) 프레임당 계산량은 같다 ⇒ 압밀 시간 ≈ 현 세대와 같다 (어림).
- kgy 근거 [리포 · progress 10-19 16]: R1 다섯째 시도 19:12:17 시작 → 19:31 frame 40 (이미 목표 도달 · 판 고정 뒤 · 다른 작업 12.4 GB 와 GPU 공유) ⇒ 150 프레임 ≈ 1–1.2 h ·
  그 뒤 킷 기본 payload (STEP3 풀이 포함 · 수십 분).  08-27 두 침대의 런 폴더 시각 13:41:04 → 15:00:29 [리포 · Table S3 §1] 도 압밀 ≤ 1 h 19 m 와 맞다.
- ⇒ **침대당 ≈ 1.5–2 h · 둘 차례로 ≈ 3–4 h** (어림 · GPU 공유 정도에 따라).

### 1-4. 결과 검사 — 읽기만 · 이 출력을 보내 주세요

- (10-23 정정 · `SELF-130`) 기준 런 = 기록에 적힌 폴더로 직접 지정 — 첫 판은 옛 킷의 `latest_run` 을 읽어 kgy 에서 FileNotFoundError (`kit_SBE/latest_run` = v100 시절 절대 경로 링크 · 가리키는 런 = 08-12 런 · 등록 기준 08-27 런 아님 · 원자료 = `docs/data/rint2_recompaction_vgcf100_20261023/s1_4_output.txt`).

```bash
python3 - <<'PY'
import glob, hashlib, json, os
import numpy as np
H = os.path.expanduser('~/sdcp')

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()[:16]

#: 기준 런 = 기록에 적힌 폴더 (옛 킷 latest_run 은 쓰지 않는다 — kit_SBE 의 것은 v100 절대 경로 · 08-12 런 · SELF-130)
REF = (('kit_SBE_vgcf100', 'kit_SBE/run_VGCF3_PTFE1_20260827_134104_3672586'),
       ('kit_DBE_sdcp1um_vgcf100', 'kit_DBE_sdcp1um/run_VGCF3_PTFE0.5_SDCP0.5_20261019_191217_2231061'))
for new, ref in REF:
    ro, rn = os.path.join(H, ref), os.path.realpath(os.path.join(H, new, 'latest_run'))
    print(f'── {new}  (기준 {ref})\n   런 {os.path.basename(rn)} · 완료 마커 {os.path.exists(os.path.join(rn, "mpm_done.marker"))}')
    if not os.path.isfile(os.path.join(ro, 'mpm_metrics.json')):
        print('   ⚠ 기준 런 없음 · 있는 run_*:', sorted(os.path.basename(x) for x in glob.glob(os.path.join(H, ref.split('/')[0], 'run_*'))))
        continue
    mo, mn = (json.load(open(os.path.join(r, 'mpm_metrics.json'))) for r in (ro, rn))
    for k in ('E_anchor', 'dt_effective', 'platen_mach_VcP', 'quasistatic_violation', 'porosity_at_target_pct',
              'porosity_settled_pct', 'thickness_um'):
        print(f'   {k:24s} {str(mo.get(k)):>40s} → {mn.get(k)}')
    for a in ('VGCF', 'PTFE', 'SDCP'):
        ao, an = ((m.get('additives') or {}).get(a) or {} for m in (mo, mn))
        if ao or an:
            print(f'   {a:5s} E_GPa {ao.get("E_GPa")} → {an.get("E_GPa")} · n_points {ao.get("n_points")} → {an.get("n_points")}')
    for f in ('phase.npy', 'fibre.npy', 'fibre_kind.npy', 'fibre_dia.npy', 'se_dump.npy'):
        po, pn = os.path.join(ro, f), os.path.join(rn, f)
        if os.path.exists(po) and os.path.exists(pn):
            print(f'   {f:16s} {"같음" if sha(po) == sha(pn) else "다름"}')
    ph = np.load(os.path.join(rn, 'phase.npy'))
    u, c = np.unique(ph, return_counts=True)
    print('   점 수 (상별)', dict(zip(u.tolist(), c.tolist())), '· 합', len(ph))
PY
```

결과 전 기대 (판정 아님 · 다르면 그대로 적는다):

| 칸 | 기대 | 근거 |
|---|---|---|
| `E_anchor` | 둘 다 `ADD_E_SET_20260926_VGCF100GPa` | 기본 세대 (§1-0) |
| VGCF `E_GPa` | 10 → 100 | 같음 |
| `dt_effective` | → ≈ 1.311 × 10⁻⁴ (옛 SBE 08-27 메트릭에는 칸이 없을 수 있다 · 옛 DBE 2.0 × 10⁻⁴) | [우리 산술] CFL 0.4·dx/√134.6 · dx = 1/263 (§1-5) |
| `platen_mach_VcP` | 0.2717 → ≈ 0.41 | [우리 산술] §1-5 |
| `porosity_at_target_pct` | 숫자 (None 아님 = 목표 도달) | DO-NOT 블록 — None 이면 *"목표 미달"* 로 읽기 전에 보내 주세요 |
| `thickness_um` · `porosity_settled_pct` | 옛 72.53 µm · 7.86 % (SBE) / 7.37 % (DBE) [리포] 와 **비교만** — 새 값 = 결과 | MPM union 진단값 (전극 porosity 아님 · Table S3 §1) |
| `phase` · `fibre` · `fibre_kind` · `fibre_dia` npy | **같음** (같은 시드 · 시딩은 E 를 안 쓴다 (추정) · R2 에서 08-27 ↔ 10-19 코드 사이 VGCF · PTFE 시딩이 같았다) · 다르면 *"새 실현"* 으로 적는다 | 등록 v2 §7 R2 |
| `se_dump` | **다름** (압밀이 바뀌었다) | — |
| 점 수 | 각자 기준 침대와 같음 — DBE 기준 (`kit_DBE_sdcp1um`) = 합 67,919,722 · SE 66,044,152 · VGCF 1,643,483 · PTFE 115,555 · SDCP 116,532 [리포 · R1 · R2] · SBE 기준 (`kit_SBE`) = VGCF 1,643,483 · PTFE 235,046 · SDCP 0 [리포 · `docs/reviews/handoff_20260831_manuscript_track.md` 211–212 행] (합 · SE 는 이 출력이 처음) | — |

### 1-4b. (10-21 · Codex 판정문 §5-2 · 1저자 Q10 권고대로) 재압밀 추가 기록 칸 — 읽기만 · 이 출력도 보내 주세요

- 왜: 압밀 명령은 별도 핀 `298a73197` (§1-1) 이라 판정문 §5-2 의 핀 코드 스칼라 검산을 **그 실행물의 동일성 증서로 쓰지 않는다** → 실제 실행 코드 지문 + 추가 출력으로 확인한다 (판정문 §5-2 · 설계 §1-5 ⑥).  압밀 코드는 고치지 않는다 — 그 핀의 metrics 에 있는 칸 (`dt_requested` · `dt_effective` · `dt_cfl_cap` · `dt_cfl_limited` · `sub` · `frames_budget` · `stop_mode` · `settled_over_target` · `platen_mach_VcP` · `platen_mach_VcS`) 은 그대로 읽고, 나머지 (CFL 을 제한한 상 · 실제 substep · 누적 코드 시간 · stroke / hold 코드 시간 · 종료 이유 · 압력 궤적 · 재시도 · 선별 이력 · 실행 코드 지문) 는 metrics · 로그 · 킷 폴더에서 유도한다.
- 시간 = **코드 단위** (밀도 1 등의 코드 규약 · 초 아님 · 판정문 §5-2) · 로그 frame 줄은 5 프레임마다 (`--print-every` 기본 5) 라 substep · 시간은 어림 (범위로 찍는다).

```bash
python3 - <<'PY'
import glob, hashlib, json, os, re, subprocess
H = os.path.expanduser('~/sdcp')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def p_modulus(E, nu):                    # M = λ + 2μ [GPa] — 압밀 코드의 CFL 식이 쓰는 P파 탄성률 (ρ = 1 코드 단위)
    mu = E / (2.0 * (1.0 + nu))
    la = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
    return la + 2.0 * mu


#: 첨가제 ν = 핀 `298a73197` 의 `scripts/mpm3d_compaction.py` `ADD_E_NU` 표 (156–162 행) — metrics 의 additives 칸에는 E 만 있다
NU_ADD = {'VGCF': 0.30, 'SuperP': 0.30, 'PTFE': 0.30, 'SDCP': 0.35, 'SWCNT': 0.30}


FR = re.compile(r'\s*frame\s+(\d+)\s+\[(\w+)\].*?wallP=\s*([-+0-9.eE]+).*?porosity=\s*([-+0-9.eE]+)%')
for kit in ('kit_SBE_vgcf100', 'kit_DBE_sdcp1um_vgcf100'):
    K = os.path.join(H, kit)
    run = os.path.realpath(os.path.join(K, 'latest_run'))
    m = json.load(open(os.path.join(run, 'mpm_metrics.json')))
    print(f'── {kit} · 런 {os.path.basename(run)}')
    for k in ('protocol', 'stop_mode', 'n_grid', 'sub', 'frames_budget', 'dt_requested', 'dt_effective', 'dt_cfl_cap',
              'dt_cfl_limited', 'platen_mach_VcP', 'platen_mach_VcS', 'settled_over_target', 'E_SE_GPa', 'nu_SE'):
        print(f'   {k:24s} {m.get(k)}')
    # ① CFL 을 제한한 상 — M_max = (0.4 / (n_grid · dt_cfl_cap))² 를 SE · 첨가제 (ν = 위 핀 표) 의 M 과 맞춘다
    ng, cap = m.get('n_grid'), m.get('dt_cfl_cap')
    if ng and cap:
        Mmax = (0.4 / (ng * cap)) ** 2
        cand = {}
        if m.get('E_SE_GPa') is not None and m.get('nu_SE') is not None:
            cand['SE'] = p_modulus(float(m['E_SE_GPa']), float(m['nu_SE']))
        for a, d in sorted((m.get('additives') or {}).items()):
            if isinstance(d, dict) and d.get('E_GPa'):
                if a in NU_ADD:
                    cand[a] = p_modulus(float(d['E_GPa']), NU_ADD[a])
                else:
                    print(f'   ⚠ 첨가제 {a}: 핀 표에 ν 없음 → CFL 후보에서 뺌 (보내 주세요)')
        hit = [n for n, M in cand.items() if abs(M - Mmax) <= 1e-6 * Mmax]
        print(f'   CFL 제한 상              M_max {Mmax:.8g} GPa → {hit or "맞는 상 없음 (보내 주세요)"} · 후보 '
              + ' · '.join(f'{n} {M:.8g}' for n, M in cand.items()))
    else:
        print('   CFL 제한 상              dt_cfl_cap · n_grid 칸 없음 (옛 산출물)')
    # ② 로그 — frame 줄 (5 프레임마다) · 종료 줄 · FINAL
    log = os.path.join(run, 'mpm_run.log')
    fr, held, conv, final, tail = [], False, False, None, []
    if os.path.exists(log):
        with open(log, encoding='utf-8', errors='replace') as f:
            for ln in f:
                mm = FR.match(ln)
                if mm:
                    fr.append((int(mm.group(1)), mm.group(2), float(mm.group(3)), float(mm.group(4))))
                held = held or ('✓ held at target' in ln)
                conv = conv or ('✓ converged' in ln)
                if ln.startswith('FINAL'):
                    final = ln.strip()
                if ln.strip():
                    tail = (tail + [ln.rstrip()])[-3:]
    why = ('hold — 도달 뒤 40 프레임 이완 (✓ held at target)' if held else 'servo 수렴 (✓ converged)' if conv
           else '종료 줄 없음 — 프레임 예산 끝 또는 그 밖 (아래 로그 끝 세 줄)')
    print(f'   종료 이유                {why} · FINAL {"있음" if final else "없음"}')
    sub, dt = m.get('sub'), m.get('dt_effective')
    if fr and sub and dt:
        last = fr[-1][0]
        reach = next((f for f, ph, _w, _p in fr if ph != 'descend'), None)
        lo_n, hi_n = (last + 1) * sub, (last + 5) * sub
        print(f'   frame 줄                 {len(fr)} 개 · 마지막 frame {last} · 첫 비-descend frame {reach} (도달 어림 · ±5)')
        print(f'   실제 substep (어림)      {lo_n} – {hi_n} · 누적 코드 시간 {lo_n * dt:.6g} – {hi_n * dt:.6g} (코드 단위 · 초 아님)')
        if reach is not None:
            print(f'   stroke · hold 코드 시간  ≈ {reach * sub * dt:.6g} · ≈ {(last + 1 - reach) * sub * dt:.6g} (어림)')
        wp = [w for _f, _ph, w, _p in fr]
        print(f'   wallP 궤적 (frame 줄)    최대 {max(wp):.4g} · 끝 {wp[-1]:.4g} GPa · 끝 porosity {fr[-1][3]:.4g} %')
    print('   로그 끝 세 줄            ' + ' ⏎ '.join(x[:110] for x in tail))
    # ③ 재시도 · 선별 이력 — 킷의 run_* 디렉터리 전부 (지우지 않는다 · 10-23 정정 SELF-130: 'run_*/' = 디렉터리만 — 'run_*' 는 run_mpm.sh 파일도 집었다)
    runs = sorted(d.rstrip('/') for d in glob.glob(os.path.join(K, 'run_*/')))
    print(f'   재시도 · 선별            run_* {len(runs)} 개 (latest_run → {os.path.basename(run)})')
    for r in runs:
        ls = []
        lg = os.path.join(r, 'mpm_run.log')
        if os.path.exists(lg):
            with open(lg, encoding='utf-8', errors='replace') as f:
                ls = [x.rstrip() for x in f if x.strip()]
        print(f'     {os.path.basename(r)} · 완료 마커 {os.path.exists(os.path.join(r, "mpm_done.marker"))} · '
              f'로그 끝 {(ls[-1][:90] if ls else "")!r}')
    # ④ 실행 코드 지문 (검사 시점 — 런 뒤 ~/dem-anchor1019b 를 건드리지 않았다는 §1-1 기록과 함께 읽는다)
    scr = os.path.realpath(os.path.join(K, 'scripts'))
    mp = os.path.join(scr, 'mpm3d_compaction.py')
    head = subprocess.run(['git', '-C', scr, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(['git', '-C', scr, 'status', '--porcelain', '--untracked-files=no'], capture_output=True,
                           text=True).stdout.strip()
    print(f'   실행 코드 지문           scripts → {scr} · HEAD {head[:9] or "?"} · dirty {bool(dirty)} · '
          f'mpm3d_compaction.py sha256 {sha(mp)[:16] if os.path.exists(mp) else "없음"}')
PY
```

결과 전 기대 (판정 아님 · 다르면 그대로 적는다 · 이 스크립트는 10-21 에 가짜 킷 폴더로만 돌려 봤다 [합성] — 실제 kgy 출력은 처음):

| 칸 | 기대 | 근거 |
|---|---|---|
| `dt_cfl_limited` · CFL 제한 상 | 새 두 킷 = True · VGCF (M ≈ 134.6 · ν 0.30 = 핀 `ADD_E_NU` 표) | 판정문 §5-2 (VGCF M 134.61538462 GPa) · 핀 `298a73197` `scripts/mpm3d_compaction.py` 156–162 행 |
| `dt_cfl_cap` · `dt_effective` | ≈ 1.3108617603 × 10⁻⁴ (옛 = SE 제한 cap 2.9722242377 × 10⁻⁴ > 요청 2.0 × 10⁻⁴ 라 dt 2.0 × 10⁻⁴) | 판정문 §5-2 |
| 종료 이유 | `--protocol hold` → *"✓ held at target, relaxed (LIGGGHTS protocol)"* (도달 뒤 40 프레임 · 핀 `298a73197` 의 `scripts/mpm3d_compaction.py` 3545–3552 행) | 핀 코드 |
| 누적 코드 시간 | 150 프레임 예산 = 150 × 40 × dt = 0.7865170562 이하 (옛 1.2) · hold 40 프레임 = 0.2097378816 (옛 0.32) — 실제 총량은 종료 경로에 따라 다르다 | 판정문 §5-2 (예산) |
| 재시도 · 선별 | 이번 재압밀의 시도 전부 (OOM · 다른 venv 등 실패 시도 포함 · 지우지 않는다) | 판정문 §5-2 ("모든 재시도/선별 이력") |
| 실행 코드 지문 | scripts → `~/dem-anchor1019b/scripts` · HEAD `298a73197` · dirty False | §1-1 |

### 1-4c. (10-23 · 선택 · 기술 보고 · 판정 미사용) SE 위치가 얼마나 바뀌었나 — 읽기만

- 옛 · 새 침대는 시딩이 같아 (`phase` 같음) 점 순서가 같다 → 점마다 최종 위치 차.  단위 = metrics `um_box_um` (µm / 상자 단위 · scaffold 상자 x · y 0.04–0.96 = 50 µm · `scripts/mpm3d_compaction.py` 1950 · 2028 행) · 옆 경계가 주기면 최소 영상으로 접는다 (주기 = 격자에 맞춘 폭 · 같은 파일 2095 · 2799 행).
- ⚠ 첫 판 (10-23 채팅) 은 1 단위 = 1000 µm 로 잡아 값이 18.40 배 컸다 (`SELF-131` · 철회) — 아래가 고친 판이다.

```bash
python3 - <<'PY'
import json, os, re
import numpy as np
H = os.path.expanduser('~/sdcp')
PAIRS = (('SBE', 'kit_SBE/run_VGCF3_PTFE1_20260827_134104_3672586', 'kit_SBE_vgcf100/latest_run'),
         ('DBE', 'kit_DBE_sdcp1um/run_VGCF3_PTFE0.5_SDCP0.5_20261019_191217_2231061', 'kit_DBE_sdcp1um_vgcf100/latest_run'))
NAME = {1: 'SE', 2: 'VGCF', 4: 'PTFE', 5: 'SDCP'}
for tag, a, b in PAIRS:
    ra, rb = os.path.join(H, a), os.path.realpath(os.path.join(H, b))
    m = json.load(open(os.path.join(rb, 'mpm_metrics.json')))
    um, ng = float(m.get('um_box_um') or 1000.0 * float(m.get('lateral_box', 0.05)) / 0.92), int(m['n_grid'])
    P = round(0.92 * ng) / ng                     # 옆 주기 = 격자에 맞춘 폭 (mpm3d_compaction.py 2095 · 2799 행)
    xy = sorted(set(re.findall(r'xy=(periodic|walls)', open(os.path.join(rb, 'mpm_run.log'), encoding='utf-8', errors='replace').read())))
    print(f'── {tag}: µm/단위 {um:.4f} · 옆 경계 {xy or "기록 없음"} · 주기 {P:.8f} 단위 = {P * um:.4f} µm')
    ph = np.load(os.path.join(rb, 'phase.npy'), mmap_mode='r'); n = ph.size
    pa = np.load(os.path.join(ra, 'se_dump.npy'), mmap_mode='r').reshape(n, 3)
    pb = np.load(os.path.join(rb, 'se_dump.npy'), mmap_mode='r').reshape(n, 3)
    acc, wrap = {c: [] for c in NAME}, {c: 0 for c in NAME}
    for s in range(0, n, 4_000_000):
        e = min(n, s + 4_000_000)
        dv = pb[s:e].astype(np.float64) - pa[s:e]
        w = (np.abs(dv[:, 0]) > P / 2) | (np.abs(dv[:, 1]) > P / 2)
        dv[:, :2] -= P * np.round(dv[:, :2] / P)      # 최소 영상 (x · y 만 · z 는 접지 않음)
        d = (np.sqrt((dv * dv).sum(1)) * um).astype(np.float32)
        p = np.asarray(ph[s:e])
        for c in NAME:
            mk = p == c
            if mk.any():
                acc[c].append(d[mk]); wrap[c] += int(w[mk].sum())
    for c, nm in NAME.items():
        if not acc[c]:
            continue
        d = np.concatenate(acc[c])
        q = np.percentile(d, [50, 90, 99, 99.9])
        print(f'   {nm:5s} n {d.size:>10,d} · 중앙 {q[0]:.5f} · p90 {q[1]:.5f} · p99 {q[2]:.5f} · p99.9 {q[3]:.5f} · 최대 {d.max():.4f} µm · '
              f'> 0.15 µm {np.mean(d > 0.15) * 100:.3f} % · > 0.4 µm {np.mean(d > 0.4) * 100:.3f} % · 주기 넘은 점 {wrap[c]}')
PY
```

- ★ **10-23 결과 (§1-4 · §1-4b · §1-4c)** = `docs/data/rint2_recompaction_vgcf100_20261023/README.md` — 결과 전 기대 전부 일치 · 두께 · porosity 는 옛 값과 같음 · SE 위치 차 p99 0.079 · 0.075 µm (기술 보고).

### 1-5. ⚠ 1저자 결정 — 이 두 킷의 플래튼은 기하 규칙이라 VGCF 100 GPa 가 **재하율도** 바꾼다 (산술 · 결과 전)

- CFL: dt = min(2.0 × 10⁻⁴, 0.4·dx/√M) · M = max(SE (E 1.53 · ν 0.49) 26.19 · VGCF 100 GPa 134.6) GPa → n_grid 263 에서 **2.0 × 10⁻⁴ → 1.311 × 10⁻⁴ (× 1/1.526)**
  [우리 산술 · `scripts/mpm3d_compaction.py` 1912–1929 행 · Phase A 재현의 n_grid 256 값 1.3467 × 10⁻⁴ 와 같은 식].
- 두 킷은 `--platen-mach` 없는 **기하 규칙** (V/c_P 0.2717 = 이 침대 높이에서 기하 규칙이 주는 값) — 프레임당 걸음 vmax = 0.008·(WALL0 − FLOOR) 는 dt 와 무관하고
  (3075 행) 프레임 시간 = sub·dt 만 짧아진다 ⇒ 같은 150 프레임 · 같은 스트로크에서 **V/c_P 0.2717 → ≈ 0.41** [우리 산술].
  Phase A 재현은 `--platen-mach 0.03` 고정이라 재하율은 같고 dt 만 바뀌었다 (그 등록의 *"E + dt 세대 전환"*) — 여기서는 한 축 (재하율) 이 더 섞인다.
- 선택지:
  - **(가) 지시대로 VGCF 만 바꾼다 (§1-1 명령 그대로)** — 옛 ↔ 새 침대 차이는 *"E + dt + 재하율 세대 전환"* 으로만 부른다 (분해 없음) · 다음 세대 안에서 SBE ↔ DBE 는 같은 전환이라 같은 조건.
  - (나) V/c_P 를 0.2717 로 묶는다 — 두 킷 압밀 줄에 `--platen-mach 0.2717 --frames 229` (150 × 1.526 · 같은 스트로크) — 재하율은 같고 E + dt 만 바뀐다 · 압밀 시간 × ≈ 1.5.
- **권고 (가)** — 1저자 지시 범위 그대로이고, Phase A 재현 때 1저자 결정 (가) (분해 팔 안 돌림) 과 같은 꼴 · 다음 세대 R 판정은 새 두 침대끼리만 쓴다 (현 세대와 한 표에 섞지 않는다 · 등록 R §7-2).
- (10-21 · Codex 판정문 §5-2 · A24 · 1저자 Q10 권고대로) 핀 코드 스칼라 검산 (Codex · 핀의 MPM 코드 스칼라 블록에서): SE M = λ + 2μ = 26.18456376 GPa (영률 E 1.53) · VGCF 100 GPa 의 M = 134.61538462 GPa · CFL 한계 2.9722242377 × 10⁻⁴ → 1.3108617603 × 10⁻⁴ · 실제 dt 0.0002 (요청) → 0.000131086176026 (CFL) · 같은 프레임 스트로크의 속도 비 1.5257138934 · V/c_P 0.2717 → 0.4145364648 (요청서의 반올림 입력 0.2717 로 · 실제 H 를 새로 잰 값 아님) · SE S파 기준 Mach 1.9403261040 → 2.9603824947 · 150 × 40 step 예산 시간 1.2 → 0.7865170562 · 40 프레임 hold 0.32 → 0.2097378816 (코드 단위 · 초 아님) — 위 [우리 산술] 어림 (≈ 1.311 × 10⁻⁴ · ≈ 0.41) 과 같은 방향 · 이름 *"E + dt + 재하율 세대 전환"* 은 맞다 · 그러나 *"같은 전환이므로 SBE/DBE 동적 오차 상쇄"* · *"VGCF E 단독 효과"* 는 성립하지 않는다 (SBE 보정값이 SBE 의 기하 오차를 흡수해도 DBE 의 다른 오차까지 보정하지 않는다) · 이 검산은 실행물의 동일성 증서가 아니다 → §1-4b 의 실행 코드 지문 · 추가 출력 · 이 회신은 금지된 정지 기준 · 서보 재설계를 지시하지 않는다 (판정문 §5-2 끝 · CLAUDE.md DO-NOT).

## 2. ② S0 — 표현 원장 (raster-only · 솔브 없음 · CPU)

### 2-0. 작업 트리 (S0 도구가 든 커밋 — 메인이 가지에 옮긴 뒤 · 그 sha 를 알려 드립니다)

```bash
cd ~/dem-mt && git fetch -q origin claude/stoic-knuth-NObVQ && git worktree add --detach ~/dem-ca1 <S0 핀> && git -C ~/dem-ca1 log --oneline -1
ls ~/dem-ca1/scripts/ca_s0_census.py ~/dem-ca1/scripts/test_ca_s0_census.py
```

### 2-1. 시험 (CPU · 1 분 안팎)

```bash
. ~/dem-venv/bin/activate
python3 ~/dem-ca1/scripts/test_ca_s0_census.py 2>&1 | tail -3        # '121 PASS · 0 FAIL' 이어야 (2 일 차 판 · 옛 판 108) (payload 를 작은 픽스처로 실제로 돌린다 · GPU 없음 · 임시 git 저장소)
```

- (10-21) S0 census 보탬 (같은 셀 비연속 재방문 · 포트 동률 · 분산판 간선 · 간선별 덮임 — 수정 계획 Q1 · Q2 · Q3 · Q11 · 구현 중) 이 들어간 핀에서는 시험 수가 바뀐다 → 그 핀의 기대 숫자는 메인이 핀과 함께 알려 드린다 (그 전에는 위 121 을 기대값으로 쓰지 않는다).
- **(10-24 · `SELF-132`) kgy `~/dem-venv` = Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1** — 10-24 전 핀 (`fe1be7960` 등) 은 3.8 에서 이 시험 5 개 (E1 · E11 · R · R8 · A) 가 `dict |` TypeError 로 실패하고 단계 1 이 α 분포 계산에서 멈춘다 (10-23 23:56 kgy 시도 = `~/sdcp/ca1_s0_sbe_20261023` 에 payload 로그만 · 폴더 보존 · 새 시도는 새 폴더).  3.8 호환 수정 커밋 이후 핀만 쓴다 — 그 핀의 기대 = **152 PASS · 0 FAIL** (같은 라이브러리 판 재현 환경 · 증거 `docs/reviews/rint2_py38_compat_evidence_20261024/`) · 이 연장 세션의 커밋은 `claude/sdcp-dem-manuscript-si-pqwtv8` 에 있다 (§2-0 의 fetch 가지를 그것으로).

### 2-1b. (선택) 도구 시험 — 현 세대 `kit_SBE` (옛 침대 · 재압밀과 무관 · GPU 안 씀)

> **지위** — 실침대에서 S0 도구가 끝까지 도는지 · 거부 사유가 없는지를 재압밀 **전에** 보는 시험.  옛 침대 (VGCF 10 GPa 세대) 라 VGCF 경로 기하가 새 침대와 다를 수 있다 ⇒
> 이 출력의 숫자로 s_min · 문턱 (u · tol_ff · tol_P · tol_sj) 을 정하지 않는다 (등록 R §2-1 = 새 침대 단계 1) · σ 없음 (솔브 0) · 결과 열람 제약 없음 (census).  작업 트리 = §2-0 (핀 `aef62d81a` 이상).

```bash
python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 1 --kit ~/sdcp/kit_SBE --out ~/sdcp/ca1_s0_sbe_oldbed_tooltest 2>&1 | tee ~/ca1_s0_sbe_oldbed_tooltest.log
```

- 보내 주세요: 화면 끝 요약 (`── kit_SBE (단계 1)` 부터) · 거부되면 `[S0] ⛔ 거부 — …` 줄 (출력 폴더는 지우지 않는다).

### 2-2. 단계 1 — SBE 새 침대 (재압밀 완주 뒤 · 그 킷의 런이 돌고 있으면 거부된다)

```bash
python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 1 --kit ~/sdcp/kit_SBE_vgcf100 --out ~/sdcp/ca1_s0_sbe 2>&1 | tee ~/ca1_s0_sbe.log
ls -la ~/sdcp/ca1_s0_sbe && cat ~/sdcp/ca1_s0_sbe/cjunc_plan.sha256
```

- 산출: `s0_stage1_kit_SBE_vgcf100.json` (보고 · 2 일 차 블록 `junction_census` · `alpha_census` · `census_preview`) · `s0_instances_kit_SBE_vgcf100.npz` (instance 배열) ·
  `s0_junctions_kit_SBE_vgcf100.npz` (접합 후보별 배열 — 같은 가닥 후보의 fid · s · L_c · 배율 = s_min 근거) · `cjunc_plan.json` (정준 바이트) · `cjunc_plan.sha256` ·
  `payload_capture_kit_SBE_vgcf100.log`.
  - (10-21 · Codex 판정문 §7-1 · 1저자 Q1 · Q2 · Q3 · Q11 · 블록 · 칸 이름 = 구현이 정한다) 새 census = **같은 셀 비연속 재방문** (셀 수 · 섬유 수 · 두 구간 사이 호 길이 s 분포) · **포트 동률** (정준 규칙에서 거리가 같은 후보 수) · **긴 접촉** (수 · L_c 분포 · 분산판 간선 수 k) · **간선별 PTFE 덮임** — 보고 JSON 에 함께 · σ 칸 없음 그대로 · 원본 경로 · 표본화 · 침대 지문 (입력 sha256) 그대로 보존.
- **보내 주세요**: 화면 끝 요약 (`── kit_SBE_vgcf100 (단계 1)` 부터) · `cjunc_plan.json` · `cjunc_plan.sha256` · 보고 JSON → 리포 `docs/data/rint2_s0_sbe_<날짜>/` 로 반입
  (npz 는 크면 kgy 에 두고 sha256 만).  (10-21) + 새 census 블록 (위) 의 화면 요약.
- 그 뒤 (메인 세션 · 등록 R §2-1 · N17): 1저자 확인 (식 · 숫자를 **고르지 않는다**) → **등록 R §2-1 개정 커밋** = 숫자 (u · tol_ff · tol_P · tol_sj · 긴 접촉 수) +
  계획 sha256 + 계획 파일 (`docs/data/rint2_s0_sbe_<날짜>/cjunc_plan.json` — 바이트 그대로) · 결과 0 건 → 그 커밋 sha 로 단계 2.
  - (10-21 · Codex RCA-11 · 1저자 Q8 권고대로) 그 개정 커밋에 함께: **s_min 개발 단계** (s_min 은 "확인만" 이 아니다 — 위 s 분포를 보고 고르되 선택 규칙 · 후보 · 실패 처리 · 본 자료를 적고 DBE 열람 (단계 2) 전 재봉인 · 등록 R §2-1b) · **해시 두 줄** — S0 계획 (`cjunc_plan.json` · `ca-cjunc-plan-v1`) sha256 = 등록 R §2-1 `| S0 계획 해시 |` 줄 (단계 2 도구가 그 커밋의 등록 문서에서 이 값을 찾는다) · R 런 계획 (`rint-r-plan-v1` · 사슬 `--plan` · §3) 파일 · sha256 = `| 계획 해시 |` 줄 (사슬이 이 줄을 읽는다) · 두 계획의 `tol_ff` · `s_min` 대조 (등록 R §2-1 · ~~도구 ⬜~~ → (10-22 · 사전 리뷰 2 회차 PRE2-design-04 · 지금 동작) `tol_ff` = 단계 2 관문 (`verify_plan_commit` · L3m) · 사슬 사다리 (`plans_cross_problems` · C05) 가 본다 · `s_min` = §2-3 손 확인 ② (기계는 숫자가 있는지만 본다)).
  - **(10-21 · 사전 리뷰 PRE-design-03 · 1저자 Q-G 권고대로) 단계 2 전에 세 숫자** — 점 수 상한 (등록 R §3-2) · 역상 폭 상한 (§3-2b ④) · SV 반사실 문턱 (§5-6 · ~~+ 범위~~ · 세 R 여부 · ~~모서리 묶는 법~~ — (10-22 · 사전 리뷰 2 회차 PRE2-design-07 · 결정 없음) 끊는 범위 = Q-D 로 닫혔다 (다른 섬유 사이 SV 다리만 · 섬유 자기 연속은 남김 · 못 가른 덩어리 = 괄호 판정 Q1 (다) · 등록 R §5-6 SV 행) · 모서리 묶는 법 = "하나라도" (등록 R §10-2 ㉟ · Q-G 때 확정) → 정할 것 = 문턱 · 세 R 여부) = 1저자가 **Codex 재검토 회신 뒤** 정해 등록 R 개정 (결과 0 건) 으로 — 위 §2-1 개정 커밋에 함께 또는 그 앞 커밋 · 어느 쪽이든 **단계 2 에 넘기는 개정 커밋에 세 숫자가 있어야 한다** (단계 2 가 DBE 의 SV 우회 후보 수를 처음 연다 · 등록 R §11 ④) · ~~지금 도구는 이 셋을 확인하지 않는다 → §2-3 의 손 확인~~ → (10-22 · 사전 리뷰 2 회차 PRE2-design-04 · 지금 동작) 단계 2 관문이 확인한다 — `--r-plan-path` 의 R 런 계획에 결과 전 등록 숫자 넷 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱 · 세 R 여부 `sv_cf_scope`) 중 하나라도 null (⬜) 이면 거부 (`verify_plan_commit` → 사슬 `require_plan_numbers` · 시험 L3v · L3w).
  - **(10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 1저자 Q2 권고대로) 개정 커밋 전에 ⑥ 숫자 탐침 (§2-2b)** — 순서 = 단계 1 → s_min 개발 단계 → ⑥ (SBE · σ 봉인) → Codex 요청 (기하 + ⑥ 의 반복 수) → 회신 → 세 숫자 → 개정 커밋 **하나** (숫자 + S0 계획 해시 + R 런 계획 해시 (maxiter 포함 · R 런 계획 `p2_extra`) + s_min) → 단계 2.  DBE 를 본 뒤 계획을 다시 등록하지 않는다 — R 런 사슬이 단계 2 보고의 봉인 계획 해시를 지금 계획과 대조해 다르면 멈춘다 (`S0_REPORT_MISMATCH` · 등록 R §2-1 끝 줄 · §11 ④).  maxiter 는 넉넉하게 — DBE 팔은 같은 설정을 쓰고, 안 모이면 등록대로 그 팔이 멈춘다 (틀린 값을 내지 않음).
- 도구가 하는 것 (요약 · 정본 = 도구 머리 주석): payload 를 이 프로세스에서 돌려 생산 `rasterize` 입력을 잡고 (솔브 0 · 킷 폴더 쓰기 0 — 바뀌면 거부) 생산 · off (PTFE 행 뺌 =
  face_alpha 의 sid 격자) · SDCP 없는 판을 다시 굽는다 · 섬유 경로 셀 = 생산 `_fibre_segment_ijk` · 단계 1 은 SDCP 점이 하나라도 있으면 거부.
- 시간 · 자원 (어림): payload 앞부분 (STEP3 전) ≈ 수 분 — 10-19 SBE arm 0 (LEAN 2 · σ_e 만) 전체 879 s [리포 · 등록 v2 §7 C] 의 대부분이 전자 풀이다
  (같은 침대 최종 16 팔 a0 의 전자 풀이 704 s [리포 · 등록 v2 §7 10-20 00:2x 줄] · 서로 다른 런) — + raster 3 번 (DBE 4 번) + 경로 셀 · census
  (합성 1/10 크기 census 12 s [합성]) ⇒ **침대당 ≈ 15–30 분** · ~~RAM 수 GB (se_dump 1.6 GB 의 몇 배)~~ ⛔ 철회 11-04 — kgy 단계 1 (SBE) 이 메모리 **52.1 GB** 에서 신호로 끝났다 (출력 없음 · 원장 `SELF-155`) · 이 시간 어림도 실측 전 · 메모리 재기 → 도구 고침 뒤 다시 적는다.
- 거부되면 (`[S0] ⛔ 거부 — …`) 출력 폴더를 지우지 말고 그 줄을 보내 주세요 · 다시 돌릴 때는 **새** 출력 폴더 (도구가 비어 있지 않은 폴더를 거부한다).

### 2-2b. ⑥ 숫자 탐침 — SBE · σ 봉인 · ★ 단계 2 **앞** (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 1저자 Q2 권고대로 · 옛 자리 = §3 (2))

> **지위** — σ 를 보지 않는다 (반복 수 · 잔차 · 판 전류 불균형 · 시간만 · `--show-results` 없음 · 등록 R §11 예외).  DBE 를 열기 **전**에 돌려 maxiter (넉넉하게) · 전처리 · 시간 상한을 정하고, 그 값을 R 런 계획 (`p2_extra`) 에 넣어 §2-1 개정 커밋 **하나**로 봉인한다 (계획 다시 등록 없음 · 등록 R §11 ④ ⑥).
> 아래 `<계획 …>` 값 = 그 개정 커밋에 봉인할 R 런 계획의 값 (아직 커밋 전 · 같은 값) · 작업 트리 = §2-0 핀.

```bash
cd ~/dem-ca1 && git log --oneline -1 && git status --porcelain --untracked-files=no | head    # 핀 · 깨끗해야
. ~/dem-venv/bin/activate && unset SIGMA_VGCF_OVERRIDE
env VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=face_alpha BRIDGE_UM=0.48 SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_SDCP_OVERRIDE=256.6 SIGMA_FIBRE_BULK=1e4 \
    CJUNC=1 CJUNC_RJ=1e6 CJUNC_LEN_LAW=<계획 len_law> CJUNC_UNREG_LAW=cut CJUNC_S_MIN_UM=<계획 s_min_um> CJUNC_TOL_FF_UM=<계획 tol_ff_um> \
    CJUNC_PTFE_JLAW=P0 SDCP_MOD_C=0 STEP3_RTOL=<계획 step3_rtol> P2_EXTRA="--step3-maxiter <넉넉한 값 · 탐침이 반복 수를 잰다>" EXPECT_BACKEND=gpu \
    KITS=kit_SBE_vgcf100 ARMS=1 LEAN=2 OUTDIR=~/sdcp/ca1_probe bash ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh
```

- 보내 주세요: 러너 화면의 반복 수 · 잔차 · 판 전류 불균형 · 시간 줄 (σ 숫자 없이) → Codex 요청 (기하 + 반복 수) · 시간 결정점 (등록 R §10-4).

### 2-3. 단계 2 — DBE 새 침대 + 옛 `kit_DBE` (★ §2-1 개정 커밋 **뒤에만**)

```bash
# ⛔ (10-21 · PRE-design-14 · 철회) 가지 끝 FETCH_HEAD 로 단계 2 를 돌리면 단계 1 과 다른 판의 census · registry 가 돌 수 있다 (s_min 의 뜻이 바뀐다)
# ★ (봉인 · 20261118) 이 블록 = 인자 계약 꼴 — 실제 S0 단계 2 = §3-1b (2b) (sh 블록 · 인자 커밋 = 봉인 커밋 · --r-doc docs/reviews/rint2_seal_20261118/registration_R_sealed.md · --r-plan-path docs/data/rint2_r_plan_20261118/ca1_plan.json)
#   --r-doc 기본값 = 원본 자리 (봉인 전 판 · 해시 줄 ⬜) 라 이 블록 그대로면 관문이 거부한다 (틀린 결과 없음 · 멈춤)
# cd ~/dem-ca1 && git fetch -q origin claude/stoic-knuth-NObVQ && git checkout -q --detach FETCH_HEAD && git log --oneline -1   # 개정 커밋이 HEAD 의 조상이어야
# (10-21 · 개정 2) 단계 2 작업 트리 = §2-1 개정 커밋 그 자체
REV=<§2-1 개정 커밋 sha>
cd ~/dem-ca1 && git fetch -q origin claude/stoic-knuth-NObVQ && git checkout -q --detach "$REV" && git log --oneline -1 && git status --porcelain
# census · registry 가 단계 1 보고의 판과 같은지 (출력 없음 + rc 0 이어야 · 다르면 단계 2 를 돌리지 않는다 → 단계 1 을 이 판으로 다시 (σ 없음) · 개정 다시)
H1=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['code']['git_head'])" docs/data/rint2_s0_sbe_<날짜>/s0_stage1_kit_SBE_vgcf100.json)
git diff --quiet "$H1" "$REV" -- scripts/ca_s0_census.py scripts/carbon_junction.py scripts/ptfe_face_alpha.py scripts/step3_sigma.py \
    scripts/mpm_webapp_payload.py scripts/fibre_segment_raster.py scripts/sr01_stamp_compare.py; echo "same-version rc=$?"
# R 런 계획 줄 · 세 숫자 = 단계 2 관문이 본다 (10-22 PRE2-design-04 · 옛 주석 "도구가 아직 보지 않는다" 철회 · verify_plan_commit · L3i–L3w) · 손 확인 = s_min 값 (등록 R §2-1b) — 등록 줄을 그대로 화면에
grep -n '^| 계획 해시 |\|^| S0 계획 해시 |' docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md
# (10-22 · 사전 리뷰 2 회차 PRE2-design-05) --r-plan-path = 같은 개정 커밋의 R 런 계획 (리포 상대 · 없으면 관문 거부 · 등록 R §10-1 (1b) 와 같은 인자)
python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 2 --threshold-commit "$REV" \
    --plan-path docs/data/rint2_s0_sbe_<날짜>/cjunc_plan.json \
    --r-plan-path <같은 개정 커밋의 R 런 계획 경로> \
    --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe 2>&1 | tee ~/ca1_s0_dbe.log
```

- 도구가 확인 (아니면 거부): 개정 커밋이 이 작업 트리 HEAD 의 조상 · 그 커밋의 계획 파일 sha256 이 그 커밋의 등록 R 문서에 있음 · 계획 숫자 = 고정 식 재유도 · 정준 바이트 · (10-22 · PRE2-design-04 · 지금 동작) + 같은 커밋의 R 런 계획 (`--r-plan-path` · 아래 ③ 의 거부 목록).
- **(10-21 · 사전 리뷰 PRE-design-04 · 14 · 손 확인 — 도구가 보지 않는 것)** ① `same-version rc=0` (단계 1 보고의 `code.git_head` ↔ 개정 커밋의 census · registry 일곱 파일이 같다 · 보고의 `code.git_dirty` 가 true 면 = 다름으로 본다 · 보고의 `code.file_digests` 는 다섯 파일만 싣는다 — `carbon_junction.py` · `ptfe_face_alpha.py` 없음 → (10-22 · PF2 D) 일곱 파일로 보탰다 · R 런 사슬이 단계 1 · 2 보고의 일곱 지문을 R 런 코드와 대조한다 (`CODE_PIN_MISMATCH` · 등록 R §2-1b) — 이 손 확인 (단계 2 전) 은 그대로 둔다: 단계 2 (DBE 열람) 를 다른 판으로 돌리는 것을 미리 막는다) ② 위 grep 의 `| 계획 해시 |` 줄 끝 칸이 64 자 sha (⬜ 아님) · 그 R 런 계획 파일의 `s_min_um` = 등록 R §2-1b 값 · `tol_ff_um` = S0 계획 `values_um.tol_ff` (같은 float) ③ 세 숫자 (§2-2 끝) 가 그 개정 커밋에 있다 — 하나라도 아니면 **단계 2 를 돌리지 않는다** (~~실측: S0 계획 해시 줄만 채운 커밋도 지금 관문은 통과시킨다 [탐침 · 리포 밖] · 관문 보강 = 에이전트 A · 그 뒤 이 손 확인을 줄인다~~ → (10-22 · 사전 리뷰 2 회차 PRE2-design-04 · 지금 동작) 관문 보강됨 (`ca_s0_census.verify_plan_commit` · 시험 `scripts/test_ca_s0_census.py` L3i–L3w): ② 의 `| 계획 해시 |` 줄 ⬜ · 없음 · 둘 · 파일 sha256 ≠ 줄 · `tol_ff_um` ≠ S0 `values_um.tol_ff` · `s_min_um` null · `len_law` ≠ 원장 법칙 = 거부 · ③ 결과 전 등록 숫자 넷 중 null = 거부 (사슬 `require_plan_numbers` · L3v · L3w) — 남은 손 확인 = ① 과 ② 의 `s_min_um` = 등록 R §2-1b 값 (관문은 숫자가 있는지만 본다 · 등록 문서의 s_min 은 산문이라 기계가 읽지 않는다)).
- `git status --porcelain` 출력이 있으면 (작업 트리가 깨끗하지 않으면) 돌리지 않는다.
- 옛 `kit_DBE` (Ø0.30 낱알 · VGCF 10 GPa 세대) = **S0 표현 대조만** (설계 §1-2 #9) · 현 세대 `kit_DBE_sdcp1um` 도 대조로 보고 싶으면 `--kit ~/sdcp/kit_DBE_sdcp1um` 을 하나 더.
- DBE 전용 분포 (SDCP 근접 · 부피로 이미 이어진 몫 · SV · SDCP 경유 섬유 연결 · 긴 접촉 수) 는 여기서 처음 연다 (N17).
- 보내 주세요: 화면 요약 · 보고 JSON 둘 (→ `docs/data/rint2_s0_dbe_<날짜>/`).

## 3. ③ 런 사슬 — 꼴만 (⛔ 발사 금지)

> ⛔ **발사 = 등록 R §11 선행 관문 1–8 이 전부 선 뒤** — 구현 B0–B6 (시험 먼저 · 게이트 · 웹앱 같은 묶음 · Codex 구현 리뷰) · Codex 설계 리뷰 GO ·
> 1저자 N1–N18 ✅ (10-20) · S0 단계 1 → §2-1 개정 (s_min 포함) → 단계 2 (~~긴 접촉 ≥ 1 이면 여기서 멈춤 — §4 ①~~ → ✅ 10-20 밤 Q17: 멈추지 않는다 · 길이 비례 접합) · B1 합성 직접해 대조 → 수렴 숫자 개정 · 숫자 탐침 · 결과 전 어림 · 1저자 비준.
> (10-21) + Codex 판정문 HOLD (S2 · 등록 R 판정) → 수정 묶음 · 등록 R 3판 · 설계 3판 → **Codex 재검토 GO** · 등록 R §11 ⑨ (새 킷 = payload 두 토큰 뺀 판 · §1-1) — 관문 = 1–9.
> ~~노브 이름은 후보 (설계 §7) — B6 에서 확정해 등록 R §10 을 개정한다.  아래는 등록 R §10 의 꼴에 새 킷 이름만 넣은 것이다.~~ → (10-21) 실제 이름 = 등록 R §10 · §10-1 (러너 `scripts/sdcp_gain_vox015_8arm.sh` · 사슬 `scripts/rint_r_chain.py` · 기반 `47d23baba`) · 첫 블록 = 2판 이력 (철회) · 둘째 블록 = 실제 명령.

```bash
# ⛔ 2판 꼴 (10-20) — 후보 이름 (PTFE_JLAW · SDCP_C · CJUNC_PLAN · P2_EXTRA 의 --step3-rtol = 지금 러너가 거부) · <사다리 사슬> 자리표 · 철회 (10-21) — 아래 실제 명령 블록
# ⛔ 발사 금지 — 꼴만.  SIGMA_VGCF_OVERRIDE 는 env 에 없어야 한다 (SIGMA_FIBRE_BULK 와 함께 있으면 러너 거부 · 설계 §7)
# VGCF voxel σ = SIGMA_FIBRE_BULK=1e4 (Endo 단섬유) 를 러너가 직경 보존으로 7,853.98 S/cm (vox 0.15) 로 — 두 전극 같은 값 (1저자 10-20 · Q5)
COMMON="VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=face_alpha BRIDGE_UM=0.48 SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_SDCP_OVERRIDE=256.6 SIGMA_FIBRE_BULK=1e4 CJUNC_PLAN=<§2-1 개정의 계획>"
# (2) 숫자 탐침 — SBE · 값 봉인 (반복 수 · 잔차 · 판 전류 불균형 · 시간만)
env $COMMON P2_EXTRA="--step3-rtol <§3-5 봉인값> --step3-maxiter <탐침 뒤>" PTFE_JLAW=P0 CJUNC_RJ=1e6 SDCP_C=0 \
    KITS="kit_SBE_vgcf100" ARMS=1 LEAN=2 OUTDIR=~/sdcp/ca1_probe bash ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh
# (3) 보정 사다리 — 법칙 끝마다 (사슬이 점을 고르고 값을 봉인한 채 보간 · 식별성 · 허용폭 양끝)
python3 ~/dem-ca1/scripts/<사다리 사슬> --law P0 --target 1.63 --kit kit_SBE_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --out ~/sdcp/ca1_ladder_P0
python3 ~/dem-ca1/scripts/<사다리 사슬> --law P1 --target 1.63 --kit kit_SBE_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --out ~/sdcp/ca1_ladder_P1
# (4) 예측 — 네 모서리 × {R_j,lo · R_j,0 · R_j,hi} (DBE arm 0 · R_j 는 사다리 요약에서 사슬이 읽는다)
python3 ~/dem-ca1/scripts/<사다리 사슬> --stage predict --ladders ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1 --kit kit_DBE_sdcp1um_vgcf100 --out ~/sdcp/ca1_predict
# (5) 판정 — 원 JSON 전부에서 (다시 판정 도구로 같은 답인지)
python3 ~/dem-ca1/scripts/<사다리 사슬> --stage verdict --runs ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1 ~/sdcp/ca1_predict <origin · 감도 · 격자 폴더> --out ~/sdcp/ca1_verdict
```

- (10-21) **실제 명령** — 사슬 CLI = `scripts/rint_r_chain.py` 머리 (Z2 보고 꼴: `--stage ladder` (`--law` · `--target` · `--runner` · `--root` · `--plan` · `--max-hours` · `--out` · [`--variant FIBRE|UNREG|GRID`] · [`--dry-run`] · (10-22 · PRE2-design-01 · Q2) `--s0-stage2-report` 필수 · (10-22 · PF2 D · PRE2-design-08) `--s0-stage1-report` 필수 · ~~[`--machine`]~~ → (10-28 · 개정 4) `--machine` 필수) · `predict` (`--ladders` 둘 · `--kit` · `--runner` · `--root` · `--max-hours` · `--out` · [`--variant …|SVORDER`] · ~~[`--machine`]~~ → (10-28 · 개정 4) `--machine` 필수) · `verdict` (`--runs` · `--out` · [`--show-results`] · (10-25 · 묶음 B · RCA2-03 · Q3 (가)) `--root` 필수 = 킷을 S0 와 같은 발견 함수로 다시 해시 · 기계마다 자기 킷 사본) · `--reverify` (+ `--root`)) · 사슬이 런마다 러너 env 를 정한다 (`CJUNC=1` · `CJUNC_RJ` (`inf` · `0` 극한) · 계획의 `CJUNC_LEN_LAW` · `CJUNC_UNREG_LAW` · `CJUNC_S_MIN_UM` · `CJUNC_TOL_FF_UM` · `STEP3_RTOL` · `P2_EXTRA` · `CJUNC_PTFE_JLAW` · `SDCP_MOD_C` · `ARM_LIST` · `SIGMA_FIBRE_BULK` · `PTFE_STAMP=face_alpha` · 부모 셸의 같은 이름꼴 env 는 지운다 · `SIGMA_VGCF_OVERRIDE` 가 있으면 멈춘다).  (10-28 밤 · 개정 5) + `--stage ledger` (`--init` · `--add` · `--ledger-target` · [`--resume`]) · 사다리 · 예측 `--ledger` · `--attempt` · 판정 `--ledger` · `--stage recover` (`--out` · `--ledger` · [`--operator-confirm` · `--operator-why`]) — 아래 블록.
- ⚠ 이 CLI 는 지금 코드 그대로 · ~~등록 R 3판 규칙 (실제 역상 끝 · origin 세 R · 상태 분기 · 법칙별 구간 · 차단 표지 닫힌 집합 · 같은 판정 함수 · §5-3 문장) 은 아직 사슬에 없다 → 메인 통합 (시험 먼저) 뒤 CLI 가 바뀌면 이 블록을 다시 고친다.  (10-21 · 개정 2) 4판 규칙 (끝 origin = 세 origin 합집합 · 보호 띠 · 이름 우선순위 · 결정표 · 변이 표지) 도 아직 사슬에 없다 (등록 R §10-3).~~ → (10-22 · 사전 리뷰 2 회차 PRE2-design-04 · 지금 동작) 3판 · 4판 규칙은 사슬에 들어갔다 (메인 통합 · 등록 R §10-1 머리 · §10-3 4판 행 · 시험 `scripts/test_rint_r_chain.py`) · 바뀐 CLI = 아래 블록 (사다리 `--s0-plan` · `--s0-stage2-report` · `--s0-stage1-report` 필수 · 감도 단계 `--after-main` 필수 · 사다리 · 예측 ~~[`--machine`]~~ → (10-28 · 개정 4) `--machine` 필수).
- **(10-26 · 묶음 B″ · 1저자 10-26 Q1 (가) · Q3 · Q4 · 보고 = 묶음 B″ 보고 (같은 증거 폴더)) 봉인 원천 · venv · 메모리** — ① 예측 단계의 SV 모서리 런마다 사슬이 **같은 러너 · 같은 env + `CJUNC_GRAPH_ONLY=1`** 로 payload 를 조립만 다시 돌린다 (CG 없음 · 끝 그래프 지문 → 증서 지문과 대조 · 원천 런 폴더 = `<단계 폴더>/graph_src` · 기록 = 단계 요약 `sv_graph_source`) · 판정 · 다시 판정도 **각자 다시** 돌린다 (판정 = `<판정 폴더>/graph_src` + `verdict_graph_src.json` · 다시 판정 = 임시 폴더) · 원천 실패 = 그 모서리 `SV_UNCHECKED` (멈춤 아님) · 원천 런 시간은 그 단계의 `--max-hours` 안에 든다.  ② 사슬이 러너에 `MPM_NO_VENV=1` 을 준다 — payload 는 **이 셸 (venv 를 켠 사슬 프로세스) 의 python** 으로 돈다 (아래 `. ~/dem-venv/bin/activate` 줄을 빼지 않는다 · 원천 런의 환경 단위 ≠ 사슬 = 원천 실패).  ③ 메모리 = 쪼개 셈 없음 (1저자 Q3) · 지문 하나 ≈ 6 GB 일시 · SV 팔마다 지문 2–3 개 · 지문 시간 ≈ 70–85 s (SBE vox 0.15 · n_dof 26,438,766 · 간선 ≤ 79 M **추정** · 묶음 B 보고 §8) + payload 의 CG 밖 부분 (실침대 미측정) — 실측 = 원천 런 기록의 `cost.peak_rss_kb` (픽스처 실측 = 묶음 B″ 보고) · 런 전 확인 줄 = 아래 블록 (기록만 · 문턱 숫자 등록 없음 · 판단 = 1저자).
- **(10-21 · 사전 리뷰 PRE-design-06 · 1저자 Q-F 권고대로) 순서 = 주 판정 먼저** — ① (3) 사다리 P0 · P1 → (4) 주 예측 → (5) **주 판정** (감도 폴더 없이 · 그 판 = `*_UNCHECKED` 표지 (지금 사슬 = 변이 폴더가 없으면 `<V>_UNCHECKED` · `scripts/rint_r_chain.py` ~~1298–1303 행 · 코드 읽기 · 시험 전~~ → (10-22 · PRE2-design-04) `assemble` (줄 번호는 판마다 바뀐다) · 시험 V02) · 결과 문장 한정어 *"감도 미완료"* · 10-31 판정 = 이것) → ② 감도 (FIBRE · UNREG · GRID 사다리 + 예측 · SVORDER 예측) → (5) **전체 판정** (새 `--out` · 같은 주 판정 런 + 감도 폴더 · 두 기록을 나란히) · 시간 = 등록 R §10-4 (① 78 팔 ~~≈ 56 h · ×1.7–2 = 95–112 h~~ → (10-22 · PRE2-design-03 · Q3) ≈ 191–231 h [추정 · 합성 침대 반복 비] · ② 264 팔 · ×1.7–2 = 392–462 h [우리 산술 · 옛 어림]) · 주 판정을 본 뒤 감도를 빼거나 바꾸지 않는다.

```bash
# ⛔ 발사 금지 — 꼴만 (10-21 · 실제 이름 · 등록 R §11 관문 1–9 뒤)
# ★ (봉인 · 20261118) 이 블록 = 인자 계약 꼴 (리포 시험 K01 이 사슬 argparse 와 대조하는 bash 줄) — 실제 실행 = 봉인본 · --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md (아래 §3-1b 의 sh 블록)
#   (저장본 --cjunc-store · 12 단위 · 넘침 점 · 합치기 · 원장 이어달리기 (가-2) · --max-hours 168 · --machine kgy | gabia · S0 단계 2 = --r-doc docs/reviews/rint2_seal_20261118/registration_R_sealed.md)
#   아래 (4) 한 기계 예측 줄 = 이 등록의 경로가 아니다 (원장 하나 = 경로 하나 · 등록 R §10-5 가 ⑮ · 1저자 11-10 Q7)
#   다음 줄의 --untracked-files=no 는 사슬보다 덜 본다 (사슬 · 현장 도구 = normal · 남은 계획 §9 어긋남 7) → §3-1b (2) 의 줄을 쓴다
cd ~/dem-ca1 && git log --oneline -1 && git status --porcelain --untracked-files=no | head    # 핀 · 깨끗해야
. ~/dem-venv/bin/activate && unset SIGMA_VGCF_OVERRIDE
# (10-26 · 묶음 B″ · 1저자 Q3) 메모리 확인 — 런 전 · 기록만 (쪼개 셈 없음 · 지문 하나 ≈ 6 GB 일시 [추정 · 묶음 B 보고 §8] · 실측 = 원천 런 기록의 cost.peak_rss_kb)
free -g     # available 칸을 적어 보내 주세요 (문턱 숫자 등록 없음 · 판단 = 1저자) · 예측 · 판정 · 다시 판정 = SV 모서리마다 조립만 런 하나 (그 사이 다른 큰 작업을 띄우지 않는다)

# (0) R 런 계획 파일 = 등록 R §2-1 개정 커밋의 파일 (~~rint-r-plan-v1 · 칸 = schema · len_law · unreg_law · s_min_um · tol_ff_um · step3_rtol · p2_extra~~ → (10-21 · 4판 정정 · 코드 이름) rint-r-plan-v2 · 칸 11 = 그 일곱 + 결과 전 등록 숫자 넷 max_ladder_points · calib_rj_ratio_max · sv_cf_threshold · sv_cf_scope · `rint_r_chain.PLAN_KEYS` · 일곱 칸 꼴 = 사슬이 PLAN_INVALID 로 거부) 바이트 그대로
# ★ (봉인 · 20261118) 코드 = rint-r-plan-v3 · 칸 12 (= 위 v2 칸 11 + exec_policy 8 칸 · rint_r_chain.PLAN_SCHEMA · v2 계획 = PLAN_INVALID · 1저자 11-17 봉인 후보 Q3)
#   봉인 계획 파일 = ~/dem-ca1/docs/data/rint2_r_plan_20261118/ca1_plan.json (아래 cp 줄의 자리표 자리) · 해시 · 블록 = 봉인본 §2-1 (원본 자리의 줄은 ⬜ 그대로)
#   실제 실행 = 봉인본 · --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md (§3-1b) — 아래 sha256sum 줄의 대조 대상 = 봉인본의 '| 계획 해시 |' 줄
cp ~/dem-ca1/<§2-1 개정 커밋의 R 런 계획 경로> ~/sdcp/ca1_plan.json
sha256sum ~/sdcp/ca1_plan.json      # = 등록 R §2-1 '| 계획 해시 |' 줄 끝 칸 (다르면 사슬이 PLAN_HASH_MISMATCH · 칸이 ⬜ 면 PLAN_HASH_UNREGISTERED 로 멈춘다)

# ~~(2) 숫자 탐침 — SBE · 러너 직접 (사슬 밖) · 값 봉인 (반복 수 · 잔차 · 판 전류 불균형 · 시간만)~~
# (10-22 · 사전 리뷰 2 회차 PRE2-design-01 · 1저자 Q2) ⑥ 숫자 탐침은 여기서 돌리지 않는다 — S0 단계 2 **앞** (§2-2b · 계획 하나 봉인 · 다시 등록 없음)
# S0 단계 2 보고 = ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json (§2-3 · 이 보고의 봉인 계획 해시 ≠ 위 계획이면 사슬이 S0_REPORT_MISMATCH 로 멈춘다)
# (10-22 · PF2 D · PRE2-design-02 · 08) S0 단계 1 보고 = ~/sdcp/ca1_s0_sbe/s0_stage1_kit_SBE_vgcf100.json (§2-2) — 두 보고의 census · registry 일곱 파일 지문 ≠ 이 핀의
#   파일이면 사슬이 CODE_PIN_MISMATCH 로 멈춘다 (→ 단계 1 · 2 를 이 핀으로 다시 · 개정 다시 · DBE 가 열렸으면 s_min 다시 고르지 않음 · 등록 R §2-1b) ·
#   단계마다 이 트리가 깨끗해야 한다 (추적 파일 고침 = CODE_PIN_MISMATCH · 사슬이 코드 파일 지문을 단계 요약에 남기고 다음 단계 · 판정이 대조) ·
#   (10-28 · 개정 4 · 등록 R §10-5 가 ①) --machine <기계 이름표> = 필수 (사다리 · 예측 · 원장 --add · 계획 exec_policy.allowed_machines 안 ·
#   없음 = rc 2 · 목록 밖 = MACHINE_NOT_ALLOWED · 런 기록마다 · 판정이 대조) — 옛 "[--machine] = 단계 요약에 기록만 · 판정에 안 쓴다" 철회

# (2b) (10-28 밤 · 사전 공격 5 회차 봉인 전 남은 #4 · 등록 R §10-5 아) 시도 원장 — 빈 git 저장소 하나 (사슬 리포 밖 · 이 기계 · 한 줄 역사 · 덧붙이기만)
#      --init 한 번 (머리 = 위 계획 sha256 · 봉인 전 계획이면 거부) · 원장 저장소 · 시도 폴더를 손으로 고치지 않는다 (판정이 결과 줄을 폴더 증거로 다시 센다)
mkdir -p ~/sdcp/ca1_ledger && git -C ~/sdcp/ca1_ledger init -q
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --init --plan ~/sdcp/ca1_plan.json
#      시도마다 먼저 --add (대상 = ladder:P0 · ladder:P1 · predict · 감도 ladder:<법칙>:<변이> · predict:<변이> · 화면 ATTEMPT_ADDED n=<번호> → 아래 --attempt 에)
#      재실행 = 같은 대상 + --resume <원 시도 번호> (원 시도 결과 줄이 재실행 자격일 때만 · 같은 기계 · 같은 --out 바탕 폴더)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target ladder:P0 --machine <기계 이름표> \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp

# (3) 보정 사다리 — 법칙 끝마다 (먼저 같은 인자 + --dry-run = 첫 런 다섯 (바닥 · 천장 · 1e4 · 1e6 · 1e8) 의 env 만 찍는다 · 폴더를 만들지 않는다)
#     (10-22 · 사전 리뷰 2 회차 PRE2-design-05) --s0-plan = S0 단계 1 계획 (개정 커밋에 든 파일 · 없으면 인자 오류 rc 2 · 두 계획 대조) — 인자 = 등록 R §10-1 블록과 같다
#     (10-28 밤 · #4) 본 런 = 원장 시도 꼴 (--ledger ~/sdcp/ca1_ledger --attempt <그 대상 항목 번호> · 시도 폴더 = <--out>/attempt_<n>/ · 사슬이 만든다) ·
#     --dry-run 은 --ledger · --attempt 없이 (시도 꼴 입구가 --dry-run 을 거부 · rc 2) · 옛 줄 (원장 시도 꼴 아님) = git 이력 b80f98f98
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_<날짜>/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours <등록 R §10 시간 상한> --machine <기계 이름표> --out ~/sdcp/ca1_ladder_P0 --dry-run
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_<날짜>/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours <등록 R §10 시간 상한> --machine <기계 이름표> --ledger ~/sdcp/ca1_ledger --attempt <ladder:P0 항목 번호> --out ~/sdcp/ca1_ladder_P0
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P1 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_<날짜>/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours <등록 R §10 시간 상한> --machine <기계 이름표> --ledger ~/sdcp/ca1_ledger --attempt <ladder:P1 항목 번호> --out ~/sdcp/ca1_ladder_P1
# (4) 예측 — 네 모서리 × {R_j,lo · R_j,0 · R_j,hi} (DBE arm 0 · R_j · 계획 = 사다리 요약에서 사슬이 읽는다)
#     (10-28 밤 · #4) --ladders = 원장 채택 사다리 시도 폴더 (attempt_<n> · 재실행 사슬이면 그 끝 시도)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours <등록 R §10 시간 상한> \
    --machine <기계 이름표> --ledger ~/sdcp/ca1_ledger --attempt <predict 항목 번호> --out ~/sdcp/ca1_predict
# (5a) (10-21 · Q-F) 주 판정 — 감도 폴더 없이 · 값 열람 = 주 판정 런이 다 끝난 뒤 · 감도 런 전 (등록 R §4-1 · 열람 기록에 순서 · 시각) · 10-31 판정 = 이것
#     (10-25 · 묶음 B · RCA2-03 · Q3 (가)) --root = 킷 뿌리 (판정 · 다시 판정이 SBE · DBE 킷을 다시 해시해 S0 보고의 원 입력과 대조 · 다르면
#     S0_REPORT_MISMATCH · 재압밀 · 재생성 침대 = 새 S0) · 사다리 · 예측도 R 직전에 같은 대조 (사다리 = SBE · 예측 = SBE · DBE)
#     (10-28 밤 · #4 · 등록 R §10-5 가 ⑨) --ledger = 필수 · --runs = 원장 채택 시도 폴더 (attempt_<n>)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --runs ~/sdcp/ca1_ladder_P0/attempt_<n> ~/sdcp/ca1_ladder_P1/attempt_<n> \
    ~/sdcp/ca1_predict/attempt_<n> --root ~/sdcp --ledger ~/sdcp/ca1_ledger --out ~/sdcp/ca1_verdict_main [--show-results]
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict_main --root ~/sdcp
# 감도 (필수 · 등록 R §5-6 · (10-21 · Q-F) 주 판정 뒤): FIBRE · UNREG · GRID = 사다리 둘 (--variant <이름> --law P0 · P1) + 예측 (--variant <이름> --ladders <그 변이 사다리 둘>) ·
#   SVORDER = 예측만 (--variant SVORDER --ladders <주 사다리 채택 시도 폴더 둘>) · 출력 폴더는 런마다 새로 (예 ~/sdcp/ca1_ladder_P0_FIBRE)
#   (10-22 · 사전 리뷰 2 회차 PRE2-design-05) 감도 단계마다 (사다리 · 예측) --after-main ~/sdcp/ca1_predict (끝난 주 예측 · 없으면 MAIN_NOT_DONE · 등록 R §10-1)
#   (10-28 밤 · #4) 감도도 원장 시도 꼴 (--add --ledger-target ladder:P0:FIBRE 먼저) · --after-main = 주 예측 채택 시도 폴더 (~/sdcp/ca1_predict/attempt_<n>)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --variant FIBRE --after-main ~/sdcp/ca1_predict/attempt_<주 예측 채택 번호> --law P0 --target 1.63 \
    --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_<날짜>/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours <등록 R §10 시간 상한> --machine <기계 이름표> --ledger ~/sdcp/ca1_ledger --attempt <ladder:P0:FIBRE 항목 번호> --out ~/sdcp/ca1_ladder_P0_FIBRE
# (5) (전체) 판정 — 원 팔 JSON 전부에서 · 값은 --show-results 로 한 번 (판정에 쓰는 런이 다 끝난 뒤 · 열람 기록) · 다시 판정 = 읽기 전용 바이트 대조
#     (10-21 · Q-F) 주 판정 (5a) 뒤 두 번째 열람 — 같은 주 판정 런 + 감도 폴더 · 주 판정 숫자는 바뀌지 않는다
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --runs ~/sdcp/ca1_ladder_P0/attempt_<n> ~/sdcp/ca1_ladder_P1/attempt_<n> \
    ~/sdcp/ca1_predict/attempt_<n> <감도 시도 폴더 전부> --root ~/sdcp --ledger ~/sdcp/ca1_ledger --out ~/sdcp/ca1_verdict [--show-results]
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict --root ~/sdcp

# (멈춘 사슬 뒤 · 10-28 밤 · 등록 R §10-5 아 ③ ④) 사슬 부모가 죽었으면 (SIGKILL · 정전 · 컨테이너 재시작 · 접속 끊김) 다음 시도 전에 — 그룹 종료 확인 · 결과 줄
#   사슬이 아직 살아 있으면 recover 는 건드리지 않는다 (rc 3 · 사슬이 끝난 뒤 다시) · 같은 부팅 = 그룹 표지로 찾아 확인
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage recover --out ~/sdcp/ca1_ladder_P0 --ledger ~/sdcp/ca1_ledger
#   다른 부팅 · 다른 pid 이름공간 · 다른 machine_id = 미확인 (rc 3 · 결과 줄 없음) → 그 그룹이 끝났음을 사람이 확인한 뒤에만 (그 기계의 uptime · 부팅 기록 ·
#   표지 프로세스 없음) — 시도 번호 하나 · 사유 한 줄 (끝 기록 operator 칸에 남는다 · 그 시도 폴더의 여기서 볼 수 없는 그룹만)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage recover --out ~/sdcp/ca1_ladder_P0 --ledger ~/sdcp/ca1_ledger \
    --operator-confirm <시도 번호> --operator-why "<확인한 것 · 한 줄>"
```

## 3-1b. ③′ R 의 실제 실행 — 12 단위 경로 · kgy · gabia 동시 · 원장 이어달리기 (가-2) (봉인 · 20261118 · 1저자 11-10 Q3 · Q4 · Q7 · 3 판 Q1 – Q11 · 봉인 후보 Q1 – Q7 · 결과 0 건)

> **머리 — 실행 정책 문장** (1저자 11-10 Q4 = 등록 R 의 실행 정책 문장 + 이 블록 머리 · 정본 = 봉인본 §10-8)
> - **등록 문서 = 봉인본** `~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md` — 아래 **모든** 사슬 명령에 `--registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md` · S0 단계 2 에 `--r-doc docs/reviews/rint2_seal_20261118/registration_R_sealed.md` (봉인 후보 Q1 · 기본 경로 = 원본 자리 = 봉인 전 판 → 해시 줄 ⬜ → 멈춤 · 틀린 결과는 없다).
> - kgy = uid 1003 · **모든 실행 셸에서 `umask 022`** (11-09 · 11-12 현장 = 002) · gabia = uid 0 (root) 그대로 (일반 로그인 계정 없음) — root · 같은 uid 에게 0600 · 단일 작성자 보호는 뜻이 없다 = 운영 규칙.
> - 단일 작성자 — 계획 사본 · 원장 · 시도 폴더 · 저장본 폴더 · 판정 폴더는 실행 사용자 하나만 · 손으로 고치지 않는다 · kgy `~/sdcp` = 0775 (그룹 구성원 [미확인]) · `~/sdcp/scripts` (0777) 는 R 출력 자리로 쓰지 않는다.
> - 값 비열람 — σ · SV 비 · origin 산포 = `verdict_results.json` (0600) 에만 · `--show-results` = 주 판정 런이 다 끝난 뒤 한 번 · 열람 기록 · 그 밖 화면 · 로그 · 보고에 σ 를 옮기지 않는다.
> - 숫자 = 봉인 계획 그대로: `--max-hours 168` · maxiter 5,000,000 (계획 `p2_extra` · 사슬이 편다) · 최대 시도 수 8 · 허용 기계 kgy · gabia · v100 (v100 = 1저자 요청 때만).
> - **한정 (Codex 2/2 §7-3 · 정본 = 봉인본 머리 절 R-00)** — 위 숫자 (5,000,000 · 168 h · 8 · 넘침 점 112 h) = 정책 값 · **완료 보장 아님** · RCA-11 = 이 R 의 입력 · 선택 고정만 한정 종결 (원장 전체 = 부분) · `env_unit` = 같음 대조 단위일 뿐 전체 실행 환경이 아니다 (python 패치 판 · cupy · GPU · 드라이버 · BLAS · SIMD = 사슬이 기록만) · 기준 기록 = 아래 (2) 의 venv 한 줄 · `nvidia-smi` 줄 출력 (두 기계 · 적어 둔다) · 확인 = 1저자 · 실행 승인 = 1저자 (Codex 2/2 = 봉인 준비 범위만).

### (1) 기계마다 바탕 (두 기계 같은 상대 자리 · `~` = 그 기계 실행 사용자 홈)

| 무엇 | 자리 | 비고 |
|---|---|---|
| 실행 트리 | `~/dem-ca1` = `<봉인 커밋>` 의 분리 작업 트리 · **새로 만든다** (봉인 커밋 = `64e4d213e` 위 문서 커밋 · 기존 트리와 다른 체크아웃) · 깨끗 | R (사다리 시작부터 다시 판정까지) 동안 바꾸지 않는다 · 11-17 현장: kgy 기존 트리 = `<HOME>/dem-p6-64e4d213e` · `<HOME>/dem-s0-64e4d213e` (핀 트리) · gabia = `dem-mt` 없음 · 기존 트리 `<HOME>/dem-siteq-11a794674` · `<HOME>/dem-siteq-db86ce9b9` → 기존 트리는 그대로 두고 그 저장소에서 새 작업 트리를 뗀다 ((2) 첫 줄들) · 이름 `~/dem-ca1` 이 이미 있으면 지우지 않고 1저자 — 다른 이름이면 아래 줄의 `~/dem-ca1` 을 그 이름으로 |
| 봉인본 | `~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md` | 봉인 커밋 안 (등록 R 의 봉인 판) · 원본 자리 `~/dem-ca1/docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` = 봉인 전 판 + 표지 한 줄 (사슬 기본값 · 쓰지 않는다) |
| venv | `~/dem-venv` — **두 기계 같은 자리 · 같은 판** (Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · cupy 12.3.0 = 계획 `env_unit` 통과 · 11-17 현장 · 1저자 결정 = 패치 판까지 kgy 와 같은 것) | gabia 의 `~/rint-venv38` (3.8.20 · 같은 numpy · scipy · cupy) 은 쓰지 않고 손대지 않는다 (FAM 등록 `docs/reviews/fam_platen_prereg_20260812.md` 951 줄) · 두 기계 기본 `python3` = 3.13 (conda base · 11-17 현장) → venv 를 켜지 않고 사슬을 부르면 env_unit 대조에서 멈춘다 (틀린 결과 없음) · 저장본 열쇠에 venv 실경로가 든다 → R 동안 옮기지 않는다 |
| 킷 뿌리 `--root` | `~/sdcp` (`kit_SBE_vgcf100` · `kit_DBE_sdcp1um_vgcf100` · S0 단계 2 대조용 `kit_DBE`) | gabia 사본 = 11-11 복사 · 해시 같음 (시간 다시 어림 2 판 E-2 의 2) · 사슬이 R 직전 다시 해시해 S0 보고와 대조 |
| 계획 사본 | `~/sdcp/ca1_plan.json` | 봉인 커밋의 파일 바이트 그대로 |
| S0 보고 둘 | `~/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json` (11-16 · kgy 원본 · 자리 = 그 런 `run.log` 15 줄 · `meta.txt` `out=`) · `~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json` (아래 (2b) · kgy) | 사다리를 도는 기계에 필요 (gabia = kgy 원본을 바이트 그대로) · 리포 사본 (`docs/data/rint2_s0_sbe_20261116/`) 은 홈 경로를 가린 사본이라 입력으로 쓰지 않는다 |
| S0 계획 | `~/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json` | 봉인 커밋 안 (가림 없음 · sha256 `6346d9ed…`) |
| 저장본 | `~/ca1_cjstore` | **기계마다 새 빈 폴더** (1저자 11-17 봉인 후보 Q4) · 0755 · 실행 트리 · 원장 밖 · ⑥ 의 `~/p6_cjstore` · S0 시험 저장본 (`cjstore_s0probe_*`) 은 쓰지 않는다 |
| 원장 | `~/sdcp/ca1_ledger` (가진 기계) · `~/sdcp/ca1_ledger.parked` (세워 둔 쪽) | 한 번에 한 기계만 `ca1_ledger` 를 가진다 · 잠금 파일 = `~/sdcp/ca1_ledger/.git/rint_r_ledger.lock` (사슬과 같은 파일) |
| 넘김 묶음 | `~/sdcp/ca1_relay/<UTC 시각>_<보낸>_to_<받는>.bundle` | 지우지 않는다 (넘김 기록의 증거) |
| 사다리 바탕 | `~/sdcp/ca1_ladder_P0` (kgy) · `~/sdcp/ca1_ladder_P1` (gabia) | 1저자 11-17 봉인 후보 Q6 · 다른 기계 = 채택 시도 폴더를 같은 상대 자리로 바이트 그대로 · 판정 전 = 바탕 통째 |
| 단위 바탕 | `~/sdcp/ca1_units` (그 기계) · `~/sdcp/ca1_units_from_gabia` (kgy 가 받은 gabia 바탕 통째) | 재실행 = 원 시도가 돈 바탕에서만 |
| 넘침 점 바탕 | `~/sdcp/ca1_points` · `~/sdcp/ca1_points_from_gabia` | 넘침이 있을 때만 |
| 합친 예측 | `~/sdcp/ca1_predict` (첫 합치기 · 넘침 없으면 이것이 예측) · `~/sdcp/ca1_predict_x` (넘침 뒤 끝 합치기) | kgy (봉인 후보 Q6 · 이름 = 봉인 밖) · 판정 · 다시 판정이 끝날 때까지 지우지 않는다 |
| 판정 | `~/sdcp/ca1_verdict_main` | kgy |
| 로그 | `~/sdcp/ca1_logs/` | nohup 출력 (실행 트리 밖) |

### (2) 두 기계 준비 (R 전 · 봉인 직전 현장 확인과 같은 셸)

```sh
umask 022 && test "$(umask)" = 0022 && echo UMASK_OK
# 실행 트리 = 봉인 커밋 (Rint 고정 가지 위 문서 커밋 · stoic 아님) · 새 작업 트리 · 얕은 저장소 아님
#   <기존 트리> = 그 기계의 기존 리포 체크아웃 (kgy <HOME>/dem-s0-64e4d213e 꼴 · gabia <HOME>/dem-siteq-db86ce9b9 꼴 · 그 트리는 바꾸지 않는다 · 그 origin 이 봉인 가지를 받아야)
git -C <기존 트리> fetch -q origin claude/rint2-seal-20261118
git -C <기존 트리> worktree add --detach ~/dem-ca1 <봉인 커밋>
git -C ~/dem-ca1 rev-parse HEAD                                    # = <봉인 커밋>
git -C ~/dem-ca1 log --diff-filter=A --format=%H -- docs/reviews/rint2_seal_20261118/registration_R_sealed.md       # = 위와 같은 sha (봉인본을 넣은 커밋)
git -C ~/dem-ca1 rev-parse --is-shallow-repository                 # false
git -C ~/dem-ca1 status --porcelain --untracked-files=normal       # 빈 줄 (사슬과 같은 기준)
~/dem-venv/bin/python -c 'import sys,numpy,scipy,cupy;print(sys.version.split()[0],numpy.__version__,scipy.__version__,cupy.__version__)'   # 3.8.10 1.24.4 1.10.1 12.3.0 (두 기계 같은 한 줄 · 같은 답)
. ~/dem-venv/bin/activate && unset SIGMA_VGCF_OVERRIDE
command -v python3                                                 # = ~/dem-venv/bin/python3 (켠 뒤 · conda base 3.13 이 아니다)
# 계획 사본 · 봉인본 · 숫자 블록 대조
cp ~/dem-ca1/docs/data/rint2_r_plan_20261118/ca1_plan.json ~/sdcp/ca1_plan.json
sha256sum ~/sdcp/ca1_plan.json ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md                  # 첫 줄 = 봉인본 '| 계획 해시 |' 줄 끝 칸 · 둘째 = 봉인 기록의 봉인본 sha256
grep -n '^| 계획 해시 |\|^| S0 계획 해시 |' ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md | grep -o '`[0-9a-f]\{64\}`'   # 두 줄 (계획 · S0 계획)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage plan-doc --plan ~/sdcp/ca1_plan.json --check-doc --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md   # PLAN_DOC_SAME (rc 0)
# 저장본 폴더 (기계마다 하나 · 새 빈 폴더) · 글자 · 모드 · 소유자 = 사슬 규칙으로 확인
( umask 022 && mkdir ~/ca1_cjstore )
chmod go-w ~/ca1_cjstore && ls -ld ~/ca1_cjstore                    # drwxr-xr-x · 소유자 = 이 사용자
printf '%s\n' ~/ca1_cjstore | LC_ALL=C grep -n '[^A-Za-z0-9._/-]' && echo '허용 밖 글자 — 1저자 (자리를 바꾼다)'
python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); import rint_r_chain as R; print(R.cjunc_store_dir_problem(sys.argv[2]) or "STORE_DIR_OK")' ~/dem-ca1/scripts ~/ca1_cjstore
( umask 022 && mkdir -p ~/sdcp/ca1_relay ~/sdcp/ca1_logs )
command -v flock || echo 'flock 없음 — 이 기계의 넘김 = (5) 의 flock 없는 기계 규칙'   # 11-17 현장 = 두 기계 다 있음 (util-linux 2.34 · 2.39.3)
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader   # 적어 둔다 (R 동안 같아야 · 자동 갱신 멈춤)
```

- `--registration` 을 빼면 (기본 = 원본 자리 · 봉인 전 판) `plan-doc --check-doc` = rc 3 `PLAN_DOC_MISMATCH` (블록 없음) · 사다리 · 예측 · 판정 = 등록 해시 줄 ⬜ 에서 멈춤 (사슬 `registration_plan_hash` = `PLAN_HASH_UNREGISTERED`) — 틀린 결과는 없고 멈출 뿐이다 (봉인 기록 증거 ④) · 그래서 아래 모든 사슬 줄에 붙인다.
- gabia 만 더: 킷 두 벌 sha256 = kgy 와 같음 (2 판 E-2 의 2 · R 직전 사슬이 다시 대조) · S0 보고 둘을 kgy 원본 바이트 그대로 같은 상대 자리에 (`sha256sum` 두 기계 같음) · 실행 트리 = 기존 트리 (`<HOME>/dem-siteq-*`) 의 저장소에서 새로 뗀다 (`dem-mt` 없음 · 11-17 현장) · venv = `~/dem-venv` (kgy 와 같은 판 · `~/rint-venv38` 은 손대지 않음).
- 11-17 현장 (1저자 읽기만 · 두 기계): `flock` 있음 · 홈 경로 글자 = `[A-Za-z0-9._/-]` 안 · `git bundle create --all` 묶음에 HEAD 실림 (kgy git 2.25.1 · gabia 2.43.0) · 디스크 여유 kgy 240 GB (916 GB 중) · gabia 192 GB (422 GB 중) = 저장본 (SBE 파일 1,340,095,705 B · DBE 파일 크기 [미확인]) 에 충분 · venv 확인 줄 = 두 기계 `3.8.10 1.24.4 1.10.1 12.3.0` · gabia GPU = RTX A6000 49 GB (드라이버 595.58.03 · R 동안 같아야).

### (2b) S0 단계 2 — kgy · 한 번 · 사다리 전 (봉인 계획의 결과 전 등록 넷이 채워져 있어야 관문이 연다 · DBE 분포를 여기서 처음 연다 · 보고 = 사다리 `--s0-stage2-report`)

```sh
cd ~/dem-ca1 && umask 022
# venv (S0 보고의 python · numpy · scipy 판 = 이 셸 · 사슬은 S0 보고의 판 글자를 대조하지 않는다 → 여기서 눈으로 · 다르면 멈추고 1저자)
. ~/dem-venv/bin/activate && python3 -c 'import sys,numpy,scipy;print(sys.version.split()[0],numpy.__version__,scipy.__version__)'   # 3.8.10 1.24.4 1.10.1
# census · registry 일곱 파일 = S0 단계 1 보고의 판 (같으면 SAME_VERSION_OK 뒤 단계 2 · 다르면 && 에서 멈춘다 · §2-3 손 확인과 같은 줄)
#   끝 rc 줄 (bash PIPESTATUS) = 단계 2 의 rc (SAME_VERSION_OK 가 없으면 = git diff 의 rc · 단계 2 를 돌리지 않았다)
H1=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['code']['git_head'])" docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json)
git diff --quiet "$H1" HEAD -- scripts/ca_s0_census.py scripts/carbon_junction.py scripts/ptfe_face_alpha.py scripts/step3_sigma.py \
    scripts/mpm_webapp_payload.py scripts/fibre_segment_raster.py scripts/sr01_stamp_compare.py && echo SAME_VERSION_OK && \
  python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 2 --threshold-commit <봉인 커밋> \
    --plan-path docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --r-plan-path docs/data/rint2_r_plan_20261118/ca1_plan.json --r-doc docs/reviews/rint2_seal_20261118/registration_R_sealed.md \
    --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe 2>&1 | tee ~/sdcp/ca1_logs/s0_stage2.log; echo "rc=${PIPESTATUS[0]}"
```

- 관문이 보는 것 (`ca_s0_census.verify_plan_commit` · 아니면 거부): 인자 커밋 = HEAD 의 조상 (같은 커밋 포함) · 그 커밋 `docs/reviews/rint2_seal_20261118/registration_R_sealed.md` 의 `| S0 계획 해시 |` 끝 칸 = S0 계획 sha256 · `| 계획 해시 |` 끝 칸 = R 계획 sha256 · R 계획 꼴 · 결과 전 등록 넷 · 실행 정책 값 넷 (null = 거부) · tol_ff · len_law 두 계획 대조.  보내 주세요: 화면 요약 · 보고 JSON 둘 (→ `docs/data/rint2_s0_dbe_<날짜>/`).

### (3) 원장 시작 — kgy · 한 번

```sh
cd ~/sdcp && umask 022
mkdir -p ~/sdcp/ca1_ledger && git -C ~/sdcp/ca1_ledger init -q
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --init --plan ~/sdcp/ca1_plan.json --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md
git -C ~/sdcp/ca1_ledger symbolic-ref --short HEAD                 # 원장 가지 → 아래 넘김 기록 머리에 한 번 적는다
```

### (4) 시도 하나 — 항목 → 띄움 → 시작 확인 (사다리 · 단위 · 넘침 점 모두 같은 꼴 · 원장이 그 기계에 있을 때만)

```sh
# 사다리 P0 (kgy) — 먼저 같은 인자 + --dry-run (--ledger · --attempt 없이 · 런 env 만 · 원장 · 폴더 무변경) → 항목 (화면 ATTEMPT_ADDED n=<n>) → 그 번호로 곧바로 본 시도
#   (항목만 두고 띄우지 않으면 안 된다 — 같은 대상의 다음 항목은 앞 항목의 결과 줄 뒤에만 · 폴더 없는 원장 시도 = 결과 뒤 · Q9 설계 §3-5 128 · 134 줄)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md \
    --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours 168 --machine kgy --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_ladder_P0 --dry-run
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target ladder:P0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md
cd ~/sdcp && nohup python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 \
    --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --plan ~/sdcp/ca1_plan.json --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md \
    --s0-plan ~/dem-ca1/docs/data/rint2_s0_sbe_20261116/files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json \
    --s0-stage2-report ~/sdcp/ca1_s0_dbe/s0_stage2_kit_DBE_sdcp1um_vgcf100.json \
    --s0-stage1-report ~/sdcp/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json \
    --max-hours 168 --machine kgy --ledger ~/sdcp/ca1_ledger --attempt <n> \
    --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_ladder_P0 > ~/sdcp/ca1_logs/ladder_P0_a<n>.log 2>&1 &
# 사다리 P1 (gabia) = 위 세 줄에서 ladder:P1 · --law P1 · --machine gabia · --out ~/sdcp/ca1_ladder_P1 · 로그 이름만 다르다

# 단위 (그 기계 · 이름 = 아래 (6) 표) — 두 사다리 채택 시도 폴더가 이 기계에 있어야 한다
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target unit:P0_c0_R_j0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md
cd ~/sdcp && nohup python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md --ledger ~/sdcp/ca1_ledger --attempt <n> --unit P0_c0_R_j0 \
    --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_units > ~/sdcp/ca1_logs/unit_P0_c0_R_j0_a<n>.log 2>&1 &
# gabia 단위 = 같은 두 줄 · --machine gabia · unit:<이름> · --unit <이름> (예 P1_c1_R_j_hi)

# 시작 확인 — 둘 다 참이면 그 사슬은 끝날 때까지 원장을 건드리지 않는다 → 원장을 넘겨도 된다
python3 -c 'import json, subprocess, sys; L = subprocess.run(["git", "-C", sys.argv[1], "show", "HEAD:rint_r_attempts.jsonl"], capture_output=True, text=True, check=True).stdout.splitlines(); x = json.loads(L[-1]); print(x.get("kind"), x.get("n"))' ~/sdcp/ca1_ledger   # start <n>
ls ~/sdcp/ca1_units/attempt_<n>/groups/ | grep -c 'launch.json$'   # 1 이상 (사다리면 ~/sdcp/ca1_ladder_<법칙>/attempt_<n>/groups/)
```

### (5) 원장 넘김 — 보낸 쪽 · 받는 쪽 (수단 = 1저자 · 묶음 파일만 옮긴다)

```sh
# 보낸 쪽 — (4) 의 시작 확인 뒤 (또는 그 기계에서 도는 사슬이 없을 때) · 원장 잠금 (사슬과 같은 잠금 파일 · 1저자 11-17 봉인 후보 Q5) 아래에서 묶고 세워 둔다
cd ~/sdcp && umask 022
T=$(date -u +%Y%m%dT%H%M%SZ); FROM=kgy; TO=gabia; B=~/sdcp/ca1_relay/${T}_${FROM}_to_${TO}.bundle
flock -x -w 120 ca1_ledger/.git/rint_r_ledger.lock -c "git -C ca1_ledger bundle create \"$B\" --all && mv ca1_ledger ca1_ledger.parked"
git -C ca1_ledger.parked rev-parse HEAD; sha256sum "$B"; echo "$T"      # 넘김 기록 한 줄 (시각 · 원장 끝 커밋 · 묶음 sha256)
test ! -e ca1_ledger && echo PARKED_OK
# 받는 쪽 — 묶음을 ~/sdcp/ca1_relay/ 에 같은 이름으로 둔 뒤 (T · FROM · TO · 가지 = 넘김 기록)
cd ~/sdcp && umask 022
T=<넘김 기록 시각>; FROM=kgy; TO=gabia; BR=<원장 가지>; RB=~/sdcp/ca1_relay/${T}_${FROM}_to_${TO}.bundle
sha256sum "$RB"                                                     # = 넘김 기록
git bundle list-heads "$RB" | grep "refs/heads/$BR"                 # 커밋 = 넘김 기록의 원장 끝 커밋
# 세워 둔 사본이 있으면 그 자리에서 먼저 받고 (그동안 이 기계 사슬은 원장 자리 ca1_ledger 를 못 연다 = 창 없음) 받은 뒤에만 되살린다 ·
#   -c pull.rebase=false = 사용자 설정을 이 줄에서만 끈다 ([추정] 옛 git 에서 rebase 설정이 --ff-only 보다 앞설 수 있다)
if [ -d ca1_ledger.parked ]; then git -C ca1_ledger.parked -c pull.rebase=false pull -q --ff-only "$RB" "$BR" && mv ca1_ledger.parked ca1_ledger; else git clone -q -b "$BR" "$RB" ca1_ledger; fi
test "$(git -C ca1_ledger rev-parse HEAD)" = <넘김 기록의 원장 끝 커밋> && echo RECV_OK   # RECV_OK 가 없으면 멈추고 1저자 (사슬을 띄우지 않는다)
```

- (11-17 현장 = 두 기계 다 `flock` 있음 → 아래 줄은 한정으로만 남긴다) **`flock` 이 없는 기계** ((2) 의 확인 줄) = 위 보낸 쪽 셋째 줄을 `git -C ca1_ledger bundle create "$B" --all && mv ca1_ledger ca1_ledger.parked` 로 (잠금 없이) 쓰되, **그 기계의 사슬이 (4) 의 시작 확인 뒤 도는 중일 때만 넘긴다** (1저자 11-17 봉인 후보 Q5 · 그 밖의 때 = 그 기계의 사슬이 시작 기록 · 결과 줄을 쓸 수 있는 때).
- 잠금 파일 = 사슬과 같은 파일 (`rint_r_chain.LEDGER_LOCK_FILE` · 원장 저장소 `.git` 안 · 대기 상한 120 s = 사슬 `LEDGER_LOCK_WAIT_S` 와 같은 값) — 같은 호스트에서 사슬의 덧붙임과 묶기 · 이름 바꾸기가 겹치지 않는다 · 세워 둔 뒤 그 기계에서 끝나는 사슬은 잠금 파일을 못 열어 rc 3 (아래 (6) 정상 끝).

**넘김 기록** (넘길 때마다 한 줄 · 원장 가지 = `<원장 가지>` (`--init` 뒤 한 번))

| 시각 (UTC · 묶음 이름) | 보낸 기계 | 받는 기계 | 원장 끝 커밋 | 묶음 sha256 | 잠금 (flock · 없음 = 시작 확인 뒤 도는 중) | 누가 |
|---|---|---|---|---|---|---|
| (빈칸 — R 때) | | | | | | |

### (6) (가-2) 정상 흐름 — 차례 · 각 단계에서 원장이 어디 있어야 하나

| # | 기계 | 그 일 전 원장 자리 | 할 일 | 정상 끝 |
|---|---|---|---|---|
| 0 | kgy | — | (2b) S0 단계 2 | rc 0 · 보고 JSON 둘 |
| 1 | kgy | kgy (시작) | (3) 원장 시작 | rc 0 · 원장 머리 = 계획 sha256 |
| 2 | kgy | kgy | (4) `ladder:P0` 항목 → 사다리 P0 → 시작 확인 | 시작 기록 · 러너 그룹 |
| 3 | kgy → gabia | kgy | (5) 넘김 | gabia 가 원장을 가진다 · kgy = 세워 둠 |
| 4 | gabia | gabia | (4) `ladder:P1` 항목 → 사다리 P1 → 시작 확인 | 시작 기록 · 러너 그룹 |
| 5 | (두 사다리 도는 중) | gabia | 먼저 끝난 기계가 원장을 받는다 — 원장이 없는 동안 끝난 사슬 = 아래 rc 3 (정상) | — |
| 6 | 끝난 기계 | 그 기계 | `--stage recover --out <그 시도 폴더> --ledger ~/sdcp/ca1_ledger --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md` | rc 0 · 결과 줄 (by recover) |
| 7 | 두 기계 | — | 사다리 채택 시도 폴더를 서로 옮김 (P0 → gabia · P1 → kgy · 같은 상대 자리 · 바이트 그대로 · `sha256sum` 이나 폴더 요약을 맞춘다) | 두 기계에 두 사다리 채택 폴더 |
| 8 | 단위 시작마다 그 기계 | 그 기계 | (4) `unit:<이름>` 항목 → 단위 → 시작 확인 → 다른 기계가 기다리면 (5) 넘김 | 단위가 끝날 때 원장이 그 기계에 있으면 사슬이 결과 줄 (rc 0) · 없으면 rc 3 → 원장이 돌아온 뒤 6 번 |
| 9 | 원장을 받는 차례 | — | 단위가 끝난 기계 (recover + 다음 단위) 가 먼저 · 도는 중인 기계는 원장이 없어도 된다 · 같은 기계에서 사슬 둘을 띄우지 않는다 | — |
| 10 | gabia → kgy | — | 단위 12 의 결과 줄이 다 있으면 gabia `~/sdcp/ca1_units` 바탕 통째 → kgy `~/sdcp/ca1_units_from_gabia` · 원장 → kgy · 사다리 P1 바탕 통째 → kgy | kgy 에 원장 · 모든 시도 폴더 |
| 11 | kgy | kgy | (7) 첫 합치기 | rc 0 = 예측 (PREDICTED · NOT_COMPUTED · STOPPED = 그 결과) · rc 4 = 넘침 (`expansion.json`) |
| 12 | (rc 4) 점마다 그 기계 | 그 기계 | 넘침 점 배정 안전 규칙 (아래) → `point:<이름>` 항목 → 점 시도 (gabia 면 `expansion.json` 을 바이트 그대로) → 다 끝나면 gabia `ca1_points` 통째 → kgy `ca1_points_from_gabia` → 끝 합치기 | rc 0 |
| 13 | kgy | kgy | (7) 주 판정 · 다시 판정 | 판정 rc 0 · `REVERIFY_SAME` |

- **rc 3 = 정상 끝** 은 셋이 다 맞을 때만 — ① 화면 끝 줄 `멈춤 [ATTEMPT_LEDGER_MISMATCH] … 원장 잠금 파일을 못 연다 (…)` ② 그 시각 그 기계에 `~/sdcp/ca1_ledger` 가 없다 (세워 둠 · `ca1_ledger.parked` 만) ③ 그 시도 폴더에 단계 요약 (`ladder_summary.json` · `unit_summary.json` · `point_summary.json`) 이 있다.  하나라도 아니면 진짜 멈춤 — 요약 · 로그의 멈춤 이름을 1저자에게 · 그 대상의 다음 시도를 띄우지 않는다.
- recover 는 그 시도가 돈 기계 · 그 바탕 · 같은 부팅에서 (옮긴 폴더에서 = rc 3 · 원장 무변경) · 사슬이 아직 살아 있으면 recover 는 아무것도 하지 않는다 (rc 3 · 끝난 뒤 다시) · 다른 부팅이면 그 그룹이 끝났음을 확인한 뒤 `--operator-confirm <시도 번호> --operator-why "<확인한 것 · 한 줄>"` (§3 끝 줄 · 등록 R §10-5 아 ④).
- 단위 ↔ 기계 **첫 배정** (봉인 밖 · 1저자 11-17 봉인 후보 Q6 · 3 판 Q7 · gabia 첫 사다리 팔 실측으로 고칠 수 있다 · 배정을 바꿔도 원장 · 폴더 · 규칙이 시도를 정한다):

| 기계 | 단위 (이 차례로) |
|---|---|
| kgy (7) | `P0_c0_R_j0` · `P0_c0_R_j_lo` · `P0_c0_R_j_hi` · `P0_c1_R_j0` · `P0_c1_R_j_lo` · `P0_c1_R_j_hi` · `P1_c0_R_j0` |
| gabia (5) | `P1_c0_R_j_lo` · `P1_c0_R_j_hi` · `P1_c1_R_j0` · `P1_c1_R_j_lo` · `P1_c1_R_j_hi` |

- **넘침 점 배정 안전 규칙** (3 판 Q11 · 운영 규칙 · 기준 값 2/3 은 바꿀 수 있다): 점을 주기 전에 그 기계의 첫 DBE 모서리 팔 실측 비로 그 기계의 첫 점 (8 팔 · 짓기 5) 시간을 다시 어림해 **112 h (= 168 h 의 2/3)** 를 넘으면 그 기계에 주지 않는다 · 둘 다 넘으면 멈추고 1저자 · 점은 kgy 먼저.
  - **어림 꼴 = 시간 다시 어림 3 판 §3-3 (4) 의 "팔 전체" 꼴** (1저자 11-17 봉인 후보 Q7 · 보수 쪽): 첫 점 ≈ r × (8 × T_hit + 5 × (T_first − T_hit)) · r = T_DBE ÷ T_first · T_DBE = 그 기계 첫 단위의 모서리 런 · T_first = 그 기계 사다리에서 저장본을 지은 첫 보통 점 런 · T_hit = 그 사다리의 적중 런 · 시간 = 런 기록 `seconds` (아래 줄 · 이름 · 역할 · 시간만 · σ 를 열지 않는다).  확인: 3 판 값 (kgy T_hit 4,932 · T_first 9,067 · gabia 6,682 · 10,817 s · r 2.933) 을 넣으면 kgy 49.0 h · gabia 60.4 h (3 판 §3-3 (4) 와 같음).
  - 모서리 런에 SV 반사실 풀이가 들면 (`sv_cf_scope`) r 이 커진다 = 보수 쪽.

```sh
python3 -c 'import json, sys; s = json.load(open(sys.argv[1])); [print(r.get("name"), r.get("role"), r.get("arms"), r.get("seconds")) for r in s.get("runs") or []]' ~/sdcp/ca1_units/attempt_<n>/unit_summary.json
python3 -c 'import json, sys; s = json.load(open(sys.argv[1])); [print(r.get("name"), r.get("role"), r.get("arms"), r.get("seconds")) for r in s.get("runs") or []]' ~/sdcp/ca1_ladder_P0/attempt_<n>/ladder_summary.json
python3 -c 'import sys; th, tf, td = map(float, sys.argv[1:4]); r = td / tf; print(round(r, 3), round(r * (8 * th + 5 * (tf - th)) / 3600, 1), "h (112 h 넘으면 그 기계에 주지 않는다)")' <T_hit> <T_first> <T_DBE>
```

### (7) 합치기 · 넘침 점 · 판정 — kgy (넘침 점 시도만 배정된 기계)

```sh
cd ~/sdcp && umask 022
# 첫 합치기 (rc 0 = 예측 · rc 4 = 넘침 · 그 밖 = 멈춤 이름을 1저자에게)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md --ledger ~/sdcp/ca1_ledger --merge ~/sdcp/ca1_units ~/sdcp/ca1_units_from_gabia --out ~/sdcp/ca1_predict
python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["points"])' ~/sdcp/ca1_predict/expansion.json   # rc 4 일 때만 · 넘침 점 이름
# 넘침 점 (점마다 · 그 기계) — 항목 → 시도
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ledger --ledger ~/sdcp/ca1_ledger --add --ledger-target point:P0_c0_R_j0 --machine kgy \
    --plan ~/sdcp/ca1_plan.json --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md
cd ~/sdcp && nohup python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md --ledger ~/sdcp/ca1_ledger --attempt <n> --point P0_c0_R_j0 \
    --expand ~/sdcp/ca1_predict/expansion.json --cjunc-store ~/ca1_cjstore --out ~/sdcp/ca1_points > ~/sdcp/ca1_logs/point_P0_c0_R_j0_a<n>.log 2>&1 &
# 끝 합치기 (넘침 점이 다 끝난 뒤 · gabia 점 바탕 통째를 받은 뒤 · 없으면 그 자리를 뺀다)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict \
    --ladders ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> \
    --kit kit_DBE_sdcp1um_vgcf100 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours 168 --machine kgy \
    --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md --ledger ~/sdcp/ca1_ledger \
    --merge ~/sdcp/ca1_units ~/sdcp/ca1_units_from_gabia ~/sdcp/ca1_points ~/sdcp/ca1_points_from_gabia \
    --expand ~/sdcp/ca1_predict/expansion.json --out ~/sdcp/ca1_predict_x
# 주 판정 (값 열람 = 주 판정 런이 다 끝난 뒤 한 번 · --show-results 를 이 줄에) · 다시 판정 (읽기 전용 바이트 대조 · 판정 JSON 에 적힌 등록 경로를 다시 읽는다)
#   --runs 의 셋째 = 넘침 없음 ~/sdcp/ca1_predict · 넘침 ~/sdcp/ca1_predict_x
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --runs ~/sdcp/ca1_ladder_P0/attempt_<P0 채택 번호> \
    ~/sdcp/ca1_ladder_P1/attempt_<P1 채택 번호> ~/sdcp/ca1_predict --root ~/sdcp --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md \
    --ledger ~/sdcp/ca1_ledger --out ~/sdcp/ca1_verdict_main
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict_main --root ~/sdcp --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md
# 원장이 없는 동안 끝난 시도 → 원장이 돌아온 뒤 (그 기계 · 그 바탕)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage recover --out ~/sdcp/ca1_units/attempt_<n> --ledger ~/sdcp/ca1_ledger --registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md
```

### (8) R 동안 운영 규칙 (정본 = 봉인본 §10-8 · 규칙 · 기계적 보장 아님 표지 그대로)

1. 실행 트리 · 봉인본 (원본 자리 포함) · 계획 사본 · 저장본 폴더 · venv = R (사다리 시작부터 다시 판정까지) 동안 바꾸지 않는다 — `git -C ~/dem-ca1 rev-parse HEAD` = `<봉인 커밋>` · `status --porcelain --untracked-files=normal` 빈 줄을 시도마다 본다.
2. 두 기계 GPU 드라이버 · CUDA 자동 갱신 멈춤 (재실행 자격 = 원 시도 환경 지문 모든 칸) · (2) 의 `nvidia-smi` 줄 값이 R 동안 같아야 한다 (방법 = 1저자 · 기계마다).
3. GPU 비움 — 두 기계 GPU 에 다른 계산 없음 (kgy = 1저자 DFT 얼림) · 같은 기계에서 사슬 둘을 동시에 띄우지 않는다.
4. 저장본 폴더 = 손대지 않음 (못 읽는 파일 `unreadable_rebuilt` = 기록 · 시간만 는다 · R 뒤 정리 · 어긋남 = 멈춤 → 1저자).
5. 재실행 = 원 시도가 돈 그 `--out` 바탕에서만 (틀린 바탕에서 시도하지 않는다 — 한 번 거부되면 원 바탕의 재실행도 거부된다) · 멈춘 GPU 런은 `--resume` 하지 않고 새 시도.
6. 원장 밖 킷 풀이 없음 · 원장 · 시도 폴더 · 넘김 묶음을 손으로 고치거나 지우지 않는다.
7. 띄우기 = `cd ~/sdcp && nohup … > ~/sdcp/ca1_logs/<이름>.log 2>&1 &` (실행 트리 밖 · `nohup.out` 을 실행 트리에 만들지 않는다).
8. 최대 시도 수 8 (같은 대상 · 풀기 전 거부 · 재실행 포함) — 넘으면 `ATTEMPT_LIMIT` · 그 대상 = 1저자.
9. `--add` 로 받은 번호 = 곧바로 그 번호의 시도를 띄운다 (항목만 두고 같은 대상 항목을 더하지 않는다 · 사다리는 dry-run 을 `--add` 앞에) — 폴더 없는 원장 시도 = 결과 뒤 (Q9 설계 §3-5 134 줄).
10. 사슬 명령에서 `--registration ~/dem-ca1/docs/reviews/rint2_seal_20261118/registration_R_sealed.md` 을 빼지 않는다 (빼면 원본 자리 = 봉인 전 판 → 해시 줄 ⬜ → 멈춤 · 틀린 결과는 없다).

## 4. 미리 보이는 쟁점 (S0 단계 1 숫자 **전에** 1저자 · Codex 가 볼 것)

① **접촉 길이 L_c 의 정의가 없다 + J8 관문** — 계약 (v2 §3-8 J8 · v3 §5 J11) · 설계 §4-1 · 등록 R §2-1 은 L_par = 2(r_fi + r_fj) = 0.30 µm 만 고정하고 L_c 를 정의하지 않는다.
S0 는 두 판을 같이 낸다 — touch (d ≤ r_fi + r_fj 인 중심선 길이) · band (d ≤ 검출 문턱 r_fi + r_fj + tol_ff 인 길이) · 긴 접촉 수 = 판마다.  손계산: 수직 관통 교차의
touch = 정확히 2 (r_fi + r_fj) = 0.30 µm (= L_par · 경계) [우리 산술] · 수직 스침의 band = 2√(0.225² − 0.15²) = 0.335 µm (긴 접촉) [우리 산술 · 시험 C2 · 같은 꼴 C3].
[합성 · 실침대 아님 · 인용 불가] 실침대 VGCF 길이 밀도 (48,189 × 10 µm / (50 × 50 × 72.5 µm³) ≈ 2.66 µm/µm³) 의 등방 무작위 섬유 (관통 허용 = MPM 과 같은 조건 · 침대의
1/10 크기) 에서 VV instance 15,353 중 L_c > 0.30 µm = touch 27.6 % · band 79.8 % ⇒ 실침대 (정렬 `--fibre-align 0.606` · 굽힘) 에서도 어느 판이든
**긴 접촉 ≥ 1 은 거의 확실** (추정) ⇒ 등록 R §11 ④ (*"1 이상이면 여기서 멈춘다"*) 가 정량 R 을 S0 에서 멈출 공산이 크다.
→ ⬜ 1저자 (+ Codex): L_c 정의 (권고 = touch 판 — 표면 겹침 길이 · 검출 문턱의 위치 불확도 tol_ff 를 길이에 넣지 않는다) · J8 처리 (N10 개정 경로 — 길이 법칙 등록,
또는 긴 접촉을 길이 L_par 단위의 instance 로 나누는 규칙 등 · 둘 다 결과 전) 를 S0 단계 1 숫자 전에.
→ ✅ **10-20 밤 1저자 Q17 = 권고대로** — 길이 비례 접합 G_j = max(1, L_c/L_par)/R_j,0 (J8 정량 거부 대체 · 새 손잡이 없음) · L_c = touch 판 · 꺾임 자기 접합 = 경로 호 길이 s < s_min 이면 접합 아님 ·
  s_min = 필수 · 기본값 없음 · 단계 1 (새 침대) 뒤 §2-1 개정 · 구현 시험 먼저 `80a9a4ab1` → `c5a3473d3` · S0 가 같은 함수로 센다 (2 일 차 `2e2b08c09`).

② **재하율** — §1-5 (기하 규칙 플래튼 · V/c_P 0.27 → ≈ 0.41) · 1저자 (가) / (나).  → ✅ **10-20 밤 1저자 Q18 = (가)** VGCF E 만 · 이름 *"E + dt + 재하율 세대 전환"*.

③ **미리보기 정의** (보고의 `notes`) — 포트 (그 fid 경로 셀 중 sid 3 · 최근접점 ↔ 셀 중심 유클리드 ≤ r_port · 동률 = 경로 열 번호 작은 셀) · 자기 접촉 (선분 번호 차 ≥ 2 ·
호 길이 차 > (π/2)·thr) · VA 문턱 tol_fs = 0 (계획에 숫자 없음 · J2b 판정문 예시 경계 = r_f + R_AM) — 판정 · 보고의 instance census = B3 `cjunc_registry` (같은 함수 · 사본 금지) 가
정의를 확정하면 그 판으로 다시 센다 (설계 §2 ① · §4-1).

④ **α 분포** (설계 §2 ① 마지막 행) — S1 `face_alpha` 함수가 생긴 뒤 같은 함수 호출로 (지금 보고 = `not_available`).

⑤ **S0 의 raster 코드 판** — S0 는 자기 작업 트리 (`~/dem-ca1`) 의 payload · `rasterize` 로 침대를 다시 굽는다 (침대를 만든 `298a73197` 과 다를 수 있다 · 보고 `code` 칸에 파일 sha256).
같은 판 안에서 S0 의 생산 격자 = payload 자신의 `--step3-rasterize-only` 원장 (시험 E5 · 셀 수 같음).  (10-21 · 개정 2 · 사전 리뷰 PRE-design-14) 단계 1 · 단계 2 · R 런의 census · registry 는 **같은 판**이어야 s_min (단계 1 의 정의로 고른 값) 의 뜻이 그대로다 → 단계 2 = §2-1 개정 커밋 자체 + 단계 1 보고 `code.git_head` 와 일곱 파일 같음 (§2-3 손 확인 · 등록 R §2-1b).

⑥ **(10-21) Codex 설계 리뷰 판정 = S2 · 등록 R 판정 HOLD** (`docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md` §0) — 지금 할 수 있는 것 = 재압밀 (§1 · Q13 (가) 판 · 수정 계획 §3) · S0 단계 1 (새 SBE 기하 · 조건부 GO · σ 결과로 선택하지 않음) / 조건이 서면 = S0 단계 2 (조건부 GO — 문턱 · s_min 선택 절차를 DBE 열람 전 개정 · 봉인 + 재방문 · 긴 접촉 · 덮임 census 를 보탠 뒤) / 기다리는 것 = 사슬 · σ 를 여는 런 (수정 묶음: S2 branch · 포트 · 분산판 · SV 반사실 · 목표량 증서 ⓓ · 상태 분리 · 사슬 3판 규칙 → Codex 재검토 GO · 등록 비준 뒤) · u = 원래 MPM 경로 표본화 그대로 (재표본화 없음 · 등록 R §2-1) · s_min = SBE 개발 단계 (등록 R §2-1b).

## 5. 기록 (빈칸 · 결과 0 건)

- (봉인 · 20261118) R 의 원장 넘김 기록 = §3-1b (5) 의 표 (넘길 때마다 한 줄 · 이 문서 · 3 판 Q9) · 시도 결과 = 원장 (`~/sdcp/ca1_ledger`) 이 정본 (이 문서에 옮겨 적지 않는다) · 등록 = 봉인본 `docs/reviews/rint2_seal_20261118/registration_R_sealed.md`.

- ⬜ ① 재압밀 — SBE · DBE 런 폴더 · 시작 · 끝 시각 · §1-4 출력 · §1-5 선택 (가 / 나)
- ⬜ ② S0 단계 1 — 요약 · 계획 sha256 → 등록 R §2-1 개정 커밋 sha
- ⬜ ③ S0 단계 2 — 요약
- ⬜ §4 ① L_c · J8 결정
- ✅ (10-21) 1저자 Q13 (가) = 새 킷 payload 줄에서 `--joule-heat` · `--save-step4-grid` 뺀다 (§1-1) · ✅ §1-5 = (가) (10-20 밤 Q18 · §4 ②) · ✅ §4 ① = Q17 (10-20 밤)
- ⬜ (10-21) ① 재압밀의 §1-1 확인 출력 (diff `^[<>]` 4 · grep 0) · §1-4b 출력 (CFL 제한 상 · 종료 이유 · substep · 코드 시간 · 재시도 · 실행 코드 지문)
- ⬜ (10-21) ② 단계 1 의 새 census 블록 · s_min 개발 단계 기록 · 해시 두 줄 (S0 계획 · R 런 계획) → 등록 R §2-1 개정
- ⬜ (10-21 · 개정 2 · Q-G) 세 숫자 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱) 등록 R 개정 커밋 — Codex 회신 뒤 · 단계 2 전
- ⬜ (10-22 · PRE2-design-01 · Q2) ②b ⑥ 숫자 탐침 (단계 2 앞 · 반복 수 · 시간) → 개정 커밋 하나 (숫자 + S0 계획 해시 + R 런 계획 해시 (maxiter 포함) + s_min) → 단계 2 보고 경로 (사다리 `--s0-stage2-report`)
- ⬜ (10-22 · PF2 D · PRE2-design-02 · 08) 단계 1 보고 경로 (사다리 `--s0-stage1-report`) · R 런 핀 = 단계 1 판 (census · registry 일곱 파일 · 사슬이 대조 · 다르면 `CODE_PIN_MISMATCH`) · 단계마다 깨끗한 트리 · ~~(기계를 더 쓰면)~~ `--machine` 이름표 (10-28 = 늘 필수 · 개정 4)
- ⬜ (10-21 · 개정 2) ③ 단계 2 의 손 확인 출력 (`same-version rc=` · 해시 두 줄 grep · `git status --porcelain`)
- ⬜ (10-21 · 개정 2 · Q-F) ④ 주 판정 (`ca1_verdict_main` · 열람 시각) → 감도 → 전체 판정 (`ca1_verdict`)
