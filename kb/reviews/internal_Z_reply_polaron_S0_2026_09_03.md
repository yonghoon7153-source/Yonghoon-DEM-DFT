---
title: 회신 Z — 폴라론 S0 내부 적대적 리뷰 (NO-GO · P0 4 · P1 12)
date: 2026-09-03
updated: 2026-09-03
tags: [review, internal, sdcp, polaron, orca, reply]
status: 회신반영
kind: review-reply
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-03
verifiedBy: "내부 리뷰 원문 (scratch mutation 12건 · P0 4건 이행 커밋 52b0edcd)"
campaign: sdcp_polaron_S0
reviewer: 내부 (별도 컨텍스트 서브에이전트 · 파일 무수정 · scratch 사본 mutation)
target: 커밋 57c5909e (회신 Y 이행) + 2336a770 (사전등록 재발행)
verdict: NO-GO — 재비준 금지(현 판) · 실행 허용 범위 없음
---

> ⚠ **첫 내부 리뷰다.** 회신 Y 가 마지막 외부(codex) 교차리뷰였고(1저자 결정 2026-09-03), 이후는
> 별도 컨텍스트의 적대적 리뷰 + 1저자 비준으로 간다. 형식은 codex 회신과 같다(GO/NO-GO · P0/P1 ·
> 확인한 것). 아래는 원문 그대로다.

---

NO-GO — 재비준 금지(현 판) · 실행 허용 범위 없음. 지금은 loccheck 도 못 연다(아래 설명). P0 1–4 이행·재봉인·재비준 뒤에도 **loccheck 단독**만 GO. L·L2·seeds·probe·S·analyze·restart 금지.

제시된 봉인은 전부 실물과 일치한다(builder e9ea6e4b… · calib e92299fa… · last-change 57c5909e…). calib selftest 29/29, 빌더 selftest 302/0, Y mutation 30건은 실제로 가드를 물고 있다(scratch 사본에서 가드 12개를 지웠더니 전부 ✗로 뒤집혔다 — 아래 확인 절). 그런데도 NO-GO 인 이유는, 이번에 **새로 들어온 증거 유형(cube → calibration)** 이 실물 단위·결박·소비 세 층에서 전부 구멍이고, 판정기의 최종 판정 경로에 block 을 우회하는 shortcut 이 있기 때문이다.

## P0

1. **calibration 도구의 단위 오류 — NORM_OFF 가 모든 실물 cube 에서 발동한다 → 전 잡 CALIB_QC_FAILED → class 0개.**
   `spin_partition_calib.py:118-123` 은 dV 를 bohr³→Å³ 로 바꾸는데(`dv = |det|·BOHR_A³`), Gaussian cube 값은 e/bohr³ 다. `:289/:325` 에서 `tot_signed = Σv · dV[Å³]` 이므로 ∫Δρ 가 0.529³ = 0.148 배로 나오고 `:339` 의 `|tot_signed − n_unpaired| > 0.05` 가 항상 참이다. `pil_run_calib` 는 `n_unpaired = mult−1` 을 넘기므로(`build_v7c_trimer.py:6987`) production 에서는 예외 없이 걸린다.
   재현(정규화된 1e 가우시안을 bohr 단위 cube 로 써서 넣음): 직접 Riemann 합 1.0000 e → 도구 `int_signed_e = 0.1482`, `qc.flags = ['NORM_OFF(∫Δρ = 0.1482 ≠ 1 …)']`. `abs_total_*_eA3` 라는 이름도 단위가 틀렸다(값×Å³).
   selftest 29건이 못 잡은 이유: 픽스처가 **무차원 값 × Å 좌표**로 만든 cube 라 도구의 잘못된 규약과 자기일관적이다. NORM_OFF 시험(1.435 vs 1)은 "정상 cube 가 1 을 준다"를 한 번도 확인하지 않는다. 빌더 selftest 의 `_pil_fake_calib`(`:6516-6549`) 는 가짜 cube 텍스트 + `qc.ok=True` 를 손으로 써 넣으므로 이 경로를 아예 지나지 않는다.
   결과: 비 문턱을 직접 대조로 바꾼 P0-1/P0-2 이행은 **실물에서 한 번도 열리지 않는 게이트**다(fail-closed 이긴 하나 15잡 200원자 r2SCAN-3c 를 다 태운 뒤 전건 class 없음). 해제 조건: 단위 수정 + **실물 ORCA cube 로 양성 시험**(loccheck 에 open-shell 소분자 `%plots SpinDens` 를 붙이고 그 cube 로 `spin_partition_calib` 를 끝까지 돌려 ∫Δρ = 홀전자수 ±0.05 · qc.ok 를 증서에 봉인). `%plots` 블록 자체도 실물 ORCA 를 지난 적이 없다.

2. **cube 가 "그 잡의 것"이라는 결박이 없다.** 사전등록·주석은 "판정 재료를 읽은 그 잡의 cube"(`:7452-7460`)라고 하지만:
   · `pil_write_receipt`(`:4979-5014`) 는 `.inp/.xyz/%moinp/.out/ORCA` 만 해시하고 `<tag>_spin.cube` 는 안 한다. receipt 는 ORCA 종료 직후(러너 `:8237`), calib 는 그 뒤(`:8240`)에 만들어지므로 receipt 에 cube SHA 를 넣는 것은 한 줄인데 빠져 있다.
   · `pil_calib_gate_for_job:7042-7044` 의 CALIB_CUBE_CHANGED 는 **cube ↔ calib.json 자기일관성**만 본다. 다른 잡(또는 다른 conformer·옛 실행)의 199원자 cube 를 넣고 `--polaron_calib` 를 다시 돌리면 그대로 통과한다. `pil_run_calib:6982-6985` 는 원자 **수**만 대조한다 — 같은 종의 S 잡은 기하가 전부 같으므로 좌표 대조로도 잡 구분은 안 되고, 결박은 receipt 해시로만 가능하다.
   · 데이터 층의 보조 검증도 없다: `pil_calib_gate_for_job(man, jd, tag, sets)` 시그니처(`:7011`)에 그 잡의 Hirshfeld F 가 들어오지 않아, cube 의 Becke `F_out` 과 production Hirshfeld `F_out` 이 아무리 달라도 게이트가 열린다. 두 값이 크게 갈리면 "절댓값 위치가 class 를 바꾸지 않는다" 는 보증 자체가 무의미하다(분할 계열 차이가 지배). 허용치를 미리 박고 대조해야 한다.
   ⇒ 회신 Y P0-5 의 기준("receipt 가 실제 소비 입력에 결박")을 새 증거 유형이 그대로 위반한다.

3. **봉인됐지만 아무도 읽지 않는 결박 3건 — 비준 뒤 calibration 도구를 고쳐도 어떤 게이트도 안 걸린다.**
   ⓐ 사전등록 `0_시각_증거.calib_tool_sha256` 을 `_pil_check_prereg`(`:5100-5297`) 가 읽지 않는다(`_REQ_EV`/`_REQ_MAN` 에 없음). 생성기는 **디스크의 현재 도구**를 manifest 에 봉인하고(`:4689`), 판정기는 manifest 와만 대조한다(`:7035`). 재현: 실물 사전등록을 ratified 로 재digest 한 픽스처에 대해 `man["calib_tool_sha256"]="000…"`, `man["calib_gate"]={"max_dF":0.99}` 로 `_pil_check_prereg` 호출 → **통과**. 즉 `direct_comparison_gate` 가 사는 파일은 빌더 SHA 밖이고 사전등록 결박 밖이다 — 회신 Y P0-2 가 요구한 "calibration 도구 SHA 결박" 이 문서에만 있다.
   ⓑ `man["calib_gate"]`(문턱) 는 `:4690` 에서 쓰고 어디서도 읽지 않는다(grep 0건). `pil_run_calib`/`pil_calib_gate_for_job` 은 모듈 상수를 쓴다.
   ⓒ 빌더 SHA 를 manifest 와 대조하는 곳은 **bash 러너**(`:7806-7818`) 뿐이다. `pilot_analyze`·`pilot_seeds`·`pilot_restart`·`pil_run_calib` 는 자기 파일 SHA 를 manifest 와 비교하지 않고(`_sha(__file__)` 사용처는 생성기 `:4565` 와 selftest 만), `_pil_check_prereg` 는 사전등록↔manifest 만 비교한다. 따라서 `python3 build_v7c_trimer.py --polaron_analyze D` 를 상수만 바꾼 빌더로 직접 부르면 사전등록·manifest 검사가 다 통과하고, `PILOT_RESULT.json`(`:7077-7083`) 에는 어느 빌더가 판정했는지 기록조차 남지 않는다. "문턱은 코드 상수라 바꾸면 커밋에 남는다" 는 문장이 판정 산출물 쪽에서는 성립하지 않는다.

4. **판정 shortcut 이 block 을 우회한다 — PROBE_CERT_MISSING·LOCCHECK_CERT_INVALID 가 있어도 dependency 판정어 + rc 0.**
   `pilot_analyze:7629-7643`: `_codes` 는 **잡 gate 만** 모은다. `if res["blocks"]:` 안에서 `_dep_hit and set(_codes) <= set(_DEP)` 이면 `res["verdict"] = _dep_hit[0]` 로 닫는다. probe 증서 결측(`:7127-7128`)·loccheck 증서 무효(`:7119-7120`)·SEED_RECEIPT_MISSING(`:7604`) 은 잡 gate 를 만들지 않으므로, 잡들이 전부 THRESHOLD_DEPENDENT 같은 dependency gate 만 가지면 block 은 무시된다. `main:8441` 은 NO_VALUE 가 아니면 rc 0.
   재현(scratch 사본, 판정기 코드는 그대로): `pilot_threshold_sensitivity` 가 threshold_dependent=True 를 돌려주게 한 뒤 `_ana("…", _no_probe_cert=True)` → `verdict=THRESHOLD_DEPENDENT`, `blocks=['PROBE_CERT_MISSING(…)', 'GATED_JOBS(7건 …)']`, `gate_codes=['THRESHOLD_DEPENDENT']`. Y P0-4/P0-7 mutation 시험은 픽스처에 dependency gate 가 없어서만 통과한다.
   같은 자리에 이중 fail-open 이 하나 더 있다: 증서가 무효면 `_cert_orca=None` 이고 `_receipt_gates:7180` 의 `if _cert_orca:` 가 **receipt ORCA 대조 자체를 끈다** — 증서를 지우면 ORCA identity 게이트가 사라지고 남는 것은 위 shortcut 으로 우회 가능한 block 하나다. 고치는 법: dependency 닫힘은 `blocks` 가 GATED_JOBS **만**일 때로 제한하고, `_cert_orca is None` 은 잡마다 RUN_RECEIPT_ORCA_UNVERIFIABLE gate 로 내린다.

## P1

- **L/L2 receipt 의 ORCA 는 아무도 대조하지 않는다.** `pilot_seeds:5848-5910` 은 out/xyz/moinp 만 보고, 판정기는 S·SR·S0P receipt 만 게이트한다. L/L2 를 ORCA A 로 돌린 뒤 loccheck 를 B 로 재발행하면(`_loccheck` 는 매번 rm -rf) 이후 단계는 전부 B 로 통과한다 — "모든 단계가 증서의 ORCA" 가 사슬의 원천에서 깨진다. 증서 재발행 시 기존 receipt 와의 불일치를 막거나, seeds/analyze 가 L/L2 receipt 의 `orca_sha256` 도 대조해야 한다.
- **probe 증서 판독이 파일을 신뢰한다**(`pil_read_probe_cert:6846-6874`). digest·builder·n_intervened 만 보고 판정을 재계산하지 않는다. 같은 사용자 위조는 위협모델 밖이라 해도, 증서 없이도 재계산은 공짜다(probe 출력 판독) — `--polaron_require_probe_pass` 가 `pilot_probe_verdict` 를 다시 돌려 blocks==[] 를 요구하는 것이 더 강하고 단순하다. 증서 안의 `prereg_sha256`·`orca_sha256`·`stop_rule`·`controls` 는 기록만 되고 검증되지 않는다.
- **P0-8 원자성은 검증 단계 거부에만 성립한다.** apply 루프(`:8163-8171`)에서 두 번째 `os.replace` 가 I/O 로 실패하면 첫 파일은 바뀌고 manifest(`:8189` 비원자적 `json.dump`)는 옛 값이다 — preflight 의 INP_CHANGED 로 fail-closed 되지만 사전등록 문구 "하나라도 거부면 아무 파일도 바뀌지 않는다" 는 과장이다. manifest 도 임시 파일→replace 로.
- **strict 분할은 estimand 형태 대조에서 빠져 있다.** class 는 extended·strict 둘의 일치를 요구하는데(`:7440-7446`) 대조는 extended 집합만(`:7458`). `partition_forms` 가 원자별 `s_A`/`∫w_A|Δρ|` 를 산출물에 안 넣어(`spin_partition_calib.py:345-370`) 판정기가 다른 분할·링 몫을 재계산할 수도 없다. 원자별 벡터를 JSON 에 넣으면 strict/ring 대조가 공짜다.
- **격자 QC 상수가 실물 cube 를 한 번도 못 봤다.** 경계 1e-3(`spc:336`)·간격 0.35 Å·`%plots` 에 min/max 없음(`:4450-4453`, ORCA 기본 상자 여백에 의존). 분자 축 방향 폭 18.8×23.8×14.6 Å 이라 dim 120 은 여백 ≤4 Å 가정에서 0.26–0.28 Å 로 통과하겠지만, 면 절단 1e-3 은 여백에 따라 전건 CALIB_QC_FAILED 가 될 수 있다. 상자를 명시하고(P0-1 의 smoke test 로 실측) 결과 보기 전에 재봉인.
- **실행 시간.** `_becke_weights_np` 를 199원자·96점 chunk 로 실측: 0.083 s/chunk → 120³ = 18,000 chunk → **cube 하나 24.8 분**(이 기계 1 thread). S 15잡 ≈ 6 h 가 S 단계 안에서 ORCA 와 직렬로 들어간다(+SR). 메모리는 chunk 당 30 MB 임시배열 수 개로 문제없다. 현실적이지만 사전등록에 시간 예산으로 적을 것; float32·원자 cutoff 로 5–10배 줄일 수 있다.
- `read_cube:106` 은 `ln` 이 정의되기 전에 쓰여 SystemExit 대신 NameError 로 죽는다(fail-closed 이나 오류 유형 오류).
- 게이트된 잡의 `r["class"]`(`:7413`) 가 산출물에 그대로 남는다. 사전등록은 "class 없음, 값은 남긴다" 인데 JSON 을 읽는 사람은 class 를 인용할 수 있다 — 게이트 시 `class_candidate` 로 옮기거나 null.
- calib receipt 행(`:7002-7007`) 은 쓰이기만 하고 읽는 곳이 없다(사전등록 "calibration 마다 RUN_RECEIPTS 에 행을 남긴다" — 기록만). `stop_rule` 은 계산·출력(`:8389-8391`)만 하고 러너 probe 루프(`:8217-8218`)는 전부 돌린 뒤 판정하므로 "남은 진단 probe 도 중단" 은 기계적으로 집행되지 않는다(사람 규칙으로 명시할 것).
- 사전등록 `결박` 절의 "판정기가 전부 재대조한다" — F 값은 calib.json 을 **신뢰**하고 재계산하지 않는다(cube·분할·도구 SHA 만 대조). 사실대로 적을 것.
- 회신 Y Q1(plan-only → PLAN.json → 봉인 → 비준) 은 이행되지 않았다. 생성기는 여전히 비준된 사전등록을 요구하고 규모는 생성 뒤 채워진다.
- 회신 Y P1 중 이행 확인: NO_ROTATION_NEEDED 통과 규칙 통일(`:7482-7483`), census=scale_actual(`:4677-4680`), UTF-8 콘솔(두 파일 머리), 균등 대체 질량 기록(`spc:342-344`).

## 확인한 것

- 봉인 대조: `sha256sum` builder e9ea6e4b…, calib e92299fa… = 사전등록 값; `git log -1 -- tools/sdcp/build_v7c_trimer.py` = 57c5909e… = `builder_last_change_commit`; HEAD 2336a770, working tree clean; 사전등록 파일 SHA 061214d8….
- 사전등록 게이트: `status: proposed`, `ratification.state: ratified`(옛 것), `content_digest` 기록 7f7e00fa… vs 재계산 c57665d5… → 불일치. 합성 manifest 로 `_pil_check_prereg` 호출 → "status 가 'proposed'" + "비준 이후에 바뀌었다(지문 불일치)" 로 SystemExit. `pilot_generate` 가 이 검사를 무조건 부르고(`:4694`) 러너는 loccheck 단계에서도 MANIFEST_PILOT.json 의 builder_sha256 을 요구하므로(`:7806-7818`), **지금은 생성도 loccheck 도 열리지 않는다.** 옛 묶음+옛 빌더로 loccheck 를 돌리는 것은 범위 밖(금지).
- selftest: `spin_partition_calib.py --selftest` 29 통과/0 실패(음성 18). 빌더 `--selftest` 302 ✓ / 0 ✗ (`grep -c "✓"` 302, "✗" 0), Y 표지 30건.
- Mutation(repo 파일 무수정 — scratch 사본 2개, 각각 git init 후 실행): 가드 12개 제거 → ✗ 13건. 1차(6개): P0-3 `not pre_seed` 제거→Y P0-3 ✗; 분석기 probe 증서 요구 제거→Y P0-4 ✗; calib gate 소비 제거→Y P0-1·P0-2 4건 ✗; xyz 해시 요구 제거→KeyError 로 중단(검출은 됨). 2차(6개): CONTROL_RECEIPT_UNVERIFIED 제거→Y P0-6 ✗; receipt ORCA 대조 제거→Y P0-7 ✗; preflight ORCA 대조 제거→X P0-9·Y P0-7 ✗; L out 결박 제거→Y P0-5 ✗; xyz 해시 fail-open 복원→Y P0-5 ✗; PYL2 를 검증 중 즉시 쓰기로 되돌림→Y P0-8 ✗. 즉 Y 시험은 가드를 실제로 물고 있다 — P0-4 의 구멍은 가드가 아니라 **판정 shortcut** 에 있다.
- P0-4 재현: scratch 사본에서 `pilot_threshold_sensitivity` 만 threshold_dependent=True 로 바꾸고 `_no_probe_cert=True` 픽스처 분석 → verdict THRESHOLD_DEPENDENT, blocks 에 PROBE_CERT_MISSING 잔존(위 본문). 같은 픽스처의 정상 실행은 ADEQUATE.
- P0-1 재현: bohr 격자·e/bohr³ 값의 1e 가우시안 cube → `int_signed_e 0.1482`, NORM_OFF(위 본문).
- P0-3 재현: ratified 로 재digest 한 사전등록 사본 + `calib_tool_sha256="000…"`·`calib_gate.max_dF=0.99` manifest → `_pil_check_prereg` 통과.
- `direct_comparison_gate` 산수: 리뷰어 반례 F_in 0.49/0.31/0.20, F_out 0.544/0.289/0.167 → ⓑ 에서 CALIB_CLASS_BOUNDARY_DIFFERS(ⓓ도 0.054 > 0.05). ⓐ–ⓓ 정의는 회신 Y Q3 와 일치. Becke a_ij·ν_ij·s_k 식 확인. "둘 다 틀린 경우"(격자·Becke≠Hirshfeld)는 문서가 정직하게 적었으나, Becke F_out↔Hirshfeld F_out 대조가 빠진 것은 P0-2 로 올렸다.
- `%plots` 블록은 ORCA 매뉴얼 형식(`Format Gaussian_Cube` · `dim1/2/3` · `SpinDens("f");`)과 일치 — 단 실물 실행 0회, 상자 미지정.
- P0-3 도달 경로: `pre_seed=True` 는 `pilot_generate:4694`, `pilot_seeds` 첫 줄 `:5809`, `pil_preflight` L/L2 `:4938` 만; `pilot_seeds` 끝 `:6236` 에서 pre_seed=False 재검사. `PIL_PREREG_S0 =` 대입은 상수 `:4716` 과 selftest 안에만 있고 main 에는 없다. `_repo_path` 의 절대경로 허용은 `rel != PIL_PREREG_S0` 검사(`:5114`)로 production 에서 막힌다.
- P0-4 러너 순서: `--polaron_require_probe_pass`(`:8232`) → `preflight S`(`:8233`). P0-7: `export PIL_RUNNER_ORCA`(`:7801`) 가 모든 단계 앞; `pil_read_loccheck:5086-5096` 이 실행 ORCA 와 증서를 대조; `pil_preflight` 가 stage 무관하게 부른다.
- P0-5: 남은 glob 은 decoy 검출(`:4853`)과 디렉터리 집합 대조(`:4894-4907`)뿐. L2·S0P·SR 행 `xyz_sha256` 있음(`:4644`,`:6112`,`:6150`,`:6707`). `pilot_seeds` 가 L receipt out/xyz 와 manifest xyz 를 지금 파일과 3자 대조(`:5873-5892`).
- P0-6: control 은 `_receipt_gates` 통과 시에만 baseline(`:7208-7211`); 실패 시 block + baseline 부재 → 잡별 SEED_INTERVENTION_UNVERIFIED 로도 막힘(간접 이중).
- P0-8: 전건 선검증 → plan → 임시 파일 `os.replace` → transition 은 전부 교체 뒤 기록(`:8177-8181`). 검증 거부 시 파일 변경 0 은 시험이 증명(Y P0-8); apply 중 I/O 실패는 P1.
- 규모·분자: 부모 xyz 200원자, 축 방향 폭 18.8×23.8×14.6 Å.
