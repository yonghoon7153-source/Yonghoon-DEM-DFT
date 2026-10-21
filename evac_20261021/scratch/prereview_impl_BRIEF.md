# 사전 리뷰 — 구현 쪽 (이름 `impl`)

먼저 `prereview_common.md` (같은 폴더) 를 읽는다.

## 볼 것 (코드 · 시험)
- `scripts/carbon_junction.py` · `scripts/ca_ext_cjunc.py` · `scripts/fibre_segment_raster.py` (접합 켤 때 경로) · `scripts/step3_sigma.py` (접합 훅 · face_alpha 조합 · 극한 R_j ∞ / 0 · 수렴 증서 · 게시 경로) · `scripts/step3_conv_cert.py` (A/B/C + 새 목표량 증서) · `scripts/run_contract.py` (증서 · ca_ext 칸 · `ca_ext_record_ok`) · `scripts/ca_s0_census.py` · `scripts/rint_r_chain.py` · 러너 (`scripts/sdcp_gain_vox015_8arm.sh` 와 그 payload 입구) · 웹앱 표지 (`webapp/test_ca_ext_labels.py` 가 보는 것) · 각 시험 파일.

## 꼭 볼 보장 (최소 — 더 찾으면 더)
1. RCA-03 — 같은 섬유가 셀을 다시 지날 때 branch 마다 따로 (`(cell, fid, branch)`) · 같은 셀 다른 branch 는 융합하지 않음 · 판정문 폴리라인 반례 5 Ω (옛 2 Ω).  옆 자리: 3 번 이상 재방문 · 셀 경계 위 꼭짓점 · 0 길이 선분 · 닫힌 고리 · 주기 경계를 넘는 섬유.
2. RCA-04 — 포트 규칙이 경로 반전 · 꼭짓점 순서 · 섬유 번호 순열에 무관.  옆 자리: 동률이 셋 이상 · 끝점이 셀 꼭짓점에 정확히 놓임.
3. RCA-05 — 긴 접촉 = 분산 (v0) · 판정문 1.366013071895 / 5 / 0.238095238095 S 꼴이 설계 값대로.  옆 자리: L_c/L_par 경계 (= 1 · 1 ± ε) · 매우 긴 접촉 · 접촉 두 개가 겹침.
4. RCA-06 — SV 지배 가드 = 진단 + 반사실 대조 · 판정문 90.49773756 % · P_SV 4.5351473923e-5 < P_VV 1e-4 꼴에서 이제 무엇이 나오나 · 우회 경로 (판정문 꼴의 변형) 로 가드를 다시 놓치게 할 수 있나.
5. RCA-07 · 13 — 목표량 증서: U (에너지 상한) ≥ G ≥ 1/R_q (Thomson 하한) 이 **정확히** 성립하는가 (부동소수 반올림이 부등호를 뒤집는 꼴 · 대비 1e12 이상 · 거의 0 인 g · 막다른 노드 · 전 자유도 한 관통 성분) · 게시 G 가 구간 밖 / 폭이 문턱 위면 거부하나 · VALID_ZERO_TOPOLOGY ↔ POSITIVE_SOLVED 분리 · 두 BLAS 경로 (기본 · Haswell) 에서 판정이 같은가.
6. Z3 조합 — α 먼저 (α = 0 면 `_keep` 압축) → 접합이 VV 면을 끊음 (α 면제) → 접합 간선에 α 없음 · PTFE 덮인 끝 = P0/P1 만 · `centerline + P1` · `off + P1` 거부.  Rayleigh 단조 (PTFE 늘려도 σ 안 커짐 · σ(P1) ≤ σ(P0)).
7. 극한 — `CJUNC_RJ=inf` (바닥 = 접합 간선 없음) · `=0` (천장 = 양 끝 정확 축약 · J11 단락) · 손계산 두 섬유 회로와 비교 · JSON 표지 (`rj_limit` · null) · `quantitative=False` 가 판정 경로에서 정말 막히는가.
8. 끄면 비트 같음 — 새 노브를 다 끄면 매니페스트 · 러너 영수증 · 팔 이름 · σ 가 `47d23baba` 와 바이트 같은가 (직접 두 판을 돌려 비교).
9. 사슬 (`rint_r_chain.py`) — 멈춤 코드 31 + 보정 이름 4 · 값 봉인 · 계획 파일 · 다른 판본 · 다른 킷 · 다른 sid_off 런을 섞으면 멈추는가.
10. `RINT2-B01` — 시험 작성기가 바이트를 정확히 쓰는가 (Windows 꼴 흉내: LF→CRLF 변환을 거친 뒤에도) · parser 는 그대로인가.

## 산출
`prereview_common.md` 의 형식대로 `<SCRATCH>/prereview_impl/REVIEW.md`.
