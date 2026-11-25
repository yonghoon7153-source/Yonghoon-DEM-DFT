---
title: "CT 프롬프트 — cascade D_rel v7 본 라운드 러너 (--main) 코드 리뷰: 이미 돌고 있는 40 런 · 조용히 틀린 경로 · 판정까지 이어지는가 · 확인 요청 여섯"
tags: [review, cascade, d_rel, v7, main-round, runner, code-review, silent-wrong-path, codex, prompt, letter]
letter: CT
date: 2026-10-07
track: cascade
channel: codex
kind: prompt
status: 발송 완료 2026-10-08 · ✅ 회신 수령 2026-10-08 → `codex_CT_reply_cascade_v7_main_runner_2026_10_08.md` (조건부 GO · P0 없음 · P1 3 · 도는 MD 계속)
confidence: medium
verificationStatus: verified
verifiedAt: 2026-10-07
verifiedBy: self
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = cascade → **사용자가 1저자**다 (통지할 제3자 없음). 이 편지는 **이미 돌고 있는** 본 라운드 러너의 사후 코드 리뷰다 — P0 가 나오면 멈출지 사용자가 정한다.
> 기준 커밋: 러너 `d283ce5` (kgy worktree `~/wt_cv7main_1007` 가 이 커밋으로 돈다) · 감시 도구 `cd014ec` · 기록 `ac06894`.
> ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_CT_reply_…` 로 원문 보존.

---

**[cascade D_rel] v7 본 라운드 러너 (`run_cascade_v7_probe.py --main`) — 이미 40 런 중 1 번째가 돈다 · 코드 리뷰 요청**

## 1. 어디까지 왔나

- 카드 `db/properties/cascade_estimand_card_v7_probe_2026_10_01.json` + 개정 `…_amendment_cp_2026_10_03.json` (당신의 회신 CP 이행 · 결정 둘 active).
- 탐침 끝 (10-06): **T\* = 1000 K** — 800 K 는 H0 seed 1 자격 미달, 1000 K 는 H0 두 시드 + 대표 쌍(부모 C · P1/P2 · 시드 3·4) 네 런 전부 자격 통과 · 골격 경보 없음. 7 런 73.07 / 141 GPU-h. 판독 산출물 repo 사본 `db/raw/cascade_v7_probe_2026_10_03/cascade_v7_probe.json` (SHA256SUMS 22 일치).
- 본 라운드 상한 결정 `D-2026-10-07-cascade-v7-main-round-cap` **active** (461.4 GPU-h = 탐침 실측 단가 최댓값 11.5341 × 40 · 넘으면 다음 런 안 띄우고 보고).
- **10-07 20:04:49 kgy 발사** — tmux `cv7main` · 첫 런 `P1_Al2O3_A__T1000__s1`. 사전점검 dry_run 통과 (준비 20 구조 해시 = repo 구조 · 드라이버·판독기 sha 탐침과 같음 · 판독기 selftest PASS). 실행 기록 `db/properties/cascade_v7_main_runlog_2026_10_07.json`.

## 2. 리뷰 대상

- `tools/doping/run_cascade_v7_probe.py` — `--main` 모드를 탐침 러너에 덧붙였다 (새 파일 아님). 새로 쓴 곳: `DECISION_MAIN` · `PROBE_JSON` · `MAIN_SEEDS` · `MAIN_EST_GPU_H_PER_RUN` · `main_roster` · `main_constant_errors` · `decision_gate(ids, cap_id)` 일반화 · `meta_expect`/`md_cmd` 의 `label` · `preflight` 의 main 분기 · `manifest_of` main 필드 · `resume_check` 의 schema·T\*·탐침 산출물 해시 대조 · `run_main` · `status` 표시 · selftest 의 '본 라운드' 절.
  탐침에서 쓰던 `run_one` (한 런 실행 · run_meta/추론 모드/md.log dt 감시 · 끝난 뒤 산출물 검사 · 시간 누적)은 **그대로 재사용**한다.
- `tools/doping/watch_cv7probe.py` — manifest schema 가 본 라운드면 판독 산출물을 읽지 않고 명단 진행 n/40 만 보인다.
- 끝에서 쓸 판독기 경로 (이번에 안 고침 · CP 개정 때 씀): `tools/doping/judge_eprime.py` `main_v7` · `v7_main_runs` · `v7_probe_t_star` · `missing_runs` · `judge_runs_card(binding, alarm=True)`.

## 3. 설계 (결과 전 고정)

1. **명단 고정** — T\* (탐침 산출물 · 기본 repo 사본) × 부모 10 (v6 원장 `load_v6_pairs`) × P1/P2 × 시드 1·2 = 40 런. 순서 = 시드 1 의 부모 A→J (P1, P2) 다음 시드 2. 판독기가 고르지 않는다. 탐침 시드 3·4 는 명단에 없다.
2. **런 사이 판독기 호출 없음** = 중간 집계 없음. 40 런이 끝나면 판정 명령 한 줄만 찍고 멈춘다 (`judge_eprime.py --card v7 --probe_json … --out_root …` 는 사람이 친다).
3. 상한 = 원장 결정의 `cost_cap.total_gpu_h`. 단가 = 본 라운드 실측 최댓값 (없으면 11.5341). `누적 + 단가 > 상한` 이면 그 런을 안 띄우고 rc 3. 끊긴 런의 시간도 누적된다.
4. 결정 셋(카드 · 개정 · 상한)이 active 가 아니면 시작 안 함. 탐침 산출물은 `v7_probe_t_star` 로 읽고 (T\* 사다리 안 · 프로토콜 · 대표 부모 대조) 해시를 manifest 에 박는다. 이어받기는 manifest schema · T\* · 탐침 산출물 해시 · 드라이버 해시 · frozen 이 같아야 한다.
5. 이미 끝난 런 (msd.json + budget 에 ok 기록) 은 건너뛴다 · msd.json 은 있는데 budget 기록이 없으면 rc 6 · msd.json 없이 폴더만 있으면 rc 11 (사람이 attic 으로 옮김).
6. 준비 구조는 v6 prep 를 초기 좌표로만 재사용 (개정 ⑩) — 원본 기록 검사 → out_root/prep 복사 → 해시 고정.
7. 라벨 `cv7main_<구조>` (판독기는 라벨을 안 읽고 폴더 태그 `<구조>__T<T>__s<시드>` 를 읽는다).

시험: selftest 104 ✓ (본 라운드 절 23 · 음성 포함). 일부러 깨기 7/7 빨강 — 런 사이 판독기 호출 · 시드 (1, 3) · 상한 결정 누락 · T\* 이어받기 검사 제거 · budget 기록 검사 제거 · 상한 게이트 제거 · 라벨.

## 4. 확인 요청

- **Q-CT-1 (조용히 틀린 경로)** — 선언(카드 · 개정 · 상한 결정)과 실행 경로가 다른 곳이 있는가? 특히 탐침용으로 쓴 `run_one` 을 본 라운드에서 그대로 쓸 때 빠진 검사, `preflight` main 분기에서 탐침 쪽 검사(`constant_errors` 등)와 겹치거나 비는 곳, 이어받기 승계에서 누적·단가가 어긋날 수 있는 경로.
- **Q-CT-2 (판정까지 이어지는가)** — 40 런이 끝났을 때 `main_v7` 이 이 out_root 를 그대로 읽는가 (scan 경로 · 태그 · T 필터 · 시드 필터 · `missing_runs`)? 그리고 **본 라운드 자격 경로**(`judge_runs_card` · binding · alarm)가 탐침이 T\* 를 고를 때 쓴 자격 정의와 **같은가** — 다르면 T\* 선택의 근거가 본 라운드로 옮겨지지 않는다.
- **Q-CT-3 (순서)** — 시드 우선 순서 (시드 1 의 20 런 → 시드 2 의 20 런) 가 맞는가, 부모 우선 (부모마다 4 런) 이 맞는가? 상한에 걸려 중간에 멈추면 판독기는 40 런이 다 없으면 판정을 거부한다 — 그때 남는 집합의 쓸모·위험이 순서에 따라 다른가?
- **Q-CT-4 (비용 게이트)** — 첫 단가가 GPU 공유 상태의 탐침 최댓값이고 본 라운드는 kgy 단독이다. 실측 최댓값 게이트가 너무 느슨하거나 빡빡해지는 경우가 있는가? 끊긴 런 시간 누적은 맞게 되는가?
- **Q-CT-5 (중간 집계 차단)** — 러너·감시 도구는 D 를 열지 않는다. 그러나 드라이버가 `logs/<태그>.log` 와 `msd.json` 에 D 를 쓴다 — 사람 규율만으로 충분한가, 러너 쪽에서 더 막을 것이 있는가?
- **Q-CT-6 (판정)** — 계속 / 조건부 계속 / 멈춤 (GO / 조건부 GO / NO-GO) 과 P0 · P1 · P2 로 답해 주길 바란다. ⚠ 멈추면 도는 런(한 런 ≈ 8–11 h)을 잃는다 — **결과를 무효로 만드는 것만** P0 로, 나머지는 다음 런 사이에 고칠 수 있는지 같이 적어 주길 바란다.
