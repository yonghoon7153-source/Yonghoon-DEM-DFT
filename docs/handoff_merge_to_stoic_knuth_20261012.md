# 인계 — 연장 세션 `claude/sdcp-dem-manuscript-si-pqwtv8` → 본 세션 `claude/stoic-knuth-NObVQ` 복귀 병합 (2026-10-12 · 2판 10-13 KST 새벽)

**작성** 2026-10-12 KST · **2판** 2026-10-13 KST 새벽 (같은 연장 세션 — 첫 판 · U5 갱신 뒤 커밋 22 개 + 이 판) · **작성 세션** 연장 세션 (pqwtv8 · 서브 세션)
**계기** 1저자 10-12 이어받기 메시지 — *"이 세션의 작업 브랜치가 claude/stoic-knuth-NObVQ 가 아니면, 그 브랜치를 origin/claude/stoic-knuth-NObVQ 에서 시작하고 끝날 때 fast-forward 병합 인계 문서를 남긴다"* ·
2판 = 1저자 10-12 *"지금 figure등 관련해서 여기서 마치고 다시 돌아가야되니까 확실하게 해결해줘"*
**앞선 인계 (같은 양식)** `docs/handoff_merge_to_stoic_knuth_20261006.md`

---

## 0. 한 줄

stoic-knuth 의 원격 헤드 `46cd0bdb8` (10-11 밤 · DEM 지배방정식 배경 보고서) 는 이 브랜치의 **조상**이고 (이 세션은 그 커밋으로 fast-forward 한 뒤에만 커밋했다) 저쪽이 앞선 커밋은 **0** 이다 (10-13 새벽 `git ls-remote` 로 다시 확인).
⇒ **fast-forward 이고 충돌이 원리적으로 없다.**  조건은 하나 — **병합 전에 stoic-knuth 에 아무것도 커밋하지 않는다.**

## 1. 브랜치 기하 (10-13 새벽 · 원격 SHA 는 `git ls-remote` 로 다시 확인)

| 브랜치 | 원격 SHA | merge-base | 이쪽이 앞선 | 저쪽이 앞선 | 병합 형태 |
|---|---|---|---:|---:|---|
| `claude/stoic-knuth-NObVQ` | `46cd0bdb8` | `46cd0bdb8` | **34** — 묶음별 목록 = §4 · 그 안에 병합 커밋 1 (`abbc63a4b` = SUP20 수정 작업트리를 이 가지 안에서 합친 것 — fast-forward 에 영향 없음) · 마지막 = ps45 σ_e 인자 끔 진단 결과 반입 + 이 문서 2판 고침 (같은 커밋) | **0** | ✅ fast-forward |
| `claude/friendly-meitner-lldvar` (litdb 정본) | (적지 않는다) | — | — | — | 무관 — 이 세션은 `litdb/` 를 건드리지 않았다 |

이쪽 HEAD = **이 문서 2판 (고친 판) 을 담은 커밋** (자기 SHA 는 적을 수 없다 — §2 의 `DOC_OK` 가 확인한다).
⚠ 이쪽에 커밋이 더 생기면 같은 프롬프트를 다시 붙이면 된다 — 단 그 사이 stoic-knuth 에 아무것도 커밋하지 않았을 때만.

## 2. 병합 절차 (저쪽 세션이 그대로 실행)

```bash
# ⓪ 아무것도 커밋하기 전에 — 작업 트리 · 로컬 커밋이 깨끗한가
git status --short                                          # 비어야 한다
git fetch origin claude/stoic-knuth-NObVQ && S=$(git rev-parse FETCH_HEAD)
git log --oneline "$S"..HEAD                                # 비어야 한다 (푸시 안 된 로컬 커밋 0)

# ① 기하 — 브랜치별 fetch 를 한 번에 하나씩 (FETCH_HEAD 가 덮인다)
git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && P=$(git rev-parse FETCH_HEAD)
git merge-base --is-ancestor "$S" "$P"   && echo FF_OK       # 원격 stoic ⊂ pqwtv8
git merge-base --is-ancestor HEAD "$P"   && echo LOCAL_FF_OK # 로컬 HEAD ⊂ pqwtv8
git cat-file -e "$P":docs/handoff_merge_to_stoic_knuth_20261012.md && echo DOC_OK
git diff --stat "$S" "$P" -- litdb/ | tail -1               # 비어야 한다
git rev-parse --is-shallow-repository                       # false 여야 한다

# ② 병합 = fast-forward 만
git checkout claude/stoic-knuth-NObVQ
git merge --ff-only "$P"

# ③ 검사 (§3) → ④ 푸시
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 bash scripts/check_all.sh; echo "EXIT=$?"   # 파이프로 받지 말 것 (SELF-29)
git push -u origin claude/stoic-knuth-NObVQ                 # 네트워크 오류면 2 · 4 · 8 · 16 s 간격으로 재시도
```

**FF_OK · LOCAL_FF_OK · DOC_OK 중 하나라도 안 나오면 멈추고 보고한다** (rebase · force-push · merge 커밋을 추측으로 만들지 않는다).  해법은 이쪽 (pqwtv8) 에서 stoic 의 새 커밋을 먼저 반입해 다시 fast-forward 로 만드는 것.

## 3. 병합 뒤 검사

| 검사 | 명령 | 기대 |
|---|---|---|
| 전수 게이트 | `bash scripts/check_all.sh` (위 스레드 환경변수) | `✓ 전부 통과` · `EXIT=0` (이쪽 HEAD 에서 10-13 새벽 통과) |
| 원장 | `python3 scripts/check_review_findings.py` | `원장 자기일관 ✓` (644 → **652** 항목 — `SUP20-01` · `SUP20-02` · `SELF-107` · `PS45E-01` · `PS45E-02` · `PS45E-03` · `SELF-108` · `SELF-109` · 상태 claimed_fixed 277 · open 246 · verified 121 · wontfix 8) |
| 인용 금지 스윕 | `python3 scripts/check_review_findings.py --ban-sweep` | 누수 없음 (⚠ ps73 상자그림 원값 · SE 별 σ_VM 은 `.csv.gz` — 숫자 15만 개가 철회값 문자열과 우연히 겹친다 · 풀어서 커밋하지 말 것) |
| 문서 참조 | `python3 scripts/check_doc_refs.py --quiet` | `✓ 깨진 참조 없음` |
| 증거 바이트 | `git status --short` (체크아웃 직후) | 비어 있음 (`.gitattributes` = `docs/reviews/codex_*_evidence_*/**` `-text` · CRLF 로 보이면 로컬 `core.autocrlf` 문제 — 정규화 커밋 금지) |

## 4. 무엇이 넘어가나

### 4-1. 첫 판 (10-12 · 커밋 9)

| 줄기 | 산출 | 정본 |
|---|---|---|
| **Codex 세대 2 재검증 7 반입** (10-12 인계 작업 A) | 판정문 (바이트 그대로) · 증거 (slim 229 / 229 = 묶음 MANIFEST · 뺀 608 = `SLIM_EXCLUDED.tsv` · source 573 = 핀 `3cedd40a5` blob · parent 2 = `821f0e151` blob · baseline_r6 = 10-11 반입 · GitHub API 응답 넷 = git 으로 복원) · 우리 트리 재현 (묶음 재구성 → Codex `run_checks.py` 무변경 전부 rc 0 · 다시 읽기 자체시험 26 / 26 · 출력 113 판정값 차이 0 · `r7_contract` 우리 판 = Codex 와 같음 · 봉인 32 `code_fp e8b2496b…` 불변 · 인계 도구 `g2_network_reread.py` 지문 `248ee5c0…`) · 원장 `G2RR6-01` · `G2RR5-03` → **verified** (범위 = `verified_scope`) · 새 `G2RR7-01` (P3 · 요청서 문장 과장) → 정정 표지 → claimed_fixed · 1저자 10-12 순서 **(나)** 기록 | `docs/reviews/codex_review_gen2_network_reverify7_20261012.md` · `docs/reviews/codex_gen2_network_reverify7_evidence_20261012/_README_import.md` · `docs/reviews/g2rr6_fix_plan_20261011.md` 머리 |
| **Codex 언로딩 개정 1 재검토 반입** | 판정문 (바이트 그대로) · 증거 (묶음 154 / 154 · source 97 = 핀 `3409814a3` blob · upstream 27 = 10-11 반입과 같음) · 우리 트리 재확인 (Codex 탐침 무변경 재실행 JSON 같음 · 우리 식 인용 등록 줄 34 / 34 · 산술 전부 같음) · 원장 `UL-01` ~ `UL-10` 노트 (open 유지) · 새 `ULR1-01` · `ULR1-02` (P1) · `ULR1-03` · `ULR1-04` · `ULR1-05` (P2) · `SELF-105` · 반영 계획 | `docs/reviews/codex_review_dem_unloading_prereg_rereview_20261012.md` · `docs/reviews/codex_dem_unloading_prereg_rereview_evidence_20261012/_README_import.md` · `docs/reviews/dem_unloading_ulr1_fix_plan_20261012.md` |
| **보충 20 지원 (U1–U5)** (1저자 (나) · Q4 (가) lhss · Q5 (가) · Q6 (가) 하중 열) | 실행기 등록 집합 supp20 · 관측 필수 (130/130) · 다시 읽기 `--expect-set supp20` (30) · lhss 설계 어댑터 + 본 하중 열 (27/27 · `docs/data/lhss_design_adapted_20261012.csv` 20 × 40) · 인계 생성기 열 사전 lhss_* (389/389) · 배포 생성기 두 배치 · 214 결합 (`--supp-batch-root` · 234/234) · 봉인 32 무변경 · 짧은 Codex 검토 요청서 `docs/reviews/codex_supp20_support_review_request_20261012.md` · 자기 결함 `SELF-106` (v1.3 계획 §2-4 컨테이너 대조 문장) | `docs/reviews/g2rr6_fix_plan_20261011.md` §2 · `docs/reviews/lhs_release_v13_plan_20261007.md` §2b |

### 4-2. 2판에서 더해진 것 (10-12 아침 ~ 10-13 · 커밋 22 + 이 판 넷)

| 줄기 | 산출 | 정본 |
|---|---|---|
| **보충 20 — 재수확 · 등록 · Codex 검토 · 수정** | 재수확 r3 반입 (`c37d92dbe` · 1저자 WSL · 수확기 판 `1e09f661d` · 20/20 · r2 와 키별 대조 = 값 같음) · 등록 §2 지문 + 1저자 비준 (`b556dd5db`) · Codex 보충 검토 = **HOLD · 새 P1 없음** (`aaf12c595` · P2 `SUP20-01` · P3 `SUP20-02` · 194 R7 기술 GO 유지 · 우리 트리 재현 판정값 차이 0) · 수정 (1저자 Q1–Q4 = 전부 (가) · 반례 먼저 · `4cae3a464` · `dd87e069c` · 입력 지문 영수증 도구 `dfee89184` · 원장 · 증거 `9a82bf138` · 병합 `abbc63a4b` · 봉인 32 무변경 · 원장 claimed_fixed · `SELF-107`) · 짧은 재확인 요청서 (`a9422d2e7` · **리뷰 핀 = `a9422d2e7` 로 고정** — 이 판에서 정정: 뒤 커밋 `a9fa84244` 가 `scripts/` 에 보고 전용 실행기를 더해서, 발송 때의 HEAD 를 핀으로 적으면 요청서 §0 의 *"그 사이 다른 scripts/ · webapp/ 변경 0"* 이 거짓이 된다) | `docs/reviews/codex_review_supp20_support_20261012.md` · `docs/reviews/sup20_fix_plan_20261012.md` §6 · `docs/reviews/codex_sup20_fix_reverify_request_20261012.md` · `docs/reviews/lhs_network_batch_registration_20261012_supp20.md` |
| **DEM 언로딩 개정 2 · 판 속도** | REG §13 (`af3af8123` · 1저자 ULR1 계획 Q1–Q4 권고대로 · 결과 0 건 · `SELF-105` 같은 커밋) · 판 속도 = **plate velocity 0.01 mm/s** (1저자 — 발표 · 보고 용어 · 값 · 계산값 = DEM 지배방정식 보고서 §9-1 내부 기록) | `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §13 · `docs/reviews/dem_unloading_ulr1_fix_plan_20261012.md` |
| **σ₀ 보고 기준 · σ_e 실험 앵커** | σ₀ = **1.5 mS/cm** (`38cc6691f` · 1저자 *"1.5로 고정하자"* · 자료 · 보고의 절대 σ_ion = f × 1.5 · 망 σ ∝ σ₀ 라 다시 계산 없음 · f · 수송 tortuosity 불변 · 솔버 상수 3.0 = 봉인 32 그대로) · P:S 다섯 조성 σ_ion 경향 분해 (`06d2cf328` · ps45 g2 README 끝) · σ_e 실험 앵커 SBE 4.47 · DBE 12.4 mS/cm (정정값 · `bef5bd5d7`) → STEP3 표 값 재실행 **등록** (`bd1db419d` · 결과 0 건) + 실험 조성 = 실조성 (`58f40a002`) | `docs/data/ps45_r45_network_g2_20261007/README.md` §σ₀ · `docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md` |
| **ps45 σ_e 기준 (덱 p15 σe−) — Codex 판정** | 요청서 (`bd1db419d`) → 판정 반입 (`a919cd4c1` · **권고 (가′) 조건부** = Hertz H0 + PC 크기 인자 끔 + 공통 기준값 4.1 mS/cm 를 *"조건부 환산"* 으로 · 다섯 망 진단 뒤 · *"이중 할인 제거 = 정답"* 논리 불성립 · 실제 AM 고체 64.71–64.92 % · 전자 Physics g2 = native AM–AM 원판 + ψ = **Tabor 아님** · 우리 트리 재현 판정값 차이 0) · 원장 `PS45E-01` · `02` · `03` (P2 open) · `SELF-108` · `109` · README §σ_e · 전자 열 표지 고침 (수치 무변경 · `e7b803c41` · `dbade898a`) · 인자 끔 다섯 전자 망 진단 **결과 전 등록** + 보고 전용 실행기 (`a9fa84244` · 봉인 파일 무변경 · 별도 출력 · manifest 필수 · 자체시험 58/58 · 결과 0 건) | `docs/reviews/codex_review_ps45_sigmae_reporting_20261013.md` · `docs/reviews/ps45_sigmae_factor_off_registration_20261013.md` |
| **ps45 tortuosity 경로 그림** (1저자 10-13 질문) | 값에 맞춘 경로는 없다 (§4-2 행 · README 끝 절) | ⬜ 실제 전류 경로 그림 = 케이스마다 `scripts/network_current.py dump <케이스 결과 폴더>` 한 번 → 웹앱 DEM 3D "⚡ 전류 흐름" (이온 · Hertz · 전류 몫 50 %) · ⬜ 전류 가중 경로 길이 = 새 계산 → 결과 전 등록 → 시험 먼저 |
| **ps73 발표 그림** | 시간–판 속도 그래프 · ibb 묶음 영수증 (`bef5bd5d7`) · 이완 단계 3D · SE σ_VM (`33326218a`) · **같은 step 네 단계 최종 판** (`ef31da994` · 체크포인트 400,000 · 1,650,000 · 3,100,000 · 3,220,000 = 0 · 47.1 · 296.2 · 165.3 MPa · porosity = **exact union** 31.81 · 25.09 · 16.68 · 16.49 % (LHS 배포 열과 같은 양 · ε_sphere 는 기록만) · SE σ_VM 중앙 11.6 · 14.5 · 91.1 · 91.7 MPa · 스냅숏 입력 = 원 덤프 대조 · r1 로그 KE) · 1저자 고침 (`560c5efd1` · 벽 SE 안 그림 (회색 없앰) · 선형 범례 0–200 / 150 / 100 MPa · 3D 단계 이름 = porosity) · 상자그림 원값 `.csv.gz` · **AM 접촉 상대별 3D** (1저자 10-13 — 상자그림 · 중앙값 대신 · 이완 단계 · None · PC · SC · PC + SC · 선형 0–150 MPa · README §6-2) | `docs/data/ps73_compaction_curve_20261006/stages_20261012/README.md` §6 · §6-1 |
| **2차년도 덱 p14 · p15 새 막대** | p15 σLi+ Hertz · σ₀ 1.5 (0.0587–0.0893 mS/cm) · p14 수송 tortuosity Hertz (7.24–5.03 · Tabor ○ 짝판) · 생성기 다시 돌려 CSV · SVG · PNG 바이트 같음 · 덱 판독 근거 `_inspect/` (`ef31da994`) | `docs/data/ps45_r45_network_g2_20261007/deck_p14p15_20261012/NOTES.md` |
| **ps45 Hertz 값 확정 · 수송 tortuosity 분해** (1저자 10-13 *"tortuosity, 이온전도도/전자전도도 (hertz) 관련해서만 확실하게 끝내고 가자"*) | 확정 = 수송 tortuosity (Hertz) 7.24 · 5.97 · 5.45 · 5.03 · 5.29 · σ_ion (Hertz · σ₀ 1.5) 0.0587 · 0.0730 · 0.0814 · 0.0893 · 0.0838 mS/cm (0:10 → 10:0) · σ_e = (나) Hertz · 4.1 · PC 인자 켬 0.391 · 0.236 · 0.159 · 0.109 · 0.107 (Codex §6-2 각주 필수) · (가′) 인자 끔 = 0:10 0.391 만 · 나머지 = 등록 진단 뒤 · 분해 (새 계산 없음) = 저항 소산의 73–75 % 가 SE–SE 접촉 협착 · 협착 뺀 같은 망 tau2 1.25–1.79 (√ 1.12–1.34) · 모형 내부 협착비 3.9–4.2 ⇒ 5–7 길이의 "구불구불한 경로" 를 고르지 않는다 · 정직한 대안 = 실제 전류 경로 그림 (`scripts/network_current.py dump` → 웹앱 ⚡ 전류 흐름) · 전류 가중 경로 길이 (새 계산 · 등록 먼저) | `docs/data/ps45_r45_network_g2_20261007/README.md` 끝 절 |
| **ps45 σ_e 인자 끔 다섯 망 진단 결과** (1저자 10-13 비준 *"이것도 하고서 넘어갈까"* · WSL 실행) | 주 값 (가′) Hertz · 4.1 · PC 인자 끔 = 0.391 · 0.406 · 0.402 · 0.375 · 0.467 mS/cm (거의 평평 · 비단조 — 인자 켬의 3.66 배 하락 = PC 크기 인자 입력 가정) · 감도 Physics g2 · 인자 끔 0.508 · 0.539 · 0.539 · 0.504 · 0.601 · 관문 전부 통과 (대조 팔 = 저장 q 상대차 0 · SC 만 비트 같음 · PC 만 35/8 · 생산 입력 · 봉인 32 무변경) · 원 묶음 sha256 `21730156…` · report-only (194 · v1.3 · 웹앱에 안 넣음) | `docs/data/ps45_sigmae_factor_off_20261013/README.md` · 등록 §7 |

## 5. 넘어간 뒤 — 지금 상태 (날짜를 보고 읽을 것 · 10-13 새벽)

| 트랙 | 마지막 기록 | 다음 (⬜ = 1저자) |
|---|---|---|
| **세대 2 망 · 보충 20** | Codex 재검증 7 (10-12 · 핀 `3cedd40a5`) = 기존 194 발사 승인 · 사전 점검 단계 GO · 보충 검토 (핀 `b429c3c1d`) = HOLD → SUP20 수정 ✅ (claimed_fixed) · 짧은 재확인 요청서 ✅ 작성 | ⬜ 재확인 요청서 발송 (1저자 · 리뷰 핀 `a9422d2e7`) → Codex GO → ⬜ 1저자 발사 승인 → 같은 날 194 → 보충 20 → v1.3 한 번에 (`docs/reviews/lhs_release_v13_plan_20261007.md` §2b) · 그 GO 전에는 194 도 발사하지 않는다 (두 배치 같은 날) |
| **ps45 σ_e (덱 p15 σe−)** | Codex 10-13 = 권고 (가′) 조건부 → ✅ 인자 끔 다섯 망 진단 (10-13 · 1저자 비준 · WSL) = 주 값 0.391 · 0.406 · 0.402 · 0.375 · 0.467 mS/cm (§4-2 행) | ✅ 진단 · 반입 끝 → ✅ **1저자 10-13 결정 (병합 뒤 첫 기록)**: ps45 σ_e = 인자 끔 다섯 값 (0.391 · 0.406 · 0.402 · 0.375 · 0.467 mS/cm) 을 덱 · 보고에 쓴다 · 각주 = Codex §6-1 문안 + *"탄소 · 바인더 없는 AM–SE 복합체"* 한 줄 · 덱 v3_1 p15 옛 막대 (Physics · σ_AM 50 = 6.19 … 1.67) 는 1저자가 PPT 에서 이 다섯 값으로 바꾼다 · PC ↔ SC 분말 σ_e 측정 요청 = 보류 · ⬜ **나중에**: PC ↔ SC 전자전도도가 다르다는 점 — 추가 문헌 (litdb 정본 카드 · 원문 PDF + SI 확인) 을 찾아 코드에 반영 (등록 → 시험 먼저 → 웹앱 같은 묶음) · 그 전까지 지금 규약 (공통 4.1 · PC 인자 끔 = 보고 전용 · 생산 상수 · 봉인 32 그대로) · (필요하면) Codex 짧은 확인 · (필요하면) Codex 짧은 확인 · ⬜ 덱 p11 AM 고체 분율 60 % → 64.7–64.9 % · p15 각주 · 표지 (PPT 는 1저자) · ⬜ 웹앱 표지 *"σ_e^physics — Tabor plastic film"* 고침 = 봉인 `webapp/app.py` → 권고 194 · 보충 20 배치 뒤 · 4.1 mS/cm = Wang 2018 원문 확인 전 *"조건부"* 그대로 · 10-06 덱 = 역사 산출물 (고치지 않음) |
| **σ₀ · σ_e 실험 앵커** | σ₀ 1.5 = 자료 · 보고 기준 · 솔버 상수 3.0 그대로 · SBE/DBE STEP3 표 값 재실행 등록 (결과 0 건) | ⬜ 봉인 32 상수까지 바꿀 시점 (권고 = 194 · 보충 20 배치 뒤) · ⬜ kgy 정찰 (등록 문서 명령) |
| **ps73 발표 그림** | 최종 판 ✅ (`aligned_ckpt/` · 위 §4-2 · 접촉 상대별 3D 포함) | ⬜ 기공 3D = 1저자가 웹앱에서 (원자 덤프 + 판 mesh STL 업로드 → DEM 기공 보기 · README §6-1) · ⚠ 관찰 (확인 전): 판 닿기 전 (400,000) 에도 아래쪽 SE 응력이 크다 (정착 중력 하중으로 보임) · 3 · 4 단계 SE 응력 중앙이 거의 같은데 (91.1 ↔ 91.7 MPa) 판 압력은 296 → 165 MPa — 같은 침대 `DEMP-01` (압축 중 판 반력의 57.9 % = 전역 감쇠 저항) 과 같은 방향 · 정량 연결은 확인 전 |
| **덱 p13–p15** | p14 · p15 새 막대 ✅ | ⬜ p13 칸 그림 (권고 = Hertz Li⁺ 접촉 전류) · p14 coverage 규약 (권고 = Tabor 유지 + 각주) · "5:7" → "5:5" 오타 · 축 이름 "Transport tortuosity" |
| **DEM 언로딩** | 개정 2 = REG §13 ✅ (10-12 · 결과 0 건) | ⬜ 키트 (시험 먼저 · 판정문 해결 증거 그대로) + S3 함수 · σ_P · 회전 KE 기준 · 표면 관측자 fixture → §12 덧붙임 → ibb 작은 시험 → Codex (키트 증거 + 개정 2) → GO · 1저자 순서 = 이종기술 · 연구세미나 뒤 (Rint 도 같음) |
| **DEM 지배방정식 보고서** (`46cd0bdb8`) | `docs/dem_governing_equations_background_20261011.md` · 자료 `docs/data/dem_governing_equations_report_20261011/` | ⬜ Luding 2008 카드 f_min 의 k_c 인자 누락 → PDF 확인 뒤 정본 브랜치에서 고침 · 고전 출처 7 은 정본 카드 없음 → 이름 언급만 |
| **`/mixer` 침대 보기** | 10-12 1저자 화면에서 LU 두 런이 목록에 없었다 → **`git pull` 뒤 다시 나옴** (원인 = 웹앱 코드가 10-06 정책 갱신 전 판 · 정책에 없는 런은 목록이 아니라 "잠긴 런 · 루트 · 정책" 칸으로 간다 · 런처 `--no-pull` 이면 재발) · DEV 런 사본 = WSL `~/mixer_dev_view/` (LU 포함 6) · `~/mixer_dev7_runs/` (LU 없는 옛 사본) | — |
| 그 밖 1저자 결정 (10-12 인계 4) | MV 실행 · CL-94 / 95 · SELF-100 비준 · 믹서 D1–D6 · 실험 원표 회수 · E_SE 민감도 가지 · DEMP-01 가지 실험 B (ibb job 271368) | 그대로 |

## 6. 지킬 것 (CLAUDE.md 가 정본)

- **보고 → 설명 → 비준 → 실행.**  1저자에게는 게이트 · 커밋 얘기 없이 결과만.  **1저자가 따라올 수 있게** — 혼자 앞서 가지 않는다 (1저자 10-12 *"니 혼자서 하지말고"*) · 파일은 **달라고 할 때** 보낸다 (*"내가 주라고 할떄 줘"*).
- Codex 판정 반입 = 판정문 · 증거 (`source/` · `upstream/` · `submitted/` 는 manifest · sha 만) · **우리 트리 재현** · 원장 · 진행 기록을 한 묶음으로.  판정문의 "닫힘" 이 **문서 항목** 한정이면 원장을 verified 로 올리지 않는다 (`UL-*`).
- 결정표 · 창 같은 *"규칙이 완결된다"* 문장은 입력 공간 (무효 · 결손 · NaN · 다른 dt) 을 다 적었을 때만 쓴다 (`SELF-105`).
- 시험표의 *"고치기 전 전부 …"* 같은 묶음 문장은 행마다 확인한 뒤에만 쓴다 (`G2RR7-01`).
- 재검증 7 의 GO 는 **그 핀의 기존 194** 에 한정 — 보충 지원 코드를 합친 핀으로 발사하면 이 GO 를 그 diff 까지 승인한 것으로 쓰지 않는다 (보충 재확인이 그 몫).
- **요청서의 리뷰 핀은 요청서를 담은 커밋으로 고정**한다 — *"발송 때의 HEAD"* 로 두면 그 사이 커밋이 요청서의 diff 범위 문장을 거짓으로 만든다 (이 판의 SUP20 재확인 요청서 정정).
- 그림 · 보고의 porosity = **exact union** (1저자 10-12 — LHS 배포 열과 같은 양 · ε_sphere 는 기록만).
- 보고 전용 변형 (ps45 σ_e 인자 끔) 의 출력은 194 · v1.3 · 웹앱 · τ 인계에 넣지 않는다 (등록 §4 · §6).
- 커밋 · PR · 코드 주석에 모델 식별자를 넣지 않는다.

## 7. 붙여 넣을 프롬프트 (stoic-knuth 세션에)

```text
연장 세션 브랜치(claude/sdcp-dem-manuscript-si-pqwtv8)를 이 브랜치(claude/stoic-knuth-NObVQ)로 fast-forward 병합해줘.
인계 문서는 pqwtv8 쪽에만 있으니 먼저 읽어 (2판 · 10-13):
  git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8 && git show FETCH_HEAD:docs/handoff_merge_to_stoic_knuth_20261012.md
1. 아무것도 커밋하지 말고 §2 를 그대로 해: 작업 트리 깨끗 · 로컬 커밋 0 → FF_OK · LOCAL_FF_OK · DOC_OK · litdb 비어 있음 · shallow false → git merge --ff-only.
   하나라도 안 나오면 rebase · force-push · merge 커밋을 만들지 말고 멈추고 보고해.
2. §3 검사 (check_all "✓ 전부 통과" · 원장 652 · ban-sweep · 문서 참조 · 증거 바이트) → claude/stoic-knuth-NObVQ 로 푸시.
3. 그다음 인계 §5 표 순서로 이어가 — 각 줄의 ⬜ 는 나한테 먼저 묻고:
   - 세대 2 망 · 보충 20: SUP20 짧은 재확인 요청서 (docs/reviews/codex_sup20_fix_reverify_request_20261012.md) 는 내가 보낸다 · 리뷰 핀 = a9422d2e7.
     Codex GO 와 내 발사 승인 전에는 194 도 발사하지 않는다 (194 · 보충 20 같은 날 → v1.3 한 번에).
   - ps45 값은 확정: 수송 tortuosity · σ_ion (Hertz · σ₀ 1.5) = docs/data/ps45_r45_network_g2_20261007/README.md · σ_e (Hertz · 4.1 · PC 인자 끔) =
     docs/data/ps45_sigmae_factor_off_20261013/README.md (0.391 · 0.406 · 0.402 · 0.375 · 0.467 mS/cm).  덱 막대 · 각주 교체는 내가 PPT 에서 한다 — 문안만 도와줘.
   - ps45 tortuosity 경로 그림: README 끝 절 그대로 — 값에 맞춘 경로는 그리지 않는다 · 실제 전류 경로 (network_current.py dump → 웹앱 ⚡ 전류 흐름) ·
     전류 가중 경로 길이는 새 계산이라 등록 먼저.
   - 2차년도 덱 결정 (내가 정함): p13 칸 그림 (권고 = Hertz Li⁺ 접촉 전류) · p14 coverage 규약 (권고 = Tabor 유지 + 각주) · "5:7" → "5:5" · 축 이름 "Transport tortuosity" ·
     σ₀ 1.5 를 코드 상수에 넣는 시점 (권고 = 194 · 보충 20 배치 뒤).
   - SDCP σ_e 앵커: kgy 정찰 결과 (docs/reviews/sdcp_sigma_e_dcp_anchor_registration_20261012.md) 를 내가 올리면 반입.
   - DEM 언로딩 키트 · Rint 는 이종기술 · 연구세미나 뒤.
보고 → 설명 → 비준 → 실행.  게이트 · 커밋 얘기는 빼고 결과만 담백하게.  파일은 내가 달라고 할 때만.
```
