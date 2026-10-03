# ① r_int 적대 자기리뷰 결과 (10-02 밤 · 에이전트 · 프로브 = scratchpad/rint_review/) — 압축 대비 메모

> ⛔ **Codex 판정 (10-03) = G1 HOLD · G2 HOLD** (`docs/reviews/codex_review_rint_stage1_20261003.md`) — P1-1 CONFIRMED = `RINT-01` (예고했던 `SELF-81` 은 이 항목으로 갈음) ·
> P2-3 확대 = `RINT-02` (wetted/bare 솔브까지 · 제안 검사로는 놓친다) · P2-4 = `RINT-04` · `RINT-05` · P2-1 의 (b) 처방은 위치를 못 고친다 (`RINT-06`) · 단위 `RINT-07` · D4 `RINT-08` ·
> P3 아홉 = `RINT-11`~`19` · 새 관찰 = `RINT-03` (r-OFF 입자별 AM 전류 오염 121–127×).

판정: rint 은 기본 OFF 선택 기구로 안전 (rint=None 19/19 격자 비트 동일 · 단위 SI 독립 검산 −3.2e-14 · 소산 항등식 ON 에서도 |Δ| 1.55e-7 · JSON 안전 · 메모리 OK). ② 진입 전 수정 필요.

| # | 내용 | 재현 | 수정 (반례 먼저) |
|---|---|---|---|
| P1-1 ✅재확인 | 같은 상 비-AM 쌍 (VGCF\|VGCF 등) 이 **AM 입자 번호 pid3** 로 판정 — 첨가제 스탬프가 sid 만 바꾸고 pid 는 AM 번호 유지 | p8b_neck.py: 한 가닥 VGCF 안에 pid 0/1/2 → VGCF\|VGCF=1e-2 에서 σ_e 0.0635649 → 0.0020275 (−96.8 %) · 원장에 실물처럼 찍힘 (내가 재실행해 같은 값) | same-sid 쌍은 AM_S\|AM_S · AM_P\|AM_P 만 허용 (파서 + 솔버 PID_OWNER_SIDS) · ②③ 은 별도 번호 격자 |
| P2-1 | r 를 복셀 **면**마다 → 접촉 면적 = N·vox² (격자 산물) · §3 "격자 무관" 문장과 모순 · §8 미기재 | p7b_tilt: 기울인 평면 1.000/1.231/1.363/1.396 (θ 0/15/30/45) · 구 표면 N·vox²/4πR² = 1.5 (vox 0.05 도) · AM 목 πa² 의 5.99×(0.4)/2.67×(0.15)/1.84×(0.05) · VGCF 접선 접촉 N≈6 고정 · p12_chain: 계면 분담 0.067→0.129 (vox 0.2→0.05) 비수렴 | **1저자 결정**: (a) 법선 L1 보정 r·(\|nx\|+\|ny\|+\|nz\|) (b) 접촉 (pid_i,pid_j) 별 참 면적 정규화 (DEM Hertz/Stage-E a²) · 권고 = 혼합 (해상되는 계면 a · 점 접촉·섬유 b) · §8 에 세 바이어스 명기 · ⑤(b) vox 사다리는 이대로면 수렴 불가 |
| P2-2 | CLI 무효 쌍 · 반복 플래그 무음 | p9: 45 쌍 중 전자 30 · 이온 39 쌍이 그 채널 σ=0 · SE\|SE 이온 r 줘도 면 0 인데 interface_model 찍힘 · 플래그 두 번 → 둘째만 · 값 없는 플래그 → 무음 OFF | action=extend + nargs='+' · 채널 σ 표로 쌍 검사 거부 · 해 뒤 r>0 ∧ 면 0 쌍 기록·경고 |
| P2-3 | rint ON 경로 지키는 게이트 없음 | 변이 (주 전자 솔브 rint= 한 줄 삭제) → σ_e = OFF 값인데 매니페스트는 r1 · 규칙 J · selftest 전부 초록 | 규칙 J rint ON 팔 (n_faces>0 ∧ σ_e<OFF) · 판정기 계약 interface_model≠None ⇒ 풀린 채널마다 interface_faces[ch].table = 기록 표 |
| P2-4 | 한 payload 안 규약 혼합 무표지 | rxn :2737 · trust :2752 · STEP4 npz :2771 (표 미저장) · 전자 trust :2070 · Joule (p11: 실제 소산 interface 0.762 인데 맵은 bulk 만) | 표지 또는 rint+--save-step4-grid 거부 · Joule 계면 몫 표지 — ④⑤ 전 |
| P3 | ① r=0/무관 쌍에서 분담 ULP 차 + interface 0.0 키 (→ _rint 맥락을 n_faces>0 일 때만) ② 솔버 API 조용한 변환 (1.7,3)→(1,3) · True→1.0 · (0,3) 왕복 실패 ③ compare_dirs OFF↔ON: interface_model derived_from 없음 → HOLD ④ --step3-rint-i + --no-ion 세대 필드 ⑤ NODIGEST → 러너 OUTDIR 태그가 ON/OFF 못 가름 (⑤ 배선 때 SKIP 캐시 함정) ⑥ interface 버킷 쌍 합산 → 쌍별 −∂lnσ/∂ln r 따로 ⑦ 이름 충돌 interface_rint_* vs r_int_ohm_cm2 (셀 ASR) ⑧ viewer3d.js:5340 "각 상의 전력손실 %" 에 interface 막대 ⑨ rint_ctx_from sid 호출자 것 | |

순서: ② 진입 전 = P1-1 · P2-2 · P2-3 (+P3-1 · P3-2) · ② 설계 전 = P2-1 결정 · ④⑤ 전 = P2-4 + P3 나머지.  원장: SELF-81 (P1-1 · 내 결함) 등재 예정.
