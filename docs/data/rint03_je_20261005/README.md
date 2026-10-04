# RINT-03 실침대 측정 — 입자별 AM 전류 옛 정의 ↔ `am-final-sid-v2` (kgy · 2026-10-05)

원장 `RINT-03` (claimed_fixed `f1f92d009`) 의 "선언된 예외" — r 를 끈 산출에서도 입자별 AM 전류 (je) 가 바뀐다 — 의 **크기**를 실제 침대에서 잰 기록.
해석 · 표 · 한정어의 정본은 Codex 요청서 `docs/reviews/codex_rint_g1_lhs_network_request_20261004.md` §1-2 다 (이 README 는 원자료 · 출처 기록).

## 무엇을 · 어디서

| 태그 | 침대 | 그리드 (kgy · `step4_grid.npz`) |
|---|---|---|
| vgcf4 | VGCF 4 wt% · PTFE 1 wt% (`pa100` 디렉터리 킷) | `~/pa100/kits/VGCF_PTFE_4_1/run_VGCF4_PTFE1_20260927_022040_2903748/` |
| vgcf1 | VGCF 1 wt% · PTFE 1 wt% (`pa100` 디렉터리 킷) | `~/pa100/kits/VGCF_PTFE_1_1/run_VGCF1_PTFE1_20260926_235839_2877079/` |
| fig | ps45 5:5 (`kit_ps_5_5_r45` = 웹앱 `260925_000513_123978` · AM 198 + 2,293 = 2,491 · SE 158,766 · 킷 입력에 첨가제 항목 없음) | `~/mpm_fig_wt/kit_260925_000513_123978/run_fig_20261001_164534/` |

- 그리드 = payload 가 옛 je 를 계산한 **바로 그 배열** (`mpm_webapp_payload.py` 의 `per_particle_current(_res3, sid3, pid3, _sig3, …)` 와 `--save-step4-grid` 저장이 같은 sid3 · pid3 · σ_e 표 · z_top).
- 도구 = `scripts/rint03_je_compare.py` blob `73a9bf88f5dd3e1055ccad7e99e2a3d4667a36f9` (`23c3e32be` 에서 만든 판 — `92dfc0517` 까지 무변경 · kgy 임시 워크트리 = 실행 직전 브랜치 끝).
  ⚠ 이 판은 수렴 정보를 JSON 에 싣지 않았다 (`SELF-85`) — 아래 로그 줄이 수렴 증거다.  고친 판은 계약을 못 채우면 `status: UNCONVERGED` 를 낸다.

## 실행 (1저자 · kgy · conda `uma` · 2026-10-05 04:34 KST 시작)

```bash
cd ~/dem-vgcfE && git fetch origin claude/sdcp-dem-manuscript-si-pqwtv8
[ -d /tmp/rint03_wt ] || git worktree add --detach /tmp/rint03_wt FETCH_HEAD     # 원 체크아웃 HEAD 는 그대로
cd /tmp/rint03_wt
G1=~/pa100/kits/VGCF_PTFE_4_1/run_VGCF4_PTFE1_20260927_022040_2903748/step4_grid.npz
G2=~/pa100/kits/VGCF_PTFE_1_1/run_VGCF1_PTFE1_20260926_235839_2877079/step4_grid.npz
G3=~/mpm_fig_wt/kit_260925_000513_123978/run_fig_20261001_164534/step4_grid.npz
nohup sh -c "python3 -u scripts/rint03_je_compare.py $G1 --json ~/rint03_je_vgcf4.json > ~/rint03_je_vgcf4.log 2>&1; \
             python3 -u scripts/rint03_je_compare.py $G2 --json ~/rint03_je_vgcf1.json > ~/rint03_je_vgcf1.log 2>&1; \
             python3 -u scripts/rint03_je_compare.py $G3 --json ~/rint03_je_fig.json   > ~/rint03_je_fig.log   2>&1" &
```

- 소요 (CPU Jacobi-CG · 같은 해 한 번): vgcf4 ≈ 8 분 (3,589,135 dof · JSON 04:42) · vgcf1 > 30 분 (2,724,342 dof · 05:12 에 아직 CG 중 — 탄소가 드문드문해 수렴이 느린 것으로 보인다 · 추정) · fig 그 뒤 (끝 시각 미기록).

## 수렴 증거 (1저자 붙여 넣기 · `grep -H 'STEP3 solve\|not converged' ~/rint03_je_*.log`)

```
/home/kgy/rint03_je_fig.log:    STEP3 solve: 2,297,784 dof, plate contacts 1,327/3,114 — CG running (CPU, 수 분 소요 가능)…
/home/kgy/rint03_je_vgcf1.log:    STEP3 solve: 2,724,342 dof, plate contacts 3,503/3,981 — CG running (CPU, 수 분 소요 가능)…
/home/kgy/rint03_je_vgcf4.log:    STEP3 solve: 3,589,135 dof, plate contacts 5,962/5,527 — CG running (CPU, 수 분 소요 가능)…
```

`⚠ STEP3 CG not converged (info=…, resid=…) — σ UNRELIABLE` 줄 (`step3_sigma.solve_sigma_z` 가 info ≠ 0 또는 resid > 1e-6 이면 찍는다) 이 세 로그 어디에도 없다.

## 파일

| 파일 | 내용 |
|---|---|
| `rint03_je_vgcf4.json` · `rint03_je_vgcf1.json` · `rint03_je_fig.json` | 도구 `--json` 출력 (행 목록 · 한 행씩).  1저자가 `cat` 으로 붙여 넣은 텍스트 — 원본은 끝 개행이 없고 리포 사본은 하나 붙었다.  `json.dumps(…, ensure_ascii=False, indent=1)` 재직렬화가 붙여 넣은 텍스트와 글자 단위로 같다 (붙여 넣기 손상 없음) |

## 요약 (정본 = 요청서 §1-2)

| 태그 | 오염 입자 | AM 번호를 단 비-AM 셀 | 옛 je 질량 중 비-AM 셀 몫 | 옛/새 비 중앙 · p90 · 최대 | Spearman | top 10 % 겹침 |
|---|---|---|---|---|---|---|
| vgcf4 | 1,498 / 1,498 | 93,352 | 97.4 % | 42.6 · 91.9 · 204 | 0.270 | 14 % |
| vgcf1 | 1,497 / 1,498 | 26,649 | 6.4 % | 1.05 · 1.22 · 27.3 | 0.954 | 91 % |
| fig | 0 / 2,491 | 0 | 0 % | 1 · 1 · 1 | 1.000 | 100 % |

⚠ 한정어: vox 0.4 격자의 값 (탄소 셀 폭 = vox → 오염 크기는 격자 의존) · 재풀이 σ_e (JSON `sigma_e_eff_S_cm`) 는 검산값이지 인용값이 아니다 (CL-24) ·
`n_carbon_cells_with_am_pid` 는 이름과 달리 AM 번호를 단 비-AM 셀 **전부** (PTFE 포함 · 전류는 도체만 나른다).
