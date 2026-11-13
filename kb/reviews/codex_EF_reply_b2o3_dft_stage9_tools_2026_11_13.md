---
title: "EF 회신 — b2o3 9 단계 DFT 도구 · 카드 개정 5: NO-GO (P0 0 · P1 6 · P2 6) · DY 확인 4 아직 해제 못 함 · 세 쌍 탐침 해석 찬성 · 기준 셀 조건부 수용"
date: 2026-11-13
updated: 2026-11-13
tags: [review, b2o3, dft, qe, eos, kprobe, readout, codex, reply, letter]
letter: EF
track: b2o3
channel: codex
kind: reply
status: 수령 2026-11-13 (사용자 붙여넣기) · NO-GO · 기준 4b95dedb (도구 sha256 559f0152) · 고침 → 다음 편지 EG
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 원문 그대로 보존 (사용자 붙여넣기 2026-11-13). 링크의 C:/ 경로는 Codex 쪽 작업 폴더다 (저장소 밖).

NO-GO — `4b95dedb`에서 P1 6건이 남았습니다. DY 확인 4의 “EOS 입력을 실제 계산 결과에 결속”도 아직 해제하지 못합니다.
대상 도구 SHA256 `559f0152…`를 확인했습니다. Windows에서 LF 쓰기를 명시한 검증용 어댑터로 selftest 66/66을 재현했고, 추가 반례를 실행했습니다. 원본 소스는 수정하지 않았고 생산 UMA·DFT·MD도 실행하지 않았습니다.
아래 재현은 합성 QE 출력과 시험용 구조를 사용했습니다. 실제 계산에서 이미 이런 오류가 발생했다는 뜻은 아닙니다. 8단계 연결은 공개된 `_FakeRD`를 사용했으므로 gabia의 실물 `md.traj` 재검증과도 구분합니다. 주장한 변이시험 38종 전체를 다시 돌린 것은 아닙니다.
P0: 이번 검증에서 확인한 항목 없음. P1: 아래 6건.
P1-1. 서로 다른 실행의 설정·완료 표시·에너지를 합쳐서 통과시킵니다.
위치: [b2o3_bo_dft.py (line 316)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:316), [348 (line 348)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:348).
재현: 정상 완료된 출력 뒤에 ENCUT 40 Ry·다른 시작 좌표·`JOB DONE` 없는 두 번째 실행을 붙였습니다. 판독기는 첫 실행의 `ecutwfc=52`, 좌표, 완료 표시와 두 번째 실행의 에너지를 조합해 문제 목록 `[]`로 통과했습니다. 완료된 relax 뒤에 미완료 재시작 머리글만 붙여도 이전 완료 결과를 그대로 승인했습니다.
최소 수정: 실행 구간을 먼저 분리하고, 설정·SCF·힘·응력·BFGS·최종 좌표·완료를 같은 실행 구간에서 읽으세요. 이번 러너가 출력 파일을 덮어쓰는 방식이라면 다중 실행 파일을 거부하는 것이 가장 단순합니다. 재시작 연결을 지원하더라도 미완료 마지막 실행을 무시하고 이전 완료분으로 후퇴하면 안 됩니다.
P1-2. 계획을 다시 검사할 때 후보 이름만 원자료와 대조하고, 실제 구조와 고밀도 k 경로의 자격은 계획을 믿습니다.
위치: [b2o3_bo_dft.py (line 695)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:695), [711 (line 711)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:711).
두 반례가 통과했습니다.

* 후보 이름은 `cfg0003`으로 두고 `structure`를 `cfg0005` 것으로 바꾼 뒤 입력과 해시를 함께 갱신하자, 다른 구조를 `cfg0003` 결과로 읽고 탐침 입력까지 생성했습니다.
* 계획의 `k_main`을 `4×2×1`로 바꾸고 입력·해시를 함께 갱신하자, `after_kprobe=null`인데도 이완과 10단계 선택까지 통과했습니다.

최소 수정: 재결속에서도 8단계 원기록의 `_struct(...)`로 구조를 다시 찾고 계획의 구조와 대조하세요. `prepare`에 있는 허용 k·발동 증거 검사를 소비 단계에서도 공통으로 적용해야 합니다. 현재의 “입력과 계획 해시를 함께 바꿔도 거부” 시험은 `mixing_beta` 사례만 보호합니다.
P1-3. 탐침이 실제로 더 촘촘한 k 격자에서 계산됐는지 확인하지 않습니다.
위치: [b2o3_bo_dft.py (line 473)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:473), [838 (line 838)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:838).
재현: 탐침 세 출력에 본 계산과 같은 k점 수와 같은 에너지를 넣었습니다. 결과는 `k_main=4점`, `k_probe=4점`, `triggered=false`였고 이완 입력 세 개를 생성했습니다.
현재 검사는 단계 안의 k점 수가 서로 같은지만 봅니다. 입력 파일이 `4×2×1`이라는 사실은 그 출력이 해당 입력으로 계산됐다는 증거가 아닙니다.
최소 수정: 실제 실행의 QE 출력 또는 함께 보존한 XML에서 격자·shift 또는 k점 좌표와 가중치를 확인해 요청한 격자와 대조하세요. 단순히 “탐침의 점 수가 더 크다”로 바꾸는 것도 충분하지 않습니다.
P1-4. 더 느슨한 기준으로 끝난 이완을 선언한 기준의 수렴으로 승인합니다.
위치: [b2o3_bo_dft.py (line 362)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:362), [433 (line 433)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:433).
재현: 출력의 BFGS 기준을 `energy < 1e-2 Ry`, `force < 1e-1 Ry/Bohr`로 바꾸고 힘 성분을 `0.05 Ry/Bohr`로 둬도 통과했습니다. 기록된 최대 힘은 약 1.286 eV/Å인데 판정에 사용하지 않습니다.
최소 수정: 출력에 찍힌 BFGS 기준을 계약과 대조하고 마지막 SCF의 완전한 힘 블록을 확인하세요. QE의 `forc_conv_thr`는 모든 원자의 모든 힘 성분 기준이므로 현재의 최대 벡터 크기와 혼동하지 않아야 합니다. [QE 수렴 기준](https://www.quantum-espresso.org/Doc/INPUT_PW.html)
P1-5. 전자 수를 읽지만 전하 상태 검증에 쓰지 않습니다.
위치: [b2o3_bo_dft.py (line 319)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:319), [382 (line 382)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:382).
재현: 출력의 전자 수를 596→595로 바꾸거나 해당 줄을 삭제해도 통과했습니다. 같은 기하·PP·cutoff로 돌린 다른 전하 상태의 출력이 들어오면 현재 검사는 구분하지 못합니다.
최소 수정: 고정한 PP의 가전자 수, 조성, 선언한 총전하로 기대 전자 수를 계산하고 출력과 대조하세요. 결측도 거부해야 합니다.
P1-6. “EOS 필요, 고르기 안 함”인데 전자구조 대상은 발행합니다.
위치: [b2o3_bo_dft.py (line 934)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:934).
재현: 세 가족을 `|P|=2.5 GPa`로 두면 `skip_eos=false`, `stage10=null`이 되지만 `electronic_targets`는 여전히 3개입니다. 개정 5의 “EOS 생략일 때만 … 전자구조 대상 … 생략 불가면 고르지 않는다”와 다릅니다.
최소 수정: 이완 구조는 진단 자료로 보존하되, EOS 보류 시 실행 대상으로 읽히는 필드는 `null`로 두세요. 전자구조를 별도로 진행하려는 정책이라면 카드에서 명시적으로 분리해야 합니다.
P2는 다음 6건입니다.

* 저장하지만 읽지 않는 증거가 남았습니다. [814 (line 814)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:814), [872 (line 872)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:872): SP 판정의 `order·gap·G5·sentence_sp`를 바꿔도 재결속이 통과하고, 탐침 판정의 출력 SHA를 전부 0으로 바꿔도 통과합니다. 현재 재계산한 값으로 판단하는 부분은 보호되지만, 보존된 설명과 증거가 참이라는 보장은 없습니다. 해당 필드도 재계산·대조하거나 검증 대상이 아닌 파생 표시로 분리하세요.
* 10단계 구조 경로의 기준 폴더가 섞입니다. [634 (line 634)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:634): 안정성 대상의 `post_relax.rel`은 8단계 폴더 기준인데 다른 구조 항목은 9단계 기준입니다. 정상 재현에서 대상 세 경로 모두 판정 폴더 기준으로는 없었습니다. 기준 폴더를 명시하거나 같은 기준으로 경로를 다시 작성하세요.
* 손상된 출력 바이트를 조용히 지웁니다. [314 (line 314)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:314): `1.0E-\xff08`이 `errors="ignore"` 때문에 `1.0E-08`로 복구되어 통과했습니다. 명시적 인코딩의 strict 판독으로 바꾸고 판독 실패를 기록하세요.
* Windows에서는 입력 쓰기와 해시 계산의 줄바꿈 규약이 다릅니다. [233 (line 233)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:233), [759 (line 759)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/b2o3_bo_dft.py:759): 실제 파일은 CRLF, `_text_sha`는 LF여서 정상 입력을 변조로 거부합니다. Native Windows selftest는 여기서 중단됐습니다. 생성 파일의 인코딩·LF를 명시하세요. Linux 결과가 틀렸다는 지적은 아닙니다.
* VRAM 여유 검사는 GPU 독점 검사와 다릅니다. [run_force_check_scf.sh (line 315)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/run_force_check_scf.sh:315): 모의 조회에서 `46000 MiB`이면 다른 프로세스 여부를 묻지 않고 진행했고, 조회 실패로 빈 값이 나와도 진행했습니다. 조회 실패는 거부하고, 동시 실행 금지는 별도 예약·공통 잠금으로 보장하세요. 카드의 “다른 GPU 잡이 있으면 시작하지 않는다”도 실제 보장 범위와 맞춰야 합니다.
* 분석기가 거부한 잡을 러너는 완료로 건너뛸 수 있습니다. [run_force_check_scf.sh (line 29)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/run_force_check_scf.sh:29), [306 (line 306)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/source/tools/doping/run_force_check_scf.sh:306): ENCUT 40 출력은 새 분석기가 거부하지만 `_fc_ok`는 0을 반환했습니다. “같은 폴더에서 같은 명령 재실행”만으로는 고쳐지지 않습니다. 거부 출력 보존 후 명시적으로 재실행하는 절차 또는 공통 완료 검사를 마련하세요.

P3는 추가하지 않습니다.
Q1. 출력 결속에 구멍이 있나? — 있습니다.
셀·초기 좌표·PP MD5·최종 에너지 대조는 유효한 검사입니다. 그러나 P1-1처럼 실행 구간이 섞이면 그 검사들이 같은 계산을 가리키지 않습니다. k 격자, 전자 수, 이온 수렴 기준도 추가로 닫아야 합니다.
Q2. DY 확인 4가 닫혔나? — 아직 아닙니다.
좋아진 부분은 명확합니다. 임의로 넘긴 숫자 대신 출력에서 E·P·V를 읽고, 단위를 변환하며, 원파일 SHA를 남깁니다.
하지만 파일 SHA는 그 파일 안의 값들이 같은 실행·같은 최종 상태에서 왔다는 보증이 아닙니다. P1-1과 이완 수렴 검사가 해결되어야 해제할 수 있습니다.
Q3. 세 가족 쌍 전체·절댓값 경계 해석은? — 찬성입니다.
세 쌍의 차 변화, 전체 순서 변화, `|차|`의 0.10 경계 통과를 따로 검사하는 구현은 제안한 규칙과 맞습니다. 부호 반전도 순서 검사로 잡습니다.
수정할 것은 발동식보다 발동식에 들어오는 두 격자 계산의 실재성입니다.
Q4. 기준 셀과 이완 문턱이 충분한가? — 기준 셀은 조건부 수용, 정확도 보증은 아닙니다.
host 모양·공통 V₀에 분수 좌표를 이식하는 것은 선언한 고정셀 비교로 일관됩니다. 다만 Cartesian 기하는 바뀌므로 “UMA 기하 그대로”는 단일점 단계에만 적용해야 합니다.
권장 보고 문구는 다음 수준입니다.
각 초기 가족에서 사전 규칙으로 선택한 대표 구조를 공통 기준 셀에서 이온 이완한 에너지 비교.
이를 가족 전체의 DFT 최저에너지나 자유 셀 바닥상태로 확대하면 안 됩니다.
`1e-3 Ry/Bohr ≈ 0.02571 eV/Å`, `1e-5 Ry ≈ 0.0001361 eV`입니다. 그러나 후자는 연속 이온 단계 사이 에너지 변화 기준이고, 남은 최소화 오차의 상한이 아닙니다. 따라서 0.10 eV는 판정 여유이지, 이 설정으로 인증된 정확도는 아닙니다. 초기 실행값으로 사용할 수 있지만 결과 전 운영 규칙에서 수렴 재확인의 적용 대상을 정하거나, 판정을 해당 수렴 설정에 조건부로 제한해야 합니다. [QE 기준 정의](https://www.quantum-espresso.org/Doc/INPUT_PW.html)
Q5. EOS 절차를 지금 완성해야 하나? — 이번 단계가 확실히 멈춘다면 필수는 아닙니다.
압력 보정량은 재계산해도 맞습니다. `|P|=0.3 GPa`에서 약 0.0211–0.0315 eV이며 독립 B 조합을 검사하는 방향도 적절합니다.
생략 불가 시 자료를 보존하고 다음 단계 선택을 막는 방식은 허용됩니다. P1-6을 고치면 됩니다. 이후 EOS를 설계할 때는 이미 관측한 압력·에너지를 밝히고 새 단계 실행 전에 규칙을 고정하세요. 전체 설계가 결과를 보기 전에 정해졌다고 소급 표현해서는 안 됩니다.
Q6. 10단계와 전자구조 계보는 맞나? — 선택 논리는 맞고 전달 계약은 미완료입니다.
승자 가족의 UMA 어닐 최저 셋, 못 가르면 가족별 UMA 최저 하나, 전자구조는 DFT 이완 대표 셋이라는 구분은 카드와 맞습니다. 안정성 대상을 DFT 이완 구조로 임의 교체하지 않은 것도 맞습니다.
다만 EOS 보류 시 대상 발행, 상대경로 기준 혼재, P1-2의 부모 구조 바꿔치기를 해결해야 합니다.
Q7. SCF 운영값과 PP 이름은? — 제안값 자체에 즉시 반대할 근거는 없습니다.
`mixing_beta=0.3`, `electron_maxstep=200`은 시작 운영값으로 수용할 수 있습니다. 서로 다른 PP 계열을 섞었다는 사실만으로 오류는 아닙니다. QE는 조건에 맞는 USPP·PAW 혼용을 지원하며, 같은 XC와 필요한 cutoff를 확인해야 합니다. 파일명만으로 52/520의 수렴을 인증할 수는 없습니다. [QE PP 안내](https://www.quantum-espresso.org/faq/faq-pseudopotentials/)
`disk_io='nowf'`는 파동함수를 저장하지 않으며 중단된 계산의 restart를 지원하지 않습니다. 따라서 실패 잡은 중간 상태 재개와 처음부터 재실행을 구분하고, 후속 전자구조에서 파동함수가 필요하면 별도 생성 단계가 필요합니다. [QE ](https://www.quantum-espresso.org/Doc/INPUT_PW.html)`disk_io`
gabia의 실제 PP 파일과 GPU 빌드는 이번에 직접 검사하지 않았습니다.
Q8. 사용자 비준만 남았나? — 아닙니다.
현재는 코드 해제조건이 남았습니다. 반대로, 이를 고치기 위해 이미 승인된 UMA 단계 전체나 고정셀 방법을 다시 열 필요는 없습니다.
DFT 진입 전 마지막 확인 목록

1. P1-1~5를 고치고, 정상 경로와 이번 반례를 거부 이유까지 확인합니다.
2. EOS 보류 시 안정성·전자구조 대상 모두 실행 승인으로 읽히지 않게 하고, 대상 구조 경로의 기준을 통일합니다.
3. 탐침 출력 SHA와 SP 해석 필드가 재검증되도록 연결합니다.
4. 손상 출력 거부, GPU 조회 실패 거부·독점 운영, 거부된 잡의 보존·재실행 절차를 닫습니다.
5. 실제 실행 Linux 환경에서 수정판을 검증하고 도구·PP·입력 지문을 고정합니다. 그 뒤 사용자 비준을 받습니다.

재현 자료: [검증 범위](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/verification.json) · [파서 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/reproductions.json) · [단계 연결 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/extended_results.json) · [전자 수·러너 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_EF_20261113/remaining_results.json).{
  "target_commit": "4b95dedba0a577a472bdc96542684058e65ab43d",
  "dft_tool_sha256": "559f0152b8774b022c1ae53a9db7ebf52569c191182127dd42af59369a59c60a",
  "readout_sha256": "872d91f7508ad21c3d67f373bee228bd894994b731a77f69525818db3a8967cf",
  "selftest": "66/66 with LF-write adapter on Windows; native Windows run stops on CRLF/LF hash mismatch",
  "production_calculations": 0,
  "source_edits": 0,
  "evidence": [
    "reproductions.json",
    "extended_results.json",
    "remaining_results.json"
  ],
  "limitations": [
    "QE outputs and PP headers in independent tests are synthetic; no actual electronic-structure calculation.",
    "Stage8 uses the disclosed selftest FakeRD; archived format examples also parsed, but live gabia md.traj and PP tree were not inspected.",
    "The 38 reported mutation variants were not independently rerun.",
    "Runner checks execute only extracted completion and memory-guard functions with mock output and mock nvidia-smi."
  ],
  "verdict": "NO-GO"
}{
  "selftest_lf_rc": 0,
  "selftest_lf_tail": [
    "  ✓ [양성] 기준 셀 — host 1×2×5 V 2432.764 → 등방 스케일 1.000488 → V₀ 2436.33",
    "selftest: 66/66"
  ],
  "source_sha256": "559f0152b8774b022c1ae53a9db7ebf52569c191182127dd42af59369a59c60a",
  "fixture": "C:\\Users\\Administrator\\Documents\\Codex\\2026-08-24\\dur\\review_EF_20261113\\scratch\\ef_fixture_a7xyq0sq",
  "baseline_sp": {
    "problems": [],
    "accepted": true,
    "E_Ry": -7.34986444,
    "P_kbar": null,
    "version": "7.4.1",
    "nk": 4,
    "job_done": true,
    "bfgs": null,
    "final_E_Ry": null,
    "ecutwfc": 52.0,
    "max_force_eV_A": 0.00962018793079914
  },
  "baseline_relax": {
    "problems": [],
    "accepted": true,
    "E_Ry": -7.42336308,
    "P_kbar": 5.0,
    "version": "7.4.1",
    "nk": 4,
    "job_done": true,
    "bfgs": {
      "scf_cycles": 2,
      "steps": 1
    },
    "final_E_Ry": -7.4233630795,
    "ecutwfc": 52.0,
    "max_force_eV_A": 0.00962018793079914
  },
  "mixed_complete_then_wrong_unfinished_sp": {
    "problems": [],
    "accepted": true,
    "E_Ry": -9.04033326,
    "P_kbar": null,
    "version": "7.4.1",
    "nk": 4,
    "job_done": true,
    "bfgs": null,
    "final_E_Ry": null,
    "ecutwfc": 52.0,
    "max_force_eV_A": 0.00962018793079914
  },
  "complete_relax_then_unfinished_restart": {
    "problems": [],
    "accepted": true,
    "E_Ry": -7.42336308,
    "P_kbar": 5.0,
    "version": "7.4.1",
    "nk": 4,
    "job_done": true,
    "bfgs": {
      "scf_cycles": 2,
      "steps": 1
    },
    "final_E_Ry": -7.4233630795,
    "ecutwfc": 52.0,
    "max_force_eV_A": 0.00962018793079914
  },
  "loose_bfgs_output": {
    "problems": [],
    "accepted": true,
    "E_Ry": -7.42336308,
    "P_kbar": 5.0,
    "version": "7.4.1",
    "nk": 4,
    "job_done": true,
    "bfgs": {
      "scf_cycles": 2,
      "steps": 1
    },
    "final_E_Ry": -7.4233630795,
    "ecutwfc": 52.0,
    "max_force_eV_A": 1.2855851108175018
  },
  "decode_ignored_corruption": {
    "problems": [],
    "accepted": true,
    "E_Ry": -7.34986444,
    "P_kbar": null,
    "version": "7.4.1",
    "nk": 4,
    "job_done": true,
    "bfgs": null,
    "final_E_Ry": null,
    "ecutwfc": 52.0,
    "max_force_eV_A": 0.00962018793079914
  },
  "probe_same_k_as_main": {
    "accepted": true,
    "triggered": false,
    "why": [],
    "pairs": {
      "F_P-F_B": {
        "k_main": 0.3000000910847689,
        "k_probe": 0.3000000910847689,
        "change": 0.0
      },
      "F_free-F_B": {
        "k_main": 4.000000035303515,
        "k_probe": 4.000000035303515,
        "change": 0.0
      },
      "F_free-F_P": {
        "k_main": 3.699999944218746,
        "k_probe": 3.699999944218746,
        "change": 0.0
      }
    },
    "main_nk": 4,
    "probe_nk": [
      4,
      4,
      4
    ]
  },
  "changed_structure_and_input": {
    "accepted": true,
    "selected_name": "cfg0003_E-0.000_O-bo4",
    "structure_now_from": "cfg0005_E-0.000_O-bo4"
  },
  "changed_k_without_trigger": {
    "accepted": true,
    "after_kprobe": null,
    "k_main": [
      4,
      2,
      1
    ]
  },
  "real_format_examples": {
    "relax": {
      "nat": 23,
      "E_Ry": -411.86371435,
      "final_E_Ry": -411.8637143506,
      "P_kbar": null,
      "volume_A3": 371.39495708243174,
      "job_done": true,
      "bfgs": {
        "scf_cycles": 15,
        "steps": 14
      },
      "nk": 24
    },
    "scf": {
      "nat": 120,
      "E_Ry": -2428.95718263,
      "final_E_Ry": null,
      "P_kbar": null,
      "volume_A3": 2781.7364588285204,
      "job_done": false,
      "bfgs": null,
      "nk": 8
    }
  },
  "conversion": {
    "force_eV_A": 0.02571103373816294,
    "step_energy_eV": 0.00013605693122994002,
    "eos_0p3GPa_eV": [
      0.03153395903926933,
      0.021054981881604446
    ]
  }
}
{
  "wrong_parent_full_read_sp": {
    "accepted": true,
    "reported_name": "cfg0003_E-0.000_O-bo4",
    "actual_structure_name": "cfg0005_E-0.000_O-bo4",
    "outputs_read": 6,
    "probe_jobs_created": 3
  },
  "dense_without_trigger_full_chain": {
    "accepted": true,
    "after_kprobe": null,
    "relax_jobs_created": 3,
    "stage10_created": true,
    "decision": "DFT 이온 이완 (고정 기준 셀 · 보정 전) 최저 F_B · 승자–차저 4.000 ≥ 0.1 — 압력 보정 범위 전체에서 순서 · 판정 그대로 (EOS 생략)"
  },
  "same_mesh_full_read_kprobe": {
    "accepted": true,
    "nk": {
      "k_main": 4,
      "k_probe": 4
    },
    "triggered": false,
    "relax_jobs_created": 3
  },
  "normal_chain": {
    "accepted": true,
    "skip_eos": true,
    "stage10": true
  },
  "stage10_paths": [
    {
      "rel": "cfg0003_E-0.000_O-bo4/post_relax.xyz",
      "exists_relative_to_readout": false,
      "exists_relative_to_stage8": true
    },
    {
      "rel": "cfg0005_E-0.000_O-bo4/post_relax.xyz",
      "exists_relative_to_readout": false,
      "exists_relative_to_stage8": true
    },
    {
      "rel": "cfg0007_E-0.000_O-bo4/post_relax.xyz",
      "exists_relative_to_readout": false,
      "exists_relative_to_stage8": true
    }
  ],
  "eos_stop": {
    "skip_eos": false,
    "stage10": null,
    "electronic_target_count": 3,
    "decision": "EOS 필요 — F_B: |P| 2.50 > 2.0 GPa · F_P: |P| 2.50 > 2.0 GPa · F_free: |P| 2.50 > 2.0 GPa (고르기 안 함 · 그 셀만 EOS — 다음 판)"
  },
  "kprobe_output_hash_tamper": {
    "accepted": true
  },
  "sp_interpretation_tamper": {
    "accepted": true
  },
  "source_sha256": "559f0152b8774b022c1ae53a9db7ebf52569c191182127dd42af59369a59c60a"
}{
  "electron_count_changed": {
    "nelec": 595.0,
    "problems": [],
    "accepted": true
  },
  "electron_count_missing": {
    "nelec": null,
    "problems": [],
    "accepted": true
  },
  "free_46000": {
    "rc": 0,
    "stdout": "[TEST]   VRAM 여유 46000 MiB (문턱 45000)\nWOULD_START_JOB",
    "stderr": ""
  },
  "free_44000": {
    "rc": 0,
    "stdout": "[TEST] ⛔ VRAM 여유 44000 MiB < MIN_FREE_MIB=45000 — **이 잡이 물러난다**.\n   남의 잡을 죽이지 않으려고 시작하지 않는다. 남은 점은 던지지 않았다.\n   먼저 돌던 계산이 끝난 뒤 같은 명령으로 이어 돌리면 끝난 점은 건너뛴다.",
    "stderr": ""
  },
  "query_failed": {
    "rc": 0,
    "stdout": "[TEST]   VRAM 여유  MiB (문턱 45000)\nWOULD_START_JOB",
    "stderr": ""
  },
  "rerun_disagreement": {
    "analyzer_problems": [
      "ecutwfc 40.0 ≠ 52.0"
    ],
    "rc": 0,
    "stdout": "fc_ok_rc=0",
    "stderr": ""
  }
}
