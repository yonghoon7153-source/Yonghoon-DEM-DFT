# LHS 보충 침대 20 + 후막 짝 8 — 실행 등록 (2026-10-06 밤)

- 1저자 결정 (10-06 밤 · ML 피드백 표 회신): *"3번은 LU 들어오면 a6 끊고 바로 들어가고 4는 아까 계획한 부분에 추가로 넣어봐"* ·
  후막 = *"6~8"* mAh/cm² · 목적 = *"후막에서의 파라미터가 면용량 낮을 때랑 같냐"*.
- 설계 = `docs/data/lhs_supp_design_20261006.csv` (28 행 · sha256 `26f33fddcfe618ee19659d94630d6ef24a0463eeb1455fd2ef921d131a9162e3`) ·
  보고 `docs/data/lhs_supp_design_20261006.json` · 생성기 `scripts/lhs_supp_design.py` (selftest · `--verify` · 게이트 등록).
- 덱 = `scripts/lhs_ext_materialize.py --points` (64 확장과 같은 실물 템플릿 외과 치환 + 행별 삽입 높이 · 코어 수 · 왕복검사).
- ⚠ 이 등록은 **DEM (LIGGGHTS) 런**만 다룬다.  접촉망 (σ · f · 수송 tortuosity) 계산은 Codex 세대 2 판정
  (`docs/reviews/codex_review_gen2_network_20261006.md` · HOLD) 의 해제 뒤 같은 코드로 한다.

## 1. 무엇을 돌리나

| 묶음 | 행 | 규약 | 입자 수 (추정) | 코어 |
|---|---|---|---|---|
| ③ 보충 `lhss_001`–`020` | 20 | 설계 3 축 (큰 AM 비율 · SE wt% · SE 지름) 의 빈 곳을 maximin 으로 · 나머지 노브 (AM 반지름 · SE-rich 의 volfrac) 는 층화 추첨 | 4,127–114,494 | 1 (n > 10 만 셋은 2) |
| ④ 후막 `lhst_<짝>_6m · _8m` | 8 | 짝 = 130 의 2 mAh 침대 넷 (`lhs00_078` AM 75 · `036` AM 80 · `045` AM 85 · `008` AM 90 — 관통 · 굴곡 3.1 → 22) · **같은 조성 · 반지름 · volfrac** · 삽입 높이만 ×3 · ×4 · 새 seed | 17,181–81,216 | 2–4 |

- 코어 합 **43** (qos cpu-60 = 60) — LU 두 런 (40 코어) 이 끝나고 a6 를 끊으면 한 번에 들어간다.
- 빈 곳 (가장 가까운 침대까지 정규화 거리 > 0.2 인 설계 공간 비율 · 시뮬 가능 영역 안): **9.3 % → 1.6 %**.
  (10-06 보고의 13.3 % → 1.5 % 는 시뮬 가능 여부를 안 가린 정육면체 전체 기준이었다 — 이번 수가 정본.)
- 시뮬 가능 범위 (1저자 — *"반지름을 작게 만드는건 안돼"*): SE 지름 ≥ 1.0 µm · 총 입자 수 ≤ 이미 돈 최대 114,609 (194 의 `n_total_est`).
  이 범위에서 한계 구역 = 0 % (가장 유리한 반지름 · volfrac 로 모든 칸이 상한 안) — 상한을 넘은 보충 점 둘은 volfrac 를 상자 안에서 낮춰 맞췄다 (`cap_adjust=volfrac`).

## 2. 규약 (이미 돈 것을 따른다)

- 2 mAh 규칙: `volfrac = L / (C · φ_AM,solid)` · C = 12.768 (lhs00_000 실측 0.222984 · AM 85 wt%) — lhs00_110 (0.250627) · 상자 경계 (0.176428 · 0.317759) 재현 (selftest s1).
- SE > 30 wt% 는 2 mAh 를 넣을 수 없다 (volfrac > 0.318) → 64 확장처럼 volfrac 를 상자 안의 설계 축으로 (로딩 0.35–0.86 mAh/cm²).
- 후막: 2 mAh 템플릿 삽입 영역 z 0.005–0.138 (덱 단위 · ×1000 = µm) → 6 mAh 0.404 · 8 mAh 0.537 · 상자 위끝 1.0.
  침강 (중력 98.1 · 200 k step) 중 자유낙하 ≤ 105 k step.  압축 · 완화 단계는 그대로 (판이 목표 압력에서 멈춘다).

## 3. 계산량 (추정)

기준 = lhs00_000 (45,030 입자 · 2.42 M step · 43 h · 1 코어 · 08-29 기록) · 다중 코어 효율 0.8 가정 · 후막 step = 고정 0.5 M + (짝 실측 압축 step) × 배율.

| | 벽시계 추정 (h) |
|---|---|
| 보충 20 | 4.5–93 (중앙 ≈ 26) |
| 후막 6 mAh | 32–84 |
| 후막 8 mAh | 56–100 |

⚠ 러너 시간 제한 5 일 (템플릿) 안이지만 추정이다 — TIMEOUT 이면 `scripts/resume_ckpt.sh` 로 재개 (체크리스트 ①–⑥).
⚠ 08-29 의 43 h 가 완주 시간인지는 기록에서 확인 못 했다 → 첫 완주 런의 `sacct` 경과 시간으로 고친다.

## 4. 실행 (WSL 에서 덱 → ibb 제출)

```bash
# WSL — 리포 사본 (~/dem-web) 을 이 커밋으로 맞춘 뒤
cd ~/dem-web && git fetch origin claude/stoic-knuth-NObVQ && git checkout <이 커밋>
python3 scripts/lhs_supp_design.py --verify docs/data/lhs_supp_design_20261006.csv \
  --expect-sha256 26f33fddcfe618ee19659d94630d6ef24a0463eeb1455fd2ef921d131a9162e3
python3 scripts/lhs_ext_materialize.py --points \
  --design docs/data/lhs_supp_design_20261006.csv \
  --expect-sha256 26f33fddcfe618ee19659d94630d6ef24a0463eeb1455fd2ef921d131a9162e3 \
  --box docs/data/lhs_ext_box_v2_20260829.json \
  --template-3t ~/lhs_local/lhs00_000/input_lhs00_000.liggghts \
  --template-2t ~/lhs_local/lhs00_110/input_lhs00_110.liggghts \
  --template-run ~/lhs_local/lhs00_110/run_lhs00_110.sh \
  --outdir ~/lhs_supp_20261006            # 비어 있는 새 폴더 · 템플릿 해시가 상자 원장과 다르면 거부
tar czf ~/lhs_supp_20261006.tgz -C ~ lhs_supp_20261006
scp -P <포트> ~/lhs_supp_20261006.tgz <사용자>@<주소>:~/

# ibb — LU 두 런이 끝난 것을 squeue 로 확인 → a6 를 끊은 뒤
tar xzf ~/lhs_supp_20261006.tgz -C ~ && cd ~/lhs_supp_20261006
for d in lhss_* lhst_*; do (cd $d && mkdir -p logs && sbatch run_$d.sh); done
squeue -u $USER
```

성공 = 28 ID 전부 `COMPLETED` + 산출물 (`lhs_ext_submit_gate.py --manifest ~/lhs_supp_20261006/deck_manifest.json --sacct …`).
부분 성공은 없다 — 실패 ID 는 체크포인트로 재개하고, 처음부터 다시 돌리기는 보고 뒤.

## 5. 분석 계획 (기술 비교 — 판정선 없음)

- 수확 = 64 확장과 같은 길 (수확기 v3 · 웹앱 접촉 단계 · 기하면적 coverage) → 194 와 같은 열.
- ④ 짝 비교 (2 mAh ↔ 6 ↔ 8 mAh): porosity (union) · SE–SE CN · AM–SE CN · coverage (Hertz) · 관통 여부 · 기하학적 tortuosity (벽 기준) ·
  두께 방향 프로파일 (판 근처 층 vs 가운데).  차이는 **기술 보고** — 이 등록은 크기 판정선을 두지 않는다.
  씨앗 잡음 참고값 = 194 의 설계 → porosity GPR 추정 잡음 0.33 %p (2 mAh · 10-05 대조).
- 접촉망 열 (f · 수송 tortuosity) = 세대 2 HOLD 해제 뒤 · 같은 코드 · 194 와 같은 세대.
- ③ 보충 20 = 194 에 붙여 v1.3 이후 인계 (같은 열 사전 · 적격성 표지).
