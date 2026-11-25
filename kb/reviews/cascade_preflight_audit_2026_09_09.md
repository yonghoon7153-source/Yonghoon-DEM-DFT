---
title: cascade_preflight_audit_2026_09_09
date: 2026-09-09
updated: 2026-09-09
tags: [cascade, 조사, 2026-09-09]
status: 진행
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: single-source
---

# cascade 273 재실행 전 적대적 사전감사 (2026-09-09)

> 6 에이전트 · 953 k 토큰 · 33분. **읽기 전용** — 파일 수정·GPU 실행 0건.
> Stage 00–12 본문을 실제로 열고 셸↔파이썬 계약을 대조했다. 아래는 원문 그대로다.
> ⚠ 각 절 말미의 *"못 본 것"* 을 같이 읽는다 — 확인한 것과 코드 읽기로만 판정한 것이 구분돼 있다.

---

## Stage 00–03

읽기 전용 감사 완료. 아래가 Stage 00–03 결과다.

---

## [치명] 3개 농도(x002/x005/x010)가 **바이트 단위로 같은 구조**를 만든다 — 273 중 182 캐스케이드가 중복

· **어디**: `tools/doping/substitute_compound.py:678` · `tools/doping/master_batch_273.sh:88-92, 312-319`
· **무엇**: `n_units = max(1, int(round(n_fu_actual * x_compound)))`. 1,1,1 셀은 `n_fu_actual = 4` 라 `round(4×0.02)=0`, `round(4×0.05)=0`, `round(4×0.10)=0` → 셋 다 `max(1,0)=1`. **x ≥ 0.125 이어야 2가 된다.** 세 농도 모두 그 아래다. 즉사하지 않고 **조용히** 같은 구조를 3번 만든다. 게다가 실제 농도는 `actual_x = 1/4 = 0.25` — 라벨(2%)의 **12.5배**다. 파일명은 `..._x020_...` / `..._x050_...` / `..._x100_...` 로 **다르게** 붙어서 겉으로는 세 농도처럼 보인다. 마지막에 `master_batch_273.sh:368` 이 디렉터리 이름에서 `concentration_pct = 2.0/5.0/10.0` 을 **지어내서** unified CSV 에 박고, 그게 Layer-2 ML predictor 의 "concentration-aware feature" 가 된다 — 같은 feature 에 서로 다른 라벨 3개.
· **근거**: 실행해서 확인 (CPU, GPU 안 씀). 세 농도로 `substitute_compound.py` 를 돌리고 대응 파일끼리 내용 md5 비교:
  ```
  IDENTICAL: Li2O_x020_cLi24gaS16e_s00.xyz   ← x050/x100 과 내용 동일
  … 20/20 전부 IDENTICAL
  x=0.02 n_units: 1 actual_x: 0.25
  x=0.05 n_units: 1 actual_x: 0.25
  x=0.10 n_units: 1 actual_x: 0.25
  ```
· **이미 판정돼 있다**: `kb/methodology/hard_dopant_handling_protocol.md:10` — *"3 농도(x002/x005/x010) actual_x 전부 0.25, 구조/에너지 동일 → 농도시리즈 무효"*. 같은 카드 §가 supercell 을 농도별로 바꾸라고(2,1,1 → 0.125 등) 적어 놓았는데 **`master_batch_273.sh` 는 아직 세 번 다 `1,1,1` 을 넘긴다**(line 318). 판정은 있고 런처에 안 들어왔다.
· **고치는 법**: `master_batch_273.sh` 가 (compound, conc) 마다 supercell 을 골라 `tier_cascade.sh` 4번째 인자로 넘기고, ML feature·CSV 열은 라벨이 아니라 **`actual_x`(구조에서 읽은 값)** 를 쓴다. 그 전까지 농도축 3배는 순수 낭비 — 대략 **193일 중 129일**.

---

## [치명] `--method cluster` 가 존재하지 않는 선택지다 — Stage 01 cluster arm 이 30 캐스케이드에서 통째로 사라진다 (2026-09-09 사고와 **같은 종류**)

· **어디**: 호출 `tools/doping/run_compound_batch.sh:169-175` ↔ 도구 `tools/doping/substitute_compound.py:585-586`
· **무엇**: 러너는 `--method cluster` 를 넘기는데 argparse 는 `choices=['spread','random','first']` 다. rc=2 로 즉사하지만, 그 줄이 `2>&1 | tail -3 || true` 로 감싸여 있어 **파이프 종료코드가 tail(0)** 이라 `set -e` 도 안 걸리고 Stage 01 은 그냥 통과한다. 결과: `typeA_<cmpd>_cluster` 디렉터리가 아예 안 생기고, merge 는 없는 걸 못 세니 구조 수만 조용히 줄어든다. 캐스케이드 로그엔 usage 세 줄만 남는다.
· **영향 범위**: `TYPEA_CLUSTER_COMPOUNDS` = Nd2O3 La2O3 Sm2O3 Al2O3 Sc2O3 Y2O3 B2O3 WO3 MoO3 Cr2O3 → **10종 × 3농도 = 30 캐스케이드**. 하필 논문 1순위(Nd2O3)가 여기 들어 있다.
· **근거**: 실행 결과 그대로 —
  ```
  $ python3 tools/doping/substitute_compound.py … --method cluster …
  rc=2
  substitute_compound.py: error: argument --method: invalid choice: 'cluster'
                          (choose from 'spread', 'random', 'first')
  ```
  같은 명령을 `--method random` 으로 바꾸면 `✓ Generated 10 structures`.
· **고치는 법**: 구현은 **이미 있다** — `substitute_struct.py:99-128` 의 `select_substitution_sites` 가 `'cluster'`(greedy chain growth)를 문서화·구현해 놓았고, 같은 파일의 `--vacancy_method` 는 `cluster` 를 받는다. 즉 `--method` 의 choices 한 줄만 빠졌다 → `choices=['spread','random','first','cluster']`. 그리고 `run_compound_batch.sh` 의 `|| true` / `| tail -3` 이 **rc 를 삼키는 것**을 같이 고쳐야 한다(`PIPESTATUS` 검사하거나 최소한 rc≠0 을 로그에 한 줄 남기기). 안 그러면 다음 것도 또 못 본다.

---

## [치명] `LiCl` · `Li2S` 는 도판트가 아니라 **무결점 원본 그대로**다 — 6 캐스케이드가 pristine host 를 재계산한다

· **어디**: `tools/doping/substitute_compound.py:298-360`(치환 로직) · 화합물 목록 `master_batch_273.sh:118,127`
· **무엇**: 화합물 치환은 cation→cation_site, anion→anion_site 로 넣는다. `LiCl` 을 (Li_24g, Cl_4d) 에 넣으면 Li→Li, Cl→Cl — **아무 일도 안 일어난다.** `Li2S` 를 (Li_*, S_16e) / (Li_*, S_4a) 에 넣어도 같다. 구조가 baseline 과 동일하니 ΔE/atom ≈ 0, dV ≈ 0 으로 필터(수렴·dV<25%·outlier)를 **전부 통과**해 winner 가 되고, anneal→BVSE→EOS→elastic→MD 까지 전부 돌아간 뒤 ML 데이터셋에 *"LiCl 25% 도핑"* 으로 들어간다.
· **근거**: 91종 전부 Stage 01 을 CPU 로 돌려 조성/좌표를 base 와 대조했다.
  ```
  base: {'Li':24,'P':4,'S':20,'Cl':4}
  LiCl   20구조 중 10개가 base 와 같은 조성 (Li_24g/Cl_4d, Li_48h/Cl_4d)
  Li2S   30구조 중 20개가 base 와 같은 조성 (Li_*/S_16e, Li_*/S_4a)
  좌표 대조: max |Δpos| = 4.33e-09 Å, cell 동일  ← 부동소수 왕복 오차뿐
  ```
· **고치는 법**: 치환 후 조성·좌표가 base 와 같으면 그 (cation_site, anion_site) 조합을 버리고 `placement_log` 에 `no_op` 로 남긴다(그룹 자체를 없앤다). LiCl/Li2S 를 목록에서 빼는 건 답이 아니다 — 나머지 조합(Cl→S_4a 등)은 진짜 도핑이다.

---

## [주의] 이번에 넣은 `check_shell_calls()` 가 **Stage 01 도구를 아예 못 본다** — 위 [치명 2] 가 그 증거다

· **어디**: `tools/convention_check.py:226` (`_RE_PYCALL`) ↔ `tools/doping/run_compound_batch.sh:140,169,191,223`
· **무엇**: 정규식이 `python3 tools/….py` 처럼 **경로 리터럴**을 요구한다. 그런데 run_compound_batch 는 `SCRIPT="tools/doping/substitute_compound.py"` 로 잡아 놓고 `python3 "$SCRIPT"` 로 부른다 → 네 군데 호출이 전부 게이트 밖이다. tier_cascade → run_compound_batch 는 셸→셸 호출이라 이것도 안 본다. 게다가 게이트는 **필수 인자 누락만** 보므로 [치명 2] 같은 *choices 불일치*는 원리적으로 못 잡는다.
· **근거**: 게이트가 실제로 해결한 (sh, tool) 쌍을 뽑아 봤다 — tier_cascade 의 13개 도구는 다 잡히는데 `substitute_compound.py resolved anywhere? **False**`. 전체 실행은 `RESULT: 0 위반` 인데 [치명 2] 는 살아 있다. **0 위반은 "그 파일을 봤다"는 뜻이 아니다.**
· **고치는 법**: ① 변수 경유 호출 지원(`SCRIPT=`/`TOOL=` 같은 셸 대입을 파싱하거나, 최소한 `python3 "$VAR"` 를 만나면 **미해결로 보고**해서 침묵하지 않게). ② `choices=[…]` 를 뽑아 셸이 넘기는 리터럴 값과 대조하는 검사 추가 — 이 종류가 오늘 실제로 터진 두 번째 사례다.

---

## [주의] Stage 02 는 구조가 0개여도 **출력 파일을 안 만들고** `STAGE_02.DONE` 을 찍는다 → Stage 03 이 엉뚱한 자리에서 죽는다

· **어디**: `tools/doping/run_uma_screening.py:310-352` (주기 저장이 `for i, struct_meta in enumerate(todo)` **안**에 있다)
· **무엇**: `todo` 가 비면 루프가 한 번도 안 돌아 `uma_results.json` 이 **한 번도 써지지 않는다**. 그런데 스크립트는 exit 0 → `STAGE()` 가 DONE 마커를 찍는다. 다음 Stage 03 이 `--results …/uma_results.json` 를 열다 FileNotFoundError 로 죽는다. 재개하면 Stage 02 는 DONE 이라 건너뛰므로 **영원히 Stage 03 에서 죽는다**(rm 하기 전까지). `todo` 가 비는 경로는 실재한다 — Stage 01 이 구조 0개를 만들어도(치환 불가·site 필터 전멸) 러너가 `|| true` 로 삼키고 merge 가 `n_structures: 0` 으로 정상 종료한다.
· **또**: 개별 구조가 전부 예외로 실패해도 `failed` 에만 쌓이고 **exit 0** 이다(:341-346). 273개 중 하나가 이렇게 되면 빈 결과로 통과한다.
· **근거**: 코드 읽기로만 판정. 이 상자엔 `fairchem` 이 없어(`ModuleNotFoundError: No module named 'fairchem'`) **실행 확인은 못 했다.**
· **고치는 법**: `todo` 계산 직후 무조건 한 번 저장(빈 results 라도), 그리고 `len(failed) > 0 and len(results) == 0` 이면 비영 종료.

---

## [주의] Stage 00 preflight 는 **지금 돌리는 화합물을 검사하지 않는다** (그리고 `--device` 를 무시한다)

· **어디**: `tools/doping/preflight.py:197-201, 104, 267-278`
· **무엇**: ① positive control 이 `Nd2O3 / MgO / Al2O3` 로 **하드코딩**돼 있다. `COMPOUND_FILTER`·`X_COMPOUND` 를 안 읽으므로, 예컨대 As2S3 의 `ALTERNATIVE_VALENCES` 누락 같은 화합물별 결함은 preflight 를 **통과한 뒤** Stage 01 에서 조용히 0개를 낸다. 273번 도는 preflight 가 매번 같은 세 산화물만 본다. ② `check_baseline_relax` 는 `calc=None` 으로 불려서 line 104 의 `device='cuda'` **하드코딩**을 쓴다 — `--device cpu` 로 돌려도 GPU 를 잡는다(gabia/kgy 공유 규칙과 충돌). ③ UMA predictor 를 세 번 따로 로드한다(`check_uma_load` / `check_baseline_relax` / `check_positive_controls`). **VRAM 실측은 못 했다**(GPU 없음) — 코드상 지적이다. ④ `n_pass != n_total` 이면 exit 1 → 캐스케이드 abort. 디스크 임계가 상수 5 GB 라(`:60`), 273개가 쌓여 여유가 5 GB 밑으로 내려가는 순간부터 **남은 전부가 Stage 00 에서 즉사**한다.
· **고치는 법**: preflight 에 `--compound`/`--x_compound` 를 받아 실제 대상 화합물 1종을 positive control 에 넣는다(그게 preflight 다). `check_baseline_relax(base, device=args.device)` 로 device 전달. calc 를 한 번 만들어 세 검사에 넘긴다. 디스크 임계는 남은 캐스케이드 수 기반으로.

---

## [주의] Type C 는 `EXOTIC=0` 을 **cation 쪽에서 우회**한다 — 33 캐스케이드

· **어디**: `tools/doping/run_compound_batch.sh:223-229` (`--auto_cation_sites` 를 안 넘긴다) ↔ `substitute_compound.py:631-651` (site_preference 사전필터가 `if args.auto_cation_sites:` 안에만 있다)
· **무엇**: Type C 는 `--auto_anion_sites` 만 넘기므로 cation 은 기본값 `Li_24g` 로 고정되고, 그 경로에선 **문헌 site 필터가 아예 안 돌아간다**. 캐스케이드는 `EXOTIC=0`("문헌 필터 적용")로 뜨는데 Type C 구조만 필터 밖이다.
· **근거**: 실행 대조 (WO3) —
  ```
  Type A (--auto_cation_sites): cation sites used: ['P_4b']      ← 필터가 고른 자리
  Type C (자동 없음)          : cation sites used: ['Li_24g']    ← W⁶⁺ 를 Li⁺ 자리에, 필터 없이 10구조 생성
  ```
  `TYPEC_COMPOUNDS ∩ 91종` = Al2O3 Sc2O3 Y2O3 La2O3 Nd2O3 MgO ZnO WO3 MoO3 B2O3 Sm2O3 → **11종 × 3농도 = 33 캐스케이드**.
· **주의**: `substitute_compound.py` 의 docstring 은 "명시적 단일 site 요청은 일부러 그대로 둔다" 고 적어 놓았다 — 도구 쪽은 의도적이다. **깨진 건 캐스케이드 수준의 약속**이다. 고치려면 Type C 호출에 `--auto_cation_sites` 를 넣거나, `EXOTIC=0` 일 때 명시 site 도 필터에 통과시키거나, 최소한 로그에 "Type C 는 cation 필터 미적용" 을 남긴다.

---

## [주의] 16개 화합물은 winner 그룹이 **하나뿐**이다 — Stage 03 필터에 걸리면 Stage 04 가 abort

· **어디**: `tools/doping/select_winners.py:274-285` ↔ `tools/doping/run_anneal.py:352-370`
· **무엇**: Stage 03 은 `(dopant, site, anion_site_label)` 그룹당 1등만 남긴다. 91종을 실제로 돌려 보니 그룹 수가 화합물마다 1~6개다. **그룹이 1개인 16종**(구조 5개가 전부):
  `AlF3 AlI3 AlN Ca3N2 CaF2 GaN LaF3 Mg3N2 MgF2 MgI2 NbCl5 NdF3 ScF3 TaCl5 TiF4 YF3`
  이 5개가 `--require_converged` 나 `--max_dv 0.25` 에 전부 걸리면 `winners: []` 로 **정상 종료**하고(Stage 03 OK, DONE), Stage 04 가 `raise SystemExit("No xyz files found")` 로 죽는다 → 48 캐스케이드가 Stage 04 에서 실패할 수 있다. (죽는 건 시끄럽지만, **원인이 Stage 03 에 있는데 Stage 04 로그에 나온다** — 오늘 사고와 같은 진단 혼선.)
· **덤**: 그룹 크기가 5~30 으로 6배 차이 난다. `select_winners.py:250` 이 스스로 적어 놓은 best-of-N 편향(후보 많은 쪽이 챔피언도 좋다, r=+0.321)이 화합물 간 비교에 그대로 들어간다. `--fixed_n` 은 있는데 캐스케이드는 안 쓴다.
· **고치는 법**: Stage 03 이 `winners == []` 이면 비영 종료 + 왜 비었는지(수렴 몇/dV 몇) 한 줄. 화합물 간 순위를 쓸 거면 `--fixed_n` 을 켜거나 최소한 `--diagnose_best_of_n` 를 캐스케이드에 넣는다.

---

## [주의] master 의 "running" 판정(최근 30분 파일)이 **방금 죽은 캐스케이드를 건너뛴다**

· **어디**: `tools/doping/master_batch_273.sh:165-172, 305-307`
· **무엇**: `cascade_status()` Layer 3 이 `find "$outdir" -type f -mmin -30` 하나만 걸리면 "running" 으로 보고 **그 캐스케이드를 통째로 건너뛴다**. 그런데 master 는 실행 직전에 `mkdir -p "$OUT"; echo $$ > "$OUT/.master_lock"` 로 파일을 만든다(:306-307). 캐스케이드가 빨리 죽으면(오늘처럼 37분 뒤 Stage 04 에서 rc=2) 그 디렉터리는 방금 수정된 상태다 → **30분 안에 재실행하면 그 화합물들이 "running" 으로 조용히 스킵**된다. `.master_lock` 은 캐스케이드가 끝나도 **지우지 않는다**(Layer 4 는 PID 생존만 본다).
· **근거**: 코드 읽기. 실행 확인 못 함(273 배치를 돌릴 수 없음).
· **고치는 법**: 캐스케이드 종료 시 `.master_lock` 제거(trap). Layer 3 은 로그 파일 mtime 이 아니라 **살아 있는 PID** 로 판정한다(Layer 4·5 가 이미 그 일을 한다 — Layer 3 은 겹치면서 더 위험하다).

---

## [참고] `xyz_file` 이 절대경로다 — 일부만 사라지면 조용히 줄어든다

· **어디**: `substitute_compound.py` 가 `xyz_file` 을 절대경로로 기록(실측: `/tmp/…/x0.05/Li2O_x050_….xyz`) ↔ `run_anneal.py:352-353`
· **무엇**: Stage 04 는 `if 'xyz_file' in r and Path(r['xyz_file']).exists()` 로 **존재하지 않는 경로를 경고 없이 버린다**. 전부 없으면 `SystemExit` 로 시끄럽게 죽지만, **일부만** 없으면(디렉터리 일부 이동·정리·기계 간 복사) winner 몇 개가 조용히 사라지고 나머지로 진행한다. 바로 아래 `--top_candidates` 분기(:363-365)는 같은 상황에서 `⚠ skip` 을 찍는다 — 두 분기의 규약이 다르다.
· **고치는 법**: summary 분기에도 skip 경고 + `len(recs) != len(xyz_paths)` 면 비영 종료(또는 최소한 결과 json 에 기록).

## [참고] `method`(random/cluster)가 group key 에 없어서 두 방법이 같은 그룹으로 합쳐진다

· **어디**: `tier_cascade.sh:163-168` (`--group_by dopant site anion_site_label`)
· **무엇**: typeA(random)와 typeA_cluster 는 dopant·site 가 같으므로 **한 그룹**이 되어 1등 하나만 남는다 — "precursor local-coord biased" 라는 cluster arm 의 구분이 순위에서 사라지고, 그룹 크기만 커져 best-of-N 편향이 커진다. 지금은 [치명 2] 때문에 cluster 가 아예 안 생겨 발현하지 않는다. **[치명 2] 를 고치면 이게 드러난다** — 같이 결정해야 한다(group key 에 method 추가할지, 합치는 게 의도인지).

---

## 못 본 것 — 무엇을 안 읽었고 왜

- **UMA/GPU 가 필요한 것은 하나도 실행하지 못했다.** 이 상자에 `fairchem` 이 없다(`ModuleNotFoundError: No module named 'fairchem'`). 그래서 **Stage 00 preflight 와 Stage 02 screening 은 코드 읽기로만 판정**했다 — 실제 수렴률, `--steps 1500` 에서 몇 개가 `converged=True` 가 되는지, 따라서 Stage 03 에서 winners 가 실제로 비는지 **확인 못 했다**. [주의] 항목 두 개(Stage 02 빈 출력, 16종 단일그룹)는 실측이 아니라 추론이다.
- **`site_preference.py` 본문을 안 읽었다** (`DOPANT_DB`, `site_preference_filter`, `LITERATURE_SITES`). 실행으로 결과만 봤다 — 어떤 화합물이 어느 site 를 허용하는지는 확인했지만, **그 화학 판정이 옳은지는 검증하지 않았다.**
- **`substitute_struct.py`(610줄)는 `select_substitution_sites` 의 docstring 만** 읽었다. `find_host_indices_for_site` 의 site 라벨링(24g vs 48h 구분)이 정확한지 **확인 못 했다** — 이게 틀리면 group key 가 전부 틀린다.
- **`substitute_compound.py` 는 300–500행(Type B/B'/C/D 실제 치환·공극 배치)을 안 읽었다.** Type A 경로와 argparse·main 만 읽었다. Type C 는 실행 결과로만 판단했다.
- **`_provenance.py` · `stage_report.py` 안 읽음.** stage_report 는 `2>/dev/null || true` 로 완전히 무음이라 실패해도 아무 영향이 없다(그래서 우선순위를 낮췄다).
- **`run_anneal.py` 는 입력선택 블록(:326-410)과 argparse 만** 읽었다. MD·relax 본체(:78-250)는 안 읽었다 — 내 구간이 아니고, 03→04 계약 확인에 필요한 부분만 봤다.
- **resume 경로를 실행으로 시험하지 않았다** (`STAGE_*.DONE`, `CASCADE_VERSION`, `cascade_status()` 5계층). 273 배치를 돌릴 수 없다.
- **Stage 05–12 는 손대지 않았다** (다른 구간 담당).
- 91종 Stage 01 실행은 **typeA(`--method random`, x=0.05, 1,1,1) 만** 돌렸다. typeA_cluster 는 [치명 2] 때문에 돌지 않고, typeC 는 WO3 하나만 돌렸다. **나머지 10종의 typeC 는 확인 못 했다.**

---

## Stage 04–07

감사 끝났다. 실행으로 확인한 것과 못 본 것을 나눠서 적는다.

---

# Stage 04–06 감사 결과

## 먼저 — 이번에 죽은 자리는 실제로 막혔다 (실행 확인)

Stage 04 의 정확한 argv 를 그대로 돌려봤다 (device 만 cpu):

```
python3 tools/doping/run_anneal.py --summary_json <OUT>/03_winners/winners.json \
    --out <OUT>/04_anneal --seed 20260830 --device cpu
→ rc=1, ModuleNotFoundError: No module named 'fairchem'   (load_uma_calc, line 54)
```

argparse 를 통과했고, winners.json 을 읽어 xyz 를 찾았고, UMA 로딩 직전까지 갔다.
즉 `--seed` 계약도 `--summary_json` 스키마도 지금은 맞는다. (fairchem 은 이 컨테이너에 없다.)

그리고 **`--seed` 가 진짜로 궤적에 닿는지**를 EMT(CPU)로 실측했다 — 이게 회신 AL 해제조건 #2 의 핵심이라 소스 grep 으로 끝내지 않았다:

```
전역 np.random.seed() 를 매번 다르게 흔들어 놓고 anneal_one() 을 3번 호출
seed 7 (a): post_md hash 964ea4d1e8d499e6   E_md 1.3688412973321
seed 7 (b): post_md hash 964ea4d1e8d499e6   E_md 1.3688412973321   ← 비트 동일
seed 8 (a): post_md hash 1b0bbad38dbf26b7   E_md 1.781595597542653 ← 갈라짐
seed 기록: 7, rng_streams {'velocities': 7, 'langevin': 1000010}
```

· 전역 numpy 상태를 안 쓴다 ✔ (ASE 3.29 `_maxwellboltzmanndistribution` / `Langevin.step` 둘 다 `rng.standard_normal` 을 호출하고, 넘긴 Generator 를 쓴다 — 소스로 확인)
· 두 스트림이 겹치지 않는다 ✔ (velocity 시드 ≤ base+65535, langevin 시드 ≥ base+1000003)
· seed 가 결과 레코드에 남는다 ✔

**이 축은 통과다.** 아래는 그 다음에 발견한 것들.

---

## [치명] Stage 04 가 전멸해도 rc=0 → Stage 05 가 미완화 구조로 조용히 갈아탄다

· **어디**: `tools/doping/run_anneal.py:425-445` + `tools/doping/tier_cascade.sh:203-219`

· **무엇**: 이번 사고와 **정반대 모양**의 같은 병이다. 이번엔 즉사해서 열흘 만에 들켰지만, 이 경로는 **안 죽는다**.

```python
# run_anneal.py:425
try:
    rec = anneal_one(...)
    results.append(rec)
except Exception as e:
    print(f"  ❌ FAILED: {e}")
    results.append({'name': ..., 'xyz_input': ..., 'error': str(e)})
```

구조 하나가 죽으면 error 레코드로 삼키고 넘어간다. 전부 죽어도 마찬가지다. `main()` 은 실패 개수를 세지도, 비영 코드로 끝내지도 않는다 → **rc=0 → `STAGE 04 anneal: OK` → `STAGE_04.DONE`**.

그러면 Stage 05 가 이렇게 받는다:

```bash
# tier_cascade.sh:205
xyzs=$(ls "$OUT"/04_anneal/*/post_relax.xyz 2>/dev/null)
if [ -z "$xyzs" ]; then
    echo "  No post_relax.xyz files; falling back to initial structures"
    xyzs_dir="$OUT/01_structures/structures"          # ← 미완화 원본
    python3 tools/doping/bvse_proxy.py --xyz_dir "$xyzs_dir" ...
```

바로 위 200-202 줄이 **왜 이러면 안 되는지**를 직접 적어 놓았다:

```
# Stage 05 — BVSE on post-anneal (relaxed) geometry, not the pre-relax input.
#   External review CR-3: BVS depends exponentially on bond length, so the
#   un-relaxed substitute-compound output gave artificial distances.
```

즉 외부 리뷰가 명시적으로 금지한 그 계산을, 폴백이 **한 줄 echo 만 남기고 rc=0 으로 수행**한다. `anneal_one` 은 `work.mkdir()` 을 맨 앞에서 하고 그 뒤 `get_potential_energy()` 에서 죽으므로, 디렉터리는 생기고 `post_relax.xyz` 만 없다 → 글롭이 정확히 비어 폴백이 발동한다.

가장 그럴듯한 발동 조건이 CLAUDE.md 에 이미 적혀 있다 — **"gabia: pw.x와 UMA 동시 실행 금지 (VRAM 47/48 GB 점유 사례)"**. `--device cuda` 가 하드코딩(`tier_cascade.sh:198`)이고 CPU 폴백이 없어서, pw.x 가 VRAM 을 잡고 있으면 `torch.cuda.OutOfMemoryError`(→ RuntimeError → Exception)가 구조마다 터지고 전부 삼켜진다. `load_uma_calc` 은 try 밖이라 **완전 불가**면 크게 죽지만, **간헐 OOM** 은 조용히 통과한다.

· **더 나쁜 것 — resume 이 실패를 "완료"로 본다**:

```python
# run_anneal.py:411-419
done = {r['name']: r for r in existing.get('results', [])}   # error 레코드 포함
todo = [p for p in xyz_paths if winner_name(p) not in done]
```

error 레코드도 `done` 에 들어간다. 다시 돌려도 **영원히 재시도 안 한다.** 게다가 `todo` 가 비면 루프가 안 돌아 rc=0 → 두 번째 실행에서도 Stage 04 는 즉시 "OK". 3개월 배치에서 이건 복구 불가능한 누적 손실이다.

· **고치는 법**:
  1. `run_anneal.py` 끝에 `n_err = sum('error' in r for r in results)` 를 세고, `n_err / len(results)` 가 문턱(예: 0)을 넘으면 **비영으로 끝낸다**. 최소한 전멸(`n_ok == 0`)은 무조건 rc≠0.
  2. resume 의 `done` 에서 **error 레코드를 뺀다** (`if 'error' not in r`). 영구 실패는 별도 `--skip_failed` 로 명시.
  3. Stage 05 폴백을 **기본 금지**로 바꾼다. 폴백이 필요하면 `BVSE_ALLOW_UNRELAXED=1` 을 명시적으로 요구하고, 안 켜져 있으면 `exit 1`. 지금은 리뷰가 금지한 계산이 기본값이다.
  4. 폴백으로 돌았으면 `bvs_report.json` 최상위에 `geometry_source: "unrelaxed_stage01"` 를 박는다. (지금은 레코드별 `'xyz'` 경로로만 사후 추적 가능 — 있긴 하지만 요약 어디에도 안 드러난다.)

---

## [치명] Stage 06 은 조인이 0 건이어도 rc=0 으로 빈 랭킹을 쓴다 (실행 확인)

· **어디**: `tools/doping/rank_anneal.py:44-73, 100-108`

· **무엇**: `rank_anneal.py` 는 screening 의 `name` 과 anneal 의 `name` 을 **교집합**으로 조인한다. 교집합이 비면 조용히 빈 파일을 쓰고 성공으로 끝난다. 실제로 이름이 하나도 안 겹치게 만들어 돌려봤다:

```
--- Stage06 argv, ZERO name overlap: rc=0
   ✓ 0 structures joined → .../06_rerank/post_anneal_ranking.json
   -> n_joined: 0 | ranked: 0
```

그리고 `06_rerank/post_anneal_ranking.json` 은 **Stage 09e·09f·10·11 네 개의 유일한 입력**이다 (전부 `ranking.get('ranked_by_post_anneal', [])[:top]` 로 읽는다 — `run_md_sigma.py:290`, `ehull_check.py:114`, `esw_check.py:72`, `run_cathode_interface.py:243` 실물 확인). 빈 리스트가 오면 네 스테이지 모두 **아무것도 안 하고 DONE 마커를 찍는다.**

캐스케이드는 끝까지 "성공"으로 완주하고, `FINAL_RANKING.json` 은 나오지만 σ_Li 도 W_ad 도 e_hull 도 없다. 273개 × 3개월 뒤에 발견하는 종류다.

· 참고: 지금 이름은 실제로 맞는다 — `substitute_compound.py:795` 가 `xyz_path = out_dir / f'{name}.xyz'` 로 쓰고, `winner_name()` 이 stem 을 돌려주므로 `name == stem` 이다 (코드로 확인). 문제는 "지금 맞다"가 아니라 **틀어져도 안 들킨다**는 것이다.

· **고치는 법**: `rank_anneal.py` 에서 `n_joined == 0` 이면 `raise SystemExit(2)`. 그리고 조인 손실률(`len(joined) / len(post_by_name)`)이 문턱 미만이면 경고가 아니라 실패로 처리. 같은 게이트를 `combine_rankings.py` 에도.

---

## [주의] Li–anion BVS 파라미터가 저장소에 두 벌 있고, 캐스케이드 쪽이 comp1_v3 정본과 다르다

· **어디**: `tools/doping/bvse_proxy.py:49-58` vs `tools/comp1_v3/compute_bvse_map.py:26-27`

· **무엇**: CLAUDE.md 정본(softBV)은 `S 2.105 / Cl 2.249 / O 1.466, b=0.37`. `comp1_v3` 세 파일 모두 그 값이다. 그런데 3개월을 돌릴 캐스케이드의 Stage 05 는 다른 값을 쓴다:

```python
# bvse_proxy.py:49
'S':  {'R0': 1.94,  'b': 0.40},   # Adams 2003 Li-S
'Cl': {'R0': 1.91,  'b': 0.37},
'O':  {'R0': 1.466, 'b': 0.37},   # ← O 만 일치
```

실제 argyrodite(`db/structures/comp1_V0_k444.xyz`, 52 atoms)로 양쪽을 돌려 차이를 쟀다:

```
                        캐스케이드(1.94/1.91)   정본 softBV(2.105/2.249)
migration_volume_fraction      0.1179                0.0250      ← 4.7×
bvs_li_mean                    1.033                 1.625
bvs_li_proxy_score             0.919                 0.369       ← 2.5×
li_mobility_score (3f+p)       1.273                 0.444       ← 2.9×
```

`li_mobility_score` 는 `combine_rankings` 에서 이동도 축 30% 를 차지한다(`bvse_proxy.py:406` 주석). 파라미터 한 줄이 그 축을 3배 흔든다.

· **다만 어느 쪽이 맞는지 나는 판정 못 했다.** 캐스케이드 값이 Li 의 BVS 를 1.03(이상값 1.0 근처)으로 주고 정본 softBV 는 1.63 을 준다 — 오히려 캐스케이드 쪽이 자기정합적으로 보인다. comp1_v3 가 Morse 형/스크리닝을 쓰는지 아닌지 확인 안 했다. CLAUDE.md 의 규약은 문언상 `tools/comp1_v3/` 에 스코프돼 있기도 하다.

· **고치는 법**: 던지기 전에 1저자가 **어느 파라미터 셋이 캐스케이드 정본인지 한 줄로 못박는다.** 그리고 `tools/convention_check.py` 에 R0/b 체크를 추가한다 — 지금 이 도구는 kB 만 보고 **BVS R0 를 전혀 안 본다**(`grep -n "R0\|BVS" tools/convention_check.py` → `def check_shell_calls` 한 줄만 매치). 규약이 kb 에 있는데 기계가 안 보는 상태다.

---

## [주의] migration_volume_fraction 은 고정 복셀이 아니라 고정 격자수라 셀 크기가 다르면 비교가 안 된다

· **어디**: `tools/doping/bvse_proxy.py:98-101`

· **무엇**: `one = np.linspace(0, 1, n_grid, endpoint=False)` — **분율 좌표에 n_grid 개**를 깐다. 그래서 복셀 변이 셀 길이에 비례해 늘어난다. 실측: comp1(a=10.06 Å) @ grid 25 → **0.402 Å 복셀**. CLAUDE.md 의 BVSE 규약(~0.25 Å 복셀)과도 다르고, Stage 03 이 `--max_dv 0.25` 로 부피 ±25% 를 통과시키므로 같은 배치 안에서 복셀 변이 ~8% 흔들린다. `SUPERCELL` 인자를 바꾸면 훨씬 크게 벌어진다.

임계 창 `[0.8, 1.2]` 위의 점 개수 비율이라 해상도에 직접 민감하다. 순위 지표로 쓰는 이상, **부피가 다른 후보끼리의 비교에 해상도 편향이 실린다.**

· **고치는 법**: `n_grid` 대신 목표 복셀 크기(`--voxel_A`)를 받아 축마다 `ceil(L_i / voxel)` 로 잡는다. 레코드에 실제 복셀 변을 기록해서 사후 검증 가능하게.

## [주의] anneal_results.json 이 재현에 필요한 인자를 다 안 남긴다

· **어디**: `run_anneal.py:448-454` (최상위) / `169-200` (레코드)

· **무엇**: 최상위에 `temperature_K`, `time_ps`, `n_done` 만 있다. **base `--seed` 가 없다** (레코드의 파생 시드에서 `seed - crc32(name)&0xFFFF` 로 역산은 되지만 도출식을 알아야 한다). 레코드에도 `friction`, `relax_fmax`, `no_cell_relax` 가 없다. `--light` 여부는 T/t 가 300/20 으로 찍히니 간접 추론만 된다.

· 재현이 이 스테이지의 존재 이유인데(회신 AL P0-3), 시드만 남기고 나머지 MD 조건은 안 남긴다.

· **고치는 법**: 최상위에 `args.__dict__` 를 통째로 (또는 `base_seed`, `friction`, `relax_fmax`, `cell_relax`, `light`) 넣는다.

## [주의] resume 이 seed 를 대조하지 않아 한 파일 안에서 시드가 섞인다

· **어디**: `run_anneal.py:411-419`

· **무엇**: `done` 판정이 `name` 만 본다. `ANNEAL_SEED` 를 바꿔 재실행하면 기존 구조는 옛 시드 결과를 유지하고 새 구조만 새 시드로 돌아, 하나의 `anneal_results.json` 안에 **두 base seed 가 섞인다.** 아무 경고도 없다.

· **고치는 법**: 최상위에 `base_seed` 를 쓰고(위 항목), resume 시 현재 `--seed` 와 다르면 중단하거나 명시적 `--allow_seed_change` 요구.

---

## [참고] 그 밖

1. **crc16 시드 충돌** — `run_anneal.py:439` `zlib.crc32(name) & 0xFFFF` 는 65536 공간이다. 임의 이름 2000개로 실측: **34개 구조가 시드를 공유한다.** 서로 다른 계라 대개 무해하지만 "구조마다 다른 시드" 라는 주석의 주장은 완전하지 않다. `& 0xFFFFFF` 로 넓히면 끝.

2. **`bvse_proxy.py:115` `tree.query(cart, k=25, ...)`** — 5.0 Å 안 음이온이 25개를 넘으면 **경고 없이 잘린다.** comp1 밀도로는 ~13개라 지금은 안전하지만(계산으로 확인), O 를 넣는 계열에서 넘을 수 있다. `k` 포화 여부를 세서 경고를 찍어야 한다.

3. **`bvse_proxy.py:276` `--out` 이 required 가 아니다.** 비-backfill 경로에서 `out = Path(args.out)` 이 `Path(None)` → TypeError. 캐스케이드는 항상 넘기니 지금은 안 터진다.

4. **`tier_cascade.sh:205, 216` 의 `--xyz $xyzs` 비인용** — `$OUT` 에 공백이나 글롭 문자가 있으면 조용히 잘못된 파일 목록이 된다. 현재 `$OUT` 은 `$BATCH_DIR/$cmp_label` 이라 공백이 없다(확인). 방어만 해두면 된다.

5. **`run_anneal.py:204-250` 의 `--selftest` 는 소스 문자열 grep 이다.** `"rng=rng_v" in src`, `src.count("default_rng") == 2` — **시드가 궤적을 실제로 바꾸는지는 안 본다.** 이번 사고의 교훈("헤더/문자열이 아니라 본문·거동") 이 이 selftest 자체에도 걸린다. (그래서 내가 위에서 EMT 로 대신 재봤고, 통과했다.) 결정론 회귀시험을 selftest 에 넣는 게 맞다 — EMT + 8원자면 1초다.

6. **`STAGE()` 의 rc 포착은 정확하다** — 실측으로 확인:
   ```
   f(){ ... python3 -c "sys.exit(7)" 2>&1 | tee /dev/null; local s=${PIPESTATUS[0]}; ...}
   → captured=7
   set -e; A=""; [ "${M:-real}" = "light" ] && A="--light"   → 종료 안 함, A=[]
   ```
   `ANNEAL_MODE=light` 분기(`tier_cascade.sh:182-183`)는 살아 있고 `set -e` 에 안 걸린다. `run_anneal.py:290` 에 `--light` 플래그도 실재한다.

---

## 확인해서 "맞다" 고 말할 수 있는 것

| 항목 | 어떻게 확인했나 |
|---|---|
| `--seed` → Langevin·초기속도 RNG 도달, 전역 numpy 미사용 | EMT 로 anneal_one 3회 실행, 해시 대조 |
| seed 가 결과 json 에 기록 | 실행 결과 dict 확인 |
| Stage 04 argv ↔ run_anneal argparse | 실제 argv 실행 (fairchem 직전까지 통과) |
| `winners.json` `{'winners':[...]}` + `xyz_file` ↔ `--summary_json` 파서 | select_winners.py:292-298 실물 + 실행 |
| `04_anneal/<name>/post_relax.xyz` ↔ 05·07·08 글롭 | 레이아웃 재현 후 glob 매치 확인, `winner_name` 이 부모 디렉터리명 반환 확인 |
| 06 출력 키 `ranked_by_post_anneal` ↔ 소비자 5곳 | 다섯 파일 grep 실물 대조 |
| `rank_anneal` 이 쓰는 `baseline_e_per_atom` 존재 | run_uma_screening.py:331 |
| `X_COMPOUND` 전파 | run_compound_batch.sh:42,142,171,225 |
| `convention_check.py` 0 위반 | 실행 (셸 러너 필수 인자 누락 0) |
| `--selftest` 3종 통과 | run_anneal / bvse_proxy 실행 |

---

## 못 본 것 — 무엇을 안 읽었고 왜

1. **UMA 로 실제 anneal 을 못 돌렸다.** 이 컨테이너에 `fairchem` 이 없고(`ModuleNotFoundError`), GPU 실행 금지 지시가 있었다. `anneal_one` 의 결정론은 **EMT 대체 계산기**로 검증했다. 따라서 UMA 고유의 비결정성(GPU 커널, TF32, 배치 순서)은 **검증 안 됐다** — run_anneal 자신의 docstring 도 "seed 는 필요조건이지 충분조건이 아니다" 라고 적어 놓았고, 나는 그 충분조건 쪽을 못 봤다.

2. **GPU OOM 시나리오는 코드 경로 추론이다, 실측이 아니다.** "pw.x 와 겹치면 구조마다 예외 → 전부 error 레코드 → rc=0" 은 `except Exception` 이 `torch.cuda.OutOfMemoryError` 를 잡는다는 타입 관계와 `work.mkdir()` 위치로부터 유도했다. 실제로 OOM 을 재현하지 않았다.

3. **`bvse_proxy.py` 의 `compute_bvs_per_li()` 본문을 안 읽었다.** 함수를 **실행**해서 출력(`bvs_li_mean/std/min/max/proxy_score`)은 봤지만, 이웃 선택·컷오프·Li 판별 로직은 안 봤다. 위 파라미터 비교표의 `bvs_li_*` 는 블랙박스 실행 결과다.

4. **전체를 읽은 파일은 4개뿐**이다 — `run_anneal.py`(473줄, 전체), `tier_cascade.sh`(416줄, 전체), `rank_anneal.py`(113줄, 전체), `bvse_proxy.py`(main + compute_migration_volume + 헤더, **약 250/500줄**). `select_winners.py`·`run_uma_screening.py`·`substitute_compound.py`·`run_compound_batch.sh`·`master_batch_273.sh` 는 **스키마 관련 부분만 grep + 부분 읽기**로 봤다. 이 파일들 안에 이번 종류의 계약 파손이 더 있는지는 **확인 못 함**.

5. **Stage 00–03 · 07–12 는 내 구간이 아니라 안 봤다.** 다만 Stage 05 폴백이 참조하는 `01_structures/structures/` 레이아웃만 `run_compound_batch.sh:258` 글롭으로 **코드상 확인**했고, 실제 디렉터리로 확인하지는 못했다(저장소에 과거 cascade 출력이 하나도 없다 — `find runs -name "anneal_results.json"` → 0건).

6. **과거 실측 출력과 대조 못 했다.** `runs/tier_*` 디렉터리가 저장소에 없어서, "실제로 이 경로가 발동한 적이 있나"(예: 폴백으로 돈 bvs_report 가 있나)를 확인할 수 없었다. 원격 서버의 `runs/` 를 보면 답이 나올 것이다 — **폴백 발동 흔적 조회를 부모 세션에 권한다**: `grep -rl "falling back to initial structures" <runs>/*/logs/05_bvse.log`.

7. **BVS 파라미터 두 벌 중 어느 쪽이 물리적으로 옳은지 판정 안 했다.** 차이의 크기만 쟀다. comp1_v3 의 BVSE 형식(Morse 여부·스크리닝·컷오프)을 안 읽었기 때문이다.

---

## Stage 08–12

Stage 07–09f 감사 결과 (읽기 전용, 파일 수정 없음). 모든 도구의 **본문 전체**를 읽었고, 합성 캐스케이드를 만들어 09a→09b→09c→09d 를 **실제로 실행**했다.

---

## [치명] Stage 09d — DFT 입력이 **0개** 만들어지고 rc=0 으로 통과한다

· **어디**: `tools/doping/generate_dft_inputs.py:832-841` ↔ `tools/doping/combine_rankings.py:142-176, 492`
· **무엇**: 조용히 틀린다. 09d 는 `FINAL_RANKING.json` 의 각 row 에서 xyz 경로를 찾는데,
  `combine_rankings.py` 가 만드는 row 에는 **xyz 경로 필드가 아예 없다.** 전 항목이
  `failed: no xyz found` 로 떨어지고, `dft_input_summary.json` 만 쓴 뒤 **exit 0** →
  `STAGE_09d.DONE` 이 찍힌다. 273개 전부가 "DFT 입력 준비 완료" 로 보이면서 실제 입력은 0개.
· **근거**: 합성 캐스케이드 실행 실측 —
  ```
  ⚠ C_x001: no xyz available   ⚠ B_x001: ...   ⚠ A_x001: ...
  ✓ Generated 0 DFT inputs (0 skipped, 3 failed)      rc=0
  $ ls .../dft2 →  dft_input_summary.json   (그것뿐)
  ```
  코드:
  ```python
  xyz_candidates = [row.get('xyz_input'), row.get('xyz_file'),
                    row.get('_anneal', {}).get('post_relax_xyz')]
  ```
  그런데 `load_rows()` Pass 2 가 만드는 row 키 전부(실측):
  `B0_GPa, B_hill_GPa, E_young_GPa, G_hill_GPa, V0_per_atom, bvs_li_proxy, dV_over_V0,
  de_per_atom_post_anneal, de_per_atom_screen, delta_E_anneal_meV, dopant_blocking_frac,
  li_li_disorder_std, li_mobility_score, migration_volume_pct, name, poisson_nu, pugh_ratio,
  score_*` — **xyz 없음.**
  ★ 이건 가설이 아니다. `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md:496` 이
  실제 270개 캠페인에서 같은 것을 이미 관측해 놓았다: *"`dft_inputs/` 270개 =
  `dft_input_summary.json` 뿐 (**실제 입력 없음**)"*. Stage 04 사고와 완전히 같은 종류인데,
  **죽지도 않아서** 열흘이 아니라 넉 달을 몰랐다.
· **고치는 법**: 둘 중 하나. (a) `combine_rankings.load_rows()` Pass 2 에 
  `row['post_relax_xyz'] = blob['_anneal'].get('post_relax_xyz')` 를 넣는다
  (`collect_dataset.py` 는 이미 이 필드를 CSV 로 내보내고 있으니 값은 존재한다).
  (b) `generate_dft_inputs.py` 에 `--anneal_dir` 를 추가해 `<anneal_dir>/<name>/post_relax.xyz`
  로 폴백. **그리고 `len(generated)==0` 이면 비영 종료**로 바꾼다 — 지금은 전멸이 성공이다.

## [치명] Stage 09a — 축 하나만 "죽어도" rc=2 로 캐스케이드가 abort 한다 (구조 1개면 100%)

· **어디**: `tools/doping/combine_rankings.py:772` (`return 2 if n_dead else 0`), 판정은 77-78행
· **무엇**: 즉사. `normalize()` 는 전 행 동일값이면 `state="constant"` → 죽은 축으로 세고,
  `main()` 이 그 수만큼 **rc=2** 를 낸다. `tier_cascade.sh:116-119` 는 비영이면 abort →
  **09b·09c·09d·09e·09f·10·11·12 가 통째로 안 돈다.** 승자가 1개뿐인 캐스케이드는
  모든 축이 자동으로 "동일값"이라 **반드시** 걸린다.
· **근거**: 승자 1개 픽스처 실측 —
  ```
  rc=2
  ⛔ stability 1/1 (100.0%) — 전 행 동일값 → 0.5 상수 · 가중치 0.4
  ⛔ modulus   1/1 ...   ⛔ mobility  1/1 ...
  ```
  승자 3개·값이 서로 다른 픽스처에서는 rc=0 (정상). `master_batch_273.sh:321-327` 은
  rc≠0 이면 "❌ FAIL → next" 로 넘어가므로, 273개가 00–08 만 남기고 09 이후가 전부 빈다.
· **고치는 법**: 죽은 축은 **경고이지 실패가 아니다** — 종료코드를 분리한다
  (예: `--strict_axes` 를 준 경우에만 2, 기본은 0 + payload 에 `axis_health` 기록).
  최소한 `len(measured) < 2` 로 인한 constant 는 별도 사유로 구분해야 한다.

## [치명] Stage 05 의 BVSE 축이 신선한 캐스케이드에서는 **항상 비어 있다** — 이동도 축이 조용히 빠진다

· **어디**: `tools/doping/bvse_proxy.py:190-211` (`backfill_one`) ↔ `tier_cascade.sh:203-219`
· **무엇**: 조용히 틀린다. `li_mobility_score` 는 **`--backfill` 경로에서만** 채워진다
  (`3*migration_volume_fraction + bvs_li_proxy_score`). 정상 Stage 05 실행이 쓰는 레코드에는
  `migration_volume_fraction` 와 `bvs_li_proxy_score` 만 있고 `li_mobility_score` 는 없다.
  `axes_present()` 는 값이 없는 축을 조용히 후보에서 빼므로 **에러도 경고도 없이 2축이 된다.**
  그런데 표 헤더는 그대로 `TOP-20 — 3축 결합점수 (stab×0.4 + mod×0.3 + mob×0.3)` 라고 찍힌다.
  BVSE 계산 시간을 273번 쓰고 순위에는 0 기여.
· **근거**: 실제 Stage 05 스키마(=`li_mobility_score` 없음)로 만든 픽스처 실행 실측 —
  ```
  ✓ 전체 3 · 3축 3 → FINAL_RANKING.json      ← "3축" 이라고 말한다
  axis_set ['stability', 'modulus']          ← 실제로는 2축
  ✅ stability 3/3 · ✅ modulus 3/3           (mobility 는 목록에 아예 없다)
  ```
  이 사고는 `combine_rankings.py:57-60` 주석이 2026-08-25 에 이미 기록했다
  (*"3,615행 전원 결측… '3축 랭킹' 이 실제로는 2축"*). **도구는 고쳤는데 러너는 안 고쳤다.**
· **고치는 법**: `tier_cascade.sh` Stage 05 뒤에 
  `python3 tools/doping/bvse_proxy.py --backfill --out $OUT/05_bvse/bvs_report.json` 한 줄을
  넣거나, `bvse_proxy` 본 계산 경로에서 바로 `li_mobility_score` 를 쓰게 한다.
  그리고 표 헤더를 `axis_set` 에서 만들어 "3축" 하드코딩을 없앤다.

## [주의] 09e/09f — MP 키가 없으면 **조용히 건너뛰고 DONE 마커까지 찍힌다**; 네트워크 실패는 더 조용하다

· **어디**: `ehull_check.py:89-104`, `esw_check.py:52-63` (키 없음) · `ehull_check.py:73-74`,
  `esw_check.py:88-92` (호출 실패)
· **무엇**: 부모가 물은 그대로 — **조용한 쪽**이다.
  - 키 없음 → `⚠ SKIPPED` 출력 + `{"skipped": true}` 파일 + **rc=0** → `STAGE_09e.DONE`.
    재개해도 DONE 마커 때문에 다시 안 돈다 (`FORCE_RERUN=09e` 를 손으로 줘야 함).
  - 키 있고 네트워크/API 실패 → `query_hull_decomposition` 의 `except` 가 삼켜서
    `hull_E_at_winner_composition_eV_atom: null` 인 행만 쌓이고 **rc=0**. 09f 는
    `rows.append({'name':…, 'error': str(e)})` 로 행마다 error 를 넣고 역시 rc=0.
    → 273개가 그 축 없이 완주하고, 요약 JSON 만 보면 "돌았다" 로 보인다.
· **근거**: 실측 종료코드 — `09e 키없음 rc=0` · `09f 키없음 rc=0`.
· **고치는 법**: 던지기 전에 `MP_API_KEY` 유무를 **master_batch 선두에서 한 번** 판정하고,
  없으면 "이 캠페인은 ehull/esw 축 없이 돈다"를 캐스케이드 밖에 한 줄로 못 박는다.
  실패 행이 전체의 일정 비율을 넘으면 비영 종료하도록 문턱을 둔다(현재 문턱 없음).

## [주의] 09e/09f 산출물은 **아무 데도 안 들어간다** — 하류 소비자 0

· **어디**: `combine_rankings.py:42-53` (`STAGE_FILE_CANDIDATES` 에 ehull/esw 없음) ·
  `collect_dataset.py:189-203` (읽는 것은 06/07/08/10/11 뿐)
· **무엇**: `ehull_summary.json` / `esw_summary.json` 을 읽는 코드가 저장소에 없다.
  게다가 순서상 09a(combine) 가 09e/09f **앞**이라 구조적으로도 못 쓴다.
  즉 키를 구해도 순위·dataset.csv·predictor 는 그대로다.
· **근거**: `grep -rn "ehull_summary\|esw_summary" --include=*.py --include=*.sh .` →
  히트는 `tier_cascade.sh` 의 출력 경로와 두 도구 자신의 docstring 뿐.
· **고치는 법**: 축으로 쓸 거면 09e/09f 를 09a 앞으로 옮기고 `STAGE_FILE_CANDIDATES` 에 등록.
  안 쓸 거면 "SI 전용 부록" 이라고 스크립트 주석에 명시(지금은 축인 척한다).

## [주의] 키가 있는데 `mp_api` 가 없으면 **캐스케이드가 09e 에서 죽는다**

· **어디**: `ehull_check.py:106-111`, `esw_check.py:65-68`
· **무엇**: 즉사(rc=1) → `tier_cascade.sh` abort → 09f·10·11·12 안 돔. 조용하진 않아서
  앞의 것들보다 낫지만, **10·11 을 그 뒤에 매달아 놓은 배치에서는 치명적**이다.
· **근거**: 실측 `09e 키있음+mp_api없음 rc=1` · `09f … rc=1`.
· **고치는 법**: 두 도구를 던지기 전에 gabia/kgy 의 uma env 에서
  `python3 -c "import mp_api, pymatgen"` 을 한 번 돌려 확인. 없으면 설치하거나,
  ImportError 도 `skipped` 로 강등(키 없음과 같은 취급)한다.

## [주의] Stage 08 라벨이 실제 계산과 다르다 — "clamped-ion" 이 아니라 relaxed-ion

· **어디**: `tier_cascade.sh:238` 주석 ↔ `run_mlip_postproc.py:214-215`
· **무엇**: 조용히 틀린 **서술**. 캐스케이드는 *"clamped-ion Cij at 0K"* 라고 적어 놨는데,
  `elastic_finite_strain` 은 각 변형 셀마다 `opt = FIRE(atoms); opt.run(fmax=…, steps=relax_steps)`
  로 **이온을 완화한다** (`process_one` 이 `relax_steps=500` 을 넘긴다). 물리적으로는
  relaxed-ion 이 실험 비교에 맞는 값이라 계산이 틀린 게 아니라 **원고에 나갈 이름이 틀렸다.**
  clamped-ion 과 relaxed-ion 은 G 가 수십 % 다르다.
· **고치는 법**: 주석을 relaxed-ion 으로 고치고, `postproc.json` 의 `elastic` 블록에
  `ion_relaxation: true` + `relax_steps` 를 기록한다(현재 `eps` 만 남는다).

## [주의] 09d 의 "Top-10" 은 결합점수 순위가 아니라 **안정성 단일축 순위**다

· **어디**: `combine_rankings.py:464, 491-492` ↔ `generate_dft_inputs.py:816, 857`
· **무엇**: 조용히 틀린다. `rows` 는 `score_stability_all` 로 정렬되고(464행), 결합점수 순위는
  별도 키 `ranking_scored_only` 에 이름 목록으로만 있다. 09d 는 `data['rows'][:10]` 을 쓰므로
  **ΔE 만으로 뽑은 10개**를 KISTI 로 보낸다. 그러면서 `composite_score: row.get('score_combined')`
  로 실어 보내는데, 그 값은 미측정 행이면 `None` 이다(461행).
· **고치는 법**: 09d 가 `ranking_scored_only` 순서를 쓰게 하거나, `--rank_by {combined,stability}`
  플래그로 명시하게 한다. `composite_score` 가 None 인 항목은 만들지 않는다.

## [주의] 09c train_predictor — 타깃 6개 중 대부분이 조용히 학습되지 않는다

· **어디**: `train_predictor.py:149-175`
· **무엇**: 타깃별 usable rows < 5 면 `✗ skip` 하고 넘어간다. 캐스케이드 하나당 승자 수가
  적은 273 캠페인에서는 EOS/elastic/σ 타깃이 거의 다 걸린다. **rc=0** 이라 안 보인다.
  실제 관측치: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md:495-496` —
  *"`predictor/` 270개 = `training_summary.json` + `predictor_screen_de_per_atom.pkl`"*
  → 6타깃 중 **1개만** 나왔다.
  · 부수: `train_predictor.py:299` 의 `'features_numeric': feats_numeric` 은 루프 안 지역변수라,
    타깃 컬럼이 CSV 에 하나도 없으면 **NameError → rc=1 → abort**.
· **고치는 법**: 캐스케이드 단위 학습을 포기하고 Stage 12 이후 **캠페인 전체 dataset 합본**으로
  한 번만 학습(`--cascade_glob` 은 `collect_dataset` 에 이미 있다). 지금 273번 학습은
  거의 전부 빈 모델을 쓴다.

## [참고] 09f 의 값은 winner 구조에 의존하지 않는다 — 같은 chemsys 면 전부 같은 숫자

· **어디**: `esw_check.py:100-106`
· **무엇**: `energy_span = max(E/atom) - min(E/atom)` 을 **chemsys 의 MP 엔트리 전체**에 대해 잰다.
  winner 는 원소 집합을 정하는 데만 쓰인다. 그래서 Li-P-S-Cl-X 가 같은 후보들은
  값이 완전히 동일하고, 273개 사이의 **변별력이 0** 이다. (도구 docstring 이 "coarse proxy"
  라고 스스로 적어 두긴 했다 — 축으로 세지 말라는 뜻으로 읽어야 한다.)

## [참고] `_de_of` 의 `or` — post-anneal ΔE 가 정확히 0.0 이면 조용히 screen 값으로 바뀐다

· **어디**: `combine_rankings.py:180-182` — `return r.get('de_per_atom_post_anneal') or r.get('de_per_atom_screen')`
· **근거**: 실측 — `post=0.0, screen=-0.25` → `_de_of = -0.25`. 첫 픽스처에서 이것 때문에
  서로 다른 두 구조의 안정성 축이 **가짜 상수**가 되어 rc=2 abort 까지 갔다.
· **고치는 법**: `x if x is not None else y`.

## [참고] `--selftest` 없음 (코드 규율 위반)

`run_mlip_postproc.py` · `collect_dataset.py` · `train_predictor.py` · `ehull_check.py` ·
`esw_check.py` 다섯 개 모두 `--selftest` 가 없다(실행해서 확인 — argparse 가 `unrecognized`
대신 required 인자를 요구하며 죽는다). 있는 것은 `combine_rankings`(31 ok, 음성 포함) ·
`generate_dft_inputs`(⭕33 ⛔0) 둘뿐이고 **둘 다 통과**한다.

## [참고] 확인해서 **정상**이었던 것들 (근거 포함)

1. **07/08 의 플래그 계약은 맞다.** `--no_anneal`(342) `--no_eos`(343) `--no_elastic`(344)
   `--n_eos_seeds`(354) 전부 존재하고 실제로 분기한다(295·304·306·321행). `--n_eos_seeds 5`
   는 살아 있어 `eos_ensemble` 이 5시드 최적 BM3 를 고른다.
2. **04→07/08 글롭 정상.** `run_anneal.py:161` 이 `work/post_relax.xyz` 를 쓰고,
   07/08 이 `$OUT/04_anneal/*/post_relax.xyz` 를 읽는다. 이름 충돌은
   `winner_name()`(264-273)이 부모 디렉터리 이름으로 푼다 — combine 쪽 폴백(125-129)과 일치.
3. **입력이 0개면 조용하지 않고 즉사한다.** 실측:
   `run_mlip_postproc.py: error: argument --xyz: expected at least one argument` → rc=2.
4. **07/08 물리 코어는 수치적으로 맞다.** EMT Cu 로 CPU 실행(GPU 미사용) —
   ```
   C11=166.7  C12=111.3  C44=86.5 GPa      (EMT 참고값 ~170/~120/~75)
   B_hill=129.7  G_hill=54.9  E=144.3  nu=0.315
   EOS: B0=134.4 GPa  Bp=4.21  r2=1.0000  fit_ok=True
   ```
   EOS 의 B0(134) 와 탄성의 B_hill(130) 이 서로 4% 안에서 일치 → 부호 규약·단위 환산·
   BM3 피팅·VRH 평균 모두 정상. (단, docstring 의 *"ASE 는 압축에서 양수 응력"* 서술은
   틀렸다 — 코드는 표준 규약대로 맞게 짜여 있다.)
5. **`generate_dft_inputs.py` 는 오늘 필수 인자가 늘지 **않았다**.** `--ranking`+`--out`
   경로는 그대로 살아 있고(812-813행), 새로 붙은 `--from_traj/--from_xyz/--collect` 는
   각자 분기 안에서만 인자를 요구한다. 09d 호출은 **인자 계약 관점에선 정상**이다
   (죽는 이유는 위의 xyz 필드 부재).
6. **`collect_dataset` 는 이제 10/11 을 읽는다** (197-203행) — kb 의 옛 지적은 해소됨.
   09b 는 rc=0 으로 3행×65열 CSV 를 정상 생성했다(실측).

---

## 못 본 것 — 무엇을 안 읽었고 왜

- **`combine_rankings.py` 의 `_batch()` (496-601행)** 와 `--cascade_glob/--write/--status` 경로:
  `tier_cascade.sh` 가 안 쓰는 경로라 건너뛰었다. 273 캠페인 사후 집계에 쓸 거면 별도 감사 필요.
- **`generate_dft_inputs.py` 1-711행** (`generate_pwin`·`scf_from_xyz`·`snapshots_from_traj`·
  `collect_results`·`PSEUDOS`·`_selftest`): 09d 가 타는 경로(712-871)와 selftest 만 봤다.
  특히 **`PSEUDOS` 에 273 캠페인의 도펀트 원소가 다 들어 있는지 대조하지 않았다** —
  없으면 `except` 에 걸려 그 항목만 `failed` 로 조용히 빠진다(09d 가 살아난 뒤 반드시 확인할 것).
- **`collect_dataset.py` 의 65개 컬럼 매핑 전수**: 헤더가 나오는지와 09b 종료코드만 봤고,
  각 컬럼이 상류 스키마와 맞는지 필드 단위로 대조하지 않았다.
- **`combine_rankings.py` 의 `grouped_stats` 정규식**(`(.+?)_s\d+$`)이 273 캠페인의 실제
  이름 규칙과 맞는지: 실물 이름 표본이 이 저장소에 없어 확인 못 했다.
- **MLIP 실행 경로 자체**: `load_uma()` · UMA 로딩 · 실제 EOS/탄성 GPU 실행은 **일부러 안 돌렸다**
  (gabia·kgy 점유). 검증은 EMT 대체 계산기로만 했다 — UMA 특유의 실패(OOM, task 이름,
  fairchem 버전)는 이 감사가 못 본다.
- **gabia/kgy 의 파이썬 환경**: 이 컨테이너에는 `pandas`·`sklearn`·`pymatgen`·`mp_api` 가
  **없다**. 09c 는 여기서 rc=1 로 죽었는데, 그게 서버에서도 그런지는 **확인 못 함**
  (SSH 를 쓰지 않았다). 던지기 전에 서버에서
  `python3 -c "import pandas, sklearn, mp_api, pymatgen"` 한 줄로 확인해야 한다.
- **Stage 10·11·12 와 Stage 00–06 본문**: 내 구간 밖이라 계약 확인에 필요한 최소한
  (`run_anneal.py` 의 출력 파일명·`rank_anneal.py` 의 `ranked_by_post_anneal` 키·
  `bvse_proxy.py` 의 레코드 스키마)만 grep 으로 봤다.
- **실제 270개 캠페인 산출물**: 이 저장소에 없다(`runs/` 에는 다른 계열만 있다).
  09d 전멸은 **합성 재현 + kb 기록**이 근거이지, 실물 `dft_input_summary.json` 을 연 것은 아니다.

---

## 배치·자원·재개

# Stage 10–12 + 배치 오케스트레이션 감사 (읽기 전용, 파일 수정·커밋 없음)

읽은 것: `master_batch_273.sh` 391줄 전체 · `tier_cascade.sh` 416줄 전체 · `run_md_sigma.py` 365줄 전체 · `run_cathode_interface.py` 380줄 전체 · `collect_dataset.py` 423줄 전체 · `train_predictor.py` 310줄 전체 · `watch_phase1_v22.sh` 200줄 · `rank_anneal.py`/`run_anneal.py`의 출력 계약 부분 · `convention_check.py`의 `check_shell_calls`/`_required_flags`.
실행한 것: `run_md_sigma.py --help` · `convention_check.py` 전체 · 합성 캐스케이드로 `collect_dataset.py` 실주행 · `cascade_status()` 함수만 떼어내 실주행 · `timeout` 프로세스그룹 실측 · `find -name 'STAGE_12*.DONE'` 계수 실측 · `git show origin/claude/unified-2026-05-15:…`. GPU 잡은 던지지 않았다.

---

## 치명

**[치명] 마스터 사용법이 지시하는 브랜치에는 오늘의 `--seed` 수정도, seed 자체도 없다**
· 어디: `tools/doping/master_batch_273.sh:59-62` (`git pull origin claude/unified-2026-05-15`)
· 무엇: 헤더대로 gabia 에서 실행하면 오늘 고친 커밋(`382cb4e17`)이 없는 브랜치를 받는다. 그 브랜치의 `run_anneal.py` 에는 **`seed` 라는 문자열이 한 번도 안 나온다** → 크래시는 안 나지만 **무시드 비결정 anneal** 로 273개가 돈다. `collect_dataset` 의 `anneal_seed`·`post_relax_sha256` 계보 열이 전부 빈칸이 되고, 그 위에서 BVSE·탄성·σ 순위가 매겨진다(= P0-3 의 뿌리 그대로). 즉사가 아니라 **조용히 틀린다**.
· 근거: `git branch -a --contains 382cb4e17` → `claude/friendly-meitner-lldvar` 뿐. `git show origin/claude/unified-2026-05-15:tools/doping/tier_cascade.sh` 의 184-188 줄에 `--seed` 없음. 같은 브랜치 `run_anneal.py` 에 `grep -n seed` → 0건 (파일은 존재, `git cat-file -e` 통과).
· 고치는 법: 헤더의 pull 대상을 실제 브랜치로 고치고, `tier_cascade.sh` 시작부에서 `git rev-parse HEAD` 를 `cascade.log` 에 박아 어느 커밋으로 돌았는지 사후에 물을 수 있게 한다.

**[치명] 273개가 전부 같은 이유로 죽어도 멈추는 장치가 없다 — 이번 사고를 그대로 재생한다**
· 어디: `master_batch_273.sh:321-329` (`else … ❌ FAIL (rc=$rc) → next`), 루프는 273-330
· 무엇: 실패 카운터도, 연속 실패 임계도, `n_done==0` 조기 중단도 없다. Stage 04 급 사고(37분 뒤 rc=2)가 다시 나면 273 × 37분 ≈ **7일을 태우고 0개 완료로 정상 종료**한다. 마지막에 "Found 0 per-cascade CSVs" 를 찍고 `Done.` 으로 rc=0. 비명을 지르는 곳이 없다.
· 근거: `tools/doping/*.sh` 전체에 연속실패 차단 흔적 없음(`grep -rn "consecutive|n_fail|연속|abort_after"` → `run_site_preference_all.sh` 의 집계 카운터만).
· 고치는 법: `n_consec_fail` 을 세서 3 연속(또는 첫 5개 중 5개) 실패면 `exit 1`. 덧붙여 첫 캐스케이드는 **드라이런 대상**으로 따로 돌려 끝까지 통과한 뒤 나머지 272개를 던진다.

**[치명] `STAGE_12.DONE` 이 12b·최종보고보다 먼저 찍혀서, 실패한 캐스케이드가 영구히 "완료" 로 센다**
· 어디: `tier_cascade.sh:351-354`(12 collect_final) → `355-359`(12b train_final) → `361`(09 report). 판정은 `master_batch_273.sh:153` (`STAGE_12.DONE` **또는** `STAGE_12b.DONE`)
· 무엇: Stage 12 가 끝나는 순간 마커가 생긴다. 그 뒤 12b(train)나 09 report 가 죽으면 tier_cascade 는 rc≠0 로 끝나 마스터는 그 판에서 FAIL 로 찍지만, **다음 마스터 실행의 사전 스캔은 `done` 으로 보고 SKIP** 한다. FINAL_REPORT.json 없는 캐스케이드가 영원히 완료로 집계된다.
· 근거: `STAGE()` 는 성공 시에만 `DONE_MARK`(107-119)하므로 12는 찍히고 12b는 안 찍힌다. `cascade_status()` Layer 1 은 둘 중 **하나**만 있어도 done.
· 고치는 법: 완료 판정을 마지막 스테이지 마커(`STAGE_09.DONE`) 또는 `FINAL_REPORT.json` 존재로 바꾼다. 지금 순서라면 `STAGE_12b.DONE` **AND** 로 바꾸는 것만으로도 절반은 막힌다.

**[치명] 대량 실패 직후 재실행하면 마스터가 몇 초 만에 "정상 종료" 한다 (30분 창)**
· 어디: `master_batch_273.sh:165-172` (Layer 3 `find -mmin -30` → `running`) + 288-301 (`running|locked|external` → `continue`) + 루프가 **단일 패스**(273-330)
· 무엇: 사고를 발견하고 바로 재실행하는 것이 사람의 자연스러운 행동인데, 방금 죽은 캐스케이드 디렉터리에는 30분 안에 쓰인 파일(`.master_lock`·`STAGE_03.DONE`·로그)이 있다 → 전부 `running` 으로 분류 → 전부 SKIP → "will retry on next master_batch invocation" 을 찍고 **그 실행은 아무것도 안 하고 끝난다**. 재시도 루프가 없으므로 "next invocation" 은 사람이 또 쳐야 온다.
· 근거: 함수를 떼어내 실측 —
```
방금 죽은 캐스케이드(파일 mtime<30분) → running
3시간 전 죽은 캐스케이드          → pending
```
· 고치는 법: Layer 3 을 "**살아있는 PID 가 있는 경우에만**" 로 좁힌다(활동 시각은 보조 근거). 그리고 루프 끝에서 skip 된 게 남아 있으면 한 바퀴 더 돌거나 최소한 `⚠ N개를 활동중으로 보고 건너뜀` 을 종료 요약에 크게 찍는다.

**[치명] Stage 10·11 은 실전에서 한 번도 돈 적이 없는 코드인데, 이번엔 기본값이 켜져 있다**
· 어디: `master_batch_273.sh:79-80` (`export TOP_K_SIGMA=2`, `TOP_K_NCM=3`)
· 무엇: 지난 273 런은 `TOP_K_SIGMA=0` 으로 껐다 — `STAGE_10.DONE`·`STAGE_11.DONE` **각 0개**, `11_*` 디렉터리 0/270. 이번엔 마스터가 2/3 을 **export** 하므로 사용자가 따로 끄지 않는 한 미검증 경로가 비용의 대부분을 차지한다. 두 도구 모두 `--selftest` 가 없고(md_sigma·cathode·collect·train 전부 0건), 저장소 어디에도 `sigma_md_summary.json`·`cathode_interface_summary.json` 산출물이 없다. 즉 **첫 실행이 3개월짜리 배치 안에서 일어난다.**
· 근거: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md:245-258` — "stage 10(σ MD)·11(W_ad) 는 **미실행**이다 … `10_md_sigma` 5/270(옛 시험런 잔재) · `11_*` 0/270 · `STAGE_10.DONE`·`STAGE_11.DONE` 각 0". `grep -c -- '--selftest'` → run_md_sigma 0 · run_cathode_interface 0 · collect_dataset 0 · train_predictor 0 (대조: run_anneal 3 · combine_rankings 2).
· 고치는 법: 273 을 던지기 전에 **한 캐스케이드만** `TOP_K_SIGMA=1 TOP_K_NCM=1` 로 끝까지 돌려 Stage 10→11→12 산출물과 dataset.csv 의 σ·Wad 열이 실제로 차는지 본다. 그 전엔 273 을 던지지 않는다.

**[치명] 시간 추정이 계획과 2배 어긋난다 — 스크립트 자신이 193일이라고 찍는다**
· 어디: `master_batch_273.sh:8-9`, `:214` (`Estimated time: ~$((TOTAL_CASCADES * 17 / 24)) days`)
· 무엇: 지금 export 된 기본값(σ 2 · NCM 3)으로 돌리면 마스터가 로그 첫머리에 **193 days (~6.4 months)** 를 찍는다. "MD·adhesion 빼고 3개월" 이라는 계획 수치는 Stage 10·11 을 **끈** 경우다(지난 런 실측 46일 = ~4 h/cascade). 어느 쪽으로 돌릴지 결정이 안 된 채 던지면 6개월짜리를 3개월인 줄 알고 시작한다.
· 근거: 273×17/24 = 193. kb 카드 같은 절: "실제는 5/26 시작 → 7/11 통합 = 46일에 273개 = **cascade 당 ~4 h**. 17 h − σ 12 h ≈ 4 h 로 정합."
· 고치는 법: 던지기 전에 `TOP_K_SIGMA`·`TOP_K_NCM` 을 **의식적으로** 정하고, 마스터 시작 로그의 추정 일수를 눈으로 확인한 뒤 nohup 한다.

**[치명] 지시된 감시 도구가 273 배치를 못 본다 — 진행률이 영원히 0 이고 실패는 표시가 없다**
· 어디: `master_batch_273.sh:69` (`Monitor: bash tools/doping/watch_phase1_v22.sh`) ↔ `watch_phase1_v22.sh:74,81,90,146,167` (`cmp_dir="$BATCH_DIR/$cmp"`)
· 무엇: 마스터는 `$BATCH_DIR/Li2O_x002` 에 쓰는데 대시보드는 `$BATCH_DIR/Li2O` 를 본다. 진행 바는 273 런 내내 `0/95`, 전 화합물이 `·`. 유일하게 움직이는 건 글롭을 쓰는 Section 3(`ls -t "$BATCH_DIR"/*/STAGE_*.DONE`)뿐이라 **"최근 활동" 만 흐르고 진행률은 0** 인 화면이 된다. 게다가 대시보드에는 **실패 표시가 없다** — 죽은 캐스케이드는 "⟲03"(마지막 DONE 스테이지)으로 나와 *지금 04 를 돌고 있는* 캐스케이드와 화면상 구별되지 않는다. 2026-09-09 에 열흘을 못 본 그 눈이 아직 그대로다.
· 근거: 위 줄들을 직접 읽었다. `PHASE_1B` 배열도 54개인데 주석/막대는 64로 그린다(마스터와 목록 자체가 다르다).
· 고치는 법: 감시 도구를 `$BATCH_DIR/${cmp}_${conc}` 로 맞추거나, 마스터 헤더에서 그 도구를 지운다. 그리고 대시보드에 **FAIL 열**을 넣는다 — 판정은 `.log` 의 `Traceback|error:|FAILED — abort` grep, 또는 마스터 로그의 `❌ FAIL` 줄.

---

## 주의

**[주의] Stage 10·11 을 건너뛰어도 12 는 돌고, dataset.csv 는 "MD 돌았고 문제 없었음" 으로 보인다**
· 어디: `collect_dataset.py:197-199, 256-270, 342` · `tier_cascade.sh:294-304, 333-344`
· 무엇: 죽지 않는다. 조용히 NaN 이다 — **그런데 품질 플래그는 NaN 이 아니라 좋은 값으로 채워진다.** `sigma_md_sanity_warnings_count` 는 `len([])` = **0**, 즉 "경고 없음" 과 같은 값이 된다. Layer-2 학습에서 `sanity_warnings_count == 0` 으로 행을 고르면 **MD 가 아예 안 돈 행이 통과**한다.
· 근거: 합성 캐스케이드(02/04/06만 있고 10·11 없음)로 실주행 →
```
RC=0 · 1 rows × 69 cols
  sigma_300K_S_cm_NE             = ''
  sigma_md_sanity_warnings_count = '0'      ← 여기
  wad_J_m2_mean                  = ''
  wad_area_mismatch_severity     = ''
```
· 고치는 법: 그 열을 `None`(미실행)과 `0`(실행·경고없음)으로 갈라 쓴다 — `sig` 가 빈 dict 면 `None`. 겸사겸사 `stage10_ran`/`stage11_ran` 불리언 열을 추가하면 하류가 스스로 거를 수 있다.

**[주의] 완료 카운터가 2배로 나온다**
· 어디: `master_batch_273.sh:338` (`find … -name 'STAGE_12*.DONE' | wc -l`)
· 무엇: `STAGE_12.DONE` 과 `STAGE_12b.DONE` 이 둘 다 걸려 완료 캐스케이드당 2를 센다. 최종 요약이 `546 / 273 cascades complete` 를 찍는다. 진짜 절반만 끝났을 때 `273/273` 으로 보인다.
· 근거: 실측 — 완료 캐스케이드 2개짜리 트리에서 `n_done = 4`.
· 고치는 법: `-name 'STAGE_12.DONE'` 하나만 세거나 `find … | xargs -n1 dirname | sort -u | wc -l`.

**[주의] Stage 11 이 동일한 기준선 6개를 273번 다시 계산한다 — 그 스테이지 비용의 2/3**
· 어디: `run_cathode_interface.py:262-285` (기준선 루프가 무조건 실행) · `tier_cascade.sh:320-341`
· 무엇: comp1~comp5+modelC 는 캐스케이드와 무관하게 **완전히 같은 입력·같은 시드(42-46)** 다. `TOP_K_NCM=3` 이면 한 캐스케이드의 Stage 11 은 SE 9개(기준선 6 + 승자 3) — **2/3 이 매번 똑같은 재계산**이다. 스크립트 자신의 비용 주석(`Stage 11 ≈5-15h`)을 그대로 쓰면 캐스케이드당 3-10 h × 273 ≈ **37-113일이 중복 계산**이다.
· 근거: 기준선 루프에 캐시·스킵·재사용이 없다. 출력은 캐스케이드별 디렉터리로만 간다.
· 고치는 법: 기준선 Wad 를 배치 공용 디렉터리에 한 번 계산해 캐싱하고(입력 해시 + 시드 + 프로토콜 상수로 키), 캐스케이드는 그걸 읽는다. **주의: 지금 구조로는 기준선만 끄는 방법이 없다** — 아래 항목.

**[주의] 기준선을 다 비우면 Stage 11 이 승자까지 통째로 스킵된다**
· 어디: `tier_cascade.sh:333` (`if [ "$TOP_K_NCM" != "0" ] && [ -n "$NCM_BASELINE_ARGS" ]`)
· 무엇: "기준선 없음" 과 "스테이지 스킵" 을 같은 조건으로 묶어 놨다. 위의 중복을 피하려고 `NCM_BASELINE_COMP1="" … ` 로 다 비우면 승자 Wad 도 안 돈다. 게다가 파일이 없는 기준선은 `[ -f "$path" ]` 로 **조용히 빠진다**(331) — 캐스케이드마다 기준선 집합이 달라져도 아무도 모른다.
· 고치는 법: 두 조건을 분리하고, 요청됐는데 파일이 없는 기준선은 로그에 `⚠ baseline X 누락` 을 찍는다.

**[주의] Stage 11 의 Δ 표가 nx 그룹을 섞는다 — 주 기준선과 승자가 다른 NCM 슬랩일 수 있다**
· 어디: `run_cathode_interface.py:146` (`nx = 5 if len(se_atoms) >= 60 else 7`) · 353-372 (Δ 표는 **모든** 기준선에 대해 계산)
· 무엇: 실측 원자수 — comp1 52 · comp2 52 · comp3/4/5 62 · modelC 62. 승자는 LPSCl 1×1×1(52원자)의 치환체라 대개 nx=7 쪽이다. 즉 comp3/4/5/modelC 는 **nx=5 = 다른 NCM 면적**이라 승자와 직접 비교가 불가한데, 표는 `Δ vs comp3` 같은 열을 그대로 찍는다. 코드는 nx 그룹을 따로 인쇄해 놓고(318-337) 정작 Δ 계산에서는 안 쓴다. 논문에 그대로 옮기면 조용히 틀린 비교다.
· 근거: xyz 1행 헤더/cif `_atom_site` 행 수로 확인.
· 고치는 법: Δ 표를 `w['ncm_nx'] == b['ncm_nx']` 인 쌍으로만 만들고, 다른 그룹은 `—` 로 남긴다.

**[주의] 나중에 TOP_K 를 켜도 dataset.csv 는 갱신되지 않는다**
· 어디: `tier_cascade.sh:294/333`(스킵 시 `DONE_MARK` 안 함) ↔ `351`(`STAGE_12.DONE` 은 이미 있음)
· 무엇: 이번처럼 σ 를 끄고 273 을 돌린 뒤 "이제 σ 를 켜자" 하면, Stage 10 은 (마커가 없어) 다시 돌지만 Stage 12 는 **마커가 있어 스킵**된다 → `dataset.csv` 에 σ 열이 영원히 안 들어온다. 스크립트가 FORCE_RERUN 에 대해 경고하는 그 하류 무효화 문제(96-104)가 **FORCE_RERUN 없이도** 일어난다.
· 고치는 법: Stage 10/11 이 실제로 돌면 `rm -f $OUT/STAGE_12*.DONE $OUT/STAGE_09.DONE` 을 그 스테이지 뒤에 붙인다.

**[주의] 마스터 최종 집계가 미완 캐스케이드의 09b 판 dataset.csv 까지 섞는다**
· 어디: `master_batch_273.sh:350` (`glob('$BATCH_DIR/*/dataset.csv')`)
· 무엇: `dataset.csv` 는 Stage **09b** 에서 한 번, Stage **12** 에서 다시 쓰인다(같은 경로). Stage 10 에서 죽은 캐스케이드에는 09b 판이 남아 있고, 집계는 완료 여부를 안 보고 전부 concat 한다. 열 구성이 같으니 섞인 걸 알 방법이 없다.
· 고치는 법: 글롭 결과를 `STAGE_12.DONE` 있는 디렉터리로 거르거나, 최소한 `is_complete` 열을 붙인다.

**[주의] Stage 10 의 MSD 창·마찰이 집 규약과 다르고, convention_check 가 이 형태를 못 잡는다**
· 어디: `run_md_sigma.py:136`(`fit_start = n_frames // 2`) · `:94`(`friction=0.01/units.fs`) · `:279-280`(equil 10 ps / prod 50 ps)
· 무엇: CLAUDE.md 규약은 **MSD 창 2–50 ps 고정** · friction 0.02 · equil 5 / prod 200. 여기는 창이 "뒤 절반"(prod 50 ps 면 25–50 ps), 마찰 0.01/fs, equil 10. `convention_check.py` 는 창을 **리터럴 상수/argparse 기본값**으로만 찾으므로(`CANON_WINDOW`·`ARG_DEFAULT2`) `n_frames//2` 는 시야 밖이다 — 지금 "0 위반" 은 **통과가 아니라 안 본 것**이다.
· 근거: `python3 tools/convention_check.py` → `위반 (0)`, `셸 러너 필수 인자 누락 (0)`, 경고는 kB 자릿수 11건뿐. 검사기 55-70줄에서 창 탐지가 리터럴 기반임을 확인.
· 고치는 법: `--fit_window_ps` 를 인자로 빼고 기본값을 `[2.0, 50.0]` 으로 둔다(그러면 검사기도 본다). 규약에서 벗어날 이유가 있으면 EXEMPT 에 사유를 적는다.

**[주의] 마스터에 cwd 가드도 중복실행 가드도 없다**
· 어디: `master_batch_273.sh:315` (`bash tools/doping/tier_cascade.sh` — 상대경로) · 파일 전체에 `cd` 없음 · `pgrep` 없음
· 무엇: 레포 루트가 아닌 곳에서 nohup 하면 273번 `rc=127` 로 실패하고 FAIL 로그만 남긴다(위의 차단기 부재와 겹치면 몇 초 만에 0개 완료 종료). 또 마스터 두 개를 동시에 띄우면 스캔→`mkdir`→lock 쓰기 사이에 경합이 있어(289-307) 같은 캐스케이드를 한 GPU 에서 둘이 돌릴 수 있다. CLAUDE.md 의 "실행 스크립트에 pgrep 중복실행 가드" 규약을 안 지킨다(`tools/doping` 안에서 가드가 있는 건 `run_as2s3_recover`·`run_force_check_scf`·`run_y_dft`·watch 계열뿐).
· 고치는 법: `SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; cd "$SCRIPT_DIR/../.."` + 맨 앞에 `pgrep -f master_batch_273 | grep -v $$` 가드.

**[주의] 캐스케이드 로그를 재실행 때마다 덮어써서 실패 증거가 사라진다**
· 어디: `master_batch_273.sh:319` (`> "$LOG" 2>&1`)
· 무엇: 이번 Stage 04 사고에서 원인을 알려준 것이 바로 이 로그다. 재개하면 `>` 가 그걸 지운다.
· 고치는 법: `>>` 로 바꾸고 실행 시작 배너를 찍거나, `${cmp_label}.log.$(date +%s)` 로 회차별 파일.

---

## 참고

**[참고] 24h timeout — 고아 GPU 잡은 안 생긴다. 대신 한 스테이지가 24h 를 넘으면 그 캐스케이드는 영원히 못 끝난다**
· 어디: `master_batch_273.sh:312`, `tier_cascade.sh:294-344`
· 근거(실측): `timeout 3 env FOO=bar bash child.sh` → rc=124, 손자 python 도 같이 죽음(프로세스 그룹 전체, coreutils 9.4). 처음 측정에서 "살아남음" 으로 잘못 읽었다가 tick 로그로 재측정해 정정했다.
· 남는 문제: resume 단위가 **스테이지**다. Stage 11(주석상 5-15h)이 24h 를 넘기면 매 판마다 처음부터 다시 돌아 영원히 마커가 안 생긴다. Stage 10/11 이 쓰는 `*_incremental.json` 은 **아무도 다시 읽지 않는다**(저장소 전체 grep — 쓰는 곳만 있고 읽는 곳이 없다). 즉 중간 저장이 재개에 쓰이지 않는다.
· 고치는 법: 승자·시드 단위 스킵(이미 있는 `sigma_md.json`/`wad.json` 이면 건너뛰기)을 넣으면 timeout 이 파괴적이지 않게 된다. 그전엔 timeout 을 스테이지 예상시간 위로 올린다.

**[참고] 철회된 H_R 0.5 보정값이 아직 매 승자 JSON 에 쓰인다**
· 어디: `run_md_sigma.py:240` (`'sigma_300K_S_cm_with_HR_0p5_estimate': float(sigma_300K * 0.5)`)
· 무엇: 같은 파일 15-28줄과 252-256줄이 "부호가 반대였고 우리 값도 아니다, 나누지 마라" 고 철회해 놓고, 출력 필드는 그대로 남아 있다. 하류에서 읽는 곳은 없지만(저장소 전체에서 이 키는 이 한 줄뿐) 사람이 JSON 을 열면 집어 갈 수 있다.
· 고치는 법: 필드 삭제, 또는 키 이름을 `RETRACTED_do_not_use_…` 로.

**[참고] train_predictor 는 0행이어도 rc=0 으로 "성공" 한다**
· 어디: `train_predictor.py:173-174` (`len(d) < 5 → continue`) · 295-306
· 무엇: dataset.csv 가 헤더만 있어도 전 타깃을 스킵하고 `training_summary.json`(모델 0개)을 쓰고 정상 종료 → `STAGE_12b.DONE`. 또 `summary['features_numeric']`(299)는 **마지막 타깃 루프의 값**이라 타깃별로 다른 특징 집합을 하나로 뭉뚱그려 기록한다. 그리고 전 타깃이 152줄 `continue`(열 자체가 없음)로 빠지면 299줄에서 `NameError` 로 죽는다 — 옛 스키마 CSV 를 물리면 나는 길이다.
· 확인 못 함: 이 컨테이너에 pandas·sklearn 이 없어 **train_predictor 는 실행하지 못했다**(아래 참조).

**[참고] `collect_dataset.main()` 의 `return 2` 가 종료코드로 안 나간다**
· 어디: `collect_dataset.py:394, 398` ↔ `422-423` (`main()` 을 `sys.exit()` 없이 호출)
· 무엇: "캐스케이드를 못 찾았다" 같은 실패가 rc=0 으로 나가 스테이지가 DONE 이 된다. Stage 12 호출은 두 인자를 다 주므로 이번 배치에서 이 경로를 타지는 않는다.

**[참고] `.master_lock` 은 한 번 쓰면 지워지지 않는다**
· 어디: `master_batch_273.sh:307` (쓰기) — 삭제는 stale 판정 시(181)뿐
· 무엇: 마스터가 살아 있는 동안 이미 지나간 캐스케이드가 전부 `locked` 로 보인다(설계 의도로 보임). 다만 3개월짜리 런에서 PID 재사용이 일어나면 죽은 lock 을 살아있다고 오판할 수 있다. 실측으로 `살아있는 PID → locked` 는 확인했다.
· 고치는 법: lock 에 PID 와 함께 `보스 시작시각`(`/proc/<pid>/stat` 의 starttime)을 적어 대조한다.

**[참고] 인자 이름이 바뀌는 종류는 조용하지 않다 — 즉사한다**
· 근거: `tools/doping/` 전체에 `parse_known_args` 사용 0건. argparse 기본 동작이라 모르는 플래그는 rc=2 로 죽는다. 다만 `check_shell_calls` 가 보는 것은 **required=True 누락뿐**이고, `_required_flags` 는 도구 파일을 못 읽으면 **빈 집합을 돌려주므로**(230-239) 경로 오타난 호출은 조용히 통과한다.
· Stage 10/11/12 호출 4건은 필수 인자를 다 넘긴다(`--ranking/--anneal_dir/--out`, `--csv/--out_dir`) — 셸과 argparse 를 눈으로 대조했고 검사기도 0을 찍는다.

**[참고] 입출력 사슬 04 → 06 → 10/11 은 맞는다**
· `run_anneal.py:113-114` 가 `<out>/<winner_name>/post_relax.xyz` 를 쓰고 `:453` 이 `{'results':[{'name':…}]}` 를 쓴다 → `rank_anneal.py:105` 가 `ranked_by_post_anneal` 로 내보내고 → `run_md_sigma.py:290,308-309` 와 `run_cathode_interface.py:243,290` 이 `anneal_dir/<name>/post_relax.xyz` 로 다시 찾는다. 이름 키가 같은 `winner_name()` 계보다. 다만 06 은 screen ∩ anneal **교집합**이라(`rank_anneal.py:45`) 이름이 어긋나면 랭킹이 0행이 되고, 그때 Stage 10 은 `raise SystemExit("No records")` 로 **즉사**한다(조용하지 않다 — 이건 좋은 쪽).

**[참고] MSD 시간축이 첫 프레임 뒤로 한 스텝(2 fs) 밀린다**
· 어디: `run_md_sigma.py:115-134` — 루프 전에 t=0 프레임을 넣고, 루프 안에서는 `md.run(1)` **뒤에** `step % save_every == 0` 을 보므로 저장 시각이 0, 1, 21, 41 … 스텝인데 `dt_arr` 은 0, 20, 40 … 을 가정한다. 상수 오프셋이고 적합은 뒤 절반만 쓰므로 기울기(D)에는 영향이 없다. 논문 SI 로 나가는 `msd_*.dat` 의 시간열이 2 fs 어긋난다는 정도.

---

## 못 본 것 — 무엇을 안 읽었고 왜

1. **`train_predictor.py` 를 실행하지 못했다.** 이 컨테이너에 `pandas`·`sklearn` 이 없다(`ModuleNotFoundError: No module named 'pandas'`). 위의 0행 거동·`feats_numeric` NameError 경로는 **코드를 읽고 추론한 것**이지 실측이 아니다. gabia 에서 헤더만 있는 CSV 를 물려 한 번 돌려 보면 30초에 확정된다.
2. **같은 이유로 `master_batch_273.sh:345-389` 의 집계 파이썬(pandas)도 실행 못 했다.** `rsplit('_x',1)` → `float('005')=5.0`/`/100=0.05` 라벨 규약은 손으로 계산해 맞다고 봤지만 실주행은 아니다.
3. **Stage 10·11 의 물리 본체(UMA MD·anneal·LBFGS)는 한 줄도 돌리지 않았다.** GPU 금지 지시 때문이다. 따라서 σ 절대값·Wad 값의 타당성, 12 h/5-15 h 라는 비용 주석의 실제 여부, 2×2×2 슈퍼셀에서 `md.run(1)` 25,000회의 파이썬 오버헤드는 **전부 미확인**이다. 위에서 인용한 시간은 스크립트 자신의 주석과 kb 실측치다.
4. **`ase`·`fairchem` import 가 이 환경에 없어** `run_cathode_interface.py --help` 는 시도하지 않았다(모듈 최상단이 아니라 `main()` 안에서 import 하므로 --help 는 통과할 가능성이 높지만 확인 안 했다). `run_md_sigma.py --help` 는 실제로 돌려 인자 목록을 확인했다.
5. **`anneal_se` 의 `friction=0.01`(단위 없는 ASE 값 ≈ 0.001 fs⁻¹)이 원본 프로토콜과 같은지 대조 못 했다.** 근거 파일 `db/inputs/adhesion_templates/adhesion_v6_anneal_test.py` 를 열지 않았다 — 같은 파일 안에서 `run_md_sigma` 는 `0.01/units.fs`, 여기는 맨 `0.01` 이라 **약 100배 차이**이고 "v6 verbatim" 이라는 주석이 사실인지 확인이 필요하다. 사실이면 계승된 것이고, 아니면 Stage 11 의 500 K 5 ps anneal 이 사실상 열욕 없이 돈다는 뜻이다. **이건 다음 감사에서 제일 먼저 볼 것.**
6. **Stage 00-09 (내 구간 밖)** 은 계약 대조에 필요한 만큼만 봤다 — `preflight.py`·`run_compound_batch.sh`·`run_uma_screening.py`·`select_winners.py`·`bvse_proxy.py`·`run_mlip_postproc.py`·`combine_rankings.py`(773줄)·`ehull_check.py`·`esw_check.py`·`generate_dft_inputs.py`·`stage_report.py` 의 **본문은 안 읽었다**. 특히 `combine_rankings.py`(Stage 09a, FINAL_RANKING.json → collect_dataset 의 `combined_score`/`rank_combined` 공급원)와 `stage_report.py`(모든 스테이지 뒤에서 `|| true` 로 삼켜지며 호출됨, `tier_cascade.sh:114-115`)는 내 구간과 맞닿아 있는데 못 봤다.
7. **실제 배치 산출물이 이 저장소에 없어** 마스터의 resume 5-트리거를 **진짜 273 트리 위에서** 검증하지 못했다. 합성 디렉터리로 함수 단위 실측만 했다.
8. **`.v3_survey/` 의 어제 전수조사 결과물은 읽지 않았다** — 이번 지시가 "본문을 읽어라" 였으므로 그 요약에 기대지 않기로 했다.

---

## 검증 ① 재현

읽기 전용 검증 완료. 파일 수정·커밋 없음. 아래가 재현 결과다.

# 0. 먼저 — `convention_check.py` 는 0 위반이 맞다, 그런데 그게 구멍이다

```
$ python3 tools/convention_check.py
위반 (0):
셸 러너 필수 인자 누락 (0):
RESULT: 0 위반 — 2026-08-11 기준선 유지
```

그런데 그 게이트가 **실제로 해결하는 도구는 37개뿐**이고, `substitute_compound.py` 는 그 안에 없다:

```
tools resolved by _RE_PYCALL: 37
  tools/doping/substitute_compound.py: NOT SEEN
  tools/doping/run_anneal.py:          YES {'tier_cascade.sh'}
required flags of substitute_compound.py: {'--out', '--base'}
```

원인은 `tools/convention_check.py:226` 의 `_RE_PYCALL` 이 **경로 리터럴**을 요구하는데
`run_compound_batch.sh` 는 140·169·191·223 네 줄 전부 `python3 "$SCRIPT"` 로 부르기 때문이다.
게다가 이 검사는 **필수 인자 누락만** 본다 — 아래 [재현 2] 의 *choices 불일치*는 원리적으로 못 잡는다.
**감사자의 이 지적은 맞다. "0 위반" 은 "그 파일을 봤다" 가 아니다.**
(도구 자신의 docstring 이 "변수로 조립한 호출은 못 본다" 고 이미 적어 놨지만, 그 사실이
실행 결과 `0 위반` 한 줄에는 안 드러난다 — 미해결 호출을 **세어서 찍는 것**이 고치는 법이다.)

---

# 1. 재현된 치명 항목 (13건 — 전부 실행 또는 실물 코드로 확인)

## [재현] 3농도가 바이트 동일 구조를 만든다
`substitute_compound.py:678` · 세 농도를 실제로 돌렸다:
```
x=0.02 n_units 1 actual_x 0.25 | x=0.05 n_units 1 actual_x 0.25 | x=0.10 n_units 1 actual_x 0.25
Effective f.u. per cell: 4   (master 가 supercell 1,1,1 → n_fu_actual=4)
md5 대조: identical 8 / 8      파일명은 x020 / x050 / x100 로 다름
```
(감사자는 20/20 이라 했고 나는 8/8 — `--n_seeds` 차이일 뿐 결론 동일.)
`master_batch_273.sh:318` 이 지금도 세 번 다 `1,1,1` 을 넘기고, `:368` 근처가
`concentration_pct = float(conc_label)` 로 **디렉터리 이름에서 2.0/5.0/10.0 을 지어낸다**. 확인.

## [재현] `--method cluster` 가 없는 선택지 + rc 가 삼켜진다
```
$ python3 tools/doping/substitute_compound.py … --method cluster …
rc=2
substitute_compound.py: error: argument --method: invalid choice: 'cluster'
                        (choose from 'spread', 'random', 'first')

$ bash -c 'set -e; python3 … --method cluster … 2>&1 | tail -3 || true; echo rc=$?'
SHELL CONTINUED, rc after pipe=0        ← set -e 도 안 걸린다
```
호출은 `run_compound_batch.sh:169-175`, argparse 는 `substitute_compound.py:585-586`.
구현이 이미 있다는 것도 확인: `substitute_struct.py:141,154` 가 `'cluster'` 를 분기한다.
**2026-09-09 사고와 같은 종류가 맞다.**

## [재현] LiCl · Li2S 는 무결점 원본 그대로다
```
base comp: {'Li':24,'P':4,'S':20,'Cl':4}
LiCl: 2/4 구조가 base 와 동일 조성   max|dpos|=4.33e-09 Å  max|dcell|=0
Li2S: 4/6 구조가 base 와 동일 조성   max|dpos|=4.33e-09 Å  max|dcell|=0
```
비율(1/2 · 2/3)이 감사자 보고(10/20 · 20/30)와 같다.

## [재현] Stage 04 가 전멸해도 rc=0, 그리고 resume 이 실패를 "완료"로 본다
`run_anneal.py` 를 EMT 로 로드하고 `anneal_one` 을 `RuntimeError("CUDA out of memory")` 로 바꿔 실행:
```
main() 정상 반환 → exit code 0
anneal_results.json:  n_done 3   error 레코드 3
done set (error 레코드 포함): 3개 → 두 번째 실행의 todo 는 비어 있다
```
`run_anneal.py:425-445`(except 로 삼킴, 실패 카운트 없음) · `:411-419`(done 에 error 포함) 확인.
⚠ 이 OOM 은 **시뮬레이션**이지 실제 GPU OOM 재현이 아니다.

## [재현] Stage 05 가 미완화 구조로 조용히 갈아탄다
`tier_cascade.sh:203-219` 의 `bash -c` 블록을 그대로 떼어 04_anneal 을 비운 채 실행:
```
  No post_relax.xyz files; falling back to initial structures
✓ 2 BVS records → …/05_bvse/bvs_report.json
Stage05 fallback rc=0
geometry_source key? False        ← 요약 어디에도 미완화 표시가 없다
record xyz: …/01_structures/structures/…xyz
```
바로 위 200-202 줄이 *"External review CR-3: BVS depends exponentially on bond length"* 라고
**금지 이유를 적어 놓은 그 계산**이 기본 폴백이다. 확인.

## [재현] Stage 06 은 조인 0 건이어도 rc=0
이름이 하나도 안 겹치는 픽스처:
```
✓ 0 structures joined → rank.json
rc=0        n_joined 0   ranked 0
```
`rank_anneal.py:44-73,100-108` 에 문턱 없음. 그 파일이 09e·09f·10·11 의 유일한 입력인 것도
`grep ranked_by_post_anneal` 로 실물 확인(run_md_sigma:290 · ehull_check:114 · esw_check:72 · run_cathode_interface:243).

## [재현] Stage 09d 가 DFT 입력 0개를 만들고 rc=0
합성 캐스케이드로 09a → 09d 를 실제로 연결해 돌렸다:
```
⚠ C_s00: no xyz available   ⚠ B_s00: …   ⚠ A_s00: …
✓ Generated 0 DFT inputs (0 skipped, 3 failed)      rc=0
$ ls dft_inputs/ →  dft_input_summary.json   (그것뿐)
```
`FINAL_RANKING.json` 실제 row 키에 xyz 경로가 없다(실측 출력):
`['B0_GPa','B_hill_GPa','E_young_GPa',…,'name','poisson_nu','pugh_ratio','score_*']`.
내 픽스처의 anneal 레코드에는 `xyz_input` 이 **있었는데도** `combine_rankings.load_rows()` Pass 2 가
그걸 row 로 안 옮긴다 — 감사자 진단이 정확하다.

## [재현] Stage 09a 는 승자 1개면 rc=2 로 캐스케이드를 abort 시킨다
승자 1개 픽스처(li_mobility_score 포함, 즉 축 3개 다 살아 있는 상태):
```
⛔ stability 1/1 (100.0%) — 전 행 동일값 → 0.5 상수 · 가중치 0.4
⛔ modulus   1/1 …   ⛔ mobility 1/1 …
09a rc=2
```
`combine_rankings.py:772` `return 2 if n_dead else 0`. `tier_cascade.sh` 의 `STAGE()` 는
비영이면 `exit $status` → 09b~12 전부 안 돈다. 확인.

## [재현] 마스터가 지시하는 브랜치에 `--seed` 가 없다
```
$ git show origin/claude/unified-2026-05-15:tools/doping/tier_cascade.sh | grep -A5 "STAGE 04 anneal"
STAGE 04 anneal \
    python3 tools/doping/run_anneal.py \
        --summary_json … --out … --device cuda $ANNEAL_FLAGS      ← --seed 없음
$ git show origin/claude/unified-2026-05-15:tools/doping/run_anneal.py | grep -c seed
0
$ git branch -a --contains 382cb4e17
  claude/friendly-meitner-lldvar  (뿐)
```
`master_batch_273.sh:59` 이 `git pull origin claude/unified-2026-05-15` 다.
그 브랜치에선 `--seed` 가 필수가 아니라 **죽지도 않는다** — 무시드 비결정 anneal 로 273개가 돈다.
**즉사가 아니라 조용히 틀리는 쪽이다. 이게 이번 검증에서 제일 무섭다.**

## [재현] 연속 실패 차단 장치가 없다
```
$ grep -nE "n_fail|consec|abort_after|fail_count|MAX_FAIL" tools/doping/master_batch_273.sh
  (없음)
:327  log_msg "… ❌ FAIL (rc=$rc) → next (check $LOG)"
```

## [재현] `STAGE_12.DONE` 만 있어도 "done", 30분 창이 방금 죽은 캐스케이드를 스킵
`cascade_status()` 를 그대로 떼어내 실행:
```
방금 죽은 캐스케이드(파일 mtime<30분): running     ← 재실행하면 조용히 SKIP
3시간 전 죽은 캐스케이드          : pending
STAGE_12.DONE 만 있고 12b 없음    : done           ← 12b/09report 실패해도 영구 완료
```
`master_batch_273.sh:153`(Layer 1 이 12 **또는** 12b) · `:165-172`(Layer 3) 확인.
`tier_cascade.sh:351-359` 에서 12 마커가 12b 보다 먼저 찍히는 것도 확인.

## [재현] 미검증 Stage 10·11 이 기본으로 켜져 있고 193일이 스크립트 자신의 수치다
```
master_batch_273.sh:79-80  export TOP_K_SIGMA=2 / TOP_K_NCM=3
:214  Estimated time: ~$((TOTAL_CASCADES*17/24)) days  →  273*17//24 = 193 days
selftest 유무: run_md_sigma 0 · run_cathode_interface 0 · collect_dataset 0 · train_predictor 0
               (있는 것: run_anneal 3 · combine_rankings 2 · generate_dft_inputs 3 · bvse_proxy 1 · select_winners 1)
```
헤더 8-9행도 `~193 days (~6.4 months)` 라고 스스로 적어 놓았다.

## [재현] Type C 는 cation site 필터를 우회한다
같은 화합물(WO3)로 두 경로를 돌려 대조:
```
Type A (--auto_cation_sites): site_preference filter (cations ['W']): [Li_24g,Li_48h,P_4b] → ['P_4b']
Type C (anion auto only)    : (cation 필터 줄 자체가 안 나온다)
tA_WO3 cation sites used: ['P_4b']
tC_WO3 cation sites used: ['Li_24g']     ← W⁶⁺ 를 Li⁺ 자리에
```
필터가 `substitute_compound.py:631-651` 의 `if args.auto_cation_sites:` 안에만 있다. 확인.

---

# 2. **재현 안 된 것 — 감사 보고를 정정한다** (이게 이번 검증의 핵심 산출물이다)

## [반증·치명등급 철회] "Stage 05 의 BVSE 축은 신선한 캐스케이드에서 항상 비어 있다"

감사자(Stage 07–09f)가 **치명**으로 올린 항목인데, **현재 코드에서는 틀렸다.**
`bvse_proxy.py` 를 실제 xyz 두 개로 CPU 실행해 출력 스키마를 봤다:

```
record keys: [… 'grid_resolution', 'li_mobility_score', 'migration_volume_fraction' …]
li_mobility_score present: True
```

`bvse_proxy.py:404-415` 가 **저장 전에** 계산한다. 그 위 주석이 바로 감사자가 인용한 2026-08-25
사고(0/3615)이고, 커밋 `bf8949299 "li_mobility_score 를 **저장 뒤가 아니라 앞에서** 계산한다"`
로 이미 고쳐졌다. 실제 스키마를 넣은 3구조 픽스처로 09a 를 돌리면:
```
axis_set ['stability','modulus','mobility']
✅ stability 3/3 · ✅ modulus 3/3 · ✅ mobility 3/3 · rc=0
```
감사자는 `li_mobility_score` 를 **뺀 픽스처를 손으로 만들어** 확인했다 — 픽스처 인공물이지
저장소 결함이 아니다. `--backfill` 은 옛 캠페인 산출물 보수용이다.

⚠ 다만 **메커니즘 자체는 실재한다.** 내가 그 필드를 뺀 픽스처로 재현했다:
```
✓ 전체 3 · 3축 3 → FINAL_RANKING.json        ← 화면은 "3축" 이라고 말한다
axis_set ['stability','modulus']              ← 실제로는 2축, mobility 는 목록에 없다
```
`combine_rankings.py:740-741` 의 표 헤더 `"TOP-20 — 3축 결합점수"` 가 `axis_set` 과 무관한
**하드코딩**인 것은 맞다. 등급은 [치명]이 아니라 [주의]다: *bvse 레코드가 error 로 떨어지면
그 캐스케이드는 조용히 2축이 되고 화면은 3축이라고 말한다.*

## [정정] crc16 시드 충돌 "2000개 중 34개" — 숫자는 맞지만 심각도가 과장됐다
```
random 이름 2000개 → 시드 공유 55개      (감사자 34개와 같은 자릿수, 생일역설대로)
한 캐스케이드 규모(30개) → 0
```
시드는 **한 실행 안에서만** 의미가 있고 한 캐스케이드의 승자는 5~30개다. 실질 위험 거의 없음.
`& 0xFFFFFF` 로 넓히는 것은 여전히 공짜지만 [참고] 이하다.

## [확인] 나머지 [주의]·[참고] 중 실행으로 확인한 것
```
_de_of or-bug:  post=0.0, screen=-0.25 → -0.25            (combine_rankings.py:180-182) 확인
09e 키 없음:    ⚠ MP_API_KEY not set — SKIPPED   rc=0     확인
09e 키 있음+mp_api 없음:                          rc=1     확인
ehull/esw 소비자: grep 히트는 tier_cascade 출력 경로 + 두 도구 자신의 docstring 뿐  확인
BVS 파라미터 두 벌: comp1_v3 S 2.105 / Cl 2.249 / O 1.466  vs  bvse_proxy S 1.94 / Cl 1.91 / O 1.466  확인
"clamped-ion" 라벨: elastic_finite_strain 이 변형 셀마다 FIRE(atoms).run(steps=relax_steps) 로
                    이온을 완화한다(:214-215, :323 이 args.relax_steps 전달) → relaxed-ion. 라벨 틀림. 확인
Stage 02 빈 todo: 주기 저장이 for 루프 **안**에만 있고(:341-352) 루프 뒤 저장 없음,
                  sys.exit 도 없음 → todo 비면 파일 미생성 + rc=0.  **코드 읽기만** (fairchem 없음)
preflight: positive control 이 Nd2O3/MgO/Al2O3 하드코딩(:267 근처 cases) ·
           check_baseline_relax(Path(args.base)) 가 device 를 안 넘겨 calc=None → device='cuda' 하드코딩 ·
           check_disk_space 기본 5.0 GB 상수 · sys.exit(0 if n_pass==n_total else 1).  코드 읽기로 확인
```

---

# 3. 못 본 것 — 무엇을 안 읽었고 왜

- **이 컨테이너에 `fairchem` · `pandas` · `sklearn` · `pymatgen` · `mp_api` 가 없다**(실행 확인).
  따라서 **Stage 00 preflight 의 UMA 경로 · Stage 02 실제 수렴률 · 09b/09c · Stage 10 · Stage 11 은
  한 줄도 실행하지 못했다.** 그 구간 판정은 전부 코드 읽기다.
- **GPU 실행 금지 지시를 지켰다.** Stage 04 전멸은 `anneal_one` 을 예외로 갈아끼운 **시뮬레이션**이고
  실제 `torch.cuda.OutOfMemoryError` 를 재현한 것이 아니다. `except Exception` 이 그 타입을
  잡는다는 것은 타입 관계로만 안다.
- **`site_preference.py` 의 화학 판정이 옳은지는 검증 안 했다.** Type A/C 대조는 결과만 봤다.
- **BVS 파라미터 두 벌 중 어느 쪽이 옳은지 판정 안 했다.** 값이 다르다는 것만 확인했고
  `comp1_v3` 의 BVSE 형식(Morse/스크리닝/컷오프)은 안 읽었다. 던지기 전 1저자 결정 필요.
- **실물 273 캠페인 산출물이 저장소에 없다.** `dft_inputs/` 전멸·Stage 10/11 미실행은
  합성 재현 + kb 기록(`kb/methodology/cascade_pipeline_anatomy_2026_08_13.md`)이 근거이지
  원격 `runs/` 를 연 것이 아니다. SSH 는 쓰지 않았다.
- **`generate_dft_inputs.py` 의 `PSEUDOS` 커버리지**(273 캠페인 도펀트 원소가 다 있나)는 안 봤다 —
  09d 가 살아난 뒤 반드시 확인할 것.
- **`master_batch_273.sh` 를 실제로 돌리지 않았다.** `cascade_status()` 함수만 떼어내 실행했다.
- **감사 보고의 [주의]·[참고] 중 코드 읽기만으로 적힌 항목**(migration_volume_fraction 의 고정 격자수,
  `tree.query(k=25)` 포화, `--xyz $xyzs` 비인용, 09c 타깃 스킵, 16종 단일그룹)은
  **이번 검증에서 다시 확인하지 않았다** — 치명 항목 재현을 우선했다.

---

# 4. 한 줄 결론

**치명 13건 중 12건 재현, 1건 반증(BVSE 이동도 축 — 이미 `bf8949299` 로 고쳐져 있다).**
지금 던지면 최소한 ① 농도축 3배가 중복, ② Nd2O3 포함 30 캐스케이드의 cluster arm 소실,
③ 헤더대로 pull 하면 무시드 anneal, ④ 승자 1개 캐스케이드는 09a 에서 abort,
⑤ 09d 는 273개 전부 DFT 입력 0개 — 이 다섯이 **각각 독립적으로** 3개월을 버린다.
그리고 `convention_check.py` 는 이 중 어느 것도 못 본다(0 위반은 커버리지가 아니다).

---

## 검증 ② 반증

읽기 전용 감사 완료. 스테이지 **사이·바깥** (검증 ②) 만 봤다 — 스테이지 내부는 앞의 두 감사자 담당이다.

---

## [치명] `timeout 86400` 이 GPU 프로세스를 안 죽인다 — 24h 초과 캐스케이드마다 **고아 UMA 가 GPU 에 남고**, 다음 캐스케이드가 그 위에 올라탄다

· **어디**: `tools/doping/master_batch_273.sh:312-319`
· **무엇**: `timeout 86400 env … bash tier_cascade.sh` 가 24h 뒤 TERM 을 보낸다. bash 는 죽고 rc=124 가 돌아와 master 는 곧바로 **다음 캐스케이드를 시작**한다. 그런데 실제로 GPU 를 물고 있는 건 손자 프로세스(`python3 run_md_sigma.py` 등)고, 그건 안 죽는다. CLAUDE.md 가 적어 놓은 gabia 사고(“pw.x와 UMA 동시 실행 금지 — VRAM 47/48 GB”)가 **UMA↔UMA 로 자동 재현**된다. 게다가 timeout 은 273번 중 여러 번 걸릴 구조다(아래 [주의] 참조) → 고아가 누적된다. master 헤더가 권하는 `pkill -9 -f master_batch_273` 도 같은 모양으로 손자를 남긴다.
· **근거**: 이 상자에서 그대로 재현 (CPU, GPU 안 씀).
  ```
  timeout 3 env FOO=1 bash /tmp/child.sh   # child.sh 가 python3 를 foreground 로 돌린다
  timeout rc=124
  grandchild pid=5000
  ORPHAN ALIVE — timeout did NOT kill the python grandchild
  ```
· **고치는 법**: `timeout -k 30 --signal=TERM 86400 setsid bash …` 로 세션을 떼고 종료 시 `kill -- -<pgid>` 로 그룹을 정리한다. 그리고 **다음 캐스케이드를 던지기 전에** `nvidia-smi --query-compute-apps=pid --format=csv,noheader` 가 비었는지 확인하고, 안 비었으면 대기하거나 중단한다(지금 master·tier_cascade 어디에도 nvidia-smi 호출이 없다 — 아래 항목 참조).

---

## [치명] `STAGE_12.DONE` 이 **12b·09 보다 먼저** 찍힌다 → 실패한 캐스케이드가 영구히 "done" 이 되고 `FINAL_REPORT.json` 은 영원히 안 생긴다

· **어디**: `tier_cascade.sh:351(12) → 355(12b) → 361(09 report)` ↔ `master_batch_273.sh:153, 197-200`
· **무엇**: `STAGE()` 는 성공 즉시 마커를 찍는다. 순서가 **12 → 12b → 09** 다. 그런데 master 의 완료 판정은
  ```bash
  if [ -f "$outdir/STAGE_12.DONE" ] || [ -f "$outdir/STAGE_12b.DONE" ]; then echo "done"; return; fi
  ```
  즉 **STAGE_12 하나만 있어도 done**. Stage 12b(train_predictor)나 Stage 09(FINAL_REPORT.json 작성)가 죽으면 그 실행에서는 `❌ FAIL` 로 찍히지만, **다음 master 호출부터는 `SKIP (status=done)`** 이라 다시는 돌지 않는다. 결과: `dataset.csv` 는 있고 `FINAL_REPORT.json` 은 없는 “완료된” 캐스케이드. 질문하신 *“STAGE_12*.DONE 이 찍혔는데 내용이 비어 있는 경우가 가능한가”* → **가능하다. 그것도 자동 복구가 안 되는 쪽으로.**
· **바로 아래 항목이 그 방아쇠다** — Stage 12b 는 pandas/sklearn 이 없으면 무조건 죽는다.
· **고치는 법**: 마커 이름을 하나로 합치거나(`STAGE_FINAL.DONE` 을 09 report 뒤에 찍는다), `cascade_status()` Layer 1 을 **가장 마지막 스테이지 마커**(`STAGE_09.DONE`)로 바꾼다. 지금은 “끝난 표시”가 끝나기 두 스테이지 전에 붙어 있다.

---

## [치명] Stage 09c·12b(`train_predictor.py`)는 **pandas·sklearn 이 없으면 rc=1** → 273개가 15시간씩 돌고 나서 전부 abort. preflight 는 그걸 **안 본다**

· **어디**: `tools/doping/train_predictor.py:97` ↔ `tools/doping/preflight.py:33-38`(REQUIRED_TOOLS)
· **무엇**: 2026-09-09 사고와 **정확히 같은 모양**이다 — 앞 스테이지들이 정상으로 오래 돌고 나서 뒤에서 죽는다. 다만 이번엔 코드 계약이 아니라 **환경 계약**이다.
  ```
  $ python3 tools/doping/train_predictor.py --csv /tmp/t.csv --out_dir /tmp/tp --mode with_structure
  Stage09c/12b rc=1
  Need pandas + sklearn: No module named 'pandas'
  ```
  preflight 의 `REQUIRED_TOOLS` 는 `site_preference.py … run_anneal.py` **6개 .py 가 ast.parse 되는지**만 본다. `grep -n "pandas\|sklearn\|mp_api" tools/doping/preflight.py` → **0 건**. 즉 preflight 는 UMA 는 검증하고 후반부 스테이지의 의존성은 하나도 검증하지 않는다. Stage 09c 는 Stage 02(3–8h)·07(3–5h)·08(3–5h) 뒤에 온다 — 캐스케이드당 **15시간 뒤에** 알게 된다.
  master 마지막의 통합 CSV 블록(`master_batch_273.sh:345 python3 -c "import pandas…"`)도 같은 의존이고, 여기는 rc 검사조차 없어서 3개월 끝에 트레이스백 한 줄만 남기고 `unified_dataset_273.csv` 없이 “Done.” 을 찍는다.
· **⚠ gabia 의 uma env 에 pandas/sklearn 이 있는지는 확인 못 했다** (원격 접속 안 함). 있으면 무해하고, 없으면 273개 전멸이다. **던지기 전에 gabia 에서 `python3 -c "import pandas, sklearn; print('ok')"` 한 줄이면 끝난다.**
· **고치는 법**: preflight 에 import 검사 섹션을 추가한다 — `pandas`, `sklearn`, `mp_api`(09e/09f), `scipy`(run_md_sigma의 linregress). 이건 preflight 의 존재 이유 그 자체다.

---

## [치명] master 가 권하는 감시판이 273 레이아웃을 **못 본다** → 이번 같은 전멸이 화면상 안 보인다

· **어디**: `master_batch_273.sh:69`(“Monitor: bash tools/doping/watch_phase1_v22.sh”) ↔ `watch_phase1_v22.sh:73, 84, 143, 165`
· **무엇**: master 는 `$BATCH_DIR/${cmp}_${conc_label}` (`Li2O_x002`) 에 쓰는데, 감시판은 `cmp_dir="$BATCH_DIR/$cmp"` (`Li2O`) 를 본다. **접미사가 없다.** 그래서 3개월 내내 `Phase 1A 0/37`, `Phase 1B 0/64`, 전 화합물 `·`(미시작)로 뜬다. 게다가 총수가 105 이고 존재하지 않는 `TIER_D` 4종을 센다 — v105 캠페인 화면이 그대로 남아 있다.
· `watch_cascade.sh` 쪽은 273 을 알지만 다른 데서 샌다:
  - `:7` 기본 `BATCH_DIR=/data/work/runs/multi_category_2026_05_26_v23` ↔ master 기본은 `…_2026_05_19_v22`. **인자 없이 돌리면 빈 디렉터리를 감시**하고 “🔴 5분내 갱신 없음” 만 찍는다.
  - `:34` `DONE_RUN=$(grep -c "✓ DONE" "$LOG")` — **`❌ FAIL` 도 `⚠ TIMEOUT` 도 한 번도 세지 않는다.** 2026-09-09 상황(273개 전부 Stage 04 rc=2)에서 이 화면은 “Step N/273 진행 중, 이번 런 완료 0개” 로 뜬다. 0 이 “아직 첫 개가 안 끝났다” 인지 “전부 죽었다” 인지 구분이 안 된다.
  - `:63` liveness 는 `find "$D" -name "*.log" -newermt "-5 min"` 하나다. **빠르게 죽으면서 로그를 계속 새로 쓰는 것도 🟢 진행중** 이다. 이번 사고의 “로그만 보면 진행 중처럼 보였다” 가 이 줄이다.
  - `:25` 폴백 `ls -t "$D"/master_*.log` — master 의 로그는 `$BATCH_DIR/_master_logs/master_273_*.log` (한 단계 아래)라 이 글롭에 안 걸린다.
· **고치는 법**: 감시판이 **실패를 1급 시민으로** 보여야 한다 — `❌ FAIL`/`⚠ TIMEOUT` 카운트, 그리고 “마지막 5개 캐스케이드가 어느 STAGE 에서 끝났는지”. watch_phase1_v22 는 `${cmp}_${conc}` 로 고치거나 273 전용으로 갈아엎는다(지금 상태로는 켜 두는 게 **더 위험하다** — 0/105 를 보고 “아직 시작 안 했나” 로 읽는다).

---

## [치명] 이전 273 캠페인의 **산출물이 농도축 붕괴를 실측으로 증명한다** — 재계산해도 같은 자리로 간다

· **어디**: `db/properties/cascade_v23_all.csv` (3615행, 저장소 정본)
· **무엇**: 앞 감사자가 코드로 예측한 `actual_x = 0.25` 붕괴가 **이미 나온 데이터에 그대로 찍혀 있다.**
  ```
  rows 3615
  concentration: ['0.25']          ← 3615행 전부 단일값
  n_fu_actual:   ['4']             ← 전부 4
  n dopant: 101 ;  dopants with >1 concentration: 0 / 101
  sigma_300K_S_cm_NE: non-null 0   ← Stage 10 산출물 0건
  anneal_delta_E_meV: non-null 681 / 3615
  ```
  즉 (1) 농도축은 **한 번도 존재한 적이 없고**, (2) 논문 핵심인 σ_Li 는 **이전 캠페인에서 0건** 이다. `master_batch_273.sh` 는 그 상태에서 supercell 을 여전히 `1,1,1` 로 세 번 넘기므로(`:318`), 지금 던지면 3615행짜리 같은 표를 3배 크기로 다시 만든다.
· **고치는 법**: 던지기 전에 농도별 supercell 을 정한다(`kb/methodology/hard_dopant_handling_protocol.md` 에 이미 판정이 있다). σ 0건의 원인은 내 구간 밖이라 확인 못 했다 — **Stage 10 이 왜 아무것도 안 남겼는지는 던지기 전에 따로 규명해야 한다.**

---

## [주의] master 의 완료 카운트가 **2배**로 나온다

· **어디**: `master_batch_273.sh:338`
· **무엇**: `find "$BATCH_DIR" -maxdepth 2 -name 'STAGE_12*.DONE' | wc -l` 인데 완주한 캐스케이드는 `STAGE_12.DONE` 과 `STAGE_12b.DONE` **둘 다** 가진다.
  ```
  actual complete cascades = 2
  master line 338 reports: 4
  ```
  3개월 끝의 최종 보고가 `546 / 273 cascades complete` 로 뜬다. 12b 에서 죽은 것은 1로 세니 “절반쯤 성공” 처럼 보이는 구간도 생긴다.
· **고치는 법**: `-name 'STAGE_12.DONE'` 으로 고정하거나 `cascade_status()` 를 재사용한다.

---

## [주의] Stage 10·11 에 **resume 이 없다** — 24h timeout 과 만나면 영원히 못 끝내는 캐스케이드가 생긴다

· **어디**: `run_md_sigma.py:334` · `run_cathode_interface.py:282,313` (둘 다 `_incremental.json` 을 **쓰기만** 한다) ↔ `master_batch_273.sh:312`
· **무엇**: 두 스테이지 모두 `cathode_interface_summary_incremental.json` / `sigma_md_summary_incremental.json` 을 중간저장하지만, **다시 읽는 코드가 없다**(`grep -n "incremental|resume" ...` 결과에 read 가 0건). STAGE_11.DONE 은 전부 끝나야 찍히므로, 24h 에 걸려 잘리면 그때까지의 GPU 시간이 전부 버려지고 다음 master 패스에서 **처음부터** 다시 돈다.
  tier_cascade 자신의 스테이지 견적을 더하면 02(3–8h)+07(3–5h)+08(3–5h)+10(TOP_K_SIGMA=2 ⇒ ~5h)+11(5–15h) ≈ **16–38h** 다. 상한 쪽 화합물은 매 패스마다 24h 를 태우고 아무것도 못 남긴다 — 무한루프다. master 헤더의 “per-cascade ~17h / ~193 days” 는 **하한**만 쓴 값이다.
· **고치는 법**: 두 러너가 시작 시 `_incremental.json` 을 읽어 이미 끝난 (winner, T) / (winner, baseline) 을 건너뛰게 한다(구조는 이미 있다 — 읽기만 붙이면 된다). 그리고 timeout 을 36h 로 올리거나, 초과 시 `⚠ TIMEOUT` 을 별도 파일로 남겨 다음 패스가 우선 처리하게 한다.

---

## [주의] `MP_API_KEY` 유무에 따라 **같은 데이터가 abort 되기도, 조용히 통과하기도** 한다

· **어디**: `tools/doping/ehull_check.py:89-101` vs `:114-116`
· **무엇**: 키가 없으면 skip json 을 쓰고 `return` → rc=0(정상 스킵). 키가 **있으면** 계속 진행해서
  ```python
  records = ranking.get('ranked_by_post_anneal', [])[:args.top]
  if not records:
      raise SystemExit(f"No records in {args.ranking}")     # rc=1 → Stage 09e FAILED → 캐스케이드 abort
  ```
  앞 감사자가 잡은 “Stage 06 이 조인 0건이어도 rc=0 으로 빈 랭킹을 쓴다” 와 결합하면: **빈 랭킹은 키 없는 환경에서 조용히 끝까지 흘러가고, 키 있는 환경에서는 09e 에서 폭발한다.** 두 gabia/kgy 사이에 결과가 갈리고, 원인은 데이터가 아니라 환경변수다.
· **고치는 법**: 빈 랭킹 판정을 Stage 06 으로 올린다(그게 옳은 자리다). 09e/09f 는 빈 입력을 skip 사유로 기록하고 rc=0 으로 끝낸다 — 지금은 반대로 돼 있다.

---

## [주의] `run_md_sigma.py` 의 MSD 창이 규약(2–50 ps 고정)이 아니라 **“뒤쪽 절반”** 이다 — 그런데 `convention_check` 는 `0 위반` 을 찍는다

· **어디**: `tools/doping/run_md_sigma.py:136-138` ↔ `tools/convention_check.py:45-47, 61-66`
· **무엇**:
  ```python
  fit_start = n_frames // 2
  slope, intercept, r, _, _ = linregress(dt_arr[fit_start:], msd[fit_start:])
  D_cm2s = slope / 6 * 1e-16
  ```
  자유절편(①)은 지킨다. 그런데 창(②)은 **고정 2–50 ps 가 아니라 런 길이의 후반부** 다. 캐스케이드가 `--prod_ps 50` 을 주므로 실제 창은 **25–50 ps**. `--prod_ps` 를 바꾸면 창이 조용히 따라 움직인다. 규약과 다른 창으로 나온 σ·Ea 가 `dataset.csv` → ML predictor → FINAL_RANKING 으로 들어간다.
  게이트가 못 보는 이유는 명확하다 — `WINDOW_ASSIGN` 은 **이름에 window 가 든 변수 대입**만, `ARG_DEFAULT2` 는 **argparse 2원소 기본값**만 본다. 여기는 둘 다 아니고 **계산된 인덱스**다.
  ```
  $ python3 tools/convention_check.py | tail -1
  RESULT: 0 위반 — 2026-08-11 기준선 유지
  ```
  convention_check 자신의 주석(`:60`)이 “**통과했다는 것과 안 봤다는 것은 다르다**” 라고 적어 놨는데, 한 층 더 아래에서 같은 일이 벌어지고 있다.
· **고치는 법**: `run_md_sigma.py` 에 `--fit_window_ps` 를 `default=(2.0, 50.0)` 으로 노출하고 그걸 쓴다(그 순간 게이트의 ⑥ 규칙에 걸려 기계가 보게 된다). 또는 게이트에 “MSD 회귀 직전의 슬라이싱이 리터럴 창에서 오지 않으면 **미해결로 보고**” 규칙을 추가한다.

---

## [주의] Stage 02 가 **완화한 구조를 버린다** — Stage 04 는 미완화 원본에서 500 K MD 를 시작한다 (설계원칙 #2 위반)

· **어디**: `run_uma_screening.py`(구조 write 0건) → `select_winners.py` → `run_anneal.py:352`
· **무엇**: Stage 02 는 구조마다 `FIRE(..., steps=1500)` 를 돌려 놓고 `uma_results.json` 만 쓴다 (`grep -n "write" run_uma_screening.py` → `baseline.json` 과 결과 json 두 줄뿐, 완화 구조 저장 없음). Stage 04 는 winners 레코드의 `xyz_file` 을 읽는데 그건 **Stage 01 이 만든 미완화 치환 구조**다. 즉 cascade 헤더의 *“No duplication — each anneal / relax happens exactly once”* 가 지켜지지 않고, 3–8 시간짜리 최고비용 스테이지의 기하 결과가 **버려진다**.
  물리적으로도 문제다: Stage 05 를 미완화 구조에 돌리면 안 되는 이유(CR-3, `tier_cascade.sh:200-202`)와 같은 논리로, 원자가 겹쳐 있을 수 있는 미완화 구조에서 500 K Langevin 을 바로 시작하면 초기 힘이 크다.
· **⚠ 실제로 Stage 04 가 그 때문에 실패하는지는 확인 못 했다** (UMA 필요, `fairchem` 없음). 코드 경로만 확인했다.
· **고치는 법**: Stage 02 가 완화 구조를 `02_screen/relaxed/<name>.xyz` 로 저장하고 결과 레코드에 `relaxed_xyz` 를 남긴다. Stage 04 는 있으면 그걸, 없으면 `xyz_file` 을 쓴다. 저장 비용은 무시할 수준이다(구조당 4.7 KB, 아래 실측).

---

## [주의] 3개월짜리 GPU 런처인데 **conda 활성화·GPU 여유 확인·중복실행 가드가 하나도 없다** — 저장소의 다른 러너엔 다 있다

· **어디**: `master_batch_273.sh` · `tier_cascade.sh` 전체
· **무엇**: 실측 grep 결과, 두 파일에 `conda activate` / `nvidia-smi` / `pgrep` / `flock` 이 **0 건**이다. 반면 같은 폴더의 다른 러너는 전부 갖췄다 —
  - `run_as2s3_recover.sh:61,85-86` (중복 가드 + nvidia-smi VRAM 확인)
  - `run_force_check_scf.sh:101-102,247-248` (flock + `MIN_FREE_MIB`)
  - `run_y_dft.sh:32,80,93` (자기 자신 오카운트 주의까지 적어 놓음)
  CLAUDE.md 공통 규율(“실행 스크립트에 pgrep 중복실행 가드”)과 gabia 규율(“pw.x와 UMA 동시 실행 금지 — nvidia-smi로 확인 후 실행”)이 **하필 가장 오래 도는 스크립트에만 빠져 있다.** 어제 조사도 이걸 봤다(`.v3_survey/…doping_58…md:127` 이 master_batch_273·tier_cascade 를 12개 무가드 목록에 넣었다) — 하지만 “끝난 캠페인” 분류라 P0 로 안 올라갔다.
  · 환경 활성화가 없다는 건 `nohup bash master_batch_273.sh` 를 uma env 밖에서 던지면 **Stage 00 preflight 가 `fairchem import failed` 로 exit 1** → 273개가 각 몇 초씩 FAIL 하고 3분 만에 “끝난다”. 시끄러워서 다행이지만, 위의 [치명] watch 문제와 겹치면 화면에는 안 뜬다.
· **고치는 법**: master 맨 앞에 ① `flock -n` 중복 가드(`run_force_check_scf.sh:101` 구현 복사), ② `python3 -c "import fairchem, pandas, sklearn"` 확인, ③ 캐스케이드마다 던지기 전 `nvidia-smi --query-compute-apps` 로 남의 잡 확인.

---

## [주의] `.master_lock` 이 지워지지 않고, Layer 3 “30분 룰” 이 **방금 죽은 캐스케이드를 running 으로 스킵**한다

· **어디**: `master_batch_273.sh:165-172(Layer 3), 174-182(Layer 4), 305-307`
· **무엇**: 앞 감사자가 지적한 그대로다. 한 가지 더: `.master_lock` 에 들어가는 PID 는 캐스케이드가 아니라 **master 자신의 `$$`** 다(`:307`). 그래서 master 가 도는 동안 그 master 가 한 번이라도 손댄 **모든** 디렉터리가 Layer 4 에서 `locked` 로 잡힌다. 두 번째 master 를 띄우면 (중복 가드가 없으니 띄울 수 있다) 첫 master 가 이미 지나간 실패 캐스케이드까지 전부 `locked` 로 건너뛴다. master 종료 후엔 죽은 PID 라 stale 로 정리되지만, **PID 재사용**이 걸리면 그 캐스케이드는 영구 스킵이다.
· **고치는 법**: 캐스케이드 종료 시 `trap ... rm -f "$OUT/.master_lock"`. Layer 3 은 삭제하고 Layer 4·5(PID 기반)만 남긴다 — Layer 3 은 중복이면서 더 위험하다.

---

## [참고] 디스크는 병목이 아니다 (실측) — 다만 preflight 의 **고정 5 GB 문턱**은 273번짜리 하드 abort 스위치다

· **실측** (이 상자, CPU):
  ```
  base 구조 52 atoms
  md.traj 51 frames (25000 steps / log_every 500) = 143,552 B = 140 KB
  구조 1개 xyz = 4,655 B
  ```
  스테이지별 산출물을 코드로 확인한 결과 **큰 이진 데이터를 쓰는 곳이 없다** — `run_uma_screening` 은 json 2개, `bvse_proxy` 는 격자를 저장하지 않고 json 만, `run_md_sigma` 는 `msd_<T>K.dat`(`save_every=20` ⇒ 1250행), Stage 07/08/11 은 json, `train_predictor` 는 작은 pickle. winners 가 화합물당 1–6개이므로 **캐스케이드당 대략 10–60 MB, 273개 합쳐 3–16 GB** 로 추정한다.
  ⚠ 이건 **추정**이다 — 실제 캐스케이드를 끝까지 돌려 `du` 를 재지 못했다(UMA 없음).
· **문제는 절대량이 아니라 판정 방식**이다. `preflight.py:60` 은 `expected_gb: float = 5.0` 고정이고, `main()` 은 `n_pass != n_total` 이면 exit 1 → 캐스케이드 abort. gabia `/data` 여유가 어떤 이유로든 5 GB 밑으로 내려가는 순간 **남은 캐스케이드 전부가 Stage 00 에서 즉사**한다. kgy 가 92% 라는 실측이 있는데 gabia 여유는 **확인 못 했다** (원격 접속 안 함).
· **고치는 법**: 문턱을 남은 캐스케이드 수 기반으로(`남은수 × 실측 캐스케이드 크기 × 1.5`), 그리고 부족 시 abort 가 아니라 **경고 + master 에게 일시정지 신호**로.

---

## [참고] 어제 조사의 **분류 때문에 안 본 곳**이 정확히 지금 던질 파이프라인이다

· **어디**: `.v3_survey/repo_tools_doping_58_….md:18` 과 `:102-104`
· **무엇**: 원문 그대로 —
  > `:18` “master_batch_273.sh · tier_cascade.sh · run_compound_batch.sh — **끝난 캠페인**이지만 273 슬롯 데이터를 어떻게 만들었는지의 유일한 기록이다.”
  > `:102-104` “watch_phase1_v22.sh · … · watch_cascade.sh … **전부 끝난 캠페인의 감시판이다** … `tools/doping/_archive/` 로 옮기고”
  즉 어제의 권고를 따랐으면 **지금 던질 런처 3개와 그 감시판 2개가 전부 `_archive/`** 로 들어갔다. `:127` 에서는 master_batch_273·tier_cascade 의 중복실행 가드 부재를 정확히 짚었는데, “끝난 캠페인” 분류 때문에 P0 로 안 올라갔다.
· **고치는 법**: 분류를 파일명·언급빈도가 아니라 **“다음에 실행할 것인가”** 로 바꾼다. `_archive/` 후보에 넣기 전 `git log -1 --format=%cr <file>` 과 “이 스크립트를 다음 4주 안에 돌릴 계획이 있는가” 를 1저자에게 묻는 절차가 필요하다.

## [참고] 그 밖 세 가지

1. **09c/12b 가 한 화합물짜리 데이터로 ML 을 546번 학습한다.** `COMPOUND_FILTER` 때문에 캐스케이드당 행이 5–30개이고 `groups = d['dopant']` 도 사실상 한 종이다. 정작 통합 데이터(`unified_dataset_273.csv`)로는 **어디서도 학습하지 않는다**(master 는 CSV 만 합치고 끝난다). 시간 손실은 작지만(수 초), 산출물 546개가 전부 의미 없는 모델이다.
2. **master 가 `cd` 를 안 한다.** `bash tools/doping/tier_cascade.sh` 가 상대경로라 repo root 밖에서 `nohup` 하면 273개가 `rc=127` 로 즉시 실패한다. 헤더 usage 는 `cd /data/work/repo` 를 사람에게 시킨다 — 스크립트가 스스로 하면 된다(tier_cascade 는 `SCRIPT_DIR` 로 이미 그렇게 한다).
3. **Stage 05 는 조용히 폴백하는데 Stage 07/08 은 시끄럽게 죽는다.** 같은 조건(`04_anneal/*/post_relax.xyz` 없음)에서 규약이 반대다 — 실행 확인:
   ```
   run_mlip_postproc.py: error: argument --xyz: expected at least one argument   (rc=2 → abort)
   ```
   Stage 05 의 폴백은 리뷰가 금지한 계산을 기본값으로 수행하고, Stage 07 은 abort 한다. 둘 중 하나로 통일해야 한다(앞 감사자 의견대로 **금지 + 명시 opt-in** 이 맞다).

---

## 못 본 것 — 무엇을 안 읽었고 왜

- **GPU·UMA 가 필요한 것은 하나도 실행하지 못했다.** `fairchem` 없음(`ModuleNotFoundError: No module named 'fairchem'`). 그래서 실제 캐스케이드 1회를 끝까지 돌려 **디스크 실측·스테이지 실소요·timeout 도달 여부를 재지 못했다.** 디스크 추정치(3–16 GB)와 소요 추정(16–38h)은 **코드에서 유도한 값**이고, 후자는 tier_cascade 헤더의 자기 신고 견적에 의존한다.
- **이 상자에 `pandas` 도 없다.** 그래서 master 마지막의 통합 CSV 블록(`:345-389`)을 **실행해서 검증하지 못했다** — 컬럼 이름 충돌·`rsplit('_x',1)` 파싱 같은 건 코드 읽기로만 봤다. 반대로 그 덕에 [치명 3]의 rc=1 을 실물로 잡았다.
- **원격 서버를 하나도 보지 않았다** (읽기 전용 감사 + GPU 금지). 따라서 **gabia 의 `/data` 여유·uma env 의 pandas/sklearn·MP_API_KEY 설정 여부·다른 잡의 GPU 점유는 전부 확인 못 했다.** 위 세 항목([치명 3]·[주의 MP key]·[참고 디스크])은 **1저자가 gabia 에서 세 줄로 확인해야 판정이 닫힌다.**
- **`stage_report.py`(419줄)는 argparse 와 main 만** 읽었다. `2>/dev/null || true` 로 완전히 무음이라 실패해도 캐스케이드에 영향이 없어 우선순위를 내렸다 — 다만 **“보고서가 조용히 안 만들어지는” 경로**로는 남아 있다.
- **`combine_rankings.py`(773줄)·`collect_dataset.py`(423줄) 는 입력 경로 표(`SOURCES` / `load(...)`)만** 읽었다. 스테이지 간 배선 확인에 필요한 부분만 봤고, 점수 결합 로직·NaN 처리는 안 봤다.
- **`analyze_screening.py`·`axis_corr_csv.py`·`predict_*.py`·`chain_predict.py` 는 열지 않았다** — 캐스케이드가 부르지 않는다(확인: `tier_cascade.sh` 전문 grep). 다른 경로로 불리는지는 확인 안 했다.
- **`master_batch_105.sh`·`watch_dualx*.sh`·`watch_status.sh`·`watch_y_site.sh` 는 안 읽었다** (273 경로 밖).
- **resume 을 실행으로 시험하지 못했다.** `STAGE_*.DONE` / `CASCADE_VERSION` / `cascade_status()` 5계층은 **코드 읽기 + 마커 파일 모의**로만 판정했다([주의] 완료 카운트 2배는 실제 파일로 재현했다). 273 배치를 돌릴 수 없어서 “Layer 3 이 실제로 몇 개를 스킵하는가” 는 못 쟀다.
- **`cascade_v23_all.csv` 는 헤더·`concentration`·`n_fu_actual`·null 개수만** 봤다. 그 캠페인이 어느 커밋·어느 BATCH_DIR 에서 나왔는지, σ 0건의 원인이 Stage 10 미실행인지 실패인지는 **확인 못 했다.**
- **Stage 00–06 내부는 다른 감사자 담당이라 재검증하지 않았다.** 그쪽 결론을 참조만 했고(특히 Stage 06 조인 0건, `--method cluster`), 내가 다시 실행해 확인한 것은 `cascade_v23_all.csv` 의 농도 붕괴 하나뿐이다.
