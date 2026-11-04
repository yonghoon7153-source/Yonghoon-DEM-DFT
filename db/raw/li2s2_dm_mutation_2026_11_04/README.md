# li2s-2 DM 고침 변이 검사 (2026-11-04)

- 하네스: `dm_mutate.py` — DL 판 (`../li2s2_dl_mutation_2026_11_04/dl_mutate.py`) 의 147 개를 가져오되 thermo 판독을 다시 써서 자리가 바뀐
  4 개 (N3 · N6 · N8 · N9) 는 새 자리로 옮기고, DM 고침 자리 13 개 (`O1_tail_time_mismatch_ok` ~ `O13_history_new_part_off`) 와
  같은 갈래로 더 막은 자리 5 개 (`O14_mid_status_check_off` ~ `O18_invalid_held` · 도중 끊김 후보의 판정 기록) 를 더했다 = **165 개**.
  저장소 밖 복사본 3 개 · 작업자 3 개 병렬.
  ⚠ 이름 앞 번호가 정전 복구 판의 O 자리 (`O6_unknown_cost_stop` · `O9_…` ~ `O13_resume_stop_run_id`) 와 겹친다 — **전체 이름으로 가른다**
  (전체 이름 165 개는 모두 다르다 · `--only=O12` 는 둘 다 잡는다).
- `dm_mutate_main.log` — 본 판 (코드 3d97d145 · 드라이버 sha16 `d03ddcf72d36eac5`): **빨강 163 / 165** · 초록 2 — 둘 다 시험 구멍이다:
  - `N18_header_check_off` (thermo 머리 검사 끄기) — 머리 없는 thermo fixture 를 DM 의 새 꼬리 시각 규칙이 대신 잡아 (첫 데이터 행을 머리로 건너뛰면
    다음 행 시각이 한 칸 밀린다) 머리 검사 자체를 안 봤다 (DL 판에서는 빨강이었다).
  - `O12_mid_pass_fail_off` (도중 끊김 후보의 pass · fail 검사 끄기) — 같은 갈래로 넣은 상태 화이트리스트 (incomplete · invalid 만) 가 pass 도
    잡아 결과 단계가 같았다.
  ⇒ 시험 둘을 더했다: 머리 이름이 다른 thermo (`time_ps,…` · 행 시각은 맞음) → 보류 · pass 이력 폴더의 보류 이유가 '과학적 판정 (pass)' 인지
  (드라이버 sha16 `c2744b7927da30cf` · selftest 211 · 러너 83).
- `dm_mutate_rerun.log` — 고친 시험으로 두 개 다시 (`--only=N18,O12` · 앞 번호가 겹친 `O12_interrupted_stop_run_id` 도 같이 걸렸다): **3 / 3 빨강**.
- ⇒ **165 / 165**. 나머지 163 개는 다시 돌리지 않았다 — 시험을 **더하기만** 했으므로 빨강이던 변이는 같은 실패 검사가 그대로 남아 빨강이다
  (DL 판과 같은 판단).
- 첫 실행 둘 (컨테이너 재시작 · 디스크 가득 — 러너 selftest 임시 폴더 450 MB × 105 개 · 2d1c3a7b 로 고침) 과 160 개 판 (같은 갈래 고침 전에 멈춤 ·
  46 / 160 까지 빨강 46) 의 로그는 버렸다 — 같은 하네스로 최종 코드에서 처음부터 다시 돌린 것이 `dm_mutate_main.log` 다.
