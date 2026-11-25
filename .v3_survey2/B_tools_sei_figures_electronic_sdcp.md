# v3_survey2 — 조사 B: tools/sei · tools/figures · tools/electronic · tools/sdcp · tools/ionic

읽음 216/216 (기계검사) — 본문 11 · 헤더/부분 9 · 안 봄 196

⚠ 먼저 자백: `tools/figures/plot_nd_sei_gaps.py --help` 를 돌렸다가 `docs/figures/nd_sei/sei_product_gaps_O.{png,pdf}` 두 개를 덮어썼다. `git checkout --` 로 되돌렸고 지금 `git status` 에 그 두 파일은 없다 (webapp 5개 수정은 내가 건드린 게 아니라 원래 있던 것). 그리고 그게 아래 [참고] 항목 하나가 됐다.

---

```
[치명] run_sei_neb.sh 의 마지막 결산(collect_neb)이 **두 기계 어디서도 db 를 못 쓴다** — 조용히
· 어디: tools/sei/run_sei_neb.sh:412 · tools/sei/collect_neb.py:52-56, 461-478
· 무엇: NEB 을 다 돌리고 나서 부르는 회수기가 인자 없이 호출되는데,
        (1) gabia(v2/v3 루트가 다 있는 곳) → 축소 가드에 걸려 **쓰기 거부**
        (2) kgy(기본 WORK=/data/work/runs/sei_neb) → "존재하는 루트가 없다" 로 **아무것도 안 함**
        어느 쪽이든 `|| true` 가 종료코드를 삼켜서 화면엔 완료처럼 보이고 db 는 안 바뀐다.
        원인은 2026-09-03 `--merge` 로 db 의 roots 에 `sei_neb` 가 들어갔는데, 회수기의
        기본 ROOTS 4개에는 그게 없어서 매 회수가 "루트가 줄어든다" 로 판정되기 때문이다.
· 근거: 샌드박스에서 실제로 재현했다 (repo db 는 안 건드리고 임시 cwd 로 복사해서 실행).
    (1) gabia 흉내 (v2·v3 루트 실물 생성):
       ⛔ 이번 회수는 루트가 **줄어든다** — 쓰지 않는다.
          기존 ['sei_neb','v2','v2_cc333','v2_ccpath','v3'] → 이번 ['v2','v3']
          (사라질 루트: ['sei_neb','v2_cc333','v2_ccpath'])
    (2) kgy 흉내 (인자 없이 = 러너가 부르는 그대로):
       ⚠ 루트 없음: /data/work/runs/sei_neb_v2 … (4줄)
       ⛔ … 에 존재하는 루트가 없다 — build_neb_inputs.py 부터
  호출부는 실제로 인자가 없다: `python3 "$REPO/tools/sei/collect_neb.py" || true`
· 고치는 법: 412행을 `python3 "$REPO/tools/sei/collect_neb.py" --merge || true` 로 바꾸고,
  `collect_neb.py:52` 의 ROOTS 와 `watch_gabia.py:41` 의 NEBW 에 `/data/work/runs/sei_neb`
  를 추가한다. 그리고 `|| true` 를 걷어내거나 최소한 실패 시 한 줄 경고를 찍게 한다 —
  지금은 "안 써졌다" 가 로그 속에 묻힌다. (열려 있는 작업 #8 이 이 증상의 수동 우회다.)
```

```
[치명] collect_neb 의 기본 루트 목록에 **러너 자신의 기본 WORK 가 없다** (계약 불일치)
· 어디: tools/sei/run_sei_neb.sh:23  vs  tools/sei/collect_neb.py:52-56  vs  tools/sei/watch_gabia.py:41-45
· 무엇: 러너 기본 `WORK=/data/work/runs/sei_neb`. 회수기 기본 ROOTS = v2 · v2_ccpath ·
        v2_cc333 · v3. 감시기 NEBW 도 같은 4개. 즉 **기본값으로 돌리면 회수도 감시도 안 된다.**
        `build_neb_inputs.py:49` 의 WORK 기본값도 `/data/work/runs/sei_neb` 이라 생성-실행 쪽
        기본값과 회수-감시 쪽 기본값이 통째로 갈라져 있다. 이번 cascade `--seed` 사고와 같은 모양이다.
· 근거: 위 (2) 재현 출력 · db/properties/sei_neb.json 의 roots 에는 이미 'sei_neb' 가 있다
        (누가 손으로 --merge 를 돌린 흔적) → 기본 경로로는 도달할 수 없는 상태.
· 고치는 법: 세 곳의 기본 루트를 한 파일(예: tools/sei/neb_roots.sh/py)에서 읽게 하고,
  `qe_env.sh` 를 뽑았던 것과 같은 방식으로 정본을 하나로 만든다.
```

```
[주의] run_sei_neb.sh 의 EXIT trap 이 **엉뚱한 락 파일**을 지운다
· 어디: tools/sei/run_sei_neb.sh:167 · 174 · 222
· 무엇: 167에서 LOCK="$WORK/.run_sei_neb.lock", 174에서 `trap 'rm -f "$LOCK"' EXIT`
        (작은따옴표라 **종료 시점에** 전개된다). 그런데 222에서 `LOCK=/tmp/sei_neb.lock` 로
        덮어쓴다 → 종료 시 지워지는 건 /tmp 쪽이고, `$WORK/.run_sei_neb.lock` 은 **영원히 남는다**.
        남은 파일의 pid 가 나중에 재사용되면 168행 `kill -0` 가 참이 되어
        "이 작업 폴더가 이미 돌고 있다" 로 **멀쩡한 실행을 막는다**. 즉사도 아니고 로그도 없다.
· 근거: 167/174/222 세 줄이 같은 변수명을 쓴다. 222 이후 LOCK 은 다시 안 바뀐다.
· 고치는 법: 222행의 변수명을 `FLOCKF=/tmp/sei_neb.lock` 로 분리하고 `exec 9>"$FLOCKF"`.
  덤으로 223행의 중복 감지가 `exit 0` 인데 169행은 `exit 1` 이다 — 종료코드도 맞춰라.
```

```
[주의] parse_eig_gap.py — 금속 가드가 없어 **조용히 "갭"을 낸다**. 정본 값 계보에 쓰인 도구다.
· 어디: tools/electronic/standard_dos/parse_eig_gap.py:39-44
· 무엇: `vbm = e[e<=EF].max(); cbm = e[e>EF].min()` 뿐이다. 금속이면 EF 가 밴드 안이라
        "가장 가까운 두 고유값 차" 라는 무의미한 작은 양수를 **아무 경고 없이** GAP 으로 찍는다.
        sei 쪽 `extract_gap.py` 는 electronic_class 레지스트리를 보고 metal 이면 거부하는데
        (tools/sei/extract_gap.py:28-41) 이쪽엔 그 게이트가 없다.
        또 EF 줄이 없으면(= occupations='fixed' 정본 경로) 18-20행에서 그냥 죽는다.
· 근거: db/governance/artifacts.json:110 이 "comp1 2.066 / modelc 2.099 는 parse_eig_gap.py 가
        tetrahedra_opt nscf .out 을 재파싱해서 낸 값" 이라고 적어 놨다. 즉 canonical 계보에 있다.
        (canonical_registry.json:52 가 fixed-occ 재계산으로 값 자체는 재현됐다고 닫아 놨으니
         **지금 값이 틀렸다는 뜻은 아니다** — 도구에 가드가 없다는 뜻이다.)
· 고치는 법: 두 줄이면 된다 — `e[e<=EF]` 와 `e[e>EF]` 사이 간격이 smearing width 안이거나
  EF 근처에 부분점유가 있으면 "metal/불확실" 로 찍고 GAP 을 내지 않는다.
  아니면 sei 쪽처럼 electronic_class 레지스트리를 참조하게 한다.
```

```
[주의] `extract_gap.py` 가 **두 개**다 — 알고리즘도 계약도 다른데 이름이 같다
· 어디: tools/sei/extract_gap.py (135행, `--nscf/--tag/--json`, 밴드 블록에서 VBM/CBM 계산,
        metal 레지스트리 게이트 있음)
        tools/electronic/standard_dos/extract_gap.py (31행, 위치인자 1개, QE 의
        'highest occupied, lowest unoccupied level' 줄을 정규식으로 읽기만 함)
· 무엇: 문서·kb·리뷰에서 "extract_gap.py" 라고만 쓰면 어느 쪽인지 알 수 없다. 실제로
        artifacts.json:109 은 "fixed-occ 경로인 extract_gap.py 는 EF 를 아예 안 찍는다" 라고
        쓰는데 그건 standard_dos 쪽이고, sei 쪽은 또 다른 물건이다.
        같은 폴더(standard_dos/)에 parse_eig_gap.py 까지 있어 셋이 뒤섞인다.
· 근거: 두 파일을 다 읽었다. diff 165줄, 공통 코드 없음.
· 고치는 법: standard_dos 쪽을 `read_homolumo_line.py` 처럼 하는 일이 드러나는 이름으로 바꾸고
  (호출부는 run_gap_nscf_gabia.sh:91/97/102 세 곳뿐이다), 어느 게 정본인지 kb 카드에 한 줄.
```

```
[주의] plot_cascade_insights.py — 그림 제목의 "47 dopants" 가 하드코딩, 결측치는 평균으로 메워 랭킹에 들어간다
· 어디: tools/figures/plot_cascade_insights.py:197 · 125-131 · 157
· 무엇: (1) 197행 suptitle 에 "47 dopants" 가 문자열로 박혀 있다. 그런데 17-18행이
          `CASCADE_CHAMP` 로 **회수분 90종**을 물려 병렬 생성하라고 스스로 안내한다.
          그 경로로 돌리면 90종 그림에 "47 dopants" 라고 적힌다 — 안 터지고 라벨만 틀린다.
       (2) `norm()` (125행)이 NaN 을 그 열의 평균으로 채운 뒤 composite score 를 만든다.
          `_elastic_ok()` 가 비물리 탄성행(B_hill<0 등)을 걸러 NaN 을 만들면, 그 도펀트는
          "평균적인 연질" 점수를 받고 그대로 cascade_v23_ranked.csv 에 순위가 매겨진다.
          157행도 같은 대체를 한 뒤 Pearson r 을 뽑아 "Key correlations" 로 출력한다
          (평균 대입은 상관을 부풀린다). 어느 쪽도 CSV·그림에 표시가 없다.
· 근거: db/properties/cascade_v23_champions.csv 는 지금 47종 (확인함) — 기본 경로에선 맞다.
        틀리는 건 문서화된 env 오버라이드 경로다. `_elastic_ok` 주석 자체가 Na2S_x100
        (B_hill=-36.27 GPa)이 평균에 섞여 틀린 발견을 만든 전례를 적어 놨다.
· 고치는 법: 197행을 `f"... , {len(D)} dopants"`. norm()/corrcoef 에서 대체가 일어난 셀 수를
  세어 CSV 각 행에 `n_imputed` 를 싣고, 그림 각주에 "imputed" 를 찍는다.
```

```
[주의] phaseB_v7c_dft_binding.py 가 **철회된 보고량**을 아무 경고 없이 다시 만든다
· 어디: tools/sdcp/phaseB_v7c_dft_binding.py:16-17 (docstring)
· 무엇: "E_bind(tag) = E(complex) - E_slab - E_mol(tag) / Verdict = sign & size of
        E_bind(doped) - E_bind(neutral)" 를 산출물로 선언한다. 그게 정확히
        citation_hazards.json 의 HZ-sdcp-phaseb-dftu-eads 가 **"아무것도 인용하지 않는다"**
        로 막은 양이고, CLAUDE.md 계산 규율이 "제약된 기준에서 자유로운 복합체를 뺐다" 로
        정정한 그 델타다. 도구 어디에도 보고량 카드·상태선택 정책·마감 파일 참조가 없다.
        지금 러너 4개(run_phaseB_sdcp_v2/v3, refine, slabfirst)가 그대로 이걸 부른다.
· 근거: docstring 16-17행 원문. 플래그 계약은 실물로 대조했고 **불일치는 없다** (러너가 넘기는
        --min_image_gap/--no_fsm/--seed_radical/--slab_coord_tol/--complex_doped2 등 전부
        add_argument 에 있다). 문제는 인자가 아니라 **재는 양**이다.
· 고치는 법: docstring 맨 위와 README_harvest.txt 생성부에 "이 델타는 2026-08-28 회신 P 로
  철회됨 · db/properties/sdcp_doped_closed_2026_08_28.json · 재개 조건 밖에서 다시 열지 말 것"
  을 박고, 상태선택 정책(전 계 자유 바닥상태 or 선언된 대응 제약)을 인자로 강제한다.
```

```
[참고] plot_nd_sei_gaps.py 가 argv 를 무시해서 `--help` 만으로도 배포 그림을 덮어쓴다
· 어디: tools/figures/plot_nd_sei_gaps.py (전체 — __main__ 가드도 argparse 도 없다)
· 무엇: 어떤 인자를 줘도 그냥 본문이 돌아 docs/figures/nd_sei/sei_product_gaps_O.{png,pdf}
        를 다시 쓴다. 내가 조사 중에 실제로 그렇게 두 파일을 수정했다(복구함).
        같은 모양이 내 영역 uncited 파이썬 중 **36개**다 (top-level 에서 savefig/dump 를 하고
        __main__ 가드가 없는 것: plot_cascade_* 9개 · fig_comp2_* 6개 · plot_icohp_* 등).
        또 26-32행의 비-Nd 갭 5개(LiCl 6.65 / Li3PO4 5.73 / Li2O 5.24 / Li2S 3.90 / Li3P 0.70)는
        여전히 하드코딩이다 — 6-11행이 "하드코딩본이 준안정 예측 다형체를 물고 있었다" 고
        스스로 적어 놓고 Nd 절반만 db 로 옮겼다. 그리고 house_style 미사용 · CSV 미출력이다.
· 근거: 파일 전문 · `git status` 에 두 파일이 M 으로 떴다가 checkout 후 사라짐.
· 고치는 법: 본문을 `def main()` 으로 감싸고 `if __name__=="__main__"` 가드. 비-Nd 5종도
  db/properties 로 옮긴다(우리 sei_dft gap.json 과 MP 값을 섞지 않도록 출처 필드 분리).
```

```
[참고] figures/ 의 house_style·CSV 규율이 절반만 지켜진다
· 어디: tools/figures/ (내 영역 uncited 68개 중)
· 무엇: savefig 하면서 house_style 을 import 안 하는 것 36개, Origin-ready CSV 를 안 내는 것 17개.
        house_style.py 는 2026-07-16 에 들어왔는데, 그 **뒤에** 커밋된 것만도 10개다:
        plot_cascade_{branches,errorbars,esw,extra,insights,interactions,litransport,
        oxidation_vs_banik,synergy,v23_detail}.py (2026-08-13~16) · elf_planes_lpsocl.py (08-04).
· 근거: 68개 전수 정적 스캔 + 각 파일 git log -1.
· 고치는 법: cascade 그림 가족 10개를 한 번에 house_style 로 넘기거나, 아니면
  "cascade 계열은 예외" 를 kb 에 명시한다. 지금은 규율이 있는데 안 지켜지는 상태라 제일 나쁘다.
```

```
[참고] convention_check --selftests 의 FAIL 4 건이 전부 환경 문제라 코드 결함과 구분이 안 된다
· 어디: tools/convention_check.py --selftests 출력
· 무엇: `selftest 스윕: PASS 78 · FAIL 4 · skip 1`. 네 건은
        tools/litdb/pdf_text.py (pdfminer 없음 — 도구가 스스로 "Wiley 본문 못 읽음" 이라고 정직하게 실패)
        tools/seminar/{build_seminar_slide,rebuild_cascade_deck,revise_cascade_deck}.py (No module named 'pptx')
        전부 이 컨테이너에 선택 의존성이 없어서지 코드가 깨진 게 아니다. 그런데 요약 줄만 보면
        "죽은 selftest 4개" 로 읽힌다.
· 근거: 스윕 실행 결과 + pdf_text.py --selftest 를 따로 돌려 `23/24 통과` 확인.
· 고치는 법: 스윕이 ModuleNotFoundError/의존성 부재를 `skip(dep)` 로 분류하고 요약을
  `PASS 78 · FAIL 0 · skip(dep) 4` 로 낸다. 그래야 진짜 FAIL 이 눈에 띈다.
```

```
[참고] 감시 스크립트가 37개 — 어느 게 그 기계의 정본인지 규칙이 없다
· 어디: tools/*/watch*.{py,sh} 37개 (내 영역: ionic/watch_all.py 1292행 2026-08-30,
        ionic/watch_kgy.py 1086행 2026-09-04, sei/watch_gabia.py 1184행 2026-09-01,
        electronic/watch_gap_nscf.sh 393행 2026-09-01, sei/watch_qe_relax.sh 368행 2026-09-06 …)
· 무엇: 셋 다 "그 기계 전체를 한 화면" 을 표방하는 대시보드인데 커버 범위가 서로 다르다
        (watch_all 의 --only 는 disorder|sdcp|committee|elf|bader|prereq|orca — NEB 이 없다.
         NEB 은 watch_gabia.py 가 본다. 그래서 위 [치명] 의 NEBW 불일치가 아무한테도 안 걸렸다).
· 근거: 파일 목록 + 각 커밋일 + watch_all.py 40-50행의 --only 선택지.
· 고치는 법: 기계별 정본 대시보드를 kb 카드 한 장에 못 박고, 나머지는 그 안의 섹션으로 흡수.
  최소한 watch_all 에 NEB 섹션을 붙여 루트 목록을 collect_neb 와 같은 파일에서 읽게 한다.
```

```
[참고] 자잘한 것 3개
· tools/ionic/run_comp1_supercell.sh:145-147 — `msd_diffusive_check.py --glob ... 2>/dev/null ||`
  로 stderr 를 버린다. 인자가 안 맞아 죽어도 원인을 못 본다. (지금은 --glob 계약이 맞다 — 확인함)
· tools/ionic/run_comp1_supercell.sh:120-121 — 주석은 "msd.json 이 있으면 건너뛴다" 인데
  코드는 ensemble_results.json 을 본다. 주석/코드 불일치.
· db/properties/citation_hazards.json HZ-sei-neb-retracted 의 why 가 "tot_charge=+1 + 끝점 미이완"
  인데, 지금 sei_neb.json 의 실제 철회 사유는 citability_contract_2026_08_16(셀 수렴 미시험)이다.
  값은 여전히 BLOCKED 라 결론은 안 바뀌지만 사유가 낡았다.
```

---

## 못 본 것 — 무엇을 안 읽었고 왜

- **본문을 읽은 건 11개뿐이다.** run_sei_neb.sh · qe_env.sh · collect_neb.py · run_sei_dft.sh · extract_gap.py(sei) · extract_gap.py(standard_dos) · parse_eig_gap.py · plot_nd_sei_gaps.py · run_comp1_supercell.sh · plot_cascade_insights.py · redo_stages.sh.
- **헤더/부분만** 본 것 9개: phaseB_v7c_dft_binding.py(1-120행 + add_argument 전부), watch_all.py(1-80), pdf_text.py(1-45 + selftest 실행), build_neb_inputs.py(add_argument만 — **1485행 본문 못 봄**), symmetric_saddle.py(**3043행 통째로 못 봄**), watch_gabia.py(NEBW 부분만, 1184행), run_phaseB_sdcp_v2/v3·refine·slabfirst(호출 블록만), vasp_cost_estimate.py(못 봄, 1339행).
- **본문을 한 줄도 안 본 것 196개.** 특히 아래는 우선순위가 높았는데 시간이 모자라 못 봤다:
  - `tools/sei/symmetric_saddle.py` (3043행, 참조 7, 2026-08-27) — 내 영역에서 제일 큰 미독 파일이다.
  - `tools/sei/build_neb_inputs.py` (1485행, 참조 15) — 위 [치명] 의 생성기 쪽 절반. WORK 기본값만 확인했다.
  - `tools/sdcp/vasp_cost_estimate.py` (1339행, 2026-09-08 = 내 영역 최신 커밋), `tools/sdcp/scfin_to_struct.py` (1682행, 09-07), `tools/litdb/extract_figures.py` (1666행).
  - litdb 논문별 추출기 20개(anderson/huang/jun/kim/lee/ren/richards/wang/zhou 계열) — 전부 안 봤다. 문헌 수치가 우리 db 로 새는지 확인 못 했다.
  - modelc_v3 9개 — 전부 2026-06-11/29 커밋이라 후순위로 뒀고 안 봤다.
  - `tools/electronic/` 37개 중 3개만 --help 를 돌렸다. run_lpsocl_bader_gabia.sh · run_lpsocl_elf_gabia.sh 는 본문 못 봄.
- **기계 검사만 한 것 216/216**: `python3 -m py_compile` (파이썬 전부) · `bash -n` (셸 전부) → **문법 오류 0**. 이건 "안 깨졌다" 가 아니라 "파싱은 된다" 는 뜻이다.
- **실행 안 한 것**: GPU 계산은 하나도 안 던졌다. `--selftest` 는 convention_check 스윕(83개)에 위임했고 개별로 다시 안 돌렸다. collect_neb 만 임시 cwd 샌드박스에서 실제 실행했다.

## 이 영역이 활성인가 — 어떻게 판단했나

**활성이다.** "끝난 캠페인" 이라고 접은 것은 하나도 없다.

- **커밋일**: 내 영역 상위 참조 파일들의 마지막 커밋이 sdcp/vasp_cost_estimate 2026-09-08, sdcp/scfin_to_struct 09-07, sdcp/run_orca_stage_a 09-06, sei/watch_qe_relax 09-06, ionic/watch_kgy 09-04, sei/collect_neb 09-03, sei/run_sei_dft 09-02, sei/watch_gabia·run_sei_neb·build_neb_inputs 09-01. 즉 **어제·그제까지 손댄 코드**다. 반대로 modelc_v3 9개는 전부 2026-06-11/29 라 후순위로 뒀다(= 안 봤다고 위에 적었다).
- **호출자**: 파일명 기준으로 repo 전체를 한 번 스캔해 참조표를 만들었다(scratchpad/refs.json). sei/build_neb_inputs.py 는 코드 참조 15곳, collect_neb.py 9곳, ionic/watch_all.py 8곳, sei/run_sei_dft.sh 8곳 — 고아가 아니다. 반대로 tools/litdb/pdf_text.py 는 tools/ 안에 호출자가 **0** 이라(사람이 직접 부름) 그 selftest FAIL 을 [참고] 로 내렸다.
- **열려 있는 작업**: 작업 #8 "kgy 에서 collect_neb --merge 실행" 이 바로 위 [치명] 의 수동 우회다. 즉 이 파이프라인은 지금 사람 손으로 굴러가고 있다.
- **판정 근거가 실물인 것**: collect_neb 의 두 실패 경로는 논증이 아니라 임시 샌드박스에서 재현한 출력이다. run_sei_neb.sh 의 LOCK trap 은 세 줄(167·174·222)을 읽고 판단했고 재현은 안 했다 — 그래서 [치명]이 아니라 [주의]로 뒀다.
