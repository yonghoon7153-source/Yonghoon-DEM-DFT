# 인계 — 연장 세션 `claude/sdcp-dem-manuscript-si-pqwtv8` → 본 세션 `claude/stoic-knuth-NObVQ` 복귀 병합 (2026-09-29)

**작성** 2026-09-29 · **작성 세션** 연장 세션 (pqwtv8 · 09-28 대피 뒤 일을 이어받은 쪽)
**대상 독자** stoic-knuth 본 세션 (1저자: *"저쪽 origin 토큰 풀려서 이제 넘어가도 될듯 · 전처럼 충돌 안 나게 머지"* = 이 병합의 비준)

---

## 0. 한 줄

stoic-knuth (`b195ddb16` = 09-28 대피 인계 커밋) 는 이 브랜치의 **조상**이다 — 저쪽이 앞선 커밋 **0**.
⇒ **fast-forward 이고 충돌이 원리적으로 없다.**  단 하나의 조건: **병합 전에 stoic-knuth 에 아무것도 커밋하지 않는다**
(커밋 하나라도 먼저 하면 fast-forward 가 깨진다).  그리고 *"충돌이 없다"* 와 *"검증됐다"* 는 다른 말이다 — §3 검사를 한다.

## 1. 브랜치 기하 (실측 2026-09-29 · 원격 SHA 는 `git ls-remote` 로 확인)

⚠ 다른 브랜치의 헤드 SHA 는 적지 않는다 — 초판이 litdb 정본 헤드를 적었다가, 그 브랜치가 그날 움직여 **아직 fetch 안 한 클론의 문서 참조 검사가 "없는 커밋" 으로 떨어졌다** (게이트 안에서 실측).  이 문서의 SHA 는 전부 이 브랜치의 조상이다 (작성 때 `git merge-base --is-ancestor` 로 확인).

| 브랜치 | 원격 SHA | merge-base | 이쪽이 앞선 | 저쪽이 앞선 | 병합 형태 |
|---|---|---|---:|---:|---|
| `claude/stoic-knuth-NObVQ` | `b195ddb16` | `b195ddb16` | **39** (이 문서 커밋 포함) | **0** | ✅ fast-forward |
| `claude/friendly-meitner-lldvar` (litdb 정본) | (움직이는 브랜치 — 적지 않는다) | — | — | — | 무관 — **이 브랜치는 `litdb/` 를 건드리지 않았다** (`git diff --stat b195ddb16..HEAD -- litdb/` 비어 있음) |
| `claude/dft-script-generator-webapp-GPSAG` (리포 기본) | (적지 않는다) | — | — | — | ⛔ **다른 계보** — PR base 로 쓰지 않는다 (09-15 인계 §1) |

이쪽 HEAD = **이 문서를 담은 커밋** (자기 SHA 는 적을 수 없다 — §2 의 `DOC_OK` 검사가 그것을 확인한다).

## 2. 병합 절차 (저쪽 세션이 그대로 실행)

```bash
# ⓪ 아무것도 커밋하기 전에 — 작업 트리 · 로컬 커밋이 깨끗한가
git status --short                                          # 비어야 한다
git fetch origin claude/stoic-knuth-NObVQ && S=$(git rev-parse FETCH_HEAD)
git log --oneline "$S"..HEAD                                # 비어야 한다 (푸시 안 된 로컬 커밋 0)

# ① 기하 — 브랜치별 fetch 를 한 번에 하나씩 · 전체 `git fetch origin` 을 사이에 끼우지 않는다 (FETCH_HEAD 가 덮인다 · 진행 ㉗)
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && P=$(git rev-parse FETCH_HEAD)
git merge-base --is-ancestor "$S" "$P"   && echo FF_OK       # 원격 stoic ⊂ pqwtv8
git merge-base --is-ancestor HEAD "$P"   && echo LOCAL_FF_OK # 로컬 HEAD ⊂ pqwtv8
git cat-file -e "$P":docs/handoff_merge_to_stoic_knuth_20260929.md && echo DOC_OK
git diff --stat "$S" "$P" -- litdb/ | tail -1               # 비어야 한다
git rev-parse --is-shallow-repository                       # false 여야 한다 (true 면 git fetch --unshallow — 검사기가 SHA 실재를 본다)

# ② 병합 = fast-forward 만 (기하가 바뀌었으면 조용히 merge 커밋을 만들지 말고 멈춘다)
git checkout claude/stoic-knuth-NObVQ
git merge --ff-only "$P"

# ③ 검사 (§3) → ④ 푸시
bash scripts/check_all.sh; echo "EXIT=$?"                   # ⚠ 파이프로 받지 말 것 (종료코드가 삼켜진다 · SELF-29)
git push -u origin claude/stoic-knuth-NObVQ                 # 네트워크 오류면 2 · 4 · 8 · 16 s 간격으로 재시도
```

**FF_OK · LOCAL_FF_OK · DOC_OK 중 하나라도 안 나오면 멈추고 보고한다** (추측으로 rebase · force-push · merge 커밋을 만들지 않는다).
그 경우의 해법은 **이쪽 (pqwtv8) 에서 stoic 의 새 커밋을 먼저 반입해 다시 fast-forward 로 만드는 것**이다 (09-15 · 09-28 과 같은 방식).
충돌이 나면 한쪽을 골라 버리지 않는다 — 특히 `CLAUDE.md` 현재 상태 표 · `docs/reviews/findings.json` (id 단위) · `docs/session_20260923_progress.md` (시간순 둘 다) 는
양쪽 내용을 모두 살리고, 같은 항목을 양쪽이 바꿨으면 사용자에게 묻는다.

## 3. 병합 뒤 검사 — 붙은 리포가 자기일관한가

| 검사 | 명령 | 기대 |
|---|---|---|
| 전수 게이트 | `bash scripts/check_all.sh` | `✓ 전부 통과` · `EXIT=0` (이쪽 HEAD 에서 09-29 통과) |
| ⚠ 알려진 네트워크 흔들림 | `python3 scripts/litdb_promote.py --selftest` | 09-29 에 두 번 `git fetch` 가 connection reset · timeout (rc 1 / 124) 으로 떨어졌다 — **단독 재실행이 PASS** 면 코드 문제가 아니다 |
| 원장 | `python3 scripts/check_review_findings.py` | `원장 자기일관 ✓` — fast-forward 라 `claimed_fixed_sha` 가 그대로 산다 |
| 인용 금지 스윕 | `python3 scripts/check_review_findings.py --ban-sweep` | `철회값 누수 없음 ✓` |
| 문서 참조 | `python3 scripts/check_doc_refs.py --quiet` | `✓ 깨진 참조 없음` (09-29 에 검사기를 고쳤다 — 문서 폴더 기준 상대 경로 · `blob` 해시 표지) |
| litdb | `git diff --stat b195ddb16..HEAD -- litdb/` | 비어 있음 |
| 증거 바이트 | `git status --short` (체크아웃 직후) | 비어 있음 — `.gitattributes` 가 `docs/reviews/codex_*_evidence_*/**` 를 `-text` 로 둔다 (Codex 산출 CRLF 를 바이트 그대로 · 매니페스트 sha256 대조용).  CRLF 로 바뀐 것처럼 보이면 로컬 `core.autocrlf` 문제다 — **정규화 커밋을 하지 않는다** |

## 4. 무엇이 넘어가나 — 39 커밋 (09-28 01:25 ~ 09-29) · 139 파일 · +50,438 / −273

| 줄기 | 주요 산출 | 정본 |
|---|---|---|
| **믹서 고-Bo LH** (~22 커밋) | Codex 4 → 8 차: HBR4/5/6 수정 (반례 먼저) · ibb SLURM 경로 · 영수증 v2 · E0 정지 벽 계약 3/3 REJECT (`SELF-62`) · LH 세 시드 발사 (09-28 18:07) → **정지** (20:23, 1저자) · Codex 7 차 HOLD (`HBR7-01`~`06`) · D-1 = Codex 권고대로 · **D-2 = (중간)** · **v2.2 = 확인 18 런 먼저 · 선별 6 긴 런 후행** (마감 10-11) · **Codex 8 차 묶음** | `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` (v2.2) · `docs/reviews/codex_mixer_highbo_round8_bundle_20260929.md` · `docs/reviews/mixer_highbo_prereg_20260927.md` §0 Q8 |
| **LHS 인계** (~12 커밋) | ① 접촉 위상 감사 v1 → v2 · WSL 130/130 CLEAN ⇒ 인계 적격 (J20-a) · ② 퍼콜레이션 감사 · WSL 130/130 CLEAN ⇒ 인계 적격 (J20-b · `lhs_perc_audit.py` 33) · J20-c ① 값 저장 계획 · **64 인계표** (`lhsx_design_adapter.py` 14/14 · J20-d) · 체크리스트 | `docs/reviews/lhs_handover_judgments_20260924.md` J20 ~ J20-d · **`docs/lhs_handover_checklist_20260929.md`** · `docs/data/lhs_handover_20260928.csv` (130) · `docs/data/lhsx_handover_20260929.csv` (64) |
| 그 밖 | 순수 SE 판정 네 칸 · J19 union 병기 · FAM §12-5 봉인 문안 · 기준 상태 지문 · ps45 킷 5/5 · 발표 그림 2 장 · DFT 7 차 (Ag–C) · 10/2 보고서 DEM 인벤토리 | 진행 기록 ㉗ · ㉘ 과 그 뒤 불릿 |

원장: **374 → 412** (open 142 → 162 · claimed_fixed 214 → 216 · verified 13 → 29 · wontfix 5).  새 open 중 인계에 걸린 것 = `LHS-17`~`21` · `HBR7-01`~`06`.

## 5. 넘어간 뒤 — 지금 상태 (리포 기록 기준 · 날짜를 보고 읽을 것)

**먼저 읽을 것 (순서)**: ① `CLAUDE.md` 맨 위 현재 상태 표 (LHS · 믹서 두 행이 09-29 밤까지 갱신됨) ② `docs/session_20260923_progress.md` ㉗ 부터 끝까지
③ `docs/lhs_handover_checklist_20260929.md` ④ 믹서 등록 v2.2 의 §0 · §0-b · §4-d · §8.

| 트랙 | 마지막 기록 | 다음 (⬜ = 비준 · 사용자 입력 대기) |
|---|---|---|
| 믹서 본 캠페인 (WSL 10 런) | 09-29 01:57 KST watch: E0 3/3 · L 81–91 % ⇒ 완주 ≈ 09-30 새벽~오전 | 완주 확인 → 등록 판정선 (8×8×2 · 문턱 5 · HOLD 해소 (b)) 으로 판정 = **코팅 대리 LC ↔ 무코팅 LA** 헤드라인 (R-3) |
| 믹서 고-Bo LH (ibb) | LH 3 런 정지 (09-28 20:23 · 폴더 보존 · M · 겹침 미열람) · Codex 8 차 묶음 사용자에게 전달 (발송 확인 전) | ⬜ Codex 8 차 발송 · 판정 → **코드 선행조건 (10-01 목표)**: 쌍별 `--stiffen-se --hold-bo-pairwise` 생성기 (9 항 · ×28) · `mixer_deck_diff --allow E` · Q2 비교기 + rank 영수증 · `launch_policy` first-seed-block/rest · 시작 직전 관문 · 스모크 상태 필드 → DEV-ONLY 7 → Codex GO → 확인 18 런 (**10-02 발사면 결과 ≈ 10-13~14** · TECH 재실행 한 번이면 +4 일) |
| LHS 인계 | 130 · 64 인계표 = 설계 · 두께 · porosity union · φ · coverage 저장 · ① ② 감사 적격 · 값은 계산 전 | ⬜ ② 감사 TSV/JSON 전송 · ⬜ J20-c 비준 ⓐ WSL 재수확 v3 + 웹앱 배치 (130 · 64) ⓑ 생성기 `--webapp-groups contact` + `n_AM_measured` (`LHS-21`) ⓒ 배포 프로필 · ⬜ `LHS-20` · 그 뒤 ② 저장 → ③ φ_SE 감사 (일괄 실행 `run_lhs_fill_wsl.sh` 전 건은 계속 보류) |
| v100 | 09-28: rep288 진행 · ps45 15 런은 rep288 끝나면 자동 발사 (≈ 45 h) | 상태 확인은 사용자에게 (리포에 09-28 뒤 기록 없음) |
| kgy · ibb 기타 | Phase A 100 GPa 재현 · 순수 SE (㉗: 3/4 완주) | 상태 확인은 사용자에게 |
| 보고 | 10/2 DEM 파트 보고서 + 발표 (믹서 절 블랭크 · 1저자) · 주간보고 09-28~10-04 · 후막 바이모달 인벤토리 (`docs/report_20261002/`) | 작성 |

⚠ **브랜치 이름이 박힌 명령**: J20-b · J20-c 의 WSL 블록과 `~/dem-audit` 워크트리 명령은 `origin/claude/sdcp-dem-manuscript-si-pqwtv8` 을 가리킨다.
fast-forward 뒤 두 브랜치는 같은 커밋이지만, **앞으로는 `claude/stoic-knuth-NObVQ` 로 바꿔 쓴다** (pqwtv8 은 여기서 동결 — 이쪽 세션은 더 커밋하지 않는다).

## 6. 지킬 것 (CLAUDE.md 가 정본 · 이 이틀의 교훈만)

- **보고 → 설명 → 비준 → 실행.**  "발송됨" · "완주" 는 사용자 확인 뒤에만 적는다 (`SELF-59`).
- **고치기 전에 반례 먼저** (규율 ②) — 이번 이틀의 수정은 전부 옛 코드에서 실패를 먼저 확인했다.  적대 자기리뷰 (서브에이전트) 가 매번 P1–P2 를 더 찾았다 (① 12 항 · ② 9 항).
- **요약 · 집계 줄도 행 키 변경과 같은 시험에 묶는다** (`SELF-65` — 없는 키를 세면 항상 0 이고 초록이다).
- **확인하지 않은 파이프라인 서술을 문서에 쓰지 않는다** (`SELF-64` — 호출 경로를 끝까지 따라가 파일이 써지는 줄을 댈 수 있을 때만).
- 커밋 · PR · 코드 주석에 **모델 식별자를 넣지 않는다**.
