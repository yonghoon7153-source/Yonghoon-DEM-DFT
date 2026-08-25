---
title: Codex 적대 리뷰 결과 — EIS·DRT·GITT
created: 2026-08-25
updated: 2026-08-25
type: review
tags: [review, audit, crosscheck, eis, gitt]
sources: [docs/reviews/codex-review-eis-gitt.md]
confidence: high
explored: false
verificationStatus: verified
---

# Codex 적대 리뷰 결과 — EIS·DRT·GITT (승인 보류)

> Codex 가 작성한 독립 리뷰 원문이다. Codex 환경에서 커밋되지 못해 사용자가
> 채팅으로 전달했고, 여기 그대로 보존한다. 교차 대응 현황은
> `2026-08-25-eis-gitt-crosscheck.md` 에서 갱신한다.

- 과제: [codex-review-eis-gitt](codex-review-eis-gitt.md)
- 범위: `b6df17bb..7b0531d1` (73파일, +11,143줄)
- 결론: **승인 보류.** 33건 — 높음 19 · 중간 12 · 낮음 2
- 대응: **아직 안 함.** 이 문서는 독립 리뷰 원문이고, 소스는 고치지 않았다.

Claude 쪽 결과는 읽지 않은 채 이 범위의 최종 파일과 diff만 검토했다. 아래 "높음"은
모두 틀린 수치가 측정·피팅·분석 결과처럼 보이는 경로다. "중간"은 원본이나 기능을
잃는 경로, "낮음"은 화면의 모순이 사람을 잘못된 입력으로 유도하는 경로다.

## 검증 환경과 판정 기준

- `CLAUDE.md` §0, ADR 0018·0019·0020, BioLogic MPR 스펙을 코드보다 먼저 읽었다.
- Windows 가상환경에서 `packages/wrdkit/tests`와 `apps/api/tests` 전체를 실행했다:
  **804 passed, 24 skipped**. EIS 집중 시험은 **57 passed, 2 skipped**였다. skip에는
  `WRDKIT_EIS_SAMPLE`이 없어 건너뛴 실측 `.mpr` 시험 6개가 포함된다.
- Ruff, TypeScript `tsc --noEmit`, ESLint, wiki lint는 통과했다. 이 호스트에는
  `make`가 없어 `make check`라는 묶음 명령 자체는 실행하지 못했다. 웹 Vitest는
  Vite/esbuild가 샌드박스 밖 `C:\`를 훑다가 `Access is denied`로 시작하지 못했다.
- 저장소, `D:\bml-data`, 다른 worktree와 Downloads를 찾았지만 `.mpr`, `.mpt`,
  `.mps` 실측 파일은 없었다. 이진 리더 지적은 합성 바이너리와 손상 변형으로 재현했다.
- GITT 식은 원 논문과 현대 검토 문헌의 정의를 대조했다 (Schied et al., Park et al.,
  Weppner–Huggins 원식). DRT의 비음수 최소제곱 판정은 Hansen et al. 과
  SciPy `lsq_linear` 의 최적성 조건을 기준으로 삼았다.

## 확인된 결함

| # | 심각도 | 파일:줄 | 증상 (틀린 숫자/잃는 데이터/화면의 거짓) | 재현 | 제안 |
| ---: | :---: | --- | --- | --- | --- |
| 1 | 높음 | `packages/wrdkit/src/wrdkit/eis/fit.py:54-71,238-244,309-339` | 경계에 붙은 미결정 파라미터가 `stderr=0`, `determined=true`인 확정값처럼 나온다. log-sigmoid의 미분이 경계에서 0이 되어 free-coordinate 오차를 물리 좌표에서 0으로 눌러 버린다. | `clean_two_arc_spectrum`을 `R0-p(R1,CPE1)-p(R2,CPE2)-CPE9`로 fit. `CPE9_Q=999.999997`(상한 1000), `CPE9_n=0.300000`(하한 0.3)이 둘 다 `stderr=0`, `determined=true`, `undetermined=[]`였다. | 경계 파라미터는 무조건 `determined=false`; 경계에서는 `stderr=None` 또는 one-sided/profile interval. 행 단위 판정을 회귀 시험으로 고정한다. |
| 2 | 높음 | `packages/wrdkit/src/wrdkit/eis/fit.py:229-252,262-306` | `p(CPE,R)`처럼 병렬 구성원 순서만 바꾸면 arc 정렬이 직렬 `R0`까지 바꾼다. 저장 χ²와 반환 파라미터·곡선이 서로 다른 해를 가리킨다. | `Rs=.1, R1=20,Q1=1e-6,n1=.9,R2=60,Q2=4e-6,n2=.5`, 0.5% noise(RNG 13)를 `R0-p(CPE1,R1)-p(CPE2,R2)`, seed 0으로 fit. 보고 χ² `2.32168e-5`, 반환 곡선 재계산 χ² `0.0354786`(1528배), 반환 `R0=20.4317 Ω`. | 문자열상 앞 R을 찾지 말고 AST에서 같은 `p()` branch의 R·CPE만 짝짓는다. 정렬 후 곡선·residual·χ² 불변을 검증한다. |
| 3 | 높음 | `packages/wrdkit/src/wrdkit/eis/derive.py:137-160,191-237` | 회로 앞에 L이 오면 직렬 `R0`를 벌크 저항으로 잘못 넣고, 전도도 세 값을 모두 틀리게 계산한다. | `L0-R0-p(R1,CPE1)-p(R2,CPE2)`, `L0=1e-6 H,R0=5,R1=20,R2=40 Ω`, 두께 `.01 cm`, 면적 `1 cm²`. 실제 출력 bulk `.002`, GB `.0005`, total `.000153846 S/cm`/`65 Ω`; 기대 `.0005`, `.00025`, `.000166667 S/cm`/`60 Ω`. | 회로 첫 글자 대신 top-level AST에서 bare series R을 식별한다. topology가 모호하면 전도도는 `None+reason`. |
| 4 | 높음 | `packages/wrdkit/src/wrdkit/eis/drt.py:120-204,245-329` | 비음수 선형문제의 해가 KKT 최적점에 멀리 있는데도 L-curve가 그것을 추천한다. 깨끗한 단일 RC가 저항 절반과 가짜 봉우리 8개로 보인다. | `Z=20/(1+jωRC)`, `R=20 Ω,C=1e-3 F,R∞=0`, `f=1e6..1e-2 Hz`, noise 0. 기본 TRF의 λ `1e-4`: residual `172.291`, `Rp=9.897 Ω`, 8 peaks, χ² `153.804`, `optimality=236778`; 더 큰 λ `1e-2` residual은 오히려 `.557`. 같은 행렬을 BVLS로 풀면 λ `1e-4`에서 residual `.147`, `Rp=20.134 Ω`, 1 peak. | column scaling+BVLS를 쓰거나 KKT/optimality를 통과한 해만 후보로 둔다. λ 증가 시 residual 비감소·벌점 norm 비증가 불변식이 깨지면 추천하지 않는다. |
| 5 | 높음 | `packages/wrdkit/src/wrdkit/eis/drt.py:99-109,197-204` | 같은 γ에 대해 forward kernel이 뜻하는 분극저항과 `total_polarisation_ohm` 보고값이 다르다. 화면의 "전체 분극"이 그린 곡선과 수치적으로 일치하지 않는다. | 대역 밖 endpoint 질량이 생기는 단일 RC 반례에서 kernel의 DC 기여 `.00360963 Ω`, 보고 total `.00336600 Ω`(7.24% 차이). endpoint-only γ는 정확히 2배 차이. `_kernel`은 `np.gradient(log τ)`의 full endpoint weight, total은 trapezoid half weight를 쓴다. | kernel과 보고값에 완전히 같은 quadrature weights를 사용하고, `Z(0)-R∞ == reported Rp` 수치 불변식을 시험한다. |
| 6 | 높음 | `apps/web/src/pages/SpectrumDetail.tsx:403-455` | 서버 fit과 다른 회로를 브라우저가 재구성해 "맞춤" 선으로 그린다. 브라우저 구현은 C·L·Ws·Wo와 중첩 topology를 무시한다. | 서버 `R0-L1`, `R0=1 Ω,L1=1e-3 H,f=1000 Hz`는 `1+j6.283`, 화면 재계산은 `1+j0`. `R0-Ws1`/`R0-Wo1`도 서버 `-Im=0.0103006`인데 화면은 0. UI는 임의 회로 문자열을 받으므로 preset 밖 입력으로 바로 도달한다. | 서버가 동일 `Circuit`으로 계산한 fitted curve를 응답하거나, 검증된 동일 AST 평가기를 공유한다. 지원 못 하는 회로는 선을 그리지 않고 이유를 적는다. |
| 7 | 높음 | `apps/web/src/lib/origin.ts:258-268` | 화면에서 "미결정"인 fit 파라미터가 클립보드에서는 일반 숫자와 1σ로 나가 다시 확정값처럼 보인다. | `FitParameter{name:'CPE1_n',value:.58,stderr:null,determined:false}`를 `fitParametersTsv()`에 넣으면 `CPE1_n\t0.58\t--`. 기존 `origin.test.ts:308-315`가 이 잘못을 정답으로 고정한다. | `determined=false`이면 값도 `--`로 내거나 status 열을 반드시 추가한다. 화면과 export의 판정을 같은 함수로 고정한다. |
| 8 | 높음 | `apps/api/app/routers/samples.py:117-129`; `apps/api/app/services.py:355-366`; `packages/wrdkit/src/wrdkit/health.py:40-62` | POST에서 사용자가 `reference_cycle`을 명시해도 `reference_cycle_source`가 빈 값이다. formation 없는 schedule을 읽으면 입력값이 1로 덮여 retention 기준이 달라진다. | 빈 DB에서 `SampleIn(name='x',reference_cycle=3)` 생성 후 저장값은 `3/source=''`; formationless 해석 결과 `(1,'formationless')`. PATCH로 3을 넣으면 source가 `user`라 보존되어 POST와 다르다. | `payload.model_fields_set`에 `reference_cycle`이 있으면 POST도 source=`user`. POST+schedule의 회귀 시험을 추가한다. |
| 9 | 높음 | `apps/api/app/routers/samples.py:185-207`; `apps/api/app/models.py:304-305`; `apps/api/app/routers/eis.py:111-115,163-188`; `apps/api/app/db.py:17-22` | 셀 A를 지운 뒤 SQLite가 같은 id를 셀 B에 재사용하면 A의 EIS가 B의 측정으로 재귀속된다. | A(id=1)에 spectrum 업로드 → A 삭제 → detail은 `sample_id=1,name=null` → B 생성(id=1) → 같은 spectrum이 `sample_name='B'`, B 필터에도 등장. 삭제는 cycling `Run`만 detach하고 `SpectrumRecord`는 남긴다. | 셀 삭제 전 `Run`·`SpectrumRecord`처럼 `sample_id`를 가진 모든 자식 연결을 명시적으로 detach하고 SQLite foreign keys를 켠다. id 재사용 통합 시험을 둔다. |
| 10 | 높음 | `packages/wrdkit/src/wrdkit/eis/biologic.py:99-168`; `packages/wrdkit/src/wrdkit/eis/spectrum.py:43-46` | `.mpr` module 길이가 1바이트만 손상돼도 행 anchor가 이동하여 무의미한 유한/비유한 수를 정상 스펙트럼처럼 수용한다. | 정상 합성 `.mpr`의 `VMP data` payload length만 `N→N+1`. 기대 첫 점 `f=100000,Re=5.11886,Im=-.613108`; 실제 `f=-.0001905,Re=-4.18e-17,Im=-9.46e29`, 31점, API 201. | module 경계가 다음 `MODULE`/EOF와 연속인지 확인하고, 필수 값 finite·주파수 양수, 저장 magnitude·phase와 Re/Im 교차검산을 한다. |
| 11 | 높음 | `packages/wrdkit/src/wrdkit/eis/biologic.py:207-220,229-237`; `packages/wrdkit/src/wrdkit/eis/spectrum.py:43-46` | `.mpt` 열 수 불일치가 오류가 아니라 행 삭제 또는 열 이동으로 처리된다. 빈 필수 셀은 NaN인 채 API 201이다. | 31행 중 한 행의 마지막 셀 제거 → 30점으로 조용히 축소. `freq,Re,-Im = 1000,5,2` 앞에 셀 `123` 삽입 → `Re=123,Im=-5`. 주파수 셀 blank → points 응답 `null`, fit만 나중에 실패. | 각 행의 열 수가 header와 정확히 같아야 하고 줄 번호와 함께 거절한다. 필수 세 열 finite, 주파수 `>0`을 파서 경계에서 확인한다. |
| 12 | 높음 | `apps/api/app/storage.py:55-85`; `apps/api/app/routers/eis.py:230-263` | EIS `points.npz`가 원본 SHA와 결합되지 않아 다른 셀의 cache를 같은 spectrum id/name 아래 반환한다. | A(`R0≈5`)와 B(`R0≈50`) 업로드 후 B의 `points.npz`를 A cache 경로에 복사. A 조회는 200이지만 첫 Re가 `5.118863→50.118862`. | cache에 source SHA·format·row count를 넣고 DB의 기대 SHA와 검증한다. 불일치/손상은 불변 원본에서 재파싱해 원자적으로 교체한다. |
| 13 | 높음 | `apps/web/src/pages/Eis.tsx:58-80`; `apps/api/app/routers/eis.py:282-359` | EC-Lab의 `_C01` 접미사 때문에 맞는 `.mps`는 빠지고, 파일이 하나씩이면 이름이 다른 `.mps`가 붙어 타 실험의 조건을 측정 조건처럼 저장한다. | `A_C01.mpr+A.mps`, `B_C01.mpr+B.mps`를 함께 올리면 둘 다 settings 없이 "2개 올렸습니다". `A_C01.mpr+B.mps`만 올리면 cardinality fallback이 B의 amplitude/device를 A에 붙인다. | data stem의 `/_C\d+$/i`를 정규화한 뒤 유일한 exact match만 허용한다. 불일치·중복은 파일명을 보이며 중단하고 서버도 독립 검증한다. |
| 14 | 높음 | `packages/wrdkit/src/wrdkit/gitt.py:108-150` | CHARGE Q/DISCHARGE Q가 cycle마다 0으로 reset될 때 reset 차분을 실제 역방향 용량으로 누적해 다사이클 GITT의 x축을 되감는다. `cycle_index`는 읽지 않는다. | 네 charge pulse의 실제 누적 끝용량이 `[0,.5,1,1.5] mAh`가 되게 하되 세 번째에서 cycle `0→1`, counter `1→0` reset. 실제 pOCV x는 `[0,.5,0,.5]`. 합성 fixture는 cycle 0 고정이라 통과한다. | cycle 경계를 감지해 각 counter의 첫 값을 새 offset에 이어 붙인다. charge/discharge 각각의 per-cycle delta를 부호 있게 누적하는 다사이클 시험을 둔다. |
| 15 | 높음 | `packages/wrdkit/src/wrdkit/gitt.py:288-310,369-395` | √t 직선의 slope와 R²를 구하지만 ΔE_t에는 slope를 쓰지 않고 "10% 뒤 첫 샘플→펄스 끝" 단순 차를 넣는다. 같은 τ를 쓰므로 D가 조용히 2.19배가 된다. | 완전한 √t transient에서 이론 ΔE_t `.03 V`; 실제 `.0202667 V`. 같은 geometry/ΔE_s로 기대 D `5.78536e-7`, 출력 `1.26767e-6 cm²/s`(2.191배), R²는 1. | IR 제외 구간의 fitted slope와 펄스 시작 원점으로 `ΔE_t = slope·sqrt(τ)`를 정의하고, 실제 펄스 끝이 아닌 닫힌식 값과 대조한다. |
| 16 | 높음 | `packages/wrdkit/src/wrdkit/gitt.py:357-408` | 짧아서 건너뛴 휴지 뒤에도 `previous_relaxed`는 그 이전 시리즈 값으로 남아 다음 펄스의 ΔE_s를 먼 두 휴지 사이에서 잰다. 방향 전환도 시리즈를 끊지 않는다. | 중간 rest만 60 s, 나머지 600 s, `min_rest_s=100`: 다음 accepted ΔE_s가 `.10 V`가 되어 정상 `.05 V` 대비 D가 정확히 4배. charge→무휴지→discharge에서는 첫 discharge D가 다음 정상값보다 약 113,000배 작았다. | 건너뛴 pulse/rest와 방향 전환에서 series state를 reset한다. 새 series 첫 pulse는 반드시 `D=None`과 "직전 휴지 없음" 이유를 낸다. |
| 17 | 높음 | `packages/wrdkit/src/wrdkit/gitt.py:249-281,353-408`; `apps/api/app/schemas.py:841-851`; `apps/web/src/pages/GittDetail.tsx:238-272` | diffusion point가 ADR 0020이 요구한 `rest_s`·`drift_mv`를 버린다. 이완되지 않은 rest에서도 R²만 좋으면 D를 확정 숫자로 내며 화면에는 반례 근거가 없다. | 휴지 끝 residual drift를 `[20,0,20,0] mV`로 합성. pOCV에는 drift `.69/2.07 mV`가 보이지만 diffusion은 모두 `R²=1,reason=''`; ΔE_s `.03/.07/.03 V`, D `4.56e-7/2.48e-6/4.56e-7`, 정상 대비 `.36×/1.96×`. | diffusion 응답·표·export에도 preceding/following `rest_s`와 drift를 보존한다. 충분히 이완됐는지 판정할 정책이 없으면 숫자를 `None+reason`으로 보류하거나 최소한 숫자와 증거를 같은 행에 둔다. |
| 18 | 높음 | `packages/wrdkit/src/wrdkit/gitt.py:225-243,250-255,397-413`; `apps/web/src/pages/GittDetail.tsx:39-69,238-272`; `apps/web/src/lib/origin.ts:299-309` | pOCV는 discharge 용량을 양의 증가축으로 바꾸지만 diffusion은 첫 점만 빼서 discharge x를 음수로 내보낸다. 같은 화면의 두 결과가 서로 반대 방향이다. | discharge-only 네 pulse. pOCV x `[0,.5,1,1.5]`, diffusion 표·그래프·TSV x `[0,-.5,-1,-1.5]`, 모두 같은 `용량(mAh)` label. | direction을 `DiffusionPoint`에 보존하고 pOCV와 같은 branch별 baseline/sign 변환을 적용한다. |
| 19 | 높음 | `apps/web/src/components/DrtPanel.tsx:23-49,85-160`; `apps/web/src/lib/hooks.ts:13-59` | 평활 차수를 바꾼 직후 새 버튼 값 아래 이전 차수의 γ가 남아 있고 복사도 가능하다. 새 응답 후에도 이전 suggested index가 남아 새 차수의 추천 λ와 다른 행을 기본 선택할 수 있다. | order 1 응답의 `suggested_index=2`를 연 뒤, 지연되는 order 2(`suggested_index=0`)를 선택. `useAsync`가 old data를 유지하고 reset effect 뒤 old data가 index 2를 다시 채운다. 지연 중 Copy는 order 1 TSV이고, 새 응답 뒤에도 index 2가 유지된다. | 응답에 `derivative_order`를 넣어 control과 일치할 때만 표시·복사한다. dependency 변경 시 data/index를 함께 무효화하고 새 응답마다 그 응답의 suggestion으로 초기화한다. |
| 20 | 중간 | `packages/wrdkit/src/wrdkit/eis/drt.py:207-242,303-343` | 측정 대역 밖 τ-grid endpoint의 최대는 `find_peaks`가 절대 peak로 만들지 않아 "대역 밖 봉우리 제외"를 우회하고 추천된다. | 측정 `1..100 kHz`, 실제 process `10 MHz`, `Z=5+20/(1+jωτ)`. γ 최대는 grid index 0, 환산 `316.228 kHz`로 대역 밖인데 `peaks=[]`, λ `.001` 추천, 이유는 "봉우리 0개". | `peaks` 목록뿐 아니라 원본 γ의 endpoint mass/maximum도 대역 검사한다. grid-edge pile-up을 end-to-end 시험한다. |
| 21 | 중간 | `apps/api/app/routers/eis.py:329-359`; `apps/api/app/storage.py:33-44,151-170`; `packages/wrdkit/src/wrdkit/eis/biologic.py:240-283` | 올린 `.mps` 원본과 파서가 모르는 설정이 저장되지 않아 재파싱할 수 없는 계측 설정 손실이 생긴다. | `.mps`에 `Custom correction ENABLED`, `Safety limit 99` 추가 후 업로드. detail settings와 uploads 어디에도 두 줄이나 `.mps` 원본이 없다. parser 개선 후에도 되찾을 바이트가 없다. | `.mps`도 content-addressed 원본으로 보존하고 SHA·원래 이름을 spectrum에 연결한다. 해석한 subset과 원문 보존을 분리한다. |
| 22 | 중간 | `apps/api/app/routers/eis.py:282-320` | 같은 raw의 두 번째 업로드가 새 sample/kind/cycle/settings를 조용히 무시하면서도 201을 내 사용자는 새 컨텍스트에 붙었다고 믿는다. | 같은 `.mpr`를 먼저 sample A/solid, 다음 sample B/liquid/cycle 200으로 업로드: 둘째도 201이지만 A/solid/cycle null. `_C01` pairing 실패 후 맞는 `.mps`를 재업로드해도 dedup가 settings parsing 전에 반환해 영구 공란. | 409로 기존 record와 차이를 명시하거나, 허용된 빈 metadata만 채우는 명시 계약을 둔다. 응답에는 `created/duplicate`를 구분한다. |
| 23 | 중간 | `apps/api/app/routers/eis.py:230-263,282-320`; `apps/api/app/routers/gitt.py:102-107,125-160`; `apps/api/app/storage.py:68-101` | cache/raw가 사라졌을 때 화면은 재업로드를 시키지만 동일 SHA dedup가 저장·cache 재생성을 건너뛰므로 안내대로 해도 복구되지 않는다. | EIS cache 삭제 → GET 409/재업로드 안내 → 같은 bytes 업로드 201 → 여전히 409. GITT raw 삭제 → pOCV 409 → 같은 bytes 업로드 201 → 여전히 409. EIS는 cache write 전 crash로 자연 발생할 수 있다. | 불변 raw가 있으면 EIS cache를 자동 재파싱하고, raw가 없으면 dedup upload가 원본과 cache를 복구한다. 불가능한 안내를 제거한다. |
| 24 | 중간 | `apps/api/app/schemas.py:730-743,811-818`; `apps/api/app/routers/eis.py:391-395`; `apps/api/app/routers/gitt.py:193-197` | 범용 `clear`가 계측기에서 온 frequency range·duration·start time까지 지워 raw-only metadata를 조용히 손실시킨다. dedup 재업로드로도 복구되지 않는다. | EIS PATCH `clear=['frequency_start_hz','frequency_end_hz']` → 200/null. GITT PATCH `clear=['duration_s','start_time']` → 200/null. | 사용자 편집 필드 allowlist만 clear 허용하고 measured/parser fields는 422. 필요하면 raw에서 재생성하는 별도 명령을 둔다. |
| 25 | 중간 | `packages/wrdkit/src/wrdkit/gitt.py:357-408`; `apps/api/app/routers/gitt.py:250-267`; `apps/web/src/pages/GittDetail.tsx:112-162,249-270` | 뒤 휴지가 없거나 짧은 pulse는 diffusion 결과에서 행 자체가 사라져 total과 이유가 거짓이 된다. | 네 pulse에서 마지막 rest 제거: 실제 pulse 3, API total 2. 모든 rest 60 s에 `min_rest_s=600`: 실제 pulse 4인데 `total=0,points=[],reasons=[]`; 화면의 "아래 이유" 자리도 빈다. | 모든 pulse마다 `DiffusionPoint(d=None,reason=...)` 한 행을 유지하고 `total`은 발견 pulse 수, `usable`만 성공 수로 둔다. |
| 26 | 중간 | `packages/wrdkit/src/wrdkit/gitt.py:99-105,121-140` | rest에 작은 nonzero offset이 있으면 p90 기반 문턱이 그 offset에서 정해져 파일 전체를 하나의 charge pulse로 합친다. 계측기가 준 CELL STATUS도 쓰지 않는다. | 1 mA pulse 20 samples/300-sample rest에 rest current `+1 µA`와 status=rest. p90=`1 µA`, threshold=`.1 µA`; 960점 전부 한 charge block, pOCV 0점/skipped 1. | CELL STATUS를 1차 권위로 쓰고 current는 fallback으로 둔다. fallback은 bimodal cluster/known rest floor로 정하며 경계 증거를 응답한다. |
| 27 | 중간 | `apps/web/src/pages/SpectrumDetail.tsx:82-102,205-211`; `apps/web/src/components/Plot.tsx:388-460` | Bode가 8-decade 주파수를 선형 x축에, Ω와 degree를 같은 선형 y축에 겹쳐 유효 데이터 대부분을 읽을 수 없게 만든다. export 코드는 두 y 단위가 섞이면 안 된다고 이미 인정한다. | `f=[1e-2,1,1e2,1e4,1e6]`, magnitude `[1000,500,100,10,1]`, phase `[-90,-60,-30,-10,0]`. 10 kHz 이하가 폭 1%에 몰리고 phase는 `-90..1000` y축 바닥에 눕는다. | log-frequency x와 magnitude/phase 독립 y scale 또는 두 패널을 사용한다. 실제 axis config를 시험한다. |
| 28 | 중간 | `apps/web/src/pages/SpectrumDetail.tsx:381-388,495-637`; `apps/api/app/schemas.py:730-743` | 전도도 화면은 "셀이나 스펙트럼에 면적을 적으라"고 하지만 스펙트럼 편집기에 `area_cm2` 입력이 없어 sample 미부착 데이터에서는 완료할 수 없다. | sample 미부착 solid+sym spectrum에 thickness 입력 후 fit → missing `면적`; 같은 화면의 편집 필드는 config/sample/cycle/thickness뿐이다. API PATCH는 area를 지원하지만 UI 경로가 없다. | thickness와 함께 area 입력·clear를 제공하고 안내대로 결손을 해소하는 UI 시험을 둔다. |
| 29 | 중간 | `apps/web/src/pages/Eis.tsx:31-80`; `apps/web/src/pages/SpectrumDetail.tsx:495-637`; `apps/api/app/routers/eis.py:311-320` | 업로드 때 잘못 고른 liquid/solid 종류를 화면에서 교정할 수 없다. 맞는 탭에서 재업로드해도 dedup가 옛 kind를 유지하면서 "올렸습니다"라고 한다. | 기본 liquid 탭에서 solid `.mpr` 업로드 → solid 탭에서 같은 bytes 재업로드 → 성공 문구지만 solid 목록은 비고 liquid preset/아크 의미로 남는다. backend raw PATCH만 가능하고 detail에는 selector가 없다. | detail에 kind 교정 UI를 제공하고 duplicate를 성공 신규 업로드처럼 말하지 않는다. relabel 전후 fit 의미를 명시한다. |
| 30 | 중간 | `apps/web/src/components/CellSpectra.tsx:28-50,78-83,116-122`; `apps/api/app/routers/eis.py:227-228`; `apps/web/src/lib/hooks.ts:13-59` | 셀에 13 spectra가 있으면 첫 화면과 "전부"가 API 제한 12를 스스로 넘겨 항상 실패한다. 선택 변경 중 chips와 그래프/clipboard도 서로 다른 집합을 말한다. | 13개 연결 → 초기 points 요청 422. 12개 성공 뒤 13번째 선택 → 13 chips on인데 stale 12개 그래프/TSV. A+B load 뒤 B를 끄고 새 요청을 지연하면 chip은 off인데 Copy는 A+B를 낸다. | 선택을 12로 제한하고 누락 수를 말하거나 endpoint 계약을 바꾼다. 요청 ids와 응답 ids가 같을 때만 plot/copy한다. |
| 31 | 중간 | `apps/web/src/pages/SampleDetail.tsx:1112-1133` | 이름 편집기를 열어 둔 사이 다른 사용자가 바꾼 이름을, 아무 글자도 안 친 blur가 옛 값으로 덮어써 동시 수정 데이터를 잃는다. | A에서 `Old` 이름 input focus만 함 → B가 `New`로 PATCH → live prop은 `New`, draft는 `Old` 유지 → A blur → `Old!==New`라 PATCH `Old`. | 편집 시작 base와 touched 여부를 보관한다. untouched draft는 외부 값으로 갱신하고, touched+version 변화는 conflict로 저장 중단한다. |
| 32 | 낮음 | `apps/web/src/pages/GittDetail.tsx:59-71,160-162`; `packages/wrdkit/src/wrdkit/gitt.py:383-405` | 코어·표·TSV는 `D=0`을 usable 숫자로 보지만 그래프는 truthy filter로 버리고 "가정을 통과한 펄스 없음"이라고 말한다. | `points=[{d_cm2_s:0,...}],missing=[],usable=1`. 표는 `0.000e+0`, TSV도 0, 그래프는 빈 상태 문구. | null 여부를 명시적으로 검사한다. 0이 물리적으로 무효면 코어에서 `None+reason`; 유효하지만 log축 불가면 그 이유를 화면에 적는다. |
| 33 | 낮음 | `apps/web/src/lib/format.ts:104-135` | 파일명 힌트 regex가 지원하지 않는 소수점 쉼표·과학 표기의 suffix만 떼어 진짜 질량/두께 근거처럼 보여 준다. | `massFromName('cell_17,5mg')=5`, `massFromName('cell_1e-3mg')=3`; `thicknessFromName('pellet_70,5um')=5`, `('pellet_1e2um')=2`. | 숫자 앞뒤 token 경계를 함께 검사하고 전체 numeric token을 parse할 수 없으면 `null`. 이 네 입력을 회귀 시험으로 둔다. |

## 재현하지 못했거나 정책 결정을 먼저 요구하는 의심

| 항목 | 파일:줄 | 확인한 반례 | 결정이 필요한 것 |
| --- | --- | --- | --- |
| 전고체 세 번째 arc를 전체 전도도에 더함 | `packages/wrdkit/src/wrdkit/eis/derive.py:83-88,208-237` | `R0=5,R1=10,R2=20,R3=70 Ω`, 두께 `.01 cm`, 면적 `1 cm²`이면 code는 total `100 Ω`, σ `.0001 S/cm`. 그런데 R3 label은 "전극 계면일 수 있음"이다. bulk+GB만이면 `30 Ω`, `.000333 S/cm`. | 세 번째 arc가 전해질 저항인지 계면 저항인지 회로 계약이 아직 없다. 정체 미정이면 total을 `None`으로 둘지, 사용자가 포함 여부를 정할지 결정해야 한다. |
| GITT 첫 pulse 용량을 0으로 버림 | `packages/wrdkit/src/wrdkit/gitt.py:174-175,225-243` | raw pulse-end 누적용량 `[.5,1,1.5,2]`가 pOCV에서 `[0,.5,1,1.5]`가 된다. ADR 0020은 "펄스 끝 용량"이라고만 하고 상대 baseline임을 정하지 않는다. | 화면/내보내기가 "시리즈 첫 pulse 대비 상대 용량"을 뜻하는지, 파일 시작부터 누적인지 분석 계약을 정해야 한다. |

실측 `.mpr/.mps`가 없어 EC-Lab 버전별 column table 전체와 실제 module header 배치를
검증하지 못했다. 따라서 "현재 `COLUMNS`가 모든 실물에서 맞다"는 주장도 하지 않는다.
다만 #10·#11은 합성 형식 안에서도 검증을 우회해 틀린 수를 수용하는 독립 결함이다.

## 기존 시험이 못 잡는 모양

| 연결 항목 | 현재 시험이 통과하는 이유 | 필요한 회귀 주장 |
| --- | --- | --- |
| #1·#2 | boundary 시험은 `undetermined OR 전체 reason`이라 행이 `determined=true`여도 통과한다. arc 시험은 `p(R,CPE)`만 쓰며 반환 곡선과 저장 χ²의 일치를 보지 않는다. | 경계 행 자체가 미결정인지, `p(CPE,R)` 반환 곡선의 재계산 χ²가 저장값과 같은지 확인. |
| #4·#5·#20 | DRT 시험은 추천 index가 0 이상인지만 보고, 대역 밖 검사는 구현이 만들지 못하는 가짜 `DrtPeak`를 직접 주입한다. | clean `R∞=0` one-RC의 Rp·봉우리 수·KKT, λ sweep 단조성, endpoint pile-up, kernel DC와 total 일치. |
| #6·#19 | 화면 fit 시험은 R/CPE preset만 보며 Plot series의 실제 숫자를 검사하지 않는다. DRT order 시험은 새 URL만 보고 지연 응답과 clipboard를 보지 않는다. | L/Ws/Wo server curve 대 overlay 비교; 서로 다른 suggestion을 가진 deferred order 응답에서 표시·복사 provenance 확인. |
| #7 | `origin.test.ts:308-315`가 `determined=false` 값 `0.58`을 내보내는 현 동작을 정답으로 고정한다. | 미결정 행은 숫자로 내보내지 않는다는 화면/export 공통 계약. |
| #8·#9 | reference-cycle 시험은 PATCH만, sample delete 시험은 cycling Run만 붙인다. | POST explicit reference+formationless schedule; EIS 연결 후 delete와 id 재사용. |
| #10·#11 | MPR은 preamble/unknown column만 손상시키고 payload length는 안 건드린다. MPT는 정상 행·소수점 쉼표·header line 수만 본다. | module length ±1, 행 열 수 ±1, blank/NaN/Inf/비양수 frequency를 업로드 경계까지. |
| #12·#13·#21-#24·#29 | cache 시험은 삭제만, MPS backend 시험은 같은 stem을 직접 전송, dedup 시험은 같은 metadata만 반복한다. | 서로 다른 SHA cache 교환; `_C01` 다중/오짝; unknown MPS 원문; duplicate metadata 차이; reupload 복구; measured-field clear 거절; UI kind correction. |
| #14-#18·#25·#26·#32 | `synthetic.make_gitt`는 cycle 0 고정이고, D 기대값을 구현이 낸 `delta_et`에서 다시 계산한다. 짧은/없는 rest와 discharge x, offset-current, D=0을 보지 않는다. | cycle-reset counter를 손으로 이어 붙인 기대 x; slope·√τ의 닫힌식 ΔE_t; skipped rest/방향 전환 state; 모든 pulse 보존; status-rest offset; 0의 계약. |
| #27·#28·#30·#31·#33 | Bode axis config와 누락값 해소 경로가 없고, CellSpectra fixture는 2개뿐이다. rename은 editing 중 prop 변경을 만들지 않으며 regex는 숫자 뒤 경계만 본다. | 실제 scale/dual-axis, area 입력 완료, 12/13 selection+deferred clipboard, concurrent rename conflict, 앞 경계가 깨진 숫자 token. |

별도로 `apps/api/tests/test_eis.py:205-212`의 "failed fit stored" fixture는 실제로
`success=true`, χ² `3.55e-16`으로 수렴했다. 실패 저장 경로를 검증하려면 측정 대역
밖 window(예: `2e6..3e6 Hz`)처럼 실제 `success=false`가 되는 입력을 써야 한다.

## 정상으로 확인한 것

- 측정 Nyquist, CellSpectra, `nyquistTsv`는 모두 raw `z_im`을 정확히 한 번만
  뒤집어 `−Z″`로 보였다. Bode export 열도 frequency, magnitude, phase 순서다.
- 서버의 R·C·L·CPE·W·Ws·Wo 식과 단위는 impedance.py의 공식 element 구현과
  일치했다. interior log-sigmoid Jacobian 역변환도 맞았다. #1은 경계에서만 생긴다.
- 표준 `p(R,CPE)`에서는 값과 stderr가 같은 순열로 움직였다. W/Ws/Wo/L 합성
  clean·1% noise를 seed 0..7로 돌렸을 때 같은 해로 수렴했고 truth 대비 약 2.2%
  안이었다.
- DRT kernel의 `1/(1+jωτ)·dlnτ`, γ 비음수 구속, R∞·L 벌점 제외 자체는 구현돼
  있다. 결함은 solver optimality, endpoint 판정, 보고 적분의 불일치다.
- `UnknownColumn`은 등록되지 않은 MPR column을 막았다. 정상 MPT header 경계와
  소수점 쉼표도 처리했다. sample 존재 검증, 원본을 지우지 않는 spectrum 삭제,
  GITT의 raw 재파싱, `kind/kind_now`, query-time derived 값의 DB 비저장은 정상이다.
- pOCV/diffusion export는 null을 0으로 만들지 않았고, NavMenu 경계와 유도성 제외
  점 수 표시는 정상이다.

## 리뷰가 못 본 곳

실측 `.mpr/.mpt/.mps`와 실제 GITT `.wrd`가 없어서 계측기 실물 왕복은 못 봤다.
브라우저 Vitest와 실제 Chromium의 uPlot canvas/clipboard도 이 Windows 샌드박스에서는
실행하지 못했고, TypeScript·ESLint와 상태 전이의 직접 반례로만 확인했다. 73파일 중
핵심 parser·수식·API·일곱 화면·export와 지정된 작은 커밋은 열었지만, `Library`의 새
family filter와 `Plot`의 확대·커서 내부 전체, 일반 MaterialFields의 동시 PATCH는 깊게
재감사하지 않았다. 따라서 이 문서는 33건을 하한으로 보며, 실측 파일과 브라우저
E2E가 들어오면 특히 #10·#13·#19·#27·#30을 다시 확인해야 한다.
