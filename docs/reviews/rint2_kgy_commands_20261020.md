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

## 0. 순서 한눈에

| # | 무엇 | 기계 | 시간 (어림) | 끝나면 |
|---|---|---|---|---|
| ① | 재압밀 SBE → DBE (차례로 · 한 GPU) · (10-21) 새 킷 = payload 두 토큰 뺀 판 (§1-1 · Q13 (가)) | kgy GPU | 침대당 ≈ 1.5–2 h · 둘 ≈ 3–4 h (§1-3) | §1-4 · §1-4b (10-21) 검사 출력 보내기 |
| ②′ | (선택 · 지금 가능 · ①과 무관) S0 **도구 시험** — 현 세대 `kit_SBE` (옛 VGCF 10 GPa 침대) | kgy CPU | ≈ 15–30 분 (§2-1b) | 화면 요약 보내기 — **s_min · 문턱 결정에 쓰지 않는다** |
| ② | S0 단계 1 — SBE 새 침대 | kgy CPU | 침대당 ≈ 15–30 분 (§2-2) | 보고 · 계획 보내기 → 등록 R §2-1 개정 커밋 |
| ③ | S0 단계 2 — DBE 새 침대 (+ 옛 `kit_DBE`) · (10-21 · Q-G) **그 전에** 세 숫자 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱) = 1저자 · Codex 회신 뒤 · 등록 R 개정 커밋 (§2-2 끝) | kgy CPU | 침대당 ≈ 15–30 분 | 보고 보내기 |
| ④ | 런 사슬 | — | — | ⛔ **발사 금지** (§3 · 등록 R §11 관문 뒤) · (10-21 · Q-F) 순서 = **주 판정 먼저** (SBE 보정 + 끝 origin + DBE 네 모서리 × 세 R + origin · 78 팔 ≈ 56 h · 부담 ×1.7–2 = 95–112 h [우리 산술 · 등록 R §10-4]) → 10-31 판정 = 주 판정만 (한정어 *"감도 미완료"*) → 감도 (264 팔 ≈ 231 h · ×1.7–2 = 392–462 h) · GPU 추가 = 1저자 |

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

```bash
python3 - <<'PY'
import hashlib, json, os
import numpy as np
H = os.path.expanduser('~/sdcp')

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()[:16]

for old, new in (('kit_SBE', 'kit_SBE_vgcf100'), ('kit_DBE_sdcp1um', 'kit_DBE_sdcp1um_vgcf100')):
    ro, rn = (os.path.realpath(os.path.join(H, k, 'latest_run')) for k in (old, new))
    print(f'── {new}  (기준 {old})\n   런 {os.path.basename(rn)} · 완료 마커 {os.path.exists(os.path.join(rn, "mpm_done.marker"))}')
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
    # ③ 재시도 · 선별 이력 — 킷의 run_* 전부 (지우지 않는다)
    runs = sorted(glob.glob(os.path.join(K, 'run_*')))
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
  - (10-21 · Codex RCA-11 · 1저자 Q8 권고대로) 그 개정 커밋에 함께: **s_min 개발 단계** (s_min 은 "확인만" 이 아니다 — 위 s 분포를 보고 고르되 선택 규칙 · 후보 · 실패 처리 · 본 자료를 적고 DBE 열람 (단계 2) 전 재봉인 · 등록 R §2-1b) · **해시 두 줄** — S0 계획 (`cjunc_plan.json` · `ca-cjunc-plan-v1`) sha256 = 등록 R §2-1 `| S0 계획 해시 |` 줄 (단계 2 도구가 그 커밋의 등록 문서에서 이 값을 찾는다) · R 런 계획 (`rint-r-plan-v1` · 사슬 `--plan` · §3) 파일 · sha256 = `| 계획 해시 |` 줄 (사슬이 이 줄을 읽는다) · 두 계획의 `tol_ff` · `s_min` 대조 (등록 R §2-1 · 도구 ⬜).
  - **(10-21 · 사전 리뷰 PRE-design-03 · 1저자 Q-G 권고대로) 단계 2 전에 세 숫자** — 점 수 상한 (등록 R §3-2) · 역상 폭 상한 (§3-2b ④) · SV 반사실 문턱 (§5-6 · + 범위 · 세 R 여부 · 모서리 묶는 법) = 1저자가 **Codex 재검토 회신 뒤** 정해 등록 R 개정 (결과 0 건) 으로 — 위 §2-1 개정 커밋에 함께 또는 그 앞 커밋 · 어느 쪽이든 **단계 2 에 넘기는 개정 커밋에 세 숫자가 있어야 한다** (단계 2 가 DBE 의 SV 우회 후보 수를 처음 연다 · 등록 R §11 ④) · 지금 도구는 이 셋을 확인하지 않는다 → §2-3 의 손 확인.
- 도구가 하는 것 (요약 · 정본 = 도구 머리 주석): payload 를 이 프로세스에서 돌려 생산 `rasterize` 입력을 잡고 (솔브 0 · 킷 폴더 쓰기 0 — 바뀌면 거부) 생산 · off (PTFE 행 뺌 =
  face_alpha 의 sid 격자) · SDCP 없는 판을 다시 굽는다 · 섬유 경로 셀 = 생산 `_fibre_segment_ijk` · 단계 1 은 SDCP 점이 하나라도 있으면 거부.
- 시간 · 자원 (어림): payload 앞부분 (STEP3 전) ≈ 수 분 — 10-19 SBE arm 0 (LEAN 2 · σ_e 만) 전체 879 s [리포 · 등록 v2 §7 C] 의 대부분이 전자 풀이다
  (같은 침대 최종 16 팔 a0 의 전자 풀이 704 s [리포 · 등록 v2 §7 10-20 00:2x 줄] · 서로 다른 런) — + raster 3 번 (DBE 4 번) + 경로 셀 · census
  (합성 1/10 크기 census 12 s [합성]) ⇒ **침대당 ≈ 15–30 분** · RAM 수 GB (se_dump 1.6 GB 의 몇 배).
- 거부되면 (`[S0] ⛔ 거부 — …`) 출력 폴더를 지우지 말고 그 줄을 보내 주세요 · 다시 돌릴 때는 **새** 출력 폴더 (도구가 비어 있지 않은 폴더를 거부한다).

### 2-3. 단계 2 — DBE 새 침대 + 옛 `kit_DBE` (★ §2-1 개정 커밋 **뒤에만**)

```bash
# ⛔ (10-21 · PRE-design-14 · 철회) 가지 끝 FETCH_HEAD 로 단계 2 를 돌리면 단계 1 과 다른 판의 census · registry 가 돌 수 있다 (s_min 의 뜻이 바뀐다)
# cd ~/dem-ca1 && git fetch -q origin claude/stoic-knuth-NObVQ && git checkout -q --detach FETCH_HEAD && git log --oneline -1   # 개정 커밋이 HEAD 의 조상이어야
# (10-21 · 개정 2) 단계 2 작업 트리 = §2-1 개정 커밋 그 자체
REV=<§2-1 개정 커밋 sha>
cd ~/dem-ca1 && git fetch -q origin claude/stoic-knuth-NObVQ && git checkout -q --detach "$REV" && git log --oneline -1 && git status --porcelain
# census · registry 가 단계 1 보고의 판과 같은지 (출력 없음 + rc 0 이어야 · 다르면 단계 2 를 돌리지 않는다 → 단계 1 을 이 판으로 다시 (σ 없음) · 개정 다시)
H1=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['code']['git_head'])" docs/data/rint2_s0_sbe_<날짜>/s0_stage1_kit_SBE_vgcf100.json)
git diff --quiet "$H1" "$REV" -- scripts/ca_s0_census.py scripts/carbon_junction.py scripts/ptfe_face_alpha.py scripts/step3_sigma.py \
    scripts/mpm_webapp_payload.py scripts/fibre_segment_raster.py scripts/sr01_stamp_compare.py; echo "same-version rc=$?"
# R 런 계획 · s_min · 세 숫자 손 확인 (도구가 아직 보지 않는다 — PRE-design-04 · 등록 R §2-1) — 등록 줄을 그대로 화면에
grep -n '^| 계획 해시 |\|^| S0 계획 해시 |' docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md
python3 ~/dem-ca1/scripts/ca_s0_census.py --stage 2 --threshold-commit "$REV" \
    --plan-path docs/data/rint2_s0_sbe_<날짜>/cjunc_plan.json \
    --kit ~/sdcp/kit_DBE_sdcp1um_vgcf100 --kit ~/sdcp/kit_DBE --out ~/sdcp/ca1_s0_dbe 2>&1 | tee ~/ca1_s0_dbe.log
```

- 도구가 확인 (아니면 거부): 개정 커밋이 이 작업 트리 HEAD 의 조상 · 그 커밋의 계획 파일 sha256 이 그 커밋의 등록 R 문서에 있음 · 계획 숫자 = 고정 식 재유도 · 정준 바이트.
- **(10-21 · 사전 리뷰 PRE-design-04 · 14 · 손 확인 — 도구가 보지 않는 것)** ① `same-version rc=0` (단계 1 보고의 `code.git_head` ↔ 개정 커밋의 census · registry 일곱 파일이 같다 · 보고의 `code.git_dirty` 가 true 면 = 다름으로 본다 · 보고의 `code.file_digests` 는 다섯 파일만 싣는다 — `carbon_junction.py` · `ptfe_face_alpha.py` 없음) ② 위 grep 의 `| 계획 해시 |` 줄 끝 칸이 64 자 sha (⬜ 아님) · 그 R 런 계획 파일의 `s_min_um` = 등록 R §2-1b 값 · `tol_ff_um` = S0 계획 `values_um.tol_ff` (같은 float) ③ 세 숫자 (§2-2 끝) 가 그 개정 커밋에 있다 — 하나라도 아니면 **단계 2 를 돌리지 않는다** (실측: S0 계획 해시 줄만 채운 커밋도 지금 관문은 통과시킨다 [탐침 · 리포 밖] · 관문 보강 = 에이전트 A · 그 뒤 이 손 확인을 줄인다).
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

- (10-21) **실제 명령** — 사슬 CLI = `scripts/rint_r_chain.py` 머리 (Z2 보고 꼴: `--stage ladder` (`--law` · `--target` · `--runner` · `--root` · `--plan` · `--max-hours` · `--out` · [`--variant FIBRE|UNREG|GRID`] · [`--dry-run`]) · `predict` (`--ladders` 둘 · `--kit` · `--runner` · `--root` · `--max-hours` · `--out` · [`--variant …|SVORDER`]) · `verdict` (`--runs` · `--out` · [`--show-results`]) · `--reverify`) · 사슬이 런마다 러너 env 를 정한다 (`CJUNC=1` · `CJUNC_RJ` (`inf` · `0` 극한) · 계획의 `CJUNC_LEN_LAW` · `CJUNC_UNREG_LAW` · `CJUNC_S_MIN_UM` · `CJUNC_TOL_FF_UM` · `STEP3_RTOL` · `P2_EXTRA` · `CJUNC_PTFE_JLAW` · `SDCP_MOD_C` · `ARM_LIST` · `SIGMA_FIBRE_BULK` · `PTFE_STAMP=face_alpha` · 부모 셸의 같은 이름꼴 env 는 지운다 · `SIGMA_VGCF_OVERRIDE` 가 있으면 멈춘다).
- ⚠ 이 CLI 는 지금 코드 그대로 · 등록 R 3판 규칙 (실제 역상 끝 · origin 세 R · 상태 분기 · 법칙별 구간 · 차단 표지 닫힌 집합 · 같은 판정 함수 · §5-3 문장) 은 아직 사슬에 없다 → 메인 통합 (시험 먼저) 뒤 CLI 가 바뀌면 이 블록을 다시 고친다.  (10-21 · 개정 2) 4판 규칙 (끝 origin = 세 origin 합집합 · 보호 띠 · 이름 우선순위 · 결정표 · 변이 표지) 도 아직 사슬에 없다 (등록 R §10-3).
- **(10-21 · 사전 리뷰 PRE-design-06 · 1저자 Q-F 권고대로) 순서 = 주 판정 먼저** — ① (3) 사다리 P0 · P1 → (4) 주 예측 → (5) **주 판정** (감도 폴더 없이 · 그 판 = `*_UNCHECKED` 표지 (지금 사슬 = 변이 폴더가 없으면 `<V>_UNCHECKED` · `scripts/rint_r_chain.py` 1298–1303 행 · 코드 읽기 · 시험 전) · 결과 문장 한정어 *"감도 미완료"* · 10-31 판정 = 이것) → ② 감도 (FIBRE · UNREG · GRID 사다리 + 예측 · SVORDER 예측) → (5) **전체 판정** (새 `--out` · 같은 주 판정 런 + 감도 폴더 · 두 기록을 나란히) · 시간 = 등록 R §10-4 (① 78 팔 ≈ 56 h · ×1.7–2 = 95–112 h · ② 264 팔 · ×1.7–2 = 392–462 h [우리 산술]) · 주 판정을 본 뒤 감도를 빼거나 바꾸지 않는다.

```bash
# ⛔ 발사 금지 — 꼴만 (10-21 · 실제 이름 · 등록 R §11 관문 1–9 뒤)
cd ~/dem-ca1 && git log --oneline -1 && git status --porcelain --untracked-files=no | head    # 핀 · 깨끗해야
. ~/dem-venv/bin/activate && unset SIGMA_VGCF_OVERRIDE

# (0) R 런 계획 파일 = 등록 R §2-1 개정 커밋의 파일 (~~rint-r-plan-v1 · 칸 = schema · len_law · unreg_law · s_min_um · tol_ff_um · step3_rtol · p2_extra~~ → (10-21 · 4판 정정 · 코드 이름) rint-r-plan-v2 · 칸 11 = 그 일곱 + 결과 전 등록 숫자 넷 max_ladder_points · calib_rj_ratio_max · sv_cf_threshold · sv_cf_scope · `rint_r_chain.PLAN_KEYS` · 일곱 칸 꼴 = 사슬이 PLAN_INVALID 로 거부) 바이트 그대로
cp ~/dem-ca1/<§2-1 개정 커밋의 R 런 계획 경로> ~/sdcp/ca1_plan.json
sha256sum ~/sdcp/ca1_plan.json      # = 등록 R §2-1 '| 계획 해시 |' 줄 끝 칸 (다르면 사슬이 PLAN_HASH_MISMATCH · 칸이 ⬜ 면 PLAN_HASH_UNREGISTERED 로 멈춘다)

# (2) 숫자 탐침 — SBE · 러너 직접 (사슬 밖) · 값 봉인 (반복 수 · 잔차 · 판 전류 불균형 · 시간만)
env VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=face_alpha BRIDGE_UM=0.48 SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_SDCP_OVERRIDE=256.6 SIGMA_FIBRE_BULK=1e4 \
    CJUNC=1 CJUNC_RJ=1e6 CJUNC_LEN_LAW=<계획 len_law> CJUNC_UNREG_LAW=cut CJUNC_S_MIN_UM=<계획 s_min_um> CJUNC_TOL_FF_UM=<계획 tol_ff_um> \
    CJUNC_PTFE_JLAW=P0 SDCP_MOD_C=0 STEP3_RTOL=<계획 step3_rtol> P2_EXTRA="--step3-maxiter <탐침 뒤>" EXPECT_BACKEND=gpu \
    KITS=kit_SBE_vgcf100 ARMS=1 LEAN=2 OUTDIR=~/sdcp/ca1_probe bash ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh

# (3) 보정 사다리 — 법칙 끝마다 (먼저 같은 인자 + --dry-run = 첫 런 다섯 (바닥 · 천장 · 1e4 · 1e6 · 1e8) 의 env 만 찍는다 · 폴더를 만들지 않는다)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --max-hours <등록 R §10 시간 상한> --out ~/sdcp/ca1_ladder_P0 --dry-run
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --max-hours <등록 R §10 시간 상한> --out ~/sdcp/ca1_ladder_P0
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --law P1 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --max-hours <등록 R §10 시간 상한> --out ~/sdcp/ca1_ladder_P1
# (4) 예측 — 네 모서리 × {R_j,lo · R_j,0 · R_j,hi} (DBE arm 0 · R_j · 계획 = 사다리 요약에서 사슬이 읽는다)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage predict --ladders ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1 --kit kit_DBE_sdcp1um_vgcf100 \
    --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --max-hours <등록 R §10 시간 상한> --out ~/sdcp/ca1_predict
# (5a) (10-21 · Q-F) 주 판정 — 감도 폴더 없이 · 값 열람 = 주 판정 런이 다 끝난 뒤 · 감도 런 전 (등록 R §4-1 · 열람 기록에 순서 · 시각) · 10-31 판정 = 이것
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --runs ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1 ~/sdcp/ca1_predict \
    --out ~/sdcp/ca1_verdict_main [--show-results]
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict_main
# 감도 (필수 · 등록 R §5-6 · (10-21 · Q-F) 주 판정 뒤): FIBRE · UNREG · GRID = 사다리 둘 (--variant <이름> --law P0 · P1) + 예측 (--variant <이름> --ladders <그 변이 사다리 둘>) ·
#   SVORDER = 예측만 (--variant SVORDER --ladders ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1) · 출력 폴더는 런마다 새로 (예 ~/sdcp/ca1_ladder_P0_FIBRE)
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage ladder --variant FIBRE --law P0 --target 1.63 --runner ~/dem-ca1/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --plan ~/sdcp/ca1_plan.json --max-hours <등록 R §10 시간 상한> --out ~/sdcp/ca1_ladder_P0_FIBRE
# (5) (전체) 판정 — 원 팔 JSON 전부에서 · 값은 --show-results 로 한 번 (판정에 쓰는 런이 다 끝난 뒤 · 열람 기록) · 다시 판정 = 읽기 전용 바이트 대조
#     (10-21 · Q-F) 주 판정 (5a) 뒤 두 번째 열람 — 같은 주 판정 런 + 감도 폴더 · 주 판정 숫자는 바뀌지 않는다
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --runs ~/sdcp/ca1_ladder_P0 ~/sdcp/ca1_ladder_P1 ~/sdcp/ca1_predict <감도 폴더 전부> \
    --out ~/sdcp/ca1_verdict [--show-results]
python3 ~/dem-ca1/scripts/rint_r_chain.py --stage verdict --reverify ~/sdcp/ca1_verdict
```

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

- ⬜ ① 재압밀 — SBE · DBE 런 폴더 · 시작 · 끝 시각 · §1-4 출력 · §1-5 선택 (가 / 나)
- ⬜ ② S0 단계 1 — 요약 · 계획 sha256 → 등록 R §2-1 개정 커밋 sha
- ⬜ ③ S0 단계 2 — 요약
- ⬜ §4 ① L_c · J8 결정
- ✅ (10-21) 1저자 Q13 (가) = 새 킷 payload 줄에서 `--joule-heat` · `--save-step4-grid` 뺀다 (§1-1) · ✅ §1-5 = (가) (10-20 밤 Q18 · §4 ②) · ✅ §4 ① = Q17 (10-20 밤)
- ⬜ (10-21) ① 재압밀의 §1-1 확인 출력 (diff `^[<>]` 4 · grep 0) · §1-4b 출력 (CFL 제한 상 · 종료 이유 · substep · 코드 시간 · 재시도 · 실행 코드 지문)
- ⬜ (10-21) ② 단계 1 의 새 census 블록 · s_min 개발 단계 기록 · 해시 두 줄 (S0 계획 · R 런 계획) → 등록 R §2-1 개정
- ⬜ (10-21 · 개정 2 · Q-G) 세 숫자 (점 수 상한 · 역상 폭 상한 · SV 반사실 문턱) 등록 R 개정 커밋 — Codex 회신 뒤 · 단계 2 전
- ⬜ (10-21 · 개정 2) ③ 단계 2 의 손 확인 출력 (`same-version rc=` · 해시 두 줄 grep · `git status --porcelain`)
- ⬜ (10-21 · 개정 2 · Q-F) ④ 주 판정 (`ca1_verdict_main` · 열람 시각) → 감도 → 전체 판정 (`ca1_verdict`)
