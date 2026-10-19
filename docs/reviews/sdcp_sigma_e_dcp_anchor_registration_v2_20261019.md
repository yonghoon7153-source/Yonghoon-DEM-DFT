# SBE · DBE σ_e 실험 앵커 v2 — 10-16 DC 분극으로 앵커 교체 · DBE 침대 SDCP 1 µm 재압밀 (2026-10-19 · 결과 0 건)

> 1저자 10-19: *"SBE는 90um, DBE는 80um / sdcp 값 바꾸고 해야될듯"* · *"이 값을 바탕으로 다시 16팔 할 준비"* · 지름 10 mm *"이거에 앵커링 하는게 맞고"* ·
> *"새 값으로 대체하는게 맞고"* · 지그 저항 *"걱정안해도 되고"* · *"s1 해서 sbe 맞추고 그거에 맞게 dbe 진행해보고 값을 우선 비교한다음에 s1b로 넘어가는걸 조금 고민해보자"* ·
> *"S1 방식으로 SBE 구한다음에 dbe를 16팔이나 해야돼?"* (→ 비교 = arm 0 · 16 팔 = 최종 값에서 한 번) · *"애초에 들어간 sdcp 크기가 잘못됐었네"* ·
> *"재압밀부터 시작하자 sbe는 놔두고 dbe에 들어가는 sdcp 크기 다르게 해서 압밀하는게 맞는듯"* · *"1um로 하면 될듯"* · *"볼밀치고 하면 이게 깨지고 할태니까 평균 크기가 이렇게 되게"*.
> 이 문서는 **런 전에** 커밋한다 — 결과를 보고 규칙 · 크기 · 문턱을 옮기지 않는다.  옛 등록 `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md`
> (앵커 4.47 · 12.4 · σ* 3.41 · 16 팔) 은 이력이다.  진행 기록 = `docs/session_20260923_progress.md` 10-19 줄.

## 0. 무엇을 · 왜

- **앵커 교체**: 4.47 · 12.4 mS/cm (조건 미확인) → 10-16 DC 분극 **SBE 1.63 · DBE 4.68 mS/cm** (원자료 · 두께 · 지름 있음 · §1).
  옛 두 값은 같은 저항에 지름 6 mm 면적을 넣은 값 (4.54 · 12.99) 과 비슷하다 — 두께가 246 · 212 µm 여도 같은 값이 나온다 · 어느 쪽인지 모른다 · 쓰지 않는다.
- **SBE 로 σ_VGCF 를 보정**한다 (v1 §0 과 같은 이유 — σ_e ∝ σ_VGCF^0.9 · 복셀에 접촉 저항 항 없음 · `CL-39` · `CL-47` · `CL-81`).  SBE 침대는 그대로다.
- **DBE 침대만 재압밀** — SDCP 크기를 원고 SEM 에 맞춘다: 지금 Ø0.30 µm 낱알 (`scripts/additives.py` `SDCP_D` — 원고 Figure 2f · S5 의 0.2–0.5 µm 판독) →
  **평균 1 µm** (1저자 판독: 전극 SEM 에서 NCM 위 SDCP ≈ 0.8–1.3 µm · 원고 그림 S1 의 만든 직후 입자는 수 µm · 볼밀로 깨진 평균).  σ_SDCP 는 측정값 256.6 그대로
  (올려도 포화 — `CL-70` ×100 = 이득 +3.5 %).
- 순서 (1저자): S1 → S2 → **비교 (arm 0)** → 1저자가 다음 단계 (S1b · PTFE 표현 · Rint 등) 결정 → 최종 값에서 16 팔 한 번 (이 등록 밖 · 그때 개정).

## 1. 실험값 (원자료 `docs/data/sdcp_dc_polarization_20261016/` · 판독 `read_dc.py` → `dc_reading.json`)

| 시료 | 채널 | R (8 점 I–V 직선) | r² · 오프셋 | 쌍 저항 (±5 · 10 · 15 · 20 mV) | 두께 | σ_e |
|---|---|---|---|---|---|---|
| SBE | C05 | 7.016 Ω | 0.999999 · +0.19 mV | 7.003–7.023 Ω | 90 µm | **1.63 mS/cm** |
| DBE | C06 | 2.178 Ω | 0.99993 · +0.33 mV | 2.141–2.199 Ω | 80 µm | **4.68 mS/cm** |

- σ = L/(R·A) · A = π (0.5 cm)² (지름 10 mm = 1저자) · 파일마다 600 s 유지의 마지막 60 s 평균 · 비 DBE/SBE **2.86**.
- 한정: 2 전극 (지그 · 리드 · 전극 접촉 포함 · 빼지 않음 = 1저자) · 시료 n = 1 씩 · 두께 하나씩 · 두께를 잰 상태 미확인 · 같은 날 두 채널 · 옴 거동 (r² 위).
  그날 첫 런 (DBE +5 mV) 만 마지막 1 분 끌림 −3 %/분 — 빼고 맞춰도 R 2.1779 Ω (같음).

## 2. 고정 (v1 §2 그대로 — STEP3)

vox 0.15 µm · 브리지 0.48 µm · VGCF 선분 스탬프 · PTFE `centerline` · SDCP 구 스탬프 Ø0.30 µm (`SDCP_SPHERE_D=0.30` — 재압밀 침대에서도 SDCP 1 차 입자 = 0.30 µm ·
덩어리는 그 1 차 입자들의 모임) · plate rule p2-occupied-surface-first · 주기 x·y 없음 · NCM σ 0.0041 S/cm · σ_SDCP 256.6 S/cm · LPSCl σ_ion 0.0015 S/cm ·
SDCP 이온 σ 1.0 × 10⁻³ (가정) · 러너 `scripts/sdcp_gain_vox015_8arm.sh` · 침대 = kgy `~/sdcp/kit_SBE` (그대로) · `kit_DBE` (옛 · 비교용) · `kit_DBE_sdcp1um` (재압밀 · §3-B).

## 3. 절차 · 판정 (결과 전 고정)

### 3-A. SBE 보정 (지금 시작 가능 · DBE 재압밀과 독립) — 사슬 `scripts/sdcp_anchor_v2_chain.py --stage sbe`

| 단계 | 무엇 | 설정 |
|---|---|---|
| S1 정찰 | SBE arm 0 · σ_e 만 · σ_VGCF **1.309 · 0.6545 · 0.3272** S/cm (= 2.618 ÷ 2 · 4 · 8) | `ARMS=1 LEAN=2` + 공통 env (§2) |
| S2 σ_VGCF* | ln σ_e ↔ ln σ_VGCF 를 목표 **1.63** 을 끼는 이웃 두 점 사이 직선 보간 · 유효숫자 3 자리 · 목표가 밖이면 같은 쪽으로 ÷2 (**0.1636 → 0.0818**) 또는 ×2 (**2.618 → 5.236**) 점을 최대 둘 더 (같은 규칙) · 단조 아니면 멈춤 | — |
| C1 비교 | σ* 에서 SBE arm 0 · **옛 DBE 킷** (`kit_DBE` · Ø0.30 낱알) arm 0 | 같은 env |

### 3-B. DBE 재압밀 (SDCP 평균 1 µm · SBE 는 그대로)

- **R0 (읽기만 · kgy)**: `scripts/sdcp_bed_meta.py ~/sdcp/kit_SBE ~/sdcp/kit_DBE` — 옛 두 침대의 압밀 명령 · 세대 (E 앵커 · 밀도 세대 · 섞기 · 난수 · seed · 격자 · 재하율 · 코드) 기록.
- **R1 (명령 = R0 를 본 뒤 이 문서 §7 에 적고 발사 — 결과 전)**: 옛 `kit_DBE` 와 **같은 명령 · 같은 세대** (코드가 바뀐 기본값은 `--add-e-override` · `--dens-gen` 등으로 옛 값 고정 ·
  가능하면 옛 침대를 만든 코드 판 그대로) + **`--sdcp-agg-d 1.0` 한 가지만** 더한다 (기존 노브 — 0.3 µm 1 차 입자 덩어리 · 평균 지름 1 µm · 내부 채움 `SDCP_AGG_PACK` 0.64 =
  기존 가정 · NCM 에 붙는 몫 = 섞기 행 기본 (ballmill 0.5) 그대로).  새 킷 폴더 `kit_DBE_sdcp1um` (옛 킷의 입력만 복사 — `run_*` · `latest_run` 은 복사하지 않는다 ·
  실패하면 옛 침대를 읽는 사고를 막는다) · `MPM_NO_PULL=1` (킷의 자동 git pull 끔 · 코드 고정).
- **R2 (침대 확인 · 읽기만)**: 새 침대의 SDCP 시딩 기록 = 덩어리 모드 · agg_d 1.0 · 1 차 입자 수 · 덩어리 수 · 실현 부착 몫 / 다른 상 (AM · SE · VGCF · PTFE) 의 시딩 기록이
  옛 `kit_DBE` 와 같은가 (같으면 *"SDCP 크기만 바뀜"* · 다르면 *"새 실현"* 으로 적는다 — `ADD` 순서상 SDCP 는 VGCF · PTFE 뒤라 공유 난수에서도 앞 상은 그대로일 것 = 추정 · 확인 대상).

### 3-C. DBE 비교 — 사슬 `--stage dbe --dbe-kit kit_DBE_sdcp1um`

- 같은 `--out` 의 3-A 요약에서 σ* 를 읽어 (사람이 옮겨 적지 않는다) 재압밀 킷 arm 0 @ σ*.

### 3-D. 이온 σ₀ 유효값 — ✅ 1저자 10-19 (결과 전 고정)

- 1저자 10-19: *"이온전도도 관련된 전류밀도도 지금 rint가 구현이 안돼서 애매하니까 우선적으로 논문용으로 문헌 anchoring … 전도도 bulk를 조절할 수 있나?"* ·
  *"0.55 이건 너무 높은듯"* · 권고 (Bazzoun 2026 70 wt% · 정본 카드 확인 뒤 300 MPa 환산 규칙과 같이 등록) 에 *"우선 이걸 anchoring 해줘"* · *"sdcp도 그거랑 맞게 anchoring 해줘"*.
- **앵커** = litdb 정본 카드 `bazzoun2026_dem_fem_rnm_ionic` (정본 가지 · status ✅): LPSCl + NCM811 (POSCO) · CAM **70 wt%** · 전자 차단 대칭셀 EIS (Z-type TLM) · **400 MPa** ·
  σ_eff,ion **0.137 mS/cm** (SI Table S1 반복 0.123 / 0.135 / 0.153) · 그 연구의 펠릿 1.02 mS/cm.
- **압력 규칙**: 주 값 = 400 MPa 값 그대로 (카드의 RNM σ–P 는 ~400 MPa 포화 · 끝점 (100 · 400 MPa) 만 있어 300 MPa 값을 못 정한다) · 민감도 = RNM 끝점 선형 보간으로 300 MPa
  (70 wt%: 0.068 → 0.135 · 배수 0.8346 → 0.114 mS/cm · 곡선이 오목하므로 하한).
- **기하 인자** f_SBE = σ_ion/σ_SE = **0.18395** (`docs/data/ion8_isd10e-03_20260831/` SBE 8 팔 평균 0.55184 mS/cm @ σ_SE 3.0 mS/cm · 같은 SBE 침대).  STEP3 이온 표
  (`step3_sigma.ionic_sigma_table`) 에서 이온을 나르는 상은 SE (sid 6) · SDCP (sid 5) 뿐 (AM · 탄소 · PTFE = 0) ⇒ SBE σ_ion ∝ σ_SE 정확 · SE 와 SDCP 를 **같은 배수**로 바꾸면 DBE 도 정확히 비례.
- **값 (유효숫자 3 자리)**: σ₀,eff = 0.137 / 0.18395 = **7.45 × 10⁻⁴ S/cm** (`SIGMA_ION_SE=0.000745`) · SDCP 이온 σ = 같은 배수 k = 0.745/3.0 = 0.2483 × 기존 1.0 × 10⁻³
  = **2.48 × 10⁻⁴ S/cm** (`SIGMA_ION_SDCP=0.000248` · 1저자 *"sdcp도 그거랑 맞게"*) / 민감도 6.22 × 10⁻⁴ · 2.07 × 10⁻⁴.
- **결과 (산술 · 다시 돌릴 런 없음)**: SBE σ_ion = 0.137 mS/cm (맞춘 값) · 옛 DBE 침대 = 0.2483 × 0.55641 = 0.138 mS/cm (비 1.008 그대로) · 새 DBE 침대 = 최종 16 팔 (LEAN=4 ·
  위 두 env) · 확인 = 최종 16 팔 SBE 8 팔 평균 σ_ion 이 0.137 ± 1 % (같은 침대 · 같은 f 면 정확).  이온 전류 밀도 **분포 모양 · 집중 인자는 그대로** (모든 이온 상을 같은 배수로) — 크기만 k 배.
- **Table S2**: LPSCl σ_ion = 7.45 × 10⁻⁴ S/cm · "Calibrated (composite EIS, CAM 70 wt%, Bazzoun 2026)" · 각주 = 복셀 모델에 없는 접촉 · 입계 저항을 bulk 유효값에 뭉뚱그린 값
  (재료 물성 아님) · 이 연구의 펠릿 실측 (원고 본문의 LPSCl σ) 과 다른 이유를 Methods 에 한 줄 · SDCP 이온 σ = 2.48 × 10⁻⁴ (가정 · LPSCl 과 같은 배수).
- 한정: Bazzoun 전극은 VGCF · PTFE 없음 (우리 첨가제는 이온 길을 더 막는다 → 같은 앵커면 우리 σ_ion 이 약간 높게 잡힌다) · 400 vs 300 MPa (위 민감도) · 반복 ±11 % ·
  균일 보정이라 접촉 협착이 빠진 분포 모양은 그대로 (= "contact-free 분포" 한정어 유지 · Rint = 다음 세대).

### 보고 (판정 아님) · 결과 전 기록

- 보고 칸: SBE arm 0 @ σ* ↔ 1.63 (보간 확인 · ±5 % 밖이면 적어 둔다) · DBE (옛 · 새) ↔ 4.68 · 비 ↔ 2.86 · 옛 ↔ 새 DBE 차이 (= 크기 바꿈의 효과 — R2 가 "SDCP 만 바뀜" 일 때만 그렇게 부른다).
- **결과 전 어림 (판정 아님)**: σ* ≈ 0.2–0.6 S/cm · 옛 DBE 비 ≤ 1.24 (`CL-70` — σ_AM/σ_VGCF 대비가 커지면 비가 내려간다 · σ* 가 v1 의 3.41 보다 낮아 그 대비가 ×10 안팎) ·
  옛 DBE ≈ 1.8–2.0 mS/cm.  **새 DBE (1 µm) 방향 예측 없음** — 같은 부피에서 SDCP 덩어리 수가 ~24 배 줄어 다리 자리가 줄고 (↓), 덩어리 하나가 ~1 µm 간격을 잇고 NCM 에 붙는다 (↑).
- 크기 1 µm 는 이 결과를 보고 다시 고르지 않는다 (SEM 판독값 · 결과 전).

### 멈춤 (사슬이 강제)

출력 폴더가 이미 있고 비어 있지 않음 (러너 SKIP 캐시 재사용 방지) · 러너 rc ≠ 0 · `.rejected_*` · σ_e 를 실은 `p2_*.json` ≠ 1 · 매니페스트 (σ_VGCF · σ_AM_S ·
σ_SDCP · vox · 브리지 · PTFE · SDCP 구 지름) ≠ 요청 · 수렴 (`run_contract.conv_ok`) 실패 · 둘 더해도 목표 밖 · 단조 아님 · 시간 상한 (8 h) · 같은 DBE 킷 두 번.

## 4. 한정어 (결과와 함께 쓴다)

- v1 §4 그대로: σ* = vox 0.15 의 뭉뚱그린 유효값 (섬유 물성 아님 · `CL-41`) · σ_ion = 접촉 저항 미포함 상한 (`CL-81`) · PTFE = centerline (실제 부피의 0.40–0.41 · 표면 코팅 없음).
- 실험: 한 측정일 · n = 1 · 2 전극 · 두께 상태 미확인 — *"모델이 실험을 재현"* 이라 쓰지 않는다 (보정 1 점 + 비교).
- SDCP 1 µm: SEM 한 시야 · 분포 모름 · 원고 Figure 2f · S5 의 0.2–0.5 µm 와의 공존 (작은 조각 + 큰 덩어리?) 미해결 · 덩어리 = 0.3 µm 1 차 입자의 채움 0.64 (가정 — 실제는
  더 치밀할 수 있다) · 부착 몫 0.5 (가정).  nm 두께 SDCP 막 (SEM 에 안 보이는 접점 코팅) 은 어느 크기로도 표현되지 않는다 (→ Rint · 계면 쪽).
- 비 2.86 에는 PTFE 1 → 0.5 wt% 몫도 들어 있다 — 모델 차이를 SDCP 로만 읽지 않는다.

## 5. 명령 (kgy · 1저자)

```bash
# ① 새 작업트리 (돌고 있는 ~/dem-mt 는 건드리지 않는다) · 파이썬 = ~/dem-venv
cd ~/dem-mt && git fetch -q origin claude/sdcp-dem-manuscript-si-pqwtv8 && git worktree add --detach ~/dem-anchor1019 FETCH_HEAD && git -C ~/dem-anchor1019 log --oneline -1
. ~/dem-venv/bin/activate && cd ~/sdcp && ls -d kit_SBE kit_DBE && nvidia-smi --query-gpu=memory.used,memory.total --format=csv

# ② 3-A — 사슬 시험 · 명령 확인 · 발사 (끊겨도 돈다)
python3 ~/dem-anchor1019/scripts/sdcp_anchor_v2_chain.py --selftest
python3 ~/dem-anchor1019/scripts/sdcp_anchor_v2_chain.py --stage sbe --runner ~/dem-anchor1019/scripts/sdcp_gain_vox015_8arm.sh --root ~/sdcp --out ~/sdcp/anchor_v2_1019 --dry-run
setsid nohup python3 ~/dem-anchor1019/scripts/sdcp_anchor_v2_chain.py --stage sbe --runner ~/dem-anchor1019/scripts/sdcp_gain_vox015_8arm.sh \
    --root ~/sdcp --out ~/sdcp/anchor_v2_1019 > ~/anchor_v2_1019_sbe.log 2>&1 < /dev/null &
tail -f ~/anchor_v2_1019_sbe.log          # 끝나면: cat ~/sdcp/anchor_v2_1019/chain_summary.json

# ③ 3-B R0 — 옛 침대 기록 (읽기만 · 이 출력을 보내 주세요 → R1 명령을 §7 에 적어 드립니다)
python3 ~/dem-anchor1019/scripts/sdcp_bed_meta.py ~/sdcp/kit_SBE ~/sdcp/kit_DBE
```

- GPU 하나 (RTX 3090 24 GB) — 3-A 의 STEP3 풀이와 3-B 의 MPM 압밀을 동시에 돌릴지는 ① 의 nvidia-smi 여유를 보고 1저자가 정한다 (기본 = 차례로).

## 6. 다시 만들 원고 그림 · 표 (DBE 침대 · σ* 가 바뀌므로 — 최종 16 팔 (LEAN=4) 한 번에서)

- 전자 전도망 그림 (원고 · 1저자 10-19 *"이거 전체적으로 바뀌겠네 · a도 바뀌고 1um로 바뀌었으니까"*): (a) CA density near AM 지도 (DBE 바뀜 · SBE 정규화 기준 그대로) ·
  (b) CA contacts per AM (`scripts/cbd_contacts_per_am.py` · `scripts/plot_cbd_contacts.py` — SBE 74 그대로 예상 · DBE 86 은 SDCP 개체 수가 ~24 배 줄어 바뀜 ·
  덩어리 = 개체 하나) · σ_ele_eff 막대 (SBE ≈ 1.63 보정 · DBE 예측).
- Table S3 (σ_e · σ_ion · 전자 연결도 · 전류 집중 인자 + DBE 두께 · 기공 · SE / CA coverage) · 전류 밀도 그림 · Table S2 (VGCF σ* = "Calibrated (SBE DC polarization)" ·
  SDCP = 0.3 µm 1 차 입자의 평균 1 µm 덩어리 (SEM) · LPSCl σ_ion = 3-D · SDCP 이온 σ = 3-D).
- ⚠ 그림 번호 = 이 문서는 옛 판 번호를 썼다 — 1저자 10-19 판 (원고 PDF sha256 `ffb824e4…` · SI docx `7e034a20…`) 에서 SDCP 크기 앵커 = Fig 3c · S1 · 전류 밀도 = S16 · S17 ·
  그림 S15 도 다시 만든다.  자리별 목록 = `docs/reviews/ms_change_checklist_sdcp_v2_20261019.md` (본문 25 · SI 25 · 값 나오면 일괄 수정 — 1저자 10-19 *"값 나오면 일괄적으로 수정하자"*).
- 원고 글 추가: Methods 에 σ_VGCF · σ₀ 보정 문장 · Experimental Section 에 전극 DC 분극 방법 (지금은 바인더–LPSCl 혼합물 측정만).

## 7. 실행 기록

- **10-19 R0 (kgy · 1저자 · 읽기만)**: 옛 두 침대 = 같은 명령 (조성만 3:1 ↔ 3:0.5:0.5) · `--mixing thinky` · `--seed 3` · `--n-grid 263` · `--frames 150` · `--protocol hold` ·
  `--lateral-box 0.05` · `--dilate-z 1.0719` · `--coh-ptfe 0.10` · `--binder-opt-wt 1.5` · `--fibre-buckle --fibre-align 0.606` · V/c_P 0.2717 · 08-27 런 · 세대 `ADD_E_SET_20260818_9.0GPa`
  (VGCF E 10 GPa · 지금 코드 기본 100 = `CL-93`) · SDCP 낱알 (agg 0) · 붙는 몫 0.5 · 시딩 138,988 (붙음 61,762 · 공극 77,226) · 코드 판 기록 없음 · `--gpu-mem 28` (V100 시절 값).
  ⇒ Table S2 SDCP E 9.0 = 침대 실제 값 (체크리스트 질문 닫힘).
- **10-19 R1 명령 (결과 전 · 제안 = 1저자에게 전달)**: 새 킷 `kit_DBE_sdcp1um` = 옛 킷 입력만 복사 (`run_*` · `latest_run` · `scripts` 제외) + `scripts` → 고정 작업트리 링크 ·
  `run_mpm.sh` 의 mpm3d 줄에 `--sdcp-agg-d 1.0 --add-e-override VGCF=10` (옛 세대 VGCF 10 GPa 고정) · `--gpu-mem 28 → 20` (자원만) · `MPM_NO_PULL=1` · 나머지 그대로.
  한정: 코드 판이 08-27 과 다를 수 있다 → R2 에서 VGCF · PTFE 섬유 (`fibre.npy`) sha256 를 옛 침대와 대조 (같으면 앞 상 시딩 그대로 · 다르면 "새 실현").
- **10-19 첫 S1 발사 = 멈춤 (계산 전)**: 사슬이 LEAN=2 런에 `SIGMA_ION_SE` 를 넘겨 러너 가드 *"이온 축을 줬는데 --no-ion"* 이 rc 2 (`SELF-120` — 사슬 결함 · 가짜 러너가
  그 가드를 흉내내지 않았다) → 고침 (이온 축 빼고 부모 env 의 것도 지움 · 시험 먼저 5/16 → 16/16 · 로그 `docs/data/sdcp_dc_polarization_20261016/chain_tests/`) → 다시 발사 대기.
