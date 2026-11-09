---
title: "DW 프롬프트 — 셀구축 v1.1 · b2o3 B·O 배치 카드 개정 1 v1.1: DV 1 단계 해제조건 네 묶음 + 후속 단계 조건 확인 (계산 0 건)"
date: 2026-11-09
updated: 2026-11-09
tags: [review, b2o3, cell-construction, uma, phonon, framework, codex, prompt, letter]
letter: DW
track: b2o3
channel: codex
kind: prompt
status: 발송 전 · 기준 커밋은 이 프롬프트를 담은 커밋 (아래 '보내는 글' 의 범위 줄) · 앞 편지 DV (NO-GO)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = b2o3 UMA-MD / B₂O₃ 계산 쪽 (1저자 = 사용자). ⛔ b2o3 전도도 (D · Ea · σ) 값은 싣지 않는다 (08-25 마감 · 인용 불가).
> ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_DW_reply_cell_construction_v1_1_release_2026_11_09.md` 로 원문 보존.

---

**[b2o3 · 셀구축 v1.1] DV 해제조건 확인 — 1 단계 (UMA) GO 여부 (계산 0 건)**

## 0. 무엇을 묻나

DV 회신 (`kb/reviews/codex_DV_reply_cell_construction_v1_1_2026_11_09.md` · 기준 ad4f41b8) 은 NO-GO 와 함께 1 단계 해제조건 네 묶음을 줬다 — ① 큐 실패 전파 ② 실물 결속 (완료 구조 · 대기 뒤 입력) ③ 생성 짝 검증 ④ 판독기 + 음성시험 → 유효 개정 비준. 포논 빈 캐시 · B 결합 분류는 각 후속 단계 전 조건.

범위 `ad4f41b8..<이 편지의 커밋>` — 커밋 다섯 (DV 원문 보존 · 큐/결속 · 생성 짝 · 판독기 · 후속 단계 조건). 생산 UMA · DFT · MD 는 안 돌았다.

**묻는 것**: 네 묶음이 닫혔나 → 1 단계 (생성 → UMA 이완 거름 → 연속 파일럿 → 어닐 → 판독) 를 사용자 비준 뒤 시작해도 되나 (GO / 조건부 GO / NO-GO). 포논 · 골격 MD 전 조건 둘도 닫혔나.

## 1. 묶음별 고침 (DV 항목 → 어디)

| DV | 고침 | 시험 · 깨기 |
|---|---|---|
| P1-1 큐 실패 전파 | `db/inputs/ndo_site_2026_10_14/run_uma_kgy.sh` `write_queue` — 명령 바로 뒤 `run_rc` · `check_rc` 저장 · 로그 · 종료 (실행 실패 → 그 rc · 검사만 실패 → 13). `echo "$(date …) rc=$?"` 가 date 의 종료코드를 찍는 것을 여기 bash 5.2 에서도 재현 | `--selftest` (모의 python · 가짜 nvidia-smi) 네 경우 + 입력 바뀜 = 5/5 · 발사 전 ③ 에서 돈다 · 깨기 3/3 |
| P2 대기 뒤 입력 | 제출 때 입력 · `run_anneal.py` · `_provenance.py` sha256 목록 → 대기 뒤 `sha256sum -c` (바뀌면 12 · 실행 0 회) | 위 selftest 의 다섯째 |
| P1-2 완료 구조 결속 | `tools/doping/run_anneal.py` — 완료 기록에 `outputs` (post_md · post_relax 의 상대 경로 · sha256) · `composition` · `verify_outputs()` (존재 · sha256 · 판독 · 원자 수 · 조성) 를 재개 생략과 `--check_results` 가 같이 씀 · 불일치면 멈춤 (`--rerun_mismatched` 로만 재실행) | Codex 두 반례 (다른 조성으로 교체 · 삭제) · 깨기 3/3 |
| P2 Windows md.log | `dyn.close()` · `opt.close()` 를 finally 에서 | (Linux 에서 열린 파일 없음 확인 · Windows 는 안 돌려 봄) |
| P2 생성 짝 | `tools/doping/b2o3_enumerate.py::verify_manifest` — 자식 = 부모 + 기록한 S→O 자리만 (원자 수 · 셀 · 좌표 1e-3 Å · 원소) · `li_candidates.json` 해시 · 후보 수 | 40/40 · Codex 반례 (다른 부모의 자식 · 해시 · O 자리 맞춤) · 보고서 삭제/변경 · 깨기 2/2 · 135 세트 다시 통과 |
| 묶음 4 판독기 · P2 G3/끝 꼴 · Q5 넷 | 새 `tools/doping/b2o3_bo_readout.py` (screen · extract · pilot · anneal · eos) + 카드 `개정_1_셀구축_v1_2026_11_09.판독_계약` (기계_판독_값을 selftest 가 도구 CONTRACT 와 대조) | 21/21 · 깨기 7/7 (G3 분모 · 승자 기준 · G1 보류 · 파일럿 옛 규칙 · EOS 공통 B · 회색 띠 · 결속) |
| P2 옛 k 재개 참조 | 개정 1 결정 `reopen_criteria` → 개정 1 v1.1 의 9_DFT ② | — |
| P3 두 문구 | '선택된 t_a 보다 긴 결과를 제외' (절차 7 · 카드 7) · 비용표 k 탐침 3 | — |
| P1-3 포논 빈 캐시 (포논 전) | `tools/electronic/uma_phonon.py` — 빈 캐시로 시작하면 정체성 새로 씀 | Codex 순서 (안장점 A → 캐시 비움 → 최소점 B → A) = 멈춤 · 깨기 1/1 |
| P1-4 B 결합 분류 (골격 MD 전) | `tools/ionic/framework_site_census.py` v2 — frame 0 가장 가까운 중심 (P ∪ B) 의 결합 음이온 · B–S/B–O 문턱 = P 와 같음 [제안] · `census_rules` 판 표시 | BS₃ 강체 회전 사건 0 (PS₃ 0) · B–S 이탈 B-bonded 1 · 깨기 1/1 |
| P2 신·구 census 섞기 | 판이 섞인 집계는 멈춤 · 옛 판만이면 B 묶음 '미측정' | 섞기 시험 · 깨기 1/1 · 09-26 v1 재집계 완전히 같음 (원궤적 재판독 아님 — DV 지적대로 그 뜻을 넓히지 않는다) |

## 2. 판독 계약 (카드 · 결과 전)

- 성공 = converged + `verify_outputs` 통과.
- 끝 꼴: O 마다 B · P 까지 < 1.8 Å 결합 · 결합 둘 이상 = 가교 · 결합 0 이고 1.8–2.3 Å = 미분류 · ≥ 2.3 Å = 자유 → 구조 F_B / F_P / F_free / mixed / unclassified. **이완된 끝 구조에서만** (시작 구조는 O 가 S 자리 그대로라 F_B · F_P 가 미분류로 나온다 — 135 세트 실측).
- G1 성공 ≥ ceil(5M/6) · G2 조성 같음 · G3 분모 = 그 가족 성공 수 · 분자 = 끝 꼴 ≠ 시작 가족 (mixed · 미분류 포함) · > 1/3 (엄격) 이면 '섞임' 표지 (판정은 막지 않음).
- 승자 = 최저 − 차저 ≥ 0.20 eV/B₂O₃ · 보류 = G1 탈락 · 성공 0 가족 · 가족 최저 구조 미분류 · G2 실패 (하나라도) · 짝 = 세 가족 모두 성공한 바탕 · n < 3 이면 짝 서술 보류 · ≥ ceil(5/6 · n) 같은 부호면 '짝으로도 같은 방향'.
- 파일럿: 6 단계 성공 전체 최저 → `run_anneal --time_ps 100` 한 연속 궤적 → `extract` 로 20 · 50 · 100 ps 프레임 (궤적 sha256 · 프레임 번호) → 셋 다 이완 → 셋 다 성공 · 유한 · 이완 입력 = 스냅숏 (sha256) · 끝 꼴 분류여야 판정 (아니면 '파일럿 미완료') · max − min ≤ 0.05 이고 끝 꼴 같으면 20 ps 아니면 100 ps.
- EOS 생략: 가족마다 B 를 21.7 · 32.5 GPa 로 **독립** 2³ 조합 모두에서 순서 · 0.10 판정이 같고 모든 |P| ≤ 2 GPa 일 때만.
- 서술 한계 (DV Q3 · Q4): '선언한 초기점 생성 · 탐색 절차에서 얻은 결과' · 띠틈은 '승자 가족에서 선택한 대표 구조의 띠틈' 까지 · 부모 · 자식 해시와 역할.

## 3. 관측창 (DV Q7)

전역 규칙 개정안을 **proposed** 로 넣었다 — `D-2026-11-09-md-observation-window-amend1` (봉인 원문 보존 · 새 개정이 '그보다 높은 장벽은 원래 못 본다' 를 대체): Ea₁ = kT·ln(ν₀tn) 은 기대 사건 1 (63.2 %) · 95 % = kT·ln(ν₀tn/3) · 예 1000 K · 0.8 ns: 0.77446 / 0.67991 eV · +0.10 eV 도 26.9 %. 비준 전에는 도구 줄 (`tools/sei/collect_neb.py::observation_window`) · CLAUDE.md 문구를 안 바꾼다.

## 4. 질문

- **Q1** DV 묶음 1–4 가 닫혔나 — 같은 반례 (큐 exit 7/1 · 결과 교체 · 삭제 · 다른 부모의 자식 · li_candidates 삭제 · G3 2/5 대 2/6 · 승자 0.01 · 파일럿 0 / −0.30 / −0.02 · EOS 독립 B) 로.
- **Q2** 판독 계약에 남은 빈칸 (끝 꼴 문턱 1.8 / 2.3 Å · 가교 처리 · 보류 넷 · 짝 n < 3) 이 있나? 결과 전에 닫아야 할 게 더 있나?
- **Q3** 포논 빈 캐시 · B 결합 분류 (v2 · B 문턱 = P 와 같음 [제안]) 가 포논 · 골격 MD 전 조건으로 충분한가?
- **Q4** 관측창 개정안 문구가 권고와 맞나?

## 5. 회신 형식

GO / 조건부 GO / NO-GO 한 줄 → P0–P3 (파일:줄 · 재현 · 최소 수정) → Q1–Q4 → 1 단계 시작 전 마지막 확인 목록.
