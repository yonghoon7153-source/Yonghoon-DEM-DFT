> ⛔ **10-26 밤 — 이 판은 쓰지 않는다.**  Codex 검토 = HOLD (`docs/reviews/codex_kg50_decks_review_20261026/codex_review_kg50_decks_20261026.md`) · 수정판 = `docs/data/kg50_decks_20261026_v2/README.md`.  아래 1 단계 명령 (속도 시험 · D3 NP 3) 을 돌리지 않는다 — 고코어 삽입 불가 (KG50-01) · 이음매 (KG50-09).

# 50kg/batch 4차년도 — SE 입도 비교 DEM 덱 (10-26)

- 생성기 `scripts/make_se_size_decks.py` (selftest 81/81) · 기준 덱 `docs/data/phase_a_6mah/in.real_4.liggghts` (sha256 고정) · 계획 `docs/50kg/dem_plan_20261026.md` · 자체 검토 · Codex 요청 `docs/50kg/codex_kg50_decks_request_20261026.md`.
- 다시 만들기: `python3 scripts/make_se_size_decks.py --preset kg50y4 --out <빈 폴더> --ibb-runner docs/data/pure_se_r075_20260927/run_pse_r075_a_r30.sh --ntasks kg50_d07_b40:56,kg50_d2_b40:4` (같은 바이트 · `manifest.json` 의 sha256 로 대조).
- 조건 (1저자 10-26): 활물질 NCM D6 단일 85 wt% · 6.5 mAh/cm² (200 mAh/g) · 300 MPa · 진밀도 4.85 / 1.64 (`lab20261014`) · SE D50 0.7 / 1 / 2 / 3 µm · 시드 1 · 언로딩 없음 · 판 속도 0.01 mm/s · 재료 블록 = 기준 덱 바이트 그대로 (E AM 140 · SE 유효 1.35 GPa).
- 결정 Q1–Q6 (1저자 10-26 *"권고대로 해"*): Q1 삽입은 NP 1 (`input_<case>_insert.liggghts`) → `resume_ckpt.sh` 로 코어 늘림 + 활물질 수 검사 ±0.5 % · Q2 skin 속도 시험 (`speed/`) 뒤 결정 · Q3 atom 덤프 50,000 · Q4 압축 체크포인트 200,000 · Q5 D3 칸 비교 시드 3 · Q6 Codex 짧은 검토 + 그동안 D3 칸 비교 먼저.  D0.7-50 철회 (50×50 의 D0.7 · D1 · D2 = `--fallback50` · 40×40 불합격 때만).

## 1. 들어 있는 것

| 폴더 | 입자 (예상) | AM 계획 · 검사 | 쓰임 |
|---|---|---|---|
| `kg50_d07_b40` | 312,506 | 948 · 943–953 | 본 비교 (2 단계) |
| `kg50_d1_b40` | 107,813 | 948 · 943–953 | 본 비교 (2 단계) |
| `kg50_d2_b40` | 14,306 | 948 · 943–953 | 본 비교 (2 단계) |
| `kg50_d3_b40` · `_s2` · `_s3` | 4,906 | 948 · 943–953 | 칸 비교 40 (1 단계) · 시드 1 = 본 비교 D3 |
| `kg50_d3_b50` · `_s2` · `_s3` | 7,665 | 1,481 · 1473–1489 | 칸 비교 50 (1 단계) |
| `speed/kg50_spd_d07_b40_sk{20,05}_np{28,56}` | 312,506 | 검사 없음 | skin 2 · 0.5 µm 속도 시험 (1 단계 · 시간만) |

케이스 폴더마다 본 덱 `input_<case>.liggghts` · 삽입 전용 덱 `input_<case>_insert.liggghts` (본 덱의 step 1 체크포인트 줄까지 바이트 그대로 + `run 2000`) · ibb 삽입 러너 `run_<case>_insert.sh` (NP 1) · ibb 본 러너 `run_<case>.sh` (`kg50_d07_b40` NP 56 · `kg50_d2_b40` NP 4 만).

## 2. 1 단계 — 지금 (ibb 속도 시험 넷 ∥ hit D3 칸 비교 여섯)

ibb (주소 · 포트는 1저자 — 리포에 적지 않는다):

```bash
# WSL
cd ~/Yonghoon-DEM-DFT && git pull
for n in sk20_np28 sk05_np28 sk20_np56 sk05_np56; do
  scp -P <포트> -r docs/data/kg50_decks_20261026/speed/kg50_spd_d07_b40_$n <사용자>@<주소>:~/dem_test/
done
# ibb — 넷 다 제출 (qos 60 코어가 순서를 정한다: 28 둘 동시 → 56 하나씩)
cd ~/dem_test && mkdir -p logs
for n in sk20_np28 sk05_np28 sk20_np56 sk05_np56; do sbatch kg50_spd_d07_b40_$n/run_kg50_spd_d07_b40_$n.sh; done
# 끝나면 (각 수십 분 · 추정)
grep -H "Loop time" ~/dem_test/kg50_spd_d07_b40_*/log.liggghts
```

hit (각 NP 3 · 18 코어 · AM 검사는 NP 3 의 SELF-70 흔들림 ≤ 약 1–2 개라 통과 예상):

```bash
# WSL → hit
for n in kg50_d3_b40 kg50_d3_b50 kg50_d3_b40_s2 kg50_d3_b40_s3 kg50_d3_b50_s2 kg50_d3_b50_s3; do
  scp -r docs/data/kg50_decks_20261026/$n <사용자>@<hit>:~/simulation/
done
# hit
cd $HOME/simulation/kg50_d3_b40 && setsid nohup mpirun --oversubscribe --bind-to none -np 3 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b40.liggghts > log_kg50_d3_b40_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b50 && setsid nohup mpirun --oversubscribe --bind-to none -np 3 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b50.liggghts > log_kg50_d3_b50_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b40_s2 && setsid nohup mpirun --oversubscribe --bind-to none -np 3 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b40_s2.liggghts > log_kg50_d3_b40_s2_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b40_s3 && setsid nohup mpirun --oversubscribe --bind-to none -np 3 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b40_s3.liggghts > log_kg50_d3_b40_s3_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b50_s2 && setsid nohup mpirun --oversubscribe --bind-to none -np 3 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b50_s2.liggghts > log_kg50_d3_b50_s2_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b50_s3 && setsid nohup mpirun --oversubscribe --bind-to none -np 3 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b50_s3.liggghts > log_kg50_d3_b50_s3_v1.out 2>&1 < /dev/null &
# 첫 확인 (삽입 직후): 두 검사 줄
grep -hE "INSERTED|====== AM|FATAL" ~/simulation/kg50_d3_*/log.liggghts
```

## 3. 2 단계 — 속도 시험 · 칸 판정 · Codex 답 뒤 (1저자 승인 뒤)

- D0.7-40 (ibb): `sbatch kg50_d07_b40/run_kg50_d07_b40_insert.sh` (NP 1 · 삽입 + 2,000 step 에서 끝) → 끝나면 `mv ~/dem_test/kg50_d07_b40 ~/dem_test/kg50_d07_b40.ins1 && bash resume_ckpt.sh -n <NP> -s ins1 -r ~/dem_test kg50_d07_b40` (settling 모드 · 2,000 step 시험 G1–G3 통과 때만 본 제출 · NP = 속도 시험으로).
- D1-40 (hit 20 코어): `cd $HOME/simulation/kg50_d1_b40 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d1_b40_insert.liggghts > log_kg50_d1_b40_ins.out 2>&1 < /dev/null &` → 끝나면 1저자 `hit_resume.sh` 로 20 코어.
- D2-40 (ibb NP 4 · 바로): `sbatch kg50_d2_b40/run_kg50_d2_b40.sh` (NP 4 의 SELF-70 흔들림 ≤ 약 2 개 → 검사 통과 예상).
- skin 이 0.5 µm 로 정해지면 본 덱 넷을 같은 값으로 다시 생성 (이 폴더는 2 µm 판 그대로 두고 새 폴더).

## 4. 시간 (추정 · 첫 실측 = 속도 시험)

- step 수 ≈ 5–7 M (판 이동 ≈ 50–60 µm ÷ 0.01 mm/s + 정착 · 안정화 · 이완 0.5 M) — 근거 = 같은 계열 순수 SE r100 런의 판 접촉 뒤 압축 run 1,020 번 (= 5.1 M · CLAUDE.md 재개 체크리스트 ⑤).
- 입자당 비용 기준 1.42 µs/입자-step (`lhs00_000` 45,030 입자 · 2.42 M step · 43 h · 1 코어) · skin 2 µm 에서 SE 한 개 이웃 ≈ φ_SE·((2r+s)/r)³ = D0.7 138 · D1 65 · D2 19 · D3 11 · 40×40 을 56 코어로 나누면 칸 5.7×5 µm < 고스트 반경 8 µm.
- D3 2–4 h (NP 2–3) · D2 4–6 h (NP 4) · D1 ≈ 1 일 (NP 20) · D0.7-40 1.5–3 일 이상 (NP 40–60).  앞서 쓴 D0.7-40 10–14 h 는 3–5 배 낮았다 (철회).

## 5. 칸 판정 기준 (결과 전 · ⬜ 1저자 확인)

D3 40 · 50 각 시드 3 의 평균 차가 네 지표 모두 문턱 안이면 40×40 합격: porosity ≤ 0.5 %p · AM coverage ≤ 1 %p · 수송 tortuosity ≤ 5 % (상대) · σ_ion ≤ 5 % (상대).  시드 산포 (표준편차) 를 같이 적는다.  불합격이면 50×50 (`--fallback50`).

## 6. 한계

- 언로딩 없음 (끝 = 판 고정 이완) · gen-1 프로토콜 · 단일 시드 (본 비교) · 단분산 SE.
- 접촉 법칙이 크기에 비례 (hooke k ∝ R → 같은 압력에서 δ/R 같음) 라 SE 유효 E 를 네 크기에 그대로 쓴다 — 단 실제 미세 분말의 응집 (반데르발스 · 크기 의존) 은 모델에 없어 D0.7 이 실제보다 유리할 수 있다.
- 2차년도 표의 Young's modulus SE 22 GPa 는 재료값 — DEM 입력은 유효 1.35 GPa (같은 재료 블록).
