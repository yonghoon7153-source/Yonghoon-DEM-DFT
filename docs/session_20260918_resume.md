# 복귀 프롬프트 — 2026-09-18 (압축 대비)

브랜치 `claude/stoic-knuth-NObVQ` · 마지막 커밋 `e3a8ea0b0` · 게이트 두 레인 rc=0.

⚠ **구속 조건** (압축돼도 살려야 한다)
- 작업 브랜치는 `claude/stoic-knuth-NObVQ` **뿐**.  다른 브랜치 push 는 사용자 명시 허락 먼저.
  ⛔ **`friendly` 는 건드리지 않는다** (WSL 작업본이 그 브랜치에 있다).
- litdb 정본은 `origin/claude/friendly-meitner-lldvar` 의 `litdb/` — **읽기만**.
  중복 확인은 INDEX 가 아니라 `git ls-tree FETCH_HEAD litdb/papers/ --name-only`.
- 커밋·PR·코드 주석에 **모델 식별자 금지**.
- `bash scripts/check_all.sh` 는 **절대 파이프하지 않는다** (파이프가 종료코드를 삼킨다).
  커밋 전 `--selftest` **와** 무인자 **둘 다** 돈다.
- 09-17 23:59 KST 봉인 마감은 저자가 계약을 고치기 전엔 안 움직인다.
  특히 **"결과가 아쉬워서 앞당기지 말 것."**
- 부분 삽입으로 끝난 LIGGGHTS 런은 통째로 폐기.
- **1.2 배출 하한은 근거 있는 하한이지 충분조건이 아니다** — 그 한정어를 지우지 말 것.
- 에이전트 스윕은 medium/low (max 아님).
- 사용자 운영 규칙: **보고 → 설명 → 비준 → 실행**.

---

## 1. 지금 당장 할 일 (사용자 기계)

### (가) LHS 본번 수확 — `LHS-02` 를 닫는다.  **9월 말 납품의 파라미터 경향 축 입력**
```bash
mkdir -p /tmp/lhsh/scripts
cd ~/Yonghoon-DEM-DFT && git fetch origin claude/stoic-knuth-NObVQ
for f in lhs_harvest_batch lhs_descriptor_harvest lhs_perc_extract; do
    git show origin/claude/stoic-knuth-NObVQ:scripts/$f.py > /tmp/lhsh/scripts/$f.py
done
cd /tmp/lhsh
nohup python3 scripts/lhs_harvest_batch.py --verify-sha \
    --cohort /tmp/lhsh/cohort.tsv --out-dir /tmp/lhsh/out > /tmp/lhsh/harvest.log 2>&1 &
```
· 리허설은 이미 **127/127 rc=0** 으로 통과했다 (mesh 583 개 = 38 + 545 전송 완료).
· ⚠ **리포 밖에서 돌리면 안 된다** — `ROOT = parent.parent` 라 수확기를 못 찾는다.
  그래서 `/tmp/lhsh/scripts/` 구조가 필요하다 (`require_harvest` 가드가 이제 dry-run 에서도 선다).
· 끝나면 `/tmp/lhsh/out/*.json` (127) + `_batch_summary.json` 을 tar 로 보내 줄 것.

### (나) 코호트 증보 2건 — `lhs00_034` · `lhs00_089`
봉인(2026-09-14) 당시 없던 contact 덤프가 **ibb 에 생겼다**.  실측 확인됨:

| 케이스 | atom 끝 | contact 끝 | mesh 끝 | 짝 |
|---|---|---|---|---|
| `lhs00_034` | 3,560,000 | 3,560,000 | 3,560,000 | 차 **0** · mesh `exact` |
| `lhs00_089` | 2,855,000 | 2,850,000 | 2,855,000 | 차 **5,000** (`SELF-30` 정상) · mesh `exact` |

⛔ **`ls | tail` 로 보지 말 것 — 사전순이다.**  `995000` 이 `3560000` 보다 크게 나와서
  내가 실제로 **거짓 경보**를 냈다.  `sed 's/.*_//' | sort -n | tail -1` 로 볼 것.
⇒ 절차: ibb 에서 마지막 atom·contact·mesh 만 tar → WSL 전송 → **양쪽 sha256 대조** →
  그 지문으로 `docs/data/area_s2_cohort.tsv` 에 `# 증보 2026-09-18` 행 2 개 추가 →
  게이트 통과 → `--case lhs00_034 --case lhs00_089` 로 2 건만 추가 수확.
⚠ `lhs00_098` 은 `r5` 로 도는 중이라 **제외**.  (10 코어 추가 완료, CPU 60/60)

---

## 2. 원장 상태 (`docs/reviews/findings.json`)

**오늘 닫은 것 (claimed_fixed)** — GAP3-19 · 20 · 35 · 36 · 37 · 38 · 39 · FIG · 15
**오늘 연 것 (open)** — **GAP3-40** (P1)
**남은 open** — GAP3-17 · 18 · 21 · 22 · 30 · 32 · 34 · DOC(㉟ 는 아카이브로 처리) ·
  LHS-02(수확 대기) · 03 · 04 · 05 · 06

### ★ 다음 1순위 = `GAP3-40`
`scripts/analyze_contacts.py:471,474,490` 의 `85` / `95` / `3.5` 가 **전거 0 건**인데
사용자에게 `critical` 을 띄운다.  ⚠ 아카이브한 스킬(`2.4`/`70`)과 **정면 충돌**하고
**양쪽 다 무출처**라 *"생산에 맞추면 된다"* 가 자동 정답이 아니다.
길 셋: ⓐ 문헌 전거(규약부터 정할 것) ⓑ `critical` → `info` + 무전거 명기 ⓒ 코퍼스 경험 문턱.
**코드는 안 건드렸다.**

---

## 3. 오늘 배운 것 — 압축해도 남겨야 할 한 줄

**같은 부류의 false-green 을 다섯 번 만났다**: 수확 dry-run 이 없는 경로로 초록 ·
porosity 2×2 분리성이 재결합에 눈이 멂 · 색상막대 검사기가 5 블록 중 **0 개** 검사 ·
`plot_tau_regime_si` 가 입력 없이 rc=0 · `plot_porosity_v4_journal` 이 빈 CSV 로 진행.

⚠⚠ **그것을 재던 내 돌연변이 시험 자체도** 같은 함정에 빠졌다 — 파일이 안 바뀐 것을
*"검사기가 못 잡았다"* 로 오독해 **없는 구멍을 보고할 뻔했다**.  sha256 단언으로 잡았다.
★ 교훈: 시험이 빨간불을 못 냈을 때 **"검사기가 못 잡았다" 와 "시험이 안 돌았다" 를 구분**하라.

### 내가 오늘 철회한 판정 3 건 (같은 실수를 반복하지 말 것)
1. `τ² = φ^(2−2α)` — **내가 지어낸 규약**.  그려진 −1.0 을 맞다고 전제하고 거꾸로 맞췄다.
   리포 규약은 코드에 있었다: `τ² = φ·σ₀/σ_eff` × `σ_eff/σ₀ = φ^1.5` ⇒ **τ² = φ^(1−α)**, α=1.5 → **−0.5**.
2. *"`compare_hertzian_vs_physics.py` 는 실행조차 안 된다"* → 실제는 `.gitignore:5-7` 로
   케이스 폴더가 리포에 안 딸려오는 것이 **전제**였다.  **"안 돈다" 와 "돌 데이터가 없다" 는 다르다.**
3. *"CI 의 `--ban-sweep` 약속은 거짓"* → **이름만** 거짓.  같은 전수 스윕이
   `--selftest` 21 번 검사로 이미 돌고 있었다.

⇒ **구멍을 찾다 보면 없는 구멍도 보인다.**  원장 note 를 그대로 믿지 말고 매번 기계적으로 재확인.

---

## 4. 게이트가 할 수 있는 것 / 없는 것 (사용자 질문에 답한 정리)

| 게이트가 하는 것 | 게이트가 **못 하는 것** |
|---|---|
| 철회값이 문서·슬라이드에 다시 안 적히게 | **문헌 앵커를 만들어 주기** |
| 검사가 조용히 초록 내는 걸 차단 | 무출처 문턱에 **전거 붙이기** |
| 숫자를 손으로 적는 걸 차단 (세거나 계산하게) | 어느 문턱이 **옳은지 판정** |

`GAP3-40` 이 정확히 그 경계다.

---

## 5. 정본 포인터
- 수리 기록 전문: `docs/reviews/gap_audit_r3_repair_20260917.md` (345 줄)
- 감사 판정 원문: `docs/reviews/gap_audit_r3_verdicts_20260917.md`
- 아카이브 사유: `docs/archive/skills_20260424/README.md`
- 봉인 코호트: `docs/data/area_s2_cohort.tsv` (131 행 = RAW_OK 127 + 결손 3 + 비케이스 1)
