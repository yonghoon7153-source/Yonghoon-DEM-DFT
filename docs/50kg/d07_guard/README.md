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
