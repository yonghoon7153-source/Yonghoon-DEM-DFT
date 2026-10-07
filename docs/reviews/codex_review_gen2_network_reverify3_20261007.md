# 접촉망 세대 2 재검증 3 — 기존 반례 차단, 배포·관측 관문 두 곳은 부분

작성: 2026-10-07 KST  
대상: `claude/stoic-knuth-NObVQ` · **`0801d4ceb540f5a5813761b20a5e0f304ed80a03`**  
요청: `codex_gen2_network_reverify3_request_20261007.md` Q1–Q5 · 갱신된 194 실행 등록  
범위: 수정 검증 · **194 발사 GO를 요청하지 않은 라운드**. 생산 코드·원장·git 상태는 변경하지 않았다.

## 0. 결론

**원래 G2RR2-01~05 반례는 수정된 경로에서 차단됐다. 이번 검증 범위에서 새 P1은 발견하지 않았다.**

다만 두 주장을 끝까지 승인할 수 없다.

1. **G2RR3-01 / P2:** “v1.3 생성기는 production194 전체를 다시 읽은 성공 기록만 받는다”는 거짓이다. 기록 부재·손상·null은 경고만 하고, 실패한 봉인 감사 내용은 판정하지 않는다. 실제 배포 생성 함수와 자체 검산에 이를 통과시켰다.
2. **G2RR3-02 / P2:** “관측 로그가 있으므로 실제 import를 봉인과 대조했다”는 충분하지 않다. **빈 로그 하나 → 관측 모듈 0개 → audit rc 0**이다. 일부 프로세스의 로그 소실도 검출하지 못한다.

숫자 결합·개별 실패 보존 수정은 지지한다. 그러나 **새 194 발사 / v1.3 인계 HOLD 유지**다. 이는 수치 교정을 철회한다는 뜻이 아니다. 새 관문 결손, 미실행 WSL 사전 점검, 별도 저자 발사 승인이 남아 있다. **S3 실행도 별도 HOLD**다.

### 기존 항목별 닫힘

| 항목 | 판정 | 실제로 닫힌 범위 / 남은 범위 |
|---|---|---|
| G2RR2-01 | **닫힘** | 원자료 지문 삭제·null, 세대 선언 동시 삭제 우회 차단. 역사 형식은 등록과 명시 모드로 구분. 전면적으로 일관된 위조를 잡는다는 뜻은 아님 |
| G2RR2-02 | **다시 읽기 자체 닫힘 / 인계 종단 부분** | 0건·빈 계획 PASS 차단. 하지만 그 검산 기록을 없애거나 망가뜨리면 v1.3 배포 관문이 건너뜀 → G2RR3-01 |
| G2RR2-03 | **발견된 의존성 누락 닫힘 / 관측 보증 부분** | fracture_model 변이는 이제 봉인 지문을 바꿈. 32파일·정적 분류 재계산 일치. 관측 로그 완전성은 보장하지 않음 → G2RR3-02 |
| G2RR2-04 | **닫힘** | CF 증서 σ₀와 차원값의 동시 ×2, FULL 증서 σ₀ ×2 차단. 정상 온도 입력은 통과 |
| G2RR2-05 | **닫힘** | 진단 상태 기록 결손 차단. 진짜 CF 풀이 실패는 FULL을 살리면서 해당 가지를 빈칸+사유로 유지 |
| S3 의존성 목록 보완 | **코드 범위 닫힘** | 여섯 파일 및 소비자 닫힘 검사 지지. Git 원형 selftest 완주·새 S3 실행 봉인·실행 승인은 아님 |

## 1. 검증 범위와 증거의 강도

- 요청서가 들어간 커밋을 고정했다. 확보한 **432개 파일 각각의 Git blob SHA-1·SHA-256·바이트 수**를 대조했고, 탐침 뒤에도 원본 사본은 일치했다.
- 첨부 두 문서는 이 커밋의 대응 문서와 일치한다(줄바꿈·끝 개행 차이만 정규화). 별도 브랜치 끝의 파일을 섞지 않았다.
- Windows / Python 3.12.14, 최종 재현 환경 NumPy 2.5.3, SciPy 1.16.3. 의존성은 리뷰 폴더에만 설치했다. 초기 시험 뒤 배포 그림 의존성 설치로 NumPy 선택 경로가 바뀐 것을 환경 대조에서 발견하여, 핵심 탐침과 관련 회귀를 최종 환경에서 다시 실행했다.
- 검증은 실제 함수·실제 audit/reread CLI·합성 침대·격리된 배포 픽스처로 수행했다. **194 생산 배치, WSL 실침대 파이프라인, 등록 S3 코호트는 실행하지 않았다.**
- 원래 탐침은 가능한 그대로 다시 사용했다. `seal_paths.py`는 정상 대조군이 새 v3 형식을 갖추도록 고치고, 새 필수 `--expect-case`를 지정했다. 그렇지 않으면 대조군부터 거부되어 수정 효과를 분리할 수 없다.
- `release_gate.py`는 **상위 τ 재독해만 대역**으로 고정했다. 정상·변이 모두 같은 대역이다. 배포 관문·생성·자체 검산은 원본 함수다. 그러므로 이 증거는 **배포 관문 결함**이지 “실제 194의 모든 관문을 우회했다”는 증거가 아니다.
- S3 Git 대조의 독립 탐침은 .git 없는 사본에서, 이미 대조한 고정 커밋 파일 해시를 Git 읽기 어댑터에 주었다. **실제 Git subprocess 경로 완주로 세지 않았다.**
- `evidence/verification.json`의 **22/22**는 “원본 바이트와 이 리뷰의 관측 결과가 일치함”이다. **제품 시험 전부 PASS, 생산 GO를 뜻하지 않는다.**

재현은 이 묶음 루트에서 아래처럼 한다. 환경 설명은 README 참조.

```bash
python run_probes.py acceptance branch_policy dependency_gap input_digest
python run_probes.py seal_paths
python run_probes.py new_gates release_gate scope_checks
python verify_evidence.py
```

## 2. Q1 — 필수 선언과 역사 등록: 동의, 원 반례 닫힘

근거: [scripts/run_network_194_parallel.py:565](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/run_network_194_parallel.py:565)의 `launch_eligibility`, 같은 파일의 run/retry/audit/merge 소비 지점.

정상 1케이스 게시 산출물로 실제 audit CLI를 호출했다.

| 입력 변화 | rc |
|---|---:|
| 정상 v3 대조군 | 0 |
| 원자료 SHA만 변경 | 1 |
| 원자료 SHA 변경 + input_digest 삭제 | 2 |
| 원자료 SHA 변경 + input_digest=null | 2 |
| 옛 레코드를 g2라고 선언 | 1 |
| 옛 레코드 + 기대 세대 두 선언 삭제 | 2 |

추가로 상위 필수 필드 10개를 각각 삭제/null로 바꿨다. **20/20 invalid**다. 세대 관문도 새 선언 결손을 거부했다. retry 생산 워커는 실행하지 않았다.

커밋된 역사 manifest는 기본 audit에서 rc 2, `--historical`에서 rc 0이다. 역사 git 신원·코드 해시 변경, 새 형식 표지 삽입은 invalid로 바뀐다.

**한정:** 역사 CLI 시험은 해당 manifest를 격리 ROOT에 놓은 형식 수용 시험이다. 그곳에는 194 생산 산출물이 없어 **NO_RECORD 194**다. 이를 “옛 194 수치 재검산 PASS”로 쓰면 안 된다. 이번 검증은 역사 신원의 명시적 취급과 삭제 우회 차단을 지지하며, 194 v1.2 숫자 전수를 재검증한 것은 아니다.

증거: `evidence/seal_paths.json`, `evidence/scope_checks.json`.

## 3. Q2 — 등록 집합과 다시 읽기: 본체 동의, 배포까지는 불충분

근거: [scripts/g2_network_reread.py:267](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/g2_network_reread.py:267)의 루프 전 계획 검사, [scripts/g2_network_reread.py:335](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/g2_network_reread.py:335)의 루프 밖 집합 대조, [scripts/g2_network_reread.py:376](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/g2_network_reread.py:376)의 CLI 등록 요구.

독립 CLI 결과:

| 입력 | 읽은 케이스 | n_fail | rc |
|---|---:|---:|---:|
| 등록한 1케이스 대조군 | 1 | 0 | 0 |
| plan 삭제 | 0 | 2 | 1 |
| cohorts=[] / queue 유지 | 0 | 2 | 1 |
| cohorts 삭제 / queue 유지 | 0 | 2 | 1 |

자체 시험도 **15/15** 통과했다. pilot3와 합성 production194 양성, 등록 모드 부재, 코호트·케이스 누락/중복, symlink 불가 환경의 사본 대체를 포함한다. 합성194는 194개의 독립 실데이터가 아니라 **한 게시 픽스처를 등록 ID에 연결한 것**이다.

### G2RR3-01 — P2 · 배포 관문은 결손/손상 검산과 실패 감사를 통과시킨다

**무너지는 결론:** 요청서 §1·§4와 실행 등록 §3b의 “v1.3 생성기는 완전한 production194 성공 기록만 받는다.”

**위치**

- [scripts/lhs_release_build.py:1109](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/lhs_release_build.py:1109): `seal_audit.json`은 해시만 적고 판정 내용은 읽지 않는다.
- [scripts/lhs_release_build.py:1140](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/lhs_release_build.py:1140): reread가 없으면 경고, JSON 손상/필수 판정 필드 타입 결손도 경고다. 제대로 읽히는 실패 기록만 예외를 낸다.
- [scripts/lhs_release_build.py:1643](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/lhs_release_build.py:1643): 실제 build가 그 경고를 수집하고 계속한다.
- [scripts/lhs_release_build.py:1897](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/lhs_release_build.py:1897): `check_v13`도 읽을 수 있는 정수 n_fail을 가진 dict에만 검사를 적용한다.

**검산**

`v13_batch_gate_check` 직접 호출에 이어 **실제 build_v13 → check_v13**로 대조했다.

| 입력 증거 | 실제 배포 생성 | check_v13 |
|---|---|---|
| 정상 reread·감사 | 생성 | 문제 0 |
| 명시 n_fail=1 | **거부** | 생성 안 함 |
| reread 파일 없음 | **생성** | **문제 0** |
| reread가 깨진 JSON `{` | **생성** | **문제 0** |
| reread={} | **생성** | **문제 0** |
| n_fail=null | **생성** | **문제 0** |
| 정상 reread + 감사 refused=true / eligibility=invalid | **생성** | **문제 0** |
| 정상 reread + 감사 UNSEALED=194 / generation_problems | **생성** | **문제 0** |

생성된 묶음은 각 21파일이다. 따라서 이 결함은 “헤더 문구만 부정확함”이 아니라 **기록을 못 읽으면 더 적게 검사하는 실행 분기**다.

**한정:** 상위 τ 재독해 대역과 저자 시험의 합성194 인계표를 썼다. 실제 원자료부터 끝까지 잘못된 값을 인계한 실증은 아니다. 원래 인계 P0–P4의 값/도장 검사가 무력하다는 판정도 아니다. 그래도 **해당 관문의 완전 검산 보증은 독립적으로 반증**된다.

**최소 해결 증거**

1. 실제 배포에서는 감사·검산 증거 부재/손상/타입 결손을 거부. 예전 도구 기록이 필요하면 **명시적인 비배포 진단 모드**로 분리.
2. 감사는 해시뿐 아니라 current 자격, 실제 실패 predicate(UNSEALED·merged 불일치·generation/input/import 문제), 요청한 등록 집합·실행 신원을 대조. 정직한 실패행 처리는 기존 등록 정책과 함께 명시하고, 별도 숫자 허용치나 무조건적인 “모든 σ 양수” 조건을 만들지 않는다.
3. reread는 성공·g2·production194·고유 집합 완전성뿐 아니라 **이번 ROOT/봉인에 대한 증거**인지 결합.
4. build와 check 양쪽에서 같은 관문을 사용. 위 6개 실패 증거 변이체는 전부 거부하고 정상 대조는 생성되어야 한다.

재현: `python run_probes.py new_gates release_gate`  
증거: `evidence/new_gates.json`, `evidence/release_gate.json`, 각 변이체의 `build.log`와 실제 출력 폴더. 새 P1로 올리지 않은 이유는 **수치 솔버 오답이 아니라 제출 관문의 증거 수용 결함**이기 때문이다.

## 4. Q3 — 32파일 봉인 지지; 실제 import 관측은 아직 충분하지 않다

독립 재계산:

- CODE_FILES = **32**, 정적 전이 닫힘 = **30**, 지연 import 조사 = **90**, 분류 밖 = **0**.
- code_fp = `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`.
- 등록194 ID 지문 = `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf`.
- 원자료 해시 **표** 지문 = `da7c93f9a0887145ff171e381c8608cb79779d96aea5a595a25677dc361ef784`.
- lhs=130 / lhsx=64. 이 원자료 지문 대조는 커밋된 수확 메타데이터에서 계산한 것으로, **WSL의 원덤프 바이트를 새로 읽은 것이 아니다.**

이전 반례를 실제 `dem_analysis_core.calc_fracture_stages`에 재적용했다. 리뷰어 사본의 K_IC_AM_P를 **0.3 → 30 MPa·m^0.5**로 바꾸면 multicrack=100→0%, intact=0→100%로 바뀌며, 이번에는 **code_fp도 e8b2496b… → 2241d046…로 바뀐다**. 발견됐던 누락은 닫혔다.

`lhs_union_webapp`과 `ml_design_structure` 추가도 지지한다. 하지만 정적 분류표는 실행되지 않는다고 분류한 경로가 실제로 안 열린다는 독립 실측이 아니다. **WSL 시범 관측을 발사 전 필수 증거로 두는 데 동의**한다.

### G2RR3-02 — P2 · 빈/부분 import 로그가 관측 성공으로 계산된다

**무너지는 결론:** 관측 기록 파일이 존재한다는 것만으로 워커·단계 하위 프로세스의 실제 의존성 조사가 완결됐다는 보증.

**위치**

- [scripts/run_network_194_parallel.py:228](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/run_network_194_parallel.py:228): 종료 훅에서 로그를 쓰며 예외를 삼킨다.
- [scripts/run_network_194_parallel.py:263](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/run_network_194_parallel.py:263): 로그 파일 개수를 n_processes로 센다. 빈 파일도 1개, 리포 밖·해석되지 않는 줄도 관측 집합에 기여하지 않는다.
- [scripts/run_network_194_parallel.py:2121](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/run_network_194_parallel.py:2121): “관측 켰는데 파일 0개” 또는 “실제로 보인 봉인 밖 모듈”만 거부한다.

**검산 — 정상 완료 1케이스를 둔 합성 ROOT의 실제 audit CLI**

| import 로그 | 관측 모듈 | rc |
|---|---:|---:|
| 파일 없음 | 0 | 1 |
| **빈 1000.txt 하나** | **0** | **0** |
| 무효/리포 밖 문자열 한 줄 | 0 | 0 |
| network_conductivity + 별도 로그의 봉인 밖 coating_presets | 2 | 1 |
| 같은 구성에서 두 번째 프로세스 로그만 없음 | 1 | 0 |

마지막 두 줄은 **부분 로그 소실에 대한 합성 대조**다. 실제 WSL에서 프로세스 로그가 소실됐다는 주장은 아니다. 빈 로그 반례는 실제 audit 함수·CLI의 결과이고, 빈 집합도 봉인의 부분집합이라는 산술만 통과한다.

**최소 해결 증거**

1. 완료 케이스/시도/단계와 관측 프로세스 시작·종료 영수증을 결합. 기대되는 로그가 빠졌는지 판단할 근거가 필요하다.
2. 로그가 유효하게 끝까지 기록됐는지 검사. 원자적 최종화·실행 신원·필수 핵심 모듈 관측 등을 명시. 단순히 `len(observed)>0`만 더하면 마지막 반례는 남는다.
3. 완료된 망 경로에서 빈/무효 로그, 필수 단계 로그 누락을 실제 audit 호출로 거부하는 회귀를 추가.
4. 정상 비관통·관통을 포함하는 WSL pilot3에서 관측 영수증과 audit 결과를 제출. 관측되지 않은 lazy 경로는 “분류됨/미관측”으로 구분.
5. 194 본 실행에서도 관측을 켜는 것을 권고한다. 시범의 경로 범위가 모든 194 입력 조건을 덮는다는 증거는 아직 없다.

재현: `python run_probes.py seal_paths new_gates`  
증거: `evidence/new_gates.json`, `evidence/new_gates/*/audit.json` 및 원 로그.

**한정:** 이 반례만으로 새로 누락된 생산 모듈이나 틀린 σ를 발견했다고 주장하지 않는다. 32파일 수치 교정은 유지하고, **실행 관측을 안전장치로 내세우는 부분만 부분 판정**한다.

## 5. Q4 — σ₀ 결합·기록 결손 정책: 동의

근거: [scripts/tau_flux.py:658](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/tau_flux.py:658) `branch_table_problems`, [scripts/tau_flux.py:708](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/tau_flux.py:708) `sigma0_binding_problems`.

### 5-1. 실제 생산 → 게시 → 소비 대조

이전 `branch_policy.py`를 그대로 실행했다.

- 정상 FULL q = **0.00400538**, CF = **0.117810 mS/cm**.
- CF 증서 σ₀ ×2 + 차원값 ×2: **게시 failed**.
- FULL 증서 σ₀ ×2: **게시 failed**.
- CF 진단 다섯 필드 삭제: **게시 failed**.
- H0 이온 CF만 SciPy 예외: **CF not_computed / solve_failed**, FULL q는 정상값 그대로.
- H0 이온 CF의 모든 시도 증서 실패: **CF not_computed / current_conservation_failed**, FULL q는 그대로.
- 위 두 정직한 실패는 게시 done, 인계·다시 읽기 통과. physics/H12 CF도 유지.

탐침 결과의 `handover=True`만 오독하지 말 것: 게시 실패 변이체에서 인계가 **실패행 빈칸**을 받아들이는 것과, 오염된 숫자를 받는 것은 다르다. 저자 강제-폴더 회귀도 따로 실행했으며 변조 레코드의 P4 거부를 재현했다.

### 5-2. 정확 일치와 상대 1e-12의 역할

- 증서 σ₀와 부모 σ₀는 같은 풀이의 같은 값이므로 **정확 일치** 정책에 이의 없다. 독립 측정값의 물리 오차 허용치가 아니다.
- 부모 σ₀를 온도·활성화에너지 규약에서 다시 계산하는 쪽의 **상대 1e-12**도 현재 double 계산 경로의 구현 대조로 합리적이다. 실험적 정확도를 주장하는 숫자로 쓰지 말 것.
- 전자·열에는 각각의 채널 기준을 적용해야 한다. 이온 σ₀를 일괄 적용하지 않는 현재 수정과 정상 대조를 지지한다.

추가 생산자 합성 사슬 대조 **8조건**: T 미지정·−40·0·25·60·120 °C 및 60 °C에서 E_a=0.29/0.46 eV. 모두 계약 문제 0. H0 q는 **0.00136157**로 동일했다. 기본 E_a에서 60 °C σ₀는 **0.014355301874382767 S/cm**로 증서·부모·온도 규약이 맞았다.

이는 시험한 범위의 과잉차단 반례를 찾지 못했다는 뜻이지, 모든 온도/입력 범위를 인증한 것은 아니다. 예외·비수렴은 숫자 없이 상태+사유로 남기고, 기록 자체 결손을 그 실패로 자동 보정하지 않는 구분을 유지해야 한다.

증거: `evidence/branch_policy.json`, `scope_checks.json`, publication **32/32**, role **44/44** 로그.

## 6. Q5 — S3 여섯 파일 목록: 동의, 실행 봉인은 별개

`se_material`을 넣는 데 동의한다. 약분될 것이라는 예상은 **실제로 import되어 계산 규약을 정하는 코드 신원을 생략할 근거가 아니다**. 공통 상수 배율이 취소되는 특정 조건과 모든 분기·기본값·채널에서 무관함은 다른 주장이다.

근거: [scripts/seal_s3_prerun.py:125](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/seal_s3_prerun.py:125)의 소비자 기반 닫힘, [scripts/seal_s3_prerun.py:251](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/seal_s3_prerun.py:251)의 커밋 바이트 대조, [scripts/run_s3_psi.py:245](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/source/scripts/run_s3_psi.py:245)의 소비 검사.

독립 탐침:

| 번들 | 소비 결과 |
|---|---|
| 정상 여섯 파일 | 수용 |
| 옛 네 파일 | 거부 |
| lens_geometry 해시만 틀림 | 거부 |
| se_material 해시만 틀림 | 거부 |
| git_sha 없음 | 거부 |

위 검사는 앞서 밝힌 **고정 Git 바이트 어댑터** 조건이다. 별도로 합성 6입자 원자료의 `run_case`에서 세 채널 경로가 동작함도 봤다. **등록 S3 결과가 아니며 합성 변화율을 과학적 효과 크기로 인용하지 않는다.**

실행 전 남은 것:

1. 닫힌 봉인 창을 어떻게 처리할지 **저자 결정과 이력**. 코드가 고쳐졌다고 기존 cutoff·baseline·후보 선별을 다시 고를 권한이 생기지 않는다.
2. 그 결정에 맞는 실제 Git 체크아웃의 새 번들 발행·소비 시험. 옛 네 파일 번들을 암묵 갱신하지 않는다.
3. 실제 S3 코호트·baseline 신원·원자료·실행 코드·출력 디렉터리의 새 봉인.
4. 양성/음성 회귀 및 기존 baseline 보존 검사를 원 환경에서 통과한 뒤 별도 실행 승인.

이번 리뷰는 S3 승인이나 봉인 창 소급 해제가 아니다.

## 7. 실행한 시험과 못 한 시험

독립 원형 시험에서 성공한 주요 항목:

| 시험 | 결과 |
|---|---:|
| test_gen2_publication_handover | 32/32 |
| test_gen2_role_contract | 44/44 |
| g2_network_reread --selftest | 15/15 |
| test_pipeline_provenance | 284/284 |
| test_network_handover_chain | 19/19 |
| test_tau_flux | 55/55 |
| test_tau_handover_status | 41/41 |
| test_reread_v12 | 22/22 |
| test_gen2_stamp_record / test_psi_generation_stamp | 24/24 · 18/18 |
| test_network_generation2 | 18/18 |
| test_network_solve_certificate | 23/23 + Git 비교 4 SKIP |
| test_network_boundary_rule | 10/10 + Git 비교 1 SKIP |

**전수 초록이라고 쓰지 않는다.**

- `test_lhs_release_v13`: 최종 **78 PASS / 2 FAIL**. V10a는 POSIX 문자열과 Windows 경로 구분자 차이, V16a는 .git 없는 사본에서 HEAD 부재다. 이번 P2 둘은 이 두 실패와 별개의 독립 실행 반례다.
- S3 두 원형 selftest 전체: Git 이력 부재 및 격리 `-I` 자식의 NumPy 환경 문제 등으로 완주 PASS를 입증하지 못했다. 신규 닫힘·번들 거부는 §6에서 별도로 검증했다.
- `lhs_design_dataset` 전체, grade/label 관련 전체 시험: 사본에 없는 이전 코퍼스·파일·도구 때문에 완주하지 못했다. 이 실패를 제품 신규 finding으로 세지 않았다.
- 실행기 전체 POSIX/실파이프라인 selftest 82/82, WSL 원형 5침대, pilot3, `check_all.sh`: 이번 환경에서 전수 재현했다고 주장하지 않는다.
- 로그는 성공뿐 아니라 환경 실패·SKIP도 묶음에 보존했다.

## 8. 다음 순서 — 최소 목록

1. G2RR3-01: 배포 증거의 결손/실패 거부를 실제 build/check 호출 회귀로 고정.
2. G2RR3-02: import 관측의 **완전성**과 관측 집합 포함 관계를 분리하고, 누락 로그를 실제 audit에서 거부.
3. 수정된 도구·관련 봉인 지문을 갱신하고 요청서/등록의 코드 신원을 맞출 것. 등록 §3의 옛 “27⊆29” 설명 등은 역사 문단임을 분명히 할 것.
4. 예정된 WSL real14·case15·LHS 셋의 생산→게시→인계 재독해, pilot3, 원자료 바이트·메시 대조, import 관측을 수행하고 **원 프로세스 rc와 전체 로그** 제출. 출력 tail/grep만 성공 증거로 세지 않는다.
5. 검토와 저자 발사 승인 뒤 194. 결과 전수 감사·등록 집합 재독해·배포 관문이 통과한 뒤 v1.3.
6. S3는 §6의 별도 결정·봉인·승인 경로 유지.

**최종: 수정 방향 지지 / 원래 반례 차단 확인 / 새 P2 2건 / 194 발사·v1.3 인계 HOLD 유지 / S3 별도 HOLD.**
