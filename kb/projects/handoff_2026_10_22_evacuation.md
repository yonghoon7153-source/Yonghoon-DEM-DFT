---
title: "대피 인계 — 2026-10-22 (friendly 세션 토큰 소진 → 서브 대시보드 세션 · 머지 때 충돌 0 설계 · W_ad 외주 2차 CZ 고침 설계 포함)"
date: 2026-10-22
updated: 2026-10-22
tags: [handoff, session, evacuation, branch, merge, wad, vasp, outsourcing, checker, runner, li2s, nd, li3nd, elastic]
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

# 대피 인계 — 2026-10-22

> 본 세션 (`claude/friendly-meitner-lldvar` · session …CTzs) 의 토큰이 다 떨어져서, 다음 세션은 **서브 대시보드의 서브 브랜치에서 잠깐** 이어 간다
> (사용자 2026-10-22 *"이거 한다음에 또 토큰 다 써서 서브 대시보드로 가야되니까 예전에 하던것처럼 머지할때 충돌 안나게끔 또 프롬프트 부탁할게용"*).
> 선례: `handoff_2026_10_02_evacuation.md` (대피) → `handoff_2026_10_05_return_to_origin.md` (복귀) · `handoff_2026_10_20_return_to_origin.md` (복귀 · 서브 세션 135 커밋 fast-forward · 충돌 0).
>
> **충돌 0 의 조건은 하나다 — 대피하는 동안 friendly 에 아무도 쓰지 않는다.** 이 카드를 담은 커밋이 friendly 의 마지막 커밋이다.
> 이 세션은 이 커밋 뒤로 friendly 에 쓰지 않는다. 대피 세션도, 원격 (kgy · gabia) 회수 블록도 friendly 로 push 하지 않는다.
> 그러면 복귀는 `git merge --ff-only` 한 줄이다.
> friendly 에 쓰는 다른 세션은 지금 없다 — 10-15 이후 커밋은 이 세션 · 사용자 회수 커밋 (kgy · gabia) · 앞 서브 세션 `session_01Er41drwDRfvL6hhZbVtBiw`
> (마지막 10-20 05:02 `34142a3d` = 10-20 복귀로 이미 들어왔다) 뿐이다.
>
> ⚠ **원격 상태는 10-22 09:15 KST (gabia r2 watch · 사용자 붙여넣기) 가 마지막 실측**이다. kgy (Nd EOS · li2s QE 사슬) 는 10-21 21:00 발사 · 잠금 대기 확인이 마지막이다.
> 그 뒤는 사용자가 붙여 주는 출력으로만 쓴다.
> ⭐ **대피 세션의 주 일거리는 W_ad 외주 2차 CZ 고침**이다 (Codex CZ = NO-GO · 묶음 발송 보류 · 설계는 그대로 · 반송 검사 경로만 고친다).
> 이 세션이 코드 (`tools/wad/build_round2_vasp_package.py` 1,927 줄 전체 · V5 `adopt_a4` · `check_rigid_shift`) 를 다 읽고 고칠 설계를 세웠다 — **§2 에 그대로 적었다.
> 코드는 아직 한 줄도 안 고쳤다.** 다시 논증하지 말고 §2 를 출발점으로 쓴다 (틀린 곳을 찾으면 고치되, 왜 바꿨는지 적는다).

## 0. 새 세션(서브 대시보드)에 붙여 넣을 프롬프트

```text
[대피 세션 시작 — 2026-10-22 · 서브 대시보드]

너는 Yonghoon-DEM-DFT 캠페인의 임시 대피 세션이다. 본 세션(브랜치 claude/friendly-meitner-lldvar)이 토큰을 다 써서
이 서브 브랜치로 잠깐 옮겨 왔다. friendly 세션이 하던 일을 그대로 이어 간다. 나중에 사용자가 "돌아가자" 하면
이 브랜치를 friendly 로 **충돌 없이** 되돌린다 — 그 조건이 아래 ■1·■5 다.

■ 1. 브랜치 (제일 먼저 · 이것부터 틀리면 다 틀린다)
- 이 세션 브랜치 = 너의 시스템 지시에 적힌 개발 브랜치 (아래 <이 세션 브랜치>).
- git fetch origin claude/friendly-meitner-lldvar
- git log --oneline -4 origin/claude/friendly-meitner-lldvar → 맨 위가 "Evacuation handoff card 2026-10-22" 커밋이어야 한다
  (그 아래 c443d793 "Save the Codex CZ reply verbatim" · 422c8c9b "Li3Nd r2: record the 10-22 trajectory read").
  그 위에 커밋이 더 있으면 (사용자 회수 커밋일 수 있다) 멈추고 무엇인지 사용자에게 묻는다. 인계 카드 커밋이 아예 없으면 멈추고 말한다.
- 이 세션 브랜치가 friendly 끝을 포함하지 않고 (git merge-base --is-ancestor origin/claude/friendly-meitner-lldvar HEAD 실패)
  아직 내가 만든 커밋도 없으면, friendly 끝에서 다시 시작한다:
    git checkout -B <이 세션 브랜치> origin/claude/friendly-meitner-lldvar
  (첫 push 가 non-fast-forward 로 거절되면 그 원격 브랜치에 내 커밋이 없는지 확인한 뒤에만 --force-with-lease.)
  이미 내 커밋이 있으면 멈추고 사용자에게 묻는다.
- 브랜치를 옮겼으면 CLAUDE.md 를 다시 읽는다 (처음 로드된 게 옛 판일 수 있다).
- ⛔ friendly 에는 push 하지 않는다. CLAUDE.md 의 "friendly 에만 커밋/푸시" 는 이 세션에서 "friendly 에는 쓰지 않는다 · 커밋·푸시는
  <이 세션 브랜치> 에만" 으로 읽는다 (사용자 2026-10-22 대피 지시). friendly 반영은 ■6 대로만.
- ⛔ 원격(kgy·gabia)에서 git push 하는 회수 블록도 <이 세션 브랜치> 로 보낸다 (friendly 로 보내면 복귀가 fast-forward 가 안 된다).
  첫 사례는 kgy 에서 Nd EOS 뒤에 도는 li2s QE 사슬의 회수 블록이다 (인계 카드 §3).
- PR 만들지 않는다 · force-push 는 --force-with-lease 만 · 커밋 메시지에 모델 ID 를 넣지 않는다.

■ 2. 먼저 읽을 것 (통째로 말고 grep · 부분 읽기 — 단 아래 두 개는 통째로)
- kb/projects/handoff_2026_10_22_evacuation.md  ← 이 인계 카드. §2 (CZ 고침 설계) 는 통째로 읽는다.
- kb/reviews/codex_CZ_reply_wad_outsourcing_round2_bundle_2026_10_17.md  ← CZ 회신 원문 (NO-GO · 해제조건 일곱) · 통째로
- kb/open_items.md 의 ⏭ 절 맨 위 (grep -n "⏭-NOW-z21\|⏭-NOW-z20" kb/open_items.md)
- W_ad: db/properties/wad_round2_build_log_2026_10_17.json (키 ⑤_묶음_빌드_2026_10_22 까지) · 카드 db/properties/wad_p2small_vasp_card_2026_10_15.json
- 값·판정은 원장이 이긴다: db/governance/decisions.json · db/properties/canonical_registry.json · db/properties/citation_hazards.json

■ 3. 시작 점검 (종료코드로 판정 · set -o pipefail · 대피 직전 friendly 실측 기대값을 옆에 적었다)
  set -o pipefail
  python3 -c "import dftd3; print(dftd3.__version__)"        # 1.6.0 — 없으면 pip install dftd3==1.6.0 (W_ad selftest 가 쓴다 · Codex 는 이게 없어서 못 돌렸다)
  python3 tools/kb_wiki.py lint | tail -1                    # 0 errors
  python3 tools/db/validate_canonical.py | tail -2           # 거버넌스 결정 143 · 판정 8 · 그래프 무결성 ✅ · 배선 전부 일치
  python3 tools/convention_check.py | tail -1                # 0 위반
  python3 -I tools/wad/build_round2_vasp_package.py --selftest | tail -1   # 53/53 (몇 분 걸린다)
  python3 -I tools/wad/build_v5_vasp_package.py --selftest | tail -1       # 228/228
  python3 -I tools/wad/se_sym_slab.py --selftest | tail -1                 # 122/122
  python3 -I tools/wad/build_aprime_interfaces.py --selftest | tail -1     # 75/75
  python3 -I tools/wad/build_aprime_s3.py --selftest | tail -1             # 41/41
  python3 -I tools/ionic/glass_model_check.py --selftest | tail -1         # PASS (68/68)
  bash db/inputs/lpscl_glass_model_check_2026_10_19/run_qe_sp_kgy.sh --selftest | tail -1   # 9 통과 · 0 실패
  웹 시험은 8 분 걸린다 — 웹앱 파일을 고칠 때만: python3 -m pytest webapp/tests -q -p no:cacheprovider | tail -2
     # 기대 2 failed (기존 둘: test_kb_index_lists_only_ledger_referenced_docs · test_recent_digests_are_on_every_litdb_surface) · 635 passed · 2 skipped
  빨간 게 있으면 새 문제다 — 고치기 전에 사용자에게 말한다.

■ 4. 지금 상태 (원격은 10-22 09:15 KST 가 마지막 실측 — 그 뒤는 사용자가 붙여 주는 출력으로만)
- ⭐ W_ad 외주 2차 (트랙 W_ad · 1저자 = 사용자 · 결정 D-2026-10-15-wad-p2small-vasp-card · D-2026-10-15-wad-aprime-v5-e70-a4-rerun active):
  ① 빌더 ② 부모 이완 (kgy 10-21 · 회수 6d3538d9) · 봉인 (d640e8e7 · G1p ③ 마스크 기준 고침 — CZ 가 GO) ④ UMA 단일점 (kgy 10-22 · 회수 eb48146b)
  ⑤ 묶음 db/inputs/wad_round2_vasp_2026_10_22/ (24 잡 · MANIFEST 31e47474… · 8d41e4e0) → Codex CZ = **NO-GO** (c443d793 · 발송 보류).
  CZ 는 설계 · 구조 봉인 · 집계 산식은 맞다고 했다. 고칠 것은 반송 검사 경로 (러너 judge · 검사기 · 봉인 등록부 · README).
  ⏭ 인계 카드 §2 순서대로 고친다 (해제조건 하나 = 커밋 하나) → 시험 · 깨기 → 묶음 v2 를 **새 폴더**로 다시 빌드 (옛 폴더는 손대지 않는다 — 리뷰받은 기록)
  → 빌드 기록 · open_items. 업체 발송은 사용자 몫이고, 고친 묶음을 Codex 에 한 번 더 보일지 (편지 DB) 도 사용자가 정한다 (§4).
  ⛔ 점착 W 값은 kb 문서 · 화면 · 편지에 싣지 않는다 (문턱 · 비율 · 벽시계만). ④ UMA 에너지는 반송 뒤 집계 때 한 번만 연다.
- li2s 모델 검증 QE 13 잡 (⛔ 트랙 li2s · 외부 1저자 · 카드 개정 9_개정_2026_10_21_단일점_축소 · 결정 D-2026-10-19-lpscl-smallcell-glass-model-check proposed):
  kgy tmux li2s_qe_sp 가 Nd EOS 잠금 (/tmp/ndsite_eos.lock) 이 풀리면 바로 시작한다 (10-21 21:00 발사 · worktree ~/wt_mcsp_1021 ·
  RUN ~/work/runs/li2s_model_check_sp_2026_10_21 · ≈ 3 GPU-h). ⏭ 사용자가 chain.log 의 '■ 끝 — sp:rc… pulay:rc… kpt:rc…' 를 붙이면
  회수 블록 (인계 카드 §3 · <이 세션 브랜치> 로 push) → glass_model_check.py --sp 판독 → 편지 DA 의 Q-DA-4 절 → 발송은 사용자 (외부 1저자에게).
- Nd 자리 EOS (트랙 CEI · 1저자 = 실험 쪽 · 결정은 '사용자'): kgy · 10-21 17:54 수렴 8/12 · MP_07 점마다 ≈ 10 h → 끝 ≈ 10-23 오전 (어림)
  → make_eos_inputs.py --fit → V₀ 에서 이온만 relax (vc-relax 아님 · CLAUDE.md) → ΔG. 에너지는 판독 도구로만.
- Li₃Nd r2 (트랙 SEI · 1저자 = 사용자): gabia · 10-22 09:14 BFGS 223 · 계속 내려가는 중 (거부 0 · 리셋 0 · 힘 성분 최대가 문턱의 1.4–3.3 배) ·
  이번 실행 한도 ≈ BFGS 386 (≈ 10-30) · 권고 = 그대로 두고 한도에서 안 끝나면 더 늘리지 않는다 (재시작 드라이버 원칙) ·
  기록 db/properties/li3nd_p333_control_runlog_2026_10_11.json 의 단계.r2_관측_2026_10_22_0915. 탄성 modelc_2x 는 r2 뒤 재개로 잡혀 있다.
- 그 밖 (사용자 대기): Nd S 빈자리 마감 비준 (D-2026-10-20-nd-s-vacancy-closed proposed) · Nd 설명 페이지 송부 · B₂O₃ Methods 1저자 회신 ·
  cascade v7 (10-20 재개 블록 전달 뒤 출력 없음 · 상한 재비준 🔔) · DEM 편지 (🔔 · 2차 반송 뒤) · BVSE R₀ 민감도 · Li₂S NEB 카드 · Feng/Wang ③ (🔔).

■ 5. 충돌 안 나게 — 대피 중에 지킬 것 (복귀가 fast-forward 면 아래는 보험이다)
- friendly 에 쓰지 않는다 (■1). 이게 지켜지면 복귀는 충돌 0 이다.
- 그래도 보험으로, 같이 쓰는 파일은 **덧붙이기**로만 고친다:
  · kb/open_items.md — 새 블록은 ⏭ 절 맨 위에 "### ⏭-NOW-z22. … (대피)" 로 얹는다. 남의 줄은 지우거나 다시 쓰지 말고, 끝에 " · ⏩ 10-2x …" 를 붙인다.
    머리 줄(최종 갱신)은 바꿔도 되지만 굵게를 겹쳐 쓰지 않는다.
  · db/governance/decisions.json — 새 결정은 끝에 추가 · 비준된 결정 본문은 한 글자도 고치지 않는다 (digest 가 깨진다) ·
    proposed → active 는 그 결정만. 저장은 json.dumps(…, ensure_ascii=False, indent=1) + "\n".
  · JSON 원장·런로그는 **원래 들여쓰기 그대로** 다시 쓴다 — 쓰기 전에 json.dumps(d, ensure_ascii=False, indent=N) + "\n" == 원문 인지
    N = 1 · 2 로 확인한다 (10-22 에 이걸 안 보고 indent 1 로 썼다가 li3nd 런로그 전체가 다시 써졌다 — 되돌렸다). 맞는 N 이 없으면 텍스트 삽입으로.
  · kb/index.md · kb/reviews/INDEX.md — 손으로 고치지 않는다. python3 tools/kb_wiki.py index · reviews --write 로만.
  · CLAUDE.md — 꼭 필요할 때만, 그 절 끝에 덧붙인다 (재배치·정리 금지).
- 리뷰 회신 원문 · 봉인 카드 · 비준된 결정 · 리뷰받은 묶음 폴더 (db/inputs/wad_round2_vasp_2026_10_22/) 는 고치지 않는다 — 새 파일 · 새 폴더로.

■ 6. friendly 로 돌아가기 (사용자가 "돌아가자" 할 때만)
- 이 브랜치를 push 하고 두 문서를 쓴다 (10-20 선례 그대로):
  kb/projects/merge_request_<날짜>.md — 커밋 표 (git log --oneline origin/claude/friendly-meitner-lldvar..HEAD) · 돌린 시험·종료코드 ·
    원장 변화 (새 결정·비준) · 원격에서 아직 도는 것 · 빨간불.
  kb/projects/handoff_<날짜>_return_to_origin.md — friendly 세션에 붙일 §0 프롬프트: ① 아무것도 쓰기 전에 git status · FF 확인
    ② 경우 A (FF 가능 · 기본): git merge --ff-only origin/<이 세션 브랜치> → push (강제 없이)
    ③ 경우 C (friendly 가 움직였음): 멈추고 묻기 → 허락 뒤 git merge --no-ff · ⛔ rebase 금지 (커밋 해시가 결정 원장 · 기록 · 원격 worktree 에 박힌다)
    ④ 파일별 충돌 규칙 (decisions 는 id 합집합 · open_items 합집합 · kb/index.md 재생성) ⑤ 머지 뒤 점검 기대값.
- 대피 브랜치는 지우지 않는다 (기록이다).
- ⚠ 원격 worktree 가 이 브랜치를 체크아웃하고 있으면 복귀 뒤에도 그대로 둔다 (돌던 러너가 읽는 중일 수 있다) — 다음 블록부터 friendly 로.
- 세션을 닫기 전에 kb/open_items.md 의 ⏭ 절을 갱신한다.

■ 7. 사용자 운영 규칙 (어기면 바로 잡힌다)
- 원격 작업은 "붙여넣기 블록 → 사용자가 실행 → 출력 회수". 붙여 준 출력은 하나씩 보고 해석한다 — 앞서가지 않는다.
- ⛔ 인증을 묻는 명령(git push) 뒤에는 다른 줄을 두지 않는다 — 뒤에 할 일은 같은 줄에 && 로.
- 감시 블록은 watch -n 30 '…' 꼴로 준다 (--loop · while 금지 · 따옴표 안은 $HOME).
- QE 계산 run 은 GPU 로만 (CPU 는 검사 프로브만 — 그때는 첫 줄에 '검사용 · run 아님 · N 초 뒤 자동 종료' 라고 먼저 말한다).
  gabia 에서 GPU pw.x 와 UMA 를 겹치지 않는다 (예외는 원장 active 결정만 · 지금 살아 있는 공존 예외 0 건).
- 프로세스는 PID 나 잡 고유 인자로만 죽인다 (pkill -f pw.x · python · 스크립트 이름 금지). 돌고 있는 러너의 worktree 를 옮기거나 지우지 않는다.
- 봉인 카드 · 리뷰 회신 원문 · 비준된 결정은 고치지 않는다 (정정은 새 파일 · 덧붙임으로).
- `1저자` 는 트랙마다 다르다 — 결정 항목을 쓸 때 트랙을 먼저 쓴다 (W_ad · cascade · ESW · 탄성 · SEI = 사용자 · li2s = 외부 1저자 ·
  CEI · Nd = 실험 쪽 다른 사람 (결정은 '사용자') · B₂O₃ 원고 = 다른 사람).
- 한국어 대화체로 짧게 · 그림 라벨은 영어 · 새 개념은 한 단계씩. "용훈 포메이션" 은 요청이 있을 때만 그 형식으로.

첫 답은: ■1 브랜치 결과 · ■3 점검 결과를 한 줄씩, 그리고 "W_ad CZ 고침을 인계 카드 §2 순서대로 시작할게요" 한 줄과
인계 카드 §4 의 첫 질문 (LOCPOT 면평균을 파일럿 S_A far 에 더할지) 을 AskUserQuestion 으로.
원격 명령 블록은 사용자가 요청할 때나 붙여 준 출력의 다음 한 수로만 준다.
```

---

## 1. W_ad 외주 2차 — 지금까지의 산출물 (해시)

| 단계 | 산출물 | 커밋 · 해시 |
|---|---|---|
| ① 빌더 | `tools/wad/build_aprime_interfaces.py --build P2S` · 초기 구조 `db/inputs/wad_p2small_geometries_2026_10_17/` | selftest 75/75 |
| ② 이완 (kgy) | `db/raw/wad_p2small_relax_2026_10_17/` (S_A FIRE 894 · Li_A 430 · 둘 다 fmax < 0.02 eV/Å) | 6d3538d9 (사용자) · SHA256SUMS 13 줄 |
| 봉인 | `db/inputs/wad_p2small_seal_2026_10_17/` (구조 9 · 끝점 10 Å · D3 만 예측 80 % 문턱 대비 19 % · 30 %) | d640e8e7 · manifest sha256 65a0ca0e376b3c67… |
| ④ UMA 단일점 (kgy) | `db/raw/wad_p2small_uma_sp_2026_10_17/` (9 구조 · 16 초 · 체크포인트 07068e9c76702ca1) | eb48146b (사용자) · SHA256SUMS 4 줄 · **아직 안 열었다** |
| ⑤ 묶음 v1 | `db/inputs/wad_round2_vasp_2026_10_22/` (24 잡 · 리뷰받은 판 — 고치지 않는다) | 8d41e4e0 · MANIFEST 31e4747450d15408… |
| CZ | 프롬프트 `kb/reviews/codex_CZ_prompt_…` · 회신 `kb/reviews/codex_CZ_reply_…` (NO-GO) | 4ab05482 · c443d793 |

## 2. ⭐ CZ 고침 설계 (해제조건 일곱 → 고칠 곳 · 규칙 · 시험)

> 줄 번호는 이 카드 커밋 기준이다 (`tools/wad/build_round2_vasp_package.py` 는 8d41e4e0 이후 안 바뀌었다).
> 러너는 그 파일 안 `RUN_ALL` 문자열 (300–716 행) 이다 — 묶음의 run_all.sh N 행 ≈ 소스 (299 + N) 행.

### 2.0 공통 규칙 (이번 고침 전체)

- **해제조건 하나 = 커밋 하나** — 메시지 `W_ad round 2 CZ fix (k/7): …`. 다음 세션이 git log 만 봐도 어디까지 됐는지 안다.
- **Codex 재현 사례 하나 = selftest 음성 시험 하나.** 시험을 먼저 쓰고 **고치기 전 판에서 빨간지** 본 뒤 고친다. 고친 뒤에는 그 고침만 되돌린 사본에서
  그 시험이 다시 빨개지는지 본다 (레포 관례 '깨기' · CLAUDE.md §코드 규율 — 2026-09-13 에 엉뚱한 것을 잰 시험 셋이 통과했다).
- 러너 (bash/awk) 와 검사기 (python) 둘 다에 걸린 규칙은 **둘 다** 고치고, 판정 계약은 기존 **탐침 대조** (selftest 1600–1647 행 · 같은 탐침을 awk 와 python 에 넣어 같은 답) 에 탐침을 더한다.
- **바꾸지 않는 것**: 카드 문턱 · 잡 행렬 24 · 사다리 INCAR (LOCPOT 결정이 나면 `P2S_S_A_far` 만 · §2.7) · 집계 산식 (Δ_C · G3 · G4 · G5 순서 · 80 % 규칙 · δ 규칙) · 구조 봉인.
- `resolve_job()` 이 돌려주는 `OK` 는 고친 뒤 **"그 잡의 모든 시도가 무결성 · 환경 · 결박 검사를 통과했고 채택 시도가 수렴했다"** 는 뜻이어야 한다
  (V5 `adopt_a4()` 가 이 OK 를 그대로 믿는다 — Q-CZ-8).

### 2.1 R1 판정 순서 — 확정 모순을 rc 보다 먼저 (Q-CZ-1 · P0)

고칠 곳: 러너 `judge()` (awk · 333–358 행) 와 검사기 `judge_text()` (755–799 행) — **둘 다 같은 순서로**. 주석 (329–332 행 · 756 행 docstring) 도.

새 순서 (지금 ④ 앞에 ④′ 가 들어간다):

| 순서 | 조건 | 판정 · 사유 |
|---|---|---|
| ① | 전자 반복행 0 | SCF_UNVERIFIED `no_rows` (그대로) |
| ② | 스텝 번호 1…N 아님 · 이온 요약 뒤 행 | SCF_UNVERIFIED (그대로) |
| ③ | NELM 모름 · N > NELM | SCF_UNVERIFIED (그대로) |
| ④′ | **실행 머리줄 (`vasp.5…`) ≥ 2** | SCF_UNVERIFIED `run_blocks` — rc 와 무관 |
| ④′ | **OUTCAR 가 끝까지 쓰였다 (`General timing and accounting`)** 인데 머리줄 ≠ 1 또는 마지막 `Iteration n( k)` 의 k ≠ N | SCF_UNVERIFIED `run_blocks` / `outcar_oszicar_mismatch` — rc 와 무관 |
| ④′ | OUTCAR 가 안 끝났다 (잘림 · 충돌) 인데 k 가 있고 **k > N + 1** | SCF_UNVERIFIED `outcar_oszicar_mismatch` |
| ⑤ | rc ≠ 0 또는 OUTCAR 안 끝남 | RUN_FAILED (지금 ④) |
| ⑥ | (여기 오면 rc 0 · 끝남 · 머리줄 1 · k = N 이 보장된다) 비유한 · EDIFF 모름 · 수렴 판정 | 그대로 |

왜 이렇게 가르나 (결측 ↔ 확정 모순 — CZ 가 요구한 구분):
- **OUTCAR 가 끝까지 쓰였으면** 잘림으로 설명할 수 없다 → 어긋남은 확정 모순이다 (CZ 재현 ② 가 이 경우 — 끝 줄이 있는 OUTCAR + k ≠ N + rc 1).
- **OUTCAR 가 안 끝났으면** 버퍼 손실로 뒤가 잘릴 수 있다 → k 없음 · k < N 은 **결측**으로 보고 RUN_FAILED 를 허용한다 (비준 정책 '전자 스텝 ≥ 1 뒤 충돌 = 실행 실패' 유지).
  k = N + 1 은 스텝 N+1 도중의 충돌 (OUTCAR 머리는 스텝 시작에 · OSZICAR 행은 스텝 끝에 쓴다) 이라 정상이다.
- k > N + 1 은 판정 근거 파일 (OSZICAR) 이 OUTCAR 보다 두 스텝 이상 모자란 것 — **판정 근거의 결측은 봐주지 않는다** (같은 실행인지 확인할 수 없다) → 미확인.
- 머리줄 둘 이상은 어떤 경우에도 한 번의 실행이 아니다 (CZ 재현 ①).

시험 (탐침을 `probes` 에 더하고 `want` 표에도):
`rc1_two_runs` (끝남 · 머리줄 2 · rc 1 → UNVERIFIED) · `rc1_it_mismatch_term` (끝남 · k 24 · N 25 · rc 1 → UNVERIFIED) ·
`crash_midstep` (안 끝남 · k = N+1 · rc 1 → RUN_FAILED) · `crash_outcar_short` (안 끝남 · k < N → RUN_FAILED) · `crash_no_iter` (안 끝남 · k 없음 → RUN_FAILED) ·
`crash_no_header` (OUTCAR 빈 파일 · rc 1 → RUN_FAILED) · `crash_outcar_ahead` (안 끝남 · k = N+3 → UNVERIFIED) · `noterm_two_runs` (안 끝남 · 머리줄 2 → UNVERIFIED) ·
`term_no_header` (끝남 · 머리줄 0 → UNVERIFIED) · `rc0_noterm_midstep` (rc 0 · 안 끝남 · k = N+1 → RUN_FAILED).
끝에서 끝 시험 하나: FAKE_VASP 에 행동 `crash_tworuns` (행 7 · rc 1 · OUTCAR 머리줄 둘) → 러너가 단 0 을 SCF_UNVERIFIED 로 보고 **r1 을 안 띄운다** ·
검사기도 단 0 에서 멈춘다 (CZ 의 `0: RUN_FAILED → r1A: OK → r1B: OK → 최종 OK` 가 안 나온다).
기존 탐침 기대값은 하나도 안 바뀐다 (`rc1` · `not_term` · `rc1_nan` = RUN_FAILED 그대로 · `two_runs` · `it_mismatch` = UNVERIFIED 그대로) — 바뀌면 설계를 다시 본다.

### 2.2 R2 ⓐ→ⓑ 결박 · ⓐ 머리 = 실제 OUTCAR · 재시작 문구 (Q-CZ-2 · P0)

고칠 곳 (검사기):
- `check_attempt(job, pkgdir, attdir, rung, registry=None, a_ref=None)` — ⓑ 단 (r1B · r2B · a4B) 은 `a_ref` (그 ⓑ 가 읽은 ⓐ 의 검사 기록) 를 **꼭** 받는다.
  재시작 확인 (986–1000 행) 에 더한다: `a_ref["wavecar"]["sha256"]` (ⓐ attempt.json 이 sha 로 묶은 ⓐ WAVECAR.info 의 끝 sha) **==** ⓑ 기록의
  `src_sha256 == copied_sha256 == end_sha256`. 다르거나 `a_ref` 가 없으면 RESTART_NOT_HONOURED (사유 "ⓑ 원본이 이 ⓐ 의 WAVECAR 가 아니다").
  `resolve_job` 이 넘긴다: a4B ← a4A · r1B ← r1A · **r2B ← r1A** (r2 는 r1 의 ⓐ WAVECAR 를 쓴다).
- `a_eligible(ra)` (1020 행) — 지금은 WAVECAR.info 안의 `head` 와 같은 파일 안의 `outcar` 사본을 비교한다 (자기 대조). 바꾼다:
  `check_attempt` 가 ⓐ 단에서 **반송된 ⓐ OUTCAR 원문에서** NKPTS · NBANDS · ENCUT 를 다시 읽어 `r["outcar_dims"]` 에 둔다
  (러너 `out_num()` 과 같은 패턴 · 마지막 값: `NKPTS *= *(\d+)` · `NBANDS *= *(\d+)` · `ENCUT *= *([0-9.]+) eV`) →
  `a_eligible` 은 head[3:6] 를 `outcar_dims` 와 대조하고, WAVECAR.info 의 `outcar` 사본도 `outcar_dims` 와 같아야 한다 (다르면 "WAVECAR.info 의 OUTCAR 사본이 실물과 다르다").
  5.4.4 실물 꼴 (V5 반송 · 같은 빌드): `k-points NKPTS =      4 … number of bands    NBANDS=    872` · `ENCUT  =  520.0 eV  38.22 Ry …`.
- 재시작 긍정 문구: 등록부에 `restart_read_regex` 가 있으면 ⓑ 단은 `re.search(regex, OUTCAR + stdout.log)` 가 맞아야 한다 — 없으면 RESTART_NOT_HONOURED
  (러너의 `honoured: 1` · `positive_regex_match` 를 믿지 않고 원문을 다시 본다). 등록부가 없으면 (파일럿 단계) 지금처럼 요구하지 않는다.
  `seal_registry` 는 받은 regex 를 ① 파이썬에서 컴파일 ② ERE 와 뜻이 같은 글자만 (`^[A-Za-z0-9 _:.,=()|*+?\[\]^$\\/-]+$`) ③ 파일럿 ⓑ 시도 (최소 a4B) 원문에 실제로 맞는지 확인하고, 아니면 봉인하지 않는다.
  ⚠ CZ: 긍정 문구가 **없는 것 자체**는 blocker 가 아니다 (Startparameter ISTART 1 · ICHARG 0 이 간접 증거) — regex 는 파일럿 원문에 문구가 있을 때만 넣는다.

고칠 곳 (러너 · 같은 규칙):
- `stat_of()` (644 행) 의 ⓑ 갈래: `honoured` 에 더해 ⓑ WAVECAR.info 의 `src_sha256` == ⓐ WAVECAR.info 의 `sha256` (ⓐ 폴더 = r1B·a4B 는 `$d/stageA` · r2B 는 `${d%_r2}_r1/stageA`).
  러너는 이미 ⓑ 띄우기 직전에 `elig_A` 로 ⓐ sha 를 확인하지만, 이어 돌리기 · 손댄 기록에서 검사기와 같은 답을 내야 한다.

시험 (CZ 재현 셋 + 양성):
① ⓐ 해시는 그대로 · ⓑ 의 src/copied/end 셋을 다른 같은 값으로 (ⓑ attempt.json 의 WAVECAR.info sha 도 맞춰서) → RESTART_NOT_HONOURED (지금은 OK) ·
② 등록부 `restart_read_regex` = 원문에 없는 문구 → RESTART_NOT_HONOURED (지금은 OK) ·
③ ⓐ WAVECAR.info 의 head NBANDS 와 `outcar` 사본 NBANDS 를 둘 다 999 로 (ⓐ attempt.json sha 맞춰서 · 실물 OUTCAR 512) → STAGE_A_INELIGIBLE (지금은 OK) ·
양성: FAKE_VASP 가 ISTART 1 로 읽었을 때 stdout 에 긍정 문구 한 줄 (예 ` reading WAVECAR`) 을 찍게 하고, 그 문구 regex 로 봉인한 등록부 → OK · 러너 `stat_of` 도 ① 에서 RESTART_NOT_HONOURED.

### 2.3 R3 모든 시도의 환경 감사 · 질문별 실패 · 파일럿 결박 · 재개 PP · 상한 (Q-CZ-3 · P0 + P1 셋)

핵심 (P0): **최종 채택 결과만 보지 말고 모든 시도를 감사한다** (V5 `check()` 의 `every` 가 선례 — build_v5_vasp_package.py 1041–1074 행).
- `resolve_job()` (1038 행) — 지금은 최종 dict 만 돌려준다. 시도 기록을 전부 `attempts = {rung: check_attempt 결과}` 로 담아 돌려준다.
- 환경 등급 = `ENV_CLASS = ("VERSION_MISMATCH", "POTCAR_MISMATCH", "KERNEL_MISMATCH", "KERNEL_NOT_READ")` (§2.4 에서 KERNEL_NOT_READ 추가).
  시도의 `status` 뿐 아니라 `conflicts` 목록 (check_attempt 975 행 — 첫 모순만 status 가 된다) 도 훑는다.
- `resolve_job` 안: 그 잡의 **어느 시도든** 환경 등급 모순이 있거나, 그 잡 시도들 사이에 VASP 버전 · PP 종별 sha · (optB88) 커널 sha 가 갈리면
  → 최종 상태를 그 환경 상태로 덮는다 (`adopted_status` · `env_in` 에 원래 값 · 어느 단인지 남김). ⇒ `OK` 는 환경이 깨끗한 잡에만.
  (CZ 재현: a4A 만 다른 VASP 빌드 → 지금은 STAGE_A_INELIGIBLE 안에 VERSION_MISMATCH 가 묻힌다.)
- `collect()` (1092 행): 모든 잡의 모든 시도를 모아 전역 감사 → 어느 하나라도 환경 등급 · 시도 사이 갈림 (POTCAR/VERSION/KERNEL_INCONSISTENT) 이면
  `common_environment_failure` = 목록 (잡 · 단 · 사유) · `G5_C.status` = `BLOCKED (공통 환경 고장 …)` · 종료 6 (`collect_exit` 는 이미 이것부터 본다).
  지금 1100–1111 행은 **최종 결과만** 모은다 — 그것을 모든 시도로 바꾼다.
- 질문별 실패 (`failure_propagation` · 1253 행) 는 그대로 최종 상태 기준 — 물리적 수렴 실패 · 실행 실패는 그 질문에만.
- `--a4_result` (1895 행): `resolve_job` 의 OK 가 위 뜻이 되므로 그대로 쓴다. 더해서 V5 `check()` (1056–1059 행) 가 `a4_result["result"]["attempts"]` 의 시도들도
  `every` 에 넣게 한 줄 고친다 (a4A 의 PP·버전도 V5 잡들과 같아야 한다 · 개정 4 '같은 빌드·같은 PP'). V5 저장본 바이트 일치 시험은 a4_result 없이 만든 것이라 안 깨진다 — 돌려서 확인.
- `seal_registry()` (1276 행) — 고친다:
  · 파일럿 잡마다 **모든 시도**의 PP 종별 sha · VASP 버전 · 커널 sha 를 모은다 (지금은 최종만 → a4A 만 다른 빌드여도 봉인된다).
  · 봉인 거부 = 무결성 실패 (ATTEMPT_MISMATCH · INPUT_MODIFIED · POTCAR_UNVERIFIED · INCOMPLETE_ATTEMPT · MISSING) 또는 환경 등급 · 갈림 · KERNEL_NOT_READ.
    **물리 실패 (RUN_FAILED · SCF_NOT_CONVERGED · SCF_UNVERIFIED · STAGE_A_INELIGIBLE · RESTART_NOT_HONOURED) 는 봉인을 막지 않는다** —
    지금 1293 행의 `or not r.get("run_id")` 때문에 a4A 가 정상 환경에서 전자행을 남기고 충돌하면 (최종 = STAGE_A_INELIGIBLE · run_id 없음) 탄소 해제가 막힌다 (CZ 반대 방향 오류).
  · 파일럿 잡마다 완결된 시도 (attempt.json 있는 것) 가 하나 이상이어야 한다.
  · `from_pilot` = {잡: {단: run_id}} · `from_pilot_sha256` = {잡: {단: {"attempt.json": sha, "OUTCAR": sha}}} — **모든 시도**. 등록부 schema 를 `wad_round2_pp_registry/v2` 로 올린다
    (아직 봉인한 등록부가 없다 · CLI 1888 행 대조도 v2).
- (P1) **파일럿 결박 소비**: 등록부가 있으면 `resolve_job` 이 파일럿 잡의 반송 시도 집합 · 단마다 run_id · attempt.json sha · OUTCAR sha 를 `from_pilot*` 과 대조
  (반송에 있는데 등록부에 없는 단 · 등록부에 있는데 반송에 없는 단 · 값 다름 = 전부) → 다르면 `PILOT_BINDING_MISMATCH` (무결성 · 그 잡 OK 아님).
  CZ 재현: 봉인 뒤 파일럿의 run_id · OUTCAR · attempt 해시를 바꿔도 지금 CLI `--check` 가 OK.
- (P1) **재개한 ⓑ 의 PP 사전검사**: 러너 `run_one()` (589 행) 맨 앞 (폴더를 만들기 전) 에 `pp_ok "$job" || return 6` — 모든 VASP 실행 직전.
  지금은 `ladder` 가 새 단 폴더를 만들 때만 부른다 → ⓐ 끝 · ⓑ 전에 끊겼다가 이어 돌리면 (`two_stage` 663–667 행) 새 POTCAR 로 ⓑ 가 뜬다.
  시험: 해제 뒤 탄소 잡 하나를 `r1B = ignore_wavecar` 로 돌려 ⓐ WAVECAR 를 남긴 다음 (drop_wav 가 재시작 미이행이면 남긴다), ⓑ 파일 (`.b` · attempt.json · OUTCAR …) 만
  지워 "ⓐ 끝 · ⓑ 전" 상태를 만들고, C POTCAR 를 바꾼 POTCAR_DIR 로 다시 → 종료 6 · `.b` 안 생김.
- (P1) **상한 값 검사**: `release_text()` (1316 행) 가 `caps_h[s]` · `total_cap_h` 를 `math.isfinite(x) and x > 0` 로 거른다 (nan · inf · 음수 · 0 → PkgError).
  러너가 해제 파일을 읽을 때 (494–504 행) 도 `cap_h` · `total_cap_h` 값이 `^[0-9]+(\.[0-9]+)?$` 이고 0 보다 큰지 — 아니면 종료 2. 시험 둘 (파이썬 nan · inf · −1 거부 · 러너 'nan' 해제 파일 종료 2).

### 2.4 R4 optB88 — 실제 교환함수 · 커널 읽기/재생성 구분 (Q-CZ-5 · P0)

고칠 곳: `audit_r2()` (829 행 · optB88 갈래 856–867 행) · `KERNEL_READ_RE` (822 행) · `check_attempt` 완결성 (1005–1006 행) · `seal_registry` · `release_text`.
- **GGA 증거**: OUTCAR 본문 (INCAR 되울림 뺀 `_body`) 의 `(?m)^\s*GGA\s*=\s*(\S+)\s+GGA type` — 5.4.4 실물 꼴은 `   GGA     =    PE    GGA type` (V5 반송 OUTCAR 822 행 · 같은 빌드).
  기대값 optb88 = `BO` · pbed3 · v5 = `PE`. 읽었는데 다르면 SETTINGS_MISMATCH (명백히 다름) · 못 읽으면 `missing` → OK 시도는 SETTINGS_UNVERIFIED (형식 못 읽음 = 미검증).
  ⚠ pbed3 · v5 에도 GGA 결측 = 미검증을 걸면 V5 실물 반송 재검사 바이트 일치가 깨지는지 본다 — V5 는 `audit_r2` 를 안 쓰므로 안 깨질 것이다 (확인).
- **커널 상태 (준비 · 읽기 · 부재 · 재생성)**: 커널을 말하는 줄 (`(?i)kernel|vdw_kernel`) 을 OUTCAR + stdout.log 에서 모아
  · 부정 · 재생성 표지가 같은 줄에 있으면 (`(?i)\b(not|no|error|cannot|unable|fail\w*|missing|differ\w*|recalc\w*|regenerat\w*|generat\w*|comput\w*|writ\w*)\b`) →
    `kernel_state = "not_read" / "regenerated"` → 모순 ("KERNEL_NOT_READ", …) — 환경 등급 (§2.3 · 전역 정지 · 봉인 거부).
  · 등록부에 `kernel_read_regex` (파일럿 원문으로 확정한 긍정 문구) 가 있으면 OK 시도는 그 문구가 맞아야 한다 — 없으면 KERNEL_UNVERIFIED.
  · 등록부가 없으면 (파일럿 단계) optB88 OK 시도는 **KERNEL_UNVERIFIED** — 5.4.4 원문으로 형식을 확정하기 전에는 읽기 확인을 완료했다고 하지 않는다 (CZ).
    ⇒ 기존 selftest 의 "C–C optB88 bound OK (파일럿 · 등록부 없음)" 기대값을 KERNEL_UNVERIFIED 로 바꾼다 (의도된 강화).
  · 준비 (러너가 복사한 파일 sha · attempt.json `kernel_sha256`) 는 지금처럼 등록부 sha 와 대조 (KERNEL_MISMATCH).
- `seal_registry(…, kernel_read_regex="")` + CLI `--kernel_read_regex` — 파일럿 optB88 두 잡 (C–C bound · far) 의 원문에 맞고, 같은 원문에 부정 · 재생성 표지가 없어야 봉인한다.
  restart regex 와 같은 글자 제한. `release_text` 에도 한 줄 (`kernel_read_regex`) — 러너는 기록만 해도 된다 (판정은 검사기).
- 시험 (CZ 재현 넷 + 양성): 해석값 `GGA = BO` → `PE` (SETTINGS_MISMATCH) · 해석 GGA 줄 지움 (SETTINGS_UNVERIFIED) ·
  커널 줄 `ERROR: vdw_kernel.bindat not read` (KERNEL_NOT_READ · 집계 종료 6 · 봉인 거부) · `kernel differs, recalculating vdW kernel` (같은) ·
  양성 = FAKE_VASP 의 ` vdW kernel read from vdw_kernel.bindat` + 그 문구로 봉인한 등록부 → OK.
  ⚠ 부정 표지가 넓다 — 5.4.4 실물 긍정 문구에 'calculating' 같은 말이 들어 있으면 거짓 경보가 된다. 파일럿 원문을 보고 표지를 다시 정한다 (검사기만 바뀌고 묶음은 안 바뀐다).

### 2.5 R5 0 스텝 인프라 중단 — 결측 ≠ 0 행 · 미상 비용 ≠ 0 초 (Q-CZ-4 · P1) + README ②

고칠 곳: 러너 `--infra-abort` (447–477 행) · `wall_s_of()` (546–562 행) · `cap_ok()` (563–569 행) · README 5 번 · English summary.
- OSZICAR 가 있고 읽히면 0 행 확인 (`oszicar: "zero_rows"`) · 없으면 `"missing"` · 있는데 못 읽으면 **거부** (읽기 실패).
- 0 행이어도 **다른 출력에 전자 반복 증거**가 있으면 거부 — stdout.log 의 `^\s*(DAV|RMM|CG|SDA):` · OUTCAR 의 `Iteration +[0-9]+\(`.
- `WALL_S` 를 안 주고 그 시도에 attempt.json 도 없으면 `wall_s: "UNKNOWN"` 으로 기록한다 (지금은 `NA` 가 합산에서 0 초가 된다).
- `wall_s_of` 는 미상이 하나라도 있으면 그 단계 (와 전체) 를 '미상' 으로 돌려주고, `cap_ok` 는 미상이면 **다음 잡을 띄우지 않는다** (종료 5 · 메시지 "비용 미상 —
  `bash run_all.sh --infra-wall <run_aborted 폴더 이름> <초>` 로 스케줄러 장부 값을 채운 뒤 다시"). `--infra-wall` 을 새로 만든다 (infra_abort.json · tsv 를 같이 고친다 · 이미 숫자면 거부).
- 알려진 시간 중복 합산 금지는 지금 규칙 그대로 (attempt.json 이 있으면 infra_abort.json 의 wall_s 를 안 더한다 · 552 행).
- README 5 번: "시간을 알면 WALL_S" 와 "그 시간도 상한에 들어갑니다" 를 같이 두지 않는다 → "`WALL_S=<초>` (스케줄러 장부의 그 시도 벽시계) 를 꼭 주세요 —
  모르면 UNKNOWN 으로 남고 그 뒤 잡은 장부를 채울 때까지 뜨지 않습니다 (`--infra-wall`)".
- 시험: OSZICAR 없음 + stdout DAV 행 → 거부 · OSZICAR 0 행 + OUTCAR Iteration → 거부 · 깨끗한 0 스텝 (WALL_S 없음) → UNKNOWN 기록 → 다음 잡 안 뜸 (종료 5) →
  `--infra-wall` 로 채움 → 다시 돌면 뜬다 · 알려진 값 + attempt.json 있음 → 한 번만 더한다.

### 2.6 R6 나머지 — 열거 오류 · δ 의존성 · far 진단 출처 · 신호 미평가 · NaN · 영어 요약 (Q-CZ-6 · Q-CZ-9 P2 · Q-CZ-10 ①③)

- **반송 열거** (러너 `pack()` 392–394 행 · Q-CZ-10 ①): 지금 `[ -d run_aborted ] || g=0` 이 `run/` 열거 실패까지 덮는다 →
  있는 폴더만 인자로 (`dirs=run; [ -d run_aborted ] && dirs="run run_aborted"`) · find 실패면 종료 4. 시험: `run/` 하위를 읽기 금지로 만든 사본 → 포장 실패 · 종료 4.
- **δ 실패 의존성** (`failure_propagation` 1253–1255 행 · Q-CZ-6): `delta_XC_vdW` 에 optB88 쌍 + **대응 PBE+D3 쌍** (`SAMPLES["S_A"]` · `SAMPLES["Li_A"]`) 을 넣는다.
  시험: S_A PBE bound 미수렴 → `delta_XC_vdW` 목록에 그 잡 (지금은 빈 목록).
- **far 진단 출처** (1233–1241 행): 채택 시도가 없으면 단 0 을 읽는다 — 진단은 남기되 `source_rung` · `source_status` · `adopted: false` 를 붙인다 (채택 자료처럼 안 읽히게).
- **신호 미평가** (1242–1251 행): p_z 가 없거나 (쌍극자 자료 결측 · 잡 미완) dW_ii · dD3_ii 가 없으면 그 신호는 `not_evaluated` (사유) — "검사했고 신호 없음" 과 구분 ·
  G5 라벨에 "전하이동 신호 ⓐ/ⓑ 미평가 (자료 결측)". 카드 규칙 "신호 없음 ≠ 중성 입증" · "신호가 있으면 라벨 제한 · 1저자 판단" 은 그대로 (CZ Q-CZ-7).
- **check_rigid_shift NaN** (build_aprime_interfaces.py 483 행 · Q-CZ-9 P2): 좌표 · 셀에 `np.isfinite` 검사 → 비유한이면 위반. 저장 파일 왕복 음성시험 (NaN 좌표를 쓴 extxyz).
  현재 봉인본은 전부 유한 (CZ 확인) — 봉인을 다시 할 필요 없다.
- **영어 요약** (`_readme` 1376 행 · Q-CZ-10 ③): `24 single-point SCF runs` → **"24 jobs; at least 25 VASP executions, up to 94 under the registered ladder, excluding separately recorded infrastructure retries."**
  (탄소 23 × 최대 4 + a4 2 = 94 · 최소 23 + 2 = 25). 한국어 '24 잡' 은 맞다. README 상태 줄은 "준비본 v2 — CZ 고침 반영 · 발송 전".

### 2.7 R7 다시 빌드 · 봉인 · 기록

1. (LOCPOT 결정이 '더한다' 면 먼저) `P2S_S_A_far` 의 사다리 INCAR 넷에 `LVHAR = .TRUE.` · 반송 허용 목록에 면평균 텍스트 하나 (예 `LOCPOT.zavg.txt`) ·
   러너가 채택 여부와 무관하게 시도마다 awk 로 만든다 (z 좌표 Å · 값 eV · 격자 NGX NGY NGZ · 원본 LOCPOT sha256 · run_id 를 머리에) · LOCPOT 원본은 반송 금지 목록.
   추출기는 전체 격자 개수 (NGX·NGY·NGZ) 와 유한수를 검사하고 어긋나면 파일을 만들지 않는다 · 음성시험 = 잘린 LOCPOT · 격자 줄 오독 (CZ Q-CZ-7).
   집계는 **채택한 최종 시도**의 면평균만 쓴다 · 정보 (판정 아님) · 조각별 순전하로 읽지 않는다. 카드 · 개정 4 · 결정은 바꾸지 않고 빌드 기록에 'CZ 권고 반영 · 사용자 결정' 으로.
2. selftest 전부 (53 + 새 시험) · 깨기 (새 시험마다 그 고침만 되돌린 사본에서 빨강) · V5 228 · interfaces · s3 · se_sym_slab · validate_canonical · kb lint.
3. `python3 -I tools/wad/build_round2_vasp_package.py --build --seal db/inputs/wad_p2small_seal_2026_10_17 --out db/inputs/wad_round2_vasp_v2_<날짜>` →
   다시 빌드 바이트 동일 · 묶음 안 `sha256sum -c MANIFEST.sha256` · 새 MANIFEST sha.
4. 빌드 기록 `db/properties/wad_round2_build_log_2026_10_17.json` 에 새 키 (`⑤-2_CZ_고침_<날짜>` · 커밋 일곱 · 시험 수 · 깨기 · 새 묶음 · MANIFEST · 옛 묶음 = 'CZ NO-GO · 발송 안 함') —
   이 파일은 indent 1 이다 (쓰기 전에 왕복 확인). open_items ⏭ 에 한 줄.
5. 사용자에게: 고친 내용 일곱 줄 요약 + (사용자가 정하면) 편지 DB (Codex · 고친 묶음 · diff 만 · 질문은 해제조건 일곱이 닫혔는지) 초안.

### 2.8 이 설계에서 미리 정한 것 (다시 논증하지 않는다 · 틀렸으면 고치고 이유를 적는다)

- 판정 근거 파일은 OSZICAR 다 — OUTCAR 정보의 **결측**은 (잘린 OUTCAR) 실행 실패를 허용하고, OSZICAR 쪽 결측 (k > N + 1) 은 미확인이다.
- 환경 등급 모순은 **그 잡의 최종 상태를 덮는다** (OK 의 뜻을 지킨다) + 집계에서 **전역 정지** (어느 시도에서 발견되든).
- 봉인 거부는 무결성 · 환경만 — 물리 실패는 질문별로 남는다 (은의 실행 실패가 탄소 해제를 막지 않는다).
- 커널 · 재시작의 **긍정 문구는 파일럿 원문으로만** 정한다 (지금 후보 문자열을 5.4.4 정답으로 박지 않는다 · CZ).
- 등록부 schema v2 (아직 봉인한 등록부가 없어서 옛 판과 섞일 일이 없다).

## 3. 원격 · 바로 쓸 블록

- **li2s QE 회수 (kgy · 사용자가 '■ 끝' 을 붙인 뒤)**: RUN = `~/work/runs/li2s_model_check_sp_2026_10_21` (sp 10 · pulay 2 · kpt 1 · 로그 chain.log) →
  레포 쪽 자리는 `db/raw/lpscl_glass_model_check_2026_10_19/qe_sp/{sp,pulay,kpt}/` (glass_model_check.py `QE_SP_ROOT` · `SP_DIRS`).
  블록 꼴은 10-21 W_ad ② 회수 블록과 같게 (kgy 메인 저장소 `~/lldvar` 는 linked worktree — `git -C ~/lldvar rev-parse --git-dir` 로 묻는다 ·
  새 worktree 를 **<이 세션 브랜치>** 에서 만들고 · scf.in/scf.out/stdout 류 + SHA256SUMS + SOURCE_COMMIT · `git push origin HEAD:<이 세션 브랜치>` 를 마지막 줄 끝에).
  회수 뒤 클라우드에서 SHA256SUMS 대조 → `python3 tools/ionic/glass_model_check.py --sp --out <json>` → 카드 개정 9 규칙대로만 읽는다.
- **Nd EOS (kgy)**: 12 점 끝 확인 → `make_eos_inputs.py --fit` (기록 `ndo_site_dft_runlog_2026_10_15.json`) — li2s 사슬이 그 뒤 잠금을 잡으므로 V₀ relax 는 li2s 뒤.
- **gabia r2 감시**: `watch -n 30 bash /root/w_li3nd_r2.sh` (사용자 것) · 추세 읽기 블록은 이 세션이 10-22 에 준 것 (dE · max|F| · Total · 거부 · 리셋).

## 4. 사용자가 정할 것

- **[W_ad]** LOCPOT 면평균을 파일럿 S_A far 에 더할까 (CZ Q-CZ-7 권고 · 잡 수 그대로 · LOCPOT 원본은 반송 안 함 · 1 차원 텍스트만 · 정보이지 합격선 아님) —
  권고: **더한다** (분리 끝점 전하 재분배를 볼 다른 자료가 없고, 나중에 더하면 묶음을 또 봉인해야 한다).
- **[W_ad]** 고친 묶음을 Codex 에 한 번 더 보일까 (편지 DB · diff 만) — 권고: **본다** (P0 다섯이 전부 검사 경로라 같은 꼴의 실수가 또 숨기 쉽다).
- **[W_ad]** 업체 발송 시점 — 고친 묶음 · (DB 를 하면 그 회신) 뒤 · 사용자.
- **[SEI]** Li₃Nd r2 — 이번 실행 한도 (≈ BFGS 386) 에서 안 끝나면 거기서 '미수렴' 으로 닫을지 (권고) / 한 번 더 늘릴지.
- 그 밖 대기 (■4 끝 줄 그대로): Nd S 빈자리 마감 비준 · Nd 페이지 송부 · cascade 상한 재비준 (🔔) · DEM 편지 (🔔) · Feng/Wang ③ (🔔) · BVSE R₀ 민감도 · Li₂S NEB 카드.

## 5. 주의

- 이 카드 커밋 뒤로 friendly 에 쓰지 않는다 (이 세션 · 원격 · 대피 세션 모두). 대피 세션이 끝나 복귀할 때까지 friendly 세션 (…CTzs) 을 다시 쓰지 않는다 —
  사용자가 토큰이 돌아와 여기로 오면 먼저 복귀 절차 (■6) 를 밟는다.
- 리뷰받은 묶음 v1 폴더 · CZ 회신 원문 · 봉인 폴더는 그대로 둔다.
- `tools/wad/build_round2_vasp_package.py` 의 selftest 는 가짜 VASP 를 수십 번 돌린다 (몇 분) — 고침마다 전체를 돌리고, 빠른 확인은 해당 절만 떼어 보지 말고 전체로.
