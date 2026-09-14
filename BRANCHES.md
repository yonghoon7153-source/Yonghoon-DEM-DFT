# BRANCHES.md — 이 모노레포의 브랜치 지도

작성: 2026-08-20 · 근거: `git rev-list --left-right --count` 전수 대조 (아래 재현
명령 참조). 이 문서는 **관측 결과**이지 계획이 아니다 — 브랜치가 늘거나 합쳐지면
재실행해서 갱신한다.

이 저장소는 이름만 하나의 모노레포이고 실제로는 **서로 무관한 프로젝트 5~6개가
브랜치로 병렬 존재**한다. `main` 에는 GitHub 이 만든 `Initial commit`
(`bf0dd1a3`) 하나뿐이고, 모든 실제 작업은 `claude/*` · `Codex/*` · `rescue/*`
브랜치에 있다. 그래서 "브랜치를 다 통합한다"는 조작은
**의미가 없을 뿐 아니라 위험하다** — 아래 계열들은 같은 경로 이름을 서로 다른
내용으로 쓰고 있어서 합치면 충돌만 남는다.

> **★ 정정 (2026-08-20, 21차 게이트 리뷰 발견 9) — `main` 은 고립돼 있지 않다.**
> 초판은 "`main` 이 다른 브랜치와 연결도 안 돼 있다" 고 썼다. **틀렸다.**
> `origin/main` 의 `Initial commit` 은 이 저장소 **37개 원격 브랜치 전부의
> 공통 조상**이다 (아래 재현 명령 2). 이 브랜치 기준으로
> `git rev-list --left-right --count origin/main...HEAD` 의 **왼쪽이 0** 이고
> `merge-base --is-ancestor` 는 exit 0 이다. (오른쪽 수는 적지 않는다 — 이
> 문서를 고치는 커밋이 그 수를 바꾼다. 22차 요청문을 쓰는 사이에도
> 234 → 240 으로 움직였다. 20차 발견 13-2 가 지적한 실패 형태를 이 줄이
> 그대로 반복하고 있었고, 이제
> `test_branch_map_records_no_volatile_commit_counts` 가 막는다.)
>
> **왜 틀렸나**: 초판을 쓴 작업 클론이 **shallow** 였다
> (`git rev-parse --is-shallow-repository` → `true`, 경계 `b7d61881`.
> 진단 시점에 HEAD 에서 155커밋만 보였다 — 이건 그 시점의 관측 기록이다).
> 뿌리가 경계 밖이라 `git merge-base` 가 빈 결과를 냈고, 그것을 "공통 조상이
> 없다" 로 읽었다. `git fetch --unshallow` 후 같은 명령이 리뷰어와 같은 값을
> 낸다 — merge-base `bf0dd1a3`, 왼쪽 카운트 0.
>
> **교훈**: 이 문서의 모든 그래프 주장은 **full clone 에서만** 재현된다.
> 아래 명령을 돌리기 전에 shallow 여부를 먼저 확인하라.

## 재현 명령

```bash
# 0. 먼저 shallow 가 아닌지 확인한다 — shallow 면 아래 결과가 전부 거짓말이다
git rev-parse --is-shallow-repository        # false 여야 한다
git fetch --unshallow origin                 # true 였다면 이것부터

git fetch origin
# 흡수 관계 전수 — "A → 포함: B" 는 A 의 커밋이 B 에 전부 들어 있다는 뜻
BR=$(git branch -r | grep -v HEAD | sed 's|.*origin/||' | grep -v '^main$')
for b in $BR; do into=""
  for h in $BR; do [ "$b" = "$h" ] && continue
    [ "$(git rev-list --count origin/$h..origin/$b)" = "0" ] && into="$into $h"; done
  [ -n "$into" ] && printf '%-46s → 포함:%s\n' "$b" "$into"; done

# 2. main 이 정말 모든 브랜치의 조상인가 (2026-08-20 실측: 37/37)
n=0; tot=0
for b in $BR; do tot=$((tot+1))
  git merge-base --is-ancestor origin/main origin/$b && n=$((n+1)); done
echo "origin/main 이 조상인 브랜치: $n / $tot"
```

## 계열

| 계열 | 살아 있는 tip | 무엇 |
|---|---|---|
| **배터리 열화 degeneracy** (이 브랜치) | `claude/14-gate-code-review-9qkx05` | `degradation-degeneracy/` — PyBaMM 합성 truth 로 LLI/LAM fitting degeneracy 판별 |
| **DEM/MPM** | `claude/stoic-knuth-NObVQ` · `Codex/dem-mpm-crosscheck` | LIGGGHTS/MPM 복합 양극 시뮬레이션. 두 브랜치에 `DEM_BRANCH_CONSOLIDATION.md` 가 있다 — **이미 통합이 진행된 계열** |
| **저항 네트워크 / GB 보정** | `claude/resistor-network-analysis-lKgcS` · `-solver-LDjW6` · `-UGoNB` · `-paper-bc5yi` | `dem_scripts/`, `GB_correction_*` |
| **argyrodite ML** | `claude/review-ml-migration-1BN1c` · `claude/unified-2026-05-15` · `claude/debug-api-500-error-iukkt` | `db/ kb/ tools/`, `CODE_INVENTORY.md` |
| **웹앱/기타** | `claude/dft-script-generator-webapp-GPSAG`(뿌리) · `notion-database-chatbot-PJA1x` · `market-research-presentation-bC9Yi` · `ssb-market-research-ZiEJ4` · `magical-carson-3j34s4` · `linear-regression-lecture-DaaRi` | 웹 뷰어·챗봇·발표자료·강의 |
| **타임로그/lineage** | `claude/friendly-meitner-lldvar` · `Codex/friendly-meitner-lldvar` · `rescue/lineage-2026-06-nd-pair01` | `TIMELOG.md`, `archive/ data/ db/` |

## 이 프로젝트(degradation-degeneracy)는 갈라져 있지 않다

`degradation-degeneracy/` 를 가진 브랜치는 **둘뿐**이고, 그중 하나는 다른 하나에
**완전히 흡수**돼 있다.

```
claude/zip-git-gpu-setup-vdqdtd  →  claude/14-gate-code-review-9qkx05
   고유 커밋 0개                  (merge-base = d8b6a952)
```

> **뒤처진 커밋 수는 여기 적지 않는다.** 이 문서를 고치는 커밋 자체가 그 수를
> 바꾼다 — 실제로 2026-08-20 하루 안에 88 → 89 → 90 으로 세 번 변했고, 20차
> 게이트 리뷰가 그 stale 값을 발견 13-2 로 지적했다. **불변인 사실은 "고유
> 커밋 0개"** 뿐이고, 그것이 통합 판단에 필요한 전부다. 나머지는 위 재현
> 명령으로 그 자리에서 세라.

즉 **통합할 것이 없다.** 옛 브랜치는 조상이고, 지금 브랜치가 그 전부를 담고 있다.
2026-08-20 이전에는 저장소 문서 8곳이 여전히 옛 이름을 작업 브랜치로 지목하고
있었다 — 그건 분기가 아니라 **문서 drift** 였고, 브랜치 이름의 정본을 루트
`CLAUDE.md` 하드룰 1 하나로 모으고 `wiki/tools/lint.py` 의
`no-hardcoded-branch-name` 검사로 재발을 막았다.

## 완전히 흡수된 브랜치 (고유 커밋 0개)

아래는 tip 이 아니라 **다른 브랜치 안에 통째로 들어 있는** 브랜치다. 지우면
잃는 커밋이 없다. 다만 원격 브랜치 삭제는 되돌리기 어려우므로 **사람 승인 없이
지우지 않는다** — 이 목록은 판단 재료다.

| 흡수된 브랜치 | 들어 있는 곳 |
|---|---|
| `claude/zip-git-gpu-setup-vdqdtd` | `claude/14-gate-code-review-9qkx05` |
| `claude/argyrodite-ml-prediction-ozuoX` | `claude/argyrodite-ml-migration-kDtHW`, `claude/review-ml-migration-1BN1c` |
| `claude/argyrodite-ml-migration-kDtHW` | `claude/review-ml-migration-1BN1c` |
| `claude/review-ml-migration-W29af` | `claude/debug-api-500-error-iukkt`, `claude/unified-2026-05-15` |
| `claude/debug-api-500-error-u8KI7` | `claude/debug-api-500-error-iukkt` |
| `claude/debug-fracture-solver-DQE6G` | `Codex/dem-mpm-crosscheck`, `claude/stoic-knuth-NObVQ` |
| `claude/debug-fracture-solver-LqBv3` | 위 + `claude/debug-fracture-solver-DQE6G` |
| `claude/stagewise-fracture-solver-3VvPg` | 위 전부 |
| `claude/optimize-dem-analysis-Nap1m` | `claude/add-bulk-operations-KddvJ`, `claude/organize-network-metrics-KEivv` 등 |
| `claude/organize-network-metrics-KEivv` | `claude/reconnect-dem-website-ubGVZ`, `claude/resistor-network-analysis-lKgcS` |
| `claude/reconnect-dem-website-ubGVZ` | `claude/resistor-network-analysis-lKgcS` |
| `claude/dft-script-generator-webapp-GPSAG` | 다수 (가장 오래된 공통 조상 — 남겨 두는 편이 낫다) |

**상호 포함(= 내용 동일)**: `claude/configure-spawn-halogen-lithium-TjDCB` ↔
`rescue/lineage-2026-06-nd-pair01` — 서로를 완전히 포함한다. 같은 이력의 이름만
다른 사본이다.

## 진짜로 갈라져 있는 곳 (합치려면 사람 판단이 필요)

흡수 관계가 없어 **양쪽에 고유 커밋이 있는** 짝이다. 자동으로 합칠 수 없다.

| 짝 | 고유 커밋 |
|---|---|
| `Codex/friendly-meitner-lldvar` ↔ `claude/friendly-meitner-lldvar` | 같은 이름인데 갈라졌다 |
| `Codex/dem-mpm-crosscheck` ↔ `claude/stoic-knuth-NObVQ` | 위와 같은 모양 |
| `claude/resistor-network-analysis-lKgcS` ↔ `-solver-LDjW6` | 저항 네트워크 계열의 실제 분기 |

(고유 커밋 수는 적지 않는다 — 위 재현 명령으로 그 자리에서 센다.)

이 셋은 **이 브랜치의 소관이 아니다** (루트 `CLAUDE.md` 저장소 지도: DEM/MPM 계열은
다른 브랜치 소유). 여기서 합치지 않는다. **Codex 계열은 독립 유지 대상이며 통합
대상이 아니다** — Codex 가 그 브랜치를 근거로 판단한다. 합칠 사람이 볼 수 있게
적어만 둔다.

## 규칙

1. 이 브랜치에서는 `degradation-degeneracy/` · `wiki/` · `.claude/` · 루트 문서만
   건드린다. `kit_*` `ps_zips` `run_mpm.sh` 등 DEM/MPM 트리는 다른 브랜치 소유다.
2. 다른 계열 브랜치를 이 브랜치로 merge 하지 않는다. 같은 경로를 다른 내용으로
   쓰고 있어 충돌만 남고, 연구 파이프라인의 `source_digest` 가 오염된다.
3. 원격 브랜치 삭제는 **사람 승인 후에만**. 위 흡수 목록은 근거이지 실행 지시가
   아니다.

## 2026-09-10 — `claude/bms-alpha-beta-verify` 분기

`claude/14-gate-code-review-9qkx05` 의 `56a35a88` 에서 갈랐다. **경로를 겹치지
않게 나눈 것**이 전부다:

| 브랜치 | 소유 경로 |
|---|---|
| `claude/14-gate-code-review-9qkx05` | `degradation-degeneracy/` · `webapp/` · `wiki/` · 루트 문서 |
| `claude/bms-alpha-beta-verify` | **`bms-balancing/` 만** |

이유: α·β 검증(규진팀 MATLAB 포팅·축퇴 측정)은 게이트 리뷰 루프와 **일정도
자원도 다르다.** 같은 브랜치에서 둘을 돌리면 게이트의 증거 사슬(`source_digest`
· 영수증 · 전수 재생)이 무관한 커밋으로 흔들린다. `bms-balancing/` 은 RUN_SCOPE
밖이므로 갈라도 `source_digest` 는 안 움직인다 — 그것이 이 분기가 안전한 이유다.

합치는 방향은 **본체가 서브를 merge** 하는 쪽 하나다. 반대로 하면 게이트
브랜치의 이력이 서브로 흘러가 판정 대상 커밋을 흐린다.

### 2026-09-14 — 본체가 서브를 merge 했다 (`cf9bad4`)

방향은 규칙대로 본체 ← 서브. merge-base `fdd3929`. 겹친 파일 0. 서브가
경계를 넘긴 `webapp/` 6 파일은 사용자 지시에 따른 것이라 그대로 받았고, 그
예외는 `CLAUDE.md` 하드룰 1 에 **한 줄**로 적었다 (예외도 한 곳에만). 확인
절차와 실측은 merge 커밋 메시지와 `bms-balancing/MERGE_BRIEF_FOR_GATE.md`.
서브 브랜치는 그대로 살아 있고 소유 경로도 그대로다 — merge 는 흡수가 아니라
동기화다.

### 2026-09-14 — merge 뒤 인수인계 전수 확인 (본체가 직접 돌렸다)

`bms-balancing/MERGE_BRIEF_FOR_GATE.md` 는 본체에 **검증 넷(§5)** 과
**판단 여섯(§6)** 을 남겼다. 요약을 믿지 말라는 것이 그 문서의 요구라 전부
이 컨테이너에서 실제로 돌렸다.

| 항목 | 결과 |
|---|---|
| §5-1 하네스 테스트 | `310 passed · 1 failed` (538.87s). 실패는 **내 간섭**이다 — `test_d9_08` 이 시작 시점 HEAD 를 `--expected-head` 로 고정해 격리 스냅샷에서 도구를 돌리는데, 실행 도중 내가 위키를 커밋해 HEAD 가 움직였다. HEAD 를 고정하고 그 시험만 다시 돌려 **1 passed** 로 확인했다. 즉 `WORKING_STATE.md` 의 "311 passed 기대" 핀은 지켜진다. **교훈: 이 하네스가 도는 동안 커밋하지 않는다** |
| §5-2 하네스 계약 `check_u14 --schema-only` | rc 0 · `blocked_by` 의 schema·content·unit·controls·numbers·alias **전부 0** · 남은 것은 `baseline_absent 1` (대조가 없으니 정상) |
| §5-3 보존 묶음 bytes | 여덟 묶음 **불일치 0** — merge 가 줄끝을 정규화하지 않았다. 서브가 적어 둔 수치와 일치 (162·140·90·186·114·112·103·136) |
| §5-4 webapp 화면 | 라우트 21 개 전부 200. `/alphabeta` 에 "쉬운 말로" 칸 9 개 + 용어 절, `plain.css` 200 (2615 bytes), 쓰인 `pl*` 클래스가 전부 CSS 에 있다. **서브가 못 한 검증을 닫았다** |
| §6-1 `webapp/` 수용 | 받았다. 예외는 `CLAUDE.md` 하드룰 1 에 한 줄 |
| §6-2 `pipeline.html` 라운드 수 | 하드코딩을 없애고 **원장에서 세는** 자리로 바꿨다 (렌더 실측: 62) |
| §6-3 루트 `.gitignore` 의 `cells/` | 들어갔다 (`.gitignore:58`) |
| §6-4 62차 게이트 준비 | 요청문 `degradation-degeneracy/docs/22p_gap/GATE62_REQUEST.md` §4 에 pyDMA 외부 검증을 경고와 함께 실었다. 순서 전체 e2e 는 smoke 7b·8b, `/self-review` 는 §3 |
| §6-5 `wiki/` 후보 3건 | **채택하고 반영했다** (2026-09-14). 새 개념 페이지 `near-optimal-set-width-measurement`, Schmitt 페이지에 12 mV 문턱 폭, 계보 페이지에 chain rule 결함. 원문은 `wiki/raw/transcripts/2026-09-14-bms-handoff-width-and-wiki-candidates.md` 에 봉인 |
| §6-6 축퇴 폭 측정법을 본체에 쓸지 | **아직 정하지 않았다.** `degradation-degeneracy/src/` 에 이 계열 도구가 없음을 확인했다 (가장 가까운 `hessian.py` 는 스스로 "결론 근거 아님" 으로 강등돼 있다). 판단 근거는 위키 페이지에 정리했고 옮기려면 `src/` 를 건드리므로 **RUN_SCOPE 안** — 게이트 라운드 중에는 시작하지 않는다 |

덤으로, 인수인계 §3-3 이 본체에 물어보라고 한 것 하나를 닫았다: 규진팀
MATLAB 의 chain rule 결함(dV/dQ 에 `1/α` 누락)이 **본체에는 없다.**
`src/objective.py` · `src/curves.py` 가 합성된 곡선을 수치미분하므로 `1/α` 가
자동으로 들어간다 (α=0.80 대조 실측: `1/α` 포함본과 6.4e-06, 누락본과 7.9e-01).
