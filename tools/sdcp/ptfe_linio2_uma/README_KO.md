# PTFE/LiNiO₂ UMA → VASP 검증 워크플로

이 패키지는 ORCA에서 이완이 끝난 PTFE dimer와 C10을 LiNiO₂(104) 표면에 놓고, **DFT에 넘길 비반응 자세 후보를 줄이는 도구**야.

## 먼저 결론

- UMA 점수는 binding energy가 아니야.
- UMA 1등을 바로 “선호 site”라고 부르면 안 돼.
- dimer와 C10의 점수를 서로 빼거나 크기 수렴으로 해석하면 안 돼.
- 최종 결론은 서로 다른 자세를 VASP+D3로 다시 계산한 뒤에만 내려.

이번 1차 실행은 안전한 범위만 다뤄.

- 192원자 LiNiO₂(104) 슬랩 전체 고정
- PTFE 분자만 이완
- C10은 주기 이미지가 겹치지 않는 면내 축 `15°`, `60°`, `165°`만 사용
- `Li-top`, `Ni-top`, `O-top`, 세 bridge, hollow의 대표 시작 registry 7개
- dimer 63개 + C10 84개 = rigid single-point 147개
- 위치 다양성을 보존해 dimer 8개 + C10 12개 = 이완 20개

따라서 이 결과는 **원셀·고정축·고정슬랩 geometry screen**이야. 7개 점은 표면 대칭 orbit를 전부 증명한 exhaustive site 목록이 아니야. C10의 자유 회전, upright 자세, 표면 이완은 다음 라운드로 분리해.

## 입력 구조

| 모델 | 조성 | 역할 | ORCA 결과 |
|---|---|---|---:|
| dimer | H-(CF₂CF₂)₂-H, C₄H₂F₈ | 저비용 대조군 | -952.346331900971 Eh |
| C10 | CF₃-(CF₂)₈-CF₃, C₁₀F₂₂ | 주 접촉 모델 | -2577.579988053998 Eh |

둘 다 `r2SCAN-3c Opt TightSCF`가 수렴했고 정상 종료했어. 다만 frequency 계산은 안 했으므로 진동학적 최소점까지 확인한 건 아니야.

dimer의 H는 실제 PTFE 사슬에 없는 인공 cap이야. H가 표면 접촉을 주도하면 `CAP_ARTIFACT`로 빼.

## 자동 차단 조건

- 분자-슬랩 원자 충돌 `< 1.5 Å`
- 분자 자기 이미지 거리 `< 4.5 Å`; `4.5–5.0 Å`는 경고
- 수직 이미지 거리 `< 5.0 Å`
- C-F, C-C, C-H 결합 이상 또는 절단
- C-F가 `1.55 Å`를 넘게 늘어나거나 C-Ni/O/Li·F-Ni/O가 반응적으로 짧아진 구조
- 고정한 슬랩 원자가 움직임
- dimer의 인공 H cap이 최근접 접촉
- FIRE 미수렴
- 분자-슬랩 최단거리가 `> 4.0 Å`로 벌어진 detached 구조

이런 구조는 랭킹에서 자동 제외해. C-F 절단이나 F 이동이 보이더라도 “반응 발견”이라고 해석하지 않고 `UMA_UNSUPPORTED_REACTION`으로 격리해.

## 실행 순서

Gabia 명령은 [GABIA_COMMANDS_KO.md](GABIA_COMMANDS_KO.md)에 그대로 붙여넣을 수 있게 적어뒀어.

1. `check`: 파일 해시, Python/ASE/fairchem, GPU, `pw.x` 동시 실행 여부 확인
2. `pilot`: dimer 1개와 C10 1개만 계산
3. pilot 로그와 `PILOT.json` 회수·검토
4. `screen`: rigid 147개 → 다양성 보존 shortlist 20개 이완
5. `RESULTS.md`, CSV, 구조쌍을 회수

중단됐다가 같은 명령을 다시 실행하면 완료된 JSON record를 건너뛰고 이어가.

## 결과 읽는 법

- `pose_score_eV`: 같은 분자·같은 model/task 안에서만 쓰는 내부 정렬 점수
- `initial_site`: 계산을 시작한 위치
- `registry_signature`: 이완 뒤 F가 Li/Ni와 만든 다중 접촉 요약
- `nearest_cation`: 이완 뒤 가장 가까운 F-양이온 쌍의 양이온
- `ranking_eligible`: 이미지·결합·수렴 gate를 모두 통과했는지
- `DFT_HANDOFF.json/csv`: 이완한 20개 중 gate를 통과한 후보 전부와 같은 azimuth/roll의 Li-top/Ni-top rigid counterfactual 쌍

`pose_score_eV`가 0.05 eV 안에 모이면 최소한 중복 후보를 묶는 heuristic으로만 써. 0.05 eV 밖이라고 UMA가 구분해 냈다는 뜻은 아니야. 가장 낮은 하나만 고르지 말고 구조 basin 다양성과 head 간 불일치를 우선해 DFT-D3로 넘겨야 해.

`DFT_HANDOFF/`의 XYZ/POSCAR는 VASP 준비용 구조쌍이야. POSCAR 종 순서는 `Li Ni O C F H`이고, UMA 때의 “슬랩 192개 전부 고정”을 그대로 승계하지 않아. DFT 비교용으로 슬랩 아래 절반만 고정하고 위 절반+PTFE를 풀어 둔 Selective Dynamics mask를 새로 쓴다. 정확한 고정 원자 수·z-cut·재정렬 뒤 최근접 Li/Ni/F의 VASP 1-based index가 manifest에 들어가. 그래도 실행 전 사람이 구조와 mask를 눈으로 확인해야 해.

자동 basin 라벨은 contact count·거리·chain 방향·높이와 1×4 병진을 고려한 원자별 주기 RMSD `≤0.75 Å`를 쓰는 **진단용 proxy**야. 이 라벨로 후보를 버리지는 않고 gate를 통과한 이완 후보를 전부 넘겨. 대칭 등가 구조를 서로 다르게 세거나 다른 구조를 합칠 수 있으므로, 물리적으로 독립인 basin 수는 구조를 직접 보고 다시 합치거나 확정해.

## VASP 검증 단계

UMA screen 뒤의 VASP 단계도 이 패키지에 구현돼 있어. [VASP_README_KO.md](VASP_README_KO.md)에
입력 규약, pilot 18개 template, full-eligible일 때 전체 54개 template, 실행기,
dense-k 선택, 반환법을 적었어.
가짜 산출물로 확인한 통과·차단 회귀시험은 [RELEASE_VALIDATION.md](RELEASE_VALIDATION.md)에
따로 적었고, 실제 계산 결과와 섞지 않았어.

```bash
./run.sh vasp-pilot
# pilot 외주 결과를 검토한 뒤
./run.sh vasp-all
```

전체판은 이완 후보 20개 중 geometry gate를 통과한 후보 전부와 matched Li/Ni
counterfactual 4개를 보존하고, 각
surface 구조를 `afm_balanced`와 `afm_net2`에서 독립 이완해. clean slab와 VASP-D3
gas fragment도 같은 기준으로 계산하므로 다음 식을 실제로 만들 수 있어.

```text
E_ads = E_complex - E_clean_slab - E_fragment
DeltaE_sampled(Ni-Li) = min E_Ni-contact - min E_Li-contact
DeltaE_matched-start(Ni-Li) = min E_Ni-start - min E_Li-start
```

site는 시작 라벨로 판정하지 않고 최종 DFT `CONTCAR`의 multi-F/nearest-F registry로 다시
분류해. Li/Ni 목표 registry가 유지되지 않으면 자동 차단하고, coarse `2x3x1` 뒤 경쟁 후보를
`3x4x1`로 다시 계산해. 다만 수치 통과 뒤에도 Ni occupation/local moment의 수동
감사는 필요하고, U·dispersion 민감도를 하지 않으면 `U=6.2/D3` 규약 조건부 결론이야.

추가적인 C10 자유 회전과 coverage 민감도에는 짧은 셀 축 2배 확장 screen이 필요해.
같은 rigid atlas의 다른 UMA head를 쓸 때도 head별 후보 합집합을 보존해야 해.

Gabia A6000은 UMA 후보 검색에는 적합하지만, 206/224원자 LiNiO₂ 복합체 QE-DFT에는 메모리가 빠듯해. DFT는 KISTI나 외주 VASP로 보내는 게 맞아.
