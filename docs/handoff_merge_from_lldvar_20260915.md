---
title: 인계 — lldvar 계보의 병합 기하 전수 조사
created: 2026-09-15
updated: 2026-09-15
type: guide
tags: [workflow, git, handoff, merge, branch-topology]
sources: [docs/handoff_merge_20260914.md (dq4ja3), docs/adr/0009-branch-is-the-home.md (dq4ja3), CLAUDE.md]
confidence: high
explored: false
verificationStatus: verified
verifiedAt: 2026-09-15
verifiedBy: "origin fetch --all --prune 직후 git for-each-ref / merge-base / rev-list 실측 23개 브랜치 전수"
---

# 인계 — `claude/friendly-meitner-lldvar` 계보의 병합 기하 (전수 조사용)

**작성** 2026-09-15 · **작성 세션** `claude/friendly-meitner-lldvar` (황화물 SE 계산 캠페인)
**우리 HEAD** `745cd2797503b1875ccb680e4e0a257e48d4c440`
**대상 독자** origin 쪽에서 병합을 판단·수행·검증할 세션
**전제** 2026-09-15 에 origin 토큰이 열렸다. 그 전에는 이 조사를 할 수 없었다.

---

## 0. 세 줄

1. **이 저장소는 한 저장소에 프로젝트가 넷 이상이고, 각자의 집이 브랜치다.** 23개 원격
   브랜치 중 대부분은 서로 **빈 루트 커밋**만 공유한다. 합치면 병합이 아니라 접붙이기다.
2. ⛔ **선행 인계 문서(dq4ja3, 2026-09-14)의 사실 하나가 틀렸다.** 거기 표의
   `merge-base … 없음` 은 실측과 다르다 — **`bf0dd1a32` 가 존재한다** (§2).
   틀린 방향이 위험한 쪽이다: `--allow-unrelated-histories` 라는 안전장치가 **안 걸린다**.
3. ⭐ **진짜 병합 후보가 셋 있고, 그 인계 문서는 그걸 못 봤다** (브랜치 5개만 비교했다).
   그중 하나는 **SDCP 원고 v5 DFT methodology·Table S1 12커밋**이고 **원고 마감이 9/16**이다 (§4).

---

## 1. 이 문서를 믿기 전에 — 재현 명령

아래 전부 `git fetch --all --prune` **직후** 실행했다. 읽는 쪽에서 그대로 재현할 것.

```bash
git fetch --all --prune
L=origin/claude/friendly-meitner-lldvar

# ① 브랜치 전수 + 기하
for b in $(git for-each-ref --sort=-committerdate --format='%(refname:short)' refs/remotes/origin); do
  read a c < <(git rev-list --left-right --count $L...$b)
  mb=$(git merge-base $L $b 2>/dev/null)
  printf "%-46s %-10s ahead(L)=%-5s ahead(them)=%-5s mb=%s\n" \
    "${b#origin/}" "$(git rev-parse --short=9 $b)" "$a" "$c" "${mb:-없음}"
done

# ② 우리 계보에서 갈라진 포크만 추리기 (merge-base 가 빈 루트가 **아닌** 것)
ROOT=bf0dd1a32ce3096a7bb67cb462a96f920c6dfab7     # = bf0dd1a32, 파일 0개인 빈 최초 커밋
for b in $(git for-each-ref --format='%(refname:short)' refs/remotes/origin); do
  if mb=$(git merge-base $L $b); then
    [ "$mb" != "$ROOT" ] && [ "$mb" != "$(git rev-parse $L)" ] && \
      echo "⭐ ${b#origin/}  mb=$(git log -1 --format='%h %ad %s' --date=short $mb)"
  else
    echo "⚠ ${b#origin/}  공통 조상 정말로 없음"
  fi
done
```

⚠ `git merge-base` 는 공통 조상이 없으면 **아무것도 안 찍고 종료코드 1** 이다.
그 빈 출력을 `없음` 으로 읽으면 §2 의 오류가 그대로 재생산된다. 종료코드를 봐야 한다.

---

## 2. ⛔ 선행 인계 문서 정정 — merge-base 는 **있다**

`docs/handoff_merge_20260914.md` (브랜치 `claude/battery-charge-discharge-webapp-dq4ja3`,
커밋 `dd3cb8c5f`) §1 표는 이렇게 적었다:

| 저쪽 표의 주장 | 실측 (2026-09-15) |
|---|---|
| `main` ↔ dq4ja3 merge-base **없음** | **`bf0dd1a32`** |
| `claude/friendly-meitner-lldvar` ↔ dq4ja3 merge-base **없음** | **`bf0dd1a32`** |
| `claude/bms-alpha-beta-verify` ↔ dq4ja3 merge-base **없음** | **`bf0dd1a32`** |
| `claude/stoic-knuth-NObVQ` ↔ dq4ja3 merge-base **없음** | **`bf0dd1a32`** |

**`bf0dd1a32` 가 무엇인가**: 2026-03-25 `Initial commit`, **추적 파일 0개인 빈 커밋**이다.

```bash
git ls-tree -r --name-only bf0dd1a32 | wc -l      # → 0
git rev-list --count origin/main                   # → 1
```

즉 `origin/main` 은 **그 빈 커밋 하나가 전부**이고, 거의 모든 브랜치가 거기서 뻗어 나왔다.

### 왜 이 정정이 중요한가 — 결론은 같지만 위험도가 다르다

저쪽의 **결론**("합치면 안 된다")은 옳다. 그러나 **근거가 틀리면 안전장치를 잘못 믿는다**:

- 저쪽 문서: *"`--allow-unrelated-histories` 로 억지로 붙일 수는 있지만"* → 그 플래그가
  **요구된다**는 전제.
- 실제: 공통 조상이 있으므로 git 은 **그 플래그 없이 그냥 머지한다.** 사람이
  "플래그를 안 썼으니 안전하다" 고 읽을 자리가 생긴다. **실수로 실행될 수 있는 상태**다.
- 결과는 빈 조상 기준의 3-way merge = 겹치는 모든 경로에서 `both added` 충돌.
  겹치는 루트 경로 실측 (lldvar ∩ stoic-knuth): `.claude` `.gitattributes` `.gitignore`
  `CLAUDE.md` `README.md` `docs` `litdb` `scripts` `tools` `webapp` — **루트 `CLAUDE.md`
  가 겹친다**. 프로젝트의 규율 파일이 충돌한다는 뜻이다.

### 저쪽이 왜 틀렸을지 (추정, 확정 아님)

`git merge-base` 의 빈 출력을 `없음` 으로 옮겨 적었을 가능성이 높다 — 원격 ref 가 아직
fetch 되지 않았거나 종료코드를 안 봤을 때 정확히 그렇게 된다. 이것은 우리 `CLAUDE.md`
코드 규율의 **"'못 찾음'과 '없음'을 구분한다"** 가 문서에서 재현된 사례다.
⚠ 이 추정은 확인하지 않았다. 저쪽 세션이 실제로 무엇을 실행했는지는 모른다.

**정정 요청**: 저 문서를 고칠 권한은 그 브랜치에 있다. 이 문서는 **정정을 주장할 뿐
저쪽 파일을 건드리지 않는다.**

---

## 3. 브랜치 기하 전수 (2026-09-15 실측, 23개)

기준 `L = origin/claude/friendly-meitner-lldvar` = `745cd2797`

| 브랜치 | HEAD | 최종 | L 만 | 저쪽만 | merge-base | 분류 |
|---|---|---|---:|---:|---|---|
| `claude/friendly-meitner-lldvar` | `745cd2797` | 09-14 | 0 | 0 | 자기 | **우리** |
| `claude/windows-reinstall-backup-oducnh` | `7880ace88` | 08-24 | 1378 | **12** | **`40ff07965`** | ⭐ **우리 포크** |
| `claude/md-status-monitoring-q2xbu1` | `f7e32d005` | 08-24 | 1378 | **11** | **`40ff07965`** | ⭐ **우리 포크** |
| `rescue/lineage-2026-06-nd-pair01` | `a90fd1cf9` | 06-16 | 3260 | **7** | **`3183da308`** | ⭐ **우리 포크** |
| `main` | `bf0dd1a32` | 03-25 | 3561 | 0 | `bf0dd1a32` | 빈 루트 |
| `claude/14-gate-code-review-9qkx05` | `9326dc228` | 09-14 | 3561 | 737 | `bf0dd1a32` | BMS |
| `claude/bms-alpha-beta-verify` | `698d226de` | 09-14 | 3561 | 733 | `bf0dd1a32` | BMS |
| `claude/battery-charge-discharge-webapp-dq4ja3` | `dd3cb8c5f` | 09-14 | 3561 | 420 | `bf0dd1a32` | 충방전 웹 |
| `claude/battery-charge-discharge-webapp-vag24d` | `a7efba10b` | 08-24 | 3561 | 113 | `bf0dd1a32` | 충방전 웹 |
| `claude/sdcp-dem-manuscript-si-pqwtv8` | `ed9050e0f` | 09-14 | 3561 | 2709 | `bf0dd1a32` | DEM |
| `claude/stoic-knuth-NObVQ` | `ed9050e0f` | 09-14 | 3561 | 2709 | `bf0dd1a32` | DEM |
| `claude/phase-a-96arm-kgy` | `48d145f1e` | 09-12 | 3561 | 2564 | `bf0dd1a32` | DEM |
| `manuscript-track` | `f70446c5f` | 09-03 | 3561 | 2381 | `bf0dd1a32` | DEM |
| `Codex/dem-mpm-crosscheck` | `ee445817c` | 08-07 | 3561 | 1991 | `bf0dd1a32` | DEM |
| `claude/review-ml-migration-1BN1c` | `ac7bed0e9` | 05-06 | 3561 | 196 | `bf0dd1a32` | 기타 |
| `claude/zip-git-gpu-setup-vdqdtd` | `1b436de5d` | 08-28 | 3561 | 136 | `bf0dd1a32` | 기타 |
| `claude/resistor-network-solver-LDjW6` | `9a49cfa72` | 07-21 | 3561 | 97 | `bf0dd1a32` | 기타 |
| `claude/market-research-presentation-bC9Yi` | `a35442859` | 04-17 | 3561 | 20 | `bf0dd1a32` | 기타 |
| `claude/dft-script-generator-webapp-GPSAG` | `3fe789ff6` | 03-26 | 3561 | 16 | `bf0dd1a32` | 기타 |
| `claude/solid-state-cathode-improvement-hevry0` | `921e8c98c` | 07-15 | 3561 | 15 | `bf0dd1a32` | 기타 |
| `claude/li2s-assb-wiki` | `bbfa5f607` | 09-11 | 3561 | 11 | `bf0dd1a32` | 위키 |
| `claude/midni-formation-wiki` | `4355e06bd` | 09-11 | 3561 | 4 | `bf0dd1a32` | 위키 |
| `Codex/friendly-meitner-lldvar` | `dde6b77cd` | 08-08 | 3562 | **1** | **없음** | ⚠ **진짜 무관** |

### 표에서 반드시 읽어야 할 네 가지

1. **`Codex/friendly-meitner-lldvar` 만이 진짜로 공통 조상이 없다.** 고아 커밋 1개
   (`Complete PTFE UMA to VASP validation workflow`). 이름이 우리와 같아서 **혼동 위험이
   제일 크다** — `Codex/` 접두어를 반드시 확인할 것.
2. **`claude/li2s-assb-wiki` 는 이름에 Li2S 가 들어가지만 우리 계보가 아니다**
   (merge-base = 빈 루트). 우리 Li₂S 1층 게이트 작업과 **무관한 다른 프로젝트**다.
   이름으로 묶지 말 것.
3. `claude/sdcp-dem-manuscript-si-pqwtv8` 와 `claude/stoic-knuth-NObVQ` 는 **같은 커밋**
   (`ed9050e0f`) 을 가리키는 두 이름이다.
4. **`main` 은 우리보다 앞선 커밋이 0개다.** 기술적으로 fast-forward 가 가능하다.
   그러나 §6 을 읽기 전에 실행하지 말 것.

---

## 4. ⭐ 진짜 병합 후보 셋 — 우리 계보의 포크

이 셋만이 `merge-base` 가 **우리 커밋**이다. 즉 우리 브랜치에서 갈라져 나갔고,
**우리에게 없는 작업을 들고 있다.** 선행 인계 문서는 브랜치 5개만 비교해서 이 셋을
전부 놓쳤다.

### 4.1 `claude/windows-reinstall-backup-oducnh` (12커밋) — **최우선**

merge-base `40ff07965` (2026-08-21, *"판정: 무질서 Li6PS5Cl 에서 단일 Li NEB 는 성립하지 않는다"*)

```
7880ace88 08-24 백업 대화의 C: 오판 정정 — repo 7벌은 D: 였다
f7e32d005 08-24 U(Ni 3d)=6.2 출처 확정 — MP 기본값과 MATCH, Table S1 에 Jain 2011 삽입
6ed6c13bc 08-24 open_items 에 S 항목 — U(Ni 3d)=6.2 원전 미보유 (원고 v5 Table S1 무출처 수치)
77850e093 08-24 U(Ni 3d) 원전 확인 도구 신설 — check_ldauu_provenance.py
1f6b77655 08-23 근거문서에 참고문헌 매핑(본문 번호 <-> SI S-번호) 기록
34c7b85b8 08-23 Table S1 에서 미확정 인용 2건 제거 — Source "-" 로, UMA 를 S4 로
9a491d161 08-23 Table S1 압축(29→17행) + 각주 a 제거, 내용은 kb 방어 카드로
48a32565c 08-23 E_ads 를 번호 붙은 별행 수식 (3) 으로 분리
722ab3d08 08-23 DFT 파트 개정 — 본문에서 caveat 제거·각주로, 캡션 2개 추가
d8f0569f4 08-23 SDCP 원고 v5 DFT 파트 Word 산출 — Computational details + Table S1
4a3452b79 08-23 DFT methodology 초안을 wave1 발주판 기준으로 재작성
36a8383de 08-23 SDCP 원고 v5 — DFT methodology · Table S1 초안 + 파이프라인 리스트
```

**우리 브랜치에 없는 파일 5개** (실측 `git cat-file -e`):

| 파일 | 우리 |
|---|---|
| `docs/manuscripts/sdcp_dft_methods_draft_2026_08_23.md` | ⛔ 없음 |
| `docs/manuscripts/SDCP_DFT_methods_TableS1.docx` | ⛔ 없음 |
| `docs/manuscripts/sdcp_dft_methods_build.js` | ⛔ 없음 |
| `kb/syntheses/sdcp_eads_revision_defense_2026_08_23.md` | ⛔ 없음 |
| `kb/methodology/windows_reinstall_backup_2026_08_24.md` | ⛔ 없음 |
| `tools/sdcp/check_ldauu_provenance.py` | ⛔ 없음 |

⭐ **SDCP 원고 마감이 2026-09-16 이다.** 원고 v5 의 DFT methodology 와 Table S1 이
우리 브랜치에 없다는 것은 **지금 당장 영향이 있는 사실**이다. 이 조사에서 나온 것 중
가장 급한 항목이다.

⚠ 충돌 예상 지점: `kb/index.md`(생성물 — 손편집 금지, `tools/kb_wiki.py index` 로 재생성),
`kb/open_items.md`(양쪽 다 크게 바뀜).

### 4.2 `claude/md-status-monitoring-q2xbu1` (11커밋) — 4.1 의 **부분집합**

HEAD `f7e32d005` 는 4.1 의 두 번째 커밋이다. 즉 `windows-reinstall-backup-oducnh` 가
이것을 **포함한다**. 따로 병합하지 말 것 — 4.1 하나로 끝난다.

```bash
git merge-base --is-ancestor origin/claude/md-status-monitoring-q2xbu1 \
                             origin/claude/windows-reinstall-backup-oducnh && echo "부분집합 확인"
```

### 4.3 `rescue/lineage-2026-06-nd-pair01` (7커밋) — **대부분 이미 반영됨, 잔여 확인 필요**

merge-base `3183da308` (2026-06-11)

```
a90fd1cf9 06-16 db: Nd 4f PDOS — no in-gap defect states (electronically benign)
07d5c61d6 06-16 ops: KISTI sbatch JobName must be llm_finetuning_test
5e80bde6a 06-16 db: Nd pair01 — magnetization (abs 6.29 uB, AFM 2 Nd3+ 4f^3) + energy decomposition
d20c2e026 06-16 db: Nd pair01 — force/stress note (P=0.53 kbar, F=0.014 Ry/bohr)
b3769cdfa 06-16 db: Nd pair01 k-convergence PASS (k441=k661, dE 4e-8 Ry/atom)
75740b9df 06-16 ops: 2026-06-16 session note
216faad02 06-11 seminar: slide 18 axis-3 reinforced
```

파일 3개를 건드리는데 **셋 다 우리 브랜치에 존재한다**:

| 파일 | 상태 |
|---|---|
| `docs/ops/seminar_cascade_neb_ops_note_2026_06_16.md` | **blob 동일** (`77df7a0a2`) — 이미 반영 |
| `db/compositions/modelc_nd_doped.json` | 다름 (우리 쪽이 더 큼: +127/−43) |
| `kb/papers/lpscl_vs_lpscl16_seminar_v1.md` | 다름 (우리 쪽이 훨씬 큼: +385/−49) |

⚠ **파일 크기로 "우리가 최신" 이라고 결론짓지 말 것.** `modelc_nd_doped.json` 에서
`magnet|6.29|k441|k661` 매치가 **우리 14 vs 저쪽 16** 이다. 두 개가 어디로 갔는지
**키 단위로** 봐야 한다. 크기가 큰 쪽이 항상 상위집합은 아니다.

```bash
diff <(git show origin/claude/friendly-meitner-lldvar:db/compositions/modelc_nd_doped.json | python3 -m json.tool --sort-keys) \
     <(git show origin/rescue/lineage-2026-06-nd-pair01:db/compositions/modelc_nd_doped.json | python3 -m json.tool --sort-keys)
```

---

## 5. 프로젝트 군집 — 무엇이 무엇인지

브랜치마다 **루트에 자기 `CLAUDE.md` 가 있다.** 같은 저장소의 다른 프로젝트라는 뜻이다.

| 군집 | 브랜치 | 표식 (루트) |
|---|---|---|
| **황화물 SE DFT 캠페인 (우리)** | `claude/friendly-meitner-lldvar` (+포크 3) | `db/` `kb/` `tools/` `litdb/` `webapp/` `research-agent/` `factory/` |
| DEM/LIGGGHTS | `stoic-knuth-NObVQ` = `sdcp-dem-manuscript-si-pqwtv8`, `phase-a-96arm-kgy`, `manuscript-track`, `Codex/dem-mpm-crosscheck` | `DEM_BRANCH_CONSOLIDATION.md` `GB_correction_*` |
| BMS 밸런싱 | `bms-alpha-beta-verify`, `14-gate-code-review-9qkx05` | `bms-balancing/` `BRANCHES.md` `anchor_params` |
| 충방전 워크벤치 | `battery-charge-discharge-webapp-dq4ja3`, `-vag24d` | `apps/` `Makefile` `.claude-plugin` `packages/wrdkit` |

**우리 브랜치 규모**: 추적 파일 **7,625개** · 워킹트리 1.9 GB · `.git` 2.5 GB

| 디렉터리 | 파일 수 | 성격 |
|---|---:|---|
| `litdb/` | 4,190 | 문헌 PDF·digest (1.7 GB — **전송 시 반드시 제외**) |
| `db/` | 1,196 | **원장**: `db/governance/decisions.json`, `db/properties/canonical_registry.json`, `citation_hazards.json` |
| `tools/` | 636 | py 305 · sh 106 · 62k 줄 |
| `docs/` | 576 | 원고·슬라이드·ops |
| `kb/` | 572 | 위키 (frontmatter 필수, `kb/index.md` 는 **생성물**) |

---

## 6. 판정 — 무엇을 해도 되고 무엇을 하면 안 되나

### ⛔ 하면 안 되는 것

1. **군집이 다른 브랜치끼리 병합.** 겹치는 루트 경로가 `CLAUDE.md` 를 포함한다 —
   프로젝트의 규율 파일이 충돌한다. 빈 조상 때문에 git 은 **플래그 없이도 시도한다.**
2. **`main` 에 우리 브랜치를 fast-forward.** 기술적으로는 된다(`main` 이 우리 조상,
   우리보다 앞선 커밋 0개). 그러나 dq4ja3 의 **ADR 0009 "이 워크벤치의 집은 브랜치다"**
   가 이를 명시적으로 금지하고, 그 ADR 표는 **우리 브랜치를 이름으로 지목한다**
   (`claude/friendly-meitner-lldvar` = DFT 판, `webapp/app.py`·`factory/`·`kb/`, port 5001).
   `main` 을 한 프로젝트로 채우면 나머지 셋이 자기 저장소 기본 브랜치에서 남의 프로젝트를
   보게 된다.
   ⚠ **다만 이 ADR 은 다른 브랜치의 문서다.** 우리 브랜치의 `CLAUDE.md` 에는 *"브랜치
   `claude/friendly-meitner-lldvar` 에만 커밋/푸시. PR 생성 금지(요청 시에만)"* 만 있고
   `main` 금지 조항은 없다. **저장소 전체에 걸리는 규약인지 확정하는 것은 1저자의 판정**
   이고, 이 문서는 그 판정을 대신하지 않는다.
3. **우리 브랜치 히스토리 재작성.** 지금 **E′ 파일럿이 V100 에서 돌고 있고**, 그 기록
   `manifest.json` 에 `code_id = 634da438b` 가 박혀 있다. 그 커밋이 사라지면 "어느 코드로
   돌렸나" 를 못 답한다. `--force-with-lease` 조차 이 기간에는 쓰지 않는다.
4. **`litdb/` 를 포함한 전송.** 1.7 GB 다. `git bundle` 실측 1.95 GB · 전체 트리 1.9 GB
   vs `tools db kb` 만 84 MB.

### ✅ 해도 되는 것 (순서대로)

1. **§4.1 `windows-reinstall-backup-oducnh` 병합 검토** — 가장 급하다(원고 9/16).
   같은 계보라 정상 3-way merge 다. 예상 충돌은 `kb/index.md`·`kb/open_items.md` 둘.
   `kb/index.md` 는 **충돌을 손으로 풀지 말고** 병합 뒤 `python3 tools/kb_wiki.py index`
   로 재생성한다.
2. **§4.3 `rescue/lineage-2026-06-nd-pair01` 잔여 2건 확인** — 병합이 아니라
   **키 단위 대조**로 처리할 수 있다. 빠진 값만 우리 원장에 넣는 편이 안전하다.
3. **§4.2 는 §4.1 에 포함** — 따로 하지 않는다.

---

## 7. 병합을 실제로 할 때의 검증 사다리

우리 브랜치는 원장·게이트가 서로 물려 있다. 병합 뒤 **반드시** 이 넷을 통과시킨다.

```bash
python3 tools/db/validate_canonical.py       # 원장 정합 (값·status·comparison_group·prohibitions)
python3 tools/convention_check.py            # 물리 규약 복사본 갈라짐 (0 위반 유지)
python3 tools/kb_wiki.py index && python3 tools/kb_wiki.py lint   # 0 errors
python3 tools/doping/run_eprime_pilot.py --selftest                # 23/23
python3 tools/doping/watch_eprime.py --selftest                    # 32/32
python3 -m pytest webapp/tests/ -q                                 # ⚠ 2026-09-15 추가 — 아래 참조
```

> ⚠ **2026-09-15 추가 (§4.1 병합 실행 중 발견).** 위 사다리 초판에 **webapp 시험이 빠져 있었다.**
> 그래서 `/cascade` §4b 패널(09-13, `e6ad796e7`)이 `p4b.*` 6슬롯을 `|bold` 없이 찍어
> `test_no_literal_markdown_asterisks` 3건이 **병합 전부터** 떨어져 있었는데 아무도 못 봤다
> (`da12372c1` 에서 실측 3 failed). 병합 커밋 뒤 고쳤다. **사다리에 없는 검사는 안 돌아간 검사다** —
> 시험 묶음이 여럿이면 전부 적는다.

그리고 우리 `CLAUDE.md` 의 규율 중 **병합이 깨뜨리기 쉬운 것**:

- `db/governance/decisions.json` — `decision_state: active` 만 유효하다. 병합으로
  `proposed` 가 `active` 로 둔갑하면 **비준 없이 판정이 선 것**이 된다. 양쪽 항목을
  id 단위로 대조할 것.
- `db/properties/canonical_registry.json` · `citation_hazards.json` — 인용 금지 원장이다.
  `BLOCKED`/`HOLD`/`SUPERSEDED` 가 병합으로 사라지면 **철회된 값이 인용 가능해진다.**
- `kb/index.md` 는 **생성물**이다. 손편집·충돌 수동해결 금지.
- `webapp/` 의 claim 결속(`data-claim`) — 값이 화면에 실릴 때 표식이 같이 가야 한다.
  병합 뒤 음성시험(렌더된 HTML 에서 선언만 지우고 다시 스캔) 을 돌린다.

---

## 8. 지금 우리 브랜치에서 돌고 있는 것 (병합 시점 판단용)

| 항목 | 상태 |
|---|---|
| **E′ 파일럿** | 🟢 V100 tmux `eprime` 실행 중. out_root `$STORE/runs/eprime_2026_09_14`, `code_id 634da438b`, 준비 5 + MD 11 호출 = 30런, 상한 10 / 120 GPU-h |
| **G1 (Li₂S 1층 DFT 게이트)** | ⏸ kgy 의 modelc 종료 대기 |
| **SDCP 원고** | ⚠ 마감 **2026-09-16** — §4.1 이 여기 걸린다 |

**병합 창(window) 권고**: E′ 파일럿이 도는 동안에도 `merge` 자체는 안전하다(우리 repo 에
쓰는 것이지 V100 을 건드리지 않는다). 다만 **V100 의 `~/lldvar` 를 통째로 갱신하지 말 것** —
`tools/` 를 덮으면 `manifest.json` 의 `code_id` 와 실제 실행 코드가 갈라진다. 파일 단위로만
집어 간다 (`git show <ref>:<path>`).

---

## 9. 반론·한계

- **이 조사는 커밋 기하와 파일 존재까지다.** 내용 동등성은 §4.3 의 세 파일만 봤다.
  §4.1 의 5개 파일은 "우리에게 없다" 까지만 확인했고, **그 내용이 지금도 유효한지는
  안 봤다** (2026-08-23 작성분이고 그 뒤 우리 쪽에서 SDCP 판정이 여러 번 바뀌었다 —
  `db/properties/sdcp_neutral_closed_2026_08_28.json`, 회신 M 마감보류).
  **병합 전에 그 대조가 필요하다.**
- **dq4ja3 세션이 왜 `없음` 으로 적었는지는 추정이다** (§2). 확인하지 않았다.
- **ADR 0009 의 적용 범위는 미확정이다** (§6-2). 다른 브랜치의 문서가 우리 브랜치를
  구속하는지는 1저자 판정 사항이다.
- **`Codex/friendly-meitner-lldvar` 의 고아 커밋 1개는 내용을 안 봤다.**
  (`Complete PTFE UMA to VASP validation workflow` — PTFE 는 우리 캠페인 주제가 아니다)
- 브랜치 23개 중 **군집 분류는 루트 디렉터리 표식으로만** 했다. 각 브랜치의 `CLAUDE.md`
  를 실제로 읽지는 않았다.

---

## 10. 관련

- `docs/handoff_merge_20260914.md` (dq4ja3 `dd3cb8c5f`) — 선행 인계. §2 에서 정정.
- `docs/adr/0009-branch-is-the-home.md` (dq4ja3) — `main` 병합 금지 근거.
- `docs/handoff_merge_to_stoic_knuth_20260915.md` (stoic-knuth `ed9050e0f`) — DEM 군집 인계.
- `bms-balancing/MERGE_BRIEF_FOR_GATE.md` (bms `698d226de`) — BMS 군집 인계.
- `CLAUDE.md` (이 브랜치) — 데이터 규율·코드 규율·git 규율.
- `kb/open_items.md` ⏭-NOW-h — 현재 진행 상태.
