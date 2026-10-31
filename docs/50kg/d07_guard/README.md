# D0.7-50 본 제출 지킴이 (10-30) — Codex 한 건 범위 GO §6 손 확인을 자동으로

- 왜: Codex 판정 (`docs/reviews/codex_kg50_d07_scoped_go_20261030/codex_review_kg50_d07_scoped_go_20261030.md`) §6 = 이 한 건의 GO 조건 — ① 원 로그 원본 ↔ 도구 사본 해시 · cmp · ② 본 호출이 새로 만든 시도 폴더의 `main_inputs.sha256` 전체 해시 = 승인값 `29ff619a…` (시험이 끝나 자동 본 제출로 넘어가기 **전**) · ④ 본 job `LMP_IDENTITY` (lmp_mpi · 덱 · 체크포인트) · ⑤ 정착 체크포인트 생성 뒤 수동 중단 (등록 Q6).  재개 도구는 ② 를 스스로 막지 않는다 (`D07S-01` = `PAI-02`).
- 무엇:

| 파일 | 무엇 |
|---|---|
| `d07_guard.sh` | 지킴이 — 읽기 전용 · 다를 때만 **그 시도 폴더의 job 하나** 취소 (② 다름 → 시험 job · ④ 다름 → 본 job) · ⑤ = 판 STL (`plate_kg50_d07_b50.stl`) 이 러너보다 새롭고 `endsolid plate` 까지 써지면 본 job 정지 |
| `d07_guard_block.txt` | DEM1 붙여넣기 블록 (`cat > ~/d07_guard.sh <<'D07_GUARD_EOF'` … + md5 게이트 · 설치만) |
| `sim_guard.sh` | 흉내 시험 — 가짜 HOME · 가짜 `scancel` · `squeue` · `sacct` · `sleep` · 흉내 도구 (작업 폴더 밀기 → 새 복사 → 새 시도 → 영수증 → 시험 → 판정 → 본 job → 신원 줄 → 판 STL) · LIGGGHTS · SLURM 없음 |

- ⑤ 신호의 근거: 재개 덱 160–187 행 순서 = `write_restart …/restart_after_settling.bin` → `print RESTART SAVED` → `run 1` → `print SETTLING COMPLETE · Z_MAX · PLATE HEIGHT` → `print … file/append plate_kg50_d07_b50.stl` (마지막 줄 `endsolid plate`).  판 STL 이 다 써졌으면 체크포인트 쓰기는 끝났다.  시험 덱은 `run 2000` 에서 끝나 판 STL 을 만들지 않는다.

## 쓰는 법 (ibb)

```bash
sed -i 's/\r$//' ~/d07_guard_block.txt && bash ~/d07_guard_block.txt     # md5 맞으면 설치
nohup bash ~/d07_guard.sh > ~/d07_guard.log 2>&1 &                        # '▶ 이제 창 A' 뒤 본 명령
```

## 흉내 시험 (10-30 메인 · `bash sim_guard.sh <블록> <승인 영수증> <-T 시험 출력> <원 로그> <장면>`)

| 장면 | 기대 | 결과 |
|---|---|---|
| happy · nomove (옛 시도가 작업 폴더에 남음) | ✅ 영수증 · ✅ 신원 3/3 · 판 STL 뒤 본 job 취소 | 같음 (scancel = 본 job) |
| recdiff (새 영수증 한 줄 다름) | 시험 job 만 취소 · 멈춤 | 같음 |
| lmpdiff (lmp_mpi sha 다름) | 본 job 취소 | 같음 (신원 2/3) |
| reject (도구가 G0–G3 로 본 제출 안 함) | 취소 없음 · 결정 줄 출력 | 같음 |
| jobgone (판 STL 전 본 job 사라짐) | 취소 없음 · ⛔ 출력 | 같음 |
| cmpdiff (원 로그 사본 다름) | 아무것도 안 함 · 멈춤 | 같음 |
| twonew (새 시도 폴더 둘) | 취소 없음 · 멈춤 | 같음 |
| early (지킴이 전에 도구를 먼저 돌림) | 기존 시도가 예상과 다름 → 멈춤 | 같음 |

## 실제 (10-30 · ibb · 1저자 화면)

| 단계 | 기록 |
|---|---|
| ① | 원본 kg50_d07_b50.ins1/log.liggghts · 사본 kg50_d07_b50/log.liggghts.ins1 (ibb) 둘 다 sha256 `b1b298bb…6657f5` · 13,475 B · cmp 같음 (15:21:13 KST) |
| 본 호출 | 시도 `attempt_r56_1030_152123_2568313` · 옛 작업 폴더 → `kg50_d07_b50.prev_1030_152123` · 복사 132 M · 정적 대조 문제 0 · 시험 job 333908 (기대 끝 22001) |
| ② · ③ | 지킴이가 ③ · ④ 에 닿음 = ② 통과 (② 가 다르면 시험 job 취소 뒤 멈추는 구조) · ③ 도구 결정 `G0 1 G1 1 G2 1 G3 1 · 잡 안 덱 신원 1` → 본 제출 job 333911 · ② 줄 원문 = 정지 뒤 전체 로그 반입 때 |
| ④ | `LMP_IDENTITY` = lmp_mpi `ee2d7726…` · 덱 `input_kg50_d07_b50_r56.liggghts` `8e129f42…` · 체크포인트 `aa833368…` → 3/3 |
| ⑤ | 15:24:18 KST 대기 시작 · 15:30 watch = P1-settle step 24,000 · 8 × 7 × 1 · 약 50 kstep/h (watch 어림) → 정지 기록 = 다음 반입 |
| ⑥ 정지 (10-31 · 1저자 ibb 화면 반입) | 정착 끝 step 200,001 · `Z_MAX 0.136972437242453` · `PLATE HEIGHT 0.142972437242453` · 원자 488,285 (계획 488,291 − 6 · 첫 감소 step 53,000 · 1저자 = SE) · job 333911 = CANCELLED (지킴이 SIGTERM · ExitCode 0:15) · 실행 05:42:08 · `restart_after_settling.bin` sha256 `45a838c18d19e3c1399a97f5948d52ad0995490f6a55040e6a6ffec8fecd2d70` · 지킴이 로그 전문 = 1저자에게 받을 것 |

- ⚠ 10-31 — 이어서 갈 압축 단계 (안정화 · 압축 · 이완) 는 이 덱 (압축 감쇠 `viscous 0.5` · 판 속도 0.01 · 목표 0.30) 으로 정지 판정에 감쇠 저항이 섞인다 (원장 `KG50-20` · `DEMP-01`) — 덱 계획 N 488,291 의 affine 어림 = 488 MPa > 목표 300 MPa (추정).  ⇒ 압축 본 제출 = Codex 답 · 1저자 결정 뒤 (요청서 `docs/50kg/report_y4/codex_kg50_y4_draft2_request_20261031.md` Q4).

- 한계: 이 한 건 전용 (경로 · 승인값 고정) · ⑤ 는 로그인 노드 백그라운드 (꺼지면 손 정지 — 판 STL 확인 줄 + `scancel`) · 일반 도구의 승인 영수증 관문 (`PAI-02` 최소 고침) 을 대신하지 않는다.

## v2 — 이어 돌리기 (10-31 · 정착 끝 → 끝 · 1저자 *"0.7 은 지금 포맷으로"* · 10-31 독립 리뷰 R2-08 · 09 · 10 · 17 반영판)

- 지키는 범위 = **제출 단계뿐** (영수증 · 신원 · 처음 5 분):
  - ① 원 로그 원본 멈춘 폴더 `kg50_d07_b50.main1031` 의 `log.liggghts` ↔ 도구 사본 `kg50_d07_b50/log.liggghts.main1031` sha256 · cmp.
  - ② 기존 시도 = 정확히 두 폴더 (집합 비교 · 순서 무관 · 그 밖 없음): 물려받은 시도 `attempt_r56_1030_152123_2568313` (멈춘 폴더에 들어 있던 10-30 본 호출 시도 — 도구의 `cp -a` 로 작업 폴더에 같이 온다) + -T 시도 (OLDATT).  새 시도 = 이 두 이름이 아닌 폴더 — 본 호출이 작업 폴더를 밀고 멈춘 폴더를 다시 복사해 물려받은 시도가 다시 생겨도 새 시도로 치지 않는다 (R2-08).
  - '이제 창 A' 전에 -T 시도 영수증 `main_inputs.sha256` ↔ 승인값 (R2-17): 파일 sha256 = OKR · 1 줄 (`…/kg50_d07_b50/input_kg50_d07_b50_r56.liggghts`) = OKD · 5 줄 (`…/restart_kg50_d07_b50/restart_after_settling.bin`) = OKK `45a838c1…` — 하나라도 다르면 아무것도 안 하고 멈춘다.
  - 새 시도 영수증 = OKR (다르면 그 시험 job 만 취소).
  - ④ 본 job `LMP_IDENTITY` 세 칸 — 도구 꼴 그대로 칸 자리를 고정해 대조 (`sha256=<OKL> deck=` · `…/input_kg50_d07_b50_r56.liggghts sha256=<OKD> checkpoint=` · `…/restart_after_settling.bin sha256=<OKK>` 줄 끝) · `LMP_IDENTITY_MISMATCH` 줄이 있으면 0/3 → 본 job 취소 · 신원 줄 5 분 뒤 `squeue` 상태 = RUNNING (아니면 1 분 뒤 한 번 더 · 그래도 아니면 ⛔ · 취소 없음).
- 지키지 않는 것 (R2-10) = 그 뒤 런 전체 (안정화 · 압축 정지 판정 · 이완 · 끝 · 물리).  머리 주석 · 끝 줄에 그렇게 적고, 읽기 전용 확인 명령 한 줄 (`squeue -j <job>` · `tail -n 3 <출력>` · `sacct -j <job> -X -o JobID,State,ExitCode,Elapsed`) 을 찍고 나간다 (오래 지켜보지 않는다).  v1 의 ⑤ (판 STL 정지) 는 없다.
- 고정값: NP 접미사 r56 (본 명령 `-n 56`) · 물려받은 시도 이름 · OKK = 10-31 정지 기록 `45a838c1…`.
- 승인값 네 자리 (OLDATT · OKR · OKL · OKD) = 10-31 -T 보고에서 채운다 — 채우기 전 · 일부만 채운 판 · 꼴이 틀린 값 (대문자 · 63 자) 이면 아무것도 안 한다.  본 제출 = Codex 한 건 범위 GO 뒤 (요청서 `docs/50kg/report_y4/codex_kg50_y4_draft2_request_20261031.md` Q4).  붙여넣기 블록 (md5 게이트) 은 채운 판으로 만든다.
- 앞 판 (R2-08 지적 대상) 을 같은 흉내에 넣은 결과: 물려받은 시도가 있는 실제 세계의 장면이 전부 ② 에서 거짓 정지 · 물려받은 폴더를 지워 ② 를 넘기면 (inherit2) 본 호출 복사가 그 폴더 (시험 job 333908 기록째) 를 다시 데려와 새 시도로 잡고 333908 을 취소한 뒤 나간다 (진짜 시도는 지키는 이 없음 · 3/3).
- 흉내 시험 (`bash sim_guard_v2.sh d07_guard_v2.sh <장면> fill` · 10-31 · 26 장면 × 3 번 = 78/78 기대와 같음): 세계 = -T 뒤 실제와 같게 (멈춘 폴더 · 작업 폴더 둘 다 물려받은 시도 · 영수증 다섯 줄 · 신원 줄 = 10-30 실제 -T 산출물과 바이트 같은 꼴 · 흉내 도구 = 실제 본 호출 흐름: 작업 폴더 밀기 → 멈춘 폴더 `cp -a` → 새 시도 → 시험 → 본 job).

| 장면 | 무엇 | 기대 | 결과 |
|---|---|---|---|
| happy | 실제 본 호출 흐름 · 값 전부 승인값 | 🟢 RUNNING · 취소 없음 (rc 0) | 같음 |
| recdiff | 새 시도 영수증 한 줄 다름 | 시험 job 만 취소 (rc 1) | 같음 (scancel 444444) |
| lmpdiff | 신원 lmp_mpi sha 다름 | 본 job 취소 · 2/3 | 같음 (scancel 555555) |
| reject | 도구가 G0–G3 로 본 제출 안 함 | 취소 없음 · 결정 줄 (rc 0) | 같음 |
| cmpdiff | 원 로그 사본 다름 | ① 에서 멈춤 (rc 1) | 같음 |
| twonew | 새 시도 폴더 둘 | 취소 없음 · 멈춤 (rc 1) | 같음 |
| early | 지킴이 전에 모르는 시도 폴더 (본 호출을 먼저 돌림) | ② 에서 멈춤 (rc 1) | 같음 |
| jobgone | 5 분 뒤 큐에 없음 | ⛔ · 취소 없음 (rc 1) | 같음 |
| unfilled | 승인값 넷 다 비움 | 아무것도 안 함 (rc 1) | 같음 |
| deckdiff | 신원 덱 sha 다름 (MISMATCH 줄 없이) | 본 job 취소 · 2/3 | 같음 (scancel 555555) |
| ckpdiff | 신원 체크포인트 sha 다름 (MISMATCH 줄 없이) | 본 job 취소 · 2/3 | 같음 (scancel 555555) |
| mismatch | 신원 3/3 + `LMP_IDENTITY_MISMATCH` 줄 | 0/3 → 본 job 취소 | 같음 (scancel 555555) |
| partialfill | OKL · OKD 비움 | 아무것도 안 함 (rc 1) | 같음 |
| partialfill_att | OLDATT 만 비움 | 아무것도 안 함 (rc 1) | 같음 |
| partialfill_lmp | OKL 만 비움 | 아무것도 안 함 (rc 1) | 같음 |
| partialfill_upper | OKL 대문자 64 자 | 아무것도 안 함 (rc 1) | 같음 |
| partialfill_short | OKL 63 자 | 아무것도 안 함 (rc 1) | 같음 |
| realfmt | `$HOME/dem_test` 가 링크 · 영수증 · 신원 줄 = 실제 경로 (/lustre 꼴) · ibb lmp_mpi 경로 | 🟢 (rc 0) | 같음 |
| inherit | 작업 폴더를 밀지 않음 · 물려받은 시도 (job_t 333908) 와 -T 시도가 있는 채로 0.5 s | 🟢 (rc 0) | 같음 |
| inherit2 | 물려받은 시도를 작업 폴더에서 지움 (멈춘 폴더엔 그대로 — 본 호출 복사가 다시 데려옴) | ② 에서 멈춤 · 취소 없음 (rc 1) | 같음 (앞 판 = 333908 취소 뒤 나감) |
| move | 실제 흐름 + 작업 폴더에 다시 생긴 물려받은 시도만 있는 0.5 s | 🟢 (rc 0) | 같음 |
| tdeck | -T 영수증 1 줄 ≠ OKD | '이제 창 A' 전에 멈춤 (rc 1) | 같음 |
| tckp | -T 영수증 5 줄 ≠ OKK | '이제 창 A' 전에 멈춤 (rc 1) | 같음 |
| trec | -T 영수증 sha256 ≠ OKR (보고 뒤 바뀜) | '이제 창 A' 전에 멈춤 (rc 1) | 같음 |
| lmpdup | OKL 자리에 덱 sha (두 번 붙여넣기) | 본 job 취소 · 2/3 | 같음 (scancel 555555) |
| jobfail | 5 분 뒤 squeue 에 FAILED 로 남음 | ⛔ · 취소 없음 (rc 1) | 같음 |

- 변이 시험 (R2-09): 검사마다 끈 판 28 개 → 27 개가 적어도 한 장면에서 잡힘 (두 번 돌려 같음).  남은 1 개 (새 시도 판정을 고정 집합 대신 시작 목록으로) = ② 를 지난 뒤에는 같은 집합이라 같은 판 (equivalent) · 같은 판이 아닌 살아남은 변이 없음.  OLDATT 검사를 뺀 판은 문구로만 잡힌다 (② · 64 자 검사가 뒤에서 같은 값을 막는다).
- 한계: 이 한 건 전용 (경로 · 승인값 고정) · 흉내 = 가짜 `sleep` · `scancel` · `squeue` (Slurm · LIGGGHTS 없음) · `squeue -j` 가 끝난 job 을 상태와 함께 보여 주는지는 ibb 에서 확인 안 함 (RUNNING 만 통과라 어느 쪽이든 ⛔) · 일반 도구의 승인 영수증 관문 (`PAI-02`) 을 대신하지 않는다.

- 10-31 `-T` 뒤 승인값 채운 판 = `d07_guard_v2_1031.sh` (틀 `d07_guard_v2.sh` 와 다른 줄 = 네 승인값 줄뿐 · `diff` 로 확인) · 값 출처 = `t_test_20261031/README.md` · 붙여 넣기 블록 = `d07_guard_v2_block.txt` (md5 `35371e83472905553df3455a2267c501` 게이트 · 설치만 · 컨테이너에서 설치 왕복 · CRLF 왕복 = 같음) · 흉내 결과 = `sim_v2_results_20261031.txt` · 변이 = `sim_v2_mutation_20261031.txt`.
- ⛔ 실행 = Codex 한 건 범위 GO 뒤 (요청서 `docs/50kg/report_y4/codex_kg50_y4_draft2_request_20261031.md` Q4) · 순서 = 창 B 에서 지킴이 먼저 → "이제 창 A" 뒤 창 A 에서 `-T` 보고 끝의 본 제출 명령.
