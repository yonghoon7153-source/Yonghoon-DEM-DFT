# 대피 세션 (litdb 논문 에이전트 전용) 상태 메모 — 압축 · 재시작 뒤 먼저 읽는다

갱신 2026-11-12 16:45 KST. 진행 상태의 정본 = 정본 가지 `litdb/_curation/status.tsv` (이 메모는 보조).

## ★★ 11-12 오후 — 본 세션 (stoic) 일을 전부 넘겨받음

1저자 11-12: "본 세션 (stoic) 토큰이 떨어져 litdb 를 뺀 일을 전부 여기서 이어받는다" + 논문 34 편 · "논문 에이전트는 두개 조수로 병렬로 하고 나머지 GB 터지지 않은 한에서 에이전트 돌려줘" · "Rint 등 잘 부탁" · "용훈 포메이션 지금 걸 수 있는거 잘 해주고 … 컨테이너 재시작 돼도 바로 복구가능하게 안전장치".

- 이제 이 세션 = 논문 에이전트 + **코드 가지 일**. 작업 가지 = `claude/sdcp-dem-manuscript-si-pqwtv8` (fast-forward 만 · rebase · force · merge 커밋 금지) · `claude/stoic-knuth-NObVQ` = 동결 (커밋 · push 금지). 규칙 = 그 가지의 CLAUDE.md + 인계 HANDOFF §7 (커밋 하나 → 게이트 두 조각 → push · 로컬 커밋 쌓지 않기 · 서명 끄지 않기 · 접속 주소 · 포트 · 계정 = 채팅만).
- 인계 묶음 = 이 폴더 `handoff_20261112/` 의 tgz 둘 (HANDOFF.md 를 먼저 끝까지 · 사본은 접속 정보를 가렸다 · 정독 · 종합 폴더 = litread tgz). scratchpad 에 푼 자리 = `handoff_20261112/` · `handoff_litread_20261112/`.

| 인계 절 | 상태 (11-12 17 시 KST 기준) | 다음 |
|---|---|---|
| §1 pqwtv8 ← stoic `af3cce37b` | ✅ fast-forward · push | — |
| §2 커밋 J (G2c′ 실행기 `-h` 고침 · siteq 예행 반입 · SELF-166 open) | ✅ **push 끝 18:14 KST** (`af3cce37b..21bb09d82` · fast-forward) · 게이트 두 조각 같은 HEAD 통과 = 1–125 fail 0 (2975 s) · 126–183 fail 0 (3393 s · 게이트 나무에 renice −5 를 걸었다 — 조수들과 CPU 다툼) | ▶ 커밋 K = `ef68eb7da` (860d02ac2 를 amend · SELF-167 더함 · 서명) · 첫 게이트 (nice −5) 는 t26 거짓 실패로 멈춤 (`SELF-167`) → 1 조각 다시 19:2x KST nice 0 (`gate/gate_K2_p1.log`) → 2 조각 (nice 0) → push · 내용 = SELF-166 claimed_fixed (`21bb09d8291f30dca217f595e34c2dfdb11f652c`) + 진행 기록 (11-12 인계 · 1저자 결정 · gabia 킷 확인) + 정독 종합 묶음 반입 → 사전 점검 셋 → 게이트 두 조각 → push |
| 커밋 K · L | ✅ **K push 끝** (`21bb09d82..ef68eb7da` · 게이트 두 조각 nice 0 = 183/183 실패 0 · 단계 126 mawk 다시 통과) · 로컬 = 51d45732c (믹서 Q5 시험 먼저) · f67c0cc92 (믹서 Q5 고침) · bfd9b3bbd (커밋 L = G2c′ 메모 §8 · 가린 기록 · SELF-167 claimed_fixed · SELF-168 · MXE0-01) · 사전 점검 셋 통과 | ▶ 게이트 L 1 조각 (`gate/gate_L_p1.log`) → 2 조각 → push 셋 |
| §3 G2c′ ibb 건식 다시 | ✅ 끝 (11-12 · 잡 359157 · 팔 아홉 rc 0 · 실행기 rc 0 · LMP -h rc 1 받아들임 = SELF-166 고침이 진짜 LIGGGHTS 에서 맞음) · 돌려받은 묶음 sha256 ed5bdb44… (업로드 = 1저자 · 풀기 `intake/g2cp_dry200_return_20261112/`) · 핀 대조기 (`intake/g2cp_pin_21bb09d82/`) 판독 rc 0 = 완료 문 · 등록 덱 문 지남 (덱 md5 같음 45 · 다름 0) · 예측 전부 해당 없음 (N 200 = 쌍 0 · 설계대로) · 판정 다 · 라 PASS (가르는 힘 없음) · 기록 `g2c_dry/compare_dry200.log` · ⚠ 관찰: 실행 파일 md5 = ibb 생산 lmp_mpi 0c0daccc… ≠ 11-04 샌드박스 기준 lmp_serialnovtk f4ba3ec0… → N 40000 에서도 예측 가 · 라-재현(나) 는 해당 없음이 됨 | 1저자 결정: 샌드박스 N 40000 GO · 실행 파일 (생산 lmp_mpi 그대로 = 가 · 라-재현(나) 포기 / 직렬 빌드 찾기) |
| G2c′ 샌드박스 N 40000 (1저자 11-12 "ㄱㄱ" · 잡 359243 · 생산 lmp_mpi · 1 프로세스) | ✅ **끝 · 판정 다 PASS · 라 PASS** (비트 같은 쌍 3111/3111 · 원자 1220) · 예측 13 줄 맞음 · 가 · 라-재현나 = 해당 없음 (md5 다름 · 관찰 = 11-04 출력 15 중 12 같음 · 다른 3 = restart 파일) · 예외③ 바닥 닿음 95 · 근처 13 · 받은 묶음 sha256 3caf3e05… → `intake/g2cp_run40000_return_20261112/x/` · 대조 화면 `g2c_dry/compare_run40000.log` (고정 판 대조기 md5 81c91989…) | 커밋 L (K push 뒤) = 메모 §8 + 가린 기록 (lmp_identity · ldd · libs 에 홈 경로 → 가림) + SELF-167 claimed_fixed · 1저자 11-12 "권고대로" = Q1 키트 적용 개정 초안 A + Q2 MPI 2 차 등록 초안 B → ✅ 초안 A (REG §15 개정 4 · `p1g2c/kit_amend_draft_A.md`) · 초안 B (MPI 2 차 · NP 2 · 4 · `mpi_stage2_registration_draft_B.md`) · 요약 `p1g2c/REPORT.md` (QA1–6 · QB1–5) → ✅ 내부 반박 리뷰 (P1 1 · P2 8 · P3 16 · `p1g2c/review/review_AB.md` · 가장 무거운 = P1G-01 10:0 S0′ 은 주기 restart · P1G-04 생성기 148 행 ul_s0 목록에 RT 덱 · P1G-02 생산 경로 이력 읽힘 증거 · P1G-06 '본 R = Codex GO 뒤' ↔ 11-10 예외는 믹서 E0 하나뿐 = 1저자 질문) → ▶ 고침 조수 (`p1g2c/BRIEF_fix_AB.md` · 처분 `review/disposition_AB.md`) → 짧은 재리뷰 → 1저자 비준 |
| ⚠ 게이트 K2 2 조각 중 awk 바뀜 | 조수 (믹서 조회 블록) 가 gawk 를 apt 로 설치 → 시스템 awk 가 11:03:53–11:04:03 UTC (10 s) gawk · 그 창 = 2 조각 시작 (11:01:06) +167 s = 단계 126 (rint_r_chain_e2e12 · 379 s) 도는 중 | 2 조각 실패 0 이면 단계 126 만 mawk 로 다시 (`CHECK_ALL_RANGE=126-126`) → 통과 뒤 push · 커밋 L 에 SELF-168 (조수가 게이트 중 시스템 패키지 · alternatives 바꿈 · 규칙 = 조수 지시서에 '시스템 패키지 · alternatives 바꾸지 않는다') |
| §4 Rint ② 코드 묶음 (1 순위 · GPU 팔 12 월 초까지) | ✅ 구현 · 시험 끝 (Opus 조수 19:0x KST) — 커밋 ebb0e9f80 시험 먼저 · f17ea8c6b 구현 · 2f97617ef 시험 보강 (작업 트리 `/home/user/rint-codepkg` · push 없음) · Q11 10/13 → 15/15 · 저장본 0/24 → 46/46 · 저장본 끝-끝 6/6 · 기존 3.11 묶음 A 27 · B 전부 통과 · kgy 판 3.8 25 묶음 rc 0 · 변이 89 전부 잡힘 (보강 뒤) · 끔 경로 ↔ 바탕 af3cce37b σ 같음 (신원 칸만 다름) · 보고 = 조수 답장 (STATE 에 요지) · S0 단계 1 다시 필요 (step3_sigma · payload 가 S0 일곱 파일 안) · ⑥ 시도 3 은 S0 다시를 기다리지 않아도 됨 | ✅ 내부 반박 리뷰 (Codex 아님 · 19:3x KST) = P1 1 (RCP-01 저장본 열쇠 코드 칸에 fibre_segment_raster 빠짐 → 다른 코드 판 사이 저장본 재사용 때 옛 원장 · 반례 CE1) · P2 3 (RCP-02 새 시험 게이트 밖 · RCP-03 독립 대조가 SV 팔뿐 · RCP-04 실침대 저장 가능 여부를 R 전에 잴 자리 없음) · P3 7 · 보장 ⓐ 섬 · ⓑ 깨짐 · ⓒ–ⓕ 조건부 (`rint/codepkg/review/review_codepkg.md`) → ▶ 고침 조수 (시험 먼저 · 작업 트리 커밋) → 고친 곳 짧은 재리뷰 → 본 가지로 cherry-pick (서명) → 게이트 → push → 1저자에게 S0 단계 1 다시 · ⑥ 시도 3 · GPU 확인 블록 (kgy · gabia) → Codex 봉인 전 묶음 → 개정 §10 → 봉인 → R · 1저자 결정 둘 = ⑥ 시도 3 저장본 켬 (권고 (나)) · 새 시험 셋을 게이트에 넣나 (저장본 끝-끝 7–10 분) |
| 정독 종합 묶음 (인계 §5 · 작업 지시서 `docs/reviews/dem_redesign_direction_20261109/WORKORDER_litdb_dem_mpm_reading_20261110.md` 3 절) | 조수 끝 (17:2x KST): 검증 문제 101 = 전부 96 · 일부 5 · 바꿈 212 줄 · 보류 기록 4 · 묶음 = scratchpad `synthfix/package` (133 파일 · 6.3 MB · README.md 는 이 세션이 씀) · 내 확인: 바꿈 기록 기계 대조 212/212 · 카드 재대조 2 건 맞음 · 리포 참조 검사 함수로 132 md 문제 0 · 철회값 스윕 133 파일 문제 0 · 사본 = `snap/synthfix_work.tgz` | ▶ 커밋 K 에 넣음 (게이트 → push) · 원래 계획: 본 트리의 `docs/reviews/dem_redesign_direction_20261109/litdb_reading_20261110/` 로 묶음을 통째 복사 (`cp -r synthfix/package/. <그 폴더>/`) → 사전 점검 셋 → SELF-166 claimed_fixed · 진행 기록과 한 커밋 (문서뿐) → 게이트 두 조각 → push |
| litdb 추가 필요 논문 목록 (1저자 11-12 "잘 list화 하고 있는지" → 곧바로 "ㄴㄴ litdb 다 진행하고 한번에 알려주고 · 오리진 브랜치에서 리스트화 해두고 있었는지만") | 확인 = 정본 `_curation/wishlist.md` (11-12 01:13 `51a4cbb71` 부터 · 커밋 19 · 본 세션 배치 7 + 대피 배치 17 · 항목 114 · 원문 그대로 · 중복 · 우선 정리 없음) · 대피 정독 배치 17 개의 n 절 = 17/17 옮겨짐 · 후보 표 = `_curation/S8_candidates.md` (129 행) | ⏸ 정리표 조수 멈춤 (1저자 지시) · **litdb 다 끝난 뒤 한 번에** 정리표 + pick list (지시서 `litdb_wish/BRIEF_wishlist_table.md` 그대로 다시 · 첫 판 `wishlist_table.tsv` = 성 + 해 맞춤 틀림 있음) |
| [DEM 우선 (수영)] 메모 3.2 | 초안 끝 (11-12 18:0x KST · Opus 이어받음) = `dem_redesign/memo_v3_2.md` (878 줄) + `drd_table.md` + `changelog_v3_2.md` · 조수 보고: DRD 닫힘 12 · 일부 1 (DRD-10) · SELF-160 · 161 메모 안에서 닫음 (원장은 open 그대로) · 철회값 스윕 0 (내 확인) · 1저자 질문 Q6–Q9 (F 대조 여는 조건 · 숫자 확정 시점 · 24 셀 단 · 어긋나는 카드) | ✅ 내부 반박 리뷰 (Codex 아님 · 18:4x KST) = P1 2 · P2 8 · P3 16 · DRD 닫힘 7 · 일부 6 (01 · 02 · 08 · 10 · 11 · 12) · SELF-160 · 161 일부 (`dem_redesign/review/review_memo32.md`) → ✅ 고침 (20:0x KST · P1 2 · P2 8 전부 · P3 15 고침 · 1 보류 → Q12 · 메모 1006 줄 · 카드 11 장 더함 · D2 = 두께 비 h150/h300 · 새 질문 Q10–Q12) → ✅ 2 회차 재리뷰 (1 회차 26 = 닫힘 24 · 일부 2 · 새 P1 0 · P2 6 (MR2-01 R 구간 = 두 팔 구간 전파로 · MR2-03 ②′ 사후 미끄럼 · MR2-05 ⑤ 가 W1 꼴을 보류로) · P3 12 · `review/review2_memo32.md`) → ✅ 2 회차 고침 (P2 6 · P3 12 · Q12 메모가 정함 · Q10 꼴 B (τ 값만 1저자) · 메모 1069 줄 sha c72f09ef3245 · 새로 찾은 한정 셋 · 남은 질문 Q6–Q11) → ✅ 3 회차 재리뷰 (2 회차 18 = 닫힘 15 · 일부 3 · 새 P1 0 · P2 4 (MR3-02 띠 미정 → (라) 0.565 막힘 · MR3-01 +∞ 규칙 · MR3-03 B 의 d₀ · MR3-04 결론 문장 한정 꼬리) · P3 5 · P2 수 8 → 6 → 4 로 줄어듦) → ▶ 3 회차 고침 (`BRIEF_fix3_memo32.md` · 앞 판 `memo_v3_2_before_review3.md` · 처분 `review/disposition3.md`) → 1저자 (남은 한정 · 질문 Q6–Q11) → 1저자 비준 (Q6–Q9 함께) → 재설계 docx v2 + 웹앱 → 리포 반입 |
| 믹서 E0 자격 pilot 등록 초안 (1저자 11-12 Q1 "권고대로" = 지금 문서만 · 발사 GO = 1저자) | ✅ 초안 끝 (18:3x KST · Opus) = `mixer_e0_v2/` 의 `baseline_table.md` · `e0_pilot_registration_draft.md` (20 절) · `review_brief.md` · `changes.md` · `REPORT.md` (조수 답장을 내가 옮김) · from_main 원본 그대로 확인 · 큰 발견 = 봉인된 관측기 로그 계약이 어긋나 **정상 런도 관측 TECH** [관찰 · 재현 `work/`] · 멈춤 규칙 S6 의 ERROR 세기 고침 · 1저자 질문 Q1–Q13 (권고 다 '예' 꼴) · ⚠ 조수가 Artifact 도구를 잘못 써 비공개 artifact 하나 생김 (링크는 채팅에만 · 지울지 = 1저자) | 1저자 Q1–Q13 → ibb 읽기 조회 q1–q9 (명령 블록) · 관측기 로그 계약 고침 (시험 먼저) → 재봉인 → 내부 반박 리뷰 (`review_brief.md`) → 리포 등록 → 1저자 발사 GO · G2c′ 먼저 (Q11) | · ✅ **Q5 관측기 고침 끝** (조수 · `mixer_e0_v2/fix_q5/` · 패치 0001 시험 먼저 + 0002 고침 · git am 뒤 트리 4f293308 · 관측기 시험 28/28 → 6/34 실패 → 43/43 (3.11 · 3.8) · 결함 62 꼴 TECH · 가드 끄기 25 판 모두 잡음 · 봉인 후보 = 관측기만 df22dcf0 → bb2f3229 · source_pin 일부러 뺌) · 1저자 질문 Q-A 짧은 삽입 TECH 유지 · Q-B q9 로그 대조 뒤 봉인 · Q-C 재봉인 = 별도 승인 · Q-D 옛 합성 꼴 거부 · Q-E first8 묶음 시험 HEAD 실패 = 기록만 (모두 권고 예) → 조회 블록과 함께 1저자에게 · 반입 = 커밋 L 과 같은 게이트  · ✅ **조회 블록 q1–q9 끝** (`mixer_e0_v2/query_block/query_block.txt` · 377 줄 · 파일 md5 20b2876b… · 스크립트 md5 664376ce… · 컨테이너 시험 675/0 · 쓰는 곳 = ibb 새 폴더 하나 · 명령 = sha256sum · lfs · find · sacct · ldd · sinfo · md5sum · tar · du · readelf · mkdir · squeue 뿐 (내가 훑음) · 판독기 `read_query_bundle.py`) → 1저자에게 블록 + Q-A–Q-E | · ✅ 빈칸 채움 (15 묶음 · Q-B 맞음 = 첫 낱말 수준 · 문턱 어긋남 없음 · E6 다시 씀 · 남은 [미확인] = 기본 할당 · MaxRSS 등 · 새 질문 Q-F q9b 보충 조회 · Q-G 라이브러리 30 목록 봉인 + 발사 직전 q7 · Q-H 관리자 할당 문의 · `fill_report.md`) → ▶ 내부 반박 리뷰 (`BRIEF_review_run.md` + `review_brief.md` · G14–G16 더함) |
| §5 열린 일 | 포메이션 = `snap/formation_20261112.md` | 걸 수 있는 것부터 조수로 |
| §6 논문 34 편 (N-2 … N-51) | PDF 전부 받음 · 대기열 · status 반영 (정독 NN 44–91 = 본 세션이 정한 번호 · 논문별 지시 = 인계 묶음 `litdb/prompts/`) | 1 순위를 2 · 3 순위보다 먼저 · 둘 병렬 |

- **1저자 11-12 저녁 "다 권고대로"** = ① 논문은 넘겨받은 1 순위 34 편 (N-2 부터 번호순) 을 2 · 3 순위보다 먼저 ② 믹서 E0 자격 pilot = Rint 코드 묶음 반입 뒤 리포 등록 문서에서 다시 잡음 (인계 묶음에 초안 · 리뷰 지시서 없음) ③ 커밋 J 는 게이트 두 조각 실패 0 뒤에 push (건너뛰지 않음). → 코드 가지의 진행 기록 (`docs/session_20260923_progress.md`) 에는 다음 코드 커밋 (SELF-166 claimed_fixed) 때 같이 적는다.
- 지금 도는 조수 (11-12 17:53 KST · 전부 Opus): 논문 N-15 (트리 1 · 정독 57 · 19:26 시작) · N-16 (트리 2 · 정독 58 · 19:52 시작) · Rint 코드 묶음 (`/home/user/rint-codepkg`) · 메모 3.2 초안 (`dem_redesign/`) · 믹서 E0 pilot 등록 초안 (`mixer_e0_v2/`) + 게이트 커밋 J 2 조각. 논문 끝 = 16 편 (N-52 · 53 · 54 · 55 · 56 · 60 · 61 · 62 · 63 · 64 · N-2 · N-5 · N-10 · N-11 · N-12 · N-14). 다음 차례 = 1 순위 번호순 (N-17 → N-19 → N-20 → …). 에이전트 지시문에 넣는 줄: 다른 트리 넷을 읽지도 쓰지도 않기 · `extract_figures.py --clean` 뒤 `_sources.json` 의 다른 카드 줄 확인 · 큰 렌더는 한 장씩 · 신호 실험 금지 · 커밋 끝 줄 = `tools/trailer.txt`. · 에이전트 지시문에 'Artifact 도구 · 웹 게시 도구 쓰지 않기' 줄 더함 (믹서 조수 사고 뒤).
- 11-12 17:3x KST 사용량 한도 오류로 조수 넷 (논문 N-2 · N-5 · Rint 코드 묶음 · 메모 3.2) 이 한꺼번에 멈춤 → 1저자 "다시 시도해 주세요" → 17:36 KST 에 SendMessage 로 끊긴 자리에서 잇게 함 (새로 띄우지 않음 · 트리의 커밋 전 작업 그대로). 같은 일이 또 나면: 조수 id 는 ListAgents 로 · 트리 상태 확인 → SendMessage "끊긴 자리에서 이어서". 정독 종합 고침 조수는 그 전에 끝남 (17:2x). 게이트 (셸) 는 한도와 무관하게 계속 돈다.
- ★ 1저자 11-12 17:4x KST "지금 진행하는거 전부 opus로 낮춰서 다시 진행해줘" → 조수 넷을 멈추고 (TaskStop) **Agent `model: "opus"`** 로 다시 띄움 (같은 지시서 · 트리의 커밋 전 작업 · 메모를 이어받게 함). **앞으로 띄우는 조수 (논문 에이전트 포함) 도 전부 `model: "opus"`.** 커밋 트레일러 = `tools/trailer.txt` (지금 Opus 5.5 줄 · 하네스가 알려 준 대로).
- ★ 1저자 11-12 20:0x KST "다 권고대로해줘 · 믹서들 q14도 지워줘" = 믹서 E0 Q1–Q13 권고대로 · Q14 비공개 artifact 지움 (확인됨) · Rint ⑥ 시도 3 = 저장본 켬 · 새 시험 셋 게이트에 넣음 · 메모 3.2 Q6–Q9 권고대로 (F 대조 = 단계 1 메모리 셈이 상한 안일 때만 · 숫자 = 등록 때 확정 · 24 셀 단 넣음 · 어긋나는 카드 = 보고만 · 기준 그대로). 믹서 조수 둘 띄움 (ibb 읽기 조회 블록 q1–q9 = `mixer_e0_v2/query_block/` · 관측기 로그 계약 고침 + 재봉인 후보 = `mixer_e0_v2/fix_q5/`).
- 재시작하면: 아래 '멈췄다가 이어갈 때' 3 번의 `restore.py` 한 번 — 이제 코드 가지 쪽도 한다 (리포 unshallow + 관련 가지 받기 = `check_doc_refs` 가 요구 · pip (`--ignore-installed blinker` 먼저) · kgy 판 3.8 · 인계 묶음 풀기 · Rint 작업 트리를 `snap/` 에서 되살림).
- 스냅샷: `finish.py` 가 돌 때마다 (논문 한 편 끝 · `--sync-only`) `snap/` 에 Rint 작업 트리 (커밋 bundle · 커밋 전 diff · 새 파일 · 메모) 와 본 트리 (push 안 된 커밋 · 커밋 전 diff) 를 묶어 올린다 → 잃는 것은 마지막 스냅샷 뒤의 일뿐.
- 게이트는 약 2 시간 (CPU 4 를 조수와 나눠 쓰면 더) — 끊기면 즉시 보고하고 조각을 다시 띄운다 · 게이트 중에는 본 트리를 건드리지 않는다. ⛔ 게이트를 nice · renice 로 띄우거나 올리지 않는다 (11-12 `SELF-167` — 실행기 시험이 자식 nice 19 를 단언).
- gabia · kgy 킷 확인 (1저자 11-12 16:35 KST 실행 결과): 두 기계에서 킷별 내용 해시 같음 — `kit_SBE_vgcf100` 168823a6…f533d7 (파일 23) · `kit_DBE_sdcp1um_vgcf100` 6a9301b2…526d9e (파일 19) · 링크 2 + 2 (= 본 세션 기록 '파일 42 · 링크 4' 와 맞음). gabia 쪽 링크 넷 (`latest_run` · `scripts` × 2) 은 끊김 — kgy 홈 절대 경로를 그대로 담고 있다. 코드 읽기 (관찰 · 시험 전): 러너 `scripts/sdcp_gain_vox015_8arm.sh` 716 행 = `latest_run` 이 없으면 `run_*` 중 `se_dump.npy` 있는 마지막 폴더로 넘어감 · 러너의 `SCR` 은 러너 자신의 폴더 (108 행) 라 킷의 `scripts` 링크는 R 에서 안 쓰임 (킷 자체 `run_mpm.sh` = STEP2 만 씀). ✅ 1저자 17:4x KST gabia 실행 = 두 킷 모두 `se_dump.npy` 있는 run 폴더 1 개 · `latest_run` 을 상대 링크로 고침 (살아 있음) · 고친 뒤 내용 해시 그대로 (168823a6… · 6a9301b2…) → 두 기계가 같은 규칙으로 같은 run 폴더를 잡는다. 남은 것 = gabia 의 `scripts` 링크 둘 (R 에서 안 쓰임 — R 핀 사본이 gabia 에 생긴 뒤 맞춤 · 계획 §10 의 4 번).

## ★ 멈췄다가 이어갈 때 (토큰 소진 · 압축 · 컨테이너 재시작) — 이 절부터 읽는다

이 파일의 사본이 정본 가지 `litdb/_curation/evac/STATE.md` 에 있다 (도구 사본 = `litdb/_curation/evac/tools/`). 진행 상태의 정본은 `litdb/_curation/status.tsv`.

1. 상태 보기: `git -C /home/user/litdb-ctl fetch origin claude/friendly-meitner-lldvar` → `git -C /home/user/litdb-ctl rebase origin/claude/friendly-meitner-lldvar` → `status.tsv` 에서 세션 칸이 '대피' 인 줄을 본다. **'도는 중' = 멈출 때 돌던 편.**
2. 돌던 편의 뒷정리 (트리 1 = `/home/user/litdb-canon` · 트리 2 = `/home/user/litdb-canon2`):
   - `git -C <트리> status --short` 가 비어 있고 원격에 그 논문 카드 커밋이 있으면 (`git log origin/claude/friendly-meitner-lldvar --oneline | head`) 에이전트는 끝낸 것이다 → `python3 -I <scratchpad>/tools/finish.py --key <키> --slug <slug> --commit <sha> --memo "<한 줄>"` 로 마무리 (모음 그림 = `<scratchpad>/litcards/<slug>_sheet*.png` → 1저자에게 보냄).
   - 트리가 더럽거나 (쓰다 만 카드 · 그림) 커밋이 없으면 에이전트가 중간에 멈춘 것이다 → ① 에이전트가 살아 있으면 (ListAgents) SendMessage 로 "지시서대로 이어서 끝내라" ② 없으면 쓰다 만 것을 `git -C <트리> stash -u` 로 치워 두고 (지우지 않는다) 같은 키로 다시 띄운다 (정독 NN 그대로 · `launch.py`).
3. 컨테이너가 새로 떴으면 (`/home/user/litdb-ctl` · scratchpad `tools/` 가 없다 = 재시작된 것) — **복구 도구 한 번**:
   ```
   git -C /home/user/Yonghoon-DEM-DFT fetch origin claude/friendly-meitner-lldvar
   git -C /home/user/Yonghoon-DEM-DFT show origin/claude/friendly-meitner-lldvar:litdb/_curation/evac/tools/restore.py > /tmp/restore.py
   python3 -I /tmp/restore.py --scratch <이 세션의 scratchpad 경로> --uploads /root/.claude/uploads/<세션 id>
   ```
   패키지 (PyMuPDF 1.28.2 등) · 작업 트리 셋 · scratchpad 도구 · stage · inbox (업로드 폴더가 남아 있을 때) · 참고 저장소 셋 · 그림 도구 selftest 를 한 번에 다시 만들고, inbox 를 받은 파일 목록 (`tools/received_files.tsv` — 170 파일 · 이름 · 크기 · sha256) 과 견줘 없는 번호를 찍는다. 11-12 에 빈 자리에서 시험: 업로드 폴더만 있으면 inbox 170/170 이 이름 · 해시까지 똑같이 다시 만들어진다.
   - 그 뒤 `tools/trailer.txt` 에 이 세션의 커밋 끝 두 줄을 적는다 (정본에 없다).
   - **업로드 폴더가 사라졌으면** PDF 는 복구할 수 없다 (PDF 는 저작권 때문에 공개 가지에 올리지 않았다) → 1저자에게 '차례 기다림' 번호의 파일을 다시 올려 달라고 한다 (PushNotification 한 번 + 답장에 번호 목록). 그동안 띄울 수 있는 것이 없으면 멈춘다 — status.tsv 의 '도는 중' 줄은 '차례 기다림 (재시작으로 끊김)' 으로 고쳐 push 한다.
   - 재시작으로 끊긴 편 (status '도는 중' 인데 원격에 카드 커밋이 없음) 은 처음부터 다시 띄운다 (에이전트 기록도 사라져 SendMessage 로 못 잇는다).
4. 다음 차례 = status.tsv 의 '차례 기다림' 을 N 번호순으로 · 한 번에 둘 (트리 1 · 2) · **기존 카드 보강 (68-1 zhang2026 · 68-2 lyu2025 · N-148 · N-149) 은 맨 끝** (다른 에이전트가 같은 카드에 관련 카드 줄을 더하므로).
5. 한 편이 끝날 때마다: 모음 그림을 1저자에게 보냄 → `finish.py --key … --next <다음 키> --tree <1|2>` (status · wishlist · 이어가기 자료 push + 다음 지시문 출력) → 그 지시문으로 `litdb-curator` 에이전트를 띄움 → 1저자에게 표로 보고 (12 줄 안 + 의도 대조 한 줄).

1저자가 새 세션에 붙여 넣을 말 (이 세션이 아예 사라졌을 때):
> [논문 에이전트 전용 세션 이어가기] 정본 가지 `claude/friendly-meitner-lldvar` 를 받아 `litdb/_curation/evac/STATE.md` 를 처음부터 끝까지 읽고 그대로 이어서 해줘. 쓰는 곳은 그 가지 하나뿐이고 코드 · 문서 가지에는 아무것도 커밋 · push 하지 않는다. PDF 는 내가 다시 올려 줄게.

## 역할 (1저자 11-12)

- 이 세션은 litdb 논문 에이전트 일 (카드 · 크롭 · 정본 push) 만 한다. 코드 · 문서 가지 (pqwtv8 · stoic) 에는 아무것도 커밋 · push 하지 않는다. 쓰는 곳 = 정본 가지 `claude/friendly-meitner-lldvar` 하나 (litdb 한정 상시 승인).
- 맡은 것 = 후보 표 2 · 3 순위 N-52 부터 (제외: N-57 · N-58 · N-59 · N-72 첫째 — N-119 는 제외했다가 1저자가 PDF 를 찾아 **취소** (11-12) = 후보로 남는다). 1 순위 N-1–N-51 은 본 세션 몫 — 하지 않는다.
- 에이전트는 한 번에 둘까지. 끝날 때마다: 모음 그림 (sheet png) 을 SendUserFile 로 보내고 · status.tsv 를 끝 (slug · 커밋) 으로 고쳐 push · 한국어 12 줄 안 보고 + 의도 대조 한 줄.
- 정본 push 규칙 = `litdb/_curation/README.md` 2 절 (시작 · push 직전 fetch · rebase · 충돌은 두 쪽 줄 다 살림 · 강제 push 금지 · INDEX_DEM 은 build_index.py 로 재생성).
- wishlist: 에이전트의 정독 출력 `## n` 절에서 내가 `litdb/_curation/wishlist.md` 로 옮긴다 (꼴 = 그 파일 머리 · 서지는 원문 목록 그대로 · 모르면 [미확인]).
- 보고 = 한국어 · 짧게 · 표 위주 · 숫자는 원문에서만. 커밋 끝 두 줄 = 그 세션의 공동 저자 줄 · 세션 줄 — scratchpad `tools/trailer.txt` 에 두고 정본에는 올리지 않는다 (새 세션은 자기 두 줄을 그 파일에 적는다 · 그 밖의 글 · 문서에는 모델 이름을 쓰지 않는다).

## 자리

| 무엇 | 경로 |
|---|---|
| 에이전트 트리 1 | `/home/user/litdb-canon` (가지 tmp-litdb-evac) |
| 에이전트 트리 2 | `/home/user/litdb-canon2` (가지 tmp-litdb-evac2) |
| 내 기록용 트리 (sparse · _curation 만) | `/home/user/litdb-ctl` (가지 tmp-litdb-evac-ctl) — status.tsv · wishlist.md 커밋은 여기서 |
| 받은 PDF | 두 트리의 `litdb/inbox/` (git 무시) · 원본 = `/root/.claude/uploads/<세션>/` · 단계 폴더 = scratchpad `stage_20261112/N-xx/` |
| 대기열 · 지시서 재료 | scratchpad `tools/queue.json` (N → nn · pdf · si · extra · bib · model · dup · note) |
| 지시서 만들기 + Agent 지시문 찍기 | `python3 -I <scratchpad>/tools/launch.py N-xx <트리> <가지>` → `briefs/brief_N-xx.md` + 짧은 지시문 |
| 모음 그림 도구 | `python3 -I <scratchpad>/tools/make_sheet.py --figdir … --out <scratchpad>/litcards/<slug>_sheet.png` |
| 환경 | PyMuPDF **1.28.2** (2.1 은 selftest 1 건 실패) · Pillow 13 · numpy · openpyxl · ffmpeg 있음. 재시작 뒤: `python3 -m pip install "pymupdf==1.28.2" pillow numpy openpyxl` → `extract_figures.py --selftest` 84/84 확인 |

재시작으로 트리가 사라졌으면: `git fetch origin claude/friendly-meitner-lldvar` → `git worktree add ../litdb-canon origin/claude/friendly-meitner-lldvar -b tmp-litdb-evac` (canon2 · ctl 도 같은 꼴 · ctl 은 `--no-checkout` + `git sparse-checkout set '/litdb/_curation/'`) → inbox 에 PDF 다시 복사.

## 대기열 (받은 PDF · 정독 NN) — 11-12 갱신 (1저자: "지금 먹여준 것들 다 논문 에이전트 돌린다")

차례 = 두 줄 (트리 1 · 트리 2) 로 번호순. 도는 중 / 끝은 status.tsv 를 본다. queue.json 키 = 표의 '키'.

| 키 | NN | 논문 | 메모 |
|---|---|---|---|
| N-52 | 101 | Taghikhani 2025 JMPS 198 106060 | 트리 1 · 11-12 10:40 KST 시작 |
| N-53 | 102 | Lu 2020 Joule 4 2746 (+SI) | 트리 2 · 11-12 10:40 KST 시작 |
| N-54 | 103 | Paulick 2015 Granular Matter 17 83 | 같은 저자 · 해 다른 카드 있음 |
| N-55 | 104 | Meyer 2017 JMPT 249 172 | |
| N-56 | 105 | Song 2025 Powder Technol 453 120667 (+SI) | 2 GPa 문턱 출처 |
| N-60 | 106 | Onoda–Liniger 1990 PRL 64 2727 | 스캔본 |
| N-61 | 107 | Meyer 2018 J Energy Storage 18 371 | N-55 가 끝난 뒤 (서로 가리키게) |
| N-62 | 108 | Cottrino 2013 Mater Charact 81 111 | |
| N-63 | 121 | Dixit 2022 ACS Energy Lett 7 3936 (본문 + 보충 PDF + xlsx 2) | 본문 PDF 받음 (11-12) |
| N-64 | 116 | Hayashi 2025 J Jpn Soc Powder Powder Metall 72 S1167 | |
| N-65 | 117 | Swinkels 1983 Acta metall 31 1829 | 스캔본 |
| N-66 | 118 | Ebner 2013 AEM 3 845 (+SI) | zhang2026 카드에 관련 카드 줄을 더한다 |
| N-67 | 119 | Ge 2022 Powder Technol 403 117366 | 〃 |
| N-68 | 122 | **Sonzogni 2024 Powder Technol 442 119891** (68-3 번 파일) | zhang2026 · lyu2025 카드에 관련 카드 줄 |
| X-68 | 115 | Kashkooli 2016 JPS 307 496 (+SI) (68 번 파일) | 후보 밖 · status.tsv 줄 이름 '후보 밖 (68 번 파일)' |
| N-69 | 120 | Stershic 2015 JPS 297 540 | zhang2026 카드에 관련 카드 줄 |
| N-70 | 109 | Xu 2023 Batteries & Supercaps 6 e202300371 (+SI · 영상 3) | 후보 표의 e202300525 는 원문과 다름 (카드 문제) |
| N-71 | 110 | Silbert 2001 PRE 64 051302 | |
| N-72 | 111 | Walton 1993 Mech Mater 16 239 (둘째) | 첫째는 제외 |
| N-73 | 112 | Chouchane–Franco 2021 B&S 4 1451 (+SI · 영상 1) | |
| N-74 | 113 | German 2014 Powder Technol 253 368 | |
| N-75 | 114 | Mullikin–Verbeek 1993 Bioimaging 1 6 | 스캔본 |
| X-68-1 | 123 | **기존 카드 보강** zhang2026_xct_dem_cathode_calendering_peel_calibration (68-1 번 파일) | ⚠ 맨 끝에 — N-66 · 67 · 68 · 69 가 다 끝난 뒤 (같은 카드를 건드린다) |
| X-68-2 | 124 | **기존 카드 보강** lyu2025_3d_dem_drying_calendering_lib (68-2 번 파일 + 영상 4) | ⚠ 맨 끝에 — N-68 이 끝난 뒤 |

3 순위 (N-76–N-129) 와 4-2 보강 (N-148 · N-149) 은 **11-12 에 전부 받았다** (1저자 "마지막이양"). 대기열 = `tools/queue.json` 79 항목 · status.tsv 에 한 줄씩 있다 (정독 NN 은 띄울 때 `launch.py` 가 '지금까지 쓴 가장 큰 NN + 1' 로 배정 — 125 부터).

| 키 | 논문 | 메모 |
|---|---|---|
| N-76 … N-129 | status.tsv 의 메모 칸에 서지 | 번호순 · 자동 항목 (서지 = PDF 문서 정보 + 첫 쪽 — 에이전트가 첫 쪽에서 다시 확인) |
| N-112-1 · N-112-2 | Li–McCarthy 2003 PRL 90 184301 · 2005 PRE 71 021305 | 후보 표 N-112 한 행 = 논문 둘 → 에이전트 둘 · status 줄 이름 'N-112 첫째' · 'N-112 둘째' |
| N-114 | Thiel–Lai–Hersey 1981 (114-1) + Egermann 1980 Powder Technol 26 235 (114-2 · 후보 밖) | 에이전트 하나가 카드 둘 → `finish.py` 는 첫 카드 slug 로 · 둘째 카드 slug · 커밋은 메모에 손으로 |
| N-105 | Ji 2025 Nat Commun 16 7667 | 보충 3 (260 MB) 은 원자료 xlsx · README 만 받음 |
| N-107 | Chouchane 2024 ACS Energy Lett | 참고 저장소 `/home/user/lescopenaccess/codes-and-data` (읽기 전용 · 실행 금지 · .pkl 열지 않음) |
| N-124 | Adam 2026 Mater Horiz 13 6380 | 참고 저장소 `/home/user/adama-wzr/effectivediffusivityfvm` (읽기 전용) |
| N-128 | Liu–Roters–Raabe 2024 Nat Commun 15 7970 | 참고 저장소 `/home/user/damask-multiphysics/damask` (태그 v2.0.2 · 읽기 전용 · 이 논문의 화학–역학 구현은 비공개 가지라고 원문이 적음) |
| N-148 | **기존 카드 보강** tron2023_rational_cathode_composite_optimization_lpscl ← 보충 자료 (SI PDF 4 쪽) | ⚠ 맨 끝에 |
| N-149 | **기존 카드 보강** boger2023_thermal_conductivity_argyrodite_lgps ← 본문 + 보충 두 파일 | ⚠ 맨 끝에 |

참고 저장소는 컨테이너가 새로 뜨면 사라진다 → 그 논문을 띄우기 전에 다시 받는다 (`GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 [--branch v2.0.2] https://github.com/<owner>/<repo> /home/user/<owner>/<repo>` · 소문자 경로 · 지시서의 경로와 같게).

## 자동 점검 (1저자 11-12: "내가 반응안해도 컨테이너 재시작됐을때 다 안날라가게 조심해줘")

- 이 세션에 **2 시간마다 깨우는 점검** 이 걸려 있다 (scheduled task · 이름 '논문 에이전트 대기열 점검 (대피 세션)' · 재시작 뒤에도 온다). 오면: 트리 · scratchpad 가 없으면 위 3 번 복구 → 대기열 잇기 / 있으면 에이전트 생사 · 처리 안 한 편 · 한도로 멈춘 에이전트를 본다 / 할 일이 없으면 한 줄로 끝. 대기열이 다 끝나면 지운다 (list_triggers → delete_trigger).
- 재시작 때 지켜지는 것 = 끝난 카드 · 크롭 (편마다 push) · status.tsv · 이 폴더 (대기열 · 도구 · 받은 파일 목록). 지켜지지 않는 것 = 돌던 에이전트의 쓰다 만 것 (많아야 두 편) · PDF 자체 (업로드 폴더가 남아 있으면 `restore.py` 가 inbox 를 똑같이 다시 만든다 · 사라지면 1저자가 다시 올려야 한다).
- 로컬 커밋을 쌓지 않는다 — litdb-ctl 의 커밋은 `finish.py` 가 그 자리에서 push 한다 · 에이전트도 카드 커밋을 바로 push 한다.

## 열린 것

- **사용량 한도로 에이전트가 끊기면** ("out of usage credits" 로 failed 알림): 그 에이전트의 트리는 쓰다 만 채로 남는다 (미추적 그림 폴더 · `_sources.json` 수정). 1저자가 초기화권을 쓴 뒤 "이어서" 라고 하면 → `SendMessage(to=<그 에이전트 id>)` 로 "끊긴 자리에서 이어서 끝까지 · 트리 상태 그대로 · push 직전 fetch · rebase" 를 보낸다 (11-12 N-56 에서 이렇게 이었다). 에이전트 id 를 모르면 (세션이 바뀜) 위 2 절의 '없으면' 절차.
- 에이전트가 끝나면: ① 답장의 slug · 커밋을 정본에서 확인 ② 모음 그림을 열어 보고 SendUserFile ③ `finish.py --key … --slug … --commit … --memo … --next <다음 키> --tree <1|2>` ④ 찍힌 지시문으로 `litdb-curator` 에이전트 ⑤ 12 줄 보고 + 의도 대조 한 줄.
- 에이전트 한 편 = 43–72 분 · 30–75 만 토큰 (쪽 수 · 보충 자료에 따라). 남은 편수가 많으니 한도에 자주 닿을 수 있다 — 닿으면 위 절차.
- 키트 README 6 절 (환경 메모) 은 이 세션이 더했다 (`533c30320`).

- 11-12 끝난 것: N-52 (1ef7e9486) · N-53 (5fb0272d7) · N-54 (9c6ff51aa) · N-55 (b6f5f591c) · N-60 (063da4bc7). 도는 중 (14:00 KST 기준): N-56 (트리 2 · 한도로 한 번 끊겼다가 이어서) · N-61 (트리 1). 다음 차례: N-62 → N-63 → N-64 → N-65 → N-66 → N-67 → N-68 → X-68 → N-69 → N-70 → … → N-75 → N-76 … N-129 → 보강 넷 (X-68-1 · X-68-2 · N-148 · N-149).
- **1저자 11-12 (litdb 보고)**: *"litdb 다 진행하고 한번에 알려주고"* — 편마다 보고 · 시트 보내기 멈춤 · 끝 (또는 큰 매듭) 에 한 번에: 편별 핵심 값 표 + 시트 경로 + 카드 문제 + 추가 필요 논문 정리표 · 끝난 편 = N-15 (sadeghirad2011 `52c378da0`) · N-16 (bardenhagen2004 `f3d6d0b14`) · 도는 편 = N-17 (트리 1) · N-19 (트리 2) · 다음 N-20.
- **1저자 11-12 믹서 Q-A–Q-E "권고대로해줘"**: Q-A 짧은 삽입 (thermo 표 안 'Less insertions than requested') = 기술 실패 유지 · 등록 초안 E6 문구를 그에 맞게 · Q-B 봉인 전 허용 줄 목록 ↔ q9 (NP20 E0 실제 로그 줄 꼴) 대조 · Q-C 관측기만 바뀐 후보로 재봉인 · 핀 = 패치 넣은 커밋 (재봉인 실행 = 별도 승인 단계) · Q-D 옛 합성 로그 꼴 거부 수용 · Q-E first8 묶음 시험 HEAD 실패 = 기록만 · 조회 블록 = 1저자가 ibb 에서 돌림 (돌아오면 빈칸 채움 → 내부 반박 리뷰).
- **11-12 믹서 조회 블록 실행 (1저자 · ibb)** = 91 s · 조회 OK 54 · FAIL 1 (q4 의 하나) · 가림 확인 0 곳 · 묶음 `mixer_e0_query_20261112T115236Z.tgz` 18808 B · sha256 a5753648e0ac34574fa8f5fa231366338093663a1155f549775a5f5ffc95beb0 → 받으면 새 빈 폴더 · 판독기 `read_query_bundle.py` · 빈칸 채움 (E6 문구 = Q-A) → 내부 반박 리뷰.
- **11-12 믹서 조회 묶음 받음** = sha256 a5753648… 같음 · `intake/mixer_e0_query_20261112/` (금지 목록 forbid.txt = 채팅 값 · 리포 · 대피 묶음에 넣지 않음) · 판독기 rc 0 · q2 74.1 step/s · 프레임 8.36–12.7 MB · q4 기본 할당 Permission denied (사용자 한도 0) · q5 OST 8 최소 여유 14.6 TB · q6 MaxRSS 다섯 다 None (walltime 3:07–6:48) · q7 바이너리 = 09-28 같음 · RPATH = 사용자 conda env · q9 표 1 비-행 INFO: 1 · - 1 (삽입 보고 꼴) · ▶ 채움 조수 (`BRIEF_fill_after_query.md`) → 내부 반박 리뷰.
- **litdb 끝 묶음 보고 메모** = scratchpad `litdb_final_report_notes.md` (편마다 한 줄 · N-15 · 16 · 17 들어감 · N-17 = 받은 PDF 가 ChemRxiv 프리프린트 → 출판본 + SI 필요) · 도는 편 N-19 (트리 2) · N-20 (트리 1) · 다음 N-24.
- litdb 진행: N-19 끝 (ai2011 `81d79396d`) · 도는 편 = N-20 (트리 1) · N-24 (트리 2) · 다음 N-26.
