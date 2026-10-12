# SBE · DBE σ_e 실험 앵커 보정 — STEP3 표 값 재실행 등록 (2026-10-12 · 결과 0 건)

> 1저자 10-12: σ_e 실험값 **SBE 4.47 · DBE 12.4 mS/cm** (kgy DC 분극 · 정정값) — *"이건 실험값이니까 앞으로 여기에 anchoring 해서 하면 될듯"* ·
> *"비율은 유지 안되도 되고 대소만 확실하면"* · Q1–Q4 비준 *"ㅇㅇ table에 맞게 다시 처음부터 하자"*.
> 이 문서는 **런 전에** 커밋한다 — 정찰 · 본 런 결과를 보고 규칙을 옮기지 않는다.  진행 기록 = `docs/session_20260923_progress.md` 10-12 줄.

## 0. 무엇을 · 왜

- 원고 SI Table S3 (STEP3 · vox 0.15 · PTFE centerline) σ_e **SBE 54.0 · DBE 70.6 mS/cm** (원장 `CL-70` 이 다른 기계에서 53.9 · 70.6 재현) ↔ 실험 4.47 · 12.4 → SBE ÷12.1 · DBE ÷5.7.
- 탄소 유효 전도도 σ_VGCF 가 σ_e 를 거의 정한다 — σ_e ∝ σ_VGCF^0.91 (`CL-39` · vox 0.15 · ×1.44 실측: SBE 0.07302 → 0.1019 S/cm).
  σ_VGCF 100 (복셀 78.5) 은 출처 없이 넣은 유효 망 계수다 (`CL-47` 정정 · `RINT-10`) — 단섬유 10⁴ ↔ 압분체 ~10² S/cm 의 차이가 섬유 접촉 저항이고 복셀에는 접촉 저항 항이 없다 (`CL-81`).
  ⇒ **SBE 하나로 σ_VGCF 를 보정하고 (Table S2 의 E_SE 1.35 와 같은 "Calibrated"), DBE 는 맞추지 않고 예측해서 대소만 본다** (Q1 비준).
- 표 값으로 맞춘다 (Q3 · Q4 비준 · *"table에 맞게"*): NCM811 σ_e = Table S2 4.1 × 10⁻³ S cm⁻¹ (코드는 0.01 이었다) · SDCP σ_e = Table S2 256.6 (측정 · 코드 250) ·
  LPSCl σ_ion = **1.5 × 10⁻³** (σ₀ 보고 기준 · 1저자 10-12 *"1.5로 다 통일"* · Table S2 의 3.0 × 10⁻³ 행도 1.5 로 바꾼다).
- **MPM 압밀 (STEP2) 은 다시 돌리지 않는다** — σ 는 침대에 영향이 없다.  STEP3 만 새 출력 폴더에서 처음부터 (옛 팔 재사용 없음).

## 1. 실험값 (1저자 전달 · 조건 미확인)

| 시료 | σ_e (mS/cm) | 방법 |
|---|---|---|
| SBE | **4.47** | DC 분극 (kgy) |
| DBE | **12.4** | DC 분극 (kgy) |

- 조성 = 실조성 = 모델과 같다 (1저자 10-12): SBE 70 : 27 : 3 : 1 · DBE 70 : 27 : 3 : 0.5 : 0.5 (NCM : LPSCl : VGCF : PTFE (: SDCP)) — 모델 SBE 침대 = PTFE 1 · DBE = PTFE 0.5 + SDCP 0.5 (`docs/sdcp_318_base_sbe_dbe_comparison.md` §1).
- ⬜ 미확인 (아는 것만 받으면 적는다): 두께 · 성형 / 측정 압력 · 온도 · 전극 · PTFE 0.5 wt% 단독 (SDCP 없음) 대조 유무.
  조성이 다르면 보정을 다시 한다 (이 문서의 규칙 그대로 · 결과 전 개정).
- 처음 전달값 5.59 · 12.3 은 1저자가 정정했다 — 쓰지 않는다.
## 2. 고정 (원고 Table S3 생산 설정 그대로 — `docs/data/w4_ptfe_centerline_20260827/` 매니페스트)

vox 0.15 µm · 브리지 0.48 µm (러너 기본 · 명시) · VGCF 선분 스탬프 · PTFE `centerline` · SDCP 구 스탬프 Ø0.30 µm (`SDCP_SPHERE_D=0.30`) · plate rule p2-occupied-surface-first ·
주기 x·y 없음 · origin 8 팔 · 침대 = kgy `/home/kgy/sdcp/kit_SBE` · `kit_DBE` (같은 MPM 침대) · 러너 `scripts/sdcp_gain_vox015_8arm.sh` · SDCP 이온 σ 1.0 × 10⁻³ (가정 · 그대로).
침대의 활물질 = AM_S 한 상 (매니페스트 dissipation_share = AM_S 뿐) ⇒ NCM σ 는 `SIGMA_AM_S_OVERRIDE` 하나로 바뀐다.

## 3. 절차 · 판정 (결과 전 고정)

| 단계 | 무엇 | 러너 설정 |
|---|---|---|
| S1 정찰 | SBE · arm 0 (진단 런 · `ARMS=1`) · σ_e 만 · σ_VGCF **7.854 · 5.236 · 3.927** (= 78.54 ÷ 10 · 15 · 20) | `KITS=kit_SBE ARMS=1 LEAN=2 SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_VGCF_OVERRIDE=<값>` |
| S2 σ_VGCF* | ln σ_e ↔ ln σ_VGCF 를 4.47 을 끼는 두 점 사이 직선 보간 · 유효숫자 3 자리 · 4.47 이 세 점 밖이면 ÷1.5 또는 ×1.5 점을 최대 둘 더 (같은 규칙) | — |
| S3 본 런 | SBE · DBE · 8 팔 · σ_e + σ_ion + 필드 (전류 집중 인자) | `ARMS=8 LEAN=4 SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_SDCP_OVERRIDE=256.6 SIGMA_ION_SE=0.0015 SIGMA_VGCF_OVERRIDE=<σ*>` |

- **J1 보정 수락**: S3 의 SBE 8 팔 평균이 4.47 ± 5 % (4.25–4.69) 안 → 수락.  밖이면 한 번만 고친다: σ** = σ* × (4.47 / 평균)^(1/b) (b = S1 의 국소 로그 기울기) 로 S3 를 다시 · 그 결과는 어긋남과 함께 그대로 보고 (더 반복하지 않음).
- **J2 대소 (판정)**: 같은 origin 짝의 DBE / SBE 비 평균 R̄ − 3·SD > 1.01 (`CL-70` 과 같은 기준) → *"DBE > SBE"* 유지.  비 (실험 2.77) 는 맞추지 않는다 (1저자) — 예측 DBE 를 12.4 옆에 그대로 적는다.
- **J3 보고**: Table S3 새 값 (σ_e · σ_ion · 전자 연결도 · 전류 집중 인자) · Table S2 바뀌는 행 (LPSCl 1.5 × 10⁻³ · VGCF 복셀 σ = σ* "Calibrated (SBE DC polarization)" · NCM 4.1 × 10⁻³ · SDCP 256.6 = 이제 코드와 같음).

## 4. 한정어 (결과와 함께 쓴다)

- σ* 는 **vox 0.15 의 뭉뚱그린 유효값**이다 — 섬유 접촉 저항 · 미해상 기하를 탄소 σ 하나에 담는다 (격자 미수렴 `CL-41` · 섬유 물성 아님).
- σ_ion = 접촉 저항 미포함 (복셀 · `CL-81`) → **상한** 표지 · σ₀ 1.5 (펠릿 문헌 1.0–2.2 안).
- PTFE = centerline (실제 PTFE 부피의 0.40–0.41 · 표면 코팅 없음) — 실험 비 2.77 과 모델 비의 차이 후보 (Lee 2025 곡선 보간으로 PTFE 1 → 0.5 wt% 만 ≈ 2.3 배 [산술 · 증거 아님] → SDCP 몫 ↔ PTFE 절반 몫은 지금 측정으로 못 가른다).
- 실험 조건 미확인 (§1) — 같은 양인지 확인 전에는 *"모델이 실험을 재현"* 이라 쓰지 않는다 (보정 1 점 + 대소 1 개).

## 5. 명령 (kgy · 1저자)

```bash
# ① 새 작업트리 (돌고 있는 ~/dem-mt 는 건드리지 않는다) · 파이썬 = ~/dem-venv
cd ~/dem-mt && git fetch -q origin claude/sdcp-dem-manuscript-si-pqwtv8 && git worktree add --detach ~/dem-anchor1012 FETCH_HEAD && git -C ~/dem-anchor1012 log --oneline -1
. ~/dem-venv/bin/activate && cd ~/sdcp && ls -d kit_SBE kit_DBE

# ② S1 정찰 — SBE arm 0 · σ_e 만 · 세 값 차례로 (≈ 20 분 × 3)
for SG in 7.854 5.236 3.927; do
  env VOX=0.15 SDCP_SPHERE_D=0.30 PTFE_STAMP=centerline KITS="kit_SBE" ARMS=1 LEAN=2 \
      SIGMA_AM_S_OVERRIDE=0.0041 SIGMA_VGCF_OVERRIDE=$SG \
      bash ~/dem-anchor1012/scripts/sdcp_gain_vox015_8arm.sh > ~/anchor_scout_sg$SG.log 2>&1
  echo "SG=$SG rc=$?"
done
# ③ 정찰 결과 (팔 JSON 의 sigma_e_eff_S_cm · 수렴) — 이 출력을 보내 주세요
python3 - <<'PY'
import glob, json, os
for sg in ('7854', '5236', '3927'):
    for f in sorted(glob.glob(os.path.expanduser(f'~/sdcp/prereg_v2_vox015*_sg{sg}*/**/*.json'), recursive=True)):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        s = d.get('step3', d) if isinstance(d, dict) else None
        if isinstance(s, dict) and 'sigma_e_eff_S_cm' in s:
            print(sg, f, s['sigma_e_eff_S_cm'], 'cg_info', s.get('cg_info'), 'unconverged', s.get('unconverged'))
PY
```

S1 결과 (세 로그 끝 · 팔 JSON 의 σ_e) 를 받으면 S2 로 σ* 를 정해 S3 명령을 준다 (S3 = 위 표 설정 · 8 팔 × 두 침대).
