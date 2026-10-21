# Rint ② 사슬 · 배선 통합 — D 를 이어받기 (이름 `D2` · 10-21)

앞 에이전트 D 가 기록이 너무 길어져 다시 띄울 수 없게 됐다.  너는 D 의 일을 **그 자리에서 이어받는다**.

## 먼저 읽을 것
1. `scratchpad/rca_common.md` — 공통 규칙.
2. `scratchpad/rca_D_BRIEF.md` — D 의 원래 지시.
3. `scratchpad/rcaD/D_report_0836.md` — D 의 마지막 전체 보고 (커밋 10 개 · 반례 값 · 코디네이터 항목 1–7 · §4 4 판 사슬 규칙 · §6 웹앱 문구 제안).
4. `scratchpad/rcaD/coord_0852.md` — 코디네이터의 다음 일 1–6.  B 증서 결합 합치기 · 픽스처 패치 · S07 순서 · 회귀 · 커밋 · A 파일 손대지 않기.

## 작업 트리 세우기 (너의 격리 작업 트리에서)
```
git reset --hard 704254ca0
git apply scratchpad/rcaD/wip_dirty_1117.patch      # sha256 e89fdcdd… · D 가 고치던 3 파일
git status --short                                  # M scripts/rint_r_chain.py · run_contract.py · test_ca_ext_b6.py
```
- 기반 = `a76f59d0d`.  D 의 커밋 13 개는 `git log --oneline a76f59d0d..704254ca0` 로 본다.
  - 마지막 셋 = B 의 커밋 둘 cherry-pick (`01729613a` 시험 · `2f83935e4` 구현) + `704254ca0` (사슬 · 상태 계약 결합 · 시험 먼저).
- `scratchpad/rcaD/` 의 스크립트 (`reg_batch2.sh` 등) 는 옛 작업 트리 경로 (…agent-afe53be7bdb176c82) 를 가리킬 수 있다.  네 작업 트리 경로로 바꿔 쓴다.

## 남은 일 (D 가 멈춘 자리 = 09:13 "run_contract (short-branch binding, ionic call, duplicate helper) and the read_run order")
1. 고치던 것을 끝낸다.  `704254ca0` 의 시험 (S07 · 결합 시험) 이 실패하는 것을 먼저 재현하고, 패치를 마무리해 통과시킨다.
   - S07 = `rint_r_chain.read_run` 에서 세대 · ca_ext 기록 검사를 증서 결합 (`next_gen_cert_ok`) 보다 **먼저**.
   - 다른 멈춤 코드 (S06 · S08 · S09 · S12 · S26 · S27 · X09) 는 그대로인지 확인한다.
2. 회귀 (coord_0852 항목 4): chain · e2e · b6 · runner · z1 · z3 · verdict · carbon_junction · target_cert 빠른 판 · conv_cert · step3 selftest 둘 · run_contract selftest · 웹앱 둘 · check_method_discipline.
   - target_cert `--long` 은 4 스레드 탐침 → `HEAVY_EXCLUSIVE=1 bash scratchpad/heavy.sh …`.
   - 끈 경로 비트 대조 (`--expect-identical`) 도 다시.
3. 커밋 (시험 먼저면 둘) → 보고.  보고 = 커밋 · 충돌 · 고치기 전 → 뒤 · 회귀 표 · 끈 경로 대조.

## ⛔ 하지 않을 것
- **[Rint] Q1 (천장 단락 = NOT_COMPUTED) · Q2 (4 판 사슬 규칙 여섯 추가) 는 1저자 답이 아직 없다 — 손대지 않는다.**
  - 지금 동작 (단락 +∞ 게시) 그대로 둔다.
  - 그 결정이 없어 못 닫는 시험 · 경로가 있으면 보고에 적기만 한다.
  - ⚠ 11:26 에 앞 D 에게 "권고대로 따로 커밋" 이라고 보냈던 지시는 **철회**한다.
- A 파일은 고치지 않는다: `carbon_junction.py` · `ca_ext_cjunc.py` 의 A 쪽 · `fibre_segment_raster.py`.  A (다른 에이전트) 가 아직 돈다.  A 가 끝나면 메인이 합치라고 따로 보낸다.
- push · fetch · `scripts/check_all.sh` 안 함.  봉인 32 파일 (`scripts/run_network_194_parallel.py` CODE_FILES) 손대지 않음.  문서에 작업 트리 SHA 를 쓰지 않는다.

## 규칙
- 60 초 넘는 실행은 `bash scratchpad/heavy.sh <명령> > <로그> 2>&1` (길면 run_in_background · 끝날 때까지 기다림).
- ⚠ 지금 (11:3x UTC) 메인 게이트가 무거운 칸 둘을 다 잡고 있다 (12:30–12:45 UTC 쯤까지) — 그동안 1 번 (코드 · 짧은 시험) 을 먼저 한다.
- 디스크 여유 ≈ 4–5 GB — `scratchpad/rcaD/base_b` 같은 풀린 사본은 다 쓴 뒤 지운다.
- 숫자 · 전칭은 실행 출력으로만 (SELF-124).
