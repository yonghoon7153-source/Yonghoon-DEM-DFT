# Part B 독립 재검증 메모 — 조인 v6

검토 대상 코드: `5dc6f7f0b91fd9db39ab595f6b8c79a8f0d2f3b5` 제출 ZIP의 `scripts/rint_iface_join.py` · `scripts/test_rint_g2_join.py`. 작성 2026-10-21. 생산 코드를 수정하지 않았고 DEM/MPM/194 배치를 실행하지 않았다.

## 0. 실행 출처 — 전체 핀 대조·재실행 완료

처음에는 이전 고정 핀 `2b9efa253edbf455c2e1abfef1d60e51818e01f8`의 보존 사본에 이번 ZIP `scripts/*.py`를 별도 검토 디렉터리로 덮은 **명시적 검토 overlay**로 실행했다. 이후 메인 검토가 취득한 전체 핀 `source/`의 AGENTS를 읽고, 실제 import 모듈 13개·현재 시험 1개·원자료/픽스처 7개 = **21/21 SHA256 동일**을 확인했다 (`evidence/fullpin_overlay_match.json`). 원본 ZIP·이전 스냅샷·현재 source는 변경하지 않았다.

전체 핀 `source/`에서 현재 시험 원문·LF 시험 작성기 어댑트판·과거 탐침 넷·독립 62건·wd-only/underflow 탐침·추가 selftest 셋을 다시 실행했고 결과는 동일했다. 초기 overlay 결과는 `preliminary_overlay_evidence/`에 별도 보존했고 최종 로그 이름은 `*_rint2_carbon_design_review_20261021_*`이다. 옛 모듈 비교 179/324·옛 시험 138/138·주변 228 시험은 바이트 동일성이 증명된 overlay에서 실행한 결과임을 구분한다.

- 현재 join SHA256: `c52c3dd0a23af2adce30ad59736ddbd9bc3e174bc5a7edb1237490cfaaaed1b9`.
- 정상 원자료: 현재 핀의 real14/case15 원 gz·scaffold. 이전 보존 사본과 바이트 동일; 파일별 해시는 `evidence/independent_join_checks.json`.
- 현재 시험이 요구하는 `LOOSE_am_scaffold.csv` SHA256 `7ded87d867bb77bb776dff1df8ec1f21ece0204e24d43c460eef6f3ccad3f007`; 초기 overlay에 쓴 이전 사본과 현재 핀 파일이 동일함을 확인.
- Windows에서 `resource` 메모리 계측만 shim으로 처리; 수치 함수 불변. Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3, 수치 스레드 1.

## 1. 질문별 판정

| 질문 | 판정 | 근거 / 남는 범위 |
|---|---|---|
| B1 RIMPR-R01 | **닫힘 — 지목된 헤더 정상화 결함** | `rint_iface_join.py:300–312`가 표지를 한 번만 제거하고 뒤 경계를 ASCII 공백·탭·끝으로 확인. 지난 구조 탐침 144건에서 뜻밖 PASS/REJECT 0. 기존 false-PASS 헤더 10건은 REJECT. 정상 공백·탭·ASCII 진단 열·원 gz는 유지. 전체 문법 검증 완결이라는 뜻 아님. |
| B2 RIMPR-03 | **닫힘 — 정수 토큰의 비-ASCII 숫자 수용** | `:105`, `:200` 부근의 ASCII 정수 및 int64 검사. 전각·아라비아 숫자를 거부하고 정상 ASCII `%g`, `-0`, 부호·0 채움 정수는 유지. `%g`가 정수 ID 1e6 이상을 지수화하는 경우까지 수용한다는 뜻 아님(명시적 지원 밖). |
| B3 RIMPR-04 | **부분 — open 유지 타당** | `:751–765` f6의 `dist/wd/dd`, `:887–895` 내보내는 폭/면적/δ 유한성은 이전 반례를 막음. 하지만 이 코드는 안정 산술이나 모든 파생값의 유효성을 보증하지 않음. 작은 단위 환산에서 0 반지름·면적 PASS를 재현. 따라서 "이 조인을 정량 소비자 인증으로 믿지 않음"은 여전히 사용 범위 조건이지 완결된 기계 인증 아님. |
| B4 SELF-124 | **닫힘 — 요청한 문서 범위** | 현재 핀 요청서 `codex_rint_join_rimpr_fix_recheck_request_20261020.md:15,22,53`과 원장 `SELF-124`의 정정 표지를 확인. Rint 수정 커밋의 봉인 교집합 0과 전체 스냅샷 동일성을 분리하고, 78/135는 저자 보고·재현 불가, 81/138은 같은 138시험의 재실행임을 구분. 이전 판정문 자체의 "NUMERIC_MODULES 여섯 모두 동일"도 틀렸음(§4). |
| B5 새 결함 | **새 생산 P1/P2는 발견하지 않음. 새 P3 시험 이식성 결함 1건** | Windows CRLF 픽스처가 CRCRLF를 만들며 정상 입력 거부로 오판. 생산 parser 결함은 아님. §3. |
| B6 PB1 다섯 | **해당 범위 닫힘** | 전역 dump ASCII 어휘, 구역 경계, scaffold 고정소수 문법, 선언 step 토큰, wd-only 회귀 모두 작동. 독립 저장 형식 양성 대조 통과. F1에 이미 적힌 비단어 꼬리·예외 경로·수치 한정은 여전히 열림. |

결론: **이번 부분 수정의 타당성 지지. ①′ 정량 채택·생산 HOLD 해제 증거는 아님. Part A의 새 정량 소비자가 자동으로 이 PASS의 권한을 상속해서는 안 됨.**

## 2. 직접 실행한 증거

### 2-1. 지난 탐침의 변경 없는 논리 재실행

경로 상수만 검토 디렉터리로 바꿨고 산술·assertion·시험 입력은 보존했다. 어댑트 사본과 로그를 함께 보관했다.

- `structure_probe.py`: 144건, 뜻밖 PASS 0·뜻밖 REJECT 0. real14 457/457/457 · AM–AM 660; case15 104/104/104 · AM–AM 119.
- `numeric_review.py`: 113건, PASS 8 / REJECT 105 / 예외 0. 원래 PASS 15 중 전각 정수 1건·overflow 6건이 REJECT로 전환. 기존 거부에 사유가 더해진 것은 상태 전환과 구분.
- `numeric_overflow_replay.py`: 정상 PASS; x=1e160의 `inf > inf` 거짓 통과는 `derived_nonfinite`로 REJECT. x=1e150 대조도 `delta_pos_mismatch` REJECT.
- `structure_minimal_replay.py`: 첫 사례의 실제 정량 소비자에서 `ValueError: join_gate_failed(T4-2 n=1)`로 중단. 옛 탐침이 ACCEPT를 가정하던 제어 흐름이라 반환코드 1은 **수정된 관문이 발화한 결과**. "탐침 전체 PASS"로 둔갑시키지 않음.

### 2-2. 독립 합성·원자료 확인

`independent_join_checks.py`는 제출자의 테스트 헬퍼를 쓰지 않고 두 같은 구의 교차 원판 `π(r²−d²/4)`를 직접 계산해 덤프를 만들었다. 62건 모두 사전에 지정한 동작과 일치(32 PASS / 30 REJECT). **32 PASS 중 8건은 요청서가 공개한 F1 잔여 false-G-frame 사례를 그대로 살아 있는 한계로 확인한 것**이므로 "62건 정상 인증"이라고 쓰지 않는다.

- 올바른 바이트로 만든 LF·CR·CRLF·gzip·gzip 2-member 모두 PASS.
- 비-ASCII 숫자·구역 경계·덤프 어휘·새 F1 word-tail는 REJECT.
- `laststep`·`my_timestep`·`step-size` 주석을 원 step 주장으로 읽지 않음.
- `# step 100-5` 등의 공개된 잔여 꼬리는 두 덤프 step=100일 때 PASS + G-frame 주장. 새 결함으로 재등재하지 않음.
- real14·case15 원 gz를 읽은 구/신 결과에서 입자 3배열·id 사상·AM–AM 6배열·`delta_bound_um` **비트/값 동일**. 두 원자료의 `delta_bound_um=0.002915255888325765 µm`.

### 2-3. wd-only 변이 감도 — 실제 필요한 가드인가

`known_limit_and_mutant.py`의 정상 AM 쌍은 유지하고, x=1e160에 겹친 비-AM 쌍 둘을 추가했다. 정확한 중심 거리 0, 두 반지름 합 0.002 sim, 기록 δ=0.0005 sim → 오차 0.0015 sim. `dist=0`, `dd=0.0015`는 유한이고 허용폭 `wd`만 inf가 된다.

- 원 v6: `REJECT`, 이유 `derived_nonfinite`, `n_derived_nonfinite=1`.
- 메모리에서만 `np.isfinite(wd)`를 제거한 검토용 변이: **PASS**.
- 따라서 wd 검사 회귀는 형식적 테스트가 아니라 실제 거짓 통과를 막는 판별력이 있음. 반면 dist/dd 가드 제거가 별도 실패를 안 내는 동치 변이는 독립 결함이라고 주장하지 않음.

### 2-4. 남은 수치 범위의 직접 반례

같은 정상 AM 쌍을 `sim_to_um=5e-324`로 호출:

| 값 | 기본 1000 환산 | 5e-324 환산 |
|---|---:|---:|
| status | PASS | PASS |
| r_um | [1.0,1.0] | [0.0,0.0] |
| area_um2 | [1.37445] | [0.0] |
| delta_bound_um | 2.732324012649634e−5 | 0.0 |

이는 요청서 B-2에 공개된 **RIMPR-04 잔여**의 재현이다. 새 finding 아님. 유한성 검사만으로는 환산 뒤 양의 물리량을 보존하지 않는다. 실 생산 단위에서 발생했다고 주장하지 않는다.

### 2-5. 테스트 묶음 교차

- 현재 시험 원문 그대로 Windows 실행 → **320 PASS / 4 FAIL**. 실패 네 건은 모두 §3의 줄 끝 픽스처 생성 문제. Linux 주장 324/324를 반박하지 않음.
- 현재 324 assertion + 아래의 명시적 LF **시험 픽스처 작성기만** 어댑트 → 324/324. 위 두 실행 모두 전체 핀 `source/`에서 재실행 완료.
- 같은 현재 324 assertion을 이전 2b9efa253 모듈에 실행 → 179 PASS / 145 FAIL. 이는 제출자가 기록한 중간 커밋별 152/206·231/309·313/324를 재현했다는 뜻이 아님.
- 이전 138 assertion을 현재 overlay 모듈에 실행 → 138/138.
- 현재 주변 시험: am_iface 136/136 · rrm 55/55 · t4 8/8 · t43 6/6 · t2 23/23.
- 전체 핀 `source/`에서 `step3 --selftest`, `--selftest-rint`, `rint_t41_census --selftest`도 직접 실행 → 셋 모두 PASS, 반환코드 0. 합성 소규모 회귀이며 생산 침대 시뮬레이션 실행 아님.

## 3. 새 P3 — 정상 CRLF 픽스처가 Windows에서 잘못 생성됨

**임시 ID `RINT2-B-01` / P3 / 시험 이식성.** 무너지는 결론은 "해당 시험을 플랫폼과 무관하게 그대로 돌리면 정상 CRLF가 통과한다"이며, 생산 판독기의 CRLF 지원이나 Linux 324/324를 반박하는 것은 아니다.

- `scripts/test_rint_g2_join.py:155–158`의 `open(...,'w')`는 Windows에서 LF를 CRLF로 변환.
- 같은 파일 `:1004`가 그 바이트의 LF를 다시 CRLF로 바꿔 **CRCRLF**를 생성.
- `:1429`는 CRLF의 LF만 CR로 바꿔 **CRCR** 생성; `:1433`의 mixed 변환에도 기존 CR이 남음.
- 실제 `A\nB\n` 기본 text write 바이트 = `410d0a420d0a`; LF→CRLF 재치환 뒤 = `410d0d0a420d0d0a`, 중복 CR 2개.
- 원 시험의 J12P CRLF(입구·소비자), J15P CR-only·mixed CRLF/LF 네 assertion이 실패. 독립적으로 정확히 직렬화한 다섯 저장 형식은 PASS.

**최소 해결:** 픽스처 작성기의 `open(..., newline='\n')` 또는 binary LF 쓰기로 초기 바이트를 고정하고 CR/CRLF 변환을 적용. 생산 parser를 CRCRLF 수용 쪽으로 풀 이유 없음. 해결 증거는 네 실패→통과, 독립 CR/CRLF 대조 유지, Linux 결과 불변. 이번 검토에서는 production/test 원본 파일을 고치지 않고 실행 메모리의 작성기 한 줄만 바꾼 별도 결과를 보존했다.

## 4. 이전 Codex 판정문 오류 정정 (신규 생산 finding 아님)

이전 판정문 `codex_review_rint_join_rimpr_q7_recheck_20261020.md:200`의 "S3 NUMERIC_MODULES 여섯 개는 두 핀 사이 모두 동일"은 잘못이다. `seal_s3_prerun.py:106–108`의 여섯 중 `network_conductivity.py`는 다르다.

- dcb97f1ed 쪽 SHA256: `da9ecfefd8dc4b84e222140e347e4a718381169f27c88bf56c71ec4a7c2749be`.
- 2b9efa253 쪽 SHA256: `a525e2db98fd044f0aa9353b028a3d5c7164c006a8e870dda24e7a0991d9751e`.
- 당시 `evidence/root_metadata.json`의 봉인 비교는 실제 경로로 이 차이를 기록했으나, 별도 `s3_comparison`은 `scripts/` 접두어 없는 키로 조회해 **null==null 여섯 건**을 동일성으로 적었다. 같은 판정문 다음 문단이 network_conductivity 변경을 열거한 것과 모순이다.

따라서 정정문은 그대로 유지할 수 있다:

> 이번 Rint 수정 두 커밋은 봉인 32개를 변경하지 않았다. 대조 핀 이후의 다른 트랙 변경까지 포함한 전체 스냅샷의 동일성은 별도다.

이전 잘못된 문장은 Codex의 비교 오류이며 저자의 정정 요구가 맞다. 해당 오류만으로 Rint 조인 관문 수치 판정이 뒤집히지는 않는다.

## 5. 재현 명령 (검토 root의 부모에서)

```powershell
$py='C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$r='rint2_carbon_design_review_20261021/part_b'
$src='rint2_carbon_design_review_20261021/source'
& $py -X utf8 -B "$r/run_review.py" probe structure_probe.py --source $src
& $py -X utf8 -B "$r/run_review.py" probe numeric_review.py --source $src
& $py -X utf8 -B "$r/independent_join_checks.py" --source $src
& $py -X utf8 -B "$r/known_limit_and_mutant.py" --source $src
& $py -X utf8 -B "$r/run_review.py" test test_rint_g2_join.py --source $src --test-source $src
& $py -X utf8 -B "$r/run_review.py" test test_rint_g2_join.py --source $src --test-source $src --lf-test-writer
& $py -X utf8 -B "$r/run_review.py" test step3_sigma.py --source $src --test-source $src --test-arg=--selftest
& $py -X utf8 -B "$r/run_review.py" test step3_sigma.py --source $src --test-source $src --test-arg=--selftest-rint
& $py -X utf8 -B "$r/run_review.py" test rint_t41_census.py --source $src --test-source $src --test-arg=--selftest
```

주의: 이전 탐침의 내부 JSON에 보존된 과거 `source_pin` 문자열은 그대로 남아 있다. 실행 위치·모듈 해시·현재 판정은 이번 harness의 실행 기록과 함께 읽는다. 과거 pin 문자열만으로 이번 실행 핀을 오인하지 않는다.
