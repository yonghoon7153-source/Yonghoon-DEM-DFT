---
title: "DG 프롬프트 — li2s-2 DF 고침 확인 (947e83ba0): 녹음 판독량 window_mto_v1 · 1 단계 시드 판정 소비자 · 시드 규칙 · 1 단계 러너 — 첫 담금질 전 조건이 닫혔나"
date: 2026-11-03
updated: 2026-11-03
tags: [review, li2s, glass, md, uma, density, quench, runner, codex, prompt, letter]
letter: DG
track: li2s
channel: codex
kind: prompt
status: 초안 (2026-11-03) — 사용자 발송 대기 · 기준 커밋 947e83ba0
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = li2s-2 (논문 1저자 = 외부 · 위임 10-30). DF (ff795d669 · NO-GO · P0 1 · P1 5 · P2 4) 다음 편지다 — **고친 곳만** 본다.
> ⛔ li2s 절대 수송값은 싣지 않는다. 기준 커밋 `947e83ba0` (브랜치 `claude/friendly-meitner-lldvar`). ⬇ 아래 **보내는 글**만 발송한다.
> 회신이 오면 `codex_DG_reply_li2s2_df_fixes_2026_11_03.md` 로 원문 보존.

---

**[li2s-2] DF 고침 확인 — 첫 담금질 전 조건 (판독량 · 실제 중단 연결 · 시드 · 한쪽 계 실패 · R0) 이 닫혔나 · 발사 GO 여부**

## 0. 무엇을 묻나

DF 의 '실행 재개 조건 1 (첫 담금질 전)' 넷을 고쳤다 — **조건마다 닫혔는가 (GO / 조건부 / NO-GO) · 고치면서 새로 생긴 구멍은 없는가 · 1 단계를 띄워도 되는가.**
DF 에서 찬성한 설계 (고정 밀도 NVT · kgy 순차 · 사다리 · 550 K 조건부 · R 주 · ΔEa 조건부) 는 다시 열지 않아도 된다. 2 단계 전 조건 (MD 압력 도구) 은 이번 범위 밖 — 절차만 카드에 박았다.

## 1. 보는 범위

- `git diff ff795d669 947e83ba0 -- tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json`
- 결정 `D-2026-11-03-li2s2-dense-window` (아직 proposed · 문구 갱신) · 실행 기록 `db/properties/lpscl_glass_dense_window_runlog_2026_11_03.json` 의 `회신_DF_2026_11_03`
- 시험: `python3 tools/ionic/melt_quench_uma.py --selftest` (⭕ 152) · `python3 tools/ionic/li2s2_stage1_runner.py --selftest` (⭕ 15)

## 2. DF 지적별로 한 것 (반례 재현 → 지금 막는 시험)

**P0 녹음 판독량** — 새 `--melt_window_check` (`melt_window_check` · `window_mto_v1`): 창 [melt/2, melt] = [50, 100] ps **안의 프레임만** 읽고 (`_leading_frames` — 쓰는 중인 반쪽 프레임에서 멈춤) **창 안 시간원점만** 쓴다 (`window_mto_msd` — 창 첫 프레임 기준 분수좌표 unwrap · 전체 병진 제거 · 지연 k 마다 모든 (j, j+k) 쌍). 지연 2–25 ps 자유절편 맞춤 → D_P > 1e-6 cm²/s.
- 창 전체 확보 (50 · 100 ps 프레임 둘 다) 가 아니면 `incomplete` + **실제 쓴 창**을 적는다 · 좌표 NaN → `invalid` · 압축 끝 > 창 시작 → `invalid` · 도구도 `--compress_ps ≤ melt/2` 를 입력에서 거부한다.
- 문턱 1e-6 은 옛 진단값 **승계** — 카드 `기계_판독_값.melt_window.threshold_source` 와 결정 문구에 결과 전에 적었다. 옛 `--melt_check` 는 그대로 두되 고정 밀도 plan 이면 거부한다 (옛 진단 결과는 안 건드림).
- 시험: DF 반례 그대로 — 창 좌표가 같고 앞 50 ps 이력만 다른 두 궤적 → **같은 D · 같은 판정** · 창 안이 얼어 있고 앞만 크게 움직인 궤적 → 미충족 · 70 ps 에서 끊긴 궤적 → 미완 + [50, 70] · 반쪽 프레임 · 겹침 · NaN.
- 깨기: 창 원점을 0 ps 로 되돌리면 반례 시험이 빨강 · 창 확보를 안 보면 끊김 시험이 빨강.

**P1-2 종료코드 ≠ 카드 통과** — `gate_check` (NVT) 에 ① 계획 일정 완주 (thermo 끝 ≥ melt + 담금질 + 유지 − save) ② 판정 창 (마지막 10 ps) 이 실제 300 K 유지 구간 안 (T_set = T_final · 유지 길이 ≥ 0.9 × hold_ps) ③ 압력 **기록** (총압 · virial 이 유한 — 크기는 판정 안 함) 을 더했다.
그리고 소비자 `--stage1_verdict` (`combine_stage1` 순수 함수 + `stage1_verdict` 수집): 카드 일정 · 고정 밀도 · 소프트웨어 기록 (`plan.json software` — fairchem · torch · ase · 모델 · 추론) · 파일 · gate_check 필드 · 녹음 판정 · 시드 게이트 (relax 본 PS₄ = 1 ∧ 최단 원자간 (P–S 제외) > 2.0 Å) 를 **직접** 읽어 pass · fail · incomplete · invalid (우선순위 invalid > incomplete > fail).
- 시험: DF 반례 — melt 기록만 (밀도는 맞음) → 통과 못 함 · 압력 NaN → '압력 기록 없음' 으로 통과 못 함 · 시드 판정 10 갈래 (PS₄ 0.9167 · 최단 1.98 · 녹음 미충족 · 미완 · 일정 미완 · 압력 없음 · 파일 없음 · 밀도 1.9 · melt 80 ps · 소프트웨어 없음).

**P1-3 시드 · 한쪽 계** — `--stage1_summary` (`summarize_stage1`): 계마다 통과 ≥ 4 면 통과 · 탈락이 (시드 수 − 4) 를 넘으면 그 계 닫힘 → **트랙 전체 멈춤** · 2 단계 시드 = 두 계 **모두** 통과한 시드 중 작은 둘 (기계 그 순서로 kgy · gabia) · 공통 통과 < 2 → 멈춤 · 통과 시드의 소프트웨어가 둘 이상 → 무효.
- 시험: DF 예 (A11 탈락 · A12–15 통과) → 2 단계 시드 [12, 13] · A 3/5 → 트랙 멈춤 · 대기 · 판 둘 → 무효.

**Q-DF-3 실제 중단 연결** — 새 러너 `tools/ionic/li2s2_stage1_runner.py`: 결정 active · 드라이버 sha16 고정 (`f5063afca93dbf31`) · 잠금 · 판정 없이 런 폴더가 있으면 멈춤 (덮어쓰지 않음) · GPU 가 두 번 연속 빌 때까지 기다림 · 누적 벽시계 + 한 시드 최악 > 상한이면 새 시드를 안 띄우고 '미완결' 로 멈춤 · **계의 첫 시드는 --poll_s 마다 녹음 판정 → 미충족 · 무효면 그 담금질의 프로세스 그룹을 죽이고 판정 파일 · STOP.json 을 쓰고 멈춘다** · 담금질 rc ≠ 0 → 멈춤 · 시드마다 stage1_verdict → stage1_summary.
- 시험 15 (가짜 GPU · 프로세스 · 시계 · 판정 · 묶음 판정은 진짜 `summarize_stage1` + 진짜 카드 값) · 깨기 5/5 (녹음 미충족에도 안 멈춤 · 묶음 멈춤 무시 · 상한 안 봄 · 결정 안 봄 · 끊긴 런 덮어씀).

**R0** — LiCl 2.07 (20 °C) 은 DF 가 확인한 제조사 물성표로 기록 · A 목표 그대로 (카드 §4 R0).

**문구 (P1-5 · P2)** — '과냉각 액체' 철회 → 'T₅₀ 거리 + 지정 밀도 · 온도 구간의 겉보기 온도 의존성 · 등적 경로' · '계별 구조 시드 재표집' · 구조 시드 재사용의 선택 효과 기록 · '밀도 하나만 바꾼 깨끗한 대조' 삭제 · B '실험 참조' / A '부피가법 참조' · 비용 합계 (조건부 포함 222–522 GPU-h) · 상한 회계 = 런 벽시계 전부 · 미완결 종료 가능 (카드 §개정_DF_2026_11_03).

## 3. 이것을 특히 봐 달라

1. `window_mto_msd` 가 창 밖 정보를 정말 못 받는가 (unwrap 기준 · 병진 제거 · 지연 범위 2–25 ps 가 창 50 ps 에 맞는가) · 문턱 승계가 새 판독량에서도 같은 뜻인가.
2. `combine_stage1` 의 우선순위와 '일정 미완이면 창 · 밀도 · 압력 실패를 fail 로 세지 않는다' 가 맞는가.
3. 러너의 정지 경로 — 프로세스 그룹 kill (`start_new_session` · `killpg`) 이 그 담금질만 죽이는가 · 첫 시드가 아닌 시드의 녹음은 끝난 뒤 판정 파일에서만 보는 것 · 상한 셈 (관측 최댓값) · 재시작 때 판정 파일이 있는 시드만 건너뛰는 것.
4. 새로 생긴 조용히 틀린 경로가 있는가 (예: 러너의 진짜 판정 함수 호출 인자 · 카드 기계_판독_값 와 카드 본문의 불일치).

## 4. 회신 꼴

판정 (GO / 조건부 GO / NO-GO) · 지적 (P0 · P1 · P2 · 각각 무엇 · 왜 · 최소 수정) · DF 지적마다 닫힘 여부 한 줄.
