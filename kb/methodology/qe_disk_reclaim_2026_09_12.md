---
title: "QE 디스크 회수 절차 — 파동함수는 스크래치, 정본은 텍스트 (kgy 2026-09-12, 306 GB)"
date: 2026-09-12
updated: 2026-09-12
tags: [ops, disk, qe, kgy, gabia, neb, reclaim]
status: 채택
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-12
verifiedBy: self   # 문서가 기록한 실행 그 자체(kgy 306 GB 회수). 재검증한 것이 아니라 스키마가 요구하는 짝을 채웠다
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: single-source
---

# QE 디스크 회수 절차

kgy 가 **95 % (남은 50 GB)** 로 찼다. 한 번에 **305.7 GB** 를 되찾았고
(793G → 487G · 남은 383 GB · 57 %), 결과값은 하나도 안 잃었다.
같은 일이 gabia·KISTI 에서도 생기므로 **순서**를 남긴다.

## 1. 왜 찼나 — 숫자가 먼저

| 종류 | 개수 | 크기 |
|---|---|---|
| `.save` 안 수집본 (`wfc*.dat`) | 3394 | **384 GB** |
| outdir 스크래치 (`*.wfc[0-9]+`) | 74 | 163 GB |
| `charge-density.dat` | 184 | 11.5 GB |

⚠ **큰 파일 top 25 를 보고 판단하면 틀린다.** top 25 는 전부 `tmp/*.wfc1`
(스크래치)이었지만 **합계는 `.save` 쪽이 2.4배**였다. 종류별 합계를 따로 세라.

## 2. 무엇이 지워도 되는가 — 세 등급

- **버린다: 파동함수.** QE 는 계산 중 k점 파동함수를 `outdir/tmp/<prefix>.wfc1` 로
  흘리고, `wf_collect` 로 `<prefix>.save/wfc*.dat` 에 모은다. 둘 다 **재시작·후처리
  (projwfc PDOS · pp.x ELF)** 에만 쓰인다.
- **남긴다: `charge-density.dat` + `data-file-schema.xml`.** 이게 있으면 nscf 를
  전하밀도에서 **다시 돌릴 수 있다** — 즉 파동함수 삭제는 되돌릴 길이 있는 삭제다.
  밴드갭 규율상 fixed-occupations nscf 가 유일한 인정 경로라 이 둘은 손대지 않는다.
- **절대 안 건드린다: `.out` · NEB `.dat`/`.int`/`.path`/`.axsf` · 도는 잡의 outdir.**

## 3. 순서 (이 순서를 바꾸지 않는다)

1. **도는 잡을 먼저 찍는다** — `pgrep -af "pw.x|neb.x|melt_quench|disorder_ensemble"`.
   ⛔ **잡 상태를 프로세스로도, 로그 꼬리로도 판정하지 마라 — 산출물 mtime 으로 판정한다.**
   2026-09-12 에 같은 잡을 **두 번 연달아 잘못 읽었다**:
   · ① `run_gap_nscf_gabia.sh` 래퍼(pid 2400966)가 살아 있어 **"돌고 있다"** 고 했다.
     `pw.x` 는 없었는데 래퍼만 보고 판단했다.
   · ② 로그 꼬리가 `nscf_dos 완료` → `Terminated` 라 **"2일 전에 죽었다"** 고 정정했다.
     역시 틀렸다.
   · 실제: 출력 디렉터리에 `projwfc.out`(2.9 MB)과 `.pdos.pdos_*` 가 **19:14 에** 있었다.
     nscf_dos 18:50 → projwfc 19:14 → 그 **뒤에** SIGTERM. 즉 **일을 다 끝낸 잡**이고,
     결과는 이미 `db/properties/ndo_lpscl16_n5fu_pdos.csv`(5260행, 09-10 커밋)로 회수돼 있었다.
   → `Terminated` 는 **실패의 증거가 아니다**. 산출물 파일 목록과 시각이 증거다.
     그리고 이렇게 끝난 잡은 파동함수를 지워도 된다 — 정본이 이미 우리 쪽에 있다.
2. **정본이 무엇인지 원장에서 확인한다.** 지우기 전에 `db/properties/` 를 본다.
   · `lpsocl_dos_gap.json` → `data_source` 가 `01_relax_v0.out`·`03b_nscf_gap.out`·
     `lpsocl_v0_gap.txt` = **텍스트**. 값(2.2309 eV)은 레지스트리에 있다 → 파동함수 불필요.
   · `vgcf_hbn_neb.json` → 7개 장벽·방법·수렴이 전부 등록돼 있다 → 마찬가지.
   원장에 값이 없으면 **먼저 등록하고** 지운다.
3. **완료 여부를 출력에서 확인한다.** scf/nscf 는 `JOB DONE`, NEB 는
   `neb: convergence achieved` + `activation energy`. 미완이면 그 런은 건너뛴다
   (재시작에 파동함수가 필요하다).
4. **파동함수만 지운다.**
   ```
   find <루트> \( -path '*.save/wfc*' -o -regex '.*\.wfc[0-9]+' \) -type f -delete
   ```
5. **정본이 남았는지 되확인한다** — `.dat`/`.int` 목록 · `charge-density.dat` 개수 ·
   `grep "activation energy"` 가 여전히 읽히는지. 확인 전에는 끝난 게 아니다.

## 4. 실측 (kgy 2026-09-12)

| 대상 | 회수 | 근거 |
|---|---|---|
| `work/lpsocl_v0/tmp/lpsocl_v0.wfc1` | 14.6 GB | 정본 = `.out`, 값 등록됨, 3×3×1 캠페인 2026-09-11 닫힘 |
| `work/lpsocl_v0/tmp/lpsocl_v0.save/wfc*` | 13.6 GB | 같음. charge-density 보존 |
| `work/vgcf_hbn` 전체 (913 파일) | **305.7 GB** | NEB 7개 전부 수렴 · 값 `vgcf_hbn_neb.json` 에 등록 |

남겨둔 것(회수량이 작고 정본 위치가 불확실): `Yonghoon-DEM-DFT/tmp` d0~d6 `.save` 12 GB ·
`work/li3n_dft`+`li3n_eads` 15 GB (`JOB DONE` 6개는 확인했으나 값 등록 위치 미확인).
`work/runs/nd_scf_2026_09_08` 의 파동함수도 이제 지울 수 있다(위 §3.1 — projwfc 완료·PDOS 회수
완료). 383 GB 가 남아서 하지 않았다 — **필요 없을 때 지우지 않는 것도 규율이다.**

## 5. 안 한 것 · 하지 말 것

- **`.cache` 를 지우지 않았다** — 그때 modelc 9런의 torch inductor 컴파일 워커가 쓰고 있었다.
  MLIP MD 가 도는 중에는 `.cache`(inductor·huggingface)를 건드리지 않는다.
- **`charge-density.dat` 11.5 GB 를 남겼다** — 아끼려고 nscf 를 다시 돌릴 이유가 없다.
- **도구로 만들지 않았다.** 판단(정본이 뭔지·끝났는지)이 매번 다르고, 자동화하면
  그 판단이 생략된다. 이건 스크립트가 아니라 **절차**다.

## 6. 예방 — `disk_io='low'` 는 이것을 막지 못한다 (2026-09-12 실측)

우리 QE 입력 생성기 10곳이 이미 `disk_io='low'` 를 쓴다 — `tools/vgcf_hbn/make_qe_inputs.py`
포함. **그런데 그 vgcf_hbn 이 305.7 GB 를 쌓았다.** 즉 `'low'` 는 런 중 스크래치를 줄일 뿐,
끝에 수집본을 `.save` 에 쓴다. "디스크 아끼는 설정" 으로 믿고 있었던 것이 실제로는
384 GB 를 막아주지 못했다.

- 파동함수가 **뒤에 필요 없는 런**(relax · 에너지/힘만 보는 scf · EOS 점)은
  `disk_io='nowf'` 가 맞다 — 전하밀도는 쓰고 파동함수는 안 쓴다.
- **PDOS 용 nscf 는 예외**다: projwfc 가 `.save` 의 파동함수를 읽는다. 남기고,
  **후처리·회수가 끝나면 지운다**(§3.1 의 nd_scf 가 그 예).
- ⚠ `'nowf'` 의 정확한 동작은 **그 기계의 QE 판에서 한 런으로 확인**한다. 기억으로 바꾸지 않는다
  (kgy: QE 7.4.1-GPU). 확인 전에는 생성기를 일괄 개서하지 않는다.

## 반론

- *"`.save` 를 통째로 지우면 더 빠르다"* — 맞지만 `charge-density.dat` 과 스키마가 같이
  날아가고, 그러면 후처리가 필요해질 때 **scf 부터** 다시다. 파동함수만 지우면 nscf 만 다시다.
- *"top 25 만 보면 충분하다"* — 위 §1 이 반례다. 이번엔 종류별 합계가 2.4배 뒤집혔다.
- *"수렴했으면 `.out` 도 필요 없다"* — 아니다. 우리 규율에서 밴드갭·장벽의 **인정 경로가
  `.out` 의 고유값·에너지**다. `.out` 은 정본이다.

## ⏩ 2026-11-09 — kgy 두 번째 회수 (236.7 GB · 89 → 64 %)

- 같은 절차를 **판단은 기록 파일에, 기계 판정은 블록에** 나눠 했다 — `db/properties/kgy_disk_reclaim_2026_11_09.json` (소유 범위 · 원장 닫힘 목록 · 제외) + `db/inputs/kgy_disk_reclaim_2026_11_09/reclaim_wfc.py` (단위마다 짝 QE 출력의 JOB DONE · 미수렴 표지 · NEB 수렴 · 도는 잡 cwd/열린 파일/명령줄 · 24 h · 링크 · 지운 뒤 남길 파일 재확인 · DRY=1). 가짜 홈 18 경우로 먼저 시험했다.
- ⛔ **kgy 는 공유 기계다 — 지울 범위는 사용자가 정한다** (11-09: *'내꺼에 대한것만'* → `~/work` 전체 (bml = 사용자 랩 폴더) + 저장소 사본). 홈의 다른 폴더는 이름으로 판단하지 않는다.
- 결과: bml 의 162 GB 는 **한 폴더 (`comp2v2_dft_0K`) 의 파동함수**였다 · 판독 전 캠페인 (CEI) 은 제외 · 짝 폴더에 미완 출력이 하나라도 있으면 그 단위는 통째로 건너뛴다 (li3n 14.5 GB 가 그렇게 남았다).
