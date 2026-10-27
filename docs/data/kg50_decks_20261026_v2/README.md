# 50kg/batch 4차년도 — SE 입도 비교 DEM 덱 v2 (10-26 밤 · Codex HOLD 수정판)

- 옛 판 `docs/data/kg50_decks_20261026/` (커밋 `3056eef12` · Codex 검토 대상) 은 **쓰지 않는다** — 이 v2 로 대체.
- 생성기 `scripts/make_se_size_decks.py` (selftest 87/87) · 기준 덱 `docs/data/phase_a_6mah/in.real_4.liggghts` · 판정문 `docs/reviews/codex_kg50_decks_review_20261026/codex_review_kg50_decks_20261026.md` · 고칠 계획 `docs/50kg/kg50_fix_plan_20261026.md` (1저자 10-26 밤 *"50kg 권고대로해"* = Q1–Q7 권고).
- 다시 만들기: `python3 scripts/make_se_size_decks.py --preset kg50y4 --out <빈 폴더> --ibb-runner docs/data/pure_se_r075_20260927/run_pse_r075_a_r30.sh --ntasks kg50_d07_b40:56,kg50_d2_b40:4` (같은 바이트 · `manifest.json` sha256).

## 1. v1 → v2 바뀐 것

| Q | 원장 | 바뀐 것 |
|---|---|---|
| Q1 | KG50-01 · 09 · 10 | 속도 시험 덱 없앰 · 비교 침대 전부 NP 1 삽입 — D3 칸 비교 여섯 = 처음부터 끝까지 NP 1 / D0.7 · D1 · D2 = 삽입 전용 덱 (본 덱의 정착 run 앞까지 그대로 + `run 20000` + `write_restart …restart_settling_20001.bin` + `run 3000`) → 재개 · 본 덱에 step 1 체크포인트 없음 |
| Q3 | KG50-06 | skin = 템플릿 2 µm 그대로 (속도 시험 없음) · NP 는 본 런 재개 시험 실측 |
| Q4 | KG50-03 · 11 | 마지막 step: `write_restart restart_<case>/restart_end.bin` → atom · contact · mesh 한 장씩 (간격 1 · `run 0`) · `unfix move_press` 바로 뒤 `restart 0` (이완 중 체크포인트 끔) |
| Q6 | KG50-07 · 08 · 13 · 14 | 정수 구간 (ceil · floor) — AM 948 → 944–952 · 1,481 → 1474–1488 · SE 수 검사 추가 · SELF-70 문장 = "부족 또는 초과" · D3 시드 1 이름 `_s1` |
| Q7 | KG50-12 | 기준 덱 줄 대조 (선언 자리 밖 변경 = 생성 거부) — 반례 일곱 (판 속도 · 감쇠 · dt · 중력 · 이웃 재구축 · 체적분율 · 목표 압력) 전부 잡음 |
| Q2 | KG50-02 · 10 · 14 | 재개 도구 `scripts/resume_ckpt.sh` 고침 (10-26 밤 `d1b34664c`) — 본 제출 = 시험 COMPLETED · ExitCode 0:0 · 기대 끝 step · Loop time (G0) ∧ G1–G3 · 원 로그 비교 줄 결손 = 실패 · 재개 덱 정적 대조 (재삽입 · 물리 줄 · 재개 지점 상태 · 남은 step · 뒤 순서) · 큐 이름 정확 일치 · `-T` 시험만 · 시험 `scripts/test_resume_ckpt.py` 32/32 |
| — | KG50-04 | **아직** — D0.7 dt · 감쇠 대조 (Q5) = 결과 전 등록 뒤 |

## 2. 1 단계 — 지금 (hit · D3 칸 비교 여섯 · 각 NP 1 · 재개 없음)

hit 주소는 1저자 (리포에 적지 않는다).  런마다 1 코어 · 여섯 = 6 코어 · 추정 5–13 h.

```bash
# WSL → hit
cd ~/Yonghoon-DEM-DFT && git pull
for n in kg50_d3_b40_s1 kg50_d3_b50_s1 kg50_d3_b40_s2 kg50_d3_b40_s3 kg50_d3_b50_s2 kg50_d3_b50_s3; do
  scp -r docs/data/kg50_decks_20261026_v2/$n <사용자>@<hit>:~/simulation/
done
# hit
cd $HOME/simulation/kg50_d3_b40_s1 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b40_s1.liggghts > log_kg50_d3_b40_s1_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b50_s1 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b50_s1.liggghts > log_kg50_d3_b50_s1_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b40_s2 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b40_s2.liggghts > log_kg50_d3_b40_s2_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b40_s3 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b40_s3.liggghts > log_kg50_d3_b40_s3_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b50_s2 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b50_s2.liggghts > log_kg50_d3_b50_s2_v1.out 2>&1 < /dev/null &
cd $HOME/simulation/kg50_d3_b50_s3 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d3_b50_s3.liggghts > log_kg50_d3_b50_s3_v1.out 2>&1 < /dev/null &
# 삽입 직후 확인 — 세 검사 줄 (INSERTED · AM · SE) 과 FATAL 없음 · LIGGGHTS 판 (빌드 신원 · KG50-15)
grep -hE "INSERTED|====== (AM|SE)|FATAL" ~/simulation/kg50_d3_*/log.liggghts
head -2 ~/simulation/kg50_d3_b40_s1/log.liggghts
# 끝난 뒤 — 끝 상태 출력 네 개 (restart_end · atom_end · contact_end · mesh_end) 가 생겼는지
ls ~/simulation/kg50_d3_*/restart_kg50_d3_*/restart_end.bin ~/simulation/kg50_d3_*/post_kg50_d3_*/*_end_*
```

## 3. 칸 판정 기준 (결과 전 고정 · 1저자 10-26 밤 Q6)

- 측정 프레임 = 끝 상태 (`atom_end` · `contact_end` · `mesh_end`) · 웹앱 파이프라인 같은 판 · 같은 규약.
- 지표 넷 · 문턱: porosity (ε_sphere) 0.5 %p · AM coverage 1 %p · 수송 tortuosity 5 % · σ_ion 5 % (상대 차 분모 = 50×50 평균).
- 판정: 40 · 50 각 시드 3 의 평균 차 |Δ| 와 SE_Δ = √(s40²/3 + s50²/3).
  - |Δ| ≤ 문턱 이고 SE_Δ ≤ 문턱 → **"D3 등록 지표 평균 차 기준 통과"** → D0.7 · D1 · D2 를 40×40 으로 (그 영역을 채택한 **탐색 비교** — 영역 수렴 주장 아님).
  - |Δ| > 문턱 → 불합격 → 50×50 (`--fallback50`).
  - SE_Δ > 문턱 · 지표 비유한 · 비관통 → **판정 불가** (1저자 결정).
- 본 비교 (D0.7 · D1 · D2 · D3 시드 1) 는 시드 하나 — D3 의 산포를 그 셋의 오차막대로 쓰지 않는다.
- ★ 10-27 (결과 전 — hit 여섯 압밀 끝 · 지표 값 열람 전) **판정 모드 = Hertz** (1저자 *"이종기술때처럼 hertz로 하는게 맞는듯"*) — σ_ion = 솔버 Hertz σ FULL (`network_conductivity_dual.json` `hertzian.sigma_full_mScm` · 상태 computed) · 수송 tortuosity = `tau2_ion_hertz` (`tau_flux.case_row` · 상태 OK) · porosity = 웹앱 `porosity` (ε_sphere = `porosity_spheresum`).
- ★ 10-27 (결과 전) **AM coverage = Physics · Hertz 둘 다 판정** (1저자 *"am coverage는 physics로 봤잖아 / 같이 봐"*) — Physics = `coverage_<AM>_mean_physics_union` (합집합 cap · 웹앱 표 Physics 열 · `coverage_status_physics_union` = ok 만) · Hertz = `coverage_<AM>_mean` (LIGGGHTS 접촉 면적) · 둘 다 문턱 1 %p · 지표 다섯.
- ★ 10-27 판정 순서 (지표마다 · 위에서 먼저 걸리는 것 · ✅ **1저자 10-27 권고대로 · 결과 전**): ① 여섯 값 중 비유한 · 상태 미달 (비관통 · 풀이 실패) → 판정 불가 ② SE_Δ = √(s40²/3 + s50²/3) > 문턱 → 판정 불가 ③ |Δ| > 문턱 → 불합격 ④ 그 밖 → 통과 (|Δ| = 문턱 은 통과).  전체 = 하나라도 불합격 → 불합격 · 아니고 하나라도 판정 불가 → 판정 불가 · 넷 다 통과 → 통과.  여섯의 망 코드 판 (`network_provenance.json` `code_sha`) 이 같아야 한다 (다르면 판정 없음).
- 판독기 `scripts/kg50_d3_cell_verdict.py` (읽기 전용 · 값 새로 계산 안 함 · selftest 첫 항목 = 이 절의 문턱 · 모드 · SE_Δ 식 대조 · 게이트 상주) — WSL: `python3 scripts/kg50_d3_cell_verdict.py --json <판정 기록.json>` (웹앱 케이스 이름 = 침대 이름 `kg50_d3_b40_s1` …).
- ★ 10-27 결과 = **불합격** — 수송 tortuosity +7.62 % · σ_ion −6.84 % (문턱 5 %) · porosity · AM coverage Physics · Hertz 통과 → 50×50 (1저자 *"50 50으로 하자 어쩔 수 없네"*) · 기록 `docs/data/kg50_d3_cell_verdict_20261027/` · 덱 v3 `docs/data/kg50_decks_20261027_v3_b50/` · 이 폴더의 40×40 비교 셋 (D0.7 · D1 · D2) 은 쓰지 않는다 · 작은 SE 의 40×40 은 재지 않았다 (1저자 *"시간 없는게 문제네"*).

## 4. 2 단계 — 칸 판정 · 재개 도구 고침 · Q5 등록 뒤 (1저자 승인 뒤)

- D0.7-40 (ibb): `sbatch kg50_d07_b40/run_kg50_d07_b40_insert.sh` (NP 1 · 삽입 + 정착 20,000 + 3,000 step) → 끝나면 고친 `resume_ckpt.sh` (`d1b34664c` 이후 · ibb 의 사본도 그 판으로) 로 step 20001 에서 재개 — NP 를 정하려면 먼저 `-T` (시험만 · 2,000 step) 로 속도를 보고 같은 명령을 `-T` 없이 (NP = 재개 시험 실측) → 정착 끝 (after_settling) 에서 Q5 dt · 감쇠 대조 → 압축.
- D1-40 (hit 20 코어): `cd $HOME/simulation/kg50_d1_b40 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d1_b40_insert.liggghts > log_kg50_d1_b40_ins.out 2>&1 < /dev/null &` → 끝나면 1저자 `hit_resume.sh` 로 20 코어.
- D2-40 (ibb): `sbatch kg50_d2_b40/run_kg50_d2_b40_insert.sh` (NP 1) → 재개 NP 4.
- ⛔ `run_kg50_d07_b40.sh` · `run_kg50_d2_b40.sh` (본 러너) 를 **처음부터 직접 sbatch 하지 않는다** — 고코어 fresh 삽입은 기하적으로 불가능하다 (KG50-01).  재개 도구가 쓰는 러너다.

## 5. 한계

- 언로딩 없음 · gen-1 프로토콜 · 단분산 SE · 본 비교 시드 하나.
- 감쇠 `fix damp all viscous 0.5` = 모든 입자에 같은 γ — γ/m 이 SE 크기에 따라 다르다 (D0.7 ↔ D3 ≈ 79 배) → Q5 대조 결과 전에는 크기 비교에 감쇠 교란이 섞여 있을 수 있다.
- 접촉 법칙의 크기 닮음 (hooke k ∝ R) 은 모든 입자를 함께 닮게 키울 때의 유도 — AM 을 고정하고 SE 만 바꾸는 이 비교에서 겹침 불변까지 보증하지 않는다 ("같은 물성 · 같은 gen-1 규약을 비교에 사용" 으로 한정).
- 실제 미세 분말의 응집 (크기 의존) 은 모델에 없다.
- 2차년도 표의 Young's modulus SE 22 GPa = 재료값 — DEM 입력 = 유효 1.35 GPa.
- 시간 = 추정 (D3 5–13 h · D0.7-40 압축 1.5–3 일) — 첫 실측 = D0.7 재개 시험.
