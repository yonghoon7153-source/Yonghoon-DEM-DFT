# 믹서 고-Bo LH 4차 적대 재리뷰 — HOLD

작성: 2026-09-28 · 대상 브랜치: claude/stoic-knuth-NObVQ

## 0. 판정과 검토 범위

**HOLD.** 이전 반례를 고친 것은 인정한다. 그러나 새 위상 영수증과 스모크 증서가, 그것을 적용할 실제 런의 기하·실행파일·운동 시계·판독 규약을 충분히 묶지 못한다. **새 P1 4건**이 있다. 이는 LH의 혼합 효과가 나쁘다는 판정이 아니라, 현 검사로 LH 발사 및 후속 판독을 해제할 수 없다는 판정이다.

핵심 재현 세 가지:

- B의 메시 좌표를 전부 NaN으로 만들었는데 영수증은 passed=true, A↔B 최대 차는 **0 m**, 소비자도 수락했다.
- 영수증이 허용하는 **80 nm**의 형상 잔차를 소비자가 버린다. 합성 침대에서 실제 벽 겹침 **1.055680317%**를 **0.950000000%**로 계산하여 PASS했다.
- 다른 폴더의 동일 이름 런을 **2×2×1** 칸으로 실제 판독한 결과가, **16×16×4** 규약의 첫 LH 스모크 증서로 런처 검사에 통과했다.

위 결과는 **실제 생산 함수에 합성 입력을 넣은 반례**다. 실제 L/LC/LH에 NaN·80 nm 변형·잘못된 증서가 발생했다고 주장하지 않는다.

### 고정 스냅샷

- 주 수정: 10c96417513a8c4b8c2057f3320c19ce011cd965.
- 원장 등재: 1ce45c53f10a86c6b107615cefd5a0a7f68f55ec.
- 요청서 §0-b 완주 판정 수정까지 포함한 **검토 코드: ba33a49398b31c79369f032f390b8a62762d2db8**.
- SELF-56 등재: 59800584e16231285670428aef2a7cfb52a7cdcd.

파일 18개의 로컬 복사본은 해당 스냅샷의 Git blob 해시와 바이트 단위로 대조했다. 목록은 증거 묶음의 sources.json에 있다. 문서의 claimed_fixed나 selftest 개수는 수정의 증거로 대신 쓰지 않았다.

**하지 않은 일:** DEM/LIGGGHTS 실행, 캠페인 재개, 생산 LH 덱 생성·발사, 생산 코드 수정, Git 상태 변경. 임시 폴더에서 합성 덱·덤프·로그를 만들고 검사 함수만 호출했다. WSL 접근이 거부되고 대체 Bash에는 setsid가 없어 **test_launcher.sh 전체 실행은 하지 않았다**. launch_highbo.sh의 실제 Python 증서 검사 부분만 추출하여 실행했다.

이 스냅샷에서 WSL의 v1 실행 원자료를 직접 검증하지 못했다. 요청서의 “예정각 오차 1.92×10⁻⁵°, 경계 0.00115°, A↔B 0 m”는 본 리뷰의 독립 실측이 아니다. v09 PNG도 시각 확인하지 못했으므로 그림 라벨까지 닫았다고 쓰지 않는다.

## 1. HBR3-01~08 해제조건 재판정

| 기존 항목 | 판정 | 독립 재현 및 남은 범위 |
|---|---|---|
| HBR3-01 영수증 생산자 | **부분** | A 0장, B 재개 전 1장만 둔 옛 반례는 거부한다. 기대 step 완전성은 개선됐다. 하지만 B NaN과 빈 해시 목록은 통과한다(HBR4-01). 형상 잔차를 인정한 뒤 벽 불확실성에서 빼는 문제도 있다(HBR4-03). |
| HBR3-02 영수증 소비자 | **부분** | v0·잘못된 값·SHA 형식·주기·축·step 미포함 거부는 강화됐다. 그러나 동일 배너의 다른 바이너리 SHA와 다른 회전 시작 step은 수락한다(HBR4-02). |
| HBR3-03 세 점 대신 구간 극값 | **닫힘 — 산술 범위** | 옛 내부 극값 반례: 상한 1.000800000%, 하한 0.992464981% → TECH가 맞다. 새 구간 계산은 그 값을 잡는다. 단, **입력 불확실성 경계 자체의 완전성**은 별개이며 HBR4-03에서 열려 있다. |
| HBR3-04 mesh 덤프의 전체 용기 확인 | **부분** | 끝판을 통째로 뺀 78삼각형은 거부하고, 각과 무관한 끝판 2% 위반은 REJECT한다. 그러나 삼각형 수와 꼭짓점 집합만 보존한 퇴화 끝판은 PASS한다(HBR4-04). |
| HBR3-05 계획 t₀·격자 밖 프레임 | **닫힘** | 평가/E0 t₀ 결손 모두 거부. 격자 밖 step 7301을 넣어도 최종 M=0.450000 유지 + tech. 최종 bin 중복 step은 24/25, M_final=null. |
| HBR3-06 프레임 스키마 | **닫힘** | id 부재·머리 부재·type=1.5를 실제 판독기에 넣으면 해당 step 제외, 24/25, M_final=null, tech. 기존의 조용한 절삭·통과가 재현되지 않는다. |
| HBR3-07 실제 seed 서명 | **닫힘** | 이름만 세 시드이고 내용은 복사한 옛 반례 → 0/3, rc=1. 목표 CED 검사기가 존재하는 것과 런처에서 실제 호출하는 것은 별개(HBR4-06). |
| HBR3-08 first/rest 발사 분리 | **부분** | 일반 run_all에서 LH 제외, first/rest 및 봉인 구조는 개선. 그러나 rest의 실제 검사 코드가 다른 출처·다른 칸 규약의 증서를 받는다(HBR4-05). 전체 프로세스 런처 시험은 이번 환경에서 미실행. |
| HB-01·정본 표기 | **부분** | CED를 Bo_code로 잘못 부른 단위 혼동은 수정. 다만 “SE 관련 모든 쌍의 Bo_code=0.21244”로 읽히는 문장이 남는다(HBR4-08). PNG는 미검증. |
| SELF-56 완주 표지 | **닫힘 — 이번 수정의 계약 범위** | 실제 run.sh의 기록 코드를 타는 20/20 selftest 통과. exit=0 및 로그의 완료 배너/마지막 thermo step을 읽는 수정은 타당하다. 이 결과를 실제 WSL A/B 실행 성공의 대리 증명으로 쓰지는 않는다. |

닫힘은 해당 결함의 닫힘이다. 도구 전체 인증이나 실데이터 승인과 동의어가 아니다.

## 2. 신규 finding 및 실제 함수 반례

모든 독립 반례의 공통 재현 명령은 증거 폴더에서 다음과 같다.

~~~bash
python3 review_round4_probe.py
~~~

원시 반환값·거부 사유·CLI stdout은 review_round4_output.json에 남겼다. 아래 각 항목의 JSON 키로 결과를 찾을 수 있다. 이 명령은 시뮬레이터를 실행하지 않는다.

### HBR4-01 · P1 — B의 비유한 좌표와 봉인 목록 공백이 통과

**위치:** [scripts/mixer_restart_phase_test.py:297](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/mixer_restart_phase_test.py:297>), [scripts/mixer_restart_phase_test.py:310](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/mixer_restart_phase_test.py:310>), [scripts/mixer_restart_phase_test.py:354](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/mixer_restart_phase_test.py:354>), [scripts/mixer_restart_phase_test.py:369](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/mixer_restart_phase_test.py:369>).

A에는 좌표 유한성 검사가 있지만 B에는 없다. B의 차이가 NaN이면 max(0.0, NaN)이 0.0을 유지하여, 최종 ab_max≤허용치 검사를 통과한다.

**검산:** 정상 합성 A 28장과 B 11장의 기대 step·로그·해시를 갖춘 뒤 B의 좌표만 전부 NaN으로 만들고, 실제 기록 코드로 덤프 해시를 다시 기록했다. 반환:

~~~text
passed = true
ab_max_vertex_diff_m = 0.0
rows[*].ab_m = NaN
consumer_accepted = true
~~~

또 seal.files와 run_status.A/B.dumps를 빈 객체로 두면, “있는 항목만” 검사하므로 역시 생산자·소비자가 수락한다. 이는 해시가 맞다는 것과 **필수 파일 전부가 해시에 들어 있다는 것**의 차이다. 임의 위조를 암호학적으로 막으라는 요구가 아니라, 현재 스키마의 누락을 거부하라는 요구다.

**무너지는 결론:** “passed=true이면 B 전체 메시가 A와 일치하고 실행 입력·산출물이 봉인됐다.”

**수정 최소안:** A/B 양쪽 shape·finite를 먼저 검사하고, 집계 및 출력 숫자도 유한성을 강제한다. 생성 계약·덱·STL 및 기대 dump 집합과 해시 목록의 집합을 정확히 대조한다. 빈/부분 목록을 허용하지 않는다.

**해결 증거:** 정상 fixture 성공을 유지하면서 B NaN/Inf, 해시 목록 전체·일부 누락이 생산 단계에서 실패해야 한다.

**재현 키:** review_round4_output.json → nan_B_receipt, empty_seal_lists_receipt, no_A_receipt, no_B_after_restart_receipt.

### HBR4-02 · P1 — “같은 바이너리·같은 step 구조”를 아직 검사하지 않는다

**위치:** [scripts/check_contact_validity.py:212](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:212>), [scripts/check_contact_validity.py:366](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:366>), [scripts/check_contact_validity.py:431](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:431>), [scripts/check_contact_validity.py:455](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:455>).

바이너리 SHA는 **영수증 내부 seal과 영수증 필드끼리** 대조한다. 판정할 런의 launch_record.json과는 대조하지 않는다. 런 연결에는 배너 문자열만 쓴다. 운동 서명은 run 길이와 회전 시작 시계를 제외한다.

**검산 1 — 다른 실행파일 식별자:**

~~~text
receipt.binary_sha256 = 8c06fd57d27948e20fa911bfe2ac2064e1ef930841e644b2c0eee7e7b5bb01cf
run.launch_record.lmp_sha256 = b7fce48a5acce90192ad512a016092f3d6ae6262497e14424341dea9e97271ac
version banner = 동일
load_phase_receipt = 수락
~~~

이 두 SHA는 서로 다른 합성 바이트 파일의 식별자다. 서로 다른 실제 LIGGGHTS 실행을 했다는 뜻은 아니다. 검사가 둘의 불일치를 보지 않는다는 반례다.

**검산 2 — 운동 시계:**

~~~text
시험 덱 회전 시작 = step 2001
판정 덱 회전 시작 = step 3001
motion_signature 동일
need_steps = [3000, 3500, 4000] 모두 A 실측 목록에 있음
load_phase_receipt = 수락
~~~

같은 step 번호 목록은 같은 회전 경과시간의 증명이 아니다. 이것만으로 실제 벽 겹침 오판을 입증한 것은 아니지만, Q1의 핵심 전제가 소비자에서 강제되지 않음을 입증한다.

**무너지는 결론:** “배너+운동 서명+step 부분집합이면 시험 메시 오차 경계를 이 런에 이식할 수 있다.”

**수정 최소안:** 실행 당시 바이너리 해시와 런 봉인을 영수증에 연결한다. 운동 계약에는 회전 시작, 경과 step, 순서가 있는 mover 생성/해제·재개 상태 등 실제 궤적을 결정하는 시계를 포함한다. 의도적인 split/upto 재개를 같은 궤적으로 정규화하되 CED가 다르다는 이유로 전체 덱 해시를 억지로 일치시키지 않는다.

기존 런에 실행 당시 SHA가 없으면 **미상**이다. 현재 파일을 해시하여 과거 실행 기록처럼 채우면 안 된다. 체크포인트 상태 확인은 기하 증거를 보강하지만 잃은 실행 이력을 복원하지는 않는다. run_banners는 배너를 못 찾은 로그를 결과에서 누락하므로, 실제 실행 세그먼트 목록도 별도로 닫혀 있어야 한다.

**해결 증거:** 위 두 불일치가 거부되고, 같은 운동의 정당한 재개만 통과해야 한다.

**재현 키:** review_round4_output.json → binary_mismatch_accepted, rotation_start_mismatch_accepted.

### HBR4-03 · P1 — 구간 극값은 맞지만, 허용한 형상 잔차를 구간에 넣지 않는다

**위치:** [scripts/mixer_restart_phase_test.py:333](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/mixer_restart_phase_test.py:333>), [scripts/mixer_restart_phase_test.py:363](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/mixer_restart_phase_test.py:363>), [scripts/mixer_restart_phase_test.py:385](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/mixer_restart_phase_test.py:385>), [scripts/check_contact_validity.py:427](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:427>), [scripts/check_contact_validity.py:484](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:484>), [scripts/check_contact_validity.py:786](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:786>).

생산자는 강체 회전 적합 뒤 남는 좌표 잔차를 최소 1×10⁻⁷ m까지 허용한다. 소비자는 그 잔차를 사용하지 않고, 원 STL을 예정각±각 경계로만 돌린다. **각 오차 0이 위치 오차 0은 아니다.**

**검산:** 회전 후 A/B 메시 전부를 회전축 x 방향으로 +80 nm 옮겼다. A/B는 서로 동일하다. 첫 회전 전 프레임은 원 STL 그대로다.

| 실제 함수 반환/독립 기하 계산 | 값 |
|---|---:|
| residual_max_m | 8.000000000017542×10⁻⁸ m |
| 생산자의 허용치 | 1×10⁻⁷ m |
| 영수증 passed | true |
| Back 근처 SE 반경 | 75.7 µm |
| 원 STL로 계산한 δ/r | 0.009500000000000557 = **0.950000000%** |
| 이동한 실제 입력 메시로 계산한 δ/r | 0.010556803170409511 = **1.055680317%** |
| 검사기 | **PASS · tech=[] · reject=[]** |

본 반례는 “엔진에 80 nm 변형이 관측됐다”가 아니라, **생산자가 적격으로 인정한 입력에 대해 소비자가 안전하지 않다**는 것이다.

또 각 경계를 max(실측 오차, 출력 해상도)로 두는 것은 일반적인 오차 합성의 상한이 아니다. 해상도가 전체 오차를 이미 포함한다는 증명 없이는 최악 방향의 합 또는 좌표 반올림 구간 전파가 필요하다. 첫 꼭짓점의 첫 좌표 문자열만으로 전 프레임·전 좌표의 출력 오차를 정하는 것도 완전한 오차 예산이 아니다.

**수정 최소안:** 각 오차뿐 아니라 위치/형상 적합 잔차와 출력 반올림을 부호거리의 불확실성으로 전파한다. 좌표별 최대 잔차와 거리 노름을 혼동하지 않는다. 또는 출처·시각이 증명된 실제 메시 평면을 사용하고 그 계측 오차를 전파한다. 허용치를 결과가 통과할 때까지 낮추거나 올리는 처방은 아니다.

**해결 증거:** 위 80 nm fixture가 더는 PASS하지 않고, 완전한 경계로 TECH 또는 확정 REJECT가 되어야 한다. 실제 영수증으로 오차 예산을 재발행한다.

**재현 키:** review_round4_output.json → translation_receipt, ignored_shape_residual_false_pass.

**이전 결함과 구분:** wall_interval의 끝점+내부 정지점 산술 자체는 맞다. 독립적인 100개 설정×4입자×201각도 대조에서 경계 위반은 없고 부동소수 오차 규모는 δ/r 기준 2.31×10⁻¹⁴ 이하였다. 이 격자 대조 자체를 해석적 증명의 대체물로 쓰지는 않는다.

### HBR4-04 · P2 — 삼각형 수·꼭짓점 집합 보존은 “전체 용기”의 증명이 아니다

**위치:** [scripts/check_contact_validity.py:257](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:257>), [scripts/check_contact_validity.py:537](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:537>), [scripts/check_contact_validity.py:570](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:570>).

mesh_dump_container는 삼각형 개수와 꼭짓점 집합의 양방향 최근접 거리를 본다. _planes는 퇴화 삼각형을 조용히 버린다.

**검산:** 전체 156삼각형과 원 꼭짓점 집합을 보존하면서, Front 39삼각형을 [중심, 테두리 점, 중심]으로 바꿨다. 유한 좌표이고, 드럼 면 수·예정각도 그대로다. Front 평면만 사라진다. 원래 완전한 Front에 **δ/r=2%** 겹치는 입자를 넣은 결과:

~~~text
triangles = 156; degenerate_front_triangles = 39
verdict = PASS; phase_status = mesh-dump; tech=[]; reject=[]
wall_max = -37.45910171730515  (δ/r, 남아 있는 다른 벽까지의 값)
~~~

끝판을 아예 제거한 옛 78삼각형 fixture는 이제 거부한다. 이번 반례는 그 수정이 연결 관계까지 검사하지는 않는다는 뜻이다.

**무너지는 결론:** “현재 mesh-dump 분기가 전체 용기 기하를 검증한다.” 실제 생산 STL이 이처럼 손상됐다는 주장은 아니다.

**수정 최소안:** 비퇴화·구성요소·면 연결/닫힘 및 원 삼각형의 강체 변환 대응을 검사한다. 순서 정규화를 하더라도 단순 점 구름으로 축약하지 않는다. 당장 이 대체 경로를 안전하게 닫기 어렵다면 **mesh-dump를 판정 근거로 사용하지 않도록 명시적으로 비활성화**하고, 고친 영수증 경로만 쓰는 선택도 가능하다.

**해결 증거:** 퇴화·중복 면·끝판 연결 변조가 모두 거부되고 정상적인 순서 재배열은 필요한 범위에서 통과.

**재현 키:** review_round4_output.json → degenerate_front_false_pass, old_missing_caps_closed.

### HBR4-05 · P1 — 다른 런·다른 칸 규약의 실제 판독 결과가 rest 증서로 통과

**위치:** [dem_scripts/mixer_20260921/launch_highbo.sh:194](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/dem_scripts/mixer_20260921/launch_highbo.sh:194>), [dem_scripts/mixer_20260921/launch_highbo.sh:215](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/dem_scripts/mixer_20260921/launch_highbo.sh:215>), [dem_scripts/mixer_20260921/launch_highbo.sh:220](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/dem_scripts/mixer_20260921/launch_highbo.sh:220>), [scripts/measure_mixing_index.py:352](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/measure_mixing_index.py:352>).

증서의 런은 basename만 비교한다. 봉인 뒤 mtime이면 “다른 발사의 증서가 아니다”라고 표시한다. 그러나 복사하거나 재판독해도 mtime은 새로워진다. 판독 결과에는 cells/x_cells/n_min/axis/r_container의 명시적 계약과 입력·발사 식별자가 없다.

**검산:** 실제 analyse로 foreign_results/LH_s32452843을 **2×2×1** 칸으로 판독했다. 그 결과를 launch_out/LH_s32452843의 first 봉인보다 나중에 복사한 뒤, **launch_highbo.sh의 실제 rest Python 관문**을 호출했다.

~~~text
등록 칸 = 16×16×4; 증서 생산 칸 = 2×2×1
smoke.complete=true; n=25; M_mean=0.43200000000000005
smoke.tech_smoke=[]; smoke.qc_repr.pass=true
actual gate rc=0
~~~

검사기의 출력은 “다른 발사·옛 시험의 증서가 아니다”였다. 이 주장은 성립하지 않는다. boolean을 임의로 채운 것이 아니라 실제 판독 결과를 사용했다. **나머지 LH를 실제 발사하지는 않았다.**

**무너지는 결론:** “rest가 받은 증서는 first에서 띄운 그 시드·그 판독 규약의 bin 0이다.”

**수정 최소안:** 증서에 판독기 버전/해시, 모든 규약 인자, 평가 및 E0 입력·덱·프레임 묶음 해시, launch_record 식별자/해시를 기록하고 관문에서 대조한다. 이동 가능한 데이터셋은 경로 문자열 대신 불변 식별자로 연결한다. mtime은 보조 진단으로만 둔다. 경로 전체 일치만 추가하는 것으로 입력 내용·격자 계약까지 증명되지는 않는다.

사전등록 §8은 접촉 계약, 보조 칸, step-s 검토를 사람 확인으로 따로 남겼다. 그 부분이 자동화되지 않았다는 것을 새 결함으로 세지 않는다. 여기서는 **기계가 보증한다고 출력한 증서 출처·규약**만 문제 삼는다.

**해결 증거:** 동일 basename의 다른 데이터, 다른 격자/n_min, 다른 E0, 봉인 뒤 복사된 옛 증서가 모두 거부되고 정상 first 산출물만 통과.

**재현 키:** review_round4_output.json → foreign_wrong_grid_smoke_gate.

### HBR4-06 · P2 — 목표 CED 검사가 런처의 자동 관문에서 빠졌다

**위치:** [dem_scripts/mixer_20260921/launch_highbo.sh:62](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/dem_scripts/mixer_20260921/launch_highbo.sh:62>), [dem_scripts/mixer_20260921/launch_highbo.sh:100](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/dem_scripts/mixer_20260921/launch_highbo.sh:100>). 대조: [docs/reviews/mixer_highbo_prereg_20260927.md:67](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/docs/reviews/mixer_highbo_prereg_20260927.md:67>).

사전등록은 --expect-deck를 요구한다. 런처 deckdiff는 --runs … --allow B만 호출하고, 그 약한 명령의 rc=0을 발사 기록에 적는다.

**검산:** 실제 생성 덱의 seed 및 비-CED 명령을 유지하고 LH 허용 다섯 CED 요소를 모두 두 배로 만들었다.

~~~text
예: AM_P–AM_P CED 3,563,480 → 7,126,960 J/m³  (덱에 찍힌 반올림 값)
런처와 같은 호출: 3/3 PASS, rc=0
--expect-deck 포함: 0/3 PASS, rc=1
~~~

허용된 “어디를 바꿀 수 있나” 검사가 “얼마로 바꾸기로 했나”를 대신했다.

**한정:** 사용자가 §2-2의 강한 수동 검사를 정확히 수행하면 이 반례는 잡힌다. 따라서 등록 절차 전체를 지켜도 무조건 새는 P1로 분류하지 않는다. 다만 자동 런처 관문만 믿으면 목표 LH가 아닌 덱이 통과한다.

**수정·해결 증거:** 런처에도 기대 행렬을 연결하거나, 현재 실행 덱 해시에 묶인 강한 사전 비교 증서를 요구한다. 위 변이체가 **런처 경로에서도 rc≠0**이어야 한다.

**재현 키:** review_round4_output.json → launcher_target_without_expect, launcher_target_with_expect.

### HBR4-07 · P2 — 정지 E0의 증거 경로가 빠져 정상 기준을 과잉차단

**위치:** [docs/reviews/mixer_highbo_prereg_20260927.md:89](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/docs/reviews/mixer_highbo_prereg_20260927.md:89>), [scripts/check_contact_validity.py:455](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:455>), [scripts/check_contact_validity.py:250](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/check_contact_validity.py:250>).

§2-4는 LC 3개와 E0 3개도 같은 --phase-receipt 명령 형식으로 검사하도록 한다. 같은 영수증 파일을 쓰라고 명시한 것은 아니다. 그러나 E0는 0회전이고, 원자 dump 격자도 회전 캠페인의 위상 시험과 다르며, 별도의 정적 증거 경로가 제시되지 않았다. 아래는 캠페인 영수증을 재사용하는 방법도 해결책이 아님을 보이는 반례다.

**검산:** 생성기의 실제 100,000입자·cgf=151.4 캠페인 조건을 썼다. LC 8회전 덱으로 합성 v1 영수증을 만들고 E0 0회전 덱의 정상 정지 프레임을 검사했다. 물리 계산을 돌린 것이 아니라 덱 구조·실제 소비자 인터페이스 시험이다.

~~~text
LC dump 격자 = 45,333 step
E0 planned_t0 = 385,000; 회전 fix 시작 = 385,337; 실제 회전 run 없음
원 STL 기준 E0 벽 δ/r = 0.500000000%
LC 영수증 적용 → step 385000이 A 실측 목록에 없어 TECH
영수증 없이 → 각 미식별; 가능한 범위 0.16–56.47% → TECH
~~~

**무너지는 결론:** “작성된 동일 절차로 정적 E0까지 계약을 닫을 수 있다.” 이것은 false-green이 아니라 운영상 과잉차단이다.

**수정 최소안:** E0에는 **정적 벽 경로**를 등록한다. fresh 실행이고 판정 시점 이전에 회전/다른 메시 운동이 없었음, 원 STL·실행 입력·상태의 동일성이 확보되면 각=0으로 검사한다. 재개/운동 이력이 불명확하면 실제 상태 증거가 필요하다. 이를 해결하려고 step 포함 검사나 1% 문턱을 느슨하게 해서는 안 된다.

**해결 증거:** 해당 정상 E0 fixture는 올바른 정적 증거로 PASS하고, 정적이라고 이름만 붙인 회전/재개 이력은 거부한다. 실제 E0 3개는 그 계약으로 판독한다.

**재현 키:** review_round4_output.json → E0_static_contract.

### HBR4-08 · P3 — SE 관련 “모든 쌍의 Bo_code 고정”이라는 표현은 아직 모호하다

**위치:** [docs/mixer_devlog/v09_20260927.md:11](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/docs/mixer_devlog/v09_20260927.md:11>), [docs/mixer_devlog/v09_20260927.md:19](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/docs/mixer_devlog/v09_20260927.md:19>), [scripts/make_mixer_deck.py:374](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/scripts/make_mixer_deck.py:374>). 이미 더 정확한 표현은 [docs/reviews/mixer_highbo_prereg_20260927.md:61](<C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/mixer_highbo_round4_evidence_20260928/docs/reviews/mixer_highbo_prereg_20260927.md:61>)에 있다.

동일 CED=10,458.232423831554 J/m³를 실제 혼합쌍 E*·R*로 다시 계산하고 작은 SE의 무게로 정규화하면:

| 쌍 | 무차원 평형 Bo_eq |
|---|---:|
| AM_P–SE | 0.17551240960668482 |
| AM_S–SE | 0.13867647178799788 |
| SE–SE | 0.2124400000000001 |

따라서 코드의 명목 Bo 입력을 “각 혼합쌍의 같은 Bo”처럼 쓰면 안 된다. **“SE–SE 목표 Bo_code=0.21244; SE 관련 CED 행렬 요소 고정”**으로 통일하면 된다. Bo_code를 명목 노브라고 명시하는 것은 가능하다. 이 문서 문제만으로 HOLD를 내리지는 않는다. PNG 확인은 별도 남긴다.

**재현 키:** review_round4_output.json → SE_pair_Bo_label.

## 3. Q1~Q5 — 설계 판단

### Q1. 0입자 위상 영수증의 논리와 이식 충분성

**물리 전제에는 조건부 동의, 현 소비자 검사의 충분성에는 반대.**

move/mesh rotate는 처방된 축·주기를 따르는 운동이다. 입자 힘 때문에 그 처방 궤적 자체가 바뀌는 종류의 운동이 아니므로, **입자가 없다는 이유만으로 위상 시험을 배척할 필요는 없다.** 공식 문서도 처방 운동, 복합 운동의 순서 의존성, 올바른 fix 설정을 통한 재개 연속성을 설명한다. [LIGGGHTS move/mesh 문서](https://www.cfdem.com/media/DEM/docu/fix_move_mesh.html)

하지만 다음 사슬이 모두 필요하다.

1. 동일 실행 바이너리와 관련 실행 환경.
2. 동일 원 메시·좌표계·scale 및 순서가 있는 운동 계약.
3. 동일 회전 시계와 초기/재개 mover 상태.
4. 판정 step에 대한 완전하고 유한한 기하 계측.
5. 각·좌표 출력 해상도·형상 잔차를 모두 포함한 거리 오차 경계.
6. 그 증거와 판정할 런의 연결.

현재 HBR4-01/02/03이 1·3·4·5·6을 끊는다. 작은 각 경계를 **실측했다는 이유만으로** 이 사슬을 건너뛸 수 없다. 반대로 ±0.05°를 모든 런에 무조건 부여하라는 요구도 아니다. 더 작은 경계가 유효하려면 그것을 떠받치는 계약을 완성하면 된다.

### Q2. 하한 max_i min_θ를 받아들일 것인가

**동의. 지금 더 조일 필요는 없다.**

각 입자·평면의 겹침을 g_i(θ)라 쓰면:

~~~text
max_i min_θ g_i(θ) ≤ min_θ max_i g_i(θ)
~~~

왼쪽이 1%를 넘을 때만 REJECT하는 것은 안전하다. 느슨함은 일부 확정 위반을 TECH로 남길 뿐, PASS를 만들지 않는다. PASS에는 별도로 전 구간 상한을 쓰므로 현재 분리도 맞다.

향후 더 조이는 알고리즘을 쓰더라도 결과값에 맞춰 선택하지 말고 고정된 방법으로 등록하면 된다. **이번 해제조건에 minimax 정밀 최적화를 추가하지 않는다.** 다만 구간 밖 오차 누락은 이 부등식으로 해결되지 않는다(HBR4-03).

### Q3. 예정각과 모순되는 실제 mesh 덤프

**현재 출처 불명 상태에서는 TECH에 동의. 출처가 독립 증명되면 실제 덤프 우선이라는 수정안.**

다른 런/시점 파일과 구분할 근거가 없으면 “이 덤프로는 독립 기하를 확정할 수 없다”가 맞다. 옛 시험의 기대를 REJECT에서 TECH로 바꾼 것 자체는 완화가 아니다. 둘 다 PASS를 막으며, 서로 다른 실패 의미를 보존한다.

그러나 해시·런 식별·step·전체 기하·실행 이력으로 그 덤프가 실제 상태임이 증명되면, 예정각과 다르다는 이유로 참 기하를 버리면 안 된다. **실제 기하로 겹침을 평가하고 예정 운동 계약 위반을 별도로 기록**해야 한다. 먼저 HBR4-04의 “전체 기하” 판정을 고치거나 그 경로를 닫아야 한다.

### Q4. 격자 밖·중복·형식 실패 프레임을 제외하고 tech에 기록

**동의 — 소비자가 tech와 완전성도 읽는다는 조건.**

이번 실제 호출에서 옛 평균 오염이 닫혔다. 격자 밖 한 장 추가 후 M_final=0.45 유지, tech 발생. 중복/스키마 실패는 최종 bin을 24/25로 만들어 M_final=null이다.

“값 보고 / 판정 적격 / A 발동”의 세 층 구분도 타당하다. 기술값이 남는 것과 판정 가능은 다르다. planned.M_final이 숫자라는 이유만으로 적격으로 읽지 않는다. 현재 사전등록 §2-3은 tech==[]와 접촉 계약·QC를 추가한다. 단, **다른 데이터·다른 칸 규약을 섞지 않는 증명**까지 이 프레임 제외 규칙이 제공하지는 않는다(HBR4-05).

### Q5. 기존 런별 상태 확인과 새 LH의 필요 증거

**두 층을 모두 요구하는 데 동의. 새 LH의 “봉인+v1이면 충분”은 수정 후 조건부 동의.**

- v1은 **해당 실행파일/운동 규약의 재개 동작**을 시험한다.
- 기존 L/LC 체크포인트 확인은 **그 런의 저장된 실제 메시/mover 상태**를 시험한다.

서로 다른 질문이므로 하나로 다른 하나를 대신할 수 없다. 공식 read_restart 문서도 fix 상태 재현 조건과 일부 granular 경로의 비정확 재시작 가능성을 구분한다. 여기서 필요한 것은 입자 궤적 전체의 비트 동일성 증명이 아니라, 판정에 쓰는 메시 상태와 처방 운동의 재현이다. [LIGGGHTS read_restart 문서](https://www.cfdem.com/media/DEM/docu/read_restart.html)

기존 런은 보존 체크포인트 **복사본**과 실제 in.resume, 실제 fix ID/순서, 실행 바이너리를 별도 검증 폴더에서 봉인하여, 원 step과 짧은 후속 step의 **전체 메시**를 비교하는 설계가 타당하다. 각뿐 아니라 위치/형상 잔차와 출력 오차를 거리 경계에 포함해야 한다. 이것을 이번 리뷰에서 실행하지 않았다.

그 검사는 **확인한 재개 구간의 상태**를 증명한다. 없어졌던 과거 실행파일 해시나 미보존 재개 이력을 증명하지 않는다. 불명인 이력은 불명으로 남긴다.

새 LH는 HBR4-01/02/03을 고친 v1, 동일 실행파일·운동 시계의 발사 봉인, 입력/출력 계보가 있다면 처음부터 과거 런의 잃은 이력 문제를 가질 필요가 없다. **그 뒤 재개하면 해당 재개 상태도 기록·검사**해야 한다. rest에는 HBR4-05의 올바른 스모크 증서가 필요하다. 정지 E0는 HBR4-07의 별도 정적 계약을 사용한다.

이 권고는 기존 캠페인을 통째로 다시 돌리라는 뜻이 아니다.

## 4. 시험 결과와 증거의 경계

| 실행한 자체 시험 | 결과 |
|---|---:|
| measure_bed_aspect | 25/25, rc=0 |
| check_contact_validity | 55/55, rc=0 |
| measure_mixing_index | 32/32, rc=0; 선택적 실물 덱 시험 ⑪은 SKIP |
| mixer_deck_diff | 24/24, rc=0 |
| mixer_restart_phase_test | 20/20, rc=0 |
| make_mixer_deck | 89/89, rc=0 |

독립 프로브의 검증 assert 14개도 모두 충족했다. 여기서 성공은 **정상 대조군, 기존 결함의 거부, 새 결함의 재현**이 각자의 기대와 맞았다는 뜻이지 “생산 코드 무결함”이 아니다.

launch_highbo.sh/run_all.sh/test_launcher.sh Bash 구문 검사 통과. 전체 check_all 및 test_launcher 실행 성공은 주장하지 않는다. 합성 fixture는 실데이터의 최대 겹침·상별 유지 부피·M 효과 크기를 추정하지 않는다.

증거 묶음:

- sources.json: 고정 스냅샷과 파일별 Git blob 식별자.
- run_selftests.py / selftests_output.json: 실행한 여섯 시험의 원문 stdout·stderr·종료 코드.
- review_round4_probe.py / review_round4_output.json: 독립 반례 및 실제 함수 반환.
- scripts, dem_scripts, docs: 해당 핀의 관련 원본 18개.
- README.md: 안전 범위와 재현 방법.

## 5. 런 전에 닫을 최소 목록

1. **영수증 무결성:** A/B finite, 필수 파일·덤프 해시 목록의 완전성(HBR4-01).
2. **이식 전제:** 실행 당시 바이너리 및 운동 시계/상태를 판정 런에 연결(HBR4-02). 기존 L/LC 상태 확인은 요청서 Q5대로 별도 증거.
3. **오차 경계:** 각뿐 아니라 형상 잔차·출력 오차를 거리 판정에 전파(HBR4-03).
4. **대체 기하 경로:** 면 연결까지 검증하거나 현 mesh-dump 판정 분기를 명시적으로 비활성화(HBR4-04).
5. **발사 관문:** 스모크의 실제 데이터·규약·발사 식별자 연결, 기대 CED 검사를 런처에도 연결(HBR4-05/06).
6. **정적 기준:** E0의 정적 벽 계약을 별도로 정하고 실제 기준 3개에 적용(HBR4-07).
7. 문서는 SE–SE 명목 Bo와 혼합쌍 CED 고정을 구분하고, v09 그림 라벨 확인을 남기지 않는다(HBR4-08).

문턱 1%, Bo, seed, LC, 칸 규약을 결과에 맞춰 바꾸라는 요구는 없다. **수정된 검사기의 실제 런 적용이 기술적으로 가능하고 출처가 이어지는지**를 닫으라는 요구다.

다음 회신은 각 항목의 수정 diff와 위 반례가 새 코드에서 거부되는 원문, 정상 대조군, 고정된 실측 영수증/출처 연결을 주면 된다. 이미 닫힌 HBR3-05/06/07을 다시 전면 재심할 필요는 없다.

HOLD
