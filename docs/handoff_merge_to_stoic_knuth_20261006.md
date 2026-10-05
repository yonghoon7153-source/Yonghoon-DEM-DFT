# 인계 — 연장 세션 `claude/sdcp-dem-manuscript-si-pqwtv8` → 본 세션 `claude/stoic-knuth-NObVQ` 복귀 병합 (2026-10-06)

**작성** 2026-10-06 새벽 KST · **작성 세션** 연장 세션 (pqwtv8)
**대상 독자** stoic-knuth 본 세션 · 1저자: *"이제 다시 origin 대시보드/브랜치로 복귀해야되거든 · 예전처럼 충돌되지않고 잘 머지되게 프롬프트 다시 부탁해 · 특히 이종기술 관련해서 바로 팔로우할 수 있게 해줘"* → *"codex 요청서 받은다음에 머지 관련 프롬프트 짜자"* (= Codex 5차 판정 반입 뒤 · 이 병합의 비준)
**앞선 인계 (같은 양식)** `docs/handoff_merge_to_stoic_knuth_20260929.md`

---

## 0. 한 줄

stoic-knuth 의 원격 헤드 `d0b495cf4` (10-03 04:14 KST · τ 명명 규약 커밋) 는 이 브랜치의 **조상**이고 저쪽이 앞선 커밋은 **0** 이다.
⇒ **fast-forward 이고 충돌이 원리적으로 없다.**  조건은 하나 — **병합 전에 stoic-knuth 에 아무것도 커밋하지 않는다.**
*"충돌이 없다"* 와 *"검증됐다"* 는 다른 말이다 — §3 검사를 한다.

## 1. 브랜치 기하 (실측 10-06 05시 KST · 원격 SHA 는 `git ls-remote` 로 확인)

⚠ 다른 브랜치의 헤드 SHA 는 적지 않는다 (09-29 인계 §1 — 움직이는 헤드를 적으면 아직 fetch 안 한 클론의 문서 참조 검사가 떨어진다).  이 문서의 SHA 는 전부 이 브랜치의 조상이다.

| 브랜치 | 원격 SHA | merge-base | 이쪽이 앞선 | 저쪽이 앞선 | 병합 형태 |
|---|---|---|---:|---:|---|
| `claude/stoic-knuth-NObVQ` | `d0b495cf4` | `d0b495cf4` | **77** (`92b6ebde1` 까지) + Codex 5차 반입 · 이 문서 | **0** | ✅ fast-forward |
| `claude/friendly-meitner-lldvar` (litdb 정본) | (적지 않는다) | — | — | — | 무관 — **이 브랜치는 `litdb/` 를 건드리지 않았다** (`git diff --stat d0b495cf4..HEAD -- litdb/` 비어 있음) |
| `claude/dft-script-generator-webapp-GPSAG` (리포 기본) | (적지 않는다) | — | — | — | ⛔ 다른 계보 — PR base 로 쓰지 않는다 |

이쪽 HEAD = **이 문서를 담은 커밋** (자기 SHA 는 적을 수 없다 — §2 의 `DOC_OK` 가 확인한다).
`d0b495cf4..92b6ebde1` = 1,605 파일 · +271,260 / −7,780.

⚠ **이쪽에 커밋이 더 생기면** (예: 1저자 비준 뒤 194 배포 v1.2 · 검산기 수정) 같은 프롬프트를 **다시 붙이면 된다** (fast-forward 반복) — 단 그 사이 stoic-knuth 에 아무것도 커밋하지 않았을 때만.

## 2. 병합 절차 (저쪽 세션이 그대로 실행)

```bash
# ⓪ 아무것도 커밋하기 전에 — 작업 트리 · 로컬 커밋이 깨끗한가
git status --short                                          # 비어야 한다
git fetch origin claude/stoic-knuth-NObVQ && S=$(git rev-parse FETCH_HEAD)
git log --oneline "$S"..HEAD                                # 비어야 한다 (푸시 안 된 로컬 커밋 0)

# ① 기하 — 브랜치별 fetch 를 한 번에 하나씩 · 사이에 전체 `git fetch origin` 을 끼우지 않는다 (FETCH_HEAD 가 덮인다)
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && P=$(git rev-parse FETCH_HEAD)
git merge-base --is-ancestor "$S" "$P"   && echo FF_OK       # 원격 stoic ⊂ pqwtv8
git merge-base --is-ancestor HEAD "$P"   && echo LOCAL_FF_OK # 로컬 HEAD ⊂ pqwtv8
git cat-file -e "$P":docs/handoff_merge_to_stoic_knuth_20261006.md && echo DOC_OK
git diff --stat "$S" "$P" -- litdb/ | tail -1               # 비어야 한다
git rev-parse --is-shallow-repository                       # false 여야 한다 (true 면 git fetch --unshallow — 검사기가 SHA 도달을 본다)

# ② 병합 = fast-forward 만 (기하가 바뀌었으면 조용히 merge 커밋을 만들지 말고 멈춘다)
git checkout claude/stoic-knuth-NObVQ
git merge --ff-only "$P"

# ③ 검사 (§3) → ④ 푸시
bash scripts/check_all.sh; echo "EXIT=$?"                   # ⚠ 파이프로 받지 말 것 (종료코드가 삼켜진다 · SELF-29)
git push -u origin claude/stoic-knuth-NObVQ                 # 네트워크 오류면 2 · 4 · 8 · 16 s 간격으로 재시도
```

**FF_OK · LOCAL_FF_OK · DOC_OK 중 하나라도 안 나오면 멈추고 보고한다** (추측으로 rebase · force-push · merge 커밋을 만들지 않는다).
그때의 해법은 **이쪽 (pqwtv8) 에서 stoic 의 새 커밋을 먼저 반입해 다시 fast-forward 로 만드는 것**이다 (09-15 · 09-28 · 09-29 와 같은 방식).
충돌이 나면 한쪽을 골라 버리지 않는다 — `CLAUDE.md` 현재 상태 표 · `docs/reviews/findings.json` (id 단위) · `docs/session_20260923_progress.md` (시간순 둘 다) 는 양쪽을 다 살리고, 같은 항목을 양쪽이 바꿨으면 1저자에게 묻는다.

## 3. 병합 뒤 검사 — 붙은 리포가 자기일관한가

| 검사 | 명령 | 기대 |
|---|---|---|
| 전수 게이트 | `bash scripts/check_all.sh` | `EXIT=0` (이쪽 HEAD 에서 10-06 통과) |
| ⚠ 알려진 네트워크 흔들림 | `python3 scripts/litdb_promote.py --selftest` | `git fetch` 가 connection reset · timeout 으로 떨어진 적이 있다 — **단독 재실행이 PASS** 면 코드 문제가 아니다 |
| 원장 | `python3 scripts/check_review_findings.py` | `원장 자기일관 ✓` (551 항목 · fast-forward 라 `claimed_fixed_sha` 가 그대로 산다) |
| 인용 금지 스윕 | `python3 scripts/check_review_findings.py --ban-sweep` | 누수 없음 |
| 문서 참조 | `python3 scripts/check_doc_refs.py --quiet` | `✓ 깨진 참조 없음` — 새 클론 조건 (`rev-list --remotes HEAD`) 으로도 10-06 확인 (로컬 전용 에이전트 커밋을 백틱 SHA 로 적은 진행 기록 한 줄을 평문으로 고쳤다) |
| litdb | `git diff --stat d0b495cf4..HEAD -- litdb/` | 비어 있음 |
| 증거 바이트 | `git status --short` (체크아웃 직후) | 비어 있음 — `.gitattributes` 가 `docs/reviews/codex_*_evidence_*/**` 를 `-text` 로 둔다.  CRLF 로 바뀐 것처럼 보이면 로컬 `core.autocrlf` 문제 — **정규화 커밋을 하지 않는다** |
| 스모크 격리 | (게이트 안) | 작업 트리가 깨끗해야 통과 — 커밋은 **로컬 커밋 → 게이트 → 푸시** 순서 |

## 4. 무엇이 넘어가나 — 10-03 ~ 10-06 (77 커밋 + 반입 · 인계)

| 줄기 | 주요 산출 | 정본 |
|---|---|---|
| **LHS 망 · 194 인계** (가장 큼) | J20-s ③ φ_SE 마감 · ④a 협착 전력 몫 · ④b Love–Weber 입자 응력 · ⑤⑥⑦ 생성기 묶음 · `stop_after='network'` → Codex RINT G1 · LHS 망 판정 (P1 4) → RGL → RGLR → RGLR2 → RGLR3 수정 (반례 먼저 · 다섯 번의 재검증) · **194 망 배치 10-05 22:13–22:49 KST 194/194** · 봉인 감사 SEALED_LEGACY 194 · 인계 v1.2 (130 × 251 · 64 × 253) · **Codex 5차 = 고정 194 행 ML 기술자 조건부 인계 GO** | `CLAUDE.md` LHS 행 끝 · `docs/data/lhs_network194_11fcf91e8/` · `docs/reviews/codex_review_rglr3_reverify_20261006.md` |
| **τ 명명 규약 · 결정 16 실행** | TAU-01~25 · `CL-94` (순수 SE 10 % 출처 철회) · D1 COMSOL (f_ion = User defined) · ② `tau_flux` · ②b 등급 τ = Hertz · 표기 *"수송 tortuosity"* (1저자 10-05) | `CLAUDE.md` τ 블록 · `docs/reviews/tau_conventions_judgment_v2_20261003.md` |
| **r_int G1** | G1-1/2/3 수정 · RINT-03 실침대 측정 · Codex = RINT 13 verified · 보조 수렴 `RGL-01` 닫힘 | `CLAUDE.md` §CL-81 절 끝 · `docs/reviews/codex_review_rint_g1_lhs_network_20261005.md` |
| **믹서 (DEV)** | dev-bo M 열람 (개발 자료) · `/mixer` 침대 보기 (M 열람된 DEV 5 런) · **dev-u LU212 · LU637 등록 · ibb 발사 (10-05 14:30 KST)** · 보조 판독기 · (가) 해석 규칙 · (나) 정확 좌표 · (다) 전 정밀도 덤프 | `CLAUDE.md` 믹서 행 끝 · `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` §11 · §12 |
| **이종기술** | 10-02 회의 원장 (발화 90) · **논지 정본 비준 (10-05)** · `/hetero` 비준 블록 표시 | `docs/hetero_thesis.md` · §6 |
| **보고** | 덱 v2 정정 · 주간보고 (09-28 ~ 10-04) · 보고자료 작성 원칙 · **10-06 09:00 보고 덱 조립기** | `docs/report_20261006/` · `docs/report_making_principles.md` · `docs/worklog/weekly_20261004.md` |
| 그 밖 | FAM §12-6 결과 (f = 0 적격 · f_(a) EXECUTION_FAILED) · 웹앱 런처 포트 주인 확인 · 수영 님 ML 1차 대조 | `docs/reviews/fam_platen_prereg_20260812.md` §12-6 · `docs/data/lhs_ml_crosscheck_20261005/README.md` |

원장: **470 → 551** (open 181 → 211 · claimed_fixed 237 → 253 · verified 46 → 81 · wontfix 6).

## 5. 넘어간 뒤 — 지금 상태 (리포 기록 기준 · 날짜를 보고 읽을 것)

**먼저 읽을 것 (순서)**: ① `CLAUDE.md` 맨 위 현재 상태 표 — LHS · 믹서 행은 10-06 까지 갱신 ② `docs/session_20260923_progress.md` 끝 열 줄
③ `docs/hetero_thesis.md` (비준 블록 · §3 · §4 · §5) ④ `docs/reviews/codex_review_rglr3_reverify_20261006.md` §1 · §6 · §7.

| 트랙 | 마지막 기록 | 다음 (⬜ = 1저자 비준 · 입력 대기) |
|---|---|---|
| **194 인계 (수영 님 · 1저자 *"무조건 되게"*)** | Codex 5차 (10-06): 고정 194 행 (CSV sha256 d1a05c64… 130 행 · b17e39a8… 64 행 — 전체 값 = 판정문 §1) = 모델 내부 ML 기술자 **조건부 인계 GO** · 재실행 불요 · Hertz = 기본 · Physics = 면적 + 협착 규약의 결합 민감도 (기본 학습 열 제외 · opt-in) · 범용 자동 검산기 · 물리 타깃 HOLD | ⬜ **배포 v1.2**: `scripts/lhs_release_build.py --columns-from <v1.1 열 사전> --add …` 로 v1.1 열 + ⑤⑥⑦ + τ Hertz (`f_ion_hertz` · `tau2_ion_hertz` · `tau_ion_hertz` · 상태 · 사유) · Physics τ = 별도 부록 파일 (opt-in) · README = **판정문 §7 문안 그대로** + §6 QV2 (상태 열 필수 · 비관통 빈칸 = ∞ ≠ 기술 실패 · log10(T) 는 폴드 안 후보 · T = φ/f 항등식이라 T 예측에 f · φ 를 같이 넣지 말 것) · QV5 (판 간격 해 ↔ L_mc 재척도 σ 표지) · QV6 (첫 출현에 "수송 tortuosity (T = φ_SE,mc / f_mc · 제곱근 아님 = 문헌의 tortuosity factor)") · ⬜ 검산기 `RGLR4-01` (C4 공통 칸 차이를 실패로) · `RGLR4-02` (C8 ID 집합 · 중복 · record hash) — 반례 먼저 · ⬜ QV4 (σ_e · σ_th · 전력 몫 인계) = 별도 amendment |
| **이종기술** | 논지 정본 비준 (10-05) · `/hetero` · 결정 D1–D6 제시됨 (미결) | **§6 을 그대로 따른다** |
| **믹서 dev-u (이종기술 강성 축 · 개발 탐색)** | ibb job 266320 (`LU212`) · 266321 (`LU637`) · 10-05 14:30 KST 발사 · NP 20 · 런당 ≈ 27 h ⇒ **≈ 10-06 17:30 KST 끝** · (나) 정확 좌표 job (LC 먼저) 은 QOS `cpu-60` 대기 (1저자 *"마스터 노드 실행 · scancel 안 함 — 자리 나면 시작"*) | §6-3 순서 (끝난 뒤) |
| **10-06 09:00 보고** | 덱 조립기 `docs/report_20261006/build_deck.py` (DEM 파트 · 믹싱 뺌) · 1저자가 PPT 를 직접 고친다 | 1장 각주 *"보정 목표 기공률 약 10 %"* 문구 확인 (알림 07:30 KST 이 세션에 예약됨) · 194 · Physics 문장은 Codex 5차 표현으로 (§7) |
| r_int | G1 verified 13 · G2 = 초안 ①′ v2 → Codex 재검토 (② 구현은 그 뒤) | 1저자 순서 결정 |
| FAM | §12-6 결과 · §12-7 gabia (A6000) = 다른 시뮬 끝난 뒤 · 이 결과를 본 뒤의 등록 | 1저자 |
| ibb 그 밖 | a5 · a6 런 (재개는 `scripts/resume_ckpt.sh` 로만 · CLAUDE.md 체크리스트) — 10-05 저녁 `a6_p04` 는 시한 ≈ 10-06 04:49 KST | 상태 확인은 1저자에게 (리포에 그 뒤 기록 없음) |

⚠ **브랜치 이름이 박힌 명령**: 194 배치 · 인계 · WSL `~/dem-audit` 워크트리 명령은 `origin/claude/sdcp-dem-manuscript-si-pqwtv8` 을 가리킨다.  fast-forward 뒤 두 브랜치는 같은 커밋이다 — **앞으로는 `claude/stoic-knuth-NObVQ` 로 바꿔 쓴다.**  pqwtv8 세션은 병합이 끝나면 더 커밋하지 않는다 (§1 의 *"커밋이 더 생기면"* 은 병합 **전** 의 경우).

## 6. 이종기술 — 바로 팔로우 (1저자 요청)

### 6-1. 정본 · 화면

- **정본** `docs/hetero_thesis.md` (1저자 비준 10-05 · *"중간에 이게 흔들리면 전체가 흔들려버리니까"*) — §1 비준 블록 (고정 문장 · 하지 않는 말 · 예측 P1–P3) 은 표지 `THESIS:BEGIN` … `THESIS:END` 사이 · **바꾸려면 저자 비준**.
- **웹앱** `/hetero` 가 그 블록을 **파일에서 읽어** 띄운다 (베끼지 않는다 · `webapp/test_hetero_transcript_page.py` ⑨–⑬) · `/hetero/transcript` = 회의 원장 `docs/data/hetero_transcript_20260918.json` · `docs/data/hetero_transcript_20261002.json` (발화 번호가 근거 단위).
- 논문 · 보고 · 믹서 설계에서 코팅 · 분산을 말하기 전에 그 문서를 본다 (`CLAUDE.md` 이종기술 절).

### 6-2. 흔들림 위험 — 모델 ↔ 논지 어긋남 (§3) · 열린 결정 (§4)

- 확인 블록의 질문 (LC ↔ LH contrast) 은 논지와 같지만 **모델이 그 기전을 아직 안 담는다**: dev-bo = **AM–AM** 응집 ↔ 논지 = **SE–SE** · LH 비코팅 표면 에너지 근거 없음 · SE–SE 충돌 불점착 (붙는 속도 상한 0.16 mm/s) · AM–SE min 규칙.
- 1저자 결정 대기 (권고는 정본 §4 표):

| # | 결정 | 권고 (정본) |
|---|---|---|
| D1 | 확인 18 런 (LC ↔ LH) 시점 | P1 을 시험할 비코팅 팔 (근거 있는 표면 에너지) 이 정해진 뒤 |
| D2 | 믹서 변수 | 표면 에너지 → 쌍별 접착일 (결합 규칙) → CED · LC 는 그대로 · 브리핑 초안 §4 의 U · S · G 는 후보 |
| D3 | SE–SE 점착 수준 | SE 분말 유동성 (안식각 · Hausner 비 등) 실험 앵커 |
| D4 | DFT | 코팅 전후 표면 에너지 · 계면 분리일 계산 요청 |
| D5 · D6 | 10/21 덱 | 믹싱 내용 빼기 (10-02 #67) · 한글 글꼴 = 맑은 고딕 (음성 337 · `docs/report_making_principles.md`) |

- 다음 순서 (정본 §5): 변수 재정의 (D2) → SE–SE 앵커 (D3) → 관측량 (이론 분모 Lacey · 상별 지수 · SE 덩어리 크기 분포 · AM–SE 접촉 비율) → 혼합 상태 → 압축 DEM → 망 (`stop_after='network'`) → σ_ion · coverage · τ (P3) → DFT · 실험.

### 6-3. dev-u (LU212 · LU637) 가 끝나면 — 순서 (10-06 17:30 KST 이후)

정본 = `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` §12 (v2.9 · DEV 전용 · 사후 설계 · 공동 개입 9 원소 · 판정 아님).

1. 완주 확인 (sacct · 로그 끝) — **M 을 열기 전에** 보조 판독기를 돌릴 준비: `scripts/mixer_contact_reader.py` (s1 SE–SE 군집 · s2 AM–SE 부착 · LC_ref_r2 · E0_ref 와 같은 식).
2. **§12-4 해석 규칙 (가)** (1저자 10-05 · LU 열람 전 등록): [확실, 가능] 범위가 **안 겹칠 때만** 차이라고 말한다 · 겹치면 *"덤프 해상도로 가를 수 없음"* (s1 은 못 가를 가능성이 크다 — LC t₀ SE 군집 분율 범위 0.27–0.98).
3. (나) 정확 좌표 `scripts/mixer_exact_frames.py` — settled + 마지막 두 체크포인트 · 보고 전용 · **LC 먼저**, LU 는 열람 때.  ibb 에서 job 이 돌았으면 `log.exact` 의 `EXACT_STEP` · `ERROR` 부터 본다.
4. ⚠ **빠진 원자 처리** (잃은 원자 ≤ 10 · id ⊆ 1..N · 집합 불변) = 권고 · **미비준** — 구현은 에이전트 브랜치의 로컬 전용 커밋 fabdd7be9 (원격에 없다 · 이 병합으로 넘어가지 **않는다**) · 비준되면 같은 내용을 다시 구현하거나 그 세션에서 반입.
5. M 열람 기록 → 등록 §12 · `/mixer` 개발 이력 (판정 미사용 · 개발 자료 · n = 1 · 사후 선택 표기).

### 6-4. 보고되지 않은 초안 · 10/21 자료

- `docs/reviews/mixer_cohesion_briefing_draft_20261002.md` — 에이전트 초안 · **1저자 미보고** (내용을 쓰기 전에 1저자에게 먼저 보고 → 설명 → 비준).
- 10/21 이종기술 덱: D5 (믹싱 빼기) · D6 (맑은 고딕) · 보고자료 원칙 문서대로.
- 배경 문헌 reference 화 (정본 §6) = **10/21 자료가 끝난 뒤** · 지금은 검색 낱말뿐 (인용 아님 · 규율 ⑥ — 원문 PDF 로 확인한 litdb 정본 카드만).

### 6-5. 본 세션의 첫 행동 (권고)

1. `/hetero` 를 열어 비준 블록 · 회의 원장이 뜨는지 확인 (병합 뒤 웹앱 재시작).
2. 1저자에게 D1–D6 중 **D2 → D3** 부터 결정을 받는다 (D2 가 정해져야 비코팅 팔 덱을 만들 수 있다).
3. 17:30 이후 §6-3 순서.

## 7. 지킬 것 (CLAUDE.md 가 정본 · 이번 나흘의 교훈만)

- **보고 → 설명 → 비준 → 실행.**  "발송됨" · "완주" 는 1저자 확인 뒤에만 적는다.  1저자에게는 **게이트 · 커밋 얘기 없이 결과만 담백하게**.
- **고치기 전에 반례 먼저** (규율 ②).  Codex 판정 반입 = 판정문 · 증거 (`source/` 는 manifest 만) · **우리 트리 재현** · 원장 · CLAUDE.md · 진행 기록을 한 묶음으로.
- **요청서 · README 문장은 시험 메시지 그대로** — 압축 · 과장이 세 번 원장에 올랐다 (`SELF-67` · `SELF-88` · `SELF-90`).  194 τ < 1 의 설명은 Codex 5차 표현만 쓴다: *"같은 망의 접촉 저항 없는 해가 이미 연속체 한계 위로 전도를 세고 (원기둥 내부 저항 — 겹치지 않는 단순입방도 T → 2/3) · Physics 는 면적과 협착식이 함께 다른 규약"* — ⛔ *"큰 면적이 접촉 저항을 지운다"* (legacy ψ 는 s > 0.4 에서 Rc 가 커진다) · ⛔ *"정의상 1 이 바닥"* (조건부 변분 상한).
- **로컬 전용 커밋을 백틱 SHA 로 적지 않는다** — 새 클론의 문서 참조 검사가 떨어진다 (10-06 실측).
- 커밋 · PR · 코드 주석에 **모델 식별자를 넣지 않는다**.

## 8. 붙여 넣을 프롬프트 (stoic-knuth 세션에)

```text
연장 세션 브랜치(claude/sdcp-dem-manuscript-si-pqwtv8)를 이 브랜치(claude/stoic-knuth-NObVQ)로 fast-forward 병합해줘.
인계 문서는 pqwtv8 쪽에만 있으니 먼저 읽어:
  git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git show FETCH_HEAD:docs/handoff_merge_to_stoic_knuth_20261006.md
1. 아무것도 커밋하지 말고 §2 를 그대로 해: 작업 트리 깨끗 · 로컬 커밋 0 → FF_OK · LOCAL_FF_OK · DOC_OK · litdb 비어 있음 · shallow false → git merge --ff-only.
   하나라도 안 나오면 rebase · force-push · merge 커밋을 만들지 말고 멈추고 보고해.
2. §3 검사 (check_all EXIT=0 · 원장 · ban-sweep · 문서 참조 · litdb · 증거 바이트) → claude/stoic-knuth-NObVQ 로 푸시.
3. 그다음 CLAUDE.md 현재 상태 표 → 진행 기록 끝 → 인계 §5 · §6 순서로 읽고 이어가.
   - 이종기술: §6-5 첫 행동부터 (D2 → D3 결정은 나한테 받고) · dev-u 는 10-06 17:30 KST 이후 §6-3 순서.
   - 194 인계: §5 표대로 — 배포 v1.2 와 검산기 수정은 내 비준 뒤.
보고 → 설명 → 비준 → 실행.  게이트 · 커밋 얘기는 빼고 결과만 담백하게.
```
