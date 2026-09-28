# 믹서 고-Bo LH — 5차 적대 재리뷰 (2026-09-28)

## 0. 판정과 범위

**HOLD.** 기존 수정은 실질적인 강화다. B-NaN·빈 봉인, 바이너리/운동 시계 불일치, 위치 오차 누락, 정지 E0 과잉차단을 다시 재현했고 새 코드가 막는다. 그러나 **새 SLURM 시작 관문의 빈 봉인 통과**, **스모크 증서 이후 추가된 중복 프레임을 놓치는 rest 관문**, **Bo와 실행 환경의 완전 교락**이 남았다. “같은 바이너리의 메시 궤적”과 “같은 초기 입자 침대·같은 혼합 응답”은 서로 다른 명제다.

- 대상: `claude/sdcp-dem-manuscript-si-pqwtv8`의 요청서 포함 커밋 **`091bb21143c426beecd196d6115666fdd49155b1`**. 요청서 파일명은 rereview4지만 본문은 **5차**다.
- 수정 코드 `999a5bf85` 및 `77919b860`, ibb v2 영수증을 함께 심사했다. 이전 `6963632a0`로 되돌려 심사하지 않았다.
- 복사한 대상 소스·문서·STL·영수증 **23/23의 Git blob SHA를 핀과 대조**했다. 원본 Back.stl은 CRLF·EOF 개행 없음까지 보존했다.
- 독립 프로브의 **16개 결과 단언이 모두 성립**했다. 이는 결함 재현·수정 대조가 예상대로 나왔다는 뜻이지 제품 16건 PASS가 아니다.
- DEM/LIGGGHTS·MPI 시뮬레이션, 실제 LH 생성/제출/재개, Git 상태 변경, 생산 코드 수정은 하지 않았다. 임시 합성 덱·덤프·로그와 실제 검사 함수를 사용했다.
- 실 LC/LH/E0 입자 덤프와 ibb 영수증의 원 mesh/log는 이 리뷰에 제공되지 않았다. 따라서 실데이터 접촉 계약·M·상 유지율을 통과시켰다는 판정은 하지 않는다.

## 1. HBR4-01–08 해제 대조

“닫힘”은 해당 반례와 수정 경로의 닫힘이다. 캠페인 실측 PASS와 구별한다.

| 항목 | 재판정 | 검산·한계 |
|---|---|---|
| HBR4-01 영수증 무결성 | **부분** | B 전체 NaN은 `passed=false`, 소비자 거부. 빈 seal.files와 빈 dumps 목록도 거부한다. 다만 기대 끝 step을 봉인 덱이 아니라 미봉인 gen.json에서 읽는 새 완결성 구멍이 있다(HBR5-05). |
| HBR4-02 실행 연결 | **닫힘 — 기존 반례 범위** | 같은 배너·다른 바이너리 거부, 시작 step 2001→3001 거부, in.resume 흔적 거부. 새 MPI 1→20 이식 범위는 별도 미검증(HBR5-04). |
| HBR4-03 거리 오차 | **닫힘** | +80 nm 평행이동에서 u=138.5640775 nm, 벽 겹침률 구간 **0.7669563–1.1330437%**, `TECH`. 옛 거짓 PASS가 사라졌다. 실 영수증의 오차 크기 설명은 정정 필요(HBR5-06). |
| HBR4-04 mesh 우회 | **닫힘 — 비활성화 선택** | STL조차 아닌 mesh_2000.stl을 놓아도 열어 판정 근거로 쓰지 않으며, 끝판 **2.0000000%**는 여전히 REJECT. 숨은 함수의 기하 완전성이 증명됐다는 뜻은 아니다. |
| HBR4-05 스모크 증서 | **부분** | 진짜 판독 결과의 격자 인자를 바꾸면 rest rc=1, 정상 rc=0. 그런데 증서 이후 bin 0 중복 덤프를 추가하면 rest rc=0인 채 재판독은 incomplete(HBR5-02). |
| HBR4-06 실제 LH 덱 | **닫힘 — 코드 배선·비교기 범위** | 런처가 실제로 expected_deck→`--expect-deck`를 넘긴다. 비교기 selftest **24/24**. 전체 Bash 런처 81건은 이 환경에서 재실행하지 않았으므로 그것까지 독립 통과했다고 쓰지 않는다. |
| HBR4-07 정지 E0 | **닫힘 — 입력 동일성을 전제로 한 정적 계산** | 합성 꼭짓점 인근 **0.5000000% → static PASS**, 기대 덱 없으면 TECH, 끝판 2%→REJECT. 과잉차단을 없애면서 1%는 유지했다. 실 E0 3건의 실행 이력·접촉 계약은 별도다. |
| HBR4-08 SE 라벨 | **닫힘 — 문서 표·정정문** | v09의 열을 SE–SE 목표 Bo_code와 SE 관련 CED 고정으로 분리했다. PNG 원본은 이번에 열지 못했으므로 “PNG도 직접 확인”이라고 인증하지 않는다. 이 한계 자체를 새 P1로 세지 않는다. |

핵심 위치: [scripts/check_contact_validity.py:294](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/check_contact_validity.py#L294), [scripts/check_contact_validity.py:599](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/check_contact_validity.py#L599), [scripts/check_contact_validity.py:868](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/check_contact_validity.py#L868), [dem_scripts/mixer_20260921/launch_highbo.sh:106](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/dem_scripts/mixer_20260921/launch_highbo.sh#L106).

## 2. 새 finding

### HBR5-01 · P1 — 빈/비객체 launch 봉인을 SLURM 시작 관문이 통과시킨다

**무너지는 주장:** S1의 “시작 시 스키마·바이너리·덱·STL·러너·대조기·rank가 전부 서야 LIGGGHTS를 부른다”.

**위치:** [dem_scripts/mixer_20260921/start_check.py:49](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/dem_scripts/mixer_20260921/start_check.py#L49), 특히 59–91; 실제 실행 연결은 [dem_scripts/mixer_20260921/launch_highbo.sh:203](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/dem_scripts/mixer_20260921/launch_highbo.sh#L203).

`json.load`에 성공한 비객체는 빈 dict로 바뀐다. 이어지는 주요 검사가 전부 `if lr and ...`여서 빈 dict이면 건너뛴다. `SLURM_NTASKS`가 정수로 존재하고 기존 log/job_start가 없으면 사유 목록은 비어 있다.

**실제 CLI 검산 — 시뮬레이터는 호출하지 않았다:**

| launch_record.json 내용 | start_check.py 종료 코드 | 생성 기록 |
|---|---:|---|
| 정상 봉인 | 0 | ok=true |
| `{}` | **0** | **ok=true** |
| `null` | **0** | **ok=true** |
| `[]` | **0** | **ok=true** |
| `"invalid"` | **0** | **ok=true** |
| 정상 봉인 뒤 in.mixer 변경 | 3에 해당하는 검사 실패 | ok=false |

마지막 대조는 `check()`의 why/ok를 직접 검사했고, 네 비정상 JSON은 `main`을 포함한 실제 CLI 종료 코드다. JSON 문법 오류나 파일 없음이 아니라 **문법적으로 정상인 빈/오형 봉인**이 반례다. 바이너리와 러너 자리는 실행하지 않는 dummy 파일이었다.

**한정:** 이후 `launch_binding`은 봉인 스키마를 거부한다. 따라서 이것만으로 최종 접촉 PASS까지 위조되었다고 주장하지 않는다. 그러나 러너는 start_check rc=0 다음에 mpirun을 호출하므로, 비싼 실행을 막아야 할 시점의 계약은 이미 무너진다.

**최소 수정 / 해결 증거:** 비어 있지 않은 dict와 정확한 schema/backend를 무조건 요구하고, 필수 nested 구조와 typed 필드를 먼저 검증할 것. 네 입력에 대해 fake mpirun 호출 **0**, 시작 관문 **rc=3**, 거부 영수증만 생성되는 통합 회귀를 둔다. 정상 봉인은 계속 통과해야 한다.

**재현:** §6 공통 명령 → `start_empty_dict / start_null / start_list / start_string / start_changed_deck`.

### HBR5-02 · P1 — “증서에 든 파일은 그대로”가 “지금 판독 대상도 그대로”는 아니다

**무너지는 주장:** HBR4-05의 수정으로 rest가 현재 첫 시드의 유효한 bin 0 증서만 받는다는 주장.

**위치:** [scripts/measure_mixing_index.py:230](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/measure_mixing_index.py#L230), [scripts/measure_mixing_index.py:248](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/measure_mixing_index.py#L248), [dem_scripts/mixer_20260921/launch_highbo.sh:349](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/dem_scripts/mixer_20260921/launch_highbo.sh#L349).

`provenance.frames`는 판독에 사용한 파일들을 봉인한다. `refiles`는 그 **목록 안의 파일만** 다시 해시한다. 현재 디렉터리를 판독기와 같은 규약으로 재열거하지 않는다.

**검산 절차:**

1. 실제 `analyse`로 등록 인자 **16×16×4, n_min=20, x, R=0.013138 m**의 정상 스모크 증서를 만든다. run/E0 이름, 덱, 발사 봉인, 판독기 SHA 모두 맞춘다.
2. 실제 launch_highbo.sh의 **rest Python 관문**을 호출한다: **rc=0**.
3. 증서와 원 파일은 손대지 않고 `post/mix_400.liggghts`를 `post/copy_400.liggghts`로 한 번 더 놓는다. 바이트도 동일하다.
4. 같은 증서로 같은 rest 관문: **rc=0**.
5. 같은 현재 디렉터리를 실제 판독기로 재판독: **25개 중 24개**, `smoke.complete=false`, “같은 step의 덤프 둘 이상”, step 400 결손.

격자 변조 대조는 rc=1이므로 새 provenance 검사가 아예 비활성인 것은 아니다. 추가 파일로 바뀐 **입력 집합**만 놓친다.

**한정:** 첫 런이 진행되며 bin 1 이후의 정상 프레임이 생기는 것을 거부하라는 뜻이 아니다. 닫힌 **bin 0 및 그 평가에 쓰는 t₀/E0 창**의 중복·격자 밖·해석 불가 입력은 증서 유효성에 영향을 준다.

**최소 수정 / 해결 증거:** rest 시점에 등록 스모크 창을 재판독하거나, 판독기와 같은 파일 선택 규칙으로 그 창의 입력 집합·중복 상태까지 재검증한다. 단지 채택된 25파일 해시를 더 강하게 묶는 것으로는 해결되지 않는다. 정상 후속 bin 추가는 통과, bin 0 중복 추가는 거부하는 양쪽 회귀가 필요하다.

**재현:** §6 → `smoke_normal=0`, `smoke_wrong_grid=1`, `smoke_after_duplicate=0`, `smoke_recomputed_duplicate.smoke.complete=false`.

### HBR5-03 · P1 — LH만 MPI로 옮기면 현재 결론의 Bo 효과가 식별되지 않는다

**무너지는 결론:** §5의 “AM 표면 점착을 LC→LH로 올리면 M이 낮아진다”와 이를 근거로 한 Bo 효과 해석. 단순히 두 실행 프로토콜의 차이를 기술하는 것은 가능하다.

**위치:** [docs/reviews/mixer_highbo_prereg_20260927.md:172](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/docs/reviews/mixer_highbo_prereg_20260927.md#L172), [docs/reviews/mixer_highbo_prereg_20260927.md:184](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/docs/reviews/mixer_highbo_prereg_20260927.md#L184), [docs/reviews/mixer_highbo_prereg_20260927.md:205](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/docs/reviews/mixer_highbo_prereg_20260927.md#L205).

관측 설계는 LC=WSL/직렬/구 빌드/재개, LH=ibb/MPI20/새 빌드/fresh다. 관측 차이에 Bo 효과와 환경 효과가 같은 방향으로 들어간다. 한정어는 누락을 공개하지만 두 효과를 분리하지 않는다.

**수치 반례 — 실측값이 아니라 식별성 반례:**

- 참 Bo 효과 = **0**.
- 환경만으로 생긴 세 차이 = **0.12, 0.13, 0.11**.
- 등록식을 그대로 계산하면 Δ=**0.1200000**, SE=**0.0057735027**, 2SE=0.0115470054.
- Δ≥0.10 및 Δ≥2SE를 모두 만족한다.

따라서 “큰 차이”를 얻어도 Bo가 원인이라는 결론은 논리적으로 나오지 않는다. 이 수치는 실제 MPI 효과 크기의 추정이 아니다. 같은 관측을 만드는 대체 원인이 현재 설계에서 분리되지 않음을 보인 것이다.

**동일 seed는 초기 침대 동일의 증거가 아니다.** ibb 영수증이 적은 소스 핀 `3d5c00f2…`의 실제 구현에서 insert는 proc_shift=true로 난수기를 만든다. Random은 seed에 rank offset을 더한다. 기본 multiplier=1이므로 seed 32452843은 rank 0에서 32452843, rank 19에서는 32452862의 내부 상태로 시작한다. pack은 subdomain 경계 거리에도 조건을 건다. 이는 MPI20의 최종 M이 반드시 달라진다는 증명이 아니라, **같은 숫자 seed만으로 동일 삽입을 보증할 수 없다는 코드 근거**다. [fix_insert.cpp:100](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_insert.cpp#L100), [random.cpp:69](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/random.cpp#L69), [random_park.h:56](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/random_park.h#L56), [fix_insert_pack.cpp:486](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_insert_pack.cpp#L486).

**권고 — 저자 선택이 필요한 두 경로:**

1. **Bo 공동개입 효과를 계속 묻는다면:** LC도 LH와 같은 ibb 바이너리·MPI20·실행 스택·fresh 절차에서 등록 세 시드로 비교한다. 추가 런은 이번 회신이 자동 승인하지 않는다. 결과 열람 전에 비교·비용·정규화 절차를 개정 등록한다. 같은 초기 상태를 주장하려면 ID/type/radius/좌표 및 관련 상태를 직접 대조하거나 공통 checkpoint 생성·분기 규약을 별도로 검증한다.
2. **기존 LC를 꼭 재사용한다면:** estimand를 “기존 LC 실행 프로토콜과 새 LH 실행 프로토콜의 차이”로 좁힌다. Bo-only 인과 문장은 버리고, 조건부 A 발동도 그 차이를 Bo 증거로 삼지 않도록 개정한다. 쓸 수 있는 문장: *“등록한 두 실행 프로토콜 사이에서 8회전 후 M의 차이는 Δ …였다. 점착 조건과 실행 환경·재개 이력이 동시에 달라 이 차이를 점착 효과로 분해하지 않았다.”*

seed를 짝지어 차이를 계산하는 **산술 자체**를 금지하는 것은 아니다. “짝이 같은 초기 난수 실현을 공유한다”와 “Bo 효과를 식별했다”를 금지하는 것이다. 단일 bridge 런도 유용한 진단이지만 세 시드·전체 8회전의 환경 효과 상한을 자동 보증하지 않는다.

**해결 증거:** 같은 환경의 적절한 대조 설계 또는 위 복합 프로토콜 estimand를 채택한 저자 개정. 단순 한정어 추가는 미해결이다.

### HBR5-04 · P2 — 1-rank 증서를 20-rank의 측정 오차 경계로 승격한다

**무너지는 표현:** “MPI20 런의 위상·위치 오차 경계가 이 영수증으로 실측 검증되었다”. **MPI20이 틀렸다는 반례는 아직 없다.**

**위치:** [scripts/check_contact_validity.py:616](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/check_contact_validity.py#L616) 및 launch_binding; 요청서 S2.

핀의 실제 `receipt_v2_ibb.json`을 수정하지 않고, 같은 바이너리 SHA·운동 서명·시계·STL에 맞춘 **합성** np20 launch/job_start를 연결했다. 실제 소비자는 수용한다.

- 영수증 접두사: `mpirun --oversubscribe --bind-to none -np 1`.
- 런 봉인/시작 증서: **np20**.
- 소비자: **accepted=true**, 각 경계 **0.001165134578°**, 위치 경계 **3.165315508e-7 m**.

합성 실행 기록으로 **소비자의 비교 항목**을 시험한 것이다. 실제 SLURM job이 실행되었다거나 SHA만으로 실행 사실을 입증했다는 주장이 아니다. 수용 경로에 rank 이식의 검증은 없다.

처방된 강체 회전이 입자력과 무관하다는 것은 이식 가설의 합리적 근거다. 그러나 그 사실만으로 MPI 출력/소유/재개 경로의 수치 경계를 **np1에서 측정한 작은 값과 같게** 둘 수 있는지는 별도의 증명이다. “가정”을 등록해도 측정 증서가 되지는 않는다.

**권고:** 같은 생산 바이너리·MPI20·실행 옵션으로 **입자 없는 A/B 위상 시험**을 마련하고, 삼각형 순서만 달라져도 대조할 수 있게 생산자를 고친 뒤 별도 검토한다. 원칙은 삼각형 내부 vertex 순서 및 삼각형 나열 순서에 불변이되, **면의 연결·중복도·Drum/Front/Back 구성**은 보존하는 비교다. 전체 vertex cloud의 최근접 거리만 비교하는 HBR4-04 방식으로 돌아가면 안 된다. 또는 MPI 경로에 대한 독립적인 수치 상한 증명을 제시한다.

새 시험 없이 진행하는 대안은 np1 경계를 **MPI20 실측 경계로 표시하지 않고** 독립적으로 보증된 더 넓은 경계/위상 무관 상·하한을 쓰는 것이다. 그 결과 TECH이면 그대로 미식별이다. 이 항목은 관측된 MPI 오류가 아니므로 코드 P1 반례와 구분해 P2로 기록하지만, 현재 경계를 쓰려면 해제 증거가 필요하다.

**재현:** §6 → `np1_receipt_on_np20`.

### HBR5-05 · P2 — gen.json의 끝 step으로 완주 기준을 짧게 바꿀 수 있다

**무너지는 주장:** `passed=true`가 봉인된 A/B 덱의 끝까지 측정을 완료했음을 보증한다.

**위치:** [scripts/mixer_restart_phase_test.py:290](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/mixer_restart_phase_test.py#L290), 322, 334–350.

seal의 정확한 목록은 덱과 STL을 포함하지만 gen.json은 포함하지 않는다. 로그 완료 검사와 기대 덤프 집합의 끝은 `g['run_total']`에서 얻는다. A 덱에서 파싱한 motion_clock의 end와 대조하지 않는다.

**실제 함수 검산:**

- 봉인된 A/B 덱·STL은 그대로. A의 motion_clock end=**14,001**.
- gen.json run_total만 **9,500**으로 둔다. n1=9,000, dump_every=500.
- 그 짧은 범위의 합성 덤프와 last_step=9,500 로그, 실제 run.sh의 상태 수집 코드를 사용한다.
- `analyze`: **passed=true**, reasons=[], A=19/B=2.
- 발급된 증서는 run_total=9,500이면서 motion_clock end=14,001이다. 앞쪽 요청 step 2000/2500/3000에는 소비자도 수용한다.

**한정:** 뒤쪽 미측정 step을 요청하면 need_steps 검사가 남아 있으므로 거부한다. 이 반례만으로 8회전 완주 판정이나 최종 M이 초록이 된다고 주장하지 않는다. 다만 “덱을 끝까지 돌린 시험”이라는 증서의 완료 의미는 틀린다.

**최소 수정 / 해결 증거:** A/B의 실제 logical commands에서 end, dump cadence, B의 read_restart 기준 step을 재구성하고 gen.json·run_status·덤프 집합을 그 기준에 맞춘다. gen.json 봉인 추가만으로는 “잘못 생성된 기준과 결과가 함께 맞음”을 막지 못하므로 덱 교차확인이 필요하다. 위 짧은 로그는 거부, 정상 전 길이는 통과해야 한다.

**재현:** §6 → `gen_end_truncated`.

### HBR5-06 · P2(문구·오차 규모) — SE에는 “반경의 약 0.03%”가 아니다

**위치:** 요청서 Q2; 실제 [scripts/mixer_restart_phase_test.py:415](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/mixer_restart_phase_test.py#L415)와 [scripts/check_contact_validity.py:989](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/091bb21143c426beecd196d6115666fdd49155b1/scripts/check_contact_validity.py#L989).

커밋된 v2의 u=**3.1653155079665423e-7 m**를 생성기의 실제 반경으로 나누었다.

| 상 | 반경 (µm) | 100u/r — 겹침률 δ/r의 불확실성 (%p) |
|---|---:|---:|
| AM_P | 681.3 | **0.0464599370** |
| AM_S | 302.8 | **0.1045348583** |
| SE | 75.7 | **0.4181394330** |

SE에서는 위치 오차 항만으로 **1% 문턱의 약 41.8%**를 사용한다. 여기에 회전각 불확실성 영향은 별도다. 이것이 실제 SE 겹침이 0.418%라는 뜻도, 모든 프레임이 TECH라는 뜻도 아니다.

√3는 좌표별 최대 오차를 유클리드 거리로 옮길 때 안전한 상한이다. 실제 39각형 법선의 구조를 이용한 더 조밀한 경계를 유도할 수는 있지만, 오차가 상관되는 방식까지 입증해야 한다. **통과율을 본 뒤 줄이지 말고** 독립 기하/반올림 계약과 음성대조를 먼저 등록한다. 현 보수성을 이유 없이 완화할 필요는 없다.

**해결:** Q2를 위 상별 숫자로 정정하고 실데이터 판정에 위치+각 오차를 유지한다. 코드를 다시 느슨하게 만들라는 finding이 아니다.

## 3. Q1–Q4 답

| 질문 | 판정 | 답 |
|---|---|---|
| Q1 봉인 없는 L/LC에 영수증을 잇지 않음 | **동의** | 현재 파일을 다시 해시해 “당시 발사 봉인”을 소급 생성하면 안 된다. 현 LC는 재개 이력도 있으므로 np1 fresh 메시 시험을 런별 상태 증거로 대체하지 않는다. 상·하한으로 PASS/REJECT를 결정할 수 있으면 그 범위에서 판정하고, 걸치면 TECH를 유지한다. |
| Q2 √3 위치 경계 | **수정안** | 상한 산술은 타당하다. 작은 규모라는 설명은 SE에서 틀린다(HBR5-06). 법선별 엄밀 경계는 후속 선택지일 뿐, 현재 문턱을 살리기 위한 조정은 아니다. |
| Q3 E0 기대 덱의 역사 판 | **동의, 출처 조건부** | 실제 생성에 사용한 commit과 CLI 인자를 먼저 특정해 재생성·비교하는 것은 적절하다. 아무 옛 판이나 찾아 “맞는 판”을 고르면 안 된다. 불일치하면 조사/미식별이지 실행 덱 자체를 기대 정본으로 복제해 자동 닫힘이 아니다. |
| Q4 mesh를 열지 않고 무권위화 | **동의** | 현재 구현은 존재 장수만 notes에 남긴다. 기하 처리를 하지 않아 해당 우회를 닫는다. 재활성화는 상수 한 줄 변경이 아니라 연결/구성 검증과 옛 반례 배터리를 갖춘 새 변경이어야 한다. |

**Q3 독립 재계산:** 현재 생성기의 등록 E0 옵션 `n_total=100000, cgf=151.4, revolutions=0`에서 다음을 얻었다. 세 덱 모두 **7,779 bytes**이며 요청서의 SHA 접두어와 일치한다.

| seed | SHA256 |
|---|---|
| 32452843 | `a38cdc7494671979400c2037fac551b3a2567a64204def8b4b8338064130039c` |
| 49979687 | `b8ba25ace11e1300741d49e0ff6e2aadf47bf0ccd8fd1dd97de2283486582230` |
| 67867967 | `f38f0093433d251a5045a9da70f3750a8e4a8318a77265e413c01ef2afb36439` |

이는 **현 생성기 산출**의 독립 재계산이다. 역사 네 판 전부의 동일성, 실제 WSL 파일의 동일성, 당시 실행 바이트 동일성은 여기서 직접 재현하지 않았다. 정지 계약이 비교하는 것은 주석을 제외한 **명령 토큰**이라는 점도 바이트 동일성 표현과 구별한다(검사기 370행).

## 4. S1–S4 답

### S1 — 제출 봉인 + 시작 대조

**원칙 동의, 현재 구현은 부분.** SLURM의 대기열 틈을 시작 시 재대조하는 것은 필요하고, 실행 중인 러너 사본을 검사하는 것도 옳다. 다만 HBR5-01은 런 전에 고쳐야 한다.

추가로 바이너리 SHA만으로 실행 스택 전체를 봉인했다고 부르면 안 된다. 현재 러너 200–206행은 conda 활성화와 PATH 변경 후 이름으로 mpirun을 해석한다. 제출 시 예상한 mpirun의 realpath/version/hash, 실제 MPI 라이브러리·동적 의존성 식별자, 환경 규약을 기록·대조할 범위를 정해야 한다. conda 활성화 실패도 즉시 중단하도록 한다. **노드명은 기록 대상이지 무조건 같은 물리 노드만 허용해야 한다는 뜻은 아니다.**

first/rest 코호트에도 backend·np·MPI 옵션·환경 규약 ID를 같은 조건으로 유지하도록 봉인하는 편이 맞다. 현재 rest의 코호트 대조는 덱/STL과 lmp SHA 중심이고, 첫 봉인의 np를 새 NP와 비교하는 관문은 없다. 이 항목은 별도 변이 실행을 하지 않은 **소스상 범위 지적**이며, 노드 간 실제 수치 차이가 발생했다고 주장하지 않는다.

### S2 — np1→np20 위상 이식

**수정안 / 현재는 미검증.** HBR5-04의 20-rank 검증 또는 독립 상한 증명이 필요하다. “삼각형 순서가 달라서 비교가 안 됨”은 관측 도구의 문제이지 np1을 np20으로 부를 근거가 아니다.

v1/v2의 **208행 step/error_deg/resid_m을 JSON 숫자로 파싱해 전부 일치**함은 재계산했다. 실 v2 파일 SHA256도 **`f2724c4afd5572f6f90579212274d7c8f6dc756cb99399f141f1822478702a17`**이다. 이것은 서로 다른 두 np1 출력의 해당 필드 일치이며, 원 STL의 모든 좌표 비트 동일성·np20·입자 침대 동일성은 아니다. 원 mesh/log가 없으므로 그 필드들의 측정 자체를 원자료에서 다시 산출하지는 못했다.

### S3 — job_start.json을 소비자에 잇기

**동의, 필요조건이다.** 없다면 거부하는 것은 과하지 않다. 검사기 324–337행은 strict ok, seal hash, 바이너리, 러너, 시작 대조기, ntasks를 묶는다. 작성자의 ㉛ 계열을 포함한 83/83을 실행했다.

그러나 시작 기록은 완료 기록이 아니다. 이것만으로 정상 종료·전 dump 완비·MPI 환경 동등성은 증명되지 않는다. HBR5-01의 malformed seal은 후단 소비자가 막지만 **이미 실행을 허용한 잘못**을 소급 복구하지 못한다.

### S4 — LC 직렬 vs LH MPI

**반대 — 현재 Bo 인과 결론을 유지하는 경우.** 저자의 실행 결정 권한과 비교에서 식별되는 과학적 양은 다르다. HBR5-03의 두 경로 중 하나를 결과 전에 선택해야 한다. 마감·CPU 경합 해소는 다른 기계에서 실행할 근거가 되지만, 그 비교를 Bo 단독 효과로 해석할 근거는 아니다.

## 5. 최소 해제 목록 — 무엇을 고치고 무엇은 그대로 둘까

1. **시작 관문:** 빈/비객체 봉인 네 반례를 fail-closed로 만들고 fake mpirun 호출 0을 회귀로 보인다(HBR5-01).
2. **rest 관문:** 현재 bin 0/t₀/E0 입력 집합이 증서의 유효성 조건을 계속 만족함을 검증한다. bin 0 중복 추가 거부와 정상 후속 bin 추가 수용을 같이 보인다(HBR5-02).
3. **비교의 뜻을 저자가 결정:** 같은 실행 환경 대조를 새로 등록하거나, 복합 실행 프로토콜 비교로 결론·A 발동 해석을 바꾼다(HBR5-03). 이 리뷰는 추가 생산 런을 발사하지 않는다.
4. **위상 증서의 적용 영역:** MPI20 경계를 실증/증명하거나, 그 증서를 MPI20 실측 증거로 쓰지 않는 대안을 명시한다(HBR5-04). 셋 다 동일한 np/실행 스택인지도 묶는다.
5. **완주 기준:** gen.json을 덱의 actual end/cadence/restart 시계와 교차확인하고 짧은 실행의 false-complete를 막는다(HBR5-05).
6. **문서:** 위치 오차의 상별 규모, old LC의 영수증 적용 불가, np1/np20 증거의 범위를 정확히 남긴다(HBR5-06).
7. 위 코드·설계 해제가 실데이터 PASS를 대신하지 않는다. 등록된 LC/LH/E0 접촉 계약, bin 0 기술 스모크, 최종 완결성·부피 QC·평탄성은 각각의 시점에 그대로 적용한다. **1%·Bo·seed·칸 규약을 이 리뷰를 이유로 느슨하게 바꾸지 않는다.**

이미 닫힌 HBR4의 수정은 되돌릴 필요 없다. 특히 mesh 경로를 되살리거나, LC에 발사 봉인을 소급 생성하거나, 위치 경계를 제거하는 것은 해제 방법이 아니다.

## 6. 재현·증거 묶음

동봉 폴더: `mixer_highbo_round5_evidence_20260928/`.

```bash
cd mixer_highbo_round5_evidence_20260928
PYTHONDONTWRITEBYTECODE=1 python3 review_round5_probe.py
# 시뮬레이션 없음. 종료 0; assertions 16개 true.
# 상세: review_round5_output.json
PYTHONDONTWRITEBYTECODE=1 python3 run_selftests.py
```

의존성: Python 3 + NumPy/SciPy. 이 환경은 Python 3.12.14. 실행기와 버전·출력은 동봉 README 및 selftests_output.json에 남겼다. Linux/Bash가 필요한 시험은 별도 제한이 있다.

| 실행한 시험 | 이 리뷰 결과 |
|---|---|
| measure_bed_aspect | 25/25 |
| check_contact_validity | 83/83 |
| measure_mixing_index | 34/34; 선택적 실제 덱 시험 ⑪는 SKIP |
| mixer_deck_diff | 24/24 |
| make_mixer_deck | 89/89 |
| mixer_restart_phase_test | **26개 PASS 후** 생성 run.sh를 호출하는 새 시험에서 Bash 미발견(WinError 2). 전체 종료 코드는 1, **28/28 통과라고 쓰지 않는다** |
| launch_highbo.sh | Bash 구문 검사; 실제 rest Python 관문은 정상·격자 변조·중복 추가로 실행 |
| start_check.py | 정상 함수 대조 + 잘못된 JSON 네 종류의 실제 CLI 실행 |
| test_launcher.sh / check_all.sh | **전체 미실행**. 저자의 81/81·전수 초록을 독립 인증하지 않는다 |

증거 파일: `sources.json`, `source_hash_verification.json`, `external_sources.json`, `review_round5_probe.py`, `review_round5_output.json`, `selftests_output.json`. 합성 프로브의 임시 디렉터리는 종료 시 제거된다. 남긴 수치와 재현 코드는 실 캠페인 관측치가 아니다.

**최종 판정: HOLD**
