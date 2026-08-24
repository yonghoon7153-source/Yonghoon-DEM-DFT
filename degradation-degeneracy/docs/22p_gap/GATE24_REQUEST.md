# 24차 게이트 리뷰 요청 — 23차 발견 1·5·7 + P0 일곱 개 대응, 계약 v3 재심사

```
브랜치   origin/claude/14-gate-code-review-9qkx05
source_digest  a72c0f3a485c19bb   ← 21·22·23·24차와 동일 (RUN_SCOPE 무변경)

# 이 문서는 왕복 하나가 아니라 **셋**을 담는다. 각 절이 어느 커밋을 말하는지:
code_target        439e06ef594acff751a557c2fe4cda86d953a6e0   §1~§10  (24차 본 요청)
supplement_parent  58fb51ed…                                   §11 을 담은 커밋의 부모
supplement_target  0ca48cbf…                                   §11    (원자료 손실 정정)
supplement2_target <이 커밋>                                    §12    (24차 보충 리뷰 대응)
직전 대상          a037eba4ef2e65205522380b123455c5de1dcda3   (23차, NO-GO)
```

> **★ 24차 보충 리뷰가 지적한 것 (발견 9)** — 초판 식별 블록은 `439e06ef` 하나만
> 적어 두고 §11 을 그 아래 덧붙였다. 그런데 §11 은 `439e06ef` 에 없다 —
> `0ca48cbf` 에서 생겼다. 리뷰어가 `439e06ef` 를 체크아웃하면 §11 이 말하는
> 파일들이 없다. 그리고 `0ca48cbf` 자체의 전체 테스트·smoke 영수증이 어디에도
> 없었다. 둘 다 아래 §12.1 에서 닫는다.

## 0. 요청 판정

리뷰가 정한 순서 **11번(문서·회귀 재심사)** 이다. 12번(RUN_SCOPE 변경)은 아직
시작하지 않았다.

**★ 24차 보충 리뷰 후 순서가 하나 늘었다** — RUN_SCOPE 변경 **앞에**
「보존 gate 구현 + 빈 root smoke」가 들어간다 (§12.5). 7다리를 잃은 원인이
도구 부재가 아니라 **강제 부재**였기 때문이다.

| 대상 | 요청 |
|---|---|
| 23차 발견 1·5·7 | 닫혔는가 |
| `STAGE3_CONTRACT.md` **v3** (P0-1~7) | 구현 착수 가능한가 |
| 대규모 재실행 | **승인 요청하지 않는다** — 고유 leg 목록·비용표 전이다 |

## 1. 검증 — 방금 실행한 출력

```
$ git rev-parse HEAD
439e06ef594acff751a557c2fe4cda86d953a6e0
$ git status --short
(빈 출력)

$ python -m pytest tests/ -q
689 passed in 377.21s

$ ./scripts/smoke_e2e.sh
✅ end-to-end smoke 통과 — 본 실행을 시작해도 된다

$ python -c "…source_digest()"
a72c0f3a485c19bb

$ python3 wiki/tools/lint.py
RESULT: 0 errors

$ git status --porcelain -- src tools configs scripts run.sh 'requirements*'
(빈 출력)
```

23차가 "이 Windows 세션에 pytest/pandas 가 없어 재실행 못 했다" 고 기록한
`685 passed` 와 smoke 를 대상 커밋에서 다시 돌렸다 (689 / 통과).

## 2. 커밋 5개

| SHA | 무엇 |
|---|---|
| `f49cd66e` | 발견 1·7 대응 + 계약 v3 + 투영 스키마 3 구현 |
| `4fd38481` | 8다리 재생성 (원자료 보유 기계) |
| `43d0ac8e` | **자체 발견** — 스키마 3 의 두 필드가 실제로 안 들어가 있었다 |
| `fa5f63fc` | 8다리 재생성 (스키마 3 실제 적용) |
| `439e06ef` | **자체 발견** — 옛 테스트가 스키마 번호를 하드코딩 |

## 3. 발견별 대응

| 23차 발견 | 대응 | 회귀 |
|---|---|---|
| **1** WARM_UNION 활성 잔여 4곳 (`LEG_INVENTORY:1012-14` · `08:1881-82` · 테스트 docstring · 계약 §0) | 원장 regex 를 **의미 기반**으로 넓히고(조사·어미 변형 6패턴) 4곳 전부 정리. 계약 §0 의 옛 문구는 울타리로 | `test_retracted_claims_do_not_reappear_in_active_prose` — 넓힌 regex 가 4곳을 **RED 로 잡은 뒤** 고쳤다 |
| **5-1** `projection_schema: 2` vs `ANALYSIS_SPEC.projection_version: 1` | spec 을 `schema_version: 3` 으로 재작성 — `row_projection`·`restart_projection`(정렬키·digest)·`summary_comparison`(type_policy)·`fits_binding` | `test_projection_schema_is_declared_consistently` |
| **5-2·3** `_restart_list` 가 `None`·float·non-dict 를 조용히 버림 / `p` NaN 패딩·절단 / index·유한성·행 수 미검사 | 전부 fail-closed. `source` enum 검사 추가, `p` 길이 4 강제 | 생성 시 예외 (변이 §5.3) |
| **5-4** `_cmp` 가 한쪽 float 이면 양쪽 `float()` → `"0.1"==0.1`, `1==1.0` | **타입 exact** — 타입이 다르면 그 자체가 불일치 | 전면 대조가 8다리에서 통과 |
| **5-5** `validate_provenance` 미호출인데 §11 이 "validate 완료" | 계약 §10·§11 에서 미충족으로 유지 (아래 §7) | — |
| **5-6** `summary_sha256`·`manifest_sha256` 없음 → 회귀가 기록된 boolean 을 다시 믿음 | 봉인 원본을 해시해 기록 | `test_projection_schema_is_declared_consistently` 가 존재 강제 + §5.2 가 값 재계산 |
| **5-7** 분석기 회귀가 YAML 끼리만 비교 → "다 같이 낡은" 것을 못 잡음 | **현재 트리에서 재계산**해 대조 | `test_projection_analyzer_digests_recompute_from_the_current_tree` |
| **5-8** fits 를 해시 후 다시 열음 | 한 번 읽은 바이트로 해시·파싱 | — |
| **7-a** `_CLAIM_SCOPE` 하드코딩 5파일 | `docs/**/*.md` + `wiki/**/*.md` 에서 **명시적 제외만 뺀 전부** (43개 스캔) | 아래 §4 자체 발견 |
| **7-b** ID 가 등록돼도 파일이 `claim.files` 에 없으면 검사 안 함 | 파일↔claim.files 결속 추가. `AXIS_RANK`·`R20_RX` 에 wiki, `WARM_TIE` 에 09 추가 | `test_claim_registry_is_complete_in_both_directions` 두 번째 층 |
| **7-c** "활성 잔여 6곳" 인데 열거는 8곳 | 8곳으로 정정 | — |
| **8** `lean_review_..._three_git_states` 이름 오기 | `four` 로 | — |

## 4. 자체 발견 3건

### 4.1 철회 체계가 **둘**로 갈려 있었다

관할을 발견 기반으로 바꾸자마자 드러났다.

```
(구) tests/test_docs_lint.py 의 RETRACTED dict + 절별 `⛔ 철회[ID]` 마커
     — 17~18차, 05_HANDOFF.md · GATE14_CYCLE_SUMMARY.md 담당, claim 8건
(신) CLAIM_STATUS.yaml + <!-- QUARANTINE:ID --> 울타리
     — 21차 이후, 나머지 담당
```

둘 다 동작하지만 **서로를 몰랐다.** 22차까지 관할이 5파일 하드코딩이라 옛
문서가 아예 밖에 있어서 이 갈라짐이 안 보였다. 한쪽에서 claim 이 사라져도
다른 쪽은 조용하다 — 이 저장소가 반복해 온 실패 형태다.

옛 8건을 `record: legacy_section_marker` 로 등록하고 **양쪽 집합이 같은지**
검사한다 (`test_legacy_and_registry_claim_systems_agree`).

⚠ 단일 체계로의 **이전은 하지 않았다.** 옛 문서는 절 단위 마커를, 새 체계는
울타리를 쓰는데 그 변환은 문서 구조를 바꾸는 별도 작업이다. 지금은 두 체계가
같은 claim 집합을 본다는 것만 고정했다.

### 4.2 restart 투영이 **렌더링된 문자열**을 정렬하고 있었다

`sorted(r_lines[1:])` — 문자열 정렬이라 `i=10` 이 `i=2` 앞에 온다. 지금은
예산 5라 한 자리여서 결과가 같지만, **계약 §6 의 예산 40 에서 발현**한다.
spec 이 선언한 정렬키 `[cond_id, objective, i]` 와 실제가 갈리는 잠복 버그다.
튜플 정렬로 고쳤다 (투영 gz 내용은 불변 — 재생성 후 `.csv.gz` diff 0).

### 4.3 스키마 번호 하드코딩 · 편집 누락

- `test_warm_probe_row_projections_are_committed_and_self_consistent` 가
  `projection_schema != 2` 로 숫자를 박아 뒀다. 스키마 3 이 되자 **정상
  산출물을 거부**했다. `ANALYSIS_SPEC.schema_version` 에서 읽도록 고쳤다.
  (20차 발견 13-2 의 `BRANCHES.md` 커밋 수, 21차 `restart_table` 앵커와 같은
  형태다 — 값이 바뀌는 곳에 리터럴.)
- `projection_schema: 3` 과 봉인 원본 digest 를 넣는 편집이 **실제로 적용되지
  않았다** — 편집 스크립트가 앞 항목의 assert 에서 죽어 파일을 안 쓰고 종료했다.
  회귀를 먼저 쓴 덕에 재생성 후에도 실패가 남아 잡혔다.

## 5. 실측

### 5.1 8다리 전량 (원자료 보유 기계, 스키마 3)

```
leg                            sch  전체  삼중  봉인  proj   rst   sum   man
fit_22p_seed_404_hc              3  True  True  True  True  True  True  True
fit_22p_seed_404_hc_nowarm       3  True  True  True  True  True  True  True
fit_22p_seed_404_hc_warm_now     3  True  True  True  True  True  True  True
fit_seed404_pe5mv                3  True  True  True  True  True  True  True
fit_seed404_pe5mv_nowarm         3  True  True  True  True  True  True  True
paired_fixed5_v4                 3  True  True  True  True  True  True  True
paired_fixed5_v4_nowarm_now      3  True  True  True  True  True  True  True
paired_fixed5_v4_warm            3  True  True  True  True  True  True  True

전체 = 봉인 summary **전체**를 원자료에서 재계산해 타입까지 자리별 일치
삼중 = 실제 fits 바이트 SHA == summary._채점원본 == manifest.fits_seal
proj/rst/sum/man = 커밋된 파일 내용의 sha256 == yaml 기록
provenance 조합(compute · analysis_spec) 종류: 1
```

### 5.2 리뷰 수치를 우리 투영에서 독립 재현

23차가 준 두 값을 커밋된 투영에서 다시 계산했다.

```
pair-group:  fit_22p_seed_404_hc → 1,280행 · cond_id 640 ·
             물리좌표(lli,lam_pe,lam_ne) 320 · noise [0.0, 0.005]
             → 계약 v2 의 n_pair_groups: 640 은 자기 §4.2 규칙과 안 맞았다

no-warm 33p→34p (primary 와 같은 arm, recoverable 1,476):
   pp=131  pf=436  fp=55  ff=854   불일치 33.27%  순증 실패 381
warm    33p→34p:
   pp=381  pf=186  fp=167 ff=742   불일치 23.92%  순증 실패 19
```

**두 표를 나란히 놓으면 v2 의 실수가 왜 중요한지 보인다** — primary 는 no-warm
인데 근거 표가 warm 이었고, 그 차이가 "34p 가 얼마나 나쁜가" 를 **20배**
바꾼다 (순증 381 vs 19).

## 6. 계약 v3 — P0 일곱 개

| P0 | v2 의 문제 | v3 |
|---|---|---|
| **1** | `N` 이 mode 에 따라 다른 random 수를 뜻함 (`equal_start_count` 는 `bank[:M-1]`) | 기준을 **총 시작점 예산 `B`** 로. `random_bank_prefix_len` 분리. `planned_counts`/`realized_counts`/`total_n_eval`/`wall_time_s` 병기 |
| **2** | `n_pair_groups: 640` (실제 320) · `latent_pair_id`/`pair_group_id` 혼용 · candidate ID 가 random 만 | 320 정정 · 이름을 `pair_group_id` 하나로 · `pairing_design_label` + `pairing_design_sha256` 분리 (canonical design spec 6항목) · `candidate_id` 를 base/warm/random 세 source 전부로 |
| **3** | `warm_provider_map` 이 관계 이름일 뿐 값 미고정 | provider artifact·solution-map·`p_ini_values` digest 6종 추가 |
| **4** | `≤1%`·`abs_tol`·`rel_tol` 이 수치가 아님 · `max(1,\|J\|)` 문제 · 작은 n 에서 1% 무의미 | objective 별 **numerical floor 를 먼저 실측**하는 절차 · max-N 한 번 + prefix minima offline · `n<100 → material 개선 0건` 규칙 |
| **5** | sentinel 조건 목록 없음 | `sentinel_panel.yaml` 스키마 · archetype 5종 · 구현 smoke 와 budget pilot 분리 · **geometry hard vs empirical hard** (후자는 holdout 필수) |
| **6** | primary 는 no-warm 인데 근거 표는 warm · status 3축 혼재 | no-warm 표(131/436/55/854)로 교체 · primary scalar `Δ = 0.2581` 하나 정의 · `preservation_status`/`validation_status`/`inference_role` 분리 |
| **7** | "기존 산출물 전부 재실행" 이 §2.1 과 모순 · `0.027초/restart` 를 단일 restart 시간처럼 | v6 claim 지지·resume 대상으로 한정 · wall / core-time(23,324 core-초) / throughput 3축 |

신설 **§9.4** — 단계 3 원 fits 에 `converged`·`termination_status`·`n_eval`·
`candidate_id`·`bank_index` 를 남긴다 (23차 발견 5 꼬리).

회귀 `test_stage3_contract_primary_table_matches_the_no_warm_projection` 이
§7.1 의 네 칸과 scalar 를 **투영에서 계산해** 문서와 대조한다.

## 7. 닫지 않은 것

| 항목 | 왜 |
|---|---|
| 계약 §2·§4·§6 **구현** | `src/` 변경 → 리뷰 순서 12번 |
| ~~`validate_provenance` 호출~~ | **닫혔다 (§12.1)** — `artifacts/paired_fixed5_v4` 복원 후 34검사 전부 통과, 영수증 커밋됨. 나머지 7다리는 원자료가 없어 영구 불가 |
| 고유 leg 목록·비용 재산정 | 계약 §9 에 항목만. 23차가 요구한 leg ID 단위 전개 미완 |
| 두 철회 체계의 **단일화** | §4.1 — 결속만 했고 이전은 안 했다 |
| 8다리 상태 | **§11 정정 참조** — 1개 `full_bundle`+`current_validated`, 7개 `missing` |
| §20.4 의 `multistart._해석` 문자열 | `src/` 가 생성 → 단계 3 코드 라운드 |
| plateau pilot · sentinel_panel.yaml **실체** | 기준·스키마만 정의, 미실행 |

## 8. 질문

### Q1. 두 철회 체계를 지금 단일화해야 하는가

§4.1 에서 결속만 했다. 옛 문서(`05_HANDOFF.md`·`GATE14_CYCLE_SUMMARY.md`)를
울타리 체계로 이전하면 문서 구조가 바뀌고, 그 두 문서는 이미 "폐기·정본 참조"
배너가 달린 handoff 기록이다. **이전이 필요한가, 결속으로 충분한가?**

### Q2. 계약 §4.2 의 canonical design spec 6항목이 구현 가능한 수준인가

`pairing_design_sha256` 에 들어갈 것을 6항목으로 적었는데, 그중
"varied treatment axis 의 **종류**와 arm 역할" 은 실험 설계를 기계가 읽을 수
있는 형태로 적어야 한다는 뜻이다. **이것을 어느 정도까지 구조화해야 하는가?**
(예: `{axis: pe_offset, arms: [control, treated], values_excluded: true}`)

### Q3. §6 의 numerical floor 측정을 어떻게 truth-free 로 하는가

"같은 입력을 반복하거나 같은 max-bank prefix 를 재평가" 라고 적었는데, 이
파이프라인은 **결정론적**이라 같은 입력을 반복하면 같은 값이 나온다
(floor = 0). 실제로 재현 산포를 만들려면 무엇을 바꿔야 하는가 — BLAS 스레드
수? 부동소수 요약 순서? 아니면 floor 를 다른 방식으로 정의해야 하는가?

### Q4. **(재작성)** `paired_fixed5_v4` 하나로 무엇을 할 수 있는가

요청문 작성 후 작업 기계가 교체되면서 warm 실험 **7다리의 원자료를 잃었다**
(§11). 살아남은 `paired_fixed5_v4` 는 완전 bundle 이고 `validate_provenance`
**34검사 전부 통과**했다 (ok=True, fail=[]).

- 이 한 다리로 23차 Q6 이 요구한 "도구 경로가 동작한다는 smoke 근거" 가
  충족되는가?
- 그 다리를 `inference_role: canonical` 로 승격할 수 있는가, 아니면 새
  protocol 산물이 아니므로 `historical_validated` 에 머물러야 하는가?
- 7다리는 투영만 남았다. 계약 §8 의 3축으로 `missing`/`unvalidated`/
  `diagnostic` 이라 적었는데, **전이표·후보 구성·다봉성을 설계 근거로 쓰는
  것**(23차 Q4 가 허용한 exploratory design prior)은 그대로 유효한가?

### Q5. 자체 발견 4.3 의 함의 — 리터럴 하드코딩 전수 점검이 필요한가

같은 형태가 이번까지 **세 번** 나왔다 (`BRANCHES.md` 커밋 수 · `restart_table`
앵커 · `projection_schema`). 테스트·문서에서 "값이 바뀌는 곳의 리터럴" 을
전수로 훑는 작업을 이번 라운드에 넣어야 하는가, 아니면 단계 3 이후로 미뤄도
되는가?

## 9. 재현 명령

```bash
git fetch origin claude/14-gate-code-review-9qkx05
git rev-parse --is-shallow-repository        # false 여야 한다
git checkout 439e06ef

# identity
python -c "import sys;sys.path.insert(0,'.');from src.io import source_digest;print(source_digest())"
git diff --name-only a037eba4..HEAD -- src tools configs scripts run.sh 'requirements*'

# 투영 전수 자기정합 (표준 라이브러리만)
python3 - <<'PY'
import gzip,hashlib,pathlib,yaml,collections
d=pathlib.Path('docs/22p_gap/warm_probe'); prov=collections.Counter()
for y in sorted(d.glob('*.projection.yaml')):
    m=yaml.safe_load(y.read_text(encoding='utf-8')); a=m['analyzer']; v=m['재계산_검증']
    chk={
      'proj': hashlib.sha256(gzip.decompress((d/m['projection_file']).read_bytes())).hexdigest()==m['projection_sha256'],
      'rst':  hashlib.sha256(gzip.decompress((d/m['restart_projection_file']).read_bytes())).hexdigest()==m['restart_projection_sha256'],
      'sum':  hashlib.sha256((d/f"{m['leg_id']}.summary.yaml").read_bytes()).hexdigest()==m['summary_sha256'],
      'man':  hashlib.sha256((d/f"{m['leg_id']}.manifest.yaml").read_bytes()).hexdigest()==m['manifest_sha256'],
    }
    prov[(a['compute_sha256'],m['analysis_spec_sha256'])]+=1
    print(f"{m['leg_id']:30s} sch={m['projection_schema']} 전체={v['전체_일치']} "
          f"삼중={v['fits_삼중일치']} 봉인={m['fits_봉인일치']} {chk}")
print('provenance 조합:', len(prov))
PY

# restart 투영의 정렬키가 실제로 (cond_id, objective, i) 인가 — 4.2 의 잠복 버그
python3 - <<'PY'
import csv,gzip,pathlib
p=pathlib.Path('docs/22p_gap/warm_probe/paired_fixed5_v4_warm.restarts.csv.gz')
with gzip.open(p,'rt',encoding='utf-8') as f: rs=list(csv.DictReader(f,delimiter='\t'))
key=[(r['cond_id'],r['objective'],int(r['i'])) for r in rs]
print('정렬 정상:', key==sorted(key), '| 행', len(rs))
PY

# no-warm primary 전이표 (계약 §7.1 과 대조)
python3 - <<'PY'
import csv,gzip,pathlib,collections
d=pathlib.Path('docs/22p_gap/warm_probe')
with gzip.open(d/'paired_fixed5_v4_nowarm_now.projection.csv.gz','rt',encoding='utf-8') as f:
    x={(r['cond_id'],r['objective']):r for r in csv.DictReader(f,delimiter='\t')}
c=collections.Counter()
for (cid,obj),a in x.items():
    if obj!='pocv_dvdq' or a['recoverable']!='1': continue
    b=x[(cid,'pocv_dvdq_dqdv')]
    c[('fail' if a['degenerate']=='1' else 'pass','fail' if b['degenerate']=='1' else 'pass')]+=1
n=sum(c.values()); net=c[('pass','fail')]-c[('fail','pass')]
print(dict(c), 'n', n, 'Δ', round(net/n,4))
PY

# pair-group 320
python3 - <<'PY'
import csv,gzip,pathlib
with gzip.open('docs/22p_gap/warm_probe/fit_22p_seed_404_hc.projection.csv.gz','rt',encoding='utf-8') as f:
    r=list(csv.DictReader(f,delimiter='\t'))
print(len(r), len({x['cond_id'] for x in r}),
      len({(x['lli'],x['lam_pe'],x['lam_ne']) for x in r}),
      sorted({x['noise'] for x in r}))
PY

# 원장 양방향 + fence 균형 + 두 체계 결속 (변이 포함)
python -m pytest tests/test_docs_lint.py -q -k "registry or fence or legacy_and_registry"
printf '\nPE 가 NE 보다 치명적이다.\n' >> ../wiki/questions/22p-physics-or-degeneracy.md
python -m pytest tests/test_docs_lint.py -q -k reappear      # 실패해야 정상
git checkout -- ../wiki/questions/22p-physics-or-degeneracy.md

# 전체
python -m pytest tests/ -q
./scripts/smoke_e2e.sh
```

원자료 필요 (리뷰어 환경 불가): `python docs/22p_gap/row_projection.py --all`

## 10. GO 시 실행 순서 (리뷰 순서 12번)

```
0  ★ 보존 gate — leg 생성이 보존 영수증 없이 끝날 수 없게 (계약 v4 bundle 3)
   tools/preserve_leg.py + 빈 root smoke. RUN_SCOPE 안이므로 digest 가 바뀐다.
   **1번보다 먼저** — 아래 1~9 가 만드는 다리를 또 잃지 않기 위해서다.
1  pair_group_id 행 단위 + unit cube bank 생성기    src/grid.py, src/fitting.py
2  protocol 을 총 시작점 예산 B · 목적함수별로 → run_spec, sig_version 6
3  p_ini 경로 분리 + candidate_mode 3종 + provider freeze
   ── 여기서 source_digest 가 바뀐다 ──
4  restart 행에 converged·termination_status·n_eval·candidate_id·bank_index (§9.4)
5  smoke 에 2×2 arm + 중첩 bank 접두사 + 후보 정책 3종 (작은 fixture)
6  leg_index 생성기를 tools/ 로 승격 · status 3축
7  numerical floor 측정 → tolerance 확정 → sentinel_panel.yaml 작성
8  plateau pilot → 예산 확정
9  고유 leg 목록 확정 → 비용 재산정 → **재실행 승인 요청**
```

9번 승인 전에는 대규모 재실행을 시작하지 않는다.


---

## 11. ★ 요청문 작성 후 정정 (2026-08-24) — 원자료 7다리 손실

이 요청문은 8다리를 전부 "원자료 보유 기계에서 재생성 가능" 으로 적었다.
**작성 후 작업 기계가 교체되면서 그것이 틀린 상태가 됐다.**

| 다리 | `preservation_status` | `validation_status` | `inference_role` |
|---|---|---|---|
| `paired_fixed5_v4` | **`full_bundle`** | **`current_validated`** | `canonical_candidate` |
| 나머지 7 (warm 실험) | `missing` | `unvalidated` | `diagnostic` |

### 11.1 `paired_fixed5_v4` — 34검사 전부 통과

2026-08-16 백업에서 복구. `fits.parquet` sha256 이 manifest 봉인과 바이트
일치하고 `_inputs/`·`attempts/`·`fit_chunks/` 가 완비된 **완전 bundle** 이다.

```
$ validate_provenance('results/paired_fixed5_v4')
ok: True · 검사 수: 34 · 실패: []
  출력봉인_재계산 · 입력_digest_재해시 · 조건집합_서명일치 ·
  run_signature_재계산 · 곡선_producer_재검 · restart_예산_완주 … 34/34
```

**검사기가 실패를 실제로 잡는지 변이로 확인**했다 — fits 중간 1비트를 뒤집으면
`ok: False`, `fail: ['출력봉인_재계산', 'restart_출처', 'restart_예산_완주']`.
즉 `fail: []` 는 검사가 안 돈 것이 아니다.

**21차 발견 6 의 세 번째 줄(`restore → validate → score → analyze`)이 이
다리에서 닫혔다.** §7 의 "닫지 않은 것" 첫 줄을 이만큼 정정한다.

투영은 **세 번째 기계**에서도 바이트 동일하게 재생성됐다 (`ad598fe77e75afec`).
`grid_curves_v4`(봉인 입력 곡선)도 함께 복구돼 계약 §9 의 곡선 재사용 경로가
실물로 확보됐다.

### 11.2 7다리 — 손실

2026-08-20 warm 실험이라 백업 이후다. 네 곳 전수 조사에서 없다.

**결론은 무너지지 않는다** — 전이표(`131/436/55/854`·`381/186/167/742`) ·
후보 구성(`base_init` → `warm` slot 교체) · random-only 다봉성(`0.969512`) 이
전부 **커밋된 투영에서 재계산**된다. 이 요청문 §4·§5.2 의 수치가 그것이다.

잃은 것: 투영을 원자료에서 다시 만들 수 없고, `validate_provenance` 가 영구
불가하며, 투영에 없는 열(`p_spread` 등)이 사라졌다.

### 11.3 계약 §10·§11 을 고쳤다 — 보존을 실행 **앞으로**

> **★ 이 절의 원인 진단은 틀렸다 (24차 보충 리뷰).** 아래 문단은 기록으로
> 남기고, 정정은 §12.4 에 있다. 요약: 보존 도구는 **이미 있었고 작동했다**.
> 없었던 것은 강제다.

23차 Q6 이 content-addressed 보존을 권고했고 우리는 계약 §10 에 적어 두고
구현을 "단계 3 이후" 로 미뤘다. **그 사이에 잃었다.**

구현 순서에서 보존을 12번(RUN_SCOPE 변경) **앞**으로 옮겼다. 보존 없이 새로
돌리면 같은 방식으로 또 잃는데, 이번엔 ~12시간짜리다.

### 11.4 부수 발견 — `validate_provenance` 가 깨진 parquet 에서 예외로 죽는다

footer 손상 시 `pd.read_parquet` 이 먼저 죽어 `ArrowInvalid` 가 그대로
올라온다 (`src/io.py:1676`). 조용한 통과는 아니라 안전 쪽이지만, 함수 계약이
`{"ok":…, "fail":[…]}` 라 **깨진 파일을 발견으로 보고하지 못한다.** `src/` 라
지금 고치면 digest 가 바뀐다 → 계약 §9.4 로 이월.

### 11.5 새 회귀 2건

- `test_preservation_registry_covers_every_warm_probe_leg` — 투영이 있는 모든
  다리가 `LEG_PRESERVATION.yaml` 에 3축으로 등록됐는가. **원자료가 없는데
  `validation_status` 가 `unvalidated` 가 아니면 실패**한다.
- `test_docs_do_not_claim_lost_legs_are_regenerable` — 손실 다리가 §32 에
  기록돼 있는가. **★ 이 판은 이름이 약속한 일을 하지 않았다** — 금지 문구를
  검색하지 않았다 (보충 발견 5). §12.3 에서 고쳤다.

변이 2건(손실 다리를 "검증됨" 으로 위장 · 원장에서 다리 삭제) 전부 실패 확인.
