# 23차 게이트 리뷰 요청 — 22차 발견 1·5·6·7·8 대응 + 계약 v2 재심사

```
브랜치   origin/claude/14-gate-code-review-9qkx05
대상 커밋 a037eba4ef2e65205522380b123455c5de1dcda3
직전 대상 db19a7b1cc22c96e9c3f35f1a72b858554be1232  (22차, NO-GO)
source_digest  a72c0f3a485c19bb   ← 21·22차와 동일
```

## 0. 이 라운드가 요구하는 판정

리뷰가 정한 순서 11번(**문서·회귀 재심사**)이다. 12번(RUN_SCOPE 변경)은 아직
시작하지 않았다.

| 대상 | 요청 |
|---|---|
| 22차 발견 1·5·6·7·8 | 닫혔는가 |
| `STAGE3_CONTRACT.md` **v2** | 구현 착수 가능한가 |
| 12시간 재실행 | **승인 요청하지 않는다** — 22차 판정대로 추정을 폐기했고, 고유 leg 목록을 만든 뒤 다시 산정한다 |

계약 v2 의 §2·§4·§6 은 **정의만 있고 구현이 없다**. 그것이 발견 2·3·4 의
현재 상태다 (§7).

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
a037eba4ef2e65205522380b123455c5de1dcda3
$ git status --short
(빈 출력)

$ python -m pytest tests/ -q
685 passed in 238.96s

$ ./scripts/smoke_e2e.sh
✅ end-to-end smoke 통과 — 본 실행을 시작해도 된다

$ python -c "…from src.io import source_digest;print(source_digest())"
a72c0f3a485c19bb

$ python3 wiki/tools/lint.py
RESULT: 0 errors

$ git diff --name-only f57ecd4d..HEAD -- src tools configs scripts run.sh 'requirements*'
(빈 출력)
```

22차가 "이 세션에서 다시 돌리지 못했다" 고 기록한 pytest·smoke 는 대상 커밋에서
재실행했다.

## 2. 커밋 5개

| SHA | 무엇 |
|---|---|
| `7e0d7d38` | 발견 1·5·6·7·8 대응 + 계약 v2 |
| `bf2549e6` | 투영 요약 줄이 가장 엄격한 판정을 보이게 (자체 발견) |
| `73b77156` | 투영 스키마 2 — 8다리 재생성 (원자료 보유 기계) |
| `2a217cee` | provenance 를 계산 경로에 묶는다 (자체 발견) + §31 |
| `a037eba4` | `compute_sha256` 통일 — 8다리 재생성 |

## 3. 발견별 대응

| 발견 | 대응 | 회귀 |
|---|---|---|
| **1** union 오분류 | 계약 §0 에 철회[WARM_UNION]. §3 이 후보 정책을 3종으로 명명 (`legacy_slot_replace` / `equal_start_count_base_retained` / `union`). 21차 실험 = 첫 번째. `equal-cost` → **`equal_start_count`** 로 개명하고 `n_eval`·wall time 별도 기록 | `test_warm_replaces_the_deterministic_slot_it_does_not_add_one` — 문장이 아니라 **restart 투영의 실제 후보 배열** |
| **5** 투영 provenance | 스키마 2 — 실제 fits 바이트 SHA **삼중 대조** · 봉인 summary **전체** 재귀 비교 · `<leg>.restarts.csv.gz` (per-restart `i·source·J·p0..p3·warm`) · `analyzer` 블록 · malformed 즉시 실패 | `test_random_only_multimodality_is_recomputable_from_the_restart_projection` |
| **6** gzip 바이트 주장 | 정본 앵커를 **압축 전 canonical TSV SHA** 로 한정. 교차 runtime 동일성 주장 삭제 | — |
| **7** 원장 3구멍 | `MV_1P5`·`THRESH_FREE`·`FPR_AS_FDR` 등록(11→15건) · **파일→원장 방향** 완전성 · fence 균형 검사 · wiki 를 관할에 포함 | `test_claim_registry_is_complete_in_both_directions`, `test_quarantine_fences_are_structurally_balanced` |
| **8** `/lean-review` | `origin/HEAD` 자동 대체 제거 → **중단하고 base 를 요구** | `test_lean_review_base_resolution_in_three_git_states` — 진짜 git 저장소 4상태 |
| **2** 목적함수별 예산 | 계약 v2 §2 — `*_budget_by_objective` · `warm_provider_map` · `realized_candidate_map_sha256` · §2.2 adaptive diagnostic schema · `N` 정의 1회 | **구현 없음** |
| **3** pair id 저장 단위 | 계약 v2 §4 — 행 단위 · `pairing_design_id` · unit cube bank · exact ordered bounds digest · truncated-ID 충돌 검사 | **구현 없음** |
| **4** truth-free plateau | 계약 v2 §6 — `degenerate`·`p` 이동·restart-source 승자를 gate 에서 제거, sentinel panel 도입 | **구현 없음** |

## 4. 발견 1 — 리뷰 수치를 우리 투영에서 독립 재현했다

리뷰가 준 두 전이표를 **커밋된 투영에서** 다시 계산했다 (리뷰 문서의 숫자를
옮겨 적지 않았다).

```
① no-warm 34p → warm 34p   (recoverable 1,476조건)
   fail → fail : 924        fail → pass : 366
   pass → pass : 182        pass → fail : 4
   순개선 362 · 실제 전이 370

② warm arm 안에서 33p → 34p
   fail → fail : 742        pass → pass : 381
   pass → fail : 186        fail → pass : 167
   discordance 353/1476 = 23.9%   (aggregate 는 +19 failures)
```

전부 리뷰 값과 일치한다. §20.4 가 이제 aggregate 가 아니라 **전이표**를 싣고,
`test_warm_contrast_reports_the_paired_transition_table` 이 투영에서 계산한
값과 문서를 결속한다.

후보 교체도 restart 투영에서 직접 센다:

```
paired_fixed5_v4_nowarm_now  33p base_init 3069 · random 12276
                             34p base_init 3069 · random 12276
paired_fixed5_v4_warm        33p base_init 3069 · random 12276
                             34p **warm 3069** · random 12276   ← base_init 소멸
```

`random` 은 양쪽 12,276 으로 같고 slot 0 만 갈린다. **후보가 늘지 않았다.**

## 5. 발견 5 — 투영 스키마 2

### 5.1 무엇이 바뀌었나

| 리뷰 지적 | 대응 |
|---|---|
| 실제 fits SHA 를 계산하지 않고 manifest 값 복사 | 읽은 바이트를 해시 → summary `_채점원본.fits_sha256` · manifest `fits_seal.file_sha256` 와 **삼중 대조** |
| `재계산_검증` 이 `by_objective` 숫자만 부분 순회 | 봉인 summary **전체** 재귀 비교 — key 집합 · `by_objective_noise` · `overall_recoverable` · `restart_conditioned` · `multistart` · `multistart_random_only` · 문자열 · 불리언 |
| per-restart 자료 없음 | `<leg>.restarts.csv.gz` — `cond_id · objective · i · source · J · p0..p3 · warm` |
| 분석기 provenance 없음 | `analyzer` 블록 (아래 §5.3) |
| malformed 입력 무시 | 중복 키 · 비유한 핵심값 · 읽기 실패 → **즉시 실패** |

### 5.2 전면 대조가 곧바로 구멍을 드러냈다

`multistart` · `multistart_random_only` 는 `summarize()` 산물이 아니라
`run_scoring` 이 `restarts_json` 에서 붙이는 블록이다. 초판 재계산은 그 둘을
**통째로 못 봤다** — 그리고 **21차 발견 3 의 근거가 바로 그 블록**이었다.
스키마 2 는 restart 투영에서 그 지표를 재계산해 봉인값과 대조한다.

### 5.3 8다리 전량 실측 (원자료 보유 기계)

```
leg                              행  restart  adaptive 예산  전체  삼중  proj  rst
fit_22p_seed_404_hc            1280     5686     True    5  True  True  True  True
fit_22p_seed_404_hc_nowarm     1280     5731     True    5  True  True  True  True
fit_22p_seed_404_hc_warm_now   1280     5686     True    5  True  True  True  True
fit_seed404_pe5mv              1280     5770     True    5  True  True  True  True
fit_seed404_pe5mv_nowarm       1280     5800     True    5  True  True  True  True
paired_fixed5_v4               6138    30690    False    5  True  True  True  True
paired_fixed5_v4_nowarm_now    6138    30690    False    5  True  True  True  True
paired_fixed5_v4_warm          6138    30690    False    5  True  True  True  True

전체   = 봉인 summary 전체를 원자료에서 재계산해 자리별 일치
삼중   = 실제 fits 바이트 SHA == summary == manifest
proj/rst = 커밋된 gz 내용의 sha256 == yaml 기록
provenance 조합(compute·scoring·spec digest) 종류: 1
```

**restart 투영이 예산 축을 구조적으로 검산한다** — 22차가 "예산 상한이지
실행 횟수가 아니다" 라고 한 것의 직접 증거다:

```
adaptive=False  6138 × 5 = 30,690  = restart 행 30,690   (정확히 일치)
adaptive=True   1280 × 5 =  6,400  → 실제 5,686~5,800
                                     adaptive 가 9.4~11.2% 를 생략
```

### 5.4 아직 못 닫은 것

`restore → validate → score → analyze` 중 `validate`(봉인 복원)는 원자료가
git 밖이라 미충족이다. Q6 의 권고(보존 단위 분리)는 계약 v2 §10 에 적었으나
실행하지 않았다. 8다리 상태는 `recorded_only` 그대로다.

## 6. 자체 발견 2건

### 6.1 fence 검사가 **이미 일어난 사고**를 잡았다

22차가 "닫는 마커가 빠지면 이후 전체가 격리된 것으로 취급된다" 고 예측했다.
균형 검사를 넣자마자 그 일이 이미 일어나 있었다:

```
08_REVIEW_RESPONSE.md:1831
  | `<!-- QUARANTINE:ID -->` … | 옛 문장을 …
  ↑ §29.1 **설명 표 안의 인용**이 여는 울타리로 파싱됐다
  → 1831줄 이후 문서 전체가 금지어 검사에서 빠져 있었고
  → 그 안에 금지어 4개가 살아 있었다
```

파서를 **"줄 전체가 마커 하나일 때만"** 으로 고쳤다. claim ID 스캐너도 같은
규칙으로 맞췄다.

**★ 그리고 원장 regex 자신이 세 번 틀렸다.** `3/51` 이 실측 붕괴 건수를,
`THRESH_FREE` 의 두 패턴이 **배너가 명시적으로 유지한다고 적은 문장**을 잡았다
(§0 의 "판정선을 어디에 두든 고칠 수 없다" 는 정반대 주장이다). 원장이 참인
문장을 금지하면 문서를 거짓으로 만든다 — "금지어는 인접 단어가 아니라
**철회된 의미**에 묶어라" 를 원장 헤더 규칙으로 박았다.

### 6.2 분석기 provenance 가 갈려 있었다

8다리 검산 중 `row_projection_py_sha256` 이 두 값으로 갈린 것을 발견했다
(7다리 `b46389d0` · `paired_fixed5_v4` `5711f104`). 확인해 보니 **차이는
`main()` 의 출력 문구뿐**이고 계산 함수 여섯 개는 바이트 동일이었다. 그러나
리뷰어는 sha 만 보고 그것을 알 수 없다.

파일 전체 대신 **계산 경로만** 해시한다 — `compute_sha256` = `_cell` ·
`_restart_list` · `_restart_facts` · `_add_multistart_blocks` ·
`_analyzer_provenance` · `build` 의 source + `COLUMNS`·`RESTART_COLUMNS`·
`ANALYSIS_SPEC`. 표시 코드를 고쳐도 안 흔들리고 계산이 바뀌면 반드시 흔들린다.
`analysis_spec_sha256` 이 **무엇을 만들기로 했는가**라면 이것은 **무엇이
만들었는가**다.

회귀 `test_all_projections_share_one_compute_provenance` 가 비교 집합 전체의
동일성을 강제한다 (현재 1종).

부수로, 요약 줄이 `by_objective_일치` 하나만 찍어 나머지 세 판정이 실패해도
✅ 가 뜨던 것도 고쳤다.

## 7. 계약 v2 — 무엇이 바뀌었나

| 절 | v1 → v2 |
|---|---|
| §0 | union 오분류 정정 (철회[WARM_UNION]) |
| §1 | 실측 교란 3 → **5** (warm slot 교체 · 예산이 warm 후보를 끌고 감) |
| §2 | 예산을 **목적함수별**로 · `warm_provider_map` · `realized_candidate_map_sha256` · `N` 정의 1회 |
| §2.1 | 하위호환을 **version-dispatched read-only** 로 완화 (Q3 — v1 의 전면 거부는 과했다) |
| §2.2 | adaptive diagnostic arm 의 표현 가능한 schema (v1 은 표현 불가 상태였다) |
| §3 | 후보 정책 3종 명명 · `equal_start_count` 로 개명 |
| §4 | pair id 를 **행 단위**로 · `pairing_design_id` · unit cube bank · exact ordered bounds digest |
| §5 | 2×2 유지 + 사전 예측(C arm 원점이 A 와 자리별 동일) |
| §6 | plateau 에서 truth 기반 gate 제거 · sentinel panel |
| §7 | primary = grid reference optimizer-controlled paired contrast + **전이표** (Q4) |
| §9 | 재실행 목록에 seed 별 0 mV control · grid sentinel · 비-PE 다리 · hard/noisy sentinel · 후보 정책 arm 추가. **12시간 추정 폐기** (Q5) |
| §10 | 보존 단위 (Q6) |

## 8. 닫지 않은 것

| 항목 | 왜 |
|---|---|
| 계약 §2·§4·§6 구현 | `src/` 변경 → `source_digest` 변화. 리뷰 순서 12번 |
| `validate`(봉인 복원) | 원자료가 git 밖. 계약 §10 에 보존 단위만 정의 |
| 고유 leg 목록·비용 재산정 | 계약 §9 에 항목만. 22차 Q5 가 요구한 leg ID 단위 전개 미완 |
| 8다리 상태 | `recorded_only` 유지 |
| §20.4 의 `multistart._해석` 문자열 | `src/` 가 생성 → 단계 3 코드 라운드 |
| plateau pilot | 기준만 정의, 미실행 |

## 9. 질문

### Q1. 계약 v2 §4 의 3단 ID 가 과한가

`latent_pair_id → bank_id → mapped_candidate_id` 로 나눴다. 리뷰 권고를 그대로
받았는데, 구현 복잡도가 실제로 필요한 수준인지 확인받고 싶다. 특히
`pairing_design_id` 를 사람이 지정하는 필드로 둘지, 실험 설계에서 자동
유도할지 판단이 갈린다.

### Q2. §2 의 목적함수별 예산이 2×2 와 곱해지면 arm 수가 폭발한다

`p_ini_budget × condition_budget × p_ini_warm × condition_warm ×
candidate_mode` 를 전부 요인화하면 arm 이 수십 개다. 계약 §4.4 는 대안으로
"provider 예산과 조건별 provider-solution map 을 먼저 고정·봉인" 을 적었다.
**둘 중 어느 쪽을 기본 설계로 삼아야 하는가?** 후자면 arm 수가 크게 준다.

### Q3. plateau sentinel panel 의 최소 구성

계약 §6 은 half-cell/grid · clean/noisy · smooth/dQdV · hard/boundary 를
포함하라고 적었으나 **구체적 조건 목록이 없다**. 몇 조건이면 충분한가, 그리고
"hard/boundary" 를 무엇으로 정의해야 하는가 (예: 21차 6격자 표에서 갈린 조건,
`alpha_wall` 이 붙은 조건)?

### Q4. `recorded_only` 8다리를 §7 primary 설계의 **사전 정보**로 쓰는 것이 허용되는가

전이표(§4)와 후보 구성(§4)은 이 다리들에서 나왔다. 이것을 **결론**으로 쓰지
않는 것은 분명한데, **새 실험의 설계 근거**(예: 예산 상한 후보 범위, sentinel
선정)로 쓰는 것도 제한해야 하는지 판단이 갈린다.

### Q5. 자체 발견 6.1 의 함의 — 다른 lint 도 같은 구멍이 있는가

fence 파서의 "줄 전체" 규칙을 이번에 넣었는데, 이 저장소의 다른 문서 검사
(`RETRACTED` 정규식, `_P22_STALE_DENIALS`, wiki lint 15검사)도 같은 형태의
**설명용 인용이 검사 대상으로 오인되는** 구멍이 있을 수 있다. 전수 점검을
이번 라운드에 넣어야 하는가, 아니면 단계 3 이후로 미뤄도 되는가?

## 10. 재현 명령

```bash
git fetch origin main claude/14-gate-code-review-9qkx05
git rev-parse --is-shallow-repository        # false 여야 한다
git checkout a037eba4

# identity
python -c "import sys;sys.path.insert(0,'.');from src.io import source_digest;print(source_digest())"
git diff --name-only f57ecd4d..HEAD -- src tools configs scripts run.sh 'requirements*'

# 발견 1 — 후보가 교체됐는가 (restart 투영에서 직접)
python3 - <<'PY'
import csv,gzip,pathlib,collections
d=pathlib.Path('docs/22p_gap/warm_probe')
for leg in ('paired_fixed5_v4_nowarm_now','paired_fixed5_v4_warm'):
    with gzip.open(d/f'{leg}.restarts.csv.gz','rt',encoding='utf-8') as f:
        rs=list(csv.DictReader(f,delimiter='\t'))
    print(leg, dict(collections.Counter((r['objective'],r['source']) for r in rs)))
PY

# 발견 1 — 전이표 재현
python3 - <<'PY'
import csv,gzip,pathlib,collections
d=pathlib.Path('docs/22p_gap/warm_probe')
def load(l):
    with gzip.open(d/f'{l}.projection.csv.gz','rt',encoding='utf-8') as f:
        return {(r['cond_id'],r['objective']):r for r in csv.DictReader(f,delimiter='\t')}
nw,wm=load('paired_fixed5_v4_nowarm_now'),load('paired_fixed5_v4_warm')
c=collections.Counter()
for (cid,obj),r in nw.items():
    if obj!='pocv_dvdq_dqdv' or r['recoverable']!='1': continue
    s=wm[(cid,obj)]
    c[('fail' if r['degenerate']=='1' else 'pass','fail' if s['degenerate']=='1' else 'pass')]+=1
print(dict(c), '합', sum(c.values()))
PY

# 발견 5 — 투영 자기정합 + provenance 단일성
python3 - <<'PY'
import gzip,hashlib,pathlib,yaml,collections
d=pathlib.Path('docs/22p_gap/warm_probe'); prov=collections.Counter()
for y in sorted(d.glob('*.projection.yaml')):
    m=yaml.safe_load(y.read_text(encoding='utf-8')); a=m['analyzer']; v=m['재계산_검증']
    p=hashlib.sha256(gzip.decompress((d/m['projection_file']).read_bytes())).hexdigest()==m['projection_sha256']
    r=hashlib.sha256(gzip.decompress((d/m['restart_projection_file']).read_bytes())).hexdigest()==m['restart_projection_sha256']
    prov[(a['compute_sha256'],a['src_scoring_py_sha256'],m['analysis_spec_sha256'])]+=1
    print(f"{m['leg_id']:30s} 전체={v['전체_일치']} 삼중={v['fits_삼중일치']} proj={p} rst={r}")
print('provenance 종류:', len(prov))
PY

# 발견 5 — 예산 상한 vs 실행 횟수 (구조적 검산)
python3 - <<'PY'
import csv,gzip,pathlib,yaml
d=pathlib.Path('docs/22p_gap/warm_probe')
for y in sorted(d.glob('*.projection.yaml')):
    m=yaml.safe_load(y.read_text(encoding='utf-8'))
    man=yaml.safe_load((d/f"{m['leg_id']}.manifest.yaml").read_text(encoding='utf-8'))['run_spec']
    cap=m['n_rows']*man['n_restarts']
    print(f"{m['leg_id']:30s} adaptive={man['optimizer']['adaptive']!s:5s} "
          f"상한 {cap:6d} 실제 {m['n_restart_rows']:6d} 생략 {cap-m['n_restart_rows']:5d}")
PY

# 발견 7 — 원장 양방향 + fence 균형 (변이 시험)
python -m pytest tests/test_docs_lint.py -q -k "registry or fence or reappear"
printf '\n<!-- QUARANTINE:OP_EQUIV -->\n' >> docs/09_22P_GAP.md   # 닫지 않은 울타리
python -m pytest tests/test_docs_lint.py -q -k fence              # 실패해야 정상
git checkout -- docs/09_22P_GAP.md

# 발견 8
python -m pytest tests/test_docs_lint.py -q -k lean_review

# 전체
python -m pytest tests/ -q
./scripts/smoke_e2e.sh
```

원자료가 필요한 것 (리뷰어 환경 불가):

```bash
python docs/22p_gap/row_projection.py --all
```

## 11. GO 시 실행 순서 (리뷰 순서 12번)

```
1  pair_group_id 행 단위 + unit cube bank 생성기   src/grid.py, src/fitting.py
2  protocol 을 목적함수별 예산으로 → run_spec, sig_version 6
3  p_ini 경로 분리 + candidate_mode 3종
   ── 여기서 source_digest 가 바뀐다 ──
4  smoke 에 2×2 arm + 중첩 bank 접두사 + 후보 정책 3종 (작은 fixture)
5  leg_index 생성기를 tools/ 로 승격
6  22p semantic freshness gate + archive index merge
7  sentinel panel plateau pilot → 예산 확정
8  고유 leg 목록 확정 → 비용 재산정 → 재실행 승인 요청
```

8번의 승인을 받기 전에는 대규모 재실행을 시작하지 않는다.
