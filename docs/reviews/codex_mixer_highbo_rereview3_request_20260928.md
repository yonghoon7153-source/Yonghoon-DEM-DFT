# Codex 4차 리뷰 요청 — 믹서 고-Bo 확장 LH (3차 HOLD 해제 목록 반영, 2026-09-28)

- 브랜치 `claude/stoic-knuth-NObVQ` · 고정 스냅샷 = **§0 의 수정 커밋** (원장 등재 커밋과 함께 적는다).
- 3차 판정문 = `docs/reviews/codex_mixer_highbo_rereview2_verdict_20260927.md` (HOLD · HBR3-01 ~ 08 · Q1 ~ Q5) · 재현 묶음 = `docs/reviews/codex_mixer_highbo_rereview2_evidence_20260927/` (우리 HEAD 에서 수치 505 개 동일 재현).
- 사전등록 = `docs/reviews/mixer_highbo_prereg_20260927.md` §2-2 · §2-3 · §2-4 · §2-5 · §8 · §10 · §12.
- 이번 수정은 **반례를 셀프테스트로 먼저 옮겨 실패시킨 뒤** 고쳤다 (규율 ②).  시뮬레이션은 돌리지 않았다.  문턱 · LC · Bo · seed 는 바꾸지 않았다.

## 0. 수정 커밋

(수정 커밋 SHA 와 원장 등재 커밋 SHA 는 등재 커밋에서 여기와 §10 에 적는다.)

## 1. 항목별 — 무엇을 바꿨고 어느 셀프테스트가 지키나

| 항목 | 수정 | 셀프테스트 (먼저 실패 확인) |
|---|---|---|
| HBR3-01 영수증 생산자 | `scripts/mixer_restart_phase_test.py` v1 전면 재작성 — A 덱 = 캠페인 덱에서 **입자 삽입 · 원자 dump · 주기 restart 만 뺀** 것 (run 구조 그대로 · 템플릿 유지) + 캠페인 원자 dump 간격의 `dump mesh/stl` · 회전 run 을 N1 에서 쪼개 `write_restart`.  B = `make_mixer_resume.transform` (캠페인 재개와 같은 변환) + 템플릿 재선언.  run.sh 가 실행 **직전** 봉인 (바이너리 · 덱 · STL sha256) · 실행 뒤 exit · 완료 표지 · 덤프 sha256.  analyze 는 기대 step 집합과 정확히 같아야 (누락 · 추가 실패) · 전 step 전체 메시 = 원 STL 의 예정각 회전 (꼭짓점 순서) · B = A · 배너 동일일 때만 통과 | ⑤ ⑥ · ⑦ 변이 11 (Codex 의 A 0 개 · B 한 장 · 재개 전 한 장 포함) — 17/17 |
| HBR3-02 영수증 소비자 | `load_phase_receipt` — schema `restart_phase_v1` 만 · `passed is True` · 주기 · dt · 축 형식과 덱 일치 · SHA 형식 = 봉인 SHA · A/B 정상 완료 · **운동 서명** (STL 내용 · scale · 축 · 주기 · 순서) = 이 덱 · **런 로그 배너 전부 = 영수증 배너** · 창의 모든 step ⊂ 영수증 실측 step | `check_contact_validity` ㉑ · ㉑b · ㉑c (변이 12) · ㉑d |
| HBR3-03 구간 극값 | `wall_interval` — 평면 부호거리 A + B cos θ + C sin θ 의 구간 끝 + 내부 정지점.  상한 ≤ 1 % PASS · **하한** (max_i min_θ) > 1 % REJECT · 사이 = TECH "위상 불확실성으로 미식별".  ε = 영수증이 판정 step 에서 잰 각 경계 (실측 · 출력 해상도 중 큰 것) · 등록 상한 `PHASE_EPS_DEG` 0.05° 한 곳 | ㉒ (구간 내부 1.00034 % → TECH) · ㉒b (REJECT) |
| HBR3-04 mesh 덤프 | `mesh_dump_container` — 삼각형 수 = 원 벽 메시 합 · 원 기하의 강체 회전 (양방향 최근접) · 예정각과 면 대칭 제외 ≤ 0.05° · 볼록.  옛 `container_from_stl` 폐기 | ㉓ (드럼만) · ㉓b · ㉓c (5°) · ㉓d · ⑮b |
| HBR3-05 기준 t₀ · 격자 밖 | 판독기 `planned_t0` · 평가 런 · E0 모두 계획 t₀ 정확 (없으면 정지) · 격자 밖 · 중복 = 제외 + tech · 검사기도 같은 `planned_t0` | 판독기 ⑲ ⑳ ㉑ ㉑b ㉑c ㉕ · 검사기 ㉕ |
| HBR3-06 프레임 스키마 | `measure_bed_aspect.validate_frame` (머리 · 필수 열 · 행 길이 · id/type 유한 정수 · id 유일 · 좌표 유한 · 반경 양수) 를 판독기 · 검사기가 **매 프레임** | bed ⑩ (변이 9) · 검사기 ㉔ · 판독기 ㉒ ㉓ ㉔ |
| HBR3-07 실제 seed | `mixer_deck_diff` — 각 덱의 실제 seed 서명 = 생성기 기대값 (생성기 CLI 와 바이트 동일한 덱에서) · LC = LH · 고유 · 예정 밖 디렉터리 거부 | 24/24 (Codex 사례 → 0/3 · rc 1) |
| HBR3-08 발사 | `run_all.sh` 는 `LH_*` 를 기본 건너뜀 · `launch_highbo.sh first` (덱 비교 게이트 · `launch_record.json` 봉인 · 첫 시드 하나) / `rest <스모크 증서>` (증서가 서야 나머지 둘) | `test_launcher.sh` (가짜 실행파일) |
| HB-01 · Q5 정본 | v09 다섯째 열 = Bo_code (CED 아님) · PNG 시각 확인 · §2-3 세 층 (값 보고 / 판정 적격 / A 발동) · §12 자리표시자 → 실제 SHA · 검사기 머리말 · `deck_walls` · `infer_drum_phase` 의 "되읽기 = 확인" 철회 | — |

## 2. 설계 판단 — 동의 · 반대를 받고 싶은 것

**Q1 — 영수증 v1 의 논리.**  드럼 회전은 처방 운동이라 입자와 무관하다 → 캠페인 덱의 step 구조를 그대로 둔 0 입자 덱은 캠페인 런과 **같은 메시 궤적**을 밟는다 → 캠페인 원자 dump 간격으로 mesh 를 덤프하면 판정 프레임과 **같은 step** 의 벽을 직접 잰다.  그래서 ε 를 가정하지 않고 그 step 의 실측 오차 (+ 출력 해상도) 를 쓴다.  이 논리와, 소비자가 대조하는 것 (배너 · 운동 서명 · 판정 step ⊂ 실측 step) 이 "시험한 바이너리 ↔ 판정할 런" 연결로 충분한가.  빠진 불변량이 있는가.
⚠ 사실 하나: 3차가 지적한 ±0.05° 면 가장자리 효과 (+0.97 %p) 때문에, ε 를 0.05° 로 **가정**하면 벽에 닿은 실제 침대는 거의 전부 TECH 가 된다.  실측 각 경계가 그 값보다 훨씬 작다는 것을 보이는 것이 v1 의 목적이다.

**Q2 — 구간 극값의 하한.**  REJECT 에 쓰는 하한 = max_i min_θ s_i 는 참 겹침의 **엄밀한 하한**이지만 느슨할 수 있다 (진짜 min_θ max_i 보다 작다).  보수적 방향이라 받아들였다.  더 조일 필요가 있는가.

**Q3 — 예정각과 모순되는 mesh 덤프.**  면 대칭을 뺀 각이 예정각과 0.05° 넘게 다르면 그 덤프를 **쓰지 않고 TECH** 로 둔다 (다른 시각 · 다른 런의 파일과 구분할 수 없어서).  2차 ⑮b 의 기대 (그 덤프로 2 % 를 REJECT) 를 이것으로 바꿨다 — 참 2 % 는 여전히 PASS 로 새지 않는다.  이 규칙이 옳은가, 아니면 출처 증명이 따로 있으면 덤프를 우선해야 하는가.

**Q4 — 판독기의 제외 규칙.**  격자 밖 · 중복 · 형식 실패 프레임은 평균 · SD · flat 에서 **빼고** `tech` 에 적는다 (그래서 판정 부적격).  중복 step 이 최종 bin 에 있으면 `planned.M_final` 이 None 이 된다.  fail-closed 로 충분한가.

**Q5 — 남은 것 (이번 커밋 밖).**  3차 Q1 의 **런별 체크포인트 상태 확인** (보존된 L/LC 체크포인트 복사본 + 실제 `in.resume` 을 별도 폴더에서 몇 step 돌려 전체 mesh 를 예정 기하에 대조) 은 아직 만들지 않았다.  영수증 v1 (바이너리 + 운동 계약) 과 이것 (런 상태) 을 둘 다 요구하는 것이 3차의 해제 조건 2 와 맞는지, 그리고 LH (새 런) 는 발사 시 봉인 + 영수증 v1 만으로 충분한지.

## 3. 재현

```bash
python3 scripts/measure_bed_aspect.py --selftest        # 25/25
python3 scripts/check_contact_validity.py --selftest    # 55/55
python3 scripts/measure_mixing_index.py --selftest      # 32/32
python3 scripts/mixer_deck_diff.py --selftest           # 24/24
python3 scripts/mixer_restart_phase_test.py --selftest  # 17/17
bash dem_scripts/mixer_20260921/test_launcher.sh        # 런처 (가짜 실행파일)
```
3차 프로브 (`docs/reviews/codex_mixer_highbo_rereview2_evidence_20260927/review_round3_probe.py`) 는 옛 동작을 **기대**하는 assert 가 있어, 새 코드에서는 그 assert 들이 실패하는 것이 정상이다 (수정의 증거로는 위 셀프테스트를 본다).

## 4. 실데이터 순서 (4차 GO 뒤)

영수증 v1 을 WSL 에서 생성 (0 입자 · 캠페인 step 구조) → L 완주 → 런별 상태 확인 (Q5) → 생산 덱 3 쌍 대조 (`--expect-deck`) → 봉인 → `launch_highbo.sh first` → bin 0 스모크 증서 → `launch_highbo.sh rest`.
