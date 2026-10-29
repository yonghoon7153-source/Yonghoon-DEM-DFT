# 독립 프로그램 대조 재검토 — 2026-10-30

검토 대상은 부모 검토자가 고정한 `bf8cf21c6466cdb9411f9320711b871c2d1c651e`의 `scripts/resume_ckpt.sh`다. 직접 읽은 파일 SHA-256은 `77c242375c4093023e609703ef471c64c2370d374e7533824412d96da5b1b9f8`이다. 아래 줄 번호는 이 파일의 1-based 번호다.

**판정: KG50R-03 / KG50P-01은 부분 수정, 핵심 준비 구간 값 보존 보장은 열림(P1).** 기존 재정의 추가·순서 변경 반례는 막지만, 허용하는 삭제가 소비되는 변수 값을 바꾸는 경우를 놓친다. 압축 거부, 첫 긴 run 꼬리 거부, 논리 명령 기준 시험 절단은 조사한 CPU 입력에서 작동했다.

## 실행 증거의 범위

- Python 3.12.14 Windows에서 제품의 내장 Python 본문을 추출했다. 함수의 내용은 변경하지 않았다. `check()` 직접 호출과 별도 프로세스의 추출 CLI 종료 코드를 각 입력마다 교차 확인했다.
- `probe_program.py`가 만든 **43개 입력**의 원문, stdout, argv, 종료 코드, 기대 의미는 `cases/`와 `results.json`에 있다. 이 숫자는 저자 시험 216개의 재실행 수가 아니다. 아래 `static_rc=0`인 반례는 검토 성공이 아니라 제품의 잘못된 수용을 뜻한다.
- 실제 SLURM, LIGGGHTS, MPI, WSL, Bash는 실행하지 않았다. 이 환경의 Bash가 시작 불가능하다는 부모 검토자의 제약을 따랐다. 저자 fake-SLURM 결과를 독립 실행 결과로 계산하지 않았다.
- 제품 파일은 읽기만 했다. 모든 산출은 `kg50_fix30/independent/program/` 아래다. 파생 D2 반례는 명시적으로 합성한 사본이며 실제 D2 런 덱에 이미 있는 결함이라는 주장이 아니다.

재현(PowerShell):

```powershell
& 'C:\Users\Administrator\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -I -X utf8 'C:\Users\Administrator\Documents\Codex\kg50_fix30\independent\program\probe_program.py'
```

## KG50RF-01 — P1: 순서 보존 부분열은 `${변수}` 소비 값 보존이 아니다

**위치:** `scripts/resume_ckpt.sh:432–468` (`setup_order`, 특히 461–468의 건너뛰기), `:313–318` / `:332–338` (`run_state`의 마지막 문자열 저장), `:482–498` (`state_cmp`), `:741–745` (통합 호출).

**주 반례는 아래 D2 파생 중력형이다.** 원 덱 196.2와 재개 덱 98.1을 소비하는 fix가 checkpoint 읽기 뒤에 확실히 위치하며, 기본 2,000-step 시험 절단과 합산까지 모두 통과한다. 먼저 표시한 작은 timestep 조각은 결함의 원인을 최소화해서 설명한다.

본 덱 준비 구간을 다음과 같이 둔다.

```text
variable dt equal 1e-6
variable dt equal 2e-6
timestep ${dt}
variable dt equal 1e-6
```

재개 덱은 `read_restart` 뒤에 아래 세 줄만 둔다.

```text
variable dt equal 1e-6
timestep ${dt}
variable dt equal 1e-6
```

재개 세 줄은 원래 네 줄의 순서 보존 부분열이다. 끝 상태 표도 양쪽 모두 `variable dt equal 1e-6`와 `timestep ${dt}`이므로 같다고 판정한다. 그러나 `${dt}`를 소비할 때 본 덱은 **2e-6**, 재개 덱은 **1e-6**이다. 마지막 `variable dt equal 1e-6`는 이미 설정한 timestep을 소급해서 바꾸지 않는다.

`cases/drop_intermediate_variable_definition/`의 실제 결과:

| 검사 | 실제 결과 |
|---|---|
| 추출 CLI / `check()` | **rc 0 / 문제 0** |
| 남은 run | 끝 100 일치 |
| `cut_trial(..., '10', ...)` | **rc 0**, `50 10 0 7` |
| `trial_steps()` | **rc 0**, `10 1 [run 10]` |
| consumed timestep | 본 2e-6 / 재개 1e-6 (2배 차이) |

`results.json`은 Python 실행 파일, 추출 본문, main/resume 파일, checkpoint, S0=50, 작업 폴더의 **전체 argv**를 보존한다. 원문 `main.liggghts:2–5`, `resume.liggghts:3–5`가 해당 블록이다. 이 작은 입력은 검사 계약의 최소 조각이며 실제 입자 시뮬레이션 실행을 주장하지 않는다.

### 받은 D2 덱 구조에 옮긴 동일 반례

작은 조각만의 문제가 아님을 확인하기 위해 받은 D2 원본과 재개 덱을 복사했다. **변형하지 않은 받은 쌍은 `d2_received_baseline`에서 문제 0**이다. 그 후 원문의 `fix gravi all gravity 98.1 ...` 한 줄을 양쪽에서 변수형으로 바꾸었다.

`cases/d2_drop_intermediate_variable_definition/main.liggghts:160–163`:

```text
variable g_probe equal 98.1
variable g_probe equal 196.2
fix gravi all gravity ${g_probe} vector 0.0 0.0 -1.0
variable g_probe equal 98.1
```

`resume.liggghts:150–152`는 두 번째 `196.2` 정의만 없다. 이 fix는 재개 덱의 `read_restart` **뒤**에 있다. 원 덱 소비 중력은 **196.2**, 재개 덱은 **98.1**이다. 나중 변수 복원은 이미 생성된 fix의 인수를 바꾸지 않는다.

실제 결과는 `check()` **문제 0 / CLI rc 0**, cutter **rc 0 / `180000 2000 0 159`**, trial 합계 **rc 0 / `2000 1 [run 2000]`**다. 뒤 64개 명령도 같다고 출력했다. 원 체크포인트 파일 또는 입자 운동을 생성하지 않았고, G0–G3/Bash 전체 사슬 통과나 물리 오차를 관측했다는 뜻은 아니다. 이것만으로도 ‘덱 명령으로 상태를 바꾸는 길은 전체 프로그램 대조가 막는다’는 보장은 성립하지 않는다.

### 같은 부류 보강 — 실행 상태 의존 equal 수식

`cases/d2_runtime_dependent_eager_variable/`은 양쪽 동일한 `variable g_probe equal 98.1*(step+1)`와 `fix gravi ... ${g_probe} ...`를 사용한다. 삭제·재정의조차 없다. 원본의 fix 소비 시점은 삽입 `run 1` 뒤 **step 1**이고 재개는 **step 20001**이다. 산술상 값은 각각 `98.1×2 = 196.2`, `98.1×20002 = 1962196.2`다. 세 Python 검사 모두 rc 0이다. 작은 timestep형 `runtime_dependent_eager_variable`도 함께 남겼으나, D2 파생 중력형을 실행 위치가 명확한 근거로 우선한다.

고정 버전의 공식 `variable` 문서는 equal/string/atom 재정의 허용(127–132행), equal 수식의 사용 시점 재평가(278–293행), `${...}`의 즉시 값 치환(700–718행)을 명시한다. 따라서 동일 문자열·마지막 정의만으로 두 소비 시점의 값이 같아지지 않는다. [CFDEM 공식 고정 커밋 variable 설명](https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/doc/variable.txt). 이 문헌은 실제 설치 바이너리가 같은 커밋임을 인증하지 않는다.

**최소 해결:** 준비 구간의 허용 삭제 규약을 좁혀, 상태 명령의 값 소비 시점에 도달하는 변수 정의(reaching definition)와 의존 변수를 보존해야 한다. 상수로 판정 가능한 표현과 독립 재선언만 지원하는 제한된 구현도 가능하다. 해석할 수 없는 재정의·의존 수식·step/count/compute 등 실행 상태를 참조한 즉시치환은 자동 수용하지 않아야 한다. 단순히 ‘모든 변수 이름이 앞에 존재’ 또는 ‘부분열’ 검사를 더 하는 것은 충분하지 않다. 중간 정의 삭제와 동적 equal 두 회귀 입력을 추가하고, 올바른 상수·안전 삭제 양성 대조도 유지해야 한다.

## 현재 정상 덱과의 구분

- 받은 D2 원문 `input_kg50_d2_b50.liggghts:43/45`, 재개 `input_kg50_d2_b50_r4.liggghts:47/49`의 dt는 **상수 1e-6**다. 위 재정의나 step 수식은 원문에 없다.
- 원문 준비 구간의 `n_ins=count(all)`, `n_am_ins=count(g_am_ins)`, `n_se_ins=count(g_se_ins)`는 삽입 수 확인용이다. 읽은 정착 덱에서는 그 뒤 새 삽입/삭제가 없으므로 이 재평가 자체를 새 물리 결함으로 보고하지 않는다.
- `z_max=c_zmax` 및 `plate_z=${z_max}+${r_AM_P}+${plate_margin}`는 원문 D2 `:175–176`, 재개 `:165–166`에 있으며 정착 뒤 동일 suffix다. 그 전에 판 높이용 `run 1`도 남아 있다.
- 보관된 D0.7 after_settling 정상쌍을 직접 다시 검사했다. `archived_after_settling_baseline`은 문제 0, 시험 `run 1 + run 2000 = 2001`이다. checkpoint 뒤 첫 긴 run 전 35개, 뒤 27개 명령의 같음을 출력했다. 이것은 CPU 정적 대조의 양성 대조다.

## 담당 항목별 판정

| 항목 | 이번 독립 판정 | 직접 근거 / 남은 경계 |
|---|---|---|
| KG50R-01 | **거부 방식으로 닫힘 — 조사 범위** | 실제 제공 r075 압축쌍, 이름을 가진 합성 압축, 다른 이름의 label/jump 루프 모두 rc 1. `:663–709`. 압축 재개 기능 구현 판정은 아님. |
| KG50R-02 | **닫힘 — Python 정적/절단 범위** | 첫 재개 run의 every/pre/post/start/stop/upto 여섯 꼬리 전부 `check=1`, `cut=1`; 보관된 every도 거부. `:270–282`, `:812–849`. |
| KG50R-03 | **부분 / P1 열림** | 보관 suffix velocity/density/delete/include, missing variable, duplicate label 반례는 모두 거부. 그러나 위 준비 구간 변수 값 반례는 통과. |
| KG50R-05 | **닫힘 — Python 정적/절단 범위** | `run &` + `50` 첫 run은 check/cut 모두 rc 1. 정상 after_settling 합은 1+2000=2001. 본 셸 예산 검사의 동적 실행은 하지 않음. |
| KG50P-01 | **부분 / P1 열림** | 추가/순서 변경 방어는 생겼지만 ‘중간 정의 삭제’로 같은 consumed-value 결함이 살아남음. |
| KG50P-02 | **닫힘 — CPU 범위** | 본 덱 첫 run 꼬리 여섯 종류는 모두 rc 1. `:658–662`. |
| KG50P-06 | **소스상 수정, 셸 동적 미확인** | CASEA 배열 `:1041`, 이름 정규식 `:1091`로 `C ./C` 부류 차단; 값 초기화 뒤 read 성공 필수 `:1211–1215`. 부모 셸 검토와 결합할 항목. |
| KG50P-08 | **열림 / 명시된 한정** | `checkpoint_basename_alias`는 다른 폴더의 같은 basename인데 rc 0. `:628–637`. 실제 파일 상태/신원 증명 없음. |
| KG50P-09 | **열림 / 알려진 파서 차이** | NBSP 및 separator 없는 `&` 입력은 정적·cut·trial 모두 rc 0. `:81–97`, `:792–809`. 이 검토는 실제 LIGGGHTS 오류/G0 차단을 실행하지 않았으므로 ‘닫힌 실패’를 독립 동적 확인했다고 쓰지 않는다. |
| KG50P-10 | **열림 / 명시된 한정** | 대체 STL이 빈 파일이어도 `mesh_empty_existing_file` rc 0. `:375–390`, `:567–586`. 존재 검사이며 기하/내용 검사 아님. fix 순서 자체는 별도 setup_order에서 강화됨. |

43개 결과 중 ‘expect reject’인데 `static_rc=0`인 것은 위 새 변수 부류 4개다(작은 반례 2 + D2 파생 2). basename/파서/메시 네 가지는 이미 요청서에서 명시한 한계를 독립 재확인한 것이므로 새 P1 숫자로 더하지 않았다. 정상 대조·기존 반례는 개별 `results.json` 기록으로 확인할 수 있다.

## 종합 검토자에게

기존 반례들의 수용 경로가 많이 닫힌 사실과 전체 프로그램 의미 보존을 닫았다는 결론을 분리해야 한다. 본 검토의 권고는 최소 해제 목록 2를 **미해제**로 유지하는 것이다. 현재 받은 D2/D0.7 정상 덱에 위 합성 변이가 이미 존재한다거나, 실제 job에서 중력이 달라졌다는 주장은 하지 않는다. 실제 도구 사슬 `-T` 및 Bash fake-SLURM 재실행은 여전히 별도 증거다.
