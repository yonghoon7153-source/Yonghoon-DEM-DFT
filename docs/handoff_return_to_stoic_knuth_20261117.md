# 대피 세션 → 본 세션 (stoic) 복귀 인계 (2026-11-17 새벽 · 1저자 11-16 밤 *"이제 새벽되면 여기서 진행하던거 다시 원래 브랜치로 갈건데 3순위 도는것만 여기서 할거야"*)

> **한 줄**: 대피 세션 (pqwtv8) 이 하던 일을 **전부** 본 세션 (stoic) 에 돌려준다 — Rint ② 포함.  대피 세션에는 **litdb 3 순위 (N-76 – N-129 · 보강 N-148 · N-149) 와 그 뒤 추가 필요 목록만** 남는다 (litdb 정본 가지에만 쓴다 · pqwtv8 · stoic 에는 더 쓰지 않는다).  이 문서 커밋 = pqwtv8 의 마지막 커밋이다.

## 0. 붙여 넣을 프롬프트 (본 세션 첫 메시지)

```
대피 세션 (pqwtv8) 이 하던 일을 전부 돌려준다 (1저자 11-17). litdb 3 순위만 대피 세션이 계속한다.
1. git fetch origin claude/stoic-knuth-NObVQ claude/sdcp-dem-manuscript-si-pqwtv8
   → origin stoic 이 af3cce37b 그대로인지 확인 → stoic 을 origin pqwtv8 끝 (이 인계 문서 커밋) 으로 fast-forward → push
   (게이트 = 대피 세션이 이 커밋에서 두 조각 통과 · 다시 불필요).
2. docs/handoff_return_to_stoic_knuth_20261117.md 를 끝까지 읽고 §3 차례대로 이어간다.
3. CLAUDE.md 의 ★ 2026-11-16 실행 우선 줄 (Q1–Q4) 이 지금 규칙이다. 새 SELF 번호 = 원장 최대 + 1 (지금 183).
```

## 1. 무엇이 어디로

| 트랙 | 맡는 곳 (11-17 부터) | 비고 |
|---|---|---|
| **[Rint ②]** 시간 다시 어림 → 봉인 숫자 → Codex 2/2 → 봉인 → R 런 | **본 세션** | 1 순위 · 기한 = GPU 팔 12 월 초 · §3-1 |
| 비 Rint 반입 (Codex 실무 가지 `cherry-pick -x` · 1저자 "반입" 뒤) | **본 세션** | Codex 실무 = 비 Rint 구현 · 반박 판정 수령 그대로 (11-16 쪽지) · §3-2 |
| [DEM 우선] Ⓒ 믹서 E0 수집물 | **본 세션** (판독 = Codex 실무) | §3-3 |
| 믹서 원고 (draft) | **본 세션** | §3-4 |
| litdb 3 순위 · 보강 · 추가 필요 목록 | **대피 세션** (정본 가지 `claude/friendly-meitner-lldvar` 만) | 2 시간 점검 예약 · 끝에 한 번에 보고 · 추가 목록 = 3 순위 끝난 뒤 (1저자 11-16) |

## 2. 가지

| 가지 | 지금 | 규칙 |
|---|---|---|
| `claude/stoic-knuth-NObVQ` (stoic) | origin = `af3cce37b` (11-12 동결 그대로) | 본 세션이 pqwtv8 끝으로 **fast-forward** 한 뒤 여기에 이어 쓴다 |
| `claude/sdcp-dem-manuscript-si-pqwtv8` (pqwtv8) | 이 인계 커밋 = 끝 | 대피 세션은 **더 쓰지 않는다** |
| `claude/friendly-meitner-lldvar` (litdb 정본) | 대피 세션 조수가 push | 본 세션이 litdb 를 건드리면 push 전 fetch · rebase · 상태표 `litdb/_curation/status.tsv` 의 '대피' 줄은 대피 세션 몫 |

## 3. 트랙별 상태 · 다음

### 3-1. [Rint ②] (1 순위)

- 실행 핀 = `64e4d213e` (반입 `dda148932`).  ⑥ 시도 3 · 4 와 11-16 S0 저장본 시험 = 기록됨: `docs/data/rint2_probe6_a3_20261116/` · `docs/data/rint2_probe6_a4_20261116/` · `docs/data/rint2_s0_sbe_20261116/`.
- 시도 3 = 저장본 만들기 포함 9,045 s (탄소 접합 준비 4,011 s) · 시도 4 = 저장본 읽기 (86 s) 4,932 s · 두 시도 풀이 코드 같음 · 주 풀이 반복 277,885 (시도 2 와 같음 · 시도 2 는 옛 핀에서 6 h 12 m) · PROBE_OK · 잔차 1.05e-12.
- **다음** = 이 실측으로 R 런 시간 다시 어림 (`docs/reviews/rint2_time_reestimate_20261111/README.md` 를 갱신 · DBE 준비 시간은 아직 안 잼 = 두 가정 그대로) → 봉인 숫자 (반복 한도 · 시간 상한 · 최대 시도 수 = 11-12 결정 틀) → Codex 2/2 요청서 (측정 결과 + 봉인 숫자 · 발송 = 1저자) → 봉인 → R 런 (kgy · gabia).  kgy 는 지금 돌고 있는 것이 없다.

### 3-2. 비 Rint (Codex 실무)

- 반입 끝 = 11-16 ⑥ (dem-observations 3 · dem-a1-contact 3 · 대응표 `docs/collab/claude_to_codex/20261116-2050_intake-sha-map.md`).  Codex 실무 11-16 밤 = "이걸로 끝" · 다음 일은 갱신된 B 끝에서.
- 11-16 1저자 결정 (진행 기록 11-16 저녁 · 밤 줄): LHS v1.3 = README 한정어 '탈압 전 값 · 모델 내부 ML 기술자' 로 미루지 않음 · G2c′ B 남은 둘 (소비자 사양 · 실패 경로 자격) = 알려진 한계 · Ⓐ 탈압 키트 먼저 · 후막 · COMSOL 넘김 = Ⓐ 와 재설계 뒤 다시 뽑기 (시드 ≥ 3 · 탈압 뒤 · `docs/data/th_comsol_handover_20261106/README.md` 머리 표지).
- Codex 실무 다음 순서 (11-16): Ⓐ 탈압 키트 → LHS v1.3 → [수영] 2D (F 접촉 선택 ①–④ 를 F 의 Φ_m 로 고른 뒤 S/F 비교) → 믹서 E0 수집물 판독 → 후막 (Ⓐ · 재설계 뒤).

### 3-3. 믹서 E0 (잡 366423)

- **COMPLETED · 종료코드 0:0 · 3:53:26** (어림 3.38–4.91 h 안) · 마지막 저장 `mix_1121000` = 계획 `t0_planned` 1,121,000 · 저장 1,121 · 재시작 3 (a · b 번갈아 + settled = 덱대로) · 폴더 25 G (멈춤 권고선 27.3 GiB 아래).  계획 대조까지만 — 자격 판정은 수집 뒤 Codex 실무 판독.
- 수집 = 1저자가 WSL 에서 Codex 수집 TXT (`PASTE_MIXER_E0_COLLECT_366423_20261116.txt` · 첫 반환은 `collection_history/` 로 바이트 보존 · 다시 붙여 넣으면 이어 받기만) — 돌아온 보고서 · 전체 묶음 · SHA256SUMS · remote_screen.txt 를 Codex 실무에 넘긴다.

### 3-4. 믹서 원고 (draft)

- 1저자 11-16: 성능이 본론이어야 한다 → 길 (가) = 코팅 vs 비코팅 셀 성능이 본론 · DEM 믹서 · 판정 지도 = 기전 절 + SI · 실험 값은 가정 (`[가정 XX]` · 방향만) · 윤곽 위주 · 모델 이야기는 짧게.
- v2 (Wiley 꼴 Word 본문 · SI) = 대피 세션이 만들어 1저자에게 보냈다 (리포 밖 · 대외비 가이드 내용 쓰지 않음).  이어 고치기 = 1저자가 Word 를 올리면 본 세션에서.
- 판가름 계산 (코팅 비율 × SE 함량 → 망 σ_ion · 멈춤 규칙 = 결과 전에) = 아직 등록 전 · Codex 실무에 맡길 후보.

## 4. 이 커밋에 든 것

- 11-16 S0 사본 (`docs/data/rint2_s0_sbe_20261116/…/s0_stage1_kit_SBE_vgcf100.json`) 의 원자료 숫자가 철회값 패턴 (CL-33 · CL-41) 과 우연히 겹친 것 → 허용 목록에 더함 (11-08 · 11-13 사본과 같은 처리).  게이트 1 조각이 잡았다 (내 순서 실수 — 게이트 전 스윕을 마지막 트리에서 다시 돌리지 않았다).
- §2 답 쪽지 (피복 · 입자 번호 승계 · 11-16 04:3x UTC 채팅으로 전달한 것) = `docs/collab/claude_to_codex/20261116-0430_coverage-id-answer.md`.
- 이 인계 문서 · CLAUDE.md ★ 줄 · 진행 기록 줄.

## 5. 그대로 지킬 규칙 (원문 = CLAUDE.md)

커밋 하나 → 게이트 두 조각 (`CHECK_ALL_RANGE=1-125` · `126-189` · 같은 HEAD · fail 0 · Bash 배경 · timeout 7200000 · 줄이지 않음) → push · 게이트 전 빠른 점검 셋 (`check_doc_refs` · `check_review_findings` · `--ban-sweep`) 은 **마지막 커밋 트리에서** · 로컬 커밋 쌓지 않기 (쌓이면 bundle 을 1저자에게) · 주소 · 포트 · 계정 · 홈 경로 = 채팅만 (리포는 공개) · 반입 = `cherry-pick -x` (1저자 "반입" 뒤) · 조수 지시서: 시스템 패키지 · `GIT_*` export · 신호 금지 · 실행 우선 Q1–Q4 (11-16) = HOLD 는 P1 만 · 개발 계산은 "개발 자료" 표지로 바로.
