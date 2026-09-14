# 검증 — 렌즈 "파생-보고서 + 공정성-의미" (대상 1049894, 독립 worktree, 읽기 전용)

스크립트: `check_df01.py` · `check_df03.py` · `check_df06_df09.py` (모두 `<wt>/bms-balancing/` 에서 실행). 렌즈 스크립트는 아이디어만 읽고 재실행하지 않았다.

| ID | 판정 | 심각도 | 한 줄 이유 | 원장 겹침 |
|---|---|---|---|---|
| DF-01 | CONFIRMED | 서술만_바뀜 (상) | 힌트 격자의 grid[5]/grid[15] 가 제약 최적화 min/max 와 비트 단위 동일 → LLI "정확히 일치·독립 수렴" 은 같은 격자점 반환. §3-3/§3-4 가 힌트 자체는 공개하나 "끝점이 격자점" 은 미공개. 폭 1.0832·`is_lower_bound` 불변 | 없음 (R2 C5 는 채택 정책만) — 신규 |
| DF-02 | CONFIRMED | 결론이_바뀜 (INTRO §6-2) / 서술만 (HANDOFF §5) | 취소선 없는 철회 문장 7 곳, §0-2 행 6·7·8·9 와 정면 모순; 두 파일 머리에 "동결/옛 판" 배너 없음 (INTRO 배너는 "숫자는 사본" 뿐) | R2 C13(INTRO §6-1만)·C14(HANDOFF §4만) 부분 겹침 — §5·§6-2 는 신규 |
| DF-03 | 부분 | 서술만_바뀜 | raw 배율 max/max 10.52 · min/min 9.66 · med/med 10.04 — 문서가 이름붙인 통계(max/max)로는 "5~10" 이 안 나온다. 단 min(cyl)/max(pouch)=4.80 → max/max 10.52, fixedhc 분모 상태별 쌍 4.8~13.2 라는 **보수적 통계로는 5~10 이 나온다** → 숫자 오류가 아니라 통계량 미표기 | R3-04 (분모·집합) 인접; 신규 |
| DF-04 | CONFIRMED | 숫자가_바뀜 | `--collect-only` 87 tests; "86 passed" 잔존 WORKING_STATE:42 · R6_REQUEST:23,40 (R5_LEDGER:35 는 R5 당시 기록이라 정상) | Codex R5 §1 (74 vs 75) 동종 |
| DF-05 | CONFIRMED | 서술만_바뀜 | `cmd_eval` 은 `obj.rmse_*` raw 출력, `rmse_pocv` 정의에 scale 없음, scale 은 `__call__` 에서만 소비; 300 build pocv scale=eps/eps_rel=0.135 V vs 인쇄 rmse_pocv 0.0468/0.0076 V(raw). §1-13 문장 "192 값의 build 는 그 조건 안" 은 문자 그대로 참이나 "96/192 빈틈 메워짐" 은 192 값에 존재한 적 없는 빈틈 | R5-06·R5-09 (범위 정정) 인접; "192 값이 scale-free" 는 신규 |
| DF-06 | CONFIRMED | 서술만_바뀜 | 6/17/9 · "전부 w=1" 은 상대 허용 1e-9(또는 1e-8) 에서만; 부호만 보면 10/22/0 이고 w=0 도 악화(<1e-9, optimizer 잡음). §4-0 에 문턱 표기 없음. 최대 악화 1.6e-4(GITT·Baggetto·w1) 재현 | 없음 — 신규 |
| DF-07 | CONFIRMED | 서술만_바뀜 | §1-10 (511~602) 안에 "하한/탐색" 은 :597 (§1-12 인용) 뿐; 표 머리 "근최적 집합 폭" · "전부 양수 구간" · "이것이 답이다" 에 한정어 없음 | R2 원장 :47 이 §1-10 을 "탐색 하한 기술로서" 라 부름 — 원장은 알고 본문만 빠짐 |
| DF-08 | CONFIRMED | 사소 | 기준 자유 3 종(Jiang 5.7940·Kunz 6.3619·Li 7.8957) 폭 2.1016; 2.11 은 2dp 반올림 후 뺄셈 | 없음 |
| DF-09 | 부분 | 사소 | v1 행은 §3-3 인쇄 정밀도(4dp) 에서 일치(6.3562/7.8957/15.7001), 비트 일치는 v2 만(Δ0) — "일치" 가 거짓은 아니고 인용 파일이 옛 산출 | §4-0 (v1=옛 multistart) 인접 |
| DF-10 | CONFIRMED | 사소 | INTRO:432 "n=1 … 산수다" 취소선 없음 vs INTRO:441 "반복 측정 없이도 잴 수 있다" · §7-3 "그건 틀렸다"; §6-3 제목 "산수라서 진짜 못 한다" 도 잔존. 절의 결론(오차막대 아님) 은 유지 | 없음 |

## 발견별 근거

### DF-01 — `check_df01.py` (v2 JSON 만으로 격자 재구성)
```
LAM_PE: stored grid range matches unclamped hint±pad: True; n_grid=22(json 22)
   ext.min -> grid idx 5 (delta 0.0e+00), ext.max -> grid idx 16 (delta 0.0e+00)   # idx 16 = best 삽입 때문
   prof.min = grid[6] (delta 0.0e+00), prof.max = grid[16]; prof.min==ext.min False, prof.max==ext.max True
   grid points inside [prof.min,prof.max] incl. best = 11 vs n_grid_attainable 11 -> contiguous=True; grid step = 0.2870 %p
LAM_NE: ... prof.min = grid[3] ... prof.max==ext.max True ... 14 vs 14 contiguous=True; step 0.3002 %p
LLI:    ext.min -> grid idx 5 (delta 0.0e+00), ext.max -> grid idx 16 (delta 0.0e+00)
   prof.min = grid[5], prof.max = grid[16]; prof.min==ext.min True, prof.max==ext.max True
   grid points inside ... = 12 vs n_grid_attainable 12 -> contiguous=True; grid step = 0.1083 %p
is_lower_bound: {'LAM_PE': True, 'LAM_NE': True, 'LLI': True} LLI span 1.0832389268006661
```
코드 근거 `verify.py:348-358`: `pad=(h_hi−h_lo)/2; linspace(h_lo−pad, h_hi+pad, 21)` → 간격 = span/10, 끝점이 index 5·15 에 정확히 놓인다. `:464` 가 `hint={min,max}` 로 (a) 의 답을 넘긴다. 프로파일 극값은 도달 격자점의 min/max (`:388-389`) 라 격자 값 밖으로 못 나간다.
(a) 격자가 method-1 min/max 를 **정확한 격자점으로 포함** — 확인 (delta 0, 세 mode). LLI 도달집합은 grid[5..15]+best 로 연속, 즉 프로파일이 보탠 정보는 "끝점 둘 도달·한 칸(0.108 %p) 밖 미도달".
(b) 공개 여부 — §3-3:1086 "(프로파일 격자 힌트 적용본)", §3-4:1116-1117 "제약 최적화가 이미 찾은 범위를 힌트로 받아 그 둘레(폭의 ±50 %)에 격자를 모으도록 고치고 다시 돌린 결과". 힌트는 공개됐고, 21점·끝점=격자점 은 미공개. 그런데도 :1111 제목 "두 독립 방법이 수렴했다 — 이 숫자를 믿을 근거", :1126 "같은 값에 수렴", :1128 "1.0832 라는 값이 두 경로에서 독립적으로 나온다는 뜻이다" → 값의 자릿수는 (a) 에서 물려받은 것이므로 이 세 문장은 성립하지 않는다. 지시대로 "공개 있음 + 독립 주장" 이라 결론이_바뀜 대신 서술만_바뀜(상) — 단 ★ 절의 증거 문장이라 서술 수정 중 1순위.
(c) `is_lower_bound: True` 세 mode 모두 잔존, LLI 폭 1.0832389 불변. LAM_PE 표의 "프로파일이 자릿수까지 따라옴" 은 (a) 의 min(grid[5]) 을 프로파일이 못 간 자리(grid[6]) 를 가린다 — 갈린 곳을 수렴처럼 읽은 것(렌즈 지적 타당).
부수 관찰(미채점): v2 JSON `from_mode_profile` 에 현재 코드가 쓰는 `attainable_pct`·`grid_pct`(R2-05) 키가 없다 — 산출이 R2-05 이전 코드 판. R2-05 의 "공유 가능값" 질문은 저장된 산출로 못 답한다.

### DF-02 — `sed -n 1,14p HANDOFF_TO_GATE.md; sed -n 205,242p …; sed -n 1,12p INTRO.md; sed -n 396,436p INTRO.md`
- HANDOFF 머리: 날짜·경계 설명만, 동결 배너 없음. §4(:213-218) 는 정정판("'대체 배제' 도 '셀 차이' 도 아니고"). §5(:231-234) 는 `~~셀 일반화~~ → 끝났다` 항목 뒤에 취소선 **없이** "대조 실험으로 반쪽전지 대체를 배제했다 … 원통형은 LAM_PE 로 가르고 LAM_NE·LLI 는 겹친다. 정확히 반대다".
- INTRO 머리 배너: "정본은 FINDINGS.md … 여기 적힌 숫자는 사본" — 옛 판 선언 아님. §6-2(:405-420) 취소선 없이: "**우리 대체 탓이 아니다.**" · "**순위가 통째로 뒤집힌다.**" · "LAM_PE 의 식별 가능성은 두 셀에서 **똑같다**" · "대조가 배제한 것은 **반쪽전지 대체 하나**다".
- §0-2 행 6 "우리 대체는 원인이 아니다 → **철회 (R2)**", 행 7 "LAM_PE 식별 가능성 똑같다 → 철회 (R2)", 행 9 "못 가른다 → 정정 (R2)". R2 원장 C13 "INTRO §6-1 재작성", C14 "HANDOFF §4 문단을 §1-12 정정판 요지로" — §5·§6-2 는 손대지 않았다.
- 강등 사유 없음(배너 없음). INTRO 는 신규 독자용 서사라 결론이_바뀜; HANDOFF §5 는 §4 바로 아래 to-do 잔재라 서술만.

### DF-03 — `check_df03.py` (`out/degeneracy_{100,200}_Li.json`, `_300_0009_Li_v2.json`, `out/cells_{c168,c171,pouch_fixedhc}/degeneracy_*_Li.json`, 반폭 = span/2)
```
pouch(6) [0.2868,0.5770]  cyl(6) [2.7721,6.0712]
max/max 10.52  min/min 9.66  med/med 10.04  min(cyl)/max(pouch) 4.80  max(cyl)/min(pouch) 21.17
same-state pairs vs pouch: 5.1~18.3; vs fixedhc: 4.8~13.2 ; all 36 cross ratios: 4.8~21.2
```
"5~10" 출처: FINDINGS:34(§0-1)·:1494(§7), HANDOFF:215, WORKING_STATE:106, R3_REQUEST:65 "raw 로 5~10 배(하한끼리, max/max; …)", R4_REQUEST:68, R5_REQUEST:70 "raw 5~10x, … pristine rmse 4.99x". §1-12 :744 "10.5x", :762 "10.52x/9.66x/10.04x", INTRO:415 "10.5 배".
반박: min(cyl)/max(pouch) 4.80 ~ max/max 10.52 는 정합적인(가장 보수적인) 통계이고 4.8~10.5 ≈ "5~10" — 렌즈의 "어느 통계로도 안 나온다" 는 과장. 남는 문제: 문서가 그 통계를 어디에도 안 적고 R3 요청문은 "max/max" 라 붙였다(그 통계는 10.5 하나). → 부분, 서술만.

### DF-04
```
$ grep -rn "86 passed\|87 passed" --include=*.md .
./WORKING_STATE.md:42:python3 -m pytest tests/ -q   # 86 passed 기대
./reviews/R5_LEDGER.md:35:| … | 86 passed (R5 신규 11 …) |      ← R5 시점 기록, 정상
./reviews/R6_REQUEST.md:23: … # 원자료 불필요. 86 passed 기대 …
./reviews/R6_REQUEST.md:40:| `pytest tests/ -q` | 86 passed (R5 신규 11) |
$ python3 -m pytest tests/ --collect-only -q | tail -2   → 87 tests collected in 1.40s
```

### DF-05
- `model.py:346 def rmse_pocv(self, p)` / `:350 rmse_dvdq` / `:363 rmse_dqdv` — `scales` 미참조; `:456-463 __call__` 만 `self.rmse_*(p) / self.scales[...]`. `verify.py cmd_eval` 상대 34-38행: `vals = {"rmse_pocv": [obj.rmse_pocv(q) …], …}` 를 그대로 인쇄. `_auto_scales :447 eps_rel = eps / raw`, scale = raw+eps.
- `out/scale_audit_eval_u13.txt:10` `state=300_0009 … pocv: … eps_rel=1.64e-15` → scale ≈ 2.22e-16/1.64e-15 = 0.135 V; `out/recompare/dd_eval_300_Li_r2.csv` rmse_pocv = 0.046792 / 0.047014 / 0.007567 (V, raw — scale 로 나눴다면 0.35/0.35/0.056).
- 문서 인용: §0-1:28 "동치는 표본이 전부 유한하고 eps 상대 영향 ≤ 1e-9 일 때의 상대 근사 — U13 실측 18 build, recompare 4 조합 포함, 전부 그 조건 안"; §1-13:971-973 "§1-8 의 recompare 4 조합 … 이 18 줄에 전부 들어 있으므로 192 값의 Python 쪽 build 는 그 조건 안이다 (Codex R5-09 가 지적한 96/192 빈틈은 이 실측으로 메워졌다)"; R6 §4:69 "U13 실측 18 build(recompare 4 조합 포함)". 
- 판정: "build 는 그 조건 안" 은 참(감사 줄이 그 build 의 것). 틀린 것은 함의 — 192 값은 scale 을 소비하지 않으므로 "빈틈" 은 192 값에 없었고, U13 의 Kunz·step_005C 2 줄은 어느 적합 산출도 안 쓰는 build 의 감사다. 서술만.

### DF-06 — `check_df06_df09.py` (`obj` 열, v1 32 행 ↔ v2 32 행, key=(half_cell,si,w_dqdv))
```
tol 0:     worse 10 better 22 same 0; worse all w=1? False (w values [0.0, 1.0])
tol 1e-10: worse 9  better 21 same 2; worse all w=1? False
tol 1e-09: worse 6  better 17 same 9; worse all w=1? True
tol 1e-08: worse 6  better 16 same 10; worse all w=1? True
max rel worsening (0.00016014, ('GITT','Baggetto',1.0))
```
§4-0:1166-1169 원문에 문턱·"같음 9" 없음 (`sed -n 1140,1172p | grep "1e-9|허용|tol|동률|같음"` → 없음). 6+17=23≠32 라 암묵적 동률 9 가 있다.

### DF-07 — `sed -n 512,545p FINDINGS.md`; §1-10 = :511~602
"#### A축 — 근최적 집합 폭 (모델 고정)" · :527 "순위가 완전히 일관된다 — 이것이 상태 일반화 질문의 답이다" · :533 "다른 세 상태는 전부 양수 구간이다". 절 안 '하한|탐색' 은 :597 (§1-12 인용문) 뿐. 네 JSON `is_lower_bound: true`(렌즈 C12 와 같음; 100 LAM_NE min −0.896). 한정어는 §0-1·R6 §4·R2 원장 :47 에만.

### DF-08 — `check_df06_df09.py` 보조 (`matrix_300_0009_v2.csv`, GITT·w0·`ref_bounds=='-'`)
`ref-free: [('Jiang', 5.794), ('Kunz', 6.3619), ('Li', 7.8957)]; LAM_NE spread (raw) 2.1016 ; from 2dp-rounded 2.11`. FINDINGS:1192 "**2.11 %p**", :557 표 2.102.

### DF-09
`v1 GITT/Li/w0: LAM_NE 7.895696 (Δ +1.2e-05), LAM_PE 6.356180 (Δ −3.9e-05), LLI 15.700072 (Δ −5.5e-05) ; v2: Δ 0.0 ×3` (Δ = 행 − `best_modes_percent`). §3-3:1094 는 4dp 로 6.3562/7.8957/15.7001 을 적었고 v1 도 그 자리까지 같다 → "일치" 는 거짓 아님; 정확 일치는 `_v2`.

### DF-10 — `sed -n 396,452p INTRO.md`
:432 "**n=1 에서는 분산을 추정할 수 없다.** 노력의 문제가 아니라 산수다." (취소선 없음) ↔ :441 "σ 는 반복 측정 없이도 한 곡선의 고차 차분으로 잴 수 있다 (§7-3 …)" ↔ FINDINGS §7-3:1455-1457 "전 판은 '반복측정이 없으면 못 한다' 고 적었는데 **그건 틀렸다**". §6-3 제목 "산수라서 진짜 못 한다" 도 잔존.

## 공정성 "통과" 주장 점검
- 1e-9 근거: `grep -rn 1e-9 *.md reviews/*.md` 에서 정의 근거는 FINDINGS:416-417 비교기 문턱 표("> 1e-9 → 모델·산술의 차이, 앵커와 같은 문턱") 와 `model.py:283` 주석 "비교기의 MODEL_REL(1e-9)과 같은 크기" 뿐 — 렌즈 진술 정확. 물리·통계적 근거는 문서에 없다(문서도 주장하지 않음).
- seed: `scale_seed` 는 `out/*.csv`·`out/*/*.csv`·모든 `.meta.json` 어디에도 없다(grep 공집합). "seed 집합 {0}" 은 `scale_audit_eval_u13.txt` 18 줄 `seed=0` 에서만 나온다 → "모든 matrix 행" 에 대해서는 검증 불가; 렌즈 C01 문구는 감사 파일로 한정해 적어야 한다(C12 INFO 는 이미 그렇게 적음).

## CONFIRMED — 수정 우선순위
1. DF-02 (결론이_바뀜): INTRO §6-2 :405-420 · HANDOFF §5 :231-234 를 §1-12 정정판 요지로 교체(또는 취소선+화살표); `test_docs_*` 에 금지 문구(`대체를 배제`, `정확히 반대`, `똑같다`, `우리 대체 탓이 아니다`) 추가.
2. DF-01 (서술만·상): §3-4 제목·:1126·:1128 을 "제약 최적화 끝점을 격자점으로 넣고 등식 프로파일로 재확인 — LLI 끝점 둘 도달·한 칸(0.108 %p) 밖 미도달; LAM_PE 는 프로파일이 min 을 못 감; 독립 수렴 아님" 으로. 산출에 `attainable_pct`/`grid_pct` 가 실리도록 v2 재생성(R2-05 코드 판) 하면 겸사겸사.
3. DF-04 (숫자): 세 줄 87.
4. DF-05 (서술만): §0-1·§1-13·R6 §4 에서 U13 대상을 "적합 산출의 목적함수 build" 로; "192 값 … 빈틈" 문장 제거.
5. DF-06 (서술만): §4-0 에 "상대 변화 1e-9 초과만 센다(동률 9; 부호만 보면 10/22)" 추가.
6. DF-07 (서술만): §1-10 표 머리·:527·:533 에 "탐색 하한" 한정어.
7. DF-08·DF-10 (사소): 2.10; INTRO:432 취소선+§7-3 참조.

## 반증됨 / 강등
- DF-03 → 부분·서술만: min(cyl)/max(pouch)=4.8 ~ max/max 10.5 라는 정합 통계가 "5~10" 을 낸다. 고칠 것은 통계량 이름(및 R3 요청문의 "max/max" 오귀속)이지 숫자가 아니다.
- DF-09 → 부분·사소: 인용 파일이 인쇄 정밀도에서는 일치. `_v2` 로만 바꾸면 끝.
- DF-01 → 결론이_바뀜에서 서술만(상) 으로 강등: 힌트 사용을 §3-3·§3-4 가 이미 밝힌다(끝점=격자점 은 안 밝힘).
