# 인계 — 본 세션 `claude/stoic-knuth-NObVQ` → 서브 세션 (tortuosity 결정 16 · 문헌 10 편) · 복귀 = fast-forward 병합

> 2026-10-03 새벽 (KST).  1저자 *"토큰을 다 써서 서브 대시보드로 · 16 건 비준건이랑 논문 관련 잘 인계 · 예전처럼 머지했을 때 충돌 없이"*.
> 선례 = `docs/handoff_merge_to_stoic_knuth_20260929.md` (연장 세션 → 본 세션 fast-forward).  ⚠ 날짜를 보고 읽을 것.

## 0. 한 줄
tortuosity 정의는 문헌으로 닫혔고 (판단 메모 v2 + 적대 리뷰 3), **명명 규약은 비준되어 CLAUDE.md 에 들어갔다**.  남은 것은 ① **결정 16 = 1저자 보류** ② **추가 문헌 10 편 = 1저자 업로드 대기** — 둘 다 서브 세션에서 한다.  본 세션은 이 인계 커밋 뒤 **stoic-knuth 에 커밋하지 않는다** (fast-forward 복귀를 위해).

## 1. 브랜치 기하
| 브랜치 | 끝 | 비고 |
|---|---|---|
| `claude/stoic-knuth-NObVQ` | **이 문서를 담은 커밋** (`git log -1 --format=%H origin/claude/stoic-knuth-NObVQ` 로 확인 — 인계 메시지에 SHA 를 적어 둔다) | 본 세션은 이후 커밋 금지 |
| `claude/friendly-meitner-lldvar` (litdb 정본) | `a626f72ef` 이후 | 카드는 **여기에만** (CLAUDE.md litdb 규칙) · 다른 세션도 쓸 수 있으니 push 전 fetch · rebase |

## 2. 서브 세션 시작 절차
```bash
git fetch origin claude/stoic-knuth-NObVQ
git log -1 --format='%H %s' FETCH_HEAD            # = 인계 메시지의 SHA 인지 확인
git checkout -B <서브 세션 지정 브랜치> FETCH_HEAD   # 지정 브랜치가 이미 다른 커밋을 갖고 있으면 멈추고 보고
git status --short                                 # 깨끗해야 함
```

## 3. 할 일 A — 결정 16 (판단 메모 v2 §0 · 1저자 보류 *"잠시만"*)
비준 전에는 **아무것도 구현하지 않는다**.  비준 뒤 = 시험 먼저 → 고침 → 웹앱 같은 묶음 (J20-l) → 게이트 → 커밋.

| # | 결정 | 권고 |
|---|---|---|
| 1 | f 를 계산할 두께 | 질량 보존 두께로 재척도한 f_mc (표지 "재척도 · 해 아님") · 해 그대로 f_gap 은 메타 열 |
| 2 | 관통 안 하는 침대 | f = 0 + `NOT_PERCOLATING` (판정 = `percolating_fraction == 0` · `sigma_full_status` 로 판정 금지) · tau2 · tau 빈칸 |
| 3 | Hertz · physics 두 모드 | 둘 다 · **"1세대"** 표지 (Hertz = 반무한 Holm a/r 0.30–0.44 에서 R_c 1.7–2.4× 과대 · physics = ψ 분모 배치) · 실험 절대 대조 보류 |
| 4 | 절대 비교 관문 | **순수 SE 망 런 1 회** 먼저 · tau2 원값 + 순수 SE 기준 정규화값 둘 다 |
| 5 | √ 값의 COMSOL 표기 | 지금 제거 · 이미 전달한 배포 v1 · v1.1 = **정오표** (값 불변) · v1.2 에서 문구 교체 · tau2 의 "COMSOL 입력" 표지는 GUI Equation 캡처 뒤 |
| 6 | 등급 · COMSOL 2D 의 τ | 모드를 명시하는 도우미 하나로 통일 · Stage-E 값에서 "τ" 이름 빼기 · 등급 문턱 = "내부 등급선" (Tippens 2019 미확인) |
| 7 | 프레임 [1] "pure-SE ≈10 % @ 300 MPa (Minnmann)" | 원장 **CL-94** (출처 미확인 · 순환 앵커 가능성) — Minnmann 2021 본문 · SI 에 없음 (리뷰가 원문 확인) · MPM σ_y 0.30 = "외부 앵커 없음" |
| 8 | `single.html` "1.4 % 일치 · 무매개 검증" | 대체 숫자 없이 철회 |
| 9 | LHS-25 | 진단 **전에** 접촉별 추정기 둘 사전등록 (부피 보존 c²·A_overlap · F_DEM/H) · 현행 F_real/H = 상한 표지 · 합 상한 = **안 B (라게르 면)** · 안 A = 강체 AM 레일만 · β_SE 철회 · C1 진단 전용 · C2 추세 회복 = 보고 전용 |
| 10 | LHS-26 | 모양 인자 = 설계 `block` · rough coverage 인계 제외 유지 |
| 11 | CF 가지 | "모형 내부 기준선" · FULL/CF = "모형 내부 협착비" (tau2 로 1.2–1.4× 과대) · 복셀 ÷ 망 대조에 이 편향 사전등록 |
| 12 | σ_e Stage 22.5 | 비관통 6 침대가 필터를 통과 → 계수 동결 · 재적합은 TAU-06 뒤 별도 등록 |
| 13 | τ_e | ML 기술자 진술로만 · P2D 입력 열 보류 · FULL 장에서 flux dead-end 먼저 (위상 p90 2.86 %) |
| 14 | 전자 · 열 tau2 | σ₀ · k₀ 관례 먼저 (이온 다음) |
| 15 | 키 이름 | `f_ion_` / `tau2_ion_` / `tau_ion_<mode>` + 메타 열 (v2 §5-1) |
| 16 | S3 봉인 모듈 | 도우미는 봉인 모듈 밖 · 봉인 모듈 (`network_conductivity.py` · `plastic_coverage.py`) 문구 수정은 다음 재봉인 때 묶음 (09-17 봉인은 이미 낡음) |

P1 결함 (v2 §4): TAU-01 (√ 값 COMSOL/EIS 표기 · 커밋 TSV 6 · 배포 v1/v1.1 포함) · TAU-02 (single.html 검증 주장) · TAU-03 (τ_Laplace,eff 변형 ≥5) · TAU-10 (10 % 앵커) · TAU-13 (1세대 협착식) · 리뷰가 더한 TAU-21~25.

## 4. 할 일 B — 추가 문헌 10 편 (v2 §8 · 1저자가 서브 세션에서 PDF 업로드)
| # | 서지 (참고문헌 목록 그대로) | 닫는 것 |
|---|---|---|
| 1 | H. F. Fischmeister, E. Arzt and L. R. Olsson, Powder Metall. 21, 179 (1978) | LHS-25 접촉 면적 실측 (접근 불가한 Fischmeister & Arzt 1983 대체) |
| 2 | L. Holzer et al., J. Mater. Sci. 48, 2934 (2013) | 협착 (constrictivity) 정량 틀 — FULL/CF/geo 분해 |
| 3 | L. Froboese et al., J. Electrochem. Soc. 166, A318 (2019) | 입경비 효과 · Park σ₀ (Table S1) 출처 후보 |
| 4 | J. Landesfeind, M. Ebner, A. Eldiven, V. Wood, H. A. Gasteiger, J. Electrochem. Soc. 165, A469 (2018) | 임피던스 τ ↔ 단층촬영 τ 직접 대조 |
| 5 | J. Park et al., Energy Storage Mater. 19, 124 (2019) / Chem. Eng. J. 391, 123528 (2020) | Park 2020 τ 의 계산법 (SI Fig S9 인용) |
| 6 | D. Hlushkou et al., J. Power Sources 396, 363 (2018) | 전고체 tortuosity |
| 7 | Z. Siroma et al., Electrochim. Acta 160, 313 (2015) | Minnmann TLM 식 (Eq 1) 원전 |
| 8 | N. Kaiser et al., J. Power Sources 396, 175 (2018) | 임피던스에서 τ 추출 |
| 9 | M. Ender et al., Electrochem. Commun. 13, 166 (2011) | Laplace N_M (Landesfeind [35]) |
| 10 | F. Pouraghajan et al., J. Electrochem. Soc. 165, 2644 (2018) | 두 τ 측정법 비교 · 접촉저항 넣은 TLM |

절차: PDF → `litdb-curator` 에이전트 (논문마다 하나) → 정본 브랜치 worktree 에 카드만 · 그림은 `tools/litdb/extract_figures.py --clean --slug … --pdf …` 를 메인이 순서대로 (공유 `_sources.json` 동시 쓰기 금지) · `build_index.py` + `--check` · `comparison_vs_ours_DEM.md` J 절 갱신 · 한 커밋 · push.  ⚠ 중복 확인은 INDEX 가 아니라 `git ls-tree FETCH_HEAD litdb/papers/` + DOI `git grep`.  카드 끝 `</content></invoke>` 잔해 확인.

## 5. 지킬 것 (CLAUDE.md 가 정본 · 이번 묶음 교훈만)
- 보고 → 설명 → 비준 → 실행 · 시험 먼저 · 커밋은 `G=scripts/check_all; bash "$G.sh"` 가 "✓ 전부 통과" 일 때만 · 게이트 도는 중 리포 수정 금지 · 명시 경로 커밋 · PR 없음 · 커밋 끝 두 줄 (Co-Authored-By / Claude-Session) · 모델 ID 금지.
- **τ 명명 규약 (CLAUDE.md ★★ 블록)** 을 따른다 — "tortuosity factor" = tau2 에만.
- 규율 ⑥: 서지 · 수치는 원문 (SI 포함) 에서 · 리뷰가 COMSOL 쪽 번호를 0-기준으로 잘못 옮긴 것을 잡았다 → **인쇄 쪽 번호**로 쓴다.
- 문서에 scratchpad 경로를 남기면 `check_doc_refs` 가 막는다 → 리포 경로로 바꾸거나 `docs/reviews/doc_refs_allowlist.tsv` 에 종류 (generated · external · absent · cross_branch) 와 함께 등재.
- ⚠ 불안정 시험: `dem_scripts/mixer_20260921/test_launcher.sh` 가 게이트 안에서 한 번 127/1 FAIL (단독 재실행 128/0 · 실패 경우 이름 미표시) — 다시 나오면 경우 이름을 잡아 원장 등재.
- 보안: 호스트 주소 · 포트는 리포에 쓰지 않는다 (채팅에서만).

## 6. 다른 트랙 — 본 세션에서 넘어가는 열린 일 (서브 세션은 1저자가 요청할 때만)
| 트랙 | 상태 | 자리 |
|---|---|---|
| FAM §12-6 (kgy) | 봉인 `1afd37a9a` · 건식 통과 · **발사 = 1저자** (발사 · watch 명령 = 아래 §6-1) · 결과 오면 12-4 분류 먼저 | prereg §12-6 · 12-6-1 |
| FAM §12-7 (gabia) | 미등록 · 딴 시뮬 끝난 뒤 · kgy 다음 | CLAUDE.md FAM 행 |
| ① 계면 저항 r_int | 구현 `5e0efdb8d` · 자기리뷰 결함 P1-1 · P2-1~4 · P3 (반례 먼저 수정 대기) · 파이프라인 초안 (결정 R1–R9) **미보고** | `docs/reviews/rint_selfreview_summary_20261002.md` · `docs/reviews/contact_resistance_pipeline_draft_20261002.md` |
| 믹서 점착 브리핑 | 초안 **미보고** (LC×10 DEV 팔 권고 등) | `docs/reviews/mixer_cohesion_briefing_draft_20261002.md` |
| LHS 접촉 네트워크 | D1–D4 비준 (D1 = f / tau2 / tau) · LHS-25/26 닫은 뒤 LHS 130 + 64 · ps45 재계산 | 진행 파일 10-03 · v2 §5 · §6 |
| litdb 크롭 후속 | minnmann SI Table S3 · 두 번째 S5 누락 · tab_S4 잘림 · nguyen Fig 5 없음 · arzt 캡션 OCR 6 | 정본 figures/ |

### 6-1. FAM §12-6 발사 · watch (kgy · 주소 없음)
```bash
cd ~/fam_seal_7f44d6534
md5sum run_r4.sh | cut -c1-8                  # 8d9e9f95
nohup bash run_r4.sh >> batch_r4.log 2>&1 &
cat batch_r4.log                              # "§12-6 시작 · <시각>" = 발사 시각 → 12-6-1
watch -n 60 bash ~/fam_watch_r4.sh            # 도는 팔 = 마지막 프레임 줄 · 끝난 팔 = 상태 줄만 (SELF-80) · md5 72a343bc
```
(`~/fam_watch_r4.sh` 내용은 10-03 대화에서 전달 — 없으면 같은 규칙으로 다시 만든다: batch_r4.log 에 그 팔의 rc 줄이 있으면 상태 줄만, 없으면 마지막 `^  frame ` 줄.)

## 7. 복귀 병합 (서브 세션 작업이 끝나면 · fast-forward 만)
```bash
git fetch origin claude/stoic-knuth-NObVQ
git merge-base --is-ancestor FETCH_HEAD HEAD && echo "FF 가능" || echo "⛔ stoic-knuth 가 움직였다 — 멈추고 보고 (merge 커밋 만들지 말 것)"
G=scripts/check_all; bash "$G.sh"             # ✓ 전부 통과 확인
git push origin HEAD:claude/stoic-knuth-NObVQ  # fast-forward push
```
병합 뒤 검사: `git log --oneline FETCH_HEAD..HEAD` 커밋 목록 · CLAUDE.md τ 블록 · 진행 파일 · 원장 (`check_review_findings.py`) 자기일관.
