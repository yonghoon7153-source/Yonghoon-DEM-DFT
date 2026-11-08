---
title: "대피 인계 — 2026-11-08 (friendly 세션 토큰 소진 → 서브 대시보드 세션 · 머지 때 충돌 0 설계 · li2s-2 1 단계 kgy 진행 중 · cascade 문헌 갭 다음 단계)"
date: 2026-11-08
updated: 2026-11-08
tags: [handoff, session, evacuation, branch, merge, li2s, glass, md, uma, runner, cascade, litdb]
status: 진행
kind: project
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# 대피 인계 — 2026-11-08

> 본 세션 (`claude/friendly-meitner-lldvar` · session …CTzs) 의 토큰이 다 떨어져서, 다음 세션은 **서브 대시보드의 서브 브랜치에서** 이어 간다
> (사용자 2026-11-08 *"여기 토큰 다 차서 넘어가야될듯, 서브 대시보드/브랜치로 · 충돌안되게 저번에 했던것처럼 잘 머지할 수 있도록 프롬프트 써줘"*).
> 선례: `handoff_2026_10_22_evacuation.md` (대피) → `handoff_2026_10_26_return_to_origin.md` (복귀 · fast-forward · 충돌 0).
>
> **충돌 0 의 조건 — 대피하는 동안 이 세션은 friendly 에 쓰지 않는다.** 이 카드를 담은 커밋이 이 세션의 friendly 마지막 커밋이다.
> ⚠ **이번엔 예외가 하나 있었다**: 11-06 12:27 UTC 에 **다른 세션**이 friendly 에 litdb 커밋 `ce4f267d` (schmitt2026 건식 PTFE 시트) 를 바로 올렸다
> (이 세션 것이 아니다 · 이 세션은 그 위로 rebase 해서 이어 갔다). 그러니 복귀 때 friendly 가 이 카드 커밋에서 더 나가 있을 수 있다 → §6 의 갈래 ② (머지) 로 간다.

## 0. 새 세션 (서브 대시보드) 에 붙여 넣을 프롬프트

```text
[대피 세션 시작 — 2026-11-08 · 서브 대시보드]

너는 Yonghoon-DEM-DFT 캠페인의 임시 대피 세션이다. 본 세션(브랜치 claude/friendly-meitner-lldvar)이 토큰을 다 써서
이 서브 브랜치로 옮겨 왔다. friendly 세션이 하던 일을 그대로 이어 간다. 나중에 사용자가 "돌아가자" 하면
이 브랜치를 friendly 로 **충돌 없이** 되돌린다 — 그 조건이 아래 ■1 · ■5 · ■6 이다.

■ 1. 브랜치 (제일 먼저)
- 이 세션 브랜치 = 너의 시스템 지시에 적힌 개발 브랜치 (아래 <이 세션 브랜치>).
- git fetch origin claude/friendly-meitner-lldvar
- git log --oneline -3 origin/claude/friendly-meitner-lldvar → 맨 위가 "Evacuation handoff card 2026-11-08" 커밋이어야 한다
  (그 아래 24408d22 "li2s-2: correct the 11-07 GPU note"). 그 위에 커밋이 더 있으면 누가 올렸는지 (git log --format='%h %an %ad %s') 보고
  사용자에게 알린다 — 11-06 에 다른 세션이 litdb 커밋을 바로 올린 전례가 있다 (ce4f267d). 카드 커밋이 아예 없으면 멈추고 말한다.
- 이 세션 브랜치가 friendly 끝을 포함하지 않고 아직 내 커밋도 없으면 friendly 끝에서 시작한다:
    git checkout -B <이 세션 브랜치> origin/claude/friendly-meitner-lldvar
  (첫 push 가 non-fast-forward 로 거절되면 그 원격 브랜치에 내 커밋이 없는지 확인한 뒤에만 --force-with-lease.) 이미 내 커밋이 있으면 멈추고 묻는다.
- 브랜치를 옮겼으면 CLAUDE.md 를 다시 읽는다.
- ⛔ friendly 에는 push 하지 않는다. CLAUDE.md 의 "friendly 에만 커밋/푸시" 는 이 세션에서 "friendly 에는 쓰지 않는다 · 커밋 · 푸시는 <이 세션 브랜치> 에만"
  으로 읽는다 (사용자 2026-11-08 대피 지시). friendly 반영은 ■6 대로만.
- ⛔ 원격 (kgy · gabia) 에서 git fetch · push 하는 블록도 <이 세션 브랜치> 를 쓴다 (friendly 로 push 하면 복귀가 꼬인다).
- PR 만들지 않는다 · force-push 는 --force-with-lease 만 · 커밋 메시지에 모델 ID 를 넣지 않는다.

■ 2. 먼저 읽을 것 (큰 파일은 grep · 부분 읽기)
- kb/projects/handoff_2026_11_08_evacuation.md ← 이 인계 카드 (§1–§6 통째로)
- kb/open_items.md 머리 (6 번째 줄 '최종 갱신') 와 ⏭-NOW-z29 의 li2s-2 줄 · cascade 줄 (grep -n "li2s-2 새 트랙\|11-06 방향 점검" kb/open_items.md)
- li2s-2: 카드 db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json 의 개정_DT_회신_조건_v14_2026_11_06 (운영 범위 — 반드시) ·
  runlog db/properties/lpscl_glass_dense_window_runlog_2026_11_03.json 의 키 발사_2026_11_06 · 진행_2026_11_07 · 확인_2026_11_08 · ⏭
- cascade: reports/황화물 분해 부피 도펀트 문헌 갭.md (끝의 '본문으로 열어야 할 논문' 표)
- 값 · 판정은 원장이 이긴다: db/governance/decisions.json · db/properties/canonical_registry.json · db/properties/citation_hazards.json

■ 3. 시작 점검 (대피 직전 friendly 실측 기대값을 옆에 적었다)
  python3 tools/kb_wiki.py lint | tail -1                 # RESULT: 0 errors
  python3 tools/db/validate_canonical.py | tail -3        # 거버넌스 결정 168 · 판정 8 · 그래프 무결성 ✅ · 배선 전부 일치
  python3 tools/convention_check.py | tail -1             # RESULT: 0 위반
  sha256sum tools/ionic/melt_quench_uma.py tools/ionic/li2s2_stage1_runner.py | cut -c1-16   # 1ca75960fa21f4e8 · 00e08de0f75a7869
  (selftest 은 필요할 때만 — 드라이버 254 · 러너 160 (Linux) · 몇 분씩 걸린다)

■ 4. 지금 상태와 할 일 — 인계 카드 §1–§4. 요약:
- li2s-2 (논문 1저자 = 외부 · 위임 10-30 — 이 트랙의 결정은 에이전트가 정해서 진행하고 원장에 '사용자 (위임 10-30)'):
  1 단계가 kgy 에서 돌고 있다 (tmux li2s2s1 · 11-06 21:22 KST 발사 · Codex DT 조건부 GO). A11 = fail (PS₄ 보존율 11/12 < 1.0) ·
  B11 녹음 통과. 카드 규칙: 계마다 5 중 4 통과 — A 는 탈락 하나를 이미 썼다 (하나 더면 트랙 닫힘). 운영 (카드 v14):
  kgy 한 기계 · 도는 동안 --stage1_verdict 로 들여다보지 않는다 · STOP 이면 --ack_stop 전에 시계 영역 대조 (§1-3).
  ⛔ 1 단계가 도는 동안 tools/ionic/melt_quench_uma.py · li2s2_stage1_runner.py · 카드 기계_판독_값을 바꾸지 않는다 (kgy worktree 9e18cd4e 가 그 판에 묶여 있다).
- cascade (1저자 = 사용자): 문헌 갭 보고서 끝 → 🔔 사용자가 다섯 편 PDF 를 올리면 논문 에이전트 (litdb-curator) 로 본문 확인 → 갭 판정 → 보고량 카드 (부피 회계 규약 먼저). 계산 없음.
- litdb: noh2026 (LFP 전도성 바인더) · liu2026 CCTO (이온겔 중간층) digest 끝. 선택 과제 하나 (§3).
- 원격: kgy = li2s-2 1 단계 (esp 계정 GPU 앱은 그대로 둔다 · --start_max_mib 6000) · gabia · ibb = 유휴 (승인된 계산 없음).

■ 5. 머지 충돌을 안 만드는 규칙
- 생성 파일은 손으로 고치지 않는다 — kb/index.md (python3 tools/kb_wiki.py index) · kb/reviews/INDEX.md (python3 tools/kb_wiki.py reviews --write).
- kb/open_items.md: 머리 '최종 갱신' 줄은 앞에 덧붙이고 (옛 내용은 그대로 뒤로) · 트랙 줄은 끝에 '⏩ **날짜**: …' 로 덧붙인다. 옛 문장을 지우거나 고쳐 쓰지 않는다.
- db/governance/decisions.json: 내가 다루는 결정만 고친다 · ratification 이 있는 결정은 내용을 바꾸지 않는다 (decision_digest 가 깨진다) — 새 사실은 새 결정이나 runlog 에.
- litdb/INDEX.md · comparison_vs_ours.md · litdb/figures/_sources.json: 행 · 항목을 덧붙이기만 한다 (다른 세션도 litdb 를 쓴다).
- JSON 원장은 indent=1 · ensure_ascii=False 형식을 지킨다 (원자적 교체 — 임시 파일 → os.replace).

■ 6. 복귀 (사용자가 "돌아가자" 할 때)
- 이 세션이 kb/projects/handoff_<날짜>_return_to_origin.md 를 쓴다 (선례 handoff_2026_10_26_return_to_origin.md) — §0 에 friendly 세션용 프롬프트.
- friendly 가 이 카드 커밋에서 안 움직였으면: friendly 쪽에서 git merge --ff-only origin/<이 세션 브랜치> 한 줄 (충돌 0).
- friendly 가 움직였으면 (다른 세션 커밋): 이 세션 브랜치에서 먼저 git merge --no-ff origin/claude/friendly-meitner-lldvar →
  충돌은 생성 파일이면 도구로 다시 만들고 · litdb 표 · open_items 는 양쪽 행을 다 남기고 → lint 0 · validate ✅ 확인 → push → 그 다음 friendly 쪽은 ff-only.
- 복귀 카드에 원격 상태 (kgy li2s-2 진행 · 마지막 실측 시각) 와 이 세션에서 바뀐 원장 목록을 적는다.
```

## 1. li2s-2 — 1 단계 kgy 진행 중 (트랙 li2s · 논문 1저자 = 외부 · 위임 10-30)

### 1-1. 무엇이 돌고 있나
- **kgy** `tmux li2s2s1` — 러너 `tools/ionic/li2s2_stage1_runner.py --worktree /home/kgy/wt_li2s2 --run_root /home/kgy/work/runs/li2s2_dense_1103 --python /home/kgy/apps/miniforge3/envs/uma/bin/python --start_max_mib 6000`
  - 발사 11-06 21:22:28 KST · worktree `~/wt_li2s2` = `9e18cd4e` (도구 · 카드 · 결정 = `5a8a019a` 와 같다 — 그 사이 커밋은 문헌 노트뿐) · 결정 `D-2026-11-03-li2s2-dense-window` **active** (비준 digest · 위임 10-30)
  - 순서 A11 → B11 → A12 → B12 → … → B15 (계 번갈아 · 한 번에 하나)
  - **A11**: 11-06 21:23 → 11-07 10:33 (≈ 13.2 h) · 녹음 판정 통과 · 시드 판정 **fail** — `PS₄ 보존율 0.9166666666666666 < 1.0` (12 P 중 11) · closes_system False
  - **B11**: 11-07 10:34 시작 · 11:49 녹음 판정 통과 · 11-07 14:21 에 305 / 1051 프레임 (≈ 80.5 프레임/h → 끝 ≈ 23:45 KST) — 그 뒤 A12 가 떴을 것 (11-08 13:36 nvidia-smi 에 uma python 1 개 4,484 MiB 가 돌고 있었다 · 어느 시드인지는 미확인)
  - 속도: 10 시드 ≈ 132 GPU-h (상한 230 안) · 끝 ≈ 11-12
- GPU (11-08 13:36): 합계 8,579 MiB · 우리 MD 4,484 · esp 앱 (grape_twin 3,186 · kiwi_twin 350) + Xorg · gnome-shell · `/home/kgy/miniconda3/bin/python` (PID 1390 · 306) ≈ 4,025 (발사 전 바닥 3,999 그대로) → 시드가 끝나면 합계 ≈ 4 GB 로 돌아가 6,000 문턱이 다음 시드를 막지 않는다.
  ⚠ 11-07 기록의 '우리 밖 ≈ 3 GB' 는 틀린 추정이었다 (runlog `진행_2026_11_07.⏩_정정_2026_11_08`).

### 1-2. 카드 규칙 (결과 전 · 재해석 금지)
- 시드 판정: `seed_gate` relaxed — PS4_fraction_min 1.0 · min_pair_excl_PS_A_gt 2.0
- `stage1_need_pass` 4 — **계마다 5 중 4 이상 통과** · 탈락이 둘 이상이면 그 계가 닫히고 두 유리 비교 트랙 전체가 멈춘다 · 두 계 모두 ≥ 4/5 면 2 단계 시드 = 공통 통과 시드 중 작은 둘 (`--stage1_summary`) · 공통 통과 < 2 면 멈춤
- 첫 시드 녹음 미충족만 그 계를 닫는 사건 (A11 · B11 은 녹음 통과)
- **A 는 탈락 하나를 썼다** → A12–A15 중 하나라도 fail 이면 트랙 닫힘 (그때 마감 기록 `db/properties/<계>_closed_<날짜>.json` — 확정 · 허용 · 금지 · 재개 조건 · CLAUDE.md §마감 규율)
- 상한 230 GPU-h — 닿으면 러너가 미완결로 멈추고 사용자 결정

### 1-3. 운영 범위 (카드 개정_DT_회신_조건_v14 · Codex DT 조건부 GO 의 조건 ②)
- ① 담금질 · 러너 판정 · 사람 판정 · 재개는 전부 **kgy 한 기계** · 런 폴더를 다른 기계로 옮겨 판정하지 않는다
- ② 도는 동안 사람이 `--stage1_verdict` 로 들여다보지 않는다 (판정 파일을 cat · json 으로 읽는 것은 된다 — 11-08 A11 판정 파일 읽기가 그 예)
- ③ **STOP 이면 `--ack_stop` 전에 시계 영역 대조** — 발사 때 기록 (`/home/kgy/work/runs/li2s2_dense_1103/clock_domain_start.txt` · runlog `발사_2026_11_06.시계_영역`):
  host `esp-Z590-AORUS-MASTER` · boot_id `fddca72b-d45e-4ae9-a9e6-68e301949eeb` · boot_at 2026-10-30 13:49:48 · NTP=yes · NTPSynchronized=yes.
  같은 다섯 줄을 다시 재서 host · boot_id 가 같고 NTP 동기면 그대로 · 다르면 (재부팅 등) 시각 비교에 기대는 복구는 확인하지 않고 사람이 본다. 정전 재시도 (끊긴 런을 새 폴더 · 새 run_id 로) 는 이 항목 밖 (카드 정전 복구 규칙 그대로).
- ④ 도구가 지키는 것이 아니다 — 운영 전제다.

### 1-4. 감시 · 확인 블록 (사용자에게 줄 때 · CLAUDE.md: watch -n 30 꼴 · 따옴표 안 `$HOME`)
```bash
watch -n 30 'tail -n 5 $HOME/work/runs/li2s2_dense_1103/stage1.log | cut -c1-140; for d in $HOME/work/runs/li2s2_dense_1103/[AB]/seed*; do [ -d "$d" ] && echo "$(basename $(dirname $d))/$(basename $d) frames $(grep -c Lattice= $d/traj.xyz 2>/dev/null)"; done | tail -2; nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader'
```
- 시드 판정 파일 읽기 (들여다봄 아님): `cd /home/kgy/work/runs/li2s2_dense_1103/<A|B>/seed<S> && python3 -c "import json;d=json.load(open('stage1_verdict.json'));print(d.get('status'),d.get('closes_system'));print(json.dumps(d.get('reasons'),ensure_ascii=False)[:800])"`
- 받은 출력은 runlog 에 새 키 (`진행_<날짜>`) 로 적는다 · open_items li2s-2 줄 끝에 `⏩` 로 덧붙인다.

### 1-5. 1 단계가 끝나면
- 러너가 `stage1_summary` 를 내고 멈춘다 (통과 → 2 단계 시드 · 닫힘 → 트랙 마감). 2 단계 (kgy + gabia · 시드–기계 대응) 는 카드의 2 단계 절을 먼저 읽고, 필요하면 2 단계 러너 · 블록을 만든다 (결과 전 규칙을 바꾸지 않는다).
- 1 단계 결과 회수 (scp → `db/raw/…` · 해시 대조 · 회수 기본 경로 `C:\Users\Administrator\Downloads\` 는 사용자 PC 쪽) 는 CLAUDE.md 의 회수 관례대로.
- ⛔ li2s 절대 수송값 비인용 · 상대 차만 (원장 규율 그대로).

## 2. cascade — 새로움 문헌 갭 다음 단계 (1저자 = 사용자)
- 11-06 사용자 *'권고대로'* → A · B 둘 다 · B 부터 문헌 갭 확인 → 보고서 `reports/황화물 분해 부피 도펀트 문헌 갭.md` (노트 `research_notes/황화물 분해 부피 도펀트 문헌 갭/`).
- 결론: **개념은 둘 다 선점 · 비어 있는 것은 한 아지로다이트 호스트의 도펀트별 숫자 표**.
  - B: 분해 ΔV/V 는 Wang–Mollenhauer 2026 (황화물 7 종 히트맵 · 숫자 · 도펀트 없음) · Xin Li 계열 (구속 열역학 · Cl 함량 계열만) 이 있다 → 남은 자리 = 도펀트별 두 전위 표 · 회계 규약 (Li 저장소 · 기체 · 정규화 · 국소/셀) · 양극 쪽 산화 수축 → 접촉 손실 · 역학 환산.
  - A: 이로운 산물 도핑은 실험 약 20 편의 상식 · 산물 물성 순위는 코팅 (Sundar 2025) · 물질 전체 (Lomeli 2024) 뿐 → 남은 자리 = SE 도펀트별 산물 품질 점수 · 금속 소수상 분율 · 연결 · Li⁺ 방출량.
- 🔔 **사용자 대기**: 갭 단정 전 본문 확인 다섯 편 — Wang–Li 2022 *JACS Au* 2, 886 · Fitzhugh 2021 *EES* 14, 4574 · Fitzhugh 2019 *AEM* 9, 1900807 · Tian 2020 *JES* 167, 090541 · Zhu 2016 *JMCA* 4, 3253. 사용자가 PDF 를 올리면 litdb-curator 로 digest → 보고서 표의 '결과가 바꾸는 것' 열대로 갭을 고친다. (출판사 호스트는 이 세션 네트워크에서 막혔었다 — 허용하려면 환경 설정 변경 승인 카드.)
- 갭이 살아 있으면: **보고량 카드를 숫자 보기 전에** — 부피 회계 규약 넷 · 판정 게이트 (CLAUDE.md §계산 규율). 그 다음 cascade 축 ① · ③ 카드 (`db/properties/cascade_axis_ncm_interface_estimand_2026_11_04.json` · `cascade_axis_li_anode_estimand_2026_11_04.json`) 의 R3 반응식에 MP 몰부피 · 산물 점수를 붙인다. 그 전 cascade 계산 없음.
- 세미나 15 쪽 질문 셋 (교수님 답) 도 아직 원장에 없다 (11-06 방향 점검).

## 3. litdb · 기타
- 11-06 digest 둘: `litdb/papers/noh2026_pedotpss_peg_swcnt_binder_ultrahigh_loading_lfp.md` (LFP 전도성 바인더 · PEDOT⁺/PSS⁻ 도핑 모델 = 우리 sdcp_doped 와 같은 구성 · 스핀 미보고) · `litdb/papers/liu2026_ccto_colossal_dielectric_interlayer_dry_lpscl.md` (CCTO 이온겔 중간층 · 바인더 아님 · 판독 도구 `tools/litdb/liu2026_ccto_readout.py` selftest 통과).
- 선택 과제 (사용자 결정 · 낮은 우선): noh2026 을 `kb/syntheses/binder_adsorption_charge_state_2026_08_29.md` 의 넷째 사례로 넣을지.
- CEI 1저자 (박재현) 11-06 세미나 덱 같이 읽기 = 기록만 (사용자 *'이미 내 손에 떴어'*).
- 다른 세션이 friendly 에 litdb 커밋을 올린 전례 (11-06 `ce4f267d` schmitt2026) — litdb 표는 덧붙이기만 (■5).

## 4. Codex · 리뷰
- li2s-2 Codex 편지 DF → DT 끝. DT 조건부 GO (`kb/reviews/codex_DT_reply_li2s2_ds_fixes_2026_11_06.md`) → 조건 ① 카드 v14 · ② 운영 범위 → 결정 활성 · 발사. 지금 보낼 편지 없음.

## 5. 이 세션이 대피 직전에 한 것 (11-06 ~ 11-08)
- li2s-2: DS 회신 고침 → DT 전 독립 리뷰 3 차 → 변이 501/501 (첫 전체 500/501 · DS1 가림 → 시험 고침 e7aac6a1) → DT 편지 → 조건부 GO → 카드 v14 · 결정 활성 (`5a8a019a`) → kgy 발사 · 진행 기록.
- cascade 문헌 갭 (deep-research · 네 갈래 + 보고서).
- litdb 두 편 · open_items 갱신.

## 6. 복귀 체크리스트 (복귀 카드에 옮길 것)
- [ ] friendly 가 이 카드 커밋에서 움직였는가 (`git log origin/claude/friendly-meitner-lldvar`) → 안 움직였으면 ff-only · 움직였으면 대피 브랜치에서 먼저 --no-ff 머지
- [ ] 생성 파일 다시 만들기 (kb_wiki index · reviews --write) · lint 0 errors · validate_canonical ✅ · convention_check 0
- [ ] 원격 마지막 실측 (kgy li2s-2 · 시각) · 이 세션에서 바뀐 원장 목록 (카드 · runlog · decisions · open_items · litdb)
- [ ] CLAUDE.md 를 고쳤으면 그 줄을 복귀 카드에 적는다
