# Codex 3차 리뷰 요청 — 믹서 고-Bo 확장 `LH` : 재리뷰 HBR2-01~08 · K1–K7 반영 (2026-09-27 밤)

> 요청자 = 1저자 (사용자) · 작성 = claude.  2차 판정 = **HOLD** (`docs/reviews/codex_mixer_highbo_rereview_verdict_20260927.md` — ① 부분 · ② 닫힘 · ③ 부분 · ④ 열림).
> 고정 스냅샷 = **`20568797b`** (브랜치 `claude/stoic-knuth-NObVQ`) — 수정 커밋.  원장 등재 커밋 = `이 요청서와 같은 커밋 (원장 HBR2-01~08 claimed_fixed)`.
> 재리뷰의 합성 반례는 **우리 HEAD 에서 먼저 전부 재현**했고 (`docs/reviews/codex_mixer_highbo_rereview_evidence_20260927/README.md`), 그 경우들을 세 스크립트의
> 셀프테스트로 옮겨 **먼저 실패시킨 뒤** 고쳤다 (TDD 기록 = 진행파일 ㉓).
> **아직 하지 않은 것**: 재개-위상 영수증 **실제 실행** (WSL · `scripts/mixer_restart_phase_test.py` — 초 단위) · 새 검사기 · 판독기를 **실데이터**에 돌리기 · LH 덱 생성 · 발사.
> 답 형식: HBR2 항목마다 **닫힘 / 부분 / 열림** + 이유, §3 질문마다 **동의 / 반대 / 수정안**, 끝에 **GO / HOLD** 한 줄 (GO = "L 완주 + 영수증 통과 + 실행 덱 대조 뒤 발사해도 된다").

## 1. HBR2 항목별로 무엇을 했나

| 항목 | 한 것 | 증거 (셀프테스트 번호) |
|---|---|---|
| **HBR2-01** 벽 위상 되읽기 | 되읽기 (fitting) 를 판정 경로에서 **뺐다** — `--diag-fit` 진단으로만 남고 `phase_note` = "증거 아님".  벽 근거 3 단: ① `post_mesh/mesh_<step>.stl` (LIGGGHTS `dump mesh/stl`) 이 창 전 프레임에 있으면 그 삼각형 (`mesh-dump`) ② 재개-위상 영수증 (`--phase-receipt`, 덱의 주기 · 축과 맞을 때만) 이면 예정각 ± 영수증 각 오차 (`receipt`) ③ 없으면 회전각-무관 상·하한 — 상한 ≤ 1 % 만 PASS · 하한 > 1 % 만 REJECT · 사이 = **TECH** (`unidentified`, 예정각 값은 미검증 표지).  0.18° 허용치 (면각의 2 %) 폐지 — 영수증의 각 오차는 ±ε 에서 다시 재 최댓값으로 **전파** | `check_contact_validity` ⑩ (증거 없으면 2 % 도 TECH) · ⑩c (mesh 덤프 → REJECT) · **⑮ = Codex 반례 1: 참 2 % + 반 면각 → TECH (PASS 불가)** · ⑮b (독립 기하 주면 REJECT) · ⑮c (일부 프레임만 mesh 덤프 → 안 씀) · **⑯ = 반례 2: 참 = 예정 · 0.5 % → PASS(bounded)** · ⑯b (영수증 → receipt) · ⑯c (주기 다른 영수증 거부) · ⑬ (면을 따라 깔린 침대 = 근거 없이는 unidentified · 진단은 각을 맞히지만 판정에 안 씀) · ⑬b · ⑬c · ⑬d |
| **HBR2-02** bin 0 스모크 | 판독기 출력에 `smoke` 블록 (bin 0 창) 과 `tech_smoke` 를 **분리** — 전체 미완주는 `tech` (최종 창) 에만 · bin 0 결손 · 비유한 · 헤더 오류 · 중복은 `tech_smoke`.  사전등록 §8 = 첫 시드 먼저 → `smoke.tech_smoke` 비어 있음 → 나머지 둘 (D-4) | `measure_mixing_index` ⑯ (정상 26 프레임 스모크 통과 · 최종 창은 미완주 표지) · ⑯b (bin 0 결손 → 스모크 실패) |
| **HBR2-03** 저장 프레임 ≠ 전 시간 최대 | 관측량을 **이름 붙였다**: `observable = snapshot-max` (덤프 사이 peak 미관측) · 창 안 덤프 결손 (계획 격자 대비) = TECH · 격자 밖 step · 중복 = TECH.  D-1 = 저장 프레임 최대 ≤ 1 % · 전 적분 최대 = `NOT OBSERVED` (사후 JSON 으로 채우지 않는다).  두 층 규약 없음 · 문턱 완화 없음 | ⑱ (2500 결손 → TECH) · ⑱b (표지) · ⑲ (헤더 step ≠ 파일명 → TECH) |
| **HBR2-04** bin 완전성 | 완전성 = **계획 덤프 격자** (t₀ 부터 덱 `steps_total` 까지 dump_every 간격) 의 그 bin step 이 다 있다.  직전 bin 결손이면 `flat = None` + `tech` (최종값은 보고) · 헤더 TIMESTEP/원자 수 ≠ 파일명/행 수 · 중복 = `tech` | ⑰ (bin 6 이 2/25 → 최종값 보고 · flat None · tech) · ⑰b (마지막 계획 덤프 없음 → 미완주) · ⑰c (복제 파일 → 헤더 불일치) · 옛 ⑬ · ⑬b · ⑭ · ⑮ 그대로 (정상 완주에서 옛 의도와 같은 창 · 값) |
| **HBR2-05** 덱 비교기 | CED 명령 머리 (fix id · group · style · n) 동일 · **양쪽** 행렬 유한 · 비음수 · 대칭 · 허용 쌍은 **증가** 방향 · `--expect-deck` (지금 생성기로 새로 만든 같은 팔 덱의 행렬과 1e-5 안 일치) · `--runs` 는 예정 세 시드 (기본 `CAMPAIGN_SEEDS`) 를 `n/N` 로 세고 빠지면 rc 1 | `mixer_deck_diff` ⑧ (한 방향 ×2 → FAIL) · ⑨ (NaN) · ⑩ (음수) · ⑪ (머리 변경) · ⑫ (방향 반대) · ⑬ (목표 행렬) · ⑭ (1/3 시드) |
| **HBR2-06** 0.90 의 지위 | D-2 = **부피 누락 QC** (평균 ≥ 0.90 (AM · SE) ∧ 프레임별 · 상별 (AM_P · AM_S · SE) 최솟값 ≥ 0.80) — 대표성 보증 아님.  판독기 `cell_stats` 가 상별 (type 별) 유지 부피 · `by_rev` 가 상별 최솟값 · 평균 · `qc_repr` 를 낸다.  미달 → M 보고 + "선택-셀 M · 대표성 QC 미달 — 전체-bed 결론 제한" (§5 결론 문장 · §6 A 발동 불가) | ⑱ (Codex 반례 재현: 유지 0.98 인데 S²_keep 0 · S²_all 0.2) · ⑱b (2/25 프레임 유지 0 → 평균 0.92 통과인데 QC 미달) |
| **HBR2-07** 라벨 | `\|Δ\| ≤ SE` = **"무분리 범주"** (부등식 불변 · "작은 차이 · 효과 없음 · 동등" 금지) — 본 캠페인 §5 · 확장 §5.  `Δ_A/Δ_B` = "LC 기준 경로상 두 contrast 의 비" ("AM–AM 몫" 철회) · A 미발동 = 미검사 · 고정 8 회전 수치는 보고하되 A 발동은 평탄 참에서만 | prereg §5 · §6 · 본 캠페인 §5 |
| **HBR2-08** id 별 속성 | id 별 type · radius = t₀ (정렬 대조) · id 유일 · 정수 · 유한 · 헤더 원자 수 = 행 수 · `--expect-types` (상별 계획 수) | ⑰ (type 교환 + 반경 절반 → REJECT) |
| HB-01 잔여 | 생성기 :152–157 의 현재형 앵커 설명을 철회 표지로 정정 (주석 — 덱 · 골든 해시 불변 89/89).  v09 표 0.212 칸 · PNG 렌더는 **아직** (§4) | `make_mixer_deck` 89/89 |
| K7 규칙 원장 | prereg **§12** — 원 규칙 / 현재 적용 규칙 / 이유 / 시각 · 커밋 / 당시 본 데이터 / 보고 제한, 8 행 | `docs/reviews/mixer_highbo_prereg_20260927.md` §12 |

## 2. 저자 결정 (2026-09-27 저녁 · "권고하는 걸로" · 겹침 미열람 · 중간 M(t) 열람 뒤 = 겹침-맹검 개정)

prereg §9 표.  **D-1** 저장 프레임 최대 ≤ 1 % · 벽 근거 규칙 · 전 적분 최대 NOT OBSERVED · **D-2** 부피 누락 QC (0.90 평균 ∧ 0.80 프레임별 · 상별) · **D-3** §6 그대로 + 몫 철회 + 평탄 참 · **D-4** 첫 시드 먼저.

## 3. 새로 생긴 것 — 검토 부탁 (재개-위상 영수증)

덱은 mesh 를 덤프하지 않고 (LC 는 이미 돌았다), 면을 따라 깔린 침대는 근거 없이는 늘 `unidentified` 다 (⑬).  그래서 K2 의 둘째 경로 *"검증된 실행 바이너리 · fix ID · 재개
상태 · 회전 스케줄"* 을 **실측 영수증**으로 만들었다 — `scripts/mixer_restart_phase_test.py`:
- `gen`: 실제 캠페인 덱 (`runs/LC_s*/in.mixer`) 에서 **입자 명령만 뺀** 두 덱 (A: 회전 N1 = 20,000 step → `write_restart` → N2 = 10,000 · B: `read_restart` 로 이어 N2) —
  fix ID · 재료 · 메시 · 벽 · 회전 · 적분기 **순서 · ID 그대로** (셀프테스트 ②) · `dump mesh/stl` 5,000 step 마다 · `run.sh` (WSL · 같은 `lmp_serial`).
- `analyze`: B 의 mesh 덤프를 (i) 같은 step 의 A 덤프와 꼭짓점 좌표 대조 (ii) 예정각 2π·s·dt/period 와 대조 (드럼 표지 꼭짓점 = 축과 나란하지 않은 첫 삼각형의 첫 꼭짓점,
  축 둘레 atan2) (iii) 리셋 대안 2π·(s − N1)·dt/period 와의 간격 — 통과 = (i) 1e-9·크기 안 · (ii) 0.05° 안 · (iii) ≥ 1° (N1 = 20,000 이면 6.7°).
  영수증 JSON = 바이너리 sha256 · 버전 줄 · 주기 · 축 · dt · 검사 step · 각 오차 · 원 덱 sha.  검사기는 주기 · 축이 덱과 맞고 `passed` 인 영수증만 받고 (⑯c · 도구 ⑥),
  각 오차를 ±ε 로 전파한다.
- **한계 (그대로 적는다)**: 영수증은 **바이너리의 성질** (read_restart 가 위상을 잇는다) 의 실측이지 어느 런의 벽 좌표가 아니다.  입자 0 개로 돈다 (입자가 위상에 영향을 줄 리는
  없지만 "같은 조건" 은 아니다).  바이너리가 바뀌면 다시 만든다.

**Q1.** 이 영수증 + 예정각을 L · LC · LH 의 벽 근거로 쓰는 것을 받아들이나 (K2 둘째 경로의 구현으로)?  아니면 "재개 상태 실물" (L 의 실제 restart 파일에서 mesh 를 덤프하는 별도 런) 까지
요구하나 — 후자는 `make_mixer_resume.py` 로 L 의 체크포인트에서 이어 몇 step 만 돌리고 `dump mesh/stl` 을 붙이면 되므로 (재개 덱에 한 줄) 할 수 있다.
**Q2.** 표지 꼭짓점 방식 (덤프 삼각형 순서 = 파일 순서, serial 실행) — 순서가 깨지면 (ii) 가 거짓 실패를 낸다 (거짓 통과는 아니다).  (i) 의 A↔B 좌표 일치가 주 근거로 충분한가.
**Q3.** 허용 0.05° · 리셋 간격 ≥ 1° 의 근거 = 39 각형 면각 9.23° 의 0.5 % / 10 %.  δ/r 로 전파하면 0.05° 는 벽 겹침 ≤ 0.02 %p 다 (⑯b 실측).  적절한가.
**Q4.** `bounded` 판정 (근거 없어도 상한 ≤ 1 % 면 PASS · 하한 > 1 % 면 REJECT) — fail-closed 로 충분한가.  ⑯ 이 그 예다.
**Q5.** 남은 HB-01 (v09 0.212 칸 · PNG) 과 발사 기록 봉인 (§2-5: 실제 STL 내용 · 바이너리 sha · nproc · 시각) 은 **발사 직전**에 한다 — 순서가 맞나.

## 4. 재현

```bash
python3 scripts/check_contact_validity.py --selftest      # 32/32
python3 scripts/measure_mixing_index.py --selftest         # 23/23
python3 scripts/mixer_deck_diff.py --selftest              # 14/14
python3 scripts/mixer_restart_phase_test.py --selftest     # 7/7
python3 scripts/make_mixer_deck.py --selftest              # 89/89 (LH 덱 · 골든 해시 불변)
bash dem_scripts/mixer_20260921/test_launcher.sh           # 31/31
bash scripts/check_all.sh                                  # 게이트
PYTHONDONTWRITEBYTECODE=1 python3 docs/reviews/codex_mixer_highbo_rereview_evidence_20260927/review_probe.py   # 옛 반례 — 이제 assert 가 **실패해야** 한다 (수정됐으므로)
```

## 5. 이 리뷰 뒤 순서
영수증 실행 (WSL) → L 10 런 완주 → `SET=highbo gen_all.sh` → `mixer_deck_diff.py --runs … --allow B --expect-deck <새 생성 LH>` (3/3) → 발사 기록 (§2-5) → 첫 시드 발사 → bin 0 스모크 (`--contract --phase-receipt` · `smoke.tech_smoke`) → 나머지 둘.
