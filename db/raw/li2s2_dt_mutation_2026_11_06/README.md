# li2s-2 DT 판 변이 검사 (2026-11-06) — 회신 DS 고침

- 트랙: li2s-2 (논문 1저자 = 외부 · 위임 10-30). 결과 0 건 · 카드 값 그대로 (값 지문 086de59c484f9c32).
- 회신 DS (`kb/reviews/codex_DS_reply_li2s2_dr_fixes_2026_11_06.md` · 기준 6b124717): NO-GO · 새 P0 없음 · P1 1 · P2 1.
  - P1-1 — plan.json 이 없거나 깨져 일정 · 프레임 검사를 건너뛰면 md_done.json 도 없을 때 완료 여부가 불명인데 md_complete_seen=False 로 적혀,
    기준 앞 면제가 그것을 '실제 진행 중' 으로 읽었다 (완료 런에서 plan · md_done 을 옮기고 들여다봄 → 되돌리고 thermo 고침 → 끝 판정 일시 오류 →
    확인 → 7 실행 → stage1_pass).
  - P2-1 — 판독기가 거부하는 판정 링크를 직접 수동 판정 (--stage1_verdict) 은 따라가 밖의 판정을 이력에 넣고 링크를 정상 파일로 바꿨다.
- 고침 (bd21f70c): 판정이 `md_progress` 를 적는다 — 'complete' (완료 흔적 또는 MD 가 끝나야 생기는 경로가 있음 · plan 판독과 무관) ·
  'in_progress' (plan 을 읽고 gate_check 가 오류 없이 일정 끝 아님 · 프레임을 세서 n < 기대 · 완료 흔적 없음) · 'unknown' (그 밖).
  기준 앞 '진행 중' 지름길은 md_progress 'in_progress' 이고 그때 지문에 뒤 산출물 (final · result · md_init_raw) 이 없을 때만 ·
  옛 꼴 · 확인 불가는 대체 규칙. 직접 판정은 판정 · 이력 자리가 정상 파일 (또는 없음) 이 아니면 읽기 · 이력 덧붙이기 · 교체 전에 거부 (written False).
  드라이버 selftest 252 · 러너 selftest 158 (Codex 재현 흐름 — 고침 있음 · 없음 → 발사 0 · 진행 중 대조 → md_progress in_progress · 회복).
- 하네스: `dt_mutate.py` — DS 판 (`../li2s2_ds_mutation_2026_11_06/ds_mutate.py`) 472 개를 가져온다.
  - 회신 DS 고침으로 자리가 바뀐 2 개는 새 자리로 옮겼다 (뜻 그대로 · `MOVED_DT`): DS10 (지름길 늘 켬) · DS21 (지름길이 진행 판정을 안 봄).
  - DT 자리 17 개: DT1–DT9 md_progress (뒤 산출물 경로 · gate · 일정 · 프레임 조건 끄기 · 기록 값 고정 · 흔적 목록에서 하나 빼기) ·
    DT10–DT11 지름길 (뒤 산출물 무시 · 옛 규칙) · DT12–DT13 기록 꼴 (plan 전 판정 열쇠 · 어휘) · DT14–DT17 직접 판정 경로 검사 (끄기 · 한쪽만 · 링크 허용).
  - 넣지 않은 것 (같은 뜻 — 시험이 가를 수 없음): md_progress 의 plan 객체 조건 (plan 을 못 읽으면 gate_check 가 안 돌아 gate 조건이 같이 막는다) ·
    프레임 하한 0 ≤ n · n ≥ 기대 갈래 (md_complete_seen 이 먼저 complete 로 보낸다).
  - 모두 **489 개** (DS 판 472 · 옮김 2 · DT 17). 실행 · 판정은 DS 판과 같다 (selftest 시간 제한은 ⚠ 로 남긴다). 뺀 것 없음.

## 실행 기록

| 실행 | 판 | 범위 | 결과 |
|---|---|---|---|
| 새 · 옮긴 자리 | bd21f70c | DS10 · DS21 (옮김) · DT1–DT17 = 19 | 빨강 16 · **초록 3** — DT7 · DT8 (흔적 목록에서 하나 빼기: 시험이 도구 상수를 돌며 기대값도 그 상수로 만들어 빠진 원소를 같이 빠뜨림 — 자기 참조) · DT15 (이력 쪽 검사 끄기: 판정이 던진 OSError 를 링크 시험 묶음의 `except OSError` 가 '링크 못 만듦' 으로 삼켜 하위 경우가 조용히 빠짐) — `dt_mutate_new_bd21f70c.log` |
| 초록 자리 + 링크 이웃 | 4358524f (시험만 — 목록은 시험이 정하고 도구 상수가 그것을 품는지 대조 · 링크 만들기만 try 안 · 판정 예외는 값으로) | DT7 · DT8 · DT14–DT17 · DS14 · DS15 · DS18 · DS19 · DS23 · DS24 = 12 | 빨강 12 / 12 — `dt_mutate_r0b_4358524f.log` |
| 전체 | (마지막 판) | 489 | (돌릴 것) |

## DT 전 독립 리뷰 (DS 때와 같은 리뷰어 · 결과 모름 · 반례 재현)

### 1 차 (bd21f70c) — (회신 기다림)
