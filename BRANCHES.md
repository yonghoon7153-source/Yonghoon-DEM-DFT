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
> `git rev-list --left-right --count origin/main...HEAD` 는 `0 234` 이고
> `merge-base --is-ancestor` 는 exit 0 이다.
>
> **왜 틀렸나**: 초판을 쓴 작업 클론이 **shallow** 였다
> (`git rev-parse --is-shallow-repository` → `true`, 경계 `b7d61881`,
> HEAD 에서 155커밋만 보였다). 뿌리가 경계 밖이라 `git merge-base` 가 빈
> 결과를 냈고, 그것을 "공통 조상이 없다" 로 읽었다. `git fetch --unshallow`
> 후 같은 명령이 리뷰어와 같은 값을 낸다 (235커밋, merge-base `bf0dd1a3`).
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
