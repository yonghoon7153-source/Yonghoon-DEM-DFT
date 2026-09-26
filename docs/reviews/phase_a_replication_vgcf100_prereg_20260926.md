# 사전등록 — Phase A 재현 런: VGCF E **100 GPa** 104 팔 + 같은 기계 **10 GPa 대조** 32 팔 · 짝 비교 (2026-09-26)

> 비준 = 사용자 09-26 밤 (*"104팔 다시 돌리지뭐 · 이참에 vgcf 10gpa, 100gpa일떄 차이가 얼마나 나는지도 보면 좋으니까"* · 대조군 32 팔 ✓ · v100 분담 ✓).
> 계기 = 원장 `CL-93` (10 GPa 는 출처 없는 06-24 모델 선택값) → 기본값 100 GPa (`8f3472c2f`, 세대 `ADD_E_SET_20260926`).
> 상태: ⬜ 등록 (런 전).  판정선 §4 는 결과를 보고 옮기지 않는다.  원판 = `docs/data/phase_a_104arms_20260921/` (ORDER-ROBUST, 09-21).
> 레시피 추출 기록 (에이전트 · 파일:행 전수) = 세션 스크래치 초안 (리포 밖 · 커밋되지 않음) — 아래 §1 표가 그 요지이고, 근거 파일:행은 표에 적었다.

## 0. 질문 셋 (estimand)

1. **재현**: VGCF E 만 100 GPa 로 바꾼 채 같은 판정기를 돌리면 조성 순서 판정이 다시 **ORDER-ROBUST** 인가.
2. **E 효과 (짝)**: 같은 기계 · 같은 코드에서 100 GPa 와 10 GPa 로 압밀한 침대의 σ_e 를 (조성 · 격자 · origin) 짝으로 비교하면 얼마나 다른가.
3. **재현 잡음**: 같은 10 GPa 를 다른 기계 (kgy) 에서 다시 압밀하면 09-21 원판 (v100) 과 얼마나 다른가 — 2 의 눈금.

σ_e **절대값** · 격자 수렴 · 하한 서술은 여전히 답하지 않는다 (`CL-41` · `CL-72`).

## 1. 바뀌는 것 하나 — 나머지는 09-21 레시피 그대로 (봉인)

| 축 | 값 (변경 없음) | 근거 |
|---|---|---|
| 킷 | `docs/data/phase_a_6mah/kits/VGCF_PTFE_{1,2,3,4}_1/{run_mpm.sh,mpm_input.json}` + 공유 스캐폴드 `docs/data/phase_a_6mah/{am,se}_scaffold.csv.gz` (am sha256 앞 16 자리 `3c76ec09f5da0bc7` — 원판 팔 전부와 같다) | 원판 README · 레시피 §1 |
| STEP2 | `run_mpm.sh` 그대로: `--periodic --lateral-box 0.050013 --n-grid 256 --protocol hold --frames 2500 --platen-mach 0.03 --allow-fast-platen --e-se 1.53 --nu-se 0.49 --target-gpa 0.3 --seed 3 --add-recipe VGCF:PTFE=w:1 --add-l-cv 0.4 --mixing thinky --coh-ptfe 0.10 --binder-opt-wt 1.5 --add-rng-per-phase --fibre-buckle --fibre-align a --dilate-z λ` (1_1 0.655/1.0214 · 2_1 0.661/1.0519 · 3_1 0.666/1.0798 · 4_1 0.67/1.1085) | K:77, 88-94, 103 |
| **VGCF E** | **100 GPa** (코드 기본, 태그 `ADD_E_SET_20260926_VGCF100GPa`) · 대조군 **10 GPa** (`--add-e-override VGCF=10`, 태그 `ADD_E_SET_20260926+override:VGCF=10.0GPa`) · 원판 = 10 GPa (`ADD_E_SET_20260818_9.0GPa`) | `mpm3d_compaction.py` ADD_E_NU · `CL-93` |
| STEP3 | `scripts/sdcp_gain_vox015_8arm.sh` · `PTFE_STAMP=centerline LEAN=2 BRIDGE_UM=0.24 ARMS=8 EXPECT_BACKEND=gpu` · VOX 0.15 / 0.20 / 0.25 · σ_VGCF 복셀 78.5398 / 44.1786 / 28.2743 · origin {0, vox/2}³ 8 팔 · **새 OUTDIR** (SKIP 캐시) · `physics_protocol_id` 가 원판 **`p2-79ade1a5c2b0c9fb`** 와 같아야 한다 (09-25 E 민감도 팔에서 확인된 값) | 레시피 §2 · §6 |
| QC | VGCF 1 wt% · vox 0.15 · origin 0–7 을 같은 침대 · 같은 코드로 **다시** 돌린 8 팔 (`--role qc`) · exact replay ≤ δ_num | 원판 §3 |
| 어댑터 · 판정기 | `phase_a_arms_from_payload.py` (code_sha 있음 → `--code-sha-missing-ok` **주지 않는다**) · `phase_a_order_verdict.py` (δ_num 0.04 % · 72/72 · QC 8/8) — **변경 없음** | 레시피 §4 |
| 짝 키 | (vgcf_wt, vox, origin) — `input_digest` · `n_dof` 는 세대에 따라 달라지므로 짝 키로 쓰지 않는다 | 레시피 §6 |
| 코드 | 이 리포 HEAD (clean tree — `CL-75`: dirty 팔은 인용 불가).  SELF-50 수정 (dt_effective 기록) 포함 | `248fd9516` |

## 2. 팔 설계 · 기계

| 세대 | STEP2 (침대) | STEP3 | 기계 | 비고 |
|---|---|---|---|---|
| **G100** (E 100) | 4 (1_1 · 2_1 · 3_1 · 4_1) | vox 0.15 · 0.20 · 0.25 × 4 킷 × 8 origin = **96** + QC **8** | **kgy** | 원판과 같은 팔 구성 |
| **G010** (E 10 대조) | 4 (같은 킷, `--add-e-override VGCF=10`) | vox 0.15 × 4 × 8 = **32** | **kgy** | 짝 비교 (질문 2) 의 분모 · 질문 3 의 분자 |
| 원판 | (v100 09-14) | v015 32 (`arms_primary_v015_20260921/arms`) | — | 질문 3 의 분모 |

- 한 기계 (kgy) 에서 G100 · G010 을 같은 코드로 돌린다 — 질문 2 가 **기계 차를 포함하지 않게**.  원판은 v100 이라 질문 3 이 그 차를 잰다.
- 09-25 실측: kgy E=10 재압밀 vs v100 원판 (3_1 · v015 · o0) — σ_e **+0.064 %** (> δ_num 0.04 %), n_dof 49,256,267 vs 49,256,215.  ⇒ 비트 재현이 아니라 **재압밀은 잡음을 갖는다**; 그래서 대조군이 필요하다.
- v100 은 d_h 288 · ps45 (별도 사전등록) 를 맡는다.  kgy 가 밀리면 §8 로 vox 0.25 (또는 0.20) 32 팔을 v100 으로 옮긴다.

## 3. 예측 (런 전 — 근거 명시)

| # | 예측 | 근거 |
|---|---|---|
| P1 | G100 104 팔 판정 = **ORDER-ROBUST** (72/72 > δ_num · QC 8/8) | 원판 조성 증분 최소 **+103.6 %** ≫ E 효과 ≤ 0.25 % (SELF-50 · 3_1 민감도) |
| P2 | 짝 비교 G100/G010 (v015 32 짝): **max \|d\| ≤ 1.0 %** → h0 "E 는 2차 입력" | 3_1 v015 o0 에서 100 vs 10 = +0.25 % (E 민감도 §7-3) · 띠는 그 4 배 |
| P3 | 재현 잡음 G010(kgy)/원판(v100) 32 짝: **max \|d\| ≤ 0.5 %** | 한 팔 실측 +0.064 % · 띠는 그 8 배 |
| P4 | G100 침대 4 개 전부 목표 도달 (`porosity_at_target_pct` non-None) · `dt_effective` ≈ 1.35e-4 (CFL, 100 GPa) · G010 은 2.0e-4 | E 민감도 3_1 E=100 이 2500 프레임 안에 도달 (V:96) · SELF-50 |
| P5 | G100 vs G010 porosity 차 ≤ 0.3 %p (킷마다) | 3_1: 14.929 vs 14.889 (+0.04 %p) |

## 4. 판정선 (런 전 등록 — 도구가 그대로 구현)

| 질문 | 도구 | 규칙 | 결과 어휘 |
|---|---|---|---|
| 1 재현 | `phase_a_order_verdict.py --dir <104 팔> --out` (변경 없음) | δ_num 0.04 % · 72/72 · QC replay 8/8 ≤ δ_num · 어느 하나라도 아니면 HOLD (문턱 확대 금지) | ORDER-ROBUST / REVERSED / HOLD |
| 2 E 효과 | `phase_a_pair_e_arms.py --a G100_v015 --b G010_v015 --band-pct 1.0 --expect-pairs 32` (selftest 14/14) | max \|ln(σ₁₀₀/σ₁₀)\| ≤ ln(1.01) → **h0_secondary_input** · 초과 → **h1_e_matters** · 짝 ≠ 32 → HOLD | h0 / h1 / HOLD |
| 3 재현 잡음 | 같은 도구 `--a G010_v015(kgy) --b 원판 v015 --band-pct 0.5 --expect-pairs 32` | ≤ 0.5 % → "띠 안" · 초과 → **질문 2 의 E 효과는 (3) 을 넘는 부분만 서술** (E 와 기계·재압밀 잡음이 같은 크기면 E 효과라 부르지 않는다) | 띠 안 / 띠 밖 |
| STEP2 게이트 | `mpm_metrics.json` | 침대마다 `additives.VGCF.E_GPa` = 100 (G010: 10) · `E_anchor` 태그 일치 · `porosity_at_target_pct` non-None · `dt_effective` 기록 — 하나라도 아니면 그 침대의 팔은 **HOLD** (승격 금지) | — |
| 보고 규약 | — | 질문 2 · 3 의 값은 *"vox 0.15 · origin 8 · 4 조성"* 짝 통계로만 · 원고 Methods 의 입력값은 **이 세대 침대에 한해** 100 GPa · 원판 (10 GPa) 결과와 섞어 표를 만들지 않는다 (세대를 적는다) | — |

## 5. 도구 상태

- `scripts/phase_a_order_verdict.py` — 변경 없음.  `scripts/phase_a_pair_e_arms.py` — **신설** (순수 짝 비교 · 짝 누락 HOLD · ptfe_wt 불일치 거부 · selftest 14/14).
- `scripts/phase_a_arms_from_payload.py` · `phase_a_receipt_from_sh.py` — 변경 없음.  ⚠ code_sha 가 있으므로 `--code-sha-missing-ok` 를 주면 어댑터가 **거부**한다 (adapter:344-347).
- `scripts/mpm3d_compaction.py` — VGCF 100 기본 (`8f3472c2f`) · dt 기록 (`248fd9516`) · selftest 154/154.

## 6. kgy 실행 명령 (순서대로 · 각 단계의 확인이 초록일 때만 다음으로)

```bash
# ── 0. 코드 · 환경 ──────────────────────────────────────────────────────────
cd ~/dem-vgcfE && git fetch origin claude/stoic-knuth-NObVQ && git checkout claude/stoic-knuth-NObVQ && git pull --ff-only
git status --short          # 비어 있어야 (CL-75) · git rev-parse --short HEAD 를 적어 둔다
conda activate ti310
python3 scripts/mpm3d_compaction.py --selftest | tail -1        # 154/154 PASS
python3 -c "import scripts.mpm3d_compaction as m" 2>/dev/null; python3 - <<'EOF'
import sys; sys.path.insert(0, 'scripts'); import mpm3d_compaction as m
print(m.ADD_E_NU['VGCF'], m.E_ANCHOR_TAG)                      # (100.0, 0.3) ADD_E_SET_20260926_VGCF100GPa
EOF
nvidia-smi --query-gpu=memory.used,memory.total --format=csv    # 남의 작업이 크면 STEP2 (--gpu-mem 20) 가 못 든다

# ── 1. 킷 8 개 (리포에서 · 두 세대 · 스캐폴드는 공유 gz 를 푼다) ──────────────
for gen in pa100 pa010; do for k in 1_1 2_1 3_1 4_1; do
  d=~/$gen/kits/VGCF_PTFE_$k; mkdir -p "$d"
  cp ~/dem-vgcfE/docs/data/phase_a_6mah/kits/VGCF_PTFE_$k/{run_mpm.sh,mpm_input.json,harvest.sh} "$d"/
  gunzip -c ~/dem-vgcfE/docs/data/phase_a_6mah/am_scaffold.csv.gz > "$d/am_scaffold.csv"
  gunzip -c ~/dem-vgcfE/docs/data/phase_a_6mah/se_scaffold.csv.gz > "$d/se_scaffold.csv"
done; ln -sfn ~/dem-vgcfE/scripts ~/$gen/kits/scripts; done
sha256sum ~/pa100/kits/VGCF_PTFE_1_1/am_scaffold.csv | cut -c1-16                  # 3c76ec09f5da0bc7
# 대조군: mpm3d 호출 한 줄에만 --add-e-override VGCF=10 (킷마다 정확히 1 곳)
for k in 1_1 2_1 3_1 4_1; do f=~/pa010/kits/VGCF_PTFE_$k/run_mpm.sh
  sed -i 's|--add-rng-per-phase --fibre-buckle|--add-rng-per-phase --add-e-override VGCF=10 --fibre-buckle|' "$f"
  echo "$k $(grep -c 'add-e-override VGCF=10' "$f")"; done                              # 전부 1 · 아니면 중단
grep -c 'add-e-override' ~/pa100/kits/VGCF_PTFE_*_1/run_mpm.sh                        # 전부 0

# ── 2. STEP2 8 침대 (한 GPU = 한 런 · 순차 · SSH 끊겨도 살게) ─────────────────
cat > ~/pa_step2.sh <<'EOF'
for gen in pa100 pa010; do for k in 1_1 2_1 3_1 4_1; do
  d=~/$gen/kits/VGCF_PTFE_$k
  [ -f "$d/latest_run/mpm_done.marker" ] && { echo "skip $gen $k (done)"; continue; }
  ( cd "$d" && MPM_NO_VENV=1 MPM_NO_PULL=1 bash run_mpm.sh )
  until [ -f "$d/latest_run/mpm_done.marker" ]; do sleep 60; done
  echo "done $gen $k $(date)"
done; done
EOF
setsid nohup bash ~/pa_step2.sh > ~/pa_step2.log 2>&1 &
# 확인 (침대마다): E · 태그 · 목표 도달 · dt
for gen in pa100 pa010; do for k in 1_1 2_1 3_1 4_1; do python3 - "$gen" "$k" <<'EOF'
import json, sys, os
gen, k = sys.argv[1:]; m = json.load(open(os.path.expanduser(f'~/{gen}/kits/VGCF_PTFE_{k}/latest_run/mpm_metrics.json')))
v = (m.get('additives') or {}).get('VGCF') or {}
print(gen, k, 'E', v.get('E_GPa'), v.get('E_anchor'), 'por@target', m.get('porosity_at_target_pct'),
      'dt_eff', m.get('dt_effective'), 'cfl', m.get('dt_cfl_limited'), 'por', m.get('porosity_sphere'))
EOF
done; done
# 기대: pa100 → E 100.0 ADD_E_SET_20260926_VGCF100GPa · dt_eff ≈ 1.347e-4 · cfl True ;  pa010 → E 10.0 …+override:VGCF=10.0GPa · dt_eff 2.0e-4
#       por@target 가 None 인 침대가 있으면 그 침대는 HOLD (§4) — 프레임 부족 → 보고 후 결정

# ── 3. STEP3 (러너 · 새 OUTDIR · 격자당 순차) ──────────────────────────────
KITS4="VGCF_PTFE_1_1 VGCF_PTFE_2_1 VGCF_PTFE_3_1 VGCF_PTFE_4_1"
cd ~/pa100/kits && for v in 0.15 0.20 0.25; do
  KITS="$KITS4" VOX=$v BRIDGE_UM=0.24 PTFE_STAMP=centerline LEAN=2 ARMS=8 EXPECT_BACKEND=gpu \
  OUTDIR=~/pa100/phaseA_v0${v#0.}_$(date +%Y%m%d) bash scripts/sdcp_gain_vox015_8arm.sh > ~/pa100/step3_v0${v#0.}.log 2>&1
done      # ← 이 세 줄은 setsid nohup bash -c '…' 로 감싸 띄운다 (v015 → v020 → v025 순차)
# QC 8 (v015 끝난 뒤 · 같은 침대 · 같은 코드 · 다른 OUTDIR)
cd ~/pa100/kits && KITS="VGCF_PTFE_1_1" VOX=0.15 BRIDGE_UM=0.24 PTFE_STAMP=centerline LEAN=2 ARMS=8 EXPECT_BACKEND=gpu \
  OUTDIR=~/pa100/phaseA_qc_v015_$(date +%Y%m%d) bash scripts/sdcp_gain_vox015_8arm.sh > ~/pa100/step3_qc.log 2>&1
# 대조군 v015
cd ~/pa010/kits && KITS="$KITS4" VOX=0.15 BRIDGE_UM=0.24 PTFE_STAMP=centerline LEAN=2 ARMS=8 EXPECT_BACKEND=gpu \
  OUTDIR=~/pa010/phaseA_v015_$(date +%Y%m%d) bash scripts/sdcp_gain_vox015_8arm.sh > ~/pa010/step3_v015.log 2>&1
# 팔마다 확인: physics_protocol_id 가 p2-79ade1a5c2b0c9fb · cg_info 0
python3 - <<'EOF'
import json, glob, os
for p in sorted(glob.glob(os.path.expanduser('~/pa100/phaseA_v015_*/p2_*.json')))[:3]:
    d = json.load(open(p)); m = d.get('step3', d).get('manifest', {})
    print(os.path.basename(p), m.get('physics_protocol_id'), m.get('ptfe_stamp'), (d.get('additive_E_GPa') or m.get('additive_E_GPa')))
EOF

# ── 4. 영수증 · 어댑터 · 판정 (OUTDIR 마다) ────────────────────────────────
SHA=$(git -C ~/dem-vgcfE rev-parse HEAD)
for O in ~/pa100/phaseA_v015_* ~/pa100/phaseA_v020_* ~/pa100/phaseA_v025_* ~/pa010/phaseA_v015_*; do
  mkdir -p "$O/sh"; find ~/pa100/kits ~/pa010/kits -path '*/latest_run/*' -name 'p2_*.sh' -newer "$O" -exec cp {} "$O/sh/" \; 2>/dev/null
  python3 ~/dem-vgcfE/scripts/phase_a_receipt_from_sh.py --sh "$O/sh" --out "$O" --logs "$O" --code-sha "$SHA" --expect-arms 32
  python3 ~/dem-vgcfE/scripts/phase_a_arms_from_payload.py --dir "$O" --out "${O}_arms"
done
#   ⚠ 러너가 팔 .sh · 로그를 어디에 쓰는지 (latest_run 안 / OUTDIR 안) 는 첫 격자에서 ls 로 확인하고 --sh · --logs 를 맞춘다.
python3 ~/dem-vgcfE/scripts/phase_a_arms_from_payload.py --dir ~/pa100/phaseA_qc_v015_* --out ~/pa100/phaseA_qc_v015_arms --role qc
mkdir -p ~/pa100/verdict_dir && cp ~/pa100/phaseA_v0{15,20,25}_*_arms/*.json ~/pa100/phaseA_qc_v015_arms/*.json ~/pa100/verdict_dir/
ls ~/pa100/verdict_dir | wc -l                                                          # 104
python3 ~/dem-vgcfE/scripts/phase_a_order_verdict.py --dir ~/pa100/verdict_dir --out ~/pa100/verdict_G100.json      # 질문 1
python3 ~/dem-vgcfE/scripts/phase_a_pair_e_arms.py --a ~/pa100/phaseA_v015_*_arms --b ~/pa010/phaseA_v015_*_arms \
  --label-a E100 --label-b E010 --band-pct 1.0 --expect-pairs 32 --out ~/pa100/pair_E100_E010.json                 # 질문 2
python3 ~/dem-vgcfE/scripts/phase_a_pair_e_arms.py --a ~/pa010/phaseA_v015_*_arms \
  --b ~/dem-vgcfE/docs/data/phase_a_104arms_20260921/arms_primary_v015_20260921/arms \
  --label-a E010_kgy --label-b E010_v100_0921 --band-pct 0.5 --expect-pairs 32 --out ~/pa100/pair_E010_vs_0921.json  # 질문 3
```
산출물 (팔 JSON · 영수증 · verdict · pair JSON · 침대 `mpm_metrics.json` 8 개) 을 `docs/data/phase_a_rep100_2026MMDD/` 로 커밋한다 (원판 README 형식).

## 7. 시간 (실측 근거 · kgy 3090)

STEP2 ≈ 1 h/침대 × 8 = 8 h · STEP3 vox 0.15 ≈ 42 min/팔 × 64 (G100 32 + G010 32) ≈ 45 h · vox 0.20 (kgy 미실측; v100 전체 파이프라인 42 min) ≈ 20 h ·
vox 0.25 (v100 23 min) ≈ 12 h · QC 8 ≈ 6 h ⇒ **≈ 90 h ≈ 4 일** (kgy 단독).  남의 GPU 작업이 있으면 더.

## 8. (선택) v100 분담 — kgy 가 밀릴 때

vox 0.25 (또는 0.20) 32 팔을 v100 으로: 침대 4 개의 `latest_run` 폴더 (se_dump.npy ≈ 815 MB · phase.npy · fibre*.npy · mpm_metrics.json · mpm_payload.json)
와 킷 (스캐폴드 · run_mpm.sh) 을 같은 상대 경로로 rsync 하고 `latest_run` 심링크를 다시 건다 → v100 `venv` 에서 같은 러너 명령 (§6-3) 을 새 OUTDIR 로.
⚠ 같은 팔을 두 기계에서 돌리지 않는다 (격자 단위로 나눈다) · `input_digest` 는 침대 파일 내용만 덮으므로 복사본은 원본과 같은 digest 를 낸다.

## 9. 결과 (런 뒤 — §4 불변)

(비어 있음)
