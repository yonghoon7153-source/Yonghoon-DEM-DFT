# D0.7 압축 체크포인트 재개 `-T` 시험 (11-03 · ibb · 1저자 화면 반입)

- 명령 (1저자 11-03 01:43 KST · 시도 이름의 시각): `cd ~/dem_test/scripts && nohup bash resume_ckpt.sh -n 56 -s run335457 -r /home/yonghoon/dem_test -x r56 -t 2000 -T kg50_d07_b50 > ~/d07_cmp_T.log 2>&1` · 멈춘 폴더 = `kg50_d07_b50.run335457` (job 335457 · 원 로그 끝 step 1,055,002) · 체크포인트 = `restart_compress_1000000.bin` (step 1,000,000).
- 결과 = **G0 · G1 · G2 · G3 통과** · 본 제출 안 함 (`-T`) · 시험 job 337078 = COMPLETED · ExitCode 0:0 · 00:03:53 · 끝 step 1,002,000 (= S0 1,000,000 + 준비 run 2 + 루프 run 1,998).
  - G0: 마지막 thermo 줄 유한 · `Loop time … for 1998 steps` = 시험 마지막 run · 잡 안 덱 신원 같음.  판정 (1,000,002) 에서 목표에 닿았다면 시험 덱의 `quit` 으로 종료 코드가 0 이 아니었다 — 0:0 = 목표 아래 · 루프 계속.
  - G1: step 1,000,000 setup 줄 KE `3.3619779e-08` = 원 로그.
  - G2: `atom_1000000.liggghts` · `mesh_1000000.stl` 같음.
  - G3: step 1,000,002 — 압력 `0.00011997834` → `0.00011998104` (상대차 2.25 × 10⁻⁵) · KE `3.3622402e-08` → `3.364381e-08` (6.37 × 10⁻⁴) · 5 % 안.
- 원문 = `t_output_grep.txt` (붙여 넣은 화면 그대로 · `sacct` · 도구 로그 grep · 영수증).
- ⚠ 도구 신원 줄 (보고 머리 `resume_ckpt.sh sha256 …`) 은 이번 grep 에 없다 — 본 제출은 `-A` · `-H` 가 같은 값을 강제한다 (`scripts/resume_ckpt.sh` 1924–1928 줄: 다르면 아무것도 하지 않음).

## 승인값 (이 시험에서)

| 자리 | 값 | 출처 |
|---|---|---|
| `-T` 시도 | `attempt_r56_1103_014321_1895853` | 도구 로그 · `ls -td` |
| 영수증 sha256 (`main_inputs.sha256` 파일 전체) | `cff47c44385a95529ed2c6e97438985a56e6e2ede194e05f7541c14788570176` | `sha256sum` 화면 — 붙여 넣은 다섯 줄을 `sha256sum` 꼴 (두 칸 · 줄 끝 개행) 로 다시 만든 값과 같음 (10-31 과 같은 방법) |
| 본 덱 (`input_kg50_d07_b50_r56.liggghts`) | `12873efcf4829de6f6cb036099782b1c2e2a11e8f9df44bb2b6720a5c1d6ccf5` | 영수증 1 줄 |
| 본 러너 (`run_kg50_d07_b50_r56.sh`) | `f20d6854293950cf3a513bfb34d660dd5e358c25da64c12f5dee532e85baefa0` | 영수증 2 줄 |
| 시험 덱 (`input_kg50_d07_b50_r56t.liggghts`) | `4110ee76810b85f0f64ce88562bc148b119b86bee9be2dfdbbac529478c8ca2a` | 영수증 3 줄 = 잡 안 신원 줄 |
| 시험 러너 (`run_kg50_d07_b50_r56t.sh`) | `97e4df27e46624864737f567a5a6152dabe39d2a3f51bcc7b77d72818d29795c` | 영수증 4 줄 |
| 체크포인트 (`restart_compress_1000000.bin`) | `164824ea603741e436361589b48ee9d9f0fb16bf6bb12b92a630552bc3799de0` | 영수증 5 줄 = 잡 안 신원 줄 |
| lmp_mpi | `ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f` | 신원 줄 (10-30 · 10-31 과 같음) |
| 도구 (`-A` · `-H`) | `66006239ec58043f963fa885f9db545c63614d279bfb6cac1665a2eae9884c6d` · `d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8` | 리포 `scripts/resume_ckpt.sh` (개정 5b) · 10-31 기록의 dem_restart.py |

- 본 제출 호출은 작업 폴더 `kg50_d07_b50` (이 시험 폴더) 를 `kg50_d07_b50.prev_<시각>` 으로 옮겨 보존하고 멈춘 폴더를 다시 복사한다 (`scripts/resume_ckpt.sh` 2216–2220 줄) → 이 시도의 영수증은 `kg50_d07_b50.prev_<시각>/attempt_r56_1103_014321_1895853/main_inputs.sha256` 에 남는다.
- ⛔ 본 제출 = Codex 짧은 확인 GO 뒤 (요청서 `docs/50kg/codex_kg50_d07_compress_resume_request_20261103.md`).
