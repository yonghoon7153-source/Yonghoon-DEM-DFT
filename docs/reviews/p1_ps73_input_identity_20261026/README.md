# P1 7:3 언로딩 입력 — 기존 원본 파일 여섯의 현재 신원 확인 (ibb · 읽기 전용 · 2026-10-26)

- 요청: 1저자 10-26 밤 — *"ibb에 이미 있는 원본 파일 여섯 개의 현재 크기·SHA256을 읽고, 과거 기록과 비교하는 것까지만"*.
- 기준 자료: Codex 쪽지 `docs/collab/codex_to_claude/20261026-1816_nonrint-facts-reply.md` (커밋 `18c7b83f97f84808d3283d8bbc37725b48bc5924` · 가지 `codex/nonrint-facts-reply` · 반입 안 함 · 읽기만).  그 기대값 = 10-09 기록 (`docs/reviews/dem_unloading_ps45_precheck1_20261009/ibb_precheck1_screen.txt` L163–170 · `docs/data/ps45_unload_20261009/unload_params.json`) · r8 로그 해시 = `docs/data/ps73_compaction_curve_20261006/curve/curve_summary.json`.
- 실행: 1저자가 ibb 로그인 노드에서 직접 (Claude 컨테이너는 ibb 에 닿지 않는다 — TCP 시간 초과 · 키 없음).  기계 `ibb-master` · 사용자 `yonghoon` · 2026-10-26 20:14:00 → 20:14:02 KST.
- 명령: Codex 블록과 **같은 읽기** (같은 여섯 경로 · `stat --printf='%s %n\n'` · `sha256sum` · 파일별 rc · 전체 rc) 를 한 줄로 옮긴 판 — 여러 줄 블록 붙여 넣기가 실행되지 않아서 · Codex 블록 원문을 그대로 돌린 것은 아니다.  복사 · 폴더 생성 · 수정 · 작업 제출 · copycmd 실행 = 없음.
- 원본 출력 = `ibb_identity_screen.txt` (1저자 화면 그대로 · stdout · stderr 같은 화면 · 오류 줄 없음).

## 대조 (기대값 = Codex 쪽지 표를 기계로 읽어 비교)

| 파일 | 현재 존재 여부 | 크기 일치 | SHA256 일치 | 오류·미확인 사항 |
|---|---|---|---|---|
| `restart_compress_3200000.bin` | 있음 (stat_rc 0 · sha256sum_rc 0) | 예 (81154383) | 예 (`0aa6e41a…3ca3730`) | 없음 |
| `atom_3200000.liggghts` | 있음 (0 · 0) | 예 (21430748) | 예 (`2da106f8…bbdd9e`) | 없음 |
| `contact_3200000.liggghts` | 있음 (0 · 0) | 예 (149687008) | 예 (`53ae293b…416e65c`) | 없음 |
| `mesh_3200000.stl` | 있음 (0 · 0) | 예 (349) | 예 (`c25296a6…bde2b820`) | 없음 |
| `output_ps_7_3_r45_r8_220537.out` | 있음 (0 · 0) | 예 (127049) | 예 (`35e28690…96c49`) | 없음 |
| `input_ps_7_3_r45_r8.liggghts` | 있음 (0 · 0) | 예 (5916) | 예 (`097658aa…cd`) | 없음 |

- 읽기 명령 성공 = `identity_read_rc=0` (여섯 파일 stat · sha256sum 모두 rc 0).  **기대값 일치는 그와 별개로** 위 표의 크기 · 해시 대조 (64 자리 전체) 로 판정했다.
- 읽는 동안 파일이 바뀌었는지는 따로 재지 않았다 (한 번 읽음 · 2 초).  크기 · 해시가 10-09 기록과 같다 = 그 뒤로 바뀌지 않았다는 것과 정합.

## 결론 (범위)

**기존 입력 파일의 현재 신원 확인** 까지다 — 여섯 파일이 ibb 의 기록된 자리에 10-09 기록과 같은 바이트로 있다.  S0 복원 자격 · 물리 실행 GO 가 아니다.

## 다음 단계의 미충족 조건 (이번 확인과 별개)

1. 작업 폴더 `~/ps45_unload_20261009/ps_7_3_r45/in/` 로 복사 (copycmd) — 안 함 · 별도 승인.
2. 7:3 복원 시험 `RJ` (7:3 = Ut0 먼저 · `docs/data/ps45_unload_20261009/README.md` §2) — 안 돌림 · 사전 점검 입력 `GRAMMAR_VERDICT` (10-15 실행 2) · `HIST_VERDICT` (ibb `hist_20261014_094731/`) 가 그 자리에 그대로인지 확인 필요.
3. 키트 본 실행 GO — 키트 README "⛔ 본 R · 10:0 연장 · U 의 GO 아님" (10-14) · 10-23 뒤 Codex 트랙 · Codex 18:16 쪽지가 닫았다고 적은 것 = ULPRI-01/02 의 한정된 marker 무결성 · T12R-01 offline 경계 · 본 실행 승인 기록은 Claude 쪽에 없다.
4. 실행 바이너리 신원 — 10-09 기록 `lmp_mpi` sha256 `ee2d77261bac9e7f…` 를 실행 때 다시 대조.
5. S0 복원 자격 · 물리 GO — 이번 범위 밖 (Codex 쪽지 경계 그대로).
