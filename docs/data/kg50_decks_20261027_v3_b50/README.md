# 50kg/batch 4차년도 — SE 입도 비교 DEM 덱 v3 (50×50 · 10-27)

- 왜: D3 칸 판정 = **불합격** (수송 지표 차 > 문턱 5 % · 판정 기록 = 별도 커밋) → 등록 (`docs/data/kg50_decks_20261026_v2/README.md` §3) 대로 비교 덱 D0.7 · D1 · D2 = **50×50** (`--fallback50`) · 1저자 10-27 *"50 50으로 하자"*.
- 이 폴더 = 새 덱 셋 (D0.7 · D1 · D2 의 50×50).  본 비교의 D3 자리 = v2 `kg50_d3_b50_s1` (hit 칸 비교에서 압밀 끝 · 여기 다시 만들지 않았다 — ⬜ 1저자 확인).  v2 의 40×40 비교 셋 (`kg50_d07_b40` · `kg50_d1_b40` · `kg50_d2_b40`) 은 쓰지 않는다.
- 다시 만들기: `python3 scripts/make_se_size_decks.py --preset kg50y4 --fallback50 --only kg50_d07_b50,kg50_d1_b50,kg50_d2_b50 --out <빈 폴더> --ibb-runner docs/data/pure_se_r075_20260927/run_pse_r075_a_r30.sh --ntasks kg50_d07_b50:56,kg50_d2_b50:4` (같은 바이트 · `manifest.json` sha256 · 생성기 sha256 `00d16e07…`).

## 1. v2 → v3 바뀐 것

| 무엇 | 바뀐 것 |
|---|---|
| 영역 | 50×50 µm (판 꼭짓점 · 압력 면적 0.0025) · 시드 슬롯 9 · 10 · 11 (40×40 셋 = 0 · 1 · 2 — 다른 침대) |
| 덱 머리 주석 | 3 · 9 행에 기준 덱 파일 이름 · 태그를 쓰지 않는다 — 기준 덱 = sha256 전체 + 폴더 `docs/data/phase_a_6mah/` (경로 전체 = `manifest.json` `template`) · ⑦ = "기준 덱의 케이스 태그 (소문자 24 곳 · 대문자 2 곳) → 케이스명".  계기 = 10-27 ibb `dem_restart.py` 가 v2 덱을 *"다른 케이스명 혼입: ['real_4']"* 로 거부 (D0.7-40 재개 계획 없음 · 실행 줄엔 없음) |
| 생성기 | 머리 주석 고침 + `build` 가 쓰기 전 생성 파일 어느 줄에든 (주석 포함) 다른 케이스명이 있으면 멈춤 · selftest 118/118 |
| 그 밖 | 같음 — 고치기 전 생성기 (`e65e92b7b`) 로 같은 세 케이스를 만들면 덱 여섯의 3 · 9 행 (줄 전체 주석) 만 다르고 실행 줄 · 러너 다섯 · `manifest.json` 기록이 같다 (sha256 값만 다름) |

## 2. 계획 입자 수 · 삽입 검사 (덱 안 · 밖이면 `quit 1`)

| 케이스 | SE D50 | AM 계획 | SE 계획 | 합 | 바닥 (99 %) | AM 정수 구간 | SE 정수 구간 | 예상 면용량 |
|---|---|---|---|---|---|---|---|---|
| `kg50_d07_b50` | 0.7 µm | 1,481 | 486,810 | 488,291 | 483,408 | 1474–1488 | 484376–489244 | 6.499 |
| `kg50_d1_b50` | 1 µm | 1,481 | 166,976 | 168,457 | 166,772 | 1474–1488 | 166142–167810 | 6.499 |
| `kg50_d2_b50` | 2 µm | 1,481 | 20,872 | 22,353 | 22,129 | 1474–1488 | 20768–20976 | 6.499 |

- 셋 다 AM D6 · 85:15 wt% · 삽입 높이 317.7 µm (z 0.322700) = 고체 두께 101.98 µm · 바닥 = `count(all)` 이 이 수보다 작으면 멈춤 · AM · SE = 계획 ±0.5 % (ceil · floor).
- PS-01 (`maxattempt` int32): 모든 덱 3,000 · 가장 큰 `kg50_d07_b50` = 488,291 × 3,000 = **1,464,873,000** < 2³¹/1.3 = 1,651,910,497 (비 0.887 · ×1.3 = 1,904,334,900 < 2,147,483,647) · 이 수에서 허용 상한 3,383 · 넘으면 생성기가 덱을 내지 않는다.
- 상별 수는 MPI 랭크마다 흔들린다 (SELF-70) → 삽입은 NP 1.  D0.7-50 입자 = 40×40 의 1.56 배 — 삽입 런 (NP 1 · 23,001 step) ≈ 7 h (추정 · 40×40 실측 4 h 40 m 의 선형).

## 3. 발사 명령 (명령만 · 아무것도 띄우지 않았다 · 1저자 승인 뒤)

```bash
# WSL → ibb (주소 · 포트 = 1저자 · 리포에 적지 않는다) · 러너 cd = $HOME/dem_test/<case> · 제출 폴더에 logs/
cd ~/Yonghoon-DEM-DFT && git pull
scp -P <포트> -r docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50 docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50 <사용자>@<ibb>:~/dem_test/
# ibb — 삽입 (NP 1 · 삽입 + 정착 20,000 + 3,000 step → restart_settling_20001.bin)
cd ~/dem_test && mkdir -p logs && sbatch kg50_d07_b50/run_kg50_d07_b50_insert.sh && sbatch kg50_d2_b50/run_kg50_d2_b50_insert.sh
# 끝난 뒤 — 세 검사 줄 (INSERTED · AM · SE) · FATAL 없음 · LIGGGHTS 판 (KG50-15)
grep -hE "INSERTED|====== (AM|SE)|FATAL" ~/dem_test/kg50_d07_b50/log.liggghts ~/dem_test/kg50_d2_b50/log.liggghts
head -2 ~/dem_test/kg50_d07_b50/log.liggghts
# 재개 — 원 폴더를 옮기고 시험만 (-T · 2,000 step) → 보고 ~/dem_test/resume_r<NP>_*.md (G0–G3) · 계획 ~/dem_test/<case>/plan_r<NP>.txt
mv ~/dem_test/kg50_d07_b50 ~/dem_test/kg50_d07_b50.ins1
nohup bash ~/dem_test/scripts/resume_ckpt.sh -T -n 56 -s ins1 -r ~/dem_test kg50_d07_b50 > ~/dem_test/resume_d07_b50_T.log 2>&1 &
mv ~/dem_test/kg50_d2_b50 ~/dem_test/kg50_d2_b50.ins1
nohup bash ~/dem_test/scripts/resume_ckpt.sh -T -n 4 -s ins1 -r ~/dem_test kg50_d2_b50 > ~/dem_test/resume_d2_b50_T.log 2>&1 &
grep -E "^ +kg50_d(07|2)_b50 +(compress|after_settling|settling) " ~/dem_test/kg50_d07_b50/plan_r56.txt ~/dem_test/kg50_d2_b50/plan_r4.txt
# G0–G3 통과 확인 뒤 같은 두 명령을 -T 없이 (본 제출 · NP 56 · 4)

# WSL → hit · hit — D1-50 삽입 (NP 1) → 끝나면 1저자 hit_resume.sh 로 20 코어
scp -r docs/data/kg50_decks_20261027_v3_b50/kg50_d1_b50 <사용자>@<hit>:~/simulation/
cd $HOME/simulation/kg50_d1_b50 && setsid nohup mpirun --oversubscribe --bind-to none -np 1 $HOME/LIGGGHTS-PUBLIC/src/lmp_auto -in input_kg50_d1_b50_insert.liggghts > log_kg50_d1_b50_ins.out 2>&1 < /dev/null &
grep -hE "INSERTED|====== (AM|SE)|FATAL" ~/simulation/kg50_d1_b50/log.liggghts
```

- ⛔ `run_kg50_d07_b50.sh` · `run_kg50_d2_b50.sh` (본 러너) 를 처음부터 직접 sbatch 하지 않는다 — 고코어 fresh 삽입은 기하적으로 불가능하다 (KG50-01) · 재개 도구가 쓰는 러너다.
- 재개 시험 `-T` 뒤 `plan_r<NP>.txt` 에 계획 줄이 있는지부터 본다 — `dem_restart.py` 의 실제 이름 목록은 리포에 없다 (이 덱이 그 도구를 지나는지 = 미확인).
- ibb QOS `cpu-60` = 사용자당 60 CPU — D0.7 56 + D2 4 = 60 (다른 ibb 잡이 돌면 대기).
- D0.7 압축 전 정착 끝 (after_settling) 에서 Q5 dt · 감쇠 대조 (KG50-04 · 결과 전 등록 뒤) — v2 README §4 와 같은 순서.
- 한계 = v2 README §5 와 같다 (언로딩 없음 · gen-1 프로토콜 · 단분산 SE · 본 비교 시드 하나 · 감쇠 γ/m 크기 의존).
